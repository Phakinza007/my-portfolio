#!/usr/bin/env python3
"""Capture the demo screenshots the showcase pages are built out of.

    python3 _tools/capture-shots.py --all
    python3 _tools/capture-shots.py --key pathapee
    python3 _tools/capture-shots.py --key pathapee --view b
    python3 _tools/capture-shots.py --url pathapee-precast --selector '#selector' \
                                    --view b --out /tmp/test.jpg
    python3 _tools/capture-shots.py --all --dry-run

Three views per demo, all 1491 x 812 except C:

    A  landing / top of the demo      1491 x 812   -> assets/screenshots/showcase-<key>.jpg
    B  the mechanism it brags about   1491 x 812   -> assets/screenshots/showcase-<key>-b.jpg
    C  the same demo at phone width    375 x 812   -> assets/screenshots/showcase-<key>-c.jpg

View A already exists on disk for all 17 demos and is NOT part of `--all`; ask
for it by name (`--view a`) and, if the file is already there, `--force`.

WHY THIS EXISTS
---------------
The showcase pages are about to carry three images of their demo instead of one.
That triples the surface for the failure CLAUDE.md records in full: twenty-three
strings across thirteen files said BuildNest used hand-drawn SVG "instead of
stock photography", and every one of them was true until the demo was rebuilt
around photography without the copy following. *Not a false claim someone
invented, but a true one nobody retired.* An image is the same kind of claim and
it goes stale the same silent way. The mitigation is that re-capturing the whole
set has to be one command, cheap enough that it actually happens when a demo
changes.

The naive way to take those 34 captures is `chrome --headless --screenshot`, and
it is measurably wrong here. Measured 2026-08-24: headless renders
`display=optional` webfonts as the fallback EVERY time, because `optional`
decides at roughly 100ms of *virtual* time, before the font can arrive, on every
load. Three runs produced byte-identical files in the wrong font, and warming the
cache with a persistent `--user-data-dir` changed nothing. 86 of this site's 88
files ask for `display=optional`. A capture in the wrong font looks entirely
normal — nothing errors, nothing logs — and silently corrupts every measurement
taken from it afterwards.

So this drives a real Chrome over CDP, and every step below is a bug this repo
has already paid for once:

1.  A real browser on `--remote-debugging-port`, never `--headless --screenshot`.
2.  `Page.navigate` TWICE. The first load puts the font on disk; the second is
    the one that can win the `optional` race.
3.  `await document.fonts.ready` before reading or capturing anything.
4.  Neutralise `.reveal` / `.rv`. This site hides them at opacity 0 until an
    IntersectionObserver fires; captured raw, everything below the fold is
    invisible or mid-transition. `work.html` once SHIPPED that way with all 13
    cards at opacity 0 and Lighthouse still scoring 100.
5.  `documentElement.style.scrollBehavior = 'auto'` before scrolling.
    `scroll-behavior: smooth` is frozen while a tab is not visible, and
    `scrollTo()` then returns with `scrollY` unchanged — a probe that scrolls and
    then measures reads the top of the page and reports the section as missing.
    The scroll is verified afterwards, not assumed.
6.  A POSITIVE CONTROL before any file is written: one real string on the page is
    measured as rendered, then measured again with only the webfont dropped from
    that element's own computed stack. The two widths MUST differ. If they match,
    the page rendered in the fallback and the capture is thrown away, loudly.
    Note the trap CLAUDE.md records: adding a `@font-face` with
    `src: local("__none__")` does NOT unload a Google font — Google's own rules
    still match, the sweep reports zero elements moved, and that reads exactly
    like "no exposure". Patch the element's computed `font-family` instead.
7.  Emit at device-pixel size, then `sips -z <h> <w>` down to the target so the
    new files match the existing 1491 x 812 set exactly — and read the result
    back with `sips -g pixelWidth -g pixelHeight`. The automated browser in this
    environment reports unreliable image intrinsics (the same JPEG has returned
    naturalWidth 1470, 1600 and 1959 across three reads); `sips`, `file` and the
    byte count agree with each other and the DOM does not.

CONFIG
------
`_content/showcase-shots.json`, one entry per demo:

    { "pathapee": { "url": "pathapee-precast",
                    "b": { "selector": "#selector", "label_th": "…", "label_en": "…" },
                    "c": { "scroll": 0,             "label_th": "…", "label_en": "…" } } }

`url` is either a repo-relative extensionless path (served locally) or an
absolute https URL — two demos are remote, HabitQuest and SupplyMate. `selector`
is what view B scrolls to; `scroll` is an absolute pixel offset; `offset` shifts
a selector scroll (negative to leave headroom above it). The `label_*` fields are
the captions the HTML carries and are ignored here. A missing or malformed entry
is an error with a message, never a silent skip.

Without the config file the tool still runs from `--url` / `--selector` on the
command line, so it is testable before the config exists.

LOCAL SERVER
------------
Local demos are served by `_tools/serve.py`, started and stopped by this script
unless something is already listening on the port. NOT `python3 -m http.server` —
site URLs dropped their `.html` on 2026-08-07 and the stdlib server cannot
resolve them, so every internal link 404s.

DEPENDENCIES
------------
Python 3 standard library only, plus the `sips` that ships with macOS and a
Google Chrome install. The CDP WebSocket client below is ~90 lines of stdlib
`socket` precisely so this needs no packages.

EXIT CODES
----------
0  every requested capture written and verified
1  something failed (message says which key, which view, and why)
"""
import argparse
import base64
import json
import re
import secrets
import shutil
import socket
import struct
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "_content" / "showcase-shots.json"
OUT_DIR = ROOT / "assets" / "screenshots"
SERVE = ROOT / "_tools" / "serve.py"

