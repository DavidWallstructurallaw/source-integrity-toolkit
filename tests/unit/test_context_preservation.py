# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W12 M014 source oracles: Definitions 26.5 and VF051--053.

Literal H7 context, native stance records and independently supplied stage
universes determine expectations. Linked M010 values retain their owner and
current job; no second retention metric or source-verification verdict exists.
"""
import copy
from dataclasses import FrozenInstanceError, replace
import importlib.util
from pathlib import Path

import pytest

from source_integrity_toolkit.analysis import context as preservation
from source_integrity_toolkit.contracts.bundle import _Array, _Object
from source_integrity_toolkit.contracts import results
from source_integrity_toolkit.contracts.execution import _AnalysisAborted
from source_integrity_toolkit.runtime import resources
from source_integrity_toolkit.validation.limits import _WitnessLedger

_spec = importlib.util.spec_from_file_location(
    'sit_w12_cohort_helpers', Path(__file__).with_name('test_pipeline_cohorts.py'))
stages = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(stages)
h = stages.h
FIELDS = ('anomaly_context_disclosures', 'contestation_disclosures', 'tail_stage_result_links')
H7_STANCES = tuple('H7-ST-' + letter for letter in 'ABCDEF')
H7_CONTEXT = ('A local clock alignment difference may affect event ordering; the present '
              'peak-value Claim does not represent this timing distinction.')
UNSUPPORTED = {'integrity_assessment', 'independent_vote', 'equal_weight', 'consensus',
               'suppression', 'retention_fraction', 'rarity_classification', 'verified_by_toolkit'}


def context(source, **changes):
    values = dict(subject_refs=(), dependency_dimension=None, graph_view='stance_contestation',
                  coverage_kind=None, relation_types=(), operation_anchor=())
    values.update(changes)
    return h.context(source, **values)


def request(stage='selection', coverage=True):
    coverage_id, stage_key, prefix = stages.KEYS[stage]
    return (coverage_id if coverage is True else coverage,
            ('answer-run-1', stage_key, stage))


def run(source, *, stage_requests=(), **changes):
    original = copy.deepcopy(source)
    prepared = h.admit(source)
    ctx = context(source, **changes)
    owner, job = h.job_pair()
    ledger = owner.witnesses
    before = owner.used, job.used, ledger._retained_witnesses, ledger._retained_members
    out = preservation._context_preservation(prepared, ctx, ledger, job,
                                              stage_requests=stage_requests)
    assert source == original
    assert out.facts.prepared is prepared and out.facts.context is ctx and out.facts.job_port is job
    assert owner.used - before[0] == job.used - before[1] > 0
    assert ledger._retained_witnesses - before[2] == len(out.witnesses)
    assert ledger._retained_members - before[3] == sum(w.member_count for w in out.witnesses)
    assert tuple(row.ref.field_key for row in out.results) == FIELDS
    for row in out.results:
        assert row.ref.diagnostic_id == 'SIT-M014'
        assert (row.execution_state, row.value_kind) == ('completed', 'record_disclosures')
        scope = row.ref.scope
        assert scope.inquiry_ref.identifier == ctx.inquiry_ref
        assert tuple(ref.identifier for ref in scope.claim_refs) == ctx.claim_refs
        assert scope.graph_view == 'stance_contestation' and scope.dependency_dimension is None
        assert row.basis_refs and row.interpretation_limit
        assert all(check.result_ref is row.ref for check in row.check_refs)
        assert all(reason.scope is scope and row.ref in reason.affected_result_refs
                   for reason in row.reason_refs)
        assert all(witness.scope is scope for witness in row.witness_refs)
        checks = {check.check_id: check.state for check in row.check_refs}
        assert checks['PC01'] == checks['PC02'] == checks['PC24'] == 'met'
        assert 'PC23' in checks
    return out, prepared, owner, job


def leaf(out, field):
    return next(row for row in out.results if row.ref.field_key == field)


def disclosures(out, field=FIELDS[0]):
    row = leaf(out, field)
    assert (row.result_state, row.result_origin) == ('available', 'attributed_record')
    answer = {item.source.identifier: h.native(item.fields) for item in row.value.records}
    assert len(answer) == len(row.value.records)
    return answer


def assert_native(out, source, identifiers, field=FIELDS[0]):
    rows = disclosures(out, field)
    for identifier in identifiers:
        assert rows[identifier]['native_record'] == h.cases.by_id(source, identifier)
        assert UNSUPPORTED.isdisjoint(rows[identifier])
    return rows


def frozen(value):
    if isinstance(value, dict):
        return _Object(tuple((key, frozen(item)) for key, item in sorted(value.items())))
    if isinstance(value, list):
        return _Array(tuple(frozen(item) for item in value))
    return value


def mutated_disclosure(out, field, identifier, alter):
    row = leaf(out, field)
    changed = []
    for item in row.value.records:
        if isinstance(item.source, results._InputRef) and item.source.identifier == identifier:
            native = h.native(item.fields)
            alter(native)
            item = replace(item, fields=frozen(native))
        changed.append(item)
    newrow = replace(row, value=results._RecordDisclosures(tuple(changed)))
    return replace(out, results=tuple(newrow if item is row else item for item in out.results))


def assert_h7_stances(out, source):
    rows = assert_native(out, source, H7_STANCES, FIELDS[1])
    assert set(rows) == set(H7_STANCES)
    assert rows['H7-ST-F']['native_record']['data'] == {
        'predicate': 'contradicts', 'from_ref': 'H7-EF', 'to_ref': 'H7-C1',
        'polarity': 'affirmed', 'dimension': None, 'details': {}}
    context_rows = {row['id']: row for row in rows['H7-ST-F']['context_records']}
    for identifier in ('H7-EF', 'H7-L07', 'H7-O2', 'H7-SUP-CONTEXT', 'H7-SUP-ACQ'):
        assert context_rows[identifier] == h.cases.by_id(source, identifier)
    assert tuple(source['inquiries'][0]['seed_evidence_refs']) == stages.MEMBERS


def assert_stage_links(out):
    row = leaf(out, FIELDS[2])
    assert row.result_state == 'available'
    actual_results = tuple(result for profile in out.facts.stage_profiles for result in profile.results
                           if result.result_state == 'available')
    assert len(row.value.records) == len(actual_results)
    for disclosure, original in zip(row.value.records, actual_results):
        assert disclosure.source is original.ref
        assert disclosure.source.diagnostic_id == 'SIT-M010'
        payload = h.native(disclosure.fields)
        assert payload['source_result_state'] == original.result_state
        assert payload['source_value_kind'] == original.value_kind
        assert {'numerator', 'denominator', 'fraction', 'value', 'metric', 'retention_fraction',
                'suppression', 'whole_anomaly_retention'}.isdisjoint(payload)
    for profile in out.facts.stage_profiles:
        assert profile.facts.prepared is out.facts.prepared
        assert profile.facts.job_port is out.facts.job_port
        assert profile.facts.family == 'SIT-M010'
    return actual_results


@pytest.fixture(scope='module')
def hero_profile():
    source = h.hero()
    return source, run(source)[0]


@pytest.fixture(scope='module')
def hero_stage_profiles():
    source = h.hero()
    # Each keyed stage is a separate bounded query. Its M010 universe remains
    # six members even when context preservation selects EF. AN1 is retained
    # independently by the complete native-context profile above.
    outputs = tuple(run(source, stage_requests=(request(stage),),
                        subject_refs=('H7-EF',))[0]
                    for stage in ('selection', 'influence'))
    return source, outputs


def test_vf051_p_h7_unclassified_timing_context_has_no_invented_claim(hero_profile):
    source, out = hero_profile
    row = assert_native(out, source, ('H7-AN1',))['H7-AN1']['native_record']['data']
    assert row['original_context'] == H7_CONTEXT
    assert (row['claim_ref'], row['classification_state'], row['caller_label']) == (None, 'unclassified', None)


@pytest.mark.parametrize('mutation', ('force_claim', 'erase_context', 'invent_rarity', 'invent_ideology'))
def test_vf051_n_native_context_oracle_rejects_reclassification(hero_profile, mutation):
    source, out = hero_profile
    assert_native(out, source, ('H7-AN1',))
    def alter(payload):
        data = payload['native_record']['data']
        if mutation == 'force_claim':
            data['claim_ref'] = 'H7-C1'
        elif mutation == 'erase_context':
            data['original_context'] = None
        else:
            data.update(classification_state='caller_classified',
                        caller_label='rare' if mutation == 'invent_rarity' else 'ideological-minority')
    mutant = mutated_disclosure(out, FIELDS[0], 'H7-AN1', alter)
    with pytest.raises(AssertionError):
        assert_native(mutant, source, ('H7-AN1',))


def test_vf051_m_protected_context_stays_null_with_exact_gap_and_reference():
    source = h.cases.pool()
    anomaly = h.cases.by_id(source, 'anomaly')
    anomaly['data'].update(original_context=None, context_evidence_ref='protected-context')
    anomaly['gaps'] = [{'field': 'data.original_context', 'reason': 'withheld',
                        'detail': 'Original context is protected; no reconstruction is authorized.'}]
    reference = {'id': 'protected-context', 'reference_kind': 'external_locator', 'availability': 'withheld',
        'artifact_ref': None, 'record_ref': None, 'locator': 'https://fictional.invalid/private-context',
        'excerpt': None, 'provided_by_ref': 'actor', 'attestor_ref': None,
        'scope_note': 'The underlying context is withheld.'}
    source['evidence_references'].append(reference)
    out = run(source)[0]
    row = assert_native(out, source, ('anomaly',))['anomaly']
    assert row['native_record']['data']['original_context'] is None
    assert reference in row['context_records']
    assert 'context_withheld_or_unavailable' in {reason.code for reason in leaf(out, FIELDS[0]).reason_refs}
    assert not disclosures(out, FIELDS[1])


def test_vf051_b_caller_label_is_attributed_without_taxonomy_or_truth_promotion():
    source = h.cases.pool()
    anomaly = h.cases.by_id(source, 'anomaly')
    anomaly['data'].update(classification_state='caller_classified', caller_label='verified rare suppressed dissent')
    anomaly['extensions'] = {'caller:classification': {'verified_by_toolkit': False, 'note': 'Source-native text only.'}}
    out = run(source)[0]
    row = assert_native(out, source, ('anomaly',))['anomaly']
    assert row['native_record']['data']['caller_label'] == 'verified rare suppressed dissent'
    assert leaf(out, FIELDS[0]).result_origin == 'attributed_record'
    assert UNSUPPORTED.isdisjoint(row)


def test_vf052_p_h7_all_stances_preserve_ef_separate_acquisition(hero_profile):
    source, out = hero_profile
    assert_h7_stances(out, source)


def test_vf052_n_disagreement_cannot_delete_source_or_lower_integrity(hero_profile):
    source, out = hero_profile
    assert_h7_stances(out, source)
    row = leaf(out, FIELDS[1])
    missing = replace(row, value=results._RecordDisclosures(tuple(
        item for item in row.value.records if item.source.identifier != 'H7-ST-F')))
    mutant = replace(out, results=tuple(missing if item is row else item for item in out.results))
    with pytest.raises((AssertionError, KeyError)):
        assert_h7_stances(mutant, source)
    mutant = mutated_disclosure(out, FIELDS[1], 'H7-ST-F',
        lambda payload: payload.update(integrity_assessment='lowered_due_to_disagreement'))
    with pytest.raises(AssertionError):
        assert_h7_stances(mutant, source)


def test_vf052_m_empty_named_stance_inventory_cannot_establish_consensus():
    source = h.cases.pool()
    out = run(source)[0]
    row = leaf(out, FIELDS[1])
    assert disclosures(out, FIELDS[1]) == {}
    assert row.result_origin == 'attributed_record'
    assert 'supplied' in row.interpretation_limit.lower()
    limits = row.interpretation_limit + ' '.join(
        text for population in row.population_refs for text in population.qualifications)
    assert 'consensus' in limits.lower() or 'disagreement' in limits.lower()
    assert not out.facts.stage_profiles


def test_vf052_b_factual_stance_and_explicit_provenance_conflict_keep_separate_scope():
    source = h.cases.pool()
    source['assertions'] = [h.cases.relation(name) for name in ('supports', 'contradicts', 'originates_from')]
    contradiction = h.cases.by_id(source, 'r-contradicts')
    contradiction['data']['from_ref'] = 'e2'
    prior = run(source)[0]
    assert_native(prior, source, ('r-supports', 'r-contradicts'), FIELDS[1])
    assert not any(row['native_record']['assertion_kind'] == 'assessment'
                   for row in disclosures(prior, FIELDS[1]).values())
    denial = copy.deepcopy(h.cases.by_id(source, 'r-originates_from'))
    denial['id'] = 'denied-origin'; denial['data']['polarity'] = 'denied'
    source['assertions'].append(denial)
    conflict = h.cases.assertion('origin-conflict', 'assessment', {
        'assessment_kind': 'conflict', 'subject_refs': ['r-originates_from', 'denied-origin'],
        'details': {'conflict_kind': 'affirmation_denial', 'resolution_state': 'unresolved',
                    'resolution_evaluation_ref': None, 'scope_note': 'Acquisition only; no truth verdict.'}})
    source['assertions'].append(conflict)
    out = run(source)[0]
    rows = assert_native(out, source, ('r-supports', 'r-contradicts', 'origin-conflict'), FIELDS[1])
    assert rows['origin-conflict']['native_record']['data']['subject_refs'] == ['r-originates_from', 'denied-origin']
    context_rows = {row['id']: row for row in rows['origin-conflict']['context_records']}
    assert context_rows['r-originates_from'] == h.cases.by_id(source, 'r-originates_from')
    assert context_rows['denied-origin'] == denial


def test_vf053_p_h7_links_actual_stage_results_without_whole_anomaly_rate(hero_stage_profiles, hero_profile):
    source, outputs = hero_stage_profiles
    for out in outputs:
        assert_stage_links(out)
        assert set(disclosures(out, FIELDS[1])) == {'H7-ST-F'}
    assert_native(hero_profile[1], source, ('H7-AN1',))
    selection, influence = (out.facts.stage_profiles[0] for out in outputs)
    stages.assert_partition(stages.partition(selection), stages.MEMBERS, stages.MEMBERS[:5], ('H7-EF',), ())
    stages.assert_scalar(stages.scalar(selection), (5, 6))
    stages.assert_partition(stages.partition(influence), stages.MEMBERS,
        ('H7-EA', 'H7-EB', 'H7-ED'), ('H7-EC', 'H7-EF'), ('H7-EE',))
    assert 'H7-AN1' not in stages.partition(selection)['members']


def test_vf053_n_stage_links_reject_duplicate_metric_and_final_only_suppression(hero_stage_profiles):
    source, outputs = hero_stage_profiles
    out = outputs[0]
    assert_stage_links(out)
    row = leaf(out, FIELDS[2])
    first = row.value.records[0]
    payload = h.native(first.fields)
    payload.update(numerator='5', denominator='6', metric='whole_anomaly_retention')
    changed = replace(row, value=results._RecordDisclosures((replace(first, fields=frozen(payload)),)
                                                           + row.value.records[1:]))
    mutant = replace(out, results=tuple(changed if item is row else item for item in out.results))
    with pytest.raises(AssertionError):
        assert_stage_links(mutant)
    source = final_only()
    out = run(source, stage_requests=(request(coverage=None),))[0]
    assert_stage_links(out)
    row = leaf(out, FIELDS[2]); first = row.value.records[0]
    payload = h.native(first.fields); payload['suppression'] = 'proved_from_final_list'
    changed = replace(row, value=results._RecordDisclosures((replace(first, fields=frozen(payload)),)
                                                           + row.value.records[1:]))
    mutant = replace(out, results=tuple(changed if item is row else item for item in out.results))
    with pytest.raises(AssertionError):
        assert_stage_links(mutant)


def final_only():
    source = stages.small()
    source['records'] = [row for row in source['records'] if row['kind'] != 'pipeline_record']
    source['assertions'] = []
    source['inquiries'][0]['coverage_assertion_refs'] = []
    return source


def test_vf053_m_final_only_context_retains_missing_intake_reasons_and_no_fraction():
    source = final_only()
    out = run(source, stage_requests=(request(coverage=None),))[0]
    assert_native(out, source, ('H7-AN1',))
    assert_stage_links(out)
    stage = out.facts.stage_profiles[0]
    assert not stage.facts.target.eligible
    for field in (stages.FIELDS[2], stages.FIELDS[3], stages.FIELDS[5], stages.FIELDS[6]):
        row = stages.leaf(stage, field)
        assert row.result_state == 'unavailable' and row.value is None
    assert {'cohort_anchor_missing', 'cohort_universe_unestablished'} & stages.codes(stages.leaf(stage, stages.FIELDS[2]))
    assert {'cohort_anchor_missing', 'cohort_universe_unestablished'} & {
        reason.code for reason in leaf(out, FIELDS[2]).reason_refs}


def test_vf053_b_explicit_anomaly_cohort_keeps_members_when_source_seeds_change():
    source = stages.small()
    stages.by_id(source, 'H7-COV-SEL')['data']['details']['member_refs'] = ['H7-AN1']
    stages.by_id(source, 'H7-COV-SEL')['data']['subject_refs'] = ['anomaly-stage']
    stages.duplicate(source, 'H7-PS-F', 'anomaly-stage')['data']['subject_ref'] = 'H7-AN1'
    before = run(source, stage_requests=(request(),))[0]
    assert_stage_links(before)
    stages.assert_partition(stages.partition(before.facts.stage_profiles[0]), ('H7-AN1',), (), ('H7-AN1',), ())
    stages.assert_scalar(stages.scalar(before.facts.stage_profiles[0]), (0, 1))
    source['inquiries'][0]['seed_evidence_refs'] = ['H7-EA', 'H7-EB']
    source['inquiries'][0]['seed_artifact_refs'] = ['H7-ANSWER']
    after = run(source, stage_requests=(request(),))[0]
    assert_stage_links(after)
    stages.assert_partition(stages.partition(after.facts.stage_profiles[0]), ('H7-AN1',), (), ('H7-AN1',), ())
    stages.assert_scalar(stages.scalar(after.facts.stage_profiles[0]), (0, 1))
    assert_native(after, source, ('H7-AN1',))


def test_all_supplied_stance_kinds_and_classification_remain_native_disclosures():
    source = h.cases.pool()
    predicates = ('supports', 'contradicts', 'describes', 'qualifies', 'contextualizes', 'corroborates')
    source['assertions'] = [h.cases.relation(name) for name in predicates]
    source['assertions'].append(h.cases.assertion('source-classification', 'assessment', {
        'assessment_kind': 'classification', 'subject_refs': ['e'],
        'details': {'axis': 'sil_governance_layer', 'labels': ['verified'],
                    'verification_assessment_refs': [], 'scope_note': 'Native label is unverified here.'}}))
    out = run(source)[0]
    rows = assert_native(out, source, tuple('r-' + name for name in predicates)
                         + ('source-classification',), FIELDS[1])
    assert len(rows) == 7
    assert rows['source-classification']['native_record']['data']['details']['labels'] == ['verified']


def test_unrelated_inquiry_anomaly_is_not_borrowed_by_matching_prose():
    source = h.cases.pool()
    other = copy.deepcopy(source['inquiries'][0]); other['id'] = 'other-inquiry'
    source['inquiries'].append(other)
    anomaly = copy.deepcopy(h.cases.by_id(source, 'anomaly'))
    anomaly['id'] = 'outside-anomaly'; anomaly['data']['inquiry_refs'] = ['other-inquiry']
    source['records'].append(anomaly)
    out = run(source)[0]
    assert set(disclosures(out)) == {'anomaly'}


def test_broad_assertion_scope_cannot_import_stance_for_another_bound_claim():
    source = h.cases.pool()
    source['inquiries'][0]['target_claim_refs'].append('claim2')
    h.cases.by_id(source, 'e2')['data']['claim_ref'] = 'claim2'
    support = h.cases.relation('supports')
    other = h.cases.relation('contradicts')
    other['scope']['claim_refs'] = ['claim', 'claim2']
    other['data'].update(from_ref='e2', to_ref='claim2')
    source['assertions'] = [support, other]
    out = run(source)[0]
    assert set(disclosures(out, FIELDS[1])) == {'r-supports'}
    assert_native(out, source, ('r-supports',), FIELDS[1])


def test_selected_subject_keeps_its_classification_without_borrowing_another():
    source = h.cases.pool()
    stance = h.cases.relation('contradicts'); stance['data']['from_ref'] = 'e2'
    source['assertions'] = [stance]
    for identifier, subject in (('other-classification', 'e'), ('selected-classification', 'e2')):
        source['assertions'].append(h.cases.assertion(identifier, 'assessment', {
            'assessment_kind': 'classification', 'subject_refs': [subject],
            'details': {'axis': 'sil_governance_layer', 'labels': ['verified'],
                        'verification_assessment_refs': [], 'scope_note': 'Attributed to this exact subject only.'}}))
    out = run(source, subject_refs=('e2',))[0]
    assert set(disclosures(out, FIELDS[1])) == {'r-contradicts', 'selected-classification'}
    assert_native(out, source, ('r-contradicts', 'selected-classification'), FIELDS[1])


def test_compatible_unresolved_stance_source_remains_attributed_with_its_claim():
    source = h.cases.pool()
    unknown = h.cases.by_id(source, 'unresolved')
    unknown['data'].update(expected_kinds=['evidence_item'],
        description='Protected supplied EvidenceItem for claim; its acquisition and identity remain unknown.')
    stance = h.cases.relation('contradicts'); stance['data']['from_ref'] = 'unresolved'
    source['assertions'] = [stance]
    out = run(source)[0]
    row = assert_native(out, source, ('r-contradicts',), FIELDS[1])['r-contradicts']
    assert unknown in row['context_records']
    assert row['native_record']['data']['to_ref'] == 'claim'
    assert row['native_record']['data']['from_ref'] == 'unresolved'


@pytest.mark.parametrize('selected', ('e', 'class-direct'))
def test_classification_only_query_preserves_explicit_subject_or_assessment(selected):
    source = h.cases.pool()
    source['assertions'] = [h.cases.assertion('class-direct', 'assessment', {
        'assessment_kind': 'classification', 'subject_refs': ['e'],
        'details': {'axis': 'sil_governance_layer', 'labels': ['verified'],
                    'verification_assessment_refs': [], 'scope_note': 'A standalone attributed classification.'}})]
    out = run(source, subject_refs=(selected,))[0]
    assert set(disclosures(out, FIELDS[1])) == {'class-direct'}
    assert_native(out, source, ('class-direct',), FIELDS[1])


def test_two_claim_query_preserves_each_stance_at_its_native_claim_scope():
    source = h.cases.pool()
    source['inquiries'][0]['target_claim_refs'].append('claim2')
    h.cases.by_id(source, 'e2')['data']['claim_ref'] = 'claim2'
    support = h.cases.relation('supports')
    other = h.cases.relation('contradicts')
    other['scope']['claim_refs'] = ['claim2']
    other['data'].update(from_ref='e2', to_ref='claim2')
    source['assertions'] = [support, other]
    out = run(source, claim_refs=('claim', 'claim2'))[0]
    assert set(disclosures(out, FIELDS[1])) == {'r-supports', 'r-contradicts'}
    rows = assert_native(out, source, ('r-supports', 'r-contradicts'), FIELDS[1])
    for row in rows.values():
        assert 'scope_unestablished' not in row['reason_codes']
    assert {check.check_id: check.state for check in leaf(out, FIELDS[1]).check_refs}['PC09'] == 'met'


def test_two_claim_context_links_stage_at_its_actual_single_claim_scope():
    source = stages.small()
    other = copy.deepcopy(stages.by_id(source, 'H7-C1'))
    other['id'] = 'H7-C2'; other['data']['claim_key'] = 'second-claim-family'
    source['records'].append(other)
    source['inquiries'][0]['target_claim_refs'].append('H7-C2')
    stance = h.cases.assertion('tail-contradiction', 'relation', {
        'predicate': 'contradicts', 'from_ref': 'H7-EF', 'to_ref': 'H7-C1',
        'polarity': 'affirmed', 'dimension': None, 'details': {}})
    stance['scope'].update(inquiry_refs=['H7-I1'], claim_refs=['H7-C1'])
    stance['provenance'] = copy.deepcopy(stages.by_id(source, 'H7-COV-SEL')['provenance'])
    source['assertions'].append(stance)
    out = run(source, claim_refs=('H7-C1', 'H7-C2'), stage_requests=(request(),))[0]
    assert_stage_links(out)
    stage = out.facts.stage_profiles[0]
    assert stage.facts.target.eligible
    assert stage.facts.context.claim_refs == ('H7-C1',)
    stages.assert_partition(stages.partition(stage), stages.MEMBERS, stages.MEMBERS[:5], ('H7-EF',), ())
    stages.assert_scalar(stages.scalar(stage), (5, 6))
    for row in stage.results:
        assert tuple(ref.identifier for ref in row.ref.scope.claim_refs) == ('H7-C1',)
        assert 'scope_unestablished' not in stages.codes(row)
    assert tuple(ref.identifier for ref in leaf(out, FIELDS[2]).ref.scope.claim_refs) == ('H7-C1', 'H7-C2')


def test_no_requested_stage_is_empty_link_inventory_without_retention_claim():
    out = run(h.cases.pool())[0]
    assert not leaf(out, FIELDS[2]).value.records
    assert not out.facts.stage_profiles
    assert_stage_links(out)


def test_unrelated_supplied_cohort_cannot_be_borrowed_for_anomaly_context():
    source = stages.small()
    prepared = h.admit(source)
    owner, job = h.job_pair()
    # The finite source cohort is a valid M010 input, but none of its six
    # members is the sole context subject AN1 and no stance connects them.
    with pytest.raises(TypeError):
        preservation._context_preservation(prepared, context(source), owner.witnesses, job,
                                             stage_requests=(request(),))


def test_distinct_jobs_recompute_stage_helpers_and_never_share_semantic_objects():
    source = stages.small()
    stance = h.cases.assertion('tail-contradiction', 'relation', {
        'predicate': 'contradicts', 'from_ref': 'H7-EF', 'to_ref': 'H7-C1',
        'polarity': 'affirmed', 'dimension': None, 'details': {}})
    stance['scope'].update(inquiry_refs=['H7-I1'], claim_refs=['H7-C1'])
    stance['provenance'] = copy.deepcopy(stages.by_id(source, 'H7-COV-SEL')['provenance'])
    source['assertions'].append(stance)
    first = run(source, stage_requests=(request(),))[0]
    second = run(source, stage_requests=(request(),))[0]
    assert_stage_links(first); assert_stage_links(second)
    assert first.facts.stage_profiles[0] is not second.facts.stage_profiles[0]
    assert first.facts.job_port is not second.facts.job_port
    assert first.facts.stage_profiles[0].results[0].ref is not second.facts.stage_profiles[0].results[0].ref


@pytest.mark.parametrize('stage_requested', (False, True))
def test_budget_interruption_never_publishes_partial_context_or_empty_success(stage_requested, monkeypatch):
    monkeypatch.setattr(resources, 'monotonic_ns', lambda: 100)
    source = stages.small()
    prepared = h.admit(source); owner, job = h.job_pair()
    job.charge(1_000_000 - job.used - 100)
    requests = (request(),) if stage_requested else ()
    with pytest.raises(_AnalysisAborted) as stopped:
        preservation._context_preservation(prepared, context(source), owner.witnesses, job,
                                             stage_requests=requests)
    assert stopped.value.limit_id == 'WU9-L11'
    assert stopped.value.stop.input_state == 'accepted'
    with pytest.raises(_AnalysisAborted) as again:
        preservation._context_preservation(prepared, context(source), owner.witnesses, job,
                                             stage_requests=requests)
    assert again.value is stopped.value


def test_two_real_h7_stage_requests_stop_atomically_at_original_job_budget(monkeypatch):
    monkeypatch.setattr(resources, 'monotonic_ns', lambda: 100)
    source = h.hero(); original = copy.deepcopy(source)
    prepared = h.admit(source); owner, job = h.job_pair()
    ctx = context(source, subject_refs=('H7-EF',))
    with pytest.raises(_AnalysisAborted) as stopped:
        preservation._context_preservation(prepared, ctx, owner.witnesses, job,
                                             stage_requests=(request(), request('influence')))
    assert stopped.value.limit_id == 'WU9-L11'
    assert stopped.value.stop.input_state == 'accepted'
    assert source == original
    with pytest.raises(_AnalysisAborted) as again:
        preservation._context_preservation(prepared, ctx, owner.witnesses, job)
    assert again.value is stopped.value


def test_witness_limit_aborts_before_completed_context_profile(monkeypatch):
    monkeypatch.setattr(resources, 'monotonic_ns', lambda: 100)
    source = h.cases.pool()
    prepared = h.admit(source); owner, job = h.job_pair()
    owner.witnesses.retain(owner.witnesses.reserve(witnesses=20_000, members=0))
    with pytest.raises(_AnalysisAborted) as stopped:
        preservation._context_preservation(prepared, context(source), owner.witnesses, job)
    assert stopped.value.limit_id == 'WU9-L13'


def test_context_outputs_are_immutable_and_require_current_job_ledger():
    source = h.cases.pool()
    out, prepared, owner, job = run(source)
    for obj, attr in ((out, 'results'), (out.facts, 'stage_profiles'), (out.results[0], 'value')):
        with pytest.raises((FrozenInstanceError, AttributeError)):
            setattr(obj, attr, ())
    foreign, unused = h.job_pair()
    for ledger in (foreign.witnesses, _WitnessLedger(owner.witnesses.port)):
        with pytest.raises(TypeError):
            preservation._context_preservation(prepared, context(source), ledger, job)
    assert foreign.witnesses._retained_witnesses == 0
