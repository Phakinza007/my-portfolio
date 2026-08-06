# Multi-Page Nav Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the site from one long homepage plus satellites into a real multi-page site — five new bilingual destination pages behind one consistent navigation bar.

**Architecture:** The homepage's existing `.navbar` CSS is extracted into a shared `assets/site-nav.css`, then the same nav markup ships to all 19 selling pages. Five new bilingual pairs are built from `assets/portfolio-pages.css` components. No framework, no build step, no new dependencies.

**Source spec:** `docs/superpowers/specs/2026-08-06-buyer-funnel-multipage-design.md` — plan 2 of 2. Plan 1 (`2026-08-06-industry-funnel.md`) shipped in `19ab68b`..`0bd8624`.

## What changed since the spec was written

The spec is accurate on intent but stale on three specifics. Do not "restore" these:

1. **The homepage pricing section was removed** after the spec was approved, along with the Formspree contact form. Contact is now Fastwork plus `mailto:`. So `services.html` becomes the **only** place on the site that compares all three packages side by side — that raises its importance, it does not lower it.
2. **The homepage section order changed** to: hero → need selector → reviews → work → about → case studies → services → tech → contact. The spec's 11-section order with pricing at 6 is obsolete.
3. **Site search already shipped** (`0bd8624`) — `assets/search-index.json`, `site-search.css`, `site-search.js`, live in the navbar of `index.html` and `index-en.html` only. This plan spreads it to the other 17 selling pages via the shared nav; it does not rebuild it.

Spec item D7's clickable technology row is still outstanding and is Task 8 here.

## Global Constraints

- **`main` auto-deploys to production.** Every commit must leave the site shippable. Never commit a nav link to a page that does not exist yet — this is why the nav rollout (Task 7) comes after all five pages are built.
- **Quality bars:** Lighthouse mobile Accessibility 100, SEO 100, CLS 0. Best Practices caps at 77 sitewide because Microsoft Clarity sets third-party cookies — `third-party-cookies` and `inspector-issues` are the only two audits allowed to fail.
- **No horizontal overflow at 375×812:** `canScrollX: false`, `body.scrollWidth === documentElement.clientWidth`.
- **`resize_window` silently does nothing in this environment** — it reports success while the viewport stays put. Use the 375×812 iframe recipe and confirm `clientWidth === 375` before believing any result.
- **Two CSS worlds, do not mix them up:**
  - `index.html` / `index-en.html` — inline `<style>`, sections wrap content in `<div class="container">`, headings are `.section-label` + `.section-title`.
  - Everything else — `assets/portfolio-pages.css`, sections wrap content in `<div class="page-shell">`, headings are `.eyebrow` + `<h2>`.
- **Design tokens** (there is no `--card`, `--line` or `--text`): `--bg #0d1117`, `--surface #161b22`, `--surface-2 #1c2128`, `--ink #e6edf3`, `--ink-2 #c9d1d9`, `--muted #8b949e`, `--border #21262d`, `--border-2 #30363d`, `--accent #5274f8`, `--accent-dark #3651d4`, `--accent-light rgba(79,110,247,.14)`, `--accent-text #7c93fb`; radii `--r`/`--r-sm`/`--r-lg`; shadows `--sh`/`--sh-sm`/`--sh-lg`; `--ease`; `--max`.
- **Every new `.html`** carries, immediately before `</head>` and using **relative** paths:
  ```html
  <link rel="stylesheet" href="assets/site-search.css" />
  <script src="assets/site-search.js" defer></script>
  <script src="assets/analytics.js" defer></script>
  ```
- **The five new pairs are bilingual**: `hreflang` trio (`th` → Thai, `en` → `-en`, `x-default` → **Thai**), self-referential `canonical`, `og:locale` `th_TH` / `en_US`.
- **The 7 industry pages stay Thai-only** — no `hreflang`, self canonical. Do not generate `-en` twins.
- **Prices are real Fastwork listings.** Copy verbatim, never reword or invent:
  - Landing Page — `฿3,900` · `5-7 วัน` · `2 รอบ + ฟรีแก้บั๊ก 3 เดือน`
  - Dashboard UI — `฿7,900` · `7-10 วัน` · `2 รอบหลังส่งแบบ`
  - Business Website — `฿9,900` · `10-14 วัน` · `2 รอบ + ฟรีแก้บั๊ก 3 เดือน`
- **No unprovable claims** — no project counts, years of experience, client names, or any statement that the 12 local demos were built with React/Node/Express/PostgreSQL. They are plain HTML/CSS/vanilla JS. Only HabitQuest genuinely uses React and Vite.
- **Fastwork CTA** (verbatim): `https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob` · **Email:** `mailto:a0626568471@gmail.com`

---

## File Structure

**Created (11):**

| File | Responsibility |
|---|---|
| `assets/site-nav.css` | The global navbar, extracted from `index.html`'s inline styles so 19 pages can share one source |
| `work.html` / `work-en.html` | Full archive — 13 project cards, industry filter, tag cloud, 4 case studies |
| `services.html` / `services-en.html` | 3 packages, the price comparison table, entry points to the 7 industry pages |
| `about.html` / `about-en.html` | Bio, experience timeline, tools, KMUTT |
| `faq.html` / `faq-en.html` | Pre-hire questions + `FAQPage` JSON-LD |
| `process.html` / `process-en.html` | Brief → delivery, step by step |

**Modified (21):** `index.html`, `index-en.html`, the 7 `web-*.html`, `sitemap.xml`, `CLAUDE.md`, plus the 10 new files gaining the nav in Task 7.

**Untouched:** the 13 demo pages, the 3 category pages, and the 42 showcase / case-study / resume files — their `.page-shell nav` is contextual (`ดูเว็บจริง` points somewhere different on every page) and replacing it with a generic bar would remove each page's most valuable link.

---

## The global nav

```
┌────────────────────────────────────────────────────────────────────────────┐
│ ◈ Phakin Chawanpunya    หน้าแรก  ผลงาน  บริการ  เกี่ยวกับผม  FAQ            │
│                                        [🔍 ค้นหา…]  [EN]  [ติดต่อ]         │
└────────────────────────────────────────────────────────────────────────────┘
  ≥1181px  full bar
  ≤1180px  links collapse into ☰; search stays in the bar
  ≤768px   search hides from the bar, full-width copy lives in the ☰ panel
```

`process.html` is deliberately **not** a nav item — six links plus a search field plus two controls overflow at 1180px. It is reached from `services.html`, `faq.html` and the footer.

**Two corrections found while reviewing this plan against the code — the naive version would not have worked:**

1. **There is no `.nav-lang` class.** The EN link is currently `<li><a href="index-en.html">EN</a></li>` inside `.nav-links`, with no rule of its own. So it stays an `<li>` in the list — no new class, and it collapses into the hamburger with the other links, which is the behaviour that already ships.
2. **`.container` does not exist in `assets/portfolio-pages.css`** (0 rules — checked). Its only definition is inline in `index.html`: `width: min(var(--max), calc(100% - 40px)); margin: 0 auto;` with `--max: 1100px`. Rather than duplicate a general layout class into a nav stylesheet, `assets/site-nav.css` folds those two declarations into `.nav-inner` itself, and the markup drops `.container` from the nav entirely. That removes the cross-file dependency instead of spreading it.

Markup, identical on all 19 pages (`{{...}}` filled per page):

