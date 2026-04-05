# Repository Systems Audit

Full audit before scaling. April 2026.

---

## 1. Areas Inspected

- 21 docs files (3,900+ lines total)
- 14 agent directories
- 3 game preview directories + 1 Vite source directory
- 20 schema files
- 3 scripts
- Pipeline, orchestrator, engine, utils
- Artifact lifecycle (schemas → agents → jobs → library → pending → backups)
- Worktree vs main repo divergence
- Pass records and game feel artifacts

---

## 2. Current Source of Truth Map

### Game prototypes — WHERE IS THE REAL CODE?

| Game | True source | Standalone HTML | Stale files |
|---|---|---|---|
| **Bakery Rush** | `preview/src/BakeryRushPrototype.jsx` (1167 lines, Vite) | `previews/bakery/pass-1.html` (built from source) | `preview/src/BakeryGame.jsx` (322 lines, old v2), `preview/src/BakeryGame.css`, `previews/bakery/pass-2.html` (still tracked in worktree) |
| **Fire Dispatch** | `previews/fire/pass-1.html` (self-contained) | Same file | None |
| **Unit Circle** | `previews/unitcircle/pass-1.html` (self-contained) | Same file | None |

**PROBLEM:** Bakery Rush has a split source-of-truth. The real code is JSX that requires a Vite build step. Fire Dispatch and Unit Circle are self-contained HTML. This means Bakery Rush requires `node` + `npm run dev` to develop but needs a manual build-and-copy process to update the standalone HTML. This process has already caused confusion ("I see the old previews").

### Design docs — WHERE ARE THE RULES?

| Question | Primary doc | Overlap docs | Conflict risk |
|---|---|---|---|
| What pass am I in? | `pass_system.md` | `pass_rules.md` (duplicate diagnostic table, naming convention, game status) | **HIGH** — both files define the same passes with different levels of detail |
| What are the engagement rules? | `os_engagement_rules.md` | `game_engagement_playbook.md` (nearly identical sections) | **HIGH** — both have "what makes games sticky", urgency patterns, onboarding patterns, platform rules, release checklists |
| What patterns exist? | `reusable_patterns_library.md` | `game_engagement_playbook.md` (overlapping pattern descriptions) | **MEDIUM** — playbook has narrative, library has structured tables |
| What did audits teach? | `atc_math_tower_audit.md`, `grocery_dash_audit.md` | `game_engagement_playbook.md` (derived from same audits) | **LOW** — audits are source, playbook is derived |

### Pipeline artifacts — WHAT IS ACTUALLY USED?

| Category | Used in practice | Defined but never produced |
|---|---|---|
| **Active** | `misconception_map`, `pass_record`, `game_feel_pass`, `misconception_library_entry` | |
| **Pipeline-only** (run via benchmarks) | All 8 pipeline stage artifacts | All validated during benchmark runs but not during game improvement work |
| **Never produced** | | `gate_decision`, `stage_ledger`, `teacher_evidence_dashboard`, `request_brief` — schemas exist, no artifact ever created |

---

## 3. Main Redundancies Found

### R1 — `pass_system.md` and `pass_rules.md` overlap heavily
Both define P0-P5 with labels, purposes, and diagnostic tables. `pass_rules.md` is the superset (442 lines vs 108). `pass_system.md` adds nothing that `pass_rules.md` doesn't already have.

**Recommendation:** Merge `pass_system.md` content into `pass_rules.md`. Delete `pass_system.md`.

### R2 — `os_engagement_rules.md` and `game_engagement_playbook.md` are near-duplicates
Both have: "what makes games sticky", urgency patterns, onboarding patterns, feedback patterns, progression patterns, platform rules, anti-patterns, release checklists. The playbook is 398 lines, the rules are 253. They were written at different times with slightly different framing but cover the same ground.

**Recommendation:** Keep `os_engagement_rules.md` as the authoritative reference (compact, structured). Archive `game_engagement_playbook.md` or merge unique content (Grocery Dash-specific patterns, "The Waste Shame" etc.) into the rules file.

### R3 — Bakery Rush has 3 redundant source files
- `BakeryRushPrototype.jsx` — the real source (1167 lines)
- `BakeryGame.jsx` — old v2, never loaded by App.jsx (322 lines)
- `BakeryGame.css` — CSS for the old v2

**Recommendation:** Delete `BakeryGame.jsx` and `BakeryGame.css`.

### R4 — `previews/bakery/pass-2.html` still tracked in worktree
Was supposed to be deleted but persists in the worktree branch.

**Recommendation:** Delete from worktree.

### R5 — Root-level stale files
`03_current_implementation_status.md` and `benchmark_run_01.md` are at the repo root. They appear to be early development artifacts that predate the current docs structure.

**Recommendation:** Move to `docs/archive/` or delete.

### R6 — 4 schemas defined but never used
`gate_decision`, `stage_ledger`, `teacher_evidence_dashboard`, `request_brief` have schemas but no agent produces them and no artifact has ever been created.

**Recommendation:** Keep for now (they define future pipeline artifacts) but mark as "not yet implemented" in a schema index.

---

## 4. Main Workflow Inefficiencies Found

### W1 — Bakery Rush build-and-copy process
Updating the playable Bakery Rush HTML requires:
1. Edit `preview/src/BakeryRushPrototype.jsx`
2. Copy it to `/Users/dalia/projects/Master-Gaming-App-and-OS/preview/src/`
3. Run `PATH="/opt/homebrew/bin:$PATH" npx vite build`
4. Python script to inline CSS+JS into single HTML
5. Copy result to `previews/bakery/pass-1.html`
6. Git add both JSX source and HTML build

This is 6 manual steps. Fire Dispatch and Unit Circle need zero build steps.

**Recommendation:** Either convert Bakery Rush to self-contained HTML (like the other games) or create a `scripts/build_bakery.sh` that does steps 2-5 in one command.

### W2 — Worktree vs main repo divergence
The worktree (`claude/great-franklin`) and main repo (`main`) have diverged. Work is being done in both places. The worktree has the misconception workflow code. Main has the latest game prototypes and docs. Files are copied manually between them.

**Recommendation:** Decide on one working location. Either abandon the worktree and work on main directly, or merge all worktree changes into main and delete the worktree.

### W3 — No pass record written for recent passes
Pass records exist for Bakery Rush P1-P3, Fire Dispatch P1, and Unit Circle P1. But all the P2A, P2B, P3 passes on all three games have no pass records. The `pass_fail_scorecard.md` has informal records but the `pass_records/` directory is stale.

**Recommendation:** Either write pass records for completed passes or decide that `pass_fail_scorecard.md` replaces individual pass record files.

### W4 — No game feel artifacts for Fire Dispatch or Unit Circle
Only Bakery Rush has a `game_feel/` artifact. The visual/motion agent was never run on the other two games.

**Recommendation:** Not a blocker — game feel artifacts should be produced on demand during P3, not required for every game.

### W5 — Pending write-backs are stale
Two pending files exist in `artifacts/misconception_library/pending/`. The Fire Dispatch one is marked "applied". The Bakery Rush one is "pending_review" from the stability check. These are leftover from workflow testing.

**Recommendation:** Clean up: delete or archive both pending files since the library has already been updated.

---

## 5. Tool / Skill / Agent Timing Recommendations

### When should each tool run?

