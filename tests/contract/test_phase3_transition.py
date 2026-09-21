# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Independent P3-W01 guard, scope and cumulative-retention counterexamples.

Oracles: approved PHASE_3_PLAN.md sections 4-6 and its fifteen explicit path
lists; the accepted planning commit; accepted W09 run 35519939650 collection.
No expected module, path or predecessor identity is copied from a guard result.
These developer tests establish no analytical field or public/native behavior.
"""
import ast
import copy
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools import check_scaffold_boundary as guard

ENTRY = "80aa943f577f4a7deaeb8a0f3253c62d1263ca62"
ENTRY_TREE = "66ba4b112554ee227bf536e0716b51d555c10747"
PHASE2 = "3a9b75ab6ca4ed9d7c97207043a5c8f54c2e2547"
PHASE2_TREE = "8e07404371fc9128ebdfcd85aab64936b15f7201"
PLAN_SHA256 = "e56da603271a489092ccfb9f9fe9086540bbb947ada8f4e7a676c8ed8f0feaae"
NODES_SHA256 = "830e15538696b1ea9370bc30f88c23a63e4b348438772e55812a858ab34e9266"
PACKAGE = "src/source_integrity_toolkit/"

# Literal transcription of approved plan section 4, independent of checker code.
FIRST_UNITS = {
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
EXTENSION_UNITS = {
    "contracts/execution.py": 2, "contracts/report.py": 2,
    "runtime/resources.py": 2, "runtime/diagnostics.py": 2,
    "validation/limits.py": 2, "contracts/evidence.py": 3,
    "validation/semantics.py": 3, "runtime/boundary.py": 13,
}
FROZEN_PREPARATION = frozenset((
    "contracts/bundle.py", "contracts/constants.py", "io/input_file.py",
    "validation/references.py", "validation/structure.py",
))
INHERITED = frozenset(EXTENSION_UNITS) | FROZEN_PREPARATION
PERMANENT_INERT = frozenset((
    "__init__.py", "api.py", "cli.py", "contracts/__init__.py",
    "analysis/__init__.py", "graph/__init__.py", "io/__init__.py",
    "reporting/__init__.py", "runtime/__init__.py", "validation/__init__.py",
    "reporting/assemble.py", "reporting/json_report.py",
    "reporting/markdown_report.py", "reporting/escaping.py",
    "runtime/disclosure.py", "io/output_directory.py", "io/publication.py",
    "io/platform_linux.py", "io/platform_windows.py",
))
COMMON = frozenset((
    "PHASE_3_PROGRESS.md", "phase3/module_policy.json",
    "phase3/implementation_evidence.json", "phase3/obligation_coverage.json",
))
# Each numbered entry transcribes the additional list in plan sections 6-20.
ADDITIONAL = {
    1: frozenset((
        "phase3/entry_manifest.json", "phase3/transition_ledger.md", "phase3/ci_review.md",
        "tools/check_scaffold_boundary.py", "tests/scaffold/test_ci_contract.py",
        "tests/scaffold/test_imports.py", "tests/scaffold/test_module_manifest.py",
        "tests/scaffold/test_no_runtime_implementation.py", "tests/scaffold/test_layer_boundaries.py",
        "tests/scaffold/test_contract_catalogs.py", "tests/contract/test_phase2_transition.py",
        "tests/contract/test_phase3_transition.py", "tests/contract/test_bundle_contract.py",
        "tests/contract/test_input_schema_mapping.py", "tests/contract/test_observability_preparation.py",
        "tests/security/test_input_capture.py", "tests/security/test_preparation_inertness.py",
        ".github/workflows/phase1-ci.yml", "README.md",
    )),
    2: frozenset((
        PACKAGE + "contracts/results.py", PACKAGE + "contracts/report.py",
        PACKAGE + "contracts/execution.py", PACKAGE + "runtime/resources.py",
        PACKAGE + "runtime/diagnostics.py", PACKAGE + "validation/limits.py",
        "tests/contract/test_result_contract.py", "tests/contract/test_prerequisite_contract.py",
        "tests/security/test_analytical_resource_limits.py", "tests/security/test_analytical_diagnostics.py",
    )),
    3: frozenset((
        PACKAGE + "contracts/evidence.py", PACKAGE + "validation/semantics.py",
        "tests/contract/test_analytical_basis.py", "tests/contract/test_analytical_temporal.py",
        "tests/unit/test_provenance_profile.py",
    )),
    4: frozenset((
        PACKAGE + "graph/projections.py", PACKAGE + "graph/traversal.py",
        PACKAGE + "graph/cycles.py", PACKAGE + "graph/witnesses.py",
        "tests/contract/test_graph_views.py", "tests/unit/test_graph_traversal.py",
        "tests/unit/test_graph_cycles.py", "tests/unit/test_graph_witnesses.py",
        "tests/security/test_graph_limits.py",
    )),
    5: frozenset((
        PACKAGE + "analysis/inventory.py", PACKAGE + "analysis/origins.py",
        "tests/unit/test_inventory.py", "tests/unit/test_origins.py", "tests/unit/test_ancestry_frontiers.py",
    )),
    6: frozenset((PACKAGE + "analysis/process_comparison.py", "tests/unit/test_process_comparison.py")),
    7: frozenset((PACKAGE + "analysis/contribution_profile.py", "tests/unit/test_contribution_profile.py",
                  "tests/unit/test_immediate_inheritance.py")),
    8: frozenset((PACKAGE + "analysis/evaluator_lineage.py", PACKAGE + "analysis/human_review.py",
                  "tests/unit/test_evaluator_lineage.py", "tests/unit/test_human_review.py")),
    9: frozenset((PACKAGE + "analysis/presence.py", "tests/unit/test_presence.py", "tests/unit/test_pipeline_cohorts.py")),
    10: frozenset((PACKAGE + "analysis/correction_routes.py", "tests/unit/test_correction_routes.py")),
    11: frozenset((PACKAGE + "analysis/correction_outcomes.py", "tests/unit/test_correction_outcomes.py")),
    12: frozenset((PACKAGE + "analysis/context.py", PACKAGE + "analysis/findings.py",
                   "tests/unit/test_context_preservation.py", "tests/unit/test_findings.py",
                   "tests/contract/test_finding_boundaries.py")),
    13: frozenset((
        PACKAGE + "runtime/boundary.py", PACKAGE + "runtime/resources.py",
        PACKAGE + "runtime/diagnostics.py", PACKAGE + "contracts/execution.py", PACKAGE + "contracts/report.py",
        "tests/integration/test_analytical_pipeline.py", "tests/contract/test_analytical_observability.py",
        "tests/security/test_analytical_interruption.py",
    )),
    14: frozenset((
        "phase3/ci_review.md", "tests/contract/test_analytical_obligations.py",
        "tests/contract/test_analytical_mutants.py", "tests/integration/test_analytical_hero_inputs.py",
        "tests/integration/test_analytical_determinism.py", "tests/integration/test_analytical_installed_runtime.py",
        "tests/security/test_analytical_inertness.py", "tests/security/test_analytical_adversarial.py",
        "tests/fixtures/micro/phase3_cases.json", "tests/fixtures/adversarial/phase3_cases.json",
        "tests/golden/phase3_core_expectations.json", "README.md",
    )),
    15: frozenset(("PHASE_3_COMPLETION.md", "phase3/delivery_manifest.json", "README.md")),
}

# Reviewed P3-W01 migration bytes. These six source files have no later normal
# Phase 3 write permission. Their old assertions were independently compared
# with the accepted entry; the original live behavior tests still execute.
# This separate test file is outside the pin set, avoiding a self-reference.
LIVE_MIGRATION_SHA256 = {
    "tests/contract/test_phase2_transition.py": "ddfe98d62cf13aec936a44a4fb970c03ee04ae187cacdcd54f31565b0be17bee",
    "tests/contract/test_bundle_contract.py": "53ff31b641652074e1c7d516ab7a9d714bc4d33a065cef27d6f275d92fdd584b",
    "tests/contract/test_input_schema_mapping.py": "31ea82cb0a96754424a58c1b106341f0d4891a05bb7b949957402bd820925c94",
    "tests/contract/test_observability_preparation.py": "5d6ecf880e5e77bc606670c9e2bc232df662ac026ddb51c145f86fd7fb6b54b8",
    "tests/security/test_input_capture.py": "e8bfab38536db60d6ec5a44412f77f2b522bfebd39c1f861dfe212a1e91784ff",
    "tests/security/test_preparation_inertness.py": "0a6ff2d62f8d5dca61d37fda2a12edce4bcaa428954f7b7042fc1f7a03fe33fa",
}


def assert_live_migration_bytes(candidates):
    assert set(candidates) == set(LIVE_MIGRATION_SHA256), "migration_source_inventory_changed"
    for path, expected in LIVE_MIGRATION_SHA256.items():
        assert hashlib.sha256(candidates[path]).hexdigest() == expected, "migration_source_bytes_changed: " + path


def git_bytes(path, commit=ENTRY):
    return subprocess.check_output(["git", "show", commit + ":" + path], cwd=ROOT,
                                   stderr=subprocess.PIPE, timeout=30)


def ci_driver():
    spec = importlib.util.spec_from_file_location("sit_phase3_test_driver", ROOT / "tests/scaffold/test_ci_contract.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def policy_for(step):
    """Approved plan schedule, never derived from the implementation's policy."""
    return {"format": "sit-phase3-modules/0.1", "active_unit": f"P3-W{step:02}",
            "plan_sha256": PLAN_SHA256, "first_units": dict(FIRST_UNITS),
            "extension_first_units": dict(EXTENSION_UNITS),
            "promotions": [{"path": path, "unit": first} for path, first in FIRST_UNITS.items() if first <= step]}


