#!/usr/bin/env python3
"""Rewrite every <lastmod> in sitemap.xml from git's last commit per page.

Run after any change that touches page content:

    python3 _tools/sitemap-lastmod.py

Dates come from `git log -1 --format=%cs -- <file>`, not from today's date.
Google ignores lastmod it judges unreliable, and stamping all 79 URLs with the
same date every deploy is exactly the pattern that earns that judgement. A URL
whose page has not been committed since 2026-08-06 says 2026-08-06.

<loc> values are extensionless (see CLAUDE.md, "URLs carry no .html"), so each
one is mapped back to its file: "/" -> index.html, "/foo" -> foo.html. A <loc>
that ends in "/" is a built app served from its own folder, not a page --
"/signalform-studio/" -> the signalform-studio directory, which `git log`
accepts as a path. Without that case it became "signalform-studio/.html", the
URL was skipped every run, and its <lastmod> silently stopped tracking the
commits that changed it.

Lives under `_tools/` so Jekyll skips it.
"""
import os, re, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SITE = 'https://ph-akin.dev'
os.chdir(ROOT)


def page_file(loc):
    path = loc[len(SITE):].split('#')[0].split('?')[0].lstrip('/')
    if path == '':
        return 'index.html'
    if path.endswith('/'):
        return path.rstrip('/')     # a built app served from its own folder
    return path if path.endswith('.html') else path + '.html'


def committed(path):
    out = subprocess.run(['git', 'log', '-1', '--format=%cs', '--', path],
                         capture_output=True, text=True).stdout.strip()
    return out or None


src = open('sitemap.xml', encoding='utf-8').read()
missing, stamped, dates = [], 0, {}

def fix(m):
    global stamped
    block, loc = m.group(0), m.group(1).strip()
    f = page_file(loc)
    if not os.path.exists(f):
        missing.append((loc, f))
        return block
    d = committed(f)
    if not d:
        missing.append((loc, f + ' (ไม่มีใน git)'))
        return block
    dates[d] = dates.get(d, 0) + 1
    stamped += 1
    block = re.sub(r'\n?\s*<lastmod>[^<]*</lastmod>', '', block)      # ของเดิมถ้ามี
    return block.replace('</loc>', '</loc>\n    <lastmod>%s</lastmod>' % d, 1)

out = re.sub(r'<url>\s*<loc>\s*([^<]+?)\s*</loc>[\s\S]*?</url>', fix, src)
open('sitemap.xml', 'w', encoding='utf-8').write(out)

print('ใส่ <lastmod> แล้ว %d URL' % stamped)
for d in sorted(dates, reverse=True):
    print('  %s  %d URL' % (d, dates[d]))
if missing:
    print('\n⚠ ข้ามไป %d รายการ:' % len(missing))
    for loc, f in missing:
        print('   %-50s → %s' % (loc, f))
    sys.exit(1)
