# Recurring Bugs Tracker

> Tracks bugs that have been reported 2+ times. When a bug appears here,
> the fix approach must be escalated — the previous fix was insufficient.
> Checked by pre-debug-check and error-memory before any fix attempt.

## Format
Each entry: Bug category | Times reported | Last occurrence | Root cause pattern

## Active Recurring Bugs

### P/L CALCULATION ERRORS — 4x reported (CRITICAL)
- **Pattern**: Win payouts shown as flat +1.00u instead of actual odds-based payout. Losses only count ML, not all bet types on the losing fighter.
- **Root cause**: Claude's mental model defaults to "win = +1 unit" instead of "win = payout at odds." This is a DOMAIN KNOWLEDGE gap, not a code bug. Fixing individual bet types doesn't work — the same error recurs on the next bet type.
- **Escalation**: MANDATORY rules now in CLAUDE.md "Sports Betting Payout Rules" section. Must re-read before ANY P/L code. wins = stake * (odds/100), losses = -1u PER BET TYPE on losing fighter, actual odds must be scraped.
- **Last**: 2026-03-22

### IMPOSSIBLE STATISTICS ACCEPTED AS CORRECT — 5x reported (CRITICAL)
- **Pattern**: Claude displays/approves stats that are mathematically impossible (profit with 0 wins, 91u/win on standard odds, 0% win rate with positive P/L)
- **Root cause**: Claude checks if the UI renders, not if the NUMBERS are possible. No invariant checking.
- **Escalation**: 7 mandatory data invariants now in CLAUDE.md. Must check EVERY card/stat against invariants before claiming correctness. This is MATH, not domain knowledge.
- **Last**: 2026-03-22

### "FIXED" BUT NOT VERIFIED — 3x reported  
- **Pattern**: Claude claims "fixed" based on code edits, user finds it's still broken
- **Root cause**: No output verification. "I edited the code" treated as evidence of correctness.
- **Escalation**: Must check actual rendered output (screenshot, DOM, preview) before claiming any fix is complete.
- **Last**: 2026-03-22

### REGRESSION DURING FIX — 2x reported
- **Pattern**: Fixing one thing breaks another that was previously working
- **Root cause**: Not checking baseline values before editing. No "before vs after" comparison.
- **Escalation**: Record baseline values for ALL related metrics BEFORE making any changes. Compare after.
- **Last**: 2026-03-22
