#!/usr/bin/env python3
"""Measured snapshot of the site, for the research step of the improve loop.

    python3 _tools/loop-scan.py            # full brief
    python3 _tools/loop-scan.py --defects  # BROKEN + DRIFT only (pre-push gate)
    python3 _tools/loop-scan.py --json     # machine-readable

It reports only what static files can prove. It cannot tell you whether copy is
TRUE, whether a page looks good, or what Lighthouse thinks — those need reading
the page and running a browser. Every section prints how many files it scanned,
so a clean result can be told apart from a broken pattern (CLAUDE.md -> "How to
measure this repo without fooling yourself").

Levels:
  BROKEN  a visitor or a crawler hits something wrong today
  DRIFT   two places in the repo disagree; one of them is a lie
  GAP     nothing is broken; this is the thinnest part of the site
  INFO    instrument counts and inventory
"""
import html
import json
import os
import re
import sys
from collections import defaultdict

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = "https://ph-akin.dev/"

findings = []          # (level, area, message)
info = []              # instrument counts


def add(level, area, msg):
    findings.append((level, area, msg))


def read(name):
    with open(os.path.join(ROOT, name), encoding="utf-8") as fh:
        return fh.read()


def html_files():
    return sorted(f for f in os.listdir(ROOT) if f.endswith(".html"))


# ---------------------------------------------------------------- taxonomy
def classify(files):
    """The site's own taxonomy: a page is what stylesheet it loads."""
    fam = {}
    for f in files:
        src = read(f)
        shell = "home-shell.css" in src
        pages = "portfolio-pages.css" in src
        if shell and pages:
            fam[f] = "BOTH"
        elif shell:
            fam[f] = "shell"
        elif pages:
            fam[f] = "portfolio"
        else:
            fam[f] = "demo"
    return fam


# ---------------------------------------------------------- card inventory
CARD_TAG = re.compile(r'<[a-z]+[^>]*class="[^"]*\bwork-card\b[^"]*"[^>]*>')
GRID_FILES = ["index.html", "index-en.html", "work.html", "work-en.html"]


def scan_cards():
    """Static .filter-count values are a no-JS fallback nothing validates."""
    per_file = {}
    for f in GRID_FILES:
        src = read(f)
        tags = CARD_TAG.findall(src)
        counts = defaultdict(int)
        all_tags = set()
        for t in tags:
            ind = re.search(r'data-industry="([^"]*)"', t)
            for key in (ind.group(1).split() if ind else []):
                counts[key] += 1
            dt = re.search(r'data-tags="([^"]*)"', t)
            if dt:
                all_tags |= {x.strip() for x in dt.group(1).split("|") if x.strip()}
        counts["all"] = len(tags)

        static = {}
        for m in re.finditer(r'data-filter="([^"]+)"(.*?)</button>', src, re.S):
            n = re.search(r'filter-count">\s*(\d+)\s*<', m.group(2))
            if n:
                static[m.group(1)] = int(n.group(1))

        for key, want in sorted(static.items()):
            got = counts.get(key, 0)
            if want != got:
                add("DRIFT", "card counts",
                    f"{f}: .filter-count for '{key}' says {want}, the DOM has {got} "
                    "(hand-maintained fallback, invisible with JS on)")
        for key in sorted(set(counts) - set(static) - {"all"}):
            add("BROKEN", "card counts",
                f"{f}: cards carry data-industry='{key}' but there is no filter button "
                "for it — those cards are unreachable from the filter")

        per_file[f] = {"cards": len(tags), "by_industry": dict(counts), "tags": sorted(all_tags)}

    sizes = {f: d["cards"] for f, d in per_file.items()}
    if len(set(sizes.values())) > 1:
        add("DRIFT", "card counts",
            "the four grid files disagree on card count: "
            + ", ".join(f"{k} {v}" for k, v in sizes.items()))

    info.append(f"cards: {sizes} across {len(GRID_FILES)} grid files")
    return per_file


