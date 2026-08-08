# SupplyMate Wholesale Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship a Thai B2B wholesale-commerce demo, derived from `Phakinza007/ecom`, that demonstrates a customer ordering flow and a secure owner fulfilment workflow, then add it truthfully to the portfolio.

**Architecture:** Keep `ecom` as a separate React/Vite/Supabase deployment; the static portfolio only links to the deployed demo and describes it as a self-initiated concept. Extend the existing security-preserving commerce flow with product pack metadata and business-order snapshots. Client UI may request an order, but the Supabase RPC continues to re-read price, availability, and shipping information server-side.

**Tech Stack:** React 19, TypeScript, Vite, Tailwind v4, shadcn/ui, TanStack Query, Zustand, Supabase Auth/Postgres/Storage/RLS, Playwright, Vercel.

## Global Constraints

- Work in a fresh `supplymate-wholesale` clone derived from `Phakinza007/ecom`; do not put React application files or dependencies in the static portfolio repository.
- Use Thai buyer-facing copy and `฿`; describe the project publicly as a self-initiated SupplyMate concept, never as client work.
- Generate every decorative/product image specifically for SupplyMate using the `imagegen` skill and tool. Do not use stock images, external placeholder URLs, copied product photography, invented reviews, invented customers, or invented business results.
- Keep all real customer data, credentials, payment accounts, and production LINE credentials out of the demo. Use only documented demo accounts and local/owned Supabase projects.
- `src/core/**` must not import from `src/modules/optional/**`; optional features remain lazy-loaded behind `<Feature>`.
- Preserve server-authoritative order pricing, private payment-slip storage, RLS policies, admin route protection, trigger-enforced order transitions, and deactivate-instead-of-delete catalogue behavior.
- Add only: `carton`, `pack`, `roll`, and `case` as product order units. A product always has an integer `units_per_package >= 1` and `min_order_quantity >= 1`.
- Store business details as immutable order snapshot fields, not as mutable user profile fields: `business_name`, optional `tax_id`, and optional `branch_name`.
- A rejected payment slip requires an admin reason and must clear both the old slip path and the rejection reason only when a new slip is successfully attached.
- Preserve the manually maintained `__InternalSupabase` block after regenerating `src/lib/database.types.ts`.
- Before portfolio edits, verify the deployed demo at 375px with no horizontal overflow and no browser-console errors.

---

## File Structure

### SupplyMate application repository

| Path | Responsibility |
|---|---|
| `src/config/branding.config.ts` | One client-specific store name, visual tokens, bank-transfer display data, and feature flags. |
| `src/index.css` | SupplyMate global color tokens and base typography only; no page-specific business logic. |
| `src/lib/wholesale.ts` | Pure pack-unit label/validation helpers shared by catalogue, cart, and admin UI. |
| `src/lib/resolveImageUrl.ts` | Treat generated local `/images/...` paths as browser-ready paths while retaining Supabase storage and absolute URL behavior. |
| `src/core/catalog/HomePage.tsx` | Customer-first home page with category navigation and a small, factual operating-information strip. |
| `src/core/catalog/ProductCard.tsx` | Product listing’s pack price, units-per-package, and minimum-order display. |
| `src/core/catalog/ProductDetailPage.tsx` | Product purchase screen; applies minimum order and presents realistic wholesale details. |
| `src/core/cart/CartPage.tsx` | Cart copy that makes clear quantity means cartons/packs/rolls/cases. |
| `src/core/checkout/CheckoutPage.tsx` | Validated business details and `p_business_details` RPC input. |
| `src/core/orders/OrderDetailPage.tsx` | Customer order state, carrier/tracking, cancellation, and payment-rejection explanation. |
| `src/core/admin/AdminProductForm.tsx` | Admin controls for pack metadata. |
| `src/core/admin/AdminProductListPage.tsx` | Admin catalogue rows with the order unit visible. |
| `src/core/admin/AdminOrderDetailPage.tsx` | Immutable buyer business snapshot and a required rejection reason. |
| `src/core/admin/useAdminOrderMutations.ts` | Typed status operations, including rejection reason. |
| `src/App.tsx` / `src/components/SiteHeader.tsx` | Route the new home page and present Thai commerce navigation. |
| `supabase/migrations/20260807000100_supplymate_wholesale.sql` | Product pack columns, order snapshot columns, hardened RPC replacements, and immutability trigger updates. |
| `supabase/seed.sql` | SupplyMate categories/products/orders/demo identities pointing only to generated local images. |
| `src/lib/database.types.ts` | Generated database contract, with the required internal block retained. |
| `e2e/supplymate-wholesale.spec.ts` | Product-unit and business-checkout assertions. |
| `e2e/golden-path.spec.ts` | Existing end-to-end checkout/admin fulfilment path, extended to verify buyer-visible tracking and payment rejection behavior. |
| `public/images/supplymate/*.png` | Six self-generated category/product images, committed as local demo assets. |

