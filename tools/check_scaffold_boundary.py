# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Developer-only Phase 2 and Phase 3 boundary checks; never imported by the product.

The accepted plan, entry manifest, fixed module inventory, external work-unit
context, static checks and behavioral tests are separate controls. A candidate
policy cannot authorize its own stage or additional module. This checker is not
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
PLAN_SHA256 = "bea21992edf58b77cfe0f9a128bb31cee9226a9ea5e87b829663a47768227918"
ENTRY_SHA256 = "bdec51c6499e080385140446eece9014144cf277c1651b05734f5166a831623f"
INTAKE = "eb730dda31d189c8487b5247a45bae47b678821b"
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
FIRST_UNIT = {
    "contracts/bundle.py": 2, "contracts/evidence.py": 2,
    "contracts/constants.py": 2, "contracts/execution.py": 2,
    "contracts/report.py": 2, "validation/limits.py": 3,
    "runtime/resources.py": 3, "runtime/diagnostics.py": 3,
    "io/input_file.py": 4, "runtime/boundary.py": 4,
    "validation/structure.py": 4, "validation/references.py": 5,
    "validation/semantics.py": 5,
}
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


def unit_number(unit=None):
    value = os.environ.get("SIT_PHASE_UNIT", "P2-W01") if unit is None else unit
    require(isinstance(value, str) and re.fullmatch(r"P2-W0[1-9]", value), "invalid_trusted_unit")
    return int(value[-1])


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def plan_paths(root):
    raw = (root / "PHASE_2_PLAN.md").read_bytes()
    require(hashlib.sha256(raw).hexdigest() == PLAN_SHA256, "approved_plan_changed")
    found = re.findall(r"^## \d+\. (P2-W0[1-9]):[^\n]*\n\n### Allowed paths\n\n```text\n(.*?)\n```",
                       raw.decode("utf-8"), re.M | re.S)
    require([u for u, _ in found] == [f"P2-W{i:02}" for i in range(1, 10)], "unit_path_table")
    return {u: frozenset(body.splitlines()) for u, body in found}


def entry_manifest(root):
    raw = (root / "phase2/entry_manifest.json").read_bytes()
    require(hashlib.sha256(raw).hexdigest() == ENTRY_SHA256, "entry_manifest_changed")
    entry = json.loads(raw, object_pairs_hook=unique)
    require(entry["intake_commit"] == INTAKE and entry["file_count"] == 125, "entry_identity")
    reference = entry["included_manifest"]
    require(reference["path"] == "scaffold/delivery_manifest.json" and reference["members"] == 121, "parent_manifest_identity")
    parent_raw = (root / reference["path"]).read_bytes()
    require(hashlib.sha256(parent_raw).hexdigest() == reference["sha256"], "parent_manifest_changed")
    parent = json.loads(parent_raw, object_pairs_hook=unique)
    require(len(parent["files"]) == 121 and len(entry["additional_files"]) == 4, "composed_entry_count")
    require(not set(parent["files"]) & set(entry["additional_files"]), "overlapping_entry_paths")
    entry["files"] = {**parent["files"], **entry["additional_files"]}
    return entry


def policy_promotions(value, unit=None):
    current = unit_number(unit)
    require(set(value) == {"format", "plan_sha256", "active_unit", "first_units", "promotions"}, "policy_keys")
    require(value["format"] == "sit-phase2-modules/0.1" and value["plan_sha256"] == PLAN_SHA256, "policy_identity")
    require(value["active_unit"] == f"P2-W{current:02}", "policy_cannot_select_unit")
    require(value["first_units"] == FIRST_UNIT, "policy_cannot_expand_modules")
    rows = value["promotions"]
    require(isinstance(rows, list), "promotion_type")
    promoted = set()
    for row in rows:
        require(set(row) == {"path", "unit"}, "promotion_keys")
        path, step = row["path"], row["unit"]
        require(path in FIRST_UNIT and path not in promoted, "unknown_or_duplicate_promotion")
        require(type(step) is int and FIRST_UNIT[path] == step <= current, "premature_promotion")
        promoted.add(path)
    return frozenset(promoted)


def _phase2_promotions(root, unit=None):
    unit_number(unit)
    p = root / "phase2/module_policy.json"
    if not (root / "PHASE_2_PLAN.md").exists():
        # Explicit package-only historical test workspace: no live promotion.
        require(not p.exists(), "policy_without_approved_plan")
        return frozenset()
    plan_paths(root)
    entry_manifest(root)
    return policy_promotions(json.loads(p.read_bytes(), object_pairs_hook=unique), unit)


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


def _phase2_live_issues(path, source):
    if path not in FIRST_UNIT:
        return ["unapproved_live_module"]
    issues = _phase2_layer_issues(path, source, live=True)
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError, RecursionError):
        return ["invalid_python"]
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in FORBIDDEN_NAMES:
            issues.append("forbidden_effect")
        if isinstance(node, ast.Attribute) and (node.attr in FORBIDDEN_ATTRS or node.attr.startswith("__")):
            issues.append("forbidden_effect")
        if isinstance(node, (ast.AsyncFunctionDef, ast.Await)):
            issues.append("async_execution_not_selected")
        if isinstance(node, ast.ClassDef) and node.keywords:
            issues.append("custom_metaclass")
        if isinstance(node, ast.Constant) and isinstance(node.value, str) and any(s in node.value for s in ("tests/golden/", "scaffold/", "phase2/", "module_manifest.json", "trace_catalog.json", "obligation_catalog.json")):
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


