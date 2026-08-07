# Work Archive Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development or
> superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox
> (`- [ ]`) syntax for tracking.

**Goal:** Rebuild `work.html` / `work-en.html` as a sidebar-filtered archive with in-page
keyword search, a visible result count, a featured toggle and the eight need tiles.

**Architecture:** Two panes inside `#projects`. The sidebar reuses the existing
`.filter-btn` buttons verbatim so `assets/site-ui.js`'s category axis needs no change and
`index.html` cannot regress. Two new predicates fold into the same `applyFilter()`.

**Tech Stack:** Vanilla HTML/CSS/JS, no build step.

## Global Constraints

- `assets/site-ui.js` is shared with `index.html` / `index-en.html`. Both new blocks must
  return early when their elements are absent.
- The nine `<button class="filter-btn" data-filter data-label>` elements keep their markup
  exactly. No `<input type="radio">`.
- The 13 `.work-card` bodies are not edited.
- `375 × 812` must report `canScrollX: false`, with `clientWidth === 375` confirmed first —
  `resize_window` silently does nothing in this environment; use the iframe recipe.
- Lighthouse: Accessibility 100, SEO 100, CLS 0. Best Practices caps at 77 (Clarity cookies).
- Both string sets come from `document.documentElement.lang`, never hard-coded per file.
- `home-shell.css` is requested with **no query string** on all 12 pages. It gains
  `?v=work-sidebar` in Task 5, or returning visitors get an unstyled sidebar.

---

## Task 1: Sidebar and results CSS

**Files:** Modify `assets/home-shell.css`

**Interfaces:**
- Produces: `.work-layout`, `.work-filter`, `.work-search`, `.work-results`,
  `.work-results-head`, `.result-count`, `.featured-toggle`
- Consumes: existing `--surface`, `--border`, `--muted`, `--accent`, `--accent-dark`, `--r`

- [ ] **Step 1: Add the block after the existing `.filter-btn` rules (~line 690)**

Two panes at ≥901px, stacked below. `.work-filter` is `<details>` markup at every width; CSS
forces it open as a column on desktop.

```css
    /* ============================================================
       WORK ARCHIVE — sidebar filter + results pane
       The sidebar reuses .filter-btn so site-ui.js needs no change;
       only the axis of the flex container differs from .filter-bar.
    ============================================================ */
    .work-layout {
      display: grid;
      grid-template-columns: 240px minmax(0, 1fr);
      gap: 28px;
      align-items: start;
    }

    .work-filter {
      position: sticky;
      top: 88px;
      padding: 18px;
      border: 1px solid var(--border);
      border-radius: var(--r);
      background: var(--surface);
    }

    .work-filter > summary {
      font: 700 0.95rem/1 'Outfit', sans-serif;
      color: var(--ink);
      cursor: pointer;
      list-style: none;
    }

    .work-filter > summary::-webkit-details-marker { display: none; }

    .work-search {
      display: block;
      width: 100%;
      height: 38px;
      margin: 14px 0 6px;
      padding: 0 12px;
      border: 1px solid var(--border-2);
      border-radius: var(--r-sm, 8px);
      background: var(--bg);
      color: var(--ink);
      font: 500 0.86rem/1 'Outfit', sans-serif;
    }

    .work-search::placeholder { color: var(--muted); }
    .work-search:focus-visible { outline: 2px solid var(--accent); outline-offset: 2px; }

    .work-filter .filter-bar {
      flex-direction: column;
      align-items: stretch;
      gap: 4px;
      margin: 14px 0 0;
    }

    /* Stacked, left-aligned, with the count pushed to the right edge */
    .work-filter .filter-btn {
      justify-content: flex-start;
      height: 34px;
      padding: 0 10px;
      border-color: transparent;
      border-radius: var(--r-sm, 8px);
      text-align: left;
    }

    .work-filter .filter-btn .filter-count { margin-left: auto; }

    .work-results-head {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      margin-bottom: 18px;
    }

    .result-count {
      margin: 0;
      color: var(--muted);
      font-size: 0.9rem;
    }

    .featured-toggle {
      display: inline-flex;
      align-items: center;
      gap: 6px;
      height: 32px;
      padding: 0 14px;
      border: 1px solid rgba(255,255,255,0.12);
      border-radius: 99px;
      background: transparent;
      color: var(--muted);
      font: 600 0.8rem/1 'Outfit', sans-serif;
      cursor: pointer;
      transition: background 150ms, color 150ms, border-color 150ms;
    }

    .featured-toggle:hover { border-color: rgba(255,255,255,0.28); color: var(--fg); }
    .featured-toggle[aria-pressed="true"] {
      background: var(--accent-dark);
      border-color: transparent;
      color: #fff;
    }

    /* Breadcrumb */
    .crumbs {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin: 0 0 8px;
      padding: 0;
      list-style: none;
      color: var(--muted);
      font-size: 0.85rem;
    }
    .crumbs a { color: var(--muted); text-decoration: none; }
    .crumbs a:hover { color: var(--accent-text); text-decoration: underline; }
    .crumbs li + li::before { content: "›"; margin-right: 8px; }
    .crumbs [aria-current="page"] { color: var(--ink); }

    @media (max-width: 900px) {
      .work-layout { grid-template-columns: minmax(0, 1fr); }
      .work-filter { position: static; }
      .work-filter > summary::after { content: " ▾"; }
      .work-filter[open] > summary::after { content: " ▴"; }
      .work-filter .filter-bar { flex-direction: row; flex-wrap: wrap; }
      .work-filter .filter-btn { justify-content: center; }
      .work-filter .filter-btn .filter-count { margin-left: 6px; }
    }
```

