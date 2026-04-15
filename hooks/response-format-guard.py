#!/usr/bin/env python3
"""Stop hook: block responses that are verbose walls of text or bullet spam.

The goal is balanced density:
- short prose when prose is denser
- bullets only when content is list-shaped
- tables for comparisons
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
from typing import Any


MAX_BLOCKS = 2
FILLER_OPENERS = (
    "got it",
    "done -",
    "done —",
    "absolutely",
    "sure",
    "great question",
    "understood",
)

BANNED_PHRASES = (
    "let me ",
    "i'll now",
    "first, i need to",
    "now i'll",
    "great question",
    "as an ai",
    "in summary",
    "to summarize",
    "i hope this helps",
    "let me know if you have",
    "please let me know if",
    "feel free to",
)

# First-sentence preamble starters (BLUF violation)
PREAMBLE_STARTERS = (
    "let me ",
    "i'll ",
    "first,",
    "now i'll",
    "i need to",
    "i'm going to",
    "i will ",
)


def get_counter_file(session_id: str) -> str:
    short = hashlib.md5((session_id or "default").encode()).hexdigest()[:8]
    return f"/tmp/.claude-response-format-{short}"


def get_block_count(counter_file: str) -> int:
    try:
        if os.path.exists(counter_file):
            return int(open(counter_file).read().strip())
    except Exception:
        return 0
    return 0


def block(reason: str, counter_file: str) -> None:
    count = get_block_count(counter_file) + 1
    try:
        with open(counter_file, "w") as handle:
            handle.write(str(count))
    except Exception:
        pass

    if count <= MAX_BLOCKS:
        sys.stderr.write(reason)
        sys.exit(2)

    try:
        os.remove(counter_file)
    except Exception:
        pass
    sys.exit(0)


def reset_counter(counter_file: str) -> None:
    try:
        if os.path.exists(counter_file):
            os.remove(counter_file)
    except Exception:
        pass


def extract_text(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, list):
        return "\n".join(part for part in (extract_text(item) for item in value) if part)
    if isinstance(value, dict):
        for key in ("text", "message", "content", "parts", "value"):
            if key in value:
                text = extract_text(value[key])
                if text:
                    return text
    return ""


def collect_assistant_messages(node: Any, messages: list[str]) -> None:
    if isinstance(node, dict):
        role = str(node.get("role", "")).lower()
        kind = str(node.get("type", "")).lower()
        if role in {"assistant", "model"} or kind in {"assistant", "model"}:
            text = extract_text(node)
            if text:
                messages.append(text)

        for value in node.values():
            collect_assistant_messages(value, messages)
        return

    if isinstance(node, list):
        for item in node:
            collect_assistant_messages(item, messages)


def load_last_message(hook_input: dict[str, Any]) -> str:
    for key in ("last_assistant_message", "lastAssistantMessage"):
        message = hook_input.get(key)
        if isinstance(message, str) and message.strip():
            return message.strip()

    transcript_path = hook_input.get("transcript_path") or hook_input.get("transcriptPath")
    if not isinstance(transcript_path, str) or not transcript_path:
        return ""

    try:
        with open(transcript_path) as handle:
            transcript = json.load(handle)
    except Exception:
        return ""

    messages: list[str] = []
    collect_assistant_messages(transcript, messages)
    return messages[-1].strip() if messages else ""


def strip_code_blocks(text: str) -> str:
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    return text.strip()


def paragraph_blocks(lines: list[str]) -> list[str]:
    blocks: list[str] = []
    current: list[str] = []

    for raw_line in lines:
        line = raw_line.strip()
        is_bullet = bool(re.match(r"^([-*+]|\d+\.)\s+", line))
        is_table = line.count("|") >= 2
        is_header = line.startswith("#")

        if not line:
            if current:
                blocks.append(" ".join(current).strip())
                current = []
            continue

        if is_bullet or is_table or is_header:
            if current:
                blocks.append(" ".join(current).strip())
                current = []
            continue

        current.append(line)

    if current:
        blocks.append(" ".join(current).strip())

    return [block for block in blocks if block]


def first_sentence(text: str) -> str:
    """Extract first non-empty sentence from text."""
    for line in text.splitlines():
        line = line.strip()
        if line and not line.startswith("#") and not line.startswith("|"):
            # Take up to first period/newline
            return line.split(".")[0].lower()
    return ""


def should_block(text: str) -> str | None:
    cleaned = strip_code_blocks(text)
    if len(cleaned) < 220:
        return None

    lowered = cleaned.lower().lstrip()

    # Filler openers
    if any(lowered.startswith(opener) for opener in FILLER_OPENERS):
        return "BLOCKED STOP: Remove filler openers. Lead with the answer immediately."

    # BLUF check — first sentence must not be preamble
    first = first_sentence(cleaned)
    if any(first.startswith(starter) for starter in PREAMBLE_STARTERS):
        return (
            "BLOCKED STOP: BLUF violation — first sentence is preamble, not the answer. "
            "Lead with the result/decision/answer. Cut 'Let me...', 'I'll...', 'First,...'."
        )

    # Banned phrases scan
    lowered_full = cleaned.lower()
    for phrase in BANNED_PHRASES:
        if phrase in lowered_full:
            return (
                f"BLOCKED STOP: Banned phrase detected — '{phrase.strip()}'. "
                "Remove it and rewrite. See CLAUDE.md Communication section."
            )

    lines = [line.rstrip() for line in cleaned.splitlines()]
    bullet_lines = [line for line in lines if re.match(r"^\s*([-*+]|\d+\.)\s+", line)]
    table_lines = [line for line in lines if line.count("|") >= 2]
    paragraphs = paragraph_blocks(lines)

    bullet_count = len(bullet_lines)
    table_count = len(table_lines)
    avg_bullet_len = 0
    if bullet_lines:
        avg_bullet_len = sum(len(re.sub(r"^\s*([-*+]|\d+\.)\s+", "", line)) for line in bullet_lines) / bullet_count

    long_paragraphs = [paragraph for paragraph in paragraphs if len(paragraph) >= 300]
    medium_paragraphs = [paragraph for paragraph in paragraphs if len(paragraph) >= 180]

    if long_paragraphs and bullet_count == 0 and table_count == 0:
        return (
            "BLOCKED STOP: Response is too paragraph-heavy. Use a short lead sentence, "
            "then compress with compact bullets or a table if needed."
        )

    if len(medium_paragraphs) >= 2 and bullet_count == 0 and table_count == 0:
        return (
            "BLOCKED STOP: Response uses too many medium paragraphs. Compress the answer into "
            "one compact paragraph plus minimal structure."
        )

    if bullet_count >= 8 and table_count == 0 and avg_bullet_len < 140:
        return (
            "BLOCKED STOP: Response is too vertically bloated. Collapse bullet spam into a short "
            "paragraph or a compact table."
        )

    if bullet_count >= 6 and not paragraphs and table_count == 0:
        return (
            "BLOCKED STOP: Response is all bullets. Mix short prose with only the minimum number "
            "of bullets needed."
        )

    # Short-bullet filler check — 3+ consecutive bullets each <40 chars
    short_bullet_runs = 0
    run = 0
    for line in lines:
        if re.match(r"^\s*([-*+]|\d+\.)\s+", line):
            content = re.sub(r"^\s*([-*+]|\d+\.)\s+", "", line).strip()
            if len(content) < 40:
                run += 1
                if run >= 3:
                    short_bullet_runs += 1
            else:
                run = 0
        else:
            run = 0

    if short_bullet_runs > 0:
        return (
            "BLOCKED STOP: Short-bullet filler detected — 3+ consecutive bullets under 40 chars. "
            "Expand each bullet to a full line (~80–120 chars) or merge into prose."
        )

    # BLUF Debrief check — every substantive response must end with DONE/FOUND block.
    # Only enforce on responses long enough to have done something meaningful (>400 chars).
    if len(cleaned) >= 400:
        tail = cleaned[-600:].lower()
        has_debrief = bool(
            re.search(r"\bdone\s*:", tail) or re.search(r"\bfound\s*:", tail)
        )
        if not has_debrief:
            return (
                "BLOCKED STOP: Missing DONE/FOUND debrief. Every response must end with:\n"
                "---\n"
                "DONE: [what was done — one tight sentence]\n"
                "FOUND: [what was found/decided — one tight sentence, or N/A]\n"
                "Add it and resubmit."
            )

    # Sonnet-switch message check — if a plan was just approved (ACTIVE_PLAN
    # pointer exists and is < 60 sec old) and this response does NOT contain
    # the verbatim hand-off line, block. Pipeline drift prevention.
    try:
        import os as _os
        import time as _time
        import subprocess as _sp
        # Find current project's ACTIVE_PLAN pointer
        result = _sp.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=_os.getcwd(), capture_output=True, text=True, timeout=2,
        )
        if result.returncode == 0 and result.stdout.strip():
            pointer = _os.path.join(result.stdout.strip(), ".plans", "ACTIVE_PLAN")
            if _os.path.isfile(pointer):
                age = _time.time() - _os.path.getmtime(pointer)
                if age < 300:
                    needle = "switch to sonnet, then type: go"
                    if needle not in cleaned.lower():
                        return (
                            "BLOCKED STOP: Plan was just approved but the response "
                            "is missing the hand-off line. Output VERBATIM:\n"
                            "  Plan saved. Switch to Sonnet, then type: go\n"
                            "Do NOT execute plan steps yourself."
                        )
    except Exception:
        pass

    return None


def main() -> None:
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        sys.exit(0)

    session_id = (
        hook_input.get("session_id")
        or hook_input.get("sessionId")
        or "default"
    )
    counter_file = get_counter_file(str(session_id))

    if hook_input.get("stop_hook_active") or hook_input.get("stopHookActive"):
        reset_counter(counter_file)
        sys.exit(0)

    last_message = load_last_message(hook_input)
    if not last_message:
        reset_counter(counter_file)
        sys.exit(0)

    reason = should_block(last_message)
    if reason:
        block(reason, counter_file)

    reset_counter(counter_file)
    sys.exit(0)


if __name__ == "__main__":
    main()