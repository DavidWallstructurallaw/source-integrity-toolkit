# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Application-originated native binding probes, separate from stdlib startup."""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from test_scaffold_inertness import run_probe


class ScaffoldNativeTests(unittest.TestCase):
    def test_all_slots_load_without_application_native_binding(self):
        result = run_probe()
        self.assertTrue(result["ok"], result)
        self.assertFalse(any(v.startswith("ctypes.") for v in result["violations"]))

    def test_deliberate_cdll_is_blocked_before_loading(self):
        # Windows requires a string before it emits the loader audit event.
        argument = '"SYNTHETIC_NONEXISTENT_LIBRARY"' if sys.platform == "win32" else "None"
        result = run_probe(("io/platform_linux.py", f'\nimport ctypes\nctypes.CDLL({argument})\n'))
        self.assertFalse(result["ok"])
        self.assertIn("ctypes.dlopen", result["violations"])

    def test_deliberate_platform_loader_cannot_hide_in_other_slot(self):
        result = run_probe(("contracts/execution.py", '\nimport ctypes\nctypes.CDLL("SYNTHETIC_NONEXISTENT_LIBRARY")\n'))
        self.assertIn("ctypes.dlopen", result["violations"])
        self.assertTrue(result["input_unchanged"] and result["output_unchanged"])


if __name__ == "__main__":
    unittest.main()