- [ ] **Step 2: Force the disclosure open above 900px**

`<details>` collapses unless `open`. Desktop must always show the sidebar:

```css
    @media (min-width: 901px) {
      .work-filter > summary { pointer-events: none; }
      .work-filter:not([open]) .work-search,
      .work-filter:not([open]) .filter-bar { display: revert; }
    }
```

`display: revert` is not enough on its own — `<details>` hides non-summary children via the
UA stylesheet's `content-visibility`. The reliable route is to ship the element with the
`open` attribute and let the mobile media query allow closing. **Use `<details open>` in the
markup** and drop this step's CSS if the browser check in Task 4 shows the sidebar collapsed
on desktop.

- [ ] **Step 3: Verify no other page is affected**

```bash
cd /Users/chawanpunya/Documents/portfolio
grep -c 'work-layout\|work-filter\|featured-toggle\|crumbs' index.html index-en.html
```
Expected: `0` for both — the classes are new and only the archive uses them.

- [ ] **Step 4: Commit**

```bash
git add assets/home-shell.css
git commit -m "feat: sidebar-archive styles for the work page"
```

---

## Task 2: Keyword and featured predicates in `site-ui.js`

**Files:** Modify `assets/site-ui.js`

**Interfaces:**
- Consumes: the existing `applyFilter(filter, label)` and `matches(card, filter)`
- Produces: nothing new globally; two predicates folded into `applyFilter`

- [ ] **Step 1: Read the current filter block**

```bash
grep -n 'Work filter' -A 60 assets/site-ui.js
```

- [ ] **Step 2: Add the two inputs above `applyFilter`, inside the existing guard**

```js
    const search   = document.getElementById('work-search');
    const featBtn  = document.getElementById('featured-toggle');
    let   activeFilter = 'all';
    let   featuredOnly = false;

    /* Card text is already in the DOM, so the query needs no index fetch.
       Substring and case-insensitive, like the site search — Thai has no
       word spaces, so segmenting would be heavy and error-prone. */
    const haystack = card =>
      (card.textContent || '').replace(/\s+/g, ' ').toLowerCase();

    const matchesQuery = (card, q) => !q || haystack(card).includes(q);
```

- [ ] **Step 3: Fold both into `applyFilter`**

Replace the card loop's condition. The three predicates are AND:

```js
      const q = (search?.value || '').trim().toLowerCase();
      cards.forEach(card => {
        const show = matches(card, filter)
                  && matchesQuery(card, q)
                  && (!featuredOnly || card.dataset.featured);
        if (show) { delete card.dataset.hidden; visible++; }
        else card.dataset.hidden = '';
      });
```

- [ ] **Step 4: Remember the active filter and wire the two controls**

`applyFilter` is currently called only from a button click, so the filter argument was always
fresh. The keyword box and the toggle must re-run it with whatever category is active:

```js
    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        activeFilter = btn.dataset.filter;
        applyFilter(activeFilter, btn.dataset.label || '');
      });
    });

    const rerun = () => {
      const btn = document.querySelector('.filter-btn[data-filter="' + activeFilter + '"]');
      applyFilter(activeFilter, btn?.dataset.label || '');
    };

    search?.addEventListener('input', rerun);
    search?.addEventListener('keydown', e => {
      if (e.key === 'Escape') { search.value = ''; rerun(); }
    });

    featBtn?.addEventListener('click', () => {
      featuredOnly = !featuredOnly;
      featBtn.setAttribute('aria-pressed', String(featuredOnly));
      rerun();
    });
```

The existing `chipClear` handler must also set `activeFilter = 'all'`.

