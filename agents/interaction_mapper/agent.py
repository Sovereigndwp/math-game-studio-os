from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from utils.shared_agent_runner import AgentSpec, SharedAgentRunner


# Canonical interaction types — must match schema enum exactly
VALID_INTERACTION_TYPES = [
    "route_and_dispatch",
    "combine_and_build",
    "allocate_and_balance",
    "transform_and_manipulate",
    "navigate_and_position",
    "sequence_and_predict",
]

# Map: intake candidate hint → canonical type + purity score
CANDIDATE_MAP = {
    "route_and_dispatch": ("route_and_dispatch", 0.88),
    "combine_and_build": ("combine_and_build", 0.85),
    "allocate_and_balance": ("allocate_and_balance", 0.82),
    "transform_and_manipulate": ("transform_and_manipulate", 0.80),
    "navigate_and_position": ("navigate_and_position", 0.83),
    "sequence_and_predict": ("sequence_and_predict", 0.80),
}

# Math domain → best-fit interaction type when no candidates are given
DOMAIN_INTERACTION_FALLBACK = {
    "addition": "combine_and_build",
    "subtraction": "allocate_and_balance",
    "multiplication": "sequence_and_predict",
    "division": "allocate_and_balance",
    "fractions": "transform_and_manipulate",
    "ratios_and_rates": "allocate_and_balance",
    "trigonometry": "navigate_and_position",
    "algebra": "sequence_and_predict",
}

# Justification templates per type
JUSTIFICATION_TEMPLATES = {
    "route_and_dispatch": (
        "The core action is deciding where something goes — matching, routing, or dispatching "
        "an element to a destination. The math judgment drives every dispatch decision directly."
    ),
    "combine_and_build": (
        "The core action is assembling or summing parts into a whole. "
        "Each combination attempt is a direct math operation, making the action itself the math."
    ),
    "allocate_and_balance": (
        "The core action is distributing a quantity across slots or balancing two sides. "
        "Every allocation attempt surfaces the math constraint immediately."
    ),
    "transform_and_manipulate": (
        "The core action is changing the form, orientation, or value of an element. "
        "Mathematical equivalence or transformation is the mechanism, not the reward."
    ),
    "navigate_and_position": (
        "The core action is placing or moving an element to a mathematically correct position. "
        "The coordinate, angle, or location is the answer — navigation is the math."
    ),
    "sequence_and_predict": (
        "The core action is ordering, continuing, or predicting a mathematical pattern. "
        "The sequence logic is the game mechanic, not decoration on top of it."
    ),
}

# Alternatives to reject for each primary type
REJECTED_ALTERNATIVES_MAP = {
    "route_and_dispatch": [
        {"interaction_type": "combine_and_build", "why_weaker": "Building implies construction; this concept requires directional dispatch judgment, not assembly."},
    ],
    "combine_and_build": [
        {"interaction_type": "route_and_dispatch", "why_weaker": "Routing implies directing to a destination; this concept requires summing parts, not routing them."},
    ],
    "allocate_and_balance": [
        {"interaction_type": "combine_and_build", "why_weaker": "Building produces a whole; this concept requires maintaining balance across parts, which is a distribution problem."},
    ],
    "transform_and_manipulate": [
        {"interaction_type": "navigate_and_position", "why_weaker": "Navigation sets a position; transformation changes a value or form — distinct enough that mixing would harm purity."},
    ],
    "navigate_and_position": [
        {"interaction_type": "transform_and_manipulate", "why_weaker": "Manipulation changes form; navigation places an element at a correct location — the interaction purity breaks if conflated."},
    ],
    "sequence_and_predict": [
        {"interaction_type": "combine_and_build", "why_weaker": "Combining produces totals; sequencing requires ordering or extending a pattern — different core judgment."},
    ],
}


def interaction_mapper_stub(context: Dict[str, Any]) -> Dict[str, Any]:
    intake = context["artifact_inputs"]["intake_brief"]
    kill = context["artifact_inputs"]["kill_report"]

    math_domain = intake.get("likely_math_domain", "unknown")
    candidates: List[str] = intake.get("possible_interaction_candidates", [])
    age_band = intake.get("likely_age_band", "unknown")
    kill_status = kill.get("status", "pass")

    # If kill said redesign, surface a note but still proceed (gate enforced it already)
    redesign_note = ""
    if kill_status == "redesign":
        redesign_note = "Kill Test recommended redesign. Interaction selection reflects revised framing."

    # --- Select primary interaction type ---
    valid_candidates = [c for c in candidates if c in VALID_INTERACTION_TYPES]

    if valid_candidates:
        primary = valid_candidates[0]
        purity_score = CANDIDATE_MAP.get(primary, (primary, 0.75))[1]
        selection_basis = "intake_brief_candidates"
    elif math_domain in DOMAIN_INTERACTION_FALLBACK:
        primary = DOMAIN_INTERACTION_FALLBACK[math_domain]
        purity_score = 0.75
        selection_basis = f"math_domain_fallback:{math_domain}"
    else:
        primary = "combine_and_build"
        purity_score = 0.60
        selection_basis = "default_fallback"

    # --- Secondary type (only when genuinely needed) ---
    secondary = ""
    overload_warning = ""
    split_family_warning = False

    if len(valid_candidates) >= 2:
        secondary_candidate = valid_candidates[1]
        if secondary_candidate != primary:
            secondary = secondary_candidate
            overload_warning = (
                f"Secondary interaction '{secondary}' is present. "
                "Ensure it does not compete with or obscure the primary math action."
            )
            split_family_warning = True
        else:
            secondary = ""
    else:
        overload_warning = "No secondary interaction type identified. Single interaction type — purity is strong."

    is_action_itself_math = purity_score >= 0.75

    rejected = REJECTED_ALTERNATIVES_MAP.get(primary, [])

    # Determine status
    if purity_score < 0.6:
        status = "revise"
        notes = f"Purity score {purity_score:.2f} is below threshold. Selection basis: {selection_basis}."
    else:
        status = "pass"
        notes = (
            f"Interaction type selected based on {selection_basis}. "
            f"Purity score: {purity_score:.2f}. "
            + (redesign_note if redesign_note else "")
        ).strip()

    return {
        "status": status,
        "timestamp": "2026-04-03T12:03:00Z",
        "primary_interaction_type": primary,
        "secondary_interaction_type": secondary,
        "interaction_justification": JUSTIFICATION_TEMPLATES[primary],
        "rejected_alternatives": rejected,
        "interaction_purity_score": purity_score,
        "is_action_itself_the_math": is_action_itself_math,
        "interaction_overload_warning": overload_warning,
        "split_family_warning": split_family_warning,
        "notes": notes,
    }


def build_spec(repo_root: Path) -> AgentSpec:
    return AgentSpec(
        agent_name="interaction_mapper_agent",
        expected_output_artifact="interaction_decision_memo",
        expected_produced_by="Interaction Mapper Agent",
        prompt_path=repo_root / "agents" / "interaction_mapper" / "prompt.md",
        config_path=repo_root / "agents" / "interaction_mapper" / "config.yaml",
        allowed_reads=["intake_brief", "kill_report"],
        allowed_writes=["interaction_decision_memo"],
        max_revision_count=2,
    )


def run(
    repo_root: Path,
    job_id: str,
    artifact_paths: Dict[str, Path],
    model_callable=None,
):
    """Run the Interaction Mapper Agent.

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
        model_callable=model_callable if model_callable is not None else interaction_mapper_stub,
    )
