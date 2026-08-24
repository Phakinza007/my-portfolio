# Showcase pages: let the work fill the page

**Date:** 2026-08-24
**Scope:** the 34 `showcase-*.html` files, plus the kicker/intro cleanup on
`case-study-raat.html` / `-en`
**Status:** approved design, ready for an implementation plan

---

## Why

The 34 showcase pages are structurally identical by design, and that was the
right call. What was never measured is how much of each page's *text* is also
identical.

Measured 2026-08-24:

| String | Identical across |
|---|---|
| `.eyebrow` — `project showcase` | **34 / 34** |
| `.story-intro` — "อ่านจากบนลงล่าง — โปรเจกต์นี้คืออะไร…" | 16 / 17 TH, 15 / 17 EN |
| the four `.story-card` `<h2>` | **17 / 17** each, both languages |
| the four `.story-kicker` | 16 / 17 TH, 15 / 17 EN |
| `#related` `<h2>` | 16 / 17 |

**144 `.story-kicker` elements across the 36 pages that carry the story stack.**
Only `showcase-signalform` wrote its own.

That is eleven lines per page that say nothing about the project. Three of the
four kickers measurably restate their own heading:

```
ภาพรวมโปรเจกต์          ← ใช้เวลาไม่กี่นาที เห็นภาพทั้งหมด
สรุปใน 30 วินาที        ← จุดที่โดดเด่น อ่านผ่าน ๆ ก็เห็น
โปรเจกต์นี้เหมาะกับใคร  ← อ่านรอบเดียวรู้เลยว่าใช่หรือไม่ใช่
```

This is not a new opinion. It is the site's own existing rule, applied where the
2026-08-10 pass did not reach — that pass deleted 44 kickers across 43 files
using exactly this criterion, and the 144 inside the story stack survived it.

The second measurement is worse. **Each showcase page carries four `<img>`
elements, and only one of them is the project the page is about.** The other
three are `#related` thumbnails of other projects. A page about work X shows
less of X than it shows of everything else.

`.impeccable/critique/2026-08-09…showcase-supplymate.md` scored the site 30/40
and named the axis: *"For a portfolio the design is the product, and this one is
currently competing on tidiness. A visitor deciding whether to hire a frontend
developer sees a well-run system rather than a point of view."* It also named
the lever — the showcase template, which 34 pages inherit at once.

## What the references said

Eight project/case-study pages were read (four opened in a browser, four
fetched for structure). Full notes: `_docs/taste/references.md`.

**Unanimous:** none of the eight carries a kicker, and none spends more than one
line framing the work before showing it. The single exception, Instrument, keeps
a `Case Study` label and is the most template-looking page in the set.

**Split on per-project identity.** Pentagram lets the project's own imagery fill
the page while the chrome stays black-on-white and silent — `h1` is the project
name, one subtitle line, two tags, and the long copy is folded behind an
`About the project +` disclosure. Emil Kowalski does the opposite and gives every
project *identical* typographic treatment on purpose, so that content quality
carries the weight. Locomotive runs 45 projects with no per-project accent at all.

Those are not actually in conflict: **all three make the chrome silent.** They
differ only in what fills the space — Pentagram fills it with the work, Emil
fills it with nothing. This site fills it with scaffolding.

## Decision

Take Pentagram's half: **show more of the work, and stop talking around it.**

Explicitly rejected, with reasons:

- **Per-page accent colour derived from each demo's palette.** Supported by
  uxfol.io's guidance but contradicted by Emil and Locomotive, and Pentagram —
  the reference that motivated it — does not tint its chrome at all. Not worth
  34 contrast re-checks for a mechanism the strongest reference does not use.
- **Rewriting the four `<h2>` per project** (Linear's approach — customer-specific
  section headings). Real evidence supports it, but it is ~136 new heading strings
  and it would cost the cross-page scan consistency that CLAUDE.md defends
  deliberately. Deferred, not refuted.
- **Folding body copy behind a disclosure.** Pentagram can do this because it has
  a dozen images to fall back on. This site would be hiding its only substance.

## The three views

Per demo, not per page — `showcase-X.html` and `showcase-X-en.html` reference the
same JPEG, so this is **17 demos, 34 new captures**, not 68.

