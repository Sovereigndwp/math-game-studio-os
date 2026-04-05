# Game Engagement Playbook

Reusable design patterns extracted from ATC Math Tower, Grocery Dash, and Bakery Rush.
For use by all future games in the Math Game Studio OS.

Written April 2026. Source: real prototypes that were playtested, not theory.

---

## 1. What Makes These Games Sticky

All three games succeed because the math **is** the gameplay, not a gate before
gameplay. The player doesn't solve a problem and then get to play — the solving
is the playing.

**ATC Math Tower**: Solving the math fact (+100) is worth more than dispatching the
plane (+40). The scoring system tells the player: the math is the point.

**Grocery Dash**: The game never tells you the answer. You read the recipe, multiply
by guest count, perform ceiling division for pack sizes, and the checkout blocks you
if your math is wrong. The math is the shopping, not a quiz before shopping.

**Bakery Rush**: Tapping pastries whose values sum to the target IS the game. There
is no separate "math phase" and "play phase."

The sticky pattern: **math is the verb, not the toll booth.**

---

## 2. Reusable Engagement Rules

### Rule 1 — The Math Must Be the Highest-Scoring Action
If the player can succeed by ignoring the math (e.g., just tapping fast), the game
is broken. The math action must be the primary source of points, progress, or
survival. ATC: correct answer = +100, dispatch = +40. Grocery Dash: checkout blocks
entirely if the math is wrong — you cannot finish the level without correct
multiplication and division. Bakery: you literally cannot fill the order without
adding correctly.

### Rule 2 — Urgency Must Be Visible and Draining
Both games use patience/countdown bars that the player can see shrinking. Invisible
timers create anxiety. Visible timers create urgency — the player can see the
consequence approaching and choose to act faster.

### Rule 3 — Consequences Must Be Felt, Not Just Counted
ATC: a plane leaving without clearance costs -200 points. That hurts. Grocery Dash:
bumping a shopper costs -5 seconds, and the store manager chasing you costs -10 — you
can see your timer shrinking because you were careless. Bakery: overshooting now
drains patience seconds and the customer visibly frowns. The player must feel the
cost in the moment, not discover it on a score screen later.

### Rule 4 — Every Correct Action Gets an Immediate Reward
ATC: score flies up on correct answer, streak counter increments, time bonus ticks.
Bakery: pastry springs into the box, running total pulses, box glows when
approaching target. The gap between action and reward must be < 500ms.

### Rule 5 — Streaks Reward Sustained Focus
ATC: 3-correct streak bonus (+25), scaling to 6-correct at higher levels.
Bakery: every third completed order gives a score bonus. Streaks teach sustained
attention, not just one-shot accuracy.

### Rule 6 — One Session Must Be Completable in Under 5 Minutes
No child will play a 20-minute math game voluntarily. ATC levels have shift timers
(60-70s). Bakery has 7-10 orders per level. A player can finish one meaningful unit
of play in a school break or a parent's car ride.

### Rule 7 — Failure Must Be Recoverable, Not Final
ATC: wrong answer costs -20, not game over. Lives exist but are generous enough
to allow learning. Bakery: overshoot bounces back one item, costs patience but
doesn't end the order. The player can recover from mistakes within the same round.

### Rule 8 — The Theme Must Carry the Math
ATC: "clear the plane for takeoff" is more motivating than "solve 7 × 8."
Grocery Dash: "dinner guests are arriving and you need to buy the right packs" is
more motivating than "practice ceiling division." The narrative creates real stakes:
the guests will be disappointed if you fail. Bakery: "fill the customer's order" is
more motivating than "find numbers that add to 12." The wrapper must make the math
feel like a real job, not homework.

### Rule 9 — The Game Must Never Tell the Answer
Grocery Dash shows "per serving" amounts and the guest count but never computes the
total for you. The checkout receipt shows the worked solution AFTER the attempt —
corrective feedback, not pre-emptive help. ATC shows the math fact but the player
types the answer. The game should create the conditions for mathematical reasoning,
not reveal the answer and ask the player to confirm it.

### Rule 10 — Distractors Must Test Understanding, Not Just Memory
Grocery Dash places distractor items on shelves that look identical to real
ingredients. The player must cross-reference the recipe card. ATC uses color-coded
runways that require remembering which direction matches which color. Distractors
should test whether the player is actually reading and reasoning, not just
pattern-matching from memory.

### Rule 11 — Randomization Creates Replay
Grocery Dash randomizes the guest count each play. Same level, different math.
ATC randomizes math facts within the selected operations. This means the player
can't memorize answers — they must actually compute every time. And it means
"play again" produces a genuinely different experience.

