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
      ? { none: 'No projects in this category yet', some: n => 'Showing ' + n + ' projects' }
      : { none: 'ยังไม่มีผลงานในหมวดนี้',            some: n => 'แสดง ' + n + ' ผลงาน' };

    const emptyState   = document.getElementById('works-empty');
    const filterStatus = document.getElementById('filter-status');
    const chip         = document.getElementById('active-filter-chip');
    const chipLabel    = document.getElementById('active-filter-label');
    const chipClear    = document.getElementById('active-filter-clear');

    const industriesOf = card => (card.dataset.industry || '').trim().split(/\s+/).filter(Boolean);
    const matches = (card, filter) => filter === 'all' || industriesOf(card).includes(filter);

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

      cards.forEach(card => {
        if (matches(card, filter)) {
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
      btn.addEventListener('click', () => applyFilter(btn.dataset.filter, btn.dataset.label || ''));
    });

    chipClear?.addEventListener('click', () => {
      applyFilter('all', '');
      document.querySelector('.filter-btn[data-filter="all"]')?.focus();
    });
  }
})();
