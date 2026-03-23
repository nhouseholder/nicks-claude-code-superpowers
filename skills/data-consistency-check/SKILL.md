---
name: data-consistency-check
description: Validates that displayed data is mathematically and logically consistent before claiming correctness. Catches impossible statistics (profit with 0 wins, implausible per-unit returns, mismatched totals). Fires on any data display, dashboard, stats page, table, or summary card.
weight: passive
---

# Data Consistency Check — Numbers Must Make Sense

Before displaying, committing, or approving ANY data output, run it through consistency checks. This is not domain knowledge — it's basic math that Claude keeps failing.

## When to Fire

- Any statistics dashboard, summary card, or performance display
- Any table with calculated values (P/L, win rates, ROI, averages)
- Any aggregated data (totals, sums, counts across categories)
- After any change to scoring, tracking, or results pipelines
- When verifying a screenshot of the website
- **ALWAYS before saying "every cell is correct" or "everything looks good"**

## The Consistency Checks

Run ALL of these. If ANY fails, the data is broken — stop and fix before proceeding.

### 1. Zero-Profit-Zero-Wins Check
```
For each category/card/row:
  IF profit > 0 THEN wins MUST be > 0
  IF profit < 0 THEN losses MUST be > 0
  IF wins == 0 AND losses == 0 THEN profit MUST be 0
```
**Failure example:** "+49.46u, 0W-0L" → IMPOSSIBLE

### 2. Win Rate Sanity
```
  IF wins > 0 THEN win_rate MUST be > 0%
  IF losses > 0 THEN win_rate MUST be < 100%
  win_rate MUST equal wins / (wins + losses) × 100
```
**Failure example:** "0% Win Rate" with positive profit → IMPOSSIBLE

### 3. Per-Unit Plausibility
```
  avg_profit_per_win = total_profit / wins
  IF avg_profit_per_win > 10u THEN SUSPICIOUS (check odds)
  IF avg_profit_per_win > 50u THEN ALMOST CERTAINLY WRONG
```
**Failure example:** +182u from 2 wins = 91u/win → W-L COUNT IS WRONG

### 4. Category Sum Check
```
  sum_of_all_category_bets (W+L across all types) ≈ total_bets_in_header
  sum_of_all_category_profits ≈ total_profit_in_header
```
**Failure example:** ML(516) + Method(2) + others(0) = 518 but Method should have ~200+ bets across 25 events

### 5. Cross-Category Activity Check
```
  IF the algorithm makes predictions for bet_type X:
    THEN X must show non-zero W-L records
  IF event_count > 10 AND a bet_type shows < 5 total bets:
    THEN the tracking is likely broken for that type
```
**Failure example:** 25 events tracked but Method shows 2W-0L → tracking bug

### 6. Internal Consistency
```
  total_displayed = sum(category_profits)
  header_total MUST equal total_displayed
  Each category: W + L = total_bets_for_that_category
```

## How to Check

1. Read each card/row and verify checks 1-3 independently
2. Then verify cross-card checks 4-6
3. If checking a screenshot: read every number, don't skim
4. If checking code output: trace ONE concrete row from data source to display

## Rules

1. **Never skip for "simple" displays** — the simple ones are where this bug hides
2. **Never say "correct" without running the checks** — "I edited the code" is not verification
3. **One impossible number invalidates the entire display** — don't approve 4 good cards and ignore 1 bad one
4. **This skill fires BEFORE verification-before-completion** — data must be consistent before you verify it works
5. **Route to Opus, always** — this is math reasoning, never Sonnet
