# Service Category Landing Pages Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Give each of the site's three real, already-live service packages (Landing Page ฿3,900, Dashboard UI ฿7,900, Business Website ฿9,900) its own dedicated, SEO-indexable landing page — inspired by bigzweb.com's per-category pages, but grounded entirely in this site's real pricing copy and real project work rather than an AI-generated recommendation.

**Architecture:** Six new static pages (3 categories × TH/EN), built entirely from components that already exist and are already proven across the site's 17 showcase/case-study pages: `assets/portfolio-pages.css`'s `.hero.case-hero`, `.study-meta`, `.study-block`, `.highlight-list`, `.project-strip`/`.project-link`, `.result-band`, and `.footer-band`. **No new CSS file and no new CSS rules are needed anywhere in this plan** — every visual piece is reused as-is.

**Tech Stack:** Static HTML, `assets/portfolio-pages.css` (shared, unchanged), `assets/analytics.js` (shared, unchanged). No JS beyond what those shared files already provide.

## Global Constraints

- Every page pair follows the exact bilingual invariant documented in `CLAUDE.md`'s "Add a case study" recipe: reciprocal `hreflang` (`th`/`en`/`x-default` → Thai), self-referential `canonical`, `og:locale` per language, `<html lang="th">`/`<html lang="en">`, `<script src="assets/analytics.js" defer></script>` before `</head>`, and a `sitemap.xml` entry for both files.
- Thai is the site default — `x-default` always points at the `.html` (Thai) URL, never the `-en.html` one.
- All prices, durations, and included-feature lists **must be copied verbatim** from the live Services section (`index.html:1567-1618`) — this plan does not invent new pricing or service terms. Where TH and EN Services sections both keep pricing copy in Thai (confirmed: `index-en.html`'s `#services` section is `lang="th"` and untranslated — a deliberate earlier decision), these new pages follow the same convention: pricing/feature-list content stays in Thai even on the `-en` page; only the surrounding hero/chrome copy is in English.
- Every internal link on a Thai page points to another Thai page; every link on an `-en` page points to another `-en` page. The only cross-language link is the `TH`/`EN` nav switcher — same rule as the rest of the site.
- Reuse `assets/portfolio-pages.css` classes exactly as named (`.hero.case-hero`, `.study-meta`, `.study-block`, `.highlight-list`, `.project-strip`, `.project-link`, `.result-band`, `.footer-band`, `.tag`/`.tag-*`, `.button.primary`) — do not redefine or fork them.
- Fastwork URL (use verbatim, matches every other CTA on the site): `https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&source=byob`

---

### Task 1: Landing Page category page

**Files:**
- Create: `landing-page.html` (Thai)
- Create: `landing-page-en.html` (English)

**Interfaces:**
- Consumes: `assets/portfolio-pages.css`, `assets/analytics.js`, `assets/favicon.svg`, `site.webmanifest` (all existing, unmodified).
- Produces: two new URLs (`https://ph-akin.dev/landing-page.html`, `https://ph-akin.dev/landing-page-en.html`) that Task 4 wires into `sitemap.xml` and links from `index.html`/`index-en.html`.

Real content used: price ฿3,900, duration 5-7 days, and the 4 included-feature bullets, all copied verbatim from `index.html:1571-1579` (`Landing Page / Sale Page` card). Related projects: the 9 projects already tagged `data-tags="landing"` in `index.html`'s Selected Work grid — BuildNest Construction, Iron Republic, NOIR Coffee, RATRI Restaurant, SolarPeak, MuseRoom, LUMI Clinic, BRIGHT Dental Clinic, VELVÉ Aesthetics — using each project's real one-line description already printed on its card.

- [ ] **Step 1: Create `landing-page.html`**

```html
<!DOCTYPE html>
<html lang="th">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="รับทำ Landing Page และ Sale Page เริ่มต้น 3,900 บาท ส่งงานใน 5-7 วัน พัฒนาใหม่ทั้งหมด ไม่ใช้เทมเพลตสำเร็จรูป ดูตัวอย่างผลงานจริง 9 ชิ้น" />
  <meta name="theme-color" content="#5274f8" />
  <link rel="canonical" href="https://ph-akin.dev/landing-page.html" />
  <link rel="alternate" hreflang="th" href="https://ph-akin.dev/landing-page.html" />
  <link rel="alternate" hreflang="en" href="https://ph-akin.dev/landing-page-en.html" />
  <link rel="alternate" hreflang="x-default" href="https://ph-akin.dev/landing-page.html" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="รับทำ Landing Page เริ่มต้น ฿3,900 | Phakin Chawanpunya" />
  <meta property="og:description" content="รับทำ Landing Page และ Sale Page เริ่มต้น 3,900 บาท ส่งงานใน 5-7 วัน พัฒนาใหม่ทั้งหมด ไม่ใช้เทมเพลตสำเร็จรูป ดูตัวอย่างผลงานจริง 9 ชิ้น" />
  <meta property="og:url" content="https://ph-akin.dev/landing-page.html" />
  <meta property="og:image" content="https://ph-akin.dev/assets/social-preview.png?v=ph-akin-dev" />
  <meta property="og:image:alt" content="Phakin Chawanpunya portfolio preview." />
  <meta property="og:locale" content="th_TH" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="รับทำ Landing Page เริ่มต้น ฿3,900 | Phakin Chawanpunya" />
  <meta name="twitter:description" content="รับทำ Landing Page และ Sale Page เริ่มต้น 3,900 บาท ส่งงานใน 5-7 วัน พัฒนาใหม่ทั้งหมด ไม่ใช้เทมเพลตสำเร็จรูป ดูตัวอย่างผลงานจริง 9 ชิ้น" />
  <meta name="twitter:image" content="https://ph-akin.dev/assets/social-preview.png?v=ph-akin-dev" />
  <title>รับทำ Landing Page เริ่มต้น ฿3,900 | Phakin Chawanpunya</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=optional" rel="stylesheet">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml" />
  <link rel="manifest" href="site.webmanifest" />
  <link rel="stylesheet" href="assets/portfolio-pages.css?v=ghdark-2" />
  <script src="assets/analytics.js" defer></script>
</head>
<body>
  <header class="topbar">
    <nav class="page-shell nav" aria-label="เมนู Landing Page">
      <a class="brand" href="/" aria-label="รับทำ Landing Page — กลับไปหน้าพอร์ตโฟลิโอ">
        <span class="brand-mark" aria-hidden="true">
          <svg viewBox="0 0 34 34" focusable="false">
            <rect class="mark-back" x="8" y="7" width="16" height="13" rx="3" />
            <rect class="mark-front" x="12" y="12" width="16" height="15" rx="3" />
            <path class="mark-line" d="M16 18h7M16 23h4" />
            <circle class="mark-dot" cx="24" cy="17" r="2.1" />
          </svg>
        </span>
        <span>รับทำ Landing Page</span>
      </a>
      <ul class="nav-links">
        <li><a href="/#projects">ผลงานทั้งหมด</a></li>
        <li><a href="/#services">บริการอื่นๆ</a></li>
        <li><a class="nav-primary" href="https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob" target="_blank" rel="noopener noreferrer">เริ่มงานบน Fastwork</a></li>
        <li><a href="landing-page-en.html">EN</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <section class="hero case-hero">
      <div class="page-shell">
        <span class="eyebrow">บริการ</span>
        <h1>รับทำ Landing Page เริ่มต้น ฿3,900</h1>
        <p class="hero-copy">หน้าเดียวจบ พัฒนาใหม่ทั้งหมด ไม่ใช้เทมเพลตสำเร็จรูป ส่งงานภายใน 5-7 วัน เหมาะกับธุรกิจที่ต้องการโปรโมทสินค้าหรือบริการให้ชัดเจนในหน้าเดียว</p>
        <div class="hero-actions">
          <a class="button primary" href="https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob" target="_blank" rel="noopener noreferrer">เริ่มงานบน Fastwork</a>
        </div>
      </div>

      <div class="page-shell" style="margin-top:32px;">
        <div class="study-meta" aria-label="ข้อมูลบริการ Landing Page">
          <div>
            <strong>ราคาเริ่มต้น</strong>
            <span>฿3,900</span>
          </div>
          <div>
            <strong>ระยะเวลา</strong>
            <span>5-7 วัน</span>
          </div>
          <div>
            <strong>แก้ไขได้</strong>
            <span>2 รอบ + ฟรีแก้บั๊ก 3 เดือน</span>
          </div>
          <div>
            <strong>เหมาะกับ</strong>
            <span>ธุรกิจที่ต้องการหน้าเดียวจบ</span>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="overview">
      <div class="page-shell study-grid">
        <article class="study-block featured">
          <span class="showcase-icon" aria-hidden="true">&#10024;</span>
          <span class="eyebrow">รวมอยู่ในแพ็กเกจ</span>
          <h2>สิ่งที่คุณได้รับ</h2>
          <ul class="highlight-list">
            <li>พัฒนาใหม่ทั้งหมด ไม่ใช้เทมเพลตสำเร็จรูป</li>
            <li>1 หน้า ไม่เกิน 6 section ลงข้อมูลและรูปภาพให้ครบ</li>
            <li>รองรับการแสดงผลบนมือถือและคอมพิวเตอร์ทุกหน้าจอ</li>
            <li>แก้ไขงานได้ 2 รอบ ฟรีบริการแก้ไขปัญหา 3 เดือน</li>
          </ul>
        </article>

        <article class="study-block">
          <span class="showcase-icon" aria-hidden="true">&#127919;</span>
          <span class="eyebrow">เหมาะกับใคร</span>
          <h2>เหมาะกับธุรกิจที่ต้องการหน้าเดียวจบ</h2>
          <p>ร้านค้า ธุรกิจบริการ หรือแคมเปญที่ต้องการหน้าเว็บเดียวที่โฟกัสการโปรโมทสินค้าหรือบริการอย่างชัดเจน ไม่ต้องมีหลายหน้าให้ผู้เข้าชมหลงทาง</p>
        </article>
      </div>
    </section>

    <section class="section" id="cta">
      <div class="page-shell">
        <div class="result-band">
          <div>
            <span class="eyebrow">พร้อมเริ่มหรือยัง?</span>
            <h2>อยากได้ Landing Page แบบนี้บ้าง?</h2>
            <p>บอกความต้องการหรืองบประมาณได้เลย ผมช่วยออกแบบและพัฒนาให้เหมาะกับธุรกิจคุณ</p>
          </div>
          <div class="result-actions">
            <a class="button primary" href="https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob" target="_blank" rel="noopener noreferrer">เริ่มงานบน Fastwork</a>
            <a class="button" href="mailto:a0626568471@gmail.com">อีเมลหาเรา</a>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="related">
      <div class="page-shell">
        <div class="section-heading">
          <div>
            <span class="eyebrow">ผลงานจริง</span>
            <h2>ตัวอย่าง Landing Page ที่เคยทำ</h2>
          </div>
        </div>
        <div class="project-strip">
          <a class="project-link" href="showcase-buildnest.html">
            <strong>BuildNest Construction</strong>
            <span>แลนดิ้งเพจบริษัทก่อสร้าง ออกแบบเป็นภาษาไทยตั้งแต่ต้น โครงสร้างบริการครบวงจร พร้อมภาพประกอบ SVG งานสถาปัตย์และผลงานที่ผ่านมา</span>
          </a>
          <a class="project-link" href="showcase-iron-republic.html">
            <strong>Iron Republic</strong>
            <span>แบรนด์ยิมที่ต้องการหน้าเว็บกระตุ้นให้คนสมัครสมาชิก พร้อมสื่อถึงพลังและความเข้มข้น</span>
          </a>
          <a class="project-link" href="showcase-noir-coffee.html">
            <strong>NOIR Coffee</strong>
            <span>ร้านกาแฟพิเศษที่ต้องการแลนดิ้งเพจหรูหรา ดึงดูดลูกค้าเดินเข้าร้านและสร้างความผูกพันกับแบรนด์</span>
          </a>
          <a class="project-link" href="showcase-ratri-restaurant.html">
            <strong>RATRI Restaurant</strong>
            <span>แลนดิ้งเพจโทนมืดสไตล์หรู สำหรับร้านอาหารไทยไฟน์ไดนิ่งสมัยใหม่ พร้อมระบบจองโต๊ะที่ใช้งานได้จริง</span>
          </a>
          <a class="project-link" href="showcase-solarpeak.html">
            <strong>SolarPeak</strong>
            <span>แลนดิ้งเพจบริษัทโซลาร์เซลล์ ดีไซน์แบบเอกสารสเปกวิศวกรรม พร้อมภาพถ่ายหน้างานจริงและตารางเปรียบเทียบ</span>
          </a>
          <a class="project-link" href="showcase-museroom.html">
            <strong>MuseRoom</strong>
            <span>แลนดิ้งเพจแกลเลอรีโทนมืด เน้นบรรยากาศดื่มด่ำ การ์ดจัดแสดงผลงาน และประสบการณ์เยี่ยมชมที่ผ่อนคลาย</span>
          </a>
          <a class="project-link" href="showcase-lumi-clinic.html">
            <strong>LUMI Clinic</strong>
            <span>หน้าเว็บคลินิกความงามสไตล์เอดิทอเรียล โทนสีขาวหมึกดำ ภาพถ่ายจริง และตารางราคาชัดเจน</span>
          </a>
          <a class="project-link" href="showcase-dental-clinic.html">
            <strong>BRIGHT Dental Clinic</strong>
            <span>แลนดิ้งเพจคลินิกทันตกรรม โทนเขียวมิ้นท์สะอาดตา พร้อมตารางราคาโปร่งใสและฟอร์มจองคิวออนไลน์</span>
          </a>
          <a class="project-link" href="showcase-velve-aesthetics.html">
            <strong>VELVÉ Aesthetics</strong>
            <span>คลินิกเสริมความงามพร้อมระบบจองคิว 4 ขั้นตอนที่ใช้งานได้จริง — เลือกบริการ แพทย์ ช่วงเวลา แล้วยืนยัน</span>
          </a>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer-band">
    <div class="page-shell footer-inner">
      <span>Landing Page service — Phakin Chawanpunya</span>
      <span>Phakin Chawanpunya</span>
    </div>
  </footer>
</body>
</html>
```

- [ ] **Step 2: Run this checklist against the file you just wrote**

- `<html lang="th">` — yes.
- `canonical` points at `landing-page.html` (itself, not `-en`) — yes.
- All three `hreflang` alternates present, `x-default` → Thai — yes.
- `<script src="assets/analytics.js" defer></script>` present before `</head>` — yes.
- Every `href` inside `<body>` points at a Thai URL or an external link (Fastwork, `mailto:`) — the only exception is the `EN` switcher link (`landing-page-en.html`), which does not exist yet (created in Step 3) — that's expected, it will resolve once Step 3 lands.

- [ ] **Step 3: Create `landing-page-en.html`**

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <meta name="description" content="Custom landing & sale pages from ฿3,900, delivered in 5-7 days. Built from scratch, no templates. See 9 real client projects." />
  <meta name="theme-color" content="#5274f8" />
  <link rel="canonical" href="https://ph-akin.dev/landing-page-en.html" />
  <link rel="alternate" hreflang="th" href="https://ph-akin.dev/landing-page.html" />
  <link rel="alternate" hreflang="en" href="https://ph-akin.dev/landing-page-en.html" />
  <link rel="alternate" hreflang="x-default" href="https://ph-akin.dev/landing-page.html" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="Landing Page Development from ฿3,900 | Phakin Chawanpunya" />
  <meta property="og:description" content="Custom landing & sale pages from ฿3,900, delivered in 5-7 days. Built from scratch, no templates. See 9 real client projects." />
  <meta property="og:url" content="https://ph-akin.dev/landing-page-en.html" />
  <meta property="og:image" content="https://ph-akin.dev/assets/social-preview.png?v=ph-akin-dev" />
  <meta property="og:image:alt" content="Phakin Chawanpunya portfolio preview." />
  <meta property="og:locale" content="en_US" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="Landing Page Development from ฿3,900 | Phakin Chawanpunya" />
  <meta name="twitter:description" content="Custom landing & sale pages from ฿3,900, delivered in 5-7 days. Built from scratch, no templates. See 9 real client projects." />
  <meta name="twitter:image" content="https://ph-akin.dev/assets/social-preview.png?v=ph-akin-dev" />
  <title>Landing Page Development from ฿3,900 | Phakin Chawanpunya</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=optional" rel="stylesheet">
  <link rel="icon" href="assets/favicon.svg" type="image/svg+xml" />
  <link rel="manifest" href="site.webmanifest" />
  <link rel="stylesheet" href="assets/portfolio-pages.css?v=ghdark-2" />
  <script src="assets/analytics.js" defer></script>
</head>
<body>
  <header class="topbar">
    <nav class="page-shell nav" aria-label="Landing Page menu">
      <a class="brand" href="index-en.html" aria-label="Landing Page service — back to portfolio">
        <span class="brand-mark" aria-hidden="true">
          <svg viewBox="0 0 34 34" focusable="false">
            <rect class="mark-back" x="8" y="7" width="16" height="13" rx="3" />
            <rect class="mark-front" x="12" y="12" width="16" height="15" rx="3" />
            <path class="mark-line" d="M16 18h7M16 23h4" />
            <circle class="mark-dot" cx="24" cy="17" r="2.1" />
          </svg>
        </span>
        <span>Landing Page Service</span>
      </a>
      <ul class="nav-links">
        <li><a href="index-en.html#projects">All Work</a></li>
        <li><a href="index-en.html#services">Other Services</a></li>
        <li><a class="nav-primary" href="https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob" target="_blank" rel="noopener noreferrer">Start on Fastwork</a></li>
        <li><a href="landing-page.html">TH</a></li>
      </ul>
    </nav>
  </header>

  <main>
    <section class="hero case-hero">
      <div class="page-shell">
        <span class="eyebrow">Service</span>
        <h1>Landing Page Development, from ฿3,900</h1>
        <p class="hero-copy">One focused page, built from scratch — no templates. Delivered in 5-7 days. A clean fit for businesses that need one page to sell one thing clearly.</p>
        <div class="hero-actions">
          <a class="button primary" href="https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob" target="_blank" rel="noopener noreferrer">Start on Fastwork</a>
        </div>
      </div>

      <div class="page-shell" style="margin-top:32px;">
        <div class="study-meta" aria-label="Landing Page service details">
          <div>
            <strong>Starting price</strong>
            <span>฿3,900</span>
          </div>
          <div>
            <strong>Timeline</strong>
            <span>5-7 days</span>
          </div>
          <div>
            <strong>Revisions</strong>
            <span>2 rounds + 3 months free bug-fixing</span>
          </div>
          <div>
            <strong>Best for</strong>
            <span>Businesses needing one focused page</span>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="overview">
      <div class="page-shell study-grid">
        <article class="study-block featured">
          <span class="showcase-icon" aria-hidden="true">&#10024;</span>
          <span class="eyebrow">What's included</span>
          <h2>What you get</h2>
          <ul class="highlight-list">
            <li>Built entirely from scratch — no pre-made templates</li>
            <li>1 page, up to 6 sections, all content and images placed</li>
            <li>Fully responsive across mobile and desktop</li>
            <li>2 revision rounds, plus 3 months of free bug-fixing</li>
          </ul>
        </article>

        <article class="study-block">
          <span class="showcase-icon" aria-hidden="true">&#127919;</span>
          <span class="eyebrow">Who it's for</span>
          <h2>A fit for businesses that need one page to do the job</h2>
          <p>Shops, service businesses, or campaigns that need a single page focused on promoting one product or service clearly — no multi-page navigation to get lost in.</p>
        </article>
      </div>
    </section>

    <section class="section" id="cta">
      <div class="page-shell">
        <div class="result-band">
          <div>
            <span class="eyebrow">Ready to start?</span>
            <h2>Want a landing page like these?</h2>
            <p>Tell me what you need or your budget — I'll help design and build something that fits your business.</p>
          </div>
          <div class="result-actions">
            <a class="button primary" href="https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob" target="_blank" rel="noopener noreferrer">Start on Fastwork</a>
            <a class="button" href="mailto:a0626568471@gmail.com">Email me</a>
          </div>
        </div>
      </div>
    </section>

    <section class="section" id="related">
      <div class="page-shell">
        <div class="section-heading">
          <div>
            <span class="eyebrow">Real work</span>
            <h2>Landing pages I've built</h2>
          </div>
        </div>
        <div class="project-strip">
          <a class="project-link" href="showcase-buildnest-en.html">
            <strong>BuildNest Construction</strong>
            <span>Thai-first construction landing page inspired by one-stop service structure, with custom SVG architecture and project proof sections.</span>
          </a>
          <a class="project-link" href="showcase-iron-republic-en.html">
            <strong>Iron Republic</strong>
            <span>Gym brand needed a homepage that drives sign-ups and communicates energy.</span>
          </a>
          <a class="project-link" href="showcase-noir-coffee-en.html">
            <strong>NOIR Coffee</strong>
            <span>Specialty café wanted a premium landing page to attract walk-ins and build brand loyalty.</span>
          </a>
          <a class="project-link" href="showcase-ratri-restaurant-en.html">
            <strong>RATRI Restaurant</strong>
            <span>Elegant dark landing page for a modern Thai fine-dining concept, built around a validated reservation flow.</span>
          </a>
          <a class="project-link" href="showcase-solarpeak-en.html">
            <strong>SolarPeak</strong>
            <span>Solar company landing page styled as an engineering spec sheet, with real field photography and a comparison datasheet.</span>
          </a>
          <a class="project-link" href="showcase-museroom-en.html">
            <strong>MuseRoom</strong>
            <span>Dark gallery landing page exploring immersive art direction, exhibit cards, and a calm visit flow.</span>
          </a>
          <a class="project-link" href="showcase-lumi-clinic-en.html">
            <strong>LUMI Clinic</strong>
            <span>Editorial beauty clinic page — porcelain-and-ink palette, real photography, and a clear price-list layout.</span>
          </a>
          <a class="project-link" href="showcase-dental-clinic-en.html">
            <strong>BRIGHT Dental Clinic</strong>
            <span>Dental clinic landing page with transparent price table, dentist profiles, and an online booking form.</span>
          </a>
          <a class="project-link" href="showcase-velve-aesthetics-en.html">
            <strong>VELVÉ Aesthetics</strong>
            <span>Aesthetic clinic with a working 4-step booking wizard — pick a service, doctor, and time slot, then confirm.</span>
          </a>
        </div>
      </div>
    </section>
  </main>

  <footer class="footer-band">
    <div class="page-shell footer-inner">
      <span>Landing Page service — Phakin Chawanpunya</span>
      <span>Phakin Chawanpunya</span>
    </div>
  </footer>
</body>
</html>
```

- [ ] **Step 4: Run the same checklist against `landing-page-en.html`**

Same six checks as Step 2, adjusted for English: `<html lang="en">`, `canonical` → `landing-page-en.html`, `og:locale` → `en_US`, every in-body link points at an `-en` URL or an external link, except the `TH` switcher which correctly points at `landing-page.html`.

- [ ] **Step 5: Verify locally**

Serve the site and open both pages. Confirm: the `.study-meta` 4-box grid renders correctly (collapses to 2 columns on tablet, per the existing responsive rule already in `portfolio-pages.css`); all 9 `.project-link` cards in `.project-strip` collapse to 1 column at 375px (existing rule, no new CSS); every project link opens its real showcase page; the `TH`/`EN` switcher round-trips correctly; the Fastwork and email CTAs match every other CTA on the site exactly.

- [ ] **Step 6: Commit**

```bash
git add landing-page.html landing-page-en.html
git commit -m "feat: add Landing Page service category landing page"
```

---

### Task 2: Dashboard UI category page

**Files:**
- Create: `dashboard-ui.html` (Thai)
- Create: `dashboard-ui-en.html` (English)

**Interfaces:**
- Consumes: same shared assets as Task 1.
- Produces: `https://ph-akin.dev/dashboard-ui.html`, `https://ph-akin.dev/dashboard-ui-en.html`, wired in Task 4.

Real content: price ฿7,900, duration 7-10 days, the 4 included-feature bullets, and the ฿15,900 full-system note, all copied verbatim from `index.html:1587-1596` (`Dashboard UI` card). Related project: **BookEase Dashboard** — the only project tagged `dashboard` in the Selected Work grid. One strong, honestly-framed example rather than padding the page with unrelated projects.

- [ ] **Step 1: Create `dashboard-ui.html`**

Follow the exact same document structure as `landing-page.html` (Task 1, Step 1) — same `<head>` boilerplate shape, same nav/footer chrome — with these values substituted:

- `meta description` / `og:description` / `twitter:description`: `รับออกแบบหน้าจอ Dashboard UI สูงสุด 5 หน้าจอ เริ่มต้น 7,900 บาท พร้อมไฟล์ดีไซน์ฉบับเต็มให้ทีมพัฒนานำไปทำต่อ ดูตัวอย่างผลงานจริง`
- `canonical`/`og:url`: `https://ph-akin.dev/dashboard-ui.html`
- `hreflang en`: `https://ph-akin.dev/dashboard-ui-en.html`
- `og:title`/`twitter:title`/`title`: `รับออกแบบ Dashboard UI เริ่มต้น ฿7,900 | Phakin Chawanpunya`
- nav `aria-label`: `เมนู Dashboard UI`; brand `aria-label`: `รับออกแบบ Dashboard UI — กลับไปหน้าพอร์ตโฟลิโอ`; brand text: `รับออกแบบ Dashboard UI`
- nav-links: same `ผลงานทั้งหมด` / `บริการอื่นๆ` / Fastwork primary CTA pattern as Task 1, `EN` link → `dashboard-ui-en.html`
- Hero `h1`: `รับออกแบบ Dashboard UI เริ่มต้น ฿7,900`
- Hero `hero-copy`: `ออกแบบหน้าจอระบบสูงสุด 5 หน้าจอ พร้อมชุดสี ฟอนต์ และองค์ประกอบหลักที่ทีมพัฒนานำไปต่อยอดได้ทันที ส่งงานภายใน 7-10 วัน`
- `.study-meta` 4 boxes:
  - ราคาเริ่มต้น → `฿7,900`
  - ระยะเวลา → `7-10 วัน`
  - แก้ไขได้ → `2 รอบหลังส่งแบบ`
  - เหมาะกับ → `ทีมที่ต้องการดีไซน์ระบบสูงสุด 5 หน้าจอ`
- `.highlight-list` (verbatim from the Services card):
  ```html
  <ul class="highlight-list">
    <li>ออกแบบหน้าจอระบบสูงสุด 5 หน้าจอ</li>
    <li>พร้อมชุดสี ฟอนต์ และองค์ประกอบหลักของดีไซน์ ใช้ต่อได้ทั้งระบบ</li>
    <li>ส่งไฟล์ออกแบบฉบับเต็ม ทีมพัฒนานำไปทำต่อได้ทันที</li>
    <li>แก้ไขได้ 2 รอบหลังส่งแบบ</li>
  </ul>
  ```
- Second `study-block` ("เหมาะกับใคร"): `h2`: `เหมาะกับทีมที่ต้องการดีไซน์ระบบพร้อมใช้`; body: `เหมาะกับสตาร์ทอัพหรือทีมพัฒนาที่มีนักพัฒนาอยู่แล้วแต่ต้องการดีไซน์ระบบที่ชัดเจน ใช้ต่อได้ทันทีโดยไม่ต้องเริ่มจากศูนย์ — ต้องการพัฒนาเป็นระบบใช้งานจริงด้วย เริ่มต้น 15,900 บาท สอบถามเพิ่มเติมได้`
- `#related` heading: `ตัวอย่าง Dashboard UI ที่เคยทำ`; `.project-strip` contains exactly one `.project-link`:
  ```html
  <div class="project-strip">
    <a class="project-link" href="showcase-bookease.html">
      <strong>BookEase Dashboard</strong>
      <span>แดชบอร์ดจองคิวนัดหมาย พร้อมตรวจสอบฟอร์ม เลือกช่วงเวลา และขั้นตอนยืนยันการจอง</span>
    </a>
  </div>
  ```
  Note: `.project-strip`'s grid (`repeat(3, minmax(0,1fr))`) handles a single item fine — it simply occupies the first column, no empty-state styling needed.
- Footer text: `Dashboard UI service — Phakin Chawanpunya`

- [ ] **Step 2: Run the Task 1 Step 2 checklist against `dashboard-ui.html`**

- [ ] **Step 3: Create `dashboard-ui-en.html`**

Same substitution pattern as Step 1, English chrome, Thai pricing/feature content (per Global Constraints):

- `meta description`/`og`/`twitter`: `Dashboard UI design, up to 5 screens, from ฿7,900. Full design files handed off ready for your dev team. See real client work.`
- `canonical`/`og:url`: `https://ph-akin.dev/dashboard-ui-en.html`; `hreflang th` → `dashboard-ui.html`
- `title`/`og:title`/`twitter:title`: `Dashboard UI Design from ฿7,900 | Phakin Chawanpunya`
- nav `aria-label`: `Dashboard UI menu`; brand `aria-label`: `Dashboard UI service — back to portfolio`; brand text: `Dashboard UI Service`; brand `href`: `index-en.html`
- nav-links: `All Work` → `index-en.html#projects`, `Other Services` → `index-en.html#services`, Fastwork primary CTA, `TH` → `dashboard-ui.html`
- Hero `h1`: `Dashboard UI Design, from ฿7,900`
- Hero `hero-copy`: `Up to 5 screens designed with a full color/type/component system your dev team can build on immediately. Delivered in 7-10 days.`
- `.study-meta`: `Starting price` → `฿7,900`; `Timeline` → `7-10 days`; `Revisions` → `2 rounds after design delivery`; `Best for` → `Teams needing up to 5 system screens designed`
- `.highlight-list` — **stays in Thai**, identical to the TH page (per Global Constraints — pricing/feature copy is not translated):
  ```html
  <ul class="highlight-list">
    <li>ออกแบบหน้าจอระบบสูงสุด 5 หน้าจอ</li>
    <li>พร้อมชุดสี ฟอนต์ และองค์ประกอบหลักของดีไซน์ ใช้ต่อได้ทั้งระบบ</li>
    <li>ส่งไฟล์ออกแบบฉบับเต็ม ทีมพัฒนานำไปทำต่อได้ทันที</li>
    <li>แก้ไขได้ 2 รอบหลังส่งแบบ</li>
  </ul>
  ```
- Second `study-block`: `h2`: `A fit for teams that need a ready-to-build design system`; body: `A good fit for startups or dev teams that already have engineers but need a clear, immediately-buildable screen design — no starting from zero. Want it built into a working system too? Full development starts at ฿15,900 — just ask.`
- `#related` heading: `Dashboard UI work I've done`; single `.project-link`:
  ```html
  <div class="project-strip">
    <a class="project-link" href="showcase-bookease-en.html">
      <strong>BookEase Dashboard</strong>
      <span>Appointment booking dashboard with form validation, time-slot picker, and confirmation flow.</span>
    </a>
  </div>
  ```
- Footer text: `Dashboard UI service — Phakin Chawanpunya`

- [ ] **Step 4: Run the Task 1 Step 4 checklist against `dashboard-ui-en.html`**

- [ ] **Step 5: Verify locally**

Same checks as Task 1 Step 5. Specifically confirm the single-item `.project-strip` doesn't look broken (no stretched card, no empty-state message needed — `.project-strip`'s CSS grid handles a partial row natively).

