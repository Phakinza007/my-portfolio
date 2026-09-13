# Improve loop — log

Append-only. Newest last. One block per iteration of the
**portfolio-improve-loop** skill.

Read this before the research step: it is the only thing that stops iteration 4
from re-proposing what iteration 2 rejected.

---

## 2026-09-13 · iteration 0 — baseline, no site change

- **Finding** — none yet; the loop had no measurement of its own. Improvement
  ideas were coming from reading `CLAUDE.md`, which is a map, not the territory.
- **Change** — added `_tools/loop-scan.py` (static scan of all 96 `.html` files),
  this log, and `BACKLOG.md`. No page on the site was touched.
- **Measured** — first run, `python3 _tools/loop-scan.py`:
  - `BROKEN`: **0**
  - `DRIFT`: **5** — 4 over-long meta descriptions (`SalonOS`,
    `showcase-baan-talay` ± `-en`, `showcase-salon-os-en`), and `CLAUDE.md`
    stating 18 cards where `index.html` carries **20**
  - `GAP`: **7** thin proof strips — `dashboard-ui` 1, `web-gym` 1,
    `web-solar` 1, then `web-construction` / `web-organization` /
    `web-restaurant` / `web-shop` at 2, against `landing-page`'s 9
  - Instrument: 96 files · 2,715 relative links resolved · 34 TH/EN pairs ·
    20 cards in each of the four grid files · sitemap 96 URLs ·
    search-index 42 th / 42 en
- **Verified** — the scan's own numbers were checked against figures `CLAUDE.md`
  arrived at independently: **28 tag buttons vs 31 distinct card tags**, the
  three orphans being `Creative Studio`, `React`, `React Bits`. Two instruments
  agreeing on a number neither was told is the positive control.
- **Learned** — three things, all from this one run:
  1. `.filter-count` fallbacks are **currently in sync** at 20 / clinic 3 /
     booking 4 / restaurant 2 / shop 3 / gym 1 / construction 2 / solar 1 /
     other 5. They have been wrong before and nothing but this check reports it.
  2. Link scanning must strip `<script>` first — `${l.img}` inside
     `ElevateCommerce.html`'s template literal reported as a dead link.
  3. `CLAUDE.md` drifts behind the repo (18 → 20 cards, two new demos:
     `SalonOS.html`, `baan-talay.html`). The doc is now checked by the scan, so
     the next drift is caught rather than inherited.
- **Spawned** — the 5 `DRIFT` lines and the 3 one-link strips → `BACKLOG.md`.
  Deliberately not fixed in this iteration: the point of iteration 0 is the
  instrument, and mixing a site change into it would leave both unverified.

## 2026-09-13 · iteration 0b — the wiring is asserted, not checklisted

- **Finding** — the owner asked whether this loop is for adding showcase pages.
  It is not, but that *is* its most common `GAP` outcome, and it is the largest
  unit of work on the site: `80cf976` (BAAN TALAY + SALON OS) touched **48
  files**, and most of those wiring points fail silently when missed.
- **Change** — `scan_wiring()` in `_tools/loop-scan.py`, plus the
  **portfolio-new-proof** skill whose checklist is derived from that commit
  rather than from memory. Registered both in `CLAUDE.md`.
- **Measured** — the wiring check runs on all **19** showcase pairs and asserts
  five things each: a card in all four grid files (Thai slug in `index`/`work`,
  `-en` slug in the `-en` pair), a `_content/project-copy.json` entry, a
  `_content/showcase-shots.json` key, all three screenshots
  (`{,-b,-c}.jpg`) on disk, and `.story-price` on both sides. **19/19 pass**,
  which is what makes the check usable as a checklist: anything it says about a
  new pair is a missed step, not a new pattern.
- **Found while writing it** — `showcase-supplymate` has no `short` copy in
  `project-copy.json`, while two `#related` strips on `showcase-signalform` ±
  `-en` link to it. Those two locations carry copy with **no canonical**, so
  `check-copy.py` cannot see them drift — it reports "all repeated copy agrees"
  because it only checks keys that exist. Left for the next iteration.
- **Verified** — `check-copy.py` clean (248 occurrences, 23 projects),
  `check-deploy.py` clean (no versioned asset touched). No page changed.
