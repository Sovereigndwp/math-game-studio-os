# Concept Lanes

This file tracks concepts that are in active pipeline stages. It is the
repo-native source of truth for which concepts are currently being worked
on, what stage each one is in, and which agent owns the next step.

It is deliberately lightweight. If a concept needs more detail, link out
to its concept source of truth under `concepts/<concept-slug>/`.

## What a lane entry is — and is not

A lane entry records the **approval and ownership state** of a concept as
it moves through the pipeline. It is **not**, by itself, evidence of any
of the following:

- build validation (a working preview prototype has been implemented)
- playtest validation (the concept has been tested with real learners)
- curricular coverage proof (a standard has been demonstrably taught)
- Delight Gate full pass (only conditional passes may be noted)
- Game Design Critic P1 pass record review

If a concept's build state is anything less than "prototype built and
playtested," the lane entry is a promise of future work, not a record of
completed work. Do not cite a lane entry as evidence that a family,
interaction type, or standard has been proven in the portfolio.

## Field conventions

Lane entries follow conservative field policies that match the family registry at [`memory/registries/family_registry.json`](../memory/registries/family_registry.json):

- **`null` on a field** means the repo contains no formal documentation backing that claim. It does NOT mean "not applicable" — it means "no formal source exists yet." Informal claims from README benchmark tables, in-file header comments, or `docs/concept_inputs/` strategy files do not qualify as formal sources.
- **"Pending Formal Family Placement"** as a Family value means the game lives in the pseudo-family holding area in the family registry, not in a real family. It is a structural placeholder, not a family assignment.
- **`pending_taxonomy_placement`** as an Interaction type means the game's core act does not cleanly match any entry in [`orchestrator_v3/policies/interaction_types.yaml`](../orchestrator_v3/policies/interaction_types.yaml). Requires a formal taxonomy extension before a real value can be assigned.
- **`release_state: never_shipped`** means no entry exists in `games/<slug>/releases/`. This is the current state for every game in the repo. Nothing has shipped yet.
- **No `concepts/<slug>/` folder** is the default state for existing games. Only Snack Line Shuffle has a formal concept packet.

See [`memory/registries/family_registry.json`](../memory/registries/family_registry.json) for the structured (machine-readable) version of the same information.

---

## Active concepts

### Bakery Rush

> ⚠ **Validation status: active review build — no formal concept packet, no formal alignment, not shipped.**
> A working review build exists at `reviews/bakery/current/index.html` with four pass records in `artifacts/pass_records/`. Misconception library entries exist. **No `concepts/bakery/` packet exists**, so the curriculum alignment and grade band are informal (benchmark-case language only). **No release has been cut**. This lane entry records the presence of an active development build — it must not be cited as evidence of ship-ready status, formal curricular coverage, or approved grade-band lock.

- **Slug:** `bakery`
- **Display title:** Bakery Rush
- **Concept source of truth:** none (`concepts/bakery/` does not exist)
- **Informal concept source:** [`docs/concept_inputs/top_5_math_concepts_claude_packet.md`](concept_inputs/top_5_math_concepts_claude_packet.md), [`docs/concept_inputs/brain_games_concept_library_by_subject.md`](concept_inputs/brain_games_concept_library_by_subject.md)
- **Family:** Quantity and Fulfillment *(documented in [`docs/concept_inputs/strategy/family_map_math.md`](concept_inputs/strategy/family_map_math.md) Family 1)*
- **Interaction type:** `combine_and_build` *(listed under `example_games` in [`orchestrator_v3/policies/interaction_types.yaml`](../orchestrator_v3/policies/interaction_types.yaml))*
- **Primary standard:** `null` — no formal alignment packet. Benchmark-case language in the README refers to "addition within 20" but that is not a formal CCSS alignment.
- **Grade band:** `null` — no formal lock. Benchmark-case language refers to "K–2" but that is not a formal packet.
- **Current stage:** Active review build
- **Build state:** `reviews/bakery/current/index.html` exists; also `pass-3.html` historical snapshot
- **Playtest state:** At least one documented playtest verification at [`artifacts/playtests/bakery-rush/2026-04-05-p3-verification.md`](../artifacts/playtests/bakery-rush/2026-04-05-p3-verification.md)
- **Pass records:** [`artifacts/pass_records/`](../artifacts/pass_records/) — `bakery-rush-pass-1.json`, `bakery-rush-pass-2.json`, `bakery-rush-pass-2a.json`, `bakery-rush-pass-3.json`
- **Misconception linkage:** [`artifacts/misconception_library/bakery-rush-misconceptions.json`](../artifacts/misconception_library/bakery-rush-misconceptions.json) — 6 game-specific entries tagged to canonical categories
- **Intended release path:** `games/bakery/releases/<version>/index.html` *(none exist; not yet shipped)*
- **Release state:** `never_shipped`
- **Next agent:** None currently assigned. Ship-ready gate has not been scheduled in Taskade.
- **Current blocker for shipping:** No ship-ready gate has been run. No `concepts/bakery/` packet exists. No formal P1 Definition of Done has been checked.
- **Family registry entry:** `Quantity and Fulfillment` → `Bakery Rush` in [`memory/registries/family_registry.json`](../memory/registries/family_registry.json)