def scan_tag_buttons(per_file):
    """A button with no card filters to an empty grid. That is the dangerous one."""
    for f in ("work.html", "work-en.html"):
        src = read(f)
        buttons = set(re.findall(r'data-tag="([^"]+)"', src))
        cards = set(per_file[f]["tags"])
        for t in sorted(buttons - cards):
            add("BROKEN", "tag filter",
                f"{f}: tag button '{t}' matches no card — clicking it empties the grid")
        orphan = sorted(cards - buttons)
        if orphan:
            add("INFO", "tag filter",
                f"{f}: {len(orphan)} tag(s) on cards with no button (harmless, "
                f"unfilterable): {', '.join(orphan)}")
        info.append(f"{f}: {len(buttons)} tag buttons vs {len(cards)} distinct card tags")


# ------------------------------------------------------------- proof strips
# Both languages: an -en category page has its own strip and can be thin on its own.
PACKAGE_PAGES = [f"{slug}{suffix}.html"
                 for slug in ("landing-page", "dashboard-ui", "business-website")
                 for suffix in ("", "-en")]


def scan_proof():
    """#related / .project-strip is the 'can he build it' answer. Rank the thin ones."""
    rows = []
    for f in html_files():
        if not (f.startswith("web-") or f in PACKAGE_PAGES):
            continue
        n = len(re.findall(r'class="project-link', read(f)))
        rows.append((n, f))
    rows.sort()
    info.append(f"proof strips measured on {len(rows)} pages (8 industry + 3 package)")
    for n, f in rows:
        if n == 0:
            add("BROKEN", "proof", f"{f}: #related strip is empty — the page makes a claim "
                                   "and shows nothing")
        elif n == 1:
            add("GAP", "proof", f"{f}: 1 project shown — thinnest kind of strip on the site. "
                                "A second demo built for this sector is the highest-value "
                                "page to add next")
        elif n == 2:
            add("GAP", "proof", f"{f}: 2 projects shown — thin")
    if rows:
        thin = ", ".join(f"{f.replace('.html','')} {n}" for n, f in rows[:3])
        fat = ", ".join(f"{f.replace('.html','')} {n}" for n, f in rows[-2:])
        add("INFO", "proof", f"thinnest: {thin} · fattest: {fat}")
    return rows


