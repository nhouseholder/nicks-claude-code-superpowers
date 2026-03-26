#!/usr/bin/env python3
"""
Background observation hook for continuous learning.
Captures tool usage patterns and stores them for later analysis.
Runs on PostToolUse — lightweight, non-blocking.
"""
import json
import sys
import os
import hashlib
from datetime import datetime
from pathlib import Path

try:
    input_data = json.load(sys.stdin)
except (json.JSONDecodeError, EOFError):
    sys.exit(0)

# Get tool info
tool_name = input_data.get("tool_name", "unknown")
tool_input = input_data.get("tool_input", {})

# Skip noisy/trivial tool calls
skip_tools = {"Glob", "Grep", "Read", "ToolSearch"}
if tool_name in skip_tools:
    sys.exit(0)

# Detect project
homunculus_dir = Path.home() / ".claude" / "homunculus"
project_dir = homunculus_dir

try:
    import subprocess
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"],
        capture_output=True, text=True, timeout=2
    )
    if result.returncode == 0:
        remote_url = result.stdout.strip()
        project_hash = hashlib.sha256(remote_url.encode()).hexdigest()[:12]
        project_dir = homunculus_dir / "projects" / project_hash
        project_dir.mkdir(parents=True, exist_ok=True)

        # Save project registry
        registry_file = homunculus_dir / "projects.json"
        registry = {}
        if registry_file.exists():
            try:
                registry = json.loads(registry_file.read_text())
            except json.JSONDecodeError:
                registry = {}
        if project_hash not in registry:
            repo_root = subprocess.run(
                ["git", "rev-parse", "--show-toplevel"],
                capture_output=True, text=True, timeout=2
            ).stdout.strip()
            registry[project_hash] = {
                "name": os.path.basename(repo_root),
                "path": repo_root,
                "remote": remote_url
            }
            registry_file.write_text(json.dumps(registry, indent=2))
except Exception:
    pass

# Record observation
observation = {
    "timestamp": datetime.now().isoformat(),
    "tool": tool_name,
    "input_summary": str(tool_input)[:200],
}

obs_file = project_dir / "observations.jsonl"
try:
    with open(obs_file, "a") as f:
        f.write(json.dumps(observation) + "\n")
except Exception:
    pass

sys.exit(0)
