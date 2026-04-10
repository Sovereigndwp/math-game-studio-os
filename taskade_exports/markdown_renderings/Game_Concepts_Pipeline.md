# Game Concepts Pipeline

# **🚦 Pipeline Entry Process**

1. Ask the Brainstorming Specialist for a new concept brief
2. Brainstorming Specialist outputs a Standardized Concept Brief (title, grade band, skill, family, fantasy, core action, math–mechanism link, ceiling, closest game, gap justification)
3. Add the concept as a new task below using the Intake Template. Set Pipeline Stage → Idea / Concept. Set GO/NO-GO → Pending.
4. Trigger the Brainstorm → Pipeline Review automation. The Game Design Critic runs Stages 1–7 automatically and writes GO/NO-GO, Delight Gate, and AI Critique back to the task fields.
5. If GO: Pipeline Orchestrator routes to Misconception Architect → Prototype Specs. If Revise: address conditions and re-trigger. If NO-GO: archive in place.

# 🎮 Game Concepts

- [ ] Snack Line Shuffle — order kids in a cafeteria line by computing and comparing addition/subtraction totals (K–2, Grades 1–2 core)

  ## P1 Definition of Done

  - [ ] Single-screen cafeteria scene; 2–4 kids; addition within 5 only; largest-first rule only
  - [ ] Drag-to-order + Serve mechanic built; correct → cheer animation; wrong → adjacent misordered pair highlighted with both computed totals shown
  - [ ] Playtest: ≥70% of 6–10 K–2 students explain in own words they're ordering 'from most snacks to least snacks'
  - [ ] Playtest: ≥60% spontaneously compute at least some sums (verbally or with fingers) — not pure guessing
  - [ ] Teacher review: line-ordering metaphor is clear and aligns with K–2 classroom goals for comparing quantities
  - [ ] Serve penalty rule implemented: hint overlay triggers after repeated wrong Serves with no kid movement; first-try correctness rewarded visibly
  - [ ] Game Design Critic reviews P1 pass record before P2A begins

  ## Misconception Risk Register

  - **M1: Bigger-looking addend = bigger total.** Risk: kids order 8+1 before 5+4 by appearance. Mitigation: include counterexamples (8+1 vs 5+4, both = 9); show computed totals side-by-side when misordered.
  - **M2: Equal totals must have different ranks.** Risk: player tries to strictly order equal-total kids. Mitigation: explicit tie episodes; both kids step forward together with announcement 'Same amount!'.
  - **M3: Subtraction always produces a small/losing result.** Risk: player always ranks any subtraction expression last. Mitigation: frequent mixed comparisons where subtraction wins (9–1 vs 4+3); feedback explains 'starting big and taking a little still leaves a lot'.
  - **M4: Leftmost digit dominance.** Risk: kids compare only the first digit they see (e.g., 9-1 vs 4+3, pick 9-1 because '9 is big,' ignoring -1). Design rule: include frequent pairs where a lower first digit wins (e.g., 4+7 vs 9-1); feedback names the comparison explicitly.
  - **M5: Operation sign blindness.** Risk: treating 6+2 and 6-2 as 'same kind of thing,' ordering by number pair only, ignoring the sign. Design rule: include side-by-side expression pairs with identical digits but different signs at every difficulty tier; wrong-order feedback highlights the sign explicitly.
  - **M6: Zero changes nothing — overgeneralized to subtraction.** Risk: player ranks 9-0 same as 9 or incorrectly versus 8+1; zero-subtraction is non-intuitive. Design rule: include 9-0 vs 8+1 and similar pairs explicitly; feedback says 'taking away zero still keeps all of it.'
  - **M7: Bigger number first = bigger result.** Risk: player assumes 9-1 > 1+9 because '9 starts it.' Design rule: include structurally symmetric pairs (e.g., 9-4 vs 4+2) and highlight that starting big with a big minus can leave less than starting small with a plus.
