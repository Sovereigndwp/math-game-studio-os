"""
Solvability Checker — Math Game Studio OS
utils/solvability_checker.py

A guard layer that checks whether a generated game state is actually winnable
under the game's own declared interaction rules.

Answers:
  - Can the target be reached?
  - Under the allowed selection rules?
  - From the currently offered options?
  - Without hidden assumptions about reuse or order?

Used by:
  - Preview generation (fail fast on unsolvable boards)
  - Gate engine (revise-level check on prototype specs)
  - Implementation plan agents (validate generated level configs)

Supported selection rules:
  - fixed_set_multi_select  : each option usable at most once; items disappear when chosen
  - reusable_multi_select   : same option selectable multiple times; combination order irrelevant

Currently supports exact-match only. Threshold-match support is deferred.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Literal, Sequence


SelectionRule = Literal[
    "fixed_set_multi_select",
    "reusable_multi_select",
]


@dataclass
class SolvabilityResult:
    """Full audit record for one solvability check."""
    is_solvable: bool
    solution_count: int                          # number of distinct solutions found (up to max_solutions)
    example_solutions: List[List[int]]           # up to max_solutions distinct solutions
    failure_reason: str                          # non-empty only when is_solvable is False
    # Interaction assumptions that were used — makes the audit transparent
    selection_rule: str
    item_reuse_allowed: bool
    selected_items_disappear: bool
    exact_match_required: bool


@dataclass
class LevelSolvabilityReport:
    """Audit record for a full level's worth of generated targets."""
    level_index: int
    selection_rule: str
    available_options: List[int]
    all_targets_checked: List[int]
    solvable_targets: List[int]
    unsolvable_targets: List[int]
    is_fully_solvable: bool                      # True only if every target is solvable
    failure_summary: str


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _dedupe_solutions(solutions: List[List[int]]) -> List[List[int]]:
    """Remove duplicate solutions (order-independent)."""
    seen: set = set()
    unique: List[List[int]] = []
    for sol in solutions:
        key = tuple(sorted(sol))
        if key not in seen:
            seen.add(key)
            unique.append(sol)
    return unique


def _fixed_set_solutions(
    target: int,
    options: Sequence[int],
    max_solutions: int = 5,
) -> List[List[int]]:
    """
    Find subsets of `options` (each used at most once) that sum to `target`.
    Uses DFS over the 2^n bitmask space; n ≤ the options length.
    Returns up to `max_solutions` distinct solutions.
    """
    results: List[List[int]] = []
    n = len(options)

    def backtrack(index: int, current_sum: int, chosen: List[int]) -> None:
        if len(results) >= max_solutions:
            return
        if current_sum == target:
            results.append(chosen[:])
            return
        if current_sum > target or index >= n:
            return
        # Include options[index]
        chosen.append(options[index])
        backtrack(index + 1, current_sum + options[index], chosen)
        chosen.pop()
        # Skip options[index]
        backtrack(index + 1, current_sum, chosen)

    backtrack(0, 0, [])
    return _dedupe_solutions(results)


def _reusable_solutions(
    target: int,
    options: Sequence[int],
    max_solutions: int = 5,
) -> List[List[int]]:
    """
    Find multisets of values drawn from `options` (with repetition allowed)
    that sum to `target`.
    Iterates in non-decreasing order to avoid duplicates.
    Returns up to `max_solutions` distinct solutions.
    """
    results: List[List[int]] = []
    usable = sorted(set(v for v in options if v > 0))

    def backtrack(start_index: int, current_sum: int, chosen: List[int]) -> None:
        if len(results) >= max_solutions:
            return
        if current_sum == target:
            results.append(chosen[:])
            return
        if current_sum > target:
            return
        for i in range(start_index, len(usable)):
            value = usable[i]
            chosen.append(value)
            backtrack(i, current_sum + value, chosen)   # i not i+1 — allows reuse
            chosen.pop()

    backtrack(0, 0, [])
    return _dedupe_solutions(results)


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def check_solvability(
    *,
    target: int,
    options: Sequence[int],
    selection_rule: SelectionRule,
    exact_match_required: bool = True,
    max_solutions: int = 5,
) -> SolvabilityResult:
    """
    Check whether `target` is reachable from `options` under `selection_rule`.

    Args:
        target:               The numeric value the player must reach.
        options:              Values available to the player this round
                              (e.g. truck capacities, pastry values).
        selection_rule:       'fixed_set_multi_select' or 'reusable_multi_select'.
        exact_match_required: Must currently be True (threshold-match is deferred).
        max_solutions:        Stop collecting solutions after this many.

    Returns:
        SolvabilityResult with is_solvable, solution_count, example_solutions,
        failure_reason, and the interaction assumptions used.
    """
    item_reuse_allowed = (selection_rule == "reusable_multi_select")
    selected_items_disappear = (selection_rule == "fixed_set_multi_select")

    # Guard: target must be positive
    if target <= 0:
        return SolvabilityResult(
            is_solvable=False,
            solution_count=0,
            example_solutions=[],
            failure_reason=f"Target must be a positive integer; got {target}.",
            selection_rule=selection_rule,
            item_reuse_allowed=item_reuse_allowed,
            selected_items_disappear=selected_items_disappear,
            exact_match_required=exact_match_required,
        )

    # Guard: threshold-match not yet implemented
    if not exact_match_required:
        return SolvabilityResult(
            is_solvable=False,
            solution_count=0,
            example_solutions=[],
            failure_reason="Threshold-match (exact_match_required=False) is not yet supported.",
            selection_rule=selection_rule,
            item_reuse_allowed=item_reuse_allowed,
            selected_items_disappear=selected_items_disappear,
            exact_match_required=exact_match_required,
        )

    # Guard: unknown selection rule
    if selection_rule not in ("fixed_set_multi_select", "reusable_multi_select"):
        return SolvabilityResult(
            is_solvable=False,
            solution_count=0,
            example_solutions=[],
            failure_reason=f"Unsupported selection_rule: '{selection_rule}'.",
            selection_rule=selection_rule,
            item_reuse_allowed=item_reuse_allowed,
            selected_items_disappear=selected_items_disappear,
            exact_match_required=exact_match_required,
        )

    if selection_rule == "fixed_set_multi_select":
        examples = _fixed_set_solutions(target, options, max_solutions)
    else:
        examples = _reusable_solutions(target, options, max_solutions)

    is_solvable = len(examples) > 0
    failure_reason = (
        ""
        if is_solvable
        else (
            f"No legal combination of {list(options)} reaches {target} "
            f"under {selection_rule} exact-match rules."
        )
    )

    return SolvabilityResult(
        is_solvable=is_solvable,
        solution_count=len(examples),
        example_solutions=examples,
        failure_reason=failure_reason,
        selection_rule=selection_rule,
        item_reuse_allowed=item_reuse_allowed,
        selected_items_disappear=selected_items_disappear,
        exact_match_required=exact_match_required,
    )