- [ ] **Step 6: Commit**

```bash
git add dashboard-ui.html dashboard-ui-en.html
git commit -m "feat: add Dashboard UI service category landing page"
```

---

### Task 3: Business Website category page

**Files:**
- Create: `business-website.html` (Thai)
- Create: `business-website-en.html` (English)

**Interfaces:**
- Consumes: same shared assets as Tasks 1-2.
- Produces: `https://ph-akin.dev/business-website.html`, `https://ph-akin.dev/business-website-en.html`, wired in Task 4.

Real content: price ฿9,900, duration 10-14 days, the 4 included-feature bullets, and the add-on-systems note, all copied verbatim from `index.html:1604-1613` (`Business Website` card). Related projects: the 5 projects with real interactive/multi-screen functionality — Elevate Commerce, Elasticshop Gaming Top-Up, RATRI Restaurant, VELVÉ Aesthetics, HabitQuest — matching this package's "3-5 pages + can add booking/member/backend systems" positioning. (RATRI Restaurant legitimately belongs on both this page and the Landing Page page — it's both a landing page *and* ships a real reservation system, matching the real, dual nature of that project rather than an indexing mistake.)

- [ ] **Step 1: Create `business-website.html`**

Same document structure as Task 1, with:

- `meta description`/`og`/`twitter`: `รับทำเว็บไซต์ธุรกิจครบวงจร 3-5 หน้า เริ่มต้น 9,900 บาท วางโครงสร้างรองรับ SEO พื้นฐาน พร้อมฟอร์มติดต่อหรือปุ่ม LINE OA ดูตัวอย่างผลงานจริง`
- `canonical`/`og:url`: `https://ph-akin.dev/business-website.html`; `hreflang en` → `business-website-en.html`
- `title`/`og:title`/`twitter:title`: `รับทำเว็บไซต์ธุรกิจ 3-5 หน้า เริ่มต้น ฿9,900 | Phakin Chawanpunya`
- nav `aria-label`: `เมนู Business Website`; brand `aria-label`: `รับทำเว็บไซต์ธุรกิจ — กลับไปหน้าพอร์ตโฟลิโอ`; brand text: `รับทำเว็บไซต์ธุรกิจ`
- nav-links: same pattern as Task 1, `EN` → `business-website-en.html`
- Hero `h1`: `รับทำเว็บไซต์ธุรกิจ เริ่มต้น ฿9,900`
- Hero `hero-copy`: `เว็บไซต์ธุรกิจครบวงจร 3-5 หน้า พัฒนาใหม่ 100% วางโครงสร้างรองรับ SEO พื้นฐาน พร้อมฟอร์มติดต่อหรือปุ่ม LINE OA ส่งงานภายใน 10-14 วัน`
- `.study-meta`: ราคาเริ่มต้น → `฿9,900`; ระยะเวลา → `10-14 วัน`; แก้ไขได้ → `2 รอบ + ฟรีแก้บั๊ก 3 เดือน`; เหมาะกับ → `ธุรกิจที่ต้องการเว็บ 3-5 หน้าพร้อม SEO`
- `.highlight-list` (verbatim):
  ```html
  <ul class="highlight-list">
    <li>พัฒนาใหม่ 100% 3-5 หน้า (หน้าแรก บริการ เกี่ยวกับเรา ผลงาน ติดต่อ)</li>
    <li>วางโครงสร้างรองรับ SEO พื้นฐาน</li>
    <li>ฟอร์มติดต่อหรือปุ่ม LINE OA สำหรับรับลูกค้าของคุณ</li>
    <li>แก้ไขงานได้ 2 รอบ ฟรีบริการแก้ไขปัญหา 3 เดือน</li>
  </ul>
  ```
