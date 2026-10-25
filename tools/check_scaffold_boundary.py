# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Developer-only current boundary checks; never imported by the product.

The accepted anchor, approved plan, fixed module inventory, external event
context, static checks and behavioral tests are separate controls. A candidate
policy cannot authorize additional paths or modules. This checker is not
a proof against an actor who also replaces the checker or trusted CI context.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
import re
import stat
import subprocess
import xml.etree.ElementTree as ET
from graphlib import CycleError, TopologicalSorter
from pathlib import Path

PACKAGE = "source_integrity_toolkit"
PIN_TEXT = """__init__.py 7bea94e138804cbeea4048ef152dcb5726047f1f
api.py 0603b4de9888a51190eeeefc6186b47e2afd88bd
cli.py f48f869385fbeb711458f0189ff55194f73fd050
analysis/__init__.py 39f3b82fbbe9c331b5728e9366d08ad5b6750a0c
analysis/context.py e45bc4485a1c7706c7c706af04c590732aef0f7a
analysis/contribution_profile.py 1380f92bf538148065fb2ee85d637ff4930944b8
analysis/correction_outcomes.py 125710879eafc46df6c1a62837fa4cabc65af56c
analysis/correction_routes.py 601820c1974f054176f4fbb937e05663fc66299a
analysis/evaluator_lineage.py ad8e0d6a447aaa4dd9522a149a7492071ffc2d30
analysis/findings.py cf6fe8419f58428e59c3e825f056d35a416ac160
analysis/human_review.py ee0359eca52f2df943ac8fff36ff71e06a887e69
analysis/inventory.py 0270bc2176369b526900673eb12e41772374bb5a
analysis/origins.py ff717183ec59983be24438a11a0ca8cc519d6108
analysis/presence.py e4d562ba405ab835ea6f18491cee5799cfd11fd8
analysis/process_comparison.py dca02534d562be02ffb43ef6142db7706471f73d
contracts/__init__.py df81f7b32eee0e54a4606b3dd02332407cf53ec1
contracts/bundle.py d26a26bfc00b2598a72a65e4091c6b2b7c0e23e9
contracts/constants.py 3744f9513f12ddd7ea3201142e1597fcd0168594
contracts/evidence.py 96876269604d2a91db04091048dcb3e312642b05
contracts/execution.py 08c594d1d79dc9cb83f2d32317faccb5ed823846
contracts/report.py 7ea8f74a471c2b09086b13d1e504ba0476dc12bf
contracts/results.py 728f573ed6540d943c3b8a40a0456cc482a160d9
graph/__init__.py d5eff5c90ff209f6f3f6b3d53b1a38d292da413e
graph/cycles.py 79148cf330f7e8a0da4bf99ac672308c05633419
graph/projections.py ba97838466377f0db4a6b10bffe924dab0dea106
graph/traversal.py 48a07d5e50f70f0fa9e6e9bcc84d6d83856973bf
graph/witnesses.py d0a47364b84326e74f0cd4e71aec780a4a4ba4d8
io/__init__.py 2714a56fb4d2ed55cf66934c8a336f0d5a51944e
io/input_file.py 594486c13130bcebe18b08aa0e16bab56762c073
io/output_directory.py 9e974acb4ae4afe96a2dfb090dfd459effc8f7cb
io/platform_linux.py 6e7c6196ec22baa91a75ced2aba8de831d03f364
io/platform_windows.py b1023ff2d960f1a7b0374c46b57069957c807e2f
io/publication.py e86a93eedb87b56809977b1c038958c41e70a6a8
reporting/__init__.py f3070404ece65e7eb26d4cfbc1ce11eb7f02d57c
reporting/assemble.py c90193c4aceba2ab971cc960fbf370a775beaa64
reporting/escaping.py a33d2f6e6bc0840f3037f7a6376cabf581251c87
reporting/json_report.py fa7905d6743818af64d7d61b0a5bfcf5be17159a
reporting/markdown_report.py c6c31013559720421645b69c756e7cb137a28c33
runtime/__init__.py 830e640c62a1ce89f5425a17c9f225332d24a751
runtime/boundary.py 486b795aef999abe3c564975cd6628b6ca58b77c
runtime/diagnostics.py d5f1edae68fac8f4fd9b18501349c0eeaf21c7cd
runtime/disclosure.py b543c75e314fc21b09799ed32ca913cf03d33157
runtime/resources.py f3b02b43e9e327ab4a4b041ea95924f946ffce18
validation/__init__.py 775fff4175affb1c95a682423fc9c06317321e8e
validation/limits.py 80bcee9c4ba5966502724c09c3995f8ed59cf4a8
validation/references.py 985ff2ddd8506e1f889f8227d4aeb06f2274b86d
validation/semantics.py c49d712867ead29d92eaef5c4c7a16d715a10ba3
validation/structure.py 7f61b244d272cd2aa1b23c2a9af9bc61b371196d"""
PINS = tuple(tuple(line.split()) for line in PIN_TEXT.splitlines())
EXPECTED_PATHS = frozenset(p for p, _ in PINS)
LAYER_PERMISSIONS = {
    "contracts": frozenset(("contracts",)),
    "validation": frozenset(("validation", "contracts")),
    "graph": frozenset(("graph", "contracts", "validation")),
    "analysis": frozenset(("analysis", "contracts", "validation", "graph")),
    "reporting": frozenset(("reporting", "contracts")),
    "runtime": frozenset(("runtime", "io", "contracts", "validation", "graph", "analysis", "reporting")),
    "io": frozenset(("io", "runtime", "contracts", "validation", "graph", "analysis", "reporting")),
    "composition": frozenset(("contracts", "runtime", "io", "validation", "graph", "analysis", "reporting")),
    "exports": frozenset(("composition", "contracts")),
}
REFUSAL = "Source Integrity Toolkit audit is not implemented in the Phase 1 scaffold."
HELP = """Source Integrity Toolkit: Phase 1 scaffold

Usage:
  sit --help
  sit --version
  sit audit INPUT --output OUTPUT_DIR [--raw-file-digest]

Audit functionality is not implemented. Audit requests exit 1 without reading
input, inspecting paths, or producing a report. This temporary refusal is not
a sit-report/0.1 processing result. The audit grammar is reserved for later work.
"""
API_FORM = f'''from typing import NoReturn

def audit_bundle(bundle: object, *, options: object = None) -> NoReturn:
    raise NotImplementedError({REFUSAL!r})

def audit_file(input_path: object, output_directory: object, *, options: object = None) -> NoReturn:
    raise NotImplementedError({REFUSAL!r})
'''
CLI_FORM = f'''import sys
from .contracts.constants import SCAFFOLD_VERSION
_HELP = {HELP!r}
_REFUSAL = {REFUSAL!r}

def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if args in ([], ["--help"], ["-h"], ["audit", "--help"], ["audit", "-h"]):
        print(_HELP, end="")
        return 0
    if args == ["--version"]:
        print(f"source-integrity-toolkit {{SCAFFOLD_VERSION}}")
        return 0
    print(_REFUSAL, file=sys.stderr)
    return 1

if __name__ == "__main__":
    raise SystemExit(main())
'''
SPECIAL_FORMS = {
    "api.py": API_FORM, "cli.py": CLI_FORM,
    "contracts/constants.py": 'SCAFFOLD_VERSION = "0.1.0.dev0"',
    "__init__.py": '''from .api import audit_bundle, audit_file
from .contracts.constants import SCAFFOLD_VERSION as __version__
__all__ = ("audit_bundle", "audit_file", "__version__")''',
}
SAFE_IMPORTS = frozenset(("__future__", "typing", "dataclasses", "enum", "math", "json", "re",
    "decimal", "fractions", "collections", "bisect", "types", "unicodedata", "datetime"))
FORBIDDEN_NAMES = frozenset(("open", "eval", "exec", "compile", "__import__", "globals", "locals",
    "getattr", "setattr", "delattr", "vars", "print", "input", "breakpoint"))
FORBIDDEN_ATTRS = frozenset(("read_text", "read_bytes", "write_text", "write_bytes", "load", "dump",
    "CDLL", "WinDLL", "PyDLL", "dlopen", "connect", "getaddrinfo", "urlopen", "system", "popen"))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate_policy_key")
        result[key] = value
    return result


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def executable_ast(source):
    tree = ast.parse(source)
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if node.body and isinstance(node.body[0], ast.Expr) and isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str):
                node.body.pop(0)
    return tree


def module_name(path):
    parts = path.removesuffix(".py").split("/")
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join((PACKAGE, *parts))


