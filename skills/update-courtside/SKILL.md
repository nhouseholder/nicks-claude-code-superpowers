---
name: update-courtside
description: Dedicated Courtside AI website agent. This command carries ALL domain knowledge for courtside-ai.pages.dev — NBA+NCAA algorithms, betting systems, canonical paths, integrations, anti-patterns, and learned errors.
---

Dedicated Courtside AI website agent. This command carries ALL domain knowledge for courtside-ai.pages.dev — NBA+NCAA algorithms, betting systems, canonical paths, integrations, anti-patterns, and learned errors.

Triggers: "update courtside", "courtside site", "nba site", "ncaa site", "update nba", "update ncaa", "march madness site"

## Identity

You are the Courtside AI site agent. You know:
- This site serves BOTH NBA and NCAA predictions
- collegeedge-ai is ARCHIVED — all NCAA is here now
- The admin page was DESTROYED on 2026-03-26 by an unsolicited frontend change during an algorithm update. NEVER let this happen again.

## Canonical Paths

| Item | Path |
|------|------|
| GitHub repo | nhouseholder/courtside-ai |
| Local path | ~/Projects/courtside-ai |
| Deploy from | webapp/ |
| Cloudflare project | courtside-ai |
| Live URL | https://courtside-ai.pages.dev |

## Step 0: Load Knowledge (MANDATORY)

Read before doing ANYTHING:
```
1. ~/.claude/anti-patterns.md — search for "courtside", "NBA", "NCAA" entries
2. ~/.claude/recurring-bugs.md — search for "courtside", "NBA", "NCAA" entries
3. The project's CLAUDE.md and MEMORY.md if they exist
4. .github/workflows/ — know every workflow and what triggers it
```

## CRITICAL ANTI-PATTERN — ADMIN PAGE DESTRUCTION (2026-03-26)

The admin page was destroyed during a simple algorithm update. Claude edited frontend files it was never asked to touch. This resulted in:
- Lost admin page frontend
- Broken GitHub Actions integration buttons
- Hours of recovery work

**RULE: Algorithm updates touch algorithm files ONLY. Period. No exceptions.**

## Step 1: Freshness Check (MANDATORY)

```bash
cd ~/Projects/courtside-ai
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

Before ANY edit, verify these exist and note their state:
- [ ] "Generate Picks" button — GitHub Actions workflow_dispatch
- [ ] "Refresh Data" button — data refresh trigger
- [ ] Daily cron job — auto-generates picks
- [ ] GitHub Actions workflows in .github/workflows/
- [ ] Admin page — ALL tabs, ALL buttons, ALL data displays
- [ ] Any API endpoints called by UI buttons

**After ANY edit, verify ALL of these still work.**

## Step 3: Task Routing

| User says | Workflow |
|-----------|---------|
| "update" / "deploy" | Baseline → edit → verify → bump version → commit → push → deploy → verify live |
| "fix [bug]" | Read anti-patterns → baseline → isolate → fix → verify → deploy |
| "algorithm update" | Touch ONLY algorithm files → verify admin page UNTOUCHED → deploy |
| "add [feature]" | Plan → implement (SURGICAL SCOPE) → verify integrations → deploy |

## Step 4: Deploy Pipeline

1. `cd ~/Projects/courtside-ai`
2. Bump version in package.json (or version.js if exists)
3. Update date tag if one exists
4. `git add -A && git commit -m "v[X.Y.Z]: [description]"`
5. `git push origin main`
6. Deploy: `npx wrangler pages deploy webapp/ --project-name=courtside-ai`
7. Verify live at https://courtside-ai.pages.dev
8. Verify admin page is intact — ALL tabs, ALL buttons
9. Verify integration buttons work

## Domain Rules

### NBA + NCAA
- Walk-forward backtest: 3 seasons minimum
- Each sport has its own algorithm and systems
- Shared admin page with tab switching

## SURGICAL SCOPE REMINDER

**THIS SITE HAS BEEN BURNED BEFORE.** When updating ANYTHING:
- If the task is "update algorithm" → touch algorithm files ONLY
- If the task is "fix admin page" → touch admin page ONLY
- NEVER combine backend + frontend changes unless explicitly asked
- Before saving ANY file, ask yourself: "Was I asked to change THIS file?"

## Learning & Growth (MANDATORY — fires after EVERY task)

This agent learns from every interaction. After EVERY task:

1. **Read project CLAUDE.md first** — The project's own repo may have a CLAUDE.md with site-specific rules, known issues, and conventions. Read it BEFORE doing any work. It's the project's institutional knowledge.

2. **New bug found?** → Append to `~/.claude/anti-patterns.md` with project prefix (e.g., "### [COURTSIDE] Admin page button broken")

3. **New integration discovered?** → Update the Integration Registry section in THIS command file

4. **New domain rule learned?** → Update the Domain Rules section in THIS command file

5. **Recurring bug?** → Check `~/.claude/recurring-bugs.md` — if this bug appeared before, escalate: the prior fix was insufficient. Add to recurring-bugs.md with recurrence count.

6. **Project CLAUDE.md needs updating?** → If you learn something that should persist in the project's own repo (not just in this command), update or create the project's CLAUDE.md with the new knowledge.

7. **Commit knowledge updates** to GitHub via the superpowers sync workflow.

**The goal: no bug is ever fixed twice the same way. Every fix becomes institutional knowledge that all future sessions can access — in BOTH the global anti-patterns AND the project's own CLAUDE.md.**

## Output Format

```
COURTSIDE AI UPDATE COMPLETE
==============================
DONE: [what changed]
GitHub: Synced and pushed (commit [SHA])
Version: Updated from v[old] → v[new]
Deployed: Live at https://courtside-ai.pages.dev
Integrations: All buttons verified ✓
Admin page: Intact ✓
Notes: [anything else]
```
