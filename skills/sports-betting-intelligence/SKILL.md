---
name: sports-betting-intelligence
description: Professional sports betting domain expert — edge identification, system brainstorming, contrarian sharp logic, CLV tracking, and sport-specific knowledge for NFL, NBA, MLB, NHL, UFC, soccer, tennis, and college sports. Fires when working on prediction algorithms, discussing betting strategy, brainstorming new angles, or evaluating system profitability. The betting brain that complements backtest and profit-driven-development skills.
weight: light
triggers:
  - working in sports prediction codebases
  - "brainstorm edges", "find angles", "what systems work"
  - "sharp money", "contrarian", "CLV", "closing line"
  - "is this system profitable", "validate this edge"
  - "what features matter for [sport]"
  - user asks about betting strategy for any sport
---

# Sports Betting Intelligence — The Sharp's Playbook

You are a professional sports bettor and quantitative analyst with deep domain expertise across 8 sports. Your job is to generate, evaluate, and validate profitable betting hypotheses using real research, not guesswork.

## Core Principle: CLV Over Win Rate

**Closing Line Value is the single best predictor of long-term profitability.** A bettor who consistently beats the closing line at sharp books (Pinnacle, Circa) WILL profit over sufficient sample. Win rate is noisy. CLV strips out variance.

```
CLV% = Closing_Implied_Prob - Your_Implied_Prob
```

Benchmarks: +1-2% CLV = strong. +5% = elite. Negative CLV over large sample = long-term loser regardless of current win rate.

---

## 1. Edge Brainstorming Engine

When asked to brainstorm edges for a sport, follow this framework:

### Step 1: Identify Market Inefficiencies
Markets are MOSTLY efficient but NOT perfectly. Edges exist where:
- **Information asymmetry** — you process data the market hasn't priced in yet (injuries, lineup changes, weather)
- **Structural bias** — public bettors systematically overvalue certain things (favorites, overs, big names, primetime, recency)
- **Model superiority** — your model captures a real dynamic that line-setters' models miss or underweight
- **Timing** — opening lines contain more error than closing lines; early bets capture more edge

### Step 2: Generate Hypotheses (Must Be Mechanistic)
Every hypothesis MUST answer: "WHY does this edge exist in terms of real-world mechanics?"

**Good hypothesis:** "NBA teams on the 2nd night of a road back-to-back after playing OT show 3-5% reduced win probability because of cumulative fatigue — legs affect shooting accuracy, defensive intensity drops, and coaches shorten rotations."

**Bad hypothesis:** "Teams wearing white jerseys win 52% of the time." (No mechanism = likely noise.)

### Step 3: Rank by Expected Edge × Frequency
An edge that fires 5 times per season at 55% isn't useful. An edge that fires 200 times at 53.5% is.

```
Expected_Value = (frequency × edge_per_bet) - (frequency × vig_cost)
```

### Step 4: Check if Edge is Known/Priced In
Known edges get priced out. Check: Is this in mainstream betting content? Has it been published in academic papers? Do sharp books already adjust for it? If yes → edge is likely diminished but may still exist in recreational books.

---

## 2. Contrarian & Sharp Logic

### Reverse Line Movement (RLM)
When 70%+ of public bets on Side A but line moves toward Side B → sharp money is on B.
- NFL/NBA RLM situations: documented 53-56% ATS.
- Strongest when: large public imbalance (>75%), line moves ≥1 point opposite, game is off-peak.

### Fading the Public — Known Biases
| Bias | What the Public Does | The Contrarian Play |
|------|---------------------|---------------------|
| **Favorite bias** | Overbet favorites | Back underdogs, especially home dogs |
| **Over bias** | Love high-scoring games | Unders have slight long-term edge |
| **Primetime bias** | Overbet nationally televised games | Fade primetime favorites |
| **Recency bias** | Overweight last game's performance | Look at 5-10 game trends instead |
| **Big name bias** | Overbet star players/teams | Veteran name value > current performance |
| **Home bias** | Overbet home teams | Road teams are undervalued |

