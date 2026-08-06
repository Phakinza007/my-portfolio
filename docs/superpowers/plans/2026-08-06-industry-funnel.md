# Industry Funnel Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the homepage into a buyer funnel — a visitor who knows their industry reaches a page about that industry in one click, with matching demos and a real price.

**Architecture:** Seven new Thai-only industry landing pages built entirely from components already in `assets/portfolio-pages.css`, reached from a new selector section under the hero. The Selected Work filter's axis moves from system type (`landing`/`app`/`fullstack`) to industry, and card tags move from English style descriptors to the Thai terms buyers actually search. A pricing comparison section is added to the homepage.

**Tech Stack:** Plain HTML, CSS and vanilla JS. No framework, no build step, no new dependencies.

**Source spec:** `docs/superpowers/specs/2026-08-06-buyer-funnel-multipage-design.md`

**Scope note — this is plan 1 of 2.** It deliberately excludes the global nav, the client-side search, the five bilingual funnel pairs (`work`/`services`/`about`/`faq`/`process`), the homepage section reorder, and the clickable technology row. Those all depend on the nav and search existing, and are written as plan 2 once this lands. Everything here ships on its own and leaves the site fully working.

## Global Constraints

- **`main` auto-deploys to production.** Every commit must leave the site working and shippable. Never commit a link to a page that does not exist yet.
- **Quality bars, verified before any task is called done:** Accessibility 100, SEO 100 in Lighthouse mobile. Best Practices caps at 77 sitewide because Microsoft Clarity sets third-party cookies (`third-party-cookies` and `inspector-issues` are the only two audits that may fail) — this is the documented accepted exception, not a regression.
- **No horizontal overflow at 375×812** on any page: `canScrollX: false` and `body.scrollWidth === documentElement.clientWidth`.
- **`resize_window` does not take effect in this environment** — it reports success while the viewport stays at its real width. Use the 375×812 iframe method below and confirm `clientWidth === 375` before trusting any overflow result.
- **The site is dark-themed** (GitHub-dark derived — the stylesheet is versioned `?v=ghdark-2`). Do not introduce new colours; use the existing custom properties, whose real names are:

  | Purpose | Property | Value |
  |---|---|---|
  | Page background | `--bg` | `#0d1117` |
  | Card / raised surface | `--surface` | `#161b22` |
  | Deeper surface | `--surface-2` | `#1c2128` |
  | Body text | `--ink` | `#e6edf3` |
  | Secondary text | `--ink-2` | `#c9d1d9` |
  | Muted text | `--muted` | `#8b949e` |
  | Border | `--border` | `#21262d` |
  | Stronger border | `--border-2` | `#30363d` |
  | Accent | `--accent` | `#5274f8` |
  | Button background | `--accent-dark` | `#3651d4` |
  | Accent tint | `--accent-light` | `rgba(79,110,247,0.14)` |
  | Accent on dark | `--accent-text` | `#7c93fb` |

  Radii `--r`, `--r-sm`, `--r-lg`; shadows `--sh`, `--sh-sm`, `--sh-lg`; `--ease`; `--max`.
  There is **no** `--card`, `--line` or `--text` — those names do not exist.

- **Section markup idiom.** Every homepage section follows this shape. Match it; there is no `.wrap` and no existing subtitle class:

  ```html
  <section class="section" id="…" aria-labelledby="…-heading">
    <div class="container">
      <span class="section-label">EYEBROW</span>
      <h2 class="section-title" id="…-heading">Title</h2>
      …content…
    </div>
  </section>
  ```
- **Every new `.html` file** carries `<script src="assets/analytics.js" defer></script>` immediately before `</head>`, using the **relative** path.
- **The 7 industry pages are Thai-only.** No `hreflang` links, self-referential `canonical`, `robots: index, follow`, `<html lang="th">`, `og:locale` `th_TH`. This is the same class as the 13 demo pages.
- **Prices and package facts are copied verbatim** from the existing category pages. They are real Fastwork listings. Never reword or invent them:
  - Landing Page — `฿3,900` · `5-7 วัน` · `2 รอบ + ฟรีแก้บั๊ก 3 เดือน`
  - Dashboard UI — `฿7,900` · `7-10 วัน` · `2 รอบหลังส่งแบบ`
  - Business Website — `฿9,900` · `10-14 วัน` · `2 รอบ + ฟรีแก้บั๊ก 3 เดือน`
- **No unprovable claims.** No project counts, years of experience, client names, or statements that these demos were built with React/Node/Express/PostgreSQL. The 13 projects are simulated client work and all 12 local demos are plain HTML/CSS/vanilla JS.
- **Fastwork CTA URL** (used verbatim everywhere): `https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob`
- **Email CTA:** `mailto:a0626568471@gmail.com`

---

## File Structure

**Created (7):**

| File | Responsibility |
|---|---|
| `web-clinic.html` | Industry landing page — คลินิก / ความงาม |
| `web-booking.html` | Industry landing page — จองคิว / นัดหมาย |
| `web-restaurant.html` | Industry landing page — ร้านอาหาร / คาเฟ่ |
| `web-shop.html` | Industry landing page — ขายของออนไลน์ |
| `web-gym.html` | Industry landing page — ฟิตเนส / ยิม |
| `web-construction.html` | Industry landing page — ก่อสร้าง / รับเหมา |
| `web-solar.html` | Industry landing page — โซลาร์ / พลังงาน |

**Modified (4):**

| File | Change |
|---|---|
| `index.html` | Filter axis, card tags, need selector, pricing section |
| `index-en.html` | Same, with English tag labels and English chrome |
| `sitemap.xml` | 7 new URLs (59 → 66) |
| `CLAUDE.md` | Industry page class, corrected cards table, new sections |

No new CSS file. Every component used already exists in `assets/portfolio-pages.css`.

---

## Shared Industry Page Template

> **CORRECTED 2026-08-06 after Task 3.** The hand-written skeleton originally in this section had
> drifted from the real markup in five ways: it used `.container` instead of `.page-shell`, invented
> a `.meta-box` class, reversed the `<strong>`/`<span>` order inside `.study-meta`, omitted the
> `.result-band` inner `<div>`, and left out the page footer entirely. Task 3 caught all five —
> which is exactly why it runs alone before the fan-out.
>
> **The canonical skeleton is now `web-clinic.html` itself.** Copy that file and swap the content.
> The structure below documents what that file does; where the two ever disagree, the file wins.

Tasks 4–9 each build one page from this structure. `{{PLACEHOLDER}}` values are given in full in
each task.

### Structure that must be preserved

```
<header class="topbar">
  <nav class="page-shell nav" aria-label="เมนู{{NAV_LABEL}}">
    <a class="brand">  brand-mark svg + <span>{{H1_SHORT}}</span>
    <ul class="nav-links">  ผลงานทั้งหมด · บริการอื่นๆ · Fastwork (.nav-primary)
                            ← no EN link; these pages have no English twin
<main>
  <section class="hero case-hero">
    <div class="page-shell">                        eyebrow · h1 · .hero-copy · .hero-actions
    <div class="page-shell" style="margin-top:32px;">
      <div class="study-meta">  4 × bare <div> each holding <strong>label</strong><span>value</span>
                                ← strong FIRST, span SECOND. No .meta-box class exists.
  <section class="section" id="overview">
    <div class="page-shell study-grid">             ← combined class, not nested
      <article class="study-block featured">  showcase-icon &#10024; · eyebrow · h2 · ul.highlight-list
      <article class="study-block">           showcase-icon &#127919; · eyebrow · h2 · p
  <section class="section" id="related">
    <div class="page-shell">
      <div class="section-heading"><div>  eyebrow · h2
      <div class="project-strip">  a.project-link × N, each <strong>name</strong><span>desc</span>
  <section class="section" id="faq">
    <div class="page-shell">
      <div class="section-heading"><div>  eyebrow · h2
      <div class="study-grid">  article.study-block × 4, each h3 question + p answer
                                ← no showcase-icon, no eyebrow on FAQ blocks
  <section class="section" id="cta">
    <div class="page-shell">
      <div class="result-band">
        <div>  eyebrow · h2 · p
        <div class="result-actions">  Fastwork .button.primary + mailto .button
<footer class="footer-band">
  <div class="page-shell footer-inner">  <span>{{H1_SHORT}} — Phakin Chawanpunya</span><span>Phakin Chawanpunya</span>
```

Heading order is `h1` → `h2` × 4 → `h3` × 4 → `h2`, which has no skipped levels.

### Head block

```html
<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="{{META_DESC}}" />
  <meta name="theme-color" content="#5274f8" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="https://ph-akin.dev/{{SLUG}}.html" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{{TITLE}}" />
  <meta property="og:description" content="{{META_DESC}}" />
  <meta property="og:url" content="https://ph-akin.dev/{{SLUG}}.html" />
  <meta property="og:image" content="https://ph-akin.dev/assets/social-preview.png?v=ph-akin-dev" />
  <meta property="og:image:alt" content="Phakin Chawanpunya portfolio preview." />
  <meta property="og:locale" content="th_TH" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{{TITLE}}" />
  <meta name="twitter:description" content="{{META_DESC}}" />
  <meta name="twitter:image" content="https://ph-akin.dev/assets/social-preview.png?v=ph-akin-dev" />
  <title>{{TITLE}}</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=optional" rel="stylesheet">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml" />
  <link rel="manifest" href="site.webmanifest" />
  <link rel="stylesheet" href="assets/portfolio-pages.css?v=ghdark-2" />
  <script src="assets/analytics.js" defer></script>
</head>
```

### Body

Do not hand-write it. **Copy `web-clinic.html` and replace the content**, keeping every
structural detail listed above. That file is the verified reference implementation:
Lighthouse accessibility 100 / SEO 100, no overflow at 375×812, every class resolving in
`assets/portfolio-pages.css`.

**`{{FEATURE_ITEMS}}`** is a list of `<li>` elements.
**`{{FAQ_BLOCKS}}`** is a list of `<article class="study-block"><h3>Q</h3><p>A</p></article>`.
**`{{PROJECT_LINKS}}`** is a list of:

```html
<a class="project-link" href="{{SHOWCASE}}.html">
  <strong>{{PROJECT_NAME}}</strong>
  <span>{{PROJECT_DESC}}</span>
</a>
```

---

## Verification Recipes

Referenced by name from the tasks. Run them exactly as written.

**Recipe A — serve locally**

```bash
pkill -f "http.server 8123" 2>/dev/null
(python3 -m http.server 8123 >/dev/null 2>&1 &)
sleep 2 && curl -s -o /dev/null -w "server: %{http_code}\n" http://localhost:8123/index.html
```

**Recipe B — Lighthouse mobile on one page**

```bash
npx -y lighthouse "http://localhost:8123/PAGE.html" --quiet --chrome-flags="--headless" \
  --output=json --output-path=/tmp/lh-PAGE.json
python3 -c "
import json; d=json.load(open('/tmp/lh-PAGE.json'))
print({k: round(v['score']*100) for k,v in d['categories'].items() if v.get('score') is not None})
bp=[r['id'] for r in d['categories']['best-practices']['auditRefs']
    if d['audits'][r['id']].get('score') is not None and d['audits'][r['id']]['score']<1]
print('BP failures:', bp)
"
```
Expected: `accessibility: 100`, `seo: 100`. `BP failures` must be exactly `['third-party-cookies', 'inspector-issues']` — anything else is a real regression.

**Recipe C — mobile overflow at 375×812**

Open any same-origin page on `localhost:8123` in the browser, then run this in the page context. It injects a 375×812 iframe so the page's own media queries evaluate against a real 375px viewport. Window resizing does **not** work in this environment.

```js
const pages = ['PAGE1','PAGE2'];  // slugs without .html
const out = [];
for (const p of pages) {
  const f = document.createElement('iframe');
  f.style.cssText = 'position:fixed;top:0;left:0;width:375px;height:812px;border:0;z-index:99999;background:#fff';
  f.src = '/' + p + '.html';
  document.body.appendChild(f);
  await new Promise(r => { f.onload = r; setTimeout(r, 6000); });
  await new Promise(r => setTimeout(r, 900));
  const d = f.contentDocument, de = d.documentElement;
  de.scrollLeft = 50; const s = de.scrollLeft; de.scrollLeft = 0;
  const offenders = [];
  d.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width > 0 && (r.right > de.clientWidth + 1 || r.left < -1)) {
      offenders.push(el.tagName.toLowerCase() + '.' + (el.className || '') + ' [' + Math.round(r.left) + '→' + Math.round(r.right) + ']');
    }
  });
  out.push({ page: p, vw: de.clientWidth, canScrollX: s > 0, bw: d.body.scrollWidth, overflowing: offenders.slice(0, 5) });
  f.remove();
}
JSON.stringify(out, null, 1)
```
Expected per page: `vw: 375`, `canScrollX: false`, `bw: 375`, `overflowing: []`. **If `vw` is not 375 the result is meaningless** — the iframe did not size correctly, fix that before trusting anything.

**Recipe D — head-tag audit for the industry pages**

```bash
for f in web-clinic web-booking web-restaurant web-shop web-gym web-construction web-solar; do
  printf "%-18s hreflang:%s canonical:%s analytics:%s lang:%s robots:%s\n" "$f" \
    "$(grep -c hreflang $f.html)" \
    "$(grep -c "rel=\"canonical\" href=\"https://ph-akin.dev/$f.html\"" $f.html)" \
    "$(grep -c 'assets/analytics.js' $f.html)" \
    "$(grep -o '<html lang="[^"]*"' $f.html)" \
    "$(grep -c 'content="index, follow"' $f.html)"
done
```
Expected every row: `hreflang:0 canonical:1 analytics:1 lang:<html lang="th"> robots:1`.

---

## Task 1: Move the work filter from system type to industry

**Files:**
- Modify: `index.html` — filter bar ~lines 1820-1825, carousel clone ~line 2940-2945, filter JS ~lines 3104-3148, and the `data-tags` attribute on all 13 `.work-card` elements
- Modify: `index-en.html` — the same four places

**Interfaces:**
- Produces: `data-industry` on every `.work-card`, with values drawn from exactly this set: `clinic`, `booking`, `restaurant`, `shop`, `gym`, `construction`, `solar`, `other`. Task 10's need selector links to industry pages named after the first seven. Task 2 relies on the cards being otherwise untouched.