@pytest.fixture
def isolated_entry(tmp_path):
    """Real W01 product bytes and metadata, with all mutations outside checkout."""
    root = tmp_path / "guard-copy"
    for path in subprocess.check_output(["git", "ls-tree", "-r", "--name-only", ENTRY, "src"], cwd=ROOT, text=True).splitlines():
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(git_bytes(path))
    for path in ("PHASE_3_PLAN.md", "phase3/entry_manifest.json"):
        target = root / path
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / path, target)
    (root / "phase3/module_policy.json").write_text(json.dumps(policy_for(1)), encoding="utf-8")
    assert guard.check_repository(root, unit="P3-W01")["ok"]
    return root


def test_approved_plan_and_actual_entry_are_independently_pinned():
    assert hashlib.sha256((ROOT / "PHASE_3_PLAN.md").read_bytes()).hexdigest() == PLAN_SHA256
    assert subprocess.check_output(["git", "rev-parse", ENTRY + "^{tree}"], cwd=ROOT, text=True).strip() == ENTRY_TREE
    assert subprocess.check_output(["git", "rev-parse", PHASE2 + "^{tree}"], cwd=ROOT, text=True).strip() == PHASE2_TREE
    entry = guard.phase3_entry_manifest(ROOT)
    assert (entry["intake_commit"], entry["intake_tree"], entry["file_count"]) == (ENTRY, ENTRY_TREE, 157)
    assert (entry["phase2_commit"], entry["phase2_tree"]) == (PHASE2, PHASE2_TREE)
    paths = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", ENTRY], cwd=ROOT, text=True).splitlines()
    assert len(paths) == 157 and set(entry["files"]) == set(paths)
    for path in paths:
        assert entry["files"][path] == hashlib.sha256(git_bytes(path)).hexdigest(), path
    parent = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", PHASE2], cwd=ROOT, text=True).splitlines()
    assert len(parent) == 156 and set(paths) - set(parent) == {"PHASE_3_PLAN.md"}


