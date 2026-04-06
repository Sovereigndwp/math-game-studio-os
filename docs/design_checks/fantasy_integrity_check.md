# Fantasy Integrity Check

## Purpose
Test whether the game's fantasy truly carries the math, or whether the theme is pasted on top of a worksheet.

## Use this when
- After the Game Experience Spec, before implementation
- When a concept feels promising but suspiciously flat
- Before P3 if the game still feels like a tool despite working mechanics

## Controls
- Whether the fantasy is strong enough to justify building
- What specific worksheet-in-costume risks exist
- What must change before the theme will carry the math

## Do not use this for
- Dialogue writing or lore generation
- Visual design decisions
- Pass-by-pass tuning
- Technical implementation

---

## Evaluation

### A. Role necessity
Does the role naturally require the math?

Bad: "You are a chef" (but the math is just a gate before cooking)
Good: "You are a baker filling orders — the math IS the box-packing"

**Score:** [strong / adequate / weak]
**Evidence:**

### B. World logic
Do the rules of the world make the math feel inevitable?

Bad: "Solve 7+5 to unlock the next room"
Good: "The fire needs 12 units of capacity — which trucks add up to exactly 12?"

**Score:** [strong / adequate / weak]
**Evidence:**

### C. Decision meaning
Does the theme change what the player's choices mean?

Bad: "Pick the right answer" (same in any theme)
Good: "Send the Tanker+Ladder or Engine+Rescue? Both hit 8 but different trucks are needed for the next call"

**Score:** [strong / adequate / weak]
**Evidence:**

### D. Emotional fit
Does the fantasy create a feeling the math alone would not create?

Bad: "Correct! +10 points"
Good: "Family rescued. House saved." (the stakes are human, not numeric)

**Score:** [strong / adequate / weak]
**Evidence:**

### E. Replaceability test
If the theme were swapped to something completely different, would the loop lose real meaning or just some visuals?

- Loses real meaning → fantasy is integral
- Loses only visuals → fantasy is decoration

**Score:** [integral / partial / decoration]
**Evidence:**

---

## Output Template

```markdown
# Fantasy Integrity: [Game Name]

**Fantasy strength:** [0.0 - 1.0]

**Strongest fantasy element:**
[One sentence]

**Strongest fantasy weakness:**
[One sentence]

**Main worksheet-in-costume risk:**
[One sentence]

**Recommendation before build:**
[One focused action]
```

---

*This is a lightweight design check, not a full agent.
Promote to a formal agent only if used on 5+ concepts and consistently improving outcomes.*