The current filter keys are `landing`, `app`, `dashboard`, `ecommerce`, `fullstack` — system-type vocabulary no shop owner uses. The existing JS derives its counts from the DOM, which is good and must be preserved.

- [ ] **Step 1: Write the check that currently fails**

Run Recipe A, open `http://localhost:8123/index.html`, then in the page context:

```js
(() => {
  const cards = [...document.querySelectorAll('.work-card[data-industry]')];
  const KEYS = ['clinic','booking','restaurant','shop','gym','construction','solar','other'];
  const bad = cards.flatMap(c => (c.dataset.industry || '').split(/\s+/).filter(v => v && !KEYS.includes(v)));
  return { cardCount: cards.length, unknownKeys: [...new Set(bad)] };
})()
```

- [ ] **Step 2: Run it and confirm it fails**

Expected right now: `{ cardCount: 0, unknownKeys: [] }` — no card carries `data-industry` yet.

- [ ] **Step 3: Rename the attribute on all 13 cards in `index.html`**

Replace `data-tags="..."` with `data-industry="..."` on each `.work-card`, using this mapping. The card order in the file is exactly this order.

| # | `work-name` | Old `data-tags` | New `data-industry` |
|---|---|---|---|
| 1 | BuildNest Construction | `landing` | `construction` |
| 2 | Iron Republic | `landing` | `gym` |
| 3 | NOIR Coffee | `landing` | `restaurant` |
| 4 | Elevate Commerce | `fullstack ecommerce` | `shop` |
| 5 | Elasticshop Gaming Top-Up | `fullstack ecommerce` | `shop` |
| 6 | RATRI Restaurant | `fullstack landing` | `restaurant` |
| 7 | SolarPeak | `landing` | `solar` |
| 8 | BookEase Dashboard | `fullstack dashboard` | `booking` |
| 9 | MuseRoom | `landing` | `other` |
| 10 | LUMI Clinic | `landing` | `clinic` |
| 11 | BRIGHT Dental Clinic | `landing` | `clinic` |
| 12 | VELVÉ Aesthetics | `landing app` | `clinic booking` |
| 13 | HabitQuest | `fullstack app` | `other` |

Leave `data-featured="1"` untouched where present (cards 1, 4, 6, 8, 12).

- [ ] **Step 4: Replace the filter bar markup in `index.html`**

Replace the six `<button class="filter-btn" …>` elements (around line 1820) with these nine. The `data-label` attribute is new — the JS needs a clean label without the count text.

```html
<button class="filter-btn active" data-filter="all" data-label="ทั้งหมด" aria-pressed="true">ทั้งหมด <span class="filter-count">13</span></button>
<button class="filter-btn" data-filter="clinic" data-label="คลินิก / ความงาม" aria-pressed="false">คลินิก / ความงาม <span class="filter-count">3</span></button>
<button class="filter-btn" data-filter="booking" data-label="จองคิว / นัดหมาย" aria-pressed="false">จองคิว / นัดหมาย <span class="filter-count">2</span></button>
<button class="filter-btn" data-filter="restaurant" data-label="ร้านอาหาร / คาเฟ่" aria-pressed="false">ร้านอาหาร / คาเฟ่ <span class="filter-count">2</span></button>
<button class="filter-btn" data-filter="shop" data-label="ขายของออนไลน์" aria-pressed="false">ขายของออนไลน์ <span class="filter-count">2</span></button>
<button class="filter-btn" data-filter="gym" data-label="ฟิตเนส / ยิม" aria-pressed="false">ฟิตเนส / ยิม <span class="filter-count">1</span></button>
<button class="filter-btn" data-filter="construction" data-label="ก่อสร้าง" aria-pressed="false">ก่อสร้าง <span class="filter-count">1</span></button>
<button class="filter-btn" data-filter="solar" data-label="โซลาร์ / พลังงาน" aria-pressed="false">โซลาร์ / พลังงาน <span class="filter-count">1</span></button>
<button class="filter-btn" data-filter="other" data-label="อื่นๆ" aria-pressed="false">อื่นๆ <span class="filter-count">2</span></button>
```

The counts above are the no-JS fallback values; the JS overwrites them from the DOM on load. They sum to 14 across 13 cards because VELVÉ Aesthetics is both `clinic` and `booking` — that is correct, not a mistake.

- [ ] **Step 5: Add the active-filter chip markup in `index.html`**

Insert immediately after the closing tag of the filter-bar container, before the works grid:

```html
<p class="active-filter" id="active-filter-chip" hidden>
  กำลังกรอง: <strong id="active-filter-label"></strong>
  <button type="button" id="active-filter-clear" class="active-filter-clear">ล้างตัวกรอง</button>
</p>
```

- [ ] **Step 6: Add the chip styles to the `<style>` block in `index.html`**

```css
.active-filter{display:flex;align-items:center;gap:.6rem;flex-wrap:wrap;margin:0 0 1.1rem;font-size:.92rem;color:var(--muted);}
.active-filter[hidden]{display:none;}
.active-filter strong{color:var(--ink);}
.active-filter-clear{border:1px solid var(--border);background:transparent;color:var(--ink);border-radius:999px;padding:.28rem .8rem;font:inherit;font-size:.85rem;cursor:pointer;}
.active-filter-clear:hover{border-color:var(--accent);color:var(--accent-text);}
.active-filter-clear:focus-visible{outline:2px solid var(--accent);outline-offset:2px;}
```

`--accent-text` (`#7c93fb`) rather than `--accent` for the hover text colour — `--accent` is tuned for use *as* a background, and this text sits on the dark page background.

- [ ] **Step 7: Fix the carousel clone in `index.html`**

Around line 2940 the carousel clones featured cards and strips attributes so clones never reach the filter. It currently removes `data-tags`, which no longer exists. Change:

```js
clone.removeAttribute('data-featured');
clone.removeAttribute('data-tags');
```

to:

```js
clone.removeAttribute('data-featured');
clone.removeAttribute('data-industry');
```

Missing this leaks 5 clone cards into every filtered result.

- [ ] **Step 8: Replace the filter JS in `index.html`**

Replace the whole `/* ---- Filter bar ---- */` block (roughly lines 3104-3148) with:

```js
      /* ---- Filter bar: one axis, industry ---- */
      const filterBtns   = document.querySelectorAll('.filter-btn');
      const cards        = document.querySelectorAll('.work-card[data-industry]');
      const emptyState   = document.getElementById('works-empty');
      const filterStatus = document.getElementById('filter-status');
      const chip         = document.getElementById('active-filter-chip');
      const chipLabel    = document.getElementById('active-filter-label');
      const chipClear    = document.getElementById('active-filter-clear');

      const industriesOf = card => (card.dataset.industry || '').trim().split(/\s+/).filter(Boolean);
      const matches = (card, filter) => filter === 'all' || industriesOf(card).includes(filter);

      /* Counts are derived from the DOM so they can never drift out of date. */
      filterBtns.forEach(btn => {
        const countEl = btn.querySelector('.filter-count');
        if (!countEl) return;
        let n = 0;
        cards.forEach(card => { if (matches(card, btn.dataset.filter)) n++; });
        countEl.textContent = String(n);
      });

      function applyFilter(filter, label) {
        let visible = 0;

        filterBtns.forEach(b => {
          const on = b.dataset.filter === filter;
          b.classList.toggle('active', on);
          b.setAttribute('aria-pressed', on ? 'true' : 'false');
        });

        cards.forEach(card => {
          if (matches(card, filter)) {
            delete card.dataset.hidden;
            visible++;
          } else {
            card.dataset.hidden = '';
          }
        });

        if (chip) {
          const show = filter !== 'all';
          chip.hidden = !show;
          if (show && chipLabel) chipLabel.textContent = label;
        }

        if (emptyState) emptyState.hidden = visible > 0;
        if (filterStatus) {
          filterStatus.textContent = visible === 0
            ? 'ยังไม่มีผลงานในหมวดนี้'
            : 'แสดง ' + visible + ' ผลงาน';
        }
      }

      filterBtns.forEach(btn => {
        btn.addEventListener('click', () => applyFilter(btn.dataset.filter, btn.dataset.label || ''));
      });

      if (chipClear) {
        chipClear.addEventListener('click', () => {
          applyFilter('all', '');
          const allBtn = document.querySelector('.filter-btn[data-filter="all"]');
          if (allBtn) allBtn.focus();
        });
      }
```

Returning focus to the "ทั้งหมด" button after clearing matters — otherwise a keyboard user's focus lands on a button that has just been hidden.

- [ ] **Step 9: Run the Step 1 check again**

Expected: `{ cardCount: 13, unknownKeys: [] }`

- [ ] **Step 10: Verify filter behaviour in the browser**

```js
(() => {
  const out = [];
  document.querySelectorAll('.filter-btn').forEach(b => {
    b.click();
    out.push({
      filter: b.dataset.filter,
      count: b.querySelector('.filter-count').textContent,
      visible: [...document.querySelectorAll('.work-card[data-industry]')].filter(c => !('hidden' in c.dataset)).length,
      chipShown: !document.getElementById('active-filter-chip').hidden,
      status: document.getElementById('filter-status').textContent
    });
  });
  document.querySelector('.filter-btn[data-filter="all"]').click();
  return out;
})()
```
Expected: `count === visible` on every row; `chipShown` false only for `all`; every filter's `visible` ≥ 1; `all` shows 13 — **not 18**, which would mean the carousel clones are leaking (Step 7).

- [ ] **Step 11: Repeat Steps 3-8 in `index-en.html`**

Same `data-industry` values and same JS. The **button labels are English**, the `data-filter` keys stay identical:

```html
<button class="filter-btn active" data-filter="all" data-label="All" aria-pressed="true">All <span class="filter-count">13</span></button>
<button class="filter-btn" data-filter="clinic" data-label="Clinic / Beauty" aria-pressed="false">Clinic / Beauty <span class="filter-count">3</span></button>
<button class="filter-btn" data-filter="booking" data-label="Booking" aria-pressed="false">Booking <span class="filter-count">2</span></button>
<button class="filter-btn" data-filter="restaurant" data-label="Restaurant / Café" aria-pressed="false">Restaurant / Café <span class="filter-count">2</span></button>
<button class="filter-btn" data-filter="shop" data-label="Online Store" aria-pressed="false">Online Store <span class="filter-count">2</span></button>
<button class="filter-btn" data-filter="gym" data-label="Fitness / Gym" aria-pressed="false">Fitness / Gym <span class="filter-count">1</span></button>
<button class="filter-btn" data-filter="construction" data-label="Construction" aria-pressed="false">Construction <span class="filter-count">1</span></button>
<button class="filter-btn" data-filter="solar" data-label="Solar / Energy" aria-pressed="false">Solar / Energy <span class="filter-count">1</span></button>
<button class="filter-btn" data-filter="other" data-label="Other" aria-pressed="false">Other <span class="filter-count">2</span></button>
```

The chip markup uses English copy:

```html
<p class="active-filter" id="active-filter-chip" hidden>
  Filtering by: <strong id="active-filter-label"></strong>
  <button type="button" id="active-filter-clear" class="active-filter-clear">Clear filter</button>
</p>
```

And the two status strings in the JS become `'No projects in this category yet'` and `'Showing ' + visible + ' projects'`.

- [ ] **Step 12: Run Step 10's check against `index-en.html`**

Same expectations.

- [ ] **Step 13: Run Recipe C for `index` and `index-en`**

Expected both: `vw: 375`, `canScrollX: false`, `overflowing: []`.

- [ ] **Step 14: Run Recipe B for `index.html`**

Expected: accessibility 100, seo 100, BP failures exactly `['third-party-cookies','inspector-issues']`.

- [ ] **Step 15: Commit**

```bash
git add index.html index-en.html
git commit -m "feat: move the work filter axis from system type to industry

The filter keys were landing/app/dashboard/ecommerce/fullstack — system
vocabulary. No shop owner thinks 'I need a fullstack'. They now name
industries, matching the seven industry pages that follow.

'อื่นๆ' is load-bearing: MuseRoom and HabitQuest match none of the seven
and would otherwise vanish from the filter entirely.

Adds an active-filter chip so a narrowed grid always explains itself, and
returns focus to 'ทั้งหมด' on clear rather than stranding it on a hidden
control. Counts stay derived from the DOM.

The carousel clone strips data-industry now that data-tags is gone —
without that, five clones leak into every filtered result."
```

---

## Task 2: Rewrite card tags as buyer search terms

**Files:**
- Modify: `index.html` — the `.work-tags` block inside each of the 13 `.work-card` elements
- Modify: `index-en.html` — same

**Interfaces:**
- Consumes: the `data-industry` attributes from Task 1. Nothing else depends on this task.

Current tags describe style to a designer (`Dark`, `Light UI`, `Design System`). They should name what the buyer's business is, using the words a Thai buyer types into Google.

Colour classes are unchanged from CLAUDE.md: `tag-mint` for tech/health, `tag-amber` for finance/energy/luxury, `tag-gray` default, `tag-rose` and `tag-accent` as already used.

- [ ] **Step 1: Replace the `.work-tags` block on all 13 cards in `index.html`**

