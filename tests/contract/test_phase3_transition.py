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

# Independent owner-approved P3-W04-R01 literals, separate from plan scopes.
W04_R01_PATHS = frozenset((
    "tests/scaffold/test_no_runtime_implementation.py",
    "tests/scaffold/test_ci_contract.py",
    "tests/contract/test_phase3_transition.py",
    "phase3/transition_ledger.md",
))
W04_R01_BASE = "879b67b7066690ab0bee8cef569aa8869f78af03"
W04_R01_BASE_TREE = "f7c92b34537b8fc089c8624af9da6ec9dea74a68"
W04_R01_PREDECESSOR = "b932bef422b4ec67b1b313ecae51b0f7e48d72a2"
W04_R01_PROPOSAL_SHA256 = "32c4372d886d98280cb389bc8912610ec2628e3c477ac7057785e304001cf42f"

# Independently transcribed approved P3-W05-R01, separate from the raw plan.
W05_R01_PATHS = frozenset((
    "tests/scaffold/test_module_manifest.py",
    "tests/scaffold/test_ci_contract.py",
    "tests/contract/test_phase3_transition.py",
    "phase3/transition_ledger.md",
))
W05_R01_BASE = "a2aa2112231ba7595070216e659798130127dc3c"
W05_R01_BASE_TREE = "d468e02fa40a5014e838937486fa49185bc1e72d"
W05_R01_PREDECESSOR = "a175d6d4b4153ddc9147301f9db8d247d12e4852"
W05_R01_PROPOSAL_SHA256 = "ec1e54522b05f0b1a5b1340a4917ad4477017cdfe80218e91a90d75c990bec87"

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
    effective = expected | (W04_R01_PATHS if step == 4 else frozenset())
    if step == 5:
        effective |= W05_R01_PATHS
    assert ci.phase3_effective_paths(paths, unit) == effective
    ci.phase3_check_changed_paths(paths, unit, effective)
    cumulative = COMMON | frozenset().union(*(ADDITIONAL[number] for number in range(1, step + 1)))
    if step >= 4:
        cumulative |= W04_R01_PATHS
    if step >= 5:
        cumulative |= W05_R01_PATHS
    assert ci.phase3_effective_paths(paths, unit, cumulative=True) == cumulative
    assert len(COMMON) == 4
    for future_path in (COMMON | frozenset().union(*ADDITIONAL.values())) - effective:
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


def test_w04_r01_literal_authority_preserves_plan_guard_and_workflow():
    ci = ci_driver()
    assert ci.P3_W04_R01_PATHS == W04_R01_PATHS and len(W04_R01_PATHS) == 4
    assert ci.P3_W04_R01_BASE == W04_R01_BASE
    assert ci.P3_W04_R01_BASE_TREE == W04_R01_BASE_TREE
    assert ci.P3_W04_R01_PREDECESSOR == W04_R01_PREDECESSOR
    paths = guard.phase3_plan_paths(ROOT)
    assert len(paths["P3-W04"]) == 13
    assert len(ci.phase3_effective_paths(paths, "P3-W04")) == 17
    assert len(ci.phase3_effective_paths(paths, "P3-W01")) == 23
    # Original W01 permission already contains these paths; R01 gives no new
    # retrospective W01 permission and cannot enlarge raw plan parsing.
    assert W04_R01_PATHS <= paths["P3-W01"]
    assert not W04_R01_PATHS & paths["P3-W04"]
    for path, digest in (
        ("tools/check_scaffold_boundary.py", "fc9885337b4973a084c4c7326370a7962b898c14f6a0858e09ee6ccbeb97071a"),
        (".github/workflows/phase1-ci.yml", "841c39f7d3c596eafd767355a4a30f5111d6a73c8752229108708fcb39c4539e"),
        ("PHASE_3_PLAN.md", PLAN_SHA256),
        ("phase3/entry_manifest.json", "dfe96f57a222937131e8e4fafd13098f76d134cd88a50ffa9fa82891b9b9659b"),
    ):
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path


@pytest.mark.parametrize("step", range(1, 16))
def test_w04_r01_name_is_cumulative_but_immediate_permissions_are_not(step):
    ci = ci_driver()
    unit = f"P3-W{step:02}"
    paths = guard.phase3_plan_paths(ROOT)
    assert ci.phase3_scope_exceptions(unit) == ((["P3-W04-R01"] if step >= 4 else []) +
                                              (["P3-W05-R01"] if step >= 5 else []))
    for path in W04_R01_PATHS:
        # Three paths have a separate W05 approval. The W04 wrapper does not.
        if step in (1, 4) or (step == 5 and path in W05_R01_PATHS):
            ci.phase3_check_changed_paths(paths, unit, {path})
        else:
            with pytest.raises(ValueError, match="^work_unit_allowlist_exceeded$"):
                ci.phase3_check_changed_paths(paths, unit, {path})
    # All four were in W01 already; the cumulative union is still independently
    # determined by approved scopes, with no new caller/source metadata input.
    assert W04_R01_PATHS <= ci.phase3_effective_paths(paths, unit, cumulative=True)


@pytest.mark.parametrize("path", (
    "tests/scaffold/test_no_runtime_implementation.py.bak",
    "tests/scaffold/../scaffold/test_no_runtime_implementation.py",
    "tests/contract/test_phase2_transition.py", "phase2/transition_ledger.md",
    "tools/check_scaffold_boundary.py", ".github/workflows/phase1-ci.yml",
    "PHASE_3_PLAN.md", "src/source_integrity_toolkit/api.py",
))
def test_w04_r01_cannot_authorize_lookalikes_or_other_frozen_paths(path):
    ci = ci_driver()
    paths = guard.phase3_plan_paths(ROOT)
    allowed = COMMON | ADDITIONAL[4] | W04_R01_PATHS
    with pytest.raises(ValueError, match="^work_unit_allowlist_exceeded$"):
        ci.phase3_check_changed_paths(paths, "P3-W04", allowed | {path})


