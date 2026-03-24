---
name: know-what-you-dont-know
description: Detects when Claude is about to implement domain-specific logic it hasn't verified understanding of. Forces background research BEFORE writing code in specialized domains (betting, finance, medicine, law, physics, etc.). Catches the dangerous failure mode where Claude is confident but wrong — not uncertain, but ignorant. Always-on metacognitive firewall.
weight: passive
triggers:
  - always-on — fires before any domain-specific implementation
  - when Claude is about to write scoring/settlement/payout logic
  - when Claude is about to implement financial calculations
  - when Claude is about to model real-world systems (sports, health, physics)
  - when the user corrects Claude on a domain concept for the second time
---

# Know What You Don't Know — Domain Ignorance Detector

## The Problem This Solves

Claude's most dangerous failure mode isn't uncertainty — it's **confident ignorance**. Claude will write prop bet scoring logic with absolute certainty, producing code that fundamentally misunderstands how prop bets settle. It won't flag uncertainty because it doesn't know it's wrong.

**Real example that cost hours:**
- Claude excluded fighter losses from round bet analysis, showing 92% win rate instead of 48%
- Claude was not uncertain. It was CERTAIN. And wrong.
- It did this 4 times in one session despite being corrected each time
- Root cause: Claude didn't understand that "Bob wins in R2" is a bet that LOSES when Bob loses — because Claude had never looked up how UFC props actually settle

This skill catches that failure mode by requiring domain verification before implementation.

## The Ignorance Detection Test

Before writing ANY domain-specific logic, Claude must pass this 3-question test:

### Question 1: "Can I explain the settlement rules from memory?"
For betting: How does this bet type settle? What outcomes = win, loss, push, void?
For finance: What are the tax implications? The regulatory constraints?
For medicine: What are the contraindications? The dosage calculations?

**If you can't answer with specific, concrete rules → RESEARCH FIRST.**

### Question 2: "Have I ever been corrected on this domain before?"
Check `~/.claude/anti-patterns.md` and `~/.claude/memory/` for prior corrections.
If the user has corrected you on this domain concept even ONCE → RE-READ the correction and verify your current approach matches.

**If you've been corrected before → READ THE CORRECTION BEFORE WRITING CODE.**

### Question 3: "Would a domain expert review my logic and find it correct?"
Imagine showing your code to a Vegas sportsbook operator, a CPA, a doctor, an attorney.
Would they say "yes, this is exactly right"?

**If you're not sure → RESEARCH FIRST.**

## Domain-Specific Checklists

### Sports Betting (UFC, NHL, NBA, MLB, CBB)
Before writing ANY scoring/payout/settlement code:
- [ ] Read `~/.claude/memory/topics/ufc_betting_domain_knowledge.md` (or sport equivalent)
- [ ] Read `~/.claude/memory/topics/ufc_betting_model_spec.md` (or sport equivalent)
- [ ] Can I explain: what happens to ALL bets when the picked fighter/team LOSES?
- [ ] Can I explain: how does a method/prop bet settle when the player wins but by the wrong method?
- [ ] Can I explain: how are parlay odds calculated? (multiply decimal odds)
- [ ] Can I explain: what's the payout formula for +150 odds? For -200 odds?
- [ ] Have I verified my logic matches the worked examples in the spec?

**If ANY checkbox fails → WebSearch for "[bet type] settlement rules [sportsbook]" and read 2+ sources before writing code.**

