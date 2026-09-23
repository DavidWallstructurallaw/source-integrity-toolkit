# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W13 actual capability navigation, field-local checks and private links.

Reporting 12--17 supplies the assertions. Registry unions are navigation only;
available record disclosures do not qualify a stronger statistic or another
domain. Test faults change a current owner's returned private representation.
"""
import copy
from dataclasses import FrozenInstanceError, fields, is_dataclass, replace
import importlib.util
import inspect
import json
from pathlib import Path

import pytest

import source_integrity_toolkit as public
from source_integrity_toolkit.contracts import report, results as r
from source_integrity_toolkit.contracts.evidence import _PreparedBundle
from source_integrity_toolkit.runtime import boundary
from source_integrity_toolkit.runtime.diagnostics import _AnalyticalDiagnostic, _SafeDiagnostic


ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    'sit_w13_observability_cases', ROOT / 'tests/integration/test_analytical_pipeline.py')
cases = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cases)
FAMILIES = tuple('SIT-M%03d' % number for number in range(1, 16))
DOMAIN_FAMILIES = (
    ('SIT-M001',),
    ('SIT-M002', 'SIT-M006', 'SIT-M007', 'SIT-M015'),
    ('SIT-M002', 'SIT-M003', 'SIT-M004', 'SIT-M005', 'SIT-M006'),
    ('SIT-M008', 'SIT-M011', 'SIT-M013', 'SIT-M015'),
    ('SIT-M009', 'SIT-M010', 'SIT-M012', 'SIT-M014'),
)


def complete(source):
    out = boundary._analyze_value(source)
    assert out.input_state == 'accepted' and out.execution_state == 'completed'
    assert out.results
    return out


@pytest.fixture(scope='module')
def full_outcome():
    return complete(cases._family_value())


def walk(value):
    yield value
    if is_dataclass(value):
        for field in fields(value):
            if field.name not in ('prepared', 'context', 'job_port'):
                yield from walk(getattr(value, field.name))
    elif type(value) in (tuple, list):
        for item in value:
            yield from walk(item)


def partition(row, result_map):
    groups = ('available', 'unavailable', 'not_applicable', 'not_evaluated')
    linked = []
    for state in groups:
        refs = getattr(row, state + '_result_refs')
        assert len({ref._key() for ref in refs}) == len(refs)
        for ref in refs:
            assert result_map[ref._key()].result_state == state
            linked.append(ref._key())
    assert len(set(linked)) == len(linked)
    assert set(linked) == {ref._key() for ref in row.result_refs}


@pytest.mark.parametrize('family', FAMILIES)
def test_each_family_slot_keeps_every_actual_state_and_field(full_outcome, family):
    out = full_outcome
    rows = [item for item in out.capabilities if item.family == family]
    assert len(rows) == 1
    row = rows[0]
    assert row.inquiry_ref == 'inquiry' and row.execution_state == 'completed'
    expected = next(item[1] for item in report.FAMILY_PREPARATION_BINDINGS if item[0] == family)
    linked = {ref.field_key for ref in row.result_refs}
    assert linked == set(expected)
    assert row.scope_note
    partition(row, {result.ref._key(): result for result in out.results})
    assert not hasattr(row, 'value') and not hasattr(row, 'result_state')


@pytest.mark.parametrize('index,families', tuple(enumerate(DOMAIN_FAMILIES)))
def test_domains_link_their_own_results_without_a_cumulative_ladder(full_outcome, index, families):
    out = full_outcome
    domains = [row for row in out.domains if row.level_index == index]
    assert len(domains) == 1 and domains[0].inquiry_ref == 'inquiry'
    domain = domains[0]
    expected = {row.ref._key() for row in out.results if row.ref.diagnostic_id in families}
    assert {ref._key() for ref in domain.result_refs} == expected
    partition(domain, {row.ref._key(): row for row in out.results})
    assert not hasattr(domain, 'score') and not hasattr(domain, 'max_level')


def test_available_stage_and_case_records_survive_unavailable_ancestry(full_outcome):
    out = full_outcome
    hhi = [row for row in out.results if row.ref.field_key == 'single_origin_contribution_hhi']
    assert hhi and all(row.result_state == 'unavailable' and row.value is None for row in hhi)
    for key in ('pipeline_stage_disclosures', 'correction_case_record_count', 'handling_event_record_count'):
        rows = [row for row in out.results if row.ref.field_key == key]
        assert rows and all(row.result_state == 'available' for row in rows)
        domain = next(item for item in out.domains if item.level_index == 4)
        assert {row.ref._key() for row in rows} <= {ref._key() for ref in domain.available_result_refs}
    assert not hasattr(out, 'overall_level') and not hasattr(out, 'max_level')


def test_actual_checks_are_field_local_and_completion_is_not_a_registry_flag(full_outcome):
    out = full_outcome
    for row in out.results:
        checks = {check.check_id: check for check in row.check_refs}
        assert checks['PC01'].state == 'met'
        assert checks['PC02'].state == 'met'
        assert checks['PC24'].state == 'met'
        assert all(check.result_ref._key() == row.ref._key() for check in row.check_refs)
    for row in out.results:
        checks = {check.check_id for check in row.check_refs}
        if row.ref.diagnostic_id == 'SIT-M001':
            assert checks == {'PC01', 'PC02', 'PC03', 'PC24'}
        if row.ref.field_key in ('correction_case_record_count', 'handling_event_record_count'):
            assert 'PC20' not in checks
        if row.ref.field_key == 'pipeline_stage_disclosures':
            assert all(check.state == 'not_applicable' for check in row.check_refs if check.check_id == 'PC18')
    # Missing comparison basis leaves its submitted population observable.
    compared = {row.ref.field_key: row for row in out.results if row.ref.diagnostic_id == 'SIT-M003'
                and row.ref.scope.dependency_dimension == 'acquisition'}
    assert compared['submitted_comparison_member_count'].result_state == 'available'
    assert compared['submitted_comparison_member_count'].value.value == 2
    assert compared['qualified_process_set_member_count'].result_state == 'unavailable'


def test_every_private_link_resolves_to_actual_supplied_or_delivered_object(full_outcome):
    out = full_outcome
    source = cases._family_value()
    input_keys = {(collection, row['id']) for collection in
                  ('inquiries', 'records', 'assertions', 'evidence_references') for row in source[collection]}
    result_keys = {row.ref._key() for row in out.results}
    witness_keys = {ref._key() for row in out.witnesses for ref in row.refs}
    assert len(result_keys) == len(out.results) and witness_keys
    observed = {'input': 0, 'result': 0, 'witness': 0}
    for obj in walk((out.results, out.findings, out.witnesses, out.capabilities, out.domains, out.jobs)):
        if type(obj) is r._InputRef:
            observed['input'] += 1
            assert (obj.collection, obj.identifier) in input_keys
        elif type(obj) is r._ResultRef:
            observed['result'] += 1
            assert obj._key() in result_keys
        elif type(obj) is r._WitnessRef:
            observed['witness'] += 1
            assert obj._key() in witness_keys
    assert all(observed.values())


def test_context_stage_links_resolve_to_original_m010_results_without_copied_metrics(full_outcome):
    out = full_outcome
    links = [item for row in out.results if row.ref.field_key == 'tail_stage_result_links'
             and row.result_state == 'available' for item in row.value.records]
    assert links
    result_map = {row.ref._key(): row for row in out.results}
    for item in links:
        assert type(item.source) is r._ResultRef and item.source.diagnostic_id == 'SIT-M010'
        actual = result_map[item.source._key()]
        assert actual.execution_state == 'completed' and actual.result_state == 'available'
        native = cases._native(item.fields)
        assert native['source_result_state'] == actual.result_state
        assert native['source_value_kind'] == actual.value_kind
        assert {'numerator', 'denominator', 'value', 'metric', 'retention_fraction',
                'suppression', 'whole_anomaly_retention'}.isdisjoint(native)


def test_navigation_preserves_reason_bindings_for_every_affected_field(full_outcome):
    out = full_outcome
    checked = 0
    for capability in out.capabilities:
        carried = {cases._semantic(reason) for reason in capability.reason_refs}
        for row in out.results:
            if row.ref.diagnostic_id == capability.family and row.ref.scope.inquiry_ref.identifier == capability.inquiry_ref:
                for reason in row.reason_refs:
                    checked += 1
                    assert cases._semantic(reason) in carried
    assert checked > 0


def test_witness_anchors_keep_one_exact_owner_payload_and_do_not_mix_context_with_stages(full_outcome):
    out = full_outcome
    witness_map = {ref._key(): witness for witness in out.witnesses for ref in witness.refs}
    observed = set()
    for row in out.results:
        if row.ref.diagnostic_id not in ('SIT-M008', 'SIT-M011', 'SIT-M014', 'SIT-M010'):
            continue
        for ref in row.witness_refs:
            witness = witness_map[ref._key()]
            assert len(witness.payload) == 1
            native = witness.payload[0]
            if ref.anchor[0] in ('context_preservation', 'presence_selection'):
                assert native[0] == 'selected_members'
                assert witness.member_count == native[2] == len(native[1])
                observed.add(ref.anchor[0])
            elif row.ref.diagnostic_id in ('SIT-M008', 'SIT-M011'):
                assert native[0] == 'graph_witness'
                assert native[8] == witness.member_count
                observed.add(row.ref.diagnostic_id)
                if row.ref.diagnostic_id == 'SIT-M011' and ref.anchor[0] == 'declared':
                    assert native[1] == 'path'
                    assert tuple(node[1].identifier for node in dict(native[7])['nodes']) == ('channel', 'claim')
    assert observed == {'context_preservation', 'presence_selection', 'SIT-M008', 'SIT-M011'}


def test_declared_and_authorized_route_links_resolve_separate_actual_ordered_paths():
    spec = importlib.util.spec_from_file_location(
        'sit_w13_route_witness_cases', ROOT / 'tests/unit/test_correction_routes.py')
    route = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(route)
    source = route.small()
    source['records'] = [row for row in source['records'] if row['id'] in ('actor', 'claim', 'artifact', 'channel')]
    source['inquiries'][0].update(seed_artifact_refs=['artifact'], seed_evidence_refs=[],
                                 target_object_refs=[], dependency_dimensions=[])
    out = complete(source)
    witness_map = {ref._key(): witness for witness in out.witnesses for ref in witness.refs}
    expected = {'declared_correction_route_witnesses': 'declared',
                'applicable_authorized_route_witnesses': 'authorized'}
    links = []
    for field, meaning in expected.items():
        row = next(row for row in out.results if row.ref.field_key == field)
        assert row.result_state == 'available' and len(row.value.witness_refs) == 1
        ref = row.value.witness_refs[0]
        assert ref.anchor[0] == meaning
        witness = witness_map[ref._key()]
        assert len(witness.payload) == 1
        native = witness.payload[0]
        assert native[0:2] == ('graph_witness', 'path')
        material = dict(native[7])
        assert tuple(node[1].identifier for node in material['nodes']) == ('channel', 'claim')
        assert len(material['edges']) == 1
        links.append(ref._key())
    assert links[0] != links[1]


def test_positive_evaluator_path_ref_does_not_attach_the_entire_family_witness_list():
    source = cases._minimal_value()
    source['inquiries'][0].update(dependency_dimensions=['model_ancestry'], target_object_refs=['evaluation'])
    for name in ('model', 'model2', 'shared'):
        source['records'].append(cases._record(name, 'model', {
            'model_key': name, 'version_label': 'v1', 'family_label': name, 'provider_ref': 'actor'}))
    source['records'].append(cases._record('evaluation', 'evaluation', {
        'evaluation_kind': 'judgment', 'target_refs': ['claim'],
        'role_bindings': [{'role': role, 'object_ref': name, 'evidence_ref_ids': [], 'qualifications': []}
                         for role, name in (('generator', 'model'), ('judge', 'model2'))],
        'result_refs': [], 'occurred_at': cases._unknown(), 'review_contribution': None}))
    for name in ('model', 'model2'):
        source['assertions'].append(cases._assertion('parent-' + name, 'relation', {
            'predicate': 'model_derived_from', 'from_ref': name, 'to_ref': 'shared',
            'polarity': 'affirmed', 'dimension': 'model_ancestry',
            'details': {'occurred_at': cases._unknown()}}))
    out = complete(source)
    row = next(row for row in out.results if row.ref.field_key == 'evaluator_overlap_witnesses')
    assert row.result_state == 'available'
    refs = [ref for ref in row.value.witness_refs if ref.kind == 'path']
    assert len(refs) == 2
    witness_map = {ref._key(): witness for witness in out.witnesses for ref in witness.refs}
    paths = set()
    for ref in refs:
        witness = witness_map[ref._key()]
        assert len(witness.payload) == 1
        native = witness.payload[0]
        assert native[0:2] == ('graph_witness', 'path')
        material = dict(native[7])
        assert len(material['edges']) == 1
        paths.add(tuple(node[1].identifier for node in material['nodes']))
    assert paths == {('model', 'shared'), ('model2', 'shared')}


def test_every_inquiry_keeps_fifteen_slots_and_five_independent_domains():
    source = cases._minimal_value()
    other = copy.deepcopy(source['inquiries'][0])
    other['id'] = 'second-inquiry'
    source['inquiries'].append(other)
    out = complete(source)
    assert {(item.inquiry_ref, item.family) for item in out.capabilities} == {
        (inquiry, family) for inquiry in ('inquiry', 'second-inquiry') for family in FAMILIES}
    assert len(out.capabilities) == 30
    assert {(item.inquiry_ref, item.level_index) for item in out.domains} == {
        (inquiry, index) for inquiry in ('inquiry', 'second-inquiry') for index in range(5)}


def test_no_structural_subject_is_explained_without_inventing_assessments_or_roles():
    out = complete(cases._minimal_value())
    assert tuple(item.family for item in out.capabilities) == FAMILIES
    for family in ('SIT-M003', 'SIT-M008', 'SIT-M009', 'SIT-M010', 'SIT-M011', 'SIT-M012'):
        capability = next(item for item in out.capabilities if item.family == family)
        assert capability.scope_note and capability.result_refs
        rows = [row for row in out.results if row.ref.diagnostic_id == family]
        assert rows
        for row in rows:
            if row.result_state != 'available':
                assert row.value is None and row.reason_refs
            else:
                # A completed empty native inventory can remain explicit; no
                # absent role, comparison or route establishes a qualified 0.
                empty_case_fields = {'documentary_linked_change_target_count': 'case_target',
                                     'cases_with_documentary_linked_change_count': 'correction_case'}
                if row.ref.field_key in empty_case_fields:
                    # Definitions 27.2 counts the qualified subset of a fully
                    # enumerated empty case population, so this exact 0 is valid.
                    assert row.ref.diagnostic_id == 'SIT-M012' and row.result_origin == 'qualification_check'
                    assert row.value_kind == 'count' and row.value.value == 0
                    population = row.value.population
                    assert population.unit == empty_case_fields[row.ref.field_key]
                    assert population.membership_state == 'enumerated_for_scope' and population.member_refs == ()
                    assert row.population_refs == (population,) and row.reason_refs == ()
                    assert [(basis.source.collection, basis.source.identifier) for basis in row.basis_refs] == [
                        ('inquiries', 'inquiry')]
                    assert {check.check_id: check.state for check in row.check_refs} == {
                        'PC01': 'met', 'PC02': 'met', 'PC03': 'met', 'PC04': 'not_applicable',
                        'PC05': 'not_applicable', 'PC08': 'not_applicable', 'PC09': 'not_applicable',
                        'PC10': 'not_applicable', 'PC21': 'not_applicable', 'PC24': 'met'}
                else:
                    assert row.result_origin == 'inventory' or (
                        row.value_kind == 'record_disclosures' and row.value.records == ())


def test_inquiry_inventory_duplicates_from_two_claim_jobs_coalesce_by_semantic_body():
    out = complete(cases._minimal_value(two_claims=True))
    rows = [row for row in out.results if row.ref.diagnostic_id == 'SIT-M001']
    assert len(rows) == 7
    assert len({row.ref._key() for row in rows}) == 7
    for key in ('nominal_seed_artifact_record_count', 'unresolved_seed_artifact_reference_count',
                'claim_unassigned_seed_artifact_record_count'):
        selected = [row for row in rows if row.ref.field_key == key]
        assert len(selected) == 1 and selected[0].ref.scope.claim_refs == ()
    for key in ('seed_evidence_item_count', 'claim_artifact_record_count'):
        assert {row.ref.scope.claim_refs[0].identifier for row in rows if row.ref.field_key == key} == {'claim', 'claim2'}


def test_actual_evaluation_with_one_role_does_not_become_structurally_inapplicable_or_zero():
    source = cases._minimal_value()
    source['inquiries'][0]['dependency_dimensions'] = ['model_ancestry']
    source['inquiries'][0]['target_object_refs'] = ['evaluation']
    source['records'].append(cases._record('evaluation', 'evaluation', {
        'evaluation_kind': 'judgment', 'target_refs': ['claim'],
        'role_bindings': [{'role': 'candidate', 'object_ref': 'claim',
                           'evidence_ref_ids': [], 'qualifications': []}],
        'result_refs': [], 'occurred_at': cases._unknown(), 'review_contribution': None}))
    out = complete(source)
    capability = next(item for item in out.capabilities if item.family == 'SIT-M008')
    assert capability.scope_note
    rows = [row for row in out.results if row.ref.diagnostic_id == 'SIT-M008']
    assert rows and all(row.result_state != 'not_applicable' for row in rows)
    for row in rows:
        if row.value_kind == 'count':
            assert row.result_state == 'unavailable' and row.value is None
    assert any(reason.code == 'roles_incomplete' for row in rows for reason in row.reason_refs)


def test_missing_comparison_is_an_evidence_gap_in_an_actual_claim_dimension():
    source = cases._minimal_value()
    source['inquiries'][0]['dependency_dimensions'] = ['acquisition']
    out = complete(source)
    selected = {row.ref.field_key: row for row in out.results if row.ref.diagnostic_id == 'SIT-M003'}
    for field in ('qualified_process_set_member_count', 'qualified_origin_set_member_count'):
        assert selected[field].result_state == 'unavailable' and selected[field].value is None
        assert any(reason.classification == 'evidence_gap' for reason in selected[field].reason_refs)


@pytest.mark.parametrize('mutation', ('unequal_duplicate', 'missing_leaf', 'missing_pc24',
                                     'dangling_result', 'dangling_witness_payload'))
def test_assembly_rejects_incomplete_or_conflicting_owner_delivery(monkeypatch, mutation):
    complete(cases._minimal_value())
    commit = boundary._commit_job

    def corrupted(port, values, findings, witnesses):
        if not values or values[0].ref.diagnostic_id != 'SIT-M001':
            return commit(port, values, findings, witnesses)
        if mutation == 'unequal_duplicate':
            values += (replace(values[0], interpretation_limit='Different semantic qualification.'),)
        elif mutation == 'missing_leaf':
            values = values[:-1]
        elif mutation == 'missing_pc24':
            values = (replace(values[0], check_refs=tuple(check for check in values[0].check_refs
                                                        if check.check_id != 'PC24')),) + values[1:]
        elif mutation == 'dangling_witness_payload':
            assert witnesses
            witnesses = (replace(witnesses[0], payload=witnesses[0].payload +
                                 (r._InputRef('records', 'absent-source-record'),)),) + witnesses[1:]
        else:
            ref = r._ResultRef('SIT-M005', 'single_origin_contribution_hhi', values[0].ref.scope)
            reason = r._Reason('documentary_basis_incomplete', values[0].ref.scope,
                (ref,), (), 'This typed analytical slot was never delivered.', 'evidence_gap')
            checks = tuple(replace(check, reason_refs=(reason,)) if check.check_id == 'PC03' else check
                           for check in values[0].check_refs)
            values = (replace(values[0], check_refs=checks),) + values[1:]
        return commit(port, values, findings, witnesses)

    monkeypatch.setattr(boundary, '_commit_job', corrupted)
    out = boundary._analyze_value(cases._minimal_value())
    assert type(out) is _AnalyticalDiagnostic
    assert (out.input_state, out.execution_state, out.code) == ('accepted', 'failed', 'execution_failed')
    assert not hasattr(out, 'results')


@pytest.mark.parametrize('mode', ('value', 'utf8'))
def test_preparation_entry_points_keep_their_original_nonanalytical_contract(mode):
    source = cases._minimal_value()
    argument = source if mode == 'value' else json.dumps(source).encode()
    prepare = boundary._prepare_value if mode == 'value' else boundary._prepare_utf8
    observe = boundary._prepare_evidence_value if mode == 'value' else boundary._prepare_evidence_utf8
    prepared = prepare(argument)
    assert type(prepared) is _PreparedBundle and not hasattr(prepared, 'results')
    observed = observe(argument)
    assert type(observed) is report._ObservabilityPreparation and not hasattr(observed, 'results')
    for inquiry in observed.inquiries:
        assert tuple(item.family for item in inquiry.families) == FAMILIES
        for check in inquiry.prerequisites:
            assert check.complete_check_executed is (check.prerequisite == 'PC01')
            assert check.answer == ('met' if check.prerequisite == 'PC01' else None)
    rejected = prepare({'contract_version': 'PRIVATE_SENTINEL'}) if mode == 'value' else prepare(b'{}')
    assert type(rejected) is _SafeDiagnostic and rejected.input_state == 'rejected'


def test_private_outcome_is_immutable_and_has_no_public_report_or_options(full_outcome):
    out = full_outcome
    with pytest.raises(FrozenInstanceError):
        out.execution_state = 'interrupted'
    for name in ('report_kind', 'report_contract', 'report_id', 'schema_version', 'run',
                 'input_validation', 'overall_level', 'max_level', 'to_json'):
        assert not hasattr(out, name)
    assert public.__all__ == ('audit_bundle', 'audit_file', '__version__')
    for finding in out.findings:
        assert not hasattr(finding.witness, 'job_port') and not hasattr(finding.witness, 'prepared')
    assert not hasattr(public, '_analyze_value') and not hasattr(public, '_analyze_utf8')
    assert tuple(inspect.signature(boundary._analyze_value).parameters) == ('value',)
    assert tuple(inspect.signature(boundary._analyze_utf8).parameters) == ('raw',)
    with pytest.raises(NotImplementedError):
        public.audit_bundle(cases._minimal_value())
    with pytest.raises(NotImplementedError):
        public.audit_file(object(), object())
