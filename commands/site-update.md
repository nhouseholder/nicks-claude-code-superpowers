Update a website/webapp safely. Baseline → changes → verify → deploy. The guardrail command — ensures updates don't break what already works.

**Sequential pipeline with pre-built skill agents. Do NOT skip phases.**

## Skill Pipeline (load at each phase — read SKILL.md, don't "apply mentally")

| Phase | Skills to Load |
|-------|---------------|
| Phase 0 | `website-guardian` (Rule Zero, gate check) |
| Phase 1 | `screenshot-dissector` (baseline snapshot quality) |
| Phase 3 | `frontend-design` and/or `senior-backend` (based on change type) |
| Phase 4 | `data-consistency-check`, `qa-gate` (verification) |
| Phase 6 | `error-memory` (log any bugs found/fixed) |

## Arguments
- `$ARGUMENTS` = specific update description (e.g., "add dark mode toggle", "update hero section copy")
- `--phase N` = skip to Phase N
- `--no-deploy` = skip deployment, just make and verify changes
- If no argument, ask what needs updating

## Phase 0: Gate Check (~30 seconds, main agent)

**MANDATORY — prevents deploying from stale or wrong state.**

```bash
PROJECT_NAME=$(basename "$(pwd)")
echo "=== GATE CHECK ==="
echo "Directory: $(pwd)"
echo "Branch: $(git branch --show-current 2>/dev/null)"

# Verify on main/master — never deploy from feature branches
BRANCH=$(git branch --show-current 2>/dev/null)
if [ "$BRANCH" != "main" ] && [ "$BRANCH" != "master" ]; then
  echo "⚠️ NOT ON MAIN — you are on branch: $BRANCH"
  echo "Switch to main before deploying, or use --no-deploy"
fi

# Check local matches remote (FAILSAFE 8)
git fetch origin --quiet 2>/dev/null
LOCAL_SHA=$(git rev-parse HEAD 2>/dev/null)
REMOTE_SHA=$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master 2>/dev/null)
if [ "$LOCAL_SHA" != "$REMOTE_SHA" ]; then
  echo "⚠️ LOCAL IS STALE — pulling..."
  git pull
fi
echo "Local SHA:  $LOCAL_SHA"
echo "Remote SHA: $REMOTE_SHA"

# Check current version (FAILSAFE 3)
cat VERSION 2>/dev/null || node -e "console.log(require('./package.json').version)" 2>/dev/null || echo "No version file"

# Stack detection
[ -f package.json ] && node -e "const p=require('./package.json'); console.log('Stack:', Object.keys(p.dependencies||{}).filter(d=>/react|next|vue|svelte|express/.test(d)).join(', '))"

# Recent commits
git log --oneline -3 2>/dev/null
git status --short 2>/dev/null
```

**If branch is not main/master:** Ask user before proceeding. Deploying from a feature branch overwrites production.
**If local is behind remote:** Pull first. Never build on stale code.

Read anti-patterns and project memory. If UFC project, read `~/.claude/memory/topics/ufc_website_maintenance_rules.md`.

## Phase 1: Baseline Snapshot (~2 min, main agent)

Do this yourself:
1. Start dev server if not running (check `ps aux | grep -E "next|vite|express"` first to avoid port conflicts)
2. Take screenshots or read current state of every page affected by this update
3. Record specific values for everything that currently works — numbers, text, colors, layouts
4. Note the current version number from VERSION or package.json
5. Note the build/deploy status

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

2. **CREDENTIAL PROTECTION (MANDATORY):**
   - NEVER remove or overwrite Firebase, Supabase, Stripe, or any auth credentials
   - If touching config files, verify all credential env vars are still present after your edit
   - `grep -c "FIREBASE\|SUPABASE\|STRIPE\|API_KEY" <file>` before AND after — counts must match

3. If UFC/MMALogic project — **DATA SYNC (MANDATORY):**
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

1. **Version check (FAILSAFE 3):** Compare current version to what was recorded in Phase 1 baseline. If the version is LOWER than what's in production, ABORT — you are deploying a regression.

2. **Bump version number (MANDATORY):**
   - Patch bump (x.y.Z+1) for fixes and small changes
   - Minor bump (x.Y+1.0) for new features
   - Update in version.js, package.json, or wherever the project stores its version
   - Update any "last updated" date display on the site (footer, version tag, etc.)

3. **Clean up temp files:**
```bash
rm -rf _update/ 2>/dev/null
```

4. **Commit and push (not git add -A):**
```bash
# Stage only the files you intentionally changed — never blind add
git add [specific files you changed]
git commit -m "v[X.Y.Z]: [description of what changed]"
git push origin main
```

5. Deploy using project-appropriate method (invoke `/deploy` or manual)

6. **Post-deploy verification (MANDATORY):** Open the live site and confirm:
   - New version number is displayed
   - Updated date is displayed
   - The actual changes are visible and working

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
Branch: [main/master] ✓
Version: [before] → [after] (bumped ✓)
Date tag: updated ✓
Changed: [list of specific files]
Baseline: [N] items verified — [all ✓ / N failed → fixed]
Build: passing ✓
Pushed: origin/main ✓
Deployed: [yes/no/rolled back]
Live verification: version + date + changes confirmed ✓
Bugs found: [N] | Fixed: [N]
Credentials: verified intact ✓
```

## Design Principles
- **Main agent does everything.** Zero subagents. This is the lightweight command.
- **Gate check before anything else.** Stale code + deploy = production regression.
- **Baseline is sacred.** If ANYTHING from baseline breaks, fix it before declaring done.
- **Specific values, not "looks fine."** Every baseline check states what it sees.
- **Specific files, not `git add -A`.** Never accidentally commit temp files or credentials.
- **Never touch credentials.** Count them before and after edits.
- **Clean up after yourself.** Remove `_update/` before committing.
- **Token budget: ~10 min.** This is the fast, safe update path.
- **One commit** for the whole update.