def test_closed_module_ceiling_and_first_units_match_approved_plan():
    assert guard.PHASE3_FIRST_UNIT == FIRST_UNITS
    assert guard.PHASE3_EXTENSION_FIRST_UNIT == EXTENSION_UNITS
    assert guard.PHASE3_INHERITED == INHERITED
    assert guard.PHASE3_FROZEN_PREPARATION == FROZEN_PREPARATION
    assert guard.PHASE3_PERMANENT_INERT == PERMANENT_INERT
    assert len(FIRST_UNITS) == 16 and len(INHERITED) == 13
    assert len(set(FIRST_UNITS) | INHERITED) == 29 and len(PERMANENT_INERT) == 19
    assert not (set(FIRST_UNITS) | INHERITED) & PERMANENT_INERT
    assert set(guard.EXPECTED_PATHS) == set(FIRST_UNITS) | INHERITED | PERMANENT_INERT


@pytest.mark.parametrize("step", range(1, 16))
def test_each_unit_has_exact_four_common_records_and_approved_paths(step):
    paths = guard.phase3_plan_paths(ROOT)
    ci = ci_driver()
    unit = f"P3-W{step:02}"
    expected = COMMON | ADDITIONAL[step]
    assert set(paths) == {f"P3-W{number:02}" for number in range(1, 16)}
    assert paths[unit] == expected
    assert ci.phase3_effective_paths(paths, unit) == expected
    ci.phase3_check_changed_paths(paths, unit, expected)
    cumulative = COMMON | frozenset().union(*(ADDITIONAL[number] for number in range(1, step + 1)))
    assert ci.phase3_effective_paths(paths, unit, cumulative=True) == cumulative
    assert len(COMMON) == 4
    for future_path in (COMMON | frozenset().union(*ADDITIONAL.values())) - expected:
        with pytest.raises(ValueError, match="^work_unit_allowlist_exceeded$"):
            ci.phase3_check_changed_paths(paths, unit, {future_path})


@pytest.mark.parametrize("step", range(1, 16))
def test_only_scheduled_new_modules_are_promoted_and_mutable(step):
    unit = f"P3-W{step:02}"
    expected = INHERITED | {path for path, first in FIRST_UNITS.items() if first <= step}
    assert guard.phase3_policy_promotions(policy_for(step), unit) == expected
    mutable = {path for path, first in (FIRST_UNITS | EXTENSION_UNITS).items() if first <= step}
    assert guard.phase3_mutable_modules(unit) == mutable
    assert not mutable & FROZEN_PREPARATION and not mutable & PERMANENT_INERT


def test_real_checkout_still_passes_and_w01_product_bytes_are_exact():
    unit = os.environ["SIT_PHASE_UNIT"]
    step = guard.phase3_unit_number(unit)
    result = guard.check_repository(ROOT, unit=unit)
    assert result["ok"], result
    expected = INHERITED | {path for path, first in FIRST_UNITS.items() if first <= step}
    assert result["checked_modules"] == 48
    assert result["protected_modules"] == 48 - len(expected)
    for path in (set(FIRST_UNITS) | INHERITED | PERMANENT_INERT) - guard.phase3_mutable_modules(unit):
        assert (ROOT / PACKAGE / path).read_bytes() == git_bytes(PACKAGE + path), path
    assert not any(path.startswith(PACKAGE) for path in COMMON | ADDITIONAL[1])


@pytest.mark.parametrize("path", ("contracts/results.py", "contracts/evidence.py", "api.py", "io/platform_windows.py"))
def test_w01_paired_policy_and_product_mutation_cannot_self_authorize(isolated_entry, path):
    candidate = policy_for(1)
    candidate["first_units"][path] = 1
    candidate["promotions"].append({"path": path, "unit": 1})
    (isolated_entry / "phase3/module_policy.json").write_text(json.dumps(candidate), encoding="utf-8")
    (isolated_entry / PACKAGE / path).write_text("def unauthorized():\n    return 42\n", encoding="utf-8")
    assert not guard.check_repository(isolated_entry, unit="P3-W01")["ok"]
    with pytest.raises(ValueError):
        guard.phase3_policy_promotions(candidate, "P3-W01")


