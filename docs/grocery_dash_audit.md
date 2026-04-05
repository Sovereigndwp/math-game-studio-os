# Grocery Dash Math Market — Mature Game Audit

Legacy / Mature Game Audit Mode. April 2026.
Source: full game design spec + live v2 HTML build (84KB single-file).

---

## Task 1 — Audit

### Lens 1: Role-to-Math Fit

**Rating: Exceptional.**

The home-cook-shopping role maps perfectly to the math. The player must:
1. Read the recipe (comprehension)
2. Multiply recipe amounts by guest count (multiplication)
3. Divide by pack size using ceiling division (division with remainders)
4. Choose between pack variants to minimize waste (optimization)

The role is not decorative — "dinner guests are arriving" creates real narrative
stakes. The math is inseparable from the shopping: you literally cannot check out
without computing correctly. The checkout blocks you if your cart is wrong, forcing
you to walk back and rethink. The math is the shopping.

Where ATC's role is "clear the plane" (procedural urgency), Grocery Dash's role
is "feed your guests without wasting money" (contextual reasoning). Both are
excellent but in different ways.

### Lens 2: Loop Purity

**Rating: High (~0.85).**

The core loop is: READ RECIPE → MULTIPLY → DIVIDE → SHOP → CHECKOUT. Five steps.
The math actions (multiply and divide) are steps 2-3. Steps 4-5 are physical
navigation and validation.

Loop purity is slightly lower than ATC (0.95) because step 4 (navigating the store,
dodging shoppers and the manager) is a spatial/motor task, not a math task. However,
the spatial pressure serves the learning goal — it forces the player to compute
BEFORE moving, because walking to the wrong shelf wastes precious time.

The navigation is not filler: it converts "I should plan my math carefully" from
abstract advice into a physical consequence. If you didn't compute ceiling division
correctly before walking, you'll waste time returning packs.

### Lens 3: Onboarding Quality

**Rating: Exceptional.**

The 4-step tutorial is the best onboarding in the portfolio:
1. "Dinner guests are coming — check the recipe card" (context)
2. "Multiply: recipe amount × guests" (the math)
3. "Walk to shelf → SPACE to grab, walk back → SPACE to return" (controls)
4. "Watch out for the store manager!" (urgency source)

Key design choice: **the timer does not start until the tutorial is dismissed.**
The player learns controls under zero pressure. This is better than ATC's approach
(training levels with generous timers) because there is truly no time cost to
reading carefully.

Levels 1-3 also have zero NPCs — the manager doesn't appear until Level 4. This
gives the player 3 full levels to master the recipe → multiply → divide → shop
loop before spatial pressure is added.

### Lens 4: Urgency and Pressure

**Rating: Very High, with a unique physical layer.**

Urgency channels:
1. **Level timer** — 90-130 seconds per level, visible countdown
2. **Store manager (the chaser)** — pathfinds toward the player, costs -10 seconds on catch
3. **Other shoppers** — collision costs -5 seconds
4. **Checkout validation** — wrong cart is blocked, wasting return-trip time

What makes this unique vs ATC: the urgency is **physical**. In ATC, urgency is
abstract (patience bars, score thresholds). In Grocery Dash, urgency has a body —
the manager is physically chasing you through the store. You can see the threat
approaching. This creates moment-to-moment tension that abstract timers cannot.

The manager also creates a beautiful design tension: you need to think carefully
(math) but you also need to move quickly (chase). Rushing leads to wrong packs.
Thinking too long gets you caught. The optimal play is "compute at the recipe card,
then move decisively" — which is exactly the metacognitive skill the game teaches.

### Lens 5: Feedback and Reward Quality

**Rating: Strong.**

Positive feedback:
- Pack grab: particle burst in category color + toast notification ("+ 1 pack Bread (1 pk = 20 slices)")
- Correct checkout: star rating (★★★/★★/★), score, level complete celebration
- Win screen: "DINNER IS SAVED! 🎉" with total stars, final score, lives remaining

Negative feedback:
- Wrong items at checkout: blocked, must return items first (physical consequence)
- Shopper bump: -5 seconds + screen shake
- Manager catch: -10 seconds + screen shake + toast
- Avoidable waste at checkout: drops to ★ rating

The feedback stack is complete: immediate particles on every grab, screen shake on
every collision, star rating on every checkout. The checkout receipt showing worked
math ("6 guests × 2 eggs = 12 needed, pack of 6: ⌈12/6⌉ = 2 packs") is brilliant
corrective feedback — the player sees the full solution after attempting it.

### Lens 6: Replayability and Mastery Loop

**Rating: Very High.**

