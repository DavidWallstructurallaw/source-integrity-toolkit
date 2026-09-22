# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W07 VF018--VF020 source oracles, Definitions 24 and W7-03/13/14/15/17.

Catch upstream uncertainty leaking into the immediate layer, multi-origin
inheritance mislabeled mixed, path/novelty scores replacing seed units, and
unknown rows lost from finite-record completion intervals. All mutants first
pass an independent literal oracle on the actual completed component output.
"""
import copy
import importlib.util
import json
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location('sit_w07_contribution_helpers', Path(__file__).with_name('test_contribution_profile.py'))
c = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(c)
h = c.h
LABELS = ('inherited_only_at_evidence_layer', 'direct_origin_link_only',
          'mixed_direct_and_inherited', 'unresolved_at_evidence_layer')
IMMEDIATE_PREDICATES = ('derived_from', 'copies', 'syndicated_from', 'summarizes', 'translates', 'quotes', 'originates_from')


def run(source, **changes):
    return c.run(source, 'SIT-M006', **changes)[0]


def partition(out):
    return c.partition_view(c.leaf(out, 'immediate_evidence_layer_dispositions'))


def fraction(out):
    return c.fraction_view(c.leaf(out, 'inherited_only_seed_fraction'))


def interval(out):
    row = c.leaf(out, 'inherited_only_completion_interval')
    value = row.value
    return {'execution': row.execution_state, 'state': row.result_state,
            'members': c.members(row.population_refs[0]), 'reasons': c.codes(row),
            'value': None if value is None else {
                'kind': value.interval_kind,
                'lower': (value.lower.numerator, value.lower.denominator),
                'upper': (value.upper.numerator, value.upper.denominator),
                'partition': {category.label: (category.count, tuple(ref.identifier for ref in category.member_refs))
                              for category in value.partition.categories}}}


def assert_interval(actual, population, lower=None, upper=None, buckets=None, *, state='available', reasons=()):
    assert actual['execution'] == 'completed' and actual['state'] == state
    assert actual['members'] == population
    assert set(reasons) <= actual['reasons']
    if state != 'available':
        assert actual['value'] is None
    else:
        assert actual['value'] == {'kind': 'finite_record_completion', 'lower': lower, 'upper': upper,
            'partition': {label: (len(bucket), bucket) for label, bucket in zip(LABELS, buckets)}}


@pytest.fixture(scope='module')
def heroes():
    return {variant: run(h.hero(variant)) for variant in ('H7-01', 'H7-V01', 'H7-V02', 'H7-V03')}


@pytest.mark.parametrize('variant', ('H7-01', 'H7-V01', 'H7-V02', 'H7-V03'))
def test_vf018_to_vf020_frozen_immediate_populations_and_exact_denominators(heroes, variant):
    """VF018 P/M, VF019 P/M, VF020 P/B remain independent of root multiplicity."""
    out = heroes[variant]
    pop, buckets, ratio = c.H7_SEEDS, (c.H7_SEEDS[:5], ('H7-EF',), (), ()), (5, 6)
    if variant == 'H7-V01':
        pop, buckets, ratio = c.H7_SEEDS[:5], (c.H7_SEEDS[:5], (), (), ()), (5, 5)
    elif variant == 'H7-V02':
        pop += ('H7-EU',); buckets = (c.H7_SEEDS[:5], ('H7-EF',), (), ('H7-EU',)); ratio = None
    elif variant == 'H7-V03':
        pop += ('H7-EG',); buckets = (c.H7_SEEDS[:5] + ('H7-EG',), ('H7-EF',), (), ()); ratio = (6, 7)
    c.assert_partition(partition(out), pop, LABELS, buckets)
    c.assert_fraction(fraction(out), pop, ratio, state='unavailable' if ratio is None else 'available')
    if variant == 'H7-V02':
        assert_interval(interval(out), pop, (5, 7), (6, 7), buckets)
    else:
        assert_interval(interval(out), pop, state='not_applicable', reasons=('completion_interval_not_needed',))
    golden = json.loads((c.ROOT / 'tests/golden' / (variant + '.logical.json')).read_bytes())
    assert pop == tuple(golden['populations']['source_contributions'])
    assert tuple(len(bucket) for bucket in buckets) == tuple(golden['immediate_partition_counts'])
    for label, bucket in zip(LABELS, buckets):
        assert bucket == tuple(row['seed_ref'] for row in golden['origin_rows'] if row['immediate_disposition'] == label)
    assert out.facts.origin_facts is None
    for row in out.results:
        checks = {check.check_id: check.state for check in row.check_refs}
        assert checks['PC13'] == ('unmet' if variant == 'H7-V02' else 'met')
    # Immediate witnesses must be retained against this completed operation.
    for row in out.results:
        assert row.witness_refs
        catalog = {witness.starts[0].identifier: witness for witness in out.witnesses}
        assert tuple(catalog) == pop
        assert {ref.anchor[1].identifier for ref in row.witness_refs} == set(pop)
        for ref in row.witness_refs:
            assert ref.kind == 'member_set' and ref.anchor[0] == 'immediate_complete_trace'
            witness = catalog[ref.anchor[1].identifier]
            assert witness.kind == 'complete_trace' and witness.graph is out.facts.graph
    expected_edges = {
        'H7-EA': (('H7-L02', 'H7-ER1'),), 'H7-EB': (('H7-L03', 'H7-ER1'),),
        'H7-EC': (('H7-L04', 'H7-ER1'),), 'H7-ED': (('H7-L05', 'H7-EB'),),
        'H7-EE': (('H7-L06', 'H7-EA'),), 'H7-EF': (('H7-L07', 'H7-O2'),),
        'H7-EU': (('H7-LU', 'H7-UX'),), 'H7-EG': (('H7-LG1', 'H7-EA'), ('H7-LG2', 'H7-EF'))}
    for witness in out.witnesses:
        seed = witness.starts[0].identifier
        assert all(edge.source.identifier == seed for edge in witness.observations)
        assert tuple((edge.source_ref.record_id, edge.target.identifier) for edge in witness.observations) == expected_edges[seed]


def test_vf018_n_multi_origin_inherited_parents_cannot_become_mixed(heroes):
    baseline = partition(heroes['H7-V03'])
    pop = c.H7_SEEDS + ('H7-EG',); buckets = (c.H7_SEEDS[:5] + ('H7-EG',), ('H7-EF',), (), ())
    c.assert_partition(baseline, pop, LABELS, buckets)
    mutant = copy.deepcopy(baseline)
    mutant['categories'][LABELS[0]] = (5, c.H7_SEEDS[:5])
    mutant['categories'][LABELS[2]] = (1, ('H7-EG',))
    with pytest.raises(AssertionError): c.assert_partition(mutant, pop, LABELS, buckets)


def test_vf019_n_paths_or_text_novelty_cannot_replace_seed_numerator():
    out = run(c.diamond())
    baseline = fraction(out)
    c.assert_fraction(baseline, ('e',), (1, 1))
    for wrong in ((2, 1), (0, 1)):
        mutant = copy.deepcopy(baseline); mutant['value'] = wrong
        with pytest.raises(AssertionError): c.assert_fraction(mutant, ('e',), (1, 1))
    c.assert_partition(partition(out), ('e',), LABELS, (('e',), (), (), ()))


def test_vf019_m_unknown_row_cannot_be_dropped_or_replaced_by_interval_endpoint(heroes):
    baseline = fraction(heroes['H7-V02']); pop = c.H7_SEEDS + ('H7-EU',)
    c.assert_fraction(baseline, pop, state='unavailable')
    for wrong in ((5, 6), (5, 7), (6, 7)):
        mutant = copy.deepcopy(baseline); mutant.update(state='available', value=wrong)
        with pytest.raises(AssertionError): c.assert_fraction(mutant, pop, state='unavailable')


def test_vf020_n_interval_cannot_be_confidence_resolved_only_or_a_point(heroes):
    baseline = interval(heroes['H7-V02']); pop = c.H7_SEEDS + ('H7-EU',)
    buckets = (c.H7_SEEDS[:5], ('H7-EF',), (), ('H7-EU',))
    assert_interval(baseline, pop, (5, 7), (6, 7), buckets)
    for mutation in ('confidence', 'denominator', 'point'):
        mutant = copy.deepcopy(baseline)
        if mutation == 'confidence': mutant['value']['kind'] = 'confidence_interval'
        elif mutation == 'denominator': mutant['value'].update(lower=(5, 6), upper=(6, 6))
        else: mutant['value']['upper'] = (5, 7)
        with pytest.raises(AssertionError): assert_interval(mutant, pop, (5, 7), (6, 7), buckets)


def test_vf020_m_all_unknown_has_full_finite_completion_interval():
    out = run(c.shared_unknown())
    c.assert_partition(partition(out), ('e', 'e2'), LABELS, ((), (), (), ('e', 'e2')))
    c.assert_fraction(fraction(out), ('e', 'e2'), state='unavailable')
    assert_interval(interval(out), ('e', 'e2'), (0, 2), (2, 2), ((), (), (), ('e', 'e2')))


def distant_unknown():
    source = h.small(edges=(('known-copy', 'copies', 'e', 'e2'),
        ('distant-unknown', 'derived_from', 'e2', 'unresolved')), roles=(), coverage_state='partial')
    h.cases.by_id(source, 'unresolved')['data']['expected_kinds'] = ['evidence_item']
    h.add_coverage(source, ('e', 'e2'), subjects=('inquiry',), predicates=IMMEDIATE_PREDICATES, identifier='immediate-coverage')
    return source


def test_vf018_m_and_vf019_b_known_copy_survives_unknown_distant_ancestry():
    source = distant_unknown()
    out, root = run(source), c.run(source)[0]
    c.assert_partition(partition(out), ('e',), LABELS, (('e',), (), (), ()))
    c.assert_fraction(fraction(out), ('e',), (1, 1))
    assert_interval(interval(out), ('e',), state='not_applicable', reasons=('completion_interval_not_needed',))
    c.assert_partition(c.dispositions(root), ('e',), c.ORIGIN_LABELS, (('e',), (), (), (), ()))
    c.assert_fraction(c.resolution(root), ('e',), (0, 1))
    # The local witness reaches the resolved first parent and never UX.
    assert out.witnesses
    for witness in out.witnesses:
        assert tuple(node.identifier for node in witness.examined_nodes) == ('e', 'e2')
        assert tuple(edge.source_ref.record_id for edge in witness.examined_edges) == ('known-copy',)
        assert witness.frontiers == ()
    for row in out.results:
        checks = {check.check_id: check for check in row.check_refs}
        assert all(checks[name].state == 'met' for name in ('PC05', 'PC06', 'PC08', 'PC09', 'PC10', 'PC13'))
        assert 'distant-unknown' not in {ref.identifier for check in row.check_refs for ref in check.input_refs}
        assert 'unknown_endpoint' not in c.codes(row)


@pytest.mark.parametrize('structure', ('mixed', 'two_roots', 'diamond', 'unqualified_direct'))
def test_vf018_b_immediate_structure_is_independent_of_qualified_root_structure(structure):
    if structure == 'mixed':
        source = h.small(edges=(('direct', 'originates_from', 'e', 'origin'),
            ('copy', 'copies', 'e', 'e2'), ('parent', 'originates_from', 'e2', 'origin')))
        buckets, ratio = ((), (), ('e',), ()), (0, 1)
    elif structure in ('two_roots', 'diamond'):
        source = c.diamond(two_origins=structure == 'two_roots')
        buckets, ratio = (('e',), (), (), ()), (1, 1)
    else:
        source = h.small(roles=(('origin', 'scope_cut'),))
        buckets, ratio = ((), ('e',), (), ()), (0, 1)
    out = run(source)
    c.assert_partition(partition(out), ('e',), LABELS, buckets)
    c.assert_fraction(fraction(out), ('e',), ratio)


def test_vf019_b_and_vf020_m_empty_population_has_no_fraction_or_endpoints():
    out = run(h.small(seeds=(), edges=(), roles=()))
    c.assert_partition(partition(out), (), LABELS, ((), (), (), ()))
    c.assert_fraction(fraction(out), (), state='unavailable', reasons=('no_seed_contributions',))
    assert_interval(interval(out), (), state='unavailable', reasons=('no_seed_contributions',))


@pytest.mark.parametrize('predicate', ('derived_from', 'copies', 'syndicated_from', 'summarizes', 'translates', 'quotes'))
def test_each_permitted_transformation_is_one_inherited_seed(predicate):
    source = h.small(edges=(('transform', predicate, 'e', 'e2'), ('root', 'originates_from', 'e2', 'origin')))
    out = run(source)
    c.assert_partition(partition(out), ('e',), LABELS, (('e',), (), (), ()))
    c.assert_fraction(fraction(out), ('e',), (1, 1))


@pytest.mark.parametrize('defect', ('late_unlisted_parent', 'unsupported', 'disputed', 'partial', 'time', 'identity'))
def test_immediate_enumeration_and_local_premises_cannot_be_silently_assumed(defect):
    source = distant_unknown(); changes = {}
    if defect == 'late_unlisted_parent':
        source['assertions'].append(h.relation('zz-late-parent', 'originates_from', 'e', 'origin'))
    elif defect == 'unsupported':
        h.cases.by_id(source, 'known-copy')['provenance'].update(basis_kind='declaration', evidence_ref_ids=[])
    elif defect == 'disputed':
        denial = h.relation('late-denial', 'copies', 'e', 'e2'); denial['data']['polarity'] = 'denied'
        source['assertions'].append(denial)
    elif defect == 'partial':
        h.cases.by_id(source, 'immediate-coverage')['data']['details'].update(state='partial', universe_enumerated=False)
    elif defect == 'time':
        from source_integrity_toolkit.contracts.evidence import _Node
        from source_integrity_toolkit.contracts.bundle import _Object
        stamp = _Node('TimeValue', _Object((('precision', 'instant'), ('state', 'known'), ('value', '2026-01-10T13:00:00Z'))))
        changes.update(temporal_basis='time_specific', requested_time=stamp)
    else:
        source = h.small()
        alias = h.relation('alias', 'same_identity_as', 'origin', 'origin2', dimension=None)
        alias['data']['details'] = {'identity_level': 'origin_event'}
        source['assertions'].append(alias)
    out = run(source, **changes)
    c.assert_partition(partition(out), ('e',), LABELS, ((), (), (), ('e',)))
    c.assert_fraction(fraction(out), ('e',), state='unavailable')
    assert_interval(interval(out), ('e',), (0, 1), (1, 1), ((), (), (), ('e',)))
    for row in out.results:
        assert next(check for check in row.check_refs if check.check_id == 'PC13').state == 'unmet'


def test_immediate_only_selected_dimension_and_claim_can_change_classification():
    source = h.small()
    # An explicitly other-dimension copy cannot change acquisition directness.
    source['inquiries'][0]['dependency_dimensions'].append('analytical_method')
    source['assertions'].append(h.relation('method-copy', 'copies', 'e', 'e2', dimension='analytical_method'))
    h.add_coverage(source, ('e', 'e2'), subjects=('inquiry',), predicates=IMMEDIATE_PREDICATES,
                   identifier='method-coverage', dimension='analytical_method')
    acquisition = run(source)
    c.assert_partition(partition(acquisition), ('e',), LABELS, ((), ('e',), (), ()))
    method = run(source, dependency_dimension='analytical_method')
    c.assert_partition(partition(method), ('e',), LABELS, (('e',), (), (), ()))
    # Denial under a different Claim cannot poison the current immediate edge.
    source['inquiries'][0]['target_claim_refs'].append('claim2')
    denial = h.relation('other-claim-denial', 'depends_on', 'origin', 'origin2')
    denial['data']['polarity'] = 'denied'; denial['scope']['claim_refs'] = ['claim2']
    source['assertions'].append(denial)
    c.assert_fraction(fraction(run(source)), ('e',), (0, 1))