def test_w04_r01_driver_keeps_original_p2_and_unrelated_ci_ast():
    path = "tests/scaffold/test_ci_contract.py"
    before_raw = git_bytes(path, W04_R01_BASE)
    assert hashlib.sha256(before_raw).hexdigest() == "f9936064805bf820bdb8ce12954f8b7389ac6ce67328ad802c4cd137524503b6"
    # Keep the original W04 proof on its actual accepted bytes, then check the
    # current driver independently against that fixed witness. No old code runs.
    accepted_raw = git_bytes(path, W05_R01_PREDECESSOR)
    assert hashlib.sha256(accepted_raw).hexdigest() == "18b1db14373ace5523062f41e48977d5b170c5b238b3a04c65bd42e11a03e6a4"
    before, after = ast.parse(before_raw), ast.parse(accepted_raw)
    changed = {"phase3_effective_paths", "phase3_history", "phase3_entry_and_scope"}
    additions = {"P3_W04_R01_PATHS", "P3_W04_R01_BASE", "P3_W04_R01_BASE_TREE",
                 "P3_W04_R01_PREDECESSOR", "phase3_scope_exceptions", "phase3_w04_pre_amendment"}
    def name(node):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            return node.name
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            return node.targets[0].id
        return None
    assert [ast.dump(n) for n in before.body if name(n) not in changed] == [
        ast.dump(n) for n in after.body if name(n) not in changed | additions]
    for expected in changed | additions:
        assert sum(name(n) == expected for n in after.body) == 1, expected
    _assert_w05_r01_driver_source((ROOT / path).read_bytes())


_W04_MIGRATED_METHODS = (
    "test_syntax_error_and_oversize_do_not_crash_guard",
    "test_real_guard_cli_is_not_removed_by_python_optimization",
)


def _assert_w04_r01_migrated_source(raw):
    """Independent old-source oracle permits only two documented substitutions."""
    path = "tests/scaffold/test_no_runtime_implementation.py"
    wrapper = git_bytes(path, W04_R01_BASE)
    assert hashlib.sha256(wrapper).hexdigest() == "aa670dc29ac290f9b68b056a580851eca57bc93e7ed899e84a0136d2e6af45f8"
    historical = git_bytes(path, "eb730dda31d189c8487b5247a45bae47b678821b")
    assert hashlib.sha256(historical).hexdigest() == "c7becbd11aa199b9299ca5fac7d205c1427d1b246bc777b18a15480eefd667f0"
    before, after = ast.parse(wrapper), ast.parse(raw)
    prefix = before.body[:-1]
    assert [ast.dump(n) for n in after.body[:len(prefix)]] == [ast.dump(n) for n in prefix], "original_adapter_changed"
    assert ast.dump(after.body[-1]) == ast.dump(before.body[-1]), "original_main_footer_changed"
    original_class = next(n for n in ast.parse(historical).body
                          if isinstance(n, ast.ClassDef) and n.name == "NoRuntimeImplementationTests")
    statements = [ast.dump(n) for n in after.body]
    for method in _W04_MIGRATED_METHODS:
        old = next(n for n in original_class.body if isinstance(n, ast.FunctionDef) and n.name == method)
        expected = copy.deepcopy(old)
        expected.name = "_current_" + method
        substitutions = 0
        for node in ast.walk(expected):
            if isinstance(node, ast.Constant) and node.value == "graph/cycles.py":
                node.value = "reporting/json_report.py"
                substitutions += 1
        assert substitutions == 1
        replacements = [n for n in after.body if isinstance(n, ast.FunctionDef) and n.name == expected.name]
        assert len(replacements) == 1 and ast.dump(replacements[0]) == ast.dump(expected), "migrated_method_assertions_changed"
        for statement in (
            f"_phase1_{method} = NoRuntimeImplementationTests.{method}",
            f"NoRuntimeImplementationTests.{method} = _current_{method}",
        ):
            assert statements.count(ast.dump(ast.parse(statement).body[0])) == 1, "method_identity_binding_changed"


def test_w04_r01_two_live_methods_preserve_all_original_assertions_and_bindings():
    path = ROOT / "tests/scaffold/test_no_runtime_implementation.py"
    _assert_w04_r01_migrated_source(path.read_bytes())
    spec = importlib.util.spec_from_file_location("sit_w04_r01_live_guard_adapter", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    for method in _W04_MIGRATED_METHODS:
        live = getattr(module.NoRuntimeImplementationTests, method)
        assert live is getattr(module, "_current_" + method)
        original = getattr(module, "_phase1_" + method)
        assert original is not live and original.__name__ == method
        assert "graph/cycles.py" in original.__code__.co_consts
        assert "reporting/json_report.py" in live.__code__.co_consts
    assert "reporting/json_report.py" in PERMANENT_INERT
    for step in range(1, 16):
        assert "reporting/json_report.py" not in guard.phase3_policy_promotions(policy_for(step), f"P3-W{step:02}")


@pytest.mark.parametrize("mutation", (
    "removed_negative_assertion", "changed_exit_code", "removed_optimization_flag",
    "restored_stale_target", "relaxed_oversize", "historical_snapshot",
    "missing_method_binding", "removed_historical_loader",
))
def test_w04_r01_migration_oracle_rejects_each_weakened_source(mutation):
    path = "tests/scaffold/test_no_runtime_implementation.py"
    raw = (ROOT / path).read_bytes()
    _assert_w04_r01_migrated_source(raw)
    tree = ast.parse(raw)
    syntax = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
                  and n.name == "_current_" + _W04_MIGRATED_METHODS[0])
    cli = next(n for n in tree.body if isinstance(n, ast.FunctionDef)
               and n.name == "_current_" + _W04_MIGRATED_METHODS[1])
    if mutation == "removed_negative_assertion":
        cli.body.pop()
    elif mutation == "changed_exit_code":
        call = next(n for n in ast.walk(cli) if isinstance(n, ast.Call)
                    and isinstance(n.func, ast.Attribute) and n.func.attr == "assertEqual"
                    and ast.unparse(n.args[0]) == "negative.returncode")
        call.args[1] = ast.Constant(value=0)
    elif mutation == "removed_optimization_flag":
        command = cli.body[0].value
        command.elts = [n for n in command.elts if not (isinstance(n, ast.Constant) and n.value == "-O")]
    elif mutation == "restored_stale_target":
        for node in ast.walk(cli):
            if isinstance(node, ast.Constant) and node.value == "reporting/json_report.py":
                node.value = "graph/cycles.py"
    elif mutation == "relaxed_oversize":
        next(n for n in ast.walk(syntax) if isinstance(n, ast.Constant) and n.value == 20000).value = 262145
    elif mutation == "missing_method_binding":
        target = "NoRuntimeImplementationTests." + _W04_MIGRATED_METHODS[1]
        tree.body = [n for n in tree.body if not (isinstance(n, ast.Assign) and ast.unparse(n.targets[0]) == target)]
    elif mutation == "removed_historical_loader":
        tree.body = [n for n in tree.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
                     and isinstance(n.value.func, ast.Attribute) and n.value.func.attr == "load_phase1_test")]
    candidate = git_bytes(path, W04_R01_BASE) if mutation == "historical_snapshot" else ast.unparse(tree)
    with pytest.raises(AssertionError):
        _assert_w04_r01_migrated_source(candidate)


