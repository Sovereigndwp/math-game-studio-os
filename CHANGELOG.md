# Changelog

All notable changes to this project will be documented here.

---

## [V1 Baseline] — 2026-04-03

### Summary

V1 is the first complete end-to-end pipeline: six agents run in sequence, all six gate
decisions enforced, stub and LLM modes both verified, and benchmark regression suite
passing 5/5 in both modes. This entry records the state of the system at the V1 baseline
lock. Everything after this entry is explicitly post-V1.

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
| bench_02 | strong_middle_fire_dispatch | approved | lowest_viable_loop_brief | route_and_dispatch |
| bench_03 | strong_high_school_unit_circle | approved | lowest_viable_loop_brief | navigate_and_position |
| bench_04 | overloaded_bad_concept | rejected | kill_report | — |
| bench_05 | cute_but_weak_concept | rejected | kill_report | — |

**Stub mode result:** 5/5 passed.
**LLM mode result (claude-sonnet-4-6):** 5/5 passed.

Reports saved to `reports/benchmark_regression_stub_20260403T224339Z.md` and
`reports/benchmark_regression_llm_20260403T225330Z.md`.

---

### Bug Fixes

**`scripts/run_benchmarks.py` — critical field name mismatch:**
- `_compare()` read `result.stop_stage`, which does not exist on `PipelineResult`. The correct field is `result.final_artifact_name`. With the old name, every stop-stage comparison returned `"unknown"`, causing all five benchmarks to fail the stop-stage check regardless of actual pipeline output.
- Fixed: `getattr(result, "stop_stage", "unknown")` → `getattr(result, "final_artifact_name", "unknown")`.

**`scripts/run_benchmarks.py` — missing `sys.path` patch:**
- Importing `pipeline` and `utils.llm_caller` from `scripts/` failed because the repo root was not on `sys.path` when the script was invoked directly.
- Fixed: `_REPO_ROOT = Path(__file__).resolve().parents[1]` added at module level with `sys.path.insert(0, str(_REPO_ROOT))` guard.

**`agents/intake_framing/agent.py` — stub coverage gaps causing bench_02 false failure:**
- The intake stub recognized `"grade 1"` and `"grade 2"` but not `"grade 3"`. The bench_02 command uses `"grade 3"`, so `likely_age_band` fell through to `"unknown"`, setting `age_fit` confidence to 0.4. The downstream kill test stub then scored `loop_obviousness` and `teacher_value` below threshold, producing a `"redesign"` status that gated the job as rejected.
- Fixed: grade detection extended to cover grades 1–5 (elementary) and grades 6–8 (middle school).
- The intake stub also recognized `"addition"` but not `"arithmetic"`. The bench_02 command uses `"arithmetic"`, so `likely_math_domain` fell through to `"unknown"`, setting `math_fit` confidence to 0.4.
- Fixed: `"arithmetic"` added as an alias for `"addition"` in domain detection.

---

### New Files

| File | Purpose |
|---|---|
| `scripts/run_benchmarks.py` | Benchmark regression runner (stub and LLM modes, optional markdown report) |
| `RUNBOOK.md` | Environment setup, venv activation, benchmark commands, API key rotation, V1 pass criteria |
| `docs/benchmark_rubric.md` | Qualitative review rubric — six dimensions scored 1–4, evidence pointers, score summary template |
| `docs/benchmark_review_v1.md` | Applied rubric scores for all three approved benchmark concepts, with strengths, weak spots, and recommended next actions |
| `.claude/launch.json` | Available pipeline entry points (no web servers in this project) |

---

### V1 Qualitative Review — Approved Concepts

Applied rubric: `docs/benchmark_rubric.md`. Full review: `docs/benchmark_review_v1.md`.

| Concept | Clarity | Purity | Family | Loop | Education | Monetization | Total |
|---|---|---|---|---|---|---|---|
| Bakery (bench_01) | 4 | 4 | 4 | 4 | 4 | 4 | **24/24** |
| Fire Dispatch (bench_02) | 3 | 3 | 3 | 3 | 3 | 3 | **19/24** |
| Unit Circle (bench_03) | 4 | 3 | 4 | 3 | 4 | 2 | **20/24** |

**Bakery (bench_01)** is the V1 exemplar. Every dimension is clean. Interaction purity 0.93.
Family boundaries are rigorous and self-governing. Loop requires no tutorial. Reference case
for all future pipeline output evaluation.

**Fire Dispatch (bench_02)** is production-viable at the primary loop level. One open item
before the family can accept a second member: a loop spec for the secondary
`allocate_and_balance` supply mechanic (currently analyzed but not loop-designed). Core
dispatch loop is ready for prototyping. Demand/capacity labeling gap in the UX needs a
design answer in the first prototype pass.

**Unit Circle (bench_03)** is the strongest educational output. Interaction purity 0.87.
The pizza-as-unit-circle metaphor is structurally exact. Fail state (correct position reveal
on miss) is the best instructional mechanism across all three concepts. Commercially narrow:
HS trig audience, lab mode, low replay after skill mastery. Recommended channel is
school/district licensing, not consumer app. Acceptance zone calibration (suggested 8% of
pizza radius) is the highest-priority unresolved technical parameter.

---

### Systemic Observation

All three approved loops are genuinely minimal. The pipeline is correctly enforcing the
"no tutorial required" constraint — all three teacher shortcuts and micro-prototypes are
playable with household objects and no digital tools. This is the most important
architectural quality V1 has delivered: a concept that requires a tutorial to understand
is a concept that has not been specified correctly.

---

### Known Limitations at V1 Baseline

- Stub agents use keyword matching only. Commands that use synonyms not in the keyword list
  (e.g., a valid grade-level term not yet covered) may produce incorrect confidence scores
  and fail the kill test stub without a real viability problem. LLM mode is not affected.
- Interaction warnings (mismatch between expected and actual `primary_interaction_type`) are
  logged but do not fail the benchmark. In LLM mode, the model may select a valid but
  different interaction type. Warnings should be reviewed before treating an LLM run as a
  clean regression pass.
- The benchmark suite does not yet test revision behavior (i.e., a concept that requires one
  revision before passing a gate). All five current cases pass or reject on the first attempt.
- No test coverage for `outcome = "stalled"` (revision limit exceeded unexpectedly). This
  path exists in the pipeline but has no corresponding benchmark case.
