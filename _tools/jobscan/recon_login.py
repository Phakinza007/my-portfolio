#!/usr/bin/env python3
"""Can the scanner log in to Fastwork, and what does its apply form ask for?

    python3 _tools/jobscan/recon_login.py

WHY THIS EXISTS
---------------
The scanner is read-only today: it reads jobboard-api.fastwork.co, which
answers a plain HTTP client with no auth at all. Drafting a proposal for each
new job does not need an account either -- the draft goes into a GitHub issue
for a human to copy, paste and send by hand.

Two smaller things WOULD need an account, and both are optional:

  * reading `already_offered` per job as the real logged-in value, so the tool
    stops drafting proposals for jobs that were already applied to by hand.
  * knowing what the apply form actually asks for, so the drafted text fits
    its fields and its length limit instead of being a wall of prose that has
    to be re-cut by hand every time.

Before asking anyone for a password, this asks whether an automated login is
even permitted and possible. If the login page is protected by CAPTCHA or
mandatory 2FA, the answer is no, and the honest response is to stop and say
so rather than to look for a way around it. A CAPTCHA is a site saying "not
by robot"; routing around it would be ignoring the answer.

WHAT IT CHECKS, IN ORDER
------------------------
1. robots.txt again, this time for the login and apply paths specifically.
   The earlier recon only cleared /jobs.
2. The login page, WITHOUT credentials -- found by following the board's own
   "เข้าสู่ระบบ" control rather than by guessing paths. (The first version
   guessed /login, /signin and /auth/login on both hosts; all six answered
   404, which is what a guess earns and says nothing about the site.) Then:
   which endpoint the form posts to, whether a CSRF token is present, and --
   the decisive question -- whether reCAPTCHA/hCaptcha/Turnstile or a 2FA
   step is in the page at all.
3. A job page's apply control, WITHOUT credentials and WITHOUT submitting:
   what fields the form has, what its length limits are, and what the page
   fetches when the control is opened.
4. Only if step 2 found no CAPTCHA and FASTWORK_EMAIL/FASTWORK_PASSWORD are
   both set: one real login attempt, then a single authenticated read of the
   jobs API to see whether `already_offered` changes from its anonymous value.

🔴 NOTHING HERE EVER SUBMITS A PROPOSAL. The apply form is opened and read.
The submit control is never clicked, and no POST to an offer/proposal
endpoint is ever made. A recon that accidentally applies for a job on
someone's behalf has done real, unrecallable damage to a real freelancer's
reputation with a real client.

EXIT CODES
----------
0  recon completed, read the output
2  robots.txt disallows the login or apply path -- stop
3  no login entry point could be found on the site at all
4  CAPTCHA or mandatory 2FA found -- automated login is off the table
"""
import json
import os
import re
import sys
import urllib.robotparser

import requests

BOARD = "https://jobboard.fastwork.co"
MAIN = "https://fastwork.co"
API = "https://jobboard-api.fastwork.co/api"

UA = (
    "PhakinJobScan/0.1 (+https://ph-akin.dev; personal job-alert bot; "
    "contact a0626568471@gmail.com)"
)
HEADERS = {"User-Agent": UA, "Accept-Language": "th,en;q=0.8"}
TIMEOUT = 30

# Every marker here is a "this site does not want robots signing in" signal.
CAPTCHA_MARKERS = [
    "recaptcha", "g-recaptcha", "grecaptcha",
    "hcaptcha", "h-captcha",
    "turnstile", "cf-turnstile",
    "captcha",
    "arkoselabs", "funcaptcha",
]
TWOFA_MARKERS = [
    "otp", "one-time", "รหัสยืนยัน", "two-factor", "2fa",
    "verification code", "authenticator",
]

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "_recon_out")
OUT = os.path.normpath(OUT)


def rule(title):
    print(f"\n{'=' * 68}\n{title}\n{'=' * 68}")


def save(name, text):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    print(f"  [saved] {path} ({len(text):,} chars)")


def check_robots():
    rule("1. robots.txt -- for the login and apply paths this time")
    ok = True
    for base in (BOARD, MAIN):
        url = f"{base}/robots.txt"
        try:
            r = requests.get(url, headers=HEADERS, timeout=TIMEOUT)
        except Exception as exc:                                # noqa: BLE001
            print(f"  {url} -> could not fetch: {exc}")
            print("  treating UNKNOWN as 'not permitted'. Stopping.")
            return False
        if r.status_code == 404:
            print(f"  {url} -> 404, nothing disallowed")
            continue
        print(f"  {url} -> {r.status_code}")
        for line in r.text.splitlines():
            print(f"  | {line}")
        parser = urllib.robotparser.RobotFileParser()
        parser.parse(r.text.splitlines())
        for path in ("/login", "/signin", "/me/", "/jobs"):
            allowed = parser.can_fetch(UA, base + path)
            print(f"    can_fetch({base}{path}) -> {allowed}")
            # /me/ being disallowed is expected and is not a blocker: the
            # scanner never needs to read the account area, only to hold a
            # session while reading /jobs.
            if path in ("/login", "/signin") and not allowed:
                ok = False
    return ok


