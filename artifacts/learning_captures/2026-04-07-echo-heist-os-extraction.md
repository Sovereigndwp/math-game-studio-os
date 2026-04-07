# Echo Heist — OS Learning Extraction

| Field | Value |
|---|---|
| **Date** | 2026-04-07 |
| **Source** | Echo Heist (5-pass prototype, reference extraction only — not an active build lane) |
| **Purpose** | Extract what Echo Heist teaches the OS that Grocery Dash and ATC did not |
| **Classification** | Mixed — lessons classified individually below |

---

## Part 1 — Strongest Unique Lessons

### 1. Role-to-math fit

Echo Heist achieves the tightest role-to-math fusion in the portfolio for **procedural gating**. Math is not a resource to earn or a speed test to pass — it is literally the lockpick. Every door, terminal, vault lock, and escape gate requires solving a problem to physically progress. The stealth context justifies typed input naturally: you are cracking codes, not answering quiz questions.

**What makes this distinct:** Grocery Dash embeds math in a *decision chain* (recipe → multiply → divide → choose pack). ATC embeds math in a *dispatch cadence* (rapid-fire under time pressure). Echo Heist embeds math in *spatial gates* — the player cannot move forward without solving. This is a third embedding model the OS has not named.

**Lesson:** Gate-locked math (solve to proceed physically) is a distinct embedding model from chain math (Grocery Dash) and cadence math (ATC). The OS should name it.

### 2. Typed input integration

Echo Heist proves that typed input works at the 11–13 age band when three conditions are met:
1. **Equivalent form acceptance** — `1/2 = 0.5 = .5`, `30% = 0.3`, whitespace tolerance
2. **No format penalty** — the system evaluates mathematical correctness, not formatting
3. **Escalation path** — hints (H key), auto-hint after 2 wrong, scaffolding panel (F key)

Neither Grocery Dash nor ATC use typed input. Both use selection or button-press. Echo Heist is the first proof in the portfolio that typed recall (not recognition) works without frustrating the target age band, provided the equivalence engine and scaffolding are present.

**Lesson:** Typed input is viable for grades 5–8 when backed by an equivalence engine + escalating support (hint → auto-hint → scaffold panel). This is an OS-level input rule, not game-specific.

### 3. Class-based skill differentiation

Three classes (Hacker, Ghost, Runner) create meaningfully different play experiences through **math-gated abilities**:

| Class | Ability math | Buff | Tactical identity |
|---|---|---|---|
| Hacker | Percents / equations | +30% score on next 2 puzzles | Optimize scoring |
| Ghost | Fractions / angles | Reduce noise meter by solved amount | Avoid detection |
| Runner | Rates / integers | 3s sprint, zero noise | Escape pressure |

The critical design: each class's ability **requires solving a problem in its own math domain** to activate. The class choice is simultaneously a gameplay preference and a curriculum selection. A player who picks Ghost practices more fractions. A player who picks Runner practices more rate problems.

Neither Grocery Dash nor ATC have class systems. This is the first proof that class identity can double as curriculum routing without the player feeling "assigned" to a topic.

**Lesson:** Class-as-curriculum-router — when a class's unique ability requires domain-specific math, the player self-selects into additional practice without explicit assignment. This pattern is new to the OS.

### 4. Run structure and pacing

Echo Heist runs follow a 5-phase arc: **stealth → math gates → vault (committed, no escape) → escape chase → score**. Two structural innovations stand out:

**a) The vault commitment point.** Once the player reaches the loot, the vault popup cannot be cancelled with Esc. The player must solve 2–3 harder problems under a 90s timer or fail the mission. This creates the highest-stakes math moment in the portfolio — the "heist moment" where everything is on the line.

**b) The escape phase escalation.** After the vault cracks, guards speed up 1.6×, cones widen, a 60s countdown starts, and the alarm audio escalates (440Hz/480ms → 660Hz/280ms when <15s). One final math gate stands between the player and the exit. The math difficulty doesn't change — the context pressure does.

Grocery Dash has a consistent loop per level (shop → checkout). ATC has a consistent cadence (dispatch → dispatch → dispatch). Echo Heist has an **within-run arc** that builds to a climax. This is structurally new.

