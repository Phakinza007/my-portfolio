/* ============================================================
   analytics.js — Microsoft Clarity loader + click tracking
   Shared across every page (see CLAUDE.md → Analytics).
   Add `<script src="/assets/analytics.js" defer></script>`
   before </head> on any new page.
============================================================ */
(() => {
  const CLARITY_PROJECT_ID = '__CLARITY_PROJECT_ID__';
  const DEBUG = /[?&]cl_debug\b/.test(location.search);

  /* ---- Clarity loader (official async snippet) ---- */
  (function (c, l, a, r, i, t, y) {
    c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
    t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
    y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
  })(window, document, 'clarity', 'script', CLARITY_PROJECT_ID);

  /* ---- track(): fire a custom Clarity event + optional tags ---- */
  const track = (name, tags = {}) => {
    window.clarity?.('event', name);
    Object.entries(tags).forEach(([key, value]) => {
      if (value != null) window.clarity?.('set', key, String(value));
    });
    if (DEBUG) console.log('[track]', name, tags);
  };
  window.__track = track;

  /* ---- classify a clicked <a>/<button> and fire the right event ---- */
  const HIGH_INTENT = new Set(['cta_fastwork', 'contact_email', 'resume_download']);

  const classify = (el) => {
    const explicit = el.dataset?.track;
    if (explicit) return { name: explicit, tags: { ...el.dataset } };

    if (el.matches('.filter-btn')) {
      return { name: 'project_filter', tags: { filter: el.dataset.filter } };
    }

    const href = el.getAttribute?.('href');
    if (!href) return null;

    if (href.includes('fastwork.co/byob')) {
      const section = el.closest('section[id], footer, nav');
      return { name: 'cta_fastwork', tags: { cta_location: section?.id || section?.tagName.toLowerCase() || 'unknown' } };
    }
    if (href.includes('fastwork.co/user')) {
      return { name: 'fastwork_profile', tags: {} };
    }
    if (href.startsWith('mailto:')) {
      return { name: 'contact_email', tags: {} };
    }
    if (href.endsWith('.pdf')) {
      return { name: 'resume_download', tags: {} };
    }
    if (/(^|\/)showcase-[^/]+\.html/.test(href)) {
      return { name: 'showcase_open', tags: { project: href.split('/').pop() } };
    }
    if (/(^|\/)case-study-[^/]+\.html/.test(href)) {
      return { name: 'case_study_open', tags: { project: href.split('/').pop() } };
    }
    if (el.matches('.work-thumb, .btn-live')) {
      return { name: 'project_open', tags: { project: href.split('/').pop() || href } };
    }
    return null;
  };

  document.addEventListener('click', (e) => {
    const el = e.target.closest('a, button');
    if (!el) return;
    const hit = classify(el);
    if (!hit) return;
    track(hit.name, hit.tags);
    if (HIGH_INTENT.has(hit.name)) window.clarity?.('upgrade', 'high_intent');
  }, true);
})();
