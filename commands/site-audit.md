Run a comprehensive multi-agent website/webapp audit. This command sequentially dispatches specialized agents to cover every dimension of the site. Each phase produces a findings report before the next phase begins.

**IMPORTANT:** This is a SEQUENTIAL pipeline. Complete each phase fully before starting the next. Do NOT skip phases. Do NOT merge phases. Each phase uses specific skills.

## Arguments
- `$ARGUMENTS` = the project directory path (e.g., `~/myapp`, `webapp/`, or `.` for current directory)
- If no argument provided, ask the user which project to audit

## Phase 1: Codebase Reconnaissance (Explore agent)
Spawn an **Explore agent** to map the project:
- Directory structure, entry points, tech stack
- Count: pages/routes, components, API endpoints, data models
- Identify: framework (React/Next/Vue/etc), styling (Tailwind/CSS/etc), backend (Node/Python/etc), database
- Output: project summary with file counts and architecture overview

## Phase 2: Frontend Audit (frontend-design + ui-ux-pro-max + react-best-practices)
Spawn a **general-purpose agent** briefed with these skills:
- Read ALL component/page files
- Check against `frontend-design` anti-slop guidelines (generic fonts? boring layouts? AI aesthetics?)
- Check against `ui-ux-pro-max` accessibility rules (contrast ratios, touch targets, ARIA labels)
- Check against `react-best-practices` performance rules (memo, bundle splitting, hydration)
- Check responsive design (mobile, tablet, desktop breakpoints)
- Output: Ranked list of frontend issues (P0-P3) with file:line locations

## Phase 3: Backend Audit (senior-backend + senior-architect + audit)
Spawn a **general-purpose agent** briefed with these skills:
- Read ALL API routes, middleware, database queries, auth logic
- Check for: security issues (unauthenticated routes, SQL injection, missing CORS)
- Check for: performance issues (N+1 queries, missing indexes, no caching)
- Check for: architecture issues (god files, missing error handling, tight coupling)
- Run `/audit` skill for secrets scanning
- Output: Ranked list of backend issues (P0-P3) with file:line locations

## Phase 4: UI/UX Review (ui-design-system + canvas-design)
Spawn a **general-purpose agent** OR use Claude in Chrome/Preview:
- If preview available: take screenshots of every page
- Check design consistency: colors, typography, spacing, component patterns
- Check against `ui-design-system` token standards
- Identify: inconsistent styling, missing states (empty, loading, error), broken layouts
- Output: Visual issues list with page locations

## Phase 5: Testing & Verification (webapp-testing + qa-gate)
Spawn a **general-purpose agent** briefed with webapp-testing:
- Use Playwright (via `webapp-testing` skill's `with_server.py`) to:
  - Navigate to each page/route
  - Check for console errors
  - Verify all links work (no 404s)
  - Check forms submit correctly
  - Take screenshots for visual regression baseline
- Output: Test results with pass/fail per page

## Phase 6: Bug Fixing (systematic-debugging + error-memory + website-guardian)
Based on findings from Phases 2-5:
- Prioritize: P0 (crashes, security) → P1 (broken features) → P2 (UX issues) → P3 (polish)
- Fix P0 and P1 issues directly
- For each fix: follow `website-guardian` baseline snapshot → fix → verify protocol
- Log all bugs to `~/.claude/anti-patterns.md` via `error-memory`
- Output: Fixed issues list with before/after

## Phase 7: Final Verification (website-guardian + verification-before-completion)
- Re-run Phase 5 tests to confirm fixes didn't break anything
- Compare screenshots before/after
- Run `website-guardian` full checklist
- Output: Final status report

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
