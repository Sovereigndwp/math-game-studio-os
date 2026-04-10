# Fire Dispatch — Question Audit (scaffold)

## Header

| Field | Value |
|---|---|
| **Game** | Fire Dispatch |
| **Audit status** | **Scaffold only — template rows authored, no audit findings yet recorded in Taskade source** |
| **Origin** | normalized from Taskade project `ZpbMJ7Dvpt9NVxmN` ("Fire Dispatch — Question Audit Results") |
| **Raw source** | [`taskade_exports/projects/ZpbMJ7Dvpt9NVxmN.json`](../../taskade_exports/projects/ZpbMJ7Dvpt9NVxmN.json) |
| **First normalized into repo** | 2026-04-10 |

## Scope note

The Taskade source project for this audit currently contains **only the template row structure** — no per-row findings, severity marks, or fix tasks have been authored yet. Running the audit is a tracked GAP in the Taskade "Genesis Build Progress" log (*"No equivalent QA Pipeline for Bakery Rush or Fire Dispatch templates"*).

This file exists so that the expected row structure is durable in the repo and the audit can be filled in with findings once it is run. When findings exist, they should be added in-place under the matching row headings below.

**Note on which Fire Dispatch build is in scope:** this repo has an active Fire Dispatch review build at [`reviews/fire/current/index.html`](../../reviews/fire/current/index.html) with pass records in [`artifacts/pass_records/`](../pass_records/). There is also a separate Fire Dispatch in the parallel "Studio OS" React codebase. The Taskade audit template does not specify which build it targets. **Any findings recorded here must name the build audited.**

## Template rows (FD-T1 through FD-T4)

### FD-T1 — Multiplication Fact Recall
*No findings recorded yet.*

### FD-T2 — Division as Partitioning
*No findings recorded yet.*

### FD-T3 — Multi-Step Dispatch
*No findings recorded yet.*

### FD-T4 — Remainder / Ceiling
*No findings recorded yet.* See also [`artifacts/learning_captures/2026-04-09-fire-dispatch-audit-lessons.md`](../learning_captures/2026-04-09-fire-dispatch-audit-lessons.md) Lesson 1: remainder traps require non-divisible numbers.

## Mission rows (FD-M1 through FD-M8)

### FD-M1 — Intro: Single-Zone Dispatch
*No findings recorded yet.*

### FD-M2 — Multiply: 2–4 Tables
*No findings recorded yet.*

### FD-M3 — Multiply: 5–9 Tables
*No findings recorded yet.*

### FD-M4 — Divide: Partition 12–36
*No findings recorded yet.*

### FD-M5 — Divide: Inverse Multiplication
*No findings recorded yet.*

### FD-M6 — Multi-Step: Multiply then Divide
*No findings recorded yet.* See Lesson 2 in the learning capture (equation reveal must match the operation used) and Lesson 5 (multi-step rounds need a visible step indicator).

### FD-M7 — Multi-Step: Remainders
*No findings recorded yet.*

### FD-M8 — Boss Round: Full Dispatch
*No findings recorded yet.* See Lesson 4 in the learning capture (boss rounds need hint suppression).

## Cross-cutting issues

### Repeated-Addition Bypass
*No findings recorded yet.*

### Subtraction-Division Confusion
*No findings recorded yet.* Note from Lesson 6: audit must grep ALL strings (prompts, `wrongHint`, `wrongHint2`, `designNotes`, UI labels) — a pass here requires explicit string-level verification, not just per-round checks.

## Related repo documents

- [`artifacts/learning_captures/2026-04-09-fire-dispatch-audit-lessons.md`](../learning_captures/2026-04-09-fire-dispatch-audit-lessons.md) — seven cross-game engineering lessons derived from the Fire Dispatch audit (the learnings exist even though the per-row findings do not)
- [`artifacts/pass_records/fire-dispatch-pass-1.json`](../pass_records/fire-dispatch-pass-1.json) through `-pass-3.json` — repo-side Fire Dispatch pass records
- [`reviews/fire/current/index.html`](../../reviews/fire/current/index.html) — repo-side review build
- [`docs/build_standards_gate.md`](../../docs/build_standards_gate.md) — Stage 8.5 gate (CO / MG checks that apply to Fire Dispatch templates)
- [`memory/registries/family_registry.json`](../../memory/registries/family_registry.json) — Fire Dispatch family placement (currently `Pending Formal Family Placement`, `interaction_type: route_and_dispatch`)
