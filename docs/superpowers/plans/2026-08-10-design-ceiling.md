# Design Ceiling Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Raise the portfolio's weakest review axis — Aesthetic and Minimalist Design, scored 2/4 on 2026-08-09 — by removing the three template tells that make a design portfolio look generated, and by fixing two font bugs found while measuring them.

**Architecture:** Three independent changes, each verifiable on its own. Typography is fixed first because two of the site's declared fonts are never loaded, so any judgement about "how the type looks" today is a judgement about a fallback nobody chose. Then the kicker is set quietly and the measurably redundant instances are removed — a count-based rule was drafted first and the copy disproved it. Then the four identical story cards are differentiated by content type. All work is CSS plus scripted HTML edits; no build step, no new dependency.

**Tech Stack:** Static HTML, two CSS files (`home-shell.css` 12 pages, `portfolio-pages.css` 56 pages), Google Fonts with `display=optional`, `python3 _tools/serve.py`, `npx lighthouse`, `python3 _tools/check-deploy.py`.

## Global Constraints

- **Lighthouse Accessibility, Best Practices and SEO must stay 100, and CLS must stay 0** on every page touched. Performance is not part of this bar. Best Practices caps at 77 on the live site because of Clarity's third-party cookies; on `localhost` Clarity does not load, so 100 is the local figure to hold.
- **`canScrollX: false` at 375×812 on every page touched**, and additionally **no element's `getBoundingClientRect().right` may exceed `clientWidth`** — `canScrollX` alone missed an 18px clipped CTA on 2026-08-10.
- **The two stylesheet families are never loaded together.** `home-shell.css` serves `index`, `work`, `services`, `about`, `faq`, `process` (± `-en`). `portfolio-pages.css` serves resume, 28 showcase/case-study pages, 6 category pages, 8 `web-*`. They name the same values differently: `--border`/`--border-2` in home-shell, `--line`/`--line-2` in portfolio-pages. Never assume a token exists in both.
- **Every `?v=` token for a changed asset moves in the same commit, across every file that references it.** `python3 _tools/check-deploy.py` must print `all changed assets have a moved ?v= token — good to ship` before any commit.
- **Fonts load with `display=optional`.** This is what keeps CLS at 0; `swap` would reintroduce layout shift.
- **Thai upper vowels and tone marks are drawn above the line box.** Any change to heading `line-height` or to the spacing above a heading must be checked against Thai text, not Latin. `.section-heading .eyebrow` carries `margin-bottom: 12px` for exactly this reason.
- **Never remove an `h2`.** Dropping `#packages`'s h2 on `services` once left `h1 → h3` and cost Accessibility 98. This plan removes `<span>`s only.
- **WCAG 2.5.3:** an element's accessible name must contain its visible text. Do not add `aria-label` that replaces visible wording.
- **Another session works in this repo.** Run `git status --porcelain` and `git log origin/main..HEAD` before starting. If either is non-empty, stop and report rather than committing on top of someone else's in-flight work.

---

## File Structure

| File | Responsibility in this plan |
|---|---|
| `assets/home-shell.css` | Body font stack for the 12 shell pages; `.section-label` spacing |
| `assets/portfolio-pages.css` | Body font stack for the 56 pages; `.eyebrow`; the `.story-*` block |
| 12 home-shell HTML files | Google Fonts `<link>` |
| 56 portfolio-pages HTML files | Google Fonts `<link>` |
| 36 files carrying a redundant kicker | Remove those 39 instances; restyle the rest |
| 28 `showcase-*.html` + 2 `case-study-raat*.html` | Story-stack markup |
| `CLAUDE.md` | Record the decisions and the two font bugs |

---

## Task 1: Load the fonts the site already claims to use

Two bugs, both invisible because a fallback silently takes over.

`home-shell.css:57` sets `font-family: 'Outfit', -apple-system, …`, but only `index.html` and `index-en.html` load Outfit. The other **10** shell pages — `about`, `faq`, `process`, `services`, `work`, each ± `-en` — render in `-apple-system`. The site's main selling pages are in a different typeface from its homepage and nobody chose that.

`portfolio-pages.css:41` sets `font-family: "Inter", "Noto Sans Thai", Arial`, but **0 of its 56 pages** load Noto Sans Thai. Every Thai character on resume, all 28 showcases, the 6 category pages and all 8 `web-*` pages is drawn by whatever the OS supplies — different on macOS, Windows, Android and iOS.

This task only makes the declared state true. Type choices come in Task 2.

**Files:**
- Modify: the 10 shell pages missing Outfit
- Modify: the 56 pages missing Noto Sans Thai
- Verify: `assets/home-shell.css:57`, `assets/portfolio-pages.css:41`

**Interfaces:**
- Produces: every page loads every family its stylesheet names. Task 2 replaces those names and relies on this being true first, so that the before/after comparison is between two chosen typefaces rather than between a fallback and a choice.

- [ ] **Step 1: Write the check that fails**

