# Counting — Concept Lane

| Field | Value |
|---|---|
| **Date** | 2026-04-07 |
| **Source** | Number Jungle Safari analysis → counting extraction |
| **Status** | Concept lane — awaiting P0/P1 prototype approval |

---

## 1. Counting Family Classification

### Structural family
**Enumerate-and-report.**

The player counts visible objects and reports the total by tapping a number. The counting act IS the math — there is no symbolic entry, no equation, no selection-from-options that could be guessed. The player must actually enumerate.

Three-part boundary rule:
- (A) Player is shown a set of discrete countable objects
- (B) Player must determine the quantity by counting
- (C) Player reports the total by tapping a numeral — the count itself is the math operation

**Boundary breaks (what this family is NOT):**
- Tapping a pre-labeled group (e.g., a basket labeled "7") — that is number recognition, not counting
- Selecting from multiple-choice answers without first counting — that is guessing, not enumerating
- Subitizing displays where quantity is perceptually obvious (3 dots in a triangle) without requiring serial counting — that tests estimation, not counting

**Nearest existing family:** Early-Arithmetic Combine-and-Build (Bakery Rush, ages 5–8). Different family. Bakery Rush requires selecting addends to reach a target sum. Counting requires determining a quantity from a visual set. The cognitive operation is different: composition vs enumeration. No overlap.

### Primary math skill
Counting objects in a set and reporting the cardinal value. Specifically:
- One-to-one correspondence (each object counted exactly once)
- Stable order principle (number sequence)
- Cardinality principle (the last number said is the quantity of the set)
- At higher tiers: counting backward, skip counting by 2s, counting with partial occlusion

### Age band
**Pre-K to Grade 1 (ages 4–6).** Lower bound is the youngest band the OS has considered. Upper bound stops before Bakery Rush's territory (ages 5–8) begins to require addition.

### Motor constraints
- **Tap only.** No drag, no swipe, no typed input. A 4-year-old's fine motor control supports tapping large targets but not precise dragging or keyboard use.
- **Touch targets minimum 64x64px.** The standard 48x48px is for ages 7+. Ages 4–6 need larger targets with more spacing.
- **Maximum 4 answer choices visible at once.** More than 4 creates visual overwhelm and accidental taps.
- **No simultaneous multi-touch.** One finger, one action.

### Worksheet risk
**Medium.** The core risk: "count the objects, tap the number" can feel like a digital worksheet if the objects are static clip-art arranged in a grid. The game must make counting feel like an action, not an exercise.

Mitigations that make counting feel like a game:
- Objects move (animals walking, fish swimming, birds flying)
- Objects appear and disappear (frogs jumping onto lily pads, butterflies landing)
- Objects are partially hidden (some behind a cloud, under a leaf)
- The scene reacts to the player's answer (animals celebrate, water splashes)
- Counting is embedded in a role ("help Ellie the Elephant count her friends before they cross the river")

If the prototype cannot make the counting action feel meaningfully different from a worksheet, the concept fails P0.

### Likely ceiling
**Moderate.** Counting 1–20 has a natural ceiling — once a child can reliably count 20 objects, the skill is fluent. The ceiling extends through:

| Tier | Ceiling extension |
|---|---|
| Count 1–5 (Sprout) | Fluency in 1–2 sessions for most 5-year-olds |
| Count 1–10 with moving/hidden objects (Sapling) | 3–5 sessions. Partial occlusion adds real cognitive demand. |
| Count 1–20 + backward + skip count by 2s (Tree) | 5–10 sessions. Backward counting and skip counting are genuinely harder skills. |

Beyond Tree tier, counting transitions into addition (counting on) and multiplication (skip counting by 3s, 5s, 10s). Those belong to different families. The counting game should stop at its natural ceiling rather than drifting into adjacent skills.

**Estimated total depth:** 10–20 sessions before the strongest players exhaust the skill. This is appropriate for ages 4–6 — these players rotate between games frequently and do not need 100-hour depth.

---

## 2. Smallest P0/P1 Prototype Plan

