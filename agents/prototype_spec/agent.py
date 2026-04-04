from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List

from utils.shared_agent_runner import AgentSpec, SharedAgentRunner


# ---------------------------------------------------------------------------
# Concept-specific prototype specs
#
# Each key matches a world_theme keyword. The stub selects the most specific
# match available, falling back to the interaction-type generic template.
# These are prototype-level translations — concrete build language, not
# abstract loop descriptions.
# ---------------------------------------------------------------------------

CONCEPT_OVERRIDES: Dict[str, Dict[str, Any]] = {
    "bakery": {
        "prototype_goal": (
            "Prove that early elementary learners can understand and enjoy a "
            "combine_and_build loop for addition to 20 without extra explanation."
        ),
        "prototype_question": (
            "Can a learner reach the correct target total by selecting pastry items "
            "one at a time and feel the target match as a satisfying repeated success moment?"
        ),
        "player_goal_each_round": (
            "Fill the pastry box so the running total exactly matches the customer "
            "ticket number."
        ),
        "first_visible_state": (
            "A customer appears with a ticket showing a target number and an empty "
            "pastry box appears beside a tray of pastry items."
        ),
        "first_player_action": (
            "Tap one pastry item to place it into the box and increase the running total."
        ),
        "success_condition": "The running total equals the target number exactly.",
        "fail_condition": "The running total goes above the target number.",
        "reset_or_retry_behavior": (
            "If the player overshoots, the last pastry item pops back out and the total "
            "returns to the previous value so the learner can continue."
        ),
        "signature_moment_delivery": (
            "When the total hits the exact target, the box snaps shut immediately and "
            "the customer leaves satisfied."
        ),
        "input_types": ["tap"],
        "math_action_mapping": (
            "Each tap adds one selected pastry value into the box and updates the total, "
            "so the act of building the box is the arithmetic."
        ),
        "feedback_timing": "immediate",
        "error_handling": (
            "Overshoot causes the last item to bounce back out instantly, preserving "
            "the learner's prior correct total and reducing frustration."
        ),
        "screens": [
            {
                "screen_id": "bakery_round",
                "screen_name": "Bakery Round Screen",
                "purpose": "Deliver the full prototype loop in one screen with no menu dependency.",
                "elements_present": [
                    "Customer with visible ticket number",
                    "Empty pastry box",
                    "Pastry tray with selectable items",
                    "Running total display",
                    "Automatic next-round transition or simple replay state",
                ],
                "player_actions": [
                    "Tap pastry item to add to box",
                    "Observe running total updating",
                    "Continue adding items until target match",
                ],
                "exit_condition": (
                    "Round ends when the target is matched and the system either loads "
                    "the next round or shows a replay state."
                ),
            },
        ],
        "ui_components": [
            {
                "component_name": "customer_ticket",
                "purpose": "Shows the target number for the order.",
                "required_now": True,
            },
            {
                "component_name": "pastry_box",
                "purpose": "Receives selected items and visually represents the build action.",
                "required_now": True,
            },
            {
                "component_name": "pastry_tray",
                "purpose": "Offers clickable items for accumulation.",
                "required_now": True,
            },
            {
                "component_name": "running_total_display",
                "purpose": "Shows the current accumulated amount clearly after each action.",
                "required_now": True,
            },
            {
                "component_name": "success_feedback",
                "purpose": "Delivers the box snap, visual confirmation, and customer satisfaction state.",
                "required_now": True,
            },
            {
                "component_name": "overshoot_feedback",
                "purpose": "Shows bounce-back behavior when the learner goes over the target.",
                "required_now": True,
            },
        ],
        "scope_included": [
            "One playable round structure",
            "Single customer order at a time",
            "Target number shown clearly",
            "Tap to add pastry items into the box",
            "Running total updates after each tap",
            "Success feedback when total matches target",
            "Fail feedback when total exceeds target",
            "Automatic bounce-back of the last item on overshoot",
            "Simple replay into the next order",
        ],
        "scope_excluded": [
            "Full level map",
            "Multiple worlds",
            "Lives system",
            "Full progression tree",
            "Account system",
            "Teacher dashboard",
            "Analytics system",
            "Voice acting",
            "Final art polish",
        ],
        "scope_deferred": [
            "Timer pressure",
            "Streak scoring",
            "Difficulty progression beyond one short sequence",
            "Multiple pastry types with different values",
            "Hint system",
            "Sound design beyond placeholder effects",
        ],
        "sample_targets": [
            "target 6",
            "target 7",
            "target 10",
            "target 13",
            "target 18",
        ],
        "content_variation": [
            "Mix of targets below 10 and above 10",
            "Enough repetition to observe understanding",
            "Option to use identical-value items first before introducing mixed values later",
        ],
        "must_build_first": [
            "Single-screen loop",
            "Tap-to-add interaction",
            "Running total state update",
            "Exact match detection",
            "Overshoot bounce-back logic",
            "Success transition to next round",
        ],
        "can_fake_or_stub": [
            "Final bakery art",
            "Advanced pastry variety",
            "Full progression",
            "Sound polish",
            "Customer animation polish",
        ],
        "known_risks": [
            "If all pastries are visually identical, the loop may feel too abstract",
            "If mixed-value pastries are introduced too early, cognitive load may rise too fast",
            "If feedback is too slow, the signature moment may weaken",
        ],
        "playtest_must_prove": [
            "Learners understand the goal without much explanation",
            "The combine_and_build action feels like the math itself",
            "Overshoot bounce-back teaches without creating anxiety",
            "The success moment is satisfying enough to repeat",
        ],
        "success_signals": [
            "Learner begins tapping toward target quickly",
            "Learner watches and responds to the running total",
            "Learner self-corrects after overshoot",
            "Learner shows satisfaction or wants another round",
        ],
        "failure_signals": [
            "Learner does not understand what to do after initial view",
            "Learner ignores the target number or running total",
            "Overshoot behavior causes confusion instead of learning",
            "Loop feels flat or repetitive after one or two rounds",
        ],
        "test_users": [
            "1st grade learners",
            "2nd grade learners",
            "Teacher or parent observer",
        ],
        "visual_assets": [
            "Simple bakery background",
            "Customer character placeholder",
            "Ticket card",
            "Pastry item placeholder art",
            "Pastry box art",
            "Running total display",
        ],
        "audio_assets": [
            "Box snap sound placeholder",
            "Soft incorrect bounce-back sound placeholder",
        ],
        "score_used": False,
        "timer_used": False,
        "lives_used": False,
        "hinting_used": False,
        "difficulty_scaling_used": "light",
        "session_end_rule": (
            "Prototype session ends after 5 rounds or after the observer has enough "
            "evidence about loop clarity and learner behavior."
        ),
        "open_questions": [
            "Should the first prototype use all pastry items as value 1 for pure counting-on, "
            "or introduce mixed values immediately?",
            "Should the next round load automatically, or should the learner tap to confirm readiness?",
            "Should the running total be centered above the box or attached visually to the box itself?",
        ],
        "notes": (
            "This prototype intentionally removes timer pressure and score pressure from "
            "the first build so the core addition loop can be evaluated cleanly."
        ),
    },
    "fire": {
        "prototype_goal": (
            "Prove that the route-and-dispatch loop makes arithmetic comparison the "
            "decision driver and that learners understand the dispatch metaphor without "
            "explanation."
        ),
        "prototype_question": (
            "Can a learner identify the correct truck by comparing demand and capacity "
            "numbers and dispatch it within 10 seconds without help?"
        ),
        "player_goal_each_round": (
            "Read the incident demand number, compare it against truck capacity labels, "
            "and tap the matching truck to dispatch it."
        ),
        "first_visible_state": (
            "An incident card appears with a demand number. Two trucks sit at the station, "
            "each labeled with a capacity number. One matches the demand."
        ),
        "first_player_action": "Tap the truck whose capacity matches the incident demand.",
        "success_condition": "The selected truck's capacity equals the incident demand.",
        "fail_condition": "The wrong truck is selected or the incident timer expires.",
        "reset_or_retry_behavior": (
            "Wrong truck shakes and returns to the station. The incident persists for retry. "
            "No penalty beyond lost time."
        ),
        "signature_moment_delivery": (
            "Correct truck launches toward the incident with a siren flash. Incident card "
            "clears from the board."
        ),
        "input_types": ["tap"],
        "math_action_mapping": (
            "Truck selection requires comparing capacity numbers against demand — the "
            "routing decision IS the arithmetic comparison."
        ),
        "feedback_timing": "immediate",
        "error_handling": (
            "Incorrect dispatch triggers a shake on the truck. Truck returns to station. "
            "Incident persists for retry."
        ),
        "screens": [
            {
                "screen_id": "dispatch_screen",
                "screen_name": "Dispatch Screen",
                "purpose": "Deliver the full dispatch loop in one screen.",
                "elements_present": [
                    "Incident card with demand number",
                    "Truck lineup with capacity labels",
                    "Station background",
                    "Incident timer bar",
                    "Shift progress indicator (e.g., incident 2 of 5)",
                ],
                "player_actions": [
                    "Read incident demand number",
                    "Compare against truck capacity labels",
                    "Tap the matching truck to dispatch",
                ],
                "exit_condition": "Correct truck dispatched or incident timer expires.",
            },
            {
                "screen_id": "shift_summary",
                "screen_name": "Shift Summary",
                "purpose": "Show session results after one shift.",
                "elements_present": [
                    "Incidents handled count",
                    "Accuracy summary",
                    "Replay prompt",
                ],
                "player_actions": ["Tap to start a new shift or exit"],
                "exit_condition": "Player taps replay or session ends.",
            },
        ],
        "ui_components": [
            {"component_name": "incident_card", "purpose": "Displays the demand number the player must match", "required_now": True},
            {"component_name": "truck_lineup", "purpose": "Shows available trucks with capacity labels", "required_now": True},
            {"component_name": "incident_timer", "purpose": "Creates mild urgency per incident", "required_now": True},
            {"component_name": "dispatch_animation", "purpose": "Visual payoff when correct truck is sent", "required_now": True},
            {"component_name": "shake_feedback", "purpose": "Shows error on wrong dispatch without punishing", "required_now": True},
            {"component_name": "shift_summary_overlay", "purpose": "Communicates session performance", "required_now": True},
        ],
        "scope_included": [
            "One shift of 5 incidents",
            "Single incident at a time",
            "Demand number shown on incident card",
            "Two trucks with capacity labels (one correct)",
            "Tap to dispatch the matching truck",
            "Immediate feedback on correct and incorrect dispatch",
            "Shift summary after 5 incidents",
        ],
        "scope_excluded": [
            "Supply mechanic (allocate_and_balance)",
            "Multiple simultaneous incidents",
            "Progression across shifts",
            "Account system or persistent state",
            "Teacher dashboard",
            "Analytics",
            "Final art or voice acting",
        ],
        "scope_deferred": [
            "Three-truck incidents (currently two trucks only)",
            "Supply mechanic loop (level 4+)",
            "Difficulty progression across shifts",
            "Dispatcher rank or badge system",
            "Sound design beyond placeholder effects",
        ],
        "sample_targets": [
            "Demand 12, trucks [12, 8]",
            "Demand 15, trucks [15, 20]",
            "Demand 7, trucks [7, 11]",
            "Demand 20, trucks [13, 20]",
            "Demand 9, trucks [9, 14]",
        ],
        "content_variation": [
            "Vary demand numbers within the arithmetic comparison range",
            "Randomize truck order so correct truck is not always first",
            "Ensure distractor capacity is not trivially different from demand",
        ],
        "must_build_first": [
            "Incident card generation with demand numbers",
            "Truck capacity assignment (one correct, one distractor)",
            "Match detection (selected capacity == demand)",
            "Dispatch animation on correct selection",
            "Shake-and-return on incorrect selection",
            "Shift counter and summary transition",
        ],
        "can_fake_or_stub": [
            "Siren audio (visual-only dispatch animation is sufficient)",
            "Truck and station art (labeled rectangles work)",
            "Shift scoring beyond simple count",
            "Background animation",
        ],
        "known_risks": [
            "If trucks always appear in the same order, learners route by position not math",
            "If demand and capacity numbers are too far apart, the comparison is trivial",
            "If learners do not understand that truck labels are capacities, they will tap randomly",
        ],
        "playtest_must_prove": [
            "Learner reads the demand number before selecting a truck",
            "Learner dispatches correctly on first attempt for at least 3 of 5 incidents",
            "Learner understands the dispatch metaphor without verbal explanation",
            "Wrong dispatch feels informative, not frustrating",
        ],
        "success_signals": [
            "Child reads the demand number aloud or visibly checks it before acting",
            "Child dispatches correctly within 10 seconds on average",
            "Child treats wrong dispatch as a cue to re-read, not as a punishment",
            "Child wants to play another shift",
        ],
        "failure_signals": [
            "Child taps the first truck without reading the demand",
            "Child does not understand that truck numbers represent capacity",
            "Child gives up after two incorrect dispatches in a row",
        ],
        "test_users": [
            "Grade 3 students (ages 8-9) with basic arithmetic comparison skills",
            "Grade 3-4 students who can compare two-digit numbers",
            "Teacher or parent observer",
        ],
        "visual_assets": [
            "Simple fire station background",
            "Incident card placeholder",
            "Truck placeholder art with capacity labels",
            "Dispatch animation frames",
            "Shift summary display",
        ],
        "audio_assets": [
            "Dispatch siren placeholder",
            "Error shake sound placeholder",
        ],
        "score_used": True,
        "timer_used": True,
        "lives_used": False,
        "hinting_used": False,
        "difficulty_scaling_used": "none",
        "session_end_rule": "Shift ends after 5 incidents. Session ends after one shift.",
        "open_questions": [
            "How does the player distinguish demand numbers from capacity numbers without "
            "verbal explanation? Color coding? Label placement? Icon differentiation?",
            "Should the incident timer be visible as a bar or implicit through incident urgency animation?",
        ],
        "notes": (
            "This prototype covers the primary route_and_dispatch loop only. "
            "The supply mechanic (allocate_and_balance) is explicitly deferred to level 4+."
        ),
    },
    "pizza": {
        "prototype_goal": (
            "Prove that placing a topping at (cos θ, sin θ) on a pizza-circle surface "
            "requires genuine trig computation and that the fail state teaches."
        ),
        "prototype_question": (
            "Can a high school student compute (cos θ, sin θ) and place a topping at "
            "the correct coordinate within 25 seconds, and does the correct-position "
            "reveal on miss function as a worked example?"
        ),
        "player_goal_each_round": (
            "Compute (cos θ, sin θ) for the given angle and drag the topping to that "
            "position on the pizza edge."
        ),
        "first_visible_state": (
            "A unit-circle pizza is displayed with axis lines. An angle θ is shown in "
            "both degrees and radians. A topping item sits at the center, ready to drag."
        ),
        "first_player_action": (
            "Drag the topping from the center toward the computed position on the pizza edge."
        ),
        "success_condition": (
            "The topping is placed within the acceptance zone of the correct (cos θ, sin θ) coordinate."
        ),
        "fail_condition": "The topping is placed outside the acceptance zone.",
        "reset_or_retry_behavior": (
            "On miss, the correct position is revealed for 1.5 seconds as a worked example. "
            "Topping resets to center. The same angle may be retried or the next angle loads."
        ),
        "signature_moment_delivery": (
            "Topping snaps to the exact coordinate with a visual lock. The (cos θ, sin θ) "
            "pair flashes on screen confirming the placement."
        ),
        "input_types": ["drag", "drop"],
        "math_action_mapping": (
            "The drag destination IS the evaluated trig coordinate. Placement accuracy "
            "measures trig computation accuracy directly."
        ),
        "feedback_timing": "immediate",
        "error_handling": (
            "Incorrect placement shows the distance to the correct position and reveals "
            "the correct coordinate for 1.5 seconds as a free worked example."
        ),
        "screens": [
            {
                "screen_id": "pizza_lab",
                "screen_name": "Pizza Lab",
                "purpose": "Deliver the full placement loop in one screen.",
                "elements_present": [
                    "Unit-circle pizza surface with axis lines",
                    "Angle θ display (degrees and radians)",
                    "Draggable topping at center",
                    "Subtle grid or angle markers for reference",
                    "Session progress indicator (e.g., angle 3 of 6)",
                ],
                "player_actions": [
                    "Read the angle θ",
                    "Compute (cos θ, sin θ) mentally or on scratch paper",
                    "Drag topping to the computed position on the pizza edge",
                ],
                "exit_condition": "Topping placed (correct or incorrect). Feedback displayed.",
            },
            {
                "screen_id": "placement_feedback",
                "screen_name": "Placement Feedback",
                "purpose": "Show correct position on miss; confirm on hit. This IS the teaching mechanism.",
                "elements_present": [
                    "Correct position marker (always shown)",
                    "Coordinate pair display (cos θ, sin θ)",
                    "Distance-to-correct indicator (on miss only)",
                ],
                "player_actions": ["Tap to continue to next angle"],
                "exit_condition": "Player taps continue or session ends after final angle.",
            },
        ],
        "ui_components": [
            {"component_name": "unit_circle_pizza", "purpose": "The coordinate space where placement happens — pizza edge IS the unit circle", "required_now": True},
            {"component_name": "angle_display", "purpose": "Shows θ in both degrees and radians", "required_now": True},
            {"component_name": "draggable_topping", "purpose": "The element the player positions at the computed coordinate", "required_now": True},
            {"component_name": "correct_position_reveal", "purpose": "Shows the right answer on miss — the primary teaching mechanism", "required_now": True},
            {"component_name": "coordinate_pair_flash", "purpose": "Confirms the (cos θ, sin θ) values on success", "required_now": True},
            {"component_name": "distance_indicator", "purpose": "Shows how far off the placement was on miss", "required_now": True},
        ],
        "scope_included": [
            "One session of 6 angle placements",
            "Single angle at a time",
            "Q1 canonical angles only (π/6, π/4, π/3, plus select axis-aligned)",
            "Drag topping to computed coordinate on pizza edge",
            "Immediate acceptance zone hit detection",
            "Correct position reveal on miss (1.5 seconds)",
            "Coordinate pair confirmation on hit",
        ],
        "scope_excluded": [
            "Full-circle angles beyond Q1",
            "Radian arc rotation mechanics",
            "Timer pressure",
            "Score or grading system",
            "Account system",
            "Analytics",
            "Final art or audio polish",
        ],
        "scope_deferred": [
            "Q2-Q4 angle expansion",
            "Radian arc rotation (transform_and_manipulate secondary type)",
            "Difficulty progression across sessions",
            "Oven-rotation tasks",
            "Sound design beyond placeholder effects",
        ],
        "sample_targets": [
            "θ = π/6 → (√3/2, 1/2)",
            "θ = π/4 → (√2/2, √2/2)",
            "θ = π/3 → (1/2, √3/2)",
            "θ = 0 → (1, 0)",
            "θ = π/2 → (0, 1)",
            "θ = 5π/6 → (−√3/2, 1/2)",
        ],
        "content_variation": [
            "Mix of axis-aligned and non-axis angles in every session",
            "Every session with an axis-aligned angle must include at least one non-axis angle",
            "Vary angle presentation between degrees and radians across rounds",
        ],
        "must_build_first": [
            "Unit-circle rendering with axis lines and angle markers",
            "Drag-and-drop positioning with coordinate mapping",
            "Acceptance zone hit detection (starting point: 8% of pizza radius)",
            "Correct position reveal animation on miss (1.5-second duration)",
            "Coordinate pair display on success",
        ],
        "can_fake_or_stub": [
            "Pizza art (plain circle with grid lines works)",
            "Topping art (colored dot is sufficient)",
            "Audio (visual-only feedback is sufficient for prototype)",
            "Background and decoration",
        ],
        "known_risks": [
            "Acceptance zone too tight causes repeated failure before skill is built",
            "Acceptance zone too loose lets learners succeed by quadrant guessing",
            "Axis-aligned angles (0, π/2) can be solved by visual anchoring without trig",
            "Fine motor drag imprecision may be confused with mathematical error",
        ],
        "playtest_must_prove": [
            "Student computes (cos θ, sin θ) before dragging, not by trial-and-error",
            "Correct-position reveal on miss functions as a worked example — student improves on subsequent similar angles",
            "Acceptance zone (8% radius) is neither too tight nor too loose for ages 14-18",
            "Students engage with the lab for a full 6-angle session",
        ],
        "success_signals": [
            "Student places topping within acceptance zone on first attempt for non-trivial angles",
            "Student can verbalize the computation ('cos 60° is 0.5, sin 60° is about 0.87')",
            "After a miss, student places the next similar angle correctly — showing the reveal taught them",
            "Student treats the reveal as informative, not discouraging",
        ],
        "failure_signals": [
            "Student drags randomly and relies on the reveal to find positions",
            "Student places correctly only at axis-aligned angles (memorized, not computed)",
            "Student gives up after 3 consecutive misses",
            "Student ignores the coordinate pair flash and does not internalize the feedback",
        ],
        "test_users": [
            "High school students (ages 14-18) currently studying trigonometry",
            "Students who have been introduced to the unit circle but are still building fluency",
            "Math teacher observer",
        ],
        "visual_assets": [
            "Unit-circle pizza surface with axis lines",
            "Angle label display",
            "Topping placeholder (colored dot)",
            "Correct position marker",
            "Coordinate pair overlay",
            "Distance indicator line",
        ],
        "audio_assets": [
            "Placement snap sound placeholder",
            "Miss indicator sound placeholder",
        ],
        "score_used": False,
        "timer_used": False,
        "lives_used": False,
        "hinting_used": False,
        "difficulty_scaling_used": "fixed",
        "session_end_rule": "Session ends after 6 angle placements from the Q1 canonical set.",
        "open_questions": [
            "Acceptance zone calibration: 8% of pizza radius is the starting point — "
            "must be tuned during the first playtesting round.",
            "Should the prototype include a scratch area or allow external computation (paper)?",
            "Should missed angles be retried immediately or queued for later in the session?",
        ],
        "notes": (
            "This prototype intentionally uses lab mode with no timer and no score. "
            "The fail state (correct position reveal) IS the primary teaching mechanism — "
            "it must feel like a free worked example, not a punishment."
        ),
    },
}


