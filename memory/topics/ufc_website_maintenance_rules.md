---
name: UFC Website Maintenance Rules
description: Mandatory 15-point checklist for reviewing/updating mmalogic.com. Every screenshot review and deploy must pass ALL items. Created after Claude missed 11 visible bugs across 5 screenshots on 2026-03-24.
type: feedback
---

# UFC Website Maintenance Rules — MANDATORY CHECKLIST

**Why:** On 2026-03-24, Claude said "no obvious bugs" while 11 bugs were visible. This checklist ensures every item is individually verified with specific values.

## The 15-Point Verification Checklist

### Landing Page (/)
1. **Combined P/L** — Must match registry sum of all 4 active bet types + parlay. Currently ~300.72u.
2. **Event count** — Must show 71+ (current NUM_BACKTEST_EVENTS). NOT 25.
3. **4 bet type cards** — ML (green), Method (blue), Combo (amber), Parlay (yellow). NO Round card. All with non-zero W-L.
4. **ROI badge** — ROI% = combined_pnl / total_bets * 100. Must be plausible (15-35% range).

### Picks Page (/picks)
5. **Confidence display** — Shows raw diff value (e.g., "2.23 diff"), NOT percentage (NOT "226% conf").
6. **R1 KO gating** — Round/Combo bets ONLY on KO R1 predictions. KO R2, KO R3, SUB Rx = NO round bet.
7. **Combo bets shown** — Every R1 KO fight shows a combo bet row (CMB tag).
8. **SUB gating** — NO "by SUB" when SUB gating is active.
9. **Both parlays** — HC parlay AND High ROI parlay (if algorithm generates both).

### Event Detail (History expanded)
10. **Fighter loss = -1u everywhere** — Lost fighter + odds existed → X -1.00u in ML, Method, Round, Combo.
11. **Fighter win = odds-based payout** — Won prop bet → actual payout at odds, not "✓ —".
12. **Parlay row** — Every event shows parlay with legs, odds, P/L.
13. **Summary header all 5 types** — ML, M, R, C, P + combined.

### Admin/Optimizer
14. **Current values populated** — NO "—" for params in constants.json.
15. **All param categories** — Includes Advanced Features and System Integration.

## The 19 Display Rules

### Core Betting Rules (from spec)
1. Fighter loss = -1u on EVERY placed bet (up to -4u combined)
2. Wins pay at REAL odds (positive: stake×odds/100; negative: stake×100/|odds|)
3. ALL prop bets require ML win
4. Combo wins require ALL 3 correct (ML + method + round)
5. No bet without odds (null odds = "—", not scored)
6. No round/combo on DEC predictions
7. Variable bet count per fight (1-4)
8. Method = exact method match (KO/TKO grouped)
9. Method and Round scored INDEPENDENTLY
10. Parlay is 5th bet type (per event, not per fight)
11. Total bets = sum of fight bets + parlays
12. W-L counts must balance

