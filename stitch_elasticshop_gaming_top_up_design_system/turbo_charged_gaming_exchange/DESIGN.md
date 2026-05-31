---
name: Turbo-Charged Gaming Exchange
colors:
  surface: '#f9f9f9'
  surface-dim: '#dadada'
  surface-bright: '#f9f9f9'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f3f3'
  surface-container: '#eeeeee'
  surface-container-high: '#e8e8e8'
  surface-container-highest: '#e2e2e2'
  on-surface: '#1a1c1c'
  on-surface-variant: '#5c403b'
  inverse-surface: '#2f3131'
  inverse-on-surface: '#f1f1f1'
  outline: '#906f6a'
  outline-variant: '#e5beb7'
  surface-tint: '#ba1b0c'
  primary: '#b6180a'
  on-primary: '#ffffff'
  primary-container: '#da3422'
  on-primary-container: '#fffbff'
  inverse-primary: '#ffb4a7'
  secondary: '#715d00'
  on-secondary: '#ffffff'
  secondary-container: '#fed400'
  on-secondary-container: '#6f5c00'
  tertiary: '#5d5c5b'
  on-tertiary: '#ffffff'
  tertiary-container: '#767474'
  on-tertiary-container: '#f7feff'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad4'
  primary-fixed-dim: '#ffb4a7'
  on-primary-fixed: '#400100'
  on-primary-fixed-variant: '#920500'
  secondary-fixed: '#ffe177'
  secondary-fixed-dim: '#ebc300'
  on-secondary-fixed: '#231b00'
  on-secondary-fixed-variant: '#554500'
  tertiary-fixed: '#e5e2e1'
  tertiary-fixed-dim: '#c8c6c5'
  on-tertiary-fixed: '#1c1b1b'
  on-tertiary-fixed-variant: '#474646'
  background: '#f9f9f9'
  on-background: '#1a1c1c'
  surface-variant: '#e2e2e2'
  surface-dark: '#111111'
  surface-light: '#FFFFFF'
  status-success: '#10B981'
  status-pending: '#FFD400'
  status-error: '#F0442F'
  status-cancelled: '#94A3B8'
typography:
  display-lg:
    fontFamily: Prompt
    fontSize: 48px
    fontWeight: '700'
    lineHeight: '1.2'
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Prompt
    fontSize: 32px
    fontWeight: '600'
    lineHeight: '1.3'
  headline-lg-mobile:
    fontFamily: Prompt
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  title-md:
    fontFamily: Prompt
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.4'
  body-lg:
    fontFamily: Prompt
    fontSize: 18px
    fontWeight: '400'
    lineHeight: '1.6'
  body-md:
    fontFamily: Prompt
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Noto Sans Thai
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.4'
  label-sm:
    fontFamily: Noto Sans Thai
    fontSize: 12px
    fontWeight: '600'
    lineHeight: '1.2'
  price-display:
    fontFamily: Prompt
    fontSize: 24px
    fontWeight: '700'
    lineHeight: '1.0'
    letterSpacing: -0.01em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-max: 1280px
  gutter: 1.5rem
  margin-mobile: 1rem
  margin-desktop: 2.5rem
  stack-sm: 0.5rem
  stack-md: 1rem
  stack-lg: 2rem
---

## Brand & Style

The design system is engineered for **Elasticshop**, an automated game top-up platform that prioritizes speed, trust, and the vibrant energy of the gaming community. The brand personality is "The Reliable Pro-Gamer"—fun and approachable, yet technically precise and efficient. 

The aesthetic follows a **Modern Gaming** style: a blend of high-contrast minimalism and functional density. It utilizes deep blacks to create a premium "dark mode" foundation, punctuated by aggressive red CTAs and high-visibility yellow highlights for promotions. The UI emphasizes a card-based architecture with generous rounding to maintain friendliness, while sharp typography ensures data like prices and UIDs are legible at a glance.

The goal is a frictionless "one-tap" psychological feel, where the interface stays out of the way of the user’s mission: getting back into the game.

## Colors

This design system uses a high-impact, promotion-centric palette. 

