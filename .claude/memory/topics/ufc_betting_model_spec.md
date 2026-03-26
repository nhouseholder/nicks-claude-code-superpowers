# UFC BETTING MODEL SPECIFICATION — CANONICAL & IMMUTABLE

**Created:** 2026-03-23
**Last verified:** 2026-03-24 — Independent bout-level audit, ALL 12 scoring checks PASS
**Optimizer fixed:** 2026-03-24 — v11.9: optimizer now scores identically to backtester (fighter loss prop scoring + R1 KO gating + constants.json auto-load)
**Authority:** User-defined, non-negotiable. NO AI agent may deviate from this spec.
**Applies to:** Every backtester, scorer, registry, website display, and future session.

## VERIFIED NUMBERS (2026-03-24 — DEFINITIVE, ALL 12 RULES PASS)

Source: Independent audit of bout-level data in `ufc_profit_registry.json`
Method: Sum each bet type's pnl from every bout, verify all 12 rules, zero violations.
**These numbers are THE TRUTH. If you get different numbers, your code has a bug.**

| Bet Type | W-L | Win% | P/L | ROI% |
|----------|-----|------|-----|------|
| ML | 353W-141L | 71.5% | +108.11u | +21.9% |
| Method | 152W-212L | 41.8% | +80.60u | +22.1% |
| Round | 19W-25L | 43.2% | -4.46u | -10.1% |
| Combo | 16W-28L | 36.4% | +29.23u | +66.4% |
| Parlay | 31W-32L | 49.2% | +28.03u | +44.5% |
| **TOTAL** | **1009 bets** | | **+241.51u** | **+23.9%** |

**494 bouts across 71 events (70 scored, 1 without odds data)**
**Round/Combo gating: R1 KO only (2026-03-24, +45.68u improvement)**

### How to reproduce
```python
# Run from ufc-predict directory:
python3 -c "
import json
reg = json.load(open('ufc_profit_registry.json'))['events']
ml_pnl = sum(b.get('ml_pnl',0) or 0 for e in reg for b in e.get('bouts',[]))
# ... (see verify_registry.py for full script)
"
```

### Scoring Rule Checks (ALL 12 PASS — zero violations)
Verified 2026-03-24 via comprehensive bout-level audit.

---

## THE 4-BET MODEL (per fight) + PARLAY (per event)

For each fight the algorithm picks, up to 4 bets are placed at **1 unit each**:

| # | Bet Type | What It Is | Odds Source | Stake |
|---|----------|-----------|-------------|-------|
| 1 | **ML** | Fighter wins (moneyline) | Live Vegas odds | 1u |
| 2 | **Method** | Fighter wins + predicted method (KO/SUB/DEC) | Fighter + method prop odds | 1u |
| 3 | **Round** | Fighter wins + predicted round (R1/R2/R3/etc.) | Fighter + round prop odds | 1u |
| 4 | **Combo** | Fighter wins + predicted method + predicted round | Fighter + method + round prop odds | 1u |

**5th bet type — PARLAY** is per-event, not per-fight:
| # | Bet Type | What It Is | Odds Source | Stake |
|---|----------|-----------|-------------|-------|
| 5 | **Parlay** | Top 2+ ML picks combined | Combined ML decimal odds | 1u |

---

## THE 12 SCORING RULES — IMMUTABLE, UNIVERSAL, NO EXCEPTIONS

Every AI agent, every backtester, every scorer, every display must enforce ALL 12 rules.
Violation of ANY rule means the data is WRONG.

### Rule 1: Fighter loss = -1.0u on EVERY placed bet
If the picked fighter loses, every bet placed on that fighter is -1.00u.
- ML: -1.00u
- Method (if placed): -1.00u
- Round (if placed): -1.00u
- Combo (if placed): -1.00u
- Combined: sum of all placed bets (up to -4.00u)
There is NO scenario where Method/Round/Combo wins but ML loses.

### Rule 2: Payouts use REAL odds, never flat +1u
```
Positive odds (+150): profit = stake × (odds / 100)     → +1.50u
Negative odds (-200): profit = stake × (100 / |odds|)   → +0.50u
Loss (any):           profit = -stake                     → -1.00u
```
NEVER use +1.00u for a win. Every win pays at the actual sportsbook odds.

### Rule 3: ALL prop bets require ML win
Method, Round, AND Combo bets are ALL contingent on the fighter winning.
- Fighter loses → Method LOSES, Round LOSES, Combo LOSES
- This is because the bet is "Fighter X wins by KO" — if Fighter X didn't win, the bet lost
- There is NO independent prop bet. They are all parlayed with the ML pick.

### Rule 4: Combo wins require ALL 3 correct
combo_correct = True ONLY when:
- ml_correct = True (fighter won)
- method_correct = True (correct method)
- round_correct = True (correct round)
If ANY of these is False, combo is a LOSS (-1.00u).

### Rule 5: No bet without odds
If method_odds is null/missing/`__NO_PROPS__`, no method bet was placed.
That fight shows "—" for method. Not a win, not a loss. Zero units.
Same for round_odds, combo_odds. No odds = no bet = not scored.