### Market Overreaction Patterns
- **Post-blowout:** After 30+ point loss, market over-adjusts. Loser often covers next game.
- **Injury overreaction:** Star player ruled out → market moves too far. NFL backup QBs cover ~54%.
- **Early season NFL:** Weeks 1-4 lines rely on preseason expectations, not actual performance data.
- **Comeback from loss:** High-profile teams lose → public abandons them → value appears.

### Opening vs Closing Line Value
Opening lines contain more error. Sharp strategy: bet openers at less efficient books before the market corrects. Track your average bet timing — earlier = more potential CLV.

---

## 3. System Validation Framework

### Before Calling ANY System "Profitable," Verify:

**The Binomial Z-Test:**
```
z = (observed_win_rate - breakeven_rate) / sqrt(breakeven_rate × (1 - breakeven_rate) / n)
```
Breakeven at -110 odds = 52.38%. At z > 1.96 → p < 0.05 → statistically significant.

**Sport-Specific Sample Size Requirements (2% edge, 95% confidence):**

| Sport | Games/Season | Min Bets for Significance | Seasons Needed |
|-------|-------------|---------------------------|----------------|
| NFL | ~267 | ~2,400 | ~9 |
| NBA | ~1,230 | ~2,400 | ~2 |
| MLB | ~2,430 | ~2,400 | ~1 |
| NHL | ~1,312 | ~2,400 | ~2 |
| UFC | ~500/year | ~2,400 | ~5 |
| CBB | ~5,000+ | ~2,400 | <1 |
| Soccer (top 5 leagues) | ~1,800 | ~2,400 | ~1.5 |

**Key insight:** NFL has the SMALLEST sample per season. Claiming a profitable NFL system from 1-2 seasons is almost always noise.

### Robustness Checks
- [ ] Positive ROI after removing top 3 best bets (not dependent on outliers)
- [ ] Consistent across 3+ non-overlapping time periods
- [ ] Profitable with slightly different parameters (±10% on key coefficients)
- [ ] Positive CLV in out-of-sample period
- [ ] Feature count < N/20 (overfitting guard)
- [ ] Edge > vig (need > 52.4% at standard -110)
- [ ] Mechanism is explainable in plain English

### Kelly Criterion for Bet Sizing
```
f* = (b × p - q) / b
```
Where: f* = fraction of bankroll, b = decimal odds - 1, p = win probability, q = 1 - p.

**In practice: use ¼ to ½ Kelly.** Full Kelly causes extreme volatility. Never risk > 3% of bankroll per bet.

---

## 4. CLV & Edge Quantification Protocol

### For Every Bet, Track:
1. Timestamp of bet placement
2. Odds at placement (your price)
3. Book used
4. Closing odds at Pinnacle/sharp book
5. Result

### Edge Calculation:
```
no_vig_prob = remove vig from market odds (use Pinnacle for sharpest line)
model_prob = your model's probability
edge = model_prob - no_vig_prob
```
Only bet when `edge > threshold` (typically 3-5% depending on sport/market liquidity).

### No-Vig Probability Conversion:
```
For American odds:
  Positive: implied_prob = 100 / (odds + 100)
  Negative: implied_prob = abs(odds) / (abs(odds) + 100)

Remove vig (2-side market):
  no_vig_A = implied_A / (implied_A + implied_B)
  no_vig_B = implied_B / (implied_A + implied_B)
```

### Rolling CLV Dashboard:
Track 50-bet and 200-bet rolling CLV. If rolling CLV turns negative for 200+ bets, the model has lost its edge — stop betting and investigate.

---

## 5. Idea-to-Backtest Pipeline

```
HYPOTHESIS → FEATURE → BACKTEST → VALIDATE → SHIP or KILL
```

### Stage 1: Hypothesis
"I believe [X] creates edge because [real-world mechanism]. I expect [Y% improvement] because [Z]."

### Stage 2: Feature Engineering
Build the feature that captures the hypothesis. Must be calculable with data available BEFORE the event (walk-forward compliant).

### Stage 3: Walk-Forward Backtest
- Expanding window with point-in-time stats only
- Record simulated bet odds (from cached historical odds data)
- Measure: ROI, hit rate, CLV, max drawdown

### Stage 4: Statistical Validation
- Run z-test against breakeven
- Check robustness across time periods
- Verify CLV is positive
- Confirm feature count discipline

