# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Finite W03 module-index checks, independent of the installed auditor.

No manifest is imported by product code. These checks compare the approved
48-path scaffold, literal owner annotations and static syntax. Future domain
and native-security test paths remain reservations, not executed tests.
"""

import ast
import copy
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
PREFIX = "src/source_integrity_toolkit/"
# PHASE_1_PLAN.md section 6: exact closed file list, including WU11 additions.
PATHS = {
    "": "__init__.py api.py cli.py",
    "contracts": "__init__.py bundle.py evidence.py results.py report.py constants.py execution.py",
    "io": "__init__.py input_file.py output_directory.py publication.py platform_linux.py platform_windows.py",
    "validation": "__init__.py structure.py references.py semantics.py limits.py",
    "graph": "__init__.py projections.py traversal.py cycles.py witnesses.py",
    "analysis": "__init__.py inventory.py origins.py process_comparison.py contribution_profile.py evaluator_lineage.py presence.py correction_routes.py correction_outcomes.py human_review.py context.py findings.py",
    "reporting": "__init__.py assemble.py json_report.py markdown_report.py escaping.py",
    "runtime": "__init__.py boundary.py resources.py disclosure.py diagnostics.py",
}
EXPECTED = {f"{directory}/{name}" if directory else name
            for directory, names in PATHS.items() for name in names.split()}
# Architecture section 5, with section 16's one presentation authority retained.
HOMES = {
    "INGESTION_CONTRACT": "contracts/bundle.py",
    "EVIDENCE_BASIS": "contracts/evidence.py",
    "SOURCE_INVENTORY": "analysis/inventory.py",
    "ORIGIN_ANALYSIS": "analysis/origins.py",
    "PROCESS_COMPARISON": "analysis/process_comparison.py",
    "CONTRIBUTION_PROFILE": "analysis/contribution_profile.py",
    "EVALUATOR_LINEAGE": "analysis/evaluator_lineage.py",
    "PRESENCE_RECORDS": "analysis/presence.py",
    "CORRECTION_ROUTES": "analysis/correction_routes.py",
    "CORRECTION_OUTCOMES": "analysis/correction_outcomes.py",
    "HUMAN_REVIEW_RECORDS": "analysis/human_review.py",
    "CONTEXT_PRESERVATION": "analysis/context.py",
    "GRAPH_VIEW_CONTRACT": "graph/projections.py",
    "TEMPORAL_CONTRACT": "validation/semantics.py",
    "REPORT_CONTRACT": "contracts/report.py",
    "FINDING_CONTRACT": "analysis/findings.py",
    "REPORT_PRESENTATION": "reporting/assemble.py",
    "RUNTIME_BOUNDARY": "runtime/boundary.py",
    "VALIDATION_GOVERNANCE": None,
}
STATUS = {"specification": "adopted", "scaffold": "catalog_present",
          "behavior_implementation": "pending", "behavior_tests": "pending"}


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def read_catalog(name):
    return json.loads((ROOT / "scaffold" / name).read_text(encoding="utf-8"))


def blob(raw):
    return hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def verify_manifest(manifest, files, owners):
    require(manifest["status"] == STATUS, "False implementation status")
    require(manifest["package_prefix"] == PREFIX, "Unexpected package prefix")
    rows = manifest["modules"]
    require(len(rows) == 48 and len({r[0] for r in rows}) == 48, "Duplicate/missing module")
    require({r[0] for r in rows} == EXPECTED == set(files), "Closed path set changed")
    require({r[0] for r in manifest["owner_bindings"]} == set(HOMES) == owners,
            "Owner set mismatch")
    require(len(manifest["owner_bindings"]) == 19, "Duplicate owner home")
    for path, layer, labels, form, expected_blob in rows:
        require(layer in manifest["layer_rules"], "Undefined dependency layer")
        expected_layer = ("exports" if path == "__init__.py" else
                          path.split("/")[0] if "/" in path else "composition")
        require(layer == expected_layer, "Module assigned to wrong layer")
        require(set(labels) <= owners and len(labels) == len(set(labels)), "Unknown owner")
        raw = files[path]
        require(blob(raw) == expected_blob, "Accepted W02 source bytes changed: " + path)
        text = raw.decode("utf-8")
        tree = ast.parse(text)
        if path == "__init__.py":
            require(labels == ["RUNTIME_BOUNDARY", "REPORT_CONTRACT"], "Root export ownership")
            require(form == "exports_only", "Root form")
        else:
            annotation = re.search(r"Owner: ([^\n]+)", text)
            require(annotation is not None, "Missing literal owner annotation")
            annotated = {owner for owner in owners if owner in annotation[1]}
            require(set(labels) == annotated, "Owner annotation mismatch")
            expected_form = {"api.py": "immediate_refusal", "cli.py": "help_version_refusal",
                             "contracts/constants.py": "version_literal"}.get(path, "docstring_only")
            require(form == expected_form, "Operational or unknown scaffold form")
        if form == "docstring_only":
            require(len(tree.body) == 1 and ast.get_docstring(tree) is not None,
                    "Executable statement in inert slot")
    for owner, primary, supporting, future_tests in manifest["owner_bindings"]:
        require(primary == HOMES[owner], "Wrong semantic authority")
        require(future_tests and isinstance(supporting, list), "Lost future binding")
        if primary is not None:
            require(primary in files, "Missing primary module")
            module_row = next(r for r in rows if r[0] == primary)
            require(owner in module_row[2], "Primary module has wrong annotation")
        else:
            require(owner == "VALIDATION_GOVERNANCE", "Unowned runtime responsibility")
            require("repository CI" in supporting, "Governance must keep non-runtime home")
        for home in supporting:
            if home.startswith(("tests/", "repository ")):
                continue
            if home == "io/*":
                require(owner == "RUNTIME_BOUNDARY", "Unbounded support scope")
                continue
            require(home in files, "Undefined supporting module")


class ModuleManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = read_catalog("module_manifest.json")
        cls.trace = read_catalog("trace_catalog.json")
        cls.owners = {row[0] for row in cls.trace["owners"]}
        package = ROOT / PREFIX
        cls.files = {p.relative_to(package).as_posix(): p.read_bytes()
                     for p in package.rglob("*.py")}

    def test_exact_paths_owners_forms_and_accepted_bytes(self):
        verify_manifest(self.manifest, self.files, self.owners)

    def test_all_trace_owners_have_a_recorded_home(self):
        bindings = {row[0]: row for row in self.manifest["owner_bindings"]}
        for trace in self.trace["traces"]:
            self.assertIn(trace[2], bindings)
        self.assertEqual(len(EXPECTED), 48)
        self.assertEqual(sum(row[3] == "docstring_only" for row in self.manifest["modules"]), 44)

    def test_presentation_and_governance_keep_their_distinct_homes(self):
        bindings = {row[0]: row for row in self.manifest["owner_bindings"]}
        self.assertEqual(bindings["REPORT_PRESENTATION"][1], "reporting/assemble.py")
        self.assertEqual(set(bindings["REPORT_PRESENTATION"][2]),
                         {"reporting/json_report.py", "reporting/markdown_report.py", "reporting/escaping.py"})
        self.assertIsNone(bindings["VALIDATION_GOVERNANCE"][1])
        self.assertEqual(bindings["VALIDATION_GOVERNANCE"][3], ["tests/golden/", "trace-coverage checks"])
        self.assertIn("16", self.manifest["binding_sections"]["REPOSITORY_ARCHITECTURE.md"])

    def test_layer_permissions_keep_their_qualifications(self):
        layers = self.manifest["layer_rules"]
        self.assertEqual(set(layers), {"contracts", "validation", "graph", "analysis", "reporting",
                                       "runtime", "io", "composition", "exports"})
        self.assertIn("not analysis or reporting", layers["validation"])
        self.assertIn("not analysis policy", layers["graph"])
        self.assertIn("no analytical recomputation", layers["reporting"])
        self.assertIn("unimplemented", layers["io"])
        self.assertIn("conditional permissions", self.manifest["layer_rules_source"])
        self.assertIn("cycle prohibition", self.manifest["layer_rules_source"])

    def test_shared_source_identities_agree(self):
        for source, identity in self.manifest["sources"].items():
            self.assertEqual(identity, self.trace["sources"][source])
        self.assertEqual(self.manifest["intake_commit"], self.trace["intake_commit"])

    def test_product_has_no_catalog_dependency(self):
        # Finite current-file inspection, not a product parser or general security engine.
        for path, raw in self.files.items():
            text = raw.decode("utf-8")
            for forbidden in ("module_manifest.json", "trace_catalog.json", "obligation_catalog.json"):
                self.assertNotIn(forbidden, text, path)

    def test_mutations_cannot_hide_missing_or_operational_slots(self):
        for mode in ("missing", "duplicate", "owner", "layer", "form", "hash", "home", "status"):
            with self.subTest(mode=mode):
                bad = copy.deepcopy(self.manifest)
                if mode == "missing": bad["modules"].pop()
                if mode == "duplicate": bad["modules"][-1] = copy.deepcopy(bad["modules"][0])
                if mode == "owner": bad["modules"][0][2] = ["INDEPENDENCE_ORACLE"]
                if mode == "layer": bad["modules"][0][1] = "analysis"
                if mode == "form": bad["modules"][0][3] = "operational"
                if mode == "hash": bad["modules"][0][4] = "0" * 40
                if mode == "home": bad["owner_bindings"][0][1] = "analysis/findings.py"
                if mode == "status": bad["status"]["behavior_tests"] = "passed"
                with self.assertRaises(AssertionError):
                    verify_manifest(bad, self.files, self.owners)

    def test_mutated_product_bytes_are_rejected(self):
        bad = dict(self.files)
        bad["analysis/origins.py"] += b"\ndef analyze():\n    return 42\n"
        with self.assertRaises(AssertionError):
            verify_manifest(self.manifest, bad, self.owners)


if __name__ == "__main__":
    unittest.main()