def test_w04_r01_ledger_is_append_only_and_records_actual_approval():
    path = "phase3/transition_ledger.md"
    before = git_bytes(path, W04_R01_BASE)
    assert hashlib.sha256(before).hexdigest() == "1177564fbc2296e50cddaf4b9b484447039f5b7424fcdb47de22a642ac6d0e59"
    after = (ROOT / path).read_bytes()
    assert after.startswith(before) and len(after) > len(before)
    addition = after[len(before):].decode()
    for marker in ("批准 **P3-W04-R01**", W04_R01_BASE, W04_R01_PROPOSAL_SHA256,
                   "reporting/json_report.py", "35596533702", *_W04_MIGRATED_METHODS, *sorted(W04_R01_PATHS)):
        assert marker in addition, marker
    assert len(guard.phase3_historical_nodes(ROOT)) == 1650


def test_w04_r01_actual_pre_amendment_history_uses_only_original_scope():
    ci = ci_driver()
    paths = guard.phase3_plan_paths(ROOT)
    entry = guard.phase3_entry_manifest(ROOT)
    history = ci.phase3_history(entry, W04_R01_PREDECESSOR, W04_R01_BASE, paths, "P3-W04")
    w04 = [row for row in history if row["unit"] == "P3-W04"]
    assert len(w04) == 1 and w04[0]["commit"] == W04_R01_BASE
    assert w04[0]["tree"] == W04_R01_BASE_TREE
    assert set(w04[0]["changed_paths"]) == COMMON | ADDITIONAL[4]
    assert w04[0]["immediate_scope_exceptions"] == []
    assert {row["unit"] for row in history} == {"P3-W01", "P3-W02", "P3-W03", "P3-W04"}


@pytest.mark.parametrize("case", (
    "clean", "pre_boundary_repair", "earlier_unit_then_restore", "post_boundary_forbidden_then_restore",
    "unanchored_side_branch", "wrong_boundary_tree", "wrong_boundary_parent", "missing_boundary_ancestry",
))
def test_w04_r01_boundary_and_complete_history_reject_unauthorized_edits(tmp_path, case):
    ci = ci_driver()
    repo = tmp_path / "four-unit-history"
    repo.mkdir()
    def git(*args):
        return subprocess.check_output(["git", "-c", "user.name=Synthetic Test",
            "-c", "user.email=synthetic@example.invalid", *args], cwd=repo,
            stderr=subprocess.PIPE, text=True, timeout=30).strip()
    def commit(message):
        git("add", "--all")
        git("commit", "-q", "-m", message)
        return git("rev-parse", "HEAD")
    git("init", "-q")
    git("config", "--local", "core.autocrlf", "false")
    git("config", "--local", "core.eol", "lf")
    repair = "tests/scaffold/test_no_runtime_implementation.py"
    names = ("one.txt", "two.txt", "three.txt", "four.txt", "side.txt", "fixed.txt", repair)
    for name in names:
        target = repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"entry\n")
    initial = commit("Synthetic planning entry")
    main = git("branch", "--show-current")
    entry = {"intake_commit": initial, "files": {name: hashlib.sha256(b"entry\n").hexdigest() for name in names}}
    paths = {"P3-W01": frozenset({"one.txt", repair}), "P3-W02": frozenset({"two.txt"}),
             "P3-W03": frozenset({"three.txt"}), "P3-W04": frozenset({"four.txt", "side.txt"})}
    for step, name in ((1, "one.txt"), (2, "two.txt"), (3, "three.txt")):
        branch = f"synthetic-w{step:02}"
        git("checkout", "-q", "-b", branch)
        (repo / name).write_bytes(b"authorized unit bytes\n")
        commit("Original unit work")
        if step == 3 and case == "earlier_unit_then_restore":
            (repo / repair).write_bytes(b"premature repair\n")
            commit("Unapproved old-unit repair")
            (repo / repair).write_bytes(b"entry\n")
            commit("Restore old-unit final bytes")
        git("checkout", "-q", main)
        git("merge", "-q", "--no-ff", branch, "-m", f"Accepted synthetic unit\n\nSIT-Phase-Unit: P3-W{step:02}")
    predecessor = git("rev-parse", "HEAD")
    git("checkout", "-q", "-b", "synthetic-w04")
    (repo / "four.txt").write_bytes(b"original W04 work\n")
    if case == "pre_boundary_repair":
        (repo / repair).write_bytes(b"unapproved before boundary\n")
    boundary = commit("Fixed pre-amendment W04 head")
    boundary_tree = git("rev-parse", boundary + "^{tree}")
    if case == "unanchored_side_branch":
        git("checkout", "-q", "-b", "unanchored", predecessor)
        (repo / "side.txt").write_bytes(b"otherwise allowed side work\n")
        commit("W04 branch outside fixed boundary ancestry")
        git("checkout", "-q", "synthetic-w04")
        git("merge", "-q", "--no-ff", "unanchored", "-m", "Merge unanchored work")
    (repo / repair).write_bytes(b"approved narrow successor repair\n")
    current = commit("Owner-authorized R01 successor")
    if case == "post_boundary_forbidden_then_restore":
        (repo / "fixed.txt").write_bytes(b"forbidden mutation\n")
        commit("Out-of-scope intermediate successor")
        (repo / "fixed.txt").write_bytes(b"entry\n")
        current = commit("Restore final protected bytes")
    if case == "missing_boundary_ancestry":
        current = predecessor
    if case == "wrong_boundary_tree":
        boundary_tree = "0" * 40
    if case == "wrong_boundary_parent":
        git("checkout", "-q", "synthetic-w04")
        (repo / "four.txt").write_bytes(b"later W04 boundary candidate\n")
        boundary = commit("Cannot replace the fixed entry-parent boundary")
        boundary_tree = git("rev-parse", boundary + "^{tree}")
        current = boundary
    with patch.object(ci, "ROOT", repo), patch.object(ci, "P3_W04_R01_BASE", boundary), \
            patch.object(ci, "P3_W04_R01_BASE_TREE", boundary_tree), \
            patch.object(ci, "P3_W04_R01_PREDECESSOR", predecessor):
        assert ci.commit_hashes(initial) == entry["files"]
        if case == "clean":
            history = ci.phase3_history(entry, predecessor, current, paths, "P3-W04")
            assert {row["commit"] for row in history} == set(git("rev-list", initial + ".." + current).splitlines())
            original = next(row for row in history if row["commit"] == boundary)
            amended = next(row for row in history if row["commit"] == current)
            assert original["immediate_scope_exceptions"] == []
            assert amended["immediate_scope_exceptions"] == ["P3-W04-R01"]
            assert amended["changed_paths"] == [repair]
        else:
            reason = {
                "pre_boundary_repair": "intermediate_work_unit_allowlist_exceeded",
                "earlier_unit_then_restore": "intermediate_work_unit_allowlist_exceeded",
                "post_boundary_forbidden_then_restore": "intermediate_work_unit_allowlist_exceeded",
                "unanchored_side_branch": "entry_or_predecessor_ancestry_mismatch",
                "wrong_boundary_tree": "w04_repair_boundary_tree_mismatch",
                "wrong_boundary_parent": "w04_repair_boundary_parent_mismatch",
                "missing_boundary_ancestry": "entry_or_predecessor_ancestry_mismatch",
            }[case]
            with pytest.raises(ValueError, match="^" + reason + "$"):
                ci.phase3_history(entry, predecessor, current, paths, "P3-W04")


