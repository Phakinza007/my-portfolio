# Portfolio → Full-Time Web Development Service — Design

## Context

The site (`index.html`) currently reads as a portfolio with services attached: the hero leads with "I build landing pages and dashboards," the CTA is "See My Work," and the three service cards are thin (one paragraph + a Fastwork link, no price, no proof). Every CTA funnels to Fastwork.

Phakin is moving from freelancing as a side activity to taking on web development work full-time, and wants the site itself to read as an active service business rather than a work sample gallery — both to convert visitors who already have a referral or found the site through Fastwork, and to start ranking for Thai search queries ("รับทำเว็บไซต์", "รับทำ landing page") that portfolio-style copy doesn't target.

**Two things are explicitly out of scope**, decided during brainstorming:
- No new contact channels (LINE OA, Facebook Page) — the existing contact form (Formspree) and `mailto:` link already satisfy "direct contact alongside Fastwork."
- No fabricated social proof — testimonials come from Phakin's real Fastwork buyer reviews (screenshotted from `fastwork.co/user/u106pl4r`), pricing comes from his real Fastwork package listings. Nothing here is invented copy.

**Addendum (found during plan review):** two more real problems surfaced before implementation started, both now folded into this spec/plan rather than spawning a separate cycle, since they're small and bounded:

1. **About section undersells the stack.** `#about` currently says "I work in HTML and CSS," while the hero's tech marquee shows React/Node.js/Express/PostgreSQL and the Selected Work filter has a "Full Stack" tag with 5 projects. A Thai SME owner reading About alone would reasonably conclude "static pages only." Fix: reword to state the frontend + Node.js backend capability directly (Task 7 in the implementation plan).
2. **Full-page language toggle is a separate, larger project.** The site's Hero/About/Experience/Projects/Case Studies serve a dual audience — Thai SME clients from Fastwork (who bounce off an all-English hero) and English-reading recruiters/clients (LinkedIn/GitHub). A real fix is a site-wide TH/EN toggle, not just translating Hero+Services. That's materially bigger than this spec (new toggle mechanism, translating ~13 project cards, About, Experience, Case Studies, Contact, Footer) and is deliberately **out of scope here** — sequenced as its own follow-up brainstorming/spec/plan cycle after this pivot ships.

## Goals

1. Hero and site framing sound like an established, full-time web development practice — not a student portfolio.
2. Services section shows real starting prices and turnaround times per package, so visitors can self-qualify before contacting.
3. Real testimonials (3 five-star Fastwork reviews) appear on the site for credibility.
4. Services/Pricing/Testimonials content is in Thai, since that's the language of the real reviews and pricing, and the language local clients search in. The rest of the site (Hero, About, Experience, Selected Work, Case Studies) stays English — no full site translation.

## Non-goals

- No new pages — everything lands in `index.html`'s existing single-page structure.
- No LINE/Facebook integration.
- No schema.org `Review`/`AggregateRating` markup for the testimonials. Google's structured-data policies are strict about self-hosted review markup representing third-party review platforms (Fastwork, not the portfolio itself) — misusing it risks a manual action. The reviews render as plain styled content, with a visible link back to the Fastwork profile so visitors can verify them independently. That link back also does double duty as a trust signal.
- No change to the existing Contact section — it already has a working form + `mailto:`, and stays in English.

## Content Plan

### 1. Hero (rewrite, English)

Current:
> "I build landing pages and dashboards for founders and small businesses — clean, fast, and ready to make the right first impression. Hire me directly on Fastwork."

New direction: same visual layout (no structural change to the metric-card mockup on the right), but copy shifts from "here's what I've built" to "I'm open for business right now":
- `hero-eyebrow`: from "Web Development Services" → something that signals an active practice, e.g. "Freelance Web Development" stays, or sharpens to "Now Taking New Projects."
- `hero-desc`: rewritten to state directly that Phakin is now taking on web development work full-time, names the three service lines (landing pages, dashboards, business websites), and points at the price transparency below.
- CTAs stay two buttons: `Hire Me on Fastwork` (primary, unchanged) and `See My Work` → reconsider pointing this at `#services` (pricing) instead of `#projects`, since the immediate next thing a convinced visitor needs is "how much / how long," not more portfolio browsing. Portfolio stays one scroll away either way via nav.

Exact new copy gets finalized during implementation (writing-plans / implementation), following this direction — not fixed word-for-word here.

### 2. Services & Pricing (rewrite, Thai)

Replaces the current 3 plain cards in `#services` with pricing cards built from Phakin's real Fastwork package copy, condensed for a scannable web card (not the full marketplace listing text). Each card:

- Title (Thai)
- Starting price (large, prominent — e.g. "เริ่มต้น ฿3,900")
- Turnaround time
- 3–4 condensed highlight bullets (cut from the fuller Fastwork description down to what a first-time visitor needs to decide)
- CTA row: `Hire Me on Fastwork` + a secondary link to `#contact`

