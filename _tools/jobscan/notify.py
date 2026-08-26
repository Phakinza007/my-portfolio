#!/usr/bin/env python3
"""Deliver the digest of new jobs.

Two channels, both optional at runtime and both skipping themselves quietly
when unconfigured -- so the scan still runs and still records state even if a
webhook is missing or a token has expired. A notifier that takes the whole
scan down with it turns a delivery problem into a data problem.

  github  one issue per scan that found new jobs. No secret to set up:
          Actions' own GITHUB_TOKEN is enough, and the GitHub mobile app
          already pushes issue notifications.
  discord one message when DISCORD_WEBHOOK_URL is set -- a card per job
          worth acting on, with the draft inline so it can be copied
          without leaving the app.

Both return a status string; scan.py prints them so the job log says what
actually went out.
"""
import json
import os
from datetime import datetime, timedelta, timezone

import requests

TIMEOUT = 20
DISCORD_LIMIT = 2000          # hard limit on `content`

# Discord's own caps. Exceeding any of them is a 400 on the whole message, so
# every string that goes into an embed is clipped against these rather than
# hoped about.
DISCORD_EMBED_DESC = 4096
DISCORD_EMBED_TOTAL = 6000    # summed across every embed in one message
DISCORD_MAX_EMBEDS = 10
DISCORD_MAX_BUTTONS = 5       # per action row

FIT_COLOURS = {
    "ตรงมาก": 0x22C55E,
    "น่าจะได้": 0xF59E0B,
    "ต้องดูก่อน": 0x94A3B8,
}

# GitHub rejects an issue body over 65,536 characters outright, so an
# oversized digest is not a truncated digest -- it is no notification at all.
# Measured against the real fixture: ~1,150 chars of draft per job, so 30 new
# jobs render ~34 KB and about 60 would go over. A seeded catch-up run can
# reach that. Drafts are trimmed to fit, best-fit first; the table and the
# reasons are never trimmed, because those are what the digest is for.
GITHUB_BODY_LIMIT = 65536
GITHUB_BODY_BUDGET = 60000    # leave room for the trim notice itself

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

    drafted = [j for j in new_jobs if j.get("proposal")]
    if drafted:
        lines += [
            f"## ร่างข้อความเสนอราคา ({len(drafted)} รายการ)",
            "",
            "คัดลอกไปวางในหน้างานบน Fastwork แล้วกดส่งเอง — "
            "เครื่องมือนี้ไม่ส่งอะไรให้แทน และล็อกอินแทนไม่ได้ "
            "(หน้าเข้าสู่ระบบใช้ Cloudflare Turnstile + OTP ทางเบอร์โทร)",
            "",
            "ราคาและระยะเวลาเว้นเป็น `[...]` ไว้ตั้งใจ — สองอย่างนี้ควรตัดสินใจต่องาน",
            "",
        ]
        used = sum(len(x) + 1 for x in lines)
        included = 0
        for i, job in enumerate(new_jobs, 1):
            if not job.get("proposal"):
                continue
            title = job.get("title") or "(ไม่มีชื่อ)"
            block = [
                f"<details><summary><b>{i}. {title}</b> — เปิดร่าง</summary>",
                "",
                f"เปิดหน้างาน: {job.get('url') or '—'}",
                "",
                "```",
                job["proposal"],
                "```",
                "",
                "</details>",
                "",
            ]
            size = sum(len(x) + 1 for x in block)
            if used + size > GITHUB_BODY_BUDGET:
                left = len(drafted) - included
                lines += [
                    f"_อีก {left} ร่างไม่ได้ใส่ในนี้ — issue body ของ GitHub "
                    f"จำกัด {GITHUB_BODY_LIMIT:,} ตัวอักษร และถ้าเกิน issue จะ"
                    "สร้างไม่สำเร็จทั้งอัน ไม่ใช่แค่ตัดท้ายทิ้ง "
                    "ร่างที่เหลืออยู่ใน `jobs/*.jsonl` บน branch `jobscan-state`_",
                    "",
                ]
                break
            lines += block
            used += size
            included += 1

    skipped = [j for j in new_jobs if not j.get("proposal")]
    if skipped:
        lines += [
            f"_ไม่ได้ร่างให้ {len(skipped)} รายการ — ติดธง "
            "`needs_backend` / `off_lane` / `not_a_project` "
            "ซึ่งเป็นงานที่รับแล้วส่งมอบตามที่เขียนไม่ได้ "
            "(ยังอยู่ในตารางด้านบนครบ ไม่ได้ถูกกรองทิ้ง)_",
            "",
        ]

    lines.append(
        "_เกณฑ์อยู่ที่ `_tools/jobscan/profile.json` · ข้อความร่างอยู่ที่ "
        "`_tools/jobscan/proposal_template.json` — แก้ได้โดยไม่ต้องแตะโค้ด_"
    )
    return "\n".join(lines)


