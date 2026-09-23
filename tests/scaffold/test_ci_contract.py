# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Cumulative Phase 3 CI, retaining the complete accepted predecessor suite."""
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
    return frozenset(allowed)


def phase3_scope_exceptions(unit):
    """Name accepted cumulative amendments without granting later edit rights."""
    current = phase_guard.phase3_unit_number(unit)
    return ((["P3-W04-R01"] if current >= 4 else []) + (["P3-W05-R01"] if current >= 5 else []) +
            (["P3-W06-R01"] if current >= 6 else []) + (["P3-W08-R01"] if current >= 8 else []) +
            (["P3-W09-R01"] if current >= 9 else []) + (["P3-W11-R01"] if current >= 11 else []))


def phase3_check_changed_paths(paths, unit, changed):
    require(changed <= phase3_effective_paths(paths, unit), "work_unit_allowlist_exceeded")


def check_entry_bytes(entry_files, actual, allowed):
    """Check every entry byte outside scope and account for every added path."""
    require(set(entry_files) <= set(actual) <= set(entry_files) | set(allowed), "tracked_path_accounting")
    require(all(actual[p] == h for p, h in entry_files.items() if p not in allowed), "frozen_entry_byte_changed")


def policy(value):
    """Validate only enumerated migration deltas, then run every old rule."""
    try:
        v = copy.deepcopy(value)
        require(v["name"] == "Phase 3 cumulative CI", "phase_name")
        v["name"] = "Phase 1 scaffold CI"
        require(v["concurrency"]["group"] == "phase3-${{ github.event.pull_request.number || github.ref }}", "phase_concurrency")
        v["concurrency"]["group"] = "phase1-${{ github.event.pull_request.number || github.ref }}"
        job = v["jobs"]["scaffold"]
        require(type(job["timeout-minutes"]) is int and job["timeout-minutes"] == 40, "phase_job_timeout")
        job["timeout-minutes"] = 25
        require(job["name"] == "analytical core (${{ matrix.os }}, Python ${{ matrix.python }})", "phase_job")
        job["name"] = "scaffold (${{ matrix.os }}, Python ${{ matrix.python }})"
        steps = job["steps"]
        require(len(steps) == 7, "step_count")
        require(steps[0]["with"]["fetch-depth"] == 0, "complete_history_required")
        steps[0]["with"]["fetch-depth"] = 1
        require(steps[4]["name"] == "Collect and run all cumulative tests", "cumulative_test_stage")
        steps[4]["name"] = "Collect and run all scaffold and security tests"
        require(steps[6]["with"]["name"] == "phase3-${{ matrix.os }}-py${{ matrix.python }}-${{ github.run_id }}-${{ github.run_attempt }}", "artifact_identity")
        steps[6]["with"]["name"] = "phase1-${{ matrix.os }}-py${{ matrix.python }}-${{ github.run_id }}-${{ github.run_attempt }}"
        expected = "${{ runner.temp }}/sit-p3/evidence/*.json\n${{ runner.temp }}/sit-p3/evidence/*.xml\n${{ runner.temp }}/sit-p3/evidence/*.log"
        require(steps[6]["with"]["path"] == expected, "artifact_scope")
        steps[6]["with"]["path"] = expected.replace("sit-p3", "sit-w06")
        _phase1_policy(v)
    except (KeyError, TypeError, IndexError) as exc:
        raise ValueError("malformed_workflow") from exc


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
    previous, segments = intake, []
    for step, merge in enumerate(accepted, 1):
        parents = git_text("show", "-s", "--format=%P", merge).split()
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
        commits = git_text("rev-list", "--reverse", "--topo-order", predecessor + ".." + successor).splitlines()
        for commit in commits:
            require(commit not in seen, "duplicate_history_commit")
            seen.add(commit)
            require_ancestor(intake, commit)
            parents = git_text("show", "-s", "--format=%P", commit).split()
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
            require(changed <= allowed, "intermediate_work_unit_allowlist_exceeded")
            actual = commit_hashes(commit)
            check_entry_bytes(entry["files"], actual, cumulative)
            records.append({"commit": commit, "tree": git_text("rev-parse", commit + "^{tree}"),
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
                  "--junitxml", evidence / "junit.xml"], evidence, "pytest", env=env, timeout=1800, check=False)
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
