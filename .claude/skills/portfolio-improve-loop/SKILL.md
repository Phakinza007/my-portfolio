---
name: portfolio-improve-loop
description: >
  Run one research → do → review iteration on Phakin's portfolio (my-portfolio).
  Use when the user asks to improve the site without naming a specific change —
  "ทำให้เว็บดีขึ้น", "รอบปรับปรุง", "improve the portfolio", "หาอะไรทำต่อ",
  "what should I work on next" — or when driven by /loop on a schedule.
  Picks the highest-value change from measured evidence, ships exactly one, then
  verifies and records it. Also use before starting any self-directed work on the
  site, to check the change is not already in the rejected list.
---

# portfolio-improve-loop

One iteration = **one** change, measured before, verified after, written down.

```
RESEARCH ──▶ DECIDE ──▶ DO ──▶ REVIEW ──▶ RECORD ──▶ (next iteration)
   ▲                                                      │
   └──────────────── the log is the input ────────────────┘
```

The log is what makes this a loop rather than N unrelated sessions. **Read it
first, write it last.** Without that, iteration 4 re-proposes what iteration 2
rejected, and the site churns instead of improving.

Files this skill owns:

| File | Role |
|---|---|
| `_tools/loop-scan.py` | the measurement — static facts about all 96 pages |
| `docs/improve-loop/LOG.md` | append-only: what shipped, what it measured, what was learned |
| `docs/improve-loop/BACKLOG.md` | candidates, and **rejected** ideas with the reason |

`docs/` is excluded in `_config.yml`, so neither file is served at ph-akin.dev.

---

## 1 · RESEARCH — measure, don't brainstorm

Read the log first, then measure. Three commands, in this order:

```bash
python3 _tools/loop-scan.py          # structural defects, drift, thin spots
python3 _tools/check-copy.py         # repeated blurbs that disagree with each other
python3 _tools/check-deploy.py       # a changed asset whose ?v= token did not change
```

`loop-scan.py` prints four levels, and they are a **priority ladder**, not a
list of options:

| Level | Meaning | Rule |
|---|---|---|
| `BROKEN` | a visitor or a crawler hits something wrong today | fix before anything else |
| `DRIFT` | two places in the repo disagree — one of them is a lie | fix before adding anything |
| `GAP` | nothing is broken; this is the thinnest part of the site | this is where new work goes |
| `INFO` | instrument counts | read these to trust the zeros above |

⚠️ **Never start a new page while a `BROKEN` or `DRIFT` line is open.** A new
showcase page on top of a dead anchor makes the site bigger and no better —
and the defect gets harder to find the more pages surround it.

**A zero is a claim about the instrument until the INSTRUMENT block backs it
up.** `loop-scan.py` prints how many files, links and pairs it checked for
exactly this reason. If a section reports nothing and its count looks wrong
(0 links, 0 pairs), the pattern is broken, not the site. CLAUDE.md →
"How to measure this repo without fooling yourself" is the long version, and
every trap in it was paid for once already.

### What the scan cannot tell you

It reads files. It can prove `#related` has one link; it cannot tell you the
copy above that link is **true**. It knows nothing about Lighthouse, nothing
about 375px, and nothing about whether a page is any good. So one iteration in
three or four, spend the research step on something the scan structurally
cannot see:

- open a page and read it against what it describes — a showcase page describes
  a demo, and nothing re-reads it when the demo is redesigned (CLAUDE.md
  records 23 strings across 13 files that stayed true-when-written and false
  after)
- run Lighthouse on the newest page (`_tools/serve.py`, never `http.server`)
- check Clarity: which pages get `showcase_open` and never `cta_fastwork`

---

## 2 · DECIDE — one change, and say why it beats the others

Write three or four sentences before touching a file:

1. **The finding.** Which scan line, or which measurement you took yourself.
2. **The change.** One sentence. If it needs two, it is two iterations.
3. **Why this one.** What it beats, and why.
4. **How you will know it worked.** The number or the check, chosen *now* —
   not after, when it is easy to pick whichever one passed.

Value order, when several candidates are level-pegged:

1. **A defect a buyer can hit** — dead link, invisible card, clipped CTA, a
   filter button that empties the grid.
2. **A false claim.** This site sells work; a sentence that is no longer true
   costs more than a thin page. The rules are not negotiable: no client claims
   on the self-directed demos (`ลูกค้าจริง` belongs to RAAT alone), no backend
   claims anywhere, no invented metrics, no PDPA copy.
3. **The thinnest proof strip.** A `#need` tile or a package page with one demo
   under it sends a buyer to a page that says "here is what I can do" and shows
   one thing.
4. **Reach** — a page that is unfindable: missing from `sitemap.xml`, missing
   from `search-index.json`, or an industry with no entry point.
5. **Polish.** Real, and last. Never the whole iteration while 1–4 are open.

