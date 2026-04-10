# Anti-Patterns — Known Failures & Working Fixes

> Claude checks this before debugging to avoid repeating known-bad approaches.
> Pruned 2026-04-01: kept recurring behavioral patterns + permanent rules. One-time bug fixes removed (the fix is in the code).
> Last updated: 2026-04-10

## UFC — Parlay With Correlated Same-Fighter Props (PARLAY_SAME_FIGHTER_CORRELATED) — 2026-04-10
- **Pattern**: Parlay builder selects two props on the SAME fighter in the SAME fight as legs of one parlay (e.g., "Fighter A by KO" + "Fighter A KO R1"). No sportsbook on any platform allows this — correlated same-fighter props are rejected at the slip.
- **When it happened**: v11.27.0 (Hypothesis 15 v2, 2026-04-09) shipped HM3 with a "correlated legs allowed" gate that bucketed legs by `fight_id` with a `>= 2` counter but never checked fighter identity. UFC 327 produced Murzakanov KO R2 + **Hokit KO R1 + Hokit by KO**. The latter two couldn't be placed.
- **Why the backtest number lied**: V3's "+875.58u" advantage over V2's "+709.01u" was partly paper P/L — 3 of V3's 6 winning parlays relied on same-fight correlated legs that would be rejected by any book (Rodriguez KO R1 + Under 2.5 same fight; Leroy KO + Over 2.5 same fight; De Ridder SUB + Over 2.5 same fight). A backtest that counts un-placeable parlays as wins overstates the strategy. The realizable edge was ≤ V2's +709.01u.
- **Root cause**: Treating fight_id as a dedup bucket (allowing 2 legs per fight) without asserting distinct fighters/markets. The dedup key must ensure every leg is independently placeable as a parlay under sportsbook correlation rules.
- **Permanent rule**: **Parlay construction must enforce 1 leg per fight** unless a rigorous check is implemented for (a) distinct fighters AND (b) independent (non-correlated) market types, verified against the target sportsbook's correlation rules. The naive "2 legs per fight OK" rule is broken by construction.
- **Detection**: Any parlay leg generator that uses a fight-level bucket with count >= 2 must be audited. Grep: `_fight_counts\.get|_live_counts\.get` in UFC_Alg_v4_fast_2026.py — gate must be `>= 1`.
- **Fix applied**: v11.27.2 reverted both paths (backtest `_build_registry_event_entry` + live prediction path) to `>= 1` per fight. Canonical baseline dropped +1631.07u → ~+1464.50u, which is the correct realizable number.
- **Validation check for new parlay builders**: For every output parlay, assert `len(set(fighter(leg) for leg in parlay.legs)) == len(parlay.legs)` AND `len(set(fight_id(leg) for leg in parlay.legs)) == len(parlay.legs)` before claiming a P/L number.
- **Files**: `UFC_Alg_v4_fast_2026.py` (dual-path fix)

## React — Whole-Site Black Screen From One Render Crash (REACT_BLACK_SCREEN_NO_BOUNDARY) — 2026-04-10
- **Pattern**: A single component throws during render (e.g. accessing `.roi` on an undefined nested key), React has no ErrorBoundary, so the entire tree unmounts and `#root` becomes empty. Users see a black/blank page that does NOT recover on refresh. Pipeline success logs are misleading because the backend succeeded — the crash is in the frontend at render time.
- **Why it keeps happening**: Data generators (daily pipelines) produce JSON whose shape can shrink when categories drop below min-sample thresholds (e.g. `tier_breakdown` only contains PLATINUM when DIAMOND/GOLD have too few picks). React code that *destructures and dot-accesses* those keys crashes on the first undefined. Two incidents so far: SeasonCard key mismatch (2026-03) and NHL tier_breakdown (2026-04-10).
- **Root cause (generalized)**: The frontend trusts that the data contract is stable. It isn't — daily regeneration re-shapes it whenever category counts fluctuate. Single crash + no boundary = full-site outage.
- **Fix (permanent, 2 layers — now in place for diamond-predictions)**:
  1. **Defense in depth**: `main.jsx` wraps `<App />` in `RootErrorBoundary` (class component with `getDerivedStateFromError` + `componentDidCatch`). A render crash now shows a recoverable error card, never a blank root. **This is the non-negotiable fix. Any new Vite/React site in Projects must have an ErrorBoundary at `main.jsx`/root mount from day one.**
  2. **Root cause (data-driven rendering)**: Replaced the crashing hardcoded legend `tier_breakdown.DIAMOND.roi / .PLATINUM.roi / .GOLD.roi` with `tierChartData.map(t => ...)` so the legend iterates only existing keys. Applies generally: when rendering from a data object whose keys may be absent, iterate via `Object.entries` or a pre-built array — never dot-access a hardcoded subkey of a variable-shape object.
