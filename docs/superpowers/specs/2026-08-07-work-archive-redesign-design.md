# Work Archive Redesign — a sidebar-filtered projects page

**Date:** 2026-08-07
**Status:** Approved, ready for implementation planning

## Context

`work.html` / `work-en.html` is the full archive: 13 project cards, a nine-button horizontal
filter bar on one axis (`data-industry`), and four case studies below.

The reference the owner asked to match is `bigzweb.com/projects`. Measured on 2026-08-07,
that page carries: a breadcrumb, six "what kind of site do you need" tiles above the fold,
a persistent left sidebar with a keyword search box, ~21 radio categories and ~20 tag pills,
a two-tab strip (all / featured), a three-column card grid whose cards overlay category chips
on the thumbnail and carry a `VDO` and a `แนะนำ` badge, and `Showing 1 to 12 of 115 results`
with ten pages of pagination.

**That page has 115 projects. This one has 13.** Most of its machinery exists to make 115
items navigable and would misrepresent 13 — a 21-row sidebar where nearly every row reads `1`,
and pagination for a single page, read as *no work yet* rather than *a lot of work*.

The redesign takes what helps at 13 and drops what only pays at 115.

## Goals

1. Give the archive a sidebar filter, an in-page keyword search and a visible result count.
2. Put the industry entry points on the archive page, not only the homepage.
3. Fix the page's existing copy defects, found while surveying (see **D6**).
4. Change nothing about how the 13 cards are authored or tagged.

## Non-goals

- **No second filter axis.** `data-industry` stays the only one. A tag axis would mean
  retagging all 13 projects — content work, and `CLAUDE.md` documents the single axis as
  deliberate.
- **No pagination.** 13 cards, one page.
- **No category chips overlaid on the thumbnail.** Explained in **D5**.
- **No `VDO` badge.** No project has a video.
- **No build step, no framework.** Site convention.
- **The 13 cards' own markup is untouched** apart from where they sit in the DOM.

## Decisions

### D1 — The sidebar reuses `.filter-btn`, and the filter script is not modified

`assets/site-ui.js` was created earlier today and drives the filter on **both** `index.html`
and `work.html`. Its contract is: `.filter-btn[data-filter][data-label]` buttons, each holding
a `.filter-count`, plus optional `#works-empty`, `#filter-status`, `#active-filter-chip`,
`#active-filter-label`, `#active-filter-clear`.

Turning the sidebar into real `<input type="radio">` controls would break `index.html`, which
keeps its horizontal bar. So the sidebar keeps the **same nine `<button class="filter-btn">`
elements, verbatim**, and CSS alone stacks them vertically inside the sidebar. The category
axis therefore needs **zero JavaScript changes** and cannot regress the homepage.

The visual radio dot is a CSS `::before` on `.work-filter .filter-btn`, not a real input.
`aria-pressed` already conveys state, which is correct for a toggle button; adding
`role="radio"` without real radio-group keyboard semantics would be worse than leaving it.

### D2 — Keyword search is a second, independent predicate

A text input above the categories filters the cards by substring against text already in the
DOM: the card's `.work-name`, its `.work-problem` and its `.work-tags`. No fetch, no index —
the data is on the page.

It combines with the category as **AND**: a card shows when it matches the active category
*and* contains the query. Matching is plain substring and case-insensitive, consistent with
the site search, because Thai has no word spaces.

It is labelled `ค้นหาในผลงาน` / `Search within work` so it is not confused with the global
site search in the navbar, which searches all 61 pages.

This is new behaviour and goes in `assets/site-ui.js`, guarded on the input's presence so it
no-ops on `index.html`.

### D3 — The result count becomes visible

`#filter-status` exists but is `.sr-only`. The archive gets a visible line above the grid —
`แสดง 13 จาก 13 ผลงาน` / `Showing 13 of 13 projects` — which is bigzweb's
`Showing 1 to 12 of 115` without the pagination.

The existing `#filter-status` keeps its `role="status"` and stays the single source of the
string, so screen readers and sighted users read the same text and the copy lives in one
place. It loses `.sr-only` on the archive only; `index.html` keeps its hidden one.

Both strings continue to come from `document.documentElement.lang`.

### D4 — A featured toggle, because the data already exists

Five cards on `work.html` carry `data-featured="1"` — the homepage carousel populates from
them. A `แนะนำ` / `Featured` toggle beside `ทั้งหมด` costs one predicate and no content work.

It is a **toggle, not a third filter button**: it narrows whatever the category and keyword
already selected, so the three compose.

### D5 — No category chip on the thumbnail

bigzweb overlays category chips on its card images. Its thumbnails are screenshots with dark
areas that a chip can sit on. These thumbnails are SVG mini-UIs — deliberately detailed, and
newly transcribed — so a chip would cover the preview it exists to show. The cards already
carry three Thai buyer-term tags under the title, which do the same job without occlusion.

### D6 — Fix the page's own copy while restructuring

Found while surveying, not part of the brief:

- The hero says `ผลงานทั้งหมด`, then the section directly below says `ผลงานคัดสรร`
  (*selected work*). This page **is** the full archive; "selected" is the homepage's framing.
- `.section-label` reads `ผลงาน` twice, in the hero and again in `#projects`.
- The hero renders roughly 500 px tall with nothing in it.

The redesign merges the two headings into one hero and drops the duplicate label.

### D7 — The need tiles move onto the archive

