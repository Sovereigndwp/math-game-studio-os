# Snack Line Shuffle — P1 Prototype Engineer Handoff Brief

## Header

| Field | Value |
|---|---|
| **Issued** | 2026-04-08 |
| **Status** | Spec Ready — awaiting Gate 6 (teacher sign-off) before build start |
| **Origin** | normalized from Taskade project `9bfNR2acXuAHiWyC` ("Prototype Specifications"), Snack Line Shuffle section |
| **Raw source** | [`taskade_exports/projects/9bfNR2acXuAHiWyC.json`](../../taskade_exports/projects/9bfNR2acXuAHiWyC.json) |
| **Build phase** | P1 — Core Loop |
| **Pipeline status** | GO — advanced to Prototype P1 on 2026-04-08 |
| **Family** | Sequence / Ordering — first K-2 member |

## Scope note for this document

This file is the **build-side** handoff brief. The outcome-side gates ("what success looks like when playtested") live in the adjacent [`p1_definition_of_done.md`](p1_definition_of_done.md). This file intentionally does not duplicate that list — it specifies:

1. Pre-build blockers
2. Ordered build checklist
3. Asset requirements
4. Telemetry schema
5. Pre-playtest review sequence (Gates 1–6, build-side)
6. P1 out-of-scope list

For the P1 fail conditions and playtest thresholds (Gates 7–10), see [`p1_definition_of_done.md`](p1_definition_of_done.md).

## Permanent design rule (P1 through P5)

> The system must never display a computed total, `>/<` relation, or explicit who-goes-first indicator during gameplay — at any state, in any build phase. Permanent. P1–P5.

This rule cannot be broken. It applies across all future build phases. A feedback or hint system may highlight which adjacent pair conflicts (amber glow) but must NEVER surface the underlying numbers (totals, `>/<` relation, or explicit who-goes-first) as part of error feedback.

---

## Section 1 — Pre-build blockers (resolve before writing a line of code)

- [ ] **BLOCKER A — Gate 6 teacher sign-off.** Recruit ≥ 2 K-2 classroom teachers. Share the approved Core Fantasy text ("kitchen helper / correct portions") and at least 3 sample amber VO lines. Each teacher must independently confirm in writing: (a) framing does not conflict with fairness or social-emotional norms; (b) a 5–8 year old would understand the role without adult explanation. Log both sign-offs in the Gate 6 row before any code is written. **No exceptions.**
- [ ] **BLOCKER B — Amber VO copy set written.** Author ≥ 3 distinct kid-voice lines for the amber state. Requirements: no totals, no `>/<` relation, no explicit who-goes-first, no shaming, non-repetitive. Examples: *"I'm not sure I'm in the right spot." / "Do you think I belong here?" / "Something doesn't feel quite right…"* Draft must be reviewed alongside Gate 6 teacher review. The line *"Hey, I think I should go before you!"* is flagged as borderline — require teacher confirmation it is not fairness-coded before using.
- [ ] **BLOCKER C — Level content set authored and audited.** Author ≥ 12 P1 rounds before build (actual P1 set is 14 rounds, R0–R13 — see [`question_audit.md`](question_audit.md)). Constraints: addition within 5 only · largest-first rule only · 2–4 kids per round · all totals strictly distinct (no ties) · ≥ 30% of rounds include an M1 trap pair (bigger-looking addend ≠ bigger total). Have one designer audit the set against the Visual Neutrality Constraint before committing.
- [ ] **BLOCKER D — Ordering-direction indicator designed.** Design the icon + VO cue for the ordering rule before building any scene chrome. Must communicate "most snacks at the front, fewest at the back" to a non-reader. Cannot rely on text alone. Cannot imply fairness, winning, or moral judgment. Will be reviewed by educator in Gate 12.

---

## Section 2 — Ordered build checklist

*Build in this order. Do not proceed past a step until verified in-engine.*

1. **Static scene shell** — Cafeteria background · serving counter at line-end · 4 drop-zone line slots rendered and labelled by position only (no rank number) · ordering-direction indicator widget placed and visible · Serve button present but inert · no kids loaded yet.
   - Verify: slot hit targets are ≥ 48×48 px for touch; slots do not visually encode rank.
