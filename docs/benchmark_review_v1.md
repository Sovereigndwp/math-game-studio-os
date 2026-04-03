# V1 Benchmark — Qualitative Review of Approved Outputs

Generated: 2026-04-03
Pipeline mode: LLM (claude-sonnet-4-6)
Canonical report: `reports/benchmark_regression_llm_20260403T225330Z.md`
Rubric: `docs/benchmark_rubric.md`

---

## bench_01 · strong_elementary_bakery

**Concept:** Grade 2 bakery game — pack pastry orders (addition to 20) before customers leave.
**Job ID:** job_20260403T224434332153Z
**Interaction:** combine_and_build (purity: 0.93)
**Family:** Early-Arithmetic Combine-and-Build: Discrete Object Composition (Ages 5–8) — age_band_specialist

| Dimension | Score | Notes |
|---|---|---|
| Clarity | 4 | "Race against the clock to pack the perfect pastry order by combining the right treats to hit the target number before the customer loses patience and walks out." One sentence, zero ambiguity. Teacher shortcut (flip two quantity cards, say the sum) runs in under 30 seconds with zero materials. |
| Interaction Purity | 4 | 0.93 purity. `is_action_itself_the_math = true`. No secondary type. Tray selection IS the addition act — no proxy, no gate. Rejected alternatives (allocate_and_balance, route_and_dispatch, sequence_and_predict) are each tested against the game's actual math structure, not just theme. |
| Family Placement | 4 | Factory type (age_band_specialist) correct. Three-part boundary rule: (A) player selects discrete countable objects as addends, (B) goal is to reach a specific numeric target sum, (C) selection action itself constitutes the arithmetic operation — no symbolic entry permitted. Both break examples (symbolic text-field entry; subtraction-as-removal) are airtight. Overlap warnings correctly identify universal_ladder adjacency and counting-on / sequence confusion risks. |
| Loop Quality | 4 | 4 steps max. Signature moment is mechanical and specific: the box snaps shut the instant the running count reaches the target — no vagueness. Fail state (tray reset + timer continues; customer leaves only on time expiry) is instructive without punishing hesitation. Five confusion risks named with concrete causes. Micro-prototype: 10 index cards, zero digital tools, playable in under 2 minutes. |
| Educational Value | 4 | Target skills named precisely: addition facts within 20, counting on, number bond recognition. Age band 5–8 is exact. Dual representation (numeral label + matching pastry icons on same tray) scaffolds both numeral readers and counters without a tutorial branch — this is the right call for Grade 2. |
| Monetization Potential | 4 | Customer urgency drives repeat play without a separate reward system. Timer pressure is a built-in difficulty lever. Family growth path provides three distinct tiers (sums to 10 → 20 → multi-addend). Thematic variants (fruit stand, toy shop, aquarium stocking) allow reskin without redesigning the mechanic. |
| **TOTAL** | **24/24** | |

**Strengths:**
- Near-perfect structural identity between game action and math operation — the highest purity score of the three approved concepts.
- Running count inside the order box is in-loop formative feedback that never interrupts play; the math surface is always visible.
- Family boundaries are rigorous enough to govern future game commissions without ambiguity.
- Loop teachable with a physical prototype in under 30 seconds; strong predictor that the digital version will require no tutorial.

**Weak spots:**
- One deferred decision: quantity representation mode (pictorial only vs. numeral only vs. mixed). Loop spec resolves this as "numeral label + matching icons" but the interaction memo notes this could shift the cognitive locus of the math if implementation diverges. Needs a final call before engineering begins — not before prototyping.
- No explicit wrong-answer feedback beyond tray reset for learners who select by icon count and ignore numerals. The running count mitigates this, but the edge case is unaddressed.

**Constraining dimension:** None — all dimensions are clean. No constraint on advancement.

**Recommended next action:** Advance to prototyping. Lock the quantity representation decision in the first build spec, before engineering begins.

---

## bench_02 · strong_middle_fire_dispatch

**Concept:** Grade 3 fire station dispatch game — send the right trucks and supplies to the right locations using arithmetic under time pressure.
**Job ID:** job_20260403T224651001833Z
**Interaction:** route_and_dispatch (purity: 0.82) + allocate_and_balance (secondary, staged at level 4+)
**Family:** Elementary Arithmetic Dispatch and Route — age_band_specialist

