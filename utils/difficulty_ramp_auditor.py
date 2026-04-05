"""
Difficulty Ramp Auditor — Math Game Studio OS
utils/difficulty_ramp_auditor.py

Checks whether a game's level progression:
  1. Gives Level 1 a genuine teaching window before pressure becomes meaningful
  2. Increases difficulty smoothly — no spikes between consecutive levels
  3. Does not stay flat so long that the player disengages

Proof case: Bakery Rush Pass 1
  Original beltDuration: [5, 4, 3, 2.5, 2]  → Level 1 too fast, L1→L2 spike
  Fixed beltDuration:    [9, 4, 3, 2.5, 2]  → Level 1 ok, but L1→L2 still 56% spike
  Ideal beltDuration:    [9, 6, 4, 3, 2]    → smooth ramp all the way

The system learns from this:
  - Teaching parameters at Level 1 need explicit thresholds per parameter type
  - Step sizes between levels need a max-cap rule
  - These rules belong in a utility that all future games can run against

Usage:
    from utils.difficulty_ramp_auditor import (
        ParameterConfig, audit_parameter, audit_game_ramp,
        BAKERY_PARAMETER_CONFIGS, audit_bakery_level_configs,
    )

    # From a prototype_spec artifact:
    audit = audit_from_prototype_spec(
        game_name="Bakery Rush",
        parameter_values={"beltDuration": [9,6,4,3,2], "patience": [20,18,15,12,10]},
        spec=json.load(open("artifacts/bakery_prototype_spec.json")),
        fallback_configs=BAKERY_PARAMETER_CONFIGS,  # used when spec has no parameters section
    )
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Sequence


# ---------------------------------------------------------------------------
# Configuration types
# ---------------------------------------------------------------------------

@dataclass
class ParameterConfig:
    """
    Describes one level-progression parameter and the thresholds used to audit it.

    Attributes:
        name:                    Human-readable parameter name (e.g. "beltDuration").
        direction:               "lower_is_harder" — values decrease as difficulty rises
                                 (belt speed, patience, time limit).
                                 "higher_is_harder" — values increase as difficulty rises
                                 (target max, demand range max, number of options).
        unit:                    Display unit for output (e.g. "s", "units", "").
        level_1_teaching_min:    Minimum value at Level 1 for "lower_is_harder" params.
                                 Level 1 should be AT OR ABOVE this to qualify as teaching.
        level_1_teaching_max:    Maximum value at Level 1 for "higher_is_harder" params.
                                 Level 1 should be AT OR BELOW this to qualify as teaching.
        max_step_pct:            Maximum allowed percentage change between consecutive levels
                                 before the transition is flagged as a spike. Default 35%.
        min_step_pct:            Minimum percentage change per level step before it's
                                 flagged as flat. Default 3%. Flat spans across 3+ consecutive
                                 levels are flagged as a design smell.
        weight:                  Relative importance when computing the overall audit verdict.
                                 1.0 = normal, 2.0 = critical.
    """
    name: str
    direction: str                          # "lower_is_harder" | "higher_is_harder"
    unit: str = ""
    level_1_teaching_min: Optional[float] = None   # used when direction == "lower_is_harder"
    level_1_teaching_max: Optional[float] = None   # used when direction == "higher_is_harder"
    max_step_pct: float = 35.0             # flag as spike above this %
    min_step_pct: float = 3.0              # flag as flat below this %
    weight: float = 1.0


# ---------------------------------------------------------------------------
# Report types
# ---------------------------------------------------------------------------

@dataclass
class LevelTransition:
    """Data for one level-to-level step in a parameter's progression."""
    from_level: int                         # 1-indexed (1 = L1, 2 = L2, ...)
    to_level: int
    from_value: float
    to_value: float
    step_pct: float                         # absolute % change
    verdict: str                            # "smooth" | "spike" | "flat" | "reversed"
    reason: str


@dataclass
class ParameterRampReport:
    """Full audit result for one parameter across all levels."""
    parameter: str
    unit: str
    direction: str
    values: List[float]
    level_1_value: float
    level_1_verdict: str                    # "teaching" | "warning" | "flag"
    level_1_reason: str
    transitions: List[LevelTransition]
    spike_transitions: List[int]           # from_level indices of spike transitions
    flat_spans: List[tuple]                # (from_level, to_level) spans of flatness
    curve_type: str                        # "smooth_ramp" | "spike" | "flat" | "mixed" | "single_level"
    is_teaching_friendly: bool
    recommendations: List[str]
    severity_score: float = 0.0


