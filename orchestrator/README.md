# orchestrator/

## Status: live

This directory is the **live Era 1 orchestrator** used by
[`pipeline.py`](../pipeline.py). It is real, imported, and running. It is
**not** the blueprint — for the blueprint, see
[`orchestrator_v3/README.md`](../orchestrator_v3/README.md).

## What it does

- Runs the nine-stage concept evaluation pipeline in sequence (Stages 0–8)
- Tracks artifact versions and revision counts via `stage_ledger.py`
- Records each stage's gate decision (pass / revise / reject)
- Halts the pipeline on rejection or revision-limit exhaustion

## Files in this directory

| File | Purpose |
|---|---|
| `orchestrator.py` | Sequential stage runner. Imported by `pipeline.py` as the top-level entry point for a concept run. |
| `stage_ledger.py` | Per-job ledger that records every artifact version, its producing agent, and its gate verdict. |
| `__init__.py` | Package marker. |

## Do not confuse with `orchestrator_v3/`

`orchestrator_v3/` is a **separate directory** containing a
**blueprint**, not a live system. It documents the design of a future
LangGraph-based orchestration graph that would eventually replace the
code in this directory. It is not wired into `pipeline.py`.

If you are debugging a live pipeline run, edit files in **this**
directory (`orchestrator/`). If you are designing the future graph,
work in `orchestrator_v3/`.

## Related docs

- [`pipeline.py`](../pipeline.py) — the entry point that calls into this orchestrator
- [`README.md`](../README.md) — root README, "Repository layers" section (three-era model)
- [`docs/pipeline_policy.md`](../docs/pipeline_policy.md) — Era 3 pipeline policy (separate from Era 1)
- [`orchestrator_v3/README.md`](../orchestrator_v3/README.md) — the blueprint, NOT this system
- [`docs/orchestration_v3_blueprint.md`](../docs/orchestration_v3_blueprint.md) — full Era 2 blueprint design doc
