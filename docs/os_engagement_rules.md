# OS Engagement Rules

The practical engagement reference for the Math Game Studio OS.
Derived from mature-game audits of ATC Math Tower and Grocery Dash,
and from prototype passes on Bakery Rush.

Use this document as a design checklist when building, reviewing, or
improving any game in the system.

---

## 1. What Makes Educational Games Sticky

A game is sticky when the player wants to come back. In educational games,
stickiness requires all three of these simultaneously:

1. **The math is the gameplay** — solving IS playing, not a gate before playing
2. **The consequence is physical** — the player sees, feels, or loses something real
3. **The replay is genuine** — same level, different math, or a better score to chase

If any one is missing, the game becomes either boring (no consequence), forgettable
(no replay), or tolerated (math as toll booth).

---

## 2. Non-Negotiable Engagement Rules

These are must-have. A game that violates any of these is not ready to ship.

### Rule 1 — Math Is the Verb
The primary scoring action, gate condition, or survival mechanic must require
mathematical reasoning. The player cannot succeed by ignoring the math.

*ATC: +100 for solving > +40 for dispatch. Grocery Dash: checkout blocks if math is wrong.*

### Rule 2 — The Answer Is Never Shown During Play
The game creates conditions for reasoning. Solutions are revealed only after the
attempt — on a receipt, a review screen, or a summary.

*Grocery Dash: checkout receipt shows worked solution. ATC: missed facts shown at level end.*

### Rule 3 — Urgency Is Visible and Compounding
At least two urgency channels must be active during play. Each must be visible
(not hidden timers) and ideally they compound — inaction costs on multiple axes.

*ATC: patience bar + shift timer + score threshold. Grocery Dash: level timer + manager chase.*

### Rule 4 — Consequences Are Felt, Not Just Counted
Errors must produce a consequence the player experiences in the moment — time
draining, items returning, characters reacting — not just a number changing.

*Grocery Dash: walk-of-shame to return packs. ATC: -200 for ignored plane. Bakery: patience drain + angry customer on overshoot.*

### Rule 5 — Failure Is Recoverable
A single mistake must not end the round. The player must be able to recover
within the same order/level. Catastrophic penalties exist only for neglect
(total inaction), not for honest wrong answers.

*ATC: wrong answer = -20 (recoverable). Plane abort = -200 (catastrophic neglect).
Grocery Dash: wrong cart = blocked but fixable. Timer out = level fail.*

### Rule 6 — Replay Produces Different Math
Randomization must ensure that replaying the same level generates genuinely
different mathematical problems, not the same sequence again.

*Grocery Dash: randomized guest count. ATC: randomized math facts. Bakery: shuffled target sequence (partial — could be stronger).*

### Rule 7 — Correct Play Is Celebrated
Success must feel emotionally distinct from neutral. Proportional celebration:
easy wins get mild feedback, hard wins get big payoff.

*ATC gap: weak level-clear celebration. Grocery Dash: ★★★ + "DINNER IS SAVED! 🎉". Bakery: box glows green, spring animation, 🎉.*

### Rule 8 — One Session Under 5 Minutes
A complete meaningful play unit (one level, one shift, one recipe) must fit
in a school break or a car ride. No 20-minute mandatory sessions.

### Rule 9 — Zero Friction to Start
No install, no account, no configuration. Teacher shares a link, student is
playing within 3 seconds. Single file or instant load.

### Rule 10 — The Theme Carries the Math
The role (air traffic controller, baker, shopper) must make the math feel
purposeful. "Clear the plane" > "solve 7×8." "Feed 6 guests" > "compute ⌈12/6⌉."

### Rule 11 — Distractors Must Test Understanding, Not Just Memory
Wrong options, shelved items, or alternate paths must require the player to
cross-reference and reason, not just pattern-match from memory.

*Grocery Dash: distractor items on shelves look identical to real ingredients — player must check the recipe card. ATC: color-coded runways require remembering which direction matches which color.*

