# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W06 source-bound registry and strict whole-check/constituent separation."""
import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess
from dataclasses import FrozenInstanceError, fields
import pytest
from source_integrity_toolkit.contracts import report
from source_integrity_toolkit.runtime.boundary import _prepare_evidence_value

ROOT = Path(__file__).resolve().parents[2]
SOURCE_HASH = "44daa3c86fc7d12e7be16a3aedfe10d16b99f55aa69141f90319ce2b5e63ff6a"
BASE = "913f0a3d56b6c0f969e8a36ef7aa909e8ecab470"


def cases():
    spec = importlib.util.spec_from_file_location("sit_w06_cases", ROOT / "tests/contract/test_typed_records.py")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def load_partition():
    return json.loads((ROOT / "phase2/prerequisite_partition.json").read_bytes())


def historical_segment():
    spec = importlib.util.spec_from_file_location("sit_w06_phase3_migration", ROOT / "tests/contract/test_phase2_transition.py")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    module.current_phase3_guard()
    return module


def verify_partition(p):
    assert p["format"] == "sit-private-prerequisite-partition/0.1"
    assert p["source"]["sha256"] == SOURCE_HASH
    assert p["whole_checks_implemented"] == ["PC01"]
    assert p["whole_checks_execution_pending"] == list(report.PREREQUISITES[1:])
    assert p["analytical_results_implemented"] == []
    assert p["public_report"] is False
    assert p["question_binding_semantics"] == "family_relevance_union_not_per_leaf_conjunctive_gate"
    assert [r["check_id"] for r in p["checks"]] == list(report.PREREQUISITES)
    for row, (pc, owner) in zip(p["checks"], report.PREREQUISITE_OWNERS):
        assert row["deferred_semantic_owner"] == (None if pc == "PC01" else owner)
        assert row["whole_check_execution"] == ("completed_only_after_actual_admission" if pc == "PC01" else "pending")
        assert row["answer_policy"] == ("met_for_this_accepted_input_only" if pc == "PC01" else "no_whole_check_answer")
    assert [(r["family"], tuple(r["field_keys"]), tuple(r["relevant_questions"]), tuple(r["domain_indices"])) for r in p["families"]] == list(report.FAMILY_PREPARATION_BINDINGS)


def test_frozen_source_registry_and_partition_exactness():
    raw = (ROOT / "OBSERVABILITY_AND_REPORTING.md").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SOURCE_HASH
    p = load_partition(); verify_partition(p)
    text = raw.decode(); pc_rows = re.findall(r"^\| (PC\d{2}) \| (.*?) \| (.*?) \|$", text, re.M)
    assert len(pc_rows) == 24
    assert [(x["check_id"], x["question"], x["owning_rule"]) for x in p["checks"]] == pc_rows
    block = text.split("## 17. Output leaf catalog")[1].split("M003 keeps each comparison")[0]
    leaves = [("SIT-M" + n, tuple(re.findall(r"`([^`]+)`", body))) for n, body in re.findall(r"^\| M(\d{3}) \| (.*?) \|$", block, re.M)]
    assert [(n, fs) for n, fs, qs, ds in report.FAMILY_PREPARATION_BINDINGS] == leaves
    assert len(leaves) == 15 and sum(len(fs) for n, fs in leaves) == 57
    domain_block = text.split("## 15. Five observability labels")[1].split("## 16.")[0]
    domains = [(int(n), label) for n, label in re.findall(r"^\| Level (\d) \| (.*?) \|", domain_block, re.M)]
    assert tuple(domains) == report.DOMAIN_LABELS


@pytest.mark.parametrize("family,keys,qs,ds", report.FAMILY_PREPARATION_BINDINGS, ids=report.FAMILIES)
def test_each_family_retains_every_leaf_and_no_computed_value(family, keys, qs, ds):
    out = _prepare_evidence_value(cases().sparse())
    assert type(out) is report._ObservabilityPreparation
    row = next(x for x in out.inquiries[0].families if x.family == family)
    assert row.field_keys == keys and row.relevant_questions == qs
    assert {f.name for f in fields(row)} == {"family", "field_keys", "relevant_questions", "explicit_record_refs", "binding_note"}
    assert not hasattr(row, "result_state") and not hasattr(row, "value")
    assert "PC01" in qs and "PC24" in qs


@pytest.mark.parametrize("pc", report.PREREQUISITES)
def test_every_whole_check_has_only_its_authorized_execution(pc):
    out = _prepare_evidence_value(cases().rich())
    check = next(c for c in out.inquiries[0].prerequisites if c.prerequisite == pc)
    assert check.complete_check_executed is (pc == "PC01")
    assert check.answer == ("met" if pc == "PC01" else None)
    assert check.deferred_owner == (None if pc == "PC01" else dict(report.PREREQUISITE_OWNERS)[pc])
    assert not hasattr(check, "reason_code")


