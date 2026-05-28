# CLAUDE.md — Phakin Chawanpunya Portfolio

## Project Overview

Personal frontend portfolio hosted on GitHub Pages.  
URL: https://phakinza007.github.io/my-portfolio/

**Owner:** Phakin Chawanpunya  
**Stack:** HTML · CSS · JavaScript (vanilla, no framework)  
**Hosting:** GitHub Pages (`gh-pages` branch or `docs/` folder)

---

## Project Structure

```
my-portfolio/
├── index.html              # Main portfolio page
├── resume.html             # Resume / CV page
│
├── assets/
│   ├── thumbs/             # Project thumbnail images (.jpg)
│   │   ├── launch-ledger.jpg
│   │   ├── museroom.jpg
│   │   ├── interntrack.jpg
│   │   ├── pulseboard.jpg
│   │   ├── gym-landing.jpg
│   │   └── noir-coffee.jpg
│   └── social-preview.png  # OG image for social sharing (1200×630)
│
├── LaunchLedger.html       # Project: Startup budget dashboard
├── MuseRoom.html           # Project: Digital gallery landing page
├── InternTrack.html        # Project: Internship tracker UI
├── PulseBoard.html         # Project: Event operations dashboard
├── gym-landing.html        # Project: Iron Republic gym landing page
├── coffee-landing.html     # Project: NOIR Coffee landing page
│
├── case-study-pulseboard.html    # Full case study: PulseBoard
└── case-study-launchledger.html  # Full case study: LaunchLedger
```

---

## Pages & Sections

### `index.html`
| Section | Description |
|---------|-------------|
| Nav | Logo + links: Projects, About, Experience, Contact, Resume |
| Hero | Name, title, CTA buttons (View Projects / Contact Me) |
| Selected Work | 6 project cards with thumbnail, title, tags, link |
| About | Bio paragraph + link to resume |
| Experience | Skills list, timeline, tools used |
| Case Studies | 2 featured case studies (PulseBoard, LaunchLedger) |
| Footer | Nav links, email, social icons (LinkedIn, GitHub, Instagram) |

---

## Projects

| # | Name | Type | File |
|---|------|------|------|
| 1 | LaunchLedger | Dashboard · Finance | `LaunchLedger.html` |
| 2 | MuseRoom | Gallery · Brand | `MuseRoom.html` |
| 3 | InternTrack | Tracker · Product UI | `InternTrack.html` |
| 4 | PulseBoard | Dashboard · UI Design | `PulseBoard.html` |
| 5 | Iron Republic | Fitness · Brand | `gym-landing.html` |
| 6 | NOIR Coffee | Dark · Coffee | `coffee-landing.html` |

---

## Tech Stack

- **HTML5** — semantic markup, accessible structure
- **CSS3** — responsive layout, custom properties
- **JavaScript** — vanilla JS (no framework)
- **Tailwind CSS** — utility classes (referenced in experience section)
- **Figma** — design tool for mockups
- **GitHub Pages** — static hosting

---

## SEO & Meta

- Theme color: `#4f6ef7`
- OG image: `assets/social-preview.png` (1200×630)
- Canonical URL set
- `robots: index, follow`
- Twitter card: `summary_large_image`

---

## Contact & Social

| Channel | Value |
|---------|-------|
| Email | a0626568471@gmail.com |
| GitHub | https://github.com/Phakinza007 |
| LinkedIn | https://linkedin.com |
| Instagram | https://www.instagram.com/phakinkinpa/ |

---

## Development Notes

- All pages are **static HTML** — no build step required
- Edit files directly and push to GitHub; Pages auto-deploys
- Keep `assets/thumbs/` images consistent (same ratio) for the project grid
- When adding a new project: add a card in `index.html` + create the project HTML file + add a thumbnail

---

## Common Tasks for Claude

### Add a new project card
1. Add thumbnail to `assets/thumbs/<name>.jpg`
2. Add `<article>` card block in the **Selected Work** section of `index.html`
3. Create `<name>.html` as the project page

### Update meta / SEO
Edit the `<head>` block in `index.html` — update `og:description`, `og:image`, `meta-description`

### Add a case study
1. Create `case-study-<name>.html`
2. Add a card in the **Case Studies** section of `index.html`