def _assert_w05_r01_driver_source(raw):
    """Allow only the named W05 driver additions beside the actual W04 AST."""
    before_raw = git_bytes("tests/scaffold/test_ci_contract.py", W05_R01_PREDECESSOR)
    assert hashlib.sha256(before_raw).hexdigest() == "18b1db14373ace5523062f41e48977d5b170c5b238b3a04c65bd42e11a03e6a4"
    before, after = ast.parse(before_raw), ast.parse(raw)
    changed = {"phase3_effective_paths", "phase3_scope_exceptions", "phase3_history"}
    additions = {"P3_W05_R01_PATHS", "P3_W05_R01_BASE", "P3_W05_R01_BASE_TREE",
                 "P3_W05_R01_PREDECESSOR", "phase3_w05_pre_amendment"}
    def name(node):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            return node.name
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            return node.targets[0].id
        return None
    assert [ast.dump(n) for n in before.body if name(n) not in changed] == [
        ast.dump(n) for n in after.body if name(n) not in changed | additions], "unrelated_ci_ast_changed"
    for expected in changed | additions:
        assert sum(name(n) == expected for n in after.body) == 1, "missing_or_duplicate_repair_definition"
    # Names alone cannot authorize caller-selected constants.
    constants = {n.targets[0].id: n.value for n in after.body if isinstance(n, ast.Assign)
                 and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)}
    for name, expected in (("P3_W05_R01_BASE", W05_R01_BASE),
                           ("P3_W05_R01_BASE_TREE", W05_R01_BASE_TREE),
                           ("P3_W05_R01_PREDECESSOR", W05_R01_PREDECESSOR)):
        assert ast.literal_eval(constants[name]) == expected, "fixed_w05_boundary_changed"
    actual = constants["P3_W05_R01_PATHS"]
    assert isinstance(actual, ast.Call) and isinstance(actual.func, ast.Name)
    assert actual.func.id == "frozenset" and len(actual.args) == 1 and not actual.keywords
    rows = ast.literal_eval(actual.args[0])
    assert type(rows) is tuple and len(rows) == len(set(rows)) == 4 and set(rows) == W05_R01_PATHS


def test_w05_r01_exact_authority_preserves_plan_and_other_unit_scopes():
    ci = ci_driver()
    assert ci.P3_W05_R01_PATHS == W05_R01_PATHS
    assert ci.P3_W05_R01_BASE == W05_R01_BASE
    assert ci.P3_W05_R01_BASE_TREE == W05_R01_BASE_TREE
    assert ci.P3_W05_R01_PREDECESSOR == W05_R01_PREDECESSOR
    _assert_w05_r01_driver_source((ROOT / "tests/scaffold/test_ci_contract.py").read_bytes())
    paths = guard.phase3_plan_paths(ROOT)
    assert paths["P3-W05"] == COMMON | ADDITIONAL[5] and len(paths["P3-W05"]) == 9
    assert len(ci.phase3_effective_paths(paths, "P3-W05")) == 13
    assert W05_R01_PATHS <= paths["P3-W01"] and not W05_R01_PATHS & paths["P3-W05"]
    assert W05_R01_PATHS - W04_R01_PATHS == {"tests/scaffold/test_module_manifest.py"}
    assert W04_R01_PATHS - W05_R01_PATHS == {"tests/scaffold/test_no_runtime_implementation.py"}
    for path, digest in (
        ("tools/check_scaffold_boundary.py", "fc9885337b4973a084c4c7326370a7962b898c14f6a0858e09ee6ccbeb97071a"),
        (".github/workflows/phase1-ci.yml", "841c39f7d3c596eafd767355a4a30f5111d6a73c8752229108708fcb39c4539e"),
        ("PHASE_3_PLAN.md", PLAN_SHA256),
        ("phase3/entry_manifest.json", "dfe96f57a222937131e8e4fafd13098f76d134cd88a50ffa9fa82891b9b9659b"),
    ):
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == digest, path
    assert_live_migration_bytes({p: (ROOT / p).read_bytes() for p in LIVE_MIGRATION_SHA256})


@pytest.mark.parametrize("step", range(1, 16))
def test_w05_r01_cumulative_name_never_grants_later_immediate_rights(step):
    ci = ci_driver()
    paths = guard.phase3_plan_paths(ROOT)
    unit = f"P3-W{step:02}"
    expected = COMMON | ADDITIONAL[step]
    if step == 4:
        expected |= W04_R01_PATHS
    if step == 5:
        expected |= W05_R01_PATHS
    assert ci.phase3_effective_paths(paths, unit) == expected
    assert ci.phase3_scope_exceptions(unit) == ((["P3-W04-R01"] if step >= 4 else []) +
                                              (["P3-W05-R01"] if step >= 5 else []))
    ci.phase3_check_changed_paths(paths, unit, expected)
    for path in (W05_R01_PATHS | W04_R01_PATHS) - expected:
        with pytest.raises(ValueError, match="^work_unit_allowlist_exceeded$"):
            ci.phase3_check_changed_paths(paths, unit, expected | {path})
    # These paths have been cumulative since W01. That never enlarges a later
    # immediate scope, including W06 after the new repair is in its history.
    assert W05_R01_PATHS <= ci.phase3_effective_paths(paths, unit, cumulative=True)


@pytest.mark.parametrize("path", (
    "tests/scaffold/test_module_manifest.py.bak", "tests/scaffold/../scaffold/test_module_manifest.py",
    "tests/scaffold/test_no_runtime_implementation.py", "tests/scaffold/test_imports.py",
    "tests/contract/test_phase2_transition.py", "tests/security/test_preparation_inertness.py",
    "phase2/transition_ledger.md", "tools/check_scaffold_boundary.py",
    ".github/workflows/phase1-ci.yml", "PHASE_3_PLAN.md", PACKAGE + "graph/projections.py",
))
def test_w05_r01_rejects_other_old_paths_and_lookalikes(path):
    ci = ci_driver()
    with pytest.raises(ValueError, match="^work_unit_allowlist_exceeded$"):
        ci.phase3_check_changed_paths(guard.phase3_plan_paths(ROOT), "P3-W05",
                                     COMMON | ADDITIONAL[5] | W05_R01_PATHS | {path})


