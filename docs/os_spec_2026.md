# Math Game Factory OS — 2026 Revision

Canonical reference for all OS design decisions from 2026 forward.
Supersedes the original 8-layer operating spec where the two conflict.

---

## 1. Operating Principle

The OS is built around this formula:

**Role + interaction + misconception detection + adaptive feedback + reflection + transfer**

Not this:

~~Role + interaction + pressure + points~~

**Reason.** Recent reviews on serious games, dynamic difficulty, and AI-supported
gamification show stronger learning outcomes when systems adapt to learner needs,
support self-regulated learning, and provide feedback that changes strategy rather
than merely increasing excitement. EEF continues to emphasize plan → monitor →
evaluate as high-value classroom moves. IES frames formative assessment around
gathering and using evidence during learning.

---

## 2. Non-Negotiable Design Rules

### Rule A — No Empty Gamification
Reject any feature that increases stimulation without improving conceptual clarity,
decision quality, retention, or transfer. Points, animations, sounds, streaks, and
badges are allowed only when they reinforce the learning signal — never as
compensation for a weak loop.

### Rule B — Every Loop Must Expose Thinking
If a learner can succeed mostly by guessing, speed-tapping, or memorizing surface
patterns, the loop is not ready. The Loop Purity Auditor gates this check.

### Rule C — Every Game Must Classify Error Types
Track not only right/wrong, but what kind of misunderstanding happened.

Required error categories:

| Category | Description |
|---|---|
| `procedure_slip` | Knows the rule, makes an execution error |
| `concept_confusion` | Wrong mental model of the underlying concept |
| `representation_mismatch` | Cannot connect the symbol/icon to its meaning |
| `impulsive_guess` | Acts before engaging the mathematical question |
| `rule_misunderstanding` | Misinterprets the game's constraint or mechanic |
| `strategic_overload` | Correct on isolated tasks; loses track under combined pressure |

### Rule D — Every Level Needs One Reflection Beat
After a meaningful chunk of play, the learner answers one short prompt.

Examples by type:
- **Planning:** "What will you look for first this level?"
- **Monitoring:** "What kept going wrong?"
- **Evaluation:** "What changed when you slowed down?"
- **Representation:** "Which way of seeing it helped most?"

This follows the planning → monitoring → evaluation pattern in metacognition guidance.
The Reflection Prompt Bank (see Section 4) provides age-appropriate prompts by
interaction family.

### Rule E — Training Mode Teaches What to Notice
Onboarding must not only teach controls. It must teach the lens of the concept —
what features matter, what to ignore, what to predict, and what to compare.

### Rule F — Review Mode Must Isolate the Weak Idea
A good retry is not the same level again. It is a cleaner version of the exact
misunderstanding. The Misconception Library (see Section 4) defines clean replay
tasks for every error category in every game.

### Rule G — Every Family Must Declare a Transfer Target
Each game must state what later topic, representation, or context it is preparing
the learner for. This is stored in `transfer_target` on the prototype spec.

### Rule H — Teacher Visibility Is Required
If a teacher cannot quickly see where students are confused, the game is not
classroom ready. The Teacher Evidence Dashboard spec (see Section 4) defines
what must be visible and how fast a teacher should be able to interpret it.

---

## 3. Nine Required Layers

The OS previously required 8 layers. A ninth is now required.

| # | Layer | What it defines |
|---|---|---|
| 1 | Role | Who the player is, why this role needs this math |
| 2 | World | The world the role operates in |
| 3 | Math | The specific concept, its representation, its difficulty axis |
| 4 | Interaction | What the player does; what action performs the math |
| 5 | Pressure | Fair urgency; pacing; time/choice/social pressure |
| 6 | Feedback | What the game returns after each action |
| 7 | Transfer | Where this learning goes next |
| 8 | Reflection | The structured pause that builds metacognition |
| **9** | **Thinking** | **What the learner must notice, predict, monitor, and revise** |

### Layer 9 — Thinking

This is the missing bridge between a good game loop and a good learning loop.

For every game, define explicitly:

- **What to notice.** Which features of the presented problem are mathematically relevant?
  What should the learner look at before acting?
- **What to predict.** Before selecting, what should the learner mentally compute or
  estimate? What does the game ask them to anticipate?
- **What to monitor.** During action, what running state must the learner track?
  What changes as they act?
- **What to revise.** After feedback, what belief or strategy should change?
  What is the cleaner version of their attempt?

This layer is stored as `thinking_layer` in the prototype spec schema.

---

## 4. Required OS Tools

### 4.1 Misconception Library

