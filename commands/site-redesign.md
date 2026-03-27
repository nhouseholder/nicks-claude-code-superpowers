Redesign a website/webapp with production-grade quality. Takes an existing site and rebuilds the visual layer with a distinctive aesthetic using a sequential pipeline of pre-built skill agents.

**REQUIRES OPUS MODEL.** Creative design work requires Opus-level reasoning. If running on Sonnet or Haiku, STOP and tell the user: "Site redesign requires Opus for design quality. Please switch to Opus before running /site-redesign."

**Sequential pipeline. 8 phases. Each phase invokes specific pre-built skills. Main agent (Opus) does ALL design and component work — no subagents for creative decisions.**

## Arguments
- `$ARGUMENTS` = project directory path (default: current directory)
- `--phase N` = skip to Phase N
- `--design-only` = Phases 0-3 only (discovery + design system, no component rebuild)

## Pre-Flight Check

Before starting:
1. **Verify model is Opus.** If not, abort.
2. **Identify the site.** Check `~/Projects/site-to-repo-map.json`.
3. **Load the site-specific command** if one exists (`/mmalogic`, `/update-diamond`, `/update-courtside`, `/update-mystrainai`, `/update-enhancedhealth`, `/update-researcharia`, `/update-nestwisehq`). Read its knowledge base — it has domain-specific display rules that the redesign MUST preserve.
4. **Identify the CSS framework** — Tailwind? CSS modules? Styled-components? This MUST be preserved.

---

## Phase 1: Discovery & Audit (~3 min)
**Skills:** Explore agent + `/site-audit`

1. Run `/site-audit` on the project (or quick version: map structure + screenshots)
2. Take screenshots of every main page via Claude Preview/Chrome
3. Read project memory and anti-patterns for site-specific rules
4. Document: current pages, components, data flow, pain points
5. Identify: what works (KEEP), what's broken (FIX), what's ugly (REDESIGN)

**Write:** `_redesign/phase1_discovery.md` — current state, screenshots, keep/fix/redesign list

## Phase 2: Design Direction (~5 min, INTERACTIVE — requires user input)
**Skills:** `brainstorming` + `frontend-design` + `spec-interview`

1. Invoke `brainstorming` skill — explore design direction with the user
2. Read `~/.claude/skills/frontend-design/SKILL.md` anti-generic rules
3. Propose 3 design directions. For each:
   - **Name** the aesthetic (not generic — "Warm Clinical" not "Modern")
   - **Typography**: specific font pair (NO Inter, Roboto, Arial)
   - **Color**: dominant + accent + neutral. Show hex values.
   - **Layout**: asymmetric? bento? editorial? card-based?
   - **Mood**: what emotion should the user feel?
4. Ask the user which direction (or combine). **Wait for response.**
5. Use `spec-interview` to confirm scope

**Write:** `_redesign/phase2_direction.md` — chosen aesthetic, fonts, colors, layout

## Phase 3: Design System Setup (~5 min)
**Skills:** `ui-design-system` + `ui-ux-pro-max`

Do this yourself (main agent). Do NOT spawn a subagent.

1. **Identify the existing CSS framework and PRESERVE IT.**
   - Tailwind → update `tailwind.config` with custom tokens
   - CSS modules → update module variables
   - Plain CSS → update custom properties in globals.css
2. Read `~/.claude/skills/ui-design-system/SKILL.md` — generate design tokens
3. Read `~/.claude/skills/ui-ux-pro-max/SKILL.md` — palette/font/style guidance
4. Build: color palette, typography scale, spacing system, shadows, animations
5. Create `_redesign/THEME.md` documenting all tokens with usage examples

**Write:** Modified config files + `_redesign/THEME.md`

**If `--design-only`, STOP HERE** and present the design system.

## Phase 4: Component Redesign (~15 min, MAIN AGENT ONLY)
**Skills:** `frontend-design` + `senior-frontend` + `react-best-practices`

**NEVER spawn subagents for this phase.** Main Opus agent does all component work sequentially.

**THE FRAMEWORK PRESERVATION RULE (NON-NEGOTIABLE):**
- Tailwind stays Tailwind. CSS modules stay CSS modules. NEVER convert between approaches.
- NEVER replace Tailwind classes with inline `style={{}}` objects.
- **Update, don't rewrite.** Swap classes/values, don't rewrite 750-line components from scratch.

For EACH page (prioritize: landing > dashboard > detail pages > settings):
1. Read the current component
2. Read `_redesign/THEME.md` for design tokens
3. Follow `frontend-design` differentiation protocol:
   - Purpose → Tone → Constraints → "What makes this UNFORGETTABLE?"
