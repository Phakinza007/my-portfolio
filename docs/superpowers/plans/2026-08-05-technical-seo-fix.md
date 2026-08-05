# Technical SEO Fix Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Fix the site-wide canonical-domain bug that is very likely preventing Google from indexing the site at all, then add the baseline technical-SEO pieces (robots.txt, richer structured data) needed for it to actually rank.

**Architecture:** No build step — every fix is a direct text edit across the existing static HTML files, `sitemap.xml`, and `CLAUDE.md`, plus one new file (`robots.txt`). The core problem: every page's `<link rel="canonical">`, `og:url`, `og:image`, `twitter:image`, and JSON-LD `url` field points at `https://ph-akin.dev/...`, but that domain does not resolve (confirmed: `https://ph-akin.dev/` fails with a TLS/SNI error, no `CNAME` file exists in the repo). The site is actually live and working at `https://phakinza007.github.io/my-portfolio/`. When a page's canonical URL points at a domain that doesn't serve any content, Google treats the canonical as broken and generally won't index the page under either URL — this is almost certainly why the site isn't showing up in search. Per the user's decision, the fix is to repoint every reference at the real, working GitHub Pages URL rather than trying to stand up the custom domain.

**Tech Stack:** Plain HTML/XML, no dependencies. The domain fix is applied via a one-off Python find-and-replace script (run once, not committed — this is a data migration, not application code). Verification uses `grep`, `python3 -c` for XML/JSON validation, and `npx lighthouse` (already used successfully earlier in this project for the showcase-pages work).

## Global Constraints