@pytest.mark.parametrize("mutation", ("p2_body", "w04_boundary", "context_resolution", "extra_constant",
                                      "missing_w05_boundary", "candidate_selected_boundary"))
def test_w05_r01_driver_oracle_rejects_unrelated_or_self_selected_changes(mutation):
    raw = (ROOT / "tests/scaffold/test_ci_contract.py").read_bytes()
    _assert_w05_r01_driver_source(raw)
    tree = ast.parse(raw)
    if mutation in ("p2_body", "w04_boundary", "context_resolution"):
        name = {"p2_body": "effective_paths", "w04_boundary": "phase3_w04_pre_amendment",
                "context_resolution": "resolve_unit"}[mutation]
        next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name).body = [ast.Return(value=ast.Constant(None))]
    elif mutation == "extra_constant":
        tree.body.append(ast.parse("SOURCE_APPROVED_PATHS = {'arbitrary.py'}").body[0])
    elif mutation == "missing_w05_boundary":
        tree.body = [n for n in tree.body if not (isinstance(n, ast.FunctionDef) and n.name == "phase3_w05_pre_amendment")]
    else:
        assignment = next(n for n in tree.body if isinstance(n, ast.Assign)
                          and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "P3_W05_R01_BASE")
        assignment.value = ast.Constant("0" * 40)
    with pytest.raises(AssertionError):
        _assert_w05_r01_driver_source(ast.unparse(tree))


def _w05_portable_ast_dump(node):
    """Keep the reviewed empty-list representation across CPython versions."""
    tree = copy.deepcopy(node)
    for child in ast.walk(tree):
        if getattr(child, "type_params", None) == []:
            child._fields = tuple(field for field in child._fields if field != "type_params")
    # CPython 3.13 defaults to omitting empty lists; the reviewed pin includes
    # them. Keep every other field, including nonempty generic parameters.
    if sys.version_info >= (3, 13):
        return ast.dump(tree, show_empty=True)
    return ast.dump(tree)


def test_w05_r01_portable_ast_preserves_explicit_empty_lists():
    node = ast.parse("def f():\n    return g()\n").body[0]
    original = ast.dump(node, include_attributes=True)
    assert _w05_portable_ast_dump(node) == (
        "FunctionDef(name='f', args=arguments(posonlyargs=[], args=[], "
        "kwonlyargs=[], kw_defaults=[], defaults=[]), body=[Return(value="
        "Call(func=Name(id='g', ctx=Load()), args=[], keywords=[]))], "
        "decorator_list=[])"
    )
    assert ast.dump(node, include_attributes=True) == original


@pytest.mark.parametrize("source", (
    "def f(x):\n    return g()\n",
    "def f():\n    return h()\n",
    "def f():\n    return g(1)\n",
    "def f():\n    return g(flag=True)\n",
    "@decorator\ndef f():\n    return g()\n",
    "def f():\n    g()\n",
))
def test_w05_r01_portable_ast_keeps_semantic_differences(source):
    baseline = ast.parse("def f():\n    return g()\n").body[0]
    expected = _w05_portable_ast_dump(baseline)
    reformatted = ast.parse("def f( ):\n    return (g( ))\n").body[0]
    assert _w05_portable_ast_dump(reformatted) == expected
    assert _w05_portable_ast_dump(ast.parse(source).body[0]) != expected
    assert _w05_portable_ast_dump(baseline) == expected


def test_w05_r01_portable_ast_only_normalizes_empty_generic_parameters():
    baseline = ast.parse("def f():\n    return g()\n").body[0]
    expected = _w05_portable_ast_dump(baseline)
    generic = copy.deepcopy(baseline)
    generic._fields = tuple(field for field in generic._fields if field != "type_params") + ("type_params",)
    generic.type_params = []
    assert _w05_portable_ast_dump(generic) == expected
    generic.type_params = [ast.Name(id="T", ctx=ast.Load())]
    assert _w05_portable_ast_dump(generic) != expected
    assert _w05_portable_ast_dump(baseline) == expected


def _assert_w05_r01_migrated_source(raw):
    """Actual P1 method plus exactly one permanent-slot substitution."""
    path = "tests/scaffold/test_module_manifest.py"
    wrapper = git_bytes(path, W05_R01_PREDECESSOR)
    historical = git_bytes(path, "eb730dda31d189c8487b5247a45bae47b678821b")
    assert hashlib.sha256(wrapper).hexdigest() == "21e9737638d822c53e71607972bd9b6a7f1fd757f3d7c3a762e6f40c377f8f96"
    assert hashlib.sha256(historical).hexdigest() == "7b4062ac0fe2cbf8ce931f472dd22ca7a9c0fe802cdf14bfc69407bb47897f96"
    before, after = ast.parse(wrapper), ast.parse(raw)
    prefix = before.body[:-1]
    assert [ast.dump(n) for n in after.body[:len(prefix)]] == [ast.dump(n) for n in prefix], "manifest_verifier_or_loader_changed"
    assert ast.dump(after.body[-1]) == ast.dump(before.body[-1]), "manifest_main_footer_changed"
    name = "test_mutated_product_bytes_are_rejected"
    original_class = next(n for n in ast.parse(historical).body
                          if isinstance(n, ast.ClassDef) and n.name == "ModuleManifestTests")
    original = next(n for n in original_class.body if isinstance(n, ast.FunctionDef) and n.name == name)
    expected = copy.deepcopy(original)
    expected.name = "_current_" + name
    substitutions = 0
    for node in ast.walk(expected):
        if isinstance(node, ast.Constant) and node.value == "analysis/origins.py":
            node.value = "reporting/json_report.py"
            substitutions += 1
    assert substitutions == 1
    replacements = [n for n in after.body if isinstance(n, ast.FunctionDef) and n.name == expected.name]
    assert len(replacements) == 1 and ast.dump(replacements[0]) == ast.dump(expected), "manifest_method_assertions_changed"
    saved = ast.parse(f"_phase1_{name} = ModuleManifestTests.{name}").body[0]
    bound = ast.parse(f"ModuleManifestTests.{name} = _current_{name}").body[0]
    middle = after.body[len(prefix):-1]
    controls = [n for n in middle if isinstance(n, ast.ClassDef) and n.name == "LiveModuleManifestTests"]
    assert len(controls) == 1, "live_manifest_observers_missing"
    # Reviewed explicit live positives, effects, owner checks and postpositives.
    # This external-source pin adds no path permission and changes no old pin.
    assert hashlib.sha256(_w05_portable_ast_dump(controls[0]).encode()).hexdigest() == \
        "615ffa1cda025db7c9bf9d44d070492936aa4a3708d544ae54c074c39ed44563", "live_manifest_observers_changed"
    assert [ast.dump(n) for n in middle] == [ast.dump(n) for n in (saved, expected, bound, controls[0])], "manifest_method_binding_or_extra_code_changed"