- **Learned** — two things:
  1. **The first version of the `short` check was wrong**, and wrong in the way
     CLAUDE.md warns about: it counted `href="showcase-signalform"` and reported
     missing copy, but the only reference was that page's own **language
     toggle**. Match the `.project-link` anchor, not the bare slug. Required
     copy is conditional on a real reference.
  2. **`CLAUDE.md` did not describe the screenshot pipeline at all** — it still
     read as one hero image per showcase, where the repo has three declared
     views and a command to re-take them. Now documented.
- **Spawned** — supplymate's missing `short` → `BACKLOG.md`.

## 2026-09-13 · iteration 1 — check-copy.py could not see a minified page

- **Finding** — `loop-scan.py` reported `showcase-supplymate` missing its `short`
  copy while two `#related` strips link to it. Reading those strips turned up the
  bigger fact: **`check-copy.py` was blind to both of them.** Its parser matched
  `^\s*<span>…</span>\s*$` — the blurb alone on its own line, true of every other
  page and false of `showcase-signalform` ± `-en`, which are emitted minified onto
  one line. Six blurbs there were unguarded and the script printed
  *"all repeated copy agrees"*.
- **Change** — the parser now reads markup in document order instead of line by
  line (`_tools/check-copy.py`), and the copy it exposed was canonicalized:
  `showcase-supplymate` gained `th.short` / `en.short`, and the three blurbs in
  each signalform strip now match the canonical text verbatim.
- **Measured** — occurrences **248 → 254** (+6, exactly the two minified pages'
  blurbs). Of those six, **four already disagreed with the canonical that
  existed**: signalform's strip called HabitQuest *"Habit tracker
  ที่สร้างแรงจูงใจผ่านเกม"* where the canonical says *"แอปสร้างนิสัย full-stack
  เปลี่ยนนิสัยให้เป็นการผจญภัยแบบ RPG"*, and MuseRoom likewise. `loop-scan.py`
  wiring findings **2 → 0**; DRIFT overall 7 → 5.
- **Verified** — a **planted drift** on the minified page turns the script red
  (exit 1, the file named). A green run on a parser change proves nothing without
  that. Plus: `loop-scan.py --defects` (wiring clean), `check-deploy.py` (no
  versioned asset), `<span>` balance 18/18 on both edited files, and the new
  blurb lengths (57–69 chars) are inside the range the same component already
  renders elsewhere.
- **Learned** — three, one of them a mistake made and caught in this iteration:
  1. **Widening a regex adds false positives in the other direction.** Reading
     markup instead of lines immediately matched `resume.html`'s five external
     GitHub anchors and reported ten unguarded blurbs that are not project copy
     at all. The parser now skips `http(s)://` and `mailto:` hrefs.
  2. **`json.dumps(…, indent=1)` reformatted all 442 lines** of
     `project-copy.json` for a two-line addition. Reverted and done as a
     surgical text insert. A generated rewrite of a hand-maintained file is not
     a diff anyone can review.
  3. Choosing the canonical for supplymate had **no majority to defer to** — one
     location per language. The strip described the *stack* (`React และ Vite`);
     the canonical `long` describes the *product* (sold by the carton, minimums
     up front), which is the role `short` plays on every other project, so the
     new text is tightened from `long`. Nothing new was claimed.
- **Spawned** — `resume.html` / `resume-en.html` link five GitHub repos with
  their own descriptions, three of them (`phakin-task-manager`,
  `phakin-knowledge-ai`, `phakin-invenflow`) for projects **culled from the site
  on 2026-07-22**. Worth reading against CLAUDE.md's note that the resume pages
  still make backend claims the rest of the site retired. → `BACKLOG.md`

## 2026-09-13 · iteration 2 — CLAUDE.md's present tense was two demos behind

- **Finding** — `scan_docs()`: *"CLAUDE.md says 18 cards; index.html has 20."* Reading around
  that one line found the same staleness in sixteen other places, because every count in the
  doc was written by hand at a different time.
- **Change** — 25 edits to `CLAUDE.md`, under one rule: **a number describing the present
  must be true now; a number describing the past stays exactly as written.** So
  *"stripped from twelve files on 2026-08-07"*, *"115 projects"* on bigzweb, *"128 cards and
  128 badges"* and *"161.5 KB of HTML removed"* are all untouched, while every count of what
  the repo contains today was re-derived from the files.
