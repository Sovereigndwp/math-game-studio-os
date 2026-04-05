# Game Design Intelligence
## Extracted from GameForge 10-Day Facilitator Curriculum

This document is a living OS-level reference. Every rule below was sourced from the
GameForge facilitator guides (Days 1–10) and cross-validated against real failures
observed in Bakery Rush and Fire Station Dispatch during Pass 1 development.

Treat every section here as a reusable design constraint the OS can check against —
not aesthetic preference, but structural logic for building games that teach.

---

## 1. The Six Building Blocks of Every Game

Source: Day 1

Every game — no matter the theme, platform, or mechanic — can be analyzed through six atoms.
The OS should be able to map any prototype_spec against all six before passing it forward.

| Atom | Question It Answers |
|------|---------------------|
| **Goal** | What is the player trying to do? |
| **Rules** | What is allowed and not allowed? |
| **Challenge** | What makes it hard? |
| **Interaction** | How does the player act on the world? |
| **Feedback** | How does the world respond to the player? |
| **Theme/Story** | Why does any of this matter in the game's world? |

**OS rule:** A prototype_spec that cannot answer all six clearly is not ready to build.
The `core_loop_translation` block already covers Goal, Interaction, and Feedback.
Challenge and Rules should be expressible via `difficulty_profile` and `interaction_constraints`.
Theme is covered by `concept_anchor`.

---

## 2. The Core Loop Sentence Test

Source: Day 7

> "If you cannot describe your core loop in one sentence, your loop is not clear enough."

This is one of the most important teachable tests in game design. A well-formed loop
sentence has the form:

> `[Player action] → [World response] → [Player decision resets]`

Examples:
- Bakery: "Player taps pastries to accumulate a target value; when the total matches the order, the order clears for score."
- Fire Dispatch: "Player selects a subset of trucks whose capacities sum exactly to the incident demand, then dispatches."
- Unit Circle: "Player clicks a position on the SVG circle to set an angle, confirms, and receives score based on precision."

**OS rule:** `core_loop_sentence` is now a required field in `prototype_spec`. If an agent
cannot produce a one-sentence loop, the spec must revise. This is a gate-level check (Dim 7).

**Two loop levels every game needs (Day 7 extension):**
- **Moment-to-moment loop**: what happens in 5–15 seconds (tap, result, reset)
- **Session loop**: what keeps the player engaged for 20–30 minutes (progression, difficulty arc, streak)

---

## 3. The Luck/Skill Spectrum

Source: Day 2

Every game sits somewhere between pure luck (dice roll decides everything) and
pure skill (outcome is entirely determined by player decisions). Neither extreme is
inherently wrong, but the ratio must be **declared intentionally**, not left accidental.

Key insight: **the satisfaction of winning scales with perceived skill influence.**
A win that feels lucky teaches less than a win that feels earned.

For math education games, the target is typically **0.75–0.95 skill** (mostly skill, with
small luck variance to prevent memorization and maintain engagement across sessions).

**OS rule:** `luck_skill_ratio` is an optional field in `prototype_spec`. Agents should
declare it. Values below 0.5 in a math education game require explicit justification.

---

## 4. Win Condition vs. Victory Path

Source: Day 3

These are two separate things that are often conflated:

- **Win condition**: the singular rule that determines success (last player standing, first to 100 points, exact target matched)
- **Victory path**: how a specific player chooses to reach that win condition (aggressive vs. defensive, fast vs. careful)

**Why this matters for the OS:**
- Win condition is set at the spec level — it defines the soul of the game
- Victory path is set at the player level — it defines replayability
- If changing the win condition makes the game feel completely different, the win condition IS the mechanic
- A game that only has one valid victory path has no strategic depth

**OS rule:** `prototype_spec.core_loop_translation.success_condition` must describe the
win condition precisely. A success_condition that implies only one valid path to success
is a design smell worth noting in `open_questions`.

---

## 5. Layered Goals

Source: Day 3

Strong games have goal depth. Three layers:

| Layer | Type | Example |
|-------|------|---------|
| **Primary** | Obvious, required to advance | Match the target exactly |
| **Secondary** | Discovered, improves score | Build a streak; use fewer moves |
| **Hidden / Mastery** | Unlocked through play | Find combinations no one else found |

