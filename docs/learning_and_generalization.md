# Learning and Generalization Operating Document

Use this at the start of every serious build session.

The goal is not just to solve one game problem.
The goal is to make the OS better at producing strong games, strong prototypes, and strong implementation paths over time.

> **New learning captures go in `artifacts/learning_captures/`** — one file per lesson, classified and promotable. The inline living records below are historical and remain for reference.

---

## Core Principle

Do not only solve the local problem.
Also extract what should become reusable inside the OS.

Always work in two layers:
1. Solve the current game problem.
2. Learn from it in a structured way.

---

## What to Optimize For

Optimize for:
- Real game quality
- Learning goals that live inside mechanics
- Clear and satisfying loops
- Implementation efficiency
- Prototype truthfulness
- Future automation
- Reusable architecture

Do not optimize for:
- Feature volume
- Fake completeness
- Premature abstraction
- Cosmetic complexity without loop value

---

## Definition of a Strong Game

A strong game is one where:
- The player understands the goal quickly
- The core action feels meaningful
- The learning objective is inside the mechanic
- Feedback is clear, strong, and useful
- Urgency feels fair
- Failure teaches instead of only punishing
- Progression deepens the original loop
- Implementation remains efficient and testable

Do not confuse more systems with a better game.

---

## Default Way of Working

For every meaningful task, work in this order:

**1. Repo truth**
First confirm what is actually implemented.
Do not assume planned stages are real.
Do not mark anything complete unless it exists in code, is wired into the pipeline, and passes benchmarks.

**2. Local problem solving**
Solve the immediate problem cleanly and within scope.

**3. Structured extraction**
After solving it, extract what the OS should learn from it.

**4. Scope discipline**
Separate what is:
- Reusable across games
- Specific only to the current game
- Too early to generalize

**5. Architectural recommendation**
End with the single most justified improvement to the OS.

---

## Required Post-Task Learning Loop

After each meaningful build, audit, proof case, or debugging step, extract learning in these four layers:

### Layer 1 — Reusable Rules
Identify what worked that should become a reusable rule across future games.

### Layer 2 — Structural Gaps
Identify what was missing in the OS that forced:
- Manual judgment
- Manual code changes
- Ad hoc fixes
- Repeated explanation
- Repeated debugging

### Layer 3 — Architecture Upgrades
For each structural gap, decide whether the right fix is:
- A new schema field
- A stronger gate rule
- A reusable template
- A new agent
- A new tool
- A new benchmark case
- Or documentation only

### Layer 4 — Scope Discipline
Separate:
- What is truly generalizable
- What is specific to the current game
- What is premature to generalize

Then end with:
- The single most justified improvement to the OS
- Why it matters
- Where it belongs in the pipeline
- Whether it should be implemented now, documented now, or deferred

---

## Questions Claude Must Always Answer After Major Work

After every major task, answer these:

1. What here is reusable?
2. What here is still manual?
3. What here should become a system rule?
4. What here should stay local to this game?
5. What is the single best next architectural improvement?

---

## How to Classify Findings

Use only these classifications:
- `acceptable for now`
- `document now`
- `fix now`

---

## When to Recommend a New Agent or Tool

Recommend a new agent or tool only if:
- The same kind of judgment keeps being done manually
- The current artifacts cannot express an important design or implementation condition
- The problem repeats across more than one game or more than one pass
- The new agent would improve both quality and efficiency

Do not recommend a new stage just because it sounds sophisticated.

---

## What Should Become Reusable

**Usually reusable:**
- Loop rules
- Pacing rules
- Attention rules
- Fairness rules
- File coverage rules
- State ownership rules
- Scoring rule patterns
- Animation ownership rules
- Patch sequencing patterns
- Diagnostic frameworks

**Usually not reusable without caution:**
- Exact game copy
- Theme-specific visual details
- One-off names
- Cosmetic gimmicks
- Mechanics that only make sense for one concept
- Highly tuned numerical values before enough evidence exists

---

## How to Judge Whether Something Is Mature Enough to Generalize

