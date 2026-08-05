# Portfolio → Full-Time Web Service Pivot Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Rewrite `index.html`'s Hero and Services sections, add a new Testimonials section, and fix the About section's stale "HTML and CSS only" self-description so the site reads as an active, full-time, full-stack-capable web development business (real prices, real reviews) instead of a portfolio, per `docs/superpowers/specs/2026-08-05-service-pivot-design.md`.

**Architecture:** Single-file static site — no build step, no JS framework. All changes are direct edits to `index.html` (inline `<style>` block starting at line 41, HTML body). The existing `.card` / `.works-grid` component pattern (already used by Services and About) is reused and extended with new CSS classes for price/duration/bullet-list/testimonial display. The existing `.reveal` scroll-fade animation (driven by a single `document.querySelectorAll('.reveal')` call in the inline `<script>` at the bottom of `<body>`) applies automatically to any new element carrying the `reveal` class — no JS changes needed anywhere in this plan.

**Tech Stack:** Plain HTML/CSS/JS, no dependencies, no package manager. Verification uses the project's existing browser-based workflow (chrome-devtools MCP `lighthouse_audit`, and the mobile-overflow JS snippet), documented in `CLAUDE.md`.

## Global Constraints

- Accent color: `--accent: #5274f8` (defined in `index.html:55`) — reuse via `var(--accent)`, never hardcode a new color.
- No new pages, no new nav-anchor scheme beyond one addition (`#testimonials`) — everything stays in `index.html`.
- Services/Pricing/Testimonials copy is Thai. Hero, About, Experience, Selected Work, Case Studies, Contact stay English — do not translate them. (About gets one English wording correction in Task 7, not a translation.)
- Full-page TH/EN toggle is explicitly out of scope for this plan — sequenced as a separate follow-up project (see spec Addendum).
- No LINE/Facebook links, no schema.org `Review`/`AggregateRating` JSON-LD — per spec Non-goals.
- All pricing/testimonial content must match exactly what's in the spec (real Fastwork listing data) — no invented numbers or quotes.
- Every task must end with `html, body { overflow-x: hidden; }` still holding — the project's mobile-overflow bar (`CLAUDE.md`) must not regress.
- Lighthouse must hold 100/100/100 (Accessibility/Best Practices/SEO) on the final result.

---

### Task 1: Hero copy and meta description

**Files:**
- Modify: `index.html:6` (meta description)
- Modify: `index.html:1206-1213` (hero badge, eyebrow, description, CTAs)

**Interfaces:** None — pure text content, no new classes or IDs.

- [ ] **Step 1: Update the meta description**

Find (exact current line 6):
```html
  <meta name="description" content="Hire Phakin Chawanpunya on Fastwork — freelance web developer (รับทำเว็บไซต์) building landing pages, dashboards, and business websites, with live demos and case studies." />
```

Replace with:
```html
  <meta name="description" content="รับทำเว็บไซต์ ทำ Landing Page และ Dashboard UI เริ่มต้น 3,900 บาท — Phakin Chawanpunya นักพัฒนาเว็บฟรีแลนซ์ รับงานเต็มตัว พร้อมผลงานจริงและรีวิวจากลูกค้า" />
```

- [ ] **Step 2: Rewrite the hero badge, eyebrow, description, and secondary CTA**

Find (exact current lines 1206-1213):
```html
            <div class="avail-badge"><span class="avail-dot"></span> Taking new projects on Fastwork</div>
            <div class="hero-eyebrow">Web Development Services</div>
            <h1>Phakin<br>Chawanpunya</h1>
            <p class="hero-desc">I build landing pages and dashboards for founders and small businesses — clean, fast, and ready to make the right first impression. Hire me directly on Fastwork.</p>
            <div class="hero-ctas">
              <a class="btn btn-dark" href="https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob" target="_blank" rel="noopener noreferrer">Hire Me on Fastwork</a>
              <a class="btn btn-ghost" href="#projects">See My Work</a>
            </div>
```

Replace with:
```html
            <div class="avail-badge"><span class="avail-dot"></span> Taking new projects on Fastwork</div>
            <div class="hero-eyebrow">Full-Time Web Development</div>
            <h1>Phakin<br>Chawanpunya</h1>
            <p class="hero-desc">I run a focused web development practice — landing pages, dashboards, and business websites for founders and small businesses, with transparent pricing and fast turnaround. Now taking on new projects full-time.</p>
            <div class="hero-ctas">
              <a class="btn btn-dark" href="https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob" target="_blank" rel="noopener noreferrer">Hire Me on Fastwork</a>
              <a class="btn btn-ghost" href="#services">See Pricing</a>
            </div>
```

