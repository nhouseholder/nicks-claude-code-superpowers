Debug a website/webapp systematically using the full Debugger Agent pipeline. Finds bugs, fixes them, verifies fixes, and logs everything permanently.

**This command calls agents in order. Do NOT skip phases.**

## Arguments
- `$ARGUMENTS` = bug description, URL, screenshot, or project directory
- If no argument, ask what's broken

## Phase 1: Read History (pre-debug-check)
BEFORE any fix attempt:
- Read `~/.claude/anti-patterns.md` — has this bug been seen before?
- Read `~/.claude/recurring-bugs.md` — is this a repeat offender?
- Read project MEMORY.md for prior context
- If bug was fixed before: announce it, show history, escalate approach

## Phase 2: Baseline Snapshot (website-guardian)
- Screenshot or read current state of the broken page
- Record what IS working (so we don't break it while fixing)
- Record the exact symptoms of the bug

## Phase 3: Isolate (isolate-before-iterate)
- Can this bug be reproduced in a minimal test?
- Write a 5-line reproduction script before running the full app
- If screenshots available: use screenshot-dissector for pixel-level analysis

## Phase 4: Diagnose (systematic-debugging)
- Form a hypothesis: what's the most likely cause?
- Test the hypothesis with ONE targeted check
- If wrong: form a new hypothesis (max 3 per approach)
- Do NOT change code until you have a diagnosis

## Phase 5: Fix (senior-dev-mindset)
- Targeted fix based on diagnosis
- Follow senior-dev-mindset checklist for the domain (Frontend/Backend)
- If website: follow website-guardian fix protocol

## Phase 6: Verify (data-consistency-check + website-guardian)
- Check EVERY baseline item — still working?
- Run data-consistency-check on any numbers/stats
- Scan output for impossible data (Rule 18)
- If webapp-testing Playwright available: run automated verification
- If fix broke something else: fix THAT before declaring done

## Phase 7: Log Permanently (error-memory)
Follow error-memory SKILL.md:
- Root cause (not just symptoms)
- Flawed assumption (what was believed that was false)
- Reasoning lesson (one-line rule to prevent recurrence)
- Append to `~/.claude/anti-patterns.md`
- If recurring: update `~/.claude/recurring-bugs.md` with escalated analysis

## Phase 8: Verify Log
- Confirm anti-patterns.md was updated
- If website bug: update site-update-protocol checklist if new failure mode found

## Output
```
SITE DEBUG COMPLETE
===================
Bug: [description]
Root cause: [what was actually wrong]
Fix: [what was changed] — [files]
Verified: baseline ✓ | data-check ✓ | visual ✓
Logged: anti-patterns.md ✓ | recurring-bugs.md [✓/n/a]
Carelessness type: [from website-guardian table]
Prevention rule: [one-line rule for future agents]
```
