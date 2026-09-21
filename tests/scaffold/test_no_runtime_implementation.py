# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Retain every historical destructive control with explicit phase context."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools import check_scaffold_boundary as phase_guard
phase_guard.load_phase1_test("tests/scaffold/test_no_runtime_implementation.py", globals())
_phase1_set_up = NoRuntimeImplementationTests.setUp


def _current_set_up(self):
    _phase1_set_up(self)
    for relative in ("PHASE_2_PLAN.md", "phase2/entry_manifest.json", "phase2/module_policy.json", "scaffold/delivery_manifest.json",
                     "PHASE_3_PLAN.md", "phase3/entry_manifest.json", "phase3/module_policy.json"):
        destination = self.root / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, destination)


NoRuntimeImplementationTests.setUp = _current_set_up

# Approved P3-W04-R01: keep the loaded historical methods and their exact
# assertions. The permanent inert reporting slot retains their original
# purpose after the scheduled graph promotion. The ledger records this change.
_phase1_test_syntax_error_and_oversize_do_not_crash_guard = NoRuntimeImplementationTests.test_syntax_error_and_oversize_do_not_crash_guard
_phase1_test_real_guard_cli_is_not_removed_by_python_optimization = NoRuntimeImplementationTests.test_real_guard_cli_is_not_removed_by_python_optimization


def _current_test_syntax_error_and_oversize_do_not_crash_guard(self):
    path = self.package / "reporting/json_report.py"
    path.write_text("def (\n")
    self.assertFalse(guard.check_repository(self.root)["ok"])
    path.write_text("#" * 20000)
    self.assertFalse(guard.check_repository(self.root)["ok"])


def _current_test_real_guard_cli_is_not_removed_by_python_optimization(self):
    command = [sys.executable, "-I", "-B", "-O", str(ROOT / "tools/check_scaffold_boundary.py"),
               "--root", str(self.root)]
    positive = subprocess.run(command, capture_output=True, text=True, timeout=20)
    self.assertEqual(positive.returncode, 0, positive.stdout + positive.stderr)
    (self.package / "reporting/json_report.py").write_text("ACTIVE = {}\n")
    negative = subprocess.run(command, capture_output=True, text=True, timeout=20)
    self.assertEqual(negative.returncode, 1)
    self.assertFalse(json.loads(negative.stdout)["ok"])


NoRuntimeImplementationTests.test_syntax_error_and_oversize_do_not_crash_guard = _current_test_syntax_error_and_oversize_do_not_crash_guard
NoRuntimeImplementationTests.test_real_guard_cli_is_not_removed_by_python_optimization = _current_test_real_guard_cli_is_not_removed_by_python_optimization


class W04R01LiveGuardTests(unittest.TestCase):
    """Current live and frozen limits, independent of the two old assertions."""
    setUp = _current_set_up

    def _assert_current_copy(self):
        result = guard.check_repository(self.root)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["checked_modules"], 48)

    def _mutation(self, relative, payload):
        self._assert_current_copy()
        path = self.package / relative
        original = path.read_bytes()
        try:
            path.write_bytes(payload)
            result = guard.check_repository(self.root)
        finally:
            path.write_bytes(original)
        self._assert_current_copy()
        return result

    def _optimized_cli_mutation(self, relative, payload):
        self._assert_current_copy()
        command = [sys.executable, "-I", "-B", "-O", str(ROOT / "tools/check_scaffold_boundary.py"),
                   "--root", str(self.root)]
        positive = subprocess.run(command, capture_output=True, text=True, timeout=20)
        self.assertEqual(positive.returncode, 0, positive.stdout + positive.stderr)
        self.assertTrue(json.loads(positive.stdout)["ok"])
        path = self.package / relative
        original = path.read_bytes()
        try:
            path.write_bytes(payload)
            negative = subprocess.run(command, capture_output=True, text=True, timeout=20)
        finally:
            path.write_bytes(original)
        self._assert_current_copy()
        self.assertEqual(negative.returncode, 1, negative.stdout + negative.stderr)
        result = json.loads(negative.stdout)
        self.assertFalse(result["ok"])
        return result

    def test_live_syntax_error_reports_affected_module(self):
        result = self._mutation("graph/cycles.py", b"def (\n")
        self.assertFalse(result["ok"])
        self.assertIn({"path": "graph/cycles.py", "code": "invalid_python"}, result["issues"])

    def test_live_size_ceiling_accepts_equality_and_rejects_one_byte_excess(self):
        prefix = b"ACTIVE = {}\n#"
        equality = prefix + b"x" * (262144 - len(prefix))
        self.assertEqual(len(equality), 262144)
        positive = self._mutation("graph/cycles.py", equality)
        self.assertTrue(positive["ok"], positive)
        excess = equality + b"x"
        self.assertEqual(len(excess), 262145)
        negative = self._mutation("graph/cycles.py", excess)
        self.assertFalse(negative["ok"])
        self.assertIn({"path": "graph/cycles.py", "code": "oversize_module"}, negative["issues"])

    def test_real_optimized_cli_rejects_live_forbidden_effect(self):
        result = self._optimized_cli_mutation(
            "graph/cycles.py", b'def unsafe():\n    return open("synthetic-canary")\n')
        self.assertIn({"path": "graph/cycles.py", "code": "forbidden_effect"}, result["issues"])

    def test_inert_size_ceiling_distinguishes_equal_and_one_byte_excess(self):
        equality = self._mutation("reporting/json_report.py", b"#" * 16384)
        # A changed inert file must still fail its byte pin at this size.
        self.assertFalse(equality["ok"])
        self.assertIn({"path": "reporting/json_report.py", "code": "accepted_blob_changed"}, equality["issues"])
        self.assertNotIn({"path": "reporting/json_report.py", "code": "oversize_module"}, equality["issues"])
        excess = self._mutation("reporting/json_report.py", b"#" * 16385)
        self.assertFalse(excess["ok"])
        self.assertIn({"path": "reporting/json_report.py", "code": "oversize_module"}, excess["issues"])

    def test_real_optimized_cli_rejects_inert_body_independently_of_pin(self):
        result = self._optimized_cli_mutation("reporting/json_report.py", b"ACTIVE = {}\n")
        self.assertIn({"path": "reporting/json_report.py", "code": "non_scaffold_body"}, result["issues"])

if __name__ == "__main__":
    unittest.main()
