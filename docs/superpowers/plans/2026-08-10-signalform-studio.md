# Signalform Studio Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create a deployable interactive creative-studio concept built with React and Vite, then surface it as a bilingual portfolio project.

**Architecture:** Source lives under `_studio-src/signalform` so Jekyll never publishes development dependencies. Vite builds the app to the static `signalform-studio/` route on GitHub Pages. The main portfolio receives a bilingual showcase pair, card entries, a matching SVG thumbnail, an actual browser screenshot, and sitemap URLs.

**Tech Stack:** React 19, Vite, a local copy of React Bits `SpotlightCard`, CSS custom properties, Vitest, Testing Library.

## Global Constraints

- `signalform-studio/` is a self-contained demo route, with no hreflang page and no portfolio chrome.
- The demo must respect `prefers-reduced-motion` and remain usable without pointer hover.
- Use one cobalt accent, no canvas or WebGL dependency, and no external analytics from the demo itself.
- Preserve Thai/English parity for portfolio surfaces and use self-referential canonical URLs.
- Build output must be committed because GitHub Pages serves the repository root directly.

---

### Task 1: Establish the React project and its test boundary

**Files:**

- Create: `_studio-src/signalform/package.json`
- Create: `_studio-src/signalform/vite.config.js`
- Create: `_studio-src/signalform/src/test/setup.js`
- Create: `_studio-src/signalform/src/App.test.jsx`

**Interfaces:**

- Consumes: Vite scripts and the `StudioApp` component from `src/App.jsx`.
- Produces: A failing test suite that defines the required headline, services, and contact action.

- [ ] Add React, Vite, Vitest, and Testing Library dependencies and configure Vite to build to `../../signalform-studio`.
- [ ] Write `App.test.jsx` before `App.jsx`, asserting the page renders `Signalform`, the three studio capabilities, and a `Start a project` link.
- [ ] Run `npm test` and record the expected missing-module failure.

### Task 2: Build the interactive studio page

**Files:**

- Create: `_studio-src/signalform/src/main.jsx`
- Create: `_studio-src/signalform/src/App.jsx`
- Create: `_studio-src/signalform/src/styles.css`
- Create: `_studio-src/signalform/src/components/SpotlightCard.jsx`

**Interfaces:**

- Consumes: `SpotlightCard({ children, className, spotlightColor })` and CSS transitions.
- Produces: A responsive app with hero, original visual, capability cards, work-selection state, and a contact CTA.

- [ ] Implement the React Bits `SpotlightCard` as a local component, preserving pointer coordinate custom properties and focus-within support.
- [ ] Implement `StudioApp` with reduced-motion-safe interaction, a keyboard-accessible service selector, and one primary contact action.
- [ ] Write CSS for dark graphite surfaces, cobalt accent, responsive one-column mobile layout, and reduced-motion fallbacks.
- [ ] Run the failing test again after implementation, then run it green and build the route.

### Task 3: Create visual evidence and portfolio surfaces

**Files:**

- Create: `assets/signalform/kinetic-sculpture.png`
- Create: `assets/thumbs/signalform-studio.svg`
- Create: `assets/screenshots/showcase-signalform.jpg`
- Create: `showcase-signalform.html`
- Create: `showcase-signalform-en.html`
- Modify: `index.html`
- Modify: `index-en.html`
- Modify: `sitemap.xml`

**Interfaces:**

- Consumes: the static app at `signalform-studio/`, the app screenshot, and portfolio `work-card` semantics.
- Produces: Thai and English card-to-showcase-to-live-demo paths, crawlable sitemap entries, and a thumbnail whose colours match the live demo.

- [ ] Generate and inspect one original art-directed visual for the app hero; copy it into `assets/signalform/`.
- [ ] Capture the built app in a browser and use that true screenshot in the showcase hero.
- [ ] Write the bilingual showcase pair using the project’s four-card story stack and analytics tag.
- [ ] Add a `data-industry="other"` work card to both homepages, reference the SVG thumbnail, and add both showcase URLs plus the demo route to the sitemap.

### Task 4: Verify the published artefacts locally

**Files:**

- Verify: `_studio-src/signalform/src/App.test.jsx`
- Verify: `signalform-studio/index.html`
- Verify: `showcase-signalform.html`
- Verify: `showcase-signalform-en.html`
- Verify: `index.html`
- Verify: `index-en.html`

**Interfaces:**

- Consumes: the completed static build and portfolio links.
- Produces: build, test, visual, accessibility, SEO, reduced-motion, and mobile-overflow evidence.

- [ ] Run `npm test` and `npm run build` from `_studio-src/signalform`.
- [ ] Serve the repository with clean-URL support and inspect the app at desktop and 375px widths.
- [ ] Verify no horizontal scroll on both portfolio homepages, the two showcase pages, and the demo route.
- [ ] Run Lighthouse on the demo and one portfolio surface, then inspect all changed files and the diff.

## Self-review

- Scope is one independently deployable demo plus the portfolio references needed to discover it.
- The source/output separation preserves Jekyll’s private-document guard and supports static GitHub Pages deployment.
- All public portfolio copy is paired in Thai and English; the demo is intentionally language-neutral and needs no language sibling.
