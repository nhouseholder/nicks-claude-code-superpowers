Run a comprehensive multi-agent website/webapp audit. This command sequentially dispatches specialized agents to cover every dimension of the site. Each phase produces a findings report before the next phase begins.

**IMPORTANT:** This is a SEQUENTIAL pipeline. Complete each phase fully before starting the next. Do NOT skip phases. Do NOT merge phases. Each phase uses specific skills.

## Arguments
- `$ARGUMENTS` = the project directory path (e.g., `~/myapp`, `webapp/`, or `.` for current directory)
- If no argument provided, ask the user which project to audit

## Partial Run
To re-run a specific phase: `/site-audit --phase N`
If `$ARGUMENTS` contains `--phase N`, skip to Phase N directly (assumes earlier phases are already complete).

## Phase 0: Auto-detect Project Context
Before asking the user anything, gather context automatically:
```bash
# Tech stack detection
PROJECT_NAME=$(basename "$(pwd)")
[ -f package.json ] && echo "Node.js project" && cat package.json | grep -E '"(react|next|vue|svelte|express)"' 2>/dev/null
[ -f requirements.txt ] && echo "Python project"
[ -f pyproject.toml ] && echo "Python project"
[ -f wrangler.toml ] && echo "Cloudflare Workers"

# Recent activity
git log --oneline -5 2>/dev/null
git status --short 2>/dev/null

# Running servers
ps aux | grep -E "(next|vite|express|flask|uvicorn|wrangler)" | grep -v grep 2>/dev/null
```

## Phase 1: Codebase Reconnaissance (Explore agent)
Spawn a **general-purpose agent** with this briefing:
"You are an Explore agent. Your task: Map the project structure — directory structure, entry points, tech stack. Count: pages/routes, components, API endpoints, data models. Identify: framework (React/Next/Vue/etc), styling (Tailwind/CSS/etc), backend (Node/Python/etc), database.
Also read: ~/.claude/anti-patterns.md (known failure patterns) and the project's MEMORY.md if it exists.
Output: project summary with file counts and architecture overview."

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-audit Phase 1: codebase reconnaissance"`

## Phase 2: Frontend Audit (frontend-design + ui-ux-pro-max + react-best-practices)
Spawn a **general-purpose agent** with this briefing:
"You are a Frontend Audit agent. Read and follow these skill protocols:
1. ~/.claude/skills/frontend-design/SKILL.md — follow its checklist
2. ~/.claude/skills/ui-ux-pro-max/SKILL.md — follow its checklist
3. ~/.claude/skills/react-best-practices/SKILL.md — follow its checklist
Also read: ~/.claude/anti-patterns.md (known failure patterns) and the project's MEMORY.md if it exists.
Your task: Read ALL component/page files. Check against frontend-design anti-slop guidelines (generic fonts? boring layouts? AI aesthetics?). Check against ui-ux-pro-max accessibility rules (contrast ratios, touch targets, ARIA labels). Check against react-best-practices performance rules (memo, bundle splitting, hydration). Check responsive design (mobile, tablet, desktop breakpoints).
Output: Ranked list of frontend issues (P0-P3) with file:line locations."

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-audit Phase 2: frontend audit"`

## Phase 3: Backend Audit (senior-backend + senior-architect + audit)
Spawn a **general-purpose agent** with this briefing:
"You are a Backend Audit agent. Read and follow these skill protocols:
1. ~/.claude/skills/senior-backend/SKILL.md — follow its checklist
2. ~/.claude/skills/senior-architect/SKILL.md — follow its checklist
3. ~/.claude/skills/audit/SKILL.md — follow its checklist
Also read: ~/.claude/anti-patterns.md (known failure patterns) and the project's MEMORY.md if it exists.
Your task: Read ALL API routes, middleware, database queries, auth logic. Check for: security issues (unauthenticated routes, SQL injection, missing CORS), performance issues (N+1 queries, missing indexes, no caching), architecture issues (god files, missing error handling, tight coupling). Run /audit skill for secrets scanning.
Output: Ranked list of backend issues (P0-P3) with file:line locations."

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-audit Phase 3: backend audit"`

## Phase 4: UI/UX Review (ui-design-system + canvas-design)
Spawn a **general-purpose agent** with this briefing:
"You are a UI/UX Review agent. Read and follow these skill protocols:
1. ~/.claude/skills/ui-design-system/SKILL.md — follow its checklist
2. ~/.claude/skills/canvas-design/SKILL.md — follow its checklist
Also read: ~/.claude/anti-patterns.md (known failure patterns) and the project's MEMORY.md if it exists.
Your task: If preview available, take screenshots of every page. Check design consistency: colors, typography, spacing, component patterns. Check against ui-design-system token standards. Identify: inconsistent styling, missing states (empty, loading, error), broken layouts.
Output: Visual issues list with page locations."

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-audit Phase 4: UI/UX review"`

## Phase 5: Testing & Verification (webapp-testing + qa-gate)
Spawn a **general-purpose agent** with this briefing:
"You are a QA agent. Read and follow these skill protocols:
1. ~/.claude/skills/webapp-testing/SKILL.md — follow its checklist
2. ~/.claude/skills/qa-gate/SKILL.md — follow its checklist
Also read: ~/.claude/anti-patterns.md (known failure patterns) and the project's MEMORY.md if it exists.
Your task: Use Playwright (via webapp-testing skill's with_server.py) to navigate to each page/route, check for console errors, verify all links work (no 404s), check forms submit correctly, take screenshots for visual regression baseline.
Output: Test results with pass/fail per page."

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-audit Phase 5: testing and verification"`

## Phase 6: Bug Fixing (systematic-debugging + error-memory + website-guardian)
Based on findings from Phases 2-5:
- Prioritize: P0 (crashes, security) → P1 (broken features) → P2 (UX issues) → P3 (polish)
- Fix P0 and P1 issues directly
- For each fix: follow `website-guardian` baseline snapshot → fix → verify protocol
- Log all bugs to `~/.claude/anti-patterns.md` via `error-memory`
- Output: Fixed issues list with before/after

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-audit Phase 6: bug fixes"`

## Phase 7: Final Verification (website-guardian + verification-before-completion)
- Re-run Phase 5 tests to confirm fixes didn't break anything
- Compare screenshots before/after
- Run `website-guardian` full checklist
- Output: Final status report

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-audit Phase 7: final verification"`

## Deliverable
Present a single summary table:

```
| Phase | Issues Found | Fixed | Remaining | Severity |
|-------|-------------|-------|-----------|----------|
| Frontend | X | Y | Z | P0: A, P1: B |
| Backend | X | Y | Z | P0: A, P1: B |
| UI/UX | X | Y | Z | ... |
| Testing | X | Y | Z | ... |
| TOTAL | X | Y | Z | ... |
```

Plus: what was fixed, what needs manual attention, and recommended next steps.
