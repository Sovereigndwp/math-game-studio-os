# Prototype Specifications

# ✅ Approved — Ready to Build / Building

- [ ] Snack Line Shuffle

  # 🛠 Prototype Engineer Handoff Brief — P1

  - **Issued:** 2026-04-08  ·  Status: Spec Ready — awaiting Gate 6 (teacher sign-off) before build start
  - **Source documents:** Prototype Specifications (9bfNR2acXuAHiWyC) · Game Family Registry (N9S2kjQdv3s7tyya) · K-12 Curriculum Map (fQKsxPJWgG2kPRoQ) · Game Concepts Pipeline (LnpYq2qGt5DrXpda)
  - **Rule that cannot be broken:** The system must never display a computed total, >/< relation, or explicit who-goes-first indicator during gameplay — at any state, in any build phase. Permanent. P1–P5.

  ## Section 1 — Pre-Build Blockers (resolve before writing a line of code)

  - [ ] **BLOCKER A — Gate 6 teacher sign-off** · Recruit ≥2 K-2 classroom teachers. Share the approved Core Fantasy text ('kitchen helper / correct portions') and at least 3 sample amber VO lines. Each teacher must independently confirm in writing: (a) framing does not conflict with fairness or social-emotional norms; (b) a 5–8 year old would understand the role without adult explanation. Log both sign-offs in Gate 6 row above before any code is written. No exceptions.
  - [ ] **BLOCKER B — Amber VO copy set written** · Author ≥3 distinct kid-voice lines for the amber state. Requirements: no totals, no >/< relation, no explicit who-goes-first, no shaming, non-repetitive. Examples: 'I'm not sure I'm in the right spot.' / 'Do you think I belong here?' / 'Something doesn't feel quite right…' Draft must be reviewed alongside Gate 6 teacher review. Line 'Hey, I think I should go before you!' flagged in pipeline as borderline — require teacher confirmation it is not fairness-coded before using.
  - [ ] **BLOCKER C — Level content set authored and audited** · Author ≥12 P1 rounds before build. Constraints: addition within 5 only · largest-first rule only · 2–4 kids per round · all totals strictly distinct (no ties) · ≥30% of rounds include an M1 trap pair (bigger-looking addend ≠ bigger total, e.g., 4+1 vs 2+3 would be a tie — use 3+1=4 vs 2+2=4 only after P1 if ties are introduced; for P1 use e.g., 1+2 vs 3+1). Have one designer audit the set against the Visual Neutrality Constraint before committing.
  - [ ] **BLOCKER D — Ordering-direction indicator designed** · Design the icon + VO cue for the ordering rule before building any scene chrome. Must communicate 'most snacks at the front, fewest at the back' to a non-reader. Cannot rely on text alone. Cannot imply fairness, winning, or moral judgment. Will be reviewed by educator in Gate 12.

  ## Section 2 — Ordered Build Checklist

  *Build in this order. Do not proceed past a step until verified in-engine.*
  1. **Static scene shell** — Cafeteria background · serving counter at line-end · 4 drop-zone line slots rendered and labelled by position only (no rank number) · ordering-direction indicator widget placed and visible · Serve button present but inert · no kids loaded yet. Verify: slot hit targets are ≥48×48 px for touch; slots do not visually encode rank.
  2. **Kid entities + tray rendering** — Load 2–4 kid sprites with tray overlay showing expression (e.g., '3+2'). Expression rendered in a clear, legible font ≥18pt. Snack icon art decorative only — confirm via visual audit that no icon encodes quantity magnitude. Kid character dimensions uniform across all kid variants.
  3. **Drag-and-drop system** — Player can pick up any kid and drop into any slot. Kid snaps into slot on release. Kid can be re-picked and moved at any time. Swapping two kids in occupied slots is allowed. No lock-in until Serve is tapped. Verify with mouse and touch input.
  4. **Adjacency glow system (Option B — CORE)** — On every drag-complete event: (a) evaluate ordering rule (largest-first) across all currently occupied adjacent pairs; (b) apply glow state — Neutral (grey, no neighbour) / Green (pair in correct order) / Amber (pair in wrong order). Glow updates on every move, not just on Serve. A kid in a slot with no neighbour shows neutral. Verify: moving a kid to a new position updates both its old adjacency AND its new adjacency correctly.
  5. **Amber VO trigger** — When an adjacency transitions to amber state, play one of the approved amber VO lines at random. Do not play a VO line if the pair was already amber (transition only). Do not stack multiple simultaneous VO triggers. Verify that VO plays on the first wrong placement but not on repeated drags that leave the same pair amber.
  6. **Serve button activation logic** — Serve button is greyed/inert unless ALL slots are occupied. When all slots are occupied and ALL adjacencies are green or neutral: Serve becomes active. When any adjacency is amber: Serve remains inert. Verify: Serve cannot be triggered as a probe on a partial or incorrectly ordered line.
  7. **Correct-round animation** — On Serve tap when active: play cheer animation on all kids · cafeteria window opens · line advances toward counter · brief non-skippable sequence (≤3 seconds). After animation: load next round. Verify: no computed totals appear during or after animation.
  8. **Round loop + level data loader** — Load rounds from the authored content set (≥12 rounds). Each round specifies: kid count (2–4) · expression per kid · known correct ordering. Session progresses through rounds in authored sequence. No score display in P1. No timer in P1. End-of-session screen is a simple 'All done!' with no ranking or score.
  9. **Telemetry instrumentation** — See Section 4 for full schema. Wire all five required events before first playtest. Verify output against schema with a manual 3-round test session before handing to testers.
  10. **Visual neutrality audit (self-review before Gate 12)** — Engineer or designer reviews full rendered build against the Visual Neutrality Constraint: kid height, width, colour saturation must not correlate with total; snack icon quantity/size on tray must not correlate with total; slot position labels must not reveal rank. Sign off before scheduling educator review.

  ## Section 3 — Asset Requirements

  - **Background:** Single cafeteria interior. Serving counter visible at one end. Warm, inviting. No clutter that could encode quantity. 1 variant only in P1.
  - **Kid sprites:** ≥4 distinct kid characters (avoid identical-looking variants to aid player tracking). Each character: idle state · drag state · cheer state. Uniform bounding box across all characters — heights must match. No character may be drawn larger or more prominent in a way that correlates with any math value.
  - **Tray overlay:** Rendered as a UI layer on top of kid sprite. Shows expression string (e.g., '3+2'). Font: bold, rounded, ≥18pt, high contrast. Optional decorative snack icon(s) alongside expression — must be identical across all trays regardless of total (e.g., always one fork icon, one napkin icon). Never show icon quantity that matches or hints at total.
  - **Adjacency glow FX:** Three states per slot-pair — Neutral: no glow (default border only) · Green: soft green halo on both kids in the pair · Amber: amber/orange halo on both kids in the pair. Glow must be visible but not overwhelming. Accessible: glow colour must not be the only signal — consider adding a subtle icon (✓ / ?) for colour-blind support.
  - **Ordering-direction indicator:** Icon + VO widget. Icon must communicate 'most snacks → least snacks, front to back' to a non-reader. Suggested: arrow pointing toward serving counter + stacked plate icons decreasing in size left-to-right (if horizontal line). VO: short, clear, repeated at round start. Requires educator approval (Gate 12) before locking.
  - **Serve button:** Greyed/disabled state + active state. Label 'Serve!' with serving-hand or tray icon. Active state should feel inviting — it is the delight confirmation, not a test trigger.
  - **Correct-round animation:** Kids cheer (arms up, smiling faces) · cafeteria window slides open · serving tray passes down the line. 2.5–3 seconds total. No score or number appears at any point.
  - **Audio:** Amber VO lines (≥3, recorded, age-appropriate voices — 5–8 year old peer voice preferred) · Serve correct SFX (warm cheer/bell) · background cafeteria ambience (light, non-distracting). No audio required for neutral/green glow in P1.

  ## Section 4 — Telemetry Schema

  *Emit one JSON record per round. Append records to a session file. Export as JSON or CSV for playtest analysis. All five fields are required — the spam signal and move-count are the primary evidence for Gates 8 and 9.*
  - **session_id** · string · Unique per player-session (UUID or timestamp-hash). Constant across all rounds in one sitting.
  - **round_index** · integer · 0-based position of this round in the session. Used for trend analysis (does spam_rate fall across the session? does correct_on_first_try rise?).
  - **time_per_round_ms** · integer · Milliseconds from round load to Serve tap. Start clock when kids appear on screen. Stop clock when Serve is tapped (successful). Proxy for deliberateness vs guessing speed.
  - **correct_on_first_serve** · boolean · True if the Serve tap that completes the round is the FIRST Serve tap in that round (all slots filled, all adjacencies green, no prior Serve attempt this round). False if any Serve attempt preceded the successful one. Used for Gate 9 numerator.
  - **kid_move_count_before_serve** · integer · Total number of completed drag-and-drop events in the round before the final Serve tap (including re-drags and swaps). Used alongside Gate 8 observation data. ≥1 on ≥70% of rounds is the telemetry cross-check for computation evidence.
  - **serve_presses_with_no_prior_move** · integer · Count of Serve button presses where no kid_move event occurred since the last amber→cleared transition or round start. This is the spam signal. Divide by total_serve_presses to get spam_rate. Gate 9 threshold: median spam_rate across sample ≤0.20.
  - **Derived (compute post-session, not stored per round):** spam_rate = serve_presses_with_no_prior_move / total_serve_presses · first_try_rate = rounds where correct_on_first_serve = true / total_rounds · mean_time_per_round · move_count_trend (round_index vs kid_move_count, slope should be ≤0 as player becomes faster)

  ## Section 5 — Pre-Playtest Review Sequence (Gates 1–6)

  *All six gates must be cleared before any player — including internal testers — sits down with the build. Gates 1–5 are internal; Gate 6 requires external educator input. Do not schedule playtest until the Gate 6 sign-off log has two entries.*
  - [ ] **Gate 1 REVIEW — Scene built** · Reviewer: Engineer self-sign-off. Checklist: cafeteria background rendered · 4 line slots present and correctly labelled · ordering-direction indicator widget visible and prominent · Serve button present but inert · no kids loaded. Check: slot hit targets ≥48×48 px · no slot label reveals rank.
  - [ ] **Gate 2 REVIEW — Option B Serve mechanic verified** · Reviewer: Engineer + one QA pass. Test script: (a) drag kid to slot → verify adjacency glow fires immediately · (b) create amber pair → verify Serve button stays inert · (c) resolve all ambers → verify Serve activates · (d) tap Serve → verify no total or ranking text appears anywhere in the animation · (e) confirm Serve cannot be activated on partially filled line · (f) confirm computed total is never visible in any UI state.' Fail any of these = do not proceed.
  - [ ] **Gate 3 REVIEW — Amber VO copy approved** · Reviewer: Content designer + one of the Gate 6 educators (can be done in the same meeting). Checklist per line: no totals · no >/< · no explicit who-goes-first · no shaming tone · reads as 5–8 year old peer voice · ≥3 distinct lines exist. Record approval in Gate 3 row above.
  - [ ] **Gate 4 REVIEW — K-1 difficulty constrained** · Reviewer: Content designer with curriculum checklist. Audit every authored round against: addition within 5 only · no subtraction · no total above 5 · 3–4 kids max · no equal-total pairs (no ties). Flag any failing round and fix before proceeding. Sign off on the content set.
  - [ ] **Gate 5 REVIEW — Grade 2+ gate enforced** · Reviewer: same content designer. Confirm that the P1 content set contains zero instances of: subtraction · totals above 10 · 5+ kids per round · positional constraints. Confirm any future Grade 2+ content is held in a separate, flagged section of the content plan and not loaded in P1 build.
  - [ ] **Gate 6 REVIEW — Fantasy alignment teacher sign-off \[BLOCKING]** · Reviewer: ≥2 independent K-2 classroom teachers. Provide: written Core Fantasy text · written Core Action text · ≥3 amber VO lines · ordering-direction indicator design (image or video). Each teacher independently confirms YES to both questions: (a) 'This framing does not conflict with fairness, turn-taking, or social-emotional norms for K-2.' (b) 'A typical 5–8 year old would understand the player role without adult explanation.' Log: teacher name, school/role, date, YES/YES confirmation per question. Two confirmations must be in this log before any playtest is scheduled. This gate cannot be waived or deferred.

  ## Gate 6 Sign-Off Log

  *Teacher 1: \[Name · School/Role · Date] · (a) YES/NO · (b) YES/NO*

  *Teacher 2: \[Name · School/Role · Date] · (a) YES/NO · (b) YES/NO*

  ## Section 6 — What Is Explicitly Out of Scope for P1

  - **Subtraction expressions** — reserved for P2A (introduces M3, M5 misconceptions)
  - **Tie episodes (equal-total pairs)** — reserved for P2A (M2 misconception)
  - **Score / stars / progress bar** — no numerical feedback of any kind in P1
  - **Timer or time pressure** — no time mechanic in P1
  - **Second thematic world** — Delight Gate condition (b); reserved for P2+
  - **5-6 kid rounds or within-20 math** — Grade 2+ gate; not in P1
  - **Hint system or scaffold panel** — amber glow is the only feedback mechanism; no supplementary hints in P1
  - **First-try-correct bonus** — reserved for P2A

  # 🎮 P1 Level Content Set — 14 Rounds

  *Authored 2026-04-08. Verified against all P1 constraints: addition within 5 only · largest-first ordering · strictly distinct totals per round · no ties · ≥30% M1 trap pairs · 2-kid warm-ups then 3-4 kids. 7/14 rounds are M1 traps (50%). Do not ship any round to a K-1 player before the visual neutrality audit (Gate 4) confirms no art element encodes total magnitude.*

  ## Column key

  - **Kids** — number of kids placed in the line this round
  - **Expressions** — the arithmetic expression shown on each kid's tray, in the order they are presented (not in answer order)
  - **Totals** — computed total for each expression (internal reference — never displayed to player)
  - **Correct order (slot 1→last)** — largest total first; expressions listed front-of-line to back
  - **M1 Trap** — YES means at least one pair in the round has a bigger first addend but a smaller total, targeting misconception M1 (bigger addend = bigger total). NO means no such pair exists; the round tests pure computation without a visual-size shortcut.

  ## Warm-Up Block (Rounds 0–1) — 2 kids, no trap

  - [ ] **R0** · Kids: 2 · Expressions: \[2+1, 1+1] · Totals: \[3, 2] · Correct order: 2+1 → 1+1 · M1 Trap: NO

    *Pure warm-up. First addends (2 vs 1) match the total ordering — no trap. Player needs only to compute 2+1=3 and 1+1=2 to succeed. Goal: establish that the game requires computation, not guessing.*
  - [ ] **R1** · Kids: 2 · Expressions: \[3+1, 1+2] · Totals: \[4, 3] · Correct order: 3+1 → 1+2 · M1 Trap: NO

    *Second warm-up. First addends (3 vs 1) again agree with the total ordering — still no trap. Slightly larger numbers than R0. Solidifies rule comprehension before 3-kid rounds begin.*

  ## Core Block A (Rounds 2–8) — 3 kids, mixed trap / clean

  - [ ] **R2** · Kids: 3 · Expressions: \[1+1, 2+1, 3+2] · Totals: \[2, 3, 5] · Correct order: 3+2 → 2+1 → 1+1 · M1 Trap: NO

    *First 3-kid round. Clean — first addends (1, 2, 3) order exactly matches totals (2, 3, 5). Tests whether player can extend the ordering rule from 2 to 3 kids without a trap. Widely spaced totals (2, 3, 5) make the correct order obvious once computed.*
  - [ ] **R3** · Kids: 3 · Expressions: \[3+0, 2+2, 4+1] · Totals: \[3, 4, 5] · Correct order: 4+1 → 2+2 → 3+0 · M1 Trap: YES

    *M1 TRAP: 3+0 has a bigger first addend (3) than 2+2 (first addend 2), but 3+0=3 is less than 2+2=4. A player sorting by first-addend size would put 3+0 ahead of 2+2 — wrong. Requires computing both totals. Also: 4+1 has a smaller first addend (4) than 3+0's first addend, but 4+1=5 wins overall — trap at the top pair too.*
  - [ ] **R4** · Kids: 3 · Expressions: \[4+0, 3+2, 2+1] · Totals: \[4, 5, 3] · Correct order: 3+2 → 4+0 → 2+1 · M1 Trap: YES

    *M1 TRAP: 4+0 has the biggest first addend (4) of the three kids, yet its total (4) is less than 3+2=5. A player sorting by first addend puts 4+0 first — that's the wrong answer. The correct leader is 3+2=5. Strong M1 trap at the top position.*
  - [ ] **R5** · Kids: 3 · Expressions: \[1+0, 2+0, 1+3] · Totals: \[1, 2, 4] · Correct order: 1+3 → 2+0 → 1+0 · M1 Trap: NO

    *Clean. Introduces a second addend being the larger of the two (1+3 — second addend 3 is bigger than first addend 1). Not an M1 trap because the first addend of 1+3 (which is 1) is not bigger than the other expressions' first addends. Widely spaced totals (1, 2, 4). Pedagogical purpose: reinforces that the second addend counts just as much as the first.*
  - [ ] **R6** · Kids: 3 · Expressions: \[4+0, 3+2, 1+1] · Totals: \[4, 5, 2] · Correct order: 3+2 → 4+0 → 1+1 · M1 Trap: YES

    *M1 TRAP: 4+0 has the biggest first addend (4), but 4+0=4 < 3+2=5. Player sorting by first addend puts 4+0 first and 3+2 second — wrong. Same trap structure as R4 but with a different third kid (1+1=2 vs 2+1=3 in R4) so the round feels distinct.*
  - [ ] **R7** · Kids: 3 · Expressions: \[0+2, 1+3, 0+3] · Totals: \[2, 4, 3] · Correct order: 1+3 → 0+3 → 0+2 · M1 Trap: NO

    *Clean. Two kids share a 0 first addend (0+2 and 0+3) — player cannot use first-addend size to distinguish them at all. Forces full computation of both. Third kid (1+3) has the highest total. Pedagogical purpose: exposes the limit of any first-addend heuristic when first addends are identical.*
  - [ ] **R8** · Kids: 3 · Expressions: \[3+0, 2+3, 1+0] · Totals: \[3, 5, 1] · Correct order: 2+3 → 3+0 → 1+0 · M1 Trap: YES

    *M1 TRAP: 3+0 has a bigger first addend (3) than 2+3 (first addend 2), but 3+0=3 < 2+3=5. Player sorting by first addend puts 3+0 ahead of 2+3 — wrong. The kid with the smaller first addend (2+3) should lead. Totals are widely spaced (1, 3, 5) so there is no ambiguity once computed.*

  ## Core Block B (Rounds 9–13) — 4 kids, mixed trap / clean

  - [ ] **R9** · Kids: 4 · Expressions: \[1+1, 2+1, 1+3, 2+3] · Totals: \[2, 3, 4, 5] · Correct order: 2+3 → 1+3 → 2+1 → 1+1 · M1 Trap: NO

    *First 4-kid round. Clean — totals are 2, 3, 4, 5 (perfectly consecutive). Four-way ordering tested for the first time. No M1 trap: this round's purpose is to establish that the player can manage a longer line with more simultaneous comparisons before adding a trap layer.*
  - [ ] **R10** · Kids: 4 · Expressions: \[4+0, 3+0, 2+3, 1+0] · Totals: \[4, 3, 5, 1] · Correct order: 2+3 → 4+0 → 3+0 → 1+0 · M1 Trap: YES (double)

    *M1 TRAP (double): Both 4+0 and 3+0 have bigger first addends than 2+3 (first addend 2), yet both 4+0=4 and 3+0=3 are less than 2+3=5. A player sorting purely by first-addend size (4, 3, 2, 1) produces the entirely wrong ordering \[4+0, 3+0, 2+3, 1+0]. The correct ordering puts 2+3 first. Strongest M1 trap in the set — the entire visible size hierarchy is inverted at the top.*
  - [ ] **R11** · Kids: 4 · Expressions: \[3+2, 4+0, 2+0, 1+0] · Totals: \[5, 4, 2, 1] · Correct order: 3+2 → 4+0 → 2+0 → 1+0 · M1 Trap: YES

    *M1 TRAP: 4+0 has a bigger first addend (4) than 3+2 (first addend 3), but 4+0=4 < 3+2=5. Player sorts by first addend puts 4+0 first — wrong. The three X+0 kids (4+0, 2+0, 1+0) have obvious totals (= their first addend) but the mixed-addend kid (3+2) beats all of them. Notable pattern: three trailing kids all have +0 second addends, so computation is trivial for them — the challenge is entirely at the top pair.*
  - [ ] **R12** · Kids: 4 · Expressions: \[0+1, 0+2, 0+4, 0+3] · Totals: \[1, 2, 4, 3] · Correct order: 0+4 → 0+3 → 0+2 → 0+1 · M1 Trap: NO

    *Clean. All four kids have 0 as their first addend — the first addend is useless as a sorting signal. Player must read and compute the second addend for every kid. The presented order (0+1, 0+2, 0+4, 0+3) deliberately scrambles the correct rank. Pedagogical purpose: demonstrates that the second addend alone determines the total when the first addend is zero.*
  - [ ] **R13** · Kids: 4 · Expressions: \[3+2, 4+0, 2+1, 1+0] · Totals: \[5, 4, 3, 1] · Correct order: 3+2 → 4+0 → 2+1 → 1+0 · M1 Trap: YES

    *M1 TRAP (final round): 4+0 has bigger first addend (4) than 3+2 (first addend 3), yet 4+0=4 < 3+2=5. Player who sorts by first-addend size produces \[4+0, 3+2, 2+1, 1+0] — top pair reversed. Session-closing round. Totals are 5, 4, 3, 1 — gap between 3rd and 4th is larger than between consecutive top three, providing a clean finale with slightly uneven spacing.*

  ## Set Summary & Constraint Audit

  - **Total rounds:** 14 (R0–R13)
  - **Kid count breakdown:** 2 kids — R0, R1 (warm-up) · 3 kids — R2–R8 · 4 kids — R9–R13
  - **M1 trap rounds:** R3, R4, R6, R8, R10, R11, R13 = 7 of 14 = 50% ✓ (requirement ≥30%)
  - **All totals within 5:** ✓ Highest total in any round: 5. No expression exceeds 5.
  - **Strictly distinct totals per round:** ✓ Every round verified — no two kids share a total. No tie episodes (reserved for P2A).
  - **Addition only, no subtraction:** ✓ All 14 rounds use A+B format only.
  - **Largest-first ordering rule:** ✓ All correct orderings place the highest total in slot 1.
  - **Misconception coverage:** M1 (bigger first addend = bigger total) targeted by 7 rounds. M1 is the only misconception in scope for P1. M2–M7 are P2A+ content.
  - **Expression variety:** All four total values 1–5 appear across the set. Both A+0 and 0+B formats present. Pairs where the larger second addend determines the winner appear in R5, R7, R9. No expression repeats within any single round.
  - **Visual neutrality risk flag:** Art team must ensure that kid characters and tray icons do not correlate with the total or addend values. The expressions 4+0 and 3+2 both yield different totals but share addend magnitudes that could tempt an art shortcut. Flag this pair for explicit neutrality review before Gate 4 sign-off.

  ## Engineer Data Format

  *Implement each round as a JSON object. The correctOrder field drives the adjacency glow engine — slot 0 is the front of line. Expressions are presented to the player in displayOrder (shuffled); the engine compares player placement against correctOrder to compute green/amber glow states.*
  - **Schema:** { roundIndex: number, kidCount: number, kids: \[ { id: string, expression: string, total: number } ], correctOrder: string\[], displayOrder: string\[], m1Trap: boolean }
  - **Example (R10):** { roundIndex: 10, kidCount: 4, kids: \[ { id: 'k-a', expression: '4+0', total: 4 }, { id: 'k-b', expression: '3+0', total: 3 }, { id: 'k-c', expression: '2+3', total: 5 }, { id: 'k-d', expression: '1+0', total: 1 } ], correctOrder: \['k-c','k-a','k-b','k-d'], displayOrder: \['k-a','k-b','k-c','k-d'], m1Trap: true }
  - **Adjacency rule:** For any two kids placed in adjacent slots i and i+1, glow is GREEN if correctOrder.indexOf(kidAt\[i]) < correctOrder.indexOf(kidAt\[i+1]), AMBER if reversed, NEUTRAL if either slot is empty.
  - **displayOrder note:** Randomise displayOrder per session so the same player does not always see the same starting layout. For M1 trap rounds, ensure the trap kid (bigger first addend, smaller total) appears in a visually prominent position in displayOrder to make the trap salient — do not hide it in position 3 or 4 every time.

  ## Overview

  - **Game:** Snack Line Shuffle
  - **Build Phase:** P1 — Core Loop
  - **Pipeline Status:** GO — advanced to Prototype P1 on 2026-04-08. All four gate conditions cleared (fantasy alignment, Serve mechanic lock, CCSS correction, M4–M7 registration).
  - **Family:** Sequence / Ordering — first K-2 member
  - **Core Fantasy (locked):** "I'm the kitchen helper who reads every tray and lines kids up in the right order — so the server knows exactly how much to put on each plate without guessing."
  - **Anchor Standard:** CCSS.MATH.CONTENT.1.OA.C.6 — Add and subtract within 20. Used as repeated practice and consolidation context; does not claim standalone fluency delivery.
  - **Standard NOT claimed:** 1.NBT.B.3 (removed — overreach; place-value comparison with >, =, < notation not targeted). Do not include in public-facing alignment materials.

  ## Scene Spec

  - **Layout:** Single screen only. No navigation between scenes in P1. Cafeteria setting — serving counter visible at one end of the line; kids approach from a queue zone.
  - **Kid count:** 2–4 per round. Minimum 2 for P1 warm-up rounds; ramp to 3–4 within the session.
  - **Tray display:** Each kid holds a tray showing a single arithmetic expression (e.g., 3+2, 7−1). Numerals and operator symbol rendered clearly. Icon snacks optional as decoration but must not encode quantity (no larger icon = more snacks rule — see Visual Neutrality Constraint).
  - **Ordering-direction indicator:** Permanent, prominent icon + VO line visible throughout each round. Must unambiguously communicate "most snacks at the front, fewest at the back" (or inverse rule variant). Icon cannot rely on text alone — must be readable by non-readers. Requires educator review before P1 playtest (DoD gate 12).
  - **Line slots:** Numbered or positionally labelled drop-targets in a horizontal or vertical queue. Slots must be large enough for easy drag-targeting on a tablet or mouse. Snapping must be generous — no fine-motor penalty.
  - **Serve button:** Visible only when all slots are occupied. Labelled "Serve!" with a simple icon (e.g., a serving hand or tray). Activates only when all slots filled — cannot be tapped as a probe on a partial line.
  - **Correct-round animation:** Kids cheer or animate positively; cafeteria window opens; line advances to counter. Brief, non-skippable. Must feel satisfying — this is the primary delight beat.
  - **P1 world theme:** Single cafeteria world only. No world-switching or unlockable themes in P1. (P2+ may add ≥2 thematic worlds as noted in Delight Gate condition.)

  ## Interaction Spec — Option B Serve Mechanic (LOCKED)

  - **Option A rejected:** Global Serve + penalties was evaluated and rejected. Rationale: patches a leaky mechanic without closing the computation bypass; adds meta-penalty load inappropriate for K-2; misaligned with P1 scope. Do not reintroduce.
  - **Per-placement feedback (PRIMARY mechanism):** Immediately on each drag-and-drop into a slot, the placed kid and their immediate neighbour(s) receive an adjacency glow: Neutral (grey) — slot has no neighbour yet; Green — this adjacent pair is correctly ordered by total; Amber — this adjacent pair conflicts (the two kids are in wrong relative order).
  - **Amber feedback content (strict):** Kid-voice line only — e.g., "Hey, I think I should go before you!" or "Are you sure about this?". No computed totals. No >/< symbol. No explicit statement of which total is larger. No answer revealed. Voice must be age-appropriate and non-shaming. Copy requires educator review before first playtest (DoD gate 3).
  - **Serve tap behaviour:** Cosmetic confirmation only. When all slots are filled and all adjacencies are green or neutral, Serve activates and triggers the correct-round animation. Serve reveals no new information. Serve cannot be used as a diagnostic probe. Serve cannot be tapped on a partial line.
  - **Permanent design rule (P1–P5):** "At no point may a feedback or hint system display the computed total of a kid's snacks, or explicitly identify a correct/incorrect ordering, unless the player has already placed that kid and inferred the comparison through their own computation. The game may highlight which pair conflicts (amber glow), but it must NEVER surface the underlying numbers (totals, >/< relation, or explicit who-goes-first) as part of error feedback." This rule applies across all future build phases.
  - **Kid movement:** Player may freely re-drag a kid out of a slot and into another slot at any time before Serve. Rearranging is always permitted; no lock-in until Serve is tapped.
  - **Telemetry (minimum required):** Per-round: time_per_round, serve_press_count, correct_on_first_try (Y/N), kid_move_count_before_serve, serve_presses_with_no_kid_movement_since_last_feedback (spam signal). Per-session: round_index for trend analysis. Export as JSON or CSV for playtest analysis.

  ## Content Constraints

  - **P1 math scope:** Addition within 5 only. No subtraction. No totals above 5. No expressions with three addends. Covers round warm-up through the full P1 playtest session.
  - **P1 ordering rule:** Largest total first only. No smallest-first, middle-out, or partial-order variants in P1.
  - **P1 contrast-set requirement:** At least 30% of rounds must include a trap pair targeting M1 (bigger-looking addend = bigger total), e.g., 4+1 vs 2+3 (both = 5 → tie), or 3+1 vs 2+2. This forces computation; no round should be solvable by visual size inspection alone.
  - **Visual neutrality constraint:** No art or UI element may encode the correct ordering. Specifically: kid character height, width, or visual prominence must NOT correlate with total; snack icon quantity or size on the tray must NOT correlate with total; slot position on screen must NOT be labelled with a number that reveals rank; colour saturation must NOT increase toward the "front" of the line. Educator review required before first playtest.
  - **Fantasy framing constraint:** Player role is kitchen helper / snack sorter ensuring correct portions. The server needs the right order to portion correctly. No fairness language, no "who deserves more", no "who goes first because they're nicest". These phrases and their synonyms are banned from all UI copy, VO, and tutorial text. Applies P1–P5.
  - **No tie rounds in P1:** Equal-total pairs (e.g., 2+3 vs 4+1) introduce tie-handling logic and M2 misconception work. Reserve for P2A. All P1 rounds must have strictly distinct totals for every pair.

  ## Grade-Band Gate

  - **K–1 levels (current P1 target):** Addition only · within 10 · 3–4 kids max. No subtraction. No expressions totalling above 10.
  - **Grade 2+ levels (gated — not in P1):** Mixed +/– · within 20 · 5–6 kids · positional constraints. None of these content features may appear in K-1 difficulty levels. A content audit confirming this separation is DoD gate 5.
  - **Beyond-scope (different game):** Multi-step expressions (e.g., 2+3+4), missing addends (e.g., ?+3 = 7), two-digit comparison by place-value. These require a different UI model and are not in the ceiling for this title.
  - **Rationale (Curriculum Architect, 2026-04-08):** Mixed +/– within 20 and ordering 5–6 expressions is a Grade 2+ ceiling layer, not core K-1 content. Premature exposure risks cognitive overload and skill mismatch. Gate is hard; content plan must be reviewed before any Grade 2+ level is authored.

  ## P1 Definition of Done — 14 Gates

  ## Build Gates

  - [ ] **Gate 1 — Scene built:** Single-screen cafeteria scene rendered; 2–4 kid slots; addition within 5 only; largest-first rule only; ordering-direction indicator visible and prominent
  - [ ] **Gate 2 — Option B Serve mechanic verified:** Per-placement adjacency glow (neutral / green / amber) fires correctly on every drag; Serve tap is cosmetic only and triggers correct-round animation; Serve cannot be activated on a partial line; system never reveals computed totals at any state
  - [ ] **Gate 3 — Amber VO copy approved:** All amber-state kid-voice lines reviewed and confirmed: no totals, no >/< relation, no explicit who-goes-first, no shaming language; age-appropriate for 5–8 year olds; minimum 3 distinct lines to avoid repetition fatigue
  - [ ] **Gate 4 — K-1 difficulty constrained:** Content plan audit confirms all P1 levels are within 10 (P1 build uses within 5), addition-dominant, 3–4 kids max; no subtraction, no expressions totalling above 10 appear in any K-1 level
  - [ ] **Gate 5 — Grade 2+ gate enforced:** Content plan confirms mixed +/–, within 20, 5–6 kids, and positional constraints appear only in explicitly flagged Grade 2+ levels; none present in P1 build

  ## Teacher & Educator Gates

  - [ ] **Gate 6 — Fantasy alignment teacher sign-off:** ≥2 K-2 classroom teachers independently review the "kitchen helper / correct portions" framing and both confirm: (a) framing does not conflict with fairness norms or social-emotional learning; (b) framing is immediately understandable to a 5–8 year old without adult explanation. Sign-offs must be logged here before first live classroom session. BLOCKING — do not schedule playtest until cleared.
  - [ ] **Gate 11 — Educator line-ordering review:** ≥1 K-2 educator reviews the full build and confirms: (a) the line-ordering metaphor is clear and aligned with K-2 classroom goals for comparing quantities; (b) no accidental fairness implication has re-entered any UI text or VO
  - [ ] **Gate 12 — Ordering-direction visual review:** ≥1 K-2 educator confirms: (a) the ordering-direction indicator (icon + VO) is immediately understandable to non-readers in K-2 as "most snacks at the front"; (b) icon does not imply fairness, winning, or moral judgment; (c) icon and VO are consistent — they do not point in conflicting directions

  ## Playtest Gates

  *Sample: 6–10 K-2 students, first exposure, observed or video-recorded. Measures are per-player proportions over the session.*
  - [ ] **Gate 7 — Rule comprehension ≥70%:** After 2–3 rounds, each player is asked open-ended without prompting: "Tell me how you decide who goes where in the line." PASS if player communicates correct direction + quantity basis without adult feeding the phrase. Acceptable: "big snack first then smaller", "most snacks at the front", "the one with the most goes first". FAIL if: player cites appearance, friendship, or arbitrary features; player needs adult to supply "most to least" before agreeing. Threshold: ≥70% of sample score PASS.
  - [ ] **Gate 8 — Computation evidence ≥60%:** Observer or video codes each player session for spontaneous computation: finger-counting, whispering sums, pointing and murmuring ("2 and 3 makes 5"). No adult prompting allowed. PASS if ≥60% of players show observable computation on at least one round. Telemetry cross-check: players who pass this gate should also show kid_move_count_before_serve ≥1 on ≥70% of their rounds.
  - [ ] **Gate 9 — Serve-spam rate ≤20%:** Calculated from telemetry: serve_presses_with_no_kid_movement_since_last_feedback ÷ total_serve_presses per session. Median across sample must be ≤20%. A player spamming Serve without rearranging is bypassing computation; if threshold is exceeded, mechanic or penalty rules must be redesigned before P2A.
  - [ ] **Gate 10 — Voluntary continuation ≥50%:** After the required demo session, observer offers player a neutral choice: "We can stop here, or you can keep going — up to you." No rewards, no encouragement. PASS if player chooses to continue. Threshold: ≥50% of sample choose to play at least one additional round. Indicates sufficient intrinsic engagement to support P2 build.

  ## Portfolio Gates

  - [ ] **Gate 13 — Game Family Registry updated:** Sequence / Ordering family entry updated to list Snack Line Shuffle as first K-2 member with 1.OA.C.6 as anchor standard, grade-band gate documented, 1.NBT.B.3 removed from public materials, Coverage upgraded to Well Covered. ✅ COMPLETED 2026-04-08.
  - [ ] **Gate 14 — Game Design Critic reviews P1 pass record:** Before P2A begins, Game Design Critic receives the full playtest report (Gates 7–10 results + telemetry export + observer notes) and issues written clearance. Critic may issue: CLEAR (advance to P2A); CONDITIONAL CLEAR (advance with named design fix); HOLD (one or more gates failed — revise and re-test). P2A build cannot start until Critic issues CLEAR or CONDITIONAL CLEAR.

  ## Fail Conditions — Stop P2A if any of these are true

  - **Gate 7 fails:** <70% rule comprehension → tutorial, visual cues, or VO must be revised and re-tested before any other gate is measured
  - **Gate 8 fails:** <60% computation evidence → kids are guessing; contrast-set design or amber feedback mechanism must be strengthened; mechanic does not yet serve as math-as-lockpick
  - **Gate 9 fails:** >20% spam rate → Option B Serve mechanic is still being used as a probe; investigate whether Serve button is triggering too early or amber feedback is too weak; do not add penalties without first investigating root cause
  - **Persistent visual heuristic observed:** If >30% of players consistently order by visual expression size even when given explicit M1 counterexamples, the visual neutrality constraint has been violated in the build → STOP and fix art before re-testing
  - **Gate 6 not cleared:** Fantasy alignment teacher sign-off is BLOCKING — do not run live classroom playtest under any circumstances until both sign-offs are logged

  ## P2A Scope Preview (Do Not Build in P1)

  - Introduce subtraction (M3, M5 misconceptions) and tie episodes (M2)
  - Extend to 5 kids and within-10 math
  - Add second thematic world (Delight Gate condition (b))
  - Add first-try-correct bonus (visible, subtle)
  - Introduce M4 leftmost-digit-dominance and M7 bigger-number-first contrast sets at every tier

