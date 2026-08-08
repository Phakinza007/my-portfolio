# Design Preview Widget — "เว็บของคุณจะหน้าตาแบบนี้"

**Date:** 2026-08-08
**Status:** Approved, ready for implementation planning
**Scope of this spec:** `web-clinic.html` only. Seven remaining `web-*.html` pages are a
follow-on that adds data, not code.

## Context

The eight `web-*.html` industry pages sell a package by describing it. A buyer reading
`web-clinic.html` learns the price, the scope, the process and the FAQ — and can see three
finished clinic designs in `#related`. What they still cannot see is **what their own site
would contain**: which pages, in what order, holding what.

The reference the owner asked to match is `bigzweb.com/recommend/realestate`, read on
2026-08-08. Its section order is:

1. `#recommend-hero` — breadcrumb + `<h1>`
2. "ระบบนี้ช่วยธุรกิจคุณยังไง"
3. `#proof-strip` — "ผลงานจริงในหมวดอสังหาริมทรัพย์"
4. `#recommend-content` — "เว็บของคุณจะหน้าตาแบบนี้" + "ผลงานทั้งหมดในหมวดนี้"

**The owner asked to invert 3 and 4**: the preview comes first, real work follows it. The
reasoning is the preview answers "what do I get", and the portfolio then answers "can he
actually build it" — objection, then proof.

### Anatomy of the reference widget, as measured

| Part | What it actually is |
|---|---|
| Header | Circular icon badge + `<h2>` + one muted line: "ภาพจำลองดีไซน์จริง ไม่ใช่หน้ารอโหลด" |
| Legend | `● หน้าฝั่งลูกค้า` (purple) · `● หน้าฝั่ง Admin` (amber), plus a right-aligned "กดเลือกหน้าเพื่อดูตัวอย่าง" |
| Frame | Browser chrome — three dots, a URL pill, a "ตัวอย่างดีไซน์" badge at right |
| Sidebar | 9 `<button>`s — 7 customer-facing, 2 admin |
| Preview pane | **Rendered DOM, not a screenshot.** Grey boxes labelled `ภาพ` stand in for photography |
| Caption | `<h3>` page name + audience badge + description + `ส่วนประกอบ:` chips |

Two properties of the reference are defects and are **not** copied:

- **No `aria-selected` or `aria-pressed` on any of the nine buttons.** A screen reader user
  cannot tell which page is active. This site holds Lighthouse Accessibility at 100 and the
  archive sidebar already documents the toggle-state lesson (`aria-pressed`, not `role=radio`
  without keyboard semantics). This widget is a genuine tab pattern and gets real tab
  semantics.
- **All nine captions pre-rendered into the DOM and hidden with `.hidden`.** Fine for one
  page; multiplied across eight industry pages it is the duplication this repo has twice
  spent effort undoing (72 copies of the search markup collapsed to one placeholder; 161.5 KB
  of card `<div>`s transcribed to SVG).

One property is correct and **is** copied: the responsive strategy. The layout is
`flex flex-col md:flex-row`; the sidebar is `md:w-56` on desktop and becomes a horizontal
`overflow-x-auto` chip strip on mobile. The scroll is contained inside the widget, which is
what keeps the page itself from scrolling horizontally.

## Goals

1. Show a clinic buyer the pages their site would contain, browsable one at a time.
2. Say what each page is for and what it is made of, in the page's own words.
3. Ship one renderer that the other seven industry pages can reuse by adding data only.
4. Hold every existing site standard: Lighthouse 100/100/100, `canScrollX: false` at 375px,
   CLS 0, full keyboard operation.

## Non-goals

- **No second industry.** `clinic` data only. The other seven are a follow-on.
- **No `-en` twin.** `web-*.html` is Thai-only by design; see the bilingual rules in
  `CLAUDE.md`.
- **No multi-slide previews.** The reference carries `1 · 2 · 3` slide dots per page. Dropped
  under YAGNI — more machinery, no additional selling.
