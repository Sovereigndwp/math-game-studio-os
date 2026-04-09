# Repository Systems Audit — 2026-04-09

A dated snapshot of the Math Game Studio OS repository state as of 2026-04-09, after the `previews/` → `reviews/` migration (Phases 1–5) and the post-migration cleanup sequence (Cleanup Steps 1–10) are complete in this cleanup sequence.

This document is **additive**. It does not edit, rename, replace, or modify the existing `docs/repo_systems_audit.md`, which remains preserved unchanged as the canonical pre-migration snapshot.

## What this audit is — and is not

This audit **is**:
- A point-in-time snapshot of the repo's directory layout, layer structure, per-game state, and outstanding work
- A reference document a new contributor can read to understand what the repo looks like right now
- A handoff artifact recording exactly what the post-migration cleanup sequence accomplished

This audit **is not**:
- A rewrite of the prior audit
- A policy document (those live in `docs/pipeline_policy.md`)
- A plan or roadmap (those live in concept folders, the Taskade live pipeline, and per-game pass records)
- A living document — it is dated and immutable. The next structural audit should be a new file at `docs/repo_systems_audit_<YYYY-MM-DD>.md`, not an edit of this one.
- A duplicate of `docs/pipeline_policy.md`, `docs/concept_lanes.md`, `memory/registries/family_registry.json`, or any other canonical reference. This audit references them by path; it does not restate their content.

## Scope

This audit covers the structural and organizational state of the repo. It does not audit:

- Working code correctness (covered by `tests/` and the V1 benchmark suite)
- Game design quality (covered by Era 2 design docs and per-game pass records)
- Per-game playtest results (covered by `artifacts/playtests/` and Taskade)
- Day-to-day operational state (covered by Taskade)

For the canonical rules that govern the repo, see [`docs/pipeline_policy.md`](pipeline_policy.md). For the active concept lane state, see [`docs/concept_lanes.md`](concept_lanes.md). For the structured family/game registry, see [`memory/registries/family_registry.json`](../memory/registries/family_registry.json). For the original pre-migration audit, see [`docs/repo_systems_audit.md`](repo_systems_audit.md) (intentionally unchanged).

---

## Top-level directory layout

The current top-level directories and their assigned era. Era assignments come from the three-era model in `docs/pipeline_policy.md` and the root `README.md` "Repository layers" section.

| Path | Era | Purpose |
|---|---|---|
| `agents/` | Era 1 | Per-stage agents for the Python concept pipeline |
| `artifacts/` | Era 1 + Era 2 | Schemas, misconception library, learning captures, pass records, playtests, design checks, jobs (gitignored), game feel records |
| `concepts/` | Era 3 | Approved concept packets (only `snack-line-shuffle/` exists today) |
| `docs/` | All eras | Policy docs (Era 3), design framework (Era 2), V1/V2 milestone docs (Era 1), this audit |
| `engine/` | Era 1 | Gate decision engine for the Python pipeline |
| `games/` | Era 3 | Release archive layer (empty by design — only README.md) |
| `memory/` | Era 1 + Era 3 | `job_workspaces/` (Era 1, gitignored) and `registries/` (Era 3) |
| `orchestrator/` | Era 1 | Live stage ledger and pipeline orchestration code |
| `orchestrator_v3/` | Era 2 | LangGraph orchestrator blueprint (not yet running) |
| `preview/` | Supporting tooling | Vite source for the bundled Bakery review build |
| `prompts/` | Era 2 | Design check prompt templates |
| `references/` | Era 2 | External reference game source HTML files |
| `reports/` | Era 1 | Benchmark markdown reports (gitignored) |
| `reviews/` | Era 3 | Active review builds, post-Phase-2 layout |
| `scripts/` | Era 1 | Benchmark runner, misconception architect runner, library write-back CLI |
| `tests/` | Era 1 | Pytest regression suite |
| `utils/` | Era 1 | Shared agent runner, LLM caller, validators |
| `.github/` | Era 3 | GitHub Actions workflows (only `promote-build.yml`) |
| `.claude/` | Tooling | Local Claude Code config (`launch.json`, `settings.local.json`, `worktrees/` gitignored) |
| `.venv/` | Tooling | Python 3.14 virtual environment (gitignored) |

