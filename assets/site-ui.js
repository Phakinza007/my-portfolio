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

  const REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;

  /* Both user-visible string sets are chosen from <html lang> rather than
     hard-coded, which is what lets the Thai and English copies merge. */
  const EN = (document.documentElement.lang || 'th').toLowerCase().startsWith('en');

  /* ---- Homepage work-card spotlight ----
     The homepage alone opts in through .hero-ambient. This keeps the archive
     and every other home-shell page still, and a fine-pointer media query
     prevents touch devices from doing work for an effect they cannot use. */
  if (!REDUCED && document.querySelector('.hero-ambient') &&
      matchMedia('(hover: hover) and (pointer: fine)').matches) {
    document.querySelectorAll('.works-grid > .work-card').forEach((card) => {
      let frame = 0;
      let x = 50;
      let y = 50;

      const paint = () => {
        card.style.setProperty('--spotlight-x', x + '%');
        card.style.setProperty('--spotlight-y', y + '%');
        frame = 0;
      };

      const position = (event) => {
        const rect = card.getBoundingClientRect();
        x = ((event.clientX - rect.left) / rect.width) * 100;
        y = ((event.clientY - rect.top) / rect.height) * 100;
        if (!frame) frame = requestAnimationFrame(paint);
      };

      card.addEventListener('pointerenter', (event) => {
        card.classList.add('is-spotlit');
        position(event);
      });
      card.addEventListener('pointermove', position);
      card.addEventListener('pointerleave', () => {
        card.classList.remove('is-spotlit');
        if (frame) {
          cancelAnimationFrame(frame);
          frame = 0;
        }
      });
    });
  }


  /* ---- Copy the email on click ----
     Enhances the mailto links already on the page rather than needing new
     markup, and keeps the href: plenty of people want their mail client, and
     on a phone selecting an address by dragging is genuinely hard. Only wired
     up where the Clipboard API exists, so nothing is promised that cannot be
     delivered. */
  if (navigator.clipboard) {
    document.querySelectorAll('a[href^="mailto:"]').forEach((a) => {
      const address = a.getAttribute('href').slice(7).split('?')[0];
      if (!address) return;
      a.addEventListener('click', (e) => {
        if (e.metaKey || e.ctrlKey || e.shiftKey || e.button !== 0) return;
        e.preventDefault();
        navigator.clipboard.writeText(address).then(() => {
          const was = a.dataset.copied;
          a.dataset.copied = EN ? 'Copied' : 'คัดลอกแล้ว';
          clearTimeout(+was || 0);
          setTimeout(() => delete a.dataset.copied, 1800);
        }).catch(() => { location.href = a.getAttribute('href'); });
      });
    });
  }

  /* ---- Reading progress ----
     Turned on by page length, not by a class, so no page has to remember to
     opt in. The threshold is four viewports: below that the scrollbar already
     answers "how much is left" and a second indicator is noise. web-clinic is
     7,104 characters over ten sections, which is where this earns its keep. */
  if (document.documentElement.scrollHeight > innerHeight * 4) {
    const bar = document.createElement('div');
    bar.className = 'read-progress';
    bar.innerHTML = '<i></i>';
    bar.setAttribute('aria-hidden', 'true');   /* decorative: scroll position is already exposed */
    document.body.appendChild(bar);
    const fill = bar.firstElementChild;
    let ticking = false;
    const paint = () => {
      const max = document.documentElement.scrollHeight - innerHeight;
      fill.style.transform = 'scaleX(' + (max <= 0 ? 1 : Math.min(1, scrollY / max)) + ')';
      ticking = false;
    };
    addEventListener('scroll', () => {
      if (!ticking) { ticking = true; requestAnimationFrame(paint); }
    }, { passive: true });
    paint();
  }

  /* ---- Section rail ----
     Built from the sections that are already there, so adding or reordering a
     section needs no second edit. Five is the floor: fewer than that and the
     rail lists things the reader can already see. It is a real <nav> with
     aria-current, not decorative dots. */
  const railSections = [...document.querySelectorAll('main > section[id]')]
    .filter((sec) => sec.querySelector('h2'));
  if (railSections.length >= 5) {
    const nav = document.createElement('nav');
    nav.className = 'section-rail';
    nav.setAttribute('aria-label', EN ? 'On this page' : 'หัวข้อในหน้านี้');
    railSections.forEach((sec) => {
      const a = document.createElement('a');
      a.href = '#' + sec.id;
      a.textContent = sec.querySelector('h2').textContent.trim();
      nav.appendChild(a);
    });
    document.body.appendChild(nav);
    const links = [...nav.children];
    if ('IntersectionObserver' in window) {
      const spy = new IntersectionObserver((entries) => {
        entries.forEach((e) => {
          if (!e.isIntersecting) return;
          links.forEach((a) => {
            const here = a.getAttribute('href') === '#' + e.target.id;
            a.classList.toggle('here', here);
            if (here) a.setAttribute('aria-current', 'true');
            else a.removeAttribute('aria-current');
          });
        });
      }, { rootMargin: '-15% 0px -70% 0px' });
      railSections.forEach((sec) => spy.observe(sec));
    }
  }

  /* ---- Hero screenshot skeleton ----
     The 28 showcase / case-study pages open on a ~115 KB JPEG. Its box is
     already reserved by the img's width/height attributes, so nothing moves
     and CLS stays 0 — but the reserved box sat empty while the file arrived,
     which reads as a stalled page rather than a loading one.

     This only ever ADDS an attribute the stylesheet keys a shimmer off. It is
     never set when the image is already complete (a cached image would flash a
     skeleton it does not need), and it is removed on load, on error, and on a
     timer. If this file 404s the attribute is never set at all and the pages
     look exactly as they did before, which is why the skeleton lives behind an
     attribute rather than the image living behind a class. */
  document.querySelectorAll('.browser-frame > img').forEach((img) => {
    if (img.complete) return;
    const frame = img.parentElement;
    frame.dataset.loading = '';
    /* The timer is the backstop the count-up above had to learn the hard way:
       a load event that never fires would otherwise shimmer forever. */
    let timer = 0;
    const done = () => { clearTimeout(timer); delete frame.dataset.loading; };
    timer = setTimeout(done, 8000);
    img.addEventListener('load', done, { once: true });
    img.addEventListener('error', done, { once: true });
  });

  /* ---- Count-up on .study-meta figures ----
     The real value is already in the HTML; this only counts up to it. So with
     JS off, with reduced motion on, or if this file 404s, the reader sees the
     true number immediately — which matters because several of these figures
     are prices, and a price caught mid-count reads as a smaller price. The
     run is kept short for the same reason. */
  const figures = document.querySelectorAll('[data-countup]');
  if (figures.length && 'IntersectionObserver' in window &&
      !matchMedia('(prefers-reduced-motion: reduce)').matches) {
    const numOf = (t) => Number(String(t).replace(/[^0-9]/g, ''));
    const io = new IntersectionObserver((entries) => {
      entries.forEach((e) => {
        if (!e.isIntersecting) return;
        io.unobserve(e.target);
        const final = e.target.textContent;
        const target = numOf(final);
        if (!target) return;
        const grouped = /,/.test(final);
        const render = (n) => final.replace(/[\d,]+/,
          grouped ? n.toLocaleString('en-US') : String(n));
        const t0 = performance.now(), dur = 620;
        /* p is clamped at BOTH ends. It used to be `Math.min(1, …)` only, and
           a negative p renders a negative number: (1 - p) exceeds 1, cubing it
           exceeds 1, and `1 - that` goes below zero, so `target * p'` comes out
           the wrong side of nothing. Observed live on web-booking as
           **฿-325** where the real figure is ฿7,900.

           t can legitimately be earlier than t0: t0 is performance.now() at
           the moment the observer fires, while the rAF timestamp is the START
           of the frame being rendered. An observer that fires mid-frame gets a
           t that predates its own t0. It is a coin flip on frame timing, not a
           rare edge case, and it lands on the one number these pages exist to
           state. */
        const step = (t) => {
          const p = Math.min(1, Math.max(0, (t - t0) / dur));
          e.target.textContent = render(Math.round(target * (1 - Math.pow(1 - p, 3))));
          if (p < 1) requestAnimationFrame(step);
          else e.target.textContent = final;
        };
        /* Backstop: the true figure is restored on a timer as well as on the
           last frame. rAF stops in a background tab and can be starved by a
           busy main thread, and the only thing that ever put the real number
           back was the final frame — so an interrupted run left a wrong price
           on screen until reload. Setting it twice is harmless; not setting it
           at all is not. */
        setTimeout(() => { e.target.textContent = final; }, dur + 600);
        requestAnimationFrame(step);
      });
    }, { rootMargin: '0px 0px -10% 0px' });
    figures.forEach((f) => io.observe(f));
  }

  /* ---- Scroll reveal with stagger ----
     The hidden state is scoped to .js-reveal on <html>, set here, so a page
     that ships .reveal markup without this file renders visible instead of
     blank. work.html once went out with all 13 cards at opacity 0 for exactly
     that reason, and Lighthouse still scored 100 because opacity-0 elements
     stay in the accessibility tree. Adding the class from JS makes that
     failure structurally impossible rather than a thing to remember. */
  const reveals = document.querySelectorAll('.reveal');
  if (reveals.length) {
    document.documentElement.classList.add('js-reveal');
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
    const tagBtns = document.querySelectorAll('.tag-btn');
    let activeFilter = 'all';
    let featuredOnly = false;
    let activeTag    = '';

    const industriesOf = card => (card.dataset.industry || '').trim().split(/\s+/).filter(Boolean);
    const matches = (card, filter) => filter === 'all' || industriesOf(card).includes(filter);

    /* The card's text is already in the DOM, so the query needs no index
       fetch. Substring and case-insensitive, like the site search — Thai has
       no word spaces, so segmenting would be heavy and error-prone. */
    const matchesQuery = (card, q) =>
      !q || (card.textContent || '').replace(/\s+/g, ' ').toLowerCase().includes(q);

    /* data-tags is pipe-separated because eight of the labels contain a
       space ("Fine Dining", "Full Stack", "Light UI", …). */
    const tagsOf = card => (card.dataset.tags || '').split('|').filter(Boolean);
    const matchesTag = (card, t) => !t || tagsOf(card).includes(t);

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

      /* Four independent predicates, ANDed: category, keyword, tag, featured. */
      const q = (search?.value || '').trim().toLowerCase();
      cards.forEach(card => {
        const show = matches(card, filter)
                  && matchesQuery(card, q)
                  && matchesTag(card, activeTag)
                  && (!featuredOnly || card.dataset.featured);
        if (show) {
          delete card.dataset.hidden;
          /* next frame, so the browser has a layout to transition *from* */
          requestAnimationFrame(() => delete card.dataset.leaving);
          visible++;
        } else {
          card.dataset.leaving = '';
          /* display:none only after the fade, otherwise it cancels it */
          setTimeout(() => {
            if (card.dataset.leaving === '') card.dataset.hidden = '';
          }, REDUCED ? 0 : 260);
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

    /* One tag at a time, and clicking the pressed one clears it — the same
       shape as the category buttons, so the two read alike. */
    tagBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        activeTag = activeTag === btn.dataset.tag ? '' : btn.dataset.tag;
        tagBtns.forEach(b => b.setAttribute('aria-pressed', String(b.dataset.tag === activeTag)));
        rerun();
      });
    });

    chipClear?.addEventListener('click', () => {
      activeFilter = 'all';
      activeTag = '';
      tagBtns.forEach(b => b.setAttribute('aria-pressed', 'false'));
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