The OS currently models only the primary goal (success_condition, score). Secondary goals
(streak, efficiency bonus) appear in the scoring logic of some games but are not
captured in the spec schema. Mastery goals are entirely absent.

**OS rule (document now):** Future passes should add secondary goal fields to
`prototype_spec`. The current single `success_condition` field is sufficient for Pass 1
prototypes but will need extension before Pass 2 designs.

---

## 6. Difficulty Curve Types

Source: Day 2, confirmed by Bakery L1 fix

Three curve shapes. Only one is acceptable by default:

| Curve | Shape | What happens | OS verdict |
|-------|-------|--------------|------------|
| **Smooth ramp** | Gradual increase | Player understands before pressure arrives | ✅ Default |
| **Spike** | Sudden cliff | Player quits before understanding | ❌ Gate rejects |
| **Flat** | No increase | Player disengages from boredom | ⚠️ Gate warns |

**Bakery proof case:** Level 1 beltDuration of 5s was a spike — the belt scrolled so fast
that Grade 3 players had no time to read pastry values before being overwhelmed.
Fix: 9s for Level 1 (teaching window), then stepped acceleration across levels 2–5.

**OS rule:** `difficulty_profile.curve_type` is now gated. `spike` triggers revise.
`difficulty_profile.intro_pressure_level = "high"` triggers revise.
Level 1 teaching window under 5s on a teaching/low intro level triggers revise.

---

## 7. The Solvability Rule

Source: Day 2 (constraints), confirmed by Fire Dispatch fix

> **Every generated target must be reachable under the current selection rules.**

This seems obvious but is violated constantly in procedurally generated games because
target generation and rule design are written by different people (or different passes)
with different assumptions.

**Fire Dispatch proof case:**
- Selection rule: fixed-set multi-select, {hose=5, ladder=3, ambulance=2}
- Achievable subset sums: {2, 3, 5, 7, 8, 10}
- Demand range: [4, 8]
- Unsolvable targets in range: 4, 6 — generated randomly, impossible to dispatch

**Fix:** `getSolvableDemands(levelConfig)` enumerates all `2^n − 1` non-empty subset sums,
then `generateIncident` draws only from values in the intersection of achievable sums
and the demand range. O(2^n) where n ≤ 5 — trivial at runtime.

**OS rule:** `interaction_constraints.target_must_be_solvable = false` is now a gate
violation (revise-level). Setting it to false requires overriding the gate with explicit
justification. Games with `route_and_dispatch`, `combine_and_build`, or `allocate_and_balance`
interaction types are required to declare `interaction_constraints`.

---

## 8. The Interaction Constraint Declaration Rule

Source: Fire Dispatch fix, Day 2 (constraints as creative fuel)

A game's selection model must be **declared explicitly** before implementation begins.
The following questions must have answers before any generation logic is written:

| Question | Why it matters |
|----------|----------------|
| Fixed-set or reusable? | Changes which subset sums are achievable |
| One selection or multi-select? | Changes the combinatorics entirely |
| Do selected items disappear? | Determines whether the UI communicates selection state |
| Exact match or threshold? | Changes the scoring and feedback model |
| What happens on overshoot? | Determines the error-recovery path |

**Fire Dispatch lesson:** The original implementation:
- Said "no overshooting allowed" in the start screen
- But kept trucks visible in the yard after selection (implying they were still available)
- And used overshoot prevention (blocked) instead of visual removal

The result: ambiguous selection state, players unsure what "selected" meant.

**Fix:** Fixed-set multi-select + trucks disappear from yard. State is now unambiguous.

**OS rule:** `interaction_constraints` is now a required field for selection-type games in
`prototype_spec`, with gate Dim 8 checking all six sub-fields.

---

## 9. Teaching-First Level Design

Source: Day 2 (difficulty curves), Day 5 (onboarding in the wild), confirmed by both fixes

> "Level 1 should optimize for comprehension before pressure."

This is not a niceness — it is a learning prerequisite. Players cannot learn a mechanic
they are too overwhelmed to observe. Pressure before comprehension produces:
- Random button-mashing (not learning)
- Quitting (not even failure — just exit)
- "This game is broken" (which means the design broke, not the player)

