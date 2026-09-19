# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Cumulative Phase 2 CI, retaining the complete pinned Phase 1 control suite."""
from pathlib import Path
import sys
import io
import ast
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools import check_scaffold_boundary as phase_guard
phase_guard.load_phase1_test("tests/scaffold/test_ci_contract.py", globals())
_phase1_policy = policy
_phase1_preflight = preflight
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
    return frozenset(allowed)


def check_changed_paths(paths, unit, changed):
    require(changed <= effective_paths(paths, unit), "work_unit_allowlist_exceeded")


def policy(value):
    """Validate only enumerated migration deltas, then run every old rule."""
    try:
        v = copy.deepcopy(value)
        require(v["name"] == "Phase 2 cumulative CI", "phase_name")
        v["name"] = "Phase 1 scaffold CI"
        require(v["concurrency"]["group"] == "phase2-${{ github.event.pull_request.number || github.ref }}", "phase_concurrency")
        v["concurrency"]["group"] = "phase1-${{ github.event.pull_request.number || github.ref }}"
        job = v["jobs"]["scaffold"]
        require(job["name"] == "preparation (${{ matrix.os }}, Python ${{ matrix.python }})", "phase_job")
        job["name"] = "scaffold (${{ matrix.os }}, Python ${{ matrix.python }})"
        steps = job["steps"]
        require(len(steps) == 7, "step_count")
        require(steps[0]["with"]["fetch-depth"] == 0, "complete_history_required")
        steps[0]["with"]["fetch-depth"] = 1
        require(steps[4]["name"] == "Collect and run all cumulative tests", "cumulative_test_stage")
        steps[4]["name"] = "Collect and run all scaffold and security tests"
        require(steps[6]["with"]["name"] == "phase2-${{ matrix.os }}-py${{ matrix.python }}-${{ github.run_id }}-${{ github.run_attempt }}", "artifact_identity")
        steps[6]["with"]["name"] = "phase1-${{ matrix.os }}-py${{ matrix.python }}-${{ github.run_id }}-${{ github.run_attempt }}"
        expected = "${{ runner.temp }}/sit-p2/evidence/*.json\n${{ runner.temp }}/sit-p2/evidence/*.xml\n${{ runner.temp }}/sit-p2/evidence/*.log"
        require(steps[6]["with"]["path"] == expected, "artifact_scope")
        steps[6]["with"]["path"] = expected.replace("sit-p2", "sit-w06")
        _phase1_policy(v)
    except (KeyError, TypeError, IndexError) as exc:
        raise ValueError("malformed_workflow") from exc


def resolve_unit(event_name, event, head):
    """Mechanical unit context from runner event, never candidate metadata."""
    if event_name == "pull_request":
        pr = event["pull_request"]
        require(pr["head"]["sha"] == head, "event_head_mismatch")
        match = re.fullmatch(r"phase2/p2-w0([1-9])", pr["head"]["ref"])
        require(match is not None, "review_branch_requires_explicit_unit")
        unit = "P2-W0" + match[1]
        base = pr["base"]["sha"]
    else:
        require(event_name == "push" and event["ref"] == "refs/heads/main", "unsupported_event")
        require(event["head_commit"]["id"] == head, "event_head_mismatch")
        marks = re.findall(r"^SIT-Phase-Unit: (P2-W0[1-9])$", event["head_commit"]["message"], re.M)
        require(len(marks) == 1, "main_merge_requires_unit_footer")
        unit, base = marks[0], event["before"]
    require(re.fullmatch(r"[0-9a-f]{40}", base) is not None, "invalid_base_sha")
    return unit, base


def configure_context():
    event = json.loads(Path(os.environ["GITHUB_EVENT_PATH"]).read_bytes(), object_pairs_hook=unique)
    unit, base = resolve_unit(os.environ["GITHUB_EVENT_NAME"], event, os.environ["SIT_REVIEW_HEAD"])
    os.environ["SIT_PHASE_UNIT"] = unit
    return unit, base


