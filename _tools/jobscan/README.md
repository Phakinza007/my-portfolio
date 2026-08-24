# jobscan — สแกนงานจาก Fastwork job board

สแกน `jobboard.fastwork.co/jobs` ทุก 2 ชม. ในเวลาทำการ จัดอันดับตามความเข้ากับงานที่
ส่งมอบได้จริง แล้วแจ้งเฉพาะ **งานใหม่** เข้า GitHub Issue (+ Discord ถ้าตั้ง webhook)

รันบน GitHub Actions ไม่ใช่บนเครื่อง — ดู `.github/workflows/jobscan.yml`

## ใช้ยังไง

```bash
# ลองเกณฑ์คะแนนแบบไม่ต่อเน็ต ไม่เขียน state ไม่แจ้งเตือน
python3 _tools/jobscan/scan.py --dry-run --fixture _tools/jobscan/fixtures/jobs.json

# รอบแรกของจริง: จำ id ไว้เฉย ๆ ไม่แจ้งเตือน
python3 _tools/jobscan/scan.py --state-dir _state --seed

# รอบปกติ
python3 _tools/jobscan/scan.py --state-dir _state
```

## ไฟล์

| ไฟล์ | หน้าที่ |
|---|---|
| `recon.py` | สำรวจว่าบอร์ดเสิร์ฟข้อมูลยังไง — รันครั้งเดียวตอนเริ่ม หรือตอนที่ parser พัง |
| `fetch.py` | ดึงข้อมูลจากแหล่งที่ recon เจอ |
| `normalize.py` | แปลง payload ดิบเป็น record มาตรฐาน |
| `score.py` | ให้คะแนน + เหตุผล อ่านเกณฑ์จาก `profile.json` |
| `profile.json` | **เกณฑ์ทั้งหมดอยู่ที่นี่** แก้คำ/น้ำหนักได้โดยไม่ต้องแตะโค้ด |
| `state.py` | `seen.json` (กันแจ้งซ้ำ) + `jobs/YYYY-MM.jsonl` (เก็บย้อนหลัง) |
| `notify.py` | GitHub Issue + Discord |
| `scan.py` | ร้อยทั้งหมดเข้าด้วยกัน |

## สามอย่างที่ตั้งใจให้เป็นแบบนี้

**คะแนนใช้จัดอันดับ ไม่ได้ใช้กรอง** งานหมวดเว็บทุกงานขึ้น digest หมด คะแนนบอกว่าควรอ่าน
อันไหนก่อน และ `reasons` บอกว่าทำไม — ตัวกรองที่ตัดงานผิดตัวทิ้งจะไม่มีใครเห็น ส่วนงานที่
อยู่อันดับท้าย ๆ พร้อมเหตุผลกำกับ ยังอยู่ให้เถียงได้

**ดึงได้ 0 รายการ = error ไม่ใช่ "ไม่มีงานใหม่"** parser ที่พังกับบอร์ดที่ว่างจริงให้ผล
หน้าตาเหมือนกันเป๊ะ อย่างหลังต้องดังกว่า ใส่ `--allow-empty` ถ้าตั้งใจ

**รอบแรก seed เงียบ ๆ** `seen.json` ที่ว่างเปล่าจะมองว่าทั้งบอร์ดคืองานใหม่ ถ้าแจ้งเลยจะได้
issue เดียวยาวเป็นร้อยบรรทัด

## state เก็บที่ไหน

branch `jobscan-state` (orphan) ไม่ใช่ `main` — เพราะ `main` auto-deploy ไป GitHub Pages
ทุก commit การเขียน state ลง `main` = deploy วันละ 7 ครั้งโดยที่เว็บไม่มีอะไรเปลี่ยน

## มารยาทกับปลายทาง

`recon.py` อ่าน `robots.txt` แล้วเช็คด้วย `urllib.robotparser` ก่อนทุกครั้ง ถ้า `/jobs`
ถูก `Disallow` มันจะ **หยุดและรายงาน** ไม่ใช่หาทางอ้อม User-Agent บอกตรง ๆ ว่าเป็นอะไรและ
ติดต่อใครได้ ยิง 1–2 request ต่อรอบ วันละ 7 รอบ และไม่เอาข้อมูลไปเผยแพร่ต่อ
