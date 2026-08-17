# มูลนิธิบันไดแรก — a nonprofit demo and its showcase pair

Date: 2026-08-16
Status: built

## Why this project exists

`web-organization.html` was the thinnest industry page on the site. Measured before
this work, its `#related` strip carried **one** entry, and that entry was
`case-study-raat` — real client work. Every other industry page pointed at one to three
*demos*:

| industry page | entries before |
|---|---|
| `web-clinic` | 3 |
| `web-booking` · `web-restaurant` · `web-shop` | 2 |
| `web-construction` · `web-gym` · `web-solar` | 1 |
| `web-organization` | **1, and it is a case study** |

A buyer searching `รับทำเว็บสมาคม` landed on a page whose only proof was a single
motorsport-association calendar. This project adds the missing demo.

## What was built

| file | role |
|---|---|
| `bandairaek-foundation.html` | the demo — its own inline CSS, no shared reset, no portfolio chrome |
| `showcase-bandairaek.html` / `-en.html` | the showcase pair, story stack, identical to the other 15 pairs |
| `assets/thumbs/bandairaek.svg` | card thumbnail, extracted from the live page |
| `assets/screenshots/showcase-bandairaek.jpg` | 1491 × 812 hero screenshot |

Wired into: the card grid on `index` / `index-en` / `work` / `work-en`, the static
filter counts in all four, the prose project counts on `work` / `work-en`, a 28th tag
button, `_content/project-copy.json`, `assets/search-index.json` (both languages),
`sitemap.xml` (3 URLs), and a second, separately labelled strip on `web-organization`.

## The design direction

The palette is downstream of a written scene, the same method `lumi-clinic.html` uses:

> The staff room of an up-country school at four in the afternoon. A stack of grant
> applications sits on the desk in their folders. A teacher is copying one student's
> bank account number onto a transfer form. Nobody is taking a photograph.

Three things that scene rules out, and each is a decision rather than a default:

**1. There are no photographs on the page at all.** Not "no identifiable faces" — zero
images. The page argues that a foundation should publish its records rather than its
beneficiaries' faces, and it says so in running text near the top. A page making that
argument over a stock photo of a smiling child would be arguing against itself. This is
the same move `lumi-clinic` made when it retired the before/after slider and turned the
reason into copy.

**2. Not donate-orange, not charity-emerald.** Those two as large fills are the template
this whole category ships with. The deep forest `#1A5C43` and deep ochre `#7E4E10`
below are neither: they appear only as status text inside one table column, as a data
encoding, never as a surface.

**3. The paper is cool, not warm.** The warm-neutral band (OKLCH L .84–.97, C < .06,
hue 40–100) is the one `lumi-clinic` identified as the default "premium" surface. This
paper sits near hue 240.

Structural colour is one deep ink-blue `#1B3A6B` — the colour of an official document
rather than a brand. Money, dates and file sizes are set in IBM Plex Mono so columns line
up on their digits, which is a functional decision, not a stylistic one.

### Sections

`.site-nav` → hero → the stance paragraph → `#scholarships` → `#documents` →
`#calendar` → `#board` → `#give` → footer.

`#scholarships` is the spine: a real `<table>` of ten grants with code, level, school,
amount, instalment, transfer date and status, filterable by status. `#documents` states
file type, size and revision date before you click. `#calendar` pages through three
months with no library. `#board` uses monogram initials rather than portraits, for the
same reason the page carries no photographs.

## Things that were measured, not assumed

**Contrast.** Every text pair was computed, not eyeballed. Lowest is `--muted` on
`--paper-3` at **5.24:1**; all 20 pairs pass AA.

**Control borders needed their own token.** `--line-2` at 1.64:1 against the paper fails
WCAG 1.4.11, which wants 3:1 for the visible boundary that identifies a control.
Lighthouse only measures *text* contrast, so a button outlined in a hairline fails
silently and still scores 100 — the same shape as the `.tag-btn` finding in CLAUDE.md.
`--control-line: #748298` measures 3.66 / 3.40 / 3.19 on the three surfaces and is used
by `.chip`, `.doc-dl` and `.cal-btn` only.

**No dead controls.** A download button that does nothing is a dead click. Each
`.doc-dl` toggles a line saying the file is a sample, with `aria-expanded` tracking it.