@dataclass
class GameRampAudit:
    """Full ramp audit result across all declared parameters."""
    game_name: str
    level_count: int
    parameter_reports: List[ParameterRampReport]
    is_fully_teaching_friendly: bool
    flagged_parameters: List[str]          # parameter names with flag-level issues
    warned_parameters: List[str]           # parameter names with warnings
    curve_verdict: str                     # "smooth_ramp" | "spike" | "mixed" | "flat"
    weighted_severity: float               # 0.0 = all clean, 1.0 = worst possible
    severity_label: str                    # "clean" | "advisory" | "concern" | "flag"
    summary: str
    recommendations: List[str]             # deduplicated across all parameters


# ---------------------------------------------------------------------------
# Last-resort fallback configs
#
# These are used ONLY when audit_bakery_level_configs() is called without a
# prototype_spec artifact, or when the spec lacks difficulty_profile.parameters.
#
# PRIMARY AUTHORITY: the difficulty_profile.parameters block inside the game's
# prototype_spec artifact (e.g. memory/job_workspaces/.../prototype_spec.v1.json).
# These defaults exist so the convenience wrapper degrades gracefully when no
# spec is available — they are NOT the design source of truth.
#
# Proof: audit_from_prototype_spec() with the Bakery spec produces identical
# results to audit_bakery_level_configs(), confirming the spec is authoritative.
# ---------------------------------------------------------------------------

BAKERY_PARAMETER_CONFIGS: List[ParameterConfig] = [
    ParameterConfig(
        name="beltDuration",
        direction="lower_is_harder",
        unit="s",
        level_1_teaching_min=7.0,           # mirrors difficulty_profile.parameters in Bakery spec
        max_step_pct=35.0,
        min_step_pct=5.0,
        weight=2.0,
    ),
    ParameterConfig(
        name="patience",
        direction="lower_is_harder",
        unit="s",
        level_1_teaching_min=15.0,          # mirrors difficulty_profile.parameters in Bakery spec
        max_step_pct=30.0,
        min_step_pct=5.0,
        weight=1.5,
    ),
    ParameterConfig(
        name="targetPoolMax",
        direction="higher_is_harder",
        unit="",
        level_1_teaching_max=10.0,          # mirrors difficulty_profile.parameters in Bakery spec
        max_step_pct=40.0,
        min_step_pct=5.0,
        weight=1.0,
    ),
]

FIRE_DISPATCH_PARAMETER_CONFIGS: List[ParameterConfig] = [
    ParameterConfig(
        name="timeLimit",
        direction="lower_is_harder",
        unit="s",
        level_1_teaching_min=20.0,
        max_step_pct=30.0,
        min_step_pct=5.0,
        weight=2.0,
    ),
    ParameterConfig(
        name="demandRangeMax",
        direction="higher_is_harder",
        unit="",
        level_1_teaching_max=10.0,
        max_step_pct=40.0,
        min_step_pct=5.0,
        weight=1.0,
    ),
]


# ---------------------------------------------------------------------------
# Core audit logic
# ---------------------------------------------------------------------------

def _pct_change(from_val: float, to_val: float) -> float:
    """Absolute percentage change from from_val to to_val."""
    if from_val == 0:
        return 0.0
    return abs(to_val - from_val) / abs(from_val) * 100.0


