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

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from utils.shared_agent_runner import AgentSpec, SharedAgentRunner


ARTIFACT_NAME = "implementation_plan"
PRODUCED_BY = "Implementation Plan Agent"


# ---------------------------------------------------------------------------
# Bakery — combine_and_build interaction
# ---------------------------------------------------------------------------

_BAKERY_IMPL_DATA: Dict[str, Any] = {
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
    "file_plan": [
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
    ],
    "component_plan": [
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
    ],
    "state_plan": {
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
    },
    "data_config_plan": {
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
    },
    "animation_plan": [
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
    ],
    "test_plan": {
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
    },
    "integration_notes": [
        "Preview app (preview/) is the live development surface — game files live under preview/src/games/.",
        "Static pass exports (previews/bakery/pass-N.html) are separate from the preview app source — do not conflate them.",
        "Component structure should support later pass export without redesigning game logic.",
        "Do not touch: pipeline.py, engine/gate_engine.py, agents/, artifacts/schemas/, orchestrator/, utils/, scripts/run_benchmarks.py.",
    ],
    "risks_and_unknowns": [
        "Cross-component flying-item animation requires a shared coordinate strategy — getBoundingClientRect at tap time may have race conditions if layout shifts during animation.",
        "Conveyor readability at higher speeds (Level 4–5) may still need tuning after implementation.",
        "FeedbackOverlay duration balance: long enough to read, short enough to not break the loop rhythm.",
    ],
    "open_questions": [
        "Should customer reaction (smile/dejection) live inside OrderTicket or FeedbackOverlay?",
        "Should conveyor item replacement be immediate or slightly delayed for readability?",
        "Should level summary reuse FeedbackOverlay or be a separate summary screen?",
    ],
}


# ---------------------------------------------------------------------------
# Fire Station Dispatch — route_and_dispatch interaction
# ---------------------------------------------------------------------------