- **Measured** — each new figure verified against the repo, not against another doc:

  | claim | was | measured |
  |---|---|---|
  | Selected Work cards | 18 (17 + RAAT) | **20** (19 + RAAT) |
  | `.filter-count` fallback line | all 18 / other 5 | all 20 / other 5 |
  | cards using an SVG thumb | 16 of 18 | **18 of 20** |
  | `assets/thumbs/` | "exactly those 14 files" | **30** (18 SVG + 12 unused JPG) |
  | showcase files | 32 / 34 (both in use) | **38** (19 TH/EN pairs) |
  | case studies | 4 | **5** |
  | TH/EN pairs | 23 pairs (46 files) | **34 pairs (68 files)** |
  | demo pages with no `-en` twin | 16 | **19** |
  | site-search pages | 70 (87 − 16 − 1) | **76** (96 − 19 − 1) |
  | `search-index.json` entries | 39 per language | **42** |
  | `.story-card`s sitewide | 136 | **160** |
  | contextual-nav files | 42 | **50** (38 + 10 + 2) |
  | industry pages | "Seven exist" / "The 7 industry pages" | **8** (`web-organization` was missing from both lists) |
  | `#projects` row | 13 project cards | **20** |
  | work archive vs bigzweb | "this one 16" | **20** |

  Two rows were **internally** contradictory before this, which is the tell that these are
  hand-written: the thumbnail section said *16 of the 18 cards* are SVGs and that the folder
  holds *exactly those 14 files*, and the showcase layout was *32 files* in one section and
  *34 pages* in two others.
- **Verified** — every figure re-derived by script after the edit (`cards 20`, `showcase 38`,
  `thumbs 30/18`, `search-index 42`, `site-search 76`, `story-price 38/38`, `web-* 8`,
  `50 contextual`, `9 filter buttons`); the full diff read line by line to confirm no
  historical figure moved; four lines rewrapped to the file's ~90-char convention.
  `loop-scan.py` DRIFT **5 → 4**, the `docs` finding gone. No browser check: `CLAUDE.md` is
  excluded in `_config.yml` and is not served.
- **Learned** — **the doc drifts one number at a time, and each one is individually plausible.**
  Nothing here was a mistake at the time of writing; the file simply has no mechanism that
  re-reads it. `scan_docs()` currently asserts only the card count, and that one line was
  enough to surface sixteen others — but only because a human followed it. Asserting the rest
  is cheap and is the obvious next move.
- **Spawned** — extend `scan_docs()` to assert the other measurable counts (showcase files,
  thumbs, pairs, search-index, story-cards, `web-*`), so this section cannot go stale again
  without the scan saying so. → `BACKLOG.md`

## 2026-09-13 · iteration 3 — four meta descriptions, and the ruler was wrong

- **Finding** — the last four `DRIFT` lines: meta descriptions at 236 / 214 / 206 / 195
  characters against the site's 190 ceiling. CLAUDE.md's own precedent is *"only those over
  190 were trimmed, because shortening the rest means rewriting his copy"* — so this is
  sanctioned trimming, not a rewrite.
- **Change before the change** — `loop-scan.py` was counting the **source** string.
  `SalonOS.html` uses `&quot;` twice, six characters each in the file and one on screen, so
  it measured **206 against a real 196** — the instrument put it 16 over the line where the
  copy is 6 over. The scan now counts `html.unescape()`d length, which is what a crawler
  counts. **Fix the ruler before cutting to it.**
- **Change** — trimmed all four, tails first:
  - `showcase-baan-talay` ± `-en`: dropped *"— ดูรายละเอียดโปรเจกต์เต็มรูปแบบ"* / *"— see the
    project write-up."*, boilerplate pointing at the page the reader is already on. 195 → 162
    and, with two tightenings, 236 → 186.
  - `showcase-salon-os-en`: dropped *"See the full project write-up."* 214 → 183.
  - `SalonOS.html` had no boilerplate tail, so two tightenings instead:
    `ย้ายด้วยสองก้าว → ย้ายสองก้าว` and `ช่างลาป่วยกลางวัน → ช่างลาป่วย`. 196 → 185. Both
    cases are still named; only "กลางวัน" is gone. No claim was cut from any of the four.
- **Measured** — `loop-scan.py`: **BROKEN 0, DRIFT 0.** The ladder is clear for the first
  time; only `GAP` remains.
