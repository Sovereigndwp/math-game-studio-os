# Game Family Registry

# 📐 About This Registry

- Each family is an interaction archetype — the felt experience of the player's core action
- Two games in the same family must have high differentiation keys or one should be cut
- Family Architect (Stage 4 of pipeline) assigns every concept to a family before advancement

<!---->

- [ ] Exact-Sum Composition
- [ ] Dispatch / Subset Selection
- [ ] Precision Placement
- [ ] Allocation / Network Balancing
- [ ] Capacity Packing
- [ ] Routing / Pathfinding

  ## Member Games

  - [ ] **Puddle Patrol** — K–2 anchor · Prototype P1 Active
    - **Grade band:** K–1 core (4×4 → 6×6 grids, unlimited arrows, 1 flower target). Grade 2 extension: arrow budget constraint (≤6), dual ordered flower targets, moving puddles.
    - **Anchor standard:** CCSS.MATH.CONTENT.K.G.A.1 — Describe the relative positions of objects using terms such as above, below, beside, in front of, behind, and next to. Arrow placement operationalises positional language as a physical act.
    - **Core action:** Tap or drag directional arrow icons (↑ ↓ ← →) onto empty grid tiles to build a frog's path. Live ghost-trace updates tile-by-tile. Press GO — frog hops. Correct path → flower blooms + cheer. Wrong path (puddle hit) → frog splashes back to start.
    - **Math-as-lockpick:** The sequence of directional steps IS the path. Without correct spatial-directional reasoning the frog cannot reach the flower. Random arrow placement fails on any grid with ≥2 puddles.
    - **Natural ceiling:** Axis 1: Grid size (4×4 → 6×6 → 8×8). Axis 2: Arrow budget (unlimited → 6 → 4 → 3). Axis 3: Path complexity (1 target → 2 ordered targets → waypoint constraint). Ceiling: 8×8 grid, 3-arrow budget, 2 ordered flower targets with mixed static/moving obstacles.
    - **Misconception register:** M1 (direction icon confusion — frog-body orientation required), M2 (step-count underestimation — live trace mitigates), M3 (obstacle optimism — hover splash on puddle tiles), M4 (reversal blindness — live trace is the primary mitigation; non-negotiable in P1 build).
    - **Critical P2A condition:** Arrow budget constraint (≤6 arrows) must be introduced by P2A. Trial-and-error bypass is viable with unlimited arrows. Budget is the single most important depth lever in this game.
    - **Differentiation from Metro Minute:** Puddle Patrol — spatial step-sequencing on a tile grid, K.G.A.1, no numeric calculation. Metro Minute — rate-constrained route optimisation (t = d÷r) across a metro network, Gr 5–7. Different grade band, different math domain, different interaction feel. Zero overlap.
    - **Differentiation from LightBot Jr (commercial):** Puddle Patrol uses drag-to-place per tile (not a command queue), anchors explicitly to K.G.A.1 positional vocabulary, and introduces obstacle-avoidance tension through puddle tiles with hover-splash signals. LightBot frames as programming; Puddle Patrol frames as spatial navigation.
    - **Pipeline status:** GO — Prototype P1 Active (promoted 2026-04-09). Depth Potential: 8/10.
  - [ ] **Metro Minute: Express Line** — Gr 5–7 · PAUSED (3 conditions unresolved)
    - **Grade band:** Grades 5–7 core (D-R-T, unit rates, simple inequalities)
    - **Pipeline status:** PAUSED — 3 design conditions unresolved. Re-evaluate 2026-07-07 (90 days). See Game Concepts Pipeline for full pause conditions and Definition of Done to unpause.
