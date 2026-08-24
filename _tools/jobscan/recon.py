#!/usr/bin/env python3
"""Find out how jobboard.fastwork.co actually serves its job listings.

    python3 _tools/jobscan/recon.py

WHY THIS EXISTS
---------------
The scanner needs one thing before any of it can be written: the real shape of
the data. Guessing produces a parser that returns an empty list forever and
reports "no new jobs" every two hours with nothing to say it is broken -- the
failure mode CLAUDE.md names under "A zero is a claim about your instrument
until you prove otherwise".

This script does not guess. It reports what is there and stops.

It is also why the scanner runs on GitHub Actions: the Claude Code sandbox's
egress proxy answers 403 to CONNECT for jobboard.fastwork.co, so this cannot
be run from there. Run it in CI (.github/workflows/jobscan-recon.yml) or on a
laptop.

WHAT IT CHECKS, IN ORDER
------------------------
1. robots.txt -- printed verbatim, then evaluated for our own User-Agent.
   If /jobs is disallowed this exits 2 and does nothing else. That is a stop
   sign, not an obstacle to route around.
2. A plain GET of /jobs -- status, type, size, and whether the markup already
   contains listings or is an empty JS shell.
3. A positive control against ph-akin.dev, which is known to have content.
   Without it, "0 job markers found" and "the HTTP layer is broken" look
   identical.
4. Only if step 2 looks JS-rendered: a headless Chromium load that logs every
   XHR/fetch the page makes, which is where the JSON endpoint will be.

Everything is printed to stdout so it can be read back out of the Actions job
log; raw bodies also land in _recon_out/ for upload as an artifact.

EXIT CODES
----------
0  recon completed, read the output
2  robots.txt disallows /jobs -- stop, and go talk to the owner
3  the page could not be fetched at all
"""
import json
import os
import re
import sys
import urllib.robotparser

import requests

BOARD = "https://jobboard.fastwork.co"
JOBS_URL = f"{BOARD}/jobs"
CONTROL_URL = "https://ph-akin.dev/"
CONTROL_MARKER = "Phakin"

# Identify honestly. A scraper that lies about what it is has already decided
# it is doing something it should not.
UA = (
    "PhakinJobScan/0.1 (+https://ph-akin.dev; personal job-alert bot; "
    "contact a0626568471@gmail.com)"
)
HEADERS = {"User-Agent": UA, "Accept-Language": "th,en;q=0.8"}
TIMEOUT = 30

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_recon_out")
OUT = os.path.normpath(OUT)


def rule(title):
    print(f"\n{'=' * 68}\n{title}\n{'=' * 68}")


def save(name, text):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"  [saved] {path} ({len(text):,} chars)")


def check_robots():
    rule("1. robots.txt")
    url = f"{BOARD}/robots.txt"
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    except Exception as exc:                                    # noqa: BLE001
        print(f"  could not fetch {url}: {exc}")
        print("  -> treating as UNKNOWN, not as permission. Stopping.")
        return False
    print(f"  GET {url} -> {r.status_code} ({len(r.text):,} chars)")
    if r.status_code == 404:
        print("  no robots.txt at all -- nothing disallows /jobs")
        return True
    print("  ---- verbatim ----")
    for line in r.text.splitlines():
        print(f"  | {line}")
    print("  ------------------")
    save("robots.txt", r.text)

    parser = urllib.robotparser.RobotFileParser()
    parser.parse(r.text.splitlines())
    for agent in (UA, "*"):
        allowed = parser.can_fetch(agent, JOBS_URL)
        print(f"  can_fetch({agent!r:20.20}...) -> {allowed}")
    ok = parser.can_fetch(UA, JOBS_URL)
    delay = parser.crawl_delay(UA) or parser.crawl_delay("*")
    if delay:
        print(f"  Crawl-delay: {delay}s -- the scan interval must respect this")
    return ok


def probe(url, label):
    rule(label)
    try:
        r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
    except Exception as exc:                                    # noqa: BLE001
        print(f"  GET {url} FAILED: {exc}")
        return None
    print(f"  GET {url}")
    print(f"  status       {r.status_code}")
    print(f"  content-type {r.headers.get('content-type')}")
    print(f"  bytes        {len(r.content):,}")
    print(f"  server       {r.headers.get('server')}")
    for h in ("last-modified", "etag", "cf-cache-status", "x-powered-by"):
        if r.headers.get(h):
            print(f"  {h:12} {r.headers[h]}")
    return r


