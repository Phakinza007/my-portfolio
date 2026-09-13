# Improve loop — backlog

Candidates for the next iteration, **Rejected** with reasons below them.
Re-measure before picking: `python3 _tools/loop-scan.py`.

An item here is a candidate, not a commitment. One per iteration.

---

## Open — DRIFT (fix before adding anything new)

- [ ] **`CLAUDE.md` says 18 cards; `index.html` has 20.** Two demos landed after
      it was last updated (`SalonOS.html`, `baan-talay.html`) and the Selected
      Work table, the `other 5` / `ทั้งหมด` counts prose and the thumbnail tally
      all need re-reading against the DOM. Read the numbers off the files, never
      off the table.
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
- [ ] **4 meta descriptions over 190 chars** — `SalonOS` (206),
      `showcase-baan-talay` (195), `showcase-baan-talay-en` (236),
      `showcase-salon-os-en` (214). Trim, don't rewrite: this is the owner's copy.

## Open — GAP, ranked by what a buyer hits

- [ ] **`dashboard-ui.html` / `-en` shows 1 project.** The ฿7,900 package has
      the least proof of the three, against `landing-page`'s 9. Named in
      `CLAUDE.md` as the obvious next gap, and still open. A second dashboard
      demo fixes the package page *and* an industry page at once.
- [ ] **`web-gym.html` shows 1** (Iron Republic alone).
- [ ] **`web-solar.html` shows 1** (SolarPeak alone). `web-solar` also has no
      `#need` tile — it reaches visitors through `services.html` only.
- [ ] **`web-construction` / `web-organization` / `web-restaurant` /
      `web-shop` show 2 each.** Thin, not broken.
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