**The 30-second onboarding test (Day 5):**
When a player opens Level 1 for the first time:
1. Can they identify what the goal is without reading instructions?
2. Can they execute their first meaningful action within 30 seconds?
3. Do they understand what happened after that action completes?

If any answer is no, Level 1 needs to be redesigned.

**OS rule:** `difficulty_profile.intro_pressure_level` should be `"teaching"` for all
new games on Pass 1. `"teaching"` means:
- No timer pressure that causes failure
- No motion pressure faster than the player can read
- Maximum 2 simultaneous pressure axes
- At least 5–8 seconds reaction window before the first meaningful time constraint

---

## 10. Feedback Is a Mechanic

Source: Day 7 (feedback systems), Day 1 (6 atoms)

> "What's the most satisfying sound in any game you've played? That's audio feedback doing its job."

Feedback is not decoration. It is a core game mechanic that:
- Communicates whether the player's action succeeded
- Teaches the rule through repetition
- Creates emotional engagement (satisfaction, urgency, curiosity)
- Signals what to do next

**Four feedback dimensions the OS should track:**
| Dimension | What it covers |
|-----------|----------------|
| **Timing** | Immediate vs. delayed (immediate is almost always right for math games) |
| **Channel** | Visual, audio, haptic — which are present? |
| **Clarity** | Is it obvious what the feedback is responding to? |
| **Consequence** | Does the feedback change the game state in a meaningful way? |

**OS rule (document now):** `interaction_model.feedback_timing` already exists in the schema.
A future pass should add `feedback_channels` (visual/audio/haptic array) and
`feedback_clarity_test` (can the player identify what caused the feedback?).

---

## 11. The Designer's Curse

Source: Day 8 (playtesting protocol)

> "You cannot see your own confusing parts."

Game designers cannot playtest their own games fairly because they know the rules.
What feels obvious to the designer is often completely opaque to a first-time player.

**Observable data points during playtesting (Day 8):**
- Where does the tester stop to read rules? → Instruction gap
- Where do they look confused? → Feedback gap
- Where do they laugh? → Surprise/delight signal
- Where do they go quiet? → Challenge or frustration signal

**The 4 feedback categories (Day 8):**

| Category | Definition | Example |
|----------|------------|---------|
| **Bug** | The game behaves incorrectly | Truck adds when it shouldn't |
| **Balance** | The difficulty curve is wrong | Level 1 belt too fast |
| **Confusion** | Player doesn't understand a rule | Player doesn't know they can tap the board to deselect |
| **Fun** | Something is actively unenjoyable | Timer pressure before understanding = not fun, not learning |

**OS rule (document now):** The `playtest_diagnostic_report` schema should eventually
include a `feedback_category` classification on each finding. Currently reports are
unstructured narratives. Adding bug/balance/confusion/fun tags would allow the OS
to route different categories to different revision agents.

---

## 12. Constraints Generate Creativity

Source: Day 2 (Design Jam), Day 5 (field trip retrospective)

> "The most interesting constraint is the weird one. That's actually the best part of your game."

The Design Jam exercise (draw 4 random constraint cards, build a game) consistently
produces better ideas than open-ended brainstorming. Constraints force novel solutions.

**Applied to the OS:**
- The `prototype_scope.excluded` list is a creative constraint — it forces the designer to
  commit to the simplest possible loop
- The `interaction_constraints` block constrains the implementation — and that constraint
  guarantees solvability
- The `core_loop_sentence` constraint forces clarity — and clarity forces simplicity

**OS rule (document now):** When a request_brief comes in with a very open scope,
the intake_brief and kill_report stages should introduce constraints early rather than
letting scope accumulate. Constraint-first design produces better games faster.

---

## 13. The GDD as Living Blueprint

Source: Day 6 (GDD intro), Day 9 (final GDD)

The Game Design Document is not a deliverable — it is a living document that evolves
through every pass. By Day 9 of the camp, students have filled in all 5 sections:
1. Game overview (concept anchor, prototype goal)
2. Mechanics (interaction model, core loop)
3. Goals and win conditions
4. Platform and audience
5. Story and world (concept anchor, theme)

**The key GDD test (Day 6):**
> "Is this YOUR game, or a generic version of your idea? What's missing?"