- [ ] Fraction Forge — smelt raw ore using equivalent fraction operations to fill orders in a fantasy blacksmith shop

  ## P1 Definition of Done

  - [ ] Single-screen forge built: 1–2 raw bars, tick marks, cut tool, merge tool
  - [ ] Orders render as fractional targets; correct → forge animation; wrong → mismatch overlay
  - [ ] Playtest: ≥70% of 8–10 testers use forge + math language — not 'just doing fractions'
  - [ ] Playtest: ≥60% continue voluntarily past tutorial with zero extrinsic rewards
  - [ ] Playtest: ≥60% improve by ≥1 item on 6-question equivalence micro-assessment post-play
  - [ ] Educator review: no visual model where 2/6 appears larger than 1/3 — hard stop if fails
- [ ] Echo Heist

  ## Pass Record Summary

  - P1 (Core Loop): WASD stealth, guard AI (patrol/investigate/chase), vision cones, LOS raycasting, math popup as lockpick, vault sequence, escape countdown, 3 classes, 71 tests.
  - P2 (Pressure & Progression): Class abilities (Space — math-gated buffs), gadget (noise maker), Web Audio API, hint system (2 levels, cost scales by district), 30 missions across 3 districts, difficulty config per district, 213 tests.
  - P3 (Feel): Particle system (correct/wrong/vault/mastery), screen shake, guard wall avoidance (moveEntityToward), focus mode (Tab = 25% game speed, 2pts/sec drain, purple vignette), mastery streaks per template, per-skill results breakdown, escape alarm audio.
  - P4 (Content & Scaffolding): Authored D3 missions (10 missions, 12 skill templates from GDD content sheet), F-key scaffold panel (8 visual reference types keyed by template), auto-hint after 2 wrong (free, no cost), mission objectives with +200 bonus, localStorage persistence (high scores, completedMissions), 2 echo charges per run, 304 tests.
  - P5 (Meta & Flair): Class unlock progression (Ghost @5, Runner @10), daily contract (D key, date-seeded), mission select screen (S key, 5×6 grid), ability VFX (purple tint/cyan ring/orange trail), ambient stealth drone (55 Hz triangle, fades in on mission start).

  ## Key Design Learnings for Studio

  - TYPED ANSWERS, NOT MULTIPLE CHOICE: Recall not recognition. Equivalent form acceptance (1/2 = 0.5 = .5, 30% = 0.3) prevents format penalization without lowering cognitive bar.
  - MATH AS THE LOCKPICK RULE: The answer literally opens the door. If you remove the math, you cannot play the game. This is the anti-worksheet-in-costume test — Echo Heist passes it by design.
  - VAULT CANNOT BE ESCAPED: Commitment mechanic — once you reach the loot, you must solve 2-3 chained prompts. Esc is blocked. This creates the 'heist moment' tension that makes math feel consequential.
  - FOCUS MODE AS TACTICAL SCAFFOLD: Tab = slow-time (25% game speed) with a real cost (2pts/sec drain). Gives struggling players a breathing tool without removing pressure. Mastery makes the cost feel smaller.
  - AUTO-HINT AFTER 2 WRONG (FREE): Prevents frustration spirals without removing the H-key paid hint. The two-tier hint system (H-key = costs score; auto = free) is the right balance for age 11-13.
  - MASTERY STREAKS PER TEMPLATE: 3 consecutive correct answers in one skill template = mastery (×1.1 score, 25% hint cost reduction, gold particle burst). Per-skill results breakdown shows color-coded bars — player can see exactly what to practice.
  - F-KEY SCAFFOLD PANEL: 8 visual reference types, keyed by math template (T1-T12). Rate triangle for T7/T8, fraction bars for T5/T6, balance scale for T1/T2, etc. Pops alongside the prompt — never replaces thinking, just reduces working memory load.
  - DAILY CONTRACT (CLIENT-SIDE ONLY): Date-seeded mission + class. Zero server infrastructure. Creates shared challenge — two players on the same date get the same mission. Limitation: not synchronized across timezones.
  - CLASS UNLOCK AS PACING GATE: Hacker always on; Ghost unlocks at 5 missions; Runner at 10. Forces players to learn the system before advanced builds unlock. Progression map visible on menu.
  - AMBIENT STEALTH DRONE (55 Hz): Triangle oscillator fades in on mission start, fades out when escape alarm triggers. Sub-bass tension layer — makes math puzzles feel high-stakes without visual noise. Designed to be heard subconsciously.
