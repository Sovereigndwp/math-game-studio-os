from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

from utils.shared_agent_runner import AgentSpec, SharedAgentRunner


# Factory type selection: age_band → factory_type
AGE_BAND_FACTORY_MAP = {
    "5_to_8": "universal_ladder",
    "8_to_11": "universal_ladder",
    "11_to_14": "age_band_specialist",
    "14_to_18": "advanced_anchor",
    "unknown": "age_band_specialist",
}

# Interaction type → family name prefix pattern
INTERACTION_FAMILY_PREFIX = {
    "route_and_dispatch": "Dispatch",
    "combine_and_build": "Builder",
    "allocate_and_balance": "Balance",
    "transform_and_manipulate": "Transform",
    "navigate_and_position": "Navigator",
    "sequence_and_predict": "Sequencer",
}

# Growth path templates per factory type
GROWTH_PATH_TEMPLATES = {
    "universal_ladder": (
        "Expand numerical range (e.g., sums to 10 → sums to 20 → sums to 100). "
        "Increase simultaneous elements. Introduce time pressure at higher levels."
    ),
    "age_band_specialist": (
        "Increase conceptual complexity within the math domain. "
        "Add multi-step problems. Introduce edge cases and exception handling."
    ),
    "advanced_anchor": (
        "Increase problem depth and abstraction. "
        "Introduce proofs, transformations, or multi-domain integration. "
        "Build toward a capstone challenge structure."
    ),
}

# Boundary rule templates per factory type
BOUNDARY_RULE_TEMPLATES = {
    "universal_ladder": (
        "Family stays within the same interaction type and world theme. "
        "New games may only extend the numerical range or add complexity layers — "
        "not change the core action or math domain."
    ),
    "age_band_specialist": (
        "Family stays within the same math domain and age band. "
        "A new game that requires a fundamentally different interaction type belongs in a new family."
    ),
    "advanced_anchor": (
        "Family stays anchored to the advanced math domain. "
        "New games must maintain conceptual depth. "
        "Simplifications that reduce to elementary concepts break the family boundary."
    ),
}

# Boundary break examples per factory type
BOUNDARY_BREAK_EXAMPLES = {
    "universal_ladder": (
        "Adding a multiplication mechanic to an addition-family game breaks the boundary — "
        "it requires a different interaction and belongs in a new family."
    ),
    "age_band_specialist": (
        "Designing a high-school version of a middle-school family game breaks the boundary — "
        "the age band assumption underpins the entire scaffolding approach."
    ),
    "advanced_anchor": (
        "Adding a 'beginner' level that reduces to single-digit arithmetic breaks the anchor — "
        "the family is built around advanced conceptual depth, not numerical range."
    ),
}


def _derive_family_name(mission: str, world_theme: str, primary_interaction: str, math_domain: str) -> str:
    prefix = INTERACTION_FAMILY_PREFIX.get(primary_interaction, "Studio")
    if mission not in ("unknown mission", ""):
        # Capitalize first meaningful word of mission; skip if it duplicates the prefix
        words = [
            w.capitalize() for w in mission.split()
            if len(w) > 2 and w.lower() != prefix.lower()
        ]
        suffix = words[0] if words else "Lab"
    elif world_theme not in ("unknown world", ""):
        words = [
            w.capitalize() for w in world_theme.split()
            if len(w) > 2 and w.lower() != prefix.lower()
        ]
        suffix = words[0] if words else "World"
    else:
        suffix = math_domain.replace("_", " ").title() if math_domain != "unknown" else "Core"
    return f"{prefix} {suffix} Family"


def family_architect_stub(context: Dict[str, Any]) -> Dict[str, Any]:
    intake = context["artifact_inputs"]["intake_brief"]
    memo = context["artifact_inputs"]["interaction_decision_memo"]

    age_band = intake.get("likely_age_band", "unknown")
    math_domain = intake.get("likely_math_domain", "unknown")
    mission = intake.get("possible_profession_or_mission", "unknown mission")
    world_theme = intake.get("possible_world_theme", "unknown world")
    likely_factory_type = intake.get("likely_factory_type", "age_band_specialist")

    primary_interaction = memo.get("primary_interaction_type", "combine_and_build")
    split_family_warning = memo.get("split_family_warning", False)
    purity_score = memo.get("interaction_purity_score", 0.75)

    # Factory type: prefer memo-derived factory from intake, else fall back to age_band map
    factory_type = AGE_BAND_FACTORY_MAP.get(age_band, "age_band_specialist")
    # Honour the likely_factory_type if it's a valid enum value
    if likely_factory_type in {"universal_ladder", "age_band_specialist", "advanced_anchor"}:
        factory_type = likely_factory_type

    family_name = _derive_family_name(mission, world_theme, primary_interaction, math_domain)

    # Reuse recommendation: always create_new for new jobs (stub has no live registry)
    is_existing_family = False
    existing_match_confidence = 0.0
    reuse_recommendation = "create_new"

    # Overlap warnings
    overlap_warnings: List[str] = []
    if split_family_warning:
        overlap_warnings.append(
            "Secondary interaction type detected. Two distinct interaction types may need two separate families."
        )
    if purity_score < 0.7:
        overlap_warnings.append(
            "Interaction purity score is low. Family identity may be weakened if interaction is later revised."
        )

    # Placement reason
    reason_for_placement = (
        f"Concept maps to '{primary_interaction}' interaction type within the '{math_domain}' domain "
        f"for '{age_band}' age band. Factory type '{factory_type}' reflects the intended growth structure."
    )

    # Gate check: missing critical fields
    critical_missing = []
    if not family_name.strip():
        critical_missing.append("family_name")
    if not reason_for_placement.strip():
        critical_missing.append("reason_for_family_placement")

    if critical_missing:
        status = "revise"
        notes = f"Critical fields missing: {', '.join(critical_missing)}. Cannot complete family placement."
    else:
        status = "pass"
        notes = (
            f"Family '{family_name}' created as '{factory_type}'. "
            f"Reuse recommendation: {reuse_recommendation}. "
            f"Overlap warnings: {len(overlap_warnings)}."
        )

    return {
        "status": status,
        "timestamp": "2026-04-03T12:04:00Z",
        "family_name": family_name,
        "factory_type": factory_type,
        "is_existing_family": is_existing_family,
        "existing_family_match_confidence": existing_match_confidence,
        "reason_for_family_placement": reason_for_placement,
        "family_growth_path": GROWTH_PATH_TEMPLATES[factory_type],
        "family_boundary_rule": BOUNDARY_RULE_TEMPLATES[factory_type],
        "boundary_break_example": BOUNDARY_BREAK_EXAMPLES[factory_type],
        "reuse_recommendation": reuse_recommendation,
        "family_overlap_warnings": overlap_warnings,
        "notes": notes,
    }


def build_spec(repo_root: Path) -> AgentSpec:
    return AgentSpec(
        agent_name="family_architect_agent",
        expected_output_artifact="family_architecture_brief",
        expected_produced_by="Family Architect Agent",
        prompt_path=repo_root / "agents" / "family_architect" / "prompt.md",
        config_path=repo_root / "agents" / "family_architect" / "config.yaml",
        allowed_reads=["intake_brief", "interaction_decision_memo"],
        allowed_writes=["family_architecture_brief"],
        max_revision_count=2,
    )


def run(
    repo_root: Path,
    job_id: str,
    artifact_paths: Dict[str, Path],
    model_callable=None,
):
    """Run the Family Architect Agent.

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
        model_callable=model_callable if model_callable is not None else family_architect_stub,
    )
