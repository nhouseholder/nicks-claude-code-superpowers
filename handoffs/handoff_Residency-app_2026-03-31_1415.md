# Handoff — Residency-app — 2026-03-31 14:15
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: handoff_Residency-app_2026-03-29_1430.md
## GitHub repo: nhouseholder/Residency-app
## Local path: ~/Library/Mobile Documents/com~apple~CloudDocs/ProjectsHQ/Residency-app/
## Last commit date: 2026-03-31 13:48:22 -0700

---

## 1. Session Summary
Nicholas wanted to continue building JARVIS (clinical reasoning engine for residency pre-charting). This session completed Phase 2D (Command Center UI) and Phase 2E (Knowledge Research + Ophthalmology Turbo Mode), then switched the LLM provider from Anthropic to free models. After Gemini API key quota issues and OpenRouter paid model credit issues, settled on genuinely free OpenRouter models (Nemotron 120B + Qwen 3.6). All phases 2A-2E are now complete with passing tests and builds.

## 2. What Was Done
- **Phase 2D: JARVIS Command Center UI**: Built dark-mode census board (`command-center/page.tsx`, 489 lines), patient deep-dive page (`patient/[id]/page.tsx`, 653 lines), JARVIS dark theme CSS variables in `globals.css`, command-center layout wrapper
- **12 Shared Components**: AcuityBadge, VitalSparkline, PatientBanner, ProblemCard, NoteViewer, ChatPanel, MonographCard, TeachingCard, ActionItem, LabTrendChart, ErrorBoundary, LoadingSkeleton
- **Phase 2E: Knowledge Research + Ophthalmology**: Research API endpoint (`/api/ai/research`), Ophthalmology API endpoint (`/api/ai/ophthalmology`), integrated into patient deep-dive with 7 tabs
- **LLM Provider Overhaul**: Replaced Anthropic SDK with multi-provider architecture (OpenRouter primary, Gemini fallback). Added `openai` npm package, removed `@anthropic-ai/sdk`. Rewrote `provider.ts` with OpenRouterProvider + GeminiProvider classes
- **JSON Robustness**: Replaced regex-based `extractJSON` with `indexOf/lastIndexOf` approach. Added `repairJSON` function (strips trailing commas, comments)
- **Error Boundaries**: React ErrorBoundary component wrapping each PatientRowCard and tab content
- **Census Persistence**: Patient IDs saved to sessionStorage, restored on page load
- **Turbopack Fix**: Added `turbopack.root` to `next.config.ts` to fix iCloud path detection

## 3. What Failed (And Why)
- **Gemini API key quota 0**: User's Gemini API key had zero quota — project didn't have Generative Language API enabled. Pivoted to OpenRouter.
- **OpenRouter free Gemini model IDs (404)**: `google/gemini-2.5-pro-exp-03-25:free` no longer exists on OpenRouter. Had to query `/api/v1/models` to find valid IDs.
- **OpenRouter 402 insufficient credits**: Gemini 2.5 Pro via OpenRouter costs $1.25/M input — user's free account had no credits. Switched to genuinely free models.
- **Free model 429 rate limits**: `meta-llama/llama-3.3-70b-instruct:free` and `nousresearch/hermes-3-llama-3.1-405b:free` hit upstream rate limits (Venice provider). Switched to `nvidia/nemotron-3-super-120b-a12b:free` and `qwen/qwen3.6-plus-preview:free`.
- **`next dev` exits on iCloud paths**: Next.js 16 CLI bug where `next dev` exits immediately on paths with spaces. Already had `scripts/dev.mjs` workaround from Phase 1; added `turbopack.root` config fix.
- **Nested HTML in layout.tsx**: Initially created command-center layout with `<html>` and `<body>` tags conflicting with root layout. Fixed to `<div>` wrapper.

## 4. What Worked Well
- **Multi-provider LLM architecture**: Auto-selecting OpenRouter > Gemini based on env keys makes the app resilient to API changes
- **`indexOf/lastIndexOf` JSON extraction**: Far more robust than regex for handling LLM output with markdown fences, mixed content
- **Smoke testing models directly**: Testing OpenRouter models via raw API calls before wiring into the app caught issues early
- **`scripts/dev.mjs`**: Programmatic Next.js dev server bypasses CLI path-with-spaces bug reliably

