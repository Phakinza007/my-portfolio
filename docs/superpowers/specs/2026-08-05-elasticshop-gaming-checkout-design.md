# Elasticshop Gaming — Functional Checkout Design

## Context

`elasticshop-gaming.html` is a portfolio case-study page: a polished four-screen UI prototype (Home → Top Up → History → Status) for a fictional game top-up shop. Visually it's complete — real pricing math, working filters, a package grid, a step indicator. But underneath, most of it is disconnected:

- Every game tile on Home routes to the same hardcoded checkout ("RoV: Arena of Valor"), regardless of which game was clicked.
- The step indicator shows three steps (Player Info → Package → Payment), but there's no actual Payment screen — "Confirm & Pay" fires straight from the Package screen.
- Completing a checkout shows a Status screen, but that order never appears in History. History only ever shows 3 hardcoded demo transactions, unaffected by anything the visitor does.
- "Login" navigates to the History screen and does nothing resembling login.

The goal is to make this a genuinely functioning demo — a visitor can pick any game, go through a real multi-step checkout including an actual payment-method choice, see their order land in History, and revisit it later (persisted across reloads). This is scoped as a demo: **client-side only, no backend, no real payment gateway, no real money, no real game top-up delivery.** That scope was chosen explicitly over standing up real infrastructure, because the latter requires business/merchant accounts only the site owner can create (see the Non-goals below) — nothing here should read as if it processes real transactions.

## Goals

1. Clicking any game tile on Home carries that game's identity through the entire checkout and into the resulting order.
2. "Payment" becomes a real step: a method-selection screen (Card / PromptPay / TrueMoney) sits between Package selection and order confirmation.
3. A completed checkout persists as a real order (`localStorage`) and appears in History immediately, on top of the existing seed/demo transactions — using the exact same transaction-card markup and filter logic already built.
4. Payment method affects the outcome realistically, reusing screens that already exist: Card → instant success. PromptPay / TrueMoney → the existing "Pending" status screen, resolved by the existing refresh button.
5. "Login" becomes a lightweight local nickname capture (no password — there's nothing to check one against) that personalizes the nav and the History profile card.

## Non-goals

- No real payment gateway integration (Omise, 2C2P, Stripe, PromptPay API, etc.) — these require a registered merchant account, which is a business decision outside this task.
- No real game top-up fulfillment — no game publisher or top-up-vendor integration exists or is implied.
- No backend, no database, no user accounts with real authentication. Everything lives in the visitor's own browser (`localStorage`) and is private to that browser/device.
- No new "failed payment" status screen — only the two outcomes (`success`, `pending`) that already have built UI are used. Card payments never fail in this simulation; that's an accepted simplification, not an oversight.
- No changes to the existing visual design, CSS, or the demo game catalog's names — this is a wiring task, not a redesign. The catalog already uses generic, non-trademarked game names ("Battle Royale," "Arena Legends," etc.); that's preserved as-is specifically because it avoids using real game trademarks.

## Architecture

Everything stays in the single `elasticshop-gaming.html` file, inside the existing inline `<script>` IIFE — no build step, no new files, matching the rest of the portfolio's convention. One new concept is introduced: a small `Orders` module (plain object with a few functions) that wraps `localStorage` access, so every other part of the script reads/writes orders through one interface rather than touching `localStorage` directly in five places.

```
localStorage key: "esg_orders"    → JSON array of order objects (newest first)
localStorage key: "esg_profile"   → JSON object { name: string }
```

Order object shape (all fields are the same ones the existing status/history markup already expects — no new UI fields are introduced):
```js
{
  ref: "TRX-...",            // existing newRef() generator
  game: "Battle Royale",     // now real, from the clicked tile
  pub: "Elasticshop Games",  // placeholder publisher for demo tiles (see Data flow)
  uid: "1234567890",
  pkg: "500 Shells",
  amount: 484,
  date: "12 Oct 2026, 14:30:00",   // existing stampNow()
  method: "card" | "promptpay" | "truemoney",
  status: "success" | "pending"
}
```

`Orders.all()` reads and JSON-parses the array (returns `[]` if the key is missing or the JSON is corrupt — never throws). `Orders.add(order)` prepends and writes back. `Orders.updateStatus(ref, status)` finds by `ref` and updates in place (used when a pending order resolves via the refresh button, so a reload still shows it as resolved). `Profile.get()` / `Profile.set(name)` are the same pattern for the nickname.

## Component Changes

**Home tiles.** Each `<button class="tile" data-screen="topup">` gains `data-game` and `data-pub`. Since these are demo/fictional games, `data-pub` is a single consistent placeholder ("Elasticshop Games") rather than inventing a fake publisher per title — there's no real distinction to model. The existing click-delegation handler (`[data-screen]` → `showScreen()`) is extended: when the clicked element also carries `data-game`, that becomes the "selected game" for the upcoming checkout, stored in a simple in-memory variable (not persisted — it's only relevant for the checkout currently in progress).

