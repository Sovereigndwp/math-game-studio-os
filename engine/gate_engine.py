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

        Seven dimensions:
          Reject-level (identity compromise):
            Dim 2 — Prototype fidelity: build spec must implement the approved prototype
          Revise-level (fixable gaps):
            Dim 1 — Build concreteness
            Dim 3 — State clarity
            Dim 4 — Edge-case coverage
            Dim 5 — Scope discipline
            Dim 6 — Acceptance clarity
            Dim 7 — Internal consistency: cross-section coherence
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

        # Deferred and not-included must not overlap
        deferred_set = set(scope.get("deferred_from_prototype", []))
        not_included_set = set(scope.get("not_included_in_v1_build", []))
        overlap = deferred_set & not_included_set
        if overlap:
            failure_fields.append("build_scope.deferred_from_prototype")
            revision_instructions.append(
                f"Items appear in both deferred_from_prototype and not_included_in_v1_build: {sorted(overlap)}. "
                "Each item must be in exactly one list."
            )

        # ---- Dim 6: Acceptance clarity (revise-level) ----
        checklist = artifact.get("acceptance_checklist", [])
        if not checklist:
            failure_fields.append("acceptance_checklist")
            revision_instructions.append("Acceptance checklist must list testable conditions for build completion.")

        # ---- Dim 7: Internal consistency (revise-level) ----
        # Component names referenced in event flow must appear in component_specs.
        component_names = {c.get("component_name", "") for c in components}
        for i, step in enumerate(event_flow):
            response = str(step.get("system_response", ""))
            # Check if the step references a component name that isn't in component_specs.
            # Only flag if a clearly named component (containing "Component" or ending in
            # a capitalized noun phrase) appears in the response but is absent from specs.
            # Conservative check: only flag if a component_spec name appears in the
            # response text that is NOT in the component_specs list (catches renames/drift).
            # Positive check: every component in component_specs should appear somewhere in the event flow.
        all_flow_text = " ".join(
            str(step.get("trigger", "")) + " " + str(step.get("system_response", "")) + " " + str(step.get("state_change", ""))
            for step in event_flow
        )

        # Check that every tracked variable in state_model appears somewhere in the event flow.
        for var in tracked:
            # Extract the variable name (first token before colon or space)
            var_name = var.split(":")[0].split(" ")[0].strip()
            if var_name and len(var_name) > 3 and var_name.lower() not in all_flow_text.lower():
                failure_fields.append("state_model.tracked_variables")
                revision_instructions.append(
                    f"Tracked variable '{var_name}' does not appear in the interaction event flow. "
                    "State model and event flow must be consistent."
                )
                break  # One instance is enough to flag the issue

        # Check that acceptance checklist items do not reference features outside build scope.
        must_exist_text = " ".join(scope.get("must_exist_in_v1_build", [])).lower()
        not_included_text = " ".join(scope.get("not_included_in_v1_build", [])).lower()
        deferred_text = " ".join(scope.get("deferred_from_prototype", [])).lower()
        excluded_text = not_included_text + " " + deferred_text
        for item in checklist:
            item_lower = item.lower()
            # Flag checklist items that mention known out-of-scope systems
            out_of_scope_signals = ["analytics", "account", "leaderboard", "backend", "deployment", "monetization"]
            for signal in out_of_scope_signals:
                if signal in item_lower and signal not in must_exist_text:
                    failure_fields.append("acceptance_checklist")
                    revision_instructions.append(
                        f"Acceptance checklist item references '{signal}' which is outside the v1 build scope. "
                        "Checklist must only include items testable within the first build."
                    )
                    break

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

    def gate_prototype_ui_spec(self, artifact: Dict[str, Any]) -> Dict[str, Any]:
        """Gate for prototype_ui_spec — Stage 8.

        Five dimensions:
          Reject-level (identity compromise):
            Dim 1 — Build spec fidelity: UI spec must implement the approved build spec
          Revise-level (fixable gaps):
            Dim 2 — Screen completeness
            Dim 3 — Component specification
            Dim 4 — Animation definition
            Dim 5 — Accessibility compliance
        """

        # ---- Dim 1: Build spec fidelity (reject-level) ----
        # The UI spec must reference the same components and screens from prototype_build_spec.
        # In stub mode, this is guaranteed by template selection. In LLM mode, the gate
        # catches drift by checking structural presence.
        screen_layouts = artifact.get("screen_layouts", [])
        ui_components = artifact.get("ui_components", [])
        if not screen_layouts:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="prototype_ui_spec",
                    target_artifact_version=artifact["version"],
                    stage_name="prototype_ui_spec",
                    status="reject",
                    failure_fields=["screen_layouts"],
                    strongest_failure_reason="UI spec has no screen layouts — cannot verify build spec fidelity",
                    revision_instructions=["screen_layouts must define at least one screen with regions and positioning."],
                    escalation_recommendation="reject_job",
                    memory_tags=["missing_screen_layouts"],
                ),
            )

        # ---- Dim 2: Screen completeness (revise-level) ----
        failure_fields = []
        revision_instructions = []

        for i, screen in enumerate(screen_layouts):
            if not screen.get("regions"):
                failure_fields.append(f"screen_layouts[{i}].regions")
                revision_instructions.append(f"Screen '{screen.get('screen_name', i)}' must have at least one region defined.")

            regions = screen.get("regions", [])
            for j, region in enumerate(regions):
                required_fields = ["position", "size", "purpose"]
                for field in required_fields:
                    if not region.get(field):
                        failure_fields.append(f"screen_layouts[{i}].regions[{j}].{field}")
                        revision_instructions.append(f"Region '{region.get('region_name', j)}' must have {field} defined.")

        # ---- Dim 3: Component specification (revise-level) ----
        if not ui_components:
            failure_fields.append("ui_components")
            revision_instructions.append("At least one UI component with styling and accessibility is required.")

        for i, comp in enumerate(ui_components):
            visual_style = comp.get("visual_style", {})
            if not visual_style.get("colors"):
                failure_fields.append(f"ui_components[{i}].visual_style.colors")
                revision_instructions.append(f"Component '{comp.get('component_name', i)}' must have color definitions.")

            if not comp.get("interaction_states"):
                failure_fields.append(f"ui_components[{i}].interaction_states")
                revision_instructions.append(f"Component '{comp.get('component_name', i)}' must define interaction states.")

            accessibility = comp.get("accessibility", {})
            required_accessibility = ["aria_label", "keyboard_navigation", "screen_reader_support", "color_contrast_ratio"]
            for field in required_accessibility:
                if field not in accessibility:
                    failure_fields.append(f"ui_components[{i}].accessibility.{field}")
                    revision_instructions.append(f"Component '{comp.get('component_name', i)}' must have {field} defined.")

        # ---- Dim 4: Animation definition (revise-level) ----
        animations = artifact.get("animations_and_transitions", [])
        if not animations:
            failure_fields.append("animations_and_transitions")
            revision_instructions.append("At least one animation or transition must be defined.")

        for i, anim in enumerate(animations):
            required_anim_fields = ["trigger", "duration", "easing", "description"]
            for field in required_anim_fields:
                if not anim.get(field):
                    failure_fields.append(f"animations_and_transitions[{i}].{field}")
                    revision_instructions.append(f"Animation '{anim.get('animation_name', i)}' must have {field} defined.")

        # ---- Dim 5: Accessibility compliance (revise-level) ----
        accessibility_reqs = artifact.get("accessibility_requirements", {})
        required_accessibility_reqs = ["wcag_level", "keyboard_navigation_complete", "screen_reader_compatible", "color_blind_friendly"]
        for field in required_accessibility_reqs:
            if field not in accessibility_reqs:
                failure_fields.append(f"accessibility_requirements.{field}")
                revision_instructions.append(f"Accessibility requirements must include {field}.")

        motor_considerations = accessibility_reqs.get("motor_impairment_considerations", [])
        if len(motor_considerations) < 2:
            failure_fields.append("accessibility_requirements.motor_impairment_considerations")
            revision_instructions.append("At least 2 motor impairment considerations must be listed.")

        # Responsive breakpoints should exist
        breakpoints = artifact.get("responsive_breakpoints", [])
        if not breakpoints:
            failure_fields.append("responsive_breakpoints")
            revision_instructions.append("At least one responsive breakpoint must be defined.")

        # Deduplicate
        failure_fields = list(dict.fromkeys(failure_fields))

        if failure_fields:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="prototype_ui_spec",
                    target_artifact_version=artifact["version"],
                    stage_name="prototype_ui_spec",
                    status="revise",
                    failure_fields=failure_fields,
                    strongest_failure_reason="UI spec is not yet implementation-ready — gaps in screen completeness, component specification, or accessibility",
                    revision_instructions=revision_instructions,
                    escalation_recommendation="reroute",
                    memory_tags=["ui_completeness", "ui_spec_gaps"],
                ),
            )

        return self._finalize_gate(
            artifact,
            _new_gate_decision(
                job_id=artifact["job_id"],
                target_artifact="prototype_ui_spec",
                target_artifact_version=artifact["version"],
                stage_name="prototype_ui_spec",
                status="pass",
            ),
        )


    def gate_implementation_plan(self, artifact: Dict[str, Any]) -> Dict[str, Any]:
        """Gate for implementation_plan — Stage 9.

        Four dimensions:
          Reject-level (identity compromise):
            Dim 1 — Build scope: must_build_now must be non-empty
          Revise-level (fixable gaps):
            Dim 2 — File plan: file_plan must list files to create or update
            Dim 3 — Component plan: component_plan must be non-empty with responsibilities
            Dim 4 — Test plan: manual_checks must exist and be non-empty
        """

        # ---- Dim 1: Build scope completeness (reject-level) ----
        build_scope = artifact.get("build_scope", {})
        must_build_now = build_scope.get("must_build_now", [])
        if not must_build_now:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="implementation_plan",
                    target_artifact_version=artifact["version"],
                    stage_name="implementation_plan",
                    status="reject",
                    failure_fields=["build_scope.must_build_now"],
                    strongest_failure_reason="Implementation plan defines nothing to build now — cannot guide a build",
                    revision_instructions=["build_scope.must_build_now must list every feature/system to implement in this pass."],
                    escalation_recommendation="reject_job",
                    memory_tags=["missing_build_scope"],
                ),
            )

        # ---- Dim 2–4: Revise-level checks ----
        failure_fields = []
        revision_instructions = []

        # Dim 2: File plan
        file_plan = artifact.get("file_plan", [])
        if not file_plan:
            failure_fields.append("file_plan")
            revision_instructions.append("file_plan must list every file to create or update with its purpose.")

        create_files = [f for f in file_plan if f.get("action") in ("create", "update")]
        if file_plan and not create_files:
            failure_fields.append("file_plan.action")
            revision_instructions.append("file_plan must include at least one file with action 'create' or 'update'.")

        # Dim 3: Component plan
        component_plan = artifact.get("component_plan", [])
        if not component_plan:
            failure_fields.append("component_plan")
            revision_instructions.append("component_plan must define at least one component with its responsibility.")

        for i, comp in enumerate(component_plan):
            if not comp.get("responsibility", "").strip():
                failure_fields.append(f"component_plan[{i}].responsibility")
                revision_instructions.append(
                    f"Component '{comp.get('component_name', i)}' must have a clear responsibility statement."
                )

        # Dim 4: Test plan
        test_plan = artifact.get("test_plan", {})
        manual_checks = test_plan.get("manual_checks", [])
        if not manual_checks:
            failure_fields.append("test_plan.manual_checks")
            revision_instructions.append("test_plan.manual_checks must list at least one player-observable behavior to verify.")

        # State plan must have state_ownership_notes
        state_plan = artifact.get("state_plan", {})
        if not state_plan.get("state_ownership_notes", "").strip():
            failure_fields.append("state_plan.state_ownership_notes")
            revision_instructions.append("state_plan.state_ownership_notes must identify which component/hook owns authoritative state.")

        # Deduplicate
        failure_fields = list(dict.fromkeys(failure_fields))

        if failure_fields:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="implementation_plan",
                    target_artifact_version=artifact["version"],
                    stage_name="implementation_plan",
                    status="revise",
                    failure_fields=failure_fields,
                    strongest_failure_reason="Implementation plan is not yet builder-ready — gaps in file plan, component coverage, or test targets",
                    revision_instructions=revision_instructions,
                    escalation_recommendation="reroute",
                    memory_tags=["implementation_plan_gaps"],
                ),
            )

        return self._finalize_gate(
            artifact,
            _new_gate_decision(
                job_id=artifact["job_id"],
                target_artifact="implementation_plan",
                target_artifact_version=artifact["version"],
                stage_name="implementation_plan",
                status="pass",
            ),
        )


    def gate_implementation_patch_plan(self, artifact: Dict[str, Any]) -> Dict[str, Any]:
        failure_fields: List[str] = []
        revision_instructions: List[str] = []

        # ---- Dim 1: Patch completeness (reject-level) ----
        patch_sequence = artifact.get("patch_sequence", [])
        if not patch_sequence:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="implementation_patch_plan",
                    target_artifact_version=artifact["version"],
                    stage_name="implementation_patch_plan",
                    status="reject",
                    failure_fields=["patch_sequence"],
                    strongest_failure_reason="patch_sequence is empty — patch plan cannot guide a build.",
                    revision_instructions=["patch_sequence must contain at least one patch entry covering every create/edit file in target_files."],
                    escalation_recommendation="reject_job",
                    memory_tags=["patch_plan_empty"],
                ),
            )

        target_files = artifact.get("target_files", [])
        files_needing_patches = {
            f["file_path"] for f in target_files if f.get("operation") in ("create", "edit")
        }
        patched_files = {p["file_path"] for p in patch_sequence}
        missing_file_coverage = files_needing_patches - patched_files
        if missing_file_coverage:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="implementation_patch_plan",
                    target_artifact_version=artifact["version"],
                    stage_name="implementation_patch_plan",
                    status="reject",
                    failure_fields=["patch_sequence"],
                    strongest_failure_reason=f"Files missing patch coverage: {sorted(missing_file_coverage)}",
                    revision_instructions=[
                        f"Every file marked create or edit in target_files must have at least one patch entry. Missing: {sorted(missing_file_coverage)}"
                    ],
                    escalation_recommendation="reject_job",
                    memory_tags=["patch_plan_missing_file_coverage"],
                ),
            )

        # ---- Dim 2: Naming registry integrity (reject-level) ----
        registry_names = {entry["name"] for entry in artifact.get("naming_registry", [])}
        unregistered: List[str] = []
        for patch in patch_sequence:
            for ne in patch.get("named_elements", []):
                parts = ne.split(":", 1)
                if len(parts) == 2:
                    name = parts[1]
                    if name not in registry_names:
                        unregistered.append(f"{patch['patch_id']}:{ne}")
        if unregistered:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="implementation_patch_plan",
                    target_artifact_version=artifact["version"],
                    stage_name="implementation_patch_plan",
                    status="reject",
                    failure_fields=["naming_registry"],
                    strongest_failure_reason=f"Named elements not in naming_registry: {unregistered[:5]}",
                    revision_instructions=[
                        f"Every name in named_elements must appear in naming_registry. Missing: {unregistered[:5]}"
                    ],
                    escalation_recommendation="reject_job",
                    memory_tags=["patch_plan_naming_drift"],
                ),
            )

        # ---- Dim 3: Dependency graph validity (revise-level) ----
        patch_ids = {p["patch_id"] for p in patch_sequence}
        for patch in patch_sequence:
            for dep in patch.get("depends_on", []):
                if dep not in patch_ids:
                    failure_fields.append(f"patch_sequence[{patch['patch_id']}].depends_on")
                    revision_instructions.append(
                        f"Patch {patch['patch_id']} declares dependency on {dep} which does not exist in patch_sequence."
                    )

        # ---- Dim 4: Acceptance signal coverage (revise-level) ----
        features_added = artifact.get("source_pass", {}).get("features_added", [])
        acceptance_signals = artifact.get("acceptance_signals", [])
        if features_added and not acceptance_signals:
            failure_fields.append("acceptance_signals")
            revision_instructions.append(
                "Every feature in source_pass.features_added must trace to at least one acceptance_signal."
            )

        # ---- Dim 5: Animation contract completeness (revise-level) ----
        animation_contract_keyframes = {ac["keyframe_name"] for ac in artifact.get("animation_contracts", [])}
        for patch in patch_sequence:
            if patch.get("patch_type") in ("add_keyframe", "add_css_custom_property"):
                for ne in patch.get("named_elements", []):
                    if ne.startswith("keyframe:"):
                        kf_name = ne.split(":", 1)[1]
                        if kf_name not in animation_contract_keyframes:
                            failure_fields.append(f"animation_contracts[{kf_name}]")
                            revision_instructions.append(
                                f"Keyframe '{kf_name}' introduced in {patch['patch_id']} has no entry in animation_contracts."
                            )

        failure_fields = list(dict.fromkeys(failure_fields))
        if failure_fields:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="implementation_patch_plan",
                    target_artifact_version=artifact["version"],
                    stage_name="implementation_patch_plan",
                    status="revise",
                    failure_fields=failure_fields,
                    strongest_failure_reason="Patch plan has dependency graph, signal coverage, or animation contract gaps.",
                    revision_instructions=revision_instructions,
                    escalation_recommendation="reroute",
                    memory_tags=["patch_plan_gaps"],
                ),
            )

        return self._finalize_gate(
            artifact,
            _new_gate_decision(
                job_id=artifact["job_id"],
                target_artifact="implementation_patch_plan",
                target_artifact_version=artifact["version"],
                stage_name="implementation_patch_plan",
                status="pass",
            ),
        )


    def gate_playtest_diagnostic_report(self, artifact: Dict[str, Any]) -> Dict[str, Any]:
        """Gate for playtest_diagnostic_report — Stage 11.

        Dimensions:
          Reject-level:
            Dim 1 — Friction points non-empty: diagnostic must identify at least one issue
          Revise-level:
            Dim 2 — Feel scores present and complete
            Dim 3 — Pattern summary non-empty
            Dim 4 — Recommended action is a valid enum value
        """
        # Dim 1: Must have friction points (reject-level)
        friction_points = artifact.get("friction_points", [])
        if not friction_points:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="playtest_diagnostic_report",
                    target_artifact_version=artifact["version"],
                    stage_name="playtest_diagnostic_report",
                    status="reject",
                    failure_fields=["friction_points"],
                    strongest_failure_reason="Diagnostic has no friction points — cannot improve without knowing what is wrong",
                    revision_instructions=["friction_points must list at least one observation, even for strong builds."],
                    escalation_recommendation="reject_job",
                    memory_tags=["missing_friction_points"],
                ),
            )

        failure_fields = []
        revision_instructions = []

        # Dim 2: Feel scores
        feel_scores = artifact.get("feel_scores", {})
        required_scores = ["immediacy", "clarity", "reward_rhythm", "math_visibility", "overall_rating"]
        for field in required_scores:
            if field not in feel_scores:
                failure_fields.append(f"feel_scores.{field}")
                revision_instructions.append(f"feel_scores.{field} must be rated 1–5.")

        # Dim 3: Pattern summary
        if not artifact.get("pattern_summary", "").strip():
            failure_fields.append("pattern_summary")
            revision_instructions.append("pattern_summary must synthesize the dominant themes in 2–3 sentences.")

        # Dim 4: Recommended action
        valid_actions = {"proceed_to_next_pass", "revise_current_pass", "tune_only", "reject_concept"}
        recommended = artifact.get("recommended_action", "")
        if recommended not in valid_actions:
            failure_fields.append("recommended_action")
            revision_instructions.append(
                f"recommended_action must be one of: {sorted(valid_actions)}. Got '{recommended}'."
            )

        failure_fields = list(dict.fromkeys(failure_fields))

        if failure_fields:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="playtest_diagnostic_report",
                    target_artifact_version=artifact["version"],
                    stage_name="playtest_diagnostic_report",
                    status="revise",
                    failure_fields=failure_fields,
                    strongest_failure_reason="Diagnostic is incomplete — missing feel scores, pattern summary, or recommended action",
                    revision_instructions=revision_instructions,
                    escalation_recommendation="reroute",
                    memory_tags=["incomplete_diagnostic"],
                ),
            )

        return self._finalize_gate(
            artifact,
            _new_gate_decision(
                job_id=artifact["job_id"],
                target_artifact="playtest_diagnostic_report",
                target_artifact_version=artifact["version"],
                stage_name="playtest_diagnostic_report",
                status="pass",
            ),
        )

    def gate_revision_brief(self, artifact: Dict[str, Any]) -> Dict[str, Any]:
        """Gate for revision_brief — Stage 12.

        Dimensions:
          Reject-level:
            Dim 1 — change_items non-empty: must specify what to change
          Revise-level:
            Dim 2 — scope.change_now and scope.preserve non-empty
            Dim 3 — All change_items have acceptance_signals
            Dim 4 — revision_goal non-empty
        """
        # Dim 1: Must have change items (reject-level)
        change_items = artifact.get("change_items", [])
        if not change_items:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="revision_brief",
                    target_artifact_version=artifact["version"],
                    stage_name="revision_brief",
                    status="reject",
                    failure_fields=["change_items"],
                    strongest_failure_reason="Revision brief specifies no changes — cannot drive a patch plan",
                    revision_instructions=["change_items must list at least one specific, independently testable change."],
                    escalation_recommendation="reject_job",
                    memory_tags=["empty_revision_brief"],
                ),
            )

        failure_fields = []
        revision_instructions = []

        # Dim 2: Scope
        scope = artifact.get("scope", {})
        if not scope.get("change_now"):
            failure_fields.append("scope.change_now")
            revision_instructions.append("scope.change_now must list at least one item to change in this revision.")
        if not scope.get("preserve"):
            failure_fields.append("scope.preserve")
            revision_instructions.append("scope.preserve must list at least one thing that must not be broken.")

        # Dim 3: Acceptance signals
        for i, item in enumerate(change_items):
            if not item.get("acceptance_signal", "").strip():
                failure_fields.append(f"change_items[{i}].acceptance_signal")
                revision_instructions.append(
                    f"Change '{item.get('change_id', i)}' must have an observable acceptance_signal."
                )

        # Dim 4: Revision goal
        if not artifact.get("revision_goal", "").strip():
            failure_fields.append("revision_goal")
            revision_instructions.append("revision_goal must be a clear one-sentence statement of what this revision achieves.")

        failure_fields = list(dict.fromkeys(failure_fields))

        if failure_fields:
            return self._finalize_gate(
                artifact,
                _new_gate_decision(
                    job_id=artifact["job_id"],
                    target_artifact="revision_brief",
                    target_artifact_version=artifact["version"],
                    stage_name="revision_brief",
                    status="revise",
                    failure_fields=failure_fields,
                    strongest_failure_reason="Revision brief has incomplete scope or missing acceptance signals",
                    revision_instructions=revision_instructions,
                    escalation_recommendation="reroute",
                    memory_tags=["incomplete_revision_brief"],
                ),
            )

        return self._finalize_gate(
            artifact,
            _new_gate_decision(
                job_id=artifact["job_id"],
                target_artifact="revision_brief",
                target_artifact_version=artifact["version"],
                stage_name="revision_brief",
                status="pass",
            ),
        )


if __name__ == "__main__":
    from pathlib import Path
    from utils.validation import load_json

    repo_root = Path(__file__).resolve().parents[1]
    engine = GateEngine(repo_root)
    fixture = load_json(repo_root / "tests" / "fixtures" / "valid" / "request_brief.valid.json")
    workspace = repo_root / "memory" / "job_workspaces" / fixture["job_id"]
    workspace.mkdir(parents=True, exist_ok=True)
    print(json.dumps(engine.gate_request_brief(fixture), indent=2))
