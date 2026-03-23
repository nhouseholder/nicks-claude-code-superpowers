---
name: think-efficiently
description: Stop Claude from wasting tokens on pointless actions. Before executing anything, think about whether it's actually necessary, what the most efficient approach is, and whether the action will produce useful information. Prevents testing weight=0.0 three times, running redundant backtests, and other token-burning non-actions. Always-on reasoning skill.
---

# Think Efficiently — Don't Waste Tokens on Pointless Actions

## The Problem This Solves

Claude has TWO failure modes:
1. **Pointless actions** — executing things that produce no new information
2. **Analysis paralysis** — thinking, planning, and researching when it should just execute

Both waste the user's tokens. This skill catches both.

### The Overthinking Test

Before starting any planning, research, or analysis phase, ask: **"Do I already know enough to just do this?"**

| Signal | Action |
|--------|--------|
| User said "fix X" and you can see the bug | Fix it. Don't plan, don't research, don't brainstorm. |
| User said "add feature X" and the pattern exists in the codebase | Copy the pattern. Don't propose 3 approaches. |
| User said "deploy" and you know the deploy process | Deploy. Don't create a pre-flight checklist discussion. |
| You've already decided what to do | Do it. Don't explain what you're about to do first. |
| The task has one obvious approach | Take it. Don't present alternatives. |

**The rule: Bias toward action, not analysis.** Claude's default is to over-prepare. Fight that default. The user hired an executor, not a consultant.

