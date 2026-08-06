# Lean Code — Removing Duplication Without a Build Step

**Date:** 2026-08-06
**Status:** Approved, ready for implementation planning

## Context

The site is 81 HTML files totalling 2.1 MB. It has no build step by design, so every shared
element — navigation, footer, search widget, behaviour scripts — is physically repeated in
every file that needs it. That was a deliberate trade: the site stays inspectable and
deployable by pushing files, at the cost of duplication.

The duplication has now grown past the point where it pays for itself. Measured:

| What | Repeated in | Size |
|---|---|---|
| The 13 project cards | 4 files (`index`, `index-en`, `work`, `work-en`) | 68 KB each |
| — of which CSS mini-UI thumbnails | | **67% of card weight** |
| Nav markup | 75 files | |
| Search markup | 61 files | ~11 lines each |
| Footer markup | 57 files | |
| Behaviour scripts (reveal / nav toggle / filter) | 21 blocks | **1,844 lines** |

`index.html` and `work.html` carry byte-identical copies of all 13 cards: **110 KB stored
twice across the two language pairs** purely because both pages show the same grid.

## Goals

1. Cut duplication that has to be maintained by hand — the same edit should not require
   touching 4, 21 or 61 files.
2. Cut bytes shipped to visitors, particularly on `index.html` (151 KB).
3. Change nothing a visitor can see.

## Non-goals

- **No build step.** Confirmed as a constraint, not a default. The site keeps its
  "edit a file, push, done" character — no `npm install`, no generated output, no Actions
  workflow beyond the existing Pages deploy.
- **Nav stays in HTML.** Rejected twice already, and for the same reason both times: the
  internal link graph is what the 7 industry pages need in order to rank. Moving it into JS
  removes those links from the source.
- **Card content stays in HTML.** Project names, descriptions and tags are the site's primary
  content. Only the *thumbnail* moves out.
- **No visual redesign.** This is a structural change with a zero-visible-difference bar.
- **Footer stays as it is.** Explained below — it was in scope until it was measured.

## Decisions

### D1 — Thumbnails become SVG files

10 of the 13 cards build their thumbnail from inline-styled `<div>`s: 2.2–6.3 KB and 18–45
elements each. Three already use `<img>`.

**The pattern already exists on this site.** `BuildNest` loads
`assets/thumbs/construction-landing.svg` — a 6.2 KB standalone SVG with `<title>`, `<desc>`,
`role="img" aria-labelledby`, and a `<defs><style>` block using `oklch()` colours. The
conversion has been done successfully once; this repeats it.

Measured: the 10 `<div>` thumbnails total **41.9 KB per file**. Removing them from all four
files is **−168 KB of HTML**, replaced by 10 SVG files the browser fetches once and caches
across every page.

The other three cards already use `<img>`: `BuildNest` (the existing SVG), `VELVÉ` (a real
photo, stays), and `BRIGHT Dental` (a remote Unsplash URL — see **D7**). `BRIGHT` gains an
SVG too, making 11 new files in total, but it contributes **no HTML saving** since it is
already an `<img>`; its benefit is removing a third-party request.

### D2 — Thumbnails are converted from measured geometry, not redrawn

The mini-UIs use `display:flex` and `position`. SVG has neither; it uses absolute coordinates.
Redrawing 10 of them by eye is 10 chances to drift.

Instead, the browser resolves the layout and the conversion reads the result:

1. Load the page, force `.work-thumb` to 1200×750 (the SVG viewBox the existing file uses).
2. For every element inside it, read `getBoundingClientRect()` plus the computed
   `background`, `borderRadius`, `color` and `fontSize`.
3. Emit a `<rect>` or `<text>` at those exact coordinates.
4. Render the result and compare against the original.

Flexbox is resolved to numbers *before* anything is transformed, so this is a transcription
rather than an interpretation.

### D3 — A card that does not convert cleanly stays a `<div>`

Per-card acceptance:

| Check | Threshold |
|---|---|
| Shape count | equals the number of elements with a background or border |
| File size | ≤ 8 KB (the existing `construction-landing.svg` is 6.2 KB) |
| Visual | screenshots compared side by side, per card, by eye |
| Accessibility | `<title>` + `<desc>` + `role="img"`, matching the existing file |

There is no requirement to convert all 10. Seven cards is already −118 KB. A card that will
not transcribe faithfully keeps its `<div>` thumbnail and the work moves on.

### D4 — Behaviour scripts move to `assets/site-ui.js`

1,844 lines across 21 inline `<script>` blocks implement three behaviours:

