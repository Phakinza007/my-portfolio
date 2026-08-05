# Elasticshop Gaming Functional Checkout Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Wire `elasticshop-gaming.html`'s existing four-screen UI prototype into a genuinely working client-side checkout — real game selection, a real Payment step, orders that persist to `localStorage` and appear in History, and a lightweight local nickname in place of the no-op Login button — per `docs/superpowers/specs/2026-08-05-elasticshop-gaming-checkout-design.md`.

**Architecture:** Single-file static page, no build step, no framework — all changes go inside the existing inline `<script>` IIFE and `<style>` block in `elasticshop-gaming.html`. A small `Orders`/`Profile` module wraps all `localStorage` access behind `all()`/`add()`/`updateStatus()` and `get()`/`set()`, so every later task reads/writes through one interface instead of touching `localStorage` directly. Game identity is read from each tile's existing `.tile-name` text at click time (no new `data-game` attributes needed — one less thing to keep in sync, and it removes 18 repetitive HTML edits the spec assumed but didn't strictly require).

**Tech Stack:** Plain HTML/CSS/JS, no dependencies. Verification is manual/browser-based — this project has no automated test suite (see `CLAUDE.md`).

## Global Constraints

- No real payment gateway, no real money, no real game top-up delivery, no backend, no accounts with real authentication — everything is simulated and lives in `localStorage`, private to the visitor's browser. (spec Non-goals)
- Only two order outcomes exist in the UI: `success` and `pending` — no new "failed" status screen. (spec Non-goals)
- No changes to existing visual design/CSS beyond what's needed for the new Payment-method panel; reuse existing classes (`.panel`, `.panel-title`, `.pkg-grid`, `.pkg`, `.field`, `.field-label`, `.field-input`, `.field-help`) wherever the shape matches, matching this file's own conventions.
- Card fields are format-checked only (digit counts, `MM/YY` pattern) and never stored or transmitted anywhere — discarded immediately after building the order object.
- Demo game catalog names stay exactly as they are today (e.g. "Battle Royale," "Arena Legends") — these are already fictional/generic and deliberately not being changed to real trademarked game names.
- `localStorage` reads must never throw on missing or corrupt data — always fall back to `[]` / `null`.

---

### Task 1: Orders + Profile localStorage module

**Files:**
- Modify: `elasticshop-gaming.html:1392-1393` (insert new module right after the `$`/`$$` helpers, before the `PRICING DATA` comment block)

**Interfaces:**
- Produces: `Orders.all(): Array<Order>`, `Orders.add(order: Order): boolean`, `Orders.updateStatus(ref: string, status: 'success'|'pending'): boolean`, `Profile.get(): {name: string} | null`, `Profile.set(name: string): boolean`. `Order` shape: `{ ref, game, pub, uid, pkg, amount, date, method, status }` (all strings except `amount`, a number).
- All later tasks (3, 4, 5, 6) consume this module — no task before this one may reference `Orders` or `Profile`.

- [ ] **Step 1: Insert the module**

Find (exact current lines 1391-1394):
```html
      var $  = function (sel, ctx) { return (ctx || document).querySelector(sel); };
      var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

      /* ============================================================
         PRICING DATA — single source of truth for the top-up flow.
```

Replace with:
```html
      var $  = function (sel, ctx) { return (ctx || document).querySelector(sel); };
      var $$ = function (sel, ctx) { return Array.prototype.slice.call((ctx || document).querySelectorAll(sel)); };

      /* ============================================================
         ORDERS + PROFILE — localStorage-backed, demo-only persistence.
         Every read tolerates missing/corrupt data and returns a safe
         empty value instead of throwing. Every write is wrapped in
         try/catch (private browsing / full quota must never block
         the checkout flow).
      ============================================================ */
      var ORDERS_KEY  = 'esg_orders';
      var PROFILE_KEY = 'esg_profile';

      var Orders = {
        all: function () {
          try {
            var raw = window.localStorage.getItem(ORDERS_KEY);
            var list = raw ? JSON.parse(raw) : [];
            return Array.isArray(list) ? list : [];
          } catch (e) {
            return [];
          }
        },
        add: function (order) {
          var list = Orders.all();
          list.unshift(order);
          try {
            window.localStorage.setItem(ORDERS_KEY, JSON.stringify(list));
            return true;
          } catch (e) {
            return false;
          }
        },
        updateStatus: function (ref, status) {
          var list = Orders.all();
          for (var i = 0; i < list.length; i++) {
            if (list[i].ref === ref) { list[i].status = status; break; }
          }
          try {
            window.localStorage.setItem(ORDERS_KEY, JSON.stringify(list));
            return true;
          } catch (e) {
            return false;
          }
        }
      };

      var Profile = {
        get: function () {
          try {
            var raw = window.localStorage.getItem(PROFILE_KEY);
            var obj = raw ? JSON.parse(raw) : null;
            return (obj && typeof obj.name === 'string' && obj.name) ? obj : null;
          } catch (e) {
            return null;
          }
        },
        set: function (name) {
          try {
            window.localStorage.setItem(PROFILE_KEY, JSON.stringify({ name: name }));
            return true;
          } catch (e) {
            return false;
          }
        }
      };

      /* ============================================================
         PRICING DATA — single source of truth for the top-up flow.
```

- [ ] **Step 2: Verify in browser console**

Open the page locally (e.g. `python3 -m http.server 8000` from the repo root, visit `http://localhost:8000/elasticshop-gaming.html`), open DevTools console, and run:
```js
Orders.all()                                   // []
Orders.add({ref:'TRX-1', game:'Test', pub:'Elasticshop Games', uid:'1', pkg:'X', amount:100, date:'now', method:'card', status:'success'})  // true
Orders.all()                                   // [{ref: 'TRX-1', ...}]
Orders.updateStatus('TRX-1', 'pending')
Orders.all()[0].status                         // 'pending'
Profile.get()                                  // null
Profile.set('Test')                            // true
Profile.get()                                  // {name: 'Test'}
localStorage.clear()                           // clean up test data before continuing
```
Expected: matches the comments above, no thrown errors.

- [ ] **Step 3: Commit**

