# Echo Heist — Pass 3 Record

## Pass purpose
Feel proof. The mechanics were solid after Pass 2 — this pass adds the sensory and motivational layer that makes the game feel responsive, tense, and rewarding to play.

## What was proved
- Math answers now have clear juice (particles, screen shake) that rewards fast, correct answers
- Guards navigate around walls instead of walking through them
- Focus mode gives players a mechanical tool for hard prompts, with a real cost
- Mastery streaks create a meta-reward loop above single-answer scoring
- Results screen now tells the player *what* they need to practice, not just a letter grade
- Escape phase is loud and rhythmic — the alarm beeping escalates as the countdown shrinks

## What changed from Pass 2

### 1. Particle system
A lightweight per-frame particle array sits in world-space and is rendered inside the shake transform.

| Trigger | Effect |
|---------|--------|
| Correct answer | 18 green particles burst from popup centre |
| Wrong answer | 12 red particles + screen shake (3px, 0.3s) |
| Vault lock cracked | 22 gold particles burst from loot position |
| Mastery unlocked (streak ≥ 3) | 25 gold particles burst above popup |
| Guard catches player | 8px screen shake for 0.5s |
| Wrong vault answer | 4px screen shake for 0.35s |

### 2. Screen shake
A decaying shake offset (`shakeX`, `shakeY`) is applied via `ctx.translate` around all world-space drawing calls. The HUD, overlays, and results screen are drawn after `ctx.restore()` and are unaffected.

### 3. Guard wall avoidance (`moveEntityToward`)
Guards previously moved directly toward targets, ignoring walls. A new `moveEntityToward(entity, tx, ty, speed, dt)` helper applies the same axis-separated collision logic the player uses — trying X movement independently, then Y. All three guard states (patrol, investigate, chase) now use this helper. Guards slide along walls instead of phasing through them.

### 4. Focus mode (Tab key)
Pressing Tab during any math popup toggles focus mode:
- Guards and cameras update at 25% normal speed (`FOCUS_TIME_SCALE = 0.25`)
- Score drains at 2 pts/sec while active
- Visual: purple radial vignette + pulsing `⏸ FOCUS MODE` label at bottom of canvas
- Popup border turns purple (`focus-mode` CSS class)
- Focus mode resets when any popup closes

### 5. Mastery streaks
The game tracks consecutive correct answers per skill template (`streaks[tpl]`). When a streak reaches 3:
- `masteryTemplates[tpl]` is set to true (persists for the mission)
- A gold particle burst fires
- Subsequent answers for that template get a ×1.1 score multiplier
- Hint cost for that template reduces to 75% of district base cost
- Streak counter shows in the HUD top bar as 🔥 ×N (amber → gold at mastery)

Templates tracked: T1–T12 from mission data, `vault` for vault locks, `general` for procedural prompts without a template tag.

### 6. Results screen — per-skill breakdown
The results screen was redesigned to fit more information without scrolling:
- Score and grade shown side by side at the top
- 6 stats in a 2-column grid (Accuracy, Avg Solve, Heat / Time, Loot, Hints)
- New SKILL BREAKDOWN section below the stats, showing one row per skill template with:
  - Template name + 🔥 badge if mastery was reached
  - Color-coded progress bar (green ≥ 80%, amber ≥ 50%, red < 50%)
  - Fraction label (e.g. `3/4`)
- Up to 7 skill rows shown

### 7. Escape alarm audio
When the escape phase starts, a `setTimeout`-based pulse loop plays a square wave beep:
- 440 Hz every 480ms when countdown > 15s
- 660 Hz every 280ms (urgent) when countdown ≤ 15s
- Stops on `finishMission()` or when player is caught
- Respects the M-key mute toggle

### 8. Vault hint support
`handleVaultKey` now handles `H` for hints (previously it only existed in `handleMathKey`). Vault prompts already had `hint1`/`hint2` fields; they are now accessible during vault solving.

## Updated controls
```
WASD       Move
Shift      Crouch (quieter + slower)
E          Interact (doors, terminals)
Space      Class ability
Q          Place gadget
R          Record/stop echo
H          Hint during any math popup (−50 pts, or less with mastery)
Tab        Toggle focus mode during math popup (−2 pts/sec)
M          Mute/unmute audio
Esc        Cancel math popup (costs heat)
```

## Files
| File | Role |
|------|------|
| `current.html` | Live playable version (Pass 3) |
| `pass-1.html` | Frozen Pass 1 checkpoint |
| `pass-1-record.md` | Pass 1 design record |
| `pass-2-record.md` | Pass 2 design record |
| `pass-3-record.md` | This document |
| `playtest.js` | Headless test suite (Pass 2 baseline, 213 tests) |

## Known limitations at this pass
- Guard waypoint routes are not wall-aware; if a waypoint spawns inside a wall segment on a procedural map, the guard will slide against the wall until the alertTimer expires. Rare but observable.
- Mastery streaks reset on retry (loadLevel call). Intentional — mastery is a within-run reward.
- Focus mode does not slow the vault timer countdown, only guards and cameras. This is intentional: the vault timer is the primary tension source.
- Playtest suite (playtest.js) covers Pass 2 features but has not yet been extended to cover Pass 3 additions (particles, streaks, focus mode, wall avoidance). Extend before Pass 4.

## Deferred to Pass 4+
- Ability visual effects (screen tint, particle trail on Runner Burst)
- Meta-progression unlocks (Fraction Lens, Percent Wheel, Rate HUD)
- Daily contract mode (fixed seed for same mission across players)
- Leaderboard / session persistence
- Extend playtest suite for Pass 3 systems
