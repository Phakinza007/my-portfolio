#!/usr/bin/env python3
"""Deliver the digest of new jobs.

Two channels, both optional at runtime and both skipping themselves quietly
when unconfigured -- so the scan still runs and still records state even if a
webhook is missing or a token has expired. A notifier that takes the whole
scan down with it turns a delivery problem into a data problem.

  github  one issue per scan that found new jobs. No secret to set up:
          Actions' own GITHUB_TOKEN is enough, and the GitHub mobile app
          already pushes issue notifications.
  discord one message, top N only, when DISCORD_WEBHOOK_URL is set.

Both return a status string; scan.py prints them so the job log says what
actually went out.
"""
import json
import os
from datetime import datetime, timedelta, timezone

import requests

TIMEOUT = 20
DISCORD_LIMIT = 2000          # hard limit imposed by Discord
DISCORD_TOP_N = 5

BANGKOK = timezone(timedelta(hours=7))
THAI_MONTHS = [
    "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.", "พ.ค.", "มิ.ย.",
    "ก.ค.", "ส.ค.", "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค.",
]


def thai_stamp(dt):
    """A UTC-aware datetime, rendered as a Thai calendar date in Bangkok time.

    scan.py's issue title uses the same format for "now" -- kept here as the
    one definition so the two never drift apart.
    """
    local = dt.astimezone(BANGKOK)
    return f"{local.day} {THAI_MONTHS[local.month - 1]} {local.strftime('%H:%M')}"

FLAG_LABELS = {
    "needs_backend": "⚠ ต้องมีหลังบ้าน",
    "off_lane": "⚠ คนละสาย",
    "below_floor": "⚠ งบต่ำกว่า ฿3,900",
}


def _budget(job):
    text = job.get("budget_text")
    if text:
        return text
    lo, hi = job.get("budget_min"), job.get("budget_max")
    if lo and hi:
        return f"฿{lo:,.0f}–{hi:,.0f}"
    if hi:
        return f"≤ ฿{hi:,.0f}"
    if lo:
        return f"≥ ฿{lo:,.0f}"
    return "—"


def _flags(job):
    return " ".join(FLAG_LABELS.get(f, f) for f in job.get("flags", []))


def _age(job):
    """When the post went up, in Thai -- calendar date plus how long ago.

    Relative age alone ("2 ชม.") is computed at scan time and then frozen into
    the GitHub issue text forever; read the issue a day later and it still
    says "2 ชม.", which by then is wrong. The calendar date is what stays
    correct no matter when it's read; the relative part is a convenience on
    top of it, not a replacement for it.
    """
    stamp = job.get("posted_at")
    if not stamp:
        return "—"
    try:
        posted = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
    except ValueError:
        return "—"
    minutes = (datetime.now(timezone.utc) - posted).total_seconds() / 60
    if minutes < 60:
        relative = f"{minutes:.0f} นาทีที่แล้ว"
    elif minutes < 60 * 24:
        relative = f"{minutes / 60:.0f} ชม.ที่แล้ว"
    else:
        relative = f"{minutes / 1440:.0f} วันที่แล้ว"
    return f"{thai_stamp(posted)} ({relative})"


def _offers(job):
    """Applicants already in. 27 offers is a lottery; 0 an hour old is not."""
    n = job.get("offers")
    return "—" if n is None else f"{n}"


def render_markdown(new_jobs, total_seen):
    """The GitHub Issue body: a table, best fit first, reasons included."""
    lines = [
        f"พบงานใหม่ **{len(new_jobs)}** รายการ (บอร์ดมีทั้งหมด {total_seen} รายการในรอบนี้)",
        "",
        "เรียงตามความเข้ากับงานที่ส่งมอบได้ — คะแนนไม่ได้กรองงานทิ้ง "
        "ทุกงานในรอบนี้อยู่ในตารางครบ",
        "",
        "| # | งาน | หมวด | งบ | ยื่นแล้ว | โพสต์เมื่อ | ความเข้า | หมายเหตุ |",
        "|--:|-----|------|----|--------:|-----------|----------|----------|",
    ]
    for i, job in enumerate(new_jobs, 1):
        title = (job.get("title") or "(ไม่มีชื่อ)").replace("|", "\\|")
        url = job.get("url") or ""
        link = f"[{title}]({url})" if url else title
        flags = _flags(job)
        lines.append(
            f"| {i} | {link} | {job.get('category') or '—'} | {_budget(job)} | "
            f"{_offers(job)} | {_age(job)} | {job['score']} · {job['fit']} | {flags} |"
        )

    lines += ["", "<details><summary>เหตุผลที่ให้คะแนนแบบนี้</summary>", ""]
    for i, job in enumerate(new_jobs, 1):
        lines.append(f"**{i}. {job.get('title') or '(ไม่มีชื่อ)'}** — {job['score']}")
        for reason in job.get("reasons") or ["(ไม่มีคำที่ตรงเกณฑ์ใด ๆ)"]:
            lines.append(f"- {reason}")
        lines.append("")
    lines += ["</details>", ""]
    lines.append(
        "_เกณฑ์อยู่ที่ `_tools/jobscan/profile.json` — แก้ได้โดยไม่ต้องแตะโค้ด_"
    )
    return "\n".join(lines)


def render_discord(new_jobs, issue_url=None):
    head = f"**งานใหม่บน Fastwork {len(new_jobs)} รายการ**\n"
    rows = []
    for job in new_jobs[:DISCORD_TOP_N]:
        title = job.get("title") or "(ไม่มีชื่อ)"
        rows.append(
            f"• [{title}]({job.get('url')}) — {_budget(job)} · ยื่นแล้ว {_offers(job)} · "
            f"{_age(job)} · {job['score']} {job['fit']} {_flags(job)}".rstrip()
        )
    tail = ""
    if len(new_jobs) > DISCORD_TOP_N:
        tail = f"\n…อีก {len(new_jobs) - DISCORD_TOP_N} รายการ"
    if issue_url:
        tail += f"\nทั้งหมด: {issue_url}"

    body = head + "\n".join(rows) + tail
    if len(body) > DISCORD_LIMIT:
        body = body[: DISCORD_LIMIT - 1] + "…"
    return body


def to_github_issue(title, body, repo=None, token=None, labels=("jobscan",)):
    repo = repo or os.environ.get("GITHUB_REPOSITORY")
    token = token or os.environ.get("GITHUB_TOKEN")
    if not (repo and token):
        return "github: skipped (GITHUB_REPOSITORY / GITHUB_TOKEN not set)"

    api = os.environ.get("GITHUB_API_URL", "https://api.github.com")
    resp = requests.post(
        f"{api}/repos/{repo}/issues",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        },
        data=json.dumps({"title": title, "body": body, "labels": list(labels)}),
        timeout=TIMEOUT,
    )
    if resp.status_code >= 300:
        return f"github: FAILED {resp.status_code} {resp.text[:300]}"
    return f"github: {resp.json().get('html_url')}"


def to_discord(text, webhook=None):
    webhook = webhook or os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook:
        return "discord: skipped (DISCORD_WEBHOOK_URL not set)"
    resp = requests.post(
        webhook,
        json={"content": text, "allowed_mentions": {"parse": []}},
        timeout=TIMEOUT,
    )
    if resp.status_code >= 300:
        return f"discord: FAILED {resp.status_code} {resp.text[:300]}"
    return "discord: sent"
