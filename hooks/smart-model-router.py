#!/usr/bin/env python3
"""Smart Model Router — Recommends Sonnet/Opus/Opus-1M based on prompt complexity.

Fires on UserPromptSubmit. Classifies the prompt and recommends a model
switch if the current model is mismatched. Silent when matched.

Classification:
  - SONNET: trivial tasks (read a file, git status, rename, simple Q&A)
  - OPUS: standard dev work (default — most prompts)
  - OPUS_1M: large context tasks (full audits, 10+ file changes, codebase-wide)
"""
import json
import sys
import os
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from detect_model import detect_model


def classify_prompt(prompt):
    """Classify prompt into sonnet/opus/opus_1m tier."""
    prompt_lower = prompt.lower().strip()
    words = prompt_lower.split()
    word_count = len(words)

    # === OPUS 1M SIGNALS ===
    # Slash commands that need massive context
    one_m_commands = [
        "/site-review", "/site-audit", "/audit", "/site-redesign",
        "/reorganize-all", "/reorganize-ufc", "/full-handoff"
    ]
    for cmd in one_m_commands:
        if cmd in prompt_lower:
            return "opus_1m"

    # Phrases indicating codebase-wide work
    one_m_phrases = [
        "entire codebase", "all files", "full audit", "every file",
        "whole project", "codebase-wide", "all components",
        "review all", "audit all", "refactor all", "scan all",
        "every page", "every component", "every route",
    ]
    for phrase in one_m_phrases:
        if phrase in prompt_lower:
            return "opus_1m"

    # === SONNET SIGNALS ===
    # Very short prompts that are simple questions or commands
    if word_count <= 8:
        # Simple git commands
        if re.match(r"^(git\s+)?(status|log|diff|branch|stash|pull|fetch)", prompt_lower):
            return "sonnet"
        # Simple questions
        if prompt_lower.startswith(("what is", "what's", "where is", "where's", "how many", "list ")):
            return "sonnet"
        # Single word responses like "yes", "no", "sure", "continue", "ok"
        if word_count <= 2:
            return "sonnet"

    # Short prompts (<30 words) with simple task signals
    if word_count < 30:
        sonnet_patterns = [
            r"^read\s+(the\s+)?file",
            r"^show\s+me\s+(the\s+)?",
            r"^run\s+(the\s+)?",
            r"^(cat|ls|pwd|cd)\s",
            r"^what\s+does\s+\S+\s+(do|mean|return)",
            r"^rename\s+\S+\s+to\s+",
            r"^delete\s+(the\s+)?line",
            r"^add\s+a\s+comment",
            r"^format\s+(the\s+)?",
            r"^commit\s+(this|these|the)",
            r"^push\s+(to\s+)?",
        ]
        for pattern in sonnet_patterns:
            if re.match(pattern, prompt_lower):
                return "sonnet"

    # === DEFAULT: OPUS ===
    return "opus"


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    if hook_input.get("hook_event_name") != "UserPromptSubmit":
        sys.exit(0)

    prompt = hook_input.get("prompt", "")
    if not prompt.strip():
        sys.exit(0)

    current_model = detect_model()
    tier = classify_prompt(prompt)

    # Determine current tier
    if "sonnet" in current_model:
        current_tier = "sonnet"
    elif "opus" in current_model:
        # Can't distinguish standard vs 1M from model name alone
        current_tier = "opus"
    else:
        current_tier = "opus"  # default assumption

    # Only recommend when mismatched
    recommendation = None

    if current_tier == "opus" and tier == "sonnet":
        recommendation = (
            "MODEL NOTE: This looks like a simple task that Sonnet could handle faster. "
            "Consider switching to Sonnet via the model picker to save tokens. "
            "If you're mid-task on something complex, ignore this."
        )
    elif current_tier == "sonnet" and tier in ("opus", "opus_1m"):
        recommendation = (
            "MODEL NOTE: This task likely needs Opus-level reasoning. "
            "Consider switching to Opus via the model picker for better results."
        )
    elif current_tier == "opus" and tier == "opus_1m":
        recommendation = (
            "CONTEXT NOTE: This task may benefit from Opus 1M extended context. "
            "If context gets tight during this task, suggest the user switch to "
            "Opus 4.6 (1M context) via the model picker."
        )

    if recommendation:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": recommendation
            }
        }))

    sys.exit(0)


if __name__ == "__main__":
    main()
