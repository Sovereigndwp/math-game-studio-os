"""
pipeline.py — Math Game Studio OS V1 end-to-end runner.

Chains all six V1 agents in order, enforces gate pre-conditions between each stage,
and returns a PipelineResult with the final outcome.

Modes:
    Stub mode (default):
        run_v1_pipeline(raw_command, repo_root)
        Uses deterministic keyword-matching stubs. Fast, no API key needed.
        Use for development, testing, and benchmark runs.

    LLM mode:
        from utils.llm_caller import make_claude_callable
        callable = make_claude_callable(model="claude-sonnet-4-6")
        run_v1_pipeline(raw_command, repo_root, model_callable=callable)
        Drives every agent through Claude. Requires ANTHROPIC_API_KEY.
        Use for production concept validation.

Usage:
    from pathlib import Path
    from pipeline import run_v1_pipeline

    result = run_v1_pipeline(
        raw_command="Create a grade 2 bakery game for addition to 20.",
        repo_root=Path("."),
    )
    print(result.outcome)
    print(result.final_artifact_path)
"""
from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

from orchestrator.orchestrator import Orchestrator, OrchestratorConfig
from orchestrator.stage_ledger import initialize_stage_ledger
from engine.gate_engine import GateEngine
from agents.intake_framing.agent import run as run_intake
from agents.kill_test.agent import run as run_kill
from agents.interaction_mapper.agent import run as run_interaction_mapper
from agents.family_architect.agent import run as run_family_architect
from agents.core_loop.agent import run as run_core_loop
from agents.prototype_spec.agent import run as run_prototype_spec
from utils.shared_agent_runner import AgentRunResult


# ---------------------------------------------------------------------------
# Pipeline result types
# ---------------------------------------------------------------------------


@dataclass
class StageRecord:
    stage_name: str
    artifact_path: str
    gate_status: str
    gate_artifact_path: str
    version: int


@dataclass
class PipelineResult:
    job_id: str
    outcome: str  # "approved" | "rejected" | "stalled"
    final_artifact_name: str
    final_artifact_path: Optional[str]
    stage_records: List[StageRecord] = field(default_factory=list)
    rejection_reason: str = ""
    error: str = ""


# ---------------------------------------------------------------------------
# Gate pre-condition enforcer
# ---------------------------------------------------------------------------


class GatePreConditionError(Exception):
    """Raised when an agent is about to run but the previous gate did not pass."""


def _enforce_gate_precondition(stage_name: str, gate_decision: Dict[str, Any]) -> None:
    """Raise GatePreConditionError if gate_decision.status is not 'pass'."""
    status = gate_decision.get("status", "unknown")
    if status != "pass":
        raise GatePreConditionError(
            f"Stage '{stage_name}' cannot run: previous gate returned '{status}'. "
            f"Reason: {gate_decision.get('strongest_failure_reason', 'none')}."
        )


# ---------------------------------------------------------------------------
# Revision limit enforcer
# ---------------------------------------------------------------------------


def _revision_limit_exceeded(stage_ledger_path: Path, artifact_name: str, max_revisions: int = 2) -> bool:
    """Return True if the revision count for artifact_name has reached the limit."""
    if not stage_ledger_path.exists():
        return False
    data = json.loads(stage_ledger_path.read_text(encoding="utf-8"))
    counts = data.get("revision_counts", {})
    return counts.get(artifact_name, 0) >= max_revisions


# ---------------------------------------------------------------------------
# Main pipeline runner
# ---------------------------------------------------------------------------