A shared catalog by concept and age band.
Location: `artifacts/misconception_library/`
Schema: `artifacts/schemas/misconception_library_entry.schema.json`

For each game, the library contains entries covering all six required error categories.
Each entry includes:
- Common error description
- Likely cause
- How it appears in play (observable signals)
- Detection trigger (what the game can measure)
- Best feedback response
- Best clean replay task
- One reflection prompt

### 4.2 Reflection Prompt Bank

Short prompts sorted by interaction type.

| Interaction family | Prompt focus |
|---|---|
| `route_and_dispatch` | Rule detection and categorization |
| `allocate_and_balance` | Fairness, equivalence, constraint logic |
| `transform_and_manipulate` | Change and effect tracking |
| `navigate_and_position` | Spatial reasoning and reference systems |
| `combine_and_build` | Composition and decomposition |
| `sequence_and_predict` | Pattern and prediction |

### 4.3 Difficulty and Adaptation Matrix

Every game must define both challenge levers and adaptation levers as distinct
columns — not as a single difficulty scale.

**Challenge levers** (what makes the game harder):
- Pace
- Item count
- Rule count
- Representation shift
- Planning horizon
- Competing demands
- Symbolic complexity

**Adaptation levers** (what the game does when the learner is confused):
- Hint timing
- Misconception-specific replay
- Simplified representation
- Slower pressure
- Alternate explanation mode
- Guided comparison mode

Stored in `difficulty_and_adaptation_levers` on the prototype spec.

### 4.4 Signature Moment Library

A catalog of payoff moments tied to understanding, not just success.

Good signature moments feel different from generic win feedback. Examples:
- The route network clears because the learner finally sorted by rule correctly
- The balance system stabilizes the moment an equation becomes equivalent
- The graph snaps into the predicted pattern after a correct transformation
- The bakery order total turns green the instant the player reaches the exact sum

Each game must name at least one signature moment in `core_loop_translation.signature_moment_delivery`.

### 4.5 Teacher Evidence Dashboard Spec

For every game, define what a teacher can see and how fast they can interpret it.
Schema: `artifacts/schemas/teacher_evidence_dashboard.schema.json`

Required outputs:
- Misconception frequencies by category
- Stuck points by level
- Students likely guessing (impulsive_guess signals)
- Students who improved after feedback
- Representation types causing the most confusion

This aligns with IES framing: formative assessment is about gathering and using
evidence during learning, not only at the end.

### 4.6 Prototype Observation Kit

OS-level method for playtesting. Not a one-off practice.

Protocol:
1. **Silent observation first.** Do not explain or coach during play.
2. **Note confusion before explanation.** Write what you see before asking why.
3. **Categorize each confusion event** using the six error categories from Rule C.
4. **Distinguish four event types:** bug / balance / confusion / fun.
5. **Record what changed after feedback** — not just whether it worked.

---

## 5. Skill Architecture

Every game must train both math skills and learning skills explicitly.

### Math Skills
Concept-specific. Defined in `target_player.target_skills`.

### Learning Skills (now required)
All games must train at least three of the following:

| Skill | What it means in practice |
|---|---|
| Pattern notice | Identifying which features of a problem are mathematically relevant |
| Error diagnosis | Naming what went wrong and why |
| Strategy selection | Choosing between approaches before acting |
| Representation switching | Using a different form of the same concept |
| Planning under pressure | Deciding before the clock forces a guess |
| Self-monitoring | Tracking your own running state during a round |
| Revision after feedback | Changing strategy based on what the game returned |
| Transfer to new context | Applying the same idea in a different setting |

Stored in `target_player.learning_skills`.

---

## 6. Agent Roster

New agents for the 2026 OS. These are defined here as interface contracts —
implementation follows the priority build order in Section 11.

| Agent | Purpose | Primary output |
|---|---|---|
| Evidence Scout | Find current research, standards, and resources for target concept and age band | Evidence brief (EEF, IES, ISTE, platform docs) |
| Role-to-Math Auditor | Reject themes where the role does not naturally require the math | Role strength score, authenticity risk, rewrite suggestions |
| Misconception Architect | Generate probable learner errors before build starts | Misconception catalog with detection signals |
| Loop Purity Auditor | Test whether the learner action IS the math | Purity score, fail conditions, warnings |
| Adaptation Designer | Define how the game responds to different confusion patterns | Adaptation map, hint triggers, review routing |
| Reflection Writer | Generate age-appropriate reflection prompts tied to play moments | Prompt set by interaction family |
| Teacher Value Translator | Turn game spec into classroom language | Teacher and parent value statements, standards notes |
| Prototype Test Director | Run silent playtest sessions and structure test notes | Structured observation notes by error category |
| Transfer Mapper | State where the same idea appears next and how the next game should echo it | Transfer map, echo design |
| Tool Router | Choose the best implementation environment for prototype and classroom use | Platform recommendation with rationale |