| Dimension | Score | Notes |
|---|---|---|
| Clarity | 3 | Primary loop clear: one incident card, two truck options, select the matching number. Teacher shortcut (demand card + two truck-capacity cards, point to the match) is excellent. The secondary supply mechanic adds scope ambiguity — a designer reading the family brief without the interaction memo may not know which mechanic to build first. The staging guidance exists but requires synthesizing two documents. |
| Interaction Purity | 3 | 0.82 purity. Primary loop (arithmetic comparison drives routing decision) is structurally clean. Secondary type (allocate_and_balance) is correctly staged at level 4+. Risk: supply mechanic was flagged as underspecified by the kill report; the interaction memo provides a concrete definition (see note below) but the loop brief correctly excludes it. If built without referencing the memo definition, the staged boundary may collapse. |
| Family Placement | 3 | Factory type (age_band_specialist, 8–11) correct. Three-part boundary rule: (a) elementary arithmetic, (b) route_and_dispatch primary, (c) arithmetic result IS the routing decision — removing arithmetic collapses the dispatch choice. Boundary-break example (fraction gate + pre-labeled button) is airtight. split_family_warning is acknowledged in family notes but monitoring is left implicit — no concrete task-distribution threshold defined to trigger re-evaluation. |
| Loop Quality | 3 | 4 steps max. Signature moment (correct truck launches toward incident, card clears) is clear and repeatable. Fail state (truck shakes, does not move, incident persists) is instructive with no penalty screen. Secondary mechanic correctly excluded from MVL. The `expected_time_to_first_correct_action_seconds` of 10 seconds may underestimate cognitive load at the lower end of the 8–11 band — reading a demand number AND comparing two truck capacity numbers is two sequential operations. |
| Educational Value | 3 | Arithmetic comparison (identify which truck capacity equals the demand) is a clear Grade 3 skill. The primary loop as specified uses exact-match comparison only — correct for a lowest viable loop, but the stated concept promise ("arithmetic under time pressure") implies addition and subtraction escalation. That escalation is not yet specified; it should be planned explicitly before the first prototype to avoid a bait-and-switch between the concept promise and the implemented mechanic. |
| Monetization Potential | 3 | Shift model (5 emergencies per shift, rated on speed and accuracy) provides natural session structure. Dispatcher role is aspirational for 8–11 year olds. Family growth path has four independent difficulty levers (arithmetic complexity, simultaneous incidents, supply mechanic, new dispatcher professions). Weaker area: collection and social hooks not yet defined. No visible reward artifact (badges, unlocked truck types, city map) to drive non-mandatory return visits. |
| **TOTAL** | **19/24** | |

**Supply mechanic authoritative definition** (from interaction_decision_memo, for build reference):
> "Player calculates total water tanks needed by adding the requirements of two simultaneous incidents, then checks whether depot stock covers the total using subtraction."
This definition keeps the math at grade-3 addition and subtraction, resolves the kill report's underspecification flag, and cleanly slots the mechanic into the allocate_and_balance secondary type without contaminating the primary routing loop.

**Strengths:**
- Dispatcher profession is a genuine structural fit: a real dispatcher's job is to calculate resource fit and route. Explains the concept as a career simulation, not just a game — unusual and strong teacher legibility.
- Interaction memo provides a concrete supply mechanic definition, fixing the kill report flag without deferring it.
- Four difficulty levers in the family growth path are independent — each can be introduced in isolation without redesigning other levels.

**Weak spots:**
- **Supply mechanic is analyzed but not loop-designed.** There is no lowest-viable-loop spec for the allocate_and_balance mechanic. The family cannot safely accept a second member until this spec exists.
- **Demand vs. capacity labeling has no UX answer.** A learner who does not understand that the truck number is a capacity and the card number is a demand will select randomly. The teacher shortcut handles this verbally; the digital version has no equivalent affordance defined.
- **Split family warning monitoring is implicit.** A concrete monitoring rule would be: "if any game in this family allocates more than 30% of tasks to supply calculations, re-evaluate family membership before releasing that game."

**Constraining dimension:** Loop Quality (3) — specifically the unspecified arithmetic-under-pressure escalation path and the demand/capacity labeling gap.

**Recommended next action:** Advance to prototyping with primary route_and_dispatch loop only. Commission the allocate_and_balance loop spec as a parallel task, not a blocker. Resolve demand/capacity labeling in the first UX pass.

