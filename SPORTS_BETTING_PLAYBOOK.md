# The Definitive Sports Betting Model Playbook
## Extracted from 3 Production Systems: UFC (MMALogic), MLB+NHL (Diamond Predictions), NBA+NCAA (Courtside AI)
### Nick Householder — April 2026

> This playbook distills everything learned from building and operating 3 profitable sports betting algorithms across 5 sports (UFC, MLB, NHL, NBA, NCAA basketball) over 159+ development sessions, 527 commits, and thousands of real-money picks. Every principle is backed by walk-forward validated evidence, not theory.

---

# PART 1: UNIVERSAL PRINCIPLES (Apply to Any Sport)

## 1.1 The Market Is Mostly Right — Your Job Is Finding Small Mispricings

**The #1 mistake new model builders make:** Thinking they can build a model that "knows better" than Vegas. They can't. The market incorporates millions of data points from sharp bettors, injury reports, weather, public sentiment, and proprietary algorithms.

**What works instead:** Anchor to the market, then find small edges.

**Evidence from production systems:**
- Diamond Predictions NHL: Model weight = **16.5%**, market weight = **83.5%** (Benter anchoring)
- Diamond Predictions MLB: Model weight = **20.8%**, market weight = **79.2%**
- Courtside AI NCAA: Uses Vegas spread AS the primary input, model provides edge OVER the line

**The Benter Principle:** Bill Benter's horse racing system (the most profitable gambling algorithm in history) used ~17% model weight. Your model should ADJUST the market price, not replace it.

**Implementation:**
```
final_prob = (market_weight × market_prob) + (model_weight × model_prob)
edge = final_prob - market_prob
```

**Where model_weight ranges from 0.15 to 0.25 depending on sport and season phase.**

---

## 1.2 Walk-Forward Validation Is Non-Negotiable

**What it is:** Train on past data, test on future data, never the reverse. The test set must be STRICTLY chronological — no peeking.

**How all 3 systems implement it:**

| System | Train | Purge | Test | Folds |
|--------|-------|-------|------|-------|
| Diamond NHL | Season N | 14 days | Season N+1 | 3 folds (2022→2025) |
| Diamond MLB | Season N | 14 days | Season N+1 | 3 folds (2023→2026) |
| Courtside NCAA | Seasons 22-23 | — | Season 24-25 | 3 seasons expanding |
| Courtside NBA | 3 seasons | — | Current season | 3 seasons |

**The 14-day purge (Diamond):** After training ends, skip 14 days before testing begins. This prevents stats computed from late-training games from leaking into early-test games.

**Point-in-time enforcement:** Every stat used for a prediction must be computed using ONLY data available BEFORE that game. If a fighter/team's stats update after a game, the backtest must use the pre-game version.

**What happens without it:**
- Courtside AI's Elo-Signal model: Claimed 60.4% ATS during optimization → actual walk-forward showed **50.0% ATS** (break-even). The optimizer was testing the wrong model's data.
- MMALogic: Career stats leakage inflated P/L by +10.44u across 3 events. Post-fight stats were being used for pre-fight predictions.

**Rule: If your backtest shows 80%+ accuracy, it's wrong. Real edges in sports betting are 2-8% above the market.**

---

## 1.3 Agreement Between Independent Models Is the Best Confidence Signal

**The breakthrough:** Don't build one big model. Build 3-4 independent models that see different data. When they AGREE, confidence is high. When they disagree, back off.

**Diamond Predictions (4-layer architecture):**
1. **WinProb** — probability model (20 features, market-anchored)
2. **StatModel** — directional filter (features as gates, not weights)
3. **Opponent-Adjusted** — schedule-adjusted team quality
4. **Systems** — rule-based situational patterns

When all 4 agree → DIAMOND tier (3x Kelly). When 1 agrees → PLATINUM (2x). When none agree → GOLD (1x, or skip in v13.6).

**Courtside AI (multi-family scoring):**
- 12+ scoring "families" (CHALK_ELO_OE, DE_NETRTG_CONVERGE, etc.)
- Score = sum of family weights when conditions fire
- Higher score = more families agree = more confidence

