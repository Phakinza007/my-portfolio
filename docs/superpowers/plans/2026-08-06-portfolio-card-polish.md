# Portfolio Card & Search Polish Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add four small, self-contained UI enhancements to the homepage — a hover preview on project thumbnails, a "styles we've done" tag cloud, a rotating example placeholder on the contact form, and a swipeable "featured work" strip — inspired by a competitor site (bigzweb.com) review, scoped down to fit this static, single-stack portfolio.

**Architecture:** All four features live entirely inside `index.html` and `index-en.html` — no new files, no build step, matching every existing convention in this codebase. Three are CSS-only or CSS+small-JS additions to existing sections (Selected Work, Contact); one (the carousel) clones existing `.work-card` DOM nodes at runtime into a new horizontally-scrolling strip, so the 13 project cards' markup is never duplicated by hand.

**Tech Stack:** Vanilla HTML/CSS/JS (no framework), inline `<style>`/`<script>` inside `index.html`/`index-en.html`, matching the rest of the site.

## Global Constraints

- Every change lands in **both** `index.html` (Thai, default) and `index-en.html` (English) — the site has no shared stylesheet/script for these pages; each carries its own inline `<style>`/`<script>` block that must be edited in parallel.
- Reuse existing CSS custom properties and classes (`--accent`, `--ease`, `--r-sm`, `.tag`/`.tag-*`, `.social-btn`) — do not invent new color values or duplicate an existing pattern under a new name.
- The site already has a global reduced-motion override (`@media (prefers-reduced-motion: reduce) { *, *::before, *::after { transition-duration: 0.01ms !important } }`) — new CSS transitions do **not** need their own reduced-motion rule; this one already covers them.
- `html, body { overflow-x: hidden; }` is a sitewide guard against accidental page-level horizontal scroll (see `CLAUDE.md`). The carousel's internal `overflow-x: auto` on its own track element is the sanctioned exception — verify with the mobile-overflow check that only the track scrolls, never `documentElement`/`body`.
- All inline script blocks are wrapped in a single top-level IIFE per file (`(() => { ... })();`) — new JS goes inside that existing IIFE, never as a new global `<script>` tag or `window.*` assignment.
- After each task, run a Lighthouse pass per `CLAUDE.md`'s "Run a Lighthouse audit" recipe (`npx lighthouse` against a local `python3 -m http.server`) — Accessibility and SEO must stay at 100.

---

### Task 1: Hover-reveal preview overlay on project thumbnails

**Files:**
- Modify: `index.html:536` (CSS, inside the `.work-thumb`/`.work-card` rule block)
- Modify: `index-en.html` (same rule, English copy)

**Interfaces:**
- Consumes: existing `.work-card`, `.work-thumb` classes (no HTML changes — this is CSS-only, using `::after` on `.work-thumb`, which is already `position: relative; overflow: clip;`).
- Produces: nothing consumed by later tasks.

- [x] **Step 1: Add the overlay rule to `index.html`**

Find this exact line (the last rule in the thumbnail-hover block):
```css
    .work-card:hover .work-thumb img { transform: scale(1.05); }
```
Replace it with:
```css
    .work-card:hover .work-thumb img { transform: scale(1.05); }

    .work-thumb::after {
      content: 'ดูตัวอย่าง →';
      position: absolute;
      inset: 0;
      display: flex;
      align-items: center;
      justify-content: center;
      background: rgba(13,17,23,0.72);
      color: #fff;
      font: 700 0.9rem/1 'Outfit', sans-serif;
      opacity: 0;
      transition: opacity 220ms var(--ease);
      pointer-events: none;
    }

    .work-card:hover .work-thumb::after,
    .work-card:focus-within .work-thumb::after { opacity: 1; }
```

- [x] **Step 2: Add the same rule to `index-en.html`**

Find the same anchor line in `index-en.html` and apply the identical CSS, except the `content` text reads `'View Preview →'` instead of `'ดูตัวอย่าง →'`.

- [x] **Step 3: Verify locally**

