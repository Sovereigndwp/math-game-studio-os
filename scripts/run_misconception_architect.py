#!/usr/bin/env python3
"""
Run the Misconception Architect stub against an existing game using
synthetic pipeline briefs that reflect the real game's design.

Usage:
    python scripts/run_misconception_architect.py [--game bakery-rush|fire-dispatch|unit-circle]

Writes the output artifact to:
    memory/job_workspaces/<job_id>/misconception_map_v1.json

Also copies a timestamped snapshot to:
    artifacts/jobs/<job_id>/misconception_map_v1.json
"""
from __future__ import annotations

import argparse
import json
import shutil
import sys
import tempfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from agents.misconception_architect.agent import run as run_agent  # noqa: E402


# ---------------------------------------------------------------------------
# Synthetic brief factories
# Each factory produces the minimal valid structure for the three input
# artifacts needed by the Misconception Architect, based on the real game.
# ---------------------------------------------------------------------------

def _bakery_rush_briefs() -> dict:
    loop_brief = {
        "job_id": "bakery-rush-pass2",
        "artifact_name": "lowest_viable_loop_brief",
        "version": 2,
        "produced_by": "Core Loop Agent",
        "timestamp": "2026-04-04T00:00:00Z",
        "status": "pass",
        "first_60_seconds_flow": (
            "Player sees a conveyor belt with pastries moving left to right. "
            "An order ticket appears in the top-right corner showing a target number. "
            "Player taps pastries on the belt; each has a +N label. "
            "Running total is shown in a box above. When total equals the target the order ships. "
            "If player exceeds the target, the last item slips back automatically. "
            "Patience bar drains if player doesn't act. "
        ),
        "lowest_viable_loop_description": (
            "Tap pastries whose +N values sum to the target number shown on the order ticket. "
            "Belt moves at increasing speed across five levels."
        ),
        "core_loop_map": {
            "what_appears_first": "Conveyor belt with 4 pastry types, each labeled +1/+2/+3/+4.",
            "what_the_learner_notices": "A target number (order) and a running total counter.",
            "what_the_learner_does_first": "Taps a pastry; sees the running total increment by the pastry value.",
            "first_correct_action": "Selects pastries whose +N values sum exactly to the order target.",
            "immediate_feedback": "Order ships with celebration animation; stars awarded.",
            "what_repeats_next": "New order appears; belt continues at same or faster speed.",
        },
        "signature_moment": (
            "Player approaches the exact target with one item left to choose — "
            "they need +3 and a +3 pastry is approaching on the belt."
        ),
        "fail_state_structure": (
            "Overshoot: last item slips back, running total decrements. "
            "Patience expiry: order fails, life lost."
        ),
        "max_steps_per_loop": 6,
        "max_simultaneous_elements": 4,
        "expected_time_to_first_correct_action_seconds": 3,
        "expected_confusion_risks": [
            "Belt speed triggers tap-before-thinking at early levels",
            "Running total not tracked — learner loses count near target",
            "Pastry icon selected by preference rather than +N label",
            "Target number confused with item count rather than sum",
            "Overshoot auto-correct mechanic misread as failure",
            "Combined belt + arithmetic pressure causes strategic freeze at L3+",
        ],
        "teacher_shortcut_version": (
            "Check the session diagnostic on the end screen: "
            "if most failures are timeouts, belt speed is the issue. "
            "If overshoots dominate, choice errors or counting breaks are the issue."
        ),
        "micro_prototype_recommendation": (
            "Static belt with single +1 and +2 item; target = 3. "
            "Confirms core loop before any belt movement is introduced."
        ),
        "notes": "Pass 2 ramp: [18s, 13s, 9s, 6s, 4s]. Reflection beat not yet implemented.",
    }

    family_brief = {
        "job_id": "bakery-rush-pass2",
        "artifact_name": "family_architecture_brief",
        "version": 1,
        "produced_by": "Family Architect Agent",
        "timestamp": "2026-04-04T00:00:00Z",
        "status": "pass",
        "family_name": "Bakery Rush",
        "factory_type": "universal_ladder",
        "is_existing_family": True,
        "existing_family_match_confidence": 1.0,
        "reason_for_family_placement": (
            "Bakery Rush is the anchor title for the combine_and_build family. "
            "Running total toward a target with value-weighted items."
        ),
        "family_growth_path": (
            "L1: targets ≤ 5, +1/+2 items only. "
            "L5: targets ≤ 20, all four pastry types, belt at full speed. "
            "Future: subtraction items (slips remove value) as a separate pass."
        ),
        "family_boundary_rule": "Any concept requiring accumulation of weighted values to reach a target.",
        "boundary_break_example": "A game requiring sorting items into categories — that is route_and_dispatch, not combine_and_build.",
        "reuse_recommendation": "extend_existing",
        "family_overlap_warnings": [
            "Allocate-and-balance overlap if two target boxes are introduced — would require redesign."
        ],
        "notes": "Loop Purity Score: 0.90 (PURE). Reflection beat is the one remaining gap.",
    }

    interaction_memo = {
        "job_id": "bakery-rush-pass2",
        "artifact_name": "interaction_decision_memo",
        "version": 1,
        "produced_by": "Interaction Mapper Agent",
        "timestamp": "2026-04-04T00:00:00Z",
        "status": "pass",
        "primary_interaction_type": "combine_and_build",
        "secondary_interaction_type": None,
        "interaction_justification": (
            "Player accumulates pastry values (weights) toward a target sum. "
            "Running total always visible. Exact match required."
        ),
        "rejected_alternatives": [
            "route_and_dispatch — no sorting; all pastries go to same destination"
        ],
        "interaction_purity_score": 0.90,
        "is_action_itself_the_math": True,
        "interaction_overload_warning": False,
        "split_family_warning": False,
        "notes": "clean combine_and_build. No secondary interaction introduced.",
    }

    return {
        "job_id": "bakery-rush-pass2",
        "loop_brief": loop_brief,
        "family_brief": family_brief,
        "interaction_memo": interaction_memo,
    }


def _fire_dispatch_briefs() -> dict:
    loop_brief = {
        "job_id": "fire-dispatch-pass1",
        "artifact_name": "lowest_viable_loop_brief",
        "version": 1,
        "produced_by": "Core Loop Agent",
        "timestamp": "2026-04-04T00:00:00Z",
        "status": "pass",
        "first_60_seconds_flow": (
            "A fire appears with a severity number. Pool of fire trucks displayed, "
            "each with a capacity value. Player selects one or more trucks whose combined "
            "capacity meets or equals fire severity. Timer ticks."
        ),
        "lowest_viable_loop_description": (
            "Select the subset of fire trucks whose combined water capacity "
            "exactly meets the fire demand."
        ),
        "core_loop_map": {
            "what_appears_first": "Fire with demand number. Pool of trucks with capacity labels.",
            "what_the_learner_notices": "Each truck has a different water capacity value.",
            "what_the_learner_does_first": "Taps a truck; sees it join the dispatch queue.",
            "first_correct_action": "Selects truck(s) whose capacity sums to fire demand.",
            "immediate_feedback": "Fire extinguished with animation; stars awarded.",
            "what_repeats_next": "New fire appears; truck pool refreshes.",
        },
        "signature_moment": "Two trucks with capacities 3 and 5 selected to match a demand of 8.",
        "fail_state_structure": (
            "Under-capacity dispatch: fire not extinguished. "
            "Timer expiry: fire spreads, life lost."
        ),
        "max_steps_per_loop": 4,
        "max_simultaneous_elements": 6,
        "expected_time_to_first_correct_action_seconds": 4,
        "expected_confusion_risks": [
            "Sends all trucks without checking combined capacity",
            "Reads truck count as capacity rather than the labeled value",
            "Capacity icon not clearly read — defaults to largest truck icon",
            "Arithmetic slip in adding two capacity values under time pressure",
            "Believes used trucks can be reused in same round",
            "Fails on multi-constraint orders (capacity + type restriction)",
        ],
        "teacher_shortcut_version": (
            "Session shows which fire demands produced the most failures. "
            "Demand at which arithmetic slips dominate indicates working memory limit."
        ),
        "micro_prototype_recommendation": (
            "One fire (demand 4). Two trucks: capacity 4 and capacity 2. "
            "Player must select the capacity-4 truck."
        ),
        "notes": "Loop Purity Score: 0.62 (ADVISORY). Reflection beat and teacher evidence both missing.",
    }

    family_brief = {
        "job_id": "fire-dispatch-pass1",
        "artifact_name": "family_architecture_brief",
        "version": 1,
        "produced_by": "Family Architect Agent",
        "timestamp": "2026-04-04T00:00:00Z",
        "status": "pass",
        "family_name": "Fire Dispatch",
        "factory_type": "age_band_specialist",
        "is_existing_family": True,
        "existing_family_match_confidence": 1.0,
        "reason_for_family_placement": "Fire Dispatch is the anchor title for route_and_dispatch.",
        "family_growth_path": "Add multi-attribute constraints progressively. Introduce truck type + capacity.",
        "family_boundary_rule": "Subset selection from a fixed pool where items are single-use per round.",
        "boundary_break_example": "A game requiring accumulation — that is combine_and_build.",
        "reuse_recommendation": "extend_existing",
        "family_overlap_warnings": ["combine_and_build overlap if trucks can be stacked without routing."],
        "notes": "Loop Purity 0.62 ADVISORY. Math-as-core-action check failed — needs redesign.",
    }

    interaction_memo = {
        "job_id": "fire-dispatch-pass1",
        "artifact_name": "interaction_decision_memo",
        "version": 1,
        "produced_by": "Interaction Mapper Agent",
        "timestamp": "2026-04-04T00:00:00Z",
        "status": "pass",
        "primary_interaction_type": "route_and_dispatch",
        "secondary_interaction_type": None,
        "interaction_justification": "Player selects from a fixed truck pool; trucks are single-use per round.",
        "rejected_alternatives": ["combine_and_build — trucks don't accumulate; they match a demand"],
        "interaction_purity_score": 0.62,
        "is_action_itself_the_math": False,
        "interaction_overload_warning": False,
        "split_family_warning": False,
        "notes": "is_action_itself_the_math False — routing action needs stronger mathematical framing.",
    }

    return {
        "job_id": "fire-dispatch-pass1",
        "loop_brief": loop_brief,
        "family_brief": family_brief,
        "interaction_memo": interaction_memo,
    }


def _unit_circle_briefs() -> dict:
    loop_brief = {
        "job_id": "unit-circle-pass1",
        "artifact_name": "lowest_viable_loop_brief",
        "version": 1,
        "produced_by": "Core Loop Agent",
        "timestamp": "2026-04-04T00:00:00Z",
        "status": "pass",
        "first_60_seconds_flow": (
            "A unit circle is shown. An angle is given (degrees or radians). "
            "Player places a dot on the circle at the correct angular position. "
            "Tolerance ring shows how precise the placement must be."
        ),
        "lowest_viable_loop_description": (
            "Place a point on the unit circle at the correct angle, "
            "converting between degrees and radians."
        ),
        "core_loop_map": {
            "what_appears_first": "Unit circle with axis labels. Angle prompt (e.g. 'Place at 3π/4').",
            "what_the_learner_notices": "Quadrant markers and reference angles on the circle.",
            "what_the_learner_does_first": "Taps or drags to a position on the circle arc.",
            "first_correct_action": "Places the dot within the tolerance zone at the correct angle.",
            "immediate_feedback": "Dot snaps and glows green; coordinates shown.",
            "what_repeats_next": "New angle prompt; different representation (degrees vs radians alternated).",
        },
        "signature_moment": "Player identifies π/2 and 90° as the same position without prompting.",
        "fail_state_structure": (
            "Placement outside tolerance ring: red flash, prompt to try again. "
            "Three failed attempts: correct position revealed."
        ),
        "max_steps_per_loop": 3,
        "max_simultaneous_elements": 2,
        "expected_time_to_first_correct_action_seconds": 5,
        "expected_confusion_risks": [
            "Places at 90° when radian prompt given (units confusion)",
            "Clockwise instead of counter-clockwise rotation",
            "Correct quadrant but wrong axis (swaps x and y)",
            "Near-miss within tolerance at quadrant boundaries",
            "Cannot connect radian fraction to circle position",
            "Quadrant determination correct but angle magnitude wrong under combined pressure",
        ],
        "teacher_shortcut_version": (
            "Placement error direction reveals the confusion type: "
            "mirror image = clockwise confusion; correct quadrant wrong magnitude = radian conversion gap."
        ),
        "micro_prototype_recommendation": (
            "One angle: 90° (also shown as π/2). "
            "Player places on top of circle. Confirms both representations name same position."
        ),
        "notes": "Loop Purity Score: 0.36 (COMPROMISED) — likely false negative from keyword check. Geometric math is structurally core.",
    }

    family_brief = {
        "job_id": "unit-circle-pass1",
        "artifact_name": "family_architecture_brief",
        "version": 1,
        "produced_by": "Family Architect Agent",
        "timestamp": "2026-04-04T00:00:00Z",
        "status": "pass",
        "family_name": "Unit Circle",
        "factory_type": "advanced_anchor",
        "is_existing_family": True,
        "existing_family_match_confidence": 1.0,
        "reason_for_family_placement": "Unit Circle is the anchor title for navigate_and_position.",
        "family_growth_path": "Add coordinates (x, y) at placed angle. Then introduce sin/cos as outputs.",
        "family_boundary_rule": "Player places or moves to a precise spatial/angular position.",
        "boundary_break_example": "A game where the player identifies a category — that is route_and_dispatch.",
        "reuse_recommendation": "extend_existing",
        "family_overlap_warnings": ["transform_and_manipulate overlap if angle transformations become the core action."],
        "notes": "Auditor false-negative likely. Geometric math is structurally pure. Fix MATH_KEYWORDS regex.",
    }

    interaction_memo = {
        "job_id": "unit-circle-pass1",
        "artifact_name": "interaction_decision_memo",
        "version": 1,
        "produced_by": "Interaction Mapper Agent",
        "timestamp": "2026-04-04T00:00:00Z",
        "status": "pass",
        "primary_interaction_type": "navigate_and_position",
        "secondary_interaction_type": None,
        "interaction_justification": "Player places a point at a precise angular position on the unit circle. Precision is the game mechanic.",
        "rejected_alternatives": ["route_and_dispatch — no pool selection; placement is a continuous spatial action"],
        "interaction_purity_score": 0.36,
        "is_action_itself_the_math": True,
        "interaction_overload_warning": False,
        "split_family_warning": False,
        "notes": "Purity score is a known false negative. Geometric language not in auditor keyword list.",
    }

    return {
        "job_id": "unit-circle-pass1",
        "loop_brief": loop_brief,
        "family_brief": family_brief,
        "interaction_memo": interaction_memo,
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def _bakery_rush_changed_brief() -> dict:
    """Bakery Rush with a changed brief: subtraction items introduced, belt speed
    is no longer a primary concern (adaptive speed added), and a new
    'negative-value confusion' risk replaces the old impulsive-tap-from-speed risk.
    This simulates a pass-3 redesign where the game has evolved."""
    base = _bakery_rush_briefs()
    base["job_id"] = "bakery-rush-pass3-changed"

    # Modify the loop brief to reflect changed game design
    base["loop_brief"]["version"] = 3
    base["loop_brief"]["first_60_seconds_flow"] = (
        "Player sees a conveyor belt with pastries moving left to right. "
        "An order ticket appears showing a target number. "
        "Player taps pastries on the belt; each has a +N or −N label. "
        "Running total is shown above. Subtraction items (−N) remove value from the box. "
        "Belt speed adapts to player performance (no longer a fixed ramp). "
        "When total equals the target the order ships. "
        "If player exceeds the target, the last item slips back automatically. "
    )
    base["loop_brief"]["expected_confusion_risks"] = [
        # REMOVED: "Belt speed triggers tap-before-thinking" — adaptive speed mitigates this
        # KEPT (same wording): running total loss
        "Running total not tracked — learner loses count near target",
        # CHANGED: icon preference risk now also involves negative items
        "Pastry icon selected by preference; negative-value pastries (−N) avoided even when needed",
        # KEPT (same wording): count vs sum confusion
        "Target number confused with item count rather than sum",
        # KEPT: overshoot mechanic
        "Overshoot auto-correct mechanic misread as failure",
        # CHANGED: strategic overload now involves subtraction decisions, not belt speed
        "Subtraction items create strategic paralysis — learner avoids all −N items or uses them randomly",
        # NEW: no prior library entry covers this
        "Learner adds a −N item expecting it to add positively (sign confusion)",
    ]
    base["loop_brief"]["notes"] = (
        "Pass 3: adaptive belt speed, subtraction items introduced. "
        "Reflection beat still not implemented."
    )
    return base


def _fire_dispatch_changed_brief() -> dict:
    """Fire Dispatch with a changed brief: helicopters added as a second resource
    type with different reach rules, and a cooldown mechanic replaces the
    single-use-per-round rule. This simulates a pass-2 redesign."""
    base = _fire_dispatch_briefs()
    base["job_id"] = "fire-dispatch-pass2-changed"

    base["loop_brief"]["version"] = 2
    base["loop_brief"]["first_60_seconds_flow"] = (
        "A fire appears with a severity number and a terrain tag (urban/forest). "
        "Pool of fire trucks AND helicopters displayed, each with a capacity value. "
        "Trucks work in urban, helicopters work in forest, both work on mixed. "
        "Player selects resources whose combined capacity meets severity. "
        "Used resources enter a 2-round cooldown instead of being removed. "
        "Timer ticks."
    )
    base["loop_brief"]["expected_confusion_risks"] = [
        # KEPT (same): impulsive dispatch
        "Sends all resources without checking combined capacity",
        # CHANGED: now two resource types — confusion about terrain matching
        "Dispatches truck to forest fire or helicopter to urban fire, ignoring terrain restriction",
        # KEPT (similar): icon confusion but now with two resource types
        "Cannot distinguish truck capacity label from helicopter capacity label",
        # CHANGED: arithmetic now involves mixed resource types
        "Arithmetic slip when adding truck + helicopter capacity values under time pressure",
        # CHANGED: cooldown replaces single-use rule
        "Does not understand cooldown — tries to select grayed-out resource or waits for wrong resource to return",
        # KEPT (similar): multi-constraint overload
        "Cannot track terrain + capacity + cooldown simultaneously",
    ]
    base["loop_brief"]["fail_state_structure"] = (
        "Under-capacity dispatch: fire not extinguished. "
        "Wrong terrain: resource cannot reach fire, wasted dispatch. "
        "Timer expiry: fire spreads, life lost."
    )
    base["loop_brief"]["notes"] = (
        "Pass 2: helicopters added, cooldown replaces single-use. "
        "Terrain matching is the new constraint axis."
    )
    return base


GAME_FACTORIES = {
    "bakery-rush": _bakery_rush_briefs,
    "bakery-rush-changed": _bakery_rush_changed_brief,
    "fire-dispatch": _fire_dispatch_briefs,
    "fire-dispatch-changed": _fire_dispatch_changed_brief,
    "unit-circle": _unit_circle_briefs,
}


def _make_mock_targeted_llm():
    """Return a mock targeted LLM that produces realistic responses for
    the Bakery Rush changed-brief scenario. Used for testing the full
    diff-and-extend + LLM pathway without an API key."""

    _MOCK_RESPONSES = {
        # Revise: representation_mismatch — negative-value pastries
        "representation_mismatch": json.dumps({
            "id": "bakery_emoji_not_value",
            "category": "representation_mismatch",
            "label": "Picks by pastry type, avoids negative items",
            "description": (
                "Learner selects items based on pastry emoji preference or visual "
                "salience rather than the +N/−N numeric value label. Additionally, "
                "learner systematically avoids −N items even when subtracting would "
                "reach the target more efficiently, treating negative values as "
                "'bad' items rather than useful arithmetic tools."
            ),
            "likely_cause": (
                "The emoji is visually larger and more salient than the +N/−N label. "
                "Negative values carry an affective 'loss' connotation from everyday "
                "experience. Without explicit framing, learners treat subtraction "
                "items as penalties to avoid rather than strategic tools."
            ),
            "how_it_appears_in_play": (
                "Consistent selection of one emoji type regardless of value. "
                "−N items are never tapped even when they would complete the order. "
                "Player waits for a positive item to appear rather than using an "
                "available −N item. Overshoot rate remains high on orders where "
                "−N items would have corrected the total."
            ),
            "detection_signal": (
                "Player selects the same emoji type >= 70% of the time across 3+ orders. "
                "−N items are tapped < 10% of the time across a session even when "
                "they appear on >= 50% of belt cycles. Orders where −N would have "
                "completed the target end in overshoot or timeout instead."
            ),
            "best_feedback_response": (
                "Every pastry has a number — positive adds, negative takes away. "
                "You need 2 more, and there is a −1 pastry on the belt. "
                "If you used it, your total would go from 6 to 5. Would that help?"
            ),
            "best_clean_replay_task": (
                "All items same emoji. Mix of +N and −N labels. Target = 5. "
                "Only reachable path requires using at least one −N item "
                "(e.g., +4, +3, −2 to reach 5). Timer removed."
            ),
            "reflection_prompt": (
                "Did you use any of the minus pastries? What would have happened "
                "to your total if you had tapped the −1?"
            ),
            "change_rationale": (
                "Revised from library: original entry covered icon preference for "
                "positive items only. Brief now includes negative-value pastries (−N) "
                "that learners avoid even when needed. Updated description, "
                "detection_signal, and clean_replay_task to cover −N avoidance."
            ),
        }),
        # Revise: strategic_overload — subtraction paralysis
        "strategic_overload": json.dumps({
            "id": "bakery_belt_overload",
            "category": "strategic_overload",
            "label": "Paralyzed by subtraction decisions",
            "description": (
                "Learner understands addition toward the target but cannot decide "
                "when to use −N items. Either avoids all subtraction items (playing "
                "as if they do not exist) or uses them randomly without connecting "
                "them to the running total. The decision of 'should I add or "
                "subtract right now?' exceeds working memory under time pressure."
            ),
            "likely_cause": (
                "Addition is a single-direction operation: always move the total up. "
                "Subtraction introduces a bidirectional decision: 'do I go up or "
                "down right now?' This doubles the comparison load at each item. "
                "Combined with belt movement and running-total tracking, the three "
                "concurrent demands exceed working memory capacity."
            ),
            "how_it_appears_in_play": (
                "Long pauses (> 5 seconds) specifically when −N items are on screen. "
                "Random tapping that mixes + and − items without a clear strategy. "
                "Total oscillates (goes up, then down, then up) rather than "
                "converging toward the target. Performance degrades specifically "
                "when −N items are introduced, not at level transitions."
            ),
            "detection_signal": (
                "Running total direction changes >= 3 times in a single order. "
                "Or: pause > 5 seconds occurs when >= 1 −N item is visible on belt "
                "but does not occur in orders with only +N items. "
                "Or: performance drops >= 40% on first 3 orders after −N introduction."
            ),
            "best_feedback_response": (
                "Look at your running total first. Is it above or below the target? "
                "If above, a minus pastry brings you closer. If below, a plus pastry "
                "brings you closer."
            ),
            "best_clean_replay_task": (
                "Static belt (no movement). Only −N items visible. Running total "
                "starts ABOVE target (e.g., total = 8, target = 5). Player must "
                "use −N items to reach the target. Isolates subtraction-as-tool "
                "without any addition decision."
            ),
            "reflection_prompt": (
                "When your total was too high, what kind of pastry could help you? "
                "How did you decide whether to use a plus or a minus?"
            ),
            "change_rationale": (
                "Revised from library: original entry described overload from belt "
                "speed + arithmetic pressure. Brief now has adaptive belt speed "
                "(no longer a fixed ramp) but introduces −N subtraction items. "
                "Overload source shifted from speed to bidirectional arithmetic "
                "decisions. Rewrote description, detection_signal, and "
                "clean_replay_task accordingly."
            ),
        }),
        # Unmatched risk: sign confusion
        "sign_confusion": json.dumps({
            "id": "bakery_sign_confusion",
            "category": "concept_confusion",
            "label": "Expects minus to add",
            "description": (
                "Learner taps a −N item expecting it to increase the running total "
                "by N rather than decrease it. Believes the minus sign is decorative "
                "or does not connect it to the subtraction operation."
            ),
            "likely_cause": (
                "In early arithmetic, the minus sign appears only in written "
                "equations (5 − 3 = 2), not attached to objects. A pastry labeled "
                "'−2' has no real-world analogy for young learners. The minus sign "
                "is visually small and may be confused with a hyphen or dash. "
                "The concept that an object can have negative value requires "
                "abstract reasoning that 7-9 year olds are still developing."
            ),
            "how_it_appears_in_play": (
                "Player taps a −N item and appears surprised when the running total "
                "decreases. Repeats the same action on the next −N item. "
                "Running total moves away from target after tapping −N items. "
                "Player does not self-correct after seeing the decrease."
            ),
            "detection_signal": (
                "Player taps a −N item when running total is already below target "
                "(total < target) on >= 2 orders. Running total moves further from "
                "target after the tap. No self-correction within 3 seconds of "
                "seeing the total decrease."
            ),
            "best_feedback_response": (
                "The minus sign means this pastry takes away from your total. "
                "Your total was 4. You tapped −2. Now your total is 2, not 6. "
                "The minus takes away."
            ),
            "best_clean_replay_task": (
                "Two pastries on a frozen belt: one +3 and one −3. Starting total "
                "is 0, target is 3. Player must learn that tapping +3 reaches the "
                "target and tapping −3 moves to −3. Three rounds with different "
                "values to build the pattern."
            ),
            "reflection_prompt": (
                "What happened to your total when you tapped the minus pastry? "
                "What does the minus sign mean for your total?"
            ),
            "change_rationale": (
                "New entry: brief risk 'Learner adds a −N item expecting it to add "
                "positively (sign confusion)' is not covered by any existing entry. "
                "Assigned to concept_confusion because the learner's mental model "
                "of what the minus sign does is incorrect — this is a conceptual "
                "misunderstanding, not a procedural or strategic error."
            ),
        }),
    }

    call_count = [0]

    def _mock_call(prompt: str) -> str:
        call_count[0] += 1
        # Match the prompt to the appropriate mock response.
        # Order matters: check specific unmatched-risk keywords first,
        # then revision-category keywords.
        if "expecting it to add positively" in prompt or "sign confusion" in prompt:
            return _MOCK_RESPONSES["sign_confusion"]
        if "representation_mismatch" in prompt:
            return _MOCK_RESPONSES["representation_mismatch"]
        if "strategic_overload" in prompt or "strategic paralysis" in prompt:
            return _MOCK_RESPONSES["strategic_overload"]
        # Default: reject unrecognized risks
        return json.dumps({"rejected": True, "reason": "Mock LLM: no matching mock response for this prompt."})

    return _mock_call


def _make_counted_llm(model: str, label: str):
    """Create a prompt->text callable with call counting.

    Returns (callable, counter_dict) where counter_dict has a "calls" key
    tracking how many times the callable was invoked.
    """
    import os

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("  WARNING: ANTHROPIC_API_KEY not set. --llm flag requires it.")
        print("  Use --mock-llm for plumbing tests without an API key.")
        sys.exit(1)

    counter = {"calls": 0, "model": model, "label": label}

    try:
        import anthropic
        client = anthropic.Anthropic(api_key=api_key)

        def _call(prompt: str) -> str:
            counter["calls"] += 1
            response = client.messages.create(
                model=model,
                max_tokens=2048,
                messages=[{"role": "user", "content": prompt}],
            )
            return response.content[0].text

        return _call, counter

    except ImportError:
        import requests as _requests

        def _call_http(prompt: str) -> str:
            counter["calls"] += 1
            resp = _requests.post(
                "https://api.anthropic.com/v1/messages",
                headers={
                    "x-api-key": api_key,
                    "anthropic-version": "2023-06-01",
                    "content-type": "application/json",
                },
                json={
                    "model": model,
                    "max_tokens": 2048,
                    "messages": [{"role": "user", "content": prompt}],
                },
                timeout=120,
            )
            if resp.status_code != 200:
                raise RuntimeError(f"API error {resp.status_code}: {resp.text[:300]}")
            return resp.json()["content"][0]["text"]

        return _call_http, counter


def main():
    parser = argparse.ArgumentParser(description="Run Misconception Architect stub on a current game.")
    parser.add_argument(
        "--game",
        choices=list(GAME_FACTORIES.keys()),
        default="bakery-rush",
        help="Which game's briefs to use (default: bakery-rush)",
    )
    parser.add_argument(
        "--llm",
        action="store_true",
        default=False,
        help="Use targeted LLM for revised entries and unmatched risks (requires ANTHROPIC_API_KEY)",
    )
    parser.add_argument(
        "--mock-llm",
        action="store_true",
        default=False,
        help="Use mock targeted LLM for testing the full pathway without an API key",
    )
    parser.add_argument(
        "--rewrite-model",
        default="claude-sonnet-4-6",
        help="Strong model for entry rewrites and unmatched risks (default: claude-sonnet-4-6)",
    )
    parser.add_argument(
        "--gate-model",
        default="claude-haiku-4-5-20251001",
        help="Cheap model for semantic keep-vs-revise gate (default: claude-haiku-4-5-20251001)",
    )
    parser.add_argument(
        "--write-back",
        action="store_true",
        default=False,
        help="Write pending library write-back files for revised primary entries",
    )
    args = parser.parse_args()

    game_data = GAME_FACTORIES[args.game]()
    job_id = game_data["job_id"]

    # Build LLM callables if requested
    targeted_llm = None
    gate_llm = None
    counters = []

    if args.mock_llm:
        print("  Targeted LLM enabled (mock mode — no API calls)")
        targeted_llm = _make_mock_targeted_llm()
    elif args.llm:
        print(f"  Gate model   : {args.gate_model}")
        print(f"  Rewrite model: {args.rewrite_model}")
        targeted_llm, rewrite_counter = _make_counted_llm(args.rewrite_model, "rewrite")
        gate_llm, gate_counter = _make_counted_llm(args.gate_model, "gate")
        counters = [gate_counter, rewrite_counter]

    # Write synthetic briefs to a temp directory
    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)

        loop_path = tmp / "lowest_viable_loop_brief.json"
        family_path = tmp / "family_architecture_brief.json"
        interaction_path = tmp / "interaction_decision_memo.json"

        loop_path.write_text(json.dumps(game_data["loop_brief"], indent=2))
        family_path.write_text(json.dumps(game_data["family_brief"], indent=2))
        interaction_path.write_text(json.dumps(game_data["interaction_memo"], indent=2))

        artifact_paths = {
            "lowest_viable_loop_brief": loop_path,
            "family_architecture_brief": family_path,
            "interaction_decision_memo": interaction_path,
        }

        print(f"Running Misconception Architect stub for: {args.game} (job_id: {job_id})")
        print(f"  Repo root: {REPO_ROOT}")

        result = run_agent(
            repo_root=REPO_ROOT,
            job_id=job_id,
            artifact_paths=artifact_paths,
            targeted_llm=targeted_llm,
            gate_llm=gate_llm,
            enable_writeback=args.write_back,
        )

    print(f"\nResult:")
    print(f"  artifact_name : {result.artifact_name}")
    print(f"  version       : {result.artifact_version}")
    print(f"  status        : {result.artifact['status']}")
    print(f"  gate_passed   : {result.artifact['gate_threshold_met']}")
    total = len(result.artifact['misconceptions'])
    print(f"  valid_count   : {result.artifact['valid_misconception_count']}/{total}")
    print(f"  library_used  : {result.artifact['library_reference_used']}")
    print(f"  workspace     : {result.artifact_path}")

    # Copy to artifacts/jobs/ for durable reference
    jobs_dir = REPO_ROOT / "artifacts" / "jobs" / job_id
    jobs_dir.mkdir(parents=True, exist_ok=True)
    dest = jobs_dir / f"misconception_map_v{result.artifact_version}.json"
    shutil.copy(result.artifact_path, dest)
    print(f"  snapshot      : {dest.relative_to(REPO_ROOT)}")

    # Print the misconception summary
    print(f"\nMisconceptions generated ({result.artifact['interaction_type']}):")
    for m in result.artifact["misconceptions"]:
        rationale = m.get("change_rationale", "(no rationale)")
        priority = m.get("priority", "")
        quality = m.get("quality_notes", "")
        pri_tag = f" [{priority}]" if priority else ""
        print(f"  [{m['category']:30s}] {m['label']}{pri_tag}")
        print(f"    rationale: {rationale[:140]}")
        if quality:
            print(f"    QUALITY: {quality}")

    print(f"\nNotes: {result.artifact['notes'][:400]}...")

    # Print API call counts
    if counters:
        print(f"\nAPI calls by model:")
        for c in counters:
            print(f"  {c['label']:10s} ({c['model']}): {c['calls']} calls")
        total_calls = sum(c["calls"] for c in counters)
        print(f"  {'total':10s}: {total_calls} calls")

    # Print write-back info
    wb_path = result.artifact.get("_writeback_pending_path")
    if wb_path:
        print(f"\nLibrary write-back:")
        print(f"  pending file: {Path(wb_path).relative_to(REPO_ROOT)}")
        # Read and summarize
        with open(wb_path) as f:
            wb_data = json.load(f)
        for entry in wb_data.get("entries_to_update", []):
            cat = entry["category"]
            fields = entry["fields_changed"]
            print(f"  [{cat}] {len(fields)} fields changed: {', '.join(fields)}")
            for field, diff in entry["field_diff"].items():
                old_preview = diff["old"][:60].replace("\n", " ")
                new_preview = diff["new"][:60].replace("\n", " ")
                print(f"    {field}:")
                print(f"      old: {old_preview}...")
                print(f"      new: {new_preview}...")
        print(f"  To apply: python3 -c \"from agents.misconception_architect.agent import apply_library_writeback; from pathlib import Path; print(apply_library_writeback(Path('{wb_path}'), Path('{REPO_ROOT}'), dry_run=False))\"")
    elif args.write_back:
        print(f"\nLibrary write-back: no eligible entries (no revised primaries passed quality checks)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