# ------------------------------------------------------- proof-piece wiring
def scan_wiring():
    """A new project lands in ~14 places and only some of them fail loudly.

    Measured against all 19 showcase pairs, which are 19/19 consistent today —
    so anything this reports on a new one is a missed step, not a new pattern.
    """
    try:
        shots = json.loads(read("_content/showcase-shots.json"))
        copy = json.loads(read("_content/project-copy.json"))["projects"]
    except Exception as exc:                                   # noqa: BLE001
        add("BROKEN", "wiring", f"_content/ canonical files unreadable: {exc}")
        return

    grids = {g: read(g) for g in GRID_FILES}

    # `short` is only used by #related strips on showcase / case-study pages, so
    # it is required only for a project some strip actually links to. Match the
    # .project-link anchor, not the bare slug: every -en page links its own Thai
    # slug from the language toggle, and counting that reported two projects as
    # missing copy they have no use for.
    strip_refs = set()
    anchor = re.compile(
        r'<a[^>]*class="[^"]*\bproject-link\b[^"]*"[^>]*href="([^"]+)"'
        r'|<a[^>]*href="([^"]+)"[^>]*class="[^"]*\bproject-link\b[^"]*"')
    for page in html_files():
        if not (page.startswith(("showcase-", "case-study-"))):
            continue
        for m in anchor.finditer(read(page)):
            href = (m.group(1) or m.group(2)).rstrip("/")
            strip_refs.add(href[:-3] if href.endswith("-en") else href)

    pairs = 0
    for f in sorted(html_files()):
        if not f.startswith("showcase-") or f.endswith("-en.html"):
            continue
        slug, key = f[:-5], f[len("showcase-"):-5]
        if slug + "-en.html" not in set(html_files()):
            continue                                    # the bilingual check owns this
        pairs += 1

        for g, want in (("index.html", slug), ("work.html", slug),
                        ("index-en.html", slug + "-en"), ("work-en.html", slug + "-en")):
            if f'href="{want}"' not in grids[g]:
                add("BROKEN", "wiring",
                    f"{slug}: no card linking to {want} in {g} — the project exists "
                    "but nothing in the grid reaches it")

        entry = copy.get(slug)
        if not entry:
            add("DRIFT", "wiring",
                f"{slug}: no entry in _content/project-copy.json — its blurb is "
                "repeated across the grids and #related strips with no canonical")
        else:
            roles = ["long"] + (["short"] if slug in strip_refs else [])
            for lang in ("th", "en"):
                for role in roles:
                    if not entry.get(lang, {}).get(role):
                        where = ("its #related strips on other showcase pages carry "
                                 "copy with no canonical, so check-copy.py cannot see "
                                 "it drift" if role == "short" else
                                 "its .work-problem blurb repeats across the grids "
                                 "with no canonical")
                        add("DRIFT", "wiring",
                            f"{slug}: project-copy.json missing {lang}.{role} — {where}")

        if key not in shots:
            add("DRIFT", "wiring",
                f"{slug}: key '{key}' missing from _content/showcase-shots.json — "
                "its screenshots cannot be re-captured when the demo changes")
        for suffix, view in (("", "A landing"), ("-b", "B mechanism"), ("-c", "C 375px")):
            shot = f"assets/screenshots/{slug}{suffix}.jpg"
            if not os.path.exists(os.path.join(ROOT, shot)):
                add("DRIFT", "wiring", f"{slug}: missing view {view} ({shot})")

        for side in (f, slug + "-en.html"):
            if "story-price" not in read(side):
                add("DRIFT", "wiring",
                    f"{side}: no .story-price — required on every showcase page "
                    "(19 sessions opened one and 1 reached Fastwork before it existed)")
    info.append(f"proof-piece wiring checked on {pairs} showcase pairs "
                f"(shots {len(shots)} keys · project-copy {len(copy)} keys · "
                f"{len(strip_refs)} linked from a #related strip)")


# ------------------------------------------------------------ page plumbing
def scan_plumbing(fam):
    files = html_files()
    for f in files:
        src = read(f)
        family = fam[f]
        if family == "BOTH":
            add("BROKEN", "stylesheet", f"{f}: loads home-shell.css AND portfolio-pages.css — "
                                        "nine selectors collide, the page is broken")
        if "assets/analytics.js" not in src:
            add("BROKEN", "analytics", f"{f}: no analytics.js tag — every click on it is invisible")
        if "display=swap" in src:
            add("DRIFT", "fonts", f"{f}: asks for display=swap; the site is display=optional "
                                  "everywhere (measured CLS 0.011-0.015 for swap)")
        if f != "404.html" and "location.replace" not in src:
            add("DRIFT", "urls", f"{f}: missing the .html -> extensionless redirect in <head> "
                                 "(a visitor on an old bookmark stays on the non-canonical URL)")
        m = re.search(r'<meta\s+name="description"\s+content="([^"]*)"', src)
        if not m:
            add("BROKEN", "seo", f"{f}: no meta description")
        else:
            # Count what a crawler counts. `&quot;` is six characters in the source
            # and one on screen, so SalonOS.html measured 206 against a real 196 —
            # the instrument, not the copy, put it 16 over instead of 6.
            shown = html.unescape(m.group(1))
            if len(shown) > 190:
                add("DRIFT", "seo",
                    f"{f}: meta description {len(shown)} chars (>190 is trimmed)")
        can = re.search(r'rel="canonical"\s+href="([^"]+)"', src)
        if not can:
            add("BROKEN", "seo", f"{f}: no canonical")
        else:
            want = SITE + ("404.html" if f == "404.html" else
                           "" if f == "index.html" else f[:-5])
            if can.group(1).rstrip("/") != want.rstrip("/"):
                add("DRIFT", "seo", f"{f}: canonical is {can.group(1)}, expected {want}")
    info.append(f"plumbing checked on all {len(files)} .html files "
                f"({sum(1 for v in fam.values() if v=='demo')} demo, "
                f"{sum(1 for v in fam.values() if v=='shell')} shell, "
                f"{sum(1 for v in fam.values() if v=='portfolio')} portfolio)")


