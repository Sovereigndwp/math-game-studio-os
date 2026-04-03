from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, Optional  # Optional used in build_agent_context return
import json

from utils.validation import (
    next_artifact_version,
    write_validated_artifact,
    ValidationErrorBundle,
    format_validation_report,
    save_debug_payload,
    load_schema,
)


@dataclass
class AgentRunResult:
    job_id: str
    agent_name: str
    artifact_name: str
    artifact_version: int
    artifact_path: str
    artifact: Dict[str, Any]


@dataclass
class AgentSpec:
    agent_name: str
    expected_output_artifact: str
    expected_produced_by: str
    prompt_path: Path
    config_path: Path
    allowed_reads: list[str]
    allowed_writes: list[str]
    max_revision_count: int = 2


class AgentRunnerError(Exception):
    pass


class SharedAgentRunner:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.schema_dir = repo_root / "artifacts" / "schemas"
        self.workspace_root = repo_root / "memory" / "job_workspaces"

    def load_text(self, path: Path) -> str:
        if not path.exists():
            raise FileNotFoundError(f"Missing file: {path}")
        return path.read_text(encoding="utf-8")

    def load_json(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            raise FileNotFoundError(f"Missing JSON file: {path}")
        return json.loads(path.read_text(encoding="utf-8"))

    def workspace_for_job(self, job_id: str) -> Path:
        path = self.workspace_root / job_id
        path.mkdir(parents=True, exist_ok=True)
        return path

    def read_authoritative_artifacts(
        self,
        job_id: str,
        artifact_paths: Dict[str, Path],
        allowed_reads: list[str],
    ) -> Dict[str, Dict[str, Any]]:
        loaded: Dict[str, Dict[str, Any]] = {}
        for artifact_name in allowed_reads:
            if artifact_name not in artifact_paths:
                raise AgentRunnerError(
                    f"{artifact_name} was not provided to the runner for job {job_id}"
                )
            loaded[artifact_name] = self.load_json(artifact_paths[artifact_name])
        return loaded

    def build_agent_context(
        self,
        spec: AgentSpec,
        job_id: str,
        artifact_inputs: Dict[str, Dict[str, Any]],
    ) -> Dict[str, Any]:
        prompt_text = self.load_text(spec.prompt_path)
        config_text = self.load_text(spec.config_path)

        # Load the output schema so it can be injected into LLM prompts.
        # Agents using the stub callable ignore this; LLM callables use it to
        # ensure the model has the exact schema constraints in the prompt.
        try:
            output_schema: Optional[Dict[str, Any]] = load_schema(self.schema_dir, spec.expected_output_artifact)
        except FileNotFoundError:
            output_schema = None

        return {
            "job_id": job_id,
            "agent_name": spec.agent_name,
            "prompt_text": prompt_text,
            "config_text": config_text,
            "artifact_inputs": artifact_inputs,
            "expected_output_artifact": spec.expected_output_artifact,
            "expected_produced_by": spec.expected_produced_by,
            "output_schema": output_schema,
        }

    def run(
        self,
        spec: AgentSpec,
        job_id: str,
        artifact_paths: Dict[str, Path],
        model_callable: Callable[[Dict[str, Any]], Dict[str, Any]],
    ) -> AgentRunResult:
        if spec.expected_output_artifact not in spec.allowed_writes:
            raise AgentRunnerError(
                f"{spec.agent_name} is not allowed to write {spec.expected_output_artifact}"
            )

        inputs = self.read_authoritative_artifacts(
            job_id=job_id,
            artifact_paths=artifact_paths,
            allowed_reads=spec.allowed_reads,
        )
        context = self.build_agent_context(spec=spec, job_id=job_id, artifact_inputs=inputs)

        artifact = model_callable(context)
        if not isinstance(artifact, dict):
            raise AgentRunnerError(f"{spec.agent_name} returned a non-dict artifact")

        artifact["job_id"] = job_id
        artifact["artifact_name"] = spec.expected_output_artifact
        artifact["produced_by"] = spec.expected_produced_by

        workspace = self.workspace_for_job(job_id)
        artifact["version"] = next_artifact_version(workspace, spec.expected_output_artifact)

        try:
            artifact_path = write_validated_artifact(
                job_workspace=workspace,
                artifact=artifact,
                schema_dir=self.schema_dir,
                expected_artifact_name=spec.expected_output_artifact,
                expected_produced_by=spec.expected_produced_by,
            )
        except ValidationErrorBundle as exc:
            # Log the invalid payload to the workspace for debugging.
            debug_path = save_debug_payload(workspace, spec.expected_output_artifact, artifact)
            # Print a full field-level error report to stdout.
            report = format_validation_report(exc.errors, spec.expected_output_artifact, job_id)
            print(report)
            print(f"  Invalid payload saved → {debug_path.name}")
            # Re-raise as AgentRunnerError so pipeline can surface it cleanly.
            raise AgentRunnerError(
                f"{spec.agent_name} produced an invalid '{spec.expected_output_artifact}' "
                f"for job '{job_id}': {len(exc.errors)} schema error(s). "
                f"See {debug_path} for the full payload."
            ) from exc

        return AgentRunResult(
            job_id=job_id,
            agent_name=spec.agent_name,
            artifact_name=artifact["artifact_name"],
            artifact_version=artifact["version"],
            artifact_path=str(artifact_path),
            artifact=artifact,
        )