- [ ] Sequence / Ordering

  ## Member Games

  - [ ] **Snack Line Shuffle** — K–2 anchor · Prototype P1
    - **Grade band:** K–2 (K–1 core within 10, addition-dominant, 3–4 kids; Grade 2+ for mixed +/–, within 20, 5–6 kids, positional constraints)
    - **Anchor standard:** CCSS.MATH.CONTENT.1.OA.C.6 — Add and subtract within 20; use strategies to develop fluency. Used here as repeated practice and consolidation context for comparing and ordering expression totals. Does not claim standalone fluency delivery.
    - **Standard removed:** 1.NBT.B.3 (overreach — place-value comparison with >, =, < notation; not targeted by this game). Listed only as a downstream beneficiary in internal notes. Do not include in any public-facing alignment materials.
    - **Core action:** Compute small addition/subtraction expressions on kid trays; drag kids into a line ordered from most snacks to least (or by stated rule); per-placement adjacency glow signals local correctness; Serve tap is cosmetic confirmation only — totals never revealed by system.
    - **Misconception register:** M1 (bigger addend = bigger total), M2 (equal totals must rank differently), M3 (subtraction always loses), M4 (leftmost digit dominance), M5 (operation sign blindness), M6 (zero-subtraction overgeneralisation), M7 (bigger number first = bigger result). M4 and M7 co-occurrence flagged. All seven written to Misconception Library (project: cyt3zvpjf32D1Ddt).
    - **Differentiation from Probability Pipeline:** Snack Line Shuffle — arithmetic expression totals within 20, K–2, cafeteria ordering fantasy. Probability Pipeline — ranking uncertain events by likelihood, Grades 5–6, probability module fantasy. Same family verb (drag-to-rank) but entirely different math domain, representation type, and grade band. No cognitive overlap risk.
    - **Pipeline status:** GO — Prototype P1 (advanced 2026-04-08). Conditions cleared: fantasy alignment fixed, Serve mechanic locked (Option B), CCSS corrected, M4–M7 registered. P1 DoD: 14 checkboxes including teacher sign-off, three playtest thresholds, educator visual review, grade-band gate, and Registry update.
    - **Natural ceiling:** Expression complexity (within 5 → within 10 → mixed +/– → within 20) × line length (2–4 → 5–6 kids) × ordering rule variants (largest-first, smallest-first, partial constraints, ties). Ceiling: 6-kid mixed +/– lines within 20 under positional constraints. Beyond this, multi-step or unknown-addend expressions require a different UI model.
  - [ ] **Probability Pipeline** — Grades 5–6 · REVISE required before P1
    - **Grade band:** Grades 5–6 core (4–7 range)
    - **Anchor standard:** CCSS 7.SP.C.5 — Probability of a chance event is a number between 0 and 1; CCSS 5.NF — Comparing fractions/decimals/percents across representations
    - **Pipeline status:** REVISE — Delight Gate FAIL. P1 mechanic not yet locked. Assigned to Brainstorming Specialist (mechanic lock) → Game Design Critic (Delight Gate re-run). See Game Concepts Pipeline for REVISE Definition of Done.
  - [ ] **Ratio Run** — Gr 3–5 anchor · Prototype P1 Active
    - **Grade band:** Grades 3–5 core (Gr 3 extension: unit fractions 1/2, 1/3, 1/4; Gr 4–5 anchor: mixed-denominator fractions and decimals; Gr 6 ceiling: full ratio notation and unit rates).
    - **Anchor standards:** Primary: 5.NF.B.3 (interpret fractions, reason about ordering). Extension: 6.RP.A.1, 6.RP.A.3 (ratios and proportional relationships). Gr 3 entry: 3.NF.A.3 (fraction equivalence).
    - **Core action:** 3–5 recipe cards appear, each showing a ratio/fraction/unit-rate (potentially in different representations). Player drags cards onto a horizontal number-line rail, left (smallest) to right (largest). Tap GO — kitchen animation fires. Correct: dishes slide to customers with cheer. Wrong: misordered card highlights amber with side-by-side fraction bar comparison.
    - **Signature mechanic — Equivalence tie-lock:** When two cards have the same value (e.g., 1/2 and 0.5), both sparkle-lock side-by-side on the rail with a positive animation. This is the primary mechanism for teaching cross-representation equivalence as a discovery, not a correction. Must be active from P1.
    - **Natural ceiling:** Axis 1: Representation mix (same-denominator → mixed denominators → decimals → unit rates → ratio notation → percentages). Axis 2: Card count (3 → 4 → 5). Axis 3: Equivalence trap density (0% → 15% → 30% rounds contain equivalent cards). Axis 4: Time pressure (untimed → customer-patience meter → rush-hour timer). Ceiling: 5 cards × 5 representations + 30% equivalence traps + timer.
    - **Misconception register:** M1 (numerator-only ordering — amber + fraction bar comparison), M2 (ratio direction confusion — icon-to-icon depiction required), M3 (decimal-fraction disconnect — sparkle tie-lock is the primary mitigation), M4 (unit rate misread — graphical plates-per-cups depiction required).
    - **Critical P1 condition:** P1 content must include at least one cross-representation pair (e.g., 2/4 vs 0.5) even at the simplest tier. Pure same-denominator P1 enables permutation guessing and buries the game's M3 misconception work. Equivalence tie-lock must be active from day one.
    - **Educator hard stop:** Fraction bar visual must accurately represent all fractions shown. No visual where 3/4 appears smaller than 1/2. This is a blocking gate equivalent to Fraction Forge's visual accuracy requirement.
    - **Differentiation from Snack Line Shuffle:** Ratio Run — ordering ratio/fraction/unit-rate values across representations, Gr 3–5, diner fantasy, number-line rail. Snack Line Shuffle — ordering arithmetic expression totals within 20, K–2, cafeteria fantasy, slot-drag. Same family verb (drag-to-rank) but different CCSS cluster, grade band, representation type, and fantasy. Zero cognitive overlap.
    - **Differentiation from Probability Pipeline:** Ratio Run — ordering ratio/fraction values (number/ratio domain, 5.NF/6.RP). Probability Pipeline — ordering probability modules by likelihood (probability domain, 7.SP). Grade band overlap: both touch Gr 5–6. Differentiation: CCSS cluster (number vs probability), visual representation type (number-line rail vs probability slot), and fantasy (diner vs probability plant/pipeline). MEDIUM overlap risk — ensure both are registered distinctly when Probability Pipeline re-enters pipeline.
    - **Pipeline status:** GO — Prototype P1 Active (promoted 2026-04-09). Depth Potential: 8/10.
