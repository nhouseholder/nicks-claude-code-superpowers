# Anti-Patterns — Known Failures & Working Fixes

> Claude checks this before debugging to avoid repeating known-bad approaches.
> Pruned 2026-04-01: kept recurring behavioral patterns + permanent rules. One-time bug fixes removed (the fix is in the code).
> Last updated: 2026-04-07

## UFC — O/U Odds Source Mismatch After Contract Unification (OU_ODDS_SOURCE_DRIFT) — 2026-04-07
- **Pattern**: O/U contract unification (v11.23.1, `ou_contract.py`) changed O/U odds source from DEC-prop-derived inline odds (broad coverage, ~438 bets) to BFO scraper cache only (~145 bets). `ufc_ou_odds_cache.json` has 618 flat entries (old derived odds) that are unreachable by `get_ou_odds()` because it requires event-nested keys. This caused a legitimate -104u absolute profit drop while per-bet ROI improved (42% → 55%).
- **Root cause**: `scrape_ou_odds.get_ou_odds(event_name, ...)` does `cache.get(event_name, {})` — only finds event-nested entries. Old derived odds stored as flat `"fighter_a|||fighter_b"` keys are orphaned.
- **Impact**: O/U bets dropped from 438 to 145 (-67%), absolute O/U P/L from +181u to +79u, full combined from +779u to +717u.
- **Status**: RESOLVED v11.23.5 (2026-04-07). DEC-prop-derived fallback added to `get_ou_odds()` + relaxed price gates (floor -400, cap ±600). Recovered 78 O/U bets (+8.65u). Remaining gap (~215 bets) is from prop cache name mismatches and missing DEC props.
- **Applies when**: Any O/U odds infrastructure change. Verify `get_ou_odds()` can reach all cache entry formats.

## UFC — Fabricated O/U Odds Fallback (FABRICATED_ODDS) — 2026-04-03
- **Pattern**: When real BFO O/U odds exceed the ±400 cap, the algorithm silently falls back to hardcoded -150 (Over) or -130 (Under) defaults. These fabricated odds produce inflated P/L (e.g., -150 pays +67% vs real -430 paying +23%).
- **Root cause**: Cap was designed for derived odds (which can hit -2000+) but also rejected legitimate real sportsbook odds at -430 to -500. Fallback to hardcoded default was silent — no indication that real odds were rejected.
- **Impact**: +5.93u inflated P/L from fake odds payouts on heavy-juice Over bets.
- **Fix**: When real BFO odds exist and exceed ±600, SKIP the bet entirely. Never fall back to fabricated defaults. Applies in both prediction path and backtest path. Cap raised from ±400 to ±600 in v11.23.5.
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

## ResearchAria — Systematic Review Prompt Overflow (REVIEW_PROMPT_OVERFLOW) — 2026-04-05
- **Pattern**: The 9-phase literature review UI falls back to "Failed. Please try again." because `/api/review/prompt` sends too much paper context to the AI provider.
- **Root cause**: The review route pulled up to 50 enriched papers and embedded long abstracts plus 2,000-character full-text excerpts into every phase request. Smaller AI-backed flows survived, but the systematic-review prompts exceeded practical context limits and all providers failed.
- **Fix**: Bound the review context before calling the AI. Prioritize papers marked `screening_decision = 'include'`, then highest-scoring remaining papers, cap total prompt context, and never embed raw full-text excerpts in the 9-phase review path. Also surface the backend error message in the UI instead of replacing it with a generic fallback.
- **Prevention rule**: Any multi-paper AI route must set an explicit context budget before calling the model. Never pass an unbounded library dump or raw full-text excerpts into a review-generation prompt.
- **Verification**: Run the bounded review context regression tests and confirm the review route compiles: `node --test --experimental-strip-types test/reviewContext.test.mjs` and `npx tsc --noEmit`.

## ResearchAria — Firebase Popup Hosted Init + Redirect Mismatch Trap (FIREBASE_GOOGLE_AUTH_TRAP) — 2026-04-05
- **Pattern**: Google sign-in breaks in two layers: the Firebase popup path requests `https://aria-research-app.firebaseapp.com/__/firebase/init.json` and gets a hosted 404 page because the Firebase Hosting auth domain has never been deployed, while a naive switch to `https://researcharia.com/__/auth/handler` triggers Google's `redirect_uri_mismatch` error because that redirect URI is not registered on the OAuth client.
- **Root cause**: I treated the popup break as a frontend auth-domain problem instead of checking whether the Firebase Hosting auth domain itself had ever been deployed. Without a deployed Hosting site, the reserved Firebase auth URLs are incomplete.
- **Fix**: Deploy a minimal Firebase Hosting site to `aria-research-app` so `__/firebase/init.json` exists again on `aria-research-app.firebaseapp.com`, keep Firebase `authDomain` on that hosted domain, and continue using Firebase `signInWithPopup`.
- **Flawed assumption**: I burned time on alternative Google auth flows before verifying that the Firebase auth domain itself was still just the default Hosting 404 site.
- **Prevention rule**: For Firebase popup auth failures, check `https://<project>.firebaseapp.com/__/firebase/init.json` first. If it returns a Hosting 404 page, deploy the Firebase Hosting site before rewriting app auth code.
- **Verification**: `curl -s https://aria-research-app.firebaseapp.com/__/firebase/init.json` must return JSON, and a popup probe against `researcharia.com` must no longer show `redirect_uri_mismatch` or a blocking init.json 404.

