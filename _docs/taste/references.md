# Taste library — project & case-study pages

Collected 2026-08-24 for the showcase-template redesign
(`docs/superpowers/specs/2026-08-24-showcase-work-first-design.md`).

**Why this file exists.** `CLAUDE.md` is 115 KB of rules about what not to do. Until
this file there was no artifact anywhere in the repo stating what the pages should
*aim at*. The one exception was `lumi-clinic.html`, whose palette runs off a written
scene in a comment above `:root` — and CLAUDE.md calls it out as "the one demo with a
written direction". This generalises that.

**Selection rule.** WebGL and video-driven agency sites were excluded on purpose.
This site is vanilla HTML/CSS holding Lighthouse 100, so a reference that cannot be
built that way is not a reference, it is a distraction. `basement.studio` was opened
and rejected on exactly this ground.

`(browser)` = opened and looked at. `(fetched)` = structure read, not rendered.

---

## Group 1 — chrome silent, work loud

### 1. Pentagram — De Bijloke *(browser)*
<https://www.pentagram.com/work/de-bijloke>

`h1` is the project name, black on white. One subtitle line: *"A new identity for De
Bijloke, a beloved music centre in Ghent."* Two tags. A single `About the project +`
control folding the long copy away. Then the work, full-bleed, immediately.

- **Take:** the ratio. Almost nothing between arriving and seeing the work.
- **Take:** progressive disclosure as an alternative to cutting copy — the reader who
  wants the story opens it; the one who wants the work is not made to wade.
- **Leave:** the image volume. Pentagram has a dozen photographs per project. We have
  one screenshot, which is why the disclosure pattern was *not* adopted — we would be
  hiding our only substance.

### 2. Rauno Freiberg — Craft *(fetched)*
<https://rauno.me/craft>

Per entry: image, title, month/year, one link. No paragraph anywhere.

- **Take:** one line is enough when the image is doing the work.
- **Leave:** nothing closes. This site has to sell.

### 3. Brian Lovin *(fetched)*
<https://brianlovin.com/>

Title plus a descriptor under ten words. No dates, no categories, no tags.
*"App Dissection — Breaking down well-designed apps"* is the entire positioning of a
whole section, in one sentence.

- **Take:** a section can be introduced once, in six words, instead of once per item.

---

## Group 2 — headings that belong to the work

### 4. Linear — Ramp ⭐ *(fetched)*
<https://linear.app/customers/ramp>

No eyebrow. The `h1` **is the conclusion**: *"The coding agent behind 60% of Ramp's
merged PRs."* Then a facts block — Company / Founded / Switched / Company size — then
section headings written for this customer alone: *"How Ramp built a coding agent for
its own stack"*, *"How Inspect scaled AI workflows at Ramp"*.

- **Take:** a scannable facts block beats a paragraph of context.
- **Take:** headings are where the writing effort belongs, not where it is saved.
- **Leave:** the metric. This site has no measured numbers and CLAUDE.md forbids
  reaching for a substitute.
- **Status:** the heading half is *deferred, not refuted* — ~136 new heading strings,
  and it costs the cross-page scan consistency CLAUDE.md defends on purpose.

### 5. Matt Orton *(secondary — via uxfol.io)*
<https://uxfol.io/68ea8622>

One pink accent, and case-study titles written to be read rather than to label.

---

## Group 3 — the counter-evidence, kept deliberately

### 6. Emil Kowalski ⚠️ *(fetched)*
<https://emilkowal.ski/>

Every project gets **identical** typographic treatment. No per-entry colour, no icons,
no visual differentiation of any kind. The restraint is the argument: it forces
content quality to carry the weight.

- **This is the direct counter-argument to per-project accent colour.** It is why that
  idea was dropped.

### 7. Locomotive ⚠️ *(fetched)*
<https://www.locomotive.ca/en/work>

45 projects, one neutral palette. Differentiated by name, industry and city, a
paragraph, service tags, year, award count.

- 45 entries can hold together with no per-project colour at all.

### 8. Instrument *(fetched)*
<https://www.instrument.com/work>

`Case Study` label, client name, tagline, category tags, CTA.

- The only reference in the set that still carries the kind of label being deleted —
  and the most template-looking page of the eight. Kept as the negative control.

---

## Group 4 — practitioner guidance

### 9. uxfol.io — UX case study design tips
<https://blog.uxfol.io/ux-portfolio-design-tips/>

Confirms per-project accent is standard practice in UX portfolios: *"select one or two
main colors from the project"*. Carries the guardrail that matters more than the
practice — **choose one accent role** (links, or subheads, or figures — not all three).

Not adopted here, but the one-role rule is worth keeping if it ever is.

---

## What the set agrees on

**Eight of eight carry no kicker, and none spends more than one line framing the work
before showing it.** Instrument's `Case Study` label is the sole exception, on the
page that reads most like a template.

## Where the set splits

Per-project visual identity. Pentagram lets the work's own imagery carry it; Emil and
Locomotive refuse identity entirely and let uniformity carry it.

They are not actually opposed — **all three make the chrome silent.** They differ only
in what fills the space. Pentagram fills it with the work. Emil fills it with nothing.
This site was filling it with scaffolding, which is the defect.

The decision taken was Pentagram's half: show more of the work, stop talking around it.
