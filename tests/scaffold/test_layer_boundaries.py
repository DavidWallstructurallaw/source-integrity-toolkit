# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Software dependency-direction tests; no source graph is evaluated."""
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools import check_scaffold_boundary as guard


class LayerBoundaryTests(unittest.TestCase):
    def test_accepted_imports_have_no_layer_errors(self):
        for path in guard.EXPECTED_PATHS:
            with self.subTest(path=path):
                source = (ROOT / "src/source_integrity_toolkit" / path).read_text()
                self.assertEqual(guard.layer_issues(path, source), [])

    def test_allowed_architecture_direction_does_not_authorize_behavior(self):
        source = "from ..contracts import evidence\n"
        self.assertEqual(guard.layer_issues("analysis/origins.py", source), [])
        self.assertTrue(guard.form_issues("analysis/origins.py", source))

    def test_reporting_cannot_recompute_analysis(self):
        self.assertIn("layer_violation", guard.layer_issues(
            "reporting/json_report.py", "from ..analysis.origins import trace\n"))

    def test_lower_layers_cannot_import_runtime_authority(self):
        for path in ("contracts/bundle.py", "validation/structure.py", "graph/traversal.py"):
            with self.subTest(path=path):
                self.assertIn("layer_violation", guard.layer_issues(path, "from ..runtime.boundary import run\n"))

    def test_cross_project_native_network_and_oracle_imports_fail(self):
        for name in ("recursive_integrity_toolkit", "integrity_core", "ctypes", "socket",
                     "requests", "subprocess", "tests.golden", "scaffold", "tools"):
            with self.subTest(name=name):
                self.assertIn("unapproved_import", guard.layer_issues("api.py", f"import {name}\n"))

    def test_relative_escape_and_wildcard_fail(self):
        self.assertIn("relative_import_escape", guard.layer_issues("api.py", "from ...x import y\n"))
        self.assertIn("wildcard_import", guard.layer_issues("analysis/origins.py", "from ..contracts import *\n"))

    def test_import_cycle_detection_has_positive_and_negative_controls(self):
        positive = {"analysis/origins.py": "from . import inventory\n", "analysis/inventory.py": '"""slot"""\n'}
        self.assertEqual(guard.import_cycle_issues(positive), [])
        negative = dict(positive)
        negative["analysis/inventory.py"] = "from . import origins\n"
        self.assertEqual(guard.import_cycle_issues(negative), ["import_cycle"])


if __name__ == "__main__":
    unittest.main()
