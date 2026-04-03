# Changelog

All notable changes to this project will be documented here.

---

## [V1 Hardening] — 2026-04-03 (post-baseline)

Changes made during the autonomous V1 hardening phase after the baseline commit.
All stub benchmarks verified 5/5 after each change.

### fix: expand intake framing stub coverage and fix hardcoded timestamp

- Replace hardcoded timestamp `"2026-04-03T12:01:00Z"` with dynamic UTC value.
- Add kindergarten / preschool grade band detection (age 3–5).
- Add grades 9–12 explicit detection alongside "high school" keyword.
- Add advanced_anchor factory type override for AP, calculus, statistics, honors.
- Expand math domain detection from 3 to 11 domains:
  `addition`, `subtraction`, `multiplication`, `division`, `fractions`,
  `ratios_and_rates`, `algebra`, `geometry`, `trigonometry`, `statistics`, `calculus`.
- Add world theme stubs for hospital, farm/garden, space, and generic shop.
- Domains are checked in specificity order (calculus before trig before algebra)
  to prevent coarser terms from shadowing more specific matches.

### chore: extend .gitignore for worktrees and debug payloads

- Exclude `.claude/worktrees/` (Claude Code session artifacts, not source).
- Exclude `memory/**/*.INVALID_DEBUG.*.json` (written by shared_agent_runner
  on artifact validation failure; not source, not test fixtures).

### docs: improve V1 runbook accuracy and completeness

- Clarify Python version: the venv is 3.14.3; system Python version is irrelevant.
- Remove misleading conditional comment on pip install.
- Add expected runtimes: stub ~5–10 seconds, LLM ~3–5 minutes.
- Add troubleshooting section covering five common failure modes with exact fixes.
- Add dependency upgrade instructions with pip freeze filter command.
- Standardize model override example to `claude-sonnet-4-6`.

### docs: tighten benchmark rubric for V1 completeness

- Add dimension conflict guidance (name constraining dimension, do not average).
- Clarify Dimension 3 "enumerated conditions" with a concrete labeled example.
- Add `confidence_scores.math_fit` thresholds to Dimension 5 evidence.
- Generalize Dimension 6 replay examples to domain-neutral language.
- Add replay_potential score thresholds to Dimension 6 evidence.
- Add run date, mode, and constraining dimension fields to score summary template.

### docs: strengthen benchmark review with explicit sequencing and action items

- Add canonical LLM report reference.
- Quote supply mechanic authoritative definition from `interaction_decision_memo`.
- Add constraining dimension field to each concept.
- Add explicit V1 Business Sequencing Guidance section.
- Add Post-Review Open Items table with owner and required-before columns.

---

## [V1 Baseline] — 2026-04-03

### Summary

V1 is the first complete end-to-end pipeline: six agents run in sequence, all six gate
decisions enforced, stub and LLM modes both verified, and benchmark regression suite
passing 5/5 in both modes. A pipeline run is a **V1 pass** when all five criteria are
met: correct outcome, correct stop stage (`final_artifact_name`), matching primary
interaction type, all intermediate gates returned `pass`, and no stalled jobs.
Everything after this entry is explicitly post-V1.

---

### Pipeline

**Six-agent V1 pipeline established and verified (`pipeline.py`):**

| Stage | Agent | Output artifact |
|---|---|---|
| 0 | Orchestrator (deterministic) | `request_brief` |
| 1 | Intake and Framing Agent | `intake_brief` |
| 2 | Kill Test Agent | `kill_report` |
| 3 | Interaction Mapper Agent | `interaction_decision_memo` |
| 4 | Family Architect Agent | `family_architecture_brief` |
| 5 | Core Loop Agent | `lowest_viable_loop_brief` |

- Gate pre-conditions enforced between every stage: no agent runs unless the previous gate returned `pass`.
- Revision limit enforced per stage (max 2 revisions). Exceeding the limit produces a synthetic `reject` gate and terminates the job with `outcome = "rejected"`.
- Dual-mode operation confirmed: stub mode (deterministic keyword-matching stubs, no API key) and LLM mode (all agents driven through Claude, requires `ANTHROPIC_API_KEY`).
- `PipelineResult` fields: `job_id`, `outcome`, `final_artifact_name`, `final_artifact_path`, `stage_records`, `rejection_reason`, `error`.

---

### Benchmark Regression Suite

**Five benchmark cases defined and locked (`scripts/run_benchmarks.py`):**

| ID | Label | Expected outcome | Expected stop stage | Expected interaction |
|---|---|---|---|---|
| bench_01 | strong_elementary_bakery | approved | lowest_viable_loop_brief | combine_and_build |
| bench_02 | strong_middle_fire_dispatch | approved | lowest_viable_loop_brief | route_and_dispatch (primary) |
| bench_03 | strong_high_school_unit_circle | approved | lowest_viable_loop_brief | navigate_and_position |
| bench_04 | overloaded_bad_concept | rejected | kill_report | — |
| bench_05 | cute_but_weak_concept | rejected | kill_report | — |

**Stub mode result:** 5/5 passed.
**LLM mode result (claude-sonnet-4-6):** 5/5 passed.

Canonical reports:
- `reports/benchmark_regression_stub_20260403T224339Z.md`
- `reports/benchmark_regression_llm_20260403T225330Z.md`

Scores recorded in the qualitative review below are from this V1 baseline LLM run.
For current scores after any re-run, see `docs/benchmark_review_v1.md`.