⚠️ **The owner's calls are constraints, not candidates.** Thai is the default
language; the 8 `web-*` pages are Thai-only; the 20 demo pages carry no
portfolio chrome; `#need` has six tiles. Re-proposing one of these is how an
agent spends an iteration arguing with a decision that was already made — and
several are recorded in `BACKLOG.md` under **Rejected** for that reason. If one
genuinely looks wrong now, say so in one sentence and **ask**, don't ship.

---

## 3 · DO — smallest change that closes the finding

- Follow the recipe that already exists. A new card → the **portfolio-add-card**
  skill. A new industry page → CLAUDE.md's own step list, starting from a copy
  of `web-clinic.html`. Do not hand-build a skeleton from memory; five details
  of that one are wrong from memory every time.
- Edit **both** languages, or state why the page is exempt.
- No new CSS unless the change genuinely needs it. The two stylesheet families
  already carry every component these pages use, and a page must load exactly
  one of them.
- Do not widen the iteration because you are already in the file. A second
  improvement spotted mid-edit goes in `BACKLOG.md`, not in this diff.

---

## 4 · REVIEW — adversarially, and never from the diff alone

The diff tells you what you typed, not what the browser does. Run the checks
that can fail:

```bash
python3 _tools/loop-scan.py --defects   # must be clean (exit 0)
python3 _tools/check-copy.py
python3 _tools/check-deploy.py          # must be clean before any push
python3 _tools/sitemap-lastmod.py       # if any page content changed
```

Then, in a browser:

- **Lighthouse** on every page touched, mobile *and* desktop — a sidebar-only
  contrast failure is invisible to the mobile pass. Read the per-audit
  failures, never the category score alone: `label-content-name-mismatch` has
  weight 0 and fails silently at 100.
- **375 × 812 overflow.** `canScrollX: false` is necessary and **not
  sufficient** — `html, body { overflow-x: hidden }` hides real overflow, so
  sweep element right edges too. Two documented bugs hid exactly there.
- **Read the rendered page**, especially any copy you touched. Then re-grep the
  bare distinguishing token across all 96 files: repeated copy has variants,
  and one grep has twice reported "done" with the last variant still live.

Three failure modes to check yourself against before believing a result — all
three have wasted a session here:

- **A background tab freezes IntersectionObserver, CSS transitions and
  `scroll-behavior: smooth`.** Every reveal reports broken and every transition
  stuck at its start value, which looks exactly like the real bug. Check
  `document.hidden` first.
- **Headless Chrome renders `display=optional` fonts as the fallback, every
  time.** 86 of 88 files ask for it, so every measurement and every screenshot
  taken headless is in the wrong font unless you drive a real browser over CDP
  and `await document.fonts.ready`.
- **When an inline style fails to win, suspect the instrument**, not the page.

If a check cannot be run in this environment, say so plainly in the log and in
the reply. **Do not report a change as verified on checks you skipped** — that
is worse than shipping it unverified, because it stops the next iteration from
looking.

---

## 5 · RECORD — then stop

Append to `docs/improve-loop/LOG.md`, newest last, one block per iteration:

```markdown
## 2026-09-13 · <one-line change>
- **Finding** — the scan line or measurement that started it
- **Change** — what shipped, which files
- **Measured** — before → after, with the numbers
- **Verified** — the checks that ran, and any that could not
- **Learned** — the thing the next iteration should not have to rediscover
- **Spawned** — anything noticed and deliberately not done (→ BACKLOG.md)
```

`Learned` is the one that compounds. If an iteration produced no number and no
lesson, it was probably polish dressed as work — write that down too, honestly.

Then update `BACKLOG.md`: strike what shipped, add what you noticed, and put
anything you decided **against** under **Rejected** *with the reason*. A
rejected idea with no reason gets re-proposed in three iterations.

Ship it with the **portfolio-ship-change** skill (`main` auto-deploys; there is
no staging and no rollback but another push).

### Stopping is a valid iteration

If research turns up nothing above `GAP` and no thin spot worth a page, **say
so and stop.** Do not invent work to fill the loop — a site that is fine and a
site with an agent restyling its kickers every hour are not the same site, and
only one of them still has a `?v=` token you can trust. Rewriting working copy,
renaming tokens, adding a section nobody asked for and "modernising" a page
that measures fine are all make-work, and they cost review attention that the
next real defect will need.

---

## Running it

| How | What happens |
|---|---|
| "ทำ improve loop รอบนึง" / invoke this skill | one full iteration, then stop |
| `/loop /portfolio-improve-loop` | iterations, self-paced |
| `/loop 2h /portfolio-improve-loop` | one iteration every 2 hours |

On a schedule, two extra rules: never push two iterations without a REVIEW
between them, and if the same finding survives two iterations, stop and ask —
it means the fix is not the thing that is wrong.