```bash
cat > /tmp/font-check.py <<'PY'
import re, pathlib, sys
bad = []
for f in sorted(pathlib.Path('.').glob('*.html')):
    s = f.read_text(encoding='utf-8')
    fam = set(re.findall(r'family=([A-Za-z+]+)', s))
    fam = {x.replace('+', ' ') for x in fam}
    if 'home-shell.css' in s and 'Outfit' not in fam:
        bad.append((f.name, 'declares Outfit, does not load it'))
    if 'portfolio-pages.css' in s and 'Noto Sans Thai' not in fam:
        bad.append((f.name, 'declares Noto Sans Thai, does not load it'))
for n, why in bad:
    print(f'  {n}: {why}')
print(f'{len(bad)} page(s) declare a font they never load')
sys.exit(1 if bad else 0)
PY
python3 /tmp/font-check.py
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `python3 /tmp/font-check.py; echo "exit=$?"`
Expected: `66 page(s) declare a font they never load` and `exit=1`.

- [ ] **Step 3: Add the missing families to the existing Google Fonts link**

Every page already has one `<link href="https://fonts.googleapis.com/css2?family=…">`. Extend it rather than adding a second request.

```bash
python3 - <<'PY'
import re, pathlib
n = 0
for f in sorted(pathlib.Path('.').glob('*.html')):
    s = f.read_text(encoding='utf-8')
    m = re.search(r'(<link href="https://fonts\.googleapis\.com/css2\?)([^"]+)(" rel="stylesheet">)', s)
    if not m:
        continue
    q = m.group(2)
    add = []
    if 'home-shell.css' in s and 'family=Outfit' not in q:
        add.append('family=Outfit:wght@400;500;600;700;800')
    if 'portfolio-pages.css' in s and 'family=Noto+Sans+Thai' not in q:
        add.append('family=Noto+Sans+Thai:wght@400;500;600;700')
    if not add:
        continue
    parts = q.split('&')
    display = [p for p in parts if p.startswith('display=')]
    families = [p for p in parts if not p.startswith('display=')]
    newq = '&'.join(sorted(families + add) + (display or ['display=optional']))
    s = s[:m.start(2)] + newq + s[m.end(2):]
    f.write_text(s, encoding='utf-8')
    n += 1
print(f'{n} file(s) updated')
PY
```

- [ ] **Step 4: Run the check to verify it passes**

Run: `python3 /tmp/font-check.py; echo "exit=$?"`
Expected: `0 page(s) declare a font they never load` and `exit=0`.

- [ ] **Step 5: Confirm every font request still returns Thai and still uses display=optional**

```bash
grep -ho 'css2?[^"]*' *.html | sort -u | while read -r q; do
  echo "$q" | grep -q 'display=optional' || echo "  MISSING display=optional: $q"
done
echo "--- distinct font requests ---"
grep -ho 'css2?[^"]*' *.html | sort | uniq -c | sort -rn
```

Expected: no `MISSING display=optional` lines.

- [ ] **Step 6: Verify no layout shift was introduced**

```bash
(nohup python3 _tools/serve.py 8123 >/tmp/serve.log 2>&1 &) ; sleep 2
S=/tmp/lh-task1
mkdir -p $S
for p in "" work about showcase-supplymate web-clinic; do
  npx -y lighthouse "http://localhost:8123/$p" --quiet --chrome-flags="--headless" \
    --output=json --output-path=$S/$(echo "${p:-index}").json >/dev/null 2>&1
done
python3 - <<PY
import json, glob, os
for f in sorted(glob.glob("$S/*.json")):
    d = json.load(open(f))
    c = {k: round(v['score']*100) for k, v in d['categories'].items() if v.get('score') is not None}
    print(os.path.basename(f)[:-5], c, 'CLS', d['audits']['cumulative-layout-shift']['displayValue'])
PY
```

Expected: accessibility, best-practices and seo all `100`; CLS `0` on all five.

- [ ] **Step 7: Commit**

```bash
git add *.html
git commit -m "fix: load the two fonts 66 pages declared and never requested

home-shell.css names Outfit but only index and index-en ever loaded it, so
the ten other shell pages — about, faq, process, services, work, each with
its -en twin — rendered in -apple-system. The site's main selling pages were
in a different typeface from its homepage and nothing said so.

portfolio-pages.css names Noto Sans Thai but not one of its 56 pages
requested it, so every Thai character on the resume, the 28 showcases, the 6
category pages and the 8 web-* pages was drawn by whatever the OS happened to
have. Thai rendering differed between macOS, Windows, Android and iOS with no
way to notice from the CSS.

