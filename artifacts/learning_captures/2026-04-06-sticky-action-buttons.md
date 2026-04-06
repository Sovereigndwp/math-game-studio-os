# Lesson: Action buttons must be visible without scrolling

| Field | Value |
|---|---|
| **Date** | 2026-04-06 |
| **Source** | fix |
| **Game(s)** | Fire Dispatch, Unit Circle |
| **Pass** | P1 |
| **Classification** | general rule |
| **Game family** | none |
| **Failure mode** | Primary action buttons (Confirm Topping, DISPATCH) were below the viewport fold on desktop screens. Player had to scroll to find the main action. |
| **Tags** | sticky-button, viewport, scrolling, action-button, desktop-layout |

## What happened
Both Fire Dispatch (DISPATCH button) and Unit Circle (Confirm Topping button) placed their primary action button at the bottom of a tall vertical stack. On typical desktop viewports (768-900px height), the button was below the fold. The player could read the prompt and interact with the game elements but had to scroll down to confirm their action.

## What the OS should learn
The primary action button must be visible at all times without scrolling — use `position: sticky; bottom: 0` on the button or its wrapper.

## Evidence
Fix commit `9b35854`. Added `position: sticky; bottom: 16px; z-index: 10` to Unit Circle's submit-btn and `position: sticky; bottom: 0; z-index: 10; background: #1c1418` to Fire Dispatch's dispatch-btn-wrap. Bakery Rush did not need this fix — tapping pastries is the direct action (no confirm button).

## Applies to future games when
Any game uses a vertical single-column layout with a confirm/submit/dispatch button at the bottom. Test on a 768px viewport before shipping.

## Promotion target
Should become part of a P1 usability checklist or release readiness check.

## Status
- [x] Captured
- [ ] Promoted to: candidate for release readiness checklist
