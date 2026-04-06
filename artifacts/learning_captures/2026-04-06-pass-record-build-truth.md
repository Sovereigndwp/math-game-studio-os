# Lesson: Pass records must describe the current build, not a previous prototype

| Field | Value |
|---|---|
| **Date** | 2026-04-06 |
| **Source** | audit |
| **Game(s)** | Bakery Rush |
| **Pass** | cross-pass |
| **Classification** | local fix |
| **Game family** | none |
| **Failure mode** | Pass-2 record described belt ramp [18,13,9,6,4] but current Vite source had always used [9,8,7,6,5]. The record described a different prototype build that was never carried into the current source. |
| **Tags** | pass-record, source-of-truth, build-drift, documentation-accuracy |

## What happened
Bakery Rush was rebuilt from a standalone HTML prototype into a Vite/React app. The pass-2 record documented tuning done on the old prototype (belt halved from 9s to 18s at L1). The current source file never contained those values — it was built fresh with `conveyorDuration: [9, 8, 7, 6, 5]`. The audit flagged this as a possible regression, but investigation showed it was a different parameterization (animation loop duration vs raw timer), not a revert.

## What the OS should learn
Pass records must describe the current live build, not a previous prototype. When a game is rebuilt on a new stack, pass records from the old stack should be annotated with a build note explaining the discrepancy.

## Evidence
Audit finding in stage confirmation audit. Clarification commit `a4bb2e0` added `_build_note` to `bakery-rush-pass-2.json`. Git history confirmed `conveyorDuration: 9` existed in every commit of the Vite source.

## Applies to future games when
A game is rebuilt on a different stack (standalone HTML → Vite, etc.) and old pass records exist from the previous build.

## Promotion target
None — local fix only. The discipline is: always verify pass records against current code, not memory.

## Status
- [x] Captured
- [x] Promoted to: none (annotated in the pass record itself)
