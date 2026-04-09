# Echo Heist — Pass 4 Record

## Pass purpose
Content integration + educational depth. Replace procedural District 3 with authored content, add scaffolding tools for students who get stuck, track mission objectives, persist progress, and expand the echo system.

## What was proved
- Authored D3 prompts produce richer, contextualised questions aligned to GDD curriculum
- Scaffolding panel gives visual cues without giving away answers — supports age 11–13 working memory
- Auto-hint after 2 wrong answers prevents frustration spirals
- localStorage persistence lets players track personal bests and unlocks across sessions
- Two echo charges per run make the system feel tactical rather than a one-time novelty

## What changed from Pass 3

### 1. District 3 curated content (missions 21–30)
Replaced `generateDistrictMissions(21, 30, 'Escape Lines', …)` with a `D3_MISSION_DATA` constant authored from the GDD content sheet. Each mission has 5–6 room prompts, 3 vault locks, and 1 escape prompt — all with `template`, `answer`, `hint1`, and `hint2` fields.

Curriculum coverage across D3:

| Template | Skill |
|---|---|
| T1 | One-step equations (x/8=6, x−27=14) |
| T2 | Two-step equations |
| T3 | Percent change (increase / decrease / discount) |
| T4 | Decimal ↔ percent conversion |
| T5 | Fraction of quantity |
| T6 | Fraction addition / subtraction |
| T7 | Rate-time-distance |
| T8 | Rate comparison (A or B) |
| T9 | Integer operations |
| T10 | Rounding (nearest 0.1, 0.01, 10, 100) |
| T11 | Angle relationships (complementary, supplementary, right, full) |
| T12 | Expected value |

### 2. Math scaffolding panel (F key)
Pressing F during any math or vault popup toggles a 194×270px reference panel drawn to the left of the canvas. Content varies by `mathPrompt.template`:

- T5/T6: Coloured fraction bars (1/2, 1/3, 2/3, 1/4, 3/4, 1/8)
- T7/T8: Rate triangle d=r×t with colour-coded compartments
- T9: Integer number line −15 to +15
- T10: Rounding guide (≥5 → round up, <5 → keep)
- T11: Three arc diagrams (90°, 180°, 360°)
- T12: EV formula with labelled terms
- T1/T2: Balance scale metaphor
- T3/T4: Percent–decimal strip
- vault/general: Number line −10 to +20

`scaffoldVisible` resets on every popup open/close.

### 3. Mission objective tracking
Three missions gained `objType` / `objTarget` fields:
- Mission 1: `stealth` (maxHeat ≤ 30 throughout mission) → +200
- Mission 2: `cameras` (disable ≥ 2) → +200
- Mission 3: `doors` (open ≥ 3 doors) → +200

`objCount` increments in `closeMathPopup` when a door opens or camera disables. `maxHeat` is tracked continuously. `finishMission` evaluates the condition and awards the bonus. Results screen shows the bonus if earned.

D3 missions 21, 24 also carry objectives (`stealth` and `doors` respectively).

### 4. Auto-hint after 2 wrong answers
`wrongCount` resets on each popup open. On the 2nd wrong answer, `showHint(true)` fires automatically — displayed as "🔔 Auto-hint:" prefix, **no score deduction** (free). The existing H-key hint still costs score as before.

### 5. localStorage persistence
`highScores` (keyed by mission ID) and `completedMissions` (Set of IDs) are loaded on page initialisation and saved after every `finishMission`. Results screen shows "★ NEW BEST!" in gold or the previous best in grey. Menu shows total missions completed.

### 6. Multiple echoes (2 charges per run)
`echoAvailable` replaced by `echoCharges = 2`. `echoGhost` replaced by `echoGhosts[]` array. `stopEchoRecording` pushes each ghost; the array keeps at most 2 active ghosts. HUD shows `ECHO ×2`, `ECHO ×1`, or `▶ REPLAY`.

## Files
| File | Role |
|------|------|
| `current.html` | Live version (Pass 4) |
| `pass-4-record.md` | This document |
| `playtest.js` | Extended test suite |

## Known limitations
- `objType: 'stealth'` missions give bonus if `maxHeat ≤ target` — guard vision during escape phase can push heat above threshold; D3 mission 21 uses target 35 to account for this.
- Scaffold panel overlaps the world canvas, not the DOM popup — on very narrow viewports the panel could clip.
- Playtest suite does not test DOM-dependent features (scaffoldVisible rendering, localStorage writes with DOM stubs).

## Deferred to Pass 5
- Ability visual effects, stealth drone, daily contract, mission select, class unlocks → delivered in Pass 5.