The eight `#need` tiles from `index.html` — seven industry pages plus an "ไม่แน่ใจ" tile —
are copied to `work.html` above the grid, matching bigzweb's placement. 2.7 KB of markup, and
`home-shell.css` already carries `.need-tile` and `.need-grid`, so no new CSS.

The eighth tile points at `#contact` on the homepage. `work.html` has its own
`.contact-section` but that section carries **no `id`** — the plan adds `id="contact"` to it
on both archive files, and the tile points there. Without that the tile would be a dead
in-page link.

The tiles' surrounding copy is already translated on `index-en.html` — `Start here`,
`What kind of site do you need?` — so `work-en.html` copies the English block, not the Thai
one. Note `index.html`'s `#need` carries `lang="th"` on the section and `index-en.html`'s
does not; copy each file's own version rather than adding or removing that attribute.

This adds eight internal links to the industry pages from a second indexed page, which is the
reason to do it.

### D8 — Mobile

Below 900 px the sidebar stops being a column and becomes a collapsed `<details>` disclosure
above the grid, labelled `กรองผลงาน`. The nine buttons inside it wrap as they do today.

The `375 × 812` no-horizontal-overflow rule is unchanged and binding.

## Architecture

One page, two panes, no new files:

```
work.html                          assets/home-shell.css        assets/site-ui.js
├── breadcrumb                     + .work-layout (grid)        + keyword predicate
├── hero (merged)                  + .work-filter (sidebar)     + featured predicate
├── #need (8 tiles, copied)        + .work-filter .filter-btn   (both guarded on
└── #projects                      + .work-results               element presence)
    ├── .work-filter  ← sidebar    + <900px details fallback
    │   ├── search input
    │   └── 9 .filter-btn (as-is)
    └── .work-results
        ├── count line
        ├── featured toggle
        └── .works-grid (13 cards, unmoved)
```

`index.html` is not touched. `site-ui.js`'s two new blocks return early when their elements
are absent, the same self-guarding pattern the file already uses.

## Data flow

Card visibility is one function of three independent predicates, evaluated on every change:

```
visible(card) = matchesCategory(card, activeFilter)
              && matchesQuery(card, searchValue)
              && (!featuredOnly || card.dataset.featured)
```

`applyFilter()` in `site-ui.js` already owns `matchesCategory` and the `data-hidden`
attribute that hides a card. The two new predicates fold into the same function so there is
one place that decides visibility and one place that writes the count.

Counts on the nine buttons stay derived from the DOM at load, as today — they describe the
category axis alone and do not react to the keyword, which is what makes them stable labels
rather than a moving target.

## Error handling and edge cases

| Case | Behaviour |
|---|---|
| Query matches nothing | `#works-empty` shows; count line reads `แสดง 0 จาก 13 ผลงาน` |
| Category + query disagree | Empty state, same as above — the predicates are AND by design |
| JavaScript disabled | All 13 cards render; the sidebar shows but does nothing. The static `.filter-count` values are the no-JS fallback, as today |
| Clearing the query | Restores whatever the category and featured toggle still select |
| `Escape` in the search box | Clears the query and restores the previous selection |

## Testing

Automated checks cannot see an invisible card — `work.html` shipped once with all 13 at
`opacity: 0` and passed Lighthouse, the overflow recipe and the dead-link sweep. So:

1. **Every filter button's count equals its visible cards**, `ทั้งหมด` reports 13 not 18.
2. **The three predicates compose** — category + query + featured together, then cleared.
3. **`index.html`'s filter still works**, since it shares `site-ui.js`.
4. **Keyboard**: the search box is reachable, `Escape` clears, the clear-chip returns focus.
5. **No overflow at 375 × 812** with `clientWidth === 375` confirmed first — `resize_window`
   silently does nothing in this environment; use the iframe recipe.
6. **The sidebar collapses below 900 px** and the grid goes single-column.
7. **Lighthouse**: Accessibility 100, SEO 100, CLS 0. Best Practices caps at 77 (Clarity
   cookies) — a known, accepted exception.
8. **`work-en.html` reports in English**, `work.html` in Thai, from `<html lang>`.
9. **Bump `assets/home-shell.css`'s cache key.** Verified 2026-08-07: all 12 pages request it
   as `assets/home-shell.css` with **no query string at all**, so a returning visitor would
   pair new HTML with a stale stylesheet and see an unstyled sidebar. This exact failure
   already happened once today with `portfolio-pages.css?v=ghdark-2`, where three edits
   shipped behind an unchanged key. Give it one — `?v=work-sidebar` — on all 12.

## Files touched

**Modified:** `work.html`, `work-en.html`, `assets/home-shell.css`, `assets/site-ui.js`,
the 12 pages that request `home-shell.css` (cache key only), `CLAUDE.md`

**Untouched:** `index.html` / `index-en.html` beyond the cache key, all 13 card bodies,
`search-index.json`, `sitemap.xml` (no new URLs), the demo pages

## What is expected to change

| Change | Effect |
|---|---|
| Horizontal filter bar → sidebar | Same nine filters, no script change |
| Keyword search | New; narrows within the archive |
| Visible result count | `#filter-status` stops being `.sr-only` here |
| Featured toggle | Uses the existing `data-featured` |
| 8 need tiles | +8 internal links to the industry pages |
| Hero merge | Removes a duplicate label and a contradictory heading |
| Pagination | None — deliberately |
