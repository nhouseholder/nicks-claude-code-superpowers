#!/usr/bin/env python3
"""
Session Bridge — Gives GLM-5 a factual state dump, not instructions.
Reads the auto-checkpoint (rich state) and constructs a handoff
that tells GLM-5 exactly what's happening, not how to think.
"""
import json
import sys
import os
import subprocess
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from detect_model import detect_model


def extract_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return " ".join(
            b.get("text", "") for b in content
            if isinstance(b, dict) and b.get("type") == "text"
        )
    return ""


try:
    hook_input = json.load(sys.stdin)
    if hook_input.get("hook_event_name") != "UserPromptSubmit":
        sys.exit(0)
    if "haiku" not in detect_model():
        sys.exit(0)

    prompt = hook_input.get("prompt", "")
    checkpoint_path = Path.home() / ".claude" / "last-checkpoint.json"

    # === SOURCE 1: Rich checkpoint from auto-checkpoint.py ===
    cp = {}
    if checkpoint_path.exists():
        try:
            cp = json.loads(checkpoint_path.read_text())
        except Exception:
            pass

    # === SOURCE 2: Transcript (fallback if no checkpoint) ===
    last_user = cp.get("last_user_message", "")
    last_assistant = cp.get("last_assistant_response", "")

    if not last_assistant:
        transcript_path = hook_input.get("transcript_path", "")
        if transcript_path and Path(transcript_path).exists():
            try:
                r = subprocess.run(["tail", "-50", transcript_path],
                                 capture_output=True, text=True, timeout=2)
                for line in reversed(r.stdout.strip().split("\n")):
                    try:
                        entry = json.loads(line)
                        text = extract_text(entry.get("content", "")).strip()
                        if len(text) < 5:
                            continue
                        if entry.get("role") == "assistant" and not last_assistant:
                            last_assistant = text[:1500]
                        elif entry.get("role") == "user" and not last_user:
                            last_user = text[:500]
                        if last_user and last_assistant:
                            break
                    except Exception:
                        pass
            except Exception:
                pass

    if not last_assistant:
        sys.exit(0)

    # === BUILD FACTUAL HANDOFF ===
    parts = ["[HANDOFF — Continuing from Opus. Here is the current state:]"]

    # What was happening
    parts.append(f"\nLAST REQUEST: {last_user[:500]}")
    parts.append(f"\nOPUS WAS DOING: {last_assistant[:1500]}")

    # Git state (what's changed on disk)
    git_status = cp.get("git_status", "")
    modified = cp.get("modified_files", "")
    diff_stat = cp.get("git_diff_stat", "")

    if git_status or modified:
        parts.append(f"\nFILES CHANGED (uncommitted): {modified or git_status}")
    if diff_stat:
        parts.append(f"DIFF SUMMARY: {diff_stat}")

    # Instructions — minimal, factual
    parts.append("\nContinue from where Opus left off. Don't redo completed work.")
    parts.append("Check git diff if you need to see what was already changed.")

    bridge = "\n".join(parts)

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": bridge
        }
    }))

except Exception:
    sys.exit(0)
