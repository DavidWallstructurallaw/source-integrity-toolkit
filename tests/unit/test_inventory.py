# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Independent SOURCE_INVENTORY oracles: Definitions 20.1/21.1 and VF001--005.

The literal member sets below come from the frozen H7/source clauses, never
from product output. Real admission and actual jobs exercise this private
component; neither public W13 execution nor independent sources are claimed.
"""
import copy
from dataclasses import FrozenInstanceError, replace
import importlib.util
import json
from pathlib import Path

import pytest

from source_integrity_toolkit.analysis import inventory
from source_integrity_toolkit.contracts.evidence import _PreparedBundle, _QualificationContext
from source_integrity_toolkit.contracts.execution import _AnalysisAborted, _AuditCancelled
from source_integrity_toolkit.contracts import results
from source_integrity_toolkit.runtime.boundary import _prepare_value
from source_integrity_toolkit.runtime import resources
from source_integrity_toolkit.validation.limits import _WitnessLedger

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('sit_w05_inventory_cases', ROOT/'tests/contract/test_typed_records.py')
cases = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cases)

FIELDS = ('nominal_seed_artifact_record_count', 'unresolved_seed_artifact_reference_count',
          'seed_evidence_item_count', 'claim_artifact_record_count',
          'claim_unassigned_seed_artifact_record_count')
UNITS = ('artifact_record', 'unresolved_reference', 'evidence_item', 'artifact_record', 'artifact_record')
H7_ARTIFACTS = ('H7-A', 'H7-B', 'H7-C', 'H7-D', 'H7-E', 'H7-F')
H7_SEEDS = ('H7-EA', 'H7-EB', 'H7-EC', 'H7-ED', 'H7-EE', 'H7-EF')
CORE_IDS = tuple('SIT-VF%03d-%s' % (number, category) for number in range(1, 6) for category in 'PNMB')


def hero(variant='H7-01'):
    return json.loads((ROOT/'tests/fixtures/hero'/f'{variant}.bundle.json').read_bytes())


def context(source, **changes):
    inquiry = source['inquiries'][0]
    values = dict(inquiry_ref=inquiry['id'], claim_refs=(inquiry['target_claim_refs'][0],),
                  subject_refs=(), dependency_dimension=None, temporal_basis='snapshot_structural',
                  requested_time=None, coverage_kind=None, relation_types=(), graph_view=None,
                  operation_anchor=())
    values.update(changes)
    return _QualificationContext(**values)


def admit(source):
    value = _prepare_value(source)
    assert type(value) is _PreparedBundle
    return value


def job_pair():
    budget = resources._new_analysis_budget()
    budget.record_input_acceptance()
    return budget, budget.start_job()


def run(source, **changes):
    prepared, ctx = admit(source), context(source, **changes)
    owner, job = job_pair()
    ledger = owner.witnesses
    before = job.used
    output = inventory._inventory_profile(prepared, ctx, ledger, job)
    assert job.used > before
    return output, prepared, owner, job


def leaf(output, field):
    return next(row for row in output.results if row.ref.field_key == field)


def assert_cell(row, field, members):
    index = FIELDS.index(field)
    assert row.ref.diagnostic_id == 'SIT-M001'
    assert row.ref.field_key == field
    assert (row.execution_state, row.result_state, row.result_origin, row.value_kind) == (
        'completed', 'available', 'inventory', 'count')
    population = row.value.population
    assert row.population_refs == (population,)
    assert population.scope is row.ref.scope
    assert population.unit == UNITS[index]
    assert population.membership_state == 'enumerated_for_scope'
    assert tuple(ref.identifier for ref in population.member_refs) == members
    assert row.value.value == len(members)
    assert bool(row.ref.scope.claim_refs) is (index in (2, 3))
    assert row.ref.scope.dependency_dimension is None
    assert row.ref.scope.graph_view is None
    assert {check.check_id: check.state for check in row.check_refs} == {
        'PC01': 'met', 'PC02': 'met', 'PC03': 'met', 'PC24': 'met'}
    assert row.basis_refs and row.witness_refs
    assert 'actual sources' in row.interpretation_limit


def replace_members(row, names):
    """Representationally valid output mutant; only source semantics reject it."""
    members = tuple(results._InputRef('records', name) for name in names)
    population = replace(row.value.population, member_refs=members)
    return replace(row, population_refs=(population,), value=results._Count(len(members), population))


def two_claims():
    source = cases.pool()
    inquiry = source['inquiries'][0]
    inquiry['target_claim_refs'] = ['claim', 'claim2']
    inquiry['seed_artifact_refs'] = ['artifact']
    cases.by_id(source, 'e2')['data'].update(claim_ref='claim2', artifact_ref='artifact')
    return source


def core_case(identifier):
    """Hand-authored source fixtures for all 20 mandatory M001 core cells."""
    number, category = int(identifier[6:9]), identifier[-1]
    source, members, mutant = hero(), (), ('invented-source',)
    if number == 1:
        members = H7_ARTIFACTS
        if category == 'N':
            mutant = H7_ARTIFACTS + ('H7-ANSWER',)
        elif category == 'M':
            source, members = cases.sparse(), ()
        elif category == 'B':
            source, members, mutant = two_claims(), ('artifact',), ('artifact', 'artifact2')
    elif number == 2:
        if category == 'P':
            source = cases.pool()
            source['inquiries'][0].update(seed_artifact_refs=['unresolved'], seed_evidence_refs=[])
            members, mutant = ('unresolved',), ()
        elif category == 'N':
            source, mutant = hero('H7-V02'), ('H7-UX',)
        elif category == 'B':
            source = cases.pool()
            source['inquiries'][0]['seed_artifact_refs'] = ['unresolved']
            cases.by_id(source, 'e')['data']['artifact_ref'] = 'unresolved'
            cases.by_id(source, 'e2')['data']['artifact_ref'] = 'unresolved'
            members, mutant = ('unresolved',), ('unresolved', 'artifact')
    elif number == 3:
        members = H7_SEEDS
        if category == 'N':
            mutant = H7_SEEDS + ('H7-ER1',)
        elif category == 'M':
            source = cases.pool()
            source['inquiries'][0]['seed_evidence_refs'] = []
            members = ()
        elif category == 'B':
            source = cases.pool()
            third = copy.deepcopy(cases.by_id(source, 'e'))
            third['id'] = 'e3'
            source['records'].append(third)
            source['inquiries'][0]['seed_evidence_refs'] = ['e', 'e2', 'e3']
            members, mutant = ('e', 'e2', 'e3'), ('e', 'e2')
    elif number == 4:
        members = H7_ARTIFACTS
        if category == 'N':
            source = cases.pool()
            for name in ('artifact', 'artifact2'):
                cases.by_id(source, name)['data']['locators'] = ['https://invalid.example/same']
            cases.by_id(source, 'artifact2')['data'].update(work_key='artifact', version_label='v2')
            members, mutant = ('artifact', 'artifact2'), ('artifact',)
        elif category == 'M':
            source = cases.pool()
            source['inquiries'][0].update(seed_artifact_refs=[], seed_evidence_refs=['e'])
            cases.by_id(source, 'e')['data']['artifact_ref'] = 'unresolved'
            members, mutant = (), ('unresolved',)
        elif category == 'B':
            source, members = two_claims(), ('artifact',)
    elif number == 5:
        if category == 'P':
            source = cases.pool()
            source['inquiries'][0]['seed_evidence_refs'] = []
            members, mutant = ('artifact', 'artifact2'), ()
        elif category == 'N':
            mutant = ('H7-ANSWER',)
        elif category == 'M':
            source = cases.sparse()
        elif category == 'B':
            source, mutant = two_claims(), ('artifact',)
            source['inquiries'][0]['seed_evidence_refs'] = ['e2']
    return source, FIELDS[number - 1], members, mutant


@pytest.mark.parametrize('identifier', CORE_IDS, ids=CORE_IDS)
def test_m001_core_source_oracle_and_rejecting_mutant(identifier):
    source, field, expected, bad_members = core_case(identifier)
    output, prepared, owner, job = run(source)
    row = leaf(output, field)
    assert_cell(row, field, expected)
    with pytest.raises(AssertionError):
        assert_cell(replace_members(row, bad_members), field, expected)
    # A mutant rejection must not corrupt the accepted source-bound positive.
    assert_cell(row, field, expected)
    if identifier == 'SIT-VF004-M':
        assert 'unknown_endpoint' in tuple(reason.code for reason in row.reason_refs)
    if identifier == 'SIT-VF004-B':
        other, _, _, _ = run(source, claim_refs=('claim2',))
        assert_cell(leaf(other, field), field, ('artifact',))
        assert_cell(leaf(other, FIELDS[0]), FIELDS[0], ('artifact',))


def test_complete_population_witnesses_and_shared_occurrence_accounting():
    output, prepared, owner, job = run(hero())
    assert len(output.results) == len(output.witnesses) == 5
    assert tuple(row.ref.field_key for row in output.results) == FIELDS
    for row, witness, expected in zip(output.results, output.witnesses,
                                      (H7_ARTIFACTS, (), H7_SEEDS, H7_ARTIFACTS, ())):
        assert_cell(row, row.ref.field_key, expected)
        assert witness.ref is row.witness_refs[0]
        assert witness.population is row.value.population
        assert witness.members is row.value.population.member_refs
        assert witness.member_count == len(expected)
    assert owner.witnesses.snapshot() == (0, 0, 5, 18)
    assert output.facts.prepared is prepared and output.facts.job_port is job
    assert output.facts.pc03.context is output.facts.context
    assert output.facts.pc03.prepared is prepared
    assert output.facts.pc03.state == 'met'
    assert len(output.facts.pc03.input_refs) == 14


def test_explicit_artifact_union_includes_all_seed_bindings_but_no_metadata():
    source = cases.pool()
    source['inquiries'][0]['seed_artifact_refs'] = ['dataset']
    output, _, _, _ = run(source)
    assert_cell(leaf(output, FIELDS[0]), FIELDS[0], ('artifact', 'artifact2', 'dataset'))
    assert_cell(leaf(output, FIELDS[4]), FIELDS[4], ('dataset',))
    assert_cell(leaf(output, FIELDS[3]), FIELDS[3], ('artifact', 'artifact2'))


def test_repeated_artifact_positions_do_not_multiply_records_or_contributions():
    source = cases.pool()
    # Closed-shape admission requires unique entries within each ref array.
    # The valid repeated source positions are explicit Artifact plus bindings
    # from two distinct contributions, not a structurally invalid duplicate.
    source['inquiries'][0]['seed_artifact_refs'] = ['artifact']
    cases.by_id(source, 'e2')['data']['artifact_ref'] = 'artifact'
    output, _, _, _ = run(source)
    assert_cell(leaf(output, FIELDS[0]), FIELDS[0], ('artifact',))
    assert_cell(leaf(output, FIELDS[2]), FIELDS[2], ('e', 'e2'))


def test_unresolved_artifact_reasons_stay_in_their_actual_claim_population():
    source = two_claims()
    clean, _, _, _ = run(source)
    assert leaf(clean, FIELDS[3]).reason_refs == ()
    cases.by_id(source, 'e2')['data']['artifact_ref'] = 'unresolved'
    other_gap, _, _, _ = run(source)
    assert_cell(leaf(other_gap, FIELDS[3]), FIELDS[3], ('artifact',))
    assert leaf(other_gap, FIELDS[3]).reason_refs == ()
    assert_cell(leaf(other_gap, FIELDS[1]), FIELDS[1], ('unresolved',))
    selected_gap, _, _, _ = run(source, claim_refs=('claim2',))
    row = leaf(selected_gap, FIELDS[3])
    assert_cell(row, FIELDS[3], ())
    assert tuple(reason.code for reason in row.reason_refs) == ('unknown_endpoint',)
    assert tuple(ref.identifier for ref in row.reason_refs[0].input_refs) == ('unresolved',)


def test_exact_shared_witness_and_member_ceilings_retain_all_five_populations():
    source = hero()
    prepared, ctx = admit(source), context(source)
    owner, job = job_pair()
    ledger = owner.witnesses
    ledger.retain(ledger.reserve(witnesses=19_995, members=99_982))
    output = inventory._inventory_profile(prepared, ctx, ledger, job)
    assert len(output.witnesses) == 5
    assert tuple(w.member_count for w in output.witnesses) == (6, 0, 6, 6, 0)
    assert ledger.snapshot() == (0, 0, 20_000, 100_000)
    with pytest.raises(_AnalysisAborted) as stopped:
        inventory._inventory_profile(prepared, ctx, ledger, job)
    assert stopped.value.limit_id == 'WU9-L13'
    assert ledger._retained_witnesses == 20_000
    assert ledger._retained_members == 100_000


@pytest.mark.parametrize('changes', ({'claim_refs': ('claim2',)}, {'claim_refs': ()},
    {'claim_refs': ('claim', 'claim2')}, {'subject_refs': ('e',)}, {'subject_refs': ('artifact',)}))
def test_pc03_rejects_wrong_claim_or_smaller_subject_population(changes):
    source = cases.pool()
    prepared = admit(source)
    owner, job = job_pair()
    positive = inventory._inventory_facts(prepared, context(source, subject_refs=('e2', 'e')), job)
    assert tuple(row.identifier for row in positive.seed_evidence) == ('e', 'e2')
    with pytest.raises(TypeError):
        inventory._inventory_facts(prepared, context(source, **changes), job)
    assert inventory._inventory_facts(prepared, context(source), job).pc03.state == 'met'


def test_fact_and_profile_are_immutable_and_no_cross_job_completion_reuse():
    output, _, owner, job = run(cases.pool())
    with pytest.raises(FrozenInstanceError):
        output.facts.artifacts = ()
    with pytest.raises(FrozenInstanceError):
        output.results = ()
    owner.finish_job(job)
    later = owner.start_job()
    with pytest.raises(TypeError):
        inventory._check_inventory(output.facts, later)
    with pytest.raises(_AnalysisAborted):
        inventory._check_inventory(output.facts, job)


@pytest.mark.parametrize('foreign', ('other_invocation', 'fresh_same_owner'))
def test_only_runtime_issued_single_invocation_witness_ledger_is_accepted(foreign):
    source = cases.pool()
    prepared, ctx = admit(source), context(source)
    owner, job = job_pair()
    issued = owner.witnesses
    if foreign == 'other_invocation':
        other, other_job = job_pair()
        wrong = other.witnesses
    else:
        wrong = _WitnessLedger(job)
    with pytest.raises(TypeError):
        inventory._inventory_profile(prepared, ctx, wrong, job)
    output = inventory._inventory_profile(prepared, ctx, issued, job)
    assert len(output.results) == 5


@pytest.mark.parametrize('operation', ('facts', 'profile'))
def test_job_limit_stops_without_available_profile_or_counter_refund(operation, monkeypatch):
    monkeypatch.setattr(resources, 'monotonic_ns', lambda: 100)
    source = cases.pool()
    prepared, ctx = admit(source), context(source)
    owner, job = job_pair()
    ledger = owner.witnesses
    job.charge(1_000_000 - job.used)
    before = owner.used, job.used
    with pytest.raises(_AnalysisAborted) as first:
        if operation == 'facts':
            inventory._inventory_facts(prepared, ctx, job)
        else:
            inventory._inventory_profile(prepared, ctx, ledger, job)
    assert first.value.limit_id == 'WU9-L11'
    assert (owner.used, job.used) == before
    with pytest.raises(_AnalysisAborted) as repeated:
        inventory._inventory_facts(prepared, ctx, job)
    assert repeated.value is first.value
    assert ledger._retained_witnesses == ledger._retained_members == 0


@pytest.mark.parametrize('resource', ('witnesses', 'members'))
def test_prospective_shared_witness_limits_do_not_clip_members(resource):
    source = cases.pool()
    prepared, ctx = admit(source), context(source)
    owner, job = job_pair()
    ledger = owner.witnesses
    token = ledger.reserve(**{resource: 20_000 if resource == 'witnesses' else 100_000})
    ledger.retain(token)
    with pytest.raises(_AnalysisAborted) as stopped:
        inventory._inventory_profile(prepared, ctx, ledger, job)
    assert stopped.value.limit_id == 'WU9-L13'
    assert ledger._retained_witnesses == (20_000 if resource == 'witnesses' else 0)
    assert ledger._retained_members == (100_000 if resource == 'members' else 0)


@pytest.mark.parametrize('stop', ('deadline', 'cancellation'))
def test_existing_clock_or_cancel_cause_cannot_become_an_empty_inventory(stop, monkeypatch):
    now = [100]
    monkeypatch.setattr(resources, 'monotonic_ns', lambda: now[0])
    source = cases.pool()
    prepared, ctx = admit(source), context(source)
    owner, job = job_pair()
    ledger = owner.witnesses
    if stop == 'deadline':
        now[0] += 60_000_000_001
        exception = _AnalysisAborted
    else:
        with pytest.raises(_AuditCancelled) as first:
            owner.cancel()
        exception = _AuditCancelled
    with pytest.raises(exception) as observed:
        inventory._inventory_profile(prepared, ctx, ledger, job)
    if stop == 'deadline':
        assert observed.value.limit_id == 'WU9-L12'
    else:
        assert observed.value is first.value
    assert owner.input_state == 'accepted'
    assert ledger._retained_witnesses == 0
