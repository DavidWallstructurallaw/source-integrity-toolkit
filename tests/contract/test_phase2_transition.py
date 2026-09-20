# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""P2-W01 controls and deliberate counterexamples; no product input processing."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools import check_scaffold_boundary as guard


def ci_driver():
    spec = importlib.util.spec_from_file_location("phase2_ci_test_driver", ROOT / "tests/scaffold/test_ci_contract.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Phase2TransitionTests(unittest.TestCase):
    def setUp(self):
        self.policy = json.loads((ROOT / "phase2/module_policy.json").read_bytes())

    def workspace(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        root = Path(temp.name)
        shutil.copytree(ROOT / "src/source_integrity_toolkit", root / "src/source_integrity_toolkit")
        for name in ("PHASE_2_PLAN.md", "phase2/entry_manifest.json", "phase2/module_policy.json", "scaffold/delivery_manifest.json"):
            target = root / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / name, target)
        return root

    def test_independent_plan_and_entry_pins(self):
        self.assertEqual(hashlib.sha256((ROOT / "PHASE_2_PLAN.md").read_bytes()).hexdigest(), guard.PLAN_SHA256)
        entry = guard.entry_manifest(ROOT)
        self.assertEqual(entry["file_count"], 125)
        self.assertEqual(entry["intake_commit"], guard.INTAKE)

    def test_first_units_match_exact_plan_paths(self):
        paths = guard.plan_paths(ROOT)
        actual = {}
        for unit, names in paths.items():
            for name in names:
                if name.startswith("src/source_integrity_toolkit/"):
                    actual.setdefault(name.removeprefix("src/source_integrity_toolkit/"), int(unit[-1]))
        self.assertEqual(actual, guard.FIRST_UNIT)
        self.assertEqual(len(paths["P2-W01"]), 16)
        self.assertFalse(any(p.startswith("src/") or p.endswith(".schema.json") for p in paths["P2-W01"]))

    def test_actual_module_policy_and_remaining_protection(self):
        active = guard.promotions(ROOT)
        self.assertLessEqual(active, set(guard.FIRST_UNIT))
        self.assertEqual(len(guard.EXPECTED_PATHS - set(guard.FIRST_UNIT)), 35)
        outcome = guard.check_repository(ROOT)
        self.assertTrue(outcome["ok"], outcome)
        self.assertEqual(outcome["checked_modules"], 48)
        self.assertEqual(outcome["protected_modules"], 48 - len(active))

    def test_w01_has_no_product_promotion(self):
        value = copy.deepcopy(self.policy)
        value["active_unit"], value["promotions"] = "P2-W01", []
        self.assertEqual(guard.policy_promotions(value, "P2-W01"), frozenset())
        value["promotions"] = [{"path": "contracts/bundle.py", "unit": 2}]
        with self.assertRaises(ValueError):
            guard.policy_promotions(value, "P2-W01")

    def test_policy_cannot_advance_trusted_unit(self):
        value = copy.deepcopy(self.policy)
        value["active_unit"], value["promotions"] = "P2-W02", []
        with self.assertRaises(ValueError):
            guard.policy_promotions(value, "P2-W01")

    def test_unlisted_module_cannot_be_added_to_policy(self):
        value = copy.deepcopy(self.policy)
        value["first_units"]["analysis/origins.py"] = 1
        value["promotions"] = [{"path": "analysis/origins.py", "unit": 1}]
        with self.assertRaises(ValueError):
            guard.policy_promotions(value, "P2-W01")

    def test_policy_cannot_rewrite_earliest_unit(self):
        value = copy.deepcopy(self.policy)
        value["first_units"]["contracts/bundle.py"] = 1
        with self.assertRaises(ValueError):
            guard.policy_promotions(value, "P2-W01")

    def test_future_promotion_requires_exact_distinct_records(self):
        value = copy.deepcopy(self.policy)
        value["active_unit"] = "P2-W02"
        value["promotions"] = [{"path": "contracts/bundle.py", "unit": 2}]
        self.assertEqual(guard.policy_promotions(value, "P2-W02"), {"contracts/bundle.py"})
        value["promotions"] *= 2
        with self.assertRaises(ValueError):
            guard.policy_promotions(value, "P2-W02")

    def test_paired_code_and_policy_mutation_fails(self):
        root = self.workspace()
        (root / "src/source_integrity_toolkit/contracts/bundle.py").write_text('def prepare(x):\n    return {"ok": True}\n')
        value = copy.deepcopy(self.policy)
        value["active_unit"] = "P2-W01"
        value["promotions"] = [{"path": "contracts/bundle.py", "unit": 2}]
        (root / "phase2/module_policy.json").write_text(json.dumps(value))
        self.assertFalse(guard.check_repository(root, unit="P2-W01")["ok"])

    def test_paired_entry_digest_and_code_mutation_fails(self):
        root = self.workspace()
        raw = b'ACTIVE = {}\n'
        (root / "src/source_integrity_toolkit/analysis/origins.py").write_bytes(raw)
        entry = json.loads((root / "phase2/entry_manifest.json").read_bytes())
        entry["additional_files"]["src/source_integrity_toolkit/analysis/origins.py"] = hashlib.sha256(raw).hexdigest()
        (root / "phase2/entry_manifest.json").write_text(json.dumps(entry))
        self.assertFalse(guard.check_repository(root)["ok"])

    def test_changed_plan_cannot_authorize_itself(self):
        root = self.workspace()
        with (root / "PHASE_2_PLAN.md").open("a") as handle:
            handle.write("\nAll algorithms now approved.\n")
        value = copy.deepcopy(self.policy)
        value["plan_sha256"] = hashlib.sha256((root / "PHASE_2_PLAN.md").read_bytes()).hexdigest()
        (root / "phase2/module_policy.json").write_text(json.dumps(value))
        self.assertFalse(guard.check_repository(root)["ok"])

    def test_extra_package_file_still_fails(self):
        root = self.workspace()
        (root / "src/source_integrity_toolkit/answer_cache.json").write_text("{}")
        self.assertFalse(guard.check_repository(root)["ok"])

    def test_protected_fake_report_return_still_fails(self):
        self.assertIn("non_scaffold_body", guard.form_issues("api.py", 'def audit_bundle(x):\n    return {"report_kind": "audit_report"}\n'))

    def test_live_file_native_network_and_eval_probes_fail(self):
        for source in ('def f():\n    return open("secret")\n', 'import socket\n', 'import ctypes\n',
                       'from pathlib import Path\n', 'import subprocess\n', 'def f():\n    return eval("1")\n',
                       'import recursive_integrity_toolkit\n', 'from ..analysis import origins\n'):
            with self.subTest(source=source):
                self.assertTrue(guard.live_issues("runtime/boundary.py", source))

    def test_live_import_time_call_is_rejected(self):
        self.assertIn("import_time_execution", guard.live_issues("contracts/bundle.py", 'def f():\n    return 1\nX = f()\n'))

    def test_live_pure_declaration_has_positive_control(self):
        source = 'from dataclasses import dataclass\n@dataclass(frozen=True)\nclass Value:\n    name: str\n'
        self.assertEqual(guard.live_issues("contracts/bundle.py", source), [])

    def test_live_import_cycle_is_not_hidden_by_promotion(self):
        sources = {"contracts/bundle.py": "from . import evidence\n", "contracts/evidence.py": "from . import bundle\n"}
        self.assertEqual(guard.import_cycle_issues(sources), ["import_cycle"])

    def test_duplicate_policy_key_and_invalid_unit_fail(self):
        with self.assertRaises(ValueError):
            json.loads('{"promotions": [], "promotions": []}', object_pairs_hook=guard.unique)
        for unit in ("P2-W10", "P3-W01", "P2-W01; echo injected", 1):
            with self.assertRaises(ValueError):
                guard.unit_number(unit)

    def test_historical_identity_ledger_is_complete(self):
        nodes = guard.historical_nodes(ROOT)
        self.assertEqual(len(nodes), 194)
        self.assertTrue(any("test_scaffold_no_native_loading" in n for n in nodes))

    def test_omitted_historical_identity_fails(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "phase2").mkdir()
            lines = (ROOT / "phase2/transition_ledger.md").read_text().splitlines()
            index = next(i for i, line in enumerate(lines) if line.startswith("| `tests/") and "::" in line)
            lines.pop(index)
            (root / "phase2/transition_ledger.md").write_text("\n".join(lines))
            with self.assertRaises(ValueError):
                guard.historical_nodes(root)

    def test_unlisted_historical_source_cannot_execute(self):
        with self.assertRaises(ValueError):
            guard.load_phase1_test("../../arbitrary.py", globals())

    def test_altered_historical_test_bytes_cannot_execute(self):
        namespace = {"__file__": str(ROOT / "tests/scaffold/test_imports.py"), "__name__": "probe"}
        with patch.object(guard.subprocess, "check_output", return_value=b'raise RuntimeError("executed")'):
            with self.assertRaises(ValueError):
                guard.load_phase1_test("tests/scaffold/test_imports.py", namespace)

    def test_component_evidence_cannot_close_domain_traces(self):
        value = json.loads((ROOT / "phase2/implementation_evidence.json").read_bytes())
        self.assertEqual(value["domain_traces_closed"], [])
        self.assertEqual(value["public_audit"], "unchanged_refusal")
        self.assertEqual({r["path"] for r in value["components"]}, set(guard.FIRST_UNIT))
        for row in value["components"]:
            self.assertEqual(row["first_unit"], guard.FIRST_UNIT[row["path"]])
        active = guard.promotions(ROOT)
        for row in value["components"]:
            if row["path"] not in active:
                self.assertEqual((row["implementation"], row["behavior_tests"], row["evidence"]), ("pending", "pending", []))

    def test_ci_unit_comes_from_exact_review_event(self):
        ci = ci_driver()
        head, base = "a" * 40, "b" * 40
        event = {"pull_request": {"head": {"sha": head, "ref": "phase2/p2-w01"}, "base": {"sha": base}}}
        self.assertEqual(ci.resolve_unit("pull_request", event, head), ("P2-W01", base))
        event["pull_request"]["head"]["ref"] = "phase2/p2-w02; injected"
        with self.assertRaises(ValueError):
            ci.resolve_unit("pull_request", event, head)

    def test_main_requires_single_explicit_unit_footer(self):
        ci = ci_driver()
        head, base = "a" * 40, "b" * 40
        event = {"ref": "refs/heads/main", "before": base, "head_commit": {"id": head, "message": "Merge\n\nSIT-Phase-Unit: P2-W01"}}
        self.assertEqual(ci.resolve_unit("push", event, head), ("P2-W01", base))
        event["head_commit"]["message"] += "\nSIT-Phase-Unit: P2-W02"
        with self.assertRaises(ValueError):
            ci.resolve_unit("push", event, head)

    def test_cumulative_collection_preserves_all_old_identities(self):
        ci = ci_driver()
        nodes = sorted(guard.historical_nodes(ROOT))
        nodes.append("tests/contract/test_phase2_transition.py::Phase2TransitionTests::test_historical_identity_ledger_is_complete")
        files = {n.split("::")[0] for n in nodes}
        ci.collection_check(nodes, files)
        with self.assertRaises(ValueError):
            ci.collection_check(nodes[1:], files)
        with self.assertRaises(ValueError):
            ci.collection_check(nodes + nodes[:1], files)

    def test_cumulative_scope_and_workflow_are_closed(self):
        ci = ci_driver()
        self.assertEqual(ci.ALL_SCOPES, ("tests/scaffold", "tests/security", "tests/contract", "tests/unit", "tests/integration"))
        ci.policy(ci.read_workflow())
        value = copy.deepcopy(ci.read_workflow())
        value["jobs"]["scaffold"]["steps"][0]["with"]["fetch-depth"] = 1
        with self.assertRaises(ValueError):
            ci.policy(value)


class W07R01Tests(unittest.TestCase):
    """Pinned repair regressions; no broad stage permission or product repair."""
    ENTRY = "067802f8df5b6958adde60bc7ced3ca8a06a7f33"
    ACCEPTED = "4f55252d98f9b57975c2bc241c9079ac259a53cd"
    EXTRA = frozenset((
        "phase2/module_policy.json", "tests/scaffold/test_ci_contract.py",
        "tests/contract/test_bundle_contract.py", "tests/security/test_input_capture.py",
        "tests/contract/test_input_schema_mapping.py", "phase2/transition_ledger.md",
    ))

    def old_bytes(self, path, expected_blob):
        import subprocess
        raw = subprocess.check_output(["git", "show", self.ENTRY + ":" + path],
                                      cwd=ROOT, stderr=subprocess.PIPE, timeout=30)
        self.assertEqual(guard.git_blob(raw), expected_blob)
        return raw

    def test_actual_policy_only_changes_the_trusted_active_context(self):
        raw = self.old_bytes("phase2/module_policy.json", "6b2d5a0f14bd840c3a894805524fb98df4652ecd")
        current = guard.unit_number()
        self.assertIn(current, (7, 8, 9))
        # Later trusted contexts still need their own path authorization.
        expected = raw.replace(b'"active_unit": "P2-W06"',
                               ('"active_unit": "P2-W%02d"' % current).encode())
        self.assertEqual((ROOT / "phase2/module_policy.json").read_bytes(), expected)
        value = json.loads(expected)
        self.assertEqual(len(guard.policy_promotions(value)), 13)
        self.assertEqual(value["promotions"], json.loads(raw)["promotions"])

    def test_policy_mismatch_and_new_promotions_still_fail(self):
        raw = self.old_bytes("phase2/module_policy.json", "6b2d5a0f14bd840c3a894805524fb98df4652ecd")
        value = json.loads(raw)
        with self.assertRaisesRegex(ValueError, "^policy_cannot_select_unit$"):
            guard.policy_promotions(value, "P2-W07")
        value["active_unit"] = "P2-W07"
        self.assertEqual(guard.policy_promotions(value, "P2-W07"), frozenset(guard.FIRST_UNIT))
        for trusted in ("P2-W06", "P2-W08", "P2-W09"):
            with self.assertRaisesRegex(ValueError, "^policy_cannot_select_unit$"):
                guard.policy_promotions(value, trusted)
        value["promotions"].append({"path": "analysis/origins.py", "unit": 7})
        with self.assertRaises(ValueError): guard.policy_promotions(value, "P2-W07")
        value["first_units"]["analysis/origins.py"] = 7
        with self.assertRaises(ValueError): guard.policy_promotions(value, "P2-W07")

    def test_exact_six_paths_are_w07_only_and_history_is_cumulative(self):
        ci = ci_driver(); paths = guard.plan_paths(ROOT)
        self.assertEqual(ci.P2_W07_R01_PATHS, self.EXTRA)
        self.assertEqual(len(paths["P2-W07"]), 12)
        self.assertFalse(paths["P2-W07"] & self.EXTRA)
        cumulative = set()
        for step in range(1, 10):
            unit = f"P2-W{step:02}"
            extra = (ci.P2_W02_R01_PATHS if step == 2 else
                     ci.P2_W04_R01_PATHS if step == 4 else
                     ci.P2_W05_R01_PATHS | ci.P2_W05_R02_PATHS if step == 5 else
                     self.EXTRA if step == 7 else frozenset())
            if step == 8:
                extra = extra | ci.P2_W08_R01_PATHS
            expected = paths[unit] | extra
            self.assertEqual(ci.effective_paths(paths, unit), expected)
            ci.check_changed_paths(paths, unit, expected)
            for path in self.EXTRA - expected:
                with self.assertRaisesRegex(ValueError, "^work_unit_allowlist_exceeded$"):
                    ci.check_changed_paths(paths, unit, {path})
            cumulative.update(expected)
            self.assertEqual(ci.effective_paths(paths, unit, cumulative=True), cumulative)

    def test_similar_paths_and_product_repairs_have_no_w07_permission(self):
        ci = ci_driver(); paths = guard.plan_paths(ROOT)
        allowed = ci.effective_paths(paths, "P2-W07")
        for path in ("phase2/module_policy.json.bak", "phase2/../phase2/module_policy.json",
                     "tests/security/test_scaffold_inertness.py", "PHASE_2_PLAN.md",
                     "src/source_integrity_toolkit/runtime/boundary.py",
                     "src/source_integrity_toolkit/validation/structure.py",
                     "tools/check_scaffold_boundary.py", ".github/workflows/phase1-ci.yml"):
            with self.assertRaisesRegex(ValueError, "^work_unit_allowlist_exceeded$"):
                ci.check_changed_paths(paths, "P2-W07", allowed | {path})

    def test_only_four_named_permission_test_bodies_change(self):
        changes = [('tests/contract/test_bundle_contract.py', '2d931416c63c25c80ee419901af1e4bd0022e768', [['        assert ci.effective_paths(paths, unit) == paths[unit] | extra\n', '        if step == 7:\n            extra = extra | ci.P2_W07_R01_PATHS\n        assert ci.effective_paths(paths, unit) == paths[unit] | extra\n'], ['        assert ci.effective_paths(paths, unit, cumulative=True) == original | extras\n', '        if step >= 7:\n            extras = extras | ci.P2_W07_R01_PATHS\n        assert ci.effective_paths(paths, unit, cumulative=True) == original | extras\n']]), ('tests/security/test_input_capture.py', 'dcc72efe086ac8a57e491d70f0cd6780344bcfb9', [['        assert ci.effective_paths(paths,unit)==paths[unit]|extra\n', '        if step==7: extra=extra | ci.P2_W07_R01_PATHS\n        assert ci.effective_paths(paths,unit)==paths[unit]|extra\n'], ['        assert ci.effective_paths(paths,unit,cumulative=True)==cumulative\n', '        if step>=7: cumulative.update(ci.P2_W07_R01_PATHS)\n        assert ci.effective_paths(paths,unit,cumulative=True)==cumulative\n']]), ('tests/contract/test_input_schema_mapping.py', '724f5f403f22dea6101305675b00212064227031', [['        assert ci.effective_paths(paths, unit) == paths[unit] | authorized\n', '        if i == 7:\n            authorized = authorized | ci.P2_W07_R01_PATHS\n        assert ci.effective_paths(paths, unit) == paths[unit] | authorized\n']])]
        for path, pin, replacements in changes:
            expected = self.old_bytes(path, pin)
            for before, after in replacements:
                self.assertEqual(expected.count(before.encode()), 1)
                expected = expected.replace(before.encode(), after.encode())
            self.assertEqual(W08R01Tests().pre_w08_bytes(path), expected)

    def test_ci_context_collection_and_failure_controls_are_unchanged(self):
        path = "tests/scaffold/test_ci_contract.py"
        expected = self.old_bytes(path, "c7b5fc7338fa4c4e08d0ba54ce0a7e87b66901ab")
        replacements = [['def effective_paths(paths, unit, *, cumulative=False):', '# Explicit owner-approved P2-W07-R01: phase-context metadata and scope tests.\n# Only W07 gains these immediate paths; later units retain cumulative history.\nP2_W07_R01_PATHS = frozenset((\n    "phase2/module_policy.json",\n    "tests/scaffold/test_ci_contract.py",\n    "tests/contract/test_bundle_contract.py",\n    "tests/security/test_input_capture.py",\n    "tests/contract/test_input_schema_mapping.py",\n    "phase2/transition_ledger.md",\n))\n\ndef effective_paths(paths, unit, *, cumulative=False):'], ['            allowed.update(P2_W05_R02_PATHS)\n', '            allowed.update(P2_W05_R02_PATHS)\n        if step == 7:\n            allowed.update(P2_W07_R01_PATHS)\n'], ['            (["P2-W05-R01", "P2-W05-R02"] if phase_guard.unit_number(unit) >= 5 else []),', '            (["P2-W05-R01", "P2-W05-R02"] if phase_guard.unit_number(unit) >= 5 else []) +\n            (["P2-W07-R01"] if phase_guard.unit_number(unit) >= 7 else []),']]
        for before, after in replacements:
            self.assertEqual(expected.count(before.encode()), 1)
            expected = expected.replace(before.encode(), after.encode())
        self.assertEqual(W08R01Tests().pre_w08_bytes(path), expected)
        ci = ci_driver(); head, base = "a" * 40, "b" * 40
        event = {"pull_request": {"head": {"sha": head, "ref": "phase2/p2-w07"}, "base": {"sha": base}}}
        self.assertEqual(ci.resolve_unit("pull_request", event, head), ("P2-W07", base))
        with self.assertRaises(ValueError): ci.resolve_unit("pull_request", event, base)

    def test_ledger_is_append_only_with_all_four_permission_transitions(self):
        raw = self.old_bytes("phase2/transition_ledger.md", "51f022d8df2d312329c2b65730e1bce38df3c17a")
        current = (ROOT / "phase2/transition_ledger.md").read_bytes()
        self.assertTrue(current.startswith(raw))
        added = current[len(raw):].decode()
        self.assertIn("## P2-W07-R01:", added)
        for name in ("test_repair_does_not_expand_another_units_immediate_diff",
                     "test_repair_cumulative_accounting_retains_only_authorized_extras",
                     "test_r01_exact_four_paths_and_no_other_unit_permission_expansion",
                     "test_r02_exact_extra_path_and_other_units_keep_their_immediate_scope"):
            self.assertIn(name, added)
        self.assertEqual(len(guard.historical_nodes(ROOT)), 194)

    def test_all_product_bytes_and_the_checker_remain_accepted(self):
        import subprocess
        raw = subprocess.check_output(["git", "ls-tree", "-r", "-z", self.ACCEPTED,
                                       "src/source_integrity_toolkit", "tools/check_scaffold_boundary.py"],
                                      cwd=ROOT, stderr=subprocess.PIPE, timeout=30)
        entries = [row.split(b"\t", 1) for row in raw.split(b"\0") if row]
        self.assertEqual(len(entries), 49)
        for meta, path in entries:
            mode, kind, sha = meta.decode().split()
            self.assertEqual((mode, kind), ("100644", "blob"))
            self.assertEqual(guard.git_blob((ROOT / path.decode()).read_bytes()), sha)

    def test_prior_phase2_transition_tests_keep_every_statement(self):
        import ast
        path = "tests/contract/test_phase2_transition.py"
        raw = self.old_bytes(path, "0ab96292e4a03cc5bc065374e5b1934d5ffce259")
        old, new = ast.parse(raw), ast.parse((ROOT / path).read_bytes())
        added = [n for n in new.body if isinstance(n, ast.ClassDef) and n.name == "W07R01Tests"]
        self.assertEqual(len(added), 1)
        new.body.remove(added[0])
        repair = [n for n in new.body if isinstance(n, ast.ClassDef) and n.name == "W08R01Tests"]
        self.assertEqual(len(repair), 1)
        new.body.remove(repair[0])
        self.assertEqual(ast.dump(old, include_attributes=False), ast.dump(new, include_attributes=False))


class W08R01Tests(unittest.TestCase):
    """Exact authorized transition and installed-runtime regression witnesses."""
    ENTRY = "a6847f90a32a4d478146f392acf83f49c84002c2"
    ACCEPTED = "22bd51454e425cf9eca87adbebecb09191fb925d"
    EXTRA = frozenset(('phase2/module_policy.json', 'tests/contract/test_bundle_contract.py', 'tests/security/test_input_capture.py', 'tests/contract/test_input_schema_mapping.py', 'tests/contract/test_phase2_transition.py', 'tests/security/test_preparation_inertness.py', 'phase2/transition_ledger.md'))
    PINS = {'tests/scaffold/test_ci_contract.py': '5928105beb8c16dff00371ac7d74d9810af9f498', 'tests/contract/test_bundle_contract.py': '46891e95b21ff33fa3f6aed8add65870710e6ca6', 'tests/security/test_input_capture.py': 'b95a96fde09efaa9c360542163e6c3a81c5ebb63', 'tests/contract/test_input_schema_mapping.py': '6dd1c91bec3df36f59c29a8f653fab0f899c09ea', 'tests/contract/test_phase2_transition.py': 'f83b8d553d353733d11b655fe02a53834f93be07', 'tests/security/test_preparation_inertness.py': '597df4a8467d4d29e13fbcf9dc92a80d5778a86b'}
    PATCHES = {'tests/scaffold/test_ci_contract.py': [('def effective_paths(paths, unit, *, cumulative=False):', '# Explicit owner-approved P2-W08-R01: exact W08 transition only.\n# Other units retain their own immediate scopes; history stays cumulative.\nP2_W08_R01_PATHS = frozenset((\n    "phase2/module_policy.json",\n    "tests/contract/test_bundle_contract.py",\n    "tests/security/test_input_capture.py",\n    "tests/contract/test_input_schema_mapping.py",\n    "tests/contract/test_phase2_transition.py",\n    "tests/security/test_preparation_inertness.py",\n    "phase2/transition_ledger.md",\n))\n\ndef effective_paths(paths, unit, *, cumulative=False):'), ('            allowed.update(P2_W07_R01_PATHS)\n', '            allowed.update(P2_W07_R01_PATHS)\n        if step == 8:\n            allowed.update(P2_W08_R01_PATHS)\n'), ('            (["P2-W07-R01"] if phase_guard.unit_number(unit) >= 7 else []),', '            (["P2-W07-R01"] if phase_guard.unit_number(unit) >= 7 else []) +\n            (["P2-W08-R01"] if phase_guard.unit_number(unit) >= 8 else []),')], 'tests/contract/test_bundle_contract.py': [('        assert ci.effective_paths(paths, unit) == paths[unit] | extra\n', '        if step == 8:\n            extra = extra | ci.P2_W08_R01_PATHS\n        assert ci.effective_paths(paths, unit) == paths[unit] | extra\n'), ('        assert ci.effective_paths(paths, unit, cumulative=True) == original | extras\n', '        if step >= 8:\n            extras = extras | ci.P2_W08_R01_PATHS\n        assert ci.effective_paths(paths, unit, cumulative=True) == original | extras\n')], 'tests/security/test_input_capture.py': [('        assert ci.effective_paths(paths,unit)==paths[unit]|extra\n', '        if step==8: extra=extra | ci.P2_W08_R01_PATHS\n        assert ci.effective_paths(paths,unit)==paths[unit]|extra\n'), ('        assert ci.effective_paths(paths,unit,cumulative=True)==cumulative\n', '        if step>=8: cumulative.update(ci.P2_W08_R01_PATHS)\n        assert ci.effective_paths(paths,unit,cumulative=True)==cumulative\n')], 'tests/contract/test_input_schema_mapping.py': [('        assert ci.effective_paths(paths, unit) == paths[unit] | authorized\n', '        if i == 8:\n            authorized = authorized | ci.P2_W08_R01_PATHS\n        assert ci.effective_paths(paths, unit) == paths[unit] | authorized\n')], 'tests/security/test_preparation_inertness.py': [('    assert guard.check_repository(ROOT, unit="P2-W07")["ok"]\n    root = tmp_path', '    unit = f"P2-W{guard.unit_number():02}"\n    assert guard.check_repository(ROOT, unit=unit)["ok"]\n    root = tmp_path'), ('    assert guard.check_repository(root, unit="P2-W07")["ok"]', '    assert guard.check_repository(root, unit=unit)["ok"]'), ('    assert not guard.check_repository(root, unit="P2-W07")["ok"]', '    assert not guard.check_repository(root, unit=unit)["ok"]'), ('    assert guard.check_repository(ROOT, unit="P2-W07")["ok"]', '    assert guard.check_repository(ROOT, unit=unit)["ok"]')]}
    TRANSITION_EDITS = [('            expected = paths[unit] | extra\n', '            if step == 8:\n                extra = extra | ci.P2_W08_R01_PATHS\n            expected = paths[unit] | extra\n'), ('            self.assertEqual((ROOT / path).read_bytes(), expected)\n', '            self.assertEqual(W08R01Tests().pre_w08_bytes(path), expected)\n'), ('        self.assertEqual((ROOT / path).read_bytes(), expected)\n        ci = ci_driver(); head, base', '        self.assertEqual(W08R01Tests().pre_w08_bytes(path), expected)\n        ci = ci_driver(); head, base'), ('        new.body.remove(added[0])\n        self.assertEqual(ast.dump(old, include_attributes=False), ast.dump(new, include_attributes=False))', '        new.body.remove(added[0])\n        repair = [n for n in new.body if isinstance(n, ast.ClassDef) and n.name == "W08R01Tests"]\n        self.assertEqual(len(repair), 1)\n        new.body.remove(repair[0])\n        self.assertEqual(ast.dump(old, include_attributes=False), ast.dump(new, include_attributes=False))')]

    def original(self, path, pin=None):
        import subprocess
        raw = subprocess.check_output(["git", "show", self.ENTRY + ":" + path],
                                      cwd=ROOT, stderr=subprocess.PIPE, timeout=30)
        self.assertEqual(guard.git_blob(raw), pin or self.PINS[path])
        return raw

    def apply_exact(self, raw, edits):
        for before, after in edits:
            self.assertEqual(raw.count(before.encode()), 1)
            raw = raw.replace(before.encode(), after.encode())
        return raw

    def pre_w08_bytes(self, path):
        # Validate the live file first. Returning history alone would bypass W08.
        original = self.original(path)
        expected = self.apply_exact(original, self.PATCHES[path])
        self.assertEqual((ROOT / path).read_bytes(), expected)
        return original

    def test_policy_delta_and_trusted_context_are_exact(self):
        raw = self.original("phase2/module_policy.json", "524697001b70fc83f0ca11b7f0ccc0366bf692af")
        expected = self.apply_exact(raw, [('"active_unit": "P2-W07"', '"active_unit": "P2-W08"')])
        self.assertEqual((ROOT / "phase2/module_policy.json").read_bytes(), expected)
        self.assertEqual(guard.unit_number(), 8)
        self.assertEqual(guard.policy_promotions(json.loads(expected)), frozenset(guard.FIRST_UNIT))
        self.assertEqual(len(guard.promotions(ROOT)), 13)
        self.assertEqual(guard.check_repository(ROOT)["protected_modules"], 35)

    def test_mismatch_and_forbidden_promotion_still_fail(self):
        value = json.loads((ROOT / "phase2/module_policy.json").read_bytes())
        for unit in ("P2-W07", "P2-W09"):
            with self.assertRaisesRegex(ValueError, "^policy_cannot_select_unit$"):
                guard.policy_promotions(value, unit)
        value["promotions"].append({"path": "analysis/origins.py", "unit": 8})
        with self.assertRaises(ValueError): guard.policy_promotions(value, "P2-W08")
        value["first_units"]["analysis/origins.py"] = 8
        with self.assertRaises(ValueError): guard.policy_promotions(value, "P2-W08")

    def test_exact_seven_paths_and_all_other_immediate_scopes(self):
        ci = ci_driver(); paths = guard.plan_paths(ROOT)
        self.assertEqual(ci.P2_W08_R01_PATHS, self.EXTRA)
        self.assertEqual(len(paths["P2-W08"]), 6)
        self.assertFalse(self.EXTRA & paths["P2-W08"])
        cumulative = set()
        for step in range(1, 10):
            unit = f"P2-W{step:02}"
            extra = (ci.P2_W02_R01_PATHS if step == 2 else
                     ci.P2_W04_R01_PATHS if step == 4 else
                     ci.P2_W05_R01_PATHS | ci.P2_W05_R02_PATHS if step == 5 else
                     ci.P2_W07_R01_PATHS if step == 7 else
                     self.EXTRA if step == 8 else frozenset())
            expected = paths[unit] | extra
            self.assertEqual(ci.effective_paths(paths, unit), expected)
            ci.check_changed_paths(paths, unit, expected)
            cumulative.update(expected)
            self.assertEqual(ci.effective_paths(paths, unit, cumulative=True), cumulative)
            for path in self.EXTRA - expected:
                with self.assertRaisesRegex(ValueError, "^work_unit_allowlist_exceeded$"):
                    ci.check_changed_paths(paths, unit, {path})

    def test_similar_paths_and_product_repairs_are_refused(self):
        ci = ci_driver(); paths = guard.plan_paths(ROOT)
        allowed = ci.effective_paths(paths, "P2-W08")
        for path in ("phase2/module_policy.json.bak", "phase2/../phase2/module_policy.json",
                     "tests/security/test_scaffold_inertness.py", "PHASE_2_PLAN.md",
                     "src/source_integrity_toolkit/runtime/boundary.py",
                     "tools/check_scaffold_boundary.py", "PHASE_2_COMPLETION.md"):
            with self.assertRaisesRegex(ValueError, "^work_unit_allowlist_exceeded$"):
                ci.check_changed_paths(paths, "P2-W08", allowed | {path})

    def test_literal_permission_deltas_preserve_every_other_byte(self):
        for path in self.PATCHES:
            self.pre_w08_bytes(path)

    def test_literal_check_rejects_mutated_scope_and_weakened_probe(self):
        # These are local mutated byte strings, never edits to the checkout.
        for path, edits in self.PATCHES.items():
            original = self.original(path)
            expected = self.apply_exact(original, edits)
            for candidate in (original, expected + b"\nUNAPPROVED = True\n", expected[:-1]):
                with self.assertRaises(AssertionError): self.assertEqual(candidate, expected)
        path = "tests/security/test_preparation_inertness.py"
        expected = self.apply_exact(self.original(path), self.PATCHES[path])
        for before, after in ((b'unit=unit', b'unit="P2-W07"'),
                              (b'assert not guard.check_repository', b'assert guard.check_repository')):
            changed = expected.replace(before, after, 1)
            self.assertNotEqual(changed, expected)
            with self.assertRaises(AssertionError): self.assertEqual(changed, expected)

    def test_w07_four_methods_only_and_all_original_identities_survive(self):
        import ast
        path = "tests/contract/test_phase2_transition.py"
        expected = self.apply_exact(self.original(path), self.TRANSITION_EDITS)
        live = ast.parse((ROOT / path).read_bytes())
        additions = [n for n in live.body if isinstance(n, ast.ClassDef) and n.name == "W08R01Tests"]
        self.assertEqual(len(additions), 1)
        live.body.remove(additions[0])
        self.assertEqual(ast.dump(live, include_attributes=False),
                         ast.dump(ast.parse(expected), include_attributes=False))

    def test_transition_record_is_append_only_and_names_all_migrations(self):
        raw = self.original("phase2/transition_ledger.md", "15d32b5d601a9f68ce838d515e7d521b2ff08d97")
        live = (ROOT / "phase2/transition_ledger.md").read_bytes()
        self.assertTrue(live.startswith(raw))
        added = live[len(raw):].decode()
        self.assertIn("## P2-W08-R01:", added)
        for name in ("test_repair_does_not_expand_another_units_immediate_diff",
                     "test_repair_cumulative_accounting_retains_only_authorized_extras",
                     "test_r01_exact_four_paths_and_no_other_unit_permission_expansion",
                     "test_r02_exact_extra_path_and_other_units_keep_their_immediate_scope",
                     "test_exact_six_paths_are_w07_only_and_history_is_cumulative",
                     "test_only_four_named_permission_test_bodies_change",
                     "test_ci_context_collection_and_failure_controls_are_unchanged",
                     "test_prior_phase2_transition_tests_keep_every_statement",
                     "test_whole_package_guard_rejects_forbidden_implementation_in_temporary_copy"):
            self.assertIn(name, added)
        self.assertEqual(len(guard.historical_nodes(ROOT)), 194)

    def test_entry_bytes_outside_authorized_changes_remain_accepted(self):
        import subprocess
        ci = ci_driver(); allowed = ci.effective_paths(guard.plan_paths(ROOT), "P2-W08")
        raw = subprocess.check_output(["git", "ls-tree", "-r", "-z", self.ACCEPTED],
                                      cwd=ROOT, stderr=subprocess.PIPE, timeout=30)
        entries = [row.split(b"\t", 1) for row in raw.split(b"\0") if row]
        self.assertEqual(len(entries), 154)
        for meta, name in entries:
            path = name.decode(); mode, kind, pin = meta.decode().split()
            self.assertEqual((mode, kind), ("100644", "blob"))
            if path not in allowed:
                self.assertEqual(guard.git_blob((ROOT / path).read_bytes()), pin)
        # The permitted workflow path is intentionally unchanged by this repair.
        path = ".github/workflows/phase1-ci.yml"
        original = subprocess.check_output(["git", "show", self.ACCEPTED + ":" + path], cwd=ROOT, timeout=30)
        self.assertEqual((ROOT / path).read_bytes(), original)

    def test_trusted_event_resolution_does_not_read_candidate_policy(self):
        ci = ci_driver(); head, base = "a" * 40, "b" * 40
        event = {"pull_request": {"head": {"sha": head, "ref": "phase2/p2-w08"}, "base": {"sha": base}}}
        self.assertEqual(ci.resolve_unit("pull_request", event, head), ("P2-W08", base))
        with self.assertRaises(ValueError): ci.resolve_unit("pull_request", event, base)
        event["pull_request"]["head"]["ref"] = "phase2/p2-w08; injected"
        with self.assertRaises(ValueError): ci.resolve_unit("pull_request", event, head)

    def test_clean_installed_components_need_no_phase_policy_or_developer_tools(self):
        import os
        import subprocess
        import tarfile
        import zipfile
        spec = importlib.util.spec_from_file_location("sit_w08_packaging_witness", ROOT / "tests/scaffold/test_packaging.py")
        packing = importlib.util.module_from_spec(spec); spec.loader.exec_module(packing)
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        work = Path(temp.name)
        class Factory:
            def mktemp(self, name):
                target = work / name; target.mkdir(); return target
        distributions = packing.distributions.__wrapped__(Factory())
        packing.test_declared_toolchain_is_actually_available()
        packing.test_source_distribution_inventory(distributions)
        packing.test_wheel_inventory_and_metadata(distributions)
        runtime_work = work / "installed"; runtime_work.mkdir()
        packing.test_wheel_installs_without_developer_tools(distributions, runtime_work)
        rebuild_work = work / "rebuild"; rebuild_work.mkdir()
        packing.test_source_distribution_rebuilds_same_package(distributions, rebuild_work)
        python = runtime_work / "runtime" / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
        modules = {}
        for path in sorted(guard.EXPECTED_PATHS):
            name = "source_integrity_toolkit." + path.removesuffix(".py").replace("/", ".")
            name = name.removesuffix(".__init__")
            modules[name] = hashlib.sha256((ROOT / "src/source_integrity_toolkit" / path).read_bytes()).hexdigest()
        self.assertEqual(len(modules), 48)
        fixtures = [json.loads((ROOT / "tests/fixtures/hero" / (name + ".bundle.json")).read_bytes())
                    for name in ("H7-01", "H7-V01", "H7-V02", "H7-V03")]
        script = r'''
import sys,json,hashlib,importlib,importlib.metadata,dataclasses,socket,ctypes
import encodings.idna
from pathlib import Path
payload=json.loads(sys.stdin.buffer.read())
assert {d.metadata['Name'] for d in importlib.metadata.distributions()}=={'source-integrity-toolkit'}
loaded={}
for name,expected in payload['modules'].items():
    module=importlib.import_module(name); path=Path(module.__file__).resolve()
    assert path.is_relative_to(Path(sys.prefix).resolve())
    assert hashlib.sha256(path.read_bytes()).hexdigest()==expected
    loaded[name]=expected
from source_integrity_toolkit.runtime.boundary import _prepare_evidence_value,_prepare_evidence_utf8
from source_integrity_toolkit.contracts.report import _ObservabilityPreparation
import source_integrity_toolkit as package
assert not hasattr(package,'_prepare_evidence_value')
assert package.__version__=='0.1.0.dev0'
events=[]
def audit(event,args):
    if event=='open' or event.startswith('socket.') or event=='ctypes.dlopen':
        events.append(event);raise RuntimeError('blocked_installed_effect')
sys.addaudithook(audit)
for source in payload['fixtures']:
    for result in (_prepare_evidence_value(source),_prepare_evidence_utf8(json.dumps(source).encode())):
        assert type(result) is _ObservabilityPreparation and result.input_state=='accepted'
        for inquiry in result.inquiries:
            assert [p.prerequisite for p in inquiry.prerequisites if p.complete_check_executed]==['PC01']
            assert all(p.answer is None for p in inquiry.prerequisites[1:])
        assert not hasattr(result,'results') and not hasattr(result,'max_level')
assert _prepare_evidence_value({}).input_state=='rejected'
assert _prepare_evidence_utf8(b'{}').input_state=='rejected'
for call,args in ((package.audit_bundle,(object(),)),(package.audit_file,(object(),object()))):
    try:call(*args,options=object())
    except NotImplementedError:pass
    else:raise AssertionError('public_audit_activated')
assert events==[]
for probe in (lambda:open('FICTIONAL_MUST_NOT_OPEN','rb'),lambda:socket.getaddrinfo('fictional.invalid',443),lambda:ctypes.CDLL('FICTIONAL_MUST_NOT_LOAD')):
    try:probe()
    except RuntimeError:pass
assert events==['open','socket.getaddrinfo','ctypes.dlopen']
print(json.dumps({'modules':loaded,'admitted_fixture_modes':8,'rejected_empty_modes':2,'public_refusals':2,'normal_effects':[],'negative_events':events,'runtime_distributions':['source-integrity-toolkit']}))
'''
        run = subprocess.run([str(python), "-I", "-B", "-c", script], cwd=runtime_work,
            input=json.dumps({"modules": modules, "fixtures": fixtures}).encode(), capture_output=True, timeout=90)
        self.assertEqual(run.returncode, 0, run.stderr.decode(errors="replace"))
        self.assertEqual(run.stderr, b"")
        result = json.loads(run.stdout)
        self.assertEqual(result["modules"], modules)
        self.assertEqual(result["admitted_fixture_modes"], 8)
        self.assertEqual(result["normal_effects"], [])
        inventory = []
        paths = [distributions[1], distributions[2], next((rebuild_work / "source_integrity_toolkit-0.1.0.dev0/dist").glob("*.whl"))]
        for path in paths:
            if path.suffix == ".whl":
                with zipfile.ZipFile(path) as archive:
                    members = {n: hashlib.sha256(archive.read(n)).hexdigest() for n in archive.namelist()}
                self.assertEqual(len(members), 55)
            else:
                with tarfile.open(path) as archive:
                    members = {m.name: hashlib.sha256(archive.extractfile(m).read()).hexdigest() for m in archive.getmembers() if m.isfile()}
                self.assertEqual(len(members), 65)
            inventory.append({"name": path.name, "bytes": path.stat().st_size,
                              "sha256": hashlib.sha256(path.read_bytes()).hexdigest(), "members": members})
        self.assertEqual(inventory[1]["members"], inventory[2]["members"])
        record = {"head": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
                  "scope": "W08 clean installed preparation; no public audit or native-file certification",
                  "unit": f"P2-W{guard.unit_number():02}", "ok": True, "runtime": result, "distributions": inventory}
        # Fixed developer evidence destination; no source payload or binary upload.
        destination = (Path(os.environ["RUNNER_TEMP"]) / "sit-p2/evidence" if os.environ.get("GITHUB_ACTIONS") == "true" else work)
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "w08-installed-runtime.json").write_text(json.dumps(record, sort_keys=True, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