```bash
git add elasticshop-gaming.html
git commit -m "$(cat <<'EOF'
Add Orders/Profile localStorage module to elasticshop-gaming

Foundational module for the functional-checkout work — wraps all
localStorage access behind Orders.all/add/updateStatus and
Profile.get/set so later tasks never touch localStorage directly.
Every read tolerates missing/corrupt data; every write is
try/catch-guarded so a full quota or private-browsing restriction
never blocks checkout.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: Real game selection from Home tiles

**Files:**
- Modify: `elasticshop-gaming.html:1143` (Order Summary "Game" row — add an id so JS can update it)
- Modify: `elasticshop-gaming.html:1482-1487` (click delegation handler — capture the clicked tile's game name)

**Depends on:** Task 1 is not required for this task (no `Orders`/`Profile` use here), but must be applied first since it shifts line numbers — use the exact "Find" text below as the authoritative anchor, not line numbers.

**Interfaces:**
- Produces: module-level `var selectedGame = { game: 'Battle Royale', pub: 'Elasticshop Games' };` and `function paintSelectedGame()`. Task 3/4 read `selectedGame` when building the order object; Task 4 must NOT hardcode `'RoV: Arena of Valor'` anymore.

- [ ] **Step 1: Give the Order Summary "Game" row an id**

Find (exact current text):
```html
                  <div class="sum-row"><span class="k">Game</span><span class="v">RoV: Arena of Valor</span></div>
```

Replace with:
```html
                  <div class="sum-row"><span class="k">Game</span><span class="v" id="sumGame">RoV: Arena of Valor</span></div>
```

- [ ] **Step 2: Capture the clicked tile's game name and repaint the summary**

Find (exact current click-delegation block):
```html
      // any element carrying data-screen (in-screen nav links, CTAs, buttons)
      // routes to that screen; data-scroll optionally targets a section
      document.addEventListener('click', function (e) {
        var el = e.target.closest ? e.target.closest('[data-screen]') : null;
        if (!el || el.classList.contains('side-link')) return;
        e.preventDefault();
        showScreen(el.getAttribute('data-screen'), el.getAttribute('data-scroll'));
      });
```

Replace with:
```html
      /* ============================================================
         SELECTED GAME — carried from whichever Home tile was clicked
         into the Top Up flow. Falls back to the first catalog game
         (matches the real catalog, unlike the old hardcoded default)
         when the Top Up screen is reached any other way (nav link,
         featured-deal CTA).
      ============================================================ */
      var selectedGame = { game: 'Battle Royale', pub: 'Elasticshop Games' };

      function paintSelectedGame() {
        var el = document.getElementById('sumGame');
        if (el) el.textContent = selectedGame.game;
      }

      // any element carrying data-screen (in-screen nav links, CTAs, buttons)
      // routes to that screen; data-scroll optionally targets a section
      document.addEventListener('click', function (e) {
        var el = e.target.closest ? e.target.closest('[data-screen]') : null;
        if (!el || el.classList.contains('side-link') || el.classList.contains('tn-login')) return;
        e.preventDefault();

        if (el.classList.contains('tile')) {
          var nameEl = $('.tile-name', el);
          if (nameEl) {
            selectedGame = { game: nameEl.textContent.trim(), pub: 'Elasticshop Games' };
            paintSelectedGame();
          }
        }

        showScreen(el.getAttribute('data-screen'), el.getAttribute('data-scroll'));
      });
```

Note: the `tn-login` exclusion is added now because Task 6 repurposes that button — adding it here avoids a second edit to this same block later.

- [ ] **Step 3: Paint the default on load**

Find (exact current INIT block):
```html
      /* ============================================================
         INIT
      ============================================================ */
      document.getElementById('year').textContent = new Date().getFullYear();
      selectPackage(selectedId);
      applyHomeFilter();
      applyTxnFilter();
    })();
```

Replace with:
```html
      /* ============================================================
         INIT
      ============================================================ */
      document.getElementById('year').textContent = new Date().getFullYear();
      selectPackage(selectedId);
      applyHomeFilter();
      applyTxnFilter();
      paintSelectedGame();
    })();
```

- [ ] **Step 4: Verify in browser**

Reload the page. Click "Battle Royale" (first tile) → Top Up screen's Order Summary "Game" row shows "Battle Royale". Go back Home, click "Idle Heroes" → summary now shows "Idle Heroes". Click the nav's plain "Top Up" link (not a tile) → summary shows whatever was last selected (or "Battle Royale" default on first load) — no error either way.

- [ ] **Step 5: Commit**

```bash
git add elasticshop-gaming.html
git commit -m "$(cat <<'EOF'
Carry the clicked game tile's identity into the Top Up summary

Every tile previously routed to the same hardcoded "RoV: Arena of
Valor" checkout. Reads the game name directly from the tile's
existing .tile-name text at click time rather than adding data-game
to all 18 tiles — one less thing to keep in sync.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: Real Payment step (method selection + card fields)

**Files:**
- Modify: `elasticshop-gaming.html:606` (insert two new CSS rules after `.pkg-tag`)
- Modify: `elasticshop-gaming.html:1130-1137` (insert new Payment panel after the Select Package panel)
- Modify: `elasticshop-gaming.html:1152` (confirm button — id stays, text now toggles by mode)
- Modify: script — add package-mode/payment-mode toggle logic

**Depends on:** Task 2 (uses `selectedGame`, though only indirectly via the summary already painted).

**Interfaces:**
- Produces: `var checkoutMode = 'package';` (`'package' | 'payment'`), `var selectedMethod = null;` (`null | 'card' | 'promptpay' | 'truemoney'`), `function enterPaymentMode()`, `function enterPackageMode()`, `function selectMethod(method)`, `function validatePayment(): boolean`.
- Task 4 reads `checkoutMode`, `selectedMethod`, and calls `enterPackageMode()` after a successful submission to reset the flow for the next checkout.

- [ ] **Step 1: Add CSS for the method cards' back-link and the generic order-icon (used later by Task 5)**

Find (exact current line, the `.pkg-tag` rule followed by the package-icon rule):
```html
    .pkg-tag { position: absolute; top: -9px; left: 50%; transform: translateX(-50%); background: var(--yellow); color: #111; font-size: 0.66rem; font-weight: 800; padding: 0.12rem 0.55rem; border-radius: var(--r-pill); }
```

