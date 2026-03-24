#!/usr/bin/env python3
"""API routing banner + GLM-5 reasoning scaffolding.

🟠 = Anthropic (Opus/Sonnet), 🟢 = Z AI (GLM-5).

On UserPromptSubmit:
  - Always injects icon prefix instruction
  - When Haiku/GLM-5: also injects reasoning scaffolding (replaces glm5-boost skill)
  - When Opus/Sonnet: no scaffolding (native intelligence sufficient)

On SessionStart:
  - Shows API status banner with proxy health
"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from detect_model import detect_model

# GLM-5 reasoning scaffolding — injected ONLY when Haiku is active.
# This replaces the glm5-boost skill with zero-cost dynamic injection.
GLM5_SCAFFOLDING = """
[GLM-5 ENHANCED MODE — Your Thinking Protocol]

You are a capable model with access to the SAME tools, skills, memory, and CLAUDE.md as Opus. The difference is that Opus thinks through these steps internally — you need to do them explicitly. Follow this protocol and you will produce Opus-quality work.

STEP 1 — UNDERSTAND (before doing anything)
Read the user's message carefully. Ask yourself:
- What are they ACTUALLY asking for? (not just the literal words — the intent)
- Is there context from earlier in this session I need? (check session-bridge context)
- What would a wrong answer look like? (so you can avoid it)
- Do I need to read any files or check any data before responding?
If uncertain about intent, ask ONE clarifying question instead of guessing.

STEP 2 — PLAN (say it in 1-2 lines)
Before taking action, briefly state your approach:
"I'll [action] by [method], then verify by [check]."
This prevents you from going off-track mid-response.

STEP 3 — EXECUTE (one thing at a time)
- Use tools for facts. READ files, don't guess their contents. GREP to search, don't assume.
- Make ONE change, verify it worked, then proceed to the next.
- Keep text output concise — tools do the heavy lifting, text communicates results.

STEP 4 — VERIFY (before delivering)
Before finishing your response, check:
- Does my response directly answer what the user asked?
- If I produced code/data, did I test or trace through one example?
- Is anything here generated from memory instead of tool results? (If so, use a tool instead)
- Would the user need to correct anything obvious?

CODING QUALITY (when writing or editing code):
- ALWAYS read the file before editing it. Never guess what's in a file.
- Match the existing code style — indentation, naming conventions, patterns.
- If editing a function, read the whole function first (not just the line you're changing).
- After making a change, consider: does this break anything else in the file?
- For multi-file changes, do them one at a time and verify each.
- When fixing a bug, explain what was wrong and why your fix addresses the root cause.
- If you're unsure your code is correct, run it or trace through a concrete example.

MULTI-FILE DEBUGGING (your weakness — compensate explicitly):
- Before forming ANY hypothesis, write down the key fact from each file you read.
  Example: "file_a.py: calls calculate_payout(odds). file_b.py: calculate_payout returns float."
- This prevents you from losing details between file reads.
- Trace the data flow: input → function A → function B → output. Write each step.
- If you need to correlate across 3+ files, use a TodoWrite to track what you've found.

DOMAIN MATH (betting, P/L, stats — high risk area):
- Wins pay at ODDS, not +1 unit. profit = stake * (odds/100) for positive, stake * (100/abs(odds)) for negative.
- Losses are always -1 unit per bet type. Fighter loses = ALL bets on that fighter lose.
- NEVER use +1.00u for a win or assume flat payouts.
- Before displaying any numbers, trace ONE concrete example by hand and show it.
- If a stat looks too good (80%+ accuracy, huge profit), suspect a bug before celebrating.

GUARDRAILS (safety nets):
- If you notice yourself writing paragraphs about topics the user didn't ask about → stop, refocus
- If you're generating code without having read the file first → stop, read the file
- If your text output is getting longer than your tool output → you're narrating instead of doing
- Keep text responses under 40 lines. Use tools for work, text for communication.
- Read ~/.claude/CLAUDE.md and the project's MEMORY.md at session start before domain work."""



try:
    hook_input = json.load(sys.stdin)
    event = hook_input.get("hook_event_name", "")

    model_lower = detect_model()

    if "haiku" in model_lower:
        icon = "🟢"
        label = "GLM-5"
        is_glm5 = True
    elif "opus" in model_lower:
        icon = "🟠"
        label = "Opus"
        is_glm5 = False
    elif "sonnet" in model_lower:
        icon = "🟠"
        label = "Sonnet"
        is_glm5 = False
    else:
        icon = "🟠"
        label = "Claude"
        is_glm5 = False

    # UserPromptSubmit: only inject for GLM-5 (Haiku). Opus/Sonnet don't need scaffolding.
    if event == "UserPromptSubmit":
        if is_glm5:
            context = f'Place exactly "{icon}" as the very first character of your FIRST message only. Do NOT repeat the emoji mid-response, after tool calls, or when subagent results return. One emoji total, at the very start. You are running on {label}.'
            context += GLM5_SCAFFOLDING
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": context
                }
            }))
        else:
            # Opus/Sonnet: emit minimal icon instruction only — no scaffolding overhead
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": f'Begin your response with exactly "{icon}" (the single emoji, nothing else before it). This indicates you are running on {label}.'
                }
            }))

    # SessionStart: show info banner with proxy status
    elif event == "SessionStart":
        if is_glm5:
            banner = f"{icon} Z AI API ACTIVE (GLM-5) — Anthropic limits bypassed"
        else:
            banner = f"{icon} Anthropic API ACTIVE — Claude {label}"
        try:
            resp = urllib.request.urlopen("http://127.0.0.1:17532/health", timeout=1)
            health = json.loads(resp.read())
            v = health.get("version", "?")
            up = health.get("uptime_seconds", 0)
            h, m = divmod(up // 60, 60)
            uptime_str = f"{h}h{m}m" if h else f"{m}m"
            banner += f"  |  Proxy v{v} up {uptime_str}"
        except Exception:
            banner += "  |  Proxy not running"

        # For GLM-5 sessions, also inject scaffolding at session level
        if is_glm5:
            print(json.dumps({
                "hookSpecificOutput": {
                    "hookEventName": "SessionStart",
                    "additionalContext": GLM5_SCAFFOLDING
                }
            }))
        print(json.dumps({"type": "info", "message": banner}))

    else:
        print(json.dumps({"type": "info", "message": f"{icon} {label}"}))

except Exception:
    pass
