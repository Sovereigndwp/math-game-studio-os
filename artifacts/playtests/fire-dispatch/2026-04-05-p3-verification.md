# Playtest: Fire Dispatch — P3 Verification

| Field | Value |
|---|---|
| **Date** | 2026-04-05 |
| **Game** | Fire Dispatch |
| **Build** | current.html as of 27f5295 (pre-L5 fix) |
| **Tester** | Claude (browser automation) |
| **Session type** | verification |

## What was tested
P3 personality elements: named incident types with emoji/location/dispatch lines, dispatch status strip, star ratings, mission debrief with contextual takeaway. Also tested tutorial flow end-to-end.

## Strongest positives
- Tutorial is clean: 3 steps (match, combine, overshoot prevention), zero timer pressure, one mechanic per step
- Incident personality works: "House Fire — Oak Street — Family trapped on second floor!" creates real urgency
- Status strip reacts: "Standing by for incoming calls" at start
- Debrief on failed run is specific: "You ran out of time more than you succeeded. Try planning your truck combination before tapping."
- Star rating (1 star on bad run) feels honest, not punishing

## Strongest negatives
- Incident pool is only 6 types — will repeat quickly across sessions
- Dispatch lines are static per type — every Factory Fire says the same thing
- Resolved lines flash briefly during success animation, easy to miss
- L5 had no victory endpoint (fixed in subsequent commit 5e5b84d)
- All 5 trucks sum to 20, enabling subtraction shortcut (separate issue, not yet fixed)

## Where they stopped
Game over at Round 3, Level 1. 0 incidents resolved, 3 timeouts. Score 0, 1 star. Tester was too slow with browser automation clicks — not a game design issue.

## One sentence verdict
P3 worked — incidents feel like real emergency calls, not generic math prompts.

## Recommended next
Fix subtraction shortcut (P2B fairness). Then P4: larger incident pool, randomized locations within type.
