"""
Prototype Build Spec Agent — Stage 7.

Translates an approved prototype_spec into a developer-ready first-build handoff
with explicit state model, event flow, component behavior, and edge cases.

Modes:
    Stub: deterministic keyword-based templates (concept overrides + generic fallback).
    LLM:  model_callable replaces the stub.
"""
from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from utils.shared_agent_runner import AgentSpec, SharedAgentRunner

# ---------------------------------------------------------------------------
# Concept-specific overrides — rich, implementation-ready build specs
# ---------------------------------------------------------------------------

CONCEPT_OVERRIDES: Dict[str, Dict[str, Any]] = {
    "bakery": {
        "build_objective": (
            "Implement a single-screen tap-to-add bakery loop where a K-2 learner "
            "fills a pastry box to match a customer's target number, with overshoot "
            "bounce-back as the primary error-handling mechanic."
        ),
        "must_exist": [
            "Single bakery round screen with customer ticket, pastry tray, pastry box, and running total",
            "Tap-to-add interaction: tap a pastry item to move it into the box",
            "Running total updates after each tap",
            "Exact-match detection: total == target triggers success",
            "Overshoot detection: total > target triggers bounce-back of last item",
            "Success feedback: box snap animation, customer satisfaction state",
            "Overshoot feedback: last item bounces back out, total decrements",
            "Round transition: next customer loads after success",
            "5-round session with varied targets",
        ],
        "not_included": [
            "Score display or scoring system",
            "Lives or retry limits",
            "Account system or persistent state",
            "Analytics or telemetry",
        ],
        "deferred_from_prototype": [
            "Timer pressure",
            "Streak scoring",
            "Difficulty progression beyond one short sequence",
            "Multiple pastry types with different values",
            "Hint system",
            "Sound design beyond placeholder effects",
        ],
        "screen_state_map": [
            {
                "state_id": "round_active",
                "state_name": "Round Active",
                "visible_elements": [
                    "Customer character with ticket showing target number",
                    "Empty pastry box (or partially filled from prior taps)",
                    "Pastry tray with tappable pastry items",
                    "Running total display showing current count",
                ],
                "allowed_player_actions": [
                    "Tap a pastry item on the tray to add it to the box",
                ],
                "transition_rules": [
                    "On tap: if current_total + 1 == target → transition to success_feedback",
                    "On tap: if current_total + 1 > target → transition to overshoot_feedback",
                    "On tap: if current_total + 1 < target → remain in round_active with updated total",
                ],
            },
            {
                "state_id": "success_feedback",
                "state_name": "Success Feedback",
                "visible_elements": [
                    "Pastry box with snap/close animation",
                    "Customer satisfaction indicator (smile, checkmark, or glow)",
                    "Running total showing matched target",
                ],
                "allowed_player_actions": [],
                "transition_rules": [
                    "After 1.5-second feedback display → if round_index < max_rounds, transition to round_active with next customer",
                    "After 1.5-second feedback display → if round_index == max_rounds, transition to session_complete",
                ],
            },
            {
                "state_id": "overshoot_feedback",
                "state_name": "Overshoot Feedback",
                "visible_elements": [
                    "Last added pastry item animating bounce-back out of box",
                    "Running total decrementing by 1",
                    "Pastry tray with items still available",
                ],
                "allowed_player_actions": [],
                "transition_rules": [
                    "After bounce-back animation completes (~0.5 seconds) → transition to round_active with total restored to pre-overshoot value",
                ],
            },
            {
                "state_id": "session_complete",
                "state_name": "Session Complete",
                "visible_elements": [
                    "Simple completion message (e.g., 'All orders filled!')",
                    "Replay prompt",
                ],
                "allowed_player_actions": [
                    "Tap to replay (resets session from round 1)",
                ],
                "transition_rules": [
                    "On tap replay → transition to round_active with round_index = 1 and new target sequence",
                ],
            },
        ],
        "component_specs": [
            {
                "component_name": "customer_ticket",
                "purpose": "Display the target number for the current round.",
                "inputs": ["target (integer)"],
                "outputs": ["Rendered ticket showing the target number"],
                "state_dependencies": ["target"],
                "behavior_rules": [
                    "Display target as a large, clearly readable number on a ticket card",
                    "Update when round_index changes and a new target is loaded",
                    "Remain static during the round — does not animate or change mid-round",
                ],
            },
            {
                "component_name": "pastry_tray",
                "purpose": "Present tappable pastry items the learner can add to the box.",
                "inputs": ["Tap events from the player"],
                "outputs": ["Emits 'item_added' event on valid tap"],
                "state_dependencies": ["is_animating"],
                "behavior_rules": [
                    "Display a row or grid of pastry items (minimum 10 visible items)",
                    "Each item has value 1 in the first build (all identical)",
                    "On tap: if is_animating == false, emit item_added event",
                    "On tap: if is_animating == true, ignore tap (prevent double-tap during animation)",
                    "Tapped item visually moves from tray toward the pastry box",
                    "Tray items are not consumed — tray always shows available items",
                ],
            },
            {
                "component_name": "pastry_box",
                "purpose": "Visually receive items and represent the accumulated total.",
                "inputs": ["item_added event", "bounce_back event"],
                "outputs": ["Visual state of items in the box"],
                "state_dependencies": ["current_total", "items_in_box"],
                "behavior_rules": [
                    "On item_added: animate item entering the box, increment visual item count",
                    "On bounce_back: animate last item exiting the box, decrement visual item count",
                    "On success: play box snap/close animation",
                    "On round reset: clear all items from box, show empty state",
                ],
            },
            {
                "component_name": "running_total_display",
                "purpose": "Show the current accumulated count after each action.",
                "inputs": ["current_total (integer)"],
                "outputs": ["Rendered number"],
                "state_dependencies": ["current_total"],
                "behavior_rules": [
                    "Display current_total as a clearly readable number",
                    "Update immediately after each item_added or bounce_back event",
                    "On round reset: display 0",
                    "Position near or attached to the pastry box for spatial association",
                ],
            },
            {
                "component_name": "success_feedback",
                "purpose": "Deliver the signature moment when the target is matched.",
                "inputs": ["success event"],
                "outputs": ["Visual confirmation animation"],
                "state_dependencies": ["round_status"],
                "behavior_rules": [
                    "On success: box snaps closed, customer shows satisfaction (smile or glow)",
                    "Animation duration: ~1.5 seconds",
                    "During animation: all tray taps are disabled",
                    "After animation: trigger round transition",
                ],
            },
            {
                "component_name": "overshoot_feedback",
                "purpose": "Deliver the bounce-back when the learner overshoots the target.",
                "inputs": ["overshoot event"],
                "outputs": ["Bounce-back animation, total decrement"],
                "state_dependencies": ["current_total", "round_status"],
                "behavior_rules": [
                    "On overshoot: last item animates bouncing back out of the box",
                    "Running total decrements by 1 after bounce-back completes",
                    "Animation duration: ~0.5 seconds",
                    "During animation: all tray taps are disabled",
                    "After animation: return to round_active — learner can continue tapping",
                ],
            },
        ],
        "interaction_event_flow": [
            {
                "step_number": 1,
                "trigger": "Round begins (first round or previous round completed)",
                "system_response": "Load next target from sequence. Display customer ticket, empty box, full tray, total = 0.",
                "state_change": "target = targets[round_index], current_total = 0, items_in_box = [], round_status = active, is_animating = false",
            },
            {
                "step_number": 2,
                "trigger": "Player taps a pastry item on the tray",
                "system_response": "Check is_animating. If true, ignore tap. If false, set is_animating = true, animate item moving from tray to box.",
                "state_change": "is_animating = true",
            },
            {
                "step_number": 3,
                "trigger": "Item-enter-box animation completes",
                "system_response": "Increment current_total by 1. Append item to items_in_box. Update running total display. Evaluate: current_total vs target.",
                "state_change": "current_total += 1, items_in_box.append(item), is_animating = false",
            },
            {
                "step_number": 4,
                "trigger": "Evaluation: current_total == target",
                "system_response": "Set round_status = success. Trigger success_feedback animation (box snap, customer satisfaction).",
                "state_change": "round_status = success, is_animating = true",
            },
            {
                "step_number": 5,
                "trigger": "Evaluation: current_total > target (overshoot)",
                "system_response": "Set round_status = overshoot. Trigger overshoot_feedback animation (last item bounces back).",
                "state_change": "round_status = overshoot, is_animating = true",
            },
            {
                "step_number": 6,
                "trigger": "Evaluation: current_total < target",
                "system_response": "No special action. Learner may tap again. Set is_animating = false.",
                "state_change": "is_animating = false (ready for next tap)",
            },
            {
                "step_number": 7,
                "trigger": "Overshoot animation completes",
                "system_response": "Decrement current_total by 1. Remove last item from items_in_box. Update running total display. Return to round_active.",
                "state_change": "current_total -= 1, items_in_box.pop(), round_status = active, is_animating = false",
            },
            {
                "step_number": 8,
                "trigger": "Success animation completes (1.5 seconds)",
                "system_response": "Increment round_index. If round_index < max_rounds, load next round. If round_index == max_rounds, show session_complete.",
                "state_change": "round_index += 1",
            },
        ],
        "state_model": {
            "tracked_variables": [
                "target: integer — the customer's order number for this round",
                "current_total: integer — running count of items in the box",
                "items_in_box: array — list of items currently in the box (for visual state)",
                "round_index: integer — current round number (1-based, max 5)",
                "round_status: enum(active, success, overshoot) — current round phase",
                "is_animating: boolean — true during any animation, blocks tap input",
                "targets: array of integers — the sequence of target numbers for the session",
            ],
            "derived_values": [
                "is_overshoot = current_total > target",
                "is_match = current_total == target",
                "is_session_complete = round_index > max_rounds",
                "can_tap = round_status == active AND is_animating == false",
            ],
            "reset_rules": [
                "On new round: current_total = 0, items_in_box = [], round_status = active, is_animating = false, target = targets[round_index]",
                "On session replay: round_index = 1, generate new targets sequence, then apply new-round reset",
                "On overshoot recovery: current_total -= 1, items_in_box.pop(), round_status = active, is_animating = false",
            ],
        },
        "edge_cases": [
            {
                "case_name": "Double-tap during animation",
                "expected_behavior": "All taps are ignored while is_animating == true. The tap queue is not buffered — taps during animation are silently discarded.",
            },
            {
                "case_name": "Tap during overshoot bounce-back",
                "expected_behavior": "Tap is ignored. is_animating remains true until bounce-back animation completes and state returns to round_active.",
            },
            {
                "case_name": "Target equals 1",
                "expected_behavior": "A single tap triggers success immediately. The round is valid — it tests whether the learner understands the mechanic at its simplest.",
            },
            {
                "case_name": "Rapid successive taps before animation completes",
                "expected_behavior": "Only the first tap registers. Subsequent taps during the item-enter-box animation are discarded. No double-counting.",
            },
            {
                "case_name": "Overshoot on the last item before target",
                "expected_behavior": "If current_total is target - 1 this cannot overshoot (adding 1 matches exactly). Overshoot only occurs when current_total + 1 > target, which requires current_total >= target. This case is impossible with value-1 items and is listed to confirm the boundary is understood.",
            },
            {
                "case_name": "Session replay after completion",
                "expected_behavior": "Full state reset: new target sequence generated, round_index = 1, all round state cleared. Player starts a fresh 5-round session.",
            },
        ],
        "asset_plan": {
            "required_now": [
                "Rectangular pastry box shape (can be a colored rectangle with border)",
                "Pastry item shape (can be a colored circle or simple icon)",
                "Customer character placeholder (can be a simple avatar or silhouette)",
                "Ticket card shape showing target number",
                "Running total number display",
            ],
            "placeholder_allowed": [
                "Bakery background (solid color or gradient is sufficient)",
                "Customer animation (static image is sufficient)",
                "Success animation (color flash or simple scale pulse)",
                "Bounce-back animation (simple translate-out motion)",
            ],
            "not_needed_yet": [
                "Final bakery art or themed illustrations",
                "Sound effects (visual-only feedback for first build)",
                "Multiple pastry varieties with different appearances",
                "Customer variety (one placeholder customer is sufficient)",
            ],
        },
        "build_sequence": {
            "phase_1_order": [
                "1. Render static round screen: ticket, empty box, tray with items, total display at 0",
                "2. Implement tap-to-add: tap tray item → item animates into box → total increments",
                "3. Implement match detection: current_total == target → success feedback",
                "4. Implement overshoot detection: current_total > target → bounce-back → total decrements",
                "5. Implement animation lock: disable taps during any animation (is_animating flag)",
                "6. Implement round transition: after success → load next target → reset round state",
                "7. Implement 5-round session: cycle through target sequence, show session_complete after round 5",
                "8. Implement session replay: tap on session_complete → reset everything → start new session",
            ],
            "phase_1_done_definition": [
                "Learner can tap pastry items to fill the box toward a target number",
                "Running total updates correctly after each tap",
                "Exact match triggers visible success feedback and advances to next round",
                "Overshoot triggers bounce-back of last item and decrements total by 1",
                "Taps are ignored during all animations (no double-counting)",
                "5 rounds complete without errors or stuck states",
                "Session replay works from the completion screen",
            ],
        },
        "acceptance_checklist": [
            "A learner can complete 5 rounds from start to session_complete without encountering a blocking error",
            "Running total accurately reflects the number of items in the box at all times",
            "Overshoot on any round triggers bounce-back and returns to round_active (not stuck)",
            "No taps register during animations (double-tap produces no effect)",
            "Each round loads a different target number from the sequence",
            "Session replay resets all state and starts a new 5-round session",
            "All feedback (success, overshoot) is visually distinguishable without sound",
            "A first-time observer can understand the goal within 10 seconds of watching",
        ],
        "open_build_questions": [
            "Should pastry items in the tray be arranged in a single row or a grid? (Recommend: single row of 10+ items for simplicity.)",
            "Should the running total animate (count up) or snap to the new value? (Recommend: snap for clarity.)",
            "Should the success feedback auto-advance to the next round, or require a tap to continue? (Recommend: auto-advance after 1.5s delay.)",
        ],
        "notes": (
            "This build spec intentionally uses value-1 pastry items only. Mixed values "
            "are deferred to a later build phase. All art can be geometric placeholders. "
            "The primary test is whether the tap-to-add loop with overshoot bounce-back "
            "is understandable and satisfying for K-2 learners."
        ),
    },
}

