# Build Standards Gate (Stage 8.5) — Prototype Engineer → Software Developer

## Purpose and scope

This document is the **repo-side authoritative reference** for the Stage 8.5 Build Standards Gate. No spec may be handed to the Software Developer unless all CRITICAL items here are RESOLVED or explicitly marked N/A. The Taskade-side Game Build Standards Agent reads the corresponding Taskade project (`pBj7H2VZq1WPfZBs`) when evaluating any prototype spec; this document is the durable repo mirror of that policy.

The gate sits between the Prototype Engineer (Stages 6–8) and the Software Developer. It is the final quality gate before any production code is written.

| Position | Owner | Output |
|---|---|---|
| **Upstream** | Prototype Engineer (Stages 6–8) | Prototype spec draft |
| **This gate** | Game Build Standards Agent | GREEN / AMBER / RED + compliance block |
| **Downstream on GREEN** | Software Developer | Production build begins |
| **Downstream on RED** | Prototype Engineer | Spec returned with a specific revision list |
| **Downstream on AMBER** | Prototype Engineer + Pipeline Orchestrator | Conditional approval + explicit plan |

This document is policy. Historical repo snapshots do not override it. See [`docs/taskade_app_reference.md`](taskade_app_reference.md) for the division between Taskade live operational state and repo durable artifacts.

## Gate status definitions

- **GREEN** — all CO and MG items RESOLVED or N/A. Spec is cleared for Software Developer handoff.
- **AMBER** — one or more items partially resolved with a concrete plan and owner. Handoff is conditional on plan approval.
- **RED** — one or more CRITICAL items unresolved. Spec is BLOCKED. Returns to Prototype Engineer for revision. Do not hand to Software Developer.

## Clarity Obligations (CO) — required on every spec

### CO-1 — First Interaction Experience (CRITICAL)
- The spec must describe what the player sees on the first interactive moment (terminal, door, prompt, challenge).
- The game objective must be stated BEFORE the first penalty-triggering action is possible.
- First popup or first interactive moment must communicate: (a) what the player is trying to accomplish, (b) what they are expected to type or do, (c) what the consequences of a wrong answer are — before any penalty is incurred.
- If no intro or onboarding overlay is included, the spec must explicitly state why one is not needed.

### CO-2 — Cost Labeling Completeness (CRITICAL)
- Every cost or penalty must be labeled at the exact moment it is incurred.
- Required format: resource name + direction + quantity. Examples: `Heat +10`, `Score −50 pts`, `+20 Heat`.
- Vague labels like "costs heat" or "−50" with no unit are NOT acceptable. Spec must list every cost and confirm each has a labeled moment of display.

### CO-3 — Time-Critical Information in Popup (CRITICAL if applicable)
- If any mechanic continues while a popup is open (guards moving, timers counting, heat rising), the popup must contain a visible note stating this.
- The spec must specify exactly what text appears in the popup to communicate ongoing time pressure. If nothing continues during popups, state that explicitly.

### CO-4 — Timer Escalation (CRITICAL if applicable)
- Every countdown timer must specify visual and audio signals at:
  - `< 30s` — color change
  - `< 15s` — REQUIRED secondary signal: flashing border, pulsing banner, or screen overlay
  - `< 5s` — REQUIRED high-urgency signal
- A timer that expires without escalating warning is classified as AP-4 HIGH anxiety point by default.

### CO-5 — Answer Format Persistence (CRITICAL)
- Accepted formats (integers, decimals, fractions, percentages, negatives) must be shown on the first popup via intro overlay or hint panel.
- On all subsequent popups: a persistent compact reference (badge row, subtitle, tooltip) must be specified. Formats shown only once are classified as AP-6 LOW anxiety point by default.

### CO-6 — Escape / Cancel / Skip Semantics (CRITICAL)
- Every skip/cancel/escape action must be (1) named specifically (not just "cancel" — use "skip", "abandon", "exit"), (2) quantified (e.g. `+20 Heat`), (3) grounded in game fiction if possible.
- The spec must state the exact label text for every skip/cancel/escape action in the game.

## Math Generation Rules (MG) — required for procedural question games

### MG-1 — Float Precision (CRITICAL)
- NEVER use `parseFloat((x).toFixed(n))` to produce a clean answer — produces float artifacts (e.g. `0.30000000000000004`).
- ALWAYS use a `roundTo(val, decimals)` helper. Canonical implementation:
  ```javascript
  function roundTo(val, decimals) {
    return Number(Math.round(+(val + 'e' + decimals)) + 'e-' + decimals);
  }
  ```
- For rounding-to-nearest-b problems, use `roundTo(Math.round(a/b)*b, 2)` — NOT `roundTo(a, 2)`.
- Spec must state which templates produce float answers and confirm `roundTo()` is used in each.

### MG-2 — Degenerate Case Guards (CRITICAL)
- **Tie guard** — for any A-vs-B comparison question, if computed values are equal within 0.01 tolerance, `gen()` must retry via `do/while` loop with a try counter.
- **Trivial answer guard** — any answer below the minimum meaningful threshold (e.g. `< 3` for fraction-of-quantity problems) must be regenerated. Spec must state the minimum threshold per template type.
- **Zero/one guard** — division, ratio, and rate problems that produce `0` or `1` as an answer must be explicitly guarded.

### MG-3 — Null Return Contract (CRITICAL)
- If any `mk()` function can return `null`, the calling `pickPrompts()` function MUST implement a retry loop:
  ```javascript
  if (!res) { i--; continue; }
  ```