- **Detection / how to catch it earlier**: 
  1. If a user reports "site down / black screen that doesn't resolve on refresh" — it is almost certainly a React render crash, NOT a deploy/DNS/cache issue. Skip purging Cloudflare. Go straight to: (a) open the live site in Chrome MCP, (b) `read_console_messages onlyErrors:true`, (c) read the TypeError, (d) grep the source for the undefined key. Should be <5 minutes to root cause.
  2. When writing React that pulls from a freshly-regenerated JSON file, **grep the current data file** for the keys you're about to dot-access. If any key might be absent, use `?.` or iterate.
- **Applies when**: Any React code in any Projects site (diamond-predictions, mmalogic, courtside-ai, nestwisehq, mystrainai, enhancedhealth, researcharia). All of them need an ErrorBoundary at root if they don't have one. Audit any project where a daily pipeline regenerates JSON consumed by the React app.

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

## MyStrainAI — useRatings TDZ Crash from ESLint exhaustive-deps (ESLINT_TDZ) — 2026-04-07
- **Pattern**: ESLint auto-fix added `_computeLocalProfile` to `rateStrain`'s useCallback dependency array. But `_computeLocalProfile` was a `const` declared 37 lines AFTER `rateStrain`. Dependency arrays are evaluated immediately (not lazily), so accessing the `const` before its declaration triggers JavaScript's Temporal Dead Zone → `ReferenceError: Cannot access 'w' before initialization` in minified bundles.
- **Root cause**: Commit `736dd2d` lint fix changed dep array from `[userId, ratings]` to `[_computeLocalProfile, ratings, userId]` without checking declaration order.
- **Fix**: Move `_computeLocalProfile` declaration (entire useCallback block) BEFORE `rateStrain` in `useRatings.js`. Added code comment warning about TDZ.
- **Diagnosis key**: Chrome MCP tools captured the stack trace pointing to `useRatings-B3X3Q6P1.js:1:2024`. Reading the minified bundle showed `const v = useCallback(... [w, o, a])` before `const w = useCallback(...)`.
- **Applies when**: Any ESLint exhaustive-deps auto-fix. Always check that added dependencies are declared BEFORE the hook that references them. `const`/`let` are not hoisted like `function` declarations.

## MyStrainAI — Cloudflare Pages _middleware.js must process all requests (CF_MIDDLEWARE_ASSETS) — 2026-04-07
- **Pattern**: Attempted to skip non-API routes in `_middleware.js` to avoid wrapping static assets in `new Response()`. Result: `_redirects` catch-all (`/*  /index.html  200`) intercepted JS asset requests and served HTML instead of JavaScript.
- **Root cause**: Cloudflare Pages Functions middleware participates in the asset serving chain. When middleware returns `context.next()` for non-API paths, it still correctly routes to static assets. But when you skip middleware entirely for some paths, the `_redirects` catch-all takes priority, serving `index.html` for all paths including `/assets/*.js`.
- **Fix**: Keep middleware processing ALL requests. The `new Response(response.body, response)` wrapper is necessary for static assets to be served correctly.
- **Applies when**: Modifying Cloudflare Pages `_middleware.js`. Never exclude routes — the middleware must call `context.next()` and wrap the response for all paths.

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