Replace with:
```html
    .pkg-tag { position: absolute; top: -9px; left: 50%; transform: translateX(-50%); background: var(--yellow); color: #111; font-size: 0.66rem; font-weight: 800; padding: 0.12rem 0.55rem; border-radius: var(--r-pill); }

    .back-link { font-size: 0.85rem; font-weight: 600; color: var(--muted); background: none; border: none; cursor: pointer; padding: 0; }
    .back-link:hover { color: var(--red); }

    .txn-icon.generic { background: linear-gradient(135deg, var(--red), var(--yellow)); }
```

- [ ] **Step 2: Insert the Payment panel after the Select Package panel**

Find (exact current text — the end of the Select Package panel, immediately followed by the closing of the left column and the start of the Order Summary column):
```html
                <div class="pkg-grid" role="radiogroup" aria-label="Select package">
                    <button type="button" class="pkg" role="radio" aria-checked="false" tabindex="-1" data-pkg="p1"><span class="pkg-icon"></span><span class="pkg-amt">100 Shells</span><span class="pkg-price">฿ 99</span></button>
                    <button type="button" class="pkg sel" role="radio" aria-checked="true" tabindex="0" data-pkg="p2"><span class="pkg-tag">-12%</span><span class="pkg-icon"></span><span class="pkg-amt">500 Shells</span><span class="pkg-price">฿ 484</span></button>
                    <button type="button" class="pkg" role="radio" aria-checked="false" tabindex="-1" data-pkg="p3"><span class="pkg-icon"></span><span class="pkg-amt">1,000 Shells</span><span class="pkg-price">฿ 935</span></button>
                    <button type="button" class="pkg" role="radio" aria-checked="false" tabindex="-1" data-pkg="p4"><span class="pkg-icon"></span><span class="pkg-amt">2,000 Shells</span><span class="pkg-price">฿ 1,804</span></button>
                    <button type="button" class="pkg" role="radio" aria-checked="false" tabindex="-1" data-pkg="p5"><span class="pkg-tag">HOT</span><span class="pkg-icon"></span><span class="pkg-amt">5,000 Shells</span><span class="pkg-price">฿ 4,400</span></button>
                    <button type="button" class="pkg" role="radio" aria-checked="false" tabindex="-1" data-pkg="p6"><span class="pkg-icon"></span><span class="pkg-amt">10,000 Shells</span><span class="pkg-price">฿ 8,250</span></button>
                  </div>
                </div>
              </div>

              <div class="summary">
```

Replace with:
```html
                <div class="pkg-grid" role="radiogroup" aria-label="Select package">
                    <button type="button" class="pkg" role="radio" aria-checked="false" tabindex="-1" data-pkg="p1"><span class="pkg-icon"></span><span class="pkg-amt">100 Shells</span><span class="pkg-price">฿ 99</span></button>
                    <button type="button" class="pkg sel" role="radio" aria-checked="true" tabindex="0" data-pkg="p2"><span class="pkg-tag">-12%</span><span class="pkg-icon"></span><span class="pkg-amt">500 Shells</span><span class="pkg-price">฿ 484</span></button>
                    <button type="button" class="pkg" role="radio" aria-checked="false" tabindex="-1" data-pkg="p3"><span class="pkg-icon"></span><span class="pkg-amt">1,000 Shells</span><span class="pkg-price">฿ 935</span></button>
                    <button type="button" class="pkg" role="radio" aria-checked="false" tabindex="-1" data-pkg="p4"><span class="pkg-icon"></span><span class="pkg-amt">2,000 Shells</span><span class="pkg-price">฿ 1,804</span></button>
                    <button type="button" class="pkg" role="radio" aria-checked="false" tabindex="-1" data-pkg="p5"><span class="pkg-tag">HOT</span><span class="pkg-icon"></span><span class="pkg-amt">5,000 Shells</span><span class="pkg-price">฿ 4,400</span></button>
                    <button type="button" class="pkg" role="radio" aria-checked="false" tabindex="-1" data-pkg="p6"><span class="pkg-icon"></span><span class="pkg-amt">10,000 Shells</span><span class="pkg-price">฿ 8,250</span></button>
                  </div>
                </div>

                <div class="panel" id="paymentPanel" hidden>
                  <div class="panel-title"><span class="pn">3</span> Payment Method</div>
                  <div class="pkg-grid" id="methodGrid" role="radiogroup" aria-label="Select payment method">
                    <button type="button" class="pkg" role="radio" aria-checked="false" tabindex="0" data-method="card"><span class="pkg-icon"></span><span class="pkg-amt">Card</span></button>
                    <button type="button" class="pkg" role="radio" aria-checked="false" tabindex="-1" data-method="promptpay"><span class="pkg-icon"></span><span class="pkg-amt">PromptPay</span></button>
                    <button type="button" class="pkg" role="radio" aria-checked="false" tabindex="-1" data-method="truemoney"><span class="pkg-icon"></span><span class="pkg-amt">TrueMoney</span></button>
                  </div>

                  <div id="cardFields" hidden style="margin-top:1.1rem;">
                    <div class="field">
                      <label class="field-label" for="cardNumber">Card Number</label>
                      <input class="field-input" id="cardNumber" name="cardNumber" type="text" inputmode="numeric" placeholder="4242 4242 4242 4242" maxlength="19" />
                    </div>
                    <div class="field" style="display:flex; gap:0.85rem;">
                      <div style="flex:1;">
                        <label class="field-label" for="cardExpiry">Expiry (MM/YY)</label>
                        <input class="field-input" id="cardExpiry" name="cardExpiry" type="text" placeholder="12/28" maxlength="5" />
                      </div>
                      <div style="flex:1;">
                        <label class="field-label" for="cardCvc">CVC</label>
                        <input class="field-input" id="cardCvc" name="cardCvc" type="text" inputmode="numeric" placeholder="123" maxlength="4" />
                      </div>
                    </div>
                    <div class="field-help">Demo only — no card data is stored or sent anywhere.</div>
                  </div>

                  <div id="promptpayInfo" hidden style="margin-top:1.1rem;">
                    <div class="field-help">You'll see a QR code to scan after confirming — this demo simulates a short pending state, just like a real PromptPay confirmation.</div>
                  </div>

                  <div id="truemoneyInfo" hidden style="margin-top:1.1rem;">
                    <div class="field-help">You'll confirm in your TrueMoney Wallet app — this demo simulates a short pending state.</div>
                  </div>

                  <button type="button" class="back-link" id="backToPackage" style="margin-top:1rem;">← Back to Package</button>
                </div>
              </div>

              <div class="summary">
```

