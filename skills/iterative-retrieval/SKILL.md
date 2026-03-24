---
name: iterative-retrieval
description: Pattern for progressively refining context retrieval to solve the subagent context problem
origin: ECC
weight: light
---

# Iterative Retrieval Pattern

Solves the "context problem" in multi-agent workflows where subagents don't know what context they need until they start working.

## When to Activate

- Spawning subagents that need codebase context they cannot predict upfront
- Building multi-agent workflows where context is progressively refined
- Encountering "context too large" or "missing context" failures
- Designing RAG-like retrieval pipelines for code exploration

## The Problem

Subagents are spawned with limited context. Standard approaches fail:
- **Send everything**: Exceeds context limits
- **Send nothing**: Agent lacks critical information
- **Guess what's needed**: Often wrong

## The Solution: 4-Phase Loop (max 3 cycles)

### Phase 1: DISPATCH — Broad initial query

```javascript
const initialQuery = {
  patterns: ['src/**/*.ts', 'lib/**/*.ts'],
  keywords: ['authentication', 'user', 'session'],
  excludes: ['*.test.ts', '*.spec.ts']
};
const candidates = await retrieveFiles(initialQuery);
```

### Phase 2: EVALUATE — Score relevance

Score each file 0-1:
- **High (0.7+)**: Directly implements target functionality
- **Medium (0.5-0.7)**: Related patterns or types
- **Low (<0.5)**: Tangentially related or irrelevant

Identify what context is still missing.

### Phase 3: REFINE — Update search criteria

```javascript
function refineQuery(evaluation, previousQuery) {
  return {
    patterns: [...previousQuery.patterns, ...extractPatterns(evaluation)],
    keywords: [...previousQuery.keywords, ...extractKeywords(evaluation)],
    excludes: [...previousQuery.excludes, ...lowRelevancePaths(evaluation)],
    focusAreas: evaluation.flatMap(e => e.missingContext).filter(unique)
  };
}
```

### Phase 4: LOOP — Exit when sufficient

Exit when: 3+ high-relevance files AND no critical gaps. Otherwise refine and repeat (max 3 cycles).

```javascript
async function iterativeRetrieve(task, maxCycles = 3) {
  let query = createInitialQuery(task);
  let bestContext = [];
  for (let cycle = 0; cycle < maxCycles; cycle++) {
    const candidates = await retrieveFiles(query);
    const evaluation = evaluateRelevance(candidates, task);
    const highRelevance = evaluation.filter(e => e.relevance >= 0.7);
    if (highRelevance.length >= 3 && !hasCriticalGaps(evaluation)) {
      return highRelevance;
    }
    query = refineQuery(evaluation, query);
    bestContext = mergeContext(bestContext, highRelevance);
  }
  return bestContext;
}
```

## Example: Bug Fix Context

```
Task: "Fix the authentication token expiry bug"

Cycle 1:
  DISPATCH: Search "token", "auth", "expiry" in src/**
  EVALUATE: auth.ts (0.9), tokens.ts (0.8), user.ts (0.3)
  REFINE: Add "refresh", "jwt"; exclude user.ts

Cycle 2:
  DISPATCH: Search refined terms
  EVALUATE: session-manager.ts (0.95), jwt-utils.ts (0.85)
  EXIT: Sufficient context

Result: auth.ts, tokens.ts, session-manager.ts, jwt-utils.ts
```

## Integration with Agent Prompts

```markdown
When retrieving context for this task:
1. Start with broad keyword search
2. Evaluate each file's relevance (0-1 scale)
3. Identify what context is still missing
4. Refine search and repeat (max 3 cycles)
5. Return files with relevance >= 0.7
```

## Best Practices

1. **Start broad, narrow progressively** — Don't over-specify initial queries
2. **Learn codebase terminology** — First cycle often reveals naming conventions
3. **Track what's missing** — Explicit gap identification drives refinement
4. **Stop at "good enough"** — 3 high-relevance files beats 10 mediocre ones
5. **Exclude confidently** — Low-relevance files won't become relevant