# width, height, mobile — A and B share the desktop frame the existing 15 use.
VIEWS = {
    "a": (1491, 812, False),
    "b": (1491, 812, False),
    "c": (375, 812, True),
}
DEFAULT_VIEWS = ("b", "c")
DEVICE_SCALE = 2          # emit at 2x, downscale with sips
JPEG_QUALITY = 92         # pre-downscale; sips re-encodes at SIPS_QUALITY
SIPS_QUALITY = 82         # existing set lands at 75-205 KB for 1491 x 812

CHROME_CANDIDATES = [
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Google Chrome Canary.app/Contents/MacOS/Google Chrome Canary",
]


class Abort(Exception):
    """A failure loud enough to refuse to write a file."""


def rel(path):
    """Path relative to the repo when it is inside it, absolute otherwise."""
    try:
        return Path(path).resolve().relative_to(ROOT)
    except ValueError:
        return Path(path)


# --------------------------------------------------------------------------
# A minimal RFC-6455 client. CDP needs text frames and nothing else; this is
# here so the tool has no third-party dependency.
# --------------------------------------------------------------------------
class WebSocket:
    def __init__(self, url, timeout=120):
        if not url.startswith("ws://"):
            raise Abort(f"not a ws:// url: {url}")
        hostport, _, path = url[len("ws://"):].partition("/")
        host, _, port = hostport.partition(":")
        self.sock = socket.create_connection((host, int(port or 80)), timeout=timeout)
        self.sock.settimeout(timeout)
        key = base64.b64encode(secrets.token_bytes(16)).decode()
        self.sock.sendall(
            f"GET /{path} HTTP/1.1\r\nHost: {hostport}\r\n"
            "Upgrade: websocket\r\nConnection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n".encode()
        )
        self.rf = self.sock.makefile("rb")
        status = self.rf.readline().decode("latin-1").strip()
        if "101" not in status:
            raise Abort(f"websocket handshake refused: {status!r}")
        while self.rf.readline() not in (b"\r\n", b"\n", b""):
            pass

    def send(self, text):
        data = text.encode()
        n = len(data)
        head = bytearray([0x81])
        if n < 126:
            head.append(0x80 | n)
        elif n < 1 << 16:
            head.append(0x80 | 126)
            head += struct.pack("!H", n)
        else:
            head.append(0x80 | 127)
            head += struct.pack("!Q", n)
        mask = secrets.token_bytes(4)
        head += mask
        self.sock.sendall(bytes(head) + bytes(b ^ mask[i & 3] for i, b in enumerate(data)))

    def _exact(self, n):
        buf = self.rf.read(n)
        if buf is None or len(buf) != n:
            raise Abort("websocket closed mid-frame (did Chrome quit?)")
        return buf

    def recv(self):
        """One complete text message, reassembling continuation frames."""
        chunks = []
        while True:
            b0, b1 = self._exact(2)
            fin, opcode = b0 & 0x80, b0 & 0x0F
            masked, n = b1 & 0x80, b1 & 0x7F
            if n == 126:
                n = struct.unpack("!H", self._exact(2))[0]
            elif n == 127:
                n = struct.unpack("!Q", self._exact(8))[0]
            mask = self._exact(4) if masked else None
            payload = self._exact(n) if n else b""
            if mask:
                payload = bytes(b ^ mask[i & 3] for i, b in enumerate(payload))
            if opcode == 0x8:
                raise Abort("websocket closed by Chrome")
            if opcode == 0x9:                      # ping -> pong
                self.sock.sendall(b"\x8a\x80" + secrets.token_bytes(4))
                continue
            if opcode == 0xA:
                continue
            chunks.append(payload)
            if fin:
                return b"".join(chunks).decode("utf-8", "replace")

    def close(self):
        try:
            self.sock.close()
        except OSError:
            pass


