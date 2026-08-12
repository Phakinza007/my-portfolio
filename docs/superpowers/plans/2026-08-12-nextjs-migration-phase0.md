# Next.js Migration — Phase 0 (De-risking Spike) Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Prove, on a throwaway branch and without touching a single live file, that Next.js 15 + TypeScript + Tailwind can reproduce three representative pages of ph-akin.dev at byte-identical URLs, with Lighthouse 100/100/100 and CLS 0 — or find out which of those is impossible before any of the 84 pages is rewritten.

**Architecture:** A separate `_spike-next/` directory inside the repo, building to `_spike-next/out/`, never deployed. **The leading underscore is load-bearing:** `main` auto-deploys and Jekyll serves every root path it is not told to skip, so a plain `next/` directory would publish the spike's `.tsx` sources at `ph-akin.dev/next/app/page.tsx`. Underscore-prefixed paths are skipped without touching `_config.yml`, the same guard that already keeps `_tools/`, `_docs/` and `_content/` off the site. Three pages are ported by hand — one home-shell page, one showcase page, one Thai-only industry page — because between them they exercise every mechanism the real migration must preserve. Nothing in the repo root changes. The spike is deleted or promoted at the end.

**Tech Stack:** Next.js 15 (App Router, `output: 'export'`), TypeScript 5, Tailwind CSS 4, Node 26.5.1 / npm 11.17.0 (confirmed present on this machine 2026-08-12).

---

## Why a spike and not a migration

The site is at Lighthouse 100/100/100 with CLS 0 across 84 pages, 21 of them bilingual pairs
with a three-link `hreflang` trio each. Five mechanisms currently work and are not obviously
reproducible in Next:

| Mechanism | Why it is at risk |
|---|---|
| Extensionless URLs (`/showcase-buildnest`) | GitHub Pages resolves `/foo` → `foo.html` on its own. Next `output: 'export'` decides the emitted filename from `trailingSlash`, and the two conventions do not obviously meet. **84 indexed URLs depend on this.** |
| `hreflang` trio + self-canonical on 21 pairs | Next's built-in i18n routing is Pages-Router-only and is unsupported under `output: 'export'`. The `-en` suffix convention must be built by hand. |
| View Transitions | `@view-transition { navigation: auto }` is **cross-document only**. App Router client navigation bypasses it entirely, so it silently stops working. |
| CLS 0 via `display=optional` | `next/font` self-hosts and injects its own `font-display`. Whether it can be pinned to `optional`, and what that does to the Thai faces, is unverified. |
| Thai typography | `.section-heading .eyebrow` carries `margin-bottom: 12px` **because Thai upper vowels and tone marks collide with the line above at line-height 1.1**. Tailwind's type scale is Latin-tuned and will reintroduce that collision unless the theme is ported deliberately. |

Phase 0 answers all five on three pages. If any answer is "no", that is worth knowing for the
cost of a spike rather than the cost of 84 rewrites.

## Global Constraints

Copied verbatim from CLAUDE.md. Every task's requirements implicitly include this section.

- **URLs carry no `.html`.** Every internal link, `canonical`, `hreflang`, `og:url`, JSON-LD `item`, `sitemap.xml` `<loc>` and `search-index.json` `u` points at an extensionless URL. `index.html` is `/`.
- **Thai is the site default.** `hreflang`: `th` → Thai URL, `en` → `-en` URL, **`x-default` → the Thai URL**. `canonical` on each file points at **itself**, never at its counterpart.
- **Internal links stay in-language.** A Thai page links to Thai pages; an `-en` page links to `-en` pages. The only cross-language link is the `TH`/`EN` switcher.
- **`og:locale`**: `th_TH` on Thai, `en_US` on English.
- **A page loads exactly one stylesheet family.** `home-shell.css` and `portfolio-pages.css` define `.hero`, `.section`, `.nav-links` and all five `.tag*` classes differently — nine colliding selectors. Loading both breaks the page.
- **Accent** `--accent: #5274f8`. **Button bg** `--accent-dark: #3651d4`. **Overflow guard** `html, body { overflow-x: hidden }`.
- **Fonts** load with `display=optional`, never `swap`. Body: `Outfit` on home-shell pages, `Inter` + `Noto Sans Thai` on portfolio-pages ones. Headings on both: `Bai Jamjuree` via `--font-display`.
- **Lighthouse targets:** Accessibility 100, SEO 100, Performance 100. Best Practices caps at 77 sitewide because Microsoft Clarity sets third-party cookies — that one deduction is accepted and must not be chased. Any *other* Best Practices deduction is a real regression.
- **Mobile:** `canScrollX: false` at 375 × 812 on every page.
- **The 15 demo pages are simulations of client sites and must not wear portfolio chrome** — no site search, no back-to-portfolio link, no shared reset. They are out of scope for every phase and stay as static files.
- **Never hide a `.reveal` element with anything that shrinks its box** — not `clip-path`, not `visibility: hidden`, not `display: none`, not `width: 0`. Chrome subtracts a target's own `clip-path` from its intersection rect, so the observer never fires and the element stays invisible forever. Use `opacity` or `transform` only.

