# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Subprocess probes scoped to application-originated effects.

The test harness may load Python/stdlib modules and write synthetic temporary
files. The application may load its approved modules; it may not use those
exceptions to access evidence. Static AST guards complement these finite probes.
This is not a sandbox or a complete proof of absence of all possible effects.
"""
from __future__ import annotations

import ast
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools import check_scaffold_boundary as guard

PROBE = r'''
import contextlib, ctypes, importlib, io, json, os, pathlib, socket, sys, typing
# P1-W06-R01: preload cache and hostname helpers before the observer.
import importlib.util
import encodings.idna
# P2-W02-R01: load this approved declaration helper before observation.
import dataclasses
request = json.loads(sys.stdin.read())
package_dir = os.path.abspath(request["package"])
source_dir = os.path.dirname(package_dir)
allowed_modules = set(os.path.join(package_dir, p.replace("/", os.sep)) for p in request["paths"])
sys.dont_write_bytecode = True
sys.path.insert(0, source_dir)
os.environ["SIT_PROBE_INPUT"] = request["input"]
os.environ["SIT_PROBE_OUTPUT"] = request["output"]
violations = []
class ProbeViolation(RuntimeError):
    pass

def in_application():
    frame = sys._getframe(1)
    for _ in range(150):
        if frame is None:
            break
        filename = frame.f_code.co_filename
        if filename.startswith(package_dir + os.sep):
            return True
        frame = frame.f_back
    return False

def loader_frame(frame):
    return frame.f_globals.get("__name__") in (
        "_frozen_importlib_external", "importlib._bootstrap_external")

def refuse(event):
    violations.append(event)
    raise ProbeViolation("application_effect_blocked")

def audit(event, args):
    # sys._getframe itself emits an audit event. Filter to monitored operations
    # before inspecting the stack, so the observer cannot recursively observe
    # its own frame inspection.
    if not (event == "open" or event.startswith(("os.", "socket.", "ctypes.")) or
            event == "subprocess.Popen"):
        return
    if not in_application():
        return
    if event.startswith(("socket.", "ctypes.")) or event in (
            "subprocess.Popen", "os.system", "os.exec", "os.spawn", "os.fork", "os.posix_spawn"):
        refuse(event)
    if event == "open":
        caller = sys._getframe(1)
        path, mode, flags = args
        safe_read = not (isinstance(flags, int) and flags & (os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND))
        if loader_frame(caller) and isinstance(path, str) and safe_read:
            absolute = os.path.abspath(path)
            if absolute in allowed_modules:
                return
            if absolute.endswith(".pyc"):
                try:
                    if importlib.util.source_from_cache(absolute) in allowed_modules:
                        return
                except ValueError:
                    pass
        refuse("application_open")
    if event in ("os.listdir", "os.scandir") and loader_frame(sys._getframe(1)):
        return
    if event.startswith("os.") and event not in ("os.putenv", "os.unsetenv"):
        refuse(event)
    if event in ("os.putenv", "os.unsetenv"):
        refuse("application_environment_write")

# stat/access/read lack uniform audit coverage. Their wrappers retain module
# loader access but reject explicit application filesystem calls.
def wrap_filesystem(name, original):
    def wrapped(*args, **kwargs):
        if in_application() and not loader_frame(sys._getframe(1)):
            refuse("application_" + name)
        return original(*args, **kwargs)
    return wrapped
for name in ("stat", "lstat", "access", "read", "write", "readlink"):
    if hasattr(os, name):
        setattr(os, name, wrap_filesystem(name, getattr(os, name)))
sys.addaudithook(audit)

class Bomb:
    def touched(self, *args, **kwargs):
        refuse("argument_method")
    __str__ = __repr__ = __bool__ = __iter__ = __len__ = __getitem__ = touched
    __fspath__ = __hash__ = __eq__ = keys = items = values = copy = touched
    def __getattribute__(self, name):
        refuse("argument_attribute")

out, err = io.StringIO(), io.StringIO()
result = {"ok": False, "imports": 0, "api_refusals": 0,
          "bundle_usage_failures": 0, "bundle_reports": 0, "violations": violations}
try:
    with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
        names = []
        for path in request["paths"]:
            suffix = path[:-3].replace("/", ".")
            if suffix == "__init__":
                suffix = ""
            elif suffix.endswith(".__init__"):
                suffix = suffix[:-9]
            names.append("source_integrity_toolkit" + ("." + suffix if suffix else ""))
        for name in sorted(names, key=lambda s: (s.count("."), s)):
            importlib.import_module(name)
            result["imports"] += 1
        import source_integrity_toolkit as sit
        from source_integrity_toolkit import cli
        expected = "Source Integrity Toolkit audit is not implemented in the Phase 1 scaffold."
        for operation in (
                lambda: sit.audit_file(Bomb(), Bomb(), options=Bomb()),
                lambda: sit.audit_file(request["input"], request["output"])):
            try:
                operation()
            except NotImplementedError as exc:
                if str(exc) != expected:
                    raise ProbeViolation("changed_refusal")
                result["api_refusals"] += 1
            else:
                raise ProbeViolation("audit_did_not_refuse")
        for operation in (
                lambda: sit.audit_bundle(Bomb(), options=Bomb()),
                lambda: sit.audit_bundle({"CANARY": [Bomb()]}, options={"raw_file_digest": True})):
            try:
                operation()
            except sit.AuditUsageError as exc:
                if str(exc) != "Invalid audit invocation." or exc.code != "invalid_invocation":
                    raise ProbeViolation("unsafe_usage_failure")
                result["bundle_usage_failures"] += 1
            else:
                raise ProbeViolation("invalid_options_accepted")
        rejected = sit.audit_bundle({"CANARY": [Bomb()]})
        if (type(rejected) is not sit.AuditReport or
                rejected.report_kind != "validation_diagnostics" or
                rejected.input_validation["state"] != "rejected"):
            raise ProbeViolation("hostile_input_accepted")
        if (json.loads(rejected.to_json_bytes())["input_validation"]["state"] != "rejected" or
                b'"state": "rejected"' not in rejected.to_markdown_bytes()):
            raise ProbeViolation("rejected_formats_missing")
        result["bundle_reports"] += 1
        # Independent, finite dossier: one claim inquiry, no seeds or dimensions.
        unknown = {"state": "unknown", "value": None, "precision": None,
                   "reason": "Fictional timing not supplied."}
        provenance = {"attributed_to_ref": "A", "basis_kind": "declaration",
                      "evidence_ref_ids": [], "method": "Finite fictional public boundary.",
                      "qualifications": []}
        source = {"contract_version": "sit-bundle/0.1", "bundle_id": "W08-SCAFFOLD",
                  "snapshot_id": "S1", "recorded_at": unknown, "predecessor": None,
                  "inquiries": [{"id": "I", "target_claim_refs": ["C"], "target_object_refs": [],
                    "seed_artifact_refs": [], "seed_evidence_refs": [],
                    "boundary": {"description": "Fictional boundary.",
                                 "criterion": "Submitted records only.", "system_refs": []},
                    "time_window": {"start": unknown, "end": unknown}, "as_of": unknown,
                    "dependency_dimensions": [], "coverage_assertion_refs": [], "provenance": provenance}],
                  "records": [{"id": "A", "kind": "actor", "provenance": provenance,
                    "data": {"actor_kind": "human", "identity_disclosure": "pseudonymous",
                             "display_name": "Fictional actor."}},
                    {"id": "C", "kind": "claim", "provenance": provenance,
                     "data": {"claim_key": "claim", "version_label": "v1", "text": "Fictional claim.",
                              "context": "Finite public boundary."}}],
                  "assertions": [], "evidence_references": []}
        before = json.dumps(source, sort_keys=True)
        delivered = sit.audit_bundle(source)
        if (type(delivered) is not sit.AuditReport or delivered.report_kind != "audit_report" or
                delivered.run["processing_state"] != "completed" or
                delivered.input_validation["state"] != "accepted"):
            raise ProbeViolation("public_delivery_missing")
        document = json.loads(delivered.to_json_bytes())
        markdown = delivered.to_markdown_bytes()
        if (document["input_identity"]["bundle_id"] != "W08-SCAFFOLD" or
                len(document["capabilities"]) != 15 or len(document["observability_domains"]) != 5 or
                b'"processing_state": "completed"' not in markdown or
                b'"bundle_id": "W08-SCAFFOLD"' not in markdown or
                before != json.dumps(source, sort_keys=True)):
            raise ProbeViolation("public_content_changed")
        result["bundle_reports"] += 1
        if out.getvalue() or err.getvalue():
            raise ProbeViolation("unexpected_import_or_api_output")
        if cli.main(["--version"]) != 0:
            raise ProbeViolation("version_failed")
        if out.getvalue() != "source-integrity-toolkit 0.1.0.dev0\n":
            raise ProbeViolation("version_output_changed")
        out.seek(0); out.truncate(0)
        if cli.main(["--help"]) != 0 or "Phase 1 scaffold" not in out.getvalue():
            raise ProbeViolation("help_failed")
        out.seek(0); out.truncate(0)
        if cli.main(["audit", request["input"], "--output", request["output"], "CANARY_SECRET"]) != 1:
            raise ProbeViolation("audit_exit_changed")
        if out.getvalue() or err.getvalue() != expected + "\n":
            raise ProbeViolation("audit_output_changed")
    result["ok"] = not violations
except BaseException as exc:
    # Constant type name only. Do not leak arbitrary exception text or paths.
    result["exception_type"] = type(exc).__name__
result["violations"] = violations
sys.stdout.write(json.dumps(result, sort_keys=True) + "\n")
raise SystemExit(0 if result["ok"] else 1)
'''


def run_probe(mutation: tuple[str, str] | None = None) -> dict:
    """Copy only known module files; mutations stay in the private temp tree."""
    with tempfile.TemporaryDirectory(prefix="sit-scaffold-probe-") as temp:
        root = Path(temp)
        package = root / "src/source_integrity_toolkit"
        shutil.copytree(ROOT / "src/source_integrity_toolkit", package,
                        ignore=shutil.ignore_patterns("__pycache__"))
        if mutation:
            name, suffix = mutation
            path = package / name
            path.write_text(path.read_text(encoding="utf-8") + suffix, encoding="utf-8")
        input_path, output_path = root / "input.json", root / "output"
        canary = b'{"fixture":"SYNTHETIC_PRIVATE_CANARY"}\n'
        input_path.write_bytes(canary)
        output_path.mkdir()
        (output_path / "existing.txt").write_bytes(b"DO_NOT_TOUCH\n")
        request = {"package": str(package), "paths": sorted(guard.EXPECTED_PATHS),
                   "input": str(input_path), "output": str(output_path)}
        env = dict(os.environ)
        env.pop("PYTHONPATH", None)
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        process = subprocess.run([sys.executable, "-I", "-B", "-c", PROBE],
                                 input=json.dumps(request), text=True, capture_output=True,
                                 timeout=20, cwd=root, env=env)
        if process.stderr:
            raise AssertionError("Unexpected probe stderr: " + process.stderr[:200])
        result = json.loads(process.stdout)
        result["returncode"] = process.returncode
        result["input_unchanged"] = input_path.read_bytes() == canary
        result["output_unchanged"] = (
            sorted(p.name for p in output_path.iterdir()) == ["existing.txt"] and
            (output_path / "existing.txt").read_bytes() == b"DO_NOT_TOUCH\n")
        result["package_paths_unchanged"] = sorted(
            p.relative_to(package).as_posix() for p in package.rglob("*") if p.is_file()) == sorted(guard.EXPECTED_PATHS)
        return result


class ScaffoldInertnessTests(unittest.TestCase):
    def test_cache_helper_preloads_in_clean_interpreter(self):
        # Exercise the actual probe preamble without site initialization or a
        # parent pytest process implicitly providing importlib.util.
        preload, delimiter, _ = PROBE.partition("\nrequest = json.loads(sys.stdin.read())\n")
        self.assertTrue(delimiter)
        imports = {alias.name for node in ast.parse(preload).body
                   if isinstance(node, ast.Import) for alias in node.names}
        self.assertIn("importlib.util", imports)
        self.assertIn("encodings.idna", imports)
        script = preload + "\n" + (
            "cache = importlib.util.cache_from_source('probe.py')\n"
            "if importlib.util.source_from_cache(cache) != 'probe.py':\n"
            "    raise RuntimeError('cache_helper_round_trip_failed')\n"
            "if 'canary.invalid'.encode('idna') != b'canary.invalid':\n"
            "    raise RuntimeError('hostname_helper_failed')\n"
            "print('CACHE_HELPER_READY')\n"
        )
        with tempfile.TemporaryDirectory(prefix="sit-preload-regression-") as temp:
            process = subprocess.run([sys.executable, "-I", "-S", "-B", "-c", script],
                                     cwd=temp, capture_output=True, text=True,
                                     encoding="utf-8", timeout=20)
        self.assertEqual(process.returncode, 0, process.stderr)
        self.assertEqual(process.stdout, "CACHE_HELPER_READY\n")
        self.assertEqual(process.stderr, "")


    def test_dataclasses_preload_in_clean_interpreter(self):
        preload, delimiter, _ = PROBE.partition("\nrequest = json.loads(sys.stdin.read())\n")
        self.assertTrue(delimiter)
        imports = [alias.name for node in ast.parse(preload).body
                   if isinstance(node, ast.Import) for alias in node.names]
        self.assertEqual(imports.count("dataclasses"), 1)
        self.assertEqual(preload.splitlines().count("import dataclasses"), 1)
        exercise = r'''
reads = []
def reject_read(event, args):
    if event == "open":
        reads.append(event)
        raise RuntimeError("post_preload_read")
sys.addaudithook(reject_read)
from dataclasses import dataclass, FrozenInstanceError
@dataclass(frozen=True, slots=True)
class Value:
    label: str
value = Value("FICTIONAL_DECLARATION")
if value.label != "FICTIONAL_DECLARATION":
    raise RuntimeError("dataclass_construction_failed")
try:
    value.label = "CHANGED"
except FrozenInstanceError:
    pass
else:
    raise RuntimeError("frozen_declaration_failed")
if reads:
    raise RuntimeError("post_preload_read_swallowed")
print("DATACLASS_HELPER_READY")
'''
        with tempfile.TemporaryDirectory(prefix="sit-dataclass-regression-") as temp:
            process = subprocess.run(
                [sys.executable, "-I", "-S", "-B", "-c", preload + exercise],
                cwd=temp, capture_output=True, text=True, encoding="utf-8", timeout=20)
            self.assertEqual(process.returncode, 0, process.stderr)
            self.assertEqual(process.stdout, "DATACLASS_HELPER_READY\n")
            self.assertEqual(process.stderr, "")
            missing = preload.replace("import dataclasses", "")
            control = subprocess.run(
                [sys.executable, "-I", "-S", "-B", "-c", missing + exercise],
                cwd=temp, capture_output=True, text=True, encoding="utf-8", timeout=20)
            self.assertNotEqual(control.returncode, 0)
            self.assertEqual(control.stdout, "")
            self.assertIn("post_preload_read", control.stderr)

    def test_imports_api_and_cli_are_inert(self):
        result = run_probe()
        self.assertTrue(result["ok"], result)
        self.assertEqual(result["imports"], 48)
        self.assertEqual(result["api_refusals"], 2)
        self.assertEqual(result["bundle_usage_failures"], 2)
        self.assertEqual(result["bundle_reports"], 2)
        self.assertEqual(result["violations"], [])
        self.assertTrue(result["input_unchanged"] and result["output_unchanged"])
        self.assertTrue(result["package_paths_unchanged"])

    def test_deliberate_evidence_read_is_detected_before_access(self):
        result = run_probe(("analysis/origins.py", '\nimport os\nopen(os.environ["SIT_PROBE_INPUT"], "rb")\n'))
        self.assertFalse(result["ok"])
        self.assertIn("application_open", result["violations"])
        self.assertTrue(result["input_unchanged"])

    def test_deliberate_write_is_detected_before_modification(self):
        result = run_probe(("analysis/origins.py", '\nimport os\nopen(os.environ["SIT_PROBE_INPUT"], "wb")\n'))
        self.assertIn("application_open", result["violations"])
        self.assertTrue(result["input_unchanged"] and result["output_unchanged"])

    def test_deliberate_path_inspection_is_detected(self):
        result = run_probe(("analysis/origins.py", '\nimport os\nos.stat(os.environ["SIT_PROBE_INPUT"])\n'))
        self.assertIn("application_stat", result["violations"])

    def test_stub_that_inspects_argument_is_detected(self):
        result = run_probe(("api.py", '\ndef audit_bundle(bundle, *, options=None):\n    repr(bundle)\n    raise NotImplementedError("unexpected")\n'))
        self.assertFalse(result["ok"])
        self.assertTrue(set(result["violations"]) & {"argument_attribute", "argument_method"})

    def test_swallowed_effect_violation_cannot_become_pass(self):
        result = run_probe(("analysis/origins.py", '\ntry:\n    open(__file__, "rb")\nexcept Exception:\n    pass\n'))
        self.assertFalse(result["ok"])
        self.assertIn("application_open", result["violations"])


if __name__ == "__main__":
    unittest.main()
