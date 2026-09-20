# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W06 private boundary and real frozen H7 navigation, with actual effects probes."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from unittest.mock import patch
import pytest
from source_integrity_toolkit.contracts.bundle import _CapturedBundle
from source_integrity_toolkit.contracts.evidence import _PreparedBundle
from source_integrity_toolkit.contracts.report import _ObservabilityPreparation, FAMILIES
from source_integrity_toolkit.runtime import boundary
from source_integrity_toolkit.runtime.boundary import _prepare_value, _capture_value, _prepare_evidence_value, _prepare_evidence_utf8
from source_integrity_toolkit.runtime.resources import _new_budget
from source_integrity_toolkit.runtime.diagnostics import _SafeDiagnostic
from source_integrity_toolkit.validation import semantics

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("sit_w06_integration_cases", ROOT / "tests/contract/test_typed_records.py")
cases = importlib.util.module_from_spec(spec); spec.loader.exec_module(cases)
CANARY = "FICTIONAL_W06_PRIVATE_SOURCE_953182"


@pytest.mark.parametrize("hero", ["H7-01", "H7-V01", "H7-V02", "H7-V03"])
@pytest.mark.parametrize("mode", ["value", "bytes"])
def test_frozen_heroes_reach_navigation_without_producing_any_analytical_result(hero, mode):
    raw = (ROOT / "tests/fixtures/hero" / (hero + ".bundle.json")).read_bytes(); source = json.loads(raw)
    out = _prepare_evidence_value(source) if mode == "value" else _prepare_evidence_utf8(raw)
    assert type(out) is _ObservabilityPreparation and out.input_state == "accepted"
    assert len(out.snapshot_records) == sum(len(source[k]) for k in ("records", "inquiries", "assertions", "evidence_references"))
    assert {r.record_id for r in out.snapshot_records} == {r["id"] for k in ("records", "inquiries", "assertions", "evidence_references") for r in source[k]}
    assert len(out.inquiries) == len(source["inquiries"])
    for row in out.inquiries:
        assert tuple(f.family for f in row.families) == FAMILIES
        assert sum(len(f.field_keys) for f in row.families) == 57
        assert [p.prerequisite for p in row.prerequisites if p.complete_check_executed] == ["PC01"]
        assert len(row.domains) == 5
    for name in ("results", "report_kind", "available_result_refs", "overall_level", "max_level", "hhi", "findings", "report_id"):
        assert not hasattr(out, name)
    # Golden metric values are never imported or passed to the product.
    assert out.prepared.source_mode == ("constructed_value" if mode == "value" else "supplied_utf8")


def test_capture_admission_and_navigation_are_distinct_private_components():
    assert type(_capture_value({})) is _CapturedBundle
    assert _prepare_value({}).input_state == "rejected"
    assert _prepare_evidence_value({}).input_state == "rejected"
    source = cases.sparse()
    assert type(_prepare_value(source)) is _PreparedBundle
    out = _prepare_evidence_value(source)
    assert type(out) is _ObservabilityPreparation and type(out.prepared) is _PreparedBundle
    import source_integrity_toolkit as toolkit
    assert set(toolkit.__all__) == {"audit_bundle", "audit_file", "__version__"}
    with pytest.raises(NotImplementedError): toolkit.audit_bundle(source)


@pytest.mark.parametrize("mode", ["value", "bytes"])
@pytest.mark.parametrize("stage", ["_observe_evidence_input", "_assemble_observability", "_ObservabilityPreparation"])
@pytest.mark.parametrize("fault", ["error", "cancel", "resource"])
def test_every_postadmission_stop_preserves_input_acceptance_without_partial_navigation(mode, stage, fault):
    budget = _new_budget()
    def fail(*args, **kwargs):
        if fault == "error": raise RuntimeError(CANARY)
        if fault == "cancel": raise KeyboardInterrupt(CANARY)
        budget.interrupt("WU9-L11")
    source = cases.sparse()
    with patch.object(boundary, "_new_budget", return_value=budget), patch.object(boundary, stage, fail):
        out = _prepare_evidence_value(source) if mode == "value" else _prepare_evidence_utf8(json.dumps(source).encode())
    assert type(out) is _SafeDiagnostic and out.input_state == "accepted"
    assert out.execution_state == {"error": "failed", "cancel": "cancelled", "resource": "interrupted"}[fault]
    assert budget.input_state == "accepted" and CANARY not in str(out) + repr(out) + out.safe_message
    assert not hasattr(out, "inquiries") and not hasattr(out, "prepared")


@pytest.mark.parametrize("stage", ["_observe_record", "_observe_inquiry_bindings"])
def test_incomplete_scan_never_yields_a_false_no_binding_statement(stage):
    with patch.object(semantics, stage, side_effect=RuntimeError(CANARY)):
        out = _prepare_evidence_value(cases.rich())
    assert type(out) is _SafeDiagnostic and out.execution_state == "failed"
    assert out.input_state == "accepted" and not hasattr(out, "families")


