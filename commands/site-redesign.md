Redesign a website/webapp with production-grade quality. Takes an existing site and rebuilds the visual layer with a distinctive aesthetic.

**Sequential pipeline. Each phase produces artifacts the next phase consumes.**

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

## Phase 2: Design System (~5 min, 1 agent)

Spawn ONE **general-purpose agent**:
```
"DESIGN SYSTEM AGENT

Context: Read _redesign/phase0_discovery.md and _redesign/phase1_direction.md.
Also read: ~/.claude/skills/ui-design-system/SKILL.md and ~/.claude/skills/ui-ux-pro-max/SKILL.md.

Your task: Build the design foundation.
1. Create/update tailwind.config with: custom colors (from direction), font families, spacing scale, border radius tokens, shadow tokens, animation keyframes
2. Create/update globals.css with: CSS custom properties mirroring Tailwind tokens, @font-face or Google Fonts imports for chosen fonts, base styles
3. Create a theme reference file: _redesign/THEME.md documenting all tokens with examples

Output: Modified tailwind.config + globals.css + _redesign/THEME.md. Write all files directly."
```

**If `--design-only` was specified, STOP HERE** and present the design system.

## Phase 3: Component Rebuild (~15 min, main agent, component by component)

Do this yourself — do NOT spawn agents for individual components. You need the design system context.

For EACH page (prioritize: landing > dashboard > detail pages > settings):
1. Read the current component
2. Read `_redesign/THEME.md` for design tokens
3. Read `~/.claude/skills/frontend-design/SKILL.md` differentiation protocol:
   - Purpose → Tone → Constraints → "What makes this UNFORGETTABLE?"
4. Rewrite the component applying:
   - New typography (from THEME.md)
   - New color palette
   - New layout approach
   - All states: empty, loading, error, success
   - Responsive: mobile-first, tablet, desktop
   - Accessible: ARIA labels, keyboard nav, contrast ratios
5. Follow `~/.claude/skills/react-best-practices/SKILL.md`:
   - No barrel imports, proper memoization, lazy loading where appropriate

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
- **User chooses the direction.** Phase 1 is interactive — present options, don't dictate.
- **Main agent does component work.** Agents can't maintain design consistency across components — only the main agent with THEME.md in context can.
- **Max 2 subagents** (design system + backend review). Everything else is direct.
- **Inter-phase data via `_redesign/` files.** THEME.md is the single source of truth for all component work.
- **Token budget: ~45 min total.** `--design-only` mode: ~12 min. If hitting limits, commit progress and hand off.
- **Commit frequently.** Every 2-3 components, not one giant commit at the end.
- **Never use Inter, Roboto, or Arial.** The whole point of a redesign is to look different.