- 12 levels with progressive difficulty
- **Randomized guest count per play** — same level, different math every time
- 3-star rating per level (★★★ perfect, ★★ good, ★ passed)
- Best times and star tracking with localStorage persistence
- Increasing ingredient count (3 → 8 across levels)
- Pack size variants that require optimization (which pack wastes less?)
- Budget constraint adds a second optimization axis

The randomized guest count is the strongest replay hook in the portfolio. ATC
randomizes math facts but the structure is the same. Grocery Dash randomizes the
scale factor, which changes every multiplication and every division problem.
Playing Level 3 with 4 guests is fundamentally different math than Level 3 with 10
guests.

### Lens 7: Teacher Usefulness / Classroom Fit

**Rating: Exceptional.**

- Zero setup — single HTML file, no install, no account, no backend
- Teacher unlock code (UNLOCK) for full level access
- Curriculum-aligned: multiplication, ceiling division, proportional reasoning (Grades 3-6)
- Recipe context makes "why do I need to multiply?" self-evident
- Star ratings provide differentiated goals (★ for struggling students, ★★★ for advanced)
- The checkout receipt is a built-in worked-example generator
- Level descriptions explain the math focus: "watch those egg pack sizes!"

Teacher pitch: "Students practice multiplication and division by grocery shopping
for dinner guests. They choose pack sizes, minimize waste, and dodge the store
manager. Every play is different because the guest count changes."

### Lens 8: Visual and Motion Feel

**Rating: Strong.**

The v2 build includes:
- 60fps canvas rendering
- Particle bursts on every grab (18 particles, category-colored)
- Screen shake on collisions (configurable intensity and duration)
- Toast notifications floating up from the player
- NPC animation and pathfinding
- Color-coded ingredient groups (grain, dairy, protein, condiment)
- Clean dark-mode UI with amber/gold accents

This is significantly ahead of where Bakery Rush was before the visual pass.
The spatial gameplay naturally creates visual interest — a moving player, moving
NPCs, particle effects — that turn-based or tap-based games have to manufacture.

### Lens 9: Hidden Weaknesses or Blind Spots

**Weakness 1 — The math computation happens off-screen.**
The player reads "2 eggs per serving, 6 guests" on the recipe card and must
compute "12 eggs needed" and "⌈12/6⌉ = 2 packs" mentally. There is no in-game
workspace for the computation. Some students will use paper. Others will guess.
The game tests whether you CAN compute but doesn't help you learn HOW to compute.
This is intentional ("the game never tells you the answer") but may frustrate
students who are on the boundary of the skill.

**Weakness 2 — Pack return requires backtracking, which can feel punitive.**
If you grabbed wrong packs, you must physically walk back to the shelf and press
SPACE to return them. With the manager chasing you, this walk-of-shame can eat
15-20 seconds and feel unfair — especially if the player's ceiling division was
close but wrong. The consequence is proportional to the distance to the shelf,
not to the severity of the math error.

**Weakness 3 — Budget constraint may conflict with ceiling division learning.**
Some levels have a budget limit. If the student computes ceiling division correctly
but the optimal pack choice exceeds the budget, they face a constraint conflict
that isn't about division — it's about cost comparison. This adds complexity that
may muddy the core learning goal for weaker students.

**Weakness 4 — No misconception detection or adaptive feedback.**
The checkout receipt shows the worked solution, but the game doesn't detect patterns
in errors. A student who consistently buys too few packs (under-rounding) gets the
same feedback as one who consistently buys too many (not understanding ceiling
division). A misconception-aware system could distinguish these and offer targeted
replay.

---

## What Grocery Dash Does Unusually Well

1. **Contextual math** — the recipe-to-shopping pipeline makes multiplication and
   division feel like real problem-solving, not abstract drill.
2. **Physical urgency** — the store manager creates embodied time pressure that
   abstract timers cannot match.
3. **The walk-of-shame** — returning wrong packs is a physical consequence that is
   more memorable than a score penalty.
4. **Randomized replay** — different guest count = different math = genuine replay value.
5. **Checkout receipt as worked example** — corrective feedback disguised as a shopping receipt.
6. **Pack size optimization** — choosing between 6-pack and 12-pack eggs is a genuine
   mathematical reasoning task (minimize waste), not just "get the right answer."
7. **Distractor items** — wrong items on shelves test whether the player is actually
   reading the recipe, not just grabbing everything.

---

## Task 2 — Improvement Recommendation

### Single Highest-Value Weakness

**The game doesn't detect misconception patterns.**

The checkout receipt shows the correct answer but doesn't diagnose what went wrong.
A student who consistently under-rounds (thinks ⌈12/6⌉ = 1 instead of 2) is
making a specific ceiling-division misconception that could be named and addressed
with a targeted clean-replay task.