# ---------------------------------------------------------------------------
# Generic fallback templates by interaction type
# Used when no concept-specific override matches the world theme.
# ---------------------------------------------------------------------------

GENERIC_TEMPLATES: Dict[str, Dict[str, Any]] = {
    "combine_and_build": {
        "prototype_goal": "Prove that the combine-and-build loop is immediately understandable and that the math action is engaging enough to sustain repeated play without instruction.",
        "prototype_question": "Can a learner reach the correct total through the intended combining action without extra instruction?",
        "player_goal_each_round": "Select components whose values sum to the target number.",
        "first_visible_state": "A target number is displayed. Below it, a tray of selectable components with numeric labels.",
        "first_player_action": "Tap a component to add it to the assembly area.",
        "success_condition": "The running total equals the target number exactly.",
        "fail_condition": "The running total exceeds the target.",
        "reset_or_retry_behavior": "Last component bounces back. Running total returns to previous value.",
        "signature_moment_delivery": "Assembly area confirms completion the instant the total matches the target.",
        "input_types": ["tap"],
        "math_action_mapping": "Each tap adds one component value to the running total. Building IS adding.",
        "feedback_timing": "immediate",
        "error_handling": "Overshoot causes the last item to bounce back, preserving prior correct total.",
    },
    "route_and_dispatch": {
        "prototype_goal": "Prove that the routing decision is driven by arithmetic comparison, not guessing.",
        "prototype_question": "Can a learner identify the correct option by comparing numbers and route it correctly?",
        "player_goal_each_round": "Read the demand, compare options, and select the matching one.",
        "first_visible_state": "A demand card appears. Two or more options with numeric labels are visible.",
        "first_player_action": "Tap the option whose label matches the demand.",
        "success_condition": "The selected option matches the demand exactly.",
        "fail_condition": "The wrong option is selected or time expires.",
        "reset_or_retry_behavior": "Wrong option shakes and returns. Demand persists for retry.",
        "signature_moment_delivery": "Correct option animates toward the demand. Card clears.",
        "input_types": ["tap"],
        "math_action_mapping": "Option selection requires comparing numbers — the routing decision IS the comparison.",
        "feedback_timing": "immediate",
        "error_handling": "Incorrect selection triggers shake feedback. Item returns. Demand persists.",
    },
    "navigate_and_position": {
        "prototype_goal": "Prove that positioning requires genuine mathematical computation, not visual guessing.",
        "prototype_question": "Can a learner compute the target position and place the element correctly?",
        "player_goal_each_round": "Compute the target coordinate and drag the element to that position.",
        "first_visible_state": "A coordinate space is displayed. A target parameter is shown. A draggable element sits at the origin.",
        "first_player_action": "Drag the element toward the computed position.",
        "success_condition": "The element is placed within the acceptance zone of the correct coordinate.",
        "fail_condition": "The element is placed outside the acceptance zone.",
        "reset_or_retry_behavior": "On miss, the correct position is revealed briefly. Element resets.",
        "signature_moment_delivery": "Element snaps to exact coordinate with confirmation display.",
        "input_types": ["drag", "drop"],
        "math_action_mapping": "The drag destination IS the mathematical result. Placement accuracy measures computation accuracy.",
        "feedback_timing": "immediate",
        "error_handling": "Incorrect placement reveals the correct position as a worked example.",
    },
    "allocate_and_balance": {
        "prototype_goal": "Prove that the allocation loop requires constraint-based math reasoning, not even splitting.",
        "prototype_question": "Can a learner distribute a total correctly according to labeled constraints?",
        "player_goal_each_round": "Assign quantities to slots so that each slot's constraint is met and the total is exhausted.",
        "first_visible_state": "A total quantity is shown. Slots with labeled constraints are visible.",
        "first_player_action": "Assign a value to the first slot.",
        "success_condition": "All slots are filled correctly and the total is exhausted with zero remainder.",
        "fail_condition": "A slot overflows or the total cannot be distributed to remaining slots.",
        "reset_or_retry_behavior": "Overflowed slot resets. Learner may reassign.",
        "signature_moment_delivery": "Last slot fills exactly — balance indicator snaps to zero remainder.",
        "input_types": ["tap", "type"],
        "math_action_mapping": "Each allocation is an arithmetic operation against the constraint. Distributing IS the math.",
        "feedback_timing": "immediate",
        "error_handling": "Overflow triggers visual effect. Slot resets. Learner reassigns.",
    },
    "transform_and_manipulate": {
        "prototype_goal": "Prove that the transformation gesture requires mathematical reasoning about the property being changed.",
        "prototype_question": "Can a learner apply the correct transformation to match the target state?",
        "player_goal_each_round": "Transform the object so its mathematical property matches the target.",
        "first_visible_state": "An object with a visible mathematical property. A target state is shown.",
        "first_player_action": "Apply a transformation gesture (rotation, scaling, flip).",
        "success_condition": "The object's mathematical property matches the target after transformation.",
        "fail_condition": "The transformation leaves a visible gap between object and target.",
        "reset_or_retry_behavior": "Object resets to starting state for retry.",
        "signature_moment_delivery": "Object locks into the target state with a snap and confirmation overlay.",
        "input_types": ["drag", "tap"],
        "math_action_mapping": "The transformation gesture IS the mathematical operation.",
        "feedback_timing": "immediate",
        "error_handling": "Overshoot triggers reset. Learner re-starts from the initial state.",
    },
    "sequence_and_predict": {
        "prototype_goal": "Prove that the sequence completion requires discovering and applying a mathematical rule.",
        "prototype_question": "Can a learner identify the pattern rule and predict the next element?",
        "player_goal_each_round": "Place the correct value in the gap to continue the mathematical pattern.",
        "first_visible_state": "A partial sequence with visible elements and one gap.",
        "first_player_action": "Place a value in the gap.",
        "success_condition": "The placed value correctly continues the mathematical pattern.",
        "fail_condition": "The placed value does not match the pattern rule.",
        "reset_or_retry_behavior": "Incorrect value is removed. Gap reopens.",
        "signature_moment_delivery": "Gap fills and pattern-reveal effect shows the rule visually.",
        "input_types": ["tap", "type"],
        "math_action_mapping": "Gap completion requires computing the next value from the rule. Predicting IS the math.",
        "feedback_timing": "immediate",
        "error_handling": "Incorrect value shakes and is removed. Gap reopens for retry.",
    },
}