## UFC — Live Tracker Scoring Gap (LIVE_TRACKER_SCORING_GAP) — 2026-04-07
- **Pattern**: `scoreFight()` in LiveTrackerPage.jsx only scored ML, Method, and Combo. O/U scoring was completely missing, and method bets had no gating (scored as placed/lost even when no method odds existed). Live-tracked events showed wrong O/U results and phantom method losses.
- **Root cause**: `scoreFight()` was written before O/U bets were added (v11.20.4) and never updated. Method gating was never implemented in the frontend — the Python `track_results.py` has it but the JS function didn't.
- **Fix**: Added O/U scoring (Over: round >= 3; Under: round <= 2 with KO/TKO/SUB finish), method gating (check method odds exist before scoring), and `*_placed` flags to `scoreFight()`. Also fixed Scoreboard to show O/U instead of Round.
- **Rule**: `scoreFight()` in LiveTrackerPage.jsx MUST mirror `track_results.py` scoring logic for ALL bet types. When a new bet type is added to the algorithm, it must be added to BOTH scoring paths.
- **Applies when**: Any new bet type added, any scoring rule change, any Live Tracker modification.

## UFC — Ghost X Bug Prevention
- Always use `*_placed` flags, never infer bet placement from `*_correct !== null`.
- Run `python3 validate_registry_cells.py --strict` after any registry modification.

## UFC — Round Bet Is INDEPENDENT of Method
- Round and method are separate bets. Fighter loss = ALL prop bets lose. SUB gating stays.
- See EVENT_TABLE_SPEC.md for canonical scoring rules.

## UFC — Hypothesis Testing Data Format Traps (HYPOTHESIS_DATA_TRAPS) — 2026-04-08
- **Pattern 1**: `fight_history` in `ufc_backtest_registry.json` uses `'WIN'`/`'LOSS'`, NOT `'W'`/`'L'`. Writing `result not in ('W', 'L')` causes zero activations with no error — silent failure.
- **Pattern 2**: File imports `from datetime import datetime` — so `datetime` is the CLASS, not the module. `datetime.date.fromisoformat()` fails with AttributeError. Correct pattern: `datetime.strptime(date_str, "%Y-%m-%d").date()`.
- **Pattern 3**: Baseline from registry totals (e.g. 745.78u) diverges from fresh backtest run (770.51u). Always establish baseline from a FRESH clean run, never from file reads. Incremental registry totals are stale.
- **Pattern 4**: Backtest overwrites production data files. Must `git restore` ALL data files between coefficient sweep runs or results are confounded.
- **Applies when**: Writing ANY new function in `UFC_Alg_v4_fast_2026.py`. Check data format with `python3 -c` BEFORE writing code. Check imports at top of file BEFORE using stdlib functions.

## Build — Node 25 Rollup Deadlock
- Node 25 + Rollup causes hanging builds. Use `NODE_OPTIONS=--max-old-space-size=4096` or downgrade to Node 22.

## General — Deploy Without GitHub Push (DEPLOY_WITHOUT_PUSH) — 2026-04-01
- **Pattern**: `wrangler pages deploy dist/` runs successfully, version goes live, but source was never committed/pushed to GitHub. Subsequent sessions see stale code, can't review changes, and source is effectively lost in the minified CDN bundles.
- **Root cause**: Previous sessions deployed to Cloudflare Pages directly without committing to git first. 10 versions (v5.168–v5.177 of MyStrainAI) were lost and had to be reverse-engineered from minified production JS.
- **Fix**: ALWAYS commit + push BEFORE deploying. Mandatory sequence: build → commit → push → deploy → verify. Never use `wrangler pages deploy` without a clean git state and pushed commit.
- **Applies when**: Any Cloudflare Pages deploy, any version bump, any `wrangler` command. Check `git status` before deploying — if there are uncommitted changes, commit and push first.