def import_cycle_issues(sources):
    by_name = {module_name(p): p for p in sources}
    dependencies = {}
    for path, source in sources.items():
        try:
            targets, _ = import_targets(path, ast.parse(source))
        except (SyntaxError, ValueError, RecursionError):
            return ["invalid_python"]
        dependencies[path] = {by_name[t] for t in targets if t in by_name}
    try:
        tuple(TopologicalSorter(dependencies).static_order())
    except CycleError:
        return ["import_cycle"]
    return []


def _check_phase2_repository(root, *, unit=None):
    issues, found, sources = [], set(), {}
    try:
        promoted = _phase2_promotions(root, unit)
    except (ValueError, OSError, KeyError, TypeError):
        return {"ok": False, "checked_modules": 0, "issues": [{"path": "phase2", "code": "invalid_phase_policy"}]}
    package = root / "src" / PACKAGE
    if (root / "src").is_symlink() or package.is_symlink() or not package.is_dir():
        return {"ok": False, "checked_modules": 0, "issues": [{"path": "src/" + PACKAGE, "code": "missing_or_linked_package"}]}
    expected_dirs = {p.split("/")[0] for p in EXPECTED_PATHS if "/" in p}
    for directory, dirs, files in os.walk(package, followlinks=False):
        current = Path(directory)
        for name in list(dirs):
            child = current / name
            key = child.relative_to(package).as_posix()
            if child.is_symlink():
                issues.append({"path": key, "code": "linked_directory"}); dirs.remove(name)
            elif name == "__pycache__":
                if any(c.is_symlink() or not c.is_file() or c.suffix != ".pyc" for c in child.iterdir()):
                    issues.append({"path": key, "code": "unexpected_cache_entry"})
                dirs.remove(name)
            elif key not in expected_dirs:
                issues.append({"path": key, "code": "unexpected_directory"}); dirs.remove(name)
        for name in files:
            path = current / name
            key = path.relative_to(package).as_posix(); found.add(key)
            if path.is_symlink() or not path.is_file():
                issues.append({"path": key, "code": "not_regular_module"}); continue
            if key not in EXPECTED_PATHS:
                issues.append({"path": key, "code": "unexpected_package_file"}); continue
            limit = 262144 if key in promoted else 16384
            with path.open("rb") as handle:
                data = handle.read(limit + 1)
            if len(data) > limit:
                issues.append({"path": key, "code": "oversize_module"}); continue
            if key not in promoted and git_blob(data) != dict(PINS)[key]:
                issues.append({"path": key, "code": "accepted_blob_changed"})
            try:
                source = data.decode("utf-8")
            except UnicodeDecodeError:
                issues.append({"path": key, "code": "invalid_utf8"}); continue
            sources[key] = source
            codes = _phase2_live_issues(key, source) if key in promoted else _phase2_layer_issues(key, source) + form_issues(key, source)
            issues.extend({"path": key, "code": c} for c in codes)
    issues.extend({"path": p, "code": "missing_module"} for p in sorted(EXPECTED_PATHS - found))
    issues.extend({"path": "src/" + PACKAGE, "code": c} for c in import_cycle_issues(sources))
    for child in (root / "src").iterdir():
        if child.name == PACKAGE or (child.name == "source_integrity_toolkit.egg-info" and child.is_dir() and not child.is_symlink()):
            continue
        issues.append({"path": "src/" + child.name, "code": "unexpected_source_entry"})
    issues.sort(key=lambda r: (r["path"], r["code"]))
    return {"ok": not issues, "checked_modules": len(sources), "issues": issues,
            "promoted_modules": sorted(promoted), "protected_modules": len(EXPECTED_PATHS - promoted),
            "unit": f"P2-W{unit_number(unit):02}", "scope": "phase-aware developer checks; no analytical conformance claim"}



# These are the only executable historical assets this developer helper loads.
# Complete source bytes are checked against the separately pinned entry record.
HISTORICAL_TESTS = frozenset((
    "tests/scaffold/test_imports.py", "tests/scaffold/test_module_manifest.py",
    "tests/scaffold/test_no_runtime_implementation.py", "tests/scaffold/test_layer_boundaries.py",
    "tests/scaffold/test_contract_catalogs.py", "tests/scaffold/test_ci_contract.py",
))
HISTORICAL_NODES_SHA256 = "3262e08ba9825a41ab78ba55845a9f45ccf3195d3f33dc030cc28ce772eedc83"


def load_phase1_test(relative, namespace):
    """Execute a named, hash-pinned historical test, never candidate input.

    Full Git history is an explicit developer-test prerequisite. There is no
    network fetch, mutable-ref fallback, user-selected asset or product import.
    Keeping the actual old assertions avoids silently rewriting their meaning.
    """
    require(relative in HISTORICAL_TESTS, "unlisted_historical_test")
    root = Path(namespace["__file__"]).resolve().parents[2]
    entry = entry_manifest(root)
    raw = subprocess.check_output(["git", "show", INTAKE + ":" + relative], cwd=root,
                                  stderr=subprocess.PIPE, timeout=30)
    require(hashlib.sha256(raw).hexdigest() == entry["files"][relative], "historical_test_changed")
    name = namespace["__name__"]
    if name == "__main__":
        namespace["__name__"] = "__sit_frozen_test__"
    try:
        exec(compile(raw, str(root / relative), "exec", dont_inherit=True), namespace)
    finally:
        namespace["__name__"] = name