### Finance / Payments
Before writing ANY financial calculation code:
- [ ] Do I know the exact formula (not an approximation)?
- [ ] Am I handling rounding correctly (banker's rounding, floor, ceil)?
- [ ] Am I aware of currency/locale-specific rules?
- [ ] Have I verified against a real-world calculator or official documentation?

### APIs / Integrations
Before implementing ANY unfamiliar API:
- [ ] Have I read the official docs (not just guessed from the endpoint name)?
- [ ] Do I know the rate limits, auth requirements, and error codes?
- [ ] Am I using the correct API version?

### Statistics / ML
Before implementing ANY statistical method:
- [ ] Can I explain when this method is valid vs invalid?
- [ ] Do I know the assumptions it requires?
- [ ] Have I verified the formula against a textbook or paper?

## The Research Protocol (When Ignorance Is Detected)

When any checklist item fails:

1. **STOP writing code immediately.** Do not "figure it out as you go."

2. **Search for authoritative sources** (see Source Quality Hierarchy below):
   ```
   WebSearch: "[domain concept] rules" OR "[domain concept] how does it work"
   WebSearch: "[domain concept] settlement" OR "[domain concept] calculation formula"
   ```

3. **Read 2-3 authoritative sources** — apply the Source Quality Hierarchy strictly.

4. **Write down the rules** in your own words. Compare against what you were about to implement.

5. **Run the Research Completeness Test** (see below). If it fails, research more.

6. **If your implementation was wrong, fix it BEFORE proceeding.**

7. **Save the knowledge** to `~/.claude/memory/topics/<domain>.md` so future sessions don't repeat the research.

## Source Quality Hierarchy

Not all sources are equal. Claude must prioritize high-quality sources and reject low-quality ones.

### Tier 1 — Gold (USE THESE FIRST)
| Domain | Gold Sources |
|--------|-------------|
| **Sports betting** | Sportsbook house rules (DraftKings, FanDuel, BetMGM), BestFightOdds.com, state gaming commission rules |
| **Finance** | IRS publications, SEC filings, official bank documentation, GAAP/IFRS standards |
| **APIs** | Official documentation (docs.stripe.com, not "how to use Stripe" blog posts) |
| **Statistics** | Textbooks (ISLR, ESL), academic papers (arXiv, JSTOR), R/Python official docs |
| **Medicine** | FDA labels, UpToDate, PubMed systematic reviews, WHO guidelines |
| **Law** | Actual statutes, court opinions, bar association guides |

### Tier 2 — Silver (USE TO SUPPLEMENT)
- Stack Overflow answers with 50+ upvotes and verified by multiple users
- Wikipedia (for general concepts, but verify specifics elsewhere)
- Reputable industry blogs (e.g., Towards Data Science for ML, but verify formulas)
- Official tutorials from framework creators

### Tier 3 — Bronze (USE WITH CAUTION)
- Medium articles, personal blogs, dev.to posts
- YouTube tutorials (can be outdated or wrong)
- ChatGPT/AI-generated content (circular reasoning risk)
- Forum posts without verification

### Tier 4 — Reject (NEVER USE AS SOLE SOURCE)
- Random blog posts with no author credentials
- SEO-optimized "what is X" articles (often surface-level or wrong)
- Social media posts (Twitter/X, Reddit without verification)
- Content that contradicts Tier 1 sources
- Any source that doesn't cite its own sources

**Rule: At least ONE source must be Tier 1.** If you can't find a Tier 1 source, flag this to the user: "I couldn't find official/authoritative documentation for X. Here's what I found from lower-quality sources — please verify."

## Research Completeness Test

After researching, Claude must pass ALL 5 checks before considering research complete:

### Check 1: "Can I explain the edge cases?"
Not just the happy path — what happens in unusual situations?
- Sports betting: What happens on a draw? No contest? Doctor stoppage?
- Finance: What about refunds? Chargebacks? Currency conversion?
- APIs: What if the request times out? Rate limited? Invalid input?

**If you can only explain the happy path → research more.**

### Check 2: "Do my sources agree?"
Cross-reference at least 2 sources. If they contradict each other:
- The Tier 1 source wins
- If both are Tier 1, flag the discrepancy to the user
- NEVER average contradicting sources or pick the one that's "easier to implement"

**If sources contradict → flag to user, don't guess.**

### Check 3: "Can I produce a worked example?"
Take a concrete scenario and trace it through the rules step by step.
- Sports: "Fighter A predicted KO R2, actual SUB R1 — what's the P/L on each bet?"
- Finance: "Customer buys $100 item with 8.25% tax, returns it 30 days later — what's the refund?"

**If you can't produce a correct worked example → research more.**

### Check 4: "Would my implementation handle the user's SPECIFIC use case?"
Generic knowledge isn't enough. The user's system may have specific rules.
- Check memory files for user-defined rules that override or extend standard rules
- Check anti-patterns for prior corrections on this exact topic
- Check the project's spec files for domain-specific constraints

**If you haven't checked project-specific rules → check them before coding.**

### Check 5: "Is my knowledge current?"
Domain rules change. Tax rates change. API versions deprecate. Sportsbook rules update.
- Check when your source was published
- If the source is 2+ years old, search for updates
- If the user mentions a specific year or version, verify against THAT version

**If your source is outdated → search for current rules.**

## Research Depth by Domain Risk

| Risk Level | Examples | Minimum Sources | Completeness Checks Required |
|-----------|---------|----------------|------------------------------|
| **Critical** (money, health, legal) | Payout calculations, dosing, contracts | 3 sources (2 Tier 1) | All 5 checks |
| **High** (accuracy matters) | Scoring logic, statistical methods, API integrations | 2 sources (1 Tier 1) | Checks 1-4 |
| **Medium** (correctness preferred) | Data formatting, UI patterns, best practices | 1-2 sources | Checks 3-4 |
| **Low** (preference-based) | Color choices, naming conventions, code style | Memory/docs only | Check 4 only |

## Anti-Patterns This Prevents

| Anti-Pattern | What Happens | This Skill's Fix |
|-------------|-------------|-----------------|
| **Confident ignorance** | Claude writes wrong logic with no uncertainty flags | Force checklist verification before implementation |
| **Correction amnesia** | Claude gets corrected, then repeats the same mistake | Check anti-patterns before acting on domain concepts |
| **Reasoning from vibes** | Claude "figures out" domain rules by reasoning instead of looking them up | Require authoritative sources, not inference |
| **Single-correction learning** | Claude fixes the specific instance but doesn't learn the general rule | Force domain-knowledge file creation after research |
| **Assumed expertise** | Claude acts like an expert because it has seen the words before | Checklist forces verification of actual understanding |

## When NOT to Fire

- Pure coding tasks with no domain logic (CRUD, UI, refactoring)
- Domains Claude has already verified this session (check memory)
- Simple math that doesn't require domain expertise
- Tasks where the user has provided all domain rules explicitly

## The Golden Rule

**If you're about to write code that models real-world rules (settlement, scoring, pricing, dosing, taxing), and you haven't READ those rules from an authoritative source THIS SESSION, you are guessing. Stop guessing. Look it up.**

Claude's training data contains enough to sound convincing about almost anything. Sounding convincing is not the same as being correct. The difference costs the user hours of debugging and trust.