### Tool Router Routing Logic

| Tool | When to use |
|---|---|
| Bloxels | Lowest-friction creation and story-driven early prototyping |
| Code.org Sprite Lab | K–upper elementary; simple game logic |
| Code.org Game Lab | Middle school–early high school; systems and logic |
| Minecraft Education | Immersive collaborative systems; standards-aligned worlds |
| Roblox Education | Advanced immersive simulations; social systems; upper ladder |
| Games for Change | Educator PD and curriculum framing |

---

## 7. Schema Upgrades

The following fields are added to `prototype_spec.schema.json`.
All are optional for backward compatibility. All are expected for any game
designed after 2026-04-04.

### In `target_player`
- `learning_skills` — array of learning skills from Section 5

### New top-level block: `thinking_layer`
- `what_to_notice` — which problem features are mathematically relevant
- `what_to_predict` — what the learner should compute before acting
- `what_to_monitor` — what running state to track during action
- `what_to_revise` — what belief/strategy should change after feedback

### New top-level block: `learning_design`
- `misconception_detection_logic` — how the game detects error categories
- `error_category_map` — array of `{category, detection_signal, play_appearance}`
- `evidence_of_understanding_signals` — observable signals that the learner has the concept
- `guessing_risk_signals` — observable signals of impulsive behavior
- `reflection_prompt_plan` — `{planning_prompt, monitoring_prompt, evaluation_prompt}`

### New top-level block: `adaptation_design`
- `hint_trigger_logic` — what triggers a hint and what it shows
- `adaptation_trigger_logic` — what triggers difficulty reduction/representation shift
- `alternate_representation_mode` — description of the simpler representation available
- `misconception_specific_review_mode` — how review targets the detected error

### In `prototype_rules` or as new top-level: `difficulty_and_adaptation_levers`
- `challenge_levers` — array of active challenge axes
- `adaptation_levers` — array of implemented adaptation responses

### New top-level fields
- `transfer_target` — what later topic/context this game prepares for
- `transfer_echo_design` — how the next game should echo this game's mechanic
- `teacher_dashboard_outputs` — array of what teachers can see

### New top-level block: `validation_targets`
- `misconception_capture_rate` — target % of error events classified by category
- `reduction_in_guessing_signals` — measurable reduction in impulsive behavior over session
- `quality_of_transfer_performance` — how performance on transfer task is measured
- `teacher_interpretation_speed` — time limit for a teacher to find a stuck student
- `revision_after_feedback_rate` — % of feedback events that produce strategy change

---

## 8. Stage Workflow

10 stages. Stages 1–8 overlap with the existing pipeline. Stages 9–10 are new.

| Stage | Name | Key output |
|---|---|---|
| 1 | Opportunity selection | Age band, concept, role fantasy, emotional hook, transfer target |
| 2 | Role-to-math audit | Role justification, world action, failure language, primary misunderstanding |
| 3 | Misconception mapping | Top 5 probable errors, play appearance, feedback per error |
| 4 | Core loop design | What appears → noticed → solved → action → world change → evidence captured |
| 5 | Reflection design | One planning prompt, one monitoring prompt, one evaluation prompt |
| 6 | Adaptation design | Hint rules, alternate representation rules, misconception review loops, pace adjustments |
| 7 | Interface design | Cognitive load limits, reading load, teacher evidence visibility, cue clarity for age |
| 8 | Prototype build | Simplest version that exposes thinking, captures misconception types, adapts once, produces one reflection beat |
| 9 | Silent playtest | Confusion points, guess behavior, reflection quality, adaptation effectiveness, teacher interpretability |
| 10 | Release package | Game + teacher guide + parent summary + standards note + misconception map + evidence dashboard + printable review tasks |

---

## 9. Tool Strategy for 2026

### Prototype Lane
- Bloxels → fast narrative and mechanic sketches with low friction
- Sprite Lab → early game logic, elementary builds
- Game Lab → systems and logic growth

### Classroom Immersion Lane
- Minecraft Education → concept benefits from worlds, collaboration, simulation,
  and standards-aligned lesson support

### Advanced Simulation Lane
- Roblox Education → deeper immersive systems, older learners, more complex
  world-based learning (chemistry, physics, robotics, etc.)

### Educator Adoption Lane
- Games for Change → educator PD, teacher onboarding, structured use of GBL in
  real school settings

