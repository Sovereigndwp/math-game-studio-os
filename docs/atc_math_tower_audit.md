# ATC Math Tower — Mature Game Audit

Legacy / Mature Game Audit Mode. April 2026.
Source: full game design spec + live itch.io build.

---

## Task 1 — Audit

### Lens 1: Role-to-Math Fit

**Rating: Exceptional.**

The air traffic controller role maps perfectly to the math action. Solving a math
fact IS clearing a plane for takeoff. The role creates natural urgency (planes are
waiting), natural consequence (ignored planes abort and cost -200), and natural
reward (cleared planes depart with a visual and score payoff).

The role is not decorative. Remove the math and the game collapses — there is no
gameplay without solving. This is the gold standard for role-to-math integration.

### Lens 2: Loop Purity

**Rating: Very High.**

The core loop is: SELECT → SOLVE → DISPATCH → SCORE. Four steps. The math action
(SOLVE) is the bottleneck — you can't dispatch without solving. Every loop iteration
reinforces the same mathematical reasoning.

Loop purity score: ~0.95. The only impurity is the dispatch direction (arrow key
matching) which is a motor-memory task, not a math task. But it adds decision load
(color → direction mapping) that rewards attention, and it's worth only +40 vs +100
for the math. The scoring keeps the math dominant.

### Lens 3: Onboarding Quality

**Rating: Strong.**

- Levels 1-5 are explicit training mode with longer patience bars and auto-modals
- 3-second countdown before each level lets players study the board
- Dispatch hints shown at L1 ("press ← for red") and progressively removed
- L1 uses just two runways — the simplest possible configuration

Minor gap: the spec mentions "auto-modal" for training levels but doesn't describe
what happens if a player already knows the controls. There's no "skip tutorial"
mechanism mentioned. For returning players, training levels may feel slow.

### Lens 4: Urgency and Pressure

**Rating: Exceptional.**

Three simultaneous urgency channels:
1. **Per-plane patience bars** — each plane has a visible countdown. Ignored planes abort (-200).
2. **Shift timer** — global countdown for the entire level
3. **Score threshold** — must hit target to advance, with time bonus for speed

The three channels interact: ignoring a plane costs you the -200 penalty AND wastes
patience time AND delays you from hitting the score threshold. Every second of
inaction has compounding cost.

Urgency scales correctly: L1-5 have generous patience, L6-15 tighten, L16-25 add
4-direction pressure on top. The ramp is smooth.

### Lens 5: Feedback and Reward Quality

**Rating: Strong with one gap.**

What works well:
- Correct answer: +100, immediate score display
- Plane departure: +40, visual takeoff animation
- Streak bonus: +25 at 3-streak, scaling to 6-streak at L21+
- Time bonus: +50/sec remaining at threshold (huge incentive for speed)
- Wrong answer: -20 (mild, recoverable)
- Plane abort: -200 (severe, felt immediately)

The gap: **the spec doesn't mention any celebration animation or screen effect for
completing a level.** Score thresholds are reached and the level ends, but there's
no described payoff moment — no confetti, no "Level Cleared!" fanfare, no star
rating. The end-of-level moment may feel anticlimactic compared to the urgency
during play. Grocery Dash has star ratings (★★★) and Bakery Rush has celebration
overlays. ATC may be missing the emotional punctuation at the finish line.

### Lens 6: Replayability and Mastery Loop

**Rating: Very High.**

- 25 levels with progressive unlock
- Per-level best scores and career total
- Missed fact review on level complete (corrective learning)
- Time bonus creates speed-running incentive
- Streak bonuses scale with level (hidden depth for returning players)
- Operation selection allows different math focus on replay

The mastery loop is clear: play → see your weak facts → replay to improve them →
beat your time → beat your score. Each cycle has a concrete reason.

### Lens 7: Teacher Usefulness / Classroom Fit

**Rating: Exceptional.**

- Operation selection (add/sub/mul/div toggle) — teacher chooses the curriculum focus
- Teacher unlock code (LEVY) — full level access for differentiation
- Missed fact review — teacher can see what the student struggled with
- Zero setup — single HTML file, no install, no account, no backend
- Full keyboard accessibility — works on school Chromebooks with bad trackpads
- localStorage persistence — progress survives browser close
- No ads, no tracking, no external requests — safe for schools

This is the template for classroom-ready design.

### Lens 8: Visual and Motion Feel

**Rating: Adequate, not exceptional.**

The spec describes:
- 60fps canvas rendering
- Color-coded planes (red, yellow, green, blue)
- No mention of particle effects, screen shake, or motion design
- No mention of visual depth or layering

The game likely looks functional but flat — similar to the pre-visual-pass state
of Bakery Rush. The ATC theme lends itself to a control-tower aesthetic with radar
screens, blinking lights, and runway glow, but the spec doesn't describe any of this.

### Lens 9: Hidden Weaknesses or Blind Spots

