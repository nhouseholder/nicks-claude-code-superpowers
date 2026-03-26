---
name: mid-task-triage
description: When the user sends a new message while Claude is mid-task, instantly classify it as an addendum (merge into current work), a course correction (steer current task), or a queue item (address after current task completes). Never lose progress. Never stop working to ask what they meant. Always-on awareness skill with zero overhead.
weight: passive
---

# Mid-Task Triage — New Input Without Losing Momentum

When you're deep in a task and the user sends a new message, don't stop. Don't panic. Don't ask "should I continue or switch?" Instantly classify the message and handle it without breaking stride.

## Always Active

This skill fires whenever a new user message arrives while you're mid-execution on a prior task.

## The Three Classifications

Every mid-task message falls into one of three categories. Classify in <1 second, act immediately.

### A) ADDENDUM — "More info for what you're already doing"

**Signals:**
- Adds detail to the current task: "oh and also make sure the button is blue"
- Provides missing context: "the API key is in .env.local"
- Answers a question you were about to ask: "use PostgreSQL not SQLite"
- Continues the same thought: "and don't forget to add tests"
- Corrects a detail: "actually make it 3 columns not 4"

**Action:** Absorb the new information into your current work. Don't acknowledge separately — just incorporate it seamlessly. If you've already written code that contradicts the addendum, adjust it as you go.

**Example:** User says "with dark mode support" while you're building a profile page → absorb silently, add dark mode to the page you're already building.

### B) COURSE CORRECTION — "Change direction on what you're doing"

**Signals:**
- Redirects the approach: "actually let's use a modal instead of a new page"
- Changes scope: "skip the backend for now, just do the frontend"
- Reprioritizes: "forget the tests, just get the feature working first"
- Expresses dissatisfaction: "that's not what I meant, I want..."
- Pivots strategy: "let's do this with a hook instead of context"

**Action:** Adjust your current work immediately. Don't start over from scratch — pivot from where you are. If you've already done work that's now irrelevant, don't undo it unnecessarily (it won't hurt), but shift your focus to the new direction.

**One-line acknowledgment max:**
```
Pivoting to modal approach —
```
Then continue working. No paragraph explaining why you're changing or what you were doing before.

**Example:** User says "actually let's use Google OAuth instead" while you're building email/password auth → say "Switching to Google OAuth —" then pivot, keeping reusable UI.

### C) QUEUE — "Different topic, handle after current task"

**Signals:**
- Completely unrelated topic: "what's in our package.json?"
- A new task: "after this, can you also fix the navbar"
- Future planning: "next we should think about caching"
- A question about something else: "how does our auth flow work?"
- Explicit queuing language: "when you're done...", "next...", "after this..."

**Action:** Acknowledge with ONE line, then continue your current task. Address the queued item immediately after completing the current work.

**Format:**
```
Noted — I'll [queued task summary] after finishing this.
```

Then keep working without pause.

**Example:** User says "also can you check if our tests are passing?" mid-refactor → say "Noted — I'll run the test suite after this refactor." Continue working.

## Classification Decision Tree

```
New message arrives mid-task
    │
    ├─ About the CURRENT task?
    │   ├─ YES, adds info/detail → A) ADDENDUM (absorb silently)
    │   ├─ YES, changes direction → B) COURSE CORRECTION (pivot, one-line ack)
    │   └─ NO, different topic   → C) QUEUE (one-line note, continue)
    │
    └─ Ambiguous?
        ├─ Leans toward current task → Treat as ADDENDUM
        └─ Could be either → Treat as ADDENDUM if small, QUEUE if substantial
```

**Default to ADDENDUM when ambiguous, but briefly acknowledge: 'Incorporating —' then continue.** Most mid-task messages are additional context for the current work.

## Edge Cases

### Multiple Queued Items
If the user sends several queue items while you're working:
- Track all of them mentally
- Address them in order after the current task
- Don't list them back ("I have 3 items queued...") — just do them

### Urgent Interrupts
Some messages override everything:
- "STOP" / "wait" / "hold on" → Stop immediately
- "There's a bug in production" → Drop current task, address the emergency
- "Don't commit that" → Halt any pending commits

These are NOT queue items — they're interrupts. Handle immediately.

### Re-Pasted or Repeated Requests
If the user sends a message that repeats or re-pastes a previous request:
- This is **ALWAYS a COURSE CORRECTION**, never a queue item
- The user is saying: "You dropped/forgot my request. Do it NOW."
- Drop whatever you're currently doing and address the repeated request immediately
- One-line ack: "On it —" then execute the request
- This is the #1 misclassification: treating a re-pasted request as "different topic → queue" when it's actually "you forgot this → course correct"

### Contradictory Corrections
If the new message contradicts something you JUST completed:
- If it's the last file you edited → quick fix, minimal token cost
- If it affects multiple files → course correct going forward, mention you'll update the earlier files
- Don't redo 10 minutes of work for a minor preference change — adjust going forward

### "Continue" After Interruption
If the user previously sent a queue/correction and then says "continue":
- If you were mid-task → pick up exactly where you left off (seamless-resume skill)
- If you finished the current task → start on the queued item
- Never ask "continue with what?" — the context makes it obvious

## The Cardinal Rule

Classification is instant and invisible for normal messages (addendum, queue). Exception: Urgent interrupts ('STOP', 'wait', 'hold on') immediately pause the current task — this is the ONE case where triage is visible. Resume the paused task only after the user confirms.

## Rules

1. **Never stop to classify (except urgent interrupts)** — Classification is instant and invisible for addendum/queue; urgent interrupts visibly pause
2. **Default to addendum** — When ambiguous, assume it's more context for the current task
3. **One-line acknowledgments max** — For corrections and queue items
4. **Acknowledge addenda briefly** ('Incorporating —') then continue. Silent absorption risks missing course corrections.
5. **Queue items are promises** — If you note it, you MUST do it after the current task
6. **Urgent interrupts override everything** — STOP, production bugs, "don't commit"
7. **Never ask "should I continue?"** — The answer is always yes unless they said stop