class CDP:
    def __init__(self, ws_url):
        self.ws = WebSocket(ws_url)
        self._id = 0
        self.events = []

    def call(self, method, params=None, session=None, timeout=120):
        self._id += 1
        mid = self._id
        msg = {"id": mid, "method": method, "params": params or {}}
        if session:
            msg["sessionId"] = session
        self.ws.send(json.dumps(msg))
        deadline = time.time() + timeout
        while True:
            m = json.loads(self.ws.recv())
            if m.get("id") == mid:
                if "error" in m:
                    raise Abort(f"{method}: {m['error'].get('message')}")
                return m.get("result", {})
            if "method" in m:
                self.events.append(m)
                del self.events[:-400]
            if time.time() > deadline:
                raise Abort(f"{method}: no reply in {timeout}s")

    def take_events(self, method):
        keep, out = [], []
        for e in self.events:
            (out if e.get("method") == method else keep).append(e)
        self.events = keep
        return out

    def close(self):
        self.ws.close()


# --------------------------------------------------------------------------
# JS run inside the page
# --------------------------------------------------------------------------
JS_NEUTRALISE_REVEAL = r"""
(() => {
  let s = document.getElementById('__capture_reveal__');
  if (!s) {
    s = document.createElement('style');
    s.id = '__capture_reveal__';
    // Only the observed wrapper is touched. Descendants keep their own
    // transforms — a page may legitimately rotate or skew something inside.
    s.textContent =
      '.reveal,.rv,.reveal.pending,.rv.pending{' +
      'opacity:1!important;transform:none!important;filter:none!important;' +
      'clip-path:none!important;visibility:visible!important;transition:none!important}' +
      '.reveal>img,.rv>img{clip-path:none!important;opacity:1!important;transform:none!important}';
    (document.head || document.documentElement).appendChild(s);
  }
  let n = 0;
  document.querySelectorAll('.reveal,.rv').forEach(el => {
    // site-ui.js reveals with .visible; the demo pages hide with .pending.
    el.classList.add('visible');
    el.classList.remove('pending');
    el.removeAttribute('data-leaving');
    el.removeAttribute('data-hidden');
    n++;
  });
  document.querySelectorAll('[data-loading]').forEach(el => el.removeAttribute('data-loading'));
  return n;
})()
"""

JS_WAIT_IMAGES = r"""
(() => new Promise(resolve => {
  const imgs = Array.from(document.images).filter(i => !i.complete);
  if (!imgs.length) return resolve({pending: 0, timedOut: false});
  let left = imgs.length, done = false;
  const finish = t => { if (!done) { done = true; resolve({pending: left, timedOut: t}); } };
  const tick = () => { if (--left <= 0) finish(false); };
  imgs.forEach(i => { i.addEventListener('load', tick, {once: true});
                      i.addEventListener('error', tick, {once: true}); });
  setTimeout(() => finish(true), 6000);
}))
"""

