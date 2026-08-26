#!/usr/bin/env python3
"""Draft a proposal for one job -- by filling a template, never by generating.

    from propose import draft
    text = draft(scored_job)        # str, or None when it should not be drafted

WHY A TEMPLATE AND NOT A MODEL
------------------------------
The scanner does not call an LLM anywhere, and this does not change that: no
API key, no per-run cost, no network call, and nothing that can invent a
sentence nobody checked. Every phrase it can emit is sitting in
proposal_template.json where it can be read and corrected, and every project
blurb is lifted verbatim from _content/project-copy.json -- the file that
already exists precisely because the same copy repeated across 84 files kept
drifting out of agreement with itself.

That matters more here than anywhere else on the site. CLAUDE.md records that
37 strings across 13 files once advertised a Node/Express backend that never
existed, and that resume.html still claims "full-stack" while the PDF -- the
honest document -- says "Frontend practice, presented as real work." A
proposal is that same claim made directly to a paying stranger. A generated
one would be the fastest possible way to repeat the mistake at scale, to an
audience that can hold him to it.

WHAT IT REFUSES TO DRAFT
------------------------
Three flags from score.py stop a draft outright, because sending one would
mean offering work that cannot honestly be delivered:

  needs_backend   the post wants an API, a database, a login system
  off_lane        mobile apps, video, ads -- a different trade
  not_a_project   a staffing ad, not a piece of work to quote for

`other_platform` was added after reading a real digest: the highest-scoring
job in it, at 99, was "Squarespace 7.1. Experience with HTML, CSS, and
JavaScript." -- scored on html/css/javascript while the thing actually being
hired for was Squarespace, which is not a platform worked in. The post also
asked for a specific Squarespace problem the applicant had diagnosed, which
no template can answer. A draft there would have implied experience that does
not exist, which is the failure CLAUDE.md keeps returning to.

A further refusal has no flag behind it: a job for which score.py found no
substantive reason to fit. If nothing can be said about why this portfolio
suits *this* job, there is nothing to propose, and a template filled in
anyway reads as spam. The first live digest proved both halves of that --
"ฉันหา คนที่สามารถยกเลิกการสมัคร U-next ได้ค่ะ" (cancel a streaming
subscription, ฿500) carried no flags and got a full website pitch, and
"เช็คว่าคลิปนี้ปั๊มไลค์หรือไม่" qualified on the bare word "เว็บ" alone.

This does NOT remove those jobs from the digest. They stay in the table with
their score and their reasons, exactly as before -- "rank, do not filter" is
still the rule. They simply arrive without a draft, which is the honest
output for a job this portfolio should not be bidding on.

Price and timeline are left as [brackets] on purpose. They are the two things
that should be decided per job by the person who has to deliver it.
"""
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TEMPLATE = os.path.join(HERE, "proposal_template.json")
DEFAULT_COPY = os.path.join(HERE, "..", "..", "_content", "project-copy.json")

# Sending a proposal for any of these would be offering work that cannot be
# delivered as described. Refusing is the honest output, not a gap.
BLOCKING_FLAGS = ("needs_backend", "off_lane", "not_a_project", "other_platform")

# One of these must fire for a draft to be worth sending. `web_generic` is
# deliberately absent: it matches the bare word "เว็บ" anywhere in the post.
SUBSTANTIVE_GROUPS = {"core", "wordpress", "stretch"}

_ASCII = re.compile(r"^[\x00-\x7f]+$")


def load_template(path=DEFAULT_TEMPLATE):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def load_copy(path=DEFAULT_COPY):
    with open(os.path.normpath(path), encoding="utf-8") as fh:
        return json.load(fh)["projects"]


def _match(term, haystack):
    """Same split as score.py: ASCII on word boundaries, Thai by substring.

    Thai has no spaces between words so a boundary match finds almost nothing;
    substring matching on ASCII is how "shop" starts matching "workshop".
    """
    term = term.lower()
    if _ASCII.match(term):
        return bool(re.search(r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])",
                              haystack))
    return term in haystack


def _reason_terms(reason):
    """Pull the '(landing page, หน้าเดียว)' tail off a score.py reason line."""
    m = re.search(r"\(([^)]*)\)", reason)
    return m.group(1).replace("…", "").strip() if m else ""


