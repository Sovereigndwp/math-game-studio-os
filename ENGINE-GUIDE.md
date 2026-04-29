# Train Your Brain Games — Engine Guide
## What exists, where it lives, and how to use it

> This document is the entry point for every collaborator, agent, and future version of you.
> Read this first. Everything else is referenced from here.

---

## Table of Contents
1. [What was built in this session](#what-was-built)
2. [Directory map](#directory-map)
3. [The pipeline](#the-pipeline)
4. [Shared skills (reusable code)](#shared-skills)
5. [Tooling (CLI commands)](#tooling)
6. [Agent roster](#agent-roster)
7. [Telemetry](#telemetry)
8. [Career matrix](#career-matrix)
9. [Monetization instruments](#monetization-instruments)
10. [Workflow integrations](#workflow-integrations)
11. [What to do next (prioritized)](#what-to-do-next)

---

## What was built

In this session the following were created from scratch:

| File | What it is |
|---|---|
| `skills/audio/tones.js` | Shared Web Audio module. Replaces copy-pasted audio in every game. |
| `skills/dom-panels/panel.js` | DOM info panel class. Accessible, real-time, themed. |
| `skills/dom-panels/panels.css` | Styles for DOM panels. |
| `skills/juice/juice.js` | Screen shake, particles, floating text, pulse rings, easing. |
| `telemetry/telemetry.js` | Lightweight event emitter. Sends data to Supabase. |
| `careers/career-matrix.json` | 12 careers with skills, grade ranges, CCSS hooks. |
| `agents/stage-1-5-standards-alignment.md` | New pipeline stage. Maps concepts to CCSS/NGSS. |
| `agents/stage-8-5-ai-playtester.md` | New pipeline stage. Simulates 3 player archetypes before build. |
| `agents/school-pitch-generator.md` | Produces teacher handout + admin pitch from concept packets. |
| `agents/grant-writer.md` | Translates pipeline artifacts into IES SBIR / NSF grant sections. |
| `tools/kill-test-cli.js` | Automated Stage 2 scoring. One command → verdict JSON. |
| `tools/portfolio-audit.js` | Coverage matrix. Shows grade × subject gaps. |
| `tools/lesson-inject.js` | Retrieves relevant past lessons for any pipeline stage. |
| `tools/concept-inbox-form-spec.md` | Form spec for community game idea intake. |
| `workflows/pipeline.yml` | Full 15-stage pipeline definition (13 original + 1.5 + 8.5). |
| `workflows/a11y-gate.yml` | GitHub Actions: axe-core accessibility check on every release. |

---

## Directory map

```
tyb-engine/
├── skills/
│   ├── audio/
│   │   └── tones.js              ← TYBAudio class
│   ├── dom-panels/
│   │   ├── panel.js              ← TYBPanel class
│   │   └── panels.css            ← Panel styles
│   └── juice/
│       └── juice.js              ← TYBJuice class + TYBEase
│
├── telemetry/
│   └── telemetry.js              ← TYBTelemetry class
│
├── careers/
│   └── career-matrix.json        ← 12 careers, skills, grade ranges
│
├── agents/
│   ├── stage-1-5-standards-alignment.md
│   ├── stage-8-5-ai-playtester.md
│   ├── school-pitch-generator.md
│   └── grant-writer.md
│
├── tools/
│   ├── kill-test-cli.js          ← node tools/kill-test-cli.js --concept <slug>
│   ├── portfolio-audit.js        ← node tools/portfolio-audit.js
│   ├── lesson-inject.js          ← node tools/lesson-inject.js --stage N --slug X
│   └── concept-inbox-form-spec.md
│
└── workflows/
    ├── pipeline.yml              ← Full 15-stage pipeline definition
    └── a11y-gate.yml             ← GitHub Actions a11y workflow
```

---

## The pipeline

The pipeline now has **15 stages** (was 13). Two stages were added:

```
Stage 0   concept-intake           Raw idea → concept-brief.json
Stage 1   learner-fit              Target learner, prerequisites
Stage 1.5 standards-alignment  ★  NEW: CCSS/NGSS mapping (required for schools)
Stage 2   kill-test               7-dimension automated scoring → PASS/REVISE/KILL
Stage 3   fantasy-integrity        Career wrapper must be load-bearing
Stage 4   interaction-mapper       Every click maps to a learning moment
Stage 5   core-loop               Action → feedback → progression defined
Stage 6   brilliant-audit          Interaction quality check
Stage 7   multisensory-spec        Audio + visual spec for every interaction
Stage 8   content-bank            Level/question bank built
Stage 8.5 ai-playtester       ★  NEW: 3 archetypes simulated before any code is written
Stage 9   ux-contract             DOM vs canvas decisions locked
Stage 10  build                   Game implemented using shared skills
Stage 11  feel-audit              20-point juice rubric
Stage 12  misconception-map        Every wrong answer tagged → telemetry schema
Stage 13  release                 Checklist + Itch.io + school pitch
Stage 14  live-ops (monthly)      Telemetry review + lesson capture + retro
```

★ = New stages added in this session

### Running a stage manually
```bash
# Stage 2 (kill test) — automated
ANTHROPIC_API_KEY=sk-... node tools/kill-test-cli.js --concept my-game-slug

# Dry run (no API call, checks file paths only)
node tools/kill-test-cli.js --concept my-game-slug --dry-run

# Inject relevant lessons before running any stage agent
node tools/lesson-inject.js --stage 8 --slug my-game-slug
# → Paste the output at the top of the agent's context window
```

---

## Shared skills

### TYBAudio — `skills/audio/tones.js`

Replaces the identical Web Audio code copy-pasted into echo-heist, orbital-drift, and future games.

```html
<script src="../../skills/audio/tones.js"></script>
<script>
  const audio = new TYBAudio();

  // Call on first user click (browser requirement)
  document.addEventListener('click', () => audio.init(), { once: true });

  // In your game logic:
  audio.sfxCorrect();      // right answer
  audio.sfxWrong();        // wrong answer
  audio.sfxSuccess();      // level complete
  audio.sfxAlert();        // warning
  audio.sfxStreak();       // combo / streak
  audio.sfxClick();        // UI button
  audio.startDrone();      // ambient background
  audio.stopDrone();       // stop ambient
  audio.setMuted(true);    // mute all
  audio.toggle();          // toggle mute, returns new state
</script>
```

### TYBPanel — `skills/dom-panels/panel.js` + `panels.css`

Persistent info panels next to canvas games. Accessible. Dark and light themes.

```html
<link rel="stylesheet" href="../../skills/dom-panels/panels.css">
<script src="../../skills/dom-panels/panel.js"></script>

<!-- Layout: flex container, canvas + panel side by side -->
<div style="display:flex">
  <canvas id="game"></canvas>
  <div id="sidebar"></div>
</div>

<script>
  const panel = new TYBPanel('#sidebar', { title: 'Mission', theme: 'dark' });

  // Key-value rows
  panel.setField('level',    'Taco Night');
  panel.setField('accuracy', '87%', { highlight: true });

  // Bulleted list
  panel.setList('objectives', ['Scale the recipe', 'Minimize waste'], { label: 'Goals' });

  // Progress bar
  panel.setProgress('mastery', 0.75, { label: '75% mastered' });

  // Feedback flash (fades out automatically)
  panel.flash('Correct! +10', 1800, 'success');
  panel.flash('Try again', 1800, 'error');
</script>
```

### TYBJuice — `skills/juice/juice.js`

Screen shake, particles, floating text, expanding rings. Call in your game loop.

```javascript
const juice = new TYBJuice(ctx, canvas);

// In your game loop:
juice.update();           // update all effects
juice.applyShake();       // ctx.save() + translate
  /* draw game here */
juice.restoreShake();     // ctx.restore()
juice.draw();             // draw particles, texts, rings

// Trigger effects:
juice.shake(8, 300);              // wrong answer shake
juice.burst(x, y, '#ff6b6b', 12); // hit/correct particle burst
juice.pulse(x, y, 60, '#00e5ff'); // expanding ring on correct
juice.popText(x, y, '+10', '#fff'); // floating score text
juice.trail(x, y, '#aaa');         // call each frame on moving objects

// Easing (standalone):
TYBEase.outBounce(t)   // t = 0..1
TYBEase.outElastic(t)
TYBEase.outBack(t)
TYBEase.inOutQuad(t)
```

---

## Tooling

### Kill Test CLI
```bash
# Run automated Stage 2 on any concept
ANTHROPIC_API_KEY=sk-... node tools/kill-test-cli.js --concept grocery-dash-2

# Output: .concepts/grocery-dash-2/kill-verdict.json
# Prints: color-coded verdict + per-dimension scores
```

**What it does:** Calls the Anthropic API with the kill-test agent prompt, scores the concept on 7 dimensions (0–3 each), returns PASS (≥14/21) / REVISE / KILL. Verdict saved to concept folder automatically.

### Portfolio Auditor
```bash
node tools/portfolio-audit.js

# Output: console coverage matrix + .governance/portfolio-audit-YYYY-MM.json
```

**What it does:** Reads all shipped games + in-flight concepts, builds a Grade Band × Subject coverage matrix, identifies empty cells (high-priority gaps), and outputs a ranked backlog of the 10 most impactful next game concepts.

**Run monthly** to steer concept selection.

### Lesson Injector
```bash
node tools/lesson-inject.js --stage 8 --slug grocery-dash-2 --top 3

# Output: formatted lesson block → pipe into agent context
```

**What it does:** Retrieves the most relevant past lessons from the lessons library for a given pipeline stage, ranked by tag overlap and priority. Prepend the output to any stage agent's context window so it doesn't rediscover known problems.

---

## Agent roster

### New agents (built this session)

**`agents/stage-1-5-standards-alignment.md`**
- Runs after Stage 1, before Stage 2
- Maps concept to CCSS Math, CCSS ELA, NGSS, CSTA standards
- Output: `standards-alignment.json` with strength scores 1–3
- Gate: minimum 2 primary standards (strength=3)
- Why it exists: school B2B sales require a standards alignment table

**`agents/stage-8-5-ai-playtester.md`**
- Runs after Stage 8, before Stage 9
- Simulates 3 player archetypes (struggling / on-grade / advanced) through every level
- Output: `playtest-report.json` with per-level pass rates and common wrong answers
- Gate: no level <20% Archetype A pass rate, no difficulty spike
- Why it exists: catches balance problems before any game code is written

**`agents/school-pitch-generator.md`**
- Trigger: `/school-pitch --slug [slug]`
- Reads: concept-brief + learner-fit + standards-alignment + feel-audit
- Output: `teacher-handout.md` + `admin-pitch.md` in `.reviews/[slug]/`
- Why it exists: every released game needs educator-facing documentation

**`agents/grant-writer.md`**
- Trigger: `/grant-write --rfp <file> --games <slug1,slug2>`
- Reads: RFP text + concept packets + lessons library
- Output: draft sections for IES SBIR / NSF SBIR applications
- Why it exists: IES SBIR Phase I = up to $200K for exactly what you're building

---

## Telemetry

### Setup (one-time, 30 minutes)
1. Create free account at [supabase.com](https://supabase.com)
2. Create new project
3. Open SQL Editor, run the SQL in `telemetry/telemetry.js` (top of file)
4. Copy your Project URL and anon key into `telemetry/telemetry.js`
5. Add `<script src="telemetry.js"></script>` to every game

### Using telemetry in a game
```javascript
const tel = new TYBTelemetry({
  gameSlug:   'echo-heist',
  gradeLevel: '6-8',  // CORRECTED 2026-04-29: math content (fractions of quantity, %, integer ops, EV, one/two-step equations) maps to CCSS 6.RP, 7.NS, 7.EE, 7.SP, 8.EE — middle school, not 9-12.
  career:     'cryptographer',
});

tel.start();   // call at game load

// On each answer:
tel.answer({ levelId: 'level-3', questionId: 'q7', answer: '42', correct: true, timeMs: 4200 });

// On level drop:
tel.drop({ levelId: 'level-3', reason: 'timeout' });

// On level complete:
tel.complete({ levelId: 'level-3', stars: 3, totalTimeMs: 45000 });

// On game end:
tel.end({ reason: 'game_over', totalScore: 1200 });
```

### What telemetry powers
- `/telemetry-review` command (post-launch): reads misconception patterns from live data
- Parent dashboard: accuracy by standard, time-on-task, recommended next game
- Grant efficacy claims: "players answered correctly X% of time on standard Y"
- Level redesign decisions: drop rate > 40% → level goes back to Stage 8

---

## Career matrix

**File:** `careers/career-matrix.json`

12 careers built out: marine biologist, emergency doctor, aerospace engineer, cryptographer, chef, architect, software engineer, wildlife biologist, airline pilot, forensic scientist, financial analyst, game designer.

Each career has:
- `grade_range` — min/max grade
- `subjects` — math/science/computer-science/etc
- `real_skills` — specific skills (taxonomy, fractions, spatial-reasoning...)
- `games` — array of game slugs (populate as games are built)
- `hook` — one concrete, surprising sentence for marketing copy
- `badge_color` — for parent dashboard UI

### Adding a new career
1. Add an entry to `careers/career-matrix.json`
2. Add the career to `agents/stage-1-5-standards-alignment.md` if it maps to a new subject
3. Run `/portfolio-audit` to see where the career fills coverage gaps

### After shipping a game
Update the `games` array in the career's entry:
```json
{ "slug": "cryptographer", ..., "games": ["echo-heist", "cipher-chase"] }
```

---

## Monetization instruments

### School pitch (per game)
Run after Stage 12 for every game:
```
/school-pitch --slug [slug]
```
Produces:
- `teacher-handout.md` — 1-page quick guide for classroom use
- `admin-pitch.md` — 3-slide budget justification for administrators

Convert to PDF using the existing pdf skill. Post on Itch.io as a download.

### Grant writing
Target: **IES SBIR Phase I** (up to $200,000)

Your strongest grant assets:
1. The lessons library = documented iterative research process
2. `standards-alignment.json` = formal curriculum alignment evidence
3. `misconception-map.json` = diagnostic assessment framework
4. `playtest-report.json` = pre-build efficacy projections
5. `telemetry/telemetry.js` = evaluation plan infrastructure (already built)

Run `/grant-write` with any IES SBIR RFP text to get draft sections.

### Concept inbox
Build the form from `tools/concept-inbox-form-spec.md` in Tally (free).
Place the link on your Itch.io page: "Have a game idea? Tell us!"
Teachers with specific misconceptions are your most valuable idea source.

### Pricing framework (to implement)
- **Free:** Single-mechanic, single-grade games on Itch.io (discovery layer)
- **Premium ($4.99–$9.99/month, families):** Multi-level games + progress tracking
- **School license ($4/student/year):** Premium + teacher dashboard + standards reports

The parent/teacher dashboard needs: Supabase (telemetry already wired) + a React frontend reading the `tyb_events` table and `career-matrix.json`.

---

## Workflow integrations

### GitHub Actions (automatic on push)
- **`workflows/a11y-gate.yml`** — runs axe-core on every `.games/*/release/*.html`
  - Place in `.github/workflows/a11y-gate.yml` in your repo
  - Fails push if accessibility violations found
  - Checks K–2 touch target sizes (48×48px minimum)

### Commands reference
| Command | What it does |
|---|---|
| `node tools/kill-test-cli.js --concept <slug>` | Automated Stage 2 kill test |
| `node tools/portfolio-audit.js` | Coverage matrix + backlog |
| `node tools/lesson-inject.js --stage N --slug X` | Retrieve relevant lessons |
| `/school-pitch --slug <slug>` | Generate teacher + admin docs |
| `/grant-write --rfp <file>` | Draft grant application sections |
| `/telemetry-review --slug <slug>` | Read live misconception data |
| `/lesson-capture --slug <slug>` | Write post-launch lessons to library |

---

## What to do next (prioritized)

### P0 — Do this week
1. **Wire telemetry into echo-heist and orbital-drift.**
   - Add `<script src="telemetry/telemetry.js"></script>`
   - Set `SUPABASE_URL` and `SUPABASE_ANON_KEY` (create free Supabase project first)
   - Add `tel.start()`, `tel.answer(...)`, `tel.complete(...)` calls
   - Without telemetry, all future efficacy claims are hypothetical

2. **Run portfolio auditor now.**
   ```bash
   node tools/portfolio-audit.js
   ```
   See your coverage gaps. Let this steer the next concept you pick.

3. **Build the concept inbox form.**
   - Use `tools/concept-inbox-form-spec.md` as your spec
   - Takes 30 minutes in Tally (free)
   - Add the link to your Itch.io page

### P1 — Do this month
4. **Run standards alignment on existing games (echo-heist, orbital-drift).**
   - Use `agents/stage-1-5-standards-alignment.md`
   - Produces `standards-alignment.json` for each game
   - Required before generating school pitch documents

5. **Generate school pitches for both existing games.**
   - Run `/school-pitch --slug echo-heist` and `/school-pitch --slug orbital-drift`
   - Upload teacher handouts as PDF downloads on Itch.io

6. **Add `a11y-gate.yml` to your GitHub repo.**
   - Copy `workflows/a11y-gate.yml` to `.github/workflows/`
   - Every future push to a release folder is automatically checked

### P2 — Do this quarter
7. **Refactor echo-heist and orbital-drift to use shared skills.**
   - Replace inline audio code with `TYBAudio` from `skills/audio/tones.js`
   - Replace canvas-based text panels (if any) with `TYBPanel`
   - Add `TYBJuice` for any game that lacks particle effects
   - This is not urgent but reduces future maintenance significantly

8. **Research IES SBIR next open solicitation.**
   - URL: `ies.ed.gov/sbir`
   - Use `agents/grant-writer.md` to draft sections
   - Your lessons library + misconception maps are your evidence base

9. **Build a minimal parent dashboard.**
   - Reads from Supabase `tyb_events` table (telemetry already wires to this)
   - Shows: games played this week, standards practiced, accuracy rate
   - This is your first paid product tier

---

## Security notes

No secrets are hardcoded in any file in this engine.

- `telemetry/telemetry.js` — `SUPABASE_URL` and `SUPABASE_ANON_KEY` are placeholder strings. Set them in the file or (better) inject via environment variables at build time.
- `tools/kill-test-cli.js` — reads `ANTHROPIC_API_KEY` from `process.env`, never from a file.
- The Supabase anon key is safe to expose in client-side code — it's a public key designed for browser use. Row Level Security (the SQL in telemetry.js) limits it to insert-only.
- No PII is collected by telemetry. Session IDs are random strings, not tied to accounts.

---

*Engine built: January 2025*
*Total files: 16*
*Coverage: skills, telemetry, careers, agents, tools, workflows, CI/CD*