Adding misconception detection (using the patterns from the Misconception Architect
workflow) would transform the checkout from "here's the answer" to "here's what
you misunderstood and here's a focused exercise to fix it."

However: the game is already strong enough as a learning tool without this.
The checkout receipt provides good corrective feedback. The misconception detection
would be an enhancement, not a fix. **Grocery Dash should primarily be used as a
learning source for the OS, not as a fix-it target.**

---

## Task 3 — OS Lesson Extraction

### What Makes Grocery Dash Sticky

The game is sticky because the math is embedded in a real-world decision chain
(recipe → scale → pack → shop → validate) rather than isolated as a single
problem. The player doesn't solve "12 ÷ 6" — they solve "how many packs of 6
do I need for 12 eggs, and is the 12-pack a better deal?" The math has context,
consequence, and a second correct answer to discover.

### Reusable Engagement Rules (from Grocery Dash)

1. **Embed math in a decision chain, not a single question.** Recipe → multiply →
   divide → optimize is four connected math steps. Each step's answer feeds the next.
2. **Never reveal the answer during play.** Show "per serving" amounts and guest count.
   The player must compute. Show the full solution only at checkout (after the attempt).
3. **Make physical consequences match mathematical mistakes.** Walking back to return
   wrong packs is a time cost proportional to carelessness, not just a score penalty.
4. **Use distractor items to test comprehension.** Wrong items that look similar to
   correct ones force the player to actually read and reason, not pattern-match.
5. **Randomize the problem, not just the presentation.** Different guest counts create
   genuinely different multiplication and division problems on the same level.
6. **Create an optimization layer above correctness.** Two pack sizes for the same
   ingredient means there's a "correct" answer AND a "better" answer. This rewards
   deeper mathematical reasoning.

### Reusable Urgency and Pressure Patterns

| Pattern | Grocery Dash Implementation | Reuse Guidance |
|---------|---------------------------|----------------|
| Physical antagonist | Store manager pathfinds toward player, -10s on catch | An NPC that chases creates more urgency than a bare timer |
| Collision penalty | Bumping shoppers costs -5s + screen shake | Mild penalties for carelessness, not for math errors |
| Checkout validation | Wrong cart is blocked, must return items | Physical validation > numeric validation for learning |
| Timer that doesn't start during instruction | Tutorial runs with no clock | Never time-pressure during onboarding |
| Escalating NPC count | 0 NPCs at L1-3, up to 5 at L9-12 | Add spatial pressure only after math is comfortable |

### Reusable Onboarding Patterns

| Pattern | Grocery Dash Implementation | Reuse Guidance |
|---------|---------------------------|----------------|
| Zero-pressure tutorial | 4-step fullscreen tutorial, timer starts after | Instruction and timer must never overlap |
| Context-first instruction | "Dinner guests are coming" before any controls | Establish the WHY before the HOW |
| Progressive NPC introduction | No NPCs for 3 levels, then manager, then shoppers | Add complexity layers one at a time |
| Recipe card as persistent reference | Always visible, never hidden during play | The math reference should be glanceable, not memorizable |

### Reusable Progression and Replay Patterns

| Pattern | Grocery Dash Implementation | Reuse Guidance |
|---------|---------------------------|----------------|
| Randomized problem scale | Guest count changes each play | Same level, different math = genuine replay |
| Star rating with tiers | ★★★ perfect, ★★ good, ★ passed | Different learners aim for different targets |
| Ingredient count progression | 3 ingredients at L1 → 8 at L12 | Increase problem complexity, not just difficulty |
| Pack size variants | Two shelf options per ingredient at higher levels | Add an optimization layer above correctness |
| Budget constraint | Spending limit at some levels | Add a second axis of mathematical reasoning |

### Reusable Feedback and Reward Patterns

| Pattern | Grocery Dash Implementation | Reuse Guidance |
|---------|---------------------------|----------------|
| Particle burst per action | 18 particles in category color on grab | Every action gets an immediate visual response |
| Screen shake on error | Shake(6, 300ms) on collision | Physical feedback for physical mistakes |
| Toast notifications | Float-up text from player position | In-context feedback, not corner notifications |
| Checkout receipt as worked example | Full solution shown after attempt | Corrective feedback must come AFTER the struggle |
| Walk-of-shame for wrong items | Physical backtracking to return packs | Physical consequences > numeric consequences |

### Reusable Teacher-Friendly Platform Patterns

| Pattern | Grocery Dash Implementation | Reuse Guidance |
|---------|---------------------------|----------------|
| Recipe context | "2 eggs per serving × 6 guests" | Real-world framing makes the math self-evident |
| Star differentiation | ★ for completion, ★★★ for perfection | Let teachers set different expectations for different students |
| Level descriptions | "Watch those egg pack sizes!" | Each level should name its math focus plainly |
| Teacher unlock code | "UNLOCK" for full access | One code, not a settings panel |
| Narrative wrapper | "Dinner guests are arriving" | The story creates stakes the student cares about |

