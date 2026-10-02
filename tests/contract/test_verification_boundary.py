# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Direct current guarantees, with real positive controls before mutations.

VC-02 adds these alongside the legacy tests. Acceptance literals and expected
failure categories below are independently written; candidate maps do not
generate expectations. The default loader/CI switch remains a later milestone.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import xml.etree.ElementTree as ET

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools import check_scaffold_boundary as guard

ANCHOR = "2413a29b839b7e1de8f76a449762f031de19d52b"
TREE = "e2f230bdf6f838f3d12df233559732aa1d5c1699"
PARENTS = ["6dbca96f3314d537beed4ccb6202147bd9248dd9", "90684996eac568af6129973764fe40f3b666a15f"]
VC01 = "a47ea2480043c2bb267c047b2d99a67ab4428e53"
PLAN_HASH = "a94b59a0bfdbde3c70c7286fd48c5e0cbdb4a538afeb094ba97dce718bd7d11d"
PROJECT = "DavidWallstructurallaw/source-integrity-toolkit"
PRODUCT = "src/source_integrity_toolkit/runtime/boundary.py"
PLAN = "VERIFICATION_CONSOLIDATION_PLAN.md"
SCOPES = {
    "tools/check_scaffold_boundary.py", "tests/scaffold/test_imports.py",
    "tests/scaffold/test_module_manifest.py", "tests/scaffold/test_no_runtime_implementation.py",
    "tests/scaffold/test_layer_boundaries.py", "tests/scaffold/test_contract_catalogs.py",
    "tests/scaffold/test_ci_contract.py", "tests/contract/test_phase2_transition.py",
    "tests/contract/test_phase3_transition.py", ".github/workflows/phase1-ci.yml",
    "tests/contract/test_bundle_contract.py", "tests/contract/test_input_schema_mapping.py",
    "tests/contract/test_observability_preparation.py", "tests/security/test_input_capture.py",
    "tests/security/test_preparation_inertness.py", "tests/contract/test_verification_boundary.py",
    "verification/consolidation_map.json", "VERIFICATION_CONSOLIDATION_PLAN.md",
    "VERIFICATION_CONSOLIDATION_COMPLETION.md", "README.md",
}