- **No real interactivity inside the mockup.** Nothing inside the preview pane is clickable.
  It is an illustration.
- **No screenshots.** The pane is built from data. Nothing is photographed, so nothing has to
  be re-photographed when copy changes.
- **No new stylesheet file.** The `.dp-*` block is appended to `assets/portfolio-pages.css`.
- **`#related`, `#faq`, `#cta` keep their content.** `#related` moves in the DOM; its markup
  is untouched.

## Truthfulness constraints

These are requirements, not style preferences. `CLAUDE.md` records that this site strips
claims it cannot back — the `ลูกค้าจริง` tag was removed from twelve files, PDPA copy is
withheld "until it is true", and the RAAT case study states that no metrics were recorded
rather than substituting a number.

**T1 — The admin track is not included in ฿3,900.** The owner chose the customer/admin axis
over a package-tier axis after the contradiction was raised. The page's own FAQ says
"เริ่มต้น ฿3,900 สำหรับเว็บหน้าเดียว", and an audit on 2026-08-08 confirmed **no `<form>` in
the repository carries an `action`** and no page makes a backend call. Therefore every admin
entry carries a visible badge reading **`งานเพิ่มเติม · ประเมินราคาแยก`**, in the caption, in
text — not conveyed by the amber dot alone.

**T2 — The customer track must not read as "six separate pages for ฿3,900".** The ฿3,900
package is one page of up to six sections; ฿9,900 buys 3–5 pages. The widget presents the
entries as **ส่วนของเว็บ**, and the header line states the scope: sections of a one-page site
at ฿3,900, separate pages from ฿9,900 up.

**T3 — The mockup is labelled as a mockup.** The subtitle says so, and the frame carries a
`ตัวอย่างดีไซน์` badge. No claim that any clinic uses this design.

**T4 — The brand is fictional and obviously so.** The mockup brand is **"คลินิกของคุณ"** and
the URL pill reads `คลินิกของคุณ.com`. It cannot be mistaken for a client, and it does not
collide with LUMI / BRIGHT / VELVÉ, which appear in `#related` directly below.

## Design

### D1 — Placement

New `<section class="section" id="preview">` between `#process` and `#related`. Final order:

```
hero → #problem → #overview → #included → #compare → #process
     → #preview  ← new
     → #related  ← moved to sit directly after the widget
     → #faq → #cta
```

`#related` is moved, not rewritten. Its heading (`ตัวอย่างงานออกแบบ` /
`ตัวอย่างเว็บคลินิกที่ผมออกแบบไว้`) already reads correctly as the answer to the widget.

Section banding does not apply — that rule is `main > section:nth-of-type(even)` on
home-shell pages. `web-*.html` uses `portfolio-pages.css`, where `.section` is unbanded.
Inserting a section here shifts nothing.

### D2 — Markup is a placeholder

The page ships one empty element and one script tag:

```html
<section class="section" id="preview">
  <div class="page-shell">
    <div class="design-preview" data-preview="clinic"></div>
  </div>
</section>
```

```html
<script src="assets/design-preview.js?v=1" defer></script>
```

The script builds everything else. This is the established pattern — `site-search.js` fills
`<div class="site-search"></div>` the same way, and the versioned query string exists for the
same reason: **a returning visitor pairing new HTML with a cached older script gets an empty
placeholder and no widget at all.** Bump `?v=` on any change to the generated markup.

The script self-guards: if `.design-preview` is absent it returns immediately, so the same
file is harmless on any page that loads it.

### D3 — Data lives in JSON

`assets/design-preview.json`, keyed by the `data-preview` value:

