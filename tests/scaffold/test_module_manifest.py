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


if __name__ == "__main__":
    unittest.main()
