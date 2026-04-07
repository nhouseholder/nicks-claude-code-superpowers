# Handoff — Residency-app — 2026-04-03 00:05
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: handoff_Residency-app_2026-03-31_1415.md
## GitHub repo: nhouseholder/Residency-app
## Local path: ~/ProjectsHQ/Residency-app/
## Last commit date: 2026-04-01 19:01:13 -0700

---

## 1. Session Summary
Nicholas wanted to address the top recommendations from /whats-next: retry/fallback for OpenRouter 429s, analysis caching, AI unit tests, version bump, server-side cache, health check endpoint, and Cloudflare deployment. All code tasks were completed and 8 commits pushed. The app was deployed to Cloudflare Workers at https://residency-app.nikhouseholdr.workers.dev. Epic OAuth sandbox testing was attempted but blocked by an Epic account-level error ("An error occurred while updating your account") that prevented saving the redirect URI at fhir.epic.com.

## 2. What Was Done
- **Retry/fallback chain**: Added 3-retry exponential backoff with 3-model fallback (Nemotron → Qwen → Gemma) per tier in `src/lib/ai/provider.ts`
- **extractJSON fix**: Changed to pick whichever delimiter ({/[) appears first, fixing array extraction from mixed LLM output
- **Client-side analysis cache**: sessionStorage-backed 30min TTL cache in `src/app/command-center/page.tsx` — Refresh buttons bypass cache
- **23 AI unit tests**: `src/__tests__/provider.test.ts` — extractJSON (8), repairJSON (6), OpenRouterProvider retry/fallback (9)
- **Version bump to v0.2.0**: Phase 2 complete milestone
- **Project CLAUDE.md**: Documented stack, dev setup, architecture, known quirks
- **Server-side analysis cache**: `src/lib/ai/analysis-cache.ts` — in-memory Map with 30min TTL, wired into `/api/ai/analyze` route with `refresh` parameter
- **Model health check**: `/api/ai/health` endpoint pings all 3 free OpenRouter models in parallel, reports latency, recommends fastest
- **FHIR scopes fix**: Changed from abbreviated `.r`/`.rs` to full `.read` format (Epic requires this)
- **Callback page fix**: Removed `useSearchParams()` (broken in Next.js 16 streaming), reads directly from `window.location.search`
- **Cloudflare deployment**: OpenNext adapter, KV session storage (async API), Workers deploy with static asset binding
- **Session store migration**: All session functions now async with KV + in-memory fallback — updated 8 API routes + tests
- **Non-Production Client ID**: Discovered app had TWO client IDs — switched to sandbox-specific `c589a1c6-c5f6-485e-b099-b4992a5ee555`

## 3. What Failed (And Why)
- **Epic OAuth "Something went wrong trying to authorize the client"**: Root cause was abbreviated FHIR scopes (`.r` instead of `.read`). Fixed.
- **Epic OAuth "Missing authorization code or state parameter"**: `useSearchParams()` returns empty during Next.js 16 streaming hydration. Fixed by reading from `window.location.search`.
- **Epic OAuth "Invalid OAuth 2.0 request"**: Using production Client ID against sandbox. Fixed by switching to Non-Production Client ID.
- **Epic account save error**: "An error occurred while updating your account" — hidden error on fhir.epic.com preventing redirect URI save. This is an Epic account-level issue, NOT a code bug. STILL BLOCKING.
- **Cloudflare Pages 404 on static assets**: `_worker.js` advanced mode intercepted all requests, CSS/JS returned 404. Fixed by switching to Workers deploy with `assets` binding.
- **OpenNext build missing esbuild**: Peer dependency not auto-installed. Fixed with `npm install --save-dev esbuild`.

## 4. What Worked Well
- **Multi-model fallback architecture**: The retry + fallback chain in provider.ts is clean and testable
- **Health check endpoint**: Live-tested against OpenRouter — Nemotron 512ms, Qwen 953ms, Gemma 429'd. Auto-recommends fastest.
- **Workers deploy with assets binding**: Correctly serves both static assets and SSR from a single Cloudflare Worker
- **KV session store with in-memory fallback**: Async API works on both Workers (KV) and local dev (Map) transparently

## 5. What The User Wants
Nicholas wants the Epic SMART on FHIR OAuth flow working end-to-end so he can test the full clinical pipeline (census → analyze → notes → chat) before his internship. He's been patient through multiple OAuth debugging iterations but is frustrated by the Epic account error blocking progress.
- Gave API keys directly: "DO NOT LOSE THIS KEY, you already lost my other key"
- Wanted browser help: "use claude in chrome to help me set this up"
- Still wants E2E working: the whole session was building toward a functioning OAuth flow

## 6. In Progress (Unfinished)
- **Epic OAuth redirect URI registration**: The redirect URI `https://residency-app.nikhouseholdr.workers.dev/callback` needs to be saved at fhir.epic.com (appId=52745). Epic's save function is returning "An error occurred while updating your account." Options: (1) create a new app at fhir.epic.com, (2) email fhir@epic.com for support, (3) try a different browser/clear cache.
- **Full E2E test**: Cannot complete until OAuth redirect URI is registered with Epic.

## 7. Blocked / Waiting On
- **Epic account-level error**: fhir.epic.com returns "An error occurred while updating your account" when trying to save app settings. This prevents registering the Cloudflare redirect URI. User needs to either create a new app or contact Epic support.

## 8. Next Steps (Prioritized)
1. **Fix Epic app registration** — Create a NEW app at fhir.epic.com with the correct redirect URI from the start (`https://residency-app.nikhouseholdr.workers.dev/callback`). Update the Client ID in `.env.local` and Cloudflare secrets. This unblocks everything.
2. **Complete E2E browser test** — Once OAuth works: launch → Epic login → callback → command center → add patient → analyze → deep dive
3. **Add tests for remaining AI modules** — clinical-analyzer.ts (183 lines), note-generator.ts (143 lines), research.ts (113 lines) have zero test coverage
4. **Polish Command Center UX** — Loading skeletons, sparkline wiring, mobile horizontal scroll

## 9. Agent Observations
### Recommendations
- The Non-Production Client ID (`c589a1c6-c5f6-485e-b099-b4992a5ee555`) must be used for sandbox testing. The Production Client ID (`b551e03c-db22-4e46-a3d6-a86402a64e01`) is for production Epic endpoints only.
- Consider adding a demo/mock mode that bypasses Epic OAuth entirely, using hardcoded FHIR sandbox data. This lets you develop and test the UI/AI pipeline without depending on Epic's OAuth.
- The `analysisCache` and `chatEngines` in-memory stores will miss frequently on Cloudflare Workers (stateless). For production, migrate these to KV too. For now, they're acceptable since the client-side cache handles most repeat loads.

### Data Contradictions Detected
No data contradictions.

### Where I Fell Short
- Spent too many iterations on Epic OAuth debugging. Should have immediately checked the Non-Production vs Production Client ID distinction when the first "Something went wrong" error appeared.
- The fhir.epic.com account error was a silent failure — I attempted to save via Chrome automation multiple times without catching the error message until explicitly searching for it with JavaScript.
- The Cloudflare Pages → Workers migration added complexity. Should have started with Workers deploy (with assets binding) from the beginning since OpenNext is designed for it.

## 10. Miscommunications
- User gave the Production Client ID (`b551e03c-...`) initially. The sandbox requires the Non-Production Client ID (`c589a1c6-...`). This wasn't a miscommunication — the user didn't know Epic uses separate IDs for sandbox vs production. The distinction was only discovered when viewing the app settings via Chrome.

## 11. Files Changed
```
 CLAUDE.md                             |    63 +
 open-next.config.ts                   |     3 +
 package-lock.json                     | 10143 +++
 package.json                          |    10 +-
 src/__tests__/provider.test.ts        |   238 +
 src/__tests__/smart-auth.test.ts      |    38 +-
 src/app/api/ai/analyze/route.ts       |    24 +-
 src/app/api/ai/chat/route.ts          |     2 +-
 src/app/api/ai/health/route.ts        |    87 +
 src/app/api/ai/note/route.ts          |     2 +-
 src/app/api/ai/ophthalmology/route.ts |     2 +-
 src/app/api/ai/research/route.ts      |     2 +-
 src/app/api/auth/callback/route.ts    |     4 +-
 src/app/api/auth/launch/route.ts      |     2 +-
 src/app/api/chart/route.ts            |     2 +-
 src/app/callback/page.tsx             |    42 +-
 src/app/command-center/page.tsx       |    87 +-
 src/lib/ai/analysis-cache.ts          |    46 +
 src/lib/ai/provider.ts                |   110 +-
 src/lib/smart/scopes.ts               |    24 +-
 src/lib/smart/session.ts              |    82 +-
 wrangler.jsonc                        |    16 +
 22 files changed, 9101 insertions(+), 1928 deletions(-)
```

| File | Action | Why |
|------|--------|-----|
| CLAUDE.md | Created | Project documentation for future sessions |
| open-next.config.ts | Created | OpenNext Cloudflare adapter config |
| wrangler.jsonc | Created | Cloudflare Workers config with KV + assets |
| src/lib/ai/provider.ts | Rewritten | Retry/fallback chain, exported extractJSON/repairJSON |
| src/lib/ai/analysis-cache.ts | Created | Server-side in-memory analysis cache with TTL |
| src/app/api/ai/health/route.ts | Created | Model health check endpoint |
| src/lib/smart/session.ts | Rewritten | Async KV + in-memory fallback session store |
| src/lib/smart/scopes.ts | Modified | Fixed FHIR scopes from .r/.rs to .read format |
| src/app/callback/page.tsx | Rewritten | Read OAuth params from window.location |
| src/app/command-center/page.tsx | Modified | Client-side analysis cache, refresh param |
| src/__tests__/provider.test.ts | Created | 23 tests for AI provider module |
| src/__tests__/smart-auth.test.ts | Modified | Updated for async session functions + new scopes |
| src/app/api/ai/analyze/route.ts | Modified | Server cache + async getSession |
| src/app/api/ai/*.ts (5 routes) | Modified | Async getSession calls |
| src/app/api/auth/*.ts (2 routes) | Modified | Async storeAuthState/retrieveAuthState |
| package.json | Modified | v0.2.0 + deploy scripts + OpenNext/esbuild deps |

## 12. Current State
- **Branch**: main
- **Last commit**: c2b36ad Switch to Workers deploy for proper static asset serving (2026-04-01 19:01:13 -0700)
- **Build**: PASSING — 119/119 tests, 0 TypeScript errors
- **Deploy**: Live at https://residency-app.nikhouseholdr.workers.dev (CSS/JS serving correctly)
- **Uncommitted changes**: none
- **Local SHA matches remote**: Yes (c2b36ad)

## 13. Environment
- **Node.js**: v25.6.1
- **Python**: 3.14.3
- **Dev servers**: None running for this project (nestwisehq has a Next.js dev server on port 3000)

## 14. Session Metrics
- **Duration**: ~120 minutes
- **Tasks**: 13 completed / 15 attempted (Epic OAuth registration and E2E test blocked)
- **User corrections**: 1 (API key persistence — "DO NOT LOSE THIS KEY")
- **Commits**: 8 (7bd44a2, ec7cf77, e198911, 84ceeee, 44a3583, 7c3cae7, 5290ad5, c2b36ad)
- **Skills used**: /whats-next (2x), /full-handoff

## 15. Memory Updates
- Created `feedback_dont_lose_keys.md` — Always persist API keys to .env.local immediately
- Updated `MEMORY.md` — Added pointer to feedback_dont_lose_keys.md
- No new anti-patterns logged (failures were all config/environment issues, not code patterns)

## 16. Skills Used
| Skill | Purpose | Helpful? |
|-------|---------|----------|
| /whats-next | Strategic recommendations (2x) | Yes — drove the entire session's task list |
| /full-handoff | End-of-session handoff | Yes |

## 17. For The Next Agent
Read these files first (in order):
1. This handoff (HANDOFF.md)
2. Previous handoff: handoff_Residency-app_2026-03-31_1415.md
3. ~/.claude/anti-patterns.md
4. CLAUDE.md (project-level)
5. src/lib/ai/provider.ts — retry/fallback architecture
6. src/lib/smart/session.ts — async KV session store
7. wrangler.jsonc — Cloudflare Workers config

**Key context**: App is deployed to Cloudflare Workers. Epic OAuth is blocked by an account-level save error at fhir.epic.com. The fastest unblock is creating a NEW Epic app with the correct redirect URI. Use the Non-Production Client ID for sandbox testing.

**API Keys** (saved in .env.local, gitignored):
- OPENROUTER_API_KEY: Set in .env.local AND Cloudflare Worker secrets
- EPIC_CLIENT_ID: Currently `c589a1c6-c5f6-485e-b099-b4992a5ee555` (Non-Production). Will change if a new Epic app is created.

**Canonical local path: ~/ProjectsHQ/Residency-app/**
**Do NOT open from iCloud or /tmp/.**

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
Before doing ANY work, run the 3-Gate Verification from ~/.claude/CLAUDE.md:
1. GATE 1: Check ~/Projects/site-to-repo-map.json — verify you're in the correct repo
2. GATE 2: git fetch && compare local SHA to remote — git pull if behind
3. GATE 3: Read this handoff + MEMORY.md + anti-patterns.md
ALL 3 GATES MUST PASS before touching any code.

**Canonical path for this project: ~/ProjectsHQ/Residency-app/**
**Last verified commit: c2b36ad on 2026-04-01 19:01:13 -0700**
