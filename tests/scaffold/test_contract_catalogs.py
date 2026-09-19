# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Keep frozen catalog assertions; stage the exact bundle schema reservation."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from tools import check_scaffold_boundary as phase_guard
phase_guard.load_phase1_test("tests/scaffold/test_contract_catalogs.py", globals())


def _schema_reservation(self):
    stage = phase_guard.unit_number()
    paths = {p.relative_to(ROOT / "schemas").as_posix() for p in (ROOT / "schemas").rglob("*") if p.is_file()}
    expected = {"README.md", "bundle/README.md", "report/README.md"}
    if stage >= 2:
        expected.add("bundle/sit-bundle-0.1.schema.json")
    self.assertEqual(paths, expected)
    for name, contract in (("bundle", "sit-bundle/0.1"), ("report", "sit-report/0.1")):
        text = (ROOT / "schemas" / name / "README.md").read_text(encoding="utf-8")
        self.assertIn(contract, text)
        if name == "report" or stage == 1:
            self.assertIn("executable schema not delivered", text)
    if stage >= 2:
        schema = json.loads((ROOT / "schemas/bundle/sit-bundle-0.1.schema.json").read_bytes(), object_pairs_hook=pairs_unique)
        self.assertEqual(schema["$schema"], "https://json-schema.org/draft/2020-12/schema")
        stack = [schema]
        while stack:
            value = stack.pop()
            if isinstance(value, dict):
                if "$ref" in value:
                    self.assertTrue(value["$ref"].startswith("#"))
                stack.extend(value.values())
            elif isinstance(value, list):
                stack.extend(value)


ContractCatalogTests.test_schemas_are_documentation_only = _schema_reservation

if __name__ == "__main__":
    unittest.main()