**Critical rule: Agreement scales SIZING, never DIRECTION.**

The anchor model (WinProb for Diamond, ML model for Courtside) determines WHICH team to bet. Agreement determines HOW MUCH to bet. This prevents blending from destroying profitable contrarian signals.

**Diamond Predictions proof:**
- DIAMOND tier (max agreement): 27.6% ROI, 42.6% WR
- PLATINUM tier (moderate agreement): **36.0% ROI**, 48.1% WR
- The MIDDLE tier outperforms! Maximum agreement often means the edge is already priced in.

This led to the **SKIP_DIAMOND** rule: Skip the highest-agreement picks (+8.5pp ROI improvement).

---

## 1.4 The "4+ Systems Trap" — When Everyone Agrees, the Edge Is Gone

**Discovery from Diamond Predictions:** When 4+ rule-based systems unanimously agree on a pick, the historical ROI is **-33.8%**. These are "obvious" spots that the market has already priced in.

**Why it happens:** Situational betting systems identify patterns the market knows about. 1-2 systems firing = edge the market underprices. 4+ systems = the market sees it too, and the line is already adjusted.

**Courtside AI's version:** NCAA MADNESS tier (postseason picks) claimed 69.2% ATS from cherry-picked data. 3-season walk-forward showed **37-43% ATS**. Obvious playoff narratives are already in the line.

**Universal rule: Moderate-confidence picks with 1-2 edge sources outperform high-confidence picks with 5+ edge sources. The sweet spot is agreement from 1-2 independent models, not unanimous consensus.**

---

## 1.5 Features as Gates, Not Weights — The Zero-Weight Architecture

**The most counterintuitive breakthrough:** Setting feature weights to zero can IMPROVE your model.

**Diamond Predictions discovery:** The StatModel layer has 19 features, ALL with weight = 0. Features don't adjust probability — they validate directional agreement. Each feature acts as a binary agree/disagree gate.

**Impact:** ~2x ROI improvement vs. traditional feature-weighted architecture. Reduced 39 optimized parameters to 19 effective parameters by zeroing noisy weights.

**Why it works:** In sports betting, the market already prices in most features. Adding feature weights on top of market probability introduces noise and overfitting. Using features as directional gates captures the information ("does this stat agree with the pick?") without introducing parameter risk.

**Which features to zero:**
- Recent form (market already prices streaks)
- Pythagorean win % (redundant with actual record)
- Strength of schedule (already in the line)
- Back-to-back (already in the line, but the MAGNITUDE is underpriced — keep as continuous feature)

**Which features to keep non-zero:**
- Process metrics (xG, Corsi, expected goals) — markets underweight process vs. results
- Opponent-adjusted stats — markets use raw stats, not schedule-adjusted
- Contrarian signals (see next section)

---

## 1.6 Contrarian Feature Discovery — Markets Overvalue These Things

**The CMA-ES optimizer (Diamond Predictions v9) discovered that the most profitable features have NEGATIVE weights — they fade what the market overvalues.**

**Top contrarian signals (NHL):**
| Feature | Weight | What It Means |
|---------|--------|---------------|
| special_teams_delta | **-0.912** | Markets MASSIVELY overvalue power play %. Fade teams with high PP%. |
| oa_momentum_delta | **-0.590** | Streaks are noise. Markets overreact to winning/losing runs. Fade hot teams. |
| b2b_fatigue_delta | **-0.426** | Back-to-back is 3× more impactful than traditional wisdom. Markets underestimate fatigue. |
| oa_defense_delta | **-0.353** | Good defense reputation is already in the line. Fade "elite defense" narrative. |

**Courtside AI confirmation:**
- P(cover) v3's strongest feature: `dog_x_spread` at **-0.358** weight. Underdogs in close games cover far more than the market expects.
- Rest differential: Teams with 3+ days rest = 69.2% ATS vs. B2B = 59.1%. A 10-point gap the market underprices.
- NCAA spread gate reversal: Close games (spread 0-5) with high ML edge = **70% ATS**. The market treats close games as coin flips, but the model finds signal.

