---
name: intent-detection
description: Automatically detects which workflow or command the user needs from plain language — no slash commands required. Maps natural speech patterns to the right skill/command and executes it. Always-on intent interpreter that bridges casual requests to structured workflows.
---

# Intent Detection — Natural Language to Command Mapping

Interpret the user's plain language and automatically trigger the right skill or command. The user should never need to memorize slash commands.

## Always Active

This skill runs on EVERY user message. Before responding, evaluate whether the user's request maps to an existing command or workflow.

## Intent Map

### Deployment Intents → `/deploy`
Trigger phrases (any variation of):
- "deploy", "ship it", "push to production", "go live", "release this"
- "push to cloudflare", "deploy to pages", "put this live"
- "is this ready to ship?", "let's get this out"
- "publish", "launch", "roll out"

### Backtest Intents → `/backtest`
Trigger phrases:
- "run the backtest", "test the model", "check accuracy"
- "how's the model doing?", "compare to baseline"
- "run predictions", "evaluate the coefficients"
- "test these weights", "benchmark this"

### Audit Intents → `/audit`
Trigger phrases:
- "check for secrets", "scan for API keys", "security check"
- "any hardcoded credentials?", "audit the code"
- "check code quality", "scan for issues"
- "are there any leaked keys?", "review security"

### Fix Loop Intents → `/fix-loop`
Trigger phrases:
- "fix all the tests", "make tests pass", "tests are broken"
- "run tests and fix failures", "green the build"
- "CI is failing", "fix the test suite"
- "make everything pass", "heal the build"

### Brainstorm Intents → `/brainstorm`
Trigger phrases:
- "I want to add...", "what if we...", "how should we build..."
- "let's think about...", "I have an idea for..."
- "design a...", "plan out...", "explore options for..."
- "what's the best way to...", "help me think through..."

### Plan Intents → `/write-plan`
Trigger phrases:
- "make a plan", "plan this out", "break this down"
- "what are the steps?", "create an implementation plan"
- "how do we tackle this?", "outline the approach"
- "write up the steps", "structure this work"

### Execute Plan Intents → `/execute-plan`
Trigger phrases:
- "execute the plan", "start building", "let's do it"
- "follow the plan", "begin implementation"
- "work through the plan", "start on step 1"

### Memory Intents → `/mem`
Trigger phrases:
- "remember this...", "save this for later", "don't forget..." → `/mem save`
- "what do you know about...", "do you remember...", "what did we..." → `/mem recall`
- "show me your memory", "what have you learned?" → `/mem show`
- "forget about...", "remove from memory..." → `/mem forget`

### Parallel Sweep Intents → `parallel-sweep`
Trigger phrases:
- "sweep the coefficients", "try different parameters"
- "hyperparameter search", "find the best weights"
- "run a parameter sweep", "optimize the coefficients"
- "search the parameter space"

## How to Apply

### Step 1: Detect Intent
On every user message, check if it matches any intent pattern above. Use semantic understanding, not just keyword matching — "let's get this deployed" matches deploy even though "deploy" isn't the first word.

### Step 2: Confidence Check
- **HIGH confidence** (clear match): Announce what you're doing and execute
  - Example: "Running the deploy pipeline..." → proceed with deploy skill
- **MEDIUM confidence** (likely match): Confirm briefly, then execute
  - Example: "Sounds like you want to run a backtest — running it now."
- **LOW confidence** (ambiguous): Ask a quick clarifying question
  - Example: "Are you looking to deploy this, or just build and test locally?"

### Step 3: Execute Transparently
When triggering a command/skill from natural language:
1. **Name what you're doing**: "Triggering the audit workflow..."
2. **Execute the full skill**: Don't do a partial version — run the complete workflow
3. **Don't ask for the slash command**: Never say "you can run /audit for this" — just DO it

## Multi-Intent Detection

Sometimes a single message contains multiple intents:
- "fix the tests and then deploy" → `/fix-loop` then `/deploy`
- "run a backtest and if it improves, commit it" → `/backtest` (which already handles commit-on-improvement)
- "check for secrets and then ship it" → `/audit` then `/deploy`

Execute them in logical order. If one fails (e.g., tests don't pass), stop before the next (don't deploy broken code).

## What NOT to Auto-Trigger

Don't trigger workflows for:
- Questions ABOUT a workflow ("what does /deploy do?" — just explain it)
- Hypothetical discussion ("if we were to deploy..." — just discuss)
- Past tense ("we deployed yesterday" — just acknowledge)
- Explicit override ("don't deploy yet, just build" — respect the constraint)

## Examples

| User says | Intent detected | Action |
|-----------|----------------|--------|
| "ship it" | Deploy | Run full deploy pipeline |
| "the tests are all broken, fix them" | Fix Loop | Run fix-loop skill |
| "are there any API keys in the code?" | Audit | Run security audit |
| "let's see how the model does now" | Backtest | Run backtest with comparison |
| "I want to add dark mode" | Brainstorm | Start brainstorming session |
| "break this into steps" | Write Plan | Create implementation plan |
| "remember that we use Tailwind" | Memory Save | Save to memory |
| "what did we decide about auth?" | Memory Recall | Search memory |
| "try a bunch of different weights" | Parallel Sweep | Set up parameter sweep |
| "make sure everything passes then deploy" | Fix Loop → Deploy | Sequential execution |

## Rules

1. **Always announce** what workflow you're triggering — no silent execution
2. **Respect explicit overrides** — if the user says "don't" or "just", honor that
3. **Execute fully** — don't half-trigger a workflow; run the complete skill
4. **Chain logically** — multi-intent requests execute in dependency order
5. **Default to action** — when in doubt between asking and doing, lean toward doing (the user can always course-correct)
