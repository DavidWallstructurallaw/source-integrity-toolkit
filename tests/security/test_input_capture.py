# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Capture faults, isolation canaries and the exact P2-W04-R01 authority delta."""
import ast
import hashlib
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from dataclasses import fields
from unittest.mock import patch
import pytest
from source_integrity_toolkit.runtime.boundary import _capture_utf8 as _prepare_utf8, _capture_value as _prepare_value
from source_integrity_toolkit.runtime.resources import _new_budget
from source_integrity_toolkit.runtime.diagnostics import _diagnostic, _CONSTRAINT_BASIS
from source_integrity_toolkit.contracts.execution import _PreparationAborted, _CONSTRAINT_CODES
from source_integrity_toolkit.contracts.bundle import _CapturedBundle
from source_integrity_toolkit.validation import structure

ROOT=Path(__file__).resolve().parents[2]
CANARY="FICTIONAL_SECRET_PATH_NAME_KEY_EXCEPTION_77893"
ENTRY="e292bf6023a59d3019221a768d9f2d4ac5c4d4cf"
EXTRA=frozenset(("src/source_integrity_toolkit/contracts/execution.py",
    "src/source_integrity_toolkit/runtime/diagnostics.py",
    "tests/scaffold/test_ci_contract.py", "tests/contract/test_bundle_contract.py"))


def visible(value):
    return repr(value)+str(value)+"|".join(str(getattr(value,f.name)) for f in fields(value))


@pytest.mark.parametrize("failure", ["cancel", "failure", "resource"])
@pytest.mark.parametrize("mode", ["value", "bytes"])
def test_capture_faults_never_return_partial_snapshots_or_relabel_cancellation(failure,mode):
    def stop(frame,ledger,decoded):
        if failure=="cancel": raise KeyboardInterrupt(CANARY)
        if failure=="failure": raise RuntimeError(CANARY)
        ledger.port.interrupt("WU9-L11")
    with patch.object(structure,"_next_child",stop):
        result=_prepare_value({"x":CANARY}) if mode=="value" else _prepare_utf8(json.dumps({"x":CANARY}).encode())
    assert result.input_state=="not_completed"
    assert result.code=={"cancel":None,"failure":"execution_failed","resource":"resource_limit_reached"}[failure]
    assert result.execution_state=={"cancel":"cancelled","failure":"failed","resource":"interrupted"}[failure]
    assert not hasattr(result,"tree") and CANARY not in visible(result)


@pytest.mark.parametrize("mode", ["value","bytes"])
def test_real_deadline_is_checked_during_work_and_before_result_delivery(mode):
    now=[0]; calls=[0]
    def clock():
        calls[0]+=1
        return 0 if calls[0]<40 else 60_000_000_001
    with patch("source_integrity_toolkit.runtime.resources.monotonic_ns",clock):
        result=_prepare_value({"x":[None]*30}) if mode=="value" else _prepare_utf8(b'{"x":[null,null,null,null]}')
    assert result.qualifications==("WU9-L12",) and result.input_state=="not_completed"


@pytest.mark.parametrize("mode", ["value","bytes"])
def test_decoder_or_capture_error_text_cannot_enter_any_diagnostic_surface(mode,capsys):
    if mode=="bytes":
        with patch("source_integrity_toolkit.io.input_file.json.loads",side_effect=RuntimeError(CANARY)):
            result=_prepare_utf8(b'{"x":1}')
    else:
        with patch.object(structure,"_finish",side_effect=RuntimeError(CANARY)):
            result=_prepare_value({"x":1})
    assert result.code=="execution_failed" and CANARY not in visible(result)
    assert len(visible(result).encode())<4096 and capsys.readouterr()==("","")


@pytest.mark.parametrize("payload", [b'"x"',b'{"a":1,"a":2}',b'{"x":"\\ud800"}',b'{"x":NaN}',b'{"x":1}tail'])
def test_synthetic_canaries_remain_out_of_failure_messages(payload,capsys):
    raw=payload.replace(b'"x"',json.dumps(CANARY).encode()).replace(b'"a"',json.dumps(CANARY).encode())
    result=_prepare_utf8(raw)
    assert CANARY not in visible(result) and result.location is None
    assert not hasattr(result,"original_exception") and capsys.readouterr()==("","")


@pytest.mark.parametrize("value", ["/private/"+CANARY,bytearray(b"{}"),memoryview(b"{}"),{},[],None])
def test_bytes_seam_does_not_coerce_paths_or_mutable_buffers(value):
    result=_prepare_utf8(value)
    assert result.code=="type_or_enum_violation" and CANARY not in visible(result)


def test_bytes_subclass_decode_and_stream_read_are_never_invoked():
    calls=[]
    class Raw(bytes):
        def decode(self,*args): calls.append("decode");raise AssertionError()
    class Stream:
        def read(self,*args): calls.append("read");raise AssertionError()
        def __bytes__(self): calls.append("bytes");raise AssertionError()
        def __repr__(self): calls.append("repr");raise AssertionError()
    for value in (Raw(b"{}"),Stream()):
        assert _prepare_utf8(value).code=="type_or_enum_violation"
    assert calls==[]


def test_capture_cannot_select_budget_clock_or_mode_from_input_or_environment(monkeypatch):
    monkeypatch.setenv("SIT_WORK_LIMIT","999999999999999")
    monkeypatch.setenv("SIT_INPUT_LIMIT","999999999999999")
    source={"options":{"decoded":True,"raw_file_digest":True,"clock":CANARY,"limit":999999999999},"value":()}
    assert _prepare_value(source).code=="type_or_enum_violation"
    with pytest.raises(TypeError): _prepare_value({},options={"limit":999})
    with pytest.raises(TypeError): _prepare_utf8(b"{}",decoded=True)


ISOLATED=r'''
import sys,json,dataclasses,typing,ctypes,socket
import encodings.idna
sys.path.insert(0,sys.argv[1])
from source_integrity_toolkit.runtime.boundary import _capture_value as _prepare_value,_capture_utf8 as _prepare_utf8
from source_integrity_toolkit.contracts.bundle import _CapturedBundle
mode=sys.argv[2]
events=[]
def audit(event,args):
    if event=='open' or event.startswith('socket.') or event=='ctypes.dlopen':
        events.append(event)
        raise RuntimeError('blocked_effect')
sys.addaudithook(audit)
if mode=='negative-open':
    try: open('FICTIONAL_MUST_NOT_OPEN','rb')
    except RuntimeError: pass
elif mode=='negative-network':
    try: socket.getaddrinfo('fictional.invalid',443)
    except RuntimeError: pass
elif mode=='negative-native':
    try: ctypes.CDLL('FICTIONAL_MUST_NOT_LOAD')
    except RuntimeError: pass
else:
    source={'path':'FICTIONAL_SECRET_PATH','url':'https://fictional.invalid','nested':[None,True,1]}
    if mode=='cycle': source['self']=source
    if mode=='malformed': source['nested']=(None,)
    a=_prepare_value(source)
    b=_prepare_utf8(b'{"path":"FICTIONAL_SECRET_PATH","url":"https://fictional.invalid"}')
    assert type(b) is _CapturedBundle
    assert (type(a) is _CapturedBundle)==(mode=='success')
print(json.dumps({'events':events,'ok':True}))
'''


@pytest.mark.parametrize("mode", ["success","cycle","malformed","negative-open","negative-network","negative-native"])
def test_isolated_capture_has_no_source_io_network_or_native_loading(mode):
    result=subprocess.run([sys.executable,"-I","-S","-B","-c",ISOLATED,str(ROOT/"src"),mode],
        text=True,capture_output=True,timeout=30)
    assert result.returncode==0, result.stderr
    data=json.loads(result.stdout)
    assert data["ok"] is True and "FICTIONAL_SECRET_PATH" not in result.stdout+result.stderr
    expected={"negative-open":"open","negative-network":"socket.getaddrinfo","negative-native":"ctypes.dlopen"}
    assert data["events"]==([expected[mode]] if mode in expected else [])


def test_cycle_qualifier_is_the_only_new_private_rule_and_has_one_fixed_basis():
    assert _CONSTRAINT_CODES==("exact_integer_range","unicode_scalar","identifier_ascii",
        "identifier_length","string_length","locator_length","container_cycle")
    matches=[text for code,text in _CONSTRAINT_BASIS if code=="container_cycle"]
    assert matches==["REPOSITORY_ARCHITECTURE section 17.1: acyclic caller-container ancestry."]
    budget=_new_budget()
    with pytest.raises(_PreparationAborted) as raised:
        budget.reject("input_constraint_violation","container_cycle")
    record=_diagnostic(raised.value)
    assert record.code=="input_constraint_violation" and record.input_state=="rejected"
    assert record.qualifications==tuple(matches)


@pytest.mark.parametrize("qualifier", [None,"unknown",CANARY,"container_cycle ",True])
def test_missing_or_unapproved_qualifiers_still_fail_closed(qualifier):
    b=_new_budget()
    with pytest.raises(_PreparationAborted) as raised: b.reject("input_constraint_violation",qualifier)
    assert raised.value.stop.reason_code=="execution_failed"
    assert CANARY not in visible(_diagnostic(raised.value))


