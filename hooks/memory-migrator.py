#!/usr/bin/env python3
"""SessionStart hook: Migrate orphaned project memories when paths change.

Problem: Claude Code keys project memory dirs by the RESOLVED file path.
When iCloud paths change (ProjectsHQ → Projects, symlink targets change),
new dirs are created and old memories become invisible.

Fix: On session start, detect the current project (by git remote repo name
or directory basename), search ALL project memory dirs for matching project
names, and copy any missing memory files into the current session's dir.
Also merges MEMORY.md indexes.

This ensures memories follow the PROJECT, not the PATH.

Exit code 0 always (context injection only).
"""
import json
import os
import sys
import re
import shutil
import subprocess
from pathlib import Path
from datetime import datetime


PROJECTS_DIR = Path(os.path.expanduser("~/.claude/projects"))
LOG_FILE = Path(os.path.expanduser("~/.claude/memory-migrator.log"))


def log(msg):
    """Append to log file for debugging."""
    try:
        with open(LOG_FILE, "a") as f:
            f.write(f"[{datetime.now().isoformat()}] {msg}\n")
    except OSError:
        pass


def get_project_identifiers():
    """Get project identifiers from the current working directory.

    Returns a set of lowercase strings that identify this project:
    - git remote repo name (most reliable)
    - directory basename
    - site name from site-to-repo-map.json
    """
    identifiers = set()
    cwd = os.getcwd()

    # Directory basename
    basename = os.path.basename(cwd).lower()
    if basename:
        identifiers.add(basename)

    # Git remote repo name
    try:
        result = subprocess.run(
            ["git", "remote", "get-url", "origin"],
            capture_output=True, text=True, timeout=5, cwd=cwd
        )
        if result.returncode == 0:
            remote = result.stdout.strip()
            # Extract repo name from URL
            repo_name = remote.rstrip("/").rsplit("/", 1)[-1]
            repo_name = repo_name.replace(".git", "").lower()
            if repo_name:
                identifiers.add(repo_name)
    except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
        pass

    # Site-to-repo mapping
    try:
        map_path = os.path.expanduser("~/Projects/site-to-repo-map.json")
        with open(map_path) as f:
            data = json.load(f)
        for site, info in data.get("sites", {}).items():
            repo = info.get("github_repo", "").lower()
            local = info.get("local_path", "").lower()
            if basename in repo or basename in local or repo in identifiers:
                identifiers.add(site.lower().replace(".", "-"))
                identifiers.add(repo)
                # Also add the local path basename
                if local:
                    identifiers.add(os.path.basename(local))
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass

    return identifiers


def get_current_memory_dir():
    """Get the memory directory Claude Code would use for the current session."""
    cwd = os.getcwd()
    # Claude Code encodes the path: / → - , leading - stripped
    # But the actual encoding replaces / with - and strips leading -
    encoded = cwd.replace("/", "-").lstrip("-")
    return PROJECTS_DIR / encoded / "memory"


def find_matching_memory_dirs(identifiers):
    """Find all project memory dirs that match any of our identifiers."""
    matching = []

    if not PROJECTS_DIR.exists():
        return matching

    for project_dir in PROJECTS_DIR.iterdir():
        if not project_dir.is_dir():
            continue

        memory_dir = project_dir / "memory"
        if not memory_dir.exists():
            continue

        # Check if any identifier appears in the dir name
        dir_name_lower = project_dir.name.lower()
        for ident in identifiers:
            if ident in dir_name_lower:
                matching.append(memory_dir)
                break

    return matching


def parse_memory_index(memory_md_path):
    """Parse a MEMORY.md file into a dict of {filename: full_line}."""
    entries = {}
    try:
        content = memory_md_path.read_text()
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            # Extract filename from markdown link: [Title](filename.md)
            match = re.search(r'\[([^\]]+)\]\(([^)]+)\)', line)
            if match:
                filename = match.group(2)
                entries[filename] = line
            else:
                # Non-link line, keep as-is with a hash key
                entries[f"_line_{hash(line)}"] = line
    except (FileNotFoundError, OSError):
        pass
    return entries


def migrate_memories(current_dir, all_dirs):
    """Copy missing memory files from old dirs to current dir.
    Returns list of migrated files."""
    migrated = []
    current_dir.mkdir(parents=True, exist_ok=True)

    # Get existing files in current dir
    current_files = {f.name for f in current_dir.iterdir() if f.is_file()} if current_dir.exists() else set()

    # Collect all index entries from all dirs
    all_index_entries = {}

    for memory_dir in all_dirs:
        if memory_dir == current_dir:
            continue

        if not memory_dir.exists():
            continue

        # Collect index entries
        index_path = memory_dir / "MEMORY.md"
        if index_path.exists():
            entries = parse_memory_index(index_path)
            for filename, line in entries.items():
                if filename not in all_index_entries:
                    all_index_entries[filename] = line

        # Copy missing memory files (not MEMORY.md itself, not handoffs, not archived)
        for f in memory_dir.iterdir():
            if not f.is_file():
                continue
            if f.name == "MEMORY.md":
                continue
            if "ARCHIVED" in f.name:
                continue
            if f.name in current_files:
                continue

            try:
                shutil.copy2(f, current_dir / f.name)
                migrated.append(f.name)
                current_files.add(f.name)
                log(f"Migrated: {f} → {current_dir / f.name}")
            except OSError as e:
                log(f"Failed to migrate {f}: {e}")

    # Merge MEMORY.md indexes
    if migrated or all_index_entries:
        current_index_path = current_dir / "MEMORY.md"
        current_entries = parse_memory_index(current_index_path)

        # Add entries from old dirs that reference files we now have
        added_entries = []
        for filename, line in all_index_entries.items():
            if filename.startswith("_line_"):
                continue
            if filename in current_entries:
                continue
            # Only add if the file exists in current dir
            if (current_dir / filename).exists():
                current_entries[filename] = line
                added_entries.append(filename)

        if added_entries:
            # Rebuild MEMORY.md
            header = "# Memory Index\n\n"
            lines = []
            for filename, line in sorted(current_entries.items()):
                if filename.startswith("_line_"):
                    lines.append(line)
                else:
                    lines.append(line)

            current_index_path.write_text(header + "\n".join(lines) + "\n")
            log(f"Updated MEMORY.md with {len(added_entries)} new entries: {added_entries}")

    return migrated


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        hook_input = {}

    # Only run on SessionStart
    if hook_input.get("hook_event_name") not in ("SessionStart", None):
        sys.exit(0)

    identifiers = get_project_identifiers()
    if not identifiers:
        sys.exit(0)

    log(f"Project identifiers: {identifiers}")

    current_dir = get_current_memory_dir()
    all_dirs = find_matching_memory_dirs(identifiers)

    if len(all_dirs) <= 1:
        # No fragmentation — nothing to migrate
        sys.exit(0)

    log(f"Found {len(all_dirs)} matching memory dirs: {[str(d) for d in all_dirs]}")

    migrated = migrate_memories(current_dir, all_dirs)

    if migrated:
        context = (
            f"MEMORY MIGRATION: Found {len(all_dirs)} memory directories for this project "
            f"(path changes created duplicates). Migrated {len(migrated)} orphaned memory files "
            f"into the current session's memory: {', '.join(migrated)}. "
            f"All project memories are now consolidated."
        )
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "SessionStart",
                "additionalContext": context
            }
        }))
        log(f"Migration complete: {len(migrated)} files migrated")
    else:
        log("No migration needed — all memories already present")

    sys.exit(0)


if __name__ == "__main__":
    main()