- This is a system-level contract — not a per-template decision. If ANY template can return null, the retry contract must be in the spec.

### MG-4 — Hint Correctness (CRITICAL)
- `hint2` must set up the computation WITHOUT completing it. It must never contain the answer.
- For comparison templates (A vs B), `hint2` must NOT show computed rates or values directly — it must ask the student to compare, not pre-compute for them.
- Hints containing computed answers are answer-reveals, not hints. The spec must flag and fix any such case.

### MG-5 — Randomization Collision Budget
- Estimate the number of distinct outputs for each template.
  - `< 20` distinct outputs → **HIGH** collision risk flag
  - `20–50` → **MEDIUM**
  - `> 50` → acceptable

### MG-6 — Answer Bias Check
- For any template with a binary or categorical answer (A/B, True/False, Greater/Less), verify neither answer is systematically more likely across the parameter space.
- If bias exists, a shuffle or rebalancing step must be added to the generator. Spec must confirm this is in place.

## Named Anxiety Points — pre-build check

These six anxiety point types were derived from the Echo Heist audit (see [`artifacts/qa_audits/echo-heist-audit-2026-04-07.md`](../artifacts/qa_audits/echo-heist-audit-2026-04-07.md)). The Build Standards Agent checks for all six in every spec before approving handoff.

| Code | Name | Severity | Resolution |
|---|---|---|---|
| **AP-1** | Penalties Before Objectives | HIGH | First-use intro overlay |
| **AP-2** | Silent Wrong-Answer Consequence | HIGH | Inline feedback with correct answer + delta (e.g. `✗ Incorrect — answer: [X] · Heat +5`) |
| **AP-3** | Silent Mechanics During Popup | MEDIUM | Persistent note in popup hint line (e.g. `· ⚠ Guards still moving!`) |
| **AP-4** | Timer Expiry Without Escalation | MEDIUM | `isUrgent = remaining <= 15` → enlarged text + pulsing amber banner + low-alpha full-screen flash |
| **AP-5** | Cost Without Fiction | LOW | CSS `:hover` tooltip on cost label with a one-sentence fiction reason |
| **AP-6** | Format Reminder Absent After First Use | LOW | Hidden `<div>` revealed on second+ popups when `mathIntroSeen === true`, showing accepted-formats badge row |

## Compliance statement template

Every spec evaluated by the Build Standards Agent must produce this compliance block:

```
- CO-1 First Interaction:      [RESOLVED / UNRESOLVED — explain]
- CO-2 Cost Labeling:          [RESOLVED / UNRESOLVED — explain]
- CO-3 Time-Critical in Popup: [RESOLVED / N/A — explain]
- CO-4 Timer Escalation:       [RESOLVED / N/A — explain]
- CO-5 Answer Format Persist:  [RESOLVED / UNRESOLVED — explain]
- CO-6 Escape Semantics:       [RESOLVED / N/A — explain]
- MG-1 Float Precision:        [RESOLVED / N/A — explain]
- MG-2 Degenerate Case Guards: [RESOLVED / N/A — explain]
- MG-3 Null Return Contract:   [RESOLVED / N/A — explain]
- MG-4 Hint Correctness:       [RESOLVED / N/A — explain]
- MG-5 Collision Budget:       [RESOLVED / N/A — explain]
- MG-6 Answer Bias:            [RESOLVED / N/A — explain]
- OVERALL PRE-BUILD STATUS:    [GREEN / AMBER / RED]
```

## Relationship to other repo gates

| Gate | Stage | Source | Role |
|---|---|---|---|
| [`docs/pre_build_excellence_checklist.md`](pre_build_excellence_checklist.md) | Concept-stage ("is this worth building?") | Repo-native | Sits before Delight Gate scoring |
| [`docs/delight_gate.md`](delight_gate.md) | Concept go/no-go | Repo-native | Scores concepts pass/fail for pipeline advancement |
| **This document (Build Standards Gate)** | Stage 8.5 ("is the spec safe to build?") | Taskade-originated policy | Sits between Prototype Engineer and Software Developer |
| [`docs/release_blockers.md`](release_blockers.md) | Pre-release | Repo-native | Final release-time blockers |

The four gates are complementary, not overlapping. The Build Standards Gate does NOT evaluate whether a concept is worth building (that is the Delight Gate), and does NOT evaluate shipping readiness (that is release gating). It evaluates whether a specific prototype spec can be handed to a developer without known clarity or math-generation failure modes.

## Document metadata

| Field | Value |
|---|---|
| **Path** | `docs/build_standards_gate.md` |
| **Status** | durable policy |
| **Origin** | normalized from Taskade project `pBj7H2VZq1WPfZBs` ("Build Standards Checklist — Prototype Engineer → Software Developer Gate") |
| **Raw source** | [`taskade_exports/projects/pBj7H2VZq1WPfZBs.json`](../taskade_exports/projects/pBj7H2VZq1WPfZBs.json) |
| **Markdown source** | [`taskade_exports/markdown_renderings/Build_Standards_Checklist_—_Prototype_Engineer_→_Software_Developer_Gate.md`](../taskade_exports/markdown_renderings/Build_Standards_Checklist_—_Prototype_Engineer_→_Software_Developer_Gate.md) |
| **First normalized into repo** | 2026-04-10 |
| **Maintainer** | not yet decided (owner is a Taskade governance gap — see [`docs/taskade_app_reference.md`](taskade_app_reference.md)) |