## BrewMap — Weak Review Flavor Evidence And Permissive Roast Filters (BREWMAP_FLAVOR_FILTER_DRIFT) — 2026-04-05
- **Pattern**: Review-derived flavor tags included one-off words that barely appeared in Yelp reviews, and the Light/Medium/Dark pill filter still showed shops with no roast data.
- **Root cause**: Flavor extraction treated any detected term in the combined review text as meaningful evidence, while the roast filter used a permissive predicate that allowed missing roast metadata to pass through an active roast filter.
- **Fix**: Require a flavor tag to appear in at least 2 separate reviews before it can become a review-derived tag, and fall back to AI flavor estimates when fewer than 2 review-backed tags remain. For roast filters, use explicit roast-bucket matching and exclude shops with no roast data when a roast filter is active.
- **Flawed assumption**: I assumed a single flavor mention across sparse reviews was enough to drive the UI, and that missing roast data should not narrow a positive roast filter.
- **Reasoning lesson**: When the UI claims a value is review-derived or filterable, require repeated evidence and use strict inclusion rules instead of permissive fallthroughs.
- **Applies when**: Extracting structured tags from sparse review text or building categorical filters on partial enrichment data.

## BrewMap — Mobile Scroll Blocked By Container Gesture Locking (BREWMAP_SCROLL_GESTURE_LOCK) — 2026-04-06
- **Pattern**: The site appears not to scroll on mobile because the bottom sheet and list areas ignore normal touch scrolling.
- **Root cause**: The entire mobile `.sidebar` was set to `touch-action:none`, and the global `touchmove` preventer only exempted a few descendants instead of treating the sidebar as a scrollable interaction region.
- **Fix**: Keep gesture locking only on the sheet handle, restore normal touch handling on the sidebar, and let the body-level touch blocker allow any touch interaction inside `.sidebar`, `.detail-panel`, `.city-search-results`, `#map`, and `.loading-overlay`.
- **Flawed assumption**: I treated the whole sheet like a drag surface instead of isolating drag behavior to the handle.
- **Prevention rule**: Never apply `touch-action:none` to an entire mobile container that also holds scrollable content. Restrict drag-only gesture locking to the explicit handle.
- **Verification**: On a mobile viewport, confirm the shop list and featured rails can scroll naturally while the sheet handle still drags the panel.

## NestWise — Portfolio Edit Rows Need Spinnerless Numeric Inputs And Inline Context Labels (NESTWISE_PORTFOLIO_EDIT_ROW_CLIPPING) — 2026-04-07
- **Project**: nestwisehq / dad-financial-planner
- **Page/Component**: `/portfolio` — `components/portfolio/holdings-table.tsx`, `components/portfolio/trade-form.tsx`, `components/portfolio/portfolio-grade.tsx`
- **Bug**: Native browser number steppers crowded the portfolio quantity input until the value was effectively hidden, inline edit cells changed meaning without labels, and the QORE distribution rendered as jammed strings like `61%A 39%B`.
- **Root cause**: Dense financial table inputs reused narrow columns and default browser numeric controls, while edit-mode cells repurposed existing headers without adding local context.
- **Carelessness type**: Didn't check actual rendered output in a cramped layout.
- **Fix**: Added a scoped `.input-no-spinner` utility for the affected portfolio number inputs, widened the inline edit fields slightly, labeled the edit cells as `Shares`, `Basis`, and `P/L`, and rendered QORE distribution values as separated badges.
- **Prevention rule**: In dense financial tables, never ship default browser number steppers or unlabeled edit-mode cells. If a cell changes meaning in edit mode, label it inside the cell and verify the value is readable at the actual table width.
- **Verification**: On `/portfolio`, inline holding edit must show the full quantity value, trade form numeric inputs must render without native Safari steppers, and the Portfolio Grade QORE buckets must render as distinct badges.

