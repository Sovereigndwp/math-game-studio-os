# V2 Boundary Definition

**Status:** Proposed — not yet started.
**Prerequisite:** V1 frozen at tag `v1.0`.

---

## Purpose

V1 proves that a concept is worth building.
V2 proves that the concept is buildable.

V2 converts an approved `lowest_viable_loop_brief` into a precise, testable
prototype plan that a designer, developer, or small team could implement without
guessing. The output is a prototype-ready build specification — not a full game,
not a polished product.

**V1 question:** Is this concept worth building?
**V2 question:** Can we specify a tight prototype for this concept without losing
what made it strong?

---

## First Artifact

**`prototype_spec`**

The bridge between concept validation and actual playable implementation. V1 tells
you what the game is, who it is for, what interaction drives it, what family it
belongs to, and what the smallest strong loop is. It does not yet tell a builder
what appears on screen, what the player can do, what counts as success or failure,
what state changes happen, what must be built first, or what can be deferred.

`prototype_spec` solves that gap. It contains:

### 1. Prototype Goal
What this prototype is trying to prove. Examples: Can children understand the loop
in under 20 seconds? Does the interaction actually teach the intended skill? Is the
signature moment satisfying enough to replay?

### 2. Player Experience Scope
What the prototype includes and what it explicitly excludes.

### 3. Core Interaction Implementation
Exactly how the player performs the main action — the mechanical translation of the
V1 interaction type into concrete player behavior.

### 4. Screen and State Definition
What appears on load, during play, on success, on failure, and on reset.

### 5. Input Model
What the player can do: tap, drag, select, type, confirm.

### 6. Feedback Model
What feedback is given: visual, audio, score, correction, bounce-back, reset, hint.

### 7. Success and Fail Conditions
What counts as a correct loop, a failed loop, a retry, and a finished session.

### 8. Prototype Boundaries
What is intentionally omitted: polish, progression map, advanced difficulty scaling,
content breadth, account systems, analytics.

### 9. Test Plan
What should be observed when someone plays it — learner observation points, teacher
observation points, and what should be measured qualitatively.

### 10. Build Priority
What must be built first vs. later.

---

## Gate Criteria

The `prototype_spec` gate is stricter than V1 but still focused. A V2 artifact
passes only if all seven conditions are met:

| # | Criterion | Fail action |
|---|---|---|
| 1 | **Build clarity.** A developer could implement the prototype without inventing major missing pieces. | revise |
| 2 | **Interaction fidelity.** The build spec preserves the exact interaction logic approved in V1. | reject |
| 3 | **Loop integrity.** The prototype still represents the approved smallest meaningful loop — no additions, no reductions. | reject |
| 4 | **Scope discipline.** The prototype is narrow enough to build quickly and test honestly. | revise |
| 5 | **Testability.** The spec includes a clear test question or learning hypothesis. | revise |
| 6 | **Deferral discipline.** The spec clearly separates: required now, nice later, and explicitly out of scope. | revise |
| 7 | **No mechanic drift.** The prototype does not quietly mutate the concept into a different game. | reject |

Interaction fidelity, loop integrity, and mechanic drift violations produce
`reject` (fundamental identity compromise). Build clarity, scope discipline,
testability, and deferral discipline gaps produce `revise` (fixable).

---

## Stop Condition

V2 is complete when an approved concept has a prototype-ready specification
detailed enough for implementation, but not yet implemented as a product.

In practical terms, V2 ends when:
- The Prototype Spec Agent is implemented in both stub and LLM modes.
- The `prototype_spec` schema is defined in `artifacts/schemas/`.
- The gate is integrated into the pipeline as Stage 6.
- `prototype_spec` passes its gate for at least one approved concept.
- The core loop is fully specified for building.
- Test goals are explicit.
- Build scope is constrained.
- Open product questions are separated from prototype requirements.
- Benchmark cases cover: (a) an approved concept producing a valid spec,
  (b) a spec that drifts from the approved interaction being rejected,
  (c) a spec with insufficient build clarity being sent back for revision.
- All existing V1 benchmarks still pass (regression).
- Revision-path and stall-path benchmarks added (V1 known limitations).

---

## What Belongs in V2

### Concept-to-build translation
- Prototype goal and success hypothesis
- Interaction implementation details (from V1 interaction type to concrete player actions)
- Screen and state flow
- Input model
- Feedback model
- Fail state model
- Session boundary

### Build readiness
- Exact prototype scope
- Required assets list
- Required UI elements
- Minimal content needed
- Build priority order

### Testing readiness
- Success hypothesis
- Learner observation points
- Teacher observation points
- What should be measured qualitatively