| # | Card | Replacement `.work-tags` inner HTML |
|---|---|---|
| 1 | BuildNest Construction | `<span class="tag tag-gray">ก่อสร้าง</span><span class="tag tag-gray">รับเหมา</span><span class="tag tag-amber">ขอใบเสนอราคา</span>` |
| 2 | Iron Republic | `<span class="tag tag-amber">ฟิตเนส</span><span class="tag tag-gray">ยิม</span><span class="tag tag-gray">แพ็กเกจสมาชิก</span>` |
| 3 | NOIR Coffee | `<span class="tag tag-gray">คาเฟ่</span><span class="tag tag-gray">ร้านกาแฟ</span><span class="tag tag-rose">ธีมมืด</span>` |
| 4 | Elevate Commerce | `<span class="tag tag-accent">ขายของออนไลน์</span><span class="tag tag-gray">ตะกร้าสินค้า</span><span class="tag tag-gray">ชำระเงิน</span>` |
| 5 | Elasticshop Gaming Top-Up | `<span class="tag tag-accent">ขายของออนไลน์</span><span class="tag tag-amber">เติมเกม</span><span class="tag tag-gray">ร้านเกม</span>` |
| 6 | RATRI Restaurant | `<span class="tag tag-gray">ร้านอาหาร</span><span class="tag tag-amber">ไฟน์ไดนิ่ง</span><span class="tag tag-gray">จองโต๊ะ</span>` |
| 7 | SolarPeak | `<span class="tag tag-amber">โซลาร์เซลล์</span><span class="tag tag-gray">ติดตั้งโซลาร์</span><span class="tag tag-gray">ประหยัดค่าไฟ</span>` |
| 8 | BookEase Dashboard | `<span class="tag tag-gray">ระบบจองคิว</span><span class="tag tag-gray">นัดหมายออนไลน์</span><span class="tag tag-gray">แดชบอร์ด</span>` |
| 9 | MuseRoom | `<span class="tag tag-gray">แกลเลอรี</span><span class="tag tag-gray">งานศิลปะ</span><span class="tag tag-gray">นิทรรศการ</span>` |
| 10 | LUMI Clinic | `<span class="tag tag-amber">คลินิกความงาม</span><span class="tag tag-gray">จองคิวออนไลน์</span><span class="tag tag-gray">ดูแลผิว</span>` |
| 11 | BRIGHT Dental Clinic | `<span class="tag tag-mint">คลินิกทันตกรรม</span><span class="tag tag-gray">จัดฟัน</span><span class="tag tag-gray">รากเทียม</span>` |
| 12 | VELVÉ Aesthetics | `<span class="tag tag-amber">คลินิกความงาม</span><span class="tag tag-gray">จองคิวออนไลน์</span><span class="tag tag-gray">ฉีดฟิลเลอร์</span>` |
| 13 | HabitQuest | `<span class="tag tag-amber">แอปสร้างนิสัย</span><span class="tag tag-gray">เกมมิฟิเคชัน</span>` |

- [ ] **Step 2: Replace the `.work-tags` block on all 13 cards in `index-en.html`**

| # | Card | Replacement `.work-tags` inner HTML |
|---|---|---|
| 1 | BuildNest Construction | `<span class="tag tag-gray">Construction</span><span class="tag tag-gray">Contractor</span><span class="tag tag-amber">Quote Request</span>` |
| 2 | Iron Republic | `<span class="tag tag-amber">Fitness</span><span class="tag tag-gray">Gym</span><span class="tag tag-gray">Memberships</span>` |
| 3 | NOIR Coffee | `<span class="tag tag-gray">Café</span><span class="tag tag-gray">Coffee Shop</span><span class="tag tag-rose">Dark Theme</span>` |
| 4 | Elevate Commerce | `<span class="tag tag-accent">Online Store</span><span class="tag tag-gray">Cart</span><span class="tag tag-gray">Checkout</span>` |
| 5 | Elasticshop Gaming Top-Up | `<span class="tag tag-accent">Online Store</span><span class="tag tag-amber">Game Top-Up</span><span class="tag tag-gray">Game Shop</span>` |
| 6 | RATRI Restaurant | `<span class="tag tag-gray">Restaurant</span><span class="tag tag-amber">Fine Dining</span><span class="tag tag-gray">Table Booking</span>` |
| 7 | SolarPeak | `<span class="tag tag-amber">Solar</span><span class="tag tag-gray">Installation</span><span class="tag tag-gray">Bill Savings</span>` |
| 8 | BookEase Dashboard | `<span class="tag tag-gray">Booking System</span><span class="tag tag-gray">Appointments</span><span class="tag tag-gray">Dashboard</span>` |
| 9 | MuseRoom | `<span class="tag tag-gray">Gallery</span><span class="tag tag-gray">Art</span><span class="tag tag-gray">Exhibition</span>` |
| 10 | LUMI Clinic | `<span class="tag tag-amber">Beauty Clinic</span><span class="tag tag-gray">Online Booking</span><span class="tag tag-gray">Skincare</span>` |
| 11 | BRIGHT Dental Clinic | `<span class="tag tag-mint">Dental Clinic</span><span class="tag tag-gray">Braces</span><span class="tag tag-gray">Implants</span>` |
| 12 | VELVÉ Aesthetics | `<span class="tag tag-amber">Beauty Clinic</span><span class="tag tag-gray">Online Booking</span><span class="tag tag-gray">Fillers</span>` |
| 13 | HabitQuest | `<span class="tag tag-amber">Habit App</span><span class="tag tag-gray">Gamification</span>` |

- [ ] **Step 3: Confirm no tag exceeds the card width at 375px**

Run Recipe C for `index` and `index-en`. Thai tag strings are longer than the English originals, so this is the real risk in this task.

Expected: `overflowing: []` on both.

- [ ] **Step 4: Run Recipe B for `index.html` and `index-en.html`**

Expected: accessibility 100, seo 100 on both.

- [ ] **Step 5: Commit**

```bash
git add index.html index-en.html
git commit -m "feat: rewrite card tags as buyer search terms

Tags described style to a designer — Dark, Light UI, Design System. They
now name the buyer's business in the words a Thai buyer actually types:
คลินิกทันตกรรม, จัดฟัน, ขอใบเสนอราคา.

English cards get English equivalents; both languages keep the same
data-industry keys so the filter behaves identically."
```

---

## Task 3: Build `web-clinic.html`

**Files:**
- Create: `web-clinic.html`

**Interfaces:**
- Consumes: the Shared Industry Page Template above.
- Produces: `web-clinic.html` at `https://ph-akin.dev/web-clinic.html`. Task 10 links to it; Task 12 sitemaps it.

This is the strongest industry page — three demos back it.

- [ ] **Step 1: Create the file from the Shared Industry Page Template with these values**

| Placeholder | Value |
|---|---|
| `{{SLUG}}` | `web-clinic` |
| `{{TITLE}}` | `รับทำเว็บคลินิก / คลินิกความงาม เริ่มต้น ฿3,900 \| Phakin Chawanpunya` |
| `{{META_DESC}}` | `รับทำเว็บไซต์คลินิกความงามและคลินิกทันตกรรม เริ่มต้น 3,900 บาท ส่งงานใน 5-7 วัน มีระบบจองคิวออนไลน์ หน้าแนะนำหมอและบริการ ดูตัวอย่างผลงานคลินิกจริง 3 เว็บ` |
| `{{NAV_LABEL}}` | `คลินิก` |
| `{{H1_SHORT}}` | `รับทำเว็บคลินิก` |
| `{{H1}}` | `รับทำเว็บคลินิก และคลินิกความงาม` |
| `{{HERO_COPY}}` | `เว็บคลินิกไม่เหมือนเว็บทั่วไป คนไข้เข้ามาหาสามอย่าง — บริการมีอะไรบ้าง ราคาประมาณเท่าไหร่ และจะจองคิวยังไง ผมออกแบบให้ตอบครบสามข้อนี้ตั้งแต่หน้าแรก ไม่ต้องโทรถาม` |
| `{{PRICE}}` | `฿3,900` |
| `{{TIMELINE}}` | `5-7 วัน` |
| `{{REVISIONS}}` | `2 รอบ + ฟรีแก้บั๊ก 3 เดือน` |
| `{{BEST_FOR}}` | `คลินิกที่อยากให้คนไข้จองคิวเองได้` |
| `{{FEATURES_H2}}` | `สิ่งที่เว็บคลินิกควรมี` |
| `{{WHO_H2}}` | `เหมาะกับคลินิกแบบไหน` |
| `{{RELATED_H2}}` | `ตัวอย่างเว็บคลินิกที่เคยทำ` |
| `{{CTA_H2}}` | `อยากได้เว็บคลินิกแบบนี้บ้าง?` |

`{{FEATURE_ITEMS}}`:

```html
<li>ปุ่มจองคิวหรือทักไลน์ ติดอยู่ทุกหน้าจอ ไม่ต้องเลื่อนหา</li>
<li>หน้ารวมบริการ แยกเป็นหมวด พร้อมช่วงราคาที่ชัดเจน</li>
<li>โปรไฟล์แพทย์และทีมงาน พร้อมวุฒิและประสบการณ์</li>
<li>แกลเลอรีก่อน-หลัง จัดวางให้ดูน่าเชื่อถือ ไม่ดูเกินจริง</li>
<li>แผนที่ เวลาทำการ และช่องทางติดต่อครบทุกช่อง</li>
<li>โครงสร้างรองรับ SEO เพื่อให้คนค้นเจอตอนหาคลินิกแถวนั้น</li>
```

`{{WHO_COPY}}`:

```html
เหมาะกับคลินิกความงาม คลินิกทันตกรรม คลินิกผิวหนัง และคลินิกเฉพาะทางที่เปิดมาแล้วระยะหนึ่ง มีบริการชัดเจน และเริ่มเสียเวลากับการตอบคำถามซ้ำ ๆ ทางโทรศัพท์หรือแชท — เว็บที่ดีจะรับงานตอบคำถามพวกนั้นแทนคุณ
```

`{{PROJECT_LINKS}}`:

```html
<a class="project-link" href="showcase-lumi-clinic.html">
  <strong>LUMI Clinic</strong>
  <span>คลินิกความงาม เน้นภาพลักษณ์พรีเมียม พร้อมหน้าบริการและช่องทางจองคิว</span>
</a>
<a class="project-link" href="showcase-dental-clinic.html">
  <strong>BRIGHT Dental Clinic</strong>
  <span>คลินิกทันตกรรม จัดหมวดบริการทำฟัน จัดฟัน รากเทียม พร้อมระบบนัดหมาย</span>
</a>
<a class="project-link" href="showcase-velve-aesthetics.html">
  <strong>VELVÉ Aesthetics</strong>
  <span>คลินิกความงามที่มีขั้นตอนจองคิวแบบโต้ตอบได้ในหน้าเดียว</span>
</a>
```

`{{FAQ_BLOCKS}}`:

```html
<article class="study-block">
  <h3>ทำเว็บคลินิกราคาเท่าไหร่?</h3>
  <p>เริ่มต้น ฿3,900 สำหรับเว็บหน้าเดียวที่ครบทั้งบริการ ทีมแพทย์ และปุ่มจองคิว ถ้าต้องการหลายหน้าแยกตามบริการพร้อมโครงสร้าง SEO เต็มรูปแบบ อยู่ที่ ฿9,900</p>
</article>
<article class="study-block">
  <h3>ระบบจองคิวออนไลน์รวมอยู่ในราคาไหม?</h3>
  <p>ปุ่มจองที่เชื่อมไปยังไลน์ ฟอร์ม หรือระบบจองที่คลินิกใช้อยู่ รวมอยู่แล้ว ถ้าต้องการระบบจองที่มีปฏิทินและหลังบ้านจัดการคิวเอง เป็นงานคนละส่วน เริ่มที่ ฿7,900</p>
</article>
<article class="study-block">
  <h3>คลินิกต้องเตรียมอะไรบ้าง?</h3>
  <p>รายการบริการพร้อมช่วงราคา ข้อมูลแพทย์ รูปคลินิก และโลโก้ ถ้ายังไม่มีรูปที่ใช้ได้ ผมช่วยจัดวางด้วยภาพประกอบก่อนได้ แล้วค่อยเปลี่ยนเป็นรูปจริงทีหลัง</p>
</article>
<article class="study-block">
  <h3>ทำแล้วคนจะเจอเราใน Google ไหม?</h3>
  <p>ผมวางโครงสร้างหน้าให้รองรับการค้นหาตั้งแต่แรก — หัวข้อ คำอธิบาย และชื่อหน้าเขียนตามคำที่คนไข้ค้นจริง แต่การขึ้นอันดับต้องใช้เวลาและขึ้นกับการแข่งขันในพื้นที่ ผมไม่รับประกันอันดับ เพราะไม่มีใครรับประกันได้จริง</p>
</article>
```

- [ ] **Step 2: Run Recipe D**

Expected for `web-clinic`: `hreflang:0 canonical:1 analytics:1 lang:<html lang="th"> robots:1`.

- [ ] **Step 3: Run Recipe C for `web-clinic`**

Expected: `vw: 375`, `canScrollX: false`, `overflowing: []`.

- [ ] **Step 4: Run Recipe B for `web-clinic.html`**

Expected: accessibility 100, seo 100, BP failures exactly the two Clarity audits.

- [ ] **Step 5: Confirm every internal link resolves**

```bash
grep -oE 'href="[a-z0-9-]+\.html"' web-clinic.html | sed 's/href="//;s/"//' | sort -u | while read f; do
  [ -f "$f" ] && echo "OK   $f" || echo "DEAD $f"
done
```
Expected: no `DEAD` rows.

- [ ] **Step 6: Commit**

```bash
git add web-clinic.html
git commit -m "feat: add the clinic industry landing page

Three demos back this one — LUMI, BRIGHT Dental and VELVÉ — so it leads
with real work rather than claims.

Thai-only by design: 'รับทำเว็บคลินิก' is a Thai-only search intent, so
an -en twin would double the file for traffic that does not exist. Same
class as the 13 demo pages: no hreflang, self canonical, index+follow.

The SEO FAQ answer refuses to promise rankings. Nobody can, and a clinic
owner who has been promised page one by someone else will notice."
```

---

## Task 4: Build `web-booking.html`

**Files:**
- Create: `web-booking.html`

**Interfaces:**
- Consumes: the Shared Industry Page Template.
- Produces: `web-booking.html`. Linked by Task 10, sitemapped by Task 12.

This page sells the ฿7,900 Dashboard UI package, not the ฿3,900 one — a booking system is a system, not a page.

- [ ] **Step 1: Create the file from the Shared Industry Page Template with these values**

