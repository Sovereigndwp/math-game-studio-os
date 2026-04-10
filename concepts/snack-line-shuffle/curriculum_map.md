# Snack Line Shuffle — Curriculum Map Entry

## Overview

| Field | Value |
|---|---|
| **Game** | Snack Line Shuffle |
| **Grade band** | K–2 (K–1 core within 10, addition-dominant; Grade 2+ extension with mixed +/-, within 20, longer sequences) |
| **Grade 1 anchor rationale** | CCSS 1.OA.C.6 is the first standard to explicitly call for within-20 fluency as a goal. Ordering computed totals is a natural fluency consolidation context at Grade 1. Kindergarten entry uses addition within 5 only (warm-up tier). Grade 2 extension introduces subtraction pairs and longer sequences. |
| **Anchor standard** | [CCSS.MATH.CONTENT.1.OA.C.6](http://www.corestandards.org/Math/Content/1/OA/C/6/) — Add and subtract within 20, demonstrating fluency for addition and subtraction within 10. Use strategies such as making ten, decomposing a number leading to a ten, and creating equivalent but easier sums. |
| **Standard removed / not claimed** | **1.NBT.B.3** (place-value comparison using `>`, `=`, `<` notation). Removed as overreach on 2026-04-08. Do not include in any educator-facing alignment materials for this game. |
| **Curriculum role** | Practice and consolidation. **Not a first-instruction tool.** Intended for use after classroom introduction of addition strategies. Complements but does not replace direct instruction on 1.OA.C.6. |
| **Math domain** | Operations and Algebraic Thinking (OA). Does NOT sit under Number and Operations in Base Ten (NBT) despite surface-level similarity to comparison tasks. |
| **Interaction family** | Sequence / Ordering — first K-2 member of this family. See [`memory/registries/family_registry.json`](../../memory/registries/family_registry.json) (`Compare and Order` family, `sequence_and_order` interaction type). |

## Coexistence with Bakery Rush

Bakery Rush (Exact-Sum Composition family, active review build in `reviews/bakery/`) occupies the "Addition & Subtraction to 20 — Compose to Exact Total" slot. Snack Line Shuffle occupies the distinct "Compare and Order Computed Totals" sub-skill.

The two games serve different cognitive targets within 1.OA and should both appear in a K-2 portfolio without overlap risk:

| Dimension | Bakery Rush | Snack Line Shuffle |
|---|---|---|
| Family | Exact-Sum Composition | Sequence / Ordering |
| Cognitive target | Compose values to match a target total | Compute totals then rank them |
| Interaction type | `combine_and_build` | `sequence_and_order` |
| Direction of the math work | Target given, decompose | Expressions given, compute |

Both slots belong in a K-2 portfolio. Neither is a substitute for the other.

*Note on formal provenance:* Bakery Rush does not currently have a formal concept packet or formal CCSS alignment in this repo — see `memory/registries/family_registry.json` where `primary_standard` is null for Bakery Rush. The coexistence statement above is a design-intent claim about cognitive targets, not a formal curricular alignment claim for Bakery Rush. Only Snack Line Shuffle has a formal alignment in this repo.

## Misconceptions addressed

| Code | Misconception | Active from |
|---|---|---|
| **M1** | Bigger first addend = bigger total | K-1 |
| **M2** | Equal totals must rank differently | K-1 |
| **M3** | Subtraction always loses | K-1 |
| **M4** | Leftmost digit dominance | Grade 2+ |
| **M5** | Operation sign blindness | Grade 2+ |
| **M6** | Zero-subtraction overgeneralisation | Grade 2+ |
| **M7** | Bigger number first = bigger result | Grade 2+ |

M1–M3 are active in K-1 levels. M4–M7 are gated to Grade 2+ levels and must NOT appear in any K-1 round. M4 and M7 co-occurrence is flagged in the misconception notes and requires explicit Grade 2+ content-set authoring.

Full register: [`misconception_notes.md`](misconception_notes.md) and [`../../artifacts/misconception_library/snack-line-shuffle-misconceptions.json`](../../artifacts/misconception_library/snack-line-shuffle-misconceptions.json).

## Grade-band scope map

### Kindergarten tier
- **Math scope** — Addition within 5 only
- **Line length** — 2–3 kids
- **Rule** — Largest-first only
- **Ties** — None; all totals distinct
- **Operations** — Addition only; no subtraction
- **CCSS** — K.OA.A.1, K.OA.A.2 (informal practice, not an alignment claim)

### Grade 1 tier (anchor — P1 target)
- **Math scope** — Addition within 10
- **Line length** — 3–4 kids
- **Rule** — Largest-first only
- **Trap coverage** — Contrast sets targeting M1 (bigger addend ≠ bigger total); ≥ 30% of rounds must be M1 trap rounds. Current P1 set is 7 / 14 = 50% M1 traps.
- **Operations** — Addition only; no subtraction
- **CCSS** — 1.OA.C.6 (anchor standard, formally claimed)

### Grade 2 tier (gated — not in P1 build)
- **Math scope** — Mixed `+/-` within 20
- **Line length** — 5–6 kids
- **Rule variants** — Largest-first, smallest-first, positional constraints
- **Misconception set** — M3–M7 active
- **CCSS** — 2.OA.B.2 (extension, not anchor)
- **Gate** — Content plan must be reviewed by the Curriculum Architect before any Grade 2 level is authored. This is a hard gate.

### Natural ceiling
6-kid mixed `+/-` lines within 20 under positional constraints. Beyond this, multi-step expressions or unknown-addend expressions require a different UI model. The game has no content pathway into Grades 3+.

## Cross-references

- **Engineer handoff** — [`p1_engineer_handoff.md`](p1_engineer_handoff.md) covers the full P1 build brief (scene spec, Option B Serve mechanic, content constraints, grade-band gate, and all 14 P1 DoD gates)
- **Question audit** — [`question_audit.md`](question_audit.md) covers the 2026-04-09 audit of all 14 P1 rounds
- **Family registry entry** — [`../../memory/registries/family_registry.json`](../../memory/registries/family_registry.json) (`Compare and Order` family, first member)
- **Misconception notes** — [`misconception_notes.md`](misconception_notes.md) for the M1–M7 register
- **P1 DoD gates** — [`p1_definition_of_done.md`](p1_definition_of_done.md)

## Document metadata

| Field | Value |
|---|---|
| **Path** | `concepts/snack-line-shuffle/curriculum_map.md` |
| **Origin** | normalized from Taskade project `fQKsxPJWgG2kPRoQ` ("K-12 Curriculum Map"), Snack Line Shuffle entry only |
| **Raw source** | [`taskade_exports/projects/fQKsxPJWgG2kPRoQ.json`](../../taskade_exports/projects/fQKsxPJWgG2kPRoQ.json) |
| **First normalized into repo** | 2026-04-10 |
| **Note** | The Taskade "K-12 Curriculum Map" project is board-wide and includes other grade-band slots for games without formal repo packets (Bakery Rush 1.OA, Fire Dispatch 3–5, Percents 6–8, Algebra 6–8, etc.). Only the Snack Line Shuffle entry is normalized into this file because it is the only game with a formal concept packet. Other entries remain in `docs/taskade_concept_inbox.md` pending formal packetization. |
