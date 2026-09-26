# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W14 clean installed private analysis with closed distribution inventories.

Only developer tests read fixtures/oracles. The child receives their bytes and
independently specified assertions through stdin; no test/catalog is installed.
Original heroes retain their fixed-budget stopping behavior. A separate finite
source example demonstrates completed installed arithmetic and member identity.
"""
import hashlib
import importlib.util
import inspect
import json
import os
from pathlib import Path
import subprocess
import tarfile
import zipfile

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _inventory(path):
    if path.name.endswith('.whl'):
        with zipfile.ZipFile(path) as archive:
            names = archive.namelist()
            assert len(names) == len(set(names)) == 55
            members = {name: hashlib.sha256(archive.read(name)).hexdigest() for name in names}
    else:
        with tarfile.open(path) as archive:
            regular = [member for member in archive.getmembers() if member.isfile()]
            assert len(regular) == len({member.name for member in regular}) == 65
            members = {member.name: hashlib.sha256(archive.extractfile(member).read()).hexdigest()
                       for member in regular}
    return {'name': path.name, 'bytes': path.stat().st_size,
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest(), 'members': members}


@pytest.fixture(scope='module')
def installed_runtime(tmp_path_factory):
    packaging = _load('sit_w14_packaging', 'tests/scaffold/test_packaging.py')
    packaging.test_declared_toolchain_is_actually_available()
    distributions = packaging.distributions.__wrapped__(tmp_path_factory)
    packaging.test_source_distribution_inventory(distributions)
    packaging.test_wheel_inventory_and_metadata(distributions)
    work = tmp_path_factory.mktemp('w14-installed')
    # Reuse the existing offline clean-runtime and public-refusal checks.
    packaging.test_wheel_installs_without_developer_tools(distributions, work)
    rebuild = tmp_path_factory.mktemp('w14-rebuild')
    packaging.test_source_distribution_rebuilds_same_package(distributions, rebuild)
    rebuilt = next((rebuild / 'source_integrity_toolkit-0.1.0.dev0/dist').glob('*.whl'))
    inventory = [_inventory(path) for path in (distributions[1], distributions[2], rebuilt)]
    assert inventory[1]['members'] == inventory[2]['members']
    python = work / 'runtime' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    return work, python, inventory


_CHILD = r'''
import sys,json,copy,hashlib,importlib,importlib.metadata,socket,ctypes
import encodings.idna
from pathlib import Path
payload=json.loads(sys.stdin.buffer.read())
assert {d.metadata['Name'] for d in importlib.metadata.distributions()} == {'source-integrity-toolkit'}
loaded={}
for name,expected in payload['modules'].items():
    module=importlib.import_module(name)
    path=Path(module.__file__).resolve()
    assert path.is_relative_to(Path(sys.prefix).resolve())
    assert hashlib.sha256(path.read_bytes()).hexdigest()==expected
    loaded[name]=expected
assert len(loaded)==48
from source_integrity_toolkit.runtime import boundary,resources
from source_integrity_toolkit.contracts.report import _AnalyticalOutcome
import source_integrity_toolkit as package
assert package.__version__=='0.1.0.dev0'
assert set(package.__all__)=={'audit_bundle','audit_file','__version__'}
assert resources._WORK_LIMIT==10_000_000 and resources._JOB_WORK_LIMIT==1_000_000
assert resources._DEADLINE_NS==60_000_000_000
events=[]
def audit(event,args):
    if event=='open' or event.startswith('socket.') or event=='ctypes.dlopen':
        events.append(event)
        raise RuntimeError('blocked_installed_effect')
sys.addaudithook(audit)
heroes=[]
for entry in payload['heroes']:
    for mode in ('value','utf8'):
        heroes.append(_hero_analysis(entry['raw'].encode('utf-8'),entry['expected'],mode))
completed=[]
for mode in ('value','utf8'):
    source=copy.deepcopy(payload['finite_source'])
    before=copy.deepcopy(source)
    out=(boundary._analyze_value(source) if mode=='value' else
         boundary._analyze_utf8(json.dumps(source).encode('utf-8')))
    assert type(out) is _AnalyticalOutcome
    assert out.input_state=='accepted' and out.execution_state=='completed'
    assert source==before
    rows={row.ref.field_key:row for row in out.results if row.value is not None}
    for field,expected in payload['finite_expectations']['counts'].items():
        row=rows[field]
        assert row.execution_state=='completed' and row.result_state=='available'
        assert row.value.value==expected
    membership=rows['per_seed_origin_memberships']
    actual={item.member_ref.identifier:[ref.identifier for ref in item.origin_refs]
            for item in membership.value.memberships}
    assert actual==payload['finite_expectations']['memberships']
    hhi=rows['single_origin_contribution_hhi']
    assert hhi.result_state=='available'
    assert [hhi.value.numerator,hhi.value.denominator]==payload['finite_expectations']['hhi']
    assert [ref.identifier for ref in hhi.value.population.member_refs]==['e','e2']
    assert {'coverage','boundary','parent-e','parent-e2'} <= {
        ref.source.identifier for ref in hhi.basis_refs}
    assert next(check.state for check in hhi.check_refs if check.check_id=='PC24')=='met'
    assert len(out.capabilities)==15 and len(out.domains)==5
    assert not hasattr(out,'report_kind') and not hasattr(out,'overall_level')
    completed.append({'mode':mode,'state':out.execution_state,'counts':payload['finite_expectations']['counts'],
                      'memberships':actual,'hhi':[hhi.value.numerator,hhi.value.denominator],
                      'source_unchanged':source==before,'capabilities':len(out.capabilities),'domains':len(out.domains)})
for fn in (boundary._analyze_value,boundary._analyze_utf8):
    bad=fn({} if fn is boundary._analyze_value else b'{}')
    assert bad.input_state=='rejected' and not hasattr(bad,'results')
for call,args in ((package.audit_bundle,(object(),)),(package.audit_file,(object(),object()))):
    try:call(*args,options=object())
    except NotImplementedError:pass
    else:raise AssertionError('public_audit_activated')
assert events==[]
for probe in (lambda:open('FICTIONAL_MUST_NOT_OPEN','rb'),
              lambda:socket.getaddrinfo('fictional.invalid',443),
              lambda:ctypes.CDLL('FICTIONAL_MUST_NOT_LOAD')):
    try:probe()
    except RuntimeError:pass
assert events==['open','socket.getaddrinfo','ctypes.dlopen']
print(json.dumps({'modules':loaded,'hero_modes':heroes,'completed_finite_modes':completed,
    'normal_effects':[],'negative_events':events,'public_refusals':2,'invalid_modes':2,
    'runtime_distributions':['source-integrity-toolkit']}))
'''


def test_clean_installed_analysis_original_heroes_and_completed_finite_case(installed_runtime):
    work, python, inventories = installed_runtime
    hero = _load('sit_w14_hero_assertions', 'tests/integration/test_analytical_hero_inputs.py')
    finite = _load('sit_w14_independent_finite_source', 'tests/integration/test_analytical_pipeline.py')
    modules = {}
    for path in sorted((ROOT / 'src/source_integrity_toolkit').rglob('*.py')):
        relative = path.relative_to(ROOT / 'src').as_posix()
        name = relative.removesuffix('.py').replace('/', '.').removesuffix('.__init__')
        modules[name] = hashlib.sha256(path.read_bytes()).hexdigest()
    assert len(modules) == 48
    heroes = [{'raw': (ROOT / 'tests/fixtures/hero' / (case + '.bundle.json')).read_bytes().decode('utf-8'),
               'expected': hero._hero_expectation(case)} for case in hero.HEROES]
    # Definitions 22/23: two distinct contributions both document one origin.
    # The complete N**2 denominator is four, never a reduced or weighted proxy.
    expectations = {'counts': {'nominal_seed_artifact_record_count': 1,
        'seed_evidence_item_count': 2, 'claim_artifact_record_count': 1,
        'reached_origin_record_count': 1, 'documentary_origin_boundary_record_count': 1},
        'memberships': {'e': ['origin'], 'e2': ['origin']}, 'hhi': [4, 4]}
    payload = {'modules': modules, 'heroes': heroes, 'finite_source': finite._documented_value(),
               'finite_expectations': expectations}
    # The helper is developer assertion code, sent to -c; it is not installed.
    script = inspect.getsource(hero._hero_analysis) + '\n' + _CHILD
    run = subprocess.run([str(python), '-I', '-B', '-c', script], cwd=work,
        input=json.dumps(payload).encode('utf-8'), capture_output=True, timeout=600)
    assert run.returncode == 0, run.stderr.decode(errors='replace')
    assert run.stderr == b''
    actual = json.loads(run.stdout)
    assert actual['modules'] == modules and len(actual['hero_modes']) == 8
    assert len(actual['completed_finite_modes']) == 2
    assert actual['normal_effects'] == []
    paths = [Path(__file__), ROOT / 'tests/integration/test_analytical_hero_inputs.py',
             ROOT / 'tests/integration/test_analytical_pipeline.py']
    fixture_paths = [ROOT / 'tests' / kind / (case + suffix) for case in hero.HEROES
                     for kind, suffix in (('fixtures/hero', '.bundle.json'), ('golden', '.logical.json'))]
    record = {'head': subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip(),
        'scope': 'W14 installed private analysis; original hero stops are not completed golden certification',
        'unit': 'P3-W14', 'ok': True, 'runtime': actual, 'distributions': inventories,
        'test_sources': {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                         for path in paths},
        'frozen_test_sources': {path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
                                for path in fixture_paths}}
    destination = (Path(os.environ['RUNNER_TEMP']) / 'sit-p3/evidence'
                   if os.environ.get('GITHUB_ACTIONS') == 'true' else work)
    destination.mkdir(parents=True, exist_ok=True)
    (destination / 'w14-installed-runtime.json').write_text(
        json.dumps(record, sort_keys=True, indent=2) + '\n', encoding='utf-8')