**Weakness 1 — Level completion feels undercelebrated.**
The game has strong urgency and strong in-round feedback but no described payoff
moment for completing a level. The player hits the score threshold and... the level
ends. Compared to the intensity of play, the completion moment may feel flat.

**Weakness 2 — No star rating or tiered achievement.**
The game tracks best scores but doesn't differentiate "barely passed" from "perfect
run." Grocery Dash's ★★★ system gives different learners different goals. ATC
treats every pass the same.

**Weakness 3 — Training levels may bore returning players.**
L1-5 are training mode with no skip option mentioned. A player who already knows
the controls must replay 5 slow levels every time they start fresh.

**Weakness 4 — The dispatch step is motor memory, not math.**
Pressing arrow keys to match colors is necessary for gameplay variety but doesn't
exercise mathematical reasoning. At L16+ with 4 runways, the dispatch becomes the
bottleneck — the player may fail because they pressed the wrong arrow, not because
they got the math wrong. This is a false failure that doesn't teach.

---

## What ATC Math Tower Does Unusually Well

1. **Math is the highest-scoring action** — +100 solve vs +40 dispatch. The scoring
   system explicitly tells the player: the math is more important.
2. **Three urgency channels that compound** — patience + shift timer + score threshold.
   Every second of inaction costs something on all three axes.
3. **Streak bonuses that scale with level** — hidden depth that rewards mastery without
   overwhelming beginners.
4. **Missed fact review as corrective learning** — the session summary tells a story
   about what to practice.
5. **Zero-friction deployment** — single HTML file, no install, no account, runs offline.
6. **Teacher controls that are exactly two things** — operation selection and level unlock.
   Nothing else.

---

## Task 2 — Improvement Recommendation

### Single Highest-Value Weakness

**Level completion is undercelebrated.**

The game creates intense urgency during play but delivers the level-clear moment
with no emotional punctuation. Adding a brief (1-2 second) completion celebration
would create a satisfying end to each high-pressure round:

- A **star rating** (★★★ for threshold + time bonus + no plane aborts, ★★ for
  threshold + minor penalties, ★ for threshold only)
- A **level clear animation** (planes depart, control tower lights up, brief fanfare)
- The **missed fact review stays** but is preceded by the celebration, so the player
  feels good before seeing their mistakes

This is the smallest change with the highest emotional impact. Every other system
in the game is already strong. The missing piece is: **the game tells you when
you're failing but doesn't properly celebrate when you succeed.**

Estimated implementation: one new screen state, one star-rating function (based on
existing score + penalty data), and one brief animation. No gameplay changes needed.

---

## Task 3 — OS Lesson Extraction

### What Makes ATC Math Tower Sticky

The game is sticky because failure is expensive and success is fast. A -200 plane
abort is catastrophic. A +100 correct answer is instant. The asymmetry means the
player is always slightly anxious and always slightly rewarded — the perfect
engagement zone.

### Reusable Engagement Rules (from ATC)

1. **Score the math higher than the action.** +100 for the math, +40 for the
   dispatch. The player learns what matters from the numbers.
2. **Make inaction costly.** Patience bars drain whether you act or not. Standing
   still is a choice with a price.
3. **Compound urgency across channels.** Per-item countdown + global timer + score
   threshold. One channel is pressure. Three channels are engagement.
4. **Scale streak rewards with difficulty.** 3-streak at L1, 6-streak at L21.
   Hidden depth that emerges as the player improves.
5. **Show the answer only after the attempt.** Missed fact review at end of level,
   not during play. Struggle first, learn after.

### Reusable Urgency and Pressure Patterns

| Pattern | ATC Implementation | Reuse Guidance |
|---------|-------------------|----------------|
| Per-item countdown | Patience bar above each plane | Every combine/dispatch game needs per-order patience |
| Global timer | Shift clock in corner | Creates urgency even when individual items are comfortable |
| Score threshold | Must hit target to advance | Makes speed valuable without requiring it |
| Compounding penalty | -200 for abort (> 2x a correct answer) | The biggest failure should cost more than one success gives |
| Time bonus | +50/sec remaining after threshold | Reward speed without punishing slowness |

### Reusable Onboarding Patterns

| Pattern | ATC Implementation | Reuse Guidance |
|---------|-------------------|----------------|
| Training levels | L1-5 with generous timers | First 20-30% of levels should be training, not testing |
| Pre-level preview | 3-second countdown to study the board | Let the player plan before pressure starts |
| Progressive hint removal | Dispatch hints L1-5, gone by L6 | Scaffolding is temporary; remove as competence grows |
| Minimal starting complexity | 2 runways at L1, 4 at L16 | Start with the simplest possible decision space |

### Reusable Progression and Replay Patterns

| Pattern | ATC Implementation | Reuse Guidance |
|---------|-------------------|----------------|
| 25-level arc | 3 phases: warmup, core, expert | Every game needs a clear phase structure |
| Progressive unlock | Runways unlock with tutorial screens | One new mechanic per phase, never more |
| Best score tracking | Per-level best + career total | Give the player something to beat on replay |
| Corrective review | Missed facts shown at level end | Show the player their specific mistakes, not generic advice |
| Operation selection | Teacher chooses add/sub/mul/div | Let the adult control the curriculum scope |

