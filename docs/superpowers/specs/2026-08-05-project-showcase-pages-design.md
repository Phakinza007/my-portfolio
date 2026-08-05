# Project Showcase Pages — Design

## Context

Right now 12 of the 13 "Selected Work" cards in `index.html` link straight from the thumbnail to the live demo page (e.g. `gym-landing.html`). There's no page in between that explains *what the project is, what it demonstrates, or why a visitor might want something similar built for their own business*. Only HabitQuest has a write-up, via the separate `case-study-habitquest.html`.

Phakin found a reference page — [bigzweb.com/projects/vibecoffeebkk](https://www.bigzweb.com/projects/vibecoffeebkk), a client-project detail page from a Thai web agency (Bigzweb) — and wants each project card to open into a similar showcase page before reaching the live demo: a real screenshot up top, a short pitch of what the project is and who it suits, and a path to either view the live page or get in touch about similar work. The reference itself ends in a Fastwork CTA, which matches how Phakin already drives leads.

The reference page is much heavier than what this spec adopts — it has view counters, a publish date, an embedded "chat with AI about this project" widget, and a two-column long-form article with a sticky sidebar and "read more" expansion. None of that carries over (see Non-goals) — this spec keeps the parts of the reference that add real value (hero framing, scannable overview blocks, related work) and drops the parts that only work for an agency with backend infrastructure and real project metrics.

## Goals

1. Every one of the 13 "Selected Work" cards opens into a showcase page — one consistent template — before the live demo.
2. Showcase pages use **real screenshots** of the live project, framed in a browser-chrome hero, not the CSS mini-UI previews already used on the index cards.
3. Each page gives a visitor enough to decide in ~30 seconds whether the project is relevant to them, then offers two paths: view the live page, or contact Phakin about similar work (Fastwork / email).
4. Visual design matches the rest of the site exactly — same `--accent: #5274f8`, same `assets/portfolio-pages.css` components (`.page-shell`, `.topbar`, `.button`, etc.) used by the existing case-study pages. No new theme.
5. HabitQuest's showcase page links onward to its existing full case study (`case-study-habitquest.html`) — the only project with both.

## Non-goals

- **No AI chat widget.** The reference's "คุยกับ AI เกี่ยวกับโปรเจกต์นี้" needs a backend/API this static site doesn't have. Replaced by the existing Fastwork/contact CTA pattern already used site-wide.
- **No long-form two-column article with sticky sidebar and "read more."** Writing unique long-form copy for 13 projects duplicates what the 4 existing `case-study-*.html` pages already do for their (different, more developed) projects, for marginal benefit on what are largely template/demo pages. Showcase pages stay to one scannable screen: overview, highlights, who it's for, CTA, related work.
- **No fake metrics.** No view counters, no publish dates, no manufactured stats — the reference has these because it's tracking real client projects; inventing them here would be dishonest.
- **No carousel/JS for related work.** Only 3 related cards are shown, in a static grid — a carousel is unjustified complexity for 3 items.
- **No dark theme.** The reference's dark-purple palette was considered and explicitly rejected in favor of matching the existing site.
- **No changes to the 4 existing `case-study-*.html` pages** or to how `#case-studies` on `index.html` works — this is additive, a new layer between the project cards and their demos.

## Page Template

One structure, reused across 13 new files (`showcase-<slug>.html`):

```
Topbar        — same nav pattern as case-study pages (Back to portfolio / Live site / Contact / Resume)
Meta bar      — "PROJECT" badge (deliberately not "CASE STUDY" — that label stays reserved for the 4 existing `case-study-*.html` pages, to avoid the two page types reading as the same thing) + this project's tag chips (tag-mint / tag-amber / tag-gray, reused from CLAUDE.md's existing tag assignments)
H1 + subtitle — project name + one-line positioning
Hero          — browser-chrome frame (traffic-light dots + fake URL bar) around a real screenshot
                → primary button "ดูเว็บจริง" (opens the live demo page)
                → ghost button "ติดต่อเรา" (Fastwork)
Content blocks (icon-led, matching the existing .proof-item-style visual language):
  ภาพรวมโปรเจกต์  — paragraph description + tag chips
  จุดเด่น          — 3–5 bullet highlights specific to that project
  เหมาะกับใคร      — 1 paragraph: what kind of business/client this style suits
CTA band      — "สนใจผลงานแบบนี้สำหรับธุรกิจคุณ?" + Fastwork (primary) + email (ghost)
Related work  — static 3-card grid, each linking to another project's showcase page (curated per page by shared tags/category — e.g. RATRI Restaurant surfaces other food/hospitality or booking-flow projects — not random or alphabetical)
Footer        — same as other pages
```

HabitQuest's page additionally gets a "อ่าน full case study →" link near the hero, pointing at `case-study-habitquest.html`.

## Content Plan

For each of the 13 projects, write:
- **Overview paragraph** — expanded from the one-liner already in that project's `.work-problem` copy in `index.html`
- **3–5 highlight bullets** — concrete, specific features of that particular page (not generic filler)
- **"Who this suits" paragraph** — what kind of real business this style/approach fits, in service of the same lead-gen goal the reference page serves for Bigzweb
- **Tags** — reused as-is from the existing per-project tag assignments (CLAUDE.md table), no new taxonomy

## Assets

- **Screenshots**: captured fresh for all 13 projects (only 8 currently exist under `assets/screenshots/`, and none are framed for this use) via browser automation against the live pages, saved to `assets/screenshots/showcase-<slug>.png`, all captured at the same 1440×900 desktop viewport so the browser-chrome hero frame looks uniform across all 13 pages.
- **File naming**: `showcase-<slug>.html`, one per current project card:

| Card | New file |
|---|---|
| BuildNest Construction | `showcase-buildnest.html` |
| Iron Republic | `showcase-iron-republic.html` |
| NOIR Coffee | `showcase-noir-coffee.html` |
| Elevate Commerce | `showcase-elevate-commerce.html` |
| Elasticshop Gaming | `showcase-elasticshop-gaming.html` |
| RATRI Restaurant | `showcase-ratri-restaurant.html` |
| SolarPeak | `showcase-solarpeak.html` |
| BookEase Dashboard | `showcase-bookease.html` |
| MuseRoom | `showcase-museroom.html` |
| LUMI Clinic | `showcase-lumi-clinic.html` |
| BRIGHT Dental Clinic | `showcase-dental-clinic.html` |
| VELVÉ Aesthetics | `showcase-velve-aesthetics.html` |
| HabitQuest | `showcase-habitquest.html` |

## Integration Changes

- **`index.html`**: each of the 13 cards' thumbnail link and "View Project" button now point to the project's `showcase-<slug>.html` instead of straight to the demo page. The GitHub icon link is untouched (still points at source). HabitQuest's card link changes from the external Vercel URL to its new showcase page; the showcase page itself links onward to the external live demo.
- **`sitemap.xml`**: add all 13 new showcase URLs.

## Quality Bar

- Mobile: `canScrollX: false` at 375×812 on every new page (per CLAUDE.md standard).
- Lighthouse 100/100/100 (Accessibility/Best Practices/SEO) verified on at least one representative showcase page before rollout, per CLAUDE.md standard.
- Screenshots captured at a consistent viewport/aspect ratio so the browser-chrome hero frame looks uniform across all 13 pages.