### Constraint handling
- What is deferred
- What is omitted
- What must not expand

### Pipeline infrastructure
- Revision-path benchmark case (V1 known limitation)
- Stall-path benchmark case (V1 known limitation)
- Benchmark expansion to 7+ cases (new stage + revision + stall paths)

---

## What Does NOT Belong in V2

| Item | Why excluded |
|---|---|
| **Full production build** | No polished game build. V2 produces specs, not products. |
| **Full progression system** | No complete multi-level progression architecture unless needed for prototype proof. Difficulty scaling beyond the prototype scope is V3+. |
| **Monetization systems** | No subscriptions, pricing, checkout, or platform packaging. |
| **Full curriculum expansion** | No broad content library. Prototype uses minimal content to test the loop. |
| **Final art direction** | No expensive asset development beyond what is needed to test the loop. |
| **Analytics stack** | No post-launch metrics system. |
| **Teacher dashboard or parent platform** | Not yet. |
| **Large-scale engine refactoring** | V2 proves a prototype path, not a rebuilt architecture. |
| **Multiple concepts at once** | V2 focuses on one prototype candidate at a time. |
| **Consumer UI or API server** | Pipeline remains CLI-only through V2. |
| **New interaction types or factory types** | V2 uses the existing V1 taxonomy. |

---

## Connection to V1 Benchmark Review

The `prototype_spec` artifact absorbs the build-adjacent open items from
`docs/benchmark_review_v1.md § Post-Review Open Items`:

| V1 Open Item | V2 Resolution |
|---|---|
| Bakery: quantity representation mode | Resolved in screen/state definition and interaction implementation |
| Fire Dispatch: supply mechanic loop spec | Deferred — prototype scope covers primary dispatch loop only; supply mechanic is explicitly out of prototype scope |
| Fire Dispatch: demand/capacity labeling | Resolved in input model and feedback model (how the player distinguishes demand from capacity on screen) |
| Unit Circle: non-axis angle pairing | Resolved in session boundary constraints within test plan |
| Unit Circle: acceptance zone tuning | Resolved in success/fail conditions (what radius tolerance counts as correct placement) |

V2 resolves 4 of 5 open items within the prototype scope. The Fire Dispatch supply
mechanic remains deferred — it is a second-loop concern, not a prototype concern.

---

## First V2 Candidate

### Bakery (bench_01)

**Why first:**
- Strongest overall V1 score (24/24) — no constraining dimension
- Cleanest interaction purity (0.93)
- No open design questions at the loop level
- Widest addressable market (K–2 addition)
- Simplest path to prototype without ambiguity

### Second: Fire Dispatch (bench_02)

- Near prototype-ready at the primary loop level
- Needs clearer mechanic boundary (supply mechanic deferred from prototype)

### Third: Unit Circle Pizza Lab (bench_03)

- Strongest educationally
- Needs confirmed institutional sales channel before build investment is justified

---

## Known Limitations

### Cross-validation of fidelity claims against input artifacts

The `prototype_spec` gate validates the agent's self-reported
`concept_fidelity_check` (three booleans and fidelity notes). However, the gate
currently only receives the output artifact — it does not have access to the
upstream V1 artifacts (`interaction_decision_memo`, `family_architecture_brief`,
`lowest_viable_loop_brief`).

This means the gate can verify that fidelity fields are present, non-empty, and
internally consistent, but it cannot independently confirm that the agent's
fidelity claims are *true* by comparing against the actual V1 values.

**Implication:** If the agent falsely claims `v1_interaction_type_preserved: true`
while actually drifting from the approved interaction, the gate will not catch
this. In stub mode this is mitigated by deterministic templates. In LLM mode it
is a real risk.

**Resolution path:** Expanding the gate interface to accept input artifacts
alongside the output artifact would enable true cross-validation. This is an
architectural change to the gate engine that affects all stages and is out of
scope for V2. It should be addressed when the gate architecture is revisited
(likely V3+).

**Current mitigation:** The agent prompt explicitly instructs the LLM to set
fidelity claims honestly and warns that claims are audited. The gate validates
that `fidelity_notes` contains a non-empty explanation, creating a paper trail
even when cross-validation is not automated.

---

## Recommended V1→V2 Sequencing

1. **Build the Prototype Spec Agent** with Bakery as the first test case.
2. **Run Bakery through the full V1+V2 pipeline.** First concept to receive a
   `prototype_spec`. Use it to validate the gate criteria and tune the agent.
3. **Apply to Fire Dispatch** once the agent is stable. Prototype spec covers
   primary dispatch loop only; supply mechanic is explicitly deferred.
4. **Hold Unit Circle** at V1 concept level until institutional sales channel
   is confirmed.
