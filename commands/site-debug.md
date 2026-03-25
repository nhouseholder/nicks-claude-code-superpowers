Debug a website/webapp systematically using the full Debugger Agent pipeline. Finds bugs, fixes them, verifies fixes, and logs everything permanently.

**This command calls agents in order. Do NOT skip phases.**

## Arguments
- `$ARGUMENTS` = bug description, URL, screenshot, or project directory
- If no argument provided:
  1. Check `git diff --stat` for recent changes that might have caused the bug
  2. Check `~/.claude/anti-patterns.md` for recently logged bugs in this project
  3. Check for running dev servers and their console output
  4. Check `~/.claude/recurring-bugs.md` for known issues
  5. If still unclear, THEN ask the user — but present what you found: "I see recent changes to [files] and a running server on port [N]. What's the issue?"

## Partial Run
To re-run a specific phase: `/site-debug --phase N`
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

## Phase 1: Read History (pre-debug-check)
BEFORE any fix attempt:
- Read `~/.claude/anti-patterns.md` — has this bug been seen before?
- Read `~/.claude/recurring-bugs.md` — is this a repeat offender?
- Read project MEMORY.md for prior context
- If bug was fixed before: announce it, show history, escalate approach

## Phase 2: Baseline Snapshot (website-guardian)
Spawn a **general-purpose agent** with this briefing:
"You are a Baseline agent. Read and follow: ~/.claude/skills/website-guardian/SKILL.md — follow its checklist.
Also read: ~/.claude/anti-patterns.md (known failure patterns) and the project's MEMORY.md if it exists.
Your task: Screenshot or read current state of the broken page. Record what IS working (so we don't break it while fixing). Record the exact symptoms of the bug.
Output: Baseline snapshot document listing all working items and exact bug symptoms."

## Phase 3: Isolate (isolate-before-iterate)
- Can this bug be reproduced in a minimal test?
- Write a 5-line reproduction script before running the full app
- If screenshots available: use screenshot-dissector for pixel-level analysis

If the bug can't be reproduced in isolation, log WHY (external dependency, race condition, state-dependent) and proceed with extra caution — add more verification in Phase 6.

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-debug Phase 3: isolation test"`

## Phase 4: Diagnose (systematic-debugging)
Spawn a **general-purpose agent** with this briefing:
"You are a Diagnosis agent. Read and follow: ~/.claude/skills/systematic-debugging/SKILL.md — follow its checklist.
Also read: ~/.claude/anti-patterns.md (known failure patterns) and the project's MEMORY.md if it exists.
Your task: Form a hypothesis for the most likely cause. Test the hypothesis with ONE targeted check. If wrong, form a new hypothesis (max 3 per approach). Do NOT change code until you have a diagnosis.
Output: Diagnosis with root cause identification and evidence."

## Phase 5: Fix (senior-dev-mindset)
Spawn a **general-purpose agent** with this briefing:
"You are a Fix agent. Read and follow: ~/.claude/skills/senior-dev-mindset/SKILL.md — follow its checklist.
Also read: ~/.claude/anti-patterns.md (known failure patterns) and the project's MEMORY.md if it exists.
Your task: Apply a targeted fix based on the diagnosis. Follow senior-dev-mindset checklist for the domain (Frontend/Backend). If website: follow website-guardian fix protocol.
Output: Description of fix applied with file paths and line numbers."

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-debug Phase 5: fix applied"`

## Phase 6: Verify (data-consistency-check + website-guardian)
Spawn a **general-purpose agent** with this briefing:
"You are a Verification agent. Read and follow these skill protocols:
1. ~/.claude/skills/data-consistency-check/SKILL.md — follow its checklist
2. ~/.claude/skills/website-guardian/SKILL.md — follow its checklist
Also read: ~/.claude/anti-patterns.md (known failure patterns) and the project's MEMORY.md if it exists.
Your task: Check EVERY baseline item — still working? Run data-consistency-check on any numbers/stats. Scan output for impossible data (Rule 18). If webapp-testing Playwright available: run automated verification. If fix broke something else: fix THAT before declaring done. If the bug could not be reproduced in isolation (Phase 3), apply EXTRA verification: test with multiple inputs, check edge cases, verify in both dev and production-like environments.
Output: Verification results — pass/fail for each baseline item."

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-debug Phase 6: verification fixes"`

## Phase 7: Log Permanently (error-memory)
Follow error-memory SKILL.md:
- Root cause (not just symptoms)
- Flawed assumption (what was believed that was false)
- Reasoning lesson (one-line rule to prevent recurrence)
- Append to `~/.claude/anti-patterns.md`
- If recurring: update `~/.claude/recurring-bugs.md` with escalated analysis

## Phase 8: Verify Log
- Confirm anti-patterns.md was updated
- If website bug: update site-update-protocol checklist if new failure mode found

**Checkpoint:** If code was changed in this phase, commit before proceeding:
`git add -A && git commit -m "site-debug Phase 8: bug logged to anti-patterns"`

## Output
```
SITE DEBUG COMPLETE
===================
Bug: [description]
Root cause: [what was actually wrong]
Fix: [what was changed] — [files]
Verified: baseline ✓ | data-check ✓ | visual ✓
Logged: anti-patterns.md ✓ | recurring-bugs.md [✓/n/a]
Carelessness type: [from website-guardian table]
Prevention rule: [one-line rule for future agents]
```