### Rule 6: No round/combo bet on DEC predictions
If the algorithm predicts Decision, there is no round to bet on.
- Round = "—" (not placed)
- Combo = "—" (not placed, since combo requires round)
- That fight gets ML + Method only (max 2 bets)

### Rule 7: Variable bet count per fight
A fight can have 1, 2, 3, or 4 bets depending on odds availability and prediction:
- **1 bet**: ML only (no prop odds available at all)
- **2 bets**: ML + Method (DEC prediction, OR only method odds available)
- **3 bets**: ML + Method + Round (method and round odds available, no combo odds)
- **4 bets**: ML + Method + Round + Combo (all odds available, non-DEC prediction)
NEVER assume every fight has 4 bets. Count only actually-placed bets.

### Rule 8: Method bet scoring
The bet is "Fighter X wins by [KO/SUB/DEC]"
- Wins ONLY if: fighter wins AND actual method matches predicted method
- Loses if: fighter loses (-1u) OR fighter wins by wrong method (-1u)
- KO and TKO are the same category for scoring purposes

### Rule 9: Round bet scoring
The bet is "Fighter X wins in [R1/R2/R3/etc.]"
- Wins ONLY if: fighter wins AND fight ends in the exact predicted round
- Loses if: fighter loses (-1u) OR fight ends in wrong round (-1u) OR fight goes to decision (-1u)
- Method and Round are scored INDEPENDENTLY of each other

### Rule 10: Parlay is the 5th bet type
- 1u per parlay, scored independently from individual fight bets
- Per EVENT, not per fight
- HC parlay (top 2 confidence picks) + high-ROI parlay (if no fighter overlap with HC)
- If fighter overlap exists between HC and ROI parlay, default to HC parlay only
- Parlay odds = multiply decimal odds of all legs
- Wins only if ALL legs win. One loss kills the entire parlay.
- Payout: 1u × (combined_decimal - 1)

### Rule 11: Total bets per event = sum of fight bets + parlay bets
- Not a fixed number. Each event has a different number of total bets.
- Event total = Σ(bets per fight) + parlay bet(s)
- Example: 3 fights × 2 bets each + 1 parlay = 7 total bets for that event

### Rule 12: W-L counts must match
For each bet type: Wins + Losses = total bets placed in that category.
- No unaccounted bets. No phantom wins or losses.
- sum(ML W+L) + sum(Method W+L) + sum(Round W+L) + sum(Combo W+L) + sum(Parlay W+L) = total bets
- If these don't add up, the scoring code has a bug.

---

## SCORING INDEPENDENCE (Method vs Round)

Method and Round are scored INDEPENDENTLY of each other:
- Predict "KO in R2", actual "KO in R1": Method WINS (+odds), Round LOSES (-1u), Combo LOSES (-1u)
- Predict "SUB in R1", actual "KO in R1": Method LOSES (-1u), Round WINS (+odds), Combo LOSES (-1u)
- Predict "KO in R2", actual "KO in R2": Method WINS (+odds), Round WINS (+odds), Combo WINS (+odds)

---

## WORKED EXAMPLES

### Example 1: Pereira predicted KO R2, actual KO R1
| Bet | Odds | Outcome | P/L |
|-----|------|---------|-----|
| ML | -110 | WIN (fighter won) | +0.91u |
| Method (KO) | +200 | WIN (method correct) | +2.00u |
| Round (R2) | +300 | LOSS (wrong round, actual R1) | -1.00u |
| Combo (KO+R2) | +600 | LOSS (wrong round) | -1.00u |
| **Net** | | **2W-2L** | **+0.91u** |

### Example 2: Justin predicted SUB R1, actual KO R1
| Bet | Odds | Outcome | P/L |
|-----|------|---------|-----|
| ML | +150 | WIN (fighter won) | +1.50u |
| Method (SUB) | +300 | LOSS (wrong method, actual KO) | -1.00u |
| Round (R1) | +300 | WIN (correct round) | +3.00u |
| Combo (SUB+R1) | +800 | LOSS (wrong method) | -1.00u |
| **Net** | | **2W-2L** | **+2.50u** |

### Example 3: Fighter predicted DEC, actual DEC (decision = no round bet)
| Bet | Odds | Outcome | P/L |
|-----|------|---------|-----|
| ML | -200 | WIN | +0.50u |
| Method (DEC) | +110 | WIN | +1.10u |
| Round | NOT PLACED (DEC has no round) | — |
| Combo | NOT PLACED (no round = no combo) | — |
| **Net** | | **2W-0L** | **+1.60u** |

### Example 4: Fighter LOSES
| Bet | Odds | Outcome | P/L |
|-----|------|---------|-----|
| ML | +150 | LOSS | -1.00u |
| Method | +300 | LOSS (fighter lost) | -1.00u |
| Round | +400 | LOSS (fighter lost) | -1.00u |
| Combo | +800 | LOSS (fighter lost) | -1.00u |
| **Net** | | **0W-4L** | **-4.00u** |

---

## PAYOUT FORMULA

