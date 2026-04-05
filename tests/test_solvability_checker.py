"""
Tests for utils/solvability_checker.py

Proof cases:
  1. The original Fire Dispatch bug: target=4, options=[5,3,2], fixed-set → unsolvable
  2. Same target under reusable rule → solvable via 2+2
  3. Various fixed-set successes and failures
  4. Edge cases: zero target, empty options, unknown rule
  5. get_solvable_targets() range filtering
  6. audit_level() full-level audit
"""

import pytest
from utils.solvability_checker import (
    SolvabilityResult,
    LevelSolvabilityReport,
    check_solvability,
    get_solvable_targets,
    audit_level,
)


# ---------------------------------------------------------------------------
# Fire Dispatch original bug — the canonical proof case
# ---------------------------------------------------------------------------

class TestFireDispatchProofCase:
    """
    The bug that triggered this tool:
      - Demand range [4, 8], Level 1 options: hose=5, ladder=3, ambulance=2
      - Achievable subset sums: {2, 3, 5, 7, 8, 10}
      - Targets 4 and 6 are IN the range but have NO valid fixed-set solution
    """

    def test_target_4_is_unsolvable_under_fixed_set(self):
        """The original failure: target=4, options=[5,3,2], fixed-set."""
        result = check_solvability(
            target=4,
            options=[5, 3, 2],
            selection_rule="fixed_set_multi_select",
        )
        assert result.is_solvable is False
        assert result.solution_count == 0
        assert result.example_solutions == []
        assert result.failure_reason != ""
        assert "4" in result.failure_reason

    def test_target_6_is_unsolvable_under_fixed_set(self):
        """Also broken in the original: no subset of [5,3,2] sums to 6."""
        result = check_solvability(
            target=6,
            options=[5, 3, 2],
            selection_rule="fixed_set_multi_select",
        )
        assert result.is_solvable is False

    def test_solvable_targets_for_level_1(self):
        """Only 5, 7, 8 are solvable in [4,8] with fixed-set [5,3,2]."""
        solvable = get_solvable_targets(
            options=[5, 3, 2],
            target_range=(4, 8),
            selection_rule="fixed_set_multi_select",
        )
        assert solvable == [5, 7, 8]
        assert 4 not in solvable
        assert 6 not in solvable

    def test_target_4_is_solvable_under_reusable(self):
        """Under reusable rule: 2+2=4. The bug was assuming fixed-set when reuse could work."""
        result = check_solvability(
            target=4,
            options=[5, 3, 2],
            selection_rule="reusable_multi_select",
        )
        assert result.is_solvable is True
        assert any(sorted(sol) == [2, 2] for sol in result.example_solutions)

    def test_target_6_is_solvable_under_reusable(self):
        """Under reusable rule: 3+3=6."""
        result = check_solvability(
            target=6,
            options=[5, 3, 2],
            selection_rule="reusable_multi_select",
        )
        assert result.is_solvable is True
        assert any(sorted(sol) == [3, 3] for sol in result.example_solutions)


# ---------------------------------------------------------------------------
# Fixed-set multi-select correctness
# ---------------------------------------------------------------------------

class TestFixedSetMultiSelect:

    def test_simple_two_item_solution(self):
        result = check_solvability(
            target=5,
            options=[3, 2, 6],
            selection_rule="fixed_set_multi_select",
        )
        assert result.is_solvable is True
        assert any(sorted(sol) == [2, 3] for sol in result.example_solutions)

    def test_single_item_solution(self):
        result = check_solvability(
            target=6,
            options=[6, 3, 2],
            selection_rule="fixed_set_multi_select",
        )
        assert result.is_solvable is True
        assert [6] in result.example_solutions

    def test_full_set_solution(self):
        result = check_solvability(
            target=10,
            options=[5, 3, 2],
            selection_rule="fixed_set_multi_select",
        )
        assert result.is_solvable is True
        assert any(sorted(sol) == [2, 3, 5] for sol in result.example_solutions)

    def test_no_solution_all_values_too_large(self):
        result = check_solvability(
            target=1,
            options=[3, 5, 7],
            selection_rule="fixed_set_multi_select",
        )
        assert result.is_solvable is False

    def test_multiple_solutions_returned(self):
        # target=5 from [1,2,3,4,5]: solutions include [5], [1,4], [2,3], [1,2,...] etc.
        result = check_solvability(
            target=5,
            options=[1, 2, 3, 4, 5],
            selection_rule="fixed_set_multi_select",
        )
        assert result.is_solvable is True
        assert result.solution_count > 1

    def test_interaction_flags_correct_for_fixed_set(self):
        result = check_solvability(
            target=5,
            options=[3, 2],
            selection_rule="fixed_set_multi_select",
        )
        assert result.item_reuse_allowed is False
        assert result.selected_items_disappear is True
        assert result.exact_match_required is True
        assert result.selection_rule == "fixed_set_multi_select"


# ---------------------------------------------------------------------------
# Reusable multi-select correctness
# ---------------------------------------------------------------------------

