---
name: confusion-prevention
description: Detect when Claude is confused and force a re-orientation instead of spiraling. Prevents the "wait... actually... let me check..." pattern where Claude burns 15+ tool calls confused about its own state. Snapshot critical state before destructive actions, recognize confusion signals, and stop to re-orient. Always-on awareness skill.
---

# Confusion Prevention — Stop Spiraling, Start Orienting

## The Problem This Solves

Claude sometimes gets confused about its own state — what version of a file is active, what config values are set, what results came from which run. Instead of stopping to re-orient, Claude spirals:

```
"Wait — 74.0% with 269 picks... that's fewer than 1435..."
"Let me check what the baseline reports..."
"Only 36 events now! The git checkout restored a different version..."
"Let me check the root copy... also 36..."
"Let me check the backup... also 36..."
"So the sweep showed 934W-501L but now I see 199W-70L..."
"The sweep must have been running a DIFFERENT version..."
```

This is 15+ tool calls of confusion. The fix was one line: set NUM_BACKTEST_EVENTS=211. Everything between the first "wait" and that fix was wasted tokens.

## The Three Failure Modes

### 1. State Destruction Without Snapshot

**Pattern**: Claude runs a state-changing command (git checkout, file revert, config change, dependency update) without first recording what the current state was.

**Rule: Before ANY state-changing action, snapshot the critical values.**

| Action | What to Snapshot |
|--------|-----------------|
| `git checkout` / `git reset` | List uncommitted changes, note key config values in working tree |
| Changing a config constant | Note the old value AND what depends on it |
| Reverting a file | Note what the current version contains that the reverted version won't |
| Switching branches | Note any uncommitted work and branch-specific settings |
| Reinstalling dependencies | Note current versions of critical packages |
| Editing env vars | Note the old value |

**Format** (mental note, not output):
```
BEFORE [action]: [key] was [value]. If this changes, [consequence].
```

### 2. The Confusion Spiral

**Pattern**: Claude's internal monologue contains "wait", "actually", "let me check", "that doesn't add up", "something else is wrong" — and instead of pausing to re-orient, it keeps pulling threads, each one revealing more confusion.

**The signals** — if you catch yourself doing ANY of these, you are confused:

| Signal | Example |
|--------|---------|
| "Wait —" | "Wait — 74.0% with 269 picks is the ML-only stream" |
| "That doesn't add up" | "934+501=1435 picks from 36 events doesn't add up" |
| "Let me check" (3rd+ time) | Third "let me check" in a row = you're lost |
| "Something else is wrong" | You fixed one thing but results still don't match |
| Checking the same value in multiple files | Looking for the "right" version across 3+ copies |
| Comparing outputs that came from different states | "The sweep showed X but now I see Y" |
| "Must have been" / "might have" | Speculating instead of verifying |

**The rule: 2 'wait/actually' moments in sequence without new information = STOP and re-orient. A 'wait' followed by genuinely new information (reading a file, getting test output) is healthy iteration, not confusion. The signal is UNPRODUCTIVE 'wait' — going in circles without learning anything new.**

### 3. Comparing Incompatible Results

**Pattern**: Claude compares output A (from state X) with output B (from state Y) without realizing X ≠ Y.

**Rule: Every result has a provenance. Before comparing two results, verify they came from the same state.**

| Before Comparing | Verify |
|-----------------|--------|
| Two backtest results | Same script version, same config, same dataset |
| Before vs after a fix | Only the fix changed, nothing else |
| Current output vs remembered output | The code hasn't been reverted/changed since the remembered run |
| Sweep results vs single run | Same parameters, same event count, same algorithm version |

## The Re-Orientation Protocol

When confusion is detected (2+ signals from above), execute this immediately:

### Step 1: STOP (0 more tool calls until oriented)

Do not read another file. Do not run another command. Do not "just check one more thing."

### Step 2: STATE (write down what you know for certain)

```
KNOWN FACTS:
- I am working on: [task]
- The current file state is: [what I can see RIGHT NOW, not what I remember]
- The last successful result was: [X] from [specific state/config]
- What changed since then: [list every state-changing action]
```

### Step 3: IDENTIFY the confusion source

It's almost always one of these:
- **State changed under me** — a git checkout, file edit, or config change I didn't fully account for
- **Comparing apples to oranges** — two results from different code/config versions
- **Assumption is wrong** — something I "knew" is no longer true
- **Multiple copies** — different versions of the same file exist and I'm reading the wrong one

### Step 4: FIX the orientation (1-2 tool calls max)

- Verify the CURRENT state of the critical value (read the actual file, not memory)
- If state was destroyed, restore it (set the config, revert the file)
- If comparing incompatible results, discard the stale one and re-run

### Step 5: RESUME from the oriented state

One sentence to yourself: "I now know [X]. The next action is [Y]." Then do Y.

## Prevention > Detection

### Pre-Action Checklist for Risky Commands

Before running commands that change state, ask:

```
1. Will this change any file I haven't committed?
2. Will this change config values that affect my current task?
3. Do I have a way to get back to the current state if this goes wrong?
```

If the answer to #1 or #2 is "yes" and #3 is "no":
- **Commit or stash first**
- **Or note the critical values** so you can restore them

### The "Before/After" Rule for Config

When you change ANY configuration value during a task:

```
CHANGED: [file]:[line] — [key] from [old] to [new]
AFFECTS: [what this value controls]
```

This takes 5 tokens and prevents 500 tokens of confusion later.

## Common Confusion Traps (Anti-Patterns)

### Git Checkout During Active Work
**Trap**: `git checkout` to compare with an old version reverts ALL uncommitted changes, not just the file you're looking at.
**Prevention**: Use `git stash` first, or `git show HEAD:path/to/file` to VIEW without reverting.

### Multiple Copies of the Same File
**Trap**: Project has `algorithm.py`, `algorithm_backup.py`, `../ufc-predict-2/algorithm.py` — editing the wrong one.
**Prevention**: At task start, identify which copy is canonical. Ignore the rest.

### Environment Variables vs Hardcoded Values
**Trap**: A sweep script uses `UFC_NUM_EVENTS=211` but the hardcoded default is 36. Results differ and you don't know why.
**Prevention**: Before running, check: "Is this value overridden by env?" `grep -r "os.environ\|process.env" [script]`

### Before/After Without Controlling Variables
**Trap**: Run baseline, make 3 changes, run again. Results differ. Which change caused it?
**Prevention**: One change at a time. Verify between each.

## Rules

1. **2 unproductive "wait" moments = STOP** — going in circles without learning anything new means you are confused. A 'wait' followed by genuinely new information is healthy iteration. Re-orient before continuing.
2. **Snapshot before state changes** — git checkout, config edits, file reverts all require noting what was there.
3. **Every result has provenance** — before comparing, verify both came from the same state.
4. **One change at a time** — don't make 3 changes then wonder which one mattered.
5. **Read the file, don't remember it** — after any state change, re-read the actual current state. Memory is unreliable.
6. **3 "let me check" in a row = you're lost** — stop checking and start orienting.
7. **Never speculate when you can verify** — "must have been" is a confusion signal. Read the file instead.
8. **Prevention is cheaper than detection** — 5 tokens to note a config value saves 500 tokens of confusion spiral.
9. **The canonical copy is the one you're running** — ignore backups, old copies, and other directories unless explicitly needed.
10. **When confused, output is WRONG** — never deliver results to the user while in a confused state. Orient first, then deliver.
