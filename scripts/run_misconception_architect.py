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

GAME_FACTORIES = {
    "bakery-rush": _bakery_rush_briefs,
    "fire-dispatch": _fire_dispatch_briefs,
    "unit-circle": _unit_circle_briefs,
}


def main():
    parser = argparse.ArgumentParser(description="Run Misconception Architect stub on a current game.")
    parser.add_argument(
        "--game",
        choices=list(GAME_FACTORIES.keys()),
        default="bakery-rush",
        help="Which game's briefs to use (default: bakery-rush)",
    )
    args = parser.parse_args()

    game_data = GAME_FACTORIES[args.game]()
    job_id = game_data["job_id"]

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
        )

    print(f"\nResult:")
    print(f"  artifact_name : {result.artifact_name}")
    print(f"  version       : {result.artifact_version}")
    print(f"  status        : {result.artifact['status']}")
    print(f"  gate_passed   : {result.artifact['gate_threshold_met']}")
    print(f"  valid_count   : {result.artifact['valid_misconception_count']}/6")
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
        print(f"  [{m['category']:30s}] {m['label']}")

    print(f"\nNotes: {result.artifact['notes'][:200]}...")
    return 0


if __name__ == "__main__":
    sys.exit(main())
