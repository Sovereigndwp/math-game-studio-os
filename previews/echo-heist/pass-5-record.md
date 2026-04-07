# Echo Heist — Pass 5 Record

## Pass purpose
Meta + visual flair. This pass adds the motivational and social layer — player progression, daily challenges, mission selection, ability payoff visuals, and atmospheric audio — that turns a working prototype into a replayable product.

## What was proved
- Class unlock progression gives new players a structured path through the game
- Daily contract mode creates a shared challenge with no extra infrastructure
- Mission select lets players freely revisit weak skill areas without replaying sequentially
- Ability effects make class choice feel tactile and visible
- Stealth drone creates the ambient tension that math puzzles need to feel high-stakes

## What changed from Pass 4

### 1. Class unlock progression
`isClassUnlocked(cls)` gates Ghost (≥5 completed missions) and Runner (≥10). `completedMissions.size` is read from localStorage so progress persists. Locked class cards show a 🔒 overlay with requirement text. The menu prevents selecting a locked class. `startDailyContract()` picks from unlocked classes only.

### 2. Daily contract mode (D key on menu)
`getDailySeed()` uses today's date (YYYYMMDD integer). `startDailyContract()` uses `seed % 30` for mission and `seed % unlockedClasses.length` for class. Launches directly to briefing. A `📅 DAILY` badge shows in the HUD top-right.

### 3. Mission select screen (S key on menu)
`STATE.MISSION_SELECT` renders a 5×6 grid of 30 mission cards. Each card shows:
- Mission number in district colour
- ✓ if completed
- Short mission name
- Personal best score (if any) in gold
- `[ENTER]` prompt on the selected card

Navigation: arrow keys. Enter starts the selected mission. Esc returns to menu.

### 4. Ability visual effects
All three class buffs now have canvas-level feedback:

| Class | Effect |
|---|---|
| Hacker (Overclock) | Faint purple world tint overlay while buff is active |
| Ghost (Soft Step) | Expanding cyan ring emanating from player position on activation |
| Runner (Burst) | Continuous orange particle trail from player while sprinting |

The soft-step ring uses `softstepFlashTimer` (set to 0.5s on buff activation). The burst trail spawns 2 particles/frame in `updatePlayer`.

### 5. Ambient stealth drone
`startStealthDrone()` creates a 55 Hz triangle oscillator (gain: 0.018) that fades in over 1.2s when a mission begins via `handleBriefingKey`. `stopStealthDrone()` fades it out when the escape alarm starts or the mission ends. The oscillator is properly cleaned up with a 500ms delayed `.stop()` call.

## Updated controls
```
WASD       Move
Shift      Crouch
E          Interact
F          Toggle scaffold panel
Space      Class ability
Q          Gadget
R          Echo (×2 charges)
Tab        Focus mode
H          Hint (free after 2 wrong)
M          Mute
Esc        Cancel popup / exit select screen

(on Menu)
← →        Select class
S          Mission select screen
D          Daily contract
Enter      Start with selected class
```

## Files
| File | Role |
|------|------|
| `current.html` | Live version (Pass 4 + 5) |
| `pass-5-record.md` | This document |

## Known limitations
- Daily contract is purely client-side; two players on different machines will get the same mission only if their local dates match. No server seed.
- Mission select starts the mission with whatever class was last selected on the menu. This is intentional — the player should choose class first, then browse missions.
- Stealth drone will not start if the user has not yet pressed a key (Web Audio API autoplay restriction). On the briefing screen, pressing ENTER always satisfies this.

## Deferred to future passes
- Leaderboard / shared daily seed (requires server)
- Meta-progression tool unlocks (Fraction Lens, Percent Wheel, Rate HUD)
- Adaptive difficulty based on per-skill accuracy history
- Playtest suite extension for Pass 4 + 5 systems