def _transition_verdict(
    step_pct: float,
    from_val: float,
    to_val: float,
    config: ParameterConfig,
) -> tuple[str, str]:
    """
    Return (verdict, reason) for a single level transition.
    verdict: "smooth" | "spike" | "flat" | "reversed"
    """
    # Check if difficulty moved in the wrong direction
    if config.direction == "lower_is_harder" and to_val > from_val:
        return ("reversed", f"Value increased {from_val}{config.unit} → {to_val}{config.unit} "
                            f"but should decrease for higher difficulty.")
    if config.direction == "higher_is_harder" and to_val < from_val:
        return ("reversed", f"Value decreased {from_val}{config.unit} → {to_val}{config.unit} "
                            f"but should increase for higher difficulty.")

    if step_pct < config.min_step_pct:
        return ("flat", f"Step of {step_pct:.1f}% is below the {config.min_step_pct}% minimum — "
                        f"difficulty barely changes here.")
    if step_pct > config.max_step_pct:
        return ("spike", f"Step of {step_pct:.1f}% exceeds the {config.max_step_pct}% max — "
                         f"too large a jump from Level {'->'} next level.")
    return ("smooth", f"Step of {step_pct:.1f}% is within the smooth-ramp range "
                      f"({config.min_step_pct}%–{config.max_step_pct}%).")


def _compute_severity_score(report: "ParameterRampReport") -> float:
    """
    Compute a severity score in [0.0, 1.0] for a single parameter report.

    - L1 flag:      +0.6
    - L1 warning:   +0.2
    - Each spike at L1→L2 (spike_at == 1): +0.4
    - Each later spike:                     +0.2
    - Each flat span of length >= 2:        +0.1
    """
    score = 0.0
    if report.level_1_verdict == "flag":
        score += 0.6
    elif report.level_1_verdict == "warning":
        score += 0.2
    for spike_at in report.spike_transitions:
        if spike_at == 1:
            score += 0.4
        else:
            score += 0.2
    for span in report.flat_spans:
        if span[1] - span[0] >= 2:
            score += 0.1
    return min(score, 1.0)