def analyse(html):
    rule("2b. What is in that HTML?")
    print(f"  <script> tags        {len(re.findall(r'<script', html))}")
    print(f"  __NEXT_DATA__        {'__NEXT_DATA__' in html}")
    print(f"  self.__next_f (RSC)  {'__next_f' in html}")
    print(f"  __NUXT__             {'__NUXT__' in html}")

    # Does the markup already carry listings, or is it an empty shell?
    for token in ("/jobs/", "งบประมาณ", "budget", "freelance", "โพสต์", "posted"):
        print(f"  occurrences of {token!r:14} {html.count(token)}")

    api = sorted(set(re.findall(r'["\'](/api/[^"\'\s]{2,120})["\']', html)))
    nextdata = sorted(set(re.findall(r'["\']([^"\'\s]*_next/data/[^"\'\s]{2,160})["\']', html)))
    absolute = sorted(set(re.findall(r'https?://[a-z0-9.-]*(?:api|graphql)[a-z0-9.-]*\.[a-z]{2,}[^"\'\s]{0,80}', html, re.I)))
    build = re.findall(r'"buildId"\s*:\s*"([^"]+)"', html)

    print(f"\n  /api/ paths found      {len(api)}")
    for p in api[:25]:
        print(f"    {p}")
    print(f"  _next/data urls found  {len(nextdata)}")
    for p in nextdata[:10]:
        print(f"    {p}")
    print(f"  api-ish absolute urls  {len(absolute)}")
    for p in absolute[:25]:
        print(f"    {p}")
    if build:
        print(f"  buildId                {build[0]}")
        print(f"    -> try {BOARD}/_next/data/{build[0]}/jobs.json")

    # If __NEXT_DATA__ is present the whole payload may already be in the page.
    m = re.search(r'<script[^>]+id="__NEXT_DATA__"[^>]*>(.*?)</script>', html, re.S)
    if m:
        try:
            data = json.loads(m.group(1))
        except Exception as exc:                                # noqa: BLE001
            print(f"  __NEXT_DATA__ present but did not parse: {exc}")
        else:
            save("next_data.json", json.dumps(data, ensure_ascii=False, indent=2))
            print("\n  __NEXT_DATA__ parsed. Top-level keys:")
            print(f"    {list(data.keys())}")
            page_props = data.get("props", {}).get("pageProps", {})
            print(f"  pageProps keys: {list(page_props.keys())[:40]}")
            describe_arrays(page_props, "pageProps")


def describe_arrays(node, path, depth=0):
    """Print any list-of-dicts found, with the keys of its first record.

    The job list is a list of dicts somewhere in there. Rather than guess the
    field name, show every candidate and let a human pick.
    """
    if depth > 4:
        return
    if isinstance(node, dict):
        for key, value in node.items():
            describe_arrays(value, f"{path}.{key}", depth + 1)
    elif isinstance(node, list) and node and isinstance(node[0], dict):
        print(f"\n  list of {len(node)} dicts at {path}")
        print(f"    record keys: {list(node[0].keys())}")
        preview = json.dumps(node[0], ensure_ascii=False)[:600]
        print(f"    first record: {preview}")


def browser_probe():
    rule("4. Headless Chromium -- what does the page actually request?")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  playwright not installed; skipping (pip install playwright)")
        return

    seen = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(user_agent=UA, locale="th-TH")

        def on_response(resp):
            ctype = (resp.headers or {}).get("content-type", "")
            if "json" in ctype or "graphql" in resp.url:
                seen.append((resp.status, resp.request.method, resp.url, ctype))

        page.on("response", on_response)
        page.goto(JOBS_URL, wait_until="networkidle", timeout=90_000)
        page.wait_for_timeout(3000)
        html = page.content()
        save("rendered.html", html)
        text = page.inner_text("body")
        print(f"  rendered body text: {len(text):,} chars")
        anchors = page.query_selector_all("a[href*='/jobs/']")
        print(f"  anchors to /jobs/:  {len(anchors)}")
        print("  ---- first 800 chars of rendered text ----")
        print("  " + text[:800].replace("\n", "\n  "))
        print("  ------------------------------------------")

        print(f"\n  JSON responses observed: {len(seen)}")
        for status, method, url, ctype in seen:
            print(f"    {status} {method} {url[:150]}")

        # Re-fetch the most promising ones inside the browser context so any
        # auth header or cookie the app sets is carried along.
        for status, method, url, _ in seen:
            if status == 200 and method == "GET" and re.search(r"job|search|list|feed", url, re.I):
                try:
                    body = page.evaluate(
                        "u => fetch(u).then(r => r.text())", url
                    )
                except Exception as exc:                        # noqa: BLE001
                    print(f"    re-fetch {url[:80]} failed: {exc}")
                    continue
                name = re.sub(r"[^a-z0-9]+", "-", url.lower())[-60:] + ".json"
                save(name, body)
                try:
                    describe_arrays(json.loads(body), url.split("?")[0].split("/")[-1])
                except Exception:                               # noqa: BLE001
                    pass
        browser.close()


def main():
    print(f"User-Agent: {UA}")

    if not check_robots():
        print("\nSTOP: robots.txt does not allow this path for this agent.")
        print("Report it to the owner rather than working around it.")
        return 2

    control = probe(CONTROL_URL, "2a. Positive control (ph-akin.dev)")
    if control is None or CONTROL_MARKER not in control.text:
        print(f"  !! control page missing {CONTROL_MARKER!r} -- the HTTP layer")
        print("     itself is suspect. Do not trust any zero measured below.")
    else:
        print(f"  control OK: found {CONTROL_MARKER!r}, {len(control.text):,} chars")

    r = probe(JOBS_URL, "2. GET /jobs (no browser)")
    if r is None:
        return 3
    save("jobs-raw.html", r.text)
    analyse(r.text)

    browser_probe()

    rule("done")
    print("Read the two sections above and pick ONE source for fetch.py:")
    print("  * a JSON endpoint  -> best; plain requests, no browser in CI")
    print("  * __NEXT_DATA__    -> good; one GET, parse the embedded payload")
    print("  * rendered HTML    -> last resort; Playwright on every scan")
    return 0


if __name__ == "__main__":
    sys.exit(main())
