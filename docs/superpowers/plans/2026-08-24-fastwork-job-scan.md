# Fastwork job scan — implementation record

**Goal:** stop hand-scanning `jobboard.fastwork.co` for web work. A scheduled job pulls
the web categories, ranks each post against what this portfolio can actually deliver, and
opens a GitHub Issue listing only the ones that are new.

**Owner's calls, taken 2026-08-24:** run it on GitHub Actions; notify through GitHub Issue
*and* Discord; **do not filter** — every post in the web categories goes into the digest
and the score only sets reading order; draft proposals later, not in this pass.

---

## Why Phase 0 was a recon and not a parser

`jobboard.fastwork.co` is unreachable from the Claude Code sandbox — its egress proxy
answers **403 to CONNECT** for that host (confirmed by `curl`, by `WebFetch`, and by the
proxy's own `recentRelayFailures`). Writing a parser without ever seeing the page would
have produced code that returns an empty list forever and reports "no new jobs" every two
hours with nothing to say it is broken.

So `_tools/jobscan/recon.py` runs in Actions instead, where the network is open, and
**reports rather than guesses**. It is kept in the repo for the day the source changes.

Two failures on the way that are worth remembering:

- The first run **hung until the job timeout and logged nothing.** Two causes:
  `wait_until="networkidle"` never arrives on a page that polls, and `page.evaluate(fetch)`
  has no deadline of its own — *and* Python buffers stdout when it is not a tty, so
  everything already printed died with the process. `PYTHONUNBUFFERED=1` is not a nicety
  here; without it a killed step is indistinguishable from a step that did nothing.
- `get_job_logs` returns a **tail**, so a section printed early is unreadable. The browser
  probe was moved behind an env flag once it had answered its question, which put the
  section that still had unread output at the end of the log.

## What the recon established

| Question | Answer |
|---|---|
| `robots.txt` | `Allow: /`, disallowing only `/me/` and `/en/`. `/jobs` is permitted. |
| Where the data is | Not the page — `__NEXT_DATA__` carries only i18n. It is `jobboard-api.fastwork.co/api/{jobs,tags}` |
| Auth | None. A plain HTTP client works, so **no Chromium in CI** |
| Category filter | `filters[0][field]=tag_id` — verified to actually filter, not merely be accepted. `tag` / `tag_ids` / `tag.id` / `tag_name` answer HTTP 400 |
| Job URL | `/jobs?job_id=<uuid>`. `/jobs/<uuid>` is a **404** |
| Size of the board | ~3,000 open posts, 24 categories. พัฒนาเว็บไซต์ holds ~41 |

The filter probe was written to distinguish "the server filtered" from "the server ignored
the parameter", by comparing `meta.total_count` against an unfiltered baseline **and**
checking that every returned record carries the tag. A filter that is silently ignored
returns the baseline, which is exactly the kind of false pass that ships.

⚠️ The API answered **HTTP 500 to unfiltered queries** three minutes after the identical
request returned 200. `_get()` retries 5xx with backoff and never retries a 4xx.

## What the live data changed

The scoring rules were drafted from the profile in `CLAUDE.md`. The first dry run over
**149 real posts** falsified four of them:

1. **24 genuine web posts scored exactly the base with no reasons at all.** The bare word
   `เว็บไซต์` was in no list — only compounds like `เว็บบริษัท`. Putting bare `เว็บ` into
   `core` would have pushed every post in the category over the line instead, so it has its
   own group at a third of the weight.
2. **68 of 149 posts carry budget `"0"`**, which the board renders as *฿ ไม่ระบุ*. They were
   shown as ฿0 — which reads as "this client wants it free" — and every one of them tripped
   the below-floor flag.
3. The API sends **`part-time` / `full-time`**; the type map had guessed the un-hyphenated
   spellings, so 18 posts passed through untranslated. A ประจำ post is a staffing ad, not a
   project, and now says so.
4. `จัดการร้านค้าออนไลน์` carries shop-admin and staffing work. Those posts **stay** in the
   digest — that is the no-filtering rule — they simply no longer outrank web work by
   sitting at the base score with nothing said about them.

None of the four was findable by reading the rules. This is why `fixtures/jobs.json` is a
real captured payload and not sample records someone invented, and why `scan.py`
re-normalizes it from each record's stored `raw` rather than trusting the file's normalized
fields — otherwise a fixture captured before a fix keeps testing the old behaviour.

## Shape

```
_tools/jobscan/
  recon.py       how the source was found; kept for when it changes
  fetch.py       API + retry + category-name → tag_id at runtime
  normalize.py   31 raw fields → one flat record (+ raw, kept whole)
  score.py       score + reasons + flags; rules live in profile.json
  profile.json   categories, keyword groups, weights, budget floor
  state.py       seen.json + jobs/YYYY-MM.jsonl
  notify.py      GitHub Issue (no secret needed) + Discord (optional)
  scan.py        the pipeline
.github/workflows/
  jobscan-recon.yml   manual; also dry-runs and refreshes the fixture
  jobscan.yml         cron, 08:00–20:00 ICT every 2h
```

Nothing is published: `_tools/` starts with `_` and `.github/` with `.`, both of which
Jekyll skips without touching `_config.yml`. No `.html` and no `assets/` file is involved,
so `check-deploy.py` and `check-copy.py` do not apply.

## Verification performed

- Recon run in Actions: robots.txt read and evaluated, source identified, tag filter proved
  to filter, URL shape proved by the id appearing in the body (a Next.js 404 is served as
  HTTP 200, so status alone would have lied).
- Dry run over the live board: 149 posts across five categories, ranked, printed.
- State machine against the fixture: first run auto-seeds silently (149 ids, no
  notification) → second run reports 0 new → **one id removed from `seen.json` brings back
  exactly that one job** and both notifiers are reached. Without that last step, "0 new" and
  "the differ is broken" read identically.
- `scan.py` exits non-zero on an empty fetch unless `--allow-empty`.

## Still open

- **The cron cannot run until this merges to `main`** — GitHub only schedules workflows on
  the default branch. First real run should be `workflow_dispatch` with `seed: true`.
- `DISCORD_WEBHOOK_URL` is unset, so that channel skips itself silently. GitHub Issues work
  with no setup at all.
- Proposal drafting (deferred by the owner) — `raw` and the jsonl archive already keep
  enough to draft retrospectively.
- After the first deploy, confirm nothing leaked:
  `curl -o /dev/null -w '%{http_code}' https://ph-akin.dev/_tools/jobscan/profile.json` → 404.
