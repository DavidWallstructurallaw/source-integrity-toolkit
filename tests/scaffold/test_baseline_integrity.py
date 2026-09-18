# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Tests of the developer freeze guard, not a source-integrity analysis.

Full-checkout invocation: python tools/check_phase0_baseline.py.
Synthetic twenty-file workspaces test the entire guard without needing to copy
or alter frozen project files. Real reference bytes are tested separately.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools import check_phase0_baseline as guard


def digest_row(path: str, data: bytes) -> dict:
    # Independent standard hash calculation; never derive expected bytes from a
    # mutated checkout or from a guard's returned 'actual' metadata.
    return {"path": path, "bytes": len(data),
            "sha256": hashlib.sha256(data).hexdigest(),
            "git_blob_sha1": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()}


class BaselineGuardTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        # The guard's repository contract has eighteen named files and a fixed
        # aggregate byte count. Synthetic padding meets the same dimensions;
        # none of these strings is presented as a real approved specification.
        rows = []
        names = sorted(guard.BASELINE_NAMES)
        for index, name in enumerate(names):
            size = 1 if index < 17 else 1094920 - 17
            data = b"X" * size
            (self.root / name).write_bytes(data)
            rows.append(digest_row(name, data))
        extras = []
        for name in ("PHASE_0_APPROVAL.md", "PHASE_1_PLAN.md"):
            data = ("SYNTHETIC TEST CONTROL " + name + "\n").encode()
            (self.root / name).write_bytes(data)
            extras.append(digest_row(name, data))
        self.manifest = {"approved_phase0_commit": guard.APPROVED_COMMIT,
                         "baseline_files": rows, "approval_record": extras[0],
                         "approved_phase1_plan": extras[1]}
        (self.root / "scaffold").mkdir()
        raw = (json.dumps(self.manifest, indent=2) + "\n").encode()
        (self.root / guard.MANIFEST_PATH).write_bytes(raw)
        # Test-only trust anchor for the independently constructed synthetic
        # fixture. The real CLI exposes no anchor override or repair switch.
        pin = digest_row("manifest", raw)["git_blob_sha1"]
        self.patch = mock.patch.object(guard, "MANIFEST_BLOB", pin)
        self.patch.start()
        self.addCleanup(self.patch.stop)

    def test_synthetic_complete_twenty_file_positive(self):
        result = guard.check_repository(self.root)
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["checked_files"], 20)

    def test_single_changed_byte_is_rejected(self):
        name = sorted(guard.BASELINE_NAMES)[0]
        (self.root / name).write_bytes(b"Y")
        result = guard.check_repository(self.root)
        self.assertFalse(result["ok"])
        self.assertIn({"path": name, "code": "sha256_mismatch"}, result["issues"])

    def test_missing_file_is_not_a_pass(self):
        (self.root / "PHASE_0_APPROVAL.md").unlink()
        self.assertFalse(guard.check_repository(self.root)["ok"])

    def test_changed_approval_and_plan_each_fail(self):
        for name in ("PHASE_0_APPROVAL.md", "PHASE_1_PLAN.md"):
            path = self.root / name
            original = path.read_bytes()
            with self.subTest(path=name):
                path.write_bytes(original + b" ")
                self.assertFalse(guard.check_repository(self.root)["ok"])
            path.write_bytes(original)

    def test_editing_file_and_manifest_cannot_self_approve(self):
        row = self.manifest["baseline_files"][0]
        data = b"Y" * row["bytes"]
        (self.root / row["path"]).write_bytes(data)
        row.update(digest_row(row["path"], data))
        (self.root / guard.MANIFEST_PATH).write_text(json.dumps(self.manifest))
        result = guard.check_repository(self.root)
        self.assertFalse(result["ok"])
        self.assertEqual(result["checked_files"], 0)

    def test_newline_conversion_is_detected(self):
        name = "PHASE_1_PLAN.md"
        path = self.root / name
        path.write_bytes(path.read_bytes().replace(b"\n", b"\r\n"))
        self.assertFalse(guard.check_repository(self.root)["ok"])

    def test_duplicate_key_parser_rejects(self):
        with self.assertRaises(ValueError):
            json.loads('{"path":1,"path":2}', object_pairs_hook=guard.unique_object)

    def test_unsafe_and_nonregular_inputs_fail(self):
        row = digest_row("../escape", b"x")
        self.assertTrue(guard.check_entry(self.root, row))
        path = self.root / "directory.md"
        path.mkdir()
        self.assertTrue(guard.check_entry(self.root, digest_row("directory.md", b"")))

    def test_actual_pinned_manifest_is_accepted_without_override(self):
        with mock.patch.object(guard, "MANIFEST_BLOB", "da48da62c4d1dd8e27af43daa0ecdc8e6c4698d8"):
            manifest = guard.load_manifest(ROOT)
        self.assertEqual(len(manifest["baseline_files"]), 18)
        self.assertEqual(manifest["approval_record"]["revision"], "1.1")

    def test_actual_reference_document_exact_bytes(self):
        # This complete real source exists in both the controlled W05 local view
        # and the full repository. The full twenty-file check is a separate CLI
        # invocation; this unit method does not claim to have run that command.
        row = {"path": "DEFINITIONS_AND_UNITS.md", "bytes": 94436,
               "sha256": "913697e733d4430a64696b36a7893fe2113da7e2cfbcadbb54247a36c1792e9d",
               "git_blob_sha1": "36fd49115cd7a3a85be93eeeb480042a1b74496f"}
        self.assertEqual(guard.check_entry(ROOT, row), [])

    def test_empty_checkout_cli_fails_even_under_optimization(self):
        result = subprocess.run([sys.executable, "-I", "-B", "-O",
                                 str(ROOT / "tools/check_phase0_baseline.py"),
                                 "--root", str(self.root / "absent")],
                                capture_output=True, text=True, timeout=20)
        self.assertEqual(result.returncode, 1)
        self.assertFalse(json.loads(result.stdout)["ok"])


if __name__ == "__main__":
    unittest.main()
