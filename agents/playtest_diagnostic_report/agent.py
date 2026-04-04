"""
Playtest Diagnostic Agent — Stage 11.

Inspects a completed playable pass and produces a structured diagnostic report:
what is working, what is broken, where pacing drags, and what comes next.

Modes:
    Stub: deterministic Bakery Pass 3 override + generic fallback.
    LLM:  model_callable replaces the stub.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from utils.shared_agent_runner import AgentSpec, SharedAgentRunner


# ---------------------------------------------------------------------------
# Concept-specific overrides
# ---------------------------------------------------------------------------

_BAKERY_DIAGNOSTIC: Dict[str, Any] = {
    "session_context": {
        "pass_number": "pass-3",
        "game_title": "Bakery Rush",
        "grade_target": "Grade 2 (ages 7-8)",
        "math_concept": "Addition to 20",
        "tester_notes": (
            "Evaluated Pass 3 build: CustomerCharacter reaction, FeedbackOverlay full-screen, "
            "FlyingPastry arc animation, game-shake on overshoot. Single-session review against "
            "acceptance signals from implementation_patch_plan."
        ),
    },
    "strength_signals": [
        "Flying pastry arc animation gives immediate, satisfying confirmation that a tap was registered — the math action (adding an item) has clear physical consequence.",
        "Full-screen FeedbackOverlay on success is unmissable. Grade 2 learners cannot miss the reward signal — it covers the viewport.",
        "Customer character smile on success creates a social reward loop. The learner is helping someone, not just solving an abstract number problem.",
        "Overshoot shake + red overlay clearly communicates 'wrong direction' without text. Pre-readers can parse it.",
        "Patience timer creates meaningful urgency without being punishing — the first 3 shifts are long enough for new learners.",
    ],
    "friction_points": [
        {
            "area": "clarity",
            "description": "The running total counter in the header is small relative to the customer target number. New learners may not track which number is 'mine' vs 'theirs'.",
            "suspected_cause": "Header layout gives equal visual weight to total and target. Target should be larger and more prominent.",
            "severity": "medium",
        },
        {
            "area": "feedback",
            "description": "Overshoot feedback disappears after 700ms, which is fast. Learners who overshoot may not understand *why* the count went back down.",
            "suspected_cause": "OVERSHOOT_MS=700 was tuned for feel, not comprehension. Grade 2 may need 900-1000ms to read the number change.",
            "severity": "medium",
        },
        {
            "area": "pacing",
            "description": "Shift 1 patience timer (longest duration) combined with simple targets (3-5 items) means the first shift has almost no pressure. The game starts too slow.",
            "suspected_cause": "The patience timer and difficulty curve were designed independently. Low difficulty + long patience = zero urgency in Shift 1.",
            "severity": "low",
        },
        {
            "area": "math_visibility",
            "description": "When items fly into the box, the running total updates before the animation lands. The math (adding 1 to the count) happens before the visual confirms it. This severs the cause-effect link.",
            "suspected_cause": "State update is synchronous; animation is asynchronous. Total increments in handleTap before FlyingPastry reaches the box.",
            "severity": "high",
        },
        {
            "area": "feel",
            "description": "The conveyor belt moves at a constant speed regardless of shift. Higher shifts should feel visibly faster — right now the speed difference is subtle.",
            "suspected_cause": "BELT_SPEED constants across shifts may not have enough spread. Visual speed difference needs to be perceptible to a 7-year-old.",
            "severity": "low",
        },
    ],
    "feel_scores": {
        "immediacy": 4,
        "clarity": 3,
        "reward_rhythm": 4,
        "math_visibility": 3,
        "overall_rating": 4,
        "score_notes": (
            "Immediacy and reward rhythm are strong — the game responds quickly and success feels good. "
            "Clarity and math_visibility are the weak points: the learner can score correctly without "
            "consciously tracking the math, and the running total competes visually with the target. "
            "Overall the game feels alive but has two fixable gaps that directly affect learning."
        ),
    },
    "pattern_summary": (
        "Pass 3 successfully makes the game feel real: the arc animation, full-screen overlay, and "
        "customer reaction all land. The dominant weakness is math visibility — the running total "
        "updates before the animation confirms it, severing the cause-effect link that is the core "
        "of the learning mechanic. A targeted revision to delay the count update until the pastry "
        "lands, plus a stronger visual hierarchy on the target number, would close the gap."
    ),
    "recommended_action": "revise_current_pass",
}


_GENERIC_DIAGNOSTIC: Dict[str, Any] = {
    "session_context": {
        "pass_number": "pass-1",
        "game_title": "Unknown Game",
        "grade_target": "Unknown",
        "math_concept": "Unknown",
        "tester_notes": "Generic fallback diagnostic — no concept override exists for this concept.",
    },
    "strength_signals": [
        "Core loop is functional — the primary interaction registers and advances game state.",
        "Session complete screen provides a clear end point.",
    ],
    "friction_points": [
        {
            "area": "clarity",
            "description": "No concept-specific override exists. Diagnostic is generic and may not reflect actual playtest conditions.",
            "suspected_cause": "Missing CONCEPT_OVERRIDES entry for this concept.",
            "severity": "low",
        },
    ],
    "feel_scores": {
        "immediacy": 3,
        "clarity": 3,
        "reward_rhythm": 3,
        "math_visibility": 3,
        "overall_rating": 3,
        "score_notes": "Generic baseline. Add a CONCEPT_OVERRIDES entry for concept-specific scoring.",
    },
    "pattern_summary": (
        "Generic diagnostic produced — no concept-specific override found. "
        "Add a CONCEPT_OVERRIDES entry for this concept to get a precise diagnostic report."
    ),
    "recommended_action": "revise_current_pass",
}

CONCEPT_OVERRIDES: Dict[str, Dict[str, Any]] = {
    "bakery": _BAKERY_DIAGNOSTIC,
}


# ---------------------------------------------------------------------------
# Stub
# ---------------------------------------------------------------------------

def playtest_diagnostic_stub(context: Dict[str, Any]) -> Dict[str, Any]:
    artifact_inputs = context.get("artifact_inputs", {})
    # Detect concept from implementation_patch_plan patch_objective or implementation_plan goal
    patch_plan = artifact_inputs.get("implementation_patch_plan", {})
    impl_plan = artifact_inputs.get("implementation_plan", {})
    search_text = (
        patch_plan.get("patch_objective", "")
        + " "
        + impl_plan.get("implementation_goal", "")
        + " "
        + " ".join(f.get("path", "") for f in impl_plan.get("file_plan", []))
    ).lower()

    concept_key = next(
        (key for key in CONCEPT_OVERRIDES if key in search_text),
        None,
    )
    override = CONCEPT_OVERRIDES[concept_key] if concept_key else _GENERIC_DIAGNOSTIC

    return {
        "artifact_name": "playtest_diagnostic_report",
        "produced_by": "Playtest Diagnostic Agent",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pass",
        **override,
    }


# ---------------------------------------------------------------------------
# AgentSpec + run entry point
# ---------------------------------------------------------------------------

def build_spec(repo_root: Path) -> AgentSpec:
    return AgentSpec(
        agent_name="playtest_diagnostic_agent",
        expected_output_artifact="playtest_diagnostic_report",
        expected_produced_by="Playtest Diagnostic Agent",
        prompt_path=repo_root / "agents" / "playtest_diagnostic_report" / "prompt.md",
        config_path=repo_root / "agents" / "playtest_diagnostic_report" / "config.yaml",
        allowed_reads=["implementation_patch_plan", "implementation_plan"],
        allowed_writes=["playtest_diagnostic_report"],
        max_revision_count=1,
    )


def run(
    repo_root: Path,
    job_id: str,
    artifact_paths: Dict[str, Any],
    model_callable=None,
) -> Any:
    """Run the Playtest Diagnostic Agent.

    Args:
        model_callable: Optional LLM callable. If None, uses the deterministic stub.
    """
    runner = SharedAgentRunner(repo_root)
    return runner.run(
        spec=build_spec(repo_root),
        job_id=job_id,
        artifact_paths=artifact_paths,
        model_callable=model_callable if model_callable is not None else playtest_diagnostic_stub,
    )