- [ ] Metro Minute: Express Line

  ## Pre-P1 Puzzle Designs (Revision #2)

  ## Puzzle 1 — Short Isn't Always Swift

  - Target Misconception: M1 — Shortest distance = fastest time
  - Learning Objective: Shift from 'pick the shorter line on the map' to 'compare total time using t = d ÷ r, even if the longer path is faster'

  Map: 3 stations — North Market (N) → \[Route A: straight, 6 km @ 20 km/h] → East Docks (E). Route B: N → Central Hub (6 km @ 60 km/h) → E (6 km @ 60 km/h). Route A is a single short-looking segment; Route B is a dogleg that visually appears longer.

  Worked Math — Route A: t = 6 ÷ 20 = 0.3 h = 18 min. Fails goal (>15 min). Route B: 6÷60 = 6 min + 6÷60 = 6 min = 12 min total. Passes goal. Key: Route B is 2× the distance but 3× the speed — time is smaller.
  - Constraint: Get VIP from North Market to East Docks in under 15 minutes.
  - The Trap: Route A is a single straight segment — visually screams shortcut. Player picks it; time bar hits 18 min and blows the 15-min goal.
  - The Reveal: 'Even though Route B is twice the distance, the speed is 3× bigger, so the time is smaller.' Before: short line = fast. After: must check both distance AND speed.
  - UI Required: Per-segment hover shows distance + speed label. Live time bar with 15-min goal line. Δt shown on each segment selection.
  - PASS: Player tries Route A, fails, switches to Route B, can say 'the longer one is faster because it's express.'
  - STOP: Player repeatedly picks Route A ignoring speed labels, or says 'the game is wrong' rather than updating reasoning.
  - Progression: Binary route choice, one trap, no chaining yet. Sets up Puzzle 2 (cumulative multi-leg).