- **Verified** — decoded length asserted ≤ 190 before writing each string; the old tails
  re-grepped and gone (0 and 0); and the `description` / `og:description` /
  `twitter:description` trio checked per page, since the baan-talay pages carry the same
  string in all three — the replace hit **3 occurrences** each, so they stay in sync. No
  browser run: nothing rendered changed, and Lighthouse's `meta-description` audit checks
  presence, not length.
- **Found while verifying** — `showcase-salon-os-en` was carrying **two different
  descriptions**: `name="description"` had the trailing sentence, `og:` and `twitter:` never
  did. The trim brought all three to one byte-identical string. That mismatch was invisible
  to every check in the repo, including this one — the scan reads `name="description"` alone.
- **Learned** — **a measurement that is 10 too high is worse than no measurement**, because
  it gets acted on. Had the scan not been fixed first, `SalonOS.html` would have been cut 16
  characters instead of 6, and the extra 10 would have come out of the owner's copy for no
  reason.
- **Spawned** — two:
  1. `scan_plumbing()` should compare `description` / `og:description` /
     `twitter:description` per page, not just measure the first.
  2. **The next iteration's work, and it is not what the backlog said.**
     `showcase-salon-os` carries `data-tags="Dashboard|…"` yet `dashboard-ui.html`'s
     `#related` still lists only BookEase — so the thinnest strip on the site is a **wiring
     miss from the SALON OS addition, not a missing demo.** Two files, not a new build.

## 2026-09-13 · iteration 4 — the thinnest strip on the site was a wiring miss

- **Finding** — `dashboard-ui` ± `-en` showed **1** `.project-link`, the thinnest strip on the
  site, against `landing-page`'s 9. The backlog (and `CLAUDE.md`) called this "the obvious next
  gap" needing **a second dashboard demo**. Measuring first said otherwise:
  `showcase-salon-os` already carries `data-tags="Dashboard|Booking|Design System|Light UI|
  Thai|Interactive"` and was reachable by `.project-link` from **only two pages** (VELVÉ's
  strips). SALON OS went into the grid and was never wired into the package page it belongs to.
- **Change** — added SALON OS as the second `.project-link` in `#related` on `dashboard-ui`
  and `dashboard-ui-en`, using `_content/project-copy.json`'s `long` verbatim per the
  category-page recipe. **Two files. Nothing built.**
- **Measured** — `dashboard-ui` **1 → 2**; `check-copy.py` occurrences 254 → **256**, still
  agreeing, which is the machine confirming the new blurbs match the canonical byte for byte
  rather than me eyeballing them.
- **Verified in a browser, since a page changed:**
  - Lighthouse mobile on `dashboard-ui`: **A11y 100 · SEO 100 · CLS 0 · LCP 1.7s**, and
    identical to the **committed baseline** (`git stash`, re-run, pop) on every category —
    including the one failing audit, `errors-in-console`, which is a single
    `ERR_CONNECTION_RESET` from this sandbox blocking an outbound font/analytics request.
    Pre-existing, not mine. Best Practices reads 96 rather than the documented 77 because
    **Clarity does not load on localhost**, so its third-party-cookie deduction cannot appear
    in a local run — worth knowing before reading 96 as an improvement.
  - 375 × 812 on both pages: `canScrollX: false`, `bodyScrollWidth` exactly 375, and a
    per-element right-edge sweep finding **zero** unclipped overflow, with 2 `.project-link`s
    rendered.
- **Also added** — `_tools/overflow-check.js`, the sweep above as one command. The review step
  asks for it every iteration, and a check that has to be rebuilt each time is a check that
  gets skipped. It drives a real Chromium over CDP, awaits `document.fonts.ready`, forces
  `scroll-behavior: auto` and neutralises `.reveal` — the three things a naive headless run
  gets wrong here — and ignores anything inside an `overflow-x` scroller, so BookEase's tables
  stay correctly unflagged.
- **Instrument fix** — `PACKAGE_PAGES` measured only the three Thai category pages, so an
  `-en` strip could have been thin on its own with nothing reporting it. Now both languages
  are measured: `landing-page-en` 9 = `landing-page` 9 and `dashboard-ui-en` 2 =
  `dashboard-ui` 2, so there was no hidden asymmetry — a verified negative, not an assumption.