| Placeholder | Value |
|---|---|
| `{{SLUG}}` | `web-booking` |
| `{{TITLE}}` | `รับทำระบบจองคิวออนไลน์ เริ่มต้น ฿7,900 \| Phakin Chawanpunya` |
| `{{META_DESC}}` | `รับทำเว็บระบบจองคิวและนัดหมายออนไลน์ เริ่มต้น 7,900 บาท มีปฏิทินว่าง จัดการคิวหลังบ้าน และแจ้งเตือนลูกค้า ดูตัวอย่างระบบจองจริง` |
| `{{NAV_LABEL}}` | `ระบบจอง` |
| `{{H1_SHORT}}` | `รับทำระบบจองคิว` |
| `{{H1}}` | `รับทำระบบจองคิว และนัดหมายออนไลน์` |
| `{{HERO_COPY}}` | `ถ้าตอนนี้ยังรับจองผ่านแชทแล้วจดลงสมุด ปัญหาไม่ใช่เรื่องเสียเวลาอย่างเดียว แต่คือคิวชนกันและลูกค้าไม่มาโดยไม่บอก ระบบจองที่ดีตัดปัญหาทั้งสองอย่างตั้งแต่ต้นทาง` |
| `{{PRICE}}` | `฿7,900` |
| `{{TIMELINE}}` | `7-10 วัน` |
| `{{REVISIONS}}` | `2 รอบหลังส่งแบบ` |
| `{{BEST_FOR}}` | `ธุรกิจที่รับจองผ่านแชทจนคิวชนกัน` |
| `{{FEATURES_H2}}` | `สิ่งที่ระบบจองควรทำได้` |
| `{{WHO_H2}}` | `เหมาะกับธุรกิจแบบไหน` |
| `{{RELATED_H2}}` | `ตัวอย่างระบบจองที่เคยทำ` |
| `{{CTA_H2}}` | `อยากเลิกจดคิวลงสมุดแล้วใช่ไหม?` |

`{{FEATURE_ITEMS}}`:

```html
<li>ปฏิทินแสดงช่วงเวลาที่ว่างจริง ลูกค้าเลือกเองได้ ไม่ต้องถามกลับ</li>
<li>กันคิวชน — เวลาที่ถูกจองแล้วหายจากตัวเลือกทันที</li>
<li>หน้าหลังบ้านดูคิววันนี้ ทั้งสัปดาห์ และย้อนหลังได้</li>
<li>เก็บข้อมูลลูกค้าที่จำเป็น เบอร์ ชื่อ บริการที่เลือก ครบในขั้นตอนเดียว</li>
<li>ส่งข้อความยืนยันและเตือนก่อนถึงคิว ลดการไม่มาตามนัด</li>
<li>ใช้งานบนมือถือได้เต็มรูปแบบ เพราะลูกค้าส่วนใหญ่จองจากมือถือ</li>
```

`{{WHO_COPY}}`:

```html
เหมาะกับคลินิก ร้านทำผม ร้านนวดและสปา สนามกีฬา สตูดิโอ และบริการที่ขายเป็นช่วงเวลา โดยเฉพาะเมื่อมีมากกว่าหนึ่งคนหรือหนึ่งห้องให้จอง ซึ่งเป็นจุดที่การจดมือเริ่มพลาด
```

`{{PROJECT_LINKS}}`:

```html
<a class="project-link" href="showcase-bookease.html">
  <strong>BookEase Dashboard</strong>
  <span>หน้าหลังบ้านจัดการคิวและการจอง ดูสถานะทั้งวันได้ในหน้าจอเดียว</span>
</a>
<a class="project-link" href="showcase-velve-aesthetics.html">
  <strong>VELVÉ Aesthetics</strong>
  <span>ขั้นตอนจองคิวแบบโต้ตอบ เลือกบริการและเวลาได้จบในหน้าเดียว</span>
</a>
```

`{{FAQ_BLOCKS}}`:

```html
<article class="study-block">
  <h3>ต่างจากการใช้ฟอร์มจองธรรมดายังไง?</h3>
  <p>ฟอร์มธรรมดาแค่ส่งข้อมูลมาให้คุณ แล้วคุณต้องเช็กเองว่าเวลานั้นว่างไหม ระบบจองรู้ตารางของคุณ จึงตัดเวลาที่เต็มแล้วออกก่อนที่ลูกค้าจะเลือกได้</p>
</article>
<article class="study-block">
  <h3>ราคา ฿7,900 รวมอะไรบ้าง?</h3>
  <p>รวมการออกแบบหน้าจอระบบสูงสุด 5 หน้าจอ พร้อมส่งไฟล์ออกแบบฉบับเต็มที่ทีมพัฒนานำไปทำต่อได้ทันที และแก้ไขได้ 2 รอบหลังส่งแบบ</p>
</article>
<article class="study-block">
  <h3>เชื่อมกับ Google Calendar หรือ LINE ได้ไหม?</h3>
  <p>ได้ แต่เป็นงานเชื่อมต่อที่คิดแยกจากราคาเริ่มต้น เพราะขึ้นกับว่าปลายทางเป็นระบบอะไรและมี API ให้ใช้แค่ไหน คุยรายละเอียดก่อนแล้วผมประเมินให้</p>
</article>
<article class="study-block">
  <h3>ลูกค้าต้องสมัครสมาชิกก่อนจองไหม?</h3>
  <p>ไม่ต้อง และผมแนะนำว่าอย่าบังคับ การให้กรอกแค่ชื่อกับเบอร์แล้วจองได้เลย ทำให้คนจองจบมากกว่าการให้ตั้งรหัสผ่านก่อนอย่างชัดเจน</p>
</article>
```

- [ ] **Step 2: Run Recipe D, Recipe C for `web-booking`, and Recipe B for `web-booking.html`**

Expected as in Task 3.

- [ ] **Step 3: Confirm every internal link resolves**

```bash
grep -oE 'href="[a-z0-9-]+\.html"' web-booking.html | sed 's/href="//;s/"//' | sort -u | while read f; do
  [ -f "$f" ] && echo "OK   $f" || echo "DEAD $f"
done
```
Expected: no `DEAD` rows.

- [ ] **Step 4: Commit**

```bash
git add web-booking.html
git commit -m "feat: add the booking-system industry landing page

Sells the ฿7,900 Dashboard UI package rather than the ฿3,900 one — a
booking system is a system, not a page, and pricing it like a landing
page would misrepresent the work.

The integration FAQ says calendar and LINE hookups are quoted separately
instead of implying they are included, and the signup FAQ argues against
forcing account creation, which is the single biggest drop-off in booking
flows."
```

---

## Task 5: Build `web-restaurant.html`

**Files:**
- Create: `web-restaurant.html`

**Interfaces:**
- Consumes: the Shared Industry Page Template.
- Produces: `web-restaurant.html`. Linked by Task 10, sitemapped by Task 12.

- [ ] **Step 1: Create the file from the Shared Industry Page Template with these values**

| Placeholder | Value |
|---|---|
| `{{SLUG}}` | `web-restaurant` |
| `{{TITLE}}` | `รับทำเว็บร้านอาหาร และคาเฟ่ เริ่มต้น ฿3,900 \| Phakin Chawanpunya` |
| `{{META_DESC}}` | `รับทำเว็บไซต์ร้านอาหารและคาเฟ่ เริ่มต้น 3,900 บาท มีเมนูพร้อมราคา จองโต๊ะ แผนที่ และเวลาเปิดปิด ดูตัวอย่างเว็บร้านอาหารจริง` |
| `{{NAV_LABEL}}` | `ร้านอาหาร` |
| `{{H1_SHORT}}` | `รับทำเว็บร้านอาหาร` |
| `{{H1}}` | `รับทำเว็บร้านอาหาร และคาเฟ่` |
| `{{HERO_COPY}}` | `คนที่ค้นหาร้านคุณตอนนี้กำลังหิวและกำลังตัดสินใจ เขาอยากรู้แค่สามอย่าง — มีอะไรกิน ราคาประมาณไหน และไปยังไง เว็บที่ตอบสามข้อนี้ได้ใน 10 วินาที ชนะเว็บสวยที่หาเมนูไม่เจอ` |
| `{{PRICE}}` | `฿3,900` |
| `{{TIMELINE}}` | `5-7 วัน` |
| `{{REVISIONS}}` | `2 รอบ + ฟรีแก้บั๊ก 3 เดือน` |
| `{{BEST_FOR}}` | `ร้านที่อยากให้คนหาเมนูและที่ตั้งเจอเร็ว` |
| `{{FEATURES_H2}}` | `สิ่งที่เว็บร้านอาหารควรมี` |
| `{{WHO_H2}}` | `เหมาะกับร้านแบบไหน` |
| `{{RELATED_H2}}` | `ตัวอย่างเว็บร้านอาหารที่เคยทำ` |
| `{{CTA_H2}}` | `อยากได้เว็บร้านแบบนี้บ้าง?` |

`{{FEATURE_ITEMS}}`:

```html
<li>เมนูพร้อมราคา อ่านง่ายบนมือถือ ไม่ใช่รูปเมนูที่ต้องซูม</li>
<li>ปุ่มโทรและปุ่มนำทางไป Google Maps อยู่ในระยะนิ้วโป้งตลอด</li>
<li>เวลาเปิด-ปิด แสดงชัด รวมวันหยุดพิเศษ</li>
<li>ฟอร์มจองโต๊ะหรือปุ่มทักไลน์ สำหรับร้านที่รับจอง</li>
<li>ภาพบรรยากาศร้านและอาหาร จัดวางให้โหลดเร็วไม่กินเน็ต</li>
<li>รองรับการค้นหาแบบ "ร้านอาหาร + ชื่อย่าน" ที่คนใช้จริง</li>
```

`{{WHO_COPY}}`:

```html
เหมาะกับร้านอาหาร คาเฟ่ ร้านกาแฟ บาร์ และร้านที่มีหน้าร้านจริง โดยเฉพาะร้านที่ตอนนี้มีแต่เพจโซเชียล แล้วลูกค้าใหม่หาเมนูกับเวลาเปิดปิดไม่เจอ เพราะโพสต์เก่าถูกดันลงไปหมดแล้ว
```

`{{PROJECT_LINKS}}`:

```html
<a class="project-link" href="showcase-ratri-restaurant.html">
  <strong>RATRI Restaurant</strong>
  <span>ร้านอาหารไฟน์ไดนิ่ง เน้นบรรยากาศและคอร์สเมนู พร้อมช่องทางจองโต๊ะ</span>
</a>
<a class="project-link" href="showcase-noir-coffee.html">
  <strong>NOIR Coffee</strong>
  <span>คาเฟ่ธีมมืด โชว์เมนูเครื่องดื่มและบรรยากาศร้านเป็นหลัก</span>
</a>
```

`{{FAQ_BLOCKS}}`:

```html
<article class="study-block">
  <h3>มีแต่เพจ Facebook อยู่แล้ว ยังต้องทำเว็บอีกไหม?</h3>
  <p>เพจดีเรื่องคนติดตามและโพสต์ประจำ แต่ลูกค้าใหม่ที่ค้นใน Google มักไม่เจอเพจก่อน และถึงเจอก็ต้องเลื่อนหาเมนูในโพสต์เก่า เว็บทำหน้าที่เป็นที่ที่ข้อมูลนิ่งอยู่ตลอด</p>
</article>
<article class="study-block">
  <h3>เมนูเปลี่ยนบ่อย แก้เองได้ไหม?</h3>
  <p>แพ็กเกจ ฿3,900 เป็นเว็บที่ผมส่งมอบแล้วแก้ให้ตามรอบที่ตกลง ถ้าอยากแก้เมนูเองบ่อย ๆ ควรคุยกันตั้งแต่ต้นเพื่อวางโครงให้แก้ง่าย หรือขยับไปแพ็กเกจที่ใหญ่กว่า</p>
</article>
<article class="study-block">
  <h3>รับทำระบบสั่งอาหารออนไลน์ด้วยไหม?</h3>
  <p>ระบบสั่งอาหารพร้อมตะกร้าและชำระเงินเป็นงานคนละขนาดกับหน้าเว็บร้าน อยู่ในกลุ่มเว็บขายของออนไลน์ เริ่มที่ ฿9,900 คุยรายละเอียดก่อนแล้วผมประเมินให้</p>
</article>
<article class="study-block">
  <h3>ยังไม่มีรูปอาหารสวย ๆ ทำได้ไหม?</h3>
  <p>ทำได้ แต่ตรงไปตรงมาคือรูปคือครึ่งหนึ่งของเว็บร้านอาหาร ผมจัดวางด้วยภาพประกอบให้ก่อนได้ แล้วเปลี่ยนเป็นรูปจริงทีหลัง แต่ถ้าลงทุนถ่ายรูปได้ก่อน ผลลัพธ์ต่างกันมาก</p>
</article>
```

- [ ] **Step 2: Run Recipe D, Recipe C for `web-restaurant`, and Recipe B for `web-restaurant.html`**

Expected as in Task 3.

- [ ] **Step 3: Confirm every internal link resolves**

```bash
grep -oE 'href="[a-z0-9-]+\.html"' web-restaurant.html | sed 's/href="//;s/"//' | sort -u | while read f; do
  [ -f "$f" ] && echo "OK   $f" || echo "DEAD $f"
done
```
Expected: no `DEAD` rows.

- [ ] **Step 4: Commit**

```bash
git add web-restaurant.html
git commit -m "feat: add the restaurant and café industry landing page

Leads on the three things a hungry searcher actually wants — menu, price
range, directions — rather than on visual atmosphere.

The photography FAQ says plainly that photos are half the job and that
placeholder illustrations are a stopgap. Overselling that would produce a
disappointed client at handover."
```

---

## Task 6: Build `web-shop.html`

**Files:**
- Create: `web-shop.html`

**Interfaces:**
- Consumes: the Shared Industry Page Template.
- Produces: `web-shop.html`. Linked by Task 10, sitemapped by Task 12.

This page sells the ฿9,900 Business Website package.

- [ ] **Step 1: Create the file from the Shared Industry Page Template with these values**