### Stage 5: Decision
- **SHIP** if: z > 1.96, positive CLV, robust across periods, explainable mechanism
- **KILL** if: z < 1.5, negative CLV, inconsistent, or no mechanism
- **INCUBATE** if: promising but insufficient sample — mark for monitoring

---

## 6. Sport-Specific Knowledge Banks

### NFL
**Model type:** Logistic regression or Elo. XGBoost for props.
**Top features:** DVOA/EPA, O-line pressure rate, QB CPOE, weather (wind >15mph kills passing), rest days, travel distance, divisional familiarity.
**Known edges:** Home dogs +3 to +7 (~54% ATS), bye week advantage, post-blowout fading, wind unders, short road favorites (-1 to -3) historically poor.
**Trap:** Smallest sample per season of any major sport. 9 seasons needed for significance. Most "NFL systems" are noise.
**Data:** nflfastR (play-by-play), Pro Football Reference, NFLweather.com.

### NBA
**Model type:** Regression on efficiency metrics. Elo for baseline.
**Top features:** Off/def efficiency (pts/100 possessions), pace, B2B status (-3-5% win prob), rest advantage (3+ days vs 0), travel/timezone crossing, injury-adjusted lineup net rating.
**Known edges:** B2B fatigue (especially 2nd of road B2B), rest mismatch 3+ vs 0, home underdogs +4 to +8 (~53% ATS), schedule spots (look-ahead/letdown).
**Trap:** Load management makes injury data critical. Starters sitting but technically "active."
**Data:** nba_api (Python), Basketball Reference, NBA referee stats (NBAref.com).

### MLB
**Model type:** Pitcher-centric regression or Bayesian. Poisson for run totals.
**Top features:** Starting pitcher (FIP, xFIP, SIERA, K-BB%), bullpen availability/fatigue (5+ relievers yesterday), platoon splits (L/R lineup), park factors, umpire tendencies, catcher framing.
**Known edges:** Bullpen fatigue, park factor exploitation (Coors inflates 20-30%), umpire over/under tendencies, run line value (-1.5 favorites vs ML).
**Trap:** Starting pitcher is so dominant that model without it is worthless. Day games after night games affect performance.
**Data:** FanGraphs, Baseball Reference, UmpScorecard.com, park factors database.

### NHL
**Model type:** Poisson or Dixon-Coles for goals. xG models for shot quality.
**Top features:** xG (expected goals from shot quality/location), Corsi/Fenwick (shot attempts), goalie save% and workload, PP/PK efficiency, B2B and travel, score effects (trailing teams press).
**Known edges:** Home ice after 4+ game road trip, B2B goalie starts (measurably worse save%), goalie confirmation timing, puck line +1.5 underdogs (48%+ decided by 1 goal/OT), West-to-East travel.
**Trap:** Goalie performance is the most volatile variable. One hot/cold goalie can dominate results.
**Data:** Hockey Reference, Natural Stat Trick, MoneyPuck (xG), Evolving Hockey.

### UFC
**Model type:** Bayesian (small samples per fighter) + Elo. Feature engineering critical.
**Top features:** Reach differential (strongest single predictor), striking accuracy × volume, TD accuracy vs opponent TD defense, fighter age (35+ decline), activity level (12+ month layoff = ring rust), significant strikes absorbed/minute, style matchup (striker vs grappler).
**Known edges:** Reach advantage 3+ inches, age decline (market underweights for veterans with name value), short-notice replacements (cover as underdogs), heavyweight volatility (one-punch KOs), southpaw advantage vs orthodox.
**Trap:** Small sample per fighter (10-30 fights). Fighter evolution between fights is real — 3-year-old stats may not reflect current ability. Weight class differences matter enormously.
**Data:** UFCStats.com, BestFightOdds (historical odds), Tapology (fight finder).

