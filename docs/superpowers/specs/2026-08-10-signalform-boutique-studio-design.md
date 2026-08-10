# Signalform Boutique Studio Design

## Goal

Turn Signalform Studio from a short interactive concept into a credible independent digital studio website. The site must communicate what the studio does, demonstrate how it works, establish trust without invented claims, and make starting a project simple.

## Audience

Founders and small teams who need a distinctive brand website or digital experience, and who want a direct collaboration with an independent designer-developer rather than a large agency.

## Positioning and voice

Signalform is an independent boutique studio for brand systems, expressive websites, and purposeful interaction design. The voice is precise, calm, and direct. It does not claim a team size, client count, awards, revenue impact, or fabricated client relationship.

## Information architecture

The existing one-page React application remains a single static route at `/signalform-studio/`. The header exposes anchors for Work, Services, Process, and Contact. The page is ordered as follows:

1. **Hero** — concise positioning, a primary `Start a project` action, and a secondary link to services. Keep the existing original cobalt sculpture and Signalform wordmark.
2. **Trust strip** — three factual principles: direct senior collaboration, a defined four-step process, and performance-conscious static delivery. These are principles, not quantified business claims.
3. **Services** — three selectable React Bits SpotlightCards for Brand systems, Web experiences, and Interaction direction. Each card names its concrete deliverables and directs prospective clients to request a scoped estimate rather than promising a fixed price.
4. **Selected work** — three compact case-study cards. Each card is explicitly labelled `Self-initiated concept` when it is not client work. The selected work links to existing live portfolio demos or showcases only.
5. **Process** — Discover, Define, Design, Build. Each step states the collaborative output that a prospective client receives.
6. **Testimonial** — use only a verified Fastwork review already published on the portfolio. It must preserve the original reviewer wording and source link. If a suitable verified review cannot be used, omit this section rather than creating a quote.
7. **FAQ** — four questions: engagement fit, timeline, what a client needs to provide, and how to start.
8. **Project enquiry** — name, email, company or project, budget range, and a short brief. Submit validates fields then opens a mailto draft addressed to `a0626568471@gmail.com`. It has no server-side data collection and says so plainly.
9. **Footer** — Signalform name, actual email, GitHub, LinkedIn, and a clear `View Phakin's portfolio` link.

## Content integrity

- Use `Phakin Chawanpunya` and the real contact destinations already defined in the portfolio.
- Link selected work to the real Signalform showcase, SupplyMate showcase, and HabitQuest demo or showcase.
- Mark self-initiated work visibly. Do not describe it as client delivery.
- Testimonial text and attribution must be copied from an existing verified Fastwork review. No generated reviews, client logos, success metrics, or awards.
- Every live action uses a real destination: mailto, Fastwork, GitHub, LinkedIn, portfolio, or a published demo.

## Component boundaries

`src/content.js` becomes the single source for services, work cards, process steps, FAQs, and contact constants. `App.jsx` composes semantic page sections from this content. Focused components keep responsibilities narrow:

- `SpotlightCard.jsx` continues to own pointer-driven visual treatment only.
- `SectionHeading.jsx` renders a shared eyebrow and heading pair.
- `WorkCard.jsx` renders a case-study link and transparent work label.
- `FaqItem.jsx` renders a keyboard-accessible native `details` and `summary` item.
- `EnquiryForm.jsx` owns field state, client validation, user-visible validation messages, and mailto creation.

No router, database, CMS, analytics SDK, or form service is added. Vite still emits a static GitHub Pages build.

## Interaction and accessibility

- Spotlight effects remain decorative and work cards are ordinary focusable links.
- Service selection updates an adjacent explanatory panel and keeps correct `aria-pressed` state.
- FAQ uses native disclosure controls.
- Form labels stay visible, errors are announced through an `aria-live` status area, invalid controls receive `aria-invalid`, and valid submission opens the mail client only after validation.
- Existing reduced-motion styles remove nonessential movement.
- All imagery carries meaningful alt text or is decorative with empty alt text.
- Maintain no horizontal overflow at 375px width.

## Error handling

The contact form never sends data silently. Empty name, invalid email, empty brief, or an unselected budget prevents mailto navigation, highlights the matching control, and announces a concise error. If `window.location.href` cannot open a mail client, the confirmation copy exposes the email address as a manual fallback.

## Acceptance criteria

1. The page contains every specified section except testimonial, which is conditional on verified source content.
2. Every project claim and destination is verifiable from the existing portfolio or public profile.
3. Services, work links, FAQ disclosure, service selection, and valid/invalid enquiry handling are covered by Vitest and Testing Library.
4. `npm test` and `npm run build` pass.
5. Lighthouse on the built demo remains 95 or higher for Performance and 100 for Accessibility, Best Practices, and SEO.
6. The page has no horizontal overflow at a 375px viewport with JavaScript enabled.