| | View | Viewport | Status |
|---|---|---|---|
| **A** | landing / top of the demo | 1491 × 812 | **exists, unchanged** |
| **B** | the one mechanism the page already brags about | 1491 × 812, scrolled | new |
| **C** | the same demo at phone width | 375 × 812 | new |

**B is derived, not invented.** Every showcase page's `.highlight-list` already
names what is distinctive about its demo. Pathapee's first bullet is
*"เครื่องมือเลือกแผ่น เลื่อนช่วงพาดกับเลือกน้ำหนักบรรทุก แล้วตารางบอกทันทีว่าเหลือรุ่นไหนให้เลือก"* —
so B is that selector. BookEase's is the New Booking modal; VELVÉ's is the
four-step wizard. The selector for each demo is recorded in config, not guessed
at capture time.

**C earns its place twice.** Mobile is 51% of this site's traffic and a Thai
small-business buyer asks about it directly, so it is the proof they want. It is
also a tall frame next to two wide ones, which is what stops the three views
reading as three identical rectangles.

### Capture sources

15 of 17 demos are local files served by `_tools/serve.py`:

```
bandairaek-foundation  BookEase  construction-landing  dental-clinic
elasticshop-gaming     ElevateCommerce  gym-landing   lumi-clinic
MuseRoom  coffee-landing  pathapee-precast  sorn-restaurant
solar-landing  aesthetic-booking  signalform-studio/index.html
```

Two are remote and must be captured over the network:

- HabitQuest — `https://habitquest-pi.vercel.app/`
- SupplyMate — `https://phakinza007.github.io/supplymate-wholesale/`

## Page layout

`.story-intro` is being deleted anyway. **Its slot becomes the work.**

```
hero — view A in .browser-frame          eager, CLS reserved, unchanged
─────────────────────────────────────────────────────────────────────
.work-strip
  [ view B — 2/3 ]            [ view C — 1/3 ]
    one-line caption            one-line caption
─────────────────────────────────────────────────────────────────────
.story-stack — four cards      h2 unchanged, 3 of 4 kickers deleted
```

Rules:

- **The captions are the only new text.** No heading, no eyebrow, no kicker above
  the strip — that is the whole point of the change, and re-introducing a label
  here would reproduce the defect being removed.
- A caption says what you are looking at, which makes it project-specific by
  construction. 68 short strings (17 demos × 2 views × 2 languages).
- Below 900px the two figures stack. Below 640px they stay stacked.
- Both new images carry explicit `width` / `height` and `loading="lazy"`.
  CLS must stay 0 and neither may compete with the hero for LCP.
- `alt` on both, describing the view, not repeating the caption verbatim.

Net effect on the image ratio: from *"1 image of this project, 3 of others"* to
*"3 of this project, 3 of others"*.

## Copy deletions

| What | Files | Note |
|---|---|---|
| `.eyebrow` `project showcase` | 34 showcase files | **`case-study-raat` is excluded** |
| `.story-intro` | 36 files | the whole paragraph |
| `.story-kicker` on cards 1–3 | 36 files | 108 elements |
| `.story-kicker` on card 4 | — | **kept**, it adds information |

**RAAT's two eyebrows must not be touched.** Its first is `งานลูกค้าจริง`, which
is the one claim on this site that says a piece of work was paid for by a client,
and CLAUDE.md treats that claim as load-bearing. Its second is `เครื่องมือที่ใช้`
above `#stack`, which introduces rather than repeats. RAAT does carry the same
generic story-intro and the same four generic kickers, so those go.

**RAAT gets no work strip.** It documents a client's live site, not a demo this
repo owns. Capturing and republishing more of raat.or.th is a courtesy nobody
asked for — the same reasoning that already keeps the client's previous design
off this site.

Card 4's kicker differs per page (`…ธุรกิจของคุณ` on demos, `…องค์กรของคุณ` on
RAAT and bandairaek). Preserve what is there; do not normalise it.

## `_tools/capture-shots.py`

34 captures cannot be taken by hand, and the naive path is known to fail
silently. CLAUDE.md records the measurement: headless Chrome renders
`display=optional` webfonts as the fallback **every time**, and three runs with a
warmed font cache produced byte-identical files in the wrong font. 86 of 88 files
on this site ask for `display=optional`.

The tool therefore must:

1. Launch Chrome with `--remote-debugging-port` (a real browser, not `--headless
   --screenshot`). Node has a global `WebSocket`, so CDP needs no packages; Python
   may drive it over the same socket.