**Universal contrarian principle:** If the public can see it on a TV broadcast graphic, the market has already priced it. The edge comes from:
1. Process metrics the public doesn't track (xG, Corsi, opponent-adjusted stats)
2. Fading narratives the public overweights (streaks, special teams, postseason storylines)
3. Physical/scheduling factors the market underestimates (rest, travel, back-to-back)

---

## 1.7 Kelly Criterion for Bet Sizing — But With Hard Caps

**Kelly Criterion formula:**
```
kelly_fraction = (model_prob × (decimal_odds - 1) - (1 - model_prob)) / (decimal_odds - 1)
```

**But full Kelly is too aggressive.** All 3 systems use fractional Kelly:

| System | Kelly Base | Kelly Cap | Agreement Scaling |
|--------|-----------|-----------|-------------------|
| Diamond NHL | 0.410 | **0.029** (2.9%) | 2.499^n_agree |
| Diamond MLB | Similar | Similar | Monthly: 0.23× (Mar) to 1.49× (Jul) |
| Courtside | Flat unit | — | Tier-based (1×, 2×, 3×) |
| UFC | Real odds payout | — | Confidence-tiered |

**The 2.9% hard cap (Diamond):** No single bet exceeds 2.9% of bankroll, regardless of model confidence. This prevents ruin from the inevitable model miscalibration.

**Monthly Kelly scaling (Diamond MLB):** March = 0.23× Kelly (spring training carryover makes early-season predictions unreliable). July = 1.49× Kelly (peak signal reliability mid-season).

**Why this matters:** A model with 55% win rate at -110 odds needs ~2,000 bets to be confident it's profitable. Overbetting early (before you have enough data) can wipe out the bankroll before the edge materializes.

---

## 1.8 Situational Betting Systems — Rule-Based Edge Stacking

**What they are:** Named conditions (like "PICK_EM_SPECIAL" or "POSSESSION_UNDERDOG") that fire when specific game-state criteria are met. Each system has a walk-forward validated ATS% and ROI.

**Diamond Predictions (38+ NHL systems, 54 MLB):**
- Scored by grade (S+ to F) + ROI weight
- Threshold: 2.25 combined score to fire
- Lifecycle management: NEW → ACTIVE → DEGRADED → PRUNED

**Courtside AI (10 NCAA systems):**
- PICK_EM_SPECIAL: Spread ≤ 2, Edge ≥ 7 → **70.5% ATS** (N=149)
- CLOSE_GAME_FAVORITE: Edge ≥ 7, Spread < 5, is_fav → **67.5% ATS** (N=126)
- NEUTRAL_SITE_HIGH_EDGE: Neutral site, Edge ≥ 8 → **70.9% ATS** (N=79)

**Implementation pattern (universal):**
```python
fired = []
if abs_spread <= 2 and edge >= 7:
    fired.append("PICK_EM_SPECIAL")
if edge >= 7 and abs_spread < 5 and is_fav:
    fired.append("CLOSE_GAME_FAVORITE")
# ... more systems ...

total_score = sum(grades[sys]["weight"] for sys in fired)
qualifies = total_score >= THRESHOLD
```

**Key rules:**
1. Every system must be walk-forward validated (not just backtested)
2. Minimum sample size: N≥50 for basketball, N≥100 for baseball/hockey
3. Systems should be graded and pruned automatically based on live performance
4. When 4+ systems agree → SKIP (the "too obvious" trap)

---

## 1.9 Edge Capping — Don't Trust Extreme Confidence

**Discovery (Diamond Predictions v13.6):** Live 2025-26 data showed 2 bets with >10% edge — both were losses. The model was miscalibrated at the extremes.

**Fix:** CONG_MAX_EDGE = 0.10. Any pick with edge > 10% is capped or skipped.

**Impact:** +12.1pp ROI improvement, +2.3pp win rate.

**Courtside AI confirmation:** Edge magnitude is monotonically positive (higher edge = better ATS) up to a point, but extreme edges (>10 points in basketball) often indicate stale lines or data errors, not genuine opportunity.

**Universal rule:** If your model says you have a 15%+ edge over the market, you're probably wrong. The market is efficient enough that true edges are 2-8%. Anything beyond that is likely model error, data lag, or overfitting.