## Three-era model

The repo contains three coexisting layers. None of them replaces another. Each has its own lifecycle, its own canonical entry doc, and its own authoritative directories.

| Era | Purpose | Canonical entry doc |
|---|---|---|
| **Era 1** — Python pipeline | Multi-agent concept evaluation pipeline (Stages 0–8), still working, still benchmarked | [`pipeline.py`](../pipeline.py) and [`README.md`](../README.md) "Pipeline" section |
| **Era 2** — OS design framework | The quality and design rulebook humans and agents consult before/during game work; also the orchestrator_v3 blueprint | [`docs/os_spec_2026.md`](os_spec_2026.md) |
| **Era 3** — Live review/release pipeline | Taskade-first live operating layer; GitHub as the review and release archive | [`docs/pipeline_policy.md`](pipeline_policy.md) |

## Era 1 — Python pipeline

**Status: live, mostly untouched by this session's migration and cleanup.**

### What's there

| Path | What it is |
|---|---|
| `pipeline.py` | Main entry point (~563 lines); runs Stages 0–8 in sequence |
| `agents/` | 14 agent directories. Pipeline-active: `intake_framing`, `kill_test`, `interaction_mapper`, `family_architect`, `core_loop`, `prototype_spec`, `prototype_build_spec`, `prototype_ui_spec`, `misconception_architect`. Era 1/2 extensions: `revision_brief`, `playtest_diagnostic_report`, `visual_motion_design`, `implementation_patch_plan`, `implementation_plan` |
| `engine/gate_engine.py` | Gate decision engine (pass/revise/reject per stage) |
| `orchestrator/` | Live stage ledger (`orchestrator.py`, `stage_ledger.py`, `__init__.py`). Now has a README.md (added in Cleanup Step 8) |
| `utils/` | 6 shared modules: `shared_agent_runner.py`, `llm_caller.py`, `validation.py`, `loop_purity_auditor.py`, `difficulty_ramp_auditor.py`, `solvability_checker.py` |
| `scripts/` | 3 CLIs: `run_benchmarks.py`, `run_misconception_architect.py`, `apply_library_writeback.py` |
| `tests/` | 3 test files: `test_difficulty_ramp_auditor.py`, `test_misconception_workflow.py`, `test_solvability_checker.py` |
| `artifacts/schemas/` | 20 JSON schemas for the artifact types each agent produces |
| `memory/job_workspaces/` | Per-job artifact storage (gitignored; ~176 historical job dirs on disk locally, 0 tracked) |
| `reports/` | Benchmark output (gitignored) |

### Status

- 5 benchmark cases passing in stub mode and LLM mode (per `README.md`)
- misconception workflow tests present and described in `README.md`
- This session added one new file (`orchestrator/README.md` in Cleanup Step 8) but did NOT modify any working Python code, YAML, or schema
- V1 frozen at tag `v1.0`; V2 boundary frozen and documented in `docs/v2_boundary_freeze.md`

### Reference

[`pipeline.py`](../pipeline.py) · [`README.md`](../README.md) Pipeline section · [`RUNBOOK.md`](../RUNBOOK.md) · [`docs/v1_handoff.md`](v1_handoff.md) · [`docs/v2_boundary.md`](v2_boundary.md) · [`docs/v2_boundary_freeze.md`](v2_boundary_freeze.md) · [`docs/benchmark_rubric.md`](benchmark_rubric.md) · [`docs/benchmark_review_v1.md`](benchmark_review_v1.md) · [`orchestrator/README.md`](../orchestrator/README.md)

---

## Era 2 — OS design framework

**Status: stable, mostly untouched by this session.**

### What's there