4. Follow `senior-frontend` patterns:
   - Component composition, state management, accessibility
5. Follow `react-best-practices` performance rules:
   - Memoization, code splitting, lazy loading, no barrel imports
6. Apply: new typography, colors, layout — using the EXISTING CSS framework
7. Handle all states: empty, loading, error, success
8. Responsive: mobile-first, tablet, desktop
9. Accessible: ARIA labels, keyboard nav, contrast ratios

**Commit after every 2-3 components:**
```bash
git add -A && git commit -m "redesign: [component names] — [aesthetic name]"
```

**Write:** `_redesign/phase4_progress.md` — track which components done/remaining

## Phase 5: Backend Review (~5 min, 1 agent IF backend exists)
**Skills:** `senior-backend` + `senior-architect`

Skip if no API routes exist. Otherwise spawn ONE general-purpose agent:
- Read `~/.claude/skills/senior-backend/SKILL.md`
- Read `~/.claude/skills/senior-architect/SKILL.md`
- Review API routes: security, performance, error handling
- Fix P0/P1 issues directly
- Ensure frontend-backend contract matches

**Write:** `_redesign/phase5_backend.md`

## Phase 6: Integration Testing (~5 min)
**Skills:** `webapp-testing` + `qa-gate`

1. Run `npm run build` — must pass with zero errors
2. Start dev server, visit every page
3. Read `~/.claude/skills/webapp-testing/SKILL.md` — use Playwright if available
4. Check: console errors? Broken layouts? Missing data? Wrong colors?
5. If site-specific rules exist (e.g., UFC 15-item checklist), run them
6. Fix any issues found

**Write:** `_redesign/phase6_testing.md` — pass/fail per page

## Phase 7: Visual QA (~3 min)
**Skills:** `ui-ux-pro-max` + `screenshot-dissector`

Final pixel-level review:
1. Check each page at mobile (375px), tablet (768px), desktop (1280px)
2. Read `~/.claude/skills/screenshot-dissector/SKILL.md` — methodical examination
3. Verify: consistent spacing, typography hierarchy, color usage
4. Check: dark mode if applicable, focus states, contrast ratios
5. Compare the FEEL against Phase 2 direction — does it match the intended mood?
6. Fix any issues found. Commit.

## Phase 8: Deploy & Verify (~3 min)
**Skills:** `deploy` + `website-guardian`

1. Read `~/.claude/skills/website-guardian/SKILL.md` — pre-deploy checklist
2. Final build: `npm run build` (or lint + typecheck + build)
3. Invoke `/deploy` or deploy manually via the project's deploy method
4. Post-deploy: visual verification on live site via Claude in Chrome
5. Log design decisions to project memory
6. Log bugs found/fixed to `~/.claude/anti-patterns.md`

**Final commit:**
```bash
git add -A && git commit -m "redesign complete: [aesthetic name] — [N] pages, [N] components

Fonts: [primary] + [secondary]
Colors: [dominant] + [accent]
Layout: [approach]"
```

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

Skills used: [list of skills invoked]
Redesign files: _redesign/ (direction, theme, progress, verification)

✅ Version bumped: v[old] → v[new]
✅ GitHub synced: committed and pushed (commit [SHA])
✅ Deployed: [method]
✅ Now live: verified at [URL]
```

---

## Design Principles
- **Opus only.** Creative design requires Opus-level reasoning. Sonnet lacks aesthetic judgment.
- **Sequential skill pipeline.** Each phase invokes specific pre-built skills by reading their SKILL.md. Don't "apply mentally" — actually load and follow the skill protocol.
- **User chooses the direction.** Phase 2 is interactive — present options, don't dictate.
- **Main agent does ALL design and component work.** NEVER spawn subagents for Phases 2-4. Only Phase 5 (backend) gets a subagent.
- **PRESERVE the CSS framework.** Tailwind stays Tailwind. Converting to inline styles is a regression. (NFL Draft incident, 2026-03-26)
- **Update, don't rewrite.** Swap classes and values. Don't rewrite components from scratch.
- **Load site-specific knowledge first.** Dedicated commands contain display rules that MUST survive.
- **Inter-phase data via `_redesign/` files.** THEME.md is the single source of truth.
- **Token budget: ~45 min total.** `--design-only`: ~13 min. Commit frequently.
- **Never use Inter, Roboto, or Arial.** The whole point is to look different.