**Implementation:**
```python
if edge > MAX_EDGE_THRESHOLD:
    skip_pick()  # or cap edge at threshold
```

---

## 1.10 The Small Sample Problem — Your Biggest Enemy

**Every wrong conclusion in these systems came from small samples:**

| System | Wrong Conclusion | Sample | Correct Answer | Sample |
|--------|-----------------|--------|----------------|--------|
| Courtside | model_spread≥10 is bad (48.6% ATS) | N=74 | model_spread≥10 is good (52.0% ATS) | N=8,741 |
| Courtside | Score-ATS correlation is negative (r=-0.191) | N=50 | Correlation is positive (r=+0.167) | N=392 |
| Courtside | MADNESS tier = 69.2% ATS | Cherry-picked | MADNESS = 37-43% ATS | 3 seasons |
| Diamond | AGREE_TIER=8 looks great | N=7 | Violated sample filter | Skipped |

**Minimum sample sizes by sport:**
- UFC/MMA: 70+ events (minimum for backtest validity)
- NHL/MLB: 3 full seasons (minimum for walk-forward)
- NBA/NCAA: 3 full seasons, 200+ test picks
- Any system/filter: N≥50 minimum before acting on it

**Statistical significance tests:**
- Bootstrap 95% CI (Diamond): 10,000 resamples to verify ROI stability
- p-value requirement: p < 0.05 for any parameter change
- Cohen's h > 0.2 for effect size (anti-overfitting)

**Rule: If you can't test it on 200+ games, don't ship it.**

---

## 1.11 Overfitting Is the Silent Killer

**Parameters-to-picks ratio:**
- Diamond NHL v9: 39 parameters / 300 picks = **1:8 ratio** (dangerous, recommended 1:50+)
- Diamond NHL v13.6: 41 parameters / 926 picks = **1:23 ratio** (improving)
- Courtside NCAA: P(cover) v3 has 35 features / 614 picks = 1:18 (acceptable for logistic regression)

**Signs of overfitting:**
1. Backtest accuracy > 65% on moneyline bets (suspicious)
2. First fold ROI >> last fold ROI (signal degrading over time)
3. Parameter changes produce identical results (feature has no effect)
4. A minor tweak produces 5%+ accuracy jump (noise, not signal)

**Diamond Predictions fold degradation (NHL):**
- Fold 1 (2023): 52.6% ROI
- Fold 2 (2024): 34.0% ROI
- Fold 3 (2025): 17.9% ROI

This is EXPECTED and healthy — it means the model isn't overfitting to recent data. But it also means you should expect future ROI to be closer to Fold 3 than Fold 1.

**Anti-overfitting strategies used across all 3 systems:**
1. Walk-forward expanding window (never retraining on test data)
2. Zero-weight noisy features (reduce parameter count)
3. Hard Kelly cap (limits damage from miscalibration)
4. Bootstrap confidence intervals (verify stability)
5. Monthly/seasonal scaling (acknowledge signal quality changes)
6. Automatic pruning of underperforming systems

---

# PART 2: SPORT-SPECIFIC FINDINGS

## 2.1 UFC/MMA (MMALogic / OctagonAI v11.22.2)

**Architecture:** Multi-factor matchup scoring with 61+ tunable parameters, optimized via 2-pass Differential Evolution with 3-fold time-series cross-validation.

**Current Performance (71 events, 550 fights):**

| Bet Type | Record | P/L | ROI | Accuracy |
|----------|--------|-----|-----|----------|
| Moneyline | 378W-146L | +118.11u | 22.5% | 72.1% |
| Method | 152W-164L | +159.77u | 50.6% | 48.1% |
| Combo (KO R1) | 30W-60L | +87.76u | 97.5% | 33.3% |
| Over/Under | 339W-121L | +174.46u | 37.9% | 73.7% |
| Parlays | 49W-15L | +239.42u | — | — |
| **TOTAL** | **~950+ bets** | **+779.52u** | **56.1%** | — |

**What Makes It Work:**

1. **KD-Adjusted Strike Ratio** — Knockdowns weighted 16.6× base strike value. Captures dominance beyond volume. Central to 72.1% ML accuracy.