### Frontend Display Rules (learned from bugs)
13. R1 KO gating: round/combo bets ONLY for KO R1 predictions
14. SUB gating: skip SUB method bets when sub_sc < threshold
15. Confidence = raw differential (0.14-3.0+), NOT a percentage
16. Registry totals must include ALL 5 bet types with wins/losses/pnl
17. Data must be synced from ufc-predict/webapp/ → root webapp/ before every build
18. algorithm_stats.json must include parlay_pnl
19. EventBetsDropdown computes missing P/L from odds when data is incomplete (frontend safety net)
20. **Losses NEVER need odds** — a loss is always -1u regardless of whether odds exist. Only WINS need odds to compute payout. If safePnl/registry has null pnl + null odds + correct=false, the answer is -1u, not null.
21. **4 active bet types in every summary (Round REMOVED v11.18.5)** — EventSlideshow, LastWeekPicks, EventBetsDropdown, and any component showing event summaries MUST include ML, Method, Combo, AND Parlay. NO Round column/chip/card. Round bets permanently disabled since v11.14.4.
22. **NEVER accept missing odds (PERMANENT, NON-NEGOTIABLE).** If ANY fight in the registry has null method_odds, round_odds, or combo_odds — IMMEDIATELY run the prop odds scraper to backfill. Do NOT display "—" for wins, do NOT skip to display fixes, do NOT accept __NO_PROPS__. The FIRST action when encountering missing odds is to scrape them. This rule overrides all other priorities. Missing odds = broken data = wrong P/L = unacceptable.
23. **R1 KO gating in registry data.** The backtester sometimes sets round_correct=False and combo_correct=False for non-R1-KO predictions. These should be NULL (no bet placed). When reviewing registry data: if predicted_method != "KO" OR predicted_round != 1, then round_correct and combo_correct MUST be null. The _correct field means "bet was placed and this was the outcome" — null means "no bet placed."
24. **KO R1 losses need round AND combo -1u.** When a KO R1 prediction is wrong (fighter won by DEC, or fighter lost), BOTH round_pnl AND combo_pnl should be -1.0u — not null. Null means no bet placed. The bet WAS placed (KO R1), it just lost.
25. **ALWAYS re-run the backtester instead of manual registry patches (PERMANENT).** When event tables show wrong data (missing -1u, gated bets displayed, wrong _correct fields), the fix is: `UFC_BACKTEST_MODE=1 UFC_CACHE_ONLY=1 python3 UFC_Alg_v4_fast_2026.py`. Then aggregate parlay totals from event-level data (backtester doesn't include them in totals). Then sync to webapp/frontend/public/data/. NEVER manually patch individual bouts across the whole registry — it diverges from the backtester's logic and produces wrong totals. The backtester has R1 KO gating, SUB gating, and correct scoring built in. Manual patches are only for freshly-scraped odds on specific events.
26. **Parlays must appear in event tables.** EventBetsDropdown already renders parlay rows when parlay data exists in the event. But registryData.computeLatestFightsFromRegistry must INCLUDE ev.parlay in the returned object, and LastWeekPicks must destructure it.
27. **"Apply & Regenerate Picks" button WORKS (verified 2026-03-26).** Full chain: AdminAlgorithm saves constants to Firestore → CF function dispatches `run-predictions` to GitHub Actions → GH Actions syncs constants from Firestore (UFC_SYNC_CONSTANTS=1) → runs algorithm → ingests predictions back to site + commits to GitHub. Required secrets: CF has GITHUB_TOKEN + INGEST_SECRET, GH has GOOGLE_APPLICATION_CREDENTIALS_JSON + INGEST_SECRET. Takes ~1-2 minutes async. The UI shows "run started" message correctly.
29. **AdminBacktest.jsx must match EventBetsDropdown format (PERMANENT).** The backtest tab in admin was showing an outdated table: only ML/Method/Round columns (no Combo), no Parlay row, no safePnl for computing losses, and combined_pnl only summed 3 types. Fixed 2026-03-26 to match EventBetsDropdown: all 5 columns, Parlay row, safePnl, all 5 types in combined. When ANY table component is updated, check ALL table components: EventBetsDropdown, AdminBacktest BoutRow, EventSlideshow EventCard, LastWeekPicks, HistoryPage. They must ALL show the same bet types.
30. **Derived data files auto-regenerate (PERMANENT, v11.18.5).** hero_stats.json and algorithm_stats.json are now auto-regenerated by fix_registry_placed_flags.py after any registry write. getHeroStats() always computes from registry at runtime (never reads hero_stats.json). After ANY registry modification, verify all data sources agree: `python3 -c "import json; [print(f'{n}: {json.load(open(p)).get(\"combined_pnl\", json.load(open(p)).get(\"totals\",{}).get(\"combined\"))}u') for n,p in [('hero',  'webapp/frontend/public/data/hero_stats.json'), ('algo', 'webapp/frontend/public/data/algorithm_stats.json'), ('reg', 'ufc_profit_registry.json')]]"`
31. **6-step site edit protocol (MANDATORY, user rule 2026-04-01).** Every site edit must: (1) automate prevention, (2) apply universally, (3) update agent knowledge, (4) bump version, (5) sync GitHub, (6) deploy and verify.
28. **When odds are missing from prediction_output.json** (pick_ml=None), the algorithm's BFO scraper couldn't find the event page. BFO may list the event under a different name (e.g., "UFC Seattle" vs "UFC Fight Night: Adesanya vs. Pyfer"). Fix: manually add ML odds to ufc_odds_cache.json with correct key format, then re-run predictions. Or wait for the Wednesday auto-refresh cron to catch new odds.

## HOW TO VERIFY (Not Optional)

1. **Do NOT glance and say "looks correct."** Check each item individually.
2. **State specific values** — "ML shows 303W-113L, +83.01u" not "ML looks fine"
3. **Check at least 2 fight cards in detail** — verify gating, combo presence
4. **Check at least 1 event detail page** — verify every bout's scoring
5. **If you can't check something**, say "UNABLE TO VERIFY: [item]"

## Bug History (2026-03-24/25)

| Bug | Root Cause | Rule Violated |
|-----|-----------|---------------|
| 260% confidence | pick.diff * 100 displayed as % | Rule 15 |
| Navajo R2 round bet | No R1 KO gating in FightCard | Rule 13 |
| No combo bets on cards | Combo row never added | Rule 7 (checklist) |
| Only 1 parlay | Algorithm only generated HC, no high-ROI | Rule 9 (checklist) |
| Optimizer Current = "—" | Firestore missing params, no fallback | Rule 14 (checklist) |
| Prop losses show "—" | Registry null pnl for losses with odds | Rule 1 |
| Prop wins show "—" | Registry null pnl for wins with odds | Rule 2 |
| No parlay in event detail | Parlay data present but not always rendered | Rule 12 (checklist) |
| Summary header missing C, P | Only ML, M, R shown | Rule 13 (checklist) |
| Landing shows 25 events | Firestore stale data overriding static JSON | Rule 2 (checklist) |
| Parlay 0W-0L | Registry totals missing parlay fields | Rule 16 |
| Method "✓ —" on wins | safePnl returned null on null odds BEFORE checking correctness | Rule 2 |
| Method "✗ —" on losses | safePnl exited early on null odds, skipping -1u loss | Rule 1 |
| Latest Event missing Combo/Parlay cards | EventSlideshow grid only had 3 cols (ML/Method/Round) | Rule 13 |
| Latest Event missing parlay data | computeLatestFightsFromRegistry didn't include ev.parlay | Rule 10 |
| Method 0W-0L when bets placed | Backtester records method_pnl=null when method_odds=null, even for losses | Rule 1 |
