Redesign a website/webapp with production-grade quality using an agent pipeline architecture. Each phase dispatches a specialized agent. Agents communicate through shared memory files in `_redesign/`. Context is handed off explicitly between phases.

**REQUIRES OPUS MODEL.** If running on Sonnet or Haiku, STOP: "Site redesign requires Opus. Please switch to Opus before running /site-redesign."

## Arguments
- `$ARGUMENTS` = project directory path (default: current directory)
- `--phase N` = skip to Phase N (reads existing `_redesign/` context)
- `--design-only` = Phases 0-3 only

---

## Shared Memory Architecture

All agents communicate via files in `_redesign/`. **Every agent reads `_redesign/CONTEXT.md` before doing any work.** The orchestrator (main Opus agent) writes and updates this file between phases.

### `_redesign/CONTEXT.md` — Master Context (written by orchestrator)
```
PROJECT: [name]
CSS_FRAMEWORK: [Tailwind | CSS modules | styled-components | plain CSS]  ← NEVER CHANGE THIS
TECH_STACK: [Next.js/React/Vue/etc.]
PACKAGE_MANAGER: [npm/pnpm/yarn]
SITE_SPECIFIC_COMMAND: [/mmalogic | /update-diamond | etc. | none]
ANTI_PATTERNS: [known bugs and regressions for this project]
PHASE_STATUS: [which phases completed]
```

### Handoff Protocol
Each agent writes `_redesign/handoff_phaseN.md` at the end of its work:
```
PHASE: N
AGENT: [type]
STATUS: complete | partial | failed
DECISIONS: [key decisions made]
FILES_WRITTEN: [list]
NEXT_AGENT_MUST_KNOW: [critical context for the next phase]
WARNINGS: [anything that could break if ignored]
```

---

## Pre-Flight (Orchestrator — before spawning any agent)

1. Verify Opus model. Abort if not.
2. Check `~/Projects/site-to-repo-map.json` — identify repo.
3. Load site-specific command knowledge base if one exists.
4. Identify CSS framework from `package.json` / config files.
5. **Write `_redesign/CONTEXT.md`** with all known values.
6. Create `_redesign/` directory.

---

## Phase 1: Discovery
**Agent type:** `Explore`
**Input:** `_redesign/CONTEXT.md`
**Output:** `_redesign/phase1_discovery.md`, `_redesign/handoff_phase1.md`

Dispatch prompt to Explore agent:
> Read `_redesign/CONTEXT.md` first. Then map the entire codebase: all pages, all components, all data flows. Identify what works (KEEP), what's broken (FIX), what's ugly (REDESIGN). Screenshot every main page via browser tools. Document current color palette, fonts, spacing. Write findings to `_redesign/phase1_discovery.md`. End by writing `_redesign/handoff_phase1.md`.

Orchestrator reads `handoff_phase1.md` before proceeding.

---

## Phase 2: Design Direction
**Agent type:** Main orchestrator (INTERACTIVE — requires user input)
**Input:** `_redesign/phase1_discovery.md`, `_redesign/CONTEXT.md`
**Output:** `_redesign/phase2_direction.md`

**Do this yourself (no subagent) — user interaction required.**

1. Read `phase1_discovery.md` — understand what currently exists.
2. Read `~/.claude/skills/frontend-design/SKILL.md` — anti-generic rules.
3. Invoke `brainstorming` skill.
4. Propose **3 design directions**. For each:
   - **Name**: specific aesthetic (NOT "modern" or "clean")
   - **Typography**: named font pair — NEVER Inter, Roboto, Arial
   - **Color**: dominant + accent + neutral (show hex)
   - **Layout**: asymmetric / bento / editorial / card-grid / etc.
   - **Mood**: one sentence — what should the user feel?
5. **Wait for user to choose.** Do not proceed without explicit choice.
6. Write `_redesign/phase2_direction.md` with the chosen direction in full detail.

---

