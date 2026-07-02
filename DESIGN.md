# Design

## Visual Theme

Two layers coexist by design:

1. **Shell (index.html, resume, case studies, 404):** dark, GitHub-inspired developer aesthetic. Near-black surfaces, blue accent, Outfit display type. Signals technical credibility to hiring visitors.
2. **Project pages:** each commits to its own independent visual identity as a demo of range. Do not force these back onto the shell palette.

## Color

### Shell (index.html)
```
--bg:           #0d1117
--surface:      #161b22
--surface-2:    #1c2128
--ink:          #e6edf3
--ink-2:        #c9d1d9
--muted:        #8b949e
--border:       #21262d
--accent:       #5274f8
--accent-dark:  #3651d4
```

### LUMI Clinic (rose/gold luxury beauty)
```
--cream: #FAF7F2   --rose: #D4A5A5   --gold: #C9A96E   --dark: #2C2422
```

### BRIGHT Dental Clinic (teal medical trust)
```
--teal: #0E8F8B   --teal-dark: #0A6B68   --teal-deep: #084E4C
--mint: #F4FBFA   --navy: #12333B   --amber: #F5B841 (accent only)
```

### SERENE Wellness Retreat (earthy luxury spa)
```
--sand: #F2EDE3   --sage: #8A9B84   --sage-deep: #5F7059
--forest: #3A4A38 (dark section bg)   --terra: #C07856   --ink: #2E2A24
```

### VELVÉ Aesthetics (violet modern clinical)
```
--violet: #7A5AF8   --violet-dark: #5F41D9   --plum: #2B2145 (dark section bg)
--blush: #F9A8D4 (gradient partner)   --ink: #241E38
```

Rule: body text is always the page's own `ink`/`navy`/`forest`/`plum` tone at ≥4.5:1 against its surface — never a generic mid-gray.

## Typography

- Shell: **Outfit** (400–800) for display, system sans for body.
- LUMI Clinic: Playfair Display (serif display) + Noto Sans Thai (body).
- BRIGHT Dental: Sora (display) + Noto Sans Thai (body).
- SERENE Retreat: Cormorant Garamond (serif, italic accents) + Noto Sans Thai (body).
- VELVÉ Aesthetics: Manrope (display, geometric) + Noto Sans Thai (body).

Each clinic/wellness page pairs a distinct serif or geometric-sans display face with the same Thai body font, so the four pages never look like reskins of one template.

## Components

- **Project card** (`index.html` `.work-card`): CSS mini-UI thumbnail (inline-styled `<div>` echoing the target page's nav/hero) + name + one-sentence problem statement + up to 3 tags + View Project / GitHub buttons.
- **Booking form**: label-above-input, 2-col grid on desktop collapsing to 1-col ≤620px, focus ring via `box-shadow` in the page's accent color at ~15% alpha.
- **Price table row**: flex row, name+small-subtext left, bold accent-colored price right, hover tint.
- **4-step wizard** (VELVÉ only): dot-stepper header on a dark `--plum` bar, one panel visible at a time via `.wiz-panel.on`, back/next footer, confirm step renders a booking-code success state.

## Layout

- Shared container width ~1100-1160px depending on page.
- Section vertical rhythm: 84-96px padding per section on desktop, collapsing to 64-68px ≤620px.
- Responsive breakpoints used across pages: 960px (nav collapses, grids go 2-col), 620px (grids go 1-col, forms stack).

## Motion

- `IntersectionObserver`-driven `.reveal` → `.reveal.in` fade-up (24-26px translate, 0.7-0.8s `cubic-bezier(.4,0,.2,1)`), respecting `prefers-reduced-motion: reduce` (motion disabled, content shown instantly).
- Hover lifts: `translateY(-2px to -8px)` + shadow bloom on cards/buttons, `.15-.35s` ease.

## Imagery

Currently CSS-only (no raster images) across the shell and all clinic/wellness pages — mini-UI previews on the index, and CSS-drawn hero visuals (tooth shape, arch composition, wizard mockup) on the project pages themselves. This is a deliberate choice for zero image weight and instant load, but it means these three pages currently show no *people* — a gap for clinic/wellness pages where trust often comes from seeing a real space or practitioner.