2. **Kid entities + tray rendering** — Load 2–4 kid sprites with tray overlay showing expression (e.g. `3+2`). Expression rendered in a clear, legible font ≥ 18 pt. Snack icon art decorative only.
   - Verify: no icon encodes quantity magnitude. Kid character dimensions uniform across all kid variants.
3. **Drag-and-drop system** — Player can pick up any kid and drop into any slot. Kid snaps into slot on release. Kid can be re-picked and moved at any time. Swapping two kids in occupied slots is allowed. No lock-in until Serve is tapped.
   - Verify: works with mouse and touch input.
4. **Adjacency glow system (Option B — CORE)** — On every drag-complete event: (a) evaluate ordering rule (largest-first) across all currently occupied adjacent pairs; (b) apply glow state — Neutral (grey, no neighbour) / Green (pair in correct order) / Amber (pair in wrong order). Glow updates on every move, not just on Serve. A kid in a slot with no neighbour shows neutral.
   - Verify: moving a kid to a new position updates both its old adjacency AND its new adjacency correctly.
5. **Amber VO trigger (transition-only)** — When an adjacency transitions to amber state, play one of the approved amber VO lines at random. Do not play a VO line if the pair was already amber (transition-only semantics — this was fixed in the 2026-04-09 audit). Do not stack multiple simultaneous VO triggers.
   - Verify: VO plays on the first wrong placement but not on repeated drags that leave the same pair amber.
6. **Serve button activation logic** — Serve button is greyed / inert unless ALL slots are occupied. When all slots are occupied and ALL adjacencies are green or neutral: Serve becomes active. When any adjacency is amber: Serve remains inert.
   - Verify: Serve cannot be triggered as a probe on a partial or incorrectly ordered line.
7. **Correct-round animation** — On Serve tap when active: play cheer animation on all kids · cafeteria window opens · line advances toward counter · brief non-skippable sequence (≤ 3 seconds). After animation: load next round.
   - Verify: no computed totals appear during or after animation.
8. **Round loop + level data loader** — Load rounds from the authored content set (14 rounds). Each round specifies: kid count (2–4) · expression per kid · known correct ordering. Session progresses through rounds in authored sequence. No score display in P1. No timer in P1. End-of-session screen is a simple "All done!" with no ranking or score.
9. **Telemetry instrumentation** — See Section 4 for full schema. Wire all required events before first playtest. Verify output against schema with a manual 3-round test session before handing to testers.
10. **Visual neutrality audit (self-review before Gate 12)** — Engineer or designer reviews full rendered build against the Visual Neutrality Constraint: kid height, width, colour saturation must not correlate with total; snack icon quantity / size on tray must not correlate with total; slot position labels must not reveal rank. Sign off before scheduling educator review.

---

## Section 3 — Asset requirements

- **Background** — Single cafeteria interior. Serving counter visible at one end. Warm, inviting. No clutter that could encode quantity. 1 variant only in P1.
- **Kid sprites** — ≥ 4 distinct kid characters (avoid identical-looking variants to aid player tracking). Each character: idle state · drag state · cheer state. Uniform bounding box across all characters — heights must match. No character may be drawn larger or more prominent in a way that correlates with any math value.
- **Tray overlay** — Rendered as a UI layer on top of kid sprite. Shows expression string (e.g. `3+2`). Font: bold, rounded, ≥ 18 pt, high contrast. Optional decorative snack icon(s) alongside expression — must be identical across all trays regardless of total (e.g. always one fork icon, one napkin icon). Never show icon quantity that matches or hints at total.
- **Adjacency glow FX** — Three states per slot-pair:
  - **Neutral** — no glow (default border only)
  - **Green** — soft green halo on both kids in the pair
  - **Amber** — amber / orange halo on both kids in the pair
  - Glow must be visible but not overwhelming. Accessibility: glow colour must not be the only signal — consider adding a subtle icon (`✓` / `?`) for colour-blind support.