_FIRE_DISPATCH_IMPL_DATA: Dict[str, Any] = {
    "build_scope": {
        "must_build_now": [
            "incident queue",
            "truck tap-dispatch surface",
            "capacity running total",
            "feedback overlay",
            "HUD (score/lives/time)",
            "level progression",
        ],
        "can_stub": [
            "placeholder incident names",
            "placeholder truck art",
        ],
        "must_not_build_now": [
            "multiplayer",
            "backend",
            "leaderboards",
            "teacher tools",
        ],
    },
    "file_plan": [
        {
            "path": "preview/src/App.jsx",
            "action": "update",
            "purpose": "Mount FireDispatchPrototype as the current game prototype entry component.",
        },
        {
            "path": "preview/src/games/FireDispatchPrototype.jsx",
            "action": "create",
            "purpose": "Own the main playable prototype container, dispatch state, and level behavior.",
        },
        {
            "path": "preview/src/games/fire/missionConfig.js",
            "action": "create",
            "purpose": "Store level configs with incident types, truck capacities, and time limits.",
        },
        {
            "path": "preview/src/games/fire/components/MissionCard.jsx",
            "action": "create",
            "purpose": "Render incident type, location, and arithmetic demand value for the active mission.",
        },
        {
            "path": "preview/src/games/fire/components/TruckYard.jsx",
            "action": "create",
            "purpose": "Render tap-to-dispatch trucks with capacity labels and multi-select support.",
        },
        {
            "path": "preview/src/games/fire/components/DispatchBoard.jsx",
            "action": "create",
            "purpose": "Render dispatched trucks and running capacity total vs. demand value.",
        },
        {
            "path": "preview/src/games/fire/components/OutcomeOverlay.jsx",
            "action": "create",
            "purpose": "Render full-screen success, excess, timeout, and shift-end feedback states.",
        },
        {
            "path": "preview/src/games/fire/styles.css",
            "action": "create",
            "purpose": "Contain prototype-scoped layout, motion, and readability styling for fire dispatch.",
        },
    ],
    "component_plan": [
        {
            "component_name": "FireDispatchPrototype",
            "responsibility": "Root container that owns all dispatch state and arithmetic validation logic.",
            "inputs": ["mission config", "level rules"],
            "outputs": ["screen state", "dispatch state", "child component props"],
        },
        {
            "component_name": "MissionCard",
            "responsibility": "Show incident type, location, and arithmetic demand value.",
            "inputs": ["incidentName", "incidentEmoji", "locationName", "demandValue", "urgency"],
            "outputs": ["visual mission context"],
        },
        {
            "component_name": "TruckYard",
            "responsibility": "Tap-to-dispatch trucks with capacity labels; multi-select supported.",
            "inputs": ["trucks", "selectedIds", "dispatchEnabled", "onTruckToggle"],
            "outputs": ["truck toggle event"],
        },
        {
            "component_name": "DispatchBoard",
            "responsibility": "Show dispatched trucks and running capacity total.",
            "inputs": ["selectedTrucks", "totalCapacity", "demandValue", "feedbackMode"],
            "outputs": ["visual capacity accounting"],
        },
        {
            "component_name": "OutcomeOverlay",
            "responsibility": "Full-screen success/excess/timeout feedback; returns null when feedbackMode is null.",
            "inputs": ["feedbackMode", "summaryStats"],
            "outputs": ["dominant outcome feedback"],
        },
    ],
    "state_plan": {
        "local_state": [
            {
                "name": "incidents",
                "type": "array",
                "initial_value": "generated from LEVEL_CONFIGS[0].incidentTypes",
                "updated_by": ["level progression"],
            },
            {
                "name": "currentIncident",
                "type": "object",
                "initial_value": "incidents[0]",
                "updated_by": ["successful dispatch", "timeout → next incident"],
            },
            {
                "name": "availableTrucks",
                "type": "array",
                "initial_value": "LEVEL_CONFIGS[0].truckTypes",
                "updated_by": ["level progression"],
            },
            {
                "name": "dispatched",
                "type": "array",
                "initial_value": "[]",
                "updated_by": ["truck toggle", "dispatch reset"],
            },
            {
                "name": "totalCapacity",
                "type": "number",
                "initial_value": "0",
                "updated_by": ["truck toggle (sum of dispatched capacities)"],
            },
            {
                "name": "feedbackMode",
                "type": "string | null",
                "initial_value": "null",
                "updated_by": ["success", "excess", "timeout", "shift_end"],
            },
            {
                "name": "timeLeft",
                "type": "number",
                "initial_value": "LEVEL_CONFIGS[0].timeLimit",
                "updated_by": ["timer tick", "new incident reset"],
            },
            {
                "name": "score",
                "type": "number",
                "initial_value": "0",
                "updated_by": ["successful dispatch"],
            },
            {
                "name": "lives",
                "type": "number",
                "initial_value": "3",
                "updated_by": ["timeout miss"],
            },
            {
                "name": "streak",
                "type": "number",
                "initial_value": "0",
                "updated_by": ["success increment", "miss or excess reset"],
            },
            {
                "name": "levelIndex",
                "type": "number",
                "initial_value": "0",
                "updated_by": ["score threshold unlock"],
            },
        ],
        "derived_state": [
            {
                "name": "currentLevelConfig",
                "derived_from": "LEVEL_CONFIGS[levelIndex]",
                "description": "Active level rules: incident types, truck capacities, time limit, score threshold.",
            },
            {
                "name": "demandValue",
                "derived_from": "currentIncident.demandValue",
                "description": "Arithmetic target the player must match with truck capacity.",
            },
            {
                "name": "capacityPercent",
                "derived_from": "totalCapacity / demandValue",
                "description": "Used to drive the dispatch board fill indicator.",
            },
            {
                "name": "nextLevelUnlocked",
                "derived_from": "score >= currentLevelConfig.scoreThreshold",
                "description": "True when the player has reached the score needed to advance.",
            },
        ],
        "state_ownership_notes": (
            "FireDispatchPrototype owns all session state. Child components receive props "
            "and emit events — they own no gameplay logic."
        ),
    },
    "data_config_plan": {
        "config_objects": [
            {
                "name": "LEVEL_CONFIGS",
                "file_path": "preview/src/games/fire/missionConfig.js",
                "description": (
                    "Array of 5 level configs: each has incidentTypes (array of {name, emoji, demandValue}), "
                    "truckTypes (array of {id, name, emoji, capacity}), timeLimit, scoreThreshold, streakBonus."
                ),
            },
            {
                "name": "TRUCK_CAPACITY_MAP",
                "file_path": "preview/src/games/fire/missionConfig.js",
                "description": "Maps truck id to capacity number — authoritative source for dispatch math.",
            },
        ],
        "hardcoded_only_if_temporary": [
            "Placeholder incident names and location strings — temporary content.",
            "Overlay copy text — will move to a content config.",
            "SUCCESS_MS and TIMEOUT_MS overlay duration constants — inline for now.",
        ],
        "future_extraction_notes": (
            "Level tuning, incident pools, truck rosters, and score thresholds should move "
            "to a separate data JSON once the game supports teacher customization."
        ),
    },
    "animation_plan": [
        {
            "animation_name": "truck_dispatch",
            "owner": "TruckYard",
            "trigger": "on tap (truck selected)",
            "implementation_note": (
                "Truck card slides toward DispatchBoard on selection — "
                "use translateX keyframe, 300ms."
            ),
        },
        {
            "animation_name": "outcome_overlay",
            "owner": "FireDispatchPrototype",
            "trigger": "on match (feedbackMode becomes non-null)",
            "implementation_note": (
                "Overlay enters with scale-in keyframe (0.88 → 1.0, opacity 0 → 1, 180ms)."
            ),
        },
        {
            "animation_name": "excess_shake",
            "owner": "DispatchBoard",
            "trigger": "on excess capacity (totalCapacity > demandValue)",
            "implementation_note": (
                "Horizontal shake keyframe applied to DispatchBoard, 350ms. "
                "Clears selection after shake completes so player can retry."
            ),
        },
    ],
    "test_plan": {
        "manual_checks": [
            "Player can identify demand value within 5 seconds of incident appearing.",
            "Correct truck selection is obvious — capacity labels are legible.",
            "Overlay is screen-dominant and communicates success/excess/timeout clearly without reading.",
        ],
        "logic_checks": [
            "totalCapacity always equals the sum of selected truck capacities.",
            "Exact match triggers success; any excess triggers excess feedback.",
            "Lives decrement only on timeout, not on excess.",
            "Level unlock fires only after score reaches currentLevelConfig.scoreThreshold.",
        ],
        "edge_case_checks": [
            "Rapid truck toggles do not corrupt totalCapacity.",
            "Timer pauses correctly during feedbackMode and restarts on new incident.",
            "Shift-end overlay appears when lives reach 0.",
        ],
    },
    "integration_notes": [
        "Preview app (preview/) is the live development surface — game files live under preview/src/games/.",
        "Static pass exports are separate from the preview app source — do not conflate them.",
        "Component structure should support later pass export without redesigning game logic.",
        "Do not touch: pipeline.py, engine/gate_engine.py, agents/, artifacts/schemas/, orchestrator/, utils/, scripts/run_benchmarks.py.",
    ],
    "risks_and_unknowns": [
        "Multi-select truck dispatch requires clean add/remove of individual truck IDs — use filter-on-toggle pattern.",
        "totalCapacity must be recomputed from scratch on each toggle, not incremented/decremented.",
        "Timer restart timing on new incident must be precise to avoid drift.",
    ],
    "open_questions": [
        "Should the dispatch button be a separate tap or should exact capacity match auto-dispatch?",
        "Should excess capacity give partial credit or always reset to zero?",
        "Should truck art be emoji or placeholder SVG icons for the first pass?",
    ],
}


