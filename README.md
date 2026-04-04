# Math Game Studio OS

A multi-agent pipeline that takes a raw educational math game concept and decides
whether it is worth building and, if so, produces both a prototype-ready
specification and a first-build implementation handoff. Each stage reasons about
the concept through a different lens such as learner fit, viability,
interaction design, loop structure, prototype translation, and implementation
readiness. A gate engine enforces pass, revise, or reject before the pipeline
advances.

**Who it's for:** Game designers, educators, and developers exploring math game
concepts for learners across K–12. The pipeline catches weak ideas early and
gives strong ideas a clear path from concept to prototype build handoff.

## Modes

- **Stub mode** — deterministic keyword-based agents, no API key needed, about
  5 seconds. Use for regression testing and development.
- **LLM mode** — each agent calls Claude for real reasoning, about 3 to 5
  minutes. Requires `ANTHROPIC_API_KEY`. Use for production concept evaluation.

## Pipeline

```text
Stage 0  Orchestrator ───────────── parse raw command into request_brief
Stage 1  Intake Framing ────────── learner band, math domain, world theme
Stage 2  Kill Test ─────────────── reject overloaded or unviable concepts early
Stage 3  Interaction Mapper ────── choose primary interaction type
Stage 4  Family Architect ──────── place concept in an interaction family
Stage 5  Core Loop Designer ────── define the smallest meaningful loop
Stage 6  Prototype Spec ────────── translate approved loop into a prototype specification
Stage 7  Prototype Build Spec ──── translate spec to implementation handoff
```

Each stage produces one JSON artifact validated against a schema in
artifacts/schemas/. Rejected concepts stop early, usually at Stage 2.
Approved concepts run all eight stages, Stages 0 through 7, and exit with a
prototype_build_spec ready for implementation planning.

Revision behavior: If a gate returns revise, the pipeline retries the
agent up to the limit in its config.yaml. If revision limits are exceeded, the
pipeline stalls and reports why.

## Quick start

```bash
# Activate the virtual environment
source .venv/bin/activate

# Run stub benchmarks
python scripts/run_benchmarks.py

# Generate a markdown report in reports/
python scripts/run_benchmarks.py --report
```

Expected output: 5/5 passed.

To run a single concept through the pipeline directly:

```python
from pathlib import Path
from pipeline import run_v1_pipeline

result = run_v1_pipeline(
    raw_command="Create a grade 2 bakery game for addition to 20.",
    repo_root=Path("."),
)
print(result.outcome)              # "approved" or "rejected"
print(result.final_artifact_name)  # e.g. "prototype_build_spec"
print(result.final_artifact_path)  # path to the output JSON
```

For LLM mode, see RUNBOOK.md.

## Benchmark cases

| # | Case | Learner | Expected outcome | Stop stage |
|---|---|---|---|---|
| 1 | Bakery | K–2, addition | approved | prototype_build_spec |
| 2 | Fire Dispatch | grades 4–6, multiplication | approved | prototype_build_spec |
| 3 | Unit Circle Pizza Lab | high school, trigonometry | approved | prototype_build_spec |
| 4 | Overloaded bad concept | — | rejected | kill_report |
| 5 | Cute but weak concept | — | rejected | kill_report |

Cases 1 through 3 test the full pipeline through the current implementation-stage
handoff. Cases 4 and 5 test early rejection at the kill gate. All five pass in
both stub and LLM modes.

## Repository structure

```
pipeline.py                  Main entry point — runs stages 0–7 in sequence
agents/                      One directory per agent (agent.py, prompt.md, config.yaml)
  intake_framing/            Stage 1 — intake_brief
  kill_test/                 Stage 2 — kill_report
  interaction_mapper/        Stage 3 — interaction_decision_memo
  family_architect/          Stage 4 — family_architecture_brief
  core_loop/                 Stage 5 — lowest_viable_loop_brief
  prototype_spec/            Stage 6 — prototype_spec
  prototype_build_spec/      Stage 7 — prototype_build_spec
engine/                      Gate decision engine (pass/revise/reject per stage)
orchestrator/                Stage ledger — tracks versions, revision counts, gate states
artifacts/schemas/           JSON schemas for all artifact types
utils/                       Shared agent runner, LLM caller, schema validator
scripts/                     Benchmark runner (run_benchmarks.py)
memory/                      Job workspace storage (generated, gitignored)
reports/                     Benchmark markdown reports (generated, gitignored)
docs/                        Project documentation
```

## Agent structure

Every agent follows the same pattern:

| File | Purpose |
|---|---|
| `agent.py` | Stub and LLM implementations. Exports a `run()` entry point. |
| `prompt.md` | Agent contract: role, reasoning rules, and constraints. |
| `config.yaml` | Allowed artifact reads and writes, revision limit, and model profile. |

The orchestrator calls `run()`, the shared agent runner injects metadata such as
job_id, version, and produced_by, validates the output against its schema, and
then hands it to the gate engine. If the gate passes, the pipeline advances.
If it revises, the agent retries. If it rejects, the pipeline stops.

## Gate engine

The gate engine in engine/gate_engine.py evaluates each artifact
independently. Gate dimensions vary by stage.

For prototype_spec, the gate focuses on:
- concept fidelity
- build clarity
- scope discipline
- loop integrity
- testability
- deferral quality

For prototype_build_spec, the gate focuses on:
- build concreteness
- prototype fidelity
- state clarity
- edge-case coverage
- scope discipline
- acceptance clarity
- internal consistency

Fidelity violations are identity-level failures and should reject. Most other
gaps are fixable and should revise.

## Documentation

| Document | Contents |
|---|---|
| RUNBOOK.md | Setup, commands, troubleshooting, API key rotation |
| CHANGELOG.md | Release notes and change history |
| docs/v1_handoff.md | What V1 delivered, what is stable, and what is deferred |
| docs/v2_boundary.md | V2 scope, gate criteria, and known limitations |
| docs/v2_boundary_freeze.md | Frozen V2 boundary checkpoint and exact defining files |
| docs/benchmark_rubric.md | Six-dimension concept scoring criteria |
| docs/benchmark_review_v1.md | Qualitative review of the three approved concepts |

## Current status

- V1 — frozen at tag v1.0. Stages 0 through 5, five benchmarks, all
  passing in stub and LLM modes.
- V2 boundary — defined and frozen. Stage 6 prototype_spec and Stage 7
  prototype_build_spec are now in place.
- Current endpoint — approved concepts now exit with
  prototype_build_spec, which serves as the first-build implementation handoff.
- First implementation example — Bakery is the lead concept through the
  current implementation-stage handoff.
