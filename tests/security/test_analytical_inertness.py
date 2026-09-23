# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W14 warm full-analysis interception and exact caller-protocol refusal.

The separate inherited scaffold subprocess probes cover import-time isolation,
all 48 modules and loader-scoped file/network/native negative controls. This
probe starts after warm imports and has no product file-access exception.
Test-authored counterexamples share the W13 helpers and accepted source lineage;
they are finite observations, not hostile-process isolation or external review.
"""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys

import pytest

from source_integrity_toolkit.runtime import boundary
from source_integrity_toolkit.runtime.diagnostics import _SafeDiagnostic


ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    'sit_w14_inert_cases', ROOT / 'tests/integration/test_analytical_pipeline.py')
cases = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cases)
FIXTURES = json.loads((ROOT / 'tests/fixtures/adversarial/phase3_cases.json').read_bytes())
CANARY = 'FICTIONAL_W14_PRIVATE_901842'


def source():
    value = cases._minimal_value()
    value['inquiries'][0].update(seed_artifact_refs=['artifact'], dependency_dimensions=['acquisition'])
    value['records'].append(cases._record('artifact', 'artifact', {
        'artifact_kind': 'document', 'work_key': 'work', 'version_label': 'v1',
        'locators': [], 'published_at': cases._unknown(), 'retrieved_at': cases._unknown(),
        'content_evidence_refs': []}))
    delta = FIXTURES['cases'][0]['delta']
    value['extensions'] = delta['extensions']
    value['records'][-1]['data']['locators'] = delta['artifact_locators']
    value['records'][1]['data']['text'] = delta['claim_text']
    return value


PROBE = r'''
import sys,json,dataclasses,typing,ctypes,socket,subprocess,os,builtins,io,logging,copy
import encodings.idna
sys.path.insert(0,sys.argv[1])
from source_integrity_toolkit.runtime.boundary import _analyze_value,_analyze_utf8
from source_integrity_toolkit.contracts.report import _AnalyticalOutcome
from source_integrity_toolkit.runtime.diagnostics import _SafeDiagnostic
request=json.loads(sys.stdin.buffer.read());source=request['source'];mode=sys.argv[2];events=[]
expected=request['expected'];rejection=request['rejection']
original=copy.deepcopy(source)
logger=logging.getLogger('sit.w14.synthetic');logger.setLevel(logging.DEBUG)
def audit(event,args):
    if event=='open' or event.startswith(('socket.','ctypes.')) or event=='subprocess.Popen' or event in ('os.listdir','os.scandir','os.system'):
        events.append(event);raise RuntimeError('blocked_real_effect')
def metadata_trap(*args,**kwargs):
    events.append('metadata.stat');raise RuntimeError('blocked_metadata_probe')
def logging_trap(*args,**kwargs):
    events.append('logging.record');raise RuntimeError('blocked_logging')
sys.addaudithook(audit)
os.stat=metadata_trap;os.lstat=metadata_trap
logging.setLogRecordFactory(logging_trap)
try:
    if mode=='negative-open': builtins.open('FICTIONAL_MUST_NOT_OPEN','rb')
    elif mode=='negative-write': io.open('FICTIONAL_MUST_NOT_WRITE','wb')
    elif mode=='negative-listdir': os.listdir('FICTIONAL_MUST_NOT_ENUMERATE')
    elif mode=='negative-stat': os.stat('FICTIONAL_MUST_NOT_STAT')
    elif mode=='negative-network': socket.getaddrinfo('fictional.invalid',443)
    elif mode=='negative-socket': socket.socket()
    elif mode=='negative-native': ctypes.CDLL('FICTIONAL_MUST_NOT_LOAD')
    elif mode=='negative-process': subprocess.Popen([sys.executable,'-c','pass'])
    elif mode=='negative-logging': logger.warning('FICTIONAL_W14_PRIVATE_901842')
    else:
        analyze=_analyze_value if mode=='constructed_value' else lambda value:_analyze_utf8(json.dumps(value).encode())
        first=analyze(source);repeat=analyze(source)
        for out in (first,repeat):
            assert type(out) is _AnalyticalOutcome
            assert (out.input_state,out.execution_state)==(expected['input_state'],expected['execution_state'])
            rows=[r for r in out.results if r.ref.diagnostic_id=='SIT-M001' and r.ref.field_key=='nominal_seed_artifact_record_count']
            assert len(rows)==1 and rows[0].value.value==expected['nominal_seed_artifact_record_count']
            assert not any(r.ref.field_key=='FORGED_RESULT' for r in out.results)
        assert first is not repeat and first.prepared is not repeat.prepared
        bad=copy.deepcopy(source);bad['FICTIONAL_W14_PRIVATE_901842']=True
        refused=analyze(bad)
        assert type(refused) is _SafeDiagnostic
        assert (refused.input_state,refused.execution_state)==(rejection['input_state'],rejection['execution_state'])
        assert not hasattr(refused,'prepared') and not hasattr(refused,'results')
        assert all('FICTIONAL_W14_PRIVATE_901842' not in str(getattr(refused,f.name)) for f in dataclasses.fields(refused))
        changed=copy.deepcopy(source)
        extra=copy.deepcopy(changed['records'][-1]);extra['id']='artifact2';extra['data']['work_key']='work2'
        changed['records'].append(extra);changed['inquiries'][0]['seed_artifact_refs'].append('artifact2')
        fresh=analyze(changed)
        assert type(fresh) is _AnalyticalOutcome and fresh.execution_state=='completed'
        count=[r for r in fresh.results if r.ref.diagnostic_id=='SIT-M001' and r.ref.field_key=='nominal_seed_artifact_record_count']
        assert len(count)==1 and count[0].value.value==2
        assert source==original
except RuntimeError:
    if not mode.startswith('negative-'): raise
print(json.dumps({'events':events,'ok':True}))
'''


@pytest.mark.parametrize('mode,event', [
    ('constructed_value', None), ('supplied_utf8', None),
    ('negative-open', 'open'), ('negative-write', 'open'),
    ('negative-listdir', 'os.listdir'), ('negative-stat', 'metadata.stat'),
    ('negative-network', 'socket.getaddrinfo'), ('negative-socket', 'socket.__new__'),
    ('negative-native', 'ctypes.dlopen'), ('negative-process', 'subprocess.Popen'),
    ('negative-logging', 'logging.record'),
])
def test_warm_actual_analysis_cannot_acquire_source_effect_authority(mode, event):
    request = {'source': source(), 'expected': FIXTURES['cases'][0]['expected'],
               'rejection': FIXTURES['cases'][1]['expected']}
    run = subprocess.run([sys.executable, '-I', '-S', '-B', '-c', PROBE, str(ROOT / 'src'), mode],
        input=json.dumps(request).encode(), capture_output=True, timeout=120)
    assert run.returncode == 0, run.stderr.decode(errors='replace')
    assert json.loads(run.stdout) == {'ok': True, 'events': [] if event is None else [event]}
    assert run.stderr == b'' and CANARY.encode() not in run.stdout


@pytest.mark.parametrize('mutation', ('root_subclass', 'key_subclass', 'callback', 'cycle', 'bytes_subclass'))
def test_actual_analysis_rejects_caller_protocols_without_invoking_them(mutation, capsys):
    calls = []
    def touched(*args, **kwargs):
        calls.append('caller_protocol')
        raise AssertionError(CANARY)
    class Hostile:
        __repr__ = __str__ = __iter__ = __fspath__ = __bool__ = __hash__ = __eq__ = touched
    class Root(dict):
        __iter__ = __repr__ = items = keys = touched
    class Key(str):
        __repr__ = __str__ = touched
    class Bytes(bytes):
        decode = __repr__ = __str__ = touched
    value = source()
    if mutation == 'root_subclass': value = Root(value)
    elif mutation == 'key_subclass': value[Key('FICTIONAL_PRIVATE_KEY')] = True
    elif mutation == 'callback': value['extensions'] = {'fictional:callback': Hostile()}
    elif mutation == 'cycle': value['extensions'] = {'fictional:cycle': value}
    out = (boundary._analyze_utf8(Bytes(b'{}')) if mutation == 'bytes_subclass'
           else boundary._analyze_value(value))
    assert type(out) is _SafeDiagnostic
    assert (out.input_state, out.execution_state) == ('rejected', 'rejected')
    assert out.code == ('input_constraint_violation' if mutation == 'cycle' else 'type_or_enum_violation')
    assert calls == [] and capsys.readouterr() == ('', '')
    assert not hasattr(out, 'results') and not hasattr(out, 'prepared')
