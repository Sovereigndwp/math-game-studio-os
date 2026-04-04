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

    def gate_prototype_spec(self, artifact: Dict[str, Any]) -> Dict[str, Any]:
        valid, errors = self._validate_structure(
            artifact, "prototype_spec", expected_produced_by="Prototype Spec Agent"
        )
        if not valid:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact.get("job_id", "unknown"),
                    target_artifact="prototype_spec",
                    target_artifact_version=artifact.get("version", 0),
                    stage_name="prototype_spec",
                    status="revise",
                    failure_fields=["schema_validation"],
                    strongest_failure_reason="prototype_spec failed schema validation",
                    revision_instructions=errors,
                    escalation_recommendation="reroute",
                ),
            )

        # Gate dimensions (6 total):
        #   Reject-level (identity compromise):
        #     Dim 2 — Concept fidelity: interaction, family, loop structure
        #   Revise-level (fixable gaps):
        #     Dim 1 — Build clarity
        #     Dim 3 — Scope discipline
        #     Dim 4 — Loop integrity (field completeness)
        #     Dim 5 — Testability
        #     Dim 6 — Deferral quality

        # ---- Dim 2: Concept fidelity (reject-level) ----
        fidelity = artifact.get("concept_fidelity_check", {})
        if not fidelity.get("v1_interaction_type_preserved", False):
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="prototype_spec",
                    target_artifact_version=artifact["version"],
                    stage_name="prototype_spec",
                    status="reject",
                    failure_fields=["concept_fidelity_check.v1_interaction_type_preserved"],
                    strongest_failure_reason="Prototype drifts from V1-approved interaction type",
                    revision_instructions=["Restore the approved primary_interaction_type from the interaction_decision_memo."],
                    escalation_recommendation="reject_job",
                    memory_tags=["mechanic_drift"],
                ),
            )

        # ---- Dim 2 continued: Loop structure fidelity (reject-level) ----
        if not fidelity.get("v1_loop_structure_preserved", False):
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="prototype_spec",
                    target_artifact_version=artifact["version"],
                    stage_name="prototype_spec",
                    status="reject",
                    failure_fields=["concept_fidelity_check.v1_loop_structure_preserved"],
                    strongest_failure_reason="Prototype does not preserve the approved loop structure",
                    revision_instructions=["core_loop_translation must be a direct translation of lowest_viable_loop_brief, not a redesign."],
                    escalation_recommendation="reject_job",
                    memory_tags=["loop_integrity"],
                ),
            )

        # ---- Dim 2 continued: Family boundary fidelity (reject-level) ----
        if not fidelity.get("v1_family_boundary_respected", False):
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="prototype_spec",
                    target_artifact_version=artifact["version"],
                    stage_name="prototype_spec",
                    status="reject",
                    failure_fields=["concept_fidelity_check.v1_family_boundary_respected"],
                    strongest_failure_reason="Prototype violates V1-approved family boundary",
                    revision_instructions=["Restore family placement from family_architecture_brief."],
                    escalation_recommendation="reject_job",
                    memory_tags=["family_violation"],
                ),
            )

        # ---- Dim 2 continued: fidelity_notes must be non-empty ----
        fidelity_notes = fidelity.get("fidelity_notes", "").strip()
        if not fidelity_notes:
            failure_fields_fn = ["concept_fidelity_check.fidelity_notes"]
            revision_instructions_fn = [
                "concept_fidelity_check.fidelity_notes must contain a non-empty explanation of how fidelity was verified."
            ]
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="prototype_spec",
                    target_artifact_version=artifact["version"],
                    stage_name="prototype_spec",
                    status="revise",
                    failure_fields=failure_fields_fn,
                    strongest_failure_reason="Fidelity notes are empty — cannot verify concept alignment",
                    revision_instructions=revision_instructions_fn,
                    escalation_recommendation="revise_agent",
                    memory_tags=["fidelity_notes_missing"],
                ),
            )

        # ---- Dim 1: Build clarity (revise-level) ----
        failure_fields = []
        revision_instructions = []

        loop_trans = artifact.get("core_loop_translation", {})
        for field in [
            "player_goal_each_round",
            "first_visible_state",
            "first_player_action",
            "success_condition",
            "fail_condition",
            "signature_moment_delivery",
        ]:
            if not str(loop_trans.get(field, "")).strip():
                failure_fields.append(f"core_loop_translation.{field}")

        # Screen flow must be concrete
        screen_flow = artifact.get("screen_flow", [])
        if not screen_flow:
            failure_fields.append("screen_flow")
            revision_instructions.append("Define at least one screen with elements, actions, and exit condition.")

        # UI components must exist
        if not artifact.get("ui_components_required"):
            failure_fields.append("ui_components_required")
            revision_instructions.append("List the required UI components for the prototype.")

        # Build notes must have at least one must_build_first item
        build_notes = artifact.get("technical_build_notes", {})
        if not build_notes.get("must_build_first"):
            failure_fields.append("technical_build_notes.must_build_first")
            revision_instructions.append("Specify what must be built first vs. what can be faked.")

        if failure_fields:
            revision_instructions.insert(0, "Fill all core_loop_translation fields with concrete build language.")

        # ---- Dim 4: Loop integrity — field completeness (revise-level) ----
        if not str(loop_trans.get("signature_moment_delivery", "")).strip():
            if "core_loop_translation.signature_moment_delivery" not in failure_fields:
                failure_fields.append("core_loop_translation.signature_moment_delivery")
                revision_instructions.append("Preserve the signature moment from the approved loop.")
        if not str(loop_trans.get("reset_or_retry_behavior", "")).strip():
            failure_fields.append("core_loop_translation.reset_or_retry_behavior")
            revision_instructions.append("Define what happens on failure — retry/reset behavior must be explicit.")

        # ---- Dim 5: Testability (revise-level) ----
        playtest = artifact.get("playtest_plan", {})
        if not playtest.get("what_this_prototype_must_prove"):
            failure_fields.append("playtest_plan.what_this_prototype_must_prove")
            revision_instructions.append("Add at least one explicit thing the prototype must prove.")
        if not playtest.get("success_signals"):
            failure_fields.append("playtest_plan.success_signals")
            revision_instructions.append("Add observable success signals, not vague impressions.")
        if not playtest.get("failure_signals"):
            failure_fields.append("playtest_plan.failure_signals")
            revision_instructions.append("Add observable failure signals.")
        if not artifact.get("prototype_question", "").strip():
            failure_fields.append("prototype_question")
            revision_instructions.append("State the single most important question this prototype should answer.")
        if not artifact.get("prototype_goal", "").strip():
            failure_fields.append("prototype_goal")
            revision_instructions.append("State what this prototype is trying to accomplish.")

        # ---- Dim 3: Scope discipline (revise-level) ----
        scope = artifact.get("prototype_scope", {})
        if not scope.get("excluded"):
            failure_fields.append("prototype_scope.excluded")
            revision_instructions.append("List what is explicitly excluded from the prototype.")
        if not scope.get("included"):
            failure_fields.append("prototype_scope.included")
            revision_instructions.append("List what is included in the prototype scope.")

        # ---- Dim 6: Deferral quality (revise-level) ----
        if "deferred" not in scope:
            failure_fields.append("prototype_scope.deferred")
            revision_instructions.append("Separate deferred items from excluded items explicitly.")

        # Deferred and excluded must not overlap
        deferred_set = set(scope.get("deferred", []))
        excluded_set = set(scope.get("excluded", []))
        overlap = deferred_set & excluded_set
        if overlap:
            failure_fields.append("prototype_scope.deferred")
            revision_instructions.append(
                f"Items appear in both deferred and excluded: {sorted(overlap)}. "
                "Each item must be in exactly one list."
            )

        # ---- Readiness score sanity ----
        readiness = artifact.get("prototype_readiness_score", 0)
        if readiness < 0.5:
            failure_fields.append("prototype_readiness_score")
            revision_instructions.append("Readiness score below 0.5 indicates the spec is too underspecified to build.")

        # Deduplicate failure_fields
        failure_fields = list(dict.fromkeys(failure_fields))

        if failure_fields:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="prototype_spec",
                    target_artifact_version=artifact["version"],
                    stage_name="prototype_spec",
                    status="revise",
                    failure_fields=failure_fields,
                    strongest_failure_reason="Prototype spec is not yet build-ready — gaps in build clarity, testability, or scope discipline",
                    revision_instructions=revision_instructions,
                    escalation_recommendation="reroute",
                    memory_tags=["build_clarity", "prototype_gaps"],
                ),
            )

        return self._finalize_gate(
            artifact,
            _new_gate_decision(
                job_id=artifact["job_id"],
                target_artifact="prototype_spec",
                target_artifact_version=artifact["version"],
                stage_name="prototype_spec",
                status="pass",
            ),
        )


    def gate_prototype_build_spec(self, artifact: Dict[str, Any]) -> Dict[str, Any]:
        """Gate for prototype_build_spec — Stage 7.

        Six dimensions:
          Reject-level (identity compromise):
            Dim 2 — Prototype fidelity: build spec must implement the approved prototype
          Revise-level (fixable gaps):
            Dim 1 — Build concreteness
            Dim 3 — State clarity
            Dim 4 — Edge-case coverage
            Dim 5 — Scope discipline
            Dim 6 — Acceptance clarity
        """

        # ---- Dim 2: Prototype fidelity (reject-level) ----
        # The build spec must reference the same interaction and loop from prototype_spec.
        # In stub mode, this is guaranteed by template selection. In LLM mode, the gate
        # catches drift by checking structural presence.
        event_flow = artifact.get("interaction_event_flow", [])
        state_model = artifact.get("state_model", {})
        if not event_flow:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="prototype_build_spec",
                    target_artifact_version=artifact["version"],
                    stage_name="prototype_build_spec",
                    status="reject",
                    failure_fields=["interaction_event_flow"],
                    strongest_failure_reason="Build spec has no interaction event flow — cannot verify prototype fidelity",
                    revision_instructions=["interaction_event_flow must define the step-by-step event sequence for the approved loop."],
                    escalation_recommendation="reject_job",
                    memory_tags=["missing_event_flow"],
                ),
            )

        # ---- Dim 1: Build concreteness (revise-level) ----
        failure_fields = []
        revision_instructions = []

        # Event flow must have at least 3 steps (action, success path, failure path)
        if len(event_flow) < 3:
            failure_fields.append("interaction_event_flow")
            revision_instructions.append("Event flow must cover at minimum: player action, success path, and failure path (at least 3 steps).")

        for i, step in enumerate(event_flow):
            if not str(step.get("trigger", "")).strip():
                failure_fields.append(f"interaction_event_flow[{i}].trigger")
            if not str(step.get("system_response", "")).strip():
                failure_fields.append(f"interaction_event_flow[{i}].system_response")
            if not str(step.get("state_change", "")).strip():
                failure_fields.append(f"interaction_event_flow[{i}].state_change")

        # Component specs must exist and have behavior rules
        components = artifact.get("component_specs", [])
        if not components:
            failure_fields.append("component_specs")
            revision_instructions.append("At least one component spec with behavior rules is required.")
        for i, comp in enumerate(components):
            if not comp.get("behavior_rules"):
                failure_fields.append(f"component_specs[{i}].behavior_rules")
                revision_instructions.append(f"Component '{comp.get('component_name', i)}' must have concrete behavior rules.")

        # Screen state map must exist with transitions
        screen_states = artifact.get("screen_state_map", [])
        if not screen_states:
            failure_fields.append("screen_state_map")
            revision_instructions.append("At least one screen/state with transition rules is required.")
        for i, state in enumerate(screen_states):
            if not state.get("transition_rules"):
                failure_fields.append(f"screen_state_map[{i}].transition_rules")
                revision_instructions.append(f"State '{state.get('state_id', i)}' must have transition rules.")

        # Build sequence must have ordered steps and done definition
        build_seq = artifact.get("build_sequence", {})
        if not build_seq.get("phase_1_order"):
            failure_fields.append("build_sequence.phase_1_order")
            revision_instructions.append("Build sequence must list phase 1 tasks in dependency order.")
        if not build_seq.get("phase_1_done_definition"):
            failure_fields.append("build_sequence.phase_1_done_definition")
            revision_instructions.append("Define testable conditions for phase 1 completion.")

        if failure_fields:
            revision_instructions.append("Every event flow step must have trigger, system_response, and state_change.")

        # ---- Dim 3: State clarity (revise-level) ----
        tracked = state_model.get("tracked_variables", [])
        if not tracked:
            failure_fields.append("state_model.tracked_variables")
            revision_instructions.append("State model must list all tracked variables the prototype needs.")
        if not state_model.get("reset_rules"):
            failure_fields.append("state_model.reset_rules")
            revision_instructions.append("State model must define what resets between rounds.")

        # ---- Dim 4: Edge-case coverage (revise-level) ----
        edge_cases = artifact.get("edge_cases", [])
        if len(edge_cases) < 3:
            failure_fields.append("edge_cases")
            revision_instructions.append("At least 3 edge cases with explicit expected behavior are required.")

        # ---- Dim 5: Scope discipline (revise-level) ----
        scope = artifact.get("build_scope", {})
        if not scope.get("must_exist_in_v1_build"):
            failure_fields.append("build_scope.must_exist_in_v1_build")
            revision_instructions.append("Build scope must list what must exist in the first build.")
        if not scope.get("not_included_in_v1_build"):
            failure_fields.append("build_scope.not_included_in_v1_build")
            revision_instructions.append("Build scope must list what is explicitly not included.")

        # ---- Dim 6: Acceptance clarity (revise-level) ----
        checklist = artifact.get("acceptance_checklist", [])
        if not checklist:
            failure_fields.append("acceptance_checklist")
            revision_instructions.append("Acceptance checklist must list testable conditions for build completion.")

        # Deduplicate
        failure_fields = list(dict.fromkeys(failure_fields))

        if failure_fields:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="prototype_build_spec",
                    target_artifact_version=artifact["version"],
                    stage_name="prototype_build_spec",
                    status="revise",
                    failure_fields=failure_fields,
                    strongest_failure_reason="Build spec is not yet developer-ready — gaps in concreteness, state clarity, or acceptance criteria",
                    revision_instructions=revision_instructions,
                    escalation_recommendation="reroute",
                    memory_tags=["build_concreteness", "build_spec_gaps"],
                ),
            )

        return self._finalize_gate(
            artifact,
            _new_gate_decision(
                job_id=artifact["job_id"],
                target_artifact="prototype_build_spec",
                target_artifact_version=artifact["version"],
                stage_name="prototype_build_spec",
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