Serve the site (`python3 -m http.server 8123` from the repo root) and open `index.html` in a browser. Hover any of the 13 project cards — a dark scrim with centered white "ดูตัวอย่าง →" text should fade in over the thumbnail (both the `<img>`-based cards like BuildNest and the CSS-mockup cards like Iron Republic, since the overlay is on `.work-thumb` itself, not the image). Tab to a card with the keyboard — the same overlay should appear on focus (`:focus-within`). Confirm the overlay never appears in the resting/unfocused state (this is what keeps it invisible to Lighthouse's contrast audit, which only evaluates the DOM's default render state).

- [x] **Step 4: Commit**

```bash
git add index.html index-en.html
git commit -m "feat: add hover-reveal preview overlay on project thumbnails"
```

---

### Task 2: "Styles we've done" tag cloud below Selected Work

**Files:**
- Modify: `index.html` (CSS near `:702`, HTML near `:2527`)
- Modify: `index-en.html` (same, English copy)

**Interfaces:**
- Consumes: the existing `.tag`/`.tag-mint`/`.tag-amber`/`.tag-gray`/`.tag-rose`/`.tag-accent` classes already defined for per-card tags (`index.html:562-577`) — do not redefine colors.
- Produces: nothing consumed by later tasks.

This reuses the **real** tag values already printed on the 13 project cards (verified via `grep` across the Selected Work section) — not a fabricated tech-stack list. The site is single-stack (HTML/CSS/vanilla JS everywhere), so a literal "technologies used" cloud would just repeat "HTML CSS JS" 13 times; the actual project **tags** (Construction, Fitness, Coffee, Dashboard, Beauty, …) are the genuinely interesting, truthful summary of the work's breadth.

- [x] **Step 1: Add the tag-cloud CSS to `index.html`**

Find this exact block:
```css
    .works-empty[hidden] { display: none; }
```
Insert immediately after it:
```css

    .work-tagcloud {
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-top: 32px;
      padding-top: 32px;
      border-top: 1px solid var(--border);
    }

    .work-tagcloud-label {
      width: 100%;
      font-size: 0.8rem;
      font-weight: 600;
      color: var(--muted);
      margin-bottom: 4px;
    }
```

- [x] **Step 2: Add the HTML to `index.html`**

Find this exact block (the empty-state paragraph, then the two closing tags that end `.works-grid` and the `<div class="container">` wrapper, right before the section closes):
```html
          <p class="works-empty" id="works-empty" hidden>ยังไม่มีผลงานในหมวดนี้</p>

        </div>
      </div>
    </section>
```
Replace it with (the new block goes **between** the two `</div>` closes — after `.works-grid` ends, still inside `.container`):
```html
          <p class="works-empty" id="works-empty" hidden>ยังไม่มีผลงานในหมวดนี้</p>

        </div>

        <div class="work-tagcloud" aria-label="สไตล์และหมวดงานที่เคยทำ">
          <span class="work-tagcloud-label">สไตล์และหมวดงานที่เคยทำ</span>
          <span class="tag tag-mint">Construction</span>
          <span class="tag tag-amber">Fitness</span>
          <span class="tag tag-gray">Coffee</span>
          <span class="tag tag-accent">E-commerce</span>
          <span class="tag tag-gray">Booking</span>
          <span class="tag tag-amber">Fine Dining</span>
          <span class="tag tag-gray">Restaurant</span>
          <span class="tag tag-amber">Energy</span>
          <span class="tag tag-mint">Full Stack</span>
          <span class="tag tag-gray">Dashboard</span>
          <span class="tag tag-gray">Gallery</span>
          <span class="tag tag-amber">Beauty</span>
          <span class="tag tag-mint">Healthcare</span>
          <span class="tag tag-gray">Interactive</span>
          <span class="tag tag-rose">Dark</span>
          <span class="tag tag-gray">Light UI</span>
          <span class="tag tag-mint">UI Design</span>
          <span class="tag tag-gray">Design System</span>
          <span class="tag tag-accent">Figma</span>
          <span class="tag tag-amber">Gamification</span>
          <span class="tag tag-gray">Habit Tracker</span>
          <span class="tag tag-amber">Gaming UI</span>
          <span class="tag tag-gray">Brand</span>
          <span class="tag tag-gray">Thai</span>
        </div>

      </div>
    </section>
```

Note: the tag-cloud `<div>` sits **inside** `.container` but **outside** `.works-grid` — it's a sibling of `.works-grid`, not a child, so it must NOT pick up grid-item sizing. The trailing `</div>` (closes `.container`) and `</section>` at the end of the replacement are the same two closing tags from the "Find" block, unchanged — only the new `.work-tagcloud` block and an extra blank line are inserted between `.works-grid`'s closing `</div>` and `.container`'s closing `</div>`.

- [x] **Step 3: Mirror into `index-en.html`**

Same CSS (identical, no translation needed — it's layout, not copy). Same HTML structure, but:
- `aria-label="Styles and categories I've worked on"`
- Label span text: `Styles and categories I've worked on`
- Tag text stays in English as already used on the EN cards (e.g. "Fine Dining", "Light UI" are already English on both files — confirm each tag's EN wording matches what's printed on the EN cards by spot-checking 2-3 cards in `index-en.html` before typing the list, since a couple of TH-only labels like "Thai" may read differently in English context).

- [x] **Step 4: Verify locally**

Reload `index.html`/`index-en.html`, scroll to the bottom of Selected Work (after the last card, before the About section). Confirm the tag cloud renders as a wrapped, comma-less row of pills matching the existing card-tag visual style, with adequate spacing from the grid above and the About section below. Check at 375×812 (per `CLAUDE.md`'s mobile-overflow recipe) that the wrapped pills never force horizontal scroll.

- [x] **Step 5: Commit**

```bash
git add index.html index-en.html
git commit -m "feat: add styles/categories tag cloud below Selected Work"
```

---

### Task 3: Rotating example placeholder on the contact form's project-type field

**Files:**
- Modify: `index.html:2700` (HTML, add an `id`), `index.html` inline `<script>` block (JS)
- Modify: `index-en.html` (same)

**Interfaces:**
- Consumes: the existing contact form (`#contact-form`), specifically the `subject` input already asking "what kind of project" (`placeholder="ประเภทโปรเจกต์ (Landing page, Dashboard ฯลฯ)"`).
- Produces: nothing consumed by later tasks.

bigzweb's version cycles placeholder text in a nav search bar that feeds their AI chat — this site has no nav search bar or AI backend, so the closest genuine equivalent is the contact form's existing "what type of project" field: guide the visitor with rotating real examples instead of one static hint.

- [x] **Step 1: Give the input a stable `id` in `index.html`**

Find:
```html
        <input type="text"  name="subject" placeholder="ประเภทโปรเจกต์ (Landing page, Dashboard ฯลฯ)" />
```
Replace with:
```html
        <input type="text"  name="subject" id="project-type-input" placeholder="ประเภทโปรเจกต์ (Landing page, Dashboard ฯลฯ)" />
```

- [x] **Step 2: Add the typewriter effect to the inline `<script>` IIFE in `index.html`**

Find this exact block (the end of the mobile-nav handling, right before the contact-form submit handler):
```js
      /* ---- Contact form async submit ---- */
      const contactForm = document.getElementById('contact-form');
```
Insert immediately before it:
```js
      /* ---- Rotating example placeholder on the project-type field ---- */
      const typeInput = document.getElementById('project-type-input');
      if (typeInput) {
        const examples = [
          'เช่น เว็บร้านอาหาร',
          'เช่น แลนดิ้งเพจธุรกิจ',
          'เช่น แดชบอร์ดจัดการระบบ',
          'เช่น เว็บจองคิว',
          'เช่น ร้านค้าออนไลน์'
        ];
        const staticPlaceholder = typeInput.placeholder;
        const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

        if (!reduceMotion) {
          let exampleIndex = 0;
          let charIndex = 0;
          let deleting = false;
          let timerId = null;

          const tick = () => {
            const current = examples[exampleIndex];
            if (!deleting) {
              charIndex++;
              typeInput.placeholder = current.slice(0, charIndex);
              if (charIndex === current.length) {
                deleting = true;
                timerId = setTimeout(tick, 1800);
                return;
              }
            } else {
              charIndex--;
              typeInput.placeholder = current.slice(0, charIndex);
              if (charIndex === 0) {
                deleting = false;
                exampleIndex = (exampleIndex + 1) % examples.length;
              }
            }
            timerId = setTimeout(tick, deleting ? 35 : 55);
          };

          const stop = () => { clearTimeout(timerId); typeInput.placeholder = staticPlaceholder; };
          const resume = () => { if (document.activeElement !== typeInput && !typeInput.value) tick(); };

          typeInput.addEventListener('focus', stop);
          typeInput.addEventListener('blur', () => { if (!typeInput.value) resume(); });

          tick();
        }
      }

```

- [x] **Step 3: Mirror into `index-en.html`**

Same `id="project-type-input"` addition on the equivalent `subject` input. Same JS block, with the `examples` array translated:
```js
        const examples = [
          'e.g. Restaurant website',
          'e.g. Business landing page',
          'e.g. Admin dashboard',
          'e.g. Booking system',
          'e.g. Online store'
        ];
```

- [x] **Step 4: Verify locally**

Reload the page, scroll to the Contact section, and watch the "ประเภทโปรเจกต์" field without clicking it — the placeholder should type out one example, pause, delete, and move to the next, looping through all 5. Click into the field — the animation must stop immediately and the placeholder must revert to the original static text (so it never fights actual typing). Click away while the field is still empty — the animation should resume. Type something and click away — the animation must stay stopped (checked via `!typeInput.value`). Test with the OS "reduce motion" setting on (or `prefers-reduced-motion: reduce` forced in DevTools) — the field should just show the static placeholder with no animation at all.

- [x] **Step 5: Commit**

```bash
git add index.html index-en.html
git commit -m "feat: rotate example project types in contact form placeholder"
```

---

### Task 4: Featured-work carousel above the filter bar

**Files:**
- Modify: `index.html` (CSS before `:627`, HTML at `:1697` and 5 `data-featured` attributes, JS in the inline `<script>` IIFE)
- Modify: `index-en.html` (same structure, English copy, same 5 projects by their `-en` hrefs)

**Interfaces:**
- Consumes: the 13 existing `.work-card` articles in `.works-grid` — clones 5 of them at runtime rather than duplicating their markup by hand.
- Produces: nothing consumed by later tasks.

**Which 5 projects are featured, and why:** BuildNest Construction, Elevate Commerce, RATRI Restaurant, BookEase Dashboard, VELVÉ Aesthetics — chosen to span the widest range of categories in one glance (construction, e-commerce, fine dining, dashboard/booking, and the most interactive booking-flow project), rather than just the first 5 cards in DOM order. This is an editorial pick — reassigning `data-featured` to different cards later is a one-line change per card, not a structural change.

- [x] **Step 1: Add the carousel CSS to `index.html`**

Find this exact block:
```css
    .filter-bar {
```
Insert immediately before it:
```css
    .featured-strip { margin-bottom: 28px; }

    .featured-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      margin-bottom: 14px;
    }

    .featured-head h3 {
      font: 700 1.05rem/1.3 'Outfit', sans-serif;
      color: var(--fg);
    }

    .featured-nav { display: flex; gap: 8px; }

    .carousel-nav {
      width: 40px;
      height: 40px;
      border-radius: var(--r-sm);
      border: 1.5px solid var(--border);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      color: var(--muted);
      background: var(--surface);
      cursor: pointer;
      transition: color 150ms, border-color 150ms, transform 160ms, background 150ms;
    }

    .carousel-nav:hover {
      color: var(--fg);
      border-color: var(--border-2);
      background: var(--surface-2);
    }

    .carousel-nav:disabled {
      opacity: 0.4;
      cursor: default;
    }

    .carousel-nav:disabled:hover {
      color: var(--muted);
      border-color: var(--border);
      background: var(--surface);
    }

    .carousel-nav svg { width: 18px; height: 18px; }

    .featured-track {
      display: flex;
      gap: 16px;
      overflow-x: auto;
      scroll-snap-type: x mandatory;
      scrollbar-width: none;
      padding-bottom: 4px;
    }

    .featured-track::-webkit-scrollbar { display: none; }

    .featured-track .work-card {
      scroll-snap-align: start;
      min-width: 280px;
      max-width: 280px;
      flex-shrink: 0;
    }

```

- [x] **Step 2: Add the carousel HTML to `index.html`**

Find:
```html
        <h2 class="section-title" id="projects-heading">ผลงานคัดสรร</h2>
```
Insert immediately after it (before the existing `<div class="filter-bar" ...>`):
```html

        <div class="featured-strip">
          <div class="featured-head">
            <h3>ผลงานเด่น</h3>
            <div class="featured-nav">
              <button type="button" class="carousel-nav" id="featuredPrev" aria-label="ผลงานเด่นก่อนหน้า">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="15 18 9 12 15 6"/></svg>
              </button>
              <button type="button" class="carousel-nav" id="featuredNext" aria-label="ผลงานเด่นถัดไป">
                <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><polyline points="9 18 15 12 9 6"/></svg>
              </button>
            </div>
          </div>
          <div class="featured-track" id="featuredTrack"></div>
        </div>
```

- [x] **Step 3: Mark the 5 featured cards in `index.html`**

Each of these five `old_string` blocks is unique in the file (matched via each card's unique `showcase-*.html` href) — find and replace each independently:

```html
          <article class="work-card reveal" data-tags="landing">
            <a class="work-thumb" href="showcase-buildnest.html" aria-label="เปิดหน้าผลงาน BuildNest">
```
→
```html
          <article class="work-card reveal" data-tags="landing" data-featured="1">
            <a class="work-thumb" href="showcase-buildnest.html" aria-label="เปิดหน้าผลงาน BuildNest">
```

```html
          <article class="work-card reveal" data-tags="fullstack ecommerce">
            <a class="work-thumb" href="showcase-elevate-commerce.html" aria-label="เปิดหน้าผลงาน Elevate Commerce">
```
→
```html
          <article class="work-card reveal" data-tags="fullstack ecommerce" data-featured="1">
            <a class="work-thumb" href="showcase-elevate-commerce.html" aria-label="เปิดหน้าผลงาน Elevate Commerce">
```

```html
          <article class="work-card reveal" data-tags="fullstack landing">
            <a class="work-thumb" href="showcase-ratri-restaurant.html" aria-label="เปิดหน้าผลงาน RATRI Restaurant">
```
→
```html
          <article class="work-card reveal" data-tags="fullstack landing" data-featured="1">
            <a class="work-thumb" href="showcase-ratri-restaurant.html" aria-label="เปิดหน้าผลงาน RATRI Restaurant">
```

```html
          <article class="work-card reveal" data-tags="fullstack dashboard">
            <a class="work-thumb" href="showcase-bookease.html" aria-label="เปิดหน้าผลงาน BookEase Dashboard">
```
→
```html
          <article class="work-card reveal" data-tags="fullstack dashboard" data-featured="1">
            <a class="work-thumb" href="showcase-bookease.html" aria-label="เปิดหน้าผลงาน BookEase Dashboard">
```

```html
          <article class="work-card reveal" data-tags="landing app">
            <a class="work-thumb" href="showcase-velve-aesthetics.html" aria-label="เปิดหน้าผลงาน VELVÉ Aesthetics">
```
→
```html
          <article class="work-card reveal" data-tags="landing app" data-featured="1">
            <a class="work-thumb" href="showcase-velve-aesthetics.html" aria-label="เปิดหน้าผลงาน VELVÉ Aesthetics">
```

If any `aria-label` text above doesn't match exactly what's in the file (wording may have drifted), re-anchor on the `href` value alone plus enough surrounding lines to be unique — every `showcase-*.html` href in this section is unique by construction.

- [x] **Step 4: Add the carousel JS to `index.html`**

Find this exact block (the start of the reveal-animation IIFE body):
```js
    (() => {
      /* ---- Scroll reveal with stagger ---- */
```
Insert immediately after `(() => {` and before the reveal comment:
```js

      /* ---- Featured-work carousel ---- */
      const featuredTrack = document.getElementById('featuredTrack');
      if (featuredTrack) {
        const featuredSource = document.querySelectorAll('.work-card[data-featured]');
        featuredSource.forEach(card => {
          const clone = card.cloneNode(true);
          clone.classList.remove('reveal');
          clone.removeAttribute('data-featured');
          featuredTrack.appendChild(clone);
        });

        const prevBtn = document.getElementById('featuredPrev');
        const nextBtn = document.getElementById('featuredNext');
        const scrollAmount = () => (featuredTrack.querySelector('.work-card')?.offsetWidth || 280) + 16;

        const updateNavState = () => {
          const max = featuredTrack.scrollWidth - featuredTrack.clientWidth;
          prevBtn.disabled = featuredTrack.scrollLeft <= 4;
          nextBtn.disabled = featuredTrack.scrollLeft >= max - 4;
        };

        prevBtn?.addEventListener('click', () => {
          featuredTrack.scrollBy({ left: -scrollAmount(), behavior: 'smooth' });
        });
        nextBtn?.addEventListener('click', () => {
          featuredTrack.scrollBy({ left: scrollAmount(), behavior: 'smooth' });
        });
        featuredTrack.addEventListener('scroll', updateNavState);
        window.addEventListener('resize', updateNavState);
        updateNavState();
      }

```

- [x] **Step 5: Mirror everything into `index-en.html`**

Same CSS verbatim. Same HTML structure, English copy:
- Heading: `Featured Work`
- `aria-label="Previous featured project"` / `aria-label="Next featured project"`

Same 5 `data-featured="1"` marks, but anchored on the `-en` hrefs and English `aria-label`s (e.g. `href="showcase-buildnest-en.html"`, `aria-label="Open BuildNest showcase page"` — verify each exact `aria-label` string in `index-en.html` before writing the `old_string`, since EN aria-label wording may differ from a literal translation).

Same JS block verbatim (no translated strings inside it — the IDs and logic are language-independent).

- [x] **Step 6: Verify locally**

Reload `index.html`. Confirm a horizontal strip of 5 cards appears above the filter bar, each showing the same thumbnail/name/tags/buttons as its counterpart in the full grid below. Click the right-arrow button — the strip should smooth-scroll by one card width; the left arrow should become enabled. Scroll to the end — the right arrow should disable. Click a card's "ดูผลงาน" link — it must navigate to the correct showcase page (proving the clone kept its real `href`). Resize to 375×812 and drag/swipe the strip — it should scroll horizontally within its own box only; use the mobile-overflow snippet from `CLAUDE.md` to confirm `document.documentElement`/`body` report `canScrollX: false` (only `#featuredTrack` itself scrolls). Repeat on `index-en.html`.

- [x] **Step 7: Commit**

```bash
git add index.html index-en.html
git commit -m "feat: add featured-work carousel above the project filter bar"
```

---

## Final Verification (all 4 tasks)

- Run `npx lighthouse` (mobile + desktop, per `CLAUDE.md`'s updated recipe) against `index.html` and `index-en.html`. Accessibility and SEO must both be 100 — the hover overlay, tag cloud, and carousel are all new visible content, so re-check color contrast and touch-target size specifically (the two carousel nav buttons are 40×40px, already above the 24×24px WCAG minimum).
- Confirm Best Practices stays at the documented, accepted 77 (Clarity cookies) — any different number means something in this plan introduced a real regression, not the known exception.
- Full click-through: hover a card (overlay appears), scroll to the tag cloud (renders, wraps correctly), watch the contact form placeholder cycle and stop-on-focus, use the featured carousel's arrows and swipe on mobile.
- `git log --oneline -4` should show the four commits from this plan sitting on top of whatever `main` was before starting — nothing pushed until requested.
