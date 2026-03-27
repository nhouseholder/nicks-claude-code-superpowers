# UFC Betting Domain Knowledge — Expert Reference

**Purpose:** Claude must understand UFC betting at an expert level. This file exists because Claude repeatedly made fundamental betting mistakes (excluding fighter losses from prop analysis, using flat +1u payouts, flip-flopping on gating decisions). Every AI agent must read this before touching any UFC code.

**Source:** Sportsbook settlement rules (BestFightOdds, DraftKings, FanDuel), verified by user.

---

## 1. UFC Bet Types at Real Sportsbooks

### Moneyline (ML)
- Pick which fighter wins. No point spreads in MMA — purely win/lose.
- Odds range: heavy favorites -600 to slight underdogs +300+
- Highest-volume UFC market. Every fight has ML odds.

### Method of Victory (MOV / Method Prop)
- Bet on HOW a specific fighter wins. Standard categories:
  - **KO/TKO** (punches, kicks, elbows, head kicks, doctor stoppages, corner stoppages — ALL grouped together)
  - **Submission** (all chokes and joint locks)
  - **Decision** (Unanimous, Split, Majority — ALL grouped together)
- Some books offer 6-way markets (each fighter × each method). Others offer 4-way.
- **KO and TKO are ALWAYS the same category at every sportsbook.**

### Round Betting
- **Exact round prop:** Bet which specific round the fight ends. R1, R2, R3 (or R1-R5 for title fights), or Goes to Decision.
- **Over/Under total rounds:** e.g., Over 2.5 / Under 2.5.
- Round props only exist for finishes — a decision has no specific round.

### Method + Round Combo (Exact Finish)
- Predict BOTH method AND round. E.g., "Fighter A by KO/TKO in Round 1."
- Typically 18-30 possible outcomes per fight.
- Highest payout prop because hardest to hit. Typical odds: +400 to +2500.

### Parlays
- Combine multiple bets into one wager. ALL legs must win.
- Can parlay MLs across multiple fights on a card.
- Parlay odds = multiply decimal odds of all legs.
- One loss kills the entire parlay.

---

## 2. Odds Math (American Odds)

### Conversion Table
| American Odds | Decimal | Implied Prob | $100 Bet Profit |
|:---:|:---:|:---:|:---:|
| -500 | 1.20 | 83.3% | $20 |
| -300 | 1.33 | 75.0% | $33.33 |
| -200 | 1.50 | 66.7% | $50 |
| -150 | 1.67 | 60.0% | $66.67 |
| -110 | 1.91 | 52.4% | $90.91 |
| +100 | 2.00 | 50.0% | $100 |
| +150 | 2.50 | 40.0% | $150 |
| +200 | 3.00 | 33.3% | $200 |
| +300 | 4.00 | 25.0% | $300 |
| +400 | 5.00 | 20.0% | $400 |
| +600 | 7.00 | 14.3% | $600 |
| +1200 | 13.00 | 7.7% | $1200 |

### Payout Formulas
```
Positive odds (+150): profit = stake × (odds / 100)      → 1u × 1.50 = +1.50u
Negative odds (-200): profit = stake × (100 / |odds|)    → 1u × 0.50 = +0.50u
Loss (any odds):      profit = -stake                     → -1.00u
```

**CRITICAL: NEVER use flat +1.00u for a win.** Always compute from actual odds.

### Parlay Odds Calculation
1. Convert each leg to decimal: positive = (odds+100)/100, negative = (|odds|-100)/|odds| + 1... actually:
   - Positive: decimal = (odds / 100) + 1. So +200 → 3.00
   - Negative: decimal = (100 / |odds|) + 1. So -150 → 1.667
2. Multiply all decimal odds together.
3. Profit = stake × (combined_decimal - 1)

Example: 2-leg parlay at -150 and +200:
- Leg 1: 1.667, Leg 2: 3.00
- Combined: 1.667 × 3.00 = 5.00
- $1 bet profit: $4.00

---

## 3. Settlement Rules (THE MOST IMPORTANT SECTION)

### Core Principle
**A prop bet wins ONLY if the EXACT condition is met. Every other outcome is a LOSS.**

### Method of Victory Settlement
| You Bet | What Happens | Result |
|---------|-------------|--------|
| Fighter A by KO | A wins by KO | **WIN** — pays at odds |
| Fighter A by KO | A wins by SUB | **LOSS** — wrong method |
| Fighter A by KO | A wins by DEC | **LOSS** — wrong method |
| Fighter A by KO | A **LOSES** (any way) | **LOSS** |
| Fighter A by KO | No Contest | VOID — stake returned |

### Round Prop Settlement
| You Bet | What Happens | Result |
|---------|-------------|--------|
| Fighter A in R2 | A wins in R2 | **WIN** |
| Fighter A in R2 | A wins in R1 | **LOSS** — wrong round |
| Fighter A in R2 | A wins in R3 | **LOSS** — wrong round |
| Fighter A in R2 | A wins by DEC | **LOSS** — no specific round |
| Fighter A in R2 | A **LOSES** (any way) | **LOSS** |

### Combo (Method + Round) Settlement
| You Bet | What Happens | Result |
|---------|-------------|--------|
| A by KO in R2 | A wins by KO in R2 | **WIN** |
| A by KO in R2 | A wins by KO in R1 | **LOSS** — wrong round |
| A by KO in R2 | A wins by SUB in R2 | **LOSS** — wrong method |
| A by KO in R2 | A wins by DEC | **LOSS** |
| A by KO in R2 | A **LOSES** | **LOSS** |