def audit_parameter(
    values: Sequence[float],
    config: ParameterConfig,
) -> ParameterRampReport:
    """
    Audit a single parameter's progression across levels.

    Args:
        values:  One value per level, in order (index 0 = Level 1).
        config:  ParameterConfig describing thresholds and direction.

    Returns:
        ParameterRampReport with full analysis.
    """
    values_list = list(values)
    if not values_list:
        return ParameterRampReport(
            parameter=config.name, unit=config.unit, direction=config.direction,
            values=[], level_1_value=0, level_1_verdict="flag",
            level_1_reason="No values provided.",
            transitions=[], spike_transitions=[], flat_spans=[],
            curve_type="single_level", is_teaching_friendly=False,
            recommendations=["Provide level values for this parameter."],
        )

    level_1 = values_list[0]
    recommendations: List[str] = []

    # ── Level 1 teaching check ──
    if config.direction == "lower_is_harder":
        threshold = config.level_1_teaching_min
        if threshold is None:
            l1_verdict, l1_reason = "acceptable", "No teaching threshold defined."
        elif level_1 >= threshold:
            l1_verdict = "teaching"
            l1_reason = (f"Level 1 value {level_1}{config.unit} meets the "
                         f"teaching minimum of {threshold}{config.unit}.")
        elif level_1 >= threshold * 0.8:
            l1_verdict = "warning"
            l1_reason = (f"Level 1 value {level_1}{config.unit} is below the "
                         f"teaching minimum of {threshold}{config.unit} but within 80%.")
            recommendations.append(
                f"Consider raising {config.name} at Level 1 to at least {threshold}{config.unit}."
            )
        else:
            l1_verdict = "flag"
            l1_reason = (f"Level 1 value {level_1}{config.unit} is well below the "
                         f"teaching minimum of {threshold}{config.unit}. "
                         f"Players cannot learn the loop under this much pressure.")
            recommendations.append(
                f"Raise {config.name} at Level 1 to at least {threshold}{config.unit}. "
                f"Level 1 should optimize for comprehension, not challenge."
            )
    else:  # higher_is_harder
        threshold = config.level_1_teaching_max
        if threshold is None:
            l1_verdict, l1_reason = "acceptable", "No teaching threshold defined."
        elif level_1 <= threshold:
            l1_verdict = "teaching"
            l1_reason = (f"Level 1 value {level_1}{config.unit} meets the "
                         f"teaching maximum of {threshold}{config.unit}.")
        elif level_1 <= threshold * 1.25:
            l1_verdict = "warning"
            l1_reason = (f"Level 1 value {level_1}{config.unit} slightly exceeds the "
                         f"teaching maximum of {threshold}{config.unit}.")
            recommendations.append(
                f"Consider lowering {config.name} at Level 1 to at most {threshold}{config.unit}."
            )
        else:
            l1_verdict = "flag"
            l1_reason = (f"Level 1 value {level_1}{config.unit} significantly exceeds the "
                         f"teaching maximum of {threshold}{config.unit}.")
            recommendations.append(
                f"Lower {config.name} at Level 1 to at most {threshold}{config.unit}."
            )

    # ── Transition analysis ──
    transitions: List[LevelTransition] = []
    spike_transitions: List[int] = []
    flat_from: Optional[int] = None
    flat_spans: List[tuple] = []

    for i in range(len(values_list) - 1):
        from_val = values_list[i]
        to_val = values_list[i + 1]
        step_pct = _pct_change(from_val, to_val)
        verdict, reason = _transition_verdict(step_pct, from_val, to_val, config)

        # Fill in level numbers in reason
        reason = reason.replace("Level '->'\nnext level", f"Level {i + 1} → Level {i + 2}")

        transition = LevelTransition(
            from_level=i + 1, to_level=i + 2,
            from_value=from_val, to_value=to_val,
            step_pct=step_pct,
            verdict=verdict, reason=reason,
        )
        transitions.append(transition)

        if verdict == "spike":
            spike_transitions.append(i + 1)  # from_level
            safe_step = config.max_step_pct / 100.0
            if config.direction == "lower_is_harder":
                suggested = round(from_val * (1.0 - safe_step), 1)
                recommendations.append(
                    f"{config.name} L{i + 1}→L{i + 2}: drop of {step_pct:.0f}% is too large. "
                    f"Consider {suggested}{config.unit} at Level {i + 2} "
                    f"(≤{config.max_step_pct:.0f}% step from {from_val}{config.unit})."
                )
            else:
                suggested = round(from_val * (1.0 + safe_step), 1)
                recommendations.append(
                    f"{config.name} L{i + 1}→L{i + 2}: jump of {step_pct:.0f}% is too large. "
                    f"Consider {suggested}{config.unit} at Level {i + 2} "
                    f"(≤{config.max_step_pct:.0f}% step from {from_val}{config.unit})."
                )

        # Flat span tracking
        if verdict == "flat":
            if flat_from is None:
                flat_from = i + 1
        else:
            if flat_from is not None:
                flat_spans.append((flat_from, i + 1))
                flat_from = None
    if flat_from is not None:
        flat_spans.append((flat_from, len(values_list)))

    if flat_spans:
        for span in flat_spans:
            if span[1] - span[0] >= 2:
                recommendations.append(
                    f"{config.name} is flat across Levels {span[0]}–{span[1] + 1}. "
                    "Players disengage when difficulty stagnates. "
                    "Introduce a meaningful step here."
                )

    # ── Curve type ──
    if len(values_list) == 1:
        curve_type = "single_level"
    elif spike_transitions:
        curve_type = "spike" if len(spike_transitions) == len(transitions) else "mixed"
    elif flat_spans and sum(s[1] - s[0] for s in flat_spans) > len(transitions) // 2:
        curve_type = "flat"
    else:
        curve_type = "smooth_ramp"

    is_teaching_friendly = (l1_verdict == "teaching") and (not spike_transitions or spike_transitions[0] > 1)

    # ── Severity score ──
    _sev = 0.0
    if l1_verdict == "flag":
        _sev += 0.6
    elif l1_verdict == "warning":
        _sev += 0.2
    for spike_at in spike_transitions:
        _sev += 0.4 if spike_at == 1 else 0.2
    for span in flat_spans:
        if span[1] - span[0] >= 2:
            _sev += 0.1
    severity_score = min(_sev, 1.0)

    return ParameterRampReport(
        parameter=config.name,
        unit=config.unit,
        direction=config.direction,
        values=values_list,
        level_1_value=level_1,
        level_1_verdict=l1_verdict,
        level_1_reason=l1_reason,
        transitions=transitions,
        spike_transitions=spike_transitions,
        flat_spans=flat_spans,
        curve_type=curve_type,
        is_teaching_friendly=is_teaching_friendly,
        recommendations=recommendations,
        severity_score=severity_score,
    )


