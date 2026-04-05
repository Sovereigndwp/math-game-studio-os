"""
Tests for utils/difficulty_ramp_auditor.py

Proof case: Bakery Rush Pass 1

Three ramp variants are tested explicitly:

  ORIGINAL (buggy):
    beltDuration [5, 4, 3, 2.5, 2]
    → Level 1 too fast (5s < 7s teaching min) → flag
    → L1→L2 step 20% → acceptable
    → Overall: Level 1 failure dominates

  CURRENT (after Level 1 fix):
    beltDuration [9, 4, 3, 2.5, 2]
    → Level 1 ok (9s ≥ 7s teaching min) → teaching
    → L1→L2 step 55.6% → spike
    → is_teaching_friendly: False (early spike)

  IDEAL (recommended after auditor output):
    beltDuration [9, 6, 4, 3, 2]
    → Level 1 ok → teaching
    → Steps: 33.3%, 33.3%, 25%, 33.3% — all within 35% max
    → is_teaching_friendly: True
"""

import pytest
from utils.difficulty_ramp_auditor import (
    ParameterConfig,
    GameRampAudit,
    ParameterRampReport,
    audit_parameter,
    audit_game_ramp,
    audit_bakery_level_configs,
    BAKERY_PARAMETER_CONFIGS,
)


# ---------------------------------------------------------------------------
# Bakery beltDuration — three ramp variants
# ---------------------------------------------------------------------------

BELT_CONFIG = ParameterConfig(
    name="beltDuration",
    direction="lower_is_harder",
    unit="s",
    level_1_teaching_min=7.0,
    max_step_pct=35.0,
    min_step_pct=5.0,
    weight=2.0,
)


class TestBeltDurationOriginalBug:
    """beltDuration [5, 4, 3, 2.5, 2] — original before Level 1 fix."""

    def test_level_1_is_flagged(self):
        report = audit_parameter([5, 4, 3, 2.5, 2], BELT_CONFIG)
        assert report.level_1_verdict == "flag"
        assert "5.0" in report.level_1_reason or "5" in report.level_1_reason

    def test_not_teaching_friendly(self):
        report = audit_parameter([5, 4, 3, 2.5, 2], BELT_CONFIG)
        assert report.is_teaching_friendly is False

    def test_recommendations_include_level_1_fix(self):
        report = audit_parameter([5, 4, 3, 2.5, 2], BELT_CONFIG)
        assert any("Level 1" in r and "7" in r for r in report.recommendations)

    def test_curve_type_mixed_or_spike(self):
        report = audit_parameter([5, 4, 3, 2.5, 2], BELT_CONFIG)
        assert report.curve_type in ("smooth_ramp", "mixed", "spike")


class TestBeltDurationCurrentFixed:
    """beltDuration [9, 4, 3, 2.5, 2] — after Level 1 fix but L1→L2 spike remains."""

    def test_level_1_is_teaching(self):
        report = audit_parameter([9, 4, 3, 2.5, 2], BELT_CONFIG)
        assert report.level_1_verdict == "teaching"

    def test_l1_to_l2_is_spike(self):
        report = audit_parameter([9, 4, 3, 2.5, 2], BELT_CONFIG)
        # 9→4 = 55.6% drop > 35% max → spike
        assert 1 in report.spike_transitions

    def test_not_teaching_friendly_due_to_early_spike(self):
        """Level 1 is ok but L1→L2 spike makes it not teaching-friendly overall."""
        report = audit_parameter([9, 4, 3, 2.5, 2], BELT_CONFIG)
        assert report.is_teaching_friendly is False

    def test_later_transitions_are_smooth(self):
        report = audit_parameter([9, 4, 3, 2.5, 2], BELT_CONFIG)
        # L2→L3: 25%, L3→L4: 16.7%, L4→L5: 20% — all smooth
        for t in report.transitions[1:]:
            assert t.verdict in ("smooth", "flat"), (
                f"Expected smooth after L1→L2, got {t.verdict} at L{t.from_level}→L{t.to_level}"
            )

    def test_recommendation_suggests_intermediate_level_2(self):
        report = audit_parameter([9, 4, 3, 2.5, 2], BELT_CONFIG)
        assert any("L1→L2" in r or "L1" in r for r in report.recommendations)

    def test_step_size_computed_correctly(self):
        report = audit_parameter([9, 4, 3, 2.5, 2], BELT_CONFIG)
        l1_to_l2 = report.transitions[0]
        assert abs(l1_to_l2.step_pct - 55.6) < 1.0