### Static portfolio repository

| Path | Responsibility |
|---|---|
| `showcase-supplymate.html` / `showcase-supplymate-en.html` | Truthful bilingual story-stack showcase and live-demo link. |
| `assets/screenshots/showcase-supplymate.jpg` | Screenshot captured from the deployed SupplyMate demo, not a borrowed image. |
| `assets/thumbs/supplymate.svg` | SVG thumbnail derived from SupplyMate’s actual rendered card at its natural size. |
| `index.html`, `index-en.html`, `work.html`, `work-en.html` | SupplyMate Selected Work card in both language grids. |
| `sitemap.xml`, `assets/search-index.json` | Discoverability entries for the bilingual showcase pages. |

## Task 1: Create a reproducible SupplyMate working baseline

**Files:**

- Create: a new `supplymate-wholesale` working clone derived from `Phakinza007/ecom`
- Modify: `README.md`
- Modify: `src/config/branding.config.ts`

**Interfaces:**

- Consumes: the source kit’s Vite scripts, Supabase migration history, feature flags, and local E2E configuration.
- Produces: a clean baseline with SupplyMate’s feature decisions documented before UI or database changes.

- [ ] **Step 1: Clone the source repository into a dedicated SupplyMate working directory and record its source revision.**

  Run:

  ```bash
  git clone https://github.com/Phakinza007/ecom.git supplymate-wholesale
  cd supplymate-wholesale
  git rev-parse HEAD
  git status --short
  ```

  Expected: the source SHA is recorded in the first SupplyMate commit message or README and `git status --short` is empty.

- [ ] **Step 2: Write a failing baseline checklist in `README.md` for SupplyMate’s required flows.**

  Add this exact acceptance list before changing implementation:

  ```markdown
  ## SupplyMate acceptance path

  - A buyer sees a Thai catalogue with pack unit and minimum order before adding an item.
  - Checkout records a business name and optional tax/branch details with the order.
  - A customer can see a payment-rejection explanation, carrier, tracking number, and cancellation reason.
  - An admin can see the immutable business snapshot, verify/reject a slip, ship, complete, and cancel an order.
  ```

- [ ] **Step 3: Set the source kit’s initial client-only configuration; do not add a second branding source.**

  In `src/config/branding.config.ts`, replace only the client configuration values with the following intent:

  ```ts
  storeName: 'SupplyMate Wholesale',
  logoUrl: '/images/supplymate/brandmark.svg',
  colors: {
    primary: 'oklch(0.30 0.06 252)',
    secondary: 'oklch(0.96 0.02 95)',
  },
  currencySymbol: '฿',
  features: {
    reviews: false,
    qna: false,
    variants: true,
    analyticsDashboard: false,
    stockAutomation: false,
    lineNotify: false,
    pdfDocuments: false,
    promotions: true,
  },
  ```

  Replace `bankTransfer` with clearly marked demo-only account display values; no real account name or number may be committed.

- [ ] **Step 4: Install dependencies and establish the source-kit baseline.**

  Run:

  ```bash
  npm ci
  npm run typecheck
  npm run lint
  npm run build
  ```

  Expected: all commands pass before functionality changes. If one fails, repair only the baseline discrepancy and re-run the command before continuing.

- [ ] **Step 5: Commit the isolated baseline.**

  ```bash
  git add README.md src/config/branding.config.ts
  git commit -m "chore: initialize SupplyMate wholesale demo"
  ```

## Task 2: Generate owned visual assets and make local assets resolvable

**Files:**

- Create: `public/images/supplymate/brandmark.svg`
- Create: `public/images/supplymate/cups-lids.png`
- Create: `public/images/supplymate/food-containers.png`
- Create: `public/images/supplymate/paper-bags.png`
- Create: `public/images/supplymate/labels.png`
- Create: `public/images/supplymate/bar-tools.png`
- Create: `public/images/supplymate/eco-packaging.png`
- Modify: `src/lib/resolveImageUrl.ts`
- Test: `src/lib/resolveImageUrl.test.ts`

**Interfaces:**

- Consumes: `ProductImage.storage_path`, which may be an absolute URL, a Supabase Storage key, or a local root-relative asset path.
- Produces: `resolveImageUrl(path: string): string`, returning local `/images/...` values unchanged and retaining current behavior for the other two path types.