- [ ] Probability Pipeline
- [ ] City of Optimal Shapes
- [ ] Snack Line Shuffle **— GO · Prototype P1 Active**

  ## Document Registry — 3 of 3 Complete

  - [x] **Prototype Specifications** — Full P1 build brief (project: 9bfNR2acXuAHiWyC). Scene spec, Option B Serve mechanic (locked), content constraints, grade-band gate, all 14 DoD gates. Status: Spec Ready.
  - [x] **Game Family Registry** — Sequence / Ordering family updated (project: N9S2kjQdv3s7tyya). Snack Line Shuffle listed as first K-2 member; 1.OA.C.6 anchor; 1.NBT.B.3 removed; Coverage → Well Covered.
  - [x] **K-12 Curriculum Map** — New slot created (project: fQKsxPJWgG2kPRoQ). 'Operations & Algebraic Thinking — Compare & Order Computed Totals (K–2, Grade 1 anchor)'. Status: Approved. Grade Band: K-2. Standard: 1.OA.C.6. Coverage: Solid.

  <!---->

  - **Consistency check (2026-04-08):** All three documents agree on standard (1.OA.C.6 only), grade band (K-2, Grade 1 anchor), family (Sequence/Ordering), pipeline status (P1 active), and removal of 1.NBT.B.3 from all public-facing materials. No discrepancies found.

  ## P1 Definition of Done — 14 Gates (see Prototype Specifications for full text)

  *Build gates (1–5): scene built · Option B Serve verified · amber VO approved · K-1 difficulty constrained · Grade 2+ gate enforced*

  *Teacher / educator gates (6, 11, 12): fantasy alignment ≥2 teachers (BLOCKING) · line-ordering review · ordering-direction visual review*

  *Playtest gates (7–10): rule comprehension ≥70% · computation evidence ≥60% · Serve-spam ≤20% · voluntary continuation ≥50%*
  - [x] **Portfolio gate 13** — Game Family Registry updated ✅ 2026-04-08
  - [ ] **Portfolio gate 14** — Game Design Critic reviews P1 pass record before P2A begins

  ## P1 Definition of Done

  - [ ] Single-screen cafeteria: 2-4 kids, addition within 5 only, largest-first rule enforced
  - [ ] Core loop: drag kids into slots -> Serve -> correct (cheers + window animation) OR wrong (misordered pair highlighted, totals shown, verbal hint)
  - [ ] Metrics captured: time per round, Serve-press count, correct-on-first-try (Y/N)
  - [ ] Playtest: >=70% of 6-10 K-2 testers explain the line rule in their own words without prompting
  - [ ] Playtest: >=60% spontaneously compute (verbal or finger-count) rather than randomly Serve
  - [ ] Teacher review: ordering-direction visual (icon + voiceover) is unambiguous for K-2
  - [ ] Misconception check: no cue accidentally implies bigger-looking expression = bigger total without computation
  - [ ] Serve mechanic is Option B: per-placement amber/green adjacency glow; Serve tap is cosmetic only; no totals ever revealed by system — verify this in build before first playtest
  - [ ] Amber feedback includes kid-voice line ('Hey, I think I should go before you!') — no numbers, no totals, no explicit answer — verify copy is age-appropriate for K-2
  - [ ] K-1 difficulty levels constrained to: within 10 only, addition-dominant, 3–4 kids max — verify in level design before build
  - [ ] Grade 2+ gate enforced in content plan: mixed +/–, within 20, 5–6 kids, positional constraints — none of these appear in K-1 levels
  - [ ] Update Game Family Registry: add Snack Line Shuffle as first K-2 member of Sequence / Ordering family; note 1.OA.C.6 as anchor standard; remove 1.NBT.B.3 from all public-facing materials

  ## Next Steps

  - [x] Game Design Critic: full Stages 1-7 review COMPLETE — see AI Critique field for full verdict
  - [x] **✅ RESOLVED — Curriculum Architect confirmed: Primary 1.OA.C.6 VALID. Secondary 1.NBT.B.3 REMOVED (overreach). K-2 slot confirmed open. Grade-band risk: mixed +/– and 5-6 kid lines gated to Grade 2+. Full note in @gcf03.**
  - [ ] Update Game Family Registry: add Snack Line Shuffle as first K-2 member of Sequence / Ordering family
  - [ ] Prototype Engineer: build P1 after Critic confirms GO — cafeteria scene, 2-4 kids, +within-5, Serve loop, metrics capture
  - [ ] **⛔ BLOCKING — Fantasy Alignment Fix (Critic mandatory, must clear before P1 build):** Core Fantasy (@gcf01) and Core Action (@gcf02) have been rewritten to remove all 'fairness' / 'fair turn' language. New framing: player is a kitchen helper who sorts the line so the server portions correctly — no fairness judgment, no 'who deserves more.' Teacher sign-off required: >=2 classroom teachers (K-2) must confirm the new framing (a) does not mis-teach fairness, and (b) is immediately understandable to a 5-8 year old. Gate: do not start P1 build until both sign-offs are logged here.
  - [ ] Add Misconceptions M4-M7 to Misconception Library (project: cyt3zvpjf32D1Ddt) with contrast-set design rules
  - [ ] Add 3 Critic-required P1 metrics to playtest plan: Serve-spam rate (<=20%), voluntary continuation (>=50%), behavioral computation evidence (>=60% observable)
  - [x] **✅ RESOLVED — Serve Mechanic: Option B (per-placement immediate feedback, no probe-Serve).** Global Serve button eliminated as evaluative probe. Per-placement amber/green adjacency glow is the primary feedback mechanism. Serve tap is cosmetic confirmation only. Design Rule locked into @gcf02. Applies P1–P5. Option A (global Serve + penalties) was rejected: it patches a leaky mechanic without closing the computation bypass, adds meta-penalty load inappropriate for K-2, and is misaligned with P1 scope.