def layer(path):
    return "exports" if path == "__init__.py" else path.split("/", 1)[0] if "/" in path else "composition"


def import_targets(path, tree):
    targets, issues = [], []
    module = module_name(path)
    parent = module if path.endswith("__init__.py") else module.rpartition(".")[0]
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            targets.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if any(alias.name == "*" for alias in node.names):
                issues.append("wildcard_import")
            if node.level:
                parts = parent.split(".")
                if node.level > len(parts):
                    issues.append("relative_import_escape")
                    continue
                target = ".".join(parts[:len(parts) - node.level + 1] + ([node.module] if node.module else []))
            else:
                target = node.module or ""
            targets.append(target)
            if not node.module:
                targets.extend(target + "." + alias.name for alias in node.names)
    return targets, issues


def _phase2_layer_issues(path, source, *, live=False):
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError, RecursionError):
        return ["invalid_python"]
    targets, issues = import_targets(path, tree)
    by_name = {module_name(p): p for p in EXPECTED_PATHS}
    for target in targets:
        if target in ("sys", "typing"):
            if live and target == "sys":
                issues.append("unapproved_import")
            continue
        if live and (target in SAFE_IMPORTS or (path == "runtime/resources.py" and target == "time")):
            continue
        if target not in by_name:
            issues.append("unapproved_import")
            continue
        if layer(by_name[target]) not in LAYER_PERMISSIONS[layer(path)]:
            issues.append("layer_violation")
        if live and (by_name[target].startswith(("analysis/", "graph/", "reporting/")) or
                     by_name[target] in ("io/platform_linux.py", "io/platform_windows.py", "io/publication.py", "io/output_directory.py", "api.py", "cli.py")):
            issues.append("phase2_forbidden_dependency")
    return sorted(set(issues))


def form_issues(path, source):
    if path not in EXPECTED_PATHS:
        return ["unexpected_module"]
    try:
        tree, expected = executable_ast(source), executable_ast(SPECIAL_FORMS.get(path, ""))
    except (SyntaxError, ValueError, RecursionError):
        return ["invalid_python"]
    return [] if ast.dump(tree, include_attributes=False) == ast.dump(expected, include_attributes=False) else ["non_scaffold_body"]


# Pre-acceptance stage schedules and identity quotas are archived in Git.
# Current source dependency and effect checks below remain active.


def promotions(root, unit=None):
    """Explicit package probe only; this does not authorize a Git checkout."""
    require(type(unit) is str and re.fullmatch(r"P4-W(?:0[1-9]|10)", unit),
            "current_external_context_required")
    return current_active(int(unit[-2:]))

def phase3_import_targets(path, tree):
    """Resolve real module aliases, including from package import future_slot."""
    targets, issues = import_targets(path, tree)
    known = {module_name(p) for p in EXPECTED_PATHS}
    module = module_name(path)
    parent = module if path.endswith("__init__.py") else module.rpartition(".")[0]
    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom):
            continue
        if node.level:
            parts = parent.split(".")
            if node.level > len(parts):
                continue
            target = ".".join(parts[:len(parts) - node.level + 1] + ([node.module] if node.module else []))
        else:
            target = node.module or ""
        for alias in node.names:
            child = target + "." + alias.name
            if child in known:
                targets.append(child)
    return targets, issues


def _dependency_issues(path, source, active, prefix="", *, stage=1):
    """Current source dependencies; no historical policy or Git test loading."""
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError, RecursionError):
        return ["invalid_python"]
    targets, issues = phase3_import_targets(path, tree)
    return _dependency_target_issues(path, targets, issues, active, prefix, stage=stage)


def _dependency_target_issues(path, targets, import_issues, active, prefix="", *, stage=1):
    """Apply every dependency rule to targets parsed by the current caller."""
    issues = list(import_issues)
    by_name = {module_name(p): p for p in EXPECTED_PATHS}
    for target in targets:
        if target in SAFE_IMPORTS or (path == "runtime/resources.py" and target == "time"):
            continue
        if target not in by_name:
            issues.append("unapproved_import")
            continue
        dependency = by_name[target]
        if layer(dependency) not in LAYER_PERMISSIONS[layer(path)]:
            issues.append("layer_violation")
        if (path == "runtime/boundary.py" and stage < 7 and
                (dependency.startswith("reporting/") or dependency == "runtime/disclosure.py")) or dependency in ("io/output_directory.py", "io/publication.py",
                "io/platform_linux.py", "io/platform_windows.py", "cli.py", "__init__.py") or (
                dependency == "api.py" and path != "__init__.py") or (
                (dependency.startswith("reporting/") or dependency == "runtime/disclosure.py")
                and dependency not in active and not dependency.endswith("/__init__.py")):
            issues.append(prefix + "forbidden_dependency")
        elif dependency not in active and not dependency.endswith("/__init__.py"):
            issues.append(prefix + "unpromoted_dependency")
    return sorted(set(issues))


def phase3_import_cycle_issues(sources):
    targets_by_path = {}
    for path, source in sources.items():
        try:
            targets, _ = phase3_import_targets(path, ast.parse(source))
        except (SyntaxError, ValueError, RecursionError):
            return ["invalid_python"]
        targets_by_path[path] = targets
    return _import_target_cycle_issues(targets_by_path)


def _import_target_cycle_issues(targets_by_path):
    by_name = {module_name(p): p for p in targets_by_path}
    dependencies = {path: {by_name[t] for t in targets if t in by_name}
                    for path, targets in targets_by_path.items()}
    try:
        tuple(TopologicalSorter(dependencies).static_order())
    except CycleError:
        return ["import_cycle"]
    return []


def _source_effect_issues(path, source):
    """Conservative static effect checks, independent of development stage."""
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError, RecursionError):
        return ["invalid_python"]
    return _source_tree_effect_issues(path, tree)


def _source_tree_effect_issues(path, tree):
    """Read-only checks on this invocation's freshly parsed source tree."""
    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in FORBIDDEN_NAMES:
            issues.append("forbidden_effect")
        if isinstance(node, ast.Attribute) and (node.attr in FORBIDDEN_ATTRS or node.attr.startswith("__")):
            issues.append("forbidden_effect")
        if isinstance(node, (ast.AsyncFunctionDef, ast.Await)):
            issues.append("async_execution_not_selected")
        if isinstance(node, ast.ClassDef) and node.keywords:
            issues.append("custom_metaclass")
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and any(s in node.value for s in ("tests/golden/", "tests/fixtures/", "schemas/", "scaffold/", "phase2/", "phase3/", "module_manifest.json", "trace_catalog.json", "obligation_catalog.json")):
            issues.append("runtime_catalog_or_oracle_reference")
    for node in tree.body:
        if not isinstance(node, (ast.Import, ast.ImportFrom, ast.FunctionDef, ast.ClassDef, ast.Assign, ast.AnnAssign, ast.Expr)):
            issues.append("import_time_execution")
        if isinstance(node, ast.Expr) and not (isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)):
            issues.append("import_time_execution")
    # Only named pure declaration helpers may run at module definition time.
    # This intentionally conservative whitelist does not certify helper semantics.
    definitions = (ast.FunctionDef, ast.AsyncFunctionDef)
    roots = []
    for node in tree.body:
        if isinstance(node, definitions):
            roots.extend(node.decorator_list)
            roots.extend(node.args.defaults)
            roots.extend(d for d in node.args.kw_defaults if d is not None)
            roots.extend(a.annotation for a in node.args.args + node.args.kwonlyargs if a.annotation is not None)
            if node.returns is not None:
                roots.append(node.returns)
        elif isinstance(node, ast.ClassDef):
            roots.extend(node.bases + node.decorator_list)
            roots.extend(n for n in node.body if not isinstance(n, definitions))
        elif isinstance(node, (ast.Assign, ast.AnnAssign)):
            roots.append(node)
    for root in roots:
        for node in ast.walk(root):
            if isinstance(node, ast.Call) and not (isinstance(node.func, ast.Name) and node.func.id in
                    {"dataclass", "field", "frozenset", "tuple", "MappingProxyType", "NamedTuple"}):
                issues.append("import_time_execution")
    if path == "contracts/constants.py":
        values = [n.value.value for n in tree.body if isinstance(n, ast.Assign) and isinstance(n.value, ast.Constant)
                  and any(isinstance(t, ast.Name) and t.id == "SCAFFOLD_VERSION" for t in n.targets)]
        if values != ["0.1.0.dev0"]:
            issues.append("scaffold_version_changed")
    return sorted(set(issues))


