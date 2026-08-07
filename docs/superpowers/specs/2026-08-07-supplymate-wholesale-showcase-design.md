# SupplyMate Wholesale Showcase Design

**Status:** Approved for specification review  
**Date:** 2026-08-07  
**Goal:** Turn the existing `Phakinza007/ecom` starter kit into a credible, end-to-end B2B wholesale-commerce demo that helps win Fastwork web and dashboard work.

## 1. Product decision

SupplyMate Wholesale is a fictional Thai supplier of packaging and café consumables. It sells items such as cups, lids, paper bags, food containers, labels, and drink supplies in case quantities to cafés, restaurants, and small retailers.

It is a **self-initiated concept**, not a client project. The public showcase will state that accurately and will not use invented clients, testimonials, sales figures, or claims of live commercial use. The experience should nevertheless behave like a small business would expect: Thai copy, realistic stock-keeping units, clear carton quantities, business checkout details, payment-slip handling, and an owner-facing order workflow.

This direction is deliberately different from the portfolio's existing general e-commerce and game top-up examples. It demonstrates the two audiences a business owner pays for:

1. A buyer can find packaged goods, understand the ordering unit and minimum quantity, pay, and follow an order.
2. A store owner can maintain the catalogue, verify a payment slip, and move orders through fulfilment.

## 2. Success criteria

The finished demo must let a reviewer complete the following believable path without encountering placeholder interfaces:

```text
Home → category / search → product → add a carton to cart → checkout
     → payment-slip upload → order status
                                 ↓
                  admin verifies payment → ships → completes order
```

The visible proof points are:

- B2B order language: per-case price, pieces per carton, minimum quantity, availability, and VAT-ready business details.
- A practical Thai mobile storefront, not a generic dashboard skin.
- A separate, protected admin experience with products, categories, orders, promotions, and clear status controls.
- A deployment that prospective Fastwork customers can click through, with seeded data and documented demo accounts rather than a dead visual mockup.

## 3. Technical foundation and boundaries

SupplyMate will be a separately branded project derived from `Phakinza007/ecom`. The static portfolio site will link to its deployed URL; it will not absorb the React application or its dependencies.

The existing stack remains in place:

- React + Vite + TypeScript
- Tailwind + shadcn/ui
- Supabase Auth, Postgres, Storage, and Row Level Security
- TanStack Query, Zustand, React Router
- Vercel deployment

The existing core capabilities are reused rather than replaced: public catalogue, product variants, cart, checkout with payment-slip upload, customer profile and address book, order history, admin product/category CRUD, and admin order fulfilment. Existing optional modules for variants, promotions, reviews, and LINE notification remain feature-flagged.

Core security behavior stays intact: client totals are re-priced by the server-side checkout RPC, payment slips remain private storage assets, and admin routes stay protected by role-aware database policies. No production customer data or actual payment credentials will be used in the demo.

## 4. Brand and content

### Brand

- **Name:** SupplyMate Wholesale
- **Positioning:** "ของใช้ร้านอาหารและคาเฟ่ สั่งเป็นลัง ส่งตรงถึงร้าน"
- **Voice:** Direct, dependable, operational; short Thai labels and no exaggerated marketing claims.
- **Visual character:** Ink/navy base, warm off-white surfaces, safety-green order states, and a restrained orange highlight for action or low-stock information. The interface is denser and more utilitarian than a beauty or fashion shop.

### Seed catalogue

Six realistic categories will contain approximately 18–24 products:

1. แก้วและฝา
2. กล่องอาหารและช้อนส้อม
3. ถุงและบรรจุภัณฑ์กระดาษ
4. สติ๊กเกอร์และฉลาก
5. อุปกรณ์เครื่องดื่ม
6. สินค้ารักษ์โลก

Every product gets a plausible SKU, pack or carton unit, pieces-per-carton amount, price, image, availability, and a short practical description. Variants should reflect a real purchase decision, such as cup size, lid type, material, or carton count. Seeded reviews, if enabled, must be clearly generic product feedback and not presented as verified testimonials from actual people; the default showcase may instead omit reviews entirely.

## 5. Customer experience

### Public storefront

The home page prioritizes an immediate path to the catalogue rather than a decorative hero:

- Compact value proposition with a primary “เลือกสินค้าตามหมวด” action.
- Category shortcuts and a small operational trust strip: minimum order, delivery cutoff, and payment method.
- A restock/bundle section using real seeded products, not made-up sales claims.
- An assistance panel that explains how businesses request help without pretending to provide live support.

