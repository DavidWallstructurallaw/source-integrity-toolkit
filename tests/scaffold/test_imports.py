# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Scaffold import evidence only; no analytical Trace is implemented.

VALIDATION_GOVERNANCE: PHASE_1_PLAN.md sections 4 and 6.
The literal file list is the W02 allowlist, not a runtime module registry.
"""

import ast
import importlib
import os
from pathlib import Path
import subprocess
import sys

import pytest

PACKAGE_FILES = ('__init__.py', 'analysis/__init__.py', 'analysis/context.py', 'analysis/contribution_profile.py', 'analysis/correction_outcomes.py', 'analysis/correction_routes.py', 'analysis/evaluator_lineage.py', 'analysis/findings.py', 'analysis/human_review.py', 'analysis/inventory.py', 'analysis/origins.py', 'analysis/presence.py', 'analysis/process_comparison.py', 'api.py', 'cli.py', 'contracts/__init__.py', 'contracts/bundle.py', 'contracts/constants.py', 'contracts/evidence.py', 'contracts/execution.py', 'contracts/report.py', 'contracts/results.py', 'graph/__init__.py', 'graph/cycles.py', 'graph/projections.py', 'graph/traversal.py', 'graph/witnesses.py', 'io/__init__.py', 'io/input_file.py', 'io/output_directory.py', 'io/platform_linux.py', 'io/platform_windows.py', 'io/publication.py', 'reporting/__init__.py', 'reporting/assemble.py', 'reporting/escaping.py', 'reporting/json_report.py', 'reporting/markdown_report.py', 'runtime/__init__.py', 'runtime/boundary.py', 'runtime/diagnostics.py', 'runtime/disclosure.py', 'runtime/resources.py', 'validation/__init__.py', 'validation/limits.py', 'validation/references.py', 'validation/semantics.py', 'validation/structure.py')
ROOT = Path(__file__).resolve().parents[2]
PACKAGE_ROOT = ROOT / "src" / "source_integrity_toolkit"


def module_name(path):
    name = path.removesuffix(".py").replace("/", ".")
    if name == "__init__":
        return "source_integrity_toolkit"
    return "source_integrity_toolkit." + name.removesuffix(".__init__")


@pytest.mark.parametrize("path", PACKAGE_FILES)
def test_each_planned_module_imports(path):
    module = importlib.import_module(module_name(path))
    assert module.__doc__
    assert module.__file__.endswith(path.replace("/", os.sep))


def test_exact_package_file_set_and_inert_slots():
    assert {p.relative_to(PACKAGE_ROOT).as_posix() for p in PACKAGE_ROOT.rglob("*.py")} == set(PACKAGE_FILES)
    active = {"__init__.py", "api.py", "cli.py", "contracts/constants.py"}
    for relative in set(PACKAGE_FILES) - active:
        tree = ast.parse((PACKAGE_ROOT / relative).read_text(encoding="utf-8"))
        assert len(tree.body) == 1
        assert isinstance(tree.body[0], ast.Expr)
        assert isinstance(tree.body[0].value, ast.Constant)
        assert isinstance(tree.body[0].value.value, str)
        assert "behavior unimplemented" in tree.body[0].value.value


def test_fresh_imports_have_no_application_io_or_native_activity(tmp_path):
    modules = [module_name(p) for p in PACKAGE_FILES]
    script = r'''import importlib, os, sys
sys.dont_write_bytecode = True
modules = %r

def guard(event, args):
    if event == "open":
        path, mode, flags = args
        if not isinstance(path, str) or not path.endswith((".py", ".pyc")):
            raise AssertionError("Non-module read during scaffold import")
        if flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND):
            raise AssertionError("Write during scaffold import")
    if event.startswith(("socket.", "subprocess.", "ctypes.")):
        raise AssertionError("Network/process/native activity during import")
    if event in ("os.system", "os.putenv", "os.chdir", "os.mkdir", "os.remove", "os.rename"):
        raise AssertionError("Application mutation during import")

sys.addaudithook(guard)
for name in modules:
    importlib.import_module(name)
for forbidden in ("ctypes", "recursive_integrity_toolkit", "requests", "httpx", "pydantic", "networkx"):
    assert forbidden not in sys.modules, forbidden
print("IMPORTS_INERT")
''' % modules
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONDONTWRITEBYTECODE": "1"}
    proc = subprocess.run([sys.executable, "-B", "-S", "-c", script], cwd=tmp_path,
                          env=env, capture_output=True, text=True, timeout=30)
    assert proc.returncode == 0, proc.stderr
    assert proc.stdout == "IMPORTS_INERT\n"
    assert proc.stderr == ""
    assert not list(tmp_path.iterdir())
