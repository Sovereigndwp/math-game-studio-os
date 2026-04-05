# Player Feeling Targets

## Purpose
Define what the player should feel at each pass type and during each phase of a run.

## Use this when
Before implementation — to set the target feeling. After playtest — to check if you hit it.

## Controls
- Every pass must name one target feeling before starting
- After playtest, complete the sentence: "Before this pass the player felt ___. After, they feel ___."
- If you cannot fill in both blanks, the pass is probably not done

## Do not use this for
- Deciding which pass type to do (use `pass_rules.md`)
- Diagnosing what is broken (use `engagement_failure_modes.md`)
- Level-specific tuning (use `level_role_map.md`)

---

## By Pass

| Pass | Target feeling | Proof question |
|---|---|---|
| P0 | "This could be a real game" | Does the concept excite or just explain? |
| P1 | "I get it" | Can the player explain the goal after 30 seconds? |
| P2A | "This run mattered" | Does the player know how they did and what to improve? |
| P2B | "This is hard but fair" | Does frustration come from challenge, not mismatch? |
| P3 | "This world is alive" | Does the player remember a moment, not just a score? |
| P4 | "I want another run" | Does the player start again voluntarily? |
| P5 | "This just works" | Can a teacher hand it to a student with no explanation? |

---

## Within a Run

| Phase | Target feeling | What creates it |
|---|---|---|
| **Start** | Oriented | Tutorial or clear first prompt. "I know what to do." |
| **First success** | Confident | Quick win on the first easy challenge. "I can do this." |
| **Mid-run** | Pressured | Timer tightening, demands increasing, stakes rising. "This is getting real." |
| **Mistake** | Warned | Visible consequence — patience drain, life lost, character reaction. "That cost me something." |
| **Recovery** | Relieved | Able to fix or continue after a mistake. "I can come back from that." |
| **Near miss** | Tense | Close to the goal, almost there. "One more step..." |
| **Hard success** | Proud | Big celebration for a difficult achievement. "I earned that." |
| **Easy success** | Satisfied | Quick confirmation, no fanfare. "Good, next." |
| **Streak** | Powerful | Sustained focus rewarded. "I'm on fire." |
| **Cascade failure** | Urgent | Multiple mistakes compound. "I need to focus NOW." |
| **End of run** | Reflective | Debrief shows what happened and what to improve. "I see what went wrong." |
| **Replay decision** | Motivated | Star to beat, mistake to fix, score to improve. "One more run." |

---

## Anti-feelings (what the player should NOT feel)

| Anti-feeling | What causes it | Which pass fixes it |
|---|---|---|
| Confused | No tutorial, unclear goal, too many simultaneous demands | P1 |
| Bored | No stakes, no variation, no personality, too easy | P2B, P3, P4 |
| Cheated | Speed kills before thinking can happen, unfair spike | P2B |
| Indifferent | No payoff, no debrief, passing and failing feel the same | P2A |
| Annoyed | Setup friction, restart bugs, controls fight the player | P5 |
| Patronized | Feedback is generic ("Good job!"), challenge is trivially easy | P2A, P2B |

---

## How to use this

### Before a pass
Pick the target feeling from the table. Write it down. That is your success criterion.

### During implementation
Ask: does this change move the player toward the target feeling?

### After playtest
Ask: did the player actually feel the target? If not, the pass needs more work or a different approach.

### The meta-test
After every pass, you should be able to complete this sentence:

> "Before this pass, the player felt ___. After this pass, the player feels ___."

If you cannot fill in both blanks, the pass is probably not done.
