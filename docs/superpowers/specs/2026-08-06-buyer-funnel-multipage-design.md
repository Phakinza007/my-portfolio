# Buyer Funnel — Multi-Page Restructure

**Date:** 2026-08-06
**Status:** Approved, ready for implementation planning

## Context

The site currently sells through a single page. `index.html` carries Services, Testimonials,
Selected Work, About, Experience, Case Studies and Contact as anchor sections, and the nav is
eight `#anchor` links. The three service category pages added earlier the same day
(`landing-page.html`, `dashboard-ui.html`, `business-website.html`) are the only standalone
selling pages that exist.

The trigger for this work was a competitor review of `https://www.bigzweb.com/` — a Thai web
agency. Its homepage does three things this site does not:

1. A **"คุณต้องการเว็บแบบไหน?"** selector sits directly under the hero and converts a browsing
   visitor into a self-qualified lead in one click.
2. Every buyer-facing topic has **its own URL** — services, portfolio, about, FAQ, pricing,
   articles — reachable from a persistent multi-page nav with a search box.
3. Portfolio items are tagged with **search terms buyers actually type** (`รับซื้อ Scrap`,
   `ชลบุรี`, `จัดฟัน`), not style descriptors.

This spec adopts that structure. It does **not** adopt Bigzweb's credibility claims — "ประสบการณ์
20 ปี+", "ส่งมอบ 500+ โปรเจกต์", and its named corporate clients are real for them and would be
fabricated here. The 13 project pages on this site are simulated client work and stay described
as such.

## Goals

1. A visitor who knows their industry ("ผมเปิดคลินิก") reaches a page about that industry in one
   click, with matching demos and a price.
2. Buyer-facing topics are indexable URLs, so Google can rank them and ads can land on them.
3. Project tags match Thai buyer search language instead of designer vocabulary.
4. Existing quality bars hold: Accessibility 100, SEO 100, CLS 0, no horizontal overflow at
   375×812.

## Non-goals

- **No blog.** Considered and rejected — it is a recurring writing commitment, and an abandoned
  blog reads worse than no blog.
- **No AI chat assistant.** Bigzweb's "คุยกับ Bigzweb AI" is its differentiator; here it would be
  a large build with an ongoing maintenance cost, out of proportion to the rest of this work.
- **No fabricated trust signals.** No invented project counts, years of experience, or client
  names.
- **No dark theme.** Bigzweb is dark-purple; this site's light theme with `--accent: #5274f8`
  already passes WCAG AA and is a taste question, not a conversion one.
- **No standalone `/contact` page.** `#contact` on the homepage already works and a separate page
  would duplicate it.
- **No framework or build step.** The site stays plain HTML/CSS/JS.

## Decisions

Each of these was a real fork during brainstorming; the rejected option is recorded so it is not
relitigated later.

### D1 — New pages are split by industry, not by system type

Rejected: splitting by what the system does (ขายของออนไลน์ / จองคิว / เว็บบริษัท / แดชบอร์ด).
That axis already exists as the three service category pages, and buyers search by their own
industry, not by system architecture.

### D2 — Industry pages are Thai-only

Rejected: giving each one an `-en` twin. The search intent (`รับทำเว็บคลินิก`) is Thai-only, so
an English twin would double the file count for traffic that does not exist.

There is precedent in the repo: the 13 demo pages carry no `hreflang`, a self-referential
canonical, and `robots: index, follow`. Industry pages join that class. This makes **two**
documented no-`-en`-twin classes, and CLAUDE.md must say so explicitly — otherwise the next
session reads them as unfinished work.

### D3 — Seven industry pages, covering every demo

Rejected: four pages (only industries with ≥2 demos) and five (four plus construction).
Three of the seven rest on a single demo — gym, construction, solar — and must compensate with
real industry-specific content rather than a single screenshot.

### D4 — Nav rolls out to funnel pages only

