// Mobile overflow check at 375 x 812, over CDP against a real Chromium.
//
//     python3 _tools/serve.py 8123 &
//     node _tools/overflow-check.js http://localhost:8123/<page>
//
// Why it exists: `canScrollX` alone is necessary and NOT sufficient on this site.
// `html, body { overflow-x: hidden }` clips real overflow, so canScrollX stayed false
// while construction-landing's hero CTA ran 18px off a 375px screen and pathapee's
// nowrap heading spans measured 387px against a 371px viewport. So this sweeps every
// element's right edge as well, and skips anything inside an overflow-x scroller —
// BookEase's tables genuinely scroll and are correct (CLAUDE.md).
//
// It also does three things the naive version gets wrong, each recorded in CLAUDE.md:
// awaits document.fonts.ready (display=optional paints the fallback first), forces
// scroll-behavior to auto, and neutralises .reveal / .rv — a headless tab suspends
// IntersectionObserver, so every revealed element would otherwise measure as hidden.
const { spawn } = require('child_process');
const PORT = 9333, URL = process.argv[2];
const chrome = spawn('/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  [`--remote-debugging-port=${PORT}`, '--headless=new', '--no-sandbox', '--disable-dev-shm-usage',
   '--window-size=375,812', 'about:blank'], { stdio: 'ignore' });
const sleep = ms => new Promise(r => setTimeout(r, ms));
(async () => {
  let list;
  for (let i = 0; i < 30; i++) {
    try { list = await (await fetch(`http://127.0.0.1:${PORT}/json/list`)).json(); if (list.length) break; } catch {}
    await sleep(300);
  }
  const ws = new WebSocket(list.find(t => t.type === 'page').webSocketDebuggerUrl);
  let id = 0; const pending = new Map();
  ws.onmessage = e => { const m = JSON.parse(e.data); if (pending.has(m.id)) { pending.get(m.id)(m); pending.delete(m.id); } };
  const send = (method, params = {}) => new Promise(res => { const i = ++id; pending.set(i, res); ws.send(JSON.stringify({ id: i, method, params })); });
  await new Promise(r => ws.onopen = r);
  await send('Emulation.setDeviceMetricsOverride', { width: 375, height: 812, deviceScaleFactor: 2, mobile: true });
  await send('Page.enable');
  await send('Page.navigate', { url: URL });
  await sleep(3500);
  const r = await send('Runtime.evaluate', { awaitPromise: true, returnByValue: true, expression: `
    (async () => {
      await document.fonts.ready;
      document.documentElement.style.scrollBehavior = 'auto';
      document.querySelectorAll('.reveal,.rv').forEach(e => { e.classList.add('visible'); e.style.opacity = 1; e.style.transform = 'none'; });
      const de = document.documentElement;
      de.scrollLeft = 50; const canScrollX = de.scrollLeft > 0; de.scrollLeft = 0;
      const vw = de.clientWidth, over = [];
      for (const el of document.querySelectorAll('body *')) {
        const b = el.getBoundingClientRect();
        if (b.width === 0 || b.height === 0) continue;
        if (b.right > vw + 1) {
          let p = el.parentElement, clipped = false;
          while (p) { const cs = getComputedStyle(p);
            if (cs.overflowX === 'auto' || cs.overflowX === 'scroll' || cs.overflowX === 'hidden') { clipped = true; break; }
            p = p.parentElement; }
          if (!clipped) over.push(el.className + ' right=' + Math.round(b.right));
        }
      }
      return JSON.stringify({ vw, canScrollX, bodyScrollWidth: document.body.scrollWidth,
                              projectLinks: document.querySelectorAll('.project-link').length,
                              unclippedOverflow: over.slice(0, 8) });
    })()` });
  console.log(r.result?.result?.value ?? JSON.stringify(r));
  chrome.kill(); process.exit(0);
})();
