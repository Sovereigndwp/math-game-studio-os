# V1 Benchmark — Qualitative Review of Approved Outputs

Generated: 2026-04-03
Pipeline mode: LLM (claude-sonnet-4-6)
Rubric: docs/benchmark_rubric.md

---

## bench_01 · strong_elementary_bakery

**Concept:** Grade 2 bakery game — pack pastry orders (addition to 20) before customers leave.
**Job ID:** job_20260403T224434332153Z
**Interaction:** combine_and_build (purity: 0.93)
**Family:** Early-Arithmetic Combine-and-Build: Discrete Object Composition (Ages 5–8) — age_band_specialist

| Dimension | Score | Notes |
|---|---|---|
| Clarity | 4 | "Race against the clock to pack the perfect pastry order by combining the right treats to hit the target number." Single sentence lands instantly. Teacher shortcut (flip two quantity cards, say the sum) is playable in 30 seconds with zero materials. |
| Interaction Purity | 4 | 0.93 purity. `is_action_itself_the_math = true`. No secondary type. Tray selection IS the addition act — no proxy, no gate. The rejected-alternatives section dismantles allocate_and_balance and route_and_dispatch with structural arguments, not preference. |
| Family Placement | 4 | Factory type (age_band_specialist) is correct. Three-part boundary rule is precise: select discrete objects as addends (A), reach a numeric target sum (B), selection equals the arithmetic act (C). Boundary-break examples cover both the symbolic-entry and the subtraction-as-removal failure modes. Overlap warnings correctly call out the universal_ladder adjacency risk and the counting-on / sequence confusion. |
| Loop Quality | 4 | 4 steps max. Signature moment is mechanical and specific: the box snaps shut the instant the running count reaches the target. Fail state (tray reset + timer continues, customer leaves only on time expiry) is instructive without punishing hesitation. Five confusion risks enumerated with concrete causes. Micro-prototype works with 10 index cards and zero digital tools. |
| Educational Value | 4 | Target skill is precise: addition facts within 20, counting on, number bond recognition. Age band 5–8 is exact. Teacher shortcut is classroom-deployable in 2 minutes. Dual representation (numeral label + matching pastry icons on the same tray) scaffolds both numeral readers and counters — this is the right call for Grade 2 without requiring a tutorial branch. |
| Monetization Potential | 4 | Emotional hook (customer urgency) drives repeat play without a separate reward system. Timer pressure is a natural difficulty lever. Family growth path provides three tiers of difficulty (sums to 10 → 20 → multi-addend). Thematic variants (fruit stand, toy shop, aquarium) allow reskin without redesign. Collection hook (happy vs. disappointed customers) is implicit. |
| **TOTAL** | **24/24** | |

**Strengths:**
- Near-perfect structural identity between game action and math operation.
- The running count inside the box is a rare example of in-loop formative feedback that doesn't interrupt play — the math surface is always visible.
- Family boundaries are rigorous enough to govern future game commissions without ambiguity.
- Loop is teachable with a physical prototype in under 30 seconds; this is a strong signal the digital version will also require no tutorial.

**Weak spots:**
- One open decision deferred to prototyping: whether quantity representation is purely pictorial, purely numeral, or mixed. The loop spec resolves this as "numeral label + matching icons" but the interaction_decision_memo notes this could shift the cognitive locus of the math if only icons are shown. Low risk, but needs a final call before engineering begins.
- No explicit wrong-answer feedback beyond tray reset — the running count should prevent most wrong selections, but learners who ignore numerals and select by icon quantity may not understand why their guess failed.

**Recommended next action:** Advance to prototyping. Resolve the representation mode decision in the first prototype build, not before.

---

## bench_02 · strong_middle_fire_dispatch

**Concept:** Grade 3 fire station dispatch game — send the right trucks to the right locations using arithmetic under time pressure.
**Job ID:** job_20260403T224651001833Z
**Interaction:** route_and_dispatch (purity: 0.82) + allocate_and_balance (secondary, staged)
**Family:** Elementary Arithmetic Dispatch and Route — age_band_specialist

