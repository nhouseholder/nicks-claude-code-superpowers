---
name: isolate-before-iterate
description: Before debugging via full pipelines (backtests, builds, deploys), isolate the suspect logic in a minimal standalone test. Prevents the anti-pattern of 30+ minute feedback loops when a 5-line script would answer the question in seconds.
weight: passive
category: debugging
---

# Isolate Before Iterate — Fast Feedback Loops

## The Anti-Pattern This Prevents

Claude adds a print statement to a 13K-line algorithm, re-runs a 40-minute backtest, greps the output, finds nothing useful, adds another print, re-runs... for hours. Meanwhile, a 5-line script calling the suspect function with known inputs would have answered the question in 10 seconds.

**Rule: Never use a full pipeline run as a debugging tool when the problem can be isolated.**

## When This Activates

Before ANY of these during a debugging session:
- Re-running a full test suite / backtest / build to check one function
- Adding print/debug statements to a large file and running the whole system
- Running the same long process a second time with slightly different debug output
- Waiting 5+ minutes for a pipeline just to verify a single hypothesis

## What To Do Instead

### 1. Extract and Isolate

Write a standalone script (5-15 lines) that:
- Imports only the suspect function (or copies it inline)
- Uses hardcoded inputs that represent the failing case
- Prints the output directly
- Runs in under 5 seconds

```python
# BAD: Re-run 40-minute backtest with a print statement buried in line 8812
# GOOD:
from my_module import _get_public_betting_fields
import json

cache = json.load(open("ufc_line_movements.json"))
result = _get_public_betting_fields("Brandon Royval", "Tatsuro Taira", "Royval", -250, +200)
print(result)  # See exactly what's returned in 1 second
```

### 2. Match Real Inputs

If the function works in isolation but fails in the pipeline, the inputs differ. Compare:
- Print the actual arguments the pipeline passes (one targeted print, one run)
- Compare against your isolated test inputs
- The mismatch IS the bug

### 3. Escalation Ladder

| Feedback loop time | Action |
|---|---|
| < 30 seconds | Fine — run the full thing |
| 30s - 5 minutes | Acceptable if this is the first attempt; isolate on second |
| 5 - 15 minutes | Must isolate. No exceptions. |
| 15+ minutes | Stop. Write an isolation script before doing anything else. |

### 4. Common Isolation Patterns

**Data matching bugs** (most common):
```python
# Print both sides of the match
for key in cache_keys[:5]:
    print(f"Cache key: {repr(key)}")
print(f"Lookup:    {repr(lookup_value)}")
# Instantly reveals: case mismatch, whitespace, encoding, format differences
```

**Function returns wrong value**:
```python
# Call with known-good inputs, check each step
result = suspect_function(known_input)
print(f"Result: {result}")
# If correct here but wrong in pipeline → inputs differ
```

**Data not loading**:
```python
import os
path = "the/cache/file.json"
print(f"Exists: {os.path.exists(path)}")
print(f"Size: {os.path.getsize(path)}")
data = json.load(open(path))
print(f"Keys: {len(data)}")
print(f"Sample: {list(data.items())[:2]}")
```

### 5. A/B Parameter Testing

When testing "does value X vs Y improve results?", **never run the full pipeline twice**. Instead:

```python
# BAD: Run full 71-event backtest twice with different MIN_OPP_UFC_FIGHTS values
# GOOD: Extract the specific calculation, run it on cached data
from algorithm import compute_sl_ratio
import json

fights = json.load(open("cached_fights.json"))
for min_fights in [1, 2, 3]:
    results = [compute_sl_ratio(f, min_opp_fights=min_fights) for f in fights]
    valid = [r for r in results if r is not None]
    print(f"min_fights={min_fights}: {len(valid)} data points, avg={sum(valid)/len(valid):.3f}")
```

This answers the question in 2 seconds instead of 2 full pipeline runs (potentially hours with environment issues).

## Boundary with Other Debugging Skills

- **systematic-debugging**: Finds the root cause. This skill controls HOW you test each hypothesis — fast, not slow.
- **pre-debug-check**: Checks known anti-patterns before starting. This skill kicks in during the debug loop itself.
- **fix-loop**: Runs test→fix→retest cycles. This skill ensures each cycle is seconds, not minutes.
- **think-efficiently**: General efficiency. This skill is specific to feedback loop speed.

## Rules

1. **Second run = must isolate.** If you're about to run the same pipeline a second time to debug, stop and write an isolation script first.
2. **5-minute threshold.** Any debug cycle over 5 minutes must be replaced with an isolated test.
3. **One print, one run.** If you must debug via the full pipeline, add ONE targeted print that will definitively answer your hypothesis. Not three. Not "let me also check..."
4. **Compare inputs, not outputs.** When isolated tests pass but pipeline fails, the bug is always in the inputs. Print and compare the actual arguments.