2. `Page.navigate` **twice** so the second load has the font on disk.
3. `await document.fonts.ready` before reading or capturing anything.
4. Neutralise `.reveal` / `.rv` so below-fold content is not captured
   mid-transition.
5. For view B, scroll the configured selector into view. Set
   `documentElement.style.scrollBehavior = 'auto'` first — `scroll-behavior:
   smooth` is frozen in a hidden tab and `scrollTo` returns with `scrollY`
   unchanged.
6. **Run a positive control before trusting any capture:** measure one string in
   the page font and again with the webfont dropped from that element's own
   stack, and require the two widths to differ. A capture in the wrong font looks
   entirely normal and silently corrupts everything measured from it.
7. Emit at the device-pixel size, then `sips -z <h> <w>` to the target so the new
   files match the existing 1491 × 812 set.

Config lives in `_content/showcase-shots.json`, one entry per demo:

```json
{
  "pathapee": {
    "url": "pathapee-precast",
    "b": { "selector": "#selector-section", "label_th": "…", "label_en": "…" },
    "c": { "scroll": 0, "label_th": "…", "label_en": "…" }
  }
}
```

Both paths are underscore-prefixed, so Jekyll never serves them.

**This tool is the mitigation for the risk below, not a convenience.**

## Risk: three times the surface for stale imagery

CLAUDE.md records the failure mode precisely: 23 strings across 13 files claimed
BuildNest used hand-drawn SVG instead of stock photography, and stayed true right
up until the demo was rebuilt around photography on 2026-08-06 without the copy
following. *"Not a false claim someone invented, but a true one nobody retired."*

Tripling the images per showcase page triples that exposure. The mitigation is
that `capture-shots.py` regenerates the whole set from one command, so
re-capturing after a demo changes is cheap enough to actually happen. Rewriting a
demo now means re-running the capture as well as re-reading the copy.

## Verification

Nothing here is complete until each of these has been run and its output read:

- `python3 _tools/check-deploy.py` — **`assets/portfolio-pages.css?v=thai-leading`
  must be bumped**, because `.work-strip` is new CSS on a versioned sheet.
- `python3 _tools/check-copy.py` — repeated project copy still agrees with itself.
- `python3 _tools/sitemap-lastmod.py` — no new URLs, but lastmod moves.
- Lighthouse on three sampled showcase pages, mobile and desktop. Accessibility
  and SEO must be 100. Best Practices caps at 77 sitewide (Clarity cookies) —
  that one is a known, accepted exception and is not to be chased.
- CLS 0 on the sampled pages. Every new `<img>` carries `width` and `height`.
- `canScrollX: false` at 375 × 812 **and** a per-element right-edge sweep.
  `canScrollX` alone has missed a real overflow on this site before —
  `html, body { overflow-x: hidden }` clips the evidence.
- Every new `<img>` has a meaningful `alt` and resolves.
- `.story-price` still present on all 34 showcase pages; still absent from
  `case-study-raat`.
- Each TH file and its `-en` sibling have the same number of `figure`s, the same
  number of `.story-card`s, and the same number of kickers.
- Verify the reveal still fires: the new figures may be hidden with `opacity` or
  `transform` only. **Never `clip-path`, `visibility`, `display`, or `width: 0`**
  on a `.reveal` element — Chrome subtracts a target's own `clip-path` from its
  intersection rect, which is what once left the hero image invisible on 30
  showcase pages with no error anywhere.
- Reveal behaviour cannot be judged in a background tab. Chrome suspends
  IntersectionObserver and freezes transitions when `document.hidden` is true;
  check it before believing any result in this family.

## Out of scope

- `DESIGN.md` is stale — it describes SERENE Wellness (deleted 2026-08-12), names
  Outfit as the display face (now Bai Jamjuree), calls the card thumbnails
  inline-styled `<div>`s (now SVG), and states the site uses no raster images
  (it does). It needs its own pass and is not touched here.
- Five orphaned files in `assets/screenshots/` — `brew-co.png`, `cover.png`,
  `cozy-coffee.png`, `devlaunch.png`, `drip.png` — matched by nothing in any
  `.html`, `.css` or `.js`. Recorded, not deleted.
- Rewriting the four `<h2>` per project (Linear's pattern). Deferred with
  evidence, above.
- The homepage, the archive, the category pages, and the 8 industry pages.
