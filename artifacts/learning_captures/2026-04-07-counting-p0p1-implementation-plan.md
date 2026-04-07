# Watering Hole Count — P0/P1 Implementation Plan

| Field | Value |
|---|---|
| **Date** | 2026-04-07 |
| **Game** | Watering Hole Count |
| **Family** | Enumerate-and-report |
| **Skill** | Counting / cardinality |
| **Age band** | 4–6 (Pre-K to Grade 1) |
| **Build target** | `previews/counting/current.html` |
| **Pass** | P0 + P1 combined (core loop proof) |

---

## 1. Tier-by-Tier P1 Plan

### Sprout — "Calm Morning"

**Purpose:** Prove a 4-year-old can count and answer without help or reading.

| Parameter | Value |
|---|---|
| Quantity range | 1–5 |
| Animal types per round | 1 (all same species) |
| Animal behavior | Walk in from one edge, stop, idle in place (gentle breathing/bobbing animation). No movement after settling. |
| Occlusion | None. All animals fully visible, no overlap, no objects blocking. |
| Spacing | Animals placed at least 80px apart (canvas-relative). No clusters that make one-to-one counting ambiguous. |
| Timer | None. Animals stay indefinitely. The round waits for the player. |
| Answer choices | 3 buttons. Correct answer + 2 distractors. |
| Distractor rule | Distractors are always ±1 and ±2 from the correct answer (never random far numbers). For quantity 1: choices are 1, 2, 3. For quantity 5: choices are 3, 4, 5 (shuffled). |
| Round count | 8 rounds |

**Round-by-round content (Sprout):**

| Round | Animal | Quantity | Why this quantity |
|---|---|---|---|
| 1 | Zebras | 1 | Baseline. Cannot fail. Builds confidence. |
| 2 | Flamingos | 2 | Still trivial. Confirms the child understands the loop. |
| 3 | Turtles | 3 | First round where counting matters (not instant recognition). |
| 4 | Zebras | 2 | Repetition of low number with different animal. Tests transfer. |
| 5 | Frogs | 4 | First count above 3. Requires serial counting for most 4-year-olds. |
| 6 | Flamingos | 5 | Maximum Sprout quantity. Tests the ceiling. |
| 7 | Turtles | 3 | Return to a known quantity. Should feel easy. Confidence round. |
| 8 | Frogs | 4 | Second exposure to 4. Checks consistency. |