def test_one_context_and_nonresetting_work_budget_cover_admission_and_navigation():
    budget = _new_budget(); observed = []; original = boundary._observe_evidence_input
    def observe(prepared, port):
        assert port is budget and budget.input_state == "accepted" and budget.used > 1024
        before = budget.used; result = original(prepared, port)
        observed.append((before, budget.used)); return result
    with patch.object(boundary, "_new_budget", return_value=budget) as factory, patch.object(boundary, "_observe_evidence_input", observe):
        out = _prepare_evidence_value(cases.sparse())
    assert type(out) is _ObservabilityPreparation and factory.call_count == 1
    assert len(observed) == 1 and 1024 < observed[0][0] < observed[0][1] < budget.used <= 10000000


def test_exhaustion_after_admission_is_not_reset_for_assembly():
    budget = _new_budget(); original = boundary._observe_evidence_input
    def exhaust(prepared, port):
        result = original(prepared, port); port.charge(port.remaining); return result
    with patch.object(boundary, "_new_budget", return_value=budget), patch.object(boundary, "_observe_evidence_input", exhaust):
        out = _prepare_evidence_value(cases.sparse())
    assert type(out) is _SafeDiagnostic and out.input_state == "accepted"
    assert out.execution_state == "interrupted" and out.qualifications == ("WU9-L11",)
    assert budget.used == 10000000


@pytest.mark.parametrize("bad", [{}, {"report_kind": "audit_report"}, {"contract_version": "wrong"}])
def test_invalid_inputs_never_receive_domains_or_prerequisite_answers(bad):
    out = _prepare_evidence_value(bad)
    assert type(out) is _SafeDiagnostic and out.input_state == "rejected"
    assert not hasattr(out, "inquiries") and not hasattr(out, "prerequisites")


def test_hostile_objects_and_public_bypass_options_are_not_invoked():
    class Hostile:
        def __repr__(self): raise AssertionError("repr")
        def __iter__(self): raise AssertionError("iter")
        def __fspath__(self): raise AssertionError("path")
    for fn in (_prepare_evidence_value, _prepare_evidence_utf8):
        out = fn(Hostile()); assert type(out) is _SafeDiagnostic
        with pytest.raises(TypeError): fn(cases.sparse(), skip_validation=True)
        with pytest.raises(TypeError): fn(cases.sparse(), budget=_new_budget())
    source = cases.sparse(); source["extensions"] = {"fictional:control": {"whole_checks_implemented": ["PC12"], "max_level": 4}}
    out = _prepare_evidence_value(source)
    assert out.inquiries[0].prerequisites[11].answer is None and not hasattr(out, "max_level")


def test_repeated_success_failure_success_has_no_stale_state_or_canary_output(capsys):
    source = cases.rich(); before = copy.deepcopy(source)
    a = _prepare_evidence_value(source); bad = copy.deepcopy(source); bad[CANARY] = CANARY
    fail = _prepare_evidence_value(bad); b = _prepare_evidence_value(source)
    assert type(a) is _ObservabilityPreparation and type(b) is _ObservabilityPreparation and a is not b
    assert a.prepared is not b.prepared and a.snapshot_records is not b.snapshot_records
    assert type(fail) is _SafeDiagnostic and CANARY not in fail.safe_message + repr(fail)
    assert source == before and capsys.readouterr() == ("", "")


PROBE = r'''
import sys,json,dataclasses,typing,ctypes,socket
import encodings.idna
sys.path.insert(0,sys.argv[1])
from source_integrity_toolkit.runtime.boundary import _prepare_evidence_value,_prepare_evidence_utf8
from source_integrity_toolkit.contracts.report import _ObservabilityPreparation
mode=sys.argv[2]
with open(sys.argv[3],'rb') as f: raw=f.read()
source=json.loads(raw);events=[]
def audit(event,args):
    if event=='open' or event.startswith('socket.') or event=='ctypes.dlopen':
        events.append(event);raise RuntimeError('blocked_effect')
sys.addaudithook(audit)
if mode=='open':
    try: open('FICTIONAL_MUST_NOT_OPEN','rb')
    except RuntimeError: pass
elif mode=='network':
    try: socket.getaddrinfo('fictional.invalid',443)
    except RuntimeError: pass
elif mode=='native':
    try: ctypes.CDLL('FICTIONAL_MUST_NOT_LOAD')
    except RuntimeError: pass
else:
    if mode=='invalid':source['FICTIONAL_W06_PRIVATE_SOURCE_953182']=True
    a=_prepare_evidence_value(source);b=_prepare_evidence_utf8(raw)
    assert type(b) is _ObservabilityPreparation
    assert (type(a) is _ObservabilityPreparation)==(mode=='success')
print(json.dumps({'ok':True,'events':events}))
'''


@pytest.mark.parametrize("mode", ["success", "invalid", "open", "network", "native"])
def test_navigation_no_io_network_or_native_activity_with_real_negative_controls(mode):
    result = subprocess.run([sys.executable, "-I", "-S", "-B", "-c", PROBE, str(ROOT / "src"), mode,
        str(ROOT / "tests/fixtures/hero/H7-01.bundle.json")], capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr
    events = {"open": "open", "network": "socket.getaddrinfo", "native": "ctypes.dlopen"}
    assert json.loads(result.stdout) == {"ok": True, "events": [events[mode]] if mode in events else []}
    assert CANARY not in result.stdout + result.stderr