The site has **two** nav systems today, not one:

| System | Files | Character |
|---|---|---|
| Homepage nav | `index.html`, `index-en.html` | anchor links + separate `.nav-mobile-panel` |
| `.page-shell.nav` | 42 files (resume ×2, case studies ×8, showcases ×26, category ×6) | **per-page links** |
| Demo page navs | 13 demo pages | belong to the simulated client site |

The `.page-shell.nav` links differ per page — `showcase-buildnest.html` links to
`construction-landing.html` under the label `ดูเว็บจริง`. That is a contextual nav, and replacing
it with a generic global nav would remove the most valuable link on the page.

So the new nav ships to the **19 funnel files** (`index` ×2, the 5 new bilingual pairs, the 7
industry pages). The 42 contextual-nav files keep their nav and gain a link back into the funnel.

Rejected: rolling the nav to all 61 files (roughly 3× the work, requires reworking 42 page heros
to rehome their contextual links, and forces a full-site Lighthouse re-run). Rejected: rendering
the nav from JS — internal links would vanish from the HTML source, and the internal link graph
is exactly what the industry pages need in order to rank. It also risks CLS, which is currently
0 sitewide.

If the full rollout is wanted later, it extends this design rather than replacing it.

### D5 — Search covers the whole site

Rejected: searching projects only. A visitor who types `ราคา` or `คลินิก` should land on the
services and industry pages, not just on demos.

### D6 — The homepage carries the full portfolio grid, not a teaser

An earlier draft of this spec moved the 13-card grid to `work.html` and left the homepage with a
5-card carousel. That was reversed: the homepage carries **both** the featured carousel and the
complete filterable grid, and `work.html` becomes the deeper archive behind a "ดูผลงานทั้งหมด"
link. This matches Bigzweb, and it means a visitor who lands on the homepage from an ad never has
to click through to see whether the work is any good.

Rejected: dropping `work.html` entirely and pointing the nav at `#projects` (the homepage grows
very long and the 4 case studies lose a home). Rejected: showing 6 cards on the homepage and 13
on `work.html` (splits the proof for no real gain).

### D7 — Technology tags sit in a static row beneath the marquee

The marquee is in continuous motion. Making its items the click targets would mean asking users
to click moving elements and tab through a scrolling strip. The marquee is kept as decoration and
a static row of real `<button>`s is added below it.

Industry and technology are **mutually exclusive filters**, not combinable. Across only 13
projects, two simultaneous axes would routinely produce an empty grid.

## Page Inventory

### Funnel pages — bilingual pairs (5 pairs, 10 files)

| Thai | English | Content |
|---|---|---|
| `work.html` | `work-en.html` | The deeper archive: same 13 cards + industry filter + tag cloud + the 4 case studies + longer per-project copy than the homepage grid carries |
| `services.html` | `services-en.html` | Hub: 3 packages linking to the existing category pages, price comparison table, entry points to the 7 industry pages |
| `about.html` | `about-en.html` | Bio, experience timeline, tools, KMUTT education |
| `faq.html` | `faq-en.html` | Pre-hire questions + `FAQPage` JSON-LD |
| `process.html` | `process-en.html` | Brief → delivery: steps, durations, what the client supplies |

`landing-page.html`, `dashboard-ui.html` and `business-website.html` are **unchanged**.
`services.html` sits above them and links down.

### Industry pages — Thai only (7 files)

| File | Industry | Demos shown |
|---|---|---|
| `web-clinic.html` | คลินิก / ความงาม | `showcase-lumi-clinic`, `showcase-dental-clinic`, `showcase-velve-aesthetics` |
| `web-booking.html` | จองคิว / นัดหมาย | `showcase-bookease`, `showcase-velve-aesthetics` |
| `web-restaurant.html` | ร้านอาหาร / คาเฟ่ | `showcase-ratri-restaurant`, `showcase-noir-coffee` |
| `web-shop.html` | ขายของออนไลน์ | `showcase-elevate-commerce`, `showcase-elasticshop-gaming` |
| `web-gym.html` | ฟิตเนส / ยิม | `showcase-iron-republic` |
| `web-construction.html` | ก่อสร้าง / รับเหมา | `showcase-buildnest` |
| `web-solar.html` | โซลาร์ / พลังงาน | `showcase-solarpeak` |

