# Improve loop — backlog

Candidates for the next iteration, **Rejected** with reasons below them.
Re-measure before picking: `python3 _tools/loop-scan.py`.

An item here is a candidate, not a commitment. One per iteration.

---

## Open — DRIFT (fix before adding anything new)

- [x] ~~`CLAUDE.md` says 18 cards; `index.html` has 20~~ — done in iteration 2, along with
      sixteen other stale present-tense counts.
- [ ] **Extend `scan_docs()` in `_tools/loop-scan.py` to assert the rest of CLAUDE.md's
      counts** — showcase files, `assets/thumbs/`, TH/EN pairs, `search-index.json` entries,
      `.story-card`s, `web-*` pages, contextual-nav files. Iteration 2 corrected seventeen
      figures that only one of them was being checked; the other sixteen were found by a
      human following that one line. Cheap to assert, and it stops the section rotting again.
- [x] ~~`showcase-supplymate` has no `short` copy~~ — done in iteration 1,
      together with the `check-copy.py` parser bug that hid it.
- [ ] **`resume.html` / `resume-en.html` link five GitHub repos with their own
      blurbs**, three for projects culled from the site on 2026-07-22
      (`phakin-task-manager`, `phakin-knowledge-ai`, `phakin-invenflow`). Read
      them against CLAUDE.md → "resume.html / resume-en.html still state the
      opposite": those two pages still carry Node/Express/JWT/REST claims and a
      `full-stack` bio line that the rest of the site retired on 2026-08-12, and
      the PDF at `assets/resume-phakin-chawanpunya.pdf` is the honest document to
      correct them against. This is the largest remaining true/false gap on the
      site and it is copy, not code.
- [x] ~~4 meta descriptions over 190 chars~~ — done in iteration 3, after fixing the scan
      to count decoded length (`&quot;` is 6 characters in the file and 1 on screen).
- [ ] **`scan_plumbing()` measures `name="description"` only.** `showcase-salon-os-en` was
      shipping a different string in `name=` than in `og:`/`twitter:`, and nothing could see
      it. Compare the three per page.

## Open — GAP, ranked by what a buyer hits

- [x] ~~`dashboard-ui` shows 1 project~~ — done in iteration 4 by wiring in SALON OS, which
      was already tagged `Dashboard`. Two files, nothing built. Now at 2.
- [x] ~~`showcase-salon-os` absent from `web-booking`~~ and ~~`showcase-supplymate` absent
      from `web-shop`~~ — both wired in iteration 5. Each card's own `data-industry` already
      named that page's key, so it was a link, not a judgment call. `scan_strip_coverage()`
      now asserts this for all seven industry pages.
- [ ] **`web-gym` shows 1** (Iron Republic) and **`web-solar` shows 1** (SolarPeak).
      Measured in iteration 5: **no existing demo carries either key**, so unlike every other
      thin strip these two are real builds, not missing links. Use **portfolio-new-proof**,
      and ask the owner first — which sector, and what the demo should prove. `web-solar` also
      has no `#need` tile; it is reached from `services` only.
- [ ] **`web-construction` / `web-organization` / `web-restaurant` show 2 each.** Thin, not
      broken, and `scan_strip_coverage()` says no unlinked demo exists for any of them.
- [ ] **3 card tags have no sidebar button** — `Creative Studio`, `React`,
      `React Bits` (all Signalform's), so they are filterable by nobody. The
      harmless direction; the dangerous direction (a button with no card) is
      clean and the scan asserts it every run.

## Open — new proof pieces (use the **portfolio-new-proof** skill)

Justified by the `GAP` block above, in value order. One demo can fill two strips
at once, which is what makes the first of these the best-value work on the site.

- [ ] **A second dashboard demo** → fills `dashboard-ui` (1 project, the ฿7,900
      package's only proof) *and* an industry `#related` if it is built for a
      specific sector. Named in `CLAUDE.md` as the obvious next gap.
- [ ] **A second gym demo** → `web-gym` (Iron Republic alone).
- [ ] **A second solar demo** → `web-solar` (SolarPeak alone). Note `web-solar`
      has no `#need` tile either; it is reached from `services` only.

## Open — needs a browser, so the scan will never raise it

- [ ] **Re-read each showcase page against the demo it describes.** A showcase
      describes a demo and nothing re-reads it when the demo is redesigned; the
      BuildNest "SVG instead of stock photography" copy stayed true-when-written
      and false-after for six days across 13 files. `baan-talay` and `SalonOS`
      are the newest and so the most likely to have drifted from their pages.
- [ ] **Lighthouse the two newest pages**, mobile *and* desktop.
- [ ] **Clarity**: which showcase pages get `showcase_open` and never
      `cta_fastwork`. That ratio is what put `.story-price` on all 38 showcases.

---

## Rejected — do not re-propose without asking the owner

These are decisions, not oversights. Each was taken deliberately; re-opening one
spends an iteration arguing with an answer that already exists.

- **English twins for the 8 `web-*` pages.** The search intent
  (`รับทำเว็บคลินิก`) is Thai-only; an `-en` twin doubles the file count for
  traffic that does not exist.
- **English twins for the 20 demo pages.** A demo simulates a client's site;
  both languages link to the same file.
- **Portfolio chrome on demo pages** — the "← Back to Portfolio" pill and the
  site search. Deleted 2026-08-07 on purpose: a demo must not wear the
  portfolio's furniture. If getting out of a demo becomes a real problem the fix
  is `target="_blank"`, never the pill.
- **More than six `#need` tiles.** Owner's call 2026-08-08: solar, association
  and "ไม่แน่ใจ" came out. Both still reachable from `services`.
- **Chasing Best Practices above 77.** Microsoft Clarity sets third-party
  cookies; that is analytics-vs-score, a deliberate trade.
- **`404.html` SEO above 66.** `is-crawlable` fails on `robots: noindex`, which
  is correct for a 404 page.
- **`.nojekyll` instead of `_config.yml`.** Looks like the same fix, does the
  opposite: it would newly expose `_docs/` and `assets/_archive/`.
- **Notification toggles in `BookEase.html` made to "work".** There is no
  backend and the page must never claim one; `saveSettingsBtn` naming them as
  needing an integration is the honest version.
- **A before/after slider or any identifiable face on `lumi-clinic.html`.** The
  page argues in its own copy that before/after photos are easy to fake.
- **A photograph on `bandairaek-foundation.html` or `pathapee-precast.html`.**
  Each refuses photography for its own stated reason — beneficiaries' privacy,
  and a span table respectively. Do not merge the two rationales.
- **A demo appended to `web-organization`'s first `#related` group.** That
  eyebrow says `งานลูกค้าจริง`; one more link under it turns a true sentence
  false.