- Second `study-block`: `h2`: `เหมาะกับธุรกิจที่ต้องการเว็บไซต์ครบวงจร`; body: `เหมาะกับธุรกิจที่ต้องการเว็บไซต์หลายหน้าที่ครอบคลุมทั้งบริการ ผลงาน และช่องทางติดต่อ — ต้องการเพิ่มเติม เช่น ระบบหลังบ้าน ระบบจองคิว ระบบสมาชิก หรือเชื่อมต่อ LINE แจ้งเตือน/แชทบอท สอบถามได้`
- `#related` heading: `ตัวอย่างเว็บไซต์ธุรกิจที่เคยทำ`; `.project-strip`:
  ```html
  <div class="project-strip">
    <a class="project-link" href="showcase-elevate-commerce.html">
      <strong>Elevate Commerce</strong>
      <span>สตาร์ทอัพอีคอมเมิร์ซที่ต้องการหน้าสินค้าพาผู้เข้าชมตั้งแต่เลือกดูจนถึงชำระเงิน</span>
    </a>
    <a class="project-link" href="showcase-elasticshop-gaming.html">
      <strong>Elasticshop Gaming Top-Up</strong>
      <span>ดีไซน์ระบบโทนดำ-เหลืองสำหรับแพลตฟอร์มเติมเงินเกมอัตโนมัติ — ครบ 4 หน้าจอ ดีไซน์แบบเกมเมอร์</span>
    </a>
    <a class="project-link" href="showcase-ratri-restaurant.html">
      <strong>RATRI Restaurant</strong>
      <span>แลนดิ้งเพจโทนมืดสไตล์หรู สำหรับร้านอาหารไทยไฟน์ไดนิ่งสมัยใหม่ พร้อมระบบจองโต๊ะที่ใช้งานได้จริง</span>
    </a>
    <a class="project-link" href="showcase-velve-aesthetics.html">
      <strong>VELVÉ Aesthetics</strong>
      <span>คลินิกเสริมความงามพร้อมระบบจองคิว 4 ขั้นตอนที่ใช้งานได้จริง — เลือกบริการ แพทย์ ช่วงเวลา แล้วยืนยัน</span>
    </a>
    <a class="project-link" href="showcase-habitquest.html">
      <strong>HabitQuest</strong>
      <span>เปลี่ยนนิสัยประจำวันให้กลายเป็นการผจญภัยแบบ RPG — ทำเควส ปราบมอนสเตอร์ และเลเวลอัพฮีโร่ ทีละนิสัยจากชีวิตจริง</span>
    </a>
  </div>
  ```
