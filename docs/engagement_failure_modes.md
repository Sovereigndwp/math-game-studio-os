# Engagement Failure Modes

## Purpose
Give a shared vocabulary for sticky-game failures so diagnosis is fast and repeatable.

## Use this when
At the start of every audit. When a playtest feels wrong but you cannot name why. When choosing the next pass.

## Controls
- Match symptoms to failure mode numbers before proposing a fix
- Name the primary failure mode (not three)
- Use the pass-to-fix column to pick the right pass type
- Add new failure modes only when a genuinely new pattern is observed

## Do not use this for
- Implementation details
- Level-specific tuning (use `level_role_map.md`)
- Deciding pass/fail on completed work (use `pass_fail_scorecard.md`)

Instead of reinventing the diagnosis each time, say: "this is failure mode 4 and 9."

---

## The Failure Modes

| # | Failure mode | Pass to fix | What it looks like |
|---|---|---|---|
| 1 | **Feels like a tool, not a game** | P3 | No personality, no world reaction, no emotional moments. Player could be using a worksheet. |
| 2 | **Math is not the verb** | P0/P1 | The math action is not the primary scoring/gating/survival mechanic. Player can succeed by ignoring the math. |
| 3 | **Speed hides the thinking** | P2B | Timer or belt speed is so tight that the player fails from motor skill, not from mathematical reasoning. |
| 4 | **No payoff** | P2A | Session ends with no star rating, no debrief, no "how did I do?" moment. The run just stops. |
| 5 | **No reason to replay** | P4 | Same problems, same sequence, same outcome. Nothing is different on the second run. |
| 6 | **World does not react** | P3 | Score changes but customers/fires/environment stay static. Success and failure look the same. |
| 7 | **Progression combines too many new demands** | P2B | A new level adds new representation + faster speed + more items + new penalty simultaneously. |
| 8 | **Debrief does not teach anything** | P2A | End screen shows score but not what went wrong. Player knows they failed but not why. |
| 9 | **Stars do not mean anything** | P2A | Star rating exists but barely passing and perfect play feel the same. No differentiation. |
| 10 | **Theme is pasted on** | P3 | The bakery/fire/pizza wrapper could be removed and the game would feel identical. |
| 11 | **First experience is confusing** | P1 | No tutorial, no zero-pressure learning phase. Player dropped into full pressure immediately. |
| 12 | **Failure is invisible** | P1/P2B | Player fails but nothing visible changes — no patience drain, no life lost, no character reaction. |
| 13 | **Failure is unrecoverable** | P1 | One mistake ends the round. Player cannot learn within the same attempt. |
| 14 | **Success is flat** | P3 | Every correct action gets the same reaction. Easy wins and hard wins feel identical. |
| 15 | **Challenge tests the wrong skill** | P2B | The bottleneck is mouse speed, not arithmetic. Or reading speed, not spatial reasoning. |
| 16 | **Levels have no clear job** | P2B | Cannot explain what a level teaches vs. tests. Levels just get "harder" vaguely. |
| 17 | **Answer is shown during play** | P1 | The game reveals the solution before the player reasons through it. Removes the thinking. |
| 18 | **Setup friction** | P5 | Requires install, account, configuration, or specific browser. Teacher gives up before students play. |
| 19 | **Generic feedback** | P2A | "Good job!" and "Try again!" instead of "You overshoot most on targets > 10." |
| 20 | **No near-miss feedback** | P2B/P3 | Close and far-off mistakes feel identical. Player cannot calibrate. |

---

## How to use this

### At the start of an audit
Read through the list. For each failure mode, ask: does this game have this problem?

### When diagnosing a playtest result
Match the symptom to a failure mode number. Then check which pass type fixes it.

### When planning a pass
Check: does this pass address a specific failure mode? If not, the pass might be too vague.

### Quick severity check
- Modes 1-3: the game's identity is broken → fix before anything else
- Modes 4-9: the game works but does not engage → fix in P2A/P2B/P3
- Modes 10-16: specific quality gaps → fix in the matching pass
- Modes 17-20: polish and release issues → fix in P2A/P5