2. **Opponent-of-Opponent (OoO) Quality Scaling** — Multi-layer adjustment: fight quality × 4-foe schedule. OOO_BLEND = 0.91. Prevents stat inflation vs. weak opponents.

3. **Style-Specific Matchup Binary** — Strict grappler-vs-striker classifier (not a continuous slider). +8.24u on 71 events. Grappler: TDAvg>3.0 AND (SUB%+DEC%>40%). Striker: SLpM>4.0 AND (KO%+DEC%>50%).

4. **SUB→DEC Fallback** — The most important betting rule. SUB accuracy is only 36%, but elite grapplers win by DEC 55%. When model predicts SUB, bet DEC instead. +25.87u on 48 fights.

5. **Method Bets as a Portfolio** — 48.1% accuracy looks bad, but method bets are a PORTFOLIO. Low-accuracy KO/DEC props at +300-800 odds fund the system. Never gate odds ranges — the DEC odds gate (-125 to +250) caused -91.95u regression by killing the profitable longshot tail.

6. **ROI3 Parlays** — 3-leg value parlays: 34.2% WR but +400-800 odds → **293.8% ROI** (+111.66u). The insight: underdog correlation + high-payout parlays = outsized returns.

7. **Over/Under from Finish Rate** — Derived from avg_dec (decision tendency metric). Under if avg_dec < 0.45 for DEC-type fighters, < 0.35 for KO/SUB fighters. 73.7% accuracy, nearly matching ML.

8. **18 Situational Betting Systems** — Statistically gated (p<0.05 only). 62.4% WR, +166.43u. Top: PROP_METHOD_dec_confident (64.4% accuracy), BET_bounce_back, BET_underdog_high_diff.

9. **Heavy Favorite KO Boost** — When favorites ≥ -400 have KO signal ≥ 0.30, boost KO method prediction. Massive favorites often destroy weaker opponents by KO.

10. **Flat 1u Betting** — No Kelly, no variable sizing. Every bet is 1 unit. Kelly fraction = 0.0. The simplicity prevents overbetting on miscalibrated picks.

**Key Constants:**
- PICK_DIFF_THRESHOLD: 0.142799 (minimum score differential)
- FAV_DISCOUNT: 0.148239 (favorites get slightly fewer picks)
- RECENCY_DECAY: 0.885234 (most recent fights weighted highest)
- AGE_THRESHOLD: 36.57 (penalties start)
- REACH_THRESHOLD: 4.25 inches (bonus activates)
- SUB_GATE_THRESHOLD: 1.0 (fully gate SUB bets)
- DEC_METHOD_ODDS_FLOOR: -125 (skip heavy-juice DEC)

**Top Discoveries:**
- Knockdowns are 16.6× more predictive than regular strikes
- Takedown defense coefficient = 0.0 (noise — the optimizer eliminated it)
- Head-specific accuracy weight = 0.016 (near-zero — body striking dominates)
- Weight-class method priors = 0.012 (near-zero — individual stats beat class averages)
- Women's adjustments: ALL tested variants were net-negative on N=73 bouts. Disabled entirely.

**What Doesn't Work in UFC:**
- Variable bet sizing (Kelly)
- Continuous broad modifiers (hurt more than help)
- Selective SUB gating for elite grapplers (+0.00u — blanket gate is better)
- Standalone SApM coefficient (double-counts existing signals)
- Standalone round bets (disabled)
- Markov Chain fight simulation (60% accuracy vs 75.4% algo accuracy)

---

## 2.2 MLB + NHL (Diamond Predictions)

**Architecture:** 4-layer Conglomerate (WinProb + StatModel + OA + Systems)

**Current Performance:**
- **NHL:** 34.2% ROI (926 picks), 46.9% WR, Sharpe 0.223
- **MLB:** 56.1% ROI (469 picks), 47.6% WR, Sharpe 0.321
- **Combined:** +579.5 units

