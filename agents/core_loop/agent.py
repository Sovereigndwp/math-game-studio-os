from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from utils.shared_agent_runner import AgentSpec, SharedAgentRunner


# Templates indexed by primary_interaction_type
LOOP_TEMPLATES = {
    "route_and_dispatch": {
        "what_appears_first": "A set of items arrives with labels or properties. One or more destination slots are visible.",
        "what_the_learner_notices": "Each item has a property that determines which destination is correct.",
        "what_the_learner_does_first": "Selects an item and drags or taps it toward a destination.",
        "first_correct_action": "Routes the first item to the matching destination based on its mathematical property.",
        "immediate_feedback": "Destination slot highlights or confirms receipt; incorrect routing bounces the item back.",
        "what_repeats_next": "The next item appears. Destinations may update or new ones appear as difficulty increases.",
        "signature_moment": "The moment the learner routes the last item in a wave correctly and all destinations are filled — the screen clears cleanly.",
        "fail_state": "An item reaches an incorrect destination. A brief visual error plays and the item resets for retry.",
        "max_steps": 4,
        "simultaneous_elements": 3,
        "time_to_first_correct_seconds": 8,
        "confusion_risks": [
            "Learner does not read item label before routing.",
            "Too many destination slots visible at once creates decision paralysis.",
        ],
        "teacher_shortcut": "Teacher selects 2-destination mode. Reduces option set and clarifies math demand.",
        "micro_proto": "Paper version: index cards as items, labeled boxes as destinations. Learner physically routes 5 cards.",
    },
    "combine_and_build": {
        "what_appears_first": "A target value or structure is displayed. A set of component pieces is available to combine.",
        "what_the_learner_notices": "The target cannot be reached with a single piece — combination is required.",
        "what_the_learner_does_first": "Selects a component and combines it with another toward the target.",
        "first_correct_action": "Combines two components whose sum or product matches part or all of the target value.",
        "immediate_feedback": "A progress indicator fills or target updates to show remaining gap. Incorrect combination shakes.",
        "what_repeats_next": "A new target appears, or the gap resets with harder piece values.",
        "signature_moment": "Final piece snaps into place and the target structure completes — visual and audio payoff confirms.",
        "fail_state": "Combining wrong pieces triggers a reset animation; pieces return to the tray.",
        "max_steps": 4,
        "simultaneous_elements": 4,
        "time_to_first_correct_seconds": 10,
        "confusion_risks": [
            "Learner guesses by trial without computing — no math reasoning engaged.",
            "Too many pieces make the selection space too large.",
        ],
        "teacher_shortcut": "Teacher locks the number of available pieces to 2. Eliminates enumeration strategies.",
        "micro_proto": "Paper: give learner numbered tiles. They arrange tiles to hit a target sum in under 30 seconds.",
    },
    "allocate_and_balance": {
        "what_appears_first": "A total quantity and a set of slots or receivers. Slot labels indicate constraints.",
        "what_the_learner_notices": "The total must be distributed correctly — not evenly, but according to the constraints.",
        "what_the_learner_does_first": "Assigns a value to one slot.",
        "first_correct_action": "Allocates the correct quantity to the first slot while respecting the constraint.",
        "immediate_feedback": "Running total updates; over-allocation or under-allocation shown visually.",
        "what_repeats_next": "Remaining quantity must fill remaining slots — tension builds as options narrow.",
        "signature_moment": "Last allocation fills the final slot exactly — balance indicator snaps to zero remainder.",
        "fail_state": "Over-allocation causes a visual overflow effect; learner must reassign.",
        "max_steps": 4,
        "simultaneous_elements": 3,
        "time_to_first_correct_seconds": 10,
        "confusion_risks": [
            "Learner treats allocation as equal sharing by default.",
            "Running total display is not clearly tied to the constraint.",
        ],
        "teacher_shortcut": "Teacher sets two-slot mode — one allocation decision only, makes arithmetic demand explicit.",
        "micro_proto": "Paper: tokens on a mat. Distribute N tokens into labeled cups so each cup meets its label constraint.",
    },
    "transform_and_manipulate": {
        "what_appears_first": "An object with a visible mathematical property (value, angle, ratio, form). A target state is shown.",
        "what_the_learner_notices": "The object must be changed to match the target — transformation is the task.",
        "what_the_learner_does_first": "Applies the first transformation gesture (rotation, scaling, flip, substitution).",
        "first_correct_action": "Transforms the object such that its mathematical property matches the target.",
        "immediate_feedback": "Object and target animate toward alignment. Incorrect transformation leaves a visible gap.",
        "what_repeats_next": "Object resets to a new starting state with a new target — transformation type may compound.",
        "signature_moment": "Object locks into the target state with a satisfying snap and overlay confirmation.",
        "fail_state": "Transformation overshoot triggers a brief reset; learner must re-start from mid-state.",
        "max_steps": 3,
        "simultaneous_elements": 2,
        "time_to_first_correct_seconds": 12,
        "confusion_risks": [
            "Learner applies correct gesture in wrong magnitude.",
            "Multiple overlapping transformation types confuse the primary mechanic.",
        ],
        "teacher_shortcut": "Teacher locks to single-transformation type per session — one axis of manipulation only.",
        "micro_proto": "Paper: learner is given a fraction card and told to transform it to an equivalent form by folding a paper strip.",
    },
    "navigate_and_position": {
        "what_appears_first": "A coordinate space, number line, or grid. A target position is marked.",
        "what_the_learner_notices": "An element must be moved to the exact correct position.",
        "what_the_learner_does_first": "Moves or places the element toward the target position.",
        "first_correct_action": "Places the element at the mathematically correct coordinate or position.",
        "immediate_feedback": "Proximity indicator updates. Correct placement locks and confirms. Incorrect placement highlights error distance.",
        "what_repeats_next": "New target position appears. Space may expand or units may change.",
        "signature_moment": "Element lands on the exact position — grid snaps, number line locks, coordinate confirms.",
        "fail_state": "Incorrect placement shows distance-to-correct overlay and resets element to start.",
        "max_steps": 3,
        "simultaneous_elements": 2,
        "time_to_first_correct_seconds": 8,
        "confusion_risks": [
            "Learner over-relies on estimation and does not compute.",
            "Fine motor placement imprecision is confused with mathematical error.",
        ],
        "teacher_shortcut": "Teacher enables snap-to-half-unit mode — reduces motor precision demand, keeps math demand.",
        "micro_proto": "Number line on paper: learner places a token at the correct value after computing from a word problem.",
    },
    "sequence_and_predict": {
        "what_appears_first": "A partial sequence with visible elements and one or more gaps.",
        "what_the_learner_notices": "The pattern has a rule — completing the sequence requires discovering and applying it.",
        "what_the_learner_does_first": "Predicts or places the next element in the sequence.",
        "first_correct_action": "Places the correct value that continues the mathematical pattern.",
        "immediate_feedback": "Placed element animates into the sequence. Correct continuation triggers pattern-reveal effect. Incorrect placement shakes.",
        "what_repeats_next": "Sequence advances. New pattern or extended complexity appears.",
        "signature_moment": "Final gap fills and the complete sequence reveals its rule visually — connection lines or highlight shows the pattern.",
        "fail_state": "Incorrect placement removes that element and resets to the gap — learner must re-examine the pattern.",
        "max_steps": 4,
        "simultaneous_elements": 3,
        "time_to_first_correct_seconds": 12,
        "confusion_risks": [
            "Learner guesses the difference rule without identifying the mathematical basis.",
            "Too many simultaneous gaps make the rule ambiguous.",
        ],
        "teacher_shortcut": "Teacher sets single-gap mode for first exposure — removes ambiguity, forces one-step reasoning.",
        "micro_proto": "Paper: learner is given a partial sequence on cards and places blank cards with their computed answers.",
    },
}


