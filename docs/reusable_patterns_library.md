# Reusable Patterns Library

Proven patterns from ATC Math Tower, Grocery Dash, Bakery Rush, and Fire Dispatch.

Check here before inventing a new system.

---

## Patterns

### Zero-pressure tutorial
| Field | Value |
|---|---|
| **Solves** | Player confusion on first use |
| **Pass type** | P1 |
| **Best example** | Grocery Dash 4-step tutorial, Fire Dispatch 3-step tutorial |
| **How it works** | Guided steps before the timer starts. Each step teaches one mechanic. Timer begins only after tutorial is dismissed. |
| **Do not use when** | The mechanic is already obvious from the visual state alone |

### Missed-fact / mistake review
| Field | Value |
|---|---|
| **Solves** | Player finishes but learns nothing from the session |
| **Pass type** | P2A |
| **Best example** | ATC missed fact screen, Grocery Dash checkout receipt |
| **How it works** | End screen shows specific mistakes — which demands were hardest, which facts were missed, which errors repeated. |
| **Do not use when** | The session is too short to accumulate meaningful data |

### Status strip
| Field | Value |
|---|---|
| **Solves** | Game feels static, no arc to the session |
| **Pass type** | P3 |
| **Best example** | Bakery Rush bakery status, Fire Dispatch dispatch status |
| **How it works** | One-line contextual text that changes with session state: "Quiet morning" → "Rush hour!" → "Boss is watching" |
| **Do not use when** | The game already has strong environmental storytelling |

### Star ratings (★★★)
| Field | Value |
|---|---|
| **Solves** | No differentiation between passing and mastering |
| **Pass type** | P2A |
| **Best example** | Grocery Dash 3-star system |
| **How it works** | ★ = completed. ★★ = good run (few errors). ★★★ = perfect (zero errors). Based on misses + overshoots, not just score. |
| **Do not use when** | The game has no meaningful quality gradient between pass and perfect |

### Streak bonus
| Field | Value |
|---|---|
| **Solves** | No reward for sustained focus |
| **Pass type** | P2A |
| **Best example** | ATC streak scaling (3-correct at L1, 6-correct at L21) |
| **How it works** | Consecutive correct actions earn a multiplier or bonus. Resets on error. Scales with difficulty level for hidden depth. |
| **Do not use when** | The game's core loop is too slow to create meaningful streaks |

### Tiered celebration
| Field | Value |
|---|---|
| **Solves** | Success feels flat — easy and hard wins identical |
| **Pass type** | P3 |
| **Best example** | Bakery Rush ✅→🎯→🎉→💎 progression |
| **How it works** | Easy success = quick flash. Medium = "Nice!" Medium-long. Hard = "Incredible!" Long celebration. Perfect hard = gold treatment. |
| **Do not use when** | Every action is equally difficult |

### Hardest-target debrief
| Field | Value |
|---|---|
| **Solves** | Debrief is generic, does not teach |
| **Pass type** | P2A |
| **Best example** | Fire Dispatch Mission Debrief, Bakery Rush Bakery Debrief |
| **How it works** | Track per-order/per-round outcome. At session end, show which specific demands/angles/targets caused the most errors. |
| **Do not use when** | Sessions are too short (< 5 rounds) to have a pattern |

### Customer / incident personality
| Field | Value |
|---|---|
| **Solves** | Game feels generic, orders are just numbers |
| **Pass type** | P3 |
| **Best example** | Bakery Rush customer templates, Fire Dispatch incident dispatch lines |
| **How it works** | Each order/incident gets a name, emoji, request line, success reaction, and failure reaction from a template pool. |
| **Do not use when** | The game's pacing is too fast for the player to read character text |

### Physical consequence
| Field | Value |
|---|---|
| **Solves** | Errors feel abstract — just a number changing |
| **Pass type** | P2B / P3 |
| **Best example** | Grocery Dash walk-of-shame, Bakery Rush patience drain + angry customer |
| **How it works** | Errors cost something the player can see and feel: time draining visibly, items returning, characters reacting, walking back. |
| **Do not use when** | The game needs errors to be cheap for learning (early P1) |

### Optimization above correctness
| Field | Value |
|---|---|
| **Solves** | Correct play has no depth — once you know the answer, it is trivial |
| **Pass type** | P4 |
| **Best example** | Grocery Dash pack size choice (minimize waste) |
| **How it works** | Beyond getting the right answer, there is a "better" answer. Two correct options, one is more efficient. |
| **Do not use when** | The core math skill is not yet solid — optimization confuses before correctness is comfortable |

### Teacher unlock code
| Field | Value |
|---|---|
| **Solves** | Teacher cannot differentiate or skip ahead |
| **Pass type** | P5 |
| **Best example** | ATC "LEVY", Grocery Dash "UNLOCK" |
| **How it works** | One code that unlocks all levels for teacher use. Not a settings panel — just a code. |
| **Do not use when** | The game has no level progression |

### Wrong-dispatch time penalty
| Field | Value |
|---|---|
| **Solves** | No consequence for careless attempts |
| **Pass type** | P2B |
| **Best example** | Fire Dispatch wrong-dispatch penalty (2-4s by level) |
| **How it works** | Attempting an incorrect action costs time, not just a score penalty. Progressive by level: zero at L1 (learning), significant at L5. |
| **Do not use when** | The game's core mechanic encourages experimentation (early P1) |

### Round shuffling within tiers
| Field | Value |
|---|---|
| **Solves** | Player memorizes sequence instead of learning the skill |
| **Pass type** | P4 / P2B |
| **Best example** | Unit Circle tier-shuffled rounds |
| **How it works** | Rounds within each difficulty tier are shuffled each session. Tier order stays fixed, content order varies. |
| **Do not use when** | The sequence is pedagogically important (each round builds on the previous) |