**What Makes It Work:**
1. **Benter anchoring** — market gets 83.5% weight, model gets 16.5%
2. **Zero-weight filter architecture** — features as gates, not probability adjusters
3. **Contrarian features** — special teams (-0.912), momentum (-0.590) are FADED
4. **Agreement-as-confidence** — scales Kelly sizing, never pick direction
5. **Edge capping** — picks >10% edge are skipped (model miscalibration)
6. **Monthly Kelly scaling** — March 0.23×, July 1.49× for MLB
7. **SKIP_DIAMOND** — highest agreement tier underperforms middle tier

**Top Discoveries:**
- Defense is the #1 predictor in NHL (team_gapg_delta = 0.835)
- Markets massively overvalue special teams (weight = -0.912)
- Recent form/momentum is already priced in (weight near zero)
- B2B fatigue is 3× more impactful than conventional wisdom
- Process beats results: xG offense (0.789) > actual offense (-0.241)

**Key Constants (NHL v10):**
- WP_MODEL_WEIGHT: 0.165
- WP_MARKET_WEIGHT: 0.835
- MIN_EDGE: 0.017
- KELLY_CAP: 0.029
- CONG_MAX_EDGE: 0.10
- DISAGREE_PENALTY: 0.229 (2× stronger than AGREE_BOOST: 0.047)

---

## 2.3 NBA + NCAA Basketball (Courtside AI)

**Architecture:** Multi-family scoring (NBA) + ML pipeline with XGBoost + P(cover) v3 (NCAA)

**Current Performance:**
- **NCAA:** 64.5% ATS, +23.1% ROI (N=614, 3 seasons walk-forward)
- **NBA:** 61.4% ATS, +17.2% ROI (N=285, 3 seasons)
- **NCAA test season (2024-25):** 61.6% ATS, +17.6% ROI (N=203)
- **NBA test season (2024-25):** 63.2% ATS, +20.7% ROI (N=117)

**What Makes It Work:**
1. **Spread gate reversal** — close games (spread 0-5) with high ML edge = 70% ATS. Market treats these as coin flips.
2. **P(cover) v3** — 35-feature logistic regression. `dog_x_spread` (-0.358) is the dominant feature: underdogs in close games cover.
3. **10 named situational systems** — PICK_EM_SPECIAL (70.5% ATS), NEUTRAL_SITE_HIGH_EDGE (70.9% ATS)
4. **Elo-Signal killed** — proven 50% ATS on 2,121 games. Sometimes the best move is removing a model.
5. **Rest filter** — 3+ days rest = 69.2% ATS vs B2B = 59.1% (NBA). 10-point gap.
6. **NBA spread sweet spot** — only bet spreads 5-11. Close games (1-4) are coin flips, blowouts (11+) are unprofitable.

**Key NCAA Systems (by ATS%):**
| System | ATS% | N | Condition |
|--------|------|---|-----------|
| NEUTRAL_SITE_HIGH_EDGE | 70.9% | 79 | Neutral site + edge ≥ 8 |
| PICK_EM_SPECIAL | 70.5% | 149 | Spread ≤ 2 + edge ≥ 7 |
| CLOSE_GAME_FAVORITE | 67.5% | 126 | Edge ≥ 7 + spread < 5 + favorite |
| CLOSE_GAME_DOG | 66.2% | 397 | Edge ≥ 7 + spread < 5 + underdog |

**Key Architecture Decision:** NCAA and NBA share the situational systems concept but have DIFFERENT models:
- NCAA: XGBoost + logistic P(cover) → systems are a scoring overlay
- NBA: Multi-family chalk-signal → 12 scoring families vote on picks
- The MLB systems architecture was ported to NCAA successfully

---

# PART 3: THE UNIVERSAL MODEL-BUILDING PLAYBOOK

## Step 1: Gather 3+ Seasons of Historical Data

**Minimum data requirements:**
- Game results (score, spread result for ATS)
- Pre-game odds (moneyline AND/OR spread from a real sportsbook)
- Team/player stats available BEFORE each game (point-in-time)
- Injuries, rest days, travel (if available)

**Where to get it:**
- ESPN API (free, game scores and schedules)
- DraftKings/FanDuel historical odds (scrape or subscribe)
- UFCStats.com (MMA), Hockey-Reference, Baseball-Reference, KenPom (NCAA)
- Action Network (sharp money signals, handle %)