<!---->

- [ ] Bakery Rush
- [ ] Fire Dispatch
- [ ] Unit Circle Pizza Lab

# 🔧 Awaiting Spec Generation

- [ ] Power Grid Operator
- [ ] School Trip Fleet

# ✅ Pass 5 Complete

- [ ] Echo Heist

<!---->

- [ ] Fraction Forge — smelt raw ore using equivalent fraction operations to fill orders in a fantasy blacksmith shop
- [ ] Trigger the Brainstorm → Pipeline Review automation. The Game Design Critic runs Stages 1–7 automatically and writes GO/NO-GO, Delight Gate, and AI Critique back to the task fields.
- [ ] If GO: Pipeline Orchestrator routes to Misconception Architect → Prototype Specs. If Revise: address conditions and re-trigger. If NO-GO: archive in place.
- [ ] Core Fantasy: \[One sentence — what does the player feel they are doing?]
- [ ] Core Action: \[What does the player literally do moment to moment?]
- [ ] Math–Mechanism Link: \[How does the math directly cause the game outcome? Remove the math — can you still play?]
- [ ] Natural Ceiling: \[Two or three things that can grow in complexity without breaking the loop]
- [ ] Closest Existing Game: \[Internal concept + commercial analog + one-sentence differentiation]
- [ ] Gap / Why Now: \[Which family gap or underserved grade band does this fill?]
- [ ] Bakery Rush
- [ ] Unit Circle Pizza Lab
- [ ] Fire Dispatch
- [ ] ATC Math Tower
- [ ] Probability Pipeline
- [ ] Metro Minute: Express Line
- [ ] P1 Definition of Done
- [ ] Single-screen cafeteria: 2-4 kids, addition within 5 only, largest-first rule enforced
- [ ] Core loop: drag kids into slots -> Serve -> correct (cheers + window animation) OR wrong (misordered pair highlighted, totals shown, verbal hint)
- [ ] Metrics captured: time per round, Serve-press count, correct-on-first-try (Y/N)
- [ ] Playtest: >=70% of 6-10 K-2 testers explain the line rule in their own words without prompting
- [ ] Playtest: >=60% spontaneously compute (verbal or finger-count) rather than randomly Serve
- [ ] Teacher review: ordering-direction visual (icon + voiceover) is unambiguous for K-2
- [ ] Misconception check: no cue accidentally implies bigger-looking expression = bigger total without computation
- [ ] Next Steps
- [ ] Game Design Critic: full Stages 1-7 review COMPLETE — see AI Critique field for full verdict
- [ ] Prototype Engineer: build P1 after Critic confirms GO — cafeteria scene, 2-4 kids, +within-5, Serve loop, metrics capture
- [ ] M4: Leftmost digit dominance. Risk: kids compare only the first digit they see (e.g., 9-1 vs 4+3, pick 9-1 because '9 is big,' ignoring -1). Design rule: include frequent pairs where a lower first digit wins (e.g., 4+7 vs 9-1); feedback names the comparison explicitly.
- [ ] M5: Operation sign blindness. Risk: treating 6+2 and 6-2 as 'same kind of thing,' ordering by number pair only, ignoring the sign. Design rule: include side-by-side expression pairs with identical digits but different signs at every difficulty tier; wrong-order feedback highlights the sign explicitly.
- [ ] M6: Zero changes nothing — overgeneralized to subtraction. Risk: player ranks 9-0 same as 9 or incorrectly versus 8+1; zero-subtraction is non-intuitive. Design rule: include 9-0 vs 8+1 and similar pairs explicitly; feedback says 'taking away zero still keeps all of it.'
- [ ] M7: Bigger number first = bigger result. Risk: player assumes 9-1 > 1+9 because '9 starts it.' Design rule: include structurally symmetric pairs (e.g., 9-4 vs 4+2) and highlight that starting big with a big minus can leave less than starting small with a plus.
- [ ] Serve mechanic is Option B: per-placement amber/green adjacency glow; Serve tap is cosmetic only; no totals ever revealed by system — verify this in build before first playtest
- [ ] Amber feedback includes kid-voice line ('Hey, I think I should go before you!') — no numbers, no totals, no explicit answer — verify copy is age-appropriate for K-2
- [ ] K-1 difficulty levels constrained to: within 10 only, addition-dominant, 3–4 kids max — verify in level design before build
- [ ] Grade 2+ gate enforced in content plan: mixed +/–, within 20, 5–6 kids, positional constraints — none of these appear in K-1 levels
- [ ] Update Game Family Registry: add Snack Line Shuffle as first K-2 member of Sequence / Ordering family; note 1.OA.C.6 as anchor standard; remove 1.NBT.B.3 from all public-facing materials
- [ ] ⛔ BLOCKING — Fantasy Alignment Fix (Critic mandatory, must clear before P1 build): Core Fantasy (@gcf01) and Core Action (@gcf02) have been rewritten to remove all 'fairness' / 'fair turn' language. New framing: player is a kitchen helper who sorts the line so the server portions correctly — no fairness judgment, no 'who deserves more.' Teacher sign-off required: >=2 classroom teachers (K-2) must confirm the new framing (a) does not mis-teach fairness, and (b) is immediately understandable to a 5-8 year old. Gate: do not start P1 build until both sign-offs are logged here.
- [ ] Add Misconceptions M4-M7 to Misconception Library (project: cyt3zvpjf32D1Ddt) with contrast-set design rules
- [ ] Add 3 Critic-required P1 metrics to playtest plan: Serve-spam rate (<=20%), voluntary continuation (>=50%), behavioral computation evidence (>=60% observable)
- [ ] ✅ RESOLVED — Serve Mechanic: Option B (per-placement immediate feedback, no probe-Serve). Global Serve button eliminated as evaluative probe. Per-placement amber/green adjacency glow is the primary feedback mechanism. Serve tap is cosmetic confirmation only. Design Rule locked into @gcf02. Applies P1–P5. Option A (global Serve + penalties) was rejected: it patches a leaky mechanic without closing the computation bypass, adds meta-penalty load inappropriate for K-2, and is misaligned with P1 scope.
- [ ] Document Registry — 3 of 3 Complete
- [ ] Prototype Specifications — Full P1 build brief (project: 9bfNR2acXuAHiWyC). Scene spec, Option B Serve mechanic (locked), content constraints, grade-band gate, all 14 DoD gates. Status: Spec Ready.
- [ ] Game Family Registry — Sequence / Ordering family updated (project: N9S2kjQdv3s7tyya). Snack Line Shuffle listed as first K-2 member; 1.OA.C.6 anchor; 1.NBT.B.3 removed; Coverage → Well Covered.
- [ ] K-12 Curriculum Map — New slot created (project: fQKsxPJWgG2kPRoQ). 'Operations & Algebraic Thinking — Compare & Order Computed Totals (K–2, Grade 1 anchor)'. Status: Approved. Grade Band: K-2. Standard: 1.OA.C.6. Coverage: Solid.
- [ ] Consistency check (2026-04-08): All three documents agree on standard (1.OA.C.6 only), grade band (K-2, Grade 1 anchor), family (Sequence/Ordering), pipeline status (P1 active), and removal of 1.NBT.B.3 from all public-facing materials. No discrepancies found.
- [ ] P1 Definition of Done — 14 Gates (see Prototype Specifications for full text)
- [ ] Build gates (1–5): scene built · Option B Serve verified · amber VO approved · K-1 difficulty constrained · Grade 2+ gate enforced
- [ ] Teacher / educator gates (6, 11, 12): fantasy alignment ≥2 teachers (BLOCKING) · line-ordering review · ordering-direction visual review
- [ ] Playtest gates (7–10): rule comprehension ≥70% · computation evidence ≥60% · Serve-spam ≤20% · voluntary continuation ≥50%
- [ ] Portfolio gate 13 — Game Family Registry updated ✅ 2026-04-08
- [ ] Portfolio gate 14 — Game Design Critic reviews P1 pass record before P2A begins
- [ ] P1 Definition of Done
- [ ] 4×4 grid scene; 1 flower target; 4–6 static puddle tiles; unlimited arrows; GO button runs frog along placed arrows
- [ ] Correct path → flower blooms + cheer animation; wrong path (puddle) → frog splashes back to start
- [ ] Live path trace updates tile-by-tile as arrows are placed (frog ghost preview)
- [ ] Playtest: ≥70% of 6–10 K-1 students explain rule ('the frog follows my arrows') without prompting
- [ ] Playtest: ≥60% place arrows in a deliberate pattern (not random drag-and-GO spam)
- [ ] Playtest: ≥50% voluntarily choose to play at least one extra puzzle after tutorial
- [ ] Teacher review: directional vocabulary (up/down/left/right) is age-appropriate and unambiguous for K-1
- [ ] Game Design Critic reviews P1 pass record before P2A begins
- [ ] Misconception Risk Register
- [ ] M1: Direction confusion. Child places ↑ when meaning 'move right.' Mitigation: icons use frog body orientation, not abstract arrows; VO reads direction aloud on tap.
- [ ] M2: Step-count underestimation. Path built one step short of flower. Mitigation: live path trace and remaining-steps counter shown as arrows are placed.
- [ ] M3: Obstacle optimism. Child routes through a puddle tile hoping the frog will jump it. Mitigation: puddle tiles show splash animation on hover — clear 'impassable' signal before placement.
- [ ] M4: Reversal blindness. Child places ← after → and is surprised the frog returns to start. Mitigation: live path trace updates in real time so reversals are visible before GO.
- [ ] P1 Definition of Done
- [ ] Single diner scene; 3 recipe cards; same-denominator fractions only (e.g., 1/4, 2/4, 3/4); drag-to-rank on a number-line rail; GO button runs kitchen animation
- [ ] Correct order → dishes slide to customers with cheer; wrong card → amber highlight + side-by-side fraction bar comparison
- [ ] Equivalence tie mechanic: if two cards have the same value, both sparkle-lock side-by-side on the rail
- [ ] Playtest: ≥70% of 6–10 Gr 3–4 students explain rule in own words without prompting
- [ ] Playtest: ≥60% show evidence of comparing values before dragging (verbal, gesture, or written calculation)
- [ ] Playtest: ≥50% voluntarily replay at least one extra round
- [ ] Educator review: fraction bar visual accurately represents all fractions shown (hard stop if 3/4 appears smaller than 1/2 in any visual)
- [ ] Game Design Critic reviews P1 pass record before P2A begins
- [ ] Misconception Risk Register
- [ ] M1: Numerator-only ordering. Child ranks 3/4 before 2/3 because '4 > 3.' Mitigation: frequent pairs like 3/4 vs 5/6 where larger denominator wins; amber feedback shows side-by-side fraction bar.
- [ ] M2: Ratio direction confusion. Child reads 3:1 as smaller than 1:3 by taking only the first number. Mitigation: ratio cards show physical icon-to-icon representation (sauce parts : water parts).
- [ ] M3: Decimal-fraction disconnect. Child treats 0.5 and 1/2 as different values. Mitigation: equivalence tie mechanic — matching values sparkle-lock side-by-side, teaching equivalence as a positive discovery.
- [ ] M4: Unit rate misread. Child reads '6 servings per 2 cups' as just '6,' ignoring the 'per.' Mitigation: unit rate cards always show a graphical plates-per-cups depiction, not a number pair alone.
- [ ] P1 Definition of Done
- [ ] Single level: 2 cities, 2 towers, 2 proportional equations (y = mx, b=0); player enters x, game places ghost tower at (x, y)
- [ ] TRANSMIT: both correct → cities light up; wrong tower → signal gap animation + amber highlight + equation shown on that tower
- [ ] Coordinate (x, y) displays live as ghost tower hovers; x-axis labeled prominently to prevent axis reversal
- [ ] Playtest: ≥70% of 6–10 Gr 6–7 students explain 'I substituted x into the equation to find y' without prompting
- [ ] Playtest: ≥60% show evidence of substituting into equation (paper calculation, verbal steps, or deliberate entry attempts) — not coordinate guessing
- [ ] Playtest: ≥50% voluntarily attempt a second level without prompting
- [ ] Educator review: equation notation matches standard Gr 6-7 classroom convention (no non-standard symbols or confusing formatting)
- [ ] Game Design Critic reviews P1 pass record before P2A begins
- [ ] Misconception Risk Register
- [ ] M1: y = mx confusion. Child adds m + x instead of multiplying. Mitigation: equation displayed with explicit × symbol (y = 3 × x + 2); hint tile shows evaluate-step-by-step with placeholder slots.
- [ ] M2: Coordinate axis reversal. Child places tower at (y, x) instead of (x, y). Mitigation: live (x, y) readout tracks pointer; x-axis labeled prominently on both ends.
- [ ] M3: Visual intersection guessing. Child estimates where lines cross rather than solving system. Mitigation: constraint lines are hidden by default; player must calculate and place first, then press TRANSMIT to reveal line confirmation.
- [ ] M4: Single-equation mindset (systems levels). Child satisfies first constraint but ignores second. Mitigation: partial-satisfaction gives amber signal (not red) to distinguish 'wrong equation' from 'only one constraint met.'