```json
{
  "clinic": {
    "brand": "คลินิกของคุณ",
    "url": "คลินิกของคุณ.com",
    "note": "฿3,900 คือเว็บหน้าเดียวรวมส่วนเหล่านี้ — แยกเป็นหลายหน้าเริ่มที่ ฿9,900",
    "pages": [
      {
        "id": "services",
        "side": "customer",
        "name": "บริการ + ราคา",
        "desc": "แยกบริการเป็นหมวด พร้อมช่วงราคาที่ชัดเจน ลดคำถามซ้ำทางไลน์",
        "parts": ["การ์ดบริการ", "ช่วงราคา", "ปุ่มจองต่อบริการ"],
        "blocks": [
          { "t": "nav", "links": ["บริการ", "ทีมแพทย์", "ติดต่อ"], "cta": "จองคิว" },
          { "t": "head", "title": "บริการของเรา" },
          { "t": "cards", "cols": 3, "items": [
            { "title": "ฟิลเลอร์", "meta": "45 นาที", "price": "฿8,000–15,000" }
          ]}
        ]
      }
    ]
  }
}
```

Fetched **lazily on `IntersectionObserver`**, not at page load — the widget sits well below
the fold and must not compete with LCP. This mirrors the search index, which is fetched on
first focus for the same reason.

`brand` and `url` are data, so T4's fictional name changes in one place.

### D4 — Nine block types render every industry

The renderer knows a fixed vocabulary. Clinic uses all of them; the remaining seven
industries were checked against this list and need no additions.

| `t` | Renders |
|---|---|
| `nav` | Brand wordmark, link labels, one filled CTA pill |
| `hero` | Headline, sub-line, CTA pair, optional image placeholder |
| `head` | Section title inside the mockup |
| `cards` | 2–3 column grid; each card is image placeholder + title + meta + price |
| `list` | Stacked rows — opening hours, service lists |
| `form` | Field boxes with labels + a submit pill (inert) |
| `gallery` | Image-placeholder grid, used for before/after |
| `map` | Wide placeholder with a pin glyph + address lines |
| `table` | Header row + body rows — the admin views |

Image placeholders are grey blocks labelled `ภาพ`, as in the reference.

**Adding an industry in the follow-on is data only.** If a future industry needs a tenth
block type, that is a code change and should be called out as one.

### D5 — The mockup wears the portfolio's own theme

Owner's decision. The pane is built from the tokens already in `portfolio-pages.css`:
`--bg`, `--surface`, `--surface-2`, `--line`, `--ink`, `--ink-2`, `--muted`, `--accent`,
`--accent-text`, `--r`, `--r-sm`. **No new colours are defined.**

Two consequences, both good:

- Contrast is inherited from a palette already audited at AA. The reference's `ภาพ`
  placeholder text is very low contrast and cannot be copied as-is; using `--muted` on
  `--surface-2` keeps it measurable.
- The widget cannot drift from the rest of the page when tokens change.

The browser chrome reuses the **existing** `.browser-frame`, `.browser-frame-bar`,
`.browser-dot`, `.browser-dot-red|amber|green` and `.browser-url` classes verbatim. They
already exist in `portfolio-pages.css` and already look like the reference's frame.

### D6 — Accessibility

- The sidebar is a real tab pattern: `role="tablist"` on the container, `role="tab"` +
  `aria-selected` + `aria-controls` on each button, `role="tabpanel"` + `aria-labelledby` on
  the pane. Roving `tabindex`; ArrowLeft / ArrowRight / Home / End move selection.
  `CLAUDE.md` warns against adding ARIA roles without the keyboard semantics they imply —
  so the keyboard handling is part of this, not a follow-up.
- **`role="tabpanel"` wraps the caption, and the mockup sits inside it as
  `aria-hidden="true"`.** Getting this the wrong way round is the easy mistake: if the panel
  were the mockup, the panel would be an empty shell and the caption — the only real content —
  would sit outside the tab relationship entirely.
  `aria-hidden` on the mockup is the legitimate use of it: an illustration of a website whose
  meaning is carried in full by the caption beside it — page name, purpose, component list,
  all real text. This is the opposite of the VELVÉ defect, where `aria-hidden` was used to
  *suppress* a visible string from an accessible name and `label-content-name-mismatch` kept
  firing. Nothing in the mockup is an interactive control, and nothing is being hidden from a
  name computation.