## Verification environment

- `python3 _tools/serve.py 8123` — **not** `python3 -m http.server`, which cannot resolve extensionless paths and makes every internal link 404.
- Lighthouse: `npx -y lighthouse <url> --quiet --chrome-flags="--headless" --output=json --output-path=/tmp/lh.json`, then read `categories`.
- ⚠️ **A background browser tab reports every reveal as broken and every transition as stuck at its start value.** Chrome suspends IntersectionObserver and freezes CSS transitions in a hidden tab. Verify end states by disabling the transition and reading the computed value, not by waiting.

---

## File Structure

Everything lives under `_spike-next/`, which is git-tracked but never deployed. The repo root is untouched by every task in this plan.

| Path | Responsibility |
|---|---|
| `_spike-next/package.json` | Pins Next 15, React 19, TypeScript 5, Tailwind 4. Scripts: `dev`, `build`, `verify`. |
| `_spike-next/next.config.ts` | `output: 'export'`, `trailingSlash`, `images.unoptimized`, `distDir`. The whole URL question lives in this file. |
| `_spike-next/tsconfig.json` | Strict mode, `@/*` path alias. |
| `_spike-next/app/layout.tsx` | `<html lang>` is per-page, so this holds only what is truly global. |
| `_spike-next/app/globals.css` | Tailwind entry + the ported design tokens. |
| `_spike-next/lib/site.ts` | `SITE`, `hreflangFor()`, `canonicalFor()` — the bilingual URL rules in one place. |
| `_spike-next/lib/copy.ts` | Reads `_content/project-copy.json`. The single source built on 2026-08-12 becomes the migration's content layer. |
| `_spike-next/app/page.tsx` | Thai homepage → `/`. Home-shell family. |
| `_spike-next/app/showcase-buildnest/page.tsx` | Portfolio-pages family, bilingual pair, story stack. |
| `_spike-next/app/web-clinic/page.tsx` | Thai-only industry page. **No `hreflang` at all** — asserts the negative case. |
| `_spike-next/_verify/urls.test.ts` | Asserts the emitted file tree matches the live URL set exactly. |
| `_spike-next/_verify/head.test.ts` | Asserts canonical / hreflang / og:locale per the bilingual rules. |

**Three pages, chosen to cover everything:** `/` is home-shell + the featured carousel + the `#need` selector; `showcase-buildnest` is portfolio-pages + a bilingual pair + the story stack + the hero skeleton; `web-clinic` is Thai-only with no twin, and carries the `design-preview` widget and a `FAQPage` JSON-LD. Between them they touch both stylesheet families, both `hreflang` cases, and every JSON-LD type on the site.

---

### Task 1: Scaffold, and answer the URL question first

Nothing else matters if the URLs cannot match. This task ends when the emitted tree is proven identical to the live URL set, or proven impossible.

**Files:**
- Create: `_spike-next/package.json`, `_spike-next/next.config.ts`, `_spike-next/tsconfig.json`, `_spike-next/.gitignore`
- Create: `_spike-next/app/layout.tsx`, `_spike-next/app/page.tsx`, `_spike-next/app/showcase-buildnest/page.tsx`, `_spike-next/app/web-clinic/page.tsx`
- Create: `_spike-next/_verify/urls.test.ts`
- Modify: `.gitignore` (repo root) — add `_spike-next/node_modules/` and `_spike-next/out/`