- [ ] **Step 1: Use the `imagegen` skill before creating the six category images.**

  Generate six individual 1:1 assets with this shared instruction, changing only the bracketed product group:

  ```text
  Product photograph for a fictional Thai B2B packaging wholesaler called SupplyMate.
  Studio still life of [PRODUCT GROUP] arranged neatly in a small café supply warehouse.
  Practical commercial look, navy-and-cream paper sweep, soft daylight, no people,
  no labels, no readable text, no brand logos, no watermark, square composition.
  The product must look real and useful, not luxury beauty advertising.
  ```

  Use `[PRODUCT GROUP]` values `clear cold cups and black lids`, `kraft food containers`, `kraft paper bags`, `blank label rolls`, `stainless bar tools`, and `compostable bagasse packaging`. Save the generated outputs at the six named `public/images/supplymate/*.png` paths.

- [ ] **Step 2: Create a simple original SVG brandmark instead of downloading an icon.**

  Use a navy rounded square with a cream carton outline and a small safety-green check mark. Keep it at `viewBox="0 0 64 64"`, include a meaningful `<title>SupplyMate Wholesale</title>`, and do not include raster data or an external `<image>` reference.

- [ ] **Step 3: Write the failing resolver test before changing the resolver.**

  ```ts
  import { describe, expect, it } from 'vitest'
  import { resolveImageUrl } from './resolveImageUrl'

  describe('resolveImageUrl', () => {
    it('returns generated local public assets unchanged', () => {
      expect(resolveImageUrl('/images/supplymate/cups-lids.png'))
        .toBe('/images/supplymate/cups-lids.png')
    })
  })
  ```

- [ ] **Step 4: Run the focused test and verify the current implementation fails.**

  Run:

  ```bash
  npx vitest run src/lib/resolveImageUrl.test.ts
  ```

  Expected: the existing resolver attempts a Supabase public URL for the local path, so the assertion fails.

- [ ] **Step 5: Implement the narrow resolver change.**

  Add the local-path guard before the existing absolute-URL/Supabase branches:

  ```ts
  if (storagePath.startsWith('/')) return storagePath
  ```

  Do not change the existing `http(s)` pass-through or the Storage bucket lookup.

- [ ] **Step 6: Verify the resolver and commit owned assets.**

  ```bash
  npx vitest run src/lib/resolveImageUrl.test.ts
  npm run typecheck
  git add public/images/supplymate src/lib/resolveImageUrl.ts src/lib/resolveImageUrl.test.ts
  git commit -m "feat: add owned SupplyMate product imagery"
  ```

## Task 3: Add the wholesale data contract without weakening checkout security

**Files:**

- Create: `supabase/migrations/20260807000100_supplymate_wholesale.sql`
- Modify: `src/lib/database.types.ts`
- Modify: `supabase/seed.sql`
- Test: `e2e/supplymate-wholesale.spec.ts`

**Interfaces:**

- Produces product columns `package_unit`, `units_per_package`, and `min_order_quantity`.
- Produces immutable order fields `business_name`, `tax_id`, `branch_name`, and `payment_rejection_reason`.
- Replaces `public.create_order(jsonb, uuid, jsonb, text, text)` with `public.create_order(jsonb, uuid, jsonb, text, text, jsonb)`.
- Replaces `public.attach_payment_slip(uuid, text)` with the same signature but clears `payment_rejection_reason` when an accepted new slip is attached.

- [ ] **Step 1: Write the end-to-end data expectation first.**

  Create `e2e/supplymate-wholesale.spec.ts` with this initial database-visible checkout assertion, reusing `signUp`, `addAddress`, and `buyFirstProductAndUploadSlip` helpers:

  ```ts
  test('records immutable B2B checkout details', async ({ page }) => {
    await signUp(page, {
      fullName: 'Wholesale Buyer',
      email: uniqueEmail('wholesale-buyer'),
      password: 'password123',
    })
    await addAddress(page, {
      recipientName: 'Wholesale Buyer',
      phone: '0891234567',
      line1: '99 Test Street',
      province: 'Bangkok',
      postalCode: '10110',
    })
    await page.goto('/products/clear-cup-16oz')
    await expect(page.getByText('ขั้นต่ำ 1 ลัง')).toBeVisible()
    await page.getByRole('button', { name: 'เพิ่มลงตะกร้า' }).click()
    await page.goto('/checkout')
    await page.getByLabel('ชื่อร้านหรือบริษัท').fill('กาแฟริมคลอง')
    await page.getByLabel('เลขประจำตัวผู้เสียภาษี').fill('0105567000001')
    await page.getByRole('button', { name: 'ยืนยันคำสั่งซื้อ' }).click()
    await expect(page.getByText('กาแฟริมคลอง')).toBeVisible()
  })
  ```

- [ ] **Step 2: Run the test against local Supabase and confirm it fails before the schema/UI work exists.**

  Run:

  ```bash
  npm run test:e2e -- e2e/supplymate-wholesale.spec.ts
  ```

  Expected: the product and Thai B2B checkout labels do not exist yet.

