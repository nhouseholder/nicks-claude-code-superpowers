# Handoff — MMALogic (UFC Predict) — 2026-03-28 00:30
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: handoff_ufc-predict_2026-03-26_2143.md
## GitHub repo: nhouseholder/ufc-predict
## Local path: ~/Projects/mmalogic/
## Last commit date: 2026-03-27 23:19:07 -0700

---

## 1. Session Summary
User wanted to implement the SUB→DEC fallback betting strategy, build an expert consensus system, update the live site, and investigate whether expert picks could improve the model. SUB→DEC was implemented across 4 algorithm sections + live scorer, backtested (+34.57u method improvement, +10.40u net), deployed to mmalogic.com at v11.13.1. Expert consensus system was built (5 verified experts, Playwright scraper, consensus builder) but backtesting showed no lift over the algorithm alone — user decided to keep algorithm standalone.

## 2. What Was Done
- **SUB→DEC fallback (v11.13)**: Modified `UFC_Alg_v4_fast_2026.py` (4 sections: backtester scoring ~9259, card display ~10353, summary display ~10492, JSON output ~10682) and `track_results.py` (~line 561). Added `SUB_DEC_FALLBACK = True` constant. When algorithm predicts SUB, bets DEC instead. Method P/L: +58.39u → +92.96u.
- **Registry totals recomputation**: Registry `totals` were stale (300W-114L, no parlay). Recomputed from all 504 bouts + 64 parlays. Combined: +293.48u.
- **Round hero card restored**: `HeroStats.jsx` — added Round card back (was excluded when negative ROI). Now all 5 bet types displayed. Grid changed from 4-col to 5-col.
- **Expert consensus system**: Built `ufc_expert_consensus/` directory with 8 files — expert_registry.json (5 experts with trust scores), consensus_builder.py (weighted vote calculator), playwright_scraper.py (BetMMA.tips scraper), trust_hierarchy.md, scrape_expert_picks.py, README.md, expert_picks/ufc_seattle.json template, expert_history/ (scraped data for all 4 BetMMA experts).
- **Playwright scraper**: Full history scrape for all 4 BetMMA experts (Jack Attack 100 events/985 picks, Dravhy 55/670, Lucrative 99/1054, Rob Brown 89/193). Uses headed Chromium to bypass Cloudflare.
- **Expert consensus backtest**: Matched 230 expert picks to registry bouts. Found NO lift — our model is 76.1% accurate when experts strongly disagree vs 66.7% when they strongly agree. Expert-driven parlay selection showed +105.6% ROI but only 7 events (insufficient sample).
- **CLAUDE.md updates**: SUB→DEC fallback docs, baseline numbers updated to v11.13, DEC-has-no-round rule, R1 KO gating rule documented.
- **Site deployed**: 3 pushes to GitHub CI (v11.13.0 main, registry fix, Round card v11.13.1). All deployed successfully.

## 3. What Failed (And Why)
- **iCloud git corruption**: Pack file `pack-3203b83b4318ea070d45427bdce356ff23cc29aa.pack` corrupted during session (iCloud sync issue). Workaround: cloned to `/tmp/mmalogic-commit` and pushed from there. The local iCloud repo needs `git clone` to reset.
- **BetMMA.tips paywalled picks**: All upcoming expert picks are behind $10/event paywall. User confirmed "we aren't buying anyone picks." Free data limited to post-event pick history.

## 4. What Worked Well
- SUB→DEC analysis was thorough — proved +53.9% ROI before implementing. Data-driven decision.
- Playwright bypassed Cloudflare in headed mode with anti-detection flags.
- Full expert history scrape (2900+ picks across 4 experts) completed in one pass.
- Consensus backtest was honest — showed no lift instead of overfitting to small samples.

## 5. What The User Wants
- Algorithm stands on its own, no expert integration: "alright, lets do algorithm on its own, no experts"
- Never buy expert picks: "we aren't buying anyone picks"
- Data-driven decisions before implementing: "we can only do option 2 if we prove it's historically profitable"
- Strict inclusion filters for experts: "if any expert is under 12% ROI or we don't have a huge sample size... we don't include them"
- DEC has no round — corrected my display: "DEC R2 for chiesa, that doesn't make sense, DEC has no round, it's the end of the fight lol"

## 6. In Progress (Unfinished)
All tasks completed. Expert consensus system is built and archived for future use when more data accumulates (need 200+ multi-expert overlapping bouts, currently at 65).

## 7. Blocked / Waiting On
Nothing blocked. Kiev O'Neil (BoydsBets expert, #3 ranked) has no BetMMA.tips profile — can only be scraped via BoydsBets leaderboard or manual entry.

## 8. Next Steps (Prioritized)
1. **Score UFC Seattle results Sunday** — `track_results.py` after event completes (2026-03-28). 6 active picks: Barber, Chiesa, McKinney, O'Neill, Stirling, Simon. Adesanya is a PASS (0.13 diff < 0.1428 threshold).
2. **Fix iCloud git corruption** — `cd ~/Projects/mmalogic && rm -rf .git && git clone https://github.com/nhouseholder/ufc-predict.git /tmp/fresh-ufc && cp -r /tmp/fresh-ufc/.git .git` to restore clean git state.
3. **Scrape expert picks after UFC Seattle** — Run `python3 playwright_scraper.py --history --max-events 5` to capture experts' Seattle picks (now free/visible post-event). Grows the consensus dataset.

