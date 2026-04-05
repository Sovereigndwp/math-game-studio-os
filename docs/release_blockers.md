# Release Blockers

Hard gate list. If any of these are true, the game cannot ship.

Use before P5 or release decision.

---

## Blockers

| # | Blocker | How to check |
|---|---|---|
| 1 | **Player cannot explain the goal quickly** | Ask someone new to play for 30 seconds. Can they tell you what they are trying to do? |
| 2 | **No useful end-of-session feedback** | Play a full session. Does the end screen tell you something you did not already know? |
| 3 | **Progression wall** | Play L1 through L3. Is there a level where you fail for reasons unrelated to the math? |
| 4 | **Replay has no reason** | Finish one run. Do you have a specific reason to play again? (Not "it was fun" — a concrete target.) |
| 5 | **Pressure tests the wrong skill** | At the hardest level, are you failing because of the math or because of mouse speed / reading speed / motor precision? |
| 6 | **Game still feels like a tool** | Show it to someone for 10 seconds without context. Do they say "that is a game" or "what app is that?" |
| 7 | **No teacher-friendly launch path** | Can a teacher share a link and have a student playing within 10 seconds? No install, no account, no config? |
| 8 | **Math is not the primary action** | Remove the theme. Is the player still doing math as their main action, or was the math a gate before the real activity? |
| 9 | **First-use experience is confusing** | Give it to someone who has never seen it. Do they understand what to do within 15 seconds? |
| 10 | **Failure is invisible or unrecoverable** | Make a deliberate mistake. Can you see what went wrong? Can you recover within the same round? |
| 11 | **Success and failure feel the same** | Complete an order perfectly, then badly. Does the game react differently? |
| 12 | **Game crashes or breaks on normal use** | Refresh mid-game. Press buttons during animations. Restart after game over. Does anything break? |

---

## How to use

### Before release
Run through all 12. Any "yes" = blocked.

### During P5
Use this as the P5 checklist. Each blocker that is resolved gets checked off.

### After a major pass
Quick scan: did the pass accidentally introduce a new blocker?

---

## Current Blocker Status

| Blocker | Bakery Rush | Fire Dispatch | Unit Circle |
|---|---|---|---|
| 1. Goal unclear | ✅ clear | ✅ clear | ✅ clear |
| 2. No end feedback | ✅ debrief | ✅ debrief | ✅ debrief |
| 3. Progression wall | ✅ smooth | ✅ smooth | ✅ smooth |
| 4. No replay reason | ⚠️ stars exist but no randomization | ⚠️ stars exist but limited variation | ⚠️ shuffled but limited pool |
| 5. Wrong skill tested | ✅ math is the bottleneck | ✅ math is the bottleneck | ✅ spatial reasoning is the skill |
| 6. Feels like a tool | ✅ personality pass done | ✅ incident personality done | ❌ still feels like a tool |
| 7. Teacher launch | ✅ single HTML | ✅ single HTML | ✅ single HTML |
| 8. Math not primary | ✅ addition is the action | ✅ subset-sum is the action | ✅ angle placement is the action |
| 9. First use confusing | ✅ tutorial exists | ✅ tutorial exists | ✅ tutorial exists |
| 10. Invisible failure | ✅ patience drain + customer reaction | ✅ timer + lives | ✅ timer + lives |
| 11. Same feel for success/failure | ✅ tiered celebration | ✅ resolved lines | ⚠️ correct/miss feedback exists but flat |
| 12. Crashes on normal use | ⚠️ not formally tested | ⚠️ not formally tested | ⚠️ not formally tested |