def historical_nodes(root):
    text = (root / "phase2/transition_ledger.md").read_text(encoding="utf-8")
    nodes = re.findall(r"^\| `(tests/[^`]+::[^`]+)` \| (?:retained|adapted) \| (?:same|`[^`]+`) \|$", text, re.M)
    require(len(nodes) == 194 and len(set(nodes)) == 194, "historical_identity_count")
    raw = ("\n".join(sorted(nodes)) + "\n").encode()
    require(hashlib.sha256(raw).hexdigest() == HISTORICAL_NODES_SHA256, "historical_identity_changed")
    return frozenset(nodes)



# Phase 3 has its own pinned authority and schedule. The Phase 2 constants and
# explicit APIs above remain historical controls with their original meaning.
PHASE3_PLAN_SHA256 = "e56da603271a489092ccfb9f9fe9086540bbb947ada8f4e7a676c8ed8f0feaae"
PHASE3_INTAKE = "80aa943f577f4a7deaeb8a0f3253c62d1263ca62"
PHASE3_INTAKE_TREE = "66ba4b112554ee227bf536e0716b51d555c10747"
PHASE3_PHASE2_COMMIT = "3a9b75ab6ca4ed9d7c97207043a5c8f54c2e2547"
PHASE3_PHASE2_TREE = "8e07404371fc9128ebdfcd85aab64936b15f7201"
PHASE3_ENTRY_SHA256 = "dfe96f57a222937131e8e4fafd13098f76d134cd88a50ffa9fa82891b9b9659b"
PHASE3_HISTORICAL_NODES_SHA256 = "830e15538696b1ea9370bc30f88c23a63e4b348438772e55812a858ab34e9266"
PHASE3_FIRST_UNIT = {
    "contracts/results.py": 2,
    "graph/projections.py": 4, "graph/traversal.py": 4,
    "graph/cycles.py": 4, "graph/witnesses.py": 4,
    "analysis/inventory.py": 5, "analysis/origins.py": 5,
    "analysis/process_comparison.py": 6,
    "analysis/contribution_profile.py": 7,
    "analysis/evaluator_lineage.py": 8, "analysis/human_review.py": 8,
    "analysis/presence.py": 9, "analysis/correction_routes.py": 10,
    "analysis/correction_outcomes.py": 11,
    "analysis/context.py": 12, "analysis/findings.py": 12,
}
PHASE3_EXTENSION_FIRST_UNIT = {
    "contracts/evidence.py": 3, "contracts/execution.py": 2,
    "contracts/report.py": 2, "validation/semantics.py": 3,
    "validation/limits.py": 2, "runtime/resources.py": 2,
    "runtime/diagnostics.py": 2, "runtime/boundary.py": 13,
}
PHASE3_INHERITED = frozenset(FIRST_UNIT)
PHASE3_FROZEN_PREPARATION = PHASE3_INHERITED - frozenset(PHASE3_EXTENSION_FIRST_UNIT)
PHASE3_PERMANENT_INERT = EXPECTED_PATHS - PHASE3_INHERITED - frozenset(PHASE3_FIRST_UNIT)
PHASE3_COMMON_PATHS = frozenset((
    "PHASE_3_PROGRESS.md", "phase3/module_policy.json",
    "phase3/implementation_evidence.json", "phase3/obligation_coverage.json",
))


def trusted_unit(unit=None):
    """Resolve a fixed context grammar without reading candidate metadata."""
    value = os.environ.get("SIT_PHASE_UNIT", "P2-W01") if unit is None else unit
    require(isinstance(value, str) and re.fullmatch(r"(?:P2-W0[1-9]|P3-W(?:0[1-9]|1[0-5]))", value),
            "invalid_trusted_unit")
    return value


def phase3_unit_number(unit=None):
    value = trusted_unit(unit)
    require(re.fullmatch(r"P3-W(?:0[1-9]|1[0-5])", value) is not None, "invalid_trusted_unit")
    return int(value[-2:])


def phase3_plan_paths(root):
    raw = (root / "PHASE_3_PLAN.md").read_bytes()
    require(hashlib.sha256(raw).hexdigest() == PHASE3_PLAN_SHA256, "approved_phase3_plan_changed")
    text = raw.decode("utf-8")
    common = re.findall(r"^The exact common record paths for W01-W15 are:\n\n```text\n(.*?)\n```", text, re.M | re.S)
    require(len(common) == 1 and frozenset(common[0].splitlines()) == PHASE3_COMMON_PATHS,
            "phase3_common_path_table")
    found = re.findall(r"^## \d+\. (P3-W(?:0[1-9]|1[0-5])):[^\n]*\n\nAdditional allowed paths:\n\n```text\n(.*?)\n```",
                       text, re.M | re.S)
    require([u for u, _ in found] == [f"P3-W{i:02}" for i in range(1, 16)], "phase3_unit_path_table")
    paths = {}
    product_first = {}
    prefix = "src/" + PACKAGE + "/"
    for unit, body in found:
        names = body.splitlines()
        require(len(names) == len(set(names)) and not (set(names) & PHASE3_COMMON_PATHS),
                "duplicate_phase3_path")
        for name in names:
            require(name and not name.startswith("/") and not any(p in ("", ".", "..") for p in name.split("/"))
                    and not any(c in name for c in ("\\", "\x00", "*", "?", "[", "]")), "invalid_phase3_path")
            if name.startswith(prefix):
                product_first.setdefault(name[len(prefix):], phase3_unit_number(unit))
        paths[unit] = frozenset(names) | PHASE3_COMMON_PATHS
    require(product_first == {**PHASE3_FIRST_UNIT, **PHASE3_EXTENSION_FIRST_UNIT},
            "phase3_product_schedule_mismatch")
    return paths


