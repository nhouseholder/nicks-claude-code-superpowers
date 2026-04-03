---
name: content-performance-audit
description: Monthly social media performance audit. Tracks the 5 metrics that predict growth and sales (not vanity metrics). Diagnoses why posts flopped, finds top content angles to double down on, and delivers the ONE change to make next month. Produces a reusable monthly review template. Triggers on "monthly audit", "content performance", "what's working", "review my content", "performance review", "monthly review", "content audit".
weight: medium
---

# Monthly Performance Audit

Stop guessing. Start making decisions from data. This skill produces a monthly review that identifies what's actually driving growth and sales — not likes and impressions.

## When This Fires

- "Monthly content audit"
- "Review my content performance"
- "What's working on my social media?"
- "Monthly performance review"
- End of every month (schedule with `/schedule` for recurring use)

## Prerequisites

1. **Read `brand-context.md`** — Required for platform and niche context.
2. **Read `content-pillars.md`** if exists — to evaluate pillar performance.
3. **Read `content-calendar-*.md`** if exists — to compare plan vs. actual.
4. **User must provide** (or gather from analytics):
   - Platform(s) being reviewed
   - Current follower count
   - Average likes per post
   - Average comments per post
   - Leads generated from content (if tracked)
   - Revenue from content (if known, or "unknown")

## Workflow

### Phase 1: Revenue-Predictive Metrics

Identify the 5 metrics that actually predict growth and sales for THIS platform and audience size:

| Metric | What It Measures | Why It Matters More Than Vanity | How to Track |
|--------|-----------------|-------------------------------|-------------|
| **Saves/Bookmarks** | Content worth revisiting | Signals algorithm boost + genuine value | [Platform-specific tracking] |
| **DM volume** | Purchase intent | People who DM are 10x more likely to buy | Count weekly |
| **Profile visits from content** | Curiosity converted | Bridge between content and bio/offer | Platform analytics |
| **Email/list signups from social** | Owned audience growth | Followers you actually own | UTM links + landing page |
| **Reply rate (comments that are conversations)** | Depth of engagement | Comments > likes for trust-building | Manual review |

Customize these 5 to the specific platform. Instagram saves matter differently than Twitter bookmarks. LinkedIn engagement rate baselines differ from TikTok.

### Phase 2: Engagement Rate Benchmarks

Provide healthy benchmarks calibrated to platform AND audience size:

| Platform | Follower Range | Healthy Engagement Rate | You're Underperforming If |
|----------|---------------|------------------------|--------------------------|
| Instagram | <1K | [%] | [%] |
| Instagram | 1K-10K | [%] | [%] |
| Instagram | 10K-100K | [%] | [%] |
| Twitter/X | <1K | [%] | [%] |
| Twitter/X | 1K-10K | [%] | [%] |
| LinkedIn | <5K | [%] | [%] |
| LinkedIn | 5K-50K | [%] | [%] |
| TikTok | <10K | [%] | [%] |
| TikTok | 10K-100K | [%] | [%] |

Note: label benchmarks as industry averages. Actual rates vary by niche.

### Phase 3: Post Flop Diagnosis

When a post underperforms, diagnose WHY using this framework:

```
FLOP DIAGNOSIS TREE:
                     Post underperformed
                            │
              ┌─────────────┼─────────────┐
              │             │             │
         Low reach    Low engagement   Low conversion
              │             │             │
    ┌─────────┤      ┌──────┤      ┌──────┤
    │         │      │      │      │      │
  Hook     Timing  Topic  Format   CTA   Offer
  failed   wrong   miss   wrong   weak  mismatch
```

For each diagnosis point:

| Problem | Signal | Fix |
|---------|--------|-----|
| **Hook failed** | Low impressions relative to followers | Test different hook formula from library |
| **Timing wrong** | Good hook but low reach | Move to optimal posting time |
| **Topic miss** | Reach OK but low saves/comments | Topic doesn't resonate — check audience profile |
| **Format wrong** | Topic good but low engagement | Try different format (carousel vs. single, thread vs. tweet) |
| **CTA weak** | Engagement OK but no clicks/DMs | Strengthen or change CTA type |
| **Offer mismatch** | Clicks but no conversion | Content-to-offer bridge is broken |

### Phase 4: Top 3 Content Angles

Analyze last month's posts to find the 3 best-performing angles:

```
ANGLE 1: [Topic/angle]
Evidence: [Which posts, what metrics]
Why it worked: [Audience psychology reason]
Double-down plan: [3 new posts using this angle next month]

ANGLE 2: [same format]
ANGLE 3: [same format]
```

Method: Sort all posts by the revenue-predictive metrics from Phase 1 (saves, DMs, profile visits) — NOT by likes.

### Phase 5: The One Change

Based on the entire audit, identify the single highest-leverage change to make next month:

```
THE ONE CHANGE: [Specific, actionable change]
WHY THIS ONE: [Data-backed reasoning]
EXPECTED IMPACT: [What metric it should improve]
HOW TO MEASURE: [How you'll know it worked in 30 days]
```

## Output Format — Monthly Review Template

Save to `content-review-[YYYY-MM].md`:

```markdown
# Content Performance Review — [Month Year]

## Snapshot
| Metric | This Month | Last Month | Delta |
|--------|-----------|------------|-------|
| Followers | [N] | [N] | [+/-] |
| Avg engagement rate | [%] | [%] | [+/-] |
| Saves/bookmarks | [N] | [N] | [+/-] |
| DMs received | [N] | [N] | [+/-] |
| Leads from content | [N] | [N] | [+/-] |
| Revenue from content | [$] | [$] | [+/-] |

## Top 3 Performing Posts
1. [Post topic] — [key metric]
2. [Post topic] — [key metric]
3. [Post topic] — [key metric]

## Bottom 3 Posts + Diagnosis
1. [Post] — Diagnosis: [hook/timing/topic/format/CTA]
2. [Post] — Diagnosis: [hook/timing/topic/format/CTA]
3. [Post] — Diagnosis: [hook/timing/topic/format/CTA]

## Top 3 Angles to Double Down
1. [Angle] — [3 new post ideas]
2. [Angle] — [3 new post ideas]
3. [Angle] — [3 new post ideas]

## The One Change for Next Month
[Change + reasoning + measurement plan]
```

## Rules

1. **Revenue-predictive metrics only** — saves, DMs, profile visits, list signups, reply depth. NOT likes, NOT impressions.
2. **Data required** — if user can't provide numbers, help them set up tracking FIRST before running the audit
3. **Diagnosis before prescription** — identify WHY something failed before suggesting fixes
4. **One change, not ten** — the power is in focus. One high-leverage change beats ten scattered tweaks.
5. **Anti-slop** — no "keep up the great work" filler. Honest assessment, specific actions.
6. **Comparative** — always show this month vs. last month. Trends matter more than absolutes.
7. **Benchmarks are labeled** — always note that engagement benchmarks are industry averages, not guarantees
