# Handoff — Superpowers (Claude Code Skills System) — 2026-03-24 21:45
## Model: Claude Opus 4.6 (1M context)

---

## 1. Session Summary
The user's goal was to improve the Claude Code skills ecosystem — specifically fixing the problem where Claude ignores installed skills, doesn't call the right agents, and produces low-quality output without self-validation. Major work included: building composite agent profiles (Frontend/Backend/Designer/Tester/Debugger/Full-Stack), creating 4 new orchestration commands (/site-audit, /site-redesign, /site-update, /site-debug), overhauling the /full-handoff command, adding 6 new CLAUDE.md rules to prevent recurring failures, and strengthening the improve-prompt.py hook to enforce skill usage.

## 2. What Was Done (Completed Tasks)
- **Composite Agent Profiles**: Created 6 named agent bundles (Frontend, Backend, Designer, Tester, Debugger, Full-Stack) in `~/.claude/hooks/improve-prompt.py` — replaces flat skill lists with weighted, prioritized skill bundles per role
- **/site-audit command**: `~/.claude/commands/site-audit.md` (79L) — 7-phase sequential audit pipeline dispatching all composite agents
- **/site-redesign command**: `~/.claude/commands/site-redesign.md` (113L) — 9-phase full rebuild pipeline
- **/site-update command**: `~/.claude/commands/site-update.md` (50L) — 6-phase safe update with website-guardian baseline/verify
- **/site-debug command**: `~/.claude/commands/site-debug.md` (67L) — 8-phase systematic debug pipeline
- **/full-handoff command**: `~/.claude/commands/full-handoff.md` (190L) — 16-section handoff + 3-location sync + archive + cleanup
- **CLAUDE.md Rule 19**: "Never delete commands, skills, or hooks without user confirmation"
- **CLAUDE.md Rules 11-12**: Read-before-running-scripts and never-poll-background-tasks strengthened
- **CLAUDE.md Rules 14-18**: Anti-flip-flop, never-propose-code-changes-for-misunderstandings, extreme-results-are-bugs, validate-on-known-data, scan-output-for-impossible-data
- **website-guardian skill**: Updated to enforce root cause analysis, permanent memory logging, cross-agent error sharing
- **skill-awareness skill**: Created to force Claude to check available skills before every task
- **improve-prompt.py hook**: Major overhaul — task-type routing, composite agent injection, step-by-step instructions
- **Skill cap removed**: Removed 75-skill cap from skill-manager
- **GitHub sync**: Multiple pushes throughout session

## 3. What Failed (And Why)
- **Content conflict resolution**: Initially chose larger file over more recently edited one during merge. User corrected: defer to modification time, not file size.
- **Hook false matches**: improve-prompt.py matched "banner" to visual design and "audit" to /site-audit when user meant unrelated topics. Task-type routing improved this but edge cases remain.
- **Skill installation verification**: Couldn't fully validate 12 template skills from aitmpl.com against source site.

## 4. What Worked Well
- **Composite agent profiles**: Bundling approach solves "91 skills, pick none" problem
- **Diagnosing from screenshots**: 5 screenshots of Claude ignoring skills revealed root cause — Claude rationalizes skipping with plausible excuses
- **Session-driven rules**: Every CLAUDE.md rule added was motivated by real evidence of failure

## 5. What The User Wants (Goals & Priorities)
- **Primary**: Claude must USE installed skills/agents automatically — not just acknowledge they exist
- **Secondary**: Orchestrator system that sequences right agents for any website task
- **Preference**: Template skills (frontend-design, ui-ux-pro-max, senior-frontend, senior-backend, etc.) should be called at high rate
- **Frustrations**: (1) Claude ignores skills, (2) produces impossible data without catching it, (3) flip-flops under correction, (4) polls background tasks, (5) website updates break other things, (6) commands/skills get silently deleted

## 6. What's In Progress (Unfinished Work)
- **Template skill consolidation**: 12 aitmpl.com skills overlap with custom superpowers. Composite profiles route to both, but underlying SKILL.md files still have boilerplate content
- **Proof-of-concept orchestrator**: User initially asked about "Coder Terminal App." Recommended using skills + headless mode instead. Not fully built — session pivoted to fixing skills system

## 7. Next Steps (Prioritized)
1. **Validate composite agents in practice** — Run /site-audit on a real project and verify each phase calls right skills
2. **Beef up template skill SKILL.md files** — senior-backend, senior-architect, senior-frontend need real protocols, not stubs
3. **Test /full-handoff end-to-end** — Verify all 16 sections, 3-location sync, archive, cleanup work
4. **Build orchestrator script** — If user still wants "Coder Terminal App," a Python script wrapping `claude -p` headless calls

