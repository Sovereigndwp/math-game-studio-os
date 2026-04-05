"""
Regression tests for the Misconception Architect workflow.

Covers:
  1. Deterministic known-game path (no API)
  2. Changed-brief diff-and-extend logic (no API)
  3. Write-back pending file generation
  4. Stability-check count extraction
  5. Quality gate checks
  6. Keyword routing fallback
  7. Category priority assignment
  8. Field diff computation

All tests run without API calls or external dependencies.
Uses unittest (stdlib) so no pip install is needed.

Run:
    python -m pytest tests/test_misconception_workflow.py -v
    # or without pytest:
    python -m unittest tests.test_misconception_workflow -v
"""

import json
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from agents.misconception_architect.agent import (
    _SIX_CATEGORIES,
    _REQUIRED_FIELDS,
    _all_fields_present,
    _risk_matches_category,
    _find_matching_risk,
    _find_matching_risk_from_routing,
    _route_risks_semantically,
    _risk_changes_entry_heuristic,
    _diff_library_entry,
    _quality_check_revised,
    _quality_check_new_entry,
    _assign_category_priority,
    _compute_field_diff,
    prepare_library_writeback,
    run,
)

from scripts.run_misconception_architect import (
    _bakery_rush_briefs,
    _bakery_rush_changed_brief,
    _extract_counts,
    _extract_llm_counts,
)


def _write_briefs(briefs, tmpdir):
    """Write brief dicts to temp files and return artifact_paths."""
    tmp = Path(tmpdir)
    paths = {}
    for name, key in [("lowest_viable_loop_brief", "loop_brief"),
                      ("family_architecture_brief", "family_brief"),
                      ("interaction_decision_memo", "interaction_memo")]:
        p = tmp / f"{name}.json"
        p.write_text(json.dumps(briefs[key], indent=2))
        paths[name] = p
    return paths


# ---------------------------------------------------------------------------
# Test 1: Deterministic known-game path
# ---------------------------------------------------------------------------

class TestDeterministicPath(unittest.TestCase):

    def setUp(self):
        self.briefs = _bakery_rush_briefs()
        self._tmpdir = tempfile.TemporaryDirectory()
        self.artifact_paths = _write_briefs(self.briefs, self._tmpdir.name)

    def tearDown(self):
        self._tmpdir.cleanup()

    def test_bakery_rush_passes_gate(self):
        result = run(repo_root=REPO_ROOT, job_id="test-det-gate",
                     artifact_paths=self.artifact_paths)
        self.assertEqual(result.artifact["status"], "pass")
        self.assertTrue(result.artifact["gate_threshold_met"])
        self.assertTrue(result.artifact["library_reference_used"])

    def test_six_entries_produced(self):
        result = run(repo_root=REPO_ROOT, job_id="test-det-count",
                     artifact_paths=self.artifact_paths)
        self.assertEqual(len(result.artifact["misconceptions"]), 6)
        self.assertEqual(result.artifact["valid_misconception_count"], 6)

    def test_all_categories_covered(self):
        result = run(repo_root=REPO_ROOT, job_id="test-det-cats",
                     artifact_paths=self.artifact_paths)
        categories = {m["category"] for m in result.artifact["misconceptions"]}
        self.assertEqual(categories, set(_SIX_CATEGORIES))

    def test_all_entries_have_required_fields(self):
        result = run(repo_root=REPO_ROOT, job_id="test-det-fields",
                     artifact_paths=self.artifact_paths)
        for m in result.artifact["misconceptions"]:
            self.assertTrue(
                _all_fields_present(m),
                f"Missing fields in {m['category']}: {_REQUIRED_FIELDS - set(m.keys())}",
            )

    def test_change_rationale_present(self):
        result = run(repo_root=REPO_ROOT, job_id="test-det-rationale",
                     artifact_paths=self.artifact_paths)
        for m in result.artifact["misconceptions"]:
            self.assertIn("change_rationale", m)
            self.assertGreater(len(m["change_rationale"]), 10)


# ---------------------------------------------------------------------------
# Test 2: Changed-brief diff-and-extend (no API)
# ---------------------------------------------------------------------------

class TestChangedBriefDiff(unittest.TestCase):

    def setUp(self):
        self.briefs = _bakery_rush_changed_brief()
        self._tmpdir = tempfile.TemporaryDirectory()
        self.artifact_paths = _write_briefs(self.briefs, self._tmpdir.name)

    def tearDown(self):
        self._tmpdir.cleanup()

    def test_detects_revisions(self):
        result = run(repo_root=REPO_ROOT, job_id="test-changed-rev",
                     artifact_paths=self.artifact_paths)
        counts = _extract_counts(result.artifact)
        self.assertGreater(counts["revised"], 0,
                           "Changed brief should trigger at least one revision")

    def test_keeps_most_entries(self):
        result = run(repo_root=REPO_ROOT, job_id="test-changed-kept",
                     artifact_paths=self.artifact_paths)
        counts = _extract_counts(result.artifact)
        self.assertGreaterEqual(counts["kept"], 3)

    def test_still_passes_gate(self):
        result = run(repo_root=REPO_ROOT, job_id="test-changed-gate",
                     artifact_paths=self.artifact_paths)
        self.assertTrue(result.artifact["gate_threshold_met"])


