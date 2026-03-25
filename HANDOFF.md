# Handoff — NFL Draft Predictor — 2026-03-25 01:00
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: First session

---

## 1. Session Summary
User wanted an AI-powered 2026 NFL Draft simulator that predicts all 32 first-round picks. We built a complete system: Python Monte Carlo simulation engine (V4 model, backtested at 14.0 exact picks/year across 10 seasons), React/Vite frontend deployed to Cloudflare Pages, and a refresh pipeline for weekly data updates. The model uses 12 weighted signals with expert consensus as the anchor (50%), supplemented by Vegas odds, team needs, prospect grades, and pre-draft visits. Analyst trust weights are computed from 6 years of verified WalterFootball accuracy data (2020-2025).

## 2. What Was Done (Completed Tasks)
- **Built simulation engine**: `engine/prospect_model.py`, `engine/simulator.py`, `engine/team_logic.py` — 12-signal scoring model with Monte Carlo simulation
- **Collected 10 years of draft data**: `data/draft_history_2016_2019.py`, `data/draft_history_2020_2022.py`, `backtest/historical_data.py` — actual + consensus mocks for 2016-2025
- **Built and ran 10-year backtest**: `backtest/model_v3.py`, `backtest/enriched_backtest.py` — tested V2, V3, V4, V5 model variants. V4 won at 14.0/yr
- **Scraped real 2026 data**: `data/prospects.json` (50 prospects), `data/teams.json` (32 teams with real FA/cap data), `data/vegas_odds.json`, `data/pre_draft_visits.json`
- **Integrated 7 expert mocks**: Tankathon, WalterFootball (Walt + Campbell), Daniel Jeremiah, Yahoo, CBS Prisco, Lineups.com — from March 17-25, 2026
- **Built verified analyst trust system**: `data/analyst_accuracy.json` — 6-year WalterFootball accuracy data, trust weights for 12 analysts, unvetted sources zeroed
- **Built advanced team evaluation framework**: `engine/advanced_team_eval.py` — roster depth, cap urgency, FA aftermath, GM personality, scheme fit, succession planning
- **Built refresh pipeline**: `scripts/refresh_pipeline.py` — updates data, runs sim, deploys to Cloudflare in one command
- **Deployed to Cloudflare**: https://draft-predictor.pages.dev/ — React frontend with latest predictions
- **Historical team eval system**: `backtest/historical_team_eval.py` — GM tenures, coach schemes, roster reconstruction for backtesting