| Placeholder | Value |
|---|---|
| `{{SLUG}}` | `web-shop` |
| `{{TITLE}}` | `รับทำเว็บขายของออนไลน์ เริ่มต้น ฿9,900 \| Phakin Chawanpunya` |
| `{{META_DESC}}` | `รับทำเว็บไซต์ขายของออนไลน์ เริ่มต้น 9,900 บาท มีหน้าสินค้า ตะกร้า ขั้นตอนสั่งซื้อ และโครงสร้างรองรับ SEO ดูตัวอย่างเว็บร้านค้าออนไลน์จริง` |
| `{{NAV_LABEL}}` | `ร้านค้าออนไลน์` |
| `{{H1_SHORT}}` | `รับทำเว็บขายของออนไลน์` |
| `{{H1}}` | `รับทำเว็บขายของออนไลน์` |
| `{{HERO_COPY}}` | `ขายในมาร์เก็ตเพลสได้ยอด แต่ไม่ได้ลูกค้า เพราะลูกค้าเป็นของแพลตฟอร์ม ไม่ใช่ของคุณ เว็บของตัวเองคือที่เดียวที่คุณคุมทั้งราคา หน้าตา และรายชื่อลูกค้าเอง` |
| `{{PRICE}}` | `฿9,900` |
| `{{TIMELINE}}` | `10-14 วัน` |
| `{{REVISIONS}}` | `2 รอบ + ฟรีแก้บั๊ก 3 เดือน` |
| `{{BEST_FOR}}` | `ร้านที่มีสินค้าประจำและอยากมีหน้าร้านของตัวเอง` |
| `{{FEATURES_H2}}` | `สิ่งที่เว็บขายของควรมี` |
| `{{WHO_H2}}` | `เหมาะกับร้านแบบไหน` |
| `{{RELATED_H2}}` | `ตัวอย่างเว็บขายของที่เคยทำ` |
| `{{CTA_H2}}` | `อยากมีหน้าร้านเป็นของตัวเองไหม?` |

`{{FEATURE_ITEMS}}`:

```html
<li>หน้าสินค้าที่บอกครบ รูป ราคา ตัวเลือก และของพร้อมส่งหรือไม่</li>
<li>ตะกร้าและขั้นตอนสั่งซื้อที่สั้นที่สุดเท่าที่จะสั้นได้</li>
<li>จัดหมวดหมู่และค้นหาสินค้า สำหรับร้านที่มีของหลายรายการ</li>
<li>วางโครงสร้างรองรับ SEO พื้นฐาน ให้สินค้าถูกค้นเจอทีละชิ้น</li>
<li>ฟอร์มติดต่อหรือปุ่ม LINE OA สำหรับรับลูกค้าของคุณ</li>
<li>แก้ไขงานได้ 2 รอบ ฟรีบริการแก้ไขปัญหา 3 เดือน</li>
```

`{{WHO_COPY}}`:

```html
เหมาะกับร้านที่มีสินค้าประจำและขายซ้ำได้ ไม่ใช่ของมือสองชิ้นเดียวจบ โดยเฉพาะร้านที่ตอนนี้พึ่งมาร์เก็ตเพลสหรือไลฟ์ขายอย่างเดียว แล้วเริ่มรู้สึกว่าค่าธรรมเนียมกินกำไรและคุมหน้าตาแบรนด์ไม่ได้
```

`{{PROJECT_LINKS}}`:

```html
<a class="project-link" href="showcase-elevate-commerce.html">
  <strong>Elevate Commerce</strong>
  <span>ร้านค้าออนไลน์ครบขั้นตอน ตั้งแต่หน้าสินค้าจนถึงตะกร้าและการชำระเงิน</span>
</a>
<a class="project-link" href="showcase-elasticshop-gaming.html">
  <strong>Elasticshop Gaming Top-Up</strong>
  <span>ร้านเติมเกมและไอเทม เน้นขั้นตอนสั่งซื้อที่จบเร็วที่สุด</span>
</a>
```

`{{FAQ_BLOCKS}}`:

```html
<article class="study-block">
  <h3>ต่างจากเปิดร้านใน Shopee หรือ Lazada ยังไง?</h3>
  <p>มาร์เก็ตเพลสมีคนเดินผ่านเยอะ ซึ่งเป็นข้อดีจริง แต่คุณแข่งราคากับร้านข้าง ๆ ตลอด และไม่ได้ข้อมูลลูกค้ากลับมา เว็บตัวเองไม่มีคนเดินผ่านฟรี แต่ลูกค้าที่มาเป็นของคุณ ส่วนใหญ่ควรทำทั้งสองอย่าง ไม่ใช่เลือกอย่างเดียว</p>
</article>
<article class="study-block">
  <h3>รับชำระเงินออนไลน์ได้เลยไหม?</h3>
  <p>ตัวเว็บและขั้นตอนสั่งซื้อรวมอยู่ในราคา ส่วนการเชื่อมกับผู้ให้บริการรับชำระเงินขึ้นกับว่าคุณเปิดบัญชีกับเจ้าไหนและเอกสารผ่านหรือยัง ซึ่งเป็นขั้นตอนของทางร้านกับผู้ให้บริการ ผมช่วยเชื่อมให้หลังจากนั้น</p>
</article>
<article class="study-block">
  <h3>มีสินค้า 200 รายการ ทำไหวไหม?</h3>
  <p>ไหว แต่ต้องคุยกันก่อนว่าจะจัดการสินค้ายังไง เพราะการกรอกสินค้า 200 รายการเป็นงานจริงที่กินเวลา ราคาเริ่มต้นครอบคลุมโครงสร้างเว็บ ส่วนการนำเข้าสินค้าจำนวนมากคิดแยกตามปริมาณ</p>
</article>
<article class="study-block">
  <h3>ทำแล้วขายดีขึ้นเลยไหม?</h3>
  <p>เว็บทำให้คนที่ตั้งใจซื้ออยู่แล้วซื้อจบง่ายขึ้น และทำให้แบรนด์ดูน่าเชื่อถือขึ้น แต่ไม่ได้พาคนใหม่เข้ามาเองโดยอัตโนมัติ ยอดที่เพิ่มมาจากการที่คุณเอาลิงก์นี้ไปใช้ในโฆษณา โซเชียล และการค้นหา ผมพูดตรงดีกว่าให้ความหวังผิด</p>
</article>
```

- [ ] **Step 2: Run Recipe D, Recipe C for `web-shop`, and Recipe B for `web-shop.html`**

Expected as in Task 3.

- [ ] **Step 3: Confirm every internal link resolves**

```bash
grep -oE 'href="[a-z0-9-]+\.html"' web-shop.html | sed 's/href="//;s/"//' | sort -u | while read f; do
  [ -f "$f" ] && echo "OK   $f" || echo "DEAD $f"
done
```
Expected: no `DEAD` rows.

- [ ] **Step 4: Commit**

```bash
git add web-shop.html
git commit -m "feat: add the online-store industry landing page

Sells the ฿9,900 Business Website package and copies its feature bullets
verbatim from the existing category page rather than rewriting them.

The marketplace FAQ concedes that Shopee and Lazada genuinely bring foot
traffic and recommends doing both, and the last FAQ says outright that a
site does not increase sales on its own. Both are more useful to a real
buyer than a pitch, and neither is something the work can deliver."
```

---

## Task 7: Build `web-gym.html`

**Files:**
- Create: `web-gym.html`

**Interfaces:**
- Consumes: the Shared Industry Page Template.
- Produces: `web-gym.html`. Linked by Task 10, sitemapped by Task 12.

Only one demo backs this page. Its weight comes from the feature and FAQ blocks, not from demo count.

- [ ] **Step 1: Create the file from the Shared Industry Page Template with these values**

| Placeholder | Value |
|---|---|
| `{{SLUG}}` | `web-gym` |
| `{{TITLE}}` | `รับทำเว็บฟิตเนส และยิม เริ่มต้น ฿3,900 \| Phakin Chawanpunya` |
| `{{META_DESC}}` | `รับทำเว็บไซต์ฟิตเนสและยิม เริ่มต้น 3,900 บาท มีตารางคลาส แพ็กเกจสมาชิก โปรไฟล์เทรนเนอร์ และปุ่มทดลองเล่นฟรี ดูตัวอย่างเว็บยิมจริง` |
| `{{NAV_LABEL}}` | `ฟิตเนส` |
| `{{H1_SHORT}}` | `รับทำเว็บฟิตเนส` |
| `{{H1}}` | `รับทำเว็บฟิตเนส และยิม` |
| `{{HERO_COPY}}` | `คนที่กำลังหายิมเปรียบเทียบอยู่ 2-3 ที่พร้อมกัน และตัดสินจากสามอย่าง — ราคาต่อเดือนเท่าไหร่ มีคลาสอะไรเวลาไหน และลองก่อนได้ไหม ยิมที่ตอบสามข้อนี้ในหน้าเดียวได้เปรียบทันที` |
| `{{PRICE}}` | `฿3,900` |
| `{{TIMELINE}}` | `5-7 วัน` |
| `{{REVISIONS}}` | `2 รอบ + ฟรีแก้บั๊ก 3 เดือน` |
| `{{BEST_FOR}}` | `ยิมที่อยากให้คนเห็นราคาและตารางคลาสก่อนเดินเข้ามา` |
| `{{FEATURES_H2}}` | `สิ่งที่เว็บยิมควรมี` |
| `{{WHO_H2}}` | `เหมาะกับยิมแบบไหน` |
| `{{RELATED_H2}}` | `ตัวอย่างเว็บยิมที่เคยทำ` |
| `{{CTA_H2}}` | `อยากได้เว็บยิมแบบนี้บ้าง?` |

`{{FEATURE_ITEMS}}`:

```html
<li>ตารางคลาสรายสัปดาห์ ดูจบในหน้าเดียว ไม่ต้องดาวน์โหลดไฟล์</li>
<li>แพ็กเกจสมาชิกวางเทียบกัน ราคาชัด ไม่ต้องทักไปถาม</li>
<li>โปรไฟล์เทรนเนอร์ พร้อมความถนัดและใบรับรอง</li>
<li>ปุ่มจองคลาสทดลองหรือทักไลน์ ติดอยู่ตลอดการเลื่อน</li>
<li>ภาพอุปกรณ์และพื้นที่จริง เพราะคนอยากเห็นก่อนว่าที่นี่แน่นไหม</li>
<li>เวลาเปิด-ปิด และแผนที่ สำหรับคนที่หายิมใกล้บ้านหรือใกล้ที่ทำงาน</li>
```

`{{WHO_COPY}}`:

```html
เหมาะกับยิม ฟิตเนส สตูดิโอโยคะ มวย และคลาสออกกำลังกายที่ขายเป็นแพ็กเกจรายเดือนหรือรายคอร์ส โดยเฉพาะที่ที่ตอนนี้ยังต้องตอบคำถามเรื่องราคาและตารางคลาสในแชททุกวัน
```

`{{PROJECT_LINKS}}`:

```html
<a class="project-link" href="showcase-iron-republic.html">
  <strong>Iron Republic</strong>
  <span>ยิมสายเวทเทรนนิ่ง ธีมเข้ม เน้นความจริงจังของสถานที่และอุปกรณ์</span>
</a>
```

`{{FAQ_BLOCKS}}`:

```html
<article class="study-block">
  <h3>ควรลงราคาแพ็กเกจบนเว็บเลยไหม?</h3>
  <p>ควร คนที่ต้องทักมาถามราคาก่อนส่วนใหญ่จะไม่ทัก แล้วไปดูที่อื่นที่บอกราคาแทน ถ้ากังวลเรื่องคู่แข่งเห็น ให้ลงเป็นช่วงราคาหรือราคาเริ่มต้นก็ยังดีกว่าไม่ลงเลย</p>
</article>
<article class="study-block">
  <h3>ตารางคลาสเปลี่ยนทุกเดือน จัดการยังไง?</h3>
  <p>ถ้าเปลี่ยนบ่อย ควรบอกตั้งแต่ต้นเพื่อผมวางโครงให้แก้ง่าย หรือทำเป็นลิงก์ไปยังตารางที่คุณอัปเดตเองอยู่แล้ว การฝังตารางแบบตายตัวแล้วต้องเรียกช่างทุกเดือนไม่คุ้มกับใครเลย</p>
</article>
<article class="study-block">
  <h3>อยากให้สมัครสมาชิกและจ่ายเงินผ่านเว็บได้</h3>
  <p>นั่นเป็นระบบสมาชิกซึ่งใหญ่กว่าหน้าเว็บยิม ต้องมีการเก็บข้อมูล ต่ออายุ และรับชำระเงิน คุยรายละเอียดก่อนแล้วผมประเมินให้ ส่วนแพ็กเกจ ฿3,900 คือเว็บที่พาคนเดินเข้ามาสมัครที่ยิม</p>
</article>
<article class="study-block">
  <h3>มีตัวอย่างเว็บยิมแค่อันเดียว พอไหม?</h3>
  <p>ตรงไปตรงมา — ผลงานสายยิมของผมมีชิ้นเดียวคือ Iron Republic แต่โครงสร้างของเว็บยิมใกล้เคียงกับเว็บคลินิกและร้านอาหารมาก คือหน้าบริการ ราคา ทีมงาน และช่องทางติดต่อ ซึ่งผมมีตัวอย่างเยอะกว่า ดูรวมได้ที่หน้าผลงาน</p>
</article>
```

- [ ] **Step 2: Run Recipe D, Recipe C for `web-gym`, and Recipe B for `web-gym.html`**

Expected as in Task 3.

- [ ] **Step 3: Confirm every internal link resolves**

```bash
grep -oE 'href="[a-z0-9-]+\.html"' web-gym.html | sed 's/href="//;s/"//' | sort -u | while read f; do
  [ -f "$f" ] && echo "OK   $f" || echo "DEAD $f"
done
```
Expected: no `DEAD` rows.

- [ ] **Step 4: Commit**

```bash
git add web-gym.html
git commit -m "feat: add the gym and fitness industry landing page

One demo backs this page, so the weight sits in the feature and FAQ
blocks instead. The last FAQ says so directly rather than padding the
project strip — a visitor can count to one, and pretending otherwise
costs more trust than it buys.

The pricing FAQ argues for publishing package prices, which is the
question gym owners actually hesitate on."
```

---

## Task 8: Build `web-construction.html`

**Files:**
- Create: `web-construction.html`

**Interfaces:**
- Consumes: the Shared Industry Page Template.
- Produces: `web-construction.html`. Linked by Task 10, sitemapped by Task 12.

- [ ] **Step 1: Create the file from the Shared Industry Page Template with these values**