- **Ordering-direction indicator** — Icon + VO widget. Icon must communicate "most snacks → least snacks, front to back" to a non-reader. Suggested: arrow pointing toward serving counter + stacked plate icons decreasing in size left-to-right (if horizontal line). VO: short, clear, repeated at round start. Requires educator approval (Gate 12) before locking.
- **Serve button** — Greyed / disabled state + active state. Label "Serve!" with serving-hand or tray icon. Active state should feel inviting — it is the delight confirmation, not a test trigger.
- **Correct-round animation** — Kids cheer (arms up, smiling faces) · cafeteria window slides open · serving tray passes down the line. 2.5–3 seconds total. No score or number appears at any point.
- **Audio** — Amber VO lines (≥ 3, recorded, age-appropriate voices — 5–8 year old peer voice preferred) · Serve correct SFX (warm cheer / bell) · background cafeteria ambience (light, non-distracting). No audio required for neutral / green glow in P1.

---

## Section 4 — Telemetry schema

*Emit one JSON record per round. Append records to a session file. Export as JSON or CSV for playtest analysis. All five fields are required — the spam signal and move-count are the primary evidence for the playtest gates.*

| Field | Type | Definition |
|---|---|---|
| `session_id` | string | Unique per player-session (UUID or timestamp-hash). Constant across all rounds in one sitting. |
| `round_index` | integer | 0-based position of this round in the session. Used for trend analysis (does `spam_rate` fall across the session? does `correct_on_first_try` rise?). |
| `time_per_round_ms` | integer | Milliseconds from round load to Serve tap. Start clock when kids appear on screen. Stop clock when Serve is tapped (successful). Proxy for deliberateness vs guessing speed. |
| `correct_on_first_serve` | boolean | `true` if the Serve tap that completes the round is the FIRST Serve tap in that round (all slots filled, all adjacencies green, no prior Serve attempt this round). `false` if any Serve attempt preceded the successful one. |
| `kid_move_count_before_serve` | integer | Total number of completed drag-and-drop events in the round before the final Serve tap (including re-drags and swaps). `≥ 1` on `≥ 70%` of rounds is the telemetry cross-check for computation evidence. |
| `serve_presses_with_no_prior_move` | integer | Count of Serve button presses where no `kid_move` event occurred since the last amber→cleared transition or round start. This is the spam signal. Divide by `total_serve_presses` to get `spam_rate`. |

### Derived (compute post-session, not stored per round)

- `spam_rate = serve_presses_with_no_prior_move / total_serve_presses`
- `first_try_rate = rounds where correct_on_first_serve = true / total_rounds`
- `mean_time_per_round`
- `move_count_trend` (`round_index` vs `kid_move_count` — slope should be ≤ 0 as player becomes faster)

**Gate 9 threshold:** median `spam_rate` across sample ≤ 0.20. See [`p1_definition_of_done.md`](p1_definition_of_done.md) for the full playtest-gate thresholds.

---

## Section 5 — Engineer data format (level content)

*Implement each round as a JSON object. The `correctOrder` field drives the adjacency glow engine — slot 0 is the front of line. Expressions are presented to the player in `displayOrder` (shuffled); the engine compares player placement against `correctOrder` to compute green/amber glow states.*

### Schema

```json
{
  "roundIndex": 10,
  "kidCount": 4,
  "kids": [
    { "id": "k-a", "expression": "4+0", "total": 4 },
    { "id": "k-b", "expression": "3+0", "total": 3 },
    { "id": "k-c", "expression": "2+3", "total": 5 },
    { "id": "k-d", "expression": "1+0", "total": 1 }
  ],
  "correctOrder": ["k-c", "k-a", "k-b", "k-d"],
  "displayOrder": ["k-a", "k-b", "k-c", "k-d"],
  "m1Trap": true
}
```

### Adjacency rule

For any two kids placed in adjacent slots `i` and `i+1`:
- `GREEN` if `correctOrder.indexOf(kidAt[i]) < correctOrder.indexOf(kidAt[i+1])`
- `AMBER` if reversed
- `NEUTRAL` if either slot is empty

### `displayOrder` note