## ResumeForge — PDF Upload Spinner From CDN Worker + Missing Finalizer (PDF_WORKER_SPINNER_TRAP) — 2026-04-08
- **Pattern**: Uploading a PDF leaves the builder stuck on "Reading file" instead of reaching either the editor or an error state.
- **Root cause**: The client parser pointed PDF.js at a CDN-hosted `pdf.worker.min.mjs` URL that failed to load for the shipped version, and `BuilderPage.handleFile()` did not use `try/finally`, so extraction exceptions left `isParsing` true forever.
- **Fix**: Bundle the PDF worker locally via `new URL('pdfjs-dist/build/pdf.worker.min.mjs', import.meta.url)`, catch text-extraction failures in `parseResume()`, and always clear parsing state in `BuilderPage` with `finally`.
- **Prevention rule**: Never make the upload spinner depend on external worker/CDN availability, and never let async intake flows mutate loading state without a guaranteed cleanup path.
- **Verification**: Upload a PDF in browser automation and confirm the app does not remain on "Reading file"; it must either open the editor or show the intake error state.

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

## MyStrainAI — esbuild.drop:['console'] Breaks Library Error Handling (ESBUILD_DROP_CONSOLE) — 2026-04-07
- **Pattern**: Using `esbuild: { drop: ['console'] }` in vite.config.js removes ALL console methods including `console.error` and `console.warn`, which breaks libraries that use those methods in their internal error handling paths (FingerprintJS, Firebase Auth).
- **Root cause**: `esbuild.drop: ['console']` is equivalent to `delete console.*` — a blanket removal. On Brave browser with fingerprint protection enabled, FingerprintJS hits error paths that call `console.error` at startup. With the method removed, uninitialized variable propagation fails silently, causing a TDZ (Temporal Dead Zone) ReferenceError that crashes the app.
- **Symptom**: Mobile TDZ crash: `ReferenceError: Cannot access 'X' before initialization` on browsers with privacy protections (Brave, Firefox w/ Enhanced Tracking). Doesn't repro on Chrome/Safari.
- **First fix (wrong)**: Added `Cache-Control: no-cache` + ErrorBoundary stale-chunk reload — didn't fix root cause.
- **Correct fix (v5.217.7)**: Changed to `esbuild: { pure: ['console.log', 'console.debug'] }` — only strips non-essential calls, preserves `console.error`/`console.warn` for library error handling.
- **Rule**: NEVER use `esbuild.drop: ['console']` for production builds. Use `esbuild.pure` targeting only `console.log` and `console.debug`. `console.error` and `console.warn` are load-bearing for third-party libraries.
- **Verification**: Build with `esbuild.pure`, test on Brave with "Shields Up". FingerprintJS initialization must not throw.

## LUCIDE-REACT NEW IMPORT IN STRAIN CARD → TDZ CRASH
- **File**: `frontend/src/components/results/StrainCard.jsx`
- **Symptom**: `ReferenceError: Cannot access 'w' before initialization` — app crashes with ErrorBoundary on all pages that render StrainCard
- **Root cause**: Adding a NEW lucide-react icon (TrendingUp) as a static import to StrainCard changed the Vite chunk graph. The new chunk dependency altered module initialization order, triggering a TDZ in one of the shared chunks (`fmt` or `normalizeStrain` — both have module-scope `const w` declarations).
- **Fix**: Use an icon already imported in StrainCard (Star, Heart, MapPin, etc.) instead of introducing a new import. If a new icon is genuinely needed, use an inline SVG instead.
- **Rule**: Never add a new lucide-react icon import to StrainCard without rebuilding and testing in the browser (not just checking build success).