- [ ] **Step 3: Add the mode/method state machine to the script**

Find (exact current text — the end of `updateSummary()` and the start of `selectPackage()`):
```html
        validate();
      }

      function selectPackage(id) {
```

Replace with:
```html
        validate();
      }

      /* ============================================================
         SCREEN 2 — PACKAGE / PAYMENT MODE TOGGLE
      ============================================================ */
      var checkoutMode   = 'package';   // 'package' | 'payment'
      var selectedMethod = null;        // null | 'card' | 'promptpay' | 'truemoney'

      var packagePanel  = pkgButtons.length ? pkgButtons[0].closest('.panel') : null;
      var paymentPanel  = document.getElementById('paymentPanel');
      var methodButtons = $$('#methodGrid .pkg');
      var cardFields     = document.getElementById('cardFields');
      var promptpayInfo  = document.getElementById('promptpayInfo');
      var truemoneyInfo  = document.getElementById('truemoneyInfo');
      var backToPackage  = document.getElementById('backToPackage');

      function enterPaymentMode() {
        checkoutMode = 'payment';
        if (packagePanel) packagePanel.hidden = true;
        paymentPanel.hidden = false;

        var pkgStep = document.getElementById('stepPackage');
        pkgStep.classList.remove('active');
        pkgStep.classList.add('done');
        $('.step-node', pkgStep).textContent = '✓';
        document.getElementById('stepLine2').classList.add('done');
        document.getElementById('stepPayment').classList.add('active');

        confirmBtn.textContent = 'Confirm & Pay';
        validate();
      }

      function enterPackageMode() {
        checkoutMode = 'package';
        paymentPanel.hidden = true;
        if (packagePanel) packagePanel.hidden = false;

        selectedMethod = null;
        methodButtons.forEach(function (b) {
          b.classList.remove('sel');
          b.setAttribute('aria-checked', 'false');
          b.tabIndex = -1;
        });
        if (methodButtons.length) methodButtons[0].tabIndex = 0;
        cardFields.hidden = true;
        promptpayInfo.hidden = true;
        truemoneyInfo.hidden = true;
        document.getElementById('cardNumber').value = '';
        document.getElementById('cardExpiry').value = '';
        document.getElementById('cardCvc').value = '';

        resetSteps();
        confirmBtn.textContent = 'Continue to Payment →';
        validate();
      }

      function selectMethod(method) {
        selectedMethod = method;
        methodButtons.forEach(function (b) {
          var on = b.getAttribute('data-method') === method;
          b.classList.toggle('sel', on);
          b.setAttribute('aria-checked', on ? 'true' : 'false');
          b.tabIndex = on ? 0 : -1;
        });
        cardFields.hidden    = method !== 'card';
        promptpayInfo.hidden = method !== 'promptpay';
        truemoneyInfo.hidden = method !== 'truemoney';
        validate();
      }

      methodButtons.forEach(function (btn, i) {
        btn.addEventListener('click', function () { selectMethod(btn.getAttribute('data-method')); });
        btn.addEventListener('keydown', function (e) {
          var next = -1;
          if (e.key === 'ArrowRight' || e.key === 'ArrowDown') next = (i + 1) % methodButtons.length;
          if (e.key === 'ArrowLeft'  || e.key === 'ArrowUp')   next = (i - 1 + methodButtons.length) % methodButtons.length;
          if (next < 0) return;
          e.preventDefault();
          methodButtons[next].focus();
          selectMethod(methodButtons[next].getAttribute('data-method'));
        });
      });

      backToPackage.addEventListener('click', function () {
        checkoutMode = 'package';
        paymentPanel.hidden = true;
        if (packagePanel) packagePanel.hidden = false;
        resetSteps();
        confirmBtn.textContent = 'Continue to Payment →';
        validate();
      });

      function validatePayment() {
        if (!selectedMethod) return 'Choose a payment method to continue.';
        if (selectedMethod === 'card') {
          var num = document.getElementById('cardNumber').value.replace(/\s+/g, '');
          var exp = document.getElementById('cardExpiry').value.trim();
          var cvc = document.getElementById('cardCvc').value.trim();
          if (!/^\d{13,19}$/.test(num)) return 'Enter a valid card number.';
          if (!/^\d{2}\/\d{2}$/.test(exp)) return 'Enter expiry as MM/YY.';
          if (!/^\d{3,4}$/.test(cvc)) return 'Enter a valid CVC.';
        }
        return '';
      }

      function selectPackage(id) {
```

- [ ] **Step 4: Route `validate()` through the current mode, and make the confirm button call `enterPaymentMode()` while in package mode**

Find (exact current `validate()` function):
```html
      function validate() {
        var msg = '';
        if (!pkgById(selectedId))     msg = 'Choose a package to continue.';
        else if (!uidInput.value.trim()) msg = 'Enter your Player UID to continue.';
        confirmBtn.disabled = msg !== '';
        sumHintText.textContent = msg;
        sumHint.classList.toggle('show', msg !== '');
        return msg === '';
      }
```

Replace with:
```html
      function validate() {
        var msg = '';
        if (!pkgById(selectedId))     msg = 'Choose a package to continue.';
        else if (!uidInput.value.trim()) msg = 'Enter your Player UID to continue.';
        else if (checkoutMode === 'payment') msg = validatePayment();
        confirmBtn.disabled = msg !== '';
        sumHintText.textContent = msg;
        sumHint.classList.toggle('show', msg !== '');
        return msg === '';
      }
```

- [ ] **Step 5: Verify in browser**

Reload. Select a package, enter a UID, click "Continue to Payment →" — Package panel hides, Payment panel shows, step indicator's step 2 turns done and step 3 turns active, button now reads "Confirm & Pay" and is disabled. Click a method — button enables (Card also reveals the card fields; typing an invalid card number keeps the button disabled with a hint; a valid-format number enables it). Click "← Back to Package" — returns to Package panel, method/card fields cleared, button reads "Continue to Payment →" again.

