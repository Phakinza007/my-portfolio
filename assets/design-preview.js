/* Design preview widget — "เว็บของคุณจะหน้าตาแบบนี้"
   Fills <div class="design-preview" data-preview="clinic"></div>.

   Self-guarding: returns immediately when the placeholder is absent, so the
   file is harmless anywhere it is loaded.

   Versioned in the tag as ?v=1. BUMP IT on any change to the generated
   markup — a returning visitor pairing new HTML with a cached older copy of
   this script gets an empty placeholder and no widget at all. That is exactly
   what happened to site-search.js during testing.

   The data is fetched on IntersectionObserver rather than at load: the widget
   sits well below the fold and must not compete with LCP. */
(function () {
  'use strict';

  const root = document.querySelector('.design-preview');
  if (!root) return;

  const KEY = root.dataset.preview;
  if (!KEY) return;

  const el = (tag, cls, text) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  };

  const img = (label) => el('div', 'dp-img', label || 'ภาพ');

  /* ---- the nine block types ---- */
  const BLOCKS = {
    nav(b, ctx) {
      const n = el('div', 'dp-mock-nav');
      n.append(el('span', 'dp-brand', b.admin ? ctx.brand + ' · Admin' : ctx.brand));
      const ul = el('ul');
      (b.links || []).forEach((l) => ul.append(el('li', null, l)));
      n.append(ul);
      if (b.cta) n.append(el('span', b.admin ? 'dp-pill ghost' : 'dp-pill', b.cta));
      return n;
    },

    hero(b) {
      const n = el('div', 'dp-hero');
      if (b.image) n.append(img());
      n.append(el('h3', null, b.title));
      if (b.sub) n.append(el('p', null, b.sub));
      if (b.ctas && b.ctas.length) {
        const row = el('div', 'dp-hero-actions');
        b.ctas.forEach((c, i) => row.append(el('span', i ? 'dp-pill ghost' : 'dp-pill', c)));
        n.append(row);
      }
      return n;
    },

    head(b) {
      return el('h4', null, b.title);
    },

    cards(b) {
      const g = el('div', 'dp-grid');
      g.dataset.cols = String(b.cols || 3);
      (b.items || []).forEach((it) => {
        const c = el('div', 'dp-card');
        c.append(img());
        const body = el('div', 'dp-card-body');
        body.append(el('strong', null, it.title));
        if (it.meta) body.append(el('span', null, it.meta));
        if (it.price) body.append(el('em', null, it.price));
        c.append(body);
        g.append(c);
      });
      return g;
    },

    list(b) {
      const w = el('div', 'dp-rows');
      (b.items || []).forEach((it) => {
        const r = el('div', 'dp-row');
        r.append(el('span', null, it.label));
        r.append(el('span', null, it.value));
        w.append(r);
      });
      return w;
    },

    form(b) {
      const w = el('div', 'dp-fields');
      (b.fields || []).forEach((f) => {
        const g = el('div', 'dp-field');
        g.append(el('span', null, f.label));
        g.append(el('div', null, f.value || ''));
        w.append(g);
      });
      if (b.submit) w.append(el('span', 'dp-pill', b.submit));
      return w;
    },

    gallery(b) {
      const g = el('div', 'dp-grid');
      g.dataset.cols = String(b.cols || 4);
      for (let i = 0; i < (b.count || 4); i++) g.append(img(i % 2 ? 'หลัง' : 'ก่อน'));
      return g;
    },

    map(b) {
      const w = el('div', 'dp-map');
      w.append(img('แผนที่'));
      const rows = el('div', 'dp-rows');
      (b.lines || []).forEach((l) => {
        const r = el('div', 'dp-row');
        r.append(el('span', null, l));
        rows.append(r);
      });
      w.append(rows);
      return w;
    },

    table(b) {
      const wrap = el('div', 'dp-table-wrap');
      const t = el('table', 'dp-table');
      const thead = el('thead');
      const hr = el('tr');
      (b.cols || []).forEach((c) => hr.append(el('th', null, c)));
      thead.append(hr);
      const tbody = el('tbody');
      (b.rows || []).forEach((row) => {
        const tr = el('tr');
        row.forEach((cell) => tr.append(el('td', null, cell)));
        tbody.append(tr);
      });
      t.append(thead, tbody);
      wrap.append(t);
      return wrap;
    }
  };

  const renderMock = (page, ctx) => {
    /* aria-hidden is correct here and is the point: this is an illustration
       of a website. Everything it means is stated as real text in the caption
       inside the same tabpanel — page name, purpose and component list. */
    const m = el('div', 'dp-mock');
    m.setAttribute('aria-hidden', 'true');
    (page.blocks || []).forEach((b) => {
      const fn = BLOCKS[b.t];
      if (fn) m.append(fn(b, ctx));
    });
    return m;
  };

  const renderCaption = (page) => {
    const c = el('div', 'dp-caption');
    const head = el('div', 'dp-caption-head');
    head.append(el('h3', null, page.name));
    head.append(
      page.side === 'admin'
        ? el('span', 'dp-tag dp-tag-admin', 'งานเพิ่มเติม · ประเมินราคาแยก')
        : el('span', 'dp-tag dp-tag-customer', 'หน้าฝั่งลูกค้า')
    );
    c.append(head);
    c.append(el('p', null, page.desc));
    const parts = el('div', 'dp-parts');
    parts.append(el('span', null, 'ส่วนประกอบ:'));
    (page.parts || []).forEach((p) => parts.append(el('span', 'dp-part', p)));
    c.append(parts);
    return c;
  };

  const ICON =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" ' +
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M9 9v11"/></svg>';

  const build = (data) => {
    const ctx = { brand: data.brand };
    const pages = data.pages || [];
    if (!pages.length) return;

    /* header */
    const head = el('div', 'dp-head');
    const badge = el('span', 'dp-badge');
    badge.innerHTML = ICON;
    const headText = el('div');
    headText.append(el('h2', null, 'เว็บของคุณจะหน้าตาแบบนี้'));
    headText.append(el('p', null, 'ภาพจำลองดีไซน์ ไม่ใช่หน้าเว็บจริง — กดเลือกดูได้ทีละส่วน'));
    head.append(badge, headText);

    /* legend */
    const legend = el('div', 'dp-legend');
    const mk = (cls, label) => {
      const s = el('span');
      s.append(el('span', 'dp-dot ' + cls));
      s.append(document.createTextNode(label));
      return s;
    };
    legend.append(mk('dp-dot-customer', 'หน้าฝั่งลูกค้า'));
    legend.append(mk('dp-dot-admin', 'หน้าฝั่ง Admin'));
    legend.append(el('span', 'dp-hint', 'กดเลือกเพื่อดูตัวอย่าง'));

    /* frame */
    const frame = el('div', 'browser-frame');
    const bar = el('div', 'browser-frame-bar');
    ['red', 'amber', 'green'].forEach((c) =>
      bar.append(el('span', 'browser-dot browser-dot-' + c))
    );
    bar.append(el('span', 'browser-url', data.url));
    bar.append(el('span', 'dp-frame-tag', 'ตัวอย่างดีไซน์'));

    const body = el('div', 'dp-body');
    const tabs = el('div', 'dp-tabs');
    tabs.setAttribute('role', 'tablist');
    tabs.setAttribute('aria-label', 'เลือกส่วนของเว็บเพื่อดูตัวอย่าง');
    const pane = el('div', 'dp-pane');

    const buttons = pages.map((page, i) => {
      const b = el('button', 'dp-tab');
      b.type = 'button';
      b.id = 'dp-tab-' + page.id;
      b.setAttribute('role', 'tab');
      b.setAttribute('aria-controls', 'dp-panel');
      b.setAttribute('aria-selected', i === 0 ? 'true' : 'false');
      b.tabIndex = i === 0 ? 0 : -1;
      b.append(el('span', 'dp-dot ' + (page.side === 'admin' ? 'dp-dot-admin' : 'dp-dot-customer')));
      b.append(document.createTextNode(page.name));
      /* Read by the existing data-track opt-in in analytics.js — no change
         to that file is needed. */
      b.dataset.track = 'preview_page';
      b.dataset.industry = KEY;
      b.dataset.page = page.id;
      b.dataset.side = page.side;
      tabs.append(b);
      return b;
    });

    /* One panel, swapped in place. The panel wraps the CAPTION as well as the
       mockup — the caption is the only content a screen reader can read, so a
       panel containing only the aria-hidden mockup would be an empty shell.
       No aria-live: a correct tab pattern already announces the change through
       aria-selected, and a live region on top of it announces twice. */
    pane.id = 'dp-panel';
    pane.setAttribute('role', 'tabpanel');
    pane.tabIndex = 0;

    let current = 0;
    const show = (i) => {
      current = i;
      const page = pages[i];
      buttons.forEach((b, j) => {
        b.setAttribute('aria-selected', j === i ? 'true' : 'false');
        b.tabIndex = j === i ? 0 : -1;
      });
      pane.setAttribute('aria-labelledby', buttons[i].id);
      pane.replaceChildren(renderMock(page, ctx), renderCaption(page));
    };

    buttons.forEach((b, i) => b.addEventListener('click', () => show(i)));

    tabs.addEventListener('keydown', (e) => {
      const last = buttons.length - 1;
      let next = null;
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') next = current === last ? 0 : current + 1;
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') next = current === 0 ? last : current - 1;
      else if (e.key === 'Home') next = 0;
      else if (e.key === 'End') next = last;
      if (next === null) return;
      e.preventDefault();
      show(next);
      buttons[next].focus();
    });

    body.append(tabs, pane);
    frame.append(bar, body);

    root.replaceChildren(head, legend);
    if (data.note) root.append(el('p', 'dp-note', data.note));
    root.append(frame);
    show(0);
  };

  const load = () => {
    fetch('assets/design-preview.json')
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(r.status))))
      .then((all) => {
        if (all[KEY]) build(all[KEY]);
      })
      .catch(() => {
        /* Leave the placeholder empty. A failed fetch must not leave a broken
           frame or a reserved gap on the page. */
      });
  };

  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          io.disconnect();
          load();
        }
      },
      { rootMargin: '600px' }
    );
    io.observe(root);
  } else {
    load();
  }
})();
