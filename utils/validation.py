from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, Tuple

try:
    import jsonschema
    # Prefer Draft202012Validator (jsonschema>=4); fall back to Draft7Validator (jsonschema 3.x).
    # The schemas use draft/2020-12 features that are all valid draft-7 (required, type, const, enum,
    # additionalProperties, minLength, minimum, maximum). No draft-2020-12-only keywords are used.
    try:
        from jsonschema import Draft202012Validator as _SchemaValidator
    except ImportError:
        from jsonschema import Draft7Validator as _SchemaValidator  # type: ignore[assignment]
except ImportError as exc:  # pragma: no cover
    raise RuntimeError("jsonschema is required for validation utilities") from exc


class ValidationErrorBundle(Exception):
    def __init__(self, errors: list[str]):
        self.errors = errors
        super().__init__("Artifact validation failed")


def load_json(path: Path) -> Dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def save_json(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def schema_path_for_artifact(schema_dir: Path, artifact_name: str) -> Path:
    return schema_dir / f"{artifact_name}.schema.json"


def load_schema(schema_dir: Path, artifact_name: str) -> Dict[str, Any]:
    path = schema_path_for_artifact(schema_dir, artifact_name)
    if not path.exists():
        raise FileNotFoundError(f"Schema not found for artifact '{artifact_name}': {path}")
    return load_json(path)


def build_validator(schema_dir: Path, artifact_name: str) -> "_SchemaValidator":
    schema = load_schema(schema_dir, artifact_name)
    return _SchemaValidator(schema)


def collect_validation_errors(validator: "_SchemaValidator", artifact: Dict[str, Any]) -> list[str]:
    errors = []
    for error in sorted(validator.iter_errors(artifact), key=lambda e: list(e.absolute_path)):
        path = ".".join(str(x) for x in error.absolute_path) or "<root>"
        errors.append(f"{path}: {error.message}")
    return errors


def validate_artifact(
    artifact: Dict[str, Any],
    schema_dir: Path,
    expected_artifact_name: str | None = None,
    expected_produced_by: str | None = None,
) -> Tuple[bool, list[str]]:
    artifact_name = artifact.get("artifact_name")

    if expected_artifact_name and artifact_name != expected_artifact_name:
        return False, [f"artifact_name mismatch: expected '{expected_artifact_name}', got '{artifact_name}'"]

    if not artifact_name:
        return False, ["artifact_name is missing"]

    validator = build_validator(schema_dir, artifact_name)
    errors = collect_validation_errors(validator, artifact)

    if expected_produced_by:
        actual = artifact.get("produced_by")
        if actual != expected_produced_by:
            errors.append(
                f"produced_by mismatch: expected '{expected_produced_by}', got '{actual}'"
            )

    return len(errors) == 0, errors


def validate_artifact_or_raise(
    artifact: Dict[str, Any],
    schema_dir: Path,
    expected_artifact_name: str | None = None,
    expected_produced_by: str | None = None,
) -> None:
    is_valid, errors = validate_artifact(
        artifact=artifact,
        schema_dir=schema_dir,
        expected_artifact_name=expected_artifact_name,
        expected_produced_by=expected_produced_by,
    )
    if not is_valid:
        raise ValidationErrorBundle(errors)


def validate_artifact_file(
    artifact_path: Path,
    schema_dir: Path,
    expected_artifact_name: str | None = None,
    expected_produced_by: str | None = None,
) -> Tuple[bool, list[str], Dict[str, Any]]:
    artifact = load_json(artifact_path)
    valid, errors = validate_artifact(
        artifact=artifact,
        schema_dir=schema_dir,
        expected_artifact_name=expected_artifact_name,
        expected_produced_by=expected_produced_by,
    )
    return valid, errors, artifact


def format_validation_report(errors: list[str], artifact_name: str, job_id: str) -> str:
    """Return a human-readable multi-line validation failure report."""
    lines = [
        f"",
        f"  ╔══ VALIDATION FAILED ══════════════════════════════════════════",
        f"  ║  Artifact : {artifact_name}",
        f"  ║  Job ID   : {job_id}",
        f"  ╠───────────────────────────────────────────────────────────────",
    ]
    for i, err in enumerate(errors, 1):
        lines.append(f"  ║  [{i:02d}] {err}")
    lines.append(f"  ╠───────────────────────────────────────────────────────────────")
    lines.append(f"  ║  {len(errors)} error(s) total")
    lines.append(f"  ╚═══════════════════════════════════════════════════════════════")
    return "\n".join(lines)


def save_debug_payload(job_workspace: Path, artifact_name: str, payload: Dict[str, Any]) -> Path:
    """
    Save an invalid artifact payload to the job workspace for debugging.
    The file is NOT a versioned authoritative artifact — it is a debug dump only.
    """
    import datetime
    ts = datetime.datetime.utcnow().strftime("%Y%m%dT%H%M%S%f")
    path = job_workspace / f"{artifact_name}.INVALID_DEBUG.{ts}.json"
    save_json(path, {
        "_debug_note": (
            "Invalid artifact payload — failed schema validation. "
            "This file is NOT authoritative and was NOT written to the stage ledger."
        ),
        "payload": payload,
    })
    return path


def artifact_filename(artifact_name: str, version: int) -> str:
    return f"{artifact_name}.v{version}.json"


def next_artifact_version(job_workspace: Path, artifact_name: str) -> int:
    versions = []
    for path in job_workspace.glob(f"{artifact_name}.v*.json"):
        try:
            version = int(path.stem.split(".v")[-1])
            versions.append(version)
        except ValueError:
            continue
    return max(versions, default=0) + 1


def write_validated_artifact(
    job_workspace: Path,
    artifact: Dict[str, Any],
    schema_dir: Path,
    expected_artifact_name: str | None = None,
    expected_produced_by: str | None = None,
) -> Path:
    validate_artifact_or_raise(
        artifact=artifact,
        schema_dir=schema_dir,
        expected_artifact_name=expected_artifact_name,
        expected_produced_by=expected_produced_by,
    )
    artifact_name = artifact["artifact_name"]
    version = artifact["version"]
    output_path = job_workspace / artifact_filename(artifact_name, version)
    save_json(output_path, artifact)
    return output_path


if __name__ == "__main__":
    repo_root = Path(__file__).resolve().parents[1]
    schema_dir = repo_root / "artifacts" / "schemas"
    fixtures_dir = repo_root / "tests" / "fixtures" / "valid"

    demo_file = fixtures_dir / "request_brief.valid.json"
    valid, errors, artifact = validate_artifact_file(
        demo_file,
        schema_dir=schema_dir,
        expected_artifact_name="request_brief",
        expected_produced_by="Orchestrator",
    )
    print(f"Valid: {valid}")
    if errors:
        print("Errors:")
        for err in errors:
            print(f"- {err}")
    else:
        print(f"Artifact OK: {artifact['artifact_name']} v{artifact['version']}")
