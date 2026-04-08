# Handoff — superpowers — 2026-04-08 00:45
## Model: Claude Sonnet 4.6
## Previous handoff: handoff_nicks-claude-code-superpowers_2026-04-07_1628.md
## GitHub repo: nhouseholder/nicks-claude-code-superpowers
## Local path: ~/ProjectsHQ/superpowers
## Last commit date: 2026-04-07 23:16:56 -0700

---

## 1. Session Summary
User wanted two new hooks to enforce the Opus-plan/Sonnet-execute workflow: (1) auto-inject Sonnet-proof plan format requirements when entering plan mode, and (2) auto-switch the model to Sonnet when a plan is approved. The plan format injection works cleanly. The model switch hit a hard platform constraint — mid-session model switching from hooks is impossible; only new sessions pick up settings.json changes. Multiple iterations landed on the current design: block Opus on first Edit/Write after a plan, then detect "go" in UserPromptSubmit to write Sonnet to settings.json before the model processes the message (relies on Claude Code hot-reloading settings between hook and model invocation).

## 2. What Was Done
- **plan-mode-enforcer.py (new hook)**: UserPromptSubmit hook that detects plan intent, injects MANDATORY Sonnet-proof plan format requirements (exact code, exact paths, banned vague language), cleans old plan files, and activates guard. Also detects "go" keyword — writes `claude-sonnet-4-6` to settings.json before model processes the turn.
- **plan-execution-guard.py (new hook)**: PreToolUse:Edit|Write hook that blocks Opus from executing after a plan. Uses `.plan-guard-active` file as signal. One-shot: blocks once, writes Sonnet to settings.json, removes guard, instructs Claude to tell user to type "go".
- **settings.json updated**: Registered `plan-mode-enforcer.py` first in UserPromptSubmit (before token-advisor, improve-prompt). Registered `plan-execution-guard.py` first in PreToolUse:Edit|Write.
- **plan-exit-model-switch.py archived**: First (broken) attempt that used PostToolUse:ExitPlanMode — harness-internal tool, hook never fires. Archived as `plan-exit-model-switch.ARCHIVED.py`.
- **CLAUDE.md updated (both copies)**: Added `plan-mode-enforcer.py` and `plan-execution-guard.py` to hooks list.
- **10 commits** across multiple fix iterations (ceaba78 → b4543d3).

## 3. What Failed (And Why)
- **PostToolUse:ExitPlanMode hook (plan-exit-model-switch.py)**: ExitPlanMode is a harness-internal tool. PostToolUse does NOT fire for it. Hook was dead from birth. Archived.
- **Marker file approach (v1)**: plan-mode-enforcer wrote `.plan-switch-pending` on keyword detection, guard read it. Failed because plan mode is entered via UI button — user doesn't type "plan", so enforcer never fired and marker was never written.
- **Consumed marker escape hatch**: Guard allowed through on second attempt once consumed. This let Opus slip through on retry. Fixed by making block persistent until guard file deleted.
- **Bash in guard matcher**: Guard matched `Bash|Edit|Write` — blocked read-only Bash calls during plan exploration. Fixed to `Edit|Write` only.
- **settings.json model check**: Guard checked settings.json to see if "already on Sonnet" — caused false allow-through when Sonnet session ran.
- **settings.json hot-reload not confirmed**: Writing Sonnet to settings.json in UserPromptSubmit hook BEFORE model processes MIGHT work if Claude Code hot-reloads between hook and model invocation — unconfirmed in live use.

## 4. What Worked Well
- Plan file recency approach for guard trigger — clean, no keywords needed.
- One-shot block pattern: write guard → block once → instruct user → allow through.
- Testing hooks by piping mock JSON in shell — fast feedback loop without spawning sessions.
- Diagnosing root cause before pivoting (most of the time).

## 5. What The User Wants
- Fully automated Opus→Sonnet switch when clicking "approve plan and start coding" — zero manual steps.
- Plans that are ultra-specific and mechanically executable (exact code, exact paths, zero pseudocode).
- Verbatim: "when i press approve plan and start coding it still does not auto switch to sonnet"
- Verbatim: "replace step 3 with something automated"
- Verbatim: "when prompted, if i type and send 'go' it should auto run model sonnet"
- User frustrated by repeated failed attempts — wants it to actually work end-to-end.

## 6. In Progress (Unfinished)
**The "go" → Sonnet switch is unverified in live use.** The hook writes `claude-sonnet-4-6` to settings.json in UserPromptSubmit BEFORE the model processes the message. Whether Claude Code hot-reloads settings between hook and model invocation is unknown. Needs live test:
1. Switch to Opus → enter plan mode → give task
2. Click approve → type "go"
3. Check which model is executing (Sonnet or Opus?)

## 7. Blocked / Waiting On
- **Platform confirmation**: Whether settings.json hot-reload between hooks and model invocation works. Needs live test.
- Nothing else blocked.