- Footer text: `Business Website service — Phakin Chawanpunya`

- [ ] **Step 2: Run the Task 1 Step 2 checklist against `business-website.html`**

- [ ] **Step 3: Create `business-website-en.html`**

- `meta description`/`og`/`twitter`: `Full 3-5 page business websites from ฿9,900, built with basic SEO in place, plus a contact form or LINE OA button. See real client work.`
- `canonical`/`og:url`: `https://ph-akin.dev/business-website-en.html`; `hreflang th` → `business-website.html`
- `title`/`og:title`/`twitter:title`: `Business Website Development from ฿9,900 | Phakin Chawanpunya`
- nav `aria-label`: `Business Website menu`; brand `aria-label`: `Business Website service — back to portfolio`; brand text: `Business Website Service`; brand `href`: `index-en.html`
- nav-links: same English pattern as Tasks 1-2, `TH` → `business-website.html`
- Hero `h1`: `Business Website Development, from ฿9,900`
- Hero `hero-copy`: `A complete 3-5 page business site, built 100% from scratch with basic SEO in place and a contact form or LINE OA button ready to capture leads. Delivered in 10-14 days.`
- `.study-meta`: `Starting price` → `฿9,900`; `Timeline` → `10-14 days`; `Revisions` → `2 rounds + 3 months free bug-fixing`; `Best for` → `Businesses needing a 3-5 page site with SEO`
- `.highlight-list` — stays in Thai, identical to the TH page:
  ```html
  <ul class="highlight-list">
    <li>พัฒนาใหม่ 100% 3-5 หน้า (หน้าแรก บริการ เกี่ยวกับเรา ผลงาน ติดต่อ)</li>
    <li>วางโครงสร้างรองรับ SEO พื้นฐาน</li>
    <li>ฟอร์มติดต่อหรือปุ่ม LINE OA สำหรับรับลูกค้าของคุณ</li>
    <li>แก้ไขงานได้ 2 รอบ ฟรีบริการแก้ไขปัญหา 3 เดือน</li>
  </ul>
  ```
