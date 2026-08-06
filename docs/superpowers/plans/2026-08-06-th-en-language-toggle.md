# TH/EN Language Toggle Implementation Plan

> **For agentic workers:** Content-heavy plan — 19 pages need real Thai prose, not templated snippets. Per explicit user decision, this plan specifies the mechanism/structure completely (no placeholders there) and the per-page task list/scope, but the Thai body copy itself is composed at execution time rather than frozen in this document — same approach used successfully for the showcase-pages feature. Implement directly; do not hand off to subagent-driven-development or executing-plans.

**Goal:** Every page listed in Scope gets a Thai (`-th.html`) counterpart with reciprocal `hreflang`, reachable via a "TH | EN" nav link, per `docs/superpowers/specs/2026-08-06-th-en-language-toggle-design.md`.

**Architecture:** Paired static files, not a JS toggle. Each English page `X.html` gets a sibling `X-th.html` — same CSS/JS/assets (all paths relative, unaffected by the new filename), same structure, Thai body copy, `<html lang="th">`, and a reciprocal `hreflang` pair declared in both files' `<head>`.

**Tech Stack:** Plain HTML, no build step. Verification via `grep`/Python (hreflang reciprocity, XML validity) and `npx lighthouse` (same tools already used for the showcase-pages and SEO-fix work).

## Global Constraints

- Base domain for all absolute URLs: `https://ph-akin.dev/` — now correctly configured (CNAME + DNS point at GitHub Pages), confirmed live during this brainstorm.
- Every `-th.html` file: `<html lang="th">`, not `en`.
- `hreflang` must be reciprocal — if `X.html` declares `X-th.html` as its `th` alternate, `X-th.html` must declare `X.html` as its `en` alternate, and both declare `x-default` → the English version.
- `canonical` on each file points at itself (not at its counterpart).
- Internal links on a Thai page point at Thai counterparts where one exists in Scope; links to out-of-scope targets (13 project demo pages, GitHub, Fastwork, external apps) are unchanged in both languages.
- Thai copy is written fresh in a natural, conversational voice (matching the existing Services/Testimonials sections) — not literal translation.
- `index-th.html`'s Services and Testimonials sections reuse the *existing* Thai copy from `index.html` verbatim — don't rewrite already-good Thai text.
- Formspree form `action` endpoint is identical in both languages.
- `og:image`/`twitter:image` reuse the same asset as the English version.
- Lighthouse Accessibility/Best Practices/SEO must hold 100 on Thai pages, matching the English pages' existing bar.

---

## The `hreflang` head-block pattern (used by every task below)

Every English page gets this added to its `<head>` (exact values substitute per page):

```html
<link rel="alternate" hreflang="en" href="https://ph-akin.dev/<file>.html" />
<link rel="alternate" hreflang="th" href="https://ph-akin.dev/<file>-th.html" />
<link rel="alternate" hreflang="x-default" href="https://ph-akin.dev/<file>.html" />
```

Every `-th.html` page gets the identical three lines (same URLs — both files in a pair declare the same set of alternates, pointing at each other and at English as `x-default`).

Every `-th.html` page's `<html>` tag: `<html lang="th">`.

