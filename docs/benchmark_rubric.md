# V1 Benchmark Output — Qualitative Review Rubric

Used to evaluate the three approved benchmark concepts after a pipeline run. Apply to the
`interaction_decision_memo`, `family_architecture_brief`, and `lowest_viable_loop_brief`
artifacts for each approved job.

---

## Scoring Guide

Each dimension is scored **1–4**:

| Score | Meaning |
|---|---|
| 4 — Exemplary | No gaps; ready to ship to prototyping as-is |
| 3 — Strong | Minor gaps or open questions; acceptable for V1 |
| 2 — Weak | Meaningful gaps that need resolution before prototyping |
| 1 — Failing | Structural problem; concept should not advance |

---

## Dimension 1: Clarity

*Can a designer who has never seen this concept understand what the game is and what the
player does, in under 10 seconds?*

| Score | Signal |
|---|---|
| 4 | One-sentence promise is specific, world is vivid, action is unambiguous |
| 3 | Concept is clear but one element (world, action, or goal) needs sharpening |
| 2 | Either the world or the action is vague; 10-second test would likely fail |
| 1 | Concept cannot be understood without reading the full artifact set |

**Evidence to check:** `one_sentence_promise_draft` (intake), `plain_english_concept`, `teacher_shortcut_version` (loop brief).

---

## Dimension 2: Interaction Purity

*Is the math action the game action — or does math sit alongside or underneath the game?*

| Score | Signal |
|---|---|
| 4 | `interaction_purity_score ≥ 0.90`; `is_action_itself_the_math = true`; no overload warning |
| 3 | `purity_score 0.75–0.89`; secondary type present but clearly subordinate |
| 2 | `purity_score 0.60–0.74`; or secondary type risks becoming co-primary |
| 1 | `purity_score < 0.60`; math is decorative or gated |

**Evidence to check:** `interaction_purity_score`, `is_action_itself_the_math`, `interaction_overload_warning`, `split_family_warning`.

---

## Dimension 3: Family Placement Quality

*Is the concept placed in the right family, with boundaries that will hold as the family grows?*

| Score | Signal |
|---|---|
| 4 | Factory type correct; `reason_for_family_placement` is specific; `boundary_break_example` is airtight; `family_boundary_rule` has three or more enumerated conditions |
| 3 | Placement is correct; minor overlap risk noted and explained; growth path is plausible |
| 2 | Factory type may be wrong OR boundaries are vague OR overlap warnings are unresolved |
| 1 | Concept is placed in an incorrect family, or boundary_break_example is circular |

**Evidence to check:** `factory_type`, `family_boundary_rule`, `boundary_break_example`, `family_overlap_warnings`, `split_family_warning` handling.

---

## Dimension 4: Loop Quality

*Is the minimum viable loop genuinely minimal, repeatable, and satisfying without any added
features?*

| Score | Signal |
|---|---|
| 4 | `max_steps_per_loop ≤ 4`; signature moment is specific and mechanical (not vague); fail state is instructive; confusion risks are enumerated; micro-prototype is playable with household objects |
| 3 | Loop is clean; one element (fail state or confusion risks) could be more specific |
| 2 | Loop has more than 4 steps OR signature moment is vague OR fail state is punishing/missing |
| 1 | Loop is not minimal; cannot repeat without a tutorial or progression unlock |

**Evidence to check:** `max_steps_per_loop`, `signature_moment`, `fail_state_structure`, `expected_confusion_risks`, `micro_prototype_recommendation`.

---

## Dimension 5: Educational Value

*Is this concept age-appropriate, skill-specific, and legible to a classroom teacher?*

| Score | Signal |
|---|---|
| 4 | Target skill is named precisely; age band is correct; teacher shortcut works as a physical activity; no ambiguity about what skill is being practiced |
| 3 | Skill is clear but one age-band edge case or representation ambiguity exists |
| 2 | Skill is vague OR the teacher shortcut is too complex to run in a classroom |
| 1 | Skill cannot be reliably assessed from gameplay; concept is thematically educational but mechanically vague |

**Evidence to check:** `likely_target_skills`, `likely_age_band`, `teacher_shortcut_version`, `ambiguities_detected` count, `confidence_scores.math_fit`.

---

## Dimension 6: Monetization Potential

*Does the concept support a viable product — repeat play, difficulty progression, and a reason
to return?*

| Score | Signal |
|---|---|
| 4 | Clear progression model; strong replay driver (time pressure, streak, collection); natural difficulty levers identified in family growth path |
| 3 | Replay is plausible; one lever (e.g., collections or social) is underdeveloped |
| 2 | Replay depends entirely on difficulty escalation with no emotional or social hook |
| 1 | Single-session concept; no natural reason to return after skill is mastered |

**Evidence to check:** `family_growth_path` (difficulty levers), `possible_emotional_hook`, `fail_state_structure` (is failure recoverable?), `replay_potential` score from kill report.

---

## Score Summary Template

```
Concept: <name>
Job ID: <job_id>

| Dimension              | Score (1–4) | Notes |
|------------------------|-------------|-------|
| Clarity                |             |       |
| Interaction Purity     |             |       |
| Family Placement       |             |       |
| Loop Quality           |             |       |
| Educational Value      |             |       |
| Monetization Potential |             |       |
| TOTAL                  | /24         |       |

Strengths:
Weak spots:
Recommended next action:
```