def phase3_entry_manifest(root):
    raw = (root / "phase3/entry_manifest.json").read_bytes()
    require(hashlib.sha256(raw).hexdigest() == PHASE3_ENTRY_SHA256, "phase3_entry_manifest_changed")
    entry = json.loads(raw, object_pairs_hook=unique)
    require(entry["format"] == "sit-phase3-entry/0.1" and entry["intake_commit"] == PHASE3_INTAKE
            and entry["intake_tree"] == PHASE3_INTAKE_TREE, "phase3_entry_identity")
    require(entry["phase2_commit"] == PHASE3_PHASE2_COMMIT and entry["phase2_tree"] == PHASE3_PHASE2_TREE,
            "phase3_accepted_predecessor_identity")
    require(entry["file_count"] == 157 and entry["plan_sha256"] == PHASE3_PLAN_SHA256,
            "phase3_entry_count_or_plan")
    files = entry["files"]
    require(type(files) is dict and len(files) == 157, "phase3_entry_file_count")
    require(all(type(p) is str and type(h) is str and re.fullmatch(r"[0-9a-f]{64}", h)
                for p, h in files.items()), "phase3_entry_file_identity")
    require(files.get("PHASE_3_PLAN.md") == PHASE3_PLAN_SHA256
            and "phase3/entry_manifest.json" not in files, "phase3_entry_boundary")
    prefix = "src/" + PACKAGE + "/"
    require({p[len(prefix):] for p in files if p.startswith(prefix)} == EXPECTED_PATHS,
            "phase3_entry_module_inventory")
    return entry


def phase3_policy_promotions(value, unit=None):
    current = phase3_unit_number(unit)
    require(type(value) is dict and set(value) == {
        "format", "plan_sha256", "active_unit", "first_units", "extension_first_units", "promotions"
    }, "phase3_policy_keys")
    require(value["format"] == "sit-phase3-modules/0.1" and value["plan_sha256"] == PHASE3_PLAN_SHA256,
            "phase3_policy_identity")
    require(value["active_unit"] == f"P3-W{current:02}", "policy_cannot_select_unit")
    require(value["first_units"] == PHASE3_FIRST_UNIT
            and value["extension_first_units"] == PHASE3_EXTENSION_FIRST_UNIT,
            "phase3_policy_cannot_expand_modules")
    rows = value["promotions"]
    require(type(rows) is list, "promotion_type")
    promoted = set()
    for row in rows:
        require(type(row) is dict and set(row) == {"path", "unit"}, "promotion_keys")
        path, step = row["path"], row["unit"]
        require(type(path) is str and path in PHASE3_FIRST_UNIT and path not in promoted,
                "unknown_or_duplicate_promotion")
        require(type(step) is int and PHASE3_FIRST_UNIT[path] == step <= current, "premature_promotion")
        promoted.add(path)
    require(promoted == {p for p, step in PHASE3_FIRST_UNIT.items() if step <= current},
            "phase3_scheduled_promotion_missing")
    return PHASE3_INHERITED | frozenset(promoted)


def phase3_promotions(root, unit=None):
    context = f"P3-W{phase3_unit_number(unit):02}"
    phase3_plan_paths(root)
    phase3_entry_manifest(root)
    value = json.loads((root / "phase3/module_policy.json").read_bytes(), object_pairs_hook=unique)
    return phase3_policy_promotions(value, context)


def phase3_mutable_modules(unit=None):
    current = phase3_unit_number(unit)
    return frozenset(p for p, step in {**PHASE3_FIRST_UNIT, **PHASE3_EXTENSION_FIRST_UNIT}.items()
                     if step <= current)


def promotions(root, unit=None):
    context = trusted_unit(unit)
    return phase3_promotions(root, context) if context.startswith("P3-") else _phase2_promotions(root, context)


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


def phase3_layer_issues(path, source, *, unit=None, promoted=None):
    current = phase3_unit_number(unit)
    expected = PHASE3_INHERITED | frozenset(p for p, step in PHASE3_FIRST_UNIT.items() if step <= current)
    require(promoted is None or frozenset(promoted) == expected, "phase3_dependency_policy_mismatch")
    return _dependency_issues(path, source, expected, "phase3_")


def _dependency_issues(path, source, active, prefix=""):
    """Current source dependencies; no historical policy or Git test loading."""
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError, RecursionError):
        return ["invalid_python"]
    targets, issues = phase3_import_targets(path, tree)
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
        if dependency.startswith("reporting/") or dependency in (
                "runtime/disclosure.py", "io/output_directory.py", "io/publication.py",
                "io/platform_linux.py", "io/platform_windows.py", "api.py", "cli.py", "__init__.py"):
            issues.append(prefix + "forbidden_dependency")
        elif dependency not in active and not dependency.endswith("/__init__.py"):
            issues.append(prefix + "unpromoted_dependency")
    return sorted(set(issues))


def phase3_import_cycle_issues(sources):
    by_name = {module_name(p): p for p in sources}
    dependencies = {}
    for path, source in sources.items():
        try:
            targets, _ = phase3_import_targets(path, ast.parse(source))
        except (SyntaxError, ValueError, RecursionError):
            return ["invalid_python"]
        dependencies[path] = {by_name[t] for t in targets if t in by_name}
    try:
        tuple(TopologicalSorter(dependencies).static_order())
    except CycleError:
        return ["import_cycle"]
    return []


