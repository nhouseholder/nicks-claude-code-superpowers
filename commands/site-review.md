Multi-agent site review panel. Dispatches senior-dev, frontend, and backend agents in parallel to review the current project from a **functional perspective** — not just bugs, but architecture, UX, performance, and improvement opportunities.

Unlike `/site-audit` (finds and fixes bugs), `/site-review` is a strategic review that asks: "Is this site as good as it could be? What would a senior team recommend?"

**REQUIRES OPUS MODEL.** Architectural judgment requires Opus-level reasoning.

## Arguments
- `$ARGUMENTS` = project directory path (default: current directory)
- `--quick` = Skip backend agent, 2 agents only (~5 min)
- `--deep` = Add architecture agent as 4th reviewer (~15 min)

---

## Shared Review Context

Before dispatching agents, the orchestrator builds a shared context file that all agents read.

### Pre-Flight (Orchestrator)

1. Identify the project from `pwd` + `git remote get-url origin`
2. Read project CLAUDE.md if it exists
3. Read the project's handoff (from superpowers repo) if one exists
4. Identify tech stack from `package.json` / project structure
5. Check if a live URL exists (from `~/Projects/site-to-repo-map.json`)
6. Write `_review/CONTEXT.md`:

```
PROJECT: [name]
REPO: [github url]
LIVE_URL: [url or N/A]
TECH_STACK: [React/Next.js/Vue/etc.]
CSS_FRAMEWORK: [Tailwind/CSS modules/etc.]
BACKEND: [Cloudflare Workers/Express/None/etc.]
LAST_COMMIT: [date + message]
HANDOFF_STATUS: [summary of in-progress/blocked items, or "clean"]
```

---

## Phase 1: Parallel Agent Dispatch

Launch **3 agents simultaneously** (2 if `--quick`, 4 if `--deep`). Each agent reads `_review/CONTEXT.md` first, then performs its domain-specific review. Each writes findings to its own file.

### Agent 1: Senior Frontend Reviewer
**Agent type:** `general-purpose`
**Skills:** `senior-frontend`, `react-best-practices`, `frontend-design`, `impeccable-design`, `design-critique`
**Output:** `_review/frontend_review.md`

Dispatch prompt:
> You are a senior frontend engineer reviewing a production website. Read `_review/CONTEXT.md` for project context. Read `~/.claude/skills/senior-frontend/SKILL.md`, `~/.claude/skills/react-best-practices/SKILL.md`, `~/.claude/skills/frontend-design/SKILL.md`, `~/.claude/skills/impeccable-design/SKILL.md`, and `~/.claude/skills/design-critique/SKILL.md`.
>
> Review the ENTIRE frontend codebase. For each area, note both **problems** and **improvement opportunities**:
>
> **1. Component Architecture**
> - Component composition: are components too large? Too granular? Right abstractions?
> - State management: prop drilling? Global state overuse? Missing context providers?
> - Code reuse: duplicated patterns that should be shared components?
> - File organization: intuitive structure? Easy to find things?
>
> **2. User Experience**
> - All user states handled? (empty, loading, error, success, partial)
> - Navigation flow: can users get lost? Dead ends?
> - Mobile responsiveness: tested at 375px, 768px, 1280px?
> - Accessibility: ARIA labels, keyboard nav, color contrast?
> - Performance feel: perceived speed, loading indicators, skeleton screens?
>
> **3. Visual Design Quality**
> - Run the AI Slop Detection checklist from `impeccable-design` — count fingerprints (0-10 scale)
> - Run Nielsen's Heuristics scoring from `design-critique` — score each of 10 heuristics 0-4 (/40 total)
> - Run cognitive load assessment from `design-critique` — 8-item checklist
> - Select 2-3 relevant personas from `design-critique` and walk through the primary user flow
> - Typography consistency and hierarchy (consult `impeccable-design/reference/typography.md`)
> - Spacing and alignment consistency (consult `impeccable-design/reference/spatial-design.md`)
> - Color usage — intentional or random? (consult `impeccable-design/reference/color-and-contrast.md`)
> - Does the design feel professional or amateur?
> - What one visual change would have the biggest impact?
>
> **4. Performance**
> - Bundle size concerns (large dependencies, barrel imports)
> - Render performance (unnecessary re-renders, missing memoization)
> - Image optimization (formats, lazy loading, sizing)
> - Code splitting and lazy loading opportunities
>
> **5. Frontend Best Practices**
> - TypeScript usage: strict enough? `any` abuse?
> - Error boundaries present?
> - SEO: meta tags, semantic HTML, structured data?
> - Console errors or warnings in dev mode?
>
> For each finding, rate it:
> - **P0** — Broken, users are affected
> - **P1** — Significant quality issue
> - **P2** — Improvement opportunity
> - **P3** — Nice to have
>
> End with: **TOP 3 FRONTEND IMPROVEMENTS** — the changes that would most improve this site for users.
>
> Write everything to `_review/frontend_review.md`.

