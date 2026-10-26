# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Public installed witnesses reused by the existing preparation/analysis tests.

The helpers below execute in the clean installed interpreters, including direct
sdist and rebuilt-wheel installs from the existing W14 build. They are not
installed with the product. Literal finite semantic expectations come from the
bundle/report contracts; independent standard-library encoders compare both
complete byte representations of the sixteen exposed public roots.
"""
import copy
import hashlib
import inspect
import json
import os
from pathlib import Path
import subprocess


PUBLIC_ROOTS = (
    'contract_version', 'report_kind', 'report_id', 'run', 'input_identity',
    'input_validation', 'scopes', 'populations', 'basis_index', 'capabilities',
    'checks', 'observability_domains', 'results', 'findings', 'reasons',
    'release_limits',
)


def public_payload():
    """Independent explicit-acquisition case, with no selected seed members."""
    unknown = {'state': 'unknown', 'value': None, 'precision': None,
               'reason': 'Fictional time not supplied.'}
    provenance = {'attributed_to_ref': 'A', 'basis_kind': 'declaration',
                  'evidence_ref_ids': [], 'method': 'Fictional declaration.',
                  'qualifications': []}
    source = {
        'contract_version': 'sit-bundle/0.1', 'bundle_id': 'P4-W08-INSTALLED',
        'snapshot_id': 'S', 'recorded_at': copy.deepcopy(unknown), 'predecessor': None,
        'inquiries': [{'id': 'I', 'target_claim_refs': ['C'], 'target_object_refs': [],
            'seed_artifact_refs': [], 'seed_evidence_refs': [],
            'boundary': {'description': 'Fictional finite scope.',
                         'criterion': 'Only supplied records.', 'system_refs': []},
            'time_window': {'start': copy.deepcopy(unknown), 'end': copy.deepcopy(unknown)},
            'as_of': copy.deepcopy(unknown), 'dependency_dimensions': ['acquisition'],
            'coverage_assertion_refs': [], 'provenance': copy.deepcopy(provenance)}],
        'records': [
            {'id': 'A', 'kind': 'actor', 'data': {'actor_kind': 'human',
                'identity_disclosure': 'pseudonymous',
                'display_name': 'P4-W08-INSTALLED-PRIVATE-DISPLAY'},
             'provenance': copy.deepcopy(provenance)},
            {'id': 'C', 'kind': 'claim', 'data': {'claim_key': 'K', 'version_label': 'v1',
                'text': 'Fictional claim.', 'context': 'Fictional supplied context.'},
             'provenance': copy.deepcopy(provenance)}],
        'assertions': [], 'evidence_references': [],
    }
    expected = {
        'bundle_id': 'P4-W08-INSTALLED', 'snapshot_id': 'S',
        'family_ids': ['SIT-M' + str(n).zfill(3) for n in range(1, 16)],
        'counts': {'nominal_seed_artifact_record_count': 0,
            'seed_evidence_item_count': 0, 'claim_artifact_record_count': 0,
            'unresolved_seed_artifact_reference_count': 0},
        'basis_total': 3,
        'basis_members': [['inquiries', 'I'], ['records', 'A'], ['records', 'C']],
        'unavailable_fractions': ['single_origin_contribution_hhi',
            'documentary_origin_resolution_fraction', 'inherited_only_seed_fraction'],
        'unavailable_reason': 'zero_denominator',
        'excluded_canary': 'P4-W08-INSTALLED-PRIVATE-DISPLAY',
    }
    return {'source': source, 'expected': expected}


def _public_plain(value):
    if isinstance(value, Mapping):
        return {key: _public_plain(item) for key, item in value.items()}
    if type(value) is tuple:
        return [_public_plain(item) for item in value]
    assert value is None or type(value) in (str, int, bool)
    return value


def _public_json(value, pretty=False):
    text = json.dumps(value, ensure_ascii=False, sort_keys=True, allow_nan=False,
                      indent=2 if pretty else None,
                      separators=(',', ': ') if pretty else (',', ':'))
    short = {'\\b': '\\u0008', '\\f': '\\u000c', '\\n': '\\u000a',
             '\\r': '\\u000d', '\\t': '\\u0009'}
    def replace(match):
        token = match.group()
        if token.startswith('\\'):
            return short.get(token, token)
        return '\\u' + format(ord(token), '04x')
    return re.sub(r'\\.|[\u007f-\u009f\u061c\u200e\u200f\u2028-\u202e\u2066-\u2069]',
                  replace, text)


def _public_markdown(document):
    text = ('# Source Integrity Audit\n\nReport kind: ' + document['report_kind'] +
            '\nProcessing state: ' + document['run']['processing_state'] +
            '\nInput state: ' + document['input_validation']['state'] + '\n\n')
    def block(value):
        body = _public_json(value, pretty=True)
        longest = max((len(match.group()) for match in re.finditer(r'`+', body)), default=0)
        fence = '`' * max(3, longest + 1)
        return fence + 'json\n' + body + '\n' + fence + '\n'
    for index, name in enumerate(PUBLIC_ROOTS):
        text += '## ' + name + '\n\n'
        if name != 'results' or not document['results']:
            text += block(document[name])
            if index != len(PUBLIC_ROOTS) - 1:
                text += '\n'
            continue
        for row in document['results']:
            text += '### ' + row['id'] + ': ' + row['field_key'] + '\n\n'
            text += block(row) + '\n'
            if row['result_state'] == 'available' and row['value_kind'] == 'fraction':
                n, d = row['value']['numerator'], row['value']['denominator']
                with localcontext() as context:
                    context.prec = 80
                    decimal = (Decimal(n) / Decimal(d)).quantize(
                        Decimal('0.000001'), rounding=ROUND_HALF_UP)
                text += 'Decimal display: ' + str(n) + '/' + str(d) + ' = ' + format(decimal, '.6f') + '\n\n'
            text += 'Reason details\n\n'
            text += block([reason for reason in document['reasons']
                           if reason['id'] in row['reason_refs']]) + '\n'
    return text.encode('utf-8')


def _public_witness(source, expected):
    before = copy.deepcopy(source)
    input_bytes = json.dumps(source, sort_keys=True, separators=(',', ':')).encode('utf-8')
    expected_bytes = json.dumps(expected, sort_keys=True, separators=(',', ':')).encode('utf-8')
    report = package.audit_bundle(source, options={'raw_file_digest': False})
    assert type(report) is package.AuditReport
    assert source == before
    document = {name: _public_plain(getattr(report, name)) for name in PUBLIC_ROOTS}
    assert document['contract_version'] == 'sit-report/0.1'
    assert document['report_id'] == 'SIT-RPT-000001' and document['report_kind'] == 'audit_report'
    assert document['run']['processing_state'] == 'completed'
    assert document['input_validation'] == {'state': 'accepted', 'diagnostics': []}
    assert document['run']['tool_version'] == '0.1.0.dev0'
    assert document['run']['requested_diagnostic_ids'] == expected['family_ids']
    assert document['run']['completed_diagnostic_ids'] == expected['family_ids']
    assert document['run']['diagnostics'] == []
    assert len(document['capabilities']) == 15
    assert sorted(row['diagnostic_id'] for row in document['capabilities']) == expected['family_ids']
    assert [row['level_index'] for row in document['observability_domains']] == list(range(5))
    assert document['input_identity']['bundle_id'] == expected['bundle_id']
    assert document['input_identity']['snapshot_id'] == expected['snapshot_id']
    assert document['input_identity']['source_mode'] == 'in_process'
    assert document['input_identity']['raw_file_digest'] is None
    assert document['input_identity']['qualifications'] and document['release_limits']
    for name in ('started_at', 'finished_at'):
        assert document['run'][name] == {'state': 'unknown', 'value': None,
            'precision': None, 'reason': 'not_recorded_by_SIT-RP-0.1'}
    assert all(row['execution_state'] == 'completed' for row in document['results'])
    by_field = {}
    for row in document['results']:
        by_field.setdefault(row['field_key'], []).append(row)
    for field, value in expected['counts'].items():
        rows = by_field[field]
        assert len(rows) == 1 and rows[0]['result_state'] == 'available'
        assert type(rows[0]['value']) is int and rows[0]['value'] == value
    inventory, = by_field['declared_basis_inventory']
    assert inventory['result_state'] == 'available'
    assert inventory['value']['total'] == expected['basis_total']
    declaration, = [row for row in inventory['value']['categories'] if row['label'] == 'declaration']
    assert declaration['count'] == expected['basis_total']
    assert sorted([ref['collection'], ref['identifier']] for ref in declaration['member_refs']) == expected['basis_members']
    reasons = {row['id']: row for row in document['reasons']}
    for field in expected['unavailable_fractions']:
        row, = by_field[field]
        assert row['result_state'] == 'unavailable' and row['value'] is None
        assert expected['unavailable_reason'] in {reasons[ref]['code'] for ref in row['reason_refs']}
    json_raw, markdown_raw = report.to_json_bytes(), report.to_markdown_bytes()
    json_expected = (_public_json(document) + '\n').encode('utf-8')
    markdown_expected = _public_markdown(document)
    assert type(json_raw) is type(markdown_raw) is bytes
    assert json_raw == json_expected and markdown_raw == markdown_expected
    assert json.loads(json_raw) == document
    assert expected['excluded_canary'].encode() not in json_raw + markdown_raw
    for unused in range(3):
        assert report.to_json_bytes() is json_raw and report.to_markdown_bytes() is markdown_raw
    source.clear()
    assert report.input_identity['bundle_id'] == expected['bundle_id']
    try:
        report.results = ()
    except (AttributeError, TypeError):
        pass
    else:
        raise AssertionError('mutable_public_report')
    try:
        report.input_identity['bundle_id'] = 'changed'
    except TypeError:
        pass
    else:
        raise AssertionError('mutable_nested_public_report')
    assert report.to_json_bytes() is json_raw and report.to_markdown_bytes() is markdown_raw
    return {'case_id': expected['bundle_id'], 'input_sha256': hashlib.sha256(input_bytes).hexdigest(),
        'expectations_sha256': hashlib.sha256(expected_bytes).hexdigest(),
        'report_kind': report.report_kind, 'processing_state': report.run['processing_state'],
        'input_state': report.input_validation['state'], 'root_members': list(PUBLIC_ROOTS),
        'family_ids': expected['family_ids'], 'counts': expected['counts'],
        'unavailable_fractions': expected['unavailable_fractions'],
        'basis_total': expected['basis_total'], 'basis_members': expected['basis_members'],
        'source_unchanged': before == json.loads(input_bytes), 'detached_after_source_clear': True,
        'immutable_roots_and_nested': True, 'cached_identity_reads': 3,
        'json': {'bytes': len(json_raw), 'sha256': hashlib.sha256(json_raw).hexdigest(),
                 'independent_sha256': hashlib.sha256(json_expected).hexdigest()},
        'markdown': {'bytes': len(markdown_raw), 'sha256': hashlib.sha256(markdown_raw).hexdigest(),
                     'independent_sha256': hashlib.sha256(markdown_expected).hexdigest()}}


def public_script():
    imports = ('import copy,hashlib,json,re\nfrom collections.abc import Mapping\n'
               'from decimal import Decimal,localcontext,ROUND_HALF_UP\n')
    functions = (_public_plain, _public_json, _public_markdown, _public_witness)
    return imports + 'PUBLIC_ROOTS = ' + repr(PUBLIC_ROOTS) + '\n' + '\n'.join(
        inspect.getsource(function) for function in functions) + '\n'


def additional_installed_public_witnesses(work, distributions, modules):
    """Use the existing sdist/rebuilt wheel; every target contains only product."""
    results = []
    for mode, archive in (('sdist', distributions[0]), ('rebuilt_wheel', distributions[2])):
        directory = work / ('public-' + mode)
        directory.mkdir()
        target = directory / 'runtime'
        commands = []
        def run(args, *, data=None, timeout=120):
            proc = subprocess.run(args, cwd=directory, input=data, capture_output=True, timeout=timeout)
            commands.append({'command': [str(arg) for arg in args], 'exit_code': proc.returncode})
            (directory / ('command-' + str(len(commands)) + '.log')).write_bytes(proc.stdout + proc.stderr)
            assert proc.returncode == 0, proc.stderr.decode(errors='replace')
            return proc
        import sys
        run([sys.executable, '-m', 'venv', '--without-pip', str(target)])
        python = target / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
        if mode == 'sdist':
            # Build with the already selected external toolchain; install only
            # the resulting product into the isolated target's actual purelib.
            purelib = run([str(python), '-I', '-B', '-c',
                'import sysconfig; print(sysconfig.get_path("purelib"))']).stdout.decode().strip()
            run([sys.executable, '-m', 'pip', '--isolated', 'install', '--no-index',
                '--no-deps', '--no-cache-dir', '--no-build-isolation',
                '--target', purelib, str(archive)])
        else:
            run([sys.executable, '-m', 'pip', '--python', str(python), '--isolated', 'install',
                '--no-index', '--no-deps', '--no-cache-dir', str(archive)])
        payload = {'modules': modules, 'public': public_payload()}
        child = public_script() + r'''
import sys,importlib,importlib.metadata,socket,ctypes
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
import source_integrity_toolkit as package
assert set(package.__all__)=={'audit_bundle','audit_file','__version__','AuditReport','AuditAbort','AuditCancelled','AuditUsageError'}
events=[]
def audit(event,args):
    if event=='open' or event.startswith('socket.') or event=='ctypes.dlopen':
        events.append(event);raise RuntimeError('blocked_installed_effect')
sys.addaudithook(audit)
public=_public_witness(payload['public']['source'],payload['public']['expected'])
try:package.audit_file(object(),object(),options=object())
except NotImplementedError:pass
else:raise AssertionError('file_audit_activated')
assert events==[]
for probe in (lambda:open('FICTIONAL_MUST_NOT_OPEN','rb'),lambda:socket.getaddrinfo('fictional.invalid',443),lambda:ctypes.CDLL('FICTIONAL_MUST_NOT_LOAD')):
    try:probe()
    except RuntimeError:pass
assert events==['open','socket.getaddrinfo','ctypes.dlopen']
print(json.dumps({'modules':loaded,'runtime_distributions':['source-integrity-toolkit'],
    'normal_effects':[],'negative_events':events,'public_refusals':1,'public_audit':public}))
'''
        proc = run([str(python), '-I', '-B', '-c', child],
                   data=json.dumps(payload).encode('utf-8'), timeout=120)
        assert proc.stderr == b''
        runtime = json.loads(proc.stdout)
        assert runtime['modules'] == modules
        results.append({'mode': mode, 'source_archive': archive.name,
            'source_archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(),
            'runtime': runtime, 'commands': commands})
    return results
