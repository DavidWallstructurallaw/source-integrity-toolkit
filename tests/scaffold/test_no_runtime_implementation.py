# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Retain every historical destructive control with explicit phase context."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools import check_scaffold_boundary as phase_guard
phase_guard.load_phase1_test("tests/scaffold/test_no_runtime_implementation.py", globals())
_phase1_set_up = NoRuntimeImplementationTests.setUp


def _phase2_set_up(self):
    _phase1_set_up(self)
    for relative in ("PHASE_2_PLAN.md", "phase2/entry_manifest.json", "phase2/module_policy.json", "scaffold/delivery_manifest.json"):
        destination = self.root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, destination)


NoRuntimeImplementationTests.setUp = _phase2_set_up

if __name__ == "__main__":
    unittest.main()