## Phase 3: Design System
**Agent type:** `general-purpose`
**Input:** `_redesign/CONTEXT.md`, `_redesign/phase2_direction.md`
**Output:** `_redesign/THEME.md`, updated config files, `_redesign/handoff_phase3.md`

Dispatch prompt:
> Read `_redesign/CONTEXT.md` — note CSS_FRAMEWORK, never change it. Read `_redesign/phase2_direction.md` — this is the chosen design direction. Read `~/.claude/skills/ui-design-system/SKILL.md` and `~/.claude/skills/ui-ux-pro-max/SKILL.md`. Build the design token system:
> - If Tailwind: update `tailwind.config` with custom color/font/spacing tokens
> - If CSS modules: update shared variables file
> - If plain CSS: update custom properties in globals.css
>
> Create `_redesign/THEME.md` — this is the single source of truth for all subsequent agents. Include: every color with hex + usage, font names + weights, spacing scale, shadow levels, animation timing. End by writing `_redesign/handoff_phase3.md`.

Orchestrator validates `THEME.md` exists and CSS framework was preserved before Phase 4.

---

## Phase 4: Component Redesign
**Agent type:** Multiple `general-purpose` agents (parallel where files are independent)
**Input:** `_redesign/CONTEXT.md`, `_redesign/THEME.md`, specific component files
**Output:** Updated component files, `_redesign/phase4_progress.md`, `_redesign/handoff_phase4.md`

**Parallelism rule:** Group components by independence. Components that share no files run in parallel. Components that share a CSS file run sequentially.

For EACH component group, dispatch:
> Read `_redesign/CONTEXT.md` — CSS_FRAMEWORK is [X]. This CANNOT change. Read `_redesign/THEME.md` — apply these tokens using the existing CSS framework. Do NOT convert Tailwind to inline styles. Do NOT convert CSS modules to any other approach. Update, do not rewrite.
>
> Components assigned to you: [list component files]
>
> For each component:
> 1. Read the current file fully before touching it
> 2. Apply THEME.md tokens — swap classes/values, don't rewrite from scratch
> 3. Handle all states: empty, loading, error, success
> 4. Mobile-first responsive: 375px, 768px, 1280px
> 5. Accessibility: ARIA labels, keyboard nav, contrast ratios
> 6. Commit after every 2-3 components: `git add -A && git commit -m "redesign: [names]"`
>
> Write progress to `_redesign/phase4_progress.md`. Write `_redesign/handoff_phase4.md` at the end.

**Orchestrator validation after each agent:** Check that no inline `style={{}}` objects were added where Tailwind classes existed. If framework was converted — revert and re-dispatch with stronger constraints.

---

## Phase 5: Backend Review
**Agent type:** `general-purpose` (skip entirely if no API routes)
**Input:** `_redesign/CONTEXT.md`, `_redesign/handoff_phase4.md`
**Output:** `_redesign/phase5_backend.md`, `_redesign/handoff_phase5.md`

Dispatch prompt:
> Read `_redesign/CONTEXT.md`. Read `~/.claude/skills/senior-backend/SKILL.md` and `~/.claude/skills/senior-architect/SKILL.md`. Review all API routes for: security issues, performance problems, error handling gaps, frontend-backend contract mismatches. Fix P0/P1 issues directly. Write findings to `_redesign/phase5_backend.md`. Write `_redesign/handoff_phase5.md`.

---

## Phase 6: Integration Testing
**Agent type:** `general-purpose`
**Input:** `_redesign/CONTEXT.md`, all previous handoff files
**Output:** `_redesign/phase6_testing.md`, `_redesign/handoff_phase6.md`

Dispatch prompt:
> Read `_redesign/CONTEXT.md`. Read all `_redesign/handoff_phase*.md` files — understand what was changed. Read `~/.claude/skills/webapp-testing/SKILL.md`. Run:
> 1. `npm run build` — must pass zero errors
> 2. Start dev server, visit every page via browser
> 3. Check: console errors, broken layouts, missing data, wrong colors
> 4. Site-specific rules from CONTEXT.md ANTI_PATTERNS — run each check
> 5. Fix issues found. Commit fixes.
> Write `_redesign/phase6_testing.md` with pass/fail per page. Write `_redesign/handoff_phase6.md`.

