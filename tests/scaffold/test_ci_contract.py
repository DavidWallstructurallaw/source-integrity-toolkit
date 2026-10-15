# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Current explicit workflow tests and a repository-only CI evidence driver.

The workflow is JSON-form YAML to permit strict standard-library inspection.
No product code imports this file. Network access is confined to the explicitly
selected CI dependency acquisition stage, never to an audit operation.
Current controls bind every hosted stage to its actual run and candidate.
The local entry runs the same five test scopes without claiming hosted evidence.
"""

from __future__ import annotations

import copy
import ast
import argparse
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
import tempfile
import unittest
from unittest import mock
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
        prefix, marker, parameter = node.partition("[")
        parts = prefix.split("::")
        require(len(parts) >= 2 and parts[0].endswith(".py"), "bad collected node")
        classname = parts[0][:-3].replace("/", ".")
        if len(parts) > 2:
            classname += "." + ".".join(parts[1:-1])
        expected.append((classname, parts[-1] + marker + parameter))
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
    command = [str(a) for a in args]
    log = evidence / (name + ".log")
    stderr_log = evidence / (name + "-stderr.log")
    status_path = evidence / (name + "-exit.json")
    # A canceled runner may never execute Python cleanup. Open the raw log and
    # record an incomplete attempt before launching the child, then stream into it.
    save(status_path, {"exit_code": None, "timed_out": False, "interrupted": False,
                       "incomplete": True, "timeout_seconds": timeout})
    def outputs():
        stdout = log.read_text(encoding="utf-8", errors="replace")
        stderr = stderr_log.read_text(encoding="utf-8", errors="replace")
        # Keep the established combined log, while stderr remains separately
        # available even if the entire process is killed before this point.
        with log.open("ab") as combined:
            combined.write(stderr_log.read_bytes())
        return stdout, stderr
    try:
        with log.open("w", encoding="utf-8") as output, stderr_log.open("w", encoding="utf-8") as error:
            outcome = subprocess.run(command, cwd=ROOT, env=env, stdout=output,
                                     stderr=error, timeout=timeout)
    except (subprocess.TimeoutExpired, OSError, KeyboardInterrupt) as exc:
        status = {"exit_code": None, "timed_out": isinstance(exc, subprocess.TimeoutExpired),
                  "interrupted": isinstance(exc, KeyboardInterrupt), "incomplete": True,
                  "timeout_seconds": timeout, "error_type": type(exc).__name__, "message": str(exc)}
        outputs()
        save(status_path, status)
        raise
    stdout, stderr = outputs()
    result = subprocess.CompletedProcess(command, outcome.returncode, stdout=stdout, stderr=stderr)
    save(status_path, {"exit_code": result.returncode, "timed_out": False, "interrupted": False,
                       "incomplete": False, "timeout_seconds": timeout})
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

def prepare_tools(base: Path, evidence: Path) -> None:
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
INSTALLED_WITNESSES = frozenset({
    "tests/contract/test_phase2_transition.py::W08R01Tests::test_clean_installed_components_need_no_phase_policy_or_developer_tools",
    "tests/integration/test_analytical_installed_runtime.py::test_clean_installed_analysis_original_heroes_and_completed_finite_case",
})


def policy(value):
    """Direct current workflow policy; independent of historical test source."""
    phase_guard.current_workflow(value)


def configure_context():
    """Require the runner's actual event; no legacy stage or local fallback."""
    require(all(os.environ.get(name) for name in
                ("GITHUB_EVENT_PATH", "GITHUB_EVENT_NAME", "SIT_REVIEW_HEAD")),
            "current_external_context_required")
    return phase_guard.current_context(os.environ["GITHUB_EVENT_NAME"],
        Path(os.environ["GITHUB_EVENT_PATH"]).read_bytes(), os.environ["SIT_REVIEW_HEAD"], root=ROOT)


def current_binding(*, local=False):
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if local:
        state = phase_guard.current_local_state(ROOT)
        require(state["head"] == head, "wrong_checked_commit")
        return {"mode": "local", **state, "python": sys.version,
                "platform": platform.platform(), "hosted_matrix_attestation": False}
    context = configure_context()
    require(os.environ.get("GITHUB_ACTIONS") == "true", "explicit Actions invocation required")
    require(head == context["head"], "wrong_checked_commit")
    names = ("GITHUB_RUN_ID", "GITHUB_RUN_ATTEMPT", "SIT_MATRIX_OS", "SIT_MATRIX_PYTHON")
    require(all(os.environ.get(name) for name in names), "actual_run_and_matrix_required")
    require(os.environ["GITHUB_RUN_ID"].isdigit() and os.environ["GITHUB_RUN_ATTEMPT"].isdigit(),
            "invalid_run_identity")
    require(f"{sys.version_info.major}.{sys.version_info.minor}" == os.environ["SIT_MATRIX_PYTHON"],
            "wrong_Python_minor")
    require(os.environ["SIT_MATRIX_OS"] in ("ubuntu-24.04", "windows-2025") and
            os.environ["SIT_MATRIX_PYTHON"] in ("3.11", "3.13"), "unknown_matrix_profile")
    require(platform.system() == {"windows-2025": "Windows", "ubuntu-24.04": "Linux"}[os.environ["SIT_MATRIX_OS"]],
            "wrong_runner_platform")
    return {"mode": "hosted", **context, "run_id": os.environ["GITHUB_RUN_ID"],
        "run_attempt": os.environ["GITHUB_RUN_ATTEMPT"], "matrix_os": os.environ["SIT_MATRIX_OS"],
        "matrix_python": os.environ["SIT_MATRIX_PYTHON"], "python": sys.version,
        "event_sha256": hashlib.sha256(Path(os.environ["GITHUB_EVENT_PATH"]).read_bytes()).hexdigest()}


def bound_record(evidence, name, binding=None):
    expected = binding if binding is not None else current_binding()
    require(json.loads((evidence / "binding.json").read_bytes()) == expected, "evidence_run_identity_mismatch")
    value = json.loads((evidence / name).read_bytes())
    require(value.get("binding") == expected, "stage_evidence_identity_mismatch")
    return value


def ci_paths():
    require(os.environ.get("GITHUB_ACTIONS") == "true", "explicit Actions invocation required")
    base = Path(os.environ["RUNNER_TEMP"]) / "sit-p3"
    evidence = base / "evidence"
    evidence.mkdir(parents=True, exist_ok=True)
    return base, evidence


