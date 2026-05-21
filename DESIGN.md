---
name: Portfolio Cover Gallery
description: Static frontend portfolio cover for ten standalone HTML projects.
colors:
  paper: "oklch(96% 0.018 62)"
  paper-soft: "oklch(93% 0.026 48)"
  surface: "oklch(98% 0.012 65)"
  ink: "oklch(22% 0.035 40)"
  muted: "oklch(48% 0.035 52)"
  line: "oklch(80% 0.028 56)"
  cobalt: "oklch(56% 0.19 256)"
  coral: "oklch(68% 0.135 35)"
  mint: "oklch(79% 0.09 165)"
  butter: "oklch(91% 0.09 88)"
typography:
  display:
    fontFamily: "Bai Jamjuree, Noto Sans Thai, Arial, sans-serif"
    fontSize: "5.35rem"
    fontWeight: 700
    lineHeight: 0.95
    letterSpacing: "0"
  headline:
    fontFamily: "Bai Jamjuree, Noto Sans Thai, Arial, sans-serif"
    fontSize: "2.4rem"
    fontWeight: 700
    lineHeight: 1.08
    letterSpacing: "0"
  title:
    fontFamily: "Bai Jamjuree, Noto Sans Thai, Arial, sans-serif"
    fontSize: "1.12rem"
    fontWeight: 700
    lineHeight: 1.25
    letterSpacing: "0"
  body:
    fontFamily: "Noto Sans Thai, Bai Jamjuree, Arial, sans-serif"
    fontSize: "1rem"
    fontWeight: 400
    lineHeight: 1.65
    letterSpacing: "0"
  label:
    fontFamily: "Bai Jamjuree, Noto Sans Thai, Arial, sans-serif"
    fontSize: "0.86rem"
    fontWeight: 700
    lineHeight: 1
    letterSpacing: "0"
rounded:
  md: "8px"
  pill: "99px"
  circle: "50%"
spacing:
  xs: "8px"
  sm: "10px"
  md: "16px"
  lg: "24px"
  xl: "44px"
  section-y: "64px"
  hero-top: "72px"
  page-max: "1180px"
components:
  button-primary:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.surface}"
    rounded: "{rounded.md}"
    padding: "0 18px"
    height: "46px"
  button-secondary:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "0 18px"
    height: "46px"
  project-card:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.ink}"
    rounded: "{rounded.md}"
    padding: "16px"
  contact-band:
    backgroundColor: "{colors.ink}"
    textColor: "{colors.surface}"
    rounded: "{rounded.md}"
    padding: "44px"
---

# Design System: Portfolio Cover Gallery

## Overview

**Creative North Star: "A tidy studio wall for web experiments"**

The portfolio should feel like a clean studio wall where finished practice pieces are pinned up with care. It is warm, direct, and a little tactile: soft paper tones, crisp blue identity marks, real screenshots, and straightforward links that let the work speak.

The design is a brand surface, not an app dashboard. It communicates taste, progress, and organization. It should stay personal and practical instead of becoming a generic startup landing page or a decorative card collage.

Key characteristics:

- Real project screenshots carry the visual weight.
- Thai-first portfolio copy gives the page its personal voice.
- English action labels are acceptable when they match common portfolio conventions.
- Layouts are structured but not sterile, with slight overlap and depth in the hero.
- Every visual element should help visitors choose, open, or understand a project.

## Colors

The palette is warm paper plus a clear cobalt identity accent, with coral, mint, and butter used as supporting notes. The implementation uses OKLCH values directly in CSS so future changes should keep perceptual color behavior intact.

### Primary

- **Portfolio Cobalt** (`oklch(56% 0.19 256)`): Brand mark, ribbon, section accents, primary contact button, and favicon base.
- **Portfolio Ink** (`oklch(22% 0.035 40)`): Primary text, dark buttons, and high-contrast surfaces.

### Secondary

- **Warm Coral** (`oklch(68% 0.135 35)`): Eyebrow rules, focus ring tint, and warm emphasis.
- **Soft Mint** (`oklch(79% 0.09 165)`): Background atmosphere and preview contrast, especially around dashboard work.
- **Butter Highlight** (`oklch(91% 0.09 88)`): Small highlight moments such as favicon contrast and warm detail.

### Neutral

- **Paper** (`oklch(96% 0.018 62)`): Main page background.
- **Soft Paper** (`oklch(93% 0.026 48)`): Secondary panels and tag backgrounds.
- **Surface** (`oklch(98% 0.012 65)`): Cards, buttons, screenshot frames, and light panels.
- **Muted Text** (`oklch(48% 0.035 52)`): Supporting copy and metadata.
- **Warm Line** (`oklch(80% 0.028 56)`): Borders, dividers, card outlines, and toolbar separation.

Named rules:

**The real-screenshot rule.** Never replace project previews with colored placeholders when a screenshot exists.

**The warm-neutral rule.** Avoid pure black and pure white. Neutral colors should stay lightly tinted toward the current paper and ink palette.

