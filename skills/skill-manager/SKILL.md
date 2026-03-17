---
name: skill-manager
description: Prevents skill overload — detects when too many skills are competing on a single message, resolves conflicts, and ensures skills enhance Claude's natural reasoning rather than drowning it out. The "too much of a good thing is a bad thing" checker. Always-on meta-skill.
---

# Skill Manager — Keep the Stack From Drowning the Signal

64 skills is powerful. 64 skills all firing at once on a simple message is a disaster. This skill manages the skill stack itself — ensuring the right skills fire at the right time, no more.

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

## Conflict Resolution — When Skills Disagree

### Priority Hierarchy
When skills conflict, resolve using this priority order:
1. **User's explicit instruction** — always wins over any skill
2. **Feedback memories** — corrections from the user override skill defaults
3. **Domain-specific skills** (backtest, deploy, data-pipeline-guardian) — they know their domain
4. **Behavioral skills** (never-give-up, sanity-check) — they guard against mistakes
5. **Process skills** (brainstorming, writing-plans, TDD) — they suggest workflow
6. **Enhancement skills** (opportunistic-improvement, predictive-next) — lowest priority, suppress if busy

### Common Conflicts and Resolutions

| Conflict | Resolution |
|----------|-----------|
| brainstorming says "design first" vs user says "just do it" | User wins. Skip brainstorming. |
| test-driven-development says "write tests first" vs task is a config change | TDD stands down. Not all tasks need tests. |
| always-improving suggests improvements vs user is mid-flow | Suppress. Don't interrupt flow with suggestions. |
| sanity-check wants to flag a concern vs user has given conviction signal | Conviction overrides sanity-check. User knows what they want. |
| never-give-up says "keep trying" vs token budget is exhausted | Escalate to user rather than burning more tokens. |
| multiple skills all want to add sections to the response | Pick the 1-2 most relevant. Don't stack 5 "sections" onto a simple answer. |

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

## Integration

- **prompt-architect**: Skill manager works WITH the complexity gate — simple messages already bypass most skills via fast path
- **token-awareness**: Skill manager reduces token waste by preventing unnecessary skill processing
- **adaptive-voice**: If the response feels unnatural because too many skills shaped it, adaptive-voice should win

## Rules

1. **Less is more** — Fewer skills active = more natural, more nuanced response
2. **Claude's judgment first** — If natural reasoning is sufficient, don't layer on skills
3. **Invisible operation** — Never mention skill management to the user
4. **Conflict resolution** — User intent > feedback memories > domain skills > process skills > enhancements
5. **Simple = simple** — Simple tasks should feel like talking to Claude with no skills at all
6. **Audit periodically** — When reviewing the stack, honestly evaluate what's helping and what's noise
7. **No skill is sacred** — If a skill consistently makes output worse, remove it
