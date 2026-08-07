# Industry Page Depth — closing the content gap on the 7 `web-*.html` pages

**Date:** 2026-08-07
**Status:** Approved, ready for implementation planning

This is **piece 1 of 4** in the search-visibility work. The others — structured data beyond
FAQ, a `/blog/`, and adding LINE as a contact channel — get their own spec and plan. Piece 1
is first because it is the only one of the four that moves ranking directly.

## Context

The seven `web-*.html` pages target Thai buyer intent and are aimed correctly: each `<title>`
and `<h1>` is the search phrase itself (`รับทำเว็บคลินิก และคลินิกความงาม`). Technically the
site is in good shape — Accessibility 100, SEO 100, CLS 0, no remote requests.

What they are not is deep enough. Measured 2026-08-07:

| | Body copy |
|---|---|
| `web-clinic.html` and its six siblings | ~2,100–2,600 characters (~400–600 Thai words) |
| `chercode.com/website/clinic`, ranking on page 1 | ~2,500–3,000 words across 15 sections |

The ranking page carries a problems section, a four-tier price table, a process, an eight-item
FAQ, a comparison table, guarantees, add-ons and three contact channels. Ours carries four
sections: `#overview` (606 chars), `#related` (452), `#faq` (812, four questions), `#cta` (210).

**Roughly a fifth of the content of what already ranks.**

The other page-1 results — `cz.co.th`, `wantalkmarketing.com`, `moveonmarketing.com` — are all
`.co.th` agencies pricing ฿19,900–25,900. None is a freelancer. Our ฿3,900 is not a small
undercut of that field; it is a different bracket, and no page on the site says so plainly.

## The constraint that shapes everything

**There are no real clients.** Confirmed by the owner on 2026-08-07: all thirteen projects are
self-directed design work. `CLAUDE.md` records the same thing.

All seven pages currently label their project list `ผลงานจริง` — *real work*. A buyer choosing
someone to build a clinic site reads that as *has built clinic sites for clients*. Tripling the
trust-building copy on top of that claim would multiply the problem, so the wording is corrected
as part of this work, not after it.

This also rules out anything the pages cannot support: no client counts, no delivered-project
totals, no named clients, no testimonials beyond the three real Fastwork reviews the site
already links to.

## Goals

1. Take each page from ~2,300 to roughly **6,000 characters** of body copy — comparable to what
   ranks, without padding.
2. Make the ฿3,900-versus-฿19,900 gap explicit, since it is the one thing no page-1 competitor
   can answer.
3. Answer the questions a buyer actually asks before hiring, so the page earns the visit even
   when it does not yet rank.
4. Say what the work is, accurately.

## Non-goals

- **No PDPA content.** The owner does not currently do anything about it, and a page that
  implies otherwise to a clinic would be worse than silence. Revisit when it is true.
- **No new CSS.** Everything is built from components `assets/portfolio-pages.css` already has.
- **No `-en` siblings.** These pages are Thai-only by design — see `CLAUDE.md`.
- **No invented facts.** Price, timeline, revisions, domain and hosting terms come from the
  category pages and `faq.html`, which are the existing sources of truth.
- **No `Review` / `AggregateRating` schema.** Deliberately avoided site-wide; that decision
  stands.

## Decisions

### D1 — Six sections, four of them new

Final order per page. `.study-meta` and the hero stay as they are.

| Section | Status | Component | Target |
|---|---|---|---|
| `#problem` | **new** | `.study-block.featured` + `.highlight-list` | ~700 chars |
| `#overview` | expand | `.study-grid` of two `.study-block`s | ~1,200 chars |
| `#included` | **new** | `.study-grid`, two blocks: what is and is not in the price | ~900 chars |
| `#compare` | **new** | `.study-grid`, three blocks | ~1,100 chars |
| `#process` | **new** | `.decision-list` + `.decision-number` | ~800 chars |
| `#related` | reword | `.project-strip` | unchanged |
| `#faq` | expand 4 → 8 | `.study-block` + `<h3>` | ~1,600 chars |
| `#cta` | keep | `.result-band` | unchanged |

### D2 — The comparison is three cards, not a table

The natural shape is a four-column table, but `portfolio-pages.css` has no table style —
`.timeline-row` is a fixed two-column grid — and a four-column table at 375 px either scrolls
sideways or collapses into something unreadable. `.study-grid` of three `.study-block`s is the
same information, already responsive, and needs no new CSS.