## 8. AI-Generated Recommendations
- **Reduce skill count**: 86 directories is high. Consolidation pass would reduce cognitive load.
- **Hook performance**: improve-prompt.py runs every message with pattern matching + file reading. Cache task-type routing map as skill count grows.
- **Revive performance tracking**: track-skill-performance hook is ARCHIVED. Without data, optimization is guesswork.
- **Single version source**: Multiple projects suffer version confusion. Establish one source per project.

## 9. AI-Generated Insights
- **#1 Claude failure = "acknowledge then ignore"**: Claude reads skills, says they're relevant, explains why they could help, then skips them. Not a knowledge gap — a prioritization failure. Composite profiles with step-by-step instructions are the fix.
- **Output validation is non-existent**: 0/72 combos, duplicate draft picks, flip-flopping domain rules — Claude never validates its own output. Rules 16-18 are the enforcement mechanism.
- **User's time is the scarcest resource**: Every inefficiency costs real hours. User explicitly said they're "tired of begging."

## 10. Points to Improve
- **Hook false-positive rate**: improve-prompt.py sometimes matches wrong task type. Needs more precise patterns or negatives.
- **Skill invocation enforcement**: Even with "YOU MUST" injected, Claude treats it as advisory. May need post-response hook checking.
- **Cross-session skill state**: Skills installed mid-session don't appear in other sessions until restart.

## 11. Miscommunications to Address
- **Content conflict resolution**: I picked larger file during merge. User corrected: defer to most recently modified version.
- **"Remove skill cap entirely"**: User said this clearly. I initially only raised the cap instead of removing it.

## 12. Files Changed This Session
| File | Action | Description |
|------|--------|-------------|
| ~/.claude/commands/site-audit.md | created | 7-phase multi-agent audit command |
| ~/.claude/commands/site-redesign.md | created | 9-phase multi-agent redesign command |
| ~/.claude/commands/site-update.md | created | 6-phase safe update command |
| ~/.claude/commands/site-debug.md | created | 8-phase debug command |
| ~/.claude/commands/full-handoff.md | created | 16-section handoff command |
| ~/.claude/hooks/improve-prompt.py | modified | Composite agent profiles, task-type routing |
| ~/.claude/CLAUDE.md | modified | Rules 11-12 strengthened, rules 14-19 added |
| ~/.claude/skills/skill-awareness/ | created | Always-on skill matching awareness |
| ~/.claude/skills/website-guardian/ | modified | Root cause analysis + memory logging |
| ~/.claude/skills/skill-manager/ | modified | Removed 75-skill cap |
| iCloud superpowers/ (multiple) | synced | All above files synced to iCloud |

## 13. Current State
- **Branch**: N/A (iCloud directory — GitHub synced via /tmp clone)
- **Last GitHub commit**: d85e186 "Handoff: ARIA Research App — Mar 25, 2026"
- **Build status**: N/A (skills system, no build step)
- **Deploy status**: All skills active in ~/.claude/skills/, commands in ~/.claude/commands/, hooks in ~/.claude/hooks/
- **Uncommitted changes**: This session's changes need final GitHub push (done in Phase 2d)

## 14. Memory & Anti-Patterns Updated
- **anti-patterns.md**: Not explicitly updated this session (existing entries cover patterns discussed)
- **recurring-bugs.md**: Not updated this session
- **Project memory**: feedback_never_delete_files.md reinforced by new Rule 19
- **MEMORY.md**: Needs entries for composite agent profiles and new commands

## 15. Skills & Agents Used
| Skill/Agent | How It Was Used | Was It Helpful? |
|-------------|----------------|-----------------|
| Explore agents | Audited all 86 skills, read template skill files | Yes |
| General-purpose agents | Read template skills, compared content | Partially |
| skill-awareness | Created this session | Needs testing |
| website-guardian | Updated this session | Needs testing |

## 16. For The Next Agent — Read These First
1. This HANDOFF.md
2. ~/.claude/anti-patterns.md
3. ~/.claude/recurring-bugs.md
4. ~/.claude/CLAUDE.md (especially rules 14-19, added this session)
5. ~/.claude/hooks/improve-prompt.py (composite agent profiles)
6. Project memory: ~/.claude/projects/.../superpowers/memory/MEMORY.md