### Rule 12 — Prompt, Action, and Confirm Must Be Within One Eye-Scan
The player should be able to read the prompt, take the action, and confirm the
result without moving their eyes across more than two element-heights of vertical
or horizontal distance. If the prompt is at the top and the action button is at
the bottom, the layout has failed. Compact the interaction zone so reading,
acting, and confirming happen in one visual cluster.

### Rule 13 — Math Should Be a Decision Chain, Not a Single Answer
The player should make connected mathematical decisions where each step's output
feeds the next. Read the problem → compute the scale → apply to quantities →
choose the best option → validate. A game where the player solves one number and
moves on is a quiz. A game where computations feed forward is genuine
problem-solving.

*Grocery Dash: read recipe → multiply by guest count → divide by pack size → choose between pack variants → validate at checkout. Five connected math steps.*

### Rule 14 — Replay Randomization Must Change the Math, Not Just Cosmetics
Variable inputs must change the actual mathematical problem on replay, not just
visual flavor. Different names on the same target number is cosmetic variation.
Different guest counts that change every multiplication is real variation. Fixed
inputs should be used during the learning phase; randomized inputs belong in the
mastery phase.

*Grocery Dash L1-L8: fixed guest counts (learnable). L9-L12: random guest counts (genuine replay). Same level, fundamentally different math each play.*

### Rule 15 — Introduce One New Complexity Layer Per Level, Never Two
Each level transition should add exactly one new axis of challenge: scaling, then
NPCs, then a second NPC, then more ingredients. Never introduce a new mechanic
AND increase difficulty simultaneously. The player must master the new element
at the current pressure level before the next element appears.

*Grocery Dash: L1-L3 learn the loop (no NPCs). L4 adds NPCs + distractors. L5 increases scaling. L6 adds another NPC. One thing per step across 12 levels.*

### Rule 16 — Scoring Must Signal What Matters Most
The scoring hierarchy should explicitly teach the player which action is most
important. If math is the core skill, the math action must be worth more points
than any other action. The player should be able to read the scoring table and
know what the game values most — without being told in words.

*ATC: correct math = +100, successful dispatch = +40. The numbers teach: math is the point, dispatch is the vehicle. A player who solves perfectly but dispatches slowly still outscores a player who dispatches fast but answers wrong.*

### Rule 17 — Neglect Must Cost Catastrophically More Than Honest Mistakes
A wrong answer should be cheap and recoverable. Ignoring a problem entirely
(plane aborts, customer leaves, timer expires with no attempt) should cost
many times more. This teaches self-correction without punishing exploration,
while making total inaction unacceptable.

*ATC: wrong answer = -20 (recoverable, 1/5 of a correct). Plane aborted from neglect = -200 (catastrophic, 10x a wrong answer). The penalty structure teaches: try and fail is fine, ignore and lose is not.*

### Rule 18 — P3 Requires World Reaction, Not Text Alone
Text-based reactions (status strip messages, chef lines) can support minimum
viable personality, but a strong P3 pass requires the world itself to respond
through visible state change — lights dimming, bars draining, borders glowing,
characters reacting visually. If only text changes, the world feels static.

*Bakery Rush and Unit Circle both reached P3 with text-only world reaction. The audit flagged this as the weakest P3 criterion in both games. Fire Dispatch's incident personality was stronger because the dispatch lines attached to named locations with visual urgency badges.*

### Rule 19 — P3 Cannot Rescue a Weak Core Loop
Personality, celebration, status strips, and character voice can enrich a
strong loop, but they cannot turn a fundamentally thin loop into a standout
game. If the core action is not satisfying to repeat before P3, adding charm
will produce a charming mediocre game, not a great one.

*Portfolio reset lesson: three games reached P3 with clean personality passes, but none had standout potential because the core loops were designed before the stronger pre-build system existed. P3 polish on a thin loop produces "nice but not wonderful."*

