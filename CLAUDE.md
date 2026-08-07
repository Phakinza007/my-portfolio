# CLAUDE.md — Phakin Chawanpunya Portfolio

## Skills

- **portfolio-add-card** (`.claude/skills/portfolio-add-card/SKILL.md`) — full workflow for adding a new project card. Trigger: any request to "add [page] to the portfolio", "link this page", "create a card for X", or "new project card".

---

## Project Overview

Personal frontend portfolio hosted on GitHub Pages.  
URL: https://ph-akin.dev/

**Owner:** Phakin Chawanpunya  
**Stack:** HTML · CSS · JavaScript (vanilla, no framework)  
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
│   ├── portfolio-context.css     # "← Back to Portfolio" floating button (shared)
│   └── portfolio-pages.css       # resume / case study / showcase / category / web-* pages
│
├── case-study-*.html             # 4 case studies — THAI
├── case-study-*-en.html          # 4 case studies — English
├── showcase-*.html               # 13 project showcase pages — THAI
├── showcase-*-en.html            # 13 project showcase pages — English
├── landing-page.html / landing-page-en.html       # Service category page — Landing Page (฿3,900)
├── dashboard-ui.html / dashboard-ui-en.html        # Service category page — Dashboard UI (฿7,900)
├── business-website.html / business-website-en.html # Service category page — Business Website (฿9,900)
├── web-*.html                    # 7 industry landing pages — THAI ONLY, no -en twin
│                                 # clinic · booking · restaurant · shop · gym · construction · solar
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

19 pairs (38 files): `index`, `resume`, 4 × `case-study-*`, 13 × `showcase-*`.

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
2. The **7 industry landing pages** (`web-clinic`, `web-booking`, `web-restaurant`,
   `web-shop`, `web-gym`, `web-construction`, `web-solar`). The search intent
   (`รับทำเว็บคลินิก`) is Thai-only, so an English twin would double the file count for
   traffic that does not exist. Both languages' `#need` selectors link to the same
   Thai pages.

Both classes carry: **no `hreflang` links at all**, a self-referential `canonical`, and
`robots: index, follow`.

See `docs/superpowers/specs/2026-08-06-th-en-language-toggle-design.md`.

---

## Current Cards in Selected Work (13 total)

The card links to its **showcase page**; the showcase page's "ดูเว็บจริง" link goes to the
**demo file**. The old version of this table conflated the two.

| # | Name | Card → | Live demo | `data-industry` |
|---|------|--------|-----------|-----------------|
| 1 | BuildNest Construction | `showcase-buildnest.html` | `construction-landing.html` | `construction` |
| 2 | Iron Republic | `showcase-iron-republic.html` | `gym-landing.html` | `gym` |
| 3 | NOIR Coffee | `showcase-noir-coffee.html` | `coffee-landing.html` | `restaurant` |
| 4 | Elevate Commerce | `showcase-elevate-commerce.html` | `ElevateCommerce.html` | `shop` |
| 5 | Elasticshop Gaming Top-Up | `showcase-elasticshop-gaming.html` | `elasticshop-gaming.html` | `shop` |
| 6 | RATRI Restaurant | `showcase-ratri-restaurant.html` | `sorn-restaurant.html` | `restaurant` |
| 7 | SolarPeak | `showcase-solarpeak.html` | `solar-landing.html` | `solar` |
| 8 | BookEase Dashboard | `showcase-bookease.html` | `BookEase.html` | `booking` |
| 9 | MuseRoom | `showcase-museroom.html` | `MuseRoom.html` | `other` |
| 10 | LUMI Clinic | `showcase-lumi-clinic.html` | `lumi-clinic.html` | `clinic` |
| 11 | BRIGHT Dental Clinic | `showcase-dental-clinic.html` | `dental-clinic.html` | `clinic` |
| 12 | VELVÉ Aesthetics | `showcase-velve-aesthetics.html` | `aesthetic-booking.html` | `clinic booking` |
| 13 | HabitQuest | `showcase-habitquest.html` | external: `https://habitquest-pi.vercel.app/` | `other` |

**The `#projects` filter runs on `data-industry`, one axis only.** Keys: `clinic`, `booking`,
`restaurant`, `shop`, `gym`, `construction`, `solar`, `other`. `other` is load-bearing —
MuseRoom and HabitQuest match none of the seven industries and would vanish from the filter
without it. Counts are derived from the DOM at runtime, so the static `.filter-count` values
are only a no-JS fallback.

The featured carousel clones `.work-card`s and **must** strip `data-industry` from the clones
(`clone.removeAttribute('data-industry')`). Miss it and five clones leak into every filtered
result — "ทั้งหมด" reports 18 instead of 13.

Visible card tags are **Thai buyer search terms** (`คลินิกทันตกรรม`, `จัดฟัน`, `ขอใบเสนอราคา`),
not style descriptors. `index-en.html` carries English equivalents but the same
`data-industry` keys.

> Culled 2026-07-22 (still in git history): Admin Inventory, Braw & Co, Task Manager,
> Knowledge AI, Weather Dashboard — weakest/template-looking or redundant with BookEase.

---

## Card Thumbnail Approach