def test_w05_r01_method_and_live_observers_preserve_original_identity():
    path = ROOT / "tests/scaffold/test_module_manifest.py"
    raw = path.read_bytes()
    _assert_w05_r01_migrated_source(raw)
    # Formatting changes cannot by themselves make a counterexample fail.
    _assert_w05_r01_migrated_source(ast.unparse(ast.parse(raw)))
    before = git_bytes("tests/scaffold/test_module_manifest.py", W05_R01_PREDECESSOR)
    footer = b'if __name__ == "__main__":\n    unittest.main()\n'
    assert before.endswith(footer) and raw.startswith(before[:-len(footer)]) and raw.endswith(footer)
    spec = importlib.util.spec_from_file_location("sit_w05_r01_live_manifest", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    name = "test_mutated_product_bytes_are_rejected"
    live = getattr(module.ModuleManifestTests, name)
    original = getattr(module, "_phase1_" + name)
    assert live is getattr(module, "_current_" + name) and original is not live
    assert original.__name__ == name and "analysis/origins.py" in original.__code__.co_consts
    assert "reporting/json_report.py" in live.__code__.co_consts
    assert not issubclass(module.LiveModuleManifestTests, module.ModuleManifestTests)
    assert {name for name in vars(module.LiveModuleManifestTests) if name.startswith("test_")} == {
        "test_inventory_live_body_and_effect", "test_origins_live_body_and_effect",
        "test_inventory_owner_annotation", "test_origins_owner_annotation",
        "test_unchanged_baseline_keeps_all_module_and_owner_rows",
    }
    for step in range(1, 16):
        assert "reporting/json_report.py" not in guard.phase3_policy_promotions(policy_for(step), f"P3-W{step:02}")


@pytest.mark.parametrize("mutation", (
    "removed_assertion", "generic_exception", "changed_payload", "changed_verifier_call", "stale_target",
    "missing_binding", "missing_original", "reordered_binding", "missing_loader", "verifier_weakened",
    "missing_live_class", "missing_effect_observer", "weakened_owner_observer", "missing_legal_positive",
    "missing_postpositive", "duplicate_old_tests", "historical_snapshot",
))
def test_w05_r01_manifest_oracle_rejects_weakened_assertions_and_observers(mutation):
    path = "tests/scaffold/test_module_manifest.py"
    raw = (ROOT / path).read_bytes()
    _assert_w05_r01_migrated_source(raw)
    tree = ast.parse(raw)
    name = "test_mutated_product_bytes_are_rejected"
    method = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "_current_" + name)
    controls = next(n for n in tree.body if isinstance(n, ast.ClassDef) and n.name == "LiveModuleManifestTests")
    if mutation == "removed_assertion":
        method.body[-1] = ast.Pass()
    elif mutation == "generic_exception":
        next(n for n in ast.walk(method) if isinstance(n, ast.Name) and n.id == "AssertionError").id = "Exception"
    elif mutation == "changed_payload":
        next(n for n in ast.walk(method) if isinstance(n, ast.Constant) and isinstance(n.value, bytes)).value = b"\npass\n"
    elif mutation == "changed_verifier_call":
        next(n for n in ast.walk(method) if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
             and n.func.id == "verify_manifest").args[1] = ast.Attribute(value=ast.Name(id="self", ctx=ast.Load()), attr="files", ctx=ast.Load())
    elif mutation == "stale_target":
        next(n for n in ast.walk(method) if isinstance(n, ast.Constant) and n.value == "reporting/json_report.py").value = "analysis/origins.py"
    elif mutation in ("missing_binding", "missing_original", "reordered_binding"):
        target = "ModuleManifestTests." + name if mutation != "missing_original" else "_phase1_" + name
        statement = next(n for n in tree.body if isinstance(n, ast.Assign) and ast.unparse(n.targets[0]) == target)
        tree.body.remove(statement)
        if mutation == "reordered_binding":
            tree.body.insert(tree.body.index(method), statement)
    elif mutation == "missing_loader":
        tree.body = [n for n in tree.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
                     and isinstance(n.value.func, ast.Attribute) and n.value.func.attr == "load_phase1_test")]
    elif mutation == "verifier_weakened":
        next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "verify_manifest").body = [ast.Pass()]
    elif mutation == "missing_live_class":
        tree.body.remove(controls)
    elif mutation == "missing_effect_observer":
        controls.body = [n for n in controls.body if not (isinstance(n, ast.FunctionDef) and n.name == "_assert_live_effect_control")]
    elif mutation == "weakened_owner_observer":
        owner = next(n for n in controls.body if isinstance(n, ast.FunctionDef) and n.name == "_assert_live_owner_control")
        owner.body = [n for n in owner.body if not isinstance(n, ast.With)]
    elif mutation in ("missing_legal_positive", "missing_postpositive"):
        effect = next(n for n in controls.body if isinstance(n, ast.FunctionDef) and n.name == "_assert_live_effect_control")
        if mutation == "missing_postpositive":
            effect.body.pop()
        else:
            effect.body = [n for n in effect.body if not (isinstance(n, ast.Expr) and isinstance(n.value, ast.Call)
                           and isinstance(n.value.func, ast.Name) and n.value.func.id == "verify_manifest"
                           and isinstance(n.value.args[1], ast.Name) and n.value.args[1].id == "legal")]
    elif mutation == "duplicate_old_tests":
        controls.bases = [ast.Name(id="ModuleManifestTests", ctx=ast.Load())]
    candidate = git_bytes(path, W05_R01_PREDECESSOR) if mutation == "historical_snapshot" else ast.unparse(tree)
    with pytest.raises(AssertionError):
        _assert_w05_r01_migrated_source(candidate)