def entry_and_scope(evidence):
    """Verify only the owner-accepted anchor and all subsequent real commits."""
    context = configure_context()
    authority = phase_guard.current_authority(ROOT)
    history = phase_guard.current_history(ROOT, context["base"], context["head"], authority)
    checkout = phase_guard.current_checkout(ROOT, context["head"], authority)
    record = {"ok": True, **context, **checkout,
        "accepted_head": phase_guard.P4_ACCEPTED_HEAD,
        "accepted_tree": phase_guard.P4_ACCEPTED_TREE,
        "actual_entry_files": len(authority[0]), "intermediate_commits": history,
        "provenance": "Accepted Git anchor, every subsequent commit including merge sides, index and actual worktree"}
    save(evidence / "entry-and-scope.json", record)
    return record


def guard_command(tool, *, local=False):
    command = [sys.executable, "-B", "tools/" + tool + ".py"]
    if tool == "check_scaffold_boundary":
        if local:
            state = phase_guard.current_local_state(ROOT)
            command += ["--modules-only", "--stage", str(state["activation_stage"])]
        else:
            command += ["--unit", configure_context()["unit"], "--event-name", os.environ["GITHUB_EVENT_NAME"],
                        "--event-file", os.environ["GITHUB_EVENT_PATH"], "--head", os.environ["SIT_REVIEW_HEAD"]]
    return command


def initialize_evidence(evidence, binding):
    # Never recycle outputs from a previous head, job or failed attempt.
    require(not any(evidence.iterdir()), "evidence_directory_must_be_empty")
    save(evidence / "binding.json", binding)
    save(evidence / "tracked-before.json", tracked_bytes())


def preflight(base, evidence):
    binding = current_binding()
    initialize_evidence(evidence, binding)
    scope = entry_and_scope(evidence)
    policy(read_workflow())
    risk = phase_guard.current_risk(ROOT, binding["base"], binding["head"])
    save(evidence / "risk.json", {"binding": binding, **risk})
    if risk["profile"] == "documentation":
        validate_documentation()
    save(evidence / "environment.json", {"binding": binding, "platform": platform.platform(),
        "image_version": os.environ.get("ImageVersion"), "scope": "Current Phase 4 verification"})
    for tool in ("check_phase0_baseline", "check_scaffold_boundary"):
        run(guard_command(tool), evidence, tool + "-before")
    save(evidence / "preflight.json", {"binding": binding, "ok": True,
        "actual_entry_files_checked": scope["actual_entry_files"],
        "actual_frozen_entry_files_checked": scope["frozen_files"], "modules": 48})


def selected_profile(evidence):
    binding = current_binding()
    require(bound_record(evidence, "preflight.json", binding).get("ok") is True, "preflight_not_successful")
    risk = bound_record(evidence, "risk.json", binding)
    actual = phase_guard.current_risk(ROOT, binding["base"], binding["head"])
    require(risk == {"binding": binding, **actual}, "risk_record_does_not_match_actual_diff")
    require(risk["profile"] in ("documentation", "full"), "unknown_risk_profile")
    return binding, risk


def validate_documentation():
    """These records carry no authority, but their formats must remain readable."""
    value = json.loads((ROOT / "phase4/implementation_evidence.json").read_bytes(), object_pairs_hook=unique)
    require(isinstance(value, dict) and bool(value), "documentation_evidence_must_be_nonempty_object")
    require(bool((ROOT / "PHASE_4_COMPLETION.md").read_text(encoding="utf-8").strip()),
            "documentation_completion_must_be_nonempty_utf8")


def prepare(base, evidence):
    binding, risk = selected_profile(evidence)
    if risk["profile"] == "full":
        prepare_tools(base, evidence)
    save(evidence / "prepare.json", {"binding": binding, "ok": True, "profile": risk["profile"],
        "dependency_install_performed": risk["profile"] == "full"})


def suite_paths():
    require(all((ROOT / scope).is_dir() for scope in ALL_SCOPES), "required_test_directory_missing")
    return list(ALL_SCOPES)


def collection_check(nodes, expected_files):
    phase_guard.current_collection(nodes, expected_files)


def reconcile_suite(xml, nodes, successful_subtests):
    require(INSTALLED_WITNESSES <= set(nodes), "required_installed_witness_missing")
    return phase_guard.current_junit(xml, nodes, successful_subtests)


def suite_environment(*, local=False):
    env = dict(os.environ)
    env.update(PYTHONPATH=str(ROOT / "src"), PIP_NO_INDEX="1", PYTHONDONTWRITEBYTECODE="1",
               PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", PYTEST_ADDOPTS="", PYTEST_PLUGINS="",
               PYTHONNOUSERSITE="1", PYTHONUTF8="1", PYTHONUNBUFFERED="1",
               PIP_DISABLE_PIP_VERSION_CHECK="1", PIP_NO_INPUT="1")
    if local:
        for name in tuple(env):
            if name.startswith(("GITHUB_", "SIT_MATRIX_")) or name in ("RUNNER_TEMP", "SIT_REVIEW_HEAD"):
                env.pop(name)
    return env


def execute_suite(base, evidence, python, binding, *, local=False):
    env, scopes = suite_environment(local=local), suite_paths()
    files = {p.relative_to(ROOT).as_posix() for scope in scopes for p in (ROOT / scope).rglob("test_*.py")}
    for name in files:
        tree = ast.parse((ROOT / name).read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute):
                require(node.attr not in ("skip", "skipif", "xfail", "skipIf", "skipUnless", "expectedFailure"),
                        "test_skip_or_xfail_not_authorized")
    collected = run([python, "-B", "-m", "pytest", *scopes, "--collect-only", "-q"],
                    evidence, "collection", env=env)
    nodes = [line.strip() for line in collected.stdout.splitlines() if line.startswith("tests/") and "::" in line]
    collection_check(nodes, files)
    save(evidence / "collection.json", {"binding": binding, "count": len(nodes), "nodes": nodes,
        "test_files": sorted(files), "scopes": scopes})
    result = run([python, "-B", "-m", "pytest", *scopes, "-q", "--basetemp", base / "pytest",
                  "--junitxml", evidence / "junit.xml"], evidence, "pytest", env=env, timeout=2400, check=False)
    # run() writes status even when subprocess creation or its 2400-second budget fails.
    require(result.returncode == 0, "accumulated_suite_failed")
    save(evidence / "test.json", {"binding": binding, "ok": True, "profile": "full", "full_suite": True})