# ---------------------------------------------------------------------------
# Unit Circle Pizza Lab — navigate_and_position interaction
# ---------------------------------------------------------------------------

_UNIT_CIRCLE_IMPL_DATA: Dict[str, Any] = {
    "build_scope": {
        "must_build_now": [
            "SVG unit circle with click placement",
            "live angle/coordinate display",
            "order panel with target",
            "inline feedback with miss explanation",
            "round progression",
            "score/streak",
        ],
        "can_stub": [
            "drag interaction (click-only first)",
            "radians display (degrees only first)",
            "difficulty scaling",
        ],
        "must_not_build_now": [
            "accounts",
            "backend",
            "teacher tools",
            "adaptive difficulty",
        ],
    },
    "file_plan": [
        {
            "path": "preview/src/App.jsx",
            "action": "update",
            "purpose": "Mount UnitCirclePrototype as the current game prototype entry component.",
        },
        {
            "path": "preview/src/games/UnitCirclePrototype.jsx",
            "action": "create",
            "purpose": "Own the main playable prototype container with angle evaluation and round progression.",
        },
        {
            "path": "preview/src/games/unitcircle/labConfig.js",
            "action": "create",
            "purpose": "Store round configs with target angles, tolerances, and difficulty labels.",
        },
        {
            "path": "preview/src/games/unitcircle/components/PizzaWheel.jsx",
            "action": "create",
            "purpose": "Render SVG unit circle and own click-to-place topping interaction.",
        },
        {
            "path": "preview/src/games/unitcircle/components/AngleReadout.jsx",
            "action": "create",
            "purpose": "Render live θ display in degrees and radians.",
        },
        {
            "path": "preview/src/games/unitcircle/components/OrderPanel.jsx",
            "action": "create",
            "purpose": "Render target angle specification for each round.",
        },
        {
            "path": "preview/src/games/unitcircle/components/CoordinateDisplay.jsx",
            "action": "create",
            "purpose": "Render live computed cos θ and sin θ values.",
        },
        {
            "path": "preview/src/games/unitcircle/components/FeedbackPanel.jsx",
            "action": "create",
            "purpose": "Render inline result with explanation and ghost correct position on miss.",
        },
        {
            "path": "preview/src/games/unitcircle/styles.css",
            "action": "create",
            "purpose": "Contain prototype-scoped layout, motion, and readability styling for unit circle lab.",
        },
    ],
    "component_plan": [
        {
            "component_name": "UnitCirclePrototype",
            "responsibility": "Root container that owns state, evaluates submissions, and drives round progression.",
            "inputs": ["lab config", "round rules"],
            "outputs": ["screen state", "angle state", "child component props"],
        },
        {
            "component_name": "PizzaWheel",
            "responsibility": "SVG unit circle; click/drag to place topping; emits onAngleChange.",
            "inputs": ["currentAngleDeg", "submittedAngleDeg", "correctAngleDeg", "onAngleChange", "interactive"],
            "outputs": ["onAngleChange event"],
        },
        {
            "component_name": "AngleReadout",
            "responsibility": "Live θ display in degrees and radians.",
            "inputs": ["angleDeg"],
            "outputs": ["visual angle readout"],
        },
        {
            "component_name": "OrderPanel",
            "responsibility": "Target angle specification for the current round.",
            "inputs": ["targetAngleDeg", "targetLabel", "radianLabel", "roundIndex", "totalRounds"],
            "outputs": ["visual target specification"],
        },
        {
            "component_name": "CoordinateDisplay",
            "responsibility": "Live computed cos θ and sin θ values.",
            "inputs": ["angleDeg"],
            "outputs": ["visual coordinate display"],
        },
        {
            "component_name": "FeedbackPanel",
            "responsibility": "Inline result with explanation; shows correct answer on miss.",
            "inputs": ["feedbackMode", "angleDelta", "targetAngleDeg", "toleranceDeg"],
            "outputs": ["inline feedback with math explanation"],
        },
    ],
    "state_plan": {
        "local_state": [
            {
                "name": "roundIndex",
                "type": "number",
                "initial_value": "0",
                "updated_by": ["round advance after feedback delay"],
            },
            {
                "name": "targetAngleDeg",
                "type": "number",
                "initial_value": "ROUND_CONFIGS[0].targetAngleDeg",
                "updated_by": ["round advance"],
            },
            {
                "name": "toleranceDeg",
                "type": "number",
                "initial_value": "ROUND_CONFIGS[0].toleranceDeg",
                "updated_by": ["round advance"],
            },
            {
                "name": "currentAngleDeg",
                "type": "number",
                "initial_value": "0",
                "updated_by": ["player click on PizzaWheel"],
            },
            {
                "name": "submitted",
                "type": "boolean",
                "initial_value": "false",
                "updated_by": ["handleSubmit", "round reset"],
            },
            {
                "name": "feedbackMode",
                "type": "string | null",
                "initial_value": "null",
                "updated_by": ["correct", "close", "miss", "session_complete"],
            },
            {
                "name": "score",
                "type": "number",
                "initial_value": "0",
                "updated_by": ["correct submission"],
            },
            {
                "name": "streak",
                "type": "number",
                "initial_value": "0",
                "updated_by": ["correct increment", "miss reset"],
            },
            {
                "name": "sessionComplete",
                "type": "boolean",
                "initial_value": "false",
                "updated_by": ["all rounds completed"],
            },
        ],
        "derived_state": [
            {
                "name": "currentRoundConfig",
                "derived_from": "ROUND_CONFIGS[roundIndex]",
                "description": "Active round: targetAngleDeg, toleranceDeg, label, radianLabel, scoreValue.",
            },
            {
                "name": "playerCoords",
                "derived_from": "{x: Math.cos(currentAngleDeg * π/180), y: Math.sin(currentAngleDeg * π/180)}",
                "description": "Live computed position of player's selected angle on unit circle.",
            },
            {
                "name": "targetCoords",
                "derived_from": "{x: Math.cos(targetAngleDeg * π/180), y: Math.sin(targetAngleDeg * π/180)}",
                "description": "Correct position shown as ghost on miss.",
            },
            {
                "name": "angleDelta",
                "derived_from": "min(|currentAngleDeg - targetAngleDeg|, 360 - |currentAngleDeg - targetAngleDeg|)",
                "description": "Shortest angular distance accounting for 0°/360° wraparound.",
            },
            {
                "name": "isWithinTolerance",
                "derived_from": "angleDelta <= toleranceDeg",
                "description": "True when player's angle is close enough to target.",
            },
        ],
        "state_ownership_notes": (
            "UnitCirclePrototype owns all session state. Child components receive props "
            "and emit events — they own no gameplay logic."
        ),
    },
    "data_config_plan": {
        "config_objects": [
            {
                "name": "ROUND_CONFIGS",
                "file_path": "preview/src/games/unitcircle/labConfig.js",
                "description": (
                    "Array of 20+ round configs spanning the full circle at three difficulty tiers. "
                    "Each has targetAngleDeg, toleranceDeg, label, radianLabel, scoreValue."
                ),
            },
            {
                "name": "TOLERANCE_LABELS",
                "file_path": "preview/src/games/unitcircle/labConfig.js",
                "description": "Maps toleranceDeg to feedback copy (e.g., 10 → 'Close enough!', 5 → 'Precise!', 3 → 'Expert!').",
            },
        ],
        "hardcoded_only_if_temporary": [
            "Feedback explanation text per round — will move to round config.",
            "FEEDBACK_DELAY_MS — inline for now.",
        ],
        "future_extraction_notes": (
            "Difficulty tiers, tolerance thresholds, and round ordering should be configurable "
            "once the game supports teacher customization or adaptive difficulty."
        ),
    },
    "animation_plan": [
        {
            "animation_name": "topping_place",
            "owner": "PizzaWheel",
            "trigger": "on submit — topping placed at selected position",
            "implementation_note": (
                "Topping SVG circle scales in at selected angle position, 200ms cubic-bezier bounce."
            ),
        },
        {
            "animation_name": "correct_flash",
            "owner": "FeedbackPanel",
            "trigger": "on correct — background green transition",
            "implementation_note": (
                "Background color transitions to green, 200ms ease."
            ),
        },
        {
            "animation_name": "ghost_reveal",
            "owner": "PizzaWheel",
            "trigger": "on miss — correct position shown as ghost topping",
            "implementation_note": (
                "Ghost SVG circle fades in at correct angle position, opacity 0 → 0.6, 300ms ease."
            ),
        },
    ],
    "test_plan": {
        "manual_checks": [
            "Player understands they are placing a topping at a math position.",
            "Angle display updates live as they move the click around the wheel.",
            "Feedback shows the correct answer on miss with a visible ghost topping.",
        ],
        "logic_checks": [
            "angleDelta uses min(|diff|, 360-|diff|) to handle 0°/360° wraparound correctly.",
            "Submit is the only path to evaluation — live angle change does not trigger feedback.",
            "correctAngleDeg is only passed to PizzaWheel on feedbackMode='miss', not on correct/close.",
            "Score and streak update according to correct/close/miss rules.",
        ],
        "edge_case_checks": [
            "SVG y-axis inversion: topping renders at -sin(θ) not sin(θ) for SVG coordinates.",
            "Clicking at exactly 0°/360° boundary is handled cleanly.",
            "Session complete state appears after all rounds are exhausted.",
        ],
    },
    "integration_notes": [
        "Preview app (preview/) is the live development surface — game files live under preview/src/games/.",
        "Static pass exports are separate from the preview app source — do not conflate them.",
        "Component structure should support later pass export without redesigning game logic.",
        "Do not touch: pipeline.py, engine/gate_engine.py, agents/, artifacts/schemas/, orchestrator/, utils/, scripts/run_benchmarks.py.",
    ],
    "risks_and_unknowns": [
        "SVG coordinate system has y-axis inverted relative to standard math — use -sin(θ) for SVG y when rendering positions.",
        "Angle wraparound at 0°/360° boundary requires explicit handling in angleDelta computation.",
        "Click-to-angle conversion via Math.atan2 must account for SVG center offset correctly.",
    ],
    "open_questions": [
        "Should 'close' (within 2× tolerance) award partial credit or just encouragement feedback?",
        "Should radians display be added in pass 1 or stubbed to degrees only?",
        "Should the session complete state offer replay or just a summary?",
    ],
}