Only generalize when at least one of these is true:
- It appears across multiple games
- It appears across multiple passes of the same game
- It repeatedly causes confusion or failure when missing
- It clearly improves both quality and implementation clarity

If it only worked once in one game, do not force it into the architecture yet.

---

## How to Think About Proof Cases

Proof cases exist to teach the OS.

For each proof case:
- Identify what it proves
- Identify what it does not prove
- Identify what it teaches the system
- Identify what still remains accidental or game-specific

Do not treat one strong proof case as full generalization.

---

## Pass Structure Rule

Treat playable passes as meaningful checkpoints.

**Pass 1** should prove: the core loop works at all.

**Pass 2** should prove: pressure, progression, or mechanic deepening works.

**Pass 3** should prove: UI, feedback, and feel upgrades improve the loop without adding product bloat.

Create a new pass only when it answers a clearly different question.
Do not create a new pass for tiny visual drift.

---

## Implementation Discipline

When moving from specs into implementation:
- Prefer explicit file ownership
- Prefer explicit component ownership
- Prefer explicit state ownership
- Prefer explicit animation ownership
- Prefer explicit test targets

Do not accept vague implementation language.

If a later stage depends on an earlier one, verify that the chain is coherent.
Do not accept two stages describing different codebases.

---

## Diagnostic Discipline

If a diagnostic stage exists, be honest about its evidence level.

If the output is based on actual play observation, say that.
If the output is based on inference from structure only, say that.

Do not call structural inference a true playtest if no real play evidence exists.

---

## Revision Discipline

A revision stage should not just sound polished. It should:
- Protect what stays
- Identify what changes
- Explain why
- Keep scope tight
- Route to the correct next pass or tuning move

---

## Default Architecture Preference

Prefer this growth pattern:

```
idea
→ concept evaluation
→ loop definition
→ prototype definition
→ build definition
→ UI behavior definition
→ implementation planning
→ patch planning
→ playable pass
→ diagnostic
→ revision
→ next pass
```

Do not jump from idea straight to final game claims.

---

## How to Prevent Fake Completeness

Always ask:
- Is this real in the repo?
- Is it wired?
- Does it pass?
- Does it produce useful output?
- Does it form a coherent chain with the stage before and after it?

If not, do not call it done.

---

## Standard End-of-Task Output

At the end of every serious task, return:

1. What was solved locally
2. What is now reusable
3. What is still manual
4. What should become: a rule / a gate / a template / an agent / a tool / or documentation only
5. Classification of each finding
6. The single most justified next move

---

## Instruction on Game Quality

Optimize for games that feel:
- Clear
- Alive
- Fair
- Satisfying
- Emotionally readable
- Mechanically honest
- Efficient to implement
- Easy to revise intelligently

Prefer fewer, sharper mechanics when they produce stronger play.

Do not mistake more screens, more systems, or more polish language for a better game.

---

## Final Rule

Whenever solving a problem, do not only ask:
**"How do we fix this game?"**

Also ask:
**"What should the OS learn from this so future games are better, faster to build, and more truthful?"**

---

## Living Record: What Three Games Taught Stage 9→10

*Last updated: 2026-04-04. Append lessons after each new proof case.*

### What remained reusable across all three games (Bakery, Fire Dispatch, Unit Circle)

**Architecture (fully generic — no changes needed per game):**
- `SharedAgentRunner` wiring (`build_spec`, `run`) — identical across all agents
- Gate dims 1–6 in `gate_implementation_patch_plan` — validated correctly for all three
- `implementation_plan_files` injection and gate coverage check — game-agnostic
- `target_files` derivation from `implementation_plan.file_plan` — worked for all three
- Stage 9 concept routing via `prototype_spec.concept_anchor.primary_interaction_type`
- Stage 10 concept routing via file path matching ("bakery", "fire", "unitcircle" in paths)
- The `CONCEPT_OVERRIDES` dict pattern — scales cleanly to N games

