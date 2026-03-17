---
name: profit-driven-development
description: The north star for all sports prediction work — future predictive accuracy and profitability. Every backtest, every parameter change, every algorithm decision must be evaluated against one question: will this make the NEXT picks more correct and more profitable? Prevents getting lost in endless optimization loops that overfit the past. Always-on for sports code sessions.
---

# Profit-Driven Development — Never Lose Sight of the Goal

## The Goal (Say It Every Time)

**We are trying to predict the future and make money.**

Not fit the past. Not optimize a metric. Not make a backtest look impressive. The ONLY thing that matters is:

> **Will this change make the algorithm pick MORE winners on games that haven't happened yet?**

If the answer isn't clearly "yes" — stop, step back, and ask why you're doing it.

## When This Fires

Always-on during any session that touches sports prediction code, betting algorithms, or backtesting infrastructure. This skill is the permanent background voice that asks "but will it actually work on FUTURE games?"

## The Three Questions — Before Every Change

Before modifying any part of the sports prediction system, answer:

### 1. "Will this make the NEXT bet more likely to win?"
Not "does this improve accuracy on 2024 data" but "if a game happens TOMORROW, does this change make the pick better?"

If you can't articulate HOW it improves future predictions, don't make the change.

### 2. "Am I fitting the past or learning a pattern?"
| Fitting the Past (BAD) | Learning a Pattern (GOOD) |
|------------------------|--------------------------|
| "This weight works great on last season's data" | "This factor captures a real-world dynamic that will repeat" |
| "Accuracy went up 2% when I added this parameter" | "This corrects for a known bias in the base model" |
| "The optimal value for games 1-500 is 0.173" | "Recent form matters more than season averages because injuries and momentum are real" |
| "Adding 5 more features boosted R²" | "This single feature captures information the model currently misses" |

### 3. "Would I bet my own money on this?"
The ultimate gut check. If the change makes the backtest look better but you wouldn't actually increase your bet size because of it — it's probably overfitting.

## The Overfitting Trap — How Claude Gets Lost

Here's what typically happens:
1. User asks to test a new variable
2. Claude runs a backtest → it doesn't help
3. Claude tweaks the weight → slightly better
4. Claude adds more complexity → accuracy goes up on training data
5. Claude runs 10 more variations → finds one that looks great
6. **The "improvement" is noise that won't generalize to future games**

**The fix:** After EVERY backtest result, ask: "Is this improvement because I found a real signal, or because I tried enough variations that one happened to fit the noise?"

### Red Flags That You're Overfitting
- Accuracy improves when you add a 4th decimal place to a weight
- The "optimal" parameter is very different from what domain knowledge suggests
- Improvement only shows on one subset of the data
- You've tried 10+ variations and the "best" one is barely better than the baseline
- The improvement disappears when you test on a different time period
- You can't explain WHY the change should work in plain English

### Green Flags That You Found a Real Signal
- The improvement is robust across multiple time periods
- The parameter value makes sense from a domain perspective
- You can explain the mechanism: "X predicts Y because Z is a real-world dynamic"
- The effect size is meaningful (not 0.1% accuracy improvement)
- Holdout data confirms the improvement
- The change makes the model SIMPLER (fewer parameters, not more)

## Profit Math — Keep It Real

Every change should be evaluated in terms of actual betting outcomes:

| Metric | What It Means | Why It Matters |
|--------|--------------|----------------|
| **Win rate** | % of picks that win | Must beat the vig threshold (~52.4% at -110) |
| **ROI** | Profit per dollar wagered | The real bottom line |
| **CLV (Closing Line Value)** | Did you beat the closing line? | Best predictor of long-term profitability |
| **Drawdown** | Worst losing streak | Even profitable systems have losing runs — is it survivable? |
| **Edge consistency** | Does the edge persist across time? | A 60% win rate for one month then 45% forever = no edge |

**An algorithm that wins 53% consistently is worth more than one that wins 58% on backtested data but is overfit.**

## What Claude Must Do Differently

### Stop Spinning on Backtests
If you've run 5+ backtests on the same feature with minor tweaks and haven't found a clear signal:
- **STOP.** Present findings to the user.
- Say: "I've tested [feature] at [values]. The signal is [weak/inconsistent/absent]. Here's what I think is happening: [analysis]. Want me to try a fundamentally different approach, or move on?"
- Do NOT run backtest #6 with weight=0.127 instead of 0.125.

### Start with the Hypothesis
Before ANY backtest:
- "I believe [X] will improve predictions because [real-world reason]"
- "If this works, I expect [specific improvement] because [mechanism]"
- "This is NOT overfitting because [the signal is generalizable for this reason]"

If you can't fill these in, you don't have a hypothesis — you're just trying stuff.

### Evaluate Changes by Future Value, Not Past Fit
After EVERY backtest result:
- "This improved accuracy by X% — is this because of a real pattern or noise?"
- "Would this improvement hold on games from NEXT season? Why?"
- "Am I more confident in tomorrow's picks because of this change?"

### Keep the Model Simple
- Fewer parameters = less overfitting risk
- Every parameter must earn its place with a clear, explainable signal
- If two features are correlated, keep the one with stronger domain justification
- A simple model that's 53% accurate and robust > a complex model that's 58% on paper

## Integration

- **backtest**: Every backtest must answer: "Does this help predict FUTURE games?" Not just "Does this fit historical data?"
- **think-efficiently**: Don't waste tokens on backtests that won't produce actionable information. Binary search, not linear sweep.
- **never-give-up**: If a feature has proven independent profitability, persist. But persistence must be guided by THIS skill's future-first lens.
- **parallel-sweep**: Sweep ranges should be domain-informed and the winner must pass the overfitting test.
- **expert-lens**: Sports analytics expertise (CLV, vig-adjusted ROI, regression to the mean) should be active during all sports code work.

## Rules

1. **Future-first** — Every change must be justified by its impact on FUTURE predictions, not historical fit
2. **Explain the mechanism** — If you can't say WHY a change helps in plain English, it's probably overfitting
3. **Stop spinning** — 5+ minor-tweak backtests without a clear signal = stop and escalate
4. **Simple beats complex** — Fewer parameters with real signals > many parameters with noise
5. **Profit is the metric** — Not accuracy, not R², not backtest performance. Actual expected profit.
6. **Holdout always** — Never evaluate a change only on the data used to develop it
7. **Domain knowledge first** — Start from what we know about sports, not from what the data mining found
8. **Would you bet on it?** — If you wouldn't increase bet size based on the change, it's not real
