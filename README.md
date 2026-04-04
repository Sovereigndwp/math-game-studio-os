# Math Game Studio OS

A multi-agent pipeline that validates educational math game concepts — from raw
idea to prototype-ready specification — using structured reasoning and gate
validation at every stage.

The pipeline runs in two modes:

- **Stub mode** — deterministic keyword-based agents, no API key needed, runs in
  seconds. Use for regression testing and development.
- **LLM mode** — each agent calls Claude for real reasoning. Use for production
  concept evaluation.

## Pipeline stages

```
Stage 0  Intake Framing ──────── learner band, math domain, world theme
Stage 1  Kill Test ────────────── reject overloaded or unviable concepts
Stage 2  Interaction Mapper ───── choose primary interaction type
Stage 3  Family Architect ─────── place concept in interaction family
Stage 4  Core Loop Designer ───── define the smallest meaningful loop
Stage 5  Prototype Spec (V2) ──── translate approved loop into build spec
```

Each stage produces one artifact, validated against a JSON schema. A gate engine
decides pass / revise / reject before the pipeline advances. Rejected concepts
stop early (typically at Kill Test). Approved concepts run all six stages.

## Quick start

```bash
# Activate the virtual environment
source .venv/bin/activate

# Run stub benchmarks (no API key needed, ~5 seconds)
python scripts/run_benchmarks.py

# Run with a markdown report
python scripts/run_benchmarks.py --report
```

Expected output: `5/5 passed`.

For LLM mode, set `ANTHROPIC_API_KEY` first — see [RUNBOOK.md](RUNBOOK.md) for
details.

## Benchmark cases

| # | Case | Expected outcome | Expected stop stage |
|---|---|---|---|
| 1 | Bakery (K–2 addition) | approved | prototype_spec |
| 2 | Fire Dispatch (grades 4–6 multiplication) | approved | prototype_spec |
| 3 | Unit Circle Pizza Lab (high school trig) | approved | prototype_spec |
| 4 | Overloaded bad concept | rejected | kill_report |
| 5 | Cute but weak concept | rejected | kill_report |

## Repository structure

```
pipeline.py             Main entry point — runs all stages in sequence
agents/                 One directory per agent (agent.py, prompt.md, config.yaml)
  intake_framing/
  kill_test/
  interaction_mapper/
  family_architect/
  core_loop/
  prototype_spec/       V2 agent — concept-to-prototype translation
engine/                 Gate decision engine (pass/revise/reject logic)
orchestrator/           Stage ledger and pipeline sequencing
artifacts/schemas/      JSON schemas for all artifact types
utils/                  Shared utilities (LLM caller, validation, agent runner)
scripts/                Benchmark runner
memory/                 Job workspace storage (generated, gitignored)
reports/                Benchmark reports (generated, gitignored)
docs/                   Project documentation
```

## Documentation

| Document | Contents |
|---|---|
| [RUNBOOK.md](RUNBOOK.md) | Setup, commands, troubleshooting, API key rotation |
| [CHANGELOG.md](CHANGELOG.md) | Release notes and change history |
| [docs/v1_handoff.md](docs/v1_handoff.md) | What V1 delivered and what's stable |
| [docs/v2_boundary.md](docs/v2_boundary.md) | V2 scope, gate criteria, known limitations |
| [docs/benchmark_rubric.md](docs/benchmark_rubric.md) | Six-dimension scoring criteria |
| [docs/benchmark_review_v1.md](docs/benchmark_review_v1.md) | Qualitative review of V1 concepts |

## Agent structure

Each agent follows the same pattern:

- `agent.py` — stub and LLM implementations, `run()` entry point
- `prompt.md` — full agent contract (role, input/output, reasoning rules)
- `config.yaml` — allowed reads/writes, revision limits, model profile

The orchestrator calls each agent's `run()` function, injects metadata, validates
the output against its schema, then passes it to the gate engine.

## Current status

- **V1** — frozen at tag `v1.0`. Five-stage pipeline, five benchmarks, all passing.
- **V2** — Prototype Spec Agent added as Stage 5. Converts approved loop briefs
  into build-ready prototype specifications. Gate validates fidelity, build
  clarity, scope discipline, loop integrity, testability, and deferral quality.