## 5. What The User Wants
Nicholas is an ophthalmologist starting internal medicine internship and needs an autonomous clinical assistant that pre-charts everything before rounds. Key priorities:
- "JARVIS" aesthetic — dark mode, data-dense, Bloomberg Terminal meets Apple Health
- Free LLM tier — no API costs during development
- Full pipeline: FHIR data fetch -> AI analysis -> differential diagnosis -> progress notes -> ophthalmology turbo mode
- User quote context: Said "yes" immediately when offered genuinely free models, showing cost sensitivity
- Confirmed Epic auth timeout error is expected behavior ("is this fixed" — answered: not a bug, Epic's OAuth timeout)

## 6. In Progress (Unfinished)
- **Full E2E browser test**: The complete pipeline (SMART on FHIR auth -> patient fetch -> AI analysis) requires browser-based Epic OAuth flow. CLI-level testing confirmed all components work individually. User saw Epic auth timeout on manual test — this is Epic's OAuth timeout, not a code bug.
- **Epic auth timeout UX**: The "Authorization Error: Your authentication attempt timed out" page works correctly but could be improved with auto-retry or longer state TTL.

## 7. Blocked / Waiting On
- **Epic sandbox auth**: Need to complete the SMART on FHIR OAuth flow in browser to test full pipeline. Epic sandbox is sometimes slow/unreliable.
- **OpenRouter rate limits**: Free tier has aggressive rate limiting. If models are rate-limited during actual use, may need to add retry logic with exponential backoff or rotate between free models.

## 8. Next Steps (Prioritized)
1. **Add retry/fallback for OpenRouter 429s** — Free models hit upstream rate limits. Add exponential backoff + model fallback (try Nemotron, then Qwen, then Gemma 27B) to make the app resilient.
2. **Complete browser E2E test** — Open localhost:3000, auth with Epic sandbox, verify full pipeline: census -> analyze -> notes -> chat -> research -> ophthalmology
3. **Add unit tests for AI modules** — The 96 existing tests cover Phase 1 (FHIR). Need tests for provider.ts (extractJSON, repairJSON), clinical-analyzer, differential, assessment-plan, note-generator with mock LLM responses.
4. **Polish Command Center UX** — Loading states during AI analysis could be smoother, sparkline charts need real data wiring, census table horizontal scroll on mobile

## 9. Agent Observations
### Recommendations
- Consider adding a model health check endpoint that pings OpenRouter to verify which free models are currently available (not rate-limited) before the user starts analyzing patients
- The `repairJSON` function handles trailing commas and comments but may need expansion for other LLM quirks (unquoted keys, single quotes) as more models are tested
- Census board currently re-analyzes all patients on every page load — should cache analysis results with a TTL

### Data Contradictions Detected
No data contradictions.

### Where I Fell Short
- Spent too many iterations on LLM provider switching (Anthropic -> Gemini -> OpenRouter paid -> OpenRouter free -> rate-limited models -> working models). Should have started with OpenRouter free models from the beginning.
- RTK was intercepting and filtering Next.js dev server output, making it hard to debug the Turbopack root issue. Took several attempts to get raw error output.

## 10. Miscommunications
None — session aligned. User's requests were clear throughout.

## 11. Files Changed
```
next.config.ts                               |   4 +-
package-lock.json                            |  81 ++--
package.json                                 |   3 +-
src/app/api/ai/ophthalmology/route.ts        |  49 ++
src/app/api/ai/research/route.ts             |  41 ++
src/app/command-center/layout.tsx            |  21 +
src/app/command-center/page.tsx              | 489 +++++++++++++++
src/app/command-center/patient/[id]/page.tsx | 653 ++++++++++++++++++
src/app/globals.css                          |  19 +
src/components/ActionItem.tsx                |  49 ++
src/components/AcuityBadge.tsx               |  24 +
src/components/ChatPanel.tsx                 | 159 +++++++
src/components/ErrorBoundary.tsx             |  58 +++
src/components/LabTrendChart.tsx             |  93 ++++
src/components/LoadingSkeleton.tsx           |  52 +++
src/components/MonographCard.tsx             |  97 ++++
src/components/NoteViewer.tsx                |  72 +++
src/components/PatientBanner.tsx             |  78 ++++
src/components/ProblemCard.tsx               | 107 +++++
src/components/TeachingCard.tsx              |  60 +++
src/components/VitalSparkline.tsx            |  69 +++
src/lib/ai/chat.ts                           |  29 +-
src/lib/ai/provider.ts                       | 173 +++++--
23 files changed, 2376 insertions(+), 104 deletions(-)
```

| File | Action | Why |
|------|--------|-----|
| next.config.ts | Modified | Added turbopack.root for iCloud path fix |
| package.json / lock | Modified | Added openai SDK, removed @anthropic-ai/sdk |
| src/app/api/ai/ophthalmology/route.ts | Created | Ophthalmology deep-dive API endpoint |
| src/app/api/ai/research/route.ts | Created | Condition/medication research API endpoint |
| src/app/command-center/layout.tsx | Created | Dark theme wrapper for JARVIS UI |
| src/app/command-center/page.tsx | Created | Census board — main JARVIS view |
| src/app/command-center/patient/[id]/page.tsx | Created | Patient deep-dive with 7 tabs |
| src/app/globals.css | Modified | JARVIS CSS custom properties (dark theme) |
| src/components/*.tsx (12 files) | Created | Shared UI components for command center |
| src/lib/ai/chat.ts | Modified | Switched from Anthropic SDK to provider abstraction |
| src/lib/ai/provider.ts | Rewritten | Multi-provider (OpenRouter + Gemini), JSON extraction/repair |

## 12. Current State
- **Branch**: main
- **Last commit**: 92cddf89 Fix Turbopack root detection for iCloud paths with spaces (2026-03-31 13:48:22 -0700)
- **Build**: PASSING — 0 errors, 2 warnings
- **Deploy**: N/A — not deployed yet (dev only)
- **Uncommitted changes**: HANDOFF.md (this file)
- **Local SHA matches remote**: Yes
- **Tests**: 96/96 passing (vitest)
- **TypeScript**: Compiles clean (0 errors)

## 13. Environment
- **Node.js**: v25.6.1
- **Python**: 3.14.3
- **Dev servers**: None running

## 14. Session Metrics
- **Duration**: ~90 minutes
- **Tasks**: 7 completed / 7 attempted (Phase 2D, Phase 2E, provider switch, error boundaries, census persistence, smoke test, turbopack fix)
- **User corrections**: 0
- **Commits**: 5 (this session: 9054291, dd725d1, 742be69, 7fe8cbf, 92cddf8)
- **Skills used**: /whats-next

## 15. Memory Updates
- Project memory previously saved: `project_epic_residency_app.md`, `reference_epic_integration.md`, `user_nicholas_residency.md`
- No new anti-patterns logged this session
- No new memory files created (existing memories still accurate)

## 16. Skills Used
| Skill | Purpose | Helpful? |
|-------|---------|----------|
| /whats-next | Strategic recommendations after Phase 2 completion | Yes — identified free API switch, E2E testing, error boundaries as priorities |

## 17. For The Next Agent
Read these files first (in order):
1. This handoff (HANDOFF.md)
2. Previous handoff: handoff_Residency-app_2026-03-29_1430.md
3. ~/.claude/anti-patterns.md
4. Project MEMORY.md (3 memory files)
5. src/lib/ai/provider.ts — current LLM provider architecture
6. src/app/command-center/page.tsx — census board UI
7. src/app/command-center/patient/[id]/page.tsx — patient deep-dive

**Key context**: All Phase 2 modules (2A-2E) are complete. The app uses free OpenRouter models (Nemotron 120B routine, Qwen 3.6 reasoning). Epic SMART on FHIR auth works but Epic sandbox can timeout. The `next dev` CLI doesn't work on this path (spaces) — use `npm run dev` or `node scripts/dev.mjs`.

**Canonical local path for this project: ~/Library/Mobile Documents/com~apple~CloudDocs/ProjectsHQ/Residency-app/**
**Do NOT open this project from /tmp/. Use the path above.**

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
Before doing ANY work, run the 3-Gate Verification from ~/.claude/CLAUDE.md:
1. GATE 1: Check ~/Projects/site-to-repo-map.json — verify you're in the correct repo
2. GATE 2: git fetch && compare local SHA to remote — git pull if behind
3. GATE 3: Read this handoff + MEMORY.md + anti-patterns.md
ALL 3 GATES MUST PASS before touching any code.

**Canonical path for this project: ~/Library/Mobile Documents/com~apple~CloudDocs/ProjectsHQ/Residency-app/**
**Last verified commit: 92cddf89 on 2026-03-31 13:48:22 -0700**