- [ ] **Step 6: Commit**

```bash
git add elasticshop-gaming.html
git commit -m "$(cat <<'EOF'
Add a real Payment step to the Top Up flow

The step indicator always showed three steps (Player Info, Package,
Payment), but Payment had no actual screen — Confirm & Pay fired
straight from Package selection. Adds a real method-selection panel
(Card / PromptPay / TrueMoney) as its own mode, reusing the existing
.panel/.pkg/.field component patterns already in this file. Card
fields are format-checked only and never persisted.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: Confirm & Pay — build a real order, branch on method, reset for next checkout

**Files:**
- Modify: `elasticshop-gaming.html` — the `confirmBtn` click handler
- Modify: `elasticshop-gaming.html` — the pending→success refresh handler

**Depends on:** Task 1 (`Orders`), Task 2 (`selectedGame`), Task 3 (`checkoutMode`, `selectedMethod`, `enterPaymentMode`, `enterPackageMode`).

**Interfaces:**
- Consumes: `Orders.add(order)`, `Orders.updateStatus(ref, status)`, `selectedGame`, `checkoutMode`, `selectedMethod`, `enterPaymentMode()`, `enterPackageMode()`.
- Produces: nothing new consumed by later tasks directly, but Task 5 depends on real orders existing in `Orders.all()` by the time History is viewed — this task is what puts them there.

- [ ] **Step 1: Give the success sub-text an id (needed for the storage-failure note in Step 3)**

Find (exact current text):
```html
              <div class="ss-sub thai">รายการของคุณถูกดำเนินการเรียบร้อยแล้ว ขอให้สนุกกับเกม!</div>
```

Replace with:
```html
              <div class="ss-sub thai" id="ssSub">รายการของคุณถูกดำเนินการเรียบร้อยแล้ว ขอให้สนุกกับเกม!</div>
```

- [ ] **Step 2: Rewrite the Confirm & Pay handler**

Find (exact current `confirmBtn` click handler):
```html
      confirmBtn.addEventListener('click', function () {
        if (!validate()) {
          if (!uidInput.value.trim()) uidInput.focus();
          return;
        }
        var pkg   = pkgById(selectedId);
        var money = priceOf(pkg);

        // step 3 (Payment) is now complete
        var pkgStep = document.getElementById('stepPackage');
        pkgStep.classList.remove('active');
        pkgStep.classList.add('done');
        $('.step-node', pkgStep).textContent = '✓';
        document.getElementById('stepLine2').classList.add('done');
        var payStep = document.getElementById('stepPayment');
        payStep.classList.add('done');
        $('.step-node', payStep).textContent = '✓';

        fillStatusCard({
          game: 'RoV: Arena of Valor',
          pub: 'Garena Thailand',
          ref: newRef(),
          uid: uidInput.value.trim(),
          pkg: pkg.label,
          amount: money.total,
          date: stampNow()
        });
        showScreen('status');
      });
```

Replace with:
```html
      confirmBtn.addEventListener('click', function () {
        if (!validate()) {
          if (checkoutMode === 'package' && !uidInput.value.trim()) uidInput.focus();
          return;
        }

        if (checkoutMode === 'package') {
          enterPaymentMode();
          return;
        }

        // checkoutMode === 'payment' — this click actually submits the order
        var pkg    = pkgById(selectedId);
        var money  = priceOf(pkg);
        var status = selectedMethod === 'card' ? 'success' : 'pending';

        var order = {
          ref: newRef(),
          game: selectedGame.game,
          pub: selectedGame.pub,
          uid: uidInput.value.trim(),
          pkg: pkg.label,
          amount: money.total,
          date: stampNow(),
          method: selectedMethod,
          status: status
        };
        var saved = Orders.add(order);
        renderOrderCard(order);

        var payStep = document.getElementById('stepPayment');
        payStep.classList.add('done');
        $('.step-node', payStep).textContent = '✓';

        fillStatusCard(order);
        if (status === 'success') {
          showSuccessStatus(saved);
        } else {
          showPendingStatus(order, saved);
        }
        showScreen('status');

        enterPackageMode();
      });
```

Note: `renderOrderCard`, `showSuccessStatus`, and `showPendingStatus` are defined in Task 5 and Task 4 Step 3 respectively — this task calls them but they must exist before this handler runs, which is satisfied because script execution order only matters at call time (click), not definition time, and both are defined earlier in the same IIFE by the time a user can click anything. `fillStatusCard` already exists unchanged from before this plan.

`showSuccessStatus`/`showPendingStatus` take a `saved` flag (`Orders.add`'s return value) so a `localStorage` failure — full quota, private-browsing restrictions — still completes the checkout (per the spec's Error Handling section: "a storage failure never blocks the demo flow") but tells the visitor their order won't survive leaving the page, instead of silently failing to persist.

- [ ] **Step 3: Add success/pending status-screen helpers, and generalize the refresh button to work by ref**

Find (exact current pending→success refresh handler, through the end of the script's business logic before INIT):
```html
      /* ============================================================
         SCREEN 4 — PENDING → SUCCESS REFRESH
      ============================================================ */
      var refreshBtn  = document.getElementById('spRefresh');
      var refreshText = document.getElementById('spRefreshText');

      refreshBtn.addEventListener('click', function () {
        // once resolved the button becomes a link to the history screen
        if (refreshBtn.getAttribute('data-screen')) return;

        refreshBtn.classList.add('loading');
        refreshBtn.disabled = true;
        refreshText.textContent = 'กำลังตรวจสอบ...';

        window.setTimeout(function () {
          refreshBtn.classList.remove('loading');
          refreshBtn.disabled = false;

          document.getElementById('pendingCard').classList.add('done');
          var badge = document.getElementById('spBadge');
          badge.classList.add('done');
          badge.innerHTML = '<span class="pdot"></span>Success';
          document.getElementById('spTitle').textContent = 'ยืนยันการชำระเงินแล้ว';
          document.getElementById('spSub').textContent   = 'เติม 1050 VP เข้าบัญชี Valorant เรียบร้อยแล้ว';
          refreshText.textContent = 'ดูประวัติการเติม';
          refreshBtn.setAttribute('data-screen', 'history');

          // keep the history row in sync
          var row = document.getElementById('txnValorant');
          row.setAttribute('data-status', 'success');
          document.getElementById('txnValorantStatus').innerHTML =
            '<span class="badge badge-success">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>' +
            'Success</span>';
          applyTxnFilter();
        }, 900);
      });
