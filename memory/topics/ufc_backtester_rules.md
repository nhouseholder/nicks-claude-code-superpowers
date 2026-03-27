---
name: UFC Backtester Rules — Universal, Non-Negotiable
description: Definitive rules for how the UFC backtester scores every bet type. Every AI agent across every session must follow these exactly. No room for confusion.
type: reference
---

# UFC Backtester — Universal Rules

**READ THIS BEFORE TOUCHING ANY UFC SCORING, P/L, OR BACKTESTING CODE.**

## The 5 Bet Types (1u each)

Every event scores up to 5 bet types. All bets are 1 unit ($1).

| # | Bet Type | What it is | When placed |
|---|----------|-----------|-------------|
| 1 | **ML** | Moneyline — fighter wins | Every fight |
| 2 | **Method** | ML + method of victory (e.g. KO, DEC) | Every fight (unless SUB-gated) |
| 3 | **Round** | ML + predicted round (e.g. R1, R2) | Only KO predictions with R1 predicted round |
| 4 | **Combo** | ML + method + round (e.g. KO in R2) | Only when method AND round are both predicted |
| 5 | **Parlay** | Top 2 ML picks combined at combined decimal odds | 1 per event (HC parlay + high-ROI if no overlap) |

## How Each Bet Wins and Loses

### ML (e.g. "Pereira ML" at -110)
- Pereira wins → **WIN** +0.91u (pays at the odds)
- Pereira loses → **LOSS** -1.00u

### Method (e.g. "Pereira + KO" at +200)
- Pereira wins by KO → **WIN** +2.00u
- Pereira wins by DEC → **LOSS** -1.00u (wrong method)
- Pereira wins by SUB → **LOSS** -1.00u (wrong method)
- Pereira loses → **LOSS** -1.00u

### Round (e.g. "Pereira + R2" at +300)
- Pereira wins in R2 → **WIN** +3.00u
- Pereira wins in R1 → **LOSS** -1.00u (wrong round)
- Pereira wins in R3 → **LOSS** -1.00u (wrong round)
- Pereira wins by DEC → **LOSS** -1.00u (no round match)
- Pereira loses → **LOSS** -1.00u

### Combo (e.g. "Pereira + KO + R2" at +600)
- Pereira wins by KO in R2 → **WIN** +6.00u
- Pereira wins by KO in R1 → **LOSS** -1.00u (wrong round)
- Pereira wins by SUB in R2 → **LOSS** -1.00u (wrong method)
- Pereira wins by DEC → **LOSS** -1.00u
- Pereira loses → **LOSS** -1.00u

### Parlay (e.g. "Pereira + Adesanya ML parlay" at combined +350)
- Both fighters win → **WIN** +3.50u
- Either fighter loses → **LOSS** -1.00u

## The One Rule That Governs Everything

**The ONLY way a prop bet wins is if the EXACT condition hits. Every other outcome is -1u.**

Fighter loses → ALL bets on that fighter lose. Not just ML — method, round, combo ALL lose -1u each.

## Worked Examples

### Example 1: Predict Pereira KO R2, actual KO R1

| Bet | Outcome | P/L |
|-----|---------|-----|
| Pereira ML (-110) | WIN (fighter won) | +0.91u |
| Pereira + KO (+200) | WIN (method correct) | +2.00u |
| Pereira + R2 (+300) | LOSS (wrong round — R1 not R2) | -1.00u |
| Pereira + KO + R2 (+600) | LOSS (wrong round) | -1.00u |
| **Net: 2W-2L** | | **+0.91u** |

### Example 2: Predict Justin SUB R1, actual KO R1

| Bet | Outcome | P/L |
|-----|---------|-----|
| Justin ML (+150) | WIN (fighter won) | +1.50u |
| Justin + SUB (+300) | LOSS (wrong method — KO not SUB) | -1.00u |
| Justin + R1 (+300) | WIN (right round) | +3.00u |
| Justin + SUB + R1 (+800) | LOSS (wrong method) | -1.00u |
| **Net: 2W-2L** | | **+2.50u** |

### Example 3: Predict Murphy DEC, Murphy loses

| Bet | Outcome | P/L |
|-----|---------|-----|
| Murphy ML (+120) | LOSS (fighter lost) | -1.00u |
| Murphy + DEC (+250) | LOSS (fighter lost) | -1.00u |
| No round bet (DEC = no round) | — | — |
| No combo bet (DEC = no round) | — | — |
| **Net: 0W-2L** | | **-2.00u** |

### Example 4: Event table format

```
Fight             | ML       | Method   | Round  | Combo  | Combined
Murphy v Evloev   | X -1.00  | X -1.00  | —      | —      | -2.00
Page v Patterson  | ✓ +0.56  | ✓ +1.90  | —      | —      | +2.46
Duncan v Dolidze  | ✓ +0.22  | ✓ +1.30  | —      | —      | +1.52
PARLAY (Page+Duncan)                                       | +1.80
NET EVENT                                                  | +3.78
```