def phase3_live_issues(path, source, *, unit=None, promoted=None):
    current = phase3_unit_number(unit)
    active = PHASE3_INHERITED | frozenset(p for p, step in PHASE3_FIRST_UNIT.items() if step <= current)
    require(promoted is None or frozenset(promoted) == active, "phase3_dependency_policy_mismatch")
    if path not in active:
        return ["unapproved_live_module"]
    issues = phase3_layer_issues(path, source, unit=unit, promoted=active)
    return sorted(set(issues + _source_effect_issues(path, source)))


def _source_effect_issues(path, source):
    """Conservative static effect checks, independent of development stage."""
    issues = []
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError, RecursionError):
        return ["invalid_python"]
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


def layer_issues(path, source, *, live=False, unit=None):
    context = trusted_unit(unit)
    if context.startswith("P3-") and live:
        return phase3_layer_issues(path, source, unit=context)
    return _phase2_layer_issues(path, source, live=live)


def live_issues(path, source, *, unit=None):
    context = trusted_unit(unit)
    return (phase3_live_issues(path, source, unit=context) if context.startswith("P3-")
            else _phase2_live_issues(path, source))


def phase3_check_repository(root, *, unit=None):
    issues, found, sources = [], set(), {}
    try:
        context = f"P3-W{phase3_unit_number(unit):02}"
        promoted = phase3_promotions(root, context)
        mutable = phase3_mutable_modules(context)
        entry = phase3_entry_manifest(root)
    except (ValueError, OSError, KeyError, TypeError):
        return {"ok": False, "checked_modules": 0, "issues": [{"path": "phase3", "code": "invalid_phase_policy"}]}
    package = root / "src" / PACKAGE
    if (root / "src").is_symlink() or package.is_symlink() or not package.is_dir():
        return {"ok": False, "checked_modules": 0, "issues": [{"path": "src/" + PACKAGE, "code": "missing_or_linked_package"}]}
    expected_dirs = {p.split("/")[0] for p in EXPECTED_PATHS if "/" in p}
    for directory, dirs, files in os.walk(package, followlinks=False):
        current = Path(directory)
        for name in list(dirs):
            child = current / name
            key = child.relative_to(package).as_posix()
            if child.is_symlink():
                issues.append({"path": key, "code": "linked_directory"}); dirs.remove(name)
            elif name == "__pycache__":
                if any(c.is_symlink() or not c.is_file() or c.suffix != ".pyc" for c in child.iterdir()):
                    issues.append({"path": key, "code": "unexpected_cache_entry"})
                dirs.remove(name)
            elif key not in expected_dirs:
                issues.append({"path": key, "code": "unexpected_directory"}); dirs.remove(name)
        for name in files:
            path = current / name
            key = path.relative_to(package).as_posix(); found.add(key)
            if path.is_symlink() or not path.is_file():
                issues.append({"path": key, "code": "not_regular_module"}); continue
            if key not in EXPECTED_PATHS:
                issues.append({"path": key, "code": "unexpected_package_file"}); continue
            limit = 262144 if key in promoted else 16384
            with path.open("rb") as handle:
                data = handle.read(limit + 1)
            if len(data) > limit:
                issues.append({"path": key, "code": "oversize_module"}); continue
            if key not in mutable and hashlib.sha256(data).hexdigest() != entry["files"]["src/" + PACKAGE + "/" + key]:
                issues.append({"path": key, "code": "accepted_blob_changed"})
            try:
                source = data.decode("utf-8")
            except UnicodeDecodeError:
                issues.append({"path": key, "code": "invalid_utf8"}); continue
            sources[key] = source
            codes = (phase3_live_issues(key, source, unit=context, promoted=promoted) if key in promoted
                     else _phase2_layer_issues(key, source) + form_issues(key, source))
            issues.extend({"path": key, "code": c} for c in codes)
    issues.extend({"path": p, "code": "missing_module"} for p in sorted(EXPECTED_PATHS - found))
    issues.extend({"path": "src/" + PACKAGE, "code": c} for c in phase3_import_cycle_issues(sources))
    for child in (root / "src").iterdir():
        if child.name == PACKAGE or (child.name == "source_integrity_toolkit.egg-info" and child.is_dir() and not child.is_symlink()):
            continue
        issues.append({"path": "src/" + child.name, "code": "unexpected_source_entry"})
    issues.sort(key=lambda row: (row["path"], row["code"]))
    return {"ok": not issues, "checked_modules": len(sources), "issues": issues,
            "promoted_modules": sorted(promoted), "protected_modules": len(EXPECTED_PATHS - promoted),
            "new_promoted_modules": sorted(promoted - PHASE3_INHERITED),
            "entry_byte_protected_modules": len(EXPECTED_PATHS - mutable),
            "unit": context, "scope": "phase-aware developer checks; no analytical conformance claim"}


def check_repository(root, *, unit=None):
    try:
        context = trusted_unit(unit)
    except ValueError:
        return {"ok": False, "checked_modules": 0, "issues": [{"path": "phase", "code": "invalid_phase_policy"}]}
    return phase3_check_repository(root, unit=context) if context.startswith("P3-") else _check_phase2_repository(root, unit=context)


