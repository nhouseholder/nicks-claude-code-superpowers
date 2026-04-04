# Anti-Patterns — Known Failures & Working Fixes

> Claude checks this before debugging to avoid repeating known-bad approaches.
> Pruned 2026-04-01: kept recurring behavioral patterns + permanent rules. One-time bug fixes removed (the fix is in the code).
> Last updated: 2026-04-03

## UFC — Fabricated O/U Odds Fallback (FABRICATED_ODDS) — 2026-04-03
- **Pattern**: When real BFO O/U odds exceed the ±400 cap, the algorithm silently falls back to hardcoded -150 (Over) or -130 (Under) defaults. These fabricated odds produce inflated P/L (e.g., -150 pays +67% vs real -430 paying +23%).
- **Root cause**: Cap was designed for derived odds (which can hit -2000+) but also rejected legitimate real sportsbook odds at -430 to -500. Fallback to hardcoded default was silent — no indication that real odds were rejected.
- **Impact**: +5.93u inflated P/L from fake odds payouts on heavy-juice Over bets.
- **Fix**: When real BFO odds exist and exceed ±400, SKIP the bet entirely. Never fall back to fabricated defaults. Applies in both prediction path (UFC_Alg line ~9760) and backtest path (fix_registry_placed_flags.py line ~370).
- **Applies when**: Any O/U odds handling. If you add a new odds source, ensure the cap-exceeded path SKIPS rather than falls back to a default.

## UFC — Stale Derived Data Files (STALE_HERO_STATS) — 2026-04-01
- **Pattern**: Registry is updated (via fix_registry_placed_flags.py or manual sweep) but hero_stats.json and algorithm_stats.json are NOT regenerated. Website shows inflated/wrong numbers (+327.99u instead of +300.72u).
- **Root cause**: fix_registry_placed_flags.py wrote the registry but didn't trigger the data pipeline (sync_and_deploy.py). hero_stats.json was a pre-baked snapshot that went stale.
- **Fix (permanent, 2 layers)**:
  1. Frontend `getHeroStats()` now always computes from registry via `computeSummaryFromRegistry()` — never reads hero_stats.json
  2. `fix_registry_placed_flags.py` auto-imports and runs `sync_and_deploy.py`'s regeneration after any registry write
- **Applies when**: Any script modifies ufc_profit_registry.json outside of sync_and_deploy.py. Always verify hero_stats.json and algorithm_stats.json match registry totals after registry modifications.

## UFC — Career Stats Data Leakage in Backtester (CAREER_STATS_LEAKAGE) — 2026-04-01
- **Pattern**: Backtester produces different picks than live predictions for recent events. Pick-flips where backtester "knows" who won.
- **Root cause**: `get_fighter_stats()` returns a single snapshot of career stats (SLpM, StrAcc, TDAvg, etc.) from `ufc_backtest_registry.json` without temporal filtering. After a fighter's latest fight, their stats change on ufcstats.com. The backtest registry stores current stats, so the backtester sees post-fight data for recent events.
- **Impact**: 3 pick-flips, 4 divergences across 3 archived events. +10.44u inflated P/L corrected.
- **Fix (immediate)**: `patch_registry_from_archive.py` — patches divergent bouts using prediction_archive/ as ground truth. Run after every backtest for events that have archives.
- **Fix (long-term needed)**: Compute career stats from fight-level data with temporal cutoff (same approach used for Elo and method profiles). This would require refactoring `get_fighter_stats()` to aggregate from `fight_history` entries filtered by `cutoff_date`.
- **Applies when**: Any backtest re-run. Always cross-check last 5 events against prediction_archive/ after re-running the backtester.

## General — iCloud Filesystem Stalling (ICLOUD_STALL)
- **Pattern**: Grep/read stalls on iCloud files → Claude retries with different tool → same stall → token burn loop
- **Fix**: Clone from GitHub to `/tmp/`, work there. Never retry stalling ops with a different tool — the issue is iCloud, not the tool.