# ---------------------------------------------------------------------------
# Generic templates — one per interaction type, thin but structurally valid
# ---------------------------------------------------------------------------

GENERIC_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "combine_and_build": {
        "build_objective": "Implement a single-screen combine-and-build loop where the learner accumulates items to match a target.",
    },
    "route_and_dispatch": {
        "build_objective": "Implement a single-screen route-and-dispatch loop where the learner selects the correct destination or vehicle.",
    },
    "allocate_and_balance": {
        "build_objective": "Implement a single-screen allocate-and-balance loop where the learner distributes resources to satisfy constraints.",
    },
    "transform_and_manipulate": {
        "build_objective": "Implement a single-screen transform-and-manipulate loop where the learner applies a transformation to match a target state.",
    },
    "navigate_and_position": {
        "build_objective": "Implement a single-screen navigate-and-position loop where the learner places an element at the correct location.",
    },
    "sequence_and_predict": {
        "build_objective": "Implement a single-screen sequence-and-predict loop where the learner identifies the next element in a pattern.",
    },
}


# ---------------------------------------------------------------------------
# Default builders for generic fallback
# ---------------------------------------------------------------------------

def _default_screen_state_map() -> list:
    return [
        {
            "state_id": "round_active",
            "state_name": "Round Active",
            "visible_elements": ["Primary game element", "Target display", "Feedback area"],
            "allowed_player_actions": ["Perform primary interaction"],
            "transition_rules": [
                "On correct action → transition to success_feedback",
                "On incorrect action → transition to error_feedback",
            ],
        },
        {
            "state_id": "success_feedback",
            "state_name": "Success Feedback",
            "visible_elements": ["Success indicator", "Target confirmation"],
            "allowed_player_actions": [],
            "transition_rules": [
                "After feedback delay → transition to round_active with next target",
                "After final round → transition to session_complete",
            ],
        },
        {
            "state_id": "error_feedback",
            "state_name": "Error Feedback",
            "visible_elements": ["Error indicator", "Correction guidance"],
            "allowed_player_actions": [],
            "transition_rules": [
                "After error animation → transition to round_active for retry",
            ],
        },
    ]