| Placeholder | Value |
|---|---|
| `{{SLUG}}` | `web-construction` |
| `{{TITLE}}` | `รับทำเว็บบริษัทก่อสร้าง และรับเหมา เริ่มต้น ฿3,900 \| Phakin Chawanpunya` |
| `{{META_DESC}}` | `รับทำเว็บไซต์บริษัทก่อสร้างและผู้รับเหมา เริ่มต้น 3,900 บาท มีแกลเลอรีผลงาน ขอบเขตบริการ และฟอร์มขอใบเสนอราคา ดูตัวอย่างเว็บก่อสร้างจริง` |
| `{{NAV_LABEL}}` | `ก่อสร้าง` |
| `{{H1_SHORT}}` | `รับทำเว็บบริษัทก่อสร้าง` |
| `{{H1}}` | `รับทำเว็บบริษัทก่อสร้าง และรับเหมา` |
| `{{HERO_COPY}}` | `งานก่อสร้างมูลค่าสูง คนจ้างจึงเช็กก่อนเสมอว่าคุณเคยทำอะไรมาแล้วบ้าง เว็บที่มีแกลเลอรีผลงานจริงและขอบเขตงานชัดเจน ทำให้คุณผ่านด่านนั้นก่อนจะได้คุยกันด้วยซ้ำ` |
| `{{PRICE}}` | `฿3,900` |
| `{{TIMELINE}}` | `5-7 วัน` |
| `{{REVISIONS}}` | `2 รอบ + ฟรีแก้บั๊ก 3 เดือน` |
| `{{BEST_FOR}}` | `ผู้รับเหมาที่มีผลงานแล้วแต่ยังไม่มีที่โชว์` |
| `{{FEATURES_H2}}` | `สิ่งที่เว็บบริษัทก่อสร้างควรมี` |
| `{{WHO_H2}}` | `เหมาะกับใคร` |
| `{{RELATED_H2}}` | `ตัวอย่างเว็บก่อสร้างที่เคยทำ` |
| `{{CTA_H2}}` | `อยากมีที่โชว์ผลงานเป็นเรื่องเป็นราวไหม?` |

`{{FEATURE_ITEMS}}`:

```html
<li>แกลเลอรีผลงาน แยกตามประเภทงาน พร้อมขนาดและระยะเวลาที่ใช้</li>
<li>ขอบเขตบริการชัดเจน รับงานแบบไหน ไม่รับแบบไหน</li>
<li>ฟอร์มขอใบเสนอราคา ถามเฉพาะข้อมูลที่ประเมินงานได้จริง</li>
<li>ขั้นตอนการทำงาน ตั้งแต่ประเมินหน้างานจนส่งมอบ</li>
<li>ข้อมูลบริษัท ทะเบียน และใบอนุญาต สำหรับลูกค้าองค์กร</li>
<li>รองรับการค้นหาแบบ "รับเหมา + ชื่อจังหวัด" ที่คนใช้จริง</li>
```

`{{WHO_COPY}}`:

```html
เหมาะกับผู้รับเหมา บริษัทก่อสร้าง งานตกแต่งภายใน และงานระบบ ที่ทำงานมาแล้วหลายโครงการแต่ผลงานยังกระจายอยู่ในไลน์กับอัลบั้มรูปในมือถือ ทำให้ต้องส่งรูปทีละชุดทุกครั้งที่มีคนถาม
```

`{{PROJECT_LINKS}}`:

```html
<a class="project-link" href="showcase-buildnest.html">
  <strong>BuildNest Construction</strong>
  <span>เว็บบริษัทก่อสร้าง ออกแบบเป็นภาษาไทยตั้งแต่ต้น โครงสร้างบริการครบวงจร</span>
</a>
```

`{{FAQ_BLOCKS}}`:

```html
<article class="study-block">
  <h3>ผลงานเก่าไม่ได้ถ่ายรูปไว้ดี ๆ ทำยังไง?</h3>
  <p>ใช้เท่าที่มีได้ รูปหน้างานจากมือถือใช้ได้จริงถ้าจัดวางดี ๆ และสำหรับงานก่อสร้าง รูปก่อน-หลังของงานเดียวมีน้ำหนักกว่ารูปสวยแยกชิ้นสิบรูป จากนี้ไปถ่ายเก็บทุกงานไว้ตั้งแต่วันแรก</p>
</article>
<article class="study-block">
  <h3>ควรลงราคาบนเว็บไหม?</h3>
  <p>งานก่อสร้างประเมินราคาตายตัวไม่ได้ ผมแนะนำให้ลงเป็นช่วงราคาต่อตารางเมตรหรือราคาเริ่มต้นของงานแต่ละประเภทแทน เพื่อคัดคนที่งบไม่ตรงออกก่อน จะได้ไม่เสียเวลาทั้งสองฝ่าย</p>
</article>
<article class="study-block">
  <h3>ลูกค้าองค์กรจะเชื่อถือได้ยังไง?</h3>
  <p>ใส่เลขทะเบียนนิติบุคคล ใบอนุญาตที่มี และรายชื่อโครงการที่เคยทำพร้อมปี ถ้าเคยทำงานให้หน่วยงานราชการหรือบริษัทใหญ่ ระบุไว้ให้ชัด ข้อมูลพวกนี้คือสิ่งที่ฝ่ายจัดซื้อมองหาเป็นอย่างแรก</p>
</article>
<article class="study-block">
  <h3>ทำเว็บแล้วจะได้งานเพิ่มไหม?</h3>
  <p>เว็บช่วยตอนที่คนกำลังตัดสินใจว่าจะเลือกคุณหรือเจ้าอื่น มันปิดดีลที่ใกล้ปิดอยู่แล้วได้ดีขึ้น แต่ไม่ได้พาคนใหม่มาเองถ้าไม่มีใครรู้จักลิงก์นี้ ส่วนใหญ่ที่ได้ผลคือเอาลิงก์ไปแนบตอนเสนอราคาและใส่ในนามบัตร</p>
</article>
```

- [ ] **Step 2: Run Recipe D, Recipe C for `web-construction`, and Recipe B for `web-construction.html`**

Expected as in Task 3.

- [ ] **Step 3: Confirm every internal link resolves**

```bash
grep -oE 'href="[a-z0-9-]+\.html"' web-construction.html | sed 's/href="//;s/"//' | sort -u | while read f; do
  [ -f "$f" ] && echo "OK   $f" || echo "DEAD $f"
done
```
Expected: no `DEAD` rows.

- [ ] **Step 4: Commit**

```bash
git add web-construction.html
git commit -m "feat: add the construction and contractor industry landing page

Leads on the portfolio gallery and quote request, which is what actually
gets a contractor shortlisted on high-value work.

The photography FAQ tells contractors to use the phone photos they
already have rather than waiting for a shoot, and the last FAQ says the
site closes deals already in motion rather than generating new ones."
```

---

## Task 9: Build `web-solar.html`

**Files:**
- Create: `web-solar.html`

**Interfaces:**
- Consumes: the Shared Industry Page Template.
- Produces: `web-solar.html`. This is the last of the seven; Task 10 links to all of them.

- [ ] **Step 1: Create the file from the Shared Industry Page Template with these values**

| Placeholder | Value |
|---|---|
| `{{SLUG}}` | `web-solar` |
| `{{TITLE}}` | `รับทำเว็บโซลาร์เซลล์ และพลังงาน เริ่มต้น ฿3,900 \| Phakin Chawanpunya` |
| `{{META_DESC}}` | `รับทำเว็บไซต์ธุรกิจโซลาร์เซลล์และพลังงานสะอาด เริ่มต้น 3,900 บาท มีตัวช่วยประเมินค่าไฟที่ประหยัดได้ แพ็กเกจอุปกรณ์ และขั้นตอนติดตั้ง` |
| `{{NAV_LABEL}}` | `โซลาร์เซลล์` |
| `{{H1_SHORT}}` | `รับทำเว็บโซลาร์เซลล์` |
| `{{H1}}` | `รับทำเว็บโซลาร์เซลล์ และพลังงานสะอาด` |
| `{{HERO_COPY}}` | `ลูกค้าโซลาร์ตัดสินใจด้วยตัวเลขเดียว — ลงทุนเท่าไหร่แล้วคืนทุนกี่ปี เว็บที่ให้เขาลองคำนวณจากบิลค่าไฟตัวเองได้ทันที เปลี่ยนคนที่แค่สนใจให้กลายเป็นคนที่อยากคุยต่อ` |
| `{{PRICE}}` | `฿3,900` |
| `{{TIMELINE}}` | `5-7 วัน` |
| `{{REVISIONS}}` | `2 รอบ + ฟรีแก้บั๊ก 3 เดือน` |
| `{{BEST_FOR}}` | `ผู้ติดตั้งโซลาร์ที่อยากคัดลูกค้าก่อนออกไปดูหน้างาน` |
| `{{FEATURES_H2}}` | `สิ่งที่เว็บธุรกิจโซลาร์ควรมี` |
| `{{WHO_H2}}` | `เหมาะกับใคร` |
| `{{RELATED_H2}}` | `ตัวอย่างเว็บโซลาร์ที่เคยทำ` |
| `{{CTA_H2}}` | `อยากได้เว็บโซลาร์แบบนี้บ้างไหม?` |

`{{FEATURE_ITEMS}}`:

```html
<li>ตัวช่วยประเมินจากบิลค่าไฟ บอกขนาดระบบและค่าไฟที่ลดได้คร่าว ๆ</li>
<li>แพ็กเกจอุปกรณ์วางเทียบกัน แผง อินเวอร์เตอร์ และการรับประกัน</li>
<li>ขั้นตอนติดตั้ง ตั้งแต่สำรวจหลังคาจนขออนุญาตและจ่ายไฟ</li>
<li>ผลงานติดตั้งจริง พร้อมขนาดระบบและประเภทหลังคา</li>
<li>ฟอร์มขอประเมินหน้างาน ถามเฉพาะข้อมูลที่ใช้ประเมินได้จริง</li>
<li>คำถามที่พบบ่อยเรื่องการคืนทุนและการดูแลรักษา</li>
```

`{{WHO_COPY}}`:

```html
เหมาะกับผู้จำหน่ายและติดตั้งโซลาร์เซลล์สำหรับบ้านและโรงงาน โดยเฉพาะทีมที่เสียเวลาไปกับการออกไปสำรวจหน้างานให้คนที่สุดท้ายแล้วงบไม่ถึง — ตัวช่วยประเมินบนเว็บคัดกรองตรงนั้นให้ก่อน
```

`{{PROJECT_LINKS}}`:

```html
<a class="project-link" href="showcase-solarpeak.html">
  <strong>SolarPeak</strong>
  <span>เว็บธุรกิจโซลาร์เซลล์ นำเสนอแพ็กเกจและประโยชน์ของการลงทุนอย่างเป็นขั้นตอน</span>
</a>
```

`{{FAQ_BLOCKS}}`:

```html
<article class="study-block">
  <h3>ตัวคำนวณค่าไฟรวมอยู่ในราคาไหม?</h3>
  <p>ตัวประเมินแบบง่ายที่รับค่าไฟต่อเดือนแล้วบอกขนาดระบบและช่วงราคาโดยประมาณ รวมอยู่ในแพ็กเกจได้ ถ้าต้องการตัวคำนวณที่ละเอียดถึงระดับทิศหลังคา องศา และชั่วโมงแดดรายพื้นที่ เป็นงานเพิ่มที่คิดแยก</p>
</article>
<article class="study-block">
  <h3>ตัวเลขที่คำนวณออกมาต้องแม่นแค่ไหน?</h3>
  <p>ควรระบุให้ชัดบนเว็บว่าเป็นการประเมินเบื้องต้น ไม่ใช่ใบเสนอราคา ตัวเลขที่ให้ความหวังเกินจริงจะย้อนกลับมาเป็นปัญหาตอนสำรวจหน้างาน ผมเขียนข้อความกำกับตรงนี้ให้ด้วย</p>
</article>
<article class="study-block">
  <h3>ต้องเตรียมข้อมูลอะไรบ้าง?</h3>
  <p>รายการแพ็กเกจพร้อมยี่ห้อแผงและอินเวอร์เตอร์ เงื่อนไขการรับประกัน ขั้นตอนการติดตั้งของทีมคุณ และรูปงานที่เคยติดตั้ง ถ้ามีตัวเลขการประหยัดจริงจากลูกค้าเก่า ใส่ได้จะช่วยมาก</p>
</article>
<article class="study-block">
  <h3>รับทำเว็บดูข้อมูลการผลิตไฟแบบเรียลไทม์ไหม?</h3>
  <p>การดึงข้อมูลจากอินเวอร์เตอร์มาแสดงผลเป็นงานระบบ ไม่ใช่หน้าเว็บ ต้องดูก่อนว่าอุปกรณ์ที่คุณใช้เปิด API ให้ไหม คุยรายละเอียดก่อนแล้วผมประเมินให้ ส่วนหน้าจอแสดงผลอยู่ในกลุ่มแดชบอร์ด เริ่มที่ ฿7,900</p>
</article>
```

- [ ] **Step 2: Run Recipe D**

This is the first point where all seven pages exist. Expected: all seven rows show `hreflang:0 canonical:1 analytics:1 lang:<html lang="th"> robots:1`.

- [ ] **Step 3: Run Recipe C for all seven pages at once**

Set `pages` to `['web-clinic','web-booking','web-restaurant','web-shop','web-gym','web-construction','web-solar']`.

Expected every row: `vw: 375`, `canScrollX: false`, `overflowing: []`.

- [ ] **Step 4: Run Recipe B for `web-solar.html`**

Expected: accessibility 100, seo 100.

- [ ] **Step 5: Confirm every internal link on all seven pages resolves**

```bash
for p in web-clinic web-booking web-restaurant web-shop web-gym web-construction web-solar; do
  grep -oE 'href="[a-z0-9-]+\.html"' $p.html | sed 's/href="//;s/"//' | sort -u | while read f; do
    [ -f "$f" ] || echo "DEAD in $p: $f"
  done
done; echo "link check done"
```
Expected: no `DEAD` rows.

- [ ] **Step 6: Commit**

```bash
git add web-solar.html
git commit -m "feat: add the solar industry landing page

Leads on the payback calculator, which is the one number solar buyers
decide on, and positions it as lead qualification — the installer stops
driving out to survey roofs for people whose budget was never close.

The accuracy FAQ insists the estimate be labelled an estimate rather than
a quote. An optimistic number that collapses at the site survey costs the
installer the deal and the trust.

Completes the seven industry pages."
```

---

## Task 10: Add the need-selector section to the homepage

