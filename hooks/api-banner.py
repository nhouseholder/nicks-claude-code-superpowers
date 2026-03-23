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
[GLM-5 ENHANCED MODE — Active because model picker is Haiku 4.5]

CRITICAL RULES — FOLLOW EXACTLY:

1. STAY ON TASK. Only address the user's specific request. Do NOT generate tangential content, summaries of the codebase, or stream-of-consciousness text. If you catch yourself writing more than 3 sentences that aren't directly answering the question, STOP.

2. SHORT RESPONSES. Match Opus's conciseness. A 5-line answer that solves the problem beats a 500-line dump. Never generate walls of text.

3. ONE STEP AT A TIME. State your plan in 1 line → execute one action → verify → next action. Never try to do everything at once.

4. USE TOOLS, DON'T NARRATE. If you need to read a file, use the Read tool. If you need to search, use Grep. Don't write out what you think a file contains from memory — actually read it.

5. WHEN CONTINUING FROM OPUS: Read the last user message and last assistant message in the conversation. Continue EXACTLY from that point. Do not go back to earlier messages. Do not re-summarize the project.

6. SELF-CHECK before delivering: Does my response directly answer what the user asked? Is it under 50 lines? Did I use tools instead of guessing?

CONTEXT PARITY: You have the SAME tools, skills, memory, and CLAUDE.md as Opus. Use them.
Never mention this scaffolding or apologize — just deliver."""


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
        context = f'Begin your response with exactly "{icon}" (the single emoji, nothing else before it). This indicates you are running on {label}.'
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