- Second `study-block`: `h2`: `A fit for businesses that need a complete website`; body: `A good fit for businesses that need a multi-page site covering services, work, and contact channels — want to add a backend, booking system, membership system, or LINE notifications/chatbot integration? Just ask.`
- `#related` heading: `Business websites I've built`; `.project-strip`:
  ```html
  <div class="project-strip">
    <a class="project-link" href="showcase-elevate-commerce-en.html">
      <strong>Elevate Commerce</strong>
      <span>E-commerce startup needed product pages that guide visitors from browsing to checkout.</span>
    </a>
    <a class="project-link" href="showcase-elasticshop-gaming-en.html">
      <strong>Elasticshop Gaming Top-Up</strong>
      <span>Dark yellow design system for an automated game top-up platform — 4 screen flows with gaming-focused UI patterns.</span>
    </a>
    <a class="project-link" href="showcase-ratri-restaurant-en.html">
      <strong>RATRI Restaurant</strong>
      <span>Elegant dark landing page for a modern Thai fine-dining concept, built around a validated reservation flow.</span>
    </a>
    <a class="project-link" href="showcase-velve-aesthetics-en.html">
      <strong>VELVÉ Aesthetics</strong>
      <span>Aesthetic clinic with a working 4-step booking wizard — pick a service, doctor, and time slot, then confirm.</span>
    </a>
    <a class="project-link" href="showcase-habitquest-en.html">
      <strong>HabitQuest</strong>
      <span>Turn daily habits into an RPG adventure — complete quests, defeat monsters, and level up your hero, one real-life habit at a time.</span>
    </a>
  </div>
  ```
