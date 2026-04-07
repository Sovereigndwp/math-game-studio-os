# Echo Heist — Pass 1 Record

## Pass purpose
Core loop proof. Does the concept work at all? Is math inside the action, not beside it?

## What was built
Self-contained HTML5 Canvas stealth game. No server, no dependencies, no build step.
Open `pass-1.html` directly in a browser.

## Core loop proven
```
Stealth movement → math-as-lockpick → vault sequence → escape chase → score
```
Every step requires math. There is no UI mode that feels like a separate quiz.

## Systems implemented

### Stealth engine
- WASD movement with AABB tile collision
- Crouching (Shift): 0.5× speed, 0.3× noise generation
- Tile-based noise values: carpet 1/s, floor 3/s, metal 5/s
- Noise meter decays at 8/s when not moving

### Guard AI
- Waypoint patrol routes
- Vision cone: configurable angle + range, direction indicator
- State machine: patrol → investigate → chase
- Line-of-sight check (20-step raycasting)
- Noise reaction: guards investigate player position if noise > 40 and within 6 tiles
- Crouch reduces effective detection range by 40%

### Camera system
- Sweeping cones: configurable angle, range, sweep speed
- Detection raises heat continuously while player is in cone + has line of sight
- Individual disable via terminal solve

### Math popup
- Typed input (not multiple choice)
- Equivalent form acceptance: 1/2 = 0.5 = .5, 30% = 0.3, whitespace tolerance
- Wrong answer: heat +5, field clears, try again
- Esc cancels: heat +10
- Score bonus scales inversely with solve time

### Echo system
- R key: record player path for 15s
- Ghost sprite with trail replays the recorded path in sync
- One echo per mission

### Vault sequence
- Triggered when player reaches loot (not instant pickup)
- 2–3 harder math prompts chained, must solve all to crack vault
- Popup shows step progress (dots: done/active)
- 90s vault timer — expire = caught
- Vault modal cannot be abandoned with Esc

### Escape sequence
- Triggered immediately after vault cracks
- Guards speed up 1.6×, cone range +30%, cone angle +20%
- Escape gate placed as a locked door on the path to EXIT
- One more math prompt to unlock the gate
- 60s countdown — expire = time's up
- Score bonus for remaining escape time (+5 pts/sec)

### 3 classes (stats only in Pass 1)
| Class | Speed | Noise mult | Ability name |
|-------|-------|-----------|--------------|
| Hacker | 2.2 | 1.0× | Overclock |
| Ghost | 2.0 | 0.7× | Soft Step |
| Runner | 2.8 | 1.2× | Burst |

Classes affect feel (Ghost is quieter, Runner is faster) but abilities are not yet active.

### HUD
- Top bar: class, mission name, countdown timer, score
- Bottom bar: heat meter, noise meter, math accuracy, echo status, loot status
- Controls strip at bottom

### Scoring
- Puzzle solved: 10–100 pts (based on solve time)
- Vault lock: 20–150 pts
- Escape gate: 100 pts
- Loot pickup: 200 pts (via vault)
- Vault completion: 300 pts bonus
- Escape bonus: escapeCountdown × 5 pts
- Time bonus: (missionTimeLimit − elapsed) / 10
- Stealth bonus: (100 − heat) × 3
- Accuracy bonus: (correct / total) × 200

### Results screen
- Score breakdown visible
- Math accuracy + avg solve time
- S/A/B/C grade (90/70/50%)
- Per-template stats shown (accuracy by skill type)

## Missions
3 hand-crafted missions, District 1: Training Gallery.

| M | Name | Focus |
|---|------|-------|
| 1 | Orientation Hall | Integers, fractions, rate |
| 2 | Camera Basics | Angles, percents |
| 3 | Quiet Floors | Fractions, integers |

Each mission: 6 room prompts + 2–3 vault prompts + 1 escape prompt.

## Playtest results
71 tests, 0 failures. Verified headlessly via `playtest.js`.

Phases tested: menu → class select → briefing → stealth → echo → vault → escape → results → retry → full success run → mission progression.

## Key design decisions

**Math is the lockpick, not a side panel.** Solving a percent problem literally opens the door. This was the critical test and it passes.

**Vault cannot be escaped.** Once you reach the loot you are committed to solving it. This adds the "heist moment" tension the GDD required.

**Typed answers, not multiple choice.** Equivalent forms are accepted. This is the right call for 11–13: it requires recall not recognition, but doesn't penalise format variation.

**Single HTML file.** Follows the repo convention established by bakery, fire, unitcircle prototypes.

## Deferred to Pass 2
- Class abilities (Space key) — classes feel identical in Pass 1
- Gadget (Q key)
- Audio feedback
- Hint system
- Districts 2 & 3 (missions 4–30)
- Difficulty scaling across districts
- Mastery streaks, meta-progression
- Focus mode (Tab slow-time)
- Procedural room generation