```html
  <header class="navbar">
    <div class="nav-inner">
      <a class="nav-brand" href="/">
        <img src="assets/favicon.svg" alt="" width="28" height="28" class="nav-logo-mark" />
        Phakin Chawanpunya
      </a>

      <nav aria-label="เมนูหลัก">
        <ul class="nav-links">
          <li><a href="/"{{CUR_HOME}}>หน้าแรก</a></li>
          <li><a href="work.html"{{CUR_WORK}}>ผลงาน</a></li>
          <li><a href="services.html"{{CUR_SERVICES}}>บริการ</a></li>
          <li><a href="about.html"{{CUR_ABOUT}}>เกี่ยวกับผม</a></li>
          <li><a href="faq.html"{{CUR_FAQ}}>FAQ</a></li>
          <li><a href="{{EN_URL}}">EN</a></li>
        </ul>
      </nav>

      <div class="site-search">
        <div class="site-search-field">
          <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.6-3.6"/></svg>
          <input type="search" autocomplete="off" role="combobox" aria-expanded="false"
                 aria-autocomplete="list" aria-label="ค้นหาในเว็บไซต์"
                 placeholder="ค้นหาผลงาน บริการ ราคา…" />
        </div>
        <div class="site-search-panel" role="listbox" aria-label="ผลการค้นหา" hidden></div>
        <p class="site-search-status" role="status" aria-live="polite"></p>
      </div>

      <a class="nav-resume" href="#contact">ติดต่อ</a>

      <button class="nav-toggle" type="button" aria-label="เปิดเมนู" aria-expanded="false" aria-controls="mobile-panel">
        <span></span><span></span><span></span>
      </button>
    </div>

    <nav class="nav-mobile-panel" id="mobile-panel" aria-label="เมนูมือถือ">
      … same search block, then the same five links, then EN and ติดต่อ …
    </nav>
  </header>
```

`{{CUR_*}}` is ` aria-current="page"` on the page's own entry and empty everywhere else — that is how a screen reader user knows where they are.

`{{EN_URL}}` is the page's `-en` twin for the five new pairs and `index-en.html` for the seven Thai-only industry pages, whose EN link therefore goes to the English homepage. That is correct and matches how the demo pages already behave.

The `ติดต่อ` button points at `#contact`, which only exists on the homepage. On every other page it must be `/#contact`.

---

## Verification Recipes

**Recipe A — serve locally**

```bash
pkill -f "http.server 8123" 2>/dev/null
(python3 -m http.server 8123 >/dev/null 2>&1 &)
sleep 2 && curl -s -o /dev/null -w "server: %{http_code}\n" http://localhost:8123/index.html
```

**Recipe B — Lighthouse one page**

```bash
npx -y lighthouse "http://localhost:8123/PAGE.html" --quiet --chrome-flags="--headless" \
  --output=json --output-path=/tmp/lh-PAGE.json
python3 -c "
import json; d=json.load(open('/tmp/lh-PAGE.json'))
s={k:round(v['score']*100) for k,v in d['categories'].items() if v.get('score') is not None}
bp=[r['id'] for r in d['categories']['best-practices']['auditRefs']
    if d['audits'][r['id']].get('score') is not None and d['audits'][r['id']]['score']<1]
print(s); print('BP failures:', bp)
"
```
Required: `accessibility: 100`, `seo: 100`, BP failures exactly `['third-party-cookies','inspector-issues']`.

**Recipe C — overflow at 375×812.** Load any same-origin page on `localhost:8123`, then run in the page context. Set `pages` to the slugs under test.

```js
const pages = ['PAGE1','PAGE2'];
const out = [];
for (const p of pages) {
  const f = document.createElement('iframe');
  f.style.cssText = 'position:fixed;top:0;left:0;width:375px;height:812px;border:0;z-index:99999;background:#0d1117';
  f.src = '/' + p + '.html';
  document.body.appendChild(f);
  await new Promise(r => { f.onload = r; setTimeout(r, 7000); });
  await new Promise(r => setTimeout(r, 800));
  const d = f.contentDocument, de = d.documentElement;
  de.scrollLeft = 50; const s = de.scrollLeft; de.scrollLeft = 0;
  const off = [];
  d.querySelectorAll('*').forEach(el => {
    const r = el.getBoundingClientRect();
    if (r.width > 0 && (r.right > de.clientWidth + 1 || r.left < -1))
      off.push(el.tagName.toLowerCase() + '.' + (typeof el.className === 'string' ? el.className.trim().split(/\s+/)[0] : ''));
  });
  out.push({ p, vw: de.clientWidth, scrollX: s > 0, bw: d.body.scrollWidth, off: [...new Set(off)].slice(0,4) });
  f.remove();
}
JSON.stringify(out, null, 1)
```
Required per page: `vw: 375`, `scrollX: false`, `bw: 375`. **If `vw` is not 375 the run is meaningless** — the iframe failed to size and the result must be discarded. `.stack-track` / `.stack-group` / `.stack-item` appearing in `off` is expected: the tech marquee is intentionally wider than the viewport inside its own overflow container, which is why `bw` stays 375.

**Recipe D — bilingual head audit for the five new pairs**

```bash
for f in work services about faq process; do
  for v in "$f" "$f-en"; do
    printf "  %-14s hreflang:%s canonical:%s search:%s analytics:%s lang:%s\n" "$v" \
      "$(grep -c hreflang $v.html)" \
      "$(grep -c "rel=\"canonical\" href=\"https://ph-akin.dev/$v.html\"" $v.html)" \
      "$(grep -c 'site-search.js' $v.html)" \
      "$(grep -c 'assets/analytics.js' $v.html)" \
      "$(grep -o '<html lang=\"[^\"]*\"' $v.html)"
  done
done
```
Required: `hreflang:3 canonical:1 search:1 analytics:1`, `lang="th"` on the plain slug and `lang="en"` on the `-en` twin.

**Recipe E — nav consistency across the 19 selling pages**

```bash
PAGES="index index-en work work-en services services-en about about-en faq faq-en process process-en web-clinic web-booking web-restaurant web-shop web-gym web-construction web-solar"
for p in $PAGES; do
  printf "  %-18s navbar:%s links:%s search:%s current:%s\n" "$p" \
    "$(grep -c 'class="navbar"' $p.html)" \
    "$(grep -c 'href="work.html"\|href="services.html"\|href="about.html"\|href="faq.html"' $p.html)" \
    "$(grep -c 'class="site-search"' $p.html)" \
    "$(grep -c 'aria-current="page"' $p.html)"
done
```
Required every row: `navbar:1`, `links:8` — the grep matches only those four exact hrefs, and each appears twice: once in the bar, once in the mobile panel. `หน้าแรก` (`/`) and `EN` (`*-en.html` or `index-en.html`) are outside the pattern by design, `search:2`, `current:2`.

---

## Task 1: Extract the navbar into a shared stylesheet

**Files:**
- Create: `assets/site-nav.css`
- Modify: `index.html`, `index-en.html`

**Interfaces:**
- Produces: `assets/site-nav.css` defining `.navbar`, `.nav-inner`, `.nav-brand`, `.nav-logo-mark`, `.nav-links`, `.nav-resume`, `.nav-toggle`, `.nav-mobile-panel` and their breakpoints. Task 7 relies on every one of those class names existing. There is **no** `.nav-lang` — see the corrections above.

The homepage nav already works and is already responsive. The problem is that its CSS lives inside `index.html`'s inline `<style>`, so the other 17 pages cannot use it. This task moves it without changing a pixel.

- [x] **Step 1: Capture the current rendering as the baseline**

Run Recipe A, then in the browser:

```js
const el = document.querySelector('.nav-inner');
const cs = getComputedStyle(el);
JSON.stringify({
  navH: Math.round(document.querySelector('.navbar').getBoundingClientRect().height),
  innerH: Math.round(el.getBoundingClientRect().height),
  display: cs.display, gap: cs.gap, justify: cs.justifyContent,
  linkCount: document.querySelectorAll('.nav-links a').length,
  brandFont: getComputedStyle(document.querySelector('.nav-brand')).fontSize
})
```
Write the result down. Step 6 must reproduce it exactly.

- [x] **Step 2: Find every nav rule in `index.html`**

```bash
grep -n '^\s*\.\(navbar\|nav-inner\|nav-brand\|nav-logo-mark\|nav-links\|nav-resume\|nav-toggle\|nav-mobile-panel\)' index.html
grep -n 'nav-links\|nav-toggle\|nav-resume\|nav-mobile-panel\|navbar' index.html | grep -E '@media|display: none'
```
The rules are contiguous near the top of the `<style>` block, plus entries inside the `1180px` and `768px` media queries.

- [x] **Step 3: Move those rules verbatim into `assets/site-nav.css`**

Cut — do not copy — every rule found in Step 2 and paste it into the new file, preserving order and the media-query nesting.

**One deliberate edit while moving:** `.nav-inner` currently relies on the markup also carrying `.container`, whose only definition is inline in `index.html`. Fold those two declarations into `.nav-inner` so the nav stylesheet stands alone:

```css
.nav-inner {
  width: min(var(--max), calc(100% - 40px));   /* was .container */
  margin: 0 auto;                              /* was .container */
  height: 68px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 20px;
}
```

Leave `.container` itself in `index.html` untouched — ten other elements on that page use it.

Add a header comment:

```css
/* ============================================================
   Global navigation — shared by the 19 selling pages.
   Extracted verbatim from index.html's inline <style> so the
   funnel pages can use the same bar. Tokens (--surface, --ink,
   --accent, --r-sm, --ease…) come from each page's own :root.
   ============================================================ */
```

Do not reformat, rename or "tidy" any declaration while moving it. A pure move is reviewable in a way that a move-plus-edit is not.

- [x] **Step 4: Link the new stylesheet from both homepages**

Immediately before the existing `site-search.css` link:

```html
  <link rel="stylesheet" href="assets/site-nav.css" />
```

- [x] **Step 5: Confirm no nav rules were left behind or duplicated**

```bash
for f in index.html index-en.html; do
  printf "%-14s inline nav rules left: %s  (expect 0)\n" "$f" \
    "$(grep -cE '^\s*\.(navbar|nav-inner|nav-brand|nav-logo-mark|nav-links|nav-resume|nav-toggle|nav-mobile-panel)[ ,{:]' $f)"
done
printf "site-nav.css rules: %s\n" "$(grep -cE '^\.' assets/site-nav.css)"
```

- [x] **Step 6: Re-run Step 1 and compare**

Every value must match the baseline. If `navH` changed, a rule was dropped.

- [x] **Step 7: Run Recipe C for `index` and `index-en`, and Recipe B for `index.html`**

Expected: unchanged from before this task — `vw: 375`, `scrollX: false`, a11y 100, SEO 100.

- [x] **Step 8: Commit**

```bash
git add assets/site-nav.css index.html index-en.html
git commit -m "refactor: extract the navbar into assets/site-nav.css

Pure move, no rule changed. The homepage nav already worked and was
already responsive; the only problem was that it lived in index.html's
inline <style>, so the other seventeen selling pages could not use it.

Verified by capturing computed navbar geometry before and after — height,
gap, justification, brand font size and link count all identical."
```

---

## Task 2: Build `work.html` and `work-en.html`

**Files:**
- Create: `work.html`, `work-en.html`

**Interfaces:**
- Consumes: `assets/portfolio-pages.css` components and the 13 `.work-card` blocks that currently live in `index.html`'s `#projects`.
- Produces: `work.html` / `work-en.html`. Task 7's nav links to them; Task 10 sitemaps them.

This is the deeper archive: the same 13 cards plus the 4 case studies and the tag cloud, all on one page.

- [x] **Step 1: Copy the whole `#projects` section out of `index.html`**

```bash
python3 - <<'PY'
import re
h = open('index.html', encoding='utf-8').read()
s = h.index('<section class="section" id="projects"')
e = h.index('\n    </section>', s) + len('\n    </section>')
open('/tmp/projects-th.html','w',encoding='utf-8').write(h[s:e])
print('extracted', h[s:e].count('work-card'), 'work-card occurrences')
PY
```
Repeat against `index-en.html` into `/tmp/projects-en.html`.

- [x] **Step 2: Build the page shell**

Use the head block and `<header class="navbar">` — no, **not yet**: the global nav lands in Task 7. For now give both files the same `.page-shell nav` the industry pages use, so the file is valid and shippable on its own:

```html
  <header class="topbar">
    <nav class="page-shell nav" aria-label="เมนูผลงาน">
      <a class="brand" href="/" aria-label="ผลงานทั้งหมด — กลับไปหน้าพอร์ตโฟลิโอ">
        <span class="brand-mark" aria-hidden="true">
          <svg viewBox="0 0 34 34" focusable="false">
            <rect class="mark-back" x="8" y="7" width="16" height="13" rx="3" />
            <rect class="mark-front" x="12" y="12" width="16" height="15" rx="3" />
            <path class="mark-line" d="M16 18h7M16 23h4" />
            <circle class="mark-dot" cx="24" cy="17" r="2.1" />
          </svg>
        </span>
        <span>ผลงานทั้งหมด</span>
      </a>
      <ul class="nav-links">
        <li><a href="/">หน้าแรก</a></li>
        <li><a href="/#services">บริการ</a></li>
        <li><a class="nav-primary" href="/#contact">ติดต่อ</a></li>
        <li><a href="work-en.html">EN</a></li>
      </ul>
    </nav>
  </header>
```

- [x] **Step 3: Head block**

```html
  <title>ผลงานทั้งหมด — เว็บไซต์ที่เคยทำ | Phakin Chawanpunya</title>
  <meta name="description" content="รวมผลงานเว็บไซต์ที่เคยทำทั้งหมด 13 โปรเจกต์ และ case study 4 ชิ้น — คลินิก ร้านอาหาร ขายของออนไลน์ ระบบจองคิว ก่อสร้าง โซลาร์ กรองดูตามประเภทธุรกิจได้" />
  <link rel="canonical" href="https://ph-akin.dev/work.html" />
  <link rel="alternate" hreflang="th" href="https://ph-akin.dev/work.html" />
  <link rel="alternate" hreflang="en" href="https://ph-akin.dev/work-en.html" />
  <link rel="alternate" hreflang="x-default" href="https://ph-akin.dev/work.html" />
  <meta property="og:locale" content="th_TH" />
```
`work-en.html` mirrors this with `lang="en"`, `og:locale` `en_US`, a self canonical at `work-en.html`, the same three `hreflang` links, and English title/description.

- [x] **Step 4: Body**