### Rule 20 — Correctness Should Not Always Be the Ceiling
When the game's domain supports it, later play should reward a mastery layer
beyond getting the right answer — efficiency, precision, prioritization, waste
reduction, or strategic tradeoffs. A strong game should eventually let the
player ask not only "Did I get it right?" but also "Did I do it well?"

*Grocery Dash: two pack sizes for the same ingredient — both correct, but one wastes less. ATC: solving faster earns a time bonus above the base score. Power Grid (future): routing power with less waste scores higher than brute-force routing.*

---

## 3. Urgency and Pressure Patterns

Use at least two. Games with all five feel the most alive.

| Pattern | What It Does | Example |
|---------|-------------|---------|
| **Per-item countdown** | Each order/plane/recipe has its own draining patience bar | ATC patience bars, Bakery patience bar |
| **Global timer** | A level clock ticking down regardless of per-item state | ATC shift timer, Grocery Dash level timer |
| **Score threshold** | Must reach a target to advance, creating speed incentive | ATC: hit target score to clear the level |
| **Physical antagonist** | An NPC that chases, blocks, or penalizes the player spatially | Grocery Dash: store manager (-10s on catch) |
| **Consequence escalation** | First error is mild, repeated errors cascade | Bakery: each overshoot drains more patience; third one loses the customer |

---

## 4. Progression and Replay Patterns

### Must-Have
- **Progressive unlock**: one new mechanic per phase, never more than one
- **Tiered achievement**: ★/★★/★★★ or score-based, so different learners aim for different goals
- **Best-score tracking**: the player has something to beat on return
- **Corrective review**: session end shows specific mistakes, not generic "try again"

### Strong Enhancement
- **Randomized problem generation**: same level = different math every play
- **Optimization above correctness**: a "better" answer beyond the "right" answer (pack size choice, efficiency)
- **Streak rewards that scale**: 3-streak bonus at L1, 6-streak at L20
- **Distractor items**: wrong options that test comprehension, not just memory

---

## 5. Feedback and Reward Patterns

### Every action gets immediate feedback (< 500ms)
| Layer | What | When |
|-------|------|------|
| 1. Visual | Color change, glow, border shift | Instant (< 100ms) |
| 2. Motion | Spring, bounce, particle burst | Immediate (100-300ms) |
| 3. Numeric | Score increment visible | Fast (200-500ms) |
| 4. Streak | Counter or multiplier | On the beat (500ms) |
| 5. Emotional | Character reaction, celebration | After confirm (500-900ms) |

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
The most engaging moment is when the player is one step from success.
Near-miss feedback (approaching-target glow, threshold proximity indicator)
creates anticipation and teaches precision. Design for the "one more step" feeling.

### Errors get specific diagnosis
- Wrong answer: name what was wrong ("you were at 9, you needed 3 more")
- Pattern errors: detect and name the misconception category
- Session end: show specific weak areas, not generic encouragement

### State-to-feedback must be distinct
Success, failure, near-miss, urgency, and reflection must each LOOK and FEEL
different. If success and failure use the same visual treatment, the player
cannot learn from feedback.

---

## 6. Onboarding Patterns

### The timer never runs during instruction
Tutorial steps, hint overlays, and onboarding modals must pause all countdowns.
Learning controls under time pressure teaches panic, not competence.

### Teach by doing, not by reading
L1 should be playable without reading instructions. The first level's design
must make the correct action obvious from the visual state alone.

### Progressive hint removal
- L1: full hints (dispatch directions, value labels, explicit prompts)
- L3: hints smaller or optional
- L5+: hints gone — player has demonstrated competence

### First level guarantees success
Any player who understands "tap/click things" must be able to complete L1.
L1 exists to build confidence, not to test.

### One new pressure dimension per phase
- Phase 1 (warmup): learn controls, no time pressure
- Phase 2 (core): add timer pressure
- Phase 3 (expert): add new mechanics or multi-axis pressure

---

## 7. Classroom and Platform-Fit Rules

