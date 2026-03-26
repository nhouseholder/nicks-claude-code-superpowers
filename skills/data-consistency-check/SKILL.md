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

### 7. Data Completeness
For every bet/prediction where action was taken:
- IF odds == null/missing/"—" AND a bet was placed → **DATA IS INCOMPLETE**
- Action: Run the data pipeline (scraper/backfill) FIRST
- NEVER display "—" for a bet that was placed — missing odds means RUN THE SCRAPER
- NEVER skip to display/formatting fixes when the underlying data is missing
- Only after the scraper confirms the source is genuinely unavailable (page deleted, event too old) can you note "odds unavailable — scraper checked [source] on [date]"

### 8. Cross-Query Consistency
When presenting multiple analyses from the same dataset:
- **Sample sizes must match.** If query 1 says "72 fights" and query 2 uses the same filter, it must also be 72 — not 54, not 48. If the count differs, EXPLAIN why (e.g., "18 fights excluded due to missing R1 odds").
- **Percentages must match their source.** If query 1 says "19.4% end in R1 KO (14/72)" and query 2 says "25.9% win rate (14/54)", those are different denominators — flag it explicitly.
- **Never silently change the dataset between queries.** If you filter differently, say so: "Note: reduced from 72 to 54 because 18 fights had no R1 KO odds available."
- **Cross-check totals.** If the user asks "what if we routed ALL X bets to Y", the bet count must equal the original X count unless you explain the reduction.

**Anti-pattern:** User asks about 72 KO R2 predictions, then asks "route all to R1." Claude returns 54 bets with no explanation of where 18 fights went. User loses trust in all the numbers.

### 9. Single-Pass Analysis (prevents query drift)
When answering multiple related questions about the same dataset:
- **Extract ALL data in ONE pass.** Write a single script/query that pulls every field you'll need for all questions. Compute all answers from that one extraction.
- **Never run separate queries per question.** Each new query risks different filters, different name matching, different edge case handling — producing numbers that contradict each other.
- **Show your denominator.** Every percentage, win rate, or count must show `X/Y` format (e.g., "14/72 = 19.4%"). If the denominator changes between tables, it's immediately visible.
- **Lock the dataset.** At the start of a multi-question analysis, state: "Working from [N] records matching [filter]." All subsequent answers must use that same N or explicitly explain reductions.

**Anti-pattern:** User asks 3 questions about KO R2 predictions. Claude runs 3 separate queries. Query 1: 72 fights. Query 2: 54 bets (different name matching). Query 3: 55 bets ("improved" matching). P/L shifts from -3.08u to -0.53u. User can't trust any of the numbers. ONE script, ONE pass, ONE dataset.

## How to Check

1. Read each card/row and verify checks 1-3 independently
2. Then verify cross-card checks 4-6
3. Then verify cross-query checks 7-8 if multiple analyses
4. If checking a screenshot: read every number, don't skim
5. If checking code output: trace ONE concrete row from data source to display

## Rules

1. **Never skip for "simple" displays** — the simple ones are where this bug hides
2. **Never say "correct" without running the checks** — "I edited the code" is not verification
3. **One impossible number invalidates the entire display** — don't approve 4 good cards and ignore 1 bad one
4. **This skill fires BEFORE verification-before-completion** — data must be consistent before you verify it works
5. **Route to Opus, always** — this is math reasoning, never Sonnet
