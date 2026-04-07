#!/usr/bin/env python3
"""Hook-backed session logger and digest builder for Copilot learning.

Captures lightweight session signals from hooks, writes per-session summaries,
and generates a rolling digest that `/insights` and related prompts can inspect.
The digest also imports recent historical session metadata when available so the
system starts with prior evidence instead of an empty history.

Exit code 0 always.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path.home() / ".claude" / "usage-data" / "copilot-insights"
LIVE_DIR = ROOT / "live"
SESSIONS_DIR = ROOT / "sessions"
DIGEST_PATH = ROOT / "learning-digest.md"
SIGNALS_PATH = ROOT / "signals.json"
ERROR_LOG_PATH = ROOT / "errors.log"
LEGACY_SESSION_META_DIR = Path.home() / ".claude" / "usage-data" / "session-meta"
MAX_PROMPTS_PER_SESSION = 8
MAX_PROMPT_PREVIEW = 240
MAX_NOTABLE_COMMANDS = 6
MAX_RECENT_HOOK_SESSIONS = 30
MAX_RECENT_LEGACY_SESSIONS = 80

CORRECTION_PATTERNS = [
    r"\bthat'?s wrong\b",
    r"\bthat'?s not right\b",
    r"\bthat'?s not correct\b",
    r"\bno,?\s+(?:don'?t|stop|that)\b",
    r"\bstop doing\b",
    r"\bI (?:already )?told you\b",
    r"\bI said\b",
    r"\bwhy did you\b",
    r"\bwhy are you\b",
    r"\byou (?:keep|always|still)\b",
    r"\bnot what I (?:asked|wanted|meant)\b",
    r"\byou (?:broke|destroyed|removed|deleted)\b",
    r"\byou just said\b",
    r"\byou changed\b",
    r"\bmake up your mind\b",
    r"\bwhich is it\b",
    r"\bcontradict(?:ed|s)\b",
]

TOOL_NAME_MAP = {
    "run_in_terminal": "Bash",
    "terminal_last_command": "Bash",
    "terminal_selection": "Bash",
    "read_file": "Read",
    "file_search": "Glob",
    "grep_search": "Grep",
    "create_file": "Write",
    "apply_patch": "Edit",
    "runSubagent": "Agent",
    "manage_todo_list": "TodoWrite",
    "fetch_webpage": "WebFetch",
    "open_browser_page": "WebFetch",
    "get_search_view_results": "ToolSearch",
    "semantic_search": "ToolSearch",
    "github_repo": "WebFetch",
}

PROMPT_CATEGORIES = [
    ("slash-command", [r"^/\w"]),
    ("continuation", [r"^continue$", r"^yes$", r"^yes implement$", r"^implement all$", r"^keep going$"]),
    ("deploy-release", [r"\bdeploy\b", r"\brelease\b", r"\bgo live\b", r"\bship\b", r"\bpush to production\b"]),
    ("review-audit", [r"\breview\b", r"\baudit\b", r"\bassess\b", r"\binspect\b"]),
    ("fix-debug", [r"\bfix\b", r"\bdebug\b", r"\bbroken\b", r"\berror\b", r"\bissue\b", r"\bnot working\b"]),
    ("implement-build", [r"\bimplement\b", r"\bbuild\b", r"\bcreate\b", r"\badd\b", r"\bmake\b"]),
    ("research-explain", [r"\bresearch\b", r"\blearn\b", r"\bexplain\b", r"\bhow\b", r"\bwhy\b"]),
    ("plan-strategy", [r"\bplan\b", r"\broadmap\b", r"\bstrategy\b", r"\bwhat(?:'s| is) next\b"]),
]


def log_internal_error(message: str) -> None:
    try:
        ROOT.mkdir(parents=True, exist_ok=True)
        with ERROR_LOG_PATH.open("a", encoding="utf-8") as handle:
            handle.write(f"{datetime.now(timezone.utc).isoformat()} {message}\n")
    except Exception:
        pass


def first_present(payload: dict[str, Any], *keys: str, default: Any = None) -> Any:
    for key in keys:
        if key in payload and payload[key] is not None:
            return payload[key]
    return default


def squeeze_text(value: Any, limit: int = MAX_PROMPT_PREVIEW) -> str:
    if value is None:
        return ""
    text = str(value)
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"


def parse_timestamp(raw_value: Any) -> datetime:
    text = str(raw_value or "").strip()
    if not text:
        return datetime.now(timezone.utc)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        parsed = datetime.fromisoformat(text)
        if parsed.tzinfo is None:
            return parsed.replace(tzinfo=timezone.utc)
        return parsed
    except ValueError:
        return datetime.now(timezone.utc)


def iso_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def ensure_dirs() -> None:
    LIVE_DIR.mkdir(parents=True, exist_ok=True)
    SESSIONS_DIR.mkdir(parents=True, exist_ok=True)


def load_json(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    try:
        with path.open("r", encoding="utf-8") as handle:
            return json.load(handle)
    except Exception:
        return default


def write_json(path: Path, payload: Any) -> None:
    with path.open("w", encoding="utf-8") as handle:
        json.dump(payload, handle, indent=2, sort_keys=True)


def increment(mapping: dict[str, int], key: str, amount: int = 1) -> None:
    mapping[key] = int(mapping.get(key, 0)) + amount


def canonical_tool_name(name: Any) -> str:
    raw_name = str(name or "unknown").strip()
    if not raw_name:
        return "unknown"
    return TOOL_NAME_MAP.get(raw_name, raw_name)


def extract_slash_commands(prompt: str) -> list[str]:
    commands = []
    for match in re.finditer(r"(?:^|\s)/([A-Za-z][A-Za-z0-9-]*)\b", prompt):
        commands.append(match.group(1))
    return commands


def detect_correction(prompt: str) -> bool:
    prompt_lower = prompt.lower()
    return any(re.search(pattern, prompt_lower) for pattern in CORRECTION_PATTERNS)


def classify_prompt(prompt: str) -> str:
    text = prompt.strip().lower()
    if not text:
        return "unknown"
    for category, patterns in PROMPT_CATEGORIES:
        if any(re.search(pattern, text) for pattern in patterns):
            return category
    return "general"


def safe_list(value: Any) -> list[Any]:
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def collect_paths(value: Any, results: set[str]) -> None:
    if isinstance(value, str):
        cleaned = value.strip()
        if cleaned:
            results.add(cleaned)
        return
    if isinstance(value, dict):
        for key in ("filePath", "file_path", "path", "paths", "filePaths", "files", "file", "dirPath"):
            if key in value:
                collect_paths(value[key], results)
        return
    if isinstance(value, list):
        for item in value:
            collect_paths(item, results)


def extract_patch_paths(patch_text: str) -> list[str]:
    paths: list[str] = []
    for line in patch_text.splitlines():
        if line.startswith("*** Update File: ") or line.startswith("*** Add File: ") or line.startswith("*** Delete File: "):
            remainder = line.split(": ", 1)[1]
            path_text = remainder.split(" -> ", 1)[0].strip()
            if path_text:
                paths.append(path_text)
    return paths


def extract_files_from_tool_input(tool_name: str, tool_input: dict[str, Any]) -> list[str]:
    results: set[str] = set()
    collect_paths(tool_input, results)
    if tool_name in {"Edit", "apply_patch"}:
        patch_text = first_present(tool_input, "input", "patch", default="")
        if patch_text:
            results.update(extract_patch_paths(str(patch_text)))
    return sorted(results)


def shell_quote(value: str) -> str:
    return value.replace("'", "'\\''")


def run_git(cwd: str, args: list[str]) -> str:
    if not cwd or not os.path.isdir(cwd):
        return ""
    try:
        result = subprocess.run(
            ["git", *args],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=2,
            check=False,
        )
    except Exception:
        return ""
    if result.returncode != 0:
        return ""
    return result.stdout.strip()


def get_repo_details(cwd: str) -> dict[str, Any]:
    repo_root = run_git(cwd, ["rev-parse", "--show-toplevel"])
    branch = run_git(cwd, ["rev-parse", "--abbrev-ref", "HEAD"]) if repo_root else ""
    status = run_git(cwd, ["status", "--porcelain"]) if repo_root else ""
    project_path = repo_root or cwd or str(Path.home())
    project_name = Path(project_path).name or "unknown"
    dirty_file_count = len([line for line in status.splitlines() if line.strip()]) if status else 0
    return {
        "projectPath": project_path,
        "projectName": project_name,
        "repoRoot": repo_root,
        "branch": branch,
        "dirtyFileCount": dirty_file_count,
    }


def new_session(session_id: str, cwd: str, timestamp: str) -> dict[str, Any]:
    repo_details = get_repo_details(cwd)
    return {
        "sessionId": session_id,
        "source": "copilot-hook",
        "startedAt": timestamp,
        "lastEventAt": timestamp,
        "cwd": cwd,
        **repo_details,
        "firstPrompt": "",
        "promptCount": 0,
        "prompts": [],
        "slashCommandCounts": {},
        "promptCategories": {},
        "correctionSignals": 0,
        "toolAttempts": {},
        "toolSuccesses": {},
        "failureSuspects": 0,
        "failureCategories": {},
        "pendingTools": {},
        "filesTouched": {},
        "notableCommands": [],
        "gitCommits": 0,
        "gitPushes": 0,
        "deployCommands": 0,
        "compactions": 0,
    }


def load_session(session_id: str, cwd: str, timestamp: str) -> tuple[Path, dict[str, Any]]:
    ensure_dirs()
    live_path = LIVE_DIR / f"{session_id}.json"
    if live_path.exists():
        return live_path, load_json(live_path, new_session(session_id, cwd, timestamp))
    session_path = SESSIONS_DIR / f"{session_id}.json"
    if session_path.exists():
        return session_path, load_json(session_path, new_session(session_id, cwd, timestamp))
    return live_path, new_session(session_id, cwd, timestamp)


def save_session(path: Path, session: dict[str, Any]) -> None:
    session["lastEventAt"] = session.get("lastEventAt") or iso_now()
    write_json(path, session)


def error_like_response(tool_name: str, tool_response: Any) -> bool:
    if tool_name not in {"Bash", "run_in_terminal", "Edit", "Write", "apply_patch"}:
        return False
    if tool_response in (None, "", {}):
        return False
    if isinstance(tool_response, (dict, list)):
        response_text = json.dumps(tool_response, ensure_ascii=False)
    else:
        response_text = str(tool_response)
    response_text = response_text.lower()
    exit_code_match = re.search(r"command exited with code\s+(\d+)", response_text)
    if exit_code_match:
        return exit_code_match.group(1) != "0"
    markers = [
        "traceback",
        "exception",
        "permission denied",
        "timed out",
        "timeout",
        "command exited with code",
        "no such file or directory",
        "json parse error",
    ]
    return any(marker in response_text for marker in markers)


def update_from_prompt(session: dict[str, Any], prompt: str, timestamp: str) -> None:
    prompt_text = squeeze_text(prompt)
    if not prompt_text:
        return
    session["promptCount"] = int(session.get("promptCount", 0)) + 1
    if not session.get("firstPrompt"):
        session["firstPrompt"] = prompt_text
    category = classify_prompt(prompt_text)
    increment(session["promptCategories"], category)
    correction = detect_correction(prompt_text)
    if correction:
        session["correctionSignals"] = int(session.get("correctionSignals", 0)) + 1
    for command_name in extract_slash_commands(prompt_text):
        increment(session["slashCommandCounts"], command_name)
    prompts = session.setdefault("prompts", [])
    if len(prompts) < MAX_PROMPTS_PER_SESSION:
        prompts.append({
            "at": timestamp,
            "text": prompt_text,
            "category": category,
            "correction": correction,
        })


def update_from_pretool(session: dict[str, Any], tool_name: str, tool_use_id: str, timestamp: str) -> None:
    increment(session["toolAttempts"], tool_name)
    if tool_use_id:
        session.setdefault("pendingTools", {})[tool_use_id] = {"tool": tool_name, "at": timestamp}


def update_from_posttool(session: dict[str, Any], tool_name: str, tool_use_id: str, tool_input: dict[str, Any], tool_response: Any) -> None:
    increment(session["toolSuccesses"], tool_name)
    pending = session.setdefault("pendingTools", {})
    if tool_use_id and tool_use_id in pending:
        pending.pop(tool_use_id, None)
    for path_text in extract_files_from_tool_input(tool_name, tool_input):
        increment(session["filesTouched"], path_text)
    if tool_name == "Bash":
        command_text = squeeze_text(first_present(tool_input, "command", default=""), limit=180)
        if command_text:
            commands = session.setdefault("notableCommands", [])
            if len(commands) < MAX_NOTABLE_COMMANDS and command_text not in commands:
                commands.append(command_text)
            lower_command = command_text.lower()
            if "git commit" in lower_command:
                session["gitCommits"] = int(session.get("gitCommits", 0)) + 1
            if "git push" in lower_command:
                session["gitPushes"] = int(session.get("gitPushes", 0)) + 1
            if any(keyword in lower_command for keyword in ("deploy", "wrangler", "cloudflare", "pages deploy")):
                session["deployCommands"] = int(session.get("deployCommands", 0)) + 1
    if error_like_response(tool_name, tool_response):
        session["failureSuspects"] = int(session.get("failureSuspects", 0)) + 1
        increment(session["failureCategories"], tool_name)


def finalize_session(session: dict[str, Any], timestamp: str) -> dict[str, Any]:
    started_at = parse_timestamp(session.get("startedAt"))
    stopped_at = parse_timestamp(timestamp)
    pending_tools = session.get("pendingTools", {}) or {}
    if pending_tools:
        session["failureSuspects"] = int(session.get("failureSuspects", 0)) + len(pending_tools)
        for pending_payload in pending_tools.values():
            increment(session["failureCategories"], pending_payload.get("tool", "unknown"))
    session["pendingToolCount"] = len(pending_tools)
    session["pendingTools"] = {}
    session["stoppedAt"] = timestamp
    session["durationMinutes"] = max(0, round((stopped_at - started_at).total_seconds() / 60))
    session["filesTouchedCount"] = len(session.get("filesTouched", {}))
    session["toolCount"] = sum(int(value) for value in session.get("toolSuccesses", {}).values())
    return session


def pick_top_items(counter_like: dict[str, int] | Counter[str], limit: int = 8) -> list[dict[str, Any]]:
    counter = Counter(counter_like)
    return [{"name": key, "count": count} for key, count in counter.most_common(limit)]


def summarize_hook_session(session: dict[str, Any]) -> dict[str, Any]:
    prompt_categories = Counter(session.get("promptCategories", {}))
    top_category = prompt_categories.most_common(1)[0][0] if prompt_categories else "unknown"
    return {
        "source": "hook",
        "sessionId": session.get("sessionId", ""),
        "startedAt": session.get("startedAt", ""),
        "projectName": session.get("projectName", "unknown"),
        "projectPath": session.get("projectPath", ""),
        "branch": session.get("branch", ""),
        "firstPrompt": squeeze_text(session.get("firstPrompt", "")),
        "promptCount": int(session.get("promptCount", 0)),
        "category": top_category,
        "errors": int(session.get("failureSuspects", 0)),
        "correctionSignals": int(session.get("correctionSignals", 0)),
        "tools": session.get("toolSuccesses", {}) or session.get("toolAttempts", {}),
        "slashCommands": session.get("slashCommandCounts", {}),
        "filesTouchedCount": int(session.get("filesTouchedCount", len(session.get("filesTouched", {})))),
        "durationMinutes": int(session.get("durationMinutes", 0)),
    }


def summarize_legacy_session(session: dict[str, Any]) -> dict[str, Any]:
    project_path = str(session.get("project_path", "") or "")
    project_name = Path(project_path).name or "unknown"
    first_prompt = squeeze_text(session.get("first_prompt", ""))
    return {
        "source": "legacy-session-meta",
        "sessionId": session.get("session_id", ""),
        "startedAt": session.get("start_time", ""),
        "projectName": project_name,
        "projectPath": project_path,
        "branch": "",
        "firstPrompt": first_prompt,
        "promptCount": int(session.get("user_message_count", 0)),
        "category": classify_prompt(first_prompt),
        "errors": int(session.get("tool_errors", 0)),
        "correctionSignals": 0,
        "tools": session.get("tool_counts", {}),
        "slashCommands": {command: 1 for command in extract_slash_commands(first_prompt)},
        "filesTouchedCount": int(session.get("files_modified", 0)),
        "durationMinutes": int(session.get("duration_minutes", 0)),
    }


def sorted_recent_json_files(directory: Path, limit: int) -> list[Path]:
    if not directory.exists():
        return []
    files = [path for path in directory.glob("*.json") if path.is_file()]
    files.sort(key=lambda path: path.stat().st_mtime, reverse=True)
    return files[:limit]


def load_hook_sessions() -> list[dict[str, Any]]:
    sessions: list[dict[str, Any]] = []
    for path in sorted_recent_json_files(SESSIONS_DIR, MAX_RECENT_HOOK_SESSIONS):
        payload = load_json(path, {})
        if payload:
            sessions.append(payload)
    return sessions


def load_legacy_sessions() -> list[dict[str, Any]]:
    sessions: list[dict[str, Any]] = []
    for path in sorted_recent_json_files(LEGACY_SESSION_META_DIR, MAX_RECENT_LEGACY_SESSIONS):
        payload = load_json(path, {})
        if payload:
            sessions.append(payload)
    return sessions


def aggregate_sessions(hook_sessions: list[dict[str, Any]], legacy_sessions: list[dict[str, Any]]) -> dict[str, Any]:
    project_counter: Counter[str] = Counter()
    project_error_counter: Counter[str] = Counter()
    tool_counter: Counter[str] = Counter()
    category_counter: Counter[str] = Counter()
    slash_counter: Counter[str] = Counter()
    correction_signal_count = 0
    continuation_count = 0
    high_error_sessions: list[dict[str, Any]] = []

    recent_hook = [summarize_hook_session(session) for session in hook_sessions]
    recent_legacy = [summarize_legacy_session(session) for session in legacy_sessions]

    for record in recent_hook + recent_legacy:
        project_name = record.get("projectName", "unknown") or "unknown"
        project_counter[project_name] += 1
        category_counter[record.get("category", "unknown") or "unknown"] += 1
        correction_signal_count += int(record.get("correctionSignals", 0))
        if record.get("category") == "continuation":
            continuation_count += 1
        for tool_name, count in (record.get("tools") or {}).items():
            tool_counter[str(tool_name)] += int(count)
        for command_name, count in (record.get("slashCommands") or {}).items():
            slash_counter[str(command_name)] += int(count)
        errors = int(record.get("errors", 0))
        if errors > 0:
            project_error_counter[project_name] += errors
            high_error_sessions.append({
                "startedAt": record.get("startedAt", ""),
                "projectName": project_name,
                "category": record.get("category", "unknown"),
                "errors": errors,
                "source": record.get("source", ""),
                "firstPrompt": record.get("firstPrompt", ""),
            })

    high_error_sessions.sort(key=lambda item: (item["errors"], item["startedAt"]), reverse=True)

    pattern_candidates: list[str] = []
    if category_counter.get("implement-build", 0) >= 3:
        pattern_candidates.append(
            f"Implementation/build requests dominate the recent sample ({category_counter['implement-build']} sessions)."
        )
    if category_counter.get("review-audit", 0) >= 2:
        pattern_candidates.append(
            f"Review/audit work recurs across sessions ({category_counter['review-audit']} sessions)."
        )
    if correction_signal_count >= 2:
        pattern_candidates.append(
            f"Correction signals appeared in {correction_signal_count} recent hook prompts."
        )
    if continuation_count >= 2:
        pattern_candidates.append(
            f"Short continuation prompts recur ({continuation_count} sessions)."
        )
    if high_error_sessions and len(high_error_sessions) >= 3:
        pattern_candidates.append(
            f"Error-heavy sessions recur across {len({item['projectName'] for item in high_error_sessions})} projects."
        )
    if slash_counter:
        top_command = slash_counter.most_common(1)[0]
        pattern_candidates.append(
            f"Slash command adoption is visible; /{top_command[0]} appears {top_command[1]} times in the recent sample."
        )

    return {
        "updatedAt": iso_now(),
        "hookSessionsAnalyzed": len(recent_hook),
        "legacySessionsAnalyzed": len(recent_legacy),
        "topProjects": pick_top_items(project_counter),
        "topProjectErrors": pick_top_items(project_error_counter),
        "topTools": pick_top_items(tool_counter),
        "topPromptCategories": pick_top_items(category_counter),
        "slashCommands": pick_top_items(slash_counter),
        "correctionSignalCount": correction_signal_count,
        "continuationCount": continuation_count,
        "highErrorSessions": high_error_sessions[:12],
        "recentHookSessions": recent_hook[:12],
        "recentLegacySessions": recent_legacy[:12],
        "patternCandidates": pattern_candidates,
    }


def format_counter_items(items: list[dict[str, Any]]) -> list[str]:
    if not items:
        return ["- none"]
    return [f"- {item['name']}: {item['count']}" for item in items]


def format_session_lines(records: list[dict[str, Any]]) -> list[str]:
    if not records:
        return ["- none"]
    lines: list[str] = []
    for record in records:
        started = squeeze_text(record.get("startedAt", ""), limit=24)
        project_name = squeeze_text(record.get("projectName", "unknown"), limit=40)
        category = squeeze_text(record.get("category", "unknown"), limit=24)
        prompt = squeeze_text(record.get("firstPrompt", ""), limit=120)
        errors = int(record.get("errors", 0))
        lines.append(
            f"- {started} | {project_name} | {category} | errors={errors} | {prompt or 'No prompt captured'}"
        )
    return lines


def write_digest(signals: dict[str, Any]) -> None:
    digest_lines: list[str] = [
        "# Copilot Learning Digest",
        f"- Updated: {signals['updatedAt']}",
        f"- Hook sessions analyzed: {signals['hookSessionsAnalyzed']}",
        f"- Historical session-meta sample analyzed: {signals['legacySessionsAnalyzed']}",
        f"- Recent correction signals: {signals['correctionSignalCount']}",
        f"- Continuation-style sessions: {signals['continuationCount']}",
        "",
        "## Top Projects",
        *format_counter_items(signals.get("topProjects", [])),
        "",
        "## Top Project Error Hotspots",
        *format_counter_items(signals.get("topProjectErrors", [])),
        "",
        "## Top Prompt Categories",
        *format_counter_items(signals.get("topPromptCategories", [])),
        "",
        "## Top Tools",
        *format_counter_items(signals.get("topTools", [])),
        "",
        "## Slash Commands",
        *format_counter_items(signals.get("slashCommands", [])),
        "",
        "## High-Error Sessions",
        *format_session_lines(signals.get("highErrorSessions", [])),
        "",
        "## Recent Hook Sessions",
        *format_session_lines(signals.get("recentHookSessions", [])),
        "",
        "## Historical Session-Meta Sample",
        *format_session_lines(signals.get("recentLegacySessions", [])),
        "",
        "## Pattern Candidates",
    ]
    pattern_candidates = signals.get("patternCandidates", [])
    if pattern_candidates:
        digest_lines.extend(f"- {candidate}" for candidate in pattern_candidates)
    else:
        digest_lines.append("- none")
    DIGEST_PATH.write_text("\n".join(digest_lines) + "\n", encoding="utf-8")
    write_json(SIGNALS_PATH, signals)


def rebuild_digest() -> None:
    hook_sessions = load_hook_sessions()
    legacy_sessions = load_legacy_sessions()
    signals = aggregate_sessions(hook_sessions, legacy_sessions)
    write_digest(signals)


def main() -> None:
    try:
        hook_input = json.load(sys.stdin)
    except Exception:
        print("{}")
        return

    try:
        event_name = first_present(hook_input, "hookEventName", "hook_event_name", default="")
        session_id = first_present(hook_input, "sessionId", "session_id", default="")
        timestamp = first_present(hook_input, "timestamp", default=iso_now())
        cwd = first_present(hook_input, "cwd", default=str(Path.home()))
        if not session_id or not event_name:
            print("{}")
            return

        session_path, session = load_session(session_id, cwd, timestamp)
        session["lastEventAt"] = timestamp
        session["cwd"] = cwd
        if event_name == "SessionStart":
            repo_details = get_repo_details(cwd)
            session.update(repo_details)
            if not DIGEST_PATH.exists():
                rebuild_digest()
        elif event_name == "UserPromptSubmit":
            prompt = first_present(hook_input, "prompt", "user_message", default="")
            update_from_prompt(session, str(prompt), timestamp)
            if not DIGEST_PATH.exists():
                rebuild_digest()
        elif event_name == "PreToolUse":
            tool_name = canonical_tool_name(first_present(hook_input, "tool_name", "toolName", default="unknown"))
            tool_use_id = first_present(hook_input, "tool_use_id", "toolUseId", default="")
            update_from_pretool(session, tool_name, str(tool_use_id), timestamp)
        elif event_name == "PostToolUse":
            tool_name = canonical_tool_name(first_present(hook_input, "tool_name", "toolName", default="unknown"))
            tool_use_id = first_present(hook_input, "tool_use_id", "toolUseId", default="")
            tool_input = first_present(hook_input, "tool_input", "toolInput", default={}) or {}
            if not isinstance(tool_input, dict):
                tool_input = {}
            tool_response = first_present(hook_input, "tool_response", "toolResponse", default=None)
            update_from_posttool(session, tool_name, str(tool_use_id), tool_input, tool_response)
        elif event_name == "PreCompact":
            session["compactions"] = int(session.get("compactions", 0)) + 1
        elif event_name == "Stop":
            if first_present(hook_input, "stop_hook_active", "stopHookActive", default=False):
                print("{}")
                return
            finalized = finalize_session(session, timestamp)
            final_path = SESSIONS_DIR / f"{session_id}.json"
            save_session(final_path, finalized)
            if session_path.exists() and session_path != final_path:
                session_path.unlink(missing_ok=True)
            rebuild_digest()
            print("{}")
            return

        save_session(session_path, session)
    except Exception as exc:
        log_internal_error(f"copilot-learning-log failure: {exc}")

    print("{}")


if __name__ == "__main__":
    main()
