---
name: portfolio-add-card
description: >
  Add a new project card to Phakin's portfolio (my-portfolio). Handles the full
  loop: inspect the target HTML page for its visual identity, build a matching
  CSS mini-UI thumbnail, write the card HTML, insert it into index.html, update
  sitemap.xml, and verify no mobile overflow at 375 px.

  Use this skill whenever the user says anything like "add [page] to the
  portfolio", "link this page", "create a card for X", "new project card", or
  "add [filename].html". Trigger even if the user only names the file — don't
  wait for a detailed request.
---

# portfolio-add-card

Add a new project page as a card in the Selected Work grid of `index.html`.
The card must match the visual identity of the target page and keep the grid
responsive and overflow-free.

---

## 1 · Inspect the target page

Use the running preview server (port 60270, server ID in `.claude/launch.json`)
to inspect the target page. Navigate there and read its identity:

```js
// Run via preview_eval
(function(){
  const root = getComputedStyle(document.documentElement);
  const body = getComputedStyle(document.body);
  // Try all common accent variable names
  const accent = ['--accent','--primary','--sun','--gold','--lime','--green',
    '--blue','--orange','--purple','--teal']
    .map(v => root.getPropertyValue(v).trim()).find(Boolean) || 'none';
  return {
    title:  document.title,
    bg:     body.backgroundColor,
    accent,
    h1:     document.querySelector('h1,h2,.hero-big,.headline')
              ?.textContent?.trim().slice(0,60),
    theme:  body.backgroundColor.includes('248,250,252') ||
            body.backgroundColor.includes('255,255,255') ? 'light' : 'dark'
  };
})()
```

Note: **bg**, **accent** (hex preferred), **theme** (light vs dark), and the
first headline. You'll use these to drive the thumbnail.

---

## 2 · Build the CSS mini-UI thumbnail

The thumbnail is a `<div>` inside the `<a class="work-thumb">` anchor. It uses
only inline styles — no external images needed. The goal is a recognisable
visual echo of the real page, not a pixel-perfect screenshot.

### Core wrapper (always the same)

```html
<div style="width:100%;height:100%;background:{BG};display:flex;
  flex-direction:column;font-family:'Inter',sans-serif;
  overflow:hidden;position:relative;">
```

### Choose a layout pattern based on page type

| Page type | Pattern to use |
|-----------|---------------|
| Dark landing page | Glow blob + nav bar + headline bars + CTA button row |
| Light dashboard / form | White bg + coloured header bar + form field rows + submit button |
| Dark dashboard (charts/stats) | Sidebar strip + chart bars + stat numbers row |
| Neon / experimental | Large accent headline bars + accent stripe ticker at bottom |
| Restaurant / luxury | Warm glow + plate circle illustration + gold rule at bottom |
| Weather / search | Coloured search bar + stacked result cards |
| AI / knowledge | Dual-colour glows + input field + entry cards with accent headings |
| Energy / solar | Sun glow top-right + gradient headline + stat strip at bottom |

### Glow blob pattern (dark pages)

```html
<div style="position:absolute;top:-10%;left:-10%;width:55%;aspect-ratio:1;
  border-radius:50%;background:radial-gradient(circle,
  rgba(R,G,B,0.18) 0%,transparent 65%);pointer-events:none;"></div>
```

Use the accent colour for the rgba values. Keep opacity 0.12–0.22 so it reads
as atmosphere rather than a solid shape.

### Headline bar set (dark pages)

```html
<!-- eyebrow line -->
<div style="height:4px;background:rgba(ACCENT,0.5);border-radius:1px;
  width:30%;margin-bottom:8px;"></div>
<!-- h1 line 1 -->
<div style="height:12px;background:#e8eaf0;border-radius:2px;
  width:88%;margin-bottom:4px;"></div>
<!-- h1 line 2 -->
<div style="height:12px;background:#e8eaf0;border-radius:2px;
  width:66%;margin-bottom:4px;"></div>
<!-- accent word -->
<div style="height:12px;background:ACCENT_GRADIENT;border-radius:2px;
  width:46%;margin-bottom:12px;"></div>
```

### CTA button row

```html
<div style="display:flex;gap:6px;">
  <!-- primary -->
  <div style="background:ACCENT;border-radius:3px;padding:5px 14px;">
    <div style="height:3px;background:#fff;border-radius:1px;width:38px;"></div>
  </div>
  <!-- ghost -->
  <div style="border:1px solid rgba(ACCENT,0.4);border-radius:3px;padding:5px 12px;">
    <div style="height:3px;background:rgba(ACCENT,0.6);border-radius:1px;width:28px;"></div>
  </div>
</div>
```

### Light form layout

```html
<div style="background:#f8fafc;...">
  <!-- header bar -->
  <div style="display:flex;align-items:center;justify-content:space-between;
    padding:5% 7% 3%;border-bottom:1px solid rgba(ACCENT,0.12);flex-shrink:0;">
    <div style="height:5px;background:ACCENT;border-radius:1px;width:44px;"></div>
    <div style="background:ACCENT;border-radius:3px;padding:3px 10px;">
      <div style="height:2.5px;background:#fff;border-radius:1px;width:24px;"></div>
    </div>
  </div>
  <!-- form rows -->
  <div style="flex:1;padding:5% 7%;display:flex;flex-direction:column;gap:6px;justify-content:center;">
    <div style="background:#fff;border:1px solid #e2e8f0;border-radius:3px;padding:5px 9px;">
      <div style="height:2.5px;background:#94a3b8;border-radius:1px;width:55%;"></div>
    </div>
    <!-- repeat 2–3 more rows, varying widths -->
    <!-- submit button -->
    <div style="background:ACCENT;border-radius:3px;padding:6px 9px;margin-top:2px;">
      <div style="height:3px;background:#fff;border-radius:1px;width:40%;margin:0 auto;"></div>
    </div>
  </div>
</div>
```

---

## 3 · Choose tags

Use at most **3 tags**. At least one should be `tag-gray`.

| Colour class | Use for |
|--------------|---------|
| `tag-mint` | AI, SaaS, Developer tools, Weather, Green-tech |
| `tag-amber` | Finance, Energy, Fine dining, Warm/luxury brands |
| `tag-gray` | Default: Dashboard, Landing Page, Brand, UI, Booking, etc. |

---

## 4 · Card HTML template

Insert this block **before** the `</div></div></section>` that closes the
Selected Work grid (search for the last `</article>` in the `#projects`
section).

```html
<!-- {PageName} — CSS mini-UI preview -->
<article class="work-card reveal">
  <a class="work-thumb" href="{filename}" aria-label="Open {PageName} project"
     style="display:block;overflow:hidden;">
    <div style="width:100%;height:100%;background:{BG};display:flex;
      flex-direction:column;font-family:'Inter',sans-serif;
      overflow:hidden;position:relative;">
      {THUMBNAIL_CONTENT}
    </div>
  </a>
  <div class="work-body">
    <div class="work-name">{PageName}</div>
    <p class="work-problem">{One sentence: what problem/concept the page demonstrates.}</p>
    <div class="work-tags">
      <span class="tag tag-{color1}">{Tag1}</span>
      <span class="tag tag-{color2}">{Tag2}</span>
    </div>
    <div class="work-foot">
      <a class="btn-project" href="{filename}">View Project</a>
      <a class="btn-github"
         href="https://github.com/Phakinza007/my-portfolio/blob/main/{filename}"
         target="_blank" rel="noopener noreferrer"
         aria-label="View {PageName} source on GitHub">
        <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">
          <path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205
          11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724
          -4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087
          -.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07
          1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3
          -5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54
          -1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405
          1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645
          1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805
          5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015
          3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297
          c0-6.627-5.373-12-12-12"/>
        </svg>
      </a>
    </div>
  </div>
</article>
```

---

## 5 · Update sitemap.xml

Add the new URL **before** the closing `</urlset>` tag:

```xml
<url>
  <loc>https://phakinza007.github.io/my-portfolio/{filename}</loc>
  <changefreq>monthly</changefreq>
  <priority>0.7</priority>
</url>
```

---

## 6 · Mobile overflow check

After inserting the card, navigate to `index.html` in the preview, resize to
375 × 812 px, and run:

```js
(function(){
  const can = (function(){
    document.documentElement.scrollLeft = 50;
    const s = document.documentElement.scrollLeft;
    document.documentElement.scrollLeft = 0;
    return s > 0;
  })();
  return { canScrollX: can, bw: document.body.scrollWidth,
           cw: document.documentElement.clientWidth,
           cards: document.querySelectorAll('.work-card').length };
})()
```

`canScrollX: false` = ✅ done. If `true`, find the overflowing element and
fix — most common cause is a flex/grid container without `minmax(0,1fr)` or a
large `gap` that pushes past the viewport.

---

## 7 · Commit

Stage `index.html` and `sitemap.xml`, commit with a message that names the new
project and what the card thumbnail represents.

---

## Quick reference: existing tag-color examples

| Project | Tags used |
|---------|-----------|
| LaunchLedger | `tag-mint` Finance, `tag-gray` Dashboard |
| DRIP Coffee | `tag-mint` Café, `tag-gray` Brand |
| SORN Restaurant | `tag-amber` Fine Dining, `tag-gray` Restaurant |
| SolarPeak | `tag-amber` Energy, `tag-gray` Landing Page |
| Knowledge AI | `tag-mint` AI, `tag-gray` Dashboard |
| BookEase | `tag-gray` × 3 (Light UI, Dashboard, Booking) |
