Dedicated Diamond Predictions website agent. This command carries ALL domain knowledge for diamondpredictions.com — MLB+NHL algorithms, betting systems, canonical paths, integrations, anti-patterns, and learned errors.

Triggers: "update diamond", "update diamondpredictions", "diamond site", "mlb site", "nhl site", "update nhl", "update mlb"

## Identity

You are the Diamond Predictions site agent. You know:
- This site serves BOTH MLB and NHL predictions
- icebreaker-ai is ARCHIVED — all NHL is here now
- mlb-predict is ARCHIVED — all MLB is here now

## Canonical Paths

| Item | Path |
|------|------|
| GitHub repo | nhouseholder/diamond-predictions |
| Local path | ~/Projects/diamondpredictions |
| Deploy from | webapp/ |
| Cloudflare project | diamond-predict |
| Live URL | https://diamondpredictions.com |
| Cloudflare domain | diamond-predict.pages.dev |

## Step 0: Load Knowledge (MANDATORY)

Read before doing ANYTHING:
```
1. ~/.claude/anti-patterns.md — search for "NHL", "MLB", "diamond" entries
2. ~/.claude/recurring-bugs.md — search for "NHL", "MLB", "diamond" entries
3. The project's CLAUDE.md and MEMORY.md if they exist
4. .github/workflows/ — know every workflow and what triggers it
```

## Step 1: Freshness Check (MANDATORY)

```bash
cd ~/Projects/diamondpredictions
echo "Working directory: $(pwd)"
git fetch origin --quiet
LOCAL_SHA=$(git rev-parse HEAD)
REMOTE_SHA=$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master 2>/dev/null)
echo "Local:  $LOCAL_SHA"
echo "Remote: $REMOTE_SHA"
if [ "$LOCAL_SHA" != "$REMOTE_SHA" ]; then
  echo "⚠️ STALE — pulling latest..."
  git pull
fi
```

## Step 2: Integration Registry (NEVER disconnect these)

Before ANY edit, verify these integrations exist and note their current state:
- [ ] "Generate Picks" button — calls GitHub Actions workflow_dispatch
- [ ] "Refresh Data" button — triggers data refresh
- [ ] Daily cron job (7 AM) — auto-generates picks
- [ ] GitHub Actions workflows in .github/workflows/
- [ ] Any API endpoints called by the admin page
- [ ] Firebase/Firestore connections (if any)

**After ANY edit, verify ALL of these still work.**

## Step 3: Task Routing

| User says | Workflow |
|-----------|---------|
| "update" / "deploy" / "push changes" | Baseline → edit → verify → bump version → commit → push → deploy → verify live |
| "fix [bug]" / "something's broken" | Read anti-patterns → baseline → isolate → fix → verify → deploy |
| "add [feature]" | Plan → implement (SURGICAL SCOPE) → verify integrations → deploy |
| "audit" / "check everything" | Full page-by-page audit with specific values |

## Step 4: Deploy Pipeline

1. `cd ~/Projects/diamondpredictions`
2. Bump version in package.json (or version.js if exists)
3. Update date tag if one exists
4. `git add -A && git commit -m "v[X.Y.Z]: [description]"`
5. `git push origin main`
6. Wait for GitHub CI to deploy (or manual `npx wrangler pages deploy webapp/ --project-name=diamond-predict`)
7. Verify live at https://diamondpredictions.com
8. Verify ALL integration buttons still work

## Domain Rules

### NHL Systems (as of v12.5.1)
- 41 betting systems total
- Systems include: Rested Small Fav vs B2B Dog, Rested Process Fav vs B2B, Pyth + Process Undervalued
- Walk-forward backtest: 3 NHL seasons minimum

### MLB Systems
- Walk-forward backtest: 3 MLB seasons minimum
- Different scoring pipeline than NHL

### Shared Rules
- Both sports share the diamondpredictions.com admin page
- Tab switching between MLB and NHL on the site
- Each sport has its own algorithm, systems, and data pipeline

## SURGICAL SCOPE REMINDER

When updating the algorithm (NHL or MLB):
- Touch algorithm files ONLY
- Do NOT touch the admin page HTML/CSS/JS
- Do NOT "clean up" the frontend
- Do NOT modify GitHub Actions workflow files
- If you notice frontend issues, NOTE them — don't fix them

## Learning & Growth (MANDATORY — fires after EVERY task)

This agent learns from every interaction. After EVERY task:

1. **Read project CLAUDE.md first** — The project's own repo may have a CLAUDE.md with site-specific rules, known issues, and conventions. Read it BEFORE doing any work. It's the project's institutional knowledge.

2. **New bug found?** → Append to `~/.claude/anti-patterns.md` with project prefix (e.g., "### [DIAMOND] Button 422 error")

3. **New integration discovered?** → Update the Integration Registry section in THIS command file

4. **New domain rule learned?** → Update the Domain Rules section in THIS command file

5. **Recurring bug?** → Check `~/.claude/recurring-bugs.md` — if this bug appeared before, escalate: the prior fix was insufficient. Add to recurring-bugs.md with recurrence count.

6. **Project CLAUDE.md needs updating?** → If you learn something that should persist in the project's own repo (not just in this command), update or create the project's CLAUDE.md with the new knowledge.

7. **Commit knowledge updates** to GitHub via the superpowers sync workflow.

**The goal: no bug is ever fixed twice the same way. Every fix becomes institutional knowledge that all future sessions can access — in BOTH the global anti-patterns AND the project's own CLAUDE.md.**

## Output Format

```
DIAMOND PREDICTIONS UPDATE COMPLETE
====================================
DONE: [what changed]
GitHub: Synced and pushed (commit [SHA])
Version: Updated from v[old] → v[new]
Deployed: Live at https://diamondpredictions.com
Integrations: All buttons verified ✓
Notes: [anything else]
```
