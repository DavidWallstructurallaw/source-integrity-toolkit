# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W11 independent M012 source oracles, Definitions 27.2/27.3 and VF041--048.

Literal H7 event identities and small hand-authored process logs determine the
five inventories. Neither native acceptance nor an unlinked later version is
a documented correction. Tests use the actual admission and paid owner seam.
"""
import copy
from dataclasses import FrozenInstanceError, replace
import importlib.util
from pathlib import Path

import pytest

from source_integrity_toolkit.analysis import correction_outcomes as outcomes
from source_integrity_toolkit.contracts import results
from source_integrity_toolkit.contracts.execution import _AnalysisAborted
from source_integrity_toolkit.runtime import resources
from source_integrity_toolkit.validation.limits import _WitnessLedger

_spec = importlib.util.spec_from_file_location(
    'sit_w11_correction_helpers', Path(__file__).with_name('test_process_comparison.py'))
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)
FIELDS = ('correction_case_record_count', 'handling_event_record_count',
          'linked_change_event_record_count', 'documentary_linked_change_target_count',
          'cases_with_documentary_linked_change_count', 'correction_case_disclosures',
          'correction_target_change_disclosures', 'reported_capacity_disclosures')
H7_PAIRS = (('H7-CASE1', 'H7-A'), ('H7-CASE1', 'H7-D'), ('H7-CASE1', 'H7-R1-V1'))


def supported(row):
    row['provenance'].update(basis_kind='documented_record', evidence_ref_ids=['support'],
        method='Read the supplied finite fictional process log for these exact records.',
        qualifications=['Attributed documentary process evidence without substantive verification.'])
    return row


def small():
    source = h.cases.pool()
    for row in source['records']:
        if row['kind'] == 'correction_event':
            supported(row)
    return source


def remove_events(source, *kinds):
    source['records'] = [row for row in source['records'] if not (
        row['kind'] == 'correction_event' and row['data']['event_kind'] in kinds)]
    return source


def duplicate(source, identifier, new_id):
    row = copy.deepcopy(h.cases.by_id(source, identifier))
    row['id'] = new_id
    source['assertions' if 'assertion_kind' in row else 'records'].append(row)
    return row


def context(source, subjects=None, **changes):
    if subjects is None:
        subjects = ('H7-CASE1',) if source['inquiries'][0]['id'] == 'H7-I1' else ('submission',)
    options = dict(subject_refs=subjects, dependency_dimension=None,
        graph_view='correction_outcomes', coverage_kind=None, relation_types=(),
        operation_anchor=(), temporal_basis='snapshot_structural', requested_time=None)
    options.update(changes)
    return h.context(source, **options)


def run(source, *, subjects=None, selected_targets=None, **changes):
    original = copy.deepcopy(source)
    prepared = h.admit(source)
    ctx = context(source, subjects, **changes)
    owner, job = h.job_pair()
    ledger = owner.witnesses
    before = owner.used, job.used, ledger._retained_witnesses, ledger._retained_members
    out = outcomes._correction_outcomes(prepared, ctx, ledger, job, selected_targets=selected_targets)
    assert source == original
    assert out.facts.prepared is prepared and out.facts.context is ctx and out.facts.job_port is job
    assert owner.used - before[0] == job.used - before[1] > 0
    assert ledger._retained_witnesses - before[2] == len(out.witnesses)
    assert ledger._retained_members - before[3] == sum(w.member_count for w in out.witnesses)
    assert tuple(row.ref.field_key for row in out.results) == FIELDS
    for row in out.results:
        assert row.ref.diagnostic_id == 'SIT-M012'
        assert row.execution_state == 'completed'
        scope = row.ref.scope
        assert scope.inquiry_ref.identifier == ctx.inquiry_ref
        assert tuple(ref.identifier for ref in scope.claim_refs) == ctx.claim_refs
        assert scope.graph_view == 'correction_outcomes'
        assert row.basis_refs and row.interpretation_limit
        assert all(check.result_ref is row.ref for check in row.check_refs)
        assert all(reason.scope is scope and row.ref in reason.affected_result_refs for reason in row.reason_refs)
        assert all(witness.scope is scope for witness in row.witness_refs)
        checks = {check.check_id: check.state for check in row.check_refs}
        assert checks['PC01'] == checks['PC02'] == checks['PC24'] == 'met'
        assert 'PC21' in checks
    return out, prepared, owner, job


def leaf(out, field):
    return next(row for row in out.results if row.ref.field_key == field)


def assert_counts(out, expected):
    actual = []
    for field in FIELDS[:5]:
        row = leaf(out, field)
        assert (row.execution_state, row.result_state, row.value_kind) == ('completed', 'available', 'count')
        assert row.value.population in row.population_refs
        assert row.value.population.membership_state == 'enumerated_for_scope'
        assert row.value.population.scope is row.ref.scope
        assert row.value.value == len(row.value.population.member_refs)
        actual.append(row.value.value)
    assert tuple(actual) == expected


def pairs(out):
    row = leaf(out, FIELDS[3])
    assert row.value.population.unit == 'case_target'
    return tuple((item.case_ref.identifier, item.before_ref.identifier)
                 for item in row.value.population.member_refs)


def disclosures(out, field=FIELDS[5]):
    row = leaf(out, field)
    assert (row.result_state, row.value_kind) == ('available', 'record_disclosures')
    payload = {item.source.identifier: h.native(item.fields) for item in row.value.records}
    assert len(payload) == len(row.value.records)
    return payload


def assert_native(out, source, identifiers, field=FIELDS[5]):
    payload = disclosures(out, field)
    for identifier in identifiers:
        original = h.cases.by_id(source, identifier)
        actual = payload[identifier]['native_record']
        for key in h.NATIVE_KEYS if 'assertion_kind' in original else ('data', 'provenance'):
            assert actual[key] == original[key]
        for key in ('gaps', 'extensions'):
            if key in original:
                assert actual[key] == original[key]
    return payload


def target_row(out, target='claim', case='submission'):
    candidates = disclosures(out, FIELDS[6])[target]['case_rows']
    return next(row for row in candidates if row['case_ref'] == case)


def assert_effect(out, target='claim', case='submission', *, available=True):
    row = target_row(out, target, case)
    assert row['requested_effect_state'] == ('available' if available else 'unavailable')
    if available:
        assert row['documentary_state'] == 'met'
        assert row['qualified_change_event_refs']
    else:
        assert row['documentary_state'] != 'met'
        assert not row['qualified_change_event_refs']
        assert 'change_evidence_missing' in row['reason_codes']
    return row


@pytest.fixture(scope='module')
def hero_profile():
    source = h.hero()
    return source, run(source)[0]


def test_vf041_p_h7_submission_is_one_case(hero_profile):
    source, out = hero_profile
    assert_counts(out, (1, 1, 3, 3, 1))
    assert tuple(ref.identifier for ref in leaf(out, FIELDS[0]).value.population.member_refs) == ('H7-CASE1',)


def test_vf041_n_handling_and_changes_cannot_be_counted_as_submissions(hero_profile):
    source, out = hero_profile
    row = leaf(out, FIELDS[0])
    names = ('H7-CASE1', 'H7-HAND1', 'H7-CHANGE-A', 'H7-CHANGE-D', 'H7-CHANGE-R1')
    population = replace(row.value.population, member_refs=tuple(results._InputRef('records', name) for name in names))
    mutant = replace(row, value=results._Count(5, population), population_refs=(population,))
    corrupted = replace(out, results=(mutant,) + out.results[1:])
    with pytest.raises(AssertionError):
        assert_counts(corrupted, (1, 1, 3, 3, 1))


def test_vf041_m_empty_finite_case_inventory_is_available_zero():
    out = run(remove_events(small(), 'submission', 'handling', 'change'), subjects=())[0]
    assert_counts(out, (0, 0, 0, 0, 0))
    assert not disclosures(out, FIELDS[7])
    assert 'capacity' in leaf(out, FIELDS[0]).interpretation_limit.lower()


def test_vf041_b_separate_submissions_to_same_target_remain_two_cases():
    source = small()
    duplicate(source, 'submission', 'submission2')
    out = run(source, subjects=('submission', 'submission2'))[0]
    assert_counts(out, (2, 1, 1, 1, 1))


def test_vf042_p_h7_handling_is_exact_native_record(hero_profile):
    source, out = hero_profile
    assert_counts(out, (1, 1, 3, 3, 1))
    assert_native(out, source, ('H7-HAND1',))


def test_vf042_n_accepted_and_later_failed_are_two_handling_events():
    source = small()
    failed = duplicate(source, 'handling', 'handling-failed')
    failed['data']['details'].update(outcome='failed', reason='Native process failure after acceptance.')
    failed['data']['occurred_at'] = {'state': 'known', 'value': '2026-01-10T15:00:00Z', 'precision': 'instant'}
    out = run(source)[0]
    assert_counts(out, (1, 2, 1, 1, 1))
    assert_native(out, source, ('handling', 'handling-failed'))


def test_vf042_m_no_handling_records_does_not_infer_neglect():
    source = remove_events(small(), 'handling')
    out = run(source)[0]
    assert_counts(out, (1, 0, 1, 1, 1))
    assert 'neglect' not in str(disclosures(out)).lower()


def test_vf042_b_repeated_outcome_values_keep_distinct_event_ids():
    source = small()
    duplicate(source, 'handling', 'handling2')
    out = run(source)[0]
    assert_counts(out, (1, 2, 1, 1, 1))
    assert_native(out, source, ('handling', 'handling2'))


def test_vf043_p_h7_three_exact_linked_event_ids(hero_profile):
    source, out = hero_profile
    assert tuple(ref.identifier for ref in leaf(out, FIELDS[2]).value.population.member_refs) == (
        'H7-CHANGE-A', 'H7-CHANGE-D', 'H7-CHANGE-R1')
    assert_native(out, source, ('H7-CHANGE-A', 'H7-CHANGE-D', 'H7-CHANGE-R1'))


def test_vf043_n_acceptance_and_unlinked_later_version_do_not_create_change():
    source = remove_events(small(), 'change')
    later = duplicate(source, 'claim2', 'claim3')
    later['data']['version_label'] = 'v3'
    source['assertions'].append(h.cases.relation('supersedes'))
    out = run(source)[0]
    assert_counts(out, (1, 1, 0, 0, 0))
    assert_effect(out, available=False)


def test_vf043_m_zero_event_inventory_and_unavailable_effect_are_distinct():
    out = run(remove_events(small(), 'change'))[0]
    assert_counts(out, (1, 1, 0, 0, 0))
    row = assert_effect(out, available=False)
    assert row['change_event_refs'] == []


def test_vf043_b_two_event_ids_on_one_pair_count_two_events_one_target():
    source = small()
    duplicate(source, 'change', 'change2')
    out = run(source)[0]
    assert_counts(out, (1, 1, 2, 1, 1))
    assert pairs(out) == (('submission', 'claim'),)


def test_vf044_p_h7_three_documentary_case_target_pairs(hero_profile):
    source, out = hero_profile
    assert pairs(out) == H7_PAIRS
    for target in ('H7-A', 'H7-D', 'H7-R1-V1'):
        assert_effect(out, target, 'H7-CASE1')


def test_vf044_n_linkage_description_without_documentary_basis_stays_event():
    control = small()
    h.cases.by_id(control, 'submission')['provenance'].update(basis_kind='declaration', evidence_ref_ids=[])
    qualified = run(control)[0]
    assert_counts(qualified, (1, 1, 1, 1, 1))
    for field in (FIELDS[3], FIELDS[4], FIELDS[6]):
        checks = {check.check_id: check for check in leaf(qualified, field).check_refs}
        assert checks['PC05'].state == 'met'
        assert {ref.identifier for ref in checks['PC05'].input_refs} == {'change'}
    source = small()
    change = h.cases.by_id(source, 'change')
    change['provenance'].update(basis_kind='declaration', evidence_ref_ids=[])
    out = run(source)[0]
    assert_counts(out, (1, 1, 1, 0, 0))
    assert_effect(out, available=False)


@pytest.mark.parametrize('endpoint', ('before', 'after'))
def test_vf044_m_unresolved_endpoint_does_not_qualify_documentary_target(endpoint):
    source = small()
    change = h.cases.by_id(source, 'change')['data']
    change['details'][endpoint + '_ref'] = 'unresolved'
    if endpoint == 'before':
        change['target_refs'] = ['unresolved']
        h.cases.by_id(source, 'submission')['data']['target_refs'].append('unresolved')
    out = run(source)[0]
    assert_counts(out, (1, 1, 1, 0, 0))
    row = assert_effect(out, 'unresolved' if endpoint == 'before' else 'claim', available=False)
    assert 'before_after_unresolved' in row['reason_codes']


def test_vf044_b_supported_explicit_removal_needs_no_invented_after_artifact():
    source = small()
    h.cases.by_id(source, 'change')['data']['details'].update(action_type='retract', after_ref=None,
        after_absence_reason='The supplied process log documents removal of this exact target.')
    duplicate(source, 'change', 'change2')
    out = run(source)[0]
    assert_counts(out, (1, 1, 2, 1, 1))
    assert_effect(out)


def test_vf045_p_h7_three_changed_targets_belong_to_one_case(hero_profile):
    source, out = hero_profile
    assert tuple(ref.identifier for ref in leaf(out, FIELDS[4]).value.population.member_refs) == ('H7-CASE1',)


def test_vf045_n_case_count_cannot_be_replaced_with_changed_target_count(hero_profile):
    source, out = hero_profile
    assert leaf(out, FIELDS[4]).value.value == 1
    assert leaf(out, FIELDS[3]).value.value == 3


def test_vf045_m_accepted_without_documentary_change_has_zero_qualifying_cases():
    source = remove_events(small(), 'change')
    out = run(source)[0]
    assert_counts(out, (1, 1, 0, 0, 0))
    assert_native(out, source, ('handling',))
    assert_effect(out, available=False)


def test_vf045_b_two_cases_changing_same_target_are_two_case_target_pairs():
    source = small()
    duplicate(source, 'submission', 'submission2')
    duplicate(source, 'change', 'change2')['data']['case_ref'] = 'submission2'
    out = run(source, subjects=('submission', 'submission2'))[0]
    assert_counts(out, (2, 1, 2, 2, 2))
    assert pairs(out) == (('submission', 'claim'), ('submission2', 'claim'))


def test_vf046_p_native_proposal_and_handling_provenance_survive(hero_profile):
    source, out = hero_profile
    assert_native(out, source, ('H7-CASE1', 'H7-HAND1'))


def test_vf046_n_native_failed_remains_available_without_newest_wins():
    source = small()
    duplicate(source, 'handling', 'later-failed')['data']['details']['outcome'] = 'failed'
    out = run(source)[0]
    payload = assert_native(out, source, ('handling', 'later-failed'))
    assert {payload[name]['native_record']['data']['details']['outcome']
            for name in ('handling', 'later-failed')} == {'accepted', 'failed'}
    assert all(row.execution_state == 'completed' for row in out.results)
    assert 'correction_success_rate' not in payload
    assert 'final_outcome' not in payload['submission']


def test_vf046_m_negative_review_observation_keeps_its_cutoff_and_basis():
    source = remove_events(small(), 'change')
    review = h.cases.by_id(source, 'evaluation')
    review['data'].update(evaluation_kind='empirical_review', target_refs=['claim'],
        occurred_at={'state': 'known', 'value': '2026-01-10T17:00:00Z', 'precision': 'instant'},
        review_contribution='Inspected this exact target at the stated cutoff; no amendment was observed.')
    supported(review)
    h.cases.by_id(source, 'support')['excerpt'] = (
        'Fictional observation at 2026-01-10T17:00:00Z: the named target was inspected and no amendment was observed.')
    out = run(source)[0]
    assert_counts(out, (1, 1, 0, 0, 0))
    assert_native(out, source, ('evaluation',))
    assert_effect(out, available=False)


def test_vf046_b_reasoned_rejection_is_handling_without_truth_verdict():
    source = remove_events(small(), 'change')
    h.cases.by_id(source, 'handling')['data']['details'].update(outcome='rejected',
        reason='The supplied service disputes the requested amendment; no truth adjudication is supplied.')
    out = run(source)[0]
    assert_counts(out, (1, 1, 0, 0, 0))
    assert_native(out, source, ('handling',))
    assert_effect(out, available=False)


def test_vf047_p_h7_downstream_subset_keeps_whole_case_inventory_distinct():
    out = run(h.hero(), selected_targets=('H7-A', 'H7-D', 'H7-E'))[0]
    assert_counts(out, (1, 1, 3, 3, 1))
    for target in ('H7-A', 'H7-D'):
        assert assert_effect(out, target, 'H7-CASE1')['selected'] is True
    assert assert_effect(out, 'H7-E', 'H7-CASE1', available=False)['selected'] is True
    assert target_row(out, 'H7-R1-V1', 'H7-CASE1')['selected'] is False


def test_vf047_n_undocumented_target_is_not_failed_and_unlisted_targets_are_not_added(hero_profile):
    source, out = hero_profile
    payload = disclosures(out, FIELDS[6])
    assert set(payload) == {'H7-R1-V1', 'H7-A', 'H7-D', 'H7-E'}
    row = assert_effect(out, 'H7-E', 'H7-CASE1', available=False)
    assert 'failed' not in str(row)


def test_vf047_m_missing_effect_remains_unavailable_without_event_invention():
    out = run(remove_events(small(), 'change'))[0]
    assert_effect(out, available=False)
    assert pairs(out) == ()
    assert leaf(out, FIELDS[2]).value.value == 0


@pytest.mark.parametrize('authority', ('missing', 'review_only', 'unknown'))
def test_vf047_b_documented_change_survives_separate_authority_gaps(authority):
    source = h.hero()
    if authority == 'missing':
        source['assertions'] = [row for row in source['assertions'] if row['id'] != 'H7-AUTH']
    else:
        details = h.cases.by_id(source, 'H7-AUTH')['data']['details']
        if authority == 'review_only':
            details['action_types'] = ['review']
        else:
            details['grant_state'] = 'unknown'
    out = run(source)[0]
    assert_counts(out, (1, 1, 3, 3, 1))
    assert pairs(out) == H7_PAIRS


def capacity(source, identifier='capacity', *, value='10 cases/day', unit='cases/day', load='7 cases/day'):
    row = h.cases.assertion(identifier, 'assessment', {'assessment_kind': 'capacity',
        'subject_refs': ['channel'], 'details': {'reported_capacity': value, 'unit': unit,
            'horizon': h.cases.window(), 'reported_load': load,
            'scope_note': 'External reported strings in their stated horizon; no local capacity model.'}})
    source['assertions'].append(supported(row))
    return row


def test_vf048_p_capacity_strings_horizon_assessor_and_limits_are_exact():
    source = small()
    capacity(source)
    out = run(source)[0]
    actual = assert_native(out, source, ('capacity',), FIELDS[7])
    assert actual['capacity']['native_record']['data']['details']['reported_capacity'] == '10 cases/day'


def test_vf048_n_capacity_and_load_are_never_parsed_into_utilization():
    source = small()
    row = capacity(source, value='010 cases/day; unvalidated', load='7 or 8 cases/day')
    row['provenance'].update(basis_kind='declaration', evidence_ref_ids=[])
    out = run(source)[0]
    actual = assert_native(out, source, ('capacity',), FIELDS[7])
    assert not {'utilization', 'adequacy', 'capacity_estimate', 'correction_success_rate'} & set(actual['capacity'])
    assert_counts(out, (1, 1, 1, 1, 1))


def test_vf048_m_empty_capacity_inventory_does_not_mean_zero_capacity(hero_profile):
    source, out = hero_profile
    row = leaf(out, FIELDS[7])
    assert row.result_state == 'available' and row.value_kind == 'record_disclosures'
    assert row.value.records == ()
    assert 'capacity' in row.interpretation_limit.lower()
    independent = remove_events(small(), 'submission', 'handling', 'change')
    assessment = capacity(independent)
    assessment['data']['subject_refs'] = ['evaluation']
    out = run(independent, subjects=())[0]
    assert_counts(out, (0, 0, 0, 0, 0))
    assert_native(out, independent, ('capacity',), FIELDS[7])


def test_vf048_b_withheld_strings_and_incompatible_units_remain_separate():
    source = small()
    first = capacity(source, value=None, unit=None, load=None)
    first['gaps'] = [{'field': 'data.details.' + name, 'reason': 'withheld',
        'detail': 'The external assessor withheld this string.'}
        for name in ('reported_capacity', 'unit', 'reported_load')]
    other = capacity(source, 'capacity-other', value='twenty per quarter', unit='appeals/quarter', load='unmeasured')
    other['data']['details']['horizon']['start'] = {
        'state': 'known', 'value': '2026-01-01', 'precision': 'date'}
    out = run(source)[0]
    actual = assert_native(out, source, ('capacity', 'capacity-other'), FIELDS[7])
    assert set(actual) == {'capacity', 'capacity-other'}
    assert actual['capacity']['native_record']['data']['details']['reported_capacity'] is None


def test_protected_resolved_artifact_identity_remains_documentary():
    source = small()
    source['inquiries'][0]['target_object_refs'] = ['artifact']
    for key, identifier in (('before_ref', 'artifact'), ('after_ref', 'artifact2')):
        item = h.cases.by_id(source, identifier)
        item['data'].update(work_key='opaque-family', version_label='opaque-' + identifier,
            locators=[], content_evidence_refs=[])
        item['gaps'] = [{'field': 'data.locators', 'reason': 'withheld',
            'detail': 'Public location is withheld; this resolved opaque record keeps exact identity.'}]
        h.cases.by_id(source, 'change')['data']['details'][key] = identifier
    h.cases.by_id(source, 'change')['data']['target_refs'] = ['artifact']
    h.cases.by_id(source, 'submission')['data']['target_refs'] = ['artifact']
    out = run(source)[0]
    assert_counts(out, (1, 1, 1, 1, 1))
    assert pairs(out) == (('submission', 'artifact'),)
    assert_effect(out, 'artifact')


def test_extra_linked_target_is_disclosed_without_enlarging_original_declaration():
    source = small()
    extra = duplicate(source, 'change', 'extra-change')
    extra['data']['target_refs'] = ['artifact']
    extra['data']['details'].update(before_ref='artifact', after_ref='artifact2')
    out = run(source)[0]
    assert_counts(out, (1, 1, 2, 2, 1))
    row = assert_effect(out, 'artifact')
    assert row['declared'] is False and row['selected'] is False
    actual = assert_native(out, source, ('submission',))
    assert actual['submission']['native_record']['data']['target_refs'] == ['claim']


def test_withheld_documentary_support_preserves_event_without_stronger_target():
    source = small()
    h.cases.by_id(source, 'support').update(reference_kind='external_locator', availability='withheld',
        excerpt=None, locator='https://example.invalid/withheld-process-log')
    out = run(source)[0]
    assert_counts(out, (1, 1, 1, 0, 0))
    assert_effect(out, available=False)


def test_supported_assertion_target_preserves_legal_case_target_collection():
    """Lineage 6.8/6.9 allows Assertion targets, including exact before/after."""
    source = small()
    before = supported(h.cases.relation('supersedes'))
    before['id'] = 'assertion-before'
    source['assertions'].append(before)
    after = duplicate(source, 'assertion-before', 'assertion-after')
    after['data']['details']['reason'] = 'The supplied correction updates this exact succession assertion.'
    h.cases.by_id(source, 'submission')['data']['target_refs'] = ['claim', 'assertion-before']
    change = h.cases.by_id(source, 'change')['data']
    change['target_refs'] = ['assertion-before']
    change['details'].update(before_ref='assertion-before', after_ref='assertion-after',
                            action_type='metadata_correction')
    out = run(source)[0]
    assert_counts(out, (1, 1, 1, 1, 1))
    assert pairs(out) == (('submission', 'assertion-before'),)
    pair = leaf(out, FIELDS[3]).value.population.member_refs[0]
    assert pair.before_ref.collection == 'assertions'
    assert_effect(out, 'assertion-before')
    for collection in ('inquiries', 'evidence_references'):
        with pytest.raises(TypeError):
            results._CaseTarget(results._InputRef('records', 'submission'),
                                results._InputRef(collection, 'not-a-correction-target'))
    with pytest.raises(TypeError):
        results._CaseTarget(results._InputRef('assertions', 'not-a-submission'),
                            results._InputRef('records', 'claim'))


def test_reordered_input_records_preserve_case_target_oracle():
    source = h.hero()
    source['records'].reverse()
    source['assertions'].reverse()
    out = run(source)[0]
    assert_counts(out, (1, 1, 3, 3, 1))
    assert pairs(out) == H7_PAIRS


def test_automatic_case_selection_excludes_unrelated_submission_and_children():
    source = small()
    other = duplicate(source, 'submission', 'unrelated-case')
    other['data']['target_refs'] = ['claim2']
    for old, new in (('handling', 'unrelated-handling'), ('change', 'unrelated-change')):
        row = duplicate(source, old, new)
        row['data'].update(case_ref='unrelated-case', target_refs=['claim2'])
        if old == 'change':
            row['data']['details'].update(before_ref='claim2', after_ref='claim')
    out = run(source, subjects=())[0]
    assert_counts(out, (1, 1, 1, 1, 1))
    assert tuple(ref.identifier for ref in leaf(out, FIELDS[0]).value.population.member_refs) == ('submission',)


@pytest.mark.parametrize('event_time,qualified,pc10', (
    ('2026-01-10T13:00:00Z', True, 'met'),
    ('2026-01-10T15:00:00Z', False, 'unmet'),
    (None, False, 'unknown'),
))
def test_time_specific_effect_does_not_erase_supplied_event_inventory(event_time, qualified, pc10):
    source = small()
    def known(value):
        return {'state': 'known', 'value': value, 'precision': 'instant'}
    source['inquiries'][0].update(as_of=known('2026-01-10T14:00:00Z'),
        time_window={'start': known('2026-01-10T00:00:00Z'), 'end': known('2026-01-10T23:59:59Z')})
    change = h.cases.by_id(source, 'change')
    change['data']['occurred_at'] = known(event_time) if event_time else h.cases.unknown()
    requested = h._Node('TimeValue', h._Object(tuple(sorted(known('2026-01-10T14:00:00Z').items()))))
    out = run(source, temporal_basis='time_specific', requested_time=requested)[0]
    assert_counts(out, (1, 1, 1, int(qualified), int(qualified)))
    assert_effect(out, available=qualified)
    checks = {check.check_id: check.state for check in leaf(out, FIELDS[3]).check_refs}
    assert checks['PC10'] == pc10


@pytest.mark.parametrize('remaining', (25, 2500))
def test_budget_interruption_never_publishes_completed_zero_counts(remaining, monkeypatch):
    monkeypatch.setattr(resources, 'monotonic_ns', lambda: 100)
    source = small()
    prepared = h.admit(source)
    owner, job = h.job_pair()
    job.charge(1_000_000 - job.used - remaining)
    with pytest.raises(_AnalysisAborted) as stopped:
        outcomes._correction_outcomes(prepared, context(source), owner.witnesses, job)
    assert stopped.value.limit_id == 'WU9-L11'
    assert stopped.value.stop.input_state == 'accepted'
    with pytest.raises(_AnalysisAborted) as again:
        outcomes._correction_outcomes(prepared, context(source), owner.witnesses, job)
    assert again.value is stopped.value


def test_witness_quota_interrupts_before_complete_profile(monkeypatch):
    monkeypatch.setattr(resources, 'monotonic_ns', lambda: 100)
    source = small()
    prepared = h.admit(source)
    owner, job = h.job_pair()
    ledger = owner.witnesses
    ledger.retain(ledger.reserve(witnesses=20_000, members=0))
    with pytest.raises(_AnalysisAborted) as stopped:
        outcomes._correction_outcomes(prepared, context(source), ledger, job)
    assert stopped.value.limit_id == 'WU9-L13'


def test_results_are_immutable_and_ledger_must_belong_to_current_job():
    source = small()
    out, prepared, owner, job = run(source)
    for obj, attr in ((out, 'results'), (out.facts, 'cases'), (out.results[0], 'value')):
        with pytest.raises((FrozenInstanceError, AttributeError)):
            setattr(obj, attr, ())
    foreign, unused = h.job_pair()
    for ledger in (foreign.witnesses, _WitnessLedger(owner.witnesses.port)):
        with pytest.raises(TypeError):
            outcomes._correction_outcomes(prepared, context(source), ledger, job)
    assert foreign.witnesses._retained_witnesses == 0
