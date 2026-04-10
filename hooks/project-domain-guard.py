#!/usr/bin/env python3
"""
Project Domain Guard — Warns when prompt references domain terms that
don't match the current cwd's project. Non-blocking.

Fires on UserPromptSubmit. Never exits non-zero.

Example: cwd = ~/ProjectsHQ/superpowers, prompt = "test H16 backtest"
-> Injects yellow-flag warning telling Claude to confirm cwd with user
   before acting on UFC-specific logic.
"""
import json
import os
import re
import sys

CONFIG = os.path.expanduser("~/.claude/project-domains.json")

try:
    input_data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

prompt = input_data.get("prompt", "").strip()
if not prompt or prompt.startswith("/") or prompt.startswith("#"):
    sys.exit(0)

# Load domain map
try:
    with open(CONFIG, "r") as f:
        domains = json.load(f)
except Exception:
    sys.exit(0)

cwd = os.getcwd().lower()
prompt_lower = prompt.lower()

# Detect current project from cwd
current_project = None
for name, cfg in domains.items():
    if any(sig in cwd for sig in cfg["dir_signals"]):
        current_project = name
        break

# Detect projects referenced by prompt domain terms
hit_projects = {}
for name, cfg in domains.items():
    hits = [
        term for term in cfg["domain_terms"]
        if re.search(r"\b" + re.escape(term) + r"\b", prompt_lower)
    ]
    if hits:
        hit_projects[name] = hits

# No domain hits: silent pass
if not hit_projects:
    sys.exit(0)

# Prompt references current project: fine, pass
if current_project and current_project in hit_projects:
    sys.exit(0)

# SAFETY NET: if cwd IS a known project, require signature-level evidence
# (project name or dir_signal) before warning about other projects.
# Generic domain terms alone cause false positives — e.g. "odds" in
# courtside-ai should not trigger an mmalogic warning.
if current_project:
    signature_hits = {}
    for name in list(hit_projects.keys()):
        cfg = domains[name]
        sig_terms = [name] + cfg.get("dir_signals", [])
        sig_matches = [
            t for t in sig_terms
            if re.search(r"\b" + re.escape(t) + r"\b", prompt_lower)
        ]
        if sig_matches:
            signature_hits[name] = sig_matches
    if not signature_hits:
        sys.exit(0)
    hit_projects = signature_hits

# MISMATCH: prompt references project(s), but cwd is different
hit_list = ", ".join(
    f"{name} ({', '.join(terms[:3])})"
    for name, terms in hit_projects.items()
)
cwd_display = os.getcwd().replace(os.path.expanduser("~"), "~")
target = list(hit_projects.keys())[0]
target_path = domains[target]["canonical_path"]

warning = (
    f"PROJECT MISMATCH WARNING:\n"
    f"Prompt references: {hit_list}\n"
    f"Current directory: {cwd_display} "
    f"({'no project match' if not current_project else current_project})\n\n"
    f"Before executing, tell the user EXACTLY:\n"
    f"\"Your prompt mentions {target} domain terms, but I'm in "
    f"{cwd_display}. Work for {target} should run from "
    f"{target_path}. Want me to (a) switch repos, (b) you'll start a "
    f"new session there, or (c) proceed here anyway?\"\n\n"
    f"Do NOT run backtests, edit domain files, or deploy until user confirms."
)

output = {
    "hookSpecificOutput": {
        "hookEventName": "UserPromptSubmit",
        "additionalContext": warning
    }
}
print(json.dumps(output))
sys.exit(0)
