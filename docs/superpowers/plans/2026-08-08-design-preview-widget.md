# Design Preview Widget Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a "เว็บของคุณจะหน้าตาแบบนี้" widget to `web-clinic.html` — a tabbed sidebar of eight site sections, each swapping a rendered mockup and a caption — and move `#related` to sit directly below it.

**Architecture:** One empty placeholder in the HTML, filled at runtime by a shared self-guarding script that lazily fetches a JSON data file and renders a fixed vocabulary of nine block types. No screenshots, no framework, no build step. Styling is appended to the existing `portfolio-pages.css` using only tokens already defined there.

**Tech Stack:** Vanilla JS (ES2020, no modules), plain CSS, JSON. Same as the rest of the site.

**Spec:** `docs/superpowers/specs/2026-08-08-design-preview-widget-design.md`

## Global Constraints

- **Lighthouse must stay 100 / 100 / 100** (Accessibility / SEO / Performance) on `web-clinic`. Best Practices is capped at 77 sitewide by Microsoft Clarity's third-party cookies — expected, not a regression. Any *other* Best Practices deduction is.
- **`canScrollX: false` at 375 × 812.** Any horizontal scroll must be contained inside the widget's own box.
- **CLS must stay 0.** The placeholder reserves its height before the JSON lands.
- **No new colours.** Only tokens already in `assets/portfolio-pages.css:1-27`: `--bg` `--bg-deep` `--surface` `--surface-2` `--ink` `--ink-2` `--muted` `--line` `--line-2` `--accent` `--accent-dark` `--accent-text` `--amber` `--amber-text` `--r` `--r-sm` `--ease`.
- **No new stylesheet file.** The `.dp-*` block is appended to `assets/portfolio-pages.css`, as the `.story-*` block was.
- **No `-en` twin.** `web-*.html` is Thai-only by design.
- **The mockup brand is `คลินิกของคุณ`** and the URL pill reads `คลินิกของคุณ.com`. Fictional, and must not collide with LUMI / BRIGHT / VELVÉ, which appear in `#related` immediately below.
- **Admin entries carry the literal text `งานเพิ่มเติม · ประเมินราคาแยก`.** The amber dot never carries that meaning alone. ฿3,900 buys one page with no backend; no `<form>` in this repository has an `action`.
- **Serve with `python3 _tools/serve.py 8123`**, never `python3 -m http.server` — the site's URLs are extensionless and `http.server` cannot resolve them, so a Lighthouse run would measure a broken page.

## Deviation from the spec

The spec's **D8** calls for adding a `preview_page` classification to `assets/analytics.js`. **That change is not needed and is dropped.** `classify()` already begins with an explicit opt-in (`assets/analytics.js:68-71`):

```js
const explicit = el.dataset?.track;
if (explicit) return { name: explicit, tags: { ...el.dataset } };
```

and the delegated listener at `assets/analytics.js:125-132` matches `a, button`. Emitting `data-track="preview_page"` plus `data-industry` / `data-page` / `data-side` on each generated tab therefore fires the event with the tags already attached. `analytics.js` is not touched by this plan.

## File Structure

| File | Responsibility |
|---|---|
| `assets/design-preview.json` | Data only. One key per industry. Adding an industry later touches nothing else. |
| `assets/design-preview.js` | Renderer, tab keyboard handling, lazy fetch, self-guard. Knows the nine block types; knows no industry. |
| `assets/portfolio-pages.css` | Gains a `.dp-*` block at the end. Nothing existing is edited. |
| `web-clinic.html` | Gains `#preview` and one script tag; `#related` moves below `#preview`. |
| `CLAUDE.md` | Three corrections this change forces true. |

---

### Task 1: The clinic data file

**Files:**
- Create: `assets/design-preview.json`

**Interfaces:**
- Produces: the contract `design-preview.js` reads. Top level is an object keyed by the `data-preview` attribute value. Each industry has `brand` (string), `url` (string), `note` (string), `pages` (array). Each page has `id` `side` `name` `desc` `parts` `blocks`. `side` is exactly `"customer"` or `"admin"`. Each block has `t` plus the fields its type declares in Task 3's `BLOCKS` table.

- [ ] **Step 1: Write the file**