def _default_screens(interaction_type: str) -> List[Dict[str, Any]]:
    """Generate generic two-screen flow for any interaction type."""
    return [
        {
            "screen_id": "play",
            "screen_name": "Play Screen",
            "purpose": f"Core {interaction_type.replace('_', ' ')} loop.",
            "elements_present": ["Primary game elements", "Feedback display", "Progress indicator"],
            "player_actions": ["Perform the primary interaction"],
            "exit_condition": "Round success or failure.",
        },
        {
            "screen_id": "result",
            "screen_name": "Round Result",
            "purpose": "Show outcome and transition.",
            "elements_present": ["Success or fail indicator", "Next round prompt"],
            "player_actions": ["Tap to continue"],
            "exit_condition": "Player continues or session ends.",
        },
    ]


def _default_ui_components() -> List[Dict[str, Any]]:
    """Generate generic UI components."""
    return [
        {"component_name": "primary_game_element", "purpose": "The main interactive element", "required_now": True},
        {"component_name": "target_display", "purpose": "Shows what the player must achieve", "required_now": True},
        {"component_name": "feedback_display", "purpose": "Communicates success or failure", "required_now": True},
    ]


def prototype_spec_stub(context: Dict[str, Any]) -> Dict[str, Any]:
    intake = context["artifact_inputs"]["intake_brief"]
    memo = context["artifact_inputs"]["interaction_decision_memo"]
    family = context["artifact_inputs"]["family_architecture_brief"]
    loop = context["artifact_inputs"]["lowest_viable_loop_brief"]

    primary_interaction = memo.get("primary_interaction_type", "combine_and_build")
    world_theme = intake.get("possible_world_theme", "unknown")
    profession = intake.get("possible_profession_or_mission", "unknown")
    family_name = family.get("family_name", "unnamed family")
    math_domain = intake.get("likely_math_domain", "unknown")
    age_band = intake.get("likely_age_band", "unknown")
    grade_band = intake.get("likely_grade_band", "unknown")
    target_skills = intake.get("likely_target_skills", ["unknown"]) or ["unknown"]

    # --- Select best template: concept-specific override > generic ---
    concept_key = None
    theme_lower = world_theme.lower()
    for key in CONCEPT_OVERRIDES:
        if key in theme_lower:
            concept_key = key
            break

    if concept_key:
        t = CONCEPT_OVERRIDES[concept_key]
    else:
        t = GENERIC_TEMPLATES.get(primary_interaction, GENERIC_TEMPLATES["combine_and_build"])

    # --- concept_fidelity_check ---
    memo_interaction = memo.get("primary_interaction_type", "")
    loop_map = loop.get("core_loop_map", {})
    fidelity_ok = bool(
        memo_interaction == primary_interaction
        and family_name
        and family_name != "unnamed family"
        and loop_map.get("first_correct_action")
    )

    # --- Enrich target_skills from intake if available ---
    enriched_skills = target_skills
    if math_domain == "addition" and target_skills == ["addition"]:
        enriched_skills = ["addition_to_20", "counting_on", "number_bonds_to_20"]
    elif math_domain == "arithmetic" and target_skills == ["arithmetic"]:
        enriched_skills = ["arithmetic_comparison", "number_magnitude"]
    elif math_domain == "trigonometry" and target_skills == ["trigonometry"]:
        enriched_skills = ["unit_circle_coordinates", "radian_angle_evaluation", "sine_cosine_computation"]

    # --- Build sample targets if not in template ---
    sample_targets = t.get("sample_targets")
    if not sample_targets:
        if math_domain == "addition":
            sample_targets = ["target 6", "target 7", "target 10", "target 13", "target 18"]
        elif math_domain == "arithmetic":
            sample_targets = ["Demand 12, options [12, 8]", "Demand 15, options [15, 20]"]
        elif math_domain == "trigonometry":
            sample_targets = ["θ = π/6 → (√3/2, 1/2)", "θ = π/4 → (√2/2, √2/2)"]
        else:
            sample_targets = [f"Sample {math_domain} problem {i+1}" for i in range(5)]

    content_variation = t.get("content_variation", [
        f"Vary values within the {math_domain} domain",
        "Randomize element order each round",
    ])

    # --- Screens, UI, assets ---
    screens = t.get("screens", _default_screens(primary_interaction))
    ui_components = t.get("ui_components", _default_ui_components())

    visual_assets = t.get("visual_assets", [
        f"Placeholder {world_theme} background",
        f"Interactive element placeholder for {math_domain} domain",
        "Feedback indicator icons",
    ])
    audio_assets = t.get("audio_assets", [
        "Success sound placeholder",
        "Error sound placeholder",
    ])

    # --- Scope ---
    scope_included = t.get("scope_included", [
        "Core loop: one math action, one feedback cycle, one retry path",
        f"Primary interaction: {primary_interaction.replace('_', ' ')}",
        "Minimal session structure",
        "Success and failure feedback",
    ])
    scope_excluded = t.get("scope_excluded", [
        "Progression systems, leveling, or unlocks",
        "Tutorial or onboarding sequences",
        "Account systems or persistent state",
        "Analytics or telemetry",
        "Final art or audio",
    ])
    scope_deferred = t.get("scope_deferred", [
        "Difficulty scaling beyond the prototype scope",
        "Secondary interaction mechanics",
        "Content breadth (full problem set)",
    ])

    # --- Build notes ---
    must_build_first = t.get("must_build_first", [
        "Core interaction logic",
        "Success and failure detection",
        "Basic feedback display",
        "Round transition",
    ])
    can_fake = t.get("can_fake_or_stub", [
        "Final art (placeholders sufficient)",
        "Audio (visual-only feedback sufficient)",
        "Advanced content variety",
    ])
    known_risks = t.get("known_risks", [
        "Prototype may feel too simple if content variety is too low",
    ])

    # --- Open questions ---
    open_questions = t.get("open_questions", [])

    # --- Notes ---
    notes = t.get("notes", (
        f"Prototype spec for '{primary_interaction}' interaction in "
        f"'{math_domain}' domain. World theme: {world_theme}. "
        f"Family: {family_name}."
    ))

    # --- Status and readiness ---
    # Concept overrides are implementation-ready (0.92); generic fallbacks are
    # structurally valid but lack domain-specific detail (0.75).
    if not fidelity_ok:
        readiness = 0.5
        status = "reject"
    elif concept_key:
        readiness = 0.92
        status = "pass"
    else:
        readiness = 0.75
        status = "pass"

    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    return {
        "status": status,
        "timestamp": timestamp,
        "prototype_goal": t.get("prototype_goal", "Prove the core loop is understandable and engaging."),
        "prototype_question": t.get("prototype_question", "Can a learner complete the core action without extra instruction?"),
        "target_player": {
            "age_band": age_band,
            "grade_band": grade_band,
            "math_domain": math_domain,
            "target_skills": enriched_skills,
        },
        "concept_anchor": {
            "world_theme": world_theme,
            "profession_or_mission": profession,
            "primary_interaction_type": primary_interaction,
            "family_name": family_name,
        },
        "concept_fidelity_check": {
            "v1_interaction_type_preserved": memo_interaction == primary_interaction,
            "v1_family_boundary_respected": bool(family_name and family_name != "unnamed family"),
            "v1_loop_structure_preserved": bool(loop_map.get("first_correct_action")),
            "fidelity_notes": (
                "All V1 design decisions preserved in prototype translation."
                if fidelity_ok
                else "Fidelity gap detected — one or more V1 constraints could not be verified."
            ),
        },
        "prototype_scope": {
            "included": scope_included,
            "excluded": scope_excluded,
            "deferred": scope_deferred,
        },
        "core_loop_translation": {
            "player_goal_each_round": t.get("player_goal_each_round", "Complete the core math action."),
            "first_visible_state": t.get("first_visible_state", "The game element and target are displayed."),
            "first_player_action": t.get("first_player_action", "Interact with the primary element."),
            "success_condition": t.get("success_condition", "The math action is completed correctly."),
            "fail_condition": t.get("fail_condition", "The math action is completed incorrectly."),
            "reset_or_retry_behavior": t.get("reset_or_retry_behavior", "Element resets for retry."),
            "signature_moment_delivery": t.get("signature_moment_delivery", "Confirmation animation plays."),
        },
        "screen_flow": screens,
        "interaction_model": {
            "input_types": t.get("input_types", ["tap"]),
            "math_action_mapping": t.get("math_action_mapping", "The player action IS the math operation."),
            "feedback_timing": t.get("feedback_timing", "immediate"),
            "error_handling": t.get("error_handling", "Error feedback is shown and element resets."),
        },
        "ui_components_required": ui_components,
        "content_requirements": {
            "minimum_round_count": 5,
            "sample_prompts_or_targets": sample_targets,
            "content_variation_needed": content_variation,
        },
        "prototype_rules": {
            "score_used": t.get("score_used", False),
            "timer_used": t.get("timer_used", False),
            "lives_used": t.get("lives_used", False),
            "hinting_used": t.get("hinting_used", False),
            "difficulty_scaling_used": t.get("difficulty_scaling_used", "none"),
            "session_end_rule": t.get("session_end_rule", "Session ends after 5 rounds."),
        },
        "asset_requirements": {
            "visual_assets_needed": visual_assets,
            "audio_assets_needed": audio_assets,
            "placeholder_allowed": True,
        },
        "technical_build_notes": {
            "must_build_first": must_build_first,
            "can_fake_or_stub": can_fake,
            "known_risks": known_risks,
        },
        "playtest_plan": {
            "what_this_prototype_must_prove": t.get("playtest_must_prove", [
                "The core loop is understandable without instruction",
                "The math action is embedded in the interaction",
            ]),
            "success_signals": t.get("success_signals", [
                "Learner completes the action correctly on first or second attempt",
                "Learner engages for a full session",
            ]),
            "failure_signals": t.get("failure_signals", [
                "Learner does not understand what to do",
                "Learner disengages before completing the session",
            ]),
            "recommended_test_users": t.get("test_users", [
                "Learners in the target age band",
                "Teacher or parent observer",
            ]),
        },
        "prototype_readiness_score": readiness,
        "open_questions": open_questions,
        "notes": notes,
    }


def build_spec(repo_root: Path) -> AgentSpec:
    return AgentSpec(
        agent_name="prototype_spec_agent",
        expected_output_artifact="prototype_spec",
        expected_produced_by="Prototype Spec Agent",
        prompt_path=repo_root / "agents" / "prototype_spec" / "prompt.md",
        config_path=repo_root / "agents" / "prototype_spec" / "config.yaml",
        allowed_reads=[
            "intake_brief",
            "interaction_decision_memo",
            "family_architecture_brief",
            "lowest_viable_loop_brief",
        ],
        allowed_writes=["prototype_spec"],
        max_revision_count=2,
    )


def run(
    repo_root: Path,
    job_id: str,
    artifact_paths: Dict[str, Path],
    model_callable=None,
):
    """Run the Prototype Spec Agent.

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
        model_callable=model_callable if model_callable is not None else prototype_spec_stub,
    )
