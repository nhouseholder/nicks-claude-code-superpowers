Redesign a website/webapp with production-grade quality. Takes an existing site and rebuilds the visual layer with a distinctive aesthetic.

**REQUIRES OPUS MODEL.** Creative design work requires Opus-level reasoning. If running on Sonnet or Haiku, STOP and tell the user: "Site redesign requires Opus for design quality. Please switch to Opus before running /site-redesign."

**Sequential pipeline. Each phase produces artifacts the next phase consumes. Main agent does ALL design work — no subagents for creative decisions.**

## Pre-Flight Check

Before starting:
1. **Verify model is Opus.** If not, abort with message above.
2. **Identify the site.** Check `~/Projects/site-to-repo-map.json` for the current project.
3. **Load the site-specific command** if one exists (`/mmalogic`, `/update-diamond`, `/update-courtside`, `/update-mystrainai`, `/update-enhancedhealth`, `/update-researcharia`, `/update-nestwisehq`). Read its knowledge base — it has domain-specific display rules that the redesign MUST preserve.
4. **Load skills sequentially** (read each SKILL.md, don't just "apply mentally"):
   - `~/.claude/skills/frontend-design/SKILL.md` — anti-generic design rules
   - `~/.claude/skills/ui-ux-pro-max/SKILL.md` — design system intelligence
   - `~/.claude/skills/website-guardian/SKILL.md` — Rule Zero (surgical scope)
   - `~/.claude/skills/react-best-practices/SKILL.md` — performance rules

## Arguments
- `$ARGUMENTS` = project directory path (default: current directory)
- `--phase N` = skip to Phase N
- `--design-only` = Phases 0-3 only (discovery + design system, no component rebuild)

## Phase 0: Orient & Discover (~2 min, main agent)

Do this yourself:
```bash
PROJECT_NAME=$(basename "$(pwd)")
echo "=== Redesign: $PROJECT_NAME ==="

# Stack
[ -f package.json ] && node -e "const p=require('./package.json'); console.log('Stack:', Object.keys(p.dependencies||{}).filter(d=>/react|next|vue|svelte|tailwind/.test(d)).join(', '))"

# Current design
find src -name "tailwind.config*" -o -name "theme*" -o -name "globals.css" -o -name "*.css" 2>/dev/null | head -10
grep -r "fontFamily\|font-family" src/ --include="*.css" --include="*.ts" --include="*.tsx" -l 2>/dev/null | head -5
grep -r "colors\|palette" tailwind.config* 2>/dev/null | head -10

# Pages and components
find src -name "page.tsx" -o -name "page.jsx" 2>/dev/null | head -20
find src/components -name "*.tsx" -o -name "*.jsx" 2>/dev/null | wc -l | xargs echo "Components:"
```

Read project memory and anti-patterns. Take screenshots of every main page via Claude Preview/Chrome.

**Write:** `_redesign/phase0_discovery.md` — current state, screenshots, what works, what's ugly, what's broken. List every page with a 1-line assessment.

## Phase 1: Design Direction (~5 min, main agent + user interaction)

This phase REQUIRES user input. Present options, don't just pick one.

1. Read `~/.claude/skills/frontend-design/SKILL.md` anti-generic rules
2. Analyze the current design: what's the vibe? Clinical? Playful? Corporate? Broken?
3. Propose 3 design directions. For each:
   - **Name** the aesthetic (not generic — "Warm Clinical" not "Modern")
   - **Typography**: specific font pair (NO Inter, Roboto, Arial — pick something with personality)
   - **Color**: dominant + accent + neutral. Show hex values.
   - **Layout**: asymmetric? bento? editorial? card-based?
   - **Mood**: what emotion should the user feel?

Example directions:
- "Warm Clinical" — Outfit + Source Serif / sage green + warm cream / generous whitespace + soft shadows
- "Bold Precision" — Space Grotesk + Fraunces / deep navy + electric coral / grid-breaking asymmetric
- "Quiet Authority" — Geist + Newsreader / charcoal + warm gold / editorial magazine layout

4. Ask the user which direction (or combine elements). Wait for response.

**Write:** `_redesign/phase1_direction.md` — chosen aesthetic, fonts, colors, layout approach.

## Phase 2: Design System (~5 min, main agent — NO subagents)

Do this yourself. Do NOT spawn a subagent for the design system — it needs to understand the existing CSS approach to avoid destroying it.

1. **Identify the existing CSS framework** — Tailwind? CSS modules? Styled-components? Plain CSS?
2. **PRESERVE IT.** A redesign changes colors, fonts, spacing, and layout — NOT the styling approach. If the project uses Tailwind, the redesigned code uses Tailwind. Period.
3. Create/update the design tokens IN the existing framework:
   - **Tailwind projects**: update `tailwind.config` with custom colors, fonts, spacing, shadows. Use `@apply` or utility classes. NEVER replace Tailwind with inline `style={{}}`.
   - **CSS modules**: update the module variables and class definitions
   - **Plain CSS**: update CSS custom properties in globals.css
4. Create `_redesign/THEME.md` documenting all tokens with examples

**Write:** Modified config files + `_redesign/THEME.md`

**If `--design-only` was specified, STOP HERE** and present the design system.

## Phase 3: Component Rebuild (~15 min, main agent ONLY — NEVER subagents)

**Do this yourself. NEVER spawn agents for component redesign work.** This rule exists because:
- Subagents lack the full design system context and make inconsistent choices
- Subagents have replaced Tailwind with inline styles (2026-03-26 NFL Draft incident)
- Subagents can't maintain visual consistency across components
- Only the main agent with THEME.md in context can ensure coherent design

**THE FRAMEWORK PRESERVATION RULE (NON-NEGOTIABLE):**
- If the project uses **Tailwind** → redesigned components use **Tailwind utility classes**
- If the project uses **CSS modules** → redesigned components use **CSS modules**
- If the project uses **styled-components** → redesigned components use **styled-components**
- **NEVER** replace one CSS approach with another during a redesign
- **NEVER** convert Tailwind classes to inline `style={{}}` objects
- **NEVER** convert utility classes to CSS custom properties accessed via `style={{var(--x)}}`
- A redesign changes the VISUAL OUTPUT, not the STYLING ARCHITECTURE

For EACH page (prioritize: landing > dashboard > detail pages > settings):
1. Read the current component
2. Read `_redesign/THEME.md` for design tokens
3. Read `~/.claude/skills/frontend-design/SKILL.md` differentiation protocol
4. **Update** the component (don't rewrite from scratch):
   - Swap color classes/values to new palette
   - Swap font classes to new typography
   - Adjust spacing and layout using existing framework's utilities
   - Preserve ALL existing functionality, state handling, data flow
   - Add responsive breakpoints using the EXISTING framework's approach
   - Add accessibility: ARIA labels, keyboard nav, contrast ratios
5. Follow `~/.claude/skills/react-best-practices/SKILL.md`

**Commit after every 2-3 components:**
```bash
git add -A && git commit -m "redesign: [component names] — [aesthetic name]"
```

**Write:** `_redesign/phase3_progress.md` — track which components are done, which remain.

## Phase 4: Backend Review (~5 min, 1 agent if backend exists)

Skip if no API routes exist. Otherwise spawn ONE **general-purpose agent**:
```
"BACKEND REVIEW AGENT

Context: Read _redesign/phase0_discovery.md.
Also read: ~/.claude/skills/senior-backend/SKILL.md.

Your task: Quick review of API routes and middleware. Check for:
- Security: unauthenticated routes, missing input validation
- Performance: N+1 queries, missing caching
- Contract: do API responses match what the new frontend expects?
Fix any P0/P1 issues directly. Write changes to _redesign/phase4_backend.md."
```

## Phase 5: Integration Test (~5 min, main agent)

Do this yourself:
1. Run `npm run build` — must pass with zero errors
2. Start dev server, visit every page
3. Take screenshots of each page — compare against Phase 0 screenshots
4. Check: console errors? Broken layouts? Missing data? Wrong colors?
5. If UFC project: run the 15-item checklist from ufc_website_maintenance_rules.md
6. Fix any issues found

**Write:** `_redesign/phase5_verification.md` — pass/fail per page with evidence.

## Phase 6: Visual QA (~3 min, main agent)

Final pixel-level review:
1. Check each page at mobile (375px), tablet (768px), desktop (1280px)
2. Verify: consistent spacing, typography hierarchy, color usage, no orphaned elements
3. Check: dark mode if applicable, print styles if needed
4. Verify accessibility: run through each page with tab key, check focus states
5. Compare the FEEL against Phase 1 direction — does it match the intended mood?

Fix any issues found. Commit.

## Phase 7: Deploy & Log (~3 min, main agent)

1. Final build check: `npm run build` or `npm run lint && npm run typecheck && npm run build`
2. Deploy if user wants: invoke `/deploy` or deploy manually
3. Log design decisions to project memory:
   - Aesthetic name, fonts, colors
   - Which components were rebuilt
   - Any compromises made (and why)
4. Log bugs found/fixed to `~/.claude/anti-patterns.md`

**Final commit:**
```bash
git add -A && git commit -m "redesign complete: [aesthetic name] — [N] pages, [N] components

Fonts: [primary] + [secondary]
Colors: [dominant] + [accent]
Layout: [approach]"
```

## Deliverable

```
REDESIGN COMPLETE
=================
Project: [name] | Aesthetic: [name]
Fonts: [primary] + [secondary]
Colors: [dominant hex] + [accent hex] + [neutral hex]
Layout: [approach]

Pages redesigned: [N] / [total]
Components rebuilt: [N]
Backend fixes: [N]
Build: passing ✓

Verification:
- Desktop: [pass/fail]
- Tablet: [pass/fail]
- Mobile: [pass/fail]
- Accessibility: [pass/fail]

Redesign files: _redesign/ (direction, theme, progress, verification)
```

## Design Principles
- **Opus only.** Creative design requires Opus-level reasoning. Sonnet and Haiku lack the aesthetic judgment for redesign work. The NFL Draft incident (2026-03-26) proved this — Sonnet agents replaced Tailwind with inline styles.
- **User chooses the direction.** Phase 1 is interactive — present options, don't dictate.
- **Main agent does ALL design and component work.** NEVER spawn subagents for redesign. No design system agents, no component agents. The main Opus agent does everything sequentially to maintain design coherence.
- **Max 1 subagent** (backend review only, and only if backend exists). Everything else is done by the main agent directly.
- **Load site-specific knowledge first.** If this site has a dedicated command (`/mmalogic`, `/update-diamond`, etc.), read its knowledge base. It contains display rules that MUST survive the redesign.
- **PRESERVE the CSS framework.** Tailwind stays Tailwind. CSS modules stay CSS modules. A redesign changes colors/fonts/layout — NOT the styling architecture.
- **Update, don't rewrite.** Swap classes and values in existing components. Don't rewrite 750-line components from scratch.
- **Inter-phase data via `_redesign/` files.** THEME.md is the single source of truth for all component work.
- **Token budget: ~45 min total.** `--design-only` mode: ~12 min. If hitting limits, commit progress and hand off.
- **Commit frequently.** Every 2-3 components, not one giant commit at the end.
- **Never use Inter, Roboto, or Arial.** The whole point of a redesign is to look different.