Note: the secondary CTA now points at `#services` instead of `#projects` (it used to say "See My Work"; the project grid is still one click away via the nav "Projects" link).

- [ ] **Step 3: Verify in browser**

Open `index.html` locally (e.g. `python3 -m http.server 8000` from the repo root, then visit `http://localhost:8000/index.html`). Confirm:
- Hero text reads the new copy, no leftover "See My Work" text.
- "See Pricing" button scrolls to the Services section.
- Browser tab title / view-source still shows the updated meta description.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "$(cat <<'EOF'
Rewrite hero copy and meta description for full-time positioning

Shifts the hero from portfolio framing ("see my work") to an active
service-business framing, and leads the meta description with Thai
service keywords now that real Thai pricing/review content backs it
up on the page.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 2: Services section → Thai pricing cards

**Files:**
- Modify: `index.html:689` (insert new CSS after `.card-link:hover`)
- Modify: `index.html:1362-1392` (replace the 3 existing service cards)

**Interfaces:**
- Produces CSS classes reused nowhere else in this plan: `.card-price`, `.card-duration`, `.card-list`, `.card-note`, `.card-cta-row`, `.card-cta-secondary`.
- Section `id="services"` and heading `id="services-heading"` are unchanged — the hero's "See Pricing" link (Task 1) and the nav's "Services" link both already point at `#services` and need no update.

- [ ] **Step 1: Add pricing-card CSS**

Find (exact current lines 688-691):
```html
    .card-link:hover { gap: 9px; }

    /* About photo */
    .about-photo {
```

Replace with:
```html
    .card-link:hover { gap: 9px; }

    .card-price {
      font-size: 1.5rem;
      font-weight: 800;
      color: var(--ink);
      letter-spacing: -0.01em;
      margin-bottom: 2px;
    }

    .card-duration {
      font-size: 0.82rem;
      color: var(--muted);
      margin-bottom: 16px;
    }

    .card-list {
      list-style: none;
      display: flex;
      flex-direction: column;
      gap: 9px;
      margin-bottom: 14px;
    }

    .card-list li {
      font-size: 0.9rem;
      color: var(--muted);
      line-height: 1.6;
      padding-left: 20px;
      position: relative;
    }

    .card-list li::before {
      content: "";
      position: absolute;
      left: 0;
      top: 0.55em;
      width: 6px;
      height: 6px;
      border-radius: 50%;
      background: var(--accent);
    }

    .card-note {
      font-size: 0.85rem;
      color: var(--muted-2);
      line-height: 1.6;
      margin-top: 10px;
      padding-top: 10px;
      border-top: 1px solid var(--border);
    }

    .card-cta-row {
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 14px;
      margin-top: 16px;
    }

    .card-cta-row .card-link { margin-top: 0; }

    .card-cta-secondary {
      display: inline-flex;
      align-items: center;
      font-size: 0.88rem;
      font-weight: 600;
      color: var(--muted);
      transition: color 150ms;
    }

    .card-cta-secondary:hover { color: var(--ink); }

    /* About photo */
    .about-photo {
```

- [ ] **Step 2: Replace the Services section HTML**

Find (exact current lines 1362-1392):
```html
    <section class="section" id="services" aria-labelledby="services-heading">
      <div class="container">
        <span class="section-label">Services</span>
        <h2 class="section-title" id="services-heading">What I Can Build for You</h2>

        <div class="works-grid">

          <div class="card reveal">
            <h3 class="card-title">Landing Page</h3>
            <p class="card-text">A one-page site that sells — hero, offer, social proof, and a clear call to action. Built for speed, SEO, and mobile from day one.</p>
            <p class="card-text">Good for: product launches, restaurants, clinics, gyms, local brands.</p>
            <a class="card-link" href="https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob" target="_blank" rel="noopener noreferrer">Start on Fastwork →</a>
          </div>

          <div class="card reveal">
            <h3 class="card-title">Dashboard UI</h3>
            <p class="card-text">Admin panels and data dashboards with KPI cards, tables, filters, and charts — numbers your team can actually read and act on.</p>
            <p class="card-text">Good for: booking systems, inventory, analytics, internal tools.</p>
            <a class="card-link" href="https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob" target="_blank" rel="noopener noreferrer">Start on Fastwork →</a>
          </div>

          <div class="card reveal">
            <h3 class="card-title">Business Website</h3>
            <p class="card-text">A multi-page company site — services, about, portfolio, and contact — that makes your business look established and easy to reach.</p>
            <p class="card-text">Good for: companies, agencies, personal brands, portfolios.</p>
            <a class="card-link" href="https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob" target="_blank" rel="noopener noreferrer">Start on Fastwork →</a>
          </div>

        </div>
      </div>
    </section>
```

