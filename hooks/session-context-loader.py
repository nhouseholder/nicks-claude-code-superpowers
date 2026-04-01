#!/usr/bin/env python3
"""SessionStart hook: Inject recent project observations as context.

On session start, loads the last N significant observations for the current
project and injects them as context. This gives Claude immediate awareness
of what happened in recent sessions without needing to read handoffs.

Focuses on DECISIONS and ERRORS — the highest-value observations:
- Git commits (what was shipped)
- Deploys (what went live)
- Errors (what went wrong)
- Agent spawns (what complex tasks were attempted)

Keeps injection under 500 tokens to avoid bloating the context window.

Exit code 0 always.
"""
import json
import sys
import os
import hashlib
import subprocess
from datetime import datetime, timedelta
from pathlib import Path

MAX_OBSERVATIONS = 15  # Most recent significant observations
MAX_AGE_DAYS = 7       # Only show observations from last week
HIGH_VALUE_TAGS = {"git-commit", "deploy", "error", "decision", "skill"}

try:
    hook_input = json.load(sys.stdin)
except (json.JSONDecodeError, EOFError):
    hook_input = {}

if hook_input.get("hook_event_name") not in ("SessionStart", None):
    sys.exit(0)

# Skip if session ALREADY initialized recently (prevents double-fire after compaction)
# Lock age >2s means a prior init batch wrote it; <2s means we're in the same batch (proceed)
_lock = Path.home() / ".claude" / ".session-init-lock"
try:
    import time as _time
    if _lock.exists():
        _age = _time.time() - _lock.stat().st_mtime
        if 2 < _age < 60:
            sys.exit(0)
except OSError:
    pass

# Detect project
cwd = os.getcwd()
homunculus_dir = Path.home() / ".claude" / "homunculus"
cache_file = homunculus_dir / ".project_cache.json"
obs_file = homunculus_dir / "observations.jsonl"  # fallback

try:
    project_cache = {}
    if cache_file.exists():
        try:
            project_cache = json.loads(cache_file.read_text())
        except json.JSONDecodeError:
            pass

    if cwd in project_cache:
        project_hash = project_cache[cwd]
        candidate = homunculus_dir / "projects" / project_hash / "observations.jsonl"
        if candidate.exists():
            obs_file = candidate
    else:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=2, cwd=cwd
        )
        if result.returncode == 0:
            project_hash = hashlib.sha256(result.stdout.strip().encode()).hexdigest()[:12]
            candidate = homunculus_dir / "projects" / project_hash / "observations.jsonl"
            if candidate.exists():
                obs_file = candidate
except Exception:
    pass

if not obs_file.exists():
    sys.exit(0)

# Read observations, filter to recent + high-value
cutoff = datetime.now() - timedelta(days=MAX_AGE_DAYS)
significant = []

try:
    # Read last 200 lines (enough to find 15 significant ones)
    lines = obs_file.read_text().splitlines()[-200:]

    for line in reversed(lines):
        if len(significant) >= MAX_OBSERVATIONS:
            break
        try:
            obs = json.loads(line)
            ts = datetime.fromisoformat(obs["ts"])
            if ts < cutoff:
                continue

            tags = set(obs.get("tags", []))
            # Prioritize high-value observations
            if tags & HIGH_VALUE_TAGS or "error" in obs.get("summary", "").lower():
                significant.append(obs)
            elif len(significant) < 5:
                # Fill remaining slots with any observation
                significant.append(obs)
        except (json.JSONDecodeError, KeyError, ValueError):
            continue

except Exception:
    sys.exit(0)

if not significant:
    sys.exit(0)

significant.reverse()  # Chronological order

# Format context injection
project_name = significant[0].get("project", os.path.basename(cwd))
lines_out = [f"RECENT ACTIVITY ({project_name}, last {MAX_AGE_DAYS}d):"]

for obs in significant:
    date = obs["ts"][:10]
    summary = obs.get("summary", "")[:120]
    tags = obs.get("tags", [])
    marker = ""
    if "error" in tags:
        marker = " ⚠️"
    elif "deploy" in tags:
        marker = " 🚀"
    elif "git-commit" in tags or "decision" in tags:
        marker = " ✓"
    lines_out.append(f"  [{date}] {summary}{marker}")

context = "\n".join(lines_out)

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": context
    }
}))

sys.exit(0)