- Footer text: `Business Website service — Phakin Chawanpunya`

- [ ] **Step 4: Run the Task 1 Step 4 checklist against `business-website-en.html`**

- [ ] **Step 5: Verify locally**

Same checks as Tasks 1-2. Confirm all 5 `.project-strip` cards render, including RATRI Restaurant (whose showcase page it links to is unchanged — this page just adds a second inbound link to it).

- [ ] **Step 6: Commit**

```bash
git add business-website.html business-website-en.html
git commit -m "feat: add Business Website service category landing page"
```

---

### Task 4: Wire sitemap, link from Services cards, final verification

**Files:**
- Modify: `sitemap.xml` (add 6 `<url>` entries)
- Modify: `index.html` (3 CTA-row edits)
- Modify: `index-en.html` (3 CTA-row edits)

**Interfaces:**
- Consumes: the 6 pages created in Tasks 1-3.
- Produces: nothing consumed elsewhere — this is the final integration task.

- [ ] **Step 1: Add sitemap entries**

Find this exact block in `sitemap.xml`:
```xml
  <!-- Project showcase pages -->
  <url>
    <loc>https://ph-akin.dev/showcase-buildnest-en.html</loc>
```
Replace with:
```xml
  <!-- Service category landing pages -->
  <url>
    <loc>https://ph-akin.dev/landing-page-en.html</loc>
    <changefreq>monthly</changefreq>
    <priority>0.85</priority>
  </url>
  <url>
    <loc>https://ph-akin.dev/landing-page.html</loc>
    <changefreq>monthly</changefreq>
    <priority>0.85</priority>
  </url>
  <url>
    <loc>https://ph-akin.dev/dashboard-ui-en.html</loc>
    <changefreq>monthly</changefreq>
    <priority>0.85</priority>
  </url>
  <url>
    <loc>https://ph-akin.dev/dashboard-ui.html</loc>
    <changefreq>monthly</changefreq>
    <priority>0.85</priority>
  </url>
  <url>
    <loc>https://ph-akin.dev/business-website-en.html</loc>
    <changefreq>monthly</changefreq>
    <priority>0.85</priority>
  </url>
  <url>
    <loc>https://ph-akin.dev/business-website.html</loc>
    <changefreq>monthly</changefreq>
    <priority>0.85</priority>
  </url>

  <!-- Project showcase pages -->
  <url>
    <loc>https://ph-akin.dev/showcase-buildnest-en.html</loc>
```