def audit_game_ramp(
    game_name: str,
    parameter_values: Dict[str, Sequence[float]],
    parameter_configs: List[ParameterConfig],
) -> GameRampAudit:
    """
    Audit the full difficulty ramp for a game across all declared parameters.

    Args:
        game_name:          Display name for the game.
        parameter_values:   Dict mapping parameter name → list of values per level.
        parameter_configs:  List of ParameterConfig objects, one per parameter.

    Returns:
        GameRampAudit with cross-parameter summary and recommendations.
    """
    reports: List[ParameterRampReport] = []
    all_recommendations: List[str] = []
    flagged: List[str] = []
    warned: List[str] = []
    level_count = max((len(v) for v in parameter_values.values()), default=0)

    for config in parameter_configs:
        vals = parameter_values.get(config.name, [])
        report = audit_parameter(vals, config)
        reports.append(report)
        all_recommendations.extend(report.recommendations)
        if report.level_1_verdict == "flag" or report.spike_transitions:
            flagged.append(config.name)
        elif report.level_1_verdict == "warning":
            warned.append(config.name)

    # Overall curve verdict
    has_spikes = any(r.spike_transitions for r in reports)
    all_smooth = all(r.curve_type == "smooth_ramp" for r in reports if r.values)
    all_flat = all(r.curve_type == "flat" for r in reports if r.values)
    if all_smooth:
        curve_verdict = "smooth_ramp"
    elif all_flat:
        curve_verdict = "flat"
    elif has_spikes:
        curve_verdict = "spike" if not all_smooth else "mixed"
    else:
        curve_verdict = "mixed"

    is_fully_teaching_friendly = (not flagged) and all(r.is_teaching_friendly for r in reports)

    # Summary
    if is_fully_teaching_friendly:
        summary = (f"{game_name}: all {len(reports)} parameter(s) pass teaching-first checks "
                   f"with a {curve_verdict} difficulty curve across {level_count} levels.")
    else:
        summary = (
            f"{game_name}: {len(flagged)} parameter(s) flagged ({', '.join(flagged) or 'none'}), "
            f"{len(warned)} warned ({', '.join(warned) or 'none'}). "
            f"Curve type: {curve_verdict}."
        )

    # Deduplicate recommendations (preserve order)
    seen: set = set()
    unique_recs: List[str] = []
    for rec in all_recommendations:
        if rec not in seen:
            seen.add(rec)
            unique_recs.append(rec)

    # Weighted severity
    total_weight = sum(c.weight for c in parameter_configs)
    if total_weight > 0:
        weighted_severity = sum(
            r.severity_score * c.weight
            for r, c in zip(reports, parameter_configs)
        ) / total_weight
    else:
        weighted_severity = 0.0

    if weighted_severity == 0.0:
        severity_label = "clean"
    elif weighted_severity <= 0.25:
        severity_label = "advisory"
    elif weighted_severity <= 0.5:
        severity_label = "concern"
    else:
        severity_label = "flag"

    return GameRampAudit(
        game_name=game_name,
        level_count=level_count,
        parameter_reports=reports,
        is_fully_teaching_friendly=is_fully_teaching_friendly,
        flagged_parameters=flagged,
        warned_parameters=warned,
        curve_verdict=curve_verdict,
        weighted_severity=weighted_severity,
        severity_label=severity_label,
        summary=summary,
        recommendations=unique_recs,
    )


# ---------------------------------------------------------------------------
# Spec-driven entry point
# ---------------------------------------------------------------------------