```html
  <main>
    <section class="hero case-hero">
      <div class="page-shell">
        <span class="eyebrow">ผลงาน</span>
        <h1>ผลงานทั้งหมด</h1>
        <p class="hero-copy">เว็บไซต์ 13 โปรเจกต์และ case study 4 ชิ้น กรองดูตามประเภทธุรกิจได้ — ทุกชิ้นกดเข้าไปดูรายละเอียดและเปิดเว็บจริงได้</p>
      </div>
    </section>

    <section class="section" id="projects">
      <div class="page-shell">
        … the filter bar, active-filter chip, works grid and tag cloud from /tmp/projects-th.html …
      </div>
    </section>

    <section class="section" id="case-studies">
      <div class="page-shell">
        <div class="section-heading"><div>
          <span class="eyebrow">เจาะลึก</span>
          <h2>Case studies</h2>
        </div></div>
        <div class="project-strip">
          <a class="project-link" href="case-study-pulseboard.html"><strong>PulseBoard</strong><span>…</span></a>
          <a class="project-link" href="case-study-launchledger.html"><strong>LaunchLedger</strong><span>…</span></a>
          <a class="project-link" href="case-study-interntrack.html"><strong>InternTrack</strong><span>…</span></a>
          <a class="project-link" href="case-study-habitquest.html"><strong>HabitQuest</strong><span>…</span></a>
        </div>
      </div>
    </section>

    <section class="section" id="cta">
      <div class="page-shell">
        <div class="result-band">
          <div>
            <span class="eyebrow">สนใจแบบไหน?</span>
            <h2>อยากได้เว็บแบบไหนบอกได้เลย</h2>
            <p>เล่าโจทย์มาคร่าว ๆ ผมช่วยดูให้ว่าควรทำแบบไหนและงบประมาณเท่าไหร่</p>
          </div>
          <div class="result-actions">
            <a class="button primary" href="https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob" target="_blank" rel="noopener noreferrer">เริ่มงานบน Fastwork</a>
            <a class="button" href="mailto:a0626568471@gmail.com">อีเมลหาผม</a>
          </div>
        </div>
      </div>
    </section>
  </main>
```

Take each case-study `<span>` blurb from the matching card in `index.html`'s `#case-studies` — same rule the industry pages follow, and the same one that was violated and fixed in plan 1's `3171266`.

- [x] **Step 5: Copy the filter JavaScript**

The cards need their filter. Copy the `/* ---- Filter bar: one axis, industry ---- */` block from `index.html`'s inline script into a `<script>` before `</body>` on both files. It is self-contained — it queries `.filter-btn`, `.work-card[data-industry]`, `#works-empty`, `#filter-status` and the chip ids, all of which come across with the markup.

Do **not** copy the featured-carousel code. There is no carousel on this page, and its clone-stripping logic would have nothing to strip.

- [x] **Step 6: Verify**

Run Recipe D (the `work` rows), Recipe C for `work` and `work-en`, Recipe B for `work.html`, and:

```bash
for f in work work-en; do
  printf "%-10s cards:%s filters:%s carousel:%s deadlinks:%s\n" "$f" \
    "$(grep -c 'data-industry=' $f.html)" \
    "$(grep -c 'class="filter-btn' $f.html)" \
    "$(grep -c 'data-featured' $f.html)" \
    "$(grep -oE 'href="[a-z0-9-]+\.html"' $f.html | sed 's/href="//;s/"//' | sort -u | while read t; do [ -f "$t" ] || echo x; done | wc -l | tr -d ' ')"
done
```
Required: `cards:13 filters:9 carousel:0 deadlinks:0`.

Then in the browser, confirm the filter works on the new page: every button's count equals the number of visible cards, and `ทั้งหมด` shows 13.

- [x] **Step 7: Commit**

```bash
git add work.html work-en.html
git commit -m "feat: add the full work archive page

The deeper archive behind the homepage grid — same 13 cards plus the tag
cloud and the 4 case studies, which had no home of their own before.

Carries the filter but not the featured carousel: there is nothing to
feature on a page that already shows everything, and the carousel's
clone-stripping would have nothing to strip."
```

---

## Task 3: Build `services.html` and `services-en.html`

**Files:**
- Create: `services.html`, `services-en.html`

**Interfaces:**
- Consumes: package facts from `landing-page.html`, `dashboard-ui.html`, `business-website.html`; the seven `web-*.html` pages from plan 1.
- Produces: `services.html` / `services-en.html`.

Since the homepage pricing section was removed, this is now the only page that puts all three packages side by side. It is the hub: three packages on top, seven industries below.

- [x] **Step 1: Head block**

```html
  <title>บริการและราคา — รับทำเว็บไซต์ เริ่มต้น ฿3,900 | Phakin Chawanpunya</title>
  <meta name="description" content="บริการรับทำเว็บไซต์ 3 แพ็กเกจ — Landing Page ฿3,900 · Dashboard UI ฿7,900 · Business Website ฿9,900 ราคาโปร่งใส ไม่มีค่าใช้จ่ายแอบแฝง พร้อมหน้าบริการแยกตามประเภทธุรกิจ" />
  <link rel="canonical" href="https://ph-akin.dev/services.html" />
  <link rel="alternate" hreflang="th" href="https://ph-akin.dev/services.html" />
  <link rel="alternate" hreflang="en" href="https://ph-akin.dev/services-en.html" />
  <link rel="alternate" hreflang="x-default" href="https://ph-akin.dev/services.html" />
```

- [x] **Step 2: Hero + package comparison**

Three `.study-block`s in a `.page-shell.study-grid`, one per package. Each carries: package name as `<h2>`, the price as a `.study-meta`-style figure, the timeline and revisions, the feature bullets **copied verbatim** from that package's `#services` card in `index.html`, and a `.button` to its category page.

Verify the numbers against the source before moving on:

```bash
for p in landing-page dashboard-ui business-website; do
  echo "--- $p ---"
  sed -n '/study-meta/,/<\/section>/p' $p.html | grep -oE '>[^<>]{2,60}<' | tr -d '<>' | sed '/^\s*$/d' | head -8
done
```

- [x] **Step 3: Industry entry points**

A `.project-strip` of seven `.project-link`s — one per `web-*.html` — using each page's own `<h1>` subject as the `<strong>` and its `{{BEST_FOR}}` line as the `<span>`:

```html
<a class="project-link" href="web-clinic.html"><strong>คลินิก / ความงาม</strong><span>คลินิกที่อยากให้คนไข้จองคิวเองได้</span></a>
<a class="project-link" href="web-booking.html"><strong>จองคิว / นัดหมาย</strong><span>ธุรกิจที่รับจองผ่านแชทจนคิวชนกัน</span></a>
<a class="project-link" href="web-restaurant.html"><strong>ร้านอาหาร / คาเฟ่</strong><span>ร้านที่อยากให้คนหาเมนูและที่ตั้งเจอเร็ว</span></a>
<a class="project-link" href="web-shop.html"><strong>ขายของออนไลน์</strong><span>ร้านที่มีสินค้าประจำและอยากมีหน้าร้านของตัวเอง</span></a>
<a class="project-link" href="web-gym.html"><strong>ฟิตเนส / ยิม</strong><span>ยิมที่อยากให้คนเห็นราคาและตารางคลาสก่อนเดินเข้ามา</span></a>
<a class="project-link" href="web-construction.html"><strong>ก่อสร้าง / รับเหมา</strong><span>ผู้รับเหมาที่มีผลงานแล้วแต่ยังไม่มีที่โชว์</span></a>
<a class="project-link" href="web-solar.html"><strong>โซลาร์ / พลังงาน</strong><span>ผู้ติดตั้งโซลาร์ที่อยากคัดลูกค้าก่อนออกไปดูหน้างาน</span></a>
```

- [x] **Step 4: Link out to process and FAQ, then the closing CTA**

A short `.study-block` pointing at `process.html` ("อยากรู้ว่าทำงานยังไง") and `faq.html` ("คำถามที่พบบ่อย"), then the standard `.result-band`.

- [x] **Step 5: English twin**

Per the site's bilingual rule, **package names, prices and feature bullets stay in Thai** on `services-en.html` — exactly as `#services` on `index-en.html` already does. Wrap those runs in `lang="th"`; leave the surrounding chrome in English with no section-level `lang`. Putting `lang="th"` on a section with an English heading is the bug that had to be fixed in plan 1's `766ecd7`.