| Path | What it is |
|---|---|
| `docs/os_spec_2026.md` | Canonical design and quality rulebook (the "OS spec") |
| `docs/game_experience_spec.md` | Pre-build experience specification template |
| `docs/delight_gate.md` | Delight Gate evaluation rules |
| `docs/pass_rules.md`, `docs/pass_fail_scorecard.md` | Pass discipline rules and scoring |
| `docs/level_role_map.md`, `docs/player_feeling_targets.md` | Per-level and per-pass feeling targets |
| `docs/engagement_failure_modes.md` | Shared vocabulary for engagement failures |
| `docs/game_design_intelligence.md` | Reusable design constraints from the GameForge curriculum |
| `docs/learning_and_generalization.md` | Operating doc for extracting reusable patterns |
| `docs/os_engagement_rules.md` | Practical engagement reference derived from mature-game audits |
| `docs/reusable_patterns_library.md` | Proven patterns from ATC, Grocery Dash, Bakery, Fire Dispatch |
| `docs/portfolio_strategy.md` | Current portfolio sequencing rationale |
| `docs/release_blockers.md` | Hard gate list before release |
| `docs/pre_build_excellence_checklist.md` | Pre-build gut check |
| `docs/atc_math_tower_audit.md`, `docs/grocery_dash_audit.md` | External reference-game audits |
| `docs/concept_inputs/` | Concept seeds: `top_5_math_concepts_claude_packet.md`, `brain_games_concept_library_by_subject.md`, `claude_eval_prompt_top_5.md`, `Echo Heist Game Concept.md` (canonical, post Cleanup Step 2), `evaluations/`, `strategy/` (`family_map_math.md`, `prototype_sequence_math.md`) |
| `orchestrator_v3/` | Blueprint for the future LangGraph-based orchestrator. Contains `state.py`, `policies/` (`gates.yaml`, `interaction_types.yaml`, `misconception_taxonomy.yaml`), `prompts/agents/` (3 agent prompts), and `README.md` |
| `prompts/design_checks/` | 2 design check prompt templates |
| `references/` | External reference game HTML sources (ATC Math Tower, Grocery Dash) |
| `artifacts/learning_captures/` | 13 historical learning capture markdown files + a README. Intentionally not edited. |
| `artifacts/pass_records/` | 11 frozen JSON pass records across 3 games (bakery-rush ×4, fire-dispatch ×4, unit-circle ×3). Intentionally not edited. |
| `artifacts/playtests/` | Per-game playtest verification reports (bakery-rush ×1, fire-dispatch ×1; unit-circle dir empty) |
| `artifacts/design_checks/` | 6 power-grid and pre-build design check records |
| `artifacts/game_feel/` | 1 bakery-rush visual pass record |

### Status

- This session added two small clarifications to `orchestrator_v3/README.md`: a one-line cross-reference to the live orchestrator (Cleanup Step 8) and the "What is not here yet" section was expanded with two new bullets and a "Note on local directory state" paragraph (Cleanup Step 9)
- This session removed three empty subdirectories (`orchestrator_v3/memory/`, `orchestrator_v3/prompts/repair/`, `orchestrator_v3/prompts/system/`) from the local working tree. These were never tracked by git, so the removal is invisible to the diff but is documented in the parent README's new "Note on local directory state" paragraph
- All other Era 2 docs are unchanged from before this session

### Reference

[`docs/os_spec_2026.md`](os_spec_2026.md) · [`docs/orchestration_v3_blueprint.md`](orchestration_v3_blueprint.md) · [`orchestrator_v3/README.md`](../orchestrator_v3/README.md)

---

## Era 3 — Live review/release pipeline

**Status: structurally operational, no game shipped yet.** This is the largest section of this audit because Era 3 did not exist when the previous audit was written. Almost everything in this section is new since `docs/repo_systems_audit.md` was last edited.

### Pipeline policy

`docs/pipeline_policy.md` is the canonical Era 3 reference. It defines:

- The two-system model (Taskade = live pipeline; GitHub = review + release archive)
- The three repo layers and their distinct lifecycles (concepts, reviews, games)
- Branch and commit policy (forward-only history; direct-to-main only at ship-ready)
- SemVer rules (start at v0.1.0; no pre-release suffixes)
- Ship-ready gate definition
- End-to-end promotion flow
- Slug and version regex contract
- Tag format
- Migration phase plan (Phases 1–7)
- Glossary

This audit references `pipeline_policy.md` rather than restating it. If anything in this audit conflicts with `pipeline_policy.md`, `pipeline_policy.md` is authoritative.

