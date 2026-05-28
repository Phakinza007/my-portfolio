# Agent Guide

This repository is a static frontend portfolio for Phakin Chawanpunya. It turns standalone HTML practice files into a polished, reviewable portfolio with live pages, source links, screenshots, resume material, and case studies.

## Project Role

- Primary surface: `index.html`
- Register: brand / portfolio
- Main audience: hiring reviewers, teachers, classmates, collaborators, and the portfolio owner
- Brand personality: warm, practical, polished, learning-forward
- Design north star: "A tidy studio wall for web experiments"

Read these files before major edits:

- `PRODUCT.md` for strategy, audience, tone, and principles
- `DESIGN.md` for visual system, components, color, typography, and design rules
- `README.md` for project list and public URLs
- `RESUME.md` for profile, skills, tools, and contact context

## Current Public Pages

- `index.html`: portfolio cover, project grid, about/resume, case studies, contact, system notes
- `resume.html`: public web resume
- `assets/resume-phakin-chawanpunya.pdf`: downloadable resume PDF
- `case-study-interntrack.html`: full InternTrack case study
- `case-study-launchledger.html`: full LaunchLedger case study
- `case-study-pulseboard.html`: full PulseBoard case study
- `404.html`: GitHub Pages fallback

Standalone project pages:

- `LaunchLedger.html`
- `MuseRoom.html`
- `InternTrack.html`
- `PulseBoard.html`
- `intern_landing_page_html_css.html`
- `gym-landing.html`
- `Brew & Co..html`
- `coffee-landing.html`
- `DRIP.html`
- `coffee_shop_landing_page.html`

## Design Rules

Do:

- Use real screenshots from `assets/screenshots/` or thumbnails from `assets/thumbs/`.
- Keep project actions split between `View live`, `Source file`, and `Case study` when available.
- Preserve Thai-first portfolio copy where it adds personality.
- Keep buttons, cards, panels, and preview frames at `8px` radius.
- Use OKLCH colors for new CSS when possible.
- Maintain visible focus states, readable contrast, and touch-friendly targets.
- Keep new sections reviewer-focused: what to open, why it matters, and what skill it demonstrates.

Do not:

- Do not replace screenshots with placeholder blocks.
- Do not hide source links.
- Do not add nested cards.
- Do not use pure black or pure white in new portfolio UI.
- Do not add decorative gradient text, glassmorphism, or generic AI-looking landing page patterns.
- Do not turn the portfolio into a fake commercial product. The learning context is part of the value.

## Common Workflow

Run locally from the repo root:

```bash
python -m http.server 4173 --bind 127.0.0.1
```

Open:

```text
http://127.0.0.1:4173/index.html
```

Recommended checks after UI changes:

- Load `index.html` on desktop and mobile widths.
- Confirm no horizontal overflow.
- Confirm all modified links open.
- Confirm images are not broken.
- Run `git diff --check`.
- Refresh screenshots if the homepage or project visuals changed.

## Screenshot And Preview Assets

Primary preview assets:

- `assets/screenshots/cover.png`
- `assets/social-preview.png`
- `assets/thumbs/portfolio-cover.jpg`
- Project screenshots in `assets/screenshots/`
- Project card thumbnails in `assets/thumbs/`

When the homepage design changes, refresh:

- `assets/screenshots/cover.png`
- `assets/social-preview.png`
- `assets/thumbs/portfolio-cover.jpg`
- `assets/resume-phakin-chawanpunya.pdf` if `resume.html` uses the changed cover image

## GitHub Pages

Live site:

```text
https://phakinza007.github.io/my-portfolio/
```

Deployment:

- Branch: `main`
- Source: repository root
- Pages can take a short moment to rebuild after push.
- Use cache-busting query strings when verifying live changes, for example `?v=<commit>`.

## Contact And Identity

Owner:

- Name: Phakin Chawanpunya
- GitHub: `https://github.com/Phakinza007`
- Instagram: `https://www.instagram.com/phakinkinpa/`
- Email: `a0626568471@gmail.com`

Keep these contact links consistent across:

- `index.html`
- `resume.html`
- `RESUME.md`

Standalone project pages should keep their floating portfolio context minimal: only the `Back to Portfolio` link belongs there.

## Best Next Improvements

High-value future work:

- Add a full DevLaunch Academy case study for landing page IA and Thai copy.
- Add `Case study` actions directly inside the main project grid for every project that has one.
- Add a small "Best review path" section near the hero: resume, case study, live pages.
- Keep README, PRODUCT, DESIGN, and this file in sync when the public site changes.
