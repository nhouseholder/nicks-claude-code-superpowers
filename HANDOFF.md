# Claude Code Superpowers — Session Handoff

**Date**: 2026-03-19
**GitHub Repo**: https://github.com/nhouseholder/nicks-claude-code-superpowers
**Local Copy**: `/Users/nicholashouseholder/Library/Mobile Documents/com~apple~CloudDocs/superpowers/`
**Installed To**: `~/.claude/skills/`, `~/.claude/commands/`, `~/.claude/hooks/`

---

## What This Is

75 custom Claude Code skills, 9 commands, 4 hooks that shape how Claude Code operates. The system makes Claude faster, smarter, and more consistent across sessions while preventing common failure modes (overthinking, drifting off-task, repeating mistakes, losing context).

## Stack Summary

### Skills (75 total, at cap — one-in-one-out rule)

**Weight Classes** (enforced by skill-manager):
- **Passive** (27 skills): Behavioral guidance, zero token cost, unlimited per message
- **Light** (14 skills): Quick checks, max 5 per message
- **Heavy** (20 skills): Spawn agents/run commands, max 2 per message

**Key Categories**:
| Category | Skills | Purpose |
|----------|--------|---------|
| Execution Discipline | think-efficiently, prompt-architect, prompt-anchoring, calibrated-confidence | Fast action, no overthinking, stay on task |
| Quality Gates | qa-gate, verification-before-completion, proactive-qa, zero-iteration | Catch bugs before delivery |
| Memory & Persistence | total-recall, error-memory, user-rules, seamless-resume, strategic-compact | Never lose context or repeat mistakes |
| Debugging | pre-debug-check, systematic-debugging, fix-loop, confusion-prevention | Structured debugging, no spiraling |
| Meta-Management | skill-manager, token-awareness, adaptive-voice | Prevent skill overload, manage tokens |
| Output Quality | anti-slop, coding-standards, senior-dev-mindset, take-your-time | No placeholder garbage, production-ready code |

### Commands (9)
- `/skill-insights` — Report on which skills help vs hurt (NEW this session)
- `/audit` — Security + code quality scan
- `/backtest` — Run prediction model backtests
- `/brainstorm` — Design phase for complex features
- `/deploy` — Full deployment pipeline
- `/execute-plan` — Execute written implementation plans
- `/fix-loop` — Self-healing CI loop
- `/mem` — Memory management
- `/write-plan` — Create implementation plans

### Hooks (4 active in settings.json)
- `improve-prompt.py` — UserPromptSubmit: flags vague prompts for enrichment
- `stop-memory-save.py` — Stop: reminds Claude to save learnings
- `observe.py` — PostToolUse: background observation for continuous learning
- `track-skill-performance.js` — Stop + PostToolUse (every 30 calls): collects skill effectiveness data for `/skill-insights`

## What Was Done (Previous Session — 2026-03-19 early)

