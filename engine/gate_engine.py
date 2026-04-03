from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

from orchestrator.stage_ledger import update_stage_ledger_for_artifact
from utils.validation import (
    ValidationErrorBundle,
    next_artifact_version,
    validate_artifact,
    write_validated_artifact,
)


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _new_gate_decision(
    job_id: str,
    target_artifact: str,
    target_artifact_version: int,
    stage_name: str,
    status: str,
    failure_fields: List[str] | None = None,
    strongest_failure_reason: str = "",
    revision_instructions: List[str] | None = None,
    escalation_recommendation: str = "continue",
    memory_tags: List[str] | None = None,
    version: int = 1,
) -> Dict[str, Any]:
    return {
        "job_id": job_id,
        "artifact_name": "gate_decision",
        "version": version,
        "status": status,
        "produced_by": "Quality Gate Engine",
        "timestamp": utc_now_iso(),
        "target_artifact": target_artifact,
        "target_artifact_version": target_artifact_version,
        "stage_name": stage_name,
        "failure_fields": failure_fields or [],
        "strongest_failure_reason": strongest_failure_reason,
        "revision_instructions": revision_instructions or [],
        "escalation_recommendation": escalation_recommendation,
        "memory_tags": memory_tags or [],
    }


class GateEngine:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.schema_dir = repo_root / "artifacts" / "schemas"

    def _workspace(self, job_id: str) -> Path:
        path = self.repo_root / "memory" / "job_workspaces" / job_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def _ledger_path(self, job_id: str) -> Path:
        return self._workspace(job_id) / "stage_ledger.json"

    def _write_gate_decision(self, workspace: Path, gate_decision: Dict[str, Any]) -> Path:
        gate_decision["version"] = next_artifact_version(workspace, "gate_decision")
        return write_validated_artifact(
            job_workspace=workspace,
            artifact=gate_decision,
            schema_dir=self.schema_dir,
            expected_artifact_name="gate_decision",
            expected_produced_by="Quality Gate Engine",
        )

    def _validate_structure(
        self,
        artifact: Dict[str, Any],
        expected_artifact_name: str,
        expected_produced_by: str | None = None,
    ) -> Tuple[bool, List[str]]:
        return validate_artifact(
            artifact=artifact,
            schema_dir=self.schema_dir,
            expected_artifact_name=expected_artifact_name,
            expected_produced_by=expected_produced_by,
        )

    def _finalize_gate(
        self,
        artifact: Dict[str, Any],
        gate_decision: Dict[str, Any],
    ) -> Dict[str, Any]:
        workspace = self._workspace(artifact["job_id"])
        self._write_gate_decision(workspace, gate_decision)
        update_stage_ledger_for_artifact(
            ledger_path=self._ledger_path(artifact["job_id"]),
            artifact_name=artifact["artifact_name"],
            gate_status=gate_decision["status"],
            version=artifact["version"],
            revise_increments=True,
        )
        return gate_decision

    def gate_request_brief(self, artifact: Dict[str, Any]) -> Dict[str, Any]:
        valid, errors = self._validate_structure(
            artifact, "request_brief", expected_produced_by="Orchestrator"
        )
        if not valid:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact.get("job_id", "unknown"),
                    target_artifact="request_brief",
                    target_artifact_version=artifact.get("version", 0),
                    stage_name="request_brief",
                    status="revise",
                    failure_fields=["schema_validation"],
                    strongest_failure_reason="request_brief failed schema validation",
                    revision_instructions=errors,
                    escalation_recommendation="reroute",
                ),
            )

        failure_fields = []
        if not artifact.get("notes_for_routing", "").strip():
            failure_fields.append("notes_for_routing")
        if artifact.get("request_type") not in {"new_game", "family_extension", "prototype_only", "production_upgrade", "audit"}:
            failure_fields.append("request_type")

        if failure_fields:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="request_brief",
                    target_artifact_version=artifact["version"],
                    stage_name="request_brief",
                    status="revise",
                    failure_fields=failure_fields,
                    strongest_failure_reason="request_brief missing routing clarity",
                    revision_instructions=["Clarify request_type and routing notes."],
                    escalation_recommendation="reroute",
                ),
            )

        return self._finalize_gate(
            artifact,
            _new_gate_decision(
                job_id=artifact["job_id"],
                target_artifact="request_brief",
                target_artifact_version=artifact["version"],
                stage_name="request_brief",
                status="pass",
            ),
        )

    def gate_intake_brief(self, artifact: Dict[str, Any]) -> Dict[str, Any]:
        valid, errors = self._validate_structure(
            artifact, "intake_brief", expected_produced_by="Intake and Framing Agent"
        )
        if not valid:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact.get("job_id", "unknown"),
                    target_artifact="intake_brief",
                    target_artifact_version=artifact.get("version", 0),
                    stage_name="intake_brief",
                    status="revise",
                    failure_fields=["schema_validation"],
                    strongest_failure_reason="intake_brief failed schema validation",
                    revision_instructions=errors,
                    escalation_recommendation="reroute",
                ),
            )

        failure_fields = []
        for field in [
            "plain_english_concept",
            "likely_age_band",
            "likely_math_domain",
            "one_sentence_promise_draft",
            "possible_profession_or_mission",
        ]:
            if not str(artifact.get(field, "")).strip():
                failure_fields.append(field)

        if failure_fields:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="intake_brief",
                    target_artifact_version=artifact["version"],
                    stage_name="intake_brief",
                    status="revise",
                    failure_fields=failure_fields,
                    strongest_failure_reason="intake_brief is too vague for fair evaluation",
                    revision_instructions=["Strengthen the one sentence promise, concept framing, and mission."],
                    escalation_recommendation="reroute",
                    memory_tags=["ambiguity"],
                ),
            )

        return self._finalize_gate(
            artifact,
            _new_gate_decision(
                job_id=artifact["job_id"],
                target_artifact="intake_brief",
                target_artifact_version=artifact["version"],
                stage_name="intake_brief",
                status="pass",
            ),
        )

    def gate_kill_report(self, artifact: Dict[str, Any]) -> Dict[str, Any]:
        valid, errors = self._validate_structure(
            artifact, "kill_report", expected_produced_by="Kill Test Agent"
        )
        if not valid:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact.get("job_id", "unknown"),
                    target_artifact="kill_report",
                    target_artifact_version=artifact.get("version", 0),
                    stage_name="kill_report",
                    status="revise",
                    failure_fields=["schema_validation"],
                    strongest_failure_reason="kill_report failed schema validation",
                    revision_instructions=errors,
                    escalation_recommendation="reroute",
                ),
            )

        if artifact["status"] == "reject":
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="kill_report",
                    target_artifact_version=artifact["version"],
                    stage_name="kill_report",
                    status="reject",
                    strongest_failure_reason=artifact.get("strongest_failure_reason", "Kill Fast reject"),
                    revision_instructions=[],
                    escalation_recommendation="reject_job",
                    memory_tags=["kill_fast_reject"],
                ),
            )

        failure_fields = []
        if not artifact.get("final_decision_note", "").strip():
            failure_fields.append("final_decision_note")
        if artifact["status"] == "redesign" and not artifact.get("redesign_direction", "").strip():
            failure_fields.append("redesign_direction")

        if failure_fields:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="kill_report",
                    target_artifact_version=artifact["version"],
                    stage_name="kill_report",
                    status="revise",
                    failure_fields=failure_fields,
                    strongest_failure_reason="kill_report lacks concrete decision support",
                    revision_instructions=["Add clear redesign direction or final decision note."],
                    escalation_recommendation="reroute",
                ),
            )

        if artifact["status"] == "redesign":
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="kill_report",
                    target_artifact_version=artifact["version"],
                    stage_name="kill_report",
                    status="revise",
                    failure_fields=["concept_strength"],
                    strongest_failure_reason=artifact.get("strongest_failure_reason", "Concept needs redesign"),
                    revision_instructions=[artifact.get("redesign_direction", "Redesign concept and rerun Kill Fast.")],
                    escalation_recommendation="reroute",
                ),
            )

        return self._finalize_gate(
            artifact,
            _new_gate_decision(
                job_id=artifact["job_id"],
                target_artifact="kill_report",
                target_artifact_version=artifact["version"],
                stage_name="kill_report",
                status="pass",
            ),
        )

    def gate_interaction_decision_memo(self, artifact: Dict[str, Any]) -> Dict[str, Any]:
        valid, errors = self._validate_structure(
            artifact, "interaction_decision_memo", expected_produced_by="Interaction Mapper Agent"
        )
        if not valid:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact.get("job_id", "unknown"),
                    target_artifact="interaction_decision_memo",
                    target_artifact_version=artifact.get("version", 0),
                    stage_name="interaction_decision_memo",
                    status="revise",
                    failure_fields=["schema_validation"],
                    strongest_failure_reason="interaction_decision_memo failed schema validation",
                    revision_instructions=errors,
                    escalation_recommendation="reroute",
                ),
            )

        if artifact.get("interaction_purity_score", 0) < 0.6:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="interaction_decision_memo",
                    target_artifact_version=artifact["version"],
                    stage_name="interaction_decision_memo",
                    status="reject",
                    strongest_failure_reason="interaction purity too weak",
                    revision_instructions=["Choose an interaction where the action itself carries the math."],
                    escalation_recommendation="reject_job",
                    memory_tags=["interaction_mismatch"],
                ),
            )

        failure_fields = []
        if not artifact.get("interaction_justification", "").strip():
            failure_fields.append("interaction_justification")
        if artifact.get("split_family_warning") not in {True, False}:
            failure_fields.append("split_family_warning")

        if failure_fields:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="interaction_decision_memo",
                    target_artifact_version=artifact["version"],
                    stage_name="interaction_decision_memo",
                    status="revise",
                    failure_fields=failure_fields,
                    strongest_failure_reason="interaction decision lacks enough reasoning clarity",
                    revision_instructions=["Strengthen the interaction justification and overload analysis."],
                    escalation_recommendation="reroute",
                ),
            )

        return self._finalize_gate(
            artifact,
            _new_gate_decision(
                job_id=artifact["job_id"],
                target_artifact="interaction_decision_memo",
                target_artifact_version=artifact["version"],
                stage_name="interaction_decision_memo",
                status="pass",
            ),
        )

    def gate_family_architecture_brief(self, artifact: Dict[str, Any]) -> Dict[str, Any]:
        valid, errors = self._validate_structure(
            artifact, "family_architecture_brief", expected_produced_by="Family Architect Agent"
        )
        if not valid:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact.get("job_id", "unknown"),
                    target_artifact="family_architecture_brief",
                    target_artifact_version=artifact.get("version", 0),
                    stage_name="family_architecture_brief",
                    status="revise",
                    failure_fields=["schema_validation"],
                    strongest_failure_reason="family_architecture_brief failed schema validation",
                    revision_instructions=errors,
                    escalation_recommendation="reroute",
                ),
            )

        failure_fields = []
        for field in ["family_name", "reason_for_family_placement", "family_growth_path", "family_boundary_rule", "boundary_break_example"]:
            if not str(artifact.get(field, "")).strip():
                failure_fields.append(field)

        if failure_fields:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="family_architecture_brief",
                    target_artifact_version=artifact["version"],
                    stage_name="family_architecture_brief",
                    status="revise",
                    failure_fields=failure_fields,
                    strongest_failure_reason="family architecture is missing critical boundary or placement logic",
                    revision_instructions=["Define family placement, growth path, and stopping point clearly."],
                    escalation_recommendation="reroute",
                ),
            )

        return self._finalize_gate(
            artifact,
            _new_gate_decision(
                job_id=artifact["job_id"],
                target_artifact="family_architecture_brief",
                target_artifact_version=artifact["version"],
                stage_name="family_architecture_brief",
                status="pass",
            ),
        )

    def gate_lowest_viable_loop_brief(self, artifact: Dict[str, Any]) -> Dict[str, Any]:
        valid, errors = self._validate_structure(
            artifact, "lowest_viable_loop_brief", expected_produced_by="Core Loop Agent"
        )
        if not valid:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact.get("job_id", "unknown"),
                    target_artifact="lowest_viable_loop_brief",
                    target_artifact_version=artifact.get("version", 0),
                    stage_name="lowest_viable_loop_brief",
                    status="revise",
                    failure_fields=["schema_validation"],
                    strongest_failure_reason="lowest_viable_loop_brief failed schema validation",
                    revision_instructions=errors,
                    escalation_recommendation="reroute",
                ),
            )

        failure_fields = []
        if not artifact.get("first_60_seconds_flow", "").strip():
            failure_fields.append("first_60_seconds_flow")
        if not artifact.get("signature_moment", "").strip():
            failure_fields.append("signature_moment")
        if artifact.get("max_steps_per_loop", 99) > 5:
            failure_fields.append("max_steps_per_loop")
        if not artifact.get("core_loop_map", {}).get("first_correct_action", "").strip():
            failure_fields.append("core_loop_map.first_correct_action")

        if failure_fields:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="lowest_viable_loop_brief",
                    target_artifact_version=artifact["version"],
                    stage_name="lowest_viable_loop_brief",
                    status="revise",
                    failure_fields=failure_fields,
                    strongest_failure_reason="lowest viable loop is not yet clear or bounded enough",
                    revision_instructions=["Tighten the first minute, first correct action, and signature moment."],
                    escalation_recommendation="reroute",
                    memory_tags=["loop_clarity"],
                ),
            )

        return self._finalize_gate(
            artifact,
            _new_gate_decision(
                job_id=artifact["job_id"],
                target_artifact="lowest_viable_loop_brief",
                target_artifact_version=artifact["version"],
                stage_name="lowest_viable_loop_brief",
                status="pass",
            ),
        )


if __name__ == "__main__":
    import json
    from pathlib import Path
    from utils.validation import load_json

    repo_root = Path(__file__).resolve().parents[1]
    engine = GateEngine(repo_root)
    fixture = load_json(repo_root / "tests" / "fixtures" / "valid" / "request_brief.valid.json")
    workspace = repo_root / "memory" / "job_workspaces" / fixture["job_id"]
    workspace.mkdir(parents=True, exist_ok=True)
    print(json.dumps(engine.gate_request_brief(fixture), indent=2))