### Concept in one sentence
Count the animals on screen and tap the right number before they wander away.

### Role
Junior Ranger helping a friendly elephant (Ellie) count animals at the watering hole.

### One mini-game: Watering Hole Count

**Scene:** A watering hole clearing. Animals walk in from the edges, stop to drink, and eventually wander off. The player must count them before they leave.

**Core loop (4 steps):**
```
Animals appear → Player counts → Player taps a number → Scene reacts
```

**Detailed flow:**
1. Ellie says (audio): "How many zebras are at the watering hole?"
2. A group of zebras walks in and stops at the water (animated, slightly moving — drinking, swishing tails)
3. Player counts them visually
4. A number bar appears at the bottom with 4 large number buttons (correct answer + 3 distractors)
5. Player taps a number
6. **Correct:** Zebras splash in the water, Ellie trumpets happily, audio says "That's right! [N] zebras!" — green burst particles
7. **Wrong:** Ellie gently shakes her head, audio says "Almost! Try counting again." Objects briefly highlight one by one (counting scaffold), then the number bar reshuffles. No score penalty, no life lost.

### 3 difficulty tiers

| Tier | Name | Object count | Scene complexity | Timer | Answer choices |
|---|---|---|---|---|---|
| Sprout | "Calm Morning" | 1–5 animals | Static positions, no occlusion, bright colors, one animal type per round | None | 3 choices |
| Sapling | "Busy Afternoon" | 3–10 animals | Animals move slowly (drinking, walking), 1–2 partially behind a rock or tree, may include 2 animal types | None, but animals begin to wander off after 20 seconds (gentle urgency) | 4 choices |
| Tree | "Sunset Rush" | 5–15 animals | Animals move, some enter/leave mid-count, some behind objects, mixed animal types, one "tricky" round (e.g., "How many are NOT drinking?") | Animals leave after 15 seconds | 4 choices |

### Audio-first design
- All instructions spoken aloud by a narrator voice (warm, encouraging, slow pace)
- Ellie makes elephant sounds on correct/wrong
- Each animal type has a distinctive sound when it appears
- Number buttons have audio feedback: the number is spoken when tapped
- No text required to play. Number buttons show both the numeral and a dot pattern (dual representation)

### Tap-only input
- Tap to select answer (number bar at bottom)
- Tap Ellie to hear the question again
- Tap a replay button (ear icon) to re-hear instructions
- No drag, no swipe, no keyboard

### No-punishment feedback
- **Correct:** Celebration animation + Ellie trumpet + audio praise. Advance to next round.
- **Wrong (1st attempt):** Ellie shakes head gently. Audio: "Hmm, let's try again!" Number bar reshuffles (same correct answer, new distractors). No penalty.
- **Wrong (2nd attempt):** Ellie reaches trunk toward animals. Audio: "Let me help! Count with me." Animals highlight one by one with a counting sound (1... 2... 3...). Then the number bar reappears. Still no penalty.
- **Wrong (3rd attempt):** The correct number glows. Audio: "It's [N]! [N] zebras." Player taps to confirm. Round counts as attempted but the child is never stuck.