## Typography

**Display Font:** Bai Jamjuree, with Noto Sans Thai and Arial fallbacks  
**Body Font:** Noto Sans Thai, with Bai Jamjuree and Arial fallbacks  
**Label Font:** Bai Jamjuree

The pairing is practical and friendly: Bai Jamjuree gives headings a compact portfolio identity, while Noto Sans Thai keeps Thai and English body copy readable.

### Hierarchy

- **Display** (700, `5.35rem`, tight line-height): Used for the hero headline. It should feel like the cover title, not ordinary section copy.
- **Headline** (700, `2.4rem`, compact line-height): Used for section headers and large callouts.
- **Title** (700, around `1.12rem`): Used for project names, card titles, and navigation identity.
- **Body** (400-600, around `1rem`, `1.65` line-height): Used for project explanations, README-like copy, and contact text. Keep paragraphs concise and around 65-75 characters where possible.
- **Label** (700, `0.78rem` to `0.92rem`): Used for tags, section kickers, metadata, and compact action labels.

Named rules:

**No viewport-scaled body copy.** Body text should stay readable and stable across breakpoints.

**Hero scale belongs to heroes.** Do not use hero-sized typography inside compact cards, nav, or tool panels.

## Elevation

Elevation is soft and ambient, designed to make screenshots feel like physical work samples laid on paper. The main shadow vocabulary is `0 26px 70px oklch(24% 0.04 42 / 0.16)`, with smaller cobalt and card shadows for marks, buttons, and hover states.

Use lift to clarify clickability, not to decorate every surface. Cards and previews may rise on hover; page sections should remain mostly unframed. The 404 page uses the same soft elevation to feel related without copying the full home layout.

Motion should use `cubic-bezier(0.16, 1, 0.3, 1)` and short 180-260ms transitions. Transform and opacity are preferred. Avoid animating layout properties.

## Components

**Sticky Topbar:** A warm translucent bar with a cobalt abstract stacked-work mark, compact navigation, and visible border. It should stay calm and utility-focused. The mark should stay symbolic rather than using initials or letterforms.

**Hero Preview Cluster:** The signature brand moment. Use real thumbnails layered around a large preview disc. The cluster should imply that every preview opens a real project.

**Buttons:** Primary buttons use dark ink or cobalt with high contrast. Secondary buttons use a light surface, warm border, and the same 8px radius. Buttons should have clear hover lift and visible focus outlines.

**Hero Actions:** The hero should offer a fast scan path: all projects, newest project, featured case study, and contact. Keep labels direct, and point the featured case study to the strongest reviewer-ready project.

**Project Cards:** Each card pairs a screenshot with title, short description, tags, and split actions for `View live` and `Source file`. Cards use 8px radius, warm borders, light surfaces, and subtle hover lift.

**Status Badges:** Small screenshot badges clarify the role of each project, such as `Case study`, `Brand page`, `Experiment`, or `New build`. Keep them compact, high-contrast, and tied to real project status rather than decorative labels.

**About / Skills Band:** A concise reviewer-facing band that explains the portfolio owner, live project count, case-study count, and practiced skills. It should support scanning without reading like a resume wall.

**Case Study Panels:** Wider reviewer-facing panels that pair a real screenshot with the challenge, three numbered decisions, practiced skill tags, and the same split `View live` / `Source file` actions. Use them for the strongest projects when the thinking behind the UI matters.

**Stack Links:** Compact project links in the featured section. They must include a mini screenshot, project name, source filename, and a clear open affordance.

**Project Context Rail:** Every standalone project page should include a compact fixed context panel with `Back to Portfolio`, a short project type label, one-sentence intent, practiced-skill tags, and small Instagram/email contact actions. It prevents visitors from getting stranded after opening a project from the portfolio.

**Contact Band:** A dark ink band that closes the page with identity and contact actions. Keep Instagram and email visually prominent, then support them with GitHub and repository links.

**404 Panel:** A single focused fallback panel with a large `404` block, Thai explanation, and two actions back to the portfolio and repository. It should feel like the same portfolio system, not a browser default error.

## Do's and Don'ts

Do:

- Use real screenshots from `assets/screenshots/` or thumbnails from `assets/thumbs/`.
- Keep each project action split into `View live` and `Source file`.
- Keep status badges truthful and useful for reviewers.
- Preserve Thai-first page copy where it gives the portfolio personality.
- Keep cards, panels, buttons, and preview frames at 8px radius unless the existing system requires another token.
- Use OKLCH colors when editing CSS so the warm neutral system stays consistent.
- Keep focus states visible and touch targets comfortable.

Don't:

- Do not add placeholder preview blocks when a real screenshot can be generated.
- Do not nest cards inside cards or turn every section into a floating card.
- Do not use pure `#000` or `#fff` in new UI work.
- Do not add decorative gradient text, side-stripe card borders, or glassmorphism as a default style.
- Do not make the portfolio feel like a generic SaaS landing page.
- Do not hide source links or make screenshots decorative without click behavior.
