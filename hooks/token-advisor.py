#!/usr/bin/env python3
"""
Token Advisor Hook — Recommends model tier and effort level based on task complexity.

Fires on UserPromptSubmit. Classifies the incoming prompt into complexity tiers
and adds a brief recommendation for model/effort optimization.

Exit code 0 always. Lightweight — no file I/O, no network, pure string analysis.
"""
import json
import re
import sys

try:
    input_data = json.load(sys.stdin)
except (json.JSONDecodeError, Exception):
    sys.exit(0)

prompt = input_data.get("prompt", "").strip()
prompt_lower = prompt.lower()

# Skip empty, very short, or slash-command prompts
if not prompt or len(prompt) < 5 or prompt.startswith("/"):
    sys.exit(0)

# Skip if user is already giving model/effort instructions
if any(kw in prompt_lower for kw in ["switch to", "/model", "/fast", "use sonnet", "use opus", "use haiku"]):
    sys.exit(0)


# === CLASSIFICATION SIGNALS ===

# TRIVIAL signals — mechanical, zero-thought tasks
trivial_patterns = [
    r"^(rename|fix typo|format|add comment|remove comment|delete line)",
    r"^what (does|is) ",
    r"^(show|list|print|display|read|cat|check) ",
    r"^(yes|no|ok|sure|go|do it|proceed|continue|looks good|lgtm|perfect)",
    r"^run ",
]

# SIMPLE signals — single-scope, clear intent
simple_patterns = [
    r"(add|create|write) (a |the )?(field|prop|column|variable|constant|import|export)",
    r"(change|update|set|modify) .{0,30} (to|from|=)",
    r"(move|copy) .{0,30} (to|into|from)",
    r"fix (the |this |that )?(bug|error|issue|typo|warning)",
    r"(install|uninstall|upgrade|add) .{0,20}(package|dependency|dep|lib)",
]

# COMPLEX signals — multi-scope, requires reasoning
complex_patterns = [
    r"(architect|design|plan|brainstorm|think about|evaluate|compare)",
    r"(refactor|restructure|reorganize|migrate|rewrite)",
    r"(debug|investigate|figure out|diagnose|why (is|does|isn't|doesn't))",
    r"(build|implement|create) .{0,30}(system|feature|module|service|api|pipeline)",
    r"(security|auth|permission|credential|encrypt|token)",
    r"(deploy|production|staging|release|rollback)",
    r"(database|schema|migration|data model)",
    r"multi.?(file|step|page|component|service)",
    r"(performance|optimize|speed|latency|memory)",
]

# CRITICAL signals — high-stakes, irreversible
critical_patterns = [
    r"(data migration|schema change|drop table|delete (all|every))",
    r"(production|live site|customer.facing)",
    r"(security (fix|patch|vuln|audit))",
    r"(rollback|disaster|recovery|restore)",
    r"ULTRATHINK",
]

# Plan-execute signals — user has or wants a plan
plan_signals = [
    r"(execute|follow|implement) .{0,20}(plan|steps|spec|roadmap)",
    r"(step \d|task \d|phase \d)",
    r"from (the |my )?(plan|spec|roadmap)",
]


def classify(text):
    """Classify prompt complexity. Returns (tier, confidence)."""
    text_lower = text.lower()
    words = text_lower.split()
    word_count = len(words)

    # Very short prompts are usually trivial
    if word_count <= 5:
        for pat in trivial_patterns:
            if re.search(pat, text_lower):
                return "TRIVIAL", 0.9
        return "TRIVIAL", 0.6

    # Check critical first (highest priority)
    for pat in critical_patterns:
        if re.search(pat, text_lower):
            return "CRITICAL", 0.8

    # Check complex
    complex_hits = sum(1 for pat in complex_patterns if re.search(pat, text_lower))
    if complex_hits >= 2:
        return "COMPLEX", 0.8
    if complex_hits == 1:
        # Long prompts with complex signal = likely complex
        if word_count > 30:
            return "COMPLEX", 0.7
        return "MODERATE", 0.7

    # Check if executing a plan (simple execution)
    for pat in plan_signals:
        if re.search(pat, text_lower):
            return "SIMPLE", 0.8

    # Check simple
    for pat in simple_patterns:
        if re.search(pat, text_lower):
            return "SIMPLE", 0.8

    # Check trivial
    for pat in trivial_patterns:
        if re.search(pat, text_lower):
            return "TRIVIAL", 0.8

    # Default: moderate for medium prompts, simple for short
    if word_count > 20:
        return "MODERATE", 0.5
    return "SIMPLE", 0.5


# === CLASSIFY AND RECOMMEND ===

tier, confidence = classify(prompt)

# Only recommend if confident enough
if confidence < 0.6:
    sys.exit(0)

# Build recommendation
recommendations = {
    "TRIVIAL": {
        "model": "Sonnet or /fast",
        "msg": "Quick task — Sonnet or /fast would save tokens here.",
    },
    "SIMPLE": {
        "model": "Sonnet",
        "msg": "Straightforward task — Sonnet handles this well.",
    },
    "MODERATE": {
        "model": "Opus (current)",
        "msg": None,  # No recommendation needed — Opus is correct
    },
    "COMPLEX": {
        "model": "Opus",
        "msg": "Complex task — consider writing a detailed plan first, then switching to Sonnet to execute.",
    },
    "CRITICAL": {
        "model": "Opus + max effort",
        "msg": "High-stakes task — use Plan Mode to think through this carefully before executing.",
    },
}

rec = recommendations.get(tier, {})
msg = rec.get("msg")

# Don't output anything for MODERATE (Opus is already correct)
if not msg:
    sys.exit(0)

# Only suggest downgrade (Sonnet/fast) — never suggest upgrade
# The hook should help save tokens, not add friction
if tier in ("COMPLEX", "CRITICAL"):
    # For complex/critical, suggest plan-then-execute workflow
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": f"TOKEN ADVISOR [{tier}]: {msg}"
        }
    }
else:
    # For trivial/simple, suggest model switch
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": f"TOKEN ADVISOR [{tier}]: {msg}"
        }
    }

print(json.dumps(output))