**No backend, and the copy never implies one.** Zero `<form>` elements, zero `fetch`.
The donation block ends at a placeholder account number and a labelled QR slot, and the
footer states plainly that the page is a design example, that every name and figure is
fictional, and that it takes no real donations. That last part is not decoration: a
convincing charity page that appears to solicit money is worth marking unambiguously.

**The thumbnail was extracted, not drawn.** Measured inside a 1440 × 1000 iframe after
`await document.fonts.ready`, at scale 0.2994 (= 323.3 / 1080, the shell width). It is a
composition, not a viewport crop — at true scale the nav and hero alone overflow a
219.6-tall frame and the ledger, the whole point of the card, never enters it. Vertical
dead space is tightened; every element keeps its measured internal proportions and real x
positions. Verified with `getBBox()`: 0 of 96 elements overflow, and the widest text ends
at 321.5 against a content edge of 337.35.

**`web-organization` could not simply gain a fourth link.** Its `#related` eyebrow reads
`งานลูกค้าจริง`. Appending a simulated demo under that label would have made the page
claim a client it does not have — the first rule of the industry-page family. The strip
is now two labelled groups: RAAT under `งานลูกค้าจริง`, the demo under
`ตัวอย่างงานออกแบบ`. No new CSS; heading order stays valid.

## Verification

| check | result |
|---|---|
| Lighthouse, all three new pages | Accessibility **100**, Best Practices **100**, SEO **100** |
| `canScrollX` at 375 × 812 | `false` on all three, plus `work` and `index` |
| per-element right-edge sweep at 375 | 0 real overflows; the table and nav scroll inside their own boxes |
| internal links + anchors, whole site | 2,181 targets, **0 dead links, 0 dead anchors** |
| `_tools/check-copy.py` | 214 occurrences across 20 projects, all agree |
| `_tools/check-deploy.py` | no versioned asset changed, nothing to bump |
| filter, runtime | `ทั้งหมด` 17, `อื่นๆ` 5, `Nonprofit` 1 — static fallbacks match |
| carousel clones | 22 `.work-card` in the DOM, 17 counted; `data-industry` still stripped |
| every tag button | owns ≥ 1 card; none filters to an empty grid |

Two traps cost time and are worth recording:

- **The automated browser reported a 1960 px viewport**, so the page looked wrongly
  left-weighted until it was re-measured inside a 1440 px iframe. Already in CLAUDE.md;
  it is still the first thing to check.
- **The tab was backgrounded**, which freezes IntersectionObserver, CSS transitions *and*
  smooth scrolling. Reveals read as `opacity: 0` and `scrollTo` appeared to do nothing.
  Neither was a bug. End state was confirmed by disabling the transition and reading the
  computed value, with a positive control on an element lacking `.visible`.
- A Google Fonts `gstatic` 404 knocked Best Practices to 96 on one run. The font request
  hashes identically to the existing showcase pages, and two clean re-runs scored 100.

## Drift found while measuring, not caused by this work

CLAUDE.md's counts had already diverged from the tree. Measured 2026-08-16:

| CLAUDE.md says | actually |
|---|---|
| `search-index.json` 33 entries per language | 38 before this change, 39 after |
| 24 tag labels | 30 before this change, 31 after |
| sitemap 79 URLs | 84 before this change, 87 after |
| `assets/thumbs/` holds exactly the 14 card SVGs | 27 files: 15 SVG plus 12 unused JPGs from culled projects |

Also left alone, deliberately:

- `resume.html` states **13 โปรเจกต์** in three places. It was already wrong at 15 and is
  now wrong at 16, but CLAUDE.md records the resume as pending its own correction pass
  (the backend claims), and half-correcting it would split that work.
- Three tag labels — `Creative Studio`, `React`, `React Bits`, all Signalform's — appear
  on cards but have no button in the archive sidebar. Pre-existing.

## Not done

- No `web-*` industry page was created for this demo; it reaches buyers through
  `web-organization`, the card grid and the site search.
- `_tools/sitemap-lastmod.py` skipped the three new URLs because they are not yet in git.
  Their `<lastmod>` is a hand-set `2026-08-16` and the tool must be re-run after the
  commit to derive the real dates.
