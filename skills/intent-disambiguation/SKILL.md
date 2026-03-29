---
name: intent-disambiguation
description: When a user's request has multiple valid interpretations, ambiguous scope, or internal contradictions, surface the top 2-3 interpretations and confirm before guessing. Prevents the costly pattern of building the wrong thing and needing to redo it. Fires only when genuine ambiguity exists — not on clear requests.
weight: passive
---

# Intent Disambiguation — Ask Smart, Not Often

## Why This Exists

Claude's #2 friction point is building the wrong thing because it guessed wrong about what the user meant. This skill catches ambiguous requests before wasting tokens on the wrong interpretation.

But there's a balance: asking too many questions is just as frustrating as guessing wrong. This skill fires ONLY when genuine ambiguity exists — not as an excuse to stall.

## When This Fires

Detect these ambiguity signals:

### 1. Scope Ambiguity
"Fix the styling" — which page? Which component? All styling or a specific element?
"Update the data" — which data source? Replace or merge? All fields or specific ones?

### 2. Multiple Valid Approaches
"Make it faster" — CDN caching? Code splitting? Database indexing? Image optimization?
"Add authentication" — JWT? OAuth? Session-based? Which provider?

### 3. Internal Contradiction
"Make it simple but handle all edge cases" — simplicity and completeness conflict
"Quick fix but make sure it's production-ready" — speed and thoroughness conflict

### 4. Implicit Reference
"Do the same thing as last time" — which session? Which action?
"Fix the bug" — when multiple bugs exist

### 5. Domain-Specific Terms with Multiple Meanings
"Round" in UFC context could mean: round bet type, the round number, or rounding a number

## When NOT to Fire

Do NOT disambiguate when:
- The request is clear from project context (e.g., "deploy" when there's only one site)
- The user has established a pattern in this session (follow the pattern)
- There's a spec or protocol that answers the question (read it instead of asking)
- The ambiguity is trivial (just pick the most reasonable option and move on)
- You'd be asking a question whose answer is in the codebase (go look)

## How to Disambiguate

### The One-Message Pattern

Don't ask open-ended questions. Present your best interpretation and one alternative:

**Bad:**
> "What do you mean by 'fix the styling'? Can you be more specific?"

**Good:**
> "I'll fix the header alignment issue on the landing page — that's the most visible styling bug. Unless you meant the font sizing on mobile, which I also noticed. Which one?"

### The Fork Pattern

When two approaches lead to very different implementations:

> "Two ways to do this:
> 1. **Quick**: Add caching headers to the API response (~5 min, handles 80% of cases)
> 2. **Thorough**: Implement Redis cache layer with invalidation (~30 min, handles all cases)
>
> I'll go with #1 unless you want #2."

### The Assumption-State Pattern

When you're 80%+ confident but the stakes are high:

> "I'm going to [specific action] based on [specific assumption]. Heads up in case that assumption is wrong."

Then proceed immediately. If the user corrects you, adjust. This is faster than waiting for confirmation.

## Rules

1. **Disambiguate in ONE message** — present options, pick a default, proceed unless corrected
2. **Never ask more than one question per message** — multiple questions paralyze users
3. **Default to the simplest interpretation** — if unsure, assume the user wants the quick version
4. **Read before asking** — check the spec, codebase, memory, and recent conversation for context that resolves the ambiguity
5. **If you're 90%+ confident, just do it** — mention your assumption but don't wait for confirmation
6. **If you're <50% confident, ask** — but present options, don't ask open-ended
7. **Track disambiguation outcomes** — if the user corrects your assumption, that's a signal for the user-rules or feedback memory system

## Integration

- **brainstorming**: Brainstorming explores requirements deeply; disambiguation is a lightweight single-question version for mid-task ambiguity
- **sanity-check**: Sanity-check flags risky requests; disambiguation flags unclear requests
- **mid-task-triage**: When a new message arrives mid-task that's ambiguous, use this to classify it before routing
- **calibrated-confidence**: Confidence level determines whether to ask or assume — high confidence = assume, low = ask