class TestBeltDurationIdeal:
    """beltDuration [9, 6, 4, 3, 2] — fully smooth after auditor recommendation."""

    def test_level_1_is_teaching(self):
        report = audit_parameter([9, 6, 4, 3, 2], BELT_CONFIG)
        assert report.level_1_verdict == "teaching"

    def test_no_spikes(self):
        report = audit_parameter([9, 6, 4, 3, 2], BELT_CONFIG)
        assert report.spike_transitions == []

    def test_is_teaching_friendly(self):
        report = audit_parameter([9, 6, 4, 3, 2], BELT_CONFIG)
        assert report.is_teaching_friendly is True

    def test_curve_type_smooth_ramp(self):
        report = audit_parameter([9, 6, 4, 3, 2], BELT_CONFIG)
        assert report.curve_type == "smooth_ramp"

    def test_all_transitions_smooth(self):
        report = audit_parameter([9, 6, 4, 3, 2], BELT_CONFIG)
        for t in report.transitions:
            assert t.verdict == "smooth", (
                f"Expected smooth, got {t.verdict} at L{t.from_level}→L{t.to_level} "
                f"(step {t.step_pct:.1f}%)"
            )

    def test_no_recommendations_needed(self):
        report = audit_parameter([9, 6, 4, 3, 2], BELT_CONFIG)
        assert report.recommendations == []


# ---------------------------------------------------------------------------
# Bakery patience — already smooth
# ---------------------------------------------------------------------------

PATIENCE_CONFIG = ParameterConfig(
    name="patience",
    direction="lower_is_harder",
    unit="s",
    level_1_teaching_min=15.0,
    max_step_pct=30.0,
    min_step_pct=5.0,
    weight=1.5,
)


class TestPatienceCurrentConfig:
    """patience [20, 18, 15, 12, 10] — already a smooth ramp."""

    def test_level_1_is_teaching(self):
        report = audit_parameter([20, 18, 15, 12, 10], PATIENCE_CONFIG)
        assert report.level_1_verdict == "teaching"

    def test_no_spikes(self):
        report = audit_parameter([20, 18, 15, 12, 10], PATIENCE_CONFIG)
        assert report.spike_transitions == []

    def test_is_teaching_friendly(self):
        report = audit_parameter([20, 18, 15, 12, 10], PATIENCE_CONFIG)
        assert report.is_teaching_friendly is True

    def test_curve_type_smooth(self):
        report = audit_parameter([20, 18, 15, 12, 10], PATIENCE_CONFIG)
        assert report.curve_type == "smooth_ramp"


# ---------------------------------------------------------------------------
# Bakery targetPoolMax — current config has an early spike
# ---------------------------------------------------------------------------

TARGET_CONFIG = ParameterConfig(
    name="targetPoolMax",
    direction="higher_is_harder",
    unit="",
    level_1_teaching_max=10.0,
    max_step_pct=40.0,
    min_step_pct=5.0,
    weight=1.0,
)


class TestTargetPoolMax:
    """
    targetPoolMax values extracted from LEVEL_CONFIGS:
    [8, 12, 15, 18, 20]
    L1→L2: (12-8)/8 = 50% → spike (> 40% max)
    """

    def test_level_1_is_teaching(self):
        # max 8 ≤ 10 threshold → teaching
        report = audit_parameter([8, 12, 15, 18, 20], TARGET_CONFIG)
        assert report.level_1_verdict == "teaching"

    def test_l1_to_l2_is_spike(self):
        # 8→12 = 50% jump > 40% max
        report = audit_parameter([8, 12, 15, 18, 20], TARGET_CONFIG)
        assert 1 in report.spike_transitions

    def test_later_transitions_smooth(self):
        report = audit_parameter([8, 12, 15, 18, 20], TARGET_CONFIG)
        # 12→15=25%, 15→18=20%, 18→20=11% — all smooth
        for t in report.transitions[1:]:
            assert t.verdict in ("smooth", "flat")

    def test_recommendation_for_level_2(self):
        report = audit_parameter([8, 12, 15, 18, 20], TARGET_CONFIG)
        assert any("L1→L2" in r or "L2" in r for r in report.recommendations)


# ---------------------------------------------------------------------------
# Full Bakery audit via convenience function
# ---------------------------------------------------------------------------

BAKERY_LEVEL_CONFIGS_CURRENT = [
    {"beltDuration": 9,   "targetPool": [4,5,6,7,8],         "patience": 20, "scoreThreshold": 30  },
    {"beltDuration": 4,   "targetPool": [5,6,7,8,10,12],     "patience": 18, "scoreThreshold": 70  },
    {"beltDuration": 3,   "targetPool": [5,7,9,12,15],        "patience": 15, "scoreThreshold": 120 },
    {"beltDuration": 2.5, "targetPool": [6,8,10,14,18],       "patience": 12, "scoreThreshold": 180 },
    {"beltDuration": 2,   "targetPool": [8,10,12,16,20],      "patience": 10, "scoreThreshold": 9999},
]

