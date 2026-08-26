#!/usr/bin/env python3
"""Scan the Fastwork job board, rank what is there, report what is new.

    python3 _tools/jobscan/scan.py --dry-run --fixture _tools/jobscan/fixtures/jobs.json
    python3 _tools/jobscan/scan.py --state-dir _state --seed
    python3 _tools/jobscan/scan.py --state-dir _state

Pipeline: fetch -> normalize -> score -> diff against seen.json -> notify.

Three things about it are deliberate:

* It ranks, it does not filter. Every job in the web category reaches the
  digest; the score sets reading order and `reasons` says why. A filter that
  drops the wrong job is invisible; a job ranked last with its reasons printed
  beside it is still there to disagree with.

* Zero jobs fetched is an error, not a quiet "nothing new". A broken parser
  and an empty board produce identical output, and only one of them should be
  survivable. Pass --allow-empty when you genuinely expect none.

* The first run seeds state without notifying. Against an empty seen.json
  every job on the board is new, which would be one issue hundreds of rows
  long. Use --seed once, then let the schedule take over.
"""
import argparse
import json
import os
import sys
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import notify                       # noqa: E402
import propose                      # noqa: E402
import score as scoring             # noqa: E402
import state as statelib            # noqa: E402


def thai_today():
    # Shares notify.thai_stamp's Thai-month table and Bangkok offset, so the
    # issue title and the "โพสต์เมื่อ" column in its own body never drift
    # apart into two different date formats.
    return notify.thai_stamp(datetime.now(timezone.utc))


def load_jobs(args, profile):
    """Either replay a saved fixture or go and fetch the board."""
    if args.fixture:
        with open(args.fixture, encoding="utf-8") as fh:
            data = json.load(fh)
        jobs = data["jobs"] if isinstance(data, dict) and "jobs" in data else data
        # Re-derive from the stored raw record rather than trusting the
        # normalized fields in the file. A fixture captured before a
        # normalize.py fix would otherwise keep testing the old behaviour --
        # which is how the budget-zero bug would have looked fixed while the
        # fixture still said ฿0.
        if jobs and isinstance(jobs[0], dict) and jobs[0].get("raw"):
            import normalize
            jobs = [normalize.normalize(j["raw"]) for j in jobs]
            print(f"fixture: {args.fixture} -> {len(jobs)} jobs, re-normalized (no network)")
        else:
            print(f"fixture: {args.fixture} -> {len(jobs)} jobs (no network)")
        return jobs

    import fetch                    # imported late: fixtures need no network deps
    jobs = fetch.fetch_jobs(profile=profile, limit=args.limit)
    print(f"fetched {len(jobs)} jobs from the board")
    if args.dump_fixture:
        print(f"payload written to {fetch.save_fixture(args.dump_fixture, jobs)}")
    return jobs


def print_table(jobs, limit=None):
    shown = jobs[:limit] if limit else jobs
    print(f"\n{'score':>5}  {'fit':<10}  {'budget':<18}  title")
    print("-" * 96)
    for job in shown:
        title = (job.get("title") or "(ไม่มีชื่อ)")[:44]
        flags = ",".join(job.get("flags", []))
        print(
            f"{job['score']:>5}  {job['fit']:<10}  {notify._budget(job):<18}  "
            f"{title}{'  [' + flags + ']' if flags else ''}"
        )
    if limit and len(jobs) > limit:
        print(f"... อีก {len(jobs) - limit} รายการ")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--fixture", help="อ่านจากไฟล์ JSON แทนการยิงเว็บ (ไว้เทสต์เกณฑ์คะแนน)")
    ap.add_argument("--state-dir", default="_state", help="ที่เก็บ seen.json และ jobs/*.jsonl")
    ap.add_argument("--profile", default=os.path.join(HERE, "profile.json"))
    ap.add_argument("--limit", type=int, default=None, help="ดึงมากสุดกี่รายการ")
    ap.add_argument("--dry-run", action="store_true", help="พิมพ์อย่างเดียว ไม่เขียน state ไม่แจ้งเตือน")
    ap.add_argument("--seed", action="store_true", help="บันทึก state แต่ไม่แจ้งเตือน (ใช้รอบแรก)")
    ap.add_argument("--no-notify", action="store_true", help="เหมือน --seed")
    ap.add_argument("--allow-empty", action="store_true", help="ยอมให้ดึงได้ 0 รายการโดยไม่ error")
    ap.add_argument("--dump-fixture", help="บันทึก payload ที่ดึงมาไว้เป็น fixture")
    args = ap.parse_args(argv)

    profile = scoring.load_profile(args.profile)
    jobs = load_jobs(args, profile)

    if not jobs and not args.allow_empty:
        print(
            "\nERROR: ดึงงานได้ 0 รายการ\n"
            "  บอร์ดว่างจริง กับ parser พัง ให้ผลหน้าตาเหมือนกันเป๊ะ และแบบหลังต้องดัง\n"
            "  ถ้าตั้งใจว่าว่างจริง ให้ใส่ --allow-empty",
            file=sys.stderr,
        )
        return 1

    ranked = scoring.score_all(jobs, profile)

    if args.dry_run:
        print_table(ranked)
        print(f"\ndry run — ไม่เขียน state ({args.state_dir}) และไม่แจ้งเตือน")
        return 0

    seen = statelib.load_seen(args.state_dir)
    first_ever = not seen
    fresh, updated = statelib.split_new(ranked, seen)

    print(f"\nงานทั้งหมดรอบนี้ {len(ranked)} · เคยเห็นแล้ว {len(ranked) - len(fresh)} · ใหม่ {len(fresh)}")

    # Drafted before the state is written, so the archived record carries its
    # draft too and a digest can be rebuilt from jobs/*.jsonl without re-running
    # the scoring. Jobs flagged needs_backend / off_lane / not_a_project get
    # no draft -- see propose.BLOCKING_FLAGS. They stay in the digest either
    # way; "rank, do not filter" still holds.
    drafted = propose.draft_all(fresh)
    if fresh:
        print(f"ร่าง proposal ให้ {drafted} จาก {len(fresh)} รายการ "
              f"(ที่เหลือติดธงว่าไม่ควรเสนอ)")
    print_table(fresh, limit=20)

    statelib.save_seen(args.state_dir, updated)
    path = statelib.archive(args.state_dir, fresh)
    print(f"\nstate: {len(updated)} ids in {args.state_dir}/seen.json"
          + (f", archived to {path}" if path else ""))

    silent = args.seed or args.no_notify
    if first_ever and not silent:
        silent = True
        print("seen.json ว่างเปล่า — ถือเป็นรอบ seed อัตโนมัติ ไม่แจ้งเตือนรอบนี้")

    if silent:
        print("ไม่แจ้งเตือน (seed / --no-notify)")
        return 0

    if not fresh:
        print("ไม่มีงานใหม่ — ไม่ต้องแจ้งเตือน")
        return 0

    title = f"งานใหม่ {len(fresh)} รายการ · {thai_today()}"
    body = notify.render_markdown(fresh, len(ranked))
    gh = notify.to_github_issue(title, body)
    print(gh)

    issue_url = gh.split("github: ", 1)[1] if gh.startswith("github: http") else None
    print(notify.to_discord(notify.render_discord(fresh, issue_url)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