```json
{
  "clinic": {
    "brand": "คลินิกของคุณ",
    "url": "คลินิกของคุณ.com",
    "note": "฿3,900 คือเว็บหน้าเดียวที่รวมส่วนเหล่านี้ — แยกออกเป็นหลายหน้าเริ่มที่ ฿9,900",
    "pages": [
      {
        "id": "home",
        "side": "customer",
        "name": "หน้าแรก",
        "desc": "สิ่งแรกที่คนเห็น — บอกว่าคุณคือคลินิกอะไร อยู่ที่ไหน และกดจองได้ตรงไหน ภายในสามวินาที",
        "parts": ["พาดหัว", "ปุ่มจองคิว", "บริการเด่น", "ปุ่มไลน์ลอย"],
        "blocks": [
          { "t": "nav", "links": ["บริการ", "ทีมแพทย์", "ผลลัพธ์", "ติดต่อ"], "cta": "จองคิว" },
          { "t": "hero", "title": "ดูแลผิวโดยแพทย์เฉพาะทาง", "sub": "เปิดทุกวัน 10:00–20:00 · ใกล้ BTS", "ctas": ["จองคิวออนไลน์", "ทักไลน์"], "image": true },
          { "t": "head", "title": "บริการยอดนิยม" },
          { "t": "cards", "cols": 3, "items": [
            { "title": "ฟิลเลอร์", "meta": "45 นาที", "price": "เริ่ม ฿8,900" },
            { "title": "เลเซอร์หน้าใส", "meta": "30 นาที", "price": "เริ่ม ฿2,500" },
            { "title": "ทรีตเมนต์สิว", "meta": "60 นาที", "price": "เริ่ม ฿1,900" }
          ]}
        ]
      },
      {
        "id": "services",
        "side": "customer",
        "name": "บริการ + ราคา",
        "desc": "หน้ารวมบริการ แยกเป็นหมวด พร้อมช่วงราคาที่ชัดเจน — รับงานตอบคำถามซ้ำ ๆ ทางไลน์แทนคุณ",
        "parts": ["การ์ดบริการ", "ช่วงราคา", "ระยะเวลา", "ปุ่มจองต่อบริการ"],
        "blocks": [
          { "t": "nav", "links": ["บริการ", "ทีมแพทย์", "ผลลัพธ์", "ติดต่อ"], "cta": "จองคิว" },
          { "t": "head", "title": "บริการทั้งหมด" },
          { "t": "cards", "cols": 3, "items": [
            { "title": "ฟิลเลอร์ร่องแก้ม", "meta": "45 นาที", "price": "฿8,900–15,000" },
            { "title": "โบท็อกซ์", "meta": "30 นาที", "price": "฿4,500–9,000" },
            { "title": "เลเซอร์หน้าใส", "meta": "30 นาที", "price": "฿2,500–4,000" },
            { "title": "ทรีตเมนต์สิว", "meta": "60 นาที", "price": "฿1,900–3,500" },
            { "title": "ร้อยไหม", "meta": "60 นาที", "price": "฿12,000–25,000" },
            { "title": "ปรึกษาแพทย์", "meta": "20 นาที", "price": "ไม่มีค่าใช้จ่าย" }
          ]}
        ]
      },
      {
        "id": "team",
        "side": "customer",
        "name": "ทีมแพทย์",
        "desc": "โปรไฟล์แพทย์และทีมงาน พร้อมวุฒิและประสบการณ์ — คนไข้เลือกคลินิกจากคนที่ลงมือทำ",
        "parts": ["รูปแพทย์", "วุฒิการศึกษา", "ความชำนาญ", "ปุ่มเลือกแพทย์"],
        "blocks": [
          { "t": "nav", "links": ["บริการ", "ทีมแพทย์", "ผลลัพธ์", "ติดต่อ"], "cta": "จองคิว" },
          { "t": "head", "title": "แพทย์ประจำคลินิก" },
          { "t": "cards", "cols": 3, "items": [
            { "title": "พญ. — แพทย์ผิวหนัง", "meta": "ประสบการณ์ 12 ปี", "price": "เลือกแพทย์ท่านนี้" },
            { "title": "นพ. — เวชศาสตร์ความงาม", "meta": "ประสบการณ์ 8 ปี", "price": "เลือกแพทย์ท่านนี้" },
            { "title": "พญ. — เลเซอร์ผิวหนัง", "meta": "ประสบการณ์ 6 ปี", "price": "เลือกแพทย์ท่านนี้" }
          ]}
        ]
      },
      {
        "id": "results",
        "side": "customer",
        "name": "ผลลัพธ์ก่อน-หลัง",
        "desc": "แกลเลอรีก่อน-หลัง จัดวางให้ดูน่าเชื่อถือ ไม่ดูเกินจริง พร้อมข้อความกำกับว่าผลลัพธ์แต่ละคนต่างกัน",
        "parts": ["ภาพคู่ก่อน-หลัง", "ชื่อคอร์ส", "จำนวนครั้ง", "ข้อความกำกับ"],
        "blocks": [
          { "t": "nav", "links": ["บริการ", "ทีมแพทย์", "ผลลัพธ์", "ติดต่อ"], "cta": "จองคิว" },
          { "t": "head", "title": "ผลลัพธ์จากคนไข้จริง" },
          { "t": "gallery", "cols": 4, "count": 8 },
          { "t": "list", "items": [
            { "label": "หมายเหตุ", "value": "ผลลัพธ์ขึ้นกับสภาพผิวของแต่ละบุคคล" }
          ]}
        ]
      },
      {
        "id": "booking",
        "side": "customer",
        "name": "จองคิวออนไลน์",
        "desc": "เลือกบริการ เลือกแพทย์ เลือกเวลา แล้วยืนยัน — ปุ่มจองติดอยู่ทุกหน้าจอ ไม่ต้องเลื่อนหา",
        "parts": ["เลือกบริการ", "เลือกแพทย์", "เลือกวันเวลา", "ยืนยันการจอง"],
        "blocks": [
          { "t": "nav", "links": ["บริการ", "ทีมแพทย์", "ผลลัพธ์", "ติดต่อ"], "cta": "จองคิว" },
          { "t": "head", "title": "จองคิวออนไลน์" },
          { "t": "form", "fields": [
            { "label": "เลือกบริการ", "value": "ฟิลเลอร์ร่องแก้ม" },
            { "label": "เลือกแพทย์", "value": "ไม่ระบุ — แพทย์ท่านใดก็ได้" },
            { "label": "วันที่", "value": "จ. 12 ส.ค." },
            { "label": "ช่วงเวลา", "value": "14:00" },
            { "label": "ชื่อผู้จอง", "value": "" },
            { "label": "เบอร์โทร", "value": "" }
          ], "submit": "ยืนยันการจอง" }
        ]
      },
      {
        "id": "contact",
        "side": "customer",
        "name": "ติดต่อ + แผนที่",
        "desc": "แผนที่ เวลาทำการ และช่องทางติดต่อครบทุกช่อง — คนหาคลินิกแถวนั้นต้องเจอทางมาให้ได้",
        "parts": ["แผนที่", "เวลาทำการ", "ไลน์ / โทร", "ที่จอดรถ"],
        "blocks": [
          { "t": "nav", "links": ["บริการ", "ทีมแพทย์", "ผลลัพธ์", "ติดต่อ"], "cta": "จองคิว" },
          { "t": "head", "title": "ติดต่อและเดินทาง" },
          { "t": "map", "lines": ["ชั้น 2 อาคารตัวอย่าง", "ใกล้ BTS · เดิน 3 นาที", "มีที่จอดรถ"] },
          { "t": "list", "items": [
            { "label": "จันทร์–ศุกร์", "value": "10:00–20:00" },
            { "label": "เสาร์–อาทิตย์", "value": "10:00–18:00" },
            { "label": "ไลน์", "value": "@yourclinic" },
            { "label": "โทร", "value": "0X-XXX-XXXX" }
          ]}
        ]
      },
      {
        "id": "admin-queue",
        "side": "admin",
        "name": "Admin — ตารางนัดหมาย",
        "desc": "หน้าจอฝั่งคุณ เห็นคิววันนี้ทั้งหมด ยืนยัน เลื่อน หรือยกเลิกได้ โดยไม่ต้องเปิดสมุดจด",
        "parts": ["คิววันนี้", "สถานะการจอง", "ยืนยัน / เลื่อน", "ค้นหาคนไข้"],
        "blocks": [
          { "t": "nav", "links": ["ตารางนัดหมาย", "บริการ", "รายงาน"], "cta": "ออกจากระบบ", "admin": true },
          { "t": "head", "title": "คิววันนี้ · 12 ส.ค." },
          { "t": "table",
            "cols": ["เวลา", "คนไข้", "บริการ", "แพทย์", "สถานะ"],
            "rows": [
              ["10:00", "คนไข้ A", "เลเซอร์หน้าใส", "พญ.", "ยืนยันแล้ว"],
              ["11:30", "คนไข้ B", "ทรีตเมนต์สิว", "นพ.", "รอยืนยัน"],
              ["14:00", "คนไข้ C", "ฟิลเลอร์ร่องแก้ม", "พญ.", "ยืนยันแล้ว"],
              ["16:30", "คนไข้ D", "ปรึกษาแพทย์", "ไม่ระบุ", "รอยืนยัน"]
            ]}
        ]
      },
      {
        "id": "admin-services",
        "side": "admin",
        "name": "Admin — จัดการบริการ",
        "desc": "เพิ่มบริการ แก้ราคา หรือปิดบริการชั่วคราวได้เอง ไม่ต้องทักหาคนทำเว็บทุกครั้งที่ปรับราคา",
        "parts": ["เพิ่มบริการ", "แก้ราคา", "เปิด/ปิดบริการ", "จัดลำดับ"],
        "blocks": [
          { "t": "nav", "links": ["ตารางนัดหมาย", "บริการ", "รายงาน"], "cta": "ออกจากระบบ", "admin": true },
          { "t": "head", "title": "บริการทั้งหมด" },
          { "t": "table",
            "cols": ["บริการ", "ระยะเวลา", "ราคา", "สถานะ"],
            "rows": [
              ["ฟิลเลอร์ร่องแก้ม", "45 นาที", "฿8,900–15,000", "เปิด"],
              ["โบท็อกซ์", "30 นาที", "฿4,500–9,000", "เปิด"],
              ["เลเซอร์หน้าใส", "30 นาที", "฿2,500–4,000", "เปิด"],
              ["ร้อยไหม", "60 นาที", "฿12,000–25,000", "ปิดชั่วคราว"]
            ]}
        ]
      }
    ]
  }
}
```