**Structure (same shape, different content):**
- One root container component that owns all game state
- 4–6 presentational child components that receive props and emit callbacks
- One data config file (levelConfig / missionConfig / labConfig)
- One styles file with keyframes
- App.jsx as the entry mount updated last
- Patch sequence always: data config → styles → keyframes → leaf components → root → App

**State shape (parallel across games):**
- `feedbackMode` (null or named state) — identical pattern in all three
- `score`, `streak`, `levelIndex` (or equivalent) — present in all three
- A timer or patience variable — present in Bakery and Fire, absent in Unit Circle
- A `sessionComplete` or equivalent end state — present in all three
- Single state owner, props-down / callbacks-up — enforced in all three

**Animation shape (parallel):**
- One rejection/incorrect animation (shake or bounce-back)
- One success or overlay entry animation
- One urgency signal (patience bar, timer pulse, or topping pop)

**Acceptance signals (same count, parallel structure):**
- All three games produced exactly 6 signals organized around: item interaction, total update, success, failure, timer/patience, progression signal

---

### What had to be hand-authored differently each time

| Concern | Bakery | Fire Dispatch | Unit Circle |
|---|---|---|---|
| Interaction model | Tap single item, accumulate | Tap multiple items, confirm dispatch | Click position, confirm submit |
| Core mechanic | Running total vs target | Running capacity sum vs demand | Angular position within tolerance |
| Feedback on error | Bounce-back (auto remove last item) | Shake + keep selection (player corrects) | Ghost reveal + coordinate display |
| Timer model | Patience per customer | Countdown per incident | No timer (no time pressure) |
| Data config shape | levelConfigs + pastryValueMap | LEVEL_CONFIGS + TRUCK_TYPES | ROUND_CONFIGS + COMMON_ANGLES |
| SVG requirements | None | None | Required (unit circle is SVG) |
| Math rendering | Integer arithmetic | Integer arithmetic | Trig fractions + decimals |
| Progression model | Score threshold → level up | Score threshold → level up | Linear round sequence |
| Exact-value lookup | Not needed | Not needed | Required (COMMON_ANGLES) |
| Component count | 6 | 5 | 6 |
| Naming registry size | 88 entries | 69 entries | 61 entries |

Every `patch_sequence` entry, every `naming_registry` entry, every `animation_contract`, and every `acceptance_signal` was authored by hand. These cannot be derived from structure alone without an LLM.

---

### What repeated enough to justify a template layer (when three or more games exist)

**Patch sequence skeleton** — the ordering pattern is identical:
```
P1-01: data config file — add primary data constant
P1-02: data config file — add secondary data constant
P1-03: styles file — add all CSS classes
P1-04: styles file — add keyframes
P1-05..P1-N: leaf components (N=4–6)
P1-(N+1): root container
P1-(N+2): App.jsx mount
```
This ordering pattern could become a `PatchSequenceTemplate` that pre-populates patch_ids, file paths, and `depends_on` chains from the `file_plan`. The `change_description` and `named_elements` would still require authoring.

**Naming registry shape** — entries follow predictable type patterns per component:
- Root container: N state_variables + N callbacks + N constants
- Leaf components: N props (matching the component_plan.inputs)
- Styles file: N css_classes + N keyframes + optional css_custom_properties
A registry generator that walks `component_plan` and `state_plan` could produce 60–80% of registry entries automatically.

**Acceptance signal structure** — all three games produced signals in this order:
1. Core interaction observed in browser
2. Running total / value update visible
3. Correct answer feedback
4. Incorrect answer feedback
5. Timer / urgency / patience visible
6. Progression visible
This is a generalizable `AcceptanceSignalTemplate` with 6 slots mapped to interaction_type.

**Animation contract structure** — all three games had:
- One rejection/error animation (shake or bounce)
- One success/overlay entry animation
- One urgency or placement animation
This is a 3-slot `AnimationContractTemplate` that could be pre-populated from `animation_plan` entries.

---

### What Stage 10 needs to support template-driven or LLM-generated output

