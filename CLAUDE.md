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
└── showcase-*-en.html            # 13 project showcase pages — English
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
- The **13 project demo pages** (`construction-landing.html`, `gym-landing.html`, …)
  are simulated client work — **not translated, no `-en` twin**. Both languages link
  to the same demo file. Same for GitHub / Fastwork / Vercel links.

See `docs/superpowers/specs/2026-08-06-th-en-language-toggle-design.md`.

---

## Current Cards in Selected Work (13 total)

| # | Name | File | Tags |
|---|------|------|------|
| 1 | Construction Landing | `construction-landing.html` | Brand, Landing |
| 2 | Iron Republic | `gym-landing.html` | Fitness, Brand |
| 3 | NOIR Coffee | `coffee-landing.html` | Dark, Coffee |
| 4 | Elevate Commerce | `ElevateCommerce.html` | E-commerce |
| 5 | Elasticshop Gaming | `elasticshop-gaming.html` | Gaming, E-commerce |
| 6 | RATRI Restaurant | `sorn-restaurant.html` | Fine Dining, Restaurant |
| 7 | SolarPeak | `solar-landing.html` | Energy, Landing Page |
| 8 | BookEase Dashboard | `BookEase.html` | Dashboard, Booking, Light UI |
| 9 | MuseRoom | `MuseRoom.html` | Gallery, Landing Page, Brand |
| 10 | LUMI Clinic | `lumi-clinic.html` | Beauty, Landing Page, Brand |
| 11 | BRIGHT Dental Clinic | `dental-clinic.html` | Healthcare, Landing Page, Booking |
| 12 | VELVÉ Aesthetics | `aesthetic-booking.html` | Beauty, Booking, Interactive |
| 13 | HabitQuest | external: `https://habitquest-pi.vercel.app/` | Gamification, Habit Tracker |

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
| Tech Stack | — | Dual-row logo marquee (Simple Icons inlined as SVG symbols), opposite scroll directions, pause on hover, reduced-motion static |
| Services | `#services` | 3 priced packages (Landing Page ฿3,900 / Dashboard UI ฿7,900 / Business Website ฿9,900), Thai copy, each links to Fastwork + `#contact` |
| Testimonials | `#testimonials` | 3 real 5-star Fastwork buyer reviews, Thai, links back to the Fastwork profile — no schema.org Review markup (see `docs/superpowers/specs/2026-08-05-service-pivot-design.md`) |
| Selected Work | `#projects` | 13 project cards |
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

### Update meta / SEO
Edit the `<head>` block in `index.html` — update `og:description`, `og:image`, `meta-description`
