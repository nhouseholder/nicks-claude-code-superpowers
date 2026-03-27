#!/usr/bin/env python3
"""SessionStart hook: Inject UFC betting rules when in a UFC project directory.

Only fires when pwd contains ufc-predict, mmalogic, or octagonai.
Injects the critical betting rules that Claude keeps getting wrong
so they're in context from the start — without bloating non-UFC sessions.

Exit code 0 always (context injection only).
"""
import json
import os
import sys

UFC_DIR_SIGNALS = ["ufc-predict", "mmalogic", "octagonai", "ufc_predict"]

UFC_CONTEXT = """UFC SESSION — BETTING RULES LOADED (from ufc-context-loader.py hook)

CRITICAL RULES (these have been wrong 15+ times):

1. Fighter loss = -1u on EVERY placed bet (ML, Method, Round, Combo). No exceptions.
2. Wins pay at REAL ODDS, not flat +1u. Positive: stake×odds/100. Negative: stake×100/|odds|.
3. ALL prop bets require ML win. Fighter loses → Method/Round/Combo ALL lose.
4. Method and Round scored INDEPENDENTLY. Right method + wrong round = Method wins, Round loses.
5. Combo wins require ALL THREE correct (ML + method + round).
6. No round/combo bets on DEC predictions.
7. R1 KO gating: round/combo bets ONLY for KO R1 predictions.
8. Missing odds = RUN THE SCRAPER. Never display "—" and call it correct.
9. Parlay is per-event (not per-fight). HC parlay + ROI parlay. 1u each.
10. 71+ event minimum backtest window (growing, never shrinks).

CANONICAL PATHS:
- Webapp: ufc-predict/webapp/frontend/ (NEVER root webapp/)
- Data: ufc-predict/webapp/frontend/public/data/
- Algorithm: ufc-predict/
- Full spec: ~/.claude/memory/topics/ufc_betting_model_spec.md

MANDATORY: Read the full spec before touching ANY scoring code.
MANDATORY: Use /mmalogic command for ALL website work.
MANDATORY: Run validate_registry.py before ANY deploy."""


def main():
    cwd = os.getcwd().lower()

    is_ufc = any(signal in cwd for signal in UFC_DIR_SIGNALS)

    if is_ufc:
        print(json.dumps({
            "decision": "allow",
            "context": UFC_CONTEXT
        }))

    sys.exit(0)


if __name__ == "__main__":
    main()
