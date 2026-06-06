# CLAUDE.md — Phakin Chawanpunya Portfolio

## Skills

- **portfolio-add-card** (`.claude/skills/portfolio-add-card/SKILL.md`) — full workflow for adding a new project card. Trigger: any request to "add [page] to the portfolio", "link this page", "create a card for X", or "new project card".

---

## Project Overview

Personal frontend portfolio hosted on GitHub Pages.  
URL: https://phakinza007.github.io/my-portfolio/

**Owner:** Phakin Chawanpunya  
**Stack:** HTML · CSS · JavaScript (vanilla, no framework)  
**Hosting:** GitHub Pages (`main` branch, auto-deploys)

---

## Project Structure

```
my-portfolio/
├── index.html                    # Main portfolio page (16 project cards)
├── resume.html                   # Resume / CV page
├── 404.html                      # Custom dark-theme 404 page
├── sitemap.xml                   # All 29 URLs for Google Search Console
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
└── case-study-interntrack.html
```

---

## Current Cards in Selected Work (16 total)

| # | Name | File | Tags |
|---|------|------|------|
| 1 | Construction Landing | `construction-landing.html` | Brand, Landing |
| 2 | Iron Republic | `gym-landing.html` | Fitness, Brand |
| 3 | NOIR Coffee | `coffee-landing.html` | Dark, Coffee |
| 4 | Admin Inventory | `AdminInventory.html` | Dashboard, Finance |
| 5 | Braw & Co | `BrawAndCo.html` | Brand, Identity |
| 6 | Elevate Commerce | `ElevateCommerce.html` | E-commerce |
| 7 | Task Manager | `task-manager.html` | Dashboard, SaaS |
| 8 | Ltdos Agent Market | `stock.html` | Dashboard |
| 9 | BookEase (Booking) | `appointment-booking.html` | Dashboard, Booking |
| 10 | Elasticshop Gaming | `elasticshop-gaming.html` | Gaming, E-commerce |
| 11 | DRIP Coffee Bar | `DRIP.html` | Café, Brand, Experimental |
| 12 | SORN Restaurant | `sorn-restaurant.html` | Fine Dining, Restaurant |
| 13 | SolarPeak | `solar-landing.html` | Energy, Landing Page |
| 14 | Knowledge AI | `knowledge-ai.html` | AI, Dashboard |
| 15 | Weather Dashboard | `weather-dashboard.html` | Dashboard, Weather |
| 16 | BookEase Dashboard | `BookEase.html` | Dashboard, Booking, Light UI |

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
| Nav | — | Logo + links: Projects, About, Experience, Case Studies, Contact, Resume |
| Hero | `#top` | Name, title, CTA buttons |
| Selected Work | `#projects` | 16 project cards |
| About | `#about` | Bio + photo |
| Experience | `#experience` | Skills, timeline, tools, KMUTT education |
| Case Studies | `#case-studies` | PulseBoard, LaunchLedger, InternTrack |
| Contact | `#contact` | Form + email |
| Footer | — | Nav links, email, social icons |

---

## SEO & Meta

- Theme color: `#5274f8`
- OG image: `assets/social-preview.png` (1200×630)
- Canonical URL set on all pages
- `robots: index, follow`
- Twitter card: `summary_large_image`
- Sitemap: `sitemap.xml` (submit to Google Search Console manually)

---

## Contact & Social

| Channel | Value |
|---------|-------|
| Email | a0626568471@gmail.com |
| GitHub | https://github.com/Phakinza007 |
| LinkedIn | https://linkedin.com |
| Instagram | https://www.instagram.com/phakinkinpa/ |

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