def run_suite(base, evidence):
    binding, risk = selected_profile(evidence)
    prepared = bound_record(evidence, "prepare.json", binding)
    require(prepared.get("ok") is True and prepared.get("profile") == risk["profile"], "prepare_not_successful")
    if risk["profile"] == "documentation":
        save(evidence / "test.json", {"binding": binding, "ok": True, "profile": "documentation",
            "full_suite": False, "collection_performed": False,
            "scope": "Explicit non-executable documentation paths; preflight and final boundary checks"})
    else:
        execute_suite(base, evidence, tool_python(base), binding)


def archive_inventories(base):
    archives = []
    for path in sorted((base / "pytest").rglob("*")):
        if not path.is_file() or not path.name.endswith((".whl", ".tar.gz")):
            continue
        if path.name.endswith(".whl"):
            with zipfile.ZipFile(path) as archive:
                names = archive.namelist()
                require(len(names) == len(set(names)), "duplicate_wheel_member")
                inventory = {name: hashlib.sha256(archive.read(name)).hexdigest() for name in names}
        else:
            with tarfile.open(path) as archive:
                members = [member for member in archive.getmembers() if member.isfile()]
                require(len(members) == len({member.name for member in members}), "duplicate_sdist_member")
                inventory = {m.name: hashlib.sha256(archive.extractfile(m).read()).hexdigest() for m in members}
        archives.append({"path": path.relative_to(base / "pytest").as_posix(), "name": path.name,
            "bytes": path.stat().st_size, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "members": inventory})
    return archives