```

Replace with:
```html
      /* ============================================================
         SCREEN 4 — STATUS DISPLAY + PENDING → SUCCESS REFRESH
      ============================================================ */
      var statusSuccessEl = $('.status-success');
      var statusPendingEl = document.getElementById('pendingCard');
      var refreshBtn       = document.getElementById('spRefresh');
      var refreshText      = document.getElementById('spRefreshText');
      var currentPendingRef = null;

      // Orders.add/Profile.set return false when localStorage write fails
      // (full quota, private-browsing restrictions) — the checkout still
      // completes either way, this just tells the visitor it won't survive
      // leaving the page, instead of silently failing to persist.
      function saveNote(saved) {
        return saved ? '' : ' (This device can’t save your order history right now — it won’t appear after you leave this page.)';
      }

      function showSuccessStatus(saved) {
        statusSuccessEl.style.display = '';
        statusPendingEl.style.display = 'none';
        document.getElementById('ssSub').textContent =
          'รายการของคุณถูกดำเนินการเรียบร้อยแล้ว ขอให้สนุกกับเกม!' + saveNote(saved);
      }

      function showPendingStatus(order, saved) {
        statusSuccessEl.style.display = 'none';
        statusPendingEl.style.display = '';
        statusPendingEl.classList.remove('done');
        currentPendingRef = order.ref;

        var badge = document.getElementById('spBadge');
        badge.classList.remove('done');
        badge.innerHTML = '<span class="pdot"></span>Pending';
        document.getElementById('spTitle').textContent = 'กำลังตรวจสอบรายการ';
        document.getElementById('spSub').textContent   =
          'ระบบกำลังยืนยันการชำระเงินของคุณ โปรดรอสักครู่...' + saveNote(saved);
        $('.sp-meta').innerHTML =
          '<div class="sp-row"><span class="k">Ref:</span><span class="v">' + order.ref + '</span></div>' +
          '<div class="sp-row"><span class="k">Game:</span><span class="v">' + order.game + '</span></div>';
        refreshBtn.removeAttribute('data-screen');
        refreshText.textContent = 'รีเฟรชสถานะ';
      }

      refreshBtn.addEventListener('click', function () {
        // once resolved the button becomes a link to the history screen
        if (refreshBtn.getAttribute('data-screen')) return;

        refreshBtn.classList.add('loading');
        refreshBtn.disabled = true;
        refreshText.textContent = 'กำลังตรวจสอบ...';

        window.setTimeout(function () {
          refreshBtn.classList.remove('loading');
          refreshBtn.disabled = false;

          statusPendingEl.classList.add('done');
          var badge = document.getElementById('spBadge');
          badge.classList.add('done');
          badge.innerHTML = '<span class="pdot"></span>Success';
          document.getElementById('spTitle').textContent = 'ยืนยันการชำระเงินแล้ว';
          document.getElementById('spSub').textContent   = 'เติมแพ็กเกจเข้าบัญชีเรียบร้อยแล้ว';
          refreshText.textContent = 'ดูประวัติการเติม';
          refreshBtn.setAttribute('data-screen', 'history');

          if (currentPendingRef) {
            Orders.updateStatus(currentPendingRef, 'success');
            updateOrderCardStatus(currentPendingRef, 'success');
          }
        }, 900);
      });
```

Note: `updateOrderCardStatus` is defined in Task 5 — same same-IIFE call-order reasoning as Step 1's note applies. The old hardcoded `#txnValorant`/`#txnValorantStatus` demo-specific sync logic is removed here because Task 5 replaces the whole History rendering approach (the 3 demo cards keep their hardcoded markup and are never touched by refresh — only real orders, which flow through `updateOrderCardStatus`, do).

- [ ] **Step 4: Verify in browser**

This task can't be fully verified until Task 5 exists (`renderOrderCard`/`updateOrderCardStatus` are undefined until then — expect a console error on submit if you test this task in isolation). Skip standalone verification here; Task 5's verification step covers the full flow.

- [ ] **Step 5: Commit**

```bash
git add elasticshop-gaming.html
git commit -m "$(cat <<'EOF'
Wire Confirm & Pay to build real orders and branch on payment method

Confirm & Pay previously always hardcoded "RoV: Arena of Valor" and
went straight to a static success screen. Now builds a real order
from the selected game/package/method, persists it via Orders.add,
and branches: card payments resolve instantly (status-success,
matching how cards behave in reality); PromptPay/TrueMoney land on
the existing pending screen, resolved by the existing refresh button
— a flow that was already fully built but only reachable from one
hardcoded demo row until now.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 5: History renders real orders, seed data stays, filters work on both

**Files:**
- Modify: `elasticshop-gaming.html` — History screen JS (filter/detail wiring, new render functions)

**Depends on:** Task 1 (`Orders`), Task 4 (calls `renderOrderCard`/`updateOrderCardStatus`, defined here).

**Interfaces:**
- Produces: `function renderOrderCard(order): void` (builds and prepends a `.txn-card` into `#txnList`, matching the exact markup shape of the 3 existing hardcoded demo cards), `function updateOrderCardStatus(ref, status): void` (finds the rendered card by `data-ref` and updates its badge in place).
- Consumes: `Orders.all()` to repaint History on page load.

- [ ] **Step 1: Replace the History filter/detail wiring with delegation, add the render functions, and paint stored orders on load**