def check_repository(root, *, unit=None):
    """Explicit package-only compatibility; never grants checkout authority."""
    if type(unit) is not str or re.fullmatch(r"P4-W(?:0[1-9]|10)", unit) is None:
        return {"ok": False, "checked_modules": 0,
                "issues": [{"code": "current_external_context_required"}]}
    return current_check_repository(root, int(unit[-2:]))

# Owner-approved Phase 4 ceiling, transcribed once from the exact plan.
# Candidate records cannot authorize paths; pre-anchor test code is never loaded.
P4_ACCEPTED_HEAD = "fdad8c3449d2d223420c5d52bb9b4c1e863a9e3c"
P4_ACCEPTED_TREE = "f6fbb8965520f33a09ca38cf413e11ca561110dd"
P4_ACCEPTED_PARENTS = (
    "2413a29b839b7e1de8f76a449762f031de19d52b",
    "ce05c5dda9368182dbee074253d3a7c829af7719",
)
P4_PLAN = "PHASE_4_PLAN.md"
P4_PLAN_SHA256 = "5fac7a2a796338faae9b98af6e0cc4519396e378ba10b8c5afeb4d029d97cd48"
P4_REPOSITORY = "DavidWallstructurallaw/source-integrity-toolkit"
P4_BRANCH = "phase4/public-report"
P4_SUITE_TIMEOUT = 2400
P4_PATH_IDS = {'P01': 'src/source_integrity_toolkit/contracts/report.py',
 'P02': 'src/source_integrity_toolkit/contracts/execution.py',
 'P03': 'src/source_integrity_toolkit/reporting/assemble.py',
 'P04': 'src/source_integrity_toolkit/runtime/disclosure.py',
 'P05': 'src/source_integrity_toolkit/reporting/escaping.py',
 'P06': 'src/source_integrity_toolkit/reporting/json_report.py',
 'P07': 'src/source_integrity_toolkit/reporting/markdown_report.py',
 'P08': 'src/source_integrity_toolkit/runtime/resources.py',
 'P09': 'src/source_integrity_toolkit/runtime/diagnostics.py',
 'P10': 'src/source_integrity_toolkit/runtime/boundary.py',
 'P11': 'src/source_integrity_toolkit/api.py',
 'P12': 'src/source_integrity_toolkit/__init__.py',
 'V01': 'tools/check_scaffold_boundary.py',
 'V02': 'tests/contract/test_verification_boundary.py',
 'V03': 'tests/scaffold/test_ci_contract.py',
 'V04': 'tests/scaffold/test_imports.py',
 'V05': 'tests/scaffold/test_module_manifest.py',
 'V06': 'tests/scaffold/test_no_runtime_implementation.py',
 'V07': 'tests/scaffold/test_layer_boundaries.py',
 'V08': '.github/workflows/phase1-ci.yml',
 'T01': 'tests/scaffold/test_api_stubs.py',
 'T02': 'tests/scaffold/test_packaging.py',
 'T03': 'tests/security/test_scaffold_inertness.py',
 'T04': 'tests/security/test_preparation_inertness.py',
 'T05': 'tests/integration/test_preparation_capability_boundary.py',
 'T06': 'tests/contract/test_analytical_observability.py',
 'T07': 'tests/contract/test_phase2_transition.py',
 'T08': 'tests/integration/test_analytical_installed_runtime.py',
 'T09': 'tests/contract/test_phase3_transition.py',
 'T10': 'tests/contract/test_input_schema_mapping.py',
 'T11': 'tests/scaffold/test_contract_catalogs.py',
 'N01': 'tests/contract/test_report_contract.py',
 'N02': 'tests/contract/test_report_assembly.py',
 'N03': 'tests/contract/test_report_identity.py',
 'N04': 'tests/contract/test_json_report.py',
 'N05': 'tests/contract/test_report_parity.py',
 'N06': 'tests/contract/test_public_api.py',
 'N07': 'tests/contract/test_public_report_obligations.py',
 'N08': 'tests/security/test_report_disclosure.py',
 'N09': 'tests/security/test_rendering.py',
 'N10': 'tests/security/test_report_resource_limits.py',
 'N11': 'tests/security/test_public_api_boundary.py',
 'N12': 'tests/integration/test_public_audit.py',
 'N13': 'tests/integration/test_report_determinism.py',
 'N14': 'tests/integration/test_public_installed_runtime.py',
 'N15': 'tests/fixtures/micro/phase4_public_cases.json',
 'N16': 'tests/fixtures/adversarial/phase4_report_cases.json',
 'N17': 'tests/golden/phase4_report_expectations.json',
 'N18': 'tests/golden/phase4_reference_report.json',
 'N19': 'tests/golden/phase4_reference_report.md',
 'N20': 'tests/contract/test_report_test_oracles.py',
 'D01': 'PHASE_4_PLAN.md',
 'D02': 'schemas/report/sit-report-0.1.schema.json',
 'D03': 'schemas/report/README.md',
 'D04': 'phase4/report_contract_coverage.json',
 'D05': 'phase4/implementation_evidence.json',
 'D06': 'phase4/ci_review.md',
 'D07': 'PHASE_4_COMPLETION.md',
 'D08': 'README.md'}
P4_UNIT_IDS = {1: 'V01 V02 V03 V04 V05 V06 V07 V08 T04 T07 T08 T09 D01 D04 D05 D06 D08',
 2: 'P01 P02 T10 T11 N01 N15 N17 N18 N19 N20 D02 D03 D04 D05',
 3: 'P01 P03 N01 N02 N03 N15 N17 N20 D04 D05',
 4: 'P01 P03 P04 N02 N08 N15 N16 N17 N20 D04 D05',
 5: 'P01 P02 P05 P06 P08 P09 N04 N10 N16 N17 N18 N20 D04 D05',
 6: 'P05 P07 N05 N09 N10 N16 N17 N19 N20 D04 D05',
 7: 'P01 P02 P03 P04 P05 P06 P07 P08 P09 P10 N01 N02 N08 N10 N11 N12 N15 N16 D04 D05',
 8: 'P01 P02 P10 P11 P12 V03 T01 T02 T03 T05 T06 T07 T08 N06 N11 N12 N14 N15 N16 D04 D05 D08',
 9: 'N01 N02 N03 N04 N05 N06 N07 N08 N09 N10 N11 N12 N13 N15 N16 N17 N18 N19 N20 D04 D05',
 10: 'N14 D04 D05 D06 D07 D08'}
P4_PATHS = frozenset(P4_PATH_IDS.values())
P4_UNIT_PATHS = {n: frozenset(P4_PATH_IDS[key] for key in keys.split())
                 for n, keys in P4_UNIT_IDS.items()}
