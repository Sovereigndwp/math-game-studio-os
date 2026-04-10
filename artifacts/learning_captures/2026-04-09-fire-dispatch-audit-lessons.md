# Lesson: Fire Dispatch Audit — Seven Cross-Game Engineering Lessons

| Field | Value |
|---|---|
| **Date** | 2026-04-09 |
| **Source** | Fire Dispatch audit, captured in Taskade project `6ra74LfBTu38GdVF` ("Genesis Build Progress — Math Game Studio OS"), lines 630–637 |
| **Raw source** | [`taskade_exports/projects/6ra74LfBTu38GdVF.json`](../../taskade_exports/projects/6ra74LfBTu38GdVF.json) · [`taskade_exports/markdown_renderings/Genesis_Build_Progress_—_Math_Game_Studio_OS.md`](../../taskade_exports/markdown_renderings/Genesis_Build_Progress_—_Math_Game_Studio_OS.md) |
| **Game(s)** | Fire Dispatch (primary) · applies cross-game |
| **Pass** | learning capture (post-audit) |
| **Classification** | reusable engineering rules |
| **Game family** | cross-family — rules apply to any game with remainder/division mechanics, equation reveals, multi-attempt hints, boss rounds, multi-step rounds, or time-pressure claims |
| **Tags** | remainder, equation-reveal, progressive-hints, boss-rounds, multi-step, text-audit, time-pressure, p2-architectural |

## What happened

Fire Dispatch was audited on 2026-04-09 and seven reusable cross-game engineering lessons were surfaced. The lessons were originally recorded inside the Taskade "Genesis Build Progress" project as a post-audit wrap-up. They are durable — each describes a rule that should apply to every future game in the studio — and therefore belong in the repo learning-capture archive.

Note: the Taskade-side Fire Dispatch game referenced in these lessons is the React version of Fire Dispatch in the parallel Taskade "Studio OS" codebase. This repo's review build at `reviews/fire/current/index.html` is a separate HTML implementation. The engineering lessons below are implementation-agnostic — they apply to both.

## The seven lessons

### LESSON 1 — Remainder traps require non-divisible numbers

M3 (remainder blindness) is only testable when `dividend ÷ divisor` has a non-zero remainder. An old version of Fire Dispatch round R8 was `20 ÷ 4 = 5` (exact) — the trap was impossible because there was no remainder to ignore.

**Rule:** For any division round that targets remainder misconceptions, always verify at generation time:
- `answer = floor(totalPool / trucksPerUnit)`
- `totalPool mod trucksPerUnit > 0`

**Applies to:** every future game using remainder mechanics (division, ceiling division, modular allocation).

### LESSON 2 — Equation reveal must match the operation the student used

A divide round showing `trucksPerUnit × units = answer` is wrong — the student used division, not multiplication. The reveal should reflect the operation the player performed, not the inverse.

**Rule:** Always branch the reveal on `round.block` (or whatever field encodes the operation type):
- Divide rounds show `totalPool ÷ trucksPerUnit = answer [r remainder]`
- Multiply rounds show `trucksPerUnit × units = answer`

**Applies globally** to any game that reveals an equation at round end.

### LESSON 3 — Progressive hints are better than flat hints

Two-tier hint structure:
- `wrongHint` (shown after attempt 1) — should direct thinking without revealing the operation
- `wrongHint2` (shown after attempt 2+) — can name the error pattern explicitly (e.g. *"9+5 is only 14. Each gate needs 9 trucks independently: 9 × 5"*)
- **Neither** hint should reveal the numeric answer

**Pattern:**
- Attempt 1 = strategy prompt
- Attempt 2 = name the misconception

**Applies to:** Echo Heist and all future games.

### LESSON 4 — Boss rounds need hint suppression

Final / boss rounds should mark `isBossRound = true` and suppress all hints. The UI should label the round "Boss round · no hints" so students understand the rule change.

**Applies to:** any game with a final challenge round.

### LESSON 5 — Multi-step rounds need a visible step indicator

When a round requires two cognitive steps (e.g. multiply then verify against fleet), show a `stepLabel` in the HUD: *"Step 1: multiply · Step 2: verify fleet"*.

This does NOT replace a locked two-step UI (which is a P2 item) but it meaningfully scaffolds without giving the answer.

**Applies to:** any multi-step round in any game.

### LESSON 6 — Audit cross-cutting text strings separately

Cross-cutting subtraction-language audit must grep ALL strings:
- `prompts`
- `wrongHint` and `wrongHint2`
- `designNotes`
- UI labels

The Fire Dispatch tracker row for "subtraction-division confusion" passed because all strings were clean — but this was only discoverable by reading every string explicitly.

**Rule:** Build a string-search step into every future audit, not just a per-round content check.

### LESSON 7 — Time pressure is architectural, not cosmetic

The Fire Dispatch tracker spec called for `≤ 4s` response windows for hard facts. This cannot be bolted onto a static input — it requires a countdown timer component with grace periods, visual escalation, and recovery behaviour.

**Rule:** Tag time-pressure gaps as **"P2 architectural"**, not **"FAIL"**, in P1 audits. Document in the tracker as `WARN` with a specific P2 implementation note and a concrete design plan for how the timer will escalate (see CO-4 in [`docs/build_standards_gate.md`](../../docs/build_standards_gate.md) for the escalation spec).

## Classification and promotion target

All seven are **reusable engineering rules** that should inform:

1. **`docs/build_standards_gate.md`** — Lessons 1, 2, 3, 6, 7 inform existing CO / MG items. Lessons 4 and 5 may deserve new items (e.g. MG-7 boss-round hint suppression, CO-7 multi-step step indicator). Propose as future amendments to the gate.
2. **`docs/pass_rules.md`** — these are pass-closure learnings that may warrant promotion into the durable pass rules once reviewed.
3. **Per-game specs** — any new prototype spec for a game with remainder, reveal, multi-attempt hints, boss round, or multi-step content must address these lessons explicitly in its compliance block.

## Related repo documents

- [`docs/build_standards_gate.md`](../../docs/build_standards_gate.md) — the Stage 8.5 gate these lessons inform
- [`docs/pass_rules.md`](../../docs/pass_rules.md) — durable pass rules
- [`artifacts/pass_records/fire-dispatch-pass-1.json`](../pass_records/fire-dispatch-pass-1.json) through `fire-dispatch-pass-3.json` — repo-side Fire Dispatch pass records
- [`artifacts/qa_audits/fire-dispatch-audit.md`](../qa_audits/fire-dispatch-audit.md) — the full audit write-up that produced these lessons
- [`reviews/fire/current/index.html`](../../reviews/fire/current/index.html) — repo-side review build