- **Learned** — **re-measure before believing a GAP needs new work.** Two documents, written
  at different times, both said this needed a new demo; the repo said it needed a link. The
  cheapest fix on the site was sitting behind a sentence nobody re-checked.
- **Spawned** — `showcase-salon-os` is still absent from `web-booking`'s `#related` (which has
  3, so not a gap) — a judgment call about whether a salon queue calendar belongs on the
  booking-industry page, left for the owner rather than taken here.

## 2026-09-13 · iteration 5 — the same miss, twice more, and now asserted

- **Finding** — iteration 4 found SALON OS wired into the card grid but not into the package
  page its own tags claim. That was found by hand, so the first thing this iteration did was
  **generalise the question**: for every industry page, which cards carry that page's
  `data-industry` key and are *not* linked from its `#related`?

  | page | links | cards tagged for it | unlinked |
  |---|---|---|---|
  | `web-booking` | 3 | 4 | **`showcase-salon-os`** |
  | `web-shop` | 2 | 3 | **`showcase-supplymate`** |
  | `web-clinic` · `web-restaurant` · `web-construction` | 3 · 2 · 2 | same | — |
  | `web-gym` · `web-solar` | 1 · 1 | 1 · 1 | — |

  So `web-shop` was flagged thin while the demo that belongs there already existed, and
  **`web-gym` and `web-solar` genuinely have no candidate** — measured, not assumed. Those
  two are the only real "needs a demo" gaps left on the site.
- **Change** — wired `showcase-supplymate` into `web-shop` and `showcase-salon-os` into
  `web-booking`, canonical `long` verbatim. `web-shop` **2 → 3**, `web-booking` **3 → 4**.
  Neither is padding: each card's own `data-industry` names that page's key, which is the
  test the recipe's "do not pad it" rule needs.
- **Made permanent** — `scan_strip_coverage()` in `_tools/loop-scan.py` now asserts it, and
  reports it in the words that matter: *"the strip is thin because of a missing link, not a
  missing demo."* Proved by **removing the link again** and confirming the scan goes red
  (exit 1, the page and slug named). It also fails loudly if it finds no `.work-card` at all,
  so a broken selector cannot read as "nothing to report".
- **Measured** — `check-copy.py` 256 → **258**, still agreeing. `loop-scan.py` BROKEN 0,
  DRIFT 0.
- **Verified in a browser** — 375 × 812 on both pages: `canScrollX: false`,
  `bodyScrollWidth` exactly 375, zero unclipped overflow, 3 and 4 `.project-link`s rendered.
  Lighthouse mobile on `web-shop` vs the committed baseline: **A11y 100 → 100, SEO 100 → 100,
  CLS 0 → 0**. Performance read 86 → 88 and LCP 2.3s → 2.1s, which is **run-to-run variance,
  not a win** — the added image is `loading="lazy"` and below the fold, so there is no
  mechanism by which it could make the page faster.
- **Learned** — **a hand-found bug is a reason to write a check, not just a fix.** One manual
  discovery in iteration 4 turned out to be three instances of the same thing; two of them
  would have gone on reading as "needs a new demo" indefinitely, and one was on a page the
  scan was already flagging.
- **Remaining GAPs are now honest ones** — `web-gym` and `web-solar` at 1 link each, with no
  existing demo that fits. That is a real build (the **portfolio-new-proof** skill, ~14
  wiring points) and it needs the owner's call on which sector and what the demo should be,
  so the loop stops here rather than inventing a brand.

## 2026-09-13 · iteration 6 — the truth-check found nothing, and the ship gate found four

- **Finding (planned)** — read the two newest showcase pages against the demos they
  describe. That is the site's most expensive documented failure class: 23 strings across 13
  files described BuildNest as hand-drawn SVG for six days after it was rebuilt around
  photography. No script can check it.
- **Result: both pages are clean.** Nineteen specific claims verified against source —
  SALON OS's 5-stylist × 30-minute grid (`SLOT = 30`, `OPEN = 600`, `CLOSE = 1200`, minutes
  from midnight), its drag *and* two-step move, skill matching, the no-more-than-30-minutes-
  earlier rule, the sick-stylist case that moves 3 of 4 and says so, undo, computed counters;
  BAAN TALAY's 14 hash routes, +35% / −15% / +20% seasonal rates, Songkran and New Year
  surcharges, 2- and 3-night minimums, seeded availability, EARLYBIRD's 30-day rule, 10
  reviews with two owner replies and deliberately no `schema.org/Review`, the single string
  table, and zero backend calls. **A verified negative is a real outcome**; the point of the
  check is that nobody could have known without running it.