# ---------------------------------------------------------------------------
# Test 3: Write-back pending file generation
# ---------------------------------------------------------------------------

class TestWritebackGeneration(unittest.TestCase):

    def test_writeback_from_revised_entries(self):
        misconceptions = []
        for cat in _SIX_CATEGORIES:
            entry = {
                "id": f"test_{cat}", "category": cat,
                "label": f"Test {cat}",
                "description": f"Test description for {cat} — updated",
                "likely_cause": "Test cause text here",
                "how_it_appears_in_play": "Test appearance text here",
                "detection_signal": "Test signal with enough specifics",
                "best_feedback_response": "Test feedback response text",
                "best_clean_replay_task": "Test replay task with structure",
                "reflection_prompt": "Test reflection prompt question?",
                "change_rationale": "Updated description.",
                "priority": "primary",
            }
            misconceptions.append(entry)

        library_entry = {
            "game_name": "Test Game", "game_family": "combine_and_build",
            "misconceptions": [
                {
                    "id": f"test_{cat}", "category": cat, "label": f"Test {cat}",
                    "description": f"Original description for {cat}",
                    "likely_cause": "Test cause text here",
                    "how_it_appears_in_play": "Test appearance text here",
                    "detection_signal": "Test signal with enough specifics",
                    "best_feedback_response": "Test feedback response text",
                    "best_clean_replay_task": "Test replay task with structure",
                    "reflection_prompt": "Test reflection prompt question?",
                }
                for cat in _SIX_CATEGORIES
            ],
        }

        wb = prepare_library_writeback(
            misconceptions=misconceptions, library_entry=library_entry,
            llm_revised_categories=["representation_mismatch"],
            quality_warnings=[], job_id="test-wb", family_name="Test Game",
            repo_root=REPO_ROOT,
        )
        self.assertIsNotNone(wb)
        self.assertEqual(wb["status"], "pending_review")
        self.assertEqual(wb["source_job_id"], "test-wb")
        self.assertEqual(len(wb["entries_to_update"]), 1)
        self.assertEqual(wb["entries_to_update"][0]["category"], "representation_mismatch")
        self.assertIn("description", wb["entries_to_update"][0]["fields_changed"])

    def test_no_writeback_when_nothing_revised(self):
        misconceptions = [
            {
                "id": f"test_{cat}", "category": cat, "label": f"Test {cat}",
                "description": "Same as library text",
                "likely_cause": "Same cause text", "how_it_appears_in_play": "Same play",
                "detection_signal": "Same signal", "best_feedback_response": "Same feedback",
                "best_clean_replay_task": "Same replay task",
                "reflection_prompt": "Same prompt?", "priority": "primary",
            }
            for cat in _SIX_CATEGORIES
        ]
        wb = prepare_library_writeback(
            misconceptions=misconceptions,
            library_entry={"misconceptions": []},
            llm_revised_categories=[], quality_warnings=[],
            job_id="test-no-wb", family_name="Test", repo_root=REPO_ROOT,
        )
        self.assertIsNone(wb)


# ---------------------------------------------------------------------------
# Test 4: Stability-check count extraction
# ---------------------------------------------------------------------------

class TestCountExtraction(unittest.TestCase):

    def test_extract_counts_from_notes(self):
        artifact = {
            "notes": "Diff-and-extend: kept 4, revised 2, added 0. Other stuff.",
            "misconceptions": [{"priority": "primary"}] * 5 + [{"priority": "secondary"}],
        }
        counts = _extract_counts(artifact)
        self.assertEqual(counts["kept"], 4)
        self.assertEqual(counts["revised"], 2)
        self.assertEqual(counts["added"], 0)
        self.assertEqual(counts["total"], 6)
        self.assertEqual(counts["secondaries"], 1)

    def test_extract_llm_counts(self):
        notes = "LLM revised 3 entries: a, b, c LLM added 1 new entries LLM rejected 2 unmatched risks"
        llm = _extract_llm_counts(notes)
        self.assertEqual(llm["llm_revised"], 3)
        self.assertEqual(llm["llm_added"], 1)
        self.assertEqual(llm["llm_rejected"], 2)

    def test_extract_llm_counts_empty(self):
        llm = _extract_llm_counts("No LLM activity.")
        self.assertEqual(llm["llm_revised"], 0)
        self.assertEqual(llm["llm_added"], 0)
        self.assertEqual(llm["llm_rejected"], 0)


# ---------------------------------------------------------------------------
# Test 5: Quality gate checks
# ---------------------------------------------------------------------------