---

## 3. Reusable Feedback and Reward Patterns

### Success Feedback Stack
Layer these in order — each adds to the one before:

| Layer | What | Timing | Example |
|-------|------|--------|---------|
| 1. Visual confirmation | Color change or glow | Instant (< 100ms) | Box border turns green |
| 2. Motion response | Spring, bounce, or fly | Immediate (100-300ms) | Pastry springs into box |
| 3. Numeric feedback | Score increment visible | Fast (200-500ms) | "+100" flies up and fades |
| 4. Streak acknowledgment | Counter or multiplier | On the beat (500ms) | "3x streak!" |
| 5. Emotional payoff | Emoji, celebration, sound | After confirm (500-900ms) | Customer smiles, confetti |

Never skip layers 1-2. They make every tap feel alive. Layers 3-5 are for
meaningful milestones (order complete, level clear).

### Failure Feedback Stack

| Layer | What | Timing | Example |
|-------|------|--------|---------|
| 1. Visual warning | Color shift or flash | Instant | Box border flashes red |
| 2. Motion consequence | Shake, bounce-back | Immediate (100-400ms) | Item wobbles and retreats |
| 3. Resource cost | Visible drain | During animation | Patience bar drops 3 seconds |
| 4. Character reaction | Mood shift | After drain | Customer frowns |
| 5. Recovery path | Clear next action | After all above | "Your total is now X — keep going" |

Never punish without showing the recovery path. The player must always know
what to do next.

### Near-Miss Feedback
The most engaging moment is when the player is ONE step from success.
- Bakery: "approaching target" glow when within 2 of the goal
- ATC: score approaching threshold triggers visible countdown of remaining points

Near-miss feedback creates anticipation and teaches precision.

---

## 4. Reusable Progression and Replay Patterns

### The Three-Phase Arc
Both games use the same structure:

| Phase | Levels | Purpose | Characteristics |
|-------|--------|---------|----------------|
| Warmup | 1-5 (or L1) | Learn the controls | Generous timers, hints visible, low targets |
| Core | 6-15 (or L2-L3) | Real gameplay | Timers tighten, values increase, focus required |
| Expert | 16-25 (or L4-L5) | Mastery | New mechanics unlock, multi-axis pressure |

### Progressive Unlock
ATC unlocks runways at specific levels. Each new runway gets a dedicated tutorial
screen. This pattern works everywhere:
- New item types (Bakery L4: cake slices worth +2)
- New constraints (Fire Dispatch L3: terrain matching)
- New tools (subtraction items, clean replay offers)

**Rule: never introduce more than one new mechanic per phase transition.**

### Score-Based or Star-Based Advancement
ATC and Bakery use score thresholds. Grocery Dash uses a 3-star rating:
- ★★★ Perfect: correct amounts, no avoidable waste, best time
- ★★ Good: correct amounts, some unavoidable overshoot
- ★ Passed: correct but avoidable waste

The star system creates a natural replay hook: "I got 2 stars, I want 3." It also
differentiates goals for different learners — some aim for completion, others for
perfection. Both approaches (score threshold and star rating) reward mastery over
mere survival.

### Replay Hooks
- ATC: per-level best scores, career total, missed fact review
- Grocery Dash: star ratings, best times, randomized guest counts (same level = different math)
- Bakery: streak tracking, session diagnostics
- All three: the replay question is "can I do it better?" not "can I finish?"

---

## 5. Reusable Onboarding Patterns

### Rule: Teach by Doing, Not by Reading
ATC L1-5 are "training mode" — the game plays normally but with longer patience
bars and auto-opening modals. The player learns the controls by using them in a
low-pressure real round, not by reading instructions.

### The Pre-Timer Preview
ATC gives a 3-second countdown before each level starts. Grocery Dash has a 4-step
full-screen tutorial before Level 1 — zero time pressure while learning — and the
timer only starts after the last tutorial slide is dismissed. Bakery shows the order
ticket before the belt matters. This preview window lets the player form a plan
before pressure begins. **The timer must never run during instruction.**

### Progressive Hint Removal
- Level 1: dispatch hints shown ("press ← for red")
- Level 3: hints still available but smaller
- Level 6: hints gone, player is expected to know the controls

**Rule: hints are scaffolding, not furniture. Remove them as the player proves competence.**

### First-Level Success Guarantee
Design L1 so that any player who understands "tap things" will succeed.
ATC L1: two planes, long patience, one operation. Bakery L1: targets 1-5, all
+1 items, generous patience. The first level exists to build confidence, not to test.