| Tool/Agent | Trigger | Blocker (don't run before) | Should happen after |
|---|---|---|---|
| **Pipeline (stages 0-8)** | New game concept | Nothing — first thing for new games | Never runs during game improvement passes |
| **Misconception Architect** | After P1 is complete for a game | P1 must be done (loop must be proven) | Pass record for P1 |
| **Visual/Motion Design Agent** | During P3 | P1 and P2A must be done | Playtest that identifies "feels dead" |
| **Mature game audit** | When a game is at P3+ or is a reference game | Game must have a playable prototype | Nothing — can run anytime on mature games |
| **Library write-back** | After misconception workflow produces revisions | Stability check should pass first | Misconception architect run with `--llm` |
| **Pass rules / scorecard** | Before and after every pass | Nothing — always applicable | Before implementation starts |
| **Engagement failure modes** | At start of any audit or when diagnosis is needed | Nothing | Playtest result or user complaint |
| **Level role map** | During P2B | P1 must be done | Before tuning difficulty |
| **Release blockers** | During P5 | P1-P3 should be done | Before shipping |

### What should NOT happen

- Do not run the visual/motion agent before P1 is complete
- Do not run misconception architect on a game that has no working prototype
- Do not apply library write-back without running the stability check
- Do not start P2B before checking the level role map
- Do not start P3 before P2A (motivation must exist before personality)
- Do not update docs during implementation passes — update after the pass is scored

---

## 6. Top Scalability Blockers

### S1 — Bakery Rush is the only game with a build step
Every new game should be self-contained HTML like Fire Dispatch and Unit Circle. The Vite/React/Tailwind stack for Bakery Rush creates a maintenance burden that doesn't exist for the other games.

### S2 — Docs have grown faster than consolidation
21 docs files totaling ~3,900 lines. Some overlap significantly (R1, R2). When scaling to 10+ games, maintainers will not know which doc to consult. `os_doc_usage.md` helps but the underlying duplication remains.

### S3 — No automated promotion path
A game improvement goes: edit HTML → playtest → commit → push. There is no automated check that the game still works (no browser test), no check that pass rules were followed, no check that a pass record was created. Everything depends on the human remembering the process.

### S4 — Worktree creates a split workspace
Two branches, two locations, manual file copying. This is fragile and has already caused confusion.

### S5 — Pass records are not enforced
The `pass_records/` directory has 5 records but 15+ passes have been completed. The scorecard partially covers this but the format is different. There is no gate that prevents starting a new pass without scoring the previous one.

---

## 7. Must Fix Before Scaling

| # | Problem | Why it matters | Smallest fix | Expected gain |
|---|---|---|---|---|
| **M1** | Worktree/main divergence | Manual file copying causes errors, confusion about which code is current | Merge worktree into main, delete worktree, work on main only | One source of truth for all files |
| **M2** | `pass_system.md` / `pass_rules.md` duplication | Two files define the same passes differently | Merge into `pass_rules.md`, delete `pass_system.md` | One pass reference instead of two |
| **M3** | `os_engagement_rules.md` / `game_engagement_playbook.md` duplication | Two files cover the same engagement patterns | Keep `os_engagement_rules.md`, archive playbook | One engagement reference instead of two |
| **M4** | Stale Bakery source files | `BakeryGame.jsx`, `BakeryGame.css`, `pass-2.html` confuse which code is real | Delete them | Clear source of truth for Bakery Rush |

## 8. Should Simplify Soon

| # | Problem | Why it matters | Smallest fix | Expected gain |
|---|---|---|---|---|
| **S1** | Bakery Rush build process (6 manual steps) | Slows iteration, causes stale HTML | Either convert to self-contained HTML or create a build script | One-step update |
| **S2** | Stale root files | `03_current_implementation_status.md`, `benchmark_run_01.md` at root look official but are outdated | Move to `docs/archive/` | Cleaner root |
| **S3** | Stale pending write-backs | Two pending files from testing clutter the library directory | Delete or archive | Clean artifact directory |
| **S4** | Missing pass records for completed passes | 10+ passes have no formal record | Either backfill or declare scorecard as the replacement | Complete history |
| **S5** | 4 unused schemas | `gate_decision`, `stage_ledger`, `teacher_evidence_dashboard`, `request_brief` never produced | Mark as "planned" in a schema index | Reduced confusion |

## 9. Nice Later

| # | Problem | Why it matters | Smallest fix | Expected gain |
|---|---|---|---|---|
| **N1** | No automated playtest check | Can't verify a game works without opening a browser | Puppeteer or Playwright smoke test | Automated regression |
| **N2** | No CI for game previews | Only misconception workflow has tests | Add HTML validation or smoke tests | Catch broken games |
| **N3** | No schema index document | 20 schemas with no overview of which are active vs planned | Create `docs/schema_index.md` | Faster orientation |
| **N4** | Game feel artifacts only for Bakery Rush | Fire Dispatch and Unit Circle have no formal visual pass artifact | Run visual agent during their P3 | Complete artifact set |

---

## 10. Suggested Order of Operations for Cleanup

1. **Merge worktree into main, delete worktree** (M1) — eliminates the biggest source of confusion
2. **Delete stale Bakery files** (M4) — `BakeryGame.jsx`, `BakeryGame.css`, `pass-2.html`
3. **Merge `pass_system.md` into `pass_rules.md`** (M2) — one pass reference
4. **Archive `game_engagement_playbook.md`** (M3) — keep `os_engagement_rules.md` as primary
5. **Move root stale files to archive** (S2) — `03_current_implementation_status.md`, `benchmark_run_01.md`
6. **Clean pending write-backs** (S3) — delete or archive stale pending files
7. **Create `scripts/build_bakery.sh`** (S1) — one-step build for Bakery Rush
8. **Decide on pass records vs scorecard** (S4) — pick one format, backfill or drop

After these 8 steps, the repo is clean enough to scale to new games without carrying confusion forward.