---

### Agent 2: Senior Backend Reviewer
**Agent type:** `general-purpose`
**Skills:** `senior-backend`, `senior-dev-mindset`
**Output:** `_review/backend_review.md`

Skip this agent if no backend exists (no API routes, no `functions/`, no server files). Write `_review/backend_review.md` with "N/A — no backend" and continue.

Dispatch prompt:
> You are a senior backend engineer reviewing a production API. Read `_review/CONTEXT.md` for project context. Read `~/.claude/skills/senior-backend/SKILL.md` and `~/.claude/skills/senior-dev-mindset/SKILL.md`.
>
> Review ALL backend code. For each area, note both **problems** and **improvement opportunities**:
>
> **1. API Design**
> - RESTful conventions followed? Consistent naming?
> - Response format consistent across endpoints?
> - Pagination on list endpoints?
> - Versioning strategy?
> - Are there missing endpoints that the frontend needs?
>
> **2. Security**
> - Authentication on protected routes?
> - Input validation and sanitization?
> - SQL/NoSQL injection vectors?
> - CORS configuration?
> - Rate limiting on sensitive endpoints?
> - Secrets management (hardcoded keys?)
>
> **3. Performance**
> - N+1 query patterns?
> - Missing database indexes?
> - Caching opportunities (frequently read, rarely written data)?
> - Connection pooling?
> - Unbounded queries (no LIMIT)?
>
> **4. Reliability**
> - Error handling: try/catch with proper HTTP status codes?
> - Graceful degradation when external services fail?
> - Logging: errors logged or silently swallowed?
> - Timeout handling on external API calls?
>
> **5. Data Layer**
> - Schema design appropriate?
> - Migrations in place?
> - Data validation at the boundary?
> - Backup/recovery considerations?
>
> Rate each finding P0-P3. End with: **TOP 3 BACKEND IMPROVEMENTS**.
>
> Write everything to `_review/backend_review.md`.

---

### Agent 3: Senior Dev / Full-Stack Reviewer
**Agent type:** `general-purpose`
**Skills:** `senior-dev-mindset`, `senior-architect`
**Output:** `_review/fullstack_review.md`

Dispatch prompt:
> You are a senior full-stack developer reviewing a production site holistically. Read `_review/CONTEXT.md` for project context. Read `~/.claude/skills/senior-dev-mindset/SKILL.md` and `~/.claude/skills/senior-architect/SKILL.md`.
>
> Review the project as a WHOLE PRODUCT, not just code. Think about what makes this site valuable to its users:
>
> **1. Product Completeness**
> - Does the site deliver on its core promise?
> - What features are half-built or stub?
> - What's the most obvious missing feature a user would expect?
> - Are there dead pages or unreachable features?
>
> **2. Integration Quality**
> - Frontend-backend contract: do they match? Mismatched types? Stale endpoints?
> - Data flow: can you trace user action → API call → database → response → UI update?
> - Auth flow: login → session → protected routes → logout — all solid?
> - Third-party integrations: healthy? Error handled? Fallbacks?
>
> **3. Developer Experience**
> - Can a new developer understand this codebase in 30 minutes?
> - Build/dev/test scripts work reliably?
> - Consistent patterns or every file does it differently?
> - Tech debt that slows down future development?
>
> **4. Deployment & Operations**
> - Build passes clean?
> - Environment config: dev/staging/prod properly separated?
> - Monitoring: would you know if the site went down?
> - Version management: can you roll back?
>
> **5. Competitive Edge**
> - What makes this site different from alternatives?
> - What would make a user choose this over competitors?
> - What's the #1 thing that would make this site 10x more valuable?
>
> Rate each finding P0-P3. End with: **TOP 3 PRODUCT IMPROVEMENTS** — the changes that would most increase this site's value.
>
> Write everything to `_review/fullstack_review.md`.