def scan_markers(html, label):
    lowered = html.lower()
    found_captcha = sorted({m for m in CAPTCHA_MARKERS if m in lowered})
    found_2fa = sorted({m for m in TWOFA_MARKERS if m.lower() in lowered})
    print(f"  {label}: captcha markers {found_captcha or 'none'}")
    print(f"  {label}: 2fa markers     {found_2fa or 'none'}")
    return found_captcha, found_2fa


def probe_login_page():
    """Find the login entry point by following the site's own control.

    The first version of this guessed: /login, /signin, /auth/login on both
    hosts. All six answered 404, which is the correct outcome for a guess and
    tells you nothing about the site. The board's own rendered page carries a
    control reading "เข้าสู่ระบบ" -- the first recon already logged it -- so
    the honest move is to read where that control points instead of inventing
    paths and concluding "no login page exists" when they miss.
    """
    rule("2. Finding the login entry point (following the site's own control)")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  playwright not installed; cannot discover the entry point")
        return None, [], []

    login_url = None
    html = None
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(user_agent=UA, locale="th-TH")
        page.set_default_timeout(20_000)
        try:
            page.goto(f"{BOARD}/jobs", wait_until="domcontentloaded", timeout=45_000)
        except Exception as exc:                                # noqa: BLE001
            print(f"  could not open the board: {exc}")
            browser.close()
            return None, [], []
        page.wait_for_timeout(6000)

        # Any anchor whose href or text looks like a way in.
        print("  anchors on the board that look auth-related:")
        for a in page.query_selector_all("a"):
            href = a.get_attribute("href") or ""
            text = (a.inner_text() or "").strip()[:40]
            if re.search(r"login|signin|sign-in|auth|register|signup", href, re.I) \
                    or "เข้าสู่ระบบ" in text or "สมัครสมาชิก" in text:
                print(f"    href={href!r} text={text!r}")
                if not login_url and href:
                    login_url = href if href.startswith("http") else BOARD + href

        # If it is a button rather than a link, click it and see where we land.
        # Safe here by construction: logged out, and a login control is not a
        # submit control -- try_login() is the only thing that ever posts
        # credentials, and it refuses to run without them.
        if not login_url:
            ctrl = page.query_selector("text=เข้าสู่ระบบ")
            if ctrl:
                print("  'เข้าสู่ระบบ' is a control, not a link -- opening it")
                before = page.url
                try:
                    ctrl.click()
                    page.wait_for_timeout(5000)
                    if page.url != before:
                        login_url = page.url
                        print(f"    navigated to {login_url}")
                    else:
                        print("    stayed put -- likely an in-page modal")
                        login_url = page.url
                except Exception as exc:                        # noqa: BLE001
                    print(f"    click failed: {str(exc)[:120]}")
            else:
                print("  no 'เข้าสู่ระบบ' control found on the board at all")

        if login_url:
            print(f"\n  login entry point: {login_url}")
            if page.url != login_url:
                try:
                    page.goto(login_url, wait_until="domcontentloaded", timeout=45_000)
                    page.wait_for_timeout(5000)
                except Exception as exc:                        # noqa: BLE001
                    print(f"  could not open it: {exc}")
            html = page.content()
            save("login-page.html", html)
        browser.close()

    if not html:
        return None, [], []

    captcha, twofa = scan_markers(html, "login page")

    print("\n  form actions found:")
    for action in sorted(set(re.findall(r'<form[^>]+action="([^"]+)"', html))):
        print(f"    {action}")
    print("  input names/types found:")
    for tag in sorted(set(re.findall(r'<input[^>]*>', html)))[:25]:
        attrs = dict(re.findall(r'(\w[\w-]*)="([^"]*)"', tag))
        keep = {k: v for k, v in attrs.items()
                if k in ("name", "type", "placeholder", "autocomplete", "id")}
        if keep:
            print(f"    {keep}")
    csrf = re.findall(r'name="(_?csrf[^"]*|authenticity_token)"', html, re.I)
    print(f"  csrf-ish inputs: {sorted(set(csrf)) or 'none'}")
    for host in sorted(set(re.findall(
            r'https?://[a-z0-9.-]*(?:auth|account|identity|login|sso)[a-z0-9.-]*\.[a-z]{2,}',
            html, re.I)))[:10]:
        print(f"  auth-ish host referenced: {host}")

    return html, captcha, twofa


