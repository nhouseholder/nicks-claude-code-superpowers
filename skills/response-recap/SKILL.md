---
name: response-recap
description: Always end responses with a plain English recap that summarizes what was done, why, and what it means. Balances technical accuracy with easy comprehension. Fires after every substantive response (not simple Q&A). Helps the user rapidly understand changes, decisions, and current state without re-reading technical output.
---

# Response Recap — Plain English Summary at End of Every Response

After every substantive response, provide a clear, organized recap that helps the user understand what happened, why, and what state things are in now.

## When to Fire

**Always** — after any response that:
- Made code changes (edits, new files, deletions)
- Ran commands with meaningful output
- Completed a multi-step task
- Made architectural decisions
- Debugged or fixed something

**Skip** when:
- Answering a simple factual question (one-liner)
- The response is already just a summary
- User explicitly says they don't want recaps

## The Recap Format

End every qualifying response with a section like this:

```
---

**What happened:** [1-3 sentences — what was done, in plain English]

**Why:** [1 sentence — the motivation or problem being solved]

**What changed:**
- [file/thing] — [what changed in plain words]
- [file/thing] — [what changed in plain words]

**Current state:** [Where things stand now — what works, what's next]
```

## Formatting Rules

### 1. Lead with the "What" — Not the "How"
- BAD: "I edited line 47 of recommend.js to change the scoring weight from 0.4 to 0.6"
- GOOD: "Boosted the science score weight in recommendations so pharmacology data has more influence on results"

### 2. Use Plain English First, Technical Detail Second
- BAD: "Modified the PostToolUse hook in settings.json to add a regex pattern match on .js file extensions"
- GOOD: "Added an automatic syntax check that runs every time a JavaScript file is saved — catches typos before they break anything"

### 3. Keep It Scannable
- Use bullet points, not paragraphs
- Bold the key terms
- Max 5-7 bullet points in "What changed" — group related changes
- If more than 7 items, summarize into categories

### 4. Right Level of Technical Detail
The goal: the user should understand WHAT changed and WHY without needing to read the code, but have enough technical breadcrumbs to find the code if they want to.

- Include: file names, feature names, the "before → after" delta
- Skip: line numbers, exact code syntax, implementation details
- Exception: if the user is debugging or learning, include more technical detail

### 5. Connect to the Big Picture
Always tie back to what the user cares about:
- "This means your quiz results will now prioritize..." (user impact)
- "This fixes the issue where..." (problem resolved)
- "Next time you deploy, this will automatically..." (future benefit)

### 6. End with Current State
The user should know:
- What works now that didn't before
- What's left to do (if anything)
- Whether they need to take any action

## Examples

### After a multi-file code change:
```
---

**What happened:** Added dispensary hours to the map view so users can see if a store is open before driving there.

**Why:** Users were clicking through to dispensaries only to find them closed — wasted time.

**What changed:**
- **Map markers** — now show green (open) / red (closed) / yellow (closing soon)
- **Dispensary card** — added hours display with "Open now" / "Closed" badge
- **Menu fetch** — hours data now pulled from Weedmaps API during daily harvest

**Current state:** Working locally. Ready to deploy — the daily harvest will start pulling hours data on the next cron run (6 AM PT).
```

### After a debugging session:
```
---

**What happened:** Fixed the blank results page that showed up when users selected "No preference" for consumption method.

**Why:** The scoring engine was dividing by zero when no consumption method weight was provided.

**What changed:**
- **recommend.js** — added a fallback so "no preference" skips the consumption score instead of crashing the calculation

**Current state:** Fix is in place. All quiz paths now return results. Committed as v5.64.1.
```

### After a config/infrastructure change:
```
---

**What happened:** Set up 6 new skills and 4 new slash commands in your Claude Code superpowers repo, plus a new "barrier recognition" system.

**Why:** You wanted workflow automation (backtest, audit, deploy, fix-loop) and the ability for Claude to recognize when it's hitting a familiar problem and redirect itself instead of wasting time.

**What changed:**
- **6 new skills** — backtest, audit, deploy, fix-loop, parallel-sweep, barrier-recognition
- **4 new commands** — `/backtest`, `/audit`, `/deploy`, `/fix-loop`
- **CLAUDE.md** — added session chunking rules and barrier awareness guidelines
- **README + SKILLS-REFERENCE** — updated to reflect 44 total skills

**Current state:** Everything installed locally and pushed to GitHub. All skills are active now.
```

## Tone Guidelines

- Conversational but efficient — like a smart coworker giving you a 30-second debrief
- No filler ("I've gone ahead and...", "As requested...", "I hope this helps...")
- No over-explaining — trust the user to ask if something's unclear
- Confident and direct — state what happened, don't hedge
- Match the user's energy — if they're moving fast, keep it tight

## Adaptive Detail

- **Quick fix** → 2-3 line recap
- **Multi-step task** → Full format with bullet points
- **Complex debugging** → Include the "aha moment" — what the root cause was and why the fix works
- **Architecture decisions** → Include the tradeoff that was considered and why this path was chosen
