# Lesson: Grocery Dash — Game-Family Rules (awaiting second example)

| Field | Value |
|---|---|
| **Date** | 2026-04-06 |
| **Source** | strong example (Grocery Dash live playthrough + source analysis) |
| **Game(s)** | Grocery Dash (reference), Fire Dispatch (partial application) |
| **Pass** | N/A — pre-build design rules |
| **Classification** | game-family rule (awaiting promotion to docs/game_families/) |

## What happened
Three game-family rules were identified from Grocery Dash that are powerful but need a second strong example before creating dedicated family docs.

## Rules awaiting promotion

### 1. Constant-Total Complement Prevention (combination/allocation games)
In any game where the player selects from a fixed set to reach a target, the available options must not sum to a predictable constant. If they do, the player solves by exclusion instead of combination. Break the constant by varying available options per incident.
- Already applied: Fire Dispatch truck exclusion fix
- Awaiting: second combination game to justify `docs/game_families/combination-allocation.md`

### 2. Physical Consequence Proportional to Error Severity (spatial/navigation games)
In games with physical space, correction cost should reflect error magnitude, not distance to the correction point. A one-item overshoot on a far shelf costs more than a three-item undershoot on a near shelf — that's distance-proportional, not error-proportional.
- Identified in: Grocery Dash audit (noted as a weakness)
- Awaiting: second spatial game to justify `docs/game_families/spatial-navigation.md`

### 3. Worked Solution After Attempt Only (recipe/scaling games)
Never show the answer during play. Show the full worked solution — with the multiplication chain, pack math, and per-ingredient verdict — only after the player commits. The receipt teaches without preempting reasoning.
- Best example: Grocery Dash checkout receipt
- Awaiting: second recipe/scaling game to justify `docs/game_families/recipe-scaling.md`

## Promotion target
`docs/game_families/` — create individual family docs when each rule has 2+ supporting games

## Status
- [x] Captured
- [ ] Promoted to: docs/game_families/ (awaiting second examples)