def git(root, *args, input_bytes=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.check_output(
        ["git", "-c", "core.autocrlf=false", "-c", "core.safecrlf=false",
         "-c", "user.name=VC synthetic test", "-c", "user.email=vc-test@example.invalid", *args],
        cwd=root, env=env, input=input_bytes, stderr=subprocess.PIPE, timeout=60)


@pytest.fixture
def repo(tmp_path):
    path = tmp_path / "repository"
    git(tmp_path, "clone", "--quiet", "--no-checkout", "--no-hardlinks", str(ROOT), str(path))
    git(path, "checkout", "--quiet", "--detach", VC01)
    # The accepted checkpoint is deliberately fixed, not the mutable test HEAD.
    assert git(path, "rev-parse", "HEAD").decode().strip() == VC01
    return path


def edit(root, path, data=b"\n# synthetic VC review change\n"):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes((target.read_bytes() if target.exists() else b"") + data)


def commit(root, message="Synthetic VC test change"):
    git(root, "add", "-A")
    git(root, "commit", "--quiet", "-m", message)
    return git(root, "rev-parse", "HEAD").decode().strip()


def event(head=VC01, base=ANCHOR):
    return {"repository": {"full_name": PROJECT}, "pull_request": {
        "head": {"sha": head, "ref": "verification/consolidation", "repo": {"full_name": PROJECT}},
        "base": {"sha": base, "ref": "main", "repo": {"full_name": PROJECT}}}}


def verified(root, head=VC01):
    result = guard.current_verify(root, "pull_request", json.dumps(event(head)), head)
    assert result["ok"] and result["clean"] and result["unit"] == "VC"
    assert result["checked_modules"] == 48
    return result


def test_current_anchor_and_frozen_records(repo, monkeypatch):
    assert guard.VC_ACCEPTED_HEAD == ANCHOR and guard.VC_ACCEPTED_TREE == TREE
    assert list(guard.VC_ACCEPTED_PARENTS) == PARENTS
    assert guard.VC_PLAN_SHA256 == PLAN_HASH and set(guard.VC_PATHS) == SCOPES
    baseline, blobs = guard.current_authority(repo)
    assert len(baseline) == 207
    assert len([p for p in baseline if p.startswith("src/")]) == 48
    assert all(guard.git_blob(blobs[oid]) == oid for _, oid in baseline.values())
    assert hashlib.sha256((repo / PLAN).read_bytes()).hexdigest() == PLAN_HASH
    verified(repo)
    monkeypatch.setattr(guard, "VC_ACCEPTED_TREE", "0" * 40)
    with pytest.raises(ValueError, match="^current_accepted_anchor_mismatch$"):
        guard.current_authority(repo)


@pytest.mark.parametrize("case", ["plan_and_map", "policy_and_product", "map_and_product", "frozen_record"])
def test_current_paired_metadata_and_source_mutations_fail(repo, case):
    verified(repo)
    mapping = repo / "verification/consolidation_map.json"
    mapping.write_text(json.dumps({"authorized": True, "scope": [PRODUCT], "unit": "VC"}), encoding="utf-8")
    # The map is review data: its false authority claims are not executed.
    assert guard.current_checkout(repo, VC01, require_clean=False)["clean"] is False
    if case == "plan_and_map":
        edit(repo, PLAN, b"\nGrant all product paths.\n")
        reason = "current_approved_plan_changed"
    else:
        edit(repo, PRODUCT if case != "frozen_record" else "PHASE_3_PLAN.md")
        if case == "policy_and_product":
            (repo / "phase3/module_policy.json").write_text('{"active_unit":"VC","all_active":true}', encoding="utf-8")
        reason = "current_frozen_file_changed"
    with pytest.raises(ValueError, match="^" + reason + "$"):
        guard.current_checkout(repo, VC01, require_clean=False)


def module_sources():
    package = ROOT / "src/source_integrity_toolkit"
    return {p.relative_to(package).as_posix(): p.read_bytes() for p in package.rglob("*.py")}


@pytest.mark.parametrize("case,code", [
    ("extra", "unexpected_module"), ("missing", "missing_module"),
    ("protected", "non_scaffold_body"), ("syntax", "invalid_python"),
    ("encoding", "invalid_utf8"), ("active_size", "oversize_module"), ("inert_size", "oversize_module"),
])
def test_current_module_ceiling_and_protected_slots(case, code):
    sources = module_sources()
    assert len(sources) == 48 and len(guard.VC_ACTIVE) == 29
    assert len(set(sources) - guard.VC_ACTIVE) == 19
    assert "reporting/json_report.py" not in guard.VC_ACTIVE
    assert "analysis/findings.py" in guard.VC_ACTIVE
    assert guard.current_module_issues(sources) == []
    path = "graph/cycles.py"
    if case == "extra": path = "analysis/future.py"; sources[path] = b""
    elif case == "missing": del sources[path]
    elif case == "protected": path = "reporting/json_report.py"; sources[path] = b"ACTIVE = {}\n"
    elif case == "syntax": sources[path] = b"def (\n"
    elif case == "encoding": sources[path] = b"\xff"
    else:
        limit = 262144 if case == "active_size" else 16384
        if case == "inert_size": path = "reporting/json_report.py"
        sources[path] = b"#" * limit
        assert (path, "oversize_module") not in guard.current_module_issues(sources)
        sources[path] += b"#"
    assert (path, code) in guard.current_module_issues(sources)
    assert guard.current_module_issues(module_sources()) == []


@pytest.mark.parametrize("path,reason", [
    ("src/source_integrity_toolkit/hidden.pyc", "current_unexpected_source_file"),
    ("src/source_integrity_toolkit/native.pyd", "current_unexpected_source_file"),
    ("src/source_integrity_toolkit/__pycache__/injected.py", "current_unexpected_cache_entry"),
    ("src/source_integrity_toolkit/unapproved/hidden.pyc", "current_unexpected_source_directory"),
    ("src/extra/hidden.pyc", "current_unexpected_source_entry"),
])
def test_current_module_tree_includes_ignored_paths(repo, path, reason):
    assert guard.current_modules(repo) == 48
    edit(repo, path)
    with pytest.raises(ValueError, match="^" + reason + "$"):
        guard.current_modules(repo)
    (repo / path).unlink()
    if path.startswith("src/extra/") or "/unapproved/" in path:
        (repo / path).parent.rmdir()
    assert guard.current_modules(repo) == 48


def test_current_context_comes_from_exact_external_event(repo, tmp_path):
    result = verified(repo)
    assert result["base"] == ANCHOR and result["head"] == VC01
    push = {"repository": {"full_name": PROJECT}, "ref": "refs/heads/main", "before": ANCHOR,
            "after": VC01, "head_commit": {"id": VC01, "message": "Accept VC\n\nSIT-Verification-Unit: VC"}}
    assert guard.current_context("push", json.dumps(push), VC01) == {
        "event": "push", "unit": "VC", "base": ANCHOR, "head": VC01}
    event_file = tmp_path / "runner-event.json"
    event_file.write_text(json.dumps(event()), encoding="utf-8")
    command = [sys.executable, "-I", "-B", "-O", str(ROOT / "tools/check_scaffold_boundary.py"),
               "--root", str(repo), "--unit", "VC", "--event-name", "pull_request",
               "--event-file", str(event_file), "--head", VC01]
    positive = subprocess.run(command, capture_output=True, text=True, timeout=60)
    assert positive.returncode == 0, positive.stdout + positive.stderr
    assert json.loads(positive.stdout)["unit"] == "VC"
    edit(repo, PRODUCT)
    negative = subprocess.run(command, capture_output=True, text=True, timeout=60)
    assert negative.returncode == 1
    assert json.loads(negative.stdout)["issues"] == [{"code": "current_frozen_file_changed"}]


@pytest.mark.parametrize("case,reason", [
    ("head", "current_event_head_mismatch"), ("branch", "current_unapproved_branch"),
    ("fork", "current_unapproved_branch"), ("base_ref", "current_wrong_base_ref"),
    ("repository", "current_wrong_repository"), ("base", "current_invalid_base"),
    ("missing", "current_malformed_event"), ("duplicate", "duplicate_policy_key"),
    ("unknown_event", "current_unsupported_event"), ("duplicate_footer", "current_invalid_merge_footer"),
    ("phase_footer", "current_invalid_merge_footer"), ("no_footer", "current_invalid_merge_footer"),
])
def test_current_context_rejects_candidate_self_authorization(monkeypatch, case, reason):
    normal = event()
    monkeypatch.setenv("SIT_PHASE_UNIT", "P3-W15")
    assert guard.current_context("pull_request", json.dumps(normal), VC01)["unit"] == "VC"
    normal["candidate_authority"] = {"approved": True, "allowed_paths": [PRODUCT]}
    name, raw = "pull_request", None
    if case == "head": normal["pull_request"]["head"]["sha"] = ANCHOR
    elif case == "branch": normal["pull_request"]["head"]["ref"] = "phase3/p3-w15"
    elif case == "fork": normal["pull_request"]["head"]["repo"]["full_name"] = "fictional/fork"
    elif case == "base_ref": normal["pull_request"]["base"]["ref"] = "unreviewed"
    elif case == "repository": normal["repository"]["full_name"] = "fictional/other"
    elif case == "base": normal["pull_request"]["base"]["sha"] = "0" * 40
    elif case == "missing": del normal["pull_request"]
    elif case == "duplicate": raw = '{"repository":{},"repository":{}}'
    elif case == "unknown_event": name = "workflow_dispatch"
    else:
        name = "push"
        footer = {"duplicate_footer": "SIT-Verification-Unit: VC\nSIT-Verification-Unit: VC",
                  "phase_footer": "SIT-Verification-Unit: VC\nSIT-Phase-Unit: P3-W15", "no_footer": "approved"}[case]
        normal.update(ref="refs/heads/main", after=VC01, before=ANCHOR,
                      head_commit={"id": VC01, "message": footer})
    with pytest.raises(ValueError, match="^" + reason + "$"):
        guard.current_context(name, raw or json.dumps(normal), VC01)


@pytest.mark.parametrize("path", [PRODUCT, "README.md.bak", "tests/contract/test_verification_boundaries.py",
                                   "./README.md", "tests/../README.md", "README.md/", "README.md:stream",
                                   "tests\\contract\\test_verification_boundary.py"])
def test_current_exact_scope_rejects_unlisted_and_lookalike_paths(repo, path):
    baseline, blobs = guard.current_authority(repo)
    actual = guard._current_snapshot(repo, VC01)
    blobs.update(guard._current_objects(repo, [actual[PLAN][1]], "blob"))
    guard.current_scope(baseline, actual, blobs.__getitem__)
    changed = dict(actual)
    changed[path] = ("100644", "0" * 40)
    expected = ("current_frozen_file_changed" if path == PRODUCT else
                "current_path_alias" if path in {"./README.md", "tests/../README.md", "README.md/", "README.md:stream",
                                                "tests\\contract\\test_verification_boundary.py"} else "current_unlisted_path")
    with pytest.raises(ValueError, match="^" + expected + "$"):
        guard.current_scope(baseline, changed, blobs.__getitem__)


@pytest.mark.parametrize("case,reason", [
    ("unstaged", "current_frozen_file_changed"), ("staged_restored", "current_frozen_file_changed"),
    ("untracked", "current_unlisted_path"), ("deleted", "current_forbidden_deletion"),
    ("rename", "current_unlisted_path"), ("assume_unchanged", "current_frozen_file_changed"),
    ("mode", "current_file_mode_changed"), ("allowed_dirty", "current_dirty_checkout"),
    ("wrong_head", "current_checkout_head_mismatch"), ("mixed_semantic", "current_mixed_semantics_changed"),
])
def test_current_checkout_rejects_out_of_scope_states(repo, case, reason):
    verified(repo)
    if case == "untracked": edit(repo, "unapproved.txt")
    elif case == "deleted": (repo / PRODUCT).unlink()
    elif case == "rename": (repo / PRODUCT).rename(repo / "renamed.py")
    elif case == "mode": git(repo, "update-index", "--chmod=+x", PRODUCT)
    elif case == "allowed_dirty": edit(repo, "README.md")
    elif case == "mixed_semantic":
        path = repo / "tests/contract/test_bundle_contract.py"
        before = path.read_text(encoding="utf-8")
        assert 'assert not hasattr(atom,"accepted")' in before
        path.write_text(before.replace('assert not hasattr(atom,"accepted")', 'assert True'), encoding="utf-8")
    elif case != "wrong_head":
        original = (repo / PRODUCT).read_bytes()
        edit(repo, PRODUCT)
        if case == "staged_restored":
            git(repo, "add", PRODUCT); (repo / PRODUCT).write_bytes(original)
        if case == "assume_unchanged": git(repo, "update-index", "--assume-unchanged", PRODUCT)
    with pytest.raises(ValueError, match="^" + reason + "$"):
        guard.current_checkout(repo, ANCHOR if case == "wrong_head" else VC01)


@pytest.mark.parametrize("path,payload,code", [
    ("graph/cycles.py", b'def f():\n    return open("x")\n', "forbidden_effect"),
    ("graph/cycles.py", b'def f():\n    return eval("1")\n', "forbidden_effect"),
    ("graph/cycles.py", b"import socket\n", "unapproved_import"),
    ("graph/cycles.py", b"import ctypes\n", "unapproved_import"),
    ("graph/cycles.py", b"import subprocess\n", "unapproved_import"),
    ("graph/cycles.py", b"VALUE = sum((1, 2))\n", "import_time_execution"),
    ("graph/cycles.py", b"def f(x=sum((1, 2))):\n    return x\n", "import_time_execution"),
    ("graph/cycles.py", b"class X(metaclass=type):\n    pass\n", "custom_metaclass"),
    ("graph/cycles.py", b"async def f():\n    pass\n", "async_execution_not_selected"),
    ("graph/cycles.py", b'VALUE = "tests/golden/answer"\n', "runtime_catalog_or_oracle_reference"),
    ("contracts/results.py", b"from source_integrity_toolkit.runtime import boundary\n", "layer_violation"),
    ("runtime/boundary.py", b"from source_integrity_toolkit.reporting import json_report\n", "forbidden_dependency"),
    ("graph/cycles.py", b"from ..... import x\n", "relative_import_escape"),
    ("graph/cycles.py", b"from typing import *\n", "wildcard_import"),
])
def test_current_live_effects_and_dependencies(path, payload, code):
    sources = module_sources()
    assert guard.current_module_issues(sources) == []
    sources[path] = payload
    assert (path, code) in guard.current_module_issues(sources)


def test_current_live_declaration_positive_control():
    sources = module_sources()
    sources["graph/cycles.py"] = (b"from dataclasses import dataclass\n@dataclass(frozen=True)\n"
                                  b"class Record:\n    value: int = 1\n\ndef f(value):\n    return value\n")
    assert guard.current_module_issues(sources) == []
    sources["graph/cycles.py"] = b"from . import projections\n"
    sources["graph/projections.py"] = b"from . import cycles\n"
    assert ("src/source_integrity_toolkit", "import_cycle") in guard.current_module_issues(sources)


def junit(nodes, subtests=0):
    root = ET.Element("testsuites")
    suite = ET.SubElement(root, "testsuite", tests=str(len(nodes) + subtests), failures="0", errors="0", skipped="0")
    for node in nodes:
        file, name = node.split("::", 1)
        ET.SubElement(suite, "testcase", classname=file[:-3].replace("/", "."), name=name)
    return ET.tostring(root)


def test_current_collection_is_complete_and_unique():
    nodes = ["tests/contract/test_a.py::test_one[value::part]", "tests/security/test_b.py::test_two"]
    files = {"tests/contract/test_a.py", "tests/security/test_b.py"}
    guard.current_collection(nodes, files)
    assert guard.current_junit(junit(nodes, 3), nodes, 3) == {"tests": 2, "subtest_events": 3, "identities_match": True}
    for altered, reason in [([], "current_empty_or_invalid_collection"), (nodes + nodes, "current_duplicate_collection"),
                            (nodes[:1], "current_test_file_omitted")]:
        with pytest.raises(ValueError, match="^" + reason + "$"):
            guard.current_collection(altered, files)
    with pytest.raises(ValueError, match="^current_subtest_count_mismatch$"):
        guard.current_junit(junit(nodes, 3), nodes, 2)


@pytest.mark.parametrize("case,reason", [
    ("substitution", "current_junit_identity_mismatch"), ("omission", "current_junit_identity_mismatch"),
    ("duplicate", "current_junit_identity_mismatch"), ("false_zero", "current_unsuccessful_test_evidence"),
    ("subtest_failure", "current_unsuccessful_test_evidence"), ("skip", "current_unsuccessful_test_evidence"),
    ("aggregate", "current_subtest_count_mismatch"), ("negative", "current_invalid_junit_count"),
])
def test_current_collection_rejects_same_count_substitution(case, reason):
    nodes = ["tests/contract/test_a.py::test_one", "tests/contract/test_a.py::test_two"]
    assert guard.current_junit(junit(nodes), nodes, 0)["tests"] == 2
    root = ET.fromstring(junit(nodes)); suite = root[0]
    if case == "substitution": suite[1].set("name", "test_invented")
    elif case == "omission": suite.remove(suite[1])
    elif case == "duplicate": suite[1].set("name", "test_one")
    elif case == "false_zero": ET.SubElement(suite[0], "failure")
    elif case == "subtest_failure": suite.set("failures", "1")
    elif case == "skip": ET.SubElement(suite[0], "skipped")
    elif case == "aggregate": suite.set("tests", "9")
    elif case == "negative": suite.set("tests", "-1")
    with pytest.raises(ValueError, match="^" + reason + "$"):
        guard.current_junit(ET.tostring(root), nodes, 0)


@pytest.mark.parametrize("case,reason", [
    ("permissions", "current_workflow_permissions"), ("event", "current_workflow_triggers"),
    ("matrix", "current_workflow_matrix"), ("credentials", "current_workflow_checkout"),
    ("head", "current_workflow_checkout"), ("shallow", "current_workflow_checkout"),
    ("pin", "current_workflow_python"), ("plugins", "current_workflow_environment"),
    ("filter", "current_workflow_stage"), ("continue", "current_workflow_job_keys"),
    ("extra_job", "current_workflow_jobs"), ("extra_step", "current_workflow_steps"),
])
def test_current_workflow_policy_and_mutations(case, reason):
    workflow = json.loads((ROOT / ".github/workflows/phase1-ci.yml").read_bytes())
    guard.current_workflow(workflow)
    changed = copy.deepcopy(workflow); job = changed["jobs"]["scaffold"]; steps = job["steps"]
    if case == "permissions": changed["permissions"]["contents"] = "write"
    elif case == "event": changed["on"]["pull_request_target"] = changed["on"].pop("pull_request")
    elif case == "matrix": job["strategy"]["matrix"]["python"] = ["3.11"]
    elif case == "credentials": steps[0]["with"]["persist-credentials"] = True
    elif case == "head": steps[0]["with"]["ref"] = "main"
    elif case == "shallow": steps[0]["with"]["fetch-depth"] = 1
    elif case == "pin": steps[1]["uses"] = "actions/setup-python@main"
    elif case == "plugins": job["env"]["PYTEST_DISABLE_PLUGIN_AUTOLOAD"] = "0"
    elif case == "filter": steps[4]["run"] += " -k test_happy_path"
    elif case == "continue": job["continue-on-error"] = True
    elif case == "extra_job": changed["jobs"]["extra"] = {}
    elif case == "extra_step": steps.append({"run": "true"})
    with pytest.raises(ValueError, match="^" + reason + "$"):
        guard.current_workflow(changed)
    guard.current_workflow(workflow)


@pytest.mark.parametrize("case,reason", [
    ("budget", "current_workflow_budget"), ("float_budget", "current_workflow_budget"),
    ("evidence_success_only", "current_workflow_evidence"), ("upload_success_only", "current_workflow_upload"),
    ("empty_artifacts", "current_workflow_upload"), ("artifact_scope", "current_workflow_upload"),
])
def test_current_ci_budgets_and_failure_evidence(case, reason):
    assert guard.VC_SUITE_TIMEOUT == 2400
    workflow = json.loads((ROOT / ".github/workflows/phase1-ci.yml").read_bytes())
    guard.current_workflow(workflow)
    job = workflow["jobs"]["scaffold"]
    if case == "budget": job["timeout-minutes"] = 500
    elif case == "float_budget": job["timeout-minutes"] = 50.0
    elif case == "evidence_success_only": del job["steps"][5]["if"]
    elif case == "upload_success_only": del job["steps"][6]["if"]
    elif case == "empty_artifacts": job["steps"][6]["with"]["if-no-files-found"] = "warn"
    elif case == "artifact_scope": job["steps"][6]["with"]["path"] = "**/*"
    with pytest.raises(ValueError, match="^" + reason + "$"):
        guard.current_workflow(workflow)


def test_current_history_rejects_restored_forbidden_changes(repo):
    verified(repo)
    original = (repo / PRODUCT).read_bytes()
    edit(repo, "README.md"); allowed = commit(repo)
    assert [r["commit"] for r in guard.current_history(repo, ANCHOR, allowed)] == [VC01, allowed]
    edit(repo, PRODUCT); forbidden = commit(repo)
    (repo / PRODUCT).write_bytes(original); restored = commit(repo)
    assert git(repo, "diff", "--name-only", allowed, restored) == b""
    assert forbidden in git(repo, "rev-list", ANCHOR + ".." + restored).decode()
    with pytest.raises(ValueError, match="^current_frozen_file_changed$"):
        guard.current_history(repo, ANCHOR, restored)


@pytest.mark.parametrize("case", ["valid_side", "forbidden_side", "pre_anchor_side", "wrong_base"])
def test_current_history_validates_anchor_parents_and_side_branches(repo, case):
    verified(repo)
    git(repo, "checkout", "--quiet", "-b", "mainline")
    edit(repo, "README.md"); main = commit(repo)
    if case == "wrong_base":
        with pytest.raises(ValueError, match="^current_git_unavailable_or_incomplete$"):
            guard.current_history(repo, PARENTS[0], main)
        return
    git(repo, "checkout", "--quiet", "-b", "side", PARENTS[0] if case == "pre_anchor_side" else VC01)
    edit(repo, PRODUCT if case == "forbidden_side" else "tests/scaffold/test_imports.py")
    side = commit(repo)
    if case == "forbidden_side":
        git(repo, "checkout", VC01, "--", PRODUCT); commit(repo)
    git(repo, "checkout", "--quiet", "mainline")
    git(repo, "merge", "--quiet", "--no-ff", "side", "-m", "Synthetic side merge")
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    if case == "valid_side":
        rows = guard.current_history(repo, ANCHOR, head)
        assert {r["commit"] for r in rows} == {VC01, main, side, head}
        assert rows[-1]["parents"] == [main, side]
    else:
        with pytest.raises(ValueError, match="^" + ("current_frozen_file_changed" if case == "forbidden_side"
                                                   else "current_unanchored_parent") + "$"):
            guard.current_history(repo, ANCHOR, head)


def batch_record(root, oid):
    body = git(root, "cat-file", "commit", oid)
    return oid.encode() + b" commit " + str(len(body)).encode() + b"\n" + body + b"\n"


@pytest.mark.parametrize("case,reason", [
    ("missing", "current_incomplete_object_batch"), ("duplicate", "current_malformed_object_record"),
    ("reordered", "current_malformed_object_record"), ("extra", "current_extra_object_records"),
    ("truncated", "current_truncated_object"), ("wrong_type", "current_malformed_object_record"),
    ("wrong_id", "current_malformed_object_record"), ("size", "current_malformed_object_record"),
    ("wrong_parent", "current_git_object_hash_mismatch"), ("wrong_tree", "current_git_object_hash_mismatch"),
    ("leading_blank", "current_malformed_object_record"), ("trailing_blank", "current_extra_object_records"),
])
def test_current_git_metadata_rejects_malformed_responses(repo, monkeypatch, case, reason):
    expected = {ANCHOR: {"tree": TREE, "parents": PARENTS},
                VC01: {"tree": "0eaa6bbc406b2797b9a64c9cb840c856571b581b", "parents": [ANCHOR]}}
    assert guard.current_commit_metadata(repo, [ANCHOR, VC01]) == expected
    first, second = batch_record(repo, ANCHOR), batch_record(repo, VC01)
    raw = first + second
    if case == "missing": raw = first
    elif case == "duplicate": raw = first + first
    elif case == "reordered": raw = second + first
    elif case == "extra": raw += first
    elif case == "truncated": raw = raw[:-1]
    elif case == "wrong_type": raw = raw.replace(b" commit ", b" blob ", 1)
    elif case == "wrong_id": raw = b"0" * 40 + raw[40:]
    elif case == "size": raw = raw.replace(b" commit ", b" commit -", 1)
    elif case == "wrong_parent": raw = raw.replace(PARENTS[0].encode(), b"0" * 40, 1)
    elif case == "wrong_tree": raw = raw.replace(TREE.encode(), b"0" * 40, 1)
    elif case == "leading_blank": raw = b"\n" + raw
    elif case == "trailing_blank": raw += b"\n"
    monkeypatch.setattr(guard, "_current_git", lambda *args, **kwargs: raw)
    with pytest.raises(ValueError, match="^" + reason + "$"):
        guard.current_commit_metadata(repo, [ANCHOR, VC01])


@pytest.mark.parametrize("commit_ids,reason", [
    ([ANCHOR[:12]], "current_invalid_object_request"), ([123], "current_invalid_object_request"),
    ([ANCHOR.upper()], "current_invalid_object_request"), (ANCHOR, "current_invalid_object_request"),
    ([ANCHOR, ANCHOR], "current_duplicate_object_request"),
])
def test_current_git_metadata_invalid_requests_do_not_launch_git(monkeypatch, commit_ids, reason):
    def unexpected(*args, **kwargs):
        raise AssertionError("invalid request must not launch Git")
    monkeypatch.setattr(guard, "_current_git", unexpected)
    assert guard.current_commit_metadata(ROOT, []) == {}
    with pytest.raises(ValueError, match="^" + reason + "$"):
        guard.current_commit_metadata(ROOT, commit_ids)


def test_current_git_metadata_rereads_root_and_state(repo, tmp_path, monkeypatch):
    verified(repo)
    other = tmp_path / "other"
    git(tmp_path, "clone", "--quiet", "--no-hardlinks", str(repo), str(other))
    verified(other)
    git(other, "replace", VC01, ANCHOR)
    with pytest.raises(ValueError, match="^current_replaced_history$"):
        guard.current_history(other, ANCHOR, VC01)
    # No cached result and no ambient GIT_DIR redirect may validate another root.
    monkeypatch.setenv("GIT_DIR", str(other / ".git"))
    verified(repo)
    git(other, "replace", "-d", VC01)
    verified(other)
    (other / ".git/shallow").write_text(VC01 + "\n", encoding="ascii")
    with pytest.raises(ValueError, match="^current_shallow_history$"):
        guard.current_history(other, ANCHOR, VC01)


@pytest.mark.parametrize("case,reason", [
    ("shallow", "current_shallow_history"), ("replace", "current_replaced_history"),
    ("graft", "current_grafted_history"), ("missing_commit", "current_git_unavailable_or_incomplete"),
    ("missing_tree", "current_git_unavailable_or_incomplete"),
    ("missing_parent", "current_git_unavailable_or_incomplete"), ("missing_blob", "current_malformed_object_record"),
])
def test_current_history_handles_missing_and_overridden_objects(repo, case, reason):
    verified(repo)
    edit(repo, "README.md"); head = commit(repo)
    parent = head
    if case == "missing_parent":
        edit(repo, "README.md"); head = commit(repo)
    assert guard.current_history(repo, ANCHOR, head)[-1]["commit"] == head
    if case == "shallow": (repo / ".git/shallow").write_text(head + "\n", encoding="ascii")
    elif case == "replace": git(repo, "replace", head, ANCHOR)
    elif case == "graft": (repo / ".git/info/grafts").write_text(head + "\n", encoding="ascii")
    else:
        oid = {"missing_commit": head, "missing_parent": parent}.get(case)
        if oid is None:
            oid = git(repo, "rev-parse", head + (":README.md" if case == "missing_blob" else "^{tree}")).decode().strip()
        path = repo / ".git/objects" / oid[:2] / oid[2:]
        path.chmod(path.stat().st_mode | 0o200); path.unlink()
    with pytest.raises(ValueError, match="^" + reason + "$"):
        guard.current_history(repo, ANCHOR, head)


def test_current_history_rejects_wrong_parent(repo, monkeypatch):
    verified(repo)
    monkeypatch.setattr(guard, "VC_ACCEPTED_PARENTS", tuple(reversed(PARENTS)))
    with pytest.raises(ValueError, match="^current_accepted_anchor_mismatch$"):
        guard.current_history(repo, ANCHOR, VC01)
