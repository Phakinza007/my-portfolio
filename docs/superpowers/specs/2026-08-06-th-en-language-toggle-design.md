# TH/EN Language Toggle — Design

## Context

The site currently mixes languages by section: `index.html`'s Services and Testimonials sections are in Thai (added during the [service-pivot work](2026-08-05-service-pivot-design.md), which explicitly deferred a full toggle as "materially bigger... sequenced as its own follow-up brainstorming/spec/plan cycle"), while Hero, About, Experience, Selected Work, Case Studies, and all of `resume.html` and the 4 case-study pages stay English. That's this follow-up.

Phakin wants every page that's actually *about him* — as opposed to the 13 project demo pages, which are sample client work, not content about him — to be readable in either language, with a simple TH/EN switch in the nav.

**Domain note:** `ph-akin.dev` is a registered domain but still resolves to its registrar's parking page (confirmed via DNS/curl during this brainstorm — same broken state found and worked around in the [technical SEO fix](2026-08-05-technical-seo-fix.md)). This spec uses `https://phakinza007.github.io/my-portfolio/` as the base for all absolute URLs (hreflang, canonical, sitemap), consistent with that earlier decision. If the custom domain is ever configured, both this spec's URLs and the SEO fix's URLs need updating together.

## Goals

1. Every page listed in Scope has a Thai counterpart, reachable via a "TH | EN" link in the nav (desktop and mobile).
2. Search engines can correctly index both language versions as distinct, related pages (via `hreflang`), rather than the toggle looking like duplicate content.
3. Thai copy reads naturally — same conversational voice as the existing Services/Testimonials sections — not a literal translation.
4. Navigating within one language stays in that language: every internal link on a Thai page points at the Thai counterpart of its target, where one exists.

## Non-goals

- **No browser-locale auto-detection or redirect.** The site is static with no server-side logic; auto-detection would need JS-based redirect or server config, adding real complexity for a feature the user didn't ask for. Language is chosen only by clicking the nav link.
- **No JS-based instant toggle (shared DOM, hidden/shown per language).** Considered and rejected: hurts SEO (crawlers see both languages in one DOM, no distinct URL per language) and doesn't fit a static, no-build-step site as naturally as two plain files. See Approach comparison below.
- **The 13 project demo pages are not translated** (`construction-landing.html`, `gym-landing.html`, etc.) — they're sample client work simulating different fictional businesses, not content about Phakin. Some already contain Thai copy as part of that simulated client's brand (e.g. BRIGHT Dental Clinic, VELVÉ Aesthetics) — that's unrelated and stays exactly as is.
- **No dropdown or flag-icon language picker.** Decided: a plain "TH | EN" text link in the nav, matching the existing text-link nav style.
- **No change to `ph-akin.dev` DNS/CNAME setup** — out of scope for this spec; see Domain note above.

## Approach: paired files + `hreflang`, not a JS toggle

Two approaches were considered:

1. **Paired static files + `hreflang`** (chosen) — every in-scope page gets a sibling file with a `-th` suffix (`index.html` ↔ `index-th.html`, `resume.html` ↔ `resume-th.html`, `case-study-launchledger.html` ↔ `case-study-launchledger-th.html`, `showcase-buildnest.html` ↔ `showcase-buildnest-th.html`, etc.). Each file's `<head>` declares both language versions via `<link rel="alternate" hreflang="...">`, so Google can index and rank each language independently for its own search queries — the standard, Google-recommended pattern for multilingual static sites. The nav's "TH | EN" link is a plain `<a href>` to the sibling file — full page load, no JS state.
2. **Client-side JS toggle** — one file per page, both languages present in the DOM, toggled by a script (state in `localStorage`). Faster to switch (no reload) but: crawlers see both languages in the same document with no distinct URL to rank per language; every page's markup roughly doubles in size; doesn't fit this codebase's existing pattern (13 independent project files, no shared templating/build step) as naturally as adding sibling files does.

Chosen: **Option 1.** The site just went through real SEO work (fixing a broken canonical domain) — introducing a mechanism that's harder for Google to parse correctly would undercut that. A no-build, plain-HTML site is also the natural fit for "two files" over "one file with a JS state machine."

## Scope — which pages get a Thai counterpart

