Run a comprehensive multi-agent website/webapp redesign. This command takes an existing site and rebuilds it with production-grade quality using every available design and development skill.

**IMPORTANT:** This is a SEQUENTIAL pipeline. Complete each phase fully before starting the next. Each phase uses specific skills that MUST be invoked — not "applied mentally."

## Arguments
- `$ARGUMENTS` = the project directory path (e.g., `~/myapp`, `webapp/`, or `.` for current directory)
- If no argument provided, ask the user which project to redesign

## Partial Run
To re-run a specific phase: `/site-redesign --phase N`
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

## Phase 1: Discovery & Audit (Explore + site-audit)
First, understand what exists:
- Run `/site-audit` on the project (or do a quick version: Explore agent maps structure + screenshots)
- Document: current pages, components, data flow, pain points
- Identify: what works (keep), what's broken (fix), what's ugly (redesign)
- Output: Current state summary + redesign scope

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-redesign Phase 1: discovery and audit"`

## Phase 2: Design Direction (brainstorming + spec-interview + frontend-design)
Before writing ANY code:
- Invoke `brainstorming` skill to explore design direction with the user
- Use `frontend-design` to pick a BOLD aesthetic (not generic AI slop):
  - Name the aesthetic ("Brutalist Joy", "Chromatic Silence", etc.)
  - Choose typography (NO Inter, Roboto, Arial — see frontend-design anti-generic rules)
  - Choose color palette (commit to a dominant + accent, not safe even distribution)
  - Choose layout approach (asymmetric? grid-breaking? bento? editorial?)
- Use `spec-interview` to confirm scope with user
- Output: Design spec document with aesthetic direction, colors, fonts, layout approach