**Lesson:** Within-run arc (flat → committed high-stakes → escalating escape) is a pacing model the OS hasn't captured. It works for games where the run is 3–5 minutes and needs a dramatic shape.

### 5. Mission quota planning

30 missions across 3 districts with clear curriculum mapping:

| District | Missions | Focus | Difficulty knobs |
|---|---|---|---|
| Training Gallery | 1–10 | Integers, fractions, percents, rate-time | Baseline |
| Camera Commons | 11–20 | Two-step equations, percent change, angles, ratios | +20% guard speed, +30% heat gain, −10s escape |
| Escape Lines | 21–30 | Multi-step equations, EV, rate problems, rounding | +40% guard speed, +60% heat gain, −15s escape |

Difficulty scales through **environmental knobs** (guard speed, heat gain, escape time, hint cost) not through harder math exclusively. D3 math is harder than D1 math, but the environmental pressure also increases independently. This is a two-axis difficulty model.

Grocery Dash scales primarily through content complexity (more guests, more ingredients, pack variants, distractors). ATC scales through mechanic additions (more runways, more plane types). Echo Heist scales through both content and environment simultaneously.

**Lesson:** Two-axis difficulty (content complexity + environmental pressure) can be tuned independently. The DISTRICT_CONFIG pattern — a single configuration object driving all environmental knobs per stage — is a clean implementation worth reusing.

### 6. Scaffolding through score tradeoffs

Echo Heist implements a 4-tier support system, each with a clear cost:

| Tier | Trigger | Cost | What it gives |
|---|---|---|---|
| Focus mode (Tab) | Player choice | −2 pts/sec | Guards/cameras at 25% speed |
| Hint 1 (H) | Player choice | −50/−75/−100 by district | Category + approach |
| Hint 2 (H again) | Player choice | Same cost again | Setup / partial work |
| Auto-hint | 2 wrong answers | Free | Same as Hint 1 |
| Scaffold panel (F) | Player choice | Free | Visual reference (fraction bars, number line, rate triangle, etc.) |

The scaffold panel (Pass 4) is template-aware — it shows fraction bars for fraction problems, rate triangles for rate problems, angle arcs for angle problems. It gives conceptual support without giving the answer. This is a distinct tool from hints (which give procedural clues).

Neither Grocery Dash nor ATC have tiered scaffolding. Grocery Dash has the checkout receipt (post-attempt worked solution). ATC has no in-play support. Echo Heist proves that **graduated in-play support** (free conceptual reference → paid procedural hint → free auto-hint safety net) can coexist with a high-stakes feel.

**Lesson:** Template-aware scaffolding (visual reference matched to problem type) is a new pattern. Separating conceptual support (free, always available) from procedural hints (costs score) is a design principle worth capturing.

### 7. Progression across districts

Echo Heist's 3-district structure uses three progression mechanisms:

1. **Curriculum progression** — D1 teaches foundational skills, D2 combines them, D3 requires multi-step reasoning
2. **Environmental progression** — DISTRICT_CONFIG scales guard speed, heat gain, escape time, hint cost
3. **Meta progression** — Class unlocks at 5 and 10 completed missions, daily contract mode, mission select for targeted revisiting

The mission select screen (Pass 5) is particularly notable: a 5×6 grid showing completion status and personal bests per mission. This lets a player who struggles with angles go directly to angle-heavy missions without replaying the entire sequence.

**Lesson:** Mission select as targeted practice — letting the player navigate directly to weak-skill missions — is a meta-progression pattern worth capturing. It converts a linear sequence into a self-directed practice tool.

### 8. Content modularity

Echo Heist's content system uses three layers:

1. **Prompt objects** — each has `template`, `answer`, `hint1`, `hint2`, and maps to a skill tag (T1–T12)
2. **Mission data** — arrays of prompt objects with difficulty assignment, either hand-authored (D1, D3) or procedurally generated (D2)
3. **District config** — environmental knobs applied uniformly to all missions in a district

The prompt object is the atomic content unit. It carries its own scaffolding (hints) and its own curriculum tag (template). This means content can be authored, swapped, and tested independently of level layout or environmental difficulty.