- [x] **Step 6: Verify**

Recipe D (`services` rows), Recipe C, Recipe B, plus:

```bash
grep -oE 'href="(web-[a-z]+|landing-page|dashboard-ui|business-website)[a-z-]*\.html"' services.html \
  | sed 's/href="//;s/"//' | sort -u | while read t; do [ -f "$t" ] && echo "OK $t" || echo "DEAD $t"; done
grep -oE '฿[0-9,]+' services.html | sort -u
```
Required: no `DEAD`, and exactly `฿3,900 ฿7,900 ฿9,900`.

- [x] **Step 7: Commit**

```bash
git add services.html services-en.html
git commit -m "feat: add the services hub page

Now the only page that compares all three packages side by side — the
homepage pricing section was removed, so this is where that job moved.

Three packages on top with prices copied verbatim from the category
pages, seven industry entry points below. English twin keeps package and
pricing copy in Thai per the site rule, with lang=\"th\" on those runs
only, not on a section whose heading is English."
```

---

## Task 4: Build `about.html` and `about-en.html`

**Files:**
- Create: `about.html`, `about-en.html`

**Interfaces:**
- Consumes: the `#about` and `#experience` content in `index.html`.
- Produces: `about.html` / `about-en.html`.

- [x] **Step 1: Extract the source content**

```bash
python3 - <<'PY'
h = open('index.html', encoding='utf-8').read()
s = h.index('<section class="section" id="about"')
e = h.index('\n    </section>', s) + len('\n    </section>')
open('/tmp/about-th.html','w',encoding='utf-8').write(h[s:e])
print('captured', e-s, 'chars; contains #experience:', 'id="experience"' in h[s:e])
PY
```

- [x] **Step 2: Head block**

```html
  <title>เกี่ยวกับผม — Phakin Chawanpunya นักพัฒนาเว็บฟรีแลนซ์</title>
  <meta name="description" content="Phakin Chawanpunya นักพัฒนาเว็บฟรีแลนซ์ รับทำ Landing Page Dashboard และเว็บไซต์ธุรกิจ — ประวัติ ทักษะ เครื่องมือที่ใช้ และการศึกษาจาก KMUTT" />
  <link rel="canonical" href="https://ph-akin.dev/about.html" />
  <link rel="alternate" hreflang="th" href="https://ph-akin.dev/about.html" />
  <link rel="alternate" hreflang="en" href="https://ph-akin.dev/about-en.html" />
  <link rel="alternate" hreflang="x-default" href="https://ph-akin.dev/about.html" />
```

- [x] **Step 3: Body**

Hero (`.hero.case-hero` with eyebrow `เกี่ยวกับผม`, `<h1>Phakin Chawanpunya</h1>`, the bio as `.hero-copy`), then the experience content translated from `index.html`'s card layout into `.study-grid` / `.study-block`s, then a `.project-strip` linking to `resume.html` and `work.html`, then a `.result-band`.

**Do not restate the stack as something the demos were built with.** The bio may say what Phakin works with; it may not claim the 12 local demos use React or Node. Only HabitQuest genuinely uses React and Vite.

- [x] **Step 4: Keep `index.html`'s `#about` in place**

The homepage keeps its condensed About; this page is the fuller version. Add a link from the homepage section to `about.html` in Task 7, not here — `main` auto-deploys and the page must exist first.

- [x] **Step 5: Verify** — Recipe D (`about` rows), Recipe C, Recipe B.

- [x] **Step 6: Commit**

```bash
git add about.html about-en.html
git commit -m "feat: add the about page

Fuller version of the homepage's condensed About — bio, experience
timeline, tools and KMUTT in one place, linking out to the résumé and the
work archive.

States what I work with without claiming the twelve local demos were
built with it. They are plain HTML/CSS/vanilla JS; only HabitQuest uses
React and Vite."
```

---

## Task 5: Build `faq.html` and `faq-en.html`

**Files:**
- Create: `faq.html`, `faq-en.html`

**Interfaces:**
- Produces: `faq.html` / `faq-en.html` with valid `FAQPage` JSON-LD.

- [x] **Step 1: Head block plus `FAQPage` structured data**

```html
  <title>คำถามที่พบบ่อย — รับทำเว็บไซต์ | Phakin Chawanpunya</title>
  <meta name="description" content="คำถามที่พบบ่อยก่อนจ้างทำเว็บไซต์ — ราคาเท่าไหร่ ใช้เวลากี่วัน แก้ได้กี่รอบ โดเมนและโฮสต์ใครออก แก้เนื้อหาเองได้ไหม รับประกันอันดับ Google ไหม" />
  <link rel="canonical" href="https://ph-akin.dev/faq.html" />
  <link rel="alternate" hreflang="th" href="https://ph-akin.dev/faq.html" />
  <link rel="alternate" hreflang="en" href="https://ph-akin.dev/faq-en.html" />
  <link rel="alternate" hreflang="x-default" href="https://ph-akin.dev/faq.html" />
```

The JSON-LD must contain **exactly** the questions and answers rendered on the page — Google treats a mismatch as a structured-data violation:

```html
  <script type="application/ld+json">
  {
    "@context": "https://schema.org",
    "@type": "FAQPage",
    "mainEntity": [
      { "@type": "Question", "name": "ทำเว็บไซต์ราคาเท่าไหร่?",
        "acceptedAnswer": { "@type": "Answer", "text": "เริ่มต้น ฿3,900 สำหรับเว็บหน้าเดียว ฿7,900 สำหรับงานออกแบบระบบสูงสุด 5 หน้าจอ และ ฿9,900 สำหรับเว็บธุรกิจ 3-5 หน้าพร้อมโครงสร้าง SEO พื้นฐาน งานที่ซับซ้อนกว่านี้ประเมินให้ก่อนเริ่มเสมอ" } }
    ]
  }
  </script>
```

- [x] **Step 2: Write the questions**

Ten `.study-block`s with `<h3>` questions in a `.study-grid`, covering: ราคา · ระยะเวลา · จำนวนรอบแก้ · โดเมนและโฮสต์ · แก้เนื้อหาเองได้ไหม · รองรับมือถือไหม · SEO และการรับประกันอันดับ · การชำระเงินผ่าน Fastwork · หลังส่งมอบดูแลต่อไหม · ถ้าไม่พอใจงานทำยังไง

Two of these must stay honest and are the reason the page is worth having:

- **SEO** — say plainly that rankings are not guaranteed by anyone, and describe what is actually done (structure, headings, descriptions written around real search terms).
- **หลังส่งมอบ** — state the real terms from the packages (`ฟรีแก้บั๊ก 3 เดือน`), not open-ended support.

- [x] **Step 3: Validate the structured data matches the page**

```bash
python3 - <<'PY'
import json, re, html
h = open('faq.html', encoding='utf-8').read()
ld = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', h, re.S).group(1))
qs_ld = [q['name'] for q in ld['mainEntity']]
qs_dom = [html.unescape(m) for m in re.findall(r'<h3>([^<]+)</h3>', h)]
print('json-ld questions :', len(qs_ld))
print('rendered questions:', len(qs_dom))
missing = [q for q in qs_ld if q not in qs_dom]
extra   = [q for q in qs_dom if q not in qs_ld]
print('in JSON-LD but not on page:', missing)
print('on page but not in JSON-LD:', extra)
PY
```
Both lists must be empty.

- [x] **Step 4: Verify** — Recipe D (`faq` rows), Recipe C, Recipe B.

- [x] **Step 5: Commit**