Families were appended to each page's existing Google Fonts request rather
than added as a second one, and display=optional is unchanged, so CLS stays 0."
```

---

## Task 2: One display face, chosen against rendered Thai

With Task 1 done, the site renders in the faces it names: Inter + Noto Sans Thai on 56 pages, Outfit on 12. Both are single-family, and Inter is the most-used typeface in AI-generated UI — for a portfolio whose product is design, using the default face argues against its owner.

The change is deliberately narrow: **headings only**. The body face stays. Swapping body type across 84 pages risks line-height, Thai vowel collisions and CLS for little gain; a display face delivers most of the distinctiveness at a fraction of the risk.

**Default choice: `Bai Jamjuree` for `h1`/`h2`.** Verified 2026-08-10 to serve 12 `@font-face` blocks including `U+0E01` Thai coverage. It is a geometric Thai sans against a humanist body, which is a real contrast axis; it is not on the reflex-reject list; and it is already proven in this repo on `construction-landing`. Step 2 renders it against three alternatives at real sizes in Thai and English, and the comparison may reject it — but it is the default, not a placeholder.

**Files:**
- Modify: `assets/portfolio-pages.css` — `h1, h2, h3` block near line 227
- Modify: `assets/home-shell.css` — heading rules
- Modify: all 68 HTML files — Google Fonts request
- Modify: `CLAUDE.md`

**Interfaces:**
- Consumes: Task 1's guarantee that every declared family is loaded.
- Produces: a `--font-display` custom property in both stylesheets, set to the chosen stack. Task 4 uses it for the story-card headings.

- [ ] **Step 1: Build the comparison page**

```bash
cat > _typecmp.html <<'EOF'
<!doctype html><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Bai+Jamjuree:wght@600;700&family=Anuphan:wght@600;700&family=Chakra+Petch:wght@600;700&family=Trirong:wght@600;700&family=Inter:wght@600;700;800&display=swap" rel="stylesheet">
<body style="margin:0;background:#0d1117;color:#e6edf3;font-family:Inter,sans-serif;padding:28px">
<div id="rows"></div>
<script>
const faces=['Inter','Bai Jamjuree','Anuphan','Chakra Petch','Trirong'];
document.getElementById('rows').innerHTML = faces.map(f=>`
  <section style="border-top:1px solid #21262d;padding:22px 0">
    <div style="color:#8b949e;font-size:.75rem;margin-bottom:10px">${f}</div>
    <h1 style="font-family:'${f}',sans-serif;font-weight:800;font-size:3.2rem;line-height:1.02;margin:0 0 8px">รับทำเว็บไซต์ธุรกิจ</h1>
    <h1 style="font-family:'${f}',sans-serif;font-weight:800;font-size:3.2rem;line-height:1.02;margin:0 0 8px">SupplyMate Wholesale</h1>
    <h2 style="font-family:'${f}',sans-serif;font-weight:700;font-size:1.9rem;line-height:1.1;margin:0">คุณต้องการเว็บแบบไหน? ปัญหาที่ได้ยินบ่อยที่สุด</h2>
  </section>`).join('');
</script>
</body>
EOF
(nohup python3 _tools/serve.py 8123 >/tmp/serve.log 2>&1 &) ; sleep 2
echo "open http://localhost:8123/_typecmp.html"
```

- [ ] **Step 2: Render and judge, with the Thai check that matters**

Open `http://localhost:8123/_typecmp.html` in a **foreground** tab and screenshot it.

Reject any face where, at `line-height: 1.02`:
- the tone mark on `ไ`/`ื` in `เว็บไซต์` touches or clips the line above, or
- `ญ`/`ฐ` descenders collide with the line below, or
- Latin and Thai on adjacent lines sit at visibly different optical weights.

Record the verdict in the commit message. If `Bai Jamjuree` is rejected, take the first survivor in the order listed.

- [ ] **Step 3: Add the display token to both stylesheets**

`portfolio-pages.css` — inside the existing `:root` block, after `--ease`:

```css
  /* Headings only. The body face stays Inter + Noto Sans Thai: swapping body
     type across 84 pages risks line-height, Thai vowel collisions and CLS for
     little gain, while a display face carries most of the distinctiveness.
     Chosen against rendered Thai at 3.2rem/1.02, not from a specimen. */
  --font-display: "Bai Jamjuree", "Noto Sans Thai", sans-serif;
```

`home-shell.css` — inside its `:root` block, after `--ease`:

```css
      --font-display: 'Bai Jamjuree', 'Outfit', sans-serif;
```

- [ ] **Step 4: Point the headings at it**

`portfolio-pages.css`, the existing `h1, h2, h3` rule (near line 227) gains one line:

```css
h1,
h2,
h3 {
  margin: 0;
  font-family: var(--font-display);
  letter-spacing: -0.02em;
  color: var(--ink);
  overflow-wrap: break-word;
}
```

`home-shell.css` — add after its heading rules, so it applies to both families of heading class:

```css
    h1, h2, h3,
    .section-title,
    .hero-role, .hero-role-alt { font-family: var(--font-display); }
```

- [ ] **Step 5: Load the face on every page**

```bash
python3 - <<'PY'
import re, pathlib
n = 0
for f in sorted(pathlib.Path('.').glob('*.html')):
    s = f.read_text(encoding='utf-8')
    if 'home-shell.css' not in s and 'portfolio-pages.css' not in s:
        continue
    m = re.search(r'(<link href="https://fonts\.googleapis\.com/css2\?)([^"]+)(" rel="stylesheet">)', s)
    if not m or 'family=Bai+Jamjuree' in m.group(2):
        continue
    parts = m.group(2).split('&')
    display = [p for p in parts if p.startswith('display=')]
    families = [p for p in parts if not p.startswith('display=')]
    families.append('family=Bai+Jamjuree:wght@600;700')
    s = s[:m.start(2)] + '&'.join(sorted(families) + (display or ['display=optional'])) + s[m.end(2):]
    f.write_text(s, encoding='utf-8')
    n += 1
print(f'{n} file(s) updated')
PY
python3 /tmp/font-check.py; echo "exit=$?"
```

Expected: `68 file(s) updated`, then `exit=0`.

- [ ] **Step 6: Bump both tokens and verify**