**Critical: You MUST have real odds.** Estimated odds or flat -110 assumptions will give you false P/L. Real odds from real sportsbooks, de-vigged to remove vig.

---

## Step 2: Build the Market-Anchored Probability Model

**Architecture:** Logistic regression or XGBoost, anchored to market probability.

```python
# Step 1: Convert odds to de-vigged market probability
market_prob = devig(home_odds, away_odds)

# Step 2: Build feature vector (10-20 features max)
features = [
    offense_metric_delta,   # Your team's strength - opponent's
    defense_metric_delta,   # Defense differential
    process_metric_delta,   # xG, Corsi, expected efficiency
    schedule_factor,        # Rest, travel, B2B
    opponent_adjusted,      # Stats adjusted for opponent quality
]

# Step 3: Model predicts probability
model_prob = model.predict_proba(features)

# Step 4: Blend with market (Benter anchoring)
final_prob = (0.80 * market_prob) + (0.20 * model_prob)

# Step 5: Compute edge
edge = final_prob - market_prob
```

**Feature selection principles:**
1. Use DELTAS (team_A - team_B), not raw stats
2. Prefer process metrics over results (xG > goals scored)
3. Include schedule/rest factors (universally underpriced)
4. Keep to 10-20 features max (more = overfitting)
5. Zero out features that don't improve walk-forward ROI

---

## Step 3: Add Independent Validation Layers

**Build 2-3 additional models that see different data:**

1. **Statistical filter** — Do the traditional stats agree with the pick direction?
2. **Opponent-adjusted model** — When you adjust stats for schedule strength, does the pick still hold?
3. **Situational systems** — Do named rule-based patterns support the pick?

**Score agreement:**
```python
n_agree = sum([stat_agrees, oa_agrees, systems_agree])
tier = {0: "SKIP", 1: "LOW", 2: "MEDIUM", 3: "HIGH"}[n_agree]
kelly_mult = {0: 0, 1: 1.0, 2: 2.0, 3: 2.5}[n_agree]  # But check for 4+ systems trap!
```

---

## Step 4: Walk-Forward Validate Everything

```python
for fold in range(n_folds):
    train = data[data.date < cutoff_dates[fold]]
    test = data[(data.date >= cutoff_dates[fold]) & (data.date < cutoff_dates[fold + 1])]

    model.fit(train)
    predictions = model.predict(test)

    roi = compute_roi(predictions, test.actual_results, test.odds)
    wr = compute_win_rate(predictions, test.actual_results)

    # Track per-fold performance
    results.append({"fold": fold, "roi": roi, "wr": wr, "n_picks": len(predictions)})

# Aggregate
total_roi = weighted_mean(results)
bootstrap_ci = bootstrap_95(all_picks, n_resamples=10000)
```

**Red flags in walk-forward results:**
- Fold 1 ROI is 3× Fold 3 ROI → overfitting to early data
- Any fold is negative → model may not be profitable long-term
- Win rate > 60% on moneyline → suspicious, verify data integrity
- Fewer than 100 picks per fold → insufficient sample

---

## Step 5: Build Situational Systems

**For each sport, identify 10-20 game-state conditions that historically produce edge:**

1. Start with simple conditions: "underdog + rest advantage + close spread"
2. Backtest each condition independently (walk-forward)
3. Require minimum N=50 picks and p<0.05
4. Grade each system: A+ (>25% ROI), A (15-25%), B (10-15%), C (5-10%), F (<5%)
5. Weight by grade in the scoring function
6. Implement lifecycle: NEW → ACTIVE → DEGRADED → PRUNED

**Discovery process (from Courtside AI):**
```python
# Test 16 candidate conditions
for system in candidate_systems:
    train_results = backtest(system, train_data)
    val_results = backtest(system, val_data)
    test_results = backtest(system, test_data)

    if val_results.ats > 55% and test_results.ats > 55%:
        system.status = "ACTIVE"
        system.grade = assign_grade(test_results.roi)
    else:
        system.status = "PRUNED"
```

---

## Step 6: Implement Bet Sizing with Kelly Criterion