## General — Context Overload From Data Dumps (CONTEXT_FLOOD)
- **Pattern**: Reading 3+ large files + dumping raw JSON in one turn → context full → silent/dead stop
- **Fix**: Max 2 large reads per turn. Never dump raw JSON — use `python3 -c` for targeted queries. Act before reading more.

## General — Empty Output Retry Loop (BLIND_RETRY)
- **Pattern**: Command produces empty output → Claude re-runs 4+ times without diagnosing why
- **Fix**: STOP → check exit code/stderr/cwd/deps → isolate smallest test → fix cause → THEN re-run.

## General — Triple Pivot: Full Pipelines Before Math (TRIPLE_PIVOT)
- **Pattern**: Running full backtests to test parameter changes that could be answered with arithmetic
- **Fix**: Pre-compute gate: (1) Can math answer this? (2) Can a 10-line script? (3) Locked approach? All must pass before running pipeline.

## General — Domain Flip-Flop Without Reading Spec (FLIP_FLOP)
- **Pattern**: Changing betting/scoring/business rules 3-4 times in one session without reading the spec
- **Fix**: Read the spec FIRST. Never change domain rules based on "I think" — read EVENT_TABLE_SPEC.md or the relevant spec file.

## General — Revert Loop (REVERT_LOOP)
- **Pattern**: Implementing a change → reverting → re-implementing → reverting. 5+ reversals of the same decision.
- **Fix**: Lock your approach before starting. Write a 1-sentence plan. If you need to revert, explain WHY in writing before reverting.

## Permanent — NEVER Accept Missing Odds
- Prop odds must be scraped/backfilled, never accepted as null. Missing odds → missing P/L → wrong totals.
- Run `python3 check_prop_odds.py` after any registry modification.

## Permanent — NEVER Gate Bets by Odds Range
- DEC odds gate caused -91.95u regression. Longshot wins (+300 to +800) cross-subsidize mid-range losses.
- Method bets are a portfolio — never remove the tail.

## Permanent — NEVER Deploy Without Commit
- Cloudflare deploys are irreversible. Deploying from dirty working tree → old code overwrites new frontend.
- Always: commit → push → deploy from clean state.

## Permanent — NEVER Overwrite Firestore/Registry Without Backup
- Size-check before write. If new data is smaller than existing → ABORT. Backup first, merge don't replace, post-write verify.

## Permanent — NEVER Touch Frontend During Backend/Algorithm Updates
- Algorithm update destroyed courtside-ai admin page. Backtester run overwrote live prediction page.
- Scope: if the task says "algorithm," touch ONLY algorithm files. Never modify components, pages, or styles.

## Permanent — NEVER Rename Directories With Active Sessions
- Kills all Claude sessions instantly. Warn user first, ensure handoffs exist.

## UFC — SUB→DEC Fallback Is Optimal (DO NOT OVERRIDE)
- GSA hybrid gate tested: +0.00u delta. Elite grapplers win by DEC (55%), not SUB (25%).
- The blanket SUB→DEC fallback captures the dominant outcome and is mathematically optimal.

## UFC — Ghost X Bug Prevention
- Always use `*_placed` flags, never infer bet placement from `*_correct !== null`.
- Run `python3 validate_registry_cells.py --strict` after any registry modification.

## UFC — Round Bet Is INDEPENDENT of Method
- Round and method are separate bets. Fighter loss = ALL prop bets lose. SUB gating stays.
- See EVENT_TABLE_SPEC.md for canonical scoring rules.

## Build — Node 25 Rollup Deadlock
- Node 25 + Rollup causes hanging builds. Use `NODE_OPTIONS=--max-old-space-size=4096` or downgrade to Node 22.