# -------------------------------------------------------------- bilinguality
EN_EXEMPT_FAMILIES = {"demo"}          # demos + 404 have no -en twin by design
EN_EXEMPT_PREFIX = ("web-",)           # Thai-only industry pages by design


def scan_bilingual(fam):
    files = set(html_files())
    checked = 0
    for f in sorted(files):
        if f.endswith("-en.html") or fam[f] in EN_EXEMPT_FAMILIES:
            continue
        if f.startswith(EN_EXEMPT_PREFIX):
            src = read(f)
            if "hreflang" in src:
                add("DRIFT", "bilingual", f"{f}: Thai-only page carrying hreflang links")
            continue
        checked += 1
        twin = f[:-5] + "-en.html"
        if twin not in files:
            add("BROKEN", "bilingual", f"{f}: no English twin ({twin}) — unpaired page")
            continue
        for a, b in ((f, twin), (twin, f)):
            src = read(a)
            alts = dict(re.findall(r'hreflang="([^"]+)"\s+href="([^"]+)"', src))
            th = SITE + ("" if f == "index.html" else f[:-5])
            en = SITE + twin[:-5]
            want = {"th": th, "en": en, "x-default": th}
            for k, v in want.items():
                if k not in alts:
                    add("BROKEN", "bilingual", f"{a}: missing hreflang '{k}'")
                elif alts[k].rstrip("/") != v.rstrip("/"):
                    add("DRIFT", "bilingual",
                        f"{a}: hreflang {k} -> {alts[k]}, expected {v}")
            loc = "en_US" if a.endswith("-en.html") else "th_TH"
            if f'og:locale" content="{loc}"' not in src:
                add("DRIFT", "bilingual", f"{a}: og:locale is not {loc}")
    info.append(f"bilingual rules checked on {checked} TH/EN pairs")


# ------------------------------------------------------------- link integrity
LINK = re.compile(r'(?:href|src)="([^"]+)"')
SCRIPTISH = re.compile(r"<(script|style)\b.*?</\1>", re.S | re.I)


def scan_links():
    """Strip <script>/<style> first — a JS template literal (`${l.img}`) is not a link."""
    files = set(html_files())
    ids_cache = {}
    n_links = 0
    for f in sorted(files):
        src = SCRIPTISH.sub("", read(f))
        for raw in LINK.findall(src):
            if raw.startswith(("http://", "https://", "//", "mailto:", "tel:", "data:", "javascript:")):
                continue
            path, _, frag = raw.partition("#")
            n_links += 1
            if not path:
                target = f                                   # same-page anchor
            else:
                p = path.lstrip("/").split("?")[0]
                if p in ("", "/"):
                    target = "index.html"
                elif os.path.exists(os.path.join(ROOT, p)):
                    target = p
                elif os.path.exists(os.path.join(ROOT, p + ".html")):
                    target = p + ".html"
                else:
                    add("BROKEN", "links", f"{f}: dead link -> {raw}")
                    continue
            if frag and target.endswith(".html"):
                if target not in ids_cache:
                    ids_cache[target] = set(re.findall(r'\sid="([^"]+)"', read(target)))
                if frag not in ids_cache[target] and frag != "top":
                    add("BROKEN", "links", f"{f}: dead anchor -> {raw}")
    info.append(f"{n_links} relative links/assets resolved across {len(files)} files")