- [ ] **Step 2: Verify it parses**

Run: `python3 -m json.tool assets/design-preview.json > /dev/null && echo OK`
Expected: `OK`

- [ ] **Step 3: Verify the invariants the renderer depends on**

Run:
```bash
python3 - <<'PY'
import json
d = json.load(open('assets/design-preview.json'))['clinic']
pages = d['pages']
assert len(pages) == 8, len(pages)
assert [p['id'] for p in pages] == ['home','services','team','results','booking','contact','admin-queue','admin-services']
assert all(p['side'] in ('customer','admin') for p in pages)
assert len({p['id'] for p in pages}) == 8, 'duplicate id'
assert all(p['blocks'] and p['parts'] and p['desc'] for p in pages)
known = {'nav','hero','head','cards','list','form','gallery','map','table'}
used = {b['t'] for p in pages for b in p['blocks']}
assert used <= known, used - known
print('OK', len(pages), 'pages, block types used:', sorted(used))
PY
```
Expected: `OK 8 pages, block types used: ['cards', 'form', 'gallery', 'head', 'hero', 'list', 'map', 'nav', 'table']`

- [ ] **Step 4: Commit**

```bash
git add assets/design-preview.json
git commit -m "feat: add clinic data for the design-preview widget"
```

---

### Task 2: The `.dp-*` stylesheet block

**Files:**
- Modify: `assets/portfolio-pages.css` — append at end of file (currently 992 lines)

**Interfaces:**
- Produces: the class names Task 3's renderer emits. Every one is listed in the CSS below; the renderer must not invent others.

- [ ] **Step 1: Append the block**

Append to the end of `assets/portfolio-pages.css`:

```css
/* ============================================================
   Design preview widget — "เว็บของคุณจะหน้าตาแบบนี้"
   Built by assets/design-preview.js from assets/design-preview.json.
   Uses only tokens declared at the top of this file; defines no colours.
   Lives here rather than in its own file so the web-* pages keep loading
   exactly one stylesheet — see CLAUDE.md, "Two stylesheet families".
   ============================================================ */

.dp-head {
  display: flex;
  gap: 14px;
  align-items: flex-start;
  margin-bottom: 6px;
}

.dp-badge {
  flex: none;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  display: grid;
  place-items: center;
  background: var(--accent-dark);
  color: #fff;
}

.dp-badge svg { width: 22px; height: 22px; }

.dp-head h2 { margin: 0 0 4px; font-size: clamp(1.35rem, 2.4vw, 1.75rem); }
.dp-head p { margin: 0; color: var(--muted); font-size: 0.9rem; line-height: 1.65; }

.dp-legend {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px 18px;
  margin: 14px 0 16px;
  font-size: 0.8rem;
  color: var(--muted);
}

.dp-legend > span { display: inline-flex; align-items: center; gap: 7px; }
.dp-legend .dp-dot { width: 8px; height: 8px; border-radius: 50%; flex: none; }
.dp-dot-customer { background: var(--accent-text); }
.dp-dot-admin { background: var(--amber-text); }
.dp-hint { margin-left: auto; color: var(--accent-text); font-weight: 600; }

.dp-note {
  margin: 0 0 16px;
  padding-left: 12px;
  border-left: 2px solid var(--line-2);
  color: var(--muted);
  font-size: 0.83rem;
  line-height: 1.6;
}

/* The frame reuses .browser-frame / .browser-frame-bar / .browser-dot /
   .browser-url, already defined above. Only the right-hand badge is new. */
.dp-frame-tag {
  margin-left: auto;
  padding: 3px 10px;
  border-radius: 999px;
  border: 1px solid var(--line-2);
  color: var(--muted);
  font-size: 0.68rem;
  white-space: nowrap;
}

.dp-body { display: flex; flex-direction: column; }

.dp-tabs {
  display: flex;
  gap: 4px;
  padding: 8px;
  overflow-x: auto;
  scrollbar-width: none;
  border-bottom: 1px solid var(--line);
  background: var(--bg-deep);
}

.dp-tabs::-webkit-scrollbar { display: none; }

.dp-tab {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  flex: none;
  padding: 9px 12px;
  border: 0;
  border-radius: var(--r-sm);
  background: transparent;
  color: var(--ink-2);
  font: inherit;
  font-size: 0.83rem;
  text-align: left;
  cursor: pointer;
  transition: background 0.2s var(--ease), color 0.2s var(--ease);
}

.dp-tab .dp-dot { width: 7px; height: 7px; border-radius: 50%; flex: none; }
.dp-tab:hover { background: var(--surface-2); color: var(--ink); }
.dp-tab[aria-selected="true"] { background: var(--accent-light); color: var(--ink); font-weight: 600; }
.dp-tab:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }

.dp-pane { padding: 18px 16px 20px; min-width: 0; }

/* ---- the mockup ---- */
.dp-mock {
  border: 1px solid var(--line);
  border-radius: var(--r-sm);
  background: var(--bg);
  padding: 14px;
  display: grid;
  gap: 14px;
  min-width: 0;
}

.dp-mock-nav {
  display: flex;
  align-items: center;
  gap: 14px;
  padding-bottom: 12px;
  border-bottom: 1px solid var(--line);
}

.dp-brand { font-weight: 800; color: var(--accent-text); font-size: 0.95rem; }
.dp-mock-nav ul { display: flex; gap: 14px; margin: 0 0 0 auto; padding: 0; list-style: none; }
.dp-mock-nav li { color: var(--muted); font-size: 0.76rem; }

.dp-pill {
  padding: 5px 12px;
  border-radius: 999px;
  background: var(--accent-dark);
  color: #fff;
  font-size: 0.74rem;
  font-weight: 600;
  white-space: nowrap;
}

.dp-pill.ghost { background: transparent; border: 1px solid var(--line-2); color: var(--ink-2); }

.dp-hero { display: grid; gap: 12px; }
.dp-hero h3 { margin: 0; font-size: 1.15rem; color: var(--ink); }
.dp-hero p { margin: 0; color: var(--muted); font-size: 0.8rem; }
.dp-hero-actions { display: flex; flex-wrap: wrap; gap: 8px; }

.dp-mock h4 {
  margin: 0;
  font-size: 0.9rem;
  color: var(--ink);
}

.dp-img {
  display: grid;
  place-items: center;
  border-radius: var(--r-sm);
  background: var(--surface-2);
  color: var(--muted);
  font-size: 0.72rem;
  min-height: 78px;
}

.dp-hero .dp-img { min-height: 120px; }

.dp-grid { display: grid; gap: 10px; }
.dp-grid[data-cols="2"] { grid-template-columns: repeat(2, minmax(0, 1fr)); }
.dp-grid[data-cols="3"] { grid-template-columns: repeat(3, minmax(0, 1fr)); }
.dp-grid[data-cols="4"] { grid-template-columns: repeat(4, minmax(0, 1fr)); }

.dp-card {
  border: 1px solid var(--line);
  border-radius: var(--r-sm);
  background: var(--surface);
  overflow: hidden;
  min-width: 0;
}

.dp-card .dp-img { border-radius: 0; }
.dp-card-body { padding: 9px 10px 11px; display: grid; gap: 3px; }
.dp-card-body strong { font-size: 0.78rem; color: var(--ink); font-weight: 600; }
.dp-card-body span { font-size: 0.7rem; color: var(--muted); }
.dp-card-body em { font-style: normal; font-size: 0.78rem; color: var(--accent-text); font-weight: 600; }

.dp-rows { display: grid; gap: 0; border: 1px solid var(--line); border-radius: var(--r-sm); overflow: hidden; }
.dp-row { display: flex; justify-content: space-between; gap: 12px; padding: 9px 12px; font-size: 0.76rem; }
.dp-row + .dp-row { border-top: 1px solid var(--line); }
.dp-row span:first-child { color: var(--muted); }
.dp-row span:last-child { color: var(--ink-2); text-align: right; }

.dp-fields { display: grid; gap: 9px; }
.dp-field { display: grid; gap: 4px; }
.dp-field span { font-size: 0.7rem; color: var(--muted); }
.dp-field div {
  border: 1px solid var(--line-2);
  border-radius: var(--r-sm);
  background: var(--surface);
  padding: 8px 11px;
  font-size: 0.76rem;
  color: var(--ink-2);
  min-height: 34px;
}

.dp-map { display: grid; gap: 10px; }
.dp-map .dp-img { min-height: 110px; }

.dp-table-wrap { overflow-x: auto; border: 1px solid var(--line); border-radius: var(--r-sm); }
.dp-table { width: 100%; border-collapse: collapse; font-size: 0.74rem; min-width: 460px; }
.dp-table th, .dp-table td { padding: 8px 11px; text-align: left; white-space: nowrap; }
.dp-table th { background: var(--surface-2); color: var(--ink-2); font-weight: 600; }
.dp-table td { color: var(--muted); border-top: 1px solid var(--line); }

/* ---- the caption ---- */
.dp-caption { margin-top: 16px; }
.dp-caption-head { display: flex; flex-wrap: wrap; align-items: center; gap: 8px; margin-bottom: 5px; }
.dp-caption h3 { margin: 0; font-size: 0.98rem; color: var(--ink); }

.dp-tag {
  padding: 3px 9px;
  border-radius: 999px;
  font-size: 0.68rem;
  font-weight: 600;
  white-space: nowrap;
}

.dp-tag-customer { background: var(--accent-light); color: var(--accent-text); }
.dp-tag-admin { background: var(--amber); color: var(--amber-text); }
.dp-caption > p { margin: 0; color: var(--muted); font-size: 0.85rem; line-height: 1.7; }

.dp-parts { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; margin-top: 10px; }
.dp-parts > span:first-child { font-size: 0.7rem; color: var(--muted); }

.dp-part {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 3px 10px;
  border: 1px solid var(--line-2);
  border-radius: 999px;
  font-size: 0.72rem;
  color: var(--ink-2);
}

.dp-part::before {
  content: "";
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background: var(--accent-text);
  flex: none;
}

@media (min-width: 900px) {
  .dp-body { flex-direction: row; }
  .dp-tabs {
    flex-direction: column;
    width: 224px;
    flex: none;
    overflow-x: visible;
    border-bottom: 0;
    border-right: 1px solid var(--line);
  }
  .dp-tab { width: 100%; }
  .dp-pane { flex: 1 1 auto; padding: 20px; }
}

@media (max-width: 639px) {
  .dp-grid[data-cols="3"] { grid-template-columns: minmax(0, 1fr); }
  .dp-grid[data-cols="4"] { grid-template-columns: repeat(2, minmax(0, 1fr)); }
  .dp-mock-nav ul { display: none; }
  .dp-hint { margin-left: 0; flex-basis: 100%; }
}

@media (prefers-reduced-motion: reduce) {
  .dp-tab { transition: none; }
}
```