def _default_component_specs() -> list:
    return [
        {
            "component_name": "primary_game_element",
            "purpose": "The main interactive element the player acts on.",
            "inputs": ["Player interaction event"],
            "outputs": ["Action result event"],
            "state_dependencies": ["is_animating"],
            "behavior_rules": [
                "Accept player input when is_animating == false",
                "Ignore input during animations",
                "Emit result event after action completes",
            ],
        },
        {
            "component_name": "target_display",
            "purpose": "Show the current round's target or goal.",
            "inputs": ["target value"],
            "outputs": ["Rendered target"],
            "state_dependencies": ["target"],
            "behavior_rules": [
                "Display target clearly and prominently",
                "Update on round transition",
            ],
        },
        {
            "component_name": "feedback_display",
            "purpose": "Show success or error feedback after each action.",
            "inputs": ["action result event"],
            "outputs": ["Visual feedback animation"],
            "state_dependencies": ["round_status"],
            "behavior_rules": [
                "On success: show confirmation animation",
                "On error: show correction animation",
                "During feedback: disable player input",
            ],
        },
    ]


def _default_event_flow() -> list:
    return [
        {
            "step_number": 1,
            "trigger": "Round begins",
            "system_response": "Load target. Display game elements. Set round_status = active.",
            "state_change": "target = next_target, round_status = active, is_animating = false",
        },
        {
            "step_number": 2,
            "trigger": "Player performs primary action",
            "system_response": "Validate action against target. Determine success or failure.",
            "state_change": "is_animating = true",
        },
        {
            "step_number": 3,
            "trigger": "Action evaluated as correct",
            "system_response": "Display success feedback. After delay, advance to next round.",
            "state_change": "round_status = success, round_index += 1",
        },
        {
            "step_number": 4,
            "trigger": "Action evaluated as incorrect",
            "system_response": "Display error feedback. After animation, return to round_active for retry.",
            "state_change": "round_status = error, is_animating = true",
        },
    ]


