# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W04 source-level privacy controls for the real selected-report seam.

These finite dossiers and literal semantic expectations precede the selector.
Every canary check starts from a completed private analysis and a complete
logical report. No public audit, renderer, whole-invocation resource ledger or
anonymity/publication certification is claimed by this component exercise.
"""
import copy
import importlib.util
import json
from pathlib import Path

import pytest

from source_integrity_toolkit.contracts import report as contract
from source_integrity_toolkit.runtime import disclosure
from source_integrity_toolkit.runtime.boundary import _analyze_value


ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    'p4_w04_disclosure_test_helpers', ROOT / 'tests/contract/test_report_assembly.py')
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)
CASES = {case['id']: case for case in json.loads(
    (ROOT / 'tests/fixtures/adversarial/phase4_report_cases.json').read_bytes())['cases']}


def _build(identifier):
    case = copy.deepcopy(CASES[identifier])
    source = case['dossier']
    before = copy.deepcopy(source)
    outcome = _analyze_value(source)
    assert type(outcome) is contract._AnalyticalOutcome
    assert outcome.execution_state == 'completed'
    port = h.RecordingPort()
    frozen = disclosure._assemble_selected_report(outcome, port)
    assert type(frozen) is contract._ReportMapping
    document = h._plain(frozen)
    assert set(document) == set(h.ROOT_FIELDS)
    assert document['report_kind'] == 'audit_report'
    assert document['input_validation']['state'] == 'accepted'
    assert document['run']['processing_state'] == 'completed'
    assert len(document['results']) == len(outcome.results)
    assert len(document['capabilities']) == 15
    assert len(document['observability_domains']) == 5
    assert 0 < port.units <= 10_000_000 and port.checks > 0
    assert source == before
    return case, document


@pytest.fixture(scope='module')
def selected_report():
    return _build('P4-W04-EXPLICIT-SELECTION')


@pytest.fixture(scope='module')
def correction_report():
    return _build('P4-W04-NATIVE-CORRECTION')


@pytest.fixture(scope='module')
def protected_report():
    return _build('P4-W04-PROTECTED-COMMON')


@pytest.fixture(scope='module')
def unknown_report():
    return _build('P4-W04-UNKNOWN-FRONTIER')


def _objects(value):
    """Read only the plain report value, never a private/source representation."""
    if type(value) is dict:
        yield value
        for child in value.values():
            yield from _objects(child)
    elif type(value) is list:
        for child in value:
            yield from _objects(child)


def _strings(value):
    if type(value) is str:
        yield value
    elif type(value) is dict:
        for key, child in value.items():
            yield key
            yield from _strings(child)
    elif type(value) is list:
        for child in value:
            yield from _strings(child)


def _contains(value, canary):
    # Compare admitted string values directly. Test-side JSON quoting must not
    # hide a backslash-bearing source locator or manufacture a false baseline.
    return any(canary in item for item in _strings(value))


def _native(document, identifier):
    rows = [obj['native_record'] for obj in _objects(document)
            if 'native_record' in obj and obj['native_record'].get('id') == identifier]
    assert rows, identifier + ': expected selected native source has no public home'
    assert all(row == rows[0] for row in rows)
    return rows[0]


def _basis(document, collection, identifier):
    rows = [row for row in document['basis_index']
            if row['source'] == {'collection': collection, 'identifier': identifier,
                                 'selector': None}]
    assert len(rows) == 1
    return rows[0]


def _result(document, field_key):
    rows = [row for row in document['results'] if row['field_key'] == field_key]
    assert len(rows) == 1, field_key
    return rows[0]


def _record(source, identifier):
    return next(row for collection in ('records', 'assertions', 'evidence_references', 'inquiries')
                for row in source[collection] if row['id'] == identifier)


@pytest.mark.parametrize('canary', CASES['P4-W04-EXPLICIT-SELECTION']['expected']['excluded_values'])
def test_excluded_source_values_are_absent_from_complete_report(selected_report, canary):
    case, document = selected_report
    assert len(document['results']) == case['expected']['private_result_count']
    assert _contains(case['dossier'], canary)
    assert not _contains(document, canary)


def test_selected_fragments_do_not_export_full_source_containers(selected_report):
    case, document = selected_report
    forbidden = {'extensions', 'excerpt', 'contact_locator', 'display_name',
                 'identity_key', 'locator', 'locators', 'citation_locator',
                 'external_locator', 'protected_key', 'checksums', 'work_key'}
    assert not any(forbidden.intersection(obj) for obj in _objects(document))
    # These real source objects contain excluded fields; their selected native
    # homes still have concrete useful content and are not wholesale copies.
    for identifier in ('P4-ACTOR', 'P4-ART', 'P4-CLAIM', 'P4-BOUND', 'P4-I001'):
        selected = _native(document, identifier)
        original = _record(case['dossier'], identifier)
        assert selected['id'] == original['id'] and selected != original
        assert selected['provenance'] == original['provenance']
    assert _native(document, 'P4-ACTOR')['data'] == {
        'actor_kind': 'human', 'identity_disclosure': 'pseudonymous'}


def test_required_context_method_and_ordered_qualifications_remain(selected_report):
    case, document = selected_report
    required = case['expected']['required']
    assert _native(document, 'P4-CLAIM')['data'] == {
        'claim_key': 'P4-CLAIM-FAMILY', 'version_label': 'v1',
        'context': required['context']}
    selected = _native(document, 'P4-BOUND')
    assert selected['provenance']['method'] == required['method']
    assert selected['provenance']['qualifications'] == [
        required['qualification_a'], required['qualification_b'], required['qualification_a']]
    original = _record(case['dossier'], 'P4-BOUND')
    assert selected['scope'] == original['scope']
    assert selected['data'] == original['data']
    assert selected['asserted_at'] == original['asserted_at']
    assert selected['lifecycle_state'] == original['lifecycle_state']


def test_required_basis_attribution_support_availability_and_limits_remain(selected_report):
    case, document = selected_report
    source = _record(case['dossier'], 'P4-BOUND')
    basis = _basis(document, 'assertions', 'P4-BOUND')
    assert basis['basis_kind'] == 'documented_record'
    assert basis['asserter_ref'] == {'collection': 'records', 'identifier': 'P4-ACTOR', 'selector': None}
    assert basis['method'] == source['provenance']['method']
    assert basis['qualifications'] == source['provenance']['qualifications']
    assert basis['support_refs'] == [
        {'collection': 'evidence_references', 'identifier': 'P4-SUPPORT', 'selector': None}]
    assert basis['scope']['inquiry_refs'] == [
        {'collection': 'inquiries', 'identifier': 'P4-I001', 'selector': None}]
    assert basis['scope']['claim_refs'] == [
        {'collection': 'records', 'identifier': 'P4-CLAIM', 'selector': None}]
    assert basis['scope']['effective_window'] == source['scope']['effective_window']
    assert basis['time'] == {'asserted_at': source['asserted_at']}
    assert basis['lifecycle'] == {'state': 'active', 'basis_refs': []}
    assert basis['check_refs']
    checks = {check['id']: check for check in document['checks']}
    assert all(checks[ref]['check_id'] in ('PC05', 'PC06', 'PC07', 'PC08', 'PC09', 'PC10')
               for ref in basis['check_refs'])
    support = _basis(document, 'evidence_references', 'P4-SUPPORT')
    assert support['availability'] == 'supplied'
    assert support['qualifications'] == [case['expected']['required']['scope_note']]


def test_source_extensions_cannot_grant_publication_or_replace_tool_limits(selected_report):
    unused, document = selected_report
    reference = h._reference_document()
    assert document['release_limits'] == reference['release_limits']
    assert document['run']['qualifications'] == reference['run']['qualifications']
    assert document['run']['tool_name'] == 'Source Integrity Toolkit'
    assert not _contains(document, 'P4-W04-PRIVATE-PUBLICATION-APPROVAL')


@pytest.mark.parametrize('state', ('accepted', 'failed', 'unknown'))
def test_native_correction_outcomes_keep_attribution_and_do_not_set_run_state(correction_report, state):
    case, document = correction_report
    identifier = 'P4-W04-HANDLING-' + state.upper()
    native = _native(document, identifier)
    original = _record(case['dossier'], identifier)
    assert native['data']['details'] == {
        'outcome': state,
        'reason': 'P4-W04-REQUIRED-NATIVE-' + state.upper() + ': attributed process state only.'}
    assert native['provenance'] == original['provenance']
    assert native['data']['case_ref'] == 'P4-W04-CASE'
    assert native['data']['target_refs'] == ['P4-CLAIM']
    result = _result(document, 'correction_case_disclosures')
    assert result['result_origin'] == 'attributed_record'
    assert result['result_state'] == 'available'
    assert document['run']['processing_state'] == 'completed'


def test_handling_outcomes_do_not_invent_successful_linked_change(correction_report):
    case, document = correction_report
    for field, expected in (
            ('correction_case_record_count', case['expected']['case_count']),
            ('handling_event_record_count', case['expected']['handling_count']),
            ('linked_change_event_record_count', case['expected']['linked_change_count'])):
        row = _result(document, field)
        assert row['result_state'] == 'available' and row['value'] == expected
    assert _native(document, 'P4-W04-CASE')['data']['details']['summary'] == (
        'P4-W04-REQUIRED-SUBMISSION: review this exact fictional Claim.')
    # Correction owner source slots include the submission's deliberately null
    # case_ref. A root reference to the same record cannot replace that slot.
    assert _native(document, 'P4-W04-CASE')['data']['case_ref'] is None
    expected_sources = [
        {'collection': 'inquiries', 'identifier': 'P4-I001', 'selector': None},
        {'collection': 'records', 'identifier': 'P4-W04-CASE', 'selector': 'data.target_refs'},
        *({'collection': 'records', 'identifier': identifier, 'selector': 'data.case_ref'}
          for identifier in ('P4-W04-CASE', 'P4-W04-HANDLING-ACCEPTED',
                             'P4-W04-HANDLING-FAILED', 'P4-W04-HANDLING-UNKNOWN')),
    ]
    conditions = {'case_handling_disclosure', 'downstream_change_undocumented'}
    findings = [finding for finding in document['findings']
                if finding['condition_code'] in conditions]
    assert {finding['condition_code'] for finding in findings} == conditions
    for finding in findings:
        components = [part for part in finding['witness']['components']
                      if part['type'] == 'correction_outcome_witness']
        assert len(components) == 1
        assert components[0]['source_refs'] == expected_sources
        assert components[0]['member_count'] == (
            len(components[0]['members']) + len(expected_sources))


def test_correction_contact_and_private_identity_are_excluded_without_losing_route(correction_report):
    case, document = correction_report
    for canary in case['expected']['excluded_values']:
        assert _contains(case['dossier'], canary) and not _contains(document, canary)
    channel = _native(document, 'P4-W04-CHANNEL')
    assert channel['data']['owner_refs'] == ['P4-ACTOR']
    assert channel['data']['target_refs'] == ['P4-CLAIM']
    assert channel['data']['declared_action_types'] == ['amend']
    assert 'contact_locator' not in channel['data']


def test_two_protected_seed_paths_preserve_one_common_origin(protected_report):
    case, document = protected_report
    expected = case['expected']
    for field in ('reached_origin_record_count', 'documentary_origin_boundary_record_count',
                  'unresolved_frontier_reference_count'):
        row = _result(document, field)
        assert row['result_state'] == 'available' and row['value'] == expected[field]
    assert _result(document, 'documentary_origin_resolution_fraction')['value'] == expected['resolution']
    assert _result(document, 'single_origin_contribution_hhi')['value'] == expected['hhi']
    for field in ('per_seed_origin_memberships', 'origin_incidence_counts'):
        incidence = _result(document, field)['value']
        assert [row['member_ref']['identifier'] for row in incidence['memberships']] == expected['seed_ids']
        assert all([ref['identifier'] for ref in row['origin_refs']] == [expected['origin_id']]
                   for row in incidence['memberships'])
        assert len(incidence['origin_counts']) == 1
        assert incidence['origin_counts'][0]['count'] == 2
        assert incidence['origin_counts'][0]['origin_ref']['identifier'] == expected['origin_id']


def test_protected_attestation_keeps_visible_support_and_specific_limits(protected_report):
    case, document = protected_report
    native = _native(document, 'P4-ACTOR')
    assert native['data']['identity_disclosure'] == 'protected'
    assert 'identity_key' not in native['data'] and 'display_name' not in native['data']
    boundary = _basis(document, 'assertions', 'P4-BOUND')
    original = _record(case['dossier'], 'P4-BOUND')
    assert boundary['basis_kind'] == 'protected_attestation'
    assert boundary['qualifications'] == original['provenance']['qualifications']
    support = _basis(document, 'evidence_references', 'P4-SUPPORT')
    assert support['availability'] == 'supplied'
    assert support['attestor_ref'] == {'collection': 'records', 'identifier': 'P4-ACTOR', 'selector': None}
    assert support['qualifications'] == [_record(case['dossier'], 'P4-SUPPORT')['scope_note']]
    for canary in case['expected']['excluded_values']:
        assert _contains(case['dossier'], canary) and not _contains(document, canary)


def test_withheld_frontier_does_not_become_an_independent_or_unrelated_origin(unknown_report):
    case, document = unknown_report
    expected = case['expected']
    for field in ('reached_origin_record_count', 'documentary_origin_boundary_record_count',
                  'unresolved_frontier_reference_count', 'seed_items_with_unresolved_ancestry_count'):
        row = _result(document, field)
        assert row['result_state'] == 'available' and row['value'] == expected[field]
    assert _result(document, 'documentary_origin_resolution_fraction')['value'] == expected['resolution']
    hhi = _result(document, 'single_origin_contribution_hhi')
    assert hhi['result_state'] == expected['hhi_state'] and hhi['value'] is None
    memberships = _result(document, 'per_seed_origin_memberships')['value']['memberships']
    assert [row['member_ref']['identifier'] for row in memberships] == expected['seed_ids']
    assert all(row['origin_refs'] == [] for row in memberships)
    assert set(expected['reason_codes']) <= {reason['code'] for reason in document['reasons']}
    frontiers = [obj for obj in _objects(document)
                 if obj.get('id') == expected['frontier_id'] and obj.get('kind') == 'unresolved_reference']
    assert frontiers
    for frontier in frontiers:
        assert frontier['data']['expected_kinds'] == ['origin_event']
        assert frontier['data']['reason'] == 'withheld'
        assert 'protected_key' not in frontier['data']
    for canary in expected['excluded_values']:
        assert _contains(case['dossier'], canary) and not _contains(document, canary)