Each industry page reuses components already in `assets/portfolio-pages.css` — the same kit the
three category pages were built from, so no new page CSS is required:

- `.hero.case-hero` + `.eyebrow` + `<h1>` + `.hero-copy` + `.hero-actions` with a Fastwork
  `.button.primary`
- `.study-meta` — 4-box strip: starting price, timeline, revisions, best-for
- `.study-grid` with a `.featured` `.study-block` carrying a `.highlight-list` of the features
  that industry actually needs, plus a plain block answering "who it's for"
- `.project-strip` of `.project-link`s pointing at the demos above
- `.result-band` closing CTA (Fastwork + email)
- An industry-specific FAQ block of 4–5 questions

The three single-demo pages (gym, construction, solar) carry their weight through the feature and
FAQ blocks, not through demo count:

- **gym** — class timetable, membership tiers, trainer profiles, trial-session booking
- **construction** — project gallery, service scope, quote request form, past-work credibility
- **solar** — electricity-bill savings calculator, equipment packages, installation process

## Navigation

### Structure

```
Desktop ≥1024px
┌──────────────────────────────────────────────────────────────────────┐
│ ◈ Phakin   หน้าแรก  ผลงาน  บริการ  เกี่ยวกับผม  FAQ                   │
│                          [🔍 ค้นหาผลงาน บริการ...]  [TH ▾]  [ติดต่อ] │
└──────────────────────────────────────────────────────────────────────┘

Tablet 768–1023px   search collapses to an icon that expands on click
Mobile <768px       ☰ opens the existing .nav-mobile-panel; search is its first row
```

`process.html` is deliberately **not** in the nav — six links plus a search box plus two controls
overflow at 1024px. It is reached from `services.html`, `faq.html`, and the footer.

`TH ▾` replaces the current plain `EN` link with a real `<button aria-expanded>` plus a menu of
two items (ไทย / English), keyboard operable.

### Search

Typing ≥ 2 characters opens a dropdown grouped by result type:

```
🔍 คลินิก
┌────────────────────────────────────┐
│ บริการ                              │
│   › รับทำเว็บคลินิก / ความงาม        │
│ ผลงาน                               │
│   › LUMI Clinic                    │
│   › BRIGHT Dental Clinic           │
│   › VELVÉ Aesthetics               │
│ คำถามที่พบบ่อย                       │
│   › ทำเว็บคลินิกราคาเท่าไหร่?        │
└────────────────────────────────────┘
```

- **Substring matching, no word segmentation.** Thai does not use spaces between words, and
  client-side Thai segmentation is heavy and error-prone. Substring is both simpler and more
  accurate here.
- Every entry carries **hidden keywords**, so `หมอฟัน` finds BRIGHT Dental and `ราคา` finds the
  price comparison.
- `assets/search-index.json` is fetched on **first focus of the input**, not on page load, so
  LCP is untouched.
- The results dropdown is `position: absolute`, so **CLS stays 0**.

Index shape — hand-written, roughly 30 entries, no build step:

```json
{
  "th": [
    { "t": "รับทำเว็บคลินิก / ความงาม", "u": "web-clinic.html", "g": "บริการ",
      "k": "คลินิก ความงาม ทันตกรรม จัดฟัน ฉีดฟิลเลอร์ หมอฟัน ดูแลผิว" }
  ],
  "en": [ ... ]
}
```

The 7 industry pages appear in **both** the `th` and `en` arrays with Thai labels — the same
principle by which `index-en.html` shows package pricing in Thai.