| English file | Thai counterpart |
|---|---|
| `index.html` | `index-th.html` |
| `resume.html` | `resume-th.html` |
| `case-study-pulseboard.html` | `case-study-pulseboard-th.html` |
| `case-study-launchledger.html` | `case-study-launchledger-th.html` |
| `case-study-interntrack.html` | `case-study-interntrack-th.html` |
| `case-study-habitquest.html` | `case-study-habitquest-th.html` |
| `showcase-buildnest.html` | `showcase-buildnest-th.html` |
| `showcase-iron-republic.html` | `showcase-iron-republic-th.html` |
| `showcase-noir-coffee.html` | `showcase-noir-coffee-th.html` |
| `showcase-elevate-commerce.html` | `showcase-elevate-commerce-th.html` |
| `showcase-elasticshop-gaming.html` | `showcase-elasticshop-gaming-th.html` |
| `showcase-ratri-restaurant.html` | `showcase-ratri-restaurant-th.html` |
| `showcase-solarpeak.html` | `showcase-solarpeak-th.html` |
| `showcase-bookease.html` | `showcase-bookease-th.html` |
| `showcase-museroom.html` | `showcase-museroom-th.html` |
| `showcase-lumi-clinic.html` | `showcase-lumi-clinic-th.html` |
| `showcase-dental-clinic.html` | `showcase-dental-clinic-th.html` |
| `showcase-velve-aesthetics.html` | `showcase-velve-aesthetics-th.html` |
| `showcase-habitquest.html` | `showcase-habitquest-th.html` |

19 English pages get a Thai sibling (38 total including originals). Everything else in the repo (13 project demo pages, `404.html`, `sitemap.xml`, `robots.txt`, `CNAME`-adjacent config) is unaffected.

## Per-page requirements

Every `-th.html` file:

- `<html lang="th">` (not `en`) — required for correct screen-reader pronunciation and Lighthouse Accessibility, independent of SEO.
- `<title>`, meta description, `og:title`, `og:description`, `twitter:title`, `twitter:description` — Thai versions, written fresh (not translated word-for-word), same conversational tone as the existing Services/Testimonials copy.
- `og:locale` set to `th_TH` (English pages keep `en_US`).
- `<link rel="canonical" href="https://phakinza007.github.io/my-portfolio/<file>-th.html">` — points at itself, not the English original.
- Both files get a matching pair:
  ```html
  <link rel="alternate" hreflang="en" href="https://phakinza007.github.io/my-portfolio/<file>.html" />
  <link rel="alternate" hreflang="th" href="https://phakinza007.github.io/my-portfolio/<file>-th.html" />
  <link rel="alternate" hreflang="x-default" href="https://phakinza007.github.io/my-portfolio/<file>.html" />
  ```
  (`x-default` points at English, matching the SEO-fix decision that English/the github.io URL is the primary indexed version.)
- JSON-LD (`index.html`/`resume.html` only): `"url"` points at the `-th.html` file's own URL, `"inLanguage": "th"` added, `"name"` stays `"Phakin Chawanpunya"` (not translated).
- Body copy, nav labels, section headings, buttons, Contact form labels/placeholders — Thai, written naturally. The Formspree form `action` endpoint stays identical in both languages (it's not user-facing content).
- `og:image`/`twitter:image` — same image asset as the English version (no separate Thai social-preview image).
- `index-th.html` specifically: the Services and Testimonials sections are *already* natural Thai copy in `index.html` — carry that text over as-is rather than rewriting it. Only Hero, About, Experience, Selected Work, and Case Studies sections need fresh Thai copy.

## Internal link rules

The core rule: **while on a Thai page, every internal link that has a Thai counterpart points at that counterpart; every link that doesn't (because its target is out of scope) stays pointed at the one URL that exists.**

- `index-th.html`'s nav → `resume-th.html`; its Case Studies section → `case-study-*-th.html`; its Selected Work cards → `showcase-*-th.html` (NOT the 13 demo pages directly — that link pattern, thumbnail → showcase page → demo, is unchanged from the English site, just each hop stays in Thai until the demo page itself).
- Each `showcase-*-th.html`'s related-work grid (3 cards) links to the *other* showcase pages' `-th` versions.
- Case-study pages' "View live" buttons, showcase pages' "View live site" buttons, GitHub icon links, Fastwork links, HabitQuest's Vercel URL — all point at the same target in both languages (no Thai counterpart exists for a demo page, GitHub repo, or external app).
- The "TH | EN" nav link on any English page points at its `-th` sibling; on any Thai page, it points back at the English original.

## Verification

- `hreflang` pairs are reciprocal (if A declares B, B declares A) — check systematically across all 19 pairs, since a one-directional hreflang is a common, silently-broken mistake.
- `sitemap.xml` gets 19 new `<url>` entries for the `-th.html` files, same `priority`/`changefreq` as their English counterpart.
- Lighthouse Accessibility/Best Practices/SEO all 100 on at least one Thai page (matching the standard already held for English pages).
- Manual click-through on at least one full Thai journey (index-th → a showcase-th → its related work → back to index-th) confirms no accidental language-crossing link.
