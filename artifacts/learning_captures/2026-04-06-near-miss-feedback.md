# Lesson: Near-miss feedback must distinguish close from far

| Field | Value |
|---|---|
| **Date** | 2026-04-06 |
| **Source** | audit |
| **Game(s)** | Fire Dispatch |
| **Pass** | P2B |
| **Classification** | pass-specific rule |
| **Game family** | combination-allocation |
| **Failure mode** | Board total of 14/15 and 3/15 looked identical — both grey, both disabled. No proximity signal. |
| **Tags** | near-miss, proximity, feedback, running-total, dispatch |

## What happened
Fire Dispatch's dispatch board showed the running total in grey with "of X" for all non-matching states. A total of 14 against demand 15 (one truck away) was visually identical to a total of 3 against demand 15 (far off). The player had no way to feel they were close.

## What the OS should learn
Any game with a running total vs target must visually distinguish near-miss (within 1-2 of target) from far-off — using color, label, or both.

## Evidence
Fix commit `2a9cfdb`. Added amber color + "N away" label when gap is 1-2. Three-state system: grey (far) → amber (near) → green (match). Unit Circle already had this pattern (correct/close/miss) but Fire Dispatch was missing it.

## Applies to future games when
The player builds a running total toward a target and the game needs to signal proximity before the player commits.

## Promotion target
`docs/pass_rules.md` under P2B Rule 3 (near miss and real miss must feel different)

## Status
- [x] Captured
- [x] Promoted to: already enforced by P2B Rule 3; this capture adds the specific implementation pattern