BAKERY_LEVEL_CONFIGS_ORIGINAL = [
    {"beltDuration": 5,   "targetPool": [4,5,6,7,8],         "patience": 20, "scoreThreshold": 30  },
    {"beltDuration": 4,   "targetPool": [5,6,7,8,10,12],     "patience": 18, "scoreThreshold": 70  },
    {"beltDuration": 3,   "targetPool": [5,7,9,12,15],        "patience": 15, "scoreThreshold": 120 },
    {"beltDuration": 2.5, "targetPool": [6,8,10,14,18],       "patience": 12, "scoreThreshold": 180 },
    {"beltDuration": 2,   "targetPool": [8,10,12,16,20],      "patience": 10, "scoreThreshold": 9999},
]

BAKERY_LEVEL_CONFIGS_IDEAL = [
    # beltDuration: 9→6→4→3→2  (steps: 33%, 33%, 25%, 33% — all ≤35%)
    # patience:     20→17→14→11→9 (steps: 15%, 18%, 21%, 18% — all ≤30%)
    # targetPoolMax: 8→10→12→15→18 (steps: 25%, 20%, 25%, 20% — all ≤40%)
    {"beltDuration": 9,   "targetPool": [4,5,6,7,8],         "patience": 20, "scoreThreshold": 30  },
    {"beltDuration": 6,   "targetPool": [5,6,7,8,9,10],      "patience": 17, "scoreThreshold": 70  },
    {"beltDuration": 4,   "targetPool": [5,7,9,10,12],       "patience": 14, "scoreThreshold": 120 },
    {"beltDuration": 3,   "targetPool": [6,8,10,12,15],      "patience": 11, "scoreThreshold": 180 },
    {"beltDuration": 2,   "targetPool": [7,9,11,14,18],      "patience": 9,  "scoreThreshold": 9999},
]


class TestFullBakeryAudit:

    def test_original_config_is_not_teaching_friendly(self):
        audit = audit_bakery_level_configs(BAKERY_LEVEL_CONFIGS_ORIGINAL)
        assert audit.is_fully_teaching_friendly is False
        assert "beltDuration" in audit.flagged_parameters

    def test_current_config_still_has_flags(self):
        """After Level 1 fix, beltDuration L1→L2 spike and targetPoolMax L1→L2 spike remain."""
        audit = audit_bakery_level_configs(BAKERY_LEVEL_CONFIGS_CURRENT)
        assert audit.is_fully_teaching_friendly is False
        assert "beltDuration" in audit.flagged_parameters
        assert "targetPoolMax" in audit.flagged_parameters

    def test_current_config_patience_is_clean(self):
        audit = audit_bakery_level_configs(BAKERY_LEVEL_CONFIGS_CURRENT)
        patience_report = next(r for r in audit.parameter_reports if r.parameter == "patience")
        assert patience_report.is_teaching_friendly is True
        assert patience_report.spike_transitions == []

    def test_ideal_config_is_teaching_friendly(self):
        audit = audit_bakery_level_configs(BAKERY_LEVEL_CONFIGS_IDEAL)
        assert audit.is_fully_teaching_friendly is True
        assert audit.flagged_parameters == []

    def test_ideal_config_curve_is_smooth_ramp(self):
        audit = audit_bakery_level_configs(BAKERY_LEVEL_CONFIGS_IDEAL)
        assert audit.curve_verdict == "smooth_ramp"

    def test_audit_produces_recommendations(self):
        audit = audit_bakery_level_configs(BAKERY_LEVEL_CONFIGS_CURRENT)
        assert len(audit.recommendations) > 0

    def test_audit_summary_is_non_empty(self):
        audit = audit_bakery_level_configs(BAKERY_LEVEL_CONFIGS_CURRENT)
        assert len(audit.summary) > 20

    def test_level_count_is_correct(self):
        audit = audit_bakery_level_configs(BAKERY_LEVEL_CONFIGS_CURRENT)
        assert audit.level_count == 5


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:

    def test_single_level_game(self):
        report = audit_parameter([5.0], BELT_CONFIG)
        assert report.curve_type == "single_level"
        assert report.transitions == []

    def test_flat_ramp_detected(self):
        # All levels the same — flat
        report = audit_parameter([9.0, 9.0, 9.0, 9.0], BELT_CONFIG)
        assert "flat" in report.curve_type or len(report.flat_spans) > 0

    def test_wrong_direction_detected(self):
        # lower_is_harder param increasing over levels = reversed
        report = audit_parameter([5.0, 6.0, 7.0, 8.0], BELT_CONFIG)
        assert any(t.verdict == "reversed" for t in report.transitions)

    def test_empty_values(self):
        report = audit_parameter([], BELT_CONFIG)
        assert report.is_teaching_friendly is False
        assert report.level_1_verdict == "flag"

    def test_higher_is_harder_teaching_check(self):
        # targetPoolMax: Level 1 value 15 > 10 teaching max → flag
        report = audit_parameter([15, 18, 20], TARGET_CONFIG)
        assert report.level_1_verdict == "flag"

    def test_higher_is_harder_teaching_pass(self):
        report = audit_parameter([8, 10, 12], TARGET_CONFIG)
        assert report.level_1_verdict == "teaching"