def installed_receipts(base, evidence, binding, archives, *, local=False):
    modules = {}
    for path in sorted((ROOT / "src/source_integrity_toolkit").rglob("*.py")):
        name = path.relative_to(ROOT / "src").as_posix().removesuffix(".py").replace("/", ".").removesuffix(".__init__")
        modules[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    require(len(modules) == 48, "installed_module_set_changed")
    results = {}
    for label in ("w08", "w14"):
        name = label + "-installed-runtime.json"
        path = evidence / name
        if local:
            if label == "w08":
                results[label] = {"receipt_persisted": False,
                    "reason": "Retained local unittest deletes its temporary receipt; exact JUnit result is required"}
                continue
            found = list((base / "pytest").rglob(name))
            require(len(found) == 1, "local_installed_receipt_missing_or_ambiguous")
            path.write_bytes(found[0].read_bytes())
        receipt = json.loads(path.read_bytes())
        require(receipt.get("head") == binding["head"] and receipt.get("ok") is True, "installed_receipt_head_or_result")
        require(receipt.get("unit") == binding["unit"] and
                type(receipt.get("activation_stage")) is int and
                receipt.get("activation_stage") == binding["activation_stage"],
                "installed_receipt_current_context_mismatch")
        runtime = receipt["runtime"]
        require(runtime["modules"] == modules and runtime["runtime_distributions"] == ["source-integrity-toolkit"] and
                runtime["normal_effects"] == [] and runtime["negative_events"] == ["open", "socket.getaddrinfo", "ctypes.dlopen"] and
                runtime["public_refusals"] == 2, "installed_runtime_boundary_incomplete")
        if label == "w08":
            require(runtime["admitted_fixture_modes"] == 8 and
                    runtime["rejected_empty_modes"] == 2, "installed_preparation_modes_missing")
        else:
            require(len(runtime["hero_modes"]) == 8 and
                    len(runtime["completed_finite_modes"]) == 2 and runtime["invalid_modes"] == 2,
                    "installed_analysis_modes_missing")
            source_sets = {
                "test_sources": {"tests/integration/test_analytical_installed_runtime.py",
                    "tests/integration/test_analytical_hero_inputs.py", "tests/integration/test_analytical_pipeline.py"},
                "frozen_test_sources": {"tests/" + kind + "/" + case + suffix
                    for case in ("H7-01", "H7-V01", "H7-V02", "H7-V03")
                    for kind, suffix in (("fixtures/hero", ".bundle.json"), ("golden", ".logical.json"))},
            }
            for field, expected in source_sets.items():
                require(set(receipt[field]) == expected and all(hashlib.sha256((ROOT / p).read_bytes()).hexdigest() == digest
                        for p, digest in receipt[field].items()), "installed_source_evidence_changed")
        distributions = receipt["distributions"]
        require(len(distributions) == 3 and distributions[0]["name"].endswith(".tar.gz") and
                all(r["name"].endswith(".whl") for r in distributions[1:]) and
                distributions[1]["members"] == distributions[2]["members"], "installed_rebuild_inventory_mismatch")
        require(all(any(r["name"] == a["name"] and r["members"] == a["members"] for a in archives)
                    for r in distributions), "installed_inventory_not_in_current_builds")
        results[label] = {"receipt_persisted": True, "sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
                          "modules": len(modules), "distributions": len(distributions)}
    return results


def emit_summary(evidence, summary):
    save(evidence / "summary.json", summary)
    print("P4_SUMMARY " + json.dumps(summary, sort_keys=True), flush=True)
    if os.environ.get("GITHUB_STEP_SUMMARY") and summary.get("mode") != "local":
        with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as output:
            output.write("## Current Phase 4 verification\n\n```json\n" + json.dumps(summary, indent=2) + "\n```\n")


def reconcile_preparation_commands(evidence, *, local=False):
    """A stage success claim cannot replace its actual subprocess receipts."""
    names = (("installed", "pip-check") if local else
             ("venv", "pip-version", "download", "install", "pip-check", "installed"))
    for name in names:
        try:
            record = json.loads((evidence / (name + "-exit.json")).read_bytes(), object_pairs_hook=unique)
        except (OSError, UnicodeError, ValueError) as exc:
            raise ValueError("preparation_subprocess_receipt_invalid:" + name) from exc
        require(type(record) is dict and type(record.get("exit_code")) is int and
                record["exit_code"] == 0 and record.get("timed_out") is False and
                record.get("interrupted") is False and record.get("incomplete") is False,
                "preparation_subprocess_not_successful:" + name)
    return list(names)


def evidence_report(base, evidence, *, local=False):
    summary = {"scope": "Current Phase 4 verification", "mode": "local" if local else "hosted",
               "pass": False, "full_suite": False, "hosted_matrix_attestation": False}
    try:
        binding = current_binding(local=local)
        summary.update(binding=binding, head=binding["head"])
        if local:
            bound_record(evidence, "preflight.json", binding)
            risk = {"profile": "full", "reason": "Local entry always runs every canonical scope"}
        else:
            _, risk = selected_profile(evidence)
        summary.update(profile=risk["profile"], risk=risk)
        archives = archive_inventories(base)
        save(evidence / "build-inventories.json", archives)
        summary["archive_count"] = len(archives)
        require(not list(evidence.glob("*-failure.json")), "earlier_stage_failed")
        prepared, tested = (bound_record(evidence, name, binding) for name in ("prepare.json", "test.json"))
        require(prepared.get("ok") is True and tested.get("ok") is True and
                prepared.get("profile") == tested.get("profile") == risk["profile"], "required_stage_incomplete")
        if risk["profile"] == "full":
            summary["preparation_commands_completed"] = reconcile_preparation_commands(evidence, local=local)
        after = tracked_bytes()
        save(evidence / "tracked-after.json", after)
        summary["tracked_bytes_unchanged"] = json.loads((evidence / "tracked-before.json").read_bytes()) == after
        require(summary["tracked_bytes_unchanged"], "tracked_bytes_changed_during_verification")
        for tool in ("check_phase0_baseline", "check_scaffold_boundary"):
            run(guard_command(tool, local=local), evidence, tool + "-after", env=suite_environment(local=local))
        policy(read_workflow())
        if not local:
            entry_and_scope(evidence)
        summary["guards_pass"] = True
        if risk["profile"] == "documentation":
            validate_documentation()
            require(prepared.get("dependency_install_performed") is False and
                    not any((evidence / (name + "-exit.json")).exists() for name in
                            ("venv", "pip-version", "download", "install", "pip-check", "installed")),
                    "unexpected_preparation_execution_on_documentation_route")
            require(tested.get("full_suite") is False and tested.get("collection_performed") is False,
                    "documentation_claimed_full_suite")
            require(not any((evidence / name).exists() for name in ("junit.xml", "collection.json", "pytest-exit.json")),
                    "unexpected_full_suite_evidence_on_documentation_route")
            summary.update(tests=None, successful_subtest_events=None,
                scope="Documentation boundary checks only; no test matrix acceptance")
        else:
            collection = bound_record(evidence, "collection.json", binding)
            collection_check(collection["nodes"], collection["test_files"])
            require(collection["count"] == len(collection["nodes"]) and collection["scopes"] == list(ALL_SCOPES),
                    "collection_scope_or_count_mismatch")
            exit_record = json.loads((evidence / "pytest-exit.json").read_bytes())
            require(exit_record["exit_code"] == 0 and exit_record["timed_out"] is False and
                    exit_record["interrupted"] is False and exit_record["incomplete"] is False,
                    "pytest_failed_or_timed_out")
            log = (evidence / "pytest.log").read_text(encoding="utf-8")
            subtests = re.findall(r"\b(\d+) subtests passed\b", log)
            successful_subtests = int(subtests[-1]) if subtests else 0
            summary.update(reconcile_suite((evidence / "junit.xml").read_bytes(),
                                            collection["nodes"], successful_subtests))
            require(len(archives) >= 3 and any(r["name"].endswith(".tar.gz") for r in archives) and
                    sum(r["name"].endswith(".whl") for r in archives) >= 2, "build_rebuild_archives_missing")
            summary.update(installed_receipts=installed_receipts(base, evidence, binding, archives, local=local),
                archive_count=len(archives), successful_subtest_events=successful_subtests,
                subtest_events_reconciled=True, full_suite=True)
        summary["pass"] = True
    except (Exception, KeyboardInterrupt) as exc:
        summary.update(error_type=type(exc).__name__, message=str(exc))
        raise
    finally:
        emit_summary(evidence, summary)


def stage_failure(evidence, stage, exc, *, local=False):
    failure = {"stage": stage, "error_type": type(exc).__name__, "message": str(exc)}
    save(evidence / (stage + "-failure.json"), failure)
    summary_path = evidence / "summary.json"
    summary = json.loads(summary_path.read_bytes()) if summary_path.exists() else {
        "scope": "Current Phase 4 verification", "mode": "local" if local else "hosted"}
    summary.update({"pass": False, "full_suite": False, "hosted_matrix_attestation": False, "failure": failure})
    emit_summary(evidence, summary)


def local_verify(evidence):
    evidence = evidence.resolve()
    require(not evidence.is_relative_to(ROOT), "local_evidence_must_be_outside_repository")
    evidence.mkdir(parents=True, exist_ok=True)
    binding = current_binding(local=True)
    initialize_evidence(evidence, binding)
    # Only the entry invocation owns this fresh directory; its subprocess tests
    # receive no GitHub context and cannot emit hosted-run attestations.
    base = evidence / "work"
    base.mkdir()
    stage = "preflight"
    try:
        policy(read_workflow())
        for tool in ("check_phase0_baseline", "check_scaffold_boundary"):
            run(guard_command(tool, local=True), evidence, tool + "-before", env=suite_environment(local=True))
        save(evidence / "preflight.json", {"binding": binding, "ok": True,
            "scope": "Local module/workflow guards; no external authorization event"})
        stage = "prepare"
        result = run([sys.executable, "-m", "pip", "--isolated", "list", "--format=json"],
                     evidence, "installed", env=suite_environment(local=True))
        installed = {r["name"].lower(): r["version"] for r in json.loads(result.stdout)}
        selected = {**SELECTED, **({"colorama": "0.4.6"} if os.name == "nt" else {})}
        require({name: version for name, version in installed.items() if name != "pip"} == selected,
                "installed tool set mismatch")
        run([sys.executable, "-m", "pip", "--isolated", "check"], evidence, "pip-check", env=suite_environment(local=True))
        save(evidence / "installed.json", installed)
        save(evidence / "prepare.json", {"binding": binding, "ok": True, "profile": "full",
            "dependency_install_performed": False, "selected_tool_versions_verified": True})
        stage = "test"
        execute_suite(base, evidence, sys.executable, binding, local=True)
        stage = "evidence"
        evidence_report(base, evidence, local=True)
    except (Exception, KeyboardInterrupt) as exc:
        stage_failure(evidence, stage, exc, local=True)
        raise


class DriverEvidenceTests(unittest.TestCase):
    """Exercise evidence failures and route boundaries without a nested full suite."""

    def workspace(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        return Path(temporary.name)

    def test_actual_event_is_checked_against_repository_commit_context(self):
        event_file = self.workspace() / "event.json"
        event_file.write_bytes(b'{"actual":"event"}')
        context = {"unit": "P4-W01", "activation_stage": 1, "head": "a" * 40,
                   "base": "b" * 40, "event": "pull_request"}
        with mock.patch.dict(os.environ, {"GITHUB_EVENT_NAME": "pull_request",
                "GITHUB_EVENT_PATH": str(event_file), "SIT_REVIEW_HEAD": context["head"],
                "SIT_PHASE_UNIT": "P4-W10"}), \
                mock.patch.object(phase_guard, "current_context", return_value=context) as resolve:
            self.assertEqual(configure_context(), context)
        resolve.assert_called_once_with("pull_request", event_file.read_bytes(), context["head"], root=ROOT)

    def test_local_binding_uses_verified_ancestry_without_hosted_attestation(self):
        state = {"unit": "P4-W02", "activation_stage": 8, "head": "a" * 40,
                 "base": "b" * 40, "clean": False}
        with mock.patch.object(phase_guard, "current_local_state", return_value=state) as resolve, \
                mock.patch.object(subprocess, "check_output", return_value=state["head"] + "\n"), \
                mock.patch.dict(os.environ, {"SIT_PHASE_UNIT": "P4-W01", "GITHUB_RUN_ID": "123"}):
            binding = current_binding(local=True)
        resolve.assert_called_once_with(ROOT)
        self.assertEqual({key: binding[key] for key in state}, state)
        self.assertEqual(binding["mode"], "local")
        self.assertIs(binding["hosted_matrix_attestation"], False)
        self.assertNotIn("run_id", binding)

    def test_local_package_probe_keeps_activation_after_earlier_unit_repair(self):
        state = {"unit": "P4-W02", "activation_stage": 8, "head": "a" * 40}
        with mock.patch.object(phase_guard, "current_local_state", return_value=state):
            command = guard_command("check_scaffold_boundary", local=True)
        self.assertEqual(command[-3:], ["--modules-only", "--stage", "8"])
        self.assertNotIn("--unit", command)

    def test_hosted_guard_unit_comes_from_verified_context(self):
        context = {"unit": "P4-W01", "activation_stage": 1}
        with mock.patch(__name__ + ".configure_context", return_value=context), \
                mock.patch.dict(os.environ, {"GITHUB_EVENT_NAME": "pull_request",
                    "GITHUB_EVENT_PATH": "actual-event.json", "SIT_REVIEW_HEAD": "a" * 40,
                    "SIT_PHASE_UNIT": "P4-W10"}):
            command = guard_command("check_scaffold_boundary")
        self.assertEqual(command[command.index("--unit") + 1], "P4-W01")

    def test_installed_receipts_bind_current_unit_activation_and_both_refusals(self):
        evidence = self.workspace()
        binding = {"head": "a" * 40, "unit": "P4-W01", "activation_stage": 1}
        modules = {}
        for path in sorted((ROOT / "src/source_integrity_toolkit").rglob("*.py")):
            name = path.relative_to(ROOT / "src").as_posix().removesuffix(".py").replace("/", ".").removesuffix(".__init__")
            modules[name] = hashlib.sha256(path.read_bytes()).hexdigest()
        self.assertEqual(len(modules), 48)
        distributions = [{"name": "synthetic.tar.gz", "members": {"source": "synthetic"}},
            {"name": "synthetic.whl", "members": {"module": "synthetic"}},
            {"name": "synthetic.whl", "members": {"module": "synthetic"}}]
        runtime = {"modules": modules, "runtime_distributions": ["source-integrity-toolkit"],
            "normal_effects": [], "negative_events": ["open", "socket.getaddrinfo", "ctypes.dlopen"],
            "public_refusals": 2}
        w08 = {**binding, "ok": True, "distributions": distributions, "runtime": {
            **runtime, "admitted_fixture_modes": 8, "rejected_empty_modes": 2}}
        w14 = {**binding, "ok": True, "distributions": distributions, "runtime": {
            **runtime, "hero_modes": list(range(8)), "completed_finite_modes": list(range(2)), "invalid_modes": 2}}
        for field, paths in {
                "test_sources": ["tests/integration/test_analytical_installed_runtime.py",
                    "tests/integration/test_analytical_hero_inputs.py", "tests/integration/test_analytical_pipeline.py"],
                "frozen_test_sources": ["tests/" + kind + "/" + case + suffix
                    for case in ("H7-01", "H7-V01", "H7-V02", "H7-V03")
                    for kind, suffix in (("fixtures/hero", ".bundle.json"), ("golden", ".logical.json"))],
                }.items():
            w14[field] = {path: hashlib.sha256((ROOT / path).read_bytes()).hexdigest() for path in paths}
        records = {"w08": w08, "w14": w14}
        for label, record in records.items():
            save(evidence / (label + "-installed-runtime.json"), record)
        self.assertEqual(set(installed_receipts(evidence, evidence, binding, distributions)), {"w08", "w14"})
        for label in records:
            for field, value, reason in (
                    ("unit", "VC", "installed_receipt_current_context_mismatch"),
                    ("unit", "P3-W14", "installed_receipt_current_context_mismatch"),
                    ("activation_stage", 8, "installed_receipt_current_context_mismatch"),
                    ("activation_stage", True, "installed_receipt_current_context_mismatch"),
                    ("head", "b" * 40, "installed_receipt_head_or_result"),
                    ("public_refusals", 1, "installed_runtime_boundary_incomplete")):
                with self.subTest(label=label, field=field, value=value):
                    changed = copy.deepcopy(records[label])
                    (changed["runtime"] if field == "public_refusals" else changed)[field] = value
                    save(evidence / (label + "-installed-runtime.json"), changed)
                    with self.assertRaisesRegex(ValueError, "^" + reason + "$"):
                        installed_receipts(evidence, evidence, binding, distributions)
                    save(evidence / (label + "-installed-runtime.json"), records[label])
        self.assertEqual(set(installed_receipts(evidence, evidence, binding, distributions)), {"w08", "w14"})

    def test_timeout_preserves_partial_stdout_stderr_and_status(self):
        evidence = self.workspace()
        command = [sys.executable, "-u", "-c",
            "import sys,time; print('partial stdout'); print('partial stderr',file=sys.stderr); time.sleep(30)"]
        with self.assertRaises(subprocess.TimeoutExpired):
            run(command, evidence, "pytest", timeout=3)
        self.assertIn("partial stdout", (evidence / "pytest.log").read_text())
        self.assertIn("partial stderr", (evidence / "pytest.log").read_text())
        status = json.loads((evidence / "pytest-exit.json").read_bytes())
        self.assertIsNone(status["exit_code"])
        self.assertIs(status["timed_out"], True)

    def test_nonzero_exit_preserves_raw_output_and_status(self):
        evidence = self.workspace()
        with self.assertRaisesRegex(ValueError, "full output preserved"):
            run([sys.executable, "-c", "print('failed canary'); raise SystemExit(7)"], evidence, "canary")
        self.assertIn("failed canary", (evidence / "canary.log").read_text())
        self.assertEqual(json.loads((evidence / "canary-exit.json").read_bytes())["exit_code"], 7)

    def test_process_creation_failure_has_status_and_log(self):
        evidence = self.workspace()
        with self.assertRaises(OSError):
            run([evidence / "missing-interpreter"], evidence, "pytest")
        self.assertTrue((evidence / "pytest.log").is_file())
        self.assertIsNone(json.loads((evidence / "pytest-exit.json").read_bytes())["exit_code"])

    def test_interrupt_keeps_live_channels_and_incomplete_status(self):
        evidence = self.workspace()
        def interrupted_child(command, **kwargs):
            kwargs["stdout"].write("live output")
            kwargs["stdout"].flush()
            kwargs["stderr"].write("live error")
            kwargs["stderr"].flush()
            self.assertEqual((evidence / "pytest.log").read_text(), "live output")
            self.assertEqual((evidence / "pytest-stderr.log").read_text(), "live error")
            self.assertIs(json.loads((evidence / "pytest-exit.json").read_bytes())["incomplete"], True)
            raise KeyboardInterrupt()
        with mock.patch.object(subprocess, "run", side_effect=interrupted_child):
            with self.assertRaises(KeyboardInterrupt):
                run(["interrupted-child"], evidence, "pytest")
        status = json.loads((evidence / "pytest-exit.json").read_bytes())
        self.assertIs(status["interrupted"], True)
        self.assertIs(status["incomplete"], True)
        self.assertEqual((evidence / "pytest.log").read_text(), "live outputlive error")

    def test_live_logs_keep_stdout_parseable_when_stderr_has_warning(self):
        evidence = self.workspace()
        result = run([sys.executable, "-c",
            "import sys; print('{\"ok\":true}'); print('stderr warning',file=sys.stderr)"], evidence, "json")
        self.assertEqual(json.loads(result.stdout), {"ok": True})
        self.assertIn("stderr warning", result.stderr)
        self.assertIn("stderr warning", (evidence / "json.log").read_text())

    def test_matching_collection_and_junit_cannot_omit_installed_witness(self):
        def document(nodes):
            cases = []
            for node in nodes:
                parts = node.split("::")
                classname = ".".join([parts[0][:-3].replace("/", "."), *parts[1:-1]])
                cases.append('<testcase classname="' + classname + '" name="' + parts[-1] + '"/>')
            return ('<testsuites><testsuite tests="' + str(len(nodes)) +
                    '" failures="0" errors="0" skipped="0">' + "".join(cases) +
                    '</testsuite></testsuites>').encode()
        nodes = [
            "tests/contract/test_phase2_transition.py::W08R01Tests::test_clean_installed_components_need_no_phase_policy_or_developer_tools",
            "tests/integration/test_analytical_installed_runtime.py::test_clean_installed_analysis_original_heroes_and_completed_finite_case",
        ]
        self.assertEqual(reconcile_suite(document(nodes), nodes, 0)["tests"], 2)
        for missing in nodes:
            with self.subTest(missing=missing):
                reduced = [node for node in nodes if node != missing]
                self.assertTrue(phase_guard.current_junit(document(reduced), reduced, 0)["identities_match"])
                with self.assertRaisesRegex(ValueError, "required_installed_witness_missing"):
                    reconcile_suite(document(reduced), reduced, 0)

    def test_existing_evidence_is_rejected_without_removing_raw_attempt(self):
        evidence = self.workspace()
        (evidence / "junit.xml").write_bytes(b"original raw attempt")
        with self.assertRaisesRegex(ValueError, "must_be_empty"):
            initialize_evidence(evidence, {"head": "new"})
        self.assertEqual((evidence / "junit.xml").read_bytes(), b"original raw attempt")
        self.assertFalse((evidence / "binding.json").exists())

    def test_missing_unit_or_integration_directory_cannot_reduce_suite(self):
        root = self.workspace()
        for scope in ALL_SCOPES[:3]:
            (root / scope).mkdir(parents=True)
        with mock.patch(__name__ + ".ROOT", root):
            for missing in ALL_SCOPES[3:]:
                with self.subTest(missing=missing):
                    with self.assertRaisesRegex(ValueError, "required_test_directory_missing"):
                        suite_paths()
                    (root / missing).mkdir()
            self.assertEqual(suite_paths(), list(ALL_SCOPES))

    def test_suite_environment_clears_selection_and_plugin_injection(self):
        with mock.patch.dict(os.environ, {"PYTEST_ADDOPTS": "--deselect tests/unit/test_x.py::test_y",
                "PYTEST_PLUGINS": "unexpected_plugin", "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "0"}):
            environment = suite_environment()
        self.assertEqual(environment["PYTEST_ADDOPTS"], "")
        self.assertEqual(environment["PYTEST_PLUGINS"], "")
        self.assertEqual(environment["PYTEST_DISABLE_PLUGIN_AUTOLOAD"], "1")
        self.assertEqual(environment["PIP_NO_INDEX"], "1")

    def test_local_children_do_not_inherit_hosted_receipt_destination(self):
        with mock.patch.dict(os.environ, {"GITHUB_ACTIONS": "true", "GITHUB_RUN_ID": "123",
                "RUNNER_TEMP": "/hosted", "SIT_MATRIX_OS": "ubuntu-24.04", "SIT_REVIEW_HEAD": "old"}):
            environment = suite_environment(local=True)
        self.assertTrue(all(name not in environment for name in
            ("GITHUB_ACTIONS", "GITHUB_RUN_ID", "RUNNER_TEMP", "SIT_MATRIX_OS", "SIT_REVIEW_HEAD")))

    def test_wrong_head_attempt_or_matrix_cannot_reuse_stage_record(self):
        evidence = self.workspace()
        binding = {"head": "candidate", "run_attempt": "1", "matrix_python": "3.11",
                   "unit": "P4-W01", "activation_stage": 1}
        save(evidence / "binding.json", binding)
        save(evidence / "preflight.json", {"binding": binding, "ok": True})
        for field, value in (("head", "other"), ("run_attempt", "2"), ("matrix_python", "3.13"),
                             ("unit", "P4-W02"), ("activation_stage", 8)):
            with self.subTest(field=field):
                with self.assertRaisesRegex(ValueError, "identity_mismatch"):
                    bound_record(evidence, "preflight.json", {**binding, field: value})

    def test_stage_record_binding_is_checked_independently(self):
        evidence = self.workspace()
        save(evidence / "binding.json", {"head": "current"})
        save(evidence / "preflight.json", {"binding": {"head": "old"}, "ok": True})
        with self.assertRaisesRegex(ValueError, "stage_evidence_identity_mismatch"):
            bound_record(evidence, "preflight.json", {"head": "current"})

    def test_recorded_documentation_route_cannot_override_actual_full_diff(self):
        evidence = self.workspace()
        binding = {"base": "base", "head": "head"}
        save(evidence / "binding.json", binding)
        save(evidence / "preflight.json", {"binding": binding, "ok": True})
        save(evidence / "risk.json", {"binding": binding, "profile": "documentation"})
        with mock.patch(__name__ + ".current_binding", return_value=binding), \
                mock.patch.object(phase_guard, "current_risk", return_value={"profile": "full"}):
            with self.assertRaisesRegex(ValueError, "actual_diff"):
                selected_profile(evidence)

    def test_documentation_route_explicitly_records_no_install_or_full_suite(self):
        evidence = self.workspace()
        binding = {"head": "candidate"}
        save(evidence / "binding.json", binding)
        with mock.patch(__name__ + ".selected_profile", return_value=(binding, {"profile": "documentation"})), \
                mock.patch(__name__ + ".prepare_tools", side_effect=AssertionError("unexpected install")), \
                mock.patch(__name__ + ".execute_suite", side_effect=AssertionError("unexpected suite")):
            prepare(evidence / "work", evidence)
            run_suite(evidence / "work", evidence)
        prepared = json.loads((evidence / "prepare.json").read_bytes())
        tested = json.loads((evidence / "test.json").read_bytes())
        self.assertIs(prepared["dependency_install_performed"], False)
        self.assertIs(tested["full_suite"], False)
        self.assertIs(tested["collection_performed"], False)
        self.assertFalse((evidence / "junit.xml").exists())

    def test_full_summary_reconciles_raw_preparation_despite_successful_stage_claims(self):
        """Valid later-stage evidence cannot repair a missing earlier exit."""
        for local in (True, False):
            evidence = self.workspace()
            binding = {"head": "a" * 40, "base": "b" * 40}
            save(evidence / "binding.json", binding)
            save(evidence / "preflight.json", {"binding": binding, "ok": True})
            save(evidence / "prepare.json", {"binding": binding, "ok": True,
                "profile": "full", "dependency_install_performed": not local})
            save(evidence / "test.json", {"binding": binding, "ok": True, "profile": "full"})
            save(evidence / "tracked-before.json", {})
            nodes = [
                "tests/contract/test_phase2_transition.py::W08R01Tests::test_clean_installed_components_need_no_phase_policy_or_developer_tools",
                "tests/integration/test_analytical_installed_runtime.py::test_clean_installed_analysis_original_heroes_and_completed_finite_case",
            ]
            save(evidence / "collection.json", {"binding": binding, "nodes": nodes,
                "count": 2, "test_files": [node.split("::")[0] for node in nodes], "scopes": list(ALL_SCOPES)})
            document = ET.Element("testsuites")
            suite = ET.SubElement(document, "testsuite", tests="2", failures="0", errors="0", skipped="0")
            for node in nodes:
                parts = node.split("::")
                ET.SubElement(suite, "testcase", classname=".".join(
                    [parts[0][:-3].replace("/", "."), *parts[1:-1]]), name=parts[-1])
            (evidence / "junit.xml").write_bytes(ET.tostring(document))
            (evidence / "pytest.log").write_text("2 passed\n", encoding="utf-8")
            complete = {"exit_code": 0, "timed_out": False, "interrupted": False,
                        "incomplete": False, "timeout_seconds": 180}
            save(evidence / "pytest-exit.json", {**complete, "timeout_seconds": 2400})
            names = (["installed", "pip-check"] if local else
                     ["venv", "pip-version", "download", "install", "pip-check", "installed"])
            for name in names:
                save(evidence / (name + "-exit.json"), complete)
            archives = [{"name": name} for name in ("a.tar.gz", "a.whl", "b.whl")]
            with mock.patch(__name__ + ".current_binding", return_value=binding), \
                    mock.patch(__name__ + ".selected_profile", return_value=(binding, {"profile": "full"})), \
                    mock.patch(__name__ + ".archive_inventories", return_value=archives), \
                    mock.patch(__name__ + ".tracked_bytes", return_value={}), \
                    mock.patch(__name__ + ".guard_command", return_value=["synthetic-guard"]), \
                    mock.patch(__name__ + ".run"), \
                    mock.patch(__name__ + ".policy"), \
                    mock.patch(__name__ + ".entry_and_scope"), \
                    mock.patch(__name__ + ".installed_receipts", return_value={}), \
                    mock.patch(__name__ + ".emit_summary", side_effect=lambda path, value: save(path / "summary.json", value)):
                evidence_report(evidence / "work", evidence, local=local)
                positive = json.loads((evidence / "summary.json").read_bytes())
                self.assertIs(positive["pass"], True)
                self.assertEqual(positive["preparation_commands_completed"], names)
                for name in names:
                    path = evidence / (name + "-exit.json")
                    mutations = [None, b"{", b"[]", b'{"exit_code":0,"exit_code":7}',
                        json.dumps({**complete, "exit_code": False}).encode(),
                        json.dumps({**complete, "exit_code": 7}).encode(),
                        json.dumps({**complete, "exit_code": None, "incomplete": True}).encode(),
                        json.dumps({**complete, "timed_out": True}).encode(),
                        json.dumps({**complete, "interrupted": True}).encode(),
                        json.dumps({**complete, "incomplete": True}).encode(),
                        json.dumps({key: value for key, value in complete.items() if key != "incomplete"}).encode()]
                    for index, raw in enumerate(mutations):
                        with self.subTest(local=local, command=name, mutation=index):
                            path.unlink()
                            if raw is not None:
                                path.write_bytes(raw)
                            with self.assertRaisesRegex(ValueError, "^preparation_subprocess_"):
                                evidence_report(evidence / "work", evidence, local=local)
                            self.assertIs(json.loads((evidence / "summary.json").read_bytes())["pass"], False)
                            self.assertIs(json.loads((evidence / "prepare.json").read_bytes())["ok"], True)
                            save(path, complete)
                evidence_report(evidence / "work", evidence, local=local)
                self.assertIs(json.loads((evidence / "summary.json").read_bytes())["pass"], True)

    def test_documentation_summary_has_no_preparation_execution(self):
        evidence = self.workspace()
        binding = {"head": "a" * 40}
        save(evidence / "binding.json", binding)
        save(evidence / "prepare.json", {"binding": binding, "ok": True,
            "profile": "documentation", "dependency_install_performed": False})
        save(evidence / "test.json", {"binding": binding, "ok": True,
            "profile": "documentation", "full_suite": False, "collection_performed": False})
        save(evidence / "tracked-before.json", {})
        with mock.patch(__name__ + ".current_binding", return_value=binding), \
                mock.patch(__name__ + ".selected_profile", return_value=(binding, {"profile": "documentation"})), \
                mock.patch(__name__ + ".archive_inventories", return_value=[]), \
                mock.patch(__name__ + ".tracked_bytes", return_value={}), \
                mock.patch(__name__ + ".guard_command", return_value=["synthetic-guard"]), \
                mock.patch(__name__ + ".run"), \
                mock.patch(__name__ + ".policy"), \
                mock.patch(__name__ + ".entry_and_scope"), \
                mock.patch(__name__ + ".validate_documentation"), \
                mock.patch(__name__ + ".reconcile_preparation_commands", side_effect=AssertionError("unexpected dependencies")), \
                mock.patch(__name__ + ".emit_summary", side_effect=lambda path, value: save(path / "summary.json", value)):
            evidence_report(evidence / "work", evidence)
            summary = json.loads((evidence / "summary.json").read_bytes())
            self.assertIs(summary["pass"], True)
            self.assertIs(summary["full_suite"], False)
            save(evidence / "pip-check-exit.json", {"exit_code": 0, "incomplete": False})
            with self.assertRaisesRegex(ValueError, "unexpected_preparation_execution_on_documentation_route"):
                evidence_report(evidence / "work", evidence)
            self.assertIs(json.loads((evidence / "summary.json").read_bytes())["pass"], False)

    def test_documentation_still_requires_readable_nonempty_records(self):
        root = self.workspace()
        (root / "phase4").mkdir()
        (root / "PHASE_4_COMPLETION.md").write_text("Review record", encoding="utf-8")
        with mock.patch(__name__ + ".ROOT", root):
            for content in ("{", "{}", "[]", '{"a":1,"a":2}'):
                with self.subTest(content=content):
                    (root / "phase4/implementation_evidence.json").write_text(content, encoding="utf-8")
                    with self.assertRaises(ValueError):
                        validate_documentation()
            (root / "phase4/implementation_evidence.json").write_text('{"record":"readable"}', encoding="utf-8")
            validate_documentation()

    def test_early_context_failure_still_writes_failed_summary(self):
        evidence = self.workspace()
        with mock.patch(__name__ + ".current_binding", side_effect=ValueError("missing actual context")), \
                mock.patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": ""}):
            with self.assertRaisesRegex(ValueError, "missing actual context"):
                evidence_report(evidence / "work", evidence)
        summary = json.loads((evidence / "summary.json").read_bytes())
        self.assertIs(summary["pass"], False)
        self.assertIs(summary["full_suite"], False)
        self.assertEqual(summary["message"], "missing actual context")

    def test_stage_failure_preserves_raw_attempt_and_cannot_keep_success(self):
        evidence = self.workspace()
        save(evidence / "summary.json", {"pass": True, "full_suite": True})
        (evidence / "pytest.log").write_text("raw failed attempt", encoding="utf-8")
        with mock.patch.dict(os.environ, {"GITHUB_STEP_SUMMARY": ""}):
            stage_failure(evidence, "test", ValueError("test failure"), local=True)
        summary = json.loads((evidence / "summary.json").read_bytes())
        self.assertIs(summary["pass"], False)
        self.assertIs(summary["full_suite"], False)
        self.assertTrue((evidence / "test-failure.json").is_file())
        self.assertEqual((evidence / "pytest.log").read_text(), "raw failed attempt")

    def test_parameter_delimiters_remain_part_of_junit_test_name(self):
        xml = (b'<testsuites><testsuite tests="1" failures="0" errors="0" skipped="0">'
               b'<testcase classname="tests.unit.test_example" name="test_one[left::right]"/>'
               b'</testsuite></testsuites>')
        node = "tests/unit/test_example.py::test_one[left::right]"
        self.assertEqual(junit_counts(xml, [node])["tests"], 1)
        self.assertTrue(phase_guard.current_junit(xml, [node], 0)["identities_match"])


if __name__ == "__main__":
    if "--ci-stage" in sys.argv or "--local" in sys.argv:
        parser = argparse.ArgumentParser(description="Current verification entry and evidence driver")
        mode = parser.add_mutually_exclusive_group(required=True)
        mode.add_argument("--ci-stage", choices=("preflight", "prepare", "test", "evidence"))
        mode.add_argument("--local", action="store_true")
        parser.add_argument("--evidence-dir", type=Path)
        args = parser.parse_args()
        if args.local:
            destination = args.evidence_dir or Path(tempfile.mkdtemp(prefix="sit-p4-local-"))
            print("Local evidence: " + str(destination.resolve()), flush=True)
            local_verify(destination)
        else:
            require(args.evidence_dir is None, "hosted_evidence_destination_is_fixed")
            base, evidence = ci_paths()
            stages = {"preflight": preflight, "prepare": prepare, "test": run_suite, "evidence": evidence_report}
            try:
                stages[args.ci_stage](base, evidence)
            except (Exception, KeyboardInterrupt) as exc:
                stage_failure(evidence, args.ci_stage, exc)
                raise
    else:
        unittest.main()