---

## 6. Reusable Tension and Urgency Patterns

### Visible Countdown > Hidden Timer
Both games show patience bars that drain visibly. The bar's color shifts:
- Green/amber → plenty of time
- Orange → getting tight
- Red → about to lose this one

The player reads urgency from color, not from a number.

### Escalating Penalty
ATC: ignored plane = -200 (catastrophic). Bakery: first overshoot = -2s patience
(mild), third overshoot = customer lost (catastrophic). The first mistake is
cheap. Repeated mistakes cascade. This teaches self-correction without punishing
exploration.

### Speed as Reward, Not Requirement
ATC: every remaining second at threshold = +50 points. Finishing early is a bonus,
not a requirement. Bakery: first-try orders = +100 vs +60 for retry. Speed is
rewarded but not gatekept.

### Multi-Axis Pressure (Expert Only)
ATC L16+: 4 runways mean 4 directional decisions under time pressure. Grocery Dash
L9+: prime-number guest counts + maximum ingredients + 5 shoppers + the manager
chasing you. Bakery L4+: mixed pastry values mean arithmetic under belt pressure.
Multi-axis pressure should only appear after the player has mastered single-axis play.

### The Antagonist Creates Urgency Without Punishment
Grocery Dash's store manager pathfinds toward the player. Getting caught costs -10
seconds but doesn't end the level. The manager creates a physical urgency layer
on top of the math — the player must think AND move. This is a reusable pattern:
an NPC that pressures the player creates more engagement than a bare countdown.
ATC uses this implicitly (planes have patience bars). Bakery could benefit from
a similar ambient threat (e.g., belt speeds up after an overshoot).

### Corrective Feedback After, Not During
Grocery Dash shows the full worked solution on the checkout receipt — but only after
the player has attempted the math. This is pedagogically stronger than showing hints
during play. The player gets to struggle, then sees exactly where their reasoning
went right or wrong. ATC shows missed facts on the level complete screen. Both games
separate the "doing" from the "reviewing."

---

## 7. Reusable Delight / Surprise / Humor Patterns

### Character Reactions
ATC doesn't have characters but Bakery does — customers smile on success, frown on
overshoot. Characters are cheap delight: one emoji change creates an emotional beat
that a score number cannot.

**Rule: if the game has characters, they must react to the player's performance.**

### The "Almost!" Moment
Bakery: approaching-target glow. ATC: threshold proximity. The near-miss is more
exciting than the easy success. Design for the "one more step" feeling.

### Celebration Proportional to Difficulty
Easy order filled? Small spring animation. Hard order filled with no overshoots?
Big emoji, score bonus, streak acknowledgment. The celebration should match the
achievement. Don't celebrate routine actions the same way you celebrate hard ones.

### Streak Surprise
ATC: streak bonuses scale with level. At L20, a 6-streak is worth more. The
player discovers this as they improve. Hidden depth that rewards returning players.

### Session Summary as Story
ATC: missed fact review on level complete. The player sees "you got 7×8 wrong
three times" — that's a story about what to practice. Grocery Dash: the checkout
receipt shows the full worked solution — "6 guests × 2 slices each = 12 slices.
Pack of 10: need ⌈12/10⌉ = 2 packs." That receipt is a math lesson disguised as a
shopping receipt. Bakery: session diagnostics showing per-level timeout/overshoot
counts. The summary should tell the player something they didn't already know.

