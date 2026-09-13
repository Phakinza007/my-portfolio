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