- [ ] **Step 2: Link the Landing Page card to `landing-page.html` in `index.html`**

Find this exact block (unique — the `<ul>` content between the h3 and the cta-row differs on every service card, so this whole span is unique even though the h3 and cta-row lines individually repeat across cards):
```html
            <h3 class="card-title">Landing Page / Sale Page</h3>
            <div class="card-price">เริ่มต้น ฿3,900</div>
            <div class="card-duration">ระยะเวลา 5-7 วัน</div>
            <ul class="card-list" role="list">
              <li>พัฒนาใหม่ทั้งหมด ไม่ใช้เทมเพลตสำเร็จรูป</li>
              <li>1 หน้า ไม่เกิน 6 section ลงข้อมูลและรูปภาพให้ครบ</li>
              <li>รองรับการแสดงผลบนมือถือและคอมพิวเตอร์ทุกหน้าจอ</li>
              <li>แก้ไขงานได้ 2 รอบ ฟรีบริการแก้ไขปัญหา 3 เดือน</li>
            </ul>
            <div class="card-cta-row">
              <a class="card-link" href="https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob" target="_blank" rel="noopener noreferrer">เริ่มงานบน Fastwork →</a>
              <a class="card-cta-secondary" href="#contact">ติดต่อสอบถาม</a>
            </div>
```
Replace with (adds one new link at the end of the cta-row):
```html
            <h3 class="card-title">Landing Page / Sale Page</h3>
            <div class="card-price">เริ่มต้น ฿3,900</div>
            <div class="card-duration">ระยะเวลา 5-7 วัน</div>
            <ul class="card-list" role="list">
              <li>พัฒนาใหม่ทั้งหมด ไม่ใช้เทมเพลตสำเร็จรูป</li>
              <li>1 หน้า ไม่เกิน 6 section ลงข้อมูลและรูปภาพให้ครบ</li>
              <li>รองรับการแสดงผลบนมือถือและคอมพิวเตอร์ทุกหน้าจอ</li>
              <li>แก้ไขงานได้ 2 รอบ ฟรีบริการแก้ไขปัญหา 3 เดือน</li>
            </ul>
            <div class="card-cta-row">
              <a class="card-link" href="https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob" target="_blank" rel="noopener noreferrer">เริ่มงานบน Fastwork →</a>
              <a class="card-cta-secondary" href="#contact">ติดต่อสอบถาม</a>
              <a class="card-cta-secondary" href="landing-page.html">ดูตัวอย่างผลงาน →</a>
            </div>
```