- **Five instrument errors in one iteration, every one of which would have been a false
  report to the owner:**
  1. Scanned `baan-talay.html` — **4.6 KB**, a shell. The demo is 126 KB of
     `assets/baan-talay.js`. Nineteen claims read as unsupported.
  2. `10:00`/`20:00` not found, because the code stores minutes (`OPEN = 600`).
  3. `10:64` looked like an invalid rendered time; it is `--s-10:64px`, a CSS spacing token
     caught by a `[012][0-9]:[0-9][0-9]` pattern.
  4. `Math.random` showed **1 hit** against a page claiming never to use it — the hit is the
     comment *"never Math.random()"*. A forbidden-call grep matches the line forbidding it.
  5. Guessed state names (`selectedApptId`, `pendingMove`, `moveMode`) all absent; the real
     ones are `picked` / `sheetPick`. Absence of my vocabulary, not of the feature.
- **Change shipped instead** — the detour through `baan-talay.js` exposed something real:
  **four asset references carried no `?v=` token at all**, and the ship gate could not see
  them.
  - `analytics.js` bare on `SalonOS`, `baan-talay`, `pathapee-precast` while **93** other
    pages carry `?v=funnel`. Next time that token moves, those three keep serving whatever
    the browser cached — silently, on the click tracking and the `?cl_off` opt-out.
  - `assets/construction-redesign.css` (18 KB) bare on its only consumer, and that sheet has
    been edited before (the clipped-CTA fix, 2026-08-10).
  - `check-deploy.py` carried `if not before and not now: continue  # asset carries no ?v=
    token at all` — a one-line exemption for the one case that **cannot be fixed after the
    fact**, since a bare URL is cached forever.
  - Worse: its bare/split sweep sat **after** the `if not assets: return 0` exit, so the
    sweep whose own comment promises it runs "for every versioned asset, not just the changed
    ones" did not run at all on a normal HTML-only change. Both sweeps now run first.
  - Scoped to served pages: `assets/_archive/index-improved.html` is underscore-prefixed, so
    Jekyll 404s it and it can strand nobody.
  - The ship skill's hand-written **"seven versioned assets"** table said seven while nine
    already carried tokens (ten now) — `baan-talay.css` / `.js`, 172 KB, landed without it
    being reread. Rebuilt from the repo, with a note not to maintain it by hand.
- **Verified** — the gate reproduced red on all four before the fix and green after;
  `?v=`-suffixed URLs return **200** for both assets; all four pages measured at 375 px with
  real content (291–747 elements, styles attached, titles read).
- 🔴 **And one more instrument error, caught only because the numbers were too tidy.** The
  first 375 px run on two of those pages reported `canScrollX: false`, zero overflow — while
  **the local server was dead**. A Chrome error page passes every overflow assertion.
  `_tools/overflow-check.js` now returns a `loaded` flag (stylesheets attached *and* >200
  characters of body text) and **exits 2** when it is false, so a dead server or a 404 can
  never read as a clean page again.
- **Learned** — **every check needs a way to fail for the right reason.** Three of the four
  things fixed this iteration were checks that passed while measuring nothing: the ship gate
  skipping bare tokens, its sweep skipped by an early return, and the overflow tool grading
  an error page.

## 2026-09-13 · iteration 7 — a claim has more than one representation

- **Finding** — continuing iteration 6's truth-check across the remaining 17 pairs, but
  **generalised into a sweep** rather than read one by one: for every showcase page, does it
  claim hand-drawn-not-photography, or name a backend, and does its demo agree? 12 pages
  flagged. Ten were my instrument:
  - the "photo" on `bandairaek` and `pathapee`, the two demos that must never carry one, is
    each page's **own OG image** in `<head>` — site chrome, not page imagery;
  - "mentions a backend term" fired on pages whose prose *denies* one
    (`ไม่ได้ต่อระบบหลังบ้าน`) — the same polarity trap as iteration 6's `Math.random`.
