#!/usr/bin/env python3
"""
Claude Code Prompt Improver + Skill Router Hook
1. Matches prompts to SPECIFIC agent configurations (not just skill lists)
2. Tells Claude exactly which agent type to spawn and how to brief it
3. Evaluates vague prompts for clarity
"""
import json
import sys
import re

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError as e:
    print(f"Error: Invalid JSON input: {e}", file=sys.stderr)
    sys.exit(1)

prompt = input_data.get("prompt", "")
prompt_lower = prompt.lower().strip()

def output_json(text):
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": text
        }
    }
    print(json.dumps(output))

# === AGENT ROUTING ENGINE ===
# Instead of flat skill lists, route to SPECIFIC agent configurations
# Format: (pattern, priority, agent_instruction)
# Higher priority wins when multiple match

AGENT_ROUTES = [
    # --- AUDITS (most specific first) ---
    (r"audit.*front|front.*audit|ui.*audit|ux.*audit|design.*audit",
     100,
     "AGENT ROUTE: Frontend Audit\n"
     "1. Spawn a general-purpose agent briefed with: 'Read ALL component/page files. Check against frontend-design anti-slop rules, ui-ux-pro-max accessibility checklist, react-best-practices performance rules. Output ranked issue list (P0-P3) with file:line.'\n"
     "2. Follow frontend-design SKILL.md protocol for design quality assessment\n"
     "3. Run ui-ux-pro-max search scripts for specific recommendations\n"
     "4. After fixes: use webapp-testing Playwright to verify"),

    (r"audit.*back|back.*audit|api.*audit|security.*audit|server.*audit",
     100,
     "AGENT ROUTE: Backend Audit\n"
     "1. Invoke /audit skill via Skill tool (scans for secrets, code quality)\n"
     "2. Spawn a general-purpose agent briefed with: 'Read ALL API routes, middleware, auth, database files. Check for: unauthenticated routes, missing input validation, N+1 queries, hardcoded secrets, missing error handling, node:fs usage on serverless. Output ranked issue list (P0-P3) with file:line.'\n"
     "3. Follow senior-dev-mindset Backend checklist for completeness\n"
     "4. After fixes: use website-guardian verify protocol"),

    (r"full.*audit|site.*audit|audit.*site|audit.*app|audit.*website|comprehensive.*audit",
     110,
     "AGENT ROUTE: Full Site Audit — use /site-audit command\n"
     "Invoke the site-audit command via Skill tool, which runs 7 sequential phases with specialized agents."),

    # --- REDESIGN ---
    (r"redesign|rebuild|overhaul|full.*redesign|site.*redesign|makeover",
     110,
     "AGENT ROUTE: Full Redesign — use /site-redesign command\n"
     "Invoke the site-redesign command via Skill tool, which runs 9 sequential phases with specialized agents."),

    # --- FRONTEND WORK ---
    (r"build.*page|build.*component|create.*page|create.*component|new.*page|add.*page|landing.*page|dashboard",
     90,
     "AGENT ROUTE: Build Frontend Component/Page\n"
     "1. Read frontend-design SKILL.md — follow its design thinking protocol (Purpose → Tone → Constraints → Differentiation)\n"
     "2. Read ui-ux-pro-max SKILL.md — use search scripts for style/palette/font recommendations\n"
     "3. Read react-best-practices rules for performance patterns\n"
     "4. Follow senior-dev-mindset Frontend checklist (all states, responsive, accessible)\n"
     "5. After building: use webapp-testing to verify in browser"),

    (r"frontend|front.?end|component|ui\b|ux\b|interface|layout|styl|beautif|html|css|react|vue|svelte|next\.?js|tailwind",
     70,
     "AGENT ROUTE: Frontend Work\n"
     "Skills to USE (read their SKILL.md, follow protocols):\n"
     "- frontend-design: anti-slop design guidelines, bold aesthetic choices\n"
     "- ui-ux-pro-max: accessibility, search scripts for recommendations\n"
     "- react-best-practices: performance rules (read relevant rules/ files)\n"
     "- senior-dev-mindset: Frontend checklist (all states, responsive, accessible)"),

    # --- BACKEND WORK ---
    (r"backend|back.?end|api|endpoint|server|database|query|migration|graphql|rest|express|postgres|supabase|prisma",
     70,
     "AGENT ROUTE: Backend Work\n"
     "Skills to USE (read their SKILL.md, follow protocols):\n"
     "- senior-dev-mindset: Backend checklist (validation, auth, error codes, N+1)\n"
     "- For security concerns: invoke /audit via Skill tool\n"
     "- For architecture decisions: follow senior-dev-mindset Architecture section"),

    # --- DEBUGGING ---
    (r"\bfix\b|bug|broken|error|crash|failing|not.?working|broke|debug|regress",
     80,
     "AGENT ROUTE: Debugging\n"
     "1. Read pre-debug-check SKILL.md — check anti-patterns.md for prior occurrences FIRST\n"
     "2. Follow systematic-debugging SKILL.md protocol (hypothesis → test → fix)\n"
     "3. After fix: follow error-memory SKILL.md to log the bug permanently\n"
     "4. If website-related: follow website-guardian baseline → fix → verify protocol"),

    (r"site.*broke|page.*broke|display.*wrong|render.*wrong|chart.*broke|table.*broke",
     85,
     "AGENT ROUTE: Website Bug\n"
     "1. Follow website-guardian SKILL.md — snapshot baseline BEFORE any fix\n"
     "2. Read pre-debug-check — check recurring-bugs.md for this exact bug\n"
     "3. Follow systematic-debugging protocol\n"
     "4. Use webapp-testing Playwright to verify fix in browser\n"
     "5. Log via error-memory to anti-patterns.md\n"
     "6. If mmalogic/OctagonAI: also follow site-update-protocol checklist"),

    # --- WEBSITE UPDATES ---
    (r"update.*site|update.*website|deploy.*site|website|webapp|web.?app|mmalogic|octagonai",
     75,
     "AGENT ROUTE: Website Update\n"
     "1. Follow website-guardian SKILL.md — snapshot baseline BEFORE changes\n"
     "2. Follow site-update-protocol if UFC/mmalogic project\n"
     "3. After changes: verify ALL baseline items still work\n"
     "4. Use webapp-testing if available for automated checks"),

    # --- TESTING ---
    (r"test.*app|test.*site|playwright|e2e|end.?to.?end|smoke.?test",
     80,
     "AGENT ROUTE: Web App Testing\n"
     "1. Read webapp-testing SKILL.md — follow the decision tree\n"
     "2. Use scripts/with_server.py to manage server lifecycle\n"
     "3. Write Playwright scripts following the examples in webapp-testing/examples/"),

    # --- CODE REVIEW ---
    (r"review|code.?review|pr.?review|check.*code",
     75,
     "AGENT ROUTE: Code Review\n"
     "1. Read code-reviewer SKILL.md\n"
     "2. Spawn a general-purpose agent briefed with code-reviewer's checklist\n"
     "3. For giving feedback: use requesting-code-review protocol\n"
     "4. For receiving feedback: use receiving-code-review protocol"),

    # --- DEPLOYMENT ---
    (r"deploy|ship|release|go.?live|push.?to.?prod|cloudflare|wrangler",
     80,
     "AGENT ROUTE: Deployment\n"
     "1. Invoke /deploy via Skill tool\n"
     "2. Follow website-guardian post-deploy verification"),

    # --- PLANNING ---
    (r"\bplan\b|architect|break.*down|roadmap|requirements",
     60,
     "AGENT ROUTE: Planning\n"
     "1. Invoke brainstorming skill for exploration\n"
     "2. Use spec-interview for requirements gathering\n"
     "3. Use writing-plans for implementation plan"),

    # --- DESIGN ---
    (r"design.?system|design.?token|theme|color.?palette|typography",
     75,
     "AGENT ROUTE: Design System\n"
     "1. Run ui-design-system token generator: python scripts/design_token_generator.py\n"
     "2. Use ui-ux-pro-max search for palette/font recommendations\n"
     "3. Follow frontend-design aesthetic guidelines"),

    (r"poster|visual|art|canvas|infographic|banner",
     80,
     "AGENT ROUTE: Visual Design\n"
     "1. Read canvas-design SKILL.md — follow the design philosophy creation process\n"
     "2. Create philosophy first, then express visually"),

    # --- OTHER ---
    (r"backtest|model.?accuracy|prediction|coefficient|sweep|betting|odds",
     80, "AGENT ROUTE: Use /backtest command via Skill tool"),
    (r"\bcommit|git\b|branch|merge|push|pull.?request|\bpr\b",
     50, "AGENT ROUTE: Follow git-sorcery skill protocol"),
    (r"research|learn.?about|how.?does",
     50, "AGENT ROUTE: Use deep-research skill protocol"),
    (r"prompt|llm|ai.?product|agent|rag",
     60, "AGENT ROUTE: Read senior-prompt-engineer SKILL.md"),
    (r"create.*skill|new.*skill|eval.*skill",
     70, "AGENT ROUTE: Use skill-creator SKILL.md protocol"),
    (r"article|blog|write.*content|draft|newsletter",
     60, "AGENT ROUTE: Use content-research-writer skill"),
    (r"powerpoint|slides|deck|\.pptx", 80, "AGENT ROUTE: Use anthropic-skills:pptx"),
    (r"\.pdf|fill.*form|merge.*pdf", 80, "AGENT ROUTE: Use anthropic-skills:pdf"),
    (r"word.?doc|\.docx|memo|letter", 80, "AGENT ROUTE: Use anthropic-skills:docx"),
    (r"spreadsheet|\.xlsx|\.csv|excel", 80, "AGENT ROUTE: Use anthropic-skills:xlsx"),
]

