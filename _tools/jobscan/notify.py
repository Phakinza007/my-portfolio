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

import requests

TIMEOUT = 20
DISCORD_LIMIT = 2000          # hard limit imposed by Discord
DISCORD_TOP_N = 5

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


def render_markdown(new_jobs, total_seen):
    """The GitHub Issue body: a table, best fit first, reasons included."""
    lines = [
        f"พบงานใหม่ **{len(new_jobs)}** รายการ (บอร์ดมีทั้งหมด {total_seen} รายการในรอบนี้)",
        "",
        "เรียงตามความเข้ากับงานที่ส่งมอบได้ — คะแนนไม่ได้กรองงานทิ้ง "
        "ทุกงานในรอบนี้อยู่ในตารางครบ",
        "",
        "| # | งาน | งบ | ความเข้า | หมายเหตุ |",
        "|--:|-----|----|----------|----------|",
    ]
    for i, job in enumerate(new_jobs, 1):
        title = (job.get("title") or "(ไม่มีชื่อ)").replace("|", "\\|")
        url = job.get("url") or ""
        link = f"[{title}]({url})" if url else title
        flags = _flags(job)
        lines.append(
            f"| {i} | {link} | {_budget(job)} | {job['score']} · {job['fit']} | {flags} |"
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
            f"• [{title}]({job.get('url')}) — {_budget(job)} · "
            f"{job['score']} {job['fit']} {_flags(job)}".rstrip()
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
