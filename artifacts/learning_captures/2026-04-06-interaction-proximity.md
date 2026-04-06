# Lesson: Prompt, action, and confirm must be within one eye-scan

| Field | Value |
|---|---|
| **Date** | 2026-04-06 |
| **Source** | fix |
| **Game(s)** | Fire Dispatch |
| **Pass** | P1 |
| **Classification** | general rule |
| **Game family** | none |
| **Failure mode** | Demand number (top of screen) was 4-5 elements away from the dispatch button (bottom). Player constantly scanned top-middle-top-middle-bottom to complete one action. |
| **Tags** | interaction-proximity, eye-travel, layout, vertical-distance, motor-friction |

## What happened
Fire Dispatch's mission card (with the demand number) was at the top, truck selection in the middle, and the DISPATCH button at the bottom. The player had to scan the full screen height on every incident. The fix compacted the mission card (reduced padding, emoji size, demand font) and made the board's "of X" demand label more prominent so the player could work from the board alone.

## What the OS should learn
Prompt, action, and confirm must be within one eye-scan — no more than 2 element-heights of vertical or horizontal distance between reading the prompt and pressing the action button.

## Evidence
Fix commit `773f28e`. Mission card padding reduced, emoji 44→32px, demand 42→32px. Board demand label upgraded to 13px/600 weight. Rule promoted to OS Rule 12 in commit `bd92ce7`.

## Applies to future games when
Any game uses a vertical single-column layout where the prompt is at the top and the action button is at the bottom. Especially games with a read → select → confirm flow.

## Promotion target
Already promoted to `docs/os_engagement_rules.md` Rule 12.

## Status
- [x] Captured
- [x] Promoted to: docs/os_engagement_rules.md Rule 12