class TestQualityGate(unittest.TestCase):

    def test_identical_detection_fails(self):
        original = {"detection_signal": "Three taps within 1500ms"}
        revised = {"detection_signal": "Three taps within 1500ms", "description": "new"}
        qc = _quality_check_revised(revised, original)
        self.assertFalse(qc["passed"])
        self.assertTrue(any("identical" in i for i in qc["issues"]))

    def test_different_detection_passes(self):
        original = {"detection_signal": "Three taps within 1500ms"}
        revised = {
            "detection_signal": "Running total direction changes 3+ times per order",
            "description": "New description that is different from original",
        }
        qc = _quality_check_revised(revised, original)
        self.assertTrue(qc["passed"])

    def test_near_duplicate_flagged(self):
        existing = [{
            "category": "concept_confusion", "id": "existing_1",
            "label": "Confuses count with sum",
            "description": "Learner believes target means number of items not sum of values",
        }]
        new_entry = {
            "category": "concept_confusion", "id": "new_1",
            "label": "Different label",
            "description": "Learner believes target means number of items not sum of their values and counts",
            "detection_signal": "Item count equals target on 3+ orders with enough detail",
        }
        qc = _quality_check_new_entry(new_entry, existing)
        self.assertEqual(qc["near_duplicate_of"], "existing_1")

    def test_short_detection_flagged(self):
        new_entry = {
            "category": "impulsive_guess", "id": "short",
            "label": "Test", "description": "Unique learner error description here",
            "detection_signal": "Too short",
        }
        qc = _quality_check_new_entry(new_entry, [])
        self.assertFalse(qc["passed"])
        self.assertTrue(any("too short" in i for i in qc["issues"]))


# ---------------------------------------------------------------------------
# Test 6: Keyword routing fallback
# ---------------------------------------------------------------------------

class TestKeywordRouting(unittest.TestCase):

    def test_impulsive_guess_matches(self):
        self.assertTrue(_risk_matches_category(
            "Belt speed triggers tap-before-thinking", "impulsive_guess"))

    def test_procedure_slip_matches(self):
        self.assertTrue(_risk_matches_category(
            "Running total not tracked — learner loses count near target", "procedure_slip"))

    def test_no_false_positive(self):
        self.assertFalse(_risk_matches_category(
            "Subtraction items create strategic paralysis", "impulsive_guess"))

    def test_find_matching_risk(self):
        risks = ["Running total not tracked", "Belt speed triggers tap-before-thinking"]
        self.assertEqual(
            _find_matching_risk(risks, "impulsive_guess"),
            "Belt speed triggers tap-before-thinking",
        )
        self.assertIsNone(_find_matching_risk(risks, "concept_confusion"))

    def test_find_from_routing_map(self):
        routing = {"risk A": "impulsive_guess", "risk B": "concept_confusion", "risk C": "unmatched"}
        self.assertEqual(_find_matching_risk_from_routing(routing, "impulsive_guess"), "risk A")
        self.assertIsNone(_find_matching_risk_from_routing(routing, "strategic_overload"))

    def test_semantic_routing_fallback(self):
        risks = [
            "Belt speed triggers tap-before-thinking",
            "Running total not tracked — learner loses count near target",
            "Something completely unrelated to any category keywords",
        ]
        routing = _route_risks_semantically(risks, _SIX_CATEGORIES, None, gate_llm=None)
        self.assertEqual(routing[risks[0]], "impulsive_guess")
        self.assertEqual(routing[risks[1]], "procedure_slip")
        self.assertEqual(routing[risks[2]], "unmatched")


# ---------------------------------------------------------------------------
# Test 7: Category priority assignment
# ---------------------------------------------------------------------------

class TestCategoryPriority(unittest.TestCase):

    def test_single_entries_are_primary(self):
        entries = [{"category": "impulsive_guess", "id": "a"},
                   {"category": "procedure_slip", "id": "b"}]
        _assign_category_priority(entries)
        self.assertEqual(entries[0]["priority"], "primary")
        self.assertEqual(entries[1]["priority"], "primary")

    def test_duplicate_gets_secondary(self):
        entries = [
            {"category": "concept_confusion", "id": "original"},
            {"category": "impulsive_guess", "id": "other"},
            {"category": "concept_confusion", "id": "added"},
        ]
        _assign_category_priority(entries)
        self.assertEqual(entries[0]["priority"], "primary")
        self.assertEqual(entries[2]["priority"], "secondary")
        self.assertEqual(entries[2]["primary_entry_id"], "original")


# ---------------------------------------------------------------------------
# Test 8: Field diff computation
# ---------------------------------------------------------------------------

class TestFieldDiff(unittest.TestCase):

    def test_detects_changed_fields(self):
        original = {"id": "x", "category": "y", "description": "old", "label": "same"}
        revised = {"id": "x", "category": "y", "description": "new", "label": "same"}
        diff = _compute_field_diff(original, revised)
        self.assertIn("description", diff)
        self.assertEqual(diff["description"]["old"], "old")
        self.assertEqual(diff["description"]["new"], "new")
        self.assertNotIn("label", diff)

    def test_no_diff_when_identical(self):
        entry = {"id": "x", "category": "y", "description": "same", "label": "same"}
        self.assertEqual(_compute_field_diff(entry, entry), {})


if __name__ == "__main__":
    unittest.main()
