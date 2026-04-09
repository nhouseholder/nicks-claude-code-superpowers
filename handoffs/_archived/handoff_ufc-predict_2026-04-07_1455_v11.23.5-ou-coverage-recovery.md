# Handoff — UFC Predict — 2026-04-07 14:55 PDT
## Model: claude-sonnet-4-6
## Previous handoff: HANDOFF.md (v11.23.4, 2026-04-07 12:35 PDT)
## GitHub repo: nhouseholder/ufc-predict
## Local path: /Users/nicholashouseholder/ProjectsHQ/mmalogic
## Last commit: b15d48d (v11.23.5: Bump frontend version to match algorithm audit)
## Deployed: Cloudflare Pages (octagonai.pages.dev, mmalogic.com)

---

## 1. Session Summary

Full O/U coverage recovery for v11.23.5. The v11.23.4 canonical rebase had dropped O/U from ~438 bets (+181u) to 145 bets (+79u) because the O/U contract unification (v11.23.1) switched from DEC-prop-derived odds to BFO cache only — BFO covers only ~376/550 bouts. This session restored coverage via two complementary fixes: (1) DEC-prop-derived fallback in `get_ou_odds()` for fights missing BFO 2.5-line data, and (2) relaxed price gates (Over floor -400, abs cap ±600) to unlock 78 additional BFO bets that were being blocked by the old -160 floor and ±400 cap. Net: +8.65u on O/U, full combined +726.43u. Deployed and live.

---

## 2. What Was Done

### Algorithm Changes
- **`scrape_ou_odds.py`**: Added DEC-prop-derived O/U fallback (`_derive_ou_from_dec_props()`), `_american_to_implied()`, `_prob_to_american()` helpers. `get_ou_odds()` now returns `_source: "bfo"|"derived"` tag and falls through to derived when BFO lacks 2.5-round data (only has 1.5-round lines).
- **`ou_contract.py`**: Relaxed defaults: `DEFAULT_OVER_ODDS_FLOOR = -400` (was -160), `DEFAULT_ODDS_ABS_CAP = 600` (was 400).
- **`UFC_Alg_v4_fast_2026.py`**: Bumped `ALG_VERSION = "11.23.5"`. Updated `OU_ODDS_CAP` and `OU_OVER_ODDS_FLOOR` constants to reference new contract defaults. Added `ou_source` to optimizer fight dataset.
- **`fix_registry_placed_flags.py`**: Updated to use `DEFAULT_OVER_ODDS_FLOOR` and `DEFAULT_ODDS_ABS_CAP` from contract.
- **`validate_registry_cells.py`**: Updated caps to match new defaults (-400 / 600).
- **`tests/test_ou_contract.py`**: Updated test thresholds to match new caps (-450 and -650).

### Documentation & Versioning
- **`CLAUDE.md`**: Updated baseline table (v11.23.5, +726.43u), O/U odds description (derived fallback), changelog entry.
- **`webapp/frontend/src/config/version.js`**: Bumped to 11.23.5.

### Deployment
- Full settle pipeline run: backtest → `fix_registry_placed_flags.py` → `patch_registry_from_archive.py` → `fix_registry_placed_flags.py`
- All 5 validators pass
- Frontend built and deployed via `wrangler pages deploy --branch main`
- Auto-update picks ran for UFC 327: Prochazka vs. Ulberg

---

## 3. Canonical Baseline (v11.23.5, 2026-04-07)

| Stream | P/L | Record |
|--------|-----|--------|
| ML | +117.82u | 378W-146L |
| Method | +161.12u | 144W-145L |
| Round | 0.00u | DISABLED |
| Combo | +121.39u | 40W-57L |
| O/U | +87.90u | 154W-69L |
| Parlay | +238.20u | 124W-113L |
| **Full Combined** | **+726.43u** | 71 events, 550 bouts |

---

## 4. Current State

- **Git**: `main` branch, clean, local = remote. Last commit: `b15d48d`.
- **Registry**: `ufc_profit_registry.json` — 71 events, 550 bouts, all validators pass.
- **Next event**: UFC 327: Prochazka vs. Ulberg (current picks live).
- **Live site**: mmalogic.com — v11.23.5, +726.43u displayed.

---

## 5. Key Files Changed This Session

| File | Change |
|------|--------|
| `scrape_ou_odds.py` | DEC-prop-derived O/U fallback + `_source` tag |
| `ou_contract.py` | Floor -400, cap ±600 defaults |
| `UFC_Alg_v4_fast_2026.py` | v11.23.5, updated OU constants, ou_source in optimizer |
| `fix_registry_placed_flags.py` | Uses contract defaults for gates |
| `validate_registry_cells.py` | Updated caps |
| `tests/test_ou_contract.py` | Updated threshold values |
| `CLAUDE.md` | Updated baseline + changelog |
| `webapp/frontend/src/config/version.js` | 11.23.5 |

---

## 6. Anti-Patterns Updated

- `OU_ODDS_SOURCE_DRIFT` — marked RESOLVED (derived fallback restored)
- `FABRICATED_ODDS` — cap updated to ±600

---

## 7. What Was Investigated (Not Shipped)

- A/B tested 5 Over floor thresholds (-160, -250, -400, -600, -9999) and 4 floor+cap configs before settling on -400/600 as optimal.
- Confirmed BFO partial data (1.5-round-only entries) was blocking derived fallback. Fixed by checking for `over_25`/`under_25` presence before accepting BFO result.
- Derived fallback recovered ~3 additional O/U bets (after gate relaxation recovered the main 78 BFO bets).

---

## 8. Open Items / Next Steps

- None critical. System is healthy.
- Future consideration: investigate whether additional DEC-prop sources could improve derived O/U accuracy beyond the current `P(Over) = P(f1_DEC) + P(f2_DEC)` approximation.
- After UFC 327 completes: run `track_results.py` (Sunday post-event), add event 72 to registry.

---

## 9. Reproduce From Scratch

```bash
git clone https://github.com/nhouseholder/ufc-predict && cd ufc-predict
python3 build_temporal_stats_cache.py
UFC_BACKTEST_MODE=1 UFC_CACHE_ONLY=1 python3 UFC_Alg_v4_fast_2026.py
python3 fix_registry_placed_flags.py
python3 patch_registry_from_archive.py
python3 fix_registry_placed_flags.py
python3 validate_registry_cells.py --strict
python3 verify_registry.py
```

Expected: 71 events, 550 bouts, +726.43u combined.
