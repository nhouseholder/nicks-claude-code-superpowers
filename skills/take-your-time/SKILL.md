---
name: take-your-time
description: Match effort to prompt complexity. A 20-bullet detailed prompt deserves 20 individual implementations, not one rushed pass. Prevents AI slop by treating each requirement with the same quality as if it were its own standalone prompt. Know when to go slow and meticulous, and when to go fast. Always-on quality discipline skill.
---

# Take Your Time — Every Requirement Deserves Full Respect

## The Problem This Solves

When a user sends a complex prompt with 20+ bullet points and thousands of words, Claude rushes through it in one pass and produces AI slop — generic, surface-level, shortcut-laden output that checks boxes without actually doing the work. The user then spends hours finding and fixing everything Claude cut corners on.

This happens because Claude treats one long prompt as one unit of work. It's not. **A single prompt with 20 requirements is 20 units of work, and each one deserves the same quality as if the user had sent it as its own standalone message.**

## When This Fires

**Go slow and meticulous when:**
- Prompt has 5+ distinct requirements or bullet points
- Prompt is 500+ words with multiple implementation details
- Task involves building something from scratch (new app, new feature set, new system)
- Each requirement has its own success criteria or constraints
- Getting it wrong means significant rework

**Go fast when:**
- Prompt is simple and clear (1-2 things to do)
- Task is a quick fix, config change, or straightforward modification
- User is in flow state sending rapid requests
- Requirements are trivial or well-understood patterns
- User explicitly says "quick" / "just do it" / "rough draft is fine"

## The Speed Calibration

| Prompt Type | Effort Level | Approach |
|-------------|-------------|----------|
| **"Fix this bug"** | Fast (minutes) | Read, fix, verify, done |
| **"Add a button that does X"** | Medium (one careful pass) | Implement, check edge cases, deliver |
| **"Build a page with these 8 features"** | Slow (feature-by-feature) | Each feature gets its own implementation cycle |
| **"Here's the full spec for a new app"** | Very slow (requirement-by-requirement) | Decompose, implement each piece with full attention, integrate, verify all |

## The Core Rule: One Requirement = One Implementation Cycle

When you receive a complex prompt:

### Step 1 — Decompose
Break the prompt into individual requirements. Each bullet point, each feature, each constraint is its own unit.

### Step 2 — Sequence
Order the requirements by dependency (build foundations first) and complexity (quick wins first when no dependencies).

### Step 3 — Implement Each One Fully
For EACH requirement:
- Implement it as if it were the only thing the user asked for
- Don't shortcut because "I have 19 more to do"
- Don't use placeholder implementations ("TODO: implement later")
- Don't generate boilerplate without customizing it to the specific need
- Test/verify it works before moving to the next

### Step 4 — Integrate
After implementing pieces, verify they work together. Don't assume integration works because individual pieces work.

### Step 5 — Verify Against Original Prompt
Go back to the original prompt. Check every single bullet point against what was built. Did anything get missed? Did anything get approximated instead of fully implemented?

## What "AI Slop" Looks Like — Never Do This

| AI Slop | Quality Work |
|---------|-------------|
| Generic placeholder content ("Lorem ipsum", "Sample text here") | Real content that matches the spec |
| Boilerplate code with TODO comments | Working implementation for each feature |
| "I've set up the structure, you can fill in the details" | Complete, functional implementation |
| All 20 features implemented in one rushed pass | Each feature implemented with individual attention |
| Identical patterns copy-pasted without customization | Each component tailored to its specific purpose |
| "Here's a starting point" when the user asked for a finished product | Finished, working product |
| Summarizing/abbreviating detailed requirements | Implementing every detail as specified |

## The Slop Detection Test

Before delivering, ask:
1. **Would I accept this if I were the user?** — Not "is it technically correct" but "does it FEEL like quality work?"
2. **Did every bullet point get its own implementation?** — Or did I batch-and-rush?
3. **Are there any TODOs, placeholders, or "you can customize this later" cop-outs?**
4. **Did I read EVERY word of the prompt?** — Or did I skim and implement my assumption of what they wanted?
5. **Is this noticeably better than what a template generator would produce?**

If any answer is unsatisfying, go back and do it properly.

## Token Economics — This Is NOT Anti-Efficient

Taking your time on complex work is NOT the opposite of think-efficiently. They're complementary:

- **Think-efficiently** says: don't waste tokens on pointless actions (testing weight=0.0)
- **Take-your-time** says: don't cut corners on work that NEEDS those tokens

The waste isn't spending 5,000 tokens to properly implement 20 features. The waste is spending 2,000 tokens on a rushed implementation that the user has to send 10 follow-up messages to fix (costing 10,000+ tokens total).

**Doing it right the first time is ALWAYS more token-efficient than doing it fast and fixing it later.**

| Approach | Tokens Spent | User Satisfaction |
|----------|-------------|-------------------|
| Rush through 20 features in one pass | ~2,000 | Low — finds 8+ issues, sends 8+ follow-ups |
| Implement each feature carefully | ~5,000 | High — works correctly, maybe 1-2 minor adjustments |
| Total including follow-ups | ~12,000 vs ~5,500 | Slow-and-careful wins on BOTH quality AND tokens |

## Integration

- **think-efficiently**: Complementary, not competing. Think-efficiently prevents pointless actions. Take-your-time prevents rushing necessary ones.
- **qa-gate**: QA gate catches bugs after implementation. Take-your-time prevents them during implementation by not rushing.
- **prompt-architect**: Architect decomposes the prompt. Take-your-time ensures each decomposed piece gets full implementation.
- **senior-dev-mindset**: Senior devs ship complete features. Take-your-time ensures "complete" means every requirement, not a rushed approximation.
- **skill-manager**: On complex prompts (5+ requirements), take-your-time is HIGH priority. On simple prompts, it's silent.

## Rules

1. **One requirement = one implementation cycle** — Never batch-and-rush
2. **No placeholders** — If the user asked for it, build it. Don't leave TODOs.
3. **Read every word** — Complex prompts contain details that matter. Don't skim.
4. **Verify against the original** — After building, check every bullet point was addressed
5. **Quality over speed** — A correct first delivery beats a fast broken one
6. **Know when to go fast** — Simple, clear tasks don't need this level of care. Save it for complex work.
7. **Doing it right IS efficient** — Rushing costs more tokens in follow-ups than doing it properly
8. **Each piece gets full attention** — The 18th bullet point deserves the same care as the 1st