---

## bench_03 · strong_high_school_unit_circle

**Concept:** High school trigonometry pizza lab — place toppings at (cos θ, sin θ) coordinates on a unit-circle pizza surface.
**Job ID:** job_20260403T224911615850Z
**Interaction:** navigate_and_position (purity: 0.87) + transform_and_manipulate (secondary, staged)
**Family:** Unit Circle Coordinate Positioning Games (High School Trigonometry) — advanced_anchor

| Dimension | Score | Notes |
|---|---|---|
| Clarity | 4 | "Drag a topping to the point (cos θ, sin θ) on the pizza edge" is immediately legible to any HS math student. Pizza-as-unit-circle is structurally exact, not decorative — a pizza of normalized radius IS a unit circle. Teacher shortcut (draw circle, mark axes, student places a coin at the angle coordinate) deployable in any classroom with a marker and paper. |
| Interaction Purity | 3 | 0.87 purity. `is_action_itself_the_math = true`. Secondary type (transform_and_manipulate for oven-rotation tasks) excluded from MVL and correctly staged. Honest deduction: early quadrant-1 tasks at axis-aligned angles (θ = 0 → (1,0); θ = π/2 → (0,1)) can be solved by visual anchoring without trig reasoning — a genuine fidelity risk at low difficulty. The memo calls this out accurately. |
| Family Placement | 4 | Factory type (advanced_anchor) correct — concept is anchored to a specific abstract domain, not a numerical range. Boundary rule is the most precise of the three: every member must require evaluation of (cos θ, sin θ) to complete the primary action; any task solvable by visual symmetry, pattern matching, or non-trig estimation without loss of correctness violates family identity. Both break examples (labeled cardinal-direction zones; explicit (x,y) labels) correctly identify violations that remove trig reasoning. Overlap warnings distinguish this family from coordinate geometry (pre-algebra) and circular geometry (middle school arc/sector) families. |
| Loop Quality | 3 | 4 steps max. Signature moment (topping snaps to exact coordinate + coordinate pair flashes) is specific and repeatable every loop. Fail state teaches: correct position reveals for 1.5 seconds after a miss, making wrong placement a free worked example. `expected_time_to_first_correct_action_seconds` is 25 seconds — realistic for trig computation. Critical gap: acceptance zone calibration (suggested 8% of pizza radius) is unresolved. Too tight → repeated early failure before skill is built. Too loose → learners succeed by pointing at the right quadrant without computing (cos θ, sin θ). This is the single highest-stakes unresolved parameter for instructional validity. |
| Educational Value | 4 | Target skill maximally specific: evaluate (cos θ, sin θ) for a given radian angle, use result to determine a position on the unit circle. Age band 14–18 is exact. Difficulty scaffolding sequence (Q1 canonical angles → full circle → radian arc rotation) maps cleanly to standard HS trig curriculum. Lab/structured-practice mode protects instructional fidelity — time pressure as an optional overlay, not the canonical interaction mode. Fail state designed to teach, not penalize — rare and correct at this abstraction level. |
| Monetization Potential | 2 | HS trig is a structurally narrow audience. Lab mode reduces the casual engagement ceiling. Family growth path (Q1 → full circle → radian arc) is a curriculum sequence, not a game progression — educationally sound but lacks emotional escalation drivers (customer stakes, time pressure, collection) that create non-mandatory return visits. Replay after skill mastery is low — the concept's value is concentrated in the learning phase. No collection or social hook identified. |
| **TOTAL** | **20/24** | |

**Early-task purity note:** The axis-aligned angle risk (θ = 0, π/2) belongs to difficulty scaffolding, not to the MVL. The recommended mitigation is a session-design constraint: *every session that includes an axis-aligned angle must pair it with at least one non-axis angle in the same session*, preventing learners from building a purely visual strategy. This constraint should be documented in the difficulty scaffolding spec before level design begins, not in the loop brief.

**Strengths:**
- Pizza IS the unit circle — structural metaphor, not costume. Every placement is a genuine trig computation. Immediately explainable to teachers and students without a tutorial.
- Fail state (correct position reveal for 1.5 seconds on miss) is the strongest instructional mechanism across all three approved concepts — wrong placement becomes a free worked example without interrupting the loop.
- Family boundary rule is the most enforceable of the three: "any task solvable without trig computation violates family identity" is a concrete, testable criterion.
- Interaction memo rigorously rejects all four alternative interaction types against the actual math structure, not just theme.