---

### Bug Fixes

**`scripts/run_benchmarks.py` — CRITICAL: field name mismatch caused all five benchmarks to fail stop-stage check:**
- `_compare()` read `result.stop_stage`, which does not exist on `PipelineResult`. The
  correct field is `result.final_artifact_name`. With the old name, every stop-stage
  comparison returned `"unknown"`, causing all five benchmarks to fail regardless of actual
  pipeline output. This was a total regression of the stop-stage criterion.
- Fixed: `getattr(result, "stop_stage", "unknown")` → `getattr(result, "final_artifact_name", "unknown")`.

**`scripts/run_benchmarks.py` — missing `sys.path` patch:**
- Importing `pipeline` and `utils.llm_caller` from `scripts/` failed because the repo root
  was not on `sys.path` when the script was invoked directly.
- Fixed: `_REPO_ROOT = Path(__file__).resolve().parents[1]` added at module level with
  `sys.path.insert(0, str(_REPO_ROOT))` guard.

**`agents/intake_framing/agent.py` — stub coverage gaps causing bench_02 false failure:**
- The intake stub recognized `"grade 1"` and `"grade 2"` but not `"grade 3"`. The bench_02
  command uses `"grade 3"`, so `likely_age_band` fell through to `"unknown"` (confidence 0.4).
  The downstream kill test then scored `loop_obviousness` and `teacher_value` below threshold,
  producing `status = "redesign"` → gate returned `"revise"` → pipeline rejected at kill_report.
- Fixed: grade detection extended to grades 1–5 (elementary) and grades 6–8 (middle school).
- The stub also recognized `"addition"` but not `"arithmetic"`. The bench_02 command uses
  `"arithmetic"`, so `likely_math_domain` fell through to `"unknown"` (confidence 0.4).
- Fixed: `"arithmetic"` added as an alias for `"addition"` in domain detection.

---

### New Files

New documentation and tooling files added during V1:

| File | Purpose |
|---|---|
| `scripts/run_benchmarks.py` | Benchmark regression runner (stub and LLM modes, optional markdown report) |
| `RUNBOOK.md` | Environment setup, venv activation, benchmark commands, API key rotation, V1 pass criteria |
| `docs/benchmark_rubric.md` | Qualitative review rubric — six dimensions scored 1–4, evidence pointers, score summary template |
| `docs/benchmark_review_v1.md` | Applied rubric scores for the three approved benchmark concepts, sequencing guidance, and open items |
| `.claude/launch.json` | Available pipeline entry points (CLI only — this project has no web dev servers) |

---

### V1 Qualitative Review — Approved Concepts

Applied rubric: `docs/benchmark_rubric.md`. Full review: `docs/benchmark_review_v1.md`.

| Concept | Clarity | Purity | Family | Loop | Education | Monetization | Total |
|---|---|---|---|---|---|---|---|
| Bakery (bench_01) | 4 | 4 | 4 | 4 | 4 | 4 | **24/24** |
| Fire Dispatch (bench_02) | 3 | 3 | 3 | 3 | 3 | 3 | **19/24** |
| Unit Circle (bench_03) | 4 | 3 | 4 | 3 | 4 | 2 | **20/24** |

**Bakery (bench_01)** is the V1 exemplar. Every dimension is clean. Interaction purity 0.93.
No open design questions at the loop level. Reference case for all future pipeline output
evaluation. Recommended to prototype first.

**Fire Dispatch (bench_02)** is production-viable at the primary loop level. One item before
the family can accept a second member: a loop spec for the `allocate_and_balance` supply
mechanic (analyzed and defined in the interaction_decision_memo, but not yet loop-designed).
Primary dispatch loop is ready for prototyping today.

**Unit Circle (bench_03)** is the strongest educational output. Interaction purity 0.87.
Fail state (correct position reveal on miss) is the best instructional mechanism across all
three concepts. Commercially narrow: HS trig audience, lab mode, low post-mastery replay.
Recommended for school/district licensing, not consumer app. Acceptance zone calibration
(suggested 8% of pizza radius) is the highest-priority unresolved technical parameter.

---

### Known Limitations at V1 Baseline

- **Stub keyword coverage is partial.** The intake stub covers 11 math domains and
  kindergarten through grade 12, but any concept using domain vocabulary not in the keyword
  list will fall through to `"unknown"` (confidence 0.4) and may fail the kill test stub
  without a real viability problem. LLM mode is not affected. See the stub for the full
  covered keyword list before using stub mode to evaluate domains outside the current set.
- **Interaction type warnings are not failures.** In LLM mode, the model may select a valid
  but different primary interaction type than the benchmark expectation. The benchmark logs
  this as a `!` warning line, not a `[FAIL]`. Review all warnings before treating an LLM
  run as a fully clean regression pass.
- **No revision-path benchmark cases.** All five cases pass or reject on the first gate
  attempt. The revision loop (gate returns `"revise"` → agent re-runs → gate re-evaluates)
  exists in the pipeline but has no benchmark coverage.
- **No stall-path benchmark case.** The `outcome = "stalled"` path (revision limit exceeded)
  exists in the pipeline but has no corresponding benchmark case.
- **Bench_02 and bench_03 have open design parameters.** Both concepts are V1-approved but
  carry unresolved items: bench_02 needs a supply mechanic loop spec before level 4+; bench_03
  needs acceptance zone calibration before the first playtesting round. These do not affect
  the benchmark but must be tracked before build begins.