- [ ] **Step 2: Verify no colour literal slipped in**

Run:
```bash
awk '/Design preview widget/,0' assets/portfolio-pages.css \
  | grep -nE '#[0-9a-fA-F]{3,8}\b|rgba?\(' | grep -v 'background: #fff\|color: #fff' || echo "OK — no raw colours"
```
Expected: `OK — no raw colours` (the two `#fff` on `.dp-badge` / `.dp-pill` are white-on-accent-dark, which the site already ships at 6.4:1)

- [ ] **Step 3: Commit**

```bash
git add assets/portfolio-pages.css
git commit -m "feat: add .dp-* styles for the design-preview widget"
```

---

### Task 3: The renderer

**Files:**
- Create: `assets/design-preview.js`

**Interfaces:**
- Consumes: `assets/design-preview.json` (Task 1) and the `.dp-*` classes (Task 2).
- Consumes: `<div class="design-preview" data-preview="<key>"></div>` (Task 4).
- Produces: tabs carrying `data-track="preview_page"`, `data-industry`, `data-page`, `data-side` — read by the existing `classify()` in `assets/analytics.js`. No change to that file.

**BLOCKS vocabulary** — the renderer handles exactly these nine `t` values:

| `t` | Fields it reads |
|---|---|
| `nav` | `links[]`, `cta`, `admin?` |
| `hero` | `title`, `sub`, `ctas[]`, `image?` |
| `head` | `title` |
| `cards` | `cols`, `items[]` of `{title, meta, price}` |
| `list` | `items[]` of `{label, value}` |
| `form` | `fields[]` of `{label, value}`, `submit` |
| `gallery` | `cols`, `count` |
| `map` | `lines[]` |
| `table` | `cols[]`, `rows[][]` |

- [ ] **Step 1: Write the file**

```js
/* Design preview widget — "เว็บของคุณจะหน้าตาแบบนี้"
   Fills <div class="design-preview" data-preview="clinic"></div>.

   Self-guarding: returns immediately when the placeholder is absent, so the
   file is harmless anywhere it is loaded.

   Versioned in the tag as ?v=1. BUMP IT on any change to the generated
   markup — a returning visitor pairing new HTML with a cached older copy of
   this script gets an empty placeholder and no widget at all. That is exactly
   what happened to site-search.js during testing.

   The data is fetched on IntersectionObserver rather than at load: the widget
   sits well below the fold and must not compete with LCP. */
(function () {
  'use strict';

  const root = document.querySelector('.design-preview');
  if (!root) return;

  const KEY = root.dataset.preview;
  if (!KEY) return;

  const el = (tag, cls, text) => {
    const n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  };

  const img = (label) => el('div', 'dp-img', label || 'ภาพ');

  /* ---- the nine block types ---- */
  const BLOCKS = {
    nav(b, ctx) {
      const n = el('div', 'dp-mock-nav');
      n.append(el('span', 'dp-brand', b.admin ? ctx.brand + ' · Admin' : ctx.brand));
      const ul = el('ul');
      (b.links || []).forEach((l) => ul.append(el('li', null, l)));
      n.append(ul);
      if (b.cta) n.append(el('span', b.admin ? 'dp-pill ghost' : 'dp-pill', b.cta));
      return n;
    },

    hero(b) {
      const n = el('div', 'dp-hero');
      if (b.image) n.append(img());
      n.append(el('h3', null, b.title));
      if (b.sub) n.append(el('p', null, b.sub));
      if (b.ctas && b.ctas.length) {
        const row = el('div', 'dp-hero-actions');
        b.ctas.forEach((c, i) => row.append(el('span', i ? 'dp-pill ghost' : 'dp-pill', c)));
        n.append(row);
      }
      return n;
    },

    head(b) {
      return el('h4', null, b.title);
    },

    cards(b) {
      const g = el('div', 'dp-grid');
      g.dataset.cols = String(b.cols || 3);
      (b.items || []).forEach((it) => {
        const c = el('div', 'dp-card');
        c.append(img());
        const body = el('div', 'dp-card-body');
        body.append(el('strong', null, it.title));
        if (it.meta) body.append(el('span', null, it.meta));
        if (it.price) body.append(el('em', null, it.price));
        c.append(body);
        g.append(c);
      });
      return g;
    },

    list(b) {
      const w = el('div', 'dp-rows');
      (b.items || []).forEach((it) => {
        const r = el('div', 'dp-row');
        r.append(el('span', null, it.label));
        r.append(el('span', null, it.value));
        w.append(r);
      });
      return w;
    },

    form(b) {
      const w = el('div', 'dp-fields');
      (b.fields || []).forEach((f) => {
        const g = el('div', 'dp-field');
        g.append(el('span', null, f.label));
        g.append(el('div', null, f.value || ''));
        w.append(g);
      });
      if (b.submit) w.append(el('span', 'dp-pill', b.submit));
      return w;
    },

    gallery(b) {
      const g = el('div', 'dp-grid');
      g.dataset.cols = String(b.cols || 4);
      for (let i = 0; i < (b.count || 4); i++) g.append(img(i % 2 ? 'หลัง' : 'ก่อน'));
      return g;
    },

    map(b) {
      const w = el('div', 'dp-map');
      w.append(img('แผนที่'));
      const rows = el('div', 'dp-rows');
      (b.lines || []).forEach((l) => {
        const r = el('div', 'dp-row');
        r.append(el('span', null, l));
        rows.append(r);
      });
      w.append(rows);
      return w;
    },

    table(b) {
      const wrap = el('div', 'dp-table-wrap');
      const t = el('table', 'dp-table');
      const thead = el('thead');
      const hr = el('tr');
      (b.cols || []).forEach((c) => hr.append(el('th', null, c)));
      thead.append(hr);
      const tbody = el('tbody');
      (b.rows || []).forEach((row) => {
        const tr = el('tr');
        row.forEach((cell) => tr.append(el('td', null, cell)));
        tbody.append(tr);
      });
      t.append(thead, tbody);
      wrap.append(t);
      return wrap;
    }
  };

  const renderMock = (page, ctx) => {
    /* aria-hidden is correct here and is the point: this is an illustration
       of a website. Everything it means is stated as real text in the caption
       inside the same tabpanel — page name, purpose and component list. */
    const m = el('div', 'dp-mock');
    m.setAttribute('aria-hidden', 'true');
    (page.blocks || []).forEach((b) => {
      const fn = BLOCKS[b.t];
      if (fn) m.append(fn(b, ctx));
    });
    return m;
  };

  const renderCaption = (page) => {
    const c = el('div', 'dp-caption');
    const head = el('div', 'dp-caption-head');
    head.append(el('h3', null, page.name));
    head.append(
      page.side === 'admin'
        ? el('span', 'dp-tag dp-tag-admin', 'งานเพิ่มเติม · ประเมินราคาแยก')
        : el('span', 'dp-tag dp-tag-customer', 'หน้าฝั่งลูกค้า')
    );
    c.append(head);
    c.append(el('p', null, page.desc));
    const parts = el('div', 'dp-parts');
    parts.append(el('span', null, 'ส่วนประกอบ:'));
    (page.parts || []).forEach((p) => parts.append(el('span', 'dp-part', p)));
    c.append(parts);
    return c;
  };

  const ICON =
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" ' +
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">' +
    '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M9 9v11"/></svg>';

  const build = (data) => {
    const ctx = { brand: data.brand };
    const pages = data.pages || [];
    if (!pages.length) return;

    /* header */
    const head = el('div', 'dp-head');
    const badge = el('span', 'dp-badge');
    badge.innerHTML = ICON;
    const headText = el('div');
    headText.append(el('h2', null, 'เว็บของคุณจะหน้าตาแบบนี้'));
    headText.append(el('p', null, 'ภาพจำลองดีไซน์ ไม่ใช่หน้าเว็บจริง — กดเลือกดูได้ทีละส่วน'));
    head.append(badge, headText);

    /* legend */
    const legend = el('div', 'dp-legend');
    const mk = (cls, label) => {
      const s = el('span');
      s.append(el('span', 'dp-dot ' + cls));
      s.append(document.createTextNode(label));
      return s;
    };
    legend.append(mk('dp-dot-customer', 'หน้าฝั่งลูกค้า'));
    legend.append(mk('dp-dot-admin', 'หน้าฝั่ง Admin'));
    legend.append(el('span', 'dp-hint', 'กดเลือกเพื่อดูตัวอย่าง'));

    /* frame */
    const frame = el('div', 'browser-frame');
    const bar = el('div', 'browser-frame-bar');
    ['red', 'amber', 'green'].forEach((c) =>
      bar.append(el('span', 'browser-dot browser-dot-' + c))
    );
    bar.append(el('span', 'browser-url', data.url));
    bar.append(el('span', 'dp-frame-tag', 'ตัวอย่างดีไซน์'));

    const body = el('div', 'dp-body');
    const tabs = el('div', 'dp-tabs');
    tabs.setAttribute('role', 'tablist');
    tabs.setAttribute('aria-label', 'เลือกส่วนของเว็บเพื่อดูตัวอย่าง');
    const pane = el('div', 'dp-pane');

    const buttons = pages.map((page, i) => {
      const b = el('button', 'dp-tab');
      b.type = 'button';
      b.id = 'dp-tab-' + page.id;
      b.setAttribute('role', 'tab');
      b.setAttribute('aria-controls', 'dp-panel');
      b.setAttribute('aria-selected', i === 0 ? 'true' : 'false');
      b.tabIndex = i === 0 ? 0 : -1;
      b.append(el('span', 'dp-dot ' + (page.side === 'admin' ? 'dp-dot-admin' : 'dp-dot-customer')));
      b.append(document.createTextNode(page.name));
      /* Read by the existing data-track opt-in in analytics.js — no change
         to that file is needed. */
      b.dataset.track = 'preview_page';
      b.dataset.industry = KEY;
      b.dataset.page = page.id;
      b.dataset.side = page.side;
      tabs.append(b);
      return b;
    });

    /* One panel, swapped in place. The panel wraps the CAPTION as well as the
       mockup — the caption is the only content a screen reader can read, so a
       panel containing only the aria-hidden mockup would be an empty shell.
       No aria-live: a correct tab pattern already announces the change through
       aria-selected, and a live region on top of it announces twice. */
    pane.id = 'dp-panel';
    pane.setAttribute('role', 'tabpanel');
    pane.tabIndex = 0;

    let current = 0;
    const show = (i) => {
      current = i;
      const page = pages[i];
      buttons.forEach((b, j) => {
        b.setAttribute('aria-selected', j === i ? 'true' : 'false');
        b.tabIndex = j === i ? 0 : -1;
      });
      pane.setAttribute('aria-labelledby', buttons[i].id);
      pane.replaceChildren(renderMock(page, ctx), renderCaption(page));
    };

    buttons.forEach((b, i) => b.addEventListener('click', () => show(i)));

    tabs.addEventListener('keydown', (e) => {
      const last = buttons.length - 1;
      let next = null;
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown') next = current === last ? 0 : current + 1;
      else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') next = current === 0 ? last : current - 1;
      else if (e.key === 'Home') next = 0;
      else if (e.key === 'End') next = last;
      if (next === null) return;
      e.preventDefault();
      show(next);
      buttons[next].focus();
    });

    body.append(tabs, pane);
    frame.append(bar, body);

    root.replaceChildren(head, legend);
    if (data.note) root.append(el('p', 'dp-note', data.note));
    root.append(frame);
    show(0);
  };

  const load = () => {
    fetch('assets/design-preview.json')
      .then((r) => (r.ok ? r.json() : Promise.reject(new Error(r.status))))
      .then((all) => {
        if (all[KEY]) build(all[KEY]);
      })
      .catch(() => {
        /* Leave the placeholder empty. A failed fetch must not leave a broken
           frame or a reserved gap on the page. */
      });
  };

  if ('IntersectionObserver' in window) {
    const io = new IntersectionObserver(
      (entries) => {
        if (entries.some((e) => e.isIntersecting)) {
          io.disconnect();
          load();
        }
      },
      { rootMargin: '600px' }
    );
    io.observe(root);
  } else {
    load();
  }
})();
```

