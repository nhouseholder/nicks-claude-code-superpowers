---
name: parallel-tool-routing
description: Automatically identify which tool calls in a response can run concurrently vs must be sequential, and always maximize parallelism. Always-on efficiency skill that reduces wall-clock time without changing results. Before making tool calls, batch all independent ones into a single response.
---

# Parallel Tool Routing — Maximize Concurrent Execution

Before making tool calls, always evaluate which ones can run in parallel. Never run sequentially what could run concurrently.

## Always Active

This skill shapes every response that involves 2+ tool calls. Before emitting tool calls, classify their dependencies.

## The Decision Tree

For every group of planned tool calls, ask:

```
Does call B depend on the RESULT of call A?
  YES → Sequential (B waits for A)
  NO  → Parallel (run A and B together)
```

### Independence Criteria

Two tool calls are independent (can parallelize) when:
- They read different files
- They search different paths or patterns
- They run commands that don't share state
- One doesn't need the output of the other to set its parameters

Two tool calls are dependent (must be sequential) when:
- Call B uses a value returned by call A (file path, line number, etc.)
- Call B modifies a file that call A also modifies
- Call B is a verification of call A's work (test after edit)
- Call A creates something that call B reads

## Common Parallel Patterns

### Multi-file reads — ALWAYS parallel
```
# BAD: Sequential reads
Read("file1.js")  # wait...
Read("file2.js")  # wait...
Read("file3.js")  # wait...

# GOOD: All at once
Read("file1.js") + Read("file2.js") + Read("file3.js")  # one round trip
```

### Multi-file grep — ALWAYS parallel
```
# BAD: One at a time
Grep(pattern="X", path="src/")
Grep(pattern="Y", path="lib/")

# GOOD: Together
Grep(pattern="X", path="src/") + Grep(pattern="Y", path="lib/")
```

### Exploration + context gathering — ALWAYS parallel
```
# Investigating a bug? Read the error file AND search for related patterns simultaneously
Read("failing-file.js") + Grep(pattern="relatedFunction", path="src/")
```

### Edit + unrelated read — PARALLEL
```
# Editing file A while reading file B for context on the next change
Edit("fileA.js", ...) + Read("fileB.js")
```

### Independent bash commands — PARALLEL
```
# Check git status AND run a build
Bash("git status") + Bash("npm run build")
```

## Common Sequential Patterns (DO NOT parallelize)

### Read then edit — SEQUENTIAL
```
Read("file.js")       # must read first
→ Edit("file.js", ...)  # then edit based on what you read
```

### Edit then verify — SEQUENTIAL
```
Edit("file.js", ...)   # make the change
→ Bash("npm test")      # verify it works
```

### Grep then targeted read — SEQUENTIAL
```
Grep(pattern="fn", path="file.js")  # find the line
→ Read("file.js", offset=N, limit=M)  # read just that section
```

### Create then use — SEQUENTIAL
```
Write("new-file.js", ...)  # create the file
→ Bash("node new-file.js")  # run it
```

## Batch Size Guidelines

- **2-5 parallel calls**: Always good. Do it.
- **6-10 parallel calls**: Fine for reads/greps. Be cautious with edits/writes.
- **10+**: Consider if all are truly needed. But if they are, parallelize.

## Self-Check Before Every Response

When about to make multiple tool calls, run this quick mental check:

1. List all planned tool calls
2. Draw dependency arrows (A → B means B depends on A)
3. Anything without an incoming arrow can run in the first batch
4. After the first batch completes, run everything that depended on it
5. Repeat until all calls are scheduled

## Rules

1. **Default to parallel** — if you're not sure whether two calls are dependent, they probably aren't
2. **Never read files one at a time** when you know you need multiple files
3. **Grep calls are almost always parallelizable** — they're read-only
4. **Edits to different files can be parallel** — they don't conflict
5. **Edits to the same file must be sequential** — they can conflict
6. **This saves time, not intelligence** — same results, just faster delivery