```bash
sed -i '' 's|portfolio-pages.css?v=[a-z0-9-]*|portfolio-pages.css?v=display-face|g' *.html
sed -i '' 's|home-shell.css?v=[a-z0-9-]*|home-shell.css?v=display-face|g' *.html
python3 _tools/check-deploy.py
```

Expected: `all changed assets have a moved ?v= token — good to ship`.

- [ ] **Step 7: Verify headings actually changed face and nothing overflows**

```bash
cat > _tv.html <<'EOF'
<!doctype html><meta charset="utf-8"><body><div id="o" style="white-space:pre;font:12px system-ui"></div>
<iframe id="f" width="375" height="812" style="border:0;position:absolute;left:-9999px"></iframe>
<script>
const P=['/','/work','/showcase-supplymate','/web-clinic','/resume'];
const f=document.getElementById('f'),o=document.getElementById('o');window.r=[];
window.run=async()=>{for(const p of P){
 await new Promise(r=>{f.onload=()=>setTimeout(r,2000);f.src=p});
 const d=f.contentDocument,w=d.defaultView,de=d.documentElement;
 d.querySelectorAll('.reveal').forEach(e=>e.classList.add('visible'));
 de.scrollLeft=50;const can=de.scrollLeft>0;de.scrollLeft=0;
 const h=d.querySelector('h1')||d.querySelector('h2');
 const over=[...d.querySelectorAll('*')].filter(e=>e.getBoundingClientRect().right>de.clientWidth+1)
   .map(e=>e.tagName+'.'+(e.className||'').toString().slice(0,26));
 window.r.push({p,canScrollX:can,headingFont:h?w.getComputedStyle(h).fontFamily.split(',')[0]:null,
   overflowing:[...new Set(over)].slice(0,4)});
 o.textContent+=JSON.stringify(window.r.at(-1))+'\n';}
 return 'done'};
</script></body>
EOF
echo "open http://localhost:8123/_tv.html then run window.run()"
```

Expected on every row: `headingFont` is `"Bai Jamjuree"`, `canScrollX` is `false`, `overflowing` is `[]`.

- [ ] **Step 8: Lighthouse**

```bash
S=/tmp/lh-task2; mkdir -p $S
for p in "" work showcase-supplymate web-clinic; do
  npx -y lighthouse "http://localhost:8123/$p" --quiet --chrome-flags="--headless" \
    --output=json --output-path=$S/$(echo "${p:-index}").json >/dev/null 2>&1
done
python3 - <<PY
import json, glob, os
for f in sorted(glob.glob("$S/*.json")):
    d = json.load(open(f))
    c = {k: round(v['score']*100) for k, v in d['categories'].items() if v.get('score') is not None}
    a = [r['id'] for r in d['categories']['accessibility']['auditRefs'] if d['audits'][r['id']].get('score') not in (None, 1)]
    print(os.path.basename(f)[:-5], c, 'a11y:', a or 'none', 'CLS', d['audits']['cumulative-layout-shift']['displayValue'])
PY
rm -f _typecmp.html _tv.html
```

Expected: accessibility/best-practices/seo `100`, no a11y failures, CLS `0`.

- [ ] **Step 9: Commit**

```bash
git add assets/home-shell.css assets/portfolio-pages.css *.html
git commit -m "feat: give the headings a face of their own

The site was single-family everywhere and the family was Inter, the most-used
typeface in AI-generated UI. On a portfolio whose product is design, the
default face argues against its owner.

Headings only. The body stays Inter + Noto Sans Thai: swapping body type on 84
pages risks line-height, Thai vowel collisions and CLS for very little, while a
display face carries most of the distinctiveness. Both stylesheets now name a
--font-display token so there is one place to change it.

Bai Jamjuree, chosen by rendering Thai and Latin headings at 3.2rem/1.02
against Anuphan, Chakra Petch, Trirong and Inter, and checking that tone marks
in เว็บไซต์ clear the line above and ญ descenders clear the line below. A
geometric Thai sans against a humanist body is a real contrast axis; two
similar sans faces would not be.

CLS stays 0 — display=optional is unchanged and the family was appended to each
page's existing request rather than added as a second one."
```

---

## Task 3: Quiet the kicker, and cut only the ones that repeat

The first draft of this task said "one kicker per page". Measuring the copy before writing the
script showed that rule is wrong, and it is recorded here so nobody re-derives it.

Of 25 `.section-label`s on the 12 shell pages, only **3** repeat their heading
(`ผลงาน`/`ผลงานคัดสรร`, `บริการ`/`บริการและราคา`, `ประสบการณ์`/`ประสบการณ์และทักษะ`). The other
22 complement it — `เริ่มตรงนี้` over `คุณต้องการเว็บแบบไหน?`, `มาร่วมงานกัน` over `ติดต่อผม`.
CLAUDE.md already records that `about` and `process` keep theirs deliberately. Of 244
`.eyebrow`-to-heading pairs on the 56 portfolio pages, the clear repeats are
`related work`/`More projects like this one.` (14 pages),
`ผลงานที่เกี่ยวข้อง`/`โปรเจกต์อื่นที่ใกล้เคียงกัน` (14) and
`คำถามที่พบบ่อย`/`คำถามก่อนเริ่มงาน` (8). `project showcase` above the project name, and
`ขอบเขตงาน` above `ราคานี้ได้อะไร และไม่ได้อะไร`, are doing real work.