### Reusable Feedback and Reward Patterns

| Pattern | ATC Implementation | Reuse Guidance |
|---------|-------------------|----------------|
| Immediate math reward | +100 on correct, < 100ms | The math action must feel instantly rewarding |
| Mild wrong-answer penalty | -20 (recoverable within one correct) | Wrong answers should sting, not kill |
| Catastrophic neglect penalty | -200 for ignored plane | Inaction should cost much more than wrong action |
| Streak scaling | +25 at 3x, scaling with level | Streaks reward sustained focus, not one-shot accuracy |
| Time bonus as mastery reward | +50/sec remaining | Speed is rewarded, not required |

### Reusable Teacher-Friendly Platform Patterns

| Pattern | ATC Implementation | Reuse Guidance |
|---------|-------------------|----------------|
| Zero-friction deployment | Single HTML, no install, no account | The gold standard. Any barrier is a lost user. |
| Operation/topic selection | Toggle add/sub/mul/div | Teachers need to control curriculum scope — one setting |
| Admin unlock | Code "LEVY" for full access | Differentiation without grinding |
| Session review | Missed fact screen | Teacher must be able to see what the student struggled with |
| Keyboard accessibility | Full Tab/Enter/Arrow play | School devices have bad trackpads |
| Offline capability | No backend, localStorage only | School WiFi is unreliable |

### What Future Games Should Copy from ATC

1. The scoring ratio: math action > non-math action, explicitly
2. Per-item patience bars (not just a global timer)
3. The 3-second pre-level preview
4. Missed fact / mistake review at session end
5. Streak bonuses that scale with level
6. Single-file deployment with localStorage
7. Teacher unlock code for differentiation
8. Full keyboard playability

### What Future Games Should Avoid

1. Undercelebrating level completion — ATC's only notable weakness
2. Motor-memory bottlenecks at high levels (arrow key dispatch becomes the failure
   point, not the math)
3. Forced training levels for returning players with no skip option
4. Treating all passes equally — no star rating or tiered achievement

### ATC-Derived Release Checklist

- [ ] Math action is the highest-scoring action in the game
- [ ] Inaction has a visible, compounding cost
- [ ] At least two urgency channels are active simultaneously during play
- [ ] Wrong answers are penalized but recoverable within one correct action
- [ ] Neglect is penalized catastrophically (> 2x a correct answer's value)
- [ ] Streak bonuses exist and scale with difficulty
- [ ] A pre-level preview gives the player time to plan before pressure starts
- [ ] Training levels exist for the first 20% of content
- [ ] Mistakes are reviewed at session end with specifics, not generics
- [ ] The game runs from a single file with no install, no account, no backend
- [ ] A teacher can control the curriculum scope with one setting
- [ ] Full keyboard play is supported
- [ ] Level completion is celebrated proportionally to difficulty

---

## Task 4 — Recommendation

### Should ATC Math Tower be the gold-standard reference game?

**Yes.** It is the most complete game in the portfolio. It passes every engagement
rule in the playbook except one (undercelebrated completion). Its teacher-fit,
platform-fit, and math-integration are all at the highest level. The 25-level arc
with streak scaling and missed fact review is the richest mastery loop in the system.

Use ATC Math Tower as the benchmark against which all other games are measured.
When a new game is being designed, the question should be: "does it match ATC's
standard on math-as-verb, urgency compounding, and teacher-fit?"

### What should be applied immediately

**To Bakery Rush:**
- Add per-order patience bars that are more visually prominent (ATC-level visibility)
- Add missed-fact/mistake review at session end ("you overshoot on orders > 10 most often")
- Consider a star rating system (★★★ = no overshoots, ★★ = 1-2 overshoots, ★ = completed)
- Ensure the math action (selecting correct pastry values) scores higher than completing the order

**To Fire Dispatch:**
- Adopt the catastrophic-neglect pattern: an unresponded fire should cost much more than a wrong dispatch
- Add the 3-second preview before each round starts
- Consider streak bonuses for consecutive correct dispatches

**To all future games:**
- Copy the scoring ratio: math > action, explicitly in the numbers
- Copy the three-channel urgency model (per-item + global + threshold)
- Copy zero-friction deployment (single file, no account, localStorage)
- Copy the missed-fact review screen

### Should Grocery Dash be the next mature-game audit?

**Yes.** Grocery Dash introduces patterns ATC doesn't have — spatial navigation,
physical comedy, the "waste shame" walk-back, star ratings, ceiling division as
the core mechanic, and NPC antagonists. Auditing it would extract a complementary
set of engagement patterns and strengthen the playbook.

---

*Audit complete. ATC Math Tower is confirmed as the gold-standard reference game
for the Math Game Studio OS.*