def get_solvable_targets(
    *,
    options: Sequence[int],
    target_range: tuple[int, int],
    selection_rule: SelectionRule,
    exact_match_required: bool = True,
) -> List[int]:
    """
    Return every integer in [target_range[0], target_range[1]] that is solvable
    from `options` under `selection_rule`.

    This is the function to call inside level generators before picking a target:

        solvable = get_solvable_targets(
            options=[5, 3, 2],
            target_range=(4, 8),
            selection_rule="fixed_set_multi_select",
        )
        # solvable == [5, 7, 8]  — NOT [4, 6] which have no valid subset

    Args:
        options:        Values available this level (e.g. truck capacities).
        target_range:   (lo, hi) inclusive range for target generation.
        selection_rule: 'fixed_set_multi_select' or 'reusable_multi_select'.

    Returns:
        Sorted list of target values that have at least one valid solution.
        Returns [] if nothing in range is reachable — the level config is invalid.
    """
    lo, hi = target_range
    solvable: List[int] = []
    for t in range(lo, hi + 1):
        result = check_solvability(
            target=t,
            options=options,
            selection_rule=selection_rule,
            exact_match_required=exact_match_required,
            max_solutions=1,  # we only need to know IF one exists, not enumerate all
        )
        if result.is_solvable:
            solvable.append(t)
    return solvable


def audit_level(
    *,
    level_index: int,
    available_options: Sequence[int],
    targets_to_check: Sequence[int],
    selection_rule: SelectionRule,
    exact_match_required: bool = True,
) -> LevelSolvabilityReport:
    """
    Audit every target in `targets_to_check` against `available_options`.

    Returns a LevelSolvabilityReport classifying each target as solvable or not,
    with a human-readable summary for gate messages and dev output.

    Example usage in a gate or implementation agent:
        report = audit_level(
            level_index=0,
            available_options=[5, 3, 2],
            targets_to_check=[4, 5, 6, 7, 8],
            selection_rule="fixed_set_multi_select",
        )
        if not report.is_fully_solvable:
            raise ValueError(report.failure_summary)
    """
    solvable: List[int] = []
    unsolvable: List[int] = []
    for t in targets_to_check:
        result = check_solvability(
            target=t,
            options=list(available_options),
            selection_rule=selection_rule,
            exact_match_required=exact_match_required,
            max_solutions=1,
        )
        (solvable if result.is_solvable else unsolvable).append(t)

    is_fully_solvable = len(unsolvable) == 0
    failure_summary = (
        ""
        if is_fully_solvable
        else (
            f"Level {level_index}: unsolvable targets {unsolvable} cannot be reached "
            f"from options {list(available_options)} under {selection_rule}. "
            f"Remove these targets from the level config or change the available options."
        )
    )

    return LevelSolvabilityReport(
        level_index=level_index,
        selection_rule=selection_rule,
        available_options=list(available_options),
        all_targets_checked=list(targets_to_check),
        solvable_targets=solvable,
        unsolvable_targets=unsolvable,
        is_fully_solvable=is_fully_solvable,
        failure_summary=failure_summary,
    )