```
Positive odds (+150): profit = stake × (odds / 100)     → 1 × (150/100) = +1.50u
Negative odds (-200): profit = stake × (100 / abs(odds)) → 1 × (100/200) = +0.50u
Loss:                 profit = -stake                     → -1.00u
```

**NEVER use +1.00u for a win.** Always use actual odds.

---

## BET AVAILABILITY

Not every fight has all 4 bets. Bets require odds from the sportsbook:
- **ML**: Always available (required to pick a fight)
- **Method**: Available when method prop odds exist
- **Round**: Available when round prop odds exist AND prediction is NOT a decision
- **Combo**: Available only when BOTH method AND round odds exist AND prediction is NOT a decision

If odds are unavailable for a bet type, that bet is simply not placed (not scored as win or loss).

### Gating Rules (bets NOT placed even if odds exist)
- **SUB method bets**: Gated when sub_sc < SUB_GATE_THRESHOLD (too unreliable)
- **Heavy favorite props**: Gated when ML odds <= HEAVY_FAV_PROP_SKIP threshold
- **Round/Combo: R1 KO ONLY** (2026-03-24, data-driven). Only place round and combo bets when predicted_method=KO AND predicted_round=1. All other round/combo bets gated.
  - R1 KO round+combo: +24.77u (44 bets). Everything else: -45.69u (96 bets).
  - SUB round bets: -64.5% ROI. R2 KO: -13.7% ROI. Only R1 KO is viable.

---

## PARLAY RULES

- **Per event**, not per fight
- Top 2 ML picks by model confidence
- Combined decimal odds = leg1_decimal × leg2_decimal
- Stake: **1 unit** (same as all other bet types)
- Wins only if ALL legs win
- Payout: 1 × (combined_decimal - 1)
- Loss: -1.00u

---

## BACKTESTER REQUIREMENTS

### Core Rules
1. **71 events minimum** (auto-incrementing, never shrinks)
2. **Walk-forward only** — no future data leakage
3. **All odds from cached scrapes** — never assumed or fabricated
4. **Registry must store per-bout:** ml_pnl, method_pnl, round_pnl, combo_pnl, combined_pnl, all odds, predicted vs actual method/round
5. **Registry must store per-event:** parlay_pnl, parlay_legs, parlay_odds
6. **Totals must be recomputable** from bout-level data (no magic numbers)

### There Is ONE Backtester
- **File:** `UFC_Alg_v4_fast_2026.py` — the ONLY backtester. No 25-event version exists.
- **If a backtest shows fewer than 71 events, STOP.** Wrong file, wrong config, or wrong env var.
- All old backtesters archived with `.ARCHIVED.py` suffix. Never run archived files.

### Backtester Must Handle
- All 5 bet types per event (ML, Method, Round, Combo, Parlay)
- Correct units: -1u for every loss, +odds_payout for every win
- Real Vegas odds from cache, never fabricated
- Parlays: HC parlay + ROI parlay (if no fighter overlap), 1u each
- Dynamic growth: new events added after they occur, window only grows
- Fighter losses: ALL placed bets lose (-1u each)
- Method and round scored INDEPENDENTLY

### Data Caching Rules
- Cache ALL scraped data on first scrape (odds, stats, fight logs)
- Subsequent runs: read cache first, only scrape genuinely new data
- Commit caches to GitHub
- Prop odds cache is IRREPLACEABLE — once events pass, odds pages disappear
- Never trust a fresh scrape over cached historical data

### Pre-Run Checklist
1. `cp ufc_profit_registry.json ufc_profit_registry_backup_$(date +%Y%m%d).json`
2. Set `UFC_BACKTEST_MODE=1` and `UFC_NUM_EVENTS=71`
3. After run: compare new registry field-by-field against backup
4. If ANY event lost data (pnl went from value to null, W-L counts dropped), ABORT and restore

### Domain Knowledge Requirement
Before touching ANY UFC scoring code, read:
- `~/.claude/memory/topics/ufc_betting_domain_knowledge.md` — expert-level betting reference
- This file (the canonical spec)

---

## THIS SPEC IS THE SINGLE SOURCE OF TRUTH

If any code, display, or AI behavior contradicts this document:
1. This document is correct
2. The code/display/behavior is wrong
3. Fix the code, not this document

**Do NOT modify this spec without explicit user approval.**

---

## CRITICAL REASONING RULE FOR AI AGENTS

**When a fighter LOSES, every prop bet on that fighter is a LOSS. Period.**

This means:
- ML loss = -1u
- Method loss = -1u (the bet was "Fighter wins by KO" — fighter didn't win)
- Round loss = -1u (the bet was "Fighter wins in R2" — fighter didn't win)
- Combo loss = -1u (the bet was "Fighter wins by KO in R2" — fighter didn't win)

When analyzing any bet type's ROI, you MUST count fighter losses as losses for that bet type. A "Round 2" bet that lost because the fighter lost is still a Round 2 loss. Do not exclude it, do not treat it as "not a round prediction failure." It is -1u on the round bet.

**Never compare registry before/after totals to evaluate gating changes.** The fighter-loss accounting shifts between categories when a gate is toggled. Instead, count wins and ALL losses for the specific bet type independently.
