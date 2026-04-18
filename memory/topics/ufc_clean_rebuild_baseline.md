---
name: UFC Clean Rebuild Baseline
description: Last known-good v11.42.0 canonical baseline for mmalogic.com after Gate2 KO round dec threshold tightening
type: project
---

# v11.42.0 Baseline — 2026-04-18

**Registry:** 100 events, 780 bouts
**Full Combined P/L:** +1982.68u

## Stream-level (per algorithm_stats.json on live site)

| Stream | P/L | Record |
|--------|-----|--------|
| ML | +180.15u | 527W-223L |
| Method | +189.76u | 211W-244L |
| Round | 0.00u (DISABLED) | 0W-0L |
| Combo | +110.32u | 43W-84L |
| O/U | +133.68u | 247W-97L |
| Parlay (all 10 types) | +1368.77u | 175W-306L |
| **Full Combined** | **+1982.68u** | 1203W-954L |

## v11.42.0 Release Highlights

- Gate2 KO round compound threshold tightened: dec_sc max 0.33 → 0.26
- Releases bouts with dec_sc 0.26–0.33 (AND sub_sc ≤ 0.10) back to R2
- Pre-compute confirmed 6 actual-R2 outcomes in that range
- Combo +93.02u → +110.32u (+17.30u direct lift)
- Full combined +1972.38u → +1982.68u (+10.30u)

## v11.41.0 (same session)

- Tightened systems pruning gates
- Bumped SYSTEM_SCORE_WEIGHT from 0.05 to 0.25

## Deploy State

- Algorithm: `UFC_Alg_v4_fast_2026.py` — `ALG_VERSION = "11.42.0"`
- Frontend marker: `webapp/frontend/src/config/version.js` → v11.42.0 (2026-04-18)
- Live site: https://www.mmalogic.com ✓ v11.42.0
- Commits on main: `e984347` (v11.42.0 code) → `7e0e174` (data sync)
- Validator: 5/5 checks pass, 0 errors, 0 warnings (780 bouts, 100 events)

## 3-File Reconciliation

hero_stats.json = algorithm_stats.json = registry = **+1982.68u** ✓

## How to Apply

- When a user asks for the current baseline, quote +1982.68u / 100 events / 780 bouts.
- If a session starts and these numbers don't match the site's live `algorithm_stats.json`, investigate drift before trusting either source.
- Kill criteria for future experiments: full combined must stay ≥ +1982.68u. Drop > 10u → revert.