def probe_apply_form():
    """Open a job page and read its apply control. Never submit anything."""
    rule("3. A job page's apply control -- read only, never submitted")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("  playwright not installed; skipping")
        return

    # Reuse a real job id from the committed fixture rather than inventing one.
    fixture = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                           "fixtures", "jobs.json")
    try:
        with open(fixture, encoding="utf-8") as fh:
            data = json.load(fh)
        jobs = data["jobs"] if isinstance(data, dict) and "jobs" in data else data
        job_id = (jobs[0].get("raw") or jobs[0]).get("id")
    except Exception as exc:                                    # noqa: BLE001
        print(f"  could not read a job id from the fixture: {exc}")
        return
    url = f"{BOARD}/jobs?job_id={job_id}"
    print(f"  opening {url}")

    seen = []
    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        page = browser.new_page(user_agent=UA, locale="th-TH")
        page.set_default_timeout(20_000)
        page.on("response", lambda r: seen.append((r.status, r.request.method, r.url))
                if "json" in (r.headers or {}).get("content-type", "") else None)
        try:
            page.goto(url, wait_until="domcontentloaded", timeout=45_000)
        except Exception as exc:                                # noqa: BLE001
            print(f"  goto failed: {exc}")
            browser.close()
            return
        page.wait_for_timeout(6000)
        save("job-page.html", page.content())
        scan_markers(page.content(), "job page")

        # Two lists, and the split is the whole safety property here.
        #
        # OPENERS are controls that reveal the form. SUBMITTERS are controls
        # that send it. "ส่งข้อเสนอ" reads like an opener and may well be the
        # confirm button inside the modal -- clicking it with a live session
        # would apply for the job. It is therefore only ever reported, never
        # clicked. Same for "ยืนยัน".
        OPENERS = ["ยื่นข้อเสนอ", "เสนอราคา", "สมัครงาน"]
        SUBMITTERS = ["ส่งข้อเสนอ", "ยืนยัน", "ตกลง", "submit"]

        for label in SUBMITTERS:
            if page.query_selector(f"text={label}"):
                print(f"  NOTE: a control labelled {label!r} exists on this page.")
                print("        Not clicked, by design -- it may be the real submit.")

        # And belt-and-braces: never click anything at all when credentials
        # are present, because that is the only situation in which a click
        # could carry a session and do something irreversible.
        if os.environ.get("FASTWORK_EMAIL") or os.environ.get("FASTWORK_PASSWORD"):
            print("  credentials are set -- skipping every click on this page.")
            print("  A logged-out probe can safely open a modal; a logged-in")
            print("  one cannot, and this recon never needs to.")
            browser.close()
            return

        opened = False
        for label in OPENERS:
            btn = page.query_selector(f"text={label}")
            if not btn:
                continue
            print(f"  found opener labelled {label!r} (logged out, safe to open)")
            try:
                btn.click()
                page.wait_for_timeout(4000)
                opened = True
            except Exception as exc:                            # noqa: BLE001
                print(f"    click did not open anything: {str(exc)[:120]}")
            break
        if not opened:
            print(f"  no opener matching {OPENERS} -- likely gated behind login")

        # Whatever is on screen now: report its form shape. Do NOT submit.
        html = page.content()
        save("job-page-after-open.html", html)
        for tag in ("textarea", "input", "select"):
            els = page.query_selector_all(tag)
            print(f"  <{tag}> count: {len(els)}")
            for el in els[:12]:
                attrs = {a: el.get_attribute(a) for a in
                         ("name", "type", "placeholder", "maxlength", "aria-label")}
                attrs = {k: v for k, v in attrs.items() if v}
                if attrs:
                    print(f"    {attrs}")

        print(f"\n  JSON responses seen while opening: {len(seen)}")
        for status, method, u in seen[:20]:
            print(f"    {status} {method} {u[:140]}")
        browser.close()


def try_login():
    rule("4. A real login attempt (only if credentials were provided)")
    email = os.environ.get("FASTWORK_EMAIL")
    password = os.environ.get("FASTWORK_PASSWORD")
    if not (email and password):
        print("  FASTWORK_EMAIL / FASTWORK_PASSWORD not set -- skipping.")
        print("  That is the expected state for the first run of this recon:")
        print("  sections 1-3 above are what decide whether asking for a")
        print("  password is even worth doing.")
        return

    print(f"  attempting login as {email[:3]}***")
    print("  (no proposal is submitted at any point)")
    # Deliberately not implemented until sections 1-3 have been read by a
    # human and the endpoint is known. Writing a speculative login POST here
    # would be guessing at exactly the step where guessing wrong means
    # hammering someone's auth endpoint with malformed requests.
    print("  NOT IMPLEMENTED YET -- see sections 1-3 first, then wire the")
    print("  real endpoint this recon discovered.")


def main():
    print(f"User-Agent: {UA}")

    if not check_robots():
        print("\nSTOP: robots.txt does not allow the login path for this agent.")
        return 2

    resp, captcha, twofa = probe_login_page()
    if resp is None:
        print("\nSTOP: no login page could be fetched at all.")
        return 3

    probe_apply_form()

    rule("verdict")
    if captcha:
        print(f"  CAPTCHA present on the login page: {captcha}")
        print("  Automated login is off the table. This is the site saying")
        print("  'not by robot', and the right response is to accept it.")
        print("  The proposal drafting still works without an account --")
        print("  it only loses the already_offered de-duplication.")
        return 4
    if twofa:
        print(f"  Possible 2FA markers: {twofa}")
        print("  These are weak signals (the words appear in unrelated copy")
        print("  too). Read section 2's form fields above before concluding.")
    print("  No CAPTCHA found on the login page.")
    print("  Next: set FASTWORK_EMAIL / FASTWORK_PASSWORD and re-run to test")
    print("  a real login -- but only after a human has read section 2.")

    try_login()
    return 0


if __name__ == "__main__":
    sys.exit(main())
