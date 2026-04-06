# Satisfaction Loop Check

## Purpose
Test whether the core loop is actually satisfying to repeat, not just structurally sound.

## Use this when
- After core loop design, before implementation
- When a game feels mechanically okay but emotionally weak
- After P1 if the game feels repetitive or mechanical despite working correctly

## Controls
- Whether the loop is satisfying enough to justify building
- What specific flatness or repetition risks exist
- What must change before the loop will feel good to repeat

## Do not use this for
- Adding many new mechanics
- Theme or personality decisions (use fantasy integrity check)
- Difficulty tuning (use P2B)
- Visual polish

---

## Evaluation

### A. Rhythm
Does the loop have a satisfying cadence?

Bad: Same pace, same weight, same timing every cycle
Good: Build tension, commit, resolve — with varied tempo across difficulty

**Score:** [strong / adequate / weak]
**Evidence:**

### B. Action consequence
Does each action visibly matter?

Bad: Tap a thing, number changes, next thing appears
Good: Pastry springs into box, total pulses, customer reacts

**Score:** [strong / adequate / weak]
**Evidence:**

### C. Feedback quality
Does the loop produce enough response to feel alive?

Bad: Correct = green, wrong = red, move on
Good: Correct = spring animation + score fly-up + streak counter + character smile

**Score:** [strong / adequate / weak]
**Evidence:**

### D. Depth through repetition
Does repeating the loop reveal more mastery or only more sameness?

Bad: Round 1 and round 10 feel identical except the numbers are bigger
Good: Round 10 requires strategy that round 1 did not — player discovers depth

**Score:** [strong / adequate / weak]
**Evidence:**

### E. Reward shape
Does success feel better than mere correctness?

Bad: "Correct!" (same every time)
Good: Tiered celebration scaled to difficulty — easy correct gets a nod, hard correct gets FLAWLESS

**Score:** [strong / adequate / weak]
**Evidence:**

### F. Friction source
Is the friction coming from the right skill?

Bad: Player struggles with controls, not with math
Good: Player struggles with the intended mathematical reasoning under pressure

**Score:** [right skill / mixed / wrong skill]
**Evidence:**

---

## Output Template

```markdown
# Satisfaction Loop: [Game Name]

**Loop satisfaction:** [0.0 - 1.0]

**Strongest source of satisfaction:**
[One sentence]

**Strongest source of flatness:**
[One sentence]

**Main repetition risk:**
[One sentence]

**Recommendation before build:**
[One focused action]
```

---

*This is a lightweight design check, not a full agent.
Promote to a formal agent only if used on 5+ concepts and consistently improving outcomes.*
