# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W09 source oracles for VF029--031: externality and native stage records.

Definitions25.2/26 and Lineage6.10/9.6 keep boundary-qualified assessments,
recorded stages and finite-cohort qualifications separate. Expected H7 sets
are literal specification values, not learned from owner output.
"""
import copy
import importlib.util
from pathlib import Path

import pytest

from source_integrity_toolkit.analysis import presence

_spec = importlib.util.spec_from_file_location('sit_w09_presence_cases', Path(__file__).with_name('test_process_comparison.py'))
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)
FIELDS = {
    'SIT-M009': ('externality_assessment_disclosures', 'externality_stage_links'),
    'SIT-M010': ('pipeline_stage_disclosures', 'stage_member_partition', 'stage_occurrence_fraction',
                'stage_occurrence_completion_interval', 'cohort_transition_disclosures',
                'cohort_transition_fraction', 'cohort_transition_completion_interval'),
}
STAGES = (
    ('admission', 'intake-1', 'H7-PA-'),
    ('preservation', 'store-1', 'H7-PP-'),
    ('selection', 'select-1', 'H7-PS-'),
    ('influence', 'answer-use-1', 'H7-PU-'),
)
F_LOGS = ('H7-PA-F', 'H7-PP-F', 'H7-PS-F', 'H7-PU-F')
SEEDS = ('H7-EA', 'H7-EB', 'H7-EC', 'H7-ED', 'H7-EE', 'H7-EF')


def run(source, *, family='SIT-M009', assessment='H7-EXT-F', subjects=(),
        stage=None, coverage=None, temporal_basis='snapshot_structural', requested_time=None, claims=None):
    prepared = h.admit(source)
    selected_claims = tuple(source['inquiries'][0]['target_claim_refs'][:1]) if claims is None else claims
    context = h.context(source, subject_refs=subjects, dependency_dimension=None, claim_refs=selected_claims,
                        temporal_basis=temporal_basis, requested_time=requested_time)
    owner, job = h.job_pair()
    ledger = owner.witnesses
    before = owner.used, job.used, ledger._retained_witnesses, ledger._retained_members
    original = copy.deepcopy(source)
    output = presence._presence(prepared, context, ledger, job, family=family,
        assessment_ref=assessment if family == 'SIT-M009' else None,
        coverage_ref=coverage, stage_anchor=stage)
    assert source == original
    assert output.facts.prepared is prepared and output.facts.context is context
    assert output.facts.job_port is job
    assert owner.used - before[0] == job.used - before[1] > 0
    assert ledger._retained_witnesses - before[2] == len(output.witnesses)
    assert ledger._retained_members - before[3] == sum(w.member_count for w in output.witnesses)
    assert tuple(row.ref.field_key for row in output.results) == FIELDS[family]
    for row in output.results:
        assert row.ref.diagnostic_id == family
        assert row.execution_state == 'completed'
        scope = row.ref.scope
        assert scope.inquiry_ref.identifier == source['inquiries'][0]['id']
        assert tuple(ref.identifier for ref in scope.claim_refs) == selected_claims
        assert scope.temporal_basis == temporal_basis
        assert row.basis_refs and row.witness_refs and row.interpretation_limit
        assert all(check.result_ref is row.ref for check in row.check_refs)
        assert all(reason.scope is scope and row.ref in reason.affected_result_refs for reason in row.reason_refs)
        assert all(witness.scope is scope for witness in row.witness_refs)
        checks = {check.check_id: check.state for check in row.check_refs}
        assert checks['PC01'] == checks['PC24'] == 'met'
        assert 'PC02' in checks
        if family == 'SIT-M009':
            assert {'PC05', 'PC09', 'PC10', 'PC15'} <= checks.keys()
            expected_targets = (assessment,) if assessment is not None else subjects
            assert tuple(ref.identifier for ref in scope.target_refs) == expected_targets
        else:
            assert {'PC16', 'PC17', 'PC18'} <= checks.keys()
    return output, prepared, owner, job


def leaf(output, name):
    return next(row for row in output.results if row.ref.field_key == name)


def records(output, name):
    row = leaf(output, name)
    assert row.value_kind == 'record_disclosures'
    if row.value is None:
        return {}
    actual = {item.source.identifier: h.native(item.fields) for item in row.value.records}
    assert len(actual) == len(row.value.records)
    return actual


def assessment_row(output, identifier='H7-EXT-F'):
    return records(output, 'externality_assessment_disclosures')[identifier]


def assert_native(actual, source, identifiers):
    assert set(actual) == set(identifiers)
    for identifier in identifiers:
        original = h.cases.by_id(source, identifier)
        keys = h.NATIVE_KEYS if 'assertion_kind' in original else ('data', 'provenance')
        for key in keys:
            assert actual[identifier][key] == original[key]
        for key in ('gaps', 'extensions'):
            if key in original:
                assert actual[identifier][key] == original[key]


def stage_rows(output, field='externality_stage_links'):
    actual = records(output, field)
    return {identifier: row for identifier, row in actual.items()
            if 'stage' in row.get('data', {})}


def reason_codes(output, field):
    return {reason.code for reason in leaf(output, field).reason_refs}


def check_state(output, field, check_id):
    row = leaf(output, field)
    check = next(check for check in row.check_refs if check.check_id == check_id)
    assert check.result_ref is row.ref
    return check.state


def stage_profile(source, stage, key):
    return run(source, family='SIT-M010', stage=('answer-run-1', key, stage))[0]


def without_stages(source, identifiers):
    """Remove only named stage records plus coverage references that need them."""
    deleted = set(identifiers)
    source['records'] = [row for row in source['records'] if row['id'] not in deleted]
    removed = {row['id'] for row in source['assertions']
               if row['assertion_kind'] == 'assessment' and row['data']['assessment_kind'] == 'coverage'
               and deleted.intersection(row['data']['subject_refs'])}
    source['assertions'] = [row for row in source['assertions'] if row['id'] not in removed]
    for inquiry in source['inquiries']:
        inquiry['coverage_assertion_refs'] = [identifier for identifier in inquiry['coverage_assertion_refs']
                                             if identifier not in removed]
    return source


@pytest.fixture(scope='module')
def hero_profiles():
    source = h.hero()
    return source, {identifier: run(source, assessment=identifier)[0] for identifier in ('H7-EXT-F', 'H7-INT-A')}, {
        stage: stage_profile(source, stage, key) for stage, key, unused in STAGES}


def test_vf029_positive_h7_external_and_internal_assessments_keep_exact_native_basis(hero_profiles):
    source, externalities, unused = hero_profiles
    for identifier, subject, conclusion, supports in (
        ('H7-EXT-F', 'H7-EF', 'external', ['H7-SUP-CONTEXT', 'H7-SUP-ACQ']),
        ('H7-INT-A', 'H7-EA', 'internal', ['H7-SUP-CONTEXT', 'H7-SUP-CHAIN'])):
        output = externalities[identifier]
        actual = records(output, 'externality_assessment_disclosures')
        assert_native(actual, source, (identifier,))
        row = actual[identifier]
        assert row['data']['subject_refs'] == [subject]
        assert row['data']['details']['boundary_inquiry_ref'] == 'H7-I1'
        assert row['data']['details']['conclusion'] == conclusion
        assert row['data']['details']['relevant_time'] == h.known('2026-01-10T10:00:00Z')
        assert row['provenance']['evidence_ref_ids'] == supports
        assert row['qualification_state'] == 'met'
        mutant = copy.deepcopy(actual)
        mutant[identifier]['data']['details']['conclusion'] = 'external' if conclusion == 'internal' else 'internal'
        with pytest.raises(AssertionError):
            assert_native(mutant, source, (identifier,))


def test_vf030_positive_h7_links_only_ef_native_four_stage_records(hero_profiles):
    source, externalities, unused = hero_profiles
    output = externalities['H7-EXT-F']
    actual = stage_rows(output)
    assert_native(actual, source, F_LOGS)
    assert [(actual[identifier]['data']['stage'], actual[identifier]['data']['stage_key'],
             actual[identifier]['data']['state']) for identifier in F_LOGS] == [
        ('admission', 'intake-1', 'occurred'), ('preservation', 'store-1', 'occurred'),
        ('selection', 'select-1', 'did_not_occur'), ('influence', 'answer-use-1', 'did_not_occur')]
    assert all(row['data']['subject_ref'] == 'H7-EF' for row in actual.values())
    mutant = copy.deepcopy(actual)
    mutant['H7-PS-F']['data']['state'] = 'occurred'
    with pytest.raises(AssertionError):
        assert_native(mutant, source, F_LOGS)


def test_vf030_negative_shared_prose_publisher_and_date_never_join_another_subject():
    source = h.hero()
    candidate = copy.deepcopy(h.cases.by_id(source, 'H7-PA-F'))
    candidate['id'] = 'W09-SAME-METADATA'
    candidate['data']['subject_ref'] = 'H7-EE'
    source['records'].append(candidate)
    # Both evidence items may even point to one Artifact while remaining
    # different supplied contribution IDs with different assessment subjects.
    h.cases.by_id(source, 'H7-EE')['data']['artifact_ref'] = 'H7-F'
    output, _, _, _ = run(source)
    actual = stage_rows(output)
    assert_native(actual, source, F_LOGS)
    mutant = copy.deepcopy(actual)
    mutant[candidate['id']] = candidate
    with pytest.raises(AssertionError):
        assert_native(mutant, source, F_LOGS)


def test_vf030_missing_stages_preserves_qualified_assessment_without_inventing_links():
    source = without_stages(h.hero(), F_LOGS)
    output, _, _, _ = run(source)
    assert assessment_row(output)['qualification_state'] == 'met'
    assert_native(records(output, 'externality_assessment_disclosures'), source, ('H7-EXT-F',))
    assert stage_rows(output) == {}
    mutant = {'H7-PA-F': h.cases.by_id(h.hero(), 'H7-PA-F')}
    with pytest.raises(AssertionError):
        assert_native(mutant, source, ())


def test_vf029_vf030_boundary_selection_and_use_negative_preserve_externality_and_admission(hero_profiles):
    positive = h.hero()
    for identifier in ('H7-PS-F', 'H7-PU-F'):
        row = h.cases.by_id(positive, identifier)
        row['data'].update(state='occurred', output_refs=['H7-ANSWER'], linkage_kind='use_record')
    plus, _, _, _ = run(positive)
    control, externalities, unused = hero_profiles
    negative = externalities['H7-EXT-F']
    assert assessment_row(plus) == assessment_row(negative)
    assert assessment_row(negative)['qualification_state'] == 'met'
    a, b = stage_rows(plus), stage_rows(negative)
    assert_native(a, positive, F_LOGS)
    assert_native(b, control, F_LOGS)
    assert a['H7-PA-F'] == b['H7-PA-F']
    assert [a[name]['data']['state'] for name in ('H7-PS-F', 'H7-PU-F')] == ['occurred', 'occurred']
    assert [b[name]['data']['state'] for name in ('H7-PS-F', 'H7-PU-F')] == ['did_not_occur', 'did_not_occur']
    assert all(row.value_kind == 'record_disclosures' for row in negative.results)


@pytest.mark.parametrize('stage,key,prefix', STAGES)
def test_vf031_positive_four_independent_stage_keys_preserve_all_native_records(hero_profiles, stage, key, prefix):
    source, unused, profiles = hero_profiles
    output = profiles[stage]
    actual = stage_rows(output, 'pipeline_stage_disclosures')
    identifiers = tuple(prefix + letter for letter in 'ABCDEF')
    assert_native(actual, source, identifiers)
    assert {row['data']['subject_ref'] for row in actual.values()} == set(SEEDS)
    assert all((row['data']['run_key'], row['data']['stage_key'], row['data']['stage']) == (
        'answer-run-1', key, stage) for row in actual.values())
    expected = ['occurred'] * 6
    if stage == 'selection':
        expected[-1] = 'did_not_occur'
    elif stage == 'influence':
        expected = ['occurred', 'occurred', 'did_not_occur', 'occurred', 'unknown', 'did_not_occur']
    assert [actual[identifier]['data']['state'] for identifier in identifiers] == expected
    mutant = copy.deepcopy(actual)
    mutant[identifiers[0]]['data']['stage'] = 'selection' if stage != 'selection' else 'admission'
    with pytest.raises(AssertionError):
        assert_native(mutant, source, identifiers)


def test_vf031_negative_repeated_attempt_keys_remain_separate_without_newest_wins():
    source = h.hero()
    extra = copy.deepcopy(h.cases.by_id(source, 'H7-PS-F'))
    extra['id'] = 'W09-SELECT-RETRY'
    extra['data'].update(stage_key='select-2', state='occurred', output_refs=['H7-ANSWER'],
                         observed_at=h.known('2026-01-10T11:35:00Z'))
    source['records'].append(extra)
    old = stage_rows(stage_profile(source, 'selection', 'select-1'), 'pipeline_stage_disclosures')
    retry = stage_rows(stage_profile(source, 'selection', 'select-2'), 'pipeline_stage_disclosures')
    assert_native(old, source, tuple('H7-PS-' + letter for letter in 'ABCDEF'))
    assert_native(retry, source, ('W09-SELECT-RETRY',))
    assert old['H7-PS-F']['data']['state'] == 'did_not_occur'
    assert retry['W09-SELECT-RETRY']['data']['state'] == 'occurred'
    mutant = copy.deepcopy(old)
    mutant['H7-PS-F']['data']['state'] = retry['W09-SELECT-RETRY']['data']['state']
    with pytest.raises(AssertionError):
        assert_native(mutant, source, tuple('H7-PS-' + letter for letter in 'ABCDEF'))


def test_vf030_vf031_missing_earlier_stages_do_not_erase_a_supported_influence_record():
    source = h.hero()
    removed = [row['id'] for row in source['records'] if row['kind'] == 'pipeline_record'
               and row['id'] != 'H7-PU-F']
    without_stages(source, removed)
    use = h.cases.by_id(source, 'H7-PU-F')
    use['data'].update(state='occurred', output_refs=['H7-ANSWER'])
    external, _, _, _ = run(source)
    assert_native(stage_rows(external), source, ('H7-PU-F',))
    assert assessment_row(external)['qualification_state'] == 'met'
    output = stage_profile(source, 'influence', 'answer-use-1')
    assert_native(stage_rows(output, 'pipeline_stage_disclosures'), source, ('H7-PU-F',))
    assert leaf(output, 'stage_occurrence_fraction').result_state == 'unavailable'
    assert leaf(output, 'stage_occurrence_fraction').value is None


def test_vf031_boundary_duplicate_unknown_and_contradictory_rows_all_remain_visible():
    source = h.hero()
    for identifier, state, timing in (
        ('W09-UNKNOWN-A', 'unknown', '2026-01-10T11:42:00Z'),
        ('W09-CONTRARY-A', 'did_not_occur', '2026-01-10T11:43:00Z')):
        extra = copy.deepcopy(h.cases.by_id(source, 'H7-PU-A'))
        extra['id'] = identifier
        extra['data'].update(state=state, observed_at=h.known(timing), output_refs=[])
        if state == 'unknown':
            extra['data']['linkage_kind'] = 'unspecified'
        source['records'].append(extra)
    output = stage_profile(source, 'influence', 'answer-use-1')
    actual = stage_rows(output, 'pipeline_stage_disclosures')
    expected = tuple('H7-PU-' + letter for letter in 'ABCDEF') + ('W09-UNKNOWN-A', 'W09-CONTRARY-A')
    assert_native(actual, source, expected)
    assert [actual[name]['data']['state'] for name in ('H7-PU-A', 'W09-UNKNOWN-A', 'W09-CONTRARY-A')] == [
        'occurred', 'unknown', 'did_not_occur']
    mutant = copy.deepcopy(actual)
    mutant.pop('H7-PU-A')
    with pytest.raises(AssertionError):
        assert_native(mutant, source, expected)


def small_presence():
    """Small complete canonical dossier for mutations unrelated to H7 volume."""
    source = h.cases.pool()
    keep = {'actor', 'claim', 'artifact', 'e', 'origin'}
    pipeline = copy.deepcopy(h.cases.by_id(source, 'pipeline'))
    pipeline.update(id='pa')
    pipeline['data'].update(subject_ref='e', run_key='run', stage_key='intake', stage='admission',
        state='occurred', output_refs=['e'], observed_at=h.known('2026-01-10T10:00:00Z'),
        linkage_kind='use_record', detail='The exact evidence contribution was admitted.')
    source['records'] = [row for row in source['records'] if row['id'] in keep] + [pipeline]
    source['predecessor'] = None
    source['inquiries'][0].update(seed_artifact_refs=['artifact'], seed_evidence_refs=['e'],
        target_object_refs=[], coverage_assertion_refs=[])
    assertion = h.cases.assertion('ext', 'assessment', {'assessment_kind': 'externality',
        'subject_refs': ['e'], 'details': {'boundary_inquiry_ref': 'inquiry', 'conclusion': 'external',
            'grounding_basis': 'The supplied acquisition was outside this inquiry reuse boundary.',
            'relevant_time': h.known('2026-01-10T09:00:00Z')}})
    source['assertions'] = [assertion]
    for row in source['records'] + source['assertions']:
        row['provenance'].update(basis_kind='documented_record', evidence_ref_ids=['support'],
            method='Inspect the supplied fictional boundary and process excerpt.',
            qualifications=['Supplied conformance record; no outside authentication.'])
    source['evidence_references'][0]['excerpt'] = 'The recorded acquisition was outside the declared reuse boundary, and e was admitted.'
    return source


def test_vf029_negative_recent_human_remote_metadata_and_admission_cannot_create_externality():
    source = small_presence()
    source['assertions'] = []
    artifact = h.cases.by_id(source, 'artifact')
    artifact['data'].update(locators=['https://example.invalid/new-external-source'],
        published_at=h.known('2026-01-10T08:00:00Z'))
    h.cases.by_id(source, 'actor')['data']['display_name'] = 'Independent human external reviewer'
    output, _, _, _ = run(source, assessment=None, subjects=('e',))
    row = leaf(output, 'externality_assessment_disclosures')
    assert (row.result_state, row.value) == ('unavailable', None)
    assert 'externality_unestablished' in reason_codes(output, 'externality_assessment_disclosures')
    assert_native(stage_rows(output), source, ('pa',))
    actual = (row.result_state, row.value)
    assert actual == ('unavailable', None)
    with pytest.raises(AssertionError):
        assert ('available', 'external') == actual


@pytest.mark.parametrize('missing', ('grounding', 'documentary_basis', 'inspectable_support'))
def test_vf029_missing_qualification_retains_native_assessment_and_explicit_unavailability(missing):
    source = small_presence()
    assessment = h.cases.by_id(source, 'ext')
    if missing == 'grounding':
        assessment['data']['details']['grounding_basis'] = None
        assessment['gaps'] = [{'field': 'data.details.grounding_basis', 'reason': 'not_recorded',
                              'detail': 'No boundary grounding was supplied.'}]
    elif missing == 'documentary_basis':
        assessment['provenance'].update(basis_kind='declaration', evidence_ref_ids=[])
    else:
        support = h.cases.by_id(source, 'support')
        support.update(reference_kind='external_locator', availability='withheld',
                       excerpt=None, locator='https://example.invalid/withheld-boundary-evidence')
    output, _, _, _ = run(source, assessment='ext')
    actual = records(output, 'externality_assessment_disclosures')
    assert_native(actual, source, ('ext',))
    row = actual['ext']
    assert row['qualification_state'] != 'met'
    assert check_state(output, 'externality_assessment_disclosures', 'PC05') == ('met' if missing == 'grounding' else 'unmet')
    assert row['qualified_externality'] == 'unavailable'
    assert row['data']['details']['conclusion'] == 'external'
    assert 'externality_unestablished' in reason_codes(output, 'externality_assessment_disclosures')
    assert next(check.state for check in leaf(output, 'externality_assessment_disclosures').check_refs
                if check.check_id == 'PC15') != 'met'
    mutant = copy.deepcopy(actual)
    mutant['ext']['qualified_externality'] = 'available'
    with pytest.raises(AssertionError):
        assert mutant['ext']['qualified_externality'] == 'unavailable'


@pytest.mark.parametrize('conclusion', ('mixed', 'unknown'))
def test_native_mixed_or_unknown_externality_is_never_promoted_to_external(conclusion):
    source = small_presence()
    h.cases.by_id(source, 'ext')['data']['details']['conclusion'] = conclusion
    if conclusion == 'unknown':
        known = copy.deepcopy(h.cases.by_id(source, 'ext'))
        known['id'] = 'known-external'
        known['data']['details']['conclusion'] = 'external'
        source['assertions'].append(known)
    output, _, _, _ = run(source, assessment='ext')
    actual = records(output, 'externality_assessment_disclosures')
    assert_native(actual, source, ('ext',))
    assert actual['ext']['data']['details']['conclusion'] == conclusion
    assert check_state(output, 'externality_assessment_disclosures', 'PC05') == 'met'
    if conclusion == 'unknown':
        assert actual['ext']['qualified_externality'] == 'unavailable'
        assert 'premise_disputed' not in reason_codes(output, 'externality_assessment_disclosures')
        supported, _, _, _ = run(source, assessment='known-external')
        assert_native(records(supported, 'externality_assessment_disclosures'), source, ('known-external',))
        assert assessment_row(supported, 'known-external')['qualified_externality'] == 'available'
        assert 'premise_disputed' not in reason_codes(supported, 'externality_assessment_disclosures')
        assert check_state(supported, 'externality_assessment_disclosures', 'PC09') == 'met'
    mutant = copy.deepcopy(actual)
    mutant['ext']['data']['details']['conclusion'] = 'external'
    with pytest.raises(AssertionError):
        assert_native(mutant, source, ('ext',))


def test_foreign_boundary_does_not_qualify_the_selected_inquiry():
    source = small_presence()
    assessment = h.cases.by_id(source, 'ext')
    other = copy.deepcopy(source['inquiries'][0])
    other['id'] = 'other-inquiry'
    other['boundary']['description'] = 'A separate supplied system boundary.'
    source['inquiries'].append(other)
    assessment['scope']['inquiry_refs'].append('other-inquiry')
    assessment['data']['details']['boundary_inquiry_ref'] = 'other-inquiry'
    output, _, _, _ = run(source, assessment='ext')
    actual = records(output, 'externality_assessment_disclosures')
    assert_native(actual, source, ('ext',))
    assert actual['ext']['qualified_externality'] == 'unavailable'
    assert check_state(output, 'externality_assessment_disclosures', 'PC05') == 'met'
    assert check_state(output, 'externality_assessment_disclosures', 'PC15') != 'met'


def test_externality_unknown_relevant_time_remains_unknown_in_a_time_specific_query():
    source = small_presence()
    assessment = h.cases.by_id(source, 'ext')
    assessment['scope']['effective_window'] = {'start': h.known('2026-01-10T00:00:00Z'),
                                               'end': h.known('2026-01-10T14:00:00Z')}
    positive, _, _, _ = run(source, assessment='ext', temporal_basis='time_specific',
        requested_time=h.requested('2026-01-10T09:00:00Z'))
    assert assessment_row(positive, 'ext')['qualified_externality'] == 'available'
    assert check_state(positive, 'externality_assessment_disclosures', 'PC05') == 'met'
    assert check_state(positive, 'externality_assessment_disclosures', 'PC10') == 'met'
    assessment['data']['details']['relevant_time'] = h.cases.unknown()
    timed, _, _, _ = run(source, assessment='ext', temporal_basis='time_specific',
        requested_time=h.requested('2026-01-10T09:00:00Z'))
    row = assessment_row(timed, 'ext')
    assert row['qualified_externality'] == 'unavailable'
    assert 'time_applicability_unknown' in reason_codes(timed, 'externality_assessment_disclosures')
    assert check_state(timed, 'externality_assessment_disclosures', 'PC05') == 'met'
    assert check_state(timed, 'externality_assessment_disclosures', 'PC10') == 'unknown'


def test_contradictory_scoped_externality_conclusions_remain_attributed_and_unresolved():
    source = small_presence()
    contrary = copy.deepcopy(h.cases.by_id(source, 'ext'))
    contrary['id'] = 'internal-contestation'
    contrary['data']['details'].update(conclusion='internal', grounding_basis='The acquisition belongs inside the same supplied boundary.')
    source['assertions'].append(contrary)
    results = {}
    for identifier in ('ext', 'internal-contestation'):
        output, _, _, _ = run(source, assessment=identifier)
        actual = records(output, 'externality_assessment_disclosures')
        assert_native(actual, source, ('ext', 'internal-contestation'))
        assert actual[identifier]['qualified_externality'] == 'unavailable'
        assert 'premise_disputed' in reason_codes(output, 'externality_assessment_disclosures')
        assert check_state(output, 'externality_assessment_disclosures', 'PC05') == 'met'
        assert check_state(output, 'externality_assessment_disclosures', 'PC09') == 'unmet'
        results[identifier] = actual[identifier]['data']['details']['conclusion']
    assert results == {'ext': 'external', 'internal-contestation': 'internal'}
    contrary['data']['details']['relevant_time'] = h.known('2026-01-10T10:00:00Z')
    for identifier in ('ext', 'internal-contestation'):
        bounded, _, _, _ = run(source, assessment=identifier)
        assert_native(records(bounded, 'externality_assessment_disclosures'), source, (identifier,))
        assert assessment_row(bounded, identifier)['qualified_externality'] == 'available'
        assert 'premise_disputed' not in reason_codes(bounded, 'externality_assessment_disclosures')
    explicit = h.cases.assertion('W09-EXPLICIT-CONFLICT', 'assessment', {
        'assessment_kind': 'conflict', 'subject_refs': ['ext', 'internal-contestation'],
        'details': {'conflict_kind': 'scope_dispute', 'resolution_state': 'unresolved',
                    'resolution_evaluation_ref': None,
                    'scope_note': 'The supplied review explicitly disputes the boundary assessments.'}})
    explicit['provenance'].update(basis_kind='documented_record', evidence_ref_ids=['support'],
        method='Supplied review of the attributed boundary dispute.', qualifications=['Unresolved supplied dispute.'])
    source['assertions'].append(explicit)
    disputed, _, _, _ = run(source, assessment='ext')
    row = leaf(disputed, 'externality_assessment_disclosures')
    assert assessment_row(disputed, 'ext')['qualified_externality'] == 'unavailable'
    expected = ('assertions', 'W09-EXPLICIT-CONFLICT')
    assert expected in {(basis.source.collection, basis.source.identifier) for basis in row.basis_refs}
    pc09 = next(check for check in row.check_refs if check.check_id == 'PC09')
    assert pc09.state == 'unmet'
    assert expected in {(ref.collection, ref.identifier) for ref in pc09.input_refs}
    conflict_sources = {(ref.collection, ref.identifier) for reason in row.reason_refs
                        if reason.code == 'premise_disputed' for ref in reason.input_refs}
    assert expected in conflict_sources


@pytest.mark.parametrize('qualified_mapping', (True, False))
def test_origin_assessment_links_stage_only_through_qualified_explicit_directional_mapping(qualified_mapping):
    source = small_presence()
    h.cases.by_id(source, 'ext')['data']['subject_refs'] = ['origin']
    mapping = h.cases.relation('originates_from')
    mapping['id'] = 'mapped-acquisition'
    mapping['provenance'].update(basis_kind='documented_record' if qualified_mapping else 'declaration',
        evidence_ref_ids=['support'] if qualified_mapping else [],
        method='The supplied record binds e directly to origin.', qualifications=['Finite supplied binding only.'])
    source['assertions'].append(mapping)
    output, _, _, _ = run(source, assessment='ext')
    actual = stage_rows(output)
    assert_native(actual, source, ('pa',) if qualified_mapping else ())
    assert assessment_row(output, 'ext')['data']['subject_refs'] == ['origin']
    if qualified_mapping:
        links = records(output, 'externality_stage_links')
        assert links['pa']['mapping_assertion_refs'] == ['mapped-acquisition']
        assert links['pa']['externality_subject_refs'] == ['origin']
        assert mapping['data']['from_ref'] == 'e' and mapping['data']['to_ref'] == 'origin'
    else:
        mutant = {'pa': h.cases.by_id(source, 'pa')}
        with pytest.raises(AssertionError):
            assert_native(mutant, source, ())


def test_origin_externality_for_another_claim_cannot_qualify_this_claim_scope():
    source = small_presence()
    claim = copy.deepcopy(h.cases.by_id(source, 'claim'))
    claim['id'] = 'other-claim'
    claim['data']['version_label'] = 'other-version'
    source['records'].append(claim)
    source['inquiries'][0]['target_claim_refs'].append('other-claim')
    assessment = h.cases.by_id(source, 'ext')
    assessment['data']['subject_refs'] = ['origin']
    assessment['scope']['claim_refs'] = ['other-claim']
    output, _, _, _ = run(source, assessment='ext')
    actual = records(output, 'externality_assessment_disclosures')
    assert_native(actual, source, ('ext',))
    assert actual['ext']['qualified_externality'] == 'unavailable'
    assert actual['ext']['scope']['claim_refs'] == ['other-claim']
    assert stage_rows(output) == {}


def test_stage_declaration_does_not_borrow_the_externality_assessment_basis():
    source = small_presence()
    stage = h.cases.by_id(source, 'pa')
    stage['provenance'].update(basis_kind='declaration', evidence_ref_ids=[])
    output, _, _, _ = run(source, assessment='ext')
    assert assessment_row(output, 'ext')['qualified_externality'] == 'available'
    assert check_state(output, 'externality_assessment_disclosures', 'PC05') == 'met'
    actual = stage_rows(output)
    assert_native(actual, source, ('pa',))
    assert actual['pa']['qualification_state'] != 'met'
    assert check_state(output, 'externality_stage_links', 'PC05') != 'met'
    mutant = copy.deepcopy(actual)
    mutant['pa']['qualification_state'] = 'met'
    with pytest.raises(AssertionError):
        assert mutant['pa']['qualification_state'] != 'met'


def test_multi_claim_externality_retains_each_scope_while_mapping_its_actual_claim_bound_member():
    source = small_presence()
    claim = copy.deepcopy(h.cases.by_id(source, 'claim'))
    claim['id'] = 'other-claim'
    claim['data']['version_label'] = 'other-version'
    source['records'].append(claim)
    source['inquiries'][0]['target_claim_refs'].append('other-claim')
    assessment = h.cases.by_id(source, 'ext')
    assessment['data']['subject_refs'] = ['origin']
    assessment['scope']['claim_refs'] = ['claim', 'other-claim']
    mapping = h.cases.relation('originates_from')
    mapping['id'] = 'mapped-acquisition'
    mapping['provenance'].update(basis_kind='documented_record', evidence_ref_ids=['support'],
        method='The supplied relation maps the C1-bound evidence to the named origin.',
        qualifications=['Only the original contribution Claim is mapped.'])
    source['assertions'].append(mapping)
    output, _, _, _ = run(source, assessment='ext', claims=('claim', 'other-claim'))
    assert assessment_row(output, 'ext')['qualified_externality'] == 'available'
    actual = stage_rows(output)
    assert_native(actual, source, ('pa',))
    assert actual['pa']['mapping_assertion_refs'] == ['mapped-acquisition']
    assert actual['pa']['externality_subject_refs'] == ['origin']
    assert h.cases.by_id(source, 'e')['data']['claim_ref'] == 'claim'
    for row in output.results:
        assert tuple(ref.identifier for ref in row.ref.scope.claim_refs) == ('claim', 'other-claim')
