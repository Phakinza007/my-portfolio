---
name: portfolio-new-proof
description: >
  Add a new proof piece to Phakin's portfolio (my-portfolio) — a demo page plus
  its Thai and English showcase pages, wired into every place a project has to
  appear. Use for "เพิ่มผลงานใหม่", "ทำ demo ใหม่", "add a new project/demo/
  showcase", "เว็บ showcase เพิ่ม", or when portfolio-improve-loop decides the
  thinnest #related strip needs a second demo. This is the big unit of work on
  this site: ~14 places, and only some of them fail loudly when missed.
  For a card pointing at a page that already exists, use portfolio-add-card.
---

# portfolio-new-proof

One proof piece = **one demo page + two showcase pages + ~14 wiring points.**

The last one (`80cf976`, BAAN TALAY + SALON OS) touched **48 files**. Nothing
about that number is avoidable, and most of it does not fail loudly: a page
missing from `search-index.json` is simply unfindable on its own site, and
nothing reports it.

So the rule for this skill is: **the scan is the checklist.**

```bash
python3 _tools/loop-scan.py --defects
```

`scan_wiring()` asserts, for every showcase pair, that the card exists in all
four grid files, the copy has a canonical entry, the key is registered for
re-capture, all three screenshots are on disk, and `.story-price` is present.
All 19 existing pairs pass, so anything it says about yours is a step you
missed, not a new pattern. Run it after every step below, not only at the end.

---

## 0 · Which gap does this fill?

A proof piece is justified by a measured thin spot, not by wanting to build
something. From `loop-scan.py`'s `GAP` block, pick the page that has the least
proof and would gain the most:

- a **package page** at 1 (`dashboard-ui`, against `landing-page`'s 9)
- an **industry page** at 1 (`web-gym`, `web-solar`)

Best case one demo fills both at once — a dashboard for a specific industry
lands in `dashboard-ui`'s strip *and* that industry's `#related`.

⚠️ **The demo must be built for that sector, not assigned to it afterwards.**
Padding a strip with a loosely-related card is the failure `web-organization`
was kept at one entry to avoid. And **never append a demo to a group whose
eyebrow says `งานลูกค้าจริง`** — that turns a true sentence false. RAAT is the
only real client work on the site and the only card that may wear `ลูกค้าจริง`.

Write the decision down before building: which strip, which industry key, which
package, and what the demo proves that the existing 19 do not.

---

## 1 · The demo page — `<key>.html`

A demo simulates a client's site. It is **not** a portfolio page:

- **Its own inline CSS**, no shared reset. **Set `box-sizing` yourself** — a
  `width: 100%` plus horizontal padding overflows by exactly the padding, and
  that shipped as a clipped primary CTA on `construction-landing` that
  `canScrollX` could not see.
- **No portfolio chrome** — no site search, no "← Back to Portfolio" pill, no
  `portfolio-context.css`. Deleted 2026-08-07 on purpose.
- **Not `site-ui.js`.** Demos carry their own small reveal implementation.
- **No bare tag selectors.** `nav { … }` in `aesthetic-booking.html` later caught
  a footer `<nav>` and shipped cream-on-cream at 1.11:1. Use a class.
- `display=optional` on every font request, analytics tag before `</head>`,
  self-canonical, `robots: index, follow`, no `hreflang` (demos are shared by
  both languages).

**Three claims a demo may never make**, all paid for once already:

| Never | Why |
|---|---|
| a backend | Nothing here talks to one. 37 strings across 13 files said otherwise. Keep `fetch`/XHR/`<form action>` at **0** and say so in the copy. |
| a real client | All demos are self-directed. `ลูกค้าจริง` belongs to RAAT alone. |
| a metric nobody recorded | No invented conversion rates, no invented counts. |

If the page has a form, a payment block or a download list, it must be
**inert and visibly labelled** as inert — `action`-less, submit-less, a
placeholder account number, no dead download links. A convincing page that
appears to take real money or real bookings is worth marking unambiguously.

Every control that exists should do something. `BookEase.html` is the standard:
eleven toast-only stubs were made real client-side, and the four notification
switches that *cannot* work say so instead of faking success.

---

## 2 · Register the screenshots, then capture them

`_content/showcase-shots.json` first, `_tools/capture-shots.py` second. Three
views per demo:

| View | Size | File |
|---|---|---|
| A — landing / top | 1491 × 812 | `assets/screenshots/showcase-<key>.jpg` |
| B — the mechanism it brags about | 1491 × 812 | `…-b.jpg` |
| C — the same demo at phone width | 375 × 812 | `…-c.jpg` |

```bash
python3 _tools/capture-shots.py --key <key> --dry-run
python3 _tools/capture-shots.py --key <key>
```

View B needs a `selector` (and an `offset`), or its own `url` when the mechanism
is a *state* rather than a scroll position — a dialog cannot be scrolled to.
Both `label_th` and `label_en` are required; they are the caption, and they are
a claim about the image, so they have to describe what is actually in frame.

🔴 **Never stage a capture by hand.** The whole point of the script is that
re-capturing the set when a demo changes is one command. A hand-made image is
exactly the image that goes stale and never gets retaken — which is how 23
strings across 13 files described BuildNest's photographic rebuild as
"hand-drawn SVG instead of stock photography" for six days.

🔴 **Headless Chrome renders `display=optional` fonts as the fallback, every
time**, so a screenshot taken the obvious way is in the wrong font and silently
corrupts every measurement from it. `capture-shots.py` already drives a real
browser over CDP and waits on `document.fonts.ready`; run a positive control
(one string measured in both faces, required to differ) before trusting a
capture you took any other way.

---

## 3 · The card thumbnail — `assets/thumbs/<key>.svg`

**Measured, never drawn by eye.** Extract from the live page: read each
element's `getBoundingClientRect()` and computed style, inside a
**1440 × 1000 `<iframe>`** (this environment misreports the window size, and
`.bn-shell`-style `min()` widths then yield the wrong margins), and
**`await document.fonts.ready` before reading a single box** — measured early,
one heading reported 3 lines where the real face wraps to 4, and every
y-coordinate below it was wrong.

Six traps, each found only by comparing side by side at natural size:
`radial-gradient` fed to the linear parser (renders opaque black), text
positioned from the element box instead of a `Range` over its text nodes, only
`borderTopWidth` read, `transform` ignored, `border-radius` passed through
unclamped (SVG clamps `rx`/`ry` independently), and `letter-spacing` /
`text-transform` dropped.

**Compare at natural size only** (351.3 × 219.6). At any other scale a correct
SVG looks wrong, because the SVG scales with its viewBox and the original's
`rem` text does not.

⚠️ **An XML comment cannot contain `--`.** A comment mentioning a CSS custom
property makes the whole file fail to parse, and the card renders as a broken
image with no console error.

A thumbnail may be a **composition rather than a viewport crop** when a true
crop would cut off the thing the card exists to show — tighten dead space, keep
every element's own internal proportions.

---

## 4 · The two showcase pages

`showcase-<key>.html` (`lang="th"`) and `showcase-<key>-en.html` (`lang="en"`).
**Copy an existing pair; do not build the skeleton from memory.** Body layout is
the story stack, identical on all 19 pairs:

1. `.story-intro` — one muted line on how to read the page
2. `.story-stack` with exactly **four** `.story-card`s, each opening with a
   `.story-head` (`<h2>` + `.story-kicker`) and **no `.story-icon` badge**.
   They are four *shapes*: 1 bordered (overview + `.tag-list`), 2
   `.story-card--flat` (the 30-second version), 3 `.story-card--statement`
   (who it fits), 4 `.story-card.accent` (the ask) with `.story-price` and
   `.story-actions`
3. `.story-links`, then `#related` as its own section

**`.story-price` is required** and states the *site's* entry price, not this
project's: `ราคาเริ่มต้น ฿3,900 ขึ้นอยู่กับขอบเขตงาน — ดูราคาทั้ง 3 แพ็กเกจ`
(`-en`: "Pricing starts at ฿3,900, depending on scope"). It must stay a floor
statement — several of these projects start at the ฿7,900 package, so
"งานนี้ ฿3,900" would be false. Its selector is **`.story-card > p.story-price`**;
a lone class loses to `.story-card > p`'s margin reset.

Head, both files: `portfolio-pages.css` **only** (never both families), the
hreflang trio (`th` → Thai, `en` → `-en`, `x-default` → **Thai**), a
self-referential `canonical`, `og:locale` `th_TH` / `en_US`, the `.html`
redirect snippet, and the analytics tag before `</head>`.

The contextual nav stays contextual — `ดูเว็บจริง` points at *this* demo. If you
change a section id, fix that nav in the same edit; a restructure once left four
dead anchors behind.

---

## 5 · Canonical copy first, then paste it everywhere

`_content/project-copy.json` → `projects["showcase-<key>"]`, with `th` and `en`,
each carrying `long` (the `.work-problem` card and `#related` strips on category
and industry pages) and `short` (the tighter strips on showcase pages, needed
once any showcase links to you).

Write it **here first**, then copy it verbatim into every location. Fresh copy
written per page is how drift starts — it concentrated in exactly the newest
pages last time. Then:

```bash
python3 _tools/check-copy.py
```

⚠️ It checks that repeated copy agrees **with itself**. It cannot tell you the
copy is true — that needs reading the page it describes. And when it reports
drift, **decide which side is true before picking a winner**: the majority
variant has been the wrong one.

---

## 6 · The grid — four files, and the counts are by hand

Add the card to `index.html`, `work.html` (Thai slug) and `index-en.html`,
`work-en.html` (`-en` slug). Per card: `data-industry` (one or more of `clinic`
`booking` `restaurant` `shop` `gym` `construction` `solar` `other`), and
`data-tags` **pipe-separated** — eight labels contain a space.

🔴 **Edit `.filter-count` by hand in all four files.** They are a no-JS fallback
that `site-ui.js` overwrites on load, so wrong numbers are invisible in every
browser and nothing tells you they went stale — they sat wrong for days once.
`loop-scan.py` now derives the truth from the DOM and reports the mismatch; read
it off there, never off a table in a doc.

Every tag you add needs a `.tag-btn` in both `work` sidebars **or** it is
filterable by nobody (harmless — three already are). The dangerous direction is
a button with no card, which filters to an empty grid; the scan asserts it.

`work.html` / `work-en.html` also state the project count **in prose** — the
`.results-sub` line and all three meta descriptions.

---

## 7 · Reach — the parts that fail silently

| Place | What goes in |
|---|---|
| `sitemap.xml` | **three** URLs: the demo, and both showcase pages |
| `assets/search-index.json` | the two showcase pages, in **both** the `th` and `en` arrays, with hidden keywords (`k`) — the demo is not indexed, it carries no search |
| the matching industry page | a `.project-link` in `#related`, using `long` verbatim |
| the matching package page | same, if the demo fits that package |
| sibling showcase pages | their `#related` strips, using `short` verbatim |

Meta description ≤ 190 characters, or the scan flags it.

---

## 8 · Verify — then ship

```bash
python3 _tools/loop-scan.py            # wiring + defects; must be clean
python3 _tools/check-copy.py
python3 _tools/sitemap-lastmod.py      # never hand-edit <lastmod>
python3 _tools/check-deploy.py         # before any push
python3 _tools/serve.py 8123           # NOT http.server — extensionless URLs
npx -y lighthouse http://localhost:8123/showcase-<key> --quiet \
  --chrome-flags="--headless" --output=json --output-path=/tmp/lh.json
```

- **Lighthouse on all three new pages, mobile *and* desktop.** Read the
  per-audit failures, not the category score: `label-content-name-mismatch` has
  weight 0 and fails at 100. Best Practices caps at 77 sitewide (Clarity
  cookies) — that one is a deliberate trade, don't chase it.
- **375 × 812.** `canScrollX: false` is necessary, not sufficient:
  `overflow-x: hidden` hides real overflow, so sweep element right edges. A
  table inside `overflow-x: auto` that genuinely scrolls is correct, and
  collecting the scroller list before switching to the view that renders it is
  an instrument bug that invents 300–400px of overflow.
- **Read the rendered pages.** The showcase describes the demo; nothing
  re-reads it later.

Then ship with **portfolio-ship-change** and record the piece in
`docs/improve-loop/LOG.md`: which strip went from N to N+1, and what the demo
proves. That log line is what stops the next iteration re-filling a strip that
is now the fattest on the site.