P4_ACTIVATION = {
    "contracts/report.py": 2, "contracts/execution.py": 2,
    "reporting/assemble.py": 3, "runtime/disclosure.py": 4,
    "reporting/escaping.py": 5, "reporting/json_report.py": 5,
    "runtime/resources.py": 5, "runtime/diagnostics.py": 5,
    "reporting/markdown_report.py": 6, "runtime/boundary.py": 7,
    "api.py": 8, "__init__.py": 8,
}
P4_BASE_ACTIVE = frozenset("""contracts/bundle.py contracts/evidence.py contracts/constants.py
contracts/execution.py contracts/report.py contracts/results.py validation/limits.py
validation/structure.py validation/references.py validation/semantics.py runtime/resources.py
runtime/diagnostics.py runtime/boundary.py io/input_file.py graph/projections.py graph/traversal.py
graph/cycles.py graph/witnesses.py analysis/inventory.py analysis/origins.py
analysis/process_comparison.py analysis/contribution_profile.py analysis/evaluator_lineage.py
analysis/human_review.py analysis/presence.py analysis/correction_routes.py
analysis/correction_outcomes.py analysis/context.py analysis/findings.py""".split())
P4_MODULE_PINS = {'__init__.py': '7bea94e138804cbeea4048ef152dcb5726047f1f',
 'analysis/__init__.py': '39f3b82fbbe9c331b5728e9366d08ad5b6750a0c',
 'analysis/context.py': 'da5a5cf361ff1c3178510c88605ad9fefd1d11fd',
 'analysis/contribution_profile.py': '2c1db4526b6aea8119c00d0977d347b02db67e0e',
 'analysis/correction_outcomes.py': '03f4f9995a9b8581508c1793f7bcbd83945f2b1d',
 'analysis/correction_routes.py': '7ea8572717bddc8a8f7546a616f3cff0628fbfe3',
 'analysis/evaluator_lineage.py': '07d9e6cb9ce52baf2d10050150392beefd45f532',
 'analysis/findings.py': 'c218b2476211757c80f6736506269cb2fdba7d11',
 'analysis/human_review.py': 'f4beebf190cff97696a9d718ce8bdb6801a017a6',
 'analysis/inventory.py': '8c163ad8aa48f478ff098451af0485da9002042d',
 'analysis/origins.py': '417e6c3b07447d825a756fc7ac457213b1d3ba48',
 'analysis/presence.py': '7f54a6642279952c7d6f857ff0f4a2417b92d456',
 'analysis/process_comparison.py': '09bd7f47583ee9583cd30501e7f257dbdd21351f',
 'api.py': '0603b4de9888a51190eeeefc6186b47e2afd88bd',
 'cli.py': 'f48f869385fbeb711458f0189ff55194f73fd050',
 'contracts/__init__.py': 'df81f7b32eee0e54a4606b3dd02332407cf53ec1',
 'contracts/bundle.py': 'efa93ccb6f750a38fe6f426fa409aa52651f78bf',
 'contracts/constants.py': 'be7acf3d76d444fef2e124bd343d89005def33d4',
 'contracts/evidence.py': '8ae7eb2185f22b52cc363d3d814aec65148209bb',
 'contracts/execution.py': '53ae5fce613ef90a8b16b1a6daf7108c8e1f0dc9',
 'contracts/report.py': 'a9d6a150299187b2b95e7f05eacadb6124de6e50',
 'contracts/results.py': 'd38094d924bf99b00b5b02c613de2945036104c5',
 'graph/__init__.py': 'd5eff5c90ff209f6f3f6b3d53b1a38d292da413e',
 'graph/cycles.py': 'e58dc6662287e43b8700dee8ad6b2e9d6dbecce4',
 'graph/projections.py': 'f8eb89afbd283830f955afa992d100bf3bfd0ae8',
 'graph/traversal.py': '0ab5b622b11ac102d06ec5a4aa46e945d3da76e9',
 'graph/witnesses.py': '7721cc527a8909584585aa468ea43697feebb2bd',
 'io/__init__.py': '2714a56fb4d2ed55cf66934c8a336f0d5a51944e',
 'io/input_file.py': '05714101f621cffda6108cecb67915488d0541f6',
 'io/output_directory.py': '9e974acb4ae4afe96a2dfb090dfd459effc8f7cb',
 'io/platform_linux.py': '6e7c6196ec22baa91a75ced2aba8de831d03f364',
 'io/platform_windows.py': 'b1023ff2d960f1a7b0374c46b57069957c807e2f',
 'io/publication.py': 'e86a93eedb87b56809977b1c038958c41e70a6a8',
 'reporting/__init__.py': 'f3070404ece65e7eb26d4cfbc1ce11eb7f02d57c',
 'reporting/assemble.py': 'c90193c4aceba2ab971cc960fbf370a775beaa64',
 'reporting/escaping.py': 'a33d2f6e6bc0840f3037f7a6376cabf581251c87',
 'reporting/json_report.py': 'fa7905d6743818af64d7d61b0a5bfcf5be17159a',
 'reporting/markdown_report.py': 'c6c31013559720421645b69c756e7cb137a28c33',
 'runtime/__init__.py': '830e640c62a1ce89f5425a17c9f225332d24a751',
 'runtime/boundary.py': 'cd0b1608ad0c47434588c7764a11eba53a04d4d5',
 'runtime/diagnostics.py': 'd64ba68f2f8bcc4dae3909a8f7d6aacd42289911',
 'runtime/disclosure.py': 'b543c75e314fc21b09799ed32ca913cf03d33157',
 'runtime/resources.py': 'f07108f7094fe153860c635b352f499863507d57',
 'validation/__init__.py': '775fff4175affb1c95a682423fc9c06317321e8e',
 'validation/limits.py': '8b248185dc7cc0e802c191fdc937d23cbc2beea5',
 'validation/references.py': '25040fe157ec1cc939a0e742c7818d493f8992e7',
 'validation/semantics.py': '45604679943dc456323f6ed046362e5982b4714d',
 'validation/structure.py': '24eb56915d8bd561abdf64d4773d486db9fb18e7'}
P4_AUDIT_FILE_BODY = 'def audit_file(\n    input_path: object, output_directory: object, *, options: object = None\n) -> NoReturn:\n    """Refuse immediately; never resolve, read or create a supplied path."""\n    raise NotImplementedError(\n        "Source Integrity Toolkit audit is not implemented in the Phase 1 scaffold."\n    )'
P4_TEST_SCOPES = ("contract", "integration", "scaffold", "security", "unit")
# README is packaging metadata. Coverage/plan/schema/checkers are full-risk.
P4_DOCUMENTATION_PATHS = frozenset((
    "PHASE_4_COMPLETION.md", "phase4/implementation_evidence.json",
))


def current_active(stage):
    require(type(stage) is int and 1 <= stage <= 10, "current_invalid_stage")
    return P4_BASE_ACTIVE | frozenset(p for p, first in P4_ACTIVATION.items() if stage >= first)


def _current_unit(message):
    require(type(message) is str, "current_invalid_commit_footer")
    marks = re.findall(r"^[ \t]*SIT-(?:Verification|Phase)-Unit:[^\n]*$", message, re.M)
    require(len(marks) == 1 and re.fullmatch(r"SIT-Phase-Unit: P4-W(?:0[1-9]|10)", marks[0])
            and message.rstrip().endswith(marks[0]), "current_invalid_commit_footer")
    return marks[0].split(": ")[1]


def _current_oid(value):
    return type(value) is str and re.fullmatch(r"[0-9a-f]{40}", value) is not None


def _current_path(value):
    return (type(value) is str and value and not value.startswith("/")
            and "\\" not in value and ":" not in value
            and all(part not in ("", ".", "..") for part in value.split("/"))
            and all(ord(char) >= 32 and ord(char) != 127 for char in value))


def _current_git(root, *args, input_bytes=None):
    # Root and objects are read afresh. No ambient GIT_DIR/index/config/replace
    # override may redirect this invocation to a different authority source.
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0")
    try:
        return subprocess.check_output(
            ["git", "--no-replace-objects", "-c", "core.fsmonitor=false", *args],
            cwd=root, env=env, input=input_bytes, stderr=subprocess.PIPE, timeout=60)
    except (OSError, subprocess.SubprocessError) as exc:
        raise ValueError("current_git_unavailable_or_incomplete") from exc


def _current_git_state(root):
    root = Path(root).resolve()
    top = _current_git(root, "rev-parse", "--show-toplevel").decode("utf-8").strip()
    require(Path(top).resolve() == root, "current_git_root_mismatch")
    require(_current_git(root, "rev-parse", "--is-shallow-repository") == b"false\n",
            "current_shallow_history")
    require(not _current_git(root, "for-each-ref", "--format=%(refname)", "refs/replace"),
            "current_replaced_history")
    graft = _current_git(root, "rev-parse", "--git-path", "info/grafts").decode("utf-8").strip()
    graft_path = root / graft
    require(not graft_path.exists(), "current_grafted_history")


def _current_objects(root, objects, kind):
    """Read hash-verified raw objects, not pretty-printed mutable metadata.

    The size-framed batch must have exactly the requested records in order.
    Hash verification also rejects well-formed, wrong-parent/tree responses.
    """
    require(type(objects) in (list, tuple) and all(_current_oid(x) for x in objects),
            "current_invalid_object_request")
    require(len(set(objects)) == len(objects), "current_duplicate_object_request")
    if not objects:
        return {}
    raw = _current_git(root, "cat-file", "--batch", input_bytes=("\n".join(objects) + "\n").encode("ascii"))
    require(type(raw) is bytes, "current_malformed_object_batch")
    result, offset = {}, 0
    for oid in objects:
        end = raw.find(b"\n", offset)
        require(end >= offset, "current_incomplete_object_batch")
        fields = raw[offset:end].split(b" ")
        require(len(fields) == 3 and fields[0] == oid.encode("ascii")
                and fields[1] == kind.encode("ascii") and re.fullmatch(rb"0|[1-9][0-9]*", fields[2]),
                "current_malformed_object_record")
        size = int(fields[2])
        require(size <= 8 * 1024 * 1024, "current_oversize_git_object")
        start, offset = end + 1, end + 2 + size
        require(offset <= len(raw) and raw[offset - 1:offset] == b"\n", "current_truncated_object")
        body = raw[start:offset - 1]
        actual = hashlib.sha1(kind.encode("ascii") + b" " + str(size).encode("ascii") + b"\0" + body).hexdigest()
        require(actual == oid, "current_git_object_hash_mismatch")
        result[oid] = body
    require(offset == len(raw), "current_extra_object_records")
    return result


