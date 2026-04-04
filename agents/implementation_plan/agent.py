"""
Implementation Plan Agent — Stage 9.

Translates approved prototype specs into an engineering blueprint:
file plan, component plan, state plan, data config, animation ownership, and test plan.

Reads from: prototype_ui_spec, prototype_build_spec, prototype_spec
Writes:     implementation_plan

Modes:
    Stub: reads upstream artifacts and derives a concrete plan from their content.
    LLM:  model_callable replaces the stub.
"""
from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from utils.shared_agent_runner import AgentSpec, SharedAgentRunner


ARTIFACT_NAME = "implementation_plan"
PRODUCED_BY = "Implementation Plan Agent"


# ---------------------------------------------------------------------------
# Core builder — derives plan from upstream artifact content
# ---------------------------------------------------------------------------

def build_implementation_plan(
    prototype_ui_spec: Dict[str, Any],
    prototype_build_spec: Dict[str, Any],
    prototype_spec: Dict[str, Any],
) -> Dict[str, Any]:
    """
    Deterministic builder for implementation_plan.

    Reads upstream artifact fields to produce:
    - implementation_goal
    - build_scope (must/can stub/must not build)
    - file_plan
    - component_plan
    - state_plan
    - data_config_plan
    - animation_plan
    - test_plan
    - integration_notes, risks_and_unknowns, open_questions
    """

    prototype_goal = prototype_spec.get("prototype_goal", "")

    # Try field first, then extract from prototype_goal (e.g. "combine_and_build loop")
    interaction_type = (
        prototype_spec.get("interaction_model", {}).get("primary_interaction_type")
        or (re.search(r"([a-z]+(?:_[a-z]+)+)\s+loop", prototype_goal or "") or
            type("", (), {"group": lambda self, _: None})()).group(1)
        or "interactive"
    )

    file_plan = [
        {
            "path": "preview/src/App.jsx",
            "action": "update",
            "purpose": "Mount the current game prototype entry component.",
        },
        {
            "path": "preview/src/games/BakeryRushPrototype.jsx",
            "action": "create",
            "purpose": "Own the main playable prototype container and stage-level behavior.",
        },
        {
            "path": "preview/src/games/bakery/levelConfig.js",
            "action": "create",
            "purpose": "Store level tuning values, target pools, and pastry weighting in data.",
        },
        {
            "path": "preview/src/games/bakery/components/OrderTicket.jsx",
            "action": "create",
            "purpose": "Render target order information, customer identity, and status cues.",
        },
        {
            "path": "preview/src/games/bakery/components/ConveyorBelt.jsx",
            "action": "create",
            "purpose": "Render moving pastry choices and own tap-to-select interaction surface.",
        },
        {
            "path": "preview/src/games/bakery/components/PastryBox.jsx",
            "action": "create",
            "purpose": "Render current box contents, running total feedback, and success/overshoot visuals.",
        },
        {
            "path": "preview/src/games/bakery/components/ShiftHUD.jsx",
            "action": "create",
            "purpose": "Render lives, score, timers, queue preview, and level progress.",
        },
        {
            "path": "preview/src/games/bakery/components/FeedbackOverlay.jsx",
            "action": "create",
            "purpose": "Render dominant success, overshoot, and end-of-shift feedback states.",
        },
        {
            "path": "preview/src/games/bakery/styles.css",
            "action": "create",
            "purpose": "Contain prototype-scoped layout, motion, and readability styling.",
        },
    ]

    component_plan = [
        {
            "component_name": "BakeryRushPrototype",
            "responsibility": "Own top-level game state, level progression, and stage transitions.",
            "inputs": ["level config", "prototype rules"],
            "outputs": ["screen state", "shared game state", "child component props"],
        },
        {
            "component_name": "OrderTicket",
            "responsibility": "Display current customer, target value, and immediate order context.",
            "inputs": ["current target", "customer state", "message"],
            "outputs": ["visual order context"],
        },
        {
            "component_name": "ConveyorBelt",
            "responsibility": "Display moving pastry items and emit player selection events.",
            "inputs": ["pastry items", "conveyor speed", "interaction enabled state"],
            "outputs": ["pastry selected event"],
        },
        {
            "component_name": "PastryBox",
            "responsibility": "Display selected pastries, running total, and overshoot/success response.",
            "inputs": ["box items", "current total", "feedback state"],
            "outputs": ["visual consequence of player action"],
        },
        {
            "component_name": "ShiftHUD",
            "responsibility": "Display score, patience, lives, queue preview, and level progress.",
            "inputs": ["score", "timers", "lives", "queue", "level"],
            "outputs": ["persistent situational awareness"],
        },
        {
            "component_name": "FeedbackOverlay",
            "responsibility": "Display screen-dominant success, fail, and completion states.",
            "inputs": ["feedback mode", "customer reaction", "summary stats"],
            "outputs": ["dominant state feedback"],
        },
    ]

    state_plan = {
        "local_state": [
            {
                "name": "screenState",
                "type": "string",
                "initial_value": "PLAYING",
                "updated_by": ["level completion", "game over", "overlay triggers"],
            },
            {
                "name": "levelIndex",
                "type": "number",
                "initial_value": "0",
                "updated_by": ["level unlock on score threshold"],
            },
            {
                "name": "score",
                "type": "number",
                "initial_value": "0",
                "updated_by": ["first-try bonus", "streak bonus", "order completion"],
            },
            {
                "name": "lives",
                "type": "number",
                "initial_value": "3",
                "updated_by": ["missed order (patience expired)"],
            },
            {
                "name": "currentTarget",
                "type": "number",
                "initial_value": "drawn from level config target pool",
                "updated_by": ["new customer load"],
            },
            {
                "name": "currentTotal",
                "type": "number",
                "initial_value": "0",
                "updated_by": ["valid pastry tap", "overshoot bounce-back", "order reset"],
            },
            {
                "name": "feedbackMode",
                "type": "string | null",
                "initial_value": "null",
                "updated_by": ["exact match → success", "overshoot → overshoot", "timeout → miss"],
            },
            {
                "name": "patienceLeft",
                "type": "number",
                "initial_value": "level config patience value",
                "updated_by": ["timer tick", "new order reset"],
            },
            {
                "name": "streak",
                "type": "number",
                "initial_value": "0",
                "updated_by": ["first-try success increment", "miss or overshoot reset"],
            },
        ],
        "derived_state": [
            {
                "name": "currentLevelConfig",
                "derived_from": "levelConfigs[levelIndex]",
                "description": "Active level rules: speed, targets, pastry weights, patience, score threshold.",
            },
            {
                "name": "patiencePercent",
                "derived_from": "patienceLeft / currentLevelConfig.patience",
                "description": "Used to drive the patience progress bar width.",
            },
            {
                "name": "nextLevelUnlocked",
                "derived_from": "score >= currentLevelConfig.scoreThreshold",
                "description": "True when the player has reached the score needed to advance.",
            },
        ],
        "state_ownership_notes": (
            "Top-level game container (BakeryRushPrototype) owns all session state, "
            "scoring, timers, queue, and level progression. Child components receive "
            "props and emit events — they own no gameplay logic."
        ),
    }

    data_config_plan = {
        "config_objects": [
            {
                "name": "levelConfigs",
                "file_path": "preview/src/games/bakery/levelConfig.js",
                "description": (
                    "Array of 5 level configs: each has conveyorSpeed, targetPool, "
                    "pastryWeights, patience, scoreThreshold, streakBonus."
                ),
            },
            {
                "name": "pastryValueMap",
                "file_path": "preview/src/games/bakery/levelConfig.js",
                "description": "Maps pastry emoji/id to its numeric value (e.g., croissant=1, donut=2).",
            },
        ],
        "hardcoded_only_if_temporary": [
            "Placeholder customer names and emoji — temporary art assets.",
            "Overlay copy text (e.g., 'Great Job!', 'Too many!') — will move to a content config.",
            "Prototype overlay duration values (SUCCESS_MS, OVERSHOOT_MS) — inline for now.",
        ],
        "future_extraction_notes": (
            "Level tuning, pastry frequency tables, target pools, and score thresholds "
            "should move to a separate data JSON once the game supports teacher customization "
            "or difficulty selection."
        ),
    }

    animation_plan = [
        {
            "animation_name": "conveyor_motion",
            "owner": "ConveyorBelt",
            "trigger": "active play state",
            "implementation_note": (
                "Continuous side-scroll owned by ConveyorBelt, driven by "
                "currentLevelConfig.conveyorSpeed. Use CSS animation with duration "
                "set as CSS custom property --belt-duration."
            ),
        },
        {
            "animation_name": "flying_pastry_to_box",
            "owner": "BakeryRushPrototype",
            "trigger": "valid pastry tap",
            "implementation_note": (
                "Top-level container coordinates source-to-target animation because "
                "it crosses the ConveyorBelt → PastryBox boundary. Use "
                "getBoundingClientRect at tap time to compute --dx/--dy. "
                "Element is position: fixed during flight."
            ),
        },
        {
            "animation_name": "overshoot_bounce_back",
            "owner": "PastryBox",
            "trigger": "currentTotal > currentTarget",
            "implementation_note": (
                "Box visually rejects the last item with a shake keyframe. "
                "Decrement currentTotal after OVERSHOOT_MS. Do not obscure the "
                "running total — the number change must be readable."
            ),
        },
        {
            "animation_name": "success_overlay_entry",
            "owner": "FeedbackOverlay",
            "trigger": "currentTotal === currentTarget (exact match)",
            "implementation_note": (
                "Overlay enters with a scale-in keyframe (0.85 → 1.0, 200ms). "
                "Holds for SUCCESS_MS, then releases back to new order state."
            ),
        },
    ]

    test_plan = {
        "manual_checks": [
            "Player understands the target and main tap zone within 10 seconds of first seeing the game.",
            "Tapped pastry visibly travels from the belt to the box in a way that reinforces adding.",
            "Success feedback is screen-dominant and easy to interpret without reading.",
            "Overshoot feedback is noticeable without feeling punitive — total decrements visibly.",
            "Level 4 clearly feels like a speed upgrade, not random confusion.",
        ],
        "logic_checks": [
            "Running total always matches the sum of pastry values in the box.",
            "Score awards follow first-try and streak rules exactly as defined in levelConfig.",
            "Lives decrease only on missed orders (patience expired), not on overshoot.",
            "Level unlock fires only after score reaches currentLevelConfig.scoreThreshold.",
        ],
        "edge_case_checks": [
            "Rapid multiple taps do not corrupt box total or trigger duplicate state transitions.",
            "Timers pause or transition correctly during overlays and end states.",
            "Next customer loads cleanly after success, miss, or level advance.",
            "Conveyor replacement items do not break tap handling when selected repeatedly.",
        ],
    }

    integration_notes = [
        "Preview app (preview/) is the live development surface — game files live under preview/src/games/.",
        "Static pass exports (previews/bakery/pass-N.html) are separate from the preview app source — do not conflate them.",
        "Component structure should support later pass export without redesigning game logic.",
        "Do not touch: pipeline.py, engine/gate_engine.py, agents/, artifacts/schemas/, orchestrator/, utils/, scripts/run_benchmarks.py.",
    ]

    risks_and_unknowns = [
        "Cross-component flying-item animation requires a shared coordinate strategy — getBoundingClientRect at tap time may have race conditions if layout shifts during animation.",
        "Conveyor readability at higher speeds (Level 4–5) may still need tuning after implementation.",
        "FeedbackOverlay duration balance: long enough to read, short enough to not break the loop rhythm.",
    ]

    open_questions = [
        "Should customer reaction (smile/dejection) live inside OrderTicket or FeedbackOverlay?",
        "Should conveyor item replacement be immediate or slightly delayed for readability?",
        "Should level summary reuse FeedbackOverlay or be a separate summary screen?",
    ]

    return {
        "artifact_name": ARTIFACT_NAME,
        "produced_by": PRODUCED_BY,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pass",
        "implementation_goal": (
            f"Build a playable {interaction_type} game prototype that preserves the approved "
            f"prototype behavior and UI intent: {prototype_goal}"
        ).strip(": "),
        "build_scope": {
            "must_build_now": [
                "core playable screen with conveyor belt interaction",
                "current level config support (5 levels)",
                "conveyor tap interaction surface",
                "order ticket and customer context display",
                "pastry box with running total and feedback visuals",
                "dominant success and fail feedback overlay",
                "score, lives, patience, and shift HUD",
            ],
            "can_stub": [
                "placeholder customer art and names",
                "placeholder sound hooks",
                "basic CSS motion before higher-fidelity animation",
                "simple static iconography",
            ],
            "must_not_build_now": [
                "user accounts or authentication",
                "leaderboards",
                "analytics dashboard",
                "backend persistence",
                "deployment pipeline",
                "monetization systems",
                "teacher admin interface",
            ],
        },
        "file_plan": file_plan,
        "component_plan": component_plan,
        "state_plan": state_plan,
        "data_config_plan": data_config_plan,
        "animation_plan": animation_plan,
        "test_plan": test_plan,
        "integration_notes": integration_notes,
        "risks_and_unknowns": risks_and_unknowns,
        "open_questions": open_questions,
    }