**Topup screen — Package step.** Unchanged mechanically (pricing math, selection, summary already work), except the summary's "Game" row and the eventual order object now use the real selected game instead of the hardcoded string. If a visitor lands on `#screen-topup` directly (no tile was clicked — e.g. a bookmark or the nav's "Top Up" link), it falls back to the first catalog game as a sane default, exactly as it silently does today.

**Topup screen — new Payment step.** A new panel, inserted as the actual step-3 screen. Three method cards (Card / PromptPay / TrueMoney), styled consistently with the existing `.panel`/`.pkg` visual language already in this file (reused classes, no new design language introduced). Selecting Card reveals simple text inputs (card number, expiry, CVC) with basic format checks (digit count, MM/YY pattern) purely for UX feedback — none of it is stored or sent anywhere, discarded the moment the order is created. The step indicator's existing three nodes (Player Info / Package / Payment) now map onto three real screens instead of two.

**Confirm & Pay.** On submit: build the order object (using the real game/pub, the real chosen method), call `Orders.add()`, then branch on method — `card` fills the status card and shows `status-success` immediately (today's behavior); `promptpay`/`truemoney` fills it and shows `status-pending` (today's Valorant-demo behavior, now reachable from a real order). The existing refresh-button handler is generalized to resolve *the order actually in view* (by `ref`, read from the currently-rendered status card) rather than the one hardcoded Valorant row, and calls `Orders.updateStatus()` so the change survives a reload.

**History screen.** On page load, real orders from `Orders.all()` are rendered as `.txn-card` elements — same markup shape as the 3 existing hardcoded ones — and inserted before them in the DOM (newest-first, real orders on top, demo orders remain visible below as seed content). Because cards can now be added after the page's initial load, the filter (`applyTxnFilter`) and the "Detail" button wiring switch from a one-time `querySelectorAll` snapshot to delegated listeners on the list container, so newly-added cards are included automatically — this fixes a real staleness bug that would otherwise make new orders invisible to the filter.

**Login.** The nav's "Login"/history button split into its real purpose: a small inline prompt (a lightweight modal — reusing this file's existing dialog-free "panel" visual style, not a new component library) asking for a display name only. `Profile.set(name)` stores it; the nav button and the History profile card's name field both read `Profile.get()` on load, falling back to the current "Ploy_Gamer99" demo placeholder when no profile is set — so the page still looks populated for a first-time visitor.

## Data Flow (one checkout, start to finish)

1. Visitor clicks a Home tile → `data-game`/`data-pub` captured in memory → `showScreen('topup')`.
2. Player Info (pre-filled demo values, editable) + Package selection → existing summary math, now labeled with the real game.
3. Continue → Payment step → pick a method → (if Card) fill fake card fields.
4. Confirm & Pay → order object built → `Orders.add()` → branch to Status (success or pending) based on method.
5. History, visited any time after, shows this order at the top — reload the page and it's still there, because it lives in `localStorage`, not memory.
6. If pending: visitor clicks Refresh on the Status screen (or returns later, clicks "Detail" on the History row, still shows pending until refreshed) → `Orders.updateStatus(ref, 'success')` → status card and history row both update.

## Error Handling

- `localStorage` unavailable or full (private browsing, quota exceeded): `Orders.add`/`Profile.set` wrap the write in try/catch; on failure the order/profile still renders for the current page view (in-memory) but a small non-blocking note (reusing the existing `.sum-hint` pattern) tells the visitor it won't persist after they leave. Checkout still completes — a storage failure never blocks the demo flow.
- Corrupt/unparseable JSON in either key: treated as empty (`Orders.all()` → `[]`, `Profile.get()` → `null`), never thrown to the console as an uncaught error.
- Payment step with no method selected: Confirm & Pay stays disabled, same `validate()`/`sumHint` pattern the Package step already uses for a missing UID.
- Fake card fields: format-only validation (right digit counts, plausible expiry), never claims to verify the card is real — there is no such thing as a real card here.

## Testing / Verification

This project has no automated test suite (static site, no framework) — verification is manual, per the project's established convention (`CLAUDE.md`'s Lighthouse + mobile-overflow workflow):

- Full click-through: pick at least 3 different games from different Home categories, confirm each carries its real name through Package → Payment → Status → History.
- Both payment branches: one Card checkout (instant success) and one PromptPay/TrueMoney checkout (pending → refresh → success), confirm both end up correctly reflected in History.
- Reload the page after a completed checkout — order must still be in History (persistence check).
- Login: set a nickname, confirm it appears in nav and the History profile card; reload, confirm it's still set.
- Mobile overflow check at 375×812 on the new Payment step screen specifically (new markup = new overflow risk).
- Lighthouse audit (mobile, navigation) — must hold the project's 100/100/100 bar.
