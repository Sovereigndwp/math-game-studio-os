# Learning Captures

Structured lessons captured after meaningful fixes, audits, passes, and playtests. Each capture describes what the OS should learn from one specific event, with metadata that supports retrieval by game family, pass type, failure mode, and keywords.

## Purpose
Store lessons as individual findable artifacts. Lessons start here. If they prove general enough, they get promoted to rules, design checks, or patterns.

## When to capture a lesson
Immediately after:
- A fix that corrected a real usability, fairness, or design problem
- An audit that found a gap the OS should not repeat
- A pass closure that revealed something reusable
- A playtest that changed understanding of what works
- A strong example from a reference game

Do not capture routine commits, typo fixes, or doc formatting changes.

## File naming

`YYYY-MM-DD-<short-description>.md`

Examples:
- `2026-04-06-subtraction-shortcut.md`
- `2026-04-06-near-miss-feedback.md`
- `2026-04-06-grocery-dash-family-rules.md`

## Classification categories

| Classification | What it means | Promotion destination |
|---|---|---|
| **General rule** | Applies to every game | `docs/os_engagement_rules.md` or `docs/pass_rules.md` |
| **Pass-specific rule** | Applies to one pass type across all games | `docs/pass_rules.md` under the relevant pass |
| **Game-family rule** | Applies to a type of game (e.g., subset-sum games) | `docs/game_families/` (when created) |
| **Reusable pattern** | A proven solution portable to future games | `docs/reusable_patterns_library.md` |
| **Design check** | Should be evaluated before build | `docs/design_checks/` |
| **Agent/check candidate** | Worth formalizing if it keeps repeating | Lightweight candidates list (when needed) |
| **Local fix only** | One game, one time, no generalization | Stays in pass record or playtest note |

## Game family values

Use one of these when applicable:
- `combination-allocation` — player selects from options to reach a target (Fire Dispatch, subset-sum games)
- `tap-accumulation` — player taps items to build a running total (Bakery Rush)
- `precision-placement` — player places something at a specific position (Unit Circle)
- `recipe-scaling` — player scales quantities and optimizes packs (Grocery Dash)
- `spatial-navigation` — player navigates physical space under pressure
- `none` — lesson is not family-specific

## Promotion path

```
Local fix (pass record / playtest note)
  ↓ worth remembering beyond this game
Captured lesson (this folder)
  ↓ appears in 2+ games or 2+ passes
Reusable pattern or game-family rule
  ↓ should be checked before every build
Design check or general rule
```

Promotion criteria:
- 1 occurrence → captured lesson
- 2+ occurrences across games/passes → pattern or game-family rule
- Would have prevented a known failure → design check
- Keeps being missed → general rule

---

## Template

```markdown
# Lesson: [Short title]

| Field | Value |
|---|---|
| **Date** | |
| **Source** | [fix / audit / playtest / pass / strong example] |
| **Game(s)** | |
| **Pass** | [P1 / P2A / P2B / P3 / P4 / P5 / pre-build / cross-pass] |
| **Classification** | [general rule / pass rule / game-family rule / reusable pattern / design check / agent candidate / local fix] |
| **Game family** | [combination-allocation / tap-accumulation / precision-placement / recipe-scaling / spatial-navigation / none] |
| **Failure mode** | [what went wrong or what gap this addresses] |
| **Tags** | [2-5 keywords, comma-separated] |

## What happened
[1-3 sentences — concrete, not abstract]

## What the OS should learn
[1 sentence rule or principle]

## Evidence
[What proves this lesson is real — commit hash, playtest note, audit finding, or source game reference]

## Applies to future games when
[1 sentence describing when a future game or pass should retrieve this lesson]

## Promotion target
[Where this should live if promoted, or "none — local fix only"]

## Status
- [ ] Captured
- [ ] Promoted to: [target]
```

---

## How to Search Captures

Three retrieval methods, all manual grep for now:

### By game family
When starting a new game, find lessons from similar games:
```bash
grep -rl "Game family.*combination" artifacts/learning_captures/
```

### By pass type
When starting a new pass, find lessons from the same pass type:
```bash
grep -rl "Pass.*P2B" artifacts/learning_captures/
```

### By failure mode or tags
When diagnosing a problem, search for related failures or keywords:
```bash
grep -rl "failure_mode.*constant.total" artifacts/learning_captures/
grep -rl "Tags.*replay.*variation" artifacts/learning_captures/
```

## When to Search Captures

Before any new game or new pass, run a 30-second capture scan:

1. **New game concept** → grep for the game's family
2. **New pass starting** → grep for the pass type
3. **Diagnosing a problem** → grep for the failure mode
4. **Game feels dead or repetitive** → grep for relevant tags

This takes 30 seconds and surfaces lessons the OS has already learned.

---

## Automation roadmap

| Capability | Now | Later (when captures > 20) |
|---|---|---|
| Writing captures | Manual | Manual (human judgment needed) |
| Searching captures | Manual grep | Agent scans before each pass |
| Matching to new games | Manual grep by family | Game Experience Spec triggers capture scan |
| Promotion decisions | Manual | Agent flags captures with 2+ occurrences |
