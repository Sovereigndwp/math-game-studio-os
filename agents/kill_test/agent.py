from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from utils.shared_agent_runner import AgentSpec, SharedAgentRunner


VALID_INTERACTION_CANDIDATES = {
    "route_and_dispatch",
    "combine_and_build",
    "allocate_and_balance",
    "transform_and_manipulate",
    "navigate_and_position",
    "sequence_and_predict",
}

# Signals that a concept is trying to cover multiple incompatible domains simultaneously.
# Any concept that matches >= OVERLOAD_SIGNAL_THRESHOLD of these is structurally unfixable
# and should be rejected outright rather than sent for redesign.
_OVERLOAD_PHRASES = [
    "all grades", "every grade", "all ages", "every age", "kindergarten through",
    "every math", "all math", "every concept", "all concepts", "every topic",
    "all topics", "entire curriculum", "all subjects",
    "unified world", "single unified", "one giant", "one app for all",
]
_OVERLOAD_THEME_MARKERS = [
    "bakery", "airport", "hospital", "robot", "farm", "space", "ocean",
    "jungle", "city", "castle", "lab", "factory",
]
_OVERLOAD_SIGNAL_THRESHOLD = 2   # structural overload phrases needed to trigger reject
_OVERLOAD_THEME_THRESHOLD = 3    # distinct world-theme keywords needed to flag theme overload


def _detect_overload(concept_text: str, ambiguities: list) -> tuple[bool, str]:
    """Return (is_overloaded, reason) based on concept scope signals."""
    text = concept_text.lower()
    structural_hits = [p for p in _OVERLOAD_PHRASES if p in text]
    theme_hits = [t for t in _OVERLOAD_THEME_MARKERS if t in text]

    if len(structural_hits) >= _OVERLOAD_SIGNAL_THRESHOLD:
        return True, (
            f"Concept contains {len(structural_hits)} scope-overload signals "
            f"({', '.join(structural_hits[:3])}). No single family boundary can contain this concept."
        )
    if len(theme_hits) >= _OVERLOAD_THEME_THRESHOLD:
        return True, (
            f"Concept references {len(theme_hits)} distinct world themes "
            f"({', '.join(theme_hits[:4])}). A game cannot have a coherent identity with this many themes."
        )
    return False, ""


def _score(value: float, reason: str) -> Dict[str, Any]:
    return {"score": round(value, 2), "reason": reason}


