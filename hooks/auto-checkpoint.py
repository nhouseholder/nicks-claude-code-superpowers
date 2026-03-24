#!/usr/bin/env python3
"""
Auto-Checkpoint — Rich state dump after every Opus response.
Writes ~/.claude/last-checkpoint.json with everything GLM-5 needs
to seamlessly continue: task state, recent changes, active files.
"""
import json
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime


def run_cmd(cmd, timeout=3):
    """Run a shell command and return stdout, or empty string on failure."""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, shell=True)
        return r.stdout.strip() if r.returncode == 0 else ""
    except Exception:
        return ""


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

    if hook_input.get("hook_event_name") != "Stop":
        sys.exit(0)
    if hook_input.get("stop_hook_active"):
        sys.exit(0)

    transcript_path = hook_input.get("transcript_path", "")

    # Extract last user + assistant messages from transcript
    last_user = ""
    last_assistant = ""

    if transcript_path and Path(transcript_path).exists():
        try:
            r = subprocess.run(["tail", "-40", transcript_path],
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

    # Gather project state — git diff, status, recent files
    git_status = run_cmd("git status --short 2>/dev/null | head -20")
    git_diff_stat = run_cmd("git diff --stat 2>/dev/null | tail -5")
    recent_files = run_cmd("git diff --name-only 2>/dev/null | head -10")
    branch = run_cmd("git branch --show-current 2>/dev/null")

    checkpoint = {
        "timestamp": datetime.now().isoformat(),
        "model": os.environ.get("CLAUDE_MODEL", "unknown"),
        "project_dir": os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()),
        "transcript_path": transcript_path,
        "last_user_message": last_user,
        "last_assistant_response": last_assistant,
        "git_branch": branch,
        "git_status": git_status,
        "git_diff_stat": git_diff_stat,
        "modified_files": recent_files,
    }

    Path(os.path.expanduser("~/.claude/last-checkpoint.json")).write_text(
        json.dumps(checkpoint, indent=2)
    )

except Exception:
    pass