**Interfaces:**
- Consumes: nothing.
- Produces: `_spike-next/out/` — a static tree whose paths later tasks assert against. Route directory names are the URL slugs (`app/showcase-buildnest/page.tsx` → `/showcase-buildnest`).

- [ ] **Step 1: Capture the live URL set as the fixture to match**

Run from the repo root:

```bash
python3 - <<'PY' > /tmp/live-urls.txt
import re, io
s = io.open('sitemap.xml', encoding='utf-8').read()
for loc in sorted(re.findall(r'<loc>([^<]+)</loc>', s)):
    print(loc.replace('https://ph-akin.dev', '') or '/')
PY
wc -l /tmp/live-urls.txt
```

Expected: 84 lines, beginning with `/` and containing `/showcase-buildnest` and `/web-clinic`, none ending in `.html`.

- [ ] **Step 2: Write the failing URL-parity test**

Create `_spike-next/_verify/urls.test.ts`:

```ts
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readdirSync, statSync } from 'node:fs'
import { join, relative } from 'node:path'

const OUT = join(import.meta.dirname, '..', 'out')

/** Every .html file in out/, expressed as the URL GitHub Pages would serve it at. */
export function emittedUrls(dir = OUT, base = OUT): string[] {
  const urls: string[] = []
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry)
    if (statSync(full).isDirectory()) { urls.push(...emittedUrls(full, base)); continue }
    if (!entry.endsWith('.html')) continue
    const rel = relative(base, full).replace(/\\/g, '/')
    if (rel === 'index.html') { urls.push('/'); continue }
    urls.push('/' + rel.replace(/\/index\.html$/, '').replace(/\.html$/, ''))
  }
  return urls.sort()
}

test('every emitted URL is extensionless and has no /index suffix', () => {
  const urls = emittedUrls()
  assert.ok(urls.length > 0, 'out/ is empty — did the build run?')
  for (const u of urls) {
    assert.doesNotMatch(u, /\.html$/, `${u} kept its extension`)
    assert.doesNotMatch(u, /\/index$/, `${u} came from <slug>/index.html, not <slug>.html`)
  }
})

test('the three spike routes are present at the URLs the live site uses', () => {
  const urls = emittedUrls()
  for (const want of ['/', '/showcase-buildnest', '/web-clinic']) {
    assert.ok(urls.includes(want), `missing ${want} — got ${JSON.stringify(urls)}`)
  }
})
```

Note `import.meta.dirname`, not `__dirname`: `package.json` sets `"type": "module"` in Step 4,
so the CommonJS globals do not exist.

- [ ] **Step 3: Run it to confirm it fails**

```bash
cd next && node --import tsx --test _verify/urls.test.ts
```

Expected: FAIL — `out/` does not exist yet (`ENOENT: no such file or directory`).
If it instead reports 0 tests, the glob matched nothing and you have proved nothing;
check the path before continuing.

- [ ] **Step 4: Scaffold the app**

`_spike-next/package.json`:

```json
{
  "name": "ph-akin-next",
  "private": true,
  "type": "module",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "verify": "node --import tsx --test _verify/*.test.ts"
  },
  "dependencies": { "next": "^15.0.0", "react": "^19.0.0", "react-dom": "^19.0.0" },
  "devDependencies": {
    "@types/node": "^22.0.0", "@types/react": "^19.0.0",
    "tailwindcss": "^4.0.0", "@tailwindcss/postcss": "^4.0.0",
    "typescript": "^5.6.0", "tsx": "^4.19.0"
  }
}
```

`_spike-next/next.config.ts` — **`trailingSlash: false` is the whole hypothesis**:

```ts
import type { NextConfig } from 'next'

const config: NextConfig = {
  output: 'export',
  // GitHub Pages resolves /foo -> foo.html. With trailingSlash:false Next 15 emits
  // out/foo.html rather than out/foo/index.html, which is the same shape the hand-written
  // site ships today. If this proves false, Task 1 fails and the migration needs a
  // different answer before anything else is written.
  trailingSlash: false,
  images: { unoptimized: true },  // no image optimiser exists under `export`
}
export default config
```

`_spike-next/.gitignore`:

```
node_modules/
out/
._spike-next/
```

`_spike-next/tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022", "lib": ["dom", "dom.iterable", "ES2022"],
    "strict": true, "noEmit": true, "esModuleInterop": true,
    "module": "esnext", "moduleResolution": "bundler",
    "jsx": "preserve", "incremental": true,
    "paths": { "@/*": ["./*"] },
    "plugins": [{ "name": "next" }]
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", "._spike-next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
```

- [ ] **Step 5: Add the three pages as stubs**

`_spike-next/app/layout.tsx` — note `lang` is deliberately not set here; each page owns it:

```tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return children as React.ReactElement
}
```

`_spike-next/app/page.tsx`:

```tsx
export default function Home() { return <main><h1>หน้าแรก</h1></main> }
```

`_spike-next/app/showcase-buildnest/page.tsx`:

```tsx
export default function Page() { return <main><h1>BuildNest</h1></main> }
```

`_spike-next/app/web-clinic/page.tsx`:

```tsx
export default function Page() { return <main><h1>รับทำเว็บคลินิก</h1></main> }
```

- [ ] **Step 6: Install and build**

```bash
cd next && npm install && npm run build
```

Expected: build succeeds and `_spike-next/out/` exists.

- [ ] **Step 7: Read the emitted tree — this is the answer**

```bash
cd next && find out -name '*.html' | sort
```

Expected if the hypothesis holds:

```
out/404.html
out/index.html
out/showcase-buildnest.html
out/web-clinic.html
```

**If instead you see `out/showcase-buildnest/index.html`,** `trailingSlash: false` did not do what this plan assumed. Do not work around it by renaming files in a postbuild script — that is a second source of truth for 84 URLs. Stop, record what Next actually emitted, and re-plan Task 1. This is the outcome the spike exists to discover cheaply.

- [ ] **Step 8: Run the parity test**

```bash
cd next && npm run verify
```

Expected: PASS — 2/2. The emitted set is `/`, `/404`, `/showcase-buildnest`, `/web-clinic`:
every entry extensionless and none ending in `/index`, matching the shape of
`/tmp/live-urls.txt`.

- [ ] **Step 9: Commit**

```bash
cd /Users/chawanpunya/Documents/portfolio
git add next .gitignore
git commit -m "spike: Next.js scaffold, URL parity proven on three routes

output:'export' with trailingSlash:false emits out/<slug>.html, which is the
same shape GitHub Pages already serves the hand-written site at. 84 indexed
extensionless URLs survive the migration."
```

---

### Task 2: The bilingual head, including the negative case

**Files:**
- Create: `_spike-next/lib/site.ts`
- Create: `_spike-next/app/showcase-buildnest-en/page.tsx`
- Create: `_spike-next/_verify/head.test.ts`
- Modify: `_spike-next/app/page.tsx`, `_spike-next/app/showcase-buildnest/page.tsx`, `_spike-next/app/web-clinic/page.tsx`

**Interfaces:**
- Consumes: the route tree from Task 1.
- Produces: `SITE: string`, `type Lang = 'th' | 'en'`, `headFor(slug: string, lang: Lang, opts: { paired: boolean }): Metadata` — every later page in every later phase builds its `<head>` through this one function.

- [ ] **Step 1: Write the failing head test**

Create `_spike-next/_verify/head.test.ts`:

```ts
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { join } from 'node:path'

const OUT = join(import.meta.dirname, '..', 'out')
const read = (f: string) => readFileSync(join(OUT, f), 'utf8')

test('a paired Thai page carries the full hreflang trio with x-default on Thai', () => {
  const html = read('showcase-buildnest.html')
  assert.match(html, /<link rel="canonical" href="https:\/\/ph-akin\.dev\/showcase-buildnest"/)
  assert.match(html, /hreflang="th" href="https:\/\/ph-akin\.dev\/showcase-buildnest"/)
  assert.match(html, /hreflang="en" href="https:\/\/ph-akin\.dev\/showcase-buildnest-en"/)
  assert.match(html, /hreflang="x-default" href="https:\/\/ph-akin\.dev\/showcase-buildnest"/)
  assert.match(html, /<html lang="th"/)
  assert.match(html, /property="og:locale" content="th_TH"/)
})

test('the English half self-canonicals and keeps x-default on Thai', () => {
  const html = read('showcase-buildnest-en.html')
  assert.match(html, /<link rel="canonical" href="https:\/\/ph-akin\.dev\/showcase-buildnest-en"/)
  assert.match(html, /hreflang="x-default" href="https:\/\/ph-akin\.dev\/showcase-buildnest"/)
  assert.match(html, /<html lang="en"/)
  assert.match(html, /property="og:locale" content="en_US"/)
})

test('a Thai-only industry page carries NO hreflang at all', () => {
  const html = read('web-clinic.html')
  assert.match(html, /<link rel="canonical" href="https:\/\/ph-akin\.dev\/web-clinic"/)
  assert.doesNotMatch(html, /hreflang/)
})

test('the homepage canonical is the bare origin', () => {
  assert.match(read('index.html'), /<link rel="canonical" href="https:\/\/ph-akin\.dev\/"/)
})
```

- [ ] **Step 2: Run it to confirm it fails**

```bash
cd next && npm run verify
```

Expected: FAIL — four failures, all `AssertionError` on a missing `canonical`.

- [ ] **Step 3: Implement the URL rules in one place**

Create `_spike-next/lib/site.ts`:

```ts
import type { Metadata } from 'next'

export const SITE = 'https://ph-akin.dev'
export type Lang = 'th' | 'en'

/** '/' for the homepage, '/slug' otherwise. Never an extension. */
export function urlFor(slug: string): string {
  return slug === '' ? `${SITE}/` : `${SITE}/${slug}`
}

/**
 * Thai is the site default, so x-default always points at the Thai URL.
 * `paired: false` is the 8 web-* industry pages and the 15 demo pages: they are
 * Thai-only by design and must carry no hreflang links whatsoever.
 */
export function headFor(
  slug: string,
  lang: Lang,
  opts: { paired: boolean },
): Metadata {
  const thaiSlug = slug.replace(/-en$/, '')
  const enSlug = thaiSlug === '' ? 'index-en' : `${thaiSlug}-en`
  const self = urlFor(slug)

  return {
    metadataBase: new URL(SITE),
    alternates: {
      canonical: self,
      ...(opts.paired
        ? {
            languages: {
              th: urlFor(thaiSlug),
              en: urlFor(enSlug),
              'x-default': urlFor(thaiSlug),
            },
          }
        : {}),
    },
    openGraph: {
      url: self,
      locale: lang === 'th' ? 'th_TH' : 'en_US',
      siteName: 'Phakin Chawanpunya Portfolio',
    },
    robots: { index: true, follow: true },
  }
}
```

- [ ] **Step 4: Wire it into all four pages**

`_spike-next/app/showcase-buildnest/page.tsx`:

```tsx
import type { Metadata } from 'next'
import { headFor } from '@/lib/site'

export const metadata: Metadata = headFor('showcase-buildnest', 'th', { paired: true })

export default function Page() {
  return (
    <html lang="th">
      <body><main><h1>BuildNest</h1></main></body>
    </html>
  )
}
```

`_spike-next/app/showcase-buildnest-en/page.tsx`:

```tsx
import type { Metadata } from 'next'
import { headFor } from '@/lib/site'

export const metadata: Metadata = headFor('showcase-buildnest-en', 'en', { paired: true })

export default function Page() {
  return (
    <html lang="en">
      <body><main><h1>BuildNest</h1></main></body>
    </html>
  )
}
```

`_spike-next/app/web-clinic/page.tsx` — the negative case:

```tsx
import type { Metadata } from 'next'
import { headFor } from '@/lib/site'

export const metadata: Metadata = headFor('web-clinic', 'th', { paired: false })

export default function Page() {
  return (
    <html lang="th">
      <body><main><h1>รับทำเว็บคลินิก</h1></main></body>
    </html>
  )
}
```

