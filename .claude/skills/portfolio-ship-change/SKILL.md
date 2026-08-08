---
name: portfolio-ship-change
description: >
  Use when deploying any change to Phakin's portfolio (my-portfolio) — pushing to
  main, "deploy", "ship it", "push", or finishing work that will go live at
  ph-akin.dev. Also use when a change touches both a stylesheet or script under
  assets/ and any .html file in the same batch, even if you are not deploying yet.
  Covers the ?v= cache token, sitemap lastmod, and verifying the live build.
---

# portfolio-ship-change

Ship a change to `ph-akin.dev` without breaking it for the people who have
already been there.

`main` auto-deploys. There is no staging, no build step, and no rollback other
than another push — so the checks below run **before** `git push`, not after.

---

## The one that actually bites

Run this. It is the whole rule:

```bash
python3 _tools/check-deploy.py
```

Exit 0 → nothing to bump. Exit 1 → it prints which asset, which token, how
many files reference it, and the `sed` line to fix it.

### Why a script and not a checklist

Every stylesheet and script here is referenced with a cache token:

```html
<link rel="stylesheet" href="assets/home-shell.css?v=merged-band">
```

GitHub Pages serves those with a long cache lifetime. **The condition that
requires a new token is:**

> a versioned asset changed **and** its `?v=` token did not

That is the predicate. It is *not* "did I touch a self-rendering script" — an
agent asked to add a badge to `services.html` reasoned, correctly against the
prose that existed at the time:

> "no cache-busting `?v=` bump is needed — this touches no self-rendering script"

…and shipped a new `.card-badge` element whose CSS rule only existed in the
copy nobody had yet downloaded. For returning visitors the pill would have
fallen back into normal flow and pushed the middle package card 38px out of
line with its neighbours — the exact breakage that same agent had rejected
during design.

**This never reproduces locally.** Your checkout is warm, so you see the new
asset every time. Nothing errors, nothing logs, and Lighthouse scores 100.

## The seven versioned assets

| asset | referenced by |
|---|---|
| `analytics.js` | 84 files |
| `site-search.js` · `site-search.css` | 64 files each |
| `portfolio-pages.css` | 52 files |
| `home-shell.css` · `site-ui.js` | 12 files each |
| `design-preview.js` | 8 files |

**Every reference moves together or not at all.** A half-bumped token splits
visitors across two versions of the same sheet.

Tokens are names, not numbers — `?v=feature-grid`, `?v=merged-band`. Name it
after the change so the diff explains itself.

## Full sequence

```bash
python3 _tools/check-deploy.py          # 1. bump if it says to, then re-run
python3 _tools/sitemap-lastmod.py       # 2. AFTER committing content — reads git log
git push origin main                    # 3. main auto-deploys
```

Then confirm the build actually landed — Pages takes ~30–60s and the first
poll usually still returns the old token:

```bash
curl -s https://ph-akin.dev/services | grep -o 'home-shell.css?v=[a-z-]*'
```

Check the *token you just set*, not that the page returns 200. A 200 proves
nothing; the old build serves 200 too.

## Quick reference

| Situation | Bump `?v=`? |
|---|---|
| HTML only | no |
| Asset only, no markup depends on the change | still yes — cheap, and "depends on" is easy to get wrong |
| Asset + HTML in the same batch | **yes** |
| Only `sitemap.xml` / `CLAUDE.md` / `docs/` | no |
| New page added | no bump; add it to `sitemap.xml` and `assets/search-index.json` (both `th` and `en`) |

## Common mistakes

- **Bumping only the file you edited.** `sed -i '' 's|name?v=old|name?v=new|g' *.html` — all references, one command.
- **Running `sitemap-lastmod.py` before committing.** It reads `git log`, so it stamps the *previous* commit's date. Commit content first, then regenerate, then commit the sitemap.
- **Serving with `python3 -m http.server`.** URLs here are extensionless; it 404s every internal link and a Lighthouse run measures a broken page. Use `python3 _tools/serve.py 8123`.
- **Treating a green Lighthouse as proof.** It renders one cold load. It cannot see the returning-visitor pairing at all.

## Red flags

- "It's only CSS" / "it's not a script" / "nothing self-renders here"
- "The markup doesn't really depend on that rule"
- "I'll bump it next time, this is a small change"
- Deploying without having run `check-deploy.py` in this session

**Each of these means: run the script and believe its exit code.**