def current_commit_metadata(root, commits):
    objects = _current_objects(root, commits, "commit")
    result = {}
    for oid, body in objects.items():
        header, separator, message = body.partition(b"\n\n")
        require(separator, "current_malformed_commit")
        lines = header.decode("utf-8").splitlines()
        require(lines and lines[0].startswith("tree ") and _current_oid(lines[0][5:]),
                "current_invalid_commit_tree")
        parents, rest = [], lines[1:]
        while rest and rest[0].startswith("parent "):
            parent = rest.pop(0)[7:]
            require(_current_oid(parent) and parent != oid and parent not in parents,
                    "current_invalid_commit_parent")
            parents.append(parent)
        require(not any(line.startswith(("tree ", "parent ")) for line in rest),
                "current_malformed_commit_headers")
        result[oid] = {"tree": lines[0][5:], "parents": parents, "message": message.decode("utf-8")}
    return result


def _current_snapshot(root, commit):
    """Parse hash-verified tree objects, never trust a pretty tree listing."""
    require(_current_oid(commit), "current_invalid_commit")
    root_tree = current_commit_metadata(root, [commit])[commit]["tree"]
    pending, result, directories = [("", root_tree)], {}, set()
    while pending:
        objects = _current_objects(root, sorted({oid for prefix, oid in pending}), "tree")
        following = []
        for prefix, oid in pending:
            require(prefix not in directories, "current_duplicate_tree_path")
            directories.add(prefix)
            raw, offset, names = objects[oid], 0, set()
            require(raw or prefix, "current_empty_or_malformed_tree")
            while offset < len(raw):
                end = raw.find(b"\0", offset)
                require(end >= offset and end + 21 <= len(raw), "current_malformed_tree_entry")
                mode, separator, name_bytes = raw[offset:end].partition(b" ")
                name = name_bytes.decode("utf-8")
                require(separator and _current_path(name) and "/" not in name and name not in names,
                        "current_malformed_tree_path")
                names.add(name)
                child = raw[end + 1:end + 21].hex()
                path = prefix + name
                offset = end + 21
                if mode == b"40000":
                    following.append((path + "/", child))
                else:
                    require(mode in (b"100644", b"100755") and path not in result,
                            "current_non_regular_tree_entry")
                    result[path] = (mode.decode("ascii"), child)
        pending = following
    require(result, "current_empty_or_malformed_tree")
    return result


def current_authority(root):
    """The accepted merge and exact approved plan bound current changes."""
    _current_git_state(root)
    metadata = current_commit_metadata(root, [P4_ACCEPTED_HEAD])[P4_ACCEPTED_HEAD]
    require(metadata["tree"] == P4_ACCEPTED_TREE and metadata["parents"] == list(P4_ACCEPTED_PARENTS),
            "current_accepted_anchor_mismatch")
    baseline = _current_snapshot(root, P4_ACCEPTED_HEAD)
    blobs = _current_objects(root, sorted({row[1] for row in baseline.values()}), "blob")
    return baseline, blobs

def current_context(event_name, event_json, review_head, *, root):
    """Bind the trusted event to the hash-verified actual commit and history."""
    require(_current_oid(review_head), "current_invalid_review_head")
    try:
        event = json.loads(event_json, object_pairs_hook=unique)
        require(event["repository"]["full_name"] == P4_REPOSITORY, "current_wrong_repository")
        metadata = current_commit_metadata(root, [review_head])[review_head]
        unit = _current_unit(metadata["message"])
        if event_name == "pull_request":
            pr = event["pull_request"]
            require(pr["head"]["sha"] == review_head, "current_event_head_mismatch")
            require(pr["head"]["ref"] == P4_BRANCH and pr["head"]["repo"]["full_name"] == P4_REPOSITORY,
                    "current_unapproved_branch")
            require(pr["base"]["ref"] == "main" and pr["base"]["repo"]["full_name"] == P4_REPOSITORY,
                    "current_wrong_base_ref")
            base = pr["base"]["sha"]
        else:
            require(event_name == "push" and event["ref"] == "refs/heads/main", "current_unsupported_event")
            require(event["after"] == review_head and event["head_commit"]["id"] == review_head
                    and event.get("deleted", False) is False and event.get("forced", False) is False,
                    "current_event_head_mismatch")
            require(event["head_commit"]["message"].rstrip("\n") == metadata["message"].rstrip("\n"),
                    "current_event_commit_mismatch")
            base = event["before"]
            if len(metadata["parents"]) > 1:
                require(len(metadata["parents"]) == 2, "current_invalid_main_merge")
                candidate = current_commit_metadata(root, [metadata["parents"][1]])[metadata["parents"][1]]
                require(metadata["tree"] == candidate["tree"], "current_merge_candidate_tree_mismatch")
        require(_current_oid(base) and base != "0" * 40 and base != review_head, "current_invalid_base")
        history = current_history(root, base, review_head)
        return {"unit": unit, "activation_stage": history[-1]["activation_stage"],
                "base": base, "head": review_head, "event": event_name}
    except (KeyError, TypeError, AttributeError, json.JSONDecodeError) as exc:
        raise ValueError("current_malformed_event") from exc

def _current_audit_file_unchanged(source):
    tree = ast.parse(source)
    definitions = [node for node in ast.walk(tree)
                   if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
                   and node.name == "audit_file"]
    if len(definitions) != 1 or definitions[0] not in tree.body or definitions[0].decorator_list:
        return False
    if ast.get_source_segment(source, definitions[0]) != P4_AUDIT_FILE_BODY:
        return False
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id == "audit_file" and isinstance(node.ctx, (ast.Store, ast.Del)):
            return False
        if isinstance(node, ast.alias) and (node.asname == "audit_file" or
                (node.asname is None and node.name.split(".")[0] in ("audit_file", "*"))):
            return False
        if isinstance(node, (ast.ExceptHandler, ast.MatchAs, ast.MatchStar)) and node.name == "audit_file":
            return False
        if isinstance(node, ast.MatchMapping) and node.rest == "audit_file":
            return False
    return True


def _current_retained_parts(path, raw, stage):
    """Keep semantic witnesses outside the exact mixed-file context migration.

    These are current accepted-byte comparisons, not old test execution or an
    inverse patch chain. At W08 the approved public receipt behavior is replaced
    atomically and directly tested by the current suite.
    """
    source = raw.decode("utf-8")
    tree = ast.parse(source)
    if path == "tests/security/test_preparation_inertness.py":
        parts = []
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and node.name == "test_whole_package_guard_rejects_forbidden_implementation_in_temporary_copy":
                continue
            first = min([node.lineno] + [n.lineno for n in getattr(node, "decorator_list", ())])
            parts.append("\n".join(source.splitlines()[first - 1:node.end_lineno]))
        return parts
    if stage >= 8:
        return None
    # Only receipt context statements differ in W01. Preserve the complete
    # child program strings, assertion bodies, fixtures and installed witnesses.
    class ReceiptContext(ast.NodeTransformer):
        def visit_Assign(self, node):
            names = [target.id for target in node.targets if isinstance(target, ast.Name)]
            permitted = ("state = guard.current_local_state(ROOT)",
                         "guard = _load('sit_current_installed_context', 'tools/check_scaffold_boundary.py')")
            if any(ast.dump(node, include_attributes=False) == ast.dump(ast.parse(text).body[0], include_attributes=False)
                   for text in permitted):
                return None
            if names == ["record"] and isinstance(node.value, ast.Dict):
                pairs = [(key, value) for key, value in zip(node.value.keys, node.value.values)
                         if key is not None and not (isinstance(key, ast.Constant) and key.value in ("head", "unit"))]
                node.value.keys = [key for key, value in pairs]
                node.value.values = [value for key, value in pairs]
            return self.generic_visit(node)
    return ast.dump(ReceiptContext().visit(tree), include_attributes=False)


