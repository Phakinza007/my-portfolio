# Homepage: give it a scale, and something to look at

**Date:** 2026-08-31
**Scope:** `index.html`, `index-en.html`, `assets/home-shell.css`
**Status:** approved design, implementing

---

## Why

The owner asked how to make the site more attractive, then narrowed it: both
"more people contact me" and "it looks better", homepage first.

The homepage is not ugly. It is **flat**, and the flatness is measurable.
Measured 2026-08-31 at 1440px in a real browser with Bai Jamjuree actually
loaded and every `.reveal` neutralised:

| section | height | % of page |
|---|---|---|
| hero | 663px | 6.6% |
| need | 481px | 4.8% |
| testimonials | 529px | 5.3% |
| **projects** | **3,949px** | **39.6%** |
| about | 624px | 6.3% |
| case-studies | 1,284px | 12.9% |
| services | 811px | 8.1% |
| stack | 523px | 5.2% |

Total 9,983px. Four findings, none of them about taste:

**1. The page has exactly one scale.** 32 `<img>` in `main`, and 30 of them are
the same 351 × 220 card thumbnail. Nothing on this page is ever large. The eye
is given no place to land, top to bottom, for ten thousand pixels.

**2. Every section head is the same gesture, and 61–79% of it is empty.**
Measured against the 1100px container:

| section | heading text width | container | used |
|---|---|---|---|
| `#projects` | 231px | 1100px | 21% |
| `#case-studies` | 244px | 1100px | 22% |
| `#services` | 268px | 1100px | 24% |
| `#testimonials` | 369px | 1100px | 34% |
| `#need` | 422px | 1100px | 38% |

Eight sections, eight identical openings: optional `.section-label`,
left-aligned `.section-title`, then a grid. The right column is empty every
time.

**3. 52 boxed containers in `main`, all one recipe** — 1px `--border`, `--r`
radius, `--surface` fill, on a background 1.06–1.09 contrast away. This is the
same condition the `.industry-page` pass fixed in 2026-08-09 (29 boxes → 3) and
the showcase story stack fixed on 2026-08-24. The homepage never got that pass.

**4. The package comparison starts ~78% down the page.** The `฿3,900` figure is
in the hero, so a visitor is not left guessing — but "which of the three do I
want" is answered last, after 7,500px.

This is exactly what `.impeccable/critique/2026-08-09…` named and scored 2/4 on
*Aesthetic and Minimalist Design*:

> For a portfolio the design is the product, and this one is currently competing
> on tidiness. A visitor sees a well-run system rather than a point of view.

Three of that critique's findings have since been fixed — Bai Jamjuree replaced
the Inter monoculture, 44 kickers were deleted, and the showcase template was
rebuilt work-first. **The homepage was never in scope for any of them.**

## What this is not

Approach B (reorder the page so price comes earlier, shrink `#projects` from 18
cards to 6) was offered and **not** chosen. Section order is unchanged here.
Approach C (a second surface, a signature visual language, scroll motion) was
also offered and deferred — it is better work once the page has a scale to hang
it on.

## The design

Four moves. Every one of them is a pattern this repo already runs somewhere
else; none invents a component.

### 1. `.section-head` — a two-column head, on four sections only

A grid: heading in the left cell, one piece of **real content** in the right.
Not decoration — a link or a line that was already on the page, moved up into
the space that was empty.

| section | right cell |
|---|---|
| `#need` | the `.need-sub` line, moved out of the stack |
| `#projects` | `ดูผลงานทั้งหมด 18 ชิ้น →` to `work` |
| `#case-studies` | `ดูทั้งหมด →` to `work#case-studies` |
| `#services` | `เทียบ 3 แพ็กเกจแบบเต็ม →` to `services` |

This is `portfolio-pages.css`'s `.section-heading` + `.heading-link` pattern,
which the eight `web-*` pages already run, ported to `home-shell.css`.

**Four, not eight.** The goal is to break a uniform, not to install a new one.
`#testimonials` gets a different treatment (below), and `#about` and
`.stack-sec` already have shapes of their own — `#about`'s h2 is a `.card-title`
inside its bio card, which is why it measured 86px wide rather than 231–429px.
After this change the page opens four different ways instead of one.

`.section-title` keeps its 36px bottom margin when it stands alone; inside
`.section-head` the wrapper carries the margin and the title zeroes it.

Below 760px the grid collapses to one column and the right cell falls under the
heading, which is where it reads anyway on a phone.

### 2. `.work-lead` — one project, at three times the area of any other

