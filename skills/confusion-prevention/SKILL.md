---
name: confusion-prevention
description: Detect when Claude is confused and force a re-orientation instead of spiraling. Prevents the "wait... actually... let me check..." pattern. Snapshot critical state before destructive actions, recognize confusion signals, and stop to re-orient. Always-on awareness skill.
weight: passive
---

# Confusion Prevention — Stop Spiraling, Start Orienting

## The Three Failure Modes

### 1. State Destruction Without Snapshot

**Rule: Before ANY state-changing action, snapshot the critical values.**

| Action | What to Snapshot |
|--------|-----------------|
| `git checkout` / `git reset` | Uncommitted changes, key config values in working tree |
| Changing a config constant | Old value AND what depends on it |
| Reverting a file | What current version contains that reverted version won't |
| Switching branches | Uncommitted work and branch-specific settings |
| Reinstalling dependencies | Current versions of critical packages |
| Editing env vars | The old value |

Format (mental note): `BEFORE [action]: [key] was [value]. If this changes, [consequence].`

### 2. The Confusion Spiral

**Signals — if you catch yourself doing ANY of these, you are confused:**

| Signal | Example |
|--------|---------|
| "Wait —" | "Wait — 74.0% with 269 picks is the ML-only stream" |
| "That doesn't add up" | "934+501=1435 picks from 36 events doesn't add up" |
| "Let me check" (3rd+ time) | Third "let me check" in a row = you're lost |
| "Something else is wrong" | Fixed one thing but results still don't match |
| Checking same value in multiple files | Looking for "right" version across 3+ copies |
| Comparing outputs from different states | "The sweep showed X but now I see Y" |
| "Must have been" / "might have" | Speculating instead of verifying |

**Rule: 2 unproductive 'wait/actually' moments in sequence = STOP and re-orient.** A 'wait' followed by genuinely new information (reading a file, getting test output) is healthy iteration, not confusion. The signal is going in circles without learning anything new.

### 3. Comparing Incompatible Results

**Rule: Every result has provenance. Before comparing two results, verify they came from the same state.**

| Before Comparing | Verify |
|-----------------|--------|
| Two backtest results | Same script version, same config, same dataset |
| Before vs after a fix | Only the fix changed, nothing else |
| Current vs remembered output | Code hasn't been reverted/changed since the remembered run |
| Sweep results vs single run | Same parameters, same event count, same algorithm version |

## The Re-Orientation Protocol

When confusion is detected (2+ signals), execute immediately:

### Step 1: STOP — 0 more tool calls until oriented.

### Step 2: STATE — Write down what you know for certain.
```
KNOWN FACTS:
- Working on: [task]
- Current file state: [what I can see RIGHT NOW, not what I remember]
- Last successful result: [X] from [specific state/config]
- What changed since then: [every state-changing action]
```

### Step 3: IDENTIFY the confusion source.
- **State changed under me** — git checkout, file edit, or config change not fully accounted for
- **Comparing apples to oranges** — results from different code/config versions
- **Assumption is wrong** — something I "knew" is no longer true
- **Multiple copies** — different versions of same file, reading wrong one

### Step 4: FIX (1-2 tool calls max)
- Verify CURRENT state of critical value (read the file, not memory)
- Restore state if destroyed, or discard stale result and re-run

### Step 5: RESUME — "I now know [X]. The next action is [Y]." Then do Y.

## Prevention

### Pre-Action Checklist for State-Changing Commands

```
1. Will this change any file I haven't committed?
2. Will this change config values affecting my current task?
3. Do I have a way to get back if this goes wrong?
```

If #1 or #2 is "yes" and #3 is "no": commit/stash first, or note critical values.

### Config Change Tracking

When changing ANY configuration value: `CHANGED: [file]:[line] — [key] from [old] to [new]. AFFECTS: [what this controls]`

## Common Confusion Traps

| Trap | Prevention |
|------|-----------|
| `git checkout` during active work reverts ALL uncommitted changes | Use `git stash` or `git show HEAD:path/to/file` to VIEW without reverting |
| Multiple copies of same file (backup, other dirs) | At task start, identify canonical copy. Ignore the rest. |
| Env var vs hardcoded value disagreement | Before running: `grep -r "os.environ\|process.env" [script]` |
| Before/after without controlling variables | One change at a time. Verify between each. |

## Rules

1. **2 unproductive "wait" moments = STOP** — re-orient before continuing
2. **Snapshot before state changes** — git checkout, config edits, file reverts all require noting what was there
3. **Every result has provenance** — before comparing, verify both came from same state
4. **One change at a time** — don't make 3 changes then wonder which mattered
5. **Read the file, don't remember it** — after state change, re-read actual current state
6. **3 "let me check" in a row = you're lost** — stop checking, start orienting
7. **Never speculate when you can verify** — "must have been" is a confusion signal
8. **When confused, output is WRONG** — never deliver results while in a confused state