- [ ] **Step 2: Syntax-check**

Run: `node --check assets/design-preview.js && echo OK`
Expected: `OK`

- [ ] **Step 3: Commit**

```bash
git add assets/design-preview.js
git commit -m "feat: add the design-preview renderer"
```

---

### Task 4: Wire it into `web-clinic.html`

**Files:**
- Modify: `web-clinic.html` — add script tag near line 36; insert `#preview` after `</section>` at line 383; move `#related` (lines 386-412) to follow it

**Interfaces:**
- Consumes: everything from Tasks 1-3.

- [ ] **Step 1: Add the script tag**

In the `<head>`, immediately after the `site-search.js` line (`web-clinic.html:36`), insert:

```html
  <script src="assets/design-preview.js?v=1" defer></script>
```

- [ ] **Step 2: Insert `#preview` and move `#related` below it**

`#process` ends at `web-clinic.html:383`. `#related` currently spans lines 386-412. Cut the whole `#related` section and re-insert it *after* the new `#preview` section, so the region between `</section>` (end of `#process`) and `<section class="section" id="faq">` reads:

```html
    <section class="section" id="preview">
      <div class="page-shell">
        <div class="design-preview" data-preview="clinic"></div>
      </div>
    </section>

    <section class="section" id="related">
      <div class="page-shell">
        <div class="section-heading">
          <div>
            <span class="eyebrow">ตัวอย่างงานออกแบบ</span>
            <h2>ตัวอย่างเว็บคลินิกที่ผมออกแบบไว้</h2>
          </div>
        </div>
        <div class="project-strip">
          <a class="project-link" href="showcase-lumi-clinic">
            <img src="assets/thumbs/lumi-clinic.svg" alt="" loading="lazy" width="351" height="220" />
            <strong>LUMI Clinic</strong>
            <span>หน้าเว็บคลินิกความงามสไตล์เอดิทอเรียล โทนสีขาวหมึกดำ ภาพถ่ายจริง ตารางราคาชัดเจน และไทม์ไลน์คอร์สที่จริงใจ แทนภาพก่อน-หลังปลอมๆ</span>
          </a>
          <a class="project-link" href="showcase-dental-clinic">
            <img src="assets/thumbs/bright-dental.svg" alt="" loading="lazy" width="351" height="220" />
            <strong>BRIGHT Dental Clinic</strong>
            <span>แลนดิ้งเพจคลินิกทันตกรรม โทนดำ-ครีม ตัดด้วยสีส้ม พร้อมตารางราคาโปร่งใส โปรไฟล์ทันตแพทย์ และฟอร์มจองคิวออนไลน์</span>
          </a>
          <a class="project-link" href="showcase-velve-aesthetics">
            <img src="assets/velve/care-tools.jpg" alt="" loading="lazy" width="351" height="220" />
            <strong>VELVÉ Aesthetics</strong>
            <span>คลินิกเสริมความงามพร้อมระบบจองคิว 4 ขั้นตอนที่ใช้งานได้จริง — เลือกบริการ แพทย์ ช่วงเวลา แล้วยืนยัน — เขียนด้วย vanilla JS ล้วน</span>
          </a>
        </div>
      </div>
    </section>
```