- The corrected canonical domain is `https://phakinza007.github.io/my-portfolio` (no trailing slash on the base — each task shows the exact trailing-slash handling per URL type).
- Do **not** add a `CNAME` file — that would make GitHub Pages attempt to serve the (currently unconfigured) custom domain and could break the site. This is a deliberate decision, not an oversight.
- Every asset/script reference must stay **relative** (`assets/...`, not `/assets/...`) — the site lives at a subpath (`/my-portfolio/`), so an absolute path silently breaks. This convention already exists (documented in `CLAUDE.md`'s Analytics section) — don't regress it while editing.
- No fabricated content: don't invent a Google Search Console verification token or paste in a placeholder — that step is manual (Task 4 documents exactly what to do).
- After this plan, zero occurrences of the string `ph-akin.dev` should remain anywhere in the repository (verified in Task 4).

---

### Task 1: Fix the broken canonical domain sitewide

**Files:**
- Modify: all 33 `*.html` files in the repo root that reference `ph-akin.dev` (full list: `404.html`, `DRIP.html`, `InternTrack.html`, `LaunchLedger.html`, `MuseRoom.html`, `PulseBoard.html`, `aesthetic-booking.html`, `case-study-habitquest.html`, `case-study-interntrack.html`, `case-study-launchledger.html`, `case-study-pulseboard.html`, `coffee-landing.html`, `construction-landing.html`, `dental-clinic.html`, `gym-landing.html`, `index.html`, `lumi-clinic.html`, `resume.html`, `showcase-bookease.html`, `showcase-buildnest.html`, `showcase-dental-clinic.html`, `showcase-elasticshop-gaming.html`, `showcase-elevate-commerce.html`, `showcase-habitquest.html`, `showcase-iron-republic.html`, `showcase-lumi-clinic.html`, `showcase-museroom.html`, `showcase-noir-coffee.html`, `showcase-ratri-restaurant.html`, `showcase-solarpeak.html`, `showcase-velve-aesthetics.html`, `solar-landing.html`, `spa-retreat.html`)
- Modify: `sitemap.xml` (all 34 `<loc>` entries)
- Modify: `CLAUDE.md:12` (Project Overview URL) and `CLAUDE.md:138-143` (Analytics section's now-stale explanation)

**Interfaces:** None — this is a content/URL migration, no new code interfaces.

- [ ] **Step 1: Write and run the domain-fix script**

Create this file at `/tmp/fix_domain.py` (temporary — not committed to the repo):

```python
#!/usr/bin/env python3
import re, os

ROOT = "/Users/chawanpunya/Documents/portfolio"
OLD_BASE = "https://ph-akin.dev"
NEW_BASE = "https://phakinza007.github.io/my-portfolio"

changed = []
for fname in os.listdir(ROOT):
    if not (fname.endswith(".html") or fname == "sitemap.xml"):
        continue
    path = os.path.join(ROOT, fname)
    text = open(path, encoding="utf-8").read()
    if OLD_BASE not in text and "ph-akin.dev/" not in text:
        continue
    original = text
    # 1. https://ph-akin.dev/... -> https://phakinza007.github.io/my-portfolio/...
    text = text.replace(OLD_BASE, NEW_BASE)
    # 2. bare decorative "ph-akin.dev/xxx" spans (showcase browser-chrome URL bar,
    #    no https:// prefix) -> "phakinza007.github.io/my-portfolio/xxx"
    text = re.sub(r'(?<!https://)ph-akin\.dev/', 'phakinza007.github.io/my-portfolio/', text)
    if text != original:
        open(path, "w", encoding="utf-8").write(text)
        changed.append(fname)

print(f"Updated {len(changed)} files:")
for f in sorted(changed):
    print(" ", f)
```

Run it:

```bash
python3 /tmp/fix_domain.py
```

Expected output: `Updated 34 files:` followed by the file list (33 HTML files + `sitemap.xml`).

- [ ] **Step 2: Verify the replacement is correct on one representative file**

```bash
grep -n "phakinza007.github.io" index.html | head -5
```

Expected: canonical link, `og:url`, `og:image`, `twitter:image`, and the JSON-LD `"url"` field all now show `https://phakinza007.github.io/my-portfolio/...` instead of `https://ph-akin.dev/...`.

Also check the homepage's root URL specifically got the trailing slash preserved correctly (it must resolve to `index.html` under GitHub Pages' directory-index behavior):

```bash
grep -n 'canonical" href="https://phakinza007.github.io/my-portfolio/"' index.html
```

Expected: one match (trailing slash intact, nothing appended after it).

- [ ] **Step 3: Verify a showcase page's decorative browser-chrome URL text also updated**

```bash
grep -n 'class="browser-url"' showcase-buildnest.html
```

Expected: `<span class="browser-url">phakinza007.github.io/my-portfolio/construction-landing.html</span>` — the bare (non-`https://`) pattern was also caught.

Note: `showcase-habitquest.html` is expected to show **no** match here — its browser-url bar shows `habitquest-pi.vercel.app` (the real external live URL), which was never a `ph-akin.dev` reference and correctly wasn't touched.

- [ ] **Step 4: Verify sitemap.xml is still well-formed XML and every URL updated**

```bash
python3 -c "
import xml.dom.minidom as m
m.parse('sitemap.xml')
print('valid XML')
"
grep -c "https://phakinza007.github.io/my-portfolio" sitemap.xml
grep -c "ph-akin.dev" sitemap.xml
```

Expected: `valid XML`, then `34` (one per `<loc>`), then `0` (no leftover old-domain references).

- [ ] **Step 5: Update CLAUDE.md's Project Overview URL**

Find (exact current lines 9-12):
```markdown
## Project Overview

Personal frontend portfolio hosted on GitHub Pages.  
URL: https://ph-akin.dev/
```

Replace with:
```markdown
## Project Overview

Personal frontend portfolio hosted on GitHub Pages.  
URL: https://phakinza007.github.io/my-portfolio/
```

- [ ] **Step 6: Update CLAUDE.md's Analytics section — the domain mismatch it warned about is now fixed**

Find (exact current lines 138-143):
```markdown
- Project ID lives at the top of `assets/analytics.js` (`CLARITY_PROJECT_ID` const)
- Every `.html` page must have `<script src="assets/analytics.js" defer></script>` right
  before `</head>` — **use the relative path**, not `/assets/analytics.js`. The site currently
  has no `CNAME` file, so it's actually served at `https://phakinza007.github.io/my-portfolio/`
  (a subpath), not at the `https://ph-akin.dev/` root this doc otherwise assumes. An
  absolute `/assets/...` path breaks under that subpath.
```

Replace with:
```markdown
- Project ID lives at the top of `assets/analytics.js` (`CLARITY_PROJECT_ID` const)
- Every `.html` page must have `<script src="assets/analytics.js" defer></script>` right
  before `</head>` — **use the relative path**, not `/assets/analytics.js`. The site has no
  `CNAME` file (deliberately — see Task 1 of
  `docs/superpowers/plans/2026-08-05-technical-seo-fix.md`) and is served at
  `https://phakinza007.github.io/my-portfolio/` (a subpath). An absolute `/assets/...` path
  breaks under that subpath — this applies to every relative reference on every page, not
  just `analytics.js`.
```

- [ ] **Step 7: Delete the temporary migration script**

```bash
rm /tmp/fix_domain.py
```

- [ ] **Step 8: Commit**

```bash
git add -A -- '*.html' sitemap.xml CLAUDE.md
git commit -m "$(cat <<'EOF'
Fix broken canonical domain sitewide (ph-akin.dev -> github.io)

https://ph-akin.dev doesn't resolve (TLS/SNI error, no CNAME file
configured) — every page's canonical link, og:url, og:image,
twitter:image, and JSON-LD url pointed at a dead domain, which is
almost certainly why the site wasn't getting indexed by Google: a
canonical URL that serves nothing tells crawlers not to trust either
copy. Repoints everything at the real, working GitHub Pages URL
(https://phakinza007.github.io/my-portfolio/) instead of standing up
the custom domain, per explicit decision — ph-akin.dev was never
actually configured to serve this site.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: Add robots.txt

**Files:**
- Create: `robots.txt`
- Modify: `CLAUDE.md:117` (SEO & Meta section — mention robots.txt alongside the existing sitemap line)

**Depends on:** Task 1 (uses the corrected domain in the `Sitemap:` directive).

**Interfaces:** None.

- [ ] **Step 1: Create robots.txt**

```
User-agent: *
Allow: /

Sitemap: https://phakinza007.github.io/my-portfolio/sitemap.xml
```

- [ ] **Step 2: Update CLAUDE.md's SEO & Meta section**

Find (exact current lines 110-117):
```markdown
## SEO & Meta

- Theme color: `#5274f8`
- OG image: `assets/social-preview.png` (1200×630)
- Canonical URL set on all pages
- `robots: index, follow`
- Twitter card: `summary_large_image`
- Sitemap: `sitemap.xml` (submit to Google Search Console manually)
```

Replace with:
```markdown
## SEO & Meta

- Theme color: `#5274f8`
- OG image: `assets/social-preview.png` (1200×630)
- Canonical URL set on all pages — must be `https://phakinza007.github.io/my-portfolio/...`
  (see `docs/superpowers/plans/2026-08-05-technical-seo-fix.md` — ph-akin.dev does not resolve)
- `robots: index, follow`
- Twitter card: `summary_large_image`
- Sitemap: `sitemap.xml`, referenced from `robots.txt`
- `robots.txt` at the repo root allows all crawlers and points at the sitemap
```

- [ ] **Step 3: Verify robots.txt is valid and reachable locally**

```bash
python3 -m http.server 8123 >/tmp/portfolio-http.log 2>&1 &
sleep 1
curl -s http://localhost:8123/robots.txt
kill %1 2>/dev/null
```

Expected: prints the exact 4-line content from Step 1.

- [ ] **Step 4: Commit**

```bash
git add robots.txt CLAUDE.md
git commit -m "$(cat <<'EOF'
Add robots.txt pointing crawlers at the sitemap

No robots.txt existed before, so crawlers had no explicit pointer to
sitemap.xml and had to discover pages purely by following links.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: Enrich Person structured data

**Files:**
- Modify: `index.html` (the `application/ld+json` Person block's `sameAs` array)
- Modify: `resume.html` (the `application/ld+json` Person block's `sameAs` array)

**Depends on:** Task 1 (the JSON-LD `url` field in both files was already corrected to the new domain in Task 1 — this task only touches `sameAs`).

**Interfaces:** None.

- [ ] **Step 1: Add LinkedIn and the real Fastwork profile to index.html's sameAs**

Find (exact current text in `index.html`'s JSON-LD block):
```json
    "sameAs": ["https://github.com/Phakinza007", "https://www.instagram.com/phakinkinpa/"],
```

Replace with:
```json
    "sameAs": [
      "https://github.com/Phakinza007",
      "https://www.instagram.com/phakinkinpa/",
      "https://linkedin.com/in/phakin-chawanpunya",
      "https://fastwork.co/user/u106pl4r"
    ],
```

- [ ] **Step 2: Add the same two links to resume.html's sameAs**

Find (exact current text in `resume.html`'s JSON-LD block):
```json
      "sameAs": [
        "https://github.com/Phakinza007",
        "https://www.instagram.com/phakinkinpa/"
      ],
```

Replace with:
```json
      "sameAs": [
        "https://github.com/Phakinza007",
        "https://www.instagram.com/phakinkinpa/",
        "https://linkedin.com/in/phakin-chawanpunya",
        "https://fastwork.co/user/u106pl4r"
      ],
```

- [ ] **Step 3: Verify both JSON-LD blocks still parse as valid JSON**

```bash
python3 -c "
import re, json
for fname in ('index.html', 'resume.html'):
    html = open(fname, encoding='utf-8').read()
    m = re.search(r'<script type=\"application/ld\+json\">(.*?)</script>', html, re.S)
    data = json.loads(m.group(1))
    assert 'https://linkedin.com/in/phakin-chawanpunya' in data['sameAs']
    assert 'https://fastwork.co/user/u106pl4r' in data['sameAs']
    print(fname, 'OK —', len(data['sameAs']), 'sameAs links')
"
```

Expected: `index.html OK — 4 sameAs links` and `resume.html OK — 4 sameAs links`, no JSON parse errors.

- [ ] **Step 4: Commit**

```bash
git add index.html resume.html
git commit -m "$(cat <<'EOF'
Add LinkedIn and Fastwork profile to Person structured data

The Person JSON-LD sameAs array only listed GitHub and Instagram,
missing two identity signals already used elsewhere on the site
(Contact & Social table in CLAUDE.md, Fastwork CTAs throughout) —
more corroborating sameAs links help Google confirm this is the same
real person/entity across the web.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: Final verification, deploy, and manual Search Console setup

**Files:** None modified — verification only, plus a manual (non-code) checklist at the end.

**Depends on:** Tasks 1-3.

**Interfaces:** None.

- [ ] **Step 1: Confirm zero stale-domain references remain anywhere in the repo**

```bash
grep -rn "ph-akin\.dev" --exclude-dir=.git . | grep -v "docs/superpowers/plans/2026-08-05-technical-seo-fix.md"
```

Expected: no output. (The plan file itself is excluded from this check since it documents the fix by name — that's expected and fine.)

**Correction found during execution:** Task 1's file scan only covered `*.html` and `sitemap.xml`, missing four Markdown files that also referenced the dead domain — `README.md` (14 occurrences, public-facing on GitHub), `_docs/agent.md` and `_docs/RESUME.md` (internal reference docs), and critically `.claude/skills/portfolio-add-card/SKILL.md` (its sitemap-entry template, which would have injected `ph-akin.dev` into every *future* project card added via that skill). Fixed with the same `https://ph-akin.dev` → `https://phakinza007.github.io/my-portfolio` replacement, committed separately. If re-running this plan from scratch, broaden Task 1 Step 1's script to scan these paths too instead of discovering the gap here.

- [ ] **Step 2: Re-validate sitemap.xml**

```bash
python3 -c "import xml.dom.minidom as m; m.parse('sitemap.xml'); print('valid XML')"
grep -c "<loc>" sitemap.xml
```

Expected: `valid XML`, then `34`.

- [ ] **Step 3: Lighthouse SEO check on two representative pages**

```bash
python3 -m http.server 8123 >/tmp/portfolio-http.log 2>&1 &
sleep 1
npx --yes lighthouse http://localhost:8123/index.html \
  --only-categories=seo --output=json --output-path=/tmp/lh-index.json \
  --chrome-flags="--headless" --quiet
npx --yes lighthouse http://localhost:8123/showcase-buildnest.html \
  --only-categories=seo --output=json --output-path=/tmp/lh-showcase.json \
  --chrome-flags="--headless" --quiet
python3 -c "
import json
for f in ('/tmp/lh-index.json', '/tmp/lh-showcase.json'):
    d = json.load(open(f))
    print(f, round(d['categories']['seo']['score']*100))
"
kill %1 2>/dev/null
```

Expected: both print `100`.

- [ ] **Step 4: Push to origin**

```bash
git push origin main
```

- [ ] **Step 5: Confirm the live site now serves the corrected canonical**

```bash
curl -s https://phakinza007.github.io/my-portfolio/ | grep -o 'canonical" href="[^"]*"'
curl -s https://phakinza007.github.io/my-portfolio/robots.txt
```

Expected: the canonical line shows `https://phakinza007.github.io/my-portfolio/` (matching the URL that was actually just fetched — this is the whole fix, confirmed end-to-end), and `robots.txt` returns the 4-line content from Task 2. Note GitHub Pages can take 1-2 minutes to redeploy after a push — if `robots.txt` 404s immediately after pushing, wait a minute and retry before concluding something's wrong.

- [ ] **Step 6: Manual steps — hand these back to Phakin, don't attempt them as code**

These require an actual Google account and cannot be scripted or faked with a placeholder value:

1. Go to [Google Search Console](https://search.google.com/search-console) and add a property for `https://phakinza007.github.io/my-portfolio/` (use the "URL prefix" property type, not "Domain" — a Domain property needs DNS verification, which doesn't apply here since this isn't a custom domain).
2. Verify ownership via the **HTML tag** method: Search Console will give a `<meta name="google-site-verification" content="...">` tag. Add that exact tag inside `<head>` in `index.html` (and ideally every page, though the homepage alone is enough to verify the property), commit, push, then click "Verify" in Search Console.
3. Once verified, submit `sitemap.xml` under Search Console's "Sitemaps" section (`https://phakinza007.github.io/my-portfolio/sitemap.xml`).
4. Use "URL Inspection" on the homepage URL and click "Request Indexing" to prompt an initial crawl rather than waiting for Google to discover it organically.
5. Expect a delay of days to a few weeks before search results reflect this — that's normal and not a sign anything is still broken.
