from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
import re
from typing import Any, Dict, List, Optional

from orchestrator.stage_ledger import (
    initialize_stage_ledger,
    update_stage_ledger_for_artifact,
    StageLedger,
)
from utils.validation import (
    next_artifact_version,
    write_validated_artifact,
    load_json,
)

ARTIFACT_ORDER = [
    "request_brief",
    "intake_brief",
    "kill_report",
    "interaction_decision_memo",
    "family_architecture_brief",
    "lowest_viable_loop_brief",
]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def create_job_id(prefix: str = "job") -> str:
    return f"{prefix}_{datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')}"


@dataclass
class OrchestratorConfig:
    repo_root: Path

    @property
    def schema_dir(self) -> Path:
        return self.repo_root / "artifacts" / "schemas"

    @property
    def workspace_root(self) -> Path:
        return self.repo_root / "memory" / "job_workspaces"

    @property
    def registries_root(self) -> Path:
        return self.repo_root / "memory" / "registries"

    @property
    def active_focus_registry_path(self) -> Path:
        return self.registries_root / "active_focus_registry.json"

    @property
    def family_registry_path(self) -> Path:
        return self.registries_root / "family_registry.json"


class Orchestrator:
    def __init__(self, config: OrchestratorConfig):
        self.config = config

    def classify_request_type(self, raw_user_command: str) -> str:
        text = raw_user_command.lower().strip()
        if any(k in text for k in ["audit this", "review this", "audit request"]):
            return "audit"
        if any(k in text for k in ["prototype only", "prototype"]):
            return "prototype_only"
        if any(k in text for k in ["extend ", "extend into", "add to existing"]):
            return "family_extension"
        if any(k in text for k in ["upgrade to production", "production upgrade"]):
            return "production_upgrade"
        return "new_game"

    def classify_priority_level(self, raw_user_command: str) -> str:
        text = raw_user_command.lower()
        if any(k in text for k in ["urgent", "immediately", "critical"]):
            return "critical"
        if any(k in text for k in ["high priority", "important"]):
            return "high"
        return "medium"

    def load_active_focus_registry(self) -> Dict[str, Any]:
        path = self.config.active_focus_registry_path
        if not path.exists():
            return {
                "current_primary_job_id": "",
                "current_primary_game_title": "",
                "current_family_name": "",
                "focus_status": "paused",
                "allowed_parallel_jobs": [],
                "notes": "",
            }
        return load_json(path)

    def load_family_registry(self) -> List[Dict[str, Any]]:
        path = self.config.family_registry_path
        if not path.exists():
            return []
        data = load_json(path)
        return data if isinstance(data, list) else []

    def detect_focus_conflict(self, request_type: str, active_focus_registry: Dict[str, Any]) -> bool:
        current_focus = active_focus_registry.get("current_primary_job_id", "")
        focus_status = active_focus_registry.get("focus_status", "paused")
        if not current_focus or focus_status == "paused":
            return False
        if request_type in {"audit", "prototype_only"}:
            return False
        return True

    def find_existing_family_candidates(self, raw_user_command: str, family_registry: List[Dict[str, Any]]) -> List[str]:
        text = raw_user_command.lower()
        candidates = []
        for item in family_registry:
            family_name = item.get("family_name", "")
            world_theme = item.get("world_theme", "")
            core_identity = item.get("core_identity", "")
            blob = " ".join([family_name, world_theme, core_identity]).lower()
            if family_name and any(token in blob for token in re.findall(r"[a-zA-Z]+", text)):
                candidates.append(family_name)
        # Deduplicate while preserving order
        seen = set()
        ordered = []
        for c in candidates:
            if c not in seen:
                seen.add(c)
                ordered.append(c)
        return ordered[:5]

    def extract_requested_constraints(self, raw_user_command: str) -> List[str]:
        text = raw_user_command.lower()
        constraints = []
        grade_match = re.search(r"grade\s*(\d+)", text)
        if grade_match:
            constraints.append(f"grade_{grade_match.group(1)}")
        for token in [
            "kindergarten", "elementary", "middle school", "high school",
            "addition", "subtraction", "multiplication", "division",
            "fractions", "ratios", "algebra", "unit circle", "trigonometry", "calculus"
        ]:
            if token in text:
                constraints.append(token.replace(" ", "_"))
        return constraints

    def extract_requested_outputs(self, request_type: str) -> List[str]:
        if request_type == "prototype_only":
            return ["lowest_viable_loop_brief"]
        if request_type == "audit":
            return ["request_brief", "routing_review"]
        return ["lowest_viable_loop_brief"]

    def build_request_brief(self, raw_user_command: str, job_id: Optional[str] = None) -> Dict[str, Any]:
        active_focus = self.load_active_focus_registry()
        family_registry = self.load_family_registry()
        request_type = self.classify_request_type(raw_user_command)
        priority_level = self.classify_priority_level(raw_user_command)
        current_production_focus_conflict = self.detect_focus_conflict(request_type, active_focus)
        existing_family_candidates = self.find_existing_family_candidates(raw_user_command, family_registry)
        requested_constraints = self.extract_requested_constraints(raw_user_command)
        requested_outputs = self.extract_requested_outputs(request_type)

        notes_for_routing = (
            "Request normalized for V1 first-six-agent pipeline. "
            "Check family reuse before creating a new family."
        )

        return {
            "job_id": job_id or create_job_id(),
            "artifact_name": "request_brief",
            "version": 1,
            "status": "active",
            "produced_by": "Orchestrator",
            "timestamp": utc_now_iso(),
            "raw_user_command": raw_user_command,
            "request_type": request_type,
            "priority_level": priority_level,
            "current_production_focus_conflict": current_production_focus_conflict,
            "notes_for_routing": notes_for_routing,
            "existing_family_candidates": existing_family_candidates,
            "requested_constraints": requested_constraints,
            "requested_outputs": requested_outputs,
        }

    def initialize_job_workspace(self, job_id: str) -> Path:
        workspace = self.config.workspace_root / job_id
        workspace.mkdir(parents=True, exist_ok=True)
        ledger_path = workspace / "stage_ledger.json"
        if not ledger_path.exists():
            initialize_stage_ledger(workspace, job_id)
        return workspace

    def create_request_brief(self, raw_user_command: str, job_id: Optional[str] = None) -> Dict[str, Any]:
        request_brief = self.build_request_brief(raw_user_command, job_id=job_id)
        workspace = self.initialize_job_workspace(request_brief["job_id"])

        # Ensure correct version if rerun on same job
        request_brief["version"] = next_artifact_version(workspace, "request_brief")

        write_validated_artifact(
            job_workspace=workspace,
            artifact=request_brief,
            schema_dir=self.config.schema_dir,
            expected_artifact_name="request_brief",
            expected_produced_by="Orchestrator",
        )

        update_stage_ledger_for_artifact(
            ledger_path=workspace / "stage_ledger.json",
            artifact_name="request_brief",
            gate_status="pass",
            version=request_brief["version"],
            revise_increments=False,
        )
        return request_brief

    def route_after_gate(self, target_artifact: str, gate_status: str) -> Dict[str, Any]:
        next_map = {
            "request_brief": "intake_framing_agent",
            "intake_brief": "kill_test_agent",
            "kill_report": "interaction_mapper_agent",
            "interaction_decision_memo": "family_architect_agent",
            "family_architecture_brief": "core_loop_agent",
            "lowest_viable_loop_brief": None,
        }
        if gate_status == "pass":
            return {"action": "advance", "next_agent": next_map.get(target_artifact)}
        if gate_status == "revise":
            stage_to_agent = {
                "request_brief": "orchestrator",
                "intake_brief": "intake_framing_agent",
                "kill_report": "kill_test_agent",
                "interaction_decision_memo": "interaction_mapper_agent",
                "family_architecture_brief": "family_architect_agent",
                "lowest_viable_loop_brief": "core_loop_agent",
            }
            return {"action": "revise", "next_agent": stage_to_agent.get(target_artifact)}
        return {"action": "reject", "next_agent": None}

    def get_authoritative_artifact_path(self, job_id: str, artifact_name: str) -> Optional[Path]:
        workspace = self.config.workspace_root / job_id
        ledger_path = workspace / "stage_ledger.json"
        if not ledger_path.exists():
            return None
        ledger = StageLedger.load(ledger_path)
        version = ledger.authoritative_versions.get(artifact_name, 0)
        if version <= 0:
            return None
        path = workspace / f"{artifact_name}.v{version}.json"
        return path if path.exists() else None


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]
    orchestrator = Orchestrator(OrchestratorConfig(repo_root=repo_root))
    demo = orchestrator.create_request_brief(
        "Create a grade 2 bakery game for addition to 20 where students pack pastry orders before customers leave."
    )
    print(json.dumps(demo, indent=2))
    print(orchestrator.route_after_gate("request_brief", "pass"))