def old_file(relative,pin):
    raw=subprocess.check_output(["git","show",ENTRY+":"+relative],cwd=ROOT,timeout=30)
    assert hashlib.sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()==pin
    return raw


def ci_driver():
    spec=importlib.util.spec_from_file_location("sit_w04_ci",ROOT/"tests/scaffold/test_ci_contract.py")
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    return module


def test_r01_exact_four_paths_and_no_other_unit_permission_expansion():
    ci=ci_driver();paths=ci.phase_guard.plan_paths(ROOT)
    assert ci.P2_W04_R01_PATHS==EXTRA and len(paths["P2-W04"])==12
    assert not EXTRA & paths["P2-W04"]
    for step in range(1,10):
        unit=f"P2-W{step:02}"
        extra=ci.P2_W02_R01_PATHS if step==2 else EXTRA if step==4 else (ci.P2_W05_R01_PATHS | ci.P2_W05_R02_PATHS) if step==5 else frozenset()
        if step==7: extra=extra | ci.P2_W07_R01_PATHS
        if step==8: extra=extra | ci.P2_W08_R01_PATHS
        if step==9: extra=extra | ci.P2_W09_R01_PATHS
        assert ci.effective_paths(paths,unit)==paths[unit]|extra
        ci.check_changed_paths(paths,unit,paths[unit]|extra)
        for path in EXTRA-paths[unit]-extra:
            with pytest.raises(ValueError,match="^work_unit_allowlist_exceeded$"):
                ci.check_changed_paths(paths,unit,{path})
        cumulative=set().union(*(paths[f"P2-W{i:02}"] for i in range(1,step+1)))
        if step>=2: cumulative.update(ci.P2_W02_R01_PATHS)
        if step>=4: cumulative.update(EXTRA)
        if step>=5: cumulative.update(ci.P2_W05_R01_PATHS | ci.P2_W05_R02_PATHS)
        if step>=7: cumulative.update(ci.P2_W07_R01_PATHS)
        if step>=8: cumulative.update(ci.P2_W08_R01_PATHS)
        if step>=9: cumulative.update(ci.P2_W09_R01_PATHS)
        assert ci.effective_paths(paths,unit,cumulative=True)==cumulative


@pytest.mark.parametrize("path", ["tests/security/test_scaffold_inertness.py",
    "src/source_integrity_toolkit/runtime/resources.py", "src/source_integrity_toolkit/contracts/execution.py.bak",
    "tests/contract/../scaffold/test_ci_contract.py", "tools/check_scaffold_boundary.py", "PHASE_2_PLAN.md"])
def test_r01_similar_or_unlisted_repair_paths_are_refused(path):
    ci=ci_driver();paths=ci.phase_guard.plan_paths(ci.ROOT)
    with pytest.raises(ValueError,match="^work_unit_allowlist_exceeded$"):
        ci.check_changed_paths(paths,"P2-W04",paths["P2-W04"]|EXTRA|{path})


def test_r01_only_two_old_scope_test_bodies_change_and_identities_survive():
    relative="tests/contract/test_bundle_contract.py"
    old=ast.parse(old_file(relative,"55377de1b6955b8d7345d1f094974f7ddc704188"))
    new=ast.parse((ROOT/relative).read_bytes())
    allowed={"test_repair_does_not_expand_another_units_immediate_diff",
        "test_repair_cumulative_accounting_retains_only_authorized_extras"}
    assert [n.name for n in old.body if isinstance(n,ast.FunctionDef)]==[n.name for n in new.body if isinstance(n,ast.FunctionDef)]
    for tree in (old,new):
        for node in tree.body:
            if isinstance(node,ast.FunctionDef) and node.name in allowed: node.body=[ast.Pass()]
    assert ast.dump(old,include_attributes=False)==ast.dump(new,include_attributes=False)


def test_r01_execution_and_diagnostic_changes_are_exact_constant_additions():
    p="src/source_integrity_toolkit/"
    old=old_file(p+"contracts/execution.py","a5d66263f572c2b888d148727b97797a3aa0a521").decode()
    new=(ROOT/p/"contracts/execution.py").read_text()
    assert new==old.replace('"identifier_length", "string_length", "locator_length",',
        '"identifier_length", "string_length", "locator_length", "container_cycle",')
    old=old_file(p+"runtime/diagnostics.py","1873edfdf9379991cb4750b6a8e41f8dd7ccb85c").decode()
    new=(ROOT/p/"runtime/diagnostics.py").read_text()
    assert new==old.replace('\n)\n_STRUCTURAL_BASIS',
        '\n    ("container_cycle", "REPOSITORY_ARCHITECTURE section 17.1: acyclic caller-container ancestry."),\n)\n_STRUCTURAL_BASIS')