The shop page uses URL-backed category, search, and pagination state already supported by the starter kit. Product cards show the case price, ordering unit, and availability before the user opens a product page.

### Product and cart

Each product page must make the order unit unambiguous:

- carton or pack label, pieces per carton, SKU, and product variant selection;
- minimum purchase quantity; and
- a concise delivery/returns note appropriate to non-perishable supplies.

The cart must retain the existing server-safe checkout model. Its summary will clarify that prices are per ordering unit and show the number of cartons, items, and total payable. Promotion code support remains available only if it is enabled and seeded with a valid demo code; no permanently visible fake discount is allowed.

### Checkout and order tracking

Checkout reuses address selection and payment-slip upload. The form gains only the business details essential to the showcase: company/shop name, optional tax ID, and branch field. These values must be recorded with the order's immutable address/business snapshot so they remain accurate after a profile edit.

The confirmation and order-detail views use understandable Thai status language for `pending`, payment verified, shipped, completed, and cancelled. Where the source kit currently has a known gap, this work will surface the carrier, tracking number, and cancellation/rejection note to the customer rather than leave the buyer unsure what happened.

## 6. Admin experience

The admin area is a concise operating console, not a second marketing site.

- **Products and categories:** Add/edit/archive catalogue items, images, SKUs, packing information, and availability.
- **Orders:** Filter orders by payment and fulfilment state; see buyer and business details; safely verify or reject a payment slip; attach carrier/tracking information; ship, complete, or cancel according to the existing database transition rules.
- **Promotions:** Manage a limited set of valid demo promotions if the optional module is enabled.

The existing deactivate-rather-than-delete convention is retained. No new live inventory reservation, courier API, VAT invoice PDF, multi-warehouse, or multi-tenant functionality enters the first release; those are separate client-specific integrations rather than proof required for this showcase.

## 7. Data and error behavior

Existing database/RLS patterns remain the source of truth. New fields for business details and pack metadata require a migration, generated TypeScript database types, seed updates, and UI validation. Input errors must be specific and preserve entered data; failed catalogue or order requests must render an explicit error state rather than an empty screen.

Key non-happy paths to preserve or cover:

- Item becomes unavailable or its server-side price changes before checkout.
- A buyer uploads an invalid or rejected payment slip.
- A non-admin attempts to open an admin URL.
- An order status change is invalid or fails.
- A private payment slip cannot be accessed by a different buyer.

## 8. Build sequence

1. Create a dedicated SupplyMate working copy from `ecom`; set local Supabase/Vercel environment variables without committing secrets.
2. Audit the base project, run its existing typecheck/lint/build, and bring the working baseline to green before branding changes.
3. Implement brand configuration, Thai storefront copy, responsive layout, and a realistic seeded catalogue.
4. Add pack metadata and business checkout/order fields through a migration, query/type updates, validation, and seeds.
5. Complete buyer-facing order-status visibility for tracking/carrier and rejection/cancellation reasons.
6. Tune the admin views so order fulfilment exposes the new business/order fields without weakening access control.
7. Extend focused unit/integration tests and end-to-end coverage for the wholesale golden path; then run responsive and accessibility checks.
8. Deploy the demo with safe, documented sample accounts. Verify buyer and admin paths independently on the deployed app.
9. Create Thai and English portfolio showcase pages only after the live demo is verified. Add the new project card to `index.html`, `index-en.html`, `work.html`, and `work-en.html`, using an SVG thumbnail; add bilingual sitemap/search-index entries and validate the site's language, accessibility, and 375px overflow rules.

## 9. Explicit non-goals for this showcase

- No fabricated client relationship, revenue, testimonials, live stock level, or delivery promise.
- No payment-gateway integration or real bank account.
- No customer-data collection outside testing accounts.
- No external courier, accounting, ERP, or LINE OA production integration.
- No duplicate static version of the React app inside the portfolio repository.

## 10. Verification

Before presenting it as a portfolio project:

- `npm run typecheck`, `npm run lint`, and `npm run build` pass in the SupplyMate project.
- Relevant unit/integration tests and the local-Supabase E2E suite pass where the environment supports them.
- The buyer happy path and the admin fulfilment path are manually verified with distinct demo accounts.
- The deployed page works at 375px without horizontal scrolling and has no console errors.
- The portfolio additions preserve Thai/English alternate links, self canonicals, site search entries, analytics tags, and Lighthouse/overflow expectations.