### Echo Heist

> ⚠ **Validation status: active review build — hybrid game, no formal packet, no canonical taxonomy fit, not shipped.**
> A working review build exists at `reviews/echo-heist/current/index.html` with five in-place pass records (Pass 1 through Pass 5). **No `concepts/echo-heist/` packet exists**. The interaction type does not cleanly match any entry in the canonical taxonomy — it is a hybrid stealth-strategy game with a math subloop that is single-expression compute-and-answer. **No misconception library entries exist**. **No release has been cut**. This lane entry records the presence of an active development build only.

- **Slug:** `echo-heist`
- **Display title:** Echo Heist
- **Concept source of truth:** none (`concepts/echo-heist/` does not exist)
- **Informal concept source:** [`docs/concept_inputs/Echo Heist Game Concept.md`](concept_inputs/Echo Heist Game Concept.md) (1750 lines, ChatGPT export). A duplicate partial export lives at `reviews/echo-heist/current/Echo Heist Game Concept.md` (1407 lines) — tracked as cleanup follow-up (Cleanup Step 2, not yet done).
- **Family:** Pending Formal Family Placement *(pseudo-family — no documented family fits this concept; see [`memory/registries/family_registry.json`](../memory/registries/family_registry.json))*
- **Interaction type:** `pending_taxonomy_placement` — hybrid game; the math subloop (single-expression compute-and-answer) is not represented in the canonical taxonomy
- **Primary standard:** `null` — no formal alignment packet. Multi-topic content across districts 1–3 (addition, subtraction, rounding, percents, fractions, rates, expected value); no single-standard mapping.
- **Grade band:** `null` — no formal lock and no informal claim either.
- **Current stage:** Active review build
- **Build state:** `reviews/echo-heist/current/index.html` exists with `pass-1.html` historical snapshot and `playtest.js` headless test suite
- **Playtest state:** In-place pass records exist (pass-1-record.md through pass-5-record.md) but no playtest verification file in `artifacts/playtests/echo-heist/`
- **Pass records:** In-place at `reviews/echo-heist/current/pass-1-record.md` through `pass-5-record.md` (NOT in `artifacts/pass_records/`)
- **Misconception linkage:** None. No `artifacts/misconception_library/echo-heist-misconceptions.json` exists. Tracked as a future content gap per the locked cleanup decisions.
- **Intended release path:** `games/echo-heist/releases/<version>/index.html` *(none exist; not yet shipped)*
- **Release state:** `never_shipped`
- **Next agent:** None currently assigned.
- **Current blocker for shipping:** No ship-ready gate has been run. No `concepts/echo-heist/` packet. No canonical interaction type. No misconception library entries. Multi-topic content has no formal standard mapping.
- **Family registry entry:** `Pending Formal Family Placement` → `Echo Heist` in [`memory/registries/family_registry.json`](../memory/registries/family_registry.json)

### Fire Dispatch

