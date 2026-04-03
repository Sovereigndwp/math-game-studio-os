from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

# Ensure repo root is on the import path when invoked as scripts/run_benchmarks.py
_REPO_ROOT = Path(__file__).resolve().parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from pipeline import run_v1_pipeline
from utils.llm_caller import make_claude_callable


BENCHMARKS = [
    {
        "id": "bench_01",
        "label": "strong_elementary_bakery",
        "command": "Create a grade 2 bakery game for addition to 20 where students pack pastry orders before customers leave.",
        "expected_outcome": "approved",
        "expected_stop": "lowest_viable_loop_brief",
        "expected_interaction": "combine_and_build",
    },
    {
        "id": "bench_02",
        "label": "strong_middle_fire_dispatch",
        "command": "Create a grade 3 fire station dispatch game where students send the right trucks and supplies to the right locations using arithmetic under time pressure.",
        "expected_outcome": "approved",
        "expected_stop": "lowest_viable_loop_brief",
        "expected_interaction": "route_and_dispatch",
    },
    {
        "id": "bench_03",
        "label": "strong_high_school_unit_circle",
        "command": "Create a high school trigonometry and unit circle pizza lab where students use angle position, radians, and sine/cosine relationships to complete pizza tasks.",
        "expected_outcome": "approved",
        "expected_stop": "lowest_viable_loop_brief",
        "expected_interaction": "navigate_and_position",
    },
    {
        "id": "bench_04",
        "label": "overloaded_bad_concept",
        "command": "Create one giant all-grades game that teaches all math from kindergarten through AP calculus across bakery, airports, hospitals, and farming in one unified world.",
        "expected_outcome": "rejected",
        "expected_stop": "kill_report",
        "expected_interaction": None,
    },
    {
        "id": "bench_05",
        "label": "cute_but_weak_concept",
        "command": "Create a kindergarten puppy adoption game with vague math and unclear mechanics.",
        "expected_outcome": "rejected",
        "expected_stop": "kill_report",
        "expected_interaction": None,
    },
]


@dataclass
class BenchmarkEvaluation:
    bench_id: str
    label: str
    passed: bool
    warnings: list[str]
    failures: list[str]
    outcome: str
    stop_stage: str
    interaction: Optional[str]
    final_artifact_path: Optional[str]


def _safe_read_json(path: Optional[str]) -> dict:
    if not path:
        return {}
    p = Path(path)
    if not p.exists():
        return {}
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _extract_interaction(
    final_artifact_path: Optional[str], repo_root: Path, job_id: Optional[str]
) -> Optional[str]:
    data = _safe_read_json(final_artifact_path)
    artifact_name = data.get("artifact_name")

    if artifact_name == "interaction_decision_memo":
        return data.get("primary_interaction_type")

    if artifact_name == "lowest_viable_loop_brief":
        # Approved run — find interaction_decision_memo via stage ledger
        if not job_id:
            return None
        workspace = repo_root / "memory" / "job_workspaces" / job_id
        ledger_path = workspace / "stage_ledger.json"
        ledger = _safe_read_json(str(ledger_path))
        version = (
            ledger.get("authoritative_versions", {})
            .get("interaction_decision_memo", 0)
        )
        if version:
            interaction_path = workspace / f"interaction_decision_memo.v{version}.json"
            interaction_data = _safe_read_json(str(interaction_path))
            return interaction_data.get("primary_interaction_type")

    return None


def _compare(bench: dict, result, repo_root: Path) -> BenchmarkEvaluation:
    failures: list[str] = []
    warnings: list[str] = []

    actual_outcome = getattr(result, "outcome", "unknown")
    # PipelineResult uses final_artifact_name (not stop_stage)
    actual_stop = getattr(result, "final_artifact_name", "unknown")
    final_artifact_path = getattr(result, "final_artifact_path", None)
    job_id = getattr(result, "job_id", None)

    actual_interaction = _extract_interaction(final_artifact_path, repo_root, job_id)

    if actual_outcome != bench["expected_outcome"]:
        failures.append(
            f"Outcome mismatch: expected '{bench['expected_outcome']}', got '{actual_outcome}'"
        )

    if actual_stop != bench["expected_stop"]:
        failures.append(
            f"Stop-stage mismatch: expected '{bench['expected_stop']}', got '{actual_stop}'"
        )

    expected_interaction = bench["expected_interaction"]
    if expected_interaction and actual_interaction and actual_interaction != expected_interaction:
        warnings.append(
            f"Interaction differs: expected '{expected_interaction}', got '{actual_interaction}'"
        )

    passed = len(failures) == 0

    return BenchmarkEvaluation(
        bench_id=bench["id"],
        label=bench["label"],
        passed=passed,
        warnings=warnings,
        failures=failures,
        outcome=actual_outcome,
        stop_stage=actual_stop,
        interaction=actual_interaction,
        final_artifact_path=final_artifact_path,
    )


