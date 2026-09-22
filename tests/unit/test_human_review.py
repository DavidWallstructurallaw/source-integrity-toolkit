# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W08 M013 source oracles: VF049/050, Definitions 10/25.3, Lineage 6.7.

Supplied contribution, scoped procedure qualification and institutional execution
remain separate. Cases use actual admission and original paid M003 comparison.
"""
import copy
from dataclasses import FrozenInstanceError
import importlib.util
from pathlib import Path

import pytest

from source_integrity_toolkit.analysis import human_review as human
from source_integrity_toolkit.analysis import process_comparison as comparison
from source_integrity_toolkit.contracts.execution import _AnalysisAborted
from source_integrity_toolkit.runtime.boundary import _prepare_value
from source_integrity_toolkit.runtime.diagnostics import _SafeDiagnostic
from source_integrity_toolkit.validation.limits import _WitnessLedger

_spec = importlib.util.spec_from_file_location('sit_w08_human_cases', Path(__file__).with_name('test_process_comparison.py'))
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)
FIELDS = ('corrective_independence_disclosures', 'human_contribution_disclosures')
REVIEWS = ('H7-HREVIEW', 'W08-REVIEW2')


def run(source, subjects=('H7-HREVIEW',), dimension='analytical_method'):
    original = copy.deepcopy(source)
    prepared = h.admit(source)
    context = h.context(source, subject_refs=subjects, dependency_dimension=dimension,
                        graph_view='model_evaluation')
    owner, job = h.job_pair()
    ledger = owner.witnesses
    before = owner.used, job.used, ledger._retained_witnesses, ledger._retained_members
    output = human._human_review(prepared, context, ledger, job)
    assert source == original
    assert owner.used - before[0] == job.used - before[1] > 0
    assert output.facts.prepared is prepared and output.facts.context is context
    assert output.facts.job_port is job
    assert ledger._retained_witnesses - before[2] == len(output.witnesses)
    assert ledger._retained_members - before[3] == sum(w.member_count for w in output.witnesses)
    assert tuple(row.ref.field_key for row in output.results) == FIELDS
    for row in output.results:
        assert row.ref.diagnostic_id == 'SIT-M013'
        assert (row.execution_state, row.result_state, row.value_kind, row.result_origin) == (
            'completed', 'available', 'record_disclosures', 'attributed_record')
        scope = row.ref.scope
        assert scope.inquiry_ref.identifier == 'H7-I1'
        assert tuple(ref.identifier for ref in scope.claim_refs) == ('H7-C1',)
        assert scope.dependency_dimension == dimension and scope.temporal_basis == 'snapshot_structural'
        assert tuple(ref.identifier for ref in scope.target_refs) == subjects
        assert row.basis_refs and row.witness_refs and row.interpretation_limit
        assert all(check.result_ref is row.ref for check in row.check_refs)
        assert all(reason.scope is scope and row.ref in reason.affected_result_refs for reason in row.reason_refs)
        assert all(witness.scope is scope for witness in row.witness_refs)
        checks = {check.check_id: check.state for check in row.check_refs}
        assert checks['PC01'] == checks['PC02'] == checks['PC24'] == 'met'
        assert {'PC05', 'PC08', 'PC09', 'PC10', 'PC11', 'PC14', 'PC22'} <= checks.keys()
        for population in row.population_refs:
            assert population.scope is scope
            assert population.membership_state == 'enumerated_for_scope'
            assert population.selection_rule
    return output, prepared, owner, job


def leaf(output, field):
    return next(row for row in output.results if row.ref.field_key == field)


def disclosures(output, field=FIELDS[1]):
    row = leaf(output, field)
    result = {item.source.identifier: h.native(item.fields) for item in row.value.records}
    assert len(result) == len(row.value.records)
    return result


def codes(row):
    return {reason.code for reason in row.reason_refs}


def assert_review(actual, source, identifier='H7-HREVIEW', status='recorded_human_contribution'):
    original = h.cases.by_id(source, identifier)
    row = actual[identifier]
    assert row['data'] == original['data']
    assert row['provenance'] == original['provenance']
    assert row['contribution_status'] == status
    for field in ('gaps', 'extensions'):
        if field in original:
            assert row[field] == original[field]
    return row


def assert_no_independence(actual):
    assert all(row.get('process_qualification_state') != 'met' for row in actual.values())
    assert all('independent_corrective_capacity' not in row for row in actual.values())


def comparison_profile(output):
    assert len(output.facts.comparisons) == 1
    return output.facts.comparisons[0]


def assert_process(output, source, state='available', dimension='analytical_method'):
    profile = comparison_profile(output)
    submitted = h.leaf(profile, 'submitted_comparison_member_count')
    qualified = h.leaf(profile, 'qualified_process_set_member_count')
    origin = h.leaf(profile, 'qualified_origin_set_member_count')
    assert submitted.value.value == 2
    assert tuple(ref.identifier for ref in submitted.value.population.member_refs) == REVIEWS
    assert qualified.result_state == state
    if state == 'available':
        assert qualified.value.value == 2
        assert tuple(ref.identifier for ref in qualified.value.population.member_refs) == REVIEWS
    else:
        assert qualified.value is None and qualified.reason_refs
    assert origin.result_state == 'not_applicable' and origin.value is None
    row = disclosures(output, FIELDS[0])['H7-IND12']
    original = h.cases.by_id(source, 'H7-IND12')
    for key in h.NATIVE_KEYS:
        assert row[key] == original[key]
    assert row['process_qualification_state'] == ('met' if state == 'available' else 'unmet')
    assert qualified.ref.scope.dependency_dimension == dimension
    expected_unexamined = (['acquisition', 'model_ancestry', 'evaluation_rubric', 'organizational_control']
                          if dimension == 'analytical_method' else
                          ['acquisition', 'analytical_method', 'model_ancestry', 'organizational_control'])
    assert row['data']['details']['unexamined_dimensions'] == expected_unexamined
    return row


def method_pair(role='method_input', dimension='analytical_method'):
    """W7-06: separate procedures inspect the same target; other dimensions open."""
    source = h.hero()
    for original, identifier in (('H7-REVIEWER', 'W08-REVIEWER2'),
                                 ('H7-CHECK-METHOD', 'W08-METHOD2'),
                                 ('H7-REVIEW-RESULT', 'W08-RESULT2')):
        row = copy.deepcopy(h.cases.by_id(source, original))
        row['id'] = identifier
        if row['kind'] == 'artifact':
            row['data']['work_key'] = identifier
        source['records'].append(row)
    review = copy.deepcopy(h.cases.by_id(source, 'H7-HREVIEW'))
    review['id'] = REVIEWS[1]
    review['data']['role_bindings'][0]['object_ref'] = 'W08-REVIEWER2'
    review['data']['role_bindings'][1]['object_ref'] = 'W08-METHOD2'
    review['data']['result_refs'] = ['W08-RESULT2']
    review['data']['review_contribution'] = 'Independently checked the same export through the second supplied procedure.'
    source['records'].append(review)
    for identifier in REVIEWS:
        h.cases.by_id(source, identifier)['data']['role_bindings'][1]['role'] = role
    assessment = h.cases.by_id(source, 'H7-IND12')
    assessment['data']['subject_refs'] = list(REVIEWS)
    assessment['data']['details'].update(dimension=dimension, examined_dependency_refs=['H7-COV-COMP'],
        unexamined_dimensions=[value for value in h.DIMENSIONS if value != dimension])
    coverage = h.cases.by_id(source, 'H7-COV-COMP')
    coverage['data']['subject_refs'] = list(REVIEWS)
    coverage['data']['details'].update(dimensions=[dimension], member_refs=list(REVIEWS), relation_types=[])
    h.cases.by_id(source, 'H7-SUP-COMPARE')['excerpt'] = (
        'The two identified human reviewers used separate documented analytical procedures on the same target. '
        'Training, rubric, acquisition and organizational dependencies remain unexamined.'
        if dimension == 'analytical_method' else
        'The two identified human reviewers used distinct supplied rubric/reference-answer procedures on the same target. '
        'Acquisition, analytical method, model training and organizational dependencies remain unexamined.')
    return source


@pytest.fixture(scope='module')
def hero_review():
    source = h.hero()
    return source, run(source)[0]


def test_vf050_positive_actual_human_reasoning_role_method_result_and_corr_basis(hero_review):
    source, output = hero_review
    actual = disclosures(output)
    row = assert_review(actual, source)
    assert row['documentary_state'] == 'met'
    assert row['data']['target_refs'] == ['H7-R1-V1']
    assert row['data']['result_refs'] == ['H7-REVIEW-RESULT']
    assert [(role['role'], role['object_ref']) for role in row['data']['role_bindings']] == [
        ('human_reviewer', 'H7-REVIEWER'), ('method_input', 'H7-CHECK-METHOD')]
    assert row['provenance']['evidence_ref_ids'] == ['H7-SUP-CORR']
    assert 'H7-REVIEWER' in actual and 'H7-CHECK-METHOD' in actual
    mutant = copy.deepcopy(actual)
    mutant['H7-HREVIEW']['data']['review_contribution'] = 'A person merely read the model result.'
    with pytest.raises(AssertionError):
        assert_review(mutant, source)


def test_vf049_missing_assessment_retains_separate_substantive_contribution(hero_review):
    source, output = hero_review
    assert not output.facts.comparisons
    assert 'missing_comparison_assessment' in codes(leaf(output, FIELDS[0]))
    assert_review(disclosures(output), source)
    actual = disclosures(output, FIELDS[0])
    assert_no_independence(actual)
    mutant = copy.deepcopy(actual)
    mutant['H7-HREVIEW']['process_qualification_state'] = 'met'
    with pytest.raises(AssertionError):
        assert_no_independence(mutant)


def test_vf049_positive_original_comparison_is_paid_in_current_job_with_full_population(monkeypatch):
    source = method_pair()
    observed = []
    original = comparison._comparison_profile
    def observe(prepared, context, assessment, ledger, port):
        before = port.used
        result = original(prepared, context, assessment, ledger, port)
        observed.append((prepared, context, assessment, ledger, port, result, port.used - before))
        return result
    monkeypatch.setattr(comparison, '_comparison_profile', observe)
    output, prepared, owner, job = run(source, REVIEWS)
    assert len(observed) == 1
    used_prepared, context, assessment, ledger, port, profile, charged = observed[0]
    assert used_prepared is prepared and ledger is owner.witnesses and port is job and charged > 0
    assert assessment == 'H7-IND12'
    assert profile is comparison_profile(output)
    assert profile.facts.context is context and profile.facts.job_port is job
    for row in output.results:
        links = [w for w in row.witness_refs if w.anchor[0] == 'corrective_comparison']
        originals = profile.results[0].witness_refs
        assert len(links) == len(originals)
        assert {w.anchor[2:] for w in links} == {w.anchor for w in originals}
        assert all(w.anchor[1].identifier == 'H7-IND12' for w in links)
    assert_process(output, source)
    for identifier in REVIEWS:
        assert_review(disclosures(output), source, identifier)
    with pytest.raises(FrozenInstanceError):
        output.facts.comparisons = ()
    # Only the caller's procedure dimension qualifies, not a broad independence unit.
    actual = disclosures(output, FIELDS[0])
    mutant = copy.deepcopy(actual)
    mutant['H7-IND12']['data']['details']['unexamined_dimensions'] = []
    assert actual['H7-IND12']['data'] == h.cases.by_id(source, 'H7-IND12')['data']
    with pytest.raises(AssertionError):
        assert mutant['H7-IND12']['data'] == h.cases.by_id(source, 'H7-IND12')['data']


@pytest.mark.parametrize('metadata', ('human_title', 'different_employer', 'separate_endpoint'))
def test_vf049_negative_identity_metadata_cannot_manufacture_corrective_independence(metadata):
    source = h.hero()
    if metadata == 'human_title':
        h.cases.by_id(source, 'H7-REVIEWER')['data']['display_name'] = 'Independent human safety director'
    elif metadata == 'different_employer':
        reviewer = h.cases.by_id(source, 'H7-REVIEWER')
        reviewer['data']['identity_key'] = 'employee-of-another-organization'
    else:
        h.cases.by_id(source, 'H7-MJUDGE')['data']['model_key'] = 'remote-independent-model-endpoint'
    output, _, _, _ = run(source)
    assert_review(disclosures(output), source)
    actual = disclosures(output, FIELDS[0])
    assert_no_independence(actual)
    assert not output.facts.comparisons
    mutant = copy.deepcopy(actual)
    mutant['H7-HREVIEW']['independent_corrective_capacity'] = 1
    with pytest.raises(AssertionError):
        assert_no_independence(mutant)


@pytest.mark.parametrize('role,dimension', (('method_input', 'analytical_method'),
    ('rubric', 'evaluation_rubric'), ('reference_answer', 'evaluation_rubric')))
def test_vf049_boundary_common_target_survives_and_shared_method_blocks_only_qualification(role, dimension):
    source = method_pair(role, dimension)
    positive, _, _, _ = run(source, REVIEWS, dimension)
    assert_process(positive, source, dimension=dimension)
    actual = disclosures(positive)
    assert all(actual[identifier]['data']['target_refs'] == ['H7-R1-V1'] for identifier in REVIEWS)
    h.cases.by_id(source, REVIEWS[1])['data']['role_bindings'][1]['object_ref'] = 'H7-CHECK-METHOD'
    negative, _, _, _ = run(source, REVIEWS, dimension)
    assert_process(negative, source, 'unavailable', dimension)
    for identifier in REVIEWS:
        assert_review(disclosures(negative), source, identifier)
    assert 'premise_disputed' in codes(h.leaf(comparison_profile(negative), 'qualified_process_set_member_count'))


@pytest.mark.parametrize('dimension', ('model_ancestry', 'evaluation_rubric'))
def test_unexamined_training_and_rubric_dependencies_do_not_erase_method_qualification(dimension):
    source = method_pair()
    for index, identifier in enumerate(REVIEWS):
        role = {'role': 'generator' if dimension == 'model_ancestry' else 'rubric',
                'object_ref': ('H7-MGEN', 'H7-MJUDGE')[index] if dimension == 'model_ancestry' else 'H7-RUBRIC',
                'evidence_ref_ids': ['H7-SUP-MODEL'], 'qualifications': ['Supplied dependency; no whole-review independence.']}
        h.cases.by_id(source, identifier)['data']['role_bindings'].append(role)
    output, _, _, _ = run(source, REVIEWS)
    assert_process(output, source)
    actual = disclosures(output)
    for identifier in REVIEWS:
        row = assert_review(actual, source, identifier)
        assert row['data']['role_bindings'][-1]['role'] == ('generator' if dimension == 'model_ancestry' else 'rubric')
    assert dimension in disclosures(output, FIELDS[0])['H7-IND12']['data']['details']['unexamined_dimensions']
    if dimension == 'model_ancestry':
        for identifier in ('H7-ML03', 'H7-ML04'):
            assert actual[identifier]['data'] == h.cases.by_id(source, identifier)['data']
        assert actual['H7-TRAINING']['data'] == h.cases.by_id(source, 'H7-TRAINING')['data']
    else:
        assert actual['H7-RUBRIC']['data'] == h.cases.by_id(source, 'H7-RUBRIC')['data']


def test_losing_documented_procedure_basis_keeps_both_contributions_without_execution_claim():
    source = method_pair()
    positive, _, _, _ = run(source, REVIEWS)
    assert_process(positive, source)
    h.cases.by_id(source, 'H7-IND12')['provenance'].update(basis_kind='declaration', evidence_ref_ids=[])
    output, _, _, _ = run(source, REVIEWS)
    assert_process(output, source, 'unavailable')
    for identifier in REVIEWS:
        assert_review(disclosures(output), source, identifier)
    assert codes(h.leaf(comparison_profile(output), 'qualified_process_set_member_count')) & {
        'support_uninspectable', 'documentary_basis_incomplete'}
    assert all(h.cases.by_id(source, identifier)['data']['evaluation_kind'] == 'human_review' for identifier in REVIEWS)
    for row in output.results:
        assert 'execution' in row.interpretation_limit.lower()
        assert 'renew' in row.interpretation_limit.lower()


def test_vf050_missing_contribution_with_valid_gap_never_becomes_substantive():
    source = h.hero()
    review = h.cases.by_id(source, 'H7-HREVIEW')
    review['data']['review_contribution'] = None
    review['gaps'] = [{'field': 'data.review_contribution', 'reason': 'not_recorded',
                       'detail': 'A human was named, but their contribution was not recorded.'}]
    output, _, _, _ = run(source)
    actual = disclosures(output)
    assert_review(actual, source, status='missing_contribution')
    mutant = copy.deepcopy(actual)
    mutant['H7-HREVIEW']['contribution_status'] = 'recorded_human_contribution'
    with pytest.raises(AssertionError):
        assert_review(mutant, source, status='missing_contribution')


@pytest.mark.parametrize('kind', ('software_agent', 'organization'))
def test_vf050_negative_nonhuman_reviewer_binding_is_rejected_after_valid_baseline(kind):
    source = h.hero()
    output, _, _, _ = run(source)
    assert_review(disclosures(output), source)
    h.cases.by_id(source, 'H7-REVIEWER')['data']['actor_kind'] = kind
    rejected = _prepare_value(source)
    assert type(rejected) is _SafeDiagnostic
    assert (rejected.input_state, rejected.execution_state, rejected.code) == (
        'rejected', 'rejected', 'endpoint_or_claim_mismatch')


@pytest.mark.parametrize('form', ('protected_actor', 'unresolved_actor'))
def test_vf050_boundary_protected_human_attestation_preserves_contribution_and_limits(form):
    source = h.hero()
    actor = h.cases.by_id(source, 'H7-REVIEWER')
    if form == 'protected_actor':
        actor['data'].update(identity_disclosure='protected', display_name=None)
        actor['gaps'] = [{'field': 'data.display_name', 'reason': 'withheld', 'detail': 'Protected human reviewer.'}]
    else:
        actor['kind'] = 'unresolved_reference'
        actor['data'] = {'expected_kinds': ['actor'], 'reason': 'withheld',
                         'description': 'Protected human reviewer attested in the supplied record.',
                         'protected_key': 'protected-reviewer-one'}
    support = h.cases.by_id(source, 'H7-SUP-CORR')
    support.update(reference_kind='protected_attestation', attestor_ref='H7-PREP',
                   excerpt='A supplied attestation records the human contribution; training and prior-model exposure are unresolved.')
    h.cases.by_id(source, 'H7-HREVIEW')['provenance']['basis_kind'] = 'protected_attestation'
    output, _, _, _ = run(source)
    actual = disclosures(output)
    row = assert_review(actual, source)
    assert row['provenance']['basis_kind'] == 'protected_attestation'
    assert actual['H7-REVIEWER']['data'] == actor['data']
    assert 'missing_comparison_assessment' in codes(leaf(output, FIELDS[0]))
    assert_no_independence(disclosures(output, FIELDS[0]))
    for result in output.results:
        assert 'renew' in result.interpretation_limit.lower()
    mutant = copy.deepcopy(actual)
    mutant['H7-HREVIEW']['provenance']['basis_kind'] = 'documented_record'
    with pytest.raises(AssertionError):
        assert_review(mutant, source)


@pytest.mark.parametrize('kind', ('formal_check', 'execution'))
def test_formal_or_execution_constraint_remains_distinct_from_human_judgment(kind):
    source = h.hero()
    review = h.cases.by_id(source, 'H7-HREVIEW')
    review['data'].update(evaluation_kind=kind, review_contribution=None)
    review['data']['role_bindings'] = [{'role': 'executor', 'object_ref': 'H7-MJUDGE',
        'evidence_ref_ids': ['H7-SUP-MODEL'], 'qualifications': ['Supplied type-appropriate constraint.']}]
    output, _, _, _ = run(source)
    actual = disclosures(output)
    assert_review(actual, source, status='distinct_constraint')
    mutant = copy.deepcopy(actual)
    mutant['H7-HREVIEW']['contribution_status'] = 'recorded_human_contribution'
    with pytest.raises(AssertionError):
        assert_review(mutant, source, status='distinct_constraint')


def test_model_judgment_later_read_by_human_is_not_a_recorded_human_contribution():
    source = h.hero()
    h.cases.by_id(source, 'H7-EVAL')['provenance']['qualifications'].append('A person later read this model-generated text.')
    output, _, _, _ = run(source, ('H7-EVAL',))
    actual = disclosures(output)
    assert_review(actual, source, 'H7-EVAL', status='no_human_role')
    assert 'H7-HREVIEW' not in actual
    assert_no_independence(disclosures(output, FIELDS[0]))


def test_selected_review_keeps_entire_actual_comparison_without_importing_other_review_contribution():
    source = method_pair()
    output, _, _, _ = run(source)
    assert_process(output, source)
    actual = disclosures(output)
    assert_review(actual, source)
    assert REVIEWS[1] not in actual
    assert tuple(review.evaluation.identifier for review in output.facts.reviews) == ('H7-HREVIEW',)


def test_owner_rejects_foreign_ledgers_stale_facts_and_sticky_exhaustion():
    source = h.hero()
    output, prepared, owner, job = run(source)
    context = output.facts.context
    other, _ = h.job_pair()
    for ledger in (other.witnesses, _WitnessLedger(owner.witnesses.port)):
        with pytest.raises(TypeError):
            human._human_review(prepared, context, ledger, job)
    owner.finish_job(job)
    next_job = owner.start_job()
    with pytest.raises(TypeError):
        human._human_review_results(output.facts, next_job)
    next_job.charge(1_000_000 - next_job.used)
    used = owner.used, next_job.used
    with pytest.raises(_AnalysisAborted) as first:
        human._human_review(prepared, context, owner.witnesses, next_job)
    assert first.value.limit_id == 'WU9-L11'
    assert (owner.used, next_job.used) == used
    with pytest.raises(_AnalysisAborted) as repeated:
        human._human_review(prepared, context, owner.witnesses, next_job)
    assert repeated.value is first.value


def test_missing_human_role_keeps_method_record_and_reports_unknown_applicable_roles():
    source = h.hero()
    review = h.cases.by_id(source, 'H7-HREVIEW')
    review['data']['role_bindings'] = [review['data']['role_bindings'][1]]
    output, _, _, _ = run(source)
    actual = disclosures(output)
    assert_review(actual, source, status='no_human_role')
    assert actual['H7-HREVIEW']['data']['role_bindings'][0]['role'] == 'method_input'
    for row in output.results:
        assert next(check.state for check in row.check_refs if check.check_id == 'PC14') == 'unknown'
    mutant = copy.deepcopy(actual)
    mutant['H7-HREVIEW']['contribution_status'] = 'recorded_human_contribution'
    with pytest.raises(AssertionError):
        assert_review(mutant, source, status='no_human_role')


def test_two_actual_assessments_keep_each_own_qualification_when_one_cites_the_other():
    source = method_pair()
    first = h.cases.by_id(source, 'H7-IND12')
    other = copy.deepcopy(first)
    other['id'] = 'W08-IND-UNKNOWN'
    other['data']['details']['conclusion'] = 'unknown'
    source['assertions'].append(other)
    first['data']['details']['examined_dependency_refs'].append(other['id'])
    output, _, _, _ = run(source, REVIEWS)
    assert len(output.facts.comparisons) == 2
    actual = disclosures(output, FIELDS[0])
    assert actual['H7-IND12']['process_qualification_state'] == 'met'
    assert actual[other['id']]['process_qualification_state'] == 'unmet'
    for identifier in ('H7-IND12', other['id']):
        assert actual[identifier]['data'] == h.cases.by_id(source, identifier)['data']
    mutant = copy.deepcopy(actual)
    mutant[other['id']]['process_qualification_state'] = 'met'
    with pytest.raises(AssertionError):
        assert mutant[other['id']]['process_qualification_state'] == 'unmet'


@pytest.mark.parametrize('role,dimension', (('method_input', 'analytical_method'),
    ('rubric', 'evaluation_rubric'), ('reference_answer', 'evaluation_rubric')))
def test_native_role_time_unknown_withholds_comparison_and_its_temporal_prerequisite(role, dimension):
    """Definitions20.5/PC10: native unknown time cannot inherit Assertion time."""
    source = method_pair(role, dimension)
    for identifier in REVIEWS:
        h.cases.by_id(source, identifier)['data']['occurred_at'] = h.cases.unknown()
    snapshot, _, _, snapshot_job = h.run(source, dependency_dimension=dimension,
        subject_refs=REVIEWS, graph_view='model_evaluation')
    qualified = h.leaf(snapshot, 'qualified_process_set_member_count')
    h.assert_count(qualified, REVIEWS, dimension=dimension)
    assert snapshot.facts.job_port is snapshot_job
    assert next(check.state for check in qualified.check_refs if check.check_id == 'PC10') == 'met'
    timed, prepared, owner, job = h.run(source, dependency_dimension=dimension,
        subject_refs=REVIEWS, graph_view='model_evaluation', temporal_basis='time_specific',
        requested_time=h.requested('2026-01-10T13:00:00Z'))
    assert timed.facts.prepared is prepared and timed.facts.job_port is job
    assert job.used > 0 and owner.witnesses._retained_witnesses == len(timed.witnesses)
    qualified = h.leaf(timed, 'qualified_process_set_member_count')
    assert (qualified.execution_state, qualified.result_state, qualified.value) == ('completed', 'unavailable', None)
    assert qualified.ref.scope.temporal_basis == 'time_specific'
    assert 'time_applicability_unknown' in codes(qualified)
    pc10 = next(check for check in qualified.check_refs if check.check_id == 'PC10')
    assert pc10.result_ref is qualified.ref and pc10.state == 'unknown'
    actual_sources = {(ref.collection, ref.identifier, ref.selector) for ref in pc10.input_refs}
    expected_sources = {('records', identifier, 'data.role_bindings[role=' + role + '].object_ref')
                        for identifier in REVIEWS}
    assert expected_sources <= actual_sources
    observations = [edge for reach in timed.facts.reaches for edge in reach.observations
                    if edge.source_ref.record_id in REVIEWS and
                    edge.source_ref.selector == 'data.role_bindings[role=' + role + '].object_ref']
    assert {edge.source_ref.record_id for edge in observations} == set(REVIEWS)
    assert all(not edge.eligible and 'time_applicability_unknown' in edge.reason_codes for edge in observations)
    # The native observation is the missing temporal premise; both supplied
    # Assertion windows still qualify independently in this requested instant.
    for identifier in ('H7-IND12', 'H7-COV-COMP'):
        premises = [premise for premise in timed.facts.premises if premise.source.identifier == identifier]
        assert premises and all(premise.time.state == 'met' for premise in premises)
    actual_state = {'pc10': pc10.state, 'qualified_state': qualified.result_state}
    assert actual_state == {'pc10': 'unknown', 'qualified_state': 'unavailable'}
    mutant = dict(actual_state, pc10='met')
    with pytest.raises(AssertionError):
        assert mutant == {'pc10': 'unknown', 'qualified_state': 'unavailable'}
