# Lesson: ATC Math Tower — Reusable Patterns (awaiting promotion)

| Field | Value |
|---|---|
| **Date** | 2026-04-06 |
| **Source** | strong example (ATC Math Tower live playthrough L1 + L16 + source analysis) |
| **Game(s)** | ATC Math Tower (reference) |
| **Pass** | cross-pass |
| **Classification** | reusable pattern |
| **Game family** | none (patterns are cross-family) |
| **Failure mode** | multiple patterns that improve replay, persistence, personalization, and session close-out |
| **Tags** | adaptive-difficulty, localStorage, career-total, missed-facts, wind-down, bonus-lives, mechanic-unlock, threshold-display |

## What happened
Eight reusable patterns were extracted from ATC Math Tower's 2557-line source code and live gameplay across Level 1 (training) and Level 16 (3-runway mid-game). All are proven in a shipped game with 25 levels of progressive complexity.

## Patterns

### 1. Adaptive Difficulty from Training Data
During levels 1-3, record how much patience/time the player uses per action. After training, compute a single adaptive multiplier: fast players get EXPERT pace (<1.0×), slow players get RELAXED pace (>1.0×). This one number personalizes the entire difficulty curve.
- ATC: `adaptiveMult` computed from `dispatchPatienceSamples` after Level 3
- Applies to: any timed-response game

### 2. Version-Keyed localStorage
Store a game version string in localStorage. On load, if the version doesn't match, wipe all stale keys and start fresh. Prevents corrupted save states from older builds.
- ATC: checks `atcVersion`, clears `atcUnlocked`, `atcLives`, `atcBestScores` etc. on mismatch
- Applies to: every game with localStorage persistence

### 3. Career Total as Sum of Per-Level Bests (No Double-Dipping)
Each level stores its best score. Career total = sum of all per-level bests. Replaying a level only improves career total if you beat your previous best. Genuine peak performance metric, not grind.
- ATC: `levelBestScores` Map, `careerTotal()` function
- Applies to: any game with per-level scoring and career progression

### 4. Missed Facts Review (Grouped by Operation)
End-of-level screen shows the specific math facts the player got wrong, grouped by operation type with the correct answers highlighted. Not "you made 3 errors" — shows "7×8=56, 9×6=54."
- ATC: `missedFactsHTML()` groups by operation with color-coded answers
- Partially exists in our games as debrief takeaway, but ATC's is more specific

### 5. Wind-Down Phase
When score threshold is met: clock FREEZES, time bonus awarded (+50/sec remaining), in-flight actions allowed to complete, then level ends. No abrupt cutoff mid-action.
- ATC: `windingDown` flag, `⭐ THRESHOLD CLEARED — CLEARING TRAFFIC` banner
- Applies to: any game with a score threshold endpoint

### 6. Bonus Lives at Milestone Levels
Specific levels award an extra life (only once ever per level, tracked in localStorage). Creates anticipation and rewards persistence without making the game easier through grinding.
- ATC: `BONUS_LIFE_LEVELS` array, `bonusLivesAwarded` Set
- Applies to: any game with a lives system and 10+ levels

### 7. Mid-Career Zero-Pressure Mechanic Unlocks
When a new mechanic appears (3rd runway at L16, 4th at L21), the game pauses to show a full-screen announcement: what it is, how to use it, what key to press. No timer during the announcement. Then gameplay resumes.
- ATC: overlay with "NEW RUNWAY UNLOCKED — RWY 36C — GREEN PLANES" + "GOT IT" button
- Applies to: any game that introduces new mechanics after the initial tutorial

### 8. Live Threshold-Gap Display ("NEED X")
The HUD shows in real-time how many more points are needed to clear the level. The number counts down with every correct answer. Changes color when time is running low and the gap is still large (red = danger). More visceral than a static threshold.
- ATC: `NEED 2400` display, color shifts from amber → red when behind pace
- Applies to: any game with a score threshold

## What the OS should learn
The best educational games layer multiple proven patterns that work together: adaptive difficulty personalizes the experience, version-keyed persistence prevents data corruption, career totals prevent grinding, and wind-down phases create satisfying endings. No single pattern makes the game great — it's the combination.

## Applies to future games when
Any game reaches P4 (replay) and needs to add persistence, personalization, or career progression. Search for these patterns before implementing custom solutions.

## Promotion target
`docs/reusable_patterns_library.md` when library expansion is justified

## Status
- [x] Captured
- [ ] Promoted to: docs/reusable_patterns_library.md