### Concept source-of-truth layer

```
concepts/
  snack-line-shuffle/
    concept.md
    p1_definition_of_done.md
    misconception_notes.md
    approvals.md
    status.md
```

**Only one concept folder exists.** Snack Line Shuffle is the only game with a formal `concepts/<slug>/` packet. The other 6 games (bakery, counting, echo-heist, fire, power-grid, unitcircle) intentionally do **not** have concepts/ folders — backfilling them was explicitly skipped per the locked Cleanup Step 7 decision.

### Review build layer

```
reviews/
  README.md
  bakery/
    current/
      index.html
      pass-3.html
  counting/
    current/
      index.html
  echo-heist/
    current/
      index.html
      pass-1.html
      pass-1-record.md
      pass-2-record.md
      pass-3-record.md
      pass-4-record.md
      pass-5-record.md
      playtest.js
  fire/
    current/
      index.html
      pass-3.html
  power-grid/
    current/
      index.html
  snack-line-shuffle/
    README.md          ← slug-level placeholder; no current/ subdir
  unitcircle/
    current/
      index.html
      pass-3.html
```

**6 active review builds + 1 slug-level placeholder.** The Snack Line Shuffle slug is deliberately asymmetric — it has no `current/` subdirectory because no prototype has been implemented yet. The placeholder README documents why.

The previous-era `previews/` directory no longer exists. All game files were moved via `git mv` in Phase 2 (commit `a78825f`) with 100% rename detection on every file. `git log --follow` walks back through the rename for every game.

### Release archive layer

```
games/
  README.md
```

**Empty by design.** The `games/` directory contains exactly one file (`README.md`) and zero release subdirectories. No game has been shipped. The empty state is correct, not a missing-files situation.

The release archive is created and populated **only** by the `promote-build` workflow in response to a Taskade GREEN gate dispatch. No human creates files in `games/` by hand.

### Promote-build workflow

`.github/workflows/promote-build.yml` is the only GitHub Actions workflow in the repo. It is the only automated bridge between Taskade and the release archive. Its 10 steps:

1. Checkout main
2. Read payload
3. Validate payload (must be GREEN)
4. **Validate slug and version format** — added in Phase 5; uses regex `^[a-z0-9]+(-[a-z0-9]+)*$` for slug and `^[0-9]+\.[0-9]+\.[0-9]+$` for version
5. Validate review build exists
6. Validate release folder does not already exist
7. Promote review → release
8. Commit to main as `github-actions[bot]`
9. Tag release as `game/<slug>/v<version>` (annotated)
10. Push commit + tag

**Status:** the workflow is structurally complete; Phase 6 dry-run dispatch remains pending before operational confidence is claimed. Phase 7 (first real release) is also still pending. The workflow has not been triggered in production.

### Concept lane tracker

`docs/concept_lanes.md` is the documentation snapshot of active concepts. It contains:

- A "What a lane entry is — and is not" disclaimer
- A "Field conventions" section explaining the conservative field policy
- 7 active concept entries in alphabetical order: Bakery Rush, Echo Heist, Fire Dispatch, Power Grid Operator, Snack Line Shuffle, Unit Circle Pizza Lab, Watering Hole Count
- A "Lane schema" section listing minimum required fields per entry

The lane tracker is a periodic documentation snapshot, not the live source of truth. The live source of truth for concept lane state is **Taskade**. See `docs/pipeline_policy.md` two-system model for the rationale.

### Family registry

`memory/registries/family_registry.json` is the structured machine-readable record of family-and-game state. Before this session it was empty (`[]`). It now contains:

- **3 family objects:**
  - `Compare and Order` (real family; first proof case Snack Line Shuffle)
  - `Quantity and Fulfillment` (real family; first member Bakery Rush)
  - `Pending Formal Family Placement` (pseudo-family with `is_pseudo_family: true`; explicit `pseudo_family_note` saying it is not a real family)