**Quantities deliberately avoid:** 0 (confusing at this age), repeated maximum (5 only appears once to avoid frustration if it's hard).

### Sapling — "Busy Afternoon"

**Purpose:** Prove that movement, occlusion, and higher quantities create meaningful challenge without confusion.

| Parameter | Value |
|---|---|
| Quantity range | 3–8 |
| Animal types per round | 1 or 2 (question always asks about one type: "How many zebras?" even if flamingos are also present) |
| Animal behavior | Walk in, settle, then continue with idle motion: drinking (head dips), walking slowly within a zone, turning. Animals do not leave their zone but are not frozen. |
| Occlusion | 1–2 animals partially behind a rock, tree, or tall grass. At least 50% of the animal's body is visible. The hidden portion is always the body — the head is always visible. |
| Spacing | Animals may be closer together (minimum 50px apart). Some natural clustering near the water's edge. |
| Timer | No hard timer. Animals begin to walk toward the edge after 20 seconds. Audio cue: Ellie says "They're starting to leave!" at 18 seconds. If the player hasn't answered by 25 seconds, the round auto-pauses: animals freeze, audio says "Take your time!" and the number bar stays. The child is never locked out. |
| Answer choices | 4 buttons. Correct answer + 3 distractors. |
| Distractor rule | Distractors are ±1, ±2, and ±3 from correct. For rounds with 2 animal types, one distractor is always the total of both types (the "counted everything" mistake). |
| Round count | 8 rounds |

**Round-by-round content (Sapling):**

| Round | Animal asked about | Other animals present | Quantity (asked) | Quantity (other) | Occlusion |
|---|---|---|---|---|---|
| 1 | Zebras | — | 3 | 0 | None. Warm-up at Sapling pace with movement. |
| 2 | Turtles | — | 5 | 0 | 1 turtle partially behind a rock. |
| 3 | Flamingos | Frogs | 4 | 2 | None. Tests selective counting (ignore the frogs). |
| 4 | Frogs | — | 6 | 0 | 1 frog behind tall grass. |
| 5 | Zebras | Turtles | 3 | 3 | None. Total is 6 — distractor includes 6 to catch "counted everything." |
| 6 | Flamingos | — | 7 | 0 | 2 flamingos partially behind a tree. |
| 7 | Turtles | Flamingos | 5 | 2 | 1 turtle behind a rock. Mixed challenge: occlusion + selective counting. |
| 8 | Frogs | — | 8 | 0 | 1 frog behind grass. Maximum Sapling quantity. |

**Key Sapling mechanic: selective counting.** Rounds 3, 5, and 7 have two animal types on screen. The question asks about one type only. The child must count selectively — a genuine cognitive step above counting everything. The "counted everything" distractor catches inattentive players.

### Tree — "Sunset Rush"

**Purpose:** Prove that entering/leaving animals and higher quantities create a genuine mastery challenge.

| Parameter | Value |
|---|---|
| Quantity range | 5–12 |
| Animal types per round | 1 or 2 |
| Animal behavior | Animals walk in, settle, and some walk out again after 8–12 seconds. The question is always about how many are at the watering hole RIGHT NOW — meaning the child must count the currently-visible set, not the total that ever appeared. |
| Entering/leaving | Each round, 1–2 animals walk in 3–4 seconds after the scene opens. 1–2 animals walk out 8–12 seconds in. The correct answer is the count at the moment the number bar appears. The number bar appears 10 seconds after the scene opens (after arrivals, during/after departures). |
| Occlusion | 1–3 animals partially behind objects. |
| Spacing | Natural clustering. Some animals overlap slightly (heads always visible). |
| Timer | The number bar is visible for 15 seconds. If no answer by 15 seconds, the round auto-pauses: animals freeze, audio says "Take your time!" Number bar stays. The child is never locked out. |
| Answer choices | 4 buttons |
| Distractor rule | ±1, ±2, ±3. One distractor is always the peak count (total that were on screen before any left) — catches "I counted them all when they first arrived." |
| Round count | 8 rounds |

**Round-by-round content (Tree):**

| Round | Animal asked | Quantity at answer time | Animals that entered late | Animals that left | Occlusion | Why this round |
|---|---|---|---|---|---|---|
| 1 | Zebras | 5 | 0 | 0 | 1 behind rock | Warm-up. Tree occlusion level, no enter/leave yet. |
| 2 | Turtles | 6 | 1 (walks in at 4s) | 0 | 1 behind grass | First "late arrival" — child must notice the new one and recount. |
| 3 | Flamingos | 5 | 0 | 2 (walk out at 8s, 10s) | 0 | First "departure" — 7 appear, 2 leave, answer is 5. Distractor: 7. |
| 4 | Frogs | 7 | 1 (walks in at 3s) | 1 (walks out at 9s) | 1 behind rock | Combined: 7 start, +1, −1 = 7. Tests whether child tracks net change. |
| 5 | Zebras | 8 | 2 (walk in at 3s, 5s) | 0 | 2 behind trees | High count + occlusion + late arrivals. No departures to keep it tractable. |
| 6 | Turtles (with frogs) | 6 (turtles) | 0 | 1 frog leaves | 1 turtle behind rock | Selective counting + departure of the OTHER type. Tests focus. |
| 7 | Flamingos | 9 | 1 (walks in at 4s) | 2 (walk out at 7s, 11s) | 1 behind grass | High count + arrivals + departures. Hardest standard round. |
| 8 | Frogs | 10 | 2 (walk in at 3s, 6s) | 0 | 2 behind rocks | Maximum quantity. Arrivals but no departures. The "can they count to 10 under pressure?" round. |

---

## 2. Round Flow

Every round follows the same sequence regardless of tier. Tier changes the parameters, never the flow.

```
PHASE 1: SCENE SETUP (2 seconds)
├── Canvas shows the watering hole (static background)
├── Ellie is visible on the left side
└── Transition: brief "shimmer" on the water surface

PHASE 2: ANIMALS ARRIVE (3–5 seconds)
├── Animals walk in from edges (left, right, or top)
├── Each animal plays a soft footstep/splash sound on arrival
├── [Sapling/Tree] Late arrivals walk in after 3–5 seconds
├── Animals settle into idle positions
└── Ellie's trunk points toward the animals

PHASE 3: QUESTION (audio, no text)
├── Ellie trumpets softly (attention cue)
├── Narrator voice: "How many [animal type] are at the watering hole?"
├── [Sapling] If 2 types present: "How many [asked type]?" (emphasis on the type name)
├── [Tree] Departing animals begin to walk off during this phase
└── Player counts visually. No UI prompt yet — just the scene.

PHASE 4: ANSWER BAR APPEARS
├── Number bar slides up from the bottom of the screen
├── [Sprout] 3 buttons, each 80x80px minimum
├── [Sapling/Tree] 4 buttons, each 72x72px minimum
├── Each button shows: large numeral (top) + dot pattern (bottom)
├── Buttons are spaced with 16px gaps
├── Audio: a soft "pop" sound as the bar appears
├── [Tree] The number bar is the "snapshot" moment — correct answer is the count NOW
└── Player taps one button

PHASE 5A: CORRECT ANSWER
├── Tapped button glows green, other buttons fade out
├── Animals play a celebration: zebras rear up, flamingos flap, frogs jump, turtles bob
├── Ellie trumpets (ascending two-tone: 300→500 Hz, 0.15s each)
├── 12 green/gold particles burst from the tapped button
├── Narrator: "[Praise line]. [N] [animal type]!"
├── Praise lines rotate: "That's right!" / "Great counting!" / "You got it!" / "Perfect!"
├── Hold celebration for 1.5 seconds
├── Number bar slides down
├── Animals walk off-screen (0.8 seconds)
└── Advance to next round (0.5s pause, then Phase 1 of next round)

PHASE 5B: WRONG ANSWER (1st attempt)
├── Tapped button shakes horizontally (3px, 0.3s) and flashes soft red
├── Ellie shakes head side to side (0.5s animation)
├── Soft low tone (200 Hz, 0.2s) — not harsh
├── Narrator: "Hmm, not quite. Count them again!"
├── Wrong button greys out (cannot be tapped again)
├── Remaining buttons stay active
├── [Sprout] Only 2 choices remain (one is correct — 50% chance)
├── [Sapling/Tree] 3 choices remain
└── Player taps again

PHASE 5C: WRONG ANSWER (2nd attempt)
├── Same shake/flash on the newly tapped wrong button
├── That button also greys out
├── Ellie extends trunk toward the animals
├── Narrator: "Let me help! Count with me."
├── COUNTING SCAFFOLD PLAYS:
│   ├── Each animal highlights in sequence (yellow glow outline, 0.6s per animal)
│   ├── Narrator counts aloud with each highlight: "One... two... three..."
│   ├── After the last animal, narrator says: "[N]! There are [N] [animal type]."
│   ├── A brief pause (0.5s)
│   └── Remaining buttons stay active (2 remain in Sprout, 2 remain in Sapling/Tree)
└── Player taps again

PHASE 5D: WRONG ANSWER (3rd attempt — Sapling/Tree only, Sprout resolves at 2nd)
├── Final wrong button greys out
├── The correct button glows gold with a gentle pulse
├── Narrator: "It's [N]! Tap [N]."
├── Player taps the glowing correct button (confirmation tap)
├── Ellie gives a small nod
├── Narrator: "[N] [animal type]. Let's try the next one!"
├── No celebration animation — just a calm transition
├── Animals walk off (0.8s)
└── Advance to next round

PHASE 6: SESSION END (after round 8)
├── Canvas shows the watering hole at golden hour (warm color shift)
├── Ellie is center-screen, facing the player
├── Narrator: "Great safari, Ranger! You counted [X] groups today!"
├── [X] = 8 (always 8 — the number of rounds, not a score)
├── Ellie does a trunk-wave animation
├── Two buttons appear:
│   ├── "🔄" (replay icon) — starts a new 8-round session at the same tier
│   └── "🏠" (home icon) — returns to tier selection screen
└── No score, no stars, no grade. Just the completion message.
```

### Tier selection screen (game entry point)

```
TIER SELECT
├── Canvas shows a simple scene: Ellie standing next to three paths
├── Three tap targets (one per tier):
│   ├── 🌱 (sprout icon) — left path, bright and sunny
│   ├── 🌿 (sapling icon) — middle path, dappled light
│   └── 🌳 (tree icon) — right path, sunset colors
├── Narrator (on load): "Pick a path, Ranger!"
├── Tapping any icon:
│   ├── Narrator says the tier name: "Calm Morning!" / "Busy Afternoon!" / "Sunset Rush!"
│   └── Transition to round 1 of that tier
├── localStorage saves last-selected tier (only persistence in P1)
└── No lock on any tier. All three available from the start.
```

**Why no tier gating:** At P1, we need to observe whether children self-select appropriate difficulty. Locking tiers would prevent us from seeing if a 4-year-old voluntarily tries Tree and gets confused (useful signal), or if a 6-year-old skips Sprout entirely (also useful signal). Gate tiers at P2B if needed.

---

## 3. Feedback Model

### Design principle
Every piece of feedback must pass one test: **would a 4-year-old understand what just happened without reading anything or having an adult explain it?**

### Correct answer feedback

| Element | Implementation | Purpose |
|---|---|---|
| Button glow | Tapped button fills green (#4ADE80), 0.3s ease-in | Immediate visual confirmation |
| Animal celebration | Species-specific: zebras rear up, flamingos flap wings, frogs jump, turtles bob shells | The world reacts — this is what makes it feel like a game, not a quiz |
| Ellie reaction | Trunk raised, ears flap, body bounces once | Character bond — the guide celebrates with you |
| Sound | Ascending two-tone chime (300→500 Hz, triangle wave, 0.15s each) | Distinct from wrong-answer tone. Learnable after 1–2 rounds. |
| Narrator praise | Rotates through 4 lines, always ends with "[N] [animal type]!" | Reinforces the correct count verbally. The repetition of the number is deliberate — it's a learning moment. |
| Particles | 12 green/gold circles, burst from button center, fade over 0.8s | Juice. Young children respond strongly to particle rewards. |

**Timing:** Celebration holds for 1.5 seconds total. Not shorter (child needs time to register the reward). Not longer (loses momentum between rounds).

### Wrong answer feedback — escalation ladder

| Attempt | What the child sees | What the child hears | What this teaches | Buttons remaining |
|---|---|---|---|---|
| 1st wrong | Button shakes, flashes soft red, greys out | Low soft tone (200 Hz, 0.2s) + "Hmm, not quite. Count them again!" | "That wasn't right, but I can try again." The grey-out prevents repeated wrong taps. | Sprout: 2 left. Sapling/Tree: 3 left. |
| 2nd wrong | Button shakes, greys out. Ellie extends trunk. | "Let me help! Count with me." + counting scaffold (each animal highlights: "One... two... three...") | The scaffold models the correct counting strategy. The child sees HOW to count, not just the answer. | Sprout: 1 left (auto-correct). Sapling/Tree: 2 left. |
| 3rd wrong (Sapling/Tree only) | Button greys out. Correct button glows gold. | "It's [N]! Tap [N]." | Direct answer reveal. The child still taps to confirm — they are never passive. | 1 left (confirmation tap). |

### Critical feedback rules

1. **No score deduction anywhere.** There is no score.
2. **No lives.** There are no lives.
3. **No "game over."** The session always completes 8 rounds.
4. **Wrong buttons grey out permanently within a round.** This prevents the child from tapping the same wrong answer twice and getting stuck in a frustration loop.
5. **The scaffold counts from 1 every time.** It does not start from where the child might have miscounted. It models the full correct strategy.
6. **After a scaffolded round, the next round does NOT increase difficulty.** The round sequence is fixed. The game does not punish struggle by making the next round harder.
7. **Narrator tone never changes.** Same warm voice on round 1 and round 8, whether the child got everything right or needed help on every round.

### Audio implementation

| Audio event | Method | Specification |
|---|---|---|
| Narrator lines | Web Speech API (`speechSynthesis`) | Rate: 0.85 (slower than default). Pitch: 1.1 (slightly higher, friendly). Voice: first available female voice, or default. |
| Correct chime | Web Audio API oscillator | Triangle wave. 300 Hz for 0.15s, then 500 Hz for 0.15s. Gain: 0.3. |
| Wrong tone | Web Audio API oscillator | Sine wave. 200 Hz for 0.2s. Gain: 0.15 (quieter than correct chime). |
| Animal footsteps | Web Audio API noise burst | Short white noise burst (0.05s) filtered through bandpass, gain 0.1. |
| Ellie trumpet | Web Audio API oscillator | Sawtooth wave. Sweep 200→400 Hz over 0.3s. Gain: 0.2. |
| Counting scaffold | Web Speech API | Each number spoken at rate 0.7 (very slow), 0.6s pause between numbers. |
| Button tap | Web Audio API | Click: 800 Hz sine, 0.03s, gain 0.1. |

**Mute button:** An 🔇 icon in the top-right corner. Tapping it toggles all audio. The icon changes to 🔊 when unmuted. This is the only persistent UI element besides the scene.

---

## 4. Playtest Measures

### What to record per round (logged to console, not displayed to the child)

```javascript
{
  round: 1,              // 1–8
  tier: "sprout",         // sprout | sapling | tree
  animalType: "zebras",   // which animal was asked about
  correctAnswer: 4,       // the true count
  attemptsNeeded: 1,      // 1 = first try correct, 2 = one wrong, 3 = two wrong, 4 = scaffold revealed answer
  scaffoldTriggered: false,  // did the counting scaffold play?
  answerRevealed: false,     // did the answer glow (3rd wrong)?
  wrongAnswersTapped: [],    // which wrong numbers were tapped, in order
  timeToFirstTap: 3200,     // ms from number bar appearing to first tap
  timeToCorrectTap: 3200,   // ms from number bar appearing to correct tap (same as above if first-try)
  hadOcclusion: false,       // were any animals partially hidden?
  hadSelectiveCounting: false, // were multiple animal types on screen?
  hadDeparture: false,         // did any animals leave during the round? (Tree only)
  hadLateArrival: false        // did any animals arrive late? (Tree only)
}
```

### What to record per session

```javascript
{
  tier: "sprout",
  rounds: 8,
  firstTryCorrect: 6,        // rounds answered correctly on first tap
  scaffoldCount: 1,           // rounds where counting scaffold triggered
  answerRevealCount: 0,       // rounds where the answer was revealed (3rd wrong)
  avgTimeToFirstTap: 4100,    // ms, averaged across all 8 rounds
  avgTimeToCorrectTap: 5200,  // ms
  sessionDurationSec: 180,    // total wall-clock time from round 1 start to session end
  replayChosen: true           // did the child tap replay or home at session end?
}
```

### Playtest observation questions (for an adult watching)

These are not shown in the game. They are questions for whoever is watching the child play.

**Understanding:**
1. Did the child look at the animals before tapping a number? (Y/N per round)
2. Did the child appear to count (pointing, mouthing, finger-tracking)? (Y/N per round)
3. Did the child seem confused about what to do at any point? (Which round?)

**Engagement:**
4. Did the child watch the celebration animation? (Y/N — indicates whether feedback registers)
5. Did the child react to Ellie (smile, laugh, talk to the screen)? (Y/N)
6. Did the child want to play again after 8 rounds? (Tapped replay / asked to play more / chose home / was pulled away by adult)
7. How long did the child stay engaged before losing focus? (Approximate round number)

**Scaffold:**
8. After the counting scaffold played, did the child's strategy visibly change on the next round? (e.g., started pointing at animals)
9. Did the child appear to deliberately tap wrong to trigger the scaffold? (Possible gaming behavior)

**Difficulty:**
10. Did the child appear bored at any point? (Which tier, which round?)
11. Did the child appear frustrated at any point? (Which tier, which round?)
12. Did the child ask an adult for help? (What did they ask about?)

---

## 5. Stop/Fail Signals

### P1 passes if ALL of the following are true:

1. **A 4–5 year old can complete a Sprout session without adult help.** They understand: look at animals, count, tap the number. No reading, no explanation needed beyond the audio.

2. **First-try accuracy on Sprout is between 50% and 95%.** Below 50% means the game is confusing. Above 95% on all 8 rounds means Sprout is trivially easy and lacks engagement value (the child might as well be tapping randomly on a 1-in-3 chance).

3. **The counting scaffold visibly helps.** At least one child, after seeing the scaffold, changes their counting behavior on a subsequent round (starts pointing, slows down, looks more carefully). If the scaffold plays but the child's behavior doesn't change, it isn't teaching.

4. **At least one child taps replay.** If every child taps home after 8 rounds, the loop is functional but not sticky. At least one child wanting another session is the minimum stickiness signal.

5. **Sapling is measurably harder than Sprout.** First-try accuracy on Sapling should be at least 15 percentage points lower than Sprout for the same child. If both tiers produce the same accuracy, the difficulty knobs (movement, occlusion, selective counting) are not working.

### P1 fails if ANY of the following are true:

1. **The child taps without counting.** If the child consistently taps a number within 1 second of the bar appearing (before they could have counted), they are guessing, not counting. The game is not testing the intended skill. This means the answer bar appears too early, or the visual prompt doesn't connect to the number bar.

2. **The dot patterns cause confusion instead of helping.** If a child taps a button because its dot pattern matches something in the scene (e.g., 4 dots looks like the 4 frogs' arrangement) but the answer is wrong, the dual representation is interfering. Watch for: children who study the buttons instead of the scene.

3. **Audio narration is not understood.** If a child cannot follow the game because the Web Speech API voice is unclear, too fast, or robotic-sounding, the audio-first design fails. This is a technical risk, not a design risk — but it kills P1 equally.

4. **The child gets stuck.** If any round state results in the child being unable to proceed (no buttons to tap, no feedback, frozen screen), the implementation has a bug that breaks the "never stuck" guarantee.

5. **Moving animals at Sapling cause systematic miscounting.** If >50% of Sapling errors are off-by-one in the same direction (always +1 or always −1), movement is causing tracking errors, not counting errors. The occlusion or movement speed needs to be reduced, or Sapling needs to be redesigned.

6. **Tree tier departures produce random guessing.** If Tree accuracy drops below 30% (chance level on 4 choices is 25%), the enter/leave mechanic is too cognitively demanding for the age band. Tree tier would need to be redesigned with simpler dynamics — possibly arrivals only, no departures.

### Kill signal (concept should be paused):

**Sprout is trivial AND Sapling is confusing, with no middle ground.** This means:
- Sprout first-try accuracy >90% (too easy)
- Sapling first-try accuracy <40% (too hard/confusing)
- The gap is not about counting skill — it's about the scene mechanics (movement, occlusion, selective counting) being a cliff rather than a ramp

If this happens, the enumerate-and-report family may not support a 3-tier difficulty ladder at ages 4–6. The concept should be paused and the failure documented before trying a redesign.