| Dimension | Score | Notes |
|---|---|---|
| Clarity | 3 | The primary loop is clear: one incident card, two truck options, pick the right number. Teacher shortcut (demand card + two number cards, point to the match) is excellent. However, the secondary allocate_and_balance mechanic (supply depot) adds scope ambiguity — a designer reading the family brief but not the interaction memo might not know which mechanic to build first. The `interaction_overload_warning` correctly stages them, but this requires the reader to synthesize two documents. |
| Interaction Purity | 3 | 0.82 purity — solid for a concept with a secondary mechanic. Primary loop (arithmetic comparison drives routing) is structurally clean. The secondary type is appropriately flagged as staged (levels 4+) and subordinate. The risk: if the supply mechanic is underspecified at this stage (flagged in the kill report), it may be implemented without sufficient scaffolding at build time, collapsing the staged boundary the memo warns about. |
| Family Placement | 3 | Factory type (age_band_specialist, 8–11) is correct. Boundary rule is precise: (a) elementary arithmetic, (b) route_and_dispatch primary, (c) arithmetic result IS the routing decision. Boundary-break example (fraction gate + pre-labeled button) is airtight. The split_family_warning is handled carefully — family notes document the risk but do not resolve it with a concrete monitoring mechanism (e.g., task distribution tracking). Three overlap warnings are thorough. Universal_ladder adjacency risk is correctly noted. |
| Loop Quality | 3 | 4 steps max, clean loop. Signature moment (truck launches toward incident) is clear. Fail state (truck shakes, does not move, incident persists) is instructive — no penalty screen. The loop deliberately excludes the secondary mechanic, which is the right scope decision. Weak spot: the `expected_time_to_first_correct_action_seconds` is 10 seconds for a loop that requires reading a demand number AND comparing two truck numbers — this may underestimate the cognitive load for learners at the low end of the 8–11 band. Five confusion risks are enumerated, but the risk that learners confuse demand vs. capacity labeling is noted without a design solution. |
| Educational Value | 3 | Arithmetic comparison (find the truck whose number equals the demand) is a clear Grade 3 skill. Age band is appropriate. However, the primary loop as specified uses exact-match comparison only — the simplest valid instance. This is correct for a lowest viable loop, but it doesn't yet exercise the "arithmetic under time pressure" promise in the command (addition and subtraction, not just matching). That escalation belongs to difficulty scaffolding but should be explicitly planned before the first prototype to avoid a bait-and-switch between the concept promise and the implemented skill. |
| Monetization Potential | 3 | Shift model (5 emergencies per shift, rating on speed and accuracy) provides natural session structure. Stakes (emergencies succeed or fail) create emotional investment. Dispatcher role is aspirational for 8–11 year olds. Growth path covers addition → subtraction → early multiplication within the same interaction type. Weaker area: collection and social hooks are not yet defined — the shift model has progression but no visible reward artifact (badges, unlocked trucks, city map) to drive return visits. |
| **TOTAL** | **19/24** | |

**Strengths:**
- The dispatcher profession is a genuine structural fit, not a costume: a real dispatcher's job is exactly "calculate resource fit, then route." This gives the concept unusual teacher legibility — it can be explained as a career simulation, not just a game.
- The interaction_decision_memo's concrete supply mechanic definition ("total water tanks needed = sum of two incident requirements, check against depot stock via subtraction") is the right fix for the kill report's vagueness flag, delivered in the memo itself rather than deferred.
- The family growth path is well-structured: the four difficulty levers (arithmetic complexity, simultaneous incidents, supply mechanic introduction, new professions) are independent and can be turned on individually.

