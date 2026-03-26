# Core Memory

<!-- Summaries + pointers to topic files -->
<!-- Updated by memory agent when topics accumulate significant insights -->

## UFC Betting Model
**CANONICAL SPEC:** `topics/ufc_betting_model_spec.md` — the 4+1 bet model, scoring rules, worked examples, backtester requirements
**DOMAIN KNOWLEDGE:** `topics/ufc_betting_domain_knowledge.md` — expert-level UFC betting reference (settlement rules, odds math, common mistakes, website standards)
**BACKTESTER RULES:** `topics/ufc_backtester_rules.md` — additional backtester details
5 bet types (ML, Method, Round, Combo, Parlay), all 1u. All contingent on ML — fighter loss = ALL prop bets lose (-1u each). Method/Round scored independently. 71-event minimum backtest (growing). Baseline: **+162.54u, 28.0% ROI** (2026-03-23). Old +$465 baseline was INVALID (buggy scoring). Read ALL spec files before touching ANY UFC scoring code.

**CRITICAL:** Read `ufc_betting_domain_knowledge.md` before ANY UFC session. Claude has repeatedly made basic betting mistakes (excluding fighter losses from prop analysis, flat +1u payouts, flip-flopping on data-driven decisions). The domain knowledge file prevents these errors.


## UFC Website Maintenance Rules [2026-03-25]
MANDATORY checklist for every site audit/update — 15 individual verification items across picks, event details, history, optimizer, and stats. Created because AI repeatedly says "looks correct" while missing 7+ bugs.
→ topics/ufc_website_maintenance_rules.md