```bash
git add faq.html faq-en.html
git commit -m "feat: add the FAQ page with FAQPage structured data

Ten pre-hire questions with JSON-LD whose questions and answers match the
rendered page exactly — a mismatch is a structured-data violation, so a
check enforces it rather than trusting the author.

The SEO answer refuses to promise rankings and the support answer states
the real three-month bug-fix term rather than implying open-ended help.
Both are the questions buyers actually hesitate on, and a page that
dodges them is not worth indexing."
```

---

## Task 6: Build `process.html` and `process-en.html`

**Files:**
- Create: `process.html`, `process-en.html`

**Interfaces:**
- Produces: `process.html` / `process-en.html`. Linked from `services.html` and `faq.html`, and from the footer in Task 7 — **not** from the nav.

- [x] **Step 1: Head block**

```html
  <title>ขั้นตอนการทำงาน — สั่งงานถึงส่งมอบ | Phakin Chawanpunya</title>
  <meta name="description" content="ขั้นตอนการทำงานตั้งแต่คุยโจทย์จนส่งมอบเว็บไซต์ — 5 ขั้น ใช้เวลากี่วัน ลูกค้าต้องเตรียมอะไร แก้ไขได้ตอนไหน และส่งมอบอะไรบ้าง" />
  <link rel="canonical" href="https://ph-akin.dev/process.html" />
  <link rel="alternate" hreflang="th" href="https://ph-akin.dev/process.html" />
  <link rel="alternate" hreflang="en" href="https://ph-akin.dev/process-en.html" />
  <link rel="alternate" hreflang="x-default" href="https://ph-akin.dev/process.html" />
```

- [x] **Step 2: Five steps as `.study-block`s**

| # | ขั้น | เนื้อหา |
|---|---|---|
| 1 | คุยโจทย์ | เล่าธุรกิจ เป้าหมาย งบ · ผมประเมินว่าควรทำแพ็กเกจไหน · ฟรี ไม่ผูกมัด |
| 2 | ตกลงงานบน Fastwork | ระบุขอบเขต ราคา กำหนดส่งชัดเจน · Fastwork ถือเงินไว้จนงานเสร็จ |
| 3 | ลูกค้าส่งข้อมูล | ข้อความ รูป โลโก้ · **ขั้นนี้คือขั้นที่ทำให้งานช้าที่สุดเสมอ** พูดตรง ๆ ว่าถ้าข้อมูลมาช้า กำหนดส่งเลื่อน |
| 4 | ออกแบบและพัฒนา | ส่งให้ดูระหว่างทาง · แก้ได้ตามรอบในแพ็กเกจ |
| 5 | ส่งมอบ | ขึ้นเว็บจริง · ส่งไฟล์และวิธีใช้ · ฟรีแก้บั๊กตามระยะของแพ็กเกจ |

Step 3's warning is the point of the page. Every freelance project slips there and saying so up front sets a real expectation instead of an argument later.

- [x] **Step 3: Verify** — Recipe D (`process` rows), Recipe C, Recipe B.

- [x] **Step 4: Commit**

```bash
git add process.html process-en.html
git commit -m "feat: add the process page

Five steps from brief to handover, aimed at someone hiring a freelancer
for the first time.

Step three says outright that waiting on the client's content is what
slows every project down and that a late handoff moves the deadline.
Saying it before the work starts sets an expectation; saying it after is
an argument."
```

---

## Task 7: Roll the global nav to all 19 selling pages

**Files:**
- Modify: `index.html`, `index-en.html`, the 10 new files from Tasks 2-6, the 7 `web-*.html`

**Interfaces:**
- Consumes: `assets/site-nav.css` (Task 1) and all five page pairs (Tasks 2-6). **Do not start until every one of those files is committed** — `main` auto-deploys and a nav pointing at a missing page ships a 404.

- [x] **Step 1: Confirm every nav destination exists**

```bash
for f in work services about faq process; do
  for v in "$f" "$f-en"; do [ -f "$v.html" ] && echo "OK $v.html" || echo "MISSING $v.html"; done
done
```
Stop if anything is missing.

- [x] **Step 2: Replace the nav on the two homepages**

Swap the anchor links for page links using the markup in "The global nav" above. `href="#projects"` becomes `work.html`, `#services` becomes `services.html`, `#about` becomes `about.html`, and `#testimonials` / `#experience` / `#case-studies` leave the bar entirely — they are still reachable by scrolling and from the footer.

Set `aria-current="page"` on `หน้าแรก`.

- [x] **Step 3: Add the nav to the 10 new pages**

Replace the interim `.page-shell nav` from Tasks 2-6 with the global nav, setting `aria-current="page"` on that page's own entry. Add the three head tags (`site-nav.css`, `site-search.css`, `site-search.js`) to each.

These pages use `portfolio-pages.css`, which has **no** `.container` rule — that is exactly why Task 1 folded its two declarations into `.nav-inner`. The markup here uses `<div class="nav-inner">` with no `.container`, so the bar aligns identically on both families of page with no cross-file dependency.

Confirm the assumption still holds before relying on it:

```bash
python3 -c "
import re
c=open('assets/portfolio-pages.css',encoding='utf-8').read()
print('.container rules in portfolio-pages.css:', len(re.findall(r'(?m)^\.container\s*[,{:]', c)), '(expect 0)')
n=open('assets/site-nav.css',encoding='utf-8').read()
print('.nav-inner has its own width:', 'min(var(--max)' in n)
"
```

- [x] **Step 4: Add the nav to the 7 industry pages**

Same, replacing their three-link `.page-shell nav`. Their `EN` link goes to `index-en.html`, since they have no `-en` twin.

- [x] **Step 5: Point `ติดต่อ` correctly**

On `index.html` / `index-en.html` it is `#contact`. On all 17 other pages it must be `/#contact`, or it will scroll to nothing.

```bash
grep -c 'href="#contact"' index.html index-en.html
grep -c 'href="/#contact"' work.html services.html about.html faq.html process.html web-clinic.html
```

- [x] **Step 6: Run Recipe E**

Every row must show `navbar:1 links:8 search:2 current:2`.

- [x] **Step 7: Verify the search works on a page that never had it**

Load `services.html`, type `คลินิก`, and confirm the dropdown lists the clinic service page and the three clinic projects. The index is fetched relative to the page, so a path bug shows up here.

- [x] **Step 8: Run Recipe C across all 19 pages, and Recipe B on four samples**

`index`, `work`, `services`, `web-clinic`.

- [x] **Step 9: Commit**

```bash
git add index.html index-en.html work*.html services*.html about*.html faq*.html process*.html web-*.html
git commit -m "feat: ship one nav across all 19 selling pages

The homepage's anchor links become page links and the same bar goes on
every page a buyer can land on, search included — previously it existed
only on the two homepages.

Landed only after all five page pairs were committed: main auto-deploys,
so rolling the nav out first would have shipped 404s.

ติดต่อ resolves to #contact on the homepages and /#contact everywhere
else, and aria-current marks the active entry so a screen reader user can
tell where they are."
```

---

## Task 8: Make the technology row open the search

**Files:**
- Modify: `index.html`, `index-en.html`

**Interfaces:**
- Consumes: the search from `assets/site-search.js`.

Spec decision **D7**: these buttons open the site search rather than filtering the portfolio. An audit of all 12 local demos found `<script>` count 2 on every one — the page's own inline script plus `analytics.js` — and zero external libraries. A truthful technology filter would offer HTML/CSS/JavaScript, each matching all 13 projects and changing nothing when clicked.

- [x] **Step 1: Fix the section heading**