- [ ] **Step 3: Write `20260807000100_supplymate_wholesale.sql` as an additive migration.**

  Add product fields with database validation:

  ```sql
  alter table public.products
    add column package_unit text not null default 'carton'
      check (package_unit in ('carton', 'pack', 'roll', 'case')),
    add column units_per_package integer not null default 1
      check (units_per_package >= 1),
    add column min_order_quantity integer not null default 1
      check (min_order_quantity >= 1);

  alter table public.orders
    add column business_name text,
    add column tax_id text,
    add column branch_name text,
    add column payment_rejection_reason text;
  ```

  In the same migration, replace the exact five-argument `create_order` overload with a six-argument version accepting `p_business_details jsonb default null`. Validate that the argument is either null or a JSON object; trim each string; use `nullif(trim(...), '')`; insert the three values with the order; and retain the source kit’s address ownership check, product row lock, active-variant condition, server-side pricing, promo revalidation, grants, and `security definer` search path.

  Update `enforce_order_immutability()` to assign the new business fields from `old`, so an admin status update cannot rewrite a placed order’s buyer data. Replace `attach_payment_slip(uuid, text)` so a successful upload sets `payment_rejection_reason = null` while retaining its ownership/status/path validation.

- [ ] **Step 4: Regenerate the database type contract and preserve the internal block.**

  Run the project’s local Supabase stack, then generate to a temporary file and compare it before replacing the tracked file:

  ```bash
  supabase start
  supabase db reset --yes
  supabase gen types typescript --local > /tmp/supplymate-database.types.ts
  ```

  Copy the existing `__InternalSupabase` / `PostgrestVersion` block into the generated output if the CLI omitted it; then replace `src/lib/database.types.ts`. Confirm `products` and `orders` contain every new field and `Functions.create_order.Args` contains `p_business_details`.

- [ ] **Step 5: Replace generic seed data with a complete local SupplyMate catalogue.**

  Seed six Thai categories and 18–24 supply products. Each row must include a unique Thai/ASCII slug, SKU, generated local image path, non-zero stock, price, `package_unit`, `units_per_package`, and `min_order_quantity`. Use this pattern for every product image reference:

  ```sql
  ('<product-id>', '/images/supplymate/cups-lids.png', 'แก้วพลาสติกใส 16 ออนซ์พร้อมฝาโดม', 0)
  ```

  Seed variants only where a buyer would choose a material, size, lid type, or carton count. Preserve the existing two demo identities, but name them `ผู้ดูแล SupplyMate` and `ร้านกาแฟตัวอย่าง`; create sample orders through `public.create_order`, never direct inserts.

- [ ] **Step 6: Reset the local database and run the type/lint gates.**

  ```bash
  supabase db reset --yes
  npm run typecheck
  npm run lint
  ```

  Expected: migrations apply from a clean database; generated types and the boundary check pass.

- [ ] **Step 7: Commit the data contract as one reviewable change.**

  ```bash
  git add supabase/migrations/20260807000100_supplymate_wholesale.sql \
    supabase/seed.sql src/lib/database.types.ts e2e/supplymate-wholesale.spec.ts
  git commit -m "feat: model SupplyMate wholesale orders"
  ```

## Task 4: Make wholesale units visible and enforce minimum purchase quantities

**Files:**

- Create: `src/lib/wholesale.ts`
- Create: `src/lib/wholesale.test.ts`
- Modify: `src/core/catalog/ProductCard.tsx`
- Modify: `src/core/catalog/ProductDetailPage.tsx`
- Modify: `src/core/cart/CartPage.tsx`
- Modify: `src/core/admin/AdminProductForm.tsx`
- Modify: `src/core/admin/AdminProductListPage.tsx`
- Test: `e2e/supplymate-wholesale.spec.ts`

**Interfaces:**

- Produces `formatPackageLabel(unit, unitsPerPackage): string` and `quantityLabel(unit, quantity): string` from `src/lib/wholesale.ts`.
- Consumes the product fields created in Task 3; neither helper calls Supabase or reads feature flags.

- [ ] **Step 1: Write helper tests before implementing copy logic.**

  ```ts
  import { describe, expect, it } from 'vitest'
  import { formatPackageLabel, quantityLabel } from './wholesale'

  describe('wholesale labels', () => {
    it('describes cartons in Thai', () => {
      expect(formatPackageLabel('carton', 1_000)).toBe('1,000 ชิ้น / ลัง')
      expect(quantityLabel('carton', 3)).toBe('3 ลัง')
    })
  })
  ```

- [ ] **Step 2: Confirm the new helper test fails.**

  ```bash
  npx vitest run src/lib/wholesale.test.ts
  ```

  Expected: `src/lib/wholesale.ts` has not been created.

