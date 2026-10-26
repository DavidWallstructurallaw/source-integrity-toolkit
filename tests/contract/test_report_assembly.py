# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W03 assembly and W04 disclosure integration with an independent reference.

The selected bodies below are a trusted, case-specific test fixture for the
W03 assembly controls. They are read from W02's independent expectations,
never from assembler output. Separate W04 controls use the actual runtime
selector and assembler under one supplied finite component port. Neither
path claims public audit delivery, whole-invocation integration or rendering.
"""
import copy
from dataclasses import replace
import json
from pathlib import Path

import pytest

from source_integrity_toolkit.contracts import report as contract
from source_integrity_toolkit.contracts import results as values
from source_integrity_toolkit.contracts.execution import (
    _AnalysisAborted, _PreparationAborted, _PreparationStop,
)
from source_integrity_toolkit.contracts.results import (
    _BasisRef, _InputRef, _RecordDisclosures,
)
from source_integrity_toolkit.reporting import assemble
from source_integrity_toolkit.runtime import disclosure as disclosure_runtime
from source_integrity_toolkit.runtime.boundary import _analyze_value


ROOT = Path(__file__).resolve().parents[2]
ROOT_FIELDS = (
    'contract_version', 'report_kind', 'report_id', 'run', 'input_identity',
    'input_validation', 'scopes', 'populations', 'basis_index', 'capabilities',
    'checks', 'observability_domains', 'results', 'findings', 'reasons',
    'release_limits',
)
COLLECTIONS = ('scopes', 'populations', 'basis_index', 'capabilities', 'checks',
               'results', 'findings', 'reasons')
FAMILIES = tuple('SIT-M' + str(index).zfill(3) for index in range(1, 16))
DOMAIN_LABELS = (
    'Artifact and contribution inventory',
    'Declared provenance and process metadata',
    'Origin-resolution and scoped process-assessment evidence',
    'Evaluator, correction-route and authority evidence',
    'Boundary-qualified external input, stage histories and documented correction outcomes',
)


class RecordingPort:
    """Finite test-owned internal port; no public API accepts this object."""
    def __init__(self, stop_after=10_000_000):
        assert type(stop_after) is int and 0 <= stop_after <= 10_000_000
        self.units = 0
        self.checks = 0
        self.stop_after = stop_after

    def charge(self, units):
        assert type(units) is int and units >= 0
        if self.units + units > self.stop_after:
            raise RuntimeError('controlled_assembly_stop')
        self.units += units

    def check(self):
        self.checks += 1


def _reference_document():
    return json.loads((ROOT / 'tests/golden/phase4_reference_report.json').read_bytes())


def _reference_dossier():
    fixture = json.loads((ROOT / 'tests/fixtures/micro/phase4_public_cases.json').read_bytes())
    assert fixture['cases'][0]['id'] == 'P4-REFERENCE-ONE-ORIGIN'
    return fixture['cases'][0]['dossier']


def _reference_outcome():
    outcome = _analyze_value(_reference_dossier())
    assert type(outcome) is contract._AnalyticalOutcome
    assert outcome.execution_state == 'completed'
    assert len(outcome.plan.jobs) == 22 and len(outcome.results) == 78
    return outcome


def _plain(value):
    """Test-only readout of the explicit frozen JSON contract, not private data."""
    if type(value) is contract._ReportMapping:
        return {name: _plain(value[name]) for name in value}
    if type(value) is tuple:
        return [_plain(item) for item in value]
    assert value is None or type(value) in (str, bool, int)
    return value


def _source(ref):
    assert type(ref) is _InputRef
    return {'collection': ref.collection, 'identifier': ref.identifier,
            'selector': ref.selector}


def _source_key(value):
    return value['collection'], value['identifier'], value['selector']


def _strict_equal(actual, expected, path='$'):
    assert type(actual) is type(expected), path + ': type'
    if type(expected) is dict:
        assert actual.keys() == expected.keys(), path + ': keys'
        for key in expected:
            _strict_equal(actual[key], expected[key], path + '.' + key)
    elif type(expected) is list:
        assert len(actual) == len(expected), path + ': length'
        for index, item in enumerate(expected):
            _strict_equal(actual[index], item, path + '[' + str(index) + ']')
    else:
        assert actual == expected, path + ': value'


def _unique_expected(values):
    """Require all matching independent expected bodies to be identical."""
    assert values, 'named reference fixture has no matching selected body'
    for other in values[1:]:
        _strict_equal(other, values[0])
    return copy.deepcopy(values[0])


def _basis_owners(outcome):
    """Enumerate only explicit owner links, never recursively dump a record."""
    owners = []
    for result in outcome.results:
        owners.extend(result.basis_refs)
        for population in result.population_refs:
            owners.extend(population.basis_refs)
    for finding in outcome.findings:
        owners.extend(finding.basis_refs)
        for population in finding.population_refs:
            owners.extend(population.basis_refs)
    distinct = {}
    for owner in owners:
        assert type(owner) is _BasisRef
        distinct.setdefault(_source_key(_source(owner.source)), owner)
    return tuple(distinct.values())


def _selected_basis_entries(outcome, expected):
    by_source = {_source_key(row['source']): row for document in expected
                 for row in document['basis_index']}
    selected = []
    for owner in _basis_owners(outcome):
        source = _source(owner.source)
        row = copy.deepcopy(by_source[_source_key(source)])
        del row['id']
        del row['source']
        # The fixture gives the assembler actual prerequisite objects, not
        # preassigned report IDs. OBS16.6: qualification checks for this basis.
        checks = []
        for result in outcome.results:
            if not any(_source(b.source) == source for b in result.basis_refs):
                continue
            for check in result.check_refs:
                if check.check_id not in ('PC05', 'PC06', 'PC07', 'PC08', 'PC09', 'PC10'):
                    continue
                if any(ref.collection == source['collection'] and
                       ref.identifier == source['identifier'] for ref in check.input_refs):
                    checks.append(check)
        row['check_refs'] = tuple(checks)
        selected.append((owner, row))
    return tuple(selected)


def _selected_result_disclosures(outcome, expected):
    selected = []
    for result in outcome.results:
        if type(result.value) is not _RecordDisclosures:
            continue
        candidates = []
        for document in expected:
            scopes = {row['id']: row for row in document['scopes']}
            candidates.extend(row for row in document['results']
                if row['field_key'] == result.ref.field_key and row['value'] is not None and
                scopes[row['scope_ref']]['inquiry_ref'] == _source(result.ref.scope.inquiry_ref))
        body = _unique_expected([row['value'] for row in candidates])
        selected.append((result.ref, body))
    return tuple(selected)


def _selected_existing_findings(outcome, expected):
    selected = []
    for owner in outcome.findings:
        candidates = [row['witness'] for document in expected for row in document['findings']
                      if row['condition_code'] == owner.condition_code and
                      row['observation_kind'] == owner.observation_kind and
                      row['statement'] == owner.statement and
                      row['interpretation_limit'] == owner.interpretation_limit and
                      row['witness']['input_refs'] == sorted(
                          [_source(ref) for ref in owner.witness.input_refs],
                          key=lambda ref: (ref['collection'], ref['identifier'], ref['selector'] or ''))]
        # The ordinary graph Finding is the existing path. The two retained
        # owner traces have their separately selected complete_trace bodies.
        if owner.condition_code == 'transformation_path_witness':
            candidates = [body for body in candidates if
                          all(component.get('kind') != 'complete_trace'
                              for component in body['components'])]
        selected.append((owner, _unique_expected(candidates)))
    return tuple(selected)


def _selected_owner_witnesses(outcome, expected):
    selected = []
    for owner in outcome.witnesses:
        graph = [payload for payload in owner.payload if payload[0] == 'graph_witness']
        if not graph:
            continue
        assert len(graph) == 1
        payload = graph[0]
        documents = [document for document in expected
                     if any(row['inquiry_ref']['identifier'] == payload[2]
                            for row in document['scopes'])]
        components = [component for document in documents for finding in document['findings']
                      for component in finding['witness']['components']
                      if component['type'] == 'graph_witness' and
                      component['kind'] == payload[1] and
                      component['member_count'] == owner.member_count]
        component = _unique_expected(components)
        # This selects the already authored payload only. Finding metadata,
        # scope, membership and result links must be supplied by the assembler.
        input_refs = _unique_expected([finding['witness']['input_refs']
                      for document in documents for finding in document['findings']
                      if component in finding['witness']['components']])
        selected.append((owner, {'input_refs': input_refs, 'components': [component]}))
    return tuple(selected)


def _selection_parts(outcome, reference=None):
    expected = _reference_document() if reference is None else reference
    if type(expected) is not tuple:
        expected = (expected,)
    return (_selected_basis_entries(outcome, expected),
            _selected_result_disclosures(outcome, expected),
            _selected_existing_findings(outcome, expected),
            _selected_owner_witnesses(outcome, expected))


def _selected_disclosure(outcome, reference=None):
    basis, disclosures, findings, witnesses = _selection_parts(outcome, reference)
    return contract._capture_report_disclosure(basis, disclosures, findings,
                RecordingPort(), owner_witnesses=witnesses)


def _assemble(outcome, disclosure=None, port=None):
    if disclosure is None:
        disclosure = _selected_disclosure(outcome)
    return assemble._assemble_report(outcome, disclosure,
                                    RecordingPort() if port is None else port)


@pytest.fixture(scope='module')
def reference_outcome():
    return _reference_outcome()


@pytest.fixture(scope='module')
def reference_assembly(reference_outcome):
    selected = _selected_disclosure(reference_outcome)
    port = RecordingPort()
    frozen = _assemble(reference_outcome, selected, port)
    assert port.units > 0 and port.checks > 0
    return frozen, _plain(frozen), selected, port.units


@pytest.fixture(scope='module')
def runtime_reference_assembly(reference_outcome):
    """Actual W04 selection and W03 assembly, with no expected bodies as input."""
    port = RecordingPort()
    frozen = disclosure_runtime._assemble_selected_report(reference_outcome, port)
    assert port.units > 0 and port.checks > 0
    return frozen, _plain(frozen), port.units


def _assert_partitions(document):
    results = {row['id']: row for row in document['results']}
    for capability in document['capabilities']:
        selected = [results[identifier] for identifier in capability['result_refs']]
        assert all(row['diagnostic_id'] == capability['diagnostic_id'] for row in selected)
        merged = []
        for state in ('available', 'unavailable', 'not_applicable', 'not_evaluated'):
            actual = capability[state + '_result_refs']
            assert actual == [row['id'] for row in selected if row['result_state'] == state]
            merged.extend(actual)
        assert len(merged) == len(set(merged)) == len(selected)
        assert set(merged) == set(capability['result_refs'])


def _assert_report_links(document):
    """Independent target-kind checks; the test does not call product closure."""
    kinds = {name: {row['id'] for row in document[name]} for name in COLLECTIONS}
    all_ids = [identifier for values in kinds.values() for identifier in values]
    assert len(all_ids) == len(set(all_ids))
    targets = {'scope_ref': 'scopes', 'scope_refs': 'scopes',
               'population_ref': 'populations', 'population_refs': 'populations',
               'basis_refs': 'basis_index', 'check_refs': 'checks',
               'result_refs': 'results', 'available_result_refs': 'results',
               'unavailable_result_refs': 'results', 'not_applicable_result_refs': 'results',
               'not_evaluated_result_refs': 'results', 'affected_result_refs': 'results',
               'witness_refs': 'findings', 'reason_refs': 'reasons'}

    def visit(value):
        if type(value) is dict:
            for key, child in value.items():
                if key in targets:
                    refs = child if type(child) is list else [child]
                    # Input lifecycle basis_refs remain explicitly typed input
                    # references; they are not report basis identifiers.
                    for ref in refs:
                        if type(ref) is str:
                            assert ref in kinds[targets[key]], (key, ref)
                visit(child)
        elif type(value) is list:
            for child in value:
                visit(child)
    visit(document)


def test_real_private_reference_assembles_exact_independent_logical_document(reference_assembly):
    frozen, actual, _, units = reference_assembly
    _assert_complete_reference(frozen, actual, units)


def _assert_complete_reference(frozen, actual, units):
    _strict_equal(actual, _reference_document())
    assert type(frozen) is contract._ReportMapping
    assert set(actual) == set(ROOT_FIELDS)
    assert 0 < units <= 10_000_000
    assert {name: len(actual[name]) for name in COLLECTIONS} == {
        'scopes': 23, 'populations': 40, 'basis_index': 16, 'capabilities': 15,
        'checks': 671, 'results': 78, 'findings': 22, 'reasons': 38,
    }
    assert len({row['field_key'] for row in actual['results']}) == 57


def test_runtime_disclosure_assembles_exact_independent_reference(runtime_reference_assembly):
    frozen, actual, units = runtime_reference_assembly
    _assert_complete_reference(frozen, actual, units)
    _assert_partitions(actual)
    _assert_report_links(actual)


@pytest.mark.parametrize('allowance', (0, 1024))
def test_runtime_disclosure_and_assembly_obey_supplied_port(reference_outcome,
                                                          runtime_reference_assembly,
                                                          allowance):
    # The same real outcome first completed through the conforming runtime
    # path above. A finite stop must propagate instead of allocating a fresh
    # report port or returning a partially selected document.
    port = RecordingPort(stop_after=allowance)
    with pytest.raises(RuntimeError, match='^controlled_assembly_stop$'):
        disclosure_runtime._assemble_selected_report(reference_outcome, port)
    assert port.units <= allowance


def test_reference_partitions_and_target_kinds_are_independently_closed(reference_assembly):
    _, actual, _, _ = reference_assembly
    _assert_partitions(actual)
    _assert_report_links(actual)
    assert [row['diagnostic_id'] for row in actual['capabilities']] == list(FAMILIES)
    assert actual['run']['requested_diagnostic_ids'] == list(FAMILIES)
    assert actual['run']['completed_diagnostic_ids'] == list(FAMILIES)
    assert [(row['level_index'], row['label']) for row in actual['observability_domains']] == list(enumerate(DOMAIN_LABELS))
    assert all('not_applicable_result_refs' not in row for row in actual['observability_domains'])


def test_owner_only_trace_and_human_review_scan_material_are_preserved(reference_assembly):
    _, actual, _, _ = reference_assembly
    results = {row['field_key']: row for row in actual['results']}
    findings = {row['id']: row for row in actual['findings']}
    for field, expected_count in (('single_origin_contribution_hhi', 6),
                                  ('inherited_only_seed_fraction', 5)):
        row = results[field]
        assert len(row['witness_refs']) == 1
        witness = findings[row['witness_refs'][0]]
        assert witness['scope_ref'] == row['scope_ref']
        assert witness['condition_code'] == 'transformation_path_witness'
        assert [component['kind'] for component in witness['witness']['components']] == ['path', 'complete_trace']
        trace = witness['witness']['components'][1]
        assert trace['member_count'] == expected_count
        assert len(trace['observations']) == 1
        assert trace['observations'][0]['source_ref']['identifier'] == 'P4-PARENT'
    scan = results['corrective_independence_disclosures']['value']['records']
    assert len(scan) == 1
    assert scan[0]['source'] == {'collection': 'inquiries', 'identifier': 'P4-I001',
                                 'selector': 'target_object_refs'}
    assert scan[0]['fields']['native_record']['target_object_refs'] == []
    assert scan[0]['qualifications'] == [
        'Actual owner selection/source reference slot; this record does not establish an applicable review or independent process.']


def test_selected_fixture_preserves_required_content_without_private_source_tree(reference_assembly):
    frozen, actual, _, _ = reference_assembly
    dumped = json.dumps(actual, ensure_ascii=False)
    assert 'P4-PRIVATE-DISPLAY-NOT-EXPORTED' not in dumped
    assert 'P4-PRIVATE-EXCERPT-NOT-EXPORTED' not in dumped
    assert 'Inspect supplied acquisition record; literal ``` is data.' in dumped
    assert 'Caller-supplied documentary premise (合成例); no external authentication.' in dumped
    assert 'operation_anchor' not in dumped
    assert 'native_records' not in dumped
    assert 'private_analytical_outcome' not in dumped
    with pytest.raises(TypeError):
        frozen['results'] = ()
    with pytest.raises(TypeError):
        frozen['results'][0]['value'] = 8
    with pytest.raises(TypeError):
        contract.AuditReport()


def _renamed(value, identifiers):
    """Explicit fixture alpha-renaming; prose/order/numeric values stay intact."""
    if type(value) is str:
        return identifiers.get(value, value)
    if type(value) is dict:
        return {key: _renamed(item, identifiers) for key, item in value.items()}
    if type(value) is list:
        return [_renamed(item, identifiers) for item in value]
    return value


def _two_full_reference_inquiry_case():
    """Preserve the larger probe that reached the unchanged 10M work limit."""
    first = _reference_dossier()
    identifiers = {row['id']: row['id'].replace('P4-', 'P4B-', 1)
                   for name in ('inquiries', 'records', 'assertions', 'evidence_references')
                   for row in first[name]}
    second = _renamed(first, identifiers)
    for name in ('inquiries', 'records', 'assertions', 'evidence_references'):
        first[name].extend(second[name])
    return first, (_reference_document(), _renamed(_reference_document(), identifiers))


# The complete double reference reached the unchanged 10M work limit.
# This separately named legal inventory case still covers all fifteen families
# for each Inquiry, and does not claim successful double-origin analysis.
def _two_compact_inquiry_case():
    first = _reference_dossier()
    inquiry = first['inquiries'][0]
    inquiry['dependency_dimensions'] = []
    inquiry['coverage_assertion_refs'] = []
    inquiry['seed_evidence_refs'] = []
    first['assertions'] = []
    first['evidence_references'] = []
    first['records'] = [row for row in first['records']
                        if row['id'] in ('P4-ACTOR', 'P4-ART', 'P4-CLAIM')]
    first['bundle_id'] = 'P4-BUNDLE-COMPACT-TWO'
    first['snapshot_id'] = 'P4-SNAPSHOT-COMPACT-TWO-01'

    # Amend only explicit disclosure-input fixture material. No expected report
    # or expected local ID is generated from the product's output.
    reference = _reference_document()
    for result in reference['results']:
        if result['field_key'] == 'coverage_disclosures':
            result['value'] = {'records': []}
        elif result['field_key'] == 'documentary_basis_gap_disclosures':
            selected = next(row for row in result['value']['records']
                            if row['source']['identifier'] == 'P4-I001')
            native = selected['fields']['native_record']
            for key in ('dependency_dimensions', 'coverage_assertion_refs', 'seed_evidence_refs'):
                native[key] = []

    ids = [row['id'] for name in ('inquiries', 'records') for row in first[name]]
    names_a = {identifier: identifier for identifier in ids}
    names_b = {identifier: identifier.replace('P4-', 'P4B-', 1) for identifier in ids}
    document = _renamed(first, names_a)
    second = _renamed(first, names_b)
    for name in ('inquiries', 'records'):
        document[name].extend(second[name])
    return document, (_renamed(reference, names_a), _renamed(reference, names_b))


def test_small_two_inquiries_keep_all_families_and_five_global_domains():
    dossier, references = _two_compact_inquiry_case()
    outcome = _analyze_value(dossier)
    assert type(outcome) is contract._AnalyticalOutcome
    assert outcome.execution_state == 'completed'
    assert len(outcome.plan.jobs) == 32 and len(outcome.results) == 120
    selected = _selected_disclosure(outcome, references)
    port = RecordingPort()
    actual = _plain(_assemble(outcome, selected, port))
    _assert_two_inquiry_material(actual, port.units)


def _assert_two_inquiry_material(actual, units):
    _assert_partitions(actual)
    _assert_report_links(actual)
    assert len(actual['capabilities']) == 30
    assert len(actual['observability_domains']) == 5
    scopes = {row['id']: row for row in actual['scopes']}
    results = {row['id']: row for row in actual['results']}
    for inquiry, artifact in (('P4-I001', 'P4-ART'), ('P4B-I001', 'P4B-ART')):
        capabilities = [row for row in actual['capabilities']
                        if row['inquiry_ref']['identifier'] == inquiry]
        assert [row['diagnostic_id'] for row in capabilities] == list(FAMILIES)
        for capability in capabilities:
            assert all(scopes[results[identifier]['scope_ref']]['inquiry_ref']['identifier'] == inquiry
                       for identifier in capability['result_refs'])
        assert any(member.get('identifier') == artifact
                   for population in actual['populations']
                   if scopes[population['scope_ref']]['inquiry_ref']['identifier'] == inquiry
                   for member in population['member_refs'])
    assert [(row['level_index'], row['label']) for row in actual['observability_domains']] == list(enumerate(DOMAIN_LABELS))
    for domain in actual['observability_domains']:
        linked = domain['available_result_refs'] + domain['unavailable_result_refs'] + domain['not_evaluated_result_refs']
        if linked:
            assert {scopes[results[identifier]['scope_ref']]['inquiry_ref']['identifier']
                    for identifier in linked} == {'P4-I001', 'P4B-I001'}
    assert 0 < units <= 10_000_000


def test_runtime_disclosure_preserves_two_independent_inquiry_selections():
    dossier, _ = _two_compact_inquiry_case()
    outcome = _analyze_value(dossier)
    assert type(outcome) is contract._AnalyticalOutcome
    assert outcome.execution_state == 'completed'
    assert len(outcome.plan.jobs) == 32 and len(outcome.results) == 120
    port = RecordingPort()
    actual = _plain(disclosure_runtime._assemble_selected_report(outcome, port))
    _assert_two_inquiry_material(actual, port.units)


@pytest.mark.parametrize('allowance', (0, 1, 32, 1024))
def test_bounded_assembly_propagates_actual_stop_without_partial_return(reference_outcome,
                                                                      reference_assembly, allowance):
    _, _, selected, _ = reference_assembly
    port = RecordingPort(stop_after=allowance)
    with pytest.raises(RuntimeError, match='^controlled_assembly_stop$'):
        _assemble(reference_outcome, selected, port)
    assert port.units <= allowance


@pytest.mark.parametrize('group', ('basis', 'disclosures', 'findings', 'owner_witnesses'))
def test_required_selected_material_cannot_silently_disappear(reference_outcome, group):
    basis, disclosures, findings, witnesses = _selection_parts(reference_outcome)
    groups = {'basis': basis, 'disclosures': disclosures,
              'findings': findings, 'owner_witnesses': witnesses}
    assert groups[group]
    groups[group] = groups[group][1:]
    selected = contract._capture_report_disclosure(groups['basis'], groups['disclosures'],
        groups['findings'], RecordingPort(), owner_witnesses=groups['owner_witnesses'])
    with pytest.raises(TypeError):
        _assemble(reference_outcome, selected)


@pytest.mark.parametrize('mutation', (
    'dangling_result_scope', 'dangling_result_population', 'dangling_result_reason',
    'dangling_result_finding', 'dangling_basis_check', 'dangling_reason_result',
    'dangling_population_member', 'missing_source_selector',
    'wrong_capability_partition', 'wrong_domain_state', 'foreign_result_scope',
    'borrowed_check', 'foreign_reason_target', 'count_member_mismatch',
    'fraction_denominator_mismatch', 'hhi_denominator_mismatch',
    'missing_required_leaf_with_closed_links', 'duplicate_pc_with_closed_links',
    'graph_node_kind_disagrees_with_actual_input',
))
def test_reference_validator_rejects_independent_single_reference_mutants(reference_outcome,
                                                                        reference_assembly, mutation):
    frozen, baseline, _, _ = reference_assembly
    contract._validate_report_references(frozen, reference_outcome.prepared, RecordingPort())
    changed = copy.deepcopy(baseline)
    if mutation == 'dangling_result_scope':
        changed['results'][0]['scope_ref'] = 'SIT-SCP-999999'
    elif mutation == 'dangling_result_population':
        changed['results'][0]['population_refs'][0] = 'SIT-POP-999999'
    elif mutation == 'dangling_result_reason':
        next(row for row in changed['results'] if row['reason_refs'])['reason_refs'][0] = 'SIT-RSN-999999'
    elif mutation == 'dangling_result_finding':
        next(row for row in changed['results'] if row['witness_refs'])['witness_refs'][0] = 'SIT-FND-999999'
    elif mutation == 'dangling_basis_check':
        next(row for row in changed['basis_index'] if row['check_refs'])['check_refs'][0] = 'SIT-CHK-999999'
    elif mutation == 'dangling_reason_result':
        changed['reasons'][0]['affected_result_refs'][0] = 'SIT-RES-999999'
    elif mutation == 'dangling_population_member':
        changed['populations'][0]['member_refs'][0]['identifier'] = 'P4-NOT-SUPPLIED'
    elif mutation == 'missing_source_selector':
        changed['basis_index'][0]['source']['selector'] = 'data.never_supplied'
    elif mutation == 'wrong_capability_partition':
        capability = next(row for row in changed['capabilities'] if row['available_result_refs'])
        target = capability['available_result_refs'].pop()
        capability['unavailable_result_refs'].append(target)
    elif mutation == 'wrong_domain_state':
        domain = next(row for row in changed['observability_domains'] if row['available_result_refs'])
        target = domain['available_result_refs'].pop()
        domain['unavailable_result_refs'].append(target)
    elif mutation == 'foreign_result_scope':
        row = changed['results'][0]
        row['scope_ref'] = next(scope['id'] for scope in changed['scopes']
                                if scope['id'] != row['scope_ref'])
    elif mutation == 'borrowed_check':
        row = changed['results'][0]
        row['check_refs'][0] = next(check['id'] for check in changed['checks']
                                    if check['scope_ref'] != row['scope_ref'])
    elif mutation == 'foreign_reason_target':
        reason = changed['reasons'][0]
        reason['affected_result_refs'][0] = next(row['id'] for row in changed['results']
                                                if row['scope_ref'] != reason['scope_ref'])
    elif mutation == 'count_member_mismatch':
        changed['results'][0]['value'] = 2
    elif mutation == 'fraction_denominator_mismatch':
        next(row for row in changed['results'] if row['field_key'] ==
             'documentary_origin_resolution_fraction')['value']['denominator'] = 2
    elif mutation == 'hhi_denominator_mismatch':
        next(row for row in changed['results'] if row['field_key'] ==
             'single_origin_contribution_hhi')['value']['denominator'] = 2
    elif mutation == 'missing_required_leaf_with_closed_links':
        # A deliberately compound mutation tests one semantic obligation:
        # the required leaf must exist even if all remaining links are closed.
        row = next(row for row in changed['results']
                   if row['field_key'] == 'claim_artifact_record_count')
        removed_result, removed_checks = row['id'], set(row['check_refs'])
        assert row['reason_refs'] == [] and row['witness_refs'] == []
        changed['results'].remove(row)
        changed['checks'] = [check for check in changed['checks']
                             if check['id'] not in removed_checks]
        for collection in ('capabilities', 'observability_domains', 'basis_index'):
            for entry in changed[collection]:
                for name, values in entry.items():
                    if name in ('result_refs', 'available_result_refs', 'check_refs'):
                        entry[name] = [ref for ref in values if ref != removed_result and
                                       ref not in removed_checks]
        _assert_partitions(changed)
        _assert_report_links(changed)
    elif mutation == 'duplicate_pc_with_closed_links':
        # Add a second ID for the same scoped PC and update its navigation.
        # All foreign targets exist; only the repeated prerequisite is wrong.
        row = changed['results'][0]
        original = next(check for check in changed['checks'] if check['id'] == row['check_refs'][0])
        duplicated = copy.deepcopy(original)
        duplicated['id'] = 'SIT-CHK-000672'
        changed['checks'].append(duplicated)
        row['check_refs'].append(duplicated['id'])
        for capability in changed['capabilities']:
            if row['id'] in capability['result_refs']:
                capability['check_refs'].append(duplicated['id'])
        _assert_partitions(changed)
        _assert_report_links(changed)
    elif mutation == 'graph_node_kind_disagrees_with_actual_input':
        node = next(node for finding in changed['findings']
                    for component in finding['witness']['components']
                    if component['type'] == 'graph_witness'
                    for node in component['nodes']
                    if node['ref']['identifier'] == 'P4-E1')
        assert node['kind'] == 'evidence_item'
        node['kind'] = 'artifact'
        # Both kinds legally use the records collection. Only actual input
        # reconciliation can reject this well-shaped, existing input ref.
        contract._freeze_report_document(changed, RecordingPort())
    with pytest.raises(TypeError):
        candidate = contract._freeze_report_document(changed, RecordingPort())
        contract._validate_report_references(candidate, reference_outcome.prepared, RecordingPort())


def test_selected_capture_detaches_mutable_container_occurrences(reference_outcome):
    basis, disclosures, findings, owners = _selection_parts(reference_outcome)
    selected = contract._capture_report_disclosure(basis, disclosures, findings,
                    RecordingPort(), owner_witnesses=owners)
    expected_basis = tuple(basis[0][1]['qualifications'])
    body = next(value for _, value in disclosures if value['records'])
    selected_body = next(value for _, value in selected.disclosures if value['records'])
    expected_native = selected_body['records'][0]['fields']['native_record']['id']
    basis[0][1]['qualifications'].append('UNSELECTED-MUTATION')
    body['records'][0]['fields']['native_record']['id'] = 'UNSELECTED-MUTATION'
    assert selected.basis_entries[0][1]['qualifications'] == expected_basis
    assert selected_body['records'][0]['fields']['native_record']['id'] == expected_native


@pytest.mark.parametrize('mutation', ('unknown_member', 'raw_source_object',
                                     'unknown_typed_leaf', 'duplicate_owner'))
def test_selected_capture_rejects_noncontract_material_without_protocol_calls(reference_outcome,
                                                                              mutation):
    from source_integrity_toolkit.contracts.bundle import _Object

    class Hostile:
        def __repr__(self):
            raise AssertionError('unknown leaf repr called')

        def __str__(self):
            raise AssertionError('unknown leaf str called')

        def __iter__(self):
            raise AssertionError('unknown leaf iteration called')

    basis, disclosures, findings, owners = _selection_parts(reference_outcome)
    if mutation == 'unknown_member':
        basis[0][1]['unregistered_member'] = None
    elif mutation == 'raw_source_object':
        basis[0][1]['method'] = _Object(())
    elif mutation == 'unknown_typed_leaf':
        basis[0][1]['method'] = Hostile()
    else:
        basis = basis + (basis[0],)
    with pytest.raises(TypeError):
        contract._capture_report_disclosure(basis, disclosures, findings,
                    RecordingPort(), owner_witnesses=owners)


@pytest.mark.parametrize('processing,input_state,kind', (
    ('rejected', 'rejected', 'validation_diagnostics'),
    ('interrupted', 'not_completed', 'processing_diagnostics'),
    ('failed', 'not_completed', 'processing_diagnostics'),
    ('failed', 'accepted', 'processing_diagnostics'),
))
def test_constructed_safe_stop_projection_has_no_analytical_salvage(reference_outcome,
                                                                   processing, input_state, kind):
    # These are explicitly constructed owner transports, not a claim that a
    # real public invocation or resource interruption has already been wired.
    code = {'rejected': 'input_not_accepted', 'interrupted': 'resource_limit_reached',
            'failed': 'execution_failed'}[processing]
    stop = _PreparationStop(input_state, processing, code)
    if processing == 'rejected':
        cause = _PreparationAborted(stop, diagnostic_code='missing_required_field')
    elif processing == 'interrupted':
        cause = _PreparationAborted(stop, limit_id='WU9-L01')
    else:
        cause = _AnalysisAborted(stop)
    prepared = reference_outcome.prepared if input_state == 'accepted' else None
    frozen = assemble._assemble_diagnostic(cause, RecordingPort(), prepared=prepared)
    actual = _plain(frozen)
    assert actual['report_kind'] == kind
    assert actual['run']['processing_state'] == processing
    assert actual['input_validation']['state'] == input_state
    assert actual['run']['completed_diagnostic_ids'] == []
    for field in COLLECTIONS[:-1] + ('observability_domains',):
        assert actual[field] == [], field
    assert all(reason['scope_ref'] is None and reason['affected_result_refs'] == [] and
               reason['input_refs'] == [] for reason in actual['reasons'])
    for field in ('started_at', 'finished_at'):
        assert actual['run'][field] == {'state': 'unknown', 'value': None,
            'precision': None, 'reason': 'not_recorded_by_SIT-RP-0.1'}
    if input_state == 'accepted':
        assert actual['input_identity']['bundle_id'] == 'P4-BUNDLE-REFERENCE'
        assert actual['input_identity']['snapshot_id'] == 'P4-SNAPSHOT-REFERENCE-01'
    else:
        assert actual['input_identity']['bundle_id'] is None
        assert actual['input_identity']['snapshot_id'] is None



def _two_hop_dossier():
    dossier = _reference_dossier()
    records = {row['id']: row for row in dossier['records']}
    second = copy.deepcopy(records['P4-E1'])
    second['id'] = 'P4-E2'
    second['data']['locator'] = 'sample-2'
    second['data']['description'] = 'Explicit intermediate contribution in a two-hop path.'
    dossier['records'].append(second)
    assertions = {row['id']: row for row in dossier['assertions']}
    last = copy.deepcopy(assertions['P4-PARENT'])
    last['id'] = 'P4-PARENT2'
    last['data']['from_ref'] = 'P4-E2'
    dossier['assertions'].append(last)
    assertions['P4-PARENT']['data'].update(predicate='derived_from', to_ref='P4-E2')
    coverage = assertions['P4-COVER']['data']['details']
    coverage['member_refs'] = ['P4-E1', 'P4-E2', 'P4-O1']
    coverage['scope_note'] = 'Exactly these three records and all their permitted acquisition-parent predicates.'
    return dossier


def _fixture_replace_strings(value, substitutions):
    """Exact names in an independently selected fixture, never product output."""
    if type(value) is str:
        return substitutions.get(value, value)
    if type(value) is list:
        return [_fixture_replace_strings(item, substitutions) for item in value]
    if type(value) is dict:
        return {key: _fixture_replace_strings(item, substitutions) for key, item in value.items()}
    return value


def _two_hop_graph_bodies():
    def ref(identifier):
        collection = ('evidence_references' if identifier == 'P4-SUPPORT'
                      else 'assertions' if identifier.startswith('P4-PARENT') else 'records')
        return {'collection': collection, 'identifier': identifier, 'selector': None}

    def node(identifier):
        return {'kind': 'origin_event' if identifier == 'P4-O1' else 'evidence_item',
                'ref': ref(identifier)}

    def edge(identifier, source, target, predicate):
        return {'source': node(source), 'target': node(target),
                'source_ref': ref(identifier), 'predicate': predicate,
                'eligible': True, 'reason_codes': []}

    first = edge('P4-PARENT', 'P4-E1', 'P4-E2', 'derived_from')
    second = edge('P4-PARENT2', 'P4-E2', 'P4-O1', 'originates_from')

    def component(kind, count, **fields):
        body = {'type': 'graph_witness', 'kind': kind, 'member_count': count,
                'nodes': [], 'edges': [], 'members': [], 'internal_edges': [],
                'exit_edges': [], 'starts': [], 'target': None,
                'examined_nodes': [], 'examined_edges': [], 'frontiers': [],
                'terminals': [], 'observations': []}
        body.update(fields)
        return body

    def witness(ids, body):
        return {'input_refs': sorted([ref(identifier) for identifier in ids],
                                    key=lambda item: (item['collection'], item['identifier'])),
                'components': [body]}

    first_path = component('path', 3, nodes=[node('P4-E1'), node('P4-E2')], edges=[first])
    last_path = component('path', 3, nodes=[node('P4-E2'), node('P4-O1')], edges=[second])
    path = component('path', 5, nodes=[node('P4-E1'), node('P4-E2'), node('P4-O1')],
                     edges=[first, second])
    full_trace = component('complete_trace', 9, starts=[node('P4-E1')],
        examined_nodes=[node('P4-E1'), node('P4-E2'), node('P4-O1')],
        examined_edges=[first, second], terminals=[node('P4-O1')], observations=[first, second])
    immediate_trace = component('complete_trace', 5, starts=[node('P4-E1')],
        examined_nodes=[node('P4-E1'), node('P4-E2')], examined_edges=[first], observations=[first])
    all_inputs = ('P4-PARENT', 'P4-PARENT2', 'P4-SUPPORT', 'P4-E1', 'P4-E2', 'P4-O1')
    first_inputs = ('P4-PARENT', 'P4-SUPPORT', 'P4-E1', 'P4-E2')
    return {
        'first_path': witness(first_inputs, first_path),
        'last_path': witness(('P4-PARENT2', 'P4-SUPPORT', 'P4-E2', 'P4-O1'), last_path),
        'path': witness(all_inputs, path),
        'full_trace': witness(all_inputs, full_trace),
        'immediate_trace': witness(first_inputs, immediate_trace),
    }


def _two_hop_case():
    dossier = _two_hop_dossier()
    outcome = _analyze_value(dossier)
    assert type(outcome) is contract._AnalyticalOutcome
    assert outcome.execution_state == 'completed'
    assert len(outcome.results) == 87 and len(outcome.plan.jobs) == 25
    selected = _reference_document()

    # P4-E2 and P4-PARENT2 intentionally copy the reference's explicit supplied
    # provenance. Their input identities remain distinct basis objects.
    for old, new in [('P4-E1', 'P4-E2'), ('P4-PARENT', 'P4-PARENT2')]:
        source = next(row for row in selected['basis_index']
                      if row['source']['identifier'] == old and row['source']['selector'] is None)
        selected['basis_index'].append(_fixture_replace_strings(source, {old: new}))

    # The selected native coverage record is the one amended input assertion.
    coverage = next(row for row in dossier['assertions'] if row['id'] == 'P4-COVER')
    for row in selected['results']:
        if row['field_key'] == 'coverage_disclosures':
            body = row['value']['records'][0]['fields']['native_record']
            body['data']['details']['member_refs'] = list(coverage['data']['details']['member_refs'])
            body['data']['details']['scope_note'] = coverage['data']['details']['scope_note']

    # Existing private Findings cover each actual single edge and each exact
    # assurance query. The longer retained owner path has no equal private
    # Finding; that distinction is the purpose of this regression case.
    graph = _two_hop_graph_bodies()
    old_path = next(row for row in selected['findings']
        if row['condition_code'] == 'transformation_path_witness' and
        len(row['witness']['components']) == 1)
    last_path = copy.deepcopy(old_path)
    old_path['witness'] = copy.deepcopy(graph['first_path'])
    last_path['witness'] = copy.deepcopy(graph['last_path'])
    selected['findings'].append(last_path)
    assurance = next(row for row in selected['findings']
        if row['condition_code'] == 'scoped_no_witness' and
        any(ref['identifier'] == 'P4-PARENT' for ref in row['witness']['input_refs']))
    selected['findings'].append(_fixture_replace_strings(assurance, {'P4-PARENT': 'P4-PARENT2'}))

    basis = _selected_basis_entries(outcome, (selected,))
    disclosures = _selected_result_disclosures(outcome, (selected,))
    findings = _selected_existing_findings(outcome, (selected,))
    owners = []
    for owner in outcome.witnesses:
        if owner.payload[0][0] != 'graph_witness':
            continue
        kind = owner.payload[0][1]
        if kind == 'path':
            assert owner.member_count == 5
            body = graph['path']
        elif owner.refs[0].anchor[0] == 'complete_trace':
            assert kind == 'complete_trace' and owner.member_count == 9
            body = graph['full_trace']
        else:
            assert owner.refs[0].anchor[0] == 'immediate_complete_trace'
            assert kind == 'complete_trace' and owner.member_count == 5
            body = graph['immediate_trace']
        owners.append((owner, copy.deepcopy(body)))
    assert len(owners) == 3
    return dossier, outcome, (basis, disclosures, findings, tuple(owners))


def _assert_two_hop_material(document):
    """Semantic expectations authored from E1 -> E2 -> O1, not report IDs."""
    findings = {row['id']: row for row in document['findings']}
    row = next(row for row in document['results'] if row['field_key'] == 'single_origin_contribution_hhi')
    assert row['execution_state'] == 'completed' and row['result_state'] == 'available'
    assert row['value'] == {'numerator': 1, 'denominator': 1}
    assert row['witness_refs']
    components = [component for ref in row['witness_refs']
                  for component in findings[ref]['witness']['components']]
    path = next(component for component in components
                if component.get('kind') == 'path' and len(component['edges']) == 2)
    assert [node['ref']['identifier'] for node in path['nodes']] == ['P4-E1', 'P4-E2', 'P4-O1']
    assert [edge['source_ref']['identifier'] for edge in path['edges']] == ['P4-PARENT', 'P4-PARENT2']
    trace = next(component for component in components if component.get('kind') == 'complete_trace')
    assert trace['member_count'] == 9
    assert [node['ref']['identifier'] for node in trace['examined_nodes']] == ['P4-E1', 'P4-E2', 'P4-O1']
    assert [edge['source_ref']['identifier'] for edge in trace['observations']] == ['P4-PARENT', 'P4-PARENT2']
    basis_ids = {(entry['source']['collection'], entry['source']['identifier'])
                 for entry in document['basis_index']}
    assert {('records', 'P4-E1'), ('records', 'P4-E2'),
            ('assertions', 'P4-PARENT'), ('assertions', 'P4-PARENT2')} <= basis_ids
    for result in document['results']:
        if result['diagnostic_id'] in ('SIT-M002', 'SIT-M004', 'SIT-M005', 'SIT-M006', 'SIT-M007'):
            assert result['witness_refs'], result['field_key']
            assert all(findings[ref]['scope_ref'] == result['scope_ref']
                       for ref in result['witness_refs'])
    inherited = next(row for row in document['results']
                     if row['field_key'] == 'inherited_only_seed_fraction')
    assert inherited['value'] == {'numerator': 1, 'denominator': 1}


def test_two_hop_retained_owner_path_does_not_require_an_equal_private_finding():
    _, outcome, parts = _two_hop_case()
    basis, disclosures, findings, owners = parts
    selected = contract._capture_report_disclosure(basis, disclosures, findings,
        RecordingPort(), owner_witnesses=owners)
    actual = _plain(_assemble(outcome, selected))
    _assert_two_hop_material(actual)
    _assert_partitions(actual)
    _assert_report_links(actual)


def test_runtime_disclosure_retains_actual_two_hop_owner_proof():
    outcome = _analyze_value(_two_hop_dossier())
    assert type(outcome) is contract._AnalyticalOutcome
    assert outcome.execution_state == 'completed'
    assert len(outcome.plan.jobs) == 25 and len(outcome.results) == 87
    port = RecordingPort()
    actual = _plain(disclosure_runtime._assemble_selected_report(outcome, port))
    _assert_two_hop_material(actual)
    _assert_partitions(actual)
    _assert_report_links(actual)
    assert 0 < port.units <= 10_000_000


# The following are explicitly constructed trusted component controls. They
# exercise value projection and linking, not a complete analytical envelope.
def _interval_component(reference_outcome):
    scope = next(result.ref.scope for result in reference_outcome.results
                 if result.ref.field_key == 'stage_occurrence_completion_interval')
    members = tuple(values._InputRef('records', 'COMPONENT-MEMBER-' + str(index))
                    for index in range(6))
    population = values._Population(scope, 'pipeline_member', members,
                                   'Explicit six-member constructed component cohort.')
    partition = values._Partition(population, (
        values._PartitionCategory('U', members[4:], 2),
        values._PartitionCategory('Y', members[:2], 2),
        values._PartitionCategory('F', members[2:4], 2),
    ))
    interval = values._CompletionInterval(values._Fraction(2, 6, population),
        values._Fraction(4, 6, population), 'finite_cohort_completion', partition)
    result = values._Result(values._ResultRef('SIT-M010',
        'stage_occurrence_completion_interval', scope), (population,), 'completed',
        'available', 'attributed_record', 'completion_interval', interval,
        (), (), (), (), 'Constructed finite cohort; not a probability interval.')
    return result


def test_available_completion_interval_uses_exact_shared_population(reference_outcome):
    result = _interval_component(reference_outcome)
    port = RecordingPort()
    selection = contract._capture_report_disclosure((), (), (), port)
    state = assemble._Assembly(reference_outcome, selection, port)
    state.result(result)
    state.identities_for_rows()
    projected = state.resolve(state.rows['results'][0]['body'])
    interval = projected['value']
    assert interval['lower'] == {'numerator': 2, 'denominator': 6}
    assert interval['upper'] == {'numerator': 4, 'denominator': 6}
    assert interval['interval_kind'] == 'finite_cohort_completion'
    assert interval['population_ref'] == interval['partition']['population_ref']
    assert projected['population_refs'] == (interval['population_ref'],)
    population = state.resolve(state.rows['populations'][0]['body'])
    assert len(population['member_refs']) == interval['partition']['total'] == 6
    categories = interval['partition']['categories']
    assert [(row['label'], row['count']) for row in categories] == [('U', 2), ('Y', 2), ('F', 2)]
    all_members = [row['identifier'] for category in categories for row in category['member_refs']]
    assert len(all_members) == len(set(all_members)) == 6
    assert set(all_members) == {row['identifier'] for row in population['member_refs']}
    assert 0 < port.units < 10_000_000


def test_completion_interval_projection_rejects_unregistered_population(reference_outcome):
    result = _interval_component(reference_outcome)
    port = RecordingPort()
    selection = contract._capture_report_disclosure((), (), (), port)
    state = assemble._Assembly(reference_outcome, selection, port)
    projected = state.value(result)
    state.identities_for_rows()
    with pytest.raises(contract._ReportContractError):
        state.resolve(projected)


def _witness_collection_component(reference_outcome, *, retain=True):
    scope = next(result.ref.scope for result in reference_outcome.results
                 if result.ref.field_key == 'evaluator_overlap_witnesses')
    members = (values._InputRef('records', 'COMPONENT-LEFT'),
               values._InputRef('records', 'COMPONENT-RIGHT'))
    population = values._Population(scope, 'record', members,
                                   'Explicit two-member constructed witness component.')
    ref = values._ResultRef('SIT-M008', 'evaluator_overlap_witnesses', scope)
    witness_ref = values._WitnessRef(scope, 'member_set', ('constructed_overlap',))
    result = values._Result(ref, (population,), 'completed', 'available',
        'graph_derivation', 'witness_collection', values._WitnessCollection((witness_ref,)),
        (), (), (witness_ref,), (), 'Constructed typed witness projection only.')
    payload = (('selected_members', members, 2),)
    record = contract._WitnessRecord((witness_ref,), payload, (), 2)
    finding = contract._PrivateFinding('positive_witness',
        'evaluator_overlap_witness', ('SIT-M008',), ('SIT-TH006',), scope,
        (population,), (), contract._DetachedFindingWitness(members, payload, 4),
        (), (), (ref,), 'These two represented members form this constructed witness.',
        'Component-only check; no source authenticity or global independence conclusion.', ())
    selected_body = {'input_refs': [_source(member) for member in members],
                     'components': [{'type': 'selected_members',
                         'members': [_source(member) for member in members],
                         'member_count': 2}]}
    port = RecordingPort()
    selection = contract._capture_report_disclosure((), (),
                                ((finding, selected_body),), port)
    outcome = replace(reference_outcome, results=(result,), findings=(finding,),
                      witnesses=(record,) if retain else (), capabilities=(), domains=())
    state = assemble._Assembly(outcome, selection, port)
    state.result(result)
    state.finding(finding)
    assemble._assemble_witnesses(state)
    state.identities_for_rows()
    return state, finding, port


def test_available_witness_collection_links_same_actual_finding(reference_outcome):
    state, finding, port = _witness_collection_component(reference_outcome)
    projected = state.resolve(state.rows['results'][0]['body'])
    identifier = state.resolve_link(finding)
    assert projected['value'] == {'witness_refs': (identifier,)}
    assert projected['witness_refs'] == (identifier,)
    assert identifier.startswith('SIT-FND-')
    proof = state.resolve(state.rows['findings'][0]['body'])
    assert proof['witness']['components'][0]['member_count'] == 2
    assert [item['identifier'] for item in proof['witness']['components'][0]['members']] == [
        'COMPONENT-LEFT', 'COMPONENT-RIGHT']
    assert 0 < port.units < 10_000_000


def test_witness_collection_projection_rejects_missing_retained_witness(reference_outcome):
    state, unused, unused_port = _witness_collection_component(reference_outcome, retain=False)
    with pytest.raises(contract._ReportContractError):
        state.resolve(state.rows['results'][0]['body'])


# Constructed typed witness components below share one exact scope on purpose.
# Additional input identities are fixture-only; this is not a full dossier test.
def _same_scope_witness_component(reference_outcome, *, unrelated=False):
    scope = next(result.ref.scope for result in reference_outcome.results
                 if result.ref.field_key == 'single_origin_contribution_hhi')
    input_specs = {
        'P4-E1': ('records', 'evidence_item', 'P4-E1'),
        'P4-O1': ('records', 'origin_event', 'P4-O1'),
        'P4-PARENT': ('assertions', None, 'P4-PARENT'),
        'P4-E2': ('records', 'evidence_item', 'P4-E1'),
        'P4-O2': ('records', 'origin_event', 'P4-O1'),
        'P4-PARENT2': ('assertions', None, 'P4-PARENT'),
        'P4-E3': ('records', 'evidence_item', 'P4-E1'),
        'P4-O3': ('records', 'origin_event', 'P4-O1'),
        'P4-BOUND': ('assertions', None, 'P4-BOUND'),
        'P4-COVER': ('assertions', None, 'P4-COVER'),
        'P4-ACTOR': ('records', 'actor', 'P4-ACTOR'),
    }

    def ref(identifier):
        return values._InputRef(input_specs[identifier][0], identifier)

    def node(identifier):
        return ('node', ref(identifier), input_specs[identifier][1])

    def public_node(identifier):
        return {'ref': _source(ref(identifier)), 'kind': input_specs[identifier][1]}

    def edge(source, target, assertion):
        return ('edge', node(source), node(target),
                ('assertions', assertion, '', 'records', target), ref(assertion),
                'originates_from', True, ())

    def public_edge(source, target, assertion):
        return {'source': public_node(source), 'target': public_node(target),
                'source_ref': _source(ref(assertion)),
                'predicate': 'originates_from', 'eligible': True, 'reason_codes': []}

    def bodies(kind, start, target, assertion=None):
        private = {name: () for name in ('nodes', 'edges', 'members', 'internal_edges',
            'exit_edges', 'starts', 'examined_nodes', 'examined_edges', 'frontiers',
            'terminals', 'observations')}
        private['target'] = None
        public = {name: [] for name in private if name != 'target'}
        public['target'] = None
        if kind == 'path':
            private.update(nodes=(node(start), node(target)), edges=(edge(start, target, assertion),))
            public.update(nodes=[public_node(start), public_node(target)],
                          edges=[public_edge(start, target, assertion)])
            count = 3
        elif kind == 'complete_trace':
            private.update(starts=(node(start),), examined_nodes=(node(start), node(target)),
                examined_edges=(edge(start, target, assertion),), terminals=(node(target),),
                observations=(edge(start, target, assertion),))
            public.update(starts=[public_node(start)], examined_nodes=[public_node(start), public_node(target)],
                examined_edges=[public_edge(start, target, assertion)], terminals=[public_node(target)],
                observations=[public_edge(start, target, assertion)])
            count = 6
        else:
            assert kind == 'no_witness_in_examined_view'
            private.update(starts=(node(start),), examined_nodes=(node(start),),
                           terminals=(node(start),), target=node(target))
            public.update(starts=[public_node(start)], examined_nodes=[public_node(start)],
                          terminals=[public_node(start)], target=public_node(target))
            count = 4
        payload = ('graph_witness', kind, scope.inquiry_ref.identifier,
                   tuple(ref.identifier for ref in scope.claim_refs),
                   scope.dependency_dimension, scope.graph_view, scope.operation_anchor,
                   tuple(private.items()), count)
        public.update(type='graph_witness', kind=kind, member_count=count)
        return payload, public

    specifications = [
        ('SIT-M002', 'origin_boundary_disclosures', 'P4-E1', 'P4-O1', 'P4-PARENT', 'P4-BOUND'),
        ('SIT-M007', 'ancestry_gap_disclosures', 'P4-E2', 'P4-O2', 'P4-PARENT2', 'P4-COVER'),
    ]
    if unrelated:
        specifications.append(('SIT-M014', 'anomaly_context_disclosures',
                               'P4-E3', 'P4-O3', None, 'P4-ACTOR'))
    results, records, selected_owners, selected_disclosures = [], [], [], []
    needed_basis = set()
    for family, field, start, target, assertion, marker in specifications:
        inputs = (start, target) if assertion is None else (start, target, assertion)
        needed_basis.update(inputs + (marker,))
        links = []
        kinds = ('no_witness_in_examined_view',) if assertion is None else ('path', 'complete_trace')
        for kind in kinds:
            payload, selected = bodies(kind, start, target, assertion)
            link = values._WitnessRef(scope, 'path' if kind == 'path' else 'member_set',
                                      ('component', family, kind, ref(start)))
            record = contract._WitnessRecord((link,), (payload,), (), payload[-1])
            records.append(record)
            links.append(link)
            selected_owners.append((record, {'input_refs': [_source(ref(name))
                for name in sorted(inputs)], 'components': [selected]}))
        result_ref = values._ResultRef(family, field, scope)
        result = values._Result(result_ref, (), 'completed', 'available', 'attributed_record',
            'record_disclosures', values._RecordDisclosures(()), (),
            (values._BasisRef(ref(marker)),), tuple(links), (),
            'Constructed component composition; no real-world qualification is asserted.')
        results.append(result)
        selected_disclosures.append((result_ref, {'records': []}))

    expected = _reference_document()
    selected_basis = []
    for identifier in sorted(needed_basis):
        template = input_specs[identifier][2]
        row = copy.deepcopy(next(item for item in expected['basis_index']
            if item['source']['identifier'] == template and item['source']['selector'] is None))
        del row['id']
        del row['source']
        row['check_refs'] = ()
        selected_basis.append((values._BasisRef(ref(identifier)), row))
    port = RecordingPort()
    selection = contract._capture_report_disclosure(tuple(selected_basis),
        tuple(selected_disclosures), (), port, owner_witnesses=tuple(selected_owners))
    outcome = replace(reference_outcome, results=tuple(results), findings=(),
                      witnesses=tuple(records), capabilities=(), domains=())
    state = assemble._Assembly(outcome, selection, port)
    for result in results:
        state.result(result)
    assemble._assemble_witnesses(state)
    state.identities_for_rows()
    projected_results = {row['owner'].ref.diagnostic_id: state.resolve(row['body'])
                         for row in state.rows['results']}
    projected_findings = {state.resolve_link(row['owner']): state.resolve(row['body'])
                          for row in state.rows['findings']}
    projected_basis = {state.resolve_link(row['owner']): state.resolve(row['body'])['source']['identifier']
                       for row in state.rows['basis_index']}
    return projected_results, projected_findings, projected_basis, port.units


def test_two_same_scope_path_trace_pairs_keep_distinct_supporting_metadata(reference_outcome):
    results, findings, basis, units = _same_scope_witness_component(reference_outcome)
    assert len(findings) == 2
    assert 0 < units < 10_000_000
    expected = {
        'SIT-M002': ('P4-E1', 'P4-O1', 'P4-PARENT', 'P4-BOUND'),
        'SIT-M007': ('P4-E2', 'P4-O2', 'P4-PARENT2', 'P4-COVER'),
    }
    identifiers = []
    for family, (start, target, assertion, marker) in expected.items():
        links = results[family]['witness_refs']
        assert len(links) == 1
        identifiers.extend(links)
        finding = findings[links[0]]
        assert finding['diagnostic_refs'] == (family,)
        assert {basis[identifier] for identifier in finding['basis_refs']} == {
            start, target, assertion, marker}
        components = finding['witness']['components']
        assert [component['kind'] for component in components] == ['path', 'complete_trace']
        path, trace = components
        assert [node['ref']['identifier'] for node in path['nodes']] == [start, target]
        assert path['edges'][0]['source_ref']['identifier'] == assertion
        assert trace['starts'][0]['ref']['identifier'] == start
        assert trace['examined_edges'][0]['source_ref']['identifier'] == assertion
        assert trace['observations'][0]['source_ref']['identifier'] == assertion
    assert len(set(identifiers)) == 2


def test_unrelated_same_scope_absence_keeps_own_material_family_and_basis(reference_outcome):
    results, findings, basis, units = _same_scope_witness_component(reference_outcome, unrelated=True)
    assert len(findings) == 3
    assert 0 < units < 10_000_000
    absent_links = results['SIT-M014']['witness_refs']
    assert len(absent_links) == 1
    finding = findings[absent_links[0]]
    assert finding['diagnostic_refs'] == ('SIT-M014',)
    assert finding['condition_code'] == 'scoped_no_witness'
    assert finding['observation_kind'] == 'no_witness_in_examined_view'
    assert finding['threat_family_refs'] == ()
    assert {basis[identifier] for identifier in finding['basis_refs']} == {'P4-E3', 'P4-O3', 'P4-ACTOR'}
    components = finding['witness']['components']
    assert len(components) == 1 and components[0]['kind'] == 'no_witness_in_examined_view'
    assert components[0]['starts'][0]['ref']['identifier'] == 'P4-E3'
    assert components[0]['target']['ref']['identifier'] == 'P4-O3'
    assert components[0]['examined_edges'] == () and components[0]['observations'] == ()
    for family in ('SIT-M002', 'SIT-M007'):
        links = results[family]['witness_refs']
        assert len(links) == 1 and absent_links[0] not in links
        assert findings[links[0]]['diagnostic_refs'] == (family,)
        assert all(component['kind'] in ('path', 'complete_trace')
                   for component in findings[links[0]]['witness']['components'])


def _review_scan_dossier():
    """Small actual input with two assessments and repeated review role slots."""
    dossier = _reference_dossier()
    dossier['bundle_id'] = 'W04-BUNDLE-SCAN-SLOTS'
    dossier['snapshot_id'] = 'W04-SNAPSHOT-SCAN-SLOTS'
    actor = next(row for row in dossier['records'] if row['id'] == 'P4-ACTOR')
    other = copy.deepcopy(actor)
    other['id'] = 'W04-OTHER'
    dossier['records'].append(other)
    role = {'role': 'human_reviewer', 'object_ref': 'P4-ACTOR',
            'evidence_ref_ids': ['P4-SUPPORT'],
            'qualifications': ['Repeated original owner role slot; no additional human is inferred.']}
    dossier['records'].append({
        'id': 'W04-REVIEW', 'kind': 'evaluation',
        'data': {'evaluation_kind': 'human_review', 'target_refs': ['P4-ART'],
                 'role_bindings': [copy.deepcopy(role), dict(copy.deepcopy(role), role='judge')],
                 'result_refs': [], 'occurred_at': copy.deepcopy(dossier['recorded_at']),
                 'review_contribution': 'Recorded review contribution with two supplied role slots.'},
        'provenance': copy.deepcopy(actor['provenance']),
    })
    dossier['inquiries'][0]['target_object_refs'] = ['W04-REVIEW']
    original = next(row for row in dossier['assertions'] if row['id'] == 'P4-BOUND')
    for suffix in ('B', 'A'):
        assessment = copy.deepcopy(original)
        assessment['id'] = 'W04-SCAN-' + suffix
        assessment['data'] = {
            'assessment_kind': 'independence', 'subject_refs': ['P4-ACTOR', 'W04-OTHER'],
            'details': {'comparison_form': 'pairwise', 'dimension': 'organizational_control',
                       'conclusion': 'unknown', 'examined_dependency_refs': [],
                       'unexamined_dimensions': ['acquisition'], 'coverage_ref': None,
                       'scope_note': 'Supplied scan context only; no applicable acquisition assessment.'},
        }
        assessment['gaps'] = [{'field': 'data.details.coverage_ref', 'reason': 'not_examined',
                              'detail': 'No coverage assessment is supplied for this other dimension.'}]
        dossier['assertions'].append(assessment)
    return dossier


@pytest.fixture(scope='module')
def review_scan_outcome():
    dossier = _review_scan_dossier()
    original = copy.deepcopy(dossier)
    outcome = _analyze_value(dossier)
    assert dossier == original
    assert type(outcome) is contract._AnalyticalOutcome
    assert outcome.execution_state == 'completed'
    return outcome


def _reverse_review_payload(payload):
    if payload[0] != 'human_review_witness':
        return payload
    kind, members, assessments, slots, count = payload
    return kind, members, tuple(reversed(assessments)), tuple(reversed(slots)), count


def _selected_input_value(value):
    """Read only this selected component's frozen JSON and typed input links."""
    if type(value) is _InputRef:
        return _source(value)
    if type(value) is contract._ReportMapping:
        return {name: _selected_input_value(value[name]) for name in value}
    if type(value) is tuple:
        return [_selected_input_value(item) for item in value]
    assert value is None or type(value) in (str, bool, int)
    return value