---

### Agent 4 (--deep only): Architecture Reviewer
**Agent type:** `general-purpose`
**Skills:** `senior-architect`
**Output:** `_review/architecture_review.md`

Dispatch prompt:
> You are a senior architect reviewing system design. Read `_review/CONTEXT.md`. Read `~/.claude/skills/senior-architect/SKILL.md`. Map the entire system architecture (services, data flow, dependencies, deployment). Identify: over-engineering, under-engineering, scalability risks, tech stack fit. Write to `_review/architecture_review.md`.

---

## Phase 2: Synthesis (Orchestrator)

After all agents complete, the orchestrator reads ALL review files and produces a unified report.

1. Read `_review/frontend_review.md`, `_review/backend_review.md`, `_review/fullstack_review.md` (and `_review/architecture_review.md` if `--deep`)
2. Deduplicate findings — same issue flagged by multiple agents gets ONE entry with "[Flagged by: Frontend + Backend]"
3. Merge all P0-P3 items into a single ranked list
4. Identify **cross-cutting themes** — patterns that appear across multiple reviews
5. Build the final recommendation list

---

## Phase 3: Present

```
SITE REVIEW — [Project Name]
==============================
Generated: [date]
Live site: [URL or N/A]
Tech stack: [stack]
Reviewers: Senior Frontend + Senior Backend + Senior Dev [+ Architect]

DESIGN SCORES
-------------
Heuristics: [N]/40 — [Rating]  |  AI Slop: [N]/10 fingerprints  |  Cognitive Load: [Low/Moderate/High]
Weakest heuristic: [name] ([score])  |  Personas tested: [names]

EXECUTIVE SUMMARY
-----------------
[3-4 sentences: overall health, biggest strengths, biggest gaps]

REVIEW PANEL FINDINGS
---------------------

### P0 — Critical (fix immediately)
| # | Issue | Domain | Impact | Effort |
|---|-------|--------|--------|--------|
| 1 | ... | Frontend/Backend/Product | ... | ... |

### P1 — Significant (fix this sprint)
| # | Issue | Domain | Impact | Effort |
|---|-------|--------|--------|--------|

### P2 — Improvement Opportunities
| # | Suggestion | Domain | Impact | Effort |
|---|------------|--------|--------|--------|

### P3 — Nice to Have
[Bulleted list]

CROSS-CUTTING THEMES
---------------------
[Patterns that multiple reviewers flagged — these are systemic, not isolated]

TOP 5 IMPROVEMENTS (RANKED)
----------------------------
The review panel's consensus on what would most improve this site:

#1. [Title]
    Why: [reasoning from multiple reviewers]
    Impact: [what users would notice]
    Effort: [session estimate]

#2. ...
#3. ...
#4. ...
#5. ...

WHAT'S WORKING WELL
--------------------
[Strengths the reviewers noted — what to preserve and build on]

SUGGESTED SESSION PLAN
----------------------
If you start working now, here's the optimal order:
1. [First task — highest value or unblocks others]
2. [Second task]
3. [Third task]
```

---

## Phase 4: Clean Up

```bash
# Keep _review/ for reference — don't delete
echo "Review files saved in _review/"
```

---

## Rules

1. **All agents run in parallel.** The whole point is multiple perspectives simultaneously.
2. **Not just bugs — improvements.** Each agent must suggest what would make the site BETTER, not just what's broken.
3. **READ-ONLY by default.** This command reviews and recommends. It does NOT make changes. The user decides what to act on.
4. **Rate everything P0-P3.** Consistent severity across all reviewers.
5. **Deduplicate in synthesis.** Same issue from 3 reviewers = 1 entry, not 3.
6. **End with a session plan.** The user wants to know what to do next.
7. **Preserve `_review/` directory.** The individual review files are valuable context for the agent that does the actual work later.
8. **Skip backend agent if no backend exists.** Don't waste tokens reviewing what isn't there.