@pytest.mark.parametrize("pc", report.PREREQUISITES[1:])
def test_deferred_check_cannot_be_promoted_to_met_unknown_or_unmet(pc):
    for answer in ("met", "unknown", "unmet", "not_applicable"):
        with pytest.raises(TypeError):
            report._PrerequisitePreparation(pc, False, answer, dict(report.PREREQUISITE_OWNERS)[pc], ())
    with pytest.raises(TypeError):
        report._PrerequisitePreparation(pc, True, None, dict(report.PREREQUISITE_OWNERS)[pc], ())


@pytest.mark.parametrize("change", ["stale", "extra_check", "pending_missing", "result", "report", "gate", "drop_pc", "wrong_owner"])
def test_partition_rejects_omissions_and_overclaims(change):
    p = load_partition(); verify_partition(p)
    if change == "stale": p["whole_checks_implemented"] = []
    elif change == "extra_check": p["whole_checks_implemented"].append("PC12")
    elif change == "pending_missing": p["whole_checks_execution_pending"].pop()
    elif change == "result": p["analytical_results_implemented"] = ["single_origin_contribution_hhi"]
    elif change == "report": p["public_report"] = True
    elif change == "gate": p["question_binding_semantics"] = "all_required"
    elif change == "drop_pc": p["checks"].pop()
    else: p["checks"][11]["deferred_semantic_owner"] = "INGESTION_CONTRACT"
    with pytest.raises(AssertionError): verify_partition(p)


def test_preserves_existing_report_declarations_and_w05_admission_body():
    migration = historical_segment()
    for relative in ("src/source_integrity_toolkit/contracts/report.py", "src/source_integrity_toolkit/runtime/boundary.py", "src/source_integrity_toolkit/validation/semantics.py"):
        old = ast.parse(subprocess.check_output(["git", "show", BASE + ":" + relative], cwd=ROOT, timeout=30))
        new = ast.parse(migration.phase2_bytes(relative))
        old_defs = {n.name: n for n in old.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
        new_defs = {n.name: n for n in new.body if isinstance(n, (ast.FunctionDef, ast.ClassDef))}
        for name, prior in old_defs.items():
            current = copy.deepcopy(new_defs["_run_preparation" if name == "_prepare" else name])
            if name == "_prepare":
                current.name = "_prepare"
                assert current.args.kwonlyargs[-1].arg == "evidence_domains"
                current.args.kwonlyargs.pop(); current.args.kw_defaults.pop()
                # Locate the authorized post-admission navigation branch by AST,
                # preserving every old validation/error/acceptance statement.
                found = []
                for node in ast.walk(current):
                    for attr in ("body", "orelse", "finalbody"):
                        body = getattr(node, attr, None)
                        if isinstance(body, list):
                            for stmt in list(body):
                                if isinstance(stmt, ast.If) and isinstance(stmt.test, ast.Name) and stmt.test.id == "evidence_domains":
                                    found.append(stmt); body.remove(stmt)
                assert len(found) == 1
            assert ast.dump(prior, include_attributes=False) == ast.dump(current, include_attributes=False), (relative, name)


def test_only_ten_w06_paths_and_no_old_test_permissions_changed():
    migration = historical_segment()
    spec = importlib.util.spec_from_file_location("sit_w06_guard", ROOT / "tools/check_scaffold_boundary.py")
    guard = importlib.util.module_from_spec(spec); spec.loader.exec_module(guard)
    paths = guard.plan_paths(ROOT)
    assert len(paths["P2-W06"]) == 10
    current = guard.unit_number("P2-W09")
    assert current >= 6
    spec = importlib.util.spec_from_file_location("sit_w06_scope_driver", ROOT / "tests/scaffold/test_ci_contract.py")
    ci = importlib.util.module_from_spec(spec); spec.loader.exec_module(ci)
    allowed = set().union(*(ci.effective_paths(paths, f"P2-W{i:02}") for i in range(6, current + 1)))
    changed = subprocess.check_output(["git", "diff", "--name-only", BASE, migration.PHASE2_ACCEPTED], cwd=ROOT, text=True).splitlines()
    assert set(changed) <= allowed
    # The trusted unit context, not candidate status metadata, governs later
    # authorized edits. Do not create another test frozen to a transient stage.
    for name in ("tests/scaffold/test_ci_contract.py", "tests/contract/test_input_schema_mapping.py", ".github/workflows/phase1-ci.yml"):
        if name not in allowed:
            raw = subprocess.check_output(["git", "show", BASE + ":" + name], cwd=ROOT, timeout=30)
            assert raw == migration.phase2_bytes(name)
