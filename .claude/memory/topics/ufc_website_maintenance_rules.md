---
name: UFC Website Maintenance Rules
description: Mandatory 15-point checklist for reviewing/updating mmalogic.com. Every screenshot review and deploy must pass ALL items. Created after Claude missed 11 visible bugs across 5 screenshots on 2026-03-24.
type: feedback
---

# UFC Website Maintenance Rules — MANDATORY CHECKLIST

**Why:** On 2026-03-24, Claude said "no obvious bugs" while 11 bugs were visible. This checklist ensures every item is individually verified with specific values.

## The 15-Point Verification Checklist

### Landing Page (/)
1. **Combined P/L** — Must match registry sum of all 5 bet types. Currently ~281u.
2. **Event count** — Must show 71+ (current NUM_BACKTEST_EVENTS). NOT 25.
3. **4 bet type cards** — ML (green), Method (blue), Combo (amber), Parlay (yellow). All with non-zero W-L.
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