**Already in place:**
- Gate validates all correctness conditions (file coverage, naming registry, dependency graph, animation contracts, acceptance signals, implementation_plan alignment)
- Schema is strict enough to reject incomplete output
- Routing pattern (`CONCEPT_OVERRIDES`) is stable and extends cleanly
- `implementation_plan_files` field closes the Stage 9→10 chain gap

**What is still missing for template-driven generation:**
1. A `PatchSequenceTemplate` that can generate the skeleton (patch_ids, file paths, ordering) from `file_plan` — the change descriptions would still need authoring
2. A way for the template to consume `component_plan.inputs` to generate `prop:` entries in the naming registry automatically
3. A way for the template to consume `state_plan.local_state` to generate `state_variable:` registry entries automatically

**What is still missing for LLM-generated output:**
1. The gate already validates the output — LLM generation is architecturally ready
2. What is needed: a well-structured prompt that passes `implementation_plan.file_plan`, `component_plan`, `state_plan`, and `animation_plan` as structured inputs, and instructs the LLM to produce a patch_sequence that the gate can validate
3. The gate is the safety net — LLM generation can fail and the gate will catch it

**Single most justified next improvement:**
Add a `PatchSequenceTemplate` that auto-generates the skeleton from `file_plan` (patch IDs, file paths, ordered phases, App.jsx last). This would reduce hand-authoring from ~300 lines per game to ~50 lines of `change_description` and `named_elements` content. The gate already handles validation. This is the highest-leverage move before attempting LLM generation.

**Classification:** `document now` — the pattern is clear and consistent across three games. Implementation requires one more game to confirm the pattern holds before committing to the template structure.

---

## Living Record: What the GameForge Facilitator Curriculum Taught the OS

*Added: 2026-04-04. Source: GameForge 10-Day Facilitator Guides, Days 1–10.*
*See full extracted intelligence in: `docs/game_design_intelligence.md`*

### New schema fields added to prototype_spec

| Field | Type | Purpose | Gate? |
|-------|------|---------|-------|
| `core_loop_sentence` | string (1 sentence) | Forces loop clarity before build | Yes — Dim 7 revise if absent |
| `interaction_constraints` | object | Declares selection rule, solvability, disappear behavior | Yes — Dim 8 required for selection games |
| `difficulty_profile` | object | Declares curve type, intro pressure, pressure axes, teaching window | Yes — Dim 9 revises spike/high/short-window |
| `luck_skill_ratio` | float 0–1 | Explicit skill vs luck declaration | No gate yet |
| `player_type_targets` | string[] max 2 | Bartle types — forces design specificity | No gate yet |

### New gate checks added (gate_prototype_spec)

**Dim 7 — Core loop sentence:**
Revise if `core_loop_sentence` is absent. A loop that cannot be stated in one sentence is not clear enough to build.

**Dim 8 — Interaction constraints:**
- Revise if `interaction_constraints` is absent for `route_and_dispatch`, `combine_and_build`, or `allocate_and_balance` games
- Revise if `target_must_be_solvable` is `false` (fundamental game logic failure)
- Revise if `selection_rule = fixed_set_multi_select` but `selected_items_disappear = false` (selection state ambiguity)

**Dim 9 — Difficulty profile teaching-first:**
- Revise if `curve_type = "spike"` (players quit before understanding)
- Revise if `intro_pressure_level = "high"` (pressure before comprehension blocks learning)
- Revise if ≥3 pressure axes stack on a teaching/low intro level
- Revise if `level_1_teaching_window_seconds < 5` on a teaching/low intro level

### Reusable rules confirmed across Bakery + Fire Dispatch proof cases

**Solvability rule (fix_now — implemented):**
> Every generated target must be reachable under the current selection rules.
>
> Implementation: enumerate all 2^n non-empty subset sums → filter to demand range → draw from intersection.
> Applies to: any `route_and_dispatch`, `combine_and_build`, or `allocate_and_balance` game.

**Teaching-first rule (fix_now — implemented):**
> Level 1 must optimize for comprehension before pressure.
> Speed, motion, and time constraints should arrive after the player has understood the loop.
> Level 1 pacing parameters are teaching parameters, not difficulty parameters.