- **7 member entries:** Snack Line Shuffle, Bakery Rush, Fire Dispatch, Unit Circle Pizza Lab, Watering Hole Count, Echo Heist, Power Grid Operator
- **Conservative field policy enforced:** `primary_standard` and `grade_band` are populated (with explicit values) only when a formal alignment packet exists in the repo. They are `null` for every entry except Snack Line Shuffle. `interaction_type` is populated at the member level only when the game is listed under `example_games` in `orchestrator_v3/policies/interaction_types.yaml` or declared in a concept packet. `release_state` is `"never_shipped"` on every entry.

### Reference

[`docs/pipeline_policy.md`](pipeline_policy.md) · [`docs/concept_lanes.md`](concept_lanes.md) · [`memory/registries/family_registry.json`](../memory/registries/family_registry.json) · [`.github/workflows/promote-build.yml`](../.github/workflows/promote-build.yml) · [`reviews/README.md`](../reviews/README.md) · [`games/README.md`](../games/README.md) · [`concepts/snack-line-shuffle/`](../concepts/snack-line-shuffle/)

---

## Per-game inventory (post-migration)

Snapshot of the 7 entries in `reviews/` as of 2026-04-09.

| Slug | Display title | Review path | Family (registry) | Interaction type | Pass records | Misconception library | Release state |
|---|---|---|---|---|---|---|---|
| `bakery` | Bakery Rush | `reviews/bakery/current/index.html` + `pass-3.html` | Quantity and Fulfillment (real) | `combine_and_build` | `artifacts/pass_records/bakery-rush-pass-{1,2,2a,3}.json` | [`bakery-rush-misconceptions.json`](../artifacts/misconception_library/bakery-rush-misconceptions.json) | `never_shipped` |
| `counting` | Watering Hole Count | `reviews/counting/current/index.html` | Pending Formal Family Placement (pseudo) | `pending_taxonomy_placement` | none | none | `never_shipped` |
| `echo-heist` | Echo Heist | `reviews/echo-heist/current/index.html` + `pass-1.html` + 5 in-place pass records + `playtest.js` | Pending Formal Family Placement (pseudo) | `pending_taxonomy_placement` | in-place at `reviews/echo-heist/current/pass-N-record.md` | none | `never_shipped` |
| `fire` | Fire Station Dispatch | `reviews/fire/current/index.html` + `pass-3.html` | Pending Formal Family Placement (pseudo) | `route_and_dispatch` | `artifacts/pass_records/fire-dispatch-pass-{1,2a,2b,3}.json` | [`fire-dispatch-misconceptions.json`](../artifacts/misconception_library/fire-dispatch-misconceptions.json) | `never_shipped` |
| `power-grid` | Power Grid Operator | `reviews/power-grid/current/index.html` | Pending Formal Family Placement (pseudo) | `pending_taxonomy_placement` | none | none | `never_shipped` |
| `snack-line-shuffle` | Snack Line Shuffle | **placeholder README only**, no `current/` subdir | Compare and Order (real) | `sequence_and_order` | n/a (concept only) | [`snack-line-shuffle-misconceptions.json`](../artifacts/misconception_library/snack-line-shuffle-misconceptions.json) (M4–M7 entries, enrichment still pending) | `never_shipped` |
| `unitcircle` | Unit Circle Pizza Lab | `reviews/unitcircle/current/index.html` + `pass-3.html` | Pending Formal Family Placement (pseudo) | `navigate_and_position` | `artifacts/pass_records/unit-circle-pass-{1,2a,2b}.json` | [`unit-circle-misconceptions.json`](../artifacts/misconception_library/unit-circle-misconceptions.json) | `never_shipped` |

For per-game lane status, validation blockquotes, and concept source notes, see [`docs/concept_lanes.md`](concept_lanes.md). This audit does not duplicate that content.

## Misconception library state

```
artifacts/misconception_library/
  bakery-rush-misconceptions.json
  fire-dispatch-misconceptions.json
  snack-line-shuffle-misconceptions.json
  unit-circle-misconceptions.json
  pending/
    archive/
      README.md
      bakery-rush-pass3-changed-stability-p1_20260405T140624Z.json
  backups/                            ← gitignored
```

### Tracked library files (4)

