# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W14 source-authored challenges to frequency, identity and qualification.

The 228 source-bound owner tests remain live in cumulative CI. These additional
cases challenge their interaction using literal expectations authored before
execution. Shared test constructors and assistant lineage do not constitute an
independent external review. A locally coherent fictional dossier supplies no
empirical validation of its source, even when the documentary gates are met.
"""
import copy
import importlib.util
import json
from pathlib import Path

import pytest

from source_integrity_toolkit.runtime import boundary


ROOT = Path(__file__).resolve().parents[2]


def _load_test(name, path):
    spec = importlib.util.spec_from_file_location(name, ROOT / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


p = _load_test('sit_w14_pipeline_cases', 'tests/integration/test_analytical_pipeline.py')
c = _load_test('sit_w14_contribution_cases', 'tests/unit/test_contribution_profile.py')
i = _load_test('sit_w14_inventory_cases', 'tests/unit/test_inventory.py')
o = c.h
CASES = json.loads((ROOT / 'tests/fixtures/micro/phase3_cases.json').read_bytes())
EXPECTED = json.loads((ROOT / 'tests/golden/phase3_core_expectations.json').read_bytes())['cases']


def _record(source, identifier):
    return next(row for collection in ('records', 'assertions', 'evidence_references')
                for row in source[collection] if row['id'] == identifier)


def _clone(source, identifier, new_id, collection):
    row = copy.deepcopy(_record(source, identifier))
    row['id'] = new_id
    source[collection].append(row)
    return row


def _finite_case(identifier):
    source = p._documented_value()
    _clone(source, 'origin', 'origin2', 'records')
    _clone(source, 'boundary', 'boundary2', 'assertions')['data']['subject_refs'] = ['origin2']
    _clone(source, 'e', 'e3', 'records')['data']['locator'] = 'Third supplied contribution'
    _clone(source, 'parent-e', 'parent-e3', 'assertions')['data'].update(from_ref='e3', to_ref='origin2')
    source['inquiries'][0]['seed_evidence_refs'].append('e3')
    members = _record(source, 'coverage')['data']['details']['member_refs']
    members.extend(['origin2', 'e3'])
    delta = next(case for case in CASES['cases'] if case['id'] == identifier)
    for original, new_id in delta['added_contributions']:
        _clone(source, original, new_id, 'records')
        _clone(source, 'parent-' + original, 'parent-' + new_id, 'assertions')['data']['from_ref'] = new_id
        source['inquiries'][0]['seed_evidence_refs'].append(new_id)
        members.append(new_id)
    if 'support_availability' in delta:
        _record(source, 'support').update(availability='locator_only', reference_kind='external_locator',
                                        excerpt=None, locator='https://invalid.example/fictional-support')
    if 'additional_parent' in delta:
        start, target = delta['additional_parent']
        edge = _clone(source, 'parent-e', 'additional-parent', 'assertions')
        edge['data'].update(from_ref=start, to_ref=target, details={'portion_note': 'roughly half from each'})
    return source


@pytest.fixture(scope='module')
def challenges():
    outcomes = {}
    for identifier in EXPECTED:
        source = _finite_case(identifier)
        original = copy.deepcopy(source)
        outcomes[identifier] = (
            source, i.run(source)[0], o.run(source)[0],
            c.run(source, 'SIT-M004')[0], c.run(source, 'SIT-M005')[0])
        assert source == original
    return outcomes


@pytest.mark.parametrize('identifier', tuple(EXPECTED))
def test_source_granularity_keeps_exact_populations_and_qualification_gates(challenges, identifier):
    source, inventory, origins, profile, scalar = challenges[identifier]
    expected = EXPECTED[identifier]
    seeds = tuple(expected['seeds'])
    i.assert_cell(i.leaf(inventory, 'nominal_seed_artifact_record_count'),
                  'nominal_seed_artifact_record_count', tuple(expected['artifacts']))
    i.assert_cell(i.leaf(inventory, 'seed_evidence_item_count'), 'seed_evidence_item_count', seeds)
    for field, member_key in (('reached_origin_record_count', 'reached_origins'),
                              ('documentary_origin_boundary_record_count', 'documentary_origins')):
        row = o.leaf(origins, field)
        assert (row.execution_state, row.result_state) == ('completed', 'available')
        assert row.value.value == len(expected[member_key])
        assert tuple(ref.identifier for ref in row.value.population.member_refs) == tuple(expected[member_key])
    c.assert_incidence(c.origins(profile), seeds,
        {seed: tuple(roots) for seed, roots in expected['memberships'].items()}, expected['incidence_counts'])
    c.assert_partition(c.dispositions(profile), seeds, c.ORIGIN_LABELS,
                       tuple(tuple(group) for group in expected['dispositions']))
    c.assert_fraction(c.resolution(profile), seeds, tuple(expected['resolution']))
    c.assert_fraction(c.hhi(scalar), seeds, None if expected['hhi'] is None else tuple(expected['hhi']),
                      state=expected['hhi_state'], reasons=expected['reasons'])
    for output in (profile, scalar):
        for row in output.results:
            assert row.ref.scope.inquiry_ref.identifier == 'inquiry'
            assert tuple(ref.identifier for ref in row.ref.scope.claim_refs) == ('claim',)
            assert row.ref.scope.dependency_dimension == 'acquisition'
            assert row.ref.scope.temporal_basis == 'snapshot_structural'
            assert row.population_refs[0].scope is row.ref.scope
            assert row.value is not None or row.reason_refs
            assert row.basis_refs and row.witness_refs
            assert {'parent-e', 'parent-e2', 'parent-e3'} <= {ref.source.identifier for ref in row.basis_refs}
            assert 'represented contribution frequency' in row.interpretation_limit
            assert 'not reliability, truth or process independence' in row.interpretation_limit
    # Equal native event keys neither merge two supplied IDs nor prove two
    # real acquisitions. Exactly this challenge is fixed before execution.
    assert _record(source, 'origin')['data'] == _record(source, 'origin2')['data']


def test_nonuniform_resegmentation_changes_frequency_while_uniform_replication_preserves_ratio(challenges):
    baseline, split, uniform = (c.hhi(challenges[name][4])['value'] for name in
        ('three_contributions', 'split_first_contribution', 'uniform_record_replication'))
    assert baseline == (5, 9) and split == (10, 16) and uniform == (20, 36)
    assert baseline[0] * split[1] != split[0] * baseline[1]
    assert baseline[0] * uniform[1] == uniform[0] * baseline[1]
    # The original finite squares stay unreduced and no effective independent
    # sample count or semantic deduplication is introduced by either case.
    assert [len(EXPECTED[name]['artifacts']) for name in
            ('three_contributions', 'split_first_contribution', 'uniform_record_replication')] == [1, 1, 1]


@pytest.mark.parametrize('mode', ('value', 'utf8'))
def test_coherent_fictional_support_can_pass_documentary_gates_without_authenticating_source(mode):
    source = p._documented_value()
    _record(source, 'support')['excerpt'] = (
        'Entirely invented fictional acquisition log. The supplied IDs, full parent scope and terminal '
        'boundary are internally coherent; this text has never been externally authenticated.')
    original = copy.deepcopy(source)
    out = boundary._analyze_value(source) if mode == 'value' else boundary._analyze_utf8(
        json.dumps(source).encode('utf-8'))
    assert out.input_state == 'accepted' and out.execution_state == 'completed'
    assert source == original
    scalar = next(row for row in out.results if row.ref.field_key == 'single_origin_contribution_hhi')
    assert (scalar.execution_state, scalar.result_state, scalar.value.numerator,
            scalar.value.denominator) == ('completed', 'available', 4, 4)
    assert tuple(ref.identifier for ref in scalar.population_refs[0].member_refs) == ('e', 'e2')
    assert {check.check_id: check.state for check in scalar.check_refs}['PC12'] == 'met'
    assert 'not reliability, truth or process independence' in scalar.interpretation_limit
    assert scalar.basis_refs and scalar.witness_refs
    assert not any(hasattr(out, name) for name in ('truth_score', 'integrity_score', 'effective_sample_size'))
