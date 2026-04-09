# Math Game Factory Orchestrator V3

Blueprint and stub implementation for the LangGraph-based orchestration system. The **live** Era 1 orchestrator currently used by `pipeline.py` lives at [`orchestrator/`](../orchestrator/README.md) — not here.

**Status: Design-committed. Not yet running.**

See `docs/orchestration_v3_blueprint.md` for the full design rationale,
visual diagram, build phases, and readiness checklist.

---

## What is here

```
orchestrator_v3/
├── state.py                   TypedDict shared state (all graph fields)
├── policies/
│   ├── gates.yaml             Gate definitions and thresholds
│   ├── misconception_taxonomy.yaml  Six required error categories
│   └── interaction_types.yaml  Approved interaction taxonomy
├── prompts/
│   └── agents/
│       ├── role_to_math_auditor.md
│       ├── misconception_architect.md
│       └── loop_purity_auditor.md
└── README.md
```

## What is not here yet

- `graph.py` — LangGraph StateGraph wiring (Phase 2 build)
- `subgraphs/` — Research, Design, Evaluation, Packaging subgraphs
- `agents/` — Python node implementations (Phase 3 build)
- `memory/` — Project and system memory stores
- `prompts/repair/` — Reserved subdirectory of `prompts/` for the future repair flow (no current contents)
- `prompts/system/` — Reserved subdirectory of `prompts/` for future graph-wide system prompts (no current contents)
- Human review UI

**Note on local directory state:** None of the planned subdirectories listed above should exist on disk until their corresponding build phase begins. Git does not track any of them — a fresh clone of this repo will not contain them. If your local working tree happens to contain empty directories for any of these (e.g. `orchestrator_v3/memory/`, `orchestrator_v3/prompts/repair/`, `orchestrator_v3/prompts/system/`), they are leftover cosmetic artifacts from earlier scaffolding work and can be safely removed with `rm -rf`. Do not add `.gitkeep` files or README stubs to them — that would promote cosmetic artifacts to tracked directories and contradict the "not here yet" framing above.

## When to build

See the readiness checklist in `docs/orchestration_v3_blueprint.md` Section 12.
Do not build v1 until:
1. Bakery Rush Pass 3 is complete (reflection beat tested)
2. Loop Purity Auditor has been run against all three current games
3. Misconception Architect produces its first real artifact

## Relationship to existing pipeline

The existing pipeline (`pipeline.py`, stages 0–8) remains the production
path. Orchestrator V3 is a parallel design that will eventually replace it.

The policies here (`gates.yaml`, `interaction_types.yaml`) are
the machine-readable source of truth for rules that currently live only in
agent prompts. They can be used immediately to validate existing artifacts
before the full graph is built.

## Connection to existing utilities

- `utils/loop_purity_auditor.py` → the `loop_purity_auditor` agent node
  wraps this for games at the code stage
- `utils/difficulty_ramp_auditor.py` → input to the Evaluation Subgraph
  (quantitative ramp check, not yet a named node)
- `artifacts/misconception_library/` → Memory Vault seed data; Misconception
  Architect reads and extends these entries