def _fit_lines(job, template):
    """Turn score.py's reason lines into sentences a client would read.

    score.py writes them for the digest -- "+36 ตรงกับที่ส่งมอบได้ (landing
    page, หน้าเดียว)" is a scoring trace, not a sentence. The phrasing lives
    in the template so it can be reworded without touching code.
    """
    phrases = template["fit_phrases"]
    labels = {
        "ตรงกับที่ส่งมอบได้": "core",
        "WordPress / Elementor": "wordpress",
        "งานเว็บทั่วไป": "web_generic",
        "ทำได้ แต่หนักขึ้น": "stretch",
    }
    lines, keys = [], []
    for reason in job.get("reasons") or []:
        if reason.startswith("−"):          # penalties never become sales copy
            continue
        for label, key in labels.items():
            if label in reason and key in phrases:
                terms = _reason_terms(reason)
                line = phrases[key].format(terms=terms)
                if line not in lines:
                    lines.append(line)
                    keys.append(key)
                break
    return lines, keys


def _portfolio_lines(job, template, copy):
    """Pick 1-2 real projects, and quote their blurbs verbatim."""
    haystack = " ".join(str(job.get(f) or "") for f in
                        ("title", "description", "category")).lower()

    keys = []
    for group in template["portfolio_match"]:
        if any(_match(t, haystack) for t in group["terms"]):
            keys = group["projects"]
            break
    if not keys:
        keys = template["portfolio_default"]

    base = template["project_urls"]["_base"]
    lines = []
    for key in keys[:2]:
        entry = copy.get(key)
        if not entry:
            # A renamed project key must not silently drop the reference and
            # leave a proposal that says "ตัวอย่างงาน" with nothing under it.
            continue
        blurb = (entry.get("th") or {}).get("long")
        if not blurb:
            continue
        lines.append(f"- {blurb}\n  {base}{key}")
    return lines


def draft(job, template=None, copy=None):
    """Return the proposal text for this job, or None if it must not be drafted."""
    flags = set(job.get("flags") or ())
    if flags & set(BLOCKING_FLAGS):
        return None

    template = template or load_template()
    copy = copy if copy is not None else load_copy()

    # No positive reason to fit means nothing to propose. The blocking flags
    # above only catch jobs that are actively wrong; this catches the ones
    # that are merely unrelated, and they are the more embarrassing failure.
    #
    # Found by reading a real digest rather than by reasoning about the rules:
    # "ฉันหา คนที่สามารถยกเลิกการสมัคร U-next ได้ค่ะ" -- someone wanting help
    # cancelling a streaming subscription, ฿500 -- carried none of the three
    # flags, so it got a full proposal offering website work with a
    # construction-firm and a clinic in the portfolio list. Sending that is
    # spam, and it would have gone out under his name.
    fit, fit_keys = _fit_lines(job, template)
    if not fit:
        return None

    # web_generic alone is not a reason to bid. It fires on the bare word
    # "เว็บ"/"web" appearing anywhere, so on its own it says only "this post
    # mentions the web" -- which "เช็คว่าคลิปนี้ปั๊มไลค์หรือไม่" does. At least
    # one substantive group has to agree: the actual services (core), the
    # actual stack (wordpress), or something adjacent already built (stretch).
    if not (set(fit_keys) & SUBSTANTIVE_GROUPS):
        return None

    parts = [template["intro"].format(title=job.get("title") or "งานนี้")]

    parts.append(template["fit_lead"])
    parts.extend(f"- {line}" for line in fit)

    portfolio = _portfolio_lines(job, template, copy)
    if portfolio:
        parts.append(template["portfolio_lead"])
        parts.extend(portfolio)

    parts.append(template["closing"])
    return "\n\n".join(parts)


def draft_all(jobs, template=None, copy=None):
    """Attach a draft to each job in place; returns how many were drafted."""
    template = template or load_template()
    copy = copy if copy is not None else load_copy()
    n = 0
    for job in jobs:
        text = draft(job, template, copy)
        job["proposal"] = text
        if text:
            n += 1
    return n