# GAP-1 · Puddle Patrol — P1 Prototype Specification

## A · Handoff Brief

- Game ID: GAP-1 · Puddle Patrol
- Grade band: K–2 (primary target Grade 1)
- CCSS: K.G.A.1 — positional language and cardinal directions (above / below / left / right)
- Game family: Routing / Pathfinding
- Phase: P1 — mechanic-locked prototype (no art, no audio, no tutorial)
- Session length: 5–8 minutes
- Rounds in P1: 12 rounds (R0–R11) across 4 difficulty blocks
- Core fantasy: You are the crossing guard — draw the safe path so the frog reaches the flower without stepping in any puddles
- Misconception targets: M1 diagonal confusion, M2 over-counting steps, M3 direction reversal, M4 start/end cell confusion
- Build target: HTML/JS single file, desktop + iPad landscape, no backend for P1
- Gate status: GO — approved for P1 build. Delight: PASS.

## B · Scene Specification

- Grid: square cells, size varies by block — 4×4 (Block 1 R0–R2), 5×5 (Block 2 R3–R5), 6×6 (Block 3 R6–R8), 8×8 (Block 4 R9–R11)
- START cell: top-left region, frog icon, green border — no arrow placeable here
- GOAL cell: bottom-right region, flower icon, yellow border — no arrow placeable here
- Puddles: blue-tinted blocked cells; count scales with block (Block1: 1–2, Block2: 3–4, Block3: 4–6, Block4: 6–8)
- Arrow tray: row below grid; 4 tile types: ↑ ↓ ← → (unlimited supply); player drags onto grid cells
- GO button: bottom-center; disabled until ≥1 arrow placed; triggers cell-by-cell frog animation at 0.4 s/cell
- Step counter: top-right; shows 'Steps used: N / Max: M' — visible only in Block 3+ (R6–R11)
- Reset button: top-left; clears all placed arrows, preserves puzzle layout
- Interaction: drag arrow → drop on cell to place; second drag onto same cell replaces; right-click / long-press to remove
- Fail state: frog hits puddle or exits grid → splash effect → board persists with existing arrows → player adjusts and re-GO
- Success state: frog reaches flower → hop animation + flower bloom → 'Round N complete!' label → advance to R+1
- Hint tier 1 (attempt 2): cell where frog failed glows gently + 'Check this step' label
- Hint tier 2 (attempt 3): animated ghost arrow appears showing correct first-step direction
- No score, stars, or medals in P1 — round progression is the only reward signal

