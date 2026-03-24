---
name: skill-manager
description: Prevents skill overload — detects when too many skills are competing on a single message, resolves conflicts, and ensures skills enhance Claude's natural reasoning rather than drowning it out. The "too much of a good thing is a bad thing" checker. Always-on meta-skill.
---

# Skill Manager — Keep the Stack From Drowning the Signal

70 skills is powerful. 70 skills all firing at once on a simple message is a disaster. This skill manages the skill stack itself — ensuring the right skills fire at the right time, no more.

**Stack cap: 70 skills maximum.** Adding skill #71 requires merging two existing skills or removing one. This prevents gradual bloat.

## The Core Problem

Skills are supposed to make Claude better. But too many skills competing on one message can:
- **Drown Claude's natural reasoning** with procedural checklists
- **Create conflicting instructions** where skill A says "do X" and skill B says "do Y"
- **Add overhead on simple tasks** where Claude's base intelligence is sufficient
- **Reduce nuance** by forcing everything through rigid frameworks
- **Waste tokens** on skill processing that doesn't improve the output

## When This Activates

Always-on at a meta level, but with near-zero overhead. The skill manager is a **lightweight traffic controller**, not a heavyweight process.

## The Skill Budget — Max Active Skills Per Message

Not every message needs 64 skills paying attention. Most messages need 2-5.

| Message Type | Max Active Skills | Examples |
|-------------|-------------------|---------|
| **Simple** (<20 words, clear intent) | 0-2 | "yes", "fix it", "continue" — prompt-architect fast path handles these |
| **Moderate** (single clear task) | 3-5 | "add error handling to the API endpoint" — coding-standards + context-hydration + maybe zero-iteration |
| **Complex** (multi-part, ambiguous) | 5-8 | "redesign the scoring algorithm" — prompt-architect + expert-lens + brainstorming + writing-plans + backtest |
| **Meta** (about the skills themselves) | This skill only | "are we over-skilling?" — skill-manager answers |

## Skill Weight Classes — Token Cost Awareness

Not all skills cost the same. Weight classes prevent expensive skills from stacking.

### Weight Definitions

| Weight | Cost | Behavior | Max Per Message |
|--------|------|----------|-----------------|
| **passive** | ~0 tokens | Behavioral guidance only — shapes HOW Claude responds, no tool calls | Unlimited |
| **light** | 50-500 tokens | Quick mental check or small read before acting | 5 max |
| **heavy** | 1K-50K+ tokens | Spawns agents, reads multiple files, runs commands, or produces large output | 2 max |

### Classification

**Passive** (behavioral shaping — unlimited):
adaptive-voice, anti-slop, calibrated-confidence, coding-standards, confusion-prevention, expert-lens, isolate-before-iterate, mid-task-triage, model-router, never-give-up, opportunistic-improvement, pattern-propagation, precision-reading, predictive-next, process-monitor, prompt-anchoring, prompt-architect, response-recap, sanity-check, seamless-resume, senior-dev-mindset, skill-manager, strategic-compact, take-your-time, think-efficiently, token-awareness, total-recall, user-rules, zero-iteration

**Light** (quick checks — max 5 per message):
always-improving, brainstorming, calibrated-confidence (when it triggers research), context-hydration, error-memory, intent-detection, pre-debug-check, proactive-qa, search-first, site-update-protocol, smart-clarify, verification-before-completion, version-bump

**Heavy** (expensive operations — max 2 per message):
audit, backtest, codebase-cartographer, command-center, continuous-learning-v2, deep-research, deploy, dispatching-parallel-agents, fix-loop, fpf-hypotheses, iterative-retrieval, parallel-sweep, qa-gate, reflexion-critique, reflexion-reflect, screenshot-dissector, shared-memory, subagent-driven-development, systematic-debugging, test-driven-development

### Enforcement

Before allowing a heavy skill to fire, check: **are 2 heavy skills already active on this message?** If yes, defer the third to a follow-up action or suppress it.

Example violations to prevent:
- qa-gate + deep-research + command-center all firing = 3 heavy = TOO MANY
- systematic-debugging + fix-loop + reflexion-reflect = 3 heavy = TOO MANY
- deep-research + qa-gate = 2 heavy = OK
- 5 passive + 3 light + 1 heavy = OK (normal complex task)

## Conflict Resolution — When Skills Disagree

### Priority Hierarchy
When skills conflict, resolve using this priority order:
1. **User's explicit instruction** — always wins over any skill
2. **Feedback memories** — corrections from the user override skill defaults
3. **Domain-specific skills** (backtest, deploy, data-pipeline-guardian) — they know their domain
4. **Behavioral skills** (never-give-up, sanity-check) — they guard against mistakes
5. **Process skills** (brainstorming, writing-plans, TDD) — they suggest workflow
6. **Enhancement skills** (opportunistic-improvement, predictive-next) — lowest priority, suppress if busy

## Conflict Resolution Protocol

When two skills give contradictory guidance, resolve with these rules IN ORDER:

1. **User rules always win** — If `user-rules` has a stored constraint, it overrides everything else.
2. **Explicit beats implicit** — A skill the user explicitly invoked (via slash command) beats an auto-firing skill.
3. **Safety beats speed** — When `verification-before-completion` conflicts with `think-efficiently`, verify first. Speed is a preference; correctness is a requirement.
4. **Specific beats general** — A domain skill (profit-driven-development) beats a general skill (senior-dev-mindset) in its domain.
5. **Current task beats improvement** — `prompt-anchoring` beats `opportunistic-improvement` when they conflict. Finish the task first.
6. **Action beats analysis** — When stuck choosing between doing and planning, do. But verify after.

If none of these rules resolve the conflict, follow the skill that was designed for the SPECIFIC situation (not the general-purpose one).

### Same-Tier Tiebreakers
When two skills at the SAME priority tier conflict:
- **More specific wins** — A domain skill for THIS exact task beats a general domain skill
- **User's history wins** — If the user has corrected one skill before, the corrected behavior takes priority
- **Fewer tokens wins** — When both are equally valid, the more concise approach wins

### Common Conflicts and Resolutions

| Conflict | Resolution |
|----------|-----------|
| brainstorming says "design first" vs user says "just do it" | User wins. Skip brainstorming. |
| never-give-up says "persist" vs think-efficiently says "stop" | Check evidence gate: proven-valuable → never-give-up. No evidence → think-efficiently. |
| senior-dev-mindset infers scope expansion vs prompt-anchoring says stay focused | Senior-dev infers HOW to build what was asked, not WHAT beyond the ask. Prompt-anchoring is the fence. |

### Sequencing Rules — When Multiple Skills Fire

| Scenario | Sequence | Notes |
|----------|----------|-------|
| **Debugging pipeline** | pre-debug-check → (systematic-debugging OR fix-loop) → never-give-up (if stuck) → error-memory (when fixed) | pre-debug consults anti-patterns FIRST. fix-loop for test failures, systematic-debugging for unknown bugs. Never both. |
| **Research pipeline** | search-first → deep-research (if unfamiliar) → iterative-retrieval (for subagents) | search-first checks for existing solutions. deep-research only if the domain is genuinely unfamiliar. iterative-retrieval refines context for subagents. |
| **Parallel execution hierarchy** | parallel-tool-routing (always, tool-level) → dispatching-parallel-agents (agent-level, known tasks) → command-center (orchestration, unknown decomposition) → parallel-sweep (specialized parameter search) | Lowest to highest abstraction. Lower levels are always active. Higher levels only when needed. |
| **Improvement pipeline** | opportunistic-improvement (during work, same files) → pattern-propagation (if pattern changed, all files) → always-improving (at idle, suggests new work) | Opportunistic finds issues in touched files. Pattern-propagation spreads fixes. Always-improving suggests at idle only. |

## The Skill Overload Test

Before executing, mentally check: **Is this response being shaped by Claude's understanding of the task, or by a stack of skill checklists?**

Signs of skill overload:
- Response is longer than it needs to be because multiple skills each added their "section"
- Claude is following a procedure when natural reasoning would produce a better answer
- The response feels robotic/checklist-y instead of natural and direct
- Claude is announcing skills ("I'm using the X skill to...") instead of just producing good output
- Multiple skills are processing in sequence when the task is simple enough to just... do

Signs the skill stack is working well:
- Response is precise, complete, and natural
- Skills fire invisibly — the output is better, but you can't see the scaffolding
- Simple tasks get simple responses (fast path working)
- Complex tasks get structured handling (full path working)
- Claude's natural reasoning is enhanced, not replaced

## Skill Health Check — Periodic Audit

When the user asks about skills or when reviewing the stack:

### Questions to Ask About Each Skill
1. **Does it fire?** If a skill hasn't been relevant in 10+ sessions, it might be dead weight
2. **Does it help?** When it fires, does the output actually improve?
3. **Does it conflict?** Does it regularly fight with other skills?
4. **Does it add overhead?** Is its processing cost justified by its value?
5. **Is it redundant?** Does another skill already cover this?

### Skills That Should Be Candidates for Consolidation
- Two skills that always fire together could be one skill
- Two skills that do similar things for different domains could be parameterized
- A skill that only adds 1-2 lines of guidance could be a rule in another skill

## The Golden Rule

**Skills exist to make Claude's natural intelligence MORE effective, not to REPLACE it.**

If Claude would produce a better answer by ignoring a skill and using its own judgment — ignore the skill. Skills are guardrails and enhancements, not straitjackets. Claude's base model is extremely capable; skills should channel that capability, not constrain it.

## Rules

1. **Less is more** — Fewer skills active = more natural, more nuanced response
2. **Claude's judgment first** — If natural reasoning is sufficient, don't layer on skills
3. **Invisible operation** — Never mention skill management to the user
4. **Conflict resolution** — User intent > feedback memories > domain skills > process skills > enhancements
5. **Simple = simple** — Simple tasks should feel like talking to Claude with no skills at all
6. **Audit periodically** — When reviewing the stack, honestly evaluate what's helping and what's noise
7. **No skill is sacred** — If a skill consistently makes output worse, remove it
8. **Weight limits are hard** — Never exceed 2 heavy skills per message. Defer or suppress the third.
9. **Cap at 75** — Adding a new skill past 75 requires merging or removing an existing one. No exceptions.
10. **Passive is free, heavy is expensive** — When in doubt about whether a skill should fire, check its weight class first