**Weak spots:**
- **Supply mechanic underspecification is load-bearing.** The kill report and interaction memo both flag it. The memo provides a definition but the loop spec correctly excludes it. This means the supply mechanic has been analyzed but not yet loop-designed — there's a gap between the staged introduction promise (level 4+) and any concrete loop spec for what that mechanic actually looks like. This needs a follow-up loop spec before the family can accept a second member.
- **Demand vs. capacity labeling** is the single highest confusion risk and receives no design answer in the loop brief. A learner who doesn't understand that the truck number is a capacity and the card number is a demand will select randomly. The teacher shortcut handles this (three labeled cards, explicit verbal framing) but the digital version has no parallel.
- Split family warning is documented but monitoring is left implicit. A concrete rule (e.g., "if any game in this family allocates more than 30% of tasks to supply calculations, re-evaluate family membership") would be more actionable.

**Recommended next action:** Advance to prototyping with the primary route_and_dispatch loop only. Commission a separate supply-mechanic loop spec before building level 4+. Resolve demand/capacity labeling in the first UX pass.

---

## bench_03 · strong_high_school_unit_circle

**Concept:** High school trigonometry pizza lab — place toppings at (cos θ, sin θ) coordinates on a unit-circle pizza surface.
**Job ID:** job_20260403T224911615850Z
**Interaction:** navigate_and_position (purity: 0.87) + transform_and_manipulate (secondary, staged)
**Family:** Unit Circle Coordinate Positioning Games (High School Trigonometry) — advanced_anchor

| Dimension | Score | Notes |
|---|---|---|
| Clarity | 4 | "Drag a topping to the point (cos θ, sin θ) on the pizza edge" is immediately legible to any HS math student. The pizza-as-unit-circle metaphor is structurally exact, not decorative — a pizza of normalized radius IS a unit circle. Teacher shortcut (draw circle, mark axes, student places a coin at the angle coordinate) is deployable in any classroom with a marker and paper. |
| Interaction Purity | 3 | 0.87 purity — strong. `is_action_itself_the_math = true`. Secondary type (transform_and_manipulate for oven-rotation tasks) is correctly staged and excluded from the MVL. The split_family_warning is acknowledged and mitigated. Small purity deduction is honest: early quadrant-1 tasks at easy angles (e.g., θ = 0, placing topping at (1,0)) can be solved by visual anchoring without trig reasoning, which is a genuine fidelity risk at the low end of the difficulty range. This is called out accurately in the memo's notes. |
| Family Placement | 4 | Factory type (advanced_anchor) is correct — the concept is anchored to a specific abstract domain, not a numerical range. Family boundary rule is the most precise of the three: every member must require evaluation of (cos θ, sin θ) to complete the primary action. The boundary-break examples are excellent — both the "labeled zones" game and the "explicit (x,y) labels" game are correctly identified as boundary violations that remove trig reasoning. Overlap warnings appropriately distinguish this family from coordinate geometry and circular geometry families that share surface similarity but require different math. |
| Loop Quality | 3 | 4 steps max. Signature moment (topping snaps to exact coordinate + coordinate pair flashes) is specific and repeatable. Fail state is instructive — the correct position reveals for 1.5 seconds after a miss, which is the primary teaching mechanism for wrong-answer learners. The `expected_time_to_first_correct_action_seconds` is 25 seconds, which is realistic for trig computation and distinguishes this loop from the younger-age-band loops. Weak spot: the acceptance zone calibration is called out as a risk (8% of pizza radius suggested) but remains unresolved — too tight means repeated early failure; too loose means learners solve by visual estimation without trig. This is the highest-stakes tuning parameter for the game's instructional validity and it has no prototype answer yet. |
| Educational Value | 4 | Target skill is maximally specific: evaluate (cos θ, sin θ) for a given radian angle, use the result to determine a position on the unit circle. Age band (14–18) is exact. The difficulty scaffolding sequence (quadrant 1 canonical angles → full circle → radian arc rotation) maps cleanly onto the standard HS trig curriculum sequence. The lab/structured-practice mode (not timed arcade) is the right default for instructional fidelity. Fail state is designed to teach (correct position reveal) rather than just penalize, which is rare and correct for a concept at this abstraction level. The note that time pressure should be optional, not canonical, is a key instructional design decision that protects the game from becoming a speed test that rewards guessing. |
| Monetization Potential | 2 | Narrower audience than the other two approved concepts — this is inherently a HS trig product, which limits addressable market. Lab/structured-practice mode reduces the casual engagement ceiling. The family growth path (Q1 → full circle → radian arc) is a curriculum sequence, not a game progression — it is educationally sound but lacks the emotional escalation drivers (time pressure, customer stakes, collection) that create non-mandatory return visits. Replay after skill mastery is low; the game's value is concentrated in the learning phase, not after it. No collection or social hook is identified. |
| **TOTAL** | **20/24** | |