## 3. What Failed (And Why)
- **Team needs at 15% weight degraded predictions**: Reconstructed historical team needs (from draft history) were too noisy. Even real expert-published needs couldn't improve V4 because discrete consensus scoring creates 20-point gaps that needs data can't bridge. Root cause: the model is structurally consensus-anchored — needs can only help through the consensus signal itself.
- **V5 enriched model lost to V4 in every variant**: Tried flat weighting, adaptive weighting, tiebreaker-only — all either tied or lost to V4. The advanced_team_eval.py framework is architecturally sound but requires real current-year data to add value (works for 2026, can't be validated historically).
- **10K simulation duplicates**: First 10K run produced duplicate players in aggregate. Fixed by adding greedy uniqueness enforcement in `refresh_pipeline.py`.
- **Initial 2025 data confusion**: First build accidentally used 2025 draft class instead of 2026. Shedeur Sanders projected #1 when he was a 5th-round pick in the actual 2025 draft. Caught by user, rebuilt correctly.

## 4. What Worked Well
- **Backtest-driven development**: Testing every model change against 10 years of real data prevented overfitting and caught bad approaches early
- **Empirical analysis of error categories**: Categorizing 178 wrong picks into REORDER/SLOT_SWAP/SURPRISE revealed that 52% are theoretically fixable by better data
- **6-year verified analyst weights**: Using complete WalterFootball accuracy data (2020-2025) instead of guessing produced objectively correct trust weights
- **Parallel research agents**: Background agents for scraping while coding in foreground maximized throughput
- **Refresh pipeline**: One command updates all data, runs simulation, and deploys

## 5. What The User Wants (Goals & Priorities)
- **Primary goal**: Predict the 2026 NFL Draft first round as accurately as possible (beat human GOAT Jason Boris at 13.0/yr)
- **Current status**: V4 model backtests at 14.0/yr. 2026 prediction deployed with picks 1-5 at 99.7-100% confidence
- **Explicit preferences**: Only trust verified analysts with multi-year accuracy data. Unvetted = 0% weight. Research before coding. Validate everything against historical data.
- **Frustrations**: Duplicate players in draft board (caught twice — now fixed with enforcement). Initial confusion with 2025 vs 2026 data.

### User Quotes (Verbatim)
- "This is horrible, first it's fully populated with 2025 picks, not 2026" — context: first build accidentally used wrong year's data
- "unvetted = 0% confidence" — context: setting the rule that only verified analysts contribute to the model
- "we just need a validated way to determine what those team needs actually are, and what they are actually going to spend a first round pick to address" — context: discussing team needs integration

## 6. What's In Progress (Unfinished Work)
- **Website frontend quality**: The Cloudflare site loads but hasn't been visually audited — may need UI polish, responsive design check, data display verification
- **Picks 17-32 from Campbell's mock**: Only captured picks 1-13 from WalterFootball. Picks 14-32 need scraping from the second page
- **Additional expert mocks to integrate**: Camenker, Norris, Brugler, Schrager mocks not yet in prospect data — only have Tankathon, Walt, Campbell, Jeremiah, Yahoo, Prisco, Lineups
- **Advanced team eval for 2026**: `engine/advanced_team_eval.py` is built but not wired into the production scoring model. It works for 2026 (real data) but couldn't be backtested (historical data too noisy)

## 7. Blocked / Waiting On
- **Jason Boris mock**: Not available until draft morning (April 23). He's the #1 analyst but publishes last.
- **Closing Vegas odds**: Current odds are from late March. Final odds publish April 22-23 and will be significantly sharper.
- **Draft-week consensus refresh**: The biggest accuracy improvement will come from April 20-22 mock updates. Pipeline is ready (`refresh_pipeline.py`).

## 8. Next Steps (Prioritized)
1. **Visual audit of Cloudflare site** — verify all 32 picks display correctly, no duplicate data, responsive design works
2. **Add more expert mocks** — scrape Camenker, Norris, Brugler 2026 mocks and integrate into prospects.json
3. **Weekly refresh cadence** — run `python3 scripts/refresh_pipeline.py --deploy` every Sunday through April 20
4. **Draft week intensive refresh** — April 20 (Mon), April 22 (Wed AM + PM), April 23 (Thu morning) — update all data sources
5. **Wire advanced_team_eval into production** — for 2026 only, use real roster/FA/cap data as a tiebreaker signal

## 9. Agent Observations

### Recommendations
- **Don't fight consensus**: The model's ceiling is determined by consensus data quality. Every experiment showed consensus dominance. Focus on getting the FRESHEST consensus rather than adding more signals.
- **Closing-week data is 90% of the game**: The difference between March mocks and April 22 mocks is ~5-10 extra correct picks. Build the refresh cadence around this.

### Patterns & Insights
- **Discrete consensus scoring is a structural limitation**: 100/80/60/40/20 point tiers create gaps too large for any secondary signal to overcome. This is why team needs, scheme fit, etc. can't improve predictions in backtesting.
- **The top 5 picks are extremely predictable**: 7/7 experts agree on picks 1-2, 5/7 on picks 3-5. The value-add is in picks 6-20 where consensus breaks down.
- **Analyst accuracy varies wildly by year**: Campbell got 13 in 2024 and 7 in 2023. Norris got 15 in 2021 and 5 in 2022. Multi-year averaging is essential.

### Where I Fell Short
- **Initial 2025/2026 confusion**: Should have verified the draft year from the start instead of assuming
- **Too many model variants tested**: V2, V3, V4, V5, enriched — consumed tokens that could have been spent on data quality
- **Duplicate enforcement should have been built from day 1**: This bug appeared 3 times before being properly fixed

## 10. Miscommunications to Address
- **2025 vs 2026 draft year**: First build used wrong year. Next agent must verify year before any work.
- **Team needs weight**: User wanted 15% for team needs. Backtesting proved this hurts with reconstructed data but could help with real current-year data. The model currently uses team needs through the consensus signal (experts already factor in needs).

## 11. Files Changed This Session
**No git repo — listing key files by modification time:**

| File | Action | Description |
|------|--------|-------------|
| engine/prospect_model.py | created | 12-signal scoring model with weighted analyst consensus |
| engine/simulator.py | created | Monte Carlo draft simulator with uniqueness enforcement |
| engine/team_logic.py | created | Team-specific override rules (Raiders QB lock, etc.) |
| engine/advanced_team_eval.py | created | Advanced team needs framework (roster, cap, scheme, GM) |
| data/prospects.json | created+updated | 50 prospects with 7-mock expert picks + Vegas odds |
| data/teams.json | created+updated | 32 teams with real 2026 FA/cap/roster data |
| data/analyst_accuracy.json | created+updated | 12 analysts with 6-year verified trust weights |
| data/vegas_odds.json | created+updated | Real DraftKings/FanDuel odds for top prospects |
| data/draft_order.json | created | 32-pick first round order with traded picks |
| data/pre_draft_visits.json | created | Pre-draft visit tracker |
| data/team_roster_analysis_2026.json | created | Deep roster analysis for top 16 teams |
| data/historical_team_needs_expert.py | created | Expert-published team needs 2020-2025 |
| data/historical_draft_odds_2020_2025.py | created | Historical Vegas odds for backtesting |
| data/prospect_grades_2020_2025.py | created | Historical big boards for backtesting |
| data/historical_visits_2020_2025.py | created | Historical visit data for backtesting |
| data/draft_history_2016_2019.py | created | Actual + consensus picks 2016-2019 |
| data/draft_history_2020_2022.py | created | Actual + consensus picks 2020-2022 |
| backtest/historical_data.py | created | Actual + consensus picks 2023-2025 |
| backtest/historical_team_eval.py | created | GM tenures, coach schemes, roster reconstruction |
| backtest/enriched_backtest.py | created | V4 vs V5 backtest comparison |
| backtest/model_v2.py | created | V2 model with full signal set |
| backtest/model_v3.py | created | V3 model with 5 new signals |
| scripts/refresh_pipeline.py | created | Full refresh + simulate + deploy pipeline |
| scripts/run_simulation.py | created | Standalone simulation runner |
| frontend/ | created | React/Vite app deployed to Cloudflare Pages |
| results/latest_prediction.json | created | Most recent 32-pick prediction |

## 12. Current State
- **Branch**: No git repo (iCloud directory)
- **Last commit**: N/A
- **Build status**: Frontend builds successfully (Vite, 94ms)
- **Deploy status**: Deployed to https://draft-predictor.pages.dev/ (last deploy: 2026-03-25 00:59)
- **Uncommitted changes**: N/A (no git)

## 13. Environment State
- **Node.js**: v25.6.1
- **Python**: 3.14.3
- **Running dev servers**: Vite dev server on port 5174 (PID 24579)
- **Environment variables set this session**: None
- **Active MCP connections**: Claude in Chrome, Desktop Commander, Claude Preview, PDF Tools

## 14. Session Metrics
- **Duration**: ~7 hours (5:00 PM - 1:00 AM)
- **Tasks completed**: 15+ major tasks
- **User corrections**: 4 (2025/2026 confusion, duplicate players x2, unvetted sources)
- **Tool calls**: 200+ estimated
- **Skills/commands invoked**: deploy, full-handoff
- **Commits made**: 0 (no git repo)

## 15. Memory & Anti-Patterns Updated
- No memory updates this session — should save: NFL Draft project context, V4 model architecture, analyst trust hierarchy, refresh pipeline location
- **TODO for next agent**: Save project memory with key findings (consensus dominance, 14.0/yr baseline, verified analyst weights)

## 16. Skills & Agents Used
| Skill/Agent | How It Was Used | Was It Helpful? |
|-------------|----------------|-----------------|
| Background research agents (x8) | Scraped draft data, team needs, Vegas odds, analyst accuracy | Yes — parallelized research effectively |
| Claude in Chrome | Read Campbell's mock from WalterFootball, checked Tankathon | Yes — captured fresh expert data |
| deploy skill | Deployed to Cloudflare Pages | Yes — seamless |
| full-handoff skill | This document | Yes |

## 17. For The Next Agent — Read These First
1. This HANDOFF.md
2. Previous handoff: First session (none)
3. `data/analyst_accuracy.json` — verified trust weights with 6-year raw data
4. `scripts/refresh_pipeline.py` — run `python3 scripts/refresh_pipeline.py --deploy` for updates
5. `engine/prospect_model.py` — the scoring model (12 signals, V4 weights)
6. `frontend/2026_NFL_Mock_Draft_Consensus_March25.md` — latest 7-mock consensus comparison
7. `data/team_roster_analysis_2026.json` — real 2026 roster/FA/cap analysis

### Critical Rules
- **Unvetted analysts = 0% weight**: Only analysts with 6-year WalterFootball data contribute
- **Discrete consensus scoring**: 100/80/60/40/20 tiers. Secondary signals can't bridge these gaps.
- **V4 model is the baseline**: 14.0/yr backtested. Any changes must beat this or be rejected.
- **No duplicate players**: Uniqueness enforcement in refresh_pipeline.py prevents this
- **Draft is April 23-25, 2026 in Pittsburgh**: 29 days from now