def _clip(text, limit):
    text = text or ""
    return text if len(text) <= limit else text[: limit - 1] + "…"


def _job_embed(job):
    """One job, sized to be acted on: title is the link, draft is copyable.

    The draft goes in a fenced code block because that is what makes it one
    gesture on a phone -- long-press a code block in the Discord app and it
    offers Copy Text. Reading the draft in a GitHub issue and copying it from
    there is the same information and four more taps.
    """
    title = _clip(job.get("title") or "(ไม่มีชื่อ)", 256)
    embed = {
        "title": title,
        "url": job.get("url"),
        "color": FIT_COLOURS.get(job.get("fit"), 0x94A3B8),
        "fields": [
            {"name": "งบ", "value": _budget(job), "inline": True},
            {"name": "ความเข้า", "value": f"{job['score']} · {job['fit']}", "inline": True},
            {"name": "ยื่นแล้ว", "value": _offers(job), "inline": True},
        ],
        "footer": {"text": _clip(f"{job.get('category') or '—'} · โพสต์ {_age(job)}", 2048)},
    }
    proposal = job.get("proposal")
    if proposal:
        # 8 chars of fence and newlines, plus a little headroom.
        body = _clip(proposal, DISCORD_EMBED_DESC - 32)
        embed["description"] = f"```\n{body}\n```"
    flags = _flags(job)
    if flags:
        embed["fields"].append({"name": "หมายเหตุ", "value": _clip(flags, 1024), "inline": False})
    return embed


def _rest_embed(jobs):
    """Everything without a draft, as one compact block.

    They are still here on purpose -- "rank, do not filter" applies to the
    digest, and a job with no draft is a job to judge for yourself, not one to
    hide. It just does not need a card of its own.
    """
    lines = []
    for job in jobs:
        title = _clip(job.get("title") or "(ไม่มีชื่อ)", 70)
        bits = [_budget(job), f"{job['score']} {job['fit']}"]
        if _flags(job):
            bits.append(_flags(job))
        lines.append(f"• [{title}]({job.get('url')}) — {' · '.join(bits)}")
    return {
        "title": f"อีก {len(jobs)} รายการ (ไม่ได้ร่างให้)",
        "color": 0x94A3B8,
        "description": _clip("\n".join(lines), DISCORD_EMBED_DESC),
    }


def _embed_size(embed):
    """Discord counts title + description + field names/values + footer."""
    n = len(embed.get("title") or "") + len(embed.get("description") or "")
    n += len((embed.get("footer") or {}).get("text") or "")
    for f in embed.get("fields") or []:
        n += len(f["name"]) + len(f["value"])
    return n


