---
name: fpf-hypotheses
description: Execute complete FPF cycle from hypothesis generation to decision
argument-hint: "[problem-statement]"
allowed-tools: Task, Read, Write, Bash, AskUserQuestion
---

# Propose Hypotheses Workflow

Execute the First Principles Framework (FPF) cycle: generate competing hypotheses, verify logic, validate evidence, audit trust, and produce a decision.

Note: This skill operates inline — no external task files required.

## User Input

```text
Problem Statement: $ARGUMENTS
```

## Workflow Execution

### Step 1a: Create Directory Structure (Main Agent)

Create `.fpf/` directory structure if it does not exist:

```bash
mkdir -p .fpf/{evidence,decisions,sessions,knowledge/{L0,L1,L2,invalid}}
touch .fpf/{evidence,decisions,sessions,knowledge/{L0,L1,L2,invalid}}/.gitkeep
```

**Postcondition**: `.fpf/` directory scaffold exists.

---

### Step 1b: Initialize Context (FPF Agent)

Launch fpf-agent with sonnet[1m] model:
- **Description**: "Initialize FPF context"
- **Prompt**:
  ```
  Analyze the problem statement and establish the FPF context. Identify the domain, key constraints, stakeholders, success criteria, and any assumptions. Summarize the problem space and what a good solution looks like.

  Problem Statement: $ARGUMENTS

  **Write**: Context summary to `.fpf/context.md`
  ```

---

### Step 2: Generate Hypotheses (FPF Agent)

Launch fpf-agent with sonnet[1m] model:
- **Description**: "Generate L0 hypotheses"
- **Prompt**:
  ```
  Generate 3-5 competing hypotheses for the problem. Each hypothesis should be a distinct approach or solution with a clear rationale. For each hypothesis, specify:
  - A unique ID (H1, H2, etc.)
  - A descriptive title
  - Kind (e.g., architectural, algorithmic, process, design)
  - Scope (narrow, medium, broad)
  - Core claim and reasoning
  - Key assumptions
  - Testable predictions

  Problem Statement: $ARGUMENTS
  Context: <summary from Step 1b>

  **Write**: Each hypothesis as a separate file to `.fpf/knowledge/L0/`

  Reply with summary table in markdown format:

    | ID | Title | Kind | Scope |
    |----|-------|------|-------|
    | ... | ... | ... | ... |
  ```

---

### Step 3: Present Summary (Main Agent)

1. Read all L0 hypothesis files from `.fpf/knowledge/L0/`
2. Present summary table from agent response.
3. Ask user: "Would you like to add any hypotheses of your own? (yes/no)"

---

### Step 4: Add User Hypothesis (FPF Agent, Conditional Loop)

**Condition**: User says yes to adding hypotheses.

Launch fpf-agent with sonnet[1m] model:
- **Description**: "Add user hypothesis"
- **Prompt**:
  ```
  Format the user's hypothesis into the standard FPF hypothesis template. Assign a unique ID, identify the kind and scope, extract key assumptions, and define testable predictions.

  User Hypothesis Description: <get from user>

  **Write**: User hypothesis to `.fpf/knowledge/L0/`
  ```

**Loop**: Return to Step 3 after hypothesis is added.

**Exit**: When user says no or declines to add more.

---

### Step 5: Verify Logic (Parallel Sub-Agents)

**Condition**: User finished adding hypotheses.

For EACH L0 hypothesis file in `.fpf/knowledge/L0/`, launch parallel fpf-agent with sonnet[1m] model:
- **Description**: "Verify hypothesis: <hypothesis-id>"
- **Prompt**:
  ```
  Verify the logical consistency of this hypothesis. Check for:
  - Internal contradictions
  - Logical fallacies
  - Unsupported leaps in reasoning
  - Circular arguments
  - Missing causal links

  Hypothesis ID: <hypothesis-id>
  Hypothesis File: .fpf/knowledge/L0/<hypothesis-id>.md

  Rate logical soundness on a scale of 0-1. If score >= 0.6, the hypothesis passes verification.

  **Move**: After you complete verification, move the file to `.fpf/knowledge/L1/` (if passes) or `.fpf/knowledge/invalid/` (if fails). Add verification notes to the file.
  ```

**Wait for all agents**, then check that files are moved to `.fpf/knowledge/L1/` or `.fpf/knowledge/invalid/`.

---

### Step 6: Validate Evidence (Parallel Sub-Agents)

For EACH L1 hypothesis file in `.fpf/knowledge/L1/`, launch parallel fpf-agent with sonnet[1m] model:
- **Description**: "Validate hypothesis: <hypothesis-id>"
- **Prompt**:
  ```
  Validate the evidence supporting this hypothesis. For each claim:
  - Is there empirical or theoretical support?
  - What is the quality of the evidence (direct observation, analogy, expert opinion, assumption)?
  - Are there counter-examples or contradicting evidence?
  - Rate evidence strength on a scale of 0-1.

  Hypothesis ID: <hypothesis-id>
  Hypothesis File: .fpf/knowledge/L1/<hypothesis-id>.md

  If overall evidence score >= 0.5, the hypothesis passes validation.

  **Move**: After you complete validation, move the file to `.fpf/knowledge/L2/` (if passes) or `.fpf/knowledge/invalid/` (if fails). Add validation notes to the file.
  ```

**Wait for all agents**, then check that files are moved to `.fpf/knowledge/L2/` or `.fpf/knowledge/invalid/`.

---

### Step 7: Audit Trust (Parallel Sub-Agents)

For EACH L2 hypothesis file in `.fpf/knowledge/L2/`, launch parallel fpf-agent with sonnet[1m] model:
- **Description**: "Audit trust: <hypothesis-id>"
- **Prompt**:
  ```
  Perform a trust audit on this hypothesis. Evaluate:
  - Source reliability of each piece of evidence
  - Confirmation bias risk
  - Survivorship bias risk
  - Anchoring effects
  - Overall epistemic humility

  Calculate R_eff (effective reliability) score and identify the weakest link in the reasoning chain.

  Hypothesis ID: <hypothesis-id>
  Hypothesis File: .fpf/knowledge/L2/<hypothesis-id>.md

  **Write**: Audit report to `.fpf/evidence/audit-{hypothesis-id}-{YYYY-MM-DD}.md`

  **Reply**: with R_eff score and weakest link
  ```

**Wait for all agents**, then check that audit reports are created in `.fpf/evidence/`.

---

### Step 8: Make Decision (FPF Agent)

Launch fpf-agent with sonnet[1m] model:
- **Description**: "Create decision record"
- **Prompt**:
  ```
  Create a Design Rationale Record (DRR) based on all surviving hypotheses and their audit reports. Compare hypotheses on:
  - R_eff scores
  - Evidence strength
  - Risk profile
  - Implementation feasibility
  - Alignment with constraints from context

  Select the best hypothesis and justify the decision. Document why alternatives were not chosen.

  Problem Statement: $ARGUMENTS
  L2 Hypotheses Directory: .fpf/knowledge/L2/
  Audit Reports: .fpf/evidence/

  **Write**: Decision record to `.fpf/decisions/`

  **Reply**: with decision record summary in markdown format:

  | Hypothesis | R_eff | Weakest Link | Status |
  |------------|-------|--------------|--------|
  | ... | ... | ... | ... |

  **Recommended Decision**: <hypothesis title>

  **Rationale**: <brief explanation>
  ```

**Wait for agent**, then check that decision record is created in `.fpf/decisions/`.
---

### Step 9: Present Final Summary (Main Agent)

1. Read the DRR from `.fpf/decisions/`
2. Present results from agent response.
3. Present next steps:
   - Implement the selected hypothesis
   - Use `/fpf:status` to check FPF state
   - Use `/fpf:actualize` if codebase changes
4. Ask user if he agree with the decision, if not launch fpf-agent at step 8 with instruction to modify the decision as user wants.

---

## Completion

Workflow complete when:
- [ ] `.fpf/` directory structure exists
- [ ] Context recorded in `.fpf/context.md`
- [ ] Hypotheses generated, verified, validated, and audited
- [ ] DRR created in `.fpf/decisions/`
- [ ] Final summary presented to user

**Artifacts Created**:
- `.fpf/context.md` - Problem context
- `.fpf/knowledge/L0/*.md` - Initial hypotheses
- `.fpf/knowledge/L1/*.md` - Verified hypotheses
- `.fpf/knowledge/L2/*.md` - Validated hypotheses
- `.fpf/knowledge/invalid/*.md` - Rejected hypotheses
- `.fpf/evidence/*.md` - Evidence files
- `.fpf/decisions/*.md` - Design Rationale Record
