# Improve loop — backlog

Candidates for the next iteration, **Rejected** with reasons below them.
Re-measure before picking: `python3 _tools/loop-scan.py`.

An item here is a candidate, not a commitment. One per iteration.

---

## Open — DRIFT (fix before adding anything new)

- [x] ~~`CLAUDE.md` says 18 cards; `index.html` has 20~~ — done in iteration 2, along with
      sixteen other stale present-tense counts.
- [x] ~~Extend `scan_docs()` to assert the rest of CLAUDE.md's counts~~ — done in iteration
      9: 14 counts asserted, all passing, with a planted-value control for three of them.
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
- [x] ~~Compare the three description tags per page~~ — done in iteration 9 as
      `scan_description_trio()`, family-relative after two absolute rules proved too noisy.

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

- [x] ~~Re-read the two newest showcase pages against their demos~~ — done in iteration 6.
      19 claims checked on `showcase-salon-os` and `showcase-baan-talay`; **both clean**.
- [x] ~~Sweep the other 17 showcase pages for photography and backend claims~~ — done in
      iteration 7; found and removed the `Full Stack` label in all five of its
      representations.
- [x] ~~Read the remaining claim types on the other 17 pairs~~ — done in iteration 8. Every
      numeric and negative claim this repo can check is true. Same class, unchecked. Two
      notes from iteration 6 that make it cheaper: `baan-talay` keeps its code in
      `assets/baan-talay.js` (the `.html` is a 4.6 KB shell), so check what a page *loads*
      before concluding a feature is missing; and a grep for a forbidden call matches the
      comment forbidding it.
- [ ] **Lighthouse the two newest pages**, mobile *and* desktop.
- [ ] **Clarity**: which showcase pages get `showcase_open` and never
      `cta_fastwork`. That ratio is what put `.story-price` on all 38 showcases.

---

## Open — questions only the owner can answer

- [ ] **`showcase-solarpeak`: are `assets/solar/*.jpg` your own on-site photographs?** The
      page says *"ภาพถ่ายหน้างานจริง ไม่ใช่ภาพสต็อก"*. The photos exist; their provenance is
      not knowable from the repo, and this site has shipped stock/Unsplash images before. If
      they are stock, that sentence needs to go — it is the page's own point of distinction.
- [ ] **`showcase-habitquest`: does the deployed app really have user accounts and persistent
      storage?** The page says so and calls itself *"ไม่ใช่ demo แบบ static"*. It is hosted
      from another repo, so nothing here can confirm it — and it is the only project on the
      site whose copy asserts a real backend, against the site-wide rule that none do.
- [ ] **A second demo for `web-gym` or `web-solar`** — the last two real GAPs (1 link each, no
      existing demo carries either key). Needs a sector choice and what the demo should prove
      before **portfolio-new-proof** can start.

## Open — the owner's pending pass, do not start unasked

- [ ] **The `full-stack` positioning line on `index` / `about` / `resume` (± `-en`)**, plus the
      resume pages' Node/Express/JWT/REST JSON-LD and the "9 Node.js + Express REST APIs"
      figure. CLAUDE.md records this as the owner's own pending pass and the PDF at
      `assets/resume-phakin-chawanpunya.pdf` as the honest document to correct against. It is
      positioning about him, not a claim about one project, so iteration 7 left it alone even
      while removing the per-project `Full Stack` label. Ask before touching.

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