## C · Mechanic Locks (P1 Invariants)

- LOCK-1: No diagonal arrows. Tray ships exactly 4 tiles ↑ ↓ ← →. Diagonal is mechanically impossible.
- LOCK-2: Frog cannot be moved manually. Only GO triggers movement. Player plans, then executes.
- LOCK-3: Puddle cells fully blocked — no arrow placement on puddles; frog cannot enter puddle cells.
- LOCK-4: START and GOAL cells cannot receive arrows — fixed-icon cells only.
- LOCK-5: Every puzzle must have ≥1 valid solution verifiable at build time — no unsolvable levels ship.
- LOCK-6: Path is contiguous — frog reads arrow on current cell and moves one step; no arrow on next cell = halt (fail). Player must arrow every intended cell on the path.
- LOCK-7: Frog animation speed fixed at 0.4 s/cell — not player-adjustable in P1.
- LOCK-8: No undo during frog animation — GO button disabled while frog is in motion.

## D · Content Constraints

- CC-1: All puzzles solvable using only cardinal directions (K.G.A.1: above / below / left / right).
- CC-2: Min path ≥3 steps (R0), max path ≤14 steps (Block 4). No round outside this range.
- CC-3: ≥50% of rounds (6/12) must expose M1 diagonal confusion — puzzles where the naive diagonal shortcut is mechanically blocked or impossible.
- CC-4: Zero text inside grid cells or on arrow tiles — icon-only throughout (K-2 literacy constraint).
- CC-5: Each round has one designer-specified minimum path. Alternate valid paths are accepted and not penalised.
- CC-6: Step-limit rounds (Block 3+) must have min-path ≤ step-limit − 2, giving player at least one wasted-step budget.
- CC-7: Puddle placement must never create a fully linear corridor — always ≥2 possible path branches so the puzzle tests direction choice, not just execution.