- [ ] **Step 3: Verify structure and that nothing links to a moved id**

Run:
```bash
grep -c 'id="related"' web-clinic.html            # expect 1
grep -n 'id="preview"\|id="related"\|id="faq"' web-clinic.html   # preview < related < faq
grep -o 'href="#[a-z-]*"' web-clinic.html | sort -u              # every target must still exist
python3 -c "
import re;s=open('web-clinic.html').read()
ids=set(re.findall(r'id=\"([a-z0-9-]+)\"',s))
bad=[h for h in set(re.findall(r'href=\"#([a-z0-9-]+)\"',s)) if h not in ids]
print('dead anchors:',bad or 'none')"
```
Expected: `1`, ascending line numbers in that order, `dead anchors: none`

- [ ] **Step 4: Commit**

```bash
git add web-clinic.html
git commit -m "feat: add the design-preview widget to web-clinic, move #related below it"
```

---

### Task 5: Verify against the site's standards, then correct CLAUDE.md

**Files:**
- Modify: `CLAUDE.md`

- [ ] **Step 1: Serve the site**

Run: `python3 _tools/serve.py 8123 &`
(Never `python3 -m http.server` — it cannot resolve this site's extensionless URLs.)

- [ ] **Step 2: Lighthouse, mobile and desktop**

```bash
npx -y lighthouse http://localhost:8123/web-clinic --quiet \
  --chrome-flags="--headless" --output=json --output-path=/tmp/lh-clinic-mobile.json
npx -y lighthouse http://localhost:8123/web-clinic --quiet --preset=desktop \
  --chrome-flags="--headless" --output=json --output-path=/tmp/lh-clinic-desktop.json
python3 -c "
import json
for v in ('mobile','desktop'):
    d=json.load(open(f'/tmp/lh-clinic-{v}.json'))
    print(v, {k:round(c['score']*100) for k,c in d['categories'].items() if c.get('score') is not None})
    print(' failed:',[k for k,a in d['audits'].items() if a.get('score') is not None and a['score']<1])"
```
Expected: Accessibility 100, SEO 100, Performance 100; Best Practices 77. Read the failed-audit list, not just the scores — `label-content-name-mismatch` has weight 0 and would leave the score at 100 while failing.

- [ ] **Step 3: Check overflow and CLS at 375 × 812**

In a browser at 375 × 812 on `/web-clinic`:

```js
({canScrollX: (function(){document.documentElement.scrollLeft=50;const s=document.documentElement.scrollLeft;document.documentElement.scrollLeft=0;return s>0;})(),
  bw: document.body.scrollWidth, cw: document.documentElement.clientWidth,
  tabsScroll: document.querySelector('.dp-tabs').scrollWidth > document.querySelector('.dp-tabs').clientWidth})
```
Expected: `canScrollX: false`, `bw <= cw`, `tabsScroll: true` — the strip scrolls inside its own box, which is the point.

- [ ] **Step 4: Check the tab semantics**

```js
[...document.querySelectorAll('.dp-tab')].map(b => [b.textContent.trim(), b.getAttribute('aria-selected'), b.tabIndex])
```
Expected: 8 rows, exactly one `"true"`, that one with `tabIndex 0` and the rest `-1`.

Then by keyboard only: Tab to the tablist, press ArrowRight through all eight and past the end (wraps to first), Home and End jump to the ends, and the panel content changes each time.

- [ ] **Step 5: Check graceful degradation**

Block `assets/design-preview.js` in DevTools and reload. Expected: `#preview` renders as an empty section — no broken frame, no reserved gap, no console error. Then restore and confirm `?cl_debug` logs `preview_page` with `industry`, `page` and `side` when a tab is clicked.

- [ ] **Step 6: Correct CLAUDE.md**

Three statements this change makes false:

1. Under **Add an industry landing page**: "no page in this family has ever needed new CSS" and "All four are built from existing components; **no page in this family has ever needed new CSS.**" — rewrite to record that the `.dp-*` block was appended to `portfolio-pages.css` on 2026-08-08 (no new file, no new colours), and that everything else in the family still needs none.
2. Same section: add `#preview` to the page's section list, before `#related`.
3. Under **Site search**: note that a second versioned self-rendering script now exists, `design-preview.js?v=`, carrying the identical cache-pairing hazard — bump the version on any change to its generated markup.

- [ ] **Step 7: Commit**

```bash
git add CLAUDE.md
git commit -m "docs: record the design-preview widget and the CSS-family exception it creates"
```

---

## Self-Review

**Spec coverage.** T1 → Task 1 data (`side: "admin"`) + Task 3 `renderCaption` (literal badge text) + Task 5 Step 5. T2 → `note` field, Task 1. T3 → header sub-line and `.dp-frame-tag`, Task 3. T4 → `brand` / `url`, Task 1. D1 → Task 4. D2 → Task 4 Steps 1-2. D3 → Task 1 + `load()`/IntersectionObserver in Task 3. D4 → the `BLOCKS` table and its nine implementations. D5 → Task 2, verified by Step 2's colour grep. D6 → Task 3's tablist block and the `aria-hidden` comment, verified Task 5 Steps 2 and 4. D7 → Task 2's two media queries, verified Task 5 Step 3. D8 → **dropped, with reason recorded above**; the behaviour still ships via `data-track`.

**Placeholders.** None. Every code step carries the full file or the exact insertion.

**Type consistency.** `page.side` is `"customer" | "admin"` in Task 1, in `renderCaption`, and in the tab dot class. Block `t` values in Task 1's data are exactly the nine keys of `BLOCKS`, asserted mechanically by Task 1 Step 3. The `.dp-*` class names emitted in Task 3 all exist in Task 2. `dp-panel` and `dp-tab-<id>` are the only generated ids and neither collides with an id already in `web-clinic.html`.