def route_agent(text):
    """Find the best agent route for this prompt."""
    matches = []
    for pattern, priority, instruction in AGENT_ROUTES:
        if re.search(pattern, text, re.IGNORECASE):
            matches.append((priority, instruction))

    if not matches:
        return None

    # Return highest priority match(es)
    matches.sort(key=lambda x: x[0], reverse=True)
    top_priority = matches[0][0]

    # Include all matches within 10 points of top
    relevant = [inst for pri, inst in matches if pri >= top_priority - 10]
    return "\n\n".join(relevant)

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
    output_json(f"{prompt}\n\nIMPORTANT: If you cannot determine what to continue, or if context feels limited, run /compact first to free space, then resume.")
    sys.exit(0)

# === AGENT ROUTING (runs on ALL non-trivial prompts) ===

word_count = len(prompt.split())
agent_route = route_agent(prompt_lower)

route_directive = ""
if agent_route:
    route_directive = (
        f"\n\n{agent_route}\n\n"
        f"ENFORCEMENT: You must follow the agent route above. Do NOT substitute a generic Explore agent "
        f"when the route specifies a skill-briefed general-purpose agent. Do NOT 'apply principles mentally' — "
        f"read the SKILL.md files referenced above and follow their step-by-step protocols. "
        f"If a route says 'invoke via Skill tool,' use the Skill tool. "
        f"If a route says 'spawn agent briefed with,' spawn an Agent with the skill's content in its prompt."
    )