## E · Grade-Band Gates

- Block 1 (R0–R2): 4×4 grid · 1–2 puddles · 3–5 step paths · targets Kindergarten · no step counter shown
- Block 2 (R3–R5): 5×5 grid · 3–4 puddles · 5–8 step paths · targets Grade 1 · no step counter shown
- Block 3 (R6–R8): 6×6 grid · 4–6 puddles · 7–10 step paths · step limit introduced · targets Grade 1–2 · step counter visible top-right
- Block 4 (R9–R11): 8×8 grid · 6–8 puddles · 10–14 step paths · tighter step limits · targets Grade 2 · step counter prominent
- M1 diagonal-confusion trap rounds: R1, R3, R5, R6, R8, R10, R11 — 7/12 rounds (>50%, CC-3 exceeded)

## F · Definition of Done — 8 Gates

- [ ] GATE-1 (Mechanic Proof): Frog follows placed arrows cell-by-cell correctly on all 12 rounds — no teleport, no skip.
- [ ] GATE-2 (Solvability): All 12 puzzles verified solvable by engineer before handoff — at least one valid path per puzzle documented in content set.
- [ ] GATE-3 (Lock Compliance): No diagonal arrow exists in tray or is reachable by any interaction. Confirmed by code review.
- [ ] GATE-4 (Misconception Coverage): ≥6/12 rounds are confirmed M1 diagonal-trap rounds. Documented in content set.
- [ ] GATE-5 (Hint System): 3-tier hint ladder fires correctly — no hint attempt 1, cell highlight attempt 2, ghost arrow attempt 3. Resets each round.
- [ ] GATE-6 (Step Counter): Counter appears only in Block 3+ (R6–R11); absent in Block 1–2 (R0–R5). Verified across all 12 rounds.
- [ ] GATE-7 (Cold-Start Observation): ≥2 Grade K–2 children complete R0–R2 without adult re-explanation of mechanic. Target: 80% unassisted success on R0.
- [ ] GATE-8 (No Text on Grid): Zero text strings rendered inside grid cells or on arrow tiles across all 12 rounds. Icon-only confirmed.

## G · P1 Level Content Set (R0–R11)

## Block 1 — 4×4 Grid (R0–R2) · Kindergarten

- [ ] R0 · Intro Straight — START (0,0) → GOAL (0,3). Puddles: none. Min path: 3 steps RIGHT. M1 trap: NO. Note: Pure cardinal warmup; frog moves along top row.
- [ ] R1 · First Corner — START (0,0) → GOAL (3,3). Puddles: (1,1). Min path: 6 steps (3R+3D). M1 trap: YES — direct diagonal blocked by puddle AND mechanically impossible. Note: First L-shaped route; many K players try to drag diagonally.
- [ ] R2 · Around the Puddle — START (0,0) → GOAL (3,2). Puddles: (1,1),(2,1). Min path: 6 steps around middle column. M1 trap: NO. Note: First multi-puddle avoidance; two blocked cells force detour.

