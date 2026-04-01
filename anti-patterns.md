# Anti-Patterns — Known Failures & Working Fixes

> Claude checks this before debugging to avoid repeating known-bad approaches.
> Pruned 2026-04-01: kept recurring behavioral patterns + permanent rules. One-time bug fixes removed (the fix is in the code).
> Last updated: 2026-04-01

## UFC — Stale Derived Data Files (STALE_HERO_STATS) — 2026-04-01
- **Pattern**: Registry is updated (via fix_registry_placed_flags.py or manual sweep) but hero_stats.json and algorithm_stats.json are NOT regenerated. Website shows inflated/wrong numbers (+327.99u instead of +300.72u).
- **Root cause**: fix_registry_placed_flags.py wrote the registry but didn't trigger the data pipeline (sync_and_deploy.py). hero_stats.json was a pre-baked snapshot that went stale.
- **Fix (permanent, 2 layers)**:
  1. Frontend `getHeroStats()` now always computes from registry via `computeSummaryFromRegistry()` — never reads hero_stats.json
  2. `fix_registry_placed_flags.py` auto-imports and runs `sync_and_deploy.py`'s regeneration after any registry write
- **Applies when**: Any script modifies ufc_profit_registry.json outside of sync_and_deploy.py. Always verify hero_stats.json and algorithm_stats.json match registry totals after registry modifications.

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