**All 13 cards are `<img src="assets/thumbs/*.svg">`.** The inline-styled `<div>` mini-UIs
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

`assets/thumbs/bright-dental.svg` is the one exception: hand-drawn, because that card was a
remote `images.unsplash.com` photo with no `<div>` to measure. Its palette is read off
`dental-clinic.html` (ink `#120F0C`, paper `#F7F2E9`, coral `#FF5B3B`).

**XML comments cannot contain `--`.** A comment mentioning `--ink` makes the whole SVG fail
to parse, and the card renders as a broken-image icon with no console error.

Tag colour classes:

Tag colour classes:
- `tag-mint` — AI, SaaS, Developer tools, Green-tech, Weather
- `tag-amber` — Finance, Energy, Fine Dining, Warm/luxury brands
- `tag-gray` — Default: Dashboard, Landing Page, Brand, Booking, etc.

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

`home-shell.css` was extracted from `index.html`'s inline `<style>` on 2026-08-06. The two
homepages' stylesheets were byte-identical apart from one `content:` string, now the
`--preview-label` custom property; `index-en.html` keeps a 3-line `<style>` overriding it.

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

Layout: breadcrumb → merged hero → the eight `#need` tiles → `.work-layout`, a `240px` sidebar
beside the results pane → the passive `.work-tagcloud` → case studies → contact.

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

## Site search

`assets/site-search.js` + `site-search.css` + `search-index.json`, live on **61 pages** —
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
  which is exactly what happened during testing.
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
- **Fonts:** Inter via Google Fonts with `display=optional` (prevents CLS)
- **Overflow guard:** `html, body { overflow-x: hidden; }`

---

## Pages & Sections (index.html)

| Section | id | Description |
|---------|----|-------------|
| Nav | — | Logo + links: Services, Reviews, Projects, About, Experience, Case Studies, Contact, Resume |
| Hero | `#top` | Name, full-time service positioning, primary CTA → Fastwork (external), secondary CTA → Services/pricing |
| Need selector | `#need` | 8 tiles directly under the hero — 7 industries → their `web-*.html` page, 8th ("ไม่แน่ใจ") → `#contact`. 4×2 desktop, 2×4 mobile. Inline SVG icons, all `aria-hidden` |
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

---

## SEO & Meta

- Theme color: `#5274f8`
- OG image: `assets/social-preview.png` (1200×630)
- Canonical URL set on all pages — `https://ph-akin.dev/...` (custom domain, live since
  2026-08-06; see `docs/superpowers/plans/2026-08-05-technical-seo-fix.md` for the prior
  github.io-subpath era this replaced)
- `robots: index, follow`
- Twitter card: `summary_large_image`
- Sitemap: `sitemap.xml`, referenced from `robots.txt`
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
- Click tracking is delegated (one listener, no per-button markup needed) — classifies
  clicks by `href`/class in `assets/analytics.js`. Custom events fired: `cta_fastwork`,
  `fastwork_profile`, `contact_email`, `resume_download`, `showcase_open`,
  `case_study_open`, `project_open`, `project_filter`, `contact_submit`
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
python3 -m http.server 8123 &
npx -y lighthouse http://localhost:8123/index.html \
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
All 26 showcase files share one body layout, added 2026-08-07: a single-column **story
stack** read top to bottom, replacing the old two-column `.study-grid` + separate `#fit`
section + `.result-band`. One `<section class="section" id="overview">` holds:

1. `.story-intro` — one muted line telling the reader how to read the page
2. `.story-stack` with exactly **four** `.story-card`s, each opening with a `.story-head`:
   a `.story-icon` badge (inline SVG, `stroke="currentColor"`) beside an `<h2>` and a
   `.story-kicker` one-liner. The four are, in order: project overview (+ `.tag-list`),
   the 30-second version (`.highlight-list`), who it fits, and the ask — the last is
   `.story-card.accent` and carries `.story-actions` with the Fastwork + email buttons
3. `.story-links` — "live site · all projects →"

`#related` stays below as its own section. The card headings are deliberately generic
labels; the project-specific claim belongs in the paragraph, not the heading.

The `.story-*` block lives at the end of `assets/portfolio-pages.css` and uses **only
existing tokens** — no new colours. `.story-card h2` overrides the sheet's global `h2`
clamp, which is far too large inside a stack.

`.eyebrow` is not used inside story cards, and neither is `.study-block`.

### Add a case study
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
5. `#overview`: a `.featured` block listing features that industry actually needs, plus a
   plain block answering "who it's for". Give the plain block's `<h2>` different wording from
   its `.eyebrow` — repeating "เหมาะกับใคร" twice reads as a bug
6. `#related`: `.project-strip` using each project's `.work-problem` text from `index.html`
   **verbatim**. A single-demo page shows one link — do not pad it
7. `#faq`: 4–5 `.study-block`s with `<h3>` questions. This is where a page with few demos
   earns its weight
8. Add a tile to `#need` on **both** `index.html` and `index-en.html` — only after the page
   exists, since `main` auto-deploys
9. Add the URL to `sitemap.xml` under the industry-pages comment, priority `0.85`

### Update meta / SEO
Edit the `<head>` block in `index.html` — update `og:description`, `og:image`, `meta-description`
