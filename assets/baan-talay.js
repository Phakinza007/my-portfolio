/* ─────────────────────────────────────────────────────────────
   BAAN TALAY — resort site.

   Nothing here talks to a server: no fetch, no XHR, no <form> and no action
   attribute anywhere on the page. Rates, availability and the booking
   reference are all computed in the browser, and the footer says so.

   THE ONE RULE THAT MAKES THIS READ AS REAL: availability and rates are
   derived from a seeded hash of (room, date) — never Math.random(). A real
   booking engine returns the same answer for the same date on every reload.
   A demo that reshuffles on refresh is spotted instantly.
   ───────────────────────────────────────────────────────────── */
(function () {
  'use strict';

  var IMG = 'assets/baan-talay/';

  var IC = {
    ac: 'M4 7h16M4 12h16M8 16l-2 3M16 16l2 3',
    wifi: 'M5 12.5a10 10 0 0 1 14 0M8 15.5a6 6 0 0 1 8 0M12 18.5h.01',
    fridge: 'M7 3h10v18H7zM7 10h10M10 6v2M10 13v2',
    balcony: 'M4 20V9l8-5 8 5v11M9 20v-6h6v6',
    sea: 'M3 17c2-2 4-2 6 0s4 2 6 0 4-2 6 0M6.5 10.5a3 3 0 1 1 6 0',
    tub: 'M3 12h18v4a3 3 0 0 1-3 3H6a3 3 0 0 1-3-3zM7 12V6a2 2 0 0 1 4 0',
    coffee: 'M4 8h11v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5zM15 9h2.5a2.5 2.5 0 0 1 0 5H15M4 21h13',
    kitchen: 'M4 4h16v6H4zM7 14v6M12 14v6M17 14v6',
    wash: 'M4 3h16v18H4zM8 7h.01M11 7h.01M12 16.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z',
    rooms2: 'M3 18v-5h18v5M6 13V9h5v4M14 13V9h5v4',
    sofa: 'M4 16v-5a2 2 0 0 1 4 0v3h8v-3a2 2 0 0 1 4 0v5M3 16h18v3H3z',
    beach: 'M2 17c2.2-2.6 4.4-2.6 6.6 0s4.4 2.6 6.6 0 4.4-2.6 6.8 0',
    pool: 'M3 18c2-2 4-2 6 0s4 2 6 0 4-2 6 0M8 15V5m8 10V5M8 8h8M8 12h8',
    clock: 'M12 3a9 9 0 1 0 0 18 9 9 0 0 0 0-18zM12 7v5l3.5 2',
    spa: 'M12 21c0-5 3-8 8-9-1 5-4 8-8 9zM12 21c0-5-3-8-8-9 1 5 4 8 8 9zM12 21V11',
    gym: 'M4 9v6M8 7v10M16 7v10M20 9v6M8 12h8',
    dine: 'M6 3v8a2 2 0 0 0 4 0V3M8 11v10M17 3c-1.4 1.8-2 3.6-2 5.4h4c0-1.8-.6-3.6-2-5.4zM17 8.4V21',
    kids: 'M12 5a2 2 0 1 0 0-4 2 2 0 0 0 0 4zM9 21v-6H7l2-6h6l2 6h-2v6',
    car: 'M5 17h14M4 17v-4l2-5h12l2 5v4M7.5 13h.01M16.5 13h.01',
    shield: 'M12 3l8 3v6c0 4.5-3.2 7.9-8 9-4.8-1.1-8-4.5-8-9V6z'
  };

  /* ── data: language-neutral (ids, numbers, images) ───────────
     `total` is the real room count per type and sums to 24, which is the
     figure the hero copy states. If one changes the other must. */
  var ROOMS = [
    { slug: 'room-garden', base: 2400, total: 8, size: 28, cap: 2, bf: false,
      shots: ['room-garden', 'room-window', 'suite-living'],
      amen: ['ac', 'wifi', 'fridge', 'balcony'] },
    { slug: 'room-breeze', base: 3200, total: 6, size: 34, cap: 2, bf: true,
      shots: ['room-breeze', 'room-bed', 'sea'],
      amen: ['sea', 'tub', 'wifi', 'coffee'] },
    { slug: 'room-villa', base: 5800, total: 4, size: 52, cap: 3, bf: true,
      shots: ['room-villa', 'boardwalk', 'beach-morning'],
      amen: ['beach', 'balcony', 'tub', 'sofa'] },
    { slug: 'room-family', base: 6500, total: 6, size: 65, cap: 5, bf: true,
      shots: ['room-family', 'suite-bed', 'pool'],
      amen: ['rooms2', 'kitchen', 'wash', 'tub'] }
  ];

  var GAL = [
    { img: 'beach-morning', w: 1800 }, { img: 'pool' }, { img: 'breakfast' },
    { img: 'boardwalk' }, { img: 'interior' }, { img: 'sea' },
    { img: 'resort-evening' }, { img: 'aerial-sea' }, { img: 'dining-room' },
    { img: 'spa-treatment' }, { img: 'grounds' }, { img: 'suite-living' }
  ];

  var OUTLETS = [{ img: 'dining-room', icon: 'dine' }, { img: 'bar', icon: 'coffee' }];
  var FACS = [
    { icon: 'pool' }, { icon: 'beach' }, { icon: 'spa' },
    { icon: 'gym' }, { icon: 'kids' }, { icon: 'car' }
  ];
  var OFFERS = [{ code: 'EARLYBIRD', off: 15, lead: true }, { code: 'STAY3PAY2', off: 33 }, { code: 'HONEYMOON', off: 0 }];

  /* Ratings are fixed, not generated — a score that drifts between reloads is
     the same tell as availability that drifts. */
  var SCORE = { avg: 4.7, count: 128,
    bars: [['clean', 4.9], ['location', 4.8], ['service', 4.8], ['food', 4.6], ['value', 4.5]] };
  var REVIEWS = [
    { id: 0, initial: 'ณ', score: 5, room: 2, month: '2026-07', trip: 'couple', verified: true, reply: false },
    { id: 1, initial: 'S', score: 5, room: 1, month: '2026-07', trip: 'couple', verified: true, reply: false },
    { id: 2, initial: 'พ', score: 4, room: 3, month: '2026-06', trip: 'family', verified: true, reply: true },
    { id: 3, initial: 'M', score: 5, room: 2, month: '2026-06', trip: 'couple', verified: true, reply: false },
    { id: 4, initial: 'อ', score: 3, room: 0, month: '2026-05', trip: 'solo', verified: true, reply: true },
    { id: 5, initial: 'ก', score: 5, room: 3, month: '2026-05', trip: 'family', verified: true, reply: false },
    { id: 6, initial: 'J', score: 4, room: 1, month: '2026-04', trip: 'friends', verified: true, reply: false },
    { id: 7, initial: 'ธ', score: 5, room: 2, month: '2026-04', trip: 'couple', verified: true, reply: false },
    { id: 8, initial: 'ว', score: 5, room: 0, month: '2026-03', trip: 'solo', verified: true, reply: false },
    { id: 9, initial: 'A', score: 4, room: 3, month: '2026-03', trip: 'family', verified: false, reply: false }
  ];

  /* ── the rate engine ─────────────────────────────────────────
     FNV-1a. Any stable hash works; what matters is that the same input
     always yields the same output, across reloads and across devices. */
  function h32(s) {
    var h = 2166136261 >>> 0;
    for (var i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619) >>> 0; }
    return h >>> 0;
  }
  function rnd(s) { return h32(s) / 4294967296; }

  function parts(iso) { var d = new Date(iso + 'T00:00'); return { d: d, dow: d.getDay(), m: d.getMonth() + 1, day: d.getDate() }; }
  function season(iso) {
    var m = parts(iso).m;
    if (m >= 11 || m <= 2) return { key: 'high', mult: 1.35 };
    if (m >= 6 && m <= 9) return { key: 'green', mult: 0.85 };
    return { key: 'shoulder', mult: 1 };
  }
  function isWeekend(iso) { var w = parts(iso).dow; return w === 5 || w === 6; }
  function isPeak(iso) {
    var p = parts(iso);
    if (p.m === 12 && p.day >= 29) return true;
    if (p.m === 1 && p.day <= 2) return true;
    if (p.m === 4 && p.day >= 12 && p.day <= 15) return true;
    return false;
  }
  function minStay(iso) { return isPeak(iso) ? 3 : isWeekend(iso) ? 2 : 1; }

  function rateFor(i, iso) {
    var r = ROOMS[i].base * season(iso).mult;
    if (isWeekend(iso)) r *= 1.20;
    if (isPeak(iso)) r *= 1.15;
    r *= 0.97 + rnd('r' + i + iso) * 0.06;   // ±3%, seeded — never random
    return Math.round(r / 50) * 50;
  }
  function invFor(i, iso) {
    var total = ROOMS[i].total, p = rnd('i' + i + iso);
    if (isPeak(iso)) p *= 0.30;
    else if (isWeekend(iso)) p *= 0.62;
    else if (season(iso).key === 'green') p = 0.45 + p * 0.55;
    return Math.max(0, Math.round(p * total));
  }

  function iso(d) {
    return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0');
  }
  function addDays(isoStr, n) { var d = new Date(isoStr + 'T00:00'); d.setDate(d.getDate() + n); return iso(d); }
  function nightsBetween(ci, co) {
    var out = [], cur = ci, guard = 0;
    while (cur < co && guard++ < 60) { out.push(cur); cur = addDays(cur, 1); }
    return out;
  }
  function daysUntil(isoStr) {
    return Math.round((new Date(isoStr + 'T00:00') - new Date(iso(new Date()) + 'T00:00')) / 86400000);
  }

  /* min inventory across every night of the stay — a room you cannot keep
     for the whole stay is not available for that stay */
  function stay(i, ci, co) {
    var ns = nightsBetween(ci, co), left = Infinity, sum = 0, rows = [], need = 1;
    ns.forEach(function (d) {
      var inv = invFor(i, d), rate = rateFor(i, d);
      left = Math.min(left, inv); sum += rate;
      need = Math.max(need, minStay(d));
      rows.push({ iso: d, rate: rate, inv: inv, weekend: isWeekend(d), peak: isPeak(d) });
    });
    return { rows: rows, sum: sum, nights: ns.length, left: left === Infinity ? ROOMS[i].total : left, minStay: need };
  }

  window.BT_ENGINE = { rateFor: rateFor, invFor: invFor, stay: stay, season: season, isPeak: isPeak, minStay: minStay };

  /* ── copy ────────────────────────────────────────────────────
     Every user-visible string lives here, in both languages, so no section
     can end up half-translated. Arrays run parallel to the data above. */
  var L = {};

  L.th = {
    code: 'th', other: 'EN',
    nav: { rooms: 'ห้องพัก', dining: 'ห้องอาหาร', facilities: 'สิ่งอำนวยความสะดวก', offers: 'แพ็กเกจ',
      reviews: 'รีวิว', about: 'เกี่ยวกับเรา', gallery: 'แกลเลอรี', faq: 'คำถามที่พบบ่อย',
      contact: 'ติดต่อและการเดินทาง', book: 'เช็คห้องว่าง', menu: 'เมนู', close: 'ปิด', home: 'หน้าแรก', skip: 'ข้ามไปเนื้อหาหลัก' },
    c: { from: 'เริ่มต้น', perNight: '/ คืน', night: 'คืน', guest: 'คน', baht: '฿',
      inclTax: 'รวมภาษีและค่าบริการแล้ว', back: 'ย้อนกลับ', viewAll: 'ดูทั้งหมด', more: 'ดูรายละเอียด',
      soldOut: 'เต็มแล้ว', left: 'เหลือ {n} ห้องสุดท้าย', selected: 'เลือกอยู่' },
    hero: { badge: '24 ห้อง · หาดส่วนตัว', title: 'ทะเลที่ยังเงียบอยู่',
      lede: 'รีสอร์ต 24 ห้องติดหาดส่วนตัว หัวหิน ไม่มีเสียงปาร์ตี้ ไม่มีคิวรอ' },
    search: { in: 'เช็คอิน', out: 'เช็คเอาท์', guests: 'ผู้เข้าพัก', go: 'ค้นหาห้องว่าง',
      nights: 'รวม {n} คืน · ผู้เข้าพัก {g} คน', pickOut: 'เลือกวันเช็คเอาท์ต่อได้เลย',
      strip: 'ราคาต่อคืน 14 วันข้างหน้า', stripNote: 'ราคาเปลี่ยนตามฤดูกาลและวันในสัปดาห์',
      minStay: 'ช่วงนี้เข้าพักขั้นต่ำ {n} คืน', noRooms: 'ช่วงวันที่เลือกเต็มทุกห้อง ลองเลื่อนวันดูอีกครั้ง' },
    feats: ['หาดส่วนตัว 200 เมตร', 'อาหารเช้าทำสดทุกจาน', '2 สระ แยกสระเด็ก', 'ห่างตลาดโต้รุ่ง 8 นาที'],
    sec: {
      rooms: 'ห้องพัก 4 แบบ', roomsLede: 'ราคาต่อคืนคิดตามวันที่เลือกจริง รวมภาษีและค่าบริการแล้ว',
      dining: 'ห้องอาหารและบาร์', diningLede: 'ครัวเปิดทุกวัน วัตถุดิบทะเลรับตรงจากแพปลาหัวหินทุกเช้า',
      facs: 'สิ่งอำนวยความสะดวก', facsLede: 'ทุกอย่างอยู่ในรีสอร์ต เดินถึงได้ภายในสองนาที',
      offers: 'แพ็กเกจและส่วนลด', offersLede: 'จองตรงกับเราถูกกว่าเสมอ ไม่มีค่าธรรมเนียมเอเจนซี',
      reviews: 'รีวิวจากผู้เข้าพัก', reviewsLede: 'ทุกรีวิวมาจากผู้ที่เข้าพักจริงและยืนยันการจองแล้ว',
      gallery: 'แกลเลอรี', about: 'เกี่ยวกับบ้านทะเล', contact: 'ติดต่อและการเดินทาง',
      faq: 'คำถามที่พบบ่อย', policy: 'นโยบายที่พัก', location: 'ที่ตั้ง'
    },
    teaser: [
      { t: 'ห้องพัก', s: '4 แบบ เริ่ม ฿2,400' },
      { t: 'ห้องอาหาร', s: 'ซีฟู้ดสดริมหาด' },
      { t: 'สปาและสระ', s: 'เปิดถึงสองทุ่ม' }
    ],
    rooms: [
      { name: 'Garden Room', bed: 'ควีน',
        blurb: 'ชั้นล่างเปิดออกสวน เดินถึงหาด 90 เมตร',
        detail: 'ห้องชั้นล่างเปิดประตูออกสวนได้เลย เดินถึงหาด 90 เมตร เงียบที่สุดในรีสอร์ตเพราะอยู่ปีกหลัง เหมาะกับคนมาพักคนเดียวหรือสองคนที่ตั้งใจมานอนอ่านหนังสือ ห้องน้ำแยกส่วนเปียกแห้ง มีระเบียงนั่งได้สองคน',
        amen: ['แอร์', 'Wi-Fi ฟรี', 'ตู้เย็นเล็ก', 'ระเบียงสวน'] },
      { name: 'Sea Breeze', bed: 'คิง',
        blurb: 'ชั้นสอง เห็นทะเลผ่านแนวต้นสน',
        detail: 'อยู่ชั้นสอง มองเห็นทะเลผ่านแนวต้นสน กลางคืนได้ยินเสียงคลื่นเบา ๆ พอดี ไม่ดังจนนอนไม่หลับ ห้องน้ำมีอ่างอาบน้ำและหน้าต่างเปิดรับลม เตียงคิงขนาด 180 ซม. พร้อมเครื่องชงกาแฟและใบชาจากไร่ในจังหวัด',
        amen: ['วิวทะเลบางส่วน', 'อ่างอาบน้ำ', 'Wi-Fi ฟรี', 'เครื่องชงกาแฟ'] },
      { name: 'Beachfront Villa', bed: 'คิง + โซฟาเบด',
        blurb: 'หลังเดี่ยวติดหาด เปิดประตูเจอทราย',
        detail: 'วิลล่าหลังเดี่ยวติดหาด เปิดประตูเจอทรายเลย มีระเบียงไม้ส่วนตัวหันหน้าออกทะเล เช้า ๆ พนักงานยกอาหารเช้ามาเสิร์ฟที่ระเบียงได้ตามนัด มีเพียงสี่หลังในรีสอร์ต จึงเต็มเร็วที่สุดในช่วงวันหยุดยาว',
        amen: ['ติดหาดโดยตรง', 'ระเบียงส่วนตัว', 'อ่างอาบน้ำ', 'โซฟาเบดเสริม'] },
      { name: 'Family Suite', bed: 'คิง + เดี่ยว 2',
        blurb: 'สองห้องนอนแยกประตู ใกล้สระเด็ก',
        detail: 'สองห้องนอนแยกประตู เดินถึงสระเด็ก 20 ก้าว มีโต๊ะกินข้าวในห้องและครัวเล็กสำหรับอุ่นอาหาร เตียงเด็กอ่อนยืมได้ฟรี และมีประตูกั้นบันไดให้ยืมสำหรับบ้านที่มีเด็กเล็ก',
        amen: ['2 ห้องนอน', 'ครัวเล็ก', 'เครื่องซักผ้า', 'อ่างอาบน้ำเด็ก'] }
    ],
    roomUI: { size: 'ขนาด', cap: 'พักได้', bed: 'เตียง', sqm: 'ตร.ม.', amen: 'สิ่งอำนวยความสะดวก',
      shots: 'ภาพห้องนี้', bookThis: 'จองห้องนี้', rate: 'ราคาต่อคืน',
      note: 'ยกเลิกฟรีก่อนเช็คอิน 7 วัน · เช็คอิน 14:00 เช็คเอาท์ 12:00',
      sideNote: 'ยกเลิกฟรีก่อนเช็คอิน 7 วัน มัดจำ 50% ตอนจอง', bfIncl: 'รวมอาหารเช้า' },
    dining: [
      { name: 'ครัวบ้านทะเล', hours: 'เปิด 06:30–22:00 น. ทุกวัน',
        body: 'ห้องอาหารหลักอยู่ริมหาด เปิดตั้งแต่อาหารเช้าถึงมื้อค่ำ ปลาและกุ้งรับจากแพปลาหัวหินทุกเช้า เมนูเปลี่ยนตามที่จับได้ในวันนั้น ครัวทำอาหารเจและอาหารแพ้กลูเตนได้ถ้าแจ้งล่วงหน้าหนึ่งวัน',
        menu: [['ปลากะพงนึ่งมะนาว', '฿380'], ['กุ้งแม่น้ำเผา (ครึ่งกิโล)', '฿520'], ['แกงส้มชะอมกุ้ง', '฿260'], ['ข้าวผัดปูก้อน', '฿220']] },
      { name: 'บาร์ริมสระ', hours: 'เปิด 15:00–23:00 น. ทุกวัน',
        body: 'บาร์เล็กข้างสระหลัก เสิร์ฟค็อกเทลและอาหารว่างจนถึงห้าทุ่ม ช่วงพระอาทิตย์ตกมีที่นั่งริมทรายให้จองล่วงหน้าได้ที่แผนกต้อนรับ ไม่มีค่าจองและไม่มีขั้นต่ำ',
        menu: [['มะพร้าวปั่นรัม', '฿220'], ['มะม่วงน้ำปลาหวานโซดา', '฿180'], ['เฟรนช์ฟรายส์สาหร่าย', '฿150'], ['ยำมะม่วงกุ้งแห้ง', '฿190']] }
    ],
    facs: [
      { name: 'สระว่ายน้ำหลัก', body: 'สระยาว 20 เมตร ลึก 1.2–1.5 เมตร มีเก้าอี้ผ้าใบและร่มให้ใช้ฟรี', hours: '07:00–20:00 น.' },
      { name: 'หาดส่วนตัว', body: 'หาดหน้ารีสอร์ตยาว 200 เมตร มีเตียงผ้าใบ ผ้าเช็ดตัว และเรือคายัคให้ยืม', hours: 'ตลอดวัน' },
      { name: 'สปา', body: 'ห้องทรีตเมนต์สองห้อง นวดไทยและนวดน้ำมัน จองที่แผนกต้อนรับล่วงหน้าสองชั่วโมง', hours: '10:00–20:00 น.' },
      { name: 'ฟิตเนส', body: 'ห้องออกกำลังกายเล็ก ลู่วิ่งสองเครื่อง จักรยาน และดัมบ์เบล ใช้คีย์การ์ดห้องเข้าได้', hours: '06:00–22:00 น.' },
      { name: 'สระเด็กและมุมเด็กเล่น', body: 'สระลึก 40 ซม. แยกจากสระหลัก มีของเล่นและหนังสือภาพให้ยืม', hours: '08:00–18:00 น.' },
      { name: 'ที่จอดรถและรับส่ง', body: 'ที่จอดรถในรีสอร์ต 20 คัน ฟรี รับส่งสถานีรถไฟหัวหินแจ้งล่วงหน้าหนึ่งวัน', hours: 'ตลอดวัน' }
    ],
    offers: [
      { name: 'จองล่วงหน้า 30 วัน', save: 'ลด 15%', tag: 'คุ้มที่สุด',
        body: 'จองก่อนวันเข้าพักอย่างน้อย 30 วัน รับส่วนลดทันทีตอนคิดราคา ใช้ได้กับทุกห้องและทุกฤดูกาล',
        terms: ['ต้องจองล่วงหน้าอย่างน้อย 30 วัน', 'ใช้ร่วมกับส่วนลดอื่นไม่ได้', 'ยกเลิกฟรีตามนโยบายปกติ'] },
      { name: 'พัก 3 คืน จ่าย 2', save: 'ประหยัด 1 คืน',
        body: 'เข้าพักติดต่อกันสามคืนขึ้นไป คืนที่สามไม่คิดค่าห้อง เหมาะกับช่วงกลางสัปดาห์ที่รีสอร์ตเงียบที่สุด',
        terms: ['เฉพาะเข้าพักวันอาทิตย์ถึงพฤหัสบดี', 'ไม่รวมช่วงวันหยุดนักขัตฤกษ์', 'ส่วนลดคิดจากคืนที่ถูกที่สุด'] },
      { name: 'ฮันนีมูน', save: 'ของขวัญในห้อง',
        body: 'สำหรับคู่ที่แจ้งโอกาสพิเศษตอนจอง จัดดอกไม้ ผลไม้ และอาหารเช้าเสิร์ฟที่ระเบียงหนึ่งครั้ง',
        terms: ['แจ้งล่วงหน้าอย่างน้อย 3 วัน', 'เฉพาะห้อง Sea Breeze และ Beachfront Villa', 'ไม่มีค่าใช้จ่ายเพิ่ม'] }
    ],
    reviewUI: { of5: 'จาก 5', count: 'รีวิว {n} รายการ', stayed: 'พักห้อง', verified: 'ยืนยันการเข้าพักแล้ว',
      replyBy: 'ตอบกลับจากบ้านทะเล', trip: { couple: 'มาเป็นคู่', family: 'มากับครอบครัว', solo: 'มาคนเดียว', friends: 'มากับเพื่อน' },
      bars: { clean: 'ความสะอาด', location: 'ทำเลที่ตั้ง', service: 'การบริการ', food: 'อาหาร', value: 'ความคุ้มค่า' } },
    reviews: [
      { name: 'ณัฐพงษ์ ส.', body: 'วิลล่าติดหาดจริงอย่างที่บอก เปิดประตูออกไปเจอทรายเลย เงียบมากตอนกลางคืน ได้ยินแค่เสียงคลื่น อาหารเช้าเสิร์ฟที่ระเบียงตามที่นัดไว้ ตรงเวลาทุกวัน' },
      { name: 'Sarah W.', body: 'เตียงนุ่มมากและห้องน้ำสะอาดจริง ๆ ชอบที่มีหน้าต่างในห้องน้ำ ลมเข้าตลอด พนักงานพูดอังกฤษได้และช่วยจัดรถไปตลาดโต้รุ่งให้' },
      { name: 'พิมพ์ชนก ร.', body: 'มากับลูกสองคน ห้อง Family Suite กว้างพอจริง สระเด็กอยู่ใกล้มาก เดินไปได้เอง ติดอย่างเดียวคือครัวเล็กไม่มีเตาจริง อุ่นอาหารได้อย่างเดียว ถ้ารู้ก่อนคงเตรียมตัวต่างไป',
        reply: 'ขอบคุณที่บอกตรง ๆ ครับ ในห้องมีไมโครเวฟกับกาต้มน้ำแต่ไม่มีเตาไฟ เราเพิ่มข้อมูลนี้ในหน้าห้องแล้ว และถ้าต้องการอุ่นอาหารมื้อใหญ่ แจ้งครัวได้ตลอดครับ ไม่มีค่าใช้จ่าย' },
      { name: 'Marco B.', body: 'ห้อง Sea Breeze เห็นทะเลผ่านต้นสนพอดี ไม่ได้เห็นเต็มตาแต่ก็สวยและลมดี ราคาคุ้มมากเมื่อเทียบกับที่พักแถวเดียวกัน' },
      { name: 'อรทัย ก.', body: 'ห้องสวนเงียบสมคำโฆษณา แต่ช่วงที่ไปมีงานซ่อมสระตอนกลางวัน เสียงดังอยู่สองวัน ไม่มีใครแจ้งล่วงหน้าตอนจอง ส่วนอื่นดีหมด พนักงานน่ารักมาก',
        reply: 'ต้องขออภัยจริง ๆ ครับ งานซ่อมสระรอบนั้นเราแจ้งเฉพาะที่แผนกต้อนรับ ไม่ได้แจ้งตอนยืนยันการจอง ตอนนี้เราแจ้งล่วงหน้าทางไลน์ทุกครั้งที่มีงานซ่อม และคืนส่วนต่างให้ผู้เข้าพักช่วงนั้นแล้วครับ' },
      { name: 'กิตติพงศ์ ว.', body: 'พาพ่อแม่มา ห้องสวีทเดินสบายไม่มีบันไดเยอะ อาหารเช้าทำสดจริง สั่งไข่ได้ตามใจ ประทับใจที่พนักงานจำชื่อได้ตั้งแต่วันที่สอง' },
      { name: 'Julia P.', body: 'เงียบและสะอาด เหมาะกับคนอยากพักจริง ๆ ไม่ใช่คนอยากปาร์ตี้ Wi-Fi เร็วพอทำงานได้ ติดแค่ว่าบาร์ปิดห้าทุ่ม อยากให้เปิดดึกกว่านี้นิดหนึ่ง' },
      { name: 'ธนกร อ.', body: 'จองผ่านเว็บโดยตรงถูกกว่าเอเจนซีประมาณเจ็ดร้อยบาท ได้ห้องเดียวกัน ขั้นตอนจองง่ายและได้เลขจองทันที' },
      { name: 'วรรณา ต.', body: 'มาคนเดียวสามคืน อ่านหนังสือจบสองเล่ม ไม่มีอะไรรบกวนเลย ชอบที่หาดไม่มีคนขายของเดินผ่าน' },
      { name: 'Andreas K.', body: 'ห้องครอบครัวคุ้มมากสำหรับสี่คน เตียงเสริมสบายกว่าที่คิด สระเด็กตื้นพอให้ปล่อยเด็กเล่นได้โดยไม่ต้องลงไปเฝ้าตลอด' }
    ],
    about: { title: 'เกี่ยวกับบ้านทะเล',
      p: ['บ้านทะเลเปิดในปี 2560 จากบ้านพักตากอากาศของครอบครัวที่ตั้งอยู่บนที่ดินผืนนี้มาตั้งแต่รุ่นคุณตา เราตั้งใจไม่ขยายเกิน 24 ห้อง เพราะจำนวนนี้คือจำนวนที่พนักงานยี่สิบคนดูแลได้ทั่วถึงจริง ไม่ใช่ตัวเลขที่คำนวณจากผลตอบแทน',
        'เราไม่รับจัดงานเลี้ยงและไม่เปิดเพลงในพื้นที่ส่วนกลางหลังสามทุ่ม เพราะคนที่เลือกมาที่นี่ส่วนใหญ่มาเพื่อความเงียบ ถ้าคุณกำลังมองหาที่พักที่มีกิจกรรมตลอดวัน เราอาจไม่ใช่ที่ที่เหมาะ และเราบอกตรง ๆ ตั้งแต่ตอนนี้ดีกว่า',
        'อาหารทะเลทั้งหมดรับจากแพปลาหัวหินทุกเช้า ผักส่วนหนึ่งปลูกเองหลังครัว เราแยกขยะและงดขวดพลาสติกในห้องพักตั้งแต่ปี 2565 โดยเปลี่ยนเป็นขวดแก้วที่เติมน้ำได้ที่จุดเติมทุกชั้น'],
      stat: [['ปีที่เปิด', '2560'], ['จำนวนห้อง', '24'], ['พนักงาน', '20 คน'], ['ความยาวหาด', '200 ม.']] },
    faq: [
      { q: 'ยกเลิกการจองได้ถึงเมื่อไหร่', a: 'ยกเลิกฟรีเต็มจำนวนถ้าแจ้งก่อนเช็คอิน 7 วันขึ้นไป แจ้งภายใน 3–6 วันคืนให้ 50% น้อยกว่า 3 วันไม่คืนเงิน แต่เลื่อนวันได้ 1 ครั้งภายใน 6 เดือน' },
      { q: 'เด็กพักฟรีถึงกี่ขวบ', a: 'เด็กไม่เกิน 11 ปี พักฟรี 2 คนต่อห้องโดยใช้เตียงร่วมกับผู้ใหญ่ เตียงเสริมคืนละ 600 บาทรวมอาหารเช้า เตียงเด็กอ่อนยืมฟรี' },
      { q: 'นำสัตว์เลี้ยงเข้าพักได้ไหม', a: 'รับสุนัขและแมวไม่เกิน 15 กก. เฉพาะ Garden Room และ Beachfront Villa ค่าทำความสะอาดคืนละ 500 บาท ต้องมีสายจูงในพื้นที่ส่วนกลาง' },
      { q: 'เช็คอินเช็คเอาท์กี่โมง', a: 'เช็คอิน 14:00 เช็คเอาท์ 12:00 มาก่อนเวลาฝากกระเป๋าและใช้สระกับหาดได้ ถ้าห้องว่างเราให้เข้าก่อนโดยไม่คิดเพิ่ม เช็คเอาท์สายถึง 15:00 คิด 400 บาท' },
      { q: 'จ่ายเงินได้ช่องทางไหน', a: 'โอนพร้อมเพย์หรือบัญชีธนาคาร มัดจำ 50% ตอนจอง ที่เหลือจ่ายวันเช็คอิน รับบัตรเครดิตที่หน้ารีสอร์ต ออกใบกำกับภาษีได้' },
      { q: 'ทำไมราคาแต่ละวันไม่เท่ากัน', a: 'ราคาคิดตามฤดูกาลและวันในสัปดาห์ ช่วงพฤศจิกายนถึงกุมภาพันธ์เป็นไฮซีซัน ราคาสูงกว่าปกติ ส่วนมิถุนายนถึงกันยายนเป็นกรีนซีซัน ราคาถูกลง คืนวันศุกร์และเสาร์บวกเพิ่มจากวันธรรมดา ทุกราคาที่แสดงรวมภาษีและค่าบริการแล้ว' },
      { q: 'มีขั้นต่ำการเข้าพักไหม', a: 'วันธรรมดาพักคืนเดียวได้ คืนวันศุกร์และเสาร์ขั้นต่ำ 2 คืน ช่วงปีใหม่และสงกรานต์ขั้นต่ำ 3 คืน ระบบจะแจ้งให้ทราบตอนเลือกวัน' },
      { q: 'ห้องเต็มช่วงที่อยากไป ทำยังไงได้บ้าง', a: 'ทักไลน์มาแจ้งช่วงวันที่ต้องการ เราจะบันทึกไว้และแจ้งกลับทันทีถ้ามีคนยกเลิก ช่วงวันหยุดยาวมักมีที่ว่างคืนก่อนเข้าพักประมาณหนึ่งสัปดาห์' }
    ],
    policy: { title: 'นโยบายที่พัก',
      cancelHead: ['แจ้งล่วงหน้า', 'คืนเงิน'],
      cancel: [['7 วันขึ้นไป', '100%'], ['3–6 วัน', '50%'], ['น้อยกว่า 3 วัน', 'ไม่คืนเงิน (เลื่อนได้ 1 ครั้ง)']],
      blocks: [
        { h: 'เด็กและเตียงเสริม', p: 'เด็กไม่เกิน 11 ปี พักฟรี 2 คนต่อห้องเมื่อใช้เตียงร่วมกับผู้ใหญ่ เตียงเสริมคืนละ 600 บาทรวมอาหารเช้า เตียงเด็กอ่อนยืมฟรีแต่มีจำนวนจำกัด' },
        { h: 'สัตว์เลี้ยง', p: 'รับสุนัขและแมวไม่เกิน 15 กิโลกรัม เฉพาะ Garden Room และ Beachfront Villa ค่าทำความสะอาดคืนละ 500 บาท ต้องใส่สายจูงในพื้นที่ส่วนกลางตลอดเวลา' },
        { h: 'การชำระเงิน', p: 'มัดจำ 50% ภายใน 24 ชั่วโมงหลังจอง ส่วนที่เหลือชำระวันเช็คอิน รับโอนพร้อมเพย์ โอนธนาคาร และบัตรเครดิตที่หน้ารีสอร์ต ออกใบกำกับภาษีเต็มรูปแบบได้' },
        { h: 'การสูบบุหรี่', p: 'ทุกห้องเป็นห้องปลอดบุหรี่ มีจุดสูบบุหรี่ที่ลานหลังห้องอาหาร ฝ่าฝืนมีค่าทำความสะอาด 2,000 บาท' }
      ] },
    contact: { addr: '129/4 ซอยหัวหิน 67 ถนนเพชรเกษม ต.หนองแก อ.หัวหิน ประจวบคีรีขันธ์ 77110',
      phone: 'โทร 032 000 000', line: 'ทักไลน์ OA', maps: 'นำทาง Google Maps',
      hours: 'แผนกต้อนรับรับสายทุกวัน 08:00–20:00 น.',
      mapNote: 'แผนผังโดยประมาณ กดปุ่มด้านล่างเพื่อเปิดแผนที่จริง', pin: 'บ้านทะเล หัวหิน',
      routesHead: 'การเดินทาง',
      routes: [['จากกรุงเทพฯ โดยรถยนต์', '2 ชม. 30 นาที'], ['สนามบินหัวหิน', '15 นาที'], ['สถานีรถไฟหัวหิน', '20 นาที'], ['ตลาดซิเคด้า', '8 นาที']] },
    book: { summary: 'สรุปก่อนจอง', checkIn: 'เช็คอิน', checkOut: 'เช็คเอาท์', nights: 'จำนวนคืน',
      guests: 'ผู้เข้าพัก', notPicked: 'ยังไม่เลือก', roomTotal: 'ค่าห้อง {n} คืน', extraGuest: 'ผู้เข้าพักเพิ่ม {n} คน',
      service: 'ค่าบริการ 10%', promoOff: 'ส่วนลด {code}', payToday: 'ยอดชำระวันนี้ (มัดจำ 50%)',
      totalNote: 'ยอดรวมทั้งหมด {t} ส่วนที่เหลือชำระวันเช็คอิน', name: 'ชื่อผู้จอง', namePh: 'ชื่อ–นามสกุล',
      phone: 'เบอร์โทร', phonePh: '08X-XXX-XXXX', confirm: 'ยืนยันการจอง',
      confirmNote: 'กดยืนยันแล้วจะได้เลขการจองทันที เจ้าหน้าที่ส่งช่องทางโอนให้ทางไลน์ภายใน 15 นาที',
      promo: 'รหัสส่วนลด', promoPh: 'ใส่รหัส', apply: 'ใช้รหัส',
      promoOk: 'ใช้รหัส {code} แล้ว ลด {n}%', promoBadCode: 'ไม่พบรหัสนี้',
      promoTooLate: 'รหัส {code} ต้องจองล่วงหน้าอย่างน้อย 30 วัน',
      okTitle: 'จองสำเร็จแล้ว', okLede: 'เราส่งรายละเอียดไปที่เบอร์ {p} เรียบร้อย', ref: 'เลขการจอง',
      okRoom: 'ห้อง', okDates: 'วันที่', okName: 'ผู้จอง', okDeposit: 'มัดจำที่ต้องโอน',
      sendSlip: 'ส่งสลิปทางไลน์ OA', backHome: 'กลับหน้าแรก',
      okNote: 'โอนมัดจำภายใน 24 ชม. เพื่อยืนยันห้อง ยกเลิกฟรีก่อนเช็คอิน 7 วัน',
      perNight: 'ราคารายคืน', weekend: 'ศุกร์–เสาร์', peak: 'ช่วงเทศกาล' },
    foot: { addr: 'ที่อยู่', contact: 'ติดต่อ', hours: 'เวลา', explore: 'เมนู',
      time: 'เช็คอิน 14:00 · เช็คเอาท์ 12:00', callHours: 'รับสายทุกวัน 08:00–20:00',
      company: 'บริษัท บ้านทะเล หัวหิน จำกัด (ตัวอย่าง)',
      legal: 'เลขประจำตัวผู้เสียภาษี 0-0000-00000-00-0 (สมมติ) · ใบอนุญาตประกอบธุรกิจโรงแรมเลขที่ 00/2560 (สมมติ)',
      disclosure: 'หน้านี้เป็นงานออกแบบตัวอย่าง ไม่ใช่เว็บของที่พักจริง · ไม่มีการรับจองจริง ไม่มีการเก็บหรือส่งข้อมูลใดออกจากเบราว์เซอร์ · ชื่อบริษัท เลขผู้เสียภาษี เลขใบอนุญาต รีวิวและคะแนนทั้งหมดเป็นข้อมูลสมมติที่สร้างขึ้นเพื่อสาธิตหน้าตาเว็บเท่านั้น' }
  };

  L.en = {
    code: 'en', other: 'TH',
    nav: { rooms: 'Rooms', dining: 'Dining', facilities: 'Facilities', offers: 'Offers',
      reviews: 'Reviews', about: 'About', gallery: 'Gallery', faq: 'FAQ',
      contact: 'Contact & getting here', book: 'Check availability', menu: 'Menu', close: 'Close', home: 'Home', skip: 'Skip to content' },
    c: { from: 'from', perNight: '/ night', night: 'nights', guest: 'guests', baht: '฿',
      inclTax: 'tax and service included', back: 'Back', viewAll: 'View all', more: 'Details',
      soldOut: 'Sold out', left: 'Only {n} left', selected: 'Selected' },
    hero: { badge: '24 ROOMS · PRIVATE BEACH', title: 'The sea, still quiet',
      lede: 'A 24-room resort on its own beach in Hua Hin. No party noise, no queues.' },
    search: { in: 'Check in', out: 'Check out', guests: 'Guests', go: 'Search availability',
      nights: '{n} nights · {g} guests', pickOut: 'Now pick your check-out date',
      strip: 'Nightly rates, next 14 days', stripNote: 'Rates change with the season and the day of the week',
      minStay: 'These dates require a {n}-night minimum stay', noRooms: 'Every room is taken on those dates. Try shifting them by a day.' },
    feats: ['200m of private beach', 'Breakfast cooked to order', 'Two pools, one for children', '8 minutes to the night market'],
    sec: {
      rooms: 'Four kinds of room', roomsLede: 'Rates are calculated for the dates you picked, tax and service included',
      dining: 'Restaurant and bar', diningLede: 'The kitchen opens daily. Seafood comes off the Hua Hin pier each morning.',
      facs: 'Facilities', facsLede: 'Everything is on site, none of it more than two minutes’ walk away',
      offers: 'Offers', offersLede: 'Booking direct is always cheaper. No agency fee.',
      reviews: 'Guest reviews', reviewsLede: 'Every review comes from a guest whose stay we could verify',
      gallery: 'Gallery', about: 'About Baan Talay', contact: 'Contact & getting here',
      faq: 'Frequently asked', policy: 'House policies', location: 'Location'
    },
    teaser: [
      { t: 'Rooms', s: 'Four types, from ฿2,400' },
      { t: 'Dining', s: 'Seafood by the sand' },
      { t: 'Spa & pools', s: 'Open until 8pm' }
    ],
    rooms: [
      { name: 'Garden Room', bed: 'Queen',
        blurb: 'Ground floor, opens onto the garden, 90m from the sand',
        detail: 'A ground-floor room that opens straight onto the garden, ninety metres from the sand. It sits in the back wing, which makes it the quietest room we have — the right choice for one or two people who came to read. Separate wet and dry bathroom, and a balcony that seats two.',
        amen: ['Air conditioning', 'Free Wi-Fi', 'Mini fridge', 'Garden balcony'] },
      { name: 'Sea Breeze', bed: 'King',
        blurb: 'Second floor, sea view through the pines',
        detail: 'On the second floor, with the sea visible through a line of pines. At night you hear the surf just enough, never enough to keep you awake. The bathroom has a tub and a window that actually opens. A 180cm king bed, a coffee maker, and tea from a plantation in the province.',
        amen: ['Partial sea view', 'Bathtub', 'Free Wi-Fi', 'Coffee maker'] },
      { name: 'Beachfront Villa', bed: 'King + sofa bed',
        blurb: 'A detached villa on the sand — open the door and you are on the beach',
        detail: 'A detached villa right on the beach: open the door and you are on the sand. It has a private timber deck facing the water, and breakfast can be served out there by arrangement. There are only four of them, which is why they are the first thing to go over a long weekend.',
        amen: ['Directly on the beach', 'Private deck', 'Bathtub', 'Extra sofa bed'] },
      { name: 'Family Suite', bed: 'King + 2 singles',
        blurb: 'Two bedrooms behind their own doors, steps from the children’s pool',
        detail: 'Two bedrooms behind their own doors, twenty paces from the children’s pool. There is a dining table in the room and a small kitchen for reheating. Cots are free to borrow, and we keep stair gates for families with small children.',
        amen: ['2 bedrooms', 'Small kitchen', 'Washing machine', 'Child bath'] }
    ],
    roomUI: { size: 'Size', cap: 'Sleeps', bed: 'Bed', sqm: 'sqm', amen: 'In the room',
      shots: 'This room', bookThis: 'Book this room', rate: 'Per night',
      note: 'Free cancellation up to 7 days before arrival · Check in 14:00, check out 12:00',
      sideNote: 'Free cancellation up to 7 days before arrival. 50% deposit on booking.', bfIncl: 'Breakfast included' },
    dining: [
      { name: 'Baan Talay Kitchen', hours: 'Open 06:30–22:00 daily',
        body: 'The main restaurant sits on the beach and runs from breakfast through dinner. Fish and prawns come off the Hua Hin pier every morning, so the menu follows the catch. The kitchen cooks vegetarian and gluten-free with a day’s notice.',
        menu: [['Steamed sea bass with lime', '฿380'], ['Grilled river prawns (500g)', '฿520'], ['Sour curry with prawns', '฿260'], ['Fried rice with crab', '฿220']] },
      { name: 'Poolside Bar', hours: 'Open 15:00–23:00 daily',
        body: 'A small bar beside the main pool serving cocktails and something to pick at until eleven. At sunset you can reserve a table on the sand at reception — no fee, no minimum spend.',
        menu: [['Coconut rum blend', '฿220'], ['Mango and soda', '฿180'], ['Seaweed fries', '฿150'], ['Mango salad with dried shrimp', '฿190']] }
    ],
    facs: [
      { name: 'Main pool', body: '20m long, 1.2–1.5m deep, with loungers and umbrellas free to use', hours: '07:00–20:00' },
      { name: 'Private beach', body: '200m of beach in front of the resort, with loungers, towels and kayaks to borrow', hours: 'All day' },
      { name: 'Spa', body: 'Two treatment rooms for Thai and oil massage. Book at reception two hours ahead.', hours: '10:00–20:00' },
      { name: 'Gym', body: 'A small gym with two treadmills, a bike and dumbbells. Your room key opens it.', hours: '06:00–22:00' },
      { name: 'Children’s pool and play corner', body: '40cm deep and separate from the main pool, with toys and picture books to borrow', hours: '08:00–18:00' },
      { name: 'Parking and transfers', body: 'Free parking on site for 20 cars. Station transfers with a day’s notice.', hours: 'All day' }
    ],
    offers: [
      { name: 'Book 30 days ahead', save: '15% off', tag: 'Best value',
        body: 'Book at least thirty days before you arrive and the discount comes off at checkout. Valid on every room, in every season.',
        terms: ['Must be booked at least 30 days ahead', 'Cannot be combined with other offers', 'Normal cancellation policy applies'] },
      { name: 'Stay 3, pay 2', save: 'One night free',
        body: 'Stay three consecutive nights and the third room charge is waived. It suits midweek, which is when the resort is at its quietest.',
        terms: ['Sunday to Thursday arrivals only', 'Excludes public holidays', 'The discount applies to the cheapest night'] },
      { name: 'Honeymoon', save: 'A gift in the room',
        body: 'For couples who tell us the occasion when booking: flowers, fruit, and breakfast served on your deck once during the stay.',
        terms: ['Tell us at least 3 days ahead', 'Sea Breeze and Beachfront Villa only', 'No extra charge'] }
    ],
    reviewUI: { of5: 'out of 5', count: '{n} reviews', stayed: 'Stayed in', verified: 'Verified stay',
      replyBy: 'Reply from Baan Talay', trip: { couple: 'Couple', family: 'Family', solo: 'Solo', friends: 'Friends' },
      bars: { clean: 'Cleanliness', location: 'Location', service: 'Service', food: 'Food', value: 'Value' } },
    reviews: [
      { name: 'Nattapong S.', body: 'The villa really is on the beach — you open the door and you are on the sand. Very quiet at night, just the surf. Breakfast arrived on the deck at the time we agreed, every morning.' },
      { name: 'Sarah W.', body: 'Very comfortable bed and a genuinely clean bathroom. I liked that the bathroom has a window, so there is always air moving. Staff speak English and arranged a car to the night market for us.' },
      { name: 'Phimchanok R.', body: 'Came with two children. The Family Suite is genuinely big enough and the children’s pool is close enough that they can walk there. One thing: the small kitchen has no real hob, only reheating. Had I known I would have packed differently.',
        reply: 'Thank you for putting that plainly. The room has a microwave and a kettle but no hob, and we have now added that to the room page. If you ever need something properly reheated, the kitchen will do it at any time, at no charge.' },
      { name: 'Marco B.', body: 'Sea Breeze looks out at the water through the pines — not a full view, but a lovely one, and the breeze is constant. Very good value against anything else on this stretch.' },
      { name: 'Orathai K.', body: 'The garden room is as quiet as they say, but there was pool maintenance during the day while we were there and it was loud for two days. Nobody mentioned it when we booked. Everything else was good and the staff were lovely.',
        reply: 'We owe you an apology. That maintenance was posted at reception but not sent out with booking confirmations. We now message guests on LINE before any works, and we refunded the difference to everyone staying that week.' },
      { name: 'Kittipong W.', body: 'Brought my parents. The suite is easy to get around with no real stairs, and breakfast is cooked to order — eggs however you want them. The staff knew our names by the second day.' },
      { name: 'Julia P.', body: 'Quiet and clean, right for people who actually want to rest rather than party. Wi-Fi is fast enough to work on. Only note: the bar shuts at eleven, and I would have liked it a little later.' },
      { name: 'Thanakorn A.', body: 'Booking direct came out about 700 baht cheaper than the agency for the same room. The booking took a minute and the reference came through immediately.' },
      { name: 'Wanna T.', body: 'Three nights on my own and I finished two books. Nothing disturbed me at all, and I liked that nobody walks the beach selling things.' },
      { name: 'Andreas K.', body: 'The family room is very good value for four. The extra bed was more comfortable than expected, and the children’s pool is shallow enough that you can let them play without standing over them.' }
    ],
    about: { title: 'About Baan Talay',
      p: ['Baan Talay opened in 2017, in what had been the family’s holiday house on land my grandfather bought. We deliberately never grew past 24 rooms, because 24 is the number twenty staff can actually look after properly — not a number that came out of a return calculation.',
        'We do not host functions and we do not play music in the public areas after nine, because most people who choose this place choose it for the quiet. If you are looking for somewhere with activities all day, we are probably not it, and it is better that we say so now.',
        'All the seafood comes off the Hua Hin pier each morning, and some of the vegetables are grown behind the kitchen. We have separated waste and kept plastic bottles out of the rooms since 2022, replacing them with glass you refill at stations on every floor.'],
      stat: [['Opened', '2017'], ['Rooms', '24'], ['Staff', '20'], ['Beach', '200m']] },
    faq: [
      { q: 'How late can I cancel?', a: 'Free cancellation with a full refund if you tell us 7 or more days before arrival. Within 3–6 days we refund 50%. Under 3 days is non-refundable, but you may move the dates once within 6 months.' },
      { q: 'Up to what age do children stay free?', a: 'Two children up to 11 stay free per room when sharing an adult bed. An extra bed is 600 baht a night including breakfast, and cots are free to borrow.' },
      { q: 'Can I bring a pet?', a: 'Dogs and cats up to 15kg, in Garden Room and Beachfront Villa only. Cleaning is 500 baht a night and pets must be leashed in the public areas.' },
      { q: 'What are the check-in and check-out times?', a: 'Check in 14:00, check out 12:00. Arrive early and you can leave bags and use the pool and the beach. If the room is ready we let you in early at no charge. Late check-out to 15:00 is 400 baht.' },
      { q: 'How can I pay?', a: 'PromptPay or bank transfer, 50% deposit on booking and the balance on arrival. We take credit cards at the resort and can issue a full tax invoice.' },
      { q: 'Why does the price change from day to day?', a: 'Rates follow the season and the day of the week. November to February is high season and costs more; June to September is green season and costs less. Friday and Saturday nights carry a supplement. Every rate shown includes tax and service.' },
      { q: 'Is there a minimum stay?', a: 'One night is fine midweek. Friday and Saturday nights carry a two-night minimum, and New Year and Songkran a three-night minimum. The booking form tells you when this applies.' },
      { q: 'You are full on the dates I want — what now?', a: 'Message us on LINE with the dates and we will note them and come back to you the moment someone cancels. Over long weekends something usually frees up about a week out.' }
    ],
    policy: { title: 'House policies',
      cancelHead: ['Notice given', 'Refund'],
      cancel: [['7 days or more', '100%'], ['3–6 days', '50%'], ['Under 3 days', 'None (one free date change)']],
      blocks: [
        { h: 'Children and extra beds', p: 'Two children up to 11 stay free per room when sharing an adult bed. An extra bed is 600 baht a night including breakfast. Cots are free to borrow but limited in number.' },
        { h: 'Pets', p: 'Dogs and cats up to 15kg, in Garden Room and Beachfront Villa only. Cleaning is 500 baht a night, and pets must be on a lead in the public areas at all times.' },
        { h: 'Payment', p: '50% deposit within 24 hours of booking, the balance on arrival. We accept PromptPay, bank transfer, and credit cards at the resort, and can issue a full tax invoice.' },
        { h: 'Smoking', p: 'Every room is non-smoking. There is a smoking area on the terrace behind the restaurant. Smoking in a room carries a 2,000 baht cleaning charge.' }
      ] },
    contact: { addr: '129/4 Soi Hua Hin 67, Phetkasem Road, Nong Kae, Hua Hin, Prachuap Khiri Khan 77110',
      phone: 'Call 032 000 000', line: 'Message us on LINE', maps: 'Open in Google Maps',
      hours: 'Reception answers daily, 08:00–20:00',
      mapNote: 'Approximate layout. Use the button below for the real map.', pin: 'Baan Talay, Hua Hin',
      routesHead: 'Getting here',
      routes: [['From Bangkok by car', '2h 30m'], ['Hua Hin airport', '15 min'], ['Hua Hin railway station', '20 min'], ['Cicada Market', '8 min']] },
    book: { summary: 'Review your stay', checkIn: 'Check in', checkOut: 'Check out', nights: 'Nights',
      guests: 'Guests', notPicked: 'Not selected', roomTotal: 'Room, {n} nights', extraGuest: 'Extra guests ({n})',
      service: 'Service charge 10%', promoOff: '{code} discount', payToday: 'Due today (50% deposit)',
      totalNote: 'Total {t}. The balance is due on arrival.', name: 'Name', namePh: 'Full name',
      phone: 'Phone', phonePh: '08X-XXX-XXXX', confirm: 'Confirm booking',
      confirmNote: 'You get a reference immediately. Reception sends transfer details on LINE within 15 minutes.',
      promo: 'Promo code', promoPh: 'Enter code', apply: 'Apply',
      promoOk: '{code} applied — {n}% off', promoBadCode: 'That code was not recognised',
      promoTooLate: '{code} requires booking at least 30 days ahead',
      okTitle: 'You are booked', okLede: 'We have sent the details to {p}', ref: 'Booking reference',
      okRoom: 'Room', okDates: 'Dates', okName: 'Guest', okDeposit: 'Deposit due',
      sendSlip: 'Send the slip on LINE', backHome: 'Back to home',
      okNote: 'Transfer the deposit within 24 hours to hold the room. Free cancellation up to 7 days before arrival.',
      perNight: 'Night by night', weekend: 'Fri–Sat', peak: 'Peak' },
    foot: { addr: 'Address', contact: 'Contact', hours: 'Hours', explore: 'Explore',
      time: 'Check in 14:00 · Check out 12:00', callHours: 'Daily 08:00–20:00',
      company: 'Baan Talay Hua Hin Co., Ltd. (fictional)',
      legal: 'Tax ID 0-0000-00000-00-0 (fictional) · Hotel licence 00/2560 (fictional)',
      disclosure: 'This page is a design demo, not a real property’s website. No booking is taken, and nothing you type leaves your browser. The company name, tax ID, licence number, reviews and ratings are all invented to demonstrate how the page looks.' }
  };

  /* ── state ───────────────────────────────────────────────── */
  var S = { view: 'home', sel: 2, ci: '', co: '', guests: 2, promo: '', promoMsg: null, lb: -1, ref: '', lang: 'th' };
  var T = L.th;

  var $ = function (id) { return document.getElementById(id); };
  function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }
  function money(n) { return '฿' + Math.round(n).toLocaleString('en-US'); }
  function tpl(s, o) { return String(s).replace(/\{(\w+)\}/g, function (_, k) { return o[k] != null ? o[k] : ''; }); }

  var TH_M = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'];
  var EN_M = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  function fmtDate(isoStr) {
    if (!isoStr) return T.book.notPicked;
    var d = new Date(isoStr + 'T00:00');
    return S.lang === 'th'
      ? d.getDate() + ' ' + TH_M[d.getMonth()] + ' ' + String(d.getFullYear() + 543).slice(2)
      : d.getDate() + ' ' + EN_M[d.getMonth()] + ' ' + d.getFullYear();
  }
  function dowShort(isoStr) {
    var d = new Date(isoStr + 'T00:00');
    return (S.lang === 'th' ? ['อา', 'จ', 'อ', 'พ', 'พฤ', 'ศ', 'ส'] : ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'])[d.getDay()];
  }

  function pic(name, alt, cls, sizes, eager) {
    var big = name === 'beach-morning' ? '-1800' : '-1200';
    var small = (name.indexOf('room-') === 0) ? '-640' : (name === 'beach-morning' ? '-900' : '-600');
    return '<img class="' + (cls || '') + '" src="' + IMG + name + small + '.webp"' +
      ' srcset="' + IMG + name + small + '.webp 640w, ' + IMG + name + big + '.webp 1400w"' +
      ' sizes="' + (sizes || '100vw') + '" width="1200" height="800"' +
      (eager ? ' fetchpriority="high"' : ' loading="lazy"') + ' alt="' + esc(alt) + '">';
  }
  function svgIcon(d, size, stroke, sw) {
    return '<svg width="' + size + '" height="' + size + '" viewBox="0 0 24 24" fill="none" stroke="' + stroke +
      '" stroke-width="' + (sw || 1.6) + '" stroke-linecap="round" aria-hidden="true"><path d="' + d + '"></path></svg>';
  }
  function stars(n) {
    var out = '<span class="bt-stars" aria-hidden="true">';
    for (var i = 1; i <= 5; i++) {
      out += '<svg viewBox="0 0 24 24" fill="' + (i <= n ? '#C9922F' : 'none') + '" stroke="#C9922F" stroke-width="1.5">' +
        '<path d="M12 3l2.7 5.5 6 .9-4.3 4.2 1 6-5.4-2.8-5.4 2.8 1-6L3.3 9.4l6-.9z"/></svg>';
    }
    return out + '</span>';
  }
  function crumb(label) {
    return '<nav class="bt-crumb" aria-label="breadcrumb"><a href="#/" data-go="home">' + esc(T.nav.home) + '</a>' +
      svgIcon('M9 5l7 7-7 7', 13, 'currentColor', 1.8) + '<span aria-current="page">' + esc(label) + '</span></nav>';
  }

  /* ── quote ───────────────────────────────────────────────── */
  function quote() {
    var i = S.sel, hasDates = !!(S.ci && S.co);
    var info = hasDates ? stay(i, S.ci, S.co) : null;
    var nights = info ? info.nights : 2;
    var roomSum = info ? info.sum : rateFor(i, iso(new Date())) * 2;
    var extra = Math.max(0, S.guests - 2) * 600 * nights;
    var off = 0, code = '';
    if (S.promo === 'EARLYBIRD' && hasDates && daysUntil(S.ci) >= 30) { off = Math.round((roomSum + extra) * 0.15); code = 'EARLYBIRD'; }
    var service = Math.round((roomSum + extra - off) * 0.10);
    var total = roomSum + extra - off + service;
    return { info: info, hasDates: hasDates, nights: nights, roomSum: roomSum, extra: extra,
      off: off, code: code, service: service, total: total, deposit: Math.round(total / 2) };
  }

  /* ── shared fragments ────────────────────────────────────── */
  function roomCard(i, clickable) {
    var r = ROOMS[i], c = T.rooms[i];
    var q = S.ci && S.co ? stay(i, S.ci, S.co) : null;
    var out = q && q.left === 0;
    var rate = q ? Math.round(q.sum / q.nights) : rateFor(i, iso(new Date()));
    var low = q && q.left > 0 && q.left <= 2;
    return '<button type="button" class="bt-room' + (out ? ' is-out' : '') + '"' +
      (out ? ' disabled aria-disabled="true"' : ' data-room="' + i + '"') + '>' +
      '<span class="bt-room-fig">' +
        pic(r.slug, c.name, '', '(min-width:900px) 540px, 92vw') +
        (r.bf && !out ? '<span class="bt-pill-bf">' + esc(T.roomUI.bfIncl) + '</span>' : '') +
        (out ? '<span class="bt-pill-out">' + esc(T.c.soldOut) + '</span>' : '') +
      '</span>' +
      '<span class="bt-room-body">' +
        '<span class="bt-room-top"><span class="bt-room-name">' + esc(c.name) + '</span>' +
        '<span class="bt-room-price">' + (q ? '' : '<span class="bt-from">' + esc(T.c.from) + ' </span>') + money(rate) + '</span></span>' +
        '<span class="bt-room-blurb">' + esc(c.blurb) + '</span>' +
        '<span class="bt-room-meta"><span>' + r.size + ' ' + esc(T.roomUI.sqm) + '</span><span>' + r.cap + ' ' + esc(T.c.guest) + '</span><span>' + esc(c.bed) + '</span></span>' +
        (low ? '<span class="bt-left">' + tpl(T.c.left, { n: q.left }) + '</span>' : '') +
      '</span></button>';
  }

  function rateStrip() {
    var start = S.ci || iso(new Date()), out = '';
    for (var k = 0; k < 14; k++) {
      var d = addDays(start, k), inv = invFor(S.sel, d), r = rateFor(S.sel, d);
      out += '<div class="bt-day' + (inv === 0 ? ' is-out' : '') + (isPeak(d) ? ' is-peak' : '') + (d === S.ci ? ' is-sel' : '') + '">' +
        '<div class="d">' + dowShort(d) + '</div><div class="n">' + new Date(d + 'T00:00').getDate() + '</div>' +
        '<div class="p">' + (inv === 0 ? esc(T.c.soldOut) : money(r)) + '</div></div>';
    }
    return '<div class="bt-strip-wrap"><p class="bt-sub"><strong>' + esc(T.search.strip) + '</strong> — ' + esc(T.search.stripNote) + '</p>' +
      '<div class="bt-strip">' + out + '</div></div>';
  }

  function searchCard() {
    var q = quote(), warn = '';
    if (q.hasDates && q.info) {
      if (q.nights < q.info.minStay) warn = tpl(T.search.minStay, { n: q.info.minStay });
      else {
        var any = ROOMS.some(function (_, i) { return stay(i, S.ci, S.co).left > 0; });
        if (!any) warn = T.search.noRooms;
      }
    }
    var note = warn ? warn : (q.hasDates ? tpl(T.search.nights, { n: q.nights, g: S.guests })
      : (S.ci ? T.search.pickOut : ''));
    return '<div class="bt-search"><div class="bt-search-in">' +
      '<div class="bt-dates">' +
        '<label class="bt-field"><span>' + esc(T.search.in) + '</span><input class="bt-input" type="date" id="in" value="' + S.ci + '"></label>' +
        '<label class="bt-field"><span>' + esc(T.search.out) + '</span><input class="bt-input" type="date" id="out" value="' + S.co + '"></label>' +
      '</div>' +
      '<div class="bt-guests"><span id="g-label">' + esc(T.search.guests) + '</span>' +
        '<div class="bt-stepper">' +
          '<button type="button" class="bt-icon" id="g-dec" aria-label="-1">' + svgIcon('M5 12h14', 16, 'currentColor', 2.2) + '</button>' +
          '<span class="bt-count" id="g-count" aria-live="polite" aria-labelledby="g-label">' + S.guests + ' ' + esc(T.c.guest) + '</span>' +
          '<button type="button" class="bt-icon" id="g-inc" aria-label="+1">' + svgIcon('M12 5v14M5 12h14', 16, 'currentColor', 2.2) + '</button>' +
        '</div></div>' +
      '<button type="button" class="bt-btn bt-btn--primary bt-go" data-go="rooms">' + esc(T.search.go) + '</button>' +
      '<p class="bt-nights" id="nights" aria-live="polite">' + esc(note) + '</p>' +
    '</div></div>';
  }

  /* ── section header helper ───────────────────────────────── */
  function head(title, lede, linkTo, linkLabel) {
    return '<div class="bt-sec-head"><div><h2 class="bt-h2">' + esc(title) + '</h2>' +
      (lede ? '<p class="bt-sub">' + esc(lede) + '</p>' : '') + '</div>' +
      (linkTo ? '<button type="button" class="bt-more" data-go="' + linkTo + '">' + esc(linkLabel || T.c.viewAll) + '</button>' : '') +
      '</div>';
  }
  function scoreBlock(compact) {
    var bars = SCORE.bars.map(function (b) {
      return '<div class="bt-bar"><span>' + esc(T.reviewUI.bars[b[0]]) + '</span>' +
        '<span class="track"><span class="fill" style="width:' + (b[1] / 5 * 100).toFixed(0) + '%"></span></span>' +
        '<span class="num">' + b[1].toFixed(1) + '</span></div>';
    }).join('');
    return '<div class="bt-score"><div class="bt-score-big"><b>' + SCORE.avg.toFixed(1) + '</b><span>' + esc(T.reviewUI.of5) + '</span></div>' +
      '<div>' + stars(Math.round(SCORE.avg)) + '<div class="bt-sub" style="margin-top:4px">' + tpl(T.reviewUI.count, { n: SCORE.count }) + '</div></div></div>' +
      (compact ? '' : '<div class="bt-bars">' + bars + '</div>');
  }
  function reviewCard(idx) {
    var r = REVIEWS[idx], c = T.reviews[idx];
    var d = new Date(r.month + '-01T00:00');
    var when = (S.lang === 'th' ? TH_M[d.getMonth()] + ' ' + String(d.getFullYear() + 543).slice(2)
      : EN_M[d.getMonth()] + ' ' + d.getFullYear());
    return '<article class="bt-review"><div class="bt-review-top"><div class="bt-review-who">' +
      /* initial comes from the localised name, not the data — otherwise the
         English page shows a Thai glyph beside a romanised name */
      '<span class="bt-avatar" aria-hidden="true">' + esc(c.name.trim().charAt(0)) + '</span>' +
      '<div><div class="bt-review-name">' + esc(c.name) + '</div>' +
      '<div class="bt-review-meta">' + when + ' · ' + esc(T.reviewUI.trip[r.trip]) + ' · ' + esc(T.reviewUI.stayed) + ' ' + esc(T.rooms[r.room].name) +
      (r.verified ? '<span class="bt-verified">' + svgIcon('M20 6L9 17l-5-5', 12, 'currentColor', 2.4) + esc(T.reviewUI.verified) + '</span>' : '') +
      '</div></div></div>' + stars(r.score) + '</div>' +
      '<p class="bt-review-body">' + esc(c.body) + '</p>' +
      (r.reply && c.reply ? '<div class="bt-reply"><b>' + esc(T.reviewUI.replyBy) + '</b><p>' + esc(c.reply) + '</p></div>' : '') +
      '</article>';
  }
  function mapPanel() {
    return '<div class="bt-map"><div class="bt-map-sea"></div>' +
      '<div class="bt-map-pin">' + svgIcon('M12 21s7-6.3 7-11a7 7 0 1 0-14 0c0 4.7 7 11 7 11z', 26, 'var(--terra)', 2) +
      '<span>' + esc(T.contact.pin) + '</span></div>' +
      '<span class="bt-map-note">' + esc(T.contact.mapNote) + '</span></div>';
  }

  /* ── views ───────────────────────────────────────────────── */
  var V = {};

  V.home = function () {
    var teaserImgs = ['room-villa', 'dining-room', 'spa-treatment'];
    var teaserGo = ['rooms', 'dining', 'facilities'];
    return '<section class="bt-view">' +
      '<div class="bt-hero">' + pic('beach-morning', T.hero.lede, '', '100vw', true) +
        '<div class="bt-hero-ov"></div>' +
        '<div class="bt-hero-nav"><div class="bt-wrap">' +
          '<span class="bt-logo"><b>BAAN TALAY</b><span>' + (S.lang === 'th' ? 'หัวหิน · ริมทะเล' : 'HUA HIN · BEACHFRONT') + '</span></span>' +
          '<button type="button" class="bt-icon bt-burger" id="burger" aria-expanded="false" aria-controls="drawer" aria-label="' + esc(T.nav.menu) + '">' +
          svgIcon('M3 6h18M3 12h18M3 18h18', 20, 'currentColor', 1.8) + '</button>' +
        '</div></div>' +
        '<div class="bt-hero-in"><div class="bt-wrap">' +
          '<span class="bt-badge">' + esc(T.hero.badge) + '</span>' +
          '<h1 class="bt-h1"><span class="nb">' + esc(T.hero.title) + '</span></h1>' +
          '<p class="bt-lede">' + esc(T.hero.lede) + '</p>' +
        '</div></div>' +
      '</div>' +
      searchCard() +
      '<div class="bt-feats">' + T.feats.map(function (f, i) {
        return '<div class="bt-feat">' + svgIcon([IC.beach, IC.coffee, IC.pool, IC.clock][i], 22, '#5B7355', 1.5) +
          '<p>' + esc(f) + '</p></div>';
      }).join('') + '</div>' +
      '<div class="bt-wrap">' +
        '<section class="bt-sec rv">' + head(T.sec.rooms, T.sec.roomsLede, 'rooms') +
          '<div class="bt-rooms">' + [0, 1].map(function (i) { return roomCard(i); }).join('') + '</div>' +
          rateStrip() +
        '</section>' +
        '<section class="bt-sec rv"><div class="bt-teasers">' + teaserImgs.map(function (im, i) {
          return '<button type="button" class="bt-teaser" data-go="' + teaserGo[i] + '">' + pic(im, T.teaser[i].t, '', '33vw') +
            '<span class="bt-teaser-ov"></span><span class="bt-teaser-in"><strong>' + esc(T.teaser[i].t) + '</strong>' +
            '<span>' + esc(T.teaser[i].s) + '</span></span></button>';
        }).join('') + '</div></section>' +
        '<section class="bt-sec rv">' + head(T.sec.reviews, T.sec.reviewsLede, 'reviews') +
          scoreBlock(true) +
          '<div class="bt-reviews">' + [0, 2].map(reviewCard).join('') + '</div>' +
        '</section>' +
        '<section class="bt-sec rv">' + head(T.sec.offers, T.sec.offersLede, 'offers') +
          '<div class="bt-offers">' + T.offers.map(function (o, i) {
            return '<div class="bt-offer' + (OFFERS[i].lead ? ' is-lead' : '') + '">' +
              (o.tag ? '<span class="bt-offer-tag">' + esc(o.tag) + '</span>' : '') +
              '<h3>' + esc(o.name) + '</h3><p class="save">' + esc(o.save) + '</p>' +
              '<p>' + esc(o.body) + '</p>' +
              (OFFERS[i].code ? '<span class="bt-code">' + OFFERS[i].code + '</span>' : '') + '</div>';
          }).join('') + '</div>' +
        '</section>' +
        '<section class="bt-sec rv">' + head(T.sec.location) +
          mapPanel() +
          '<ul class="bt-routes">' + T.contact.routes.map(function (r) {
            return '<li><span class="how">' + esc(r[0]) + '</span><span class="t">' + esc(r[1]) + '</span></li>';
          }).join('') + '</ul>' +
          '<div class="bt-contact" style="margin-top:18px">' +
            '<a class="bt-btn bt-btn--green" href="tel:+66320000000">' + esc(T.contact.phone) + '</a>' +
            '<a class="bt-btn bt-btn--ghost" href="https://maps.google.com/?q=12.5684,99.9577" target="_blank" rel="noopener">' + esc(T.contact.maps) + '</a>' +
          '</div>' +
        '</section>' +
      '</div></section>';
  };

  V.rooms = function () {
    return '<section class="bt-view"><div class="bt-wrap bt-view-pad">' + crumb(T.nav.rooms) +
      '<h1 class="bt-page-title">' + esc(T.sec.rooms) + '</h1>' +
      '<p class="bt-lede-2">' + esc(T.sec.roomsLede) + '</p>' +
      searchCardInline() +
      '<div class="bt-rooms" style="margin-top:22px">' + ROOMS.map(function (_, i) { return roomCard(i); }).join('') + '</div>' +
      rateStrip() +
      '</div></section>';
  };
  function searchCardInline() {
    return '<div style="margin-top:18px">' + searchCard().replace('class="bt-search"', 'class="bt-search" style="margin-top:0;padding:0"') + '</div>';
  }

  V.room = function () {
    var i = S.sel, r = ROOMS[i], c = T.rooms[i], q = quote();
    var st = S.ci && S.co ? stay(i, S.ci, S.co) : null;
    var rate = st ? Math.round(st.sum / st.nights) : rateFor(i, iso(new Date()));
    return '<section class="bt-view"><div class="bt-wrap"><div class="bt-dt">' +
      '<div class="bt-dt-hero">' + pic(r.slug, c.name, '', '(min-width:900px) 650px, 100vw') +
        '<div class="bt-dt-ov"></div>' +
        '<button type="button" class="bt-icon bt-dt-back" data-go="rooms" aria-label="' + esc(T.c.back) + '">' +
        svgIcon('M15 5l-7 7 7 7', 20, 'currentColor', 2) + '</button></div>' +
      '<div class="bt-dt-main">' + crumb(c.name) +
        '<h1 class="bt-dt-title">' + esc(c.name) + '</h1>' +
        '<p class="bt-dt-price"><b>' + money(rate) + '</b><span>' + esc(T.c.perNight) + ' · ' + esc(T.c.inclTax) + '</span></p>' +
        '<p class="bt-dt-copy">' + esc(c.detail) + '</p>' +
        '<dl class="bt-facts"><div><dt>' + esc(T.roomUI.size) + '</dt><dd>' + r.size + ' ' + esc(T.roomUI.sqm) + '</dd></div>' +
        '<div><dt>' + esc(T.roomUI.cap) + '</dt><dd>' + r.cap + ' ' + esc(T.c.guest) + '</dd></div>' +
        '<div><dt>' + esc(T.roomUI.bed) + '</dt><dd>' + esc(c.bed) + '</dd></div></dl>' +
        '<h2 class="bt-subhead">' + esc(T.roomUI.amen) + '</h2>' +
        '<ul class="bt-amen">' + r.amen.map(function (k, n) {
          return '<li>' + svgIcon(IC[k], 17, '#5B7355') + esc(c.amen[n]) + '</li>';
        }).join('') + '</ul>' +
        '<h2 class="bt-subhead">' + esc(T.roomUI.shots) + '</h2>' +
        '<div class="bt-shots">' + r.shots.map(function (sh) {
          var gi = GAL.map(function (g) { return g.img; }).indexOf(sh);
          return '<button type="button" class="bt-shot" data-shot="' + (gi >= 0 ? gi : 0) + '" aria-label="' + esc(c.name) + '">' +
            pic(sh, c.name, '', '260px') + '</button>';
        }).join('') + '</div>' +
        '<p class="bt-note">' + esc(T.roomUI.note) + '</p></div>' +
      '<aside class="bt-dt-side"><p class="bt-side-label">' + esc(T.roomUI.rate) + '</p>' +
        '<p class="bt-side-price">' + money(rate) + '</p>' +
        '<dl class="bt-side-rows"><div><dt>' + esc(T.book.checkIn) + '</dt><dd>' + esc(fmtDate(S.ci)) + '</dd></div>' +
        '<div><dt>' + esc(T.book.checkOut) + '</dt><dd>' + esc(fmtDate(S.co)) + '</dd></div>' +
        '<div><dt>' + esc(T.book.guests) + '</dt><dd>' + S.guests + ' ' + esc(T.c.guest) + '</dd></div></dl>' +
        '<button type="button" class="bt-btn bt-btn--primary bt-side-cta" data-go="summary">' + esc(T.roomUI.bookThis) + '</button>' +
        '<p class="bt-note bt-side-note">' + esc(T.roomUI.sideNote) + '</p></aside>' +
      '</div></div></section>';
  };

  function simplePage(title, lede, crumbLabel, inner) {
    return '<section class="bt-view"><div class="bt-wrap bt-view-pad">' + crumb(crumbLabel || title) +
      '<h1 class="bt-page-title">' + esc(title) + '</h1>' +
      (lede ? '<p class="bt-lede-2">' + esc(lede) + '</p>' : '') + inner + '</div></section>';
  }

  V.dining = function () {
    return simplePage(T.sec.dining, T.sec.diningLede, T.nav.dining,
      '<div class="bt-outlets">' + T.dining.map(function (o, i) {
        return '<article class="bt-outlet">' + pic(OUTLETS[i].img, o.name, '', '(min-width:600px) 50vw, 100vw') +
          '<div class="bt-outlet-body"><h3>' + esc(o.name) + '</h3>' +
          '<p class="hours">' + esc(o.hours) + '</p><p>' + esc(o.body) + '</p>' +
          '<ul class="bt-menu">' + o.menu.map(function (m) {
            return '<li><span>' + esc(m[0]) + '</span><span class="price">' + esc(m[1]) + '</span></li>';
          }).join('') + '</ul></div></article>';
      }).join('') + '</div>' +
      '<div class="bt-split" style="margin-top:28px">' + pic('thai-food', T.dining[0].name, '', '(min-width:600px) 50vw, 100vw') +
      '<div class="bt-split-body"><h3>' + esc(T.dining[0].name) + '</h3><p>' + esc(T.dining[0].body) + '</p></div></div>');
  };

  V.facilities = function () {
    return simplePage(T.sec.facs, T.sec.facsLede, T.nav.facilities,
      '<div class="bt-facs">' + T.facs.map(function (f, i) {
        return '<article class="bt-fac">' + svgIcon(IC[FACS[i].icon], 24, '#5B7355', 1.5) +
          '<h3>' + esc(f.name) + '</h3><p>' + esc(f.body) + '</p><p class="hours">' + esc(f.hours) + '</p></article>';
      }).join('') + '</div>' +
      '<div class="bt-split" style="margin-top:28px">' + pic('pool', T.facs[0].name, '', '(min-width:600px) 50vw, 100vw') +
      '<div class="bt-split-body"><h3>' + esc(T.facs[2].name) + '</h3><p>' + esc(T.facs[2].body) + '</p></div></div>');
  };

  V.offers = function () {
    return simplePage(T.sec.offers, T.sec.offersLede, T.nav.offers,
      '<div class="bt-offers">' + T.offers.map(function (o, i) {
        return '<div class="bt-offer' + (OFFERS[i].lead ? ' is-lead' : '') + '">' +
          (o.tag ? '<span class="bt-offer-tag">' + esc(o.tag) + '</span>' : '') +
          '<h3>' + esc(o.name) + '</h3><p class="save">' + esc(o.save) + '</p><p>' + esc(o.body) + '</p>' +
          '<ul class="bt-terms">' + o.terms.map(function (t) { return '<li>' + esc(t) + '</li>'; }).join('') + '</ul>' +
          (OFFERS[i].code ? '<span class="bt-code">' + OFFERS[i].code + '</span>' : '') + '</div>';
      }).join('') + '</div>');
  };

  V.reviews = function () {
    return simplePage(T.sec.reviews, T.sec.reviewsLede, T.nav.reviews,
      '<div style="margin-top:20px">' + scoreBlock(false) + '</div>' +
      '<div class="bt-reviews">' + REVIEWS.map(function (_, i) { return reviewCard(i); }).join('') + '</div>');
  };

  V.about = function () {
    return simplePage(T.about.title, null, T.nav.about,
      '<div class="bt-split" style="margin-top:22px">' + pic('grounds', T.about.title, '', '(min-width:600px) 50vw, 100vw') +
      '<div class="bt-split-body">' + T.about.p.map(function (p) { return '<p>' + esc(p) + '</p>'; }).join('') + '</div></div>' +
      '<dl class="bt-facts" style="margin-top:26px;grid-template-columns:repeat(4,1fr)">' +
      T.about.stat.map(function (s) { return '<div><dt>' + esc(s[0]) + '</dt><dd>' + esc(s[1]) + '</dd></div>'; }).join('') + '</dl>' +
      '<div class="bt-split" style="margin-top:28px">' + pic('resort-evening', T.about.title, '', '(min-width:600px) 50vw, 100vw') +
      '<div class="bt-split-body"><h3>' + esc(T.sec.facs) + '</h3><p>' + esc(T.sec.facsLede) + '</p>' +
      '<button type="button" class="bt-btn bt-btn--ghost" style="margin-top:14px;display:inline-flex" data-go="facilities">' + esc(T.c.more) + '</button></div></div>');
  };

  V.gallery = function () {
    return '<section class="bt-view bt-gv"><div class="bt-wrap bt-view-pad">' +
      '<div class="bt-gv-head"><button type="button" class="bt-icon" data-go="home" aria-label="' + esc(T.nav.close) + '">' +
      svgIcon('M6 6l12 12M18 6L6 18', 20, 'currentColor', 1.9) + '</button>' +
      '<h1 class="bt-gv-title">' + esc(T.sec.gallery) + ' · ' + GAL.length + '</h1></div>' +
      '<div class="bt-gv-grid">' + GAL.map(function (g, i) {
        return '<button type="button" class="bt-shot" data-shot="' + i + '" aria-label="' + esc(T.sec.gallery) + ' ' + (i + 1) + '">' +
          pic(g.img, T.sec.gallery + ' ' + (i + 1), '', '33vw') + '</button>';
      }).join('') + '</div></div></section>';
  };

  V.faq = function () {
    return simplePage(T.sec.faq, null, T.nav.faq,
      '<div class="bt-faq">' + T.faq.map(function (f) {
        return '<div><button type="button" class="bt-q" aria-expanded="false"><span>' + esc(f.q) + '</span>' +
          svgIcon('M6 9l6 6 6-6', 18, '#5B7355', 1.9) + '</button>' +
          '<div class="bt-a"><p>' + esc(f.a) + '</p></div></div>';
      }).join('') + '</div>' +
      '<h2 class="bt-h2" style="margin-top:38px">' + esc(T.policy.title) + '</h2>' +
      '<div class="bt-ptable-wrap" style="margin-top:16px"><table class="bt-ptable">' +
      '<thead><tr><th>' + esc(T.policy.cancelHead[0]) + '</th><th style="text-align:right">' + esc(T.policy.cancelHead[1]) + '</th></tr></thead><tbody>' +
      T.policy.cancel.map(function (r) { return '<tr><td>' + esc(r[0]) + '</td><td>' + esc(r[1]) + '</td></tr>'; }).join('') +
      '</tbody></table></div>' +
      '<div class="bt-facs" style="margin-top:20px">' + T.policy.blocks.map(function (b) {
        return '<article class="bt-fac">' + svgIcon(IC.shield, 22, '#5B7355', 1.5) + '<h3>' + esc(b.h) + '</h3><p>' + esc(b.p) + '</p></article>';
      }).join('') + '</div>');
  };

  V.contact = function () {
    return simplePage(T.sec.contact, T.contact.hours, T.nav.contact,
      '<div style="margin-top:20px">' + mapPanel() + '</div>' +
      '<address class="bt-addr">' + esc(T.contact.addr) + '</address>' +
      '<h2 class="bt-subhead">' + esc(T.contact.routesHead) + '</h2>' +
      '<ul class="bt-routes">' + T.contact.routes.map(function (r) {
        return '<li><span class="how">' + esc(r[0]) + '</span><span class="t">' + esc(r[1]) + '</span></li>';
      }).join('') + '</ul>' +
      '<div class="bt-contact" style="margin-top:20px">' +
        '<a class="bt-btn bt-btn--green" href="tel:+66320000000">' + esc(T.contact.phone) + '</a>' +
        '<a class="bt-btn bt-btn--ghost" href="https://line.me" target="_blank" rel="noopener">' + esc(T.contact.line) + '</a>' +
        '<a class="bt-btn bt-btn--ghost" href="https://maps.google.com/?q=12.5684,99.9577" target="_blank" rel="noopener">' + esc(T.contact.maps) + '</a>' +
      '</div>');
  };

  V.summary = function () {
    var q = quote(), r = ROOMS[S.sel], c = T.rooms[S.sel];
    var rows = q.info ? q.info.rows : [];
    var nightList = rows.length ? '<div class="bt-nightlist">' + rows.map(function (n) {
      return '<div class="bt-night"><span class="lbl">' + esc(fmtDate(n.iso)) +
        (n.peak ? '<span class="tag">' + esc(T.book.peak) + '</span>' : n.weekend ? '<span class="tag">' + esc(T.book.weekend) + '</span>' : '') +
        '</span><span class="val">' + money(n.rate) + '</span></div>';
    }).join('') + '</div>' : '';
    var msg = S.promoMsg;
    return '<section class="bt-view"><div class="bt-wrap bt-view-pad">' + crumb(T.book.summary) +
      '<button type="button" class="bt-icon bt-back" data-go="room" aria-label="' + esc(T.c.back) + '">' +
      svgIcon('M15 5l-7 7 7 7', 20, 'currentColor', 2) + '</button>' +
      '<h1 class="bt-page-title">' + esc(T.book.summary) + '</h1>' +
      '<div class="bt-sum">' +
        '<div class="bt-sum-a"><div class="bt-sum-room">' + pic(r.slug, c.name, '', '112px') +
          '<div><p class="n">' + esc(c.name) + '</p><p class="m">' + r.size + ' ' + esc(T.roomUI.sqm) + ' · ' + esc(c.bed) + '</p>' +
          '<p class="p">' + esc(T.c.inclTax) + '</p></div></div>' +
          '<dl class="bt-rows">' +
            '<div><dt>' + esc(T.book.checkIn) + '</dt><dd>' + esc(fmtDate(S.ci)) + '</dd></div>' +
            '<div><dt>' + esc(T.book.checkOut) + '</dt><dd>' + esc(fmtDate(S.co)) + '</dd></div>' +
            '<div><dt>' + esc(T.book.nights) + '</dt><dd>' + q.nights + ' ' + esc(T.c.night) + '</dd></div>' +
            '<div><dt>' + esc(T.book.guests) + '</dt><dd>' + S.guests + ' ' + esc(T.c.guest) + '</dd></div>' +
          '</dl>' +
          (nightList ? '<h2 class="bt-subhead">' + esc(T.book.perNight) + '</h2>' + nightList : '') +
        '</div>' +
        '<div class="bt-sum-b"><div class="bt-price">' +
          '<div class="bt-price-row"><span>' + tpl(T.book.roomTotal, { n: q.nights }) + '</span><span>' + money(q.roomSum) + '</span></div>' +
          '<div class="bt-price-row' + (q.extra ? '' : ' is-off') + '"><span>' + tpl(T.book.extraGuest, { n: Math.max(0, S.guests - 2) }) + '</span><span>' + (q.extra ? money(q.extra) : '—') + '</span></div>' +
          (q.off ? '<div class="bt-price-row"><span>' + tpl(T.book.promoOff, { code: q.code }) + '</span><span>−' + money(q.off) + '</span></div>' : '') +
          '<div class="bt-price-row"><span>' + esc(T.book.service) + '</span><span>' + money(q.service) + '</span></div>' +
          '<div class="bt-price-total"><span>' + esc(T.book.payToday) + '</span><b>' + money(q.deposit) + '</b></div>' +
          '<p class="bt-price-foot">' + tpl(T.book.totalNote, { t: money(q.total) }) + '</p>' +
          '<div class="bt-promo"><input class="bt-input" id="promo" placeholder="' + esc(T.book.promoPh) + '" value="' + esc(S.promo) + '" aria-label="' + esc(T.book.promo) + '">' +
          '<button type="button" class="bt-btn bt-btn--ghost" id="promo-go">' + esc(T.book.apply) + '</button></div>' +
          '<p class="bt-promo-msg ' + (msg ? msg.k : '') + '" aria-live="polite">' + (msg ? esc(msg.t) : '') + '</p>' +
        '</div>' +
        '<button type="button" class="bt-btn bt-btn--primary bt-side-cta" data-go="confirm">' + esc(T.book.confirm) + '</button></div>' +
        '<div class="bt-sum-c"><div class="bt-form">' +
          '<label><span>' + esc(T.book.name) + '</span><input class="bt-input" type="text" id="f-name" placeholder="' + esc(T.book.namePh) + '" autocomplete="name"></label>' +
          '<label><span>' + esc(T.book.phone) + '</span><input class="bt-input" type="tel" id="f-phone" placeholder="' + esc(T.book.phonePh) + '" autocomplete="tel"></label>' +
        '</div><p class="bt-note">' + esc(T.book.confirmNote) + '</p></div>' +
      '</div></div></section>';
  };

  V.success = function () {
    var q = quote(), c = T.rooms[S.sel];
    return '<section class="bt-view"><div class="bt-wrap bt-view-pad"><div class="bt-ok">' +
      '<div class="bt-ok-mark">' + svgIcon('M20 6L9 17l-5-5', 36, '#5B7355', 2.2) + '</div>' +
      '<h1>' + esc(T.book.okTitle) + '</h1>' +
      '<p class="bt-ok-lede">' + tpl(T.book.okLede, { p: esc(S.phone || T.book.phonePh) }) + '</p>' +
      '<div class="bt-ok-card"><span>' + esc(T.book.ref) + '</span><p class="bt-ref">' + esc(S.ref || 'BT-0000') + '</p>' +
      '<dl class="bt-ok-rows">' +
        '<div><dt>' + esc(T.book.okRoom) + '</dt><dd>' + esc(c.name) + '</dd></div>' +
        '<div><dt>' + esc(T.book.okDates) + '</dt><dd>' + esc(fmtDate(S.ci)) + ' – ' + esc(fmtDate(S.co)) + '</dd></div>' +
        '<div><dt>' + esc(T.book.okName) + '</dt><dd>' + esc(S.name || '—') + '</dd></div>' +
        '<div><dt>' + esc(T.book.okDeposit) + '</dt><dd>' + money(q.deposit) + '</dd></div>' +
      '</dl></div>' +
      '<div class="bt-ok-actions"><a class="bt-btn bt-btn--green" href="https://line.me" target="_blank" rel="noopener">' + esc(T.book.sendSlip) + '</a>' +
      '<button type="button" class="bt-btn bt-btn--ghost" data-go="home">' + esc(T.book.backHome) + '</button></div>' +
      '<p class="bt-note">' + esc(T.book.okNote) + '</p></div></div></section>';
  };

  /* ── persistent chrome ───────────────────────────────────── */
  var NAVS = ['rooms', 'dining', 'facilities', 'offers', 'reviews', 'gallery', 'about', 'faq', 'contact'];

  function renderChrome() {
    /* the skip link lives in the shell, so it has to be translated here or it
       is the one string that stays Thai in English */
    var sk = $('skip'); if (sk) sk.textContent = T.nav.skip;
    $('hd').innerHTML = '<div class="bt-hd-in">' +
      '<a class="bt-logo" href="#/" data-go="home"><b>BAAN TALAY</b><span>' +
        (S.lang === 'th' ? 'หัวหิน · ริมทะเล' : 'HUA HIN · BEACHFRONT') + '</span></a>' +
      '<nav class="bt-nav" aria-label="' + esc(T.nav.menu) + '">' +
        NAVS.slice(0, 5).map(function (k) { return '<button type="button" data-go="' + k + '">' + esc(T.nav[k]) + '</button>'; }).join('') +
        '<span class="bt-lang" role="group" aria-label="Language">' +
          '<button type="button" data-lang="th" aria-pressed="' + (S.lang === 'th') + '">TH</button>' +
          '<button type="button" data-lang="en" aria-pressed="' + (S.lang === 'en') + '">EN</button>' +
        '</span>' +
      '</nav></div>';

    $('drawer').innerHTML = '<div class="bt-drawer-head">' +
      '<span class="bt-logo"><b>BAAN TALAY</b><span>' + (S.lang === 'th' ? 'หัวหิน · ริมทะเล' : 'HUA HIN · BEACHFRONT') + '</span></span>' +
      '<button type="button" class="bt-icon" id="drawer-close" aria-label="' + esc(T.nav.close) + '">' +
      svgIcon('M6 6l12 12M18 6L6 18', 20, 'currentColor', 1.9) + '</button></div>' +
      '<ul>' + NAVS.map(function (k) { return '<li><button type="button" data-go="' + k + '">' + esc(T.nav[k]) + '</button></li>'; }).join('') +
      '<li><a href="tel:+66320000000">' + esc(T.contact.phone) + '</a></li>' +
      '<li><span class="bt-lang" style="margin:10px 0">' +
        '<button type="button" data-lang="th" aria-pressed="' + (S.lang === 'th') + '">TH</button>' +
        '<button type="button" data-lang="en" aria-pressed="' + (S.lang === 'en') + '">EN</button></span></li>' +
      '</ul>';

    $('foot').innerHTML = '<div class="bt-wrap"><div class="bt-foot-grid">' +
      '<div><h2>' + esc(T.foot.addr) + '</h2><address>' + esc(T.contact.addr) + '</address></div>' +
      '<div><h2>' + esc(T.foot.contact) + '</h2><ul>' +
        '<li><a href="tel:+66320000000">032 000 000</a></li>' +
        '<li><a href="https://line.me" target="_blank" rel="noopener">' + esc(T.contact.line) + '</a></li>' +
        '<li><a href="https://maps.google.com/?q=12.5684,99.9577" target="_blank" rel="noopener">' + esc(T.contact.maps) + '</a></li>' +
      '</ul></div>' +
      '<div><h2>' + esc(T.foot.hours) + '</h2><p>' + esc(T.foot.time) + '<br>' + esc(T.foot.callHours) + '</p>' +
        '<div class="bt-foot-links">' + ['rooms', 'dining', 'offers', 'faq'].map(function (k) {
          return '<button type="button" data-go="' + k + '">' + esc(T.nav[k]) + '</button>';
        }).join('') + '</div></div>' +
      '</div>' +
      '<p class="bt-foot-legal">' + esc(T.foot.company) + '<br>' + esc(T.foot.legal) + '</p>' +
      '<p class="bt-foot-note">' + esc(T.foot.disclosure) + '</p></div>';
  }

  function renderBar() {
    var bar = $('bar'), show = ['home', 'rooms', 'room', 'summary'].indexOf(S.view) >= 0;
    bar.hidden = !show;
    document.body.classList.toggle('bt-has-bar', show);
    if (!show) return;
    var q = quote(), withPrice = S.view === 'room' || S.view === 'summary';
    var rate = S.ci && S.co ? Math.round(stay(S.sel, S.ci, S.co).sum / q.nights) : rateFor(S.sel, iso(new Date()));
    bar.innerHTML =
      (withPrice ? '<span class="bt-bar-price"><span>' + esc(S.view === 'room' ? T.roomUI.rate : T.book.payToday) + '</span>' +
        '<b>' + money(S.view === 'room' ? rate : q.deposit) + '</b></span>' : '') +
      '<button type="button" class="bt-btn bt-btn--primary" data-go="' +
        (S.view === 'summary' ? 'confirm' : S.view === 'room' ? 'summary' : 'rooms') + '">' +
        esc(S.view === 'summary' ? T.book.confirm : S.view === 'room' ? T.roomUI.bookThis : T.nav.book) + '</button>';
  }

  /* ── router ──────────────────────────────────────────────── */
  var ROUTE = { home: '#/', rooms: '#/rooms', room: '#/room', dining: '#/dining',
    facilities: '#/facilities', offers: '#/offers', reviews: '#/reviews', about: '#/about',
    gallery: '#/gallery', faq: '#/faq', contact: '#/contact', summary: '#/summary', success: '#/success' };

  function viewFromHash() {
    for (var k in ROUTE) { if (ROUTE[k] === location.hash) return k; }
    return 'home';
  }
  function render() {
    S.view = viewFromHash();
    T = L[S.lang];
    document.documentElement.lang = S.lang;
    renderChrome();
    $('app').innerHTML = (V[S.view] || V.home)();
    renderBar();
    syncHeader();
    revealAll();
    if ($('in')) { $('in').min = iso(new Date()); }
    if ($('out')) { $('out').min = S.ci ? addDays(S.ci, 1) : iso(new Date()); }
    if (S.view === 'summary') {
      if ($('f-name')) $('f-name').value = S.name || '';
      if ($('f-phone')) $('f-phone').value = S.phone || '';
    }
  }
  var pending = null;
  function go(name) {
    if (location.hash === ROUTE[name]) { render(); window.scrollTo(0, 0); }
    else location.hash = ROUTE[name];
  }

  function nav(what) {
    if (what === 'confirm') {
      S.ref = 'BT-' + String(Math.floor(1000 + rnd('ref' + S.ci + S.sel + Date.now()) * 9000)).slice(0, 4);
      go('success'); return;
    }
    if (ROUTE[what]) { go(what); return; }
  }

  function syncHeader() {
    var hd = $('hd');
    if (S.view !== 'home') { hd.classList.remove('is-over'); return; }
    var hero = document.querySelector('.bt-hero');
    hd.classList.toggle('is-over', window.scrollY < (hero ? hero.offsetHeight - 90 : 320));
  }
  function revealAll() {
    var rv = document.querySelectorAll('.rv');
    if (!('IntersectionObserver' in window)) {
      Array.prototype.forEach.call(rv, function (e) { e.classList.add('is-in'); }); return;
    }
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('is-in'); io.unobserve(e.target); } });
    }, { threshold: 0.08, rootMargin: '0px 0px -6% 0px' });
    Array.prototype.forEach.call(rv, function (e) { io.observe(e); });
    /* A lazy trigger that fails to fire produces no error and no console
       warning — work.html once shipped 13 cards at opacity 0 exactly this way
       while Lighthouse still scored 100. The observer is the nice path. */
    setTimeout(function () {
      Array.prototype.forEach.call(rv, function (e) {
        if (!e.classList.contains('is-in') && e.getBoundingClientRect().top < window.innerHeight) e.classList.add('is-in');
      });
    }, 2500);
  }

  /* ── lightbox ────────────────────────────────────────────── */
  var lastFocus = null;
  function lbSet(i) {
    S.lb = i;
    var g = GAL[i], big = g.img === 'beach-morning' ? '-1800' : '-1200';
    $('lb-img').src = IMG + g.img + big + '.webp';
    $('lb-img').alt = T.sec.gallery + ' ' + (i + 1);
    $('lb-cap').textContent = T.sec.gallery + ' ' + (i + 1) + ' / ' + GAL.length;
    $('lb-count').textContent = (i + 1) + ' / ' + GAL.length;
  }
  function lbOpen(i) { lastFocus = document.activeElement; lbSet(i); $('lb').hidden = false; document.body.style.overflow = 'hidden'; $('lb-close').focus(); }
  function lbClose() {
    if (S.lb < 0) return;
    S.lb = -1; $('lb').hidden = true; document.body.style.overflow = '';
    if (lastFocus && lastFocus.isConnected) lastFocus.focus();
    lastFocus = null;
  }
  function lbStep(d) { if (S.lb >= 0) lbSet((S.lb + d + GAL.length) % GAL.length); }

  function setDrawer(open) {
    var d = $('drawer'), b = $('burger');
    if (open) d.setAttribute('data-open', ''); else d.removeAttribute('data-open');
    if (b) b.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) { var f = d.querySelector('button, a'); if (f) f.focus(); }
  }

  /* ── events (delegated: the DOM is re-rendered on every view) ── */
  document.addEventListener('click', function (e) {
    var t = e.target;
    var lang = t.closest('[data-lang]');
    if (lang) { setLang(lang.dataset.lang); return; }
    var g = t.closest('[data-go]');
    if (g) { e.preventDefault(); setDrawer(false); nav(g.dataset.go); return; }
    var rm = t.closest('[data-room]');
    if (rm) { S.sel = +rm.dataset.room; go('room'); return; }
    var sh = t.closest('[data-shot]');
    if (sh) { lbOpen(+sh.dataset.shot); return; }
    if (t.closest('#burger')) { setDrawer($('burger').getAttribute('aria-expanded') !== 'true'); return; }
    if (t.closest('#drawer-close')) { setDrawer(false); return; }
    if (t.closest('#lb-close')) { lbClose(); return; }
    if (t.closest('#lb-prev')) { lbStep(-1); return; }
    if (t.closest('#lb-next')) { lbStep(1); return; }
    if (t === $('lb')) { lbClose(); return; }
    if (t.closest('#g-inc')) { S.guests = Math.min(6, S.guests + 1); render(); return; }
    if (t.closest('#g-dec')) { S.guests = Math.max(1, S.guests - 1); render(); return; }
    if (t.closest('#promo-go')) { applyPromo(); return; }
    var q = t.closest('.bt-q');
    if (q) {
      var open = q.getAttribute('aria-expanded') === 'true';
      Array.prototype.forEach.call(document.querySelectorAll('.bt-q'), function (b) { b.setAttribute('aria-expanded', 'false'); });
      q.setAttribute('aria-expanded', open ? 'false' : 'true');
    }
  });

  function applyPromo() {
    var v = ($('promo').value || '').trim().toUpperCase();
    S.promo = v;
    if (!v) { S.promoMsg = null; }
    else if (v !== 'EARLYBIRD') { S.promoMsg = { k: 'no', t: T.book.promoBadCode }; S.promo = ''; }
    else if (!S.ci || daysUntil(S.ci) < 30) { S.promoMsg = { k: 'no', t: tpl(T.book.promoTooLate, { code: v }) }; S.promo = ''; }
    else { S.promoMsg = { k: 'ok', t: tpl(T.book.promoOk, { code: v, n: 15 }) }; }
    render();
  }

  document.addEventListener('change', function (e) {
    if (e.target.id === 'in') {
      S.ci = e.target.value;
      if (S.co && S.co <= S.ci) S.co = '';
      render();
    } else if (e.target.id === 'out') {
      if (S.ci && e.target.value <= S.ci) { e.target.value = S.co; return; }
      S.co = e.target.value; render();
    }
  });
  document.addEventListener('input', function (e) {
    if (e.target.id === 'f-name') S.name = e.target.value;
    if (e.target.id === 'f-phone') S.phone = e.target.value;
  });
  document.addEventListener('keydown', function (e) {
    if (e.key === 'Escape') { lbClose(); setDrawer(false); return; }
    if (S.lb < 0) return;
    if (e.key === 'ArrowRight') lbStep(1);
    if (e.key === 'ArrowLeft') lbStep(-1);
  });

  function setLang(code) {
    if (code === S.lang) return;
    S.lang = code;
    try { localStorage.setItem('bt-lang', code); } catch (err) {}
    render();
  }

  window.addEventListener('hashchange', function () { render(); window.scrollTo(0, 0); });
  window.addEventListener('scroll', syncHeader, { passive: true });
  window.addEventListener('resize', syncHeader, { passive: true });

  /* ── init ────────────────────────────────────────────────── */
  /* The header's transparent-over-hero state must not depend on a transition
     finishing: Chrome freezes transitions in a tab that is not visible, which
     is how an opaque bar reached a showcase screenshot once already. */
  document.documentElement.classList.add('bt-boot');
  requestAnimationFrame(function () {
    requestAnimationFrame(function () { document.documentElement.classList.remove('bt-boot'); });
  });
  try {
    var saved = localStorage.getItem('bt-lang');
    if (saved === 'en' || saved === 'th') S.lang = saved;
  } catch (err) {}
  render();
})();
