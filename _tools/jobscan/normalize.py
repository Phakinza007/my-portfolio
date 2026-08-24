#!/usr/bin/env python3
"""Turn one raw API record into the flat shape the rest of the tool uses.

The field names come from a complete record printed by recon.py on
2026-08-24, not from a truncated preview -- 31 keys, of which these matter.
Everything else is kept under `raw` so a later change to the scoring rules
(or the proposal drafting) can be replayed over the archive without going
back to the board.
"""
import re

import fetch

# "700" -> 700. Some posts carry "ไม่ระบุ", an empty string, or null.
_NUM = re.compile(r"[\d,]+(?:\.\d+)?")


def _money(value):
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    m = _NUM.search(str(value))
    if not m:
        return None
    try:
        return float(m.group(0).replace(",", ""))
    except ValueError:
        return None


def _budget_text(lo, hi, raw_lo):
    if lo is None and hi is None:
        # Keep whatever the post actually said rather than inventing a dash.
        return str(raw_lo).strip() if raw_lo else "ไม่ระบุ"
    if lo is not None and hi is not None and lo != hi:
        return f"฿{lo:,.0f}–{hi:,.0f}"
    only = lo if lo is not None else hi
    return f"฿{only:,.0f}"


# `type` is how the client wants to engage; worth surfacing because a
# สัญญาจ้าง / พาร์ทไทม์ post is a job, not a project, whatever its keywords say.
TYPE_TH = {
    "freelance": "ฟรีแลนซ์",
    "contract": "สัญญาจ้าง",
    "parttime": "พาร์ทไทม์",
    "fulltime": "ประจำ",
}


def normalize(row):
    job_id = row.get("id")
    lo = _money(row.get("budget"))
    hi = _money(row.get("budget_2"))
    if lo is not None and hi is not None and hi < lo:
        lo, hi = hi, lo

    tag = row.get("tag") or {}
    poster = row.get("company_display_name") or (row.get("user_profile") or {}).get("display_name")

    return {
        "id": job_id,
        "url": fetch.job_url(job_id),
        "title": (row.get("title") or "").strip(),
        "description": (row.get("description") or "").strip(),
        "category": tag.get("name"),
        "category_id": tag.get("id"),
        "engagement": TYPE_TH.get(row.get("type"), row.get("type")),
        "kind": row.get("kind"),
        "budget_min": lo,
        "budget_max": hi,
        "budget_text": _budget_text(lo, hi, row.get("budget")),
        "posted_at": row.get("inserted_at"),
        "deadline_at": row.get("deadline_at"),
        "expired_at": row.get("expired_at"),
        # How many freelancers already applied. A 126-offer post is a lottery
        # ticket; a 0-offer post an hour old is the one worth opening.
        "offers": row.get("freelance_offers_count"),
        "poster": poster,
        "requires_english": bool(row.get("require_english_speaker")),
        "raw": row,
    }