> ⚠ **Validation status: active review build — no formal concept packet, no formal alignment, not shipped.**
> A working review build exists at `reviews/fire/current/index.html` with four pass records in `artifacts/pass_records/`. Misconception library entries exist. **No `concepts/fire/` packet exists**, so the curriculum alignment and grade band are informal. **No release has been cut**. This lane entry records the presence of an active development build only.

- **Slug:** `fire`
- **Display title:** Fire Station Dispatch
- **Concept source of truth:** none (`concepts/fire/` does not exist)
- **Informal concept source:** [`docs/concept_inputs/top_5_math_concepts_claude_packet.md`](concept_inputs/top_5_math_concepts_claude_packet.md)
- **Family:** Pending Formal Family Placement *(pseudo-family — not formally placed in [`family_map_math.md`](concept_inputs/strategy/family_map_math.md); no documented best-fit family)*
- **Interaction type:** `route_and_dispatch` *(listed under `example_games` in [`orchestrator_v3/policies/interaction_types.yaml`](../orchestrator_v3/policies/interaction_types.yaml))*
- **Primary standard:** `null` — no formal alignment packet. Benchmark-case language refers to "multiplication" but the actual game mechanic is subset-sum selection (additive decomposition), not multiplication.
- **Grade band:** `null` — no formal lock. Benchmark-case language refers to "grades 4–6" but that is not a formal packet.
- **Current stage:** Active review build
- **Build state:** `reviews/fire/current/index.html` exists; also `pass-3.html` historical snapshot
- **Playtest state:** At least one documented playtest verification at [`artifacts/playtests/fire-dispatch/2026-04-05-p3-verification.md`](../artifacts/playtests/fire-dispatch/2026-04-05-p3-verification.md)
- **Pass records:** [`artifacts/pass_records/`](../artifacts/pass_records/) — `fire-dispatch-pass-1.json`, `fire-dispatch-pass-2a.json`, `fire-dispatch-pass-2b.json`, `fire-dispatch-pass-3.json`
- **Misconception linkage:** [`artifacts/misconception_library/fire-dispatch-misconceptions.json`](../artifacts/misconception_library/fire-dispatch-misconceptions.json)
- **Intended release path:** `games/fire/releases/<version>/index.html` *(none exist; not yet shipped)*
- **Release state:** `never_shipped`
- **Next agent:** None currently assigned.
- **Current blocker for shipping:** No ship-ready gate has been run. No `concepts/fire/` packet. No formal family placement.
- **Family registry entry:** `Pending Formal Family Placement` → `Fire Dispatch` in [`memory/registries/family_registry.json`](../memory/registries/family_registry.json)

### Power Grid Operator

> ⚠ **Validation status: active review build — no formal packet, no canonical taxonomy fit, no misconception linkage, not shipped.**
> A working review build exists at `reviews/power-grid/current/index.html`. **No `concepts/power-grid/` packet exists**. No pass records in `artifacts/pass_records/`. No misconception library entries. The interaction type (missing-addend / one-step equation) is not represented in the canonical taxonomy. **No release has been cut**. This lane entry records the presence of an active development build only.

- **Slug:** `power-grid`
- **Display title:** Power Grid Operator
- **Concept source of truth:** none (`concepts/power-grid/` does not exist)
- **Informal concept source:** None — concept lives inline in the review build with no external packet
- **Family:** Pending Formal Family Placement *(pseudo-family — no documented family fits this concept)*
- **Interaction type:** `pending_taxonomy_placement` — core act is solving a one-step equation (missing addend); closest documented adjacency is `combine_and_build` (additive reasoning), but the player works backward from a target rather than accumulating toward it
- **Primary standard:** `null` — no formal alignment packet. Game mechanic is single-step additive equation (current + x = demand), consistent with early missing-addend work, but no explicit CCSS standard is claimed anywhere in the repo.
- **Grade band:** `null` — no formal lock and no informal claim either.
- **Current stage:** Active review build
- **Build state:** `reviews/power-grid/current/index.html` exists (3 levels + tutorial)
- **Playtest state:** None documented
- **Pass records:** None in `artifacts/pass_records/`
- **Misconception linkage:** None. No `artifacts/misconception_library/power-grid-misconceptions.json` exists. Tracked as a future content gap per the locked cleanup decisions.
- **Intended release path:** `games/power-grid/releases/<version>/index.html` *(none exist; not yet shipped)*
- **Release state:** `never_shipped`
- **Next agent:** None currently assigned.
- **Current blocker for shipping:** No ship-ready gate. No `concepts/power-grid/` packet. No canonical interaction type. No misconception library entries. No pass records.
- **Family registry entry:** `Pending Formal Family Placement` → `Power Grid Operator` in [`memory/registries/family_registry.json`](../memory/registries/family_registry.json)