**Interaction constraint declaration rule (fix_now — implemented):**
> The selection model must be declared before implementation begins.
> Ambiguous selection state (items stay visible but "selected") produces confused players.
> Fixed-set multi-select → items disappear from option pool. No exceptions.

### Rules documented for future passes (not yet gated)

**Win condition ≠ victory path:** The win condition defines the soul of the game.
Changing the win condition changes the game more than changing any mechanic.
The OS should distinguish these at the spec level.

**Layered goals (primary/secondary/hidden):** Current `success_condition` covers primary only.
Secondary goals (streak, efficiency) exist in game code but are not captured in the spec schema.
Future pass: add `secondary_goal` and `mastery_goal` fields to `prototype_spec`.

**Feedback as mechanic (4 dimensions: timing/channel/clarity/consequence):**
`interaction_model.feedback_timing` exists. `feedback_channels` and `feedback_clarity_test` are missing.
Future pass: add these to `interaction_model`.

**Playtest feedback categories (bug/balance/confusion/fun):**
`playtest_diagnostic_report` should categorize findings by type.
Currently unstructured narrative. Future pass: add `finding_category` field to each finding.

**Designer's Curse (silent playtest protocol):**
The designer cannot see their own confusing parts. Playtest protocol: designer silent, tester thinks aloud.
The OS should encode this as a required protocol in any playtest_diagnostic instructions.

**Two loop levels (moment-to-moment + session):**
Current `core_loop_translation` captures only the moment-to-moment loop.
Session loop (what keeps a player for 20–30 min) needs a separate field.
Future pass: add `session_loop_description` to `prototype_spec`.

**Onboarding requires no instruction overlay:**
`first_visible_state` should imply `first_player_action` without text instructions.
Future pass: add `onboarding_requires_instruction_overlay: boolean` as a flag field.

### Classification summary

| Finding | Classification |
|---------|---------------|
| Solvability rule | `fix_now` — implemented in getSolvableDemands + gate Dim 8 |
| Teaching-first rule | `fix_now` — implemented in beltDuration fix + gate Dim 9 |
| Interaction constraint declaration | `fix_now` — implemented in interaction_constraints schema + gate Dim 8 |
| Core loop sentence test | `fix_now` — implemented in gate Dim 7 |
| Win condition vs. victory path | `document now` |
| Layered goals | `document now` — schema field deferred to Pass 2 |
| Feedback dimensions | `document now` — schema field deferred to Pass 2 |
| Playtest feedback categories | `document now` — schema field deferred when diagnostic agent is written |
| Designer's Curse protocol | `document now` |
| Two loop levels | `document now` — session_loop field deferred to Pass 2 |
| Onboarding overlay flag | `document now` — field deferred to next prototype_spec revision |
| Luck/skill ratio | `acceptable for now` — field added, gate deferred |
| Player type targets | `acceptable for now` — field added, gate deferred |

### Single most justified next improvement

Add `solvability_auditor` as a standalone utility (not a full agent) that the implementation
plan stub can call during generation. It takes `available_options: [{id, value}]` and
`target_range: [lo, hi]` and returns `solvable_targets: number[]`. This encapsulates the
`getSolvableDemands` pattern already proven in Fire Dispatch into a reusable helper that
any future game with discrete selection can import. The pattern is now confirmed across
Bakery (trivially solvable — any combo of any value works) and Fire Dispatch (non-trivially
solvable — subset sum of fixed options). The helper would have caught the Fire Dispatch
bug before Pass 1 was ever built.


---

## Proof-Case Review Session — 2026-04-04

Source: improvements made to all three pass-1 previews based on direct playthrough of the live HTML files.

### Rules extracted

**Rule: Every visible element in a game UI must have mechanical consequence, or be removed.**