- [ ] **Step 3: Implement the pure helper with exhaustive order-unit handling.**

  ```ts
  export type PackageUnit = 'carton' | 'pack' | 'roll' | 'case'

  const thaiUnit: Record<PackageUnit, string> = {
    carton: 'ลัง',
    pack: 'แพ็ก',
    roll: 'ม้วน',
    case: 'กล่อง',
  }

  export function quantityLabel(unit: PackageUnit, quantity: number) {
    return `${quantity.toLocaleString('th-TH')} ${thaiUnit[unit]}`
  }

  export function formatPackageLabel(unit: PackageUnit, unitsPerPackage: number) {
    return `${unitsPerPackage.toLocaleString('th-TH')} ชิ้น / ${thaiUnit[unit]}`
  }
  ```

- [ ] **Step 4: Render the same product truth at each decision point.**

  In `ProductCard`, show `ราคา / ลัง` (or matching unit) and `formatPackageLabel`. In `ProductDetailPage`, set the quantity input’s `min` to `product.min_order_quantity`, initialize state from that minimum, and clamp the value upward to it. Use `quantityLabel` in the cart row rather than rendering an ambiguous `× 3`. In `AdminProductForm`, add labelled controls `หน่วยสั่งซื้อ`, `จำนวนต่อหน่วย`, and `ขั้นต่ำต่อรายการ`; pass all three typed fields through `ProductInput` without creating a parallel form state.

- [ ] **Step 5: Extend the browser assertion before treating the UI as complete.**

  Add these checks to `e2e/supplymate-wholesale.spec.ts`:

  ```ts
  await expect(page.getByText('1,000 ชิ้น / ลัง')).toBeVisible()
  const quantity = page.getByRole('spinbutton')
  await expect(quantity).toHaveValue('1')
  await quantity.fill('0')
  await expect(quantity).toHaveValue('1')
  ```

- [ ] **Step 6: Run focused tests and commit.**

  ```bash
  npx vitest run src/lib/wholesale.test.ts
  npm run test:e2e -- e2e/supplymate-wholesale.spec.ts
  git add src/lib/wholesale.ts src/lib/wholesale.test.ts src/core/catalog \
    src/core/cart/CartPage.tsx src/core/admin/AdminProductForm.tsx \
    src/core/admin/AdminProductListPage.tsx e2e/supplymate-wholesale.spec.ts
  git commit -m "feat: show wholesale pack and minimum order details"
  ```

## Task 5: Build a Thai customer-first storefront around the real catalogue

**Files:**

- Create: `src/core/catalog/HomePage.tsx`
- Modify: `src/App.tsx`
- Modify: `src/components/SiteHeader.tsx`
- Modify: `src/core/catalog/ProductListPage.tsx`
- Modify: `src/index.css`
- Test: `e2e/supplymate-wholesale.spec.ts`

**Interfaces:**

- `HomePage` consumes `useCategories()` and `useProducts()`; it contains no duplicate product list or hardcoded product image URL.
- `App` owns the `/` route and `SiteHeader` owns global navigation; both display Thai labels but preserve existing route URLs.

- [ ] **Step 1: Write the failing storefront navigation test.**

  ```ts
  test('starts a B2B buyer in the catalogue', async ({ page }) => {
    await page.goto('/')
    await expect(page.getByRole('heading', { name: 'ของใช้ร้านอาหารและคาเฟ่ สั่งเป็นลัง ส่งตรงถึงร้าน' }))
      .toBeVisible()
    await page.getByRole('link', { name: 'เลือกสินค้าตามหมวด' }).click()
    await expect(page).toHaveURL(/\/shop/)
    await expect(page.getByRole('searchbox', { name: 'ค้นหาสินค้า' })).toBeVisible()
  })
  ```

- [ ] **Step 2: Run the test and observe its failure against the kit’s placeholder home screen.**

  ```bash
  npm run test:e2e -- e2e/supplymate-wholesale.spec.ts
  ```

- [ ] **Step 3: Extract the current `Home` function from `App.tsx` into `HomePage.tsx`.**

  The new page must contain, in this order:

  ```tsx
  <section aria-labelledby="home-title">...</section>
  <section aria-labelledby="category-title">...</section>
  <section aria-labelledby="operations-title">...</section>
  ```

  The first section uses the exact heading in Step 1 and a `<Link to="/shop">เลือกสินค้าตามหมวด</Link>`. The category section maps actual `useCategories()` data to links. The operations section contains only factual demo content: `ขั้นต่ำเริ่ม 1 ลัง`, `ชำระเงินด้วยการโอน`, and `ติดตามสถานะหลังสั่งซื้อ`.

- [ ] **Step 4: Convert navigation and catalogue labels to Thai without changing query behavior.**

  In `SiteHeader`, use `สินค้า`, `ตะกร้า`, `คำสั่งซื้อ`, `บัญชี`, `หลังบ้าน`, and `เข้าสู่ระบบ`. In `ProductListPage`, give the `<Input>` an explicit `aria-label="ค้นหาสินค้า"`, retain `q`, `category`, and `page` URL parameters, and change the category/filter/loading/error copy to Thai. Do not alter the `useProducts` query key or its `enabled` guard.

