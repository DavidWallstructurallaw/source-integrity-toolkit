# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""P4-W08 public invocation safety and retained W07 effect controls.

Observers cover exercised Python effects in a warmed process. They do not claim
hostile same-process isolation, native file validation or future CLI behavior.
"""
import copy
import json
from pathlib import Path
import subprocess
import sys
import traceback
from types import MappingProxyType

import pytest

from source_integrity_toolkit import api
from source_integrity_toolkit import AuditAbort, AuditCancelled, AuditUsageError
from source_integrity_toolkit import AuditReport
from source_integrity_toolkit.runtime import boundary, resources


ROOT = Path(__file__).resolve().parents[2]
CANARY = "FICTIONAL_W07_PRIVATE_SOURCE_EXCEPTION_529713"


def finite_input():
    """Independent minimal claim inquiry from the frozen bundle contract."""
    unknown = {"state": "unknown", "value": None, "precision": None,
               "reason": "Time not supplied in this fictional boundary case."}
    provenance = {"attributed_to_ref": "A", "basis_kind": "declaration",
                  "evidence_ref_ids": [], "method": "Fictional declaration.",
                  "qualifications": []}
    return {
        "contract_version": "sit-bundle/0.1", "bundle_id": "W07-BOUNDARY",
        "snapshot_id": "S1", "recorded_at": copy.deepcopy(unknown),
        "predecessor": None,
        "inquiries": [{"id": "I", "target_claim_refs": ["C"],
            "target_object_refs": [], "seed_artifact_refs": [], "seed_evidence_refs": [],
            "boundary": {"description": "Fictional finite claim only.",
                         "criterion": "Explicit submitted records.", "system_refs": []},
            "time_window": {"start": copy.deepcopy(unknown), "end": copy.deepcopy(unknown)},
            "as_of": copy.deepcopy(unknown), "dependency_dimensions": [],
            "coverage_assertion_refs": [], "provenance": copy.deepcopy(provenance)}],
        "records": [{"id": "A", "kind": "actor", "data": {
            "actor_kind": "human", "identity_disclosure": "pseudonymous",
            "display_name": "Fictional boundary actor."},
            "provenance": copy.deepcopy(provenance)},
            {"id": "C", "kind": "claim", "data": {
            "claim_key": "fictional-claim", "version_label": "v1",
            "text": "Fictional claim.", "context": "Finite boundary test."},
            "provenance": copy.deepcopy(provenance)}],
        "assertions": [], "evidence_references": [],
    }


@pytest.mark.parametrize("kind", (
    "root", "dict_subclass", "key_subclass", "string_subclass", "list_subclass",
    "nested_object", "generator", "cycle",
))
def test_public_invocation_rejects_hostile_input_without_executing_protocols(kind, capsys):
    calls = []

    def touched(*args, **kwargs):
        calls.append("caller_protocol")
        raise AssertionError("untrusted protocol executed")

    class Hostile:
        __str__ = __repr__ = __iter__ = __bool__ = __hash__ = __eq__ = touched
        __int__ = __float__ = __index__ = __fspath__ = touched
        __copy__ = __deepcopy__ = __reduce__ = __reduce_ex__ = touched

    class HostileDict(dict):
        __str__ = __repr__ = __iter__ = __len__ = items = keys = values = touched

    class HostileText(str):
        __str__ = __repr__ = __iter__ = __len__ = __eq__ = touched
        __hash__ = str.__hash__

    class HostileList(list):
        __str__ = __repr__ = __iter__ = __len__ = __getitem__ = touched

    def generator():
        touched()
        yield None

    source = finite_input()
    if kind == "root":
        source = Hostile()
    elif kind == "dict_subclass":
        source = HostileDict(source)
    elif kind == "key_subclass":
        source[HostileText("caller-key")] = CANARY
    elif kind == "string_subclass":
        source["bundle_id"] = HostileText(CANARY)
    elif kind == "list_subclass":
        source["records"] = HostileList(source["records"])
    elif kind == "nested_object":
        source["extensions"] = {"fictional:private": Hostile()}
    elif kind == "generator":
        source["extensions"] = {"fictional:private": generator()}
    else:
        source["extensions"] = {"fictional:cycle": source}
    result = api.audit_bundle(source)
    assert type(result) is AuditReport
    assert result.report_kind == "validation_diagnostics"
    assert result.input_validation["state"] == "rejected"
    assert result.run["processing_state"] == "rejected"
    assert result.results == () and result.findings == ()
    assert calls == []
    assert CANARY.encode() not in result.to_json_bytes() + result.to_markdown_bytes()
    assert capsys.readouterr() == ("", "")


@pytest.mark.parametrize("fault", ("opaque", "memory", "cancel"))
def test_public_native_fault_surface_does_not_format_or_retain_source_exception(fault, monkeypatch, capsys):
    calls = []

    class Opaque(Exception):
        def __str__(self):
            calls.append("str")
            raise AssertionError("native exception formatted")

        def __repr__(self):
            calls.append("repr")
            raise AssertionError("native exception represented")

    def fail(*args, **kwargs):
        if fault == "opaque":
            raise Opaque(CANARY)
        if fault == "memory":
            raise MemoryError(CANARY)
        raise KeyboardInterrupt(CANARY)

    monkeypatch.setattr(boundary, "_admit", fail)
    source = finite_input()
    before = copy.deepcopy(source)
    try:
        result = api.audit_bundle(source)
    except (AuditAbort, AuditCancelled) as error:
        if fault == "cancel":
            assert type(error) is AuditCancelled
            assert not hasattr(error, "reason_code")
        else:
            assert type(error) is AuditAbort and error.reason_code == "execution_failed"
        assert error.input_validation_state == "not_completed"
        assert error.publication_state == "not_published"
        assert CANARY not in str(error) + repr(error) + str(error.args)
        assert CANARY not in "".join(traceback.format_exception(error))
    else:
        assert fault != "cancel"
        assert type(result) is AuditReport
        assert result.report_kind == "processing_diagnostics"
        assert result.run["processing_state"] == "failed"
        assert result.input_validation["state"] == "not_completed"
        assert CANARY.encode() not in result.to_json_bytes() + result.to_markdown_bytes()
    assert calls == [] and source == before
    assert capsys.readouterr() == ("", "")


def test_public_report_contains_only_frozen_disclosure_and_two_cached_bytes(monkeypatch):
    source = finite_input()
    source["extensions"] = {"fictional:private": {"secret": CANARY}}
    before = copy.deepcopy(source)
    report = api.audit_bundle(source)
    assert type(report) is AuditReport
    assert report.run["processing_state"] == "completed"
    assert report.input_validation["state"] == "accepted"
    assert source == before
    assert not hasattr(report, "__dict__")
    assert AuditReport.__slots__ == ("_document", "_json_bytes", "_markdown_bytes")
    original_json, original_markdown = report.to_json_bytes(), report.to_markdown_bytes()
    assert CANARY.encode() not in original_json + original_markdown
    source.clear()

    def forbidden(*args, **kwargs):
        raise AssertionError("cached report started new runtime work")

    monkeypatch.setattr(resources, "monotonic_ns", forbidden)
    monkeypatch.setattr(boundary, "_new_analysis_budget", forbidden)
    monkeypatch.setattr(boundary, "_audit_value", forbidden)
    from source_integrity_toolkit.reporting import json_report, markdown_report
    monkeypatch.setattr(json_report, "_encode_json_report", forbidden)
    monkeypatch.setattr(markdown_report, "_encode_markdown_report", forbidden)
    for unused in range(3):
        assert report.to_json_bytes() is original_json
        assert report.to_markdown_bytes() is original_markdown
        assert report.input_identity["bundle_id"] == "W07-BOUNDARY"

    from source_integrity_toolkit.contracts.report import _ReportMapping
    assert type(report._document) is MappingProxyType
    assert len(report._document) == 16
    pending = []
    for key, value in report._document.items():
        assert type(key) is str
        pending.append(value)
    while pending:
        value = pending.pop()
        if type(value) is _ReportMapping:
            assert type(value._pairs) is tuple
            for key, item in value._pairs:
                assert type(key) is str
                pending.append(item)
        elif type(value) is tuple:
            pending.extend(value)
        else:
            assert type(value) in (str, bool, int, type(None))


def test_public_usage_and_file_refusals_leave_hostile_arguments_untouched():
    calls = []

    class Hostile:
        def touched(self, *args, **kwargs):
            calls.append("caller_protocol")
            raise AssertionError("public stub touched input")
        __repr__ = __str__ = __iter__ = __len__ = __fspath__ = touched

    hostile = Hostile()
    with pytest.raises(AuditUsageError, match="^Invalid audit invocation\\.$"):
        api.audit_bundle(hostile, options=hostile)
    with pytest.raises(NotImplementedError):
        api.audit_file(hostile, hostile, options=hostile)
    assert calls == []


PROBE = r'''
import sys,json,ctypes,socket,subprocess,os,builtins,io
import encodings.idna
sys.path.insert(0,sys.argv[1])
from source_integrity_toolkit import audit_bundle
from source_integrity_toolkit import AuditReport
source=json.loads(sys.stdin.buffer.read());mode=sys.argv[2];events=[]
# Warm trusted imports before observing the entire subsequent invocation.
# Negative controls exercise each observer directly and need no audit replay.
if mode=='success':
    warm=audit_bundle(source)
    assert type(warm) is AuditReport and warm.run['processing_state']=='completed'
before=json.dumps(source,sort_keys=True)
def audit(event,args):
    if event=='open' or event.startswith('socket.') or event=='ctypes.dlopen' or event=='subprocess.Popen' or event in ('os.listdir','os.scandir'):
        events.append(event);raise RuntimeError('blocked_observed_effect')
sys.addaudithook(audit)
def metadata_trap(*args,**kwargs):
    events.append('metadata.stat');raise RuntimeError('blocked_metadata_effect')
os.stat=metadata_trap;os.lstat=metadata_trap
try:
    if mode=='negative-open': builtins.open('FICTIONAL_MUST_NOT_OPEN','rb')
    elif mode=='negative-listdir': os.listdir('FICTIONAL_MUST_NOT_ENUMERATE')
    elif mode=='negative-stat': os.stat('FICTIONAL_MUST_NOT_STAT')
    elif mode=='negative-network': socket.getaddrinfo('fictional.invalid',443)
    elif mode=='negative-native': ctypes.CDLL('FICTIONAL_MUST_NOT_LOAD')
    elif mode=='negative-process': subprocess.Popen([sys.executable,'-c','pass'])
    else:
        report=audit_bundle(source)
        assert type(report) is AuditReport and report.run['processing_state']=='completed'
        assert report.to_json_bytes()==warm.to_json_bytes()
        assert report.to_markdown_bytes()==warm.to_markdown_bytes()
        rejected=audit_bundle({'fictional:source':source})
        assert type(rejected) is AuditReport and rejected.input_validation['state']=='rejected'
        assert json.dumps(source,sort_keys=True)==before
except RuntimeError:
    if not mode.startswith('negative-'): raise
print(json.dumps({'events':events,'ok':True}))
'''


@pytest.mark.parametrize("mode,event", (
    ("success", None), ("negative-open", "open"),
    ("negative-listdir", "os.listdir"), ("negative-stat", "metadata.stat"),
    ("negative-network", "socket.getaddrinfo"), ("negative-native", "ctypes.dlopen"),
    ("negative-process", "subprocess.Popen"),
))
def test_public_complete_invocation_has_no_observed_file_network_native_or_process_effect(mode, event):
    source = finite_input()
    source["extensions"] = {"fictional:untrusted": {
        "path": "../" + CANARY, "$ref": "https://fictional.invalid/schema",
        "code": "__import__('os').system('FICTIONAL_MUST_NOT_EXECUTE')",
    }}
    run = subprocess.run([sys.executable, "-I", "-S", "-B", "-c", PROBE,
        str(ROOT / "src"), mode], input=json.dumps(source).encode(),
        capture_output=True, timeout=90)
    assert run.returncode == 0, run.stderr.decode(errors="replace")
    assert json.loads(run.stdout) == {"ok": True, "events": [] if event is None else [event]}
    assert run.stderr == b"" and CANARY.encode() not in run.stdout


@pytest.mark.parametrize("kind", (
    "opaque_options", "dict_subclass", "text_key_subclass", "collision_key",
    "hostile_value", "unknown_key", "too_many_keys", "list_options",
))
def test_hostile_options_are_rejected_before_dossier_or_runtime_access(kind, monkeypatch, capsys):
    calls = []

    def touched(*args, **kwargs):
        calls.append("caller_protocol")
        raise AssertionError("options executed a caller protocol")

    class Hostile:
        __str__ = __repr__ = __iter__ = __bool__ = __eq__ = touched
        __len__ = __getitem__ = __int__ = __float__ = __index__ = touched
        __fspath__ = __copy__ = __deepcopy__ = touched

    class HostileDict(dict):
        __str__ = __repr__ = __iter__ = __len__ = items = keys = values = touched
        __getitem__ = __contains__ = touched

    class HostileText(str):
        __str__ = __repr__ = __iter__ = __len__ = __eq__ = touched
        __hash__ = str.__hash__

    class CollisionKey(Hostile):
        def __hash__(self):
            # Building the caller-owned dict is outside the observed operation.
            # A lookup for this literal during validation would invoke __eq__.
            calls.append("caller_hash")
            return hash("raw_file_digest")

    if kind == "opaque_options":
        options = Hostile()
    elif kind == "dict_subclass":
        options = HostileDict(raw_file_digest=False)
    elif kind == "text_key_subclass":
        options = {HostileText("raw_file_digest"): False}
    elif kind == "collision_key":
        options = {CollisionKey(): False}
    elif kind == "hostile_value":
        options = {"raw_file_digest": Hostile()}
    elif kind == "unknown_key":
        options = {CANARY: Hostile()}
    elif kind == "too_many_keys":
        options = {"raw_file_digest": False, CANARY: Hostile()}
    else:
        options = [Hostile()]
    calls.clear()
    dossier = HostileDict()

    def runtime_forbidden(*args, **kwargs):
        calls.append("runtime")
        raise AssertionError("invalid options reached the invocation")

    monkeypatch.setattr(api, "_audit_value", runtime_forbidden)
    monkeypatch.setattr(boundary, "_new_analysis_budget", runtime_forbidden)
    with pytest.raises(AuditUsageError) as captured:
        api.audit_bundle(dossier, options=options)
    error = captured.value
    assert type(error) is AuditUsageError
    assert error.code == "invalid_invocation"
    assert str(error) == error.safe_message == "Invalid audit invocation."
    assert error.args == ("Invalid audit invocation.",)
    assert CANARY not in repr(error) + str(error.args) + "".join(traceback.format_exception(error))
    assert calls == [] and capsys.readouterr() == ("", "")