### Accessibility

These are requirements, not suggestions; the site's Accessibility 100 must survive.

| Element | Requirement |
|---|---|
| Search input | `role="combobox"`, `aria-expanded`, `aria-controls`, `aria-activedescendant` |
| Results list | `role="listbox"` with `role="option"` children |
| Keyboard | `↑`/`↓` move, `Enter` opens, `Esc` closes and returns focus to the input |
| Result count | announced via `aria-live="polite"` |
| `TH ▾` | a real `<button aria-expanded>` with a keyboard-operable menu |

### New shared assets

```
assets/site-nav.css        nav + search dropdown styles
assets/site-nav.js         search, language menu, mobile panel behaviour
assets/search-index.json   { "th": [...], "en": [...] }
```

This follows the existing shared-asset convention (`portfolio-pages.css`,
`portfolio-context.css`, `analytics.js`) — referenced by **relative** path, per CLAUDE.md.

### Analytics

Two events added to the existing delegated tracking in `assets/analytics.js`:

- `nav_search` — carries the query string
- `search_result_click` — carries the destination

Queries that return nothing are the signal for which industry page to build next.

## Homepage Restructure

The homepage is not gutted — the opposite. It carries the full selling story, and the child pages
exist as deeper destinations rather than as the only home for that content. This mirrors Bigzweb,
whose homepage carries both a featured carousel *and* the complete filterable portfolio grid, with
a link out to a fuller portfolio page.

```
1   Hero                          unchanged
2   คุณต้องการเว็บแบบไหน?          NEW — directly under the hero, qualifies the visitor
3   ผลงานแนะนำ                     carousel of the 5 featured
4   ผลงานของเรา                    full 13-card grid + industry filter
    └─ ดูผลงานทั้งหมด → work.html

    ╔══ decision block — kept contiguous ══╗
5   บริการของเรา                   3 packages → services.html
6   ราคา                          NEW — ฿3,900 / ฿7,900 / ฿9,900 comparison
7   รีวิว                          3 real 5★ Fastwork reviews, full, not trimmed
    ╚═════════════════════════════════════╝

8   เทคโนโลยีและเฟรมเวิร์ก          marquee + NEW clickable tech tags
9   เกี่ยวกับผม (condensed)        → about.html
10  Case studies (condensed)      → work.html
11  ติดต่อ                         unchanged, full
```

**Sections 5–7 stay contiguous on purpose.** A visitor who has just read a price is at peak
objection; the reviews answer it immediately. Placing the technology section between them —
the ordering originally sketched — interrupts that with a low-intent "how it's built" digression.

**`work.html` is the deeper archive, not a duplicate.** It carries the same 13 cards plus the 4
case studies, the tag cloud, and longer per-project copy. The 13 cards appearing on two pages is
intentional and not a duplicate-content problem: they are card summaries, not substantive page
bodies, and each links to its own showcase page.

### Pricing section (new, section 6)

A three-column comparison of the existing packages — ฿3,900 Landing Page, ฿7,900 Dashboard UI,
฿9,900 Business Website. Prices, feature bullets and package names are copied **verbatim** from
`index.html`'s current `#services` section; they are real Fastwork listings and must not be
reworded. Each column links to its category page and to Fastwork.

Per the existing bilingual rule, this section's pricing and feature copy stays in Thai on
`index-en.html` as well.

### The need selector

```
        คุณต้องการเว็บแบบไหน?
เลือกประเภทที่ใกล้เคียง — พาไปดูผลงานจริงและราคาของหมวดนั้นทันที

┌──────────┬──────────┬──────────┬──────────┐
│ คลินิก    │ จองคิว    │ ร้านอาหาร │ ขายของ    │
│ ความงาม   │ นัดหมาย   │ คาเฟ่     │ ออนไลน์   │
├──────────┼──────────┼──────────┼──────────┤
│ ฟิตเนส    │ ก่อสร้าง  │ โซลาร์    │ ไม่แน่ใจ  │
│ ยิม       │ รับเหมา   │ พลังงาน   │ ปรึกษาก่อน│
└──────────┴──────────┴──────────┴──────────┘
     4×2 desktop  ·  2×4 mobile
```

