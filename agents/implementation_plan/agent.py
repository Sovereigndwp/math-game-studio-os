"""
Implementation Plan Agent — Stage 9.

Translates an approved prototype_ui_spec into an engineering blueprint:
files, components, state model, data flow, build order, and test targets.

Does NOT generate code. That is implementation_patch_plan (Stage 10).

Modes:
    Stub: deterministic Bakery override + generic fallback.
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

CONCEPT_OVERRIDES: Dict[str, Dict[str, Any]] = {
    "bakery": {
        "implementation_objective": (
            "Build a single-screen React prototype for a K-2 tap-to-add bakery "
            "addition game where a learner fills a pastry box to match a customer's "
            "target number, with overshoot bounce-back as the primary error mechanic."
        ),
        "tech_stack": {
            "framework": "React 18 (functional components + hooks)",
            "language": "JavaScript (JSX)",
            "styling": "CSS Modules via plain .css files co-located with components",
            "bundler": "Vite",
            "test_approach": "Manual browser verification against acceptance checklist; "
                             "automated unit tests deferred from prototype scope",
        },
        "file_manifest": {
            "create": [
                {
                    "file_path": "preview/src/constants.js",
                    "purpose": "TARGET_SEQUENCE, ROUND_STATES enum, and animation timing constants",
                    "file_type": "constant",
                },
                {
                    "file_path": "preview/src/hooks/useGameState.js",
                    "purpose": "Custom hook owning all game state: targets, roundIndex, "
                               "currentTotal, roundState, isAnimating. Exposes handleTap "
                               "and handleReplay as the only mutation surface.",
                    "file_type": "hook",
                },
                {
                    "file_path": "preview/src/components/CustomerTicket.jsx",
                    "purpose": "Renders the customer character and the target number ticket. "
                               "Changes customer expression on success state.",
                    "file_type": "component",
                },
                {
                    "file_path": "preview/src/components/CustomerTicket.css",
                    "purpose": "Styles for CustomerTicket: ticket card, character emoji, "
                               "target number, satisfaction animation.",
                    "file_type": "style",
                },
                {
                    "file_path": "preview/src/components/PastryBox.jsx",
                    "purpose": "Renders items accumulated in the box. Plays success/overshoot "
                               "CSS animations based on roundState prop.",
                    "file_type": "component",
                },
                {
                    "file_path": "preview/src/components/PastryBox.css",
                    "purpose": "Box layout, item grid, success pulse animation, overshoot shake.",
                    "file_type": "style",
                },
                {
                    "file_path": "preview/src/components/PastryTray.jsx",
                    "purpose": "Renders 12 tappable pastry buttons. Disables all taps "
                               "when disabled prop is true (during animations).",
                    "file_type": "component",
                },
                {
                    "file_path": "preview/src/components/PastryTray.css",
                    "purpose": "Tray grid layout, 44px+ touch targets, disabled state opacity.",
                    "file_type": "style",
                },
                {
                    "file_path": "preview/src/components/FlyingPastry.jsx",
                    "purpose": "Renders a single pastry emoji that animates from a tray "
                               "origin position to the pastry box position via CSS keyframe. "
                               "Mounts on tap, unmounts after animation completes.",
                    "file_type": "component",
                },
                {
                    "file_path": "preview/src/components/FlyingPastry.css",
                    "purpose": "Keyframe arc animation: translate from tray footer to box "
                               "center using absolute positioning and transform.",
                    "file_type": "style",
                },
                {
                    "file_path": "preview/src/components/FeedbackOverlay.jsx",
                    "purpose": "Full-screen overlay rendered over the entire game on success "
                               "or overshoot. Covers all regions to make feedback unmissable.",
                    "file_type": "component",
                },
                {
                    "file_path": "preview/src/components/FeedbackOverlay.css",
                    "purpose": "Full-screen positioning (position: fixed, inset: 0), "
                               "scale-in animation, success green and overshoot red variants.",
                    "file_type": "style",
                },
                {
                    "file_path": "preview/src/components/RunningTotal.jsx",
                    "purpose": "Renders current total count and progress bar toward target. "
                               "Lives in the header region.",
                    "file_type": "component",
                },
                {
                    "file_path": "preview/src/components/SessionComplete.jsx",
                    "purpose": "End-of-session screen with completion message and replay button.",
                    "file_type": "component",
                },
            ],
            "edit": [
                {
                    "file_path": "preview/src/BakeryGame.jsx",
                    "change_description": "Refactor to use useGameState hook and import "
                                          "individual sub-components. Remove inline component "
                                          "definitions. Wire FlyingPastry on tap events.",
                    "reason": "BakeryGame should be a thin orchestrator, not a monolith. "
                              "All component logic must move to dedicated files to enable "
                              "independent testing and patching.",
                },
                {
                    "file_path": "preview/src/BakeryGame.css",
                    "change_description": "Remove styles that will move to component-level "
                                          "CSS files. Keep only layout region rules "
                                          "(game-header, game-play-area, game-footer).",
                    "reason": "Co-located component CSS prevents style bleed and makes "
                              "each component independently patchable.",
                },
                {
                    "file_path": "preview/src/index.css",
                    "change_description": "No changes required — global reset is correct.",
                    "reason": "Global reset already matches UI spec requirements.",
                },
            ],
            "do_not_touch": [
                "pipeline.py",
                "engine/gate_engine.py",
                "agents/",
                "artifacts/schemas/",
                "orchestrator/",
                "utils/",
                "scripts/run_benchmarks.py",
                "memory/",
                "docs/",
            ],
        },
        "component_breakdown": [
            {
                "component_name": "BakeryGame",
                "file_path": "preview/src/BakeryGame.jsx",
                "purpose": "Root orchestrator. Mounts all child components. Passes state "
                           "and callbacks down. Contains no game logic of its own — "
                           "delegates to useGameState.",
                "props": [],
                "state_owned": [],
                "events_emitted": [],
                "depends_on": [
                    "CustomerTicket",
                    "PastryBox",
                    "PastryTray",
                    "RunningTotal",
                    "FeedbackOverlay",
                    "FlyingPastry",
                    "SessionComplete",
                    "useGameState",
                ],
            },
            {
                "component_name": "CustomerTicket",
                "file_path": "preview/src/components/CustomerTicket.jsx",
                "purpose": "Renders the customer character emoji and the target number. "
                           "Character expression changes on roundState === success_feedback.",
                "props": [
                    "target: number — the current round's target count",
                    "roundIndex: number — 0-based current round index",
                    "totalRounds: number — total rounds in session",
                    "roundState: string — current round state from ROUND_STATES",
                ],
                "state_owned": [],
                "events_emitted": [],
                "depends_on": [],
            },
            {
                "component_name": "PastryBox",
                "file_path": "preview/src/components/PastryBox.jsx",
                "purpose": "Renders accumulated pastry items as emojis. Applies success "
                           "pulse and overshoot shake CSS classes based on roundState.",
                "props": [
                    "total: number — current count of items in the box",
                    "roundState: string — current round state, drives animation class",
                ],
                "state_owned": [],
                "events_emitted": [],
                "depends_on": [],
            },
            {
                "component_name": "PastryTray",
                "file_path": "preview/src/components/PastryTray.jsx",
                "purpose": "12-item tappable grid. Fires onTap callback on valid tap. "
                           "All taps ignored when disabled is true.",
                "props": [
                    "onTap: () => void — callback fired when a valid tap occurs",
                    "disabled: boolean — when true, all taps are blocked",
                ],
                "state_owned": [],
                "events_emitted": ["onTap"],
                "depends_on": [],
            },
            {
                "component_name": "FlyingPastry",
                "file_path": "preview/src/components/FlyingPastry.jsx",
                "purpose": "Single-use animation component. Mounts with a tap origin "
                           "coordinate, animates a pastry emoji to the box position, "
                           "then calls onComplete to unmount itself.",
                "props": [
                    "originY: number — vertical start position in px (tap Y coordinate)",
                    "onComplete: () => void — called when animation ends so parent can unmount",
                ],
                "state_owned": [],
                "events_emitted": ["onComplete"],
                "depends_on": [],
            },
            {
                "component_name": "FeedbackOverlay",
                "file_path": "preview/src/components/FeedbackOverlay.jsx",
                "purpose": "Full-screen overlay (position: fixed) that renders on success "
                           "or overshoot. Uses roundState to choose green (success) or "
                           "red (overshoot) variant. Pointer-events: none so it does not "
                           "block tray taps during the brief overshoot window.",
                "props": [
                    "roundState: string — drives which variant renders (success_feedback | overshoot_feedback)",
                ],
                "state_owned": [],
                "events_emitted": [],
                "depends_on": [],
            },
            {
                "component_name": "RunningTotal",
                "file_path": "preview/src/components/RunningTotal.jsx",
                "purpose": "Displays current total count and a progress bar showing "
                           "total / target ratio. Lives in the header region.",
                "props": [
                    "total: number — current accumulated count",
                    "target: number — current round target, used to compute progress",
                ],
                "state_owned": [],
                "events_emitted": [],
                "depends_on": [],
            },
            {
                "component_name": "SessionComplete",
                "file_path": "preview/src/components/SessionComplete.jsx",
                "purpose": "Full-session end screen. Shows completion message and "
                           "a replay button that triggers session reset.",
                "props": [
                    "onReplay: () => void — called when player taps replay",
                ],
                "state_owned": [],
                "events_emitted": ["onReplay"],
                "depends_on": [],
            },
        ],
        "state_model": {
            "owner_component": "useGameState (custom hook, consumed by BakeryGame)",
            "tracked_variables": [
                {
                    "name": "targets",
                    "type": "number[]",
                    "initial_value": "getTargets() — shuffled TARGET_SEQUENCE",
                    "updated_by": ["handleReplay"],
                },
                {
                    "name": "roundIndex",
                    "type": "number",
                    "initial_value": "0",
                    "updated_by": ["success_feedback timeout — advance to next round"],
                },
                {
                    "name": "currentTotal",
                    "type": "number",
                    "initial_value": "0",
                    "updated_by": [
                        "handleTap — increment on valid tap",
                        "overshoot_feedback timeout — decrement by 1 (bounce-back)",
                        "round transition — reset to 0",
                    ],
                },
                {
                    "name": "roundState",
                    "type": "string (ROUND_STATES enum)",
                    "initial_value": "ROUND_STATES.ACTIVE",
                    "updated_by": [
                        "handleTap — set to SUCCESS on exact match",
                        "handleTap — set to OVERSHOOT on total > target",
                        "success timeout — advance round or set COMPLETE",
                        "overshoot timeout — restore to ACTIVE",
                    ],
                },
                {
                    "name": "isAnimating",
                    "type": "boolean",
                    "initial_value": "false",
                    "updated_by": [
                        "handleTap start — set true",
                        "item animation complete — set false",
                        "success/overshoot timeout — set false on completion",
                    ],
                },
                {
                    "name": "flyingPastry",
                    "type": "{ id: number, originY: number } | null",
                    "initial_value": "null",
                    "updated_by": [
                        "handleTap — set with tap Y coordinate and unique id",
                        "FlyingPastry.onComplete — reset to null",
                    ],
                },
            ],
            "state_transitions": [
                {
                    "trigger": "Player taps pastry; currentTotal + 1 < target",
                    "from_state": "round_active",
                    "to_state": "round_active",
                    "side_effects": [
                        "currentTotal += 1",
                        "flyingPastry set with tap Y origin",
                        "isAnimating = true while flying, then false",
                    ],
                },
                {
                    "trigger": "Player taps pastry; currentTotal + 1 === target",
                    "from_state": "round_active",
                    "to_state": "success_feedback",
                    "side_effects": [
                        "currentTotal += 1",
                        "isAnimating = true",
                        "FeedbackOverlay success variant renders",
                        "CustomerTicket switches to satisfaction expression",
                        "After 1500ms: advance roundIndex, reset total, return to round_active OR set session_complete",
                    ],
                },
                {
                    "trigger": "Player taps pastry; currentTotal + 1 > target",
                    "from_state": "round_active",
                    "to_state": "overshoot_feedback",
                    "side_effects": [
                        "currentTotal temporarily increments then decrements after 700ms",
                        "FeedbackOverlay overshoot variant renders",
                        "PastryBox applies shake animation",
                        "After 700ms: currentTotal restored, return to round_active",
                    ],
                },
                {
                    "trigger": "success_feedback timeout; roundIndex + 1 >= totalRounds",
                    "from_state": "success_feedback",
                    "to_state": "session_complete",
                    "side_effects": ["SessionComplete renders"],
                },
                {
                    "trigger": "Player taps replay on SessionComplete",
                    "from_state": "session_complete",
                    "to_state": "round_active",
                    "side_effects": [
                        "targets reshuffled",
                        "roundIndex = 0",
                        "currentTotal = 0",
                        "isAnimating = false",
                        "flyingPastry = null",
                    ],
                },
            ],
        },
        "data_flow": [
            {
                "data_name": "target (current round target number)",
                "source": "useGameState (derived: targets[roundIndex])",
                "consumers": ["CustomerTicket", "RunningTotal", "BakeryGame (evaluation logic)"],
                "mechanism": "props",
            },
            {
                "data_name": "currentTotal",
                "source": "useGameState",
                "consumers": ["PastryBox", "RunningTotal"],
                "mechanism": "props",
            },
            {
                "data_name": "roundState",
                "source": "useGameState",
                "consumers": ["CustomerTicket", "PastryBox", "FeedbackOverlay", "BakeryGame (conditional render)"],
                "mechanism": "props",
            },
            {
                "data_name": "isAnimating",
                "source": "useGameState",
                "consumers": ["PastryTray (disabled prop)"],
                "mechanism": "props",
            },
            {
                "data_name": "flyingPastry (origin + id)",
                "source": "useGameState",
                "consumers": ["BakeryGame (conditional render of FlyingPastry)"],
                "mechanism": "props",
            },
            {
                "data_name": "onTap callback",
                "source": "BakeryGame (calls useGameState.handleTap)",
                "consumers": ["PastryTray"],
                "mechanism": "callback",
            },
            {
                "data_name": "onReplay callback",
                "source": "BakeryGame (calls useGameState.handleReplay)",
                "consumers": ["SessionComplete"],
                "mechanism": "callback",
            },
            {
                "data_name": "FlyingPastry.onComplete",
                "source": "FlyingPastry (fires when animation ends)",
                "consumers": ["useGameState (clears flyingPastry, sets isAnimating = false)"],
                "mechanism": "callback",
            },
        ],
        "reusable_logic": [
            {
                "name": "useGameState",
                "logic_type": "hook",
                "file_path": "preview/src/hooks/useGameState.js",
                "purpose": "Encapsulates all game state and mutations. Prevents BakeryGame "
                           "from containing business logic. Returns: targets, roundIndex, "
                           "currentTotal, roundState, isAnimating, flyingPastry, "
                           "handleTap, handleReplay.",
                "signature": "() => { targets, roundIndex, currentTotal, roundState, "
                             "isAnimating, flyingPastry, handleTap, handleReplay }",
            },
            {
                "name": "getTargets",
                "logic_type": "utility",
                "file_path": "preview/src/constants.js",
                "purpose": "Returns a shuffled copy of TARGET_SEQUENCE for each new session.",
                "signature": "() => number[]",
            },
            {
                "name": "ROUND_STATES",
                "logic_type": "constant",
                "file_path": "preview/src/constants.js",
                "purpose": "Enum-style object for all valid round state strings. "
                           "Prevents magic string errors across components.",
                "signature": "{ ACTIVE: string, SUCCESS: string, OVERSHOOT: string, COMPLETE: string }",
            },
            {
                "name": "TARGET_SEQUENCE",
                "logic_type": "constant",
                "file_path": "preview/src/constants.js",
                "purpose": "5-element array of target numbers for the session. "
                           "Defined once; shuffled per session via getTargets().",
                "signature": "number[]",
            },
        ],
        "build_order": [
            {
                "phase": 1,
                "tasks": [
                    "Create constants.js with TARGET_SEQUENCE, ROUND_STATES, and timing values",
                    "Create useGameState.js hook with full state and handleTap/handleReplay logic",
                    "Refactor BakeryGame.jsx to use useGameState and import split components",
                    "Verify: game plays through all 5 rounds with correct state transitions",
                ],
                "done_when": "The game runs in the browser, all 5 rounds complete, "
                             "overshoot restores the total correctly, session_complete renders.",
            },
            {
                "phase": 2,
                "tasks": [
                    "Create CustomerTicket.jsx with customer character emoji and target number",
                    "CustomerTicket switches expression when roundState === success_feedback",
                    "Create FlyingPastry.jsx with CSS arc animation from tap origin to box",
                    "Wire FlyingPastry into BakeryGame: mount on tap, unmount on onComplete",
                    "Verify: tapping a pastry shows the emoji flying to the box before it appears there",
                ],
                "done_when": "A customer character is visible on the ticket. "
                             "Tapping causes a pastry to visibly travel from the tray to the box.",
            },
            {
                "phase": 3,
                "tasks": [
                    "Refactor FeedbackOverlay.jsx to use position: fixed covering full viewport",
                    "Add scale-in CSS animation to overlay entry",
                    "Success overlay: full-screen green with large emoji and text, 1500ms duration",
                    "Overshoot overlay: full-screen red with bounce emoji and text, 700ms duration",
                    "Verify: feedback is impossible to miss; it covers the entire screen on both events",
                ],
                "done_when": "Success and overshoot events produce a full-screen color flash "
                             "with readable text that disappears after the correct duration.",
            },
        ],
        "test_targets": [
            {
                "description": "Tapping a pastry increments the box total by 1",
                "how_to_verify": "Tap once; running total in header increases from 0 to 1, "
                                 "one pastry emoji appears in the box.",
                "target_component": "PastryTray + PastryBox + RunningTotal",
            },
            {
                "description": "Tapping during animation is blocked",
                "how_to_verify": "Tap rapidly multiple times in a row; the total increments "
                                 "only once per animation cycle, not once per tap.",
                "target_component": "PastryTray (disabled prop) + useGameState (isAnimating)",
            },
            {
                "description": "Exact match triggers success feedback",
                "how_to_verify": "Tap until total equals target; full-screen green overlay "
                                 "appears, customer character shows satisfaction expression.",
                "target_component": "FeedbackOverlay + CustomerTicket",
            },
            {
                "description": "Overshoot triggers bounce-back",
                "how_to_verify": "Tap one beyond target; full-screen red overlay appears, "
                                 "total decrements by 1 after ~700ms, round continues from restored total.",
                "target_component": "FeedbackOverlay + PastryBox + useGameState",
            },
            {
                "description": "Flying pastry travels from tray to box",
                "how_to_verify": "Tap a pastry; a croissant emoji visibly moves from the "
                                 "footer tray region upward to the pastry box before appearing in the box.",
                "target_component": "FlyingPastry",
            },
            {
                "description": "5-round session completes and replay resets state",
                "how_to_verify": "Complete all 5 rounds; session_complete screen renders. "
                                 "Tap replay; round 1/5 loads with an empty box and a new target.",
                "target_component": "SessionComplete + useGameState (handleReplay)",
            },
            {
                "description": "Customer character is visible and reacts on success",
                "how_to_verify": "On round start, customer character shows neutral expression. "
                                 "On success, character switches to satisfaction expression "
                                 "for the duration of the success_feedback state.",
                "target_component": "CustomerTicket",
            },
        ],
        "open_engineering_questions": [
            "FlyingPastry: should originY be captured from the DOM tap event (e.clientY) "
            "or from a fixed tray offset constant? Using e.clientY is more accurate but "
            "requires passing the event object up from PastryTray.",
            "FlyingPastry: should multiple flying pastries be queued (array in state) or "
            "is one-at-a-time sufficient given isAnimating blocks rapid tapping? "
            "One-at-a-time is simpler and matches the current scope.",
            "FeedbackOverlay: pointer-events: none allows tray taps during overshoot "
            "if the player is fast. Is this acceptable or should a hard input lock persist "
            "for the full overlay duration? The build spec says taps are disabled during "
            "animation — isAnimating already handles this, but confirm the interaction.",
        ],
        "implementation_notes": (
            "State lives entirely in useGameState. BakeryGame renders only — it owns no logic. "
            "All component CSS is co-located to enable independent patching. "
            "FlyingPastry is a single-use ephemeral component: it mounts on tap, runs its "
            "animation, calls onComplete, and is immediately unmounted by the parent. "
            "This avoids accumulating DOM nodes. "
            "The three build phases are ordered by player-visible impact: Phase 1 restores "
            "correctness, Phase 2 adds the flying item and customer (highest diagnostic value), "
            "Phase 3 makes feedback land. Do not start Phase 2 until Phase 1 is verified."
        ),
    }
}

# ---------------------------------------------------------------------------
# Generic fallback (thin — warns that this stage needs a concept override)
# ---------------------------------------------------------------------------

_GENERIC_IMPLEMENTATION_PLAN: Dict[str, Any] = {
    "implementation_objective": (
        "Build the approved prototype as a browser-based interactive game "
        "following the component and state structure defined in the UI spec."
    ),
    "tech_stack": {
        "framework": "React 18 (functional components + hooks)",
        "language": "JavaScript (JSX)",
        "styling": "CSS files co-located with components",
        "bundler": "Vite",
        "test_approach": "Manual browser verification against acceptance checklist",
    },
    "file_manifest": {
        "create": [
            {
                "file_path": "preview/src/constants.js",
                "purpose": "Game constants: state enum, sequence data, timing values",
                "file_type": "constant",
            },
            {
                "file_path": "preview/src/hooks/useGameState.js",
                "purpose": "Custom hook owning all game state and mutations",
                "file_type": "hook",
            },
        ],
        "edit": [
            {
                "file_path": "preview/src/App.jsx",
                "change_description": "Mount the main game component",
                "reason": "Entry point must render the game",
            }
        ],
        "do_not_touch": [
            "pipeline.py",
            "engine/gate_engine.py",
            "agents/",
            "artifacts/schemas/",
            "orchestrator/",
            "utils/",
            "scripts/run_benchmarks.py",
        ],
    },
    "component_breakdown": [
        {
            "component_name": "GameRoot",
            "file_path": "preview/src/GameRoot.jsx",
            "purpose": "Root orchestrator. Passes state and callbacks to child components.",
            "props": [],
            "state_owned": [],
            "events_emitted": [],
            "depends_on": ["useGameState"],
        }
    ],
    "state_model": {
        "owner_component": "useGameState (custom hook)",
        "tracked_variables": [
            {
                "name": "gameState",
                "type": "string",
                "initial_value": "STATES.ACTIVE",
                "updated_by": ["player interactions", "timers"],
            }
        ],
        "state_transitions": [
            {
                "trigger": "Player completes the core action",
                "from_state": "active",
                "to_state": "feedback",
                "side_effects": ["Show feedback", "Advance round after delay"],
            }
        ],
    },
    "data_flow": [
        {
            "data_name": "gameState",
            "source": "useGameState",
            "consumers": ["GameRoot", "feedback components"],
            "mechanism": "props",
        }
    ],
    "reusable_logic": [
        {
            "name": "useGameState",
            "logic_type": "hook",
            "file_path": "preview/src/hooks/useGameState.js",
            "purpose": "Encapsulates all game state and mutation handlers",
            "signature": "() => { gameState, handleAction, handleReplay }",
        }
    ],
    "build_order": [
        {
            "phase": 1,
            "tasks": [
                "Create constants and useGameState hook",
                "Wire game root component with state",
            ],
            "done_when": "Game renders and core interaction loop completes in browser",
        },
        {
            "phase": 2,
            "tasks": [
                "Add feedback states",
                "Add session complete screen",
            ],
            "done_when": "All screen states render correctly and session completes",
        },
    ],
    "test_targets": [
        {
            "description": "Core interaction increments the game state",
            "how_to_verify": "Perform the core action; state visibly advances on screen",
            "target_component": "GameRoot",
        }
    ],
    "open_engineering_questions": [
        "No concept override exists for this concept. Results will be generic. "
        "Add a CONCEPT_OVERRIDES entry for this concept to get a precise plan."
    ],
    "implementation_notes": (
        "Generic fallback plan. Not tailored to any specific game. "
        "Add a concept override for production-quality output."
    ),
}


# ---------------------------------------------------------------------------
# Stub
# ---------------------------------------------------------------------------

def implementation_plan_stub(context: Dict[str, Any]) -> Dict[str, Any]:
    """Deterministic stub for the Implementation Plan Agent.

    Selects concept override by world_theme keyword from prototype_spec,
    or falls back to the generic template.

    NOTE: Short keys risk false positives in LLM mode. Same documented
    limitation as other stubs in this pipeline.
    """
    proto = context.get("artifact_inputs", {}).get("prototype_spec", {})
    world_theme = proto.get("concept_anchor", {}).get("world_theme", "")

    concept_key = None
    theme_lower = world_theme.lower()
    for key in CONCEPT_OVERRIDES:
        if key in theme_lower:
            concept_key = key
            break

    t = CONCEPT_OVERRIDES[concept_key] if concept_key else _GENERIC_IMPLEMENTATION_PLAN

    return {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "status": "pass",
        "implementation_objective":  t["implementation_objective"],
        "tech_stack":                t["tech_stack"],
        "file_manifest":             t["file_manifest"],
        "component_breakdown":       t["component_breakdown"],
        "state_model":               t["state_model"],
        "data_flow":                 t["data_flow"],
        "reusable_logic":            t["reusable_logic"],
        "build_order":               t["build_order"],
        "test_targets":              t["test_targets"],
        "open_engineering_questions": t["open_engineering_questions"],
        "implementation_notes":      t["implementation_notes"],
    }


# ---------------------------------------------------------------------------
# AgentSpec + run()
# ---------------------------------------------------------------------------

def build_spec(repo_root: Path) -> AgentSpec:
    return AgentSpec(
        agent_name="implementation_plan_agent",
        expected_output_artifact="implementation_plan",
        expected_produced_by="Implementation Plan Agent",
        prompt_path=repo_root / "agents" / "implementation_plan" / "prompt.md",
        config_path=repo_root / "agents" / "implementation_plan" / "config.yaml",
        allowed_reads=["prototype_ui_spec", "prototype_build_spec", "prototype_spec"],
        allowed_writes=["implementation_plan"],
        max_revision_count=2,
    )


def run(
    repo_root: Path,
    job_id: str,
    artifact_paths: Dict[str, Path],
    model_callable=None,
):
    """Run the Implementation Plan Agent.

    Args:
        model_callable: Optional override. If provided, replaces the stub.
                        If None, uses the deterministic stub.
    """
    runner = SharedAgentRunner(repo_root)
    return runner.run(
        spec=build_spec(repo_root),
        job_id=job_id,
        artifact_paths=artifact_paths,
        model_callable=model_callable if model_callable is not None else implementation_plan_stub,
    )
