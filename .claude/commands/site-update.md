Update a website/webapp safely. Baseline → changes → verify → deploy. The guardrail command — ensures updates don't break what already works.

**Sequential pipeline. Do NOT skip phases.**

## Arguments
- `$ARGUMENTS` = specific update description (e.g., "add dark mode toggle", "update hero section copy")
- `--phase N` = skip to Phase N
- `--no-deploy` = skip deployment, just make and verify changes
- If no argument, ask what needs updating

## Phase 0: Orient (~30 seconds, main agent)

```bash
PROJECT_NAME=$(basename "$(pwd)")
[ -f package.json ] && node -e "const p=require('./package.json'); console.log('Stack:', Object.keys(p.dependencies||{}).filter(d=>/react|next|vue|svelte|express/.test(d)).join(', '))"
git log --oneline -3 2>/dev/null
git status --short 2>/dev/null
```

Read anti-patterns and project memory. If UFC project, read `~/.claude/memory/topics/ufc_website_maintenance_rules.md`.

## Phase 1: Baseline Snapshot (~2 min, main agent)

Do this yourself:
1. Start dev server if not running
2. Take screenshots or read current state of every page affected by this update
3. Record specific values for everything that currently works — numbers, text, colors, layouts
4. Note the build/deploy status

**Write:** `_update/phase1_baseline.md` — every working item with specific values. NOT "looks fine."

## Phase 2: Plan (~1 min, main agent)

Assess complexity:
- **Simple** (1-2 files, clear scope): proceed directly to Phase 3
- **Complex** (3+ files, unclear scope): write a brief plan in `_update/phase2_plan.md` listing files to change and order of operations

## Phase 3: Make Changes (~varies, main agent)

Do this yourself:
1. Apply the changes. Follow skill protocols based on what you're changing:
   - Frontend: read `~/.claude/skills/frontend-design/SKILL.md` patterns
   - Backend: read `~/.claude/skills/senior-backend/SKILL.md` patterns
   - UFC site: read `~/.claude/skills/site-update-protocol/SKILL.md` rules + data sync step
2. If UFC/MMALogic project — **DATA SYNC (MANDATORY):**
   - Sync all 7 data files from `ufc-predict/webapp/frontend/public/data/` → `webapp/frontend/public/data/`
   - Check `diff -rq` for source file divergence
   - Verify registry totals include ALL 5 bet types
   - Check algorithm_stats.json includes parlay_pnl

## Phase 4: Verify (~3 min, main agent)

Do this yourself:
1. Re-check EVERY item from Phase 1 baseline — still working? State specific values.
2. Verify the update works as intended
3. If visual change: take new screenshots, compare against Phase 1
4. If data change: spot-check at least 2 values end-to-end
5. If UFC project: run the 15-item checklist with specific values
6. Run build: `npm run build` or equivalent — must pass
7. If anything from baseline is broken: FIX IT before proceeding

If the fix creates regressions, iterate until baseline is restored AND the update works.

## Phase 5: Deploy (~2 min, main agent)

Skip if `--no-deploy` was specified.

1. Commit:
```bash
git add -A && git commit -m "update: [description of what changed]"
```
2. Deploy using project-appropriate method (invoke `/deploy` or manual)
3. Post-deploy: verify the live site matches what you saw in Phase 4

**If deploy fails or live site has regressions:**
1. Rollback: `npx wrangler rollback` or `git revert HEAD`
2. Log failure to anti-patterns.md
3. Report what failed

## Phase 6: Log (~30 seconds, main agent)

If any bugs were found/fixed during verification:
- Log to `~/.claude/anti-patterns.md` with root cause and prevention rule
- Update project memory if the update changes how the site works

## Deliverable

```
SITE UPDATE COMPLETE
====================
Update: [description]
Changed: [list of files]
Baseline: [N] items verified — [all ✓ / N failed → fixed]
Build: passing ✓
Deployed: [yes/no/rolled back]
Bugs found: [N] | Fixed: [N]

Update files: _update/ (baseline, plan if complex)
```

## Design Principles
- **Main agent does everything.** Zero subagents. This is the lightweight command.
- **Baseline is sacred.** If ANYTHING from baseline breaks, fix it before declaring done.
- **Specific values, not "looks fine."** Every baseline check states what it sees.
- **Token budget: ~10 min.** This is the fast, safe update path.
- **One commit** for the whole update.
