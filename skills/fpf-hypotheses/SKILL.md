---
name: fpf-hypotheses
description: Execute complete FPF cycle from hypothesis generation to decision
argument-hint: "[problem-statement]"
allowed-tools: Task, Read, Write, Bash, AskUserQuestion
weight: light
---

# Propose Hypotheses Workflow

Execute the First Principles Framework (FPF) cycle: Context → Hypotheses → User Input → Verify Logic → Validate Evidence → Audit Trust → Decision → Present.

Problem Statement: `$ARGUMENTS`

---

## Parallel Evaluation Template (used in Steps 5-7)

For each hypothesis file in `[source_dir]`, launch a parallel fpf-agent (sonnet[1m]):
- Read the hypothesis from `[source_dir]/<hypothesis-id>.md`
- Evaluate against `[criteria]`
- Rate on 0-1 scale; pass if score >= `[threshold]`
- `[action]`: move passing files to `[dest_dir]`, failing to `.fpf/knowledge/invalid/`, appending evaluation notes
- Wait for all agents, confirm files moved correctly

| Step | Source | Dest | Threshold | Criteria | Action |
|------|--------|------|-----------|----------|--------|
| 5 | L0 | L1 | 0.6 | Internal contradictions, logical fallacies, unsupported leaps, circular arguments, missing causal links | Move + add verification notes |
| 6 | L1 | L2 | 0.5 | Empirical/theoretical support, evidence quality, counter-examples, evidence strength | Move + add validation notes |
| 7 | L2 | — | — | Source reliability, confirmation/survivorship bias, anchoring, epistemic humility → compute R_eff | Write audit to `.fpf/evidence/audit-{id}-{date}.md`, reply with R_eff + weakest link |

---

## Steps

### Step 1: Initialize (Main Agent + FPF Agent)

1. Create directory scaffold:
   ```bash
   mkdir -p .fpf/{evidence,decisions,sessions,knowledge/{L0,L1,L2,invalid}}
   touch .fpf/{evidence,decisions,sessions,knowledge/{L0,L1,L2,invalid}}/.gitkeep
   ```
2. Launch fpf-agent (sonnet[1m]): Analyze problem statement, identify domain/constraints/stakeholders/success criteria/assumptions. Write context summary to `.fpf/context.md`.

### Step 2: Generate Hypotheses (FPF Agent)

Launch fpf-agent (sonnet[1m]): Generate 3-5 competing hypotheses. Each gets:
- Unique ID (H1, H2...), title, kind, scope
- Core claim, reasoning, key assumptions, testable predictions

Write each as separate file to `.fpf/knowledge/L0/`. Reply with summary table (ID | Title | Kind | Scope).

### Step 3: Present Summary (Main Agent)

Read all L0 files, present summary table, ask user: "Would you like to add any hypotheses of your own?"

### Step 4: Add User Hypothesis (Conditional Loop)

If user says yes: launch fpf-agent (sonnet[1m]) to format user's hypothesis into standard template with ID/kind/scope/assumptions/predictions. Write to `.fpf/knowledge/L0/`. Loop back to Step 3. Exit when user declines.

### Step 5: Verify Logic

Apply **Parallel Evaluation Template** with Step 5 parameters.

### Step 6: Validate Evidence

Apply **Parallel Evaluation Template** with Step 6 parameters.

### Step 7: Audit Trust

Apply **Parallel Evaluation Template** with Step 7 parameters.

### Step 8: Make Decision (FPF Agent)

Launch fpf-agent (sonnet[1m]): Create Design Rationale Record (DRR) comparing all L2 hypotheses on R_eff, evidence strength, risk, feasibility, and constraint alignment. Select best hypothesis, justify decision, document why alternatives were rejected.

Inputs: `.fpf/knowledge/L2/`, `.fpf/evidence/`
Write DRR to `.fpf/decisions/`. Reply with comparison table (Hypothesis | R_eff | Weakest Link | Status) + recommended decision + rationale.

### Step 9: Present Final (Main Agent)

1. Read DRR from `.fpf/decisions/`, present results
2. Suggest next steps: implement selected hypothesis, `/fpf:status`, `/fpf:actualize`
3. Ask user if they agree; if not, relaunch Step 8 with user's modifications