# === FAST-PATH ===

if word_count <= 3 and not agent_route:
    output_json(prompt)
    sys.exit(0)

if word_count <= 3 and agent_route:
    output_json(prompt + route_directive)
    sys.exit(0)

clear_signals = [
    "fix ", "add ", "update ", "change ", "remove ", "delete ", "create ",
    "implement ", "refactor ", "move ", "rename ", "install ", "deploy ",
    "run ", "test ", "build ", "push ", "commit ", "merge ",
    "show me", "read ", "open ", "check ", "look at", "what is",
    "how do", "why does", "can you", "please ",
]
if any(prompt_lower.startswith(signal) for signal in clear_signals):
    output_json(prompt + route_directive)
    sys.exit(0)

if word_count >= 20:
    output_json(prompt + route_directive)
    sys.exit(0)

# === EVALUATION for ambiguous prompts ===

escaped_prompt = prompt.replace("\\", "\\\\").replace('"', '\\"')

wrapped_prompt = f"""PROMPT EVALUATION

Original user request: "{escaped_prompt}"

EVALUATE: Is this prompt clear enough to execute, or does it need enrichment?

PROCEED IMMEDIATELY if:
- Detailed/specific OR you have sufficient context OR can infer intent

ONLY USE SKILL if genuinely vague (e.g., "fix the bug" with no context):
- If vague:
  1. First, preface with brief note: "Hey! The Prompt Improver Hook flagged your prompt as a bit vague because [specific reason]."
  2. Then use the prompt-improver skill to research and generate clarifying questions

If clear, proceed with the original request. If vague, invoke the skill."""

output_json(wrapped_prompt + route_directive)
sys.exit(0)