- [ ] **Step 5: Apply only global SupplyMate tokens in `src/index.css`.**

  Set neutral warehouse-like background/card/border values and map primary to the configured navy through `--brand-primary`; use readable Thai system fonts as fallback. Do not create per-page selectors in this global file and do not use a dark-mode toggle in the demo.

- [ ] **Step 6: Run the full application quality gate and commit.**

  ```bash
  npm run test:e2e -- e2e/supplymate-wholesale.spec.ts
  npm run typecheck
  npm run lint
  npm run build
  git add src/core/catalog/HomePage.tsx src/App.tsx src/components/SiteHeader.tsx \
    src/core/catalog/ProductListPage.tsx src/index.css e2e/supplymate-wholesale.spec.ts
  git commit -m "feat: build Thai SupplyMate storefront"
  ```

## Task 6: Capture business checkout details and make fulfilment status understandable

**Files:**

- Modify: `src/core/checkout/CheckoutPage.tsx`
- Modify: `src/core/orders/OrderDetailPage.tsx`
- Modify: `src/core/admin/AdminOrderDetailPage.tsx`
- Modify: `src/core/admin/useAdminOrderMutations.ts`
- Modify: `e2e/golden-path.spec.ts`
- Modify: `e2e/supplymate-wholesale.spec.ts`

**Interfaces:**

- `CheckoutPage` calls `create_order` with `p_business_details: { business_name, tax_id, branch_name }`.
- `useAdminOrderMutations().rejectSlip` accepts `{ reason: string }`; callers may not reject a slip without a non-empty reason.
- `OrderDetailPage` reads `tracking_number`, `shipping_carrier`, `cancel_reason`, and `payment_rejection_reason` directly from the order row; it does not leak the private slip path.

- [ ] **Step 1: Extend the golden path with the customer-visible completion contract.**

  Replace the final assertion in `e2e/golden-path.spec.ts` with:

  ```ts
  await customerPage.goto(orderUrl)
  await expect(customerPage.getByText('จัดส่งแล้ว')).toBeVisible()
  await expect(customerPage.getByText('Thailand Post · TH1234567890')).toBeVisible()
  await expect(customerPage.getByText('คำสั่งซื้อเสร็จสมบูรณ์')).toBeVisible()
  ```

  Add a second test that uploads a slip, has the admin reject it with `ยอดโอนไม่ตรง`, and confirms the customer sees that reason and the re-upload input.

- [ ] **Step 2: Run the targeted Playwright tests and verify they fail.**

  ```bash
  npm run test:e2e -- e2e/golden-path.spec.ts e2e/supplymate-wholesale.spec.ts
  ```

- [ ] **Step 3: Add validated business details to checkout and the RPC call.**

  Use component state with this exact shape:

  ```ts
  const [businessDetails, setBusinessDetails] = useState({
    business_name: '',
    tax_id: '',
    branch_name: '',
  })
  ```

  Render a fieldset headed `ข้อมูลสำหรับธุรกิจ`; make `business_name` required and label the inputs `ชื่อร้านหรือบริษัท`, `เลขประจำตัวผู้เสียภาษี`, and `สาขา`. In the existing mutation, pass:

  ```ts
  p_business_details: businessDetails,
  ```

  Keep `p_address_id`, `p_items`, and `p_promo_code` unchanged. Disable the order button while `business_name.trim()` is empty.

- [ ] **Step 4: Make customer status specific, readable, and action-oriented.**

  In `OrderDetailPage`, use a local exhaustive map:

  ```ts
  const orderStatusLabel = {
    pending: 'รอตรวจสอบการชำระเงิน',
    verified: 'ตรวจสอบการชำระเงินแล้ว',
    shipped: 'จัดส่งแล้ว',
    done: 'คำสั่งซื้อเสร็จสมบูรณ์',
    cancelled: 'ยกเลิกคำสั่งซื้อ',
  } as const
  ```

  Render the carrier/tracking block whenever both fields exist. Render `payment_rejection_reason` as an alert before the pending re-upload form. Render `cancel_reason` only for a cancelled order. Keep file validation and the private upload path format untouched.

- [ ] **Step 5: Require and persist a payment-rejection explanation in the admin workflow.**

  Give `AdminOrderDetailPage` a labelled input `เหตุผลที่ให้แนบสลิปใหม่`. Disable `Reject slip` until it contains trimmed text. Update the mutation call to send the value in the update that also transitions `verified -> pending`, clears `payment_slip_path`, and clears `payment_slip_uploaded_at`. Do not reuse `payment_note`, because it belongs to buyer-provided transfer context.