D3's conversion from procedural to authored content (Pass 4) proved that authored prompts produce richer, more contextualized questions. The procedural system works for volume; authored content works for curriculum precision.

**Lesson:** The prompt-object-as-atom pattern (problem + answer + hints + curriculum tag) is a content structure worth standardizing. It enables independent authoring, template-aware scaffolding, per-skill tracking, and hot-swapping between procedural and authored content.

---

## Part 2 — Classified Lessons

| # | Lesson | Classification | Rationale |
|---|---|---|---|
| 1 | Gate-locked math is a distinct embedding model | **general OS rule** | Applies to any future game where math controls physical progression. Names a third embedding type alongside chain math and cadence math. |
| 2 | Typed input viable at grades 5–8 with equivalence engine + escalating support | **general OS rule** | Applies whenever typed input is considered for any game targeting ages 11+. Not game-specific. |
| 3 | Class-as-curriculum-router | **reusable pattern** | Applicable to any game with a class/role system where abilities can require domain-specific math. Needs a second proof case before becoming an OS rule. |
| 4 | Within-run arc (flat → committed → escalating escape) | **game-family rule** | Specific to games with 3–5 minute runs that need dramatic pacing. Defines a family of "heist-shaped" runs. |
| 5 | DISTRICT_CONFIG pattern (environmental difficulty knobs) | **reusable pattern** | Any game with stage-based progression can use a single config object to drive all environmental difficulty. |
| 6 | Two-axis difficulty (content + environment scaled independently) | **general OS rule** | Applies whenever a game has both content complexity and environmental pressure. Should be a design check in the orchestrator. |
| 7 | Template-aware scaffolding (visual reference matched to problem type) | **reusable pattern** | Any game using typed input with multiple math domains. Needs the prompt-object-as-atom pattern as a prerequisite. |
| 8 | Separating conceptual support (free) from procedural hints (costs score) | **general OS rule** | Whenever a game has an in-play help system, this separation should be the default architecture. |
| 9 | Auto-hint after N wrong answers (free, no penalty) | **general OS rule** | Frustration prevention. Applicable to every game with typed or constructed responses. The threshold (2 wrong) may vary by age band. |
| 10 | Vault commitment point (no-escape high-stakes math) | **game-family rule** | Specific to games with a climactic math moment. Defines the "committed gate" pattern for heist/boss-fight structures. |
| 11 | Escape phase escalation (context pressure increases, math difficulty stays constant) | **reusable pattern** | Any game with an endgame phase. Escalating environmental pressure without changing math difficulty is a clean way to raise stakes. |
| 12 | Mission select as targeted practice | **reusable pattern** | Any game with 10+ levels and skill tagging. Converts a linear game into a self-directed practice tool at meta-progression level. |
| 13 | Prompt-object-as-atom (problem + answer + hints + curriculum tag) | **general OS rule** | Content architecture standard. Should apply to every game that uses math prompts. |
| 14 | Authored vs procedural content tradeoff (precision vs volume) | **design check** | At P4, check whether procedural content should be replaced with authored content for curriculum-critical stages. |
| 15 | Mastery streaks with template-specific tracking | **reusable pattern** | Already partially captured (ATC streak bonus). Echo Heist adds per-template tracking, which is new — streaks are per-skill, not per-session. |
| 16 | Focus mode (slow-time at score cost) | **game-family rule** | Specific to games with real-time pressure during math solving. Not appropriate for turn-based or untimed games. |
| 17 | Class unlock gating by mission count | **reusable pattern** | Any game with classes or modes that should be earned. Simple threshold (5 missions, 10 missions) prevents overwhelm on first use. |
| 18 | Daily contract (date-seeded daily challenge) | **reusable pattern** | Already partially captured in ATC patterns. Echo Heist confirms it works client-side with no server. |

---

## Part 3 — Echo Heist vs Grocery Dash vs ATC

### What Echo Heist teaches better than either

