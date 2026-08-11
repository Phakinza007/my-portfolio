# LUMI Clinic Redesign Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or
> superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Take `lumi-clinic.html` from a competent page in a saturated aesthetic lane to one a
Bangkok clinic owner would want, without reintroducing the photos of identifiable people that
were deliberately removed on 2026-08-02.

**Architecture:** One demo page with its own inline CSS. It carries no shared reset, does not
load `home-shell.css` or `portfolio-pages.css`, and must not gain portfolio chrome.

**Tech Stack:** Vanilla HTML + inline CSS + a small amount of JS already on the page.

---

## What the page is today

Measured on the live site, not read off the source:

| | |
|---|---|
| Height | 5,651px, 5 sections |
| Images | **2** (`hero-dropper.jpg`, `about-dropper.jpg`) — both fine; the second is `loading="lazy"` |
| Body | `#F6F3EE`, token named `--paper`; ink `#1C1714`; rust accent |
| Display face | Trirong (serif) |
| Section padding | `140px 0` on **all five** — 280px between every pair |
| Prices | ฿2,500 / ฿8,500 / ฿3,500 / ฿1,800, framed as starting prices |
| Form | 3 fields (text, tel, select) |
| Sticky booking | none |

The copy is the strongest thing on the page and most of it should survive. "The clinic that
knows when to say no" is a real position, and "We don't publish before/after photos — skin
tone, lighting and angle make them easy to fake and hard to verify" turns a missing asset into
a trust claim. **Do not rewrite either.**

## The three problems

**1. It is sitting in two lanes that read as generated.** `#F6F3EE` is inside the warm-neutral
band (OKLCH L 0.84–0.97, C < 0.06, hue 40–100) that the `impeccable` brand reference names as
*the* saturated AI default of 2026 — and the token is literally called `--paper`, one of the
named tells. On top of that, display-serif + ruled separators + muted restraint + almost no
imagery is the **editorial-typographic** reflex-reject lane by name. Neither choice is bad on
its own. Together they are the shape a generator reaches for when told "premium clinic".

**2. Two photographs across 5,651px.** Aesthetics is an image-led category; a buyer is judging
whether their own clinic could look like this. The reference is explicit that text-only pages
where typography carries the entire visual weight are the failure mode for this register.

**3. The conversion mechanics that clinic buyers look for are partly missing.** Against the
nine elements the 2026 med-spa roundups agree on, this page has the single clear hero promise,
transparent starting prices, and fast load. It is missing **one-tap booking on every screen**
(no sticky bar, no persistent CTA), **reviews placed next to the booking action** (the quotes
sit in their own band far from any CTA), and it states credentials as one thin line of text
rather than a visible trust block.