| File | Game | Notes |
|---|---|---|
| `bakery-rush-misconceptions.json` | Bakery Rush | 6 game-specific entries tagged to canonical categories |
| `fire-dispatch-misconceptions.json` | Fire Dispatch | populated |
| `unit-circle-misconceptions.json` | Unit Circle | populated |
| `snack-line-shuffle-misconceptions.json` | Snack Line Shuffle | M4–M7 linked to canonical categories, core fields populated, enrichment pending after P1 playtest data |

### Missing library files (3, locked as future content gap)

`power-grid`, `echo-heist`, `counting` have no `*-misconceptions.json` files. Per the locked Step 11 cleanup decision, these are tracked as a future gap and not backfilled in this session.

### Pending write-backs

- **0 active** pending write-backs in `pending/` (after Cleanup Step 6 archived the only one)
- **1 archived** at `pending/archive/bakery-rush-pass3-changed-stability-p1_20260405T140624Z.json` with a `README.md` explaining the archive policy. The archived file was never applied; its `status: pending_review` field is preserved byte-identical for honesty.

## Concept folders state

```
concepts/
  snack-line-shuffle/
    concept.md
    p1_definition_of_done.md
    misconception_notes.md
    approvals.md
    status.md
```

**1 concept folder exists, 6 are missing by design.** Per the locked Cleanup Step 7 decision, no concept folders are being backfilled for the existing 6 games (bakery, counting, echo-heist, fire, power-grid, unitcircle). They lived in the repo before formal concept folders were a thing, and inventing a retroactive concept packet for them would invent approval history.

## Gitignored vs tracked

The repo's `.gitignore` is short and explicit. Gitignored:

| Path | Reason |
|---|---|
| `.venv/`, `__pycache__/`, `*.py[cod]`, `*.pyo`, `*.egg-info/`, `dist/`, `build/` | Python artifacts |
| `.env`, `*.env` | Secrets |
| `.DS_Store` | macOS |
| `.idea/`, `.vscode/` | Editor |
| `memory/job_workspaces/` | Pipeline runtime artifacts (~176 dirs locally; 0 tracked) |
| `reports/` | Benchmark output |
| `.claude/worktrees/` | Claude Code session-local |
| `Master Gaming App and OS/` | Duplicate dir from spaces in path (macOS artifact) |
| `memory/**/*.INVALID_DEBUG.*.json` | Debug payloads from agent runner failures |
| `artifacts/jobs/` | Ephemeral per-run job snapshots |
| `artifacts/misconception_library/backups/` | Auto-backups from write-back applies |

Everything else under tracked directories is in git.

---

## What changed since the previous audit

The previous audit ([`docs/repo_systems_audit.md`](repo_systems_audit.md)) is intentionally preserved unchanged. It documents the pre-migration repo state and remains an accurate snapshot of that moment. **Do not edit it.** To compare states, read both files.

The high-level changes between the previous audit and this one:

1. **Era 3 layer added.** The entire concept-of-three-layers (concepts/reviews/games) did not exist when the previous audit was written. The previous audit's framing is single-system; this audit's framing is three-era.

2. **`previews/` → `reviews/<slug>/current/index.html` rename (Phase 2, commit `a78825f`).** The previous audit's references to `previews/bakery/current.html`, `previews/fire/`, etc., are now historical. The new path is `reviews/<slug>/current/index.html`. History is preserved via `git mv` rename detection.

3. **`games/` directory created (Phase 4, commit `12be815`).** Empty by design; only `README.md`. No release has been cut.

4. **Pipeline policy doc added (Phase 1, commit `6145c83`).** `docs/pipeline_policy.md` is the new canonical Era 3 reference.

5. **Promote-build workflow added (pre-migration infrastructure step, commit `9717e98`; regex validation Phase 5, commit `18c16db`).** `.github/workflows/promote-build.yml` is the only GitHub Actions workflow in the repo. It enforces the GREEN gate contract and the slug/version regex.

6. **Family registry populated (Cleanup Step 4, commit `f2d371f`).** Was empty `[]`. Now 3 family objects + 7 member entries with conservative field policy.

7. **Concept lanes tracker added (Phase 1, commit `6145c83`; populated Cleanup Step 5, commit `4990517`).** `docs/concept_lanes.md` did not exist before. Now has 7 alphabetically-sorted lane entries with validation status blockquotes.

