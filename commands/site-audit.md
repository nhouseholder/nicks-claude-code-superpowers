Run a comprehensive website/webapp audit. Finds every issue across frontend, backend, design, and functionality — then fixes the critical ones.

**Sequential pipeline with pre-built skill agents. Complete each phase fully before starting the next.**

## Skill Pipeline (load at each phase — read SKILL.md, don't "apply mentally")

| Phase | Skills to Load |
|-------|---------------|
| Phase 0 | `website-guardian` (Rule Zero, baseline) |
| Phase 2 | `frontend-design`, `react-best-practices`, `senior-frontend` |
| Phase 3 | `senior-backend`, `code-reviewer`, `senior-architect` |
| Phase 4 | `screenshot-dissector`, `data-consistency-check` |
| Phase 5 | `error-memory` (log all bugs found) |
| Phase 6 | `qa-gate` (final verification) |

## Arguments
- `$ARGUMENTS` = project directory path (default: current directory)
- `--phase N` = skip to Phase N (assumes earlier phases complete)
- `--quick` = Phases 0-2 only (recon + frontend scan, no agents, ~5 min)

## Phase 0: Auto-detect & Orient (~30 seconds, main agent, no subagent)

Do this yourself — do NOT spawn an agent:
```bash
PROJECT_NAME=$(basename "$(pwd)")
echo "=== Project: $PROJECT_NAME ==="

# Tech stack
[ -f package.json ] && node -e "const p=require('./package.json'); console.log('Stack:', Object.keys(p.dependencies||{}).filter(d=>/react|next|vue|svelte|express|fastify/.test(d)).join(', '))"
[ -f requirements.txt ] && echo "Python project"
[ -f wrangler.toml ] && echo "Cloudflare Workers"

# Size
find src -name "*.tsx" -o -name "*.ts" -o -name "*.jsx" -o -name "*.js" 2>/dev/null | wc -l | xargs echo "Source files:"
find src -name "*.tsx" -o -name "*.jsx" 2>/dev/null | wc -l | xargs echo "Components:"

# Git state
git log --oneline -3 2>/dev/null
git status --short 2>/dev/null

# Running servers
ps aux | grep -E "(next|vite|express|flask|uvicorn|wrangler)" | grep -v grep 2>/dev/null || echo "No dev servers running"
```

Read anti-patterns and project memory yourself:
- `~/.claude/anti-patterns.md`
- Project MEMORY.md if it exists

**CRITICAL: Load site-specific domain knowledge.** Match the current project to its update command and READ IT:

| Project directory contains | Read this command for domain knowledge |
|---------------------------|---------------------------------------|
| `ufc-predict` or `mmalogic` | `~/.claude/commands/mmalogic.md` + `~/.claude/memory/topics/ufc_website_maintenance_rules.md` |
| `diamond-predictions` or `diamondpredictions` | `~/.claude/commands/update-diamond.md` |
| `courtside-ai` | `~/.claude/commands/update-courtside.md` |
| `Strain-Finder` or `mystrainai` | `~/.claude/commands/update-mystrainai.md` |
| `enhanced-health` or `enhancedhealthai` | `~/.claude/commands/update-enhancedhealth.md` |
| `aria-research` or `researcharia` | `~/.claude/commands/update-researcharia.md` |
| `dad-financial` or `nestwisehq` | `~/.claude/commands/update-nestwisehq.md` |

The update command contains: canonical paths, integration registry, domain rules, known anti-patterns, and the exact output format for that site. **Use this as your audit checklist — it defines what "correct" looks like for this specific site.**

If none match, fall back to generic audit.

**Write:** `_audit/phase0_context.md` with project summary + which site-specific command was loaded.

## Phase 1: Codebase Reconnaissance (~2 min, main agent)

Do this yourself — read the codebase directly:
1. Read `package.json` (dependencies, scripts)
2. Glob for all page/route files, list them
3. Glob for all API route files, list them
4. Read the main layout/app entry point
5. Check for config files (tailwind.config, next.config, tsconfig, etc.)

**Write:** `_audit/phase1_recon.md` — file counts, routes, tech stack, architecture notes.

## Phase 2: Frontend Scan (~5 min, 1 agent)

