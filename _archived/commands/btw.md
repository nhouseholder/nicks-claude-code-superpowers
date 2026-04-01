Quick side question — answer in a background subagent to avoid polluting the main conversation context.

Spawn a background Agent with model=haiku to answer this question concisely (1-3 sentences max). Do NOT use the main conversation to answer. The agent should:
1. Answer the question directly
2. Keep it brief — this is a "by the way" side question, not a deep research task
3. Return the answer to the main conversation

Question: $ARGUMENTS