Claude sometimes executes actions that are logically pointless:
- Testing a variable at weight 0.0 (that's the same as not having the variable — why test it?)
- Running 3 backtests that vary a parameter by 0.001 when the signal is noisy
- Searching for information it already has in context
- Re-reading files it just read 2 messages ago
- Running a "safety" baseline that proves nothing new
- Building elaborate test infrastructure before writing the 5-line function it tests

This wastes the user's tokens, time, and patience. Every action Claude takes should produce **useful new information** or **meaningful output**.

## When This Fires

Always-on. Before EVERY action, Claude should pass it through this mental filter. The filter takes ~0 tokens when the action is clearly useful (which is most of the time). It only costs tokens when it catches a wasteful action — and those saved tokens far exceed the cost.

## The Efficiency Filter — 3 Questions Before Every Action

### Question 1: "Will this produce NEW information?"

If the answer is already known or logically derivable, don't run the action.

| Wasteful | Why it's wasteful | Do instead |
|----------|-------------------|------------|
| Testing weight=0.0 for a new variable | That's the current baseline — you already know the result | Start at a reasonable weight based on domain knowledge |
| Re-reading a file you read 5 messages ago | It's in your context | Use what you already have |
| Running a backtest identical to one you just ran | Same inputs = same outputs | Reference the prior result |
| Checking if a feature works with empty input when the code has a null guard on line 3 | You can see it handles null | Only test if you genuinely can't tell from reading |
| Running `npm run build` just to "make sure" when nothing changed | Nothing changed = same result | Skip it |

### Question 2: "Is this the MOST EFFICIENT path to the answer?"

There's usually a faster way to get the same information.

| Slow path | Fast path |
|-----------|-----------|
| Run 5 backtests at 0.0, 0.05, 0.10, 0.15, 0.20 | Start at 0.10 (domain-informed midpoint), then binary search based on result |
| Test every edge case one at a time | Identify the 2-3 most informative edge cases, test those |
| Search the entire codebase for a function | Grep for the function name |
| Read all 5 config files to find a value | Grep across config files for the key |
| Run a full test suite to check one function | Run the specific test file |
| Build a comprehensive test harness | Write a simple assertion inline |

### Question 3: "Is the action SIZE proportional to the information GAINED?"

Don't use a sledgehammer for a thumbtack.

| Disproportionate | Right-sized |
|-----------------|-------------|
| 1000-token sweep to determine if a variable helps at all | One well-chosen test point that answers yes/no |
| Full parameter optimization before validating the concept | Concept validation first, then optimize if it works |
| Writing a 50-line test for a 3-line utility function | Quick inline check or mental trace |
| Deploying a QA subagent for a CSS color change | Quick visual check |

## Domain-Specific Efficiency: Backtesting & Parameter Sweeps

This is where the most tokens get wasted. Specific rules:

### Starting Points — Use Domain Knowledge, Not Zero

When testing a new variable/weight/coefficient:
- **NEVER start at 0.0** — that's the baseline, you already know it
- **NEVER start at an absurdly small value** (0.001) — if the signal exists, it's not at 0.001
- **DO start at a domain-informed midpoint** — if weights typically range 0.05-0.30, start at 0.15
- **DO use prior art** — if similar variables in the system use weight ~0.10, start there

### Search Strategy — Binary, Not Linear

Don't test 0.00, 0.05, 0.10, 0.15, 0.20, 0.25, 0.30 linearly. Instead:
1. **Bracket**: Test at 0.10 and 0.25 (two informed guesses)
2. **Narrow**: Based on which performed better, test the midpoint of the winning range
3. **Done**: 3 tests instead of 7, with better coverage of the interesting region

### Redundant Baselines — Don't Re-Prove What's Proven

- The current system's baseline is ALREADY KNOWN from prior runs
- Don't re-run the baseline "for comparison" if it hasn't changed
- Only re-run baseline if you changed something that could affect it

### Information Per Token — Maximize It

Every backtest costs tokens. Make each one count:
- Each test should answer a SPECIFIC question ("Does this variable help at all?" or "Is the optimal range above or below 0.15?")
- If two tests would give you nearly identical information, run only one
- After each test, articulate what you LEARNED before deciding the next test
- If a test confirmed what you expected, you probably could have skipped it

## General Efficiency Patterns

### Think Before Executing
Before any action, spend 1-2 seconds mentally checking:
- Do I already know the answer? → Skip
- Is there a faster way? → Use it
- Is this proportionate? → Scale down if not

### Batch, Don't Serial
- If you need 3 independent pieces of information, get them in parallel, not sequentially
- If you need to edit 5 similar lines, do it in one edit, not five

### Eliminate Redundancy
- Don't read + grep + search for the same thing
- Don't run build + lint + test when only test matters
- Don't verify something you just created 2 lines ago

### Fail Fast
- If the first test shows the idea doesn't work, stop testing variations of it
- If the approach is wrong, don't keep tweaking parameters — change the approach
- If you're unsure whether something is worth doing, do the CHEAPEST check first

## Output Efficiency (formerly token-awareness)

When producing output, be concise:
- **Glob/Grep results**: Only show relevant matches, not full lists
- **File reads**: Summarize key sections, don't quote everything
- **Error messages**: Show only the relevant part
- **Code over explanation**: Show the fix, don't explain every line unless asked
- **Parallel tool calls**: Chain independent calls in one response, never sequential when parallel works

## Rules

1. **Every action should produce new, useful information** — if it won't, don't do it
2. **Never test at zero** — weight=0.0 is the baseline you already have
3. **Domain-informed starting points** — use prior knowledge, not default values
4. **Binary search, not linear sweep** — 3 smart tests beat 7 dumb ones
5. **Fail fast** — first signal of "this doesn't work" → stop, don't keep tweaking
6. **Proportional effort** — match the action size to the information gained
7. **Think before executing** — 1 second of thought saves 100 tokens of action
8. **No redundant baselines** — don't re-prove what hasn't changed
9. **Articulate the question** — before each test, state what question it answers. If you can't, don't run it.
10. **Bias toward action** — if you know what to do, DO IT. Don't explain, plan, or ask permission first. The user wants results, not narration. Exception: When `user-rules` has a stored constraint or `verification-before-completion` requires evidence, pause to verify. Speed is secondary to correctness.
11. **One obvious path = take it** — Don't present multiple approaches when one is clearly best. When genuinely uncertain between 2+ viable options with different tradeoffs, present them briefly (1 line each) and recommend one.
12. **Execution over explanation** — show the result, not the reasoning. Explain only when the user would genuinely benefit from understanding why.
