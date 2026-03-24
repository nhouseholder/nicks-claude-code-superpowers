Run a comprehensive multi-agent website/webapp redesign. This command takes an existing site and rebuilds it with production-grade quality using every available design and development skill.

**IMPORTANT:** This is a SEQUENTIAL pipeline. Complete each phase fully before starting the next. Each phase uses specific skills that MUST be invoked — not "applied mentally."

## Arguments
- `$ARGUMENTS` = the project directory path (e.g., `~/myapp`, `webapp/`, or `.` for current directory)
- If no argument provided, ask the user which project to redesign

## Phase 1: Discovery & Audit (Explore + site-audit)
First, understand what exists:
- Run `/site-audit` on the project (or do a quick version: Explore agent maps structure + screenshots)
- Document: current pages, components, data flow, pain points
- Identify: what works (keep), what's broken (fix), what's ugly (redesign)
- Output: Current state summary + redesign scope

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

## Phase 3: Design System Setup (ui-design-system + ui-ux-pro-max)
Build the foundation before components:
- Run `ui-design-system` design token generator: `python scripts/design_token_generator.py [brand_color] [style]`
- Generate: color palette, typography scale, spacing system, shadows, animations, breakpoints
- Use `ui-ux-pro-max` search tool for style/palette/font recommendations
- Create or update: CSS variables, Tailwind config, theme file
- Output: Design tokens file (CSS/JSON/SCSS) + updated theme config

## Phase 4: Component Redesign (frontend-design + senior-frontend + react-best-practices)
Rebuild components with design quality:
- For EACH major component/page, follow `frontend-design` protocol:
  - Purpose → Tone → Constraints → Differentiation ("what makes this UNFORGETTABLE?")
  - Implement with: distinctive typography, bold color use, intentional motion, spatial composition
- Follow `react-best-practices` rules for performance:
  - Memoization where needed, code splitting, lazy loading
  - No barrel imports, proper suspense boundaries
- Follow `senior-frontend` patterns:
  - Component composition, state management, accessibility
- Follow `senior-dev-mindset` completeness checklist:
  - All states handled (empty, loading, error, success)
  - Mobile responsive, keyboard navigable, accessible
- Output: Rebuilt components with design tokens applied

## Phase 5: Backend Review & Fixes (senior-backend + senior-architect)
While frontend is being redesigned:
- Review API routes for: security, performance, error handling
- Fix any issues found (auth middleware, input validation, query optimization)
- Ensure frontend-backend contract matches (response shapes, error formats)
- Follow `senior-architect` system design patterns
- Output: Backend fixes applied

## Phase 6: Integration Testing (webapp-testing + qa-gate)
Verify everything works together:
- Use `webapp-testing` Playwright toolkit to:
  - Navigate every page, check for console errors
  - Test all forms, buttons, navigation
  - Verify responsive at mobile/tablet/desktop
  - Take baseline screenshots
- Run `qa-gate` for quality verification
- Output: Test results, screenshots at all breakpoints

## Phase 7: Visual QA (ui-ux-pro-max + screenshot-dissector)
Final design quality check:
- Use `ui-ux-pro-max` pre-delivery checklist:
  - Accessibility: contrast ratios, touch targets, ARIA
  - Performance: no layout shifts, images optimized
  - Consistency: same spacing/colors/fonts everywhere
- Use `screenshot-dissector` for pixel-level review of each page
- Fix any visual issues found
- Output: Visual QA pass/fail per page

## Phase 8: Deploy & Verify (deploy + website-guardian)
Ship it:
- Run `/deploy` skill (build, lint, deploy)
- Follow `website-guardian` post-deploy checklist:
  - Baseline snapshot before deploy
  - Verify ALL baseline items after deploy
  - Check every page visually
- Output: Deploy confirmation + verification results

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