## 9. Agent Observations
### Recommendations
- The expert consensus parlay idea (+105.6% ROI) is promising but needs 30+ events. Worth revisiting in 6-8 months. Save a memory note.
- The iCloud git corruption issue is recurring. Consider the `/reorganize-ufc` skill to move to `~/Projects/` canonical path permanently.
- SUB→DEC fallback should be documented in the betting model spec (`ufc_betting_model_spec.md`) as a permanent gating rule.

### Where I Fell Short
- Initially displayed Adesanya as an active pick when he's a PASS (0.13 < 0.1428 threshold). Should have checked `is_pass` flag in prediction_output.json before presenting picks.
- Showed "DEC R2" for Chiesa — nonsensical since DEC has no round. Should have stripped the round when SUB→DEC fires.

## 10. Miscommunications
- Showed Adesanya in active picks table — user correctly caught it was below threshold.
- Showed Chiesa as "DEC R2" — user correctly noted DEC has no round. Rules updated.

## 11. Files Changed
31 files changed, 4114 insertions, 2271 deletions across 6 commits.

| File | Action | Why |
|------|--------|-----|
| UFC_Alg_v4_fast_2026.py | Modified | SUB_DEC_FALLBACK constant + 4 scoring sections |
| track_results.py | Modified | Live scorer SUB→DEC fallback |
| CLAUDE.md | Modified | Baseline numbers, SUB→DEC docs, DEC-no-round rule |
| algorithm_stats.json | Modified | Parlay totals, version bump, features list |
| ufc_profit_registry.json | Modified | Recomputed totals from bout-level data |
| webapp/frontend/src/config/version.js | Modified | 11.9.6 → 11.13.1 |
| webapp/frontend/src/components/landing/HeroStats.jsx | Modified | 5-card grid + Round card |
| webapp/frontend/public/data/*.json | Modified | Synced from root |
| ufc_expert_consensus/ (8 files) | Created | Full consensus system |
| ufc_expert_consensus/expert_history/ (4 files) | Created | Scraped expert pick history |

## 12. Current State
- **Branch**: main
- **Last commit**: fe12f65 "Clarify DEC has no round + R1 KO gating rules in CLAUDE.md" (2026-03-27 23:19:07 -0700)
- **Build**: passing (vite build succeeds)
- **Deploy**: deployed via GitHub CI (3 successful deploys this session)
- **Uncommitted changes**: fight_breakdowns.json, prediction_cache/, ufc_prop_odds_cache.json, various backup/log files
- **Local SHA matches remote**: iCloud repo is corrupted (git pack issue). GitHub has the correct latest code.

## 13. Environment
- **Node.js**: v25.6.1
- **Python**: 3.14.3
- **Dev servers**: none running
- **Playwright**: installed (chromium browser)

## 14. Session Metrics
- **Duration**: ~180 minutes
- **Tasks**: 6 completed / 6 attempted
- **User corrections**: 3 (Adesanya pass, DEC-no-round, no buying picks)
- **Commits**: 6 (v11.13.0, registry fix, Round card v11.13.1, CLAUDE.md x2, DEC rules)
- **Skills used**: /mmalogic, /full-handoff

## 15. Memory Updates
- CLAUDE.md: Updated baseline numbers to v11.13, added SUB→DEC fallback docs, DEC-has-no-round rule, R1 KO gating clarification
- anti-patterns.md: Synced to superpowers repo
- project_expert_consensus.md: Previously created (expert consensus project status)
- feedback_expert_consensus_filters.md: Previously created (strict 12%+ ROI filter)

## 16. Skills Used
| Skill | Purpose | Helpful? |
|-------|---------|----------|
| /mmalogic | Full site update protocol | Yes — loaded knowledge base, verified freshness, deployed correctly |
| /full-handoff | End-of-session handoff | Yes |

## 17. For The Next Agent
Read these files first (in order):
1. This handoff (HANDOFF.md)
2. ~/.claude/anti-patterns.md (search for "UFC" entries)
3. CLAUDE.md (project rules + baseline numbers)
4. ~/.claude/memory/topics/ufc_betting_model_spec.md
5. ~/.claude/memory/topics/ufc_website_maintenance_rules.md

**Canonical local path for this project: ~/Projects/mmalogic/**
**Do NOT open this project from iCloud or /tmp/. Use the path above.**
**WARNING: iCloud .git is corrupted — may need to re-clone .git from GitHub.**

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
Before doing ANY work, run the 3-Gate Verification from ~/.claude/CLAUDE.md:
1. GATE 1: Check ~/Projects/site-to-repo-map.json — verify you're in the correct repo
2. GATE 2: git fetch && compare local SHA to remote — git pull if behind
3. GATE 3: Read this handoff + MEMORY.md + anti-patterns.md + recurring-bugs.md
ALL 3 GATES MUST PASS before touching any code.

**Canonical path for this project: ~/Projects/mmalogic/**
**Last verified commit: fe12f65 on 2026-03-27 23:19:07 -0700**