```bash
grep -n 'เทคโนโลยีที่เราใช้ในผลงาน\|stack-sec' index.html index-en.html
```
The heading must describe a skill set, not the demos' stacks: **`เทคโนโลยีที่ผมทำงานด้วย`** with the sub-line `คลิกเพื่อค้นหาในเว็บ`.

- [x] **Step 2: Add the static button row beneath the marquee**

The marquee keeps scrolling and stays decorative — clicking a moving target is hostile and tabbing through a scrolling strip is worse. Add real buttons below it:

```html
        <div class="tech-tags">
          <button type="button" class="tech-tag" data-q="HTML">HTML</button>
          <button type="button" class="tech-tag" data-q="CSS">CSS</button>
          <button type="button" class="tech-tag" data-q="JavaScript">JavaScript</button>
          <button type="button" class="tech-tag" data-q="React">React</button>
          <button type="button" class="tech-tag" data-q="Vite">Vite</button>
          <button type="button" class="tech-tag" data-q="Figma">Figma</button>
        </div>
```

Only technologies that return a result may appear. `React` and `Vite` resolve to HabitQuest; `HTML`, `CSS` and `JavaScript` resolve broadly. Verify before shipping:

```bash
python3 -c "
import json
d=json.load(open('assets/search-index.json',encoding='utf-8'))['th']
for q in ['HTML','CSS','JavaScript','React','Vite','Figma']:
    n=sum(1 for r in d if q.lower() in (r['t']+' '+r.get('k','')).lower())
    print(f'{q:<12} {n} results' + ('   <-- DROP THIS BUTTON' if n==0 else ''))
"
```

- [x] **Step 3: Wire the buttons to the navbar search**

```js
      /* ---- Technology tags open the site search ---- */
      document.querySelectorAll('.tech-tag').forEach(btn => {
        btn.addEventListener('click', () => {
          const input = document.querySelector('.nav-inner .site-search input[type="search"]')
                     || document.querySelector('.site-search input[type="search"]');
          if (!input) return;
          input.focus();
          input.value = btn.dataset.q;
          input.dispatchEvent(new Event('input', { bubbles: true }));
          window.__track?.('tech_tag_search', { query: btn.dataset.q });
        });
      });
```

Below 768px the navbar field is hidden, so the fallback selector picks the copy inside the mobile panel. Confirm the panel is open first, or the focus goes nowhere:

```js
          if (getComputedStyle(input).display === 'none' || !input.offsetParent) {
            document.querySelector('.nav-toggle')?.click();
          }
```
Insert that before `input.focus()`.

- [x] **Step 4: Style the buttons**

```css
    .tech-tags{display:flex;flex-wrap:wrap;gap:.5rem;justify-content:center;margin-top:1.4rem;}
    .tech-tag{border:1px solid var(--border);background:var(--surface);color:var(--ink-2);border-radius:999px;padding:.4rem .9rem;font:inherit;font-size:.85rem;cursor:pointer;transition:border-color .18s var(--ease),color .18s var(--ease);}
    .tech-tag:hover{border-color:var(--accent);color:var(--accent-text);}
    .tech-tag:focus-visible{outline:2px solid var(--accent);outline-offset:2px;}
    @media (prefers-reduced-motion:reduce){.tech-tag{transition:none;}}
```

- [x] **Step 5: Verify in the browser**

Click `React`; the search must open showing HabitQuest. Tab to a tag and press Enter; same result. Repeat at 375px with the panel closed — the panel must open and the field receive focus.

- [x] **Step 6: Confirm no unsupportable claim remains**

```bash
grep -rn 'เทคโนโลยีที่เราใช้ในผลงาน' *.html || echo "clean"
grep -rniE '(สร้างด้วย|พัฒนาด้วย|built with).{0,60}(React|Node|Express|PostgreSQL)' *.html | grep -v habitquest || echo "clean"
```
Both must fall through to `clean`. HabitQuest's React claim is true and stays.

- [x] **Step 7: Run Recipe C and Recipe B on both homepages, then commit**

```bash
git add index.html index-en.html
git commit -m "feat: technology tags open the site search

Spec decision D7. A technology filter over the portfolio was designed and
then abandoned on evidence: all twelve local demos show script count 2 —
their own inline script plus analytics.js — and zero external libraries.
A truthful filter would have offered HTML/CSS/JavaScript, each matching
all thirteen projects and changing nothing when clicked.

The tags fire the search instead, so React surfaces the one project that
genuinely uses it. Every tag is checked against the index; a tag with no
results does not ship.

Heading changes from 'เทคโนโลยีที่เราใช้ในผลงาน' to 'เทคโนโลยีที่ผมทำงานด้วย'.
The marquee was never dishonest — it is a real skill set — but a heading
claiming these technologies were used in these projects is not
supportable."
```

---

## Task 9: Update `sitemap.xml` and `CLAUDE.md`

**Files:**
- Modify: `sitemap.xml` (66 → 76), `CLAUDE.md`

- [x] **Step 1: Add the ten new URLs**