Seven tiles link to their industry page; the eighth links to `#contact`.

Icons are **inline SVG**, not emoji — emoji render inconsistently across platforms and screen
readers announce them unpredictably. The tech marquee already establishes inline SVG as the
site's icon pattern.

### Clickable technology section (new behaviour, section 8)

Today the dual-row logo marquee is purely decorative. It becomes a way into the work:

```
        เทคโนโลยีและเฟรมเวิร์ก
เทคโนโลยีที่ผมใช้ในผลงาน — คลิกเพื่อดูโปรเจกต์ที่ใช้เทคโนโลยีนั้น

  [ existing dual-row logo marquee — unchanged, decorative, aria-hidden ]

  HTML   CSS   JavaScript   React   Node.js   Express
  PostgreSQL   Figma   Tailwind   Chart.js   ...
  └── static row of real <button>s
```

**The marquee is kept and a static clickable row is added beneath it**, rather than making the
marquee items themselves clickable. Marquee items are in continuous motion; clicking a moving
target is hostile, and tabbing through a scrolling strip is worse. The marquee stays as the
visual, the static row does the work. The existing `prefers-reduced-motion` static fallback and
pause-on-hover behaviour are untouched.

Clicking a technology scrolls to `ผลงานของเรา` and filters the grid to projects using it.

**Two filter axes, one active filter.** The grid can be filtered by industry (the button bar) or
by technology (this section) but never both at once — selecting one clears the other, and an
active-filter chip with a dismiss control shows what is applied. Two simultaneous axes would
routinely produce empty result sets across only 13 projects.

**Technology tags must be truthful.** The 13 projects are simulated client work and most are
static HTML/CSS/JS; the marquee currently advertises React, Node.js, Express and PostgreSQL,
which reflects Phakin's skill set rather than every demo's stack. During implementation, each
project's `data-tech` value must be taken from what that project actually uses — read from its
showcase page's stated stack — not assigned to make a technology look well-represented. A
technology with no truthful matches does not get a button.

## Tag Taxonomy

### The problem

The filter bar keys are `landing`, `app`, `dashboard`, `ecommerce`, `fullstack`. No shop owner
thinks "I need a fullstack". The visible card tags are English style descriptors
(`Construction`, `Landing`, `Dark`). The 24-item tag cloud is inert `<span>`s.

### Filter axis becomes industry

```
ทั้งหมด · คลินิก · จองคิว · ร้านอาหาร · ขายของออนไลน์ · ฟิตเนส · ก่อสร้าง · โซลาร์ · อื่นๆ
```

`อื่นๆ` is required, not filler: **MuseRoom** (gallery) and **HabitQuest** (habit app) match none
of the seven industries and would otherwise disappear from the filter entirely.

Full mapping of the 13 cards:

| Card | Industry key(s) |
|---|---|
| BuildNest Construction | `construction` |
| Iron Republic | `gym` |
| NOIR Coffee | `restaurant` |
| Elevate Commerce | `shop` |
| Elasticshop Gaming | `shop` |
| RATRI Restaurant | `restaurant` |
| SolarPeak | `solar` |
| BookEase Dashboard | `booking` |
| MuseRoom | `other` |
| LUMI Clinic | `clinic` |
| BRIGHT Dental Clinic | `clinic` |
| VELVÉ Aesthetics | `clinic`, `booking` |
| HabitQuest | `other` |

### Card tags become buyer search terms

Three to four per card. Examples:

| Card | Before | After |
|---|---|---|
| BuildNest | `Construction` `Landing` | `ก่อสร้าง` `รับเหมา` `ขอใบเสนอราคา` |
| LUMI Clinic | `Beauty` `Landing Page` `Brand` | `คลินิกความงาม` `จองคิวออนไลน์` `ดูแลผิว` |
| BRIGHT Dental | `Healthcare` `Landing Page` `Booking` | `คลินิกทันตกรรม` `จัดฟัน` `รากเทียม` |

`-en` pages carry English equivalents, but both languages share the same underlying
`data-industry` keys so the filter behaves identically.

Tag colour classes (`tag-mint`, `tag-amber`, `tag-gray`, `tag-rose`, `tag-accent`) are unchanged.

### Tag cloud becomes clickable

The 24 inert spans become buttons that **fire the site search** with that term. This gives them a
job without duplicating the filter bar — the filter narrows the grid on the current page, search
crosses the whole site — and exercises the search index that is being built anyway.

## Attached Fixes

Small problems found while surveying the code that this work touches directly:

- `data-tags` → `data-industry` affects both the filter JS **and** the featured carousel, which
  reads `data-featured` from the same elements. A third attribute, `data-tech`, is added for the
  technology filter. All three live on the same `.work-card` elements and must change together.
- CLAUDE.md's "Current Cards in Selected Work" table is stale: it lists card 1 as
  `construction-landing.html`, but the card links to `showcase-buildnest.html`. Since this work
  rewrites that table's tag column anyway, correct the file column at the same time.

## Files Touched

**New (17):**
`work.html`, `work-en.html`, `services.html`, `services-en.html`, `about.html`, `about-en.html`,
`faq.html`, `faq-en.html`, `process.html`, `process-en.html`, `web-clinic.html`,
`web-booking.html`, `web-restaurant.html`, `web-shop.html`, `web-gym.html`,
`web-construction.html`, `web-solar.html`

**New shared assets (3):**
`assets/site-nav.css`, `assets/site-nav.js`, `assets/search-index.json`

**Modified:**
`index.html`, `index-en.html` — the largest change: 11-section restructure, new nav, need
selector, new pricing section, clickable technology row, and the filter axis rewrite,
`assets/analytics.js` (two events), `sitemap.xml` (17 new URLs, 59 → 76), `CLAUDE.md` (structure,
the two no-`-en`-twin classes, corrected cards table, new homepage section table)

**Untouched:** the 13 demo pages, the 3 service category pages, the 42 contextual-nav files
except for one added link back into the funnel.

## Verification

Every item must pass before the work is called done:

1. **Lighthouse mobile** on all 17 new pages plus the rebuilt homepage: Accessibility 100,
   SEO 100. Best Practices caps at 77 sitewide because Microsoft Clarity sets third-party
   cookies — that is the documented accepted exception and is not a regression.
2. **No horizontal overflow** at 375×812 on every new page: `canScrollX: false`,
   `body.scrollWidth === documentElement.clientWidth`. Window resizing does not take effect in
   this environment; use the 375×812 iframe method instead and confirm `clientWidth === 375`
   before trusting the result.
3. **CLS 0** on pages carrying the search box.
4. **Search keyboard path** works without a mouse: focus input → type → `↓` → `Enter` navigates;
   `Esc` closes and returns focus.
5. **Filter mutual exclusion** — selecting an industry clears any active technology filter and
   vice versa; the active-filter chip reflects what is applied and dismisses correctly. No
   combination of clicks can produce a silently empty grid with no chip explaining why.
6. **Technology tags are truthful** — every `data-tech` value on a card is backed by that
   project's actually stated stack, and every technology button returns at least one project.
7. **hreflang audit** — the 5 funnel pairs each carry the 3-link trio and a self canonical; the 7
   industry pages carry no `hreflang` and a self canonical.
8. **Every new URL is in `sitemap.xml`** and reachable by at least one crawlable `<a href>` from
   the homepage.