- [ ] Puddle Patrol — navigate a rain-soaked garden path by choosing the right directional steps to reach each flower (K-2, Routing / Pathfinding family) — **GO · Prototype P1 Active**

  ## P1 Definition of Done

  - [ ] 4×4 grid scene; 1 flower target; 4–6 static puddle tiles; unlimited arrows; GO button runs frog along placed arrows
  - [ ] Correct path → flower blooms + cheer animation; wrong path (puddle) → frog splashes back to start
  - [ ] Live path trace updates tile-by-tile as arrows are placed (frog ghost preview)
  - [ ] Playtest: ≥70% of 6–10 K-1 students explain rule ('the frog follows my arrows') without prompting
  - [ ] Playtest: ≥60% place arrows in a deliberate pattern (not random drag-and-GO spam)
  - [ ] Playtest: ≥50% voluntarily choose to play at least one extra puzzle after tutorial
  - [ ] Teacher review: directional vocabulary (up/down/left/right) is age-appropriate and unambiguous for K-1
  - [ ] Game Design Critic reviews P1 pass record before P2A begins

  ## Misconception Risk Register

  - **M1: Direction confusion.** Child places ↑ when meaning 'move right.' Mitigation: icons use frog body orientation, not abstract arrows; VO reads direction aloud on tap.
  - **M2: Step-count underestimation.** Path built one step short of flower. Mitigation: live path trace and remaining-steps counter shown as arrows are placed.
  - **M3: Obstacle optimism.** Child routes through a puddle tile hoping the frog will jump it. Mitigation: puddle tiles show splash animation on hover — clear 'impassable' signal before placement.
  - **M4: Reversal blindness.** Child places ← after → and is surprised the frog returns to start. Mitigation: live path trace updates in real time so reversals are visible before GO.
- [ ] Ratio Run — rank recipe ingredient ratios on a number line to serve the right dish at a packed diner (Gr 3–5, Sequence / Ordering — Ratio Edition) — **GO · Prototype P1 Active**

  ## P1 Definition of Done

  - [ ] Single diner scene; 3 recipe cards; same-denominator fractions only (e.g., 1/4, 2/4, 3/4); drag-to-rank on a number-line rail; GO button runs kitchen animation
  - [ ] Correct order → dishes slide to customers with cheer; wrong card → amber highlight + side-by-side fraction bar comparison
  - [ ] Equivalence tie mechanic: if two cards have the same value, both sparkle-lock side-by-side on the rail
  - [ ] Playtest: ≥70% of 6–10 Gr 3–4 students explain rule in own words without prompting
  - [ ] Playtest: ≥60% show evidence of comparing values before dragging (verbal, gesture, or written calculation)
  - [ ] Playtest: ≥50% voluntarily replay at least one extra round
  - [ ] Educator review: fraction bar visual accurately represents all fractions shown (hard stop if 3/4 appears smaller than 1/2 in any visual)
  - [ ] Game Design Critic reviews P1 pass record before P2A begins

  ## Misconception Risk Register

  - **M1: Numerator-only ordering.** Child ranks 3/4 before 2/3 because '4 > 3.' Mitigation: frequent pairs like 3/4 vs 5/6 where larger denominator wins; amber feedback shows side-by-side fraction bar.
  - **M2: Ratio direction confusion.** Child reads 3:1 as smaller than 1:3 by taking only the first number. Mitigation: ratio cards show physical icon-to-icon representation (sauce parts : water parts).
  - **M3: Decimal-fraction disconnect.** Child treats 0.5 and 1/2 as different values. Mitigation: equivalence tie mechanic — matching values sparkle-lock side-by-side, teaching equivalence as a positive discovery.
  - **M4: Unit rate misread.** Child reads '6 servings per 2 cups' as just '6,' ignoring the 'per.' Mitigation: unit rate cards always show a graphical plates-per-cups depiction, not a number pair alone.