**Files:**
- Modify: `index.html` — insert a new `<section>` between the hero (`</section>` at ~line 1582) and the tech stack section (`<section class="stack-sec"` at ~line 1587); add CSS to the `<style>` block
- Modify: `index-en.html` — same, with English chrome

**Interfaces:**
- Consumes: all seven `web-*.html` pages from Tasks 3-9. **Do not start this task until they all exist** — `main` auto-deploys and this section would ship seven dead links.

This is the highest-value change in the plan. It sits directly under the hero and converts a browsing visitor into a self-qualified one in a single click.

- [ ] **Step 1: Write the check that currently fails**

Run Recipe A, open `http://localhost:8123/index.html`, then:

```js
(() => {
  const tiles = [...document.querySelectorAll('.need-tile')];
  return {
    count: tiles.length,
    dead: tiles.map(t => t.getAttribute('href')).filter(h => h && h !== '#contact' && !h.startsWith('web-'))
  };
})()
```

- [ ] **Step 2: Run it and confirm it fails**

Expected right now: `{ count: 0, dead: [] }`.

- [ ] **Step 3: Add the CSS to the `<style>` block in `index.html`**

```css
.need-sub{margin:0 0 1.8rem;color:var(--muted);max-width:52ch;}
.need-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:.9rem;}
.need-tile{display:flex;flex-direction:column;gap:.45rem;padding:1.1rem 1rem;border:1px solid var(--border);border-radius:var(--r);background:var(--surface);text-decoration:none;color:inherit;transition:border-color .18s var(--ease),transform .18s var(--ease);}
.need-tile:hover{border-color:var(--accent);transform:translateY(-2px);}
.need-tile:focus-visible{outline:2px solid var(--accent);outline-offset:3px;}
.need-tile svg{width:26px;height:26px;stroke:var(--accent-text);fill:none;stroke-width:1.7;stroke-linecap:round;stroke-linejoin:round;}
.need-tile strong{font-size:1rem;line-height:1.35;color:var(--ink);}
.need-tile span{font-size:.86rem;color:var(--muted);line-height:1.45;}
@media (max-width:900px){.need-grid{grid-template-columns:repeat(2,1fr);}}
@media (prefers-reduced-motion:reduce){.need-tile{transition:none;}.need-tile:hover{transform:none;}}
```

Two columns below 900px gives the 4×2 desktop / 2×4 mobile layout from the spec. `--r` and `--ease` are the site's existing radius and easing tokens — do not hard-code replacements. Icon strokes use `--accent-text`, which is the accent tuned for dark backgrounds.

- [ ] **Step 4: Add the section markup to `index.html`**

Insert immediately after the hero's closing `</section>`:

```html
    <!-- =============================================
         NEED SELECTOR
    ============================================= -->
    <section class="section" id="need" lang="th" aria-labelledby="need-heading">
      <div class="container">
        <span class="section-label">เริ่มตรงนี้</span>
        <h2 class="section-title" id="need-heading">คุณต้องการเว็บแบบไหน?</h2>
        <p class="need-sub">เลือกประเภทที่ใกล้เคียง — พาไปดูผลงานจริงและราคาของหมวดนั้นทันที</p>
        <div class="need-grid">
          <a class="need-tile" href="web-clinic.html">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 7v10M7 12h10"/><rect x="3" y="3" width="18" height="18" rx="4"/></svg>
            <strong>คลินิก / ความงาม</strong>
            <span>จองคิว บริการ ทีมแพทย์</span>
          </a>
          <a class="need-tile" href="web-booking.html">
            <svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="3"/><path d="M8 3v4M16 3v4M3 11h18"/></svg>
            <strong>จองคิว / นัดหมาย</strong>
            <span>ปฏิทินว่าง กันคิวชน</span>
          </a>
          <a class="need-tile" href="web-restaurant.html">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3v8a3 3 0 0 0 6 0V3M9 11v10M18 3c-1.5 2-2 4-2 6h4c0-2-.5-4-2-6zM18 9v12"/></svg>
            <strong>ร้านอาหาร / คาเฟ่</strong>
            <span>เมนู ราคา จองโต๊ะ</span>
          </a>
          <a class="need-tile" href="web-shop.html">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 6h18l-1.6 11.2A2 2 0 0 1 17.4 19H6.6a2 2 0 0 1-2-1.8L3 6zM8 10a4 4 0 0 0 8 0"/></svg>
            <strong>ขายของออนไลน์</strong>
            <span>สินค้า ตะกร้า ชำระเงิน</span>
          </a>
          <a class="need-tile" href="web-gym.html">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9v6M8 7v10M16 7v10M20 9v6M8 12h8"/></svg>
            <strong>ฟิตเนส / ยิม</strong>
            <span>ตารางคลาส แพ็กเกจสมาชิก</span>
          </a>
          <a class="need-tile" href="web-construction.html">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 21h18M5 21V10l7-5 7 5v11M10 21v-6h4v6"/></svg>
            <strong>ก่อสร้าง / รับเหมา</strong>
            <span>ผลงาน ขอใบเสนอราคา</span>
          </a>
          <a class="need-tile" href="web-solar.html">
            <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M19.1 4.9L17 7M7 17l-2.1 2.1"/></svg>
            <strong>โซลาร์ / พลังงาน</strong>
            <span>ประเมินค่าไฟ แพ็กเกจ</span>
          </a>
          <a class="need-tile" href="#contact">
            <svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 15a2 2 0 0 1-2 2H8l-5 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/></svg>
            <strong>ไม่แน่ใจ</strong>
            <span>เล่าโจทย์มา ผมช่วยดูให้</span>
          </a>
        </div>
      </div>
    </section>
```

Every `<svg>` is `aria-hidden="true"` — the tile's `<strong>` already names it, so announcing the icon would just repeat.

- [ ] **Step 5: Run the Step 1 check again**

Expected: `{ count: 8, dead: [] }`.

- [ ] **Step 6: Confirm all eight destinations resolve**

```bash
for f in web-clinic web-booking web-restaurant web-shop web-gym web-construction web-solar; do
  [ -f "$f.html" ] && echo "OK   $f.html" || echo "DEAD $f.html"
done
grep -c 'id="contact"' index.html
```
Expected: seven `OK` rows and `1`.

- [ ] **Step 7: Mirror Steps 3-4 into `index-en.html`**

Same CSS, same markup, same seven `web-*.html` destinations — those pages are Thai-only and both languages link to them, exactly as both languages link to the 13 demo pages. Only the surrounding chrome is English:

```html
        <span class="section-label">Start here</span>
        <h2 class="section-title" id="need-heading">What kind of site do you need?</h2>
        <p class="need-sub">Pick the closest match — you'll see real work and pricing for that category.</p>
```

Tile labels in `index-en.html`:

| `href` | `<strong>` | `<span>` |
|---|---|---|
| `web-clinic.html` | `Clinic / Beauty` | `Booking, services, practitioners` |
| `web-booking.html` | `Booking / Appointments` | `Live availability, no double-booking` |
| `web-restaurant.html` | `Restaurant / Café` | `Menu, pricing, reservations` |
| `web-shop.html` | `Online Store` | `Products, cart, checkout` |
| `web-gym.html` | `Fitness / Gym` | `Class timetable, memberships` |
| `web-construction.html` | `Construction` | `Portfolio, quote requests` |
| `web-solar.html` | `Solar / Energy` | `Savings estimate, packages` |
| `#contact` | `Not sure yet` | `Tell me the problem, I'll help` |

Keep `lang="th"` **off** this section in `index-en.html` — the chrome is English here. The destination pages carry their own `lang="th"`.

- [ ] **Step 8: Run the Step 1 check against `index-en.html`**

Expected: `{ count: 8, dead: [] }`.

- [ ] **Step 9: Run Recipe C for `index` and `index-en`**

The 4-column grid at 375px is the risk here.

Expected: `vw: 375`, `canScrollX: false`, `overflowing: []`.

- [ ] **Step 10: Run Recipe B for `index.html` and `index-en.html`**

Expected: accessibility 100, seo 100 on both. Heading order matters — the new `<h2>` must not skip a level after the hero's `<h1>`.

- [ ] **Step 11: Commit**

```bash
git add index.html index-en.html
git commit -m "feat: add the need selector under the hero

The highest-leverage change in this plan. A visitor who knows their
industry now reaches a page about it in one click, instead of scrolling a
project grid and inferring whether their business is covered.

Eight tiles, 4x2 desktop and 2x4 mobile. The eighth is 'ไม่แน่ใจ' pointing
at contact — without it, anyone outside the seven industries reads the
grid as 'he does not do my kind of business'.

Icons are inline SVG rather than emoji: emoji render inconsistently
across platforms and screen readers announce them unpredictably. All are
aria-hidden since the tile text already names each one.

Both languages link to the same Thai industry pages, exactly as both link
to the same 13 demo pages."
```

---

## Task 11: Add the pricing section to the homepage

**Files:**
- Modify: `index.html` — insert a new `<section>` immediately after the services section closes (`</section>` at ~line 1728, before `<section class="section" id="testimonials"`); add CSS to the `<style>` block
- Modify: `index-en.html` — same

**Interfaces:**
- Consumes: nothing from earlier tasks. Links to the three existing category pages, which already exist on `main`.

Placing this between services and testimonials puts the real 5★ reviews directly after the price, which is where the objection lands.

- [ ] **Step 1: Add the CSS to the `<style>` block in `index.html`**

```css
.pricing-sub{margin:0 0 1.6rem;color:var(--muted);max-width:60ch;}
.pricing-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:1rem;}
.price-col{display:flex;flex-direction:column;padding:1.4rem;border:1px solid var(--border);border-radius:var(--r);background:var(--surface);box-shadow:var(--sh-sm);}
.price-col.is-mid{border-color:var(--accent);}
.price-col h3{margin:0 0 .3rem;font-size:1.05rem;color:var(--ink);}
.price-amt{font-size:1.9rem;font-weight:800;letter-spacing:-.02em;margin:.2rem 0 .1rem;color:var(--ink);}
.price-meta{font-size:.86rem;color:var(--muted);margin:0 0 1rem;}
.price-col ul{list-style:none;margin:0 0 1.2rem;padding:0;display:flex;flex-direction:column;gap:.5rem;font-size:.9rem;line-height:1.5;color:var(--ink-2);}
.price-col ul li{padding-left:1.3rem;position:relative;}
.price-col ul li::before{content:"";position:absolute;left:0;top:.5em;width:.5rem;height:.5rem;border-radius:50%;background:var(--accent-text);}
.price-col .btn-project{margin-top:auto;text-align:center;}
@media (max-width:900px){.pricing-grid{grid-template-columns:1fr;}}
```

`.price-col` deliberately mirrors the existing `.card` rule (`--surface` background, `--border` border, `var(--r)` radius, `var(--sh-sm)` shadow) so the pricing columns read as the same component family as the services cards directly above them.

- [ ] **Step 2: Add the section markup to `index.html`**

```html
    <!-- =============================================
         PRICING
    ============================================= -->
    <section class="section" id="pricing" lang="th" aria-labelledby="pricing-heading">
      <div class="container">
        <span class="section-label">ราคา</span>
        <h2 class="section-title" id="pricing-heading">ราคาแพ็กเกจ</h2>
        <p class="pricing-sub">ราคาเริ่มต้นจริงจาก Fastwork ไม่มีค่าใช้จ่ายแอบแฝง งานที่ซับซ้อนกว่านี้ประเมินให้ก่อนเริ่มเสมอ</p>
        <div class="pricing-grid">

          <div class="price-col">
            <h3>Landing Page</h3>
            <div class="price-amt">฿3,900</div>
            <p class="price-meta">5-7 วัน · แก้ไข 2 รอบ + ฟรีแก้บั๊ก 3 เดือน</p>
            <ul>
              <li>เว็บหน้าเดียวจบ พัฒนาใหม่ทั้งหมด ไม่ใช้เทมเพลต</li>
              <li>รองรับมือถือเต็มรูปแบบ</li>
              <li>ฟอร์มติดต่อหรือปุ่มไลน์</li>
            </ul>
            <a class="btn-project" href="landing-page.html">ดูรายละเอียด</a>
          </div>

          <div class="price-col is-mid">
            <h3>Dashboard UI</h3>
            <div class="price-amt">฿7,900</div>
            <p class="price-meta">7-10 วัน · แก้ไข 2 รอบหลังส่งแบบ</p>
            <ul>
              <li>ออกแบบหน้าจอระบบสูงสุด 5 หน้าจอ</li>
              <li>ส่งไฟล์ออกแบบฉบับเต็ม ทีมพัฒนาทำต่อได้ทันที</li>
              <li>เหมาะกับระบบจอง ระบบหลังบ้าน แดชบอร์ด</li>
            </ul>
            <a class="btn-project" href="dashboard-ui.html">ดูรายละเอียด</a>
          </div>

          <div class="price-col">
            <h3>Business Website</h3>
            <div class="price-amt">฿9,900</div>
            <p class="price-meta">10-14 วัน · แก้ไข 2 รอบ + ฟรีแก้บั๊ก 3 เดือน</p>
            <ul>
              <li>เว็บ 3-5 หน้า พร้อมโครงสร้างรองรับ SEO พื้นฐาน</li>
              <li>ฟอร์มติดต่อหรือปุ่ม LINE OA</li>
              <li>เหมาะกับเว็บบริษัทและร้านค้าออนไลน์</li>
            </ul>
            <a class="btn-project" href="business-website.html">ดูรายละเอียด</a>
          </div>

        </div>
      </div>
    </section>
```

There is no existing section-subtitle class on the site — sections currently go straight from `.section-title` to their content — so `.pricing-sub` is defined in Step 1 rather than borrowed.

- [ ] **Step 3: Verify the numbers match the category pages exactly**

```bash
for p in landing-page dashboard-ui business-website; do
  echo "--- $p ---"
  sed -n '/study-meta/,/<\/section>/p' $p.html | grep -oE '>[^<>]{2,60}<' | tr -d '<>' | sed '/^\s*$/d' | head -8
done
grep -oE '฿[0-9,]+|[0-9]+-[0-9]+ วัน|2 รอบ[^<]*' index.html | sort -u
```
Expected: every price, duration and revision string in `index.html` appears identically in the category pages. Any mismatch is a real error — these are live Fastwork listings.

