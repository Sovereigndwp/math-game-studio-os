"""
OrchestratorState — shared graph state for the Math Game Factory V3 orchestrator.

Every node reads from and writes to this TypedDict.
LangGraph passes the full state between nodes; nodes return only the fields they update.

All fields are optional (total=False) so any node can be the entry point
without requiring prior nodes to have run.

See: docs/orchestration_v3_blueprint.md
"""

from __future__ import annotations

from typing import Any, Dict, List, Literal, Optional, TypedDict


class OrchestratorState(TypedDict, total=False):

    # ── Identity ────────────────────────────────────────────────────────────
    run_id: str
    mode: Literal[
        "new_family_build",
        "family_expansion",
        "prototype_review_and_repair",
        "classroom_packaging",
    ]
    user_goal: str
    timestamp: str

    # ── Concept ─────────────────────────────────────────────────────────────
    game_title: str
    game_family: str
    age_band: str
    grade_band: str
    math_domain: str
    target_skill: str
    transfer_target: str

    # ── Design ──────────────────────────────────────────────────────────────
    role_fantasy: str
    world_theme: str
    primary_interaction: str          # from approved OS interaction taxonomy
    secondary_interaction: Optional[str]
    one_sentence_promise: str

    # ── Research ────────────────────────────────────────────────────────────
    evidence_summary: str
    standards_notes: List[str]
    tool_recommendations: List[str]   # e.g. ["Code.org Game Lab", "LangSmith"]
    evidence_risks: List[str]

    # ── Learning design ─────────────────────────────────────────────────────
    prerequisite_skills: List[str]
    conceptual_goal: str
    procedural_goal: str

    misconception_map: List[Dict[str, Any]]
    # Each entry:
    # {
    #   "category": "procedure_slip" | "concept_confusion" | ...,
    #   "label": str,
    #   "description": str,
    #   "detection_signal": str,
    #   "feedback_response": str,
    #   "clean_replay_task": str,
    # }

    evidence_of_understanding: List[str]   # observable signals that concept is internalized
    guessing_risk_signals: List[str]       # observable signals of impulsive/bypass behavior

    reflection_plan: Dict[str, str]
    # {
    #   "planning_prompt": str,
    #   "monitoring_prompt": str,
    #   "evaluation_prompt": str,
    # }

    adaptation_plan: Dict[str, Any]
    # {
    #   "hint_triggers": [...],
    #   "alternate_representation_triggers": [...],
    #   "pace_adjustment_triggers": [...],
    #   "misconception_specific_retries": {...},
    # }

    core_loop_map: List[str]           # ordered steps: appear → notice → solve → act → world changes → evidence
    progression_plan: List[Dict[str, Any]]

    # ── Evaluation scores ────────────────────────────────────────────────────
    role_to_math_score: float          # 0.0 – 1.0. Gate threshold: 0.75
    loop_purity_score: float           # 0.0 – 1.0. Gate threshold: 0.80
    clarity_risks: List[str]           # cognitive load flags
    overload_risks: List[str]          # simultaneous demand flags
    teacher_value_score: float         # 0.0 – 1.0

    gate_fail_reasons: List[str]       # accumulates across gate checks
    gate_fail_count: int               # triggers Human Review 2 when >= 2

    # ── Outputs ──────────────────────────────────────────────────────────────
    spec_draft: str                    # prototype_spec JSON as string
    prototype_brief: str               # implementation handoff
    teacher_guide: str
    parent_summary: str
    dashboard_spec: str                # teacher evidence dashboard spec
    test_plan: str                     # silent playtest observation kit
    packaging_bundle: Dict[str, str]   # all outputs keyed by name

    # ── Memory links ─────────────────────────────────────────────────────────
    similar_prior_games: List[str]     # game names from Memory Vault
    reusable_patterns: List[str]       # pattern IDs from system memory
    failed_patterns: List[str]         # pattern IDs to avoid repeating

    # ── Human review ─────────────────────────────────────────────────────────
    human_review_1_decision: Literal["approve", "revise"]
    human_review_1_notes: str
    human_review_2_decision: Literal["repair", "kill"]
    human_review_2_notes: str
    human_review_3_decision: Literal["approve", "revise"]
    human_review_3_notes: str
