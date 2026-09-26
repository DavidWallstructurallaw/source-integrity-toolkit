# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W14 independently specified metamorphic deltas through the private pipeline.

Reporting 19.2 / Validation VG018 distinguish semantic sets, native ordered
source arrays, and causal paths. Definitions 20.4/22.1-22.2 fix record membership
and the effects of a relevant disputed parent. These tests share W13's fixture
constructor, not a runtime-generated expected-value snapshot or public export.
"""
import copy
from dataclasses import fields, is_dataclass
import importlib.util
from pathlib import Path

import pytest

_spec = importlib.util.spec_from_file_location(
    'sit_w14_determinism_fixture', Path(__file__).with_name('test_analytical_pipeline.py'))
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

MODES = ('value', 'utf8')
CORE_FIELDS = (
    'seed_evidence_item_count', 'reached_origin_record_count',
    'documentary_origin_boundary_record_count', 'seed_items_with_unresolved_ancestry_count',
    'per_seed_origin_memberships', 'origin_incidence_counts', 'seed_origin_dispositions',
    'documentary_origin_resolution_fraction', 'single_origin_contribution_hhi',
)


def _by_id(source, identifier):
    return next(row for collection in ('records', 'assertions', 'evidence_references')
                for row in source[collection] if row['id'] == identifier)


def _analyze(source, mode):
    before = copy.deepcopy(source)
    result = h._analyze(source, mode)
    assert source == before
    assert result.execution_state == 'completed'
    return result


def _leaf(outcome, field):
    rows = h._rows(outcome, field)
    assert len(rows) == 1
    assert rows[0].execution_state == 'completed'
    return rows[0]


def _normal(value, names=None):
    """Normalize immutable test observations; no production expectation source."""
    if is_dataclass(value):
        return (type(value).__name__, tuple((field.name, _normal(getattr(value, field.name), names))
                    for field in fields(value)))
    if type(value) in (tuple, list):
        return tuple(_normal(item, names) for item in value)
    if type(value) is str and names is not None:
        return names.get(value, value)
    return value


def _core_values(outcome, names=None):
    return tuple((name, row.result_state, _normal(row.value, names),
                  tuple(reason.code for reason in row.reason_refs))
                 for name in CORE_FIELDS for row in (_leaf(outcome, name),))


def _count(outcome, field, members):
    row = _leaf(outcome, field)
    assert row.result_state == 'available'
    assert row.value.value == len(members)
    assert tuple(ref.identifier for ref in row.value.population.member_refs) == members


def _qualified_pair(outcome, *, prefix=''):
    """Literal finite oracle: two supplied contributions to one terminal origin."""
    seeds = tuple(prefix + identifier for identifier in ('e', 'e2'))
    origin = prefix + 'origin'
    _count(outcome, 'seed_evidence_item_count', seeds)
    _count(outcome, 'reached_origin_record_count', (origin,))
    _count(outcome, 'documentary_origin_boundary_record_count', (origin,))
    _count(outcome, 'seed_items_with_unresolved_ancestry_count', ())
    memberships = _leaf(outcome, 'per_seed_origin_memberships')
    assert memberships.result_state == 'available'
    assert {row.member_ref.identifier: tuple(ref.identifier for ref in row.origin_refs)
            for row in memberships.value.memberships} == {seed: (origin,) for seed in seeds}
    incidence = _leaf(outcome, 'origin_incidence_counts')
    assert incidence.result_state == 'available' and incidence.value.nonexclusive is True
    assert tuple((ref.identifier, count) for ref, count in incidence.value.origin_counts) == ((origin, 2),)
    partition = _leaf(outcome, 'seed_origin_dispositions')
    assert partition.result_state == 'available'
    assert {row.label: (row.count, tuple(ref.identifier for ref in row.member_refs))
            for row in partition.value.categories} == {
        'unresolved_or_conflicted': (0, ()), 'contains_baseline_or_scope_cut': (0, ()),
        'contains_declared_origin': (0, ()), 'multiple_documented_origins': (0, ()),
        'single_documented_origin': (2, seeds)}
    resolution = _leaf(outcome, 'documentary_origin_resolution_fraction')
    assert resolution.result_state == 'available'
    assert (resolution.value.numerator, resolution.value.denominator) == (2, 2)
    hhi = _leaf(outcome, 'single_origin_contribution_hhi')
    assert hhi.result_state == 'available'
    assert (hhi.value.numerator, hhi.value.denominator) == (4, 4)
    assert tuple(ref.identifier for ref in hhi.value.population.member_refs) == seeds
    assert {prefix + identifier for identifier in ('coverage', 'boundary', 'parent-e2')} <= {
        ref.source.identifier for ref in hhi.basis_refs}
    assert not {'premise_disputed', 'lineage_cycle'} & {reason.code for reason in hhi.reason_refs}


@pytest.mark.parametrize('mode', MODES)
def test_nested_coverage_sets_permute_without_reordering_native_qualifications(mode):
    source = h._documented_value()
    native_order = ['Second supplied qualification.', 'First supplied qualification.']
    _by_id(source, 'boundary')['provenance']['qualifications'] = native_order[:]
    changed = copy.deepcopy(source)
    details = _by_id(changed, 'coverage')['data']['details']
    details['member_refs'].reverse()
    details['relation_types'] = details['relation_types'][3:] + details['relation_types'][:3]
    changed['inquiries'][0]['seed_evidence_refs'].reverse()
    changed['records'].reverse()
    changed['assertions'].reverse()
    before, after = _analyze(source, mode), _analyze(changed, mode)
    _qualified_pair(before)
    _qualified_pair(after)
    assert _core_values(before) == _core_values(after)
    for outcome in (before, after):
        disclosure = h._disclosures(outcome, 'origin_boundary_disclosures')['boundary']
        assert disclosure['provenance']['qualifications'] == native_order
    assert _by_id(changed, 'coverage')['data']['details']['member_refs'] == ['origin', 'e2', 'e']


@pytest.mark.parametrize('mode', MODES)
def test_id_preserving_native_text_and_array_changes_are_retained_without_count_drift(mode):
    source = h._documented_value()
    changed = copy.deepcopy(source)
    boundary = _by_id(changed, 'boundary')
    boundary['data']['details']['termination_reason'] = 'A new attributed explanation; the same finite boundary.'
    boundary['provenance']['qualifications'] = ['B supplied first.', 'A supplied second.']
    _by_id(changed, 'claim')['data']['text'] = 'Edited source wording, with identical structural references.'
    before, after = _analyze(source, mode), _analyze(changed, mode)
    assert {row['id'] for row in changed['records']} == {row['id'] for row in source['records']}
    assert _core_values(before) == _core_values(after)
    _qualified_pair(after)
    native = h._disclosures(after, 'origin_boundary_disclosures')['boundary']
    assert native['data'] == boundary['data']
    assert native['provenance'] == boundary['provenance']
    assert native['provenance']['qualifications'] != sorted(native['provenance']['qualifications'])


@pytest.mark.parametrize('mode', MODES)
def test_bijective_local_id_renaming_preserves_exact_memberships_after_inverse_mapping(mode):
    source = h._documented_value()
    identifiers = {row['id'] for collection in ('inquiries', 'records', 'assertions', 'evidence_references')
                   for row in source[collection]}
    mapping = {identifier: 'Case:A.' + identifier for identifier in identifiers}

    def rename(value, field=''):
        if type(value) is dict:
            return {key: rename(item, key) for key, item in value.items()}
        if type(value) is list:
            return [rename(item, field) for item in value]
        is_reference = field == 'id' or field.endswith(('_ref', '_refs', '_ref_ids'))
        return mapping.get(value, value) if is_reference and type(value) is str else value

    before, after = _analyze(source, mode), _analyze(rename(source), mode)
    _qualified_pair(before)
    _qualified_pair(after, prefix='Case:A.')
    assert _core_values(before) == _core_values(after, {value: key for key, value in mapping.items()})
    assert all(row.ref.scope.inquiry_ref.identifier == 'Case:A.inquiry' for row in after.results)
    assert _normal(before.plan) == _normal(after.plan, {value: key for key, value in mapping.items()})


@pytest.mark.parametrize('delta', ('parallel_assertion', 'additional_route'))
@pytest.mark.parametrize('mode', MODES)
def test_duplicate_provenance_paths_do_not_multiply_origin_or_contribution_members(delta, mode):
    source = h._documented_value()
    changed = copy.deepcopy(source)
    extra = copy.deepcopy(_by_id(source, 'parent-e'))
    extra['id'] = 'extra-path'
    if delta == 'additional_route':
        extra['data'].update(predicate='derived_from', to_ref='e2')
    changed['assertions'].append(extra)
    before, after = _analyze(source, mode), _analyze(changed, mode)
    _qualified_pair(before)
    _qualified_pair(after)
    assert _core_values(before) == _core_values(after)
    incidence = _leaf(after, 'origin_incidence_counts')
    assert 'extra-path' in {ref.source.identifier for ref in incidence.basis_refs}
    assert len(changed['assertions']) == len(source['assertions']) + 1


@pytest.mark.parametrize('mode', MODES)
def test_causal_witness_edge_order_survives_source_reordering_and_is_not_lexical(mode):
    source = h._documented_value()
    source['assertions'].remove(_by_id(source, 'parent-e'))
    hop = copy.deepcopy(_by_id(source, 'parent-e2'))
    hop['id'] = 'z-first-hop'
    hop['data'].update(predicate='derived_from', from_ref='e', to_ref='e2')
    source['assertions'].append(hop)
    changed = copy.deepcopy(source)
    changed['assertions'].reverse()
    changed['records'].reverse()
    paths = []
    for value in (source, changed):
        out = _analyze(value, mode)
        _qualified_pair(out)
        actual = set()
        for witness in out.witnesses:
            for part in witness.payload:
                if part[0:2] != ('graph_witness', 'path') or part[5] != 'claim_origin':
                    continue
                material = dict(part[7])
                nodes = tuple(node[1].identifier for node in material['nodes'])
                edges = tuple(edge[4].identifier for edge in material['edges'])
                actual.add((nodes, edges))
        assert (('e', 'e2', 'origin'), ('z-first-hop', 'parent-e2')) in actual
        assert (('e', 'e2', 'origin'), ('parent-e2', 'z-first-hop')) not in actual
        paths.append(actual)
    assert paths[0] == paths[1]


@pytest.mark.parametrize('mode', MODES)
def test_disconnected_contrary_data_does_not_poison_the_completed_seed_population(mode):
    source = h._documented_value()
    changed = copy.deepcopy(source)
    isolated = copy.deepcopy(_by_id(source, 'origin'))
    isolated['id'] = 'unreached-origin'
    isolated['data']['event_key'] = 'unreached-origin'
    changed['records'].append(isolated)
    denial = copy.deepcopy(_by_id(source, 'parent-e'))
    denial['id'] = 'unrelated-denial'
    denial['data'].update(predicate='depends_on', from_ref='unreached-origin',
                          to_ref='unreached-origin', polarity='denied')
    denial['provenance'] = h._provenance()
    changed['assertions'].append(denial)
    before, after = _analyze(source, mode), _analyze(changed, mode)
    _qualified_pair(before)
    _qualified_pair(after)
    assert _core_values(before) == _core_values(after)
    assert 'unreached-origin' not in {
        ref.identifier for ref in _leaf(after, 'reached_origin_record_count').value.population.member_refs}
    assert 'premise_disputed' not in {
        reason.code for field in CORE_FIELDS for reason in _leaf(after, field).reason_refs}


@pytest.mark.parametrize('mode', MODES)
def test_relevant_weak_denial_changes_only_its_seed_and_blocks_full_population_hhi(mode):
    source = h._documented_value()
    changed = copy.deepcopy(source)
    denial = copy.deepcopy(_by_id(source, 'parent-e'))
    denial['id'] = 'relevant-denial'
    denial['data']['polarity'] = 'denied'
    denial['provenance'] = h._provenance()
    changed['assertions'].append(denial)
    before, after = _analyze(source, mode), _analyze(changed, mode)
    _qualified_pair(before)
    _count(after, 'seed_evidence_item_count', ('e', 'e2'))
    _count(after, 'reached_origin_record_count', ('origin',))
    _count(after, 'seed_items_with_unresolved_ancestry_count', ('e',))
    row = _leaf(after, 'seed_origin_dispositions')
    categories = {category.label: tuple(ref.identifier for ref in category.member_refs)
                  for category in row.value.categories}
    assert categories == {'unresolved_or_conflicted': ('e',), 'contains_baseline_or_scope_cut': (),
        'contains_declared_origin': (), 'multiple_documented_origins': (),
        'single_documented_origin': ('e2',)}
    assert 'premise_disputed' in {reason.code for reason in row.reason_refs}
    assert {'parent-e', 'parent-e2', 'coverage', 'boundary'} <= {
        ref.source.identifier for ref in row.basis_refs}
    # Reporting 13.1-13.2 localizes contrary premises through the actual PC09
    # and Reason input_refs. It does not require copying those links into each
    # positive ancestry basis entry (Reporting 12.5/16.6).
    reason = next(reason for reason in row.reason_refs if reason.code == 'premise_disputed')
    assert {(ref.collection, ref.identifier) for ref in reason.input_refs} == {
        ('records', 'e'), ('assertions', 'parent-e'), ('assertions', 'relevant-denial')}
    check = next(check for check in row.check_refs if check.check_id == 'PC09')
    assert check.state == 'unmet'
    assert {'parent-e', 'relevant-denial'} <= {ref.identifier for ref in check.input_refs}
    resolution = _leaf(after, 'documentary_origin_resolution_fraction')
    assert resolution.result_state == 'available'
    assert (resolution.value.numerator, resolution.value.denominator) == (1, 2)
    hhi = _leaf(after, 'single_origin_contribution_hhi')
    assert hhi.result_state == 'unavailable' and hhi.value is None
    assert tuple(ref.identifier for ref in hhi.population_refs[0].member_refs) == ('e', 'e2')
    assert 'premise_disputed' in {reason.code for reason in hhi.reason_refs}
    assert _core_values(before) != _core_values(after)
