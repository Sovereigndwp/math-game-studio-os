from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from utils.shared_agent_runner import AgentSpec, SharedAgentRunner


def intake_framing_stub(context: Dict[str, Any]) -> Dict[str, Any]:
    request_brief = context["artifact_inputs"]["request_brief"]
    raw = request_brief["raw_user_command"]

    concept = raw.strip()
    likely_age_band = "unknown"
    likely_grade_band = "unknown"
    likely_course_band = "unknown"
    likely_math_domain = "unknown"
    possible_profession = "unknown mission"
    possible_world_theme = "unknown world"
    emotional_hook = "solve a meaningful task"
    likely_factory_type = "age_band_specialist"
    interaction_candidates = []

    text = raw.lower()
    if "grade 1" in text or "grade 2" in text or "grade 3" in text or "grade 4" in text or "grade 5" in text or "elementary" in text:
        likely_age_band = "5_to_8"
        likely_grade_band = "elementary"
        likely_course_band = "elementary_arithmetic"
        likely_factory_type = "universal_ladder"
    elif "grade 6" in text or "grade 7" in text or "grade 8" in text or "middle school" in text:
        likely_age_band = "11_to_14"
        likely_grade_band = "middle_school"
        likely_course_band = "middle_school_math"
        likely_factory_type = "age_band_specialist"
    elif "high school" in text:
        likely_age_band = "14_to_18"
        likely_grade_band = "high_school"
        likely_course_band = "high_school_math"
        likely_factory_type = "advanced_anchor"

    if "bakery" in text or "pastry" in text:
        possible_profession = "bakery helper"
        possible_world_theme = "busy bakery counter"
        emotional_hook = "serve customers before they leave"
        interaction_candidates = ["combine_and_build"]
    elif "fire" in text or "dispatch" in text:
        possible_profession = "dispatch coordinator"
        possible_world_theme = "fire station control room"
        emotional_hook = "send the right help fast"
        interaction_candidates = ["route_and_dispatch"]
    elif "unit circle" in text or "pizza" in text:
        possible_profession = "pizza lab operator"
        possible_world_theme = "unit circle pizza lab"
        emotional_hook = "master angles and motion through slicing and rotation"
        interaction_candidates = ["navigate_and_position", "transform_and_manipulate"]

    if "addition" in text or "arithmetic" in text:
        likely_math_domain = "addition"
    elif "ratio" in text or "rate" in text:
        likely_math_domain = "ratios_and_rates"
    elif "unit circle" in text or "radians" in text or "sine" in text or "cosine" in text:
        likely_math_domain = "trigonometry"

    return {
        "status": "pass",
        "timestamp": "2026-04-03T12:01:00Z",
        "plain_english_concept": concept,
        "likely_age_band": likely_age_band,
        "likely_grade_band": likely_grade_band,
        "likely_course_band": likely_course_band,
        "likely_math_domain": likely_math_domain,
        "likely_target_skills": [likely_math_domain] if likely_math_domain != "unknown" else [],
        "possible_profession_or_mission": possible_profession,
        "possible_world_theme": possible_world_theme,
        "possible_emotional_hook": emotional_hook,
        "likely_factory_type": likely_factory_type,
        "possible_interaction_candidates": interaction_candidates,
        "one_sentence_promise_draft": concept,
        "ambiguities_detected": [],
        "confidence_scores": {
            "age_fit": 0.8 if likely_age_band != "unknown" else 0.4,
            "math_fit": 0.8 if likely_math_domain != "unknown" else 0.4,
            "theme_fit": 0.8 if possible_profession != "unknown mission" else 0.4,
        },
        "notes": "Initial framing stub output.",
    }


def build_spec(repo_root: Path) -> AgentSpec:
    return AgentSpec(
        agent_name="intake_framing_agent",
        expected_output_artifact="intake_brief",
        expected_produced_by="Intake and Framing Agent",
        prompt_path=repo_root / "agents" / "intake_framing" / "prompt.md",
        config_path=repo_root / "agents" / "intake_framing" / "config.yaml",
        allowed_reads=["request_brief"],
        allowed_writes=["intake_brief"],
        max_revision_count=2,
    )


def run(
    repo_root: Path,
    job_id: str,
    artifact_paths: Dict[str, Path],
    model_callable=None,
):
    """Run the Intake and Framing Agent.

    Args:
        model_callable: Optional override. If provided, replaces the stub (e.g., a Claude
                        API callable from utils.llm_caller.make_claude_callable()).
                        If None, uses the deterministic stub for development and testing.
    """
    runner = SharedAgentRunner(repo_root)
    return runner.run(
        spec=build_spec(repo_root),
        job_id=job_id,
        artifact_paths=artifact_paths,
        model_callable=model_callable if model_callable is not None else intake_framing_stub,
    )
