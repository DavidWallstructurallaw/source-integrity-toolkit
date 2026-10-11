# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Retained component-evidence and clean-install guarantees.

Historical transition replay and reverse patches were retired in VC-04.
Their original implementation remains at commit
3ac5128e4744e2d3708400e3cb1875a9cd4ed0e1; the one-time disposition map is
verification/consolidation_map.json. These direct checks retain their identities.
"""
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools import check_scaffold_boundary as guard

# Independent transcription of the accepted component evidence. All thirteen
# components were implemented by the accepted preparation boundary; this is a
# record assertion, not a source of current execution or modification authority.
PREPARATION_FIRST_UNITS = {
    "contracts/bundle.py": 2, "contracts/evidence.py": 2,
    "contracts/constants.py": 2, "contracts/execution.py": 2,
    "contracts/report.py": 2, "validation/limits.py": 3,
    "runtime/resources.py": 3, "runtime/diagnostics.py": 3,
    "io/input_file.py": 4, "runtime/boundary.py": 4,
    "validation/structure.py": 4, "validation/references.py": 5,
    "validation/semantics.py": 5,
}


class Phase2TransitionTests(unittest.TestCase):
    def test_component_evidence_cannot_close_domain_traces(self):
        value = json.loads((ROOT / "phase2/implementation_evidence.json").read_bytes())
        self.assertEqual(value["domain_traces_closed"], [])
        self.assertEqual(value["public_audit"], "unchanged_refusal")
        self.assertEqual({r["path"] for r in value["components"]}, set(PREPARATION_FIRST_UNITS))
        for row in value["components"]:
            self.assertEqual(row["first_unit"], PREPARATION_FIRST_UNITS[row["path"]])
        active = frozenset(PREPARATION_FIRST_UNITS)
        for row in value["components"]:
            if row["path"] not in active:
                self.assertEqual((row["implementation"], row["behavior_tests"], row["evidence"]), ("pending", "pending", []))


class W08R01Tests(unittest.TestCase):
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
                  "unit": "VC", "ok": True, "runtime": result, "distributions": inventory}
        # Fixed developer evidence destination; no source payload or binary upload.
        destination = (Path(os.environ["RUNNER_TEMP"]) / "sit-p3/evidence" if os.environ.get("GITHUB_ACTIONS") == "true" else work)
        destination.mkdir(parents=True, exist_ok=True)
        (destination / "w08-installed-runtime.json").write_text(json.dumps(record, sort_keys=True, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
