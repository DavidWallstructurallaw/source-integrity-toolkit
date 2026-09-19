# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Retain Phase 1 import assertions; migrate only authorized slot forms."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools import check_scaffold_boundary as phase_guard
phase_guard.load_phase1_test("tests/scaffold/test_imports.py", globals())


def test_exact_package_file_set_and_inert_slots():
    assert {p.relative_to(PACKAGE_ROOT).as_posix() for p in PACKAGE_ROOT.rglob("*.py")} == set(PACKAGE_FILES)
    active = phase_guard.promotions(ROOT)
    for relative in set(PACKAGE_FILES) - {"__init__.py", "api.py", "cli.py", "contracts/constants.py"}:
        source = (PACKAGE_ROOT / relative).read_text(encoding="utf-8")
        if relative in active:
            assert not phase_guard.live_issues(relative, source)
        else:
            tree = ast.parse(source)
            assert len(tree.body) == 1
            assert isinstance(tree.body[0], ast.Expr)
            assert isinstance(tree.body[0].value, ast.Constant)
            assert isinstance(tree.body[0].value.value, str)
            assert "behavior unimplemented" in tree.body[0].value.value
    result = phase_guard.check_repository(ROOT)
    assert result["ok"], result
