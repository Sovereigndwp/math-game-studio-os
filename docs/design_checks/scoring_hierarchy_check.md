# Scoring Hierarchy Check

## Purpose
Verify that the scoring system explicitly teaches the player which action matters most, and that neglect is penalized far more than honest mistakes.

## Use this when
- After core loop design, before implementation
- When scoring feels flat or arbitrary
- Before P2B if the player can succeed by ignoring the math

## Controls
- Whether the scoring teaches the right lesson
- Whether the penalty structure encourages trying over ignoring
- Whether the highest-scoring action is the intended core skill

## Do not use this for
- Star rating thresholds (P2A)
- Difficulty tuning (P2B)
- Visual feedback design (P3)

---

## Evaluation

### A. Is the core math action the highest-scoring single action?
Can the player outscore the math action by doing well at everything else?

Bad: Dispatch = +40, correct math = +40 (both equal — math is not privileged)
Good: Correct math = +100, dispatch = +40 (math is 2.5× more valuable)

**Score:** [math dominant / equal / math subordinate]

### B. Is a wrong answer cheap and recoverable?
Can the player recover from one mistake within the same round?

Bad: Wrong answer = -100 (half a round's progress lost)
Good: Wrong answer = -20 (recoverable in one more correct answer)

**Score:** [recoverable / painful / fatal]

### C. Is neglect catastrophically more expensive than honest mistakes?
Does ignoring a problem cost much more than attempting and failing?

Bad: Timeout = -20, same as wrong answer (no difference between trying and ignoring)
Good: Timeout/abort = -200, wrong answer = -20 (10× penalty for neglect)

**Score:** [catastrophic neglect / moderate neglect / no distinction]

### D. Can the player read the scoring and understand what matters?
Without being told in words, does the scoring table make priorities clear?

Bad: All actions worth similar points — no signal
Good: +100 math / +40 dispatch / -20 wrong / -200 neglect — clear hierarchy

**Score:** [self-teaching / ambiguous / misleading]

---

## Output Template

```markdown
# Scoring Hierarchy: [Game Name]

**Hierarchy clarity:** [0.0 - 1.0]

**Highest-scoring action:** [what it is and how many points]
**Core math action value:** [points]
**Non-math action value:** [points]
**Wrong answer penalty:** [points]
**Neglect penalty:** [points]

**Does scoring teach what matters?** [yes / partially / no]

**Recommendation:**
[One focused action]
```

---

*Source: ATC Math Tower. Correct math (+100) is worth 2.5× more than dispatch (+40). Wrong answer (-20) is 10× cheaper than neglect (-200). The scoring itself is the curriculum.*