### What Future Games Should Copy from Grocery Dash

1. The decision chain: math is not one step but a connected sequence
2. Randomized problem generation per play (guest count randomization)
3. The checkout receipt as a worked-example generator
4. Physical antagonist for embodied urgency (the store manager)
5. Distractor items that test reading comprehension
6. Pack size optimization as a "better than correct" challenge
7. Screen shake and particle effects on every meaningful action
8. Zero-pressure tutorial with timer starting only after dismissal

### What Future Games Should Avoid

1. Off-screen computation with no workspace — students on the boundary need support
2. Backtracking penalties proportional to distance rather than error severity
3. Budget constraints that conflict with the core math learning goal
4. No misconception detection — the checkout receipt is good but doesn't diagnose patterns
5. Making spatial navigation so dominant that math planning feels secondary

### Grocery Dash Release Checklist

- [ ] Math is embedded in a multi-step decision chain, not isolated as a single question
- [ ] The game never reveals answers during play — solutions shown after the attempt
- [ ] Randomization creates genuinely different problems on replay
- [ ] At least one physical consequence exists for math errors (not just score penalties)
- [ ] Distractor items or options test comprehension, not just memory
- [ ] An optimization layer exists above "correct" (better pack sizes, less waste)
- [ ] Star ratings differentiate completion from mastery
- [ ] Tutorial runs with zero time pressure — timer starts only after instruction
- [ ] A physical antagonist or ambient threat creates embodied urgency
- [ ] Corrective feedback is specific and shows the worked solution
- [ ] The game loads from a single file with no install, account, or backend
- [ ] Particle effects and screen shake provide immediate feedback on every action

---

## Task 4 — ATC vs Grocery Dash Comparison

### What ATC Teaches Best

| Strength | Why ATC is the better reference |
|----------|-------------------------------|
| **Loop purity** | 4-step loop, math is 50% of every cycle. Tightest loop in the portfolio. |
| **Urgency compounding** | Three simultaneous pressure channels (patience + timer + threshold) |
| **Streak rewards** | Scaling bonuses that reward sustained focus across difficulty levels |
| **Keyboard accessibility** | Full Tab/Enter/Arrow play — best accessibility model |
| **Scoring as curriculum signal** | +100 math > +40 action. The numbers teach what matters. |

### What Grocery Dash Teaches Best

| Strength | Why Grocery Dash is the better reference |
|----------|----------------------------------------|
| **Contextual math** | Multi-step decision chain (read → multiply → divide → optimize) |
| **Physical consequence** | Walk-of-shame for wrong packs is more memorable than -20 points |
| **Physical urgency** | The manager chasing you creates embodied tension |
| **Replay depth** | Randomized guest count means same level = different math |
| **Corrective feedback** | Checkout receipt as a built-in worked-example generator |
| **Optimization above correctness** | Pack size choice adds a "better" layer above "right" |

### What Both Games Share

1. **Math is the verb** — you cannot progress without computing correctly
2. **Zero-friction deployment** — single HTML file, no install, no account
3. **Teacher controls** — operation/topic selection + unlock code
4. **Narrative wrapper** — the role creates real stakes (clear the plane / feed the guests)
5. **Visible countdown** — urgency is shown, not hidden
6. **Recoverable failure** — wrong answers cost something but don't end the game instantly
7. **Session summary** — missed facts (ATC) / checkout receipt (Grocery Dash) shows what to learn
8. **Progressive complexity** — one new mechanic per phase, never more

### What All Future Games Must Inherit Immediately

From both games combined, the non-negotiable patterns are:

1. **Math must be the highest-value action** — scoring, progression, or gate logic must make the math dominant
2. **At least two urgency channels** — per-item pressure + global pressure at minimum
3. **The answer is never shown during play** — solutions revealed only after the attempt
4. **Physical or visible consequences for errors** — not just score changes
5. **Randomization prevents memorization** — replay must produce different math
6. **Zero-friction deployment** — single file or instant load, no account, no backend
7. **Corrective feedback is specific** — "you got X wrong" not "try again"
8. **Tutorial runs under zero time pressure** — timer starts only after instruction ends
9. **Progressive complexity** — one new mechanic per phase transition, never more
10. **Star rating or tiered achievement** — different learners need different goals

---

*Grocery Dash audit complete. Together with ATC Math Tower, the OS now has two
complementary gold-standard references: ATC for urgency and loop purity,
Grocery Dash for contextual math and physical consequence.*