| Lesson | Why Echo Heist is the stronger source |
|---|---|
| Gate-locked math embedding | Neither GD nor ATC use spatial gating. GD uses decision chains, ATC uses dispatch cadence. Echo Heist is the only proof of solve-to-proceed. |
| Typed input viability | GD and ATC use selection/buttons. Echo Heist is the only typed-input proof with equivalence engine and graduated support. |
| Class-as-curriculum-router | Neither GD nor ATC have class systems. This is entirely new. |
| Template-aware scaffolding | GD has post-attempt receipts. ATC has missed-fact review. Neither has in-play visual scaffolding matched to problem type. |
| Conceptual vs procedural support separation | Neither GD nor ATC distinguish between free conceptual reference and paid procedural hints. |
| Within-run dramatic arc | GD has consistent loops. ATC has consistent cadence. Neither has a multi-phase arc within a single run. |
| Multi-domain curriculum coverage | GD covers multiplication + division + optimization. ATC covers arithmetic operations. Echo Heist covers 12 template types across algebra, fractions, geometry, probability, and rates in a single game. |
| Prompt-object-as-atom content architecture | Neither GD nor ATC expose their content structure as cleanly as Echo Heist's tagged, hinted, scaffolded prompt objects. |

### What overlaps with existing references

| Lesson | Overlap with |
|---|---|
| Mastery streaks | ATC streak bonus (Echo Heist adds per-template tracking, but the core idea exists) |
| Daily contract / date-seeded challenge | ATC daily seed concept (Echo Heist confirms client-side viability) |
| Per-skill results breakdown | ATC missed-fact review + GD checkout receipt (Echo Heist combines both approaches) |
| localStorage persistence with version awareness | ATC version-keyed localStorage (Echo Heist uses it but doesn't improve the pattern) |
| Environmental difficulty scaling | GD progressive feature introduction + ATC adaptive difficulty (Echo Heist's DISTRICT_CONFIG is a cleaner implementation but the concept exists) |
| Score-based hints | Exists as a concept in GD star penalties. Echo Heist formalizes the cost structure more clearly. |
| Particle/shake feedback for correct/wrong | GD and ATC both have feedback. Echo Heist's implementation is not structurally new. |
| Mission select screen | GD has level select. ATC has level select. Echo Heist's version adds per-skill targeting but the basic pattern exists. |

### What is genuinely new to the OS

1. **Gate-locked math as embedding model** — third type alongside chain and cadence
2. **Typed input proof at grades 5–8** — first non-selection input validation
3. **Class-as-curriculum-router** — first proof that player identity choice drives practice distribution
4. **Template-aware scaffolding** — first in-play visual reference system matched to math domain
5. **Conceptual/procedural support separation** — first formalized free/paid support architecture
6. **Within-run dramatic arc** — first multi-phase run pacing model
7. **Prompt-object-as-atom** — first standardized content unit with embedded hints and curriculum tags
8. **Two-axis difficulty** — first explicit separation of content complexity from environmental pressure
9. **Vault commitment point** — first no-escape high-stakes math gate (the concept of "you cannot back out of this problem")
10. **Auto-hint as frustration safety net** — first proof that free automatic hints after N wrong don't undermine difficulty feel

---

## Part 4 — OS Incorporation Path

### Capture now (add to learning captures or pattern library)

These are proven by Echo Heist and ready to document:

| Lesson | Target location | Action |
|---|---|---|
| Prompt-object-as-atom | `docs/reusable_patterns_library.md` | Add as new pattern entry. This is a content architecture standard, not a game mechanic. |
| Auto-hint after N wrong (free) | `docs/reusable_patterns_library.md` | Add as new pattern entry. Threshold may vary; Echo Heist uses 2. |
| Template-aware scaffolding | `artifacts/learning_captures/` | Capture as reusable pattern awaiting second proof case. |
| DISTRICT_CONFIG (environmental knobs object) | `artifacts/learning_captures/` | Capture as reusable pattern. Clean implementation reference. |
| Escape phase escalation (raise context pressure, hold math difficulty) | `artifacts/learning_captures/` | Capture as reusable pattern. Applicable beyond heist games. |
| Mission select as targeted practice | `artifacts/learning_captures/` | Capture. Extends the existing level-select pattern with per-skill navigation. |

### Promote now (add to OS-level rules or docs)

These are strong enough to become OS rules immediately:

| Lesson | Target location | Action |
|---|---|---|
| Three math embedding models: chain, cadence, gate-locked | `docs/game_experience_spec.md` or a new `docs/math_embedding_models.md` | Name and define the three models. Future games should identify which model they use at P0. |
| Typed input rule (equivalence engine + escalating support required) | `docs/pass_rules.md` — add as a P1 rule for typed-input games | Any game proposing typed input must have equivalence acceptance and at least 2 tiers of support. |
| Conceptual support (free) vs procedural hints (costs score) | `docs/reusable_patterns_library.md` | Add as a new pattern. Frame as the default architecture for any in-play help system. |
| Two-axis difficulty (content + environment) | `docs/pass_rules.md` — add as a P2B design check | At P2B, verify whether content difficulty and environmental difficulty are being scaled independently or conflated. |
| Authored vs procedural content check | `docs/pass_rules.md` — add as a P4 design check | At P4, evaluate whether curriculum-critical stages need authored content to replace procedural generation. |

### Hold until a second proof case appears

| Lesson | Why hold | What would trigger promotion |
|---|---|---|
| Class-as-curriculum-router | Only one example (Echo Heist). Powerful idea but could be game-specific. | A second game with class/role selection that routes to different math domains. |
| Within-run dramatic arc (flat → committed → escape) | Could be specific to the heist fantasy. Needs proof in another genre. | A second game with a multi-phase run that builds to a climactic math moment (e.g., a boss-fight structure, a rescue mission). |
| Vault commitment point (no-escape gate) | High-stakes and effective, but could cause frustration in younger age bands. | A second game proving no-escape math works at grades 3–5, or explicit teacher feedback validating it at 5–8. |
| Focus mode (slow-time at score cost) | Specific to real-time games with math popups during active gameplay. | A second real-time game that uses slow-time as a learner support tool. |
| Per-template mastery streaks | Extends ATC's streak pattern but the per-template tracking needs a second proof before formalizing. | A second game tracking streaks per skill category rather than per session. |

### Does Echo Heist suggest a new family worth naming later?

**Yes, tentatively.** Echo Heist suggests a "stealth-gate" or "infiltration" family characterized by:
- Gate-locked math embedding
- Multi-phase within-run arc
- Class-as-curriculum-router
- Typed input with equivalence
- 3+ districts with two-axis difficulty

However, naming a family requires two members. Echo Heist is a reference extraction, not an active build. If a second game emerges with gate-locked math, a within-run arc, and class-based routing, the family should be named then. Until that point, the individual patterns should live in the patterns library and learning captures, not in a family doc.

---

## Part 5 — Curriculum Relevance

### Echo Heist is best treated as: a structural reference with future curriculum architecture potential

**Not a single broad multi-skill game model.** Echo Heist covers 12 template types (T1–T12) across algebra, fractions, geometry, probability, and rates. This breadth is a strength for a reference extraction but would be a weakness for a production game — it tries to teach too many skills to be the best tool for any one of them. A production version would need to narrow to 3–4 related skills per district or risk being a general-purpose math quiz in a stealth costume.

**Not a structural reference only.** Echo Heist contributes too many genuinely new patterns (gate-locked math, typed input proof, class-as-curriculum-router, template-aware scaffolding, prompt-object-as-atom) to be filed as "reference only." These patterns will actively shape future game design.

**Best treatment: structural reference now, curriculum architecture source for middle school later.** Echo Heist's strongest curriculum contribution is demonstrating that a single game can serve grades 5–8 across multiple math domains when:
1. Districts map to curriculum progression (foundational → combined → multi-step)
2. Class selection provides soft curriculum routing
3. Template-aware scaffolding adapts support to math domain
4. Mission select enables self-directed practice by skill

This architecture — district-as-curriculum-stage, class-as-domain-router, mission-as-skill-target — is a plausible model for middle school math game design. But it needs a production proof (not just a prototype) and teacher validation before the OS should adopt it as a curriculum framework.

**Recommendation:** File Echo Heist as a structural reference. Capture its unique patterns now. Revisit its curriculum architecture model when the OS is ready to design for middle school (grades 5–8) as a distinct age band with its own design constraints.
