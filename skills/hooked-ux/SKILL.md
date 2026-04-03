---
name: hooked-ux
description: Analyze product retention using the Hook Model (trigger, action, reward, investment). Use when users aren't coming back, engagement is low, you need to improve retention, or designing a habit loop for a product feature.
weight: light
---

# Hooked UX — Retention & Engagement Audit

Maps your product against Nir Eyal's Hook Model to find where the habit loop is breaking. Use this when users sign up but don't return.

## When This Fires

- "users aren't coming back"
- "improve retention"
- "habit loop"
- "engagement"
- "why do users leave"
- Any site-review or site-audit where retention is a concern

## The Hook Model Audit

### 1. TRIGGER — What brings users back?

**External triggers** (you control):
- [ ] Email notifications with personalized, actionable content?
- [ ] Push/browser notifications (if applicable)?
- [ ] Social sharing that brings new/returning users?

**Internal triggers** (user's own motivation):
- [ ] What emotion drives usage? (boredom, curiosity, FOMO, anxiety, desire to win)
- [ ] Is the product associated with a specific routine or moment?
- [ ] Does the user think of this product when they feel [emotion]?

**Diagnosis:** If no internal trigger exists, the product is 100% dependent on external triggers — retention will always be fragile.

### 2. ACTION — Is the desired action easy enough?

Fogg Behavior Model: Behavior = Motivation × Ability × Trigger

- [ ] Can the core action be completed in <10 seconds?
- [ ] Is the number of steps minimized? (each step loses ~20% of users)
- [ ] Does it work on mobile without friction?
- [ ] Is the UI obvious enough that no instructions are needed?
- [ ] Login/auth friction is minimal? (no forced sign-up before value)

**Diagnosis:** If the action requires more than 3 taps/clicks, simplify. The first session should deliver value in under 30 seconds.

### 3. REWARD — Does the user get something variable?

Three types (at least one must be present):

**Tribe** (social validation):
- [ ] Does the user see what others are doing? (social proof, leaderboards)
- [ ] Is there recognition or status for engagement?

**Hunt** (information/resources):
- [ ] Does the product surface new, unpredictable content each visit?
- [ ] Are there personalized recommendations that change?
- [ ] Is there a "feed" or "discovery" element?

**Self** (mastery/completion):
- [ ] Does the user feel progress? (streaks, levels, completion %)
- [ ] Is there a sense of accomplishment?
- [ ] Can users see themselves improving?

**Diagnosis:** Fixed rewards (same content every visit) kill retention. At least one reward type must be variable.

### 4. INVESTMENT — Does the user put something in?

Investment increases switching cost and improves future experience:

- [ ] Does the user create data that makes the product better? (preferences, history, favorites)
- [ ] Does the product get smarter/more personalized with use?
- [ ] Would leaving mean losing something? (saved data, reputation, customization)
- [ ] Does investment load the next trigger? (following someone → future notification)

**Diagnosis:** If users can leave with zero switching cost, they will. Every session should accumulate value that makes the next session better.

## Output Format

```
HOOK MODEL AUDIT — [Product Name]

Trigger:    STRONG / WEAK / BROKEN — [diagnosis]
Action:     STRONG / WEAK / BROKEN — [diagnosis]
Reward:     STRONG / WEAK / BROKEN — [diagnosis]
Investment: STRONG / WEAK / BROKEN — [diagnosis]

The loop breaks at: [weakest phase]

Top 3 retention fixes:
1. [specific, implementable change]
2. [specific, implementable change]
3. [specific, implementable change]
```

## Applying to Sports Betting / Prediction Sites

For sites like MMALogic, Diamond Predictions, Courtside AI:
- **Trigger:** Upcoming fight/game → email/notification with preview
- **Action:** Check predictions in <5 seconds from homepage
- **Reward (Hunt):** New predictions, updated odds, fresh analysis each event
- **Reward (Self):** Track record, accuracy streaks, P/L history
- **Investment:** Favorites, custom alerts, bet tracking history