**Strengths:**
- The structural metaphor is this concept's primary competitive advantage: the pizza IS the unit circle, not a costume for it. This makes the game immediately explainable to teachers and students without a tutorial, and it makes every placement a genuine math act rather than a gamified worksheet.
- The fail state (correct position reveal for 1.5 seconds) is the strongest instructional mechanism across all three approved concepts — a wrong placement becomes a free worked example without interrupting the loop.
- The interaction_decision_memo's justification for rejecting all four alternatives is the most rigorous of any of the three concepts. Each rejected type is tested against the actual math structure, not just the theme.
- The family boundary rule is enforceable: "any task solvable by visual symmetry, pattern matching, or non-trig estimation without loss of correctness violates the family identity" is a concrete, testable criterion.

**Weak spots:**
- **Acceptance zone calibration is unresolved and high-stakes.** The 8% radius suggestion is a starting point, not a design answer. The game's instructional validity depends on this parameter more than any other single variable — if it's too loose, learners succeed by pointing vaguely at the right quadrant rather than computing the coordinate. A prototype test plan should include a specific protocol for tuning this parameter.
- **Monetization is structurally limited.** The concept is strong educationally but the audience (HS trig students) is narrow and the lab mode reduces entertainment-first play. This is not a fatal weakness — the concept is better suited to school licensing than consumer app — but it should inform go-to-market strategy before any further investment.
- **Early tasks are purity-vulnerable.** θ = 0 → (1, 0) and θ = π/2 → (0, 1) can be placed by visual anchoring on the axes without trig computation. These angles are necessary for orientation scaffolding but should be paired with a second task at a non-axis angle in the same session to prevent learners from building a purely visual strategy.

**Recommended next action:** Advance to prototyping with a specific acceptance zone tuning protocol included in the build spec. Target school/district licensing rather than consumer app. Flag the early-task purity vulnerability to the UX designer before the first round of playtesting.

---

## Cross-Concept Summary

| Concept | Clarity | Purity | Family | Loop | Education | Monetization | Total |
|---|---|---|---|---|---|---|---|
| Bakery (bench_01) | 4 | 4 | 4 | 4 | 4 | 4 | **24/24** |
| Fire Dispatch (bench_02) | 3 | 3 | 3 | 3 | 3 | 3 | **19/24** |
| Unit Circle (bench_03) | 4 | 3 | 4 | 3 | 4 | 2 | **20/24** |

**Overall pattern:**

- **Bench_01 is the V1 exemplar.** Every dimension is clean. It is the reference case for what a fully-specified pipeline output looks like.
- **Bench_02 is production-viable with one follow-up task:** a loop spec for the supply mechanic. The core dispatch loop is ready for prototyping; the secondary mechanic is not. Do not let a developer interpret the family growth path as permission to build both loops simultaneously.
- **Bench_03 is educationally strong but requires a go-to-market reframe.** The instructional design is the best of the three, but the monetization model needs to shift from consumer game to institutional product before investment continues. The acceptance zone calibration is the single highest-priority unresolved technical question.

**Systemic observation:** All three loops are clean at the minimum viable level. The pipeline is correctly enforcing the "no tutorial required" constraint — all three teacher shortcuts and micro-prototypes work without digital tools. This is the most important architectural quality V1 has delivered.