Sources consulted: [Codura — 9 elements the top med spa sites share](https://codurasolutions.com/blog/best-med-spa-websites) ·
[KG Web Designer — luxury skin clinic design](https://kgwebdesigner.com/blog/designing-a-luxury-experience-through-your-skin-clinic-website) ·
[DevMart — aesthetic clinic trust signals 2026](https://devmart.org/aesthetic-clinic-trust-signals-2026/) ·
[SMPLY Studio — aesthetic clinic design guide](https://smply.studio/aesthetic-clinic-website-design-guide/) ·
[Colorlib — med spa website examples](https://colorlib.com/wp/med-spa-website-examples/)

## Global Constraints

- **No identifiable faces.** Commit `6cf2ad1` removed four hotlinked Unsplash photos showing a
  clear face, and retired a before/after slider that used the same face as both its "before"
  and its "after". Any new imagery is skin-adjacent, environmental, material or abstract —
  never a recognisable person. Verify every URL resolves before shipping it; guessed Unsplash
  IDs 404 and ship as broken images.
- **Do not reinstate before/after.** The page's refusal is a stated position and better copy
  than the widget was.
- This is a **demo page**: no portfolio nav, no site search, no back-to-portfolio pill.
- The page carries its own CSS with **no shared reset** — it must set its own `box-sizing`.
  `construction-landing.html` shipped a CTA 18px off-screen for exactly this reason, and
  `canScrollX` stayed `false` so the usual sweep missed it. Check with a per-element right-edge
  sweep at 375×812.
- Lighthouse Accessibility 100 and CLS 0. Reserve every image box with `width`/`height`.
- A bare element selector in a demo page will eventually collide with a second element —
  `aesthetic-booking.html` styled `nav {}` and later put cream-on-cream links in its footer at
  1.11:1. Scope new selectors to a class.

---

## The one decision that is not mine to make

Tasks 2–5 are the same either way. Task 1 is the direction, and it changes how the page feels
more than everything else combined.

**Option A — commit the surface (recommended).** Drop the cream. Take the body to a deep,
low-chroma ink-green or near-black and let warm light be the accent rather than the substrate.
The clinic's own promise is refusal, not pampering — a doctor telling you that you don't need
the procedure yet. That reads as clinical calm, not spa warmth, and it is the move that gets
the page out of both saturated lanes at once. Risk: further from what a Bangkok clinic owner
expects a clinic site to look like.

**Option B — keep it light, but make the light deliberate.** True off-white at chroma 0 (or
tinted toward the brand's own hue, not toward warmth by default), with one saturated colour
carrying 30–60% of the surface in bands. Lower risk, still leaves the editorial-serif lane
half-intact.

Everything below assumes the direction is settled first.

---

## Task 1: Land the direction

**Files:** `lumi-clinic.html` (the `:root` token block and the type rules)

- [ ] **Step 1: Write the scene sentence.** One sentence naming who is on this page, where,
  under what light, in what mood. If it does not force the light/dark answer, it is not
  concrete enough yet. Put it in a CSS comment above `:root` so the next person inherits the
  reasoning rather than the result.
- [ ] **Step 2: Replace the palette in OKLCH**, keeping the token names honest — if the body
  stops being paper, `--paper` stops being its name.
- [ ] **Step 3: Re-pick the display face against the new surface.** Trirong is a reasonable
  Thai-capable serif and may survive; the test is rendering the real headline at its real size
  on the real background, not a specimen. If it stays, say why in a comment.
- [ ] **Step 4: Verify contrast** — body text ≥4.5:1, large text ≥3:1, and the placeholder text
  in the form at 4.5:1 too. Run the check, paste the numbers.
- [ ] **Step 5: Screenshot the hero at 1440 and 375 and compare against the current live page.**

## Task 2: Give the page something to look at

**Files:** `lumi-clinic.html`, `assets/lumi/`

- [ ] **Step 1: Decide the visual system before sourcing anything.** Options that need no face:
  the clinic room and its materials; macro texture (glass, steel, water, light on a wall);
  a single decisive full-bleed image per band. One decisive photo beats five mediocre ones.
- [ ] **Step 2: Source and verify.** Every candidate URL must be fetched and confirmed to
  resolve before it goes in the file. Download into `assets/lumi/`; do not hotlink — the
  previous hotlinks are exactly what had to be removed.
- [ ] **Step 3: Ship them with real `alt`**, correct `width`/`height`, `loading="lazy"` below
  the fold, and CLS still 0.
- [ ] **Step 4: Re-measure page height.** If the page got longer without getting better, cut.

## Task 3: Fix the vertical rhythm

**Files:** `lumi-clinic.html`

Every section is `padding: 140px 0`, so every boundary is 280px, five times, with no variation.
Uniform spacing reads as a template even when each section is fine.

- [ ] **Step 1: Vary it deliberately** — tight groupings where content belongs together,
  generous separations where the page should breathe. Fluid `clamp()`, not a fixed 140.
- [ ] **Step 2: Measure the new boundaries and record them** the way `CLAUDE.md` records the
  home-shell rhythm, so the next change has a number to respect.

## Task 4: Add the conversion mechanics the page is missing

**Files:** `lumi-clinic.html`

- [ ] **Step 1: A persistent booking affordance.** On mobile this is the single highest-value
  addition — the roundups are unanimous that a booking action must be reachable from any
  screen. It must not cover content; reserve its height.
- [ ] **Step 2: Move one real quote next to the booking action.** The quotes band stays; one
  line of it earns its place beside the CTA where the decision happens.
- [ ] **Step 3: Turn the credentials line into a visible trust block** — board-certified
  doctors, FDA-registered products, the Sukhumvit location. It is currently one thin rule of
  text under the hero doing the work of a trust signal.
- [ ] **Step 4: Verify the form.** Three fields is right; check labels are associated, the
  `select` has an accessible name, and focus order is sane. No `action` — nothing on this site
  talks to a backend, and that must stay true.

## Task 5: Verify and record

- [ ] **Step 1:** `canScrollX: false` at 375×812 **and** a per-element right-edge sweep — the
  sweep is the one that catches the `box-sizing` class of bug.
- [ ] **Step 2:** Lighthouse — Accessibility 100, SEO 100, CLS 0. Best Practices caps at 77 in
  production because Clarity sets third-party cookies; that one is not a regression.
- [ ] **Step 3:** Confirm zero `images.unsplash.com` hotlinks and zero identifiable faces.
- [ ] **Step 4:** Update the LUMI thumbnail `assets/thumbs/lumi-clinic.svg` if the palette
  moved — the card on the homepage and the archive is supposed to telegraph the page's
  identity, and it is now also one of the three cards in the homepage hero deck.
- [ ] **Step 5:** Record the direction and the no-faces constraint in `CLAUDE.md`.

---

## Deliberately not in this plan

- **Before/after gallery.** Every source lists it; this page refuses it on stated grounds and
  the refusal is better copy than the widget.
- **Booking software integration** (Fresha / Jane / Acuity). No form on this site has an
  `action` and nothing talks to a backend. A real booking system is a different sale — the
  site already says so, at ฿7,900.
- **A page per treatment.** Correct for a real clinic, wrong for a one-page demo.