@pytest.mark.parametrize("path", ("contracts/bundle.py", "runtime/boundary.py", "contracts/results.py", "reporting/assemble.py"))
def test_w01_rejects_even_pure_or_comment_only_product_byte_changes(isolated_entry, path):
    target = isolated_entry / PACKAGE / path
    target.write_bytes(target.read_bytes() + b"\n# Unapproved W01 byte change.\n")
    assert not guard.check_repository(isolated_entry, unit="P3-W01")["ok"]


def test_paired_plan_policy_and_entry_digest_edits_cannot_self_authorize(isolated_entry):
    plan = isolated_entry / "PHASE_3_PLAN.md"
    plan.write_bytes(plan.read_bytes() + b"\nPermit every module at W01.\n")
    altered_digest = hashlib.sha256(plan.read_bytes()).hexdigest()
    candidate = policy_for(1)
    candidate["plan_sha256"] = altered_digest
    (isolated_entry / "phase3/module_policy.json").write_text(json.dumps(candidate), encoding="utf-8")
    entry_path = isolated_entry / "phase3/entry_manifest.json"
    entry = json.loads(entry_path.read_bytes())
    entry["plan_sha256"] = altered_digest
    entry["files"]["PHASE_3_PLAN.md"] = altered_digest
    entry_path.write_text(json.dumps(entry), encoding="utf-8")
    assert not guard.check_repository(isolated_entry, unit="P3-W01")["ok"]


def test_entry_file_and_matching_candidate_product_hash_cannot_self_approve(isolated_entry):
    path = PACKAGE + "contracts/results.py"
    (isolated_entry / path).write_bytes(b"def unexpected():\n    return 42\n")
    entry_path = isolated_entry / "phase3/entry_manifest.json"
    value = json.loads(entry_path.read_bytes())
    value["files"][path] = hashlib.sha256((isolated_entry / path).read_bytes()).hexdigest()
    entry_path.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(ValueError):
        guard.phase3_entry_manifest(isolated_entry)
    assert not guard.check_repository(isolated_entry, unit="P3-W01")["ok"]


@pytest.mark.parametrize("unit", ("P3-W00", "P3-W16", "P3-W1", "P4-W01", "P2-W09", "P3-W01;echo", "P3-W01\n", 1, None))
def test_phase3_context_rejects_unknown_nonexact_or_other_phase_values(unit):
    if unit is None:
        with patch.dict(os.environ, {}, clear=True):
            with pytest.raises(ValueError):
                guard.phase3_unit_number()
    else:
        with pytest.raises(ValueError):
            guard.phase3_unit_number(unit)


def test_candidate_policy_cannot_select_or_advance_trusted_context():
    candidate = policy_for(2)
    assert guard.phase3_policy_promotions(candidate, "P3-W02") == INHERITED | {"contracts/results.py"}
    with patch.dict(os.environ, {"SIT_PHASE_UNIT": "P3-W01"}):
        with pytest.raises(ValueError):
            guard.phase3_policy_promotions(candidate)
    for unit in ("P2-W09", "P3-W01", "P3-W03"):
        with pytest.raises(ValueError):
            guard.phase3_policy_promotions(candidate, unit)


@pytest.mark.parametrize("mode", ("value", "utf8"))
def test_source_extensions_cannot_select_stage_or_complete_analytical_checks(mode):
    from source_integrity_toolkit.runtime.boundary import _prepare_evidence_value, _prepare_evidence_utf8
    from source_integrity_toolkit.contracts.report import _ObservabilityPreparation
    source = json.loads((ROOT / "tests/fixtures/hero/H7-01.bundle.json").read_bytes())
    source["extensions"] = {"fictional:phase_authority": {
        "SIT_PHASE_UNIT": "P3-W15", "active_unit": "P3-W15", "approved": True,
        "first_units": {"api.py": 1}, "promotions": [{"path": "api.py", "unit": 1}],
    }}
    original = copy.deepcopy(source)
    policy_before = (ROOT / "phase3/module_policy.json").read_bytes()
    with patch.dict(os.environ, {"SIT_PHASE_UNIT": "P3-W01"}):
        result = _prepare_evidence_value(source) if mode == "value" else _prepare_evidence_utf8(json.dumps(source).encode())
        assert type(result) is _ObservabilityPreparation and result.input_state == "accepted"
        assert result.inquiries
        for inquiry in result.inquiries:
            assert [item.prerequisite for item in inquiry.prerequisites if item.complete_check_executed] == ["PC01"]
            assert all(item.answer is None for item in inquiry.prerequisites[1:])
        assert guard.phase3_unit_number() == 1
        assert guard.phase3_policy_promotions(policy_for(1)) == INHERITED
        assert source == original
    assert (ROOT / "phase3/module_policy.json").read_bytes() == policy_before


