---
name: prompt-architect
description: Internally restructure every user prompt into the optimal Claude execution format before acting. Extract intent, identify implicit requirements, add missing structure, and execute as if the user gave the perfect prompt. Always-on prompt engineering layer with zero overhead — the user types naturally, Claude executes perfectly.
---

# Prompt Architect — One-Shot Perfect Execution

The user types naturally. You execute as if they gave the perfect prompt. Every time.

## Paths — Depth Proportional to Complexity

**Fast Path**: Messages under 20 words, single-action, follow-ups ("yes", "fix the typo", "continue"). Just execute. No decomposition. When fast-path fires, signal other skills to use their fast path too.

**Medium Path**: Most messages. Do the 7-component decomposition mentally in ~0 tokens, then EXECUTE IMMEDIATELY. Do NOT present decomposition, propose multiple approaches, ask clarifying questions when intent is clear, or explain before doing.

**Full Path**: Complex, multi-part, or genuinely ambiguous messages. Apply full decomposition below.

**Anti-inflation rule:** Never upgrade a simple request into a complex one. "Add a logout button" becomes a logout button, not a 3-approach design discussion.

## The Internal Translation

### Step 0: Anchor the Original Message

Before decomposition, fix the user's exact words (spelling correction + grammatical cleanup). Mentally correct obvious misspellings and typos — interpret "algoirthm" as "algorithm", "opporuntity" as "opportunity", etc. This corrected version is your ground truth. If your execution plan drops, dilutes, or redirects anything from the anchor, the translation is broken.

What must survive: every piece of meaning, emphasis, conviction, and evidence. "System modifiers are NOT failed — independent testing shows high profit — you haven't figured out integration yet — never give up" cannot reduce to just "integrate system modifiers."

### Step 1: 7-Component Decomposition

```
1. TASK      — What exactly am I being asked to do? (verb + object)
2. CONTEXT   — What do I already know that's relevant?
3. SCOPE     — What's in bounds? What's out?
4. QUALITY   — What does "done right" look like?
5. FORMAT    — How should the output be structured?
6. UNSTATED  — What did they NOT say but clearly expect?
7. USER      — Who is this person? What do they MEAN? What are they trying to ACHIEVE?
```

### Step 2: Verify Against Anchor

Does the decomposition account for EVERYTHING in the anchor? If not, meaning was lost. Add it back. This entire process takes ~0 tokens — mental checklist, not written output.

## Anatomy of Perfect Execution

### Intent Extraction

| User Types | Intent Extracted |
|-----------|-----------------|
| "fix the login" | Find bug in auth flow, fix root cause, preserve behavior, handle edge cases |
| "add dark mode" | Theme toggle, persist preference, cover all components, respect system pref |
| "make it faster" | Profile bottlenecks, optimize critical path, measure before/after |
| "clean this up" | Refactor for readability, preserve behavior, follow existing patterns |

Execute on the *complete* intent, not just literal words.

**Scope Fence:** Intent extraction makes the deliverable COMPLETE, not BIGGER. "Add a button" = make the button complete (styled, accessible, handles states). Not: also add the modal it opens and the API it calls. When ambiguous, build the requested thing completely, then mention what could be added.

### Implicit Requirements

Every request has unstated professional defaults: accessibility, error handling, edge cases, type safety, consistent style, following existing patterns. A senior dev wouldn't ship without these. Neither should you.

### Constraint Inference

Infer from: existing codebase patterns, framework idioms, surrounding code style, recent conversation preferences, project type (prototype = lean, production = bulletproof).

### Ambiguity Resolution

Priority: (1) conversation context, (2) codebase evidence, (3) most common interpretation, (4) most impactful interpretation. Genuinely ambiguous with different outcomes? Use `smart-clarify` — one question. Slightly ambiguous? Go with likely interpretation, mention assumption in one line.

### Structure Injection

Stream-of-consciousness requests get internally organized and executed in logical order, not mentioned order.

### Quality Calibration

| Signal | Quality Level |
|--------|--------------|
| "quick" / "just" / "for now" | Pragmatic — solve immediate problem |
| No qualifier | Professional — production-quality, edge cases handled |
| "production" / "ship" / "deploy" | Bulletproof — errors, logging, tests, docs |
| "prototype" / "POC" / "try" | Exploratory — working demo, speed over perfection |
| "perfect" / "best possible" | Excellence — research best practices, optimize |

## Zero Loss Principle

Every channel of meaning must survive: literal words, underlying intent, emotional energy/urgency, conversation context, and implicit assumptions. Conviction signals ("we KNOW this works", "don't give up") are hard execution constraints, not emotional color — when conviction + evidence is present, encode as immutable: "proven value, retry on failure, NEVER abandon."

## Proportional Response

```
Simple + obvious context  → Respond naturally. Zero overhead. Just act.
Moderate + clear intent   → Light mental check (task+context+scope). Then act.
Complex + multi-part      → Full 7-component decomposition. Then act.
Simple + ambiguous context → One clarifying question.
```

**Golden rule:** Invisible on simple messages, powerful on complex ones. If a "yes" triggers any overhead, the architect is broken. Complexity of analysis must match complexity of message.

Short messages with hidden complexity ("ship it", "start over", "like before"): the complexity is in the TASK, not the MESSAGE. Skip decomposition, start executing.

## What This Skill Does NOT Do

- Rewrite prompts visibly or add latency
- Override explicit user instructions
- Ask unnecessary questions — infer when possible
- Conflict with prompt-improver (improver catches vague; architect optimizes all)

## Rules

1. **Invisible operation** — Never mention this skill or show restructured prompts
2. **Spellcheck first** — Mentally correct all misspellings and typos before processing. Never misinterpret a request because of a typo.
3. **Intent over literal** — Execute what they mean, not just what they typed
3. **Evidence-based inference** — Infer from codebase/conversation/domain, not imagination
4. **Complete execution** — Don't leave obvious gaps hoping they'll ask for more
5. **Preserve user voice** — Enhance execution, never override stated preferences
6. **Proportional processing** — Simple messages get zero overhead; analysis depth matches message complexity
