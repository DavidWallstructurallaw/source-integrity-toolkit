# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Preserve software-layer controls; permit only promoted standard-library use."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools import check_scaffold_boundary as phase_guard
phase_guard.load_phase1_test("tests/scaffold/test_layer_boundaries.py", globals())


def _current_imports(self):
    active = guard.promotions(ROOT)
    for path in guard.EXPECTED_PATHS:
        with self.subTest(path=path):
            source = (ROOT / "src/source_integrity_toolkit" / path).read_text(encoding="utf-8")
            self.assertEqual(guard.layer_issues(path, source, live=path in active), [])


LayerBoundaryTests.test_accepted_imports_have_no_layer_errors = _current_imports

if __name__ == "__main__":
    unittest.main()