- [ ] Build / Craft

  ## Family Arc: Gr 4–8 Build / Craft Continuum

  - **Arc structure:** Fraction Forge (Gr 4–6) → Signal Tower (Gr 6–8). Both use the same family verb (calculate → place in construction scene) but at different CCSS clusters. A student who masters Fraction Forge at Gr 6 transitions naturally into Signal Tower at Gr 6–7 with the same construction-as-validation fantasy.
  - **Overlap zone Gr 6:** Both games claim Gr 6. Fraction Forge: Gr 6 ceiling (fraction operations under 4.NF → 6.NS bridge). Signal Tower: Gr 6 anchor (6.EE.B.6, 6.EE.C.9 — evaluate equations). Teachers should use Fraction Forge to consolidate fraction fluency first, then Signal Tower for algebraic extension. Not competitive — sequential.
  - **City of Optimal Shapes (ARCHIVED):** NO-GO as currently framed. Failed: no visceral consequence, no math-as-lockpick core. Signal Tower satisfies both archive conditions. Do NOT reopen City of Optimal Shapes while Signal Tower is active. Rewrite eligibility conditions documented in Game Concepts Pipeline.

  ## Member Games

  - [ ] **Fraction Forge** — Gr 4–6 · Prototype P1 Active — Arc Tier 1
    - **Grade band:** Grades 4–6 core. Gr 4 anchor: equivalent fractions and fraction operations (4.NF). Gr 6 ceiling: fraction division, connecting to ratio reasoning (6.NS).
    - **Anchor standard:** CCSS 4.NF — Equivalent fractions, fraction addition/subtraction, simplification.
    - **Core action:** Smelt raw ore bars by cutting (subdividing into equal parts) and merging (combining equal-sized pieces) to produce exact fractional lengths that fill forge orders. Correct order → forge animation + stamp. Wrong → mismatch overlay showing target vs produced.
    - **Natural ceiling:** Ore bar count (1–2 → 3–4), order complexity (simple equivalents → multi-step with addition/subtraction), fraction range (halves → sixths → twelfths). Ceiling: multi-step orders requiring both cutting and merging across different denominators.
    - **Arc handoff to Signal Tower:** After mastering fraction operations (Gr 6), learner is ready for Signal Tower's algebraic coordinate placement (also Gr 6 anchor). The construction-as-validation pattern is identical: calculate a value → place it in the scene → system confirms.
    - **Pipeline status:** GO — Prototype P1 Active (promoted 2026-04-08). P1 DoD in Prototype Specifications project (9bfNR2acXuAHiWyC).
  - [ ] **Signal Tower** — Gr 6–8 · Prototype P1 Active — Arc Tier 2
    - **Grade band:** Grades 6–8. Gr 6 anchor: evaluate y = mx + b for given x (6.EE.B.6, 6.EE.C.9). Gr 7 extension: find x given y (inverse operations). Gr 8 ceiling: solve 2×2 systems of linear equations (8.EE.C.8a/b). First and only studio game targeting CCSS 8.EE.C.8.
    - **Core action:** Side panel shows terrain equation(s). Player enters x-value AND expected y-value (commitment mechanic — both required before ghost tower appears). System places ghost tower at (x, y). Player confirms placement. Press TRANSMIT — system checks all towers against all constraints. Correct → cities light up. Wrong → signal-gap animation + amber on offending tower with equation shown.
    - **Most critical design constraint:** Player MUST provide both x AND expected y before ghost tower appears. System must NOT auto-evaluate y from entered x. If this constraint is violated the game becomes an iterative coordinate-guesser, not a math game. Non-negotiable from P1.
    - **Natural ceiling:** Axis 1: Equation complexity (y = mx → y = mx + b → 2-equation system). Axis 2: Tower count (2 → 3 → 4 → 5). Axis 3: Constraint type (evaluate for x → find x given y → solve system). Axis 4: Inequality hazard zones. Ceiling: 5-tower network requiring three 2×2 systems plus inequality constraints.
    - **Misconception register:** M1 (y=mx adds instead of multiplies — explicit × symbol + step-by-step hint tile), M2 (axis reversal — live (x,y) readout + prominent axis labels), M3 (visual intersection guessing at systems levels — constraint lines hidden until after TRANSMIT), M4 (single-equation mindset at systems levels — amber partial-signal for one-constraint satisfaction).
    - **City of Optimal Shapes archive note:** Signal Tower satisfies both conditions that caused City of Optimal Shapes to be archived: (1) immediate visceral consequence (dead signal, dark city), (2) math-as-lockpick (coordinate cannot be guessed reliably). Do not reopen City of Optimal Shapes while Signal Tower is active.
    - **Depth Potential:** 9/10 — highest of all three new GAP concepts. Richest mastery arc in the studio.
    - **Pipeline status:** GO — Prototype P1 Active (promoted 2026-04-09). CCSS 8.EE.C.8 coverage: first game in studio portfolio to address systems of linear equations.
- [ ] Stealth-Gated Precision Solve
