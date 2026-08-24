# ปฐพีพรีคาสท์ — a B2B precast demo and its showcase pair

Date: 2026-08-24
Status: built

## Why this project exists

Measured before this work, `web-construction.html` carried **one** entry in its `#related`
strip, and the three thinnest industry pages were also the three whose demo count was one:

| industry page | entries before |
|---|---|
| `web-clinic` | 3 |
| `web-booking` · `web-restaurant` · `web-shop` · `web-organization` | 2 |
| `web-construction` · `web-gym` · `web-solar` | **1** |

`web-construction` and `web-gym` are two of the six tiles in the `#need` selector, so they
take the most intent traffic of the eight and had the least to show it. Construction was the
owner's pick.

A second measurement decided the *shape*: the three category pages carry wildly uneven proof.

| category page | package | `.project-link`s before |
|---|---|---|
| `landing-page` | ฿3,900 | 9 |
| `business-website` | ฿9,900 | 5 |
| `dashboard-ui` | ฿7,900 | **1** |

This project is a ฿9,900-shaped page, so it also lifts `business-website` from 5 to 6.
`dashboard-ui` remains the thinnest strip on the site and is the obvious next one.

## The demo had to be a different buyer, not a different palette

`construction-landing.html` (BuildNest) is already a B2C general contractor: four service
types, eight photographs, a warm teal-and-gold page aimed at someone building a house. A
second construction demo that differed only in colour would be padding, which is exactly what
the rule above `#related` on the industry pages forbids.

So this one sells **to a purchasing department**: precast floor slabs, columns, beams and wall
panels, bought on span tables and lead times by someone comparing three suppliers at once.

An asset measurement then fixed the visual direction rather than taste doing it.
`assets/construction/` holds eight files and `construction-landing.html` already uses six.
The two spares are `planning.jpg` and the superseded `hero.jpg`. Reusing `rebar.jpg` or
`tower.jpg` would put an identical photograph on two demos **in the same industry**, and those
two demos now sit next to each other in `web-construction`'s strip, where anyone opening both
would see it. There was no industrial photography to use.

That constraint happens to agree with the buyer: a procurement officer does not choose a
supplier from a hero shot.

## The design direction

The palette is downstream of a written scene, the method `lumi-clinic.html` and
`bandairaek-foundation.html` both use:

> A precast yard at six in the morning. The crane has not started. The dust has not risen.
> Hollow-core slabs are stacked in piles as tall as a man, and every slab has its lot number
> brushed on the end in burnt orange. The shift foreman is walking the row checking today's
> delivery list off a single clipboard.

Three things that scene rules out, each a decision rather than a default:

**1. Safety orange and hi-vis yellow as large fills.** That is the template every construction
page in this category ships with. In the scene the burnt orange is a lot number written on a
slab, so on the page `--mark: #A8431A` appears only as dimension lines, the currently selected
spec value, the `.hit` row in the selector, and the quote button. It is a data encoding, never
a surface — the same rule bandairaek applies to its forest green and ochre.

**2. A full-page blueprint field.** `solar-landing.html` owns that on this site already (two
1px gradients tiled at 22px as a `<pattern>`). This page is also drafting-flavoured; sharing
the ground would make the two read as twins. `showcase-solarpeak`'s strip now points here, so
they are one click apart.

**3. Flat industrial grey.** Concrete at six in the morning is not `#888888`. The paper
`#E9EBE7` sits near hue 130 at very low chroma, deliberately away from the cool blue paper
bandairaek uses (hue ~240) so the two no-photograph pages on this site do not share a ground.

Type is **Anuphan + Roboto Mono**. The first draft specified IBM Plex Sans Thai + IBM Plex
Mono before checking, which is exactly what `bandairaek-foundation.html` already uses — two
pages sharing both a cool light paper and a typeface. Neither Anuphan nor Roboto Mono appears
on any other page in the repo.