def phase3_historical_nodes(root):
    text = (root / "phase3/transition_ledger.md").read_text(encoding="utf-8")
    nodes = re.findall(r"^\| `(tests/[^`]+::[^`]+)` \| (?:retained|adapted) \| (?:same|`[^`]+`) \|$", text, re.M)
    require(len(nodes) == 1650 and len(set(nodes)) == 1650, "phase3_historical_identity_count")
    raw = ("\n".join(sorted(nodes)) + "\n").encode()
    require(hashlib.sha256(raw).hexdigest() == PHASE3_HISTORICAL_NODES_SHA256, "phase3_historical_identity_changed")
    evidence = phase3_entry_manifest(root)["predecessor_tests"]
    require(evidence["count"] == 1650 and evidence["sorted_test_identity_sha256"] == PHASE3_HISTORICAL_NODES_SHA256,
            "phase3_predecessor_collection_identity")
    require(type(evidence["nodes"]) is list and len(evidence["nodes"]) == 1650
            and frozenset(evidence["nodes"]) == frozenset(nodes), "phase3_predecessor_collection_mismatch")
    return frozenset(nodes)


# Owner-approved verification consolidation. These literals are independent of
# candidate manifests and the one-time review map. Legacy entrypoints remain
# selected until the separately reviewed loader/CI switch (VC-03 through VC-05).
VC_ACCEPTED_HEAD = "2413a29b839b7e1de8f76a449762f031de19d52b"
VC_ACCEPTED_TREE = "e2f230bdf6f838f3d12df233559732aa1d5c1699"
VC_ACCEPTED_PARENTS = (
    "6dbca96f3314d537beed4ccb6202147bd9248dd9",
    "90684996eac568af6129973764fe40f3b666a15f",
)
VC_PLAN = "VERIFICATION_CONSOLIDATION_PLAN.md"
VC_PLAN_SHA256 = "a94b59a0bfdbde3c70c7286fd48c5e0cbdb4a538afeb094ba97dce718bd7d11d"
VC_REPOSITORY = "DavidWallstructurallaw/source-integrity-toolkit"
VC_BRANCH = "verification/consolidation"
VC_SUITE_TIMEOUT = 2400
VC_PATHS = frozenset((
    "tools/check_scaffold_boundary.py",
    "tests/scaffold/test_imports.py", "tests/scaffold/test_module_manifest.py",
    "tests/scaffold/test_no_runtime_implementation.py", "tests/scaffold/test_layer_boundaries.py",
    "tests/scaffold/test_contract_catalogs.py", "tests/scaffold/test_ci_contract.py",
    "tests/contract/test_phase2_transition.py", "tests/contract/test_phase3_transition.py",
    ".github/workflows/phase1-ci.yml", "tests/contract/test_bundle_contract.py",
    "tests/contract/test_input_schema_mapping.py", "tests/contract/test_observability_preparation.py",
    "tests/security/test_input_capture.py", "tests/security/test_preparation_inertness.py",
    "tests/contract/test_verification_boundary.py", "verification/consolidation_map.json",
    VC_PLAN, "VERIFICATION_CONSOLIDATION_COMPLETION.md", "README.md",
))
VC_REMOVABLE = frozenset((
    "tests/contract/test_phase2_transition.py", "tests/contract/test_phase3_transition.py",
))
VC_ACTIVE = frozenset("""contracts/bundle.py contracts/evidence.py contracts/constants.py
contracts/execution.py contracts/report.py contracts/results.py validation/limits.py
validation/structure.py validation/references.py validation/semantics.py runtime/resources.py
runtime/diagnostics.py runtime/boundary.py io/input_file.py graph/projections.py graph/traversal.py
graph/cycles.py graph/witnesses.py analysis/inventory.py analysis/origins.py
analysis/process_comparison.py analysis/contribution_profile.py analysis/evaluator_lineage.py
analysis/human_review.py analysis/presence.py analysis/correction_routes.py
analysis/correction_outcomes.py analysis/context.py analysis/findings.py""".split())
VC_MIXED_FUNCTIONS = {
    "tests/contract/test_bundle_contract.py": frozenset((
        "_repair_driver", "test_repair_exception_names_exactly_two_paths",
        "test_repair_does_not_expand_another_units_immediate_diff",
        "test_repair_cumulative_accounting_retains_only_authorized_extras",
        "test_repair_rejects_unlisted_and_similarly_named_paths",
        "test_repair_rejects_invalid_context_without_mutating_plan",
        "test_repair_preserves_original_observer_and_every_old_assertion")),
    "tests/contract/test_input_schema_mapping.py": frozenset((
        "test_r02_exact_extra_path_and_other_units_keep_their_immediate_scope",
        "test_r02_preserves_every_old_schema_assertion_except_the_named_stage_check")),
    "tests/contract/test_observability_preparation.py": frozenset((
        "historical_segment", "test_preserves_existing_report_declarations_and_w05_admission_body",
        "test_only_ten_w06_paths_and_no_old_test_permissions_changed")),
    "tests/security/test_input_capture.py": frozenset((
        "old_file", "ci_driver", "test_r01_exact_four_paths_and_no_other_unit_permission_expansion",
        "test_r01_similar_or_unlisted_repair_paths_are_refused",
        "test_r01_only_two_old_scope_test_bodies_change_and_identities_survive",
        "test_r01_execution_and_diagnostic_changes_are_exact_constant_additions")),
    # Keep the entire destructive witness until its fixture/context adaptation
    # is demonstrated in VC-03. A filename permission never waives assertions.
    "tests/security/test_preparation_inertness.py": frozenset(),
}
VC_TEST_SCOPES = ("contract", "integration", "scaffold", "security", "unit")


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
        header, separator, _ = body.partition(b"\n\n")
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
        result[oid] = {"tree": lines[0][5:], "parents": parents}
    return result