Spawn ONE **general-purpose agent**:
```
"FRONTEND AUDIT AGENT

Context: Read _audit/phase0_context.md and _audit/phase1_recon.md first.

Read and follow these protocols:
1. ~/.claude/skills/frontend-design/SKILL.md — anti-slop checklist
2. ~/.claude/skills/react-best-practices/SKILL.md — performance rules

Your task:
- Read every page/component file listed in phase1_recon.md
- For EACH file, check: accessibility (ARIA, contrast, touch targets), performance (unnecessary re-renders, missing memo, barrel imports), design quality (generic fonts? boring layouts?), responsive design, missing states (empty/loading/error)
- Read the site-specific update command identified in Phase 0 and check EVERY item in its integration registry and domain rules
- For UFC: read ~/.claude/memory/topics/ufc_website_maintenance_rules.md and check ALL 15 items
- For Diamond: verify both NHL and MLB tabs work, all GitHub Actions buttons trigger correctly
- For Courtside: verify admin page is intact (ALL tabs, ALL buttons — this was destroyed before)
- For ResearchAria: verify D1 database, paper search, login flow, auto-fetch pipeline
- For ALL sites: test every action button (Generate Picks, Refresh Data, etc.) — don't just check they render, click them and verify the response

Output format — write to _audit/phase2_frontend.md:
## P0 — Critical (crashes, security, data wrong)
- [file:line] [issue] [fix suggestion]

## P1 — High (broken features, bad UX)
- [file:line] [issue] [fix suggestion]

## P2 — Medium (design issues, performance)
- [file:line] [issue] [fix suggestion]

## P3 — Low (polish, minor improvements)
- [file:line] [issue] [fix suggestion]

## Stats
- Files scanned: N
- Issues found: P0: N, P1: N, P2: N, P3: N
"
```

**If `--quick` was specified, STOP HERE** and present Phase 2 findings.

## Phase 3: Backend Scan (~5 min, 1 agent)

Spawn ONE **general-purpose agent**:
```
"BACKEND AUDIT AGENT

Context: Read _audit/phase0_context.md and _audit/phase1_recon.md first.

Read and follow these protocols:
1. ~/.claude/skills/senior-backend/SKILL.md — audit checklist
2. ~/.claude/skills/audit/SKILL.md — secrets scanning

Your task:
- Read ALL API routes, middleware, auth logic, database queries
- Check for: hardcoded secrets/API keys, unauthenticated routes, SQL/command injection, missing CORS, N+1 queries, missing indexes, no error handling, god files
- Scan for secrets: grep for patterns matching API keys, tokens, passwords in source

Output format — write to _audit/phase3_backend.md:
[Same P0-P3 format as Phase 2]
"
```

## Phase 4: Visual Verification (~3 min, main agent)
**Skills:** `screenshot-dissector` + `data-consistency-check`

Do this yourself using Claude Preview or Claude in Chrome:
1. Read `~/.claude/skills/screenshot-dissector/SKILL.md` — follow the pixel-level examination protocol
2. Read `~/.claude/skills/data-consistency-check/SKILL.md` — validate all numbers/stats before presenting
3. Start the dev server if not running
4. Screenshot every main page/route
5. For each screenshot, apply `screenshot-dissector` protocol: examine every element, every value, every state
6. Apply `data-consistency-check`: profit>0 requires wins>0, W+L=total, etc.
7. Look for: broken layouts, missing data, wrong colors, truncated text, console errors
8. If UFC project: run the 15-item checklist from ufc_website_maintenance_rules.md with SPECIFIC values

**Write:** `_audit/phase4_visual.md` — visual issues with screenshots/descriptions.

## Phase 5: Fix Critical Issues (~10 min, main agent)

Do this yourself — do NOT spawn an agent for fixes:
1. Read `_audit/phase2_frontend.md` and `_audit/phase3_backend.md` and `_audit/phase4_visual.md`
2. Fix ALL P0 issues directly
3. Fix P1 issues if time permits
4. For each fix: verify the fix doesn't break baseline items

**Commit after all fixes:**
```bash
git add -A && git commit -m "site-audit: fix P0/P1 issues

[list each fix on its own line]"
```

## Phase 6: Final Verification (~2 min, main agent)

1. Re-check every page affected by fixes
2. Verify baseline items still work
3. Run build: `npm run build` (or equivalent) — must pass

**Write:** `_audit/phase6_final.md` — pass/fail for each verification item.

## Deliverable

```
SITE AUDIT COMPLETE
===================
Project: [name] | Stack: [framework] | Files: [N]

| Category | P0 | P1 | P2 | P3 | Fixed |
|----------|----|----|----|----|-------|
| Frontend |  N |  N |  N |  N |   N   |
| Backend  |  N |  N |  N |  N |   N   |
| Visual   |  N |  N |  N |  N |   N   |
| TOTAL    |  N |  N |  N |  N |   N   |

Fixed this session:
- [file]: [what was fixed]

Needs manual attention:
- [file:line]: [issue] — [why it needs human decision]

Audit files: _audit/ (6 phase reports)
```

## Design Principles
- **Main agent does most work.** Only 2 subagents max (frontend scan + backend scan). Everything else is direct.
- **Inter-phase data via files.** All phase output goes to `_audit/` directory. Each phase reads prior phases' files.
- **Token budget: ~30 min total.** Quick mode: ~5 min. If hitting rate limits, commit fixes so far and report.
- **Fixes are direct.** No "agent to fix" — the main agent applies fixes and verifies them.
- **One commit at the end** (not per-phase). Cleaner git history.