## General — Deploy Without GitHub Push (DEPLOY_WITHOUT_PUSH) — 2026-04-01
- **Pattern**: `wrangler pages deploy dist/` runs successfully, version goes live, but source was never committed/pushed to GitHub. Subsequent sessions see stale code, can't review changes, and source is effectively lost in the minified CDN bundles.
- **Root cause**: Previous sessions deployed to Cloudflare Pages directly without committing to git first. 10 versions (v5.168–v5.177 of MyStrainAI) were lost and had to be reverse-engineered from minified production JS.
- **Fix**: ALWAYS commit + push BEFORE deploying. Mandatory sequence: build → commit → push → deploy → verify. Never use `wrangler pages deploy` without a clean git state and pushed commit.
- **Applies when**: Any Cloudflare Pages deploy, any version bump, any `wrangler` command. Check `git status` before deploying — if there are uncommitted changes, commit and push first.

## Permanent — ALWAYS Use `tier` Field for Pick Filtering (TIER_FILTER_GATE) — 2026-04-02
- **Pattern**: Frontend filters picks using legacy boolean flags (`is_apex`, `is_agree`, `is_ml_pick`) which miss newer tiers (MADNESS, DISCOVERY, MONEYLINE) that only set `tier` field. Picks appear in grading but never show in bet history.
- **Root cause**: DashboardPage.jsx `unifiedResults` filter checked `!r.is_apex && !r.is_agree && !r.is_ml_pick` — MADNESS picks have `is_madness: true` but this flag was never checked. The `tier` field was introduced later but never used as the canonical filter.
- **Fix**: Filter on `tier` field first (`VALID_TIERS` set), fall back to boolean flags for legacy data. Badge rendering also uses tier-first logic.
- **Rule**: NEVER filter picks using only boolean flags. Always check `tier` field. When adding a new tier, add it to BOTH: (1) `TRACKED_TIERS` in grading files, (2) `VALID_TIERS` in frontend display filters. Both NCAA and NBA.
- **Applies when**: Any new tier is added, any frontend bet history rendering, any grading pipeline change.

## Permanent — NEVER Apply Filters From Small Samples (SMALL_SAMPLE_FILTER) — 2026-04-02
- **Pattern**: Experiment on N=74 showed "|model_spread|>=10 = 48.6% ATS" → applied as production filter. Expanded dataset (N=8,741) showed edge 10+ = 52.0% ATS (profitable). Filter was cutting good picks.
- **Root cause**: Small samples (N<200) produce noisy ATS estimates. A 48.6% finding on N=74 has a 95% CI of roughly [37%, 60%] — it could easily be 55% ATS.
- **Fix**: NEVER apply hard production filters from experiments with N<200 decided bets. Use the auto-learning pipeline (auto-prune with rolling 30-bet windows) instead — it evaluates continuously as data accumulates.
- **Rule**: For any hypothesis to become a hard-coded filter, it must show statistical significance (p<0.05) on N≥200 walk-forward validation data. Below that threshold, log the finding and let auto-prune handle it.
- **Applies when**: Any experiment finding, any backtest result, any "this range underperforms" conclusion.

## Permanent — NCAA Postseason Model FAILS (POSTSEASON_FAIL) — 2026-04-02
- **Pattern**: NCAA MADNESS/tournament tier shows high backtest ATS on small cherry-picked subsets, but 3-season walk-forward on N=350 postseason games = 37-43% ATS consistently. Live record: 2W-3L (40%).
- **Root cause**: Elo ratings from regular season don't transfer to single-elimination tournament play (neutral sites, different team preparation, higher variance). The "69.2% ATS" claim was overfitted.
- **Fix**: MADNESS tier disabled in v12.36.3. Code preserved, `if (false &&` guard.
- **Rule**: Do NOT re-enable postseason picks without a fundamentally different model (not just parameter tuning of Elo). Regular season model works (57.4% ATS, N=8,225).
- **Applies when**: Any discussion of March Madness picks, tournament tier, or postseason model. Read this before re-enabling MADNESS.