- [ ] Signal Tower — build a relay tower network by placing signal boosters at algebraically-determined positions to bridge the dead zone between two cities (Gr 6–8, Build / Craft family) — **GO · Prototype P1 Active**

  ## P1 Definition of Done

  - [ ] Single level: 2 cities, 2 towers, 2 proportional equations (y = mx, b=0); player enters x, game places ghost tower at (x, y)
  - [ ] TRANSMIT: both correct → cities light up; wrong tower → signal gap animation + amber highlight + equation shown on that tower
  - [ ] Coordinate (x, y) displays live as ghost tower hovers; x-axis labeled prominently to prevent axis reversal
  - [ ] Playtest: ≥70% of 6–10 Gr 6–7 students explain 'I substituted x into the equation to find y' without prompting
  - [ ] Playtest: ≥60% show evidence of substituting into equation (paper calculation, verbal steps, or deliberate entry attempts) — not coordinate guessing
  - [ ] Playtest: ≥50% voluntarily attempt a second level without prompting
  - [ ] Educator review: equation notation matches standard Gr 6-7 classroom convention (no non-standard symbols or confusing formatting)
  - [ ] Game Design Critic reviews P1 pass record before P2A begins

  ## Misconception Risk Register

  - **M1: y = mx confusion.** Child adds m + x instead of multiplying. Mitigation: equation displayed with explicit × symbol (y = 3 × x + 2); hint tile shows evaluate-step-by-step with placeholder slots.
  - **M2: Coordinate axis reversal.** Child places tower at (y, x) instead of (x, y). Mitigation: live (x, y) readout tracks pointer; x-axis labeled prominently on both ends.
  - **M3: Visual intersection guessing.** Child estimates where lines cross rather than solving system. Mitigation: constraint lines are hidden by default; player must calculate and place first, then press TRANSMIT to reveal line confirmation.
  - **M4: Single-equation mindset (systems levels).** Child satisfies first constraint but ignores second. Mitigation: partial-satisfaction gives amber signal (not red) to distinguish 'wrong equation' from 'only one constraint met.'
- [ ] Trig Tower — siege cannon game where students solve trig problems to aim and fire at enemy towers (Gr 9–12, Build / Precision-Placement family)
- [ ] Bakery Rush — fill orders by computing the right addition total before the next ticket drops (K–2, addition fluency)
- [ ] Bakery Rush — tap-to-answer oven total game (K–2, Addition Fluency family)

<!---->

- [ ] **📋 INTAKE TEMPLATE — copy this task for each new concept**
  - **Core Fantasy:** \[One sentence — what does the player feel they are doing?]
  - **Core Action:** \[What does the player literally do moment to moment?]
  - **Math–Mechanism Link:** \[How does the math directly cause the game outcome? Remove the math — can you still play?]
  - **Natural Ceiling:** \[Two or three things that can grow in complexity without breaking the loop]
  - **Closest Existing Game:** \[Internal concept + commercial analog + one-sentence differentiation]
  - **Gap / Why Now:** \[Which family gap or underserved grade band does this fill?]
- [ ] Bakery Rush
  - [ ] DoD: Learner band locked (K–2 or Grades 1–3)
  - [ ] DoD: Core Fantasy written in player-voice (1 sentence) → @gcf01
  - [ ] DoD: Core Action written (moment-to-moment verb + 2 sentences) → @gcf02
  - [ ] DoD: CCSS skill code + description → @gcf03; Family assignment confirmed
  - [ ] DoD: Math–mechanism link + natural ceiling (2–3 axes) → @gcf10; Closest game → @gcf08
  - [ ] DoD: Curriculum Architect validates CCSS alignment + grade band fit
- [ ] Fire Dispatch
  - [ ] DoD: Learner band + CCSS code confirmed (Grades 3–5, 3.OA expected)
  - [ ] DoD: Core Fantasy + Core Action written with exact dispatch verb → @gcf01 / @gcf02
  - [ ] DoD: Math–mechanism link written — removing math must make dispatch impossible, not just harder
  - [ ] DoD: Differentiation from Grocery Dash (both Dispatch family) documented → @gcf08
  - [ ] DoD: Curriculum Architect validates grade band + skill slot in K-12 Curriculum Map
