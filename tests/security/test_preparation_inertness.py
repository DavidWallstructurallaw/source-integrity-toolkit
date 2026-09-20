# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W07 integrated effects, diagnostics, replay and phase-boundary regressions.

Authority: architecture 17, 19; privacy 8; governance 22; Phase 2 plan 13.
The subprocess harness owns stdin and process launch. Product receives only
values or bytes. Audit hooks plus exact metadata traps are finite observations,
not a claim of hostile same-process isolation or a native file-interface test.
"""
import copy
from dataclasses import fields
import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import sys
from unittest.mock import patch
import pytest
from source_integrity_toolkit.contracts.report import _ObservabilityPreparation
from source_integrity_toolkit.runtime import boundary, resources
from source_integrity_toolkit.runtime.diagnostics import _SafeDiagnostic

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("sit_w07_independent_cases", ROOT / "tests/integration/test_preparation_pipeline.py")
cases = importlib.util.module_from_spec(spec); spec.loader.exec_module(cases)
CANARY = cases.CANARY


def diagnostic_surface(value):
    assert type(value) is _SafeDiagnostic
    return repr(value) + str(value) + "|".join(str(getattr(value, f.name)) for f in fields(value))


PROBE = r'''
import sys,json,dataclasses,typing,ctypes,socket,subprocess,os,builtins,io
import encodings.idna
sys.path.insert(0,sys.argv[1])
from source_integrity_toolkit.runtime.boundary import _prepare_evidence_value,_prepare_evidence_utf8
from source_integrity_toolkit.contracts.report import _ObservabilityPreparation
from source_integrity_toolkit.contracts.bundle import _Object
raw=sys.stdin.buffer.read();source=json.loads(raw);mode=sys.argv[2];events=[]
# Harness-only capture precedes all observations; all product imports are warm.
original=json.dumps(source,sort_keys=True)
def audit(event,args):
    if event=='open' or event.startswith('socket.') or event=='ctypes.dlopen' or event=='subprocess.Popen' or event in ('os.listdir','os.scandir'):
        events.append(event);raise RuntimeError('blocked_real_effect')
sys.addaudithook(audit)
# os.stat lacks a matching open audit event; keep this separate from that claim.
def metadata_trap(*args,**kwargs):
    events.append('metadata.stat');raise RuntimeError('blocked_metadata_probe')
os.stat=metadata_trap;os.lstat=metadata_trap
try:
    if mode=='negative-open': builtins.open('FICTIONAL_MUST_NOT_OPEN','rb')
    elif mode=='negative-io': io.open('FICTIONAL_MUST_NOT_OPEN','rb')
    elif mode=='negative-listdir': os.listdir('FICTIONAL_MUST_NOT_ENUMERATE')
    elif mode=='negative-scandir': os.scandir('FICTIONAL_MUST_NOT_ENUMERATE')
    elif mode=='negative-stat': os.stat('FICTIONAL_MUST_NOT_STAT')
    elif mode=='negative-network': socket.getaddrinfo('fictional.invalid',443)
    elif mode=='negative-native': ctypes.CDLL('FICTIONAL_MUST_NOT_LOAD')
    elif mode=='negative-process': subprocess.Popen([sys.executable,'-c','pass'])
    else:
        a=_prepare_evidence_value(source);b=_prepare_evidence_utf8(raw)
        assert type(a) is _ObservabilityPreparation and type(b) is _ObservabilityPreparation
        bad=dict(source);bad['FICTIONAL_W07_PRIVATE_318472']=True
        c=_prepare_evidence_value(bad)
        assert c.input_state=='rejected' and not hasattr(c,'prepared')
        d=_prepare_evidence_value(source)
        assert type(d) is _ObservabilityPreparation and d is not a and d.prepared is not a.prepared
        assert json.dumps(source,sort_keys=True)==original
        assert a.inquiries[0].prerequisites[11].answer is None
        assert all(not x.complete_check_executed for x in a.inquiries[0].prerequisites[1:])
except RuntimeError:
    if not mode.startswith('negative-'): raise
print(json.dumps({'events':events,'ok':True}))
'''


@pytest.mark.parametrize("mode,event", [
    ("success", None), ("negative-open", "open"), ("negative-io", "open"),
    ("negative-listdir", "os.listdir"), ("negative-scandir", "os.scandir"),
    ("negative-stat", "metadata.stat"), ("negative-network", "socket.getaddrinfo"),
    ("negative-native", "ctypes.dlopen"), ("negative-process", "subprocess.Popen"),
])
def test_integrated_source_strings_cannot_acquire_io_network_native_or_process_authority(mode, event):
    source = cases.dossier()
    source["extensions"] = {"fictional:untrusted": {"$ref": "https://fictional.invalid/schema", "path": "../" + CANARY,
        "code": "__import__('os').system('FICTIONAL_MUST_NOT_EXECUTE')", "whole_prerequisites_completed": ["PC12"],
        "available_result_refs": ["FORGED"], "unicode": "\u202e\n```json\n" + CANARY}}
    find = cases.find(source, "AR-a")
    find["data"]["locators"] = ["file:///FICTIONAL/" + CANARY, "https://fictional.invalid/" + CANARY]
    find["data"]["checksums"] = [{"algorithm": "sha256", "value": "not-authenticated", "covered_material": CANARY}]
    run = subprocess.run([sys.executable, "-I", "-S", "-B", "-c", PROBE, str(ROOT / "src"), mode],
        input=json.dumps(source).encode(), capture_output=True, timeout=90)
    assert run.returncode == 0, run.stderr.decode(errors="replace")
    assert json.loads(run.stdout) == {"ok": True, "events": [] if event is None else [event]}
    assert run.stderr == b"" and CANARY.encode() not in run.stdout


@pytest.mark.parametrize("mode", ["navigate-value", "navigate-bytes"])
@pytest.mark.parametrize("stage,input_state", [("_validate_structure", "not_completed"), ("_observe_evidence_input", "accepted")])
@pytest.mark.parametrize("fault", ["opaque_exception", "memory", "cancel", "work"])
def test_fault_transport_never_formats_an_exception_or_returns_a_partial_snapshot(mode, stage, input_state, fault, capsys):
    class Opaque(Exception):
        def __str__(self): raise AssertionError("exception_str_called")
        def __repr__(self): raise AssertionError("exception_repr_called")
    budget = resources._new_budget()
    def fail(*args, **kwargs):
        if fault == "opaque_exception": raise Opaque(CANARY)
        if fault == "memory": raise MemoryError(CANARY)
        if fault == "cancel": raise KeyboardInterrupt(CANARY)
        budget.interrupt("WU9-L11")
    source = cases.dossier(); before = copy.deepcopy(source)
    with patch.object(boundary, "_new_budget", return_value=budget), patch.object(boundary, stage, fail):
        out = cases.execute(source, mode)
    assert type(out) is _SafeDiagnostic and out.input_state == input_state
    expected = "cancelled" if fault == "cancel" else "interrupted" if fault == "work" else "failed"
    assert out.execution_state == expected and CANARY not in diagnostic_surface(out)
    assert out.code == (None if fault == "cancel" else "resource_limit_reached" if fault == "work" else "execution_failed")
    assert out.location is None and not hasattr(out, "prepared") and not hasattr(out, "inquiries")
    assert source == before and capsys.readouterr() == ("", "")
    assert type(boundary._prepare_evidence_value(source)) is _ObservabilityPreparation


@pytest.mark.parametrize("mode", ["navigate-value", "navigate-bytes"])
@pytest.mark.parametrize("delta", [-1, 0, 1])
def test_actual_deadline_is_not_reset_between_admission_and_navigation(mode, delta):
    now = [0]; original = boundary._observe_evidence_input
    def at_boundary(value, port):
        now[0] = 60_000_000_000 + delta
        return original(value, port)
    with patch.object(resources, "monotonic_ns", lambda: now[0]), patch.object(boundary, "_observe_evidence_input", at_boundary):
        out = cases.execute(cases.dossier(), mode)
    if delta <= 0: cases.assert_admitted(out, mode)
    else:
        assert type(out) is _SafeDiagnostic and out.input_state == "accepted"
        assert out.execution_state == "interrupted" and out.qualifications == ("WU9-L12",)
        assert not hasattr(out, "prepared")


@pytest.mark.parametrize("bad", ["root_subclass", "key_subclass", "value_callback", "container_cycle"])
def test_untrusted_python_protocols_remain_unused_through_full_navigation(bad):
    calls = []
    def touched(*args, **kwargs): calls.append("executed"); raise AssertionError("caller_protocol_called")
    class Hostile:
        __repr__ = __str__ = __iter__ = __fspath__ = __bool__ = __hash__ = __eq__ = touched
    class Root(dict):
        __iter__ = __repr__ = items = keys = touched
    class Key(str):
        __repr__ = __str__ = touched
    value = cases.dossier()
    if bad == "root_subclass": value = Root(value)
    elif bad == "key_subclass": value[Key("unknown-key")] = True
    elif bad == "value_callback": value["extensions"] = {"fictional:callback": Hostile()}
    else: value["extensions"] = {"fictional:cycle": value}
    out = boundary._prepare_evidence_value(value)
    assert type(out) is _SafeDiagnostic and out.input_state == "rejected" and calls == []
    assert out.code == ("input_constraint_violation" if bad == "container_cycle" else "type_or_enum_violation")


@pytest.mark.parametrize("target", ["analysis/origins.py", "reporting/assemble.py", "io/platform_linux.py", "io/platform_windows.py"])
def test_whole_package_guard_rejects_forbidden_implementation_in_temporary_copy(tmp_path, target):
    sys.path.insert(0, str(ROOT))
    from tools import check_scaffold_boundary as guard
    unit = f"P2-W{guard.unit_number():02}"
    assert guard.check_repository(ROOT, unit=unit)["ok"]
    root = tmp_path / "isolated-probe"
    shutil.copytree(ROOT / "src/source_integrity_toolkit", root / "src/source_integrity_toolkit")
    for name in ("PHASE_2_PLAN.md", "phase2/entry_manifest.json", "phase2/module_policy.json", "scaffold/delivery_manifest.json"):
        dest = root / name; dest.parent.mkdir(parents=True, exist_ok=True); shutil.copyfile(ROOT / name, dest)
    assert guard.check_repository(root, unit=unit)["ok"]
    changed = root / "src/source_integrity_toolkit" / target
    assert changed.is_file()
    changed.write_bytes(changed.read_bytes() + b'\nUNAUTHORIZED_RESULT = {"independent": True}\n')
    assert not guard.check_repository(root, unit=unit)["ok"]
    assert guard.check_repository(ROOT, unit=unit)["ok"]