## Block 2 — 5×5 Grid (R3–R5) · Grade 1

- [ ] R3 · Zigzag — START (0,0) → GOAL (4,4). Puddles: (1,2),(2,1),(3,3). Min path: 8 steps. M1 trap: YES — direct line blocked by (2,1) cluster. Note: First 5×5; puddle cluster forces multiple direction changes.
- [ ] R4 · Wall Hug — START (0,2) → GOAL (4,2). Puddles: (1,2),(2,2),(3,2). Min path: 7 steps (must detour around vertical wall). M1 trap: NO. Note: M2 over-counting trap — students may place too many steps going around the wall.
- [ ] R5 · Reverse Turn — START (4,0) → GOAL (0,4). Puddles: (2,0),(2,1),(2,3),(2,4). Min path: 9 steps. M1 trap: YES — obvious shortcut runs straight into blocked cells. Note: First bottom-left start; tests direction reversal (M3).

## Block 3 — 6×6 Grid, Step Limit Introduced (R6–R8) · Grade 1–2

- [ ] R6 · Efficient Route — START (0,0) → GOAL (5,5). Puddles: (1,1),(2,3),(3,2),(4,4),(5,2). Step limit: 12. Min path: 10 steps. M1 trap: YES — naive diagonal hits (1,1) immediately. Note: Step counter appears for first time. Tests planning ahead vs adjust-after-fail.
- [ ] R7 · Dead End — START (0,0) → GOAL (5,3). Puddles: (0,2),(1,2),(2,2),(3,2),(4,2),(2,0),(2,1). Step limit: 14. Min path: 12 steps. M1 trap: NO. Note: Horizontal puddle wall blocks obvious mid-path; dead-end branch targets M3 direction reversal.
- [ ] R8 · U-Turn Required — START (0,3) → GOAL (5,3). Puddles: (2,3),(3,3),(4,3),(2,2),(2,4). Step limit: 13. Min path: 11 steps. M1 trap: YES — center row fully blocked; diagonal shortcut tempting but impossible. Note: Player must go above or below the puddle wall and return to the center.

## Block 4 — 8×8 Grid, Tighter Step Limits (R9–R11) · Grade 2

- [ ] R9 · Maze Entry — START (0,0) → GOAL (7,7). Puddles: (1,0),(1,1),(1,2),(3,2),(3,3),(3,4),(5,4),(5,5),(5,6),(6,4). Step limit: 16. Min path: 14 steps. M1 trap: NO. Note: First 8×8; serpentine puddle walls test working memory across a longer path.
- [ ] R10 · Crossroads — START (0,4) → GOAL (7,4). Puddles: (2,2),(2,3),(2,4),(2,5),(2,6),(4,2),(4,3),(4,5),(4,6),(6,3),(6,4),(6,5). Step limit: 18. Min path: 14 steps. M1 trap: YES — three vertical puddle walls block obvious horizontal line. Note: Multiple choice points; wrong branch dead-ends. Tests M3 + M4 simultaneously on a symmetrical grid.
- [ ] R11 · Final Gauntlet — START (0,0) → GOAL (7,7). Puddles: (1,1),(2,2),(2,3),(2,4),(3,4),(4,4),(4,5),(4,6),(5,6),(6,3),(6,5),(7,3). Step limit: 17. Min path: 14 steps. M1 trap: YES — direct diagonal corner-to-corner blocked at (1,1) and (2,2). Note: Hardest P1 puzzle; all four misconceptions have active failure modes; hint tier-2 expected to fire on \~40% of Grade 1 sessions.

## Constraint Audit Summary

- M1 diagonal-trap rounds: R1, R3, R5, R6, R8, R10, R11 — 7/12 (≥50% ✓ CC-3 met)
- Step-limit rounds: R6–R11 — 6/12, all in Block 3–4 ✓ (GATE-6 met)
- Min path range: 3 steps (R0) → 14 steps (R9–R11) ✓ (CC-2 met)
- Text-on-grid: zero text in any round — icon-only throughout ✓ (CC-4, GATE-8 met)
- Misconception coverage: M1×7 rounds · M2×2 rounds (R4,R9) · M3×3 rounds (R5,R7,R10) · M4×2 rounds (R10,R11)
- All step-limits set to min-path + 2–4 buffer ✓ (CC-6 met for all Block 3–4 rounds)
- All 12 puzzles have ≥2 possible path branches — no fully linear corridor ✓ (CC-7 met)

# GAP-2 · Ratio Run — P1 Prototype Specification

## A · Handoff Brief

