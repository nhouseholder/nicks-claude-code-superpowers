## UFC MMA Logic Website Maintenance Rules [2026-03-24]

### MANDATORY CHECKLIST — Every Site Update/Audit Must Verify ALL Of These

This checklist exists because the AI has repeatedly claimed pages "look correct" while missing 7+ bugs simultaneously. Every item must be individually verified with specific values, not "looks fine."

#### Picks Page (Fight Cards)
- [ ] **Confidence values are 0-100%** — values like "260% conf" are RAW DIFFERENTIALS not percentages. This is a formatting bug.
- [ ] **SUB gating is enforced** — if SUB gating is active, NO fighter should show "by SUB" in recommended bets. Check EVERY card.
- [ ] **Round gating is enforced** — if a round bet should be gated (e.g., DEC predictions have no round bet), verify it's not displayed.
- [ ] **Combo bets appear on cards** — every fight card that has a method AND round prediction should show a combo bet. If NONE show combos, the combo rendering is broken.
- [ ] **Both parlays are shown** — the site must show TWO parlays per event: (1) High Confidence parlay and (2) High ROI parlay. If only one appears, the second is broken.

#### Event Detail Pages (Expanded View)
- [ ] **Every LOST method/round/combo bet shows -1u** — a lost prop bet is ALWAYS -1 unit. If it shows blank/missing/null, the scoring display is broken.
- [ ] **Every WON method/round/combo bet shows units won at Vegas odds** — a won bet pays at the odds, not +1u flat. If odds were +150, show +1.50u. If blank/missing, the payout display is broken.
- [ ] **Parlay results appear on event detail pages** — parlay bets must be shown with their W/L status and payout. If missing entirely, the parlay rendering is broken.
- [ ] **Fighter loss = ALL bets on that fighter show -1u** — ML, method, round, combo ALL lose. No "N/A" or blank for props when the fighter lost.

#### History/Event Breakdowns Page
- [ ] **All 5 bet types shown** — ML (M), Method (M), Round (R), Combo (C), Parlay (P). If any column is missing, the table is broken.
- [ ] **Event P/L totals match sum of individual bets** — spot-check at least 2 events manually.

#### Optimizer/Admin Page
- [ ] **"Current" section has values populated** — if the current params section shows blanks/missing/null, the data loading is broken. Do NOT say "looks correct" if values are missing.

#### Summary Stats Cards
- [ ] **Profit > 0 requires Wins > 0** — impossible to have profit with 0 wins
- [ ] **W + L = total bets placed** per category
- [ ] **All bet types that were bet on show non-zero W-L**

### HOW TO VERIFY (Not Optional)

1. **Do NOT glance and say "looks correct."** Check each item individually.
2. **State specific values** — "ML shows 45W-26L, +12.4u" not "ML looks fine"
3. **Check at least 2 fight cards in detail** — open the expanded view
4. **Check at least 1 event detail page fully** — verify every bout's scoring
5. **If you can't check something** (no screenshot, no access), say "UNABLE TO VERIFY: [item]" — do NOT assume it's correct.

### WHY THIS EXISTS

The AI has been caught:
- Saying "no obvious bugs" while 260% confidence values were on screen
- Saying "looks correct" while SUB-gated bets were being displayed
- Missing ALL combo bets being absent from picks cards
- Missing entire parlay section being absent
- Claiming event detail "looks correct" when every prop bet had missing P/L values
- Missing that the optimizer "current" section was empty

**If you skip this checklist, you WILL miss bugs. Every time.**
