# Handoff — ARIA Research App — Mar 24, 2026

## Session Summary
Took ARIA from v1.3 to v2.2.0 — production-ready paid SaaS. Completed full security audit (40+ fixes), iOS optimization, premium UI polish, AI quality upgrades, Google sign-in, admin panel with analytics, Stripe paywall, and custom domain deployment to researcharia.com.

**Repo:** https://github.com/nhouseholder/aria-research
**Live:** https://researcharia.com
**Admin:** nikhouseholdr@gmail.com (role=admin)

## What Was Done

### v2.0.0 — Production Security Audit
- Full RS256 JWT signature verification (was claims-only) → `src/middleware/auth.ts`
- CORS locked to researcharia.com (was `origin: '*'`) → `src/index.ts`
- XSS sanitization on all paper/metadata content → `public/app.js`
- Stripe webhook returns 500 on error (was swallowing with 200) → `src/routes/subscription.ts`
- Gemini API key moved to header (was in URL params) → `src/services/ai.ts`
- Constant-time webhook HMAC comparison → `src/lib/stripe.ts`
- Rate limiting on all AI endpoints → `src/middleware/rateLimit.ts`
- Chat delete ownership verification → `src/routes/chat.ts`
- Subscription cancel grace period → `src/middleware/subscription.ts`
- Toast notification system replacing all alert() → `public/app.js`
- SEO meta tags, favicon → `public/index.html`
- DB migration 0004: UNIQUE(user_id, pmid), enrichment + stripe indexes

### v2.1.0 — AI Quality + Premium UI
- Section-specific writing prompts (specific aims, abstract, lit review, methods, intro, discussion) → `src/routes/writing.ts`
- Chat: stop word filtering, follow-up questions, uncertainty admission → `src/routes/chat.ts`
- Enrichment: publication_type + evidence_level, markdown fence stripping → `src/services/enrichment.ts`
- Gemini 429/503 retry with 1.5s backoff → `src/services/ai.ts`
- Cron batch dedup, enrichment limit 5/user → `src/index.ts`
- Dashboard slim query (80% smaller) → `src/index.ts`
- Landing: above-fold CTA, social proof, pricing badge → `public/index.html`
- Button active states, stat card accents, chat bubbles, sidebar indicator → `public/styles.css`
- Paywall loss-aversion, skeleton loading, focus-visible → `public/styles.css`

### v2.2.0 — Google Sign-In, Admin, Analytics
- Google sign-in (Firebase popup) on login + signup → `public/index.html` + `public/app.js`
- Admin role system → `migrations/0005_admin_analytics.sql`
- Admin panel: user table, stats, activity → `src/routes/admin.ts` + `public/*`
- Usage analytics (login, page_view, chat, writing, sync) → `src/routes/analytics.ts`

### Infrastructure
- Custom domain: researcharia.com + www (Cloudflare Workers Custom Domains)
- Firebase: Email/Password + Google enabled, 3 domains whitelisted
- Stripe: Live webhook (we_1TEa7MQBM4GMGA1HxEPJJg4d)
- Secrets: STRIPE_SECRET_KEY, STRIPE_WEBHOOK_SECRET, GEMINI_API_KEY
- D1: aria-db (e9260202-0887-465c-8dd3-600fe8c1899a), 5 migrations

## What's Left To Do
- **Digest caching**: Regenerates on every request. Add `digest_cache` table, cache per user/day.
- **Writing history click-to-reload**: Items not clickable to view past content.
- **Markdown parser**: Naive `markdownToHTML()`. Consider marked.js for code blocks/tables.
- **PubMed year parsing**: May grab DateRevised year. Fix to use PubDate block.
- **Methodology scoring**: Hardcoded 50 in scoring.ts. Should use user preference.
- **Password minlength**: HTML=8, Firebase=6. Pick one.
- **Chat delete UI**: No delete button on conversations.
- **Pagination truncation**: No ellipsis for large page counts.
- **Mobile overlay close**: ::after can't receive clicks. Add real overlay div.

## Key Decisions
- Firebase Auth + D1 for app data. JWT verified with Google X.509 keys.
- Gemini 2.0 Flash primary, Llama 3.1 8B fallback.
- Vanilla JS frontend (no framework). Single-page app, static files.
- D1 for everything (papers, users, chat, writing, analytics).
- In-memory rate limiter (resets on Worker recycling). Switch to D1 if abused.
- Admin by email match in SQL migration.

## Gotchas for Next Agent
- **Clone to /tmp**: `git clone https://github.com/nhouseholder/aria-research.git /tmp/aria-research`
- **Never push from iCloud** — git operations fail in iCloud Drive
- **Deploy**: `cd /tmp/aria-research && npm install && npx wrangler deploy`
- **Secrets NOT in wrangler.toml** — set via `npx wrangler secret put`
- **Version string in 3 places** in index.html (mobile header, sidebar-version, sidebar-footer)
- **Rate limiter** is in-memory, resets on isolate recycle

## Current State
- Branch: `main`
- Last commit: `6318cfe` v2.2.0
- Build: passing
- Deploy: live at researcharia.com
- Version: v2.2.0 · Mar 24, 2026
