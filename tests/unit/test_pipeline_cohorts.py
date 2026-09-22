# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W09 M010 finite-cohort oracles from Definitions 26 and VF032--VF037.

Literal H7/W7 member sets and fractions precede rejecting output mutants.
Real admission, evidence qualification and current-job accounting execute;
these component tests do not claim public orchestration or external verification.
"""
import copy
from dataclasses import FrozenInstanceError
import importlib.util
from pathlib import Path

import pytest

from source_integrity_toolkit.analysis import presence
from source_integrity_toolkit.contracts.bundle import _Object
from source_integrity_toolkit.contracts.evidence import _Node
from source_integrity_toolkit.contracts.execution import _AnalysisAborted
from source_integrity_toolkit.runtime import resources
from source_integrity_toolkit.validation.limits import _WitnessLedger

_spec = importlib.util.spec_from_file_location(
    'sit_w09_cohort_cases', Path(__file__).with_name('test_process_comparison.py'))
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

FIELDS = ('pipeline_stage_disclosures', 'stage_member_partition', 'stage_occurrence_fraction',
          'stage_occurrence_completion_interval', 'cohort_transition_disclosures',
          'cohort_transition_fraction', 'cohort_transition_completion_interval')
MEMBERS = ('H7-EA', 'H7-EB', 'H7-EC', 'H7-ED', 'H7-EE', 'H7-EF')
FIVE = MEMBERS[:5]
KEYS = {'admission': ('H7-COV-ADM', 'intake-1', 'H7-PA-'),
        'preservation': ('H7-COV-PRES', 'store-1', 'H7-PP-'),
        'selection': ('H7-COV-SEL', 'select-1', 'H7-PS-'),
        'influence': ('H7-COV-USE', 'answer-use-1', 'H7-PU-')}


def by_id(source, identifier):
    return h.cases.by_id(source, identifier)


def context(source, stage='influence', **changes):
    values = dict(subject_refs=(), dependency_dimension=None, graph_view='pipeline_stages',
                  coverage_kind='pipeline_universe', relation_types=(),
                  operation_anchor=('answer-run-1', KEYS[stage][1], stage))
    values.update(changes)
    return h.context(source, **values)


def run(source, stage='influence', *, coverage=True, **changes):
    original = copy.deepcopy(source)
    snapshot = h.admit(source)
    ctx = context(source, stage, **changes)
    owner, job = h.job_pair(); ledger = owner.witnesses
    before = owner.used, job.used, ledger._retained_witnesses, ledger._retained_members
    chosen = KEYS[stage][0] if coverage is True else (coverage if isinstance(coverage, str) else None)
    out = presence._presence(snapshot, ctx, ledger, job, family='SIT-M010',
                             coverage_ref=chosen, stage_anchor=ctx.operation_anchor)
    assert source == original
    assert out.facts.prepared is snapshot and out.facts.context is ctx and out.facts.job_port is job
    assert owner.used - before[0] == job.used - before[1] > 0
    assert ledger._retained_witnesses - before[2] == len(out.witnesses)
    assert ledger._retained_members - before[3] == sum(w.member_count for w in out.witnesses)
    assert tuple(row.ref.field_key for row in out.results) == FIELDS
    for row in out.results:
        assert row.ref.diagnostic_id == 'SIT-M010'
        scope = row.ref.scope
        assert scope.inquiry_ref.identifier == ctx.inquiry_ref
        assert tuple(ref.identifier for ref in scope.claim_refs) == ctx.claim_refs
        if row.ref.field_key in FIELDS[4:]:
            suffix = (('from_admission',) + out.facts.baseline.anchor if out.facts.baseline is not None
                      else ('unestablished_admission',))
            assert scope.operation_anchor == ctx.operation_anchor + suffix
        else:
            assert scope.operation_anchor == ctx.operation_anchor
        assert scope.graph_view == 'pipeline_stages' and scope.dependency_dimension is None
        assert scope.temporal_basis == ctx.temporal_basis
        assert row.interpretation_limit and row.basis_refs
        assert all(c.result_ref is row.ref for c in row.check_refs)
        assert all(r.scope is scope and row.ref in r.affected_result_refs for r in row.reason_refs)
        assert all(w.scope is scope for w in row.witness_refs)
        checks = {c.check_id: c.state for c in row.check_refs}
        assert checks['PC01'] == checks['PC02'] == checks['PC24'] == 'met'
        for population in row.population_refs:
            assert population.scope is scope and population.selection_rule
    return out, snapshot, owner, job


def leaf(out, field):
    return next(row for row in out.results if row.ref.field_key == field)


def codes(row):
    return {reason.code for reason in row.reason_refs}


def member_ids(population):
    assert population.unit == 'pipeline_member'
    assert population.membership_state == 'enumerated_for_scope'
    assert all(ref.collection == 'records' and ref.selector is None for ref in population.member_refs)
    return tuple(ref.identifier for ref in population.member_refs)


def partition(out):
    row = leaf(out, FIELDS[1])
    assert (row.execution_state, row.result_state, row.value_kind) == ('completed', 'available', 'partition')
    assert row.value.population in row.population_refs
    return {'members': member_ids(row.value.population),
            'buckets': {category.label: (category.count, tuple(r.identifier for r in category.member_refs))
                        for category in row.value.categories}}


def assert_partition(actual, members, y, f, u):
    assert actual == {'members': members, 'buckets': {
        label: (len(bucket), bucket) for label, bucket in (('Y', y), ('F', f), ('U', u))}}


def scalar(out, field=FIELDS[2]):
    row = leaf(out, field)
    assert row.execution_state == 'completed' and row.value_kind == 'fraction'
    if row.value is not None:
        assert row.value.population in row.population_refs
        members = member_ids(row.value.population)
        assert row.value.denominator == len(members)
    return {'state': row.result_state, 'value': None if row.value is None else (
        row.value.numerator, row.value.denominator), 'reasons': codes(row)}


def assert_scalar(actual, expected=None, *, state='available', reasons=()):
    assert actual['state'] == state and actual['value'] == expected
    assert set(reasons) <= actual['reasons']


def interval(out, field=FIELDS[3]):
    row = leaf(out, field)
    assert row.execution_state == 'completed' and row.value_kind == 'completion_interval'
    value = row.value
    if value is not None:
        assert value.lower.population is value.upper.population is value.partition.population
        assert value.lower.population in row.population_refs
        assert member_ids(value.lower.population) == member_ids(leaf(out, FIELDS[1]).value.population)
        fraction_field = FIELDS[5] if field == FIELDS[6] else FIELDS[2]
        assert value.lower.population is leaf(out, fraction_field).population_refs[0]
    return {'state': row.result_state, 'bounds': None if value is None else (
        (value.lower.numerator, value.lower.denominator), (value.upper.numerator, value.upper.denominator)),
        'kind': None if value is None else value.interval_kind, 'reasons': codes(row)}


def assert_interval(actual, bounds=None, *, state='available', reasons=()):
    assert actual['state'] == state and actual['bounds'] == bounds
    assert actual['kind'] == ('finite_cohort_completion' if bounds is not None else None)
    assert set(reasons) <= actual['reasons']


def disclosures(out, field=FIELDS[4]):
    row = leaf(out, field)
    assert (row.execution_state, row.result_state, row.value_kind) == (
        'completed', 'available', 'record_disclosures')
    return {record.source.identifier: h.native(record.fields) for record in row.value.records}


def tokens(value):
    if isinstance(value, dict):
        return [part for key, item in value.items() for part in (key, *tokens(item))]
    if isinstance(value, (list, tuple)):
        return [part for item in value for part in tokens(item)]
    return [value]


def observed(source, identifier, state):
    row = by_id(source, identifier)
    row['data'].update(state=state, output_refs=['H7-ANSWER'] if state == 'occurred' else [],
        linkage_kind='unspecified' if state == 'unknown' else 'use_record',
        detail='The supplied fictional observation is ' + state + '.')
    return row


def duplicate(source, identifier, new_id, state=None):
    row = copy.deepcopy(by_id(source, identifier)); row['id'] = new_id
    source['records'].append(row)
    if state is not None:
        observed(source, new_id, state)
    return row


def small():
    """Small complete fictional dossier; expected fractions do not come from it."""
    source = h.cases.sparse()
    known = lambda minute: {'state': 'known', 'value': '2026-01-10T11:' + minute + ':00Z',
                            'precision': 'instant'}
    basis = {'attributed_to_ref': 'actor', 'basis_kind': 'documented_record',
             'evidence_ref_ids': ['support'], 'method': 'Inspect the supplied exact finite member and stage log.',
             'qualifications': ['Fictional supplied process evidence; no outside authentication.']}
    artifact = h.cases.pool()['records'][2]
    for identifier in ('H7-ANSWER', 'H7-DOC-PIPE', 'H7-A-V2'):
        row = copy.deepcopy(artifact); row['id'] = identifier
        row['data'].update(work_key=identifier, content_evidence_refs=[])
        source['records'].append(row)
    for identifier in MEMBERS:
        row = h.cases.record(identifier, 'evidence_item', {'claim_ref': 'claim', 'artifact_ref': 'H7-ANSWER',
            'locator': identifier, 'epistemic_type': 'fictional_example', 'description': 'Finite declared member.'})
        row['provenance'] = copy.deepcopy(basis); source['records'].append(row)
    anomaly = h.cases.record('H7-AN1', 'anomaly', {'inquiry_refs': ['inquiry'], 'claim_ref': None,
        'original_context': 'An unclassified timing distinction supplied outside the Claim taxonomy.',
        'context_evidence_ref': None, 'classification_state': 'unclassified', 'caller_label': None,
        'comparison_note': 'No rarity or suppression conclusion supplied.'})
    anomaly['provenance'] = copy.deepcopy(basis); source['records'].append(anomaly)
    source['records'].append(h.cases.record('H7-UX', 'unresolved_reference', {
        'expected_kinds': ['evidence_item'], 'reason': 'not_recorded',
        'description': 'Unresolved possible cohort member.'}))
    source['evidence_references'] = [{'id': 'support', 'reference_kind': 'supplied_excerpt',
        'availability': 'supplied', 'artifact_ref': 'H7-DOC-PIPE', 'record_ref': None,
        'locator': None, 'excerpt': 'The listed finite members and exact keyed observations are the whole supplied process record.',
        'provided_by_ref': 'actor', 'attestor_ref': None, 'scope_note': 'Finite fictional eligibility and observation log.'}]
    for stage, minute in (('admission', '10'), ('preservation', '20'), ('selection', '30'), ('influence', '40')):
        coverage_id, key, prefix = KEYS[stage]
        for letter, member in zip('ABCDEF', MEMBERS):
            state = ('did_not_occur' if stage == 'selection' and letter == 'F' else
                     'did_not_occur' if stage == 'influence' and letter in 'CF' else
                     'unknown' if stage == 'influence' and letter == 'E' else 'occurred')
            row = h.cases.record(prefix + letter, 'pipeline_record', {'subject_ref': member,
                'run_key': 'answer-run-1', 'stage_key': key, 'stage': stage, 'state': state,
                'output_refs': ['H7-ANSWER'] if state == 'occurred' else [], 'observed_at': known(minute),
                'linkage_kind': 'unspecified' if state == 'unknown' else 'use_record',
                'detail': 'Supplied exact member and stage observation.'})
            row['provenance'] = copy.deepcopy(basis); source['records'].append(row)
        coverage = h.cases.assertion(coverage_id, 'assessment', {'assessment_kind': 'coverage',
            'subject_refs': [prefix + 'A'], 'details': {'coverage_kind': 'pipeline_universe',
            'state': 'complete_for_scope', 'relation_types': [], 'dimensions': [],
            'member_refs': list(MEMBERS), 'omitted_refs': [], 'universe_enumerated': True,
            'scope_note': 'Exactly the listed member IDs for this one anchored run and stage.'}})
        coverage['provenance'] = copy.deepcopy(basis)
        source['assertions'].append(coverage)
        source['inquiries'][0]['coverage_assertion_refs'].append(coverage_id)
    # Rename only canonical reference scalars, not prose or inferred identities.
    names = {'inquiry': 'H7-I1', 'claim': 'H7-C1', 'actor': 'H7-PREP'}
    def renamed(value):
        if isinstance(value, str): return names.get(value, value)
        if isinstance(value, list): return [renamed(item) for item in value]
        if isinstance(value, dict):
            return {key: item if key in ('kind', 'assertion_kind', 'expected_kinds') else renamed(item)
                    for key, item in value.items()}
        return value
    return renamed(source)


def five(*, missing=False):
    """W7-19 literal A/B/D positive, C negative, E unresolved, with valid intake."""
    source = small()
    for identifier in ('H7-COV-SEL', 'H7-COV-ADM'):
        by_id(source, identifier)['data']['details']['member_refs'] = list(FIVE)
    observed(source, 'H7-PS-C', 'did_not_occur')
    observed(source, 'H7-PS-E', 'unknown')
    if missing:
        source['records'] = [row for row in source['records'] if row['id'] != 'H7-PS-E']
    return source


def competing_baseline(source):
    for letter in 'ABCDEF':
        duplicate(source, 'H7-PA-' + letter, 'other-intake-' + letter)['data']['stage_key'] = 'intake-2'
    coverage = copy.deepcopy(by_id(source, 'H7-COV-ADM')); coverage['id'] = 'other-intake-coverage'
    coverage['data']['subject_refs'] = ['other-intake-A']
    source['assertions'].append(coverage)
    source['inquiries'][0]['coverage_assertion_refs'].append(coverage['id'])
    return source


def remove_admission_coverage(source):
    source['assertions'] = [row for row in source['assertions'] if row['id'] != 'H7-COV-ADM']
    source['inquiries'][0]['coverage_assertion_refs'].remove('H7-COV-ADM')
    return source


@pytest.fixture(scope='module')
def heroes():
    return {stage: run(h.hero(), stage)[0] for stage in ('preservation', 'selection', 'influence')}


@pytest.fixture(scope='module')
def w719():
    return run(five(), 'selection')[0]


def test_vf032_p_h7_exact_member_partition_uses_anchored_six(heroes):
    out = heroes['influence']
    assert_partition(partition(out), MEMBERS, ('H7-EA', 'H7-EB', 'H7-ED'),
                     ('H7-EC', 'H7-EF'), ('H7-EE',))
    assert tuple(row.member.identifier for row in out.facts.target.rows) == MEMBERS
    assert out.facts.target.anchor == ('answer-run-1', 'answer-use-1', 'influence')


@pytest.mark.parametrize('mutation', ('omit_unknown', 'duplicate_log_member'))
def test_vf032_n_partition_rejects_unknown_omission_and_log_count_inflation(heroes, mutation):
    actual = partition(heroes['influence'])
    oracle = lambda value: assert_partition(value, MEMBERS, ('H7-EA', 'H7-EB', 'H7-ED'),
                                           ('H7-EC', 'H7-EF'), ('H7-EE',))
    oracle(actual)
    mutant = copy.deepcopy(actual)
    if mutation == 'omit_unknown':
        mutant['members'] = tuple(member for member in MEMBERS if member != 'H7-EE')
        mutant['buckets']['U'] = (0, ())
    else:
        mutant['buckets']['Y'] = (4, ('H7-EA', 'H7-EA', 'H7-EB', 'H7-ED'))
    with pytest.raises(AssertionError):
        oracle(mutant)


@pytest.mark.parametrize('absence', ('missing', 'different_key', 'different_run'))
def test_vf032_m_missing_observation_stays_u_in_w719_population(absence):
    source = five(missing=absence == 'missing')
    if absence != 'missing':
        row = observed(source, 'H7-PS-E', 'occurred')
        row['data']['stage_key' if absence == 'different_key' else 'run_key'] = 'another-attempt'
    out = run(source, 'selection')[0]
    assert_partition(partition(out), FIVE, ('H7-EA', 'H7-EB', 'H7-ED'), ('H7-EC',), ('H7-EE',))
    unresolved = next(row for row in out.facts.target.rows if row.member.identifier == 'H7-EE')
    assert unresolved.records == () and unresolved.reason_codes


def test_vf032_m_unestablished_population_is_not_an_empty_partition():
    out = run(small(), coverage=False)[0]
    row = leaf(out, FIELDS[1])
    assert row.result_state == 'unavailable' and row.value is None
    assert any(population.membership_state == 'unestablished' for population in row.population_refs)
    assert 'cohort_universe_unestablished' in codes(row) or 'cohort_anchor_missing' in codes(row)
    assert disclosures(out, FIELDS[0])


@pytest.mark.parametrize('extra', ('unknown', 'did_not_occur'))
def test_vf032_b_additional_unknown_differs_from_bare_contrary_declaration(extra):
    source = five()
    row = duplicate(source, 'H7-PS-A', 'extra-A', extra)
    if extra == 'did_not_occur':
        row['provenance'].update(basis_kind='declaration', evidence_ref_ids=[])
        row['data']['observed_at'] = {'state': 'known', 'value': '2026-01-10T11:59:00Z', 'precision': 'instant'}
    out = run(source, 'selection')[0]
    if extra == 'unknown':
        assert_partition(partition(out), FIVE, ('H7-EA', 'H7-EB', 'H7-ED'), ('H7-EC',), ('H7-EE',))
        assert_interval(interval(out), ((3, 5), (4, 5)))
    else:
        assert_partition(partition(out), FIVE, ('H7-EB', 'H7-ED'), ('H7-EC',), ('H7-EA', 'H7-EE'))
        assert_interval(interval(out), ((2, 5), (4, 5)))
    member = next(row for row in out.facts.target.rows if row.member.identifier == 'H7-EA')
    assert {record.identifier for record in member.records} == {'H7-PS-A', 'extra-A'}
    assert 'extra-A' in tokens(disclosures(out, FIELDS[0]))


def test_vf033_p_selection_fraction_keeps_exact_six_member_denominator(heroes):
    out = heroes['selection']
    assert_scalar(scalar(out), (5, 6))
    assert_partition(partition(out), MEMBERS, MEMBERS[:5], ('H7-EF',), ())
    checks = {c.check_id: c.state for c in leaf(out, FIELDS[2]).check_refs}
    assert checks['PC16'] == checks['PC17'] == 'met'


def test_vf033_n_unknown_use_member_cannot_be_dropped_to_report_three_fifths(heroes):
    actual = scalar(heroes['influence'])
    assert_scalar(actual, state='unavailable', reasons=('stage_classification_unresolved',))
    mutant = dict(actual, state='available', value=(3, 5))
    with pytest.raises(AssertionError):
        assert_scalar(mutant, state='unavailable')


@pytest.mark.parametrize('anchor', ('missing', 'ambiguous'))
def test_vf033_m_stage_logs_cannot_supply_missing_or_ambiguous_cohort_anchor(anchor):
    source = small()
    by_id(source, 'H7-COV-USE')['data']['subject_refs'] = (
        ['H7-I1'] if anchor == 'missing' else ['H7-PU-A', 'H7-PS-A'])
    out = run(source)[0]
    assert_scalar(scalar(out), state='unavailable', reasons=(
        'cohort_anchor_missing' if anchor == 'missing' else 'cohort_anchor_ambiguous',))
    assert disclosures(out, FIELDS[0])


@pytest.mark.parametrize('kind', ('empty', 'negative'))
def test_vf033_b_known_empty_and_all_negative_cohorts_have_different_values(kind):
    source = small()
    if kind == 'empty':
        by_id(source, 'H7-COV-SEL')['data']['details']['member_refs'] = []
    else:
        for letter in 'ABCDEF':
            observed(source, 'H7-PS-' + letter, 'did_not_occur')
    out = run(source, 'selection')[0]
    if kind == 'empty':
        assert_partition(partition(out), (), (), (), ())
        assert_scalar(scalar(out), state='unavailable', reasons=('zero_denominator',))
        assert_interval(interval(out), state='unavailable', reasons=('zero_denominator',))
    else:
        assert_partition(partition(out), MEMBERS, (), MEMBERS, ())
        assert_scalar(scalar(out), (0, 6))


def test_vf034_p_h7_and_w719_intervals_preserve_full_finite_cohorts(heroes, w719):
    assert_interval(interval(heroes['influence']), ((3, 6), (4, 6)))
    assert_interval(interval(w719), ((3, 5), (4, 5)))


@pytest.mark.parametrize('mutation', ('wrong_denominator', 'measured_rate_label'))
def test_vf034_n_interval_rejects_measured_rate_or_resolved_only_denominator(heroes, mutation):
    actual = interval(heroes['influence'])
    assert_interval(actual, ((3, 6), (4, 6)))
    mutant = copy.deepcopy(actual)
    if mutation == 'wrong_denominator':
        mutant['bounds'] = ((3, 5), (4, 5))
    else:
        mutant['kind'] = 'measured_use_rate'
    with pytest.raises(AssertionError):
        assert_interval(mutant, ((3, 6), (4, 6)))


@pytest.mark.parametrize('defect', ('not_enumerated', 'partial', 'omitted', 'wrong_kind', 'unresolved',
                                  'declared_coverage'))
def test_vf034_m_invalid_universe_never_supplies_interval(defect):
    source = small()
    coverage = by_id(source, 'H7-COV-USE')
    details = coverage['data']['details']
    if defect == 'not_enumerated':
        details['universe_enumerated'] = False
    elif defect == 'partial':
        details['state'] = 'partial'
    elif defect == 'omitted':
        details['omitted_refs'] = ['H7-AN1']
    elif defect == 'wrong_kind':
        details['member_refs'] = ['H7-ANSWER']
    elif defect == 'declared_coverage':
        coverage['provenance'].update(basis_kind='declaration', evidence_ref_ids=[])
    else:
        details['member_refs'].append('H7-UX')
    out = run(source)[0]
    assert_interval(interval(out), state='unavailable', reasons=('cohort_universe_unestablished',))
    assert leaf(out, FIELDS[1]).value is None


def test_vf034_b_complete_classifications_make_interval_structurally_unneeded(heroes):
    out = heroes['selection']
    assert_scalar(scalar(out), (5, 6))
    assert_interval(interval(out), state='not_applicable', reasons=('completion_interval_not_needed',))
    assert leaf(out, FIELDS[2]).population_refs[0] is leaf(out, FIELDS[3]).population_refs[0]


def test_vf035_p_h7_retention_and_selection_keep_distinct_valid_pairs(heroes):
    for stage, numerator in (('preservation', 6), ('selection', 5)):
        out = heroes[stage]
        assert out.facts.baseline is not None
        assert out.facts.baseline.anchor == ('answer-run-1', 'intake-1', 'admission')
        assert tuple(member.identifier for member in out.facts.baseline.members) == MEMBERS
        assert all(row.classification == 'Y' for row in out.facts.baseline.rows)
        values = tokens(disclosures(out))
        assert all(value in values for value in ('intake-1', KEYS[stage][1], 'H7-COV-ADM', KEYS[stage][0]))
        assert_scalar(scalar(out, FIELDS[5]), (numerator, 6))


def test_vf035_n_competing_admission_keys_block_transition_only():
    out = run(competing_baseline(small()), 'selection')[0]
    assert out.facts.baseline is None
    assert_scalar(scalar(out), (5, 6))
    assert_scalar(scalar(out, FIELDS[5]), state='unavailable', reasons=('transition_baseline_unestablished',))
    assert {'intake-1', 'intake-2'} <= set(tokens(disclosures(out)))


def test_vf035_m_no_admission_coverage_retains_target_stage_disclosures():
    out = run(remove_admission_coverage(small()), 'selection')[0]
    assert out.facts.baseline is None
    assert_scalar(scalar(out), (5, 6))
    assert_scalar(scalar(out, FIELDS[5]), state='unavailable', reasons=('transition_baseline_unestablished',))
    assert disclosures(out, FIELDS[0])


def test_vf035_b_influence_is_outside_transition_and_output_versions_are_not_members(heroes):
    influence = heroes['influence']
    assert_interval(interval(influence), ((3, 6), (4, 6)))
    assert_scalar(scalar(influence, FIELDS[5]), state='not_applicable', reasons=('no_applicable_subject',))
    source = small()
    for letter in 'ABCDE':
        by_id(source, 'H7-PS-' + letter)['data']['output_refs'] = ['H7-A-V2']
    out = run(source, 'selection')[0]
    assert_scalar(scalar(out, FIELDS[5]), (5, 6))
    assert member_ids(leaf(out, FIELDS[5]).value.population) == MEMBERS
    assert 'H7-A-V2' in tokens(disclosures(out, FIELDS[0]))


def test_vf036_p_unique_fully_admitted_baseline_yields_exact_five_sixths(heroes):
    out = heroes['selection']
    assert_scalar(scalar(out, FIELDS[5]), (5, 6))
    assert next(c for c in leaf(out, FIELDS[5]).check_refs if c.check_id == 'PC18').state == 'met'
    assert member_ids(leaf(out, FIELDS[5]).value.population) == MEMBERS


@pytest.mark.parametrize('defect', ('unknown_admission', 'negative_admission', 'unsupported_admission',
                                  'missing_admission', 'different_members'))
def test_vf036_n_ineligible_baseline_cannot_borrow_standalone_target_fraction(defect):
    source = small()
    if defect == 'different_members':
        by_id(source, 'H7-COV-ADM')['data']['details']['member_refs'] = list(FIVE)
    elif defect == 'missing_admission':
        source['records'] = [row for row in source['records'] if row['id'] != 'H7-PA-E']
    elif defect == 'unsupported_admission':
        by_id(source, 'H7-PA-E')['provenance'].update(basis_kind='declaration', evidence_ref_ids=[])
    else:
        observed(source, 'H7-PA-E', 'unknown' if defect == 'unknown_admission' else 'did_not_occur')
    out = run(source, 'selection')[0]
    assert_scalar(scalar(out), (5, 6))
    assert_scalar(scalar(out, FIELDS[5]), state='unavailable', reasons=('transition_baseline_unestablished',))


def test_vf036_m_different_run_does_not_supply_compatible_admission_baseline():
    source = small()
    for letter in 'ABCDEF':
        by_id(source, 'H7-PA-' + letter)['data']['run_key'] = 'another-run'
    out = run(source, 'selection')[0]
    assert_scalar(scalar(out), (5, 6))
    assert_scalar(scalar(out, FIELDS[5]), state='unavailable', reasons=('transition_baseline_unestablished',))


def test_vf036_b_transition_point_requires_all_target_classifications(w719):
    assert_scalar(scalar(w719, FIELDS[5]), state='unavailable', reasons=('stage_classification_unresolved',))
    assert w719.facts.baseline is not None
    source = five(); observed(source, 'H7-PS-E', 'did_not_occur')
    out = run(source, 'selection')[0]
    assert_scalar(scalar(out, FIELDS[5]), (3, 5))


def test_vf037_p_w719_transition_interval_requires_qualified_same_member_intake(w719):
    assert w719.facts.baseline is not None
    assert tuple(member.identifier for member in w719.facts.baseline.members) == FIVE
    assert all(row.classification == 'Y' for row in w719.facts.baseline.rows)
    assert_interval(interval(w719, FIELDS[6]), ((3, 5), (4, 5)))


@pytest.mark.parametrize('defect', ('ambiguous', 'different_members'))
def test_vf037_n_target_interval_cannot_be_copied_to_ineligible_transition(defect):
    source = five()
    if defect == 'ambiguous':
        competing_baseline(source)
    else:
        by_id(source, 'H7-COV-ADM')['data']['details']['member_refs'] = list(MEMBERS)
    out = run(source, 'selection')[0]
    target = interval(out)
    assert_interval(target, ((3, 5), (4, 5)))
    actual = interval(out, FIELDS[6])
    assert_interval(actual, state='unavailable', reasons=('transition_baseline_unestablished',))
    with pytest.raises(AssertionError):
        assert_interval(target, state='unavailable', reasons=('transition_baseline_unestablished',))


def test_vf037_m_absent_baseline_keeps_target_interval_without_transition_endpoints():
    out = run(remove_admission_coverage(five()), 'selection')[0]
    assert_interval(interval(out), ((3, 5), (4, 5)))
    assert_interval(interval(out, FIELDS[6]), state='unavailable', reasons=('transition_baseline_unestablished',))


def test_vf037_b_exact_transitions_need_no_interval_and_influence_has_no_transition(heroes):
    for stage in ('preservation', 'selection'):
        assert_interval(interval(heroes[stage], FIELDS[6]), state='not_applicable',
                        reasons=('completion_interval_not_needed',))
    assert_interval(interval(heroes['influence'], FIELDS[6]), state='not_applicable',
                    reasons=('no_applicable_subject',))


@pytest.mark.parametrize('variant', ('H7-V01', 'H7-V02', 'H7-V03'))
def test_frozen_seed_variants_do_not_redefine_pipeline_cohort(variant):
    out = run(h.hero(variant))[0]
    assert_partition(partition(out), MEMBERS, ('H7-EA', 'H7-EB', 'H7-ED'),
                     ('H7-EC', 'H7-EF'), ('H7-EE',))
    assert_interval(interval(out), ((3, 6), (4, 6)))


def test_duplicate_positive_logs_do_not_enlarge_cohort_or_hide_native_rows():
    source = small()
    duplicate(source, 'H7-PS-A', 'repeated-A')
    out = run(source, 'selection')[0]
    assert_partition(partition(out), MEMBERS, MEMBERS[:5], ('H7-EF',), ())
    assert_scalar(scalar(out), (5, 6))
    assert {'H7-PS-A', 'repeated-A'} <= set(tokens(disclosures(out, FIELDS[0])))


def test_explicit_anomaly_member_needs_no_invented_claim_or_source_seed():
    source = small()
    by_id(source, 'H7-COV-SEL')['data']['details']['member_refs'] = ['H7-AN1']
    by_id(source, 'H7-COV-SEL')['data']['subject_refs'] = ['anomaly-stage']
    duplicate(source, 'H7-PS-F', 'anomaly-stage')['data']['subject_ref'] = 'H7-AN1'
    out = run(source, 'selection')[0]
    assert_partition(partition(out), ('H7-AN1',), (), ('H7-AN1',), ())
    assert_scalar(scalar(out), (0, 1))
    assert by_id(source, 'H7-AN1')['data']['claim_ref'] is None
    assert 'H7-AN1' not in source['inquiries'][0]['seed_evidence_refs']


def test_cohort_member_from_another_claim_cannot_enter_selected_claim_population():
    source = small()
    claim = copy.deepcopy(by_id(source, 'H7-C1')); claim['id'] = 'other-claim'
    source['records'].append(claim)
    source['inquiries'][0]['target_claim_refs'].append('other-claim')
    by_id(source, 'H7-EA')['data']['claim_ref'] = 'other-claim'
    out = run(source, 'selection')[0]
    assert_scalar(scalar(out), state='unavailable')
    assert_interval(interval(out), state='unavailable')
    assert not out.facts.target.eligible
    assert 'cohort_universe_unestablished' in codes(leaf(out, FIELDS[2])) or 'scope_unestablished' in codes(leaf(out, FIELDS[2]))


@pytest.mark.parametrize('time_case', ('exact', 'earlier', 'date', 'unknown'))
def test_time_specific_stage_classification_needs_exact_observation_instant(time_case):
    source = small()
    known = lambda value: {'state': 'known', 'value': value, 'precision': 'instant'}
    stamp = known('2026-01-10T11:30:00Z')
    by_id(source, 'H7-COV-SEL')['scope']['effective_window'] = {
        'start': known('2026-01-10T11:00:00Z'), 'end': known('2026-01-10T12:00:00Z')}
    times = {'exact': stamp, 'earlier': known('2026-01-10T11:20:00Z'),
             'date': {'state': 'known', 'value': '2026-01-10', 'precision': 'date'},
             'unknown': h.cases.unknown()}
    by_id(source, 'H7-PS-E')['data']['observed_at'] = times[time_case]
    out = run(source, 'selection', temporal_basis='time_specific',
              requested_time=_Node('TimeValue', _Object(tuple(sorted(stamp.items())))))[0]
    if time_case == 'exact':
        assert_partition(partition(out), MEMBERS, MEMBERS[:5], ('H7-EF',), ())
        assert_scalar(scalar(out), (5, 6))
    else:
        assert_partition(partition(out), MEMBERS, MEMBERS[:4], ('H7-EF',), ('H7-EE',))
        assert_scalar(scalar(out), state='unavailable', reasons=('stage_classification_unresolved',))
        assert_interval(interval(out), ((4, 6), (5, 6)))
        row = next(row for row in out.facts.target.rows if row.member.identifier == 'H7-EE')
        assert 'time_applicability_unknown' in row.reason_codes


def test_independent_supplied_support_survives_self_pointer_limitation():
    source = small()
    pointer = copy.deepcopy(by_id(source, 'support'))
    pointer.update(id='self-pointer', reference_kind='record_pointer', record_ref='H7-COV-SEL',
                   artifact_ref=None, locator=None, excerpt=None)
    source['evidence_references'].append(pointer)
    coverage = by_id(source, 'H7-COV-SEL')
    coverage['provenance']['evidence_ref_ids'] = ['support', 'self-pointer']
    supported = run(source, 'selection')[0]
    assert_partition(partition(supported), MEMBERS, MEMBERS[:5], ('H7-EF',), ())
    assert_scalar(scalar(supported), (5, 6), reasons=('self_supporting_assurance',))
    assert supported.facts.target.eligible
    coverage['provenance']['evidence_ref_ids'] = ['self-pointer']
    unsupported = run(source, 'selection')[0]
    assert_scalar(scalar(unsupported), state='unavailable', reasons=('self_supporting_assurance',))
    assert not unsupported.facts.target.eligible


def test_multiple_declared_coverage_dimensions_do_not_change_stage_population():
    source = small()
    dimensions = ['acquisition', 'analytical_method']
    by_id(source, 'H7-COV-SEL')['data']['details']['dimensions'] = dimensions
    out = run(source, 'selection')[0]
    assert_partition(partition(out), MEMBERS, MEMBERS[:5], ('H7-EF',), ())
    assert_scalar(scalar(out), (5, 6))
    assert disclosures(out)['H7-COV-SEL']['data']['details']['dimensions'] == dimensions
    assert all(row.ref.scope.dependency_dimension is None for row in out.results)


def test_disputed_coverage_retains_exact_conflict_basis_reason_and_witness():
    source = small()
    challenge = copy.deepcopy(by_id(source, 'H7-COV-SEL')); challenge['id'] = 'coverage-challenge'
    challenge['data']['details']['state'] = 'partial'
    source['assertions'].append(challenge)
    conflict = copy.deepcopy(by_id(source, 'H7-COV-SEL')); conflict['id'] = 'coverage-dispute'
    conflict['data'] = {'assessment_kind': 'conflict', 'subject_refs': ['H7-COV-SEL', 'coverage-challenge'],
        'details': {'conflict_kind': 'scope_dispute', 'resolution_state': 'unresolved',
                    'resolution_evaluation_ref': None, 'scope_note': 'The finite eligibility boundary is contested.'}}
    conflict['provenance'].update(basis_kind='declaration', evidence_ref_ids=[])
    source['assertions'].append(conflict)
    out = run(source, 'selection')[0]
    row = leaf(out, FIELDS[2])
    assert_scalar(scalar(out), state='unavailable', reasons=('premise_disputed',))
    assert 'coverage-dispute' in {basis.source.identifier for basis in row.basis_refs}
    reasons = [reason for reason in row.reason_refs if reason.code == 'premise_disputed']
    assert any('coverage-dispute' in {ref.identifier for ref in reason.input_refs} for reason in reasons)
    assert any('coverage-dispute' in {entity.identifier for entity in witness.members} for witness in out.witnesses)


def test_expired_admission_coverage_does_not_compete_but_unknown_window_does():
    source = small()
    known = lambda value: {'state': 'known', 'value': value, 'precision': 'instant'}
    stamp = known('2026-01-10T11:30:00Z')
    for identifier in ('H7-COV-ADM', 'H7-COV-SEL'):
        by_id(source, identifier)['scope']['effective_window'] = {
            'start': known('2026-01-10T11:00:00Z'), 'end': known('2026-01-10T12:00:00Z')}
    for letter in 'ABCDEF':
        by_id(source, 'H7-PA-' + letter)['data']['observed_at'] = copy.deepcopy(stamp)
    competing_baseline(source)
    other = by_id(source, 'other-intake-coverage')
    other['scope']['effective_window'] = {
        'start': known('2026-01-10T10:00:00Z'), 'end': known('2026-01-10T10:59:00Z')}
    requested = _Node('TimeValue', _Object(tuple(sorted(stamp.items()))))
    out = run(source, 'selection', temporal_basis='time_specific', requested_time=requested)[0]
    assert_scalar(scalar(out), (5, 6))
    assert_scalar(scalar(out, FIELDS[5]), (5, 6))
    assert out.facts.baseline.anchor == ('answer-run-1', 'intake-1', 'admission')
    other['scope']['effective_window'] = h.cases.window()
    unknown = run(source, 'selection', temporal_basis='time_specific', requested_time=requested)[0]
    assert_scalar(scalar(unknown), (5, 6))
    assert_scalar(scalar(unknown, FIELDS[5]), state='unavailable', reasons=('transition_baseline_unestablished',))


def test_permutations_preserve_finite_member_units_and_exact_transition():
    source = five()
    source['records'].reverse(); source['assertions'].reverse()
    for identifier in ('H7-COV-SEL', 'H7-COV-ADM'):
        by_id(source, identifier)['data']['details']['member_refs'].reverse()
    out = run(source, 'selection')[0]
    assert_partition(partition(out), FIVE, ('H7-EA', 'H7-EB', 'H7-ED'), ('H7-EC',), ('H7-EE',))
    assert_interval(interval(out, FIELDS[6]), ((3, 5), (4, 5)))


def test_cohort_results_are_immutable_and_reject_foreign_witness_ledger():
    source = five(); out, snapshot, owner, job = run(source, 'selection')
    for obj, name in ((out, 'results'), (out.facts, 'target'), (leaf(out, FIELDS[1]).value, 'categories')):
        with pytest.raises((FrozenInstanceError, AttributeError)):
            setattr(obj, name, ())
    other, unused = h.job_pair()
    for ledger in (other.witnesses, _WitnessLedger(owner.witnesses.port)):
        with pytest.raises(TypeError):
            presence._presence(snapshot, context(source, 'selection'), ledger, job, family='SIT-M010',
                coverage_ref='H7-COV-SEL', stage_anchor=('answer-run-1', 'select-1', 'selection'))


def test_interruption_cannot_publish_a_partial_cohort_as_complete(monkeypatch):
    monkeypatch.setattr(resources, 'monotonic_ns', lambda: 100)
    source = five(); snapshot = h.admit(source); ctx = context(source, 'selection')
    owner, job = h.job_pair(); job.charge(1_000_000 - job.used - 100)
    with pytest.raises(_AnalysisAborted) as stopped:
        presence._presence(snapshot, ctx, owner.witnesses, job, family='SIT-M010',
            coverage_ref='H7-COV-SEL', stage_anchor=ctx.operation_anchor)
    assert stopped.value.limit_id == 'WU9-L11'
    with pytest.raises(_AnalysisAborted) as repeated:
        presence._presence(snapshot, ctx, owner.witnesses, job, family='SIT-M010',
            coverage_ref='H7-COV-SEL', stage_anchor=ctx.operation_anchor)
    assert repeated.value is stopped.value