**Landing Page / Sale Page** — ฿3,900, 5–7 วัน
- พัฒนาใหม่ทั้งหมด ไม่ใช้เทมเพลตสำเร็จรูป
- 1 หน้า ไม่เกิน 6 section, ลงข้อมูล/รูปภาพให้ครบ
- รองรับมือถือและคอมพิวเตอร์ทุกหน้าจอ
- แก้ไขได้ 2 รอบ, ฟรีแก้ไขปัญหา 3 เดือน

**Dashboard UI** — ฿7,900, 7–10 วัน
- ออกแบบหน้าจอระบบสูงสุด 5 หน้าจอ พร้อมชุดสี/ฟอนต์/ดีไซน์ระบบ
- ส่งไฟล์ออกแบบฉบับเต็ม พร้อมให้ทีมพัฒนาต่อได้ทันที
- แก้ไขได้ 2 รอบหลังส่งแบบ
- Note: พัฒนาเป็นระบบใช้งานจริงเพิ่มเติม เริ่มต้น ฿15,900

**Business Website** — ฿9,900, 10–14 วัน
- พัฒนาใหม่ 100%, 3–5 หน้า (หน้าแรก/บริการ/เกี่ยวกับเรา/ผลงาน/ติดต่อ)
- วางโครงสร้างรองรับ SEO พื้นฐาน
- ฟอร์มติดต่อ/ปุ่ม LINE OA สำหรับรับลูกค้าของลูกค้าเอง (a deliverable *for the client's* site, unrelated to our own LINE-removal decision above)
- แก้ไขได้ 2 รอบ, ฟรีแก้ไขปัญหา 3 เดือน
- Small note under the card: ลูกค้าสามารถสอบถามเพิ่มเติมได้ เช่น ระบบหลังบ้าน ระบบจองคิว ระบบสมาชิก หรือเชื่อมต่อ LINE แจ้งเตือน/แชทบอท

Section heading/label also localize (e.g. `section-label`: "บริการ", `section-title`: "บริการและราคา").

### 3. Testimonials (new section, Thai)

New `<section id="testimonials">` inserted between Services and Selected Work. Three cards, each showing:
- 5.0 star rating (visual, static — five filled stars, not an interactive widget)
- Quote (as given):
  - ppxyb58z: "ผลงานดีมากค่ะ"
  - Pornsawan PT.: "เริ่ดมากแปปเดียวเสร็จ งานตามบรีฟ"
  - namfon.upwt: "มีความตั้งใจ งานไว แนะนำเลยค้า"
- Attribution: the Fastwork username as shown, tagged "รีวิวจาก Fastwork" (not presented as a full real name — these are already Fastwork handles, not invented)

Section includes one link to the Fastwork profile (`https://fastwork.co/user/u106pl4r`) so the reviews are independently verifiable — framed as "ดูรีวิวทั้งหมดบน Fastwork →".

Nav gets one new entry ("Reviews", linking `#testimonials`) alongside the existing Services/Projects/About/Experience/Case Studies/Contact, in both the header nav and footer nav — consistent with how every other named section is already linked.

### 4. Unchanged

Tech stack marquee, Selected Work (13 cards), About, Experience, Case Studies, Contact section, Footer — no content changes. The Contact section's lead line ("The fastest way to hire me is on Fastwork — or send a message below...") already covers the "direct contact alongside Fastwork" goal; no edit needed there.

## SEO

- `index.html` meta description already contains one Thai keyword ("รับทำเว็บไซต์") folded into an English sentence. Update it to lead more clearly with the Thai service terms now that there's real Thai content on the page to back it up, while keeping it truthful to the page content (no keyword stuffing).
- No new pages, so `sitemap.xml` doesn't need new entries — same URL, richer content.
- Explicitly skipping `Review`/`AggregateRating` JSON-LD (see Non-goals) — the existing `WebSite`/`Person` JSON-LD block stays as is.

## Visual/Component Notes

Reuses the existing `.card` / `.works-grid` pattern already used by Services and Selected Work, extended with:
- A price/duration sub-row (new, small CSS addition — not a new design system)
- A simple 5-star glyph row for testimonials (static SVG or CSS, no third-party rating widget)

Follows existing tokens (`--accent: #5274f8`, existing type scale) — no new color or font introduced. Both new sections must pass the same bars as the rest of the site: Lighthouse 100/100/100 (Accessibility/Best Practices/SEO) and no horizontal overflow at 375×812.

## Files Touched

- `index.html` — hero copy, services section (rewrite to pricing cards, Thai), new testimonials section (Thai), nav + footer nav (new "Reviews" link), meta description tweak.
- `CLAUDE.md` — update the "Pages & Sections" table to add the Testimonials section, and note that Services now includes pricing.
- `sitemap.xml` — no change (same URL).

## Verification

- Visual check in browser at desktop and 375×812 mobile widths for both new/changed sections.
- Mobile overflow check per `CLAUDE.md`'s standard snippet (`canScrollX: false`).
- Lighthouse audit (mobile, navigation) on the local preview — must hold 100/100/100 on Accessibility/Best Practices/SEO.
- Manual read-through of the new Thai copy for tone/correctness (Phakin as native speaker) before merging.
