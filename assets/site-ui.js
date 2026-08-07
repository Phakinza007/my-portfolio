/* ============================================================
   Shared UI behaviour for the 12 portfolio pages.

   Three self-guarding blocks. Each returns early when its
   elements are absent, so one file serves every page.

   This file exists because work.html once shipped with all 13
   cards at opacity:0 and a dead hamburger — the reveal observer
   and nav handler were simply not copied across with the filter
   block, and Lighthouse, the overflow check and the dead-link
   sweep all passed anyway. With one shared file there is nothing
   left to forget to copy.

   NOT for the demo pages. Those are simulated client sites and
   carry their own, deliberately different reveal implementations.
   ============================================================ */
(() => {
  'use strict';

  /* Both user-visible string sets are chosen from <html lang> rather than
     hard-coded, which is what lets the Thai and English copies merge. */
  const EN = (document.documentElement.lang || 'th').toLowerCase().startsWith('en');

  /* ---- Scroll reveal with stagger ---- */
  const reveals = document.querySelectorAll('.reveal');
  if (reveals.length) {
    if ('IntersectionObserver' in window) {
      const obs = new IntersectionObserver((entries) => {
        entries.forEach(e => {
          if (!e.isIntersecting) return;
          /* Cards in a grid stagger in one after another by column index */
          const siblings = [...(e.target.parentElement?.children ?? [])];
          e.target.style.transitionDelay = (siblings.indexOf(e.target) % 3) * 90 + 'ms';
          e.target.classList.add('visible');
          /* Drop the delay once it has played so hover stays instant */
          setTimeout(() => { e.target.style.transitionDelay = ''; }, 700);
          obs.unobserve(e.target);
        });
      }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
      reveals.forEach(el => obs.observe(el));
    } else {
      reveals.forEach(el => el.classList.add('visible'));
    }
  }

  /* ---- Mobile nav drawer ---- */
  const toggle = document.querySelector('.nav-toggle');
  const panel  = document.getElementById('mobile-panel');
  if (toggle && panel) {
    const NAV = EN
      ? { open: 'Open navigation', close: 'Close navigation' }
      : { open: 'เปิดเมนู',          close: 'ปิดเมนู' };

    const shut = () => {
      panel.classList.remove('open');
      toggle.setAttribute('aria-expanded', 'false');
      toggle.setAttribute('aria-label', NAV.open);
    };

    toggle.addEventListener('click', () => {
      const open = panel.classList.toggle('open');
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? NAV.close : NAV.open);
    });

    /* Close on in-page link tap */
    panel.querySelectorAll('a[href^="#"]').forEach(a => a.addEventListener('click', shut));

    /* Close when clicking outside the nav */
    document.addEventListener('click', (e) => {
      if (panel.classList.contains('open') &&
          !panel.contains(e.target) &&
          !toggle.contains(e.target)) shut();
    });
  }

  /* ---- Work filter: one axis, industry ---- */
  const filterBtns = document.querySelectorAll('.filter-btn');
  const cards      = document.querySelectorAll('.work-card[data-industry]');
  if (filterBtns.length && cards.length) {
    const COPY = EN
      ? { none: 'No projects match',
          some: n => 'Showing ' + n + ' of ' + cards.length + ' projects' }
      : { none: 'ไม่พบผลงานที่ตรงกับที่ค้นหา',
          some: n => 'แสดง ' + n + ' จาก ' + cards.length + ' ผลงาน' };

    const emptyState   = document.getElementById('works-empty');
    const filterStatus = document.getElementById('filter-status');
    const chip         = document.getElementById('active-filter-chip');
    const chipLabel    = document.getElementById('active-filter-label');
    const chipClear    = document.getElementById('active-filter-clear');

    /* Archive-only controls. Absent on index.html, where both predicates
       stay inert and the filter behaves exactly as it did before. */
    const search  = document.getElementById('work-search');
    const featBtn = document.getElementById('featured-toggle');
    let activeFilter = 'all';
    let featuredOnly = false;

    const industriesOf = card => (card.dataset.industry || '').trim().split(/\s+/).filter(Boolean);
    const matches = (card, filter) => filter === 'all' || industriesOf(card).includes(filter);

    /* The card's text is already in the DOM, so the query needs no index
       fetch. Substring and case-insensitive, like the site search — Thai has
       no word spaces, so segmenting would be heavy and error-prone. */
    const matchesQuery = (card, q) =>
      !q || (card.textContent || '').replace(/\s+/g, ' ').toLowerCase().includes(q);

    /* Counts are derived from the DOM so they can never drift out of date. */
    filterBtns.forEach(btn => {
      const countEl = btn.querySelector('.filter-count');
      if (!countEl) return;
      let n = 0;
      cards.forEach(card => { if (matches(card, btn.dataset.filter)) n++; });
      countEl.textContent = String(n);
    });

    function applyFilter(filter, label) {
      let visible = 0;

      filterBtns.forEach(b => {
        const on = b.dataset.filter === filter;
        b.classList.toggle('active', on);
        b.setAttribute('aria-pressed', on ? 'true' : 'false');
      });

      /* Three independent predicates, ANDed: category, keyword, featured. */
      const q = (search?.value || '').trim().toLowerCase();
      cards.forEach(card => {
        const show = matches(card, filter)
                  && matchesQuery(card, q)
                  && (!featuredOnly || card.dataset.featured);
        if (show) {
          delete card.dataset.hidden;
          visible++;
        } else {
          card.dataset.hidden = '';
        }
      });

      if (chip) {
        const show = filter !== 'all';
        chip.hidden = !show;
        if (show && chipLabel) chipLabel.textContent = label;
      }

      if (emptyState) emptyState.hidden = visible > 0;
      if (filterStatus) filterStatus.textContent = visible === 0 ? COPY.none : COPY.some(visible);
    }

    filterBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        activeFilter = btn.dataset.filter;
        applyFilter(activeFilter, btn.dataset.label || '');
      });
    });

    /* The keyword box and the featured toggle re-run the filter against
       whichever category is currently active, rather than resetting it. */
    const rerun = () => {
      const btn = document.querySelector('.filter-btn[data-filter="' + activeFilter + '"]');
      applyFilter(activeFilter, btn?.dataset.label || '');
    };

    search?.addEventListener('input', rerun);
    search?.addEventListener('keydown', (e) => {
      if (e.key === 'Escape') { search.value = ''; rerun(); }
    });

    featBtn?.addEventListener('click', () => {
      featuredOnly = !featuredOnly;
      featBtn.setAttribute('aria-pressed', String(featuredOnly));
      rerun();
    });

    chipClear?.addEventListener('click', () => {
      activeFilter = 'all';
      applyFilter('all', '');
      document.querySelector('.filter-btn[data-filter="all"]')?.focus();
    });

    /* The archive shows its count on screen, so it needs filling before the
       first click. Tied to the search box — index.html's #filter-status is
       sr-only, and writing to an aria-live region on load would make a
       screen reader announce a result count nobody asked for. */
    if (search) applyFilter(activeFilter, '');

    /* The sidebar ships open so it is a column on desktop; on a phone that
       would push the grid down by the height of nine buttons, so collapse it
       there. Not a media query, because <details> hides its own children and
       CSS cannot reliably reopen them. */
    const sidebar = document.querySelector('.work-filter');
    if (sidebar && window.matchMedia('(max-width: 900px)').matches) {
      sidebar.open = false;
    }
  }
})();