@pytest.mark.parametrize("mutation", ("premature", "missing", "duplicate", "wrong_first", "wrong_extension", "forbidden", "source_context", "bool_unit"))
def test_policy_schedule_and_closed_keys_reject_specific_mutants(mutation):
    value = policy_for(2)
    assert guard.phase3_policy_promotions(value, "P3-W02") == INHERITED | {"contracts/results.py"}
    if mutation == "premature":
        value["promotions"].append({"path": "analysis/origins.py", "unit": 5})
    elif mutation == "missing":
        value["promotions"] = []
    elif mutation == "duplicate":
        value["promotions"] *= 2
    elif mutation == "wrong_first":
        value["first_units"]["analysis/origins.py"] = 2
    elif mutation == "wrong_extension":
        value["extension_first_units"]["runtime/boundary.py"] = 2
    elif mutation == "forbidden":
        value["first_units"]["api.py"] = 2
        value["promotions"].append({"path": "api.py", "unit": 2})
    elif mutation == "source_context":
        value["SIT_PHASE_UNIT"] = "P3-W02"
    else:
        value["promotions"][0]["unit"] = True
    with pytest.raises(ValueError):
        guard.phase3_policy_promotions(value, "P3-W02")


@pytest.mark.parametrize("path", ("phase3/module_policy.json.bak", "phase3/../phase3/module_policy.json",
    "PHASE_3_PLAN.md", "PHASE_2_COMPLETION.md", "phase2/module_policy.json", "phase2/transition_ledger.md",
    "tests/fixtures/hero/H7-01.bundle.json", "pyproject.toml", "requirements-dev.txt", "src/source_integrity_toolkit/api.py"))
def test_unlisted_lookalike_frozen_and_product_paths_are_refused(path):
    ci = ci_driver()
    paths = guard.phase3_plan_paths(ROOT)
    with pytest.raises(ValueError, match="^work_unit_allowlist_exceeded$"):
        ci.phase3_check_changed_paths(paths, "P3-W01", COMMON | ADDITIONAL[1] | {path})


@pytest.mark.parametrize("source", (
    "from ..analysis import origins\n", "from ..analysis.origins import analyze\n",
    "from ..analysis import origins as harmless_name\n", "from ..reporting import assemble\n",
    "from ..io import platform_windows\n", "import recursive_integrity_toolkit\n", "import socket\n",
))
def test_phase3_live_import_checks_reject_unactivated_and_forbidden_dependencies(source):
    assert guard.phase3_live_issues("runtime/boundary.py", source, unit="P3-W01")


def test_scheduled_graph_import_has_real_positive_and_premature_controls():
    source = "from ..graph import traversal\ndef inspect(value):\n    return value\n"
    assert guard.phase3_live_issues("analysis/origins.py", source, unit="P3-W01")
    assert guard.phase3_live_issues("analysis/origins.py", source, unit="P3-W05") == []


def test_current_frozen_phase2_records_keep_their_accepted_bytes():
    paths = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", ENTRY, "phase2"], cwd=ROOT, text=True).splitlines()
    assert paths and "phase2/module_policy.json" in paths and "phase2/transition_ledger.md" in paths
    for path in paths:
        assert (ROOT / path).read_bytes() == git_bytes(path), path
    for path in ("PHASE_2_PLAN.md", "PHASE_2_PROGRESS.md", "PHASE_2_COMPLETION.md"):
        assert (ROOT / path).read_bytes() == git_bytes(path), path


def test_all_1650_predecessor_identities_are_independently_anchored():
    nodes = guard.phase3_historical_nodes(ROOT)
    assert len(nodes) == 1650 and len(set(nodes)) == 1650
    assert len({node.split("::", 1)[0] for node in nodes}) == 34
    assert hashlib.sha256(("\n".join(sorted(nodes)) + "\n").encode()).hexdigest() == NODES_SHA256
    assert guard.historical_nodes(ROOT) <= nodes


def test_collection_accepts_real_predecessors_and_rejects_same_count_replacement():
    ci = ci_driver()
    nodes = sorted(guard.phase3_historical_nodes(ROOT))
    files = {node.split("::", 1)[0] for node in nodes}
    with patch.dict(os.environ, {"SIT_PHASE_UNIT": "P3-W01"}):
        ci.collection_check(nodes, files)
        missing = [node for node in nodes if "test_w09_event_and_main_footer_resolve_independent_context" not in node]
        assert len(missing) == 1649
        missing.append("tests/contract/test_phase2_transition.py::InventedCountReplacement::test_fake")
        with pytest.raises(ValueError):
            ci.collection_check(missing, files)
        with pytest.raises(ValueError):
            ci.collection_check(nodes + [nodes[-1]], files)
        with pytest.raises(ValueError):
            ci.collection_check(nodes, files | {"tests/contract/test_missing.py"})


def test_retained_test_entrypoints_remain_present_in_current_test_sources():
    files = {node.split("::", 1)[0] for node in guard.phase3_historical_nodes(ROOT)}
    def names(raw):
        result = set()
        for node in ast.parse(raw).body:
            if isinstance(node, ast.FunctionDef) and node.name.startswith("test_"):
                result.add(node.name)
            elif isinstance(node, ast.ClassDef):
                result.update(node.name + "." + child.name for child in node.body
                              if isinstance(child, ast.FunctionDef) and child.name.startswith("test_"))
        return result
    for path in sorted(files):
        assert names(git_bytes(path)) <= names((ROOT / path).read_bytes()), path


