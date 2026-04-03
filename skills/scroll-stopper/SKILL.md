---
name: scroll-stopper
description: Write high-engagement social media posts that stop the scroll. Takes a topic, writes a hook, delivers insight, and closes with a CTA that drives comments, saves, or clicks. Platform-aware formatting. Triggers on "write a post", "social media post", "scroll stopper", "write me a tweet", "Instagram caption", "LinkedIn post", "draft a post about".
weight: light
---

# Posts That Stop the Scroll

Write a high-engagement social media post on any topic. Hook → Insight → CTA. Every time.

## When This Fires

- "Write a post about [topic]"
- "Draft a tweet about [topic]"
- "Write an Instagram caption for [topic]"
- "LinkedIn post about [topic]"
- "Create a scroll-stopper post"
- Any request to write a specific social media post

## Prerequisites

1. **Read `brand-context.md`** — Required for voice/tone. If missing, ask for tone direction.
2. **Read `audience-profile.md`** if exists — use messaging angles.
3. **Read `content-pillars.md`** if exists — identify which pillar this post serves.
4. **User must provide:** topic OR let you pick from the content calendar.

## Workflow

### Step 1: Classify the Post

| Dimension | Options |
|-----------|---------|
| **Platform** | Twitter/X, Instagram, LinkedIn, TikTok, YouTube Community |
| **Goal** | Reach, Trust, Conversion |
| **Pillar** | [From content-pillars.md or inferred] |
| **Format** | Single post, Thread, Carousel script, Caption + visual direction |

If the user didn't specify platform, default to Twitter/X. Ask if unclear.

### Step 2: Write the Hook (First 1-2 lines)

The hook is everything. Rules:

**Hook Formulas That Work:**
| Formula | Example |
|---------|---------|
| **Contrarian claim** | "Most [industry] advice is designed to keep you average." |
| **Specific number** | "I analyzed 847 [things] and found 3 patterns nobody talks about." |
| **Open loop** | "The #1 reason your [thing] isn't working has nothing to do with [obvious cause]." |
| **Direct challenge** | "Stop doing [common practice]. Here's what works instead." |
| **Result tease** | "[Specific result] in [timeframe]. No [common objection]. Here's how." |
| **Pattern interrupt** | "Delete your [common tool]. You don't need it." |
| **Confession** | "I wasted [time/money] on [thing] before I figured this out." |

**Hook Anti-Patterns (NEVER use):**
- "In today's fast-paced world..."
- "Have you ever wondered..."
- "Let me tell you about..."
- "I'm excited to share..."
- Starting with a question that's easy to answer "no" to

### Step 3: Deliver the Insight (Body)

Platform-specific structure:

**Twitter/X (single):**
- Hook (1 line)
- Insight (2-4 lines, line breaks between each)
- CTA (1 line)
- Total: 280 chars or less for single, up to 4 tweets for thread

**Twitter/X (thread):**
- Tweet 1: Hook + promise of what's coming
- Tweets 2-N: One idea per tweet, each stands alone
- Final tweet: Summary + CTA
- Thread length: 5-12 tweets ideal

**Instagram (caption):**
- Hook line (shows in preview before "...more")
- 3-5 short paragraphs with line breaks
- Value-dense middle section
- CTA at end
- Hashtags: 5-10 relevant, mix of broad and niche

**LinkedIn:**
- Hook line
- Short paragraphs (1-2 sentences each)
- Personal angle or professional insight
- No hashtag spam (3 max)
- Professional but not corporate

**TikTok (script):**
- Hook in first 3 seconds (what you say on camera)
- Key points as bullet script
- Closing CTA
- Caption text (separate from script)

### Step 4: Close with CTA

Match CTA to goal:

| Goal | CTA Type | Example |
|------|----------|---------|
| **Reach** | Share/Save | "Save this for later" / "Send this to someone who needs it" |
| **Engagement** | Comment prompt | "What's your experience with [topic]? Drop it below." |
| **Trust** | Follow | "Follow for more [topic] breakdowns" |
| **Conversion** | Link/DM | "DM me '[keyword]' for [free resource]" / "Link in bio" |

### Step 5: Visual Direction (if applicable)

For platforms that need visuals (Instagram, TikTok):
- Suggest image/video concept
- Provide Nano Banana prompt if ad creative is needed
- Note: reference `brand-context.md` visual identity section for colors/style

## Output Format

```
PLATFORM: [Platform]
PILLAR: [Content pillar]
GOAL: [Reach | Trust | Conversion]

---

[THE POST — ready to copy/paste]

---

VISUAL: [Image/video direction if applicable]
BEST TIME TO POST: [Based on audience patterns]
HASHTAGS: [If applicable]
```

## Batch Mode

If user says "write 5 posts" or "batch of posts":
1. Vary pillars across the batch
2. Vary hook formulas (no two posts use the same formula)
3. Vary CTAs
4. Mix goals (not all conversion, not all reach)
5. Present as numbered list with all fields

## Hook Library Mode

When user says "generate hooks", "hook library", "hook formulas", or "give me 10 hooks":

Generate 10 hooks using 5 formulas (2 hooks per formula):

| Formula | Psychological Trigger | Hook Template |
|---------|---------------------|---------------|
| **Pattern interrupt** | Cognitive dissonance — breaks expected narrative | "Everyone says [common belief]. They're wrong." |
| **Specific number** | Credibility + curiosity — precision implies research | "I analyzed [N] [things] and found [unexpected insight]." |
| **Counterintuitive** | Surprise — contradicts what audience assumes is true | "[Do less of obvious thing] to [get more of desired result]." |
| **Credibility + result** | Social proof + aspiration — proves it's possible | "[Starting point] to [impressive result] in [timeframe]." |
| **Direct address** | Pattern match — reader self-selects instantly | "If you're a [specific person] with [specific problem], read this." |

For each hook provide:
- The hook text (customized to the user's topic/niche)
- Which psychological trigger it uses and WHY it works for this audience
- Rank the top 2 by scroll-stopping power for the specific audience

Save to `hook-library.md` as a reusable reference for future posts.

---

## Rules

1. **Hook or die** — if the first line doesn't stop the scroll, the post fails. Spend 50% of effort here.
2. **One idea per post** — don't cram 3 insights into one post. Split them.
3. **Platform-native** — write FOR the platform, not a generic post adapted to platforms
4. **Voice match** — must sound like the brand, not like AI. Read brand-context.md tone.
5. **Anti-slop** — no "game-changer", "unlock your potential", "level up". Real language only.
6. **Specific > vague** — "I increased revenue 34% in 6 weeks" beats "I grew my business"
7. **No engagement bait** — no "like if you agree" or "retweet for reach". Earn engagement with value.