The three are **ฟรีแลนซ์ (ผม) · เอเจนซี่ · เว็บสำเร็จรูป**, compared on price, timeline, who
does the work, and what happens after handover. **No competitor is named**; the agency column
describes the ฿19,900–25,900 bracket the page-1 results occupy, which is verifiable and fair.
The freelance column states the real trade-offs too — one person, no account manager, no
24-hour support line — because a comparison that only flatters one side reads as advertising
and converts worse.

### D3 — `ผลงานจริง` becomes accurate

The eyebrow above `#related` changes on all seven pages to **`ตัวอย่างงานออกแบบ`**, and the
section heading names it plainly: these are pieces built to demonstrate the approach, not client
engagements. The `.project-strip` entries themselves are unchanged.

The three real Fastwork reviews stay the only social proof, linked as they already are.

Two showcase pages (`showcase-lumi-clinic`, `showcase-dental-clinic`) also omit the word
`คอนเซปต์` that their siblings use. That inconsistency is **noted, not fixed here** — it is a
separate sweep across 26 files and does not belong in this plan.

### D4 — `FAQPage` JSON-LD ships with the FAQ

Each page grows to eight questions, and `faq.html` already demonstrates the markup. Adding the
JSON-LD now costs nothing extra and makes the pages eligible for FAQ rich results; doing it in
piece 2 would mean opening the same seven files twice.

This is the one piece of structured-data work that belongs here rather than in its own spec.

### D5 — Content comes from what the site already states

Nothing is authored from scratch where a source exists:

| Fact | Source |
|---|---|
| ฿3,900 · 5-7 วัน · แก้ 2 รอบ + ฟรีแก้บั๊ก 3 เดือน | `.study-meta` on the category and industry pages |
| Domain and host are the customer's, not in the price | `faq.html` |
| No monthly retainer; post-handover additions are new work | `faq.html` |
| Payment and dispute handling via Fastwork | `faq.html` |
| Per-industry features | each page's existing `#overview` |
| Project descriptions | the `.work-problem` copy, already verbatim across the site |

Per-industry sections — the problems, the process wording, four new FAQs each — are written for
this work and are the only genuinely new copy.

### D6 — Keyword targeting adds the price angle

Each page currently targets one head phrase. The new sections give natural room for the
long-tail variants that a one-day-old domain can realistically reach first:
`รับทำเว็บคลินิก ราคาถูก`, `ทำเว็บคลินิก งบน้อย`, `ฟรีแลนซ์ รับทำเว็บคลินิก`.

These go in body copy and `<h3>`s, **not** in the `<title>` or `<h1>`, which are already correct
and should not be diluted. No meta-description rewrite; they are accurate as they stand.

## What this does not do

Ranking is not on-page work alone, and this spec should not be read as promising a position.
The domain went live on 2026-08-06. It has no backlinks and no history. What this work does is
remove the reason a search engine would prefer a competitor **on content grounds**, which is the
part that can be built. The rest — time, links, Google Business Profile, published articles —
is the owner's, and is tracked as pieces 2–4 plus the off-page checklist.

## Verification

1. **Character count per page** ≥ 5,500, measured with tags and scripts stripped.
2. **No page claims a client.** `grep` for `ผลงานจริง`, `ลูกค้าจริง`, `เคยทำให้` returns nothing.
3. **No PDPA mention** anywhere in the seven files.
4. **Every price, timeline and revision figure matches** the category pages, checked by diff of
   the extracted `.study-meta` strings.
5. **Valid `FAQPage`** on all seven: JSON parses, question count equals the rendered `<h3>`
   count, and every `acceptedAnswer` is non-empty.
6. **No new CSS** — `git diff --stat assets/portfolio-pages.css` is empty.
7. **Lighthouse** on two of the seven: Accessibility 100, SEO 100, CLS 0. Best Practices caps
   at 77 (Clarity cookies).
8. **No overflow at 375 × 812**, iframe recipe with `clientWidth === 375` confirmed first.
9. **Nav and search still present** — these pages carry `portfolio-pages.css`'s `.page-shell nav`
   and the search placeholder; the rewrite must not drop them.

## Files touched

**Modified:** the seven `web-*.html` files, `CLAUDE.md`

**Untouched:** `assets/portfolio-pages.css`, every other page, `sitemap.xml` (no new URLs)