- **No `aria-live`.** A correct tab pattern already announces the switch through
  `aria-selected` and the panel relationship; adding a live region on top double-announces.
- Every mockup glyph is decorative and `aria-hidden`.
- The amber dot never carries meaning alone — T1's badge is text.

### D7 — Responsive

- **≥900px:** `flex-direction: row`; sidebar fixed at 224px, pane fills the rest.
- **<900px:** `flex-direction: column`; the sidebar becomes a horizontal chip strip with
  `overflow-x: auto` and a bottom hairline. The scroll is **contained inside the widget** —
  this is what preserves `canScrollX: false` on the page.
- The mockup is fluid, built from the same responsive rules as the rest of the sheet. It is
  **not** scaled with `transform: scale()`, which would produce unreadable text at 375px.
- `cards` drops to a single column below 640px; `table` gets its own `overflow-x: auto`.
- The placeholder reserves its height before the JSON arrives, so **CLS stays 0**.

### D8 — Analytics

One new delegated classification in `assets/analytics.js`:

```
preview_page  { industry: 'clinic', page: '<id>', side: 'customer' | 'admin' }
```

This answers a question nothing on the site can answer today: which page of a prospective
site buyers actually want. If `จองคิวออนไลน์` and the admin views dominate, that is direct
evidence for the booking-system work the owner is weighing.

Consistent with the existing pattern — one delegated listener, no per-button markup. Note
that Clarity does not load on localhost, so verify locally with `?cl_debug`.

## Files touched

| File | Change |
|---|---|
| `assets/design-preview.js` | New. Renderer, tab keyboard handling, lazy fetch, self-guard |
| `assets/design-preview.json` | New. `clinic` entry only |
| `assets/portfolio-pages.css` | Append the `.dp-*` block at the end, as `.story-*` did |
| `web-clinic.html` | Add `#preview`; move `#related` below it; add the script tag |
| `assets/analytics.js` | Add `preview_page` |
| `CLAUDE.md` | See below |

### CLAUDE.md corrections this change forces

1. **"no page in this family has ever needed new CSS"** stops being true. Rewrite to record
   that the `.dp-*` block was appended to `portfolio-pages.css` — no new file, no new
   colours — and that everything else in the family still needs none.
2. The industry-page recipe gains `#preview` in its section list, placed before `#related`.
3. The site-search entry documents one versioned self-rendering script; a second now exists.
   Note `design-preview.js?v=` and the identical cache-pairing hazard.

## Acceptance

Run before committing, not after:

1. `python3 _tools/serve.py 8123` — **not** `http.server`, which cannot resolve the
   extensionless URLs this site uses.
2. `npx -y lighthouse http://localhost:8123/web-clinic` mobile and `--preset=desktop`.
   Accessibility 100, SEO 100, Performance 100. Best Practices is capped at 77 sitewide by
   Clarity's third-party cookies — that one is expected; any *other* deduction is a
   regression.
3. Read the per-audit failures, not the category score. `label-content-name-mismatch` has
   weight 0 and the score stays 100 while failing.
4. 375 × 812: `canScrollX: false`, and the sidebar strip scrolls inside its own box.
5. Keyboard only: Tab reaches the tablist, arrows move between all eight pages, Home/End
   jump to the ends, and a screen reader announces the newly selected page's caption once —
   not twice (see **D6**).
6. Load the page with `assets/design-preview.js` blocked. The widget must be absent, not
   broken — no empty frame, no reserved gap.
7. Confirm `#related` still renders its three cards unchanged in its new position, and that
   no anchor anywhere in the file points at a section id that moved.

## Follow-on, not in this spec

- The seven remaining `web-*.html` pages — data only, same renderer.
- The three category pages (`landing-page`, `dashboard-ui`, `business-website`). These have
  `-en` twins, so the JSON would need `th` / `en` keys the way `search-index.json` does.
- Whether the admin track ever stops being `งานเพิ่มเติม`. That depends on the booking-backend
  work under separate consideration; until it ships, T1 stands.