### Non-negotiable
- [ ] Loads from a single file or URL with no install
- [ ] No account, no login, no sign-up
- [ ] No ads, no tracking, no external requests
- [ ] Full keyboard playability (Tab, Enter, arrows at minimum)
- [ ] localStorage persistence for progress (survives browser close)
- [ ] Works offline after first load

### Teacher controls (exactly two things)
1. **Topic/operation selection** — teacher chooses what math to practice
2. **Level unlock code** — teacher can differentiate by unlocking content

Nothing else. No settings panels, no dashboards, no admin interfaces.

### Session visibility
A teacher must be able to glance at a student's screen and understand:
- what level they're on
- whether they're succeeding or struggling
- what specific mistakes they're making (via session summary)

---

## 8. Delight, Surprise, and Physical Consequence Patterns

### The "Waste Shame" Moment
When a player makes an avoidable error, a physical consequence (walking back,
returning items, waiting) is stronger feedback than a numeric penalty. Grocery
Dash's checkout blocks on avoidable overshoot — the player walks back to the
shelf and rethinks. The walk of shame is more memorable than "-20 points."
Reusable anywhere a player can overshoot or waste.

### Physical Comedy and Spatial Humor
Games with a spatial component can add ambient NPCs that create mild physical
comedy (bumping shoppers, screen shake on collision). Shoppers teleport away
after collision so they stay funny, not frustrating. This pattern turns
navigation from dead time into engagement.

---

## 9. What Future Games Must Avoid

| Anti-Pattern | Why It Kills Engagement |
|-------------|----------------------|
| **Math as gate** | "Solve this to unlock the fun" teaches tolerance, not enjoyment |
| **Invisible consequences** | If the player can't see the cost, they can't learn from it |
| **Flat visual treatment** | Same color/border/shadow on everything = no hierarchy = no guidance |
| **Multiple new mechanics at once** | More than one new thing per phase = strategic overload |
| **Generic feedback** | "Good job!" and "Try again!" teach nothing |
| **Forced long sessions** | > 5 minutes mandatory = lost students |
| **Setup friction** | npm install, accounts, config = lost classrooms |
| **Showing the answer during play** | Pre-emptive help removes the reasoning the game is teaching |
| **No replay variation** | Same problems on replay = memorization, not learning |
| **Pressure without purpose** | Fast timers on a boring loop = stress, not engagement |

---

## 10. Release Readiness Checklist

Every game must pass ALL of these before shipping.

### Core Loop
- [ ] Math is the primary scoring/gating/survival action
- [ ] The answer is never shown during play
- [ ] First level guarantees success for any player
- [ ] One session completes in under 5 minutes

### Consequence and Feedback
- [ ] At least two urgency channels are active during play
- [ ] Errors produce a visible, felt consequence (not just score change)
- [ ] Failure is recoverable within the same round
- [ ] Success is celebrated proportionally to difficulty
- [ ] Near-miss feedback exists (visual cue when close to goal)
- [ ] Session end shows specific mistakes, not generic praise

### Replay and Mastery
- [ ] Replay produces different math problems
- [ ] Tiered achievement exists (★/★★/★★★ or score tiers)
- [ ] Best scores or progress persist across sessions
- [ ] Streak or sustained-focus rewards exist

### Onboarding
- [ ] Tutorial runs with zero time pressure
- [ ] Hints are progressively removed as competence grows
- [ ] One new mechanic per phase transition, never more

### Visual and Feel
- [ ] Interactive, passive, urgent, and calm elements look distinct
- [ ] Every player action gets immediate visual/motion feedback
- [ ] Characters react to player performance (if characters exist)

### Platform
- [ ] Loads in < 3 seconds, no install, no account
- [ ] Full keyboard playability
- [ ] Works offline
- [ ] Teacher can control topic scope with one setting
- [ ] No ads, no tracking, no external requests

---

*This is the OS's authoritative engagement reference.
Derived from ATC Math Tower, Grocery Dash, and Bakery Rush.
Update when new games produce new patterns.*