`_spike-next/app/page.tsx`:

```tsx
import type { Metadata } from 'next'
import { headFor } from '@/lib/site'

export const metadata: Metadata = headFor('', 'th', { paired: true })

export default function Home() {
  return (
    <html lang="th">
      <body><main><h1>หน้าแรก</h1></main></body>
    </html>
  )
}
```

Note: App Router normally owns `<html>` in `layout.tsx`. Because `lang` differs per page and `layout.tsx` is shared, each page renders its own — which is why Task 1's layout returns `children` untouched.

- [ ] **Step 5: Rebuild and run the test**

```bash
cd next && npm run build && npm run verify
```

Expected: PASS — 4/4.

- [ ] **Step 6: Commit**

```bash
git add next
git commit -m "spike: bilingual head rules, including the Thai-only negative case

hreflang trio with x-default on Thai for paired pages, self-canonical on both
halves, and no hreflang at all on web-clinic. One headFor() so the rule cannot
drift per page the way 21 hand-written pairs can."
```

---

### Task 3: Thai typography and CLS under Tailwind

The two things most likely to regress silently. Both are measured, not eyeballed.

**Files:**
- Create: `_spike-next/app/globals.css`, `_spike-next/lib/fonts.ts`
- Modify: `_spike-next/app/layout.tsx`, `_spike-next/app/showcase-buildnest/page.tsx`

**Interfaces:**
- Consumes: `headFor()` from Task 2.
- Produces: `display`, `sansTh` — `next/font/google` objects whose `.variable` class names later phases attach to `<html>`.

- [ ] **Step 1: Write the failing CLS + collision test**

Create `_spike-next/_verify/type.test.ts`:

```ts
import { test } from 'node:test'
import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import { join } from 'node:path'

const html = readFileSync(join(import.meta.dirname, '..', 'out', 'showcase-buildnest.html'), 'utf8')

test('fonts are self-hosted with font-display: optional, never swap', () => {
  assert.match(html, /font-display:\s*optional/)
  assert.doesNotMatch(html, /font-display:\s*swap/)
})

test('the Bai Jamjuree display token reaches the page', () => {
  assert.match(html, /Bai_Jamjuree|--font-display/)
})

test('no Google Fonts stylesheet is requested — next/font self-hosts', () => {
  assert.doesNotMatch(html, /fonts\.googleapis\.com/)
})
```

- [ ] **Step 2: Run it to confirm it fails**

```bash
cd next && npm run build && npm run verify
```

Expected: FAIL on all three — no font is configured yet.

- [ ] **Step 3: Configure the faces**

Create `_spike-next/lib/fonts.ts`:

```ts
import { Bai_Jamjuree, Inter, Noto_Sans_Thai } from 'next/font/google'

// display: 'optional' matches the hand-written site exactly. 'swap' reflowed the h1,
// the nav logo and the hero buttons on lumi-clinic and measured CLS 0.011-0.015.
export const display = Bai_Jamjuree({
  subsets: ['latin', 'thai'], weight: ['600', '700'],
  display: 'optional', variable: '--font-display',
})

export const bodyLatin = Inter({
  subsets: ['latin'], display: 'optional', variable: '--font-body-latin',
})

export const bodyThai = Noto_Sans_Thai({
  subsets: ['thai'], display: 'optional', variable: '--font-body-thai',
})
```

- [ ] **Step 4: Port the tokens and the Thai spacing fix**

Create `_spike-next/app/globals.css`:

```css
@import "tailwindcss";

@theme {
  --color-accent: #5274f8;
  --color-accent-dark: #3651d4;
  --font-display: var(--font-display), "Noto Sans Thai", sans-serif;
  --font-body: var(--font-body-latin), var(--font-body-thai), Arial, sans-serif;
}

html, body { overflow-x: hidden; }

h1, h2, h3 { font-family: var(--font-display); }

/*
 * Load-bearing, not decoration. .eyebrow had no bottom margin and the h2 beneath it
 * runs at line-height 1.1 -- fine for Latin, but Thai upper vowels and tone marks are
 * drawn above the line box, so "สิ่ง" and "ที่" collided with the eyebrow. Measured at
 * gap: 0px on every .section-heading sitewide before the fix. Tailwind's type scale is
 * Latin-tuned and will reintroduce this if the rule is dropped.
 */
.section-heading .eyebrow { margin-bottom: 12px; }
```

