# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Independent W06 oracles: Definitions 9/21.3, Lineage 7/9.2, VF009--012.

Literal H7 and finite source mutations define expectations, not implementation
output. Every case uses actual admission, a current analysis job and its sole
witness ledger. These owner-local cases do not claim W13 orchestration.
"""
import copy
from dataclasses import FrozenInstanceError, replace
import importlib.util
import json
from pathlib import Path

import pytest

from source_integrity_toolkit.analysis import inventory
from source_integrity_toolkit.analysis import process_comparison as comparison
from source_integrity_toolkit.contracts.bundle import _Array, _Object
from source_integrity_toolkit.contracts.evidence import _Node, _PreparedBundle, _QualificationContext
from source_integrity_toolkit.contracts.execution import _AnalysisAborted, _AuditCancelled
from source_integrity_toolkit.contracts import results
from source_integrity_toolkit.runtime import resources
from source_integrity_toolkit.runtime.boundary import _prepare_value
from source_integrity_toolkit.validation.limits import _WitnessLedger

ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location('sit_w06_admitted_cases', ROOT/'tests/contract/test_typed_records.py')
cases = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cases)
FIELDS = ('submitted_comparison_member_count', 'qualified_process_set_member_count',
          'qualified_origin_set_member_count', 'independence_assessment_disclosures')
DIMENSIONS = ('acquisition', 'analytical_method', 'model_ancestry', 'evaluation_rubric', 'organizational_control')
PARENTS = ('derived_from', 'copies', 'syndicated_from', 'summarizes', 'translates', 'quotes', 'originates_from', 'depends_on')
H7_MEMBERS = ('H7-O1', 'H7-O2')
CORE_IDS = tuple(f'SIT-VF{number:03d}-{category}' for number in range(9, 13) for category in 'PNMB')
NATIVE_KEYS = ('data', 'scope', 'provenance', 'asserted_at', 'lifecycle_state', 'lifecycle_basis_ref_ids')


def hero(variant='H7-01'):
    return json.loads((ROOT/'tests/fixtures/hero'/f'{variant}.bundle.json').read_bytes())


def native(value):
    if type(value) is _Object:
        return {key: native(item) for key, item in value.items}
    if type(value) is _Array:
        return [native(item) for item in value.items]
    return value


def context(source, **changes):
    inquiry = source['inquiries'][0]
    fields = dict(inquiry_ref=inquiry['id'], claim_refs=(inquiry['target_claim_refs'][0],),
                  subject_refs=(), dependency_dimension='acquisition', temporal_basis='snapshot_structural',
                  requested_time=None, coverage_kind='upstream_history', relation_types=PARENTS,
                  graph_view=None, operation_anchor=())
    fields.update(changes)
    return _QualificationContext(**fields)


def admit(source):
    prepared = _prepare_value(source)
    assert type(prepared) is _PreparedBundle
    return prepared


def job_pair():
    owner = resources._new_analysis_budget()
    owner.record_input_acceptance()
    return owner, owner.start_job()


def run(source, assessment='H7-IND12', **changes):
    prepared = admit(source)
    ctx = context(source, **changes)
    owner, job = job_pair()
    ledger = owner.witnesses
    before = job.used
    output = comparison._comparison_profile(prepared, ctx, assessment, ledger, job)
    assert job.used > before
    assert tuple(row.ref.field_key for row in output.results) == FIELDS
    assert len({row.ref._key() for row in output.results}) == 4
    return output, prepared, owner, job


def leaf(output, field):
    return next(row for row in output.results if row.ref.field_key == field)


def codes(row):
    return {reason.code for reason in row.reason_refs}


def reason_sources(row, code):
    return {ref.identifier for reason in row.reason_refs if reason.code == code
            for ref in reason.input_refs}


def assert_scope(row, assessment='H7-IND12', claims=('H7-C1',), dimension='acquisition'):
    assert row.ref.diagnostic_id == 'SIT-M003'
    assert row.ref.scope.inquiry_ref.identifier == 'H7-I1'
    assert tuple(ref.identifier for ref in row.ref.scope.claim_refs) == claims
    assert row.ref.scope.dependency_dimension == dimension
    assert tuple((ref.collection, ref.identifier, ref.selector) for ref in row.ref.scope.target_refs) == (
        () if assessment is None else (('assertions', assessment, None),))
    assert row.interpretation_limit
    for reason in row.reason_refs:
        assert reason.scope is row.ref.scope
        assert row.ref in reason.affected_result_refs
    assert all(check.result_ref is row.ref for check in row.check_refs)


def assert_count(row, members, *, assessment='H7-IND12', claims=('H7-C1',),
                 dimension='acquisition', pc03_state='met'):
    assert_scope(row, assessment, claims, dimension)
    assert (row.execution_state, row.result_state, row.value_kind) == ('completed', 'available', 'count')
    assert row.result_origin == ('inventory' if row.ref.field_key == FIELDS[0] else 'qualification_check')
    assert row.value.value == len(members)
    population = row.value.population
    assert population in row.population_refs and population.scope is row.ref.scope
    assert population.membership_state == 'enumerated_for_scope'
    assert population.unit == ('origin_event' if row.ref.field_key == FIELDS[2] else 'comparison_member')
    assert tuple(ref.identifier for ref in population.member_refs) == members
    assert all(ref.collection == 'records' and ref.selector is None for ref in population.member_refs)
    assert row.basis_refs and row.witness_refs
    checks = {item.check_id: item.state for item in row.check_refs}
    assert checks['PC02'] == checks['PC24'] == 'met'
    assert checks['PC03'] == pc03_state
    if row.ref.field_key in FIELDS[1:3]:
        assert checks['PC05'] == 'met'
        assert checks['PC11'] == 'met'
    if row.ref.field_key == FIELDS[2]:
        assert checks['PC07'] == 'met'


def assert_nonresult(row, reason=None, *, state='unavailable', assessment='H7-IND12', dimension='acquisition'):
    assert_scope(row, assessment, dimension=dimension)
    assert (row.execution_state, row.result_state, row.value) == ('completed', state, None)
    assert row.reason_refs
    if reason is not None:
        assert reason in codes(row)


def disclosure_rows(output):
    row = leaf(output, FIELDS[3])
    assert (row.execution_state, row.result_state, row.value_kind) == ('completed', 'available', 'record_disclosures')
    assert row.result_origin == 'attributed_record'
    assert all(item.source.collection == 'assertions' and item.source.selector is None for item in row.value.records)
    answer = {item.source.identifier: native(item.fields) for item in row.value.records}
    assert len(answer) == len(row.value.records)
    return answer


def assert_native(output, source, identifiers=('H7-IND12',)):
    disclosed = disclosure_rows(output)
    for identifier in identifiers:
        original = cases.by_id(source, identifier)
        assert identifier in disclosed
        for key in NATIVE_KEYS:
            assert disclosed[identifier][key] == original[key]
    return disclosed


def replace_members(row, names):
    """A type-valid count mutant; only the independent source oracle rejects it."""
    population = replace(row.value.population, member_refs=tuple(results._InputRef('records', name) for name in names))
    populations = tuple(population if item is row.value.population else item for item in row.population_refs)
    return replace(row, population_refs=populations, value=results._Count(len(names), population))


def no_comparison(source):
    source['assertions'] = [a for a in source['assertions'] if a['id'] != 'H7-IND12']
    return source


def third_origin(source):
    origin = copy.deepcopy(cases.by_id(source, 'H7-O2'))
    origin['id'] = 'H7-O3'
    origin['data']['event_key'] = 'fictional-third-capture'
    source['records'].append(origin)
    boundary = copy.deepcopy(cases.by_id(source, 'H7-OB2'))
    boundary['id'] = 'H7-OB3'
    boundary['data']['subject_refs'] = ['H7-O3']
    source['assertions'].append(boundary)
    for identifier in ('H7-COV-ACQ', 'H7-COV-COMP'):
        cov = cases.by_id(source, identifier)
        cov['data']['subject_refs'].append('H7-O3')
        cov['data']['details']['member_refs'].append('H7-O3')
    cases.by_id(source, 'H7-SUP-COMPARE')['excerpt'] = (
        'Fictional controlled extension: three named capture procedures were compared; '
        'each uses distinct instruments, operators and raw receipts within the supplied acquisition scope.')
    return source


def setwise(source=None):
    source = third_origin(hero() if source is None else source)
    assessment = cases.by_id(source, 'H7-IND12')
    assessment['data']['subject_refs'].append('H7-O3')
    assessment['data']['details'].update(comparison_form='setwise', examined_dependency_refs=['H7-OB1','H7-OB2','H7-OB3','H7-COV-COMP'])
    return source


def nonorigin(kind):
    source = hero()
    members = ('H7-EVAL', 'H7-HREVIEW') if kind == 'evaluation' else ('H7-MGEN', 'H7-MJUDGE')
    assessment = cases.by_id(source, 'H7-IND12')
    assessment['data']['subject_refs'] = list(members)
    assessment['data']['details'].update(dimension='analytical_method', examined_dependency_refs=['H7-COV-COMP'],
        unexamined_dimensions=[d for d in DIMENSIONS if d != 'analytical_method'])
    coverage = cases.by_id(source, 'H7-COV-COMP')
    coverage['data']['subject_refs'] = list(members)
    coverage['data']['details'].update(dimensions=['analytical_method'], member_refs=list(members), relation_types=[])
    cases.by_id(source, 'H7-SUP-COMPARE')['excerpt'] = (
        'The two named supplied subjects used separately documented analytical procedures. '
        'Their training, rubric, acquisition and organizational dependencies were not examined.')
    return source, members


def add_dependency(source, *, polarity='denied', supported=False, dimension='acquisition', identifier='W06-DENIAL'):
    row = copy.deepcopy(cases.by_id(source, 'H7-IND12'))
    row.update(id=identifier, assertion_kind='relation')
    row['data'] = dict(predicate='depends_on', from_ref='H7-O1', to_ref='H7-O2', polarity=polarity,
                       dimension=dimension, details={})
    if not supported:
        row['provenance'].update(basis_kind='declaration', evidence_ref_ids=[])
    source['assertions'].append(row)
    return row


def weaken(source, kind):
    assertion = cases.by_id(source, 'H7-IND12')
    if kind == 'declaration':
        assertion['provenance'].update(basis_kind='declaration', evidence_ref_ids=[])
    elif kind == 'locator':
        support = cases.by_id(source, 'H7-SUP-COMPARE')
        support.update(reference_kind='external_locator', availability='locator_only', excerpt=None)
    elif kind == 'origin_boundary':
        cases.by_id(source, 'H7-OB1')['data']['details']['boundary_role'] = 'declared_origin'
    else:
        raise AssertionError(kind)
    return source


@pytest.mark.parametrize('identifier', CORE_IDS)
def test_m003_core_source_oracle_and_rejecting_mutant(identifier):
    """Exactly the independent P/N/M/B rows in VALIDATION_PLAN 12.3."""
    number, category = int(identifier[6:9]), identifier[-1]
    field = FIELDS[number - 9]
    source, assessment, dimension, members = hero(), 'H7-IND12', 'acquisition', H7_MEMBERS
    unavailable, inapplicable, required = False, False, None
    if category == 'M' and number in (9, 12):
        source, assessment = no_comparison(source), None
        unavailable = number == 9
        required = 'missing_comparison_assessment'
    elif number == 9 and category == 'B':
        source, members = weaken(setwise(), 'declaration'), ('H7-O1','H7-O2','H7-O3')
    elif number == 10 and category == 'N':
        add_dependency(source)
        unavailable, required = True, 'premise_disputed'
    elif number == 10 and category == 'M':
        weaken(source, 'locator')
        unavailable, required = True, 'support_uninspectable'
    elif (number == 10 and category == 'B') or (number == 11 and category in ('N','B')):
        source, members = nonorigin('model' if category == 'N' else 'evaluation')
        dimension = 'analytical_method'
        inapplicable, required = number == 11, 'no_applicable_subject'
    elif number == 11 and category == 'M':
        weaken(source, 'origin_boundary')
        unavailable, required = True, 'unqualified_origin_boundary'
    elif number == 12 and category in ('N','B'):
        contrary = copy.deepcopy(cases.by_id(source, assessment))
        contrary['id'] = 'W06-CONTRARY'
        contrary['data']['details']['conclusion'] = 'shared_dependency'
        source['assertions'].append(contrary)
    output, _, _, _ = run(source, assessment, dependency_dimension=dimension)
    row = leaf(output, field)
    if unavailable or inapplicable:
        assert_nonresult(row, required, state='not_applicable' if inapplicable else 'unavailable',
                         assessment=assessment, dimension=dimension)
        # A false zero is forbidden even after a completed examination.
        with pytest.raises(AssertionError):
            assert (row.result_state, row.value) == ('available', 0)
        if number == 11 and category == 'N':
            # VF011-N is an output mutant, not merely a missing-input case.
            # Model procedures can qualify while their kind cannot become
            # OriginEvent. The shared representation intentionally cannot
            # resolve these InputRefs; this independent source oracle must.
            process = leaf(output, FIELDS[1])
            assert_count(process, members, dimension=dimension)
            population = replace(process.value.population, scope=row.ref.scope,
                                 unit='origin_event')
            mutant = replace(row, result_state='available',
                             value=results._Count(2, population),
                             population_refs=(population,), reason_refs=())
            assert type(mutant) is results._Result and type(mutant.value) is results._Count
            with pytest.raises(AssertionError):
                assert_nonresult(mutant, 'no_applicable_subject', state='not_applicable',
                                 dimension=dimension)
            assert_nonresult(row, 'no_applicable_subject', state='not_applicable',
                             dimension=dimension)
    elif number != 12:
        assert_count(row, members, assessment=assessment, dimension=dimension)
        mutant = replace_members(row, members + ('invented-third-source',))
        with pytest.raises(AssertionError):
            assert_count(mutant, members, assessment=assessment, dimension=dimension)
        assert_count(row, members, assessment=assessment, dimension=dimension)
    elif assessment is None:
        assert disclosure_rows(output) == {}
        assert 'missing_comparison_assessment' in codes(row)
        with pytest.raises(AssertionError):
            assert 'synthetic-singleton' in disclosure_rows(output)
    else:
        expected = ('H7-IND12','W06-CONTRARY') if category in ('N','B') else ('H7-IND12',)
        assert_native(output, source, expected)
        disclosures = row.value.records
        altered = tuple(item for item in disclosures if item.source.identifier != expected[-1])
        mutant = replace(output, results=tuple(replace(item, value=results._RecordDisclosures(altered)) if item is row else item for item in output.results))
        with pytest.raises(AssertionError):
            assert_native(mutant, source, expected)
        assert_native(output, source, expected)
    if assessment is not None:
        assert_count(leaf(output, FIELDS[0]), members, dimension=dimension)
        assert_native(output, source)
    if number == 9 and category == 'B':
        for qualified in FIELDS[1:3]:
            assert_nonresult(leaf(output, qualified))
            assert codes(leaf(output, qualified)) & {'documentary_basis_incomplete',
                                                    'support_uninspectable'}


def test_h7_all_four_fields_keep_exact_attributed_acquisition_scope_and_full_witnesses():
    source = hero()
    output, prepared, owner, job = run(source)
    for field in FIELDS[:3]:
        assert_count(leaf(output, field), H7_MEMBERS)
    disclosed = assert_native(output, source)['H7-IND12']
    assert disclosed['data']['details']['unexamined_dimensions'] == list(DIMENSIONS[1:])
    assert disclosed['data']['details']['conclusion'] == 'independent_process'
    assert disclosed['provenance']['attributed_to_ref'] == 'H7-REVIEWER'
    assert disclosed['provenance']['evidence_ref_ids'] == ['H7-SUP-COMPARE']
    basis = {ref.source.identifier for ref in leaf(output, FIELDS[2]).basis_refs}
    assert {'H7-IND12','H7-COV-COMP','H7-OB1','H7-OB2',
            'H7-SUP-COMPARE','H7-SUP-ACQ'} <= basis
    assert output.witnesses
    selection = [w for w in output.witnesses if type(w) is comparison._ComparisonWitness]
    assert len(selection) == 1
    selection = selection[0]
    assert selection.prepared is prepared and selection.job_port is job
    assert selection.context is output.facts.context
    assert selection.assessment.identifier == 'H7-IND12'
    assert tuple(member.identifier for member in selection.members) == H7_MEMBERS
    assert tuple(item.identifier for item in selection.examined_assessments) == ('H7-IND12',)
    assert selection.member_count == 3  # two members and the examined assessment occurrence
    payloads = {('comparison_selection',): selection}
    examined = set()
    for witness in output.witnesses:
        if witness is selection:
            continue
        assert witness.kind == 'complete_trace'
        assert witness.graph.prepared is prepared and witness.graph.job_port is job
        assert tuple(witness.graph.context.claim_refs) == ('H7-C1',)
        starts = tuple(node.identifier for node in witness.starts)
        nodes = tuple(node.identifier for node in witness.examined_nodes)
        # H7 has no outgoing acquisition parents from either named origin.
        assert set(starts) <= set(H7_MEMBERS) and starts
        assert nodes == starts
        assert tuple(node.identifier for node in witness.terminals) == nodes
        assert witness.examined_edges == witness.frontiers == witness.observations == ()
        assert witness.member_count == 3 * len(starts)
        examined.update(nodes)
        key = ('complete_trace', ('records','H7-C1'),
               *(('records', identifier) for identifier in starts))
        assert key not in payloads
        payloads[key] = witness
    assert examined == set(H7_MEMBERS)
    for row in output.results:
        assert row.witness_refs
        referenced = []
        for ref in row.witness_refs:
            key = (ref.anchor[0], *((part.collection, part.identifier) for part in ref.anchor[1:]))
            assert key in payloads and ref.kind == 'member_set'
            referenced.append(key)
        assert set(referenced) == set(payloads) and len(referenced) == len(payloads)
    assert owner.witnesses.snapshot() == (0, 0, len(output.witnesses),
                                         sum(w.member_count for w in output.witnesses))
    with pytest.raises((FrozenInstanceError, AttributeError)):
        output.results = ()


@pytest.mark.parametrize('count', (2, 3))
def test_explicit_source_member_population_never_becomes_seed_population(count):
    source = hero() if count == 2 else setwise()
    output, _, _, _ = run(source)
    members = H7_MEMBERS if count == 2 else ('H7-O1','H7-O2','H7-O3')
    for field in FIELDS[:3]:
        assert_count(leaf(output, field), members)


@pytest.mark.parametrize('variant', ('no_seeds', 'H7-V02'))
def test_documentary_comparison_does_not_require_seed_reach_or_unrelated_seed_completion(variant):
    source = hero() if variant == 'no_seeds' else hero(variant)
    if variant == 'no_seeds':
        source['inquiries'][0]['seed_evidence_refs'] = []
        source['inquiries'][0]['seed_artifact_refs'] = []
    output, _, _, _ = run(source)
    for field in FIELDS[:3]:
        assert_count(leaf(output, field), H7_MEMBERS)
        assert not codes(leaf(output, field)) & {'no_seed_contributions','unknown_endpoint'}


@pytest.mark.parametrize('kind', ('evaluation', 'model'))
def test_qualified_nonorigin_procedures_never_count_as_origins(kind):
    source, members = nonorigin(kind)
    output, _, _, _ = run(source, dependency_dimension='analytical_method')
    for field in FIELDS[:2]:
        assert_count(leaf(output, field), members, dimension='analytical_method')
    assert_nonresult(leaf(output, FIELDS[2]), 'no_applicable_subject', state='not_applicable', dimension='analytical_method')
    assert_native(output, source)


@pytest.mark.parametrize('kind', ('declaration', 'locator'))
def test_missing_process_basis_preserves_submitted_population_and_original_assessment(kind):
    positive, _, _, _ = run(hero())
    assert_count(leaf(positive, FIELDS[1]), H7_MEMBERS)
    source = weaken(hero(), kind)
    output, _, _, _ = run(source)
    assert_count(leaf(output, FIELDS[0]), H7_MEMBERS)
    for field in FIELDS[1:3]:
        assert_nonresult(leaf(output, field))
        assert codes(leaf(output, field)) & {'support_uninspectable','documentary_basis_incomplete'}
    assert_native(output, source)


@pytest.mark.parametrize('polarity', ('affirmed', 'denied'))
@pytest.mark.parametrize('supported', (False, True))
def test_relevant_dependency_cannot_disappear_because_its_basis_is_weak(polarity, supported):
    positive, _, _, _ = run(hero())
    assert_count(leaf(positive, FIELDS[1]), H7_MEMBERS)
    source = hero()
    add_dependency(source, polarity=polarity, supported=supported)
    output, _, _, _ = run(source)
    assert_count(leaf(output, FIELDS[0]), H7_MEMBERS)
    for field in FIELDS[1:3]:
        assert_nonresult(leaf(output, field), 'premise_disputed')
        assert 'W06-DENIAL' in reason_sources(leaf(output, field), 'premise_disputed')
    assert_native(output, source, ('H7-IND12','W06-DENIAL'))


def test_other_dimension_dependency_does_not_poison_exact_acquisition_comparison():
    source = hero()
    add_dependency(source, dimension='analytical_method')
    output, _, _, _ = run(source)
    for field in FIELDS[:3]:
        assert_count(leaf(output, field), H7_MEMBERS)
    assert 'premise_disputed' not in codes(leaf(output, FIELDS[1]))


@pytest.mark.parametrize('conclusion', ('shared_dependency','partial_overlap','unknown','not_assessed','not_applicable'))
def test_native_nonindependence_conclusions_are_disclosures_not_qualified_zero(conclusion):
    source = hero()
    cases.by_id(source, 'H7-IND12')['data']['details']['conclusion'] = conclusion
    output, _, _, _ = run(source)
    assert_count(leaf(output, FIELDS[0]), H7_MEMBERS)
    for field in FIELDS[1:3]:
        assert_nonresult(leaf(output, field))
        assert 'documentary_basis_incomplete' not in codes(leaf(output, field))
        assert next(check.state for check in leaf(output, field).check_refs
                    if check.check_id == 'PC05') == 'met'
    assert_native(output, source)


def test_all_five_unexamined_dimensions_remain_native_and_selected_dimension_is_unqualified():
    source = hero()
    cases.by_id(source, 'H7-IND12')['data']['details']['unexamined_dimensions'] = list(DIMENSIONS)
    output, _, _, _ = run(source)
    assert_count(leaf(output, FIELDS[0]), H7_MEMBERS)
    assert_nonresult(leaf(output, FIELDS[1]), 'scope_unestablished')
    assert assert_native(output, source)['H7-IND12']['data']['details']['unexamined_dimensions'] == list(DIMENSIONS)


@pytest.mark.parametrize('claims', (('H7-C1',), ('H7-C1','W06-C2')))
def test_nonempty_multi_claim_assertion_scope_retains_each_explicit_claim(claims):
    source = hero()
    second = copy.deepcopy(cases.by_id(source, 'H7-C1'))
    second['id'] = 'W06-C2'
    second['data']['version_label'] = 'second-exact-version'
    source['records'].append(second)
    source['inquiries'][0]['target_claim_refs'].append('W06-C2')
    for assertion in source['assertions']:
        if assertion['scope']['claim_refs']:
            assertion['scope']['claim_refs'].append('W06-C2')
    output, _, _, _ = run(source, claim_refs=claims)
    for field in FIELDS[:3]:
        assert_count(leaf(output, field), H7_MEMBERS, claims=claims)
    assert assert_native(output, source)['H7-IND12']['scope']['claim_refs'] == ['H7-C1','W06-C2']


def test_overlapping_pairs_and_supplied_set_stay_separate_without_transitive_completion():
    source = third_origin(hero())
    second = copy.deepcopy(cases.by_id(source, 'H7-IND12'))
    second['id'] = 'W06-IND23'
    second['data']['subject_refs'] = ['H7-O2','H7-O3']
    second['data']['details']['examined_dependency_refs'] = ['H7-OB2','H7-OB3','H7-COV-COMP']
    source['assertions'].append(second)
    for identifier, members in [('H7-IND12',H7_MEMBERS), ('W06-IND23',('H7-O2','H7-O3'))]:
        output, _, _, _ = run(source, identifier)
        for field in FIELDS[:3]:
            row = leaf(output, field)
            assert_count(row, members, assessment=identifier)
            for wrong in [('H7-O1','H7-O2','H7-O3'), ('H7-O1','H7-O2','H7-O3','invented-fourth')]:
                with pytest.raises(AssertionError):
                    assert_count(replace_members(row, wrong), members, assessment=identifier)
    source['assertions'] = [item for item in source['assertions']
                            if item['data'].get('assessment_kind') != 'independence']
    missing, _, _, _ = run(source, None)
    for field in FIELDS[:3]:
        assert_nonresult(leaf(missing, field), 'missing_comparison_assessment', assessment=None)


@pytest.mark.parametrize('reverse', (False, True))
def test_conflicting_assessments_survive_array_order_without_prestige_winner(reverse):
    source = hero()
    contrary = copy.deepcopy(cases.by_id(source, 'H7-IND12'))
    contrary['id'] = 'W06-CONTRARY'
    contrary['data']['details']['conclusion'] = 'shared_dependency'
    contrary['provenance'].update(basis_kind='declaration', evidence_ref_ids=[])
    source['assertions'].append(contrary)
    if reverse:
        source['assertions'].reverse()
    output, _, _, _ = run(source)
    assert_nonresult(leaf(output, FIELDS[1]), 'premise_disputed')
    assert_count(leaf(output, FIELDS[0]), H7_MEMBERS)
    assert_native(output, source, ('H7-IND12','W06-CONTRARY'))


@pytest.mark.parametrize('stage', ('profile','facts','results'))
def test_current_job_stop_is_sticky_and_never_yields_completed_profile(stage):
    source = hero()
    prepared, ctx = admit(source), context(source)
    owner, job = job_pair()
    ledger = owner.witnesses
    facts = comparison._comparison_facts(prepared, ctx, 'H7-IND12', ledger, job) if stage == 'results' else None
    job.charge(1_000_000 - job.used)
    used = owner.used, job.used
    def invoke():
        if stage == 'profile':
            return comparison._comparison_profile(prepared, ctx, 'H7-IND12', ledger, job)
        if stage == 'facts':
            return comparison._comparison_facts(prepared, ctx, 'H7-IND12', ledger, job)
        return comparison._comparison_results(facts, job)
    with pytest.raises(_AnalysisAborted) as first:
        invoke()
    assert first.value.limit_id == 'WU9-L11'
    assert (owner.used, job.used) == used
    with pytest.raises(_AnalysisAborted) as again:
        invoke()
    assert again.value is first.value


@pytest.mark.parametrize('foreign', ('other_invocation','unissued'))
def test_only_current_invocation_runtime_issued_ledger_can_retain_comparison(foreign):
    source = hero()
    prepared, ctx = admit(source), context(source)
    owner, job = job_pair()
    issued = owner.witnesses
    if foreign == 'other_invocation':
        other, _ = job_pair()
        ledger = other.witnesses
    else:
        ledger = _WitnessLedger(issued.port)
    with pytest.raises(TypeError):
        comparison._comparison_profile(prepared, ctx, 'H7-IND12', ledger, job)
    assert issued._retained_witnesses == issued._retained_members == 0


def add_alias(source):
    row = copy.deepcopy(cases.by_id(source, 'H7-IND12'))
    row.update(id='W06-ALIAS', assertion_kind='relation')
    row['data'] = dict(predicate='same_identity_as', from_ref='H7-O1', to_ref='H7-O2',
                       polarity='affirmed', dimension=None, details={'identity_level':'origin_event'})
    source['assertions'].append(row)
    return row


@pytest.mark.parametrize('supported', (False, True))
def test_relevant_alias_withholds_qualified_counts_without_merging_input_members(supported):
    source = hero()
    alias = add_alias(source)
    if not supported:
        alias['provenance'].update(basis_kind='declaration', evidence_ref_ids=[])
    original = copy.deepcopy(source)
    output, _, _, _ = run(source)
    assert source == original
    assert_count(leaf(output, FIELDS[0]), H7_MEMBERS)
    for field in FIELDS[1:3]:
        assert_nonresult(leaf(output, field), 'identity_unresolved')
        assert 'W06-ALIAS' in reason_sources(leaf(output, field), 'identity_unresolved')
    assert_native(output, source, ('H7-IND12','W06-ALIAS'))


@pytest.mark.parametrize('form', ('pairwise', 'setwise'))
def test_two_members_are_valid_under_either_explicit_comparison_form(form):
    source = hero()
    cases.by_id(source, 'H7-IND12')['data']['details']['comparison_form'] = form
    output, _, _, _ = run(source)
    for field in FIELDS[:3]:
        assert_count(leaf(output, field), H7_MEMBERS)
    assert assert_native(output, source)['H7-IND12']['data']['details']['comparison_form'] == form


def known(value):
    return dict(state='known', value=value, precision='instant')


def requested(value):
    return _Node('TimeValue', _Object(tuple(sorted(known(value).items()))))


@pytest.mark.parametrize('case', ('strict_inside', 'unknown', 'strict_outside', 'boundary', 'reversed'))
def test_time_specific_qualification_preserves_native_window_without_endpoint_invention(case):
    source = hero()
    assertion = cases.by_id(source, 'H7-IND12')
    window = assertion['scope']['effective_window']
    stamp = '2026-01-10T13:00:00Z'
    if case == 'unknown':
        window['start'] = cases.unknown()
    elif case == 'strict_outside':
        window.update(start=known('2026-01-11T00:00:00Z'), end=known('2026-01-12T00:00:00Z'))
    elif case == 'boundary':
        window['start'] = known(stamp)
    elif case == 'reversed':
        window.update(start=known('2026-01-10T15:00:00Z'), end=known('2026-01-10T11:00:00Z'))
    output, _, _, _ = run(source, temporal_basis='time_specific', requested_time=requested(stamp))
    assert_count(leaf(output, FIELDS[0]), H7_MEMBERS)
    if case == 'strict_inside':
        assert_count(leaf(output, FIELDS[1]), H7_MEMBERS)
    else:
        for field in FIELDS[1:3]:
            assert_nonresult(leaf(output, field))
            assert codes(leaf(output, field)) & {'time_applicability_unknown','temporal_inconsistency'}
    assert_native(output, source)


@pytest.mark.parametrize('requested_members', (('H7-O1',), ('H7-O1','H7-O2','H7-EA')))
def test_caller_subject_subset_or_superset_cannot_replace_the_supplied_comparison(requested_members):
    source = hero()
    output, _, _, _ = run(source, subject_refs=requested_members)
    for field in FIELDS[1:3]:
        assert_nonresult(leaf(output, field), 'scope_unestablished')
    assert_native(output, source)
    if leaf(output, FIELDS[0]).result_state == 'available':
        # Exact submitted-source size can survive a caller's incompatible
        # scope, with the real provider's unmet qualification kept visible.
        assert_count(leaf(output, FIELDS[0]), H7_MEMBERS, pc03_state='unmet')


def test_self_supporting_assurance_is_not_process_documentation():
    source = hero()
    support = cases.by_id(source, 'H7-SUP-COMPARE')
    support.update(reference_kind='record_pointer', availability='supplied', artifact_ref=None,
                   record_ref='H7-IND12', locator=None, excerpt=None)
    output, _, _, _ = run(source)
    assert_count(leaf(output, FIELDS[0]), H7_MEMBERS)
    assert_nonresult(leaf(output, FIELDS[1]), 'self_supporting_assurance')
    assert_native(output, source)


@pytest.mark.parametrize('field', ('method','attributed_to_ref'))
def test_missing_named_assessor_or_method_never_certifies_native_independent_label(field):
    source = hero()
    assessment = cases.by_id(source, 'H7-IND12')
    assessment['provenance'][field] = None
    assessment.setdefault('gaps', []).append(dict(field='provenance.'+field, reason='not_recorded',
                                                  detail='The required documentary basis was not supplied.'))
    output, _, _, _ = run(source)
    assert_count(leaf(output, FIELDS[0]), H7_MEMBERS)
    assert_nonresult(leaf(output, FIELDS[1]), 'documentary_basis_incomplete')
    assert_native(output, source)


def test_source_array_permutation_preserves_exact_member_count_and_native_subject_order():
    source = hero()
    assessment = cases.by_id(source, 'H7-IND12')
    assessment['data']['subject_refs'].reverse()
    source['records'].reverse()
    source['assertions'].reverse()
    output, _, _, _ = run(source)
    for field in FIELDS[:3]:
        assert_count(leaf(output, field), H7_MEMBERS)
    assert assert_native(output, source)['H7-IND12']['data']['subject_refs'] == ['H7-O2','H7-O1']


@pytest.mark.parametrize('boundary', ('witnesses','members'))
def test_shared_retention_limit_never_returns_clipped_comparison_members(boundary):
    source = hero()
    prepared, ctx = admit(source), context(source)
    owner, job = job_pair()
    ledger = owner.witnesses
    ledger.retain(ledger.reserve(**{boundary: 20_000 if boundary == 'witnesses' else 100_000}))
    retained = ledger._retained_witnesses, ledger._retained_members
    with pytest.raises(_AnalysisAborted) as stop:
        comparison._comparison_profile(prepared, ctx, 'H7-IND12', ledger, job)
    assert stop.value.limit_id == 'WU9-L13'
    assert (ledger._retained_witnesses, ledger._retained_members) == retained
    with pytest.raises(_AnalysisAborted) as again:
        comparison._comparison_profile(prepared, ctx, 'H7-IND12', ledger, job)
    assert again.value is stop.value


@pytest.mark.parametrize('cause', ('deadline','cancelled','backwards'))
def test_sticky_clock_or_cancellation_never_becomes_completed_missing_assessment(cause, monkeypatch):
    now = [100]
    monkeypatch.setattr(resources, 'monotonic_ns', lambda: now[0])
    source = hero()
    prepared, ctx = admit(source), context(source)
    owner, job = job_pair()
    ledger = owner.witnesses
    if cause == 'deadline':
        now[0] += 60_000_000_001
    elif cause == 'backwards':
        now[0] -= 1
    else:
        def interrupted():
            raise KeyboardInterrupt('private-input-canary')
        monkeypatch.setattr(resources, 'monotonic_ns', interrupted)
    error = _AuditCancelled if cause == 'cancelled' else _AnalysisAborted
    with pytest.raises(error) as first:
        comparison._comparison_profile(prepared, ctx, None, ledger, job)
    with pytest.raises(error) as second:
        comparison._comparison_profile(prepared, ctx, None, ledger, job)
    assert second.value is first.value
    assert 'private-input-canary' not in str(first.value)
    assert owner.input_state == 'accepted'
    assert ledger._retained_witnesses == ledger._retained_members == 0


def test_completed_comparison_facts_cannot_be_reused_in_another_job():
    source = hero()
    prepared, ctx = admit(source), context(source)
    owner, job = job_pair()
    facts = comparison._comparison_facts(prepared, ctx, 'H7-IND12', owner.witnesses, job)
    owner.finish_job(job)
    next_job = owner.start_job()
    with pytest.raises((TypeError, _AnalysisAborted)):
        comparison._comparison_results(facts, next_job)


# The approved R01 adds this exact-population provider without changing M001.
def provider_source(*, multi=False, missing=False):
    data = cases.pool()
    if multi:
        data['inquiries'][0]['target_claim_refs'] = ['claim','claim2']
    if not missing:
        row = cases.assertion('CMP','assessment',dict(assessment_kind='independence',
            subject_refs=['origin','origin2'],details=dict(comparison_form='pairwise',dimension='acquisition',
                conclusion='independent_process',examined_dependency_refs=[],
                unexamined_dimensions=['analytical_method','model_ancestry','evaluation_rubric','organizational_control'],
                coverage_ref=None,scope_note='Precisely the two supplied origin records.')))
        row['gaps']=[dict(field='data.details.coverage_ref',reason='not_recorded',detail='This inventory does not assert documentary qualification.')]
        if multi: row['scope']['claim_refs']=['claim','claim2']
        data['assertions'].append(row)
    prepared = _prepare_value(data)
    assert type(prepared) is _PreparedBundle
    return data, prepared


def provider_context(**updates):
    values = dict(inquiry_ref='inquiry',claim_refs=('claim',),subject_refs=(),dependency_dimension='acquisition',
                  temporal_basis='snapshot_structural',requested_time=None,coverage_kind=None,
                  relation_types=(),graph_view=None,operation_anchor=())
    values.update(updates)
    return _QualificationContext(**values)


def provider_inspect(prepared,ctx,job,ref='CMP'):
    return inventory._comparison_inventory_facts(prepared,ctx,ref,job)


@pytest.mark.parametrize('claims', (('claim',),('claim','claim2')))
def test_provider_exact_source_members_and_provider_ownership_not_seed_population(claims):
    data,prepared=provider_source(multi=len(claims)==2)
    ctx=provider_context(claim_refs=claims)
    owner,job=job_pair();before=job.used
    facts=provider_inspect(prepared,ctx,job)
    assert job.used>before
    assert tuple(e.identifier for e in facts.members)==('origin','origin2')
    assert facts.assessment.identifier=='CMP'
    assert facts.inquiry.identifier=='inquiry'
    assert facts.prepared is prepared and facts.context is ctx and facts.job_port is job
    assert (facts.pc03.check_id,facts.pc03.owner,facts.pc03.state)==('PC03','SOURCE_INVENTORY','met')
    assert facts.pc03.prepared is prepared and facts.pc03.context is ctx
    selected={(r.collection,r.record_id,r.selector) for r in facts.pc03.input_refs}
    assert ('assertions','CMP','data.subject_refs') in selected
    assert not any(r[2]=='seed_evidence_refs' for r in selected)
    assert facts.selection_refs==facts.pc03.input_refs
    with pytest.raises((FrozenInstanceError,AttributeError)):facts.members=()
    # Source membership selection does not certify independent_process.
    assert data['assertions'][0]['provenance']['basis_kind']=='declaration'


@pytest.mark.parametrize('members', (('origin','origin2'),('origin2','origin')))
def test_provider_nonempty_caller_population_must_equal_whole_source_set(members):
    _,prepared=provider_source();ctx=provider_context(subject_refs=members);_,job=job_pair()
    facts=provider_inspect(prepared,ctx,job)
    assert tuple(e.identifier for e in facts.members)==('origin','origin2')


@pytest.mark.parametrize('members', (('origin',),('origin','origin2','e')))
def test_provider_subset_and_superset_are_rejected_without_mutating_source_selection(members):
    _,prepared=provider_source();_,job=job_pair()
    facts=provider_inspect(prepared,provider_context(subject_refs=members),job)
    assert facts.pc03.state=='unmet' and facts.scope_compatible is False
    assert tuple(e.identifier for e in facts.members)==('origin','origin2')
    assert 'scope_unestablished' in facts.reason_codes


def test_provider_missing_assessment_is_unknown_population_not_available_zero():
    _,prepared=provider_source(missing=True);ctx=provider_context();_,job=job_pair()
    facts=provider_inspect(prepared,ctx,job,None)
    assert facts.assessment is None and facts.members==()
    assert facts.pc03.state=='unknown'
    assert facts.pc03.prepared is prepared and facts.pc03.context is ctx


def test_provider_none_cannot_hide_an_actual_applicable_assessment():
    _,prepared=provider_source();_,job=job_pair()
    with pytest.raises(TypeError):provider_inspect(prepared,provider_context(),job,None)


@pytest.mark.parametrize('ref', ('origin','unknown-CMP',True,7))
def test_provider_selector_is_exact_supplied_independence_assessment(ref):
    _,prepared=provider_source();_,job=job_pair()
    with pytest.raises(TypeError):provider_inspect(prepared,provider_context(),job,ref)


@pytest.mark.parametrize('claims', ((),('claim2',)))
def test_provider_empty_or_nontarget_claim_scope_is_rejected(claims):
    _,prepared=provider_source();_,job=job_pair()
    with pytest.raises(TypeError):provider_inspect(prepared,provider_context(claim_refs=claims),job)


@pytest.mark.parametrize('changed', ('prepared','context','job'))
def test_provider_consumer_requires_actual_prepared_context_and_current_job_identities(changed):
    _,prepared=provider_source();ctx=provider_context();owner,job=job_pair()
    facts=provider_inspect(prepared,ctx,job)
    inventory._check_comparison_inventory(facts,prepared,ctx,job)
    foreign_prepared=provider_source()[1] if changed=='prepared' else prepared
    foreign_context=replace(ctx) if changed=='context' else ctx
    foreign_job=job_pair()[1] if changed=='job' else job
    with pytest.raises(TypeError):
        inventory._check_comparison_inventory(facts,foreign_prepared,foreign_context,foreign_job)


def test_provider_stale_job_cannot_reuse_completed_selection_authority():
    _,prepared=provider_source();ctx=provider_context();owner,job=job_pair()
    facts=provider_inspect(prepared,ctx,job);owner.finish_job(job);later=owner.start_job()
    with pytest.raises((TypeError,_AnalysisAborted)):
        inventory._check_comparison_inventory(facts,prepared,ctx,later)


def test_provider_paid_limit_stops_before_selection_with_sticky_original_cause():
    _,prepared=provider_source();ctx=provider_context();owner,job=job_pair()
    job.charge(1_000_000-job.used);before=owner.used,job.used
    with pytest.raises(_AnalysisAborted) as first:provider_inspect(prepared,ctx,job)
    assert first.value.limit_id=='WU9-L11'
    assert (owner.used,job.used)==before
    with pytest.raises(_AnalysisAborted) as again:provider_inspect(prepared,ctx,job)
    assert again.value is first.value


def test_provider_old_m001_seed_contract_is_not_reinterpreted_as_comparison_population():
    _,prepared=provider_source(multi=True);owner,job=job_pair()
    baseline=inventory._inventory_facts(prepared,provider_context(),job)
    assert tuple(e.identifier for e in baseline.seed_evidence)==('e','e2')
    with pytest.raises(TypeError):inventory._inventory_facts(prepared,provider_context(subject_refs=('origin','origin2')),job)
    with pytest.raises(TypeError):inventory._inventory_facts(prepared,provider_context(claim_refs=('claim','claim2')),job)


def test_provider_explicit_compatible_unresolved_member_remains_placeholder_in_exact_population():
    data,unused=provider_source()
    member=cases.by_id(data,'origin2')
    member.update(kind='unresolved_reference',data=dict(expected_kinds=['origin_event'],reason='withheld',description='Only a represented origin identity gap.'))
    prepared=_prepare_value(data)
    assert type(prepared) is _PreparedBundle
    ctx=provider_context();_,job=job_pair()
    facts=provider_inspect(prepared,ctx,job)
    assert tuple(e.identifier for e in facts.members)==('origin','origin2')
    assert tuple(e.kind for e in facts.members)==('origin_event','unresolved_reference')
    assert facts.pc03.state=='met'


def test_profile_executes_owned_exact_population_provider_in_the_actual_job(monkeypatch):
    observed = []
    actual = inventory._comparison_inventory_facts
    def observe(prepared, ctx, assessment, job):
        fact = actual(prepared, ctx, assessment, job)
        observed.append(fact)
        return fact
    monkeypatch.setattr(comparison, '_comparison_inventory_facts', observe)
    output, prepared, _, job = run(hero())
    assert len(observed) == 1
    fact = observed[0]
    assert output.facts.inventory is fact
    assert type(fact).__module__ == inventory.__name__
    assert fact.prepared is prepared and fact.job_port is job
    assert fact.pc03.prepared is prepared and fact.pc03.context is fact.context
    assert (fact.pc03.owner, fact.pc03.state) == ('SOURCE_INVENTORY', 'met')
    assert tuple(item.identifier for item in fact.members) == H7_MEMBERS
    expected = {('assertions','H7-IND12','data.subject_refs')}
    assert expected <= {(ref.collection, ref.record_id, ref.selector) for ref in fact.selection_refs}
    for row in output.results:
        pc03 = next(check for check in row.check_refs if check.check_id == 'PC03')
        assert pc03.state == 'met'
        assert expected <= {(ref.collection, ref.identifier, ref.selector) for ref in pc03.input_refs}


def test_comparison_scope_cannot_upgrade_boundary_basis_from_only_one_claim():
    source = hero()
    second = copy.deepcopy(cases.by_id(source, 'H7-C1'))
    second['id'] = 'W06-C2'
    second['data']['version_label'] = 'second-exact-version'
    source['records'].append(second)
    source['inquiries'][0]['target_claim_refs'].append('W06-C2')
    cases.by_id(source, 'H7-IND12')['scope']['claim_refs'].append('W06-C2')
    one, _, _, _ = run(source)
    assert_count(leaf(one, FIELDS[2]), H7_MEMBERS)
    both, _, _, _ = run(source, claim_refs=('H7-C1','W06-C2'))
    assert_count(leaf(both, FIELDS[0]), H7_MEMBERS, claims=('H7-C1','W06-C2'))
    origin = leaf(both, FIELDS[2])
    assert (origin.execution_state, origin.result_state, origin.value) == ('completed','unavailable',None)
    assert codes(origin) & {'scope_unestablished','unqualified_origin_boundary','upstream_coverage_incomplete'}
    assert tuple(ref.identifier for ref in origin.ref.scope.claim_refs) == ('H7-C1','W06-C2')
    assert_native(both, source)


def test_missing_assessment_preserves_all_requested_nonresults_and_empty_supplied_disclosure():
    source = no_comparison(hero())
    output, _, _, _ = run(source, None)
    for field in FIELDS[:3]:
        row = leaf(output, field)
        assert_nonresult(row, 'missing_comparison_assessment', assessment=None)
        assert next(check.state for check in row.check_refs if check.check_id == 'PC03') == 'unknown'
    assert disclosure_rows(output) == {}
    assert 'missing_comparison_assessment' in codes(leaf(output, FIELDS[3]))


def change_frozen_field(fields, path, value):
    key, *rest = path
    return _Object(tuple((name, change_frozen_field(item, rest, value) if rest else value)
                         if name == key else (name, item) for name, item in fields.items))


def test_disclosure_output_mutant_cannot_turn_supplied_conclusion_into_tool_authentication():
    source = hero()
    output, _, _, _ = run(source)
    assert_native(output, source)
    row = leaf(output, FIELDS[3])
    records = tuple(replace(record, fields=change_frozen_field(record.fields,
        ('data','details','conclusion'), 'tool_authenticated_independence'))
        if record.source.identifier == 'H7-IND12' else record for record in row.value.records)
    mutant = replace(output, results=tuple(replace(item, value=results._RecordDisclosures(records))
                     if item is row else item for item in output.results))
    assert type(leaf(mutant, FIELDS[3]).value) is results._RecordDisclosures
    with pytest.raises(AssertionError):
        assert_native(mutant, source)
    assert_native(output, source)


def test_explicit_pairwise_and_setwise_records_keep_separate_result_targets():
    source = setwise()
    combined = cases.by_id(source, 'H7-IND12')
    combined['id'] = 'W06-IND123'
    for identifier, members in [('W06-IND12',['H7-O1','H7-O2']),('W06-IND23',['H7-O2','H7-O3'])]:
        pair = copy.deepcopy(combined)
        pair['id'] = identifier
        pair['data']['subject_refs'] = members
        pair['data']['details']['comparison_form'] = 'pairwise'
        source['assertions'].append(pair)
    scopes = []
    for identifier, members in [('W06-IND12',H7_MEMBERS),('W06-IND23',('H7-O2','H7-O3')),
                                ('W06-IND123',('H7-O1','H7-O2','H7-O3'))]:
        output, _, _, _ = run(source, identifier)
        for field in FIELDS[:3]:
            assert_count(leaf(output, field), members, assessment=identifier)
        assert_native(output, source, (identifier,))
        scopes.append(leaf(output, FIELDS[0]).ref.scope._key())
    assert len(set(scopes)) == 3


@pytest.mark.parametrize('case', ('basis','scope','lifecycle','time','conflict','partial','null_gap'))
def test_named_comparison_coverage_uses_actual_basis_without_inventing_global_completeness(case):
    # Reporting 14.2 separates relevant supporting premises from unrelated
    # global completeness. This named coverage is a real supplied premise.
    positive, _, _, _ = run(hero())
    assert_count(leaf(positive, FIELDS[1]), H7_MEMBERS)
    source = hero()
    coverage = cases.by_id(source, 'H7-COV-COMP')
    changes = {}
    expected = None
    if case == 'basis':
        coverage['provenance'].update(basis_kind='declaration', evidence_ref_ids=[])
        expected = 'documentary_basis_incomplete'
    elif case == 'scope':
        claim = copy.deepcopy(cases.by_id(source, 'H7-C1'))
        claim['id'] = 'W06-C2'
        claim['data']['version_label'] = 'second-exact-version'
        source['records'].append(claim)
        source['inquiries'][0]['target_claim_refs'].append('W06-C2')
        coverage['scope']['claim_refs'] = ['W06-C2']
        expected = 'scope_unestablished'
    elif case == 'lifecycle':
        coverage.update(lifecycle_state='withdrawn', lifecycle_basis_ref_ids=['H7-SUP-COMPARE'])
        coverage['provenance']['qualifications'].append('This supported record describes withdrawal of the coverage assessment.')
        expected = 'scope_unestablished'
    elif case == 'time':
        coverage['scope']['effective_window']['start'] = cases.unknown()
        changes = dict(temporal_basis='time_specific', requested_time=requested('2026-01-10T13:00:00Z'))
        expected = 'time_applicability_unknown'
    elif case == 'conflict':
        opposing = copy.deepcopy(coverage)
        opposing['id'] = 'W06-COUNTER-COVERAGE'
        opposing['data']['details']['state'] = 'partial'
        source['assertions'].append(opposing)
        dispute = copy.deepcopy(cases.by_id(source, 'H7-IND12'))
        dispute['id'] = 'W06-COVERAGE-CONFLICT'
        dispute['data'] = dict(assessment_kind='conflict',
            subject_refs=['H7-COV-COMP','W06-COUNTER-COVERAGE'],
            details=dict(conflict_kind='scope_dispute', resolution_state='unresolved',
                         resolution_evaluation_ref=None, scope_note='The two attributed coverage records disagree.'))
        source['assertions'].append(dispute)
        expected = 'premise_disputed'
    elif case == 'partial':
        coverage['data']['details']['state'] = 'partial'
    else:
        assessment = cases.by_id(source, 'H7-IND12')
        assessment['data']['details']['coverage_ref'] = None
        assessment.setdefault('gaps', []).append(dict(field='data.details.coverage_ref', reason='not_recorded',
                                                      detail='No separate full coverage claim accompanies these process materials.'))
    output, _, _, _ = run(source, **changes)
    assert_count(leaf(output, FIELDS[0]), H7_MEMBERS)
    assert_native(output, source)
    if case in ('partial','null_gap'):
        assert_count(leaf(output, FIELDS[1]), H7_MEMBERS)
    else:
        for field in FIELDS[1:3]:
            row = leaf(output, field)
            assert_nonresult(row, expected)
            assert 'H7-COV-COMP' in reason_sources(row, expected)
    if case != 'null_gap':
        assert_native(output, source, ('H7-COV-COMP',))


def test_distinct_missing_comparison_queries_keep_distinct_typed_scope_slots():
    source = third_origin(no_comparison(hero()))
    outputs = []
    for members in (('H7-O1','H7-O2'), ('H7-O1','H7-O3')):
        output, _, _, _ = run(source, None, subject_refs=members)
        outputs.append(output)
        for field in FIELDS[:3]:
            assert_nonresult(leaf(output, field), 'missing_comparison_assessment', assessment=None)
        assert disclosure_rows(output) == {}
        anchor = leaf(output, FIELDS[0]).ref.scope.operation_anchor
        requested_refs = {(part.collection, part.identifier, part.selector)
                          for part in anchor if type(part) is results._InputRef}
        assert {('records', member, None) for member in members} <= requested_refs
        assert all(row.value is None for row in output.results[:3])
    for field in FIELDS:
        assert leaf(outputs[0], field).ref._key() != leaf(outputs[1], field).ref._key()
    repeated, _, _, _ = run(source, None, subject_refs=('H7-O2','H7-O1'))
    for field in FIELDS:
        assert leaf(repeated, field).ref._key() == leaf(outputs[0], field).ref._key()