Not cosmetic tolerance — removed. Flavor is permitted (character names, incident locations, bakery theme). But any label that describes a game state or attribute — urgency levels, priority badges, status indicators — implies a mechanical difference to the player. If the system does not back that difference with behavior, the label is a lie. Urgency in Fire Dispatch was showing 🔴 HIGH / 🟢 LOW with identical point values and identical time limits. Fix: HIGH = 1.5×, MED = 1.0×, LOW = 0.8× points. Four lines. This rule applies at proof-case review, before any gate stage.

**Rule: Every state transition that penalizes the player requires a visible feedback window.**

If the player loses something (a life, a customer, time), the game must show *why* for long enough to perceive. 900ms minimum. The Bakery patience timer expired silently — the UI reset instantly with no indication that a customer had left as a penalty. A learner has no way to connect the patience bar emptying to the customer disappearing without a bridging moment. This is not polish. It is the cause-and-effect chain that teaching depends on.

**Rule: Feedback language implies a contract with the player.**

If feedback text contains an action verb the player can take ("Try again", "Retry", "Continue"), the system must support that action in the current state. If it does not, cut the verb. Unit Circle showed "Close! Try again." while auto-advancing after 1800ms with no retry mechanism. This is worse than silence — it sets an expectation, then violates it. Fix: either remove the verb or implement the action. The retry system was implemented.

**Rule (implementation discipline): Avoid nested cross-state updater logic when simpler sequencing is possible.**

Using `setScore(prevScore => { setLevelIndex(...); })` — reading one piece of state inside another state's updater to drive a third update — is technically valid React but produces silent correctness bugs under batching. The Fire Dispatch level-advancement check used `prevScore + pts >= threshold` inside such a nesting, which double-counted `pts` because `prevScore` was already post-update. The correct fix is to compute the outcome first, then apply it, or to use a `useEffect` that watches the score. The bug was subtle enough to ship in a playable preview and survive code review.

**Rule (teaching principle): Make cause-and-effect explicit at every state change in teaching games.**

This generalizes the patience feedback and the urgency badge rules. A learner builds a mental model of how a game works by observing what happens when they act or fail to act. Every state change that has a consequence — a penalty, a reward, a difficulty increase — needs a perceivable moment that names what happened. Silent transitions teach nothing. Instant transitions teach the wrong thing.

### Patterns documented for future use

**Retry-state machine (precision games):**
Three states: `null → 'offered' → 'active'`. First close result pauses the round and offers retry. Ghost position stays visible during 'offered' and 'active' states as a placement guide. Second attempt always auto-advances. This pattern is local to Unit Circle now but is portable to any game where spatial or temporal precision is the core challenge. Extract when a second precision game needs it.

**pass_record artifact:**
A lightweight JSON artifact written at the end of each pass. Shape: `pass_name`, `game_name`, `pass_number`, `timestamp`, `what_this_pass_proved`, `open_questions`, `bugs_fixed` (with `impact` dimension), `known_limits`, optional `auditor_results`, and `next_pass_first_obligation`. Schema at `artifacts/schemas/pass_record.schema.json`. This is an evidence bridge between passes — makes Pass N+1 start from proof rather than memory. Not a new pipeline stage.

### Classification

| Finding | Classification |
|---------|---------------|
| Visible labels must have mechanical consequence | `fix_now` — applied to urgency in Fire Dispatch |
| Penalty transitions need feedback windows | `fix_now` — applied to customer_left in Bakery |
| Feedback language implies contract | `fix_now` — applied to "Try again" in Unit Circle |
| Nested cross-state updater risk | `fix_now` — applied to level advancement bug in Fire Dispatch |
| Retry-state pattern | `document_now` — local to Unit Circle; extract when second precision game needs it |
| pass_record schema | `fix_now` — schema written; actual pass records to be created at start of Pass 2 |

### Single most justified next architectural improvement

Define and write the three `pass_record` artifacts (one per game, one per pass) before beginning Pass 2 on any of them. This costs one short document per game and makes the OS's understanding of each game's current state explicit and queryable, rather than reconstructed from commit history each session.

---

## OS 2026 Revision — 2026-04-04

The OS operating principle was upgraded from:

> Role + interaction + pressure + points

to:

> Role + interaction + misconception detection + adaptive feedback + reflection + transfer

