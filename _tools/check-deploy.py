#!/usr/bin/env python3
"""Pre-deploy check: does anything on its way out need a ?v= bump?

    python3 _tools/check-deploy.py

Compares everything you are about to push (commits + working tree) against
origin/main and fails if a versioned asset changed without its ?v= token
moving with it.

WHY THIS EXISTS
---------------
Every stylesheet and script on this site is referenced with a ?v= token:

    <link rel="stylesheet" href="assets/home-shell.css?v=merged-band">

GitHub Pages serves those with a long cache lifetime. A returning visitor
holds the old copy. If the HTML changes to depend on a rule that only exists
in the new copy, that visitor gets new markup paired with the old asset, and
the page renders wrong for them alone — never for you, because your checkout
is warm. Nothing errors. Nothing shows up in Lighthouse.

The condition is not "did I touch a script". It is:

    a versioned asset changed  AND  its ?v= token did not

That is what this script checks, because a human reading a diff reliably gets
it wrong: the rule had been written up around self-rendering scripts, so a
change to a plain stylesheet read as exempt, and shipped unbumped.

EXIT CODES
----------
0  nothing to bump
1  something needs bumping (message says what)
"""
import re
import subprocess
import sys
from collections import defaultdict

BASE = "origin/main"
ASSET = re.compile(r"^assets/.+\.(css|js)$")


def sh(*args):
    return subprocess.run(args, capture_output=True, text=True).stdout


def changed_files():
    """Everything different from BASE: committed, staged and unstaged."""
    out = set()
    for cmd in (["git", "diff", "--name-only", BASE],
                ["git", "diff", "--name-only"],
                ["git", "diff", "--name-only", "--cached"]):
        out.update(f for f in sh(*cmd).splitlines() if f)
    return out


def token_for(asset, ref=None):
    """The ?v= token each HTML file uses for this asset, as a set."""
    name = asset.split("/")[-1]
    pat = re.compile(re.escape(name) + r"\?v=([A-Za-z0-9._-]+)")
    tokens = set()
    if ref is None:
        blob = sh("git", "grep", "-h", "-o", "-E",
                  re.escape(name) + r"\?v=[A-Za-z0-9._-]+", "--", "*.html")
        if not blob:  # not yet committed anywhere; read the working tree
            blob = sh("bash", "-c",
                      f"grep -ho -E '{re.escape(name)}\\?v=[A-Za-z0-9._-]+' *.html")
    else:
        blob = sh("git", "grep", "-h", "-o", "-E",
                  re.escape(name) + r"\?v=[A-Za-z0-9._-]+", ref, "--", "*.html")
    for line in blob.splitlines():
        m = pat.search(line)
        if m:
            tokens.add(m.group(1))
    return tokens



def refs_for(asset):
    """(with-token, without-token) counts of real src=/href= references.

    `token_for` only sees `name?v=...`, so a reference with no token at all is
    invisible to it — and that is the one reference that can never be fixed after
    the fact. An asset loaded bare is cached by URL forever: editing it changes
    nothing for anyone who has already been to the site.
    """
    name = asset.split("/")[-1]
    pat = re.compile(r'(?:src|href)="(?:\./)?(?:assets/)?'
                     + re.escape(name) + r'(\?v=[A-Za-z0-9._-]+)?"')
    with_tok, without = 0, []
    for f in sh("git", "ls-files", "*.html").splitlines():
        # Jekyll skips underscore-prefixed paths, so assets/_archive/*.html and
        # friends are 404 and cannot strand anyone on a cached asset.
        if any(seg.startswith("_") for seg in f.split("/")):
            continue
        try:
            body = open(f, encoding="utf-8").read()
        except OSError:
            continue
        for m in pat.finditer(body):
            if m.group(1):
                with_tok += 1
            else:
                without.append(f)
    return with_tok, without


def main():
    if not sh("git", "rev-parse", "--verify", BASE).strip():
        print(f"! cannot resolve {BASE} — run `git fetch origin` first")
        return 1

    files = changed_files()
    if not files:
        print("nothing differs from origin/main")
        return 0

    assets = sorted(f for f in files if ASSET.match(f))
    html = sorted(f for f in files if f.endswith(".html"))

    # A split token is worse than a stale one: half the visitors get one build
    # of the asset and half get the other, and neither half is wrong enough to
    # notice. Same for a bare reference, which can never be fixed after the fact.
    # Both are checked for every versioned asset, not just the changed ones,
    # because both are introduced by a page being added rather than by the asset
    # being edited — which is why this sweep runs BEFORE the "nothing changed"
    # exit. It used to sit after it, so the sweep its own comment promised was
    # skipped on every run where no asset happened to change.
    split, bare = [], []
    for a in sorted(set(ASSET.match(f).string for f in sh("git", "ls-files").splitlines()
                        if ASSET.match(f))):
        toks = token_for(a)
        if len(toks) > 1:
            split.append((a, sorted(toks)))
        with_tok, without = refs_for(a)
        if without:
            bare.append((a, with_tok, without))

    if not assets and not split and not bare:
        print(f"no versioned asset changed ({len(html)} HTML file(s) only) — nothing to bump")
        return 0

    problems = []
    for a in assets:
        now, before = token_for(a), token_for(a, BASE)
        if not before and not now:
            continue  # no token anywhere — reported by the `bare` check below
        if now == before:
            refs = len([f for f in sh("bash", "-c",
                        f"grep -l '{a.split('/')[-1]}?v=' *.html").splitlines()])
            problems.append((a, sorted(now) or ["(none)"], refs))

    if bare:
        print("STOP — referenced with no ?v= token at all:\n")
        for a, with_tok, without in bare:
            shown = ", ".join(sorted(set(without))[:4])
            more = f" (+{len(set(without)) - 4} more)" if len(set(without)) > 4 else ""
            print(f"  {a}")
            print(f"    {len(without)} bare reference(s) in {shown}{more}"
                  + (f"  ·  {with_tok} other reference(s) DO carry one" if with_tok else ""))
        print("\nA bare reference is cached by URL forever: editing the asset changes")
        print("nothing for anyone who has already visited. Give every reference a token")
        print("now, while it still costs one edit:\n")
        for a, with_tok, _ in bare:
            name = a.split("/")[-1]
            tok = (sorted(token_for(a)) or ["1"])[0]
            print(f"  sed -i 's|{name}\"|{name}?v={tok}\"|g' *.html   # then verify")
        return 1

    if split:
        print("STOP — one asset, more than one ?v= token:\n")
        for a, toks in split:
            print(f"  {a}")
            print(f"    {' vs '.join(toks)}")
        print("\nHalf your visitors get one build of it and half get the other.")
        print("Every reference moves together or not at all.")
        return 1

    if not problems:
        print("all changed assets have a moved ?v= token — good to ship")
        return 0

    print("STOP — these changed but their ?v= token did not:\n")
    for a, tok, refs in problems:
        print(f"  {a}")
        print(f"    still ?v={tok[0]}  ·  referenced by {refs} HTML file(s)")
    print("\nA returning visitor will pair the new HTML with their cached copy.")
    print("Bump every reference together, e.g.:\n")
    for a, tok, _ in problems:
        name = a.split("/")[-1]
        print(f"  sed -i '' 's|{name}?v={tok[0]}|{name}?v=<new-token>|g' *.html")
    return 1


if __name__ == "__main__":
    sys.exit(main())