- **The two that survived were real, and the same bug in both.** `showcase-bookease` says
  `ไม่ได้ต่อระบบหลังบ้าน` **and wears a `Full Stack` pill in the same page**; so does
  `showcase-elevate-commerce`. The 2026-08-12 purge removed 37 backend *sentences* across 13
  files and left the label. Measured extent:

  | representation | where |
  |---|---|
  | `.tag-list` pill | 5 showcase pairs — bookease, elevate-commerce, elasticshop-gaming, ratri-restaurant, supplymate |
  | visible card tag | `index` ± `-en` |
  | `data-tags` | 5 cards × 4 grid files |
  | sidebar filter button | `work` ± `-en` |
  | prose | `showcase-elasticshop-gaming` ± `-en`: *"แล้วพัฒนาแบบ full-stack"* / *"implemented full-stack"*, on a demo with **0** backend calls |

- **Change** — all of it removed, 17 files. The button had to go with the label or the filter
  would have had a control that empties the grid — the failure `scan_strip_coverage`'s sibling
  check asserts against. `CLAUDE.md`'s tag arithmetic updated (31 labels / 28 buttons → **30 /
  27**, and `Full Stack` off the spaced-label list).
- **Deliberately left**: the `full-stack` positioning line on `index` / `about` / `resume`
  (± `-en`) — CLAUDE.md records those as the owner's own pending pass, and they are
  positioning, not a per-project claim — and HabitQuest's blurb, whose app is external and
  cannot be verified from this repo. Both stated in `CLAUDE.md` so the next pass sees them.
- **Verified behaviourally, because the filter is live JS**: clicked **all 27** buttons on
  `work` and `work-en`. Every one returns 1–6 cards, **none empties the grid**, releasing them
  all returns to 20, and `ลูกค้าจริง` returns exactly 1 — RAAT alone, as the rule requires.
  Plus `check-copy.py` clean and `loop-scan.py` BROKEN 0 / DRIFT 0.
- 🔴 **The verification lied twice before it worked, and the way it lied is the lesson.**
  First pass: 14 of 27 buttons reported the *full set*, which reads as "this tag matches
  everything". It was a **deferred script**: `site-ui.js` had not attached when the clicks
  started, so they silently no-opped, and a no-op is indistinguishable from a filter that
  matched all 20. A single-button probe proved it — `aria-pressed` stayed `"false"` and
  `#filter-status` was empty. **Navigating is not readiness.** The tool now polls until the
  filter writes its own status line (its only observable proof of life) and refuses to report
  at all if that never happens.
- **Also added** — `_tools/tag-filter-check.js`, that sweep as one command. `loop-scan.py`
  asserts the same invariant statically; this is the version that can see a broken handler.
- **Learned** — **a claim lives in more than one kind of markup.** Prose, a pill, a
  `data-*` attribute, a filter button and a card label are five representations of one
  sentence, and a sweep for sentences finds one of them. When retiring a claim, ask what
  *else* renders it.

## 2026-09-13 · iteration 8 — every checkable claim is true; two are not checkable here

- **Finding** — the claim types iteration 7's sweep did not cover: numeric ("N screens",
  "N steps") and negative ("no X").
- **Numeric: 4 pages make one about themselves, and all four are true.**
  `baan-talay` 14 screens / 10 reviews / "2 rooms left" and `salon-os` 5 columns were
  verified in iteration 6; `elasticshop-gaming`'s "ครบ 4 flow หน้าจอ" matches exactly four
  views (`home`, `topup`, `status`, `history` — as ids, `data-view` and `<section>`s);
  VELVÉ's "ระบบจองคิว 4 ขั้นตอน" matches **4 `.wiz-dot`s** and four panel headings
  (เลือกบริการ / แพทย์ / วันและเวลา / ยืนยัน).
- **Negative: mostly rhetoric, and every falsifiable one that can be checked here holds.**
  MuseRoom's *"ไม่มีราคาและไม่มีปุ่มซื้อ"* — **0** price mentions, **0** cart controls.
  Signalform's *"ไม่มี horizontal overflow"* — measured in a real browser at 375 px:
  `canScrollX false`, `bodyScrollWidth` 375, zero unclipped overflow. bandairaek's and
  pathapee's *"ไม่มีรูปถ่ายแม้แต่รูปเดียว"* — confirmed in iteration 7.