def core_loop_stub(context: Dict[str, Any]) -> Dict[str, Any]:
    intake = context["artifact_inputs"]["intake_brief"]
    memo = context["artifact_inputs"]["interaction_decision_memo"]
    family = context["artifact_inputs"]["family_architecture_brief"]

    primary_interaction = memo.get("primary_interaction_type", "combine_and_build")
    math_domain = intake.get("likely_math_domain", "unknown")
    world_theme = intake.get("possible_world_theme", "unknown world")
    mission = intake.get("possible_profession_or_mission", "unknown mission")
    factory_type = family.get("factory_type", "age_band_specialist")
    family_name = family.get("family_name", "unnamed family")

    template = LOOP_TEMPLATES.get(primary_interaction, LOOP_TEMPLATES["combine_and_build"])

    concept = intake.get("plain_english_concept", "")
    one_sentence = intake.get("one_sentence_promise_draft", concept)

    first_60 = (
        f"Learner is introduced to the {world_theme} context. "
        f"A {primary_interaction.replace('_', ' ')} challenge appears. "
        f"{template['what_appears_first']} "
        f"Within 15 seconds, the learner understands what they must do: {template['what_the_learner_does_first']}. "
        f"The first attempt takes under {template['time_to_first_correct_seconds']} seconds. "
        f"Correct action produces immediate feedback: {template['immediate_feedback']} "
        f"By 60 seconds, the learner has completed at least one full loop and seen the core math demand clearly."
    )

    lvl_description = (
        f"The lowest viable loop for '{one_sentence}' is a single, complete instance of the "
        f"{primary_interaction.replace('_', ' ')} mechanic applied to one {math_domain} problem. "
        f"No difficulty scaling, no progression — just the minimum interaction that lets the learner "
        f"demonstrate the core math action and receive feedback. If this loop is not engaging on its own, "
        f"the concept is not viable."
    )

    core_loop_map = {
        "what_appears_first": template["what_appears_first"],
        "what_the_learner_notices": template["what_the_learner_notices"],
        "what_the_learner_does_first": template["what_the_learner_does_first"],
        "first_correct_action": template["first_correct_action"],
        "immediate_feedback": template["immediate_feedback"],
        "what_repeats_next": template["what_repeats_next"],
    }

    confusion_risks: List[str] = template["confusion_risks"]

    # Validate max_steps_per_loop (gate enforces <= 5)
    max_steps = min(template["max_steps"], 5)

    teacher_shortcut = template["teacher_shortcut"]
    micro_proto = template["micro_proto"]

    # Status: if primary interaction is unclear, force revise
    if primary_interaction not in LOOP_TEMPLATES:
        status = "revise"
        notes = f"Unknown primary_interaction_type '{primary_interaction}'. Cannot build loop template."
    else:
        status = "pass"
        notes = (
            f"Core loop designed for '{primary_interaction}' interaction in '{math_domain}' domain. "
            f"Family: '{family_name}' ({factory_type}). "
            f"Max steps: {max_steps}. Simultaneous elements: {template['simultaneous_elements']}."
        )

    return {
        "status": status,
        "timestamp": "2026-04-03T12:05:00Z",
        "first_60_seconds_flow": first_60,
        "lowest_viable_loop_description": lvl_description,
        "core_loop_map": core_loop_map,
        "signature_moment": template["signature_moment"],
        "fail_state_structure": template["fail_state"],
        "max_steps_per_loop": max_steps,
        "max_simultaneous_elements": template["simultaneous_elements"],
        "expected_time_to_first_correct_action_seconds": template["time_to_first_correct_seconds"],
        "expected_confusion_risks": confusion_risks,
        "teacher_shortcut_version": teacher_shortcut,
        "micro_prototype_recommendation": micro_proto,
        "notes": notes,
    }


def build_spec(repo_root: Path) -> AgentSpec:
    return AgentSpec(
        agent_name="core_loop_agent",
        expected_output_artifact="lowest_viable_loop_brief",
        expected_produced_by="Core Loop Agent",
        prompt_path=repo_root / "agents" / "core_loop" / "prompt.md",
        config_path=repo_root / "agents" / "core_loop" / "config.yaml",
        allowed_reads=["intake_brief", "interaction_decision_memo", "family_architecture_brief"],
        allowed_writes=["lowest_viable_loop_brief"],
        max_revision_count=2,
    )


def run(
    repo_root: Path,
    job_id: str,
    artifact_paths: Dict[str, Path],
    model_callable=None,
):
    """Run the Core Loop Agent.

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
        model_callable=model_callable if model_callable is not None else core_loop_stub,
    )