This is not a cosmetic rename. It reflects what the three proof-case games already revealed:
- The difficulty ramp auditor proved that pressure without diagnosis is incomplete
- The pass record artifacts proved that honest documentation of what was proved vs. assumed matters
- The retry-state machine in Unit Circle proved that adaptation (even one-shot) changes the learning outcome

### New operating principle grounding

The upgrade is grounded in:
- EEF metacognition guidance: plan → monitor → evaluate as high-value classroom moves
- IES formative assessment framing: gather and use evidence during learning, not only at the end
- Current platform ecosystems (Games for Change, Code.org, Minecraft Education, Roblox Education, ISTE): all reward creation, standards alignment, and educator usability — not shallow point-chasing

### What changed structurally

| Change | Location | Status |
|---|---|---|
| Full OS spec | `docs/os_spec_2026.md` | Written |
| Ninth required layer (Thinking) | `prototype_spec.schema.json` → `thinking_layer` | Schema added |
| Six required error categories | `prototype_spec.schema.json` → `learning_design.error_category_map` | Schema added |
| Reflection beat requirement | `prototype_spec.schema.json` → `learning_design.reflection_prompt_plan` | Schema added |
| Adaptation design layer | `prototype_spec.schema.json` → `adaptation_design` | Schema added |
| Challenge vs. adaptation levers (separate) | `prototype_spec.schema.json` → `difficulty_and_adaptation_levers` | Schema added |
| Transfer target (required) | `prototype_spec.schema.json` → `transfer_target` | Schema added |
| Teacher evidence (required) | `prototype_spec.schema.json` → `teacher_dashboard_outputs` | Schema added |
| Ten approval gates | `prototype_spec.schema.json` → `approval_gates_2026` | Schema added |
| Learning skills (metacognitive) | `prototype_spec.schema.json` → `target_player.learning_skills` | Schema added |
| Misconception Library — Bakery Rush | `artifacts/misconception_library/bakery-rush-misconceptions.json` | Written |
| Misconception Library — Fire Dispatch | `artifacts/misconception_library/fire-dispatch-misconceptions.json` | Written |
| Misconception Library — Unit Circle | `artifacts/misconception_library/unit-circle-misconceptions.json` | Written |
| Misconception Library schema | `artifacts/schemas/misconception_library_entry.schema.json` | Written |
| Loop Purity Auditor | `utils/loop_purity_auditor.py` | Written |
| Teacher Evidence Dashboard schema | `artifacts/schemas/teacher_evidence_dashboard.schema.json` | Written |

### Reusable rules from this revision

**Rule: Challenge levers and adaptation levers are not the same axis.**
The original OS treated difficulty as one dial (harder/easier). The 2026 revision separates making the game harder (challenge levers) from responding to confusion (adaptation levers). A game can be at L3 difficulty and still offer a simplified-representation adaptation. These are independent.

**Rule: Misconception classification is the minimum evidence threshold.**
Right/wrong is not enough. The OS now requires every game to classify error events into at least 3 of 6 categories. This is what separates diagnostic games from scoring games.

**Rule: The Thinking Layer is the missing design piece.**
The strongest games already implicitly define what to notice, predict, monitor, and revise. Making it explicit as Layer 9 prevents loops that are mechanically correct but cognitively opaque — loops where the player acts correctly without understanding why.

**Rule: Teacher evidence is not an add-on.**
Approval Gate 7 now makes teacher interpretability a first-class requirement. A game that cannot surface confused students within 60 seconds is not classroom-ready regardless of how good the loop is.

### What remains out of scope (not changed by this revision)

- The pipeline stages 0–8 are unchanged in their gate logic
- The V2 boundary document is superseded by the new approval gates where they conflict
- The ten new agents are defined as interface contracts only — implementation follows priority build order
- Platform integrations (Minecraft Education, Roblox Education, Bloxels, etc.) are named in the routing spec but not wired to any existing stage
- Subtraction mechanic in Bakery Rush remains a possible future experiment, not a decided extension
