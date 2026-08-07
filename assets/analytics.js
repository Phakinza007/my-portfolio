/* ============================================================
   analytics.js — Microsoft Clarity loader + click tracking
   Shared across every page (see CLAUDE.md → Analytics).
   Add `<script src="assets/analytics.js?v=funnel" defer></script>`
   before </head> on any new page (relative path, not absolute).
============================================================ */
(() => {
  const CLARITY_PROJECT_ID = 'xxos49tnj8';
  const DEBUG = /[?&]cl_debug\b/.test(location.search);

  /* Development traffic must never reach the real project. Checked on
     2026-08-08: of the ten most-visited URLs, six were localhost:8123 —
     91 of 157 visits were somebody building the site, not reading it.
     Left unguarded, that noise becomes indistinguishable from buyers the
     moment search traffic starts arriving. */
  const IS_LOCAL =
    /^(localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\])$/.test(location.hostname) ||
    location.protocol === 'file:';

  /* ---- Clarity loader (official async snippet) ---- */
  if (!IS_LOCAL) {
    (function (c, l, a, r, i, t, y) {
      c[a] = c[a] || function () { (c[a].q = c[a].q || []).push(arguments); };
      t = l.createElement(r); t.async = 1; t.src = 'https://www.clarity.ms/tag/' + i;
      y = l.getElementsByTagName(r)[0]; y.parentNode.insertBefore(t, y);
    })(window, document, 'clarity', 'script', CLARITY_PROJECT_ID);
  }

  /* ---- track(): fire a custom Clarity event + optional tags ----
     The listeners below still run locally so `?cl_debug` can verify the
     instrumentation without sending anything; window.clarity is simply
     undefined there and every call is optional-chained. */
  const track = (name, tags = {}) => {
    window.clarity?.('event', name);
    Object.entries(tags).forEach(([key, value]) => {
      if (value != null) window.clarity?.('set', key, String(value));
    });
    if (DEBUG) console.log('[track]', name, tags, IS_LOCAL ? '(local — not sent)' : '');
  };
  window.__track = track;

  /* Where on the page a link was clicked. The same industry page is reachable
     from the #need tiles, the nav and a project strip; without this they are
     one undifferentiated number. */
  const originOf = (el) => {
    if (el.closest('.need-grid')) return 'need_tile';
    if (el.closest('.crumbs')) return 'breadcrumb';
    if (el.closest('.project-strip')) return 'project_strip';
    if (el.closest('.story-links')) return 'story_links';
    if (el.closest('nav, .navbar')) return 'nav';
    if (el.closest('footer')) return 'footer';
    const section = el.closest('section[id]');
    return section?.id || 'body';
  };

  /* ---- classify a clicked <a>/<button> and fire the right event ----
     URLs are extensionless as of 2026-08-07 (GitHub Pages resolves /foo to
     foo.html). The patterns below therefore treat `.html` as OPTIONAL rather
     than required — the old `\.html` anchors matched nothing the moment the
     links were rewritten, and every funnel event would have silently stopped
     firing with no error anywhere. */
  const HIGH_INTENT = new Set(['cta_fastwork', 'contact_email', 'resume_download']);

  const classify = (el) => {
    const explicit = el.dataset?.track;
    if (explicit) return { name: explicit, tags: { ...el.dataset } };

    if (el.matches('.filter-btn')) {
      return { name: 'project_filter', tags: { filter: el.dataset.filter } };
    }
    if (el.matches('.tag-btn')) {
      return { name: 'tag_filter', tags: { tag: el.dataset.tag } };
    }
    if (el.matches('#featured-toggle')) {
      return { name: 'featured_toggle', tags: { pressed: el.getAttribute('aria-pressed') } };
    }

    const href = el.getAttribute?.('href');
    if (!href) return null;

    if (href.includes('fastwork.co/byob')) {
      return { name: 'cta_fastwork', tags: { cta_location: originOf(el) } };
    }
    if (href.includes('fastwork.co/user')) {
      return { name: 'fastwork_profile', tags: {} };
    }
    if (href.startsWith('mailto:')) {
      return { name: 'contact_email', tags: { origin: originOf(el) } };
    }
    if (href.startsWith('tel:')) {
      return { name: 'contact_phone', tags: { origin: originOf(el) } };
    }
    if (href.endsWith('.pdf')) {
      return { name: 'resume_download', tags: {} };
    }
    /* The industry pages are the whole search strategy and were untracked.
       Must be tested before the generic showcase/case-study rules — those
       patterns do not overlap, but the origin tag is what makes this useful. */
    if (/(^|\/)web-[a-z-]+(\.html)?(?=[#?]|$)/.test(href)) {
      const m = href.match(/web-([a-z-]+?)(?:\.html)?(?=[#?]|$)/);
      return { name: 'industry_open', tags: { industry: m ? m[1] : 'unknown', origin: originOf(el) } };
    }
    if (/(^|\/)(landing-page|dashboard-ui|business-website)(-en)?(\.html)?(?=[#?]|$)/.test(href)) {
      const m = href.match(/(landing-page|dashboard-ui|business-website)/);
      return { name: 'package_open', tags: { package: m ? m[1] : 'unknown', origin: originOf(el) } };
    }
    if (/(^|\/)showcase-[^/#?]+/.test(href)) {
      return { name: 'showcase_open', tags: { project: href.split('/').pop(), origin: originOf(el) } };
    }
    if (/(^|\/)case-study-[^/#?]+/.test(href)) {
      return { name: 'case_study_open', tags: { project: href.split('/').pop() } };
    }
    if (el.matches('.work-thumb, .btn-live') || el.closest('.story-links')) {
      return { name: 'project_open', tags: { project: href.split('/').pop() || href, origin: originOf(el) } };
    }
    /* Last, so a breadcrumb pointing at an industry page still records
       industry_open with origin=breadcrumb rather than being flattened here.
       This only catches the ancestor hops — usually "/" and services.html. */
    if (el.closest('.crumbs')) {
      return { name: 'breadcrumb_nav', tags: { to: href.split('/').pop() || 'home' } };
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

  /* ---- Archive keyword search ----
     Typing is not a click. Fired once the visitor stops for 1.2s so a
     six-character query is one event, not six. */
  const search = document.getElementById('work-search');
  if (search) {
    let timer;
    search.addEventListener('input', () => {
      clearTimeout(timer);
      timer = setTimeout(() => {
        const q = search.value.trim();
        if (q.length >= 2) track('work_search', { query: q.slice(0, 40) });
      }, 1200);
    });
  }
})();