Randomise `displayOrder` per session so the same player does not always see the same starting layout. For M1 trap rounds, ensure the trap kid (bigger first addend, smaller total) appears in a visually prominent position in `displayOrder` to make the trap salient — do not hide it in position 3 or 4 every time.

---

## Section 6 — Pre-playtest review sequence (Gates 1–6, build-side)

*All six gates must be cleared before any player — including internal testers — sits down with the build. Gates 1–5 are internal; Gate 6 requires external educator input. Do not schedule playtest until the Gate 6 sign-off log has two entries.*

| Gate | Reviewer | Pass criteria |
|---|---|---|
| **Gate 1 — Scene built** | Engineer self-sign-off | Cafeteria background rendered · 4 line slots present and correctly labelled · ordering-direction indicator widget visible and prominent · Serve button present but inert · no kids loaded. Slot hit targets ≥ 48×48 px. No slot label reveals rank. |
| **Gate 2 — Option B Serve mechanic verified** | Engineer + one QA pass | (a) drag kid to slot → verify adjacency glow fires immediately · (b) create amber pair → verify Serve button stays inert · (c) resolve all ambers → verify Serve activates · (d) tap Serve → verify no total or ranking text appears anywhere in the animation · (e) confirm Serve cannot be activated on partially filled line · (f) confirm computed total is never visible in any UI state. **Fail any of these = do not proceed.** |
| **Gate 3 — Amber VO copy approved** | Content designer + one Gate 6 educator | Per line: no totals · no `>/<` · no explicit who-goes-first · no shaming tone · reads as 5–8 year old peer voice · ≥ 3 distinct lines exist. |
| **Gate 4 — K-1 difficulty constrained** | Content designer | Audit every authored round against: addition within 5 only · no subtraction · no total above 5 · 3–4 kids max · no equal-total pairs (no ties). |
| **Gate 5 — Grade 2+ gate enforced** | Content designer | Confirm P1 content set contains zero instances of: subtraction · totals above 10 · 5+ kids per round · positional constraints. Any future Grade 2+ content is held in a separate flagged section. |
| **Gate 6 — Fantasy alignment teacher sign-off** *(BLOCKING)* | ≥ 2 independent K-2 classroom teachers | Each teacher independently confirms YES to both: (a) "This framing does not conflict with fairness, turn-taking, or social-emotional norms for K-2." (b) "A typical 5–8 year old would understand the player role without adult explanation." **This gate cannot be waived or deferred.** |

### Gate 6 sign-off log

| Teacher | Name · School / Role · Date | (a) | (b) |
|---|---|---|---|
| 1 | — | — | — |
| 2 | — | — | — |

---

## Section 7 — What is explicitly out of scope for P1

- **Subtraction expressions** — reserved for P2A (introduces M3, M5 misconceptions)
- **Tie episodes (equal-total pairs)** — reserved for P2A (M2 misconception)
- **Score / stars / progress bar** — no numerical feedback of any kind in P1
- **Timer or time pressure** — no time mechanic in P1
- **Second thematic world** — Delight Gate condition; reserved for P2+
- **5-6 kid rounds or within-20 math** — Grade 2+ gate; not in P1
- **Hint system or scaffold panel** — amber glow is the only feedback mechanism; no supplementary hints in P1
- **First-try-correct bonus** — reserved for P2A

---

## Related repo documents

- [`concepts/snack-line-shuffle/concept.md`](concept.md) — concept packet (core fantasy, CCSS, family placement)
- [`concepts/snack-line-shuffle/p1_definition_of_done.md`](p1_definition_of_done.md) — outcome-side DoD (Gates 7–10 playtest thresholds)
- [`concepts/snack-line-shuffle/misconception_notes.md`](misconception_notes.md) — M1–M7 register
- [`concepts/snack-line-shuffle/curriculum_map.md`](curriculum_map.md) — grade-band scope and tier gating
- [`concepts/snack-line-shuffle/question_audit.md`](question_audit.md) — 14-round audit + fix record
- [`docs/build_standards_gate.md`](../../docs/build_standards_gate.md) — Stage 8.5 Build Standards Gate (applies to this handoff before dev can start)
