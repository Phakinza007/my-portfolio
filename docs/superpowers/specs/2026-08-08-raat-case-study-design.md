# RAAT — the portfolio's first real client work

**Date:** 2026-08-08
**Status:** Approved, ready for implementation planning

## Context

Every one of the thirteen projects on this site is self-directed design work. That was
established on 2026-08-07 and acted on: the phrase `ผลงานจริง` was removed from twelve files,
along with `See 9 real client projects` and `See real client work` from six category pages,
because none of it was true of the work those pages point at.

It is still true of those thirteen. What changed is that the site was **understating** its
author in a different way: there is real, paid, named, launched client work, and none of it
appears anywhere on the site.

The client is **ราชยานยนต์สมาคมแห่งประเทศไทย ในพระบรมราชูปถัมภ์** — the Royal Automobile
Association of Thailand, the country's national motorsport governing body and its FIA
representative. The engagement was direct, and the owner confirms he may name them.

## What the work actually was

Two things, both confirmed by the owner and verified against the live site on 2026-08-08:

1. **A visual refresh** — colours, typography, and the hero section image.
2. **A competition calendar page** — `raat.or.th/competition-calendar/1442/`, built with
   FullCalendar.

**Verified independently:**

| Claim | Evidence |
|---|---|
| FullCalendar, not a WordPress calendar plugin | `index.global.min.js` plus the full `fc-*` class set (`fc-dayGridMonth-button`, `fc-listMonth-button`, `fc-today-button`, `fc-view-harness`). The page's plugin list is Elementor, Happy/Royal addons, TablePress and dFlip — none of which produce this |
| Month and list views, Thai UI | Buttons render as `วันนี้` · `เดือน` · `รายการ` |
| Five colour-coded disciplines | Circuit Racing · Karting · Rally · Digital (eRacing) · Drifting |
| 22 events, 2026 season | Counted in the DOM |
| Typeface choice | `IBM Plex Sans Thai`, `Sarabun`, `Barlow Condensed` |
| Palette | Navy `rgb(15,31,61)`, pale blue `rgb(189,201,255)`, gold on the calendar controls |
| Still in use | Live, carrying 2026-season content, one month after launch |

## The honesty rules this spec exists to enforce

Mid-conversation, an earlier draft of this case study was going to claim the owner
restructured the site's information architecture from three top-level menus to seven. That
came from comparing a 2024 Wayback snapshot against the live site. **The owner had not done
it.** He said so, and it was cut.

Had he not, the site would have carried a false statement about work done for an organisation
under royal patronage. That is a real risk, not untidiness.

**Rule for this repo, and it belongs in `CLAUDE.md`: facts about client work come from the
person who did the work. Never infer scope by diffing a client's site against an archive.**

Four things are therefore excluded, permanently, unless the owner supplies them:

- **No IA or navigation claim.** He did not do it.
- **No metrics.** None were recorded. The case study says so rather than reaching for a
  substitute number.
- **No claim about how the 22 events are fed in.** He does not remember; the page will say
  "configured the calendar and loaded the season's fixtures" and stop there.
- **No "redesigned the website".** He changed colour, type and a hero image, and built one
  page. Saying more would be inflation, and the narrower claim is the better one anyway:
  "built the race calendar for Thailand's FIA member federation" is specific and checkable in
  a way that "redesigned an association website" is not.

**No images of the previous design.** The 2024 archive cannot be shown to be the immediate
predecessor, and republishing a client's old site is a courtesy question that has not been
asked. The before-state is described in words the owner can confirm, or not described at all.

## Decisions

### D1 — It is a case study, and it also sits in Selected Work

The site already separates two formats: thirteen `showcase-*` pages for self-directed pieces,
and four `case-study-*` pages for narrative write-ups. Real client work with a brief and an
outcome belongs in the second.

But the owner asked for it on the work page too, and he is right: `work.html` is where
"ผลงาน" leads, and the filterable grid is the most prominent thing on it. So RAAT appears
twice, deliberately:

- **A card in Selected Work** — the fourteenth — on `index`, `index-en`, `work`, `work-en`
- **A card in `#case-studies`** — the fifth — on the same four files

Both link to `case-study-raat.html`, which links out to the live site. This mirrors HabitQuest,
whose card points at a showcase page that then links to Vercel.

### D2 — The card must read as a different kind of thing

Thirteen cards are design exercises; this one is a live client site. Collapsing that
distinction wastes the only thing on the page a buyer weighs differently.

The card carries a **`ลูกค้าจริง`** tag. That phrase was removed from twelve files yesterday
for being untrue; here it is true, and it is the one place on the site it may appear.

### D3 — `data-industry="other"`, no ninth category

A national sports federation fits none of the eight keys. Opening a ninth for a single item
repeats the problem already flagged for `gym`, `construction` and `solar`, whose industry
pages each show one example and read as "done once". A second association project can open the
category later.

### D4 — Two new tags: `WordPress` and `FullCalendar`

The tag filter shipped on 2026-08-07 with 24 labels, all drawn from work that uses no external
libraries at all. These two are the first entries describing a stack, and they are the reason
this project matters beyond the client name: **nothing on this site currently shows that its
author works in WordPress**, which is what the Thai market hires for most.

Both must own at least one project, which they now do. The existing assertion — every tag
returns a non-empty grid — continues to hold.

### D5 — The thumbnail is a real screenshot

Twelve cards use transcribed SVG mini-UIs and one uses a photograph (`VELVÉ`). A screenshot of
the actual calendar page is more informative here than a stylised redraw, and the precedent
exists. It is the owner's own design, so there is no permission question.

### D6 — `CLAUDE.md`'s stack line stops being true

Checked 2026-08-08: the file does **not** contain the phrase "zero external libraries" that an
earlier draft of this spec attributed to it. What it does say, on line 15, is:

> **Stack:** HTML · CSS · JavaScript (vanilla, no framework)

That describes this repository, and stays accurate for it. But it is also the only place the
portfolio's technical range is written down, and it will now be wrong as a description of the
author — WordPress, Elementor and FullCalendar are none of those things. The line gains a
clause separating the two, and the card table moves from thirteen to fourteen with the
fourteenth marked as client work.

The audit that dropped the tech filter is recorded in the session history, not in `CLAUDE.md`;
no such sentence needs correcting because none exists.

## Scope

**Created:** `case-study-raat.html`, `case-study-raat-en.html`, one screenshot asset

**Modified:** `index.html`, `index-en.html`, `work.html`, `work-en.html` (two cards each),
`sitemap.xml`, `assets/search-index.json`, `CLAUDE.md`

**Not in this spec** — a new industry vertical for associations and organisations, and
reworking the homepage to lead with client work. Both are real opportunities and both are
larger than this; they get their own specs.

## Verification

1. **Every factual sentence traces to the owner's account or to an observation recorded above.**
   No sentence about IA, metrics, or the calendar's data source.
2. **`ลูกค้าจริง` appears on exactly one card**, and `grep` finds it nowhere near the thirteen
   self-directed projects.
3. **Card counts:** fourteen `.work-card[data-industry]` and five case-study cards in each of
   the four files; the filter's `ทั้งหมด` reports 14, not 18 — the carousel clone bug is
   permanent and must be re-checked whenever the card count changes.
4. **Tags:** 26 labels, each still owning at least one project.
5. **The bilingual pair rule holds** — `hreflang` trio on both files, self-referential
   canonical, `og:locale` per language, analytics tag before `</head>`, both URLs in
   `sitemap.xml`, both added to `search-index.json`'s `th` and `en` arrays.
6. **Outbound link works** — `https://www.raat.or.th/competition-calendar/1442/` returns 200.
7. **No overflow at 375 × 812**, iframe recipe with `clientWidth === 375` confirmed first.
8. **Lighthouse** on the new page: Accessibility 100, SEO 100, CLS 0. Best Practices caps at 77.
9. **Cache keys** — no stylesheet or script changes are expected; if any is touched, its query
   string is bumped. Three separate cache-key misses happened on 2026-08-07.