- **Primary Red (#F0442F):** Reserved exclusively for high-priority actions (Confirm, Buy Now, Top-up). It serves as the "action" anchor of the UI.
- **Secondary Yellow (#FFD400):** Used for attention-grabbing elements such as "HOT" badges, discount percentages, and promotion banners.
- **Main Black (#111111):** Provides the structural weight. Used for headers, footers, and dark-themed card variants to create a professional gaming atmosphere.
- **Neutral Grays & White:** Used for content backgrounds and secondary containers to ensure the interface doesn't feel overly heavy or fatiguing.

**Color Ratio Strategy:**
45% White/Light Gray (Readability), 30% Black (Structure), 15% Yellow (Highlight), 10% Red (Action).

## Typography

The typography system is optimized for bilingual (Thai/English) legibility. **Prompt** is the primary typeface for its modern, geometric feel that resonates with gaming culture. **Noto Sans Thai** is utilized for smaller labels and UI metadata to maintain absolute clarity.

- **Headlines:** Use Bold weights to create a clear hierarchy.
- **Prices:** Should be significantly larger than surrounding body text, using the `price-display` token to ensure the core value proposition is never missed.
- **Functional Labels:** Used for form field headers and status indicators, favoring medium to semi-bold weights to distinguish them from body copy.

## Layout & Spacing

The design system employs a **Fluid Grid** model with fixed maximum constraints for desktop to ensure content doesn't become overly sparse on wide monitors.

- **Grid:** 12-column grid for desktop, 2-column for tablet, and 1-column for mobile.
- **Rhythm:** An 8px base unit drives all spacing.
- **Mobile First:** The top-up flow is designed as a vertical stack for thumb-friendly interaction. On desktop, the layout shifts to a two-column split: the configuration form on the left and a persistent "Order Summary" sticky sidebar on the right.
- **Sectioning:** Large vertical gaps (stack-lg) are used to separate logical steps in the top-up process (e.g., between "Player Info" and "Package Selection").

## Elevation & Depth

This design system uses **Tonal Layers** supplemented by **Low-contrast Outlines** rather than heavy ambient shadows. This keeps the UI feeling fast and "flat-modern."

- **Level 0 (Background):** Light Gray (#F3F3F3) or Deep Black (#111111).
- **Level 1 (Cards/Containers):** Pure White (#FFFFFF) or Surface Dark (#111111). Cards use a subtle 1px border (`#E5E7EB` on light, `#333333` on dark) to define edges.
- **Level 2 (Interactive/Floating):** Subtle, tight shadows (4px blur, 10% opacity) are used only for active states (hover) and floating elements like sticky bottom bars on mobile.
- **Active State:** When a package or payment method is selected, the card receives a 2px Primary Red or Secondary Yellow border to denote focus, removing the need for elevation changes.

## Shapes

The shape language is consistently "Rounded" to balance the aggressive color palette with a friendly, modern feel.

- **Main Containers:** All game cards, package selections, and input fields must use a **16px (1rem)** corner radius.
- **Small Elements:** Chips, badges, and small buttons use **8px (0.5rem)**.
- **Status Badges:** Use a full pill-shape (999px) to distinguish them from interactive buttons.
- **Images:** Game artwork within cards should always inherit the container's 16px radius on the top corners or all corners depending on the layout.

## Components

### Buttons
- **Primary:** Background Red (#F0442F), White text, Bold, 16px rounded.
- **Secondary:** Background Transparent, Red border 2px, Red text.
- **Promotion:** Background Yellow (#FFD400), Black text, used for "Special Offer" triggers.

### Game Cards
- **Structure:** 1:1 or 4:3 Aspect ratio image at the top, Game Logo overlay in the corner (32px size), Game Name in Title-MD, and a full-width "Top Up" button at the bottom.
- **Badges:** Top-left corner placement for "HOT" or "NEW" labels using the Yellow (#FFD400) background.

### Package Selections
- **Layout:** Horizontal list or grid.
- **Details:** Large item icon (left), Item Amount (Top/Bold), Price (Bottom/Red).
- **Selected State:** 2px Red border with a checkmark icon in the top-right corner.

### Payment Status Badges
- **Success:** Green background, White text, Pill-shaped.
- **Pending:** Yellow background, Black text, Pill-shaped.
- **Failed/Cancelled:** Red or Gray background, White text, Pill-shaped.

### Input Fields
- **Style:** 16px rounded, #F3F3F3 background, 1px border.
- **Helper Text:** Small Noto Sans Thai text below the field explaining where to find the UID, using a neutral gray color.

### Progress Indicator
- A "Step" layout at the top of the top-up page (1. Info -> 2. Package -> 3. Payment) using a simple line-and-node system to show user progress.