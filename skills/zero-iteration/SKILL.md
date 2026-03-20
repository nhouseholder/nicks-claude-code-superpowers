---
name: zero-iteration
description: Mentally execute code before writing it. Trace inputs through logic, predict outputs, catch bugs before they exist. Reduces edit-test-fix cycles by getting it right the first time. Always-on awareness skill that activates during any code generation.
---

# Zero Iteration — Get It Right the First Time

Before writing code, run it in your head. Trace the data. Predict the output. Catch the bug before it exists. The fastest debugging is the debugging you never have to do.

## Always Active

This skill fires automatically whenever you're about to write or modify code. It's a mental discipline, not a tool — zero token overhead until it catches something.

## The Mental Execution Protocol

### Before Writing Any Function

```
1. INPUTS  — What types/shapes come in? What are the edge cases?
2. TRACE   — Step through the logic line by line with concrete values
3. OUTPUT  — What exactly comes out? Does it match the caller's expectation?
4. FAIL    — What makes this break? Null? Empty? Concurrent access? Off-by-one?
```

### Before Modifying Existing Code

```
1. CURRENT — What does this code do right now? (Read it, don't assume)
2. CALLERS — Who calls this? What do they expect?
3. CHANGE  — Apply your modification mentally
4. TRACE   — Run through with the same inputs as before — does it still work?
5. EDGE    — Run through with edge case inputs — does the change break them?
```

## Common Pre-Bugs to Catch

### Data Shape Mismatches
```
API returns: { data: { items: [...] } }
Code assumes: response.items  ← WRONG: response.data.items
```
**Rule**: Verify the actual shape before accessing nested properties.

### Off-by-One Errors
```
for (let i = 0; i <= arr.length; i++)  ← WRONG: should be <
arr.slice(0, n)  ← Does this include index n? No, it's exclusive.
```
**Rule**: Trace with arrays of length 0, 1, and 3. Check boundaries.

### Async Timing
```
const data = fetchData()  ← Missing await
setState(newVal); console.log(state)  ← State hasn't updated yet
```
**Rule**: For every async call, verify await/then. For every state update, don't read the new value immediately.

### Type Coercion Traps
```
"5" + 3 = "53"  (string concat, not addition)
null == undefined  (true)
[] == false  (true, but [] is truthy)
```
**Rule**: When mixing types, trace the actual coercion.

### Reference vs Value
```
const copy = original  ← Same reference, not a copy
arr.sort()  ← Mutates in place, doesn't return new array (well, it does, but it's the same array)
```
**Rule**: When "copying" objects/arrays, verify it's a real copy if mutation matters.

### Import/Export Mismatches
```
export default function X()  →  import { X }  ← WRONG: import X
export function X()  →  import X  ← WRONG: import { X }
```
**Rule**: Before writing an import, check the export style.

## The Three-Value Test

For any function you write, mentally run it with three inputs:

1. **The happy path** — Normal expected input
2. **The empty/zero case** — Empty string, empty array, 0, null
3. **The boundary case** — Max length, negative number, special characters

If all three produce correct output → write the code.
If any fails → fix the logic BEFORE writing.

## Token Economics

This skill costs zero tokens when code is correct (it's mental execution, not output). It only costs tokens when it catches a pre-bug — and those tokens are far cheaper than a debug cycle.

## Rules

1. **Trace before you type** — Never write a function without mentally running it first
2. **Concrete values** — Don't trace with "some object", trace with `{ id: 1, name: "test" }`
3. **Check the callers** — Your function is only correct if it satisfies its consumers
4. **Three-value test** — Happy path, empty case, boundary case. Every time.
5. **Silent when clean** — Don't announce "I traced through the code mentally." Just write correct code.
6. **Speak up when caught** — If you catch a pre-bug, briefly mention it: "Caught an off-by-one before writing — using `<` not `<=`"
