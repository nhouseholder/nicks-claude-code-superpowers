#!/usr/bin/env python3
"""
Claude Code Prompt Improver Hook
Evaluates prompts for clarity and invokes the prompt-improver skill for vague cases.
Only fires on genuinely vague prompts — short/clear prompts pass through untouched.
"""
import json
import sys

# Load input from stdin
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

prompt = input_data.get("prompt", "")

def output_json(text):
    """Output text in UserPromptSubmit JSON format"""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": text
        }
    }
    print(json.dumps(output))

# === BYPASS CONDITIONS ===

# 1. Explicit bypass with * prefix
if prompt.startswith("*"):
    clean_prompt = prompt[1:].strip()
    output_json(clean_prompt)
    sys.exit(0)

# 2. Slash commands
if prompt.startswith("/"):
    output_json(prompt)
    sys.exit(0)

# 3. Memorize feature (# prefix)
if prompt.startswith("#"):
    output_json(prompt)
    sys.exit(0)

# === FAST-PATH: Skip evaluation for clearly actionable prompts ===

# Short prompts (under 5 words) that are single-letter or quick answers → pass through
word_count = len(prompt.split())
if word_count <= 3:
    # Very short prompts are usually answers to questions, confirmations, or clear directives
    output_json(prompt)
    sys.exit(0)

# Prompts with specific technical signals are almost always clear enough
clear_signals = [
    "fix ", "add ", "update ", "change ", "remove ", "delete ", "create ",
    "implement ", "refactor ", "move ", "rename ", "install ", "deploy ",
    "run ", "test ", "build ", "push ", "commit ", "merge ",
    "show me", "read ", "open ", "check ", "look at", "what is",
    "how do", "why does", "can you", "please ",
]
prompt_lower = prompt.lower().strip()
if any(prompt_lower.startswith(signal) for signal in clear_signals):
    output_json(prompt)
    sys.exit(0)

# Prompts over 20 words are usually detailed enough
if word_count >= 20:
    output_json(prompt)
    sys.exit(0)

# === EVALUATION: Only reaches here for mid-length, ambiguous prompts ===

# Show visual confirmation only when actually evaluating
print("✓ Prompt Improver evaluating", file=sys.stderr)

# Escape quotes in prompt for safe embedding
escaped_prompt = prompt.replace("\\", "\\\\").replace('"', '\\"')

wrapped_prompt = f"""PROMPT EVALUATION

Original user request: "{escaped_prompt}"

EVALUATE: Is this prompt clear enough to execute, or does it need enrichment?

PROCEED IMMEDIATELY if:
- Detailed/specific OR you have sufficient context OR can infer intent

ONLY USE SKILL if genuinely vague (e.g., "fix the bug" with no context):
- If vague:
  1. First, preface with brief note: "Hey! The Prompt Improver Hook flagged your prompt as a bit vague because [specific reason: ambiguous scope/missing context/unclear target/etc]."
  2. Then use the prompt-improver skill to research and generate clarifying questions
- The skill will guide you through research, question generation, and execution
- Trust user intent by default. Check conversation history before using the skill.

If clear, proceed with the original request. If vague, invoke the skill."""

output_json(wrapped_prompt)
sys.exit(0)
