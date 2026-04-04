# V1 Handoff Document

**Tag:** `v1.0` · **Commit:** `ce1c246` · **Date:** 2026-04-03

---

## What V1 Delivered

A six-agent sequential pipeline that takes a raw game concept command and produces
either a rejection report or a complete lowest-viable-loop brief:

| Stage | Agent | Artifact |
|---|---|---|
| 0 | Orchestrator (deterministic) | `request_brief` |
| 1 | Intake and Framing | `intake_brief` |
| 2 | Kill Test | `kill_report` |
| 3 | Interaction Mapper | `interaction_decision_memo` |
| 4 | Family Architect | `family_architecture_brief` |
| 5 | Core Loop | `lowest_viable_loop_brief` |

**Dual-mode operation:** stub mode (deterministic keyword stubs, no API key) and
LLM mode (Claude API, requires `ANTHROPIC_API_KEY`).

**Benchmark regression suite:** 5 cases, 5/5 passing in both modes.

**Qualitative review:** three approved concepts scored against a six-dimension rubric.

**Documentation:** RUNBOOK, benchmark rubric, benchmark review with business
sequencing, CHANGELOG, requirements.txt.

---

## What Is Stable

These components are hardened, tested, and safe to build on:

- **Pipeline orchestration** (`pipeline.py`): stage sequencing, gate enforcement,
  revision limits, `PipelineResult` contract.
- **Gate engine** (`engine/gate_engine.py`): pass/revise/reject decisions between
  every stage.
- **Stage ledger** (`orchestrator/stage_ledger.py`): version tracking, revision
  counts, stage state management.
- **Artifact schemas** (`artifacts/schemas/`): JSON schema validation for all six
  artifacts.
- **SharedAgentRunner** (`utils/shared_agent_runner.py`): metadata injection
  (`artifact_name`, `produced_by`, `job_id`, `version`).
- **Benchmark runner** (`scripts/run_benchmarks.py`): outcome, stop-stage, and
  interaction checks; markdown report generation.
- **Stub agents** for all six stages: deterministic keyword matching, sufficient
  for regression testing without API calls.

---

## What Is Intentionally Out of Scope for V1

These items were considered and explicitly deferred:

| Item | Reason for deferral |
|---|---|
| Revision-path benchmark cases | Pipeline supports revisions, but no benchmark exercises the revise→re-run→re-gate loop. Requires V2 benchmark expansion. |
| Stall-path benchmark case | `outcome = "stalled"` path exists but has no regression coverage. Same reason. |
| Prototype or build output | V1 produces design briefs, not runnable games. Prototyping is a downstream activity. |
| Consumer-facing UI | Pipeline is CLI-only. No web interface, no API server. |
| Multi-pipeline orchestration | V1 runs one concept at a time. Parallel or batched runs are not supported. |
| Difficulty scaffolding specs | Loop briefs define the core loop; difficulty progression and level design are prototyping concerns. |
| Collection, social, or reward systems | Identified as gaps in monetization scoring but belong to game design, not pipeline design. |

---

## Open Questions That Belong to Prototyping

These are approved by V1 but have unresolved design parameters. They are tracked in
`docs/benchmark_review_v1.md § Post-Review Open Items` and must be resolved during
prototyping, not by the pipeline.

1. **Bakery (bench_01):** Lock quantity representation mode — pictorial, numeral, or
   mixed. Required before engineering start.
2. **Fire Dispatch (bench_02):** Commission `allocate_and_balance` loop spec for the
   supply mechanic. Required before level 4+ build.
3. **Fire Dispatch (bench_02):** Define demand/capacity labeling affordance in UX.
   Required before first prototype pass.
4. **Unit Circle (bench_03):** Document non-axis angle pairing constraint in difficulty
   scaffolding spec. Required before level design start.
5. **Unit Circle (bench_03):** Define acceptance zone tuning protocol (starting point:
   8% of pizza radius). Required before first playtesting round.

---

## Concept Sequencing (from V1 Review)

1. **Prototype Bakery first.** 24/24, no open design questions at loop level, widest
   market (K–2 addition).
2. **Spec Fire Dispatch supply mechanic in parallel** — primary dispatch loop is
   prototype-ready today; supply mechanic loop spec is a parallel task, not a blocker.
3. **Hold Unit Circle at concept** until a confirmed institutional sales channel
   justifies the build investment.

---

## Canonical Artifacts

| File | Purpose |
|---|---|
| `CHANGELOG.md` | Complete V1 baseline and hardening record |
| `RUNBOOK.md` | Environment setup, commands, troubleshooting |
| `docs/benchmark_rubric.md` | Six-dimension scoring rubric (1–4 scale) |
| `docs/benchmark_review_v1.md` | Applied rubric, sequencing, open items |
| `scripts/run_benchmarks.py` | Regression runner (stub + LLM modes) |
| `requirements.txt` | Pinned Python dependencies |