def _print_result(ev: BenchmarkEvaluation) -> None:
    mark = "PASS" if ev.passed else "FAIL"
    print(f"\n[{mark}] {ev.bench_id} · {ev.label}")
    print(f"  outcome:      {ev.outcome}")
    print(f"  stop_stage:   {ev.stop_stage}")
    print(f"  interaction:  {ev.interaction or 'n/a'}")
    if ev.final_artifact_path:
        print(f"  artifact:     {ev.final_artifact_path}")

    for f in ev.failures:
        print(f"  x {f}")
    for w in ev.warnings:
        print(f"  ! {w}")


def _build_report(
    results: list[BenchmarkEvaluation], use_llm: bool, model: Optional[str]
) -> str:
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC")
    mode = "LLM" if use_llm else "stub"
    model_line = model if model else "n/a"
    passed = sum(1 for r in results if r.passed)
    total = len(results)

    lines = [
        "# Benchmark Regression Report",
        "",
        f"- Generated: {ts}",
        f"- Mode: {mode}",
        f"- Model: {model_line}",
        f"- Result: {passed}/{total} passed",
        "",
        "| ID | Label | Outcome | Stop Stage | Interaction | Pass |",
        "|---|---|---|---|---|---|",
    ]

    for r in results:
        lines.append(
            f"| {r.bench_id} | {r.label} | {r.outcome} | {r.stop_stage} "
            f"| {r.interaction or 'n/a'} | {'✓' if r.passed else '✗'} |"
        )

    lines.append("")
    lines.append("## Details")
    for r in results:
        lines.append("")
        lines.append(f"### {r.bench_id} · {r.label}")
        lines.append(f"- outcome: {r.outcome}")
        lines.append(f"- stop_stage: {r.stop_stage}")
        lines.append(f"- interaction: {r.interaction or 'n/a'}")
        if r.final_artifact_path:
            lines.append(f"- final_artifact_path: `{r.final_artifact_path}`")
        if r.failures:
            lines.append("- failures:")
            for f in r.failures:
                lines.append(f"  - {f}")
        if r.warnings:
            lines.append("- warnings:")
            for w in r.warnings:
                lines.append(f"  - {w}")
        if not r.failures and not r.warnings:
            lines.append("- notes: clean pass")

    return "\n".join(lines) + "\n"


def run(
    use_llm: bool = False, save_report: bool = False, model: Optional[str] = None
) -> int:
    repo_root = _REPO_ROOT

    model_callable = None
    if use_llm:
        model_callable = make_claude_callable(model=model or "claude-sonnet-4-6")

    results: list[BenchmarkEvaluation] = []

    print("=== Math Game Studio OS — Benchmark Regression Runner ===")
    print(f"Mode: {'LLM' if use_llm else 'stub'}")
    if use_llm:
        print(f"Model: {model or 'claude-sonnet-4-6'}")

    for bench in BENCHMARKS:
        print(f"\nRunning {bench['id']} · {bench['label']}")
        result = run_v1_pipeline(
            raw_command=bench["command"],
            repo_root=repo_root,
            model_callable=model_callable,
        )
        ev = _compare(bench, result, repo_root)
        results.append(ev)
        _print_result(ev)

    passed = sum(1 for r in results if r.passed)
    total = len(results)

    print(f"\n=== Summary: {passed}/{total} passed ===")

    if save_report:
        report = _build_report(results, use_llm=use_llm, model=model)
        reports_dir = repo_root / "reports"
        reports_dir.mkdir(parents=True, exist_ok=True)
        suffix = "llm" if use_llm else "stub"
        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        report_path = reports_dir / f"benchmark_regression_{suffix}_{ts}.md"
        report_path.write_text(report, encoding="utf-8")
        print(f"Report written: {report_path}")

    return 0 if passed == total else 1


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Run Math Game Studio OS benchmark regression suite."
    )
    parser.add_argument("--llm", action="store_true", help="Run using live LLM mode.")
    parser.add_argument(
        "--report", action="store_true", help="Write a markdown report to reports/."
    )
    parser.add_argument(
        "--model", default=None, help="Claude model name for LLM mode."
    )
    args = parser.parse_args()
    return run(use_llm=args.llm, save_report=args.report, model=args.model)


if __name__ == "__main__":
    raise SystemExit(main())