@pytest.mark.parametrize('owner_order', ('actual', 'reversed_component'))
def test_runtime_review_scan_and_repeated_source_slots_keep_owner_order(review_scan_outcome,
                                                                       owner_order):
    outcome = review_scan_outcome
    if owner_order == 'reversed_component':
        # Explicit trusted detached-owner component variant, backed by the
        # same real prepared input. This alternative order is not attributed
        # to the current analytical implementation or reservation ledger.
        witnesses = tuple(replace(row, payload=tuple(_reverse_review_payload(part)
            for part in row.payload)) for row in outcome.witnesses)
        findings = tuple(replace(row, witness=replace(row.witness,
            owner_witnesses=tuple(_reverse_review_payload(part)
                for part in row.witness.owner_witnesses))) for row in outcome.findings)
        outcome = replace(outcome, witnesses=witnesses, findings=findings)
    owner = next(row for row in outcome.witnesses
                 if any(part[0] == 'human_review_witness' for part in row.payload))
    payload = next(part for part in owner.payload if part[0] == 'human_review_witness')
    _, members, assessments, slots, count = payload
    assert [ref.identifier for ref in members] == ['W04-REVIEW']
    expected_scan = ['W04-SCAN-A', 'W04-SCAN-B']
    expected_slots = [
        {'collection': 'inquiries', 'identifier': 'P4-I001', 'selector': 'target_object_refs'},
        {'collection': 'records', 'identifier': 'W04-REVIEW', 'selector': None},
        {'collection': 'records', 'identifier': 'P4-ACTOR', 'selector': None},
        {'collection': 'records', 'identifier': 'P4-ACTOR', 'selector': None},
    ]
    if owner_order == 'reversed_component':
        expected_scan.reverse()
        expected_slots.reverse()
    assert [ref.identifier for ref in assessments] == expected_scan
    assert [_source(ref) for ref in slots] == expected_slots
    assert count == len(members) + len(assessments) + len(slots) == 7
    original = next(row for row in outcome.results
                    if row.ref.field_key == 'corrective_independence_disclosures')
    port = RecordingPort()
    selected = disclosure_runtime._select_report_disclosure(outcome, port)
    body = next(body for ref, body in selected.disclosures
                if ref.field_key == 'corrective_independence_disclosures')
    rows = _selected_input_value(body)['records']
    primary_count = len(original.value.records)
    assert [row['source'] for row in rows[:primary_count]] == [
        _source(row.source) for row in original.value.records]
    scan_rows = rows[primary_count:primary_count + 2]
    source_rows = rows[primary_count + 2:]
    assert [row['source'] for row in scan_rows] == [
        {'collection': 'assertions', 'identifier': identifier, 'selector': None}
        for identifier in expected_scan]
    assert [row['source'] for row in source_rows] == expected_slots
    assert all(row['qualifications'] == [
        'Examined assessment only; this scan does not establish applicability or qualification for the selected review scope.']
        for row in scan_rows)
    assert all(row['qualifications'] == [
        'Actual owner selection/source reference slot; this record does not establish an applicable review or independent process.']
        for row in source_rows)
    for row in scan_rows + source_rows:
        assert set(row['fields']) == {'native_record'}
        assert row['fields']['native_record']['id'] == row['source']['identifier']
    actor_rows = [row for row in source_rows if row['source']['identifier'] == 'P4-ACTOR']
    assert len(actor_rows) == 2 and actor_rows[0] == actor_rows[1]
    review_row = next(row for row in source_rows if row['source']['identifier'] == 'W04-REVIEW')
    roles = review_row['fields']['native_record']['data']['role_bindings']
    assert [role['role'] for role in roles] == ['human_reviewer', 'judge']
    assert [role['object_ref'] for role in roles] == ['P4-ACTOR', 'P4-ACTOR']
    assert roles[0]['qualifications'] == [
        'Repeated original owner role slot; no additional human is inferred.']
    assert 0 < port.units <= 10_000_000


