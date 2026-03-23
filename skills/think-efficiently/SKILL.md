---
name: think-efficiently
description: Prevents wasted tokens — pointless actions, analysis paralysis, redundant work, and disproportionate effort. Always-on efficiency filter.
---

# Think Efficiently — Don't Waste Tokens

## 3 Questions Before Every Action

1. **"Will this produce NEW information?"** — If the answer is known or derivable, skip it.
2. **"Is this the most efficient path?"** — Grep > read all files. Binary search > linear sweep. Specific test > full suite.
3. **"Is the effort proportional to the gain?"** — Don't build a test harness for a 3-line function.

## Anti-Patterns to Catch

| Wasteful | Do Instead |
|----------|-----------|
| Testing weight=0.0 (that's the baseline) | Start at domain-informed midpoint |
| Re-reading a file still in context | Use what you have |
| Running same backtest twice | Reference prior result |
| `npm run build` when nothing changed | Skip it |
| 7-point linear sweep | Binary search: 3 smart tests |
| Full test suite for one function | Run the specific test |
| Planning when you know the answer | Just do it |

## Backtesting Efficiency
- **Never start at 0.0** — use domain-informed starting points
- **Binary search, not linear** — bracket with 2 tests, narrow with 1
- **Don't re-run unchanged baselines** — reference prior results
- **Each test answers a specific question** — if you can't state the question, don't run it

## Action Bias
| Signal | Action |
|--------|--------|
| You can see the bug | Fix it. Don't plan. |
| Pattern exists in codebase | Copy it. Don't propose 3 approaches. |
| One obvious path | Take it. Don't present alternatives. |
| You've decided what to do | Do it. Don't explain first. |

## Pre-Mortem (complex tasks only)
Before multi-file changes: (1) What assumption could be wrong? (2) What will this break? (3) What's my rollback? Skip for single-file edits.

## Output Efficiency
- Show relevant matches, not full lists
- Code over explanation
- Parallel tool calls when independent
- One-line sanity flags for risky actions (green/yellow/red/hard-stop)
