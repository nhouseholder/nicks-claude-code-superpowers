Update a website/webapp safely using the composite agent pipeline. Follows website-guardian protocol: baseline → changes → verify → deploy.

**This command calls agents in order. Do NOT skip phases.**

## Arguments
- `$ARGUMENTS` = project directory or specific update description
- If no argument, ask what needs updating

## Partial Run
To re-run a specific phase: `/site-update --phase N`
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

## Phase 1: Baseline Snapshot (Website Guardian)
Spawn a **general-purpose agent** with this briefing:
"You are a Baseline agent. Read and follow: ~/.claude/skills/website-guardian/SKILL.md — follow its checklist.
Also read: ~/.claude/anti-patterns.md (known failure patterns) and the project's MEMORY.md if it exists.
Your task: Screenshot or read current state of every affected page. Record what's currently working (specific values, not 'looks fine'). Note the current build/deploy status.
Output: Baseline snapshot document listing all working items with specific values."

## Phase 2: Plan the Update (Planner Agent — Priority 1 skills)
Spawn a **general-purpose agent** with this briefing:
"You are a Planner agent. Read and follow these skill protocols:
1. ~/.claude/skills/brainstorming/SKILL.md — follow its checklist
2. ~/.claude/skills/writing-plans/SKILL.md — follow its checklist
Also read: ~/.claude/anti-patterns.md (known failure patterns) and the project's MEMORY.md if it exists.
Your task: Determine if this is a simple update or complex change. If complex (3+ files): write PLAN.md first. If simple: proceed directly.
Output: Update plan or 'simple — proceeding directly'."

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-update Phase 2: update plan"`

## Phase 3: Make Changes (Frontend Agent or Backend Agent)
Based on what's being updated:
- **Frontend changes** → Spawn a **general-purpose agent** with this briefing:
  "You are a Frontend agent. Read and follow these skill protocols:
  1. ~/.claude/skills/frontend-design/SKILL.md — follow its checklist
  2. ~/.claude/skills/ui-ux-pro-max/SKILL.md — follow its checklist
  3. ~/.claude/skills/react-best-practices/SKILL.md — follow its checklist
  4. ~/.claude/skills/senior-frontend/SKILL.md — follow its checklist
  5. ~/.claude/skills/senior-dev-mindset/SKILL.md — follow its checklist
  Also read: ~/.claude/anti-patterns.md (known failure patterns) and the project's MEMORY.md if it exists.
  Your task: [specific frontend changes].
  Output: List of files changed with descriptions."
- **Backend changes** → Spawn a **general-purpose agent** with this briefing:
  "You are a Backend agent. Read and follow these skill protocols:
  1. ~/.claude/skills/senior-backend/SKILL.md — follow its checklist
  2. ~/.claude/skills/senior-dev-mindset/SKILL.md — follow its checklist
  Also read: ~/.claude/anti-patterns.md (known failure patterns) and the project's MEMORY.md if it exists.
  Your task: [specific backend changes].
  Output: List of files changed with descriptions."
- **Both** → Frontend first, then Backend

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-update Phase 3: changes applied"`

## Phase 4: Verify (Debugger Agent — Priority 1 skills)
Spawn a **general-purpose agent** with this briefing:
"You are a Verification agent. Read and follow these skill protocols:
1. ~/.claude/skills/data-consistency-check/SKILL.md — follow its checklist
2. ~/.claude/skills/website-guardian/SKILL.md — follow its checklist
Also read: ~/.claude/anti-patterns.md (known failure patterns) and the project's MEMORY.md if it exists.
Your task: Check EVERY item from the Phase 1 baseline — is it still working? Run data-consistency-check on any displayed numbers. If webapp-testing Playwright is available, run automated checks. If anything from baseline is broken, FIX IT before proceeding.
Output: Verification results — pass/fail for each baseline item."

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-update Phase 4: verification fixes"`

## Phase 5: Deploy (Deploy Agent)
- Invoke /deploy via Skill tool
- Follow website-guardian post-deploy verification
- Follow site-update-protocol if UFC/mmalogic project
- Visual verification of every affected page

If Phase 5 deploy fails or verification shows regressions:
1. Rollback: `npx wrangler rollback` or `git revert HEAD && npx wrangler deploy`
2. Log the failure to anti-patterns.md
3. Report: what was deployed, what broke, what was rolled back

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-update Phase 5: deploy"`

## Phase 6: Log (Error Memory)
- If any bugs were found/fixed, log to anti-patterns.md via error-memory
- Update project memory with what changed

## Output
```
SITE UPDATE COMPLETE
====================
Changed: [list of files]
Baseline: [all items verified ✓ or ✗]
Deployed: [yes/no]
Bugs found: [N] | Fixed: [N]
```