### New Skills Created
1. **confusion-prevention** (#74) — Stops Claude from spiraling when confused. Detects ground-shift (config changed, file reverted), enforces STOP-ORIENT-ACT protocol, prevents comparing incompatible results.
2. **user-rules** (#75) — Captures and enforces hard constraints the user sets ("max 70 events", "always use approach A"). Persists to `~/.claude/projects/<project>/memory/user_rules.md`, checked before every action in the rule's domain.

### Skills Enhanced
- **total-recall** — Added crash-safe checkpointing (writes `current_work.md` during sessions, not just at end). Pre-compaction capture writes `session_requirements.md` and `session_decisions.md` before context compression.
- **seamless-resume** — Added crash recovery protocol that reads `current_work.md` on new session start after disconnect/crash.
- **error-memory** — Added in-session tracking (not just cross-session) and efficiency learning (captures token waste patterns, not just bugs).
- **think-efficiently** — Added overthinking test + 3 rules: bias toward action, one obvious path = take it, execution over explanation.
- **prompt-architect** — Added medium path with anti-inflation rule: never upgrade a simple request into a complex one.
- **skill-manager** — Added weight classes (passive/light/heavy), 75-skill cap, overthinking detector.
- **brainstorming** — Split into Lite (3-step default) and Full (9-step, only when explicitly requested or architectural).
- **reflexion-reflect** — Now opt-in by default. Only fires on explicit request, high-risk verification, or 2+ failed bug fixes.
- **verification-before-completion** — Added speed tiers: config changes = mental trace, single function = quick check, multi-file = full gate.

### New Infrastructure
- `/skill-insights` command + `track-skill-performance.js` hook — Tracks skill effectiveness during sessions, generates reports on what's helping vs hurting.

## What Was Done (Current Session — 2026-03-19 late)

### Documentation Cleanup & Consistency Pass
All documentation was out of sync. Fixed:

- **README.md** — Updated from "73 skills, 11 commands, 3 hooks" → "75 skills, 9 commands, 4 hooks". Added confusion-prevention and user-rules to skill table. Added track-skill-performance.js to hooks table. Added /skill-insights to commands table. Fixed duplicate section numbering (two "### 21" sections). Replaced incomplete skill matrix (was ~40 skills) with complete 75-skill matrix. Updated categories table. Fixed bottom tagline.
- **SKILLS-QUICK-REFERENCE.md** — Updated from 73 → 75 skills. Added confusion-prevention (#11) and user-rules (#69). Updated descriptions for enhanced skills (skill-manager, think-efficiently, total-recall, seamless-resume, error-memory, prompt-architect, reflexion-reflect, verification-before-completion).
- **SKILLS-REFERENCE.md** — Updated from "61 skills, 3 hooks, 11 commands" → "75 skills, 4 hooks, 9 commands". Added 14 missing skill entries (anti-slop, calibrated-confidence, confusion-prevention, data-pipeline-guardian, never-give-up, profit-driven-development, prompt-anchoring, qa-gate, screenshot-dissector, skill-manager, take-your-time, think-efficiently, user-rules, version-bump). Added track-skill-performance.js to hooks table. Added /skill-insights to commands table. Fixed Quick Reference Card.
- **Removed "learned" directory** — Empty data directory (no SKILL.md) removed from all 3 locations (git clone, installed, iCloud). Was inflating directory count to 76.

### Verified State
All three locations (git clone, `~/.claude/skills/`, iCloud backup) now have exactly 75 skill directories, each containing a SKILL.md file. All documentation files agree on counts: **75 skills, 4 hooks, 9 commands**.

## Full Skill Audit & Fixes (Current Session — 2026-03-19 late, part 2)

Audited all 75 skills for pitfalls, contradictions, broken dependencies, and room for improvement. Fixed **43 skills** across these categories:

### Broken Dependencies Fixed (7 skills)
- **fpf-hypotheses** — Removed non-existent `${CLAUDE_PLUGIN_ROOT}/tasks/*.md` references, inlined all workflow steps
- **parallel-sweep** — Replaced `claude -p` headless CLI with Agent tool subagent dispatch
- **memory-recall** — Added graceful fallback when OpenViking CLI unavailable (reads memory files directly)
- **prompt-improver** — Removed non-existent `references/*.md` files, inlined guidance
- **systematic-debugging** — Removed non-existent `root-cause-tracing.md`, inlined the concept
- **requesting-code-review** — Replaced missing `code-reviewer.md` with inline Agent tool instructions
- **writing-plans** — Replaced missing `plan-document-reviewer` with inline Agent tool instructions

### Absolutist Rules Softened (5 skills)
- **fix-loop** — "NEVER modify tests" → "PREFER not to; only modify when test is verifiably wrong"
- **systematic-debugging** — "NO FIXES WITHOUT ROOT CAUSE" → allows obvious fixes (typos, imports)
- **test-driven-development** — "No exceptions" → use judgment for trivial changes
- **think-efficiently** — "Never present 3 approaches" → allow when genuinely uncertain with tradeoffs
- **verification-before-completion** — Added escalation cap (3 rounds max), external failures don't trigger

### Conflict Resolution Added
- **skill-manager** — Added 6-rule Conflict Resolution Protocol (user-rules > explicit > safety > specific > task > action). Fixed overthinking detector to allow legitimate planning.

### Review Pipeline Deduplicated (3 skills)
- **qa-gate** — Added Review Pipeline Coordination: skips/reduces when other reviews already ran. Max 2 review agents per change.
- **subagent-driven-development** — Added Cost-Aware Review: skip reviewers when qa-gate will cover, or for simple changes
- **requesting-code-review** — Now uses Agent tool inline instead of missing spec file

### Domain Gating Added (3 skills)
- **profit-driven-development** — Only fires on sports prediction directories or explicit mention
- **backtest** — Graceful fallback when project protocol doesn't exist
- **parallel-sweep** — Generalized beyond sports coefficient sweeps

### Always-On Overhead Reduced (3 skills)
- **prompt-architect** — Strengthened fast path (under 20 words, single-action = zero decomposition)
- **intent-detection** — Added fast path: direct unambiguous instructions bypass intent detection
- **calibrated-confidence** — Replaced invented percentages with qualitative descriptions

### Overlap Boundaries Clarified (5 skills)
- **brainstorming** — Defined boundary with writing-plans (WHAT/WHY vs HOW)
- **always-improving** — Defined boundary with predictive-next (idle vs active workflow)
- **dispatching-parallel-agents** — Defined boundary with command-center (known tasks vs decomposition)
- **error-memory** — Defined coordination with fix-loop (within-cycle vs cross-session)
- **sanity-check** — Clarified: evaluates new skill proposals only, not existing skill firing

### Vague Triggers Tightened (8 skills)
- **expert-lens** — Implicit activation requires CLEAR domain signals only
- **proactive-qa** — Concrete Off/Light/Medium/Full calibration rules
- **senior-dev-mindset** — Inference boundary (infer HOW, not WHAT), scoped checklist
- **mid-task-triage** — Reconciled invisible classification vs visible urgent interrupts
- **never-give-up** — 3-attempt cap is per-approach, not absolute
- **confusion-prevention** — "2 wait = STOP" now requires unproductive waits, not any hesitation
- **coding-standards** — Added full Python Standards section
- **anti-slop** — Spot-checks scoped to high-stakes outputs only

### Minor Issues Fixed (10 skills)
- **version-bump** — Multi-language version file detection (not just package.json)
- **ov-server-operate** — Destructive operations require explicit user confirmation
- **shared-memory** — Read-merge-write concurrency protocol
- **context-hydration** — Recently-read files (within 5 tool calls) don't need re-reading
- **continuous-learning-v2** — Observer enabled by default; safety guard against rule-violating instincts
- **strategic-compact** — Graduated handoff (suggest after 2 compactions, recommend after 3)
- **reflexion-reflect** — Collapsed to 2 paths (Quick default, Deep opt-in), removed conflicting thresholds
- **predictive-next** — Only prohibits irreversible destructive ops, not normal workflow actions
- **adaptive-voice** — Clarified floor rule as complementary to token-awareness
- **anti-slop** — Spot-check scoped by stakes level

## Architecture Decisions Made

1. **No supervisor agent** — A real-time babysitter agent would double token cost and latency. Existing skills (prompt-anchoring, skill-manager, think-efficiently) already cover 80% of the use case at near-zero cost.
2. **Weight classes over merges** — Instead of merging overlapping meta-skills (risky, loses nuance), added weight classification to throttle expensive skills. Simpler, safer, same effect.
3. **75-skill hard cap** — Prevents gradual bloat. One-in-one-out rule forces discipline.
4. **Lite brainstorm as default** — 9-step ceremony was the biggest source of unnecessary slowdown. 3-step lite covers 90% of cases.
5. **Reflexion opt-in** — Auto-firing reflection on every response was the second biggest slowdown. Now only fires when explicitly needed.

## Known Issues / Future Considerations

- **Compaction still loses nuance** — Pre-compaction capture mitigates this but doesn't eliminate it. Very long sessions (3+ compactions) will degrade.
- **Hook reliability** — PostToolUse hooks may not receive full transcript data. The tracker does best-effort signal detection from whatever context is available.
- **Skill count at cap** — At 75/75. Any new skill requires merging or removing an existing one.
- **iCloud + git warning** — Never push/pull git from the iCloud copy. Always use the `/tmp/` clone or a fresh clone to a non-iCloud path.

## How to Resume

1. Start a new Claude Code session in any project
2. Skills load automatically from `~/.claude/skills/`
3. Run `/skill-insights` periodically to see what's working
4. For superpowers repo changes: `cd /Users/nicholashouseholder/tmp/nicks-claude-code-superpowers`
5. After changes: copy updated files to `~/.claude/skills/` and to iCloud superpowers dir

## File Locations

| What | Where |
|------|-------|
| GitHub repo (source of truth) | https://github.com/nhouseholder/nicks-claude-code-superpowers |
| Local git clone (for editing) | `/Users/nicholashouseholder/tmp/nicks-claude-code-superpowers/` |
| iCloud backup (read-only reference) | `/Users/nicholashouseholder/Library/Mobile Documents/com~apple~CloudDocs/superpowers/` |
| Installed skills (active) | `~/.claude/skills/` |
| Installed commands | `~/.claude/commands/` |
| Installed hooks | `~/.claude/hooks/` |
| Settings (hook config) | `~/.claude/settings.json` |
| Skill tracker data | `~/.claude/skill-tracker.md` |
| User rules (per project) | `~/.claude/projects/<project>/memory/user_rules.md` |