def current_scope(baseline, actual, read_blob, stage=1):
    """Cumulative path/byte ceiling; per-commit ownership is checked separately."""
    current_active(stage)
    allowed = frozenset().union(*(P4_UNIT_PATHS[n] for n in range(1, stage + 1)))
    require(all(_current_path(p) for p in actual), "current_path_alias")
    require(set(actual) - set(baseline) <= P4_PATHS, "current_unlisted_path")
    require(not set(baseline) - set(actual), "current_forbidden_deletion")
    require(P4_PLAN in actual, "current_approved_plan_missing")
    for path, row in actual.items():
        require(row[0] == (baseline[path][0] if path in baseline else "100644"), "current_file_mode_changed")
        if row != baseline.get(path):
            relative = path.removeprefix("src/" + PACKAGE + "/")
            if relative in P4_ACTIVATION:
                require(stage >= P4_ACTIVATION[relative], "current_premature_activation")
            require(path in allowed, "current_frozen_file_changed" if path in baseline else "current_unit_path_not_allowed")
    workflow = ".github/workflows/phase1-ci.yml"
    if actual[workflow] != baseline[workflow]:
        current_workflow(json.loads(read_blob(actual[workflow][1]), object_pairs_hook=unique))
    api = "src/" + PACKAGE + "/api.py"
    if actual[api] != baseline[api]:
        source = read_blob(actual[api][1]).decode("utf-8")
        require(_current_audit_file_unchanged(source), "current_audit_file_changed")
    # Allowed paths do not permit intermediate forbidden effects that are later
    # restored. Inspect changed active source without requiring future features
    # to have been implemented in history-only synthetic permission fixtures.
    for relative, first in P4_ACTIVATION.items():
        path = "src/" + PACKAGE + "/" + relative
        if actual[path] != baseline[path]:
            raw = read_blob(actual[path][1])
            require(len(raw) <= 262144 and not current_live_issues(relative, raw.decode("utf-8"), stage),
                    "current_product_boundary_failed")
    for path in ("tests/security/test_preparation_inertness.py", "tests/contract/test_phase2_transition.py",
                 "tests/integration/test_analytical_installed_runtime.py"):
        if actual[path] != baseline[path]:
            require(_current_retained_parts(path, read_blob(baseline[path][1]), stage) ==
                    _current_retained_parts(path, read_blob(actual[path][1]), stage), "current_mixed_semantics_changed")
    require(hashlib.sha256(read_blob(actual[P4_PLAN][1])).hexdigest() == P4_PLAN_SHA256,
            "current_approved_plan_changed")

def current_history(root, base, head, authority=None):
    """Validate each original commit and every parent edge after acceptance.

    Owner unit determines new bytes. Activation is the maximum verified ancestor
    progress and never decreases on repairs. Inherited merge bytes retain their
    original validated ownership; a novel resolution needs this commit's scope.
    This is history permission evidence, not proof of completed product behavior.
    """
    require(_current_oid(base) and _current_oid(head), "current_invalid_history_range")
    baseline, known_blobs = current_authority(root) if authority is None else authority
    _current_git(root, "merge-base", "--is-ancestor", P4_ACCEPTED_HEAD, base)
    _current_git(root, "merge-base", "--is-ancestor", base, head)
    raw = _current_git(root, "rev-list", "--reverse", "--topo-order", P4_ACCEPTED_HEAD + ".." + head)
    commits = raw.decode("ascii").splitlines()
    require(bool(commits) and all(_current_oid(c) for c in commits) and len(set(commits)) == len(commits),
            "current_empty_or_malformed_history")
    metadata = current_commit_metadata(root, commits)
    snapshots, stages, rows = {P4_ACCEPTED_HEAD: baseline}, {P4_ACCEPTED_HEAD: 0}, []
    def read_blob(oid):
        if oid not in known_blobs:
            known_blobs.update(_current_objects(root, [oid], "blob"))
        return known_blobs[oid]
    for commit in commits:
        meta = metadata[commit]
        parents = meta["parents"]
        require(parents and all(p in stages for p in parents), "current_unanchored_parent")
        unit = _current_unit(meta["message"])
        owner = int(unit[-2:])
        previous = max(stages[p] for p in parents)
        require(owner <= previous + 1, "current_unit_out_of_order")
        stage = max(previous, owner)
        actual = _current_snapshot(root, commit)
        missing = sorted({row[1] for row in actual.values()} - set(known_blobs))
        known_blobs.update(_current_objects(root, missing, "blob"))
        current_scope(baseline, actual, read_blob, stage)
        edges = []
        for parent in parents:
            before = snapshots[parent]
            require(not set(before) - set(actual), "current_forbidden_deletion")
            changed = sorted(p for p in set(before) | set(actual) if before.get(p) != actual.get(p))
            inherited = []
            for path in changed:
                if any(actual.get(path) == snapshots[other].get(path) for other in parents if other != parent):
                    inherited.append(path)
                else:
                    require(path in P4_UNIT_PATHS[owner], "current_unit_path_not_allowed")
            edges.append({"parent": parent, "changed_paths": changed, "inherited_paths": inherited})
        snapshots[commit], stages[commit] = actual, stage
        rows.append({"commit": commit, **meta, "unit": unit, "owner_unit": unit, "activation_stage": stage,
                     "parent_changes": edges,
                     "changed_from_anchor": sorted(p for p in set(actual) | set(baseline)
                                                   if actual.get(p) != baseline.get(p))})
    require(head in stages and base in stages, "current_missing_range_endpoint")
    return rows

def current_risk(root, base, head, authority=None):
    """Classify the complete reviewed range after validating its authority.

    A final tree diff cannot reveal restored changes or everything introduced
    by a merge. Derive the range from the verified parent graph, then compare
    each included commit with every parent. The result records both that union
    and the net endpoint diff; caller-declared scope never selects a profile.
    """
    require(_current_oid(base) and _current_oid(head), "current_invalid_history_range")
    authority = current_authority(root) if authority is None else authority
    if base == head == P4_ACCEPTED_HEAD:
        rows = []
    else:
        rows = current_history(root, base, head, authority)
    metadata = {row["commit"]: row for row in rows}

    def ancestors(commit):
        found, pending = set(), [commit]
        while pending:
            item = pending.pop()
            if item in found:
                continue
            found.add(item)
            if item == P4_ACCEPTED_HEAD:
                continue
            require(item in metadata, "current_incomplete_risk_history")
            pending.extend(metadata[item]["parents"])
        return found

    head_ancestors, base_ancestors = ancestors(head), ancestors(base)
    require(base in head_ancestors, "current_risk_base_not_ancestor")
    included = head_ancestors - base_ancestors
    snapshots = {P4_ACCEPTED_HEAD: authority[0]}

    def snapshot(commit):
        if commit not in snapshots:
            snapshots[commit] = _current_snapshot(root, commit)
        return snapshots[commit]

    def changed(left, right):
        return sorted(path for path in set(left) | set(right)
                      if left.get(path) != right.get(path))

    net = changed(snapshot(base), snapshot(head))
    all_paths, changes = set(), []
    for row in rows:
        if row["commit"] not in included:
            continue
        actual, parents = snapshot(row["commit"]), []
        for parent in row["parents"]:
            paths = changed(snapshot(parent), actual)
            all_paths.update(paths)
            parents.append({"parent": parent, "changed_paths": paths})
        changes.append({"commit": row["commit"], "tree": row["tree"], "parents": parents})
    require(set(net) <= all_paths, "current_incomplete_risk_changes")
    if all_paths - P4_DOCUMENTATION_PATHS:
        profile, reason = "full", "non_documentation_paths"
    elif not all_paths or not net:
        profile, reason = "full", "empty_change_set"
    elif not rows or rows[-1]["activation_stage"] < 10:
        profile, reason = "full", "early_stage_requires_full"
    else:
        profile, reason = "documentation", "documentation_paths_only"
    return {"profile": profile, "reason": reason, "base": base, "head": head,
            "changed_paths": sorted(all_paths), "net_changed_paths": net,
            "commit_changes": changes}