So the tell is not the count — it is the **treatment**. `0.82rem / weight 700 / uppercase /
1.6px tracking / 28px rule in front` is the recognisable 2023 kicker; the same words set
quietly are just a label. This task changes the treatment everywhere and deletes only the 39
instances that measurably repeat.

**Files:**
- Modify: `assets/portfolio-pages.css` — `.eyebrow` and `.eyebrow::before`
- Modify: `assets/home-shell.css` — `.section-label`
- Modify: the 36 files carrying a redundant kicker

**Interfaces:**
- Consumes: nothing. Kickers deliberately stay in the body face, not `--font-display`.
- Produces: nothing later depends on this.

- [ ] **Step 1: Write the check that fails**

Save this as `/tmp/kicker-check.py` with an editor, not a shell heredoc — it contains regex
braces that a nested heredoc will mangle.

```python
import re, pathlib, sys

REDUNDANT = [
    ('eyebrow', 'related work'),
    ('eyebrow', 'ผลงานที่เกี่ยวข้อง'),
    ('eyebrow', 'คำถามที่พบบ่อย'),
    ('section-label', 'ผลงาน'),
    ('section-label', 'บริการ'),
    ('section-label', 'ประสบการณ์'),
]

found = 0
for f in sorted(pathlib.Path('.').glob('*.html')):
    s = f.read_text(encoding='utf-8')
    for cls, text in REDUNDANT:
        pattern = '<span class="' + cls + '"[^>]*>\\s*' + re.escape(text) + '\\s*</span>'
        for _ in re.finditer(pattern, s):
            print('  ' + f.name + ': ' + cls + ' "' + text + '"')
            found += 1
print(str(found) + ' redundant kicker(s) remain')
sys.exit(1 if found else 0)
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `python3 /tmp/kicker-check.py; echo "exit=$?"`

Expected: 39 lines listing file and kicker, then `39 redundant kicker(s) remain` and `exit=1`.

The `section-label` entries must match on exact text — `ผลงาน` is a prefix of
`ผลงานที่เกี่ยวข้อง`, and the `\s*` anchors either side of the escaped text are what keep the
two apart. If the count comes out above 39, the anchors are not holding; fix the pattern before
running Step 3.

- [ ] **Step 3: Delete only those**

Save as `/tmp/kicker-fix.py` with an editor:

```python
import re, pathlib

REDUNDANT = [
    ('eyebrow', 'related work'),
    ('eyebrow', 'ผลงานที่เกี่ยวข้อง'),
    ('eyebrow', 'คำถามที่พบบ่อย'),
    ('section-label', 'ผลงาน'),
    ('section-label', 'บริการ'),
    ('section-label', 'ประสบการณ์'),
]

n = 0
for f in sorted(pathlib.Path('.').glob('*.html')):
    s = f.read_text(encoding='utf-8')
    before = s
    for cls, text in REDUNDANT:
        pattern = '[ \\t]*<span class="' + cls + '"[^>]*>\\s*' + re.escape(text) + '\\s*</span>\\n?'
        s = re.sub(pattern, '', s)
    if s != before:
        f.write_text(s, encoding='utf-8')
        n += 1
print(str(n) + ' file(s) updated')
```

Run: `python3 /tmp/kicker-fix.py && python3 /tmp/kicker-check.py; echo "exit=$?"`

Expected: `36 file(s) updated`, then `0 redundant kicker(s) remain` and `exit=0`.

- [ ] **Step 4: Take the shout out of the ones that stay**

In `assets/portfolio-pages.css`, replace the existing `.eyebrow` rule with this, and **delete
the `.eyebrow::before` rule entirely** — the 28px rule in front is half the tell.

```css
/* Set quietly. The words mostly earn their place: `ขอบเขตงาน` above "ราคานี้ได้
   อะไร และไม่ได้อะไร" tells a reader something the heading does not. What made
   this read as scaffolding was the treatment — 0.8rem at weight 700,
   uppercased, tracked 1.6px, with a rule in front. That exact combination is
   the kicker every generated landing page shipped in 2023. Same words,
   ordinary label. */
.eyebrow {
  display: inline-block;
  color: var(--accent-text);
  font-size: 0.82rem;
  font-weight: 600;
  letter-spacing: 0;
  text-transform: none;
}
```

In `assets/home-shell.css`, the `.section-label` rule loses the same three properties: set
`text-transform: none`, `letter-spacing: 0`, `font-weight: 600`, and remove its `::before` if it
has one.

⚠️ `.section-heading .eyebrow { margin-bottom: 12px }` **stays.** It exists because Thai upper
vowels and tone marks are drawn above the line box and collided with the heading at
`line-height: 1.1`. Lowercasing the kicker does not change that.

- [ ] **Step 5: Verify Thai still clears, in both families**

```bash
(nohup python3 _tools/serve.py 8123 >/tmp/serve.log 2>&1 &) ; sleep 2
```

Open `http://localhost:8123/web-clinic` and `http://localhost:8123/process` in a **foreground**
tab — a background tab freezes CSS transitions and suspends IntersectionObserver, so reveal
content never appears and the check is worthless. At each kicker sitting directly above a Thai
`h2`, confirm no tone mark or upper vowel touches the kicker's baseline. Screenshot both.