- [ ] **Step 6: Show the immutable business snapshot to the admin.**

  Add a `ข้อมูลธุรกิจผู้สั่งซื้อ` card below the customer card in `AdminOrderDetailPage`. Render business name always when present; render tax ID and branch only when non-null. The card is display-only; no admin edit control is allowed.

- [ ] **Step 7: Run the end-to-end path and commit.**

  ```bash
  npm run test:e2e -- e2e/golden-path.spec.ts e2e/supplymate-wholesale.spec.ts
  npm run typecheck
  npm run lint
  git add src/core/checkout/CheckoutPage.tsx src/core/orders/OrderDetailPage.tsx \
    src/core/admin/AdminOrderDetailPage.tsx src/core/admin/useAdminOrderMutations.ts \
    e2e/golden-path.spec.ts e2e/supplymate-wholesale.spec.ts
  git commit -m "feat: complete SupplyMate business checkout flow"
  ```

## Task 7: Verify, deploy, and capture the live demo

**Files:**

- Modify: `README.md`
- Modify: `vercel.json` only if the existing SPA rewrite does not already work in preview
- Create: `docs/demo-accounts.md` (private repository documentation)

**Interfaces:**

- Consumes: a Supabase project owned for this showcase and Vercel environment variables `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY`.
- Produces: a live URL with separate buyer/admin demonstration accounts and no committed credentials.

- [ ] **Step 1: Write a deployment smoke-test list before deploying.**

  Add these exact checks to `README.md`:

  ```markdown
  ## Pre-deploy smoke test

  1. Browse a local product, add one permitted pack, and complete checkout with a business name.
  2. Upload the fixture slip as the buyer.
  3. Verify, ship with a carrier/tracking number, and complete it as admin.
  4. Reopen the buyer order and verify status, tracking, and reasons render in Thai.
  5. Load `/admin` while signed out and confirm redirection to `/login`.
  ```

- [ ] **Step 2: Execute the clean-database test suite.**

  ```bash
  supabase start
  supabase db reset --yes
  npm run typecheck
  npm run lint
  npm run build
  npm run test:e2e
  ```

  Expected: all commands pass. If Docker/Supabase is unavailable, record the exact unavailable command in the commit/hand-off and still run typecheck, lint, build, plus manual UI verification against a configured owned Supabase project.

- [ ] **Step 3: Configure owned hosted Supabase and Vercel environments without committing secrets.**

  Apply the reviewed migrations to a new owned Supabase project, create a demo admin through the Auth flow, promote that profile using the documented one-time SQL, and load only the owned demo catalogue. Set Vercel variables in the Vercel dashboard/CLI environment, never `.env` tracked files.

- [ ] **Step 4: Deploy and run the buyer/admin smoke path on the deployment.**

  Confirm every route reloads directly: `/`, `/shop`, `/products/clear-cup-16oz`, `/cart`, `/checkout`, `/orders/:id`, and `/admin/orders/:id`. At 375×812, verify `document.documentElement.scrollWidth === document.documentElement.clientWidth` and inspect the browser console for errors.

- [ ] **Step 5: Capture an honest showcase screenshot and commit deployment documentation.**

  Capture `assets/screenshots/showcase-supplymate.jpg` only from the final deployed SupplyMate screen; do not alter it to imply a real client. Record the live URL, demo-account access policy, and smoke-test date in `docs/demo-accounts.md` without placing credentials in the document.

  ```bash
  git add README.md docs/demo-accounts.md
  git commit -m "docs: record SupplyMate deployment verification"
  ```

## Task 8 completion note — 2026-08-08

Task 8 was executed on `main` on 2026-08-08, after the app had already shipped. Three points
where the plan above no longer matched reality, and what was done instead:

- **The deployed demo is the static showcase build, not the admin/slip-upload build this
  plan describes.** `#/`, `#/shop`, `#/products/:slug`, `#/cart` and a simulated `#/checkout`,
  browser-only cart, no network calls, no login and no back office. Verified by walking the
  live site before writing a word of the showcase page. So the showcase copy describes only
  that, and Step 4's suggested `หลังบ้านออเดอร์` tag was **dropped** — it would have claimed a
  back office that is not there. Tags shipped: `ขายส่ง` / `สั่งเป็นลัง` / `บรรจุภัณฑ์`.
- **Step 5's `python3 -m http.server 8123` no longer serves this site.** Extensionless URLs
  mean every internal link 404s under it; `python3 _tools/serve.py 8123` is the replacement.
  Its Lighthouse URL also drops the `.html`.
- **Step 5's "verify `site-ui.js` is only present on home-shell pages" is obsolete.** Since
  `ee2f9fe` all 64 selling pages load it, showcases included, and the new pair does too.

Also corrected while here: the static `.filter-count` fallbacks in all four grid files had
been stale by one since the RAAT card was added (`all 13 / other 2` against a DOM of 14 / 3).
They are now `all 15 / other 3`. `work.html` / `work-en.html` prose counts went 13 to 14.