def test_w05_r01_ledger_is_append_only_and_approval_precedes_adaptation():
    path = "phase3/transition_ledger.md"
    before = git_bytes(path, W05_R01_BASE)
    assert hashlib.sha256(before).hexdigest() == "9e2b1f212f4e6b561860588cff3631e5e4b37cd83aab62be7eb59a4aeca0597d"
    after = (ROOT / path).read_bytes()
    assert after.startswith(before) and len(after) > len(before)
    addition = after[len(before):].decode()
    for marker in ("批准 **P3-W05-R01**", W05_R01_BASE, W05_R01_BASE_TREE, W05_R01_PREDECESSOR,
                   W05_R01_PROPOSAL_SHA256, "ab0bde2117b05dc4cf39a8c84e556c87a1c1a4d08a55db483b98ac506105e9b2",
                   "test_mutated_product_bytes_are_rejected", "reporting/json_report.py", *sorted(W05_R01_PATHS)):
        assert marker in addition, marker
    assert len(guard.phase3_historical_nodes(ROOT)) == 1650


def test_w05_r01_actual_boundary_keeps_original_scope_and_complete_w04_history():
    ci = ci_driver()
    paths = guard.phase3_plan_paths(ROOT)
    entry = guard.phase3_entry_manifest(ROOT)
    assert ci.git_text("rev-parse", W05_R01_BASE + "^{tree}") == W05_R01_BASE_TREE
    assert ci.git_text("show", "-s", "--format=%P", W05_R01_BASE).split() == [W05_R01_PREDECESSOR]
    assert ci.phase3_w05_pre_amendment(W05_R01_PREDECESSOR, W05_R01_BASE) == {W05_R01_BASE}
    history = ci.phase3_history(entry, W05_R01_PREDECESSOR, W05_R01_BASE, paths, "P3-W05")
    assert {row["commit"] for row in history} == set(ci.git_text("rev-list", ENTRY + ".." + W05_R01_BASE).splitlines())
    current = [row for row in history if row["current_unit_segment"]]
    assert len(current) == 1 and current[0]["commit"] == W05_R01_BASE and current[0]["tree"] == W05_R01_BASE_TREE
    assert set(current[0]["changed_paths"]) == COMMON and current[0]["immediate_scope_exceptions"] == []
    assert {row["unit"] for row in history} == {f"P3-W{i:02}" for i in range(1, 6)}
    w04 = [row for row in history if row["unit"] == "P3-W04"]
    assert next(row for row in w04 if row["commit"] == W04_R01_BASE)["immediate_scope_exceptions"] == []
    assert all(row["immediate_scope_exceptions"] == ["P3-W04-R01"] for row in w04 if row["commit"] != W04_R01_BASE)
    actual = ci.commit_hashes(W05_R01_BASE)
    accepted = ci.commit_hashes(W05_R01_PREDECESSOR)
    assert len(actual) == len(accepted) == 177 and set(actual) == set(accepted)
    assert {p for p in actual if actual[p] != accepted[p]} == COMMON


def test_w05_r01_only_three_old_transition_methods_have_authorized_adaptations():
    path = "tests/contract/test_phase3_transition.py"
    before = git_bytes(path, W05_R01_BASE)
    assert hashlib.sha256(before).hexdigest() == "6d04e15cdf30e3a832af1d50fdfa1bec85577710910817100aaa110fd7021169"
    changed = {
        "test_each_unit_has_exact_four_common_records_and_approved_paths",
        "test_w04_r01_name_is_cumulative_but_immediate_permissions_are_not",
        "test_w04_r01_driver_keeps_original_p2_and_unrelated_ci_ast",
    }
    live = ast.parse((ROOT / path).read_bytes())
    functions = [n for n in live.body if isinstance(n, ast.FunctionDef)]
    original = [n for n in ast.parse(before).body if isinstance(n, ast.FunctionDef)]
    for node in original:
        current = [n for n in functions if n.name == node.name]
        assert len(current) == 1, node.name
        if node.name not in changed:
            assert ast.dump(node) == ast.dump(current[0]), node.name
        else:
            assert ast.dump(node) != ast.dump(current[0]), node.name
    assert changed <= {n.name for n in original}


