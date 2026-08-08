# BuildNest redesign — design QA

## Comparison target

- Source visual truth: `/Users/chawanpunya/.codex/generated_images/019fe02b-855c-7820-9c12-7b84da5d9de8/exec-ebc28ed3-1974-44ab-841f-5e2d9698477d.png`
- Implementation capture: `docs/design-qa/buildnest-desktop.png`
- Desktop state: initial page load at the hero.
- Source pixels: 910 × 1728. Implementation pixels: 1280 × 720 at a 1280 × 720 CSS browser viewport; density normalization was not needed for the shared above-the-fold hero comparison.
- Mobile capture: `docs/design-qa/buildnest-mobile.png`, 1280 × 720 outer-browser capture containing a 375 × 812 same-origin iframe. Mobile state: menu open.

## Evidence

The source mock and final desktop capture were opened together for comparison. The same above-the-fold composition is preserved: white navigation, dark construction image, editorial Thai display headline, gold CTA, and a transparent deep-teal proof panel on the right.

The mobile iframe measured `clientWidth: 375`, `scrollWidth: 375`, and `canScrollX: false`. The hamburger interaction was exercised; it exposed all four navigation links in the open state. Desktop navigation and the primary estimate link resolve to their intended anchors; the final contact action opens the existing email channel.

## Required fidelity surfaces

- **Fonts and typography:** Noto Serif Thai is now used for the display hierarchy and Noto Sans Thai for navigation and body copy. Heading weight, scale, and three-line hero wrapping follow the source direction.
- **Spacing and layout rhythm:** The wide desktop hero maintains a generous left copy column and 390px proof panel; the three-step section switches to a single-column sequence on mobile.
- **Colors and visual tokens:** Deep teal, off-white, and restrained construction gold are centralized as `--bn-*` tokens. Text contrast remains high over the photo treatment.
- **Image quality and asset fidelity:** Existing local construction photographs are used at their natural crops. The hero uses an accessible image element with a dark overlay; the secondary photo remains a real local worksite image.
- **Copy and content:** Thai construction copy is concise, conversion-led, and preserves the page’s practice-project disclosure in the footer.

## Findings

- [P2, fixed] Navigation links inherited the browser’s default underline and link color.
  - **Fix:** Added a scoped global link reset in `assets/construction-redesign.css` and re-captured the page.
- [P2, fixed] The first rendered hero used a sans-serif fallback for the Thai display heading.
  - **Fix:** Loaded Noto Serif Thai and used it for display headings and the brand lockup; the final capture confirms the editorial hierarchy.
- [P3] The source uses bespoke line icons inside the proof panel, while the implementation uses numbered construction stages to avoid introducing custom illustrative assets. The hierarchy and panel density remain comparable.

## Implementation checklist

1. Confirm the sticky navigation, anchor links, mobile menu, and mailto CTA after deployment.
2. Keep `assets/construction-redesign.css` as the page-specific visual layer.
3. Use only verified business claims if the practice page is ever converted to a live client site.

## Comparison history

1. Initial desktop capture revealed default link styling; corrected with the link reset.
2. A second comparison revealed the Thai display font fallback; corrected by loading Noto Serif Thai.
3. Final desktop and mobile evidence has no actionable P0/P1/P2 mismatch.

final result: passed