### Round structure
- **One session = 8 rounds** (enough data to assess, short enough for a 4-year-old's attention span)
- Round types vary: different animal types, different quantities, different positions
- After 8 rounds: simple results screen showing number of rounds with a smiley face (no score, no stars at P1 — just "You counted [X] groups today!")
- Replay button to immediately start another session

### What P0/P1 must prove

**P0 proof (is there a game here?):**
- The role (Junior Ranger helping Ellie) naturally carries the math (counting)
- The loop is one sentence: "Count the animals and tap the right number before they wander away"
- There is one reason this could be sticky: animated animals reacting to the player's answers

**P1 proof (does the loop work?):**
- A 4–5 year old can understand the goal without reading
- A 4–5 year old can complete a Sprout round with no help
- Wrong answers feel like gentle redirects, not failures
- The counting scaffold (animals highlight one by one) is actually helpful, not confusing
- The child wants to do at least one more round after completing a session

### Build spec
- Single HTML file (follows repo convention: `previews/counting/current.html`)
- HTML5 Canvas for scene rendering
- Web Speech API or pre-recorded audio clips for narration
- No external dependencies, no build step
- localStorage for tier selection persistence only (no progress tracking at P1)
- Target: mobile-first responsive, minimum 375px width

---

## 3. Stop Conditions

### The concept is too thin if:
- **Sprout tier is trivially easy and Sapling doesn't add meaningful challenge.** If counting 1–10 with slight movement is as easy as counting 1–5 static, the skill has no progression ladder — it is a one-session game, not a replayable loop. Test: if a 5-year-old completes Sprout and Sapling in the same first session with >90% accuracy on both, the tiers are not differentiated enough.

- **The child counts correctly but shows no engagement.** If the child gets the answers right but does not watch the celebration animations, does not react to Ellie, and does not ask for another round, the game is functional but dead. The counting action is not carrying any game feel. This is the worksheet failure mode.

- **The "count again" scaffold replaces actual counting.** If the child learns to tap wrong deliberately to trigger the one-by-one highlight (because the highlight does the counting for them), the scaffold is undermining the skill. Watch for: children who get round 1 wrong, see the scaffold, then get round 2 wrong again on purpose.

### The concept is too confusing if:
- **The child does not understand they should count.** If they tap numbers randomly without looking at the animals, the visual prompt is failing — the connection between the scene and the number bar is not legible. This means the audio-first instruction is not working or the spatial layout is wrong.

- **The child counts correctly but cannot find the right number on the bar.** This means number recognition is a prerequisite the child doesn't have, and the game is testing number recognition (a different skill) instead of counting. The number bar must include dot patterns alongside numerals to prevent this.

- **Moving animals at Sapling tier cause miscounts because the child cannot track them.** If >50% of Sapling errors are off-by-one in the same direction (overcounting animals that walked behind objects, or undercounting animals that are partially hidden), the occlusion mechanic is too hard for the age band and should be removed or softened.

### Kill signal:
If both "too thin" and "too confusing" appear in the same playtest — meaning the easy tier is trivial AND the harder tiers confuse rather than challenge — the concept does not have a viable difficulty progression and should be paused.

---

## 4. Out of Scope

The following are explicitly excluded from the P0/P1 prototype. They belong to the broader Jungle Safari concept but must not be built until the counting loop is proven.

| Item | Why out of scope |
|---|---|
| Zone progression (multiple zones, unlocking) | Multi-zone is a curriculum shell, not a game. Prove one game first. |
| Other skill zones (Numbers, Addition, Shapes, Patterns) | Different game families. Each needs its own concept lane and P0/P1. |
| Animal guide system (5 named characters) | One guide (Ellie) is enough for P1. More characters add theme, not loop proof. |
| Sticker journal / collection meta-game | Meta-progression layer. Cannot be tested until the core loop retains players. |
| Star / badge / trophy reward system | Reward system. Premature before the core loop is engaging on its own. |
| Parent dashboard / Ranger Report Card | Diagnostic layer. Requires session data, sub-skill tracking, gap detection — all P2A+ concerns. |
| Practice mode (unlimited, no pass/fail) | The P1 prototype already has no pass/fail. Practice mode is structurally identical to the game at this stage. |
| PDF export / teacher reports | Teacher layer. P5 concern. |
| Adaptive difficulty (auto-adjust tier) | Adaptive systems need baseline data. Manual tier selection is correct for P1. |
| Skip counting / backward counting content | Tree tier content. Build only if Sprout and Sapling tiers prove the loop works. Can be added in a later pass. |
| Multiple mini-game variants per skill | One mini-game proves or disproves the loop. Variants are P2/P3 expansion. |
| Jungle theme art, custom sprites, custom audio | Placeholder art and Web Speech API are sufficient for P1. Visual polish is P3. |
| Cloud sync / accounts / multi-device | Infrastructure. Not relevant until the game is worth distributing. |
| Daily challenge / shared seed | Meta feature from Echo Heist. Not applicable at ages 4–6. |
