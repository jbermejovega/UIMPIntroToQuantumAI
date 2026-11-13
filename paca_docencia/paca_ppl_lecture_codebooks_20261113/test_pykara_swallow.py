"""Pure structural TDD for KOKO PYKARA/SWALLOW. No notebook execution."""
import unittest
from pathlib import Path

from pykara_swallow_pydantic2 import build_plan, inspect_local


class TestPykaraSwallow(unittest.TestCase):
    def test_nine_identity_distinct_occurrences(self):
        plan = build_plan("57026af5da039388d98478398825b4d7ad53393b")
        self.assertEqual(len(plan.occurrences), 9)
        self.assertEqual(len({o.codebook_path for o in plan.occurrences}), 9)

    def test_deterministic_receipt(self):
        h = "57026af5da039388d98478398825b4d7ad53393b"
        self.assertEqual(build_plan(h).receipt(), build_plan(h).receipt())

    def test_no_effect_promotion(self):
        receipt = build_plan("57026af5da039388d98478398825b4d7ad53393b").receipt()
        self.assertFalse(receipt["git_mutation"])
        self.assertFalse(receipt["ci_certified"])
        self.assertFalse(receipt["monty_executed"])

    def test_actual_files_and_unexecuted_cells(self):
        result = inspect_local(Path(__file__).resolve().parent,
            "57026af5da039388d98478398825b4d7ad53393b")
        self.assertEqual(result["missing"], [])
        self.assertEqual(result["malformed"], [])
        self.assertEqual(result["status"], "SOURCE_PLAN")


if __name__ == "__main__":
    unittest.main()
