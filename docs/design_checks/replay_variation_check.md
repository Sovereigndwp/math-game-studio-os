# Replay Variation Check

## Purpose
Verify that replaying the same level generates genuinely different mathematical problems, not just cosmetic differences.

## Use this when
- After core loop design, before implementation
- Before P4 (replay) to assess whether variation exists
- When a game feels repetitive after two sessions

## Controls
- Whether replay produces real math variation
- Whether fixed inputs are used appropriately during learning phases
- Whether randomized inputs appear in mastery phases

## Do not use this for
- Content volume ("add more levels")
- Visual variety or theming
- Difficulty tuning (P2B)

---

## Evaluation

### A. What changes on replay?
List every variable that differs between two plays of the same level.

Bad: Only customer names or visual order change (cosmetic)
Good: Guest count changes, which changes every multiplication and division problem

**Score:** [math changes / presentation changes / nothing changes]

### B. Is there a learning phase with fixed inputs?
Are early levels predictable so the player can learn the loop before randomization?

Bad: Everything is random from L1 (player can't learn from retry)
Good: L1-L8 fixed (learnable), L9+ randomized (genuine replay)

**Score:** [well-phased / no learning phase / no mastery phase]

### C. Does the variation create different optimal strategies?
Does a different random input change which actions are best?

Bad: Different numbers, same strategy every time
Good: 6 guests vs 12 guests means different pack choices, different ceiling division, different optimization

**Score:** [strategy changes / minor changes / identical strategy]

### D. Can the player memorize their way through?
After 3 plays, can the player solve by memory instead of reasoning?

Bad: Same 15 angles every session (Unit Circle current state)
Good: Random guest counts mean the math is genuinely different (Grocery Dash L9+)

**Score:** [cannot memorize / partially memorizable / fully memorizable]

---

## Output Template

```markdown
# Replay Variation: [Game Name]

**Variation strength:** [0.0 - 1.0]

**What changes on replay:**
[List]

**What stays the same:**
[List]

**Main memorization risk:**
[One sentence]

**Recommendation:**
[One focused action]
```

---

*Source: Grocery Dash audit. Random guest counts on L9-L12 are the gold standard — same level, fundamentally different math each play.*