## WRONG_PROJECT_CWD — Running Domain Tasks in the Wrong Repo — 2026-04-09
- **Symptom**: Running backtests, edits, or deploys in the wrong project repo because cwd happened to be elsewhere when the task was requested.
- **Example**: User in `~/ProjectsHQ/superpowers/` asks "test H16 backtest" — UFC task, wrong repo, would have failed silently or worse, modified the wrong files.
- **Fix**: `project-domain-guard.py` hook warns on domain/cwd mismatch before Claude acts. If you see a PROJECT MISMATCH warning, STOP and confirm with user which repo to use.
- **Rule**: Never assume cwd is the right directory for a task. If the task has domain-specific keywords, verify cwd matches the project those keywords belong to.
- **Prevention**: Domain map lives at `~/.claude/project-domains.json`. Update it when adding new projects or domain terms.

## MATCHUP_OVER_ANTI_SIGNALS — NBA prop over systems that backtest negative — 2026-04-10 (courtside-ai)
- **Context**: NBA prop matchup sweep, part of v12.48.2 backtest (26 hypotheses, 36 accepted). Two "over" systems that sound intuitive but are inverse signals.
- **Anti-signal 1 — `BLK_OVER_HOT_vs_SOFT`**: 44.9% win / **−14.2% ROI** / N=280. Logic sounds right ("hot blocker vs soft block defense") but "soft block defense" actually means the opponent has tall shot-blockers who absorb shots — which hurts your blocker's stat line, not helps it. Counterintuitive but strong.
- **Anti-signal 2 — `3PM_OVER_SIEVE`**: 46.1% win / **−11.9% ROI** / N=355. Logic sounds right ("fade any player vs team that allows many 3s") but team-level 3PA volume does not transfer to individual player 3PM. Shooters still need the ball.
- **Rule**: Never build these systems into production. Never flip the sign and build them either — always run a fresh full walk-forward backtest before building any matchup system.
- **Source**: `/Users/nicholashouseholder/ProjectsHQ/courtside-ai/scripts/analysis/props_matchup_sweep_summary.md`
- **Prevention**: When porting backtest winners to production, also explicitly record the losers with their N and ROI so they can't sneak back in via "hey this sounds like it should work" intuition.

## PLAN_AUTO_SWITCH_IMPOSSIBLE — Hook-based model switching from Opus to Sonnet — 2026-04-10
- **Context**: Claude Code Desktop app on macOS. User wanted "when I approve a plan, auto-switch to Sonnet before execution" for ~40-60% token savings on mechanical plan execution.
- **Failed approach**: PreToolUse / UserPromptSubmit hooks that (a) write `claude-sonnet-4-6` to `~/.claude/settings.json` when a plan is approved or "go" is typed, or (b) read `settings.json` to check "am I already on Sonnet?" and branch behavior. Tried in 10 commits from 2026-04-07 through 2026-04-10.
- **Why it failed**: **The running session's model is locked at startup.** Writes to `settings.json` only affect NEW sessions, not the currently-running one. Additionally, the Desktop app's model dropdown is the real source of truth and does NOT reliably sync back to settings.json — so the file goes stale and tells lies ("model: sonnet" while the session is actually running Opus). Every hook branch that read settings.json to detect the running model was reading a stale value. One commit (`e37d4b6`) wrote Sonnet to settings.json from ExitPlanMode; a later commit (`08438d8`) discovered this was removing the guard immediately because the guard then saw "model=sonnet" and allowed Opus to execute freely. Classic self-inflicted bug chain from workarounds that couldn't exist cleanly.
- **Working fix**: **Manual switch only.** The `plan-mode-enforcer.py` hook now (1) detects plan intent + writes a `.plan-guard-active` file, (2) injects a mandatory user-facing message saying "switch to Sonnet then type `go`", (3) on `go`, removes the guard and injects execution instructions WITHOUT claiming to know the model. `plan-execution-guard.py` blocks Edit/Write unconditionally while the guard exists — no model check. Trust the user to have switched; the hook cannot verify it and must not pretend to.
- **Flawed assumption**: API/behavior assumption — believed `settings.json` writes propagated to the running session, and that settings.json would stay in sync with the Desktop UI dropdown. Both false.
- **Reasoning lesson**: *If a hook cannot detect a piece of state reliably, it must not pretend to know it.* Reading a stale settings.json and interpolating that value into user-facing messages ("PLAN EXECUTION MODE — running on claude-sonnet-4-6") produces lies that damage user trust faster than the feature ever delivered value. Honest "I don't know which model you're on, here's the plan, go execute it" beats clever-but-wrong auto-detection every time.
- **Secondary lesson**: Substring matching on user prompts ("execute plan" inside "why does execute plans fail") triggered false plan-execution injections. All GO detection must be start-anchored regex + length-guarded. Never substring-match on user prose.
- **Applies when**: Any future attempt to have a Claude Code hook (a) change the active model mid-session, (b) inject `/model` slash commands into the CLI, (c) read settings.json to infer the running model, (d) substring-match user prompts for action signals. Don't.
- **History**: 10 commits tried variations. Zero worked. Session transcript `45c88614-7853-4083-a404-12faa23a963a` (superpowers project, 2026-04-10) documents the final root-cause diagnosis and remediation.
