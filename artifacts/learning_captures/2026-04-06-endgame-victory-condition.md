# Lesson: Every level must have a reachable victory condition

| Field | Value |
|---|---|
| **Date** | 2026-04-06 |
| **Source** | audit |
| **Game(s)** | Fire Dispatch |
| **Pass** | P1 |
| **Classification** | general rule |
| **Game family** | none |
| **Failure mode** | L5 had no endpoint — the game spawned incidents indefinitely until lives ran out. The player could never win. |
| **Tags** | victory, endpoint, win-condition, level-completion, session-end |

## What happened
Fire Dispatch L5 checked `prevLevel < 4` before allowing level advancement, which prevented the game from ever ending on success at the final level. The only way to end was running out of lives. The player could never "win."

## What the OS should learn
Every level — especially the final level — must have a reachable victory condition. If the advancement check blocks at the last level, an explicit session-victory path must exist.

## Evidence
Fix commit `5e5b84d`. Added L5 victory trigger: when score >= threshold at L5, set sessionComplete and show shift_end overlay. Reused the existing end-screen infrastructure.

## Applies to future games when
Any game has a final level or highest difficulty tier. Verify that the player can reach a victory state, not just a death state.

## Promotion target
Should be caught by P1 exit criteria ("the player can complete or fail a run for understandable reasons") — but P1 audits should explicitly check that completion is reachable at every level, including the last.

## Status
- [x] Captured
- [x] Promoted to: already enforced by P1 exit criteria (this capture adds the specific failure case)