8. **Snack Line Shuffle normalized into the repo (commit `490bb56`).** New `concepts/snack-line-shuffle/` folder with 5 files. Family registry and concept lanes both reference it.

9. **Echo Heist concept document de-duplicated (Cleanup Step 2, commit `de9437b`).** The duplicate at `reviews/echo-heist/current/Echo Heist Game Concept.md` was removed; the canonical at `docs/concept_inputs/Echo Heist Game Concept.md` is preserved unchanged. Verified before removal that the duplicate was an informational subset of the canonical (zero information loss).

10. **Stale pending misconception write-back archived (Cleanup Step 6, commit `3faf937`).** Moved from `pending/` to `pending/archive/` with a README explaining the archive policy. The live `bakery-rush-misconceptions.json` was untouched; the archived file's `status: pending_review` field is preserved byte-identical.

11. **Orchestrator clarification (Cleanup Steps 8 and 9, commits `ebfc2c1` and `7a32df9`).** New `orchestrator/README.md` (which previously did not exist) explicitly states this is the live Era 1 orchestrator and points at `orchestrator_v3/` as a separate blueprint. `orchestrator_v3/README.md` got a one-line cross-reference to the live orchestrator and an expanded "What is not here yet" section with a "Note on local directory state" paragraph. Three previously-untracked empty subdirectories were removed from the local working tree.

12. **Root README clarified (Cleanup Step 1, commit `90e76e9`).** Strictly additive: a new "Repository layers" section and a "Where to start reading" routing table were inserted after the existing intro. All existing content (Pipeline, Modes, Quick start, Benchmark cases, Agent structure, Gate engine, Misconception Architect, Repository structure, Current status, Current limitations) is byte-unchanged.

13. **`reviews/README.md` rewritten (Cleanup Step 3, commit `667b2b0`).** Replaces the previews/-era "Playable Prototype Checkpoints" framing with the new "mutable review-build layer" framing. Drops the outdated 3-pass convention table.

For the per-commit details, see `git log --oneline` from `6145c83` (the first migration commit) through this audit's commit.

## What is still pending

This list is not exhaustive — see Taskade for the live operational queue. Repo-side pending items:

### Migration phases not yet complete

| Phase | What | Status |
|---|---|---|
| **Phase 6** | Dry-run dispatch test against one game (e.g. `unitcircle`) to confirm end-to-end plumbing | not started; requires Taskade dispatch credentials and explicit go-ahead |
| **Phase 7** | First real release | not started; will only happen on explicit Taskade GREEN gate dispatch |

### Locked-as-future-gap content items

| Item | Status |
|---|---|
| Misconception library entries for `power-grid`, `echo-heist`, `counting` | Locked as a future content gap. Will not be invented; await real misconception data. |
| Concept folders for the 6 existing games (`bakery`, `counting`, `echo-heist`, `fire`, `power-grid`, `unitcircle`) | Locked as deferred. Will not be invented retroactively. |

### Deferred work items

| Item | Status |
|---|---|
| Taskade app reference doc (`docs/taskade_app_reference.md`) | Structure approved (Option A, real values, no placeholders); blocked on user supplying 8 inputs (Taskade space URL, live agents, live workflows, PAT storage location, PAT rotation policy, review cadence, maintainer, next review date). This audit completes the cleanup sequence, which unblocks asking for those inputs. |
| Update to `agents/implementation_plan/agent.py` line 315 prompt text (`previews/bakery/pass-N.html` reference) | Explicitly deferred per user instruction. Not a correctness issue. |
| Update to `docs/repo_systems_audit.md` (the previous audit) | Will not happen. The previous audit is preserved unchanged as a historical snapshot. New audits get new dated files. |

### Branch state

`main` is currently 19 commits ahead of `origin/main`. Nothing has been pushed during this session.

---

## Conservative honesty section

This audit follows the same conservative field policy as the family registry and the concept lane tracker. Specifically:

- **Nothing in this repo has been shipped.** `games/` is empty. `release_state` is `"never_shipped"` on every game in the family registry. There is no SemVer tag of the form `game/<slug>/vX.Y.Z` in git. The promote-build workflow has never been triggered.
- **Nothing has a formal CCSS alignment** except Snack Line Shuffle. Bakery Rush, Fire Dispatch, Unit Circle Pizza Lab, Power Grid Operator, Watering Hole Count, and Echo Heist all have `primary_standard: null` in the registry. Informal claims from README benchmark tables, in-file header comments, or concept_inputs strategy docs do **not** count as formal alignment. The same applies to grade-band claims.
- **Family placement is documented for 2 of 7 games.** Snack Line Shuffle (Compare and Order — documented in family_map_math.md and the concept packet) and Bakery Rush (Quantity and Fulfillment — documented in family_map_math.md). The other 5 games live in the `Pending Formal Family Placement` pseudo-family in the registry, which is explicitly marked `is_pseudo_family: true`.
- **Interaction type is documented for 4 of 7 games.** Snack Line Shuffle, Bakery Rush, Fire Dispatch, Unit Circle Pizza Lab. The other 3 (Counting, Echo Heist, Power Grid) are marked `pending_taxonomy_placement`.
- **Concept folders exist for 1 of 7 games.** Only `concepts/snack-line-shuffle/`. The other 6 have no `concepts/<slug>/` packet.
- **Misconception library entries exist for 4 of 7 games.** Bakery Rush, Fire Dispatch, Unit Circle, Snack Line Shuffle. The other 3 are tracked as a future content gap.
- **The promote-build workflow is structurally complete but operationally untested.** Phase 6 (dry-run dispatch) and Phase 7 (first real release) are still pending.

This audit must not be cited as evidence of build validation, playtest validation, curricular coverage proof, ship-ready status, or family/interaction-type coverage beyond what is already documented in the canonical references it cites.

---

## References

| Reference | What it is |
|---|---|
| [`docs/pipeline_policy.md`](pipeline_policy.md) | Canonical Era 3 policy (two-system model, three layers, branch policy, SemVer, gate, promotion flow) |
| [`docs/concept_lanes.md`](concept_lanes.md) | Concept lane tracker (7 entries with conservative field policy) |
| [`memory/registries/family_registry.json`](../memory/registries/family_registry.json) | Structured family-and-game registry (3 families + 7 members, conservative fields) |
| [`docs/os_spec_2026.md`](os_spec_2026.md) | Era 2 OS design rulebook |
| [`README.md`](../README.md) | Root README with the three-era model in the "Repository layers" section |
| [`reviews/README.md`](../reviews/README.md) | Review build layer documentation |
| [`games/README.md`](../games/README.md) | Release archive layer documentation |
| [`.github/workflows/promote-build.yml`](../.github/workflows/promote-build.yml) | The only GitHub Actions workflow; enforces the GREEN gate contract |
| [`orchestrator/README.md`](../orchestrator/README.md) | Live Era 1 orchestrator |
| [`orchestrator_v3/README.md`](../orchestrator_v3/README.md) | Era 2 LangGraph orchestrator blueprint |
| [`docs/repo_systems_audit.md`](repo_systems_audit.md) | The previous (pre-migration) audit. **Intentionally preserved unchanged.** |

## Document metadata

| Field | Value |
|---|---|
| Filename | `docs/repo_systems_audit_2026-04-09.md` |
| Date | 2026-04-09 |
| Status | Snapshot (immutable) |
| Author | Cleanup Step 10 snapshot |
| Supersedes | Nothing — this is additive; the prior audit at `docs/repo_systems_audit.md` is preserved unchanged |
| When to update | **Never edit this file.** When the next large structural change happens, create a new audit at `docs/repo_systems_audit_<YYYY-MM-DD>.md`. Audits are dated immutable snapshots. |
| Related commits | `6145c83` (Phase 1), `a78825f` (Phase 2), `07abf1f` (Phase 3), `12be815` (Phase 4), `18c16db` (Phase 5), `667b2b0` `90e76e9` `f2d371f` `4990517` `de9437b` `3faf937` `ebfc2c1` `7a32df9` (Cleanup Steps 3, 1, 4, 5, 2, 6, 8, 9), and this commit (Cleanup Step 10) |
