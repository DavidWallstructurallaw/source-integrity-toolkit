# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Historical catalog and current phase authority remain separate."""
from pathlib import Path
import sys
import subprocess
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools import check_scaffold_boundary as phase_guard
phase_guard.load_phase1_test("tests/scaffold/test_module_manifest.py", globals())
_phase1_verify_manifest = verify_manifest


def verify_manifest(manifest, files, owners):
    active = phase_guard.promotions(ROOT)
    historical = dict(files)
    for path in active:
        require(path in files, "Missing live slot")
        raw = subprocess.check_output(["git", "show", phase_guard.INTAKE + ":" + PREFIX + path], cwd=ROOT)
        require(blob(raw) == dict(phase_guard.PINS)[path], "Historical module bytes mismatch")
        historical[path] = raw
    _phase1_verify_manifest(manifest, historical, owners)
    for path in active:
        source = files[path].decode("utf-8")
        require(not phase_guard.live_issues(path, source), "Forbidden live-module behavior")
        annotation = re.search(r"Owner: ([^\n]+)", source)
        require(annotation is not None, "Missing live owner annotation")
        row = next(r for r in manifest["modules"] if r[0] == path)
        require({owner for owner in owners if owner in annotation[1]} == set(row[2]), "Live owner mismatch")
    require(not phase_guard.import_cycle_issues({p: raw.decode("utf-8") for p, raw in files.items()}), "Live import cycle")


# P3-W05-R01 preserves the original node and its unchanged inert-slot assertion.
_phase1_test_mutated_product_bytes_are_rejected = ModuleManifestTests.test_mutated_product_bytes_are_rejected


def _current_test_mutated_product_bytes_are_rejected(self):
    bad = dict(self.files)
    bad["reporting/json_report.py"] += b"\ndef analyze():\n    return 42\n"
    with self.assertRaises(AssertionError):
        verify_manifest(self.manifest, bad, self.owners)


ModuleManifestTests.test_mutated_product_bytes_are_rejected = _current_test_mutated_product_bytes_are_rejected


class LiveModuleManifestTests(unittest.TestCase):
    """Actual live-body/effect/owner controls, separate from historical bytes."""

    @classmethod
    def setUpClass(cls):
        ModuleManifestTests.setUpClass.__func__(cls)

    def _assert_live_effect_control(self, path):
        self.assertIn(path, phase_guard.promotions(ROOT))
        verify_manifest(self.manifest, self.files, self.owners)
        legal = dict(self.files)
        legal[path] += b"\ndef analyze():\n    return 42\n"
        verify_manifest(self.manifest, legal, self.owners)
        bad = dict(self.files)
        bad[path] += b'\ndef analyze():\n    return open("synthetic-canary")\n'
        with self.assertRaises(AssertionError):
            verify_manifest(self.manifest, bad, self.owners)
        verify_manifest(self.manifest, self.files, self.owners)

    def _assert_live_owner_control(self, path):
        self.assertIn(path, phase_guard.promotions(ROOT))
        verify_manifest(self.manifest, self.files, self.owners)
        legal = dict(self.files)
        legal[path] += b"\ndef analyze():\n    return 42\n"
        verify_manifest(self.manifest, legal, self.owners)
        original = self.files[path].decode("utf-8")
        self.assertIsNotNone(re.search(r"Owner: ([^\n]+)", original))
        missing = dict(self.files)
        missing[path] = re.sub(r"Owner: [^\n]+", "Ownership omitted", original, count=1).encode("utf-8")
        with self.assertRaises(AssertionError):
            verify_manifest(self.manifest, missing, self.owners)
        verify_manifest(self.manifest, self.files, self.owners)
        wrong = dict(self.files)
        wrong[path] = re.sub(r"Owner: [^\n]+", "Owner: REPORT_CONTRACT", original, count=1).encode("utf-8")
        with self.assertRaises(AssertionError):
            verify_manifest(self.manifest, wrong, self.owners)
        verify_manifest(self.manifest, self.files, self.owners)

    def test_inventory_live_body_and_effect(self):
        self._assert_live_effect_control("analysis/inventory.py")

    def test_origins_live_body_and_effect(self):
        self._assert_live_effect_control("analysis/origins.py")

    def test_inventory_owner_annotation(self):
        self._assert_live_owner_control("analysis/inventory.py")

    def test_origins_owner_annotation(self):
        self._assert_live_owner_control("analysis/origins.py")

    def test_unchanged_baseline_keeps_all_module_and_owner_rows(self):
        verify_manifest(self.manifest, self.files, self.owners)
        self.assertEqual(set(self.files), EXPECTED)
        self.assertEqual(len(self.files), 48)
        self.assertEqual({row[0] for row in self.manifest["modules"]}, EXPECTED)
        self.assertEqual({row[0] for row in self.manifest["owner_bindings"]}, set(HOMES))
        self.assertEqual(len(self.manifest["owner_bindings"]), 19)


if __name__ == "__main__":
    unittest.main()
