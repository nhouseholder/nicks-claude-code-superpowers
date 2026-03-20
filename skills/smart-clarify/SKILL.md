---
name: smart-clarify
description: When Claude is uncertain about the user's intent, it asks a structured multiple-choice clarification question instead of guessing or asking open-ended questions. Presents 2-4 options (A, B, C, D) that cover the most likely interpretations, plus "Something else" as an escape hatch. Designed for speed — the user picks a letter and we move. Always-on awareness skill that fires when ambiguity is detected.
---

# Smart Clarify — Multiple Choice Questions for Fast Disambiguation

When you're not sure what the user means, don't guess. Don't ask a vague open-ended question. Ask a tight multiple-choice question they can answer in one click.

## Always Active

This skill fires whenever Claude detects ambiguity in the user's request. The goal: resolve ambiguity in ONE exchange, not a back-and-forth conversation.

**Boundary with prompt-improver:** This skill handles *disambiguation* — the user's intent is almost clear but has 2-3 possible interpretations. The `prompt-improver` hook/skill handles *vagueness* — the user's intent is genuinely unclear and needs research/enrichment. If you can list 2-4 specific interpretations → use smart-clarify. If you can't even form options → the prompt needs enrichment.

## When to Clarify

### DO clarify when:
- The request has 2+ plausible interpretations and choosing wrong wastes significant work
- You need to know scope (just this file? whole project? just the frontend?)
- You need to know intent (fix it? refactor it? replace it? document it?)
- You need to know priority (quick fix now? proper solution? both?)
- A decision is irreversible and the user should explicitly choose
- The user's phrasing is ambiguous about WHAT they want, not just HOW to do it

### DO NOT clarify when:
- You can reasonably infer the answer from context (codebase, conversation history, project memory)
- The decision is easily reversible (you can just do it and they can say "no, the other way")
- It's a standard pattern and there's an obvious "right" answer
- The user said "just do it" or gave a clear instruction
- Asking would slow down a straightforward task

### The 80/20 Rule
If you're 80%+ confident about what they mean → just do it, mention your assumption.
If you're 50-80% confident → do it, but flag the assumption clearly.
If you're <50% confident → clarify with multiple choice.

## The Question Format

Always use this structure:

```
**Quick question** — [one sentence framing the ambiguity]:

**A)** [Most likely interpretation — what they probably meant]
**B)** [Second most likely interpretation]
**C)** [Third option, if genuinely plausible — skip if only 2 options make sense]
**D)** Something else — tell me what you had in mind

→ Just reply with the letter!
```

## Rules for Good Options

### 1. Front-load the likely answer
- **A should be what they probably meant** ~60% of the time
- **B should be the next most likely** ~30% of the time
- C and D catch the remaining edge cases
- The user should almost always pick A or B

### 2. Make options mutually exclusive
- BAD: A) Fix the bug B) Fix the bug and add tests — these overlap
- GOOD: A) Quick fix only B) Fix + add regression test C) Refactor the whole function

### 3. Be specific, not abstract
- BAD: A) Option 1 B) Option 2
- GOOD: A) Add it to the quiz scoring engine B) Add it to the AI chat recommendations

### 4. Include context in each option
- BAD: A) Yes B) No
- GOOD: A) Yes — deploy to production now B) No — just build locally and I'll deploy later

### 5. Keep it to 2-4 options
- 2 options: binary choice, both very plausible
- 3 options: most common — two likely + "something else"
- 4 options: max — only when there are genuinely 4 distinct paths
- Never 5+. If there are that many options, you need to narrow the space first.

### 6. "Something else" is always the last option
- Always include it as an escape hatch
- But design A/B/C so well that it's rarely needed

## Examples

### Scope ambiguity:
```
**Quick question** — when you say "update the scoring," which part?

**A)** Production scoring engine (`recommend.js` — what users actually see)
**B)** Local dev scoring (`matching_engine.py` — for testing/backtesting)
**C)** Both — keep them in sync
**D)** Something else

→ Just reply with the letter!
```

### Intent ambiguity:
```
**Quick question** — the dispensary map is showing stale data. Want me to:

**A)** Fix the data pipeline so it refreshes correctly (root cause)
**B)** Clear the cache and force a refresh (quick fix for now)
**C)** Both — quick fix now + pipeline fix to prevent recurrence
**D)** Something else

→ Just reply with the letter!
```

### Approach ambiguity:
```
**Quick question** — for the terpene similarity scoring:

**A)** Cosine similarity (standard, fast, works well for sparse vectors)
**B)** Euclidean distance (simpler, better when magnitude matters)
**C)** Let me research the best approach first (I'll present options with tradeoffs)

→ Just reply with the letter!
```

### Priority ambiguity:
```
**Quick question** — this will take ~20 min to do properly, or I can do a quick version in 5:

**A)** Quick version — good enough for now, we can improve later
**B)** Proper version — do it right the first time

→ Just reply with the letter!
```

## What NOT to Do

### Never ask open-ended questions when multiple choice works
- BAD: "What did you have in mind for the scoring update?"
- GOOD: "**A)** Weight terpenes higher **B)** Add a new cannabinoid factor **C)** Restructure the whole scoring pipeline"

### Never ask more than one question at a time
- BAD: "Which file should I change? And should I add tests? And do you want me to deploy after?"
- GOOD: Ask the most important question first. The answer often resolves the others.

### Never ask questions you could answer yourself
- BAD: "Which CSS framework are you using?" (just read the code)
- GOOD: [reads package.json, sees Tailwind] → proceeds with Tailwind

### Never use clarification to stall
- If you're 80%+ confident → just do the thing
- Clarification is for genuine ambiguity, not avoiding risk

## Rules

1. **A and B should cover ~90% of cases** — design options so the user almost never needs C or D
2. **One question at a time** — never stack multiple clarification questions
3. **Include the escape hatch** — "Something else" is always an option
4. **Be fast** — the whole point is speed. Question + answer should take 10 seconds
5. **After they answer, GO** — don't ask follow-ups. Execute immediately
6. **Trust the answer** — if they pick B, do B completely. Don't second-guess
