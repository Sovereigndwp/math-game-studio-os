# Current Implementation Status
## Last updated: 2026-04-03

---

## Already implemented

### Core engine (complete)
- `utils/validation.py` — schema loading, artifact versioning, write_validated_artifact
- `orchestrator/stage_ledger.py` — StageLedger, initialize, update_stage_ledger_for_artifact
- `engine/gate_engine.py` — all six gate methods (request_brief through lowest_viable_loop_brief)
- `utils/shared_agent_runner.py` — SharedAgentRunner, AgentSpec, AgentRunResult

### Orchestrator (complete)
- `orchestrator/orchestrator.py` — build_request_brief, create_request_brief, route_after_gate,
  initialize_job_workspace, get_authoritative_artifact_path, focus conflict detection

### Agent wrappers (all six complete as stubs)
- `agents/intake_framing/agent.py` + config.yaml + prompt.md ✅
- `agents/kill_test/agent.py` + config.yaml + prompt.md ✅
- `agents/interaction_mapper/agent.py` + config.yaml + prompt.md ✅
- `agents/family_architect/agent.py` + config.yaml + prompt.md ✅
- `agents/core_loop/agent.py` + config.yaml + prompt.md ✅

### Pipeline runner (complete)
- `pipeline.py` — end-to-end V1 runner with gate pre-condition enforcement and revision limits

### Artifact schemas (all six complete)
- request_brief, intake_brief, kill_report, interaction_decision_memo,
  family_architecture_brief, lowest_viable_loop_brief, gate_decision, stage_ledger

### System docs and governance (complete)
- routing_rules.yaml, agent_stack_overview.md, artifact_flow_map.md, gate_rules.yaml,
  field_definitions.md, output_rules.md, human_override_policy.md, tool_boundary.md

---

## Known open issues (not blocking V1 execution, but should be addressed before benchmark run)

### File structure issue
The blueprint source files use colon-separated flat names (e.g., `agents:kill_test:agent.py`).
Python imports require directory structure (`agents/kill_test/agent.py`).
All new files in `Master Gaming App and OS/` use proper directory structure.
The flat-named files in `Math Game Factory Blueprint_files/` must be reorganized before running tests.

### SharedAgentRunner does not enforce gate pre-conditions
`config.yaml` files declare `requires_gate_pass_from:` but SharedAgentRunner never reads this field.
Gate enforcement currently lives in `pipeline.py` only.
This is acceptable for V1 but should be hardened.

### Orchestrator auto-passes request_brief
`create_request_brief` sets gate_status="pass" without calling gate_engine.gate_request_brief().
The pipeline then re-gates it. This double-path should be resolved to single-authority gating.

### interaction_decision_memo secondary_interaction_type schema gap
`secondary_interaction_type` is required in the schema but has no enum constraint.
A bad secondary type passes schema validation. The gate does not check this.

---

## Not yet implemented (V1 complete — these are post-V1)
- prompt fragment merger
- registry promotion automation (agents propose, Orchestrator approves — write path only)
- prototype builder
- later design layer agents (post V1 scope)
- production layer agents
- release automation

---

## Current recommended next step
Run the benchmark set through `pipeline.py`:
- 3 strong concepts — verify they reach approved `lowest_viable_loop_brief`
- 2 weak concepts — verify they are rejected with traceable reasons

Then address the file structure issue by reorganizing the flat-named blueprint files
into the proper `agents/`, `orchestrator/`, `utils/`, and `engine/` directory structure
so that all imports resolve and the test suite runs cleanly.