`#projects` opens with **RAAT** at ~660px wide, unboxed, image left and text
right.

Three reasons it is RAAT and not one of the seventeen demos:

- It is **the only real client work on the site**, and the only card that may
  carry the `ลูกค้าจริง` tag. Leading the work section with it is the strongest
  sales moment available and it is true.
- `assets/raat/competition-calendar.jpg` is **the only photograph among the 18
  cards** (VELVÉ's is the other, but it sits in the grid). At 660px it renders
  at 702 × 440 native — no upscaling — and it introduces the only photographic
  surface on a page that is otherwise 30 flat SVG mini-UIs.
- It already appears in two places deliberately (`#projects` grid and the fifth
  `#case-studies` card), so a third placement is a decision this page has
  already made once, not a new one.

It is **not a `.card`**: no border, no fill, no radius on the container. The
photograph is the surface. That is the move that makes it read as a different
kind of thing rather than a bigger version of the same thing.

The RAAT `.work-card` **stays in the grid**. Removing it would change the
`ทั้งหมด 18` and `other 5` filter counts, which are hand-maintained in four
files, and would take the card out of the `other` filter. Duplication on this
page is established — BuildNest, BookEase and LUMI each already appear in both
`.hero-work` and the grid.

### 3. The price becomes the largest thing in `#services`

`.card-price` is 1.5rem today, smaller than the `.section-title` above it and
barely larger than the `.card-title` beside it. Scoped to `#services` it goes to
`clamp(2rem, 3.4vw, 2.6rem)` with `font-variant-numeric: tabular-nums`, so the
three figures align down the column and the section can be read by price alone.

The figures themselves are **unchanged** — ฿3,900 / ฿7,900 / ฿9,900, and the
`.card-note` escalation lines stay verbatim. These are live Fastwork listings
and the category pages state the same numbers.

### 4. De-box what is not a control and not a card with a picture

`border` is this site's signal for "this is a control" (CLAUDE.md, the
`.tag-btn` finding). Applying that rule honestly to the homepage:

| element | verdict |
|---|---|
| `#testimonials .card` × 3 | **de-box** — not clickable, and a four-word quote in a 350px filled box is a box around nothing |
| `#services .card` × 3 | **de-box** into ruled columns, same move as `.industry-page`'s `.study-meta` |
| `#about` experience card | **de-box** — a list of three entries, not a control |
| `.work-card`, `.case-card` | **keep** — clickable, and the border is what makes the thumbnail read as a target |
| `.need-tile`, `.filter-btn` | **keep** — controls |
| `#about` bio card | **keep** — one boxed card left in that section reads as a portrait, not as texture |

Seven boxes go. The point is not the count; it is that after this, a box on the
homepage means something.

`.card` itself is **not touched** — `faq.html` ships ten of them and they are
correct there. Both changes are scoped by section id, which is the same
mechanism `#compare` / `#stack` already use in `portfolio-pages.css`.

⚠️ That mechanism carries a known trap, recorded on `#compare`: **an id selector
out-specifies a class inside a media query.** Any responsive override for these
must be written at the same or higher specificity, or the desktop rule will win
on a phone.

## Testing

- `canScrollX: false` at 375 × 812 on `index` and `index-en` — and, because
  `.work-lead` and `.section-head` both introduce two-column grids, a per-element
  right-edge sweep as well, not just `canScrollX`. `html, body { overflow-x:
  hidden }` hides the exact failure `construction-landing`'s CTA shipped with.
- Lighthouse on both files, mobile and desktop. Accessibility and SEO must stay
  100. `heading-order` is the one to watch: nothing here removes an `h2`, but
  `.work-lead`'s project name must not be one.
- `python3 _tools/check-deploy.py` — `home-shell.css` is versioned
  (`?v=hero-work`) and changing it without moving the token ships new markup
  against a cached stylesheet for every returning visitor.
- `python3 _tools/check-copy.py` — the RAAT blurb in `.work-lead` is the 64th
  copy of a string that already lives in 203 locations across 84 files, and the
  canonical for RAAT is the **minority** wording (`ส่งมอบ ก.ค. 2026 และยังใช้งานอยู่`),
  which is the one the owner actually confirmed.
- Re-measure the section table above and the box count. The claim is scale
  contrast; a rebuild that leaves every image the same size has not made it.

## Out of scope

Section order, the 18-card grid, the industry filter, `index-en`'s Thai pricing
copy (which stays Thai by rule), the other 76 pages, and any new colour. The
palette does not change.
