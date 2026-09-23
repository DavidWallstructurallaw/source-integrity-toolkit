# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W13 source-derived integration oracles for the complete private pipeline.

The synthetic dossiers below name their entire finite populations. They do not
borrow a result from an earlier owner job or change the fixed runtime budgets.
Plan 3.4/18 and Reporting 12--17 supply the execution and scope expectations.
"""
import copy
from dataclasses import fields, is_dataclass
import json

import pytest

from source_integrity_toolkit.contracts.bundle import _Array, _Number, _Object
from source_integrity_toolkit.runtime import boundary, resources


FAMILIES = tuple('SIT-M%03d' % number for number in range(1, 16))


def _unknown():
    return {'state': 'unknown', 'value': None, 'precision': None,
            'reason': 'Fictional time not supplied.'}


def _window():
    return {'start': _unknown(), 'end': _unknown()}


def _provenance():
    return {'attributed_to_ref': 'actor', 'basis_kind': 'declaration',
            'evidence_ref_ids': [], 'method': 'Finite fictional integration case.',
            'qualifications': ['Supplied declaration only.']}


def _record(identifier, kind, data):
    return {'id': identifier, 'kind': kind, 'data': data,
            'provenance': _provenance()}


def _minimal_value(*, two_claims=False):
    """Exactly one Inquiry; no implicit dimension, seed, role, or stage cohort."""
    source = {'contract_version': 'sit-bundle/0.1', 'bundle_id': 'bundle',
              'snapshot_id': 'snapshot', 'recorded_at': _unknown(), 'predecessor': None,
              'inquiries': [{'id': 'inquiry', 'target_claim_refs': ['claim'],
                  'target_object_refs': [], 'seed_artifact_refs': [], 'seed_evidence_refs': [],
                  'boundary': {'description': 'Fictional boundary',
                      'criterion': 'Only supplied structural bindings', 'system_refs': []},
                  'time_window': _window(), 'as_of': _unknown(),
                  'dependency_dimensions': [], 'coverage_assertion_refs': [],
                  'provenance': _provenance()}],
              'records': [_record('actor', 'actor', {'actor_kind': 'human',
                  'identity_disclosure': 'pseudonymous', 'display_name': 'Fictional preparer'}),
                  _record('claim', 'claim', {'claim_key': 'claim-family',
                      'version_label': 'v1', 'text': 'Fictional claim', 'context': 'Original context'})],
              'assertions': [], 'evidence_references': []}
    if two_claims:
        source['inquiries'][0]['target_claim_refs'].append('claim2')
        source['records'].append(_record('claim2', 'claim', {'claim_key': 'claim-family',
            'version_label': 'v2', 'text': 'Second supplied claim', 'context': 'Second context'}))
    return source


def _assertion(identifier, kind, data):
    return {'id': identifier, 'assertion_kind': kind,
            'scope': {'inquiry_refs': ['inquiry'], 'claim_refs': ['claim'],
                      'effective_window': _window()}, 'provenance': _provenance(),
            'asserted_at': _unknown(), 'lifecycle_state': 'active',
            'lifecycle_basis_ref_ids': [], 'data': data}


def _assessment(identifier, kind, subjects, details):
    return _assertion(identifier, 'assessment', {'assessment_kind': kind,
        'subject_refs': list(subjects), 'details': details})


def _family_value():
    """Small independently authored dossier with actual bindings for 15 owners."""
    source = _minimal_value()
    inquiry = source['inquiries'][0]
    inquiry.update(seed_artifact_refs=['artifact', 'artifact2'],
        seed_evidence_refs=['e', 'e2'], target_object_refs=['evaluation'],
        dependency_dimensions=['acquisition', 'model_ancestry'])
    for suffix in ('', '2'):
        source['records'].extend([
            _record('artifact' + suffix, 'artifact', {'artifact_kind': 'document',
                'work_key': 'work' + suffix, 'version_label': 'v1', 'locators': [],
                'published_at': _unknown(), 'retrieved_at': _unknown(),
                'content_evidence_refs': []}),
            _record('e' + suffix, 'evidence_item', {'claim_ref': 'claim',
                'artifact_ref': 'artifact' + suffix, 'locator': 'paragraph',
                'epistemic_type': 'fictional_example', 'description': 'Supplied contribution'}),
            _record('origin' + suffix, 'origin_event', {'event_kind': 'data_collection',
                'event_key': 'origin' + suffix, 'performed_by_refs': ['actor'],
                'method_ref': 'artifact', 'occurred_at': _unknown(),
                'description': 'Fictional acquisition'}),
            _record('model' + suffix, 'model', {'model_key': 'model' + suffix,
                'version_label': 'v1', 'family_label': 'literal-family', 'provider_ref': 'actor'}),
        ])
        source['assertions'].append(_assertion('parent' + suffix, 'relation', {
            'predicate': 'originates_from', 'from_ref': 'e' + suffix,
            'to_ref': 'origin' + suffix, 'polarity': 'affirmed',
            'dimension': 'acquisition', 'details': {}}))
    source['records'].extend([
        _record('evaluation', 'evaluation', {'evaluation_kind': 'judgment',
            'target_refs': ['claim'], 'role_bindings': [
                {'role': 'generator', 'object_ref': 'model', 'evidence_ref_ids': [], 'qualifications': []},
                {'role': 'judge', 'object_ref': 'model2', 'evidence_ref_ids': [], 'qualifications': []}],
            'result_refs': [], 'occurred_at': _unknown(), 'review_contribution': None}),
        _record('channel', 'correction_channel', {'owner_refs': ['actor'],
            'target_refs': ['claim'], 'contact_locator': 'mailto:inert@example.invalid',
            'declared_action_types': ['review'], 'valid_window': _window()}),
        _record('submission', 'correction_event', {'event_kind': 'submission', 'case_ref': None,
            'channel_ref': 'channel', 'target_refs': ['claim'], 'occurred_at': _unknown(),
            'details': {'submission_kind': 'objection', 'summary': 'Supplied request'}}),
        _record('handling', 'correction_event', {'event_kind': 'handling', 'case_ref': 'submission',
            'channel_ref': 'channel', 'target_refs': ['claim'], 'occurred_at': _unknown(),
            'details': {'outcome': 'accepted', 'reason': 'Handling is not downstream change'}}),
        _record('pipeline', 'pipeline_record', {'subject_ref': 'e', 'run_key': 'run',
            'stage_key': 'admit', 'stage': 'admission', 'state': 'occurred', 'output_refs': ['e'],
            'observed_at': _unknown(), 'linkage_kind': 'use_record', 'detail': 'One native observation'}),
        _record('anomaly', 'anomaly', {'inquiry_refs': ['inquiry'], 'claim_ref': None,
            'original_context': 'Unclassified timing distinction remains unresolved.',
            'context_evidence_ref': None, 'classification_state': 'unclassified',
            'caller_label': None, 'comparison_note': 'No rarity or suppression claim'}),
    ])
    source['assertions'].extend([
        _assessment('comparison', 'independence', ('origin', 'origin2'), {
            'comparison_form': 'pairwise', 'dimension': 'acquisition',
            'conclusion': 'independent_process', 'examined_dependency_refs': [],
            'unexamined_dimensions': [], 'coverage_ref': None, 'scope_note': 'Supplied comparison only'}),
        _assessment('externality', 'externality', ('e',), {'boundary_inquiry_ref': 'inquiry',
            'conclusion': 'external', 'grounding_basis': 'Supplied externality only',
            'relevant_time': _unknown()}),
        _assertion('stance', 'relation', {'predicate': 'contradicts', 'from_ref': 'e',
            'to_ref': 'claim', 'polarity': 'affirmed', 'dimension': None, 'details': {}}),
    ])
    source['assertions'][2]['gaps'] = [{'field': 'data.details.coverage_ref',
        'reason': 'not_recorded', 'detail': 'No comparison coverage supplied.'}]
    return source


def _documented_value():
    """Two seed contributions, one supported terminal, one exact population."""
    source = _minimal_value()
    source['inquiries'][0].update(seed_artifact_refs=['artifact'], seed_evidence_refs=['e', 'e2'],
        dependency_dimensions=['acquisition'], coverage_assertion_refs=['coverage'])
    source['records'].append(_record('artifact', 'artifact', {'artifact_kind': 'document',
        'work_key': 'fictional-source', 'version_label': 'v1', 'locators': [],
        'published_at': _unknown(), 'retrieved_at': _unknown(), 'content_evidence_refs': []}))
    source['records'].append(_record('origin', 'origin_event', {'event_kind': 'data_collection',
        'event_key': 'origin', 'performed_by_refs': ['actor'], 'method_ref': 'artifact',
        'occurred_at': _unknown(), 'description': 'One represented documentary origin'}))
    for identifier in ('e', 'e2'):
        source['records'].append(_record(identifier, 'evidence_item', {'claim_ref': 'claim',
            'artifact_ref': 'artifact', 'locator': identifier, 'epistemic_type': 'fictional_example',
            'description': 'Distinct supplied contribution to the same Claim'}))
        source['assertions'].append(_assertion('parent-' + identifier, 'relation', {
            'predicate': 'originates_from', 'from_ref': identifier, 'to_ref': 'origin',
            'polarity': 'affirmed', 'dimension': 'acquisition', 'details': {}}))
    source['assertions'].extend([
        _assessment('coverage', 'coverage', ('inquiry',), {'coverage_kind': 'upstream_history',
            'state': 'complete_for_scope', 'relation_types': ['derived_from', 'copies',
                'syndicated_from', 'summarizes', 'translates', 'quotes', 'originates_from', 'depends_on'],
            'dimensions': ['acquisition'], 'member_refs': ['e', 'e2', 'origin'],
            'omitted_refs': [], 'universe_enumerated': True,
            'scope_note': 'Exactly these three records and their full permitted parent predicates'}),
        _assessment('boundary', 'origin_boundary', ('origin',), {'dimension': 'acquisition',
            'boundary_role': 'documented_origin', 'coverage_ref': 'coverage',
            'termination_reason': 'The supplied finite process excerpt terminates here'}),
    ])
    source['evidence_references'].append({'id': 'support', 'reference_kind': 'supplied_excerpt',
        'availability': 'supplied', 'artifact_ref': 'artifact', 'record_ref': None, 'locator': None,
        'excerpt': 'Fictional supplied acquisition and complete finite parent-scope record.',
        'provided_by_ref': 'actor', 'attestor_ref': None, 'scope_note': 'No outside authentication'})
    for row in source['assertions'] + [row for row in source['records']
                                      if row['kind'] in ('origin_event', 'evidence_item')]:
        row['provenance'].update(basis_kind='documented_record', evidence_ref_ids=['support'],
            method='Examine the supplied finite process excerpt.',
            qualifications=['Caller-supplied documentary material, without external authentication.'])
    return source


def _native(value):
    if type(value) is _Object:
        return {key: _native(item) for key, item in value.items}
    if type(value) is _Array:
        return [_native(item) for item in value.items]
    return value


def _semantic(value):
    """Compare immutable semantic bodies without relying on eq=False identity."""
    if is_dataclass(value):
        return (type(value).__name__, tuple((field.name, _semantic(getattr(value, field.name)))
            for field in fields(value)))
    if type(value) in (tuple, list):
        return tuple(_semantic(item) for item in value)
    return value


def _analyze(source, mode='value'):
    if mode == 'value':
        return boundary._analyze_value(source)
    return boundary._analyze_utf8(json.dumps(source, ensure_ascii=False).encode('utf-8'))


def _rows(outcome, field, *, family=None, claims=None):
    return tuple(row for row in outcome.results if row.ref.field_key == field
        and (family is None or row.ref.diagnostic_id == family)
        and (claims is None or tuple(ref.identifier for ref in row.ref.scope.claim_refs) == claims))


def _disclosures(outcome, field):
    return {item.source.identifier: _native(item.fields)
        for row in _rows(outcome, field) if row.value is not None
        for item in row.value.records}


@pytest.mark.parametrize('mode', ('value', 'utf8'))
def test_all_fifteen_families_execute_actual_finite_scopes_in_both_modes(mode, monkeypatch):
    source = _family_value()
    original = copy.deepcopy(source)
    executed = []
    execute = boundary._execute_job

    def observe(prepared, spec, ledger, port):
        result = execute(prepared, spec, ledger, port)
        executed.append((spec.family, port.used))
        return result

    monkeypatch.setattr(boundary, '_execute_job', observe)
    out = _analyze(source, mode)
    assert out.execution_state == 'completed'
    assert source == original
    assert set(family for family, _ in executed) == set(FAMILIES)
    assert all(used > 0 for _, used in executed)
    assert set(row.ref.diagnostic_id for row in out.results) == set(FAMILIES)
    assert all(row.execution_state == 'completed' for row in out.results)
    assert all(next(check for check in row.check_refs if check.check_id == 'PC24').state == 'met'
               for row in out.results)
    assert {row.value.value for row in _rows(out, 'seed_evidence_item_count')} == {2}
    acquisition_origins = [row for row in _rows(out, 'reached_origin_record_count')
                           if row.ref.scope.dependency_dimension == 'acquisition']
    assert len(acquisition_origins) == 1 and acquisition_origins[0].value.value == 2
    assert tuple(ref.identifier for ref in acquisition_origins[0].value.population.member_refs) == ('origin', 'origin2')
    memberships = [row for row in _rows(out, 'per_seed_origin_memberships')
                   if row.ref.scope.dependency_dimension == 'acquisition']
    assert len(memberships) == 1
    # Definitions22.1: these are documentary-qualified memberships, unlike
    # the separately preserved two reached OriginEvent records above.
    assert {item.member_ref.identifier: tuple(ref.identifier for ref in item.origin_refs)
            for item in memberships[0].value.memberships} == {'e': (), 'e2': ()}
    partition = next(row for row in _rows(out, 'seed_origin_dispositions')
                     if row.ref.scope.dependency_dimension == 'acquisition')
    assert next(category.count for category in partition.value.categories
                if category.label == 'unresolved_or_conflicted') == 2
    assert 'unqualified_origin_boundary' in {reason.code for reason in partition.reason_refs}
    assert {'parent', 'parent2'} <= {
        ref.source.identifier for ref in partition.basis_refs}
    immediate = [row for row in _rows(out, 'immediate_evidence_layer_dispositions')
                 if row.ref.scope.dependency_dimension == 'acquisition']
    assert len(immediate) == 1 and immediate[0].value is not None
    assert tuple(ref.identifier for ref in immediate[0].value.population.member_refs) == ('e', 'e2')
    assert sum(category.count for category in immediate[0].value.categories) == 2
    frontier = [row for row in _rows(out, 'unresolved_frontier_reference_count')
                if row.ref.scope.dependency_dimension == 'acquisition']
    assert len(frontier) == 1 and frontier[0].value.value == 0
    assert {row.value.value for row in _rows(out, 'submitted_comparison_member_count')
            if row.value is not None} == {2}
    for field in ('qualified_process_set_member_count', 'single_origin_contribution_hhi'):
        assert all(row.result_state == 'unavailable' and row.value is None for row in _rows(out, field))
    assert {row.value.value for row in _rows(out, 'correction_case_record_count')} == {1}
    assert {row.value.value for row in _rows(out, 'handling_event_record_count')} == {1}
    assert {row.value.value for row in _rows(out, 'linked_change_event_record_count')} == {0}
    assert any(row.value is not None and row.value.value == 1
               for row in _rows(out, 'matching_family_label_count'))
    assert any(row.value is not None and row.value.witness_refs
               for row in _rows(out, 'declared_correction_route_witnesses'))
    review = _disclosures(out, 'human_contribution_disclosures')['evaluation']
    assert review['data']['review_contribution'] is None
    assert review['contribution_status'] == 'no_human_role'
    basis = _rows(out, 'declared_basis_inventory')
    assert basis and all(row.value is not None for row in basis)
    assert all(sum(category.count for category in row.value.categories) > 0 for row in basis)
    assert all('pipeline' in {ref.identifier for ref in row.value.population.member_refs} for row in basis)
    assert all(category.count == 0 for row in basis for category in row.value.categories
               if category.label != 'declaration')
    assert _disclosures(out, 'externality_assessment_disclosures')['externality']['data']['details']['conclusion'] == 'external'
    assert _disclosures(out, 'pipeline_stage_disclosures')['pipeline']['data']['state'] == 'occurred'
    anomaly = _disclosures(out, 'anomaly_context_disclosures')['anomaly']['native_record']['data']
    assert anomaly['claim_ref'] is None and anomaly['classification_state'] == 'unclassified'
    assert anomaly['original_context'] == 'Unclassified timing distinction remains unresolved.'


@pytest.mark.parametrize('fixture', (_minimal_value, _family_value), ids=('sparse', 'all_families'))
def test_equivalent_admitted_values_agree_in_results_findings_and_scope_plan(fixture):
    source = fixture()
    left, right = _analyze(source), _analyze(source, 'utf8')
    assert left.execution_state == right.execution_state == 'completed'
    assert left.prepared.source_mode == 'constructed_value'
    assert right.prepared.source_mode == 'supplied_utf8'
    for name in ('results', 'findings', 'witnesses', 'capabilities', 'domains', 'plan'):
        assert _semantic(getattr(left, name)) == _semantic(getattr(right, name))


def test_original_binary_float_and_supplied_decimal_are_not_silently_rounded_together():
    source = _minimal_value()
    source['extensions'] = {'fictional:numeric': {'ratio': 0.1, 'exact': 0.5, 'large': 9007199254740991}}
    left, right = _analyze(source), _analyze(source, 'utf8')
    assert left.execution_state == right.execution_state == 'completed'
    l = _native(left.prepared.tree)['extensions']['fictional:numeric']
    r = _native(right.prepared.tree)['extensions']['fictional:numeric']
    assert type(l['ratio']) is type(r['ratio']) is _Number
    assert (l['ratio'].sign, l['ratio'].coefficient, l['ratio'].exponent, l['ratio'].source_kind) == (
        1, '1000000000000000055511151231257827021181583404541015625', -55, 'binary_float')
    assert (r['ratio'].sign, r['ratio'].coefficient, r['ratio'].exponent, r['ratio'].source_kind) == (
        1, '1', -1, 'decimal')
    assert (l['exact'].coefficient, l['exact'].exponent) == (r['exact'].coefficient, r['exact'].exponent) == ('5', -1)
    assert l['large'].coefficient == r['large'].coefficient == '9007199254740991'
    assert _semantic(left.results) == _semantic(right.results)


@pytest.mark.parametrize('mode', ('value', 'utf8'))
def test_two_claim_inventory_coalesces_only_equal_inquiry_cells(mode):
    source = _minimal_value(two_claims=True)
    out = _analyze(source, mode)
    assert out.execution_state == 'completed'
    for field in ('nominal_seed_artifact_record_count', 'unresolved_seed_artifact_reference_count',
                  'claim_unassigned_seed_artifact_record_count'):
        rows = _rows(out, field)
        assert len(rows) == 1 and rows[0].ref.scope.claim_refs == () and rows[0].value.value == 0
    for field in ('seed_evidence_item_count', 'claim_artifact_record_count'):
        rows = _rows(out, field)
        assert len(rows) == 2
        assert {tuple(ref.identifier for ref in row.ref.scope.claim_refs) for row in rows} == {('claim',), ('claim2',)}
        assert {row.value.value for row in rows} == {0}


@pytest.mark.parametrize('mode', ('value', 'utf8'))
def test_no_declared_dimension_cannot_execute_an_implicit_world_dimension(mode):
    out = _analyze(_minimal_value(), mode)
    assert out.execution_state == 'completed'
    dimensional = {'SIT-M002', 'SIT-M004', 'SIT-M005', 'SIT-M006', 'SIT-M007'}
    for row in out.results:
        if row.ref.diagnostic_id in dimensional:
            assert row.ref.scope.dependency_dimension is None
            assert row.result_state == 'not_applicable' and row.value is None
            assert row.reason_refs
    for field in ('declared_basis_inventory', 'reference_availability_inventory'):
        rows = _rows(out, field)
        assert rows and all(row.result_state == 'available' for row in rows)


def test_whole_plan_precedes_single_acceptance_and_jobs_follow_semantic_schedule(monkeypatch):
    source = _minimal_value(two_claims=True)
    second = copy.deepcopy(source['inquiries'][0])
    source['inquiries'][0]['id'] = 'z-inquiry'
    source['inquiries'][0]['target_claim_refs'].reverse()
    second['id'] = 'a-inquiry'
    source['inquiries'].append(second)
    events, owners = [], []
    factory, planner, executor = boundary._new_analysis_budget, boundary._plan_analysis, boundary._execute_job
    accept = resources._AnalysisBudget.record_input_acceptance

    def new_budget():
        owner = factory()
        owners.append(owner)
        events.append(('entry', owner.used))
        return owner

    def plan(prepared, owner):
        assert owner is owners[0] and owner._state == 'not_completed'
        result = planner(prepared, owner)
        events.append(('planned', tuple((job.inquiry_ref, job.family, job.operation_key) for job in result.jobs)))
        assert owner._state == 'not_completed' and owner.used > 0
        return result

    def accepted(owner):
        assert events[-1][0] == 'planned'
        events.append(('accepted', owner.used))
        return accept(owner)

    def execute(prepared, spec, ledger, port):
        assert owners[0]._state == 'accepted'
        events.append(('job', (spec.inquiry_ref, spec.family, spec.operation_key)))
        return executor(prepared, spec, ledger, port)

    monkeypatch.setattr(boundary, '_new_analysis_budget', new_budget)
    monkeypatch.setattr(boundary, '_plan_analysis', plan)
    monkeypatch.setattr(boundary, '_execute_job', execute)
    monkeypatch.setattr(resources._AnalysisBudget, 'record_input_acceptance', accepted)
    out = _analyze(source)
    assert out.execution_state == 'completed' and len(owners) == 1
    assert [event[0] for event in events].count('accepted') == 1
    expected = next(value for kind, value in events if kind == 'planned')
    actual = tuple(value for kind, value in events if kind == 'job')
    assert actual == expected
    assert actual == tuple(sorted(actual, key=lambda key: (key[0], int(key[1][-3:]), key[2])))
    assert {key[0] for key in actual} == {'a-inquiry', 'z-inquiry'}
    assert owners[0].used > next(value for kind, value in events if kind == 'accepted') > 0


def test_supplied_comparison_and_evaluation_bindings_do_not_expand_to_all_pairs():
    source = _family_value()
    source['records'].append(_record('origin3', 'origin_event', {'event_kind': 'data_collection',
        'event_key': 'origin3', 'performed_by_refs': ['actor'], 'method_ref': 'artifact',
        'occurred_at': _unknown(), 'description': 'Uncompared third origin'}))
    out = _analyze(source)
    assert out.execution_state == 'completed'
    comparisons = tuple(row for row in _rows(out, 'submitted_comparison_member_count')
                        if row.value is not None)
    assert len(comparisons) == 1 and comparisons[0].value.value == 2
    assert set(_disclosures(out, 'independence_assessment_disclosures')) == {'comparison'}
    evaluator_rows = _rows(out, 'evaluator_overlap_disclosures')
    assert evaluator_rows
    assert {row.ref.scope.operation_anchor for row in evaluator_rows} == {('generator', 'judge')}
    assert all(tuple(ref.identifier for ref in row.ref.scope.target_refs) == ('evaluation',)
               for row in evaluator_rows)


def test_native_stage_without_cohort_is_retained_beside_unavailable_ratio():
    out = _analyze(_family_value())
    assert out.execution_state == 'completed'
    stages = _disclosures(out, 'pipeline_stage_disclosures')
    assert set(stages) == {'pipeline'} and stages['pipeline']['data']['state'] == 'occurred'
    for field in ('stage_member_partition', 'stage_occurrence_fraction', 'stage_occurrence_completion_interval'):
        rows = _rows(out, field)
        assert rows and all(row.result_state == 'unavailable' and row.value is None for row in rows)


def test_missing_comparison_does_not_erase_the_applicable_claim_question():
    source = _family_value()
    source['assertions'] = [row for row in source['assertions'] if row['id'] != 'comparison']
    out = _analyze(source)
    assert out.execution_state == 'completed'
    rows = _rows(out, 'qualified_process_set_member_count')
    assert rows and all(row.result_state == 'unavailable' and row.value is None for row in rows)
    assert all(row.reason_refs for row in rows)


def test_actual_evaluation_with_missing_role_is_unavailable_not_structurally_absent():
    source = _family_value()
    evaluation = next(row for row in source['records'] if row['id'] == 'evaluation')
    evaluation['data']['role_bindings'] = evaluation['data']['role_bindings'][:1]
    out = _analyze(source)
    assert out.execution_state == 'completed'
    rows = [row for row in out.results if row.ref.diagnostic_id == 'SIT-M008']
    assert rows and all(row.result_state == 'unavailable' and row.value is None for row in rows)
    assert all('roles_incomplete' in {reason.code for reason in row.reason_refs} for row in rows)
    assert 'evaluation' in _disclosures(out, 'human_contribution_disclosures')


def test_reordering_unordered_inputs_keeps_same_plan_and_semantic_results():
    source = _family_value()
    other = copy.deepcopy(source)
    for collection in ('records', 'assertions', 'evidence_references'):
        other[collection].reverse()
    for name in ('seed_artifact_refs', 'seed_evidence_refs', 'dependency_dimensions'):
        other['inquiries'][0][name].reverse()
    first, second = _analyze(source), _analyze(other)
    assert first.execution_state == second.execution_state == 'completed'
    assert _semantic(first.plan) == _semantic(second.plan)
    assert _semantic(first.results) == _semantic(second.results)
    assert _semantic(first.findings) == _semantic(second.findings)


@pytest.mark.parametrize('fixture', (_minimal_value, _family_value), ids=('no_dimension', 'all_families'))
def test_m015_uses_actual_current_job_inventory_and_selected_edge_provider_facts(fixture, monkeypatch):
    from source_integrity_toolkit.analysis import inventory
    from source_integrity_toolkit.graph import projections
    from source_integrity_toolkit.validation import semantics

    inventory_calls, edge_calls, profile_calls = [], [], []
    inventory_owner = inventory._inventory_facts
    edge_owner = projections._check_edge_eligibility
    profile_owner = semantics._provenance_profile

    def inventory_probe(prepared, context, port):
        before = port.used
        facts = inventory_owner(prepared, context, port)
        inventory_calls.append((facts.pc03, prepared, context, port, before, port.used))
        return facts

    def edge_probe(projection, selected_edges, port):
        before = port.used
        fact = edge_owner(projection, selected_edges, port)
        edge_calls.append((fact, projection.prepared, projection.context, port,
                           before, port.used, tuple(selected_edges)))
        return fact

    def provenance_probe(prepared, context, record_refs, reference_refs, coverage_refs, port, *, provider_facts=()):
        providers = {fact.check_id: fact for fact in provider_facts}
        assert set(providers) == {'PC03', 'PC04'}
        pc03 = [call for call in inventory_calls if call[0] is providers['PC03']]
        pc04 = [call for call in edge_calls if call[0] is providers['PC04']]
        assert len(pc03) == len(pc04) == 1
        for call in (pc03[0], pc04[0]):
            assert call[1] is prepared and call[2] is context and call[3] is port
            assert call[5] > call[4]
        assert providers['PC03'].owner == 'SOURCE_INVENTORY'
        assert providers['PC04'].owner == 'GRAPH_VIEW_CONTRACT'
        assert providers['PC03'].state == 'met'
        assert providers['PC04'].state == ('met' if pc04[0][6] else 'not_applicable')
        before = port.used
        result = profile_owner(prepared, context, record_refs, reference_refs, coverage_refs,
                               port, provider_facts=provider_facts)
        assert port.used > before
        for row in result.results:
            checks = {check.check_id: check for check in row.check_refs}
            assert checks['PC03'].state == providers['PC03'].state
            assert checks['PC04'].state == providers['PC04'].state
        profile_calls.append((context, port, result))
        return result

    # Direct imports and module-qualified calls both retain the real owner.
    for module, name, original, probe in (
            (inventory, '_inventory_facts', inventory_owner, inventory_probe),
            (projections, '_check_edge_eligibility', edge_owner, edge_probe),
            (semantics, '_provenance_profile', profile_owner, provenance_probe)):
        for alias, value in tuple(vars(boundary).items()):
            if value is original:
                monkeypatch.setattr(boundary, alias, probe)
        monkeypatch.setattr(module, name, probe)
    out = _analyze(fixture())
    assert out.execution_state == 'completed'
    assert profile_calls
    assert len({id(port) for _, port, _ in profile_calls}) == len(profile_calls)
    assert all(row.ref.diagnostic_id == 'SIT-M015' for _, _, result in profile_calls for row in result.results)


def test_one_claim_cohort_cannot_hide_other_claim_native_stage_at_same_anchor():
    source = _minimal_value(two_claims=True)
    source['records'].append(_record('artifact', 'artifact', {'artifact_kind': 'document',
        'work_key': 'source', 'version_label': 'v1', 'locators': [],
        'published_at': _unknown(), 'retrieved_at': _unknown(), 'content_evidence_refs': []}))
    source['inquiries'][0].update(seed_artifact_refs=['artifact'], seed_evidence_refs=['e', 'e2'],
                                 coverage_assertion_refs=['cohort'])
    for suffix in ('', '2'):
        source['records'].append(_record('e' + suffix, 'evidence_item', {
            'claim_ref': 'claim' + suffix, 'artifact_ref': 'artifact', 'locator': 'paragraph',
            'epistemic_type': 'fictional_example', 'description': 'One distinct Claim contribution'}))
        source['records'].append(_record('stage' + suffix, 'pipeline_record', {
            'subject_ref': 'e' + suffix, 'run_key': 'shared-run', 'stage_key': 'shared-stage',
            'stage': 'selection', 'state': 'occurred', 'output_refs': ['e' + suffix],
            'observed_at': _unknown(), 'linkage_kind': 'use_record', 'detail': 'Claim-local native observation'}))
    source['assertions'].append(_assessment('cohort', 'coverage', ('stage',), {
        'coverage_kind': 'pipeline_universe', 'state': 'complete_for_scope', 'relation_types': [],
        'dimensions': [], 'member_refs': ['e'], 'omitted_refs': [], 'universe_enumerated': True,
        'scope_note': 'Explicitly one Claim and one member, no second Claim coverage'}))
    out = _analyze(source)
    assert out.execution_state == 'completed'
    assert set(_disclosures(out, 'pipeline_stage_disclosures')) == {'stage', 'stage2'}
    second_rows = [row for row in _rows(out, 'pipeline_stage_disclosures') if row.value is not None
                   and any(item.source.identifier == 'stage2' for item in row.value.records)]
    assert second_rows
    assert all('claim2' in tuple(ref.identifier for ref in row.ref.scope.claim_refs) for row in second_rows)


def test_unrelated_channel_does_not_create_a_route_under_another_inquiry():
    source = _minimal_value()
    source['records'].append(_record('channel', 'correction_channel', {'owner_refs': ['actor'],
        'target_refs': ['claim'], 'contact_locator': 'mailto:inert@example.invalid',
        'declared_action_types': ['review'], 'valid_window': _window()}))
    source['records'].append(_record('other-claim', 'claim', {'claim_key': 'unrelated',
        'version_label': 'v1', 'text': 'Unrelated inquiry target', 'context': 'Separate scope'}))
    other = copy.deepcopy(_minimal_value()['inquiries'][0])
    other.update(id='other-inquiry', target_claim_refs=['other-claim'])
    source['inquiries'].append(other)
    out = _analyze(source)
    assert out.execution_state == 'completed'
    rows = [row for row in out.results if row.ref.diagnostic_id == 'SIT-M011'
            and row.ref.scope.inquiry_ref.identifier == 'other-inquiry']
    assert rows and all(row.result_state in ('unavailable', 'not_applicable') and row.value is None for row in rows)
    assert all(row.reason_refs for row in rows)
    assert all(not row.ref.scope.target_refs for row in rows)
    basis = [row for row in _rows(out, 'declared_basis_inventory')
             if row.ref.scope.inquiry_ref.identifier == 'other-inquiry']
    assert basis
    assert all({ref.identifier for ref in row.value.population.member_refs} ==
               {'other-inquiry', 'other-claim', 'actor'} for row in basis)


@pytest.mark.parametrize('mode', ('value', 'utf8'))
def test_documentary_memberships_and_hhi_preserve_full_two_seed_denominator(mode):
    out = _analyze(_documented_value(), mode)
    assert out.execution_state == 'completed'
    rows = _rows(out, 'per_seed_origin_memberships')
    assert len(rows) == 1 and rows[0].result_state == 'available'
    assert {item.member_ref.identifier: tuple(ref.identifier for ref in item.origin_refs)
            for item in rows[0].value.memberships} == {'e': ('origin',), 'e2': ('origin',)}
    partition = _rows(out, 'seed_origin_dispositions')[0]
    assert next(category.count for category in partition.value.categories
                if category.label == 'single_documented_origin') == 2
    hhi = _rows(out, 'single_origin_contribution_hhi')[0]
    assert hhi.result_state == 'available'
    assert (hhi.value.numerator, hhi.value.denominator) == (4, 4)
    assert tuple(ref.identifier for ref in hhi.value.population.member_refs) == ('e', 'e2')
    assert {'coverage', 'boundary', 'parent-e', 'parent-e2'} <= {
        ref.source.identifier for ref in hhi.basis_refs}
    assert next(check.state for check in hhi.check_refs if check.check_id == 'PC24') == 'met'


def test_native_evaluation_target_keeps_exact_claim_scope_and_reverse_metadata_binding():
    source = _minimal_value(two_claims=True)
    source['inquiries'][0]['dependency_dimensions'] = ['model_ancestry']
    for identifier in ('model', 'model2'):
        source['records'].append(_record(identifier, 'model', {'model_key': identifier,
            'version_label': 'v1', 'family_label': 'same-literal-label', 'provider_ref': 'actor'}))
    source['records'].append(_record('evaluation', 'evaluation', {
        'evaluation_kind': 'judgment', 'target_refs': ['claim2'], 'role_bindings': [
            {'role': 'generator', 'object_ref': 'model', 'evidence_ref_ids': [], 'qualifications': []},
            {'role': 'judge', 'object_ref': 'model2', 'evidence_ref_ids': [], 'qualifications': []}],
        'result_refs': [], 'occurred_at': _unknown(), 'review_contribution': None}))
    # No direct Inquiry target_object_ref: this is the adopted native target
    # binding from Definitions20.2, not an invented new selector.
    out = _analyze(source)
    assert out.execution_state == 'completed'
    first = _rows(out, 'human_contribution_disclosures', claims=('claim',))
    second = _rows(out, 'human_contribution_disclosures', claims=('claim2',))
    assert second
    capability = next(row for row in out.capabilities if row.family == 'SIT-M013')
    assert capability.execution_state == 'completed' and capability.scope_note
    assert all(not any(item.source.identifier == 'evaluation' for item in row.value.records)
               for row in first if row.value is not None)
    assert any(any(item.source.identifier == 'evaluation' for item in row.value.records)
               for row in second if row.value is not None)
    overlaps = _rows(out, 'matching_family_label_count')
    assert overlaps and all(tuple(ref.identifier for ref in row.ref.scope.claim_refs) == ('claim2',)
                            for row in overlaps)
    assert any(row.value is not None and row.value.value == 1 for row in overlaps)
    assert any('evaluation' in {ref.identifier for ref in row.value.population.member_refs}
               for row in _rows(out, 'declared_basis_inventory') if row.value is not None)


@pytest.mark.parametrize('mode', ('value', 'utf8'))
@pytest.mark.parametrize('shape', ('one_claim', 'claim2_assertion'))
def test_native_self_support_cycle_retains_actual_assurance_limitation_and_witness(mode, shape):
    source = _minimal_value(two_claims=shape == 'claim2_assertion')
    if shape == 'one_claim':
        subject, selected_claims = source['records'][1], ('claim',)
    else:
        subject = _assessment('self-assertion', 'classification', ('actor',), {
            'axis': 'sil_governance_layer', 'labels': ['verified'],
            'verification_assessment_refs': [], 'scope_note': 'Self-support cannot authenticate this supplied label.'})
        subject['scope']['claim_refs'] = ['claim2']
        source['assertions'].append(subject)
        selected_claims = ('claim2',)
    subject_id = subject['id']
    subject['provenance'].update(basis_kind='documented_record', evidence_ref_ids=['self-support'])
    source['evidence_references'].append({'id': 'self-support', 'reference_kind': 'record_pointer',
        'availability': 'supplied', 'artifact_ref': None, 'record_ref': subject_id, 'locator': None,
        'excerpt': None, 'provided_by_ref': 'actor', 'attestor_ref': None,
        'scope_note': 'This pointer returns to its own source; it provides no independent support.'})
    assert not any(row['assertion_kind'] == 'relation' for row in source['assertions'])
    out = _analyze(source, mode)
    assert out.execution_state == 'completed'
    findings = [finding for finding in out.findings if finding.condition_code == 'assurance_loop_limitation']
    assert findings and all(finding.observation_kind == 'qualification_gap' for finding in findings)
    assert any({subject_id, 'self-support'} <= {ref.identifier for ref in finding.witness.input_refs}
               for finding in findings)
    assert any(tuple(ref.identifier for ref in finding.scope_ref.claim_refs) == selected_claims
               for finding in findings)

    def atoms(value):
        if type(value) is tuple:
            return tuple(atom for child in value for atom in atoms(child))
        return (value,)

    payloads = [atoms(_semantic(witness)) for finding in findings
                for witness in finding.witness.owner_witnesses]
    assert any('cycle' in payload and subject_id in payload and 'self-support' in payload for payload in payloads)
    assert all(finding.statement and finding.interpretation_limit for finding in findings)
    gaps = _disclosures(out, 'documentary_basis_gap_disclosures')
    assert subject_id in gaps