# The positive control. Two things about it are load-bearing:
#
#   * It measures elements ALREADY laid out by the page, never a span created
#     for the purpose. Under display=optional Chrome can hold a loaded face and
#     still render the existing text in the fallback for the whole page life, so
#     a fresh span would pick up the font the real page never used and turn the
#     control into a rubber stamp.
#   * It measures single-line runs only. A wrapped paragraph's Range rect is the
#     union of its line boxes — effectively its CONTAINER width — which moves by
#     ~0.2% when the face changes. Measured 2026-08-24 on pathapee-precast: a
#     wrapped <p> reported a 1.68px delta while the h1 on the same page moved
#     15.8px. Sampling the wrapped one is how a fallback render passes.
#
# It reports how many of the sampled elements moved, not just that one did, so a
# weak result is visible rather than merely non-zero.
JS_FONT_CONTROL = r"""
(() => {
  const trim = s => s.trim().replace(/^['"]|['"]$/g, '');
  const web = new Set();
  document.fonts.forEach(f => { if (f.status === 'loaded') web.add(trim(f.family)); });
  if (!web.size) return {status: 'no-webfont',
                         reason: 'no @font-face family on this page reports status "loaded"'};

  const lineWidth = el => {
    const r = document.createRange();
    r.selectNodeContents(el);
    const rects = r.getClientRects();
    return rects.length === 1 ? rects[0].width : null;   // single-line runs only
  };

  const cands = [];
  for (const el of document.querySelectorAll(
        'h1,h2,h3,h4,p,a,li,span,button,td,th,strong,em,label,figcaption,dt,dd')) {
    if (el.children.length) continue;                       // leaf text only
    const text = (el.textContent || '').trim();
    if (text.length < 4) continue;
    const cs = getComputedStyle(el);
    if (cs.visibility === 'hidden' || cs.display === 'none') continue;
    const fams = cs.fontFamily.split(',').map(trim);
    const keep = fams.filter(f => !web.has(f));             // drop ONLY the webfont
    if (keep.length === fams.length) continue;              // element never asked for one
    const w = lineWidth(el);
    if (w === null || w < 40) continue;
    cands.push({el, w, text, fams, keep, size: parseFloat(cs.fontSize) || 0});
  }
  if (!cands.length) return {status: 'no-webfont',
      reason: 'no single-line rendered element requests a loaded webfont'};

  cands.sort((a, b) => b.size - a.size);                    // big type moves furthest
  const sample = cands.slice(0, 40);
  let moved = 0, best = null;
  for (const c of sample) {
    const prev = c.el.style.fontFamily;
    c.el.style.fontFamily = c.keep.length ? c.keep.join(', ') : 'sans-serif';
    void c.el.offsetWidth;                                  // force reflow
    const fb = lineWidth(c.el);
    c.el.style.fontFamily = prev;
    void c.el.offsetWidth;
    if (fb === null) continue;                              // wrapped once patched
    const d = Math.abs(c.w - fb);
    if (d > 0.5) moved++;
    if (!best || d > best.d) best = {d, fb, c};
  }
  if (!best) return {status: 'no-webfont', reason: 'every sampled element wrapped when patched'};

  return {
    status: moved ? 'ok' : 'fallback',
    sampled: sample.length, moved,
    real: Math.round(best.c.w * 100) / 100,
    fallback: Math.round(best.fb * 100) / 100,
    delta: Math.round(best.d * 100) / 100,
    text: best.c.text.slice(0, 48),
    stack: best.c.fams.join(', '),
    without: best.c.keep.join(', ') || 'sans-serif',
    tag: best.c.el.tagName.toLowerCase()
  };
})()
"""


def js_scroll(selector, offset, absolute):
    return (
        "(() => {"
        "  const de = document.documentElement;"
        "  de.style.scrollBehavior = 'auto';"
        "  if (document.body) document.body.style.scrollBehavior = 'auto';"
        f"  const SEL = {json.dumps(selector)}, OFF = {json.dumps(offset)},"
        f"        ABS = {json.dumps(absolute)};"
        "  const before = window.scrollY;"
        "  const max = Math.max(0, de.scrollHeight - window.innerHeight);"
        "  let target, mode;"
        "  if (SEL !== null) {"
        "    const el = document.querySelector(SEL);"
        "    if (!el) return {error: 'selector matched nothing: ' + SEL};"
        "    const r = el.getBoundingClientRect();"
        "    if (!r.width && !r.height) return {error: 'selector has no box: ' + SEL};"
        "    target = Math.round(window.scrollY + r.top + OFF); mode = 'selector';"
        "  } else if (ABS !== null) { target = ABS; mode = 'absolute'; }"
        "  else { return {mode: 'none', before, target: before, after: window.scrollY, max}; }"
        "  target = Math.max(0, Math.min(target, max));"
        "  window.scrollTo(0, target);"
        "  return {mode, before, target, after: window.scrollY, max};"
        "})()"
    )


# --------------------------------------------------------------------------
def evaluate(cdp, sess, expr, await_promise=False, timeout=120):
    r = cdp.call("Runtime.evaluate",
                 {"expression": expr, "returnByValue": True,
                  "awaitPromise": await_promise, "userGesture": True},
                 sess, timeout=timeout)
    if r.get("exceptionDetails"):
        detail = r["exceptionDetails"]
        msg = (detail.get("exception") or {}).get("description") or detail.get("text")
        raise Abort(f"page JS failed: {msg}")
    return r["result"].get("value")


def wait_ready(cdp, sess, timeout=45):
    deadline = time.time() + timeout
    while time.time() < deadline:
        if evaluate(cdp, sess, "document.readyState") == "complete":
            return
        time.sleep(0.15)
    raise Abort(f"page never reached readyState complete in {timeout}s")


def await_fonts(cdp, sess):
    evaluate(cdp, sess, "document.fonts.ready.then(()=>document.fonts.size)",
             await_promise=True)


