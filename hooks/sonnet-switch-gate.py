#!/usr/bin/env python3
"""Stop hook: After a plan is written/approved, require Claude to hand off to Sonnet.

NO EXCEPTIONS policy (per 2026-04-16):
  Fires every turn while an ACTIVE_PLAN pointer exists AND the last
  assistant message is missing the verbatim hand-off line. Does not
  silently give up after N attempts. The only ways to clear it:
    1. User types "go" → plan-mode-enforcer clears ACTIVE_PLAN pointer
    2. User manually deletes <project>/.plans/ACTIVE_PLAN
    3. Pointer is older than SESSION_WINDOW_SEC (24h — abandoned plan)

Respects the harness's stop_hook_active recursion flag (mandatory to
prevent infinite loops during the re-prompt cycle). This is not a
user-configurable exception — it's a Claude Code protocol requirement.

Does NOT enforce:
  - Word count, BLUF, bullet density, paragraph length, DONE/FOUND debrief
  - Any other communication style rule
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from typing import Any


NEEDLE = "switch to sonnet to execute and reply go"
# Narrow window: the gate is meant to fire for the ONE turn right after a
# plan was written. If the user takes longer than 5 min to type "go", the
# mtime-fallback in plan-mode-enforcer still resolves the plan file.
# Previous value (86400) made every assistant turn for 24h fire this gate
# whenever an ACTIVE_PLAN pointer was lingering — unrelated Q&A got blocked.
SESSION_WINDOW_SEC = 300  # 5 min


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


def active_plan_pointer() -> str:
    """Return path to project's ACTIVE_PLAN pointer, or '' if not in a project."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=os.getcwd(), capture_output=True, text=True, timeout=2,
        )
        if result.returncode == 0 and result.stdout.strip():
            return os.path.join(result.stdout.strip(), ".plans", "ACTIVE_PLAN")
    except Exception:
        pass
    return ""


def active_plan_is_live(pointer: str) -> bool:
    """True iff the ACTIVE_PLAN pointer exists and is not abandoned (<24h old)."""
    if not pointer or not os.path.isfile(pointer):
        return False
    try:
        age = time.time() - os.path.getmtime(pointer)
    except Exception:
        return False
    if age >= SESSION_WINDOW_SEC:
        # Abandoned plan — clean up pointer so it stops firing.
        try:
            os.remove(pointer)
        except Exception:
            pass
        return False
    return True


def strip_code(text: str) -> str:
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def _clear_pointer(pointer: str) -> None:
    try:
        os.remove(pointer)
    except Exception:
        pass


def main() -> None:
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    pointer = active_plan_pointer()
    if not active_plan_is_live(pointer):
        sys.exit(0)

    last = load_last_message(hook_input)
    cleaned = strip_code(last).lower() if last else ""
    has_needle = bool(cleaned) and NEEDLE in cleaned

    # Harness recursion guard — MANDATORY to avoid infinite re-prompt loops.
    # If the needle is now present (retry succeeded), clear the pointer so
    # future turns don't re-fire. Otherwise just exit without blocking.
    if hook_input.get("stop_hook_active") or hook_input.get("stopHookActive"):
        if has_needle:
            _clear_pointer(pointer)
        sys.exit(0)

    if not last:
        # Fail-closed: can't verify needle, block.
        sys.stderr.write(
            "BLOCKED: Output this one line only, nothing else:\n"
            "switch to sonnet to execute and reply go"
        )
        sys.exit(2)

    if has_needle:
        # Handoff delivered — clear pointer so subsequent unrelated turns
        # don't keep firing this gate. plan-mode-enforcer's "go" handler
        # falls back to mtime-based plan discovery when the pointer is gone.
        _clear_pointer(pointer)
        sys.exit(0)

    # ACTIVE_PLAN is live and needle is missing — block once.
    sys.stderr.write(
        "BLOCKED: Output this one line only, nothing else:\n"
        "switch to sonnet to execute and reply go"
    )
    sys.exit(2)


if __name__ == "__main__":
    main()