- the `.reveal` IntersectionObserver (12 files)
- the mobile nav drawer toggle (15 files)
- the industry filter bar (4 files)

They are byte-identical copies. One file, three self-guarding blocks — each returns early if
its elements are absent — and pages include `<script src="assets/site-ui.js" defer></script>`.

This is the highest-value and lowest-risk item in the spec: the code already behaves
identically everywhere, so moving it cannot change behaviour, only location.

It also removes a whole class of bug. `work.html` shipped with all 13 cards at `opacity: 0`
because the reveal observer was not copied along with the filter block — see the plan-2
completion note. With one shared file there is nothing to forget to copy.

### D5 — Search markup collapses to a placeholder

61 files carry ~11 lines of identical search widget markup. `site-search.js` already runs on
every one of them, so it can build its own DOM:

```html
<div class="site-search"></div>
```

Placement stays explicit in the HTML — the script fills a placeholder rather than guessing
where the widget belongs, because it sits inside `.nav-inner` on one page family, inside
`.page-shell nav` on the other, and inside `.nav-mobile-panel` as a second instance.

Roughly 610 lines removed. Safe for SEO: the widget is a control, not content. This is the
opposite call to the nav, and deliberately so — the nav carries links Google should follow.

### D6 — The footer stays in HTML

This was in scope until it was measured, and the measurement reversed it:

| Variant | Files | Links |
|---|---|---|
| `footer-band` | 45 | **0** |
| `footer-section` | 12 | 13 |

The variant repeated 45 times is two `<span>`s of text with no links — the savings are a few
hundred lines. The variant with real links, and therefore real SEO value, is in only 12 files
and should stay in the source anyway. Neither case justifies moving the footer into JS.

### D7 — `BRIGHT Dental`'s remote image becomes a local SVG

Found while surveying, not part of the original brief. That card's thumbnail is:

```html
<img src="https://images.unsplash.com/photo-1728342057953-...">
```

Every visitor to the homepage makes a third-party request to `images.unsplash.com`. The site
otherwise depends on nothing external except Google Fonts and Microsoft Clarity, both
deliberate. This one is not — it is a placeholder that was never replaced, and it breaks if
Unsplash changes anything.

It converts to an SVG alongside the other 10, which removes the request as a side effect.
Fixing it while the cards are already open is cheaper than a separate pass.

## What is expected to change

| Change | Effect |
|---|---|
| 10 `<div>` thumbnails → SVG files | **−168 KB of HTML**, replaced by cached SVG |
| `BRIGHT Dental` → local SVG (11th file) | no byte change; one fewer third-party request |
| Scripts → `assets/site-ui.js` | **−1,844 duplicated lines** |
| Search markup → placeholder | **−610 duplicated lines** |
| Footer | unchanged — measured, does not pay (**D6**) |

`index.html` should drop from 151 KB to roughly 100 KB.

## Files touched

**Created:** ~11 files in `assets/thumbs/`, `assets/site-ui.js`

**Modified:** `index.html`, `index-en.html`, `work.html`, `work-en.html` (thumbnails), the 21
files carrying inline behaviour scripts, the 61 files carrying search markup,
`assets/site-search.js` (gains the markup builder), `CLAUDE.md`

**Untouched:** all nav markup, all card text content, all footers, `portfolio-pages.css`,
`home-shell.css`, the 13 demo pages

## Verification

Nothing a visitor sees may change. The bar is stricter than usual because this is a pure
refactor: a passing Lighthouse score is not evidence that the page still looks right.

1. **Per-card visual comparison.** Screenshot the original thumbnail and the SVG at the same
   size and compare by eye, one card at a time. A card that differs keeps its `<div>` (D3).
2. **Cards still render.** After the script move, confirm on `index.html` and `work.html` that
   all 13 cards reach `opacity: 1` after scrolling — the exact failure that shipped once
   already and that every automated check passed through.
3. **Search still works** on one page from each stylesheet family, including the keyboard path.
4. **Filter still works**: every button's count equals its visible cards, "ทั้งหมด" reports 13
   and not 18.
5. **Mobile drawer still opens** on a page from each family.
6. **Lighthouse** across a sample of every page type: Accessibility 100, SEO 100, CLS 0.
   Best Practices caps at 77 (Clarity cookies); `404.html` caps at SEO 66 (`noindex`).
7. **No overflow at 375×812**, using the iframe recipe with `clientWidth === 375` confirmed
   first — `resize_window` silently does nothing in this environment.
8. **No remaining third-party image requests**:
   `grep -rn 'src="https\?://' *.html` returns nothing outside the known font and analytics tags.
9. **Byte count before and after**, recorded, so the change can be judged against its purpose.