- **Two more instrument errors, both scoping:**
  1. The first numeric pass reported **"4 ขั้นตอน" on every single page**, because it read
     each file whole and so read the `#related` strip — three *other* projects' blurbs — as
     the page's own claims. A page's claims are in `<section id="overview">`.
  2. VELVÉ's wizard "had 5 steps": the fifth is `<!-- Step 5: success -->`, an **HTML
     comment** labelling the success panel. Four `.wiz-dot`s, four headings. Count elements,
     not the labels around them.
- **Shipped** — no site change; nothing was wrong. Instead the recipe those nine wrong
  readings bought is now written into the **portfolio-improve-loop** skill as six rules, so
  the next claim check starts where this one ended rather than repeating it.
- **Two claims cannot be settled from this repo, and both are the owner's to confirm:**
  1. `showcase-solarpeak` says *"ภาพถ่ายหน้างานจริง ไม่ใช่ภาพสต็อก"* — real on-site
     photographs, not stock. Six photos do exist in `assets/solar/`, so the *existence* is
     true; **provenance is not knowable here**, the commit that added them says nothing about
     it, and this site has shipped Unsplash photos before (`dental-clinic`'s old card,
     lumi-clinic's four hotlinked faces). If they are stock, the sentence is false on a page
     that makes a point of the distinction.
  2. `showcase-habitquest` says the app has *"บัญชีผู้ใช้จริงและเก็บข้อมูลถาวร"* and is
     *"ไม่ใช่ demo แบบ static"*. HabitQuest is hosted on Vercel from another repo, so nothing
     here can confirm or deny it — and it is the one project on the site whose copy asserts a
     real backend.
- **Learned** — **when the loop runs out of things it can verify, the honest next step is a
  question, not a change.** Iterations 6–8 checked every claim this repo can settle; what is
  left needs the person who made the work.

## 2026-09-13 · iteration 9 — turn iterations 2 and 3 into assertions

- **Finding** — two items this loop spawned itself: `scan_docs()` asserted **one** of
  CLAUDE.md's counts (iteration 2 corrected seventeen), and nothing compared a page's
  `description` / `og:description` / `twitter:description`, which is how iteration 3's
  mismatch stayed invisible to every check in the repo.
- **Change 1 — all 14 measurable CLAUDE.md counts are now asserted**: cards, showcase files
  and pairs, `assets/thumbs/` contents, cards using an SVG thumb, TH/EN pairs and their file
  count, search-index entries, site-search pages, `.story-card`s, contextual-nav files, tag
  labels, tag buttons, demo pages. All 14 pass, which independently re-confirms iteration 2.
  If a sentence is reworded so a check cannot find it, that is reported as INFO rather than
  passing silently — a check that stops matching is a check that stops checking.
- **Change 2 — the description trio, and the rule took three attempts.** Each rejected
  attempt is why the final one is worth having:
  1. *"flag any page where the three differ"* → **34 of 96** pages carry deliberately shorter
     social text. Pure noise.
  2. *"flag when one is a strict prefix of another"* → **15**, and six of them are the
     `web-*` family all dropping the same trailing CTA for Twitter. A pattern repeated across
     six siblings is a convention, not a slip.
  3. **Deviation from the page's own family.** The real bug was `showcase-salon-os-en`
     carrying a tail in `name="description"` that `og:`/`twitter:` never had, while its 37
     siblings had identical trios. So: group by family, find the majority shape, flag the
     minority — and only fail on the *tail* shape, because that is the signature of one copy
     being edited and its siblings left behind.
- **It found a real deviation and I chose not to fail it.** `showcase-signalform` ± `-en`
  write independent, tighter social lines where 36 of 38 showcase pages repeat one string.
  That is not a stale copy — it is arguably better than the family's pattern — so it reports
  as INFO. **A check that detects a difference cannot infer intent**; the honest version says
  what it saw and names the benign explanation.
- **Verified** — three wrong counts planted into `CLAUDE.md` (36 showcase files, 39
  search-index entries, 136 `.story-card`s) were each caught with the measured value named;
  and **iteration 3's exact bug, re-planted verbatim**, turns the trio check red. Both
  restored. `loop-scan.py` BROKEN 0, DRIFT 0; `check-copy.py` and `check-deploy.py` clean.
- **Learned** — **calibrate a new check against the bug it was built for and against the
  site's normal variation, before believing either its passes or its failures.** The first two
  rules here would each have shipped a permanently noisy check, and noise is how a gate stops
  being read.
