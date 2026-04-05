"""
Loop Purity Auditor
===================
Tests whether the learner action IS the math.

Fail condition (from OS spec 2026, Rule B):
  The math could be removed and the loop would still function.

A pure loop cannot be completed through speed-tapping, surface-pattern
matching, or guessing without engaging the mathematical concept.

Usage
-----
    from utils.loop_purity_auditor import LoopPuritySpec, audit_loop_purity

    spec = LoopPuritySpec(
        game_name="Bakery Rush",
        core_loop_sentence=(
            "Tap pastries whose values sum to the customer's target."
        ),
        math_action_mapping=(
            "Each tap adds the pastry's +N value to a running total; "
            "success requires the total to equal the target exactly."
        ),
        player_actions=[
            "tap pastry on belt",
            "observe running total",
            "observe overshoot feedback",
        ],
        success_conditions=[
            "running total equals target exactly",
        ],
        fail_conditions=[
            "patience timer expires",
            "running total exceeds target repeatedly",
        ],
        math_domain="addition / additive decomposition",
        luck_skill_ratio=0.75,
        guessing_surface=(
            "belt items are labeled with +N values visible before selection"
        ),
        bypass_path_exists=False,
        bypass_path_description="",
        error_categories_detectable=[
            "impulsive_guess",
            "procedure_slip",
            "concept_confusion",
        ],
        reflection_beat_present=True,
        teacher_evidence_defined=False,
    )

    report = audit_loop_purity(spec)
    print(report.verdict)        # "pure" | "advisory" | "compromised"
    print(report.purity_score)   # 0.0 – 1.0
    for c in report.checks:
        print(c.check_name, "PASS" if c.passed else "FAIL", c.detail)
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Sequence


# ─────────────────────────────────────────────────────────────────────────────
# Spec types
# ─────────────────────────────────────────────────────────────────────────────

@dataclass
class LoopPuritySpec:
    """
    Declarative description of a game's core loop for purity evaluation.

    All fields are required unless marked optional.
    """
    game_name: str

    # The entire loop in one sentence (from core_loop_sentence in prototype_spec).
    core_loop_sentence: str

    # Explains how the player's action maps to a mathematical operation.
    # Must name the operation explicitly (e.g., "adds X to running sum").
    math_action_mapping: str

    # What the player physically does each round.
    player_actions: List[str]

    # What state satisfies the round.
    success_conditions: List[str]

    # What state fails the round.
    fail_conditions: List[str]

    # The mathematical concept and domain being exercised.
    math_domain: str

    # 0.0 = pure luck, 1.0 = pure skill.
    # Below 0.4 is a design smell — see OS spec Rule B.
    luck_skill_ratio: float

    # Description of what information the player has BEFORE guessing.
    # If rich info is available, guessing can still be strategic — note that.
    guessing_surface: str

    # Is there a known path to success that bypasses mathematical reasoning?
    # e.g. "the player can memorize that tap 3 always wins on level 1".
    bypass_path_exists: bool

    # Required if bypass_path_exists is True.
    bypass_path_description: str

    # Which of the 6 OS error categories this game can detect and classify.
    error_categories_detectable: List[str]

    # Does at least one reflection beat exist in the loop?
    reflection_beat_present: bool

    # Is there a teacher evidence output defined?
    teacher_evidence_defined: bool

    # Optional: from the prototype_spec's interaction_model.error_handling.
    error_handling_description: Optional[str] = None

    # Optional: from prototype_spec's interaction_constraints.
    exact_match_required: Optional[bool] = None


@dataclass
class PurityCheckResult:
    """Result of a single named purity check."""
    check_name: str
    passed: bool
    weight: float          # relative importance in overall score
    detail: str            # short explanation of pass or fail reason
    recommendation: str    # what to fix if failed; empty if passed


@dataclass
class LoopPurityReport:
    """Full output of audit_loop_purity()."""
    game_name: str
    purity_score: float           # 0.0 – 1.0 weighted aggregate
    verdict: str                  # "pure" | "advisory" | "compromised"
    checks: List[PurityCheckResult]
    fail_conditions_found: List[str]
    warnings: List[str]
    passed_count: int
    total_count: int


# ─────────────────────────────────────────────────────────────────────────────
# Constants
# ─────────────────────────────────────────────────────────────────────────────

REQUIRED_ERROR_CATEGORIES = {
    "procedure_slip",
    "concept_confusion",
    "representation_mismatch",
    "impulsive_guess",
    "rule_misunderstanding",
    "strategic_overload",
}

# Minimum number of error categories a loop must be able to detect.
MIN_DETECTABLE_CATEGORIES = 3

# Skill ratio below this → guessing is too viable.
MIN_LUCK_SKILL_RATIO = 0.4

# Verdict thresholds.
VERDICT_PURE       = 0.85
VERDICT_ADVISORY   = 0.60

# Keywords that signal mathematical language in free-text fields.
MATH_KEYWORDS = re.compile(
    r"\b(sum|total|equal|exact|value|count|add|subtract|multiply|divide|"
    r"match|target|fraction|angle|ratio|compute|calculate|number|quantity|"
    r"greater|less|remain|balance|decompos|compos|factor|product|quotient|"
    r"place.?value|carry|regroup|equivalent|proportion|percent|rate)\b",
    re.IGNORECASE,
)


# ─────────────────────────────────────────────────────────────────────────────
# Individual check functions
# ─────────────────────────────────────────────────────────────────────────────

def _check_math_is_core_action(spec: LoopPuritySpec) -> PurityCheckResult:
    """
    The math_action_mapping must describe a real mathematical operation.
    Looks for explicit mathematical language; penalises vague descriptions.
    Weight: 2.0 (critical)
    """
    hits = MATH_KEYWORDS.findall(spec.math_action_mapping)
    unique_hits = set(h.lower() for h in hits)
    passed = len(unique_hits) >= 2

    # Also check the core_loop_sentence for at least one math term.
    sentence_hits = MATH_KEYWORDS.findall(spec.core_loop_sentence)
    passed = passed and len(sentence_hits) >= 1

    detail = (
        f"math_action_mapping contains {len(unique_hits)} distinct math term(s): "
        f"{sorted(unique_hits)[:5]}."
        if passed
        else f"Only {len(unique_hits)} math term(s) found in math_action_mapping; "
             f"description may be too vague to confirm the action IS the math."
    )
    recommendation = (
        ""
        if passed
        else "Rewrite math_action_mapping to explicitly name the mathematical "
             "operation. e.g. 'each tap adds the item's value to a running sum; "
             "success requires the sum to equal the target exactly'."
    )
    return PurityCheckResult(
        check_name="math_is_core_action",
        passed=passed,
        weight=2.0,
        detail=detail,
        recommendation=recommendation,
    )


def _check_success_requires_math(spec: LoopPuritySpec) -> PurityCheckResult:
    """
    Success conditions must be stated in mathematical terms.
    A condition like 'player presses confirm' is not enough.
    Weight: 1.5
    """
    math_conditions = [
        c for c in spec.success_conditions
        if MATH_KEYWORDS.search(c)
    ]
    passed = len(math_conditions) >= 1

    detail = (
        f"{len(math_conditions)}/{len(spec.success_conditions)} success condition(s) "
        f"contain mathematical language."
        if passed
        else "No success condition names a mathematical outcome. "
             "Success appears to be non-mathematical."
    )
    recommendation = (
        ""
        if passed
        else "At least one success_condition must require a specific mathematical "
             "result. e.g. 'running total equals target exactly' or "
             "'angle placed within 5° of correct position'."
    )
    return PurityCheckResult(
        check_name="success_requires_math",
        passed=passed,
        weight=1.5,
        detail=detail,
        recommendation=recommendation,
    )


def _check_guessing_not_viable(spec: LoopPuritySpec) -> PurityCheckResult:
    """
    Luck/skill ratio must be >= MIN_LUCK_SKILL_RATIO and there must be no
    known bypass path.
    Weight: 2.0 (critical)
    """
    ratio_ok   = spec.luck_skill_ratio >= MIN_LUCK_SKILL_RATIO
    bypass_ok  = not spec.bypass_path_exists
    passed = ratio_ok and bypass_ok

    parts = []
    if not ratio_ok:
        parts.append(
            f"luck_skill_ratio={spec.luck_skill_ratio:.2f} is below the "
            f"minimum {MIN_LUCK_SKILL_RATIO:.2f} — guessing is too viable."
        )
    if not bypass_ok:
        parts.append(
            f"bypass_path_exists=True: '{spec.bypass_path_description}'"
        )
    if passed:
        parts.append(
            f"luck_skill_ratio={spec.luck_skill_ratio:.2f} ≥ {MIN_LUCK_SKILL_RATIO:.2f} "
            f"and no bypass path identified."
        )

    detail = " ".join(parts)
    recommendation = (
        ""
        if passed
        else "Raise luck_skill_ratio or redesign the loop so that guessing "
             "cannot reliably succeed. If a bypass path exists, document and "
             "eliminate it before shipping."
    )
    return PurityCheckResult(
        check_name="guessing_not_viable",
        passed=passed,
        weight=2.0,
        detail=detail,
        recommendation=recommendation,
    )


def _check_error_detection_present(spec: LoopPuritySpec) -> PurityCheckResult:
    """
    The loop must be able to detect and classify at least MIN_DETECTABLE_CATEGORIES
    of the six required error categories.
    Weight: 1.5
    """
    valid = set(spec.error_categories_detectable) & REQUIRED_ERROR_CATEGORIES
    passed = len(valid) >= MIN_DETECTABLE_CATEGORIES

    detail = (
        f"Detectable categories ({len(valid)}): {sorted(valid)}."
        if passed
        else f"Only {len(valid)}/{len(REQUIRED_ERROR_CATEGORIES)} required "
             f"categories detectable: {sorted(valid)}. "
             f"Minimum required: {MIN_DETECTABLE_CATEGORIES}."
    )
    recommendation = (
        ""
        if passed
        else f"Add detection logic for at least "
             f"{MIN_DETECTABLE_CATEGORIES - len(valid)} more error category/ies. "
             f"Missing from detectable list: "
             f"{sorted(REQUIRED_ERROR_CATEGORIES - valid)}."
    )
    return PurityCheckResult(
        check_name="error_detection_present",
        passed=passed,
        weight=1.5,
        detail=detail,
        recommendation=recommendation,
    )


def _check_fail_conditions_are_mathematical(spec: LoopPuritySpec) -> PurityCheckResult:
    """
    At least one fail condition should reflect a mathematical error, not only
    a time or administrative failure.
    Weight: 1.0
    """
    math_fails = [
        f for f in spec.fail_conditions
        if MATH_KEYWORDS.search(f)
    ]
    # A time-only failure (patience/timer expiry) is acceptable if there is also
    # a mathematical failure condition.
    passed = len(math_fails) >= 1

    detail = (
        f"{len(math_fails)}/{len(spec.fail_conditions)} fail condition(s) "
        f"reflect a mathematical error."
        if passed
        else "All fail conditions are non-mathematical (e.g. only time-based). "
             "The game never directly penalises wrong math — only slowness."
    )
    recommendation = (
        ""
        if passed
        else "Add at least one fail condition that triggers when the learner "
             "makes a mathematically incorrect choice — not only when time expires."
    )
    return PurityCheckResult(
        check_name="fail_conditions_mathematical",
        passed=passed,
        weight=1.0,
        detail=detail,
        recommendation=recommendation,
    )


def _check_reflection_beat_present(spec: LoopPuritySpec) -> PurityCheckResult:
    """
    A loop without any reflection beat cannot produce metacognitive learning.
    OS spec Rule D requires at least one reflection beat per level.
    Weight: 1.0
    """
    passed = spec.reflection_beat_present
    detail = (
        "At least one reflection beat is present in the loop."
        if passed
        else "No reflection beat is defined. The loop does not ask the learner "
             "to plan, monitor, or evaluate their own strategy."
    )
    recommendation = (
        ""
        if passed
        else "Add one short reflection prompt after a meaningful chunk of play. "
             "See the Reflection Prompt Bank in docs/os_spec_2026.md Section 4.2."
    )
    return PurityCheckResult(
        check_name="reflection_beat_present",
        passed=passed,
        weight=1.0,
        detail=detail,
        recommendation=recommendation,
    )


def _check_teacher_evidence_defined(spec: LoopPuritySpec) -> PurityCheckResult:
    """
    Teacher evidence is a 2026 Gate requirement (Approval Gate 7).
    Weight: 0.75 — advisory; does not compromise verdict alone.
    """
    passed = spec.teacher_evidence_defined
    detail = (
        "Teacher evidence outputs are defined."
        if passed
        else "No teacher evidence output is defined. Teachers cannot see where "
             "students are confused — this game is not classroom-ready."
    )
    recommendation = (
        ""
        if passed
        else "Define teacher_dashboard_outputs in the prototype spec. "
             "See artifacts/schemas/teacher_evidence_dashboard.schema.json."
    )
    return PurityCheckResult(
        check_name="teacher_evidence_defined",
        passed=passed,
        weight=0.75,
        detail=detail,
        recommendation=recommendation,
    )


# ─────────────────────────────────────────────────────────────────────────────
# Main audit function
# ─────────────────────────────────────────────────────────────────────────────

def audit_loop_purity(spec: LoopPuritySpec) -> LoopPurityReport:
    """
    Run all purity checks against spec and return a LoopPurityReport.

    Verdict thresholds:
        >= 0.85  → "pure"
        >= 0.60  → "advisory"
        < 0.60   → "compromised"
    """
    checks: List[PurityCheckResult] = [
        _check_math_is_core_action(spec),
        _check_success_requires_math(spec),
        _check_guessing_not_viable(spec),
        _check_error_detection_present(spec),
        _check_fail_conditions_are_mathematical(spec),
        _check_reflection_beat_present(spec),
        _check_teacher_evidence_defined(spec),
    ]

    total_weight  = sum(c.weight for c in checks)
    earned_weight = sum(c.weight for c in checks if c.passed)
    purity_score  = earned_weight / total_weight if total_weight > 0 else 0.0

    if purity_score >= VERDICT_PURE:
        verdict = "pure"
    elif purity_score >= VERDICT_ADVISORY:
        verdict = "advisory"
    else:
        verdict = "compromised"

    fail_conditions_found = [
        f"{c.check_name}: {c.recommendation}"
        for c in checks
        if not c.passed and c.weight >= 1.5  # only critical/major checks
    ]
    warnings = [
        f"{c.check_name}: {c.recommendation}"
        for c in checks
        if not c.passed and c.weight < 1.5
    ]

    return LoopPurityReport(
        game_name=spec.game_name,
        purity_score=round(purity_score, 4),
        verdict=verdict,
        checks=checks,
        fail_conditions_found=fail_conditions_found,
        warnings=warnings,
        passed_count=sum(1 for c in checks if c.passed),
        total_count=len(checks),
    )


# ─────────────────────────────────────────────────────────────────────────────
# Convenience: build a spec from a prototype_spec artifact dict
# ─────────────────────────────────────────────────────────────────────────────

def loop_purity_spec_from_prototype(artifact: Dict) -> LoopPuritySpec:
    """
    Build a LoopPuritySpec from a prototype_spec artifact dict.

    Fields not present in the artifact default to conservative values
    (bypass_path_exists=False, reflection_beat_present=False, etc.).
    """
    tp  = artifact.get("target_player", {})
    cl  = artifact.get("core_loop_translation", {})
    im  = artifact.get("interaction_model", {})
    ld  = artifact.get("learning_design", {})
    pr  = artifact.get("prototype_rules", {})
    ic  = artifact.get("interaction_constraints", {})

    return LoopPuritySpec(
        game_name=artifact.get("prototype_goal", "Unknown game")[:80],
        core_loop_sentence=artifact.get("core_loop_sentence", ""),
        math_action_mapping=im.get("math_action_mapping", ""),
        player_actions=[
            a for screen in artifact.get("screen_flow", [])
            for a in screen.get("player_actions", [])
        ],
        success_conditions=[cl.get("success_condition", "")],
        fail_conditions=[cl.get("fail_condition", "")],
        math_domain=tp.get("math_domain", ""),
        luck_skill_ratio=artifact.get("luck_skill_ratio", 0.5),
        guessing_surface=ic.get("selection_rule", ""),
        bypass_path_exists=False,  # must be set manually
        bypass_path_description="",
        error_categories_detectable=[
            e.get("category", "")
            for e in ld.get("error_category_map", [])
        ],
        reflection_beat_present=bool(ld.get("reflection_prompt_plan")),
        teacher_evidence_defined=bool(
            artifact.get("teacher_dashboard_outputs")
        ),
        error_handling_description=im.get("error_handling"),
        exact_match_required=ic.get("exact_match_required"),
    )


# ─────────────────────────────────────────────────────────────────────────────
# Quick smoke test — run directly with: python utils/loop_purity_auditor.py
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    _bakery_spec = LoopPuritySpec(
        game_name="Bakery Rush (Pass 2)",
        core_loop_sentence=(
            "Tap pastries whose values sum to the customer's target."
        ),
        math_action_mapping=(
            "Each tap adds the pastry's +N value to a running total; "
            "success requires the total to equal the target exactly."
        ),
        player_actions=[
            "tap pastry on belt",
            "observe running total",
            "observe overshoot feedback",
        ],
        success_conditions=[
            "running total equals target exactly",
        ],
        fail_conditions=[
            "patience timer expires",
            "running total exceeds target (auto-corrected, resets last item)",
        ],
        math_domain="Addition / additive decomposition",
        luck_skill_ratio=0.75,
        guessing_surface=(
            "belt items labeled with +N values visible before tap; "
            "player can plan before acting"
        ),
        bypass_path_exists=False,
        bypass_path_description="",
        error_categories_detectable=[
            "impulsive_guess",
            "procedure_slip",
            "concept_confusion",
        ],
        reflection_beat_present=False,   # not yet in pass-2
        teacher_evidence_defined=False,  # diagnostics shown but not structured
    )

    report = audit_loop_purity(_bakery_spec)

    print(f"\n{'='*60}")
    print(f"  Loop Purity Audit: {report.game_name}")
    print(f"  Score:   {report.purity_score:.4f}")
    print(f"  Verdict: {report.verdict.upper()}")
    print(f"  Passed:  {report.passed_count}/{report.total_count} checks")
    print(f"{'='*60}")
    for c in report.checks:
        status = "✓" if c.passed else "✗"
        print(f"  {status} [{c.weight:.1f}x] {c.check_name}")
        print(f"         {c.detail}")
        if not c.passed:
            print(f"         → {c.recommendation}")
    if report.fail_conditions_found:
        print(f"\n  FAIL CONDITIONS (major):")
        for f in report.fail_conditions_found:
            print(f"    • {f}")
    if report.warnings:
        print(f"\n  WARNINGS (minor):")
        for w in report.warnings:
            print(f"    • {w}")
    print()