```python
def size_bet(model_prob, odds, n_agree, month=None):
    decimal_odds = american_to_decimal(odds)
    full_kelly = (model_prob * (decimal_odds - 1) - (1 - model_prob)) / (decimal_odds - 1)

    # Fractional Kelly (40% of full)
    kelly_fraction = full_kelly * 0.41

    # Agreement scaling
    kelly_mult = min(kelly_base * (agree_scale ** n_agree), 1.0)

    # Monthly adjustment (if applicable)
    if month:
        kelly_mult *= month_scale.get(month, 1.0)

    # Hard cap
    bet_size = min(kelly_fraction * kelly_mult, MAX_BET)

    return bet_size if bet_size > 0 else 0  # Never bet negative EV
```

---

## Step 7: Deploy, Monitor, and Self-Correct

**Daily pipeline (all 3 systems use this pattern):**
1. Fetch today's games + odds
2. Compute features (point-in-time)
3. Run model + agreement scoring
4. Generate picks with Kelly sizing
5. Publish to website/database
6. Grade yesterday's results
7. Update system grades and performance tracking
8. Auto-prune underperforming systems

**Auto-correction pipeline (Diamond Predictions):**
- Track per-tier, per-system ROI
- Auto-prune systems below 15% ROI threshold
- Optimizer runs on schedule with walk-forward validation
- Auto-apply with rollback safety (if live ROI drops, revert)

**Loss analysis (Courtside AI):**
- Classify every losing bet (WHY did the model lose?)
- Detect trends (is one loss category growing?)
- Suggest coefficient adjustments (one at a time, anti-overfitting)
- Auto-revert on regression

---

# PART 4: CRITICAL ANTI-PATTERNS (Things That Will Lose You Money)

## 4.1 Using Flat Units Instead of Real Odds
Every bet must be sized and graded using REAL sportsbook odds. Flat 1u bets hide the true edge — a +300 underdog win is worth 3× a -150 favorite win. MMALogic fixed this bug 4 times across multiple sessions.

## 4.2 Fabricated Odds Fallbacks
When real odds are unavailable, SKIP the bet. Never fall back to hardcoded defaults (-150/-130). Diamond Predictions caught +5.93u of inflated P/L from fabricated Over/Under odds.

## 4.3 Overfitting to Small Samples
N=74 said one thing. N=8,741 said the opposite. Always wait for sufficient data before acting. Minimum N=50 for any filter/system.

## 4.4 Postseason/Tournament Models Using Regular Season Data
NCAA MADNESS tier: claimed 69% ATS, actual 37-43%. Postseason dynamics are fundamentally different. Build separate models or skip postseason entirely.

## 4.5 Trusting Model Confidence at Extremes
Edges >10% are almost always model error, not real opportunity. Cap or skip extreme-confidence picks.

## 4.6 Ignoring Monthly Signal Quality
Early season (March/April) predictions are unreliable in both baseball and hockey. Scale down bet sizes in low-signal months.

## 4.7 Letting Multiple Fix Cycles Burn Tokens
When a backtest corrupts, fix the ROOT CAUSE (the writer, the serializer, the pipeline), not the symptom (the corrupted file). Restoring and retrying produces the same corruption.

---

# PART 5: THE CHECKLIST (Before Shipping Any Model Change)

- [ ] Walk-forward validated on 3+ seasons?
- [ ] Minimum 200 test picks?
- [ ] Bootstrap 95% CI excludes zero?
- [ ] p-value < 0.05?
- [ ] Fold degradation is reasonable (not 3× between first and last)?
- [ ] Parameter-to-pick ratio better than 1:20?
- [ ] No future data leakage (point-in-time enforced)?
- [ ] Real odds used (not estimated or flat)?
- [ ] Edge capped at reasonable maximum (≤10%)?
- [ ] Monthly/seasonal adjustment applied where signal quality varies?
- [ ] Existing systems not broken by the change (regression test)?
- [ ] Committed and pushed to GitHub before deploying?

---

*Document generated 2026-04-03. Based on production data from MMALogic (UFC), Diamond Predictions (MLB+NHL), and Courtside AI (NBA+NCAA). All ROI figures are walk-forward validated, not in-sample.*
