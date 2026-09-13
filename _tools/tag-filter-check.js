// Click every tag filter button on work.html / work-en.html and assert that none of
// them empties the grid.
//
//     python3 _tools/serve.py 8123 &
//     node _tools/tag-filter-check.js http://localhost:8123/work
//
// loop-scan.py asserts the same thing statically — every sidebar button must match at
// least one card's data-tags — but the filter is live JS, so after removing a label
// (Full Stack, 2026-09-13) only a click proves the four ANDed predicates still agree.
// Exits 2 if the filter never initialised, if any button yields zero cards, or if
// releasing every button does not return the full set.
const { spawn } = require('child_process');
const PORT = 9334, URL = process.argv[2];
const chrome = spawn('/opt/pw-browsers/chromium-1194/chrome-linux/chrome',
  [`--remote-debugging-port=${PORT}`, '--headless=new', '--no-sandbox', '--disable-dev-shm-usage',
   '--window-size=1280,900', 'about:blank'], { stdio: 'ignore' });
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
  await send('Page.enable'); await send('Page.navigate', { url: URL }); await sleep(2000);
  const r = await send('Runtime.evaluate', { awaitPromise: true, returnByValue: true, expression: `
    (async () => {
      const sleep = ms => new Promise(r => setTimeout(r, ms));
      // site-ui.js is deferred, so navigating is not readiness: clicking before it
      // attaches silently no-ops and the grid reads as "filter matched everything"
      // — 14 of 27 buttons reported the full set that way once. Wait for the filter
      // to write its own status line, which is the only observable proof it is live.
      const ready = await (async () => {
        for (let i = 0; i < 150; i++) {
          const el = document.querySelector('#filter-status');
          if (el && el.textContent.trim()) return true;
          await new Promise(r => setTimeout(r, 100));
        }
        return false;
      })();
      if (!ready) return JSON.stringify({ loaded: false, empty: [], results: {},
                                          reason: 'filter never initialised within 15s' });
      const visible = () => [...document.querySelectorAll('.work-card')]
        .filter(c => !c.hasAttribute('data-hidden') && c.offsetParent !== null).length;
      const btns = [...document.querySelectorAll('.tag-btn')];
      const out = { loaded: document.styleSheets.length > 0, cards: document.querySelectorAll('.work-card').length,
                    tagButtons: btns.length, baseline: visible(), empty: [], results: {} };
      for (const b of btns) {
        b.click(); await sleep(400);
        const n = visible();
        out.results[b.dataset.tag] = n;
        if (n === 0) out.empty.push(b.dataset.tag);
        b.click(); await sleep(300);           // release the toggle
      }
      out.afterReset = visible();
      return JSON.stringify(out);
    })()` });
  const out = r.result?.result?.value ?? JSON.stringify(r);
  const o = JSON.parse(out);
  console.log(`loaded=${o.loaded} cards=${o.cards} tagButtons=${o.tagButtons} baseline=${o.baseline} afterReset=${o.afterReset}`);
  console.log(`buttons that empty the grid: ${o.empty.length ? o.empty.join(', ') : 'NONE'}`);
  console.log("per-tag counts:", JSON.stringify(o.results));
  chrome.kill();
  process.exit(o.loaded && o.empty.length === 0 && o.afterReset === o.baseline ? 0 : 2);
})();