---

## Phase 7: Visual QA
**Agent type:** Main orchestrator (screenshot tools required)
**Input:** `_redesign/CONTEXT.md`, `_redesign/phase2_direction.md`, `_redesign/handoff_phase6.md`

**Do this yourself — screenshot and visual inspection tools are only available to the main agent.**

1. Read `phase2_direction.md` — what mood/aesthetic was chosen?
2. Screenshot each page at 375px, 768px, 1280px via Claude Preview/Chrome.
3. Read `~/.claude/skills/screenshot-dissector/SKILL.md` — methodical pixel examination.
4. Verify: spacing consistency, typography hierarchy, color adherence to THEME.md.
5. Check: focus states, contrast ratios, dark mode if applicable.
6. Ask: does the FEEL match the intended mood from Phase 2?
7. Fix issues. Commit.

---

## Phase 8: Deploy & Verify
**Agent type:** Main orchestrator
**Input:** All `_redesign/` files

1. Read `~/.claude/skills/website-guardian/SKILL.md` — pre-deploy checklist.
2. Final build: `npm run build` (or project's build command).
3. Invoke `/deploy` or project's deploy method.
4. Post-deploy: visual verification on live site via Claude in Chrome.
5. Log design decisions to project memory.
6. Log bugs found/fixed to `~/.claude/anti-patterns.md`.
7. Final commit: include aesthetic name, page count, component count.

---

## Deliverable

```
REDESIGN COMPLETE
=================
Project: [name] | Aesthetic: [name]
Fonts: [primary] + [secondary]
Colors: [dominant hex] + [accent hex] + [neutral hex]
Layout: [approach]
CSS Framework: [preserved — Tailwind/CSS modules/etc.]

Agent pipeline:
  Phase 1 (Discovery):     Explore agent
  Phase 2 (Direction):     Orchestrator + user
  Phase 3 (Design System): general-purpose agent
  Phase 4 (Components):    [N] general-purpose agents ([M] parallel groups)
  Phase 5 (Backend):       general-purpose agent | skipped
  Phase 6 (Testing):       general-purpose agent
  Phase 7 (Visual QA):     Orchestrator
  Phase 8 (Deploy):        Orchestrator

Pages redesigned: [N] / [total]
Components updated: [N]
Backend fixes: [N]
Build: passing ✓

Verification:
- Desktop: [pass/fail]
- Tablet: [pass/fail]
- Mobile: [pass/fail]
- Accessibility: [pass/fail]
- Site-specific rules: [N/N passed]

Shared memory: _redesign/ ([N] files — direction, theme, handoffs, progress)

✅ Version bumped: v[old] → v[new]
✅ GitHub synced: committed and pushed (commit [SHA])
✅ Deployed: [method]
✅ Now live: verified at [URL]
```

---

## Agent Pipeline Rules

- **Orchestrator controls flow.** Main Opus agent dispatches agents, reads handoffs, validates output, proceeds or retries.
- **Every agent reads CONTEXT.md first.** No exceptions. CSS framework is in CONTEXT.md — this prevents framework drift.
- **Every agent writes a handoff.** No agent finishes without writing `_redesign/handoff_phaseN.md`.
- **Phases 2, 7, 8 stay with orchestrator.** Phase 2 needs user interaction. Phases 7-8 need screenshot tools only available to main agent.
- **Framework preservation is enforced by orchestrator validation** between Phase 3 → Phase 4. Orchestrator checks output before dispatching next agent.
- **Parallelism only for independent files.** Components sharing a CSS file are sequential. Never parallel-write the same file.
- **Retry on framework violation.** If an agent converts Tailwind to inline styles — revert, add stronger constraint to prompt, re-dispatch.
- **Commit after every agent phase.** Rate limits and crashes don't lose work.
- **NEVER use Inter, Roboto, or Arial.** Non-negotiable. The whole point is differentiation.