Example aesthetics to inspire direction (don't copy, create your own):
- "Brutalist Joy" — raw concrete textures + neon accent colors + oversized type
- "Chromatic Silence" — minimal layout + one bold color gradient + generous whitespace
- "Editorial Grid" — magazine-style asymmetric layout + serif headlines + strong hierarchy
- "Warm Industrial" — dark backgrounds + amber/copper accents + monospace code aesthetic

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-redesign Phase 2: design direction"`

## Phase 3: Design System Setup (ui-design-system + ui-ux-pro-max)
Spawn a **general-purpose agent** with this briefing:
"You are a Design System agent. Read and follow these skill protocols:
1. ~/.claude/skills/ui-design-system/SKILL.md — follow its checklist
2. ~/.claude/skills/ui-ux-pro-max/SKILL.md — follow its checklist
Also read: ~/.claude/anti-patterns.md (known failure patterns) and the project's MEMORY.md if it exists.
Your task: Build the design foundation before components. Run ui-design-system design token generator: `python scripts/design_token_generator.py [brand_color] [style]`. Generate: color palette, typography scale, spacing system, shadows, animations, breakpoints. Use ui-ux-pro-max search tool for style/palette/font recommendations. Create or update: CSS variables, Tailwind config, theme file.
Output: Design tokens file (CSS/JSON/SCSS) + updated theme config."

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-redesign Phase 3: design system setup"`

## Phase 4: Component Redesign (frontend-design + senior-frontend + react-best-practices)
Spawn a **general-purpose agent** with this briefing:
"You are a Component Redesign agent. Read and follow these skill protocols:
1. ~/.claude/skills/frontend-design/SKILL.md — follow its checklist
2. ~/.claude/skills/senior-frontend/SKILL.md — follow its checklist
3. ~/.claude/skills/react-best-practices/SKILL.md — follow its checklist
4. ~/.claude/skills/senior-dev-mindset/SKILL.md — follow its checklist
Also read: ~/.claude/anti-patterns.md (known failure patterns) and the project's MEMORY.md if it exists.
Your task: Rebuild components with design quality. For EACH major component/page, follow frontend-design protocol: Purpose -> Tone -> Constraints -> Differentiation ('what makes this UNFORGETTABLE?'). Implement with: distinctive typography, bold color use, intentional motion, spatial composition. Follow react-best-practices for performance (memoization, code splitting, lazy loading, no barrel imports, proper suspense boundaries). Follow senior-dev-mindset completeness checklist (all states handled: empty, loading, error, success; mobile responsive, keyboard navigable, accessible).
Output: Rebuilt components with design tokens applied."

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-redesign Phase 4: component redesign"`

## Phase 5: Backend Review & Fixes (senior-backend + senior-architect)
Spawn a **general-purpose agent** with this briefing:
"You are a Backend Review agent. Read and follow these skill protocols:
1. ~/.claude/skills/senior-backend/SKILL.md — follow its checklist
2. ~/.claude/skills/senior-architect/SKILL.md — follow its checklist
Also read: ~/.claude/anti-patterns.md (known failure patterns) and the project's MEMORY.md if it exists.
Your task: Review API routes for security, performance, error handling. Fix any issues found (auth middleware, input validation, query optimization). Ensure frontend-backend contract matches (response shapes, error formats).
Output: Backend fixes applied with descriptions."

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-redesign Phase 5: backend review and fixes"`

## Phase 6: Integration Testing (webapp-testing + qa-gate)
Spawn a **general-purpose agent** with this briefing:
"You are a QA agent. Read and follow these skill protocols:
1. ~/.claude/skills/webapp-testing/SKILL.md — follow its checklist
2. ~/.claude/skills/qa-gate/SKILL.md — follow its checklist
Also read: ~/.claude/anti-patterns.md (known failure patterns) and the project's MEMORY.md if it exists.
Your task: Verify everything works together. Use webapp-testing Playwright toolkit to navigate every page, check for console errors, test all forms/buttons/navigation, verify responsive at mobile/tablet/desktop, take baseline screenshots. Run qa-gate for quality verification.
Output: Test results, screenshots at all breakpoints."

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-redesign Phase 6: integration testing"`

## Phase 7: Visual QA (ui-ux-pro-max + screenshot-dissector)
Spawn a **general-purpose agent** with this briefing:
"You are a Visual QA agent. Read and follow these skill protocols:
1. ~/.claude/skills/ui-ux-pro-max/SKILL.md — follow its checklist
2. ~/.claude/skills/screenshot-dissector/SKILL.md — follow its checklist
Also read: ~/.claude/anti-patterns.md (known failure patterns) and the project's MEMORY.md if it exists.
Your task: Final design quality check. Use ui-ux-pro-max pre-delivery checklist: accessibility (contrast ratios, touch targets, ARIA), performance (no layout shifts, images optimized), consistency (same spacing/colors/fonts everywhere). Use screenshot-dissector for pixel-level review of each page. Fix any visual issues found.
Output: Visual QA pass/fail per page."

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-redesign Phase 7: visual QA fixes"`

## Phase 8: Deploy & Verify (deploy + website-guardian)
Ship it:
- Run `/deploy` skill (build, lint, deploy)
- Follow `website-guardian` post-deploy checklist:
  - Baseline snapshot before deploy
  - Verify ALL baseline items after deploy
  - Check every page visually
- Output: Deploy confirmation + verification results

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-redesign Phase 8: deploy"`

## Phase 9: Documentation & Learning (error-memory + total-recall)
Record what was done:
- Log any bugs found/fixed to `~/.claude/anti-patterns.md`
- Update project memory with new design decisions
- Save design tokens and aesthetic direction for future sessions
- Output: Session handoff document

## Deliverable
Present a redesign summary:

```
REDESIGN COMPLETE
=================
Pages redesigned: X
Components rebuilt: X
Backend fixes: X
Tests passing: X/Y
Design system: [aesthetic name] — [font pair] — [color scheme]

Key changes:
- [bullet list of major changes]

Verified via:
- Playwright tests: [pass/fail]
- Visual QA: [pass/fail]
- Deploy: [success/fail]
```