**Weak spots:**
- **Acceptance zone calibration is unresolved and high-stakes.** The 8% radius suggestion is a starting point, not a design answer. A prototype test plan must include a specific protocol for tuning this parameter before release.
- **Monetization is structurally limited.** The concept is better suited to school/district licensing than a consumer app. This is not a fatal weakness, but it must inform go-to-market strategy before additional investment.
- **Early-task purity vulnerability** at axis-aligned angles needs a session-design constraint documented in difficulty scaffolding before level design begins.

**Constraining dimension:** Monetization Potential (2) — structurally limits the viable go-to-market channel to institutional licensing.

**Recommended next action:** Advance to prototyping with a specific acceptance zone tuning protocol in the build spec. Target school/district licensing, not consumer app. Document the non-axis angle pairing rule in the difficulty scaffolding spec before level design.

---

## Cross-Concept Summary

| Concept | Clarity | Purity | Family | Loop | Education | Monetization | Total |
|---|---|---|---|---|---|---|---|
| Bakery (bench_01) | 4 | 4 | 4 | 4 | 4 | 4 | **24/24** |
| Fire Dispatch (bench_02) | 3 | 3 | 3 | 3 | 3 | 3 | **19/24** |
| Unit Circle (bench_03) | 4 | 3 | 4 | 3 | 4 | 2 | **20/24** |

---

## V1 Business Sequencing Guidance

**Strongest concept overall — Bakery (bench_01, 24/24).**
Every dimension is clean. No open design questions at the loop level. Broadest addressable market (K–2 addition), strongest replay hook (customer urgency + timer), and family boundaries that self-govern future commissions. This is the V1 exemplar and the reference case for all future pipeline output evaluation.

**Closest to prototype-ready — Bakery (bench_01), then Fire Dispatch (bench_02).**
Bakery has no unresolved design parameters. Fire Dispatch is ready to prototype at the primary loop level today — the route_and_dispatch loop has no open blockers. Its only blocker before the *family* can accept a second member is the supply mechanic loop spec, which is a parallel task, not a prerequisite for the first prototype.

**Strongest educationally, weaker commercially — Unit Circle (bench_03).**
The pizza-as-unit-circle metaphor is the most intellectually rigorous output the pipeline has produced. The instructional design is the best of the three: structural metaphor, teach-on-fail state, enforceable family boundary. The commercial weakness is structural — narrow HS audience, lab mode, low post-mastery replay. This is a school-licensing product, not a consumer app.

**Recommended sequencing:**
1. **Prototype Bakery first.** Lowest risk, widest market, no open design questions.
2. **Spec Fire Dispatch supply mechanic in parallel** (not after), so the second game is not blocked when the first ships.
3. **Hold Unit Circle** at concept until there is a confirmed institutional sales channel to justify the build investment.

---

## Post-Review Open Items

These items are approved by the pipeline but have open design parameters that must
be resolved before or during prototyping. They are not blockers on the current V1
baseline, but should be tracked before build begins.

| Item | Concept | Owner | Required before |
|---|---|---|---|
| Lock quantity representation mode (pictorial / numeral / mixed) | Bakery (bench_01) | Loop designer | Engineering start |
| Commission allocate_and_balance loop spec for fire dispatch supply mechanic | Fire Dispatch (bench_02) | Loop designer | Level 4+ build |
| Define demand/capacity labeling affordance in UX | Fire Dispatch (bench_02) | UX designer | First prototype pass |
| Document non-axis angle pairing constraint in difficulty scaffolding spec | Unit Circle (bench_03) | Level designer | Level design start |
| Define acceptance zone tuning protocol (starting point: 8% of pizza radius) | Unit Circle (bench_03) | Prototyper | First playtesting round |

---

## Systemic Observation

All three approved loops are genuinely minimal. The pipeline is correctly enforcing the
"no tutorial required" constraint: each teacher shortcut is deployable in under 5 minutes
with zero digital tools, and the first correct action is discoverable within 2–3 failed
attempts without reading any instructions. A concept that requires a tutorial to
understand has not been specified correctly — none of these three require one.