**There are no photographs anywhere on the page, and the page says why in running text near
the top.** This is the second no-photograph page on the site and the reason is *not* the same
one: bandairaek refuses photography on ethical grounds (a foundation should publish its
records rather than its beneficiaries' faces), while this page argues a commercial point —
that the buyer decides from a span table, so a stock photo of a stock yard answers nothing.

## What was built

| file | role |
|---|---|
| `pathapee-precast.html` | the demo — own inline CSS, own reset, no portfolio chrome, 83 KB |
| `showcase-pathapee.html` / `-en.html` | the showcase pair, story stack, identical to the other 16 pairs |
| `assets/thumbs/pathapee.svg` | card thumbnail, composed from measured page geometry |
| `assets/screenshots/showcase-pathapee.jpg` | 1491 × 812 hero screenshot |

Wired into: the card grid on `index` / `index-en` / `work` / `work-en`, the static filter
counts in all four (`all` 17 → 18, `construction` 1 → 2), the prose project counts on
`work` / `work-en` (four strings each), `_content/project-copy.json`,
`assets/search-index.json` (both languages), `sitemap.xml` (3 URLs),
`web-construction`'s `#related` (1 → 2), `business-website` / `-en` (5 → 6), and the
`#related` strips on `showcase-buildnest` / `showcase-solarpeak` (± `-en`), where MuseRoom —
a dark gallery landing page, the least adjacent neighbour on either — was swapped out so each
strip stays at three.

No new tag button was needed: the card's `data-tags` are
`Construction|UI Design|Light UI|Thai|Interactive`, all five of which already own a pill.

## The page's own content

Nine sections: hero → why-no-photographs → `#catalog` → `#selector` → `#plant` →
`#schedule` → `#standards` → `#projects` → `#faq` → `#quote`.

`#catalog` is a four-tab product catalogue (solid plank, hollow core, column/beam, wall panel).
Each tab pairs a **cross-section drawn as SVG** — real dimension lines, real values, prestress
strands at the soffit — with a span-against-live-load table. The tabs follow the correct tab
pattern: roving `tabindex`, arrow keys wrapping, Home/End.

`#selector` is the piece that makes this a ฿9,900 page rather than a brochure. Drag a span,
pick a live load, enter a floor area, and it reports which of six models still pass, marks the
thinnest passing one, and derives piece count, tonnage and truck trips. It reads the same
numbers the catalogue tables show, from one array in the page. Nothing is fetched.

`#plant` states output, casting beds, stock area, fleet and the next free production slot, and
draws the delivery radius as a **diagram, not a map** — no third-party key, no external
request.

## Two things are deliberately inert, and say so

No demo on this site talks to a backend and the copy must never imply one does. Both places
where this page could have implied it are labelled in words:

- The **document list** under `#standards` shows type, size and modified date for five files
  and is *not* linked, with a paragraph saying the files do not exist yet. Dead download links
  would have been the alternative.
- The **quote form** has no `action`, no submit button, and a dashed panel stating that it
  sends nothing anywhere and that a real site would wire it to the sales inbox.

The footer repeats that the company, its figures and its project list are invented.

## Two measurement traps this project paid for

**🔴 Chrome here has no Thai line-break dictionary, so an unspaced Thai run breaks at any
character.** The `h1` shipped as `...จากตารางส / แปน`, split mid-word. Established by probe,
with a control: `"ตารางสแปน"` in a 90px box breaks at character 5, while the Latin control
`"concretehollowcore"` in the same box refuses to break at all. `word-break: keep-all` was
tried, computed correctly as `keep-all`, and changed the rendered height by **zero pixels** —
it does not apply to Thai in this engine. `text-wrap: balance` does not help either; it
rebalances the same bad break opportunities.

The fix is structural: every phrase in every `h1`/`h2`/`h3` is wrapped in
`<span class="nb">` with `white-space: nowrap`, which leaves the spaces between phrases as the
only break opportunities the browser is given. **Heading copy on this page must therefore
carry spaces at real phrase boundaries**, and four headings were rewritten to add them.

That has a cost worth knowing: a `nowrap` run that does not fit simply overflows. Measured at
375px, two spans came out 387px wide against a 371px viewport — clipped by
`html, body { overflow-x: hidden }`, so `canScrollX` stayed `false` and the standard mobile
check saw nothing. This is the same failure mode as `construction-landing`'s clipped CTA.
Both were split further and re-measured. **Any new heading here needs the 375px span-width
check, not just `canScrollX`.**

This is not specific to this page — it is how Thai wraps on all 88 files. Nothing else on the
site was touched.

**⚠ Headless Chrome renders `display=optional` webfonts as the fallback, every time.** The
first three attempts at the hero screenshot were captured with `--headless --screenshot` and
`--virtual-time-budget`, and produced a page laid out in a system font: `ch`-based
`max-width` resolved differently and the `h1` came out two lines instead of three. Warming
the font cache with a persistent `--user-data-dir` changed nothing — the three renders were
**byte-identical** — because `display=optional` decides at ~100ms of *virtual* time, before
the font can arrive, on every load.

The working path is CDP against a real browser: navigate twice so the second load has the font
on disk, `await document.fonts.ready`, then `Page.captureScreenshot`. A positive control runs
before the capture is trusted — the same string measured in Anuphan and in the fallback stack,
which must differ (626px vs 655px) — because a capture in the wrong font looks completely
normal and is wrong in every measurement taken from it.

## Redesign, same day: the first build measured as flat

The first build was reviewed as "ไม่ค่อยสวย" and the reason turned out to be measurable
rather than a matter of taste. Every block sat on a tinted card, and:

| measured | value |
|---|---|
| `--sheet` against `--paper` | **1.13:1** |
| `--paper-2` (the alternating band) against `--paper` | **1.08:1** |
| distinct painted surface colours on the whole page | **2** |
| dead vertical space from `align-items: start` on four grids | **435px** |
| band heights, nine sections | 536–835px, no rhythm |

At 1.13:1 a card is not a surface. Every box on the page was carried by a single hairline,
which is why the whole thing read as an unfinished wireframe.

**Research.** The US precast majors (Clark Pacific, Jensen, Coreslab) were captured and
discarded: all three are photography-led marketing sites behind modals, which is the lane
this page deliberately refuses. The useful references were a category over — spec-led pages
that are still good-looking. [Teenage Engineering](https://teenage.engineering) and
[McMaster-Carr](https://www.mcmaster.com) both do the same three things: commit to real
black and real white rather than three greys, let one accent be genuinely loud, and put the
density in the type and the rules instead of in tinted boxes. McMaster has no card anywhere
in its catalogue.

**What changed.** The card metaphor is gone.

- Ground is near-white `#FBFBF9`; the only filled surface left is the drawing sheet, which is
  white with a **drawn 1px ink border and a real title block** ruled into three cells.
- `--r: 4px` → **0**. A drawing sheet has square corners, and the radius alone was carrying a
  lot of the generic-card reading.
- Sections are separated by rules, not by an alternating tint. The alternation is deleted.
- **One dark band, at `#plant`.** Ten light sections in a row read as one flat scroll; the page
  needed at least one real contrast event between the hero and the footer.
- Form fields are **underlines, not boxes**; `input[type=range]` is styled (it had been shipping
  as the browser default); the span readout jumps to 3.4rem mono.
- Tables lose their box and their filled steel header: a 1px ink rule under the head, hairlines
  between rows, and **rows that fail the span are dimmed rather than left looking identical to
  passing ones** — information the first build rendered but did not encode.
- `verdict` and `derived` now emit markup so the figures carry the accent. They were plain
  `textContent`, so the payoff line of the whole tool was unemphasised grey.
- The delivery-radius ring diagram is replaced by a **distance ladder**. The ring put seven
  labels around one circle and three of them overlapped (`กรุงเทพฯ 70` over `สมุทรปราการ 45`);
  its crosshair axes meant nothing and its ring labels floated unanchored. A ladder cannot
  collide, sorts by distance, and carries the over-100km freight rate as a second encoding.
- The inert notice moved to full width under both quote columns, closing 223px of dead space
  and giving the one block that must not be missed more presence.

`assets/thumbs/pathapee.svg` was rebuilt to match. A palette change is never one file — that
card appears on `index`, `index-en`, `work` and `work-en`.

Result: **0 contrast failures** across every text node on the page, and dead space in the three
two-column grids down from 136 / 72 / 223px to 0 / 17 / 103px.

⚠️ **The font positive control earned its keep during this pass.** Patching
`Network.setCacheDisabled` into the capture script to defeat HTML caching also defeated the
two-load warm-cache strategy the screenshot depends on, and the control caught it immediately:
`anuphan 655 = fallback 655`. The capture looked entirely normal. The fix is to bust the cache
per navigation with a query parameter and leave the font cache alone.

## Third pass: the `impeccable` skill

The owner pointed at a video (*"Turn Claude Into A Design GENIUS In 3 Simple Steps"*) whose
method is: build a taste library, add a design skill, then cast wide and narrow down. Its
step two names **Impeccable**, which was already installed in this repo's toolchain and had
not been used. Running it found things two rounds of hand-measurement had missed, because
they are category tells rather than measurable defects.

`scripts/detect.mjs` flagged four; `reference/brand.md` supplied the rest.

| finding | source | resolution |
|---|---|---|
| `border-left: 3px solid` on `.inert` | detector, **absolute ban** | full 1.5px border plus a `SPECIMEN` corner tag. The two `inset 3px 0 0` stripes on the chosen table row and the active tab were the same move by another property; both replaced with tint and colour |
| Roboto Mono is an overused face | detector | **Overpass Mono**, which descends from Highway Gothic — road-signage lineage is a real reason to sit in the technical lane on an infrastructure page rather than mono-as-costume |
| 8 em-dashes in body copy | detector | 2. Four were `<option>` separators (now `·`); the dash-clause-dash sentence was rewritten |
| numbered markers `01`–`05` | detector, advisory | **kept.** brand.md permits numbers when the section genuinely *is* a sequence; `#schedule` is a five-stage production run with day counts, and it is the only numbered sequence on the page |
| a tracked mono kicker above **all nine** sections | brand.md | 8 deleted, 1 kept (the one that asks a question its heading answers). An eyebrow on every section is the scaffold; the headings took the size instead |
| one identical fade on every section | brand.md | the delivery bars now draw from zero on reveal, which fits what they are |
| the reveal gated content at `opacity: 0` | brand.md | only below-the-fold elements are ever hidden, so no-JS, a hidden tab and a headless render all get the finished page |
| slider 2px tall, nav links 17px | audit.md | 34px and 44px hit areas |

🔴 **Then Lighthouse accessibility fell to 97, and the cause is worth keeping.** axe reported
foreground colours that appear nowhere in the token set — `#a2a7a8`, `#7a7c7c`, `#cd947c`
against tokens of `#5C6568`, `#6A7275`, `#A8431A` — across 164 nodes. Those are **composited**
colours: back-solving `162 = α·92 + (1−α)·251` gives α ≈ 0.56, and another node gives 0.81.
Lighthouse was measuring the page mid-reveal, and a partially-faded element fails
colour-contrast on its blended value. The previous `opacity: 0` gate had hidden this because
axe skips fully transparent nodes.

The fix is to **never fade text on a scroll reveal**: the animation is transform-only, so every
text node is at full opacity at every frame and axe measures the real token. Motion survives as
travel plus the bar draw. a11y is back to 100 and performance rose from 85 to 98, because the
reveal had been suppressing LCP.

**What did not apply, and why.** Step one of the video is a Dribbble/Pinterest inspiration
library; for this page that would pull toward the generic marketing aesthetic it exists to
refuse, so the references stayed targeted (technical catalogues and spec-led product pages).
Higgsfield MCP generates hero imagery, and this page carries no photography by rule. 21st.dev
is a React component source, and this is one file of hand-written CSS.

## Fourth pass: motion

The page had two transitions and zero keyframes after the accessibility fix, which is close
to static. The motion added is the page's own subject rather than decoration: **the drawings
draw themselves.** Each stroke is dashed to its own `getTotalLength()` and the offset runs to
zero — outline first, voids staggered, strands landing at 620ms, dimension lines at 750ms, and
the labels travelling in last. The catalogue sections draw the first time their tab is opened.
Alongside it the plant figures count up, the catalogue panel slides on tab change, and the
span readout and derived figures nudge when they change.

Three rules govern all of it, and each was learned the hard way earlier in this build:

1. **Nothing containing text animates opacity.** axe measures the composited colour of a
   partially faded node. This is the single constraint that keeps accessibility at 100.
2. **Every hidden start state is gated behind `[data-anim]`, which only JS sets.** Without it
   `.fill` and `.strand` sat at `scale(0)` in the stylesheet, so a visitor without JS lost the
   concrete and the prestressing strands entirely. With the gate, no-JS renders the finished
   drawing.
3. **No bounce.** Two `cubic-bezier` curves overshot past y = 1; the detector flagged both as
   `bounce-easing`. Replaced with ease-out-quart.

⚠️ **Verifying this needs the transition disabled, never a wait.** Chrome freezes CSS
transitions in a hidden tab, so stepping through the animation and reading computed values
returns the start value at every timestamp — which looks exactly like "the animation is
broken" and is not. Both apparent bugs found while testing this pass were that artifact. The
real check is: inject `* { transition: none !important }`, toggle the class, and read the two
end states (`stroke-dashoffset` 1214px → 0px, `.fill` `scaleX(0)` → `scaleX(1)`).

## Verification

| check | result |
|---|---|
| Lighthouse a11y / best-practices / SEO, all 3 new pages | 100 / 100 / 100 |
| `impeccable` detector | 1 advisory left (`numbered-section-markers`), kept deliberately |
| touch targets under 24px | 0 |
| Lighthouse performance | 98 (demo), 83–94 (showcase); 81 / 76 on the first build |
| horizontal overflow, per-element sweep at 375 / 768 / 1440 | 0 real leaks; `canScrollX` false; verified with an injected-overflow positive control (63 → 65) |
| mid-word heading breaks at 375 and 1440 | 0 |
| dead links / dead anchors across 90 files | 0 / 0 |
| duplicate ids on the 3 new pages | 0 |
| text contrast, every rendered text node against its painted background | 0 failures |
| `_tools/check-copy.py` | 227 occurrences across 21 projects, all agree |
| `_tools/check-deploy.py` | no versioned asset changed |
| tag buttons with no card, `work` and `work-en` | 0 |
| sitemap | 90 URLs, parses, no duplicates |
| selector arithmetic, spot-checked | 420 m² ÷ (1.2 × 6.0) = 59 pieces; × 195 = 81.9 t; ÷ 18 = 5 trips |

Best Practices reads 100 here only because Microsoft Clarity does not load on localhost. Live
it will return to the accepted 77 cap.