Find (exact current History filter/detail block):
```html
      /* ============================================================
         SCREEN 3 — HISTORY FILTERS
      ============================================================ */
      var pills    = $$('.filter-pill');
      var txnCards = $$('.txn-card');
      var txnEmpty = document.getElementById('txnEmpty');
      var activeFilter = 'all';

      function applyTxnFilter() {
        var shown = 0;
        txnCards.forEach(function (card) {
          var match = activeFilter === 'all' || card.getAttribute('data-status') === activeFilter;
          card.classList.toggle('hide', !match);
          if (match) shown++;
        });
        txnEmpty.classList.toggle('show', shown === 0);
      }

      pills.forEach(function (pill) {
        pill.addEventListener('click', function () {
          activeFilter = pill.getAttribute('data-filter');
          pills.forEach(function (p) {
            var on = p === pill;
            p.classList.toggle('active', on);
            p.setAttribute('aria-pressed', on ? 'true' : 'false');
          });
          applyTxnFilter();
        });
      });

      // "Detail" opens that order on the transaction status screen
      $$('.txn-detail').forEach(function (btn) {
        btn.addEventListener('click', function () {
          var card = btn.closest('.txn-card');
          fillStatusCard({
            game: card.getAttribute('data-game'),
            pub: card.getAttribute('data-pub'),
            ref: card.getAttribute('data-ref'),
            uid: card.getAttribute('data-uid'),
            pkg: card.getAttribute('data-pkg'),
            amount: Number(card.getAttribute('data-amt')),
            date: card.getAttribute('data-date')
          });
          showScreen('status');
        });
      });
```

Replace with:
```html
      /* ============================================================
         SCREEN 3 — HISTORY: SEED CARDS + REAL ORDERS
         Cards can be added after page load (a completed checkout),
         so filtering and the Detail button use delegated listeners
         on the list container instead of a one-time querySelectorAll
         snapshot — otherwise new cards would be invisible to both.
      ============================================================ */
      var pills    = $$('.filter-pill');
      var txnList  = document.getElementById('txnList');
      var txnEmpty = document.getElementById('txnEmpty');
      var activeFilter = 'all';

      function applyTxnFilter() {
        var shown = 0;
        $$('.txn-card', txnList).forEach(function (card) {
          var match = activeFilter === 'all' || card.getAttribute('data-status') === activeFilter;
          card.classList.toggle('hide', !match);
          if (match) shown++;
        });
        txnEmpty.classList.toggle('show', shown === 0);
      }

      pills.forEach(function (pill) {
        pill.addEventListener('click', function () {
          activeFilter = pill.getAttribute('data-filter');
          pills.forEach(function (p) {
            var on = p === pill;
            p.classList.toggle('active', on);
            p.setAttribute('aria-pressed', on ? 'true' : 'false');
          });
          applyTxnFilter();
        });
      });

      // "Detail" opens that order on the transaction status screen — delegated,
      // so it works for cards rendered after page load too.
      txnList.addEventListener('click', function (e) {
        var btn = e.target.closest ? e.target.closest('.txn-detail') : null;
        if (!btn) return;
        var card = btn.closest('.txn-card');
        var status = card.getAttribute('data-status');
        var order = {
          game: card.getAttribute('data-game'),
          pub: card.getAttribute('data-pub'),
          ref: card.getAttribute('data-ref'),
          uid: card.getAttribute('data-uid'),
          pkg: card.getAttribute('data-pkg'),
          amount: Number(card.getAttribute('data-amt')),
          date: card.getAttribute('data-date')
        };
        fillStatusCard(order);
        if (status === 'pending') { showPendingStatus(order, true); } else { showSuccessStatus(true); }
        showScreen('status');
      });

      function statusBadgeHtml(status) {
        if (status === 'pending') {
          return '<span class="badge badge-pending">' +
            '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>' +
            'Pending</span>';
        }
        return '<span class="badge badge-success">' +
          '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>' +
          'Success</span>';
      }

      function renderOrderCard(order) {
        var card = document.createElement('div');
        card.className = 'txn-card';
        card.setAttribute('data-status', order.status);
        card.setAttribute('data-game', order.game);
        card.setAttribute('data-pub', order.pub);
        card.setAttribute('data-uid', order.uid);
        card.setAttribute('data-pkg', order.pkg);
        card.setAttribute('data-amt', String(order.amount));
        card.setAttribute('data-ref', order.ref);
        card.setAttribute('data-date', order.date);

        card.innerHTML =
          '<div class="txn-icon generic"></div>' +
          '<div>' +
            '<div class="txn-game">' + order.game + '</div>' +
            '<div class="txn-sub">UID: ' + order.uid + '</div>' +
          '</div>' +
          '<div>' +
            '<div class="txn-pkg">' + order.pkg + '</div>' +
            '<div class="txn-date">' +
              '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="4" width="18" height="18" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/></svg>' +
              order.date +
            '</div>' +
          '</div>' +
          '<div>' +
            '<div class="txn-amt">' + baht(order.amount) + '</div>' +
            '<div class="txn-status">' + statusBadgeHtml(order.status) + '</div>' +
          '</div>' +
          '<button class="txn-detail">Detail</button>';

        txnList.insertBefore(card, txnList.firstChild);
        applyTxnFilter();
      }

      function updateOrderCardStatus(ref, status) {
        var card = $('.txn-card[data-ref="' + ref + '"]', txnList);
        if (!card) return;
        card.setAttribute('data-status', status);
        $('.txn-status', card).innerHTML = statusBadgeHtml(status);
        applyTxnFilter();
      }

      // paint any orders from previous visits, oldest first so the
      // final DOM order matches Orders.all()'s newest-first array
      Orders.all().slice().reverse().forEach(renderOrderCard);
```

- [ ] **Step 2: Verify in browser**

Reload, clear any leftover test data first (`localStorage.clear()` in the console, then reload). Complete a Card checkout for any game — land on status-success, go to History, confirm the new order appears at the top, above the 3 seed demo transactions, with the correct game/package/amount and a "Success" badge. Reload the page — the order is still there. Complete a PromptPay checkout — lands on the Pending screen; click "Detail" on that same order from History — Pending screen shows it correctly; click the History link from a resolved pending order — status is "Success" both on the Status screen and in History, and survives a reload. Click through all 5 filter pills (All/Success/Pending/Failed/Cancelled) — real orders and seed demo cards both respond correctly (note: "Failed"/"Cancelled" only ever match seed data, since real orders never produce those statuses — expected).

- [ ] **Step 3: Commit**

