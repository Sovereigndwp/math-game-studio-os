# Math Game Studio OS

A multi-agent pipeline that takes a raw educational math game concept and decides
whether it is worth building — and if so, produces a prototype-ready build
specification. Each stage reasons about the concept through a different lens
(learner fit, viability, interaction design, loop structure) and a gate engine
enforces pass / revise / reject before the pipeline advances.

**Who it's for:** Game designers, educators, and developers exploring math game
concepts for learners across K–12. The pipeline catches weak ideas early and
gives strong ideas a clear path to prototype.

## Modes

- **Stub mode** — deterministic keyword-based agents, no API key needed, ~5
  seconds. Use for regression testing and development.
- **LLM mode** — each agent calls Claude for real reasoning, ~3–5 minutes.
  Requires `ANTHROPIC_API_KEY`. Use for production concept evaluation.

## Pipeline

```
Stage 0  Orchestrator ─────────── parse raw command into request_brief
Stage 1  Intake Framing ──────── learner band, math domain, world theme
Stage 2  Kill Test ────────────── reject overloaded or unviable concepts early
Stage 3  Interaction Mapper ───── choose primary interaction type
Stage 4  Family Architect ─────── place concept in an interaction family
Stage 5  Core Loop Designer ───── define the smallest meaningful loop
Stage 6  Prototype Spec (V2) ──── translate approved loop into build spec
```

Each stage produces one JSON artifact validated against a schema in
`artifacts/schemas/`. Rejected concepts stop early (typically at Stage 2).
Approved concepts run all seven stages and exit with a `prototype_spec` ready
for implementation.

**Revision behavior:** If a gate returns `revise`, the pipeline retries the
agent (up to the limit in its `config.yaml`). If revision limits are exceeded,
the pipeline stalls and reports why.

## Quick start

```bash
# Activate the virtual environment (ships pre-provisioned)
source .venv/bin/activate

# Run stub benchmarks — no API key needed
python scripts/run_benchmarks.py

# Generate a markdown report in reports/
python scripts/run_benchmarks.py --report
```

Expected output: `5/5 passed`.

To run a single concept through the pipeline directly:

```python
from pathlib import Path
from pipeline import run_v1_pipeline

result = run_v1_pipeline(
    raw_command="Create a grade 2 bakery game for addition to 20.",
    repo_root=Path("."),
)
print(result.outcome)           # "approved" or "rejected"
print(result.final_artifact_name)  # e.g. "prototype_spec"
print(result.final_artifact_path)  # path to the output JSON
```

For LLM mode, see [RUNBOOK.md](RUNBOOK.md).

## Benchmark cases

| # | Case | Learner | Expected outcome | Stop stage |
|---|---|---|---|---|
| 1 | Bakery | K–2, addition | approved | prototype_spec |
| 2 | Fire Dispatch | grades 4–6, multiplication | approved | prototype_spec |
| 3 | Unit Circle Pizza Lab | high school, trigonometry | approved | prototype_spec |
| 4 | Overloaded bad concept | — | rejected | kill_report |
| 5 | Cute but weak concept | — | rejected | kill_report |

Cases 1–3 test the full pipeline through V2. Cases 4–5 test early rejection at
the kill gate. All five pass in both stub and LLM modes.

## Repository structure

```
pipeline.py             Main entry point — runs stages 0–6 in sequence
agents/                 One directory per agent (agent.py, prompt.md, config.yaml)
  intake_framing/       Stage 1 — intake_brief
  kill_test/            Stage 2 — kill_report
  interaction_mapper/   Stage 3 — interaction_decision_memo
  family_architect/     Stage 4 — family_architecture_brief
  core_loop/            Stage 5 — lowest_viable_loop_brief
  prototype_spec/       Stage 6 — prototype_spec (V2)
engine/                 Gate decision engine (pass/revise/reject per stage)
orchestrator/           Stage ledger — tracks versions, revision counts, gate states
artifacts/schemas/      JSON schemas for all artifact types
utils/                  Shared agent runner, LLM caller, schema validator
scripts/                Benchmark runner (run_benchmarks.py)
memory/                 Job workspace storage (generated, gitignored)
reports/                Benchmark markdown reports (generated, gitignored)
docs/                   Project documentation (see table below)
```

## Agent structure

Every agent follows the same pattern:

| File | Purpose |
|---|---|
| `agent.py` | Stub and LLM implementations. Exports a `run()` entry point. |
| `prompt.md` | Full agent contract — role, input/output, reasoning rules, forbidden behaviors. |
| `config.yaml` | Allowed artifact reads/writes, revision limit, model profile. |

The orchestrator calls `run()`, the shared agent runner injects metadata
(`job_id`, `version`, `produced_by`), validates the output against its schema,
then hands it to the gate engine. If the gate passes, the pipeline advances.
If it revises, the agent retries. If it rejects, the pipeline stops.

## Gate engine

The gate engine (`engine/gate_engine.py`) evaluates each artifact independently.
Gate dimensions vary by stage. For `prototype_spec` (the most complex gate):

| Dimension | What it checks | Fail action |
|---|---|---|
| Concept fidelity | Interaction type, family boundary, loop structure preserved from V1 | reject |
| Build clarity | Core loop fields, screen flow, UI components, build notes present | revise |
| Scope discipline | Prototype scope is narrow, included/excluded clearly separated | revise |
| Loop integrity | Signature moment, reset/retry behavior defined | revise |
| Testability | Playtest plan, prototype question, prototype goal present | revise |
| Deferral quality | Deferred items explicitly listed | revise |

Fidelity violations are identity-level failures (reject). All other gaps are
fixable (revise).

## Documentation

| Document | Contents |
|---|---|
| [RUNBOOK.md](RUNBOOK.md) | Setup, commands, troubleshooting, API key rotation |
| [CHANGELOG.md](CHANGELOG.md) | Release notes and change history |
| [docs/v1_handoff.md](docs/v1_handoff.md) | What V1 delivered, what's stable, what's deferred |
| [docs/v2_boundary.md](docs/v2_boundary.md) | V2 scope, gate criteria, known limitations |
| [docs/benchmark_rubric.md](docs/benchmark_rubric.md) | Six-dimension concept scoring criteria |
| [docs/benchmark_review_v1.md](docs/benchmark_review_v1.md) | Qualitative review of the three approved concepts |

## Current status

- **V1** — frozen at tag `v1.0`. Stages 0–5 (six agents), five benchmarks, all
  passing in stub and LLM modes.
- **V2** — Prototype Spec Agent added as Stage 6. Converts approved loop briefs
  into prototype-ready build specifications. Bakery is the first V2 example.
  See [docs/v2_boundary.md](docs/v2_boundary.md) for scope, gate criteria, and
  known limitations.