- [ ] **Step 6: Bump tokens, check heading order, run Lighthouse**

```bash
sed -i '' 's|portfolio-pages.css?v=[a-z0-9-]*|portfolio-pages.css?v=quiet-kicker|g' *.html
sed -i '' 's|home-shell.css?v=[a-z0-9-]*|home-shell.css?v=quiet-kicker|g' *.html
python3 _tools/check-deploy.py
```

Expected: `all changed assets have a moved ?v= token — good to ship`.

Save as `/tmp/heading-order.py` and run it:

```python
import re, pathlib

bad = []
for f in sorted(pathlib.Path('.').glob('*.html')):
    order = ''.join(re.findall(r'<h([1-6])[ >]', f.read_text(encoding='utf-8')))
    for i in range(len(order) - 1):
        if int(order[i+1]) - int(order[i]) > 1:
            bad.append(f.name)
            break
print('heading-order breaks:', bad or 'NONE')
```

Expected: `NONE`. Only spans were removed, so any break here means the delete pattern ate more
than it should have — revert and fix the pattern.

Then run the Task 2 Step 8 Lighthouse command over `""`, `work`, `process`,
`showcase-supplymate` and `web-clinic`. Expected: accessibility, best-practices and seo `100`,
no a11y failures, CLS `0`.

- [ ] **Step 7: Commit**

```bash
git add *.html assets/portfolio-pages.css assets/home-shell.css
git commit -m "refactor: quiet the kicker, delete only the ones that repeat

This task began as one kicker per page. Measuring the copy first showed that
was wrong: of 25 .section-labels on the shell pages only three repeat their
heading, and of 244 .eyebrow-to-heading pairs on the portfolio pages the clear
repeats are related work, ผลงานที่เกี่ยวข้อง and คำถามที่พบบ่อย. project
showcase above a project name, and ขอบเขตงาน above ราคานี้ได้อะไร และไม่ได้
อะไร, tell a reader something the heading does not, and CLAUDE.md already
recorded that about and process keep theirs on purpose.

So the tell was the treatment, not the count. 0.8rem at weight 700, uppercased,
tracked 1.6px, with a 28px rule in front is the kicker every generated landing
page shipped in 2023. Those four properties are gone; the words stay.

39 measurably redundant instances removed across 36 files. Only spans were
touched and heading order comes back clean.

.section-heading .eyebrow keeps its 12px bottom margin: Thai upper vowels and
tone marks are drawn above the line box and collided with the heading at
line-height 1.1. Lowercasing does not change that."
```

---

## Task 4: Four cards that look like four different things

Every showcase and case-study page ends in a `.story-stack` of four `.story-card`s with identical radius, border, surface and padding, each opened by a 40×40 rounded tinted `.story-icon`. **128 cards and 128 badges across 32 files.** Two flagged patterns compounding: identical card grids, and a large rounded icon above every heading.

The four hold genuinely different content — a narrative paragraph, a bullet list, a fit statement, and the call to action — and dressing them the same flattens the page into one texture with nothing for the eye to catch.

Differentiate by what each one is:

| Position | Content | Treatment |
|---|---|---|
| 1 | Project overview + tag list | stays a card — it is the anchor |
| 2 | The 30-second list | leaves the card: a ruled list on the page |
| 3 | Who it fits | leaves the card: an indented statement, larger type |
| 4 | The ask | stays a card, keeps `.accent` — it is the CTA |

The `.story-icon` badge goes from all four.

**Files:**
- Modify: `assets/portfolio-pages.css` — the `.story-*` block
- Modify: 28 `showcase-*.html` + `case-study-raat.html` + `case-study-raat-en.html`

**Interfaces:**
- Consumes: `--font-display` from Task 2.
- Produces: `.story-card--flat` and `.story-card--statement` modifiers on cards 2 and 3. Nothing later depends on them.

- [ ] **Step 1: Write the check that fails**

```bash
cat > /tmp/story-check.py <<'PY'
import re, pathlib, sys
bad = []
for f in sorted(pathlib.Path('.').glob('showcase-*.html')) + sorted(pathlib.Path('.').glob('case-study-raat*.html')):
    s = f.read_text(encoding='utf-8')
    icons = len(re.findall(r'class="story-icon', s))
    flat = len(re.findall(r'story-card--flat', s))
    stmt = len(re.findall(r'story-card--statement', s))
    if icons or flat != 1 or stmt != 1:
        bad.append((f.name, icons, flat, stmt))
for n, i, fl, st in bad:
    print(f'  {n}: icons={i} flat={fl} statement={st}')
print(f'{len(bad)} page(s) still undifferentiated')
sys.exit(1 if bad else 0)
PY
python3 /tmp/story-check.py
```

- [ ] **Step 2: Run it to confirm it fails**

Run: `python3 /tmp/story-check.py; echo "exit=$?"`
Expected: 30 pages listed with `icons=4 flat=0 statement=0`, and `exit=1`.

- [ ] **Step 3: Rewrite the markup**

Cards are in fixed order on all 30 pages — verified 2026-08-09: every file has exactly 4 `.story-card`, exactly 1 `.story-card.accent`, and it is the last.

