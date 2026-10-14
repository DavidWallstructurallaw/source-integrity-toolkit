# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Direct current guarantees, with real positive controls before mutations.

Acceptance literals and failure categories are independently written; candidate
maps do not generate expectations. Actual Git histories exercise the current
context and risk routing, including restored changes and merge side branches.
"""
import copy
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools import check_scaffold_boundary as guard

ANCHOR = "fdad8c3449d2d223420c5d52bb9b4c1e863a9e3c"
TREE = "f6fbb8965520f33a09ca38cf413e11ca561110dd"
PARENTS = ["2413a29b839b7e1de8f76a449762f031de19d52b", "ce05c5dda9368182dbee074253d3a7c829af7719"]
# Reproducible synthetic plan-only bootstrap; no candidate source is executed.
ENTRY = "3dc6c7860e8206158338179d41d10ca6c37d13f1"
ENTRY_TREE = "b7fb26d515432776f4663550a26baf5826cebfa4"
PLAN_HASH = "5fac7a2a796338faae9b98af6e0cc4519396e378ba10b8c5afeb4d029d97cd48"
PROJECT = "DavidWallstructurallaw/source-integrity-toolkit"
BRANCH = "phase4/public-report"
PRODUCT = "src/source_integrity_toolkit/runtime/boundary.py"
PLAN = "PHASE_4_PLAN.md"
# Independently transcribed from the exact approved plan, never guard output.
PATH_IDS = {'P01': 'src/source_integrity_toolkit/contracts/report.py',
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
UNIT_IDS = {1: 'V01 V02 V03 V04 V05 V06 V07 V08 T04 T07 T08 T09 D01 D04 D05 D06 D08',
 2: 'P01 P02 T10 T11 N01 N15 N17 N18 N19 N20 D02 D03 D04 D05',
 3: 'P01 P03 N01 N02 N03 N15 N17 N20 D04 D05',
 4: 'P01 P03 P04 N02 N08 N15 N16 N17 N20 D04 D05',
 5: 'P01 P02 P05 P06 P08 P09 N04 N10 N16 N17 N18 N20 D04 D05',
 6: 'P05 P07 N05 N09 N10 N16 N17 N19 N20 D04 D05',
 7: 'P01 P02 P03 P04 P05 P06 P07 P08 P09 P10 N01 N02 N08 N10 N11 N12 N15 N16 D04 D05',
 8: 'P01 P02 P10 P11 P12 V03 T01 T02 T03 T05 T06 T07 T08 N06 N11 N12 N14 N15 N16 D04 D05 D08',
 9: 'N01 N02 N03 N04 N05 N06 N07 N08 N09 N10 N11 N12 N13 N15 N16 N17 N18 N19 N20 D04 D05',
 10: 'N14 D04 D05 D06 D07 D08'}
SCOPES = set(PATH_IDS.values())
UNIT_PATHS = {n: {PATH_IDS[key] for key in keys.split()} for n, keys in UNIT_IDS.items()}
ACTIVATION = {
    "contracts/report.py": 2, "contracts/execution.py": 2,
    "reporting/assemble.py": 3, "runtime/disclosure.py": 4,
    "reporting/escaping.py": 5, "reporting/json_report.py": 5,
    "runtime/resources.py": 5, "runtime/diagnostics.py": 5,
    "reporting/markdown_report.py": 6, "runtime/boundary.py": 7,
    "api.py": 8, "__init__.py": 8,
}
# SHA256 of all 48 accepted product files at fdad8c3. These values come from
# that independently accepted immutable tree, not a mutable policy table.
SOURCE_SHA256 = {
    "__init__.py": "0fdc19062761d6b718ff371557376483f7c8e7bbf7f3c347bcae576587513b97",
    "analysis/__init__.py": "2bcd171bde6b0b6c92c3a048cff959780e2e0616f468158b4b97d8967bf7e956",
    "analysis/context.py": "40cb6afefd1c187eaa8afe6555971d55da4cecba8ce3b157c83b42552e56a736",
    "analysis/contribution_profile.py": "4eccb7e682f8a8ce67192da1f7ccd3ced314b2f92e2cd2637444e9553ee502ed",
    "analysis/correction_outcomes.py": "11a09a667f6a2c6552a980875bf6f09255714582318263bc743db5907259af78",
    "analysis/correction_routes.py": "4935dd55e0f4b47b49b4e50d02b73dd816387fa93cdb6bc447ee8dde0c619c0f",
    "analysis/evaluator_lineage.py": "71e8a96caf3d25e9b6f130c99243ab5df16ab5a3407e8b39ac08f583a93c0cdd",
    "analysis/findings.py": "e983a368d3544998b2a4879a82e1a3366f20da074651a1084dc758bc569ff34b",
    "analysis/human_review.py": "bcff22f09add6285a2bcd744ab1e77d1d878f2a92eb1effb738564fe3716a3aa",
    "analysis/inventory.py": "6179f29dbff1afccb939d225947d57f9b9c1b4b03875f4ba992e993560087313",
    "analysis/origins.py": "de77914facb7cfabc7390dcd84cbbc80c8c9823f67d3e2bcb8e826ec21b7fac0",
    "analysis/presence.py": "69b3447fa721f97ce0aa5d488a22e6798ffa2012e1ec73a047e4da1141e8c518",
    "analysis/process_comparison.py": "9d0777bf4fdd422f4392657c3407970c47093de4992cf3837c9a3fe6e3d7e9d0",
    "api.py": "8808d7ef4a0db2f6e314c82fddd4b51cce164a165afaf43e6d626663f6f6768d",
    "cli.py": "0c3ee9522fbdf1774a707ec14ed630ce34a901da1f83f63b8aee0f25393d26bc",
    "contracts/__init__.py": "5a5c57d26930d12c3de59e180987f740b915e9eb17fd18a2daf29a6f91985432",
    "contracts/bundle.py": "7509a30f008de4ade02543bea26ccc4bd3d5843ae62f75b1841e2e61bcb903da",
    "contracts/constants.py": "d4bee68c62ba495e6aca1fdba352b013f9cc4ed7c3583b61092af234827ad486",
    "contracts/evidence.py": "1b9be04cde9674cb250b34c9d6acfb43bfd35beb19f8ebbe9304f714ef3fc611",
    "contracts/execution.py": "212101c332201eda064d0a45140e922cbf24b7d9bcf36f14a9dc89c2b1790fa3",
    "contracts/report.py": "262b8129cec88e4c0ee30b781045598fa73e76bfb578ee4211e631b67460b82a",
    "contracts/results.py": "565b4aa8d1053931b0b69b1af686b563427dce2b27be8215e916fbc18d335a11",
    "graph/__init__.py": "3db1c2c13cc1ae2bfb1a049894a04f7d27d7e6874d2079f1348d910aa0f5c943",
    "graph/cycles.py": "350e986d14aa6452c3a334eb4288d0d1b1105bdea6b0786c0ffc59380d8c5db9",
    "graph/projections.py": "b3aa1df29751c0001446af84abcbbde84820576ecb39bc34ff693485b9aea76d",
    "graph/traversal.py": "95f9f8a3eec1828f458256c1438fbd169f615c9698daaca176776b803d54f8f7",
    "graph/witnesses.py": "40682c09e9d3b53d0d36c5204961eb16739d13b392be68c4bf9698cbd1c31b9f",
    "io/__init__.py": "252ed1b29bff2517bc3ce909f4695d0f67c4baf0f1d7707708124107fbba783b",
    "io/input_file.py": "5628507c0989e94a3b5b5401e570b19256c940204859da9e938178ea261dea1f",
    "io/output_directory.py": "d27ae40d53b09355a0e3e137d490d1c2d1352edf67821c985bd0c79096b605ac",
    "io/platform_linux.py": "b63420614f26fc52ebe4e7d9af4d12782fd7374dc4780c420e0e4bdbe6091544",
    "io/platform_windows.py": "31e5f7b304d4455d5d60222f2077eefd284edce341c47524ac85de84f690b4c0",
    "io/publication.py": "ec5124c4f8f1db6d0f8a0d83ad6a62c28646d34c47740f706d1b47871480661d",
    "reporting/__init__.py": "f9db2edfae16c1062a74fcff49d6b5a68b25e35b108413cb1b2bab115ef9dcaa",
    "reporting/assemble.py": "ebbc9d87df2283da9e055be5b2db79187791a95043faa2311961d95be17e890d",
    "reporting/escaping.py": "9b910e3cc9e6d3bdbb20824420d8a2a599e12f3a300e0dffb9674a8696db0ca8",
    "reporting/json_report.py": "5e5b41e8e1a1f0c6d731a22d288905f8ad5d969e6904f374487be1d54bec26dc",
    "reporting/markdown_report.py": "e2af7736cc1254fd6f4ad4366ed24e6fc6163e2761c17c1cce8f48307a83ca7e",
    "runtime/__init__.py": "6bcbe18cb7295bd3339cf426931bdb29ed89edb348575d5deb070f008dec72c7",
    "runtime/boundary.py": "a53ce75d52b8720a7a7981b88d06dcc16d5e4ba6d21d0bb17094e67b693d5101",
    "runtime/diagnostics.py": "2763dd36343ad5e60aca3d5c244d6c94a288b09ebf268f045dcc3d5f01445814",
    "runtime/disclosure.py": "a9cf0d4b24eb4ddaa239747fc487a91aaf2708f8bd9954035dd42536b1c15b11",
    "runtime/resources.py": "0ff61d32061f78e5eb46ff9903d322dd9335cc964411dc10ffc91eef0a440449",
    "validation/__init__.py": "0688a44d77c520368899546cc30531aad2849443c12941b536539bab5aac218e",
    "validation/limits.py": "f01e4e5cbc076b07440df19ed2524db549849fcc6cd9834648437ee61a5e53c8",
    "validation/references.py": "7ab63627c068b38364f5c47a6731903fc55bc9d86318bed4f182d9602418df7b",
    "validation/semantics.py": "f98ce60e55d88f543c94a1e260d0172939eb061a983ade4a05f906f7df42ec5d",
    "validation/structure.py": "bf2e61a236539b4b8bada935b39c46203bb8ccad4102e79730e9f84ba52fa315"
}


def git(root, *args, input_bytes=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GIT_AUTHOR_DATE="2026-10-14T00:00:00+0000",
               GIT_COMMITTER_DATE="2026-10-14T00:00:00+0000")
    return subprocess.check_output(
        ["git", "-c", "core.autocrlf=false", "-c", "core.safecrlf=false",
         "-c", "user.name=P4 synthetic test", "-c", "user.email=p4-test@example.invalid", *args],
        cwd=root, env=env, input=input_bytes, stderr=subprocess.PIPE, timeout=60)


@pytest.fixture
def repo(tmp_path):
    path = tmp_path / "repository"
    git(tmp_path, "clone", "--quiet", "--no-checkout", "--no-hardlinks", str(ROOT), str(path))
    git(path, "checkout", "--quiet", "--detach", ANCHOR)
    (path / PLAN).write_bytes((ROOT / PLAN).read_bytes())
    assert commit(path, "Synthetic P4 bootstrap") == ENTRY
    # Entry bytes and metadata are fixed independently of the mutable HEAD.
    assert git(path, "rev-parse", "HEAD^{tree}").decode().strip() == ENTRY_TREE
    return path


def edit(root, path, data=b"\n# synthetic P4 review change\n"):
    target = root / path
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes((target.read_bytes() if target.exists() else b"") + data)


def commit(root, message="Synthetic P4 test change", *, unit=1):
    git(root, "add", "-A")
    git(root, "commit", "--quiet", "-m", message + "\n\nSIT-Phase-Unit: P4-W%02d" % unit)
    return git(root, "rev-parse", "HEAD").decode().strip()


def advance(root, stage):
    checkpoints = {1: ENTRY}
    for unit in range(2, stage + 1):
        record = root / 'phase4/implementation_evidence.json'
        record.parent.mkdir(exist_ok=True)
        record.write_text(json.dumps({'synthetic_unit': unit}) + '\n', encoding='utf-8')
        checkpoints[unit] = commit(root, 'Synthetic ordered checkpoint', unit=unit)
    return checkpoints


def event(head=ENTRY, base=ANCHOR):
    return {"repository": {"full_name": PROJECT}, "pull_request": {
        "head": {"sha": head, "ref": BRANCH, "repo": {"full_name": PROJECT}},
        "base": {"sha": base, "ref": "main", "repo": {"full_name": PROJECT}}}}


def push_event(root, head, base=ANCHOR):
    message = git(root, 'cat-file', 'commit', head).partition(b'\n\n')[2].decode('utf-8')
    return {'repository': {'full_name': PROJECT}, 'ref': 'refs/heads/main',
            'before': base, 'after': head, 'head_commit': {'id': head, 'message': message}}


def verified(root, head=ENTRY):
    result = guard.current_verify(root, "pull_request", json.dumps(event(head)), head)
    assert result["ok"] and result["clean"] and result["unit"] == "P4-W01"
    assert result["checked_modules"] == 48
    return result


def test_current_anchor_and_frozen_records(repo, monkeypatch):
    assert guard.P4_ACCEPTED_HEAD == ANCHOR and guard.P4_ACCEPTED_TREE == TREE
    assert list(guard.P4_ACCEPTED_PARENTS) == PARENTS
    assert guard.P4_PLAN_SHA256 == PLAN_HASH and set(guard.P4_PATHS) == SCOPES
    assert guard.P4_PLAN == PLAN and guard.P4_REPOSITORY == PROJECT and guard.P4_BRANCH == BRANCH
    assert len(SCOPES) == 59 and len(ACTIVATION) == 12
    assert {int(str(n).removeprefix('P4-W')): set(v) for n, v in guard.P4_UNIT_PATHS.items()} == UNIT_PATHS
    assert {k.removeprefix('src/source_integrity_toolkit/'): v for k, v in guard.P4_ACTIVATION.items()} == ACTIVATION
    baseline, blobs = guard.current_authority(repo)
    assert len(baseline) == 211
    observed = {path.removeprefix('src/source_integrity_toolkit/'):
                hashlib.sha256(blobs[oid]).hexdigest()
                for path, (_, oid) in baseline.items() if path.startswith('src/')}
    assert observed == SOURCE_SHA256
    assert all(guard.git_blob(blobs[oid]) == oid for _, oid in baseline.values())
    assert hashlib.sha256((repo / PLAN).read_bytes()).hexdigest() == PLAN_HASH
    verified(repo)
    monkeypatch.setattr(guard, 'P4_ACCEPTED_TREE', '0' * 40)
    with pytest.raises(ValueError, match='^current_accepted_anchor_mismatch$'):
        guard.current_authority(repo)


@pytest.mark.parametrize('case', ['plan_and_map', 'policy_and_product', 'map_and_product', 'frozen_record'])
def test_current_paired_metadata_and_source_mutations_fail(repo, case):
    verified(repo)
    mapping = repo / 'phase4/implementation_evidence.json'
    mapping.parent.mkdir(exist_ok=True)
    mapping.write_text(json.dumps({'authorized': True, 'scope': [PRODUCT], 'unit': 'P4-W10'}), encoding='utf-8')
    assert guard.current_checkout(repo, ENTRY, require_clean=False)['clean'] is False
    if case == 'plan_and_map':
        edit(repo, PLAN, b'\nGrant all product paths.\n')
        reason = 'current_approved_plan_changed'
    else:
        edit(repo, PRODUCT if case != 'frozen_record' else 'PHASE_3_PLAN.md')
        if case == 'policy_and_product':
            (repo / 'phase3/module_policy.json').write_text('{"active_unit":"P4-W10","all_active":true}', encoding='utf-8')
        reason = 'current_frozen_file_changed' if case in ('frozen_record', 'policy_and_product') else 'current_premature_activation'
    with pytest.raises(ValueError, match='^' + reason + '$'):
        guard.current_checkout(repo, ENTRY, require_clean=False)


def module_sources():
    package = ROOT / "src/source_integrity_toolkit"
    return {p.relative_to(package).as_posix(): p.read_bytes() for p in package.rglob("*.py")}


@pytest.mark.parametrize("case", ["without_git", "git_blocked", "poisoned_git_output"])
def test_current_test_loading_has_no_historical_blob_execution(tmp_path, case):
    paths = ["tests/scaffold/" + name + ".py" for name in (
        "test_imports", "test_module_manifest", "test_no_runtime_implementation",
        "test_layer_boundaries", "test_contract_catalogs", "test_ci_contract")]
    root = ROOT
    if case == "without_git":
        root = tmp_path / "source-only"
        for relative in [*paths, "tools/check_scaffold_boundary.py"]:
            target = root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / relative, target)
        assert not (root / ".git").exists()
    script = r'''
import ast, inspect, json, os, subprocess, sys
from pathlib import Path
from unittest.mock import patch
root, case, paths = Path(sys.argv[1]), sys.argv[2], json.loads(sys.argv[3])
sys.path[:0] = [str(root), str(root / "src")]
os.environ.update(PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", SIT_PHASE_UNIT="INVALID-CONTEXT")
import pytest
calls = []
poison = b'raise AssertionError("historical_source_executed")\n'
original = subprocess.check_output
def source_gate(command, *args, **kwargs):
    if isinstance(command, (list, tuple)) and Path(str(command[0])).name.lower() in ("git", "git.exe"):
        calls.append(list(command))
        if case == "poisoned_git_output":
            return poison.decode() if kwargs.get("text") else poison
        raise RuntimeError("git_disabled_for_test_loading")
    return original(command, *args, **kwargs)
def audit(event, args):
    if event == "subprocess.Popen" and Path(str(args[0])).name.lower() in ("git", "git.exe"):
        calls.append(list(args[1]))
        raise RuntimeError("git_disabled_for_test_loading")
sys.addaudithook(audit)
class Capture:
    def pytest_collection_finish(self, session):
        self.items = list(session.items)
capture = Capture()
with patch.object(subprocess, "check_output", source_gate):
    # Prove the gate is active before using its zero-call result as evidence.
    if case == "poisoned_git_output":
        assert subprocess.check_output(["git", "show", "fixture:source.py"]) == poison
    else:
        try:
            subprocess.check_output(["git", "show", "fixture:source.py"])
        except RuntimeError as error:
            assert str(error) == "git_disabled_for_test_loading"
        else:
            raise AssertionError("inactive_git_gate")
    assert len(calls) == 1
    calls.clear()
    status = pytest.main([*paths, "--collect-only", "-q", "-p", "no:cacheprovider"], plugins=[capture])
assert status == 0 and capture.items and calls == []
assert {item.nodeid.split("::", 1)[0] for item in capture.items} == set(paths)
assert len({item.nodeid for item in capture.items}) == len(capture.items)
for item in capture.items:
    function = inspect.unwrap(item.obj)
    path = root / item.nodeid.split("::", 1)[0]
    assert Path(function.__code__.co_filename).resolve() == path.resolve()
    declarations = [node for node in ast.walk(ast.parse(path.read_text(encoding="utf-8")))
                    if isinstance(node, ast.FunctionDef) and node.name == function.__name__]
    assert any(min([node.lineno] + [d.lineno for d in node.decorator_list]) ==
               function.__code__.co_firstlineno for node in declarations)
from tools import check_scaffold_boundary as guard
assert not hasattr(guard, "load_phase1_test")
print("CURRENT_SOURCE_LOADING_OK")
'''
    result = subprocess.run([sys.executable, "-I", "-B", "-c", script, str(root), case, json.dumps(paths)],
                            cwd=root, capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stdout + result.stderr
    assert result.stdout.splitlines()[-1] == "CURRENT_SOURCE_LOADING_OK"


def test_current_package_probe_cannot_substitute_for_checkout_authorization(repo):
    command = [sys.executable, '-I', '-B', '-O', str(ROOT / 'tools/check_scaffold_boundary.py'),
               '--root', str(repo), '--modules-only']
    for package_stage in ([], ['--unit', 'P4-W01'], ['--stage', '1'],
                          ['--unit', 'P4-W01', '--stage', '1']):
        positive = subprocess.run(command + package_stage, capture_output=True, text=True, timeout=60)
        assert positive.returncode == 0, positive.stdout + positive.stderr
        report = json.loads(positive.stdout)
        assert report['ok'] and report['checked_modules'] == 48
    for context in (['--head', ENTRY], ['--event-name', 'pull_request'],
                    ['--event-file', str(repo / 'event.json')]):
        refused = subprocess.run(command + context, capture_output=True, text=True, timeout=60)
        assert refused.returncode == 1
        assert json.loads(refused.stdout) == {
            'ok': False, 'issues': [{'code': 'current_external_context_required'}]}
    verified(repo)
    edit(repo, 'README.md')
    package_only = subprocess.run(command, capture_output=True, text=True, timeout=60)
    assert package_only.returncode == 0 and json.loads(package_only.stdout)['ok']
    with pytest.raises(ValueError, match='^current_dirty_checkout$'):
        guard.current_checkout(repo, ENTRY)


def test_current_package_frozen_preparation_bytes_have_positive_and_negative_controls():
    sources = module_sources()
    assert {p: hashlib.sha256(raw).hexdigest() for p, raw in sources.items()} == SOURCE_SHA256
    assert guard.current_module_issues(sources, stage=1) == []
    for path in SOURCE_SHA256:
        changed = dict(sources)
        changed[path] += b'\n# unauthorized byte change\n'
        assert (path, 'accepted_blob_changed') in guard.current_module_issues(changed, stage=1)
    for path in set(SOURCE_SHA256) - set(ACTIVATION):
        changed = dict(sources)
        changed[path] += b'\n# permanently frozen byte change\n'
        assert (path, 'accepted_blob_changed') in guard.current_module_issues(changed, stage=10)
    assert len(set(SOURCE_SHA256) - set(ACTIVATION)) == 36
    assert guard.current_module_issues(sources, stage=1) == []


@pytest.mark.parametrize("case,code", [
    ("extra", "unexpected_module"), ("missing", "missing_module"),
    ("protected", "non_scaffold_body"), ("syntax", "invalid_python"),
    ("public_report", "non_scaffold_body"),
    ("encoding", "invalid_utf8"), ("active_size", "oversize_module"), ("inert_size", "oversize_module"),
])
def test_current_module_ceiling_and_protected_slots(case, code):
    sources = module_sources()
    assert len(sources) == 48
    assert len(ACTIVATION) == 12 and len(set(sources) - set(ACTIVATION)) == 36
    assert guard.current_module_issues(sources) == []
    path = "graph/cycles.py"
    if case == "extra": path = "analysis/future.py"; sources[path] = b""
    elif case == "missing": del sources[path]
    elif case == "protected": path = "reporting/json_report.py"; sources[path] = b"ACTIVE = {}\n"
    elif case == "public_report":
        path = "api.py"
        sources[path] = b'def audit_bundle(x):\n    return {"report_kind": "audit_report"}\n'
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
    assert result['base'] == ANCHOR and result['head'] == ENTRY
    pushed = push_event(repo, ENTRY)
    context = guard.current_context('push', json.dumps(pushed), ENTRY, root=repo)
    assert context['event'] == 'push' and context['unit'] == 'P4-W01'
    assert context['base'] == ANCHOR and context['head'] == ENTRY
    event_file = tmp_path / 'runner-event.json'
    event_file.write_text(json.dumps(event()), encoding='utf-8')
    command = [sys.executable, '-I', '-B', '-O', str(ROOT / 'tools/check_scaffold_boundary.py'),
               '--root', str(repo), '--unit', 'P4-W01', '--event-name', 'pull_request',
               '--event-file', str(event_file), '--head', ENTRY]
    positive = subprocess.run(command, capture_output=True, text=True, timeout=60)
    assert positive.returncode == 0, positive.stdout + positive.stderr
    assert json.loads(positive.stdout)['unit'] == 'P4-W01'
    edit(repo, PRODUCT)
    negative = subprocess.run(command, capture_output=True, text=True, timeout=60)
    assert negative.returncode == 1
    assert json.loads(negative.stdout)['issues'] == [{'code': 'current_premature_activation'}]


@pytest.mark.parametrize('case,reason', [
    ('head', 'current_event_head_mismatch'), ('branch', 'current_unapproved_branch'),
    ('fork', 'current_unapproved_branch'), ('base_ref', 'current_wrong_base_ref'),
    ('repository', 'current_wrong_repository'), ('base', 'current_invalid_base'),
    ('missing', 'current_malformed_event'), ('duplicate', 'duplicate_policy_key'),
    ('unknown_event', 'current_unsupported_event'), ('forged_message', 'current_event_commit_mismatch'),
])
def test_current_context_rejects_candidate_self_authorization(repo, monkeypatch, case, reason):
    normal = event()
    monkeypatch.setenv('SIT_PHASE_UNIT', 'P4-W10')
    assert guard.current_context('pull_request', json.dumps(normal), ENTRY, root=repo)['unit'] == 'P4-W01'
    normal['candidate_authority'] = {'approved': True, 'allowed_paths': [PRODUCT]}
    normal['pull_request']['title'] = 'SIT-Phase-Unit: P4-W10'
    name, raw = 'pull_request', None
    if case == 'head': normal['pull_request']['head']['sha'] = ANCHOR
    elif case == 'branch': normal['pull_request']['head']['ref'] = 'phase3/p3-w15'
    elif case == 'fork': normal['pull_request']['head']['repo']['full_name'] = 'fictional/fork'
    elif case == 'base_ref': normal['pull_request']['base']['ref'] = 'unreviewed'
    elif case == 'repository': normal['repository']['full_name'] = 'fictional/other'
    elif case == 'base': normal['pull_request']['base']['sha'] = '0' * 40
    elif case == 'missing': del normal['pull_request']
    elif case == 'duplicate': raw = '{"repository":{},"repository":{}}'
    elif case == 'unknown_event': name = 'workflow_dispatch'
    else:
        name, normal = 'push', push_event(repo, ENTRY)
        normal['head_commit']['message'] = 'SIT-Phase-Unit: P4-W10'
    with pytest.raises(ValueError, match='^' + reason + '$'):
        guard.current_context(name, raw or json.dumps(normal), ENTRY, root=repo)


@pytest.mark.parametrize('case,value,reason', [
    ('branch', 'phase4/public-report; injected', 'current_unapproved_branch'),
    ('branch', 'phase4/public-report\n', 'current_unapproved_branch'),
    ('branch', 'phase4/public-report/extra', 'current_unapproved_branch'),
    ('branch', 'verification/consolidation', 'current_unapproved_branch'),
    ('push_ref', 'refs/heads/phase4/public-report', 'current_unsupported_event'),
    ('push_after', ANCHOR, 'current_event_head_mismatch'),
    ('push_head_id', ANCHOR, 'current_event_head_mismatch'),
    ('push_deleted', True, 'current_event_head_mismatch'),
    ('push_forced', True, 'current_event_head_mismatch'),
    ('base', 'HEAD', 'current_invalid_base'), ('base', None, 'current_invalid_base'),
    ('base', ENTRY, 'current_invalid_base'),
    ('review_head', ENTRY[:12], 'current_invalid_review_head'),
    ('review_head', ENTRY.upper(), 'current_invalid_review_head'),
    ('review_head', None, 'current_invalid_review_head'),
])
def test_current_context_preserves_exact_branch_footer_and_commit_boundaries(repo, case, value, reason):
    normal = event()
    assert guard.current_context('pull_request', json.dumps(normal), ENTRY, root=repo)['unit'] == 'P4-W01'
    push = push_event(repo, ENTRY)
    assert guard.current_context('push', json.dumps(push), ENTRY, root=repo)['unit'] == 'P4-W01'
    name, head = 'pull_request', ENTRY
    if case == 'branch': normal['pull_request']['head']['ref'] = value
    elif case == 'base': normal['pull_request']['base']['sha'] = value
    elif case == 'review_head': head = value
    else:
        name, normal = 'push', push
        if case == 'push_head_id': normal['head_commit']['id'] = value
        else: normal[case.removeprefix('push_')] = value
    with pytest.raises(ValueError, match='^' + reason + '$'):
        guard.current_context(name, json.dumps(normal), head, root=repo)


@pytest.mark.parametrize("path", [PRODUCT, "README.md.bak", "tests/contract/test_verification_boundaries.py",
                                   "./README.md", "tests/../README.md", "README.md/", "README.md:stream",
                                   "tests\\contract\\test_verification_boundary.py"])
def test_current_exact_scope_rejects_unlisted_and_lookalike_paths(repo, path):
    baseline, blobs = guard.current_authority(repo)
    actual = guard._current_snapshot(repo, ENTRY)
    blobs.update(guard._current_objects(repo, [actual[PLAN][1]], "blob"))
    guard.current_scope(baseline, actual, blobs.__getitem__)
    changed = dict(actual)
    changed[path] = ("100644", "0" * 40)
    expected = ("current_premature_activation" if path == PRODUCT else
                "current_path_alias" if path in {"./README.md", "tests/../README.md", "README.md/", "README.md:stream",
                                                "tests\\contract\\test_verification_boundary.py"} else "current_unlisted_path")
    with pytest.raises(ValueError, match="^" + expected + "$"):
        guard.current_scope(baseline, changed, blobs.__getitem__)


@pytest.mark.parametrize("case,reason", [
    ("unstaged", "current_premature_activation"), ("staged_restored", "current_premature_activation"),
    ("untracked", "current_unlisted_path"), ("deleted", "current_forbidden_deletion"),
    ("rename", "current_unlisted_path"), ("assume_unchanged", "current_premature_activation"),
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
        path = repo / "tests/security/test_preparation_inertness.py"
        before = path.read_text(encoding="utf-8")
        assert "assert type(value) is _SafeDiagnostic" in before
        path.write_text(before.replace("assert type(value) is _SafeDiagnostic", "assert True"), encoding="utf-8")
    elif case != "wrong_head":
        original = (repo / PRODUCT).read_bytes()
        edit(repo, PRODUCT)
        if case == "staged_restored":
            git(repo, "add", PRODUCT); (repo / PRODUCT).write_bytes(original)
        if case == "assume_unchanged": git(repo, "update-index", "--assume-unchanged", PRODUCT)
    with pytest.raises(ValueError, match="^" + reason + "$"):
        guard.current_checkout(repo, ANCHOR if case == "wrong_head" else ENTRY)


@pytest.mark.parametrize("path,payload,code", [
    ("graph/cycles.py", b'def f():\n    return open("x")\n', "forbidden_effect"),
    ("graph/cycles.py", b'def f():\n    return eval("1")\n', "forbidden_effect"),
    ("graph/cycles.py", b"import socket\n", "unapproved_import"),
    ("graph/cycles.py", b"import ctypes\n", "unapproved_import"),
    ("graph/cycles.py", b"import subprocess\n", "unapproved_import"),
    ("runtime/boundary.py", b"from pathlib import Path\n", "unapproved_import"),
    ("runtime/boundary.py", b"import recursive_integrity_toolkit\n", "unapproved_import"),
    ("graph/cycles.py", b"VALUE = sum((1, 2))\n", "import_time_execution"),
    ("graph/cycles.py", b"def f(x=sum((1, 2))):\n    return x\n", "import_time_execution"),
    ("graph/cycles.py", b"class X(metaclass=type):\n    pass\n", "custom_metaclass"),
    ("graph/cycles.py", b"async def f():\n    pass\n", "async_execution_not_selected"),
    ("graph/cycles.py", b'VALUE = "tests/golden/answer"\n', "runtime_catalog_or_oracle_reference"),
    ("contracts/results.py", b"from source_integrity_toolkit.runtime import boundary\n", "layer_violation"),
    ("runtime/boundary.py", b"from source_integrity_toolkit.reporting import json_report\n", "forbidden_dependency"),
    ("runtime/boundary.py", b"from ..reporting import assemble\n", "forbidden_dependency"),
    ("runtime/boundary.py", b"from ..io import platform_windows\n", "forbidden_dependency"),
    ("graph/cycles.py", b"from ..... import x\n", "relative_import_escape"),
    ("graph/cycles.py", b"from typing import *\n", "wildcard_import"),
])
def test_current_live_effects_and_dependencies(path, payload, code):
    sources = module_sources()
    assert guard.current_module_issues(sources) == []
    sources[path] = payload
    assert code in guard.current_live_issues(path, payload.decode(), stage=1)


def test_current_live_declaration_positive_control():
    path = 'reporting/assemble.py'
    source = ('from dataclasses import dataclass\n@dataclass(frozen=True)\n'
              'class Record:\n    value: int = 1\n\ndef f(value):\n    return value\n')
    assert guard.current_live_issues(path, source, stage=3) == []
    sources = module_sources()
    sources[path] = b'from . import json_report\n'
    sources['reporting/json_report.py'] = b'from . import assemble\n'
    assert ('src/source_integrity_toolkit', 'import_cycle') in guard.current_module_issues(sources, stage=5)


def test_reporting_composition_activation_does_not_grant_lower_layers_authority():
    source = 'from ..reporting import assemble\n'
    assert guard.current_live_issues('runtime/boundary.py', source, stage=7) == []
    assert 'forbidden_dependency' in guard.current_live_issues('runtime/boundary.py', source, stage=6)
    for stage in (3, 7, 10):
        assert 'layer_violation' in guard.current_layer_issues(
            'reporting/assemble.py', 'from ..analysis import origins\n', stage=stage)
        assert 'layer_violation' in guard.current_layer_issues(
            'contracts/report.py', 'from ..runtime import boundary\n', stage=stage)
        assert 'forbidden_dependency' in guard.current_live_issues(
            'runtime/boundary.py', 'from ..io import platform_windows\n', stage=stage)


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
    assert guard.P4_SUITE_TIMEOUT == 2400
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
    assert [r["commit"] for r in guard.current_history(repo, ANCHOR, allowed)] == [ENTRY, allowed]
    edit(repo, PRODUCT); forbidden = commit(repo)
    (repo / PRODUCT).write_bytes(original); restored = commit(repo)
    assert git(repo, "diff", "--name-only", allowed, restored) == b""
    assert forbidden in git(repo, "rev-list", ANCHOR + ".." + restored).decode()
    with pytest.raises(ValueError, match="^current_premature_activation$"):
        guard.current_history(repo, ANCHOR, restored)


def test_current_history_rejects_restored_workflow_security_changes(repo):
    verified(repo)
    path = '.github/workflows/phase1-ci.yml'
    original = (repo / path).read_bytes()
    workflow = json.loads(original)
    steps = workflow['jobs']['scaffold']['steps']
    python_step = next(step for step in steps if step.get('uses', '').startswith('actions/setup-python@'))
    assert python_step['uses'] != 'actions/setup-python@main'
    python_step['uses'] = 'actions/setup-python@main'
    (repo / path).write_text(json.dumps(workflow) + '\n', encoding='utf-8')
    changed = commit(repo)
    (repo / path).write_bytes(original)
    restored = commit(repo)
    assert git(repo, 'diff', '--name-only', ENTRY, restored) == b''
    assert changed in git(repo, 'rev-list', ANCHOR + '..' + restored).decode()
    with pytest.raises(ValueError, match='^current_workflow_python$'):
        guard.current_history(repo, ANCHOR, restored)


@pytest.mark.parametrize('case', ['body', 'decorator', 'rebind'])
def test_current_history_rejects_restored_audit_file_changes_after_w08(repo, case):
    before = advance(repo, 8)[8]
    assert guard.current_history(repo, ANCHOR, before)[-1]['activation_stage'] == 8
    path = 'src/source_integrity_toolkit/api.py'
    original = (repo / path).read_bytes()
    if case == 'body':
        marker = b'    """Refuse immediately; never resolve, read or create a supplied path."""\n'
        assert original.count(marker) == 1
        changed_source = original.replace(marker, marker + b'    repr(input_path)\n')
    elif case == 'decorator':
        assert original.count(b'def audit_file(') == 1
        changed_source = original.replace(b'def audit_file(', b'@staticmethod\ndef audit_file(')
    else:
        changed_source = original + b'\naudit_file = audit_bundle\n'
    assert changed_source != original
    (repo / path).write_bytes(changed_source)
    changed = commit(repo, unit=8)
    (repo / path).write_bytes(original)
    restored = commit(repo, unit=8)
    assert git(repo, 'diff', '--name-only', before, restored) == b''
    assert changed in git(repo, 'rev-list', ANCHOR + '..' + restored).decode()
    with pytest.raises(ValueError, match='^current_audit_file_changed$'):
        guard.current_history(repo, ANCHOR, restored)


def test_current_history_rejects_restored_later_product_effects(repo):
    before = advance(repo, 3)[3]
    assert guard.current_history(repo, ANCHOR, before)[-1]['activation_stage'] == 3
    path = 'src/source_integrity_toolkit/reporting/assemble.py'
    original = (repo / path).read_bytes()
    edit(repo, path, b'\nimport socket\n')
    changed = commit(repo, unit=3)
    (repo / path).write_bytes(original)
    restored = commit(repo, unit=3)
    assert git(repo, 'diff', '--name-only', before, restored) == b''
    assert changed in git(repo, 'rev-list', ANCHOR + '..' + restored).decode()
    with pytest.raises(ValueError, match='^current_product_boundary_failed$'):
        guard.current_history(repo, ANCHOR, restored)


@pytest.mark.parametrize('stage', [1, 5, 9])
def test_current_risk_early_records_only_changes_require_full_verification(repo, stage):
    base = advance(repo, stage)[stage]
    assert guard.current_history(repo, ANCHOR, base)[-1]['activation_stage'] == stage
    path = 'phase4/implementation_evidence.json'
    edit(repo, path, b'\n')
    head = commit(repo, unit=stage)
    route = guard.current_risk(repo, base, head)
    assert route['changed_paths'] == route['net_changed_paths'] == [path]
    assert route['profile'] == 'full' and route['reason'] == 'early_stage_requires_full'
    assert [row['commit'] for row in route['commit_changes']] == [head]


@pytest.mark.parametrize('path', ['PHASE_4_COMPLETION.md', 'phase4/implementation_evidence.json'])
def test_current_risk_allows_only_explicit_non_executable_documentation(repo, path):
    checkpoints = advance(repo, 10)
    base = checkpoints[10]
    edit(repo, path, b'\n')
    head = commit(repo, unit=10)
    route = guard.current_risk(repo, base, head)
    assert route['profile'] == 'documentation'
    assert route['reason'] == 'documentation_paths_only'
    assert route['base'] == base and route['head'] == head
    assert route['changed_paths'] == route['net_changed_paths'] == [path]
    assert route['commit_changes'] == [{
        'commit': head, 'tree': git(repo, 'rev-parse', head + '^{tree}').decode().strip(),
        'parents': [{'parent': base, 'changed_paths': [path]}],
    }]
    cumulative = guard.current_risk(repo, ANCHOR, head)
    assert cumulative['profile'] == 'full'
    assert {row['commit'] for row in cumulative['commit_changes']} == set(checkpoints.values()) | {head}
    assert set(route['changed_paths']) < set(cumulative['changed_paths'])


@pytest.mark.parametrize("case", ["packaged_readme", "executable", "mixed", "candidate_override"])
def test_current_risk_escalates_package_code_and_mixed_changes(repo, case, monkeypatch):
    path = "README.md" if case == "packaged_readme" else "tests/scaffold/test_imports.py"
    expected = {path}
    edit(repo, path)
    if case in {"mixed", "candidate_override"}:
        expected.add("phase4/implementation_evidence.json")
        if case == "candidate_override":
            (repo / "phase4").mkdir(exist_ok=True)
            (repo / "phase4/implementation_evidence.json").write_text(
                '{"profile":"documentation","authorized":true,"changed_paths":[]}', encoding="utf-8")
            monkeypatch.setenv("SIT_VERIFICATION_PROFILE", "documentation")
            monkeypatch.setenv("SIT_PHASE_UNIT", "P3-W15")
        else:
            edit(repo, "phase4/implementation_evidence.json", b"\n")
    head = commit(repo)
    route = guard.current_risk(repo, ENTRY, head)
    assert route["profile"] == "full" and route["reason"] == "non_documentation_paths"
    assert set(route["changed_paths"]) == set(route["net_changed_paths"]) == expected
    assert [row["commit"] for row in route["commit_changes"]] == [head]


def test_current_risk_cannot_hide_executable_change_by_restoring_final_tree(repo):
    path = 'tests/scaffold/test_imports.py'
    original = (repo / path).read_bytes()
    edit(repo, path)
    changed = commit(repo)
    (repo / path).write_bytes(original)
    restored = commit(repo)
    edit(repo, 'phase4/implementation_evidence.json', b'{}\n')
    head = commit(repo)
    route = guard.current_risk(repo, ENTRY, head)
    assert route['net_changed_paths'] == ['phase4/implementation_evidence.json']
    assert route['changed_paths'] == ['phase4/implementation_evidence.json', path]
    assert route['profile'] == 'full' and route['reason'] == 'non_documentation_paths'
    assert [row['commit'] for row in route['commit_changes']] == [changed, restored, head]


def test_current_risk_includes_restored_executable_changes_on_merge_sides(repo):
    path = 'tests/scaffold/test_imports.py'
    record = 'phase4/implementation_evidence.json'
    original = (repo / path).read_bytes()
    git(repo, 'checkout', '--quiet', '-b', 'risk-main')
    edit(repo, record, b'{}\n')
    main = commit(repo)
    git(repo, 'checkout', '--quiet', '-b', 'risk-side', ENTRY)
    edit(repo, path)
    side = commit(repo)
    (repo / path).write_bytes(original)
    restored = commit(repo)
    git(repo, 'checkout', '--quiet', 'risk-main')
    git(repo, 'merge', '--quiet', '--no-ff', 'risk-side', '-m', 'Synthetic risk merge\n\nSIT-Phase-Unit: P4-W01')
    head = git(repo, 'rev-parse', 'HEAD').decode().strip()
    route = guard.current_risk(repo, ENTRY, head)
    assert route['profile'] == 'full' and route['reason'] == 'non_documentation_paths'
    assert route['net_changed_paths'] == [record]
    assert route['changed_paths'] == [record, path]
    assert {row['commit'] for row in route['commit_changes']} == {main, side, restored, head}
    assert route['commit_changes'][-1]['parents'] == [
        {'parent': main, 'changed_paths': []},
        {'parent': restored, 'changed_paths': [record]},
    ]


@pytest.mark.parametrize('case', ['same_endpoint', 'restored_docs'])
def test_current_risk_empty_changes_do_not_claim_documentation_success(repo, case):
    base = advance(repo, 10)[10]
    head = base
    if case == 'restored_docs':
        path = 'phase4/implementation_evidence.json'
        original = (repo / path).read_bytes()
        edit(repo, path, b'\n')
        commit(repo, unit=10)
        (repo / path).write_bytes(original)
        head = commit(repo, unit=10)
    route = guard.current_risk(repo, base, head)
    assert route['profile'] == 'full' and route['reason'] == 'empty_change_set'
    assert route['net_changed_paths'] == []


def test_current_risk_does_not_authorize_unknown_markdown_paths(repo):
    edit(repo, "verification/unreviewed.md")
    head = commit(repo)
    with pytest.raises(ValueError, match="^current_unlisted_path$"):
        guard.current_risk(repo, ENTRY, head)


@pytest.mark.parametrize("case", ["valid_side", "forbidden_side", "pre_anchor_side", "wrong_base"])
def test_current_history_validates_anchor_parents_and_side_branches(repo, case):
    verified(repo)
    git(repo, "checkout", "--quiet", "-b", "mainline")
    edit(repo, "README.md"); main = commit(repo)
    if case == "wrong_base":
        with pytest.raises(ValueError, match="^current_git_unavailable_or_incomplete$"):
            guard.current_history(repo, PARENTS[0], main)
        return
    git(repo, "checkout", "--quiet", "-b", "side", PARENTS[0] if case == "pre_anchor_side" else ENTRY)
    edit(repo, PRODUCT if case == "forbidden_side" else "phase4/implementation_evidence.json")
    side = commit(repo)
    if case == "forbidden_side":
        git(repo, "checkout", ENTRY, "--", PRODUCT); commit(repo)
    git(repo, "checkout", "--quiet", "mainline")
    git(repo, "merge", "--quiet", "--no-ff", "side", "-m", "Synthetic side merge\n\nSIT-Phase-Unit: P4-W01")
    head = git(repo, "rev-parse", "HEAD").decode().strip()
    if case == "valid_side":
        rows = guard.current_history(repo, ANCHOR, head)
        assert {r["commit"] for r in rows} == {ENTRY, main, side, head}
        assert rows[-1]["parents"] == [main, side]
    else:
        with pytest.raises(ValueError, match="^" + ("current_premature_activation" if case == "forbidden_side"
                                                   else "current_unanchored_parent") + "$"):
            guard.current_history(repo, ANCHOR, head)


def batch_record(root, oid):
    body = git(root, "cat-file", "commit", oid)
    return oid.encode() + b" commit " + str(len(body)).encode() + b"\n" + body + b"\n"


@pytest.mark.parametrize('target', ['root', 'nested'])
def test_current_tree_objects_reject_hash_inconsistent_bodies(repo, monkeypatch, target):
    baseline, blobs = guard.current_authority(repo)
    assert len(baseline) == 211
    assert guard._current_snapshot(repo, ANCHOR) == baseline
    assert {path.removeprefix('src/source_integrity_toolkit/'): hashlib.sha256(blobs[oid]).hexdigest()
            for path, (_, oid) in baseline.items() if path.startswith('src/')} == SOURCE_SHA256
    oid = TREE if target == 'root' else git(repo, 'rev-parse', ANCHOR + ':src').decode().strip()
    body = git(repo, 'cat-file', 'tree', oid)
    assert body
    changed_body = body[:-1] + bytes([body[-1] ^ 1])
    prefix = oid.encode() + b' tree ' + str(len(body)).encode() + b'\n'
    original_record = prefix + body + b'\n'
    changed_record = prefix + changed_body + b'\n'
    assert len(changed_record) == len(original_record) and changed_record != original_record
    original_git = guard._current_git
    changed_responses = []

    def corrupted_tree(root, *args, input_bytes=None):
        raw = original_git(root, *args, input_bytes=input_bytes)
        if args == ('cat-file', '--batch') and oid.encode() in input_bytes.splitlines():
            assert raw.count(original_record) == 1
            changed_responses.append(oid)
            return raw.replace(original_record, changed_record, 1)
        return raw

    monkeypatch.setattr(guard, '_current_git', corrupted_tree)
    with pytest.raises(ValueError, match='^current_git_object_hash_mismatch$'):
        guard.current_authority(repo)
    assert changed_responses == [oid]


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
                ENTRY: {"tree": ENTRY_TREE, "parents": [ANCHOR]}}
    for oid, metadata in expected.items():
        metadata['message'] = git(repo, 'cat-file', 'commit', oid).partition(b'\n\n')[2].decode('utf-8')
    assert guard.current_commit_metadata(repo, [ANCHOR, ENTRY]) == expected
    first, second = batch_record(repo, ANCHOR), batch_record(repo, ENTRY)
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
        guard.current_commit_metadata(repo, [ANCHOR, ENTRY])


@pytest.mark.parametrize("case,reason", [
    ("invalid_tree", "current_invalid_commit_tree"),
    ("invalid_parent", "current_invalid_commit_parent"),
    ("duplicate_parent", "current_invalid_commit_parent"),
    ("duplicate_tree", "current_malformed_commit_headers"),
    ("late_parent", "current_malformed_commit_headers"),
    ("missing_separator", "current_malformed_commit"),
])
def test_current_git_metadata_rejects_hash_valid_malformed_commit_headers(repo, monkeypatch, case, reason):
    body = git(repo, "cat-file", "commit", ANCHOR)
    header, separator, message = body.partition(b"\n\n")
    assert guard.current_commit_metadata(repo, [ANCHOR]) == {
        ANCHOR: {"tree": TREE, "parents": PARENTS, "message": message.decode('utf-8')}}
    assert separator and header.startswith(b"tree " + TREE.encode() + b"\n")
    lines = header.split(b"\n")
    assert lines[1:3] == [b"parent " + parent.encode() for parent in PARENTS]
    if case == "invalid_tree": lines[0] = b"tree invalid-object-id"
    elif case == "invalid_parent": lines[1] = b"parent invalid-object-id"
    elif case == "duplicate_parent": lines.insert(2, lines[1])
    elif case == "duplicate_tree": lines.insert(3, lines[0])
    elif case == "late_parent": lines.append(lines.pop(1))
    changed = b"\n".join(lines)
    if case != "missing_separator": changed += b"\n\n" + message
    # The response is internally hash-valid, so rejection must come from the
    # commit grammar rather than merely detecting tampered object bytes.
    oid = hashlib.sha1(b"commit " + str(len(changed)).encode() + b"\0" + changed).hexdigest()
    raw = oid.encode() + b" commit " + str(len(changed)).encode() + b"\n" + changed + b"\n"
    monkeypatch.setattr(guard, "_current_git", lambda *args, **kwargs: raw)
    with pytest.raises(ValueError, match="^" + reason + "$"):
        guard.current_commit_metadata(repo, [oid])


@pytest.mark.parametrize("commit_ids,reason", [
    ([ANCHOR[:12]], "current_invalid_object_request"), ([123], "current_invalid_object_request"),
    ([ANCHOR.upper()], "current_invalid_object_request"), (ANCHOR, "current_invalid_object_request"),
    ([ANCHOR, ANCHOR], "current_duplicate_object_request"),
    ({ANCHOR}, "current_invalid_object_request"),
])
def test_current_git_metadata_invalid_requests_do_not_launch_git(monkeypatch, commit_ids, reason):
    def unexpected(*args, **kwargs):
        raise AssertionError("invalid request must not launch Git")
    monkeypatch.setattr(guard, "_current_git", unexpected)
    assert guard.current_commit_metadata(ROOT, []) == {}
    assert guard.current_commit_metadata(ROOT, ()) == {}
    with pytest.raises(ValueError, match="^" + reason + "$"):
        guard.current_commit_metadata(ROOT, commit_ids)


def test_current_git_metadata_rereads_root_and_state(repo, tmp_path, monkeypatch):
    verified(repo)
    other = tmp_path / "other"
    git(tmp_path, "clone", "--quiet", "--no-hardlinks", str(repo), str(other))
    verified(other)
    git(other, "replace", ENTRY, ANCHOR)
    with pytest.raises(ValueError, match="^current_replaced_history$"):
        guard.current_history(other, ANCHOR, ENTRY)
    # No cached result and no ambient GIT_DIR redirect may validate another root.
    monkeypatch.setenv("GIT_DIR", str(other / ".git"))
    verified(repo)
    git(other, "replace", "-d", ENTRY)
    verified(other)
    (other / ".git/shallow").write_text(ENTRY + "\n", encoding="ascii")
    with pytest.raises(ValueError, match="^current_shallow_history$"):
        guard.current_history(other, ANCHOR, ENTRY)


@pytest.mark.parametrize("case,reason", [
    ("shallow", "current_shallow_history"), ("replace", "current_replaced_history"),
    ("graft", "current_grafted_history"), ("missing_commit", "current_git_unavailable_or_incomplete"),
    ("missing_tree", "current_malformed_object_record"),
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
    monkeypatch.setattr(guard, "P4_ACCEPTED_PARENTS", tuple(reversed(PARENTS)))
    with pytest.raises(ValueError, match="^current_accepted_anchor_mismatch$"):
        guard.current_history(repo, ANCHOR, ENTRY)


@pytest.mark.parametrize('footer', [
    '', 'SIT-Phase-Unit: P4-W01 ', 'SIT-Phase-Unit: P4-W01 injected',
    'SIT-Phase-Unit: P4-W00', 'SIT-Phase-Unit: P4-W11',
    'SIT-Phase-Unit: P4-W01\nSIT-Phase-Unit: P4-W01',
    'SIT-Phase-Unit: P4-W01\nSIT-Verification-Unit: VC',
    'SIT-Phase-Unit: P4-W01\nSIT-Phase-Unit: P3-W15',
])
def test_actual_commit_footer_cannot_be_replaced_by_candidate_claims(repo, footer, monkeypatch):
    verified(repo)
    git(repo, 'commit', '--quiet', '--amend', '--cleanup=verbatim',
        '-m', 'Synthetic bad footer\n\n' + footer)
    head = git(repo, 'rev-parse', 'HEAD').decode().strip()
    assert git(repo, 'cat-file', 'commit', head).partition(b'\n\n')[2].decode('utf-8') == (
        'Synthetic bad footer\n\n' + footer + ('\n' if footer else ''))
    candidate = event(head)
    candidate['pull_request']['title'] = 'SIT-Phase-Unit: P4-W01'
    candidate['approved_unit'] = 'P4-W01'
    monkeypatch.setenv('SIT_PHASE_UNIT', 'P4-W01')
    with pytest.raises(ValueError, match='^current_invalid_commit_footer$'):
        guard.current_context('pull_request', json.dumps(candidate), head, root=repo)
    with pytest.raises(ValueError, match='^current_invalid_commit_footer$'):
        guard.current_context('push', json.dumps(push_event(repo, head)), head, root=repo)


@pytest.mark.parametrize('path,first_stage', sorted(ACTIVATION.items()))
def test_all_twelve_product_activation_boundaries_are_independent(repo, path, first_stage):
    baseline, blobs = guard.current_authority(repo)
    actual = guard._current_snapshot(repo, ENTRY)
    blobs.update(guard._current_objects(repo, [actual[PLAN][1]], 'blob'))
    guard.current_scope(baseline, actual, blobs.__getitem__, stage=first_stage - 1)
    relative = 'src/source_integrity_toolkit/' + path
    original = blobs[actual[relative][1]]
    changed = original + b'\n# synthetic authorized declaration review\n'
    oid = guard.git_blob(changed)
    blobs[oid] = changed
    actual[relative] = ('100644', oid)
    with pytest.raises(ValueError, match='^current_premature_activation$'):
        guard.current_scope(baseline, actual, blobs.__getitem__, stage=first_stage - 1)
    guard.current_scope(baseline, actual, blobs.__getitem__, stage=first_stage)


@pytest.mark.parametrize('unit,path', [
    (1, 'src/source_integrity_toolkit/contracts/report.py'),
    (2, 'README.md'), (3, 'README.md'), (4, 'README.md'),
    (5, 'README.md'), (6, 'README.md'), (7, 'README.md'),
    (8, 'src/source_integrity_toolkit/reporting/json_report.py'),
    (9, 'README.md'), (10, 'src/source_integrity_toolkit/contracts/report.py'),
])
def test_each_unit_rejects_paths_owned_by_another_approved_unit(repo, unit, path):
    checkpoints = advance(repo, unit)
    before = checkpoints[unit]
    rows = guard.current_history(repo, ANCHOR, before)
    assert rows[-1]['activation_stage'] == unit
    assert path in SCOPES and path not in UNIT_PATHS[unit]
    edit(repo, path)
    head = commit(repo, unit=unit)
    reason = 'current_premature_activation' if unit == 1 else 'current_unit_path_not_allowed'
    with pytest.raises(ValueError, match='^' + reason + '$'):
        guard.current_history(repo, ANCHOR, head)


@pytest.mark.parametrize('reached,skipped', [(1, 3), (1, 10), (2, 4), (7, 9)])
def test_first_units_cannot_skip_their_predecessors(repo, reached, skipped):
    checkpoints = advance(repo, reached)
    assert guard.current_history(repo, ANCHOR, checkpoints[reached])[-1]['activation_stage'] == reached
    edit(repo, 'phase4/implementation_evidence.json', b'\n')
    head = commit(repo, unit=skipped)
    with pytest.raises(ValueError, match='^current_unit_out_of_order$'):
        guard.current_history(repo, ANCHOR, head)


def test_later_repair_keeps_monotonic_activation_and_exact_owner(repo):
    checkpoints = advance(repo, 8)
    before = guard.current_history(repo, ANCHOR, checkpoints[8])
    assert [row['activation_stage'] for row in before] == list(range(1, 9))
    edit(repo, 'src/source_integrity_toolkit/contracts/report.py')
    repair = commit(repo, 'Synthetic W02 repair after W08', unit=2)
    rows = guard.current_history(repo, ANCHOR, repair)
    assert rows[-1]['owner_unit'] == 'P4-W02'
    assert rows[-1]['activation_stage'] == 8
    context = guard.current_context('pull_request', json.dumps(event(repair)), repair, root=repo)
    assert context['unit'] == 'P4-W02' and context['activation_stage'] == 8
    # W02 ownership cannot borrow a different already-active product path.
    edit(repo, 'src/source_integrity_toolkit/reporting/json_report.py')
    bad = commit(repo, unit=2)
    with pytest.raises(ValueError, match='^current_unit_path_not_allowed$'):
        guard.current_history(repo, ANCHOR, bad)


def test_final_normal_merge_inherits_verified_candidate_without_w10_path_expansion(repo):
    checkpoints = advance(repo, 9)
    # A real earlier-owner product change is inherited by the W10 merge.
    edit(repo, 'src/source_integrity_toolkit/contracts/report.py')
    repaired = commit(repo, 'Synthetic approved-scope W02 repair', unit=2)
    assert guard.current_history(repo, ANCHOR, repaired)[-1]['activation_stage'] == 9
    edit(repo, 'phase4/implementation_evidence.json', b'\n')
    candidate = commit(repo, unit=10)
    candidate_tree = git(repo, 'rev-parse', candidate + '^{tree}').decode().strip()
    assert guard.current_history(repo, ANCHOR, candidate)[-1]['activation_stage'] == 10
    git(repo, 'checkout', '--quiet', '--detach', ANCHOR)
    git(repo, 'merge', '--quiet', '--no-ff', candidate, '-m',
        'Synthetic accepted candidate merge\n\nSIT-Phase-Unit: P4-W10')
    merged = git(repo, 'rev-parse', 'HEAD').decode().strip()
    assert git(repo, 'rev-parse', merged + '^{tree}').decode().strip() == candidate_tree
    rows = guard.current_history(repo, ANCHOR, merged)
    assert rows[-1]['parents'] == [ANCHOR, candidate]
    assert rows[-1]['owner_unit'] == 'P4-W10' and rows[-1]['activation_stage'] == 10
    assert set(checkpoints.values()) | {repaired, candidate, merged} == {row['commit'] for row in rows}
    context = guard.current_context('push', json.dumps(push_event(repo, merged)), merged, root=repo)
    assert context == {'unit': 'P4-W10', 'activation_stage': 10,
                       'base': ANCHOR, 'head': merged, 'event': 'push'}
    # New merge bytes are not inherited authority, even at an active path.
    edit(repo, 'src/source_integrity_toolkit/contracts/report.py')
    git(repo, 'add', '-A')
    git(repo, 'commit', '--quiet', '--amend', '--no-edit')
    changed_merge = git(repo, 'rev-parse', 'HEAD').decode().strip()
    with pytest.raises(ValueError, match='^current_unit_path_not_allowed$'):
        guard.current_history(repo, ANCHOR, changed_merge)
    with pytest.raises(ValueError, match='^current_merge_candidate_tree_mismatch$'):
        guard.current_context('push', json.dumps(push_event(repo, changed_merge)), changed_merge, root=repo)
    # A third parent cannot be passed off as the normal main-branch merge,
    # even when its result exactly inherits the verified candidate tree.
    octopus = git(repo, 'commit-tree', candidate_tree, '-p', ANCHOR, '-p', candidate, '-p', repaired,
                  '-m', 'Synthetic octopus merge\n\nSIT-Phase-Unit: P4-W10').decode().strip()
    assert git(repo, 'rev-parse', octopus + '^{tree}').decode().strip() == candidate_tree
    with pytest.raises(ValueError, match='^current_invalid_main_merge$'):
        guard.current_context('push', json.dumps(push_event(repo, octopus)), octopus, root=repo)


def test_two_ordered_branches_cannot_combine_to_authorize_skipped_unit(repo):
    verified(repo)
    git(repo, 'checkout', '--quiet', '-b', 'order-main')
    main = advance(repo, 2)[2]
    assert guard.current_history(repo, ANCHOR, main)[-1]['activation_stage'] == 2
    git(repo, 'checkout', '--quiet', '-b', 'order-side', ENTRY)
    edit(repo, 'tests/contract/test_report_identity.py', b'# synthetic scope test\n')
    side = commit(repo, unit=3)
    with pytest.raises(ValueError, match='^current_unit_out_of_order$'):
        guard.current_history(repo, ANCHOR, side)
    git(repo, 'checkout', '--quiet', 'order-main')
    git(repo, 'merge', '--quiet', '--no-ff', 'order-side', '-m',
        'Synthetic falsely ordered merge\n\nSIT-Phase-Unit: P4-W03')
    merged = git(repo, 'rev-parse', 'HEAD').decode().strip()
    with pytest.raises(ValueError, match='^current_unit_out_of_order$'):
        guard.current_history(repo, ANCHOR, merged)