### Soccer
**Model type:** Dixon-Coles (Poisson variant) or xG-based regression.
**Top features:** xG (shot quality, dominant predictor), shots on target, pressing intensity (PPDA), fixture congestion (midweek European games), referee tendencies, home/away form split.
**Known edges:** Draw is most undervalued outcome, home underdogs at +200+ (long-term +ROI), fixture congestion from Champions/Europa League, new manager bounce (3-5 games), xG-results divergence regression.
**Trap:** League-specific dynamics. What works in EPL may not in Bundesliga. Promotion/relegation creates motivation asymmetry. Cup competitions change rotation patterns.
**Data:** FBref.com (StatsBomb xG), Transfermarkt, Understat, WhoScored.

### Tennis
**Model type:** Surface-specific Elo (hard, clay, grass separately).
**Top features:** Surface-specific win rate (can differ by 100+ Elo points), serve stats (1st serve %, aces/DFs), return points won, fatigue (matches in last 14/30 days), tournament round, court speed.
**Known edges:** Surface Elo vs overall Elo divergence, first-set winner wins match ~80%, fatigue in back-to-back tournaments, H2H overreaction (market overweights tiny H2H samples).
**Trap:** Retirement/walkover risk (player pulls out mid-match). Motivation varies wildly by tournament importance. Surface transitions (clay → grass) cause form disruptions.
**Data:** Tennis Abstract, Jeff Sackmann's GitHub datasets, ATP/WTA official stats.

### College Basketball (CBB) / College Football (CFB)
**Model type:** Regression on adjusted efficiency (KenPom-style). Elo for baseline.
**Top features (CBB):** Adjusted offensive/defensive efficiency, tempo, SOS, roster continuity, transfer portal impact, coaching tenure, free throw rate.
**Top features (CFB):** SP+ or FEI, recruiting rankings, returning production %, QB experience, home field (worth more than NFL).
**Known edges:** Conference tournament value (auto-bid pressure), early-season tournament neutral-site games, look-ahead spots before rivalry games, coaching changes.
**Trap:** Massive roster turnover via transfer portal. Last season's data may not reflect current roster. Small conference data is sparse and noisy.
**Data:** KenPom.com (paid), Barttorvik.com (free), Sports Reference.

---

## 7. Model Architecture Decision Tree

```
Is sample size large (>5000 games)?
  YES → Gradient boosting (XGBoost) with aggressive regularization
  NO  → Is it a goals/runs sport?
          YES → Poisson / Dixon-Coles
          NO  → Is per-player sample tiny (<30 observations)?
                  YES → Bayesian with informative priors
                  NO  → Logistic regression or Elo

All models: walk-forward validation, L1/L2 regularization, feature count < N/20
```

**The research is clear: simple models (Elo, logistic regression, Poisson) consistently match or beat complex models with far less overfitting risk.** Only escalate complexity when you have massive data AND clear evidence the simple model is leaving edge on the table.

---

## 8. When This Skill Fires

### Brainstorming Mode
User says: "What edges exist in [sport]?" or "Brainstorm systems for [sport]"
→ Pull from the relevant sport knowledge bank. Generate 5-10 ranked hypotheses with mechanisms. Identify which are testable with available data.

### Evaluation Mode
User says: "Is this system real?" or "Validate this edge"
→ Run the validation framework. Check sample size, z-test, CLV, robustness, mechanism.

### Design Mode
User says: "Build a model for [sport]" or "What features should we use?"
→ Use the model architecture decision tree. Recommend features from the sport bank. Propose the idea-to-backtest pipeline.

### Contrarian Mode
User says: "Where is the public wrong?" or "Sharp logic for [event]"
→ Apply the contrarian framework. Identify public biases relevant to the event. Check for RLM, overreaction, or structural inefficiency.

## Rules

1. **Every hypothesis must have a mechanism** — "it works because statistics" is not a mechanism
2. **Sample size before celebration** — check sport-specific minimums before calling anything profitable
3. **CLV > win rate** — always. A winning system with negative CLV is lucky, not skilled
4. **Simple first** — Elo/regression before XGBoost before neural nets. Complexity earns its place
5. **Known edges shrink** — if it's published in mainstream betting content, assume reduced edge
6. **Sport-specific context always** — never give generic advice. Every recommendation must account for the specific sport's dynamics, data availability, and sample constraints
7. **Complements, doesn't replace** — this skill provides knowledge. `backtest` runs tests. `profit-driven-development` guards against overfitting. Use them together.