```bash
git add elasticshop-gaming.html
git commit -m "$(cat <<'EOF'
Render real orders in History, connect Status ↔ History

A completed checkout previously vanished after the Status screen —
History only ever showed 3 hardcoded demo transactions. Real orders
now render into the same list (newest first, above the seed demo
cards) using Orders.all(), and the pending→success refresh updates
both the Status screen and the matching History row via
Orders.updateStatus. Filtering and the Detail button switch from a
one-time DOM snapshot to delegated listeners so cards added after
page load are included.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 6: Lightweight local login (nickname only)

**Files:**
- Modify: `elasticshop-gaming.html` — add nav/profile personalization JS
- Modify: `elasticshop-gaming.html:1190` (History profile card name — add an id)

**Depends on:** Task 1 (`Profile`).

**Interfaces:** None consumed by later tasks.

- [ ] **Step 1: Give the profile-card name an id**

Find (exact current text):
```html
                <div class="pc-name">Ploy_Gamer99</div>
```

Replace with:
```html
                <div class="pc-name" id="pcName">Ploy_Gamer99</div>
```

- [ ] **Step 2: Add the login/profile logic**

Find (exact current INIT block — this is the same anchor Task 2 already modified; the "Find" text below reflects the state *after* Task 2's edit, so apply this only after Task 2 is in place):
```html
      /* ============================================================
         INIT
      ============================================================ */
      document.getElementById('year').textContent = new Date().getFullYear();
      selectPackage(selectedId);
      applyHomeFilter();
      applyTxnFilter();
      paintSelectedGame();
    })();
```

Replace with:
```html
      /* ============================================================
         LOGIN — local nickname only. There's no backend, so there's
         no password to check one against; this personalizes the
         nav and History profile card and nothing more.
      ============================================================ */
      var loginButtons = $$('.tn-login');
      var pcNameEl      = document.getElementById('pcName');

      function paintProfile() {
        var profile = Profile.get();
        var label = profile ? profile.name : 'Login';
        loginButtons.forEach(function (btn) { btn.textContent = label; });
        if (pcNameEl) pcNameEl.textContent = profile ? profile.name : 'Ploy_Gamer99';
      }

      loginButtons.forEach(function (btn) {
        btn.addEventListener('click', function () {
          var current = Profile.get();
          var name = window.prompt('What should we call you?', current ? current.name : '');
          if (name === null) return;          // cancelled
          name = name.trim();
          if (!name) return;                  // empty submit — ignore
          Profile.set(name);
          paintProfile();
        });
      });

      /* ============================================================
         INIT
      ============================================================ */
      document.getElementById('year').textContent = new Date().getFullYear();
      selectPackage(selectedId);
      applyHomeFilter();
      applyTxnFilter();
      paintSelectedGame();
      paintProfile();
    })();
```

- [ ] **Step 3: Verify in browser**

Reload. Click "Login" in the nav (any screen) — a browser prompt appears asking for a name. Enter "Ploy" — nav button now reads "Ploy" on every screen, and the History profile card's name updates to "Ploy" too. Reload the page — still shows "Ploy" (persisted). Click "Ploy" again, clear the field and submit — name stays "Ploy" (empty submissions are ignored, matching the step's documented behavior). Click "Ploy", then Cancel the prompt — name stays "Ploy" (cancel is a no-op).

- [ ] **Step 4: Commit**

```bash
git add elasticshop-gaming.html
git commit -m "$(cat <<'EOF'
Turn the no-op Login button into a real (nickname-only) login

"Login" previously just navigated to the History screen without
logging anything in. Captures a display name via a lightweight
prompt, persisted through Profile.set — no password, since there's
no backend to check one against. Personalizes the nav button and the
History profile card, replacing the hardcoded "Ploy_Gamer99" once a
name is set.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 7: Full-flow verification

**Files:** None modified — this task only runs checks. If it finds a regression, fix it in `elasticshop-gaming.html` and commit the fix before considering this task done.

**Interfaces:** None.

- [ ] **Step 1: Clean-slate full click-through**

`localStorage.clear()` in the console, reload. Pick 3 different games from 3 different Home categories (e.g. one from "เกมยอดนิยม," one from "เกมมือถือ," one from "บัตรเงินสด"). For each: complete a full checkout (Player Info already pre-filled — edit the UID to something distinct per run so orders are distinguishable) using a different payment method per run (Card, PromptPay, TrueMoney). Confirm each order's real game name/package/amount is correct at every screen it appears on (Summary → Status → History).

- [ ] **Step 2: Persistence check**

After Step 1, reload the page. All 3 real orders must still appear in History, in the same order, with the same statuses (the Card one "Success," the PromptPay/TrueMoney ones "Pending" unless you resolved them via the refresh button — resolve at least one and confirm it now reads "Success" after reload too).

- [ ] **Step 2b: Storage-failure note**

In the console, simulate a `localStorage` write failure: `var orig = Storage.prototype.setItem; Storage.prototype.setItem = function(){ throw new Error('quota'); };`. Complete one more checkout — it must still reach the Status screen (checkout is never blocked), and the success/pending sub-text must now include the "won't appear after you leave this page" note. Restore normal behavior afterward: `Storage.prototype.setItem = orig;`.

- [ ] **Step 3: Mobile overflow check on the new Payment step**

At 375×812 (per `CLAUDE.md`'s documented snippet, via whatever browser-automation tool is available at execution time), navigate into the Payment step specifically (Package → Continue to Payment) and run:
```js
({canScrollX: (function(){document.documentElement.scrollLeft=50;const s=document.documentElement.scrollLeft;document.documentElement.scrollLeft=0;return s>0;})(), bw:document.body.scrollWidth, cw:document.documentElement.clientWidth})
```
Expected: `canScrollX: false`, `bw === cw`. Check with the Card method selected too (card fields visible) since that's the tallest/most complex state of the new panel.

- [ ] **Step 4: Lighthouse audit**

Run `lighthouse_audit(device="mobile", mode="navigation")` on the local URL, per `CLAUDE.md`'s "Run a Lighthouse audit" instructions, on both `elasticshop-gaming.html` directly and after navigating into the Top Up → Payment state. Confirm Accessibility, Best Practices, and SEO all score 100.

- [ ] **Step 5: Login click-through**

Set a nickname, confirm it shows on Home, Top Up, and History nav bars simultaneously (all three `.tn-login` instances), and in the History profile card. Reload — still set.

- [ ] **Step 6: If all checks pass, no commit needed for this task** (verification-only). If any check failed and required a fix, stage and commit that fix with a message describing what regressed and why, following the same `Co-Authored-By` convention as the other tasks in this plan.