def kill_test_stub(context: Dict[str, Any]) -> Dict[str, Any]:
    intake = context["artifact_inputs"]["intake_brief"]

    concept = intake.get("plain_english_concept", "")
    math_domain = intake.get("likely_math_domain", "unknown")
    age_band = intake.get("likely_age_band", "unknown")
    mission = intake.get("possible_profession_or_mission", "unknown mission")
    world_theme = intake.get("possible_world_theme", "unknown world")
    one_sentence = intake.get("one_sentence_promise_draft", "")
    interaction_candidates = intake.get("possible_interaction_candidates", [])
    ambiguities = intake.get("ambiguities_detected", [])
    confidence = intake.get("confidence_scores", {})

    age_confidence = confidence.get("age_fit", 0.5)
    math_confidence = confidence.get("math_fit", 0.5)
    theme_confidence = confidence.get("theme_fit", 0.5)

    # --- Clarity: 10-second test ---
    has_clear_action = bool(one_sentence.strip() and len(one_sentence) > 15)
    has_world = world_theme != "unknown world"
    clarity_score = 0.5
    if has_clear_action and has_world:
        clarity_score = 0.85
    elif has_clear_action or has_world:
        clarity_score = 0.65
    clarity_reason = (
        "Clear world and action present in one-sentence promise."
        if clarity_score >= 0.8
        else "Concept survives a 10-second read but lacks specificity."
        if clarity_score >= 0.6
        else "Concept is too vague to pass a cold 10-second read."
    )

    # --- Interaction fit first pass ---
    valid_candidates = [c for c in interaction_candidates if c in VALID_INTERACTION_CANDIDATES]
    interaction_score = 0.75 if valid_candidates else 0.4
    interaction_reason = (
        f"Plausible interaction candidates identified: {', '.join(valid_candidates)}."
        if valid_candidates
        else "No valid interaction candidates surfaced in framing. Interaction fit unclear."
    )

    # --- Loop obviousness ---
    loop_score = 0.7 if math_confidence >= 0.7 else 0.45
    loop_reason = (
        f"Math domain '{math_domain}' has a natural repeating action pattern."
        if loop_score >= 0.65
        else f"Math domain '{math_domain}' is unclear or too broad to guarantee an obvious loop."
    )

    # --- Teacher value immediacy ---
    teacher_score = 0.75 if (math_confidence >= 0.6 and age_confidence >= 0.6) else 0.5
    teacher_reason = (
        "Age-appropriate math domain identified — teacher value is immediate."
        if teacher_score >= 0.7
        else "Age band or math domain needs more definition before teacher value is clear."
    )

    # --- Replay potential ---
    has_mission = mission != "unknown mission"
    replay_score = 0.75 if (has_mission and math_confidence >= 0.6) else 0.5
    replay_reason = (
        f"Mission context '{mission}' creates natural difficulty escalation."
        if replay_score >= 0.7
        else "Replay structure unclear — escalation path not visible from framing."
    )

    # --- Final decision ---
    scores = [clarity_score, interaction_score, loop_score, teacher_score, replay_score]
    avg = sum(scores) / len(scores)
    min_score = min(scores)
    below_threshold_count = sum(1 for s in scores if s < 0.5)

    # Check structural overload before scoring — these concepts are never fixable by revision
    is_overloaded, overload_reason = _detect_overload(concept, ambiguities)

    if is_overloaded:
        status = "reject"
        strongest_failure = overload_reason
        redesign_direction = ""
        final_note = (
            "Reject. Concept scope is too broad to belong to any single family. "
            "This is not a framing problem — it is a structural problem. "
            "Split into separate, focused game concepts."
        )
    elif min_score < 0.40 or (below_threshold_count >= 3 and avg < 0.50):
        # Multiple dimensions fail or a single dimension is definitively broken
        status = "reject"
        strongest_failure = (
            f"Concept fails {below_threshold_count} Kill Fast dimensions at a level "
            "that redesign cannot recover. Interaction identity is absent or entirely decorative."
        )
        redesign_direction = ""
        final_note = (
            f"Reject. Average score {avg:.2f}, minimum score {min_score:.2f}. "
            "Too weak across multiple dimensions to salvage with targeted revision."
        )
    elif min_score < 0.5 or avg < 0.60:
        status = "redesign"
        weakest_label = [
            ("clarity", clarity_score),
            ("interaction_fit", interaction_score),
            ("loop_obviousness", loop_score),
            ("teacher_value", teacher_score),
            ("replay_potential", replay_score),
        ]
        weakest_label.sort(key=lambda x: x[1])
        weakest_name = weakest_label[0][0]
        strongest_failure = f"Kill Fast dimension '{weakest_name}' is below threshold."
        redesign_direction = (
            f"Strengthen the {weakest_name} dimension. Revisit framing and resubmit."
        )
        final_note = (
            "Redesign required. Core idea may be viable but critical dimension "
            "needs clarification before advancing."
        )
    else:
        status = "pass"
        strongest_failure = ""
        redesign_direction = ""
        final_note = (
            f"Pass. Concept clears all five Kill Fast questions with average score {avg:.2f}. "
            "Advance to Interaction Mapper."
        )

    # Pattern comparisons
    failure_patterns = []
    success_patterns = []
    if not valid_candidates:
        failure_patterns.append("no_clear_interaction_candidate")
    if len(ambiguities) >= 3:
        failure_patterns.append("high_ambiguity_framing")
    if math_confidence >= 0.75 and theme_confidence >= 0.75:
        success_patterns.append("strong_math_and_theme_alignment")
    if valid_candidates and math_confidence >= 0.7:
        success_patterns.append("interaction_math_coherence")

    return {
        "status": status,
        "timestamp": "2026-04-03T12:02:00Z",
        "clarity_10_second_test": _score(clarity_score, clarity_reason),
        "interaction_fit_first_pass": _score(interaction_score, interaction_reason),
        "loop_obviousness": _score(loop_score, loop_reason),
        "teacher_value_immediacy": _score(teacher_score, teacher_reason),
        "replay_potential": _score(replay_score, replay_reason),
        "strongest_failure_reason": strongest_failure,
        "redesign_direction": redesign_direction,
        "comparison_to_known_failure_patterns": failure_patterns,
        "comparison_to_known_success_patterns": success_patterns,
        "final_decision_note": final_note,
    }


def build_spec(repo_root: Path) -> AgentSpec:
    return AgentSpec(
        agent_name="kill_test_agent",
        expected_output_artifact="kill_report",
        expected_produced_by="Kill Test Agent",
        prompt_path=repo_root / "agents" / "kill_test" / "prompt.md",
        config_path=repo_root / "agents" / "kill_test" / "config.yaml",
        allowed_reads=["intake_brief"],
        allowed_writes=["kill_report"],
        max_revision_count=2,
    )


def run(
    repo_root: Path,
    job_id: str,
    artifact_paths: Dict[str, Path],
    model_callable=None,
):
    """Run the Kill Test Agent.

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
        model_callable=model_callable if model_callable is not None else kill_test_stub,
    )