- [ ] Unit Circle Pizza Lab
  - [ ] DoD: Learner band + CCSS-HSF code confirmed (9–12, trig)
  - [ ] DoD: Core Fantasy + Core Action written — placement verb is the math act itself → @gcf01 / @gcf02
  - [ ] DoD: Pizza theme confirmed load-bearing OR redesigned so trig drives placement (not decoration)
  - [ ] DoD: Natural ceiling + closest game documented → @gcf10 / @gcf08
  - [ ] DoD: Curriculum Architect confirms 9–12 slot + Precision Placement family fit in K-12 Curriculum Map
- [ ] Power Grid Operator
- [ ] School Trip Fleet
- [ ] Firefly Ranger

## 🏆 Reference Games (Gold Standard)

- [ ] ATC Math Tower

  Here’s where **ATC Math Tower** sits in the pipeline and what’s missing.

  Right now in the Game Concepts Pipeline project, ATC Math Tower is just a **title** with no attached brief or fields filled in. That makes it effectively **Stage 0 (Orchestrator) / undefined**.

  To move it out of “undefined,” we need to complete **Stage 1: Intake Framing** for this concept.

  **1. Pipeline Status for ATC Math Tower**
  - **Concept:** ATC Math Tower
  - **Current Stage:** Stage 0 – Orchestrator (undefined; title only)
  - **Blocking issue:** No intake framing:
    - No learner band
    - No math domain / target skill
    - No world/theme details beyond the title
    - No interaction notes

  Because of that, I can’t run:
  - Kill Test (Stage 2)
  - Interaction Mapper (Stage 3)
  - Family Architect (Stage 4)

  …or anything downstream.

  **2. Next Required Action & Which Agent**

  **Next stage:**
  - **Stage 1 — Intake Framing**

  **Recommended agent:**
  - **Curriculum Architect** (with support from Brainstorming Specialist if needed)

  **What we need defined for ATC Math Tower:**

  Please either answer these directly in Taskade under “ATC Math Tower” or paste answers here and I’ll translate them into a Stage 1 brief:
  1. **Learner Band**
     - e.g., Grades 3–4, 5–6, 7–8, 9–10, or “mixed 5–8”
  2. **Target Math Domain & Subskill**
     - Examples:
       - Ratios & proportional reasoning
       - Integer operations under time pressure
       - Coordinate plane / quadrants
       - Estimation and mental math (sums/differences/products)
       - Linear functions (choose which is appropriate)
     - If you’re unsure, say what you *want players to be better at* after playing (e.g., “quickly comparing two sums in their head”).
  3. **Theme & Fantasy for This Title**
     - Confirm or refine:
       - Is this “Air Traffic Control tower where you route planes safely using math”?
       - Is the math gating: spacing planes (time/distance), fuel, altitude sequencing, etc.?
  4. **Primary Player Action (one verb)**
     - e.g., “route,” “sequence,” “allocate,” “match,” “aim,” “type”

  Once those are set, I’ll:
  1. Run a **Kill Test** on the concept (Stage 2).
  2. If it passes, assign it to a **Game Family** (likely Routing / Sequence, which is a gap we want to fill).
  3. Design the **core loop** and move it toward Prototype Spec.

  **3. Concrete suggestion (so it’s not blank)**

  If you’re happy for me to propose defaults for ATC Math Tower, here’s a strong starting intake framing that fits our identified gaps (Routing / Sequence):
  - **Learner band:** Grades 6–8
  - **Target skill:**
    - Primary: Rate = distance ÷ time, comparing and sequencing arrival times
    - Secondary: Estimating whether a plane can reach a waypoint before/after another given speed and distance
  - **Theme:**
    - Player is an air traffic controller in a busy tower, sequencing arrivals and departures so planes don’t conflict and still hit time windows.
  - **Primary interaction verb:**
    - “Route and sequence” (drag planes to paths/altitudes + choose approach order)

  If you confirm “yes, use that framing,” I’ll treat ATC Math Tower as having **completed Stage 1** and proceed to:
  - Stage 2: Kill Test
  - Stage 3: Interaction Mapper
  - Stage 4: Family Architect

  and report back with:
  - Pass/Fail on Kill Test
  - Chosen interaction family
  - Draft core loop.
- [ ] Grocery Dash
