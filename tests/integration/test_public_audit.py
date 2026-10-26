# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W08 real public memory composition, retaining W07 private regression.

The finite dossier below is independently authored from the bundle contract.
Its empty seed/dimension populations have literal expectations, not snapshots
generated from the new implementation. Exact formatting is checked independently
against its frozen logical document; the larger W02 reference retains its
original independent goldens and its real same-invocation budget outcome.
"""
import copy
from dataclasses import FrozenInstanceError
import importlib.util
import json
from pathlib import Path
import re

import pytest

from source_integrity_toolkit.contracts import report as contract
from source_integrity_toolkit import AuditAbort, audit_bundle
from source_integrity_toolkit.runtime import boundary, resources


ROOT = Path(__file__).resolve().parents[2]
FAMILIES = tuple('SIT-M' + str(number).zfill(3) for number in range(1, 16))
ROOT_MEMBERS = (
    'contract_version', 'report_kind', 'report_id', 'run', 'input_identity',
    'input_validation', 'scopes', 'populations', 'basis_index', 'capabilities',
    'checks', 'observability_domains', 'results', 'findings', 'reasons',
    'release_limits',
)
DIMENSIONAL = {'SIT-M002', 'SIT-M003', 'SIT-M004', 'SIT-M005',
               'SIT-M006', 'SIT-M007', 'SIT-M013'}


def _load(name, relative):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _unknown():
    return {'state': 'unknown', 'value': None, 'precision': None,
            'reason': 'P4-W07 fictional occurrence time is not supplied.'}


def _provenance():
    return {'attributed_to_ref': 'P4-W07-ACTOR', 'basis_kind': 'declaration',
            'evidence_ref_ids': [], 'method': 'Finite W07 supplied declaration.',
            'qualifications': ['Supplied declaration only; no authentication.']}


def _minimal_value():
    """One declared claim, no seeds/dimensions, and no implicit world subjects."""
    return {
        'contract_version': 'sit-bundle/0.1', 'bundle_id': 'P4-W07-BUNDLE',
        'snapshot_id': 'P4-W07-SNAPSHOT', 'recorded_at': _unknown(),
        'predecessor': None,
        'inquiries': [{
            'id': 'P4-W07-I', 'target_claim_refs': ['P4-W07-CLAIM'],
            'target_object_refs': [], 'seed_artifact_refs': [],
            'seed_evidence_refs': [],
            'boundary': {'description': 'Finite W07 declared boundary.',
                         'criterion': 'Only supplied typed bindings.',
                         'system_refs': []},
            'time_window': {'start': _unknown(), 'end': _unknown()},
            'as_of': _unknown(), 'dependency_dimensions': [],
            'coverage_assertion_refs': [], 'provenance': _provenance(),
        }],
        'records': [
            {'id': 'P4-W07-ACTOR', 'kind': 'actor',
             'data': {'actor_kind': 'human', 'identity_disclosure': 'pseudonymous',
                      'display_name': 'W07-PRIVATE-DISPLAY-NOT-EXPORTED'},
             'provenance': _provenance()},
            {'id': 'P4-W07-CLAIM', 'kind': 'claim',
             'data': {'claim_key': 'P4-W07-CLAIM-FAMILY', 'version_label': 'v1',
                      'text': 'Finite W07 fictional claim.',
                      'context': 'Finite W07 supplied context.'},
             'provenance': _provenance()},
        ],
        'assertions': [], 'evidence_references': [],
    }


def _plain(value):
    if type(value) is contract._ReportMapping:
        return {name: _plain(value[name]) for name in value}
    if type(value) is tuple:
        return [_plain(item) for item in value]
    assert value is None or type(value) in (str, bool, int)
    return value


def _compact(value):
    """Independent J scalar spellings on the exposed logical report only."""
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(',', ':'), allow_nan=False)
    short = {'\\b': '\\u0008', '\\f': '\\u000c', '\\n': '\\u000a',
             '\\r': '\\u000d', '\\t': '\\u0009'}

    def replace(match):
        token = match.group()
        if token.startswith('\\'):
            return short.get(token, token)
        return '\\u' + format(ord(token), '04x')

    raw = re.sub(r'\\.|[\u007f-\u009f\u061c\u200e\u200f\u2028-\u202e\u2066-\u2069]',
                 replace, raw)
    return (raw + '\n').encode('utf-8')


def _assert_complete_formats(report):
    assert type(report) is contract.AuditReport
    document = {name: _plain(getattr(report, name)) for name in ROOT_MEMBERS}
    json_raw = report.to_json_bytes()
    markdown_raw = report.to_markdown_bytes()
    assert type(json_raw) is type(markdown_raw) is bytes
    assert json_raw == _compact(document)
    parity = _load('sit_w07_independent_parity', 'tests/contract/test_report_parity.py')
    parity._strict_equal(parity._parse_markdown(markdown_raw, document), document)
    schema = _load('sit_w07_report_schema', 'tests/contract/test_report_contract.py')
    assert schema.schema_accepts(document, schema.report_schema(), schema.report_schema())
    return document


@pytest.fixture(scope='module')
def completed():
    source = _minimal_value()
    before = copy.deepcopy(source)
    owners = []
    factory = boundary._new_analysis_budget

    def observe():
        owner = factory()
        owners.append(owner)
        return owner

    patch = pytest.MonkeyPatch()
    try:
        patch.setattr(boundary, '_new_analysis_budget', observe)
        report = audit_bundle(source)
    finally:
        patch.undo()
    assert source == before
    assert len(owners) == 1
    return report, _assert_complete_formats(report), owners[0]


def test_one_actual_invocation_delivers_both_formats_on_one_unchanged_budget(completed):
    report, document, owner = completed
    assert document['report_kind'] == 'audit_report'
    assert document['run']['processing_state'] == 'completed'
    assert document['input_validation'] == {'state': 'accepted', 'diagnostics': []}
    assert 1024 < owner.used <= 10_000_000
    assert owner.remaining == 10_000_000 - owner.used
    assert owner._json_output_bytes == len(report.to_json_bytes())
    assert owner._markdown_output_bytes == len(report.to_markdown_bytes())
    assert owner._start > 0 and owner._last >= owner._start
    assert owner._last - owner._start <= 60_000_000_000
    assert resources._WORK_LIMIT == 10_000_000
    assert resources._EMERGENCY_RESERVE == 1024
    assert resources._DEADLINE_NS == 60_000_000_000


def test_finite_declared_inputs_have_literal_public_inventory_and_family_facts(completed):
    _, document, _ = completed
    assert document['report_id'] == 'SIT-RPT-000001'
    assert document['run']['requested_diagnostic_ids'] == list(FAMILIES)
    assert document['run']['completed_diagnostic_ids'] == list(FAMILIES)
    assert document['run']['diagnostics'] == []
    assert len(document['capabilities']) == 15
    assert {row['diagnostic_id'] for row in document['capabilities']} == set(FAMILIES)
    assert [row['level_index'] for row in document['observability_domains']] == list(range(5))
    assert all(row['execution_state'] == 'completed' for row in document['results'])
    for field in ('nominal_seed_artifact_record_count', 'seed_evidence_item_count',
                  'claim_artifact_record_count', 'unresolved_seed_artifact_reference_count'):
        rows = [row for row in document['results'] if row['field_key'] == field]
        assert len(rows) == 1
        assert rows[0]['result_state'] == 'available'
        assert type(rows[0]['value']) is int and rows[0]['value'] == 0
    inventory = next(row for row in document['results']
                     if row['field_key'] == 'declared_basis_inventory')
    assert inventory['result_state'] == 'available' and inventory['value']['total'] == 3
    declaration = next(row for row in inventory['value']['categories']
                       if row['label'] == 'declaration')
    assert declaration['count'] == 3
    assert {(ref['collection'], ref['identifier']) for ref in declaration['member_refs']} == {
        ('inquiries', 'P4-W07-I'), ('records', 'P4-W07-ACTOR'),
        ('records', 'P4-W07-CLAIM'),
    }


def test_empty_declared_dimensions_preserve_explicit_nonresults(completed):
    _, document, _ = completed
    reasons = {row['id']: row for row in document['reasons']}
    scopes = {row['id']: row for row in document['scopes']}
    dimensional = [row for row in document['results'] if row['diagnostic_id'] in DIMENSIONAL]
    assert {row['diagnostic_id'] for row in dimensional} == DIMENSIONAL
    for row in dimensional:
        assert row['result_state'] == 'not_applicable' and row['value'] is None
        assert scopes[row['scope_ref']]['dependency_dimension'] is None
        assert row['reason_refs']
        actual = [reasons[identifier] for identifier in row['reason_refs']]
        assert {reason['code'] for reason in actual} == {'dimension_not_selected'}
        assert {reason['classification'] for reason in actual} == {'structural_inapplicability'}
        assert all(row['id'] in reason['affected_result_refs'] for reason in actual)


def test_explicit_dimension_empty_seed_ratios_complete_as_unavailable():
    """Reporting W4-10 and Definitions 22: known N=0 is not a ratio zero."""
    source = _minimal_value()
    source['inquiries'][0]['dependency_dimensions'] = ['acquisition']
    before = copy.deepcopy(source)
    report = audit_bundle(source)
    document = _assert_complete_formats(report)
    assert source == before
    assert document['run']['processing_state'] == 'completed'
    assert document['input_validation']['state'] == 'accepted'
    reasons = {row['id']: row for row in document['reasons']}
    for field in ('single_origin_contribution_hhi', 'documentary_origin_resolution_fraction',
                  'inherited_only_seed_fraction'):
        rows = [row for row in document['results'] if row['field_key'] == field]
        assert len(rows) == 1
        row = rows[0]
        assert row['execution_state'] == 'completed'
        assert row['result_state'] == 'unavailable' and row['value'] is None
        assert row['reason_refs']
        assert 'zero_denominator' in {reasons[identifier]['code'] for identifier in row['reason_refs']}


def test_run_identity_unknown_times_and_disclosure_are_retained(completed):
    report, document, _ = completed
    identity = document['input_identity']
    assert identity['bundle_id'] == 'P4-W07-BUNDLE'
    assert identity['snapshot_id'] == 'P4-W07-SNAPSHOT'
    assert identity['source_mode'] == 'in_process'
    assert identity['raw_file_digest'] is None and identity['qualifications']
    for field in ('started_at', 'finished_at'):
        assert document['run'][field] == {'state': 'unknown', 'value': None,
            'precision': None, 'reason': 'not_recorded_by_SIT-RP-0.1'}
    assert b'W07-PRIVATE-DISPLAY-NOT-EXPORTED' not in report.to_json_bytes()
    assert b'W07-PRIVATE-DISPLAY-NOT-EXPORTED' not in report.to_markdown_bytes()


def test_delivered_report_caches_and_frozen_graph_do_not_reenter_runtime(completed, monkeypatch):
    report, document, owner = completed
    original_used, original_last = owner.used, owner._last
    json_raw, markdown_raw = report.to_json_bytes(), report.to_markdown_bytes()

    def forbidden(*args, **kwargs):
        raise AssertionError('completed report reentered execution')

    monkeypatch.setattr(resources, 'monotonic_ns', forbidden)
    monkeypatch.setattr(boundary, '_new_analysis_budget', forbidden)
    for _ in range(3):
        assert report.to_json_bytes() is json_raw
        assert report.to_markdown_bytes() is markdown_raw
        assert report.report_id == document['report_id']
    assert (owner.used, owner._last) == (original_used, original_last)
    assert set(type(report).__slots__) == {'_document', '_json_bytes', '_markdown_bytes'}
    original_results = report.results
    with pytest.raises((TypeError, FrozenInstanceError)):
        report.results = ()
    assert report.results is original_results
    with pytest.raises(TypeError):
        report.results[0]['value'] = 99
    with pytest.raises(TypeError):
        report.run['requested_diagnostic_ids'][0] = 'altered'
    assert report.to_json_bytes() is json_raw
    assert report.to_markdown_bytes() is markdown_raw
    assert (owner.used, owner._last) == (original_used, original_last)


def test_source_mutation_after_delivery_cannot_change_report_or_encodings():
    source = _minimal_value()
    before = copy.deepcopy(source)
    report = audit_bundle(source)
    assert source == before
    json_raw, markdown_raw = report.to_json_bytes(), report.to_markdown_bytes()
    source['inquiries'][0]['target_claim_refs'].clear()
    source['records'][1]['data']['text'] = 'MUTATED-AFTER-DELIVERY'
    source.clear()
    assert report.input_identity['bundle_id'] == 'P4-W07-BUNDLE'
    assert report.to_json_bytes() is json_raw
    assert report.to_markdown_bytes() is markdown_raw
    assert b'MUTATED-AFTER-DELIVERY' not in json_raw + markdown_raw


@pytest.mark.parametrize('mode', ('value', 'utf8'))
def test_existing_private_entry_preserves_real_analysis_without_public_delivery(mode):
    source = _minimal_value()
    before = copy.deepcopy(source)
    argument = source if mode == 'value' else json.dumps(source).encode('utf-8')
    out = boundary._analyze_value(argument) if mode == 'value' else boundary._analyze_utf8(argument)
    assert type(out) is contract._AnalyticalOutcome
    assert out.execution_state == 'completed' and out.input_state == 'accepted'
    assert not hasattr(out, 'to_json_bytes') and not hasattr(out, 'report_kind')
    assert len(out.capabilities) == 15 and len(out.domains) == 5
    assert source == before
    for field in ('nominal_seed_artifact_record_count', 'seed_evidence_item_count'):
        row = next(row for row in out.results if row.ref.field_key == field)
        assert row.result_state == 'available' and row.value.value == 0


@pytest.mark.parametrize('mutation,code', (
    ('missing', 'missing_required_field'),
    ('contract', 'unsupported_input_contract'),
    ('duplicate', 'duplicate_identifier'),
    ('dangling', 'dangling_reference'),
))
def test_structural_rejection_delivers_complete_safe_diagnostic_formats(mutation, code):
    source = _minimal_value()
    if mutation == 'missing':
        del source['snapshot_id']
    elif mutation == 'contract':
        source['contract_version'] = 'unsupported-private-contract-canary'
    elif mutation == 'duplicate':
        source['records'].append(copy.deepcopy(source['records'][1]))
    else:
        source['inquiries'][0]['target_claim_refs'] = ['PRIVATE-MISSING-CLAIM']
    before = copy.deepcopy(source)
    report = audit_bundle(source)
    document = _assert_complete_formats(report)
    assert source == before
    assert document['report_kind'] == 'validation_diagnostics'
    assert document['run']['processing_state'] == 'rejected'
    assert document['input_validation']['state'] == 'rejected'
    assert [row['code'] for row in document['input_validation']['diagnostics']] == [code]
    assert {row['code'] for row in document['reasons']} == {'input_not_accepted'}
    for name in ('scopes', 'populations', 'basis_index', 'capabilities', 'checks',
                 'observability_domains', 'results', 'findings'):
        assert document[name] == []
    assert document['input_identity']['bundle_id'] is None
    assert document['input_identity']['snapshot_id'] is None
    for canary in (b'PRIVATE-MISSING-CLAIM', b'unsupported-private-contract-canary',
                   b'W07-PRIVATE-DISPLAY-NOT-EXPORTED'):
        assert canary not in report.to_json_bytes() + report.to_markdown_bytes()


def test_full_reference_is_subject_to_the_actual_whole_invocation_limit(monkeypatch):
    """W02 component completion does not authorize another report allowance."""
    cases = json.loads((ROOT / 'tests/fixtures/micro/phase4_public_cases.json').read_bytes())
    assert cases['cases'][0]['id'] == 'P4-REFERENCE-ONE-ORIGIN'
    source = cases['cases'][0]['dossier']
    before = copy.deepcopy(source)
    owners = []
    factory = boundary._new_analysis_budget

    def observe():
        owner = factory()
        owners.append(owner)
        return owner

    monkeypatch.setattr(boundary, '_new_analysis_budget', observe)
    try:
        report = audit_bundle(source)
    except AuditAbort as stopped:
        assert stopped.processing_state == 'interrupted'
        assert stopped.input_validation_state == 'accepted'
        assert stopped.reason_code == 'resource_limit_reached'
        assert stopped.publication_state == 'not_published'
        assert len(owners) == 1 and owners[0]._cause.limit_id == 'WU9-L11'
        assert owners[0]._stop_kind == 'global' and owners[0]._emergency_taken
    else:
        # If a future scoped integration eliminates redundant work legitimately,
        # success must still satisfy both unchanged independent complete goldens.
        assert report.to_json_bytes() == (ROOT / 'tests/golden/phase4_reference_report.json').read_bytes()
        assert report.to_markdown_bytes() == (ROOT / 'tests/golden/phase4_reference_report.md').read_bytes()
        _assert_complete_formats(report)
    assert len(owners) == 1 and 1024 < owners[0].used <= 10_000_000
    assert source == before