@pytest.mark.parametrize("case", (
    "clean", "clean_later_unit", "pre_boundary_repair", "earlier_unit_then_restore",
    "post_boundary_forbidden_then_restore", "unanchored_side_branch", "candidate_metadata_boundary",
    "wrong_boundary_tree", "wrong_boundary_parent", "wrong_predecessor_constant",
    "missing_boundary_ancestry", "wrong_footer", "duplicate_footer", "later_unit_repair",
))
def test_w05_r01_fixed_boundary_and_complete_history_reject_unauthorized_edits(tmp_path, case):
    """Real multi-unit Git history; candidate files never choose its boundary."""
    ci = ci_driver()
    repo = tmp_path / "five-unit-history"
    repo.mkdir()
    def git(*args):
        return subprocess.check_output(["git", "-c", "user.name=Synthetic Test",
            "-c", "user.email=synthetic@example.invalid", *args], cwd=repo,
            stderr=subprocess.PIPE, text=True, timeout=30).strip()
    def commit(message):
        git("add", "--all")
        git("commit", "-q", "-m", message)
        return git("rev-parse", "HEAD")
    git("init", "-q")
    git("config", "--local", "core.autocrlf", "false")
    git("config", "--local", "core.eol", "lf")
    repair = "tests/scaffold/test_module_manifest.py"
    w04_repair = "tests/scaffold/test_no_runtime_implementation.py"
    names = ("one.txt", "two.txt", "three.txt", "four.txt", "five.txt", "six.txt", "side.txt",
             "fixed.txt", repair, w04_repair)
    for name in names:
        target = repo / name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"entry\n")
    initial = commit("Synthetic planning entry")
    main = git("branch", "--show-current")
    entry = {"intake_commit": initial, "files": {name: hashlib.sha256(b"entry\n").hexdigest() for name in names}}
    paths = {"P3-W01": frozenset({"one.txt", repair, w04_repair}), "P3-W02": frozenset({"two.txt"}),
             "P3-W03": frozenset({"three.txt"}), "P3-W04": frozenset({"four.txt"}),
             "P3-W05": frozenset({"five.txt", "side.txt"}), "P3-W06": frozenset({"six.txt"})}
    for step, name in ((1, "one.txt"), (2, "two.txt"), (3, "three.txt"), (4, "four.txt")):
        previous = git("rev-parse", "HEAD")
        branch = f"synthetic-w{step:02}"
        git("checkout", "-q", "-b", branch)
        (repo / name).write_bytes(b"authorized unit bytes\n")
        unit_head = commit("Original unit work")
        if step == 3 and case == "earlier_unit_then_restore":
            (repo / repair).write_bytes(b"premature later repair\n")
            commit("Unapproved earlier-unit repair")
            (repo / repair).write_bytes(b"entry\n")
            commit("Restore old-unit final bytes")
        if step == 4:
            w04_predecessor, w04_boundary = previous, unit_head
            w04_tree = git("rev-parse", w04_boundary + "^{tree}")
            (repo / w04_repair).write_bytes(b"separately authorized W04 repair\n")
            commit("Existing W04 R01 successor")
        git("checkout", "-q", main)
        footer = f"SIT-Phase-Unit: P3-W{step:02}"
        if step == 4 and case == "wrong_footer":
            footer = "SIT-Phase-Unit: P3-W05"
        if step == 4 and case == "duplicate_footer":
            footer += "\n" + footer
        git("merge", "-q", "--no-ff", branch, "-m", "Accepted synthetic unit\n\n" + footer)
    predecessor = git("rev-parse", "HEAD")
    git("checkout", "-q", "-b", "synthetic-w05")
    (repo / "five.txt").write_bytes(b"original W05 records\n")
    if case in ("pre_boundary_repair", "candidate_metadata_boundary"):
        (repo / repair).write_bytes(b"unapproved before W05 boundary\n")
    boundary = commit("Fixed pre-amendment W05 head")
    boundary_tree = git("rev-parse", boundary + "^{tree}")
    if case == "unanchored_side_branch":
        git("checkout", "-q", "-b", "unanchored", predecessor)
        (repo / repair).write_bytes(b"unanchored repair\n")
        commit("Repair on a side branch before fixed boundary")
        (repo / repair).write_bytes(b"entry\n")
        (repo / "side.txt").write_bytes(b"otherwise allowed side work\n")
        commit("Restore side-branch repair bytes")
        git("checkout", "-q", "synthetic-w05")
        git("merge", "-q", "--no-ff", "unanchored", "-m", "Merge unanchored work")
    (repo / repair).write_bytes(b"approved narrow W05 successor repair\n")
    current = commit("Owner-authorized W05 R01 successor")
    if case == "candidate_metadata_boundary":
        (repo / "five.txt").write_text(json.dumps({
            "repair_base": current, "repair_tree": git("rev-parse", current + "^{tree}"),
            "scope_exceptions": ["P3-W05-R01"], "authorized_paths": sorted(ci.P3_W05_R01_PATHS),
        }), encoding="utf-8")
        current = commit("Candidate cannot relabel pre-amendment authority")
    if case == "post_boundary_forbidden_then_restore":
        (repo / "fixed.txt").write_bytes(b"forbidden mutation\n")
        commit("Out-of-scope intermediate successor")
        (repo / "fixed.txt").write_bytes(b"entry\n")
        current = commit("Restore final protected bytes")
    base, unit = predecessor, "P3-W05"
    if case in ("clean_later_unit", "later_unit_repair"):
        git("checkout", "-q", main)
        git("merge", "-q", "--no-ff", "synthetic-w05", "-m", "Accepted W05\n\nSIT-Phase-Unit: P3-W05")
        base = git("rev-parse", "HEAD")
        git("checkout", "-q", "-b", "synthetic-w06")
        (repo / "six.txt").write_bytes(b"authorized W06 work\n")
        if case == "later_unit_repair":
            (repo / repair).write_bytes(b"not authorized by cumulative W05 R01\n")
        current = commit("Later unit work")
        unit = "P3-W06"
    if case == "missing_boundary_ancestry":
        current = predecessor
    if case == "wrong_boundary_tree":
        boundary_tree = "0" * 40
    if case == "wrong_boundary_parent":
        (repo / "five.txt").write_bytes(b"candidate cannot move entry-parent boundary\n")
        boundary = current = commit("Wrong later boundary")
        boundary_tree = git("rev-parse", boundary + "^{tree}")
    declared_predecessor = initial if case == "wrong_predecessor_constant" else predecessor
    with patch.object(ci, "ROOT", repo), \
            patch.object(ci, "P3_W04_R01_BASE", w04_boundary), \
            patch.object(ci, "P3_W04_R01_BASE_TREE", w04_tree), \
            patch.object(ci, "P3_W04_R01_PREDECESSOR", w04_predecessor), \
            patch.object(ci, "P3_W05_R01_BASE", boundary), \
            patch.object(ci, "P3_W05_R01_BASE_TREE", boundary_tree), \
            patch.object(ci, "P3_W05_R01_PREDECESSOR", declared_predecessor):
        assert ci.commit_hashes(initial) == entry["files"]
        if case in ("clean", "clean_later_unit"):
            history = ci.phase3_history(entry, base, current, paths, unit)
            assert {row["commit"] for row in history} == set(git("rev-list", initial + ".." + current).splitlines())
            assert next(row for row in history if row["commit"] == boundary)["immediate_scope_exceptions"] == []
            assert any(row["unit"] == "P3-W04" and row["immediate_scope_exceptions"] == ["P3-W04-R01"] for row in history)
            assert any(row["unit"] == "P3-W05" and row["immediate_scope_exceptions"] == ["P3-W05-R01"] for row in history)
            for row in history:
                expected = (["P3-W04-R01"] if row["unit"] == "P3-W04" and row["commit"] != w04_boundary else
                            ["P3-W05-R01"] if row["unit"] == "P3-W05" and row["commit"] != boundary else [])
                assert row["immediate_scope_exceptions"] == expected
            if case == "clean_later_unit":
                assert next(row for row in history if row["commit"] == current)["immediate_scope_exceptions"] == []
                assert ci.phase3_scope_exceptions(unit) == ["P3-W04-R01", "P3-W05-R01"]
        else:
            reason = {
                "pre_boundary_repair": "intermediate_work_unit_allowlist_exceeded",
                "earlier_unit_then_restore": "intermediate_work_unit_allowlist_exceeded",
                "post_boundary_forbidden_then_restore": "intermediate_work_unit_allowlist_exceeded",
                "unanchored_side_branch": "entry_or_predecessor_ancestry_mismatch",
                "candidate_metadata_boundary": "intermediate_work_unit_allowlist_exceeded",
                "wrong_boundary_tree": "w05_repair_boundary_tree_mismatch",
                "wrong_boundary_parent": "w05_repair_boundary_parent_mismatch",
                "wrong_predecessor_constant": "w05_repair_predecessor_mismatch",
                "missing_boundary_ancestry": "entry_or_predecessor_ancestry_mismatch",
                "wrong_footer": "wrong_phase3_predecessor",
                "duplicate_footer": "wrong_phase3_predecessor",
                "later_unit_repair": "intermediate_work_unit_allowlist_exceeded",
            }[case]
            with pytest.raises(ValueError, match="^" + reason + "$"):
                ci.phase3_history(entry, base, current, paths, unit)
