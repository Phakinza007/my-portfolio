#!/usr/bin/env python3
"""What the scanner remembers between runs.

Two files, both on the orphan branch `jobscan-state` rather than `main`:

  seen.json          job id -> ISO timestamp it was first seen
  jobs/YYYY-MM.jsonl one normalized record per line, appended, never rewritten

`main` auto-deploys to GitHub Pages on every commit, so writing state there
would redeploy the site seven times a day with nothing changed on it. A
separate branch does not trigger Pages and keeps the site's history readable.

The jsonl archive is not required for dedupe -- seen.json alone does that. It
is kept because the scoring rules will change (and because the proposal
drafting in Phase 6 needs real posts to work from), and re-scoring history
should never mean re-fetching the board.
"""
import json
import os
from datetime import datetime, timezone


def _seen_path(state_dir):
    return os.path.join(state_dir, "seen.json")


def load_seen(state_dir):
    path = _seen_path(state_dir)
    if not os.path.exists(path):
        return {}
    with open(path, encoding="utf-8") as fh:
        try:
            return json.load(fh)
        except json.JSONDecodeError:
            # A truncated state file must not silently become an empty one --
            # that would re-notify every job on the board.
            raise SystemExit(f"{path} exists but is not valid JSON; refusing to overwrite it")


def save_seen(state_dir, seen):
    os.makedirs(state_dir, exist_ok=True)
    path = _seen_path(state_dir)
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as fh:
        json.dump(seen, fh, ensure_ascii=False, indent=1, sort_keys=True)
        fh.write("\n")
    os.replace(tmp, path)                      # atomic; a killed run leaves the old file


def split_new(jobs, seen):
    """Return (new_jobs, updated_seen). Order of `jobs` is preserved."""
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    updated = dict(seen)
    fresh = []
    for job in jobs:
        job_id = str(job.get("id") or job.get("url") or "")
        if not job_id:
            continue
        if job_id in updated:
            continue
        updated[job_id] = now
        fresh.append(job)
    return fresh, updated


def archive(state_dir, jobs):
    """Append this run's records to the month's jsonl file."""
    if not jobs:
        return None
    month = datetime.now(timezone.utc).strftime("%Y-%m")
    folder = os.path.join(state_dir, "jobs")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{month}.jsonl")
    with open(path, "a", encoding="utf-8") as fh:
        for job in jobs:
            fh.write(json.dumps(job, ensure_ascii=False) + "\n")
    return path
