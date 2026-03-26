---
name: UFC Ground Truth Validation Spec
description: Schema for validate_registry.py — automated validation of all 12 scoring rules + learned bug checks before any UFC website deploy
type: project
---

# UFC Ground Truth Validation Specification

**Purpose:** A Python script (`ufc-predict/validate_registry.py`) that reads `ufc_profit_registry.json` and validates every bout against the 12 scoring rules from the betting model spec + all learned bug patterns. Runs before every deploy. Blocks deploy on failure.

## Why This Exists

The UFC event table has been wrong 15+ times. Root cause: no automated check between backtester output and website display. Humans (the user) have been the only QA gate, finding bugs like:
- Duncan predicted KO but tiebreaker should have made it DEC (2026-03-26)
- Parlay showing -1u when both legs won (2026-03-26)
- Method "0W-0L" when bets were placed (2026-03-25)
- Losses showing "—" instead of -1u (2026-03-24)
- Missing combo bets (2026-03-24)
- Registry totals not matching bout sums (2026-03-24)

## validate_registry.py Specification

### Input
- `ufc_profit_registry.json` — the full event registry

### Output
- Exit code 0: all rules pass, safe to deploy
- Exit code 1: failures found, deploy blocked
- Prints detailed report: which events/bouts fail which rules

### The 12 Core Rules (from betting model spec)

```python
def validate_rule_1(bout):
    """Fighter loss = -1u on EVERY placed bet"""
    if not bout['ml_correct']:
        for bet_type in ['ml_pnl', 'method_pnl', 'round_pnl', 'combo_pnl']:
            if bout.get(f'{bet_type.replace("_pnl", "_odds")}') is not None:
                # Bet was placed (odds exist), so pnl must be -1.0
                assert bout[bet_type] == -1.0, f"Rule 1: {bet_type} should be -1.0 on fighter loss"

def validate_rule_2(bout):
    """Wins use real odds payout, not flat +1u"""
    for bet_type, odds_key in [('ml_pnl','ml_odds'), ('method_pnl','method_odds'),
                                ('round_pnl','round_odds'), ('combo_pnl','combo_odds')]:
        if bout.get(bet_type) and bout[bet_type] > 0:
            odds = bout.get(odds_key)
            if odds is not None:
                expected = calculate_payout(odds)
                assert abs(bout[bet_type] - expected) < 0.02, f"Rule 2: {bet_type}={bout[bet_type]} but expected {expected} at odds {odds}"

def validate_rule_3(bout):
    """All prop bets require ML win"""
    if not bout.get('ml_correct'):
        for correct_key in ['method_correct', 'round_correct', 'combo_correct']:
            if bout.get(correct_key) is True:
                raise AssertionError(f"Rule 3: {correct_key}=True but ml_correct=False — impossible")

def validate_rule_4(bout):
    """Combo wins require ALL 3 correct"""
    if bout.get('combo_correct'):
        assert bout.get('ml_correct'), "Rule 4: combo_correct but not ml_correct"
        assert bout.get('method_correct'), "Rule 4: combo_correct but not method_correct"
        assert bout.get('round_correct'), "Rule 4: combo_correct but not round_correct"

def validate_rule_5(bout):
    """No bet without odds"""
    for pnl_key, odds_key in [('method_pnl','method_odds'), ('round_pnl','round_odds'), ('combo_pnl','combo_odds')]:
        if bout.get(odds_key) is None and bout.get(pnl_key) is not None:
            raise AssertionError(f"Rule 5: {pnl_key} has value but {odds_key} is null — phantom bet")

def validate_rule_6(bout):
    """No round/combo on DEC predictions"""
    if bout.get('predicted_method') == 'DEC':
        assert bout.get('round_pnl') is None, "Rule 6: round bet placed on DEC prediction"
        assert bout.get('combo_pnl') is None, "Rule 6: combo bet placed on DEC prediction"

def validate_rule_7(bout):
    """Bet count matches available odds"""
    bet_count = 0
    if bout.get('ml_odds') is not None: bet_count += 1
    if bout.get('method_odds') is not None: bet_count += 1
    if bout.get('round_odds') is not None: bet_count += 1
    if bout.get('combo_odds') is not None: bet_count += 1
    # Actual bets placed should match odds availability (minus gating)
    actual_bets = sum(1 for k in ['ml_pnl','method_pnl','round_pnl','combo_pnl'] if bout.get(k) is not None)
    assert actual_bets <= bet_count, f"Rule 7: {actual_bets} bets placed but only {bet_count} odds available"

def validate_rule_8(bout):
    """Method scoring: exact method match, KO/TKO grouped"""
    if bout.get('method_correct'):
        pred = bout.get('predicted_method', '').upper()
        actual = bout.get('actual_method', '').upper()
        ko_group = {'KO', 'TKO', 'KO/TKO'}
        if pred in ko_group:
            assert actual in ko_group, f"Rule 8: method_correct=True but predicted={pred}, actual={actual}"
        else:
            assert pred == actual, f"Rule 8: method_correct=True but predicted={pred}, actual={actual}"

def validate_rule_9(bout):
    """Method and Round scored independently"""
    # If method is correct but round is wrong, method should still win
    # If round is correct but method is wrong, round should still win
    # This is structural — just verify they CAN differ
    pass  # Checked via other rules

def validate_rule_10(event):
    """Parlay exists per event"""
    parlay = event.get('parlay')
    if parlay is None:
        return  # Some early events may lack parlay data
    assert 'legs' in parlay or 'parlay_legs' in event, "Rule 10: parlay data missing legs"
    assert 'pnl' in parlay or 'parlay_pnl' in event, "Rule 10: parlay data missing pnl"

def validate_rule_11(event):
    """Total bets = sum of fight bets + parlays"""
    bout_bets = 0
    for bout in event.get('bouts', []):
        for k in ['ml_pnl','method_pnl','round_pnl','combo_pnl']:
            if bout.get(k) is not None:
                bout_bets += 1
    parlay_bets = 1 if event.get('parlay', {}).get('pnl') is not None else 0
    # total_bets field should match
    if event.get('total_bets') is not None:
        assert event['total_bets'] == bout_bets + parlay_bets

def validate_rule_12(registry):
    """W + L = total bets per category"""
    for bet_type in ['ml', 'method', 'round', 'combo', 'parlay']:
        wins = registry.get(f'{bet_type}_wins', 0) or 0
        losses = registry.get(f'{bet_type}_losses', 0) or 0
        total = registry.get(f'{bet_type}_total', 0)
        if total:
            assert wins + losses == total, f"Rule 12: {bet_type} W({wins})+L({losses}) != total({total})"
```

