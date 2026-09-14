#!/usr/bin/env python3
"""Fail when a project's one-line blurb drifts between the files that repeat it.

    python3 _tools/check-copy.py

Every project blurb on this site is written in more than one place. Measured
2026-08-12: 63 distinct strings repeated across 203 locations in 84 files, one
of them in 7 files at once. That duplication is not a style problem, it is the
direct cause of two shipped defects:

  * BuildNest advertised "hand-drawn SVG architecture graphics instead of stock
    photography" in 23 strings across 13 files, for six days after the page was
    rebuilt around photographs.
  * BookEase and ElevateCommerce advertised a Node/Express backend that never
    existed, in 37 strings across 13 files.

Both were fixed by grepping. Both times the grep missed strings that said the
same thing in different words, and the miss was only caught by a second sweep.
This script exists so the third one is caught by a command instead.

`_content/project-copy.json` holds the canonical text per project, per
language, per role:

    long   the .work-problem text on a card (index, work), and the #related
           strip on category and industry pages
    short  the #related strip on showcase pages, which is deliberately tighter

Both files are underscore-prefixed so Jekyll never serves them -- see
CLAUDE.md, "What is public and what is not".

This checks that repeated copy agrees with itself. It cannot tell you the copy
is TRUE; that needs reading the page it describes. See CLAUDE.md, "A showcase
page describes a demo page, and nothing re-reads it when that demo is
redesigned."
"""
import collections
import glob
import io
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

# Parsed over the whole file, never line by line. The first version matched
# `^\s*<span>...</span>\s*$`, which requires the blurb to sit alone on its own
# line -- true of most pages and false of a minified one. showcase-signalform and
# its -en twin are emitted on single lines, so six blurbs there were invisible and
# the script still printed "all repeated copy agrees". A checker that cannot see a
# page is indistinguishable from a page with nothing wrong: CLAUDE.md, "A zero is
# a claim about your instrument until you prove otherwise."
ANCHOR = re.compile(r'<a\s[^>]*class="(?:project-link|work-thumb)[^"]*"[^>]*>'
                    r'|<a\s[^>]*class="[^"]*\b(?:project-link|work-thumb)\b[^"]*"[^>]*>')
HREF = re.compile(r'href="([^"]+)"')
SPAN = re.compile(r'<span>([^<]{25,})</span>')
PROB = re.compile(r'<p class="work-problem">([^<]+)</p>')


def occurrences():
    """Yield (slug, lang, role, file, line, text) for every repeated blurb."""
    for f in sorted(glob.glob('*.html')):
        lang = 'en' if f.endswith('-en.html') else 'th'
        src = io.open(f, encoding='utf-8').read()
        starts = [0] + [m.end() for m in re.finditer(r'\n', src)]

        def line_of(pos):
            lo, hi = 0, len(starts) - 1
            while lo < hi:
                mid = (lo + hi + 1) // 2
                if starts[mid] <= pos:
                    lo = mid
                else:
                    hi = mid - 1
            return lo + 1

        # One pass over the anchors and .work-problem blurbs in document order.
        # A blurb belongs to the nearest preceding anchor, which is what the
        # line-based version approximated with its `slug = None` reset.
        events = []
        for m in ANCHOR.finditer(src):
            href = HREF.search(m.group(0))
            if not href or re.match(r'(?:https?:)?//|mailto:', href.group(1)):
                continue                       # external repo/profile link, not a project card
            events.append((m.start(), 'anchor', re.sub(r'-en$', '', href.group(1))))
        for m in SPAN.finditer(src):
            events.append((m.start(), 'short', m.group(1)))
        for m in PROB.finditer(src):
            events.append((m.start(), 'long', m.group(1)))
        events.sort()

        slug = None
        for pos, kind, value in events:
            if kind == 'anchor':
                slug = value
                continue
            if not slug:
                continue
            role = 'short' if (kind == 'short' and f.startswith('showcase-')) else 'long'
            yield slug, lang, role, f, line_of(pos), ' '.join(value.split())
            slug = None


canon = json.load(io.open('_content/project-copy.json', encoding='utf-8'))['projects']

drift, unknown, seen = [], [], collections.Counter()
for slug, lang, role, f, i, text in occurrences():
    want = canon.get(slug, {}).get(lang, {}).get(role)
    if want is None:
        unknown.append((slug, lang, role, f, i))
        continue
    seen[(slug, lang, role)] += 1
    if text != want:
        drift.append((slug, lang, role, f, i, text, want))

# A blurb that stopped being repeated is worth knowing about too: the canonical
# entry is now unverifiable, and the next edit has nothing to check it against.
orphan = [(slug, lang, role)
          for slug, langs in canon.items()
          for lang, roles in langs.items()
          for role in roles
          if seen[(slug, lang, role)] == 0]

print('checked %d occurrences across %d projects'
      % (sum(seen.values()), len({s for s, _, _ in seen})))

if drift:
    print('\n%d blurb(s) disagree with _content/project-copy.json:\n' % len(drift))
    for slug, lang, role, f, i, text, want in drift:
        print('  %s:%d  [%s %s/%s]' % (f, i, slug, lang, role))
        print('     is:     %s' % text)
        print('     canon:  %s\n' % want)
    print('Fix the page, or update the canonical entry if the new wording is')
    print('the one you want -- then make every other copy match it.')

if unknown:
    print('\n%d blurb(s) have no canonical entry:' % len(unknown))
    for slug, lang, role, f, i in unknown:
        print('   %s:%d  %s [%s/%s]' % (f, i, slug, lang, role))
    print('Add them to _content/project-copy.json, or they are unguarded.')

if orphan:
    print('\n%d canonical entr(ies) are no longer used by any page:' % len(orphan))
    for slug, lang, role in orphan:
        print('   %s [%s/%s]' % (slug, lang, role))

if drift or unknown:
    sys.exit(1)
print('\nall repeated copy agrees')
