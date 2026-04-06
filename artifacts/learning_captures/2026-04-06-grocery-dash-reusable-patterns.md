# Lesson: Grocery Dash — Reusable Patterns (awaiting library justification)

| Field | Value |
|---|---|
| **Date** | 2026-04-06 |
| **Source** | strong example (Grocery Dash live playthrough + source analysis) |
| **Game(s)** | Grocery Dash (reference) |
| **Pass** | N/A — design patterns |
| **Classification** | reusable pattern (stored here until pattern library expansion is justified) |

## What happened
Six reusable patterns were extracted from Grocery Dash. Some already exist partially in `docs/reusable_patterns_library.md`. Stored here as structured captures until the library is expanded.

## Patterns

### 1. Checkout Receipt as Worked Example
After the player attempts the math, show the full worked solution as a world artifact. Each line: `recipe_amount × scale_factor = total_needed — got X ✓/✗`. Player sees where reasoning matched or failed — but only after the struggle.
- Partially exists as "missed-fact review" in current library
- Grocery Dash receipt is the strongest implementation

### 2. Physical Antagonist for Embodied Urgency
An NPC that physically pursues the player (greedy pathfinding, ~520ms moves). Consequence: drops a random cart item. Creates moment-to-moment tension that abstract timers cannot. Optimal response: "compute first, then move decisively."
- Partially referenced in current engagement rules
- Grocery Dash manager is the strongest implementation

### 3. Freeze-on-Collision as Social Obstacle
Wandering NPCs that freeze the player for 5 seconds on contact. Spatial awareness tax, not a math penalty. Introduced after the math loop is learned (L4+), escalating 1→5 NPCs.

### 4. Pack Variant Optimization
Two shelf options for the same ingredient with different pack sizes. Player computes ceiling division for each, chooses less waste. Introduced at L4, grows to most ingredients by L12. Creates the "better than correct" layer above rote computation.

### 5. Progressive Feature Introduction Ladder
L1-L3: learn the loop (no pressure). L4: first big jump (NPCs + distractors + variants). L5+: one new axis per level. Randomization at L9+ after 8 fixed levels. Exact pattern reusable for any 10+ level game.

### 6. Distractor Items on Shelves
Wrong items that look similar to correct ones, placed on the same shelves. Forces active cross-referencing with the recipe card. Escalates 0→5 across 12 levels. Checkout blocks if distractors in cart.

## Promotion target
`docs/reusable_patterns_library.md` — add when library expansion is justified

## Status
- [x] Captured
- [ ] Promoted to: docs/reusable_patterns_library.md
