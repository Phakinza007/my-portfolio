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

    # Every wait here is bounded. The first version used wait_until="networkidle"
    # and an unbounded page.evaluate(fetch), and hung until the job timeout on a
    # page that polls -- networkidle never arrives, and a fetch that never
    # settles has no deadline of its own. A recon that cannot finish tells you
    # nothing.
    seen = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(user_agent=UA, locale="th-TH")
        page.set_default_timeout(20_000)

        def on_response(resp):
            ctype = (resp.headers or {}).get("content-type", "")
            if "json" in ctype or "graphql" in resp.url:
                seen.append((resp.status, resp.request.method, resp.url, ctype))

        page.on("response", on_response)
        try:
            page.goto(JOBS_URL, wait_until="domcontentloaded", timeout=45_000)
        except Exception as exc:                                # noqa: BLE001
            print(f"  goto failed: {exc}")
            browser.close()
            return
        page.wait_for_timeout(8000)          # let the client-side fetches land

        html = page.content()
        save("rendered.html", html)
        text = page.inner_text("body")
        anchors = page.query_selector_all("a[href*='/jobs/']")
        print(f"  rendered body text: {len(text):,} chars")
        print(f"  anchors to /jobs/:  {len(anchors)}")
        for a in anchors[:8]:
            print(f"    {a.get_attribute('href')}  |  {(a.inner_text() or '')[:70]}")
        print("  ---- first 1200 chars of rendered text ----")
        print("  " + text[:1200].replace("\n", "\n  "))
        print("  ------------------------------------------")

        print(f"\n  JSON responses observed: {len(seen)}")
        for status, method, url, ctype in seen:
            print(f"    {status} {method} {url[:150]}")

        # Re-fetch the most promising few inside the page context, so any
        # header or cookie the app sets is carried along. Capped, and each with
        # its own deadline on the JS side.
        candidates = [
            (s_, m, u) for (s_, m, u, _) in seen
            if s_ == 200 and m == "GET" and re.search(r"job|search|list|feed|post", u, re.I)
        ][:6]
        print(f"\n  re-fetching {len(candidates)} candidate endpoint(s)")
        for _, _, url in candidates:
            try:
                body = page.evaluate(
                    """async (u) => {
                        const c = new AbortController();
                        const t = setTimeout(() => c.abort(), 15000);
                        try { const r = await fetch(u, {signal: c.signal}); return await r.text(); }
                        finally { clearTimeout(t); }
                    }""",
                    url,
                )
            except Exception as exc:                            # noqa: BLE001
                print(f"    re-fetch failed {url[:90]}: {str(exc)[:120]}")
                continue
            name = re.sub(r"[^a-z0-9]+", "-", url.lower())[-60:] + ".json"
            save(name, body)
            try:
                describe_arrays(json.loads(body), url.split("?")[0].split("/")[-1])
            except Exception:                                   # noqa: BLE001
                print("    (body is not JSON we could walk)")
        browser.close()


API = "https://jobboard-api.fastwork.co/api"


def api_probe():
    """Hit the API the page itself calls, with plain requests and no browser.

    This is the whole question for fetch.py: if these two calls work from a
    bare HTTP client, the scanner needs no Chromium in CI at all -- 13 seconds
    and 184 MB of browser download per run go away.
    """
    rule("5. jobboard-api.fastwork.co -- does it answer a plain client?")

    for path in ("/robots.txt",):
        try:
            r = requests.get("https://jobboard-api.fastwork.co" + path,
                             headers=HEADERS, timeout=TIMEOUT)
            print(f"  GET api{path} -> {r.status_code}")
            if r.status_code == 200:
                for line in r.text.splitlines()[:12]:
                    print(f"    | {line}")
        except Exception as exc:                                # noqa: BLE001
            print(f"  GET api{path} failed: {exc}")

    # --- tags: the category axis the scan will filter on -------------------
    try:
        r = requests.get(f"{API}/tags", headers=HEADERS, timeout=TIMEOUT)
        print(f"\n  GET /api/tags -> {r.status_code} ({len(r.content):,} bytes)")
        tags = r.json()
        save("api-tags.json", json.dumps(tags, ensure_ascii=False, indent=2))
        rows = tags.get("data", tags) if isinstance(tags, dict) else tags
        print(f"  {len(rows)} tags, ALL of them:")
        for t in sorted(rows, key=lambda x: x.get("sort", 999)):
            print(f"    sort={t.get('sort'):>3}  {t.get('name')}   ({t.get('id')})")
    except Exception as exc:                                    # noqa: BLE001
        print(f"  /api/tags failed: {exc}")

    # --- jobs: shape, pagination, and one full record ----------------------
    variants = {
        "kind=standard": {
            "page": 1, "page_size": 5,
            "order_by[]": "inserted_at", "order_directions[]": "desc",
            "filters[0][field]": "kind", "filters[0][value]": "standard",
        },
        "no kind filter": {
            "page": 1, "page_size": 5,
            "order_by[]": "inserted_at", "order_directions[]": "desc",
        },
    }
    for label, params in variants.items():
        try:
            r = requests.get(f"{API}/jobs", params=params, headers=HEADERS, timeout=TIMEOUT)
        except Exception as exc:                                # noqa: BLE001
            print(f"\n  /api/jobs [{label}] failed: {exc}")
            continue
        print(f"\n  GET /api/jobs [{label}] -> {r.status_code} ({len(r.content):,} bytes)")
        print(f"    url: {r.url}")
        if r.status_code != 200:
            print(f"    body: {r.text[:300]}")
            continue
        payload = r.json()
        save(f"api-jobs-{label.replace(' ', '-').replace('=', '-')}.json",
             json.dumps(payload, ensure_ascii=False, indent=2))
        print(f"    top-level keys: {list(payload.keys())}")
        for key, value in payload.items():
            if key != "data":
                print(f"    {key}: {json.dumps(value, ensure_ascii=False)[:200]}")
        rows = payload.get("data") or []
        print(f"    {len(rows)} records; kinds seen: "
              f"{sorted({row.get('kind') for row in rows})}; "
              f"tags seen: {sorted({(row.get('tag') or {}).get('name') for row in rows})}")

    # One complete record, so normalize.py is written against real fields and
    # not against a truncated preview.
    try:
        r = requests.get(f"{API}/jobs", headers=HEADERS, timeout=TIMEOUT, params={
            "page": 1, "page_size": 1,
            "order_by[]": "inserted_at", "order_directions[]": "desc",
        })
        row = (r.json().get("data") or [{}])[0]
        print("\n  ---- one complete record ----")
        print(json.dumps(row, ensure_ascii=False, indent=2)[:4000])
        print("  -----------------------------")
    except Exception as exc:                                    # noqa: BLE001
        print(f"  single-record probe failed: {exc}")


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

    # browser_probe() answered its question on 2026-08-24 -- it found the two
    # API endpoints below, and re-running it costs a 184 MB Chromium download
    # for output nobody reads. Kept in the file, off by default: set
    # JOBSCAN_RECON_BROWSER=1 if the API ever stops being the source.
    if os.environ.get("JOBSCAN_RECON_BROWSER") == "1":
        browser_probe()
    api_probe()

    rule("done")
    print("Read the two sections above and pick ONE source for fetch.py:")
    print("  * a JSON endpoint  -> best; plain requests, no browser in CI")
    print("  * __NEXT_DATA__    -> good; one GET, parse the embedded payload")
    print("  * rendered HTML    -> last resort; Playwright on every scan")
    return 0


if __name__ == "__main__":
    sys.exit(main())