Claude often produces technically correct but thematically generic output.
The OS should flag when generated content could describe any game rather
than the specific game being designed.

**OS rule (document now):** After Stage 3 (kill_report), if the concept_anchor
`world_theme` and `profession_or_mission` fields could apply to more than 3 other
games in the family, they are probably too generic. Specificity is a design quality signal.

---

## 14. The Onboarding Window Is a Design Invariant

Source: Day 5 (field trip design analysis)

When students analyzed real-world designed experiences (game arcades, parks, buildings)
as design detectives, the most consistent finding was:

> "Onboarding works when the environment itself teaches you what to do — no instructions needed."

**The best games onboard through action, not text:**
- The first visible state shows the player exactly what they can interact with
- The first player action is rewarded immediately and clearly
- The player understands the feedback without explanation

**Applied to the OS:**
- `core_loop_translation.first_visible_state` (already in schema): should describe a state that implies action
- `core_loop_translation.first_player_action` (already in schema): should be obvious from the first_visible_state alone
- The connection between these two should be implicit — if you need an instruction overlay to bridge them, redesign

**OS rule (document now):** A future gate check for `gate_prototype_spec` should ask:
"Does first_visible_state imply first_player_action without a text instruction?" This
is currently a judgment call but could be formalized as a field:
`onboarding_requires_instruction_overlay: boolean`. If true, that's a flag, not a failure.

---

## 15. Bartle's Player Types

Source: Day 6

Four player type archetypes. **Pick at most 2 for any single game.**

| Type | Motivation | What they want | Math game example |
|------|-----------|----------------|-------------------|
| **Achiever** | Progress | Levels, scores, badges | Bakery Rush (score + level advance) |
| **Explorer** | Discovery | Hidden content, secrets | Unit Circle (finding angle patterns) |
| **Socializer** | Connection | Competing/collaborating with others | Not present in current prototypes |
| **Killer** | Dominance | Beating others | Not present in current prototypes |

> "Your target audience is not 'everyone.' The most dangerous phrase in game design."

**OS rule:** `player_type_targets` is now an optional field in `prototype_spec` with a
max of 2 entries. Games that list all 4 types are almost certainly not designing for any
of them specifically.

---

## Summary: New OS Rules Added This Session

| # | Rule | Source | Status |
|---|------|--------|--------|
| R1 | Core loop sentence test | Day 7 | Gate Dim 7 in prototype_spec |
| R2 | Solvability guarantee | Fire Dispatch fix | Gate Dim 8 in prototype_spec |
| R3 | Interaction constraints required for selection games | Fire Dispatch fix | Gate Dim 8 in prototype_spec |
| R4 | Teaching-first Level 1 (spike → revise, high pressure → revise) | Bakery fix + Day 2 | Gate Dim 9 in prototype_spec |
| R5 | Luck/skill ratio declaration | Day 2 | Optional schema field |
| R6 | Player type targets (max 2) | Day 6 | Optional schema field |
| R7 | Win condition ≠ victory path | Day 3 | Document now |
| R8 | Layered goals (primary/secondary/hidden) | Day 3 | Document now, schema in future pass |
| R9 | Feedback is a mechanic (4 dimensions) | Day 7 | Document now, schema in future pass |
| R10 | 4 playtest feedback categories | Day 8 | Document now, diagnostic schema future |
| R11 | Constraints generate creativity (scope first) | Day 2/5 | Document now |
| R12 | GDD specificity test (not generic) | Day 6 | Document now |
| R13 | Onboarding requires no instruction overlay | Day 5 | Document now, flag field future |
| R14 | Designer's Curse (silent playtest protocol) | Day 8 | Document now |
| R15 | Two loop levels (moment-to-moment + session) | Day 7 | Document now |

**Gates added:** Dims 7, 8, 9 in `gate_prototype_spec`
**Schema fields added:** `core_loop_sentence`, `luck_skill_ratio`, `player_type_targets`, `interaction_constraints`, `difficulty_profile`
**Files created:** `docs/game_design_intelligence.md`
**Files updated:** `artifacts/schemas/prototype_spec.schema.json`, `engine/gate_engine.py`, `docs/learning_and_generalization.md`