### Snack Line Shuffle

> ⚠ **Validation status: approved concept only — not yet prototyped.**
> This entry documents that Snack Line Shuffle has been approved for
> concept normalization and repo placement. **No preview build exists.**
> No playtests have been run. No P1 Definition of Done has been checked.
> This lane entry must not be cited as evidence of build validation,
> curricular coverage proof, or family/interaction-type coverage. It
> records the approval state of the concept only.

- **Concept source of truth:** [`concepts/snack-line-shuffle/`](../concepts/snack-line-shuffle/)
- **Family:** Compare and Order
- **Interaction type:** `sequence_and_order`
- **Primary standard:** CCSS.MATH.CONTENT.1.OA.C.6 *(alignment claim, not fluency claim; see concept.md fluency caution)*
- **Grade band:** K–2 core (Grade 2+ ceiling layers gated)
- **Current stage:** Approved concept, entering normalization
- **Build state:** No review build — deferred. **No prototype exists.**
- **Playtest state:** None. No learners have played this concept.
- **P1 Definition of Done:** Drafted, not yet checked. See [`concepts/snack-line-shuffle/p1_definition_of_done.md`](../concepts/snack-line-shuffle/p1_definition_of_done.md).
- **Intended review path:** `reviews/snack-line-shuffle/current/index.html` (not created)
- **Slug-level placeholder:** [`reviews/snack-line-shuffle/README.md`](../reviews/snack-line-shuffle/README.md) — documents why no prototype exists yet
- **First member of family:** yes — structurally, not evidentially
- **First proof case for interaction type:** yes — pending a prototype that actually demonstrates the type
- **Next agent after normalization:** Game Design Critic (reviews P1 pass record — *after* P1 implementation, which requires separate approval)
- **Next owner after that:** Prototype Engineer (pre-build → build transition)
- **Current blocker:** None for normalization. P1 implementation requires separate explicit approval.
- **Misconception linkage:** [`artifacts/misconception_library/snack-line-shuffle-misconceptions.json`](../artifacts/misconception_library/snack-line-shuffle-misconceptions.json) — M4–M7 linked to canonical categories (core fields populated; enrichment pending after P1 playtest data)

### Unit Circle Pizza Lab

> ⚠ **Validation status: active review build — no formal concept packet, no formal alignment, not shipped.**
> A working review build exists at `reviews/unitcircle/current/index.html` with three pass records in `artifacts/pass_records/`. Misconception library entries exist. **No `concepts/unitcircle/` packet exists**, so the curriculum alignment and grade band are informal. **No release has been cut**. This lane entry records the presence of an active development build only.