def goto(cdp, sess, url, label):
    cdp.take_events("Network.responseReceived")
    r = cdp.call("Page.navigate", {"url": url}, sess)
    if r.get("errorText"):
        raise Abort(f"{label}: navigation failed — {r['errorText']}")
    frame = r.get("frameId")
    wait_ready(cdp, sess)
    await_fonts(cdp, sess)
    for e in cdp.take_events("Network.responseReceived"):
        p = e.get("params", {})
        if p.get("type") == "Document" and p.get("frameId") == frame:
            status = p.get("response", {}).get("status", 0)
            if status >= 400:
                raise Abort(f"{label}: {url} answered HTTP {status}")


def set_viewport(cdp, sess, width, height, mobile):
    cdp.call("Emulation.setDeviceMetricsOverride", {
        "width": width, "height": height,
        "deviceScaleFactor": DEVICE_SCALE, "mobile": mobile,
        "screenWidth": width, "screenHeight": height,
    }, sess)
    cdp.call("Emulation.setTouchEmulationEnabled",
             {"enabled": mobile, "maxTouchPoints": 5 if mobile else 1}, sess)


def check_viewport(cdp, sess, width, height, label):
    got = evaluate(cdp, sess, "({w: innerWidth, h: innerHeight, dpr: devicePixelRatio})")
    if got["w"] != width or got["h"] != height:
        raise Abort(f"{label}: asked for {width}x{height}, page reports "
                    f"{got['w']}x{got['h']} — refusing to capture at the wrong size")
    return got


# --------------------------------------------------------------------------
def capture_one(cdp, sess, url, view, spec, out_path, args, log):
    width, height, mobile = VIEWS[view]
    label = f"{out_path.name} [{view}]"

    set_viewport(cdp, sess, width, height, mobile)
    if not args.no_reduced_motion:
        cdp.call("Emulation.setEmulatedMedia",
                 {"features": [{"name": "prefers-reduced-motion", "value": "reduce"}]}, sess)

    # Twice. The first load puts the webfont on disk; only the second one can
    # win the display=optional race, which is decided ~100ms into the load.
    goto(cdp, sess, url, label)
    goto(cdp, sess, url, label)
    check_viewport(cdp, sess, width, height, label)

    ctl = evaluate(cdp, sess, JS_FONT_CONTROL)
    if ctl["status"] == "fallback":
        raise Abort(
            f"{label}: POSITIVE CONTROL FAILED — none of {ctl['sampled']} sampled "
            f"elements moved. Widest case '{ctl['text']}' measures {ctl['real']}px in "
            f"its own stack ({ctl['stack']}) and {ctl['fallback']}px with the webfont "
            f"dropped ({ctl['without']}). Identical widths mean the page rendered in "
            "the fallback face. Nothing written.")
    if ctl["status"] == "no-webfont":
        if not args.allow_no_webfont:
            raise Abort(
                f"{label}: cannot run the positive control — {ctl['reason']}. "
                "Pass --allow-no-webfont if this page really uses system fonts; "
                "otherwise the font never loaded. Nothing written.")
        log(f"    font control : SKIPPED — {ctl['reason']} (--allow-no-webfont)")
    else:
        log(f"    font control : OK — {ctl['moved']}/{ctl['sampled']} sampled elements "
            f"moved; widest {ctl['tag']} '{ctl['text']}' "
            f"{ctl['real']}px real vs {ctl['fallback']}px fallback "
            f"(delta {ctl['delta']}px, stack {ctl['stack']})")
        if ctl["moved"] * 4 < ctl["sampled"]:
            log(f"    ! only {ctl['moved']} of {ctl['sampled']} moved — read that before "
                "trusting anything measured off this capture")

    revealed = evaluate(cdp, sess, JS_NEUTRALISE_REVEAL)

    scroll = evaluate(cdp, sess, js_scroll(spec.get("selector"),
                                           spec.get("offset", 0),
                                           spec.get("scroll")))
    if isinstance(scroll, dict) and scroll.get("error"):
        raise Abort(f"{label}: {scroll['error']}")
    if scroll["mode"] != "none" and abs(scroll["after"] - scroll["target"]) > 2:
        raise Abort(
            f"{label}: scrollTo({scroll['target']}) left scrollY at {scroll['after']}. "
            "That is the frozen-smooth-scroll signature — a hidden tab returns from "
            "scrollTo with scrollY unchanged. Nothing written.")

    imgs = evaluate(cdp, sess, JS_WAIT_IMAGES, await_promise=True, timeout=20)
    if imgs.get("timedOut"):
        log(f"    ! {imgs['pending']} image(s) still loading after 6s — captured anyway")
    evaluate(cdp, sess, JS_NEUTRALISE_REVEAL)     # anything the scroll uncovered
    log(f"    reveal       : {revealed} .reveal/.rv neutralised · "
        f"scroll {scroll['mode']} -> y={scroll['after']} of {scroll['max']}")

    cdp.call("Page.bringToFront", {}, sess)
    time.sleep(args.settle)

    shot = cdp.call("Page.captureScreenshot",
                    {"format": "jpeg", "quality": JPEG_QUALITY,
                     "captureBeyondViewport": False, "fromSurface": True}, sess)
    raw = base64.b64decode(shot["data"])

    out_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = out_path.with_suffix(".tmp.jpg")
    tmp.write_bytes(raw)
    native = sips_size(tmp)
    run_sips(["-s", "format", "jpeg", "-s", "formatOptions", str(SIPS_QUALITY),
              "-z", str(height), str(width), str(tmp)])
    final = sips_size(tmp)
    if final != (width, height):
        tmp.unlink(missing_ok=True)
        raise Abort(f"{label}: sips produced {final[0]}x{final[1]}, wanted {width}x{height}")
    tmp.replace(out_path)
    size = out_path.stat().st_size
    log(f"    wrote        : {rel(out_path)}  "
        f"{native[0]}x{native[1]} -> {final[0]}x{final[1]}  {size:,} bytes")
    return {"path": out_path, "native": native, "final": final, "bytes": size, "control": ctl}