```bash
python3 - <<'PY'
import re, pathlib

ICON = re.compile(r'[ \t]*<span class="story-icon[^"]*"[^>]*>.*?</span>\n?', re.S)
CARD = re.compile(r'<article class="story-card( accent)? reveal">')

n = 0
for f in sorted(pathlib.Path('.').glob('showcase-*.html')) + sorted(pathlib.Path('.').glob('case-study-raat*.html')):
    s = f.read_text(encoding='utf-8')
    s = ICON.sub('', s)
    idx = {'i': 0}
    def repl(m):
        idx['i'] += 1
        if idx['i'] == 2:
            return '<article class="story-card story-card--flat reveal">'
        if idx['i'] == 3:
            return '<article class="story-card story-card--statement reveal">'
        return m.group(0)
    s = CARD.sub(repl, s)
    f.write_text(s, encoding='utf-8')
    n += 1
print(f'{n} file(s) rewritten')
PY
python3 /tmp/story-check.py; echo "exit=$?"
```

Expected: `30 file(s) rewritten`, then `exit=0`.

- [ ] **Step 4: Style the two new shapes**

Append to `assets/portfolio-pages.css`:

```css
/* ============================================================
   Story stack — four shapes, not four copies. Added 2026-08-10.

   The four cards held a narrative paragraph, a bullet list, a fit statement
   and a call to action, dressed identically: same radius, border, surface and
   padding, each opened by a 40×40 rounded tinted badge. 128 cards and 128
   badges across 32 files, flattening every project page into one texture.

   Card 1 stays a card because it anchors the page; card 4 stays because it is
   the ask. The middle two step out of their boxes.
   ============================================================ */

/* 2 · the 30-second list reads as a list, not as a boxed list */
.story-card--flat {
  padding-left: 0;
  padding-right: 0;
  border: 0;
  border-top: 1px solid var(--line);
  border-radius: 0;
  background: none;
}

/* 3 · who it fits is one claim, so it is set as one — larger, indented,
   with a rule instead of a container. Left rule is 1px: a divider, not the
   decorative side-stripe the shared bans rule out. */
.story-card--statement {
  padding: 4px 0 4px 22px;
  border: 0;
  border-left: 1px solid var(--accent);
  border-radius: 0;
  background: none;
}

.story-card--statement p {
  color: var(--ink-2);
  font-size: 1.08rem;
  line-height: 1.7;
}

/* The head lost its badge, so the text is now the whole row. */
.story-card--flat .story-head,
.story-card--statement .story-head { gap: 0; }

.story-card h2 { font-family: var(--font-display); }

@media (max-width: 640px) {
  .story-card--statement { padding-left: 16px; }
}
```

- [ ] **Step 5: Confirm the badge rules are dead and remove them**

```bash
grep -rn "story-icon" *.html | wc -l
```

Expected: `0`. Then delete the `.story-icon`, `.story-icon.amber`, `.story-icon.mint`, `.story-icon.rose` and `.story-icon svg` rules from `assets/portfolio-pages.css`.

- [ ] **Step 6: Bump the token and check**

```bash
sed -i '' 's|portfolio-pages.css?v=[a-z0-9-]*|portfolio-pages.css?v=story-shapes|g' *.html
python3 _tools/check-deploy.py
```

Expected: `all changed assets have a moved ?v= token — good to ship`.

- [ ] **Step 7: Verify contrast, overflow and Lighthouse**

```bash
cat > _sv.html <<'EOF'
<!doctype html><meta charset="utf-8"><body><div id="o" style="white-space:pre;font:12px system-ui"></div>
<iframe id="f" width="375" height="812" style="border:0;position:absolute;left:-9999px"></iframe>
<script>
const P=['/showcase-supplymate','/showcase-buildnest','/case-study-raat'];
const f=document.getElementById('f'),o=document.getElementById('o');window.r=[];
window.run=async()=>{for(const p of P){
 await new Promise(r=>{f.onload=()=>setTimeout(r,2200);f.src=p});
 const d=f.contentDocument,w=d.defaultView,de=d.documentElement;
 d.querySelectorAll('.reveal').forEach(e=>e.classList.add('visible'));
 de.scrollLeft=50;const can=de.scrollLeft>0;de.scrollLeft=0;
 const cards=[...d.querySelectorAll('.story-card')].map(c=>w.getComputedStyle(c).borderTopWidth+'/'+w.getComputedStyle(c).backgroundColor.slice(0,12));
 const over=[...d.querySelectorAll('*')].filter(e=>e.getBoundingClientRect().right>de.clientWidth+1).length;
 window.r.push({p,canScrollX:can,overflowing:over,icons:d.querySelectorAll('.story-icon').length,shapes:cards});
 o.textContent+=JSON.stringify(window.r.at(-1))+'\n';}
 return 'done'};
</script></body>
EOF
echo "open http://localhost:8123/_sv.html then run window.run()"
```

Expected on every row: `canScrollX` `false`, `overflowing` `0`, `icons` `0`, and `shapes` showing four **different** values rather than four identical ones.

Then Lighthouse on `showcase-supplymate`, `showcase-buildnest`, `case-study-raat` with the Task 2 Step 8 command. Expected: accessibility/best-practices/seo `100`, CLS `0`.