# ---------------------------------------------------------------------------
# Concept routing
# ---------------------------------------------------------------------------

CONCEPT_OVERRIDES: Dict[str, Dict[str, Any]] = {
    "combine_and_build": _BAKERY_IMPL_DATA,
    "route_and_dispatch": _FIRE_DISPATCH_IMPL_DATA,
    "navigate_and_position": _UNIT_CIRCLE_IMPL_DATA,
}
_GENERIC_IMPL_DATA = _BAKERY_IMPL_DATA  # fallback


# ---------------------------------------------------------------------------
# Stub — called by SharedAgentRunner when no model_callable is provided
# ---------------------------------------------------------------------------

def implementation_plan_stub(context: Dict[str, Any]) -> Dict[str, Any]:
    """Reads upstream artifact inputs from context and derives the plan."""
    artifact_inputs = context.get("artifact_inputs", {})
    prototype_spec = artifact_inputs.get("prototype_spec", {})

    interaction_type = (
        prototype_spec.get("concept_anchor", {}).get("primary_interaction_type", "")
    )
    prototype_goal = prototype_spec.get("prototype_goal", "")

    data = CONCEPT_OVERRIDES.get(interaction_type, _GENERIC_IMPL_DATA)

    implementation_goal = (
        f"Build a playable {interaction_type} game prototype that preserves the approved "
        f"prototype behavior: {prototype_goal}"
    ).strip(": ").strip()

    return {
        "artifact_name": ARTIFACT_NAME,
        "produced_by": PRODUCED_BY,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pass",
        "implementation_goal": implementation_goal,
        "build_scope": data["build_scope"],
        "file_plan": data["file_plan"],
        "component_plan": data["component_plan"],
        "state_plan": data["state_plan"],
        "data_config_plan": data["data_config_plan"],
        "animation_plan": data["animation_plan"],
        "test_plan": data["test_plan"],
        "integration_notes": data["integration_notes"],
        "risks_and_unknowns": data["risks_and_unknowns"],
        "open_questions": data["open_questions"],
    }


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