def run_v1_pipeline(
    raw_command: str,
    repo_root: Path,
    job_id: Optional[str] = None,
    max_revisions_per_stage: int = 2,
    model_callable: Optional[Callable] = None,
) -> PipelineResult:
    """
    Run the full pipeline (V1 + V2 stages).

    Stages:
        0. Orchestrator      → request_brief              → gate_request_brief
        1. IntakeFraming     → intake_brief               → gate_intake_brief
        2. KillTest          → kill_report                → gate_kill_report
        3. InteractionMapper → interaction_decision_memo   → gate_interaction_decision_memo
        4. FamilyArchitect   → family_architecture_brief   → gate_family_architecture_brief
        5. CoreLoop          → lowest_viable_loop_brief    → gate_lowest_viable_loop_brief
        6. PrototypeSpec     → prototype_spec              → gate_prototype_spec

    Gate pre-conditions are enforced: no agent runs unless the previous gate returned 'pass'.
    Revision limits are enforced: if a stage exceeds max_revisions, the job is rejected.

    Args:
        model_callable: If provided, all agents run in LLM mode using this callable.
                        Build with: utils.llm_caller.make_claude_callable()
                        If None (default), all agents use their deterministic stubs.
    """
    config = OrchestratorConfig(repo_root=repo_root)
    orchestrator = Orchestrator(config)
    gate_engine = GateEngine(repo_root)
    stage_records: List[StageRecord] = []

    # Convenience: each agent runner closes over the model_callable
    mc = model_callable  # None → stub mode; Callable → LLM mode

    # ------------------------------------------------------------------
    # Stage 0: Orchestrator → request_brief
    # (Always deterministic — Orchestrator classification is code, not LLM)
    # ------------------------------------------------------------------
    request_brief = orchestrator.create_request_brief(raw_command, job_id=job_id)
    job_id = request_brief["job_id"]
    workspace = config.workspace_root / job_id
    ledger_path = workspace / "stage_ledger.json"

    rb_version = request_brief["version"]
    rb_path = workspace / f"request_brief.v{rb_version}.json"

    gate_rb = gate_engine.gate_request_brief(request_brief)
    _record_stage(stage_records, "request_brief", str(rb_path), gate_rb, rb_version, workspace)

    if gate_rb["status"] != "pass":
        return PipelineResult(
            job_id=job_id,
            outcome="rejected",
            final_artifact_name="request_brief",
            final_artifact_path=str(rb_path),
            stage_records=stage_records,
            rejection_reason=gate_rb.get("strongest_failure_reason", "request_brief gate failed"),
        )

    # ------------------------------------------------------------------
    # Stage 1: Intake and Framing Agent → intake_brief
    # ------------------------------------------------------------------
    intake_result, gate_ib = _run_agent_with_gate(
        stage_name="intake_brief",
        agent_runner=lambda artifact_paths: run_intake(repo_root, job_id, artifact_paths, model_callable=mc),
        gate_fn=gate_engine.gate_intake_brief,
        artifact_paths={"request_brief": rb_path},
        stage_records=stage_records,
        workspace=workspace,
        ledger_path=ledger_path,
        max_revisions=max_revisions_per_stage,
    )
    if gate_ib["status"] != "pass":
        return _rejected_result(job_id, "intake_brief", intake_result, gate_ib, stage_records)

    intake_path = Path(intake_result.artifact_path)

    # ------------------------------------------------------------------
    # Stage 2: Kill Test Agent → kill_report
    # ------------------------------------------------------------------
    kill_result, gate_kr = _run_agent_with_gate(
        stage_name="kill_report",
        agent_runner=lambda artifact_paths: run_kill(repo_root, job_id, artifact_paths, model_callable=mc),
        gate_fn=gate_engine.gate_kill_report,
        artifact_paths={"intake_brief": intake_path},
        stage_records=stage_records,
        workspace=workspace,
        ledger_path=ledger_path,
        max_revisions=max_revisions_per_stage,
    )
    if gate_kr["status"] != "pass":
        return _rejected_result(job_id, "kill_report", kill_result, gate_kr, stage_records)

    kill_path = Path(kill_result.artifact_path)

    # ------------------------------------------------------------------
    # Stage 3: Interaction Mapper Agent → interaction_decision_memo
    # ------------------------------------------------------------------
    mapper_result, gate_idm = _run_agent_with_gate(
        stage_name="interaction_decision_memo",
        agent_runner=lambda artifact_paths: run_interaction_mapper(repo_root, job_id, artifact_paths, model_callable=mc),
        gate_fn=gate_engine.gate_interaction_decision_memo,
        artifact_paths={"intake_brief": intake_path, "kill_report": kill_path},
        stage_records=stage_records,
        workspace=workspace,
        ledger_path=ledger_path,
        max_revisions=max_revisions_per_stage,
    )
    if gate_idm["status"] != "pass":
        return _rejected_result(job_id, "interaction_decision_memo", mapper_result, gate_idm, stage_records)

    mapper_path = Path(mapper_result.artifact_path)

    # ------------------------------------------------------------------
    # Stage 4: Family Architect Agent → family_architecture_brief
    # ------------------------------------------------------------------
    family_result, gate_fab = _run_agent_with_gate(
        stage_name="family_architecture_brief",
        agent_runner=lambda artifact_paths: run_family_architect(repo_root, job_id, artifact_paths, model_callable=mc),
        gate_fn=gate_engine.gate_family_architecture_brief,
        artifact_paths={"intake_brief": intake_path, "interaction_decision_memo": mapper_path},
        stage_records=stage_records,
        workspace=workspace,
        ledger_path=ledger_path,
        max_revisions=max_revisions_per_stage,
    )
    if gate_fab["status"] != "pass":
        return _rejected_result(job_id, "family_architecture_brief", family_result, gate_fab, stage_records)

    family_path = Path(family_result.artifact_path)

    # ------------------------------------------------------------------
    # Stage 5: Core Loop Agent → lowest_viable_loop_brief
    # ------------------------------------------------------------------
    loop_result, gate_lvlb = _run_agent_with_gate(
        stage_name="lowest_viable_loop_brief",
        agent_runner=lambda artifact_paths: run_core_loop(repo_root, job_id, artifact_paths, model_callable=mc),
        gate_fn=gate_engine.gate_lowest_viable_loop_brief,
        artifact_paths={
            "intake_brief": intake_path,
            "interaction_decision_memo": mapper_path,
            "family_architecture_brief": family_path,
        },
        stage_records=stage_records,
        workspace=workspace,
        ledger_path=ledger_path,
        max_revisions=max_revisions_per_stage,
    )
    if gate_lvlb["status"] != "pass":
        return _rejected_result(job_id, "lowest_viable_loop_brief", loop_result, gate_lvlb, stage_records)

    loop_path = Path(loop_result.artifact_path)

    # ------------------------------------------------------------------
    # Stage 6: Prototype Spec Agent → prototype_spec
    # ------------------------------------------------------------------
    proto_result, gate_ps = _run_agent_with_gate(
        stage_name="prototype_spec",
        agent_runner=lambda artifact_paths: run_prototype_spec(repo_root, job_id, artifact_paths, model_callable=mc),
        gate_fn=gate_engine.gate_prototype_spec,
        artifact_paths={
            "intake_brief": intake_path,
            "interaction_decision_memo": mapper_path,
            "family_architecture_brief": family_path,
            "lowest_viable_loop_brief": loop_path,
        },
        stage_records=stage_records,
        workspace=workspace,
        ledger_path=ledger_path,
        max_revisions=max_revisions_per_stage,
    )
    if gate_ps["status"] != "pass":
        return _rejected_result(job_id, "prototype_spec", proto_result, gate_ps, stage_records)

    # ------------------------------------------------------------------
    # Pipeline success: approved prototype_spec
    # ------------------------------------------------------------------
    return PipelineResult(
        job_id=job_id,
        outcome="approved",
        final_artifact_name="prototype_spec",
        final_artifact_path=proto_result.artifact_path,
        stage_records=stage_records,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _run_agent_with_gate(
    stage_name: str,
    agent_runner,
    gate_fn,
    artifact_paths: Dict[str, Path],
    stage_records: List[StageRecord],
    workspace: Path,
    ledger_path: Path,
    max_revisions: int,
):
    """Run an agent, then run its gate. Return (AgentRunResult, gate_decision_dict)."""
    # Revision limit guard
    if _revision_limit_exceeded(ledger_path, stage_name, max_revisions):
        # Build a synthetic gate rejection to surface it
        synthetic_gate = {
            "job_id": "unknown",
            "status": "reject",
            "target_artifact": stage_name,
            "strongest_failure_reason": (
                f"Revision limit ({max_revisions}) exceeded for '{stage_name}'. Job rejected."
            ),
        }
        return None, synthetic_gate

    result: AgentRunResult = agent_runner(artifact_paths)
    gate_decision = gate_fn(result.artifact)

    version = result.artifact_version
    artifact_path = result.artifact_path
    gate_artifact_path = str(workspace / f"gate_decision.v{gate_decision.get('version', 1)}.json")

    _record_stage(stage_records, stage_name, artifact_path, gate_decision, version, workspace)
    return result, gate_decision


def _record_stage(
    stage_records: List[StageRecord],
    stage_name: str,
    artifact_path: str,
    gate_decision: Dict[str, Any],
    version: int,
    workspace: Path,
) -> None:
    gate_version = gate_decision.get("version", 1)
    stage_records.append(
        StageRecord(
            stage_name=stage_name,
            artifact_path=str(artifact_path),
            gate_status=gate_decision.get("status", "unknown"),
            gate_artifact_path=str(workspace / f"gate_decision.v{gate_version}.json"),
            version=version,
        )
    )


def _rejected_result(
    job_id: str,
    stage_name: str,
    agent_result: Optional[AgentRunResult],
    gate_decision: Dict[str, Any],
    stage_records: List[StageRecord],
) -> PipelineResult:
    return PipelineResult(
        job_id=job_id,
        outcome="rejected",
        final_artifact_name=stage_name,
        final_artifact_path=agent_result.artifact_path if agent_result else None,
        stage_records=stage_records,
        rejection_reason=gate_decision.get("strongest_failure_reason", f"{stage_name} gate did not pass"),
    )


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------


if __name__ == "__main__":
    import os
    import sys

    repo_root = Path(__file__).resolve().parent

    command = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else (
        "Create a grade 2 bakery game for addition to 20 "
        "where students pack pastry orders before customers leave."
    )

    # LLM mode: set ANTHROPIC_API_KEY env var and pass --llm flag
    use_llm = "--llm" in sys.argv
    mc = None
    if use_llm:
        from utils.llm_caller import make_claude_callable
        mc = make_claude_callable(model="claude-sonnet-4-6")
        print("Mode: LLM (claude-sonnet-4-6)")
    else:
        print("Mode: Stub (deterministic — pass --llm to use Claude API)")

    print(f"\n=== Math Game Studio OS — V1 Pipeline ===")
    print(f"Command: {command}\n")

    result = run_v1_pipeline(raw_command=command, repo_root=repo_root, model_callable=mc)

    print(f"Job ID:   {result.job_id}")
    print(f"Outcome:  {result.outcome.upper()}")
    if result.rejection_reason:
        print(f"Rejected: {result.rejection_reason}")
    if result.final_artifact_path:
        print(f"Final artifact: {result.final_artifact_path}")

    print("\nStage summary:")
    for record in result.stage_records:
        symbol = "✓" if record.gate_status == "pass" else ("✗" if record.gate_status == "reject" else "~")
        print(f"  {symbol} {record.stage_name} v{record.version} → gate: {record.gate_status}")

    if result.outcome == "approved":
        print(f"\nPIPELINE COMPLETE — {result.final_artifact_name} approved.")
