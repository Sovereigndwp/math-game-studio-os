# Consequence Quality Check

## Purpose
Verify that math errors produce consequences the player can feel in the game world, not just number changes on a score counter.

## Use this when
- After the Game Experience Spec, before implementation
- When a game feels correct but consequence-free
- Before P2B if errors have no visible impact on the world

## Controls
- Whether the consequence design is strong enough to teach from mistakes
- What specific consequence gaps exist
- What must change before errors will feel meaningful

## Do not use this for
- Visual polish or animation quality
- Difficulty tuning (P2B)
- Personality or charm (P3)

---

## Evaluation

### A. Does the player see the consequence happen?
When the player makes a math error, is there a visible event in the game world?

Bad: Score changes from 100 to 80 (number change only)
Good: Customer walks away, item falls from cart, checkout blocks your entry

**Score:** [visible / partially visible / invisible]

### B. Is the consequence proportional to the error?
Does a small error cost less than a big error?

Bad: All errors cost the same -20 points
Good: Small overshoot costs 2s patience, large miss loses the customer entirely

**Score:** [proportional / flat / inverted]

### C. Does the consequence teach what went wrong?
Can the player learn from the consequence itself, or only from a separate feedback message?

Bad: "Wrong! -10 points" (no information about the error)
Good: Checkout says "Bread: need 12 slices, got 20 — return some" (names the gap)

**Score:** [diagnostic / vague / silent]

### D. Is the consequence world-grounded?
Does the consequence make sense in the game's world, or is it abstract?

Bad: Red flash and a buzzer sound
Good: Manager catches you and an item drops from your cart. Walk-of-shame back to return wrong packs.

**Score:** [world-grounded / partially grounded / abstract]

---

## Output Template

```markdown
# Consequence Quality: [Game Name]

**Consequence strength:** [0.0 - 1.0]

**Strongest consequence:**
[One sentence]

**Weakest consequence gap:**
[One sentence]

**Main risk:**
[What happens if this isn't fixed]

**Recommendation:**
[One focused action]
```

---

*Source: Grocery Dash audit. The checkout-blocks-entry and manager-drops-item patterns are the gold standard for world-grounded, diagnostic, proportional consequences.*
