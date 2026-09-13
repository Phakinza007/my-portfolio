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