Every `-th.html` page's nav: the existing nav-link list gains one more entry, a plain link to the English counterpart, labeled `EN`. Every English page's nav gains a link to its Thai counterpart, labeled `TH`. (On `index.html`/`index-th.html`, which has both a desktop nav and a mobile drawer, both need the link. Case-study/showcase pages built on `portfolio-pages.css`'s `.nav-links` need just the one list.)

Every `-th.html` page's JSON-LD (only `index-th.html` and `resume-th.html` have one): `"url"` → the `-th.html` file's own URL, add `"inLanguage": "th"`, `"name"` unchanged.

---

### Task 1: `index.html` → `index-th.html` (reference implementation)

**Files:**
- Modify: `index.html` (add hreflang block to `<head>`, add "TH" nav link to desktop nav + mobile drawer)
- Create: `index-th.html`
- Modify: `sitemap.xml` (add `index-th.html` entry, priority `1.0`, changefreq `weekly` — matching `index.html`'s own entry)

**Interfaces:** None — establishes the pattern Tasks 2-7 follow.

- [ ] **Step 1:** Add the hreflang block (see pattern above, `<file>` = `index`) to `index.html`'s `<head>`, right after the existing `<link rel="canonical">` line.
- [ ] **Step 2:** Add a "TH" link to `index.html`'s desktop `.nav-links` list (after "Resume") and to the mobile `.nav-mobile-panel` (same position), each pointing at `index-th.html`.
- [ ] **Step 3:** Create `index-th.html` as a full copy of `index.html`, then:
  - Set `<html lang="th">`
  - Add the hreflang block (same three lines as Step 1 — both files in a pair carry identical alternate declarations)
  - Translate `<title>`, meta description, `og:title`/`og:description`, `twitter:title`/`twitter:description` into natural Thai; set `og:locale` to `th_TH`
  - Update `<link rel="canonical">` to `index-th.html`'s own URL
  - Update JSON-LD: `"url"` → `https://ph-akin.dev/index-th.html`, add `"inLanguage": "th"`
  - Translate the Hero, About, Experience, Selected Work (all 13 card titles/one-line descriptions — tags and hrefs stay as-is, pointing at the same showcase pages, since Selected Work links to showcase pages which get their own `-th` pair in Task 4-6, not `index-th.html`'s job to redirect those — wire Selected Work card links to `showcase-*-th.html` per the spec's internal-link rule), and Case Studies sections into natural Thai
  - Keep Services and Testimonials sections' Thai copy exactly as already written in `index.html` — do not retranslate
  - Change the desktop nav's "TH" link (added in Step 2's counterpart) to say "EN" and point at `index.html`; same for the mobile drawer
  - Translate the Contact section's labels/placeholders and the footer's nav labels; the Formspree form `action` attribute stays identical to `index.html`'s
- [ ] **Step 4:** Add `index-th.html` to `sitemap.xml`, same priority/changefreq as `index.html`.
- [ ] **Step 5: Verify.** Serve locally (`python3 -m http.server 8123`), open both `index.html` and `index-th.html`:
  - Confirm the TH/EN nav links swap correctly and land on the right page
  - Confirm every Selected Work card link points at a `showcase-*-th.html` URL on the Thai page
  - `curl -s http://localhost:8123/index-th.html | grep 'hreflang'` — expect 3 lines, all URLs correct
  - `python3 -c "import json,re; d=json.loads(re.search(r'application/ld\+json\">(.*?)</script>', open('index-th.html').read(), __import__('re').S).group(1)); assert d['inLanguage']=='th'; print('OK')"`
  - Mobile check at the environment's narrowest achievable width (375px target, ~500px floor observed previously): `canScrollX: false`
- [ ] **Step 6: Commit.**

```bash
git add index.html index-th.html sitemap.xml
git commit -m "$(cat <<'EOF'
Add Thai translation of the homepage (index-th.html)

First page of the TH/EN toggle rollout — establishes the paired-file
+ reciprocal-hreflang pattern the rest of the site follows. Services
and Testimonials sections reuse their existing Thai copy verbatim;
everything else translated fresh in the same conversational voice.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: `resume.html` → `resume-th.html`

**Files:**
- Modify: `resume.html` (hreflang block, nav TH link)
- Create: `resume-th.html`
- Modify: `sitemap.xml` (add entry, priority `0.9`, changefreq `monthly` — matching `resume.html`)

**Interfaces:** Consumes the hreflang pattern and JSON-LD pattern from Task 1.

- [ ] **Step 1:** Add hreflang block to `resume.html`'s `<head>` (`<file>` = `resume`), plus a "TH" link in its `.nav-links`.
- [ ] **Step 2:** Create `resume-th.html`: `<html lang="th">`, hreflang block, translated meta/OG/JSON-LD (`url` → `resume-th.html`'s own URL, `inLanguage: "th"`), full body translated to natural Thai (summary, skills, timeline, project strip — the project-strip's GitHub/case-study links stay pointed at whatever they already point at: GitHub repos unchanged, `case-study-*-th.html` for the 3 case-study links it contains per the internal-link rule), nav's link flipped to "EN" → `resume.html`.
- [ ] **Step 3:** Add `resume-th.html` to `sitemap.xml`.
- [ ] **Step 4: Verify** — same checks as Task 1 Step 5 (hreflang reciprocity, JSON-LD `inLanguage`, mobile overflow), plus confirm the 3 case-study project-strip links on `resume-th.html` point at `-th` versions.
- [ ] **Step 5: Commit** (same message pattern as Task 1, naming `resume-th.html`).

---

### Task 3: 4 case-study pages → `-th` counterparts

**Files:**
- Modify: `case-study-pulseboard.html`, `case-study-launchledger.html`, `case-study-interntrack.html`, `case-study-habitquest.html` (hreflang block + nav TH link, each)
- Create: `case-study-pulseboard-th.html`, `case-study-launchledger-th.html`, `case-study-interntrack-th.html`, `case-study-habitquest-th.html`
- Modify: `sitemap.xml` (4 new entries, priority `0.8`, changefreq `monthly`, matching the English originals)

**Interfaces:** Consumes Task 1's pattern. `case-study-habitquest-th.html` is linked from `showcase-habitquest-th.html` (Task 6) — must exist before Task 6's verification step.

- [ ] **Step 1:** For each of the 4 English case-study files: add its hreflang block, add a "TH" nav link.
- [ ] **Step 2:** For each, create the `-th` counterpart: `<html lang="th">`, hreflang block, translated meta/OG, translated body (problem/goal, design decisions, what-I-practiced, result band), "View live" button unchanged (points at the same demo page in both languages), the result band's cross-link to another case study updated to that case study's `-th` version, nav's link flipped to "EN".
- [ ] **Step 3:** Add all 4 `-th` entries to `sitemap.xml`.
- [ ] **Step 4: Verify** — hreflang reciprocity + JSON-LD (none of these pages have JSON-LD, so skip that check) + mobile overflow, for all 4 pairs.
- [ ] **Step 5: Commit** (one commit covering all 4 pairs).

---

### Task 4: Showcase pages batch 1 — BuildNest, Iron Republic, NOIR Coffee, Elevate Commerce

**Files:**
- Modify: `showcase-buildnest.html`, `showcase-iron-republic.html`, `showcase-noir-coffee.html`, `showcase-elevate-commerce.html` (hreflang block + nav TH link)
- Create: the 4 matching `-th.html` files
- Modify: `sitemap.xml` (4 entries, priority `0.75`, changefreq `monthly`)

**Interfaces:** Consumes Task 1's pattern. Each page's related-work section links to 3 other showcase pages — on the `-th` version, those must point at the other pages' `-th` counterparts (some of which land in Tasks 5-6, not yet created when this task runs — see note below).

**Note on cross-task related-work links:** Because showcase pages' related-work links span across this task's own batch and later batches (e.g. BuildNest's related work includes SolarPeak, created in Task 5), those links will 404 briefly until the batch containing the target lands. This resolves once Task 6 completes — call this out, don't treat it as a bug mid-rollout. Final verification (Task 7) confirms every link resolves once all batches are done.

- [ ] **Step 1:** For each of the 4 English showcase files: add its hreflang block, add "TH" nav link (next to "Resume" in the `.nav-links` list, same position as Task 1's index.html placement).
- [ ] **Step 2:** For each, create the `-th` counterpart: `<html lang="th">`, hreflang block, translated meta/OG, hero eyebrow/subtitle translated (the "View live site" button and browser-chrome URL bar text stay unchanged — they point at the demo page, which has no Thai counterpart), Overview/Highlights/Who-this-fits sections translated to natural Thai, the CTA band is *already* Thai in the English version — reuse verbatim (don't retranslate), related-work card titles unchanged but hrefs updated to the 3 targets' `-th.html` versions, nav's link flipped to "EN".
- [ ] **Step 3:** Add the 4 `-th` entries to `sitemap.xml`.
- [ ] **Step 4: Verify** — hreflang reciprocity + mobile overflow for all 4 pairs. Related-work link targets checked in Task 7 (not yet all created).
- [ ] **Step 5: Commit.**

---

### Task 5: Showcase pages batch 2 — Elasticshop Gaming, RATRI Restaurant, SolarPeak, BookEase

**Files:**
- Modify: `showcase-elasticshop-gaming.html`, `showcase-ratri-restaurant.html`, `showcase-solarpeak.html`, `showcase-bookease.html`
- Create: the 4 matching `-th.html` files
- Modify: `sitemap.xml` (4 entries, priority `0.75`)

**Interfaces:** Same as Task 4.

- [ ] **Step 1-3:** Same process as Task 4 Steps 1-3, applied to this batch's 4 pages.
- [ ] **Step 4: Verify** — same as Task 4 Step 4.
- [ ] **Step 5: Commit.**

---

### Task 6: Showcase pages batch 3 — MuseRoom, LUMI Clinic, BRIGHT Dental Clinic, VELVÉ Aesthetics, HabitQuest

**Files:**
- Modify: `showcase-museroom.html`, `showcase-lumi-clinic.html`, `showcase-dental-clinic.html`, `showcase-velve-aesthetics.html`, `showcase-habitquest.html`
- Create: the 5 matching `-th.html` files
- Modify: `sitemap.xml` (5 entries, priority `0.75`)

**Interfaces:** Same as Task 4. `showcase-habitquest-th.html` additionally links to `case-study-habitquest-th.html` (created in Task 3) — must exist by this point (it does, Task 3 runs first).

- [ ] **Step 1-3:** Same process as Task 4 Steps 1-3, applied to this batch's 5 pages. For `showcase-habitquest-th.html` specifically: its extra "Read the full case study" hero button points at `case-study-habitquest-th.html`; its "View live site" button stays pointed at the external `https://habitquest-pi.vercel.app/` URL unchanged.
- [ ] **Step 4: Verify** — same as Task 4 Step 4.
- [ ] **Step 5: Commit.**

---

### Task 7: Final verification across all 19 pairs

**Files:** None modified — verification only. Fix and commit separately if anything fails.

**Interfaces:** Consumes the output of Tasks 1-6 (all 44 files must exist).

- [ ] **Step 1: hreflang reciprocity check across every pair.**

```python
import re, os

PAIRS = [
    "index", "resume",
    "case-study-pulseboard", "case-study-launchledger",
    "case-study-interntrack", "case-study-habitquest",
    "showcase-buildnest", "showcase-iron-republic", "showcase-noir-coffee",
    "showcase-elevate-commerce", "showcase-elasticshop-gaming",
    "showcase-ratri-restaurant", "showcase-solarpeak", "showcase-bookease",
    "showcase-museroom", "showcase-lumi-clinic", "showcase-dental-clinic",
    "showcase-velve-aesthetics", "showcase-habitquest",
]
BASE = "https://ph-akin.dev/"
problems = []
for slug in PAIRS:
    for fname in (f"{slug}.html", f"{slug}-th.html"):
        text = open(fname, encoding="utf-8").read()
        alts = dict(re.findall(r'hreflang="(en|th|x-default)" href="([^"]+)"', text))
        if alts.get("en") != BASE + f"{slug}.html":
            problems.append(f"{fname}: en alternate wrong or missing")
        if alts.get("th") != BASE + f"{slug}-th.html":
            problems.append(f"{fname}: th alternate wrong or missing")
        if alts.get("x-default") != BASE + f"{slug}.html":
            problems.append(f"{fname}: x-default alternate wrong or missing")
        if fname.endswith("-th.html"):
            lang = re.search(r'<html lang="([^"]+)"', text)
            if not lang or lang.group(1) != "th":
                problems.append(f"{fname}: <html lang> is not 'th'")

print("\n".join(problems) if problems else f"All {len(PAIRS)*2} files: hreflang + lang correct.")
```

Expected: `All 38 files: hreflang + lang correct.`

- [ ] **Step 2: Every internal link inside a `-th.html` file that has a Thai counterpart in Scope actually points at it.**

```python
import re, os

SCOPE_SLUGS = {
    "index", "resume", "case-study-pulseboard", "case-study-launchledger",
    "case-study-interntrack", "case-study-habitquest",
    "showcase-buildnest", "showcase-iron-republic", "showcase-noir-coffee",
    "showcase-elevate-commerce", "showcase-elasticshop-gaming",
    "showcase-ratri-restaurant", "showcase-solarpeak", "showcase-bookease",
    "showcase-museroom", "showcase-lumi-clinic", "showcase-dental-clinic",
    "showcase-velve-aesthetics", "showcase-habitquest",
}
problems = []
for fname in os.listdir("."):
    if not fname.endswith("-th.html"):
        continue
    text = open(fname, encoding="utf-8").read()
    for href in re.findall(r'href="([a-zA-Z0-9_-]+)\.html', text):
        if href in SCOPE_SLUGS:
            problems.append(f"{fname}: links to {href}.html (English) instead of {href}-th.html")

print("\n".join(problems) if problems else "No English-language leaks found in any -th.html file's internal links.")
```

Expected: `No English-language leaks found in any -th.html file's internal links.` If this finds anything, it's a real bug — fix it and re-run.

- [ ] **Step 3: sitemap.xml has all 19 new entries and is still valid XML.**

```bash
python3 -c "import xml.dom.minidom as m; m.parse('sitemap.xml'); print('valid XML')"
grep -c "<loc>" sitemap.xml
```

Expected: `valid XML`, then `53` (34 existing + 19 new).

- [ ] **Step 4: Lighthouse on a sample Thai page.**

```bash
python3 -m http.server 8123 >/tmp/portfolio-http.log 2>&1 &
sleep 1
npx --yes lighthouse http://localhost:8123/index-th.html \
  --only-categories=accessibility,best-practices,seo \
  --output=json --output-path=/tmp/lh-index-th.json \
  --chrome-flags="--headless" --quiet
python3 -c "
import json
d = json.load(open('/tmp/lh-index-th.json'))
for k, v in d['categories'].items():
    print(k, round(v['score']*100))
"
kill %1 2>/dev/null
```

Expected: all three categories 100. If accessibility fails on something specific to the Thai page (not already fixed by the shared CSS work from the SEO-fix plan), fix and re-run before moving on.

- [ ] **Step 5: Full click-through of one Thai journey.**

In a browser: `index-th.html` → click a Selected Work card → confirm it lands on a `showcase-*-th.html` page → click a related-work card → confirm it's also `-th` → click "EN" → confirm it lands on the matching English page → click "TH" → confirm it returns to the same Thai page you started that hop from.

- [ ] **Step 6: If all checks pass, no commit needed (verification-only).** If Steps 1-2 found real problems, fix them in the relevant page(s), re-run the check, and commit the fix with a message describing what was wrong.