class TestReusableMultiSelect:

    def test_solution_via_repetition(self):
        result = check_solvability(
            target=4,
            options=[2, 5],
            selection_rule="reusable_multi_select",
        )
        assert result.is_solvable is True
        assert any(sorted(sol) == [2, 2] for sol in result.example_solutions)

    def test_no_solution_when_smallest_value_too_large(self):
        result = check_solvability(
            target=3,
            options=[5, 7],
            selection_rule="reusable_multi_select",
        )
        assert result.is_solvable is False

    def test_interaction_flags_correct_for_reusable(self):
        result = check_solvability(
            target=4,
            options=[2],
            selection_rule="reusable_multi_select",
        )
        assert result.item_reuse_allowed is True
        assert result.selected_items_disappear is False

    def test_large_target_via_repetition(self):
        result = check_solvability(
            target=12,
            options=[3, 5],
            selection_rule="reusable_multi_select",
        )
        assert result.is_solvable is True
        # 3+3+3+3 or 3+4... wait options are 3 and 5
        # 3*4=12 → [3,3,3,3]
        assert any(all(v == 3 for v in sol) for sol in result.example_solutions)


# ---------------------------------------------------------------------------
# Edge cases
# ---------------------------------------------------------------------------

class TestEdgeCases:

    def test_zero_target_returns_unsolvable(self):
        result = check_solvability(
            target=0,
            options=[1, 2, 3],
            selection_rule="fixed_set_multi_select",
        )
        assert result.is_solvable is False
        assert "positive" in result.failure_reason.lower()

    def test_negative_target_returns_unsolvable(self):
        result = check_solvability(
            target=-5,
            options=[1, 2, 3],
            selection_rule="fixed_set_multi_select",
        )
        assert result.is_solvable is False

    def test_empty_options_returns_unsolvable(self):
        result = check_solvability(
            target=5,
            options=[],
            selection_rule="fixed_set_multi_select",
        )
        assert result.is_solvable is False

    def test_unknown_selection_rule_returns_unsolvable(self):
        result = check_solvability(
            target=5,
            options=[3, 2],
            selection_rule="drag_and_place",  # type: ignore[arg-type]
        )
        assert result.is_solvable is False
        assert "Unsupported" in result.failure_reason

    def test_threshold_match_not_yet_supported(self):
        result = check_solvability(
            target=5,
            options=[3, 2],
            selection_rule="fixed_set_multi_select",
            exact_match_required=False,
        )
        assert result.is_solvable is False
        assert "not yet supported" in result.failure_reason.lower()


# ---------------------------------------------------------------------------
# get_solvable_targets — range filtering
# ---------------------------------------------------------------------------

class TestGetSolvableTargets:

    def test_fire_dispatch_level_1_range(self):
        """Only 5, 7, 8 are reachable from [5,3,2] in [4,8]."""
        result = get_solvable_targets(
            options=[5, 3, 2],
            target_range=(4, 8),
            selection_rule="fixed_set_multi_select",
        )
        assert result == [5, 7, 8]

    def test_all_reachable_under_reusable(self):
        """Under reusable rule [2,3] every value >= 2 is reachable."""
        result = get_solvable_targets(
            options=[2, 3],
            target_range=(2, 10),
            selection_rule="reusable_multi_select",
        )
        # All values 2-10 should be reachable with 2 and 3
        assert result == list(range(2, 11))

    def test_empty_when_nothing_reachable(self):
        result = get_solvable_targets(
            options=[10, 20],
            target_range=(1, 5),
            selection_rule="fixed_set_multi_select",
        )
        assert result == []

    def test_single_value_range(self):
        result = get_solvable_targets(
            options=[5, 3],
            target_range=(8, 8),
            selection_rule="fixed_set_multi_select",
        )
        assert result == [8]


# ---------------------------------------------------------------------------
# audit_level — full level solvability audit
# ---------------------------------------------------------------------------

class TestAuditLevel:

    def test_fire_dispatch_level_1_audit(self):
        """Audit the original Fire Dispatch Level 1 config — should catch targets 4 and 6."""
        report = audit_level(
            level_index=0,
            available_options=[5, 3, 2],
            targets_to_check=[4, 5, 6, 7, 8],
            selection_rule="fixed_set_multi_select",
        )
        assert report.is_fully_solvable is False
        assert 4 in report.unsolvable_targets
        assert 6 in report.unsolvable_targets
        assert 5 in report.solvable_targets
        assert 7 in report.solvable_targets
        assert 8 in report.solvable_targets
        assert "4" in report.failure_summary
        assert "6" in report.failure_summary

    def test_fully_solvable_level(self):
        report = audit_level(
            level_index=1,
            available_options=[5, 3, 2, 4],
            targets_to_check=[5, 6, 7, 8, 9],
            selection_rule="fixed_set_multi_select",
        )
        assert report.is_fully_solvable is True
        assert report.unsolvable_targets == []
        assert report.failure_summary == ""

    def test_report_metadata(self):
        report = audit_level(
            level_index=2,
            available_options=[3, 2],
            targets_to_check=[5],
            selection_rule="fixed_set_multi_select",
        )
        assert report.level_index == 2
        assert report.selection_rule == "fixed_set_multi_select"
        assert report.available_options == [3, 2]
        assert report.all_targets_checked == [5]