- [ ] **Step 5: Attach the variables**

`_spike-next/app/layout.tsx`:

```tsx
import './globals.css'
import { display, bodyLatin, bodyThai } from '@/lib/fonts'

export const fontClass = `${display.variable} ${bodyLatin.variable} ${bodyThai.variable}`

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return children as React.ReactElement
}
```

and in `_spike-next/app/showcase-buildnest/page.tsx`, change the opening tag to:

```tsx
    <html lang="th" className={fontClass}>
```

importing `fontClass` from `../layout`.

- [ ] **Step 6: Rebuild and run**

```bash
cd next && npm run build && npm run verify
```

Expected: PASS — 3/3 on type, 4/4 still passing on head.

- [ ] **Step 7: Measure the Thai collision in a real browser**

Serve `_spike-next/out` and, at 1440 × 900 with the tab **foregrounded**, run against a `.section-heading`:

```js
(() => {
  const eb = document.querySelector('.section-heading .eyebrow')
  const h2 = eb?.parentElement?.querySelector('h2')
  if (!eb || !h2) return 'no .section-heading on this page yet — add one before trusting this'
  const a = eb.getBoundingClientRect(), b = h2.getBoundingClientRect()
  return { gapPx: +(b.top - a.bottom).toFixed(1) }
})()
```

Expected: `gapPx` ≥ 12. A gap of 0 means the rule was dropped or out-specified.

- [ ] **Step 8: Commit**

```bash
git add next
git commit -m "spike: Thai type and font-display:optional under Tailwind

next/font self-hosts, so the Google Fonts request disappears; display:'optional'
is pinned explicitly because swap measured CLS 0.011-0.015 on lumi-clinic. The
12px .eyebrow margin is ported with the reason attached -- Thai tone marks
collide with the line above at line-height 1.1 without it."
```

---

### Task 4: Lighthouse, mobile overflow, and the View Transitions answer

The task that decides whether the spike is a green light.

