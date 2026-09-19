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


if __name__ == "__main__":
    unittest.main()
