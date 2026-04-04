from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
from typing import Dict, Optional

ARTIFACT_ORDER = [
    "request_brief",
    "intake_brief",
    "kill_report",
    "interaction_decision_memo",
    "family_architecture_brief",
    "lowest_viable_loop_brief",
    "prototype_spec",
    "prototype_build_spec",
    "prototype_ui_spec",
    "implementation_plan",
    "implementation_patch_plan",
]

REVISION_TRACKED = [
    "intake_brief",
    "kill_report",
    "interaction_decision_memo",
    "family_architecture_brief",
    "lowest_viable_loop_brief",
    "prototype_spec",
    "prototype_build_spec",
    "prototype_ui_spec",
    "implementation_plan",
    "implementation_patch_plan",
]

DEFAULT_STAGE_STATE = {
    "request_brief": "not_started",
    "intake_brief": "not_started",
    "kill_report": "not_started",
    "interaction_decision_memo": "not_started",
    "family_architecture_brief": "not_started",
    "lowest_viable_loop_brief": "not_started",
    "prototype_spec": "not_started",
    "prototype_build_spec": "not_started",
    "prototype_ui_spec": "not_started",
    "implementation_plan": "not_started",
    "implementation_patch_plan": "not_started",
}

DEFAULT_AUTHORITATIVE_VERSIONS = {
    "request_brief": 0,
    "intake_brief": 0,
    "kill_report": 0,
    "interaction_decision_memo": 0,
    "family_architecture_brief": 0,
    "lowest_viable_loop_brief": 0,
    "prototype_spec": 0,
    "prototype_build_spec": 0,
    "prototype_ui_spec": 0,
    "implementation_plan": 0,
    "implementation_patch_plan": 0,
}

DEFAULT_REVISION_COUNTS = {
    "intake_brief": 0,
    "kill_report": 0,
    "interaction_decision_memo": 0,
    "family_architecture_brief": 0,
    "lowest_viable_loop_brief": 0,
    "prototype_spec": 0,
    "prototype_build_spec": 0,
    "prototype_ui_spec": 0,
    "implementation_plan": 0,
    "implementation_patch_plan": 0,
}


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def infer_stage_from_artifact(artifact_name: str) -> str:
    if artifact_name not in ARTIFACT_ORDER:
        raise ValueError(f"Unknown artifact_name: {artifact_name}")
    return artifact_name


@dataclass
class StageLedger:
    job_id: str
    current_stage: str
    stage_states: Dict[str, str]
    revision_counts: Dict[str, int]
    authoritative_versions: Dict[str, int]
    last_gate_status: str
    updated_at: str

    @classmethod
    def create(cls, job_id: str) -> "StageLedger":
        return cls(
            job_id=job_id,
            current_stage="request_brief",
            stage_states=DEFAULT_STAGE_STATE.copy(),
            revision_counts=DEFAULT_REVISION_COUNTS.copy(),
            authoritative_versions=DEFAULT_AUTHORITATIVE_VERSIONS.copy(),
            last_gate_status="not_started",
            updated_at=utc_now_iso(),
        )

    @classmethod
    def load(cls, path: Path) -> "StageLedger":
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls(**data)

    def to_dict(self) -> Dict:
        return {
            "job_id": self.job_id,
            "current_stage": self.current_stage,
            "stage_states": self.stage_states,
            "revision_counts": self.revision_counts,
            "authoritative_versions": self.authoritative_versions,
            "last_gate_status": self.last_gate_status,
            "updated_at": self.updated_at,
        }

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(self.to_dict(), indent=2), encoding="utf-8")

    def set_stage_active(self, artifact_name: str) -> None:
        stage = infer_stage_from_artifact(artifact_name)
        self.current_stage = stage
        self.stage_states[stage] = "active"
        self.updated_at = utc_now_iso()

    def mark_authoritative(self, artifact_name: str, version: int) -> None:
        stage = infer_stage_from_artifact(artifact_name)
        self.authoritative_versions[stage] = version
        self.updated_at = utc_now_iso()

    def increment_revision(self, artifact_name: str) -> None:
        if artifact_name not in REVISION_TRACKED:
            return
        self.revision_counts[artifact_name] += 1
        self.updated_at = utc_now_iso()

    def apply_gate_decision(self, artifact_name: str, gate_status: str, version: int, revise_increments: bool = True) -> None:
        stage = infer_stage_from_artifact(artifact_name)
        self.last_gate_status = gate_status

        if gate_status == "pass":
            self.stage_states[stage] = "approved"
            self.authoritative_versions[stage] = version
            self.current_stage = stage
        elif gate_status == "revise":
            self.stage_states[stage] = "revise"
            if revise_increments and artifact_name in REVISION_TRACKED:
                self.revision_counts[artifact_name] += 1
            self.current_stage = stage
        elif gate_status == "reject":
            self.stage_states[stage] = "reject"
            self.current_stage = stage
        else:
            raise ValueError(f"Unsupported gate status: {gate_status}")

        self.updated_at = utc_now_iso()

    def next_stage_after_pass(self, artifact_name: str) -> Optional[str]:
        stage = infer_stage_from_artifact(artifact_name)
        idx = ARTIFACT_ORDER.index(stage)
        if idx == len(ARTIFACT_ORDER) - 1:
            return None
        return ARTIFACT_ORDER[idx + 1]


def initialize_stage_ledger(job_workspace: Path, job_id: str) -> Path:
    job_workspace.mkdir(parents=True, exist_ok=True)
    ledger = StageLedger.create(job_id)
    ledger_path = job_workspace / "stage_ledger.json"
    ledger.save(ledger_path)
    return ledger_path


def update_stage_ledger_for_artifact(
    ledger_path: Path,
    artifact_name: str,
    gate_status: str,
    version: int,
    revise_increments: bool = True,
) -> Dict:
    ledger = StageLedger.load(ledger_path)
    ledger.apply_gate_decision(
        artifact_name=artifact_name,
        gate_status=gate_status,
        version=version,
        revise_increments=revise_increments,
    )
    ledger.save(ledger_path)
    return ledger.to_dict()


if __name__ == "__main__":
    demo_workspace = Path("memory/job_workspaces/demo_job")
    ledger_path = initialize_stage_ledger(demo_workspace, "demo_job")
    print(f"Initialized: {ledger_path}")
    updated = update_stage_ledger_for_artifact(ledger_path, "request_brief", "pass", 1)
    print(json.dumps(updated, indent=2))