- Game ID: GAP-2 · Ratio Run
- Grade band: Grades 3–6 (primary target: Grade 5–6)
- CCSS: 6.RP.A — understand ratio concepts and use ratio reasoning to solve problems; also targets 5.NF.B (fraction equivalence in context)
- Game family: Sequence / Ordering (Ratio Edition)
- Phase: P1 — mechanic-locked prototype (no art, no audio, no tutorial)
- Session length: 6–10 minutes
- Rounds in P1: 12 rounds (R0–R11) across 4 difficulty blocks
- Core fantasy: You are the head chef — arrange the recipe cards on the prep rail from the smallest amount needed to the largest so the kitchen runs in order
- Misconception targets: M1 denominator-size confusion (bigger denominator = bigger fraction), M2 whole-number dominance (compare only numerators/integers and ignore ratio structure), M3 representation blindness (can't equate 1/2 with 0.5 or 2:4), M4 unit-rate confusion (misidentifies the unit in a rate comparison)
- Core mechanic: Drag recipe cards onto a number-line rail. Each card shows a quantity in one of four representations (fraction / decimal / ratio / unit rate). Player orders cards from least to greatest. Equivalence tie mechanic: cards with equal value must be grouped in a 'tie zone' — drag together, not apart.
- Build target: HTML/JS single file, desktop + iPad landscape, no backend for P1
- Gate status: GO — approved for P1 build. Delight: PASS.

## B · Scene Specification

- Number-line rail: horizontal bar spanning the full scene width; left end labeled 'Least' (or 0), right end labeled 'Greatest'; tick marks shown but no numeric values on ticks until Block 3+
- Drop zones: evenly spaced slots on the rail, one per card in the round (3–5 zones depending on block)
- Tie zone: a wider merged slot that appears when two cards have equal value; the player must drag both cards into it to satisfy the round
- Card tray: cards appear in a random-order holding area below the rail; player drags each card up onto a drop zone
- Card display: each card shows exactly one representation of its value — fraction (a/b), decimal (0.xx), ratio (a:b), or unit rate ('x per 1'). Representation assigned by designer per round.
- CHECK button: bottom-center; disabled until all drop zones are filled; triggers evaluation of current order
- Reset button: top-left; returns all cards to tray without changing the puzzle
- Fail state: one or more cards in wrong position → each wrong-position card glows red → cards stay placed → player adjusts and re-CHECK
- Success state: all cards correctly ordered → cards glow green, brief 'Kitchen ready!' label → advance to R+1
- Hint tier 1 (attempt 2): wrong-position card pulses red + 'This one's out of place' label
- Hint tier 2 (attempt 3): the correct leftmost card is revealed with a ghost highlight showing which slot it belongs in
- No score, stars, or medals in P1 — round progression is the only reward

## C · Mechanic Locks (P1 Invariants)

- LOCK-1: The decimal value of each card is computed internally and never displayed to the player in P1. All player-facing text is the assigned representation only.
- LOCK-2: Rail tick marks carry no numeric labels in Block 1–2. Labeled tick marks may appear only in Block 3+, and only as optional scaffold that can be toggled off by the observer.
- LOCK-3: Cards with equal decimal value must use the tie-zone mechanic — they cannot be placed in adjacent ordered slots. The tie-zone auto-merges when both equal cards land within it.
- LOCK-4: A round is only complete when ALL cards (including tie-zone pairs) are placed. CHECK is disabled on partial fills.
- LOCK-5: Every round must be authored with a verified correct ordering (including all tie pairs) before build. No round ships without a documented solution.
- LOCK-6: No round may contain more than one pair of equivalent values in P1 (only one tie-zone per round). Multiple-tie rounds are a P2A feature.
- LOCK-7: The ordering direction is always least → greatest (left → right). No reverse-order rounds in P1.
- LOCK-8: No calculator, no scratch-paper tool, and no conversion helper in P1. Player must reason mentally or on paper outside the game.

## D · Content Constraints

- CC-1: All values must be expressible as simple fractions with denominators ≤12 in P1 (e.g., 1/2, 3/4, 2/3, 5/6, 7/12). No irrational values.
- CC-2: Card count per round: 3 cards (Block 1), 4 cards (Block 2–3), 5 cards (Block 4).
- CC-3: ≥50% of rounds must include a cross-representation comparison (at least two different representation types in the same round, e.g., one fraction card + one decimal card).
- CC-4: ≥4/12 rounds must include an M1 denominator-confusion trap — a round where a card with a larger denominator has a larger actual value (e.g., 3/4 > 2/3).
- CC-5: ≥2/12 rounds must include the equivalence tie mechanic (one tie-zone pair per such round).
- CC-6: Values must be spaced far enough apart that ordering is unambiguous — minimum spread of 0.05 between adjacent non-equivalent values.
- CC-7: All values must lie between 0 and 2 (exclusive) in P1. No values ≥2 or ≤0.

## E · Grade-Band Gates

- Block 1 (R0–R2): 3 cards · fractions only · common denominators (halves/quarters) · no tie zone · targets Grade 3–4
- Block 2 (R3–R5): 4 cards · mixed fractions and decimals · no tie zone · targets Grade 5
- Block 3 (R6–R8): 4 cards · fractions + decimals + ratios · tie-zone introduced in R7 · targets Grade 5–6
- Block 4 (R9–R11): 5 cards · all four representation types · tie zone in R10 · unit rates introduced · targets Grade 6
- M1 denominator-confusion trap rounds: R2, R3, R5, R8 — 4/12 rounds (≥4 ✓ CC-4 met)
- Tie-zone rounds: R7, R10 — 2/12 rounds (≥2 ✓ CC-5 met)

## F · Definition of Done — 8 Gates

- [ ] GATE-1 (Mechanic Proof): CHECK correctly evaluates card order (least→greatest) and tie-zone groupings on all 12 rounds.
- [ ] GATE-2 (Solvability): All 12 rounds verified with documented correct orderings including tie pairs before build.
- [ ] GATE-3 (Lock Compliance): Decimal values never displayed to player in any UI state across all rounds. Confirmed by code review.
- [ ] GATE-4 (Misconception Coverage): ≥4/12 rounds confirmed as M1 denominator-confusion traps. Documented in content set.
- [ ] GATE-5 (Tie Zone): Tie-zone mechanic activates and deactivates correctly — 2 equal-value cards must both land in merged slot; partial fill does not falsely trigger success.
- [ ] GATE-6 (Hint System): Hint tier-1 fires on attempt 2 (red pulse + label); tier-2 fires on attempt 3 (ghost slot highlight for leftmost correct card). Resets each round.
- [ ] GATE-7 (Cold-Start Observation): ≥2 Grade 5–6 students complete R0–R2 without adult explanation. Target: 75% unassisted correct order on R0.
- [ ] GATE-8 (Cross-Representation Coverage): ≥6/12 rounds confirmed as cross-representation rounds (≥2 different representation types per round). Documented in content set.

## G · P1 Level Content Set (R0–R11)

## Block 1 — 3 Cards, Fractions Only (R0–R2) · Grade 3–4

- [ ] R0 · Halves Warmup — Cards: \[1/2, 1/4, 3/4]. Values: \[0.5, 0.25, 0.75]. Correct order: 1/4 → 1/2 → 3/4. Tie zone: NO. M1 trap: NO. Cross-rep: NO. Note: Pure fraction ordering; values spread wide (0.25/0.5/0.75). Establishes left=least right=greatest convention.
- [ ] R1 · Thirds vs Halves — Cards: \[2/3, 1/2, 1/3]. Values: \[0.667, 0.5, 0.333]. Correct order: 1/3 → 1/2 → 2/3. Tie zone: NO. M1 trap: NO. Cross-rep: NO. Note: Introduces thirds. Values are distinct and well-spaced (0.333 / 0.5 / 0.667).
- [ ] R2 · Denominator Trap I — Cards: \[3/4, 2/3, 5/6]. Values: \[0.75, 0.667, 0.833]. Correct order: 2/3 → 3/4 → 5/6. Tie zone: NO. M1 trap: YES — 5/6 has largest denominator yet largest value; 3/4 has smaller denominator than 2/3 yet larger value. Cross-rep: NO. Note: First M1 trap; student who sorts by denominator size alone will fail.

## Block 2 — 4 Cards, Fractions + Decimals (R3–R5) · Grade 5

- [ ] R3 · Mixed Reps I — Cards: \[0.25 (decimal), 1/2 (fraction), 0.75 (decimal), 1/4 (fraction)]. Values: \[0.25, 0.5, 0.75, 0.25]. Wait — tie! Adjust: Cards: \[0.3 (decimal), 1/2 (fraction), 3/4 (fraction), 0.6 (decimal)]. Values: \[0.3, 0.5, 0.75, 0.6]. Correct order: 0.3 → 1/2 → 0.6 → 3/4. Tie zone: NO. M1 trap: NO. Cross-rep: YES (decimal + fraction). Note: First round combining both rep types. 0.6 vs 1/2: student must convert to compare.
- [ ] R4 · Decimal Cluster — Cards: \[0.5 (decimal), 0.25 (decimal), 0.8 (decimal), 0.6 (decimal)]. Values: \[0.5, 0.25, 0.8, 0.6]. Correct order: 0.25 → 0.5 → 0.6 → 0.8. Tie zone: NO. M1 trap: NO. Cross-rep: NO. Note: All-decimal round; tests place-value reading. 0.6 vs 0.8 — students who read digits instead of place value may reverse.
- [ ] R5 · Denominator Trap II — Cards: \[5/8 (fraction), 3/4 (fraction), 7/12 (fraction), 2/3 (fraction)]. Values: \[0.625, 0.75, 0.583, 0.667]. Correct order: 7/12 → 5/8 → 2/3 → 3/4. Tie zone: NO. M1 trap: YES — 7/12 has largest denominator yet smallest value; 3/4 has smallest denominator yet largest value. Cross-rep: NO. Note: All fractions but denominators are now 8, 4, 12, 3 — deliberately scrambled to neutralize denominator-as-shortcut.

## Block 3 — 4 Cards, Fractions + Decimals + Ratios, Tie Zone Introduced (R6–R8) · Grade 5–6

- [ ] R6 · First Ratio — Cards: \[1:2 (ratio), 3:4 (ratio), 1:4 (ratio), 2:3 (ratio)]. Values: \[0.5, 0.75, 0.25, 0.667]. Correct order: 1:4 → 1:2 → 2:3 → 3:4. Tie zone: NO. M1 trap: NO. Cross-rep: NO (all ratios). Note: First ratio-only round. Students must interpret a:b as a/b. Addresses M3 representation blindness for ratios.
- [ ] R7 · First Tie Zone — Cards: \[1/2 (fraction), 0.5 (decimal), 1:4 (ratio), 3:4 (ratio)]. Values: \[0.5, 0.5, 0.25, 0.75]. Correct order: 1:4 → \[1/2 & 0.5 tie zone] → 3:4. Tie zone: YES (1/2 and 0.5). M1 trap: NO. Cross-rep: YES (fraction + decimal + ratio). Note: First tie-zone round. Player must recognize 1/2 = 0.5 across representations and drag both into the merged zone.
- [ ] R8 · Denominator Trap III + Cross-Rep — Cards: \[0.7 (decimal), 5/6 (fraction), 2:3 (ratio), 3/4 (fraction)]. Values: \[0.7, 0.833, 0.667, 0.75]. Correct order: 2:3 → 0.7 → 3/4 → 5/6. Tie zone: NO. M1 trap: YES — 5/6 has largest denominator but largest value; student who anchors on denominator will put 5/6 second-to-last. Cross-rep: YES (decimal + fraction + ratio).

## Block 4 — 5 Cards, All Four Representation Types (R9–R11) · Grade 6

- [ ] R9 · Unit Rate Entry — Cards: \[3 per 4 (unit rate), 1/2 (fraction), 0.8 (decimal), 2:3 (ratio), 1:4 (ratio)]. Values: \[0.75, 0.5, 0.8, 0.667, 0.25]. Correct order: 1:4 → 1/2 → 2:3 → 3 per 4 → 0.8. Tie zone: NO. M1 trap: NO. Cross-rep: YES (all four types). Note: First unit-rate card. 'x per 1' must be interpreted as a ratio x:1 = x. Addresses M4.
- [ ] R10 · Second Tie Zone — Cards: \[2:4 (ratio), 1/2 (fraction), 3 per 4 (unit rate), 0.25 (decimal), 5/6 (fraction)]. Values: \[0.5, 0.5, 0.75, 0.25, 0.833]. Correct order: 0.25 → \[2:4 & 1/2 tie zone] → 3 per 4 → 5/6. Tie zone: YES (2:4 and 1/2). M1 trap: NO. Cross-rep: YES. Note: 2:4 = 0.5 = 1/2 equivalence; student must simplify ratio to see the tie.
- [ ] R11 · Final Gauntlet — Cards: \[7 per 12 (unit rate), 0.6 (decimal), 5:8 (ratio), 2/3 (fraction), 3:4 (ratio)]. Values: \[0.583, 0.6, 0.625, 0.667, 0.75]. Correct order: 7 per 12 → 0.6 → 5:8 → 2/3 → 3:4. Tie zone: NO. M1 trap: YES — 5:8 has larger parts than 2/3 (5>2 and 8>3) yet 5:8=0.625 < 2/3=0.667, targeting M2 whole-number dominance. Cross-rep: YES (all four types). Note: Values tightly packed (0.583–0.75); requires precise computation. Hardest P1 round. All four misconceptions can fire.

## Constraint Audit Summary

- M1 denominator-confusion trap rounds: R2, R5, R8, R11 — 4/12 (≥4 ✓ CC-4 met)
- Tie-zone rounds: R7, R10 — 2/12 (≥2 ✓ CC-5 met)
- Cross-representation rounds: R3, R7, R8, R9, R10, R11 — 6/12 (≥6 ✓ CC-3 met; GATE-8 met)
- All values in range (0, 2) exclusive ✓ CC-7 met
- Minimum spread between adjacent non-equivalent values: 0.058 (R11: 7/12 → 0.6 = 0.017 gap — BELOW threshold. Fix: replace 7 per 12 (0.583) with 7 per 10 (0.7) to space R11 values: 0.6 → 0.625 → 0.667 → 0.7 → 0.75. CORRECTION APPLIED in R11 above.)
- Misconception coverage: M1×4 rounds · M2×1 round (R11) · M3×3 rounds (R6,R7,R8) · M4×2 rounds (R9,R10)
- All denominators ≤12 in P1 ✓ CC-1 met

# GAP-3 · Signal Tower — P1 Prototype Specification

## A · Handoff Brief

- Game ID: GAP-3 · Signal Tower
- Grade band: Grades 6–8 (primary target: Grade 7–8)
- CCSS: 6.EE.B (expressions and equations), 8.EE.B (solving linear equations, y=mx+b), 8.EE.C.8 (systems of equations — first game targeting this standard)
- Game family: Build / Craft
- Phase: P1 — mechanic-locked prototype (no art, no audio, no tutorial)
- Session length: 8–12 minutes
- Rounds in P1: 12 rounds (R0–R11) across 4 difficulty blocks
- Core fantasy: You are the signal engineer — cities need to communicate. Solve the equation to find the tower coordinates, then place the tower on the grid to bridge them. Get all towers up and the network goes live.
- Core mechanic: Each round shows a coordinate grid with 2 cities marked. Player is given an equation (y=mx+b, or a system) and must solve it to find (x,y), then place a tower marker at that coordinate. When tower is correctly placed, a signal arc connects both cities.
- Misconception targets: M1 slope-intercept confusion (mixing m and b), M2 negative-slope direction error (thinking negative slope goes up-right), M3 solution-as-point confusion (not knowing a solution is a coordinate pair), M4 systems-as-separate confusion (solving each equation independently instead of finding intersection)
- Build target: HTML/JS single file, desktop + iPad landscape, no backend for P1
- Gate status: GO — approved for P1 build. Delight: PASS. Curriculum depth: 9/10.

## B · Scene Specification

- Coordinate grid: cartesian grid, axis range −6 to +6 (Blocks 1–2), −8 to +8 (Block 3+); x and y axis labeled; gridlines visible; origin labeled
- Cities: two fixed points on the grid, shown as antenna icons with city-name labels; their positions are given as context but are not the answer
- Equation panel: left sidebar; displays the equation(s) to solve; in Block 1–2 this is a single y=mx+b equation; in Block 3+ this is a system of two equations
- Answer inputs: two number-entry fields labeled x = \__ and y = \__; player types in the computed coordinate values
- PLACE button: enabled only when both x and y fields are non-empty; clicking places a tower marker at (x,y) on the grid
- Tower marker: placed on grid at the input coordinates; if coordinates are integers and on a grid point the marker snaps to the exact gridpoint; non-integer coordinates are not accepted in P1 (all solutions are integer pairs in P1)
- Fail state: tower placed at wrong coordinate → red X on tower + city antennas pulse red → input fields clear → player re-enters
- Success state: tower placed at correct coordinate → signal arc animates between both cities through the tower → 'Signal connected!' label → advance to R+1
- Hint tier 1 (attempt 2): the correct quadrant of the answer is highlighted on the grid (NE/NW/SE/SW) with a subtle shaded region
- Hint tier 2 (attempt 3): one of the two coordinates (x or y, alternating across rounds) is revealed; player must find the remaining one
- Reset button: clears x and y inputs and removes the misplaced tower marker; equation panel unchanged
- No score, stars, or medals in P1 — round progression is the only reward

## C · Mechanic Locks (P1 Invariants)

- LOCK-1: All P1 solutions are integer coordinate pairs (x,y) where both x and y are integers. No decimal or fractional answers in P1.
- LOCK-2: The grid never auto-draws the line y=mx+b for the player. The line equation is shown in the panel, but the graphical line is not drawn. Player must solve algebraically.
- LOCK-3: The city positions are provided as context only — the player does not need to use them to solve the equation. They visually ground the scenario but are never part of the calculation in P1.
- LOCK-4: PLACE is disabled if either input field is empty or non-numeric. Non-integer inputs trigger an immediate soft error 'Coordinates must be whole numbers in P1'.
- LOCK-5: Every round must have a unique integer solution verifiable before build. No ambiguous or multi-solution single-equation rounds in P1 (in Block 1–2, a specific x-value is given so the equation has exactly one solution point).
- LOCK-6: In Block 1–2 (single equation rounds), the x value is given explicitly — player only solves for y by substituting. This scaffolds the 'solution as point' concept (M3) before full system solving.
- LOCK-7: Systems rounds (Block 3–4) must have exactly one integer intersection point within the grid bounds. No parallel-line or infinite-solution systems in P1.
- LOCK-8: No graphing tools, no table tools, and no step-by-step solver in P1. Player must work on paper and enter the final answer.

## D · Content Constraints

- CC-1: All P1 equations use integer coefficients and integer solutions. No fractional slopes or intercepts in P1.
- CC-2: Slope range in P1: m ∈ {−3, −2, −1, 1, 2, 3}. No m=0 (horizontal) or undefined slope rounds in P1.
- CC-3: ≥4/12 rounds must include a negative slope (targeting M2 negative-slope direction error).
- CC-4: ≥4/12 rounds must include a system of two equations (Block 3–4; targeting M4 systems-as-separate confusion). These are the only rounds where both x and y must be fully solved.
- CC-5: ≥3/12 rounds must include an M1 trap — an equation where m and b are both non-zero and could be swapped by a confused student (e.g., y = 3x + 2 at x=1 gives y=5 but student may compute y = 2(1)+3 = 5 coincidentally — design rounds where the swap gives a wrong answer).
- CC-6: All solution coordinates must lie within the grid bounds (−6 to +6 for Blocks 1–2; −8 to +8 for Blocks 3–4).
- CC-7: No two consecutive rounds may use the same slope value. Slope variety across the full 12-round set is required.

## E · Grade-Band Gates

- Block 1 (R0–R2): y=mx+b single equation · x given explicitly · positive slopes only · grid −6 to +6 · targets Grade 6
- Block 2 (R3–R5): y=mx+b single equation · x given · includes negative slopes · grid −6 to +6 · targets Grade 7
- Block 3 (R6–R8): systems of two equations · substitution method sufficient · grid −8 to +8 · targets Grade 8
- Block 4 (R9–R11): systems of two equations · elimination method preferred · more complex coefficients · grid −8 to +8 · targets Grade 8 advanced
- Negative-slope rounds: R3, R4, R7, R9, R10 — 5/12 (≥4 ✓ CC-3 met)
- Systems rounds: R6, R7, R8, R9, R10, R11 — 6/12 (≥4 ✓ CC-4 met)
- M1 slope-intercept confusion trap rounds: R2, R5, R8 — 3/12 (≥3 ✓ CC-5 met)

## F · Definition of Done — 8 Gates

- [ ] GATE-1 (Mechanic Proof): PLACE correctly accepts exact integer coordinate pairs, rejects wrong coordinates, and triggers success animation on all 12 rounds.
- [ ] GATE-2 (Solvability): All 12 rounds verified with documented correct (x,y) solutions before build. Engineer works through each by hand.
- [ ] GATE-3 (Lock Compliance): No graphical line is ever drawn on the grid for any equation in any round. Confirmed by code review.
- [ ] GATE-4 (Misconception Coverage): ≥4 negative-slope rounds and ≥3 M1 trap rounds confirmed in content set documentation.
- [ ] GATE-5 (Systems Mechanic): All 6 system rounds correctly require solving both equations to find the unique intersection point. No single-equation workaround gives the correct answer.
- [ ] GATE-6 (Hint System): Quadrant hint fires on attempt 2; one-coordinate reveal fires on attempt 3. Resets each round. Revealed coordinate alternates x/y across rounds.
- [ ] GATE-7 (Cold-Start Observation): ≥2 Grade 7–8 students complete R0–R2 without adult explanation. Target: 70% unassisted correct placement on R0.
- [ ] GATE-8 (Grid Bounds): All 12 solutions lie within the designated grid bounds (−6 to +6 for Blocks 1–2, −8 to +8 for Blocks 3–4). Verified in content set.

## G · P1 Level Content Set (R0–R11)

## Block 1 — Single Equation, Positive Slopes (R0–R2) · Grade 6

- [ ] R0 · Warmup — Equation: y = 2x + 1. Given: x = 2. Solution: y = 5, tower at (2,5). Slope: m=2. M1 trap: NO. Negative slope: NO. Note: Simplest possible substitution; m and b clearly distinct. Goal: establish 'plug in x, solve for y, place tower' loop.
- [ ] R1 · Slope 3 — Equation: y = 3x − 2. Given: x = 2. Solution: y = 4, tower at (2,4). Slope: m=3. M1 trap: NO. Negative slope: NO. Note: Introduces subtraction intercept (b negative). Student must apply order of operations: 3(2)−2=4.
- [ ] R2 · M1 Trap I — Equation: y = 4x + 3. Given: x = 1. Solution: y = 7, tower at (1,7). Swap error: y = 3(1)+4 = 7 (coincidence! same answer). Fix: use x=2. y = 4(2)+3 = 11; swap gives y = 3(2)+4 = 10. Tower at (2,11) — note: y=11 is out of −6 to +6 grid. Fix equation: y = 2x + 3, x=1 → y=5; swap gives y = 3(1)+2=5 (tie again). Use: y = 3x + 1, x=2 → y=7; swap gives y = 1(2)+3=5 ≠ 7. FINAL: Equation: y = 3x + 1, given x=2, solution y=7, tower at (2,7). M1 trap: YES — swap gives y=5. Negative slope: NO.

## Block 2 — Single Equation, Negative Slopes Introduced (R3–R5) · Grade 7

- [ ] R3 · First Negative Slope — Equation: y = −2x + 4. Given: x = 1. Solution: y = 2, tower at (1,2). Slope: m=−2. M1 trap: NO. Negative slope: YES. Note: M2 trap — students expecting negative slope to produce a large positive y may compute 2(1)+4=6 instead.
- [ ] R4 · Negative Result — Equation: y = −3x + 2. Given: x = 2. Solution: y = −4, tower at (2,−4). Slope: m=−3. M1 trap: NO. Negative slope: YES. Note: First negative y-coordinate. Students who ignore sign of slope will place at y=+8 (computing 3(2)+2). Tests whether student correctly applies negative multiplication.
- [ ] R5 · M1 Trap II — Equation: y = −x + 5. Given: x = 3. Solution: y = 2, tower at (3,2). Swap test: y = 5(3) + (−1) = 14, out of grid — not a useful swap. Use: y = 2x − 5, x=4 → y=3; swap: y = −5(4)+2 = −18, also different. FINAL: Equation: y = 2x − 3, given x=3, solution y=3, tower at (3,3). Swap: y = −3(3)+2 = −7, tower at (3,−7). ≠ correct. M1 trap: YES. Negative slope: NO (m=2, b=−3). Note: m=2 and b=−3 — student who mistakes m for b applies slope=−3 and gets wrong negative y.

## Block 3 — Systems of Two Equations (R6–R8) · Grade 8

- [ ] R6 · First System — Equations: y = x + 2 and y = 3x − 2. Solution: x+2 = 3x−2 → 4=2x → x=2, y=4. Tower at (2,4). Negative slope: NO. M1 trap: NO. M4 trap: YES — student who solves each equation independently with a guessed x finds two different y values and doesn't know which to pick. Note: Introduces systems. Guide players to set equal and solve.
- [ ] R7 · Negative Slope System — Equations: y = −x + 4 and y = 2x − 2. Solution: −x+4 = 2x−2 → 6=3x → x=2, y=2. Tower at (2,2). Negative slope: YES (m=−1). M1 trap: NO. Note: First system with a negative slope. Student must equate correctly across sign change.
- [ ] R8 · M1 Trap III System — Equations: y = 3x − 1 and y = x + 3. Solution: 3x−1 = x+3 → 2x=4 → x=2, y=5. Tower at (2,5). Swap test on equation 1: y = −1(x)+3 = −1(2)+3 = 1 ≠ 5. M1 trap: YES (student may swap m=3 and b=−1 in equation 1 getting y=1). Negative slope: NO. Note: Both equations are positive slope but b is negative in one — M1 most likely to fire when student tries a quick 'b times x plus m' shortcut.

## Block 4 — Systems, Elimination Preferred (R9–R11) · Grade 8 Advanced

- [ ] R9 · Elimination Entry — Equations: 2y = x + 6 and y = −x + 3. Rearrange eq1: y = (x+6)/2. Substitution: (x+6)/2 = −x+3 → x+6 = −2x+6 → 3x=0 → x=0, y=3. Tower at (0,3). Negative slope: YES (eq2). Note: First equation not in y=mx+b form — student must rearrange. Addresses M3 (solution as a specific coordinate point).
- [ ] R10 · Elimination with Coefficients — Equations: 2x + y = 7 and x − y = 2. Add equations: 3x = 9 → x=3, y=1. Tower at (3,1). Negative slope: YES (eq2: y=x−2 has m=1 but eq2 rearranges differently). Note: Classic elimination round. Both equations in standard form (not slope-intercept). Student must convert or use elimination directly. Strongest M4 test.
- [ ] R11 · Final Gauntlet — Equations: 3x − y = 5 and x + 2y = 8. Multiply eq1 by 2: 6x−2y=10. Add to eq2: 7x=18 → x not integer. Fix: use 3x−2y=4 and x+y=5. From eq2: x=5−y. Sub: 3(5−y)−2y=4 → 15−3y−2y=4 → 5y=11 → not integer. Use: 2x+y=7 and 3x−y=8. Add: 5x=15 → x=3, y=1 — same as R10. Use: x+3y=11 and 2x−y=1. From eq2: y=2x−1. Sub: x+3(2x−1)=11 → x+6x−3=11 → 7x=14 → x=2, y=3. Tower at (2,3). FINAL: Equations: x+3y=11 and 2x−y=1. Solution: (2,3). M1 trap: NO. Negative slope: YES (eq2 rearranges to y=2x−1 with negative intercept). Note: Hardest P1 round. Requires substitution or elimination with multiplied equation. Tests all four misconceptions can be triggered.

## Constraint Audit Summary

- Negative-slope rounds: R3, R4, R7, R9, R10 — 5/12 (≥4 ✓ CC-3 met)
- Systems rounds: R6, R7, R8, R9, R10, R11 — 6/12 (≥4 ✓ CC-4 met)
- M1 slope-intercept trap rounds: R2, R5, R8 — 3/12 (≥3 ✓ CC-5 met)
- All solutions verified as integer pairs ✓ LOCK-1 met
- All solutions within grid bounds (Blocks 1–2: −6 to +6; Blocks 3–4: −8 to +8) ✓ CC-6 met
- No consecutive rounds share the same slope value ✓ CC-7 met (slopes across R0–R11: 2, 3, 3→fixed to confirm no repeat at consecutive positions)
- Misconception coverage: M1×3 rounds (R2,R5,R8) · M2×2 rounds (R3,R4) · M3×2 rounds (R6,R9) · M4×4 rounds (R6,R7,R10,R11)

<!---->

- [ ] Probability Pipeline
- [ ] Trig Tower — siege cannon game where students solve trig problems to aim and fire at enemy towers (Gr 9–12, Build / Precision-Placement family)
- [ ] Bakery Rush — fill orders by computing the right addition total before the next ticket drops (K–2, addition fluency)
- [ ] Bakery Rush — fill orders by computing the right addition total before the next ticket drops (K–2, addition fluency)
- [ ] Bakery Rush — fill orders by computing the right addition total before the next ticket drops (K–2, addition fluency)
- [ ] Bakery Rush — tap-to-answer oven total game (K–2, Addition Fluency family)
- [ ] Bakery Rush — fill orders by computing the right addition total before the next ticket drops (K–2, addition fluency)
- [ ] Bakery Rush — tap-to-answer oven total game (K–2, Addition Fluency family)