def _default_state_model() -> dict:
    return {
        "tracked_variables": [
            "target — the goal for this round",
            "round_index: integer — current round number",
            "round_status: enum(active, success, error) — current phase",
            "is_animating: boolean — true during animations, blocks input",
        ],
        "derived_values": [
            "is_session_complete = round_index > max_rounds",
        ],
        "reset_rules": [
            "On new round: target = next value, round_status = active, is_animating = false",
            "On session replay: round_index = 1, reload targets",
        ],
    }


def _default_edge_cases() -> list:
    return [
        {
            "case_name": "Input during animation",
            "expected_behavior": "All input is ignored while is_animating == true.",
        },
        {
            "case_name": "Rapid successive inputs",
            "expected_behavior": "Only the first input registers. Subsequent inputs during processing are discarded.",
        },
        {
            "case_name": "Final round completion",
            "expected_behavior": "Session transitions to completion state. Replay option is presented.",
        },
    ]


# ---------------------------------------------------------------------------
# Stub callable
# ---------------------------------------------------------------------------

def prototype_build_spec_stub(context: Dict[str, Any]) -> Dict[str, Any]:
    proto = context["artifact_inputs"]["prototype_spec"]

    world_theme = proto.get("concept_anchor", {}).get("world_theme", "unknown")
    interaction_type = proto.get("concept_anchor", {}).get("primary_interaction_type", "combine_and_build")

    # --- Select best template: concept-specific override > generic ---
    # NOTE: Short keys ("fire", "pizza") risk false positives in LLM mode.
    # See agents/prototype_spec/agent.py for the same documented limitation.
    concept_key = None
    theme_lower = world_theme.lower()
    for key in CONCEPT_OVERRIDES:
        if key in theme_lower:
            concept_key = key
            break

    if concept_key:
        t = CONCEPT_OVERRIDES[concept_key]
    else:
        t = GENERIC_TEMPLATES.get(interaction_type, GENERIC_TEMPLATES["combine_and_build"])

    # --- Build scope ---
    proto_scope = proto.get("prototype_scope", {})

    build_scope = {
        "must_exist_in_v1_build": t.get("must_exist", [
            "Core interaction loop",
            "Success and failure detection",
            "Basic feedback display",
            "Round transition",
            "5-round session",
        ]),
        "not_included_in_v1_build": t.get("not_included", [
            "Progression systems",
            "Account or persistent state",
            "Analytics",
            "Final art or audio",
            "Timer or scoring",
        ]),
        "deferred_from_prototype": t.get("deferred_from_prototype", proto_scope.get("deferred", [])),
    }

    # --- Screen state map ---
    screen_state_map = t.get("screen_state_map", _default_screen_state_map())

    # --- Component specs ---
    component_specs = t.get("component_specs", _default_component_specs())

    # --- Event flow ---
    event_flow = t.get("interaction_event_flow", _default_event_flow())

    # --- State model ---
    state_model = t.get("state_model", _default_state_model())

    # --- Edge cases ---
    edge_cases = t.get("edge_cases", _default_edge_cases())

    # --- Asset plan ---
    asset_plan = t.get("asset_plan", {
        "required_now": ["Primary game element rendering", "Target display", "Feedback indicators"],
        "placeholder_allowed": ["Background art", "Character art", "Animation polish"],
        "not_needed_yet": ["Final art", "Sound effects", "Multiple content variants"],
    })

    # --- Build sequence ---
    build_sequence = t.get("build_sequence", {
        "phase_1_order": [
            "1. Render static round screen with game elements",
            "2. Implement primary interaction",
            "3. Implement success/failure detection",
            "4. Implement feedback display",
            "5. Implement round transition",
            "6. Implement 5-round session cycle",
        ],
        "phase_1_done_definition": [
            "Learner can complete the primary action",
            "Success and failure are detected correctly",
            "5 rounds complete without errors",
        ],
    })

    # --- Acceptance checklist ---
    acceptance_checklist = t.get("acceptance_checklist", [
        "Learner can complete 5 rounds without blocking errors",
        "Success and failure feedback are visually distinguishable",
        "Round transitions work correctly",
        "No input registers during animations",
    ])

    # --- Open questions ---
    open_questions = t.get("open_build_questions", [])

    # --- Notes ---
    notes = t.get("notes", (
        f"Build spec for '{interaction_type}' prototype. "
        f"World theme: {world_theme}."
    ))

    # --- Status ---
    status = "pass" if concept_key else "pass"

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "status": status,
        "timestamp": timestamp,
        "build_objective": t.get("build_objective", f"Implement a single-screen {interaction_type} prototype loop."),
        "build_scope": build_scope,
        "screen_state_map": screen_state_map,
        "component_specs": component_specs,
        "interaction_event_flow": event_flow,
        "state_model": state_model,
        "edge_cases": edge_cases,
        "asset_plan": asset_plan,
        "build_sequence": build_sequence,
        "acceptance_checklist": acceptance_checklist,
        "open_build_questions": open_questions,
        "notes": notes,
    }


def build_spec(repo_root: Path) -> AgentSpec:
    return AgentSpec(
        agent_name="prototype_build_spec_agent",
        expected_output_artifact="prototype_build_spec",
        expected_produced_by="Prototype Build Spec Agent",
        prompt_path=repo_root / "agents" / "prototype_build_spec" / "prompt.md",
        config_path=repo_root / "agents" / "prototype_build_spec" / "config.yaml",
        allowed_reads=[
            "prototype_spec",
            "lowest_viable_loop_brief",
            "interaction_decision_memo",
        ],
        allowed_writes=["prototype_build_spec"],
        max_revision_count=2,
    )


def run(
    repo_root: Path,
    job_id: str,
    artifact_paths: Dict[str, Path],
    model_callable=None,
):
    """Run the Prototype Build Spec Agent.

    Args:
        model_callable: Optional override. If provided, replaces the stub.
                        If None, uses the deterministic stub.
    """
    runner = SharedAgentRunner(repo_root)
    return runner.run(
        spec=build_spec(repo_root),
        job_id=job_id,
        artifact_paths=artifact_paths,
        model_callable=model_callable if model_callable is not None else prototype_build_spec_stub,
    )