Left alone deliberately: `resume.html` / `resume-en.html` still say 13 projects. That line is
about "standalone HTML/CSS/JS projects ... curated down to the 13 strongest", and SupplyMate
is a React + Vite app in its own repository, so 13 is arguably still correct there. Owner's
call, not a silent edit.

## Task 8: Add the verified demo to the bilingual static portfolio

**Files:**

- Create: `showcase-supplymate.html`
- Create: `showcase-supplymate-en.html`
- Create: `assets/thumbs/supplymate.svg`
- Create: `assets/screenshots/showcase-supplymate.jpg`
- Modify: `index.html`
- Modify: `index-en.html`
- Modify: `work.html`
- Modify: `work-en.html`
- Modify: `sitemap.xml`
- Modify: `assets/search-index.json`

**Interfaces:**

- Consumes: the verified live SupplyMate deployment, honest screenshot, and the portfolio’s existing showcase/story-stack layout.
- Produces: two self-canonical showcase pages with the Thai-default hreflang trio, in-language links, analytics, search indexing, and one card per language/grid.

- [x] **Step 1: Invoke the `portfolio-add-card` skill before touching the four project grids.**

  Inspect the final demo at natural thumbnail size. Derive `assets/thumbs/supplymate.svg` from actual SupplyMate layout/measurements; do not use generated product images or an arbitrary stock-style thumbnail. Set its `data-industry="shop"` only on the canonical project card, never on featured-carousel clones.

- [x] **Step 2: Create the Thai/English showcase pair from an existing current showcase skeleton.**

  Each page needs a self-referential canonical, `og:locale` (`th_TH` / `en_US`), the same Thai-default `hreflang` trio, and `<script src="assets/analytics.js" defer></script>` before `</head>`. Use the four story cards in order: project overview, 30-second version, who it fits, and the ask. State `โปรเจกต์แนวคิดที่พัฒนาขึ้นเอง` / `self-initiated concept project` in the overview.

- [x] **Step 3: Link only to verified experience.**

  Use the deployed SupplyMate URL for `ดูเว็บจริง` / `View live site`, the actual `showcase-supplymate.jpg` for the hero image, and no fabricated metrics or review quotes. Make both project cards link to their respective showcase sibling, not directly to the demo.

- [x] **Step 4: Add cards to all four grids and both search-index language arrays.**

  Add SupplyMate after the existing shopping examples with Thai buyer tags such as `ขายส่ง`, `สั่งเป็นลัง`, `หลังบ้านออเดอร์`; use English equivalents in English pages while retaining `data-industry="shop"`. Add concise searchable keywords for both `ขายส่ง` and `wholesale` in `assets/search-index.json`.

- [x] **Step 5: Update sitemap and run portfolio integrity checks.**

  Add both showcase URLs to `sitemap.xml`. Then run:

  ```bash
  rg -n "showcase-supplymate|supplymate" index.html index-en.html work.html work-en.html sitemap.xml assets/search-index.json
  python3 -m http.server 8123 &
  npx -y lighthouse http://localhost:8123/showcase-supplymate.html --quiet --chrome-flags="--headless" --output=json --output-path=/tmp/lh-supplymate.json
  ```

  Check the Thai and English pages at 375×812 for horizontal overflow. Verify `site-ui.js` is only present on home-shell pages and that the showcase pages load only `portfolio-pages.css`.

- [x] **Step 6: Commit the portfolio hand-off.**

  ```bash
  git add showcase-supplymate.html showcase-supplymate-en.html assets/thumbs/supplymate.svg \
    assets/screenshots/showcase-supplymate.jpg index.html index-en.html work.html work-en.html \
    sitemap.xml assets/search-index.json
  git commit -m "feat: showcase SupplyMate wholesale commerce"
  ```

## Plan Self-Review

| Spec requirement | Plan coverage |
|---|---|
| B2B pack/MOQ details | Tasks 3–4 |
| Customer storefront and Thai copy | Tasks 1, 4–5 |
| Business checkout snapshot | Tasks 3 and 6 |
| Private slips and safe fulfilment | Tasks 3 and 6 |
| Buyer-visible tracking/rejection/cancellation state | Task 6 |
| Admin operations | Tasks 4 and 6 |
| Own/generated visual assets | Task 2 |
| Clean deployment with demo-only data | Task 7 |
| Honest bilingual portfolio integration | Task 8 |
| Type/lint/build/E2E/mobile verification | Tasks 1, 3–8 |

The plan deliberately omits live payment processing, courier APIs, tax invoice PDFs, multi-warehouse stock, B2B tiered pricing, and quote-to-sales workflows. They would increase implementation surface without adding proportionate proof for the first showcase release.