- [ ] **Step 4: Mirror Steps 1-2 into `index-en.html`**

Per the site's bilingual rule, the pricing and feature copy **stays in Thai** on the English page, exactly as `#services` already does. Only the heading and subtitle become English:

```html
        <span class="section-label">Pricing</span>
        <h2 class="section-title" id="pricing-heading">Package pricing</h2>
        <p class="pricing-sub">Real starting prices from Fastwork, no hidden costs. Anything more complex is quoted before work starts.</p>
```

Keep `lang="th"` on the section wrapper in `index-en.html` — the body copy really is Thai, and marking it correctly is what keeps the Accessibility score at 100.

The three `ดูรายละเอียด` links become `landing-page-en.html`, `dashboard-ui-en.html`, `business-website-en.html` and read `View details`.

- [ ] **Step 5: Confirm the English page's links resolve**

```bash
for f in landing-page-en dashboard-ui-en business-website-en; do
  [ -f "$f.html" ] && echo "OK   $f.html" || echo "DEAD $f.html"
done
```
Expected: three `OK` rows.

- [ ] **Step 6: Run Recipe C for `index` and `index-en`**

Expected: `vw: 375`, `canScrollX: false`, `overflowing: []`. The 3-column grid collapsing to 1 column below 900px is what makes this pass.

- [ ] **Step 7: Run Recipe B for `index.html` and `index-en.html`**

Expected: accessibility 100, seo 100 on both.

- [ ] **Step 8: Commit**

```bash
git add index.html index-en.html
git commit -m "feat: add a pricing comparison section to the homepage

Sits between services and testimonials so the three real 5-star Fastwork
reviews land immediately after the price, which is where the objection
is.

Every price, duration and revision string is copied verbatim from the
category pages — they are live Fastwork listings, not marketing copy to
be reworded.

Pricing copy stays Thai on index-en.html, matching the existing #services
rule, with lang=\"th\" on the section so the language is announced
correctly."
```

---

## Task 12: Update `sitemap.xml` and `CLAUDE.md`

**Files:**
- Modify: `sitemap.xml` — add 7 `<url>` entries (59 → 66)
- Modify: `CLAUDE.md` — project structure, the two no-`-en`-twin classes, corrected cards table, new homepage sections

**Interfaces:**
- Consumes: all seven industry pages from Tasks 3-9 and the homepage changes from Tasks 1, 2, 10, 11.

- [ ] **Step 1: Check the current sitemap entry format**

```bash
grep -A4 -m1 '<url>' sitemap.xml
grep -c '<loc>' sitemap.xml
```
Expected: `59`. Match whatever `<lastmod>` / `<changefreq>` / `<priority>` fields the existing entries use — do not invent a different shape.

- [ ] **Step 2: Add the seven URLs to `sitemap.xml`**

Following the existing entry format exactly, add:

```
https://ph-akin.dev/web-clinic.html
https://ph-akin.dev/web-booking.html
https://ph-akin.dev/web-restaurant.html
https://ph-akin.dev/web-shop.html
https://ph-akin.dev/web-gym.html
https://ph-akin.dev/web-construction.html
https://ph-akin.dev/web-solar.html
```

These have no `-en` twin, so no `xhtml:link` alternates — same as the 13 demo pages already in the file.

- [ ] **Step 3: Verify the sitemap**

```bash
python3 -c "
import xml.etree.ElementTree as ET
t = ET.parse('sitemap.xml')
locs = [e.text for e in t.iter('{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
print('total:', len(locs))
print('duplicates:', [u for u in set(locs) if locs.count(u) > 1])
import os
missing = [u for u in locs if not os.path.exists(u.replace('https://ph-akin.dev/','') or 'index.html')]
print('missing files:', missing)
"
```
Expected: `total: 66`, `duplicates: []`, `missing files: []`. The XML parsing succeeding at all also proves the file is still well-formed.

- [ ] **Step 4: Update the bilingual rules in `CLAUDE.md`**

In the "Bilingual structure" section, replace the single demo-page exception note with an explicit statement of **two** classes that have no `-en` twin:

```markdown
**Two page classes have no `-en` twin. Both are deliberate, not unfinished work:**

1. **The 13 project demo pages** (`construction-landing.html`, `gym-landing.html`, …) —
   simulated client work. Both languages link to the same demo file.
2. **The 7 industry landing pages** (`web-clinic.html`, `web-booking.html`,
   `web-restaurant.html`, `web-shop.html`, `web-gym.html`, `web-construction.html`,
   `web-solar.html`) — the search intent (`รับทำเว็บคลินิก`) is Thai-only, so an English
   twin would double the file count for traffic that does not exist. Both languages link
   to the same Thai page, and `index-en.html`'s need selector points at them directly.

Both classes carry: no `hreflang`, a self-referential `canonical`, `robots: index, follow`.
Do not "fix" them by generating `-en` siblings.
```

- [ ] **Step 5: Correct the stale cards table in `CLAUDE.md`**

The "Current Cards in Selected Work" table lists file names that no longer match — card 1 is listed as `construction-landing.html` but the card links to `showcase-buildnest.html`. Replace the whole table with:

| # | Name | Card links to | `data-industry` |
|---|---|---|---|
| 1 | BuildNest Construction | `showcase-buildnest.html` | `construction` |
| 2 | Iron Republic | `showcase-iron-republic.html` | `gym` |
| 3 | NOIR Coffee | `showcase-noir-coffee.html` | `restaurant` |
| 4 | Elevate Commerce | `showcase-elevate-commerce.html` | `shop` |
| 5 | Elasticshop Gaming Top-Up | `showcase-elasticshop-gaming.html` | `shop` |
| 6 | RATRI Restaurant | `showcase-ratri-restaurant.html` | `restaurant` |
| 7 | SolarPeak | `showcase-solarpeak.html` | `solar` |
| 8 | BookEase Dashboard | `showcase-bookease.html` | `booking` |
| 9 | MuseRoom | `showcase-museroom.html` | `other` |
| 10 | LUMI Clinic | `showcase-lumi-clinic.html` | `clinic` |
| 11 | BRIGHT Dental Clinic | `showcase-dental-clinic.html` | `clinic` |
| 12 | VELVÉ Aesthetics | `showcase-velve-aesthetics.html` | `clinic booking` |
| 13 | HabitQuest | external: `https://habitquest-pi.vercel.app/` | `other` |

Verify the `Card links to` column before writing it:

```bash
python3 -c "
import re
h=open('index.html',encoding='utf-8').read()
for m in re.finditer(r'data-industry=\"([^\"]*)\".*?<a class=\"work-thumb\" href=\"([^\"]*)\".*?<div class=\"work-name\">([^<]*)</div>', h, re.S):
    print(f'{m.group(3):<28} {m.group(2):<38} {m.group(1)}')
"
```

- [ ] **Step 6: Add the new sections to the `CLAUDE.md` "Pages & Sections" table**

Add rows for `#need` (the need selector, directly under the hero) and `#pricing` (between Services and Testimonials), and note that `#projects`' filter axis is now industry with an `อื่นๆ` bucket.

- [ ] **Step 7: Add the industry page recipe to "Common Tasks for Claude" in `CLAUDE.md`**

```markdown
### Add an industry landing page
Seven exist (`web-clinic`, `web-booking`, `web-restaurant`, `web-shop`, `web-gym`,
`web-construction`, `web-solar`). They are **Thai-only** — see "Bilingual structure".
Built entirely from `assets/portfolio-pages.css` components, no new CSS:
1. Copy an existing `web-*.html` as the skeleton
2. Hero `.hero.case-hero` + `.study-meta` 4-box strip — price, timeline, revisions, best-for.
   **Prices come verbatim from the category pages**, never invented
3. `.study-grid` with a `.featured` block listing features that industry actually needs,
   plus a plain block answering "who it's for"
4. `.project-strip` of `.project-link`s pointing at matching showcase pages
5. An FAQ `.study-grid` of 4-5 `.study-block`s
6. `.result-band` closing CTA
7. Add a tile to `#need` on **both** `index.html` and `index-en.html`
8. Add the URL to `sitemap.xml` (no `xhtml:link` alternates)
```

- [ ] **Step 8: Commit**

```bash
git add sitemap.xml CLAUDE.md
git commit -m "docs: sitemap the industry pages and document their exception

Adds the 7 industry URLs (59 -> 66), with no xhtml:link alternates since
they have no -en twin.

CLAUDE.md now states the two no--en-twin classes explicitly — demo pages
and industry pages — with the reason and a 'do not fix this' note. Left
implicit, the next session reads seven unpaired files as unfinished work
and generates -en siblings nobody wants.

Also corrects the Selected Work table, which had drifted: card 1 was
listed as construction-landing.html while the card actually links to
showcase-buildnest.html. Adds the data-industry column."
```

---

## Task 13: Full verification pass

**Files:** none modified — this task only runs checks and fixes what they surface.

**Interfaces:**
- Consumes: everything from Tasks 1-12.

Nothing in Tasks 1-12 verified the whole site at once. This task does, and it is where regressions in pages nobody touched get caught.

- [ ] **Step 1: Start the server**

Run Recipe A.

- [ ] **Step 2: Lighthouse mobile on all seven industry pages plus both homepages**

```bash
for p in index index-en web-clinic web-booking web-restaurant web-shop web-gym web-construction web-solar; do
  npx -y lighthouse "http://localhost:8123/$p.html" --quiet --chrome-flags="--headless" \
    --output=json --output-path="/tmp/lh-$p.json" >/dev/null 2>&1
  python3 -c "
import json
d = json.load(open('/tmp/lh-$p.json'))
s = {k: round(v['score']*100) for k,v in d['categories'].items() if v.get('score') is not None}
bp = [r['id'] for r in d['categories']['best-practices']['auditRefs']
      if d['audits'][r['id']].get('score') is not None and d['audits'][r['id']]['score'] < 1]
flag = '' if (s['accessibility'] == 100 and s['seo'] == 100
              and set(bp) <= {'third-party-cookies','inspector-issues'}) else '  <-- FAIL'
print(f\"{'$p':<18} a11y:{s['accessibility']:<4} seo:{s['seo']:<4} bp:{s['best-practices']:<4} {bp}{flag}\")
"
done
```
Expected: no `<-- FAIL` rows. Accessibility and SEO 100 everywhere; Best Practices 77 with only the two Clarity audits.

- [ ] **Step 3: Mobile overflow on all nine pages**

Run Recipe C with `pages` set to `['index','index-en','web-clinic','web-booking','web-restaurant','web-shop','web-gym','web-construction','web-solar']`.

Expected every row: `vw: 375`, `canScrollX: false`, `bw: 375`, `overflowing: []`.

- [ ] **Step 4: Every internal link on the site resolves**

```bash
for f in *.html; do
  grep -oE 'href="[a-zA-Z0-9._-]+\.html"' "$f" | sed 's/href="//;s/"//' | sort -u | while read t; do
    [ -f "$t" ] || echo "DEAD  $f -> $t"
  done
done; echo "link sweep complete"
```
Expected: no `DEAD` rows.

- [ ] **Step 5: Head-tag audit on the industry pages**

Run Recipe D. Expected all seven rows correct.

- [ ] **Step 6: No unsupportable technology claims anywhere**

```bash
grep -rniE '(สร้างด้วย|พัฒนาด้วย|built with|ใช้เทคโนโลยี).{0,60}(React|Node|Express|PostgreSQL)' *.html || echo "no unsupportable stack claims"
grep -rn 'เทคโนโลยีที่เราใช้ในผลงาน' *.html || echo "no inaccurate tech heading"
```
Expected: both fall through to their `echo`. All 12 local demos are plain HTML/CSS/vanilla JS; only the HabitQuest case study names React.

- [ ] **Step 7: Filter still returns 13, not 18**

On `index.html` and `index-en.html`:

```js
(() => {
  document.querySelector('.filter-btn[data-filter="all"]').click();
  const all = [...document.querySelectorAll('.work-card[data-industry]')].filter(c => !('hidden' in c.dataset)).length;
  const clones = document.querySelectorAll('.work-card:not([data-industry])').length;
  return { visibleOnAll: all, carouselClones: clones };
})()
```
Expected: `{ visibleOnAll: 13, carouselClones: 5 }`. If `visibleOnAll` is 18 the carousel fix from Task 1 Step 7 was missed.

- [ ] **Step 8: Fix anything the checks surfaced, then re-run the failing check only**

Do not proceed until every check above passes. If a check cannot be made to pass, stop and report it rather than marking this task done.

- [ ] **Step 9: Stop the server and commit any fixes**

```bash
pkill -f "http.server 8123"
git status --short
```
If Step 8 changed files, commit them with a message naming the specific check that caught the problem. If nothing changed, there is nothing to commit — the plan is done.

---

## Plan Self-Review

**Spec coverage.** Every requirement this plan claims: industry-split pages (D1) → Tasks 3-9; Thai-only with the documented exception (D2) → Tasks 3-9 plus Task 12 Step 4; seven pages covering every demo (D3) → Tasks 3-9; need selector → Task 10; industry filter axis → Task 1; buyer-search-term tags → Task 2; pricing section → Task 11; the `อื่นๆ` bucket for MuseRoom and HabitQuest → Task 1 Step 3.

**Deliberately deferred to plan 2**, all of it dependent on the nav and search: the global nav (D4), site search (D5), the five bilingual funnel pairs, the homepage 11-section reorder (D6), the clickable technology row (D7), and the tag cloud becoming clickable. Verification items 3 (CLS on search pages) and 6 (technology heading) from the spec are partly covered here — Task 13 Step 6 checks the heading claim — and complete in plan 2.

**Type consistency.** `data-industry` is used identically in Tasks 1, 12 and 13. The eight filter keys in Task 1 Step 4 match the eight card values in Step 3 and the seven page slugs in Tasks 3-9. `applyFilter(filter, label)` is defined once in Task 1 Step 8 and called from two places in the same block. `.need-tile` in Task 10's CSS matches the selector in its Step 1 check.

**Known cross-task ordering constraint.** Task 10 must not run before Tasks 3-9 are all committed — `main` auto-deploys and the selector would ship seven dead links. This is stated in Task 10's Interfaces block.
