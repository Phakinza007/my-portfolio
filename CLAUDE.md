# CLAUDE.md — Phakin Chawanpunya Portfolio

## Skills

- **portfolio-add-card** (`.claude/skills/portfolio-add-card/SKILL.md`) — full workflow for adding a new project card. Trigger: any request to "add [page] to the portfolio", "link this page", "create a card for X", or "new project card".
- **portfolio-ship-change** (`.claude/skills/portfolio-ship-change/SKILL.md`) — pre-deploy
  checks. Trigger: "deploy", "ship it", "push", or any change touching both an `assets/`
  stylesheet/script and a `.html` file. Run `python3 _tools/check-deploy.py` before pushing;
  it fails when a versioned asset changed and its `?v=` token did not, which is invisible
  locally and invisible to Lighthouse.

---

## Project Overview

Personal frontend portfolio hosted on GitHub Pages.  
URL: https://ph-akin.dev/

**Owner:** Phakin Chawanpunya  
**Stack (this site):** HTML · CSS · JavaScript (vanilla, no framework)  
**Stack (the owner's work generally):** also WordPress · Elementor · FullCalendar — see the
RAAT case study. The line above describes this repository, not the range of work on offer;
do not cite it as the latter.  
**Hosting:** GitHub Pages (`main` branch, auto-deploys), custom domain `ph-akin.dev` (live as of
2026-08-06 — DNS A/AAAA records at name.com point to GitHub Pages, `CNAME` file in repo root)

---

## Project Structure

```
my-portfolio/
├── index.html                    # หน้าแรก — THAI (default, served at ph-akin.dev/)
├── index-en.html                 # หน้าแรก — English
├── resume.html / resume-en.html  # Resume / CV (th / en)
├── 404.html                      # Custom dark-theme 404 page
├── sitemap.xml                   # All URLs (both languages) for Google Search Console
├── robots.txt                    # Allows all crawlers, points at sitemap
├── CNAME                         # ph-akin.dev custom domain
│
├── assets/
│   ├── thumbs/                   # 12 card thumbnails, all SVG (see Card Thumbnail Approach)
│   ├── screenshots/              # showcase-*.jpg hero screenshots
│   ├── social-preview.png        # OG image (1200×630)
│   ├── favicon.svg
│   ├── analytics.js              # Microsoft Clarity loader + click tracking (shared)
│   ├── site-ui.js                # reveal + mobile drawer + work filter — 12 portfolio pages
│   ├── site-search.js            # search widget; builds its own markup into an empty div
│   ├── search-index.json         # hand-maintained, 33 entries per language
│   ├── resume-phakin-chawanpunya.pdf
│   ├── home-shell.css            # index / work / services / about / faq / process (+ -en)
│   └── portfolio-pages.css       # resume / case study / showcase / category / web-* pages
│
├── case-study-*.html             # 4 case studies — THAI
├── case-study-*-en.html          # 4 case studies — English
├── showcase-*.html               # 15 project showcase pages — THAI
├── showcase-*-en.html            # 15 project showcase pages — English
├── landing-page.html / landing-page-en.html       # Service category page — Landing Page (฿3,900)
├── dashboard-ui.html / dashboard-ui-en.html        # Service category page — Dashboard UI (฿7,900)
├── business-website.html / business-website-en.html # Service category page — Business Website (฿9,900)
├── web-*.html                    # 8 industry landing pages — THAI ONLY, no -en twin
│                                 # clinic · booking · restaurant · shop · gym · construction ·
│                                 # solar · organization
├── work.html / work-en.html      # Full archive — 13 projects + filter + 4 case studies
├── services.html / -en           # 3 packages + price comparison + 7 industry entry points
├── about.html / -en              # Bio, experience, tools, KMUTT
├── faq.html / -en                # 10 pre-hire questions + FAQPage JSON-LD
└── process.html / -en            # Brief → delivery, 5 steps
```

---

## Bilingual structure (TH default / EN alternate)

**Thai is the site default.** `ph-akin.dev/` serves Thai. English lives on `-en` siblings.

| Language | URL pattern | `<html lang>` |
|----------|-------------|---------------|
| ไทย (default) | `/` · `/{slug}.html` | `th` |
| English | `/index-en.html` · `/{slug}-en.html` | `en` |

21 pairs (42 files): `index`, `resume`, 4 × `case-study-*`, 15 × `showcase-*`.

**Rules any change must preserve:**

- Every pair carries the same 3 `hreflang` links in both files:
  `th` → Thai URL, `en` → `-en` URL, `x-default` → **Thai URL** (Thai is the default).
- `canonical` on each file points at **itself**, never at its counterpart.
- **Internal links stay in-language.** A Thai page links to Thai pages (`{slug}.html`);
  an `-en` page links to `-en` pages. The only cross-language link is the nav
  switcher (`TH` / `EN`).
- `href="/"` means the **Thai** homepage. English pages must use `index-en.html`.
- `og:locale`: `th_TH` on Thai, `en_US` on English.
**Two page classes deliberately have no `-en` twin. Neither is unfinished work — do not
"fix" them by generating `-en` siblings:**

1. The **13 project demo pages** (`construction-landing.html`, `gym-landing.html`, …)
   are simulated client work. Both languages link to the same demo file. Same for
   GitHub / Fastwork / Vercel links.
2. The **8 industry landing pages** (`web-clinic`, `web-booking`, `web-restaurant`,
   `web-shop`, `web-gym`, `web-construction`, `web-solar`, `web-organization`). The search intent
   (`รับทำเว็บคลินิก`) is Thai-only, so an English twin would double the file count for
   traffic that does not exist. Both languages' `#need` selectors link to the same
   Thai pages.

Both classes carry: **no `hreflang` links at all**, a self-referential `canonical`, and
`robots: index, follow`.

See `docs/superpowers/specs/2026-08-06-th-en-language-toggle-design.md`.

---

## Current Cards in Selected Work (16 cards — 15 projects + the RAAT case study)

The card links to its **showcase page**; the showcase page's "ดูเว็บจริง" link goes to the
**demo file**. The old version of this table conflated the two.

| # | Name | Card → | Live demo | `data-industry` |
|---|------|--------|-----------|-----------------|
| 1 | BuildNest Construction | `showcase-buildnest.html` | `construction-landing.html` | `construction` |
| 2 | Iron Republic | `showcase-iron-republic.html` | `gym-landing.html` | `gym` |
| 3 | NOIR Coffee | `showcase-noir-coffee.html` | `coffee-landing.html` | `restaurant` |
| 4 | Elevate Commerce | `showcase-elevate-commerce.html` | `ElevateCommerce.html` | `shop` |
| 5 | Elasticshop Gaming Top-Up | `showcase-elasticshop-gaming.html` | `elasticshop-gaming.html` | `shop` |
| 6 | Signalform Studio | `showcase-signalform.html` | source: `_studio-src/signalform` (React 19 + Vite) | `other` |
| 7 | SupplyMate Wholesale | `showcase-supplymate.html` | external: `https://phakinza007.github.io/supplymate-wholesale/` | `shop` |
| 8 | RATRI Restaurant | `showcase-ratri-restaurant.html` | `sorn-restaurant.html` | `restaurant` |
| 9 | SolarPeak | `showcase-solarpeak.html` | `solar-landing.html` | `solar` |
| 10 | BookEase Dashboard | `showcase-bookease.html` | `BookEase.html` | `booking` |
| 11 | MuseRoom | `showcase-museroom.html` | `MuseRoom.html` | `other` |
| 12 | LUMI Clinic | `showcase-lumi-clinic.html` | `lumi-clinic.html` | `clinic` |
| 13 | BRIGHT Dental Clinic | `showcase-dental-clinic.html` | `dental-clinic.html` | `clinic` |
| 14 | VELVÉ Aesthetics | `showcase-velve-aesthetics.html` | `aesthetic-booking.html` | `clinic booking` |
| 15 | HabitQuest | `showcase-habitquest.html` | external: `https://habitquest-pi.vercel.app/` | `other` |
| 16 | **RAAT Competition Calendar** | `case-study-raat.html` | external: `https://www.raat.or.th/competition-calendar/1442/` | `other` |

**Card 16 is the only real client work on the site.** The other fifteen are self-directed
design pieces. It is the one card that may carry the `ลูกค้าจริง` tag, and that tag must never
appear on the other fifteen — it was stripped from twelve files on 2026-08-07 for exactly
that reason. RAAT also appears as the fifth `#case-studies` card, deliberately in both places.

**SupplyMate (card 7) is the second project that lives in its own repository**, alongside
HabitQuest. It is a React + Vite + TypeScript app deployed to GitHub Pages at
`phakinza007.github.io/supplymate-wholesale`, source at
`github.com/Phakinza007/supplymate-wholesale`. What is deployed is the **static showcase
build**, not the full application in that repo: home, `#/shop`, `#/products/:slug`, `#/cart`
and a simulated `#/checkout`, with a browser-only cart and no network calls. There is **no
login, no admin, no payment-slip upload and no order history** in the published demo, and
`showcase-supplymate.html` must keep describing only what is deployed. The 2026-08-07 plan
predates that decision and still describes an admin/slip-upload build — do not write the
showcase page from the plan.

**On `index.html` the `#projects` filter runs on `data-industry` alone.** Keys: `clinic`,
`booking`, `restaurant`, `shop`, `gym`, `construction`, `solar`, `other`. The archive adds a
second axis on top of it — see "The work archive" — but the homepage has only this one.
`other` is load-bearing —
MuseRoom, HabitQuest and RAAT match none of the seven industries and would vanish from the
filter without it. Counts are derived from the DOM at runtime, so the static `.filter-count`
values are only a no-JS fallback.

⚠️ **Because they are a fallback, nothing tells you when they go stale.** They sat at
`all 13 / other 2` from the day the RAAT card was added until 2026-08-08 while the DOM had
already been at `14 / 3` — `site-ui.js` overwrites them on load, so the wrong numbers were
invisible in every browser and only showed with JS off. They are now `all 16 / other 4`.
**Adding or removing a card means editing these by hand in all four grid files** (`index`,
`index-en`, `work`, `work-en`); read the truth off the DOM rather than counting the table
above. `work.html` / `work-en.html` also state the project count in prose — the
`.results-sub` line and all three meta descriptions.

The featured carousel clones `.work-card`s and **must** strip `data-industry` from the clones
(`clone.removeAttribute('data-industry')`). Miss it and five clones leak into every filtered
result — "ทั้งหมด" reports 20 instead of 15.

Visible card tags are **Thai buyer search terms** (`คลินิกทันตกรรม`, `จัดฟัน`, `ขอใบเสนอราคา`),
not style descriptors. `index-en.html` carries English equivalents but the same
`data-industry` keys.

> Culled 2026-07-22 (still in git history): Admin Inventory, Braw & Co, Task Manager,
> Knowledge AI, Weather Dashboard — weakest/template-looking or redundant with BookEase.

---

## Card Thumbnail Approach

**14 of the 16 cards are `<img src="assets/thumbs/*.svg">`**, and `assets/thumbs/` holds
exactly those 14 files. The other two carry real photographs and always should: VELVÉ
(`assets/velve/care-tools.jpg`) and RAAT (`assets/raat/competition-calendar.jpg`). The
inline-styled `<div>` mini-UIs
they used to be were transcribed to SVG on 2026-08-07 — 161.5 KB of HTML removed from the
four files that carry the grid (`index`, `index-en`, `work`, `work-en`), against 64 KB of
SVG the browser fetches once and caches across every page. `index.html` went 151 → 103 KB.

The SVGs were **not redrawn by eye**. A browser-console extractor read each element's
`getBoundingClientRect()` and computed style at the card's natural size (351.3 × 219.6) and
emitted a `<rect>` or `<text>` per shape, so flexbox was resolved to numbers before anything
was transcribed. Six things the first version silently got wrong, each found only by
comparing side by side at natural size — if you ever rerun this, they are the traps:

| Trap | Symptom |
|---|---|
| `radial-gradient` fed to the linear parser | first stop becomes `stop-color="at 60% 30%"` → renders **opaque black** |
| text positioned from the element box | a flex-centred button label lands in the box's top-left corner (use a `Range` over the text nodes) |
| only `borderTopWidth` read | a header ruled with `border-bottom` alone vanishes |
| `transform` ignored | `getBoundingClientRect` returns the transformed AABB — a 45° chevron squares off, a skewed bar stands upright |
| `border-radius` passed through unclamped | CSS clamps to `min(w,h)/2`; SVG clamps `rx`/`ry` **independently**, so `99px` on a 56×12 pill becomes a full ellipse |
| `letter-spacing` / `text-transform` dropped | tracked-out wordmarks render tight; `SELECT PACKAGE` becomes `Select Package` |

**Compare at natural size only.** At any other scale the SVG scales with its viewBox while
the original's `rem`-sized text does not, so a correct SVG looks wrong. A three-up comparison
at 0.72 scale once produced a false "all three are broken" verdict.

Two effects are hand-patched because the flat-rect model cannot express them: Iron Republic's
scanline and SolarPeak's blueprint grid (two 1px gradients tiled at 22px) are `<pattern>`s.
SolarPeak's is swapped into the existing rect's `fill` **in place** so it keeps its z-order
behind the content — appending it would paint over everything.

**Three never had a `<div>` mini-UI to transcribe.** Two of those are hand-drawn; the third
was measured off its own live page instead:

- `assets/thumbs/bright-dental.svg` — that card was a remote `images.unsplash.com` photo.
  Its palette is read off `dental-clinic.html` (ink `#120F0C`, paper `#F7F2E9`,
  coral `#FF5B3B`).
- `assets/thumbs/supplymate.svg` — the source is a React app on another origin, so there is
  nothing local to extract. Palette and geometry were still **measured, not eyeballed**:
  colours sampled by painting the app's `oklch()` values onto a 1×1 canvas and reading the
  pixel back (`getComputedStyle` returns `oklch()` verbatim in Chrome, and feeding that
  string to `canvas.fillStyle` does not convert it either) — bg `#f8f7f2`, card `#fefdfb`,
  navy `#152f4b`, ink `#121b26`, line `#d3d1c8`, muted `#545f6c` — and card proportions read
  off `getBoundingClientRect()` on the live catalogue, scaled 0.288. It is a **composition,
  not a viewport crop**: at true scale the 220px-tall frame would cut off the price lines,
  which are the whole point of the card, so the vertical spacing is tightened while each
  element keeps its real internal proportions.
- `assets/thumbs/construction-landing.svg` (BuildNest) — rebuilt 2026-08-12. The file it
  replaced predated the transcription batch and was never part of it: an illustrated
  1200 × 750 poster with readable display text, decorative circles and an isometric
  building, drawn in rounded dark green against a page that is teal `#123d45`, gold
  `#c9922f` and 2px corners. Nothing about it was measured. It is now extracted from
  `construction-landing.html` itself — see **Extracting from a live page** below.

The two hand-drawn files clip their photo areas with a `<clipPath>` per card. Drawing a
square-cornered "table" rect straight over a rounded image rect leaves the corners poking
out — subtle at natural size and invisible at any smaller scale.

**XML comments cannot contain `--`.** A comment mentioning `--ink` makes the whole SVG fail
to parse, and the card renders as a broken-image icon with no console error.

Tag colour classes:
- `tag-mint` — AI, SaaS, Developer tools, Green-tech, Weather
- `tag-amber` — Finance, Energy, Fine Dining, Warm/luxury brands
- `tag-gray` — Default: Dashboard, Landing Page, Brand, Booking, etc.

### Extracting from a live page

Reading the page rather than a card-sized `<div>` adds two traps the 2026-08-07 batch never
hit. Both were paid for on `construction-landing.svg`:

**Measure inside a 1440 × 1000 `<iframe>`, not in the window this environment gives you.**
The automated browser here reported a 1960px viewport for a 1440px resize request. `.bn-shell`
is `min(1280px, 100% - 48px)`, so that viewport yields 17% side margins where a real 1440px
one yields 5.6% — the thumbnail would have read as inset from nothing, and no other thumb in
the set looks like that. An iframe evaluates the page's own media queries against the
iframe's box, which is the same mechanism the "Check mobile overflow" recipe uses at 375px.

🔴 **`await document.fonts.ready` before reading a single box.** Every page here loads fonts
with `display=optional`, so the first paint uses the fallback. Measured too early,
`#hero-heading` reported **three** lines of 114.9px; with Noto Serif Thai actually loaded it
wraps to **four** of 86.1px, the third a one-word orphan (`คุณ`). That is not a rounding
error — every y-coordinate below the headline was wrong and the whole file had to be
rewritten. `getBoundingClientRect()` is honest about what is rendered and has no way to tell
you a different face is still in flight.

Two further notes, both consistent with how supplymate was done:

- **A photographic hero is composited, not picked.** Sample `hero.webp` through a canvas —
  replicating `object-fit: cover` and `object-position: center 55%` by hand, since the canvas
  will not do it for you — then blend the result under the page's own overlay
  (`rgba(4,32,38, .93 → .81 → .51)`) to get the three stops of the SVG's gradient. Reading a
  colour off a screenshot instead bakes in the JPEG's own shifts.
- **It is a composition, not a viewport crop.** Nav plus hero at 1440px is 1.77 aspect and the
  frame is 1.60, so at true scale the services section never enters it. The hero's vertical
  dead space is tightened (its 102px top and 95px bottom gaps scaled down together) while
  every element keeps its measured internal proportions — the same call supplymate's price
  lines forced.

---

## Client work

**Facts about client work come from the person who did it. Never infer scope by diffing a
client's live site against a Wayback snapshot.** On 2026-08-08 that inference nearly put a
false claim on the site — that the owner had restructured RAAT's navigation from three menus
to seven. He had not. Caught only because he was asked.

What may be said about RAAT is fixed by what he confirmed: a colour, type and hero-image
refresh, plus one competition-calendar page built with FullCalendar, delivered July 2026 and
still live. Not an IA change. No metrics — none were recorded, and the case study says so
rather than reaching for a substitute number. No claim about how the calendar's fixtures are
loaded; he does not remember, so the page stops at "configured the calendar and loaded the
season's fixtures".

No images of the client's previous design are published. The 2024 Wayback capture cannot be
shown to be the immediate predecessor, and republishing a client's old site is a courtesy that
was never asked for.

---

## What is public and what is not

`_config.yml` controls this. Without it Jekyll renders and serves **every**
`.md` file that does not start with `_` — which for a long time meant
`CLAUDE.md`, `README.md`, `DESIGN.md`, `PRODUCT.md` and all 13 plans and specs
were readable by anyone at `ph-akin.dev/<path>`, with `robots.txt` saying
`Allow: /`. That included the line stating the 13 project pages are simulated
client work, the pricing strategy, and the competitor analysis.

**Do not replace `_config.yml` with `.nojekyll`.** It looks like the same fix
and does the opposite: it switches Jekyll off and serves the repo as-is, which
would newly expose `_docs/` and `assets/_archive/` — `RESUME.md` and the
Fastwork reply templates. Those are 404 today *because* Jekyll skips
underscore-prefixed paths. Jekyll is the guard, not the problem.

Adding a new internal document? Put it under `docs/` (already excluded) or a
`_`-prefixed folder. If it must live at the repo root — as `CLAUDE.md` does,
because Claude Code only reads it there — add it to `_config.yml`'s `exclude`
list and verify with `curl -o /dev/null -w '%{http_code}' https://ph-akin.dev/<file>`,
which must return 404.

Setting `exclude` **replaces** Jekyll's default list rather than extending it,
which is why the defaults are restated in the file.

---

## Typography

**Body:** Inter + Noto Sans Thai on the 56 `portfolio-pages.css` pages, Outfit on the 12
`home-shell.css` pages. **Display** (`h1`/`h2`/`h3`, plus `.section-title` on home-shell and
`.hero-role` / `.hero-role-alt`): Bai Jamjuree, via the `--font-display` token — see "Two
stylesheet families" below for the per-family fallback stack and how the face was chosen.

⚠️ **Both stylesheets once named a body font that most of their own pages never requested**,
and a system fallback covered for it with nothing in the CSS to reveal the gap. `home-shell.css`
named Outfit while only `index` / `index-en` asked for it, so the other ten shell pages —
`about`, `faq`, `process`, `services`, `work`, each ± `-en` — rendered in `-apple-system`.
`portfolio-pages.css` named Noto Sans Thai while **none** of its 56 pages requested it, so
every Thai character on the resume, the showcases, the case studies, the category pages and
the `web-*` pages was drawn by whatever the OS happened to ship — different on macOS, Windows,
Android and iOS. Found 2026-08-10, fixed by appending the missing family to each page's
existing Google Fonts request rather than adding a second `<link>`. **After changing a font
declaration, check that every page loads every family its stylesheet names** — a font a
stylesheet names but no page requests fails with no console warning and no Lighthouse penalty.

**A kicker (`.eyebrow`, `.section-label`) is restyled, not counted.** They lost
`text-transform: uppercase`, `letter-spacing`, weight 700 → 600, and `.eyebrow::before` (a
28px rule drawn in front of the label) — 0.8rem uppercase, tracked, weight 700, with a rule in
front is the kicker every generated landing page shipped in 2023, and that treatment, not the
fact of a label above a heading, was the actual tell. The rule this replaced — keep one kicker
per page, delete the rest — was tested against the copy first and found false: of 25
`.section-label`s on the shell pages only 3 repeat their own heading, and of roughly 244
`.eyebrow`-to-heading pairs on the portfolio pages most complement rather than repeat it
(`เริ่มตรงนี้` above `คุณต้องการเว็บแบบไหน?`, `ขอบเขตงาน` above `ราคานี้ได้อะไร และไม่ได้อะไร`)
— `about` and `process` above already kept theirs for exactly that reason. Only kickers that
measurably repeat their own heading were deleted: 44 instances across 43 files, out of
hundreds that were restyled and kept. **Reading only the delete count invites the wrong
generalisation** — the decision was never "fewer kickers," it was "no scaffolding."

**The four `.story-card`s on the showcase / case-study story stack are four shapes now, not
four copies of one box, and none of the 128 carries a `.story-icon` badge any more** — see
"Edit a showcase page" for which class does what.

---

## Two stylesheet families — never mix them

| Family | Stylesheet | Pages | Section wrapper | Headings |
|---|---|---|---|---|
| Home shell | `assets/home-shell.css` | `index`, `index-en`, `work`, `services`, `about`, `faq`, `process` (+ `-en`) | `<div class="container">` | `.section-label` + `.section-title` |
| Portfolio pages | `assets/portfolio-pages.css` | resume, case studies, showcases, the 3 category pages, the 7 `web-*.html` | `<div class="page-shell">` | `.eyebrow` + `<h2>` |

**A page must load exactly one of them.** They define `.hero`, `.section`, `.nav-links` and
all five `.tag*` classes differently — nine colliding selectors. Loading both breaks the page.

They also disagree on token names for the same values: `--border` / `--border-2` in
home-shell, `--line` / `--line-2` in portfolio-pages (both `#21262d` / `#30363d`). Anything
loaded by both families — `assets/site-search.css` — must ask for one, then the other, then a
literal fallback.

`assets/portfolio-context.css` and the floating "← Back to Portfolio" pill it styled were
**deleted on 2026-08-07**. A demo page is a simulation of a client's site and must not wear
portfolio chrome — the same rule that keeps the site search off those 13 pages. Six of them
(`DRIP`, `PulseBoard`, `appointment-booking`, `coffee-landing`, `gym-landing`, `solar-landing`)
now have no link back at all, and all 66 links into the demos open in the same tab, so the
browser Back button is the only way out. If that becomes a problem the fix is
`target="_blank"` on those links, **not** reinstating the pill.

`home-shell.css` was extracted from `index.html`'s inline `<style>` on 2026-08-06. The two
homepages' stylesheets were byte-identical apart from one `content:` string, now the
`--preview-label` custom property; `index-en.html` keeps a 3-line `<style>` overriding it.

**Headings carry a display token, body type does not.** Both stylesheets define
`--font-display`, set to `"Bai Jamjuree", "Noto Sans Thai", sans-serif` in `portfolio-pages.css`
and `'Bai Jamjuree', 'Outfit', sans-serif` in `home-shell.css`, and `h1`/`h2`/`h3` (plus
`.section-title`, `.hero-role`, `.hero-role-alt` in home-shell) read from it. The body face is
unchanged — `'Outfit'` in home-shell, `"Inter", "Noto Sans Thai", Arial` in portfolio-pages —
because swapping body type across 84 pages risks line-height, Thai vowel collisions and CLS
for little gain, while a display face on headings alone carries most of the distinctiveness.
Bai Jamjuree was chosen 2026-08-10 by rendering Thai and Latin headings at 3.2rem/1.02 against
Anuphan, Chakra Petch, Trirong and Inter and checking that tone marks in `เว็บไซต์` clear the
line above and `ญ` descenders clear the line below — not from a specimen page. All 68 pages
that load either stylesheet append `family=Bai+Jamjuree:wght@600;700` to their existing Google
Fonts request (never a second `<link>`), keeping `display=optional` so CLS stays 0.

### Vertical rhythm

`.section` is `padding: clamp(56px, 9vw, 88px) 0`, so **every section boundary is 176px on
desktop and 112px on mobile** — measured in a browser, not read off the sheet. A section that
sets its own `padding` replaces that clamp outright and silently breaks the rhythm:
`.stack-sec` carried `6px 0 30px` and produced a 94px join, barely half of its neighbours, so
the logo marquee read as crowded against the pricing cards. Fixed 2026-08-07 by deleting the
override, not by tuning it. **A new band on a home-shell page should take `.section`'s padding
and add nothing.**

Two bands legitimately differ, because both carry their own background and so read as separate
surfaces rather than as part of the flow: `.contact-section` (`80px 0`, `#090d13`) and
`.footer-section` (`clamp(48px, 7vw, 72px) 0 …`, `#010409`).

**Every second section is banded**: `main > section:nth-of-type(even)` takes `#10151c` — a
3-step lift off `--bg` — plus hairline `--border` rules top and bottom. `nth-of-type` rather
than a hand-placed class, so the alternation stays correct through any add/remove/reorder and
needs no markup on the 12 pages. `main >` is what keeps it off the two body-level bands above.

The rule **redefines `--bg`** inside the band instead of only setting `background`.
`.section-label` and `.work-search` paint `var(--bg)` on themselves to sit flush with the page;
without the redefinition they would paint `#0d1117` rectangles on top of the band. Those two,
plus `body` and `.hero-eyebrow`, are the sheet's only `var(--bg)` readers — and `.hero-eyebrow`
sits in section 1, which is odd and never banded. **Anything new that paints `var(--bg)` to
blend with the page keeps working; anything that hardcodes `#0d1117` will not.**

Card-to-background contrast drops 1.094 → 1.059 inside a band, which sounds alarming and is
not: `.card` / `.work-card` were never carried by fill contrast at 1.09 either — the `#21262d`
border and `--sh-sm` do that work. Text stays at 5.62:1 minimum, and Lighthouse `color-contrast`
passes on all three sampled pages.

Audited 2026-08-07 when the gaps were questioned as too large. They are not: the 1,392px of
inter-section space is 14.7% of the page, while `#projects` alone is **36.7%**. Trimming the
clamp to 64px would recover 3.7% of page height for a visibly tighter page — measure before
touching it. Every other section is transparent over the page background, which is why the
spacing *reads* emptier than it measures.

**View Transitions are on sitewide** — `@view-transition { navigation: auto }` in both
stylesheets, three lines, so moving between the 84 pages cross-fades instead of flashing
white. Nothing feature-detects it: a browser without support just navigates as it always
did. Off under `prefers-reduced-motion`.

**Three things used to change state with no transition, all for the same reason:**
`display` is not animatable, so a rule that swaps `display` cancels any fade declared
beside it. The work filter was one (below); the other two are the **mobile drawer** and the
**site-search results panel**. Both keep their original mechanism — the drawer keeps
`display: none` so the closed panel stays out of the tab order, the search panel keeps its
`hidden` attribute so it stays out of the accessibility tree — and gain
`transition: display …ms allow-discrete` plus an `@starting-style` rule, which is what
makes a discrete property transitionable. A browser without support gets exactly the
previous snap, so there is nothing to feature-detect. **Do not "simplify" these by
dropping `display: none` or the `hidden` attribute** — those are load-bearing for
accessibility, not leftovers.

**The work filter's transition was dead code until 2026-08-08.** `.work-card` declared
`transition: opacity 250ms, transform 250ms` while the hidden state used `display: none`,
which is not animatable — so the filter snapped from the day it was written. It now uses
two attributes: `data-leaving` fades the card, and `data-hidden` removes it from layout
260ms later. **Do not collapse them back into one.**

**The hero screenshot shows a skeleton while it loads.** The 30 `showcase-*.html`
pages open on a ~115 KB JPEG inside `.browser-frame`; its box was already reserved by the
img's `width`/`height` attributes so CLS was 0, but the reserved box sat empty and flat,
which reads as a stalled page rather than a loading one.

The shimmer paints on the **img's own `background`**, not on an overlay element — an
`<img>` shows its background wherever the bitmap has not painted, so this needs no extra
node, no absolute positioning, and no knowledge of the frame bar's height, and the decoded
image covers it with no swap. It is gated on a `[data-loading]` attribute that `site-ui.js`
sets **only when the image is not already `complete`** (a cached image would otherwise flash
a skeleton it does not need) and removes on `load`, on `error`, and on an 8s timer. With no
JS, a cached image, or a 404 on `site-ui.js` the attribute is never set and the pages behave
exactly as they did before — the skeleton is additive, never a gate on content.

The sweep runs `--surface` → `--line-2`, not `--surface` → `--line`: the first version moved
through three near-identical greys on this dark theme and read as a flat panel. A skeleton
that cannot be seen is not doing the one job it has. Under `prefers-reduced-motion` it keeps
the placeholder tint and drops the sweep.

⚠️ **The `.study-meta` count-up clamps `p` at BOTH ends, and the low clamp is the
load-bearing one.** It shipped as `Math.min(1, (t - t0) / dur)` and rendered **฿-325 on
`web-booking` where the real figure is ฿7,900** — a negative `p` makes `(1 - p)` exceed 1,
cubing it exceeds 1, and `1 - that` goes below zero. `t` can legitimately predate `t0`:
`t0` is `performance.now()` when the observer fires, `t` is the *start* of the frame being
rendered, so an observer firing mid-frame gets a `t` earlier than its own `t0`. It is frame
timing, not a rare edge case, and it lands on the one number these pages exist to state.
A `setTimeout` backstop also restores the true figure, because rAF stops in a background tab
and the final frame used to be the only thing that put the real number back — an interrupted
run left a wrong price on screen until reload. **Any new count-up needs both.**

🔴 **Never hide a `.reveal` element with anything that shrinks its box.** The hero
screenshot's wipe shipped as `clip-path: inset(0 100% 0 0)` on `.browser-frame.reveal` — the
very element the reveal IntersectionObserver watches. Chrome subtracts a target's own
`clip-path` from its intersection rect, so the element had `intersectionRatio: 0`, never
reached the `0.08` threshold, never got `.visible`, and so the clip never opened. **A loop
that locks itself**: the hero image stayed invisible on all 30 showcase pages,
with no console error, no failed request and no Lighthouse penalty. Reported 2026-08-10 as
"preview หาย" on `showcase-elevate-commerce`; the file was there and returned HTTP 200 the
whole time.

The clip now lives on the `> img` inside the frame, so the observed box is never shrunk.
**Hide with `opacity` or `transform` only** — neither affects the intersection rect. Not
`clip-path`, not `visibility: hidden`, not `display: none`, not `width: 0`.

`site-ui.js` also carries a failsafe: 2.5s after load, any `.reveal` still hidden whose box is
in or above the viewport is shown outright. The observer is the nice path, not the only one.
Below-fold elements are left to the observer so the scroll reveal still reads as one.

⚠️ **This class of bug cannot be reproduced in a background tab.** Chrome suspends
IntersectionObserver *and* freezes CSS transitions in a hidden tab, so an automated browser
whose tab never becomes visible reports every reveal as broken and every transition as stuck
at its start value — which looks exactly like the real bug and is not. Verify the end state
by disabling the transition and reading the computed value, not by waiting.

**Behaviour lives in `assets/site-ui.js`, not inline.** `home-shell.css` sets
`.reveal { opacity: 0 }` and only `.reveal.visible` restores it, so any page using `.reveal`
**must** ship the IntersectionObserver — without it every card renders invisible, and
Lighthouse still scores 100 because opacity-0 elements stay in the accessibility tree. That
is exactly how `work.html` once shipped with all 13 cards invisible and a dead hamburger.

Since 2026-08-07 the reveal observer, the mobile drawer and the industry filter live in one
shared file on **12 pages** (`index`, `work`, `about`, `faq`, `process`, `services`, ± `-en`).
Three self-guarding blocks, each returning early when its elements are absent. A new
home-shell page needs one tag and nothing else:

```html
  <script src="assets/site-ui.js" defer></script>
```

Both user-visible string sets — the filter status line and the hamburger's `aria-label` —
are chosen from `document.documentElement.lang`, which is what let the Thai and English
copies merge. Merging them fixed three bugs that had drifted in: `work-en.html` announced
its filter results in Thai, the Thai pages carried an English `aria-label`, and the two
`services` pages had no close-on-outside-click handler at all.

`index.html` / `index-en.html` keep their featured-carousel block inline — it is theirs
alone, and it still must strip `data-industry` from the clones. **The nine demo pages carry
their own, smaller reveal implementations and must not be given `site-ui.js`.**

---

## Global navigation

19 selling pages share the same destinations: `หน้าแรก · ผลงาน · บริการ · เกี่ยวกับผม · FAQ`
plus the site search.

- The 12 home-shell pages carry the full `.navbar` with hamburger and mobile panel.
- The 7 industry pages and the 3 category pages (6 files) keep `portfolio-pages.css`'s
  `.page-shell nav` and get the same links and search — 25 selling pages in total. Two navs, one set of destinations — unifying the CSS was tried and reverted
  because of the `.nav-links` collision above.
- `aria-current="page"` marks the active entry.
- **Three chrome elements are built by `site-ui.js`, not written into any page** — the
  reading-progress bar, the section rail, and the copy-on-click behaviour on `mailto:`
  links. None needs markup, so none of the 84 files had to change and none can drift.
  Each self-guards on something observable rather than on a class someone has to remember:
  the progress bar appears when the page is taller than four viewports, the rail when
  `main > section[id]` with an `h2` numbers five or more. `work.html` has four, so it
  correctly gets no rail. The rail is a real `<nav>` with `aria-current`, collapsed to
  ticks until hovered, and `display: none` below 1280px where it would overlap content.
- **The language switcher is a two-state toggle, not a link.** `.lang-toggle` renders
  `TH | EN` with the current language as a `<span class="lang-on" aria-current="true">` and
  the other as the only anchor. It replaced a lone `EN` (or `TH`) nav link on 56 pages —
  which never said which language you were *in*: on a Thai page the bare word `EN` reads
  equally as "you are in English" and "switch to English". The current side is deliberately
  not a link; there is nowhere for it to go. The anchor carries `hreflang` **and** `lang` so
  a screen reader pronounces `EN`/`TH` in the right voice.
  One identical block ships in **both** stylesheets — they are never loaded together, but
  they name the same colour differently (`--border` vs `--line`), so each value asks for one,
  then the other, then a literal, exactly as `site-search.css` does.
  Home-shell pages carry two copies, navbar and drawer. The drawer needs its own override:
  `.nav-mobile-panel a` sets a 44px block, which stretches the pill to the full 335px panel
  width and restyles its inner link.
  **The 8 `web-*` industry pages have no toggle and must not get one** — they are Thai-only
  by design and have no `-en` twin to point at.
- **`services` · `about` · `faq` · `process` (± `-en`) open with a merged band**, same shape as
  `work`: breadcrumb → `h1.work-title` → one `.work-problem` blurb → straight into that
  section's own content. Merged 2026-08-08; each used to spend a whole `.section` (336–441px)
  on four lines of text. `services` and `faq` also lost a `.section-label` that repeated the
  `h1` — `บริการและราคา` above `บริการรับทำเว็บไซต์ และราคา`, `คำถามที่พบบ่อย` above
  `คำถามก่อนจ้างทำเว็บไซต์`. `about` and `process` keep theirs, which complement rather than
  repeat. All eight gained a breadcrumb and a `BreadcrumbList` JSON-LD, which they had never
  carried while `work`, the 8 `web-*` and the 6 category pages all did.
  **`.work-title + .work-problem` gets `margin-bottom: 2.2rem`** — the blurb otherwise sat
  8–13px off the content below it, because the section boundary that used to separate them
  is gone. This is the counterpart of `.need-start` on `work`.
  ⚠️ **Removing a section's `h2` breaks `heading-order`.** Dropping `#packages`'s h2 on
  `services` left `h1 → h3` straight to the card titles; Lighthouse Accessibility fell to 98.
  The `h2` is back, the redundant `.section-label` above it is not.
- The CTA button is `#contact` on the homepages and `/#contact` everywhere else.
- `process.html` is deliberately **not** a nav item — six links plus a search field plus two
  controls overflow at 1180px.
- The 42 showcase / case-study / resume files keep their **contextual** nav on purpose: its
  links differ per page (`ดูเว็บจริง` points somewhere different on each), which a generic bar
  would destroy.

---

## The work archive (`work.html` / `work-en.html`)

Rebuilt 2026-08-07 after `bigzweb.com/projects`, scoped down: that page carries 115 projects,
this one 13, and most of its machinery exists to make 115 navigable.

Layout: **one opening band — breadcrumb + `h1` + one-line blurb + the six `#need` tiles** →
`#projects`, which now opens with a *visible* `h2` + blurb above `.work-layout` (a `240px`
sidebar beside the results pane) → the passive `.work-tagcloud` → case studies → contact.

Restructured 2026-08-08 against `bigzweb.com/projects`, in two passes:

- **The title band and `#need` merged.** The title was its own `.section` carrying four lines
  of text — 176px of padding for a heading — and its `.section-label` read `ผลงาน`, the same
  word as the breadcrumb's current page and all but the same as the `h1`, so the page opened
  by saying it three times.
- **The `h1` is now the question, not the page name** — `คุณต้องการเว็บแบบไหน?` /
  `What kind of site do you need?`. The `เริ่มตรงนี้` / `Start here` eyebrow went with it.
- **`ผลงานทั้งหมด` / `All work` moved down to `#projects` as a visible `h2`**, together with
  the blurb that used to sit under the old title. It was `sr-only` before, so the page gained
  visible keyword text rather than losing it; `<title>` and the breadcrumb are unchanged.

Three consequences worth knowing:

- **The banding shifted by one.** `main > section:nth-of-type(even)` now lands on `#projects`,
  not `#need`.
- `id="work-heading"` stays on the `h1` and labels the merged section; `#need-heading` is gone.
- `lang="th"` came off `#need` on `work.html`: redundant on a `lang="th"` document, and after
  the merge it would have wrapped the `h1` too.

**The sidebar reuses the nine `<button class="filter-btn">` elements verbatim.** They are not
radios. `assets/site-ui.js` drives the same filter on `index.html`, so changing the control
type would break the homepage; only the flex axis differs, in CSS. `aria-pressed` carries the
state, which is right for a toggle button — adding `role="radio"` without real radio-group
keyboard semantics would be worse.

Four predicates, ANDed in one `applyFilter()`:

| Predicate | Source | Present on |
|---|---|---|
| category | `data-industry` | both pages |
| keyword | `#work-search`, substring over the card's own `textContent` | archive only |
| tag | `.tag-btn[data-tag]` against the card's `data-tags` | archive only |
| featured | `#featured-toggle`, reads `data-featured` | archive only |

**`data-tags` is pipe-separated**, not space-separated — eight of the 24 labels contain a
space (`Fine Dining`, `Full Stack`, `Light UI`, `UI Design`, `Design System`, `Habit Tracker`,
`Gaming UI`, `Landing Page`). All four card files carry it so the cards stay in sync, though
only the archive renders the buttons.

The 24 labels were **not invented**: each project's own showcase page already carried English
tags, and the mapping is those, normalised. Every label owns at least one project, so no tag
can be clicked into an empty grid — assert that when adding a project or a tag. The one
exception needed patching: Iron Republic's page says `Fitness brand` where the list says
`Fitness`.

These pills used to be a passive `.work-tagcloud` under the grid. They moved into the sidebar
when they became interactive — a filter belongs with the other filters, and a non-clickable
list sitting there would read as a filter that does nothing.

**`border` is this site's signal for "this is a control", and `.tag-btn` was the one
exception.** `.filter-btn` beside it has always carried `border: 1px solid rgba(255,255,255,
0.12)`; `.tag-btn` sat at `border: 1px solid transparent`, so a clickable filter pill and
the static `.work-tags` pill on every card below it were **pixel-identical apart from the
cursor — and a phone has no cursor.** Mobile is 51% of traffic and Clarity logged dead
clicks in 7.61% of sessions (14 of 184, measured 2026-08-09). `.tag-btn` now takes the same
visible border as `.filter-btn`; `aria-pressed="true"` still swaps it to `--accent` plus a
ring, which reads more clearly from a neutral border than it ever did from a transparent
one. **Anything new that is a pill and is clickable needs that border**; static `.tag` /
`.tag-list` pills on the showcase pages must stay borderless, which is what makes the
distinction mean something.

The last two are guarded on their elements, so they are inert on `index.html`. `#filter-status`
is `.result-count` (visible) on the archive and `.sr-only` on the homepage — the same string
serves both, and the initial fill is tied to `#work-search` existing so a screen reader is not
made to announce a result count on page load.

The sidebar ships `<details open>` and `site-ui.js` closes it below 900px. That is JS, not a
media query, because `<details>` hides its own children and CSS cannot reliably reopen them.

Deliberately **not** copied from bigzweb: a second tag axis (would mean retagging all 13),
pagination (one page), category chips over the thumbnails (they are detailed SVG mini-UIs and
a chip would cover them), and the `VDO` badge (no project has video).

---

## The `#need` selector

**Six tiles** on `index`, `index-en`, `work` and `work-en` — clinic, booking, restaurant, shop,
gym, construction. Owner's call on 2026-08-08: solar, "ไม่แน่ใจ" and association came out of
the selector.

`.need-grid` is **six columns — one row** above 1100px, so the selector reads as a single row
of choices rather than a 3 × 2 block that looks like content. It steps to three columns below
1100px (six would put every Thai label on three lines) and two below 900px. Each tile carries
a **`.need-icon` badge** — a 34 × 34 tinted rounded square around the 18px inline SVG — and a
`→` drawn by `.need-tile::after`, so a tile reads as a destination rather than a label.
`.need-tile` is `position: relative` purely to anchor that arrow.

**There are eight industry pages, not six.** `web-solar` and `web-organization` are still live,
still in `sitemap.xml`, and reach visitors through `services.html` / `services-en.html` instead.
Anything that removes an industry tile must confirm the page keeps an entry point somewhere, or
it becomes orphaned — reachable only from the sitemap and the site search.

`web-organization` (สมาคม / มูลนิธิ / องค์กร) is the only industry page whose `#related` strip
points at a **case study** rather than a showcase, because the work behind it — RAAT — is real
client work. It shows **one** entry. Per the industry-page rules that is correct and it must not
be padded with loosely-related demos.

---

## Site search

`assets/site-search.js` + `site-search.css` + `search-index.json`, live on **63 pages** —
everything except the 13 demo pages (they are simulated client sites and must not carry
portfolio chrome) and `404.html`.

- **The markup is a placeholder.** Pages ship `<div class="site-search"></div>` and the script
  fills it — 72 copies of the same 11 lines across 61 files collapsed into one place on
  2026-08-07. Placement stays in the HTML because it differs per family: `.nav-inner` on
  home-shell pages, `.page-shell nav` on portfolio-pages ones, plus a second instance inside
  `.nav-mobile-panel`. The two instances namespace their option ids (`ss0-opt-0`) or the
  listboxes collide and `aria-activedescendant` points at the wrong element.
- **The script tag is versioned: `assets/site-search.js?v=self-render`.** Bump it on any
  change that alters the generated markup. A returning visitor pairing the new HTML with a
  cached copy of an older script gets an empty placeholder and **no search field at all** —
  which is exactly what happened during testing. `assets/design-preview.js?v=` (now `v=2`) is a second
  self-rendering script with the identical hazard; the same rule applies to it.
- **`search-index.json` is hand-maintained.** A new page that is not added to *both* the `th`
  and `en` arrays is simply unfindable, and nothing fails to tell you.
- Matching is plain **substring** — Thai has no word spaces, so segmentation would be heavy and
  error-prone. Each entry carries hidden keywords (`k`), which is why `หมอฟัน` finds BRIGHT
  Dental and `ราคา` finds all three packages.
- The index is fetched on **first focus**, not page load, so it never competes with LCP.
- The results panel is `position: absolute` — CLS must stay 0.
- Below 768px the field hides from both navbars; on home-shell pages the full-width copy inside
  the hamburger panel takes over.

---

## `lumi-clinic.html` — the one demo with a written direction

Redesigned 2026-08-11. It is a demo page: its own inline CSS, no shared reset, no portfolio
chrome. Two things about it are decisions, not defaults, and both are easy to undo by accident.

**The surface is deliberately dark.** It used to be `#F6F3EE` on a token literally named
`--paper`. That colour sits inside the warm-neutral band (OKLCH L .84–.97, C < .06, hue
40–100) that reads as the default "premium clinic" surface, and display-serif + rules +
restraint + almost no imagery on top of it is a second saturated lane. Neither is wrong alone.
The palette now runs off a written scene — *a Sukhumvit consult room at six, overhead lights
off, one warm lamp, the doctor saying you don't need filler yet* — which is in a comment above
`:root`. Lights off, one lamp: surface `#0D1511`, the warm `#EEB15B` as accent rather than
substrate. Every value is OKLCH-derived and contrast-checked; the lowest pair on the page is
5.41:1. **`assets/thumbs/lumi-clinic.svg` was recoloured to match** — it is the card on the
homepage, the archive, *and* one of the three cards in the homepage hero deck, so a palette
change here is four places, not one.

⚠️ **No identifiable faces, and no before/after.** Commit `6cf2ad1` removed four hotlinked
Unsplash photos showing a clear face and retired a before/after slider that used the same face
as both its "before" and its "after". The page turns that into a claim — "We don't publish
before/after photos — skin tone, lighting and angle make them easy to fake and hard to verify"
— which is better copy than the widget was. **Do not add faces back and do not add a
comparison widget**, however many med-spa articles list it as essential.

The page carries a mobile-only sticky `.book-bar`. It reserves its height with
`body { padding-bottom }`, **not** with padding on `.booking` — the first version padded the
booking section and the *footer*, the actual last element, still ran 73px underneath the bar.
Padding the body is indifferent to which element happens to be last.

`display=optional`, not `swap`: swap reflowed the `h1`, the nav logo and the hero buttons when
Trirong arrived and measured CLS 0.011–0.015. That was a real finding, not a style preference,
and it has since been worked through the family: **86 of the 88 `.html` files now ask for
`display=optional`.** `sorn-restaurant.html` was the last reachable page still on `swap` and
moved 2026-08-12 — with Playfair Display and Inter dropped from their own stacks, **111 of its
157 visible elements shift, the furthest by 65.2px**, which is the reflow `swap` was letting a
cold visitor watch. (That is total reflow, not a CLS score; CLS weights by viewport fraction.)

The only two files left on `swap` are `DRIP.html` and `spa-retreat.html`, both retired demos —
`noindex`, absent from `sitemap.xml`, and linked from zero files. Leave them or delete them
with the rest of the retired set; there is no visitor to protect.

⚠️ **Measuring this needs a positive control.** Adding a `@font-face` with
`src: local("__none__")` to unload a webfont does **nothing** — Google's own `@font-face` rules
still match, the face stays applied, and the sweep reports **0 elements moved**, which reads
exactly like "no exposure" and is not. Patch each element's computed `font-family`, dropping
only the webfont and keeping the rest of that element's own stack, and confirm the count is
non-zero before believing a zero anywhere else.

---

## Lessons from the 2026-08-07 site-wide audit

Four defects that static greps and the Lighthouse score both missed. Each is a class of bug,
not a one-off:

**`aria-hidden` does not satisfy WCAG 2.5.3.** The VELVÉ card's `.work-thumb` link wraps a
photo with a `4-step booking wizard` badge painted over it. Hiding the badge with
`aria-hidden="true"` removed it from the accessible name but **not** from the rendered text
axe compares against, so `label-content-name-mismatch` kept firing. The fix is the opposite
of hiding: the `aria-label` must *contain* the visible string. A voice-control user saying
"click 4-step booking wizard" has to reach the link.

**That audit has weight 0**, so Accessibility still reported 100 while failing. Read the
per-audit failures, never the category score alone.

**A demo page has no reset, so `width: 100%` plus horizontal padding overflows by exactly
the padding.** `construction-landing.html` shipped `.btn-primary { width: 100% }` in its
≤560px block on top of `padding: 0 21px`, and with no `box-sizing` anywhere in
`construction-redesign.css` the hero CTA — the page's primary call to action — ran 18px past
the right edge of a 375px screen. `canScrollX` stayed `false`, so the overflow sweep never
caught it; the button was simply clipped. Found 2026-08-10. Each demo stylesheet must set its
own `box-sizing`; check with a per-element right-edge sweep, not just `canScrollX`.

**A bare element selector in a demo page will find a second element eventually.**
`aesthetic-booking.html` styled `nav { position: sticky; background: rgba(244,239,230,.92) }`
for its header. When a `nav.foot-links` was later added to the footer it inherited the cream
panel, putting cream 0.68 links on cream 0.92: **1.11:1, effectively invisible**, and it had
been shipping that way. Now `.site-nav`. The 13 demo pages each carry their own inline CSS
with no shared reset — assume every bare tag selector in them is a latent collision.

**An `-en` page carrying Thai copy must mark it.** Package features stay Thai deliberately
(see the bilingual rules), so `lang="th"` on that block is what stops a screen reader reading
Thai in an English voice. `index-en.html` and `services-en.html` already did this; the three
category pages did not. Their `.project-strip` blurbs were also Thai — those were the wrong
source, not a language-marking problem: the English one-liners already existed on
`index-en.html`'s cards, which is what step 6 of the category-page recipe means by "the
project's real one-line description".

**Verified clean and not worth re-checking blind:** 0 dead links and 0 dead anchors across 84
files, no stylesheet-family mixing, sitemap 79 URLs with no duplicates or dead entries, all
JSON-LD parses, all 8 `FAQPage` blocks match their rendered `<h3>` count, every `<img>` has
`alt` and resolves, no duplicate `id`s, and no horizontal overflow at 375px on any of the 84
pages. `ลูกค้าจริง` appears only around RAAT; the three `ผลงานจริง` hits are ordinary Thai for
"actual work" in copy about the *client's* needs, not a claim about this portfolio.

**Left alone, deliberately.** Four retired demos — `DRIP`, `appointment-booking`,
`spa-retreat`, `stock` — are `noindex, follow`, absent from `sitemap.xml`, and linked from
nowhere. `appointment-booking.html` has no heading of any level and is superseded by
`BookEase.html`. Deleting them is the owner's call. Twenty meta descriptions sit at 161–190
characters; only those over 190 were trimmed, because shortening the rest means rewriting his
copy.

---

## How to measure this repo without fooling yourself

Four wrong answers were reported to the owner as fact on 2026-08-11, all from the
same two mistakes. They are cheap to avoid and expensive to miss.

**`class` is a list — never match it with equality.** Every one of these was
written as an exact match and silently under-counted:

| Written | Missed | Reported | Truth |
|---|---|---|---|
| `class="story-icon"` | `class="story-icon amber"`, `… mint` | 64 | **128** |
| `class="browser-frame"` | `class="browser-frame reveal"` | 0 files | **30 files** |

Grep the bare token (`grep -c 'story-icon'`) or match `class="[^"]*token`, then
list the distinct values you actually found:
`grep -ho 'class="story-icon[^"]*"' *.html | sort | uniq -c`.

**A zero is a claim about your instrument until you prove otherwise.**
`BookEase.html` was reported as having a dead sidebar and a dead "New Booking"
button. It has **86 controls, 12 switchable views and a 27 KB script**, and all of
it works. The probe checked `e.onclick`, which is always `null` on this page
because it binds with `addEventListener`; and the selector `^Appointments$` never
matched that nav button, because it contains a `<span class="nav-badge">2</span>`,
so the click never happened. Before reporting an absence, run the same probe
against something that must be non-zero — and treat an *inconsistent* result as
the same warning (two buttons had handlers and seven did not; that asymmetry was
the tell).

⚠️ **Character count does not measure a JS-rendered page.** `BookEase.html` has
2,419 characters of static HTML and renders everything else from its script; by
that metric it looked like one of the thinnest pages on the site when it is one of
the most substantial. Count controls, views and rendered `innerText` instead.

⚠️ **The automated browser here reports unreliable image intrinsics.** The same
JPEG returned `naturalWidth` 1470, 1600 and 1959 across three reads, and a file
that rendered correctly on screen reported `0x0`. Use `sips -g pixelWidth -g
pixelHeight`, `file`, and the server's byte count; those three agree with each
other. Also distinguish `complete && naturalWidth === 0` (broken) from
`!complete` (not loaded yet) — a `loading="lazy"` image below the fold is the
second, and was once reported as the first.

---

## Key Standards to Maintain

- **Lighthouse:** 100 / 100 / 100 (Accessibility / Best Practices / SEO) — run after changes.
  Accepted exception: **Best Practices caps at 77** sitewide because Microsoft Clarity sets
  third-party cookies (`third-party-cookies` and `inspector-issues` audits both fire on this,
  confirmed via a real `npx lighthouse` run on 2026-08-06). This is analytics-vs-score, a
  deliberate trade — don't chase it. Any other Best Practices deduction is a real regression.
  Second accepted exception: **`404.html` caps at SEO 66** — the `is-crawlable` audit fails
  on its `robots: noindex`, which is correct for a 404 page. Lighthouse has no way to know
  it is one. Accessibility on that page must still be 100.
- **Mobile overflow:** `canScrollX: false` at 375 × 812 px on every page
- **Accent colour:** `--accent: #5274f8` (slightly lighter than #4f6ef7 for WCAG AA contrast)
- **Button bg:** `--accent-dark: #3651d4` (white text: 6.4:1 contrast ✅)
- **Fonts:** body text via Google Fonts with `display=optional` (prevents CLS) — `Outfit` on
  home-shell pages, `Inter` + `Noto Sans Thai` on portfolio-pages ones; headings on both
  families use the `--font-display` token (`Bai Jamjuree`) — see "Two stylesheet families"
- **Overflow guard:** `html, body { overflow-x: hidden; }`

---

## Pages & Sections (index.html)

| Section | id | Description |
|---------|----|-------------|
| Nav | — | Logo + links: Services, Reviews, Projects, About, Experience, Case Studies, Contact, Resume |
| Hero | `#top` | **Role leads, name is the byline.** `h1` holds `.hero-role` (`นักพัฒนาเว็บฟรีแลนซ์` in `--ink`) + `.hero-role-alt` (`Freelance Web Developer` in `--accent-text`, own line) + `.hero-name` at ~1/2 the size in `--ink-2`. Buyers search the service, not the person, and the h1 text order follows the visual order. Two real colours, never `background-clip: text` — that computes the colour to transparent and the contrast audit cannot measure it. `.hero-role` maxes at **2.8rem**: the `.hero-left` track is 526px, the English line fills it at 2.9rem and tips to three lines at 3.1rem. No `max-width` on the `h1` — a `ch` limit cut the Thai mid-word. Primary CTA → Fastwork, secondary → pricing. Below the CTAs, `.hero-proof` states price floor, reply time and review count as **one line of running text, never a three-card stat row** — that shape is the SaaS metric template. Every figure is already stated elsewhere (`฿3,900` on the category pages, 24 hours in the FAQ, the three reviews in `#testimonials`), so the hero claims nothing new; **if one of those changes, this line is a second place to edit.** The right half is `.hero-work` — see below |
| Need selector | `#need` | **6 tiles**, one row on desktop → their `web-*.html` page. 3 columns below 1100px, 2 below 900px. Each tile: `.need-icon` badge + inline SVG (`aria-hidden`) + a `::after` arrow. See "The `#need` selector" |
| Tech Stack | — | Dual-row logo marquee (Simple Icons inlined as SVG symbols), opposite scroll directions, pause on hover, reduced-motion static |
| Services | `#services` | 3 priced packages (Landing Page ฿3,900 / Dashboard UI ฿7,900 / Business Website ฿9,900), Thai copy, each links to Fastwork + `#contact` |
| Pricing | `#pricing` | 3-column comparison of the same packages, prices verbatim from the category pages. On `index-en.html` the copy stays Thai, with `lang="th"` on the `.price-meta` and feature lists **only** — not the section, whose heading is English |
| Testimonials | `#testimonials` | 3 real 5-star Fastwork buyer reviews, Thai, links back to the Fastwork profile — no schema.org Review markup (see `docs/superpowers/specs/2026-08-05-service-pivot-design.md`) |
| Selected Work | `#projects` | 13 project cards, industry filter bar (9 buttons), active-filter chip, featured carousel |
| About | `#about` | Bio + photo |
| Experience | `#experience` | Skills, timeline, tools, KMUTT education |
| Case Studies | `#case-studies` | PulseBoard, LaunchLedger, InternTrack, HabitQuest |
| Contact | `#contact` | Form + email |
| Footer | — | Nav links, email, social icons |

### `.hero-work` — the right half of the hero

Three real projects, one per package sold: **BuildNest** (Landing Page), **BookEase**
(Dashboard), **LUMI Clinic** (business site). They are `<a>`s to the showcase pages, reusing
the `assets/thumbs/*.svg` the card grid already ships, so the browser has them cached and the
hero fetches nothing new.

It replaced three `<div>` cards drawn from grey bars — a fake chart, a fake tag, a fake pill,
the whole block `aria-hidden="true"`. That block filled half the first screen and said
nothing, on the one screen where a buyer decides whether to keep reading. **It is no longer
`aria-hidden`**, because it now contains real links.

Three things about it are deliberate:

- **The cards must not overlap.** The first version stacked them for a "deck" feel and the
  overlap landed on the `.hw-meta` strips — the project names, the one thing the block exists
  to say. `.hw-1` ends at ~196px, `.hw-2` sits hard left in the band below it, `.hw-3` starts
  below `.hw-1`'s bottom edge. Measure after any change to `height: 408px` or the card widths.
- **Names are short** (`BuildNest`, not `BuildNest Construction`). `.hw-name` is
  `text-overflow: ellipsis`, so a long name truncates silently rather than wrapping — it
  looked fine in CSS and shipped as `BuildNest Constructi…` in the browser.
- **Below 900px it becomes a three-up row, not `display: none`.** The old decorative block was
  hidden there and that was correct for scenery; real work is not scenery, and mobile is 51%
  of this site's traffic. Below 480px `.hw-kind` drops so the name still fits.

`.hero-eyebrow` was deleted in the same change — it read `รับทำเว็บไซต์เต็มเวลา` directly under
a badge already saying `รับงานใหม่บน Fastwork`, two availability statements stacked, and it was
the last element on the site still carrying the pre-2026-08-10 kicker treatment (uppercase,
`0.1em` tracking, weight 700, a 28px `::before` rule). Its meaning moved into the badge.

---

## URLs carry no `.html`

Every internal link, `canonical`, `hreflang`, `og:url`, JSON-LD `item`, `sitemap.xml` `<loc>`
and `search-index.json` `u` points at an **extensionless** URL — `/showcase-buildnest`, not
`/showcase-buildnest.html`. GitHub Pages resolves `/foo` to `foo.html` on its own; no config,
no redirects, no directory restructure. Verified live before the rewrite.

`index.html` is `/`. `404.html` is the one exception and keeps its extension in its own
`canonical` and `og:url` — GitHub Pages looks the file up by name — though its outgoing links
were rewritten with everything else.

**The `.html` URLs still return 200** — GitHub Pages cannot redirect, and
`jekyll-redirect-from` cannot help because source and target are the same file. `canonical` is
what tells Google which URL counts, so a page whose canonical still ends in `.html` splits its
own ranking signal.

Canonical fixes the index; it does nothing for the address bar. A visitor arriving from an old
bookmark or an already-indexed result sat on the URL we had just told Google to ignore, and
Clarity counted the homepage twice — 32 sessions on `/` beside 19 on `/index.html`. So all 83
pages (every file except `404.html`) carry a **six-line inline redirect in `<head>`**:

```js
(function(p){if(location.protocol!=='file:'&&/\.html$/.test(p)&&!/\/404\.html$/.test(p))
  location.replace((/\/index\.html$/.test(p)?p.slice(0,-10):p.slice(0,-5))+location.search+location.hash)})(location.pathname)
```

Four things about it are deliberate and should survive edits:

- **Inline, in `<head>`.** This repo consolidates duplicated inline scripts on principle — this
  is the exception. A deferred external file runs after the parse, so the page renders and then
  jumps.
- **`location.replace`, not `location.href`.** No history entry, so Back leaves the site instead
  of bouncing off the redirect.
- **`404.html` is excluded.** GitHub Pages serves it under the *missing* path, which does not end
  in `.html` and so never triggers; visiting `/404.html` directly is the only case, and it is
  left alone.
- **It cannot loop.** The result never ends in `.html`, so the guard is false on the second pass.

`/index.html` → `/`, `/index.html#services` → `/#services`, `/work.html#projects` →
`/work#projects`. Query strings and hashes are carried through.

**Never strip `.html` from a link to github.com.** Seven `blob/main/*.html` source links exist
and they point at real files in the repo; the migration matched only relative paths and
`https://ph-akin.dev/…`.

**`assets/analytics.js` classifies clicks by href, and its patterns had `\.html` baked in.**
They now treat the extension as optional. Had they not been updated, `industry_open`,
`package_open`, `showcase_open` and `case_study_open` would all have stopped firing silently —
no error, no console warning, just an empty funnel.

**`python3 -m http.server` no longer serves this site correctly** — it does not resolve
extensionless paths, so every internal link 404s and a Lighthouse run measures a broken page.
Use `python3 _tools/serve.py 8123` instead; it mirrors the GitHub Pages fallback and serves
`404.html` on a miss. `_tools/` is underscore-prefixed so Jekyll skips it.

---

## SEO & Meta

- Theme color: `#5274f8`
- OG image: `assets/social-preview.png` (1200×630)
- Canonical URL set on all pages — `https://ph-akin.dev/...` (custom domain, live since
  2026-08-06; see `docs/superpowers/plans/2026-08-05-technical-seo-fix.md` for the prior
  github.io-subpath era this replaced)
- `robots: index, follow`
- Twitter card: `summary_large_image`
- Sitemap: `sitemap.xml`, referenced from `robots.txt`. Every `<url>` carries
  `<lastmod>` · `<changefreq>` · `<priority>`, in that order after `<loc>`.
  **`<lastmod>` is generated, never hand-edited** — run
  `python3 _tools/sitemap-lastmod.py` after any change to page content. It reads
  `git log -1 --format=%cs` per page and maps the extensionless `<loc>` back to its file.
  Stamping every URL with today's date on each deploy is the pattern Google treats as
  unreliable and then ignores; deriving from git keeps the values honest and lets them
  diverge as pages actually diverge. First run (2026-08-07) legitimately produced one date
  for all 79, because the extensionless-URL rewrite touched every page in a single commit.
- `robots.txt` at the repo root allows all crawlers and points at the sitemap

---

## Contact & Social

| Channel | Value |
|---------|-------|
| Fastwork (primary CTA) | https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&source=byob |
| Email | a0626568471@gmail.com |
| GitHub | https://github.com/Phakinza007 |
| LinkedIn | https://linkedin.com/in/phakin-chawanpunya |
| Instagram | https://www.instagram.com/phakinkinpa/ |

---

## Analytics

Click/scroll heatmaps + session recording via **Microsoft Clarity**, loaded from
`assets/analytics.js` (shared across all pages, same pattern as `portfolio-context.css`).

- Project ID lives at the top of `assets/analytics.js` (`CLARITY_PROJECT_ID` const)
- Every `.html` page must have `<script src="assets/analytics.js" defer></script>` right
  before `</head>` — **use the relative path**, not `/assets/analytics.js`. The site is served
  at the custom domain root `https://ph-akin.dev/` (via the `CNAME` file + DNS at name.com,
  live since 2026-08-06 — see `docs/superpowers/plans/2026-08-05-technical-seo-fix.md` for the
  prior github.io-subpath era). An absolute path would work fine at this root, but keep using
  relative paths anyway — it's the established convention and safe regardless of hosting path.
- **Clarity does not load on localhost / 127.0.0.1 / file:.** Checked 2026-08-08 against the
  real project: six of the ten most-visited URLs were `localhost:8123`, 91 of 157 visits.
  Development traffic was indistinguishable from buyers. The click listeners still run
  locally so `?cl_debug` verifies instrumentation without sending anything.
- **The owner's own visits are the other half of that problem, and the localhost guard
  cannot catch them** — he reads the live site from a phone on mobile data and from a
  laptop, exactly as a buyer would. Measured 2026-08-09: one visitor was 27 of 184
  sessions, **15% of every number on the dashboard**. Visiting any page once with
  **`?cl_off`** sets a `clOptOut` flag in `localStorage` and Clarity never loads in that
  browser again; **`?cl_on`** undoes it. A per-browser flag rather than a Clarity IP block
  because the IP changes with the network and each one would have to be re-entered. The
  `localStorage` calls are wrapped in `try`/`catch` — it throws outright in some privacy
  modes, and an analytics opt-out must never take the page down with it. **This has to be
  done once per browser and per device**, so it is not self-enforcing; if the dashboard
  ever shows a suspiciously heavy single visitor again, that is the first thing to check.
- Click tracking is delegated (one listener, no per-button markup needed) — classifies
  clicks by `href`/class in `assets/analytics.js`. Custom events fired: `cta_fastwork`,
  `fastwork_profile`, `contact_email`, `contact_phone`, `resume_download`, `showcase_open`,
  `case_study_open`, `project_open`, `project_filter`, `tag_filter`, `featured_toggle`,
  `work_search`, `industry_open`, `package_open`, `breadcrumb_nav`, `contact_submit`
- **Most events carry an `origin` tag** from `originOf()` — `need_tile`, `breadcrumb`,
  `project_strip`, `story_links`, `nav`, `footer`, or the enclosing section id. The same
  industry page is reachable from four places; without it they are one number.
- `industry_open` is the load-bearing one. The seven `web-*.html` pages are the entire search
  strategy and went untracked until 2026-08-08, so the funnel
  `home → #need tile → industry page → Fastwork` could only be seen at its last step.
- `work_search` is debounced 1.2s — typing is not a click, and a six-character query should
  be one event, not six.
- `cta_fastwork` / `contact_email` / `resume_download` also call `clarity('upgrade', 'high_intent')`
  so those sessions aren't dropped by sampling
- Debug: open any page with `?cl_debug` in the URL to `console.log` every tracked event
- Any element can opt into a custom event name via `data-track="event_name"`
- New pages: just add the shared `<script>` tag — no other wiring needed

---

## Common Tasks for Claude

### Add a new project card
Use the **portfolio-add-card** skill — it handles the full workflow automatically.

### Run a Lighthouse audit
Real Lighthouse via the CLI — no MCP tool needed (`node`/`npx` are available; confirmed
2026-08-06). Serve the site locally, then run per page/viewport:
```bash
python3 _tools/serve.py 8123 &          # ไม่ใช่ http.server — ดู "URLs carry no .html"
npx -y lighthouse http://localhost:8123/ \
  --quiet --chrome-flags="--headless" \
  --output=json --output-path=/tmp/lh-<page>-mobile.json
# add --preset=desktop for the desktop pass
```
Pull scores from the JSON: `python3 -c "import json; d=json.load(open('/tmp/lh-<page>-mobile.json')); print({k:round(v['score']*100) for k,v in d['categories'].items() if v.get('score') is not None})"`.
Fix any Accessibility/SEO/Performance regression before committing. See the accepted
Best Practices exception above — don't chase that one.

### Check mobile overflow
If a real browser preview is available, navigate to the page, resize to 375×812, then run:
```js
({canScrollX: (function(){document.documentElement.scrollLeft=50;const s=document.documentElement.scrollLeft;document.documentElement.scrollLeft=0;return s>0;})(), bw:document.body.scrollWidth, cw:document.documentElement.clientWidth})
```
If viewport resize isn't available in your environment, embed the page in a 375×812
`<iframe>` on a blank page instead — its own CSS media queries evaluate against the
iframe's viewport, giving the same real breakpoint behavior — then run the same
snippet against `iframe.contentDocument`/`contentWindow`.

### Edit a showcase page
All 30 showcase files share one body layout, added 2026-08-07: a single-column **story
stack** read top to bottom, replacing the old two-column `.study-grid` + separate `#fit`
section + `.result-band`. One `<section class="section" id="overview">` holds:

1. `.story-intro` — one muted line telling the reader how to read the page
2. `.story-stack` with exactly **four** `.story-card`s, each opening with a `.story-head`
   holding an `<h2>` and a `.story-kicker` one-liner — **no `.story-icon` badge**; the badge
   was removed from all four cards 2026-08-10 (see below). The four are, in order: project
   overview (+ `.tag-list`), the 30-second version (`.highlight-list`), who it fits, and the
   ask — the last is `.story-card.accent` and carries a `.story-price` line plus
   `.story-actions` with the Fastwork + email buttons
3. `.story-links` — "live site · all projects →"

**The four cards are four shapes, not four copies.** They shipped identical — same radius,
border, surface and padding, each opened by a 40×40 rounded tinted badge — 128 cards and 128
badges across 32 files reading as one texture, and an icon above every heading was a second
template tell on top of the first. Card 1 (overview) stays a bordered card: it anchors the
page and holds the tag list. Card 2 (`.story-card--flat`, the 30-second version) drops border,
radius and background and reads as a plain ruled list. Card 3 (`.story-card--statement`, who
it fits) is one claim set as one — larger type, indented, a 1px `--accent` rule in place of a
container, not a decorative side-stripe. Card 4 (`.story-card.accent`) is unchanged and stays
the most prominent, because it is the ask.

**`.story-price` is required on all 30 showcase pages and states the *site's* entry price, not the
project's.** Added 2026-08-09 off the first full week of Clarity: `showcase_open` fired in
19 sessions and `cta_fastwork` in 1, and no showcase page named a price anywhere while
`#related` sent the reader to three more demos. The copy is
`ราคาเริ่มต้น ฿3,900 ขึ้นอยู่กับขอบเขตงาน — ดูราคาทั้ง 3 แพ็กเกจ` → `services`
(`-en`: "Pricing starts at ฿3,900, depending on scope" → `services-en`). It must stay a
floor statement: several of these projects are dashboards that start at the ฿7,900 package,
so "งานนี้ ฿3,900" would be false on them. The figure is verbatim from the category pages.

⚠️ Its selector is **`.story-card > p.story-price`**, not `.story-price`. `.story-card > p`
zeroes paragraph margins and out-specifies a lone class, so the first version computed to
`margin-top: 0` and welded the line to the paragraph above it — visible only in the browser,
never in the CSS. `.story-note` carries the same shape for the same reason.

**`case-study-raat.html` is deliberately excluded** even though it uses the same story
stack: it is real client work, and a package price under it would read as what that client
paid.

`#related` stays below as its own section. The card headings are deliberately generic
labels; the project-specific claim belongs in the paragraph, not the heading.

The `.story-*` block lives at the end of `assets/portfolio-pages.css` and uses **only
existing tokens** — no new colours. `.story-card h2` overrides the sheet's global `h2`
clamp, which is far too large inside a stack.

`.eyebrow` is not used inside story cards, and neither is `.study-block`.

### Add a case study

**Two body formats are in use, deliberately.** The four concept case studies
(`pulseboard`, `launchledger`, `interntrack`, `habitquest`) run
`#problem` → `#decisions` → `#practice` → `#result`, where `#decisions` is an
`<ol class="decision-list">` of three numbered `.study-block.decision` cards. That shape is
built to narrate a design exercise.

`case-study-raat.html` uses the **showcase story stack** instead — `.story-intro` +
four `.story-card`s + `.story-links`, identical to the 26 `showcase-*` pages — because a
buyer reading the one piece of real client work wants the same scan as the demos, not an
essay. It keeps `#stack` (three reasons FullCalendar beat a plugin) between the stack and
`#related`: that is the substance of the engagement, and cutting it to match the showcase
outline exactly would leave the real project thinner than the self-directed ones.

Its nav follows the showcase pattern too — `ผลงานทั้งหมด · ดูเว็บจริง · เรซูเม่ · EN`, four
items, **no in-page anchors**. The old nav pointed at `#work` and `#result`; restructuring
the body deleted both ids and left four dead anchors behind. **Changing a section id on
these pages means checking the contextual nav in the same edit.**

The honest "no metrics were recorded" line survives the reformat as `p.story-note` inside
the first card — a `--muted` aside with a left rule, immediately under the claim it
qualifies. It is required content, not decoration; see "Client work".

Case studies ship in bilingual pairs, same as every other page on the site (see
"Bilingual structure" above). Producing only the Thai file makes an unpaired,
uncrawlable page — do all of these:
1. Create `case-study-<name>.html` (Thai, `<html lang="th">`) using `portfolio-pages.css`
2. Create `case-study-<name>-en.html` (English sibling, `<html lang="en">`)
3. Add the `hreflang` trio to **both**: `th` → Thai URL, `en` → `-en` URL,
   `x-default` → Thai URL (Thai is the site default); `canonical` self-referential on each
4. Set `og:locale` per language (`th_TH` / `en_US`)
5. Add `<script src="assets/analytics.js" defer></script>` before `</head>` on both
6. Add a card in `#case-studies` on **both** `index.html` and `index-en.html`
7. Add both URLs to `sitemap.xml`

### Add a service category landing page
Three exist today: `landing-page.html`, `dashboard-ui.html`, `business-website.html`
(each with an `-en` sibling) — one per package in the `#services` section, giving each
its own SEO-indexable, ad-landable URL instead of relying on the homepage section alone.
Same bilingual-pair rule as case studies, built entirely from components already in
`assets/portfolio-pages.css` — **no new CSS needed**:
1. Create `<slug>.html` / `<slug>-en.html` using `portfolio-pages.css`, same hreflang/
   canonical/`og:locale`/analytics-tag rules as case studies above
2. Hero: `.hero.case-hero` + `.eyebrow` + `<h1>` + `.hero-copy` + `.hero-actions` with
   a `.button.primary` Fastwork CTA
3. Pricing/facts strip: `.study-meta` (4-box grid — price, timeline, revisions, best-for)
4. Body: two `.study-block`s inside `.study-grid` — one `.featured` block with a
   `.highlight-list` (copy the package's `<ul class="card-list">` bullets **verbatim**
   from `index.html`'s `#services` section, don't rewrite them), one plain block
   answering "who it's for"
5. Closing CTA: `.result-band` (same Fastwork + email pattern as showcase pages)
6. Real work: `.project-strip` of `.project-link`s pointing at matching showcase pages,
   using each project's real one-line description already on its Selected Work card
7. Link the page from its matching Services card's `.card-cta-row` (a third
   `.card-cta-secondary` link) on **both** `index.html` and `index-en.html`
8. Add both URLs to `sitemap.xml`

Per "Bilingual structure" above, `index-en.html`'s `#services` pricing/feature copy stays
in Thai (never translated) — so the `.highlight-list` on the `-en` category page also
stays in Thai; only the surrounding hero/chrome copy is in English.

### Add an industry landing page
Seven exist: `web-clinic`, `web-booking`, `web-restaurant`, `web-shop`, `web-gym`,
`web-construction`, `web-solar`. They target Thai buyer search intent (`รับทำเว็บคลินิก`) and
are **Thai-only** — see "Bilingual structure" for why. Built entirely from
`assets/portfolio-pages.css`, **no new CSS**:

1. **Copy `web-clinic.html`** and replace the content. Do not hand-build the skeleton — the
   container is `.page-shell` (not `.container`, which is `index.html`'s), the hero has two
   `.page-shell` blocks, `.study-meta` children are bare `<div>`s with `<strong>` before
   `<span>`, `.result-band` has an inner `<div>` plus `.result-actions`, and the page ends
   with `<footer class="footer-band">`. All five are easy to get wrong from memory.
2. Head: no `hreflang`, self canonical, `robots: index, follow`, `og:locale` `th_TH`,
   `<html lang="th">`, analytics tag before `</head>`
3. Nav has **no EN link**
4. `.study-meta` price/timeline/revisions come **verbatim** from the matching package on the
   category pages. Never invent pricing — these are live Fastwork listings
5. `#overview`: a **`.feature-grid` of six `.feature-card`s** — one per feature that industry
   actually needs, each a check badge beside a single line — then a plain `.study-block`
   answering "who it's for". Give that block's `<h2>` different wording from its `.eyebrow` —
   repeating "เหมาะกับใคร" twice reads as a bug.
   Rebuilt 2026-08-08 from `bigzweb.com/recommend/corporate`'s benefit row. The six features
   used to be a bulleted list inside one tall card beside a short paragraph, so the section
   was a 382px column next to a 236px one and the features read as fine print. **The copy is
   the same six lines, moved not rewritten** — three columns, two below 900px, one below 640px
6. `#related`: `.project-strip` using each project's `.work-problem` text from `index.html`
   **verbatim**. A single-demo page shows one link — do not pad it. A `.heading-link`
   ("ดูผลงานทั้งหมด →") sits in the second cell of its `.section-heading`, which was already a
   two-column grid with `align-items: end`, so it needed no new layout
7. `#faq`: **10** `.study-block`s with `<h3>` questions — 4 industry-specific, 2 on price
   objections, 4 shared (domain/host, revisions, payment, dissatisfaction) copied from
   `faq.html`. A matching `FAQPage` JSON-LD ships in the `<head>`; the question count in the
   JSON must equal the rendered `<h3>` count.

**Section order, all 8 pages:**

```
hero → #problem → #preview → #overview → #included → #compare → #process → #related → #faq → #cta
```

`#preview` sits **directly after `#problem`** — owner's call 2026-08-08. State the problem,
then show what the fix looks like, before any of the scope, price or process copy. It used to
sit between `#process` and `#related`.

Two things depend on that position and must survive any reorder:

- `#preview` ships `hidden`, so `design-preview.js` watches its **previous sibling** for the
  IntersectionObserver — an element with no box never triggers one. That sibling is now
  `#problem`. Any section it lands after must be a real, rendered section with height.
- `#related` still follows `#preview` in reading order even though they are no longer
  adjacent: the preview answers "what do I get", the strip answers "can he build it".
  `bigzweb.com/recommend/*` runs proof before preview; the owner asked to invert it.

Since 2026-08-07 each page also carries `#problem`, `#included`, `#compare` and `#process`,
taking the body from ~2,300 to ~6,800 characters — the page-1 result measured against them
carries roughly 2,500–3,000 words. All four are built from existing components and needed no
new CSS.

**One page in the family now carries new CSS: the design preview widget** (below). Everything
else here is still built from existing components, and a new industry page needs none.

`#compare` sets ฿3,900 against the ฿19,900–25,900 bracket the page-1 agencies occupy. It
**names no competitor** and states the freelance side's own limits (one person, no cover, no
out-of-hours support) — a comparison that only flatters one side reads as advertising.

**`#compare` is a three-column grid, not the sheet's default two.** `.study-grid` is two
columns, so the third card used to drop onto a row of its own and leave a 292px hole beside
it — the third option read as an afterthought rather than a peer. Fixed 2026-08-08 with a
rule scoped to `#compare` and `#stack` (RAAT's three FullCalendar reasons); `.study-grid`
itself is untouched and still correct at two columns on the ~50 pages that use it for a pair.
Two things about that rule are load-bearing:

- It is wrapped in `@media (min-width: 861px)`. The 860px rule collapses `.study-grid` to one
  column, and an **id selector out-specifies a class inside a media query** — written as a
  plain override it would have forced three columns onto a phone.
- `align-items: stretch` is set alongside it on `#overview` / `#included` / `#compare` /
  `#stack`. `.study-grid` is `align-items: start` globally, which is what let `#overview`'s
  short right card stop 146px above its neighbour's bottom edge. Cards being read *against*
  each other share a bottom edge; cards that merely sit near each other need not.

Fixing the orphan took `web-booking` from 7,171px to 5,969px tall — 17% shorter with no copy
removed.

**`.section-heading .eyebrow` carries `margin-bottom: 12px`, and it is not decoration.**
`.eyebrow` had no bottom margin and the `h2` beneath it runs at line-height 1.1 — fine for
Latin, but Thai upper vowels and tone marks are drawn above the line box, so `สิ่ง` and `ที่`
collided with the eyebrow. Measured at `gap: 0px` on **every** `.section-heading` sitewide
before the fix. It is a spacing change, not a type-size change, so no heading got smaller.

**All 8 carry `<body class="industry-page">`, and that class is load-bearing.** Added
2026-08-09 when the family was de-boxed: `web-booking` measured 7,215px tall carrying **29
boxed containers** across 10 sections, every one the same recipe (1px `--line` border, `--r`
radius, `--surface` fill), ten of them in `#faq` alone — one repeated surface for the whole
scroll. Inside `.industry-page`, `.study-block`, `.feature-card` and `.study-meta` drop the
border, radius and fill and keep a 1px top rule instead; `.study-meta`'s column dividers
become real 1px `border-left`s because its `gap: 1px` over a `--line` background had nothing
to show once the fill was gone. Result: 29 boxes to 3, page 7,215px to 6,850px.

**The scope is what protects the other 52 pages.** `.study-block` is shared with 17
non-industry files and `.study-meta` with 16 — case studies, showcases and the three category
pages all still want their cards. Verified after the change: `case-study-pulseboard` keeps
7/7 boxed, `landing-page` / `dashboard-ui` / `business-website` 2/2 each, `case-study-raat`
3/3. **Never move these rules out of the `.industry-page` scope**, and a new industry page
must carry the class or it will look like nothing else in the family.

Two containers survive on purpose: `#related`'s `.project-link` carries a thumbnail and is a
real card, and `#cta`'s `.result-band` has to read as a separate surface to close the page.

**These pages must not claim clients.** All thirteen projects are self-directed design work.
The eyebrow above `#related` is `ตัวอย่างงานออกแบบ`, never `ผลงานจริง`, and no page carries a
client count, a client name, or a testimonial beyond the three real Fastwork reviews.

### The design preview widget (`#preview`)

"เว็บของคุณจะหน้าตาแบบนี้" — a tabbed sidebar of the parts of that industry's site, each
swapping a **rendered** mockup (no screenshots) plus a caption. Added 2026-08-08, adapted from
`bigzweb.com/recommend/realestate`. **Live on all 8 `web-*.html` pages**, 57 mockup pages in
total, 6–8 per industry.

- `assets/design-preview.js?v=2` + **one `assets/design-preview-<key>.json` per industry**;
  the page ships only `<div class="design-preview" data-preview="clinic"></div>` inside
  `<section id="preview">`.
- **One file per industry, not one file keyed by industry.** All eight combined are 11.2 KB
  gzipped against 2.6 KB for the largest single one — 8.6 KB per visit that the page never
  uses. Shared caching does not pay it back, because the whole point of these pages is that
  someone searching `รับทำเว็บคลินิก` lands on one and never sees the other seven.
- Nine block types (`nav` `hero` `head` `cards` `list` `form` `gallery` `map` `table`) covered
  all 8 industries with none left over. **A new industry is a new JSON file and nothing else.**
  If one ever needs a tenth block type, that is a code change — call it out as one.
  **The `?v=` is load-bearing** — same hazard as `site-search.js`: new HTML paired with a
  cached older script renders an empty placeholder and no widget. Bump it whenever the
  generated markup changes.
- Styles are a `.dp-*` block appended to `assets/portfolio-pages.css` — no new file, no new
  colours, +1.6 KB gzipped on a sheet 52 pages load. That is the exception noted above.
- **The section ships `hidden` and only `build()` reveals it.** An empty `.section` still
  carries 56–88px of padding top and bottom, so without this a failed fetch leaves a blank band.
- **The IntersectionObserver watches the *preceding* section.** `#preview` is `hidden` and the
  placeholder is empty, so both have zero area before the build — and an element with no box
  never triggers an observer. A 3s `setTimeout` backs it up, because a lazy trigger that fails
  to fire produces no error and no console warning; `work.html` once shipped all 13 cards at
  opacity 0 exactly this way while Lighthouse still scored 100.
- **`role="tabpanel"` wraps the caption; the mockup inside it is `aria-hidden`.** The caption
  is the only readable content, so a panel holding just the mockup would be an empty shell.
  No `aria-live` — a correct tab pattern announces the switch once already. Arrow keys wrap,
  Home/End jump, roving `tabindex` leaves exactly one `0`.
- **Every admin tab carries escalation wording as text**, never the amber dot alone — the
  default is `งานเพิ่มเติม · ประเมินราคาแยก`, and a page may override it with an optional
  `badge` field. No `<form>` in this repo has an `action` and nothing here talks to a backend.
  This is not a new position: `web-clinic`'s own FAQ already says a booking system with a
  calendar and a back office is "งานคนละส่วน เริ่มที่ ฿7,900".
- **`note` states each page's real price, and they differ** — ฿3,900 (clinic, restaurant, gym,
  construction, solar) buys one page, ฿9,900 (shop, organization) buys 3–5 pages, and
  `web-booking` is ฿7,900. Do not copy one industry's `note` to another.
- ⚠️ **`web-booking`'s existing copy already promises more than the stack can deliver** —
  its `#overview` sells "หน้าหลังบ้านดูคิววันนี้", "กันคิวชน" and "ส่งข้อความยืนยันและเตือน",
  all of which need a database. That predates this widget, but the widget makes it concrete,
  which is why that page alone overrides the badge to `ต้องต่อระบบหลังบ้าน · ประเมินราคาแยก`.
  The copy itself is still worth a decision.
- The mockup brand is **`คลินิกของคุณ`**, fictional on purpose and chosen not to collide with
  LUMI / BRIGHT / VELVÉ, which appear in `#related` right below it.
- Tabs emit `data-track="preview_page"` with `data-industry` / `data-page` / `data-side`.
  `analytics.js` already spreads `el.dataset` into the tags, so **that file needed no change**.

- **The tab list is split into two labelled groups, customer and admin** (2026-08-09).
  They used to run together as one list, told apart only by a dot colour and an
  `Admin — ` prefix, so the admin screens read as part of the same ฿-figure — the one
  misreading these pages cannot afford, since every admin screen is quoted separately.
  Each group is a `role="presentation"` wrapper (a `tablist` may only own `tab`s, and a
  presentational wrapper is transparent to AT) and the group heading is `aria-hidden`,
  because the grouping is already in each admin tab's accessible name. Grouping is **by
  run, not by filtering**, so a file that ever interleaves sides still renders in the
  order the JSON asked for; all eight are customer-then-admin today, giving two groups.
  `.dp-group` has to mirror `.dp-tabs`' own axis at each breakpoint — row under 900px,
  column above — because it now sits between the flex container and its items.

Spec: `docs/superpowers/specs/2026-08-08-design-preview-widget-design.md`.
Plan: `docs/superpowers/plans/2026-08-08-design-preview-widget.md`.

**No PDPA content** until it is true — the owner does not currently do anything about it, and
implying otherwise to a clinic is worse than silence
8. Add a tile to `#need` on **both** `index.html` and `index-en.html` — only after the page
   exists, since `main` auto-deploys
9. Add the URL to `sitemap.xml` under the industry-pages comment, priority `0.85`

### Update meta / SEO
Edit the `<head>` block in `index.html` — update `og:description`, `og:image`, `meta-description`
