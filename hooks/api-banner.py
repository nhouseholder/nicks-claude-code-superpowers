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
import urllib.request

# GLM-5 reasoning scaffolding — injected ONLY when Haiku is active.
# This replaces the glm5-boost skill with zero-cost dynamic injection.
GLM5_SCAFFOLDING = """
[GLM-5 ENHANCED MODE]

HARD RULES — VIOLATING THESE MEANS YOUR RESPONSE FAILED:

1. MAX 40 LINES of text output per response. If you need more, use tool calls (which don't count). Text is for the user. Tools are for work. Walls of text = failure.

2. NEVER GENERATE FROM MEMORY. If you need file contents, READ THE FILE. If you need search results, USE GREP. Never write out what you think code looks like — you WILL hallucinate. Every fact must come from a tool call.

3. ONE ACTION PER STEP. Do ONE thing → verify it worked → do the next. Never batch multiple unrelated changes.

4. STAY ON THE CURRENT MESSAGE. The session-bridge hook provides the last exchange for context. Address ONLY what the user just asked. Do not revisit old topics.

5. IF UNCERTAIN, ASK. A 1-line question beats a 500-line wrong answer.

6. NO FILLER. No "Let me think about this", no restating the question, no codebase summaries, no stream-of-consciousness. Answer → act → done.

7. STOP GENERATING if you notice: repeated phrases, code fragments without tool calls, paragraphs about topics the user didn't ask about, or text longer than your tool output. These are hallucination signals — stop immediately and use a tool instead.

You have the SAME tools, skills, memory, and CLAUDE.md as Opus. Use them."""


def detect_model():
    """Detect current model from CLAUDE_MODEL env var or proxy's /last-route."""
    model = os.environ.get("CLAUDE_MODEL", "")

    # Fallback: query proxy's /last-route endpoint
    if not model:
        try:
            resp = urllib.request.urlopen("http://127.0.0.1:17532/last-route", timeout=1)
            data = json.loads(resp.read())
            model = data.get("model", "")
        except Exception:
            pass

    return model.lower()


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

    # UserPromptSubmit: inject icon prefix + optional GLM-5 scaffolding
    if event == "UserPromptSubmit":
        context = f'Place exactly "{icon}" as the very first character of your FIRST message only. Do NOT repeat the emoji mid-response, after tool calls, or when subagent results return. One emoji total, at the very start. You are running on {label}.'
        if is_glm5:
            context += GLM5_SCAFFOLDING
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": context
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
