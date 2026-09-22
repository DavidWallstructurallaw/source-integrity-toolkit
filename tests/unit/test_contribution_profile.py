# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W07 source oracles for VF013--VF017, Definitions 22--23.

Detect invented acquisition parents, denominator laundering, nonexclusive
incidence normalization, incomplete-row promotion and unsupported HHI gates.
H7/W7 literal expectations precede narrow output mutants; completed component
jobs are reused within module fixtures, never presented as public orchestration.
"""
import copy
from dataclasses import FrozenInstanceError, replace
import importlib.util
import json
from pathlib import Path

import pytest

from source_integrity_toolkit.analysis import contribution_profile as contribution
from source_integrity_toolkit.contracts.execution import _AnalysisAborted
from source_integrity_toolkit.runtime import resources
from source_integrity_toolkit.validation.limits import _WitnessLedger

_spec = importlib.util.spec_from_file_location('sit_w07_origin_helpers', Path(__file__).with_name('test_origins.py'))
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)
ROOT = h.ROOT
ORIGIN_LABELS = ('unresolved_or_conflicted', 'contains_baseline_or_scope_cut',
                 'contains_declared_origin', 'multiple_documented_origins', 'single_documented_origin')
FIELDS = {
    'SIT-M004': ('per_seed_origin_memberships', 'origin_incidence_counts',
                 'seed_origin_dispositions', 'documentary_origin_resolution_fraction'),
    'SIT-M005': ('single_origin_contribution_hhi',),
    'SIT-M006': ('immediate_evidence_layer_dispositions', 'inherited_only_seed_fraction',
                 'inherited_only_completion_interval'),
}
H7_SEEDS = ('H7-EA', 'H7-EB', 'H7-EC', 'H7-ED', 'H7-EE', 'H7-EF')
H7_ROWS = {'H7-EA': ('H7-O1',), 'H7-EB': ('H7-O1',), 'H7-EC': ('H7-O1',),
           'H7-ED': ('H7-O1',), 'H7-EE': ('H7-O1',), 'H7-EF': ('H7-O2',)}


def run(source, family='SIT-M004', **changes):
    snapshot = h.prepared(source)
    ctx = replace(h.context(source), **changes)
    owner, job = h.job_pair()
    ledger = owner.witnesses
    before = (owner.used, job.used, ledger._retained_witnesses, ledger._retained_members)
    out = contribution._contribution_profile(snapshot, ctx, ledger, job, family=family)
    assert owner.used - before[0] == job.used - before[1] > 0
    assert out.facts.prepared is snapshot and out.facts.context is ctx
    assert out.facts.job_port is job
    assert ledger._retained_witnesses - before[2] == len(out.witnesses)
    assert ledger._retained_members - before[3] == sum(w.member_count for w in out.witnesses)
    assert tuple(row.ref.field_key for row in out.results) == FIELDS[family]
    for row in out.results:
        assert row.ref.diagnostic_id == family
        scope = row.ref.scope
        assert scope.inquiry_ref.identifier == ctx.inquiry_ref
        assert tuple(ref.identifier for ref in scope.claim_refs) == ctx.claim_refs
        assert scope.dependency_dimension == ctx.dependency_dimension
        assert scope.temporal_basis == ctx.temporal_basis
        assert tuple(ref.identifier for ref in scope.target_refs) == ctx.subject_refs
        assert row.basis_refs and row.interpretation_limit
        assert all(check.result_ref is row.ref for check in row.check_refs)
        assert all(reason.scope is scope and row.ref in reason.affected_result_refs for reason in row.reason_refs)
        assert all(witness.scope is scope for witness in row.witness_refs)
        checks = {check.check_id: check.state for check in row.check_refs}
        assert checks['PC01'] == checks['PC02'] == checks['PC24'] == 'met'
        assert {'PC03', 'PC04', 'PC05', 'PC06', 'PC08', 'PC09', 'PC10'} <= checks.keys()
        for provider in (out.facts.inventory.pc03, out.facts.pc04):
            actual = next(check for check in row.check_refs if check.check_id == provider.check_id)
            assert actual.state == provider.state
            assert {(ref.collection, ref.identifier, ref.selector or '') for ref in actual.input_refs} == {
                (ref.collection, ref.record_id, ref.selector) for ref in provider.input_refs}
        if family == 'SIT-M005':
            assert checks['PC12'] == ('met' if row.result_state == 'available' else 'unmet')
            assert 'PC07' in checks
        elif family == 'SIT-M006':
            assert 'PC13' in checks
        else:
            assert 'PC07' in checks
    return out, snapshot, owner, job


def leaf(out, field):
    return next(row for row in out.results if row.ref.field_key == field)


def codes(row):
    return {reason.code for reason in row.reason_refs}


def members(population):
    assert population.unit == 'evidence_item'
    assert population.membership_state == 'enumerated_for_scope'
    assert population.selection_rule
    assert all(ref.collection == 'records' and ref.selector is None for ref in population.member_refs)
    return tuple(ref.identifier for ref in population.member_refs)


def incidence_view(row):
    assert (row.execution_state, row.result_state, row.value_kind) == ('completed', 'available', 'incidence')
    value = row.value
    assert value.population in row.population_refs
    return {'members': members(value.population), 'nonexclusive': value.nonexclusive,
            'rows': {r.member_ref.identifier: tuple(o.identifier for o in r.origin_refs) for r in value.memberships},
            'counts': {origin.identifier: count for origin, count in value.origin_counts}}


def assert_incidence(actual, population, rows, counts):
    assert actual == {'members': population, 'nonexclusive': True, 'rows': rows, 'counts': counts}


def partition_view(row):
    assert (row.execution_state, row.result_state, row.value_kind) == ('completed', 'available', 'partition')
    assert row.value.population in row.population_refs
    return {'members': members(row.value.population),
            'categories': {c.label: (c.count, tuple(ref.identifier for ref in c.member_refs)) for c in row.value.categories}}


def assert_partition(actual, population, labels, buckets):
    assert actual == {'members': population,
                      'categories': {label: (len(bucket), bucket) for label, bucket in zip(labels, buckets)}}


def fraction_view(row):
    value = row.value
    return {'execution': row.execution_state, 'state': row.result_state,
            'value': None if value is None else (value.numerator, value.denominator),
            'members': members(row.population_refs[0]), 'reasons': codes(row)}


def assert_fraction(actual, population, ratio=None, *, state='available', reasons=()):
    assert actual['execution'] == 'completed' and actual['state'] == state
    assert actual['value'] == ratio and actual['members'] == population
    assert set(reasons) <= actual['reasons']


def origins(out):
    return incidence_view(leaf(out, 'per_seed_origin_memberships'))


def dispositions(out):
    return partition_view(leaf(out, 'seed_origin_dispositions'))


def resolution(out):
    return fraction_view(leaf(out, 'documentary_origin_resolution_fraction'))


def hhi(out):
    return fraction_view(leaf(out, 'single_origin_contribution_hhi'))


def direct_case(roles=('documented_origin', 'documented_origin', 'documented_origin')):
    """W7-01/16/17 finite direct populations; no inferred semantic deduplication."""
    source = h.small(edges=(), roles=())
    seeds, roots = [], []
    for index, role in enumerate(roles):
        seed = 'e' if index == 0 else 'e' + str(index + 1)
        root = 'origin' if index == 0 else 'origin' + str(index + 1)
        if index >= 2:
            for template, identifier in (('e', seed), ('origin', root)):
                obj = copy.deepcopy(h.cases.by_id(source, template)); obj['id'] = identifier
                source['records'].append(obj)
        seeds.append(seed); roots.append(root)
        source['assertions'].append(h.relation('direct-' + seed, 'originates_from', seed, root))
        h.add_boundary(source, root, role=role, identifier='boundary-' + seed)
    source['inquiries'][0].update(seed_evidence_refs=seeds,
        seed_artifact_refs=list(dict.fromkeys(h.cases.by_id(source, seed)['data']['artifact_ref'] for seed in seeds)))
    h.cases.by_id(source, 'coverage')['data']['details']['member_refs'] = seeds + roots
    return source


def diamond(*, two_origins=False):
    source = h.small(edges=(('left', 'derived_from', 'e', 'e2'), ('right', 'derived_from', 'e', 'e3'),
        ('left-root', 'originates_from', 'e2', 'origin'),
        ('right-root', 'originates_from', 'e3', 'origin2' if two_origins else 'origin')),
        roles=(('origin', 'documented_origin'), ('origin2', 'documented_origin')) if two_origins else (('origin', 'documented_origin'),))
    other = copy.deepcopy(h.cases.by_id(source, 'e2')); other['id'] = 'e3'; source['records'].append(other)
    h.cases.by_id(source, 'left')['data']['details']['portion_note'] = 'roughly half from each'
    return source


def shared_unknown():
    source = h.small(edges=(('unknown-e', 'derived_from', 'e', 'unresolved'),
        ('unknown-e2', 'derived_from', 'e2', 'unresolved')), seeds=('e', 'e2'), roles=(), coverage_state='partial')
    h.cases.by_id(source, 'unresolved')['data']['expected_kinds'] = ['evidence_item']
    return source


@pytest.fixture(scope='module')
def heroes():
    # Eight actual family jobs. Every later oracle reuses these completed facts.
    return {variant: {family: run(h.hero(variant), family)[0] for family in ('SIT-M004', 'SIT-M005')}
            for variant in ('H7-01', 'H7-V01', 'H7-V02', 'H7-V03')}


@pytest.mark.parametrize('variant', ('H7-01', 'H7-V01', 'H7-V02', 'H7-V03'))
def test_vf013_to_vf017_frozen_hero_populations_incidence_dispositions_and_gates(heroes, variant):
    """VF013--017 P/M/B: fixed seeds, branch evidence and exact whole denominators."""
    out, scalar = heroes[variant]['SIT-M004'], heroes[variant]['SIT-M005']
    population, rows = H7_SEEDS, dict(H7_ROWS)
    counts, buckets, ratio, scalar_ratio = {'H7-O1': 5, 'H7-O2': 1}, ((), (), (), (), H7_SEEDS), (6, 6), (26, 36)
    reasons = ()
    if variant == 'H7-V01':
        population = H7_SEEDS[:5]; rows.pop('H7-EF'); counts = {'H7-O1': 5}
        buckets, ratio, scalar_ratio = ((), (), (), (), population), (5, 5), (25, 25)
    elif variant == 'H7-V02':
        population += ('H7-EU',); rows['H7-EU'] = ()
        buckets, ratio, scalar_ratio = (('H7-EU',), (), (), (), H7_SEEDS), (6, 7), None
        reasons = ('unknown_endpoint', 'upstream_coverage_incomplete')
    elif variant == 'H7-V03':
        population += ('H7-EG',); rows['H7-EG'] = ('H7-O1', 'H7-O2')
        counts, buckets, ratio, scalar_ratio = {'H7-O1': 6, 'H7-O2': 2}, ((), (), (), ('H7-EG',), H7_SEEDS), (7, 7), None
        reasons = ('multi_origin_unallocated',)
    assert_incidence(origins(out), population, rows, counts)
    assert_incidence(incidence_view(leaf(out, 'origin_incidence_counts')), population, rows, counts)
    assert_partition(dispositions(out), population, ORIGIN_LABELS, buckets)
    assert_fraction(resolution(out), population, ratio)
    assert_fraction(hhi(scalar), population, scalar_ratio, state='available' if scalar_ratio else 'unavailable', reasons=reasons)
    # The immutable logical fixture is an additional independent source oracle.
    golden = json.loads((ROOT / 'tests/golden' / (variant + '.logical.json')).read_bytes())
    assert population == tuple(golden['populations']['source_contributions'])
    assert rows == {r['seed_ref']: tuple(r['qualified_origin_refs']) for r in golden['origin_rows']}
    assert tuple(len(bucket) for bucket in buckets) == tuple(golden['origin_partition_counts'])
    paths = h.path_view(out.facts.origin_facts)
    for seed in H7_SEEDS[:5] if variant == 'H7-V01' else H7_SEEDS:
        assert h.H7_PATHS[seed] in paths[seed]
    if variant == 'H7-V02':
        assert (('H7-EU', 'H7-UX'), ('H7-LU',)) in paths['H7-EU']
    for profile in (out, scalar):
        for row in profile.results:
            assert len(row.witness_refs) == 1
            witness, = h.resolved_witnesses(row, profile.facts.origin_facts)
            assert witness is profile.facts.origin_facts.inventory_witness
            assert tuple(seed.identifier for seed in witness.starts) == population
            expected_edges = {'H7-L01', 'H7-L02', 'H7-L03', 'H7-L04', 'H7-L05', 'H7-L06'}
            if variant != 'H7-V01': expected_edges.add('H7-L07')
            if variant == 'H7-V02': expected_edges.add('H7-LU')
            if variant == 'H7-V03': expected_edges.update(('H7-LG1', 'H7-LG2'))
            assert {edge.source_ref.record_id for edge in witness.examined_edges} == expected_edges


def test_vf014_n_and_vf016_n_reject_normalized_incidence_and_dropped_unresolved_denominator(heroes):
    """Accept real full profiles first, then reject only the prescribed numeric corruption."""
    multi = origins(heroes['H7-V03']['SIT-M004'])
    pop = H7_SEEDS + ('H7-EG',); rows = dict(H7_ROWS, **{'H7-EG': ('H7-O1', 'H7-O2')})
    assert_incidence(multi, pop, rows, {'H7-O1': 6, 'H7-O2': 2})
    mutant = copy.deepcopy(multi); mutant['counts'] = {'H7-O1': 6 / 8, 'H7-O2': 2 / 8}
    with pytest.raises(AssertionError): assert_incidence(mutant, pop, rows, {'H7-O1': 6, 'H7-O2': 2})
    for variant, expected, wrong in (('H7-V02', (6, 7), (6, 6)), ('H7-V03', (7, 7), (6, 7))):
        baseline = resolution(heroes[variant]['SIT-M004'])
        population = H7_SEEDS + (('H7-EU',) if variant == 'H7-V02' else ('H7-EG',))
        assert_fraction(baseline, population, expected)
        mutant = copy.deepcopy(baseline); mutant['value'] = wrong
        with pytest.raises(AssertionError): assert_fraction(mutant, population, expected)


def test_vf017_n_reject_half_allocation_and_resolved_subset_hhi(heroes):
    for variant, extra, reasons, wrong in (
        ('H7-V02', 'H7-EU', ('unknown_endpoint', 'upstream_coverage_incomplete'), (26, 36)),
        ('H7-V03', 'H7-EG', ('multi_origin_unallocated',), (130, 196))):
        baseline = hhi(heroes[variant]['SIT-M005']); population = H7_SEEDS + (extra,)
        assert_fraction(baseline, population, state='unavailable', reasons=reasons)
        mutant = copy.deepcopy(baseline); mutant.update(state='available', value=wrong)
        with pytest.raises(AssertionError): assert_fraction(mutant, population, state='unavailable', reasons=reasons)


def test_vf013_n_artifact_context_cannot_create_an_acquisition_parent():
    source = h.small(edges=(), roles=())
    for pred in ('cites', 'published_by', 'owned_by', 'generated_by'):
        row = h.cases.relation(pred); h.supplied(row); source['assertions'].append(row)
    out = run(source)[0]
    baseline = origins(out)
    assert_incidence(baseline, ('e',), {'e': ()}, {})
    mutant = copy.deepcopy(baseline); mutant['rows']['e'] = ('origin',); mutant['counts']['origin'] = 1
    with pytest.raises(AssertionError): assert_incidence(mutant, ('e',), {'e': ()}, {})


@pytest.mark.parametrize('two_origins', (False, True))
def test_vf013_b_paths_and_distinct_origins_are_different_units(two_origins):
    source = diamond(two_origins=two_origins)
    out, scalar = run(source)[0], run(source, 'SIT-M005')[0]
    roots = ('origin', 'origin2') if two_origins else ('origin',)
    assert_incidence(origins(out), ('e',), {'e': roots}, {root: 1 for root in roots})
    assert_partition(dispositions(out), ('e',), ORIGIN_LABELS,
                     ((), (), (), ('e',), ()) if two_origins else ((), (), (), (), ('e',)))
    assert_fraction(resolution(out), ('e',), (1, 1))
    if two_origins: assert_fraction(hhi(scalar), ('e',), state='unavailable', reasons=('multi_origin_unallocated',))
    else: assert_fraction(hhi(scalar), ('e',), (1, 1))
    trace = out.facts.origin_facts.seed_traces[0]
    edge_ids = {edge.source_ref.record_id for edge in trace.reachability.edges}
    assert {'left', 'right', 'left-root', 'right-root'} <= edge_ids
    assert h.cases.by_id(source, 'left')['data']['details']['portion_note'] == 'roughly half from each'


def test_vf015_b_declared_baseline_scope_cut_precedence_is_exhaustive():
    source = direct_case(('documented_origin', 'declared_origin', 'reference_baseline', 'scope_cut'))
    out, scalar = run(source)[0], run(source, 'SIT-M005')[0]
    assert_partition(dispositions(out), ('e', 'e2', 'e3', 'e4'), ORIGIN_LABELS,
                     ((), ('e3', 'e4'), ('e2',), (), ('e',)))
    assert_fraction(resolution(out), ('e', 'e2', 'e3', 'e4'), (1, 4))
    assert_fraction(hhi(scalar), ('e', 'e2', 'e3', 'e4'), state='unavailable', reasons=('declared_origin_only', 'baseline_or_scope_cut'))
    # A declared branch coexisting with a baseline has one governing category.
    source['assertions'].append(h.relation('additional-declared', 'originates_from', 'e3', 'origin2'))
    out = run(source)[0]
    assert_partition(dispositions(out), ('e', 'e2', 'e3', 'e4'), ORIGIN_LABELS,
                     ((), ('e3', 'e4'), ('e2',), (), ('e',)))


@pytest.mark.parametrize('branch', ('unknown', 'disputed'))
def test_vf015_n_late_bad_branch_preserves_known_incidence_but_blocks_complete_row(branch):
    source = h.small()
    # Preserve the documentary origin's own finite boundary qualification.
    # The later seed gap must not rewrite this independent, origin-only area.
    h.add_coverage(source, ('origin',), subjects=('origin',), identifier='origin-only-coverage')
    h.cases.by_id(source, 'boundary0')['data']['details']['coverage_ref'] = 'origin-only-coverage'
    if branch == 'unknown':
        h.cases.by_id(source, 'unresolved')['data']['expected_kinds'] = ['evidence_item']
        source['assertions'].append(h.relation('zz-late-parent', 'derived_from', 'e', 'unresolved'))
        h.cases.by_id(source, 'coverage')['data']['details']['member_refs'].append('unresolved')
        h.cases.by_id(source, 'coverage')['data']['details'].update(state='partial', universe_enumerated=False)
        reason = 'unknown_endpoint'
    else:
        source['assertions'].append(h.relation('zz-late-parent', 'derived_from', 'e', 'e2'))
        denial = h.relation('zz-late-denial', 'derived_from', 'e', 'e2'); denial['data']['polarity'] = 'denied'
        source['assertions'].append(denial)
        h.cases.by_id(source, 'coverage')['data']['details']['member_refs'].append('e2')
        reason = 'premise_disputed'
    out, scalar = run(source)[0], run(source, 'SIT-M005')[0]
    assert_incidence(origins(out), ('e',), {'e': ('origin',)}, {'origin': 1})
    baseline = dispositions(out)
    assert_partition(baseline, ('e',), ORIGIN_LABELS, (('e',), (), (), (), ()))
    mutant = copy.deepcopy(baseline)
    mutant['categories']['unresolved_or_conflicted'] = (0, ())
    mutant['categories']['single_documented_origin'] = (1, ('e',))
    with pytest.raises(AssertionError): assert_partition(mutant, ('e',), ORIGIN_LABELS, (('e',), (), (), (), ()))
    assert_fraction(hhi(scalar), ('e',), state='unavailable')
    assert reason in hhi(scalar)['reasons']


def test_vf016_b_all_unknown_is_zero_resolution_over_known_population():
    out = run(shared_unknown())[0]
    assert_incidence(origins(out), ('e', 'e2'), {'e': (), 'e2': ()}, {})
    assert_partition(dispositions(out), ('e', 'e2'), ORIGIN_LABELS, (('e', 'e2'), (), (), (), ()))
    assert_fraction(resolution(out), ('e', 'e2'), (0, 2))


def test_vf016_m_and_vf017_b_empty_population_has_no_ratio():
    source = h.small(seeds=(), edges=(), roles=())
    out, scalar = run(source)[0], run(source, 'SIT-M005')[0]
    assert_incidence(origins(out), (), {}, {})
    assert_partition(dispositions(out), (), ORIGIN_LABELS, ((), (), (), (), ()))
    assert_fraction(resolution(out), (), state='unavailable', reasons=('no_seed_contributions',))
    assert_fraction(hhi(scalar), (), state='unavailable', reasons=('no_seed_contributions',))


def test_vf017_b_three_buckets_need_no_independence_assessment_or_agreement():
    source = direct_case()
    # W7-01 explicitly permits removing comparisons without changing HHI.
    source['assertions'].append(h.supplied(h.cases.relation('contradicts')))
    scalar = run(source, 'SIT-M005')[0]
    assert_fraction(hhi(scalar), ('e', 'e2', 'e3'), (3, 9))
    assert not hhi(scalar)['reasons'] & {'missing_comparison_assessment', 'multi_origin_unallocated'}
    # W7-16 contribution decomposition is explicit, even with shared Artifacts.
    h.cases.by_id(source, 'direct-e2')['data']['to_ref'] = 'origin'
    h.cases.by_id(source, 'e2')['data']['artifact_ref'] = 'artifact'
    scalar = run(source, 'SIT-M005')[0]
    assert_fraction(hhi(scalar), ('e', 'e2', 'e3'), (5, 9))


@pytest.mark.parametrize('defect,reason', (
    ('partial', 'upstream_coverage_incomplete'), ('terminal', 'unqualified_origin_boundary'),
    ('basis', 'documentary_basis_incomplete'), ('cycle', 'lineage_cycle'),
    ('identity', 'identity_unresolved'), ('time', 'time_applicability_unknown')))
def test_full_population_hhi_gate_retains_specific_blockers(defect, reason):
    source = h.small(); changes = {}
    if defect == 'partial':
        coverage = h.cases.by_id(source, 'coverage')
        coverage['data']['details'].update(state='partial', universe_enumerated=False)
    elif defect == 'terminal':
        source['assertions'] = [row for row in source['assertions'] if row['id'] != 'boundary0']
    elif defect == 'basis':
        h.cases.by_id(source, 'direct')['provenance'].update(basis_kind='declaration', evidence_ref_ids=[])
    elif defect == 'cycle':
        source['assertions'].extend((h.relation('copy-out', 'derived_from', 'e', 'e2'),
                                    h.relation('copy-back', 'derived_from', 'e2', 'e')))
        h.cases.by_id(source, 'coverage')['data']['details']['member_refs'].append('e2')
    elif defect == 'identity':
        source = direct_case(('documented_origin', 'documented_origin'))
        alias = h.relation('alias', 'same_identity_as', 'origin', 'origin2', dimension=None)
        alias['data']['details'] = {'identity_level': 'origin_event'}
        source['assertions'].append(alias)
    elif defect == 'time':
        from source_integrity_toolkit.contracts.evidence import _Node
        from source_integrity_toolkit.contracts.bundle import _Object
        stamp = _Node('TimeValue', _Object((('precision', 'instant'), ('state', 'known'), ('value', '2026-01-10T13:00:00Z'))))
        changes.update(temporal_basis='time_specific', requested_time=stamp)
    scalar = run(source, 'SIT-M005', **changes)[0]
    population = ('e', 'e2') if defect == 'identity' else ('e',)
    assert_fraction(hhi(scalar), population, state='unavailable', reasons=(reason,))
    # M005 retains the source population when no scalar qualifies.
    assert scalar.facts.origin_facts.seed_traces
    if defect == 'identity':
        assert tuple(trace.seed.identifier for trace in scalar.facts.origin_facts.seed_traces) == ('e', 'e2')
        assert tuple(origin.identifier for origin in scalar.facts.origin_facts.reached_origins) == ('origin', 'origin2')
        assert h.cases.by_id(source, 'alias')['data']['from_ref'] == 'origin'
        assert h.cases.by_id(source, 'alias')['data']['to_ref'] == 'origin2'


def test_origin_population_is_claim_and_dimension_scoped_without_implicit_narrowing():
    source = direct_case(('documented_origin', 'documented_origin'))
    source['inquiries'][0]['target_claim_refs'].append('claim2')
    h.cases.by_id(source, 'e2')['data']['claim_ref'] = 'claim2'
    for name in ('direct-e2', 'boundary-e2'):
        h.cases.by_id(source, name)['scope']['claim_refs'] = ['claim2']
    h.cases.by_id(source, 'coverage')['scope']['claim_refs'] = ['claim', 'claim2']
    scalar = run(source, 'SIT-M005')[0]
    assert_fraction(hhi(scalar), ('e',), (1, 1))
    other = run(source, 'SIT-M005', claim_refs=('claim2',))[0]
    assert_fraction(hhi(other), ('e2',), (1, 1))
    assert leaf(scalar, FIELDS['SIT-M005'][0]).ref.scope.claim_refs[0].identifier == 'claim'
    assert leaf(other, FIELDS['SIT-M005'][0]).ref.scope.claim_refs[0].identifier == 'claim2'


@pytest.mark.parametrize('family', ('SIT-M004', 'SIT-M005', 'SIT-M006'))
def test_current_jobs_charge_real_work_and_interrupt_without_partial_values(family, monkeypatch):
    monkeypatch.setattr(resources, 'monotonic_ns', lambda: 100)
    source = h.small(); snapshot = h.prepared(source); ctx = h.context(source)
    owner, job = h.job_pair(); ledger = owner.witnesses
    job.charge(1_000_000 - job.used - 100)
    before = job.used
    with pytest.raises(_AnalysisAborted) as stopped:
        contribution._contribution_profile(snapshot, ctx, ledger, job, family=family)
    assert stopped.value.limit_id == 'WU9-L11'
    assert stopped.value.stop.input_state == 'accepted'
    assert job.used > before
    with pytest.raises(_AnalysisAborted) as repeated:
        contribution._contribution_profile(snapshot, ctx, ledger, job, family=family)
    assert repeated.value is stopped.value


def test_completed_contribution_immutable_and_foreign_witness_ledger_rejected():
    source = h.small(); before = copy.deepcopy(source)
    out, snapshot, owner, job = run(source)
    assert source == before
    for obj, attr in ((out, 'results'), (out.facts, 'seed_rows'), (out.results[0].value, 'memberships')):
        with pytest.raises((FrozenInstanceError, AttributeError)): setattr(obj, attr, ())
    other, other_job = h.job_pair()
    for ledger in (other.witnesses, _WitnessLedger(owner.witnesses.port)):
        with pytest.raises(TypeError):
            contribution._contribution_profile(snapshot, h.context(source), ledger, job, family='SIT-M004')
    assert other.witnesses._retained_witnesses == 0


def test_permuted_input_sets_preserve_nonexclusive_profiles_and_exact_hhi_gate():
    source = diamond(two_origins=True)
    baseline = run(source)[0]
    source['records'].reverse(); source['assertions'].reverse()
    for row in source['assertions']:
        if row['assertion_kind'] == 'assessment' and row['data']['assessment_kind'] == 'coverage':
            row['data']['details']['member_refs'].reverse()
            row['data']['details']['relation_types'].reverse()
    permuted = run(source)[0]
    for output in (baseline, permuted):
        assert_incidence(origins(output), ('e',), {'e': ('origin', 'origin2')}, {'origin': 1, 'origin2': 1})
        assert_partition(dispositions(output), ('e',), ORIGIN_LABELS, ((), (), (), ('e',), ()))
        assert_fraction(resolution(output), ('e',), (1, 1))
    assert_fraction(hhi(run(source, 'SIT-M005')[0]), ('e',), state='unavailable', reasons=('multi_origin_unallocated',))


def test_origin_rows_and_hhi_select_dimension_before_reading_late_parent():
    source = h.small()
    source['inquiries'][0]['dependency_dimensions'].append('analytical_method')
    source['assertions'].append(h.relation('late-method', 'originates_from', 'e', 'origin2', dimension='analytical_method'))
    h.add_coverage(source, ('e', 'origin2'), identifier='method-coverage', dimension='analytical_method')
    h.add_boundary(source, 'origin2', identifier='method-boundary', coverage='method-coverage', dimension='analytical_method')
    for dimension, origin in (('acquisition', 'origin'), ('analytical_method', 'origin2')):
        out = run(source, dependency_dimension=dimension)[0]
        assert_incidence(origins(out), ('e',), {'e': (origin,)}, {origin: 1})
        assert_fraction(hhi(run(source, 'SIT-M005', dependency_dimension=dimension)[0]), ('e',), (1, 1))