def _current_snapshot(root, commit):
    require(_current_oid(commit), "current_invalid_commit")
    raw = _current_git(root, "ls-tree", "-r", "-z", "--full-tree", commit)
    require(raw.endswith(b"\0"), "current_empty_or_malformed_tree")
    result = {}
    for row in raw[:-1].split(b"\0"):
        fields, tab, name = row.partition(b"\t")
        parts = fields.split(b" ")
        path = name.decode("utf-8")
        require(tab and len(parts) == 3 and _current_path(path) and path not in result,
                "current_malformed_tree_path")
        mode, kind, oid = (x.decode("ascii") for x in parts)
        require(kind == "blob" and mode in ("100644", "100755") and _current_oid(oid),
                "current_non_regular_tree_entry")
        result[path] = (mode, oid)
    return result


def current_authority(root):
    """The accepted merge bounds history; the approved plan bounds VC changes."""
    _current_git_state(root)
    metadata = current_commit_metadata(root, [VC_ACCEPTED_HEAD])[VC_ACCEPTED_HEAD]
    require(metadata == {"tree": VC_ACCEPTED_TREE, "parents": list(VC_ACCEPTED_PARENTS)},
            "current_accepted_anchor_mismatch")
    baseline = _current_snapshot(root, VC_ACCEPTED_HEAD)
    blobs = _current_objects(root, sorted({row[1] for row in baseline.values()}), "blob")
    return baseline, blobs


def current_context(event_name, event_json, review_head):
    """Only trusted runner event bytes and the separately supplied exact head.

    Branch/footer selection is subordinate to the owner-approved constants;
    no source manifest, dossier extension, map or environment unit grants scope.
    """
    require(_current_oid(review_head), "current_invalid_review_head")
    try:
        event = json.loads(event_json, object_pairs_hook=unique)
        require(event["repository"]["full_name"] == VC_REPOSITORY, "current_wrong_repository")
        if event_name == "pull_request":
            pr = event["pull_request"]
            require(pr["head"]["sha"] == review_head, "current_event_head_mismatch")
            require(pr["head"]["ref"] == VC_BRANCH and pr["head"]["repo"]["full_name"] == VC_REPOSITORY,
                    "current_unapproved_branch")
            require(pr["base"]["ref"] == "main" and pr["base"]["repo"]["full_name"] == VC_REPOSITORY,
                    "current_wrong_base_ref")
            base = pr["base"]["sha"]
        else:
            require(event_name == "push" and event["ref"] == "refs/heads/main", "current_unsupported_event")
            require(event["after"] == review_head and event["head_commit"]["id"] == review_head
                    and event.get("deleted", False) is False and event.get("forced", False) is False,
                    "current_event_head_mismatch")
            marks = re.findall(r"^[ \t]*SIT-(?:Verification|Phase)-Unit:[^\n]*$", event["head_commit"]["message"], re.M)
            require(marks == ["SIT-Verification-Unit: VC"], "current_invalid_merge_footer")
            base = event["before"]
        require(_current_oid(base) and base != "0" * 40 and base != review_head, "current_invalid_base")
        return {"unit": "VC", "base": base, "head": review_head, "event": event_name}
    except (KeyError, TypeError, json.JSONDecodeError) as exc:
        raise ValueError("current_malformed_event") from exc


def _current_retained_parts(path, raw):
    """Protect the accepted semantic portions of the four mixed test files.

    Only explicitly named historical functions are editable here. Dedicated
    imports/constants remain unchanged at VC-02; later dead-helper cleanup
    must demonstrate its call-site and retained-witness equivalence.
    """
    source = raw.decode("utf-8")
    tree = ast.parse(source)
    parts = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in VC_MIXED_FUNCTIONS[path]:
            continue
        first = min([node.lineno] + [n.lineno for n in getattr(node, "decorator_list", ())])
        parts.append("\n".join(source.splitlines()[first - 1:node.end_lineno]))
    return parts


def current_scope(baseline, actual, read_blob):
    """Compare actual regular-file inventories to the accepted tree.

    This is a path/byte ceiling, not permission to erase a mapped assertion.
    Retirement and the remaining mixed-file adaptations retain review gates.
    """
    require(all(_current_path(p) for p in actual), "current_path_alias")
    require(set(actual) - set(baseline) <= VC_PATHS, "current_unlisted_path")
    require(set(baseline) - set(actual) <= VC_REMOVABLE, "current_forbidden_deletion")
    require(VC_PLAN in actual, "current_approved_plan_missing")
    for path, row in actual.items():
        require(row[0] == (baseline[path][0] if path in baseline else "100644"), "current_file_mode_changed")
        if path in baseline and path not in VC_PATHS:
            require(row == baseline[path], "current_frozen_file_changed")
        if path in VC_MIXED_FUNCTIONS and row != baseline[path]:
            require(_current_retained_parts(path, read_blob(baseline[path][1])) ==
                    _current_retained_parts(path, read_blob(row[1])), "current_mixed_semantics_changed")
    require(hashlib.sha256(read_blob(actual[VC_PLAN][1])).hexdigest() == VC_PLAN_SHA256,
            "current_approved_plan_changed")


