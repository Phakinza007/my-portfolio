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
├── index.html                    # Main portfolio page (13 project cards)
├── resume.html                   # Resume / CV page
├── 404.html                      # Custom dark-theme 404 page
├── sitemap.xml                   # All 21 URLs for Google Search Console
│
├── assets/
│   ├── thumbs/                   # Legacy .jpg thumbnails (some cards use CSS mini-UI instead)
│   ├── social-preview.png        # OG image (1200×630)
│   ├── favicon.svg
│   ├── resume-phakin-chawanpunya.pdf
│   ├── portfolio-context.css     # "← Back to Portfolio" floating button (shared)
│   └── portfolio-pages.css       # Shared styles for resume.html and case study pages
│
├── case-study-pulseboard.html
├── case-study-launchledger.html
├── case-study-interntrack.html
└── case-study-habitquest.html
```

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

- **Lighthouse:** 100 / 100 / 100 (Accessibility / Best Practices / SEO) — run after changes
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
Use the chrome-devtools MCP: `lighthouse_audit(device="mobile", mode="navigation")` on `http://localhost:60270/index.html`. Fix any failures before committing.

### Check mobile overflow
Navigate to the page in preview (port 60270), resize to 375×812, then run:
```js
({canScrollX: (function(){document.documentElement.scrollLeft=50;const s=document.documentElement.scrollLeft;document.documentElement.scrollLeft=0;return s>0;})(), bw:document.body.scrollWidth, cw:document.documentElement.clientWidth})
```

### Add a case study
1. Create `case-study-<name>.html` (use `portfolio-pages.css`)
2. Add a card in the `#case-studies` section of `index.html`

### Update meta / SEO
Edit the `<head>` block in `index.html` — update `og:description`, `og:image`, `meta-description`