Replace with:
```html
    <section class="section" id="services" aria-labelledby="services-heading">
      <div class="container">
        <span class="section-label">บริการ</span>
        <h2 class="section-title" id="services-heading">บริการและราคา</h2>

        <div class="works-grid">

          <div class="card reveal">
            <h3 class="card-title">Landing Page / Sale Page</h3>
            <div class="card-price">เริ่มต้น ฿3,900</div>
            <div class="card-duration">ระยะเวลา 5-7 วัน</div>
            <ul class="card-list">
              <li>พัฒนาใหม่ทั้งหมด ไม่ใช้เทมเพลตสำเร็จรูป</li>
              <li>1 หน้า ไม่เกิน 6 section ลงข้อมูลและรูปภาพให้ครบ</li>
              <li>รองรับการแสดงผลบนมือถือและคอมพิวเตอร์ทุกหน้าจอ</li>
              <li>แก้ไขงานได้ 2 รอบ ฟรีบริการแก้ไขปัญหา 3 เดือน</li>
            </ul>
            <div class="card-cta-row">
              <a class="card-link" href="https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob" target="_blank" rel="noopener noreferrer">เริ่มงานบน Fastwork →</a>
              <a class="card-cta-secondary" href="#contact">ติดต่อสอบถาม</a>
            </div>
          </div>

          <div class="card reveal">
            <h3 class="card-title">Dashboard UI</h3>
            <div class="card-price">เริ่มต้น ฿7,900</div>
            <div class="card-duration">ระยะเวลา 7-10 วัน</div>
            <ul class="card-list">
              <li>ออกแบบหน้าจอระบบสูงสุด 5 หน้าจอ</li>
              <li>พร้อมชุดสี ฟอนต์ และองค์ประกอบหลักของดีไซน์ ใช้ต่อได้ทั้งระบบ</li>
              <li>ส่งไฟล์ออกแบบฉบับเต็ม ทีมพัฒนานำไปทำต่อได้ทันที</li>
              <li>แก้ไขได้ 2 รอบหลังส่งแบบ</li>
            </ul>
            <div class="card-note">ต้องการพัฒนาเป็นระบบใช้งานจริง เริ่มต้น ฿15,900 — สอบถามเพิ่มเติมได้</div>
            <div class="card-cta-row">
              <a class="card-link" href="https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob" target="_blank" rel="noopener noreferrer">เริ่มงานบน Fastwork →</a>
              <a class="card-cta-secondary" href="#contact">ติดต่อสอบถาม</a>
            </div>
          </div>

          <div class="card reveal">
            <h3 class="card-title">Business Website</h3>
            <div class="card-price">เริ่มต้น ฿9,900</div>
            <div class="card-duration">ระยะเวลา 10-14 วัน</div>
            <ul class="card-list">
              <li>พัฒนาใหม่ 100% 3-5 หน้า (หน้าแรก บริการ เกี่ยวกับเรา ผลงาน ติดต่อ)</li>
              <li>วางโครงสร้างรองรับ SEO พื้นฐาน</li>
              <li>ฟอร์มติดต่อหรือปุ่ม LINE OA สำหรับรับลูกค้าของคุณ</li>
              <li>แก้ไขงานได้ 2 รอบ ฟรีบริการแก้ไขปัญหา 3 เดือน</li>
            </ul>
            <div class="card-note">ต้องการเพิ่มเติม เช่น ระบบหลังบ้าน ระบบจองคิว ระบบสมาชิก หรือเชื่อมต่อ LINE แจ้งเตือน/แชทบอท สอบถามได้</div>
            <div class="card-cta-row">
              <a class="card-link" href="https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob" target="_blank" rel="noopener noreferrer">เริ่มงานบน Fastwork →</a>
              <a class="card-cta-secondary" href="#contact">ติดต่อสอบถาม</a>
            </div>
          </div>

        </div>
      </div>
    </section>
```