def current_checkout(root, head, authority=None, *, require_clean=True, stage=None):
    """Read index and worktree separately; do not trust assume-unchanged flags."""
    baseline, blobs = current_authority(root) if authority is None else authority
    require(_current_git(root, "rev-parse", "HEAD").decode("ascii").strip() == head,
            "current_checkout_head_mismatch")
    history = current_history(root, P4_ACCEPTED_HEAD, head, (baseline, blobs))
    verified_stage = history[-1]["activation_stage"]
    require(stage is None or (type(stage) is int and stage == verified_stage), "current_stage_mismatch")
    stage = verified_stage
    owner = int(history[-1]["unit"][-2:])
    committed = _current_snapshot(root, head)
    index = {}
    for row in _current_git(root, "ls-files", "--stage", "-z").split(b"\0"):
        if not row:
            continue
        info, tab, name = row.partition(b"\t")
        fields, path = info.decode("ascii").split(" "), name.decode("utf-8")
        require(tab and len(fields) == 3 and fields[2] == "0" and _current_path(path)
                and path not in index and _current_oid(fields[1]), "current_unmerged_or_malformed_index")
        index[path] = (fields[0], fields[1])
    missing = sorted({row[1] for row in index.values()} - set(blobs))
    blobs.update(_current_objects(root, missing, "blob"))
    def read_blob(oid):
        if oid not in blobs:
            blobs.update(_current_objects(root, [oid], "blob"))
        return blobs[oid]
    current_scope(baseline, index, read_blob, stage)
    unknown = _current_git(root, "ls-files", "--others", "--exclude-standard", "-z")
    paths = set(index) | {p.decode("utf-8") for p in unknown.split(b"\0") if p}
    actual, work_blobs = {}, dict(blobs)
    for path in sorted(paths):
        require(_current_path(path), "current_path_alias")
        target = Path(root) / path
        require(not any(p.is_symlink() for p in [target, *target.parents] if p != Path(root).parent),
                "current_linked_checkout_path")
        if not target.exists():
            continue
        info = target.stat()
        require(stat.S_ISREG(info.st_mode), "current_non_regular_checkout_path")
        require(info.st_size <= 8 * 1024 * 1024, "current_oversize_checkout_file")
        data = target.read_bytes()
        oid = git_blob(data)
        mode = ("100755" if info.st_mode & 0o111 else "100644") if os.name != "nt" else index.get(path, ("100644",))[0]
        actual[path], work_blobs[oid] = (mode, oid), data
    current_scope(baseline, actual, work_blobs.__getitem__, stage)
    if not require_clean:
        for snapshot in (index, actual):
            require(all(path in P4_UNIT_PATHS[owner] for path in set(snapshot) | set(committed)
                        if snapshot.get(path) != committed.get(path)), "current_unit_path_not_allowed")
    if require_clean:
        require(index == committed and actual == committed, "current_dirty_checkout")
    return {"tracked_files": len(index), "worktree_files": len(actual),
            "clean": index == committed == actual, "frozen_files": len(set(baseline) - P4_PATHS)}


def current_live_issues(path, source, stage=1):
    active = current_active(stage)
    if path not in active:
        return ["unapproved_live_module"]
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError, RecursionError):
        return ["invalid_python"]
    targets, import_issues = phase3_import_targets(path, tree)
    return sorted(set(_dependency_target_issues(path, targets, import_issues, active, stage=stage)
                      + _source_tree_effect_issues(path, tree)))

def current_layer_issues(path, source, stage=1):
    active = current_active(stage)
    return (_dependency_issues(path, source, active, stage=stage) if path in active
            else _phase2_layer_issues(path, source))

def current_module_issues(sources, stage=1):
    """All 48 baseline bodies stay pinned until their explicit activation stage."""
    active = current_active(stage)
    # Trees and targets exist only within this call. Every source is read and
    # parsed anew on the next invocation; no authorization verdict is cached.
    issues, decoded, targets_by_path = [], {}, {}
    invalid_cycle_source = False
    for path in sorted(set(sources) | set(EXPECTED_PATHS)):
        if path not in EXPECTED_PATHS:
            issues.append((path, "unexpected_module")); continue
        if path not in sources:
            issues.append((path, "missing_module")); continue
        raw = sources[path]
        if len(raw) > (262144 if path in active else 16384):
            issues.append((path, "oversize_module")); continue
        if (path not in P4_ACTIVATION or stage < P4_ACTIVATION[path]) and git_blob(raw) != P4_MODULE_PINS[path]:
            issues.append((path, "accepted_blob_changed"))
        try:
            source = raw.decode("utf-8")
        except UnicodeDecodeError:
            issues.append((path, "invalid_utf8")); continue
        decoded[path] = source
        try:
            tree = ast.parse(source)
        except (SyntaxError, ValueError, RecursionError):
            invalid_cycle_source = True
            codes = ["invalid_python"]
        else:
            targets, import_issues = phase3_import_targets(path, tree)
            targets_by_path[path] = targets
            if path in active:
                codes = (_dependency_target_issues(path, targets, import_issues, active, stage=stage)
                         + _source_tree_effect_issues(path, tree))
            else:
                # Scaffold comparison removes docstrings from its own parse;
                # never let it mutate the tree used for dependency inspection.
                codes = _phase2_layer_issues(path, source) + form_issues(path, source)
        issues.extend((path, code) for code in codes)
    if stage >= 8 and "__init__.py" in decoded:
        try:
            tree = ast.parse(decoded["__init__.py"])
            exports = [ast.literal_eval(node.value) for node in tree.body if isinstance(node, ast.Assign)
                       and any(isinstance(target, ast.Name) and target.id == "__all__" for target in node.targets)]
            if exports != [("audit_bundle", "audit_file", "__version__", "AuditReport", "AuditAbort", "AuditCancelled", "AuditUsageError")]:
                issues.append(("__init__.py", "current_public_exports_mismatch"))
        except (SyntaxError, ValueError, TypeError):
            issues.append(("__init__.py", "current_public_exports_mismatch"))
    if stage >= 8 and "api.py" in decoded:
        try:
            if not _current_audit_file_unchanged(decoded["api.py"]):
                issues.append(("api.py", "accepted_audit_file_changed"))
        except (SyntaxError, ValueError):
            issues.append(("api.py", "invalid_python"))
    cycle_issues = (["invalid_python"] if invalid_cycle_source
                    else _import_target_cycle_issues(targets_by_path))
    issues.extend(("src/" + PACKAGE, code) for code in cycle_issues)
    return sorted(set(issues))


def _current_module_sources(root, stage=1):
    """Inspect the actual source tree, including ignored files and links."""
    active = current_active(stage)
    source_root, package = Path(root) / "src", Path(root) / "src" / PACKAGE
    require(not source_root.is_symlink() and not package.is_symlink() and package.is_dir(),
            "current_missing_or_linked_package")
    directories = {p.split("/")[0] for p in EXPECTED_PATHS if "/" in p}
    sources = {}
    for directory, dirs, files in os.walk(package, followlinks=False):
        current = Path(directory)
        for name in list(dirs):
            child = current / name
            require(not child.is_symlink(), "current_linked_source_directory")
            if name == "__pycache__":
                require(all(p.is_file() and not p.is_symlink() and p.suffix == ".pyc" for p in child.iterdir()),
                        "current_unexpected_cache_entry")
                dirs.remove(name)
            else:
                require(child.relative_to(package).as_posix() in directories, "current_unexpected_source_directory")
        for name in files:
            path = current / name
            relative = path.relative_to(package).as_posix()
            require(not path.is_symlink() and path.is_file(), "current_non_regular_source_file")
            require(relative in EXPECTED_PATHS, "current_unexpected_source_file")
            with path.open("rb") as stream:
                sources[relative] = stream.read((262144 if relative in active else 16384) + 1)
    for child in source_root.iterdir():
        require(child.name == PACKAGE or (child.name == "source_integrity_toolkit.egg-info"
                and child.is_dir() and not child.is_symlink()), "current_unexpected_source_entry")
    return sources


def current_modules(root, stage=1):
    sources = _current_module_sources(root, stage)
    require(not current_module_issues(sources, stage), "current_module_boundary_failed")
    return len(sources)

def current_check_repository(root, stage=1):
    """Package inspection only; explicit stage never grants checkout authority."""
    try:
        active = current_active(stage)
        sources = _current_module_sources(root, stage)
        issues = [{"path": path, "code": code} for path, code in current_module_issues(sources, stage)]
    except (ValueError, OSError) as exc:
        return {"ok": False, "checked_modules": 0,
                "issues": [{"path": "src/" + PACKAGE, "code": str(exc)}]}
    return {"ok": not issues, "checked_modules": len(sources), "issues": issues,
            "activation_stage": stage, "promoted_modules": sorted(active),
            "protected_modules": len(EXPECTED_PATHS - active),
            "entry_byte_protected_modules": sum(p not in P4_ACTIVATION or stage < P4_ACTIVATION[p]
                                                  for p in EXPECTED_PATHS),
            "scope": "current package inspection only; no checkout authorization or analytical conformance claim"}

def current_collection(nodes, expected_files):
    require(type(nodes) in (list, tuple) and nodes and all(type(n) is str for n in nodes),
            "current_empty_or_invalid_collection")
    require(len(set(nodes)) == len(nodes), "current_duplicate_collection")
    require(all("::" in n and _current_path(n.split("::", 1)[0]) and
                re.fullmatch(r"tests/(?:contract|integration|scaffold|security|unit)/.+\.py", n.split("::", 1)[0])
                for n in nodes), "current_invalid_test_identity")
    require({n.split("::", 1)[0] for n in nodes} == set(expected_files), "current_test_file_omitted")


