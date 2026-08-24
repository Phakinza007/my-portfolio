#!/usr/bin/env python3
"""Pull the web-category jobs off jobboard-api.fastwork.co.

Everything here was measured by _tools/jobscan/recon.py on 2026-08-24, not
guessed. What it found:

  * The page at jobboard.fastwork.co/jobs is a Next.js shell -- its
    __NEXT_DATA__ carries only i18n -- and the listings come from a separate
    host, jobboard-api.fastwork.co, which answers a plain HTTP client with no
    auth, no cookie and no browser. So no Chromium in CI.
  * robots.txt on the board is "Allow: /", disallowing only /me/ and /en/.
  * `filters[0][field]=tag_id` filters server-side and really works: the web
    tag returned total_count 42 with every record carrying that tag. The
    other spellings (tag, tag_ids, tag.id, tag_name) all answer HTTP 400.
    That 42 against the board's ~3,000 open posts is the whole reason a scan
    is two requests instead of sixty pages.
  * A job's page is /jobs?job_id=<uuid>. The obvious /jobs/<uuid> is a 404.

🔴 The API returned HTTP 500 to *unfiltered* queries during recon, minutes
after the identical request had returned 200. So: always filter, and treat 5xx
as "retry", never as "no jobs". An empty result from a flaky upstream reported
as "nothing new" is the failure this whole tool is built to avoid.
"""
import json
import os
import time

import requests

API = "https://jobboard-api.fastwork.co/api"
BOARD = "https://jobboard.fastwork.co"

UA = (
    "PhakinJobScan/0.1 (+https://ph-akin.dev; personal job-alert bot; "
    "contact a0626568471@gmail.com)"
)
HEADERS = {"User-Agent": UA, "Accept": "application/json", "Accept-Language": "th,en;q=0.8"}

TIMEOUT = 30
RETRIES = 3
PAUSE = 1.2          # between requests, so a scan is a trickle and not a burst

HERE = os.path.dirname(os.path.abspath(__file__))


def job_url(job_id):
    """The page a human opens. Measured -- /jobs/<id> is a 404."""
    return f"{BOARD}/jobs?job_id={job_id}"


def _get(path, params=None):
    """GET with backoff on 5xx and on transport errors.

    A 4xx is not retried: it means the request is wrong, and repeating a wrong
    request is just noise on someone else's server.
    """
    last = None
    for attempt in range(1, RETRIES + 1):
        try:
            r = requests.get(f"{API}{path}", params=params, headers=HEADERS, timeout=TIMEOUT)
        except requests.RequestException as exc:
            last = f"transport error: {exc}"
        else:
            if r.status_code < 400:
                return r.json()
            last = f"HTTP {r.status_code}: {r.text[:200]}"
            if r.status_code < 500:
                break
        if attempt < RETRIES:
            time.sleep(2 ** attempt)
    raise RuntimeError(f"{path} failed after {attempt} attempt(s) -- {last}")


def list_tags():
    """[{id, name, sort}] -- 24 of them as of 2026-08-24."""
    return _get("/tags").get("data") or []


def resolve_tag_ids(profile, tags=None):
    """Turn the tag names in profile.json into the ids the API filters on.

    Names are resolved at runtime rather than hardcoded, because a renamed or
    re-issued tag would otherwise silently filter to nothing. Anything that
    fails to resolve is returned so the caller can say so out loud.
    """
    wanted = profile.get("categories") or []
    tags = tags if tags is not None else list_tags()
    by_name = {t["name"]: t["id"] for t in tags}
    resolved = [(name, by_name[name]) for name in wanted if name in by_name]
    missing = [name for name in wanted if name not in by_name]
    return resolved, missing, tags


def fetch_tag(tag_id, page_size=50, max_pages=2):
    """Newest-first jobs carrying one tag.

    Two pages of 50 is ~100 posts per category. The web category holds 42 open
    posts in total, so one page already covers it; the second exists so a busy
    day cannot silently truncate. It stops as soon as a page is short.
    """
    out = []
    for page in range(1, max_pages + 1):
        payload = _get("/jobs", {
            "page": page,
            "page_size": page_size,
            "order_by[]": "inserted_at",
            "order_directions[]": "desc",
            "filters[0][field]": "tag_id",
            "filters[0][value]": tag_id,
        })
        rows = payload.get("data") or []
        out.extend(rows)
        meta = payload.get("meta") or {}
        if len(rows) < page_size or page >= (meta.get("total_pages") or 1):
            break
        time.sleep(PAUSE)
    return out


def fetch_jobs(profile=None, limit=None):
    """Every open job in the configured categories, normalized, newest first."""
    import normalize
    import score as scoring

    profile = profile or scoring.load_profile()
    resolved, missing, all_tags = resolve_tag_ids(profile)

    print(f"tags on the board: {len(all_tags)}")
    if missing:
        # Loud, because a mistyped category is indistinguishable from a quiet
        # week otherwise.
        print(f"!! these categories in profile.json match no tag: {missing}")
        print(f"   available: {sorted(t['name'] for t in all_tags)}")
    if not resolved:
        raise RuntimeError(
            "no category in profile.json resolved to a tag id -- refusing to "
            "scan the whole board"
        )

    seen_ids = set()
    jobs = []
    for name, tag_id in resolved:
        time.sleep(PAUSE)
        rows = fetch_tag(tag_id)
        fresh = [r for r in rows if r.get("id") not in seen_ids]
        seen_ids.update(r.get("id") for r in fresh)
        print(f"  {name:<24} {len(rows):>3} posts ({len(fresh)} not already seen this run)")
        jobs.extend(fresh)

    jobs = [normalize.normalize(row) for row in jobs]
    jobs.sort(key=lambda j: j.get("posted_at") or "", reverse=True)
    return jobs[:limit] if limit else jobs


def save_fixture(path, jobs):
    # git does not track empty directories, so fixtures/ does not exist in a
    # fresh checkout even though it exists here.
    parent = os.path.dirname(os.path.abspath(path))
    os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump({"jobs": jobs}, fh, ensure_ascii=False, indent=1)
        fh.write("\n")
    return path
