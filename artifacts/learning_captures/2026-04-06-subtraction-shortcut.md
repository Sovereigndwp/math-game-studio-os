# Lesson: Constant-total subtraction shortcut in combination games

| Field | Value |
|---|---|
| **Date** | 2026-04-06 |
| **Source** | fix |
| **Game(s)** | Fire Dispatch |
| **Pass** | P2B |
| **Classification** | game-family rule |
| **Game family** | combination-allocation |
| **Failure mode** | All available options sum to a fixed constant, allowing the player to solve by subtraction from the total instead of genuine combination |
| **Tags** | constant-total, complement, subtraction, subset-sum, truck selection |

## What happened
Fire Dispatch had 5 trucks summing to exactly 20 (5+3+2+4+6). At L3-L5 where all trucks were available, the player could solve any demand by computing 20-demand to identify which trucks to exclude, bypassing the intended subset-sum addition reasoning.

## What the OS should learn
In any game where the player selects from a fixed set to reach a target, the available options must not sum to a predictable constant — vary the available set per incident.

## Evidence
Fix commit `1725a07`. Per-incident truck exclusion at L3+ breaks the constant total. Solvability verified for all 5 possible 4-truck subsets across all level demand ranges.

## Applies to future games when
The game presents a fixed set of options (trucks, items, tiles) and asks the player to select a subset that sums to a target. Check whether the full set sums to a constant.

## Promotion target
`docs/game_families/combination-allocation.md` (when 2+ games in family)

## Status
- [x] Captured
- [ ] Promoted to: docs/game_families/combination-allocation.md