### Standards and Planning Lane
- ISTE → agency, design, creative communication, empowered learner framing

---

## 10. Approval Gates

A game is not ready unless all ten answers are YES.

| # | Gate question |
|---|---|
| 1 | Does the role naturally need the math? |
| 2 | Does the player action perform the math? |
| 3 | Can the game detect at least three meaningful misconception types? |
| 4 | Does the game adapt to at least one of them? |
| 5 | Is there at least one short reflection beat? |
| 6 | Is there a named transfer target? |
| 7 | Can a teacher see useful evidence quickly? |
| 8 | Can the learner improve through a cleaner replay? |
| 9 | Does the simplest version still work? |
| 10 | Is the excitement serving understanding rather than hiding weak learning design? |

---

## 11. Priority Build Order

Follow this order. Do not expand platform integrations or polish layers until
items 1–5 are complete.

1. **Misconception Library** for the first three game families (Bakery Rush, Fire Dispatch, Unit Circle)
2. **Loop Purity Auditor** (`utils/loop_purity_auditor.py`)
3. **Misconception Architect** (agent stub + prompt)
4. **Schema upgrades** — add new fields to `prototype_spec.schema.json`
5. **Teacher Evidence Dashboard spec** — `artifacts/schemas/teacher_evidence_dashboard.schema.json`
6. Platform integrations and polish layers (deferred)

---

## 12. Core Takeaway

The best 2026 move is not to chase what looks most futuristic. It is to make the OS
more honest, more diagnostic, and more adaptive.

The official ecosystems most useful right now reward creation, project-based learning,
standards alignment, and educator usability. The strongest research signal still points
to metacognition, formative evidence, and targeted adaptation as the difference between
a fun activity and a real learning system.

---

## 13. Source Grounding

This operating document was informed by the existing Math Game Factory source of truth
plus current official educator resources and recent peer-reviewed work on metacognition,
formative assessment, serious games, dynamic difficulty adjustment, and AI-supported gamification.

| Source | What it grounds |
|---|---|
| EEF Metacognition and Self-Regulated Learning guidance | Rule D (reflection beats), Layer 9 (Thinking), plan/monitor/evaluate framing |
| IES Formative Assessment and Elementary Achievement review | Rule H (teacher visibility), Section 4.5 (Teacher Evidence Dashboard), "gather and use evidence during learning" |
| Frontiers in Education 2025 — systematic review of serious games in STEM | Operating principle shift; outcomes from adaptive vs. reward-only systems |
| MDPI Information 2026 — DDA in serious games review | Section 4.3 (Difficulty and Adaptation Matrix); adaptation as distinct design layer |
| Frontiers in Psychology 2026 — AI-driven gamification and metacognition | New skill architecture (Section 5); metacognitive learning skills as required |
| Games for Change educator resources | Section 9 tool strategy; educator adoption lane |
| Code.org Sprite Lab / Game Lab | Section 9 prototype lane routing |
| Minecraft Education lesson library | Section 9 classroom immersion lane |
| Roblox Education | Section 9 advanced simulation lane |
| Bloxels Education | Section 9 early prototyping lane |
| ISTE Standards for Students | Section 9 standards lane; agency, design, creative communication |

---

## 14. Reference Links

| Resource | URL |
|---|---|
| EEF Metacognition guidance | https://educationendowmentfoundation.org.uk/education-evidence/guidance-reports/metacognition |
| IES Formative Assessment review | https://ies.ed.gov/use-work/resource-library/report/descriptive-study/formative-assessment-and-elementary-school-student-academic-achievement-review-evidence |
| Games for Change educator resources | https://learn.gamesforchange.org/educator-resources |
| Code.org Sprite Lab | https://code.org/en-US/tools/sprite-lab |
| Code.org Game Lab | https://code.org/en-US/tools/game-lab |
| Minecraft Education lessons | https://education.minecraft.net/en-us/resources/explore-lessons |
| Minecraft Education for educators | https://education.minecraft.net/en-us/get-started/educators |
| Roblox Education | https://about.roblox.com/education |
| Roblox educational planning guide | https://create.roblox.com/docs/education/developer/planning-for-educational-settings |
| Bloxels Education | https://www.bloxels.com/education |
| ISTE Standards for Students | https://iste.org/standards/students |
| Frontiers 2025 — Serious Games in STEM | https://www.frontiersin.org/journals/education/articles/10.3389/feduc.2025.1432982/full |
| MDPI 2026 — Dynamic Difficulty Adjustment | https://www.mdpi.com/2078-2489/17/1/96 |
| Frontiers 2026 — AI Gamification & Metacognition | https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2026.1692949/full |