- [ ] **Step 3: Verify in browser**

Reload `http://localhost:8000/index.html`. Confirm:
- Three pricing cards render in Thai with price, duration, bullet list, and a note line on the Dashboard UI and Business Website cards.
- Both buttons per card work: "เริ่มงานบน Fastwork →" opens Fastwork in a new tab, "ติดต่อสอบถาม" scrolls to `#contact`.
- Bullet markers show as small accent-colored dots (from `.card-list li::before`), not default browser bullets.
- At 375px width (mobile), cards stack to one column with no horizontal scroll (per `CLAUDE.md`'s overflow check — run the snippet from `CLAUDE.md` "Check mobile overflow" section and confirm `canScrollX: false`).

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "$(cat <<'EOF'
Turn Services into priced packages (Thai)

Replaces the three generic service cards with real pricing,
turnaround time, and package details pulled from Phakin's actual
Fastwork listings, in Thai to match the language of that content and
target Thai search queries.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 3: New Testimonials section

**Files:**
- Modify: `index.html:1392` (insert new CSS block after the Services-adjacent CSS added in Task 2 — see exact anchor below)
- Modify: `index.html` (insert new `<section id="testimonials">` between the Services section's closing `</section>` and the "SELECTED WORK" comment block)

**Depends on:** Task 2 — Step 1 below anchors its edit on the CSS that Task 2 Step 1 adds (`.card-cta-secondary:hover`), so Task 2 must be applied first.

**Interfaces:**
- Produces CSS classes: `.testimonial-stars`, `.testimonial-quote`, `.testimonial-author`, `.testimonial-source`, `.testimonials-footer`.
- Produces new section `id="testimonials"` — Task 4 (nav) links to this ID.
- Reuses `.sr-only`, already defined at `index.html:611` (visually-hidden-but-accessible pattern: `position:absolute; width:1px; height:1px; clip:rect(0,0,0,0)` etc.) — do not redefine it.

- [ ] **Step 1: Add testimonial CSS**

Find (exact current lines, end of the `.card-cta-secondary:hover` rule added in Task 2, right before the `/* About photo */` comment):
```html
    .card-cta-secondary:hover { color: var(--ink); }

    /* About photo */
    .about-photo {
```

Replace with:
```html
    .card-cta-secondary:hover { color: var(--ink); }

    /* ============================================================
       TESTIMONIALS
    ============================================================ */
    .testimonial-stars {
      display: flex;
      gap: 3px;
      margin-bottom: 14px;
    }

    .testimonial-stars svg {
      width: 16px;
      height: 16px;
      fill: var(--amber-text);
    }

    .testimonial-quote {
      font-size: 0.98rem;
      color: var(--ink-2);
      line-height: 1.75;
      margin-bottom: 18px;
    }

    .testimonial-author {
      display: flex;
      align-items: center;
      gap: 8px;
      font-size: 0.85rem;
      color: var(--muted);
    }

    .testimonial-author strong {
      color: var(--ink);
      font-weight: 600;
    }

    .testimonial-source {
      display: inline-flex;
      align-items: center;
      font-size: 0.72rem;
      font-weight: 700;
      letter-spacing: 0.04em;
      text-transform: uppercase;
      color: var(--accent);
      background: var(--accent-light);
      padding: 3px 8px;
      border-radius: 999px;
    }

    .testimonials-footer {
      margin-top: 32px;
      text-align: center;
    }

    /* About photo */
    .about-photo {
```

- [ ] **Step 2: Insert the Testimonials section**

Find (exact current text — the Services section's closing tag followed by the Selected Work comment block):
```html
        </div>
      </div>
    </section>

    <!-- =============================================
         SELECTED WORK
    ============================================= -->
```

Replace with:
```html
        </div>
      </div>
    </section>

    <!-- =============================================
         TESTIMONIALS
    ============================================= -->
    <section class="section" id="testimonials" aria-labelledby="testimonials-heading">
      <div class="container">
        <span class="section-label">รีวิว</span>
        <h2 class="section-title" id="testimonials-heading">ลูกค้าพูดถึงเราอย่างไร</h2>

        <div class="works-grid">

          <div class="card reveal">
            <div class="testimonial-stars" aria-hidden="true">
              <svg viewBox="0 0 24 24"><path d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279L12 19.771l-7.416 3.642 1.48-8.279L0 9.306l8.332-1.151z"/></svg>
              <svg viewBox="0 0 24 24"><path d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279L12 19.771l-7.416 3.642 1.48-8.279L0 9.306l8.332-1.151z"/></svg>
              <svg viewBox="0 0 24 24"><path d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279L12 19.771l-7.416 3.642 1.48-8.279L0 9.306l8.332-1.151z"/></svg>
              <svg viewBox="0 0 24 24"><path d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279L12 19.771l-7.416 3.642 1.48-8.279L0 9.306l8.332-1.151z"/></svg>
              <svg viewBox="0 0 24 24"><path d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279L12 19.771l-7.416 3.642 1.48-8.279L0 9.306l8.332-1.151z"/></svg>
            </div>
            <p class="sr-only">ให้คะแนน 5 จาก 5 ดาว</p>
            <p class="testimonial-quote">"ผลงานดีมากค่ะ"</p>
            <div class="testimonial-author">
              <strong>ppxyb58z</strong>
              <span class="testimonial-source">Fastwork</span>
            </div>
          </div>

          <div class="card reveal">
            <div class="testimonial-stars" aria-hidden="true">
              <svg viewBox="0 0 24 24"><path d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279L12 19.771l-7.416 3.642 1.48-8.279L0 9.306l8.332-1.151z"/></svg>
              <svg viewBox="0 0 24 24"><path d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279L12 19.771l-7.416 3.642 1.48-8.279L0 9.306l8.332-1.151z"/></svg>
              <svg viewBox="0 0 24 24"><path d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279L12 19.771l-7.416 3.642 1.48-8.279L0 9.306l8.332-1.151z"/></svg>
              <svg viewBox="0 0 24 24"><path d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279L12 19.771l-7.416 3.642 1.48-8.279L0 9.306l8.332-1.151z"/></svg>
              <svg viewBox="0 0 24 24"><path d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279L12 19.771l-7.416 3.642 1.48-8.279L0 9.306l8.332-1.151z"/></svg>
            </div>
            <p class="sr-only">ให้คะแนน 5 จาก 5 ดาว</p>
            <p class="testimonial-quote">"เริ่ดมากแปปเดียวเสร็จ งานตามบรีฟ"</p>
            <div class="testimonial-author">
              <strong>Pornsawan PT.</strong>
              <span class="testimonial-source">Fastwork</span>
            </div>
          </div>

          <div class="card reveal">
            <div class="testimonial-stars" aria-hidden="true">
              <svg viewBox="0 0 24 24"><path d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279L12 19.771l-7.416 3.642 1.48-8.279L0 9.306l8.332-1.151z"/></svg>
              <svg viewBox="0 0 24 24"><path d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279L12 19.771l-7.416 3.642 1.48-8.279L0 9.306l8.332-1.151z"/></svg>
              <svg viewBox="0 0 24 24"><path d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279L12 19.771l-7.416 3.642 1.48-8.279L0 9.306l8.332-1.151z"/></svg>
              <svg viewBox="0 0 24 24"><path d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279L12 19.771l-7.416 3.642 1.48-8.279L0 9.306l8.332-1.151z"/></svg>
              <svg viewBox="0 0 24 24"><path d="M12 .587l3.668 7.568 8.332 1.151-6.064 5.828 1.48 8.279L12 19.771l-7.416 3.642 1.48-8.279L0 9.306l8.332-1.151z"/></svg>
            </div>
            <p class="sr-only">ให้คะแนน 5 จาก 5 ดาว</p>
            <p class="testimonial-quote">"มีความตั้งใจ งานไว แนะนำเลยค้า"</p>
            <div class="testimonial-author">
              <strong>namfon.upwt</strong>
              <span class="testimonial-source">Fastwork</span>
            </div>
          </div>

        </div>

        <div class="testimonials-footer">
          <a class="card-link" href="https://fastwork.co/user/u106pl4r" target="_blank" rel="noopener noreferrer">ดูรีวิวทั้งหมดบน Fastwork →</a>
        </div>
      </div>
    </section>

    <!-- =============================================
         SELECTED WORK
    ============================================= -->
```

- [ ] **Step 3: Verify in browser**

Reload `http://localhost:8000/index.html`. Confirm:
- New "รีวิว" section appears between Services and Selected Work, with three cards each showing 5 filled amber stars, a Thai quote, and a username with a small "FASTWORK" pill badge.
- "ดูรีวิวทั้งหมดบน Fastwork →" opens `https://fastwork.co/user/u106pl4r` in a new tab.
- Cards fade/stagger in on scroll (the existing `.reveal` behavior) — confirms no JS changes were needed.
- 375px width: three testimonial cards stack to one column, no horizontal scroll.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "$(cat <<'EOF'
Add real Fastwork testimonials section

Three real 5-star reviews from Phakin's Fastwork buyer history, with
a link back to the Fastwork profile so they're independently
verifiable. Deliberately skips schema.org Review/AggregateRating
markup since the reviews live on a third-party platform, not this
site.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 4: Nav links (desktop, mobile, footer)

**Files:**
- Modify: `index.html:1167-1174` (desktop `.nav-links`)
- Modify: `index.html:1185-1193` (mobile `.nav-mobile-panel`)
- Modify: `index.html` footer `.footer-nav` (search for `<ul class="footer-nav">` — content given below)

**Interfaces:** Consumes `#testimonials` (produced by Task 3). No new interfaces produced.

- [ ] **Step 1: Add "Reviews" to the desktop nav**

Find (exact current lines 1167-1174):
```html
        <ul class="nav-links">
          <li><a href="#services">Services</a></li>
          <li><a href="#projects">Projects</a></li>
          <li><a href="#about">About</a></li>
          <li><a href="#experience">Experience</a></li>
          <li><a href="#case-studies">Case Studies</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>
```

Replace with:
```html
        <ul class="nav-links">
          <li><a href="#services">Services</a></li>
          <li><a href="#testimonials">Reviews</a></li>
          <li><a href="#projects">Projects</a></li>
          <li><a href="#about">About</a></li>
          <li><a href="#experience">Experience</a></li>
          <li><a href="#case-studies">Case Studies</a></li>
          <li><a href="#contact">Contact</a></li>
        </ul>
```

- [ ] **Step 2: Add "Reviews" to the mobile nav panel**

Find (exact current lines 1185-1193):
```html
    <nav class="nav-mobile-panel" id="mobile-panel" aria-label="Mobile navigation">
      <a href="#services">Services</a>
      <a href="#projects">Projects</a>
      <a href="#about">About</a>
      <a href="#experience">Experience</a>
      <a href="#case-studies">Case Studies</a>
      <a href="#contact">Contact</a>
      <a class="resume-mobile" href="resume.html">Resume</a>
    </nav>
```

Replace with:
```html
    <nav class="nav-mobile-panel" id="mobile-panel" aria-label="Mobile navigation">
      <a href="#services">Services</a>
      <a href="#testimonials">Reviews</a>
      <a href="#projects">Projects</a>
      <a href="#about">About</a>
      <a href="#experience">Experience</a>
      <a href="#case-studies">Case Studies</a>
      <a href="#contact">Contact</a>
      <a class="resume-mobile" href="resume.html">Resume</a>
    </nav>
```

- [ ] **Step 3: Add "Reviews" to the footer nav**

Find (exact current footer nav list):
```html
          <ul class="footer-nav">
            <li><a href="https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob" target="_blank" rel="noopener noreferrer">Hire on Fastwork</a></li>
            <li><a href="#services">Services</a></li>
            <li><a href="#projects">Projects</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#experience">Experience</a></li>
            <li><a href="#case-studies">Case Studies</a></li>
            <li><a href="resume.html">Resume</a></li>
            <li><a href="mailto:a0626568471@gmail.com">Email</a></li>
          </ul>
```

Replace with:
```html
          <ul class="footer-nav">
            <li><a href="https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob" target="_blank" rel="noopener noreferrer">Hire on Fastwork</a></li>
            <li><a href="#services">Services</a></li>
            <li><a href="#testimonials">Reviews</a></li>
            <li><a href="#projects">Projects</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#experience">Experience</a></li>
            <li><a href="#case-studies">Case Studies</a></li>
            <li><a href="resume.html">Resume</a></li>
            <li><a href="mailto:a0626568471@gmail.com">Email</a></li>
          </ul>
```

- [ ] **Step 4: Verify in browser**

Reload `http://localhost:8000/index.html`. Confirm:
- Desktop nav shows "Reviews" between "Services" and "Projects," and clicking it scrolls to the Testimonials section.
- Resize to 375px, open the mobile hamburger menu — "Reviews" appears in the same position, works the same way.
- Footer "Navigation" column shows "Reviews" in the same position and works.

- [ ] **Step 5: Commit**

```bash
git add index.html
git commit -m "$(cat <<'EOF'
Link the new Reviews section from nav and footer

Adds #testimonials to the desktop nav, mobile drawer, and footer nav,
positioned right after Services to match its position on the page.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 5: Update CLAUDE.md documentation

**Files:**
- Modify: `CLAUDE.md:96` (Nav row)
- Modify: `CLAUDE.md:99` (Services row)
- Modify: `CLAUDE.md` (insert new Testimonials row after Services)

**Interfaces:** None — documentation only.

- [ ] **Step 1: Update the Pages & Sections table**

Find (exact current lines 94-105):
```markdown
| Section | id | Description |
|---------|----|-------------|
| Nav | — | Logo + links: Services, Projects, About, Experience, Case Studies, Contact, Resume |
| Hero | `#top` | Name, service positioning, primary CTA → Fastwork (external) |
| Tech Stack | — | Dual-row logo marquee (Simple Icons inlined as SVG symbols), opposite scroll directions, pause on hover, reduced-motion static |
| Services | `#services` | 3 service cards (Landing Page / Dashboard UI / Business Website), each links to Fastwork |
| Selected Work | `#projects` | 13 project cards |
| About | `#about` | Bio + photo |
| Experience | `#experience` | Skills, timeline, tools, KMUTT education |
| Case Studies | `#case-studies` | PulseBoard, LaunchLedger, InternTrack, HabitQuest |
| Contact | `#contact` | Form + email |
| Footer | — | Nav links, email, social icons |
```

Replace with:
```markdown
| Section | id | Description |
|---------|----|-------------|
| Nav | — | Logo + links: Services, Reviews, Projects, About, Experience, Case Studies, Contact, Resume |
| Hero | `#top` | Name, full-time service positioning, primary CTA → Fastwork (external), secondary CTA → Services/pricing |
| Tech Stack | — | Dual-row logo marquee (Simple Icons inlined as SVG symbols), opposite scroll directions, pause on hover, reduced-motion static |
| Services | `#services` | 3 priced packages (Landing Page ฿3,900 / Dashboard UI ฿7,900 / Business Website ฿9,900), Thai copy, each links to Fastwork + `#contact` |
| Testimonials | `#testimonials` | 3 real 5-star Fastwork buyer reviews, Thai, links back to the Fastwork profile — no schema.org Review markup (see `docs/superpowers/specs/2026-08-05-service-pivot-design.md`) |
| Selected Work | `#projects` | 13 project cards |
| About | `#about` | Bio + photo |
| Experience | `#experience` | Skills, timeline, tools, KMUTT education |
| Case Studies | `#case-studies` | PulseBoard, LaunchLedger, InternTrack, HabitQuest |
| Contact | `#contact` | Form + email |
| Footer | — | Nav links, email, social icons |
```

- [ ] **Step 2: Commit**

```bash
git add CLAUDE.md
git commit -m "$(cat <<'EOF'
Document the Testimonials section and priced Services in CLAUDE.md

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 6: About section — fix the "HTML and CSS only" undersell

**Files:**
- Modify: `index.html:2252-2256` (About paragraph 1 — see exact text below; line numbers shift slightly after Tasks 1-4's insertions, so use the "Find" text as the authoritative anchor, not the line numbers)

**Interfaces:** None — pure text content, no new classes or IDs. Independent of Tasks 1-5; can be done in any order relative to them, but is sequenced last among content edits so it can be verified alongside everything else in Task 7.

**Why:** The hero's tech-stack marquee shows React, Node.js, Express, and PostgreSQL, and the Selected Work filter bar has a "Full Stack" tag with 5 projects — but `#about` says "I work in HTML and CSS," directly contradicting both. A visitor who reads About before scrolling further reasonably concludes the offering is static pages only, undermining the Dashboard UI and full-stack-leaning parts of the new pricing section (Task 2).

- [ ] **Step 1: Reword the About paragraph**

Find (exact current text inside `#about`'s first `<p class="card-text">`):
```html
            <p class="card-text">
              I'm Phakin Chawanpunya — a frontend developer who helps startups and small teams
              get online with clean, fast, and professional-looking pages. I work in HTML and CSS,
              turning ideas and designs into responsive, accessible pages that represent your brand well.
            </p>
```

Replace with:
```html
            <p class="card-text">
              I'm Phakin Chawanpunya — a frontend developer with React and Node.js backend
              experience, helping startups and small teams get online with clean, fast,
              professional-looking sites — from static landing pages to full-stack apps with a
              working backend when the project calls for it.
            </p>
```

The second `<p class="card-text">` right after it ("I work best with founders...") is unchanged — leave it exactly as is.

- [ ] **Step 2: Verify in browser**

Reload the local preview, scroll to `#about`. Confirm the paragraph reads the new copy and no longer contains the phrase "I work in HTML and CSS." Confirm it doesn't overflow the `.card` at 375px width (it's plain text in an existing card, so this is a quick visual check, not expected to regress).

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "$(cat <<'EOF'
Fix About section undercutting the full-stack pricing tiers

"I work in HTML and CSS" contradicted the hero's React/Node.js/
Express/PostgreSQL stack chips and the Selected Work "Full Stack"
filter (5 projects) — a visitor reading About alone would reasonably
conclude the offering is static pages only, which undersells the
Dashboard UI package.

Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>
EOF
)"
```

---

### Task 7: Full-page verification

**Files:** None modified — this task only runs checks. If it finds a regression, fix it in `index.html` and commit the fix before considering this task done.

**Interfaces:** None.

- [ ] **Step 1: Mobile overflow check**

With the local server running and `index.html` open at 375×812, run (per `CLAUDE.md`'s documented snippet, via whatever browser-automation tool is available at execution time — chrome-devtools MCP or claude-in-chrome):

```js
({canScrollX: (function(){document.documentElement.scrollLeft=50;const s=document.documentElement.scrollLeft;document.documentElement.scrollLeft=0;return s>0;})(), bw:document.body.scrollWidth, cw:document.documentElement.clientWidth})
```

Expected: `canScrollX: false` and `bw === cw`. If not, find which new element (pricing card, testimonial card, star row) is overflowing and fix it — the most likely culprit is a fixed-width element inside `.card-list li` or `.testimonial-stars`; both are written in this plan using flexible units already, so no overflow is expected, but this step is the check that confirms it.

- [ ] **Step 2: Lighthouse audit**

Run `lighthouse_audit(device="mobile", mode="navigation")` on the local URL, per `CLAUDE.md`'s "Run a Lighthouse audit" instructions. Confirm Accessibility, Best Practices, and SEO all still score 100. If Accessibility drops, check first whether it's the new `aria-hidden="true"` + `.sr-only` pairing on `.testimonial-stars` (Task 3, Step 2) — every star row must have its `.sr-only` sibling text.

- [ ] **Step 3: Full click-through**

In the browser, click every link touched by this plan in order: hero "Hire Me on Fastwork," hero "See Pricing," each Services card's two buttons, the Testimonials "ดูรีวิวทั้งหมดบน Fastwork →" link, nav "Reviews" (desktop and mobile), footer "Reviews." Confirm each lands where expected (Fastwork profile/listing in a new tab, or the correct in-page anchor). Also scroll to `#about` and confirm the reworded paragraph (Task 6) reads correctly and no longer says "I work in HTML and CSS."

- [ ] **Step 4: If all checks pass, no commit needed for this task** (it's verification-only). If any check failed and required a fix, stage and commit that fix with a message describing what regressed and why, following the same `Co-Authored-By` convention as the other tasks in this plan.

- [ ] **Step 5: Flag the new Thai copy for Phakin's own read-through**

The agent executing this plan should not treat Thai copy correctness as self-verified — per the spec's Verification section, tone/correctness of the new Thai text (Services pricing cards, Testimonials, meta description) needs a native-speaker pass by Phakin before this is considered fully done. End this task by listing the exact strings added in Tasks 1–3 (meta description, hero, 3 pricing cards, 3 testimonial quotes) and the reworded English About paragraph (Task 6) back to Phakin for a quick read, rather than silently marking the plan complete.