- **Slug:** `unitcircle`
- **Display title:** Unit Circle Pizza Lab
- **Concept source of truth:** none (`concepts/unitcircle/` does not exist)
- **Informal concept source:** [`docs/concept_inputs/top_5_math_concepts_claude_packet.md`](concept_inputs/top_5_math_concepts_claude_packet.md)
- **Family:** Pending Formal Family Placement *(pseudo-family — not formally placed; closest documented adjacency is Family 3 Coordinate Navigation in [`family_map_math.md`](concept_inputs/strategy/family_map_math.md), but that family's examples are Cartesian grid games; Unit Circle is angular/trigonometric)*
- **Interaction type:** `navigate_and_position` *(listed under `example_games` in [`orchestrator_v3/policies/interaction_types.yaml`](../orchestrator_v3/policies/interaction_types.yaml))*
- **Primary standard:** `null` — no formal alignment packet. Benchmark-case language refers to "trigonometry"; the game mechanic covers unit circle angles and coordinates but no specific CCSS code is formally claimed.
- **Grade band:** `null` — no formal lock. Benchmark-case language refers to "high school" but that is not a formal packet.
- **Current stage:** Active review build
- **Build state:** `reviews/unitcircle/current/index.html` exists; also `pass-3.html` historical snapshot
- **Playtest state:** `artifacts/playtests/unit-circle/` exists but is empty — no verification file recorded
- **Pass records:** [`artifacts/pass_records/`](../artifacts/pass_records/) — `unit-circle-pass-1.json`, `unit-circle-pass-2a.json`, `unit-circle-pass-2b.json`
- **Misconception linkage:** [`artifacts/misconception_library/unit-circle-misconceptions.json`](../artifacts/misconception_library/unit-circle-misconceptions.json)
- **Intended release path:** `games/unitcircle/releases/<version>/index.html` *(none exist; not yet shipped)*
- **Release state:** `never_shipped`
- **Next agent:** None currently assigned.
- **Current blocker for shipping:** No ship-ready gate has been run. No `concepts/unitcircle/` packet. No formal family placement.
- **Family registry entry:** `Pending Formal Family Placement` → `Unit Circle Pizza Lab` in [`memory/registries/family_registry.json`](../memory/registries/family_registry.json)

### Watering Hole Count

> ⚠ **Validation status: active review build — no formal packet, no canonical taxonomy fit, no misconception linkage, not shipped.**
> A working review build exists at `reviews/counting/current/index.html`. **No `concepts/counting/` packet exists**. No pass records in `artifacts/pass_records/`. No misconception library entries. The interaction type (enumerate-and-report / count-and-verify) is not represented in the canonical taxonomy. **No release has been cut**. This lane entry records the presence of an active development build only.

- **Slug:** `counting`
- **Display title:** Watering Hole Count
- **Concept source of truth:** none (`concepts/counting/` does not exist)
- **Informal concept source:** [`artifacts/learning_captures/2026-04-07-counting-concept-lane.md`](../artifacts/learning_captures/2026-04-07-counting-concept-lane.md), [`artifacts/learning_captures/2026-04-07-counting-p0p1-implementation-plan.md`](../artifacts/learning_captures/2026-04-07-counting-p0p1-implementation-plan.md) *(historical learning captures, not rewritten)*
- **Family:** Pending Formal Family Placement *(pseudo-family — no documented family fits counting/cardinality as a distinct cognitive act)*
- **Interaction type:** `pending_taxonomy_placement` — enumerate-and-report / count-and-verify is not a clean match for any of: `combine_and_build`, `route_and_dispatch`, `allocate_and_balance`, `transform_and_manipulate`, `navigate_and_position`, `sequence_and_predict`, `sequence_and_order`
- **Primary standard:** `null` — no formal alignment packet. In-file header comment informally refers to "counting / cardinality" without a specific CCSS code.
- **Grade band:** `null` — no formal lock. In-file header comment informally refers to "ages 4–6 (Pre-K to Grade 1)" but that is not a formal packet.
- **Current stage:** Active review build
- **Build state:** `reviews/counting/current/index.html` exists
- **Playtest state:** None documented
- **Pass records:** None in `artifacts/pass_records/`
- **Misconception linkage:** None. No `artifacts/misconception_library/counting-misconceptions.json` exists. Tracked as a future content gap per the locked cleanup decisions.
- **Intended release path:** `games/counting/releases/<version>/index.html` *(none exist; not yet shipped)*
- **Release state:** `never_shipped`
- **Next agent:** None currently assigned.
- **Current blocker for shipping:** No ship-ready gate. No `concepts/counting/` packet. No canonical interaction type. No misconception library entries. No pass records.
- **Family registry entry:** `Pending Formal Family Placement` → `Watering Hole Count` in [`memory/registries/family_registry.json`](../memory/registries/family_registry.json)

---

## Retired / archived concepts

(none yet)

---

## Lane schema

Each active concept entry should include, at minimum:

- concept source of truth path
- family and interaction type
- primary CCSS standard and grade band
- current stage
- build state (no preview, P0, P1, P2A/B, P3, P4, P5)
- intended preview path
- next agent and next owner
- current blocker (if any)
- misconception library link
