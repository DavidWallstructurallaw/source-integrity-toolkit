# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Current explicit workflow tests and a repository-only CI evidence driver.

The workflow is JSON-form YAML to permit strict standard-library inspection.
No product code imports this file. Network access is confined to the explicitly
selected CI dependency acquisition stage, never to an audit operation.
Historical stage helpers remain until VC-04; the CI-context switch is VC-05.
"""

from __future__ import annotations

import copy
import ast
import io
from email.parser import BytesParser
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys
import tarfile
import unittest
import urllib.request
import xml.etree.ElementTree as ET
import zipfile

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT))
from tools import check_scaffold_boundary as phase_guard

WORKFLOW = ".github/workflows/phase1-ci.yml"

CHECKOUT = "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1"

PYTHON = "actions/setup-python@5fda3b95a4ea91299a34e894583c3862153e4b97"

UPLOAD = "actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a"

HEAD = "${{ github.event.pull_request.head.sha || github.sha }}"

DRIVER = "python -B tests/scaffold/test_ci_contract.py --ci-stage "

SELECTED = {"setuptools": "84.0.0", "pytest": "9.1.1", "iniconfig": "2.3.0",
            "packaging": "25.0", "pluggy": "1.6.0", "pygments": "2.20.0"}

DIRECT_HASHES = {
    "setuptools": "51a52592b3b99e102b609654876bd65f19f999935166d1352678931132b0c670",
    "pytest": "37a86b45efb9a47a61a36449063e8e18d0cab3161329fc099eb21783169c4f0c",
}

SCOPES = ["tests/scaffold", "tests/security"]

def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)

def unique(pairs):
    result = {}
    for key, value in pairs:
        require(key not in result, "duplicate_json_key")
        result[key] = value
    return result

def read_workflow() -> dict:
    return json.loads((ROOT / WORKFLOW).read_text(encoding="utf-8"), object_pairs_hook=unique)

class CiContractTests(unittest.TestCase):
    def altered(self, mutate):
        value = copy.deepcopy(read_workflow())
        mutate(value)
        with self.assertRaises(ValueError):
            policy(value)

    def test_workflow_is_closed_and_minimal(self):
        policy(read_workflow())

    def test_duplicate_keys_fail(self):
        with self.assertRaises(ValueError):
            json.loads('{"permissions":{},"permissions":{"contents":"write"}}', object_pairs_hook=unique)

    def test_write_permission_fails(self):
        self.altered(lambda v: v["permissions"].update(contents="write"))

    def test_privileged_trigger_fails(self):
        self.altered(lambda v: v["on"].update(pull_request_target={}))

    def test_mutable_action_pin_fails(self):
        self.altered(lambda v: v["jobs"]["scaffold"]["steps"][0].update(uses="actions/checkout@main"))

    def test_saved_checkout_credentials_fail(self):
        self.altered(lambda v: v["jobs"]["scaffold"]["steps"][0]["with"].update({"persist-credentials": True}))

    def test_missing_platform_fails(self):
        self.altered(lambda v: v["jobs"]["scaffold"]["strategy"]["matrix"].update(os=["ubuntu-24.04"]))

    def test_missing_lower_bound_fails(self):
        self.altered(lambda v: v["jobs"]["scaffold"]["strategy"]["matrix"].update(python=["3.13"]))

    def test_skipped_test_step_fails(self):
        self.altered(lambda v: v["jobs"]["scaffold"]["steps"][4].update({"if": "false"}))

    def test_ignored_failure_fails(self):
        self.altered(lambda v: v["jobs"]["scaffold"].update({"continue-on-error": True}))

    def test_untrusted_shell_expression_fails(self):
        self.altered(lambda v: v["jobs"]["scaffold"]["steps"][4].update(run="echo '${{ github.event.pull_request.title }}'"))

    def test_broad_artifact_upload_fails(self):
        self.altered(lambda v: v["jobs"]["scaffold"]["steps"][6]["with"].update(path="."))

    def test_cache_or_secret_injection_fails(self):
        self.altered(lambda v: v["jobs"]["scaffold"]["env"].update(TOKEN="${{ secrets.DEPLOY_KEY }}"))

    def test_missing_guard_stage_fails(self):
        self.altered(lambda v: v["jobs"]["scaffold"]["steps"].pop(2))

def junit_counts(xml_bytes: bytes, collected_nodes: list[str]) -> dict:
    """Match top-level outcomes to collection while retaining all failure events.

    Pytest 9.1 includes successful unittest subtest events in the suite's tests
    attribute but does not emit a separate testcase element for each of them.
    Keep that aggregate separate from actual collected top-level test instances.
    """
    root = ET.fromstring(xml_bytes)
    require(root.tag == "testsuites", "unexpected JUnit root")
    suites = list(root)
    require(bool(suites) and all(s.tag == "testsuite" for s in suites), "JUnit suites missing")
    totals = {key: sum(int(s.attrib[key]) for s in suites)
              for key in ("tests", "failures", "errors", "skipped")}
    require(all(value >= 0 for value in totals.values()), "negative JUnit count")
    expected = []
    for node in collected_nodes:
        parts = node.split("::")
        require(len(parts) >= 2 and parts[0].endswith(".py"), "bad collected node")
        classname = parts[0][:-3].replace("/", ".")
        if len(parts) > 2:
            classname += "." + ".".join(parts[1:-1])
        expected.append((classname, parts[-1]))
    require(bool(expected) and len(set(expected)) == len(expected), "ambiguous collection identity")
    cases = list(root.iter("testcase"))
    actual = [(case.get("classname"), case.get("name")) for case in cases]
    require(len(actual) == len(expected) and len(set(actual)) == len(actual) and
            set(actual) == set(expected), "JUnit does not cover exact collected test identities")
    require(totals["tests"] >= len(cases), "JUnit aggregate smaller than top-level results")
    failed = sum(case.find("failure") is not None for case in cases)
    errored = sum(case.find("error") is not None for case in cases)
    skipped = sum(case.find("skipped") is not None for case in cases)
    return {"tests": len(cases), "reported_test_events": totals["tests"],
            "additional_reported_events": totals["tests"] - len(cases),
            "failures": max(totals["failures"], failed),
            "errors": max(totals["errors"], errored),
            "skipped": max(totals["skipped"], skipped),
            "top_level_failures": failed, "top_level_errors": errored,
            "top_level_skipped": skipped, "collection_identities_match": True}

class JunitAccountingTests(unittest.TestCase):
    NODE = "tests/scaffold/test_example.py::Example::test_one"

    def document(self, aggregate=4, failures=0, child=""):
        return (f'<testsuites><testsuite tests="{aggregate}" failures="{failures}" errors="0" skipped="0">'
                '<testcase classname="tests.scaffold.test_example.Example" name="test_one">'
                + child + '</testcase></testsuite></testsuites>').encode()

    def test_subtest_aggregate_does_not_inflate_top_level_count(self):
        result = junit_counts(self.document(), [self.NODE])
        self.assertEqual(result["tests"], 1)
        self.assertEqual(result["reported_test_events"], 4)
        self.assertEqual(result["additional_reported_events"], 3)
        self.assertEqual(result["failures"], 0)

    def test_subtest_failure_in_suite_cannot_be_lost(self):
        result = junit_counts(self.document(failures=1), [self.NODE])
        self.assertEqual(result["failures"], 1)

    def test_failure_element_overrides_false_zero_header(self):
        result = junit_counts(self.document(child='<failure message="canary"/>'), [self.NODE])
        self.assertEqual(result["failures"], 1)

    def test_missing_collected_result_is_rejected(self):
        with self.assertRaises(ValueError):
            junit_counts(self.document(), [self.NODE, self.NODE.replace("test_one", "test_two")])

    def test_unknown_or_duplicate_test_identity_is_rejected(self):
        with self.assertRaises(ValueError):
            junit_counts(self.document().replace(b"test_one", b"test_other"), [self.NODE])
        with self.assertRaises(ValueError):
            junit_counts(self.document(), [self.NODE, self.NODE])

    def test_invalid_aggregate_and_skipped_child_do_not_pass(self):
        with self.assertRaises(ValueError):
            junit_counts(self.document(aggregate=0), [self.NODE])
        result = junit_counts(self.document(child='<skipped message="canary"/>'), [self.NODE])
        self.assertEqual(result["skipped"], 1)

def save(path: Path, data) -> None:
    path.write_bytes((json.dumps(data, indent=2, sort_keys=True) + "\n").encode("utf-8"))

def run(args, evidence: Path, name: str, *, env=None, timeout=180, check=True):
    result = subprocess.run([str(a) for a in args], cwd=ROOT, env=env, capture_output=True,
                            text=True, encoding="utf-8", errors="replace", timeout=timeout)
    (evidence / (name + ".log")).write_bytes((result.stdout + result.stderr).encode("utf-8"))
    print(name + ": exit=" + str(result.returncode), flush=True)
    print(result.stdout[-6000:] + result.stderr[-6000:], flush=True)
    if check:
        require(result.returncode == 0, name + " failed; full output preserved")
    return result

def tracked_bytes() -> dict:
    names = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT).decode("utf-8").split("\0")
    return {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in names if name}

def tool_python(base: Path) -> Path:
    return base / "tools" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")

def prepare(base: Path, evidence: Path) -> None:
    run([sys.executable, "-m", "venv", str(base / "tools")], evidence, "venv")
    python = tool_python(base)
    run([python, "-m", "pip", "--version"], evidence, "pip-version")
    wheels = base / "wheelhouse"
    run([python, "-m", "pip", "--isolated", "download", "--index-url", "https://pypi.org/simple",
         "--only-binary=:all:", "--no-cache-dir", "--retries", "2", "--timeout", "30",
         "--dest", wheels, "-r", "requirements-dev.txt"], evidence, "download", timeout=300)
    selected = dict(SELECTED)
    if os.name == "nt":
        selected["colorama"] = "0.4.6"
    reviewed = []
    seen = set()
    for wheel in sorted(wheels.glob("*.whl")):
        raw = wheel.read_bytes()
        digest = hashlib.sha256(raw).hexdigest()
        with zipfile.ZipFile(wheel) as archive:
            members = archive.namelist()
            metas = [n for n in members if n.endswith(".dist-info/METADATA") and n.count("/") == 1]
            require(len(metas) == 1, "wheel metadata shape")
            meta = BytesParser().parsebytes(archive.read(metas[0]))
            name, version = meta["Name"].lower(), meta["Version"]
            require(name in selected and version == selected[name] and name not in seen, "unselected development wheel")
            seen.add(name)
            if name in DIRECT_HASHES:
                require(digest == DIRECT_HASHES[name], "previously selected wheel hash changed")
            url = "https://pypi.org/pypi/" + name + "/" + version + "/json"
            with urllib.request.urlopen(url, timeout=30) as response:
                upstream = json.load(response)
            files = [f for f in upstream["urls"] if f["filename"] == wheel.name]
            require(len(files) == 1 and not files[0]["yanked"], "unavailable/yanked wheel")
            require(files[0]["digests"]["sha256"] == digest and files[0]["size"] == len(raw), "PyPI wheel identity")
            notices = [{"path": n, "sha256": hashlib.sha256(archive.read(n)).hexdigest()}
                for n in members if not n.endswith("/") and
                any(part.lower().startswith(("license", "copying", "notice")) for part in n.split("/"))]
            require(bool(notices), "license/notice material absent")
            vendors = []
            for n in members:
                if "/_vendor/" in n and n.endswith(".dist-info/METADATA"):
                    vm = BytesParser().parsebytes(archive.read(n))
                    vendors.append({"name": vm["Name"], "version": vm["Version"],
                                    "license": vm.get("License-Expression") or vm.get("License")})
            reviewed.append({"name": name, "version": version, "filename": wheel.name, "sha256": digest,
                "bytes": len(raw), "upstream": url, "requires_python": meta.get("Requires-Python"),
                "requires_dist": meta.get_all("Requires-Dist", []), "notices": notices,
                "license": meta.get("License-Expression") or meta.get("License"), "vendored_metadata": vendors})
    require(seen == set(selected), "development wheel set incomplete")
    save(evidence / "reviewed-wheels.json", reviewed)
    run([python, "-m", "pip", "--isolated", "install", "--no-index", "--find-links", wheels,
         "--no-cache-dir", "--report", evidence / "install-report.json", "-r", "requirements-dev.txt"],
        evidence, "install", timeout=300)
    run([python, "-m", "pip", "--isolated", "check"], evidence, "pip-check")
    result = run([python, "-m", "pip", "--isolated", "list", "--format=json"], evidence, "installed")
    installed = {r["name"].lower(): r["version"] for r in json.loads(result.stdout)}
    require({k: v for k, v in installed.items() if k != "pip"} == selected, "installed tool set mismatch")
    save(evidence / "installed.json", installed)


ALL_SCOPES = ("tests/scaffold", "tests/security", "tests/contract", "tests/unit", "tests/integration")


# Explicit owner-approved P2-W02-R01. These two paths supplement only W02's
# immediate diff. Cumulative accounting retains them after W02, without giving
# later units a new permission to edit either path. No metadata selects extras.
P2_W02_R01_PATHS = frozenset((
    "tests/security/test_scaffold_inertness.py",
    "tests/scaffold/test_ci_contract.py",
))


# Explicit owner-approved P2-W04-R01: fixed cycle qualifier and scope tests.
# Only W04 receives immediate permission; no candidate metadata adds paths.
P2_W04_R01_PATHS = frozenset((
    "src/source_integrity_toolkit/contracts/execution.py",
    "src/source_integrity_toolkit/runtime/diagnostics.py",
    "tests/scaffold/test_ci_contract.py",
    "tests/contract/test_bundle_contract.py",
))

# Explicit owner-approved P2-W05-R01: capture-test retargeting only.
# These five paths extend W05 immediate scope, never another unit's scope.
P2_W05_R01_PATHS = frozenset((
    "tests/unit/test_input_decoding.py",
    "tests/unit/test_value_capture.py",
    "tests/security/test_input_capture.py",
    "tests/scaffold/test_ci_contract.py",
    "phase2/transition_ledger.md",
))

# Explicit owner-approved P2-W05-R02: the live W02 coverage-status assertion.
# Only this one additional path is authorized; older exceptions stay separate.
P2_W05_R02_PATHS = frozenset(("tests/contract/test_input_schema_mapping.py",))

# Explicit owner-approved P2-W07-R01: phase-context metadata and scope tests.
# Only W07 gains these immediate paths; later units retain cumulative history.
P2_W07_R01_PATHS = frozenset((
    "phase2/module_policy.json",
    "tests/scaffold/test_ci_contract.py",
    "tests/contract/test_bundle_contract.py",
    "tests/security/test_input_capture.py",
    "tests/contract/test_input_schema_mapping.py",
    "phase2/transition_ledger.md",
))

# Explicit owner-approved P2-W08-R01: exact W08 transition only.
# Other units retain their own immediate scopes; history stays cumulative.
P2_W08_R01_PATHS = frozenset((
    "phase2/module_policy.json",
    "tests/contract/test_bundle_contract.py",
    "tests/security/test_input_capture.py",
    "tests/contract/test_input_schema_mapping.py",
    "tests/contract/test_phase2_transition.py",
    "tests/security/test_preparation_inertness.py",
    "phase2/transition_ledger.md",
))

# Explicit owner-approved P2-W09-R01: final handoff context only.
# Only W09 gains these immediate paths; all earlier scopes remain exact.
P2_W09_R01_PATHS = frozenset((
    "phase2/module_policy.json",
    "tests/scaffold/test_ci_contract.py",
    "tests/contract/test_bundle_contract.py",
    "tests/security/test_input_capture.py",
    "tests/contract/test_input_schema_mapping.py",
    "tests/contract/test_phase2_transition.py",
    "phase2/transition_ledger.md",
))

def effective_paths(paths, unit, *, cumulative=False):
    current = phase_guard.unit_number(unit)
    steps = range(1, current + 1) if cumulative else (current,)
    allowed = set()
    for step in steps:
        allowed.update(paths[f"P2-W{step:02}"])
        if step == 2:
            allowed.update(P2_W02_R01_PATHS)
        if step == 4:
            allowed.update(P2_W04_R01_PATHS)
        if step == 5:
            allowed.update(P2_W05_R01_PATHS)
            allowed.update(P2_W05_R02_PATHS)
        if step == 7:
            allowed.update(P2_W07_R01_PATHS)
        if step == 8:
            allowed.update(P2_W08_R01_PATHS)
        if step == 9:
            allowed.update(P2_W09_R01_PATHS)
    return frozenset(allowed)


def check_changed_paths(paths, unit, changed):
    require(changed <= effective_paths(paths, unit), "work_unit_allowlist_exceeded")


# Approved P3-W04-R01: two inherited inert-slot controls, their independent
# regression tests, this driver's exact exception and the append-only ledger.
# The original plan and every other unit's immediate permissions stay intact.
P3_W04_R01_PATHS = frozenset((
    "tests/scaffold/test_no_runtime_implementation.py",
    "tests/scaffold/test_ci_contract.py",
    "tests/contract/test_phase3_transition.py",
    "phase3/transition_ledger.md",
))
P3_W04_R01_BASE = "879b67b7066690ab0bee8cef569aa8869f78af03"
P3_W04_R01_BASE_TREE = "f7c92b34537b8fc089c8624af9da6ec9dea74a68"
P3_W04_R01_PREDECESSOR = "b932bef422b4ec67b1b313ecae51b0f7e48d72a2"


# Approved P3-W05-R01: one historical inert-slot manifest control, its
# independent regression tests, this exact exception and the appended ledger.
# Earlier W05 commits retain the original nine-path scope.
P3_W05_R01_PATHS = frozenset((
    "tests/scaffold/test_module_manifest.py",
    "tests/scaffold/test_ci_contract.py",
    "tests/contract/test_phase3_transition.py",
    "phase3/transition_ledger.md",
))
P3_W05_R01_BASE = "a2aa2112231ba7595070216e659798130127dc3c"
P3_W05_R01_BASE_TREE = "d468e02fa40a5014e838937486fa49185bc1e72d"
P3_W05_R01_PREDECESSOR = "a175d6d4b4153ddc9147301f9db8d247d12e4852"


P3_W06_R01_PATHS = frozenset((
    "src/source_integrity_toolkit/analysis/inventory.py",
    "tests/scaffold/test_ci_contract.py",
    "tests/contract/test_phase3_transition.py",
    "phase3/transition_ledger.md",
))
P3_W06_R01_BASE = "5dbf39949b8fca63e5abad87b32578b61df87b80"
P3_W06_R01_BASE_TREE = "5cbb23c0b1f2cc65656fca813ca7b90b36274bfa"
P3_W06_R01_PREDECESSOR = "3dd10f987816dffd73e56631b1c4593e9c3f1b54"


def phase3_effective_paths(paths, unit, *, cumulative=False):
    """Phase 3 scopes are separate from the unchanged historical P2 API."""
    current = phase_guard.phase3_unit_number(unit)
    steps = range(1, current + 1) if cumulative else (current,)
    allowed = set()
    for step in steps:
        allowed.update(paths[f"P3-W{step:02}"])
        if step == 4:
            allowed.update(P3_W04_R01_PATHS)
        if step == 5:
            allowed.update(P3_W05_R01_PATHS)
        if step == 6:
            allowed.update(P3_W06_R01_PATHS)
        if step == 8:
            allowed.update(P3_W08_R01_PATHS)
        if step == 9:
            allowed.update(P3_W09_R01_PATHS)
        if step == 11:
            allowed.update(P3_W11_R01_PATHS)
        if step == 15:
            allowed.update(P3_W15_R01_PATHS)
    return frozenset(allowed)


def phase3_scope_exceptions(unit):
    """Name accepted cumulative amendments without granting later edit rights."""
    current = phase_guard.phase3_unit_number(unit)
    return ((["P3-W04-R01"] if current >= 4 else []) + (["P3-W05-R01"] if current >= 5 else []) +
            (["P3-W06-R01"] if current >= 6 else []) + (["P3-W08-R01"] if current >= 8 else []) +
            (["P3-W09-R01"] if current >= 9 else []) + (["P3-W11-R01"] if current >= 11 else []) +
            (["P3-W15-R01"] if current >= 15 else []))


def phase3_check_changed_paths(paths, unit, changed):
    require(changed <= phase3_effective_paths(paths, unit), "work_unit_allowlist_exceeded")


def check_entry_bytes(entry_files, actual, allowed):
    """Check every entry byte outside scope and account for every added path."""
    require(set(entry_files) <= set(actual) <= set(entry_files) | set(allowed), "tracked_path_accounting")
    require(all(actual[p] == h for p, h in entry_files.items() if p not in allowed), "frozen_entry_byte_changed")


def policy(value):
    """Direct current workflow policy; independent of historical test source."""
    phase_guard.current_workflow(value)


def resolve_unit(event_name, event, head):
    """Mechanical unit context from runner event, never candidate metadata."""
    if event_name == "pull_request":
        pr = event["pull_request"]
        require(pr["head"]["sha"] == head, "event_head_mismatch")
        match = re.fullmatch(r"(?:phase2/(p2-w0[1-9])|phase3/(p3-w(?:0[1-9]|1[0-5])))", pr["head"]["ref"])
        require(match is not None, "review_branch_requires_explicit_unit")
        unit = (match[1] or match[2]).upper()
        base = pr["base"]["sha"]
    else:
        require(event_name == "push" and event["ref"] == "refs/heads/main", "unsupported_event")
        require(event["head_commit"]["id"] == head, "event_head_mismatch")
        marks = re.findall(r"^SIT-Phase-Unit:([^\n]*)$", event["head_commit"]["message"], re.M)
        require(len(marks) == 1 and re.fullmatch(r" (?:P2-W0[1-9]|P3-W(?:0[1-9]|1[0-5]))", marks[0]) is not None,
                "main_merge_requires_unit_footer")
        unit, base = marks[0][1:], event["before"]
    require(isinstance(base, str) and re.fullmatch(r"[0-9a-f]{40}", base) is not None, "invalid_base_sha")
    return unit, base


def configure_context():
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_bytes(), object_pairs_hook=unique)
    unit, base = resolve_unit(os.environ["GITHUB_EVENT_NAME"], event, os.environ["SIT_REVIEW_HEAD"])
    require(unit.startswith("P3-"), "current_workflow_requires_phase3_context")
    os.environ["SIT_PHASE_UNIT"] = unit
    return unit, base


def ci_paths():
    require(os.environ.get("GITHUB_ACTIONS") == "true", "explicit Actions invocation required")
    base = Path(os.environ["RUNNER_TEMP"]) / "sit-p3"
    evidence = base / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    return base, evidence


def commit_hashes(commit):
    require(re.fullmatch(r"[0-9a-f]{40}", commit) is not None, "invalid_commit")
    raw = subprocess.check_output(["git", "archive", "--format=tar", commit], cwd=ROOT, timeout=60)
    with tarfile.open(fileobj=io.BytesIO(raw), mode="r:") as archive:
        files = [m for m in archive.getmembers() if not m.isdir()]
        require(all(m.isfile() for m in files), "unexpected_git_object_type")
        require(len({m.name for m in files}) == len(files), "duplicate_git_archive_path")
        return {m.name: hashlib.sha256(archive.extractfile(m).read()).hexdigest() for m in files}


def entry_and_scope(evidence):
    unit, base = configure_context()
    if unit.startswith("P3-"):
        return phase3_entry_and_scope(evidence, unit, base)
    entry = phase_guard.entry_manifest(ROOT)
    paths = phase_guard.plan_paths(ROOT)
    require(commit_hashes(entry["intake_commit"]) == entry["files"], "actual_intake_hash_mismatch")
    original = {p: h for p, h in entry["files"].items() if p != "PHASE_2_PLAN.md"}
    require(len(original) == 124 and commit_hashes(entry["phase1_commit"]) == original, "actual_phase1_hash_mismatch")
    for key, commit_key in (("intake_tree", "intake_commit"), ("phase1_tree", "phase1_commit")):
        actual = subprocess.check_output(["git", "rev-parse", entry[commit_key] + "^{tree}"], cwd=ROOT, text=True).strip()
        require(actual == entry[key], "entry_tree_mismatch")
    changed = subprocess.check_output(["git", "diff", "--name-only", "-z", base, "HEAD"], cwd=ROOT).decode().split("\0")
    changed = {p for p in changed if p}
    check_changed_paths(paths, unit, changed)
    deleted = subprocess.check_output(["git", "diff", "--name-only", "--diff-filter=DR", base, "HEAD"], cwd=ROOT)
    require(not deleted, "deletion_or_rename_not_authorized")
    cumulative = effective_paths(paths, unit, cumulative=True)
    actual = tracked_bytes()
    require(set(entry["files"]) <= set(actual) <= set(entry["files"]) | cumulative, "tracked_path_accounting")
    require(all(actual[p] == h for p, h in entry["files"].items() if p not in cumulative), "frozen_entry_byte_changed")
    old = phase_guard.historical_nodes(ROOT)
    save(evidence / "entry-and-scope.json", {"ok": True, "unit": unit, "base": base,
        "intake_commit": entry["intake_commit"], "actual_entry_files": 125, "actual_phase1_files": 124,
        "changed_paths": sorted(changed), "tracked_files": len(actual), "historical_test_identities": len(old),
        "scope_exceptions": (["P2-W02-R01"] if phase_guard.unit_number(unit) >= 2 else []) +
            (["P2-W04-R01"] if phase_guard.unit_number(unit) >= 4 else []) +
            (["P2-W05-R01", "P2-W05-R02"] if phase_guard.unit_number(unit) >= 5 else []) +
            (["P2-W07-R01"] if phase_guard.unit_number(unit) >= 7 else []) +
            (["P2-W08-R01"] if phase_guard.unit_number(unit) >= 8 else []) +
            (["P2-W09-R01"] if phase_guard.unit_number(unit) >= 9 else []),
        "provenance": "Full local Git commit archives and actual checkout, not substituted artifact metadata"})


def git_text(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True, encoding="utf-8", timeout=60).strip()


def phase3_commit_metadata(commits):
    """Read one ordered batch from Git, with exact rows and terminated fields."""
    require(type(commits) in (list, tuple) and
            all(type(commit) is str and re.fullmatch(r"[0-9a-f]{40}", commit) for commit in commits),
            "invalid_commit_metadata_request")
    require(len(commits) == len(set(commits)), "duplicate_commit_metadata_request")
    if not commits:
        return {}
    output = subprocess.check_output(["git", "show", "--no-walk=unsorted", "-s",
                                      "--format=%H%x00%T%x00%P%x00", *commits],
                                     cwd=ROOT, text=True, encoding="utf-8", timeout=60)
    require(type(output) is str and output.endswith("\n"), "malformed_commit_metadata_batch")
    rows = output.split("\n")[:-1]
    require(len(rows) == len(commits), "incomplete_commit_metadata_batch")
    metadata = {}
    for expected, row in zip(commits, rows):
        fields = row.split("\0")
        require(len(fields) == 4 and fields[3] == "", "malformed_commit_metadata_record")
        commit, tree, parents = fields[:3]
        require(commit == expected and commit not in metadata, "wrong_commit_metadata_identity")
        require(re.fullmatch(r"[0-9a-f]{40}", tree) is not None, "invalid_commit_metadata_tree")
        parents = parents.split(" ") if parents else []
        require(all(re.fullmatch(r"[0-9a-f]{40}", parent) for parent in parents),
                "invalid_commit_metadata_parent")
        metadata[commit] = {"parents": parents, "tree": tree}
    require(set(metadata) == set(commits), "incomplete_commit_metadata_batch")
    return metadata


def changed_between(base, head):
    names = subprocess.check_output(["git", "diff", "--no-renames", "--name-only", "-z", base, head],
                                    cwd=ROOT, timeout=60).decode("utf-8").split("\0")
    deleted = subprocess.check_output(["git", "diff", "--no-renames", "--name-only", "--diff-filter=D", base, head],
                                      cwd=ROOT, timeout=60)
    require(not deleted, "deletion_or_rename_not_authorized")
    return frozenset(name for name in names if name)


def require_ancestor(ancestor, descendant):
    result = subprocess.run(["git", "merge-base", "--is-ancestor", ancestor, descendant],
                            cwd=ROOT, capture_output=True, timeout=60)
    require(result.returncode == 0, "entry_or_predecessor_ancestry_mismatch")


def phase3_w04_pre_amendment(predecessor, successor):
    """Read the fixed failed W04 boundary; candidate records cannot select it."""
    require(predecessor == P3_W04_R01_PREDECESSOR, "w04_repair_predecessor_mismatch")
    require(git_text("rev-parse", P3_W04_R01_BASE + "^{tree}") == P3_W04_R01_BASE_TREE,
            "w04_repair_boundary_tree_mismatch")
    require(git_text("show", "-s", "--format=%P", P3_W04_R01_BASE).split() == [predecessor],
            "w04_repair_boundary_parent_mismatch")
    require_ancestor(P3_W04_R01_BASE, successor)
    return frozenset(git_text("rev-list", predecessor + ".." + P3_W04_R01_BASE).splitlines())


def phase3_w05_pre_amendment(predecessor, successor):
    """Read the fixed records-only W05 boundary, independently of metadata."""
    require(predecessor == P3_W05_R01_PREDECESSOR, "w05_repair_predecessor_mismatch")
    require(git_text("rev-parse", P3_W05_R01_BASE + "^{tree}") == P3_W05_R01_BASE_TREE,
            "w05_repair_boundary_tree_mismatch")
    require(git_text("show", "-s", "--format=%P", P3_W05_R01_BASE).split() == [predecessor],
            "w05_repair_boundary_parent_mismatch")
    require_ancestor(P3_W05_R01_BASE, successor)
    return frozenset(git_text("rev-list", predecessor + ".." + P3_W05_R01_BASE).splitlines())


def phase3_w06_pre_amendment(predecessor, successor):
    """Read the fixed approved W06 boundary, never a candidate declaration."""
    require(predecessor == P3_W06_R01_PREDECESSOR, "w06_repair_predecessor_mismatch")
    require(git_text("rev-parse", P3_W06_R01_BASE + "^{tree}") == P3_W06_R01_BASE_TREE,
            "w06_repair_boundary_tree_mismatch")
    require(git_text("show", "-s", "--format=%P", P3_W06_R01_BASE).split() == [predecessor],
            "w06_repair_boundary_parent_mismatch")
    require_ancestor(P3_W06_R01_BASE, successor)
    return frozenset(git_text("rev-list", predecessor + ".." + P3_W06_R01_BASE).splitlines())


def phase3_history(entry, base, head, paths, unit):
    """Check each accepted unit's entire DAG against that unit's own scope.

    The runner supplies the actual main predecessor. Its first-parent merge
    chain supplies historical boundaries; candidate policy cannot relabel an
    earlier commit using a later unit's cumulative permissions.
    """
    intake = entry["intake_commit"]
    require_ancestor(intake, base)
    require_ancestor(base, head)
    current = phase_guard.phase3_unit_number(unit)
    accepted = git_text("rev-list", "--reverse", "--first-parent", intake + ".." + base).splitlines()
    require(len(accepted) == current - 1, "wrong_phase3_predecessor")
    metadata = phase3_commit_metadata(accepted)
    previous, segments = intake, []
    for step, merge in enumerate(accepted, 1):
        parents = metadata[merge]["parents"]
        require(len(parents) == 2 and parents[0] == previous, "invalid_accepted_merge_chain")
        message = subprocess.check_output(["git", "show", "-s", "--format=%B", merge],
                                          cwd=ROOT, text=True, encoding="utf-8", timeout=60)
        marks = re.findall(r"^SIT-Phase-Unit:([^\n]*)$", message, re.M)
        require(marks == [f" P3-W{step:02}"], "wrong_phase3_predecessor")
        segments.append((previous, merge, f"P3-W{step:02}", False))
        previous = merge
    require(previous == base, "wrong_phase3_predecessor")
    segments.append((base, head, unit, True))
    records = []
    seen = set()
    for predecessor, successor, owner, current_segment in segments:
        immediate = phase3_effective_paths(paths, owner)
        cumulative = phase3_effective_paths(paths, owner, cumulative=True)
        pre_amendment = (phase3_w04_pre_amendment(predecessor, successor)
                         if owner == "P3-W04" else
                         phase3_w05_pre_amendment(predecessor, successor)
                         if owner == "P3-W05" else
                         phase3_w06_pre_amendment(predecessor, successor)
                         if owner == "P3-W06" else frozenset())
        if owner == "P3-W08":
            require(predecessor == P3_W08_R01_PREDECESSOR, "w08_repair_predecessor_mismatch")
            require(git_text("rev-parse", P3_W08_R01_BASE + "^{tree}") == P3_W08_R01_BASE_TREE,
                    "w08_repair_boundary_tree_mismatch")
            # The approved boundary follows two original-scope W08 commits.
            require_ancestor(predecessor, P3_W08_R01_BASE)
            require_ancestor(P3_W08_R01_BASE, successor)
            pre_amendment = frozenset(git_text("rev-list", predecessor + ".." + P3_W08_R01_BASE).splitlines())
        if owner == "P3-W09":
            require(predecessor == P3_W09_R01_PREDECESSOR, "w09_repair_predecessor_mismatch")
            require(git_text("rev-parse", P3_W09_R01_BASE + "^{tree}") == P3_W09_R01_BASE_TREE,
                    "w09_repair_boundary_tree_mismatch")
            require(git_text("show", "-s", "--format=%P", P3_W09_R01_BASE).split() ==
                    ["59a25116bfe5fe8f4f9b407852bb29fa692e542d"], "w09_repair_boundary_parent_mismatch")
            # Both original W09 commits retain their raw seven-path scope.
            require_ancestor(predecessor, P3_W09_R01_BASE)
            require_ancestor(P3_W09_R01_BASE, successor)
            pre_amendment = frozenset(git_text("rev-list", predecessor + ".." + P3_W09_R01_BASE).splitlines())
        if owner == "P3-W11":
            require(predecessor == P3_W11_R01_PREDECESSOR, "w11_repair_predecessor_mismatch")
            require(git_text("rev-parse", P3_W11_R01_BASE + "^{tree}") == P3_W11_R01_BASE_TREE,
                    "w11_repair_boundary_tree_mismatch")
            require(git_text("show", "-s", "--format=%P", P3_W11_R01_BASE).split() ==
                    [P3_W11_R01_PREDECESSOR], "w11_repair_boundary_parent_mismatch")
            require_ancestor(predecessor, P3_W11_R01_BASE)
            require_ancestor(P3_W11_R01_BASE, successor)
            pre_amendment = frozenset(git_text("rev-list", predecessor + ".." + P3_W11_R01_BASE).splitlines())
        if owner == "P3-W15":
            require(predecessor == P3_W15_R01_PREDECESSOR, "w15_repair_predecessor_mismatch")
            require(git_text("rev-parse", P3_W15_R01_BASE + "^{tree}") == P3_W15_R01_BASE_TREE,
                    "w15_repair_boundary_tree_mismatch")
            require(git_text("show", "-s", "--format=%P", P3_W15_R01_BASE).split() ==
                    [P3_W15_R01_PREDECESSOR], "w15_repair_boundary_parent_mismatch")
            require_ancestor(predecessor, P3_W15_R01_BASE)
            require_ancestor(P3_W15_R01_BASE, successor)
            pre_amendment = frozenset(git_text("rev-list", predecessor + ".." + P3_W15_R01_BASE).splitlines())
            require(git_text("rev-parse", P3_W15_R02_BASE + "^{tree}") == P3_W15_R02_BASE_TREE,
                    "w15_r02_boundary_tree_mismatch")
            require(git_text("show", "-s", "--format=%P", P3_W15_R02_BASE).split() ==
                    [P3_W15_R02_PREDECESSOR], "w15_r02_boundary_parent_mismatch")
            require_ancestor(P3_W15_R01_BASE, P3_W15_R02_BASE)
            pre_r02 = frozenset(git_text("rev-list", predecessor + ".." + P3_W15_R02_BASE).splitlines())
            require(git_text("rev-parse", P3_W15_R03_BASE + "^{tree}") == P3_W15_R03_BASE_TREE,
                    "w15_r03_boundary_tree_mismatch")
            require(git_text("show", "-s", "--format=%P", P3_W15_R03_BASE).split() ==
                    [P3_W15_R03_PREDECESSOR], "w15_r03_boundary_parent_mismatch")
            require_ancestor(P3_W15_R02_BASE, P3_W15_R03_BASE)
            pre_r03 = frozenset(git_text("rev-list", predecessor + ".." + P3_W15_R03_BASE).splitlines())
        commits = git_text("rev-list", "--reverse", "--topo-order", predecessor + ".." + successor).splitlines()
        metadata.update(phase3_commit_metadata([commit for commit in commits if commit not in metadata]))
        for commit in commits:
            require(commit not in seen, "duplicate_history_commit")
            seen.add(commit)
            require_ancestor(intake, commit)
            parents = metadata[commit]["parents"]
            require(bool(parents), "unexpected_root_commit")
            changed = changed_between(parents[0], commit)
            # Approval cannot retrospectively bless a pre-amendment unit edit
            # or a side branch that has not descended from the fixed boundary.
            allowed = paths[owner] if commit in pre_amendment else immediate
            if owner == "P3-W04" and commit not in pre_amendment:
                require_ancestor(P3_W04_R01_BASE, commit)
            if owner == "P3-W05" and commit not in pre_amendment:
                require_ancestor(P3_W05_R01_BASE, commit)
            if owner == "P3-W06" and commit not in pre_amendment:
                require_ancestor(P3_W06_R01_BASE, commit)
            if owner == "P3-W08" and commit not in pre_amendment:
                require_ancestor(P3_W08_R01_BASE, commit)
            if owner == "P3-W09" and commit not in pre_amendment:
                require_ancestor(P3_W09_R01_BASE, commit)
            if owner == "P3-W11" and commit not in pre_amendment:
                require_ancestor(P3_W11_R01_BASE, commit)
            if owner == "P3-W15" and commit not in pre_amendment:
                require_ancestor(P3_W15_R01_BASE, commit)
            if owner == "P3-W15" and commit not in pre_r02:
                require_ancestor(P3_W15_R02_BASE, commit)
                allowed = paths[owner] | P3_W15_R02_PATHS
            if owner == "P3-W15" and commit not in pre_r03:
                require_ancestor(P3_W15_R03_BASE, commit)
                allowed = paths[owner] | P3_W15_R03_PATHS
            require(changed <= allowed, "intermediate_work_unit_allowlist_exceeded")
            actual = commit_hashes(commit)
            check_entry_bytes(entry["files"], actual, cumulative)
            records.append({"commit": commit, "tree": metadata[commit]["tree"],
                            "parents": parents, "unit": owner, "accepted_predecessor": predecessor,
                            "segment_successor": successor, "current_unit_segment": current_segment,
                            "immediate_scope_exceptions": (["P3-W04-R01"] if owner == "P3-W04"
                                                           and commit not in pre_amendment else
                                                           ["P3-W05-R01"] if owner == "P3-W05"
                                                           and commit not in pre_amendment else
                                                           ["P3-W06-R01"] if owner == "P3-W06"
                                                           and commit not in pre_amendment else
                                                           ["P3-W08-R01"] if owner == "P3-W08"
                                                           and commit not in pre_amendment else
                                                           ["P3-W09-R01"] if owner == "P3-W09"
                                                           and commit not in pre_amendment else
                                                           ["P3-W11-R01"] if owner == "P3-W11"
                                                           and commit not in pre_amendment else
                                                           ["P3-W15-R03"] if owner == "P3-W15"
                                                           and commit not in pre_r03 else
                                                           ["P3-W15-R02"] if owner == "P3-W15"
                                                           and commit not in pre_r02 else
                                                           ["P3-W15-R01"] if owner == "P3-W15"
                                                           and commit not in pre_amendment else []),
                            "changed_paths": sorted(changed), "tracked_files": len(actual)})
    all_commits = set(git_text("rev-list", intake + ".." + head).splitlines())
    require(seen == all_commits, "incomplete_history_accounting")
    return records


def phase3_entry_and_scope(evidence, unit, base):
    entry = phase_guard.phase3_entry_manifest(ROOT)
    paths = phase_guard.phase3_plan_paths(ROOT)
    require(len(entry["files"]) == 157 and commit_hashes(entry["intake_commit"]) == entry["files"],
            "actual_phase3_intake_hash_mismatch")
    original = {p: h for p, h in entry["files"].items() if p != "PHASE_3_PLAN.md"}
    require(len(original) == 156 and commit_hashes(entry["phase2_commit"]) == original,
            "actual_phase2_hash_mismatch")
    for key, commit_key in (("intake_tree", "intake_commit"), ("phase2_tree", "phase2_commit")):
        require(git_text("rev-parse", entry[commit_key] + "^{tree}") == entry[key], "entry_tree_mismatch")
    head = git_text("rev-parse", "HEAD")
    require(head == os.environ["SIT_REVIEW_HEAD"], "wrong_checked_commit")
    history = phase3_history(entry, base, head, paths, unit)
    changed = changed_between(base, head)
    if unit == "P3-W15" and any(row["immediate_scope_exceptions"] == ["P3-W15-R03"] for row in history):
        require(changed <= phase3_effective_paths(paths, unit) | P3_W15_R03_PATHS,
                "work_unit_allowlist_exceeded")
    else:
        phase3_check_changed_paths(paths, unit, changed)
    actual = tracked_bytes()
    require(actual == commit_hashes(head), "checkout_differs_from_reviewed_commit")
    cumulative = phase3_effective_paths(paths, unit, cumulative=True)
    check_entry_bytes(entry["files"], actual, cumulative)
    old = phase_guard.phase3_historical_nodes(ROOT)
    save(evidence / "entry-and-scope.json", {"ok": True, "unit": unit, "base": base, "head": head,
        "intake_commit": entry["intake_commit"], "intake_tree": entry["intake_tree"],
        "phase2_commit": entry["phase2_commit"], "phase2_tree": entry["phase2_tree"],
        "actual_entry_files": 157, "actual_phase2_files": 156,
        "changed_paths": sorted(changed), "tracked_files": len(actual),
        "frozen_entry_files": len(set(entry["files"]) - cumulative),
        "historical_test_identities": len(old), "phase1_historical_test_identities": len(phase_guard.historical_nodes(ROOT)),
        "predecessor_subtest_events": 428, "scope_exceptions": phase3_scope_exceptions(unit),
        "intermediate_commits": history,
        "provenance": "Full local Git commit archives, all intermediate first-parent changes and actual checkout"})


def preflight(base, evidence):
    entry_and_scope(evidence)
    policy(read_workflow())
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    require(head == os.environ["SIT_REVIEW_HEAD"], "wrong_checked_commit")
    require(f"{sys.version_info.major}.{sys.version_info.minor}" == os.environ["SIT_MATRIX_PYTHON"], "wrong_Python_minor")
    save(evidence / "environment.json", {"head": head, "python": sys.version, "platform": platform.platform(),
        "matrix_os": os.environ["SIT_MATRIX_OS"], "matrix_python": os.environ["SIT_MATRIX_PYTHON"],
        "run_id": os.environ["GITHUB_RUN_ID"], "run_attempt": os.environ["GITHUB_RUN_ATTEMPT"],
        "image_version": os.environ.get("ImageVersion"), "scope": "Phase 3 cumulative verification",
        "unit": os.environ["SIT_PHASE_UNIT"]})
    save(evidence / "tracked-before.json", tracked_bytes())
    for tool in ("check_phase0_baseline", "check_scaffold_boundary"):
        run([sys.executable, "-B", "tools/" + tool + ".py"], evidence, tool + "-before")
    save(evidence / "preflight.json", {"ok": True, "actual_frozen_files_checked": 20,
        "actual_entry_files_checked": 157, "actual_phase2_files_checked": 156, "modules": 48})


def suite_paths():
    scopes = [s for s in ALL_SCOPES if (ROOT / s).is_dir()]
    require(all(s in scopes for s in ALL_SCOPES[:3]), "required_test_directory_missing")
    return scopes


def collection_check(nodes, expected_files, *, unit=None):
    require(len(nodes) == len(set(nodes)) and nodes, "incomplete_or_duplicate_collection")
    require({n.split("::", 1)[0] for n in nodes} == expected_files, "test_file_omitted")
    context = os.environ.get("SIT_PHASE_UNIT", "P3-W01") if unit is None else unit
    if context.startswith("P3-"):
        phase_guard.phase3_unit_number(context)
        require(phase_guard.phase3_historical_nodes(ROOT) <= set(nodes), "phase3_historical_test_identity_omitted")
    else:
        phase_guard.unit_number(context)
    require(phase_guard.historical_nodes(ROOT) <= set(nodes), "historical_test_identity_omitted")


def run_suite(base, evidence):
    env = dict(os.environ)
    env["PYTHONPATH"], env["PIP_NO_INDEX"] = str(ROOT / "src"), "1"
    python, scopes = tool_python(base), suite_paths()
    files = {p.relative_to(ROOT).as_posix() for scope in scopes for p in (ROOT / scope).rglob("test_*.py")}
    for name in files:
        tree = ast.parse((ROOT / name).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute):
                require(node.attr not in ("skip", "skipif", "xfail", "skipIf", "skipUnless", "expectedFailure"), "test_skip_or_xfail_not_authorized")
    collected = run([python, "-m", "pytest", *scopes, "--collect-only", "-q"], evidence, "collection", env=env)
    nodes = [line.strip() for line in collected.stdout.splitlines() if line.startswith("tests/") and "::" in line]
    collection_check(nodes, files)
    save(evidence / "collection.json", {"count": len(nodes), "nodes": nodes, "test_files": sorted(files),
        "historical_retained": 1650, "phase1_historical_retained": 194,
        "predecessor_subtest_events": 428,
        "scope": "all present scaffold/security/contract/unit/integration directories"})
    result = run([python, "-m", "pytest", *scopes, "-q", "--basetemp", base / "pytest",
                  "--junitxml", evidence / "junit.xml"], evidence, "pytest", env=env, timeout=2400, check=False)
    save(evidence / "pytest-exit.json", {"exit_code": result.returncode})
    require(result.returncode == 0, "accumulated_suite_failed")


def evidence_report(base, evidence):
    summary = {"scope": "Phase 3 cumulative verification",
               "unit": os.environ["SIT_PHASE_UNIT"], "pass": False}
    archives = []
    for path in sorted((base / "pytest").rglob("*")):
        if not path.is_file() or not path.name.endswith((".whl", ".tar.gz")):
            continue
        if path.name.endswith(".whl"):
            with zipfile.ZipFile(path) as archive:
                inventory = [{"path": n, "sha256": hashlib.sha256(archive.read(n)).hexdigest()} for n in archive.namelist()]
        else:
            with tarfile.open(path) as archive:
                inventory = [{"path": m.name, "sha256": hashlib.sha256(archive.extractfile(m).read()).hexdigest()}
                             for m in archive.getmembers() if m.isfile()]
        archives.append({"path": path.relative_to(base / "pytest").as_posix(), "bytes": path.stat().st_size,
                         "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "members": inventory})
    save(evidence / "build-inventories.json", archives)
    xml, collection = evidence / "junit.xml", evidence / "collection.json"
    if xml.exists() and collection.exists():
        summary.update(junit_counts(xml.read_bytes(), json.loads(collection.read_bytes())["nodes"]))
    before_file = evidence / "tracked-before.json"
    after = tracked_bytes()
    save(evidence / "tracked-after.json", after)
    unchanged = before_file.exists() and json.loads(before_file.read_bytes()) == after
    pytest_log = evidence / "pytest.log"
    subtests = re.findall(r"\b(\d+) subtests passed\b", pytest_log.read_text(encoding="utf-8")) if pytest_log.exists() else []
    subtest_events = int(subtests[-1]) if subtests else None
    summary["successful_subtest_events"] = subtest_events
    summary["predecessor_subtest_events"] = 428
    summary["predecessor_subtests_retained"] = bool(subtest_events is not None and subtest_events >= 428 and
        subtest_events == summary.get("additional_reported_events"))
    summary["tracked_bytes_unchanged"] = unchanged
    guards_ok = True
    for tool in ("check_phase0_baseline", "check_scaffold_boundary"):
        outcome = run([sys.executable, "-B", "tools/" + tool + ".py"], evidence, tool + "-after", check=False)
        guards_ok = guards_ok and outcome.returncode == 0
    entry_and_scope(evidence)
    exit_record = evidence / "pytest-exit.json"
    summary.update(guards_pass=guards_ok, archive_count=len(archives), historical_retained=1650, phase1_historical_retained=194)
    summary["pass"] = bool(unchanged and guards_ok and summary["predecessor_subtests_retained"] and
        collection.exists() and exit_record.exists() and
        summary.get("tests") == json.loads(collection.read_bytes())["count"] and
        all(summary.get(k) == 0 for k in ("failures", "errors", "skipped")) and
        json.loads(exit_record.read_bytes())["exit_code"] == 0 and len(archives) >= 3)
    save(evidence / "summary.json", summary)
    print("P3_SUMMARY " + json.dumps(summary, sort_keys=True), flush=True)
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as output:
        output.write("## Phase 3 cumulative verification\n\n```json\n" + json.dumps(summary, indent=2) + "\n```\n")
    require(summary["pass"], "required_CI_evidence_failed_or_incomplete")


# Owner-approved P3-W08-R01: the original W08 segment keeps its eight paths.
P3_W08_R01_PATHS = frozenset((
    "src/source_integrity_toolkit/analysis/process_comparison.py",
    "tests/scaffold/test_ci_contract.py",
    "tests/contract/test_phase3_transition.py",
))
P3_W08_R01_BASE = "250dd83b3a7c7fc420263da48583473faf4ebc13"
P3_W08_R01_BASE_TREE = "34fd6ae4e7179d748dcfd03a599d7a12ccb5bf57"
P3_W08_R01_PREDECESSOR = "5b685e80585fe19adb0d9b0324b698cf5bb54e42"


# Owner-approved P3-W09-R01: CI timeouts and their exact existing controls.
# The fixed preapproval checkpoint and its parent retain seven paths.
P3_W09_R01_PATHS = frozenset((
    "tests/scaffold/test_ci_contract.py",
    "tests/contract/test_phase3_transition.py",
    ".github/workflows/phase1-ci.yml",
))
P3_W09_R01_BASE = "5bccceee13995f7ee51ed44339d596aadb309644"
P3_W09_R01_BASE_TREE = "012e520e14977a3ee6a6a1ab143799cfa87ca18a"
P3_W09_R01_PREDECESSOR = "c25c827b9c0c2cf84075c79ebbf6c238dee4ca74"


# Owner-approved P3-W11-R01: exact Assertion before-target dependency repair.
# The original six-path checkpoint remains outside the approved successor scope.
P3_W11_R01_PATHS = frozenset((
    "src/source_integrity_toolkit/contracts/results.py",
    "tests/scaffold/test_ci_contract.py",
    "tests/contract/test_phase3_transition.py",
))
P3_W11_R01_BASE = "48c9a22e2b07df545cd492f921604431c3fec09c"
P3_W11_R01_BASE_TREE = "e1eb494e80e00d5d99640704a81ae4399cd12a86"
P3_W11_R01_PREDECESSOR = "82dc7de63e1007f007e527f53ef0ba719e9c1db4"


# Owner-approved P3-W15-R01: declared dimension selection reason only.
# The fixed seven-path proposal checkpoint keeps its original permission.
P3_W15_R01_PATHS = frozenset((
    "src/source_integrity_toolkit/runtime/boundary.py",
    "tests/integration/test_analytical_pipeline.py",
    "tests/scaffold/test_ci_contract.py",
    "tests/contract/test_phase3_transition.py",
))
P3_W15_R01_BASE = "e8cf08296f6d335a501a451c777b9de4677ff934"
P3_W15_R01_BASE_TREE = "2f26ad5ae8357d972b61464e42f5229f21ae2ec4"
P3_W15_R01_PREDECESSOR = "6dbca96f3314d537beed4ccb6202147bd9248dd9"


# Owner-approved P3-W15-R02: within-call Git parents/tree batching only.
# Later W15 commits keep the seven record paths plus these two controls;
# the earlier R01 product and integration-test permissions do not extend here.
P3_W15_R02_PATHS = frozenset((
    "tests/scaffold/test_ci_contract.py",
    "tests/contract/test_phase3_transition.py",
))
P3_W15_R02_BASE = "4d480f2cc5400e96e724d949ed00c82d62f5aeb7"
P3_W15_R02_BASE_TREE = "bf667ea9d1e46379eee610793c9ecf317ca77276"
P3_W15_R02_PREDECESSOR = "2a8697ea23e315e74c7cc8d7632c95725332b45b"


# Owner-approved P3-W15-R03: bounded full-suite and CI job budgets only.
# Only descendants of this fixed proposal checkpoint gain the workflow path;
# earlier R02 commits keep their nine paths and earlier scopes stay intact.
P3_W15_R03_PATHS = frozenset((
    ".github/workflows/phase1-ci.yml",
    "tests/scaffold/test_ci_contract.py",
    "tests/contract/test_phase3_transition.py",
))
P3_W15_R03_BASE = "d32c1499fe7969b9415468ef62c966c38110a090"
P3_W15_R03_BASE_TREE = "1234a087200c5e56d20c7f53aa0d71a828f167fb"
P3_W15_R03_PREDECESSOR = "3a8c6f99a2aa71ce8e67454801e16a1c5c5caed7"


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--ci-stage":
        stage = sys.argv[2]
        stages = {"preflight": preflight, "prepare": prepare, "test": run_suite, "evidence": evidence_report}
        require(stage in stages, "unknown_CI_stage")
        base, evidence = ci_paths()
        try:
            configure_context()
            stages[stage](base, evidence)
        except Exception as exc:
            save(evidence / (stage + "-failure.json"), {"stage": stage, "error_type": type(exc).__name__, "message": str(exc)})
            raise
    else:
        unittest.main()