def audit_from_prototype_spec(
    game_name: str,
    parameter_values: Dict[str, Sequence[float]],
    spec: Dict[str, Any],
    fallback_configs: Optional[List[ParameterConfig]] = None,
) -> GameRampAudit:
    """
    Run the ramp audit using thresholds declared in a prototype_spec artifact.

    Reads difficulty_profile.parameters from the spec dict. If that key is
    absent or empty, falls back to fallback_configs. If fallback_configs is
    also None, raises ValueError with a clear message.

    Args:
        game_name:         Display name for the game.
        parameter_values:  Dict mapping parameter name → list of values per level.
        spec:              A prototype_spec artifact dict (parsed JSON).
        fallback_configs:  Optional list of ParameterConfig to use when the spec
                           does not declare difficulty_profile.parameters.

    Returns:
        GameRampAudit — identical structure to audit_game_ramp() output.

    Example:
        import json
        spec = json.load(open("artifacts/bakery_prototype_spec.json"))
        audit = audit_from_prototype_spec(
            game_name="Bakery Rush",
            parameter_values={"beltDuration": [9, 6, 4, 3, 2], ...},
            spec=spec,
            fallback_configs=BAKERY_PARAMETER_CONFIGS,
        )
    """
    diff_profile = spec.get("difficulty_profile", {})
    param_specs = diff_profile.get("parameters") or []

    if param_specs:
        configs: List[ParameterConfig] = []
        for p in param_specs:
            configs.append(ParameterConfig(
                name=p["name"],
                direction=p["direction"],
                unit=p.get("unit", ""),
                level_1_teaching_min=p.get("level_1_teaching_min"),
                level_1_teaching_max=p.get("level_1_teaching_max"),
                max_step_pct=p.get("max_step_pct", 35.0),
                min_step_pct=p.get("min_step_pct", 3.0),
                weight=p.get("weight", 1.0),
            ))
    elif fallback_configs is not None:
        configs = list(fallback_configs)
    else:
        raise ValueError(
            f"No difficulty_profile.parameters found in spec for '{game_name}', "
            "and no fallback_configs provided. Add a 'parameters' array to "
            "difficulty_profile in the prototype_spec artifact, or pass fallback_configs."
        )

    return audit_game_ramp(game_name, parameter_values, configs)


# ---------------------------------------------------------------------------
# Bakery convenience wrapper
#
# Handles Bakery-schema extraction (beltDuration, patience, max(targetPool))
# and delegates to audit_from_prototype_spec() with BAKERY_PARAMETER_CONFIGS
# as a last-resort fallback.
#
# Preferred call pattern (spec as primary authority):
#
#     import json
#     spec = json.load(open("memory/job_workspaces/<job_id>/prototype_spec.v1.json"))
#     audit = audit_bakery_level_configs(level_configs, spec=spec)
#
# Fallback call pattern (no spec available):
#
#     audit = audit_bakery_level_configs(level_configs)
#     # Uses BAKERY_PARAMETER_CONFIGS defaults — thresholds not sourced from any artifact.
# ---------------------------------------------------------------------------

def audit_bakery_level_configs(
    level_configs: List[Dict[str, Any]],
    spec: Optional[Dict[str, Any]] = None,
) -> GameRampAudit:
    """
    Convenience wrapper: audit Bakery LEVEL_CONFIGS directly.

    Extracts beltDuration, patience, and max(targetPool) from the Bakery
    level config schema, then delegates entirely to audit_from_prototype_spec().

    Thresholds are sourced from (in priority order):
      1. spec["difficulty_profile"]["parameters"]  — artifact, primary authority
      2. BAKERY_PARAMETER_CONFIGS                  — fallback defaults, last resort

    Args:
        level_configs:  List of Bakery level dicts, each containing at minimum
                        "beltDuration" (float), "patience" (float),
                        "targetPool" (List[int]).
        spec:           Parsed prototype_spec artifact dict. When provided and
                        the spec contains difficulty_profile.parameters, those
                        thresholds are used instead of the hardcoded fallback.
                        Pass None to use BAKERY_PARAMETER_CONFIGS as fallback.

    Returns:
        GameRampAudit — full advisory report, never blocking.
    """
    belt_durations   = [c["beltDuration"]   for c in level_configs]
    patiences        = [c["patience"]        for c in level_configs]
    target_pool_maxs = [max(c["targetPool"]) for c in level_configs]

    param_values = {
        "beltDuration":  belt_durations,
        "patience":      patiences,
        "targetPoolMax": target_pool_maxs,
    }

    if spec is not None:
        return audit_from_prototype_spec(
            game_name="Bakery Rush",
            parameter_values=param_values,
            spec=spec,
            fallback_configs=BAKERY_PARAMETER_CONFIGS,
        )

    # No spec provided — use last-resort fallback configs directly.
    return audit_game_ramp(
        game_name="Bakery Rush",
        parameter_values=param_values,
        parameter_configs=BAKERY_PARAMETER_CONFIGS,
    )