- [ ] **Step 3: Link the Dashboard UI card to `dashboard-ui.html` in `index.html`**

Find this exact block:
```html
            <h3 class="card-title">Dashboard UI</h3>
            <div class="card-price">เริ่มต้น ฿7,900</div>
            <div class="card-duration">ระยะเวลา 7-10 วัน</div>
            <ul class="card-list" role="list">
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
```
Replace with:
```html
            <h3 class="card-title">Dashboard UI</h3>
            <div class="card-price">เริ่มต้น ฿7,900</div>
            <div class="card-duration">ระยะเวลา 7-10 วัน</div>
            <ul class="card-list" role="list">
              <li>ออกแบบหน้าจอระบบสูงสุด 5 หน้าจอ</li>
              <li>พร้อมชุดสี ฟอนต์ และองค์ประกอบหลักของดีไซน์ ใช้ต่อได้ทั้งระบบ</li>
              <li>ส่งไฟล์ออกแบบฉบับเต็ม ทีมพัฒนานำไปทำต่อได้ทันที</li>
              <li>แก้ไขได้ 2 รอบหลังส่งแบบ</li>
            </ul>
            <div class="card-note">ต้องการพัฒนาเป็นระบบใช้งานจริง เริ่มต้น ฿15,900 — สอบถามเพิ่มเติมได้</div>
            <div class="card-cta-row">
              <a class="card-link" href="https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob" target="_blank" rel="noopener noreferrer">เริ่มงานบน Fastwork →</a>
              <a class="card-cta-secondary" href="#contact">ติดต่อสอบถาม</a>
              <a class="card-cta-secondary" href="dashboard-ui.html">ดูตัวอย่างผลงาน →</a>
            </div>
```

- [ ] **Step 4: Link the Business Website card to `business-website.html` in `index.html`**

Find this exact block:
```html
            <h3 class="card-title">Business Website</h3>
            <div class="card-price">เริ่มต้น ฿9,900</div>
            <div class="card-duration">ระยะเวลา 10-14 วัน</div>
            <ul class="card-list" role="list">
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
```
Replace with:
```html
            <h3 class="card-title">Business Website</h3>
            <div class="card-price">เริ่มต้น ฿9,900</div>
            <div class="card-duration">ระยะเวลา 10-14 วัน</div>
            <ul class="card-list" role="list">
              <li>พัฒนาใหม่ 100% 3-5 หน้า (หน้าแรก บริการ เกี่ยวกับเรา ผลงาน ติดต่อ)</li>
              <li>วางโครงสร้างรองรับ SEO พื้นฐาน</li>
              <li>ฟอร์มติดต่อหรือปุ่ม LINE OA สำหรับรับลูกค้าของคุณ</li>
              <li>แก้ไขงานได้ 2 รอบ ฟรีบริการแก้ไขปัญหา 3 เดือน</li>
            </ul>
            <div class="card-note">ต้องการเพิ่มเติม เช่น ระบบหลังบ้าน ระบบจองคิว ระบบสมาชิก หรือเชื่อมต่อ LINE แจ้งเตือน/แชทบอท สอบถามได้</div>
            <div class="card-cta-row">
              <a class="card-link" href="https://fastwork.co/byob/0G16E5GFIO?openExternalBrowser=1&amp;source=byob" target="_blank" rel="noopener noreferrer">เริ่มงานบน Fastwork →</a>
              <a class="card-cta-secondary" href="#contact">ติดต่อสอบถาม</a>
              <a class="card-cta-secondary" href="business-website.html">ดูตัวอย่างผลงาน →</a>
            </div>
```

- [ ] **Step 5: Mirror Steps 2-4 into `index-en.html`**

Same three edits, same anchor blocks (the `<h3>`-through-`card-cta-row` text is byte-identical between `index.html` and `index-en.html`, since `#services` is untranslated Thai on both files per Global Constraints — use the exact same three `old_string`/`new_string` pairs from Steps 2-4 above, applied to `index-en.html` instead), except the new link's own visible text is in English and its `href` points at the `-en` category page:
- Landing Page card → `<a class="card-cta-secondary" href="landing-page-en.html">See real work →</a>`
- Dashboard UI card → `<a class="card-cta-secondary" href="dashboard-ui-en.html">See real work →</a>`
- Business Website card → `<a class="card-cta-secondary" href="business-website-en.html">See real work →</a>`

- [ ] **Step 6: Verify locally — full site**

- Serve locally, open all 6 new pages directly, and via the new links from the Services section on `index.html`/`index-en.html`.
- Click every `.project-strip` link on all 6 pages — confirm each lands on the correct real showcase page.
- Click the `TH`/`EN` switcher on each of the 6 pages in both directions.
- Run `npx lighthouse` (mobile + desktop) against all 6 new pages per `CLAUDE.md`'s recipe — Accessibility and SEO must be 100 (these pages reuse only already-100-scoring components, so a failure here means something was mistyped, not a new design flaw).
- Mobile-overflow check at 375×812 on all 6 pages, particularly the `.study-meta` 4-box grid and `.project-strip` grid.
- Confirm `grep -c '<loc>' sitemap.xml` increased by exactly 6 from its pre-plan count.

- [ ] **Step 7: Commit**

```bash
git add sitemap.xml index.html index-en.html
git commit -m "feat: wire service category pages into sitemap and Services section"
```

---

## Final Verification (whole plan)

- All 6 new pages pass the bilingual-pair checklist from `CLAUDE.md`'s "Add a case study" recipe.
- `sitemap.xml` holds 6 more `<loc>` entries than before this plan started, none pointing at a `-th.html` URL (the site's default-language files carry no `-th`/`-en` suffix distinction beyond the established `-en` pattern).
- Every price/duration/feature claim on all 6 pages traces back to the live `#services` section in `index.html` — nothing was invented.
- `git log --oneline -4` shows the four commits from this plan; nothing pushed until requested.