- [ ] **Step 5: Make the count line visible-safe**

`#filter-status` already receives `COPY.some(visible)`. Change the two strings so they read as
a count of the whole archive rather than a bare number:

```js
    const COPY = EN
      ? { none: 'No projects match',        some: n => 'Showing ' + n + ' of ' + cards.length + ' projects' }
      : { none: 'ไม่พบผลงานที่ตรงกับที่ค้นหา', some: n => 'แสดง ' + n + ' จาก ' + cards.length + ' ผลงาน' };
```

- [ ] **Step 6: Syntax check and confirm the homepage is unaffected**

```bash
node --check assets/site-ui.js
```
Then load `index.html` and click every filter button — counts must still equal visible cards
and `ทั้งหมด` must report 13.

- [ ] **Step 7: Commit**

```bash
git add assets/site-ui.js
git commit -m "feat: keyword and featured predicates for the work archive"
```

---

## Task 3: Restructure `work.html`

**Files:** Modify `work.html`

- [ ] **Step 1: Add the breadcrumb and merge the hero**

Replace the hero `<section>` (currently lines ~80–86) with:

```html
    <section class="section" aria-labelledby="work-heading">
      <div class="container">
        <nav aria-label="เส้นทาง">
          <ol class="crumbs">
            <li><a href="/">หน้าแรก</a></li>
            <li aria-current="page">ผลงาน</li>
          </ol>
        </nav>
        <span class="section-label">ผลงาน</span>
        <h1 class="section-title" id="work-heading">ผลงานทั้งหมด</h1>
        <p class="work-problem" style="max-width:60ch;margin-top:10px;">เว็บไซต์ 13 โปรเจกต์และ case study 4 ชิ้น กรองตามประเภทธุรกิจหรือค้นหาด้วยคำก็ได้ — ทุกชิ้นกดเข้าไปดูรายละเอียดและเปิดเว็บจริงได้</p>
      </div>
    </section>
```

- [ ] **Step 2: Copy the `#need` block from `index.html`**

Take the whole `<section class="section" id="need" lang="th" …>…</section>` verbatim and paste
it directly after the hero. Then change the eighth tile's `href="#contact"` — it already
points at an in-page anchor, and Step 4 gives this page one.

- [ ] **Step 3: Convert `#projects` to two panes**

The `.section-label` and `<h2>` go, since the hero above now carries the page's heading. The
nine `.filter-btn` elements move inside the sidebar **unchanged**.

```html
    <section class="section" id="projects" aria-labelledby="projects-heading">
      <div class="container">
        <h2 class="sr-only" id="projects-heading">รายการผลงาน</h2>
        <div class="work-layout">

          <details class="work-filter" open>
            <summary>กรองผลงาน</summary>
            <input type="search" id="work-search" class="work-search"
                   autocomplete="off" placeholder="ค้นหาในผลงาน…" aria-label="ค้นหาในผลงาน" />
            <div class="filter-bar" role="group" aria-label="กรองตามประเภทธุรกิจ">
              <!-- the nine existing .filter-btn buttons, unchanged -->
            </div>
          </details>

          <div class="work-results">
            <div class="work-results-head">
              <p class="result-count" role="status" aria-live="polite" id="filter-status"></p>
              <button type="button" class="featured-toggle" id="featured-toggle"
                      aria-pressed="false">แนะนำ <span class="filter-count">5</span></button>
            </div>
            <p class="active-filter" id="active-filter-chip" hidden>
              กำลังกรอง: <strong id="active-filter-label"></strong>
              <button type="button" id="active-filter-clear" class="active-filter-clear">ล้างตัวกรอง</button>
            </p>
            <div class="works-grid">
              <!-- the 13 existing .work-card articles, unchanged -->
            </div>
            <p class="works-empty" id="works-empty" hidden>ยังไม่มีผลงานในหมวดนี้</p>
          </div>

        </div>
      </div>
    </section>
```

`#filter-status` loses `class="sr-only"` and becomes `.result-count`. It keeps `role="status"`
so the same string serves both audiences.

- [ ] **Step 4: Give the contact section an id**

```bash
grep -n 'class="contact-section"' work.html
```
Add `id="contact"` to it. Without this the eighth need tile is a dead link.

- [ ] **Step 5: Verify the structure before moving on**

```bash
cd /Users/chawanpunya/Documents/portfolio
printf "  filter-btn : %s (9)\n"      "$(grep -c 'class="filter-btn' work.html)"
printf "  work-card  : %s (13)\n"     "$(grep -c 'class="work-card' work.html)"
printf "  need-tile  : %s (8)\n"      "$(grep -c 'class="need-tile"' work.html)"
printf "  #contact   : %s (1)\n"      "$(grep -c 'id="contact"' work.html)"
printf "  sr-only st : %s (0)\n"      "$(grep -c 'sr-only" role="status"' work.html)"
```