def test_empty_seed_dimension_preserves_completed_trace_and_unavailable_ratios():
    """Reporting W4-10/18.2: an empty typed search cannot invent a ratio zero."""
    source = _reference_dossier()
    source['bundle_id'] = 'P4-EMPTY-SEED-ACQUISITION'
    source['snapshot_id'] = 'P4-EMPTY-SEED-ACQUISITION-01'
    inquiry = source['inquiries'][0]
    inquiry['dependency_dimensions'] = ['acquisition']
    for name in ('seed_artifact_refs', 'seed_evidence_refs', 'coverage_assertion_refs'):
        inquiry[name] = []
    source['records'] = [row for row in source['records']
                         if row['id'] in ('P4-ACTOR', 'P4-CLAIM')]
    source['assertions'] = []
    source['evidence_references'] = []
    before = copy.deepcopy(source)
    outcome = _analyze_value(source)
    assert type(outcome) is contract._AnalyticalOutcome
    assert outcome.execution_state == 'completed'
    assert source == before
    traces = [part for record in outcome.witnesses for part in record.payload
              if part[0] == 'graph_witness']
    assert len(traces) == 1 and traces[0][1] == 'complete_trace'
    assert traces[0][-1] == 0
    port = RecordingPort()
    document = _plain(disclosure_runtime._assemble_selected_report(outcome, port))
    assert document['run']['processing_state'] == 'completed'
    assert document['input_validation'] == {'state': 'accepted', 'diagnostics': []}
    assert len(document['capabilities']) == 15
    reasons = {row['id']: row for row in document['reasons']}
    findings = {row['id']: row for row in document['findings']}
    empty = [row for row in document['findings']
             if any(part['kind'] == 'complete_trace' for part in row['witness']['components']
                    if part['type'] == 'graph_witness')]
    assert len(empty) == 1
    finding = empty[0]
    assert finding['condition_code'] == 'scoped_no_witness'
    assert finding['observation_kind'] == 'no_witness_in_examined_view'
    assert finding['threat_family_refs'] == []
    assert len(finding['witness']['components']) == 1
    component = finding['witness']['components'][0]
    assert component['type'] == 'graph_witness' and component['kind'] == 'complete_trace'
    assert component['member_count'] == 0 and component['target'] is None
    for name in ('nodes', 'members', 'starts', 'examined_nodes', 'frontiers', 'terminals',
                 'edges', 'internal_edges', 'exit_edges', 'examined_edges', 'observations'):
        assert component[name] == []
    assert 'no selected starting members' in finding['statement']
    assert 'does not establish outside-world absence or independence' in finding['interpretation_limit']
    assert 'does not supply a nonzero ratio denominator' in finding['interpretation_limit']
    for field in ('single_origin_contribution_hhi', 'documentary_origin_resolution_fraction',
                  'inherited_only_seed_fraction'):
        selected = [row for row in document['results'] if row['field_key'] == field]
        assert len(selected) == 1
        result = selected[0]
        assert result['execution_state'] == 'completed'
        assert result['result_state'] == 'unavailable' and result['value'] is None
        assert 'zero_denominator' in {reasons[ref]['code'] for ref in result['reason_refs']}
        assert all(ref in findings for ref in result['witness_refs'])
    for field in ('reached_origin_record_count', 'documentary_origin_boundary_record_count',
                  'origin_boundary_disclosures', 'unresolved_frontier_reference_count',
                  'unqualified_terminal_record_count', 'seed_items_with_unresolved_ancestry_count',
                  'ancestry_gap_disclosures'):
        result = next(row for row in document['results'] if row['field_key'] == field)
        assert result['witness_refs'] == [finding['id']]
    _assert_partitions(document)
    _assert_report_links(document)


@pytest.mark.parametrize('field', [
    'nodes', 'members', 'starts', 'examined_nodes', 'frontiers', 'terminals',
    'edges', 'internal_edges', 'exit_edges', 'examined_edges', 'observations',
    'target', 'member_count',
])
def test_nonempty_trace_cannot_use_empty_search_projection(field):
    component = {name: () for name in ('nodes', 'members', 'starts', 'examined_nodes',
        'frontiers', 'terminals', 'edges', 'internal_edges', 'exit_edges', 'examined_edges', 'observations')}
    component.update(kind='complete_trace', target=None, member_count=0)
    assert assemble._empty_completed_trace(component, RecordingPort()) is True
    component[field] = 1 if field == 'member_count' else (('one_retained_occurrence',),)
    assert assemble._empty_completed_trace(component, RecordingPort()) is False
