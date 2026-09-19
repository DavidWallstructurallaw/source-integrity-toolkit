# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Developer-only Phase 2 boundary checks; never imported by the product.

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
import subprocess
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


def promotions(root, unit=None):
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


def layer_issues(path, source, *, live=False):
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


def live_issues(path, source):
    if path not in FIRST_UNIT:
        return ["unapproved_live_module"]
    issues = layer_issues(path, source, live=True)
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


def check_repository(root, *, unit=None):
    issues, found, sources = [], set(), {}
    try:
        promoted = promotions(root, unit)
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
            codes = live_issues(key, source) if key in promoted else layer_issues(key, source) + form_issues(key, source)
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


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--unit", choices=[f"P2-W{i:02}" for i in range(1, 10)], default=None)
    args = parser.parse_args(argv)
    result = check_repository(args.root, unit=args.unit)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
