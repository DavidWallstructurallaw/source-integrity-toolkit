# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Current explicit workflow tests and a repository-only CI evidence driver.

The workflow is JSON-form YAML to permit strict standard-library inspection.
No product code imports this file. Network access is confined to the explicitly
selected CI dependency acquisition stage, never to an audit operation.
VC-04 removes historical replay and binds this driver to current controls.
Workflow presentation and developer-entry consolidation remain VC-05 work.
"""

from __future__ import annotations

import copy
import ast
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


def policy(value):
    """Direct current workflow policy; independent of historical test source."""
    phase_guard.current_workflow(value)


def configure_context():
    """Require the runner's actual event; no legacy stage or local fallback."""
    require(all(os.environ.get(name) for name in
                ("GITHUB_EVENT_PATH", "GITHUB_EVENT_NAME", "SIT_REVIEW_HEAD")),
            "current_external_context_required")
    return phase_guard.current_context(os.environ["GITHUB_EVENT_NAME"],
        Path(os.environ["GITHUB_EVENT_PATH"]).read_bytes(), os.environ["SIT_REVIEW_HEAD"])


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
        "accepted_head": phase_guard.VC_ACCEPTED_HEAD,
        "accepted_tree": phase_guard.VC_ACCEPTED_TREE,
        "actual_entry_files": len(authority[0]),
        "intermediate_commits": history,
        "provenance": "Accepted Git anchor, every subsequent commit including merge sides, index and actual worktree"}
    save(evidence / "entry-and-scope.json", record)
    return record


def guard_command(tool):
    command = [sys.executable, "-B", "tools/" + tool + ".py"]
    if tool == "check_scaffold_boundary":
        command += ["--unit", "VC", "--event-name", os.environ["GITHUB_EVENT_NAME"],
                    "--event-file", os.environ["GITHUB_EVENT_PATH"], "--head", os.environ["SIT_REVIEW_HEAD"]]
    return command


def preflight(base, evidence):
    scope = entry_and_scope(evidence)
    policy(read_workflow())
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    require(head == os.environ["SIT_REVIEW_HEAD"], "wrong_checked_commit")
    require(f"{sys.version_info.major}.{sys.version_info.minor}" == os.environ["SIT_MATRIX_PYTHON"], "wrong_Python_minor")
    save(evidence / "environment.json", {"head": head, "python": sys.version, "platform": platform.platform(),
        "matrix_os": os.environ["SIT_MATRIX_OS"], "matrix_python": os.environ["SIT_MATRIX_PYTHON"],
        "run_id": os.environ["GITHUB_RUN_ID"], "run_attempt": os.environ["GITHUB_RUN_ATTEMPT"],
        "image_version": os.environ.get("ImageVersion"), "scope": "Current verification consolidation",
        "unit": scope["unit"]})
    save(evidence / "tracked-before.json", tracked_bytes())
    for tool in ("check_phase0_baseline", "check_scaffold_boundary"):
        run(guard_command(tool), evidence, tool + "-before")
    save(evidence / "preflight.json", {"ok": True, "actual_frozen_files_checked": 20,
        "actual_entry_files_checked": scope["actual_entry_files"],
        "actual_frozen_entry_files_checked": scope["frozen_files"], "modules": 48})


def suite_paths():
    scopes = [s for s in ALL_SCOPES if (ROOT / s).is_dir()]
    require(all(s in scopes for s in ALL_SCOPES[:3]), "required_test_directory_missing")
    return scopes


def collection_check(nodes, expected_files):
    phase_guard.current_collection(nodes, expected_files)


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
        "scope": "all present scaffold/security/contract/unit/integration directories"})
    result = run([python, "-m", "pytest", *scopes, "-q", "--basetemp", base / "pytest",
                  "--junitxml", evidence / "junit.xml"], evidence, "pytest", env=env, timeout=2400, check=False)
    save(evidence / "pytest-exit.json", {"exit_code": result.returncode})
    require(result.returncode == 0, "accumulated_suite_failed")


def evidence_report(base, evidence):
    context = configure_context()
    summary = {"scope": "Current verification consolidation",
               "unit": context["unit"], "head": context["head"], "pass": False}
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
    subtest_events = int(subtests[-1]) if subtests else (0 if pytest_log.exists() else None)
    summary["successful_subtest_events"] = subtest_events
    summary["subtest_events_reconciled"] = bool(subtest_events is not None and
        subtest_events == summary.get("additional_reported_events"))
    summary["tracked_bytes_unchanged"] = unchanged
    guards_ok = True
    for tool in ("check_phase0_baseline", "check_scaffold_boundary"):
        outcome = run(guard_command(tool), evidence, tool + "-after", check=False)
        guards_ok = guards_ok and outcome.returncode == 0
    entry_and_scope(evidence)
    exit_record = evidence / "pytest-exit.json"
    summary.update(guards_pass=guards_ok, archive_count=len(archives))
    summary["pass"] = bool(unchanged and guards_ok and summary["subtest_events_reconciled"] and
        collection.exists() and exit_record.exists() and
        summary.get("tests") == json.loads(collection.read_bytes())["count"] and
        all(summary.get(k) == 0 for k in ("failures", "errors", "skipped")) and
        json.loads(exit_record.read_bytes())["exit_code"] == 0 and len(archives) >= 3)
    save(evidence / "summary.json", summary)
    print("VC_SUMMARY " + json.dumps(summary, sort_keys=True), flush=True)
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as output:
        output.write("## Current verification consolidation\n\n```json\n" + json.dumps(summary, indent=2) + "\n```\n")
    require(summary["pass"], "required_CI_evidence_failed_or_incomplete")


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