Following the existing entry shape exactly — `<loc>`, `<changefreq>monthly</changefreq>`, `<priority>` — add under a new `<!-- Funnel pages -->` comment at priority `0.9` (above the category pages' `0.85`; these are the nav destinations):

```
https://ph-akin.dev/work.html          https://ph-akin.dev/work-en.html
https://ph-akin.dev/services.html      https://ph-akin.dev/services-en.html
https://ph-akin.dev/about.html         https://ph-akin.dev/about-en.html
https://ph-akin.dev/faq.html           https://ph-akin.dev/faq-en.html
https://ph-akin.dev/process.html       https://ph-akin.dev/process-en.html
```

- [x] **Step 2: Validate**

```bash
python3 -c "
import xml.etree.ElementTree as ET, os
t=ET.parse('sitemap.xml'); ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'
l=[e.text for e in t.iter(ns+'loc')]
print('total:', len(l))
print('duplicates:', sorted({u for u in l if l.count(u)>1}))
print('missing:', [u for u in l if not os.path.exists(u.replace('https://ph-akin.dev/','') or 'index.html')])
"
```
Required: `total: 76`, no duplicates, nothing missing.

- [x] **Step 3: Update `CLAUDE.md`**

- Add the five pairs and `assets/site-nav.css` to the Project Structure tree.
- Replace the "Pages & Sections (index.html)" table's Nav row with the global nav's five links plus search, EN and ติดต่อ, and note that `#pricing` and the contact form no longer exist.
- Add a **Global navigation** section: the 19 pages that carry it, that `assets/site-nav.css` is the single source, that `ติดต่อ` is `#contact` on the homepages and `/#contact` elsewhere, that `aria-current="page"` marks the active entry, and that the 42 showcase / case-study / resume files keep their contextual nav on purpose.
- Add a **Site search** section: `assets/search-index.json` is hand-maintained — **every new page must be added to both the `th` and `en` arrays or it will be unfindable** — matching is substring, and hidden keywords are what make `หมอฟัน` find the dental clinic.
- Update the "Add an industry landing page" recipe: step 1 becomes copy `web-clinic.html`, and a new final step says add the page to `assets/search-index.json`.

- [x] **Step 4: Commit**

```bash
git add sitemap.xml CLAUDE.md
git commit -m "docs: sitemap the funnel pages and document nav and search

Ten new URLs at priority 0.9, above the category pages — these are the
nav destinations now.

CLAUDE.md gains a global-navigation section and a site-search section.
The search one carries the trap: search-index.json is hand-maintained, so
a new page that is not added to both language arrays is simply
unfindable, with nothing failing to signal it."
```

---

## Task 10: Full verification pass

**Files:** none modified — this task runs checks and fixes what they surface.

- [x] **Step 1: Run Recipe A**

- [x] **Step 2: Lighthouse across all 12 new and changed pages**

```bash
for p in index index-en work work-en services services-en about about-en faq faq-en process process-en; do
  npx -y lighthouse "http://localhost:8123/$p.html" --quiet --chrome-flags="--headless" \
    --output=json --output-path="/tmp/lhv-$p.json" >/dev/null 2>&1
  python3 -c "
import json
d=json.load(open('/tmp/lhv-$p.json'))
s={k:round(v['score']*100) for k,v in d['categories'].items() if v.get('score') is not None}
bp=[r['id'] for r in d['categories']['best-practices']['auditRefs']
    if d['audits'][r['id']].get('score') is not None and d['audits'][r['id']]['score']<1]
ok = s['accessibility']==100 and s['seo']==100 and set(bp)<={'third-party-cookies','inspector-issues'}
print(f\"  {'$p':<14} a11y:{s['accessibility']:<4} seo:{s['seo']:<4} cls:{d['audits']['cumulative-layout-shift']['displayValue']:<5} {'PASS' if ok else 'FAIL '+str(bp)}\")
"
done
```
Lighthouse is slow — run this in two batches of six rather than letting a 2-minute timeout kill it midway.

- [x] **Step 3: Overflow across all 19 selling pages** — Recipe C.

- [x] **Step 4: Site-wide dead-link sweep**

```bash
for f in *.html; do
  grep -oE 'href="[a-zA-Z0-9._-]+\.html"' "$f" | sed 's/href="//;s/"//' | sort -u | while read t; do
    [ -f "$t" ] || echo "DEAD  $f -> $t"
  done
done; echo "sweep complete"
```

- [x] **Step 5: Recipe D and Recipe E**

- [x] **Step 6: Every page in the sitemap is in the search index and vice versa**

```bash
python3 - <<'PY'
import json, xml.etree.ElementTree as ET
idx = {r['u'] for r in json.load(open('assets/search-index.json',encoding='utf-8'))['th']}
t = ET.parse('sitemap.xml'); ns='{http://www.sitemaps.org/schemas/sitemap/0.9}'
sm = {e.text.replace('https://ph-akin.dev/','') for e in t.iter(ns+'loc')}
sm = {u for u in sm if u and not u.endswith('-en.html')}
print('in sitemap, missing from search index:', sorted(sm - idx))
PY
```
New funnel pages appearing here means Task 9 Step 3's warning was ignored — add them to both arrays.

- [x] **Step 7: Keyboard path through the search on a non-homepage**

On `services.html`: focus the field, type, `↓`, `Enter` navigates; `Esc` closes and returns focus.

- [x] **Step 8: Fix anything the checks surfaced, re-run only the failing check, then stop the server**

Do not call this task done while any check fails. If one cannot be made to pass, stop and report it rather than marking it complete.

---

## Plan Self-Review

**Spec coverage.** Global nav (D4) → Tasks 1 and 7; five bilingual funnel pairs → Tasks 2-6; clickable technology row (D7) → Task 8; sitemap and docs → Task 9; verification → Task 10. Search (D5) and the homepage restructure (D6) shipped in plan 1 and are explicitly out of scope here, recorded in "What changed since the spec was written".

**Placeholder scan.** The `…` inside Task 2 Step 4's body block and Task 7's mobile-panel line are structural elisions pointing at content extracted by a preceding step in the same task, not unspecified work. Every other code block is complete.

**Type consistency.** The class names Task 1 promises — `.navbar`, `.nav-inner`, `.nav-brand`, `.nav-logo-mark`, `.nav-links`, `.nav-resume`, `.nav-toggle`, `.nav-mobile-panel` — are exactly the ones Task 7's markup uses. Reviewing the draft against the code killed a `.nav-lang` class that appeared in both and exists in neither, and a `.container` dependency that `portfolio-pages.css` cannot satisfy. `.site-search` / `.site-search-field` / `.site-search-panel` / `.site-search-status` match the shipped `assets/site-search.css`. `data-industry` and `.filter-btn` in Task 2 match what `index.html` already carries.

**Ordering constraints, both stated in the tasks that depend on them:** Task 7 must not run before Tasks 2-6 are committed, and Task 8's tags must be verified against the search index before shipping.

**Parallelisation note.** Tasks 2-6 create five disjoint file pairs and can run as five concurrent agents. Tasks 1, 7, 8 all touch `index.html` / `index-en.html` and must serialise. Only one browser session exists, so per-task Lighthouse and overflow checks should consolidate into Task 10 exactly as they did in plan 1.

---

## Completion note — 2026-08-06

Shipped across `aac9fee`..`8b4ac4b`. Executed as: one page pair built and fully
verified first, then four agents in parallel on the remaining pairs, then the nav
rollout, then docs and verification.

**Executed differently from what is written above:**

1. **Task 1 grew into a full stylesheet extraction.** It planned to move only the
   navbar into `assets/site-nav.css`. Building `work.html` showed that was not
   enough — the page needs 71 rules that live in `index.html`'s inline `<style>`,
   and it cannot borrow them from `portfolio-pages.css` because the two sheets
   define `.hero`, `.section`, `.nav-links` and all five `.tag*` differently. The
   whole 1,343-line block moved to `assets/home-shell.css` instead.
2. **The nav is not one stylesheet.** Extracting the navbar so both families could
   share it was attempted and reverted: both define `.nav-links` at equal
   specificity, and the extraction left `.navbar`, `.nav-toggle` and
   `.nav-mobile-panel` behind because they sit after comment blocks. The 12
   home-shell pages carry the full navbar; the 13 portfolio-pages selling pages
   keep theirs and gain the same links and search.
3. **Task 8's clickable technology row was dropped.** Its own rule — a technology
   with no truthful matches gets no button — killed it: 2 of 19 names return
   results, both from HabitQuest. The section got an honest heading instead.
4. **The 3 category pages were added to scope.** Not in the original 19;
   `services.html` links straight at them, so leaving them on the old nav made a
   dead end mid-funnel. 25 selling pages now share the nav.

**Defects this plan contained, found by executing it:**

- `.nav-lang` appeared in the interface contract and the markup and exists in
  neither. The EN link is an `<li>` inside `.nav-links`.
- `.container` has zero rules in `portfolio-pages.css`, so 17 of 19 pages could
  not have satisfied the `container nav-inner` markup.
- `site-search.css` used `flex: 0 1 260px`, written for a row. The industry nav
  goes `flex-direction: column` at mobile, where that sized the height — the
  sticky bar became 378px, 27% of a 375×812 viewport.
- The two stylesheets name the same border colours `--border`/`--border-2` and
  `--line`/`--line-2`.
- `.card-link` used `--accent`: 4.5:1 on the page background, 4.29:1 inside a
  card. `index.html` passed only because its single instance sits in the
  testimonials footer.

**Worth remembering more than any of the above:** `work.html` was committed with
all 13 cards at `opacity: 0` and a dead hamburger, because only the filter block
was copied from `index.html` and not the reveal observer or the nav handler. It
passed Lighthouse a11y 100, SEO 100, the overflow recipe and the dead-link sweep.
Opacity-0 elements stay in the accessibility tree and still report layout boxes.
Three of the four parallel agents flagged it independently while working on their
own pages. Nothing in the automated checks would have caught it — only opening
the page.

**Final verification:** all 25 selling pages at Lighthouse a11y 100 / SEO 100 /
CLS 0, no overflow at 375×812, no dead links site-wide, no page loading both
stylesheet families, sitemap 76 URLs, search index 33 entries per language.