## Payout Math

- **Positive odds:** profit = stake × (odds / 100). E.g. +200 → 1 × (200/100) = +2.00u
- **Negative odds:** profit = stake × (100 / |odds|). E.g. -110 → 1 × (100/110) = +0.91u
- **Loss:** always -1.00u per bet, no exceptions
- **NEVER use flat +1.00u for wins** — always compute from real Vegas odds

## Gating Rules

| Rule | Effect |
|------|--------|
| SUB method gating | SUB method predictions below confidence threshold → no method/round/combo bets placed |
| DEC predictions | No round bet, no combo bet (decision has no predictable round) |
| **R1 KO ONLY** | Round and combo bets placed ONLY when predicted_method=KO AND predicted_round=1. All R2, R3, SUB rounds gated. Data-driven 2026-03-24. |
| Heavy fav skip | Props skipped for extreme ML favorites (odds below HEAVY_FAV_PROP_SKIP threshold) |

## Backtester Requirements

1. **71-event minimum** (growing — auto-increments, never shrinks)
2. **Walk-forward** — only use data available BEFORE each event
3. **Real Vegas odds** — scraped and cached, never assumed
4. **All 5 bet types** scored per event
5. **Registry is an accumulator** — grows over time, never overwritten with less data
6. **Prop odds are irreplaceable** — once an event passes, those odds pages vanish
7. **One backtester only** — `UFC_Alg_v4_fast_2026.py`, all old versions archived
8. **Cache everything** — fighter stats, fight logs, odds, all cached for instant re-runs

## Systems Integration — SCORING MODIFIERS, NOT INDEPENDENT BETS

**Systems are NOT a 6th bet type. They do NOT place independent bets.**

Systems are scoring pipeline modifiers that influence the algorithm's picks:
- When a system signal AGREES with the algorithm's pick → boost confidence
- When a system signal DISAGREES → lower confidence
- Net positive consensus → algorithm more likely to bet (lower threshold)
- Net negative consensus → algorithm might skip (higher threshold)
- System agreement on method → boost method prediction confidence

**The "Systems P/L" on the website is HYPOTHETICAL TRACKING ONLY.**
It shows what WOULD have happened if you bet $1 on every system signal independently.
It is NOT included in the combined P/L and does NOT represent actual bets.
Purpose: monitor which systems are profitable over time for optimizer guidance.

### System Parameters (all affect the SCORING PIPELINE, not bets)
| Parameter | What it does |
|-----------|-------------|
| `SYSTEM_BET_BOOST` | Add to diff when systems confirm pick |
| `SYSTEM_FADE_PENALTY` | Subtract from diff when systems disagree |
| `SYSTEM_THRESHOLD_ADJ` | Lower PICK_DIFF_THRESHOLD per net agreeing signal |
| `SYSTEM_METHOD_BOOST` | Amplify method score when systems agree on method |
| `SYSTEM_SCORE_WEIGHT` | Base weight for score modification |
| `SYSTEM_WEIGHTS` | Per-system weight dict (0=disabled, 1=standard) |

---

## Optimizer ↔ Backtester ↔ Predictor Pipeline (v11.9)

### Single Source of Truth: constants.json
- **Optimizer** runs → writes optimized values to `constants.json`
- **Backtester/Predictor** reads `constants.json` at startup → overrides hardcoded defaults
- **Website** reads `constants.json` from `webapp/frontend/public/data/constants.json`
- All three systems use **identical parameter values** — no drift possible

### Optimizer Rules (v11.9 — fixed 2026-03-24)
1. Optimizer scoring MUST match backtester scoring — same 12 rules
2. Fighter loss = -1u on every PLACED prop bet (was missing before v11.9)
3. R1 KO gating applies in optimizer too (was missing before v11.9)
4. Parlay P/L is NOT tracked in optimizer (follows from ML accuracy improvement)
5. 61 parameters optimized via 2-pass Differential Evolution + 3-fold expanding-window CV
6. Overfitting protection: L2 regularization (0.10), holdout gate (3% accuracy drop = reject)
7. After optimizer runs, values auto-reload into globals for same-session backtesting

### What the Optimizer Maximizes
```
objective = -normalized_profit - win_bonus + regularization - method_bonus - round_bonus - accuracy_bonus
```
- **Priority #1:** Combined P/L (ML + 0.5× prop profit) — dominant term
- **Priority #2:** ML win rate — 8% weight bonus
- **Priority #3:** Overfitting prevention — L2 penalty for deviating from current values
- **Priority #4:** Method accuracy + round proximity + general accuracy — tiebreakers