def run_sips(argv):
    r = subprocess.run(["sips"] + argv, capture_output=True, text=True)
    if r.returncode != 0:
        raise Abort(f"sips failed: {r.stderr.strip() or r.stdout.strip()}")
    return r.stdout


def sips_size(path):
    out = run_sips(["-g", "pixelWidth", "-g", "pixelHeight", str(path)])
    w = re.search(r"pixelWidth:\s*(\d+)", out)
    h = re.search(r"pixelHeight:\s*(\d+)", out)
    if not (w and h):
        raise Abort(f"sips could not read the size of {path}")
    return int(w.group(1)), int(h.group(1))


# --------------------------------------------------------------------------
def port_open(port, host="127.0.0.1"):
    with socket.socket() as s:
        s.settimeout(0.4)
        return s.connect_ex((host, port)) == 0


class LocalServer:
    """_tools/serve.py, not http.server — see the docstring."""

    def __init__(self, port):
        self.port = port
        self.proc = None
        self.borrowed = False

    def start(self):
        if port_open(self.port):
            self.borrowed = True
            print(f"  server       : reusing whatever already listens on :{self.port}")
            return
        self.proc = subprocess.Popen([sys.executable, str(SERVE), str(self.port)],
                                     cwd=str(ROOT),
                                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(60):
            if port_open(self.port):
                print(f"  server       : _tools/serve.py on :{self.port}")
                return
            time.sleep(0.1)
        raise Abort(f"_tools/serve.py never came up on :{self.port}")

    def stop(self):
        if self.proc and not self.borrowed:
            self.proc.terminate()
            try:
                self.proc.wait(5)
            except subprocess.TimeoutExpired:
                self.proc.kill()


class Browser:
    def __init__(self, chrome, port):
        self.chrome = chrome
        self.port = port
        self.proc = None
        self.profile = None
        self.cdp = None
        self.session = None
        self.target = None

    def start(self):
        if port_open(self.port):
            raise Abort(f"something already listens on :{self.port} — "
                        "pass --debug-port to pick another")
        self.profile = tempfile.mkdtemp(prefix="capture-shots-profile-")
        self.proc = subprocess.Popen([
            self.chrome,
            f"--remote-debugging-port={self.port}",
            f"--user-data-dir={self.profile}",
            "--no-first-run", "--no-default-browser-check",
            "--disable-background-timer-throttling",
            "--disable-backgrounding-occluded-windows",
            "--disable-renderer-backgrounding",
            "--disable-features=Translate,CalculateNativeWinOcclusion",
            "--hide-scrollbars",
            "--window-size=1600,1000",
            "about:blank",
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        ws_url = None
        for _ in range(120):
            try:
                with urllib.request.urlopen(
                        f"http://127.0.0.1:{self.port}/json/version", timeout=1) as r:
                    ws_url = json.load(r)["webSocketDebuggerUrl"]
                break
            except Exception:
                time.sleep(0.25)
        if not ws_url:
            raise Abort(f"Chrome never opened the debugging port :{self.port}")

        self.cdp = CDP(ws_url)
        self.target = self.cdp.call("Target.createTarget", {"url": "about:blank"})["targetId"]
        self.session = self.cdp.call(
            "Target.attachToTarget", {"targetId": self.target, "flatten": True})["sessionId"]
        for domain in ("Page", "Runtime", "Network"):
            self.cdp.call(f"{domain}.enable", {}, self.session)
        print(f"  browser      : {self.chrome} on :{self.port}")

    def stop(self):
        try:
            if self.cdp and self.target:
                self.cdp.call("Target.closeTarget", {"targetId": self.target}, timeout=10)
            if self.cdp:
                self.cdp.call("Browser.close", timeout=10)
        except Exception:
            pass
        if self.cdp:
            self.cdp.close()
        if self.proc:
            try:
                self.proc.wait(8)
            except subprocess.TimeoutExpired:
                self.proc.kill()
        if self.profile:
            shutil.rmtree(self.profile, ignore_errors=True)


def find_chrome(explicit):
    if explicit:
        if not Path(explicit).exists():
            raise Abort(f"--chrome {explicit} does not exist")
        return explicit
    for c in CHROME_CANDIDATES:
        if Path(c).exists():
            return c
    found = shutil.which("google-chrome") or shutil.which("chromium")
    if found:
        return found
    raise Abort("no Google Chrome found — pass --chrome /path/to/Chrome. "
                "This tool needs a real browser; --headless --screenshot renders "
                "display=optional webfonts as the fallback every time.")


# --------------------------------------------------------------------------
def load_config(path):
    if not path.exists():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise Abort(f"{rel(path)} is not valid JSON: {e}")
    if not isinstance(data, dict):
        raise Abort(f"{rel(path)} must be an object keyed by demo")
    return data


def entry_spec(cfg, key, view, path):
    """(page_url, view_spec) for one key/view, or a loud error. Never a skip."""
    if key not in cfg:
        raise Abort(f"'{key}' is not in {rel(path)} "
                    f"(has: {', '.join(sorted(cfg)) or 'nothing'})")
    entry = cfg[key]
    if not isinstance(entry, dict):
        raise Abort(f"'{key}' must be an object, found {type(entry).__name__}")
    url = entry.get("url")
    if not isinstance(url, str) or not url.strip():
        raise Abort(f"'{key}' has no usable \"url\"")
    spec = entry.get(view, {} if view != "b" else None)
    if spec is None:
        raise Abort(f"'{key}' has no \"{view}\" block — view {view.upper()} needs one "
                    "with a \"selector\" or a \"scroll\"")
    if not isinstance(spec, dict):
        raise Abort(f"'{key}.{view}' must be an object, found {type(spec).__name__}")
    if view == "b" and not spec.get("selector") and spec.get("scroll") is None:
        raise Abort(f"'{key}.b' needs a \"selector\" (or an explicit \"scroll\") — "
                    "view B is the mechanism the page brags about, not the top of it")
    if spec.get("selector") is not None and not isinstance(spec["selector"], str):
        raise Abort(f"'{key}.{view}.selector' must be a string")
    if spec.get("scroll") is not None and not isinstance(spec["scroll"], (int, float)):
        raise Abort(f"'{key}.{view}.scroll' must be a number")
    return url.strip(), spec


def page_url(raw, server_port):
    if raw.startswith(("http://", "https://")):
        return raw
    return f"http://localhost:{server_port}/{raw.lstrip('/')}"


def out_for(key, view):
    return OUT_DIR / (f"showcase-{key}.jpg" if view == "a" else f"showcase-{key}-{view}.jpg")


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser(
        description="Capture demo screenshots for the showcase pages (real Chrome, CDP).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="View A is never part of --all: it already exists for all 17 demos.")
    ap.add_argument("--all", action="store_true", help="every key in the config")
    ap.add_argument("--key", action="append", default=[], metavar="KEY",
                    help="one demo key from the config (repeatable)")
    ap.add_argument("--view", action="append", default=[], choices=list(VIEWS),
                    help="a, b or c (default: b and c)")
    ap.add_argument("--url", metavar="PATH_OR_URL",
                    help="capture this page instead of the config (needs --out)")
    ap.add_argument("--selector", metavar="CSS", help="with --url: what view B scrolls to")
    ap.add_argument("--scroll", type=int, metavar="PX", help="with --url: absolute scroll")
    ap.add_argument("--offset", type=int, default=0, metavar="PX",
                    help="with --url: shift a selector scroll (negative leaves headroom)")
    ap.add_argument("--out", metavar="FILE", help="with --url: where to write")
    ap.add_argument("--dry-run", action="store_true", help="print the plan, capture nothing")
    ap.add_argument("--force", action="store_true",
                    help="allow overwriting an existing view-A hero shot")
    ap.add_argument("--allow-no-webfont", action="store_true",
                    help="proceed on a page that genuinely uses system fonts only")
    ap.add_argument("--no-reduced-motion", action="store_true",
                    help="do not emulate prefers-reduced-motion (animations keep running)")
    ap.add_argument("--settle", type=float, default=0.6, metavar="S",
                    help="seconds to settle after scrolling (default 0.6)")
    ap.add_argument("--config", default=str(CONFIG_PATH), metavar="FILE",
                    help=f"config file (default {CONFIG_PATH.name})")
    ap.add_argument("--server-port", type=int, default=8123)
    ap.add_argument("--debug-port", type=int, default=9333)
    ap.add_argument("--chrome", help="path to a Chrome/Chromium binary")
    args = ap.parse_args()

    views = tuple(dict.fromkeys(args.view)) or DEFAULT_VIEWS

    # ---- build the job list -------------------------------------------------
    jobs = []          # (key, view, raw_url, spec, out_path)
    if args.url:
        if args.all or args.key:
            return die("--url is for a single ad-hoc page; do not mix it with --all/--key")
        if not args.out:
            return die("--url needs --out (there is no config key to name the file from)")
        if len(views) != 1:
            return die("--url takes exactly one --view")
        view = views[0]
        spec = {}
        if args.selector:
            spec["selector"] = args.selector
        if args.scroll is not None:
            spec["scroll"] = args.scroll
        spec["offset"] = args.offset
        if view == "b" and not spec.get("selector") and spec.get("scroll") is None:
            return die("--view b needs --selector or --scroll")
        jobs.append(("(ad-hoc)", view, args.url, spec, Path(args.out).expanduser().resolve()))
    else:
        cfg_path = Path(args.config).expanduser()
        cfg = load_config(cfg_path)
        if cfg is None:
            return die(f"{rel(cfg_path)} does not exist yet.\n"
                       "Until it does, drive one page directly, e.g.:\n"
                       "  python3 _tools/capture-shots.py --url pathapee-precast "
                       "--selector '#selector' --view b --out /tmp/test.jpg")
        if args.all and args.key:
            return die("--all and --key are alternatives")
        keys = sorted(cfg) if args.all else args.key
        if not keys:
            return die("nothing to do — pass --all, --key KEY, or --url")
        for key in keys:
            for view in views:
                raw, spec = entry_spec(cfg, key, view, cfg_path)
                out = out_for(key, view)
                if view == "a" and out.exists() and not args.force:
                    raise Abort(f"{out.relative_to(ROOT)} already exists and view A is the "
                                "hero the showcase pages already ship — pass --force to "
                                "overwrite it deliberately")
                jobs.append((key, view, raw, spec, out))

    needs_server = any(not r.startswith(("http://", "https://")) for _, _, r, _, _ in jobs)

    print(f"capture-shots — {len(jobs)} capture(s), views {'/'.join(views)}")
    for key, view, raw, spec, out in jobs:
        w, h, mobile = VIEWS[view]
        where = spec.get("selector") or (f"y={spec['scroll']}" if spec.get("scroll") is not None
                                         else "top")
        print(f"  {key:<22} {view}  {w}x{h}{' mobile' if mobile else ''}  "
              f"{raw}  @{where}  -> {out.name}")
    if args.dry_run:
        print("\n--dry-run: nothing captured")
        return 0

    if not shutil.which("sips"):
        return die("no `sips` on PATH — this tool downscales with macOS sips")

    server = LocalServer(args.server_port) if needs_server else None
    browser = Browser(find_chrome(args.chrome), args.debug_port)
    ok, failed = [], []
    try:
        if server:
            server.start()
        browser.start()
        for key, view, raw, spec, out in jobs:
            print(f"\n  {key} [{view}]")
            try:
                res = capture_one(browser.cdp, browser.session,
                                  page_url(raw, args.server_port),
                                  view, spec, out, args, log=print)
                ok.append((key, view, res))
            except Abort as e:
                print(f"    FAILED       : {e}")
                failed.append((key, view, str(e)))
    finally:
        browser.stop()
        if server:
            server.stop()

    print(f"\n{len(ok)} written, {len(failed)} failed")
    for key, view, msg in failed:
        print(f"  ! {key} [{view}] — {msg}")
    return 1 if failed else 0


def die(msg):
    print(f"! {msg}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Abort as e:
        sys.exit(die(e))
    except KeyboardInterrupt:
        sys.exit(130)