**Files:**
- Create: `_spike-next/_verify/README.md` (records the measured numbers — this is the spike's actual deliverable)
- Modify: `_spike-next/app/globals.css`

**Interfaces:**
- Consumes: everything from Tasks 1–3.
- Produces: a go / no-go recommendation with numbers attached.

- [ ] **Step 1: Build and serve the export the way GitHub Pages will**

```bash
cd next && npm run build
cd out && python3 ../../_tools/serve.py 8124
```

`_tools/serve.py` mirrors the GitHub Pages extensionless fallback and serves `404.html` on a miss, which `python3 -m http.server` does not.

- [ ] **Step 2: Run Lighthouse on all three pages, mobile and desktop**

```bash
for p in "" showcase-buildnest web-clinic; do
  npx -y lighthouse "http://localhost:8124/$p" --quiet --chrome-flags="--headless" \
    --output=json --output-path="/tmp/lh-next-${p:-home}-mobile.json"
  npx -y lighthouse "http://localhost:8124/$p" --preset=desktop --quiet --chrome-flags="--headless" \
    --output=json --output-path="/tmp/lh-next-${p:-home}-desktop.json"
done
python3 - <<'PY'
import json, glob
for f in sorted(glob.glob('/tmp/lh-next-*.json')):
    d = json.load(open(f))
    s = {k: round(v['score']*100) for k, v in d['categories'].items() if v.get('score') is not None}
    cls = d['audits']['cumulative-layout-shift']['numericValue']
    print('%-44s %s  CLS=%.4f' % (f.split('/')[-1], s, cls))
PY
```

Expected: Accessibility 100, SEO 100, Performance 100, CLS 0.000 on all six runs. Best Practices will **not** be 77 here — Clarity is not wired into the spike — so it should be 100; a lower number is a real regression introduced by Next.

- [ ] **Step 3: Check mobile overflow at 375 × 812**

Embed each page in a 375 × 812 `<iframe>` on a blank page — its own media queries evaluate against the iframe's viewport — and run against `iframe.contentDocument` / `contentWindow`:

```js
({ canScrollX: (function(){ const d = document.documentElement; d.scrollLeft = 50; const s = d.scrollLeft; d.scrollLeft = 0; return s > 0 })(),
   bw: document.body.scrollWidth, cw: document.documentElement.clientWidth })
```

Expected: `canScrollX: false` on all three.

- [ ] **Step 4: Determine what happened to View Transitions**

Add to `_spike-next/app/globals.css`:

```css
@view-transition { navigation: auto; }
```

Rebuild, then navigate between two pages **by clicking a link** and record whether the cross-fade occurs.

```js
// Does this browser/app combination even reach the cross-document path?
({ supported: 'startViewTransition' in document,
   rule: [...document.styleSheets].flatMap(s => { try { return [...s.cssRules] } catch { return [] } })
           .some(r => r.constructor.name === 'CSSViewTransitionRule') })
```

**The expected result is that it does not cross-fade**, because `@view-transition { navigation: auto }` applies to cross-document navigation only and App Router intercepts `<a>` clicks into client-side routing. Record which of these the spike found:

1. It still cross-fades → nothing to do, note it and move on.
2. It does not → the honest options are (a) accept the loss, (b) opt the links out of client routing so navigations stay cross-document, or (c) reimplement with `document.startViewTransition()` on route change. **Do not pick one here.** Record the finding; it belongs to the Phase 1 plan.

- [ ] **Step 5: Write down what was actually measured**

Create `_spike-next/_verify/README.md` with the real numbers from Steps 2–4 — not a template. It must state, for each of the three pages: the six Lighthouse category scores, CLS, `canScrollX`, and the View Transitions outcome; plus whether `out/` emitted `<slug>.html` or `<slug>/index.html`.

- [ ] **Step 6: Commit**

```bash
git add next
git commit -m "spike: measured Lighthouse, CLS, mobile overflow and View Transitions

Numbers in _spike-next/_verify/README.md. This is the spike's deliverable: the
go/no-go for migrating 84 pages rests on these six Lighthouse runs and the
View Transitions result, not on an expectation that Next behaves like the
hand-written site."
```

---

## What this plan deliberately does NOT cover

Per the writing-plans scope check, the full migration spans several independent subsystems. Each needs its own plan, written **after** Phase 0 reports:

| Phase | Subsystem | Notes it must start from |
|---|---|---|
| 1 | Content model + the 30 showcase pages | `_content/project-copy.json` already exists and is verified by `_tools/check-copy.py`. Extend it rather than inventing a second source. |
| 2 | The 12 home-shell pages | Two stylesheet families must stay unmixed — nine colliding selectors. |
| 3 | The 8 industry pages + the `design-preview` widget | One `design-preview-<key>.json` per industry, 57 mockup pages, nine block types. A tenth block type is a code change, not data. |
| 4 | Site search + `sitemap.xml` + `search-index.json` generation | All three become build outputs, which removes the "hand-maintained and nothing tells you" failure mode. |
| — | The 15 demo pages | **Never migrated.** They move to `public/` byte-for-byte. |

**Not in any phase:** the resume backend claims. That is a truth problem, not a migration problem, and is tracked separately in CLAUDE.md.

## Exit criteria

Phase 0 succeeds if all of the following are true, each with a number recorded in `_spike-next/_verify/README.md`:

- [ ] `out/` emits `<slug>.html`, matching the live extensionless URL shape
- [ ] `hreflang` trio + self-canonical correct on the pair; **zero** `hreflang` on `web-clinic`
- [ ] no `fonts.googleapis.com` request; `font-display: optional` present, `swap` absent
- [ ] Lighthouse Accessibility 100, SEO 100, Performance 100 on all three pages, mobile and desktop
- [ ] CLS 0.000 on all six runs
- [ ] `canScrollX: false` at 375 × 812 on all three
- [ ] the View Transitions outcome is recorded, whichever way it went

If the first criterion fails, **stop and re-plan** — every other result is moot if 84 indexed URLs cannot be reproduced.
