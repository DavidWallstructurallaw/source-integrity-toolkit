# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Positive and destructive controls for the developer scaffold guard."""
from __future__ import annotations

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools import check_scaffold_boundary as guard


class NoRuntimeImplementationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / "src/source_integrity_toolkit", self.root / "src/source_integrity_toolkit")
        self.package = self.root / "src/source_integrity_toolkit"

    def test_real_accepted_package_passes_all_guards(self):
        result = guard.check_repository(ROOT)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["checked_modules"], 48)

    def test_exact_package_path_set_is_independent(self):
        self.assertEqual(len(guard.EXPECTED_PATHS), 48)
        self.assertEqual(len(guard.PINS), 48)
        self.assertIn("io/platform_windows.py", guard.EXPECTED_PATHS)
        self.assertIn("contracts/execution.py", guard.EXPECTED_PATHS)

    def test_extra_module_and_data_each_fail(self):
        for name in ("extra.py", "stored_answers.json", "native.so", "startup.pth"):
            path = self.package / name
            path.write_text("{}")
            with self.subTest(path=name):
                self.assertFalse(guard.check_repository(self.root)["ok"])
            path.unlink()

    def test_missing_slot_fails(self):
        (self.package / "analysis/origins.py").unlink()
        self.assertFalse(guard.check_repository(self.root)["ok"])

    def test_executable_body_is_detected_without_hash_check(self):
        for source in ('def calculate(x):\n    return 1\n', 'REGISTRY = {}\n',
                       'from pathlib import Path\nPath("x").read_bytes()\n',
                       'exec("pass")\n', 'import ctypes\n',
                       'if False:\n    import requests\n',
                       'class Node:\n    pass\n'):
            with self.subTest(source=source):
                self.assertIn("non_scaffold_body", guard.form_issues("analysis/origins.py", source))

    def test_argument_inspection_before_refusal_fails_ast_and_tree(self):
        path = self.package / "api.py"
        source = path.read_text().replace('    raise NotImplementedError(',
                                         '    repr(options)\n    raise NotImplementedError(', 1)
        self.assertIn("non_scaffold_body", guard.form_issues("api.py", source))
        path.write_text(source)
        result = guard.check_repository(self.root)
        self.assertFalse(result["ok"])
        self.assertIn({"path": "api.py", "code": "non_scaffold_body"}, result["issues"])

    def test_decorator_default_and_annotation_side_effects_fail(self):
        sources = [
            '@print("x")\ndef audit_bundle(bundle, *, options=None):\n    raise NotImplementedError()\n',
            'def audit_bundle(bundle, *, options=open("x")):\n    raise NotImplementedError()\n',
            'def audit_bundle(bundle: print("x"), *, options=None):\n    raise NotImplementedError()\n',
        ]
        for source in sources:
            self.assertTrue(guard.form_issues("api.py", source))

    def test_cached_directory_cannot_hide_python_source(self):
        path = self.package / "__pycache__"
        path.mkdir(exist_ok=True)
        (path / "hidden.py").write_text("pass\n")
        self.assertFalse(guard.check_repository(self.root)["ok"])

    def test_changed_literal_or_fake_report_is_rejected(self):
        self.assertTrue(guard.form_issues("contracts/constants.py", 'SCAFFOLD_VERSION="1.0.0"'))
        self.assertTrue(guard.form_issues("api.py", 'def audit_bundle(bundle, *, options=None):\n    return {"status":"success"}\n'))

    def test_syntax_error_and_oversize_do_not_crash_guard(self):
        path = self.package / "graph/cycles.py"
        path.write_text("def (\n")
        self.assertFalse(guard.check_repository(self.root)["ok"])
        path.write_text("#" * 20000)
        self.assertFalse(guard.check_repository(self.root)["ok"])

    def test_extra_source_package_cannot_escape_inventory(self):
        (self.root / "src/shadow.py").write_text("pass\n")
        self.assertFalse(guard.check_repository(self.root)["ok"])

    def test_real_guard_cli_is_not_removed_by_python_optimization(self):
        command = [sys.executable, "-I", "-B", "-O", str(ROOT / "tools/check_scaffold_boundary.py"),
                   "--root", str(self.root)]
        positive = subprocess.run(command, capture_output=True, text=True, timeout=20)
        self.assertEqual(positive.returncode, 0, positive.stdout + positive.stderr)
        (self.package / "graph/cycles.py").write_text("ACTIVE = {}\n")
        negative = subprocess.run(command, capture_output=True, text=True, timeout=20)
        self.assertEqual(negative.returncode, 1)
        self.assertFalse(json.loads(negative.stdout)["ok"])


if __name__ == "__main__":
    unittest.main()
