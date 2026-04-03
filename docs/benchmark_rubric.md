# V1 Benchmark Output — Qualitative Review Rubric

Applied to approved concepts after a pipeline run. Evaluate the
`interaction_decision_memo`, `family_architecture_brief`, and
`lowest_viable_loop_brief` artifacts for each approved job.

---

## Scoring Guide

Each dimension is scored **1–4**:

| Score | Meaning |
|---|---|
| 4 — Exemplary | No gaps; ready to ship to prototyping as-is |
| 3 — Strong | Minor gaps or open questions; acceptable for V1 |
| 2 — Weak | Meaningful gaps that need resolution before prototyping |
| 1 — Failing | Structural problem; concept should not advance |

**When dimensions conflict** (e.g., education = 4, monetization = 2): do not average
them away. The summary should name which dimension most constrains advancement and why.
A low monetization score does not block a concept from educational use; a low loop
quality score blocks everything.

---

## Dimension 1: Clarity

*Can a designer who has never seen this concept understand what the game is and what the
player does, in under 10 seconds?*

| Score | Signal |
|---|---|
| 4 | One-sentence promise is specific, world is vivid, action is unambiguous |
| 3 | Concept is clear but one element (world, action, or goal) needs sharpening |
| 2 | Either the world or the action is vague; 10-second test would fail |
| 1 | Concept cannot be understood without reading the full artifact set |

**Evidence:** `one_sentence_promise_draft` (intake brief), `plain_english_concept`,
`teacher_shortcut_version` (loop brief — should be executable in under 5 minutes
with no digital tools).

---

## Dimension 2: Interaction Purity

*Is the math action the game action — or does math sit alongside or underneath the game?*

| Score | Signal |
|---|---|
| 4 | `interaction_purity_score ≥ 0.90`; `is_action_itself_the_math = true`; no overload warning |
| 3 | `purity_score 0.75–0.89`; secondary type present but clearly subordinate and staged |
| 2 | `purity_score 0.60–0.74`; or secondary type risks becoming co-primary |
| 1 | `purity_score < 0.60`; math is decorative or gated behind a separate action |

**Evidence:** `interaction_purity_score`, `is_action_itself_the_math`,
`interaction_overload_warning`, `split_family_warning`.

---

## Dimension 3: Family Placement Quality

*Is the concept placed in the right family, with boundaries that will hold as the
family grows?*

| Score | Signal |
|---|---|
| 4 | Factory type correct; `reason_for_family_placement` is specific; `boundary_break_example` is airtight; `family_boundary_rule` lists **three or more named, distinct conditions** — e.g. "(A) player selects discrete objects, (B) goal is a numeric target sum, (C) selection equals the arithmetic act" |
| 3 | Placement correct; minor overlap risk noted and explained; growth path is plausible |
| 2 | Factory type may be wrong OR boundaries are vague OR overlap warnings are unresolved |
| 1 | Concept is in an incorrect family, or `boundary_break_example` is circular |

**Evidence:** `factory_type`, `family_boundary_rule`, `boundary_break_example`,
`family_overlap_warnings`, `split_family_warning` handling in family notes.

---

## Dimension 4: Loop Quality

*Is the minimum viable loop genuinely minimal, repeatable, and satisfying without any
added features?*

| Score | Signal |
|---|---|
| 4 | `max_steps_per_loop ≤ 4`; signature moment is specific and mechanical (not "the player feels good"); fail state is instructive; confusion risks enumerated with concrete causes; micro-prototype is playable with household objects in under 5 minutes |
| 3 | Loop is clean; one element (fail state detail or confusion risk specificity) could be tightened |
| 2 | Loop has more than 4 steps OR signature moment is vague OR fail state is punishing or absent |
| 1 | Loop is not minimal; requires a tutorial or progression unlock before repeating |

**Evidence:** `max_steps_per_loop`, `signature_moment`, `fail_state_structure`,
`expected_confusion_risks`, `micro_prototype_recommendation`.

---

## Dimension 5: Educational Value

*Is this concept age-appropriate, skill-specific, and legible to a classroom teacher?*

| Score | Signal |
|---|---|
| 4 | Target skill is named precisely (not just "math"); age band is correct; teacher shortcut is deployable as a physical activity in under 5 minutes with no digital tools; no ambiguity about which skill is practiced |
| 3 | Skill is clear but one age-band edge case or representation ambiguity exists |
| 2 | Skill is vague OR teacher shortcut is too complex to run in a classroom |
| 1 | Skill cannot be reliably assessed from gameplay; thematically educational but mechanically vague |

**Evidence:** `likely_target_skills`, `likely_age_band`, `teacher_shortcut_version`,
`ambiguities_detected` count, `confidence_scores.math_fit`
(≥ 0.8 supports a score of 4; < 0.6 suggests score 2 or below).

---

## Dimension 6: Monetization Potential

*Does the concept support a viable product — repeat play, difficulty progression, and
an identifiable reason to return after initial skill acquisition?*

| Score | Signal |
|---|---|
| 4 | Clear progression model; identifiable reason for repeat play beyond skill mastery (e.g., progression, social, time pressure, collection, competitive ranking); natural difficulty levers named in family growth path |
| 3 | Replay is plausible; one return-visit driver (e.g., social or collection layer) is underdeveloped |
| 2 | Replay depends entirely on difficulty escalation; no emotional or social hook beyond "get better at the skill" |
| 1 | Single-session concept; no natural reason to return after the target skill is mastered |

**Evidence:** `family_growth_path` (difficulty levers), `possible_emotional_hook`,
`fail_state_structure` (is failure recoverable without penalty?),
`replay_potential` score from kill report (≥ 0.7 supports a score of 4; < 0.5 suggests 2).

---

## Score Summary Template

```
Concept: <name>
Job ID:  <job_id>
Run date: <YYYY-MM-DD>
Mode: stub | LLM (<model>)

| Dimension              | Score (1–4) | Notes |
|------------------------|-------------|-------|
| Clarity                |             |       |
| Interaction Purity     |             |       |
| Family Placement       |             |       |
| Loop Quality           |             |       |
| Educational Value      |             |       |
| Monetization Potential |             |       |
| TOTAL                  |        /24  |       |

Strengths: (3–4 bullets — what is working well structurally)
Weak spots: (up to 3, ordered by blocking impact — highest risk first)
Constraining dimension: (the single score that most limits advancement)
Recommended next action: (one sentence + one concrete step)
```
