#!/usr/bin/env python3
"""Stop hook: After a plan is written/approved, require Claude to hand off to Sonnet.

Narrow-purpose — fires ONLY when:
  (1) the current project has an ACTIVE_PLAN pointer
  (2) the pointer was set within the last 5 minutes
  (3) the last assistant message is missing the verbatim hand-off line

Behavior:
  - Block with exit code 2 → Claude regenerates with the hand-off line
  - Max 2 blocks per session, then silently pass (avoid infinite loops)

Does NOT enforce:
  - Word count, BLUF, bullet density, paragraph length, DONE/FOUND debrief
  - Any other communication style rule (removed per user request)

Designed to replace the Sonnet-switch enforcement that lived inside the old
response-format-guard.py, without the format-guard baggage.
"""
from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
import time
from typing import Any


MAX_BLOCKS = 2
NEEDLE = "switch to sonnet, then type: go"
FRESH_WINDOW_SEC = 300  # 5 min — matches plan-relocate / ExitPlanMode recency


def counter_path(session_id: str) -> str:
    short = hashlib.md5((session_id or "default").encode()).hexdigest()[:8]
    return f"/tmp/.claude-sonnet-gate-{short}"


def get_count(path: str) -> int:
    try:
        if os.path.exists(path):
            return int(open(path).read().strip())
    except Exception:
        pass
    return 0


def bump_count(path: str, n: int) -> None:
    try:
        with open(path, "w") as h:
            h.write(str(n))
    except Exception:
        pass


def reset_count(path: str) -> None:
    try:
        if os.path.exists(path):
            os.remove(path)
    except Exception:
        pass


def extract_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(p for p in (extract_text(i) for i in value) if p)
    if isinstance(value, dict):
        for key in ("text", "message", "content", "parts", "value"):
            if key in value:
                t = extract_text(value[key])
                if t:
                    return t
    return ""


def collect_assistant(node: Any, out: list[str]) -> None:
    if isinstance(node, dict):
        role = str(node.get("role", "")).lower()
        kind = str(node.get("type", "")).lower()
        if role in {"assistant", "model"} or kind in {"assistant", "model"}:
            t = extract_text(node)
            if t:
                out.append(t)
        for v in node.values():
            collect_assistant(v, out)
        return
    if isinstance(node, list):
        for item in node:
            collect_assistant(item, out)


def load_last_message(hook_input: dict[str, Any]) -> str:
    # Prefer direct field if harness provides it
    for key in ("last_assistant_message", "lastAssistantMessage"):
        msg = hook_input.get(key)
        if isinstance(msg, str) and msg.strip():
            return msg.strip()

    transcript_path = hook_input.get("transcript_path") or hook_input.get("transcriptPath")
    if not isinstance(transcript_path, str) or not transcript_path:
        return ""

    messages: list[str] = []
    try:
        with open(transcript_path) as h:
            content = h.read()
        # JSONL format (Claude Code standard)
        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                entry = json.loads(line)
                collect_assistant(entry, messages)
            except Exception:
                continue
        # Single-doc fallback
        if not messages:
            try:
                collect_assistant(json.loads(content), messages)
            except Exception:
                pass
    except Exception:
        return ""

    return messages[-1].strip() if messages else ""


def active_plan_fresh() -> bool:
    """True iff the current project has a freshly-set ACTIVE_PLAN pointer."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=os.getcwd(), capture_output=True, text=True, timeout=2,
        )
        if result.returncode != 0 or not result.stdout.strip():
            return False
        pointer = os.path.join(result.stdout.strip(), ".plans", "ACTIVE_PLAN")
        if not os.path.isfile(pointer):
            return False
        age = time.time() - os.path.getmtime(pointer)
        return age < FRESH_WINDOW_SEC
    except Exception:
        return False


def strip_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def main() -> None:
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    session_id = str(
        hook_input.get("session_id") or hook_input.get("sessionId") or "default"
    )
    counter_file = counter_path(session_id)

    # Allow recursion guard from harness
    if hook_input.get("stop_hook_active") or hook_input.get("stopHookActive"):
        reset_count(counter_file)
        sys.exit(0)

    # Only enforce if a plan was just pinned as active
    if not active_plan_fresh():
        reset_count(counter_file)
        sys.exit(0)

    last = load_last_message(hook_input)
    if not last:
        reset_count(counter_file)
        sys.exit(0)

    cleaned = strip_code(last).lower()
    if NEEDLE in cleaned:
        reset_count(counter_file)
        sys.exit(0)

    # Block — require hand-off line
    count = get_count(counter_file) + 1
    bump_count(counter_file, count)

    if count > MAX_BLOCKS:
        reset_count(counter_file)
        sys.exit(0)

    sys.stderr.write(
        "BLOCKED: A plan was just approved. Pause here and output exactly:\n\n"
        "  Plan saved. Switch to Sonnet, then type: go\n\n"
        "Do NOT execute the plan. Do NOT summarize the plan. Just the hand-off line, then stop."
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
