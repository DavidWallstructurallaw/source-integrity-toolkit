# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Developer-only package boundary checks, PHASE_1_PLAN.md sections 4, 6 and 9.

Checks use independently enumerated adopted paths and accepted W02 blob IDs.
The package's own metadata cannot grant itself an extra module or capability.
AST checks are independently testable without the byte pin. Import relationships
here concern software modules only, never an evidence/source graph.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
import os
from graphlib import CycleError, TopologicalSorter
from pathlib import Path

PACKAGE = "source_integrity_toolkit"
# Exact W02 objects as retained by the W03 manifest at accepted commit bad936b.
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
# These templates describe the accepted executable AST, independently of the
# candidate file under examination. They never execute, load or repair a module.
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
    "api.py": API_FORM,
    "cli.py": CLI_FORM,
    "contracts/constants.py": 'SCAFFOLD_VERSION = "0.1.0.dev0"',
    "__init__.py": '''from .api import audit_bundle, audit_file
from .contracts.constants import SCAFFOLD_VERSION as __version__
__all__ = ("audit_bundle", "audit_file", "__version__")''',
}


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def executable_ast(source: str) -> ast.Module:
    tree = ast.parse(source)
    # A docstring may identify the owner but does not execute behavior.
    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            if (node.body and isinstance(node.body[0], ast.Expr) and
                    isinstance(node.body[0].value, ast.Constant) and
                    isinstance(node.body[0].value.value, str)):
                node.body.pop(0)
    return tree


def module_name(path: str) -> str:
    parts = path.removesuffix(".py").split("/")
    if parts[-1] == "__init__":
        parts.pop()
    return ".".join((PACKAGE, *parts))


def layer(path: str) -> str:
    if path == "__init__.py":
        return "exports"
    return path.split("/", 1)[0] if "/" in path else "composition"


def import_targets(path: str, tree: ast.Module) -> tuple[list[str], list[str]]:
    """Resolve only syntactic Python imports, never execute import machinery."""
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
                prefix = parts[:len(parts) - node.level + 1]
                target = ".".join(prefix + ([node.module] if node.module else []))
            else:
                target = node.module or ""
            targets.append(target)
            if not node.module:
                targets.extend(target + "." + alias.name for alias in node.names)
    return targets, issues


def layer_issues(path: str, source: str) -> list[str]:
    try:
        tree = ast.parse(source)
    except (SyntaxError, ValueError, RecursionError):
        return ["invalid_python"]
    targets, issues = import_targets(path, tree)
    by_name = {module_name(p): p for p in EXPECTED_PATHS}
    for target in targets:
        if target in ("sys", "typing"):
            continue
        if target not in by_name:
            issues.append("unapproved_import")
            continue
        if layer(by_name[target]) not in LAYER_PERMISSIONS[layer(path)]:
            issues.append("layer_violation")
    return sorted(set(issues))


def form_issues(path: str, source: str) -> list[str]:
    if path not in EXPECTED_PATHS:
        return ["unexpected_module"]
    try:
        tree = executable_ast(source)
        expected = executable_ast(SPECIAL_FORMS.get(path, ""))
    except (SyntaxError, ValueError, RecursionError):
        return ["invalid_python"]
    return ([] if ast.dump(tree, include_attributes=False) == ast.dump(expected, include_attributes=False)
            else ["non_scaffold_body"])


def import_cycle_issues(sources: dict[str, str]) -> list[str]:
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


def check_repository(root: Path) -> dict:
    package = root / "src" / PACKAGE
    issues: list[dict] = []
    found: set[str] = set()
    sources: dict[str, str] = {}
    if (root / "src").is_symlink() or package.is_symlink() or not package.is_dir():
        return {"ok": False, "checked_modules": 0,
                "issues": [{"path": "src/" + PACKAGE, "code": "missing_or_linked_package"}]}
    expected_dirs = {p.split("/")[0] for p in EXPECTED_PATHS if "/" in p}
    for directory, dirs, files in os.walk(package, followlinks=False):
        current = Path(directory)
        relative = current.relative_to(package)
        for name in list(dirs):
            child = current / name
            child_rel = child.relative_to(package).as_posix()
            if child.is_symlink():
                issues.append({"path": child_rel, "code": "linked_directory"})
                dirs.remove(name)
            elif name == "__pycache__":
                # CPython may create ordinary caches. Reject code, native files,
                # links or subdirectories masquerading as a cache.
                for cached in child.iterdir():
                    if cached.is_symlink() or not cached.is_file() or cached.suffix != ".pyc":
                        issues.append({"path": child_rel, "code": "unexpected_cache_entry"})
                dirs.remove(name)
            elif child_rel not in expected_dirs:
                issues.append({"path": child_rel, "code": "unexpected_directory"})
                dirs.remove(name)
        for name in files:
            path = current / name
            key = path.relative_to(package).as_posix()
            found.add(key)
            if path.is_symlink() or not path.is_file():
                issues.append({"path": key, "code": "not_regular_module"})
                continue
            if key not in EXPECTED_PATHS:
                issues.append({"path": key, "code": "unexpected_package_file"})
                continue
            with path.open("rb") as handle:
                data = handle.read(16385)
            if len(data) > 16384:
                issues.append({"path": key, "code": "oversize_module"})
                continue
            if git_blob(data) != dict(PINS)[key]:
                issues.append({"path": key, "code": "accepted_blob_changed"})
            try:
                source = data.decode("utf-8")
            except UnicodeDecodeError:
                issues.append({"path": key, "code": "invalid_utf8"})
                continue
            sources[key] = source
            issues.extend({"path": key, "code": code}
                          for code in layer_issues(key, source) + form_issues(key, source))
    issues.extend({"path": p, "code": "missing_module"} for p in sorted(EXPECTED_PATHS - found))
    issues.extend({"path": "src/" + PACKAGE, "code": code}
                  for code in import_cycle_issues(sources))
    # Reject additional source packages/modules, while permitting the conventional
    # local build backend's metadata directory outside the installed package.
    for child in (root / "src").iterdir():
        if child.name == PACKAGE:
            continue
        if child.name == "source_integrity_toolkit.egg-info" and child.is_dir() and not child.is_symlink():
            continue
        issues.append({"path": "src/" + child.name, "code": "unexpected_source_entry"})
    issues.sort(key=lambda row: (row["path"], row["code"]))
    return {"ok": not issues, "checked_modules": len(sources), "issues": issues,
            "scope": "accepted W02 module bytes, closed scaffold AST, software-import layers"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    result = check_repository(parser.parse_args(argv).root)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
