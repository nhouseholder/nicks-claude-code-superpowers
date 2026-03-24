#!/usr/bin/env python3
"""
Claude Code Prompt Improver + Skill Matcher Hook
1. Matches prompts against installed skills and tells Claude to USE them
2. Evaluates prompts for clarity (invokes prompt-improver skill for vague cases)
"""
import json
import sys
import re

# Load input from stdin
try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

prompt = input_data.get("prompt", "")
prompt_lower = prompt.lower().strip()

def output_json(text):
    """Output text in UserPromptSubmit JSON format"""
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": text
        }
    }
    print(json.dumps(output))

# === SKILL MATCHING ENGINE ===
# Keywords → skills that MUST be used (not optional, not "consider")

SKILL_TRIGGERS = {
    # Web design & frontend (HIGH PRIORITY — user's pain point)
    r"frontend|front.?end|component|landing.?page|dashboard|ui\b|ux\b|interface|layout|styl|beautif|redesign|web.?design|web.?app|html|css|react|vue|svelte|next\.?js|tailwind":
        "frontend-design, ui-ux-pro-max, senior-dev-mindset",
    # Website updates & maintenance
    r"website|webapp|site.?update|deploy.*site|update.*site|the site|mmalogic|octagonai|page.?broke":
        "website-guardian, site-update-protocol",
    # Debugging & fixing
    r"\bfix\b|bug|broken|error|crash|failing|not.?working|broke|debug|issue|regress":
        "systematic-debugging, pre-debug-check, error-memory",
    # Website bugs specifically
    r"site.*broke|page.*broke|display.*wrong|render.*wrong|chart.*broke|table.*broke":
        "website-guardian, site-update-protocol, error-memory, screenshot-dissector",
    # Deployment
    r"deploy|ship it|release|go.?live|push.?to.?prod|cloudflare|wrangler":
        "deploy, website-guardian",
    # Planning
    r"\bplan\b|architect|break.*down|design.*system|how.?should|roadmap":
        "writing-plans, brainstorming, spec-interview",
    # Testing
    r"\btest|tdd|coverage|spec|unit.?test|integration.?test":
        "test-driven-development, qa-gate",
    # Git
    r"\bcommit|git\b|branch|merge|push|pull.?request|\bpr\b":
        "git-sorcery, version-bump",
    # Research
    r"research|learn.?about|understand|how.?does|explain.?how":
        "deep-research, know-what-you-dont-know",
    # Sports/betting
    r"backtest|model.?accuracy|prediction|coefficient|sweep|betting|odds":
        "backtest, profit-driven-development, backtestor-quality-control",
    # Code review
    r"review|audit|check.*code|scan|security|vulnerab":
        "audit, reflexion, requesting-code-review",
    # Content writing
    r"article|blog|write.*content|draft|newsletter|case.?study":
        "content-research-writer",
    # File formats
    r"powerpoint|slides|deck|presentation|\.pptx": "anthropic-skills:pptx",
    r"\.pdf|fill.*form|merge.*pdf|pdf": "anthropic-skills:pdf",
    r"word.?doc|\.docx|document|memo|letter": "anthropic-skills:docx",
    r"spreadsheet|\.xlsx|\.csv|excel|tabular": "anthropic-skills:xlsx",
}

def match_skills(text):
    """Find all skills that match the prompt."""
    matched = set()
    for pattern, skills in SKILL_TRIGGERS.items():
        if re.search(pattern, text, re.IGNORECASE):
            for s in skills.split(", "):
                matched.add(s.strip())
    return sorted(matched)

# === BYPASS CONDITIONS ===

if prompt.startswith("*"):
    output_json(prompt[1:].strip())
    sys.exit(0)

if prompt.startswith("/"):
    output_json(prompt)
    sys.exit(0)

if prompt.startswith("#"):
    output_json(prompt)
    sys.exit(0)

# === CONTINUE HANDLING ===

continue_signals = ["continue", "go", "keep going", "go on", "proceed", "carry on", "next"]
if prompt_lower in continue_signals:
    output_json(f"{prompt}\n\nIMPORTANT: If you cannot determine what to continue, or if context feels limited, run /compact first to free space, then resume. Never generate an empty response — always either continue the task, compact, or tell the user what happened.")
    sys.exit(0)

# === SKILL MATCHING (runs on ALL non-trivial prompts) ===

word_count = len(prompt.split())
matched_skills = match_skills(prompt_lower)

skill_reminder = ""
if matched_skills:
    skills_list = ", ".join(matched_skills)
    skill_reminder = (
        f"\n\nSKILL MATCH: These installed skills apply to this task: [{skills_list}]. "
        f"You MUST actively use these skills — read their SKILL.md protocols, follow their checklists, "
        f"invoke them via the Skill tool if they're slash commands, or spawn agents briefed with their instructions. "
        f"Do NOT ignore these and do the task manually. The user installed these skills specifically for tasks like this."
    )

# === FAST-PATH for short/clear prompts ===

if word_count <= 3 and not matched_skills:
    output_json(prompt)
    sys.exit(0)

if word_count <= 3 and matched_skills:
    output_json(prompt + skill_reminder)
    sys.exit(0)

clear_signals = [
    "fix ", "add ", "update ", "change ", "remove ", "delete ", "create ",
    "implement ", "refactor ", "move ", "rename ", "install ", "deploy ",
    "run ", "test ", "build ", "push ", "commit ", "merge ",
    "show me", "read ", "open ", "check ", "look at", "what is",
    "how do", "why does", "can you", "please ",
]
if any(prompt_lower.startswith(signal) for signal in clear_signals):
    output_json(prompt + skill_reminder)
    sys.exit(0)

if word_count >= 20:
    output_json(prompt + skill_reminder)
    sys.exit(0)

# === EVALUATION: Mid-length, potentially ambiguous prompts ===

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

output_json(wrapped_prompt + skill_reminder)
sys.exit(0)
