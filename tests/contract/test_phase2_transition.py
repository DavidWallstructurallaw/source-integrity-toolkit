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
            self.assertEqual((ROOT / path).read_bytes(), expected)

    def test_ci_context_collection_and_failure_controls_are_unchanged(self):
        path = "tests/scaffold/test_ci_contract.py"
        expected = self.old_bytes(path, "c7b5fc7338fa4c4e08d0ba54ce0a7e87b66901ab")
        replacements = [['def effective_paths(paths, unit, *, cumulative=False):', '# Explicit owner-approved P2-W07-R01: phase-context metadata and scope tests.\n# Only W07 gains these immediate paths; later units retain cumulative history.\nP2_W07_R01_PATHS = frozenset((\n    "phase2/module_policy.json",\n    "tests/scaffold/test_ci_contract.py",\n    "tests/contract/test_bundle_contract.py",\n    "tests/security/test_input_capture.py",\n    "tests/contract/test_input_schema_mapping.py",\n    "phase2/transition_ledger.md",\n))\n\ndef effective_paths(paths, unit, *, cumulative=False):'], ['            allowed.update(P2_W05_R02_PATHS)\n', '            allowed.update(P2_W05_R02_PATHS)\n        if step == 7:\n            allowed.update(P2_W07_R01_PATHS)\n'], ['            (["P2-W05-R01", "P2-W05-R02"] if phase_guard.unit_number(unit) >= 5 else []),', '            (["P2-W05-R01", "P2-W05-R02"] if phase_guard.unit_number(unit) >= 5 else []) +\n            (["P2-W07-R01"] if phase_guard.unit_number(unit) >= 7 else []),']]
        for before, after in replacements:
            self.assertEqual(expected.count(before.encode()), 1)
            expected = expected.replace(before.encode(), after.encode())
        self.assertEqual((ROOT / path).read_bytes(), expected)
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
        self.assertEqual(ast.dump(old, include_attributes=False), ast.dump(new, include_attributes=False))


if __name__ == "__main__":
    unittest.main()
