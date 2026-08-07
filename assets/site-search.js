/* ============================================================
   Site search — client-side, no backend, no build step.

   Matching is plain substring, deliberately. Thai does not put
   spaces between words, so token-based matching would need a
   segmenter; substring is both simpler and more accurate here.
   Each entry carries hidden keywords (`k`) so "หมอฟัน" finds the
   dental clinic and "ราคา" finds the packages.

   The index is fetched on first focus rather than on load, so it
   never competes with LCP. The results panel is absolutely
   positioned, so opening it cannot shift layout.
   ============================================================ */
(() => {
  'use strict';

  const MIN_QUERY = 2;
  const MAX_RESULTS = 8;

  const COPY = {
    th: { empty: 'ไม่พบผลลัพธ์สำหรับ', count: n => `พบ ${n} รายการ`, none: 'ไม่พบผลลัพธ์' },
    en: { empty: 'No results for', count: n => `${n} results`, none: 'No results' }
  };

  const lang = (document.documentElement.lang || 'th').toLowerCase().startsWith('en') ? 'en' : 'th';
  const copy = COPY[lang];

  let index = null;
  let loading = null;

  function loadIndex() {
    if (index) return Promise.resolve(index);
    if (loading) return loading;
    loading = fetch('assets/search-index.json')
      .then(r => (r.ok ? r.json() : Promise.reject(new Error(r.status))))
      .then(data => { index = data[lang] || data.th || []; return index; })
      .catch(() => { index = []; return index; });
    return loading;
  }

  const norm = s => s.toLowerCase().trim();

  function search(q) {
    const needle = norm(q);
    if (needle.length < MIN_QUERY || !index) return [];
    const scored = [];
    for (const row of index) {
      const title = norm(row.t);
      const keys = norm(row.k || '');
      let score;
      if (title.startsWith(needle)) score = 0;
      else if (title.includes(needle)) score = 1;
      else if (keys.includes(needle)) score = 2;
      else continue;
      scored.push({ row, score });
    }
    scored.sort((a, b) => a.score - b.score);
    return scored.slice(0, MAX_RESULTS).map(s => s.row);
  }

  const escapeHtml = s => s.replace(/[&<>"']/g, c =>
    ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

  function highlight(text, q) {
    const i = norm(text).indexOf(norm(q));
    if (i < 0) return escapeHtml(text);
    return escapeHtml(text.slice(0, i))
      + '<mark>' + escapeHtml(text.slice(i, i + q.length)) + '</mark>'
      + escapeHtml(text.slice(i + q.length));
  }

  let instances = 0;

  function init(root) {
    /* The markup used to be repeated in all 61 files. The page now supplies
       an empty <div class="site-search"></div> and this fills it, so the
       widget's structure lives in exactly one place. Placement stays in the
       HTML because it differs per page family — .nav-inner on home-shell
       pages, .page-shell nav on portfolio-pages ones, plus a second copy
       inside .nav-mobile-panel. */
    if (!root.querySelector('input[type="search"]')) {
      const en = lang === 'en';
      root.innerHTML =
        '<div class="site-search-field">' +
          '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="M20 20l-3.6-3.6"/></svg>' +
          '<input type="search" autocomplete="off" role="combobox" aria-expanded="false" aria-autocomplete="list"' +
          ' aria-label="' + (en ? 'Search this site' : 'ค้นหาในเว็บไซต์') + '"' +
          ' placeholder="' + (en ? 'Search work, services, pricing…' : 'ค้นหาผลงาน บริการ ราคา…') + '" />' +
        '</div>' +
        '<div class="site-search-panel" role="listbox" aria-label="' +
          (en ? 'Search results' : 'ผลการค้นหา') + '" hidden></div>' +
        '<p class="site-search-status" role="status" aria-live="polite"></p>';
    }

    const input  = root.querySelector('input[type="search"]');
    const panel  = root.querySelector('.site-search-panel');
    const status = root.querySelector('.site-search-status');
    if (!input || !panel || !status) return;

    /* There are two instances on the page — the desktop navbar and the mobile
       panel — so ids have to be namespaced or the two listboxes collide and
       aria-activedescendant points at the wrong element. */
    const uid = 'ss' + (instances++);
    panel.id = uid + '-results';
    input.setAttribute('aria-controls', panel.id);

    let options = [];
    let active = -1;

    const close = () => {
      panel.hidden = true;
      input.setAttribute('aria-expanded', 'false');
      input.removeAttribute('aria-activedescendant');
      active = -1;
    };

    const setActive = i => {
      if (!options.length) return;
      if (active >= 0) options[active].setAttribute('aria-selected', 'false');
      active = (i + options.length) % options.length;
      const el = options[active];
      el.setAttribute('aria-selected', 'true');
      input.setAttribute('aria-activedescendant', el.id);
      el.scrollIntoView({ block: 'nearest' });
    };

    function render(q, rows) {
      if (!rows.length) {
        panel.innerHTML = '<p class="site-search-empty">' + copy.empty + ' “' + escapeHtml(q) + '”</p>';
        status.textContent = copy.none;
        options = [];
        active = -1;
        panel.hidden = false;
        input.setAttribute('aria-expanded', 'true');
        return;
      }

      let html = '';
      let group = null;
      let n = 0;
      for (const row of rows) {
        if (row.g !== group) {
          group = row.g;
          html += '<div class="site-search-group" role="presentation">' + escapeHtml(group) + '</div>';
        }
        html += '<a class="site-search-option" role="option" aria-selected="false" id="' + uid + '-opt-' + n
              + '" href="' + escapeHtml(row.u) + '" data-track="search_result_click">'
              + highlight(row.t, q) + '</a>';
        n++;
      }
      panel.innerHTML = html;
      options = [...panel.querySelectorAll('.site-search-option')];
      active = -1;
      status.textContent = copy.count(options.length);
      panel.hidden = false;
      input.setAttribute('aria-expanded', 'true');
    }

    let debounce;
    input.addEventListener('input', () => {
      clearTimeout(debounce);
      const q = input.value;
      if (norm(q).length < MIN_QUERY) { close(); return; }
      debounce = setTimeout(() => {
        loadIndex().then(() => {
          if (norm(input.value).length < MIN_QUERY) return;
          render(input.value, search(input.value));
          window.__track?.('nav_search', { query: input.value });
        });
      }, 120);
    });

    input.addEventListener('focus', loadIndex, { once: true });

    input.addEventListener('keydown', e => {
      if (e.key === 'Escape') { close(); input.blur(); return; }
      if (panel.hidden || !options.length) return;
      if (e.key === 'ArrowDown') { e.preventDefault(); setActive(active + 1); }
      else if (e.key === 'ArrowUp') { e.preventDefault(); setActive(active - 1); }
      else if (e.key === 'Enter' && active >= 0) { e.preventDefault(); options[active].click(); }
      else if (e.key === 'Home') { e.preventDefault(); setActive(0); }
      else if (e.key === 'End') { e.preventDefault(); setActive(options.length - 1); }
    });

    document.addEventListener('click', e => { if (!root.contains(e.target)) close(); });
    root.addEventListener('focusout', () => {
      setTimeout(() => { if (!root.contains(document.activeElement)) close(); }, 0);
    });
  }

  const start = () => document.querySelectorAll('.site-search').forEach(init);
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', start);
  else start();
})();
