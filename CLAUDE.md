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
│   ├── thumbs/                   # Legacy .jpg thumbnails (some cards use CSS mini-UI instead)
│   ├── screenshots/              # showcase-*.jpg hero screenshots
│   ├── social-preview.png        # OG image (1200×630)
│   ├── favicon.svg
│   ├── analytics.js              # Microsoft Clarity loader + click tracking (shared)
│   ├── resume-phakin-chawanpunya.pdf
│   ├── portfolio-context.css     # "← Back to Portfolio" floating button (shared)
│   └── portfolio-pages.css       # Shared styles for resume / case study / showcase pages
│
├── case-study-*.html             # 4 case studies — THAI
├── case-study-*-en.html          # 4 case studies — English
├── showcase-*.html               # 13 project showcase pages — THAI
├── showcase-*-en.html            # 13 project showcase pages — English
├── landing-page.html / landing-page-en.html       # Service category page — Landing Page (฿3,900)
├── dashboard-ui.html / dashboard-ui-en.html        # Service category page — Dashboard UI (฿7,900)
├── business-website.html / business-website-en.html # Service category page — Business Website (฿9,900)
└── web-*.html                    # 7 industry landing pages — THAI ONLY, no -en twin
                                  # clinic · booking · restaurant · shop · gym · construction · solar
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

Cards use **CSS-only mini-UI previews** (inline styles inside the `<a class="work-thumb">`),
not screenshot images. This means no `assets/thumbs/` files are needed for new cards.
The `portfolio-add-card` skill handles the full thumbnail creation process.

Tag colour classes:
- `tag-mint` — AI, SaaS, Developer tools, Green-tech, Weather
- `tag-amber` — Finance, Energy, Fine Dining, Warm/luxury brands
- `tag-gray` — Default: Dashboard, Landing Page, Brand, Booking, etc.

---

## Key Standards to Maintain

- **Lighthouse:** 100 / 100 / 100 (Accessibility / Best Practices / SEO) — run after changes.
  Accepted exception: **Best Practices caps at 77** sitewide because Microsoft Clarity sets
  third-party cookies (`third-party-cookies` and `inspector-issues` audits both fire on this,
  confirmed via a real `npx lighthouse` run on 2026-08-06). This is analytics-vs-score, a
  deliberate trade — don't chase it. Any other Best Practices deduction is a real regression.
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

> **Known drift:** the three category pages' `.project-strip` descriptions have fallen out
> of sync with `index.html`'s `.work-problem` text. The 7 industry pages were normalised to
> the `index.html` wording on 2026-08-06; these three still need the same pass.

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
