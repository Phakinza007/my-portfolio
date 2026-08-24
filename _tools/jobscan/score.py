#!/usr/bin/env python3
"""Rank a job against what this portfolio can actually deliver.

This ranks; it does not filter. Every job the board returns in the web
category reaches the digest -- the score decides reading order and the
`reasons` list says why, so the call stays with a human.

That is deliberate: a filter that drops the wrong job is invisible, while a
job ranked third with "-20 ต้องมีระบบสมาชิก" beside it is still there to
disagree with.

The weights live in profile.json, not here.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PROFILE = os.path.join(HERE, "profile.json")

_ASCII = re.compile(r"^[\x00-\x7f]+$")


def load_profile(path=DEFAULT_PROFILE):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def _matcher(term):
    """Build a search function for one term.

    An ASCII term is matched on word boundaries; a Thai one on plain
    substring. Thai is written without spaces between words, so a boundary
    match would find almost nothing -- the same reason site-search.js matches
    by substring. But applying substring matching to ASCII too is how "ios"
    starts matching "studios" and "portfolios", and how "php" matches
    "graphps"-style noise, so the two cases genuinely need different rules.
    """
    term = term.lower()
    if _ASCII.match(term):
        pattern = re.compile(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])")
        return lambda haystack: bool(pattern.search(haystack))
    return lambda haystack: term in haystack


_MATCHERS = {}


def _match(term, haystack):
    fn = _MATCHERS.get(term)
    if fn is None:
        fn = _MATCHERS[term] = _matcher(term)
    return fn(haystack)


def score_job(job, profile):
    """Return (score, fit, reasons, flags) for one normalized job record."""
    title = (job.get("title") or "").lower()
    body = " ".join(
        str(job.get(field) or "")
        for field in ("description", "category", "tags_text")
    ).lower()

    total = float(profile["base_score"])
    body_weight = float(profile.get("body_weight", 0.5))
    reasons = []
    flags = []

    for group in profile["groups"]:
        weight = float(group["weight"])
        cap = float(group["cap"])
        subtotal = 0.0
        hits = []

        for term in group["terms"]:
            in_title = _match(term, title)
            in_body = _match(term, body)
            if not (in_title or in_body):
                continue
            # A term found in both places counts once, at the title's weight.
            gain = weight if in_title else weight * body_weight
            subtotal += gain
            hits.append(term)

        if not hits:
            continue

        # Cap has the same sign as weight, so clamp toward zero from the
        # correct side rather than assuming positives.
        if weight >= 0:
            subtotal = min(subtotal, cap)
        else:
            subtotal = max(subtotal, cap)

        total += subtotal
        shown = ", ".join(hits[:3]) + ("…" if len(hits) > 3 else "")
        sign = "+" if subtotal >= 0 else "−"
        reasons.append(f"{sign}{abs(subtotal):.0f} {group['label']} ({shown})")
        if group.get("flag"):
            flags.append(group["flag"])

    penalties = profile.get("engagement_penalties") or {}
    hit = penalties.get(job.get("engagement_key"))
    if hit:
        amount, label = hit
        total += float(amount)
        flags.append("not_a_project")
        reasons.append(f"−{abs(float(amount)):.0f} {label}")

    budget_max = job.get("budget_max")
    floor = profile.get("budget_floor")
    if floor and isinstance(budget_max, (int, float)) and budget_max > 0:
        if budget_max < floor:
            penalty = float(profile.get("below_floor_penalty", 0))
            total += penalty
            flags.append("below_floor")
            reasons.append(
                f"−{abs(penalty):.0f} งบสูงสุด ฿{budget_max:,.0f} "
                f"ต่ำกว่าราคาเริ่มต้น ฿{floor:,}"
            )

    score = max(0, min(100, round(total)))

    fit = profile["fit_bands"][-1][1]
    for threshold, label in profile["fit_bands"]:
        if score >= threshold:
            fit = label
            break

    return score, fit, reasons, flags


def score_all(jobs, profile=None):
    """Score every job and return them sorted best-first."""
    profile = profile or load_profile()
    out = []
    for job in jobs:
        score, fit, reasons, flags = score_job(job, profile)
        out.append({**job, "score": score, "fit": fit, "reasons": reasons, "flags": flags})
    out.sort(key=lambda j: (-j["score"], j.get("title") or ""))
    return out
