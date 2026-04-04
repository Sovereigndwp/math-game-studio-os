"""
Revision Brief Agent — Stage 12.

Translates a playtest_diagnostic_report into a scoped revision brief:
what to change, what to preserve, what comes next.

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

_BAKERY_REVISION_BRIEF: Dict[str, Any] = {
    "revision_goal": (
        "Restore the causal link between tap and count by delaying the total update "
        "until the flying pastry lands, making the addition visible in the game action."
    ),
    "source_diagnostic_version": 1,
    "scope": {
        "change_now": [
            "Delay running total increment until FlyingPastry animation completes (onComplete callback)",
            "Increase visual prominence of the target number relative to the running total",
            "Extend OVERSHOOT_MS from 700ms to 900ms to give Grade 2 learners time to read the change",
        ],
        "preserve": [
            "Full-screen FeedbackOverlay — do not reduce coverage or duration",
            "CustomerCharacter smile reaction on success — this is a key social reward signal",
            "FlyingPastry arc animation — core of the physical math metaphor",
            "Conveyor belt mechanic — do not touch shift logic",
            "Lives system and patience timer — pass-2 mechanics must stay intact",
        ],
        "out_of_scope": [
            "Belt speed differentiation across shifts — low severity, deferred",
            "Sound effects — audio is out of scope for pass-3",
            "Accessibility attributes — deferred past pass-3",
            "Customer dejection animation on overshoot — not specified in prototype_ui_spec",
        ],
    },
    "next_pass": "pass_3",
    "change_items": [
        {
            "change_id": "R01",
            "area": "math_visibility",
            "description": "Delay the running total increment until FlyingPastry.onComplete fires, not on handleTap.",
            "rationale": "The diagnostic flagged high severity: total updates before the animation confirms it, severing the cause-effect link that is the core of the learning mechanic. Grade 2 learners need to see the item arrive before the count goes up.",
            "priority": "high",
            "acceptance_signal": "Tap a pastry; the running total in the header does NOT change until the flying pastry emoji visibly reaches the box.",
        },
        {
            "change_id": "R02",
            "area": "clarity",
            "description": "Increase the target number font size and add a label ('Goal:' or a target emoji) so it is visually dominant over the running total.",
            "rationale": "Diagnostic flagged medium severity: running total and target number have equal visual weight. Learners need to clearly distinguish 'my count' from 'the target'.",
            "priority": "medium",
            "acceptance_signal": "Target number is visually 1.5x larger than the running total. A first-time player can immediately identify which number is the goal without reading any labels.",
        },
        {
            "change_id": "R03",
            "area": "feedback",
            "description": "Extend OVERSHOOT_MS from 700ms to 900ms across the entire overshoot feedback cycle.",
            "rationale": "Diagnostic flagged medium severity: 700ms is fast for Grade 2 to read the number change. 900ms gives enough time to see the total decrement without breaking the game rhythm.",
            "priority": "medium",
            "acceptance_signal": "Tap one beyond the target; the red overshoot overlay and count decrement are visible for at least 900ms before the game resumes. The number change is readable without replaying.",
        },
    ],
    "constraint_notes": (
        "R01 requires changing when handleTap updates currentTotal — the increment must move "
        "from handleTap into the FlyingPastry.onComplete callback. This must not break "
        "the overshoot check (currentTotal + 1 > target), which currently happens synchronously "
        "in handleTap. The overshoot evaluation must still be based on the intended new value, "
        "even if the displayed total is delayed. Use a 'pendingTotal' pattern: increment the "
        "logical total immediately for game evaluation, but only update displayed total on onComplete. "
        "Do NOT break the conveyor belt, lives, patience timer, or shift logic."
    ),
    "open_questions": [
        "R01: If the player taps again before onComplete fires (during isAnimating), the pendingTotal must be computed correctly. Confirm isAnimating lock is synchronous with handleTap to prevent stacking.",
        "R02: Should 'my count' use a different color from 'goal' to add a second encoding channel? Not specified — default to size alone unless the UI spec is updated.",
    ],
}


_GENERIC_REVISION_BRIEF: Dict[str, Any] = {
    "revision_goal": "Address the highest-severity friction points identified in the diagnostic to improve player clarity and math visibility.",
    "source_diagnostic_version": 1,
    "scope": {
        "change_now": [
            "Fix all high-severity friction points identified in the diagnostic",
        ],
        "preserve": [
            "Core interaction loop",
            "Existing feedback animations that are working",
        ],
        "out_of_scope": [
            "Sound effects",
            "Accessibility attributes",
        ],
    },
    "next_pass": "tuning_only",
    "change_items": [
        {
            "change_id": "R01",
            "area": "clarity",
            "description": "Address primary high-severity clarity issue identified in diagnostic.",
            "rationale": "High-severity friction points directly affect learner comprehension and must be fixed before the game is educationally valid.",
            "priority": "high",
            "acceptance_signal": "Player completes the core action correctly on first attempt without external instruction.",
        },
    ],
    "constraint_notes": "Generic fallback brief — no concept override exists. Add a CONCEPT_OVERRIDES entry for concept-specific revision guidance.",
    "open_questions": [
        "Add a CONCEPT_OVERRIDES entry for this concept to get a precise revision brief.",
    ],
}

CONCEPT_OVERRIDES: Dict[str, Dict[str, Any]] = {
    "bakery": _BAKERY_REVISION_BRIEF,
}


# ---------------------------------------------------------------------------
# Stub
# ---------------------------------------------------------------------------

def revision_brief_stub(context: Dict[str, Any]) -> Dict[str, Any]:
    artifact_inputs = context.get("artifact_inputs", {})
    # Detect concept from playtest_diagnostic session_context or implementation_patch_plan
    diagnostic = artifact_inputs.get("playtest_diagnostic_report", {})
    patch_plan = artifact_inputs.get("implementation_patch_plan", {})
    search_text = (
        diagnostic.get("session_context", {}).get("game_title", "")
        + " "
        + patch_plan.get("patch_objective", "")
    ).lower()

    concept_key = next(
        (key for key in CONCEPT_OVERRIDES if key in search_text),
        None,
    )
    override = CONCEPT_OVERRIDES[concept_key] if concept_key else _GENERIC_REVISION_BRIEF

    return {
        "artifact_name": "revision_brief",
        "produced_by": "Revision Brief Agent",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pass",
        **override,
    }


# ---------------------------------------------------------------------------
# AgentSpec + run entry point
# ---------------------------------------------------------------------------

def build_spec(repo_root: Path) -> AgentSpec:
    return AgentSpec(
        agent_name="revision_brief_agent",
        expected_output_artifact="revision_brief",
        expected_produced_by="Revision Brief Agent",
        prompt_path=repo_root / "agents" / "revision_brief" / "prompt.md",
        config_path=repo_root / "agents" / "revision_brief" / "config.yaml",
        allowed_reads=["playtest_diagnostic_report", "implementation_patch_plan"],
        allowed_writes=["revision_brief"],
        max_revision_count=1,
    )


def run(
    repo_root: Path,
    job_id: str,
    artifact_paths: Dict[str, Any],
    model_callable=None,
) -> Any:
    """Run the Revision Brief Agent.

    Args:
        model_callable: Optional LLM callable. If None, uses the deterministic stub.
    """
    runner = SharedAgentRunner(repo_root)
    return runner.run(
        spec=build_spec(repo_root),
        job_id=job_id,
        artifact_paths=artifact_paths,
        model_callable=model_callable if model_callable is not None else revision_brief_stub,
    )
