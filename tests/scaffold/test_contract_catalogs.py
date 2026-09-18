# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Static W03 index checks only; no audit/graph/qualification implementation.

Full primary registry bytes are checked. Supplement IDs/homes were read from the
connected, frozen W9/W11 documents during authoring; these tests check their
finite references and cross-links, not their unimplemented runtime behavior.
"""

import copy
import hashlib
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).resolve().parents[2]
TRACE = "THEORY_TO_CODE_TRACEABILITY.md"
REPORT = "OBSERVABILITY_AND_REPORTING.md"
VALIDATION = "VALIDATION_PLAN.md"
PINNED = {
    TRACE: "73a69a56828b6ff416164b7bd6420521da1c635bd92f03b92e07231b552a7849",
    REPORT: "44daa3c86fc7d12e7be16a3aedfe10d16b99f55aa69141f90319ce2b5e63ff6a",
    VALIDATION: "f958a12bda396cd12bfec096353ec17ec786e8c7fe30e07ee987f7d52874b707",
}
STATUS = {"specification": "adopted", "scaffold": "catalog_present",
          "behavior_implementation": "pending", "behavior_tests": "pending"}


def pairs_unique(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate developer-catalog key")
        result[key] = value
    return result


def load_catalog(name):
    return json.loads((ROOT / "scaffold" / name).read_text(encoding="utf-8"),
                      object_pairs_hook=pairs_unique)


def cells(line):
    return [part.strip() for part in line.strip().strip("|").split("|")]


def tokens(text):
    return re.findall(r"`([^`]+)`", text)


def table_rows(text, start, end):
    for number, line in enumerate(text.splitlines(), 1):
        if start <= number <= end and line.startswith("|") and not re.fullmatch(r"[| :\-]+", line):
            yield number, cells(line)


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def verify_trace(cat, sources):
    require(cat["status"] == STATUS, "Status promotion")
    owners = [[c[0], n, c[1]] for n, c in table_rows(sources[TRACE], 68, 93)
              if len(c) == 3 and re.fullmatch(r"[A-Z_]+", c[0])]
    require(cat["owners"] == owners and len(owners) == 19, "Owner registry mismatch")
    parsed = []
    for m in re.finditer(r"^### (SIT-TR\d{3}): ([^\n]+)\n(.*?)(?=^### |^## |\Z)",
                         sources[TRACE], re.MULTILINE | re.DOTALL):
        assignment = dict(cells(line) for line in m[3].splitlines()
                          if line.startswith("|") and len(cells(line)) == 2)
        parsed.append([m[1], m[2], tokens(assignment["Primary prospective owner"])[0],
                       sources[TRACE][:m.start()].count("\n") + 1,
                       assignment["Controlling specification"],
                       tokens(assignment["Existing source entries"]),
                       tokens(assignment["Existing product requirements"]),
                       tokens(assignment["Required shared validation"]),
                       tokens(assignment["Existing acceptance criteria"]),
                       assignment["Non-negotiable interpretation limit"],
                       assignment["Owned analytical families"]])
    require(cat["traces"] == parsed and len(parsed) == 35, "Trace assignment/qualification mismatch")
    family_rows = [[c[0], n, c[2]] for n, c in table_rows(sources[REPORT], 58, 81)
                   if len(c) == 4 and re.fullmatch(r"SIT-M\d{3}", c[0])]
    require(cat["families"] == family_rows and len(family_rows) == 15, "Family mismatch")
    field_kinds = {}
    for n, c in table_rows(sources[REPORT], 764, 797):
        if len(c) != 2 or not re.fullmatch(r"M\d{3}", c[0]):
            continue
        for group in c[1].split(";"):
            names, kind = group.split(":", 1)
            for key in tokens(names):
                require(key not in field_kinds, "Duplicate source field")
                field_kinds[key] = ("SIT-" + c[0], kind.strip().split()[0], n)
    vrows = {}
    for n, c in table_rows(sources[VALIDATION], 745, 882):
        if re.match(r"`SIT-VF\d{3}`", c[0]):
            vf, key = tokens(c[0])
            require(len(c) == 5 and all(c[1:]), "Missing source expectation")
            vrows[vf] = (key, n)
    rows = []
    for n, c in table_rows(sources[TRACE], 588, 652):
        if len(c) != 6 or not c[0].startswith("`SIT-M"):
            continue
        family, key = tokens(c[0])
        tests = [tokens(cell)[0] for cell in c[2:]]
        vf = tests[0].removesuffix("-P")
        require(tests == [vf + "-" + suffix for suffix in "PNMB"], "Test suffix mismatch")
        require(field_kinds[key][0] == family and vrows[vf][0] == key, "Three-registry mismatch")
        rows.append([vf, key, family, tokens(c[1])[0], field_kinds[key][1], tests,
                     n, field_kinds[key][2], vrows[vf][1]])
    require(cat["fields"] == rows and len(rows) == 57, "Field crosswalk mismatch")
    require({r[1] for r in rows} == set(field_kinds), "Extra or missing reporting field")
    require(len({r[0] for r in rows}) == 57, "Duplicate field obligation")
    require({r[0] for r in rows} == set(vrows), "Extra or missing validation row")


def verify_obligations(ob, trace, sources):
    require(ob["status"] == STATUS, "Behavior status promotion")
    expected = [[test, row[0], row[8], column]
                for row in trace["fields"] for column, test in enumerate(row[5], 1)]
    require(ob["field_obligations"] == expected and len(expected) == 228, "P/N/M/B cell mismatch")
    require(len({r[0] for r in expected}) == 228, "Duplicate field-test ID")
    for test, vf, line, column in expected:
        row = cells(sources[VALIDATION].splitlines()[line - 1])
        require(tokens(row[0])[0] == vf and row[column], "Empty or wrong source cell")
    shared = []
    for m in re.finditer(r"^### (SIT-VG\d{3}): ([^\n]+)\n(.*?)(?=^### |^## |\Z)",
                         sources[VALIDATION], re.MULTILINE | re.DOTALL):
        start = sources[VALIDATION][:m.start()].count("\n") + 1
        end = sources[VALIDATION][:m.end()].count("\n")
        contract = re.search(r"\*\*Governing contract:\*\* ([^\n]+)", m[3])[1]
        consumers = [r[0] for r in trace["traces"] if m[1] in r[7]]
        shared.append([m[1], m[2], start, end, contract, consumers])
    require(ob["shared_families"] == shared and len(shared) == 26, "Shared-family mismatch")
    pcs = [[n, c] for n, c in table_rows(sources[REPORT], 490, 526)
           if re.fullmatch(r"PC\d{2}", c[0])]
    vpcs = {c[0]: (n, c) for n, c in table_rows(sources[VALIDATION], 932, 963)
            if re.fullmatch(r"PC\d{2}", c[0])}
    require(len(pcs) == len(vpcs) == 24, "Prerequisite source count")
    expected_pc = [[c[0], n, vpcs[c[0]][0], "SIT-VG014/" + c[0],
                    re.findall(r"SIT-VG\d{3}", vpcs[c[0]][1][2])] for n, c in pcs]
    require(ob["prerequisites"] == expected_pc, "Prerequisite mapping mismatch")
    for group, a, b, va, vb, prefix, count in (
            ("reasons", 527, 577, 964, 1011, "SIT-VG014/", 40),
            ("finding_conditions", 808, 840, 1012, 1045, "SIT-VG015/", 22)):
        source_rows = [(n, c) for n, c in table_rows(sources[REPORT], a, b)
                       if re.fullmatch(r"`[a-z0-9_]+`", c[0]) and c[0] != "`condition_code`"]
        target_rows = {c[0].strip("`"): (n, c) for n, c in table_rows(sources[VALIDATION], va, vb)
                       if re.fullmatch(r"[a-z0-9_]+", c[0].strip("`"))}
        rows = []
        for n, c in source_rows:
            code = c[0].strip("`")
            require(code in target_rows, "Unregistered exercise branch")
            row = [code, n, target_rows[code][0], prefix + code]
            if group == "finding_conditions":
                require(c[2] == target_rows[code][1][2], "Threat qualification mismatch")
                row.append(c[2])
            rows.append(row)
        require(ob[group] == rows and len(rows) == count, "Registry/exercise mismatch: " + group)


class ContractCatalogTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = {p: (ROOT / p).read_text(encoding="utf-8") for p in PINNED}
        cls.trace = load_catalog("trace_catalog.json")
        cls.ob = load_catalog("obligation_catalog.json")

    def test_complete_primary_source_bytes(self):
        for path, expected in PINNED.items():
            raw = (ROOT / path).read_bytes()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), expected)
            for cat in (self.trace, self.ob):
                ref = cat["sources"][path]
                self.assertEqual(ref["bytes"], len(raw))
                self.assertEqual(ref["sha256"], expected)
                self.assertEqual(ref["git_blob_sha1"], hashlib.sha1(
                    b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest())

    def test_trace_owner_family_and_field_equality(self):
        verify_trace(self.trace, self.sources)

    def test_all_obligation_and_code_references(self):
        verify_obligations(self.ob, self.trace, self.sources)

    def test_cross_references_are_closed(self):
        owners = {r[0] for r in self.trace["owners"]}
        traces = {r[0]: r for r in self.trace["traces"]}
        shared = {r[0] for r in self.ob["shared_families"]}
        for row in traces.values():
            self.assertIn(row[2], owners)
            self.assertLessEqual(set(row[5]), {f"SIT-T{i:03}" for i in range(1, 41)})
            self.assertLessEqual(set(row[6]), {f"SIT-P{i:03}" for i in range(1, 17)})
            self.assertLessEqual(set(row[7]), shared)
            self.assertLessEqual(set(row[8]), {f"SIT-SC{i:03}" for i in range(1, 67)})
        for row in self.trace["fields"]:
            self.assertIn(row[3], traces)
            self.assertIn(row[2], traces[row[3]][10])

    def test_surrounding_qualifications_stay_binding(self):
        self.assertEqual(self.trace["binding_sections"], self.ob["binding_sections"])
        self.assertIn("5.1", self.trace["binding_sections"][TRACE])
        self.assertIn("5.2", self.trace["binding_sections"][TRACE])
        self.assertIn("17", self.trace["binding_sections"][REPORT])
        self.assertIn("22", self.trace["binding_sections"]["GOVERNANCE_AND_HANDOFF.md"])
        self.assertIn("complete row", self.ob["pointer_contract"])

    def test_data_handling_ids_and_reference_closure(self):
        rows = self.ob["data_handling_controls"]
        self.assertEqual([r[0] for r in rows], [f"SIT-DH{i:03}" for i in range(1, 21)])
        tr = {r[0] for r in self.trace["traces"]}
        vg = {r[0] for r in self.ob["shared_families"]}
        for _, source, section, trace_ids, shared_ids in rows:
            self.assertEqual((source, section), ("PRIVACY_AND_DATA_HANDLING.md", "9"))
            self.assertLessEqual(set(trace_ids), tr)
            self.assertLessEqual(set(shared_ids), vg)
            self.assertTrue(trace_ids and shared_ids)
        limits = self.ob["resource_limit_references"]
        self.assertEqual(limits["ids"], [f"WU9-L{i:02}" for i in range(1, 15)])
        self.assertEqual(limits["implementation_status"], "pending")

    def test_control_case_groups_and_exact_future_paths(self):
        groups = self.ob["control_cases"]
        self.assertEqual(len(groups), 3)
        for group, source, section, prefix, count in zip(groups,
                ["SOURCE_INTEGRITY_THREAT_MODEL.md", "LICENSING_NOTES.md", "REPOSITORY_ARCHITECTURE.md"],
                ["13", "8", "21"], ["W9-", "W9-LIC", "W11-R"], [24, 6, 32]):
            self.assertEqual((group["source_document"], group["section"]), (source, section))
            self.assertEqual(group["ids"], [f"{prefix}{i:02}" for i in range(1, count + 1)])
            self.assertIn(source, self.ob["sources"])
        expected = {
            "tests/contract/test_normalization_profile.py": list(range(1, 11)),
            "tests/contract/test_realization_profile.py": list(range(11, 18)) + [31, 32],
            "tests/security/test_resource_profile.py": list(range(18, 23)),
            "tests/security/test_filesystem_profiles.py": list(range(23, 31)),
        }
        self.assertEqual(groups[2]["future_test_paths"],
                         {p: [f"W11-R{i:02}" for i in ids] for p, ids in expected.items()})
        flat = [case for cases in groups[2]["future_test_paths"].values() for case in cases]
        self.assertEqual(len(flat), len(set(flat)))
        self.assertEqual(set(flat), set(groups[2]["ids"]))

    def test_schemas_are_documentation_only(self):
        paths = {p.relative_to(ROOT / "schemas").as_posix() for p in (ROOT / "schemas").rglob("*") if p.is_file()}
        self.assertEqual(paths, {"README.md", "bundle/README.md", "report/README.md"})
        for name, contract in (("bundle", "sit-bundle/0.1"), ("report", "sit-report/0.1")):
            text = (ROOT / "schemas" / name / "README.md").read_text(encoding="utf-8")
            self.assertIn(contract, text)
            self.assertIn("executable schema not delivered", text)

    def test_duplicate_json_keys_are_rejected(self):
        with self.assertRaises(ValueError):
            json.loads('{"owners": [], "owners": []}', object_pairs_hook=pairs_unique)

    def test_mutations_cannot_drop_field_or_replace_primary_trace(self):
        for mode in ("drop", "trace", "kind", "owner", "limit", "status"):
            with self.subTest(mode=mode):
                bad = copy.deepcopy(self.trace)
                if mode == "drop": bad["fields"].pop()
                if mode == "trace": bad["fields"][0][3] = "SIT-TR999"
                if mode == "kind": bad["fields"][0][4] = "truth_score"
                if mode == "owner": bad["owners"][0][0] = "UNREGISTERED_OWNER"
                if mode == "limit": bad["traces"][0][9] = "Admission authenticates sources."
                if mode == "status": bad["status"]["behavior_tests"] = "passed"
                with self.assertRaises(AssertionError):
                    verify_trace(bad, self.sources)

    def test_mutations_cannot_relabel_test_cells_or_drop_codes(self):
        for mode in ("cell", "test", "reason", "shared", "association", "status"):
            with self.subTest(mode=mode):
                bad = copy.deepcopy(self.ob)
                if mode == "cell": bad["field_obligations"][0][3] = 2
                if mode == "test": bad["field_obligations"][0][0] = "SIT-VF001-B"
                if mode == "reason": bad["reasons"] = [r for r in bad["reasons"] if r[0] != "outside_v01"]
                if mode == "shared": bad["shared_families"][0][3] -= 1
                if mode == "association": bad["finding_conditions"][0][4] = "All sources are false"
                if mode == "status": bad["status"]["behavior_implementation"] = "implemented"
                with self.assertRaises(AssertionError):
                    verify_obligations(bad, self.trace, self.sources)


if __name__ == "__main__":
    unittest.main()
