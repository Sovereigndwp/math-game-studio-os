# Learning and Generalization Operating Document

Use this at the start of every serious build session.

The goal is not just to solve one game problem.
The goal is to make the OS better at producing strong games, strong prototypes, and strong implementation paths over time.

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