### Physical Comedy and Spatial Humor
Grocery Dash adds something ATC and Bakery don't have: physical comedy. Bumping
shoppers, dodging the manager, screen shake on collision — these create laugh
moments that make the game feel human, not clinical. Shoppers teleport away after
collision (they can't block you permanently) which keeps it funny instead of
frustrating. This pattern is reusable: any game with a spatial component can add
ambient NPCs that create mild physical comedy.

### The "Waste Shame" Moment
Grocery Dash's checkout blocks you if you bought avoidably too much. You have to
walk back, return packs, and rethink. This is a powerful teaching moment disguised
as inconvenience: the player feels the cost of sloppy reasoning in lost time, not
just in a score penalty. The walk of shame back to the shelf is more memorable than
"-20 points." Physical consequences (walking, waiting, returning) are stronger
feedback than numeric consequences.

---

## 8. Platform-Fit Rules

### Zero Friction
ATC: single HTML file, no install, no account, no backend. Runs offline.
Grocery Dash: same — single HTML, zero dependencies, localStorage only.
This is the gold standard. Every barrier between "teacher shares link" and
"student is playing" is a lost user.

### Single File or Instant Load
If the game cannot load in under 3 seconds on a school Chromebook, it will not
be used in classrooms. ATC achieves this with zero dependencies. Bakery achieves
it with Vite + minimal deps.

### No Accounts, No Tracking, No Ads
Educational games that require login lose half their audience at the login screen.
ATC uses localStorage only. No external requests. This is a trust signal for
teachers and parents.

### Teacher Controls Must Be Simple
ATC: operation selection (add/sub/mul/div toggle), admin unlock code (LEVY).
Teachers need exactly two things: choose what math to practice, and unlock content
for differentiation. Nothing else.

### Keyboard-First Accessibility
ATC: full keyboard play — Tab to select, Enter to open, arrows to dispatch.
Every game must be playable without a mouse. Many school devices have unreliable
trackpads. Keyboard play also supports accessibility needs.

### Persistent Progress Without Accounts
ATC: localStorage with version-keyed data. Best scores, unlocked levels, and
career total persist across sessions. Version key wipes stale data automatically
on updates. This gives players continuity without authentication.

---

## 9. What Future Games Should Avoid

### Anti-Pattern 1 — Math as a Gate
"Solve this problem to unlock the next level" separates math from gameplay.
The player learns to tolerate the math, not enjoy it. Math must be woven into
the core action, not bolted on as a prerequisite.

### Anti-Pattern 2 — Invisible Consequences
If the player can't see why they failed, they can't learn from it. Every failure
must be visible, immediate, and paired with a recovery path.

### Anti-Pattern 3 — Flat Visual Treatment
If every element on screen has the same color, border, shadow, and size, the
player cannot distinguish interactive from passive, urgent from calm, success
from failure. Visual hierarchy is not decoration — it is gameplay communication.

### Anti-Pattern 4 — Too Many New Things at Once
Introducing a new mechanic AND a new difficulty level AND a new item type in the
same level transition creates strategic overload. One new thing per phase.

### Anti-Pattern 5 — No Replay Reason
If the player's only question after finishing is "now what?" the game has no
replay hook. Best scores, missed-fact review, streak records, and career totals
give the player a reason to return.

### Anti-Pattern 6 — Setup Friction
Any game that requires npm install, account creation, teacher configuration,
or a specific browser version will not survive first contact with a real classroom.

### Anti-Pattern 7 — Generic Feedback
"Good job!" and "Try again!" are not feedback. Feedback must be specific:
"You were at 9 — you only needed 3 more" or "You got 7×8 wrong twice."

---

## 10. Release Readiness Checklist

Every game must pass these before it ships:

- [ ] **Math is the verb** — the primary scoring action requires mathematical reasoning
- [ ] **First level guarantees success** — a new player can complete L1 without prior knowledge
- [ ] **Urgency is visible** — at least one countdown or patience bar is always on screen during play
- [ ] **Consequences are felt** — at least one failure type costs something the player can see drain
- [ ] **Streaks exist** — sustained correct play is rewarded with a visible multiplier or bonus
- [ ] **One session < 5 minutes** — a complete meaningful play unit fits in a school break
- [ ] **Failure is recoverable** — the player can recover from a mistake within the same round
- [ ] **Near-miss feedback exists** — the player gets visual/motion feedback when close to success
- [ ] **Characters react** — if characters exist, they respond to player performance
- [ ] **Celebration matches difficulty** — hard achievements get bigger rewards than easy ones
- [ ] **Onboarding is play** — L1 teaches by doing, not by reading
- [ ] **Hints are removed progressively** — scaffolding disappears as competence grows
- [ ] **Zero-friction platform fit** — loads in < 3s, no account, no install, keyboard playable
- [ ] **Teacher controls are simple** — operation/topic selection and level unlock, nothing else
- [ ] **Progress persists** — best scores and unlocked levels survive browser close
- [ ] **Session summary tells a story** — the end screen shows something the player didn't already know
- [ ] **Visual hierarchy is clear** — interactive, passive, urgent, and calm elements look different
- [ ] **Replay hook exists** — the player has a reason to return (beat my score, fix my weak facts)
- [ ] **Randomization prevents memorization** — same level produces different math on replay
- [ ] **The game never tells the answer** — the player must reason; solutions shown after, not during
- [ ] **Distractors test understanding** — items, options, or pathways exist that test real comprehension

---

*This playbook is a living document. Update it as new games produce new patterns.
Sources: ATC Math Tower, Grocery Dash Math Market, Bakery Rush.*