def ci_paths():
    require(os.environ.get("GITHUB_ACTIONS") == "true", "explicit Actions invocation required")
    base = Path(os.environ["RUNNER_TEMP"]) / "sit-p2"
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
            (["P2-W05-R01", "P2-W05-R02"] if phase_guard.unit_number(unit) >= 5 else []),
        "provenance": "Full local Git commit archives and actual checkout, not substituted artifact metadata"})


def preflight(base, evidence):
    entry_and_scope(evidence)
    policy(read_workflow())
    head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    require(head == os.environ["SIT_REVIEW_HEAD"], "wrong_checked_commit")
    require(f"{sys.version_info.major}.{sys.version_info.minor}" == os.environ["SIT_MATRIX_PYTHON"], "wrong_Python_minor")
    save(evidence / "environment.json", {"head": head, "python": sys.version, "platform": platform.platform(),
        "matrix_os": os.environ["SIT_MATRIX_OS"], "matrix_python": os.environ["SIT_MATRIX_PYTHON"],
        "run_id": os.environ["GITHUB_RUN_ID"], "run_attempt": os.environ["GITHUB_RUN_ATTEMPT"],
        "image_version": os.environ.get("ImageVersion"), "scope": "Phase 2 cumulative verification",
        "unit": os.environ["SIT_PHASE_UNIT"]})
    save(evidence / "tracked-before.json", tracked_bytes())
    for tool in ("check_phase0_baseline", "check_scaffold_boundary"):
        run([sys.executable, "-B", "tools/" + tool + ".py"], evidence, tool + "-before")
    save(evidence / "preflight.json", {"ok": True, "actual_frozen_files_checked": 20,
        "actual_entry_files_checked": 125, "actual_phase1_files_checked": 124, "modules": 48})


def suite_paths():
    scopes = [s for s in ALL_SCOPES if (ROOT / s).is_dir()]
    require(all(s in scopes for s in ALL_SCOPES[:3]), "required_test_directory_missing")
    return scopes


def collection_check(nodes, expected_files):
    require(len(nodes) == len(set(nodes)) and nodes, "incomplete_or_duplicate_collection")
    require({n.split("::", 1)[0] for n in nodes} == expected_files, "test_file_omitted")
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
        "historical_retained": 194, "scope": "all present scaffold/security/contract/unit/integration directories"})
    result = run([python, "-m", "pytest", *scopes, "-q", "--basetemp", base / "pytest",
                  "--junitxml", evidence / "junit.xml"], evidence, "pytest", env=env, timeout=900, check=False)
    save(evidence / "pytest-exit.json", {"exit_code": result.returncode})
    require(result.returncode == 0, "accumulated_suite_failed")


def evidence_report(base, evidence):
    summary = {"scope": "Phase 2 cumulative verification; W01 does not implement product behavior",
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
    unchanged = before_file.exists() and json.loads(before_file.read_bytes()) == tracked_bytes()
    summary["tracked_bytes_unchanged"] = unchanged
    guards_ok = True
    for tool in ("check_phase0_baseline", "check_scaffold_boundary"):
        outcome = run([sys.executable, "-B", "tools/" + tool + ".py"], evidence, tool + "-after", check=False)
        guards_ok = guards_ok and outcome.returncode == 0
    entry_and_scope(evidence)
    exit_record = evidence / "pytest-exit.json"
    summary.update(guards_pass=guards_ok, archive_count=len(archives), historical_retained=194)
    summary["pass"] = bool(unchanged and guards_ok and collection.exists() and exit_record.exists() and
        summary.get("tests") == json.loads(collection.read_bytes())["count"] and
        all(summary.get(k) == 0 for k in ("failures", "errors", "skipped")) and
        json.loads(exit_record.read_bytes())["exit_code"] == 0 and len(archives) >= 3)
    save(evidence / "summary.json", summary)
    print("P2_SUMMARY " + json.dumps(summary, sort_keys=True), flush=True)
    with open(os.environ["GITHUB_STEP_SUMMARY"], "a", encoding="utf-8") as output:
        output.write("## Phase 2 cumulative verification\n\n```json\n" + json.dumps(summary, indent=2) + "\n```\n")
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
