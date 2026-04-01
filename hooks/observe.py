#!/usr/bin/env python3
"""PostToolUse observer — captures meaningful context from tool usage.

Records WHAT happened (not just which tool ran) so future sessions can
search observations semantically. Extracts:
- Files created/modified and why
- Commands run and their outcomes
- Decisions made (commit messages, config changes)
- Errors encountered

Stores observations as JSONL with rich text summaries alongside the raw
tool data. Kept lightweight (<50ms) by doing string extraction, not LLM calls.

Exit code 0 always.
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

tool_name = input_data.get("tool_name", "unknown")
tool_input = input_data.get("tool_input", {})
tool_response = input_data.get("tool_response", {})

# Skip read-only tools and internal tools — they don't produce observations worth storing
skip_tools = {"Glob", "Grep", "Read", "ToolSearch", "WebFetch", "WebSearch", "TodoWrite", "SendMessage"}
if tool_name in skip_tools:
    sys.exit(0)

# Skip MCP read-only tools (list/get/read/search operations)
if tool_name.startswith("mcp__") and any(
    op in tool_name for op in ["_read", "_list", "_get", "_search", "_fetch", "_find", "_context"]
):
    sys.exit(0)

# === Extract meaningful context based on tool type ===

summary = None
tags = []
file_path = None

if tool_name in ("Write", "Edit"):
    file_path = tool_input.get("file_path", "")
    fname = os.path.basename(file_path)
    if tool_name == "Write":
        # New file or full rewrite
        content = tool_input.get("content", "")
        lines = len(content.splitlines())
        summary = f"Created/rewrote {fname} ({lines} lines)"
        tags = ["file-write", fname]
    else:
        old = tool_input.get("old_string", "")[:80]
        new = tool_input.get("new_string", "")[:80]
        summary = f"Edited {fname}: '{old}' → '{new}'"
        tags = ["file-edit", fname]

elif tool_name == "Bash":
    cmd = tool_input.get("command", "")
    # Extract meaningful commands, skip trivial ones
    trivial_prefixes = (
        "ls", "pwd", "echo", "cat ", "head ", "tail ", "which ", "wc ",
        "test ", "[ ", "true", "false", "mkdir ", "cd ", "rm -rf /tmp/",
        "python3 -c", "node -e",  # one-liner checks
    )
    if any(cmd.startswith(skip) for skip in trivial_prefixes):
        sys.exit(0)
    # Skip short commands that are just checks (< 40 chars, no side effects)
    if len(cmd) < 40 and not any(w in cmd for w in ("commit", "push", "deploy", "install", "write", "mv ", "cp ")):
        sys.exit(0)

    # Capture git commits specifically — these are decisions
    if "git commit" in cmd:
        summary = f"Git commit: {cmd[:200]}"
        tags = ["git-commit", "decision"]
    elif "git push" in cmd:
        summary = f"Pushed to remote: {cmd[:150]}"
        tags = ["git-push", "deploy"]
    elif cmd.startswith(("npm ", "npx ", "pip ", "python3 ", "node ")):
        summary = f"Ran: {cmd[:200]}"
        tags = ["command"]
        # Check for errors in response
        resp_str = str(tool_response)[:500] if tool_response else ""
        if "error" in resp_str.lower() or "Error" in resp_str:
            tags.append("error")
            summary += " [HAD ERRORS]"
    elif "deploy" in cmd.lower() or "wrangler" in cmd.lower():
        summary = f"Deploy: {cmd[:200]}"
        tags = ["deploy", "decision"]
    else:
        summary = f"Command: {cmd[:200]}"
        tags = ["command"]

elif tool_name == "Agent":
    prompt = tool_input.get("prompt", "")[:200]
    agent_type = tool_input.get("subagent_type", "general")
    summary = f"Spawned {agent_type} agent: {prompt}"
    tags = ["agent", agent_type]

elif tool_name == "Skill":
    skill = tool_input.get("skill", "")
    args = tool_input.get("args", "")
    summary = f"Invoked /{skill} {args}".strip()
    tags = ["skill", skill]

elif tool_name == "TodoWrite":
    # Skip — internal tracking, not meaningful context
    sys.exit(0)

else:
    # Generic fallback
    summary = f"{tool_name}: {str(tool_input)[:150]}"
    tags = [tool_name.lower()]

if not summary:
    sys.exit(0)

# === Detect project ===

homunculus_dir = Path.home() / ".claude" / "homunculus"
project_dir = homunculus_dir
cache_file = homunculus_dir / ".project_cache.json"
cwd = os.getcwd()
project_name = os.path.basename(cwd)

try:
    homunculus_dir.mkdir(parents=True, exist_ok=True)
    project_cache = {}
    if cache_file.exists():
        try:
            project_cache = json.loads(cache_file.read_text())
        except json.JSONDecodeError:
            project_cache = {}

    if cwd in project_cache:
        project_hash = project_cache[cwd]
        project_dir = homunculus_dir / "projects" / project_hash
        project_dir.mkdir(parents=True, exist_ok=True)
    else:
        import subprocess
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=2, cwd=cwd
        )
        if result.returncode == 0:
            remote_url = result.stdout.strip()
            project_hash = hashlib.sha256(remote_url.encode()).hexdigest()[:12]
            project_dir = homunculus_dir / "projects" / project_hash
            project_dir.mkdir(parents=True, exist_ok=True)

            project_cache[cwd] = project_hash
            cache_file.write_text(json.dumps(project_cache, indent=2))

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

            project_name = registry.get(project_hash, {}).get("name", project_name)
except Exception:
    pass

# === Record observation ===

observation = {
    "ts": datetime.now().isoformat(),
    "project": project_name,
    "tool": tool_name,
    "summary": summary,
    "tags": tags,
}
if file_path:
    observation["file"] = file_path

obs_file = project_dir / "observations.jsonl"
try:
    with open(obs_file, "a") as f:
        f.write(json.dumps(observation) + "\n")
except Exception:
    pass

# === Rotate if too large (>5000 lines → keep last 2000) ===
try:
    lines = obs_file.read_text().splitlines()
    if len(lines) > 5000:
        obs_file.write_text("\n".join(lines[-2000:]) + "\n")
except Exception:
    pass

sys.exit(0)