- [ ] **Step 8: Clean up and commit**

```bash
rm -f _sv.html
git add assets/portfolio-pages.css showcase-*.html case-study-raat*.html
git commit -m "refactor: the four story cards become four shapes

Every showcase and case-study page ended in four cards with identical radius,
border, surface and padding, each opened by a 40×40 rounded tinted badge — 128
cards and 128 badges across 32 files. Identical card grids and a large rounded
icon above every heading are two separate template tells, and here they
compounded: the page read as one texture with nothing for the eye to catch.

The four hold different things, so they are now shaped differently. The
overview stays a card because it anchors the page and carries the tag list.
The 30-second list steps out and reads as a list. Who-it-fits is one claim, so
it is set as one — larger, indented, a 1px rule instead of a container. The ask
stays a card and keeps .accent, because it is the call to action.

The badges are gone from all four. The statement's left rule is 1px, a divider
rather than the decorative side-stripe the shared bans rule out."
```

---

## Task 5: Record the decisions

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Add the two font bugs and the three rules**

Insert before the `## Two stylesheet families — never mix them` heading:

```markdown
## Typography

**Body:** Inter + Noto Sans Thai on the 56 `portfolio-pages.css` pages; Outfit on the 12
`home-shell.css` pages. **Display (`h1`/`h2`/`h3` and `.section-title`):** Bai Jamjuree, via a
`--font-display` token declared in both stylesheets — change it there, not at the call sites.

⚠️ **Both stylesheets once named a font that most of their pages never loaded**, and a
fallback covered for it silently. `home-shell.css` named Outfit while only `index` and
`index-en` requested it, so the ten other shell pages rendered in `-apple-system`.
`portfolio-pages.css` named Noto Sans Thai while **none** of its 56 pages requested it, so all
Thai text fell to whatever the OS supplied and differed between macOS, Windows, Android and
iOS. Found 2026-08-10. **After any font edit, check that every page loads every family its
stylesheet names** — nothing in the CSS reveals the gap.

Families are appended to each page's single existing Google Fonts request, never added as a
second `<link>`, and `display=optional` is never changed: it is what holds CLS at 0.

Display faces are chosen by rendering Thai and Latin headings at the real size and
line-height, not from a specimen. The test that matters is whether the tone mark in
`เว็บไซต์` clears the line above and `ญ` clears the line below at `line-height: 1.02`.

**The kicker was restyled, not counted out.** `.eyebrow` and `.section-label` ran 246 and 61
times before 2026-08-10, and the drafted rule here was "one per page". Measuring the copy
disproved it: only 3 of 25 `.section-label`s repeat their heading, and most `.eyebrow`s
complement it — `เริ่มตรงนี้` above `คุณต้องการเว็บแบบไหน?` tells a reader something the
heading does not, and CLAUDE.md already recorded that `about` and `process` keep theirs on
purpose. What read as generated was the *treatment*: 0.8rem at weight 700, uppercased,
tracked 1.6px, with a 28px rule in front. Those four properties are gone and the words
stayed; only the 44 instances that measurably repeated their own heading were deleted.
⚠️ Do not re-derive "delete kickers" from that commit's 44 deletions — it is the opposite of
what was decided. `.section-heading .eyebrow { margin-bottom: 12px }` stays regardless: Thai
upper vowels and tone marks are drawn above the line box and collide with the heading at
`line-height: 1.1`.

**The story stack is four shapes, not four copies.** Card 1 is a card (it anchors the page and
holds the tags), card 2 is a bare ruled list, card 3 is an indented statement, card 4 is the
accent card (it is the ask). There are no `.story-icon` badges: a large rounded icon above
every heading is a template tell, and it compounded with the identical-card one.
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: record the typography rules and the two silent font bugs"
```

---

## Self-Review

**Spec coverage.** The review's three Aesthetic findings each have a task: single font → Task 2, the kicker → Task 3, 128 identical cards with badges → Task 4. Task 3 changed shape during writing: the drafted "one kicker per page" rule was tested against the copy and found to delete 22 shell-page labels and ~200 portfolio-page eyebrows that complement rather than repeat their heading, including a decision CLAUDE.md already records for `about` and `process`. It now restyles all of them and deletes the 39 that measurably repeat. The two font bugs found while measuring are Task 1, which must precede Task 2 or the comparison would be between a fallback and a choice rather than between two chosen faces. Task 5 records all of it.

**Placeholder scan.** Every step carries the command or the CSS it needs. Task 2 Step 2 is a human judgement call, which is why it ships with a named default (`Bai Jamjuree`), a stated fallback order, and three concrete rejection criteria rather than "pick a font you like".

**Type consistency.** `--font-display` is declared in Task 2 Step 3 and used in Task 2 Step 4 and Task 4 Step 4. `.story-card--flat` and `.story-card--statement` are produced in Task 4 Step 3 and styled in Step 4; the check script in Step 1 asserts exactly one of each per page. `/tmp/font-check.py` is written in Task 1 Step 1 and reused in Task 2 Step 5.

**Known gap, deliberately out of scope.** The review also scored User Control 2/4, for the 13 demo pages that open in the same tab with no way back. That is an unrelated navigation fix and belongs in its own plan; folding it in here would mean one commit touching demos, showcases and both stylesheets at once.