- [ ] **Step 6: Commit**

```bash
git add work.html
git commit -m "feat: work.html becomes a sidebar-filtered archive"
```

---

## Task 4: Mirror to `work-en.html`

**Files:** Modify `work-en.html`

- [ ] **Step 1: Apply Task 3 steps 1–4 with English chrome**

Breadcrumb `Home › Work`; summary `Filter work`; placeholder and `aria-label`
`Search within work`; toggle `Featured`; the sr-only heading `Project list`.

- [ ] **Step 2: Copy `#need` from `index-en.html`, not `index.html`**

That file's block is already translated (`Start here`, `What kind of site do you need?`) and
carries **no** `lang="th"` attribute. Copy it as it stands.

- [ ] **Step 3: Verify both files agree structurally**

```bash
cd /Users/chawanpunya/Documents/portfolio
for f in work.html work-en.html; do
  printf "%-14s filter-btn:%s work-card:%s need-tile:%s work-layout:%s contact:%s\n" "$f" \
    "$(grep -c 'class="filter-btn' $f)" "$(grep -c 'class="work-card' $f)" \
    "$(grep -c 'class="need-tile"' $f)" "$(grep -c 'work-layout' $f)" "$(grep -c 'id="contact"' $f)"
done
```
Both rows must read `9 13 8 1 1`.

- [ ] **Step 4: Commit**

```bash
git add work-en.html
git commit -m "feat: work-en.html matches the redesigned archive"
```

---

## Task 5: Cache key

**Files:** Modify the 12 pages requesting `home-shell.css`

- [ ] **Step 1: Add the query string**

```bash
cd /Users/chawanpunya/Documents/portfolio
python3 - <<'PY'
import glob, io
n = 0
for f in sorted(glob.glob('*.html')):
    t = io.open(f, encoding='utf-8').read()
    if 'assets/home-shell.css"' not in t: continue
    io.open(f, 'w', encoding='utf-8').write(
        t.replace('assets/home-shell.css"', 'assets/home-shell.css?v=work-sidebar"'))
    n += 1
print(f'{n} files versioned')
PY
grep -ho 'assets/home-shell.css[^"]*' *.html | sort -u
```
Expected: `12 files versioned`, one distinct string.

- [ ] **Step 2: Commit**

```bash
git add *.html
git commit -m "chore: version home-shell.css so the sidebar styles reach cached visitors"
```

---

## Task 6: Verification

**Files:** none — read-only

- [ ] **Step 1: Filter, keyword and featured compose**

In the browser on `work.html`, with the tab foregrounded:

```js
const btns=[...document.querySelectorAll('.filter-btn')];
const cards=[...document.querySelectorAll('.work-card[data-industry]')];
const q=document.getElementById('work-search'), f=document.getElementById('featured-toggle');
const vis=()=>cards.filter(c=>!('hidden' in c.dataset)).length;
const out=[];
for(const b of btns){ b.click(); out.push([b.dataset.filter, +b.querySelector('.filter-count').textContent, vis()]); }
btns[0].click(); q.value='คลินิก'; q.dispatchEvent(new Event('input',{bubbles:true}));
const afterQuery=vis();
f.click(); const afterBoth=vis();
q.value=''; q.dispatchEvent(new Event('input',{bubbles:true})); f.click();
({countsMatch: out.every(([,c,v])=>c===v), out, afterQuery, afterBoth, restored: vis()===13,
  status: document.getElementById('filter-status').textContent})
```
Required: `countsMatch: true`, `restored: true`, status reads `แสดง 13 จาก 13 ผลงาน`.

- [ ] **Step 2: `index.html` did not regress**

Same count check on `index.html`; `ทั้งหมด` must report 13, not 18.

- [ ] **Step 3: No overflow at 375 × 812**

Iframe recipe on `work.html`, `work-en.html`, `index.html`, confirming `clientWidth === 375`
before trusting the result. Also confirm the sidebar has collapsed into the disclosure.

- [ ] **Step 4: Lighthouse**

`work.html` and `work-en.html`: Accessibility 100, SEO 100, CLS 0, Best Practices failures
exactly `third-party-cookies` and `inspector-issues`.

- [ ] **Step 5: Update `CLAUDE.md`**

The archive's structure, the sidebar-reuses-`.filter-btn` constraint, and the new
`home-shell.css` cache key.

- [ ] **Step 6: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: record the work-archive redesign"
```