### THE GOLDEN RULE
**Fighter loses → ALL prop bets on that fighter LOSE. Period. No exceptions.**

This means:
- If you placed ML + Method + Round + Combo (4 bets, 4 units), and the fighter loses: -4.00u total.
- The method bet doesn't get a pass because "it wasn't a method failure." The bet was "Fighter A wins by KO" — Fighter A didn't win. Loss.
- The round bet doesn't get excluded because "it wasn't a round prediction failure." The bet was "Fighter A in R2" — Fighter A didn't win. Loss.

---

## 4. Common Mistakes Claude Has Made (NEVER REPEAT)

### Mistake 1: Excluding Fighter Losses from Prop Analysis
**Wrong:** "R1 round bets are 12W-1L (92.3% win rate) when the fighter wins"
**Right:** "R1 round bets are 12W-13L (48.0% win rate) counting all outcomes"

Fighter losses ARE round bet losses. Never filter them out. Never analyze prop performance "conditional on ML being correct." The real P/L includes every loss.

### Mistake 2: Flat +1u Payouts
**Wrong:** Win = +1.00u, Loss = -1.00u
**Right:** Win at -200 = +0.50u, Win at +200 = +2.00u, Loss = -1.00u

### Mistake 3: Treating Props as Independent of ML
**Wrong:** "Method bet is a separate bet from ML"
**Right:** Method bet IS a parlay with ML. "Fighter A wins by KO" includes both conditions: (1) Fighter A wins AND (2) by KO. Both must be true.

### Mistake 4: Flip-Flopping on Data-Driven Decisions
**Wrong:** Gating R2 → reverting → re-gating → reverting → re-gating (5 times)
**Right:** Analyze once with correct methodology, confirm with user, implement once.

If re-analysis produces different numbers, the analysis has a BUG. Read raw data directly.

### Mistake 5: Re-Running Backtests That Destroy Historical Data
**Wrong:** Running a fresh 71-event backtest that re-scrapes odds (getting __NO_PROPS__) and overwrites the registry that had real odds cached from prior sessions.
**Right:** NEVER overwrite a registry without backing it up first. NEVER trust a fresh scrape over cached historical odds. The registry IS the source of truth for historical odds.

---

## 5. What a Professional UFC Betting Website Should Display

### Per-Event Display (Event Table)
```
FIGHT              | ML      | METHOD  | ROUND  | COMBO  | COMBINED
Murphy v Evloev    | X -1.00 | X -1.00 | —      | —      | -2.00
Page v Patterson   | ✓ +0.56 | ✓ +1.90 | —      | —      | +2.46
Duncan v Dolidze   | ✓ +0.22 | ✓ +1.30 | —      | —      | +1.52
PARLAY (Page+Duncan)                                      | +1.80
EVENT TOTAL        | -0.22   | +0.20   | —      | —      | +3.78
```

Rules:
- Fighter LOSS → "X -1.00u" in every column where a bet was placed
- Fighter WIN, no odds → "✓ —" (checkmark, no dollar amount)
- No bet placed → "—"
- NEVER show "0.00u" with wins > 0

### Dashboard Stats
- Total units wagered, total P/L, overall ROI%
- W-L record and ROI PER BET TYPE (ML, Method, Round, Combo, Parlay — all 5)
- Current and max win/loss streaks
- Event-by-event P/L with running total

### Charts
- **Cumulative P/L curve** — most important visual. ALL lines start at (0,0) from event 1.
- ROI by bet type (bar chart)
- Profit breakdown by odds bucket
- Rolling 10-event trend line

### Design Standards (from screenshot bugs)
- X-axis labels: angled -45°, at least 100px height so text isn't cut off
- Legend: no overlap, no truncation. Use 2-row layout if needed.
- Chart must start at event 1, not midway through the dataset
- Event names: show full name or truncate with "..." only after 40+ chars, not "UFC ..."
- No "Please fill out this field" browser tooltips on non-form elements
- All 5 bet type colors must be visually distinct and consistent across all pages

---

## 6. 3-Round vs 5-Round Fight Differences

| | 3-Round Fight | 5-Round (Title/Main Event) |
|---|---|---|
| Total rounds | 3 | 5 |
| Round props available | R1, R2, R3, DEC | R1, R2, R3, R4, R5, DEC |
| Finish probability | Higher per round | Lower per round (more time to recover) |
| Decision likelihood | ~50-60% | ~40-50% |
| O/U standard line | 1.5 or 2.5 | 2.5, 3.5, or 4.5 |

The algorithm should model these differently. Round prediction accuracy differs significantly between 3-round and 5-round fights.

---

## 7. KO vs TKO Distinction (For Algorithm Purposes)

For BETTING purposes, KO and TKO are the same category. Every sportsbook groups them together.

For ALGORITHM purposes, the data may distinguish them:
- **KO**: Fighter unconscious or knocked down and can't continue
- **TKO**: Referee stops fight due to strikes, corner stoppage, doctor stoppage, cut stoppage
- Both count as "KO/TKO" for method of victory props

The algorithm should treat KO and TKO as identical when scoring method bets.

---

**This document is permanent reference material. It should be read at the start of any UFC-related session and never contradicted by AI reasoning.**