def test_current_migration_sources_match_reviewed_bytes_and_remain_live():
    assert len(LIVE_MIGRATION_SHA256) == 6
    assert "tests/contract/test_phase3_transition.py" not in LIVE_MIGRATION_SHA256
    assert_live_migration_bytes({path: (ROOT / path).read_bytes() for path in LIVE_MIGRATION_SHA256})
    later_scopes = frozenset().union(*(ADDITIONAL[number] for number in range(2, 16))) | COMMON
    assert not set(LIVE_MIGRATION_SHA256) & later_scopes
    # These two untouched historical permission-test sources are pinned too.
    for path in ("tests/contract/test_bundle_contract.py", "tests/contract/test_input_schema_mapping.py"):
        assert (ROOT / path).read_bytes() == git_bytes(path)


@pytest.mark.parametrize("mutation", ("weakened_assertion", "removed_observer", "reversed_guard", "missing_file", "extra_file", "historical_snapshot"))
def test_live_migration_guard_rejects_weakened_assertions_and_missing_observers(mutation):
    original = {path: (ROOT / path).read_bytes() for path in LIVE_MIGRATION_SHA256}
    assert_live_migration_bytes(original)
    changed = dict(original)
    path = "tests/security/test_preparation_inertness.py"
    if mutation == "weakened_assertion":
        path = "tests/contract/test_phase2_transition.py"
        before = b'        self.assertEqual(outcome["checked_modules"], 48)'
        assert before in changed[path]
        changed[path] = changed[path].replace(before, b"        self.assertTrue(True)", 1)
    elif mutation == "removed_observer":
        before = b"sys.addaudithook(audit)\n"
        assert changed[path].count(before) == 1
        changed[path] = changed[path].replace(before, b"", 1)
    elif mutation == "reversed_guard":
        before = b'assert not guard.check_repository(root, unit=unit)["ok"]'
        assert changed[path].count(before) == 1
        changed[path] = changed[path].replace(before, b'assert guard.check_repository(root, unit=unit)["ok"]', 1)
    elif mutation == "missing_file":
        del changed[path]
    elif mutation == "extra_file":
        changed["tests/contract/test_unreviewed_migration.py"] = b"assert True\n"
    else:
        changed[path] = git_bytes(path)
        assert changed[path] != original[path]
    if mutation in ("weakened_assertion", "removed_observer", "reversed_guard"):
        ast.parse(changed[path])  # Valid source whose assertions/effects check was weakened.
    with pytest.raises(AssertionError, match="^migration_source_(bytes|inventory)_changed"):
        assert_live_migration_bytes(changed)
    assert_live_migration_bytes(original)


def test_old_phase2_scopes_and_repair_meanings_are_unchanged():
    """Frozen P2 plan plus separately named historical repair authorizations."""
    raw = git_bytes("PHASE_2_PLAN.md")
    assert hashlib.sha256(raw).hexdigest() == "bea21992edf58b77cfe0f9a128bb31cee9226a9ea5e87b829663a47768227918"
    blocks = re.findall(r"^## \d+\. (P2-W0[1-9]):[^\n]*\n\n### Allowed paths\n\n```text\n(.*?)\n```", raw.decode(), re.M | re.S)
    original = {unit: frozenset(body.splitlines()) for unit, body in blocks}
    assert len(original) == 9
    repairs = {
        2: {"tests/security/test_scaffold_inertness.py", "tests/scaffold/test_ci_contract.py"},
        4: {PACKAGE + "contracts/execution.py", PACKAGE + "runtime/diagnostics.py",
            "tests/scaffold/test_ci_contract.py", "tests/contract/test_bundle_contract.py"},
        5: {"tests/unit/test_input_decoding.py", "tests/unit/test_value_capture.py", "tests/security/test_input_capture.py",
            "tests/scaffold/test_ci_contract.py", "phase2/transition_ledger.md", "tests/contract/test_input_schema_mapping.py"},
        7: {"phase2/module_policy.json", "tests/scaffold/test_ci_contract.py", "tests/contract/test_bundle_contract.py",
            "tests/security/test_input_capture.py", "tests/contract/test_input_schema_mapping.py", "phase2/transition_ledger.md"},
        8: {"phase2/module_policy.json", "tests/contract/test_bundle_contract.py", "tests/security/test_input_capture.py",
            "tests/contract/test_input_schema_mapping.py", "tests/contract/test_phase2_transition.py",
            "tests/security/test_preparation_inertness.py", "phase2/transition_ledger.md"},
        9: {"phase2/module_policy.json", "tests/scaffold/test_ci_contract.py", "tests/contract/test_bundle_contract.py",
            "tests/security/test_input_capture.py", "tests/contract/test_input_schema_mapping.py",
            "tests/contract/test_phase2_transition.py", "phase2/transition_ledger.md"},
    }
    ci = ci_driver()
    current = guard.plan_paths(ROOT)
    assert current == original
    cumulative = set()
    for step in range(1, 10):
        unit = f"P2-W{step:02}"
        expected = original[unit] | repairs.get(step, set())
        assert ci.effective_paths(current, unit) == expected
        ci.check_changed_paths(current, unit, expected)
        cumulative.update(expected)
        assert ci.effective_paths(current, unit, cumulative=True) == cumulative
        for path in COMMON | {"PHASE_3_PLAN.md", "phase3/entry_manifest.json", "tests/contract/test_phase3_transition.py"}:
            with pytest.raises(ValueError, match="^work_unit_allowlist_exceeded$"):
                ci.check_changed_paths(current, unit, expected | {path})
    with pytest.raises(ValueError):
        ci.effective_paths(current, "P3-W01")