## 8. Next Steps (Prioritized)
1. **Live test "go" flow** — fresh Opus session, plan mode, approve, type "go", confirm model. This is the #1 open question.
2. **If "go" doesn't switch**: Add `commands/go.md` slash command that chains `/model sonnet` + plan execution instruction. Slash commands are the only reliable model switch trigger.
3. **Log anti-pattern PLAN_MODE_HOOK_PLATFORM_LIMIT**: hooks cannot switch running session model. settings.json only affects new sessions. Should be in anti-patterns.md to prevent future attempts.

## 9. Agent Observations
### Recommendations
- If settings hot-reload works, the "go" approach is the right final solution. Test it before building alternatives.
- The plan format injection (MANDATORY block, BANNED list) is working — confirmed firing in system-reminder during session.
- `.plan-guard-active` file pattern is clean and inspectable. Keep it.
- The guard's 30-minute auto-expire prevents stale blocks.

### Data Contradictions Detected
- Remote "last commit" appeared later than local after pull (concurrent Strain-Finder session). Not a bug.

### Where I Fell Short
- Should have surfaced the platform limitation (mid-session model switch impossible) on attempt 1, not attempt 4. Cost the user ~5 extra iterations.
- Should have researched PostToolUse:ExitPlanMode behavior before implementing. 2 commits wasted.
- 10 commits for 2 hooks is too many. Root causes should have been diagnosed faster.

## 10. Miscommunications
- User expected "approve plan and start coding" to be fully automatic. Platform limitation not surfaced until attempt 4. Should have been said upfront.

## 11. Files Changed
```
CLAUDE.md                                |   2 +-
hooks/plan-execution-guard.py            | 135 ++++++++++++++++++++++++
hooks/plan-exit-model-switch.ARCHIVED.py | 130 +++++++++++++++++++++++
hooks/plan-mode-enforcer.py              | 174 +++++++++++++++++++++++++++++++
4 files changed, 440 insertions(+), 1 deletion(-)
```

| File | Action | Why |
|------|--------|-----|
| hooks/plan-mode-enforcer.py | Created | UserPromptSubmit: plan format injection + "go" model switch |
| hooks/plan-execution-guard.py | Created | PreToolUse:Edit\|Write: blocks Opus from executing plans |
| hooks/plan-exit-model-switch.ARCHIVED.py | Archived | Dead code — PostToolUse:ExitPlanMode never fires |
| CLAUDE.md | Modified | Added both new hooks to hooks list |
| ~/.claude/settings.json | Modified (not in repo) | Registered new hooks in UserPromptSubmit and PreToolUse |

## 12. Current State
- **Branch**: main
- **Last commit**: 4b8d07a — Strain-Finder handoff pulled (2026-04-08 00:27:41 -0700) — superpowers work at b4543d3
- **Build**: N/A — skills/hooks repo
- **Deploy**: N/A — synced to GitHub
- **Uncommitted changes**: None (clean)
- **Local SHA matches remote**: YES after pull

## 13. Environment
- **Node.js**: v25.6.1
- **Python**: Python 3.9.6 (system)
- **Dev servers**: None

## 14. Session Metrics
- **Duration**: ~90 minutes
- **Tasks**: 2 features / plan format injection complete, "go" model switch unconfirmed
- **User corrections**: 6 (one per failed hook iteration)
- **Commits**: 10 (ceaba78 → b4543d3)
- **Skills used**: review-handoff, full-handoff

## 15. Memory Updates
- No new anti-pattern entries this session.
- **Recommended next session**: Add PLAN_MODE_HOOK_PLATFORM_LIMIT to anti-patterns.md — hooks cannot switch running session model.
- No new memory files written.

## 16. Skills Used
| Skill | Purpose | Helpful? |
|-------|---------|----------|
| review-handoff | Orient at session start | Yes |
| full-handoff | Generate this document | Yes |

## 17. For The Next Agent
Read these files first (in order):
1. This handoff
2. handoff_nicks-claude-code-superpowers_2026-04-07_1628.md (previous)
3. ~/.claude/anti-patterns.md
4. ~/ProjectsHQ/superpowers/CLAUDE.md
5. ~/.claude/hooks/plan-mode-enforcer.py
6. ~/.claude/hooks/plan-execution-guard.py
7. ~/.claude/settings.json (verify hooks registered)

**Canonical local path for this project: ~/ProjectsHQ/superpowers**
**Do NOT open this project from /tmp/ or iCloud. Use the path above.**

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
Before doing ANY work, run the 3-Gate Verification from ~/.claude/CLAUDE.md:
1. GATE 1: Check ~/Projects/site-to-repo-map.json — verify you're in the correct repo
2. GATE 2: git fetch && compare local SHA to remote — git pull if behind
3. GATE 3: Read this handoff + MEMORY.md + anti-patterns.md + recurring-bugs.md
ALL 3 GATES MUST PASS before touching any code.

**Canonical path for this project: ~/ProjectsHQ/superpowers**
**Last verified commit: 4b8d07a on 2026-04-08**
