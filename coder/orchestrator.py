#!/usr/bin/env python3
"""
Coder Orchestrator — Thin autonomous loop runner for Claude Code.

This is NOT a replacement for Claude Code skills — it's the outer loop
that skills can't provide (they run inside Claude, this runs around it).

What it does:
1. Takes your high-level goal
2. Calls claude -p to plan (Claude's own skills handle model routing, planning logic)
3. Executes each step via claude -p sessions (skills inside handle the intelligence)
4. Tracks progress, cost, and time
5. Retries failed steps with session continuation
6. Continues until done or all retries exhausted

What it delegates to existing skills (NOT reimplemented here):
- Model routing → model-router skill (always-on inside Claude)
- Planning logic → writing-plans skill
- Retry strategy → never-give-up skill (with model escalation)
- Debug approach → pre-debug-check, systematic-debugging skills
- Code quality → proactive-qa, zero-iteration skills

Usage:
    python orchestrator.py "Build a login page with OAuth"
    python orchestrator.py --goal-file goals.txt
    python orchestrator.py "Fix the dashboard bug" --project-dir /path/to/project
    python orchestrator.py --dry-run "Add auth" --project-dir ~/app
"""

import subprocess
import json
import sys
import os
import time
import argparse
import re
from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class Task:
    description: str
    status: TaskStatus = TaskStatus.PENDING
    attempts: int = 0
    max_attempts: int = 3
    result: Optional[str] = None
    error: Optional[str] = None
    session_id: Optional[str] = None
    cost_usd: float = 0.0
    duration_ms: int = 0


@dataclass
class OrchestratorState:
    goal: str
    project_dir: str
    tasks: list = field(default_factory=list)
    total_cost: float = 0.0
    start_time: float = field(default_factory=time.time)
    log_file: Optional[str] = None


# ─── Claude Code Interface ───────────────────────────────────────────────────

def call_claude(
    prompt: str,
    project_dir: str = ".",
    session_id: Optional[str] = None,
    max_turns: int = 50,
    permission_mode: str = "acceptEdits",
    timeout_sec: int = 600,
) -> dict:
    """Call Claude Code in headless mode. Model routing handled by skills inside Claude."""

    cmd = ["claude", "-p", prompt]
    cmd += ["--output-format", "json"]
    cmd += ["--max-turns", str(max_turns)]

    if permission_mode:
        cmd += ["--permission-mode", permission_mode]

    if session_id:
        cmd += ["--resume", session_id]

    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        cwd=project_dir,
        timeout=timeout_sec,
    )

    try:
        parsed = json.loads(result.stdout)
        return parsed
    except json.JSONDecodeError:
        return {
            "result": result.stdout,
            "is_error": result.returncode != 0,
            "total_cost_usd": 0,
            "duration_ms": 0,
        }


# ─── Planning ────────────────────────────────────────────────────────────────

def create_plan(goal: str, project_dir: str) -> list[Task]:
    """Ask Claude to break the goal into tasks. Claude's own skills handle the intelligence."""
    log(f"Planning: {goal}")

    planning_prompt = f"""Break this goal into concrete, sequential tasks for autonomous execution.

GOAL: {goal}

Return ONLY a JSON array, no markdown fences, no explanation. Each item has "description" (string).
Example: [{{"description": "Read the auth module and understand current flow"}}, {{"description": "Add OAuth config"}}]

Rules:
- Start with reading/understanding steps
- Maximum 10 tasks
- Each task completable in one session
- Include a verification step at the end"""

    result = call_claude(
        prompt=planning_prompt,
        project_dir=project_dir,
        max_turns=5,
    )

    response_text = result.get("result", "")
    tasks = parse_task_list(response_text)

    if not tasks:
        log("Could not parse plan, treating as single task")
        return [Task(description=goal)]

    return tasks


def parse_task_list(text: str) -> list[Task]:
    """Parse a JSON task list from Claude's response."""
    # Strip emoji prefixes and markdown fencing
    cleaned = re.sub(r'```json\s*', '', text)
    cleaned = re.sub(r'```\s*$', '', cleaned)

    json_match = re.search(r'\[.*\]', cleaned, re.DOTALL)
    if not json_match:
        return []

    try:
        items = json.loads(json_match.group())
        return [Task(description=item["description"]) for item in items]
    except (json.JSONDecodeError, KeyError, ValueError):
        return []


# ─── Execution ───────────────────────────────────────────────────────────────

def execute_task(task: Task, state: OrchestratorState) -> bool:
    """Execute a single task via claude -p. Returns True if successful."""
    task.status = TaskStatus.IN_PROGRESS
    task.attempts += 1

    # Build context
    completed = [t for t in state.tasks if t.status == TaskStatus.COMPLETED]
    context = ""
    if completed:
        context = "\n\nAlready completed:\n" + "\n".join(
            f"- {t.description}" for t in completed
        )

    # If retrying, include error context
    error_context = ""
    if task.attempts > 1 and task.error:
        error_context = f"""

PREVIOUS ATTEMPT FAILED (attempt {task.attempts - 1}):
Error: {task.error}
Previous output (last 500 chars): {(task.result or '')[-500:]}

Try a DIFFERENT approach. The previous approach did not work."""

    exec_prompt = f"""Execute this task autonomously. Do not ask questions — make reasonable decisions.

TASK: {task.description}

OVERALL GOAL: {state.goal}
{context}{error_context}

Rules:
- Complete the task fully, don't leave TODOs
- If you encounter an error, try to fix it
- Commit working code with descriptive messages
- If genuinely impossible, explain why clearly"""

    attempt_label = f"[{task.attempts}/{task.max_attempts}]"
    log(f"{attempt_label} {task.description[:70]}")

    try:
        result = call_claude(
            prompt=exec_prompt,
            project_dir=state.project_dir,
            session_id=task.session_id,
            max_turns=50,
            permission_mode="acceptEdits",
        )

        task.result = result.get("result", "")
        task.session_id = result.get("session_id")

        # Track cost
        cost = result.get("total_cost_usd", 0)
        if cost:
            task.cost_usd += cost
            state.total_cost += cost

        task.duration_ms += result.get("duration_ms", 0)

        # Check success via the structured output
        is_error = result.get("is_error", False)
        if is_error:
            task.error = task.result[:200] if task.result else "Unknown error"
            log(f"  FAILED: {task.error[:80]}")
            return False

        # Heuristic: check for clear failure language
        text_lower = task.result.lower() if task.result else ""
        failure_signals = ["i cannot", "i'm unable", "failed to", "traceback", "build failed"]
        success_signals = ["completed", "done", "successfully", "implemented", "created", "updated", "fixed", "committed"]

        failures = sum(1 for s in failure_signals if s in text_lower)
        successes = sum(1 for s in success_signals if s in text_lower)

        if successes >= failures:
            task.status = TaskStatus.COMPLETED
            log(f"  Done (${cost:.3f})")
            return True
        else:
            task.error = "Output suggests task did not complete successfully"
            log(f"  Likely failed — retrying...")
            return False

    except subprocess.TimeoutExpired:
        task.error = "Timed out after 10 minutes"
        log(f"  Timeout")
        return False
    except Exception as e:
        task.error = str(e)
        log(f"  Error: {e}")
        return False


# ─── Progress Tracking ───────────────────────────────────────────────────────

def print_progress(state: OrchestratorState):
    """Print progress bar with cost and time."""
    total = len(state.tasks)
    completed = sum(1 for t in state.tasks if t.status == TaskStatus.COMPLETED)
    failed = sum(1 for t in state.tasks if t.status == TaskStatus.FAILED)
    elapsed = time.time() - state.start_time

    bar_width = 30
    filled = int(bar_width * completed / max(total, 1))
    bar = "█" * filled + "░" * (bar_width - filled)

    pct = round(completed / total * 100) if total > 0 else 0
    cost = round(state.total_cost, 3)
    mins = round(elapsed / 60, 1)

    print(f"\n  [{bar}] {pct}% ({completed}/{total}) | {mins}min | ${cost}")
    if failed > 0:
        print(f"  Failed: {failed} tasks")
    print()


# ─── Logging ─────────────────────────────────────────────────────────────────

LOG_FILE = None

def log(msg: str):
    timestamp = datetime.now().strftime("%H:%M:%S")
    line = f"[{timestamp}] {msg}"
    print(line)
    if LOG_FILE:
        with open(LOG_FILE, "a") as f:
            f.write(line + "\n")


# ─── Main Loop ───────────────────────────────────────────────────────────────

def orchestrate(goal: str, project_dir: str = ".", log_path: Optional[str] = None):
    """Main loop — plan, execute each step, retry failures, track progress."""
    global LOG_FILE
    LOG_FILE = log_path or f"orchestrator_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  CODER ORCHESTRATOR                                         ║
║  Goal: {goal[:53].ljust(53)}║
║  Dir:  {project_dir[:53].ljust(53)}║
╚══════════════════════════════════════════════════════════════╝
""")

    state = OrchestratorState(goal=goal, project_dir=project_dir, log_file=LOG_FILE)

    # Phase 1: Plan
    log("Phase 1: Planning...")
    state.tasks = create_plan(goal, project_dir)
    log(f"Plan: {len(state.tasks)} tasks")
    for i, task in enumerate(state.tasks, 1):
        log(f"  {i}. {task.description}")

    # Phase 2: Execute with retry
    log("\nPhase 2: Executing...")
    for task in state.tasks:
        success = execute_task(task, state)

        # Retry loop
        while not success and task.attempts < task.max_attempts:
            success = execute_task(task, state)

        if not success:
            task.status = TaskStatus.FAILED
            log(f"  GAVE UP after {task.attempts} attempts")

        print_progress(state)

    # Phase 3: Summary
    completed = sum(1 for t in state.tasks if t.status == TaskStatus.COMPLETED)
    failed = sum(1 for t in state.tasks if t.status == TaskStatus.FAILED)
    elapsed = round((time.time() - state.start_time) / 60, 1)

    # If anything failed, ask Claude for a status report
    if failed > 0:
        log("Phase 3: Checking final state...")
        failed_tasks = [t for t in state.tasks if t.status == TaskStatus.FAILED]
        completed_tasks = [t for t in state.tasks if t.status == TaskStatus.COMPLETED]

        verify_result = call_claude(
            prompt=f"""Goal: {goal}
Completed: {[t.description for t in completed_tasks]}
Failed: {[f"{t.description} ({t.error})" for t in failed_tasks]}
Check the project state. What's done, what's left?""",
            project_dir=project_dir,
            max_turns=10,
        )
        log(f"Status: {verify_result.get('result', 'No response')[:300]}")

    print(f"""
╔══════════════════════════════════════════════════════════════╗
║  DONE                                                       ║
║  {str(completed).rjust(2)}/{str(len(state.tasks)).ljust(2)} completed | {str(failed).rjust(2)} failed | {str(elapsed).ljust(5)}min | ${str(round(state.total_cost, 3)).ljust(7)}   ║
║  Log: {LOG_FILE[:54].ljust(54)}║
╚══════════════════════════════════════════════════════════════╝
""")

    return state


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="Coder Orchestrator — autonomous loop runner for Claude Code",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python orchestrator.py "Fix the login page bug"
  python orchestrator.py "Add dark mode" --project-dir ~/myapp
  python orchestrator.py --goal-file goals.txt
  python orchestrator.py --dry-run "Add auth"
        """,
    )
    parser.add_argument("goal", nargs="?", help="High-level goal")
    parser.add_argument("--goal-file", help="Read goal from file")
    parser.add_argument("--project-dir", default=".", help="Project directory")
    parser.add_argument("--log", help="Log file path")
    parser.add_argument("--dry-run", action="store_true", help="Plan only")
    parser.add_argument("--max-retries", type=int, default=3, help="Max retries per task")
    parser.add_argument("--timeout", type=int, default=600, help="Timeout per task (seconds)")

    args = parser.parse_args()

    goal = args.goal
    if args.goal_file:
        goal = Path(args.goal_file).read_text().strip()

    if not goal:
        parser.print_help()
        sys.exit(1)

    project_dir = os.path.abspath(args.project_dir)
    if not os.path.isdir(project_dir):
        print(f"Error: {project_dir} is not a directory")
        sys.exit(1)

    if args.dry_run:
        print("DRY RUN — Planning only\n")
        tasks = create_plan(goal, project_dir)
        for i, task in enumerate(tasks, 1):
            print(f"  {i}. {task.description}")
        return

    state = orchestrate(goal, project_dir, args.log)
    failed = sum(1 for t in state.tasks if t.status == TaskStatus.FAILED)
    sys.exit(1 if failed > 0 else 0)


if __name__ == "__main__":
    main()