@pytest.mark.parametrize("step", range(1, 16))
def test_exact_pr_and_single_main_footer_supply_phase3_context(step):
    ci = ci_driver()
    head, base = "a" * 40, "b" * 40
    unit = f"P3-W{step:02}"
    pr = {"pull_request": {"head": {"sha": head, "ref": f"phase3/p3-w{step:02}"}, "base": {"sha": base}},
          "active_unit": "P3-W15", "SIT_PHASE_UNIT": "P3-W15"}
    assert ci.resolve_unit("pull_request", pr, head) == (unit, base)
    main = {"ref": "refs/heads/main", "before": base,
            "head_commit": {"id": head, "message": "Accepted unit\n\nSIT-Phase-Unit: " + unit}}
    assert ci.resolve_unit("push", main, head) == (unit, base)
    with pytest.raises(ValueError):
        ci.resolve_unit("pull_request", pr, base)
    with pytest.raises(ValueError):
        ci.resolve_unit("push", main, base)


@pytest.mark.parametrize("branch", ("phase3/plan", "phase3/p3-w1", "phase3/p3-w00", "phase3/p3-w16",
    "phase4/p4-w01", "phase3/p3-w01; injected", "phase3/p3-w01\n", "phase3/p3-w01/extra"))
def test_unknown_future_or_nonexact_review_branches_are_rejected(branch):
    ci = ci_driver()
    head, base = "a" * 40, "b" * 40
    event = {"pull_request": {"head": {"sha": head, "ref": branch}, "base": {"sha": base}}}
    with pytest.raises(ValueError):
        ci.resolve_unit("pull_request", event, head)


@pytest.mark.parametrize("message", (
    "No work-unit footer", "SIT-Phase-Unit: P3-W00", "SIT-Phase-Unit: P3-W16",
    "SIT-Phase-Unit: P4-W01", "SIT-Phase-Unit: P3-W01\nSIT-Phase-Unit: P3-W01",
    "SIT-Phase-Unit: P3-W01\nSIT-Phase-Unit: P2-W09",
    "SIT-Phase-Unit: P3-W01\nSIT-Phase-Unit: P3-W99",
    "SIT-Phase-Unit: P3-W01 injected", "SIT-Phase-Unit: P3-W01 ",
))
def test_main_rejects_missing_unknown_duplicate_or_mixed_footers(message):
    ci = ci_driver()
    head, base = "a" * 40, "b" * 40
    event = {"ref": "refs/heads/main", "before": base, "head_commit": {"id": head, "message": message}}
    with pytest.raises(ValueError):
        ci.resolve_unit("push", event, head)


@pytest.mark.parametrize("mode", ("wrong_ref", "wrong_event", "invalid_base", "nonstring_base"))
def test_context_rejects_unsupported_events_refs_and_commit_identities(mode):
    ci = ci_driver()
    head, base = "a" * 40, "b" * 40
    event = {"ref": "refs/heads/main", "before": base,
             "head_commit": {"id": head, "message": "SIT-Phase-Unit: P3-W01"}}
    event_name = "push"
    if mode == "wrong_ref":
        event["ref"] = "refs/heads/phase3/p3-w01"
    elif mode == "wrong_event":
        event_name = "pull_request_target"
    elif mode == "invalid_base":
        event["before"] = "HEAD"
    else:
        event["before"] = None
    with pytest.raises(ValueError):
        ci.resolve_unit(event_name, event, head)


def test_entry_byte_checker_accepts_real_live_files_then_rejects_frozen_mutants():
    ci = ci_driver()
    entry = guard.phase3_entry_manifest(ROOT)
    unit = os.environ["SIT_PHASE_UNIT"]
    allowed = ci.phase3_effective_paths(guard.phase3_plan_paths(ROOT), unit, cumulative=True)
    # Include current regular artifacts while excluding unrelated scratch/cache files.
    names = set(entry["files"]) | {path for path in allowed if (ROOT / path).is_file()}
    actual = {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in names}
    ci.check_entry_bytes(entry["files"], actual, allowed)
    for path in ("phase2/module_policy.json", "phase2/transition_ledger.md", "PHASE_2_COMPLETION.md",
                 "requirements-dev.txt", "tests/fixtures/hero/H7-01.bundle.json"):
        changed = dict(actual)
        assert path in changed
        changed[path] = hashlib.sha256((ROOT / path).read_bytes() + b"\nMUTATION\n").hexdigest()
        with pytest.raises(ValueError):
            ci.check_entry_bytes(entry["files"], changed, allowed)
    missing = dict(actual)
    del missing["phase2/module_policy.json"]
    with pytest.raises(ValueError):
        ci.check_entry_bytes(entry["files"], missing, allowed)
    unknown = dict(actual, **{"phase3/approved_by_source.json": "0" * 64})
    with pytest.raises(ValueError):
        ci.check_entry_bytes(entry["files"], unknown, allowed)