# ------------------------------------------------------------------ coverage
def scan_coverage():
    sm = read("sitemap.xml")
    locs = set(re.findall(r"<loc>([^<]+)</loc>", sm))
    if len(locs) != len(re.findall(r"<loc>", sm)):
        add("DRIFT", "sitemap", "duplicate <loc> entries in sitemap.xml")
    listed = {u[len(SITE):] or "index" for u in locs if u.startswith(SITE)}
    for u in sorted(locs):
        p = u[len(SITE):]
        fn = (p or "index") + ".html"
        if os.path.exists(os.path.join(ROOT, fn)) and "noindex" in read(fn):
            add("BROKEN", "sitemap", f"sitemap lists {u} but the page is robots:noindex")
        if p and not os.path.exists(os.path.join(ROOT, p + ".html")) \
           and not os.path.exists(os.path.join(ROOT, p)):
            add("BROKEN", "sitemap", f"sitemap lists {u} — no such file")

    try:
        idx = json.loads(read("assets/search-index.json"))
        indexed = {lang: {e.get("u", "").lstrip("/") or "index" for e in arr}
                   for lang, arr in idx.items() if isinstance(arr, list)}
    except Exception as exc:                                   # noqa: BLE001
        add("BROKEN", "search", f"search-index.json unreadable: {exc}")
        indexed = {}

    for f in html_files():
        src = read(f)
        if f == "404.html" or "noindex" in src:
            continue
        slug = "index" if f == "index.html" else f[:-5]
        if slug not in listed:
            add("DRIFT", "sitemap", f"{f} is indexable but not in sitemap.xml")
        if "site-search.js" in src:
            lang = "en" if f.endswith("-en.html") else "th"
            if indexed and slug not in indexed.get(lang, set()):
                add("DRIFT", "search", f"{f} carries the search widget but is not in "
                                       f"search-index.json['{lang}'] — unfindable on its own site")
    info.append(f"sitemap: {len(locs)} URLs · search-index: "
                + " · ".join(f"{k} {len(v)}" for k, v in sorted(indexed.items())))


# --------------------------------------------------------------- doc drift
def scan_docs(per_file):
    src = read("CLAUDE.md")
    m = re.search(r"Current Cards in Selected Work \((\d+) cards", src)
    real = per_file["index.html"]["cards"]
    if m and int(m.group(1)) != real:
        add("DRIFT", "docs", f"CLAUDE.md says {m.group(1)} cards in Selected Work; "
                             f"index.html has {real}. The map is behind the territory")


def main():
    only_defects = "--defects" in sys.argv
    fam = classify(html_files())
    per_file = scan_cards()
    scan_tag_buttons(per_file)
    scan_proof()
    scan_wiring()
    scan_plumbing(fam)
    scan_bilingual(fam)
    scan_links()
    scan_coverage()
    scan_docs(per_file)

    if "--json" in sys.argv:
        print(json.dumps({"findings": [{"level": l, "area": a, "message": m}
                                       for l, a, m in findings],
                          "instrument": info}, ensure_ascii=False, indent=2))
        return 1 if any(l in ("BROKEN", "DRIFT") for l, _, _ in findings) else 0

    order = ["BROKEN", "DRIFT", "GAP", "INFO"]
    if only_defects:
        order = order[:2]
    for level in order:
        rows = [(a, m) for l, a, m in findings if l == level]
        if not rows:
            print(f"\n{level}: none")
            continue
        print(f"\n{level} ({len(rows)})")
        for area, msg in sorted(rows):
            print(f"  [{area}] {msg}")

    if not only_defects:
        print("\nINSTRUMENT (a zero above is only as good as these numbers)")
        for line in info:
            print(f"  {line}")
        print("\nNot covered here — these need a browser or a human reading the page:")
        print("  Lighthouse · mobile overflow at 375px · whether copy is TRUE ·")
        print("  whether the page is any good. See CLAUDE.md.")

    return 1 if any(l in ("BROKEN", "DRIFT") for l, _, _ in findings) else 0


if __name__ == "__main__":
    sys.exit(main())