def current_history(root, base, head, authority=None):
    """Every post-acceptance commit, including reverted changes and side DAGs."""
    require(_current_oid(base) and _current_oid(head), "current_invalid_history_range")
    baseline, known_blobs = current_authority(root) if authority is None else authority
    _current_git(root, "merge-base", "--is-ancestor", VC_ACCEPTED_HEAD, base)
    _current_git(root, "merge-base", "--is-ancestor", base, head)
    raw = _current_git(root, "rev-list", "--reverse", "--topo-order", VC_ACCEPTED_HEAD + ".." + head)
    commits = raw.decode("ascii").splitlines()
    require(bool(commits) and all(_current_oid(c) for c in commits) and len(set(commits)) == len(commits),
            "current_empty_or_malformed_history")
    metadata = current_commit_metadata(root, commits)
    known, rows = {VC_ACCEPTED_HEAD}, []
    def read_blob(oid):
        if oid not in known_blobs:
            known_blobs.update(_current_objects(root, [oid], "blob"))
        return known_blobs[oid]
    for commit in commits:
        parents = metadata[commit]["parents"]
        require(parents and all(p in known for p in parents), "current_unanchored_parent")
        actual = _current_snapshot(root, commit)
        missing = sorted({row[1] for row in actual.values()} - set(known_blobs))
        known_blobs.update(_current_objects(root, missing, "blob"))
        current_scope(baseline, actual, read_blob)
        known.add(commit)
        rows.append({"commit": commit, **metadata[commit],
                     "changed_from_anchor": sorted(p for p in set(actual) | set(baseline)
                                                   if actual.get(p) != baseline.get(p))})
    require(head in known and (base == VC_ACCEPTED_HEAD or base in known), "current_missing_range_endpoint")
    return rows


def current_checkout(root, head, authority=None, *, require_clean=True):
    """Read index and worktree separately; do not trust assume-unchanged flags."""
    baseline, blobs = current_authority(root) if authority is None else authority
    require(_current_git(root, "rev-parse", "HEAD").decode("ascii").strip() == head,
            "current_checkout_head_mismatch")
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
    current_scope(baseline, index, read_blob)
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
    current_scope(baseline, actual, work_blobs.__getitem__)
    if require_clean:
        require(index == committed and actual == committed, "current_dirty_checkout")
    return {"tracked_files": len(index), "worktree_files": len(actual),
            "clean": index == committed == actual, "frozen_files": len(set(baseline) - VC_PATHS)}


def current_module_issues(sources):
    """Current 48-module effects/limits, separate from VC's all-product freeze."""
    issues, decoded = [], {}
    for path in sorted(set(sources) | set(EXPECTED_PATHS)):
        if path not in EXPECTED_PATHS:
            issues.append((path, "unexpected_module")); continue
        if path not in sources:
            issues.append((path, "missing_module")); continue
        raw = sources[path]
        if len(raw) > (262144 if path in VC_ACTIVE else 16384):
            issues.append((path, "oversize_module")); continue
        try:
            source = raw.decode("utf-8")
        except UnicodeDecodeError:
            issues.append((path, "invalid_utf8")); continue
        decoded[path] = source
        codes = (_dependency_issues(path, source, VC_ACTIVE) + _source_effect_issues(path, source)
                 if path in VC_ACTIVE else _phase2_layer_issues(path, source) + form_issues(path, source))
        issues.extend((path, code) for code in codes)
    issues.extend(("src/" + PACKAGE, code) for code in phase3_import_cycle_issues(decoded))
    return sorted(set(issues))


def current_modules(root):
    """Inspect the actual source tree, including ignored files and links."""
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
                sources[relative] = stream.read((262144 if relative in VC_ACTIVE else 16384) + 1)
    for child in source_root.iterdir():
        require(child.name == PACKAGE or (child.name == "source_integrity_toolkit.egg-info"
                and child.is_dir() and not child.is_symlink()), "current_unexpected_source_entry")
    require(not current_module_issues(sources), "current_module_boundary_failed")
    return len(sources)


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
    closed. The default driver's later VC wiring is a separate switch.
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


def current_verify(root, event_name, event_json, review_head):
    """Explicit VC entrypoint; no implicit environment or candidate promotion."""
    context = current_context(event_name, event_json, review_head)
    authority = current_authority(root)
    history = current_history(root, context["base"], review_head, authority)
    checkout = current_checkout(root, review_head, authority)
    modules = current_modules(root)
    current_workflow(json.loads((Path(root) / ".github/workflows/phase1-ci.yml").read_bytes(), object_pairs_hook=unique))
    return {"ok": True, **context, **checkout, "checked_modules": modules, "history": history}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--unit", choices=[f"P2-W{i:02}" for i in range(1, 10)] + [f"P3-W{i:02}" for i in range(1, 16)] + ["VC"], default=None)
    parser.add_argument("--event-name", choices=("pull_request", "push"))
    parser.add_argument("--event-file", type=Path)
    parser.add_argument("--head")
    args = parser.parse_args(argv)
    if args.unit == "VC":
        try:
            require(args.event_name and args.event_file and args.head, "current_external_context_required")
            result = current_verify(args.root, args.event_name, args.event_file.read_bytes(), args.head)
        except (ValueError, OSError, UnicodeError, SyntaxError) as exc:
            result = {"ok": False, "unit": "VC", "issues": [{"code": str(exc)}]}
    else:
        result = check_repository(args.root, unit=args.unit)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