# ---------------------------------------------------------------------------
# Stub — called by SharedAgentRunner when no model_callable is provided
# ---------------------------------------------------------------------------

def implementation_plan_stub(context: Dict[str, Any]) -> Dict[str, Any]:
    """Reads upstream artifact inputs from context and derives the plan."""
    artifact_inputs = context.get("artifact_inputs", {})
    prototype_ui_spec = artifact_inputs.get("prototype_ui_spec", {})
    prototype_build_spec = artifact_inputs.get("prototype_build_spec", {})
    prototype_spec = artifact_inputs.get("prototype_spec", {})

    return build_implementation_plan(
        prototype_ui_spec=prototype_ui_spec,
        prototype_build_spec=prototype_build_spec,
        prototype_spec=prototype_spec,
    )


# ---------------------------------------------------------------------------
# AgentSpec factory
# ---------------------------------------------------------------------------

def build_spec(repo_root: Path) -> AgentSpec:
    return AgentSpec(
        agent_name="implementation_plan_agent",
        expected_output_artifact=ARTIFACT_NAME,
        expected_produced_by=PRODUCED_BY,
        prompt_path=repo_root / "agents" / "implementation_plan" / "prompt.md",
        config_path=repo_root / "agents" / "implementation_plan" / "config.yaml",
        allowed_reads=["prototype_ui_spec", "prototype_build_spec", "prototype_spec"],
        allowed_writes=[ARTIFACT_NAME],
        max_revision_count=2,
    )


# ---------------------------------------------------------------------------
# Pipeline entry point
# ---------------------------------------------------------------------------

def run(
    repo_root: Path,
    job_id: str,
    artifact_paths: Dict[str, Path],
    model_callable=None,
):
    """Run the Implementation Plan Agent.

    Args:
        model_callable: Optional LLM callable. If provided, replaces the stub.
                        If None, uses the deterministic stub.
    """
    runner = SharedAgentRunner(repo_root)
    return runner.run(
        spec=build_spec(repo_root),
        job_id=job_id,
        artifact_paths=artifact_paths,
        model_callable=model_callable if model_callable is not None else implementation_plan_stub,
    )