def test_forbidden_intermediate_commit_cannot_be_hidden_by_restored_final_bytes(tmp_path):
    """Actual Git commits exercise the driver, including a clean positive chain."""
    ci = ci_driver()
    repo = tmp_path / "history"
    repo.mkdir()
    def git(*args):
        return subprocess.check_output(["git", "-c", "user.name=Synthetic Test", "-c", "user.email=synthetic@example.invalid",
            *args], cwd=repo, stderr=subprocess.PIPE, text=True, timeout=30).strip()
    def commit(message):
        git("add", "--all")
        git("commit", "-q", "-m", message)
        return git("rev-parse", "HEAD")
    git("init", "-q")
    # Synthetic entry bytes and archive bytes have one explicit local format;
    # inherited Windows Git settings must not alter this history counterexample.
    git("config", "--local", "core.autocrlf", "false")
    git("config", "--local", "core.eol", "lf")
    (repo / "fixed.txt").write_bytes(b"fixed entry\n")
    (repo / "allowed.txt").write_bytes(b"entry progress\n")
    initial = commit("Synthetic entry")
    entry_files = {name: hashlib.sha256(raw).hexdigest() for name, raw in (
        ("fixed.txt", b"fixed entry\n"), ("allowed.txt", b"entry progress\n"))}
    entry = {"intake_commit": initial, "files": entry_files}
    with patch.object(ci, "ROOT", repo):
        assert ci.commit_hashes(initial) == entry_files
    (repo / "allowed.txt").write_bytes(b"allowed progress\n")
    good = commit("Allowed unit progress")
    paths = {"P3-W01": frozenset({"allowed.txt"})}
    with patch.object(ci, "ROOT", repo):
        ci.phase3_history(entry, initial, good, paths, "P3-W01")
    (repo / "fixed.txt").write_bytes(b"forbidden temporary modification\n")
    commit("Unapproved intermediate change")
    (repo / "fixed.txt").write_bytes(b"fixed entry\n")
    restored = commit("Restore final fixed bytes")
    assert git("diff", "--name-only", initial, restored) == "allowed.txt"
    with patch.object(ci, "ROOT", repo):
        with pytest.raises(ValueError, match="^intermediate_work_unit_allowlist_exceeded$"):
            ci.phase3_history(entry, initial, restored, paths, "P3-W01")


@pytest.mark.parametrize("case", ("clean", "premature_then_restore", "wrong_footer", "duplicate_footer", "linear_predecessor"))
def test_later_unit_cannot_relabel_an_earlier_units_commit_scope(tmp_path, case):
    ci = ci_driver()
    repo = tmp_path / "two-unit-history"
    repo.mkdir()
    def git(*args):
        return subprocess.check_output(["git", "-c", "user.name=Synthetic Test", "-c", "user.email=synthetic@example.invalid",
            *args], cwd=repo, stderr=subprocess.PIPE, text=True, timeout=30).strip()
    def commit(message):
        git("add", "--all")
        git("commit", "-q", "-m", message)
        return git("rev-parse", "HEAD")
    git("init", "-q")
    git("config", "--local", "core.autocrlf", "false")
    git("config", "--local", "core.eol", "lf")
    for name in ("first.txt", "second.txt", "fixed.txt"):
        (repo / name).write_bytes(b"entry\n")
    initial = commit("Synthetic entry")
    main_branch = git("branch", "--show-current")
    entry = {"intake_commit": initial, "files": {
        name: hashlib.sha256(b"entry\n").hexdigest()
        for name in ("first.txt", "second.txt", "fixed.txt")}}
    with patch.object(ci, "ROOT", repo):
        assert ci.commit_hashes(initial) == entry["files"]
    git("checkout", "-q", "-b", "synthetic-w01")
    (repo / "first.txt").write_bytes(b"first-unit work\n")
    accepted_head = commit("Allowed first-unit work")
    if case == "premature_then_restore":
        (repo / "second.txt").write_bytes(b"premature second-unit work\n")
        commit("Second-unit path changed during first unit")
        (repo / "second.txt").write_bytes(b"entry\n")
        accepted_head = commit("Restore final second-unit bytes")
    if case == "linear_predecessor":
        base = accepted_head
    else:
        git("checkout", "-q", main_branch)
        footer = "SIT-Phase-Unit: P3-W02" if case == "wrong_footer" else "SIT-Phase-Unit: P3-W01"
        if case == "duplicate_footer":
            footer += "\nSIT-Phase-Unit: P3-W01"
        git("merge", "-q", "--no-ff", "synthetic-w01", "-m", "Accepted synthetic first unit\n\n" + footer)
        base = git("rev-parse", "HEAD")
    git("checkout", "-q", "-b", "synthetic-w02")
    (repo / "second.txt").write_bytes(b"authorized second-unit work\n")
    current = commit("Allowed second-unit work")
    paths = {"P3-W01": frozenset({"first.txt"}), "P3-W02": frozenset({"second.txt"})}
    assert git("diff", "--name-only", initial, base) == "first.txt"
    assert git("diff", "--name-only", base, current) == "second.txt"
    with patch.object(ci, "ROOT", repo):
        if case == "clean":
            history = ci.phase3_history(entry, base, current, paths, "P3-W02")
            assert {row["unit"] for row in history} == {"P3-W01", "P3-W02"}
            assert any(row["current_unit_segment"] for row in history)
            assert any(not row["current_unit_segment"] for row in history)
        else:
            expected = ("intermediate_work_unit_allowlist_exceeded" if case == "premature_then_restore" else
                        "invalid_accepted_merge_chain" if case == "linear_predecessor" else "wrong_phase3_predecessor")
            with pytest.raises(ValueError, match="^" + expected + "$"):
                ci.phase3_history(entry, base, current, paths, "P3-W02")