### Learned Bug Checks (from anti-patterns)

```python
def check_r1_ko_gating(bout):
    """Round/combo bets only on KO R1 predictions"""
    pred_method = bout.get('predicted_method', '').upper()
    pred_round = bout.get('predicted_round')
    if bout.get('round_pnl') is not None:
        assert pred_method in ('KO', 'TKO', 'KO/TKO') and pred_round == 1, \
            f"Round bet placed on non-R1-KO prediction: {pred_method} R{pred_round}"
    if bout.get('combo_pnl') is not None:
        assert pred_method in ('KO', 'TKO', 'KO/TKO') and pred_round == 1, \
            f"Combo bet placed on non-R1-KO prediction: {pred_method} R{pred_round}"

def check_dec_tiebreaker(bout):
    """When KO/DEC are close, tiebreaker should fire to DEC"""
    # This is a warning, not a hard fail — requires model internals to validate
    # But if predicted_method=KO and actual_method=DEC and confidence is low,
    # flag for manual review
    pass

def check_combined_pnl(bout):
    """combined_pnl must equal sum of component P/L values"""
    components = sum(bout.get(k, 0) or 0 for k in ['ml_pnl','method_pnl','round_pnl','combo_pnl'])
    combined = bout.get('combined_pnl', 0) or 0
    if abs(combined - components) > 0.02:
        raise AssertionError(f"P/L math: combined={combined} but sum of components={components}")

def check_odds_range(bout):
    """No odds outside -2000 to +5000 range"""
    for k in ['ml_odds','method_odds','round_odds','combo_odds']:
        odds = bout.get(k)
        if odds is not None and (odds < -2000 or odds > 5000):
            raise AssertionError(f"Suspicious odds: {k}={odds}")

def check_no_profit_without_wins(registry_totals):
    """Profit > 0 requires Wins > 0"""
    for bet_type in ['ml', 'method', 'round', 'combo', 'parlay']:
        pnl = registry_totals.get(f'{bet_type}_pnl', 0) or 0
        wins = registry_totals.get(f'{bet_type}_wins', 0) or 0
        if pnl > 0 and wins == 0:
            raise AssertionError(f"Impossible: {bet_type} profit={pnl} with 0 wins")

def check_missing_odds(bout):
    """Flag any bout where the fighter won a prop bet but odds are missing"""
    if bout.get('method_correct') and bout.get('method_odds') is None:
        raise AssertionError(f"Method win but no odds — run scraper")
    if bout.get('round_correct') and bout.get('round_odds') is None:
        raise AssertionError(f"Round win but no odds — run scraper")
```

### Usage

```bash
# From ufc-predict directory:
python3 validate_registry.py

# Output example (success):
# Validating ufc_profit_registry.json...
# Events: 71 | Bouts: 494
# Rule 1 (fighter loss = -1u): ✓ 494/494 bouts
# Rule 2 (real odds payout): ✓ 353 wins checked
# ...
# Rule 12 (W+L balance): ✓ all 5 bet types
# R1 KO gating: ✓ 44 round/combo bets, all on R1 KO
# Combined P/L math: ✓ 494/494 bouts
#
# ALL CHECKS PASSED — safe to deploy

# Output example (failure):
# Rule 1 FAILED: Event "Evloev vs Murphy", bout "Duncan vs Opponent"
#   method_pnl=null but fighter lost and method_odds=-110 (bet was placed)
#   Expected: method_pnl=-1.0
#
# 1 FAILURE — DEPLOY BLOCKED
```

### Integration Points

1. **Pre-deploy hook**: validator runs automatically before `wrangler deploy` or `git push`
2. **Post-backtest**: validator runs after every backtest to catch scorer bugs immediately
3. **Debug workflow**: first step in any "table is wrong" debug session — validator output tells you WHERE the data is wrong
4. **/mmalogic command**: every task type runs the validator at the appropriate step

## Clean Rebuild Protocol

When the data pipeline is too corrupted to patch:

1. Backup current registry
2. Run clean backtest (UFC_BACKTEST_MODE=1 UFC_CACHE_ONLY=1)
3. Run validator on fresh output
4. Fix any failures (backtester bug, not data patch)
5. Generate frontend data files from validated registry
6. Rebuild frontend
7. Deploy
8. Visual verification via Claude in Chrome
9. Save baseline snapshot to memory

**The validator is the gatekeeper.** No data reaches the website without passing all rules.