def render_discord(new_jobs, issue_url=None):
    """Build the Discord payload: act on it without leaving the app.

    The old message was one text blob whose drafts lived elsewhere, so acting
    on a job meant Discord -> GitHub issue -> find the row -> expand -> copy ->
    Fastwork. Six moves. This puts the draft in the message and the job link on
    the card, which makes it two: tap the title, long-press the code block.

    Layout follows what can be acted on, not what arrived:
      * every job WITH a draft gets its own colour-coded card
      * everything else collapses into one list -- still there (the digest is
        never filtered), just not competing for attention
    """
    drafted = [j for j in new_jobs if j.get("proposal")]
    rest = [j for j in new_jobs if not j.get("proposal")]

    head = f"**งานใหม่ {len(new_jobs)} รายการ**"
    if drafted:
        head += f" · ร่างพร้อมคัดลอก {len(drafted)}"

    embeds, budget = [], DISCORD_EMBED_TOTAL
    # Cards first, and only as many as the 6,000-char budget really allows --
    # a draft runs ~1,200 chars, so about four fit. Going over is a 400 on the
    # whole message, which would lose the notification entirely.
    for job in drafted:
        if len(embeds) >= DISCORD_MAX_EMBEDS - 1:
            break
        embed = _job_embed(job)
        size = _embed_size(embed)
        if size > budget:
            break
        embeds.append(embed)
        budget -= size

    undrawn = drafted[len(embeds):]
    trailing = undrawn + rest
    if trailing:
        embed = _rest_embed(trailing)
        if _embed_size(embed) <= budget:
            embeds.append(embed)

    payload = {
        "content": _clip(head, DISCORD_LIMIT),
        "embeds": embeds,
        "allowed_mentions": {"parse": []},
    }

    # Link buttons need no bot and no interaction endpoint -- they just open a
    # URL. to_discord() retries without them if this webhook will not take
    # components, so an unsupported field costs a retry, never the message.
    buttons = []
    for job in drafted[: DISCORD_MAX_BUTTONS - 1]:
        if not job.get("url"):
            continue
        label = _clip(f"เปิดงาน: {job.get('title') or ''}".strip(), 40)
        buttons.append({"type": 2, "style": 5, "label": label, "url": job["url"]})
    if issue_url and len(buttons) < DISCORD_MAX_BUTTONS:
        buttons.append({"type": 2, "style": 5, "label": "ดูทั้งหมดใน GitHub", "url": issue_url})
    if buttons:
        payload["components"] = [{"type": 1, "components": buttons}]

    return payload


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


def to_discord(payload, webhook=None):
    """Post the digest, degrading one tier at a time rather than failing.

    Three tiers, richest first: buttons + cards, cards alone, then plain text.
    The tiers exist because a plain webhook's support for `components` is not
    something this code should assume -- if Discord rejects the field, the
    notification must still arrive, and the log must say which tier landed so
    the answer is measured rather than believed.
    """
    webhook = webhook or os.environ.get("DISCORD_WEBHOOK_URL")
    if not webhook:
        return "discord: skipped (DISCORD_WEBHOOK_URL not set)"

    if isinstance(payload, str):        # older callers, and the plain fallback
        payload = {"content": payload, "allowed_mentions": {"parse": []}}

    tiers = [("buttons+embeds", payload)]
    if payload.get("components"):
        tiers.append(("embeds", {k: v for k, v in payload.items() if k != "components"}))
    tiers.append(("plain", {
        "content": _clip(_plain_fallback(payload), DISCORD_LIMIT),
        "allowed_mentions": {"parse": []},
    }))

    last = ""
    for name, body in tiers:
        try:
            resp = requests.post(webhook, json=body, timeout=TIMEOUT)
        except Exception as exc:                                # noqa: BLE001
            last = f"{name}: {exc}"
            continue
        if resp.status_code < 300:
            return f"discord: sent ({name})"
        last = f"{name}: {resp.status_code} {resp.text[:200]}"
    return f"discord: FAILED — {last}"


def _plain_fallback(payload):
    """Flatten a rich payload back to text, for the last tier."""
    lines = [payload.get("content") or "งานใหม่บน Fastwork"]
    for embed in payload.get("embeds") or []:
        title = embed.get("title") or ""
        url = embed.get("url")
        lines.append(f"• [{title}]({url})" if url else f"• {title}")
        for f in embed.get("fields") or []:
            lines.append(f"    {f['name']}: {f['value']}")
    return "\n".join(lines)