def current_junit(xml_bytes, nodes, successful_subtests):
    """Exact top-level identities; separately reconcile observed subtest events."""
    current_collection(nodes, {n.split("::", 1)[0] for n in nodes})
    expected = []
    for node in nodes:
        # Parameter text can itself contain '::'; only split the structural part.
        stem, bracket, parameter = node.partition("[")
        parts = stem.split("::")
        expected.append((".".join([parts[0][:-3].replace("/", "."), *parts[1:-1]]),
                         parts[-1] + bracket + parameter))
    require(len(set(expected)) == len(expected), "current_ambiguous_junit_identity")
    try:
        root = ET.fromstring(xml_bytes)
        require(root.tag == "testsuites" and len(root) > 0 and all(s.tag == "testsuite" for s in root),
                "current_invalid_junit_root")
        totals = {k: sum(int(s.attrib[k]) for s in root) for k in ("tests", "failures", "errors", "skipped")}
        require(all(re.fullmatch(r"0|[1-9][0-9]*", s.attrib[k]) for s in root for k in totals),
                "current_invalid_junit_count")
        cases = list(root.iter("testcase"))
        actual = [(case.get("classname"), case.get("name")) for case in cases]
        require(len(actual) == len(expected) and len(set(actual)) == len(actual) and set(actual) == set(expected),
                "current_junit_identity_mismatch")
        observed = {k: sum(len(list(root.iter(tag))) for tag in tags) for k, tags in (
            ("failures", ("failure",)), ("errors", ("error",)), ("skipped", ("skipped",)))}
        require(type(successful_subtests) is int and successful_subtests >= 0 and
                totals["tests"] == len(nodes) + successful_subtests, "current_subtest_count_mismatch")
        require(all(totals[k] == 0 and observed[k] == 0 for k in observed), "current_unsuccessful_test_evidence")
        return {"tests": len(nodes), "subtest_events": successful_subtests, "identities_match": True}
    except (ET.ParseError, KeyError, TypeError) as exc:
        raise ValueError("current_malformed_junit") from exc


def current_workflow(value):
    """Direct current CI security policy; no reverse Phase 1 transformation.

    Labels are descriptive. Security-bearing keys, stages and arguments are
    closed. The current driver resolves and records its risk profile itself.
    """
    try:
        require(set(value) == {"name", "on", "permissions", "concurrency", "jobs"}, "current_workflow_keys")
        require(value["on"] == {"pull_request": {"branches": ["main"],
            "types": ["opened", "synchronize", "reopened", "ready_for_review"]},
            "push": {"branches": ["main"]}}, "current_workflow_triggers")
        require(value["permissions"] == {"contents": "read"}, "current_workflow_permissions")
        require(value["concurrency"] == {"group": "phase3-${{ github.event.pull_request.number || github.ref }}",
                                        "cancel-in-progress": True}, "current_workflow_concurrency")
        require(set(value["jobs"]) == {"scaffold"}, "current_workflow_jobs")
        job = value["jobs"]["scaffold"]
        require(set(job) == {"name", "runs-on", "timeout-minutes", "strategy", "env", "defaults", "steps"},
                "current_workflow_job_keys")
        require(job["runs-on"] == "${{ matrix.os }}" and type(job["timeout-minutes"]) is int
                and job["timeout-minutes"] == 50, "current_workflow_budget")
        require(job["strategy"] == {"fail-fast": False, "matrix": {
            "os": ["ubuntu-24.04", "windows-2025"], "python": ["3.11", "3.13"]}}, "current_workflow_matrix")
        require(job["defaults"] == {"run": {"shell": "bash"}}, "current_workflow_shell")
        head = "${{ github.event.pull_request.head.sha || github.sha }}"
        require(job["env"] == {"PYTHONDONTWRITEBYTECODE": "1", "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1",
            "PIP_DISABLE_PIP_VERSION_CHECK": "1", "PIP_NO_INPUT": "1", "PYTHONUTF8": "1",
            "SIT_REVIEW_HEAD": head, "SIT_MATRIX_OS": "${{ matrix.os }}",
            "SIT_MATRIX_PYTHON": "${{ matrix.python }}"}, "current_workflow_environment")
        steps = job["steps"]
        require(type(steps) is list and len(steps) == 7, "current_workflow_steps")
        for step in steps:
            require(type(step.get("name")) is str and step["name"], "current_workflow_step_name")
        actual = [{k: v for k, v in s.items() if k != "name"} for s in steps]
        require(actual[0] == {"uses": "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1",
            "with": {"ref": head, "fetch-depth": 0, "persist-credentials": False, "submodules": False, "lfs": False}},
            "current_workflow_checkout")
        require(actual[1] == {"uses": "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97",
            "with": {"python-version": "${{ matrix.python }}", "architecture": "x64", "check-latest": False,
                     "allow-prereleases": False}}, "current_workflow_python")
        driver = "python -B tests/scaffold/test_ci_contract.py --ci-stage "
        for i, stage in enumerate(("preflight", "prepare", "test"), 2):
            require(actual[i] == {"run": driver + stage}, "current_workflow_stage")
        require(actual[5] == {"if": "${{ always() }}", "run": driver + "evidence"}, "current_workflow_evidence")
        require(actual[6] == {"if": "${{ always() }}",
            "uses": "actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a",
            "with": {"name": "phase3-${{ matrix.os }}-py${{ matrix.python }}-${{ github.run_id }}-${{ github.run_attempt }}",
                "path": "${{ runner.temp }}/sit-p3/evidence/*.json\n${{ runner.temp }}/sit-p3/evidence/*.xml\n${{ runner.temp }}/sit-p3/evidence/*.log",
                "if-no-files-found": "error", "include-hidden-files": False, "overwrite": False, "retention-days": 14}},
            "current_workflow_upload")
    except (KeyError, TypeError, AttributeError) as exc:
        raise ValueError("current_malformed_workflow") from exc


def current_local_state(root):
    """Read actual local commit provenance, allowing only its owned worktree edits."""
    head = _current_git(root, "rev-parse", "HEAD").decode("ascii").strip()
    authority = current_authority(root)
    rows = current_history(root, P4_ACCEPTED_HEAD, head, authority)
    checkout = current_checkout(root, head, authority, require_clean=False, stage=rows[-1]["activation_stage"])
    return {"clean": checkout["clean"], "unit": rows[-1]["unit"], "activation_stage": rows[-1]["activation_stage"],
            "head": head, "base": P4_ACCEPTED_HEAD}


def current_verify(root, event_name, event_json, review_head):
    """Explicit current entrypoint; no source records or environment grant scope."""
    context = current_context(event_name, event_json, review_head, root=root)
    authority = current_authority(root)
    history = current_history(root, context["base"], review_head, authority)
    stage = context["activation_stage"]
    checkout = current_checkout(root, review_head, authority, stage=stage)
    modules = current_modules(root, stage)
    current_workflow(json.loads((Path(root) / ".github/workflows/phase1-ci.yml").read_bytes(), object_pairs_hook=unique))
    return {"ok": True, **context, **checkout, "checked_modules": modules, "history": history}

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--unit", choices=["P4-W%02d" % n for n in range(1, 11)])
    parser.add_argument("--stage", type=int, choices=range(1, 11))
    parser.add_argument("--event-name", choices=("pull_request", "push"))
    parser.add_argument("--event-file", type=Path)
    parser.add_argument("--head")
    parser.add_argument("--modules-only", action="store_true",
                        help="Inspect explicit-stage package bytes/effects without checkout authorization")
    args = parser.parse_args(argv)
    try:
        if args.modules_only:
            require(not any((args.event_name, args.event_file, args.head)), "current_external_context_required")
            stage = args.stage if args.stage is not None else int(args.unit[-2:]) if args.unit else 1
            require(args.unit is None or int(args.unit[-2:]) == stage, "current_stage_mismatch")
            result = current_check_repository(args.root, stage)
        else:
            require(args.stage is None and args.event_name and args.event_file and args.head,
                    "current_external_context_required")
            result = current_verify(args.root, args.event_name, args.event_file.read_bytes(), args.head)
            require(args.unit is None or args.unit == result["unit"], "current_unit_mismatch")
    except (ValueError, OSError, UnicodeError, SyntaxError) as exc:
        result = {"ok": False, "issues": [{"code": str(exc)}]}
    print(json.dumps(result, sort_keys=True))
    return 0 if result["ok"] else 1

if __name__ == "__main__":
    raise SystemExit(main())
