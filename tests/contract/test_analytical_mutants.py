# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W14 source-derived rejection of the remaining analytical output mutants.

VALIDATION_PLAN 12 fixes each mutation and its contrary oracle. These tests
first accept actual paid owner results, then reject the prescribed corruption
with the same assertion. Mutable projections are test-only views of private
results; they do not assert that a public report/serializer exists. Existing
owner tests retain the other named output mutations and eight input deltas.
"""
import copy
import importlib.util
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]


def _owner(name):
    spec = importlib.util.spec_from_file_location(
        'sit_w14_mutants_' + name, ROOT / 'tests' / 'unit' / ('test_' + name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


routes = _owner('correction_routes')
outcomes = _owner('correction_outcomes')
provenance = _owner('provenance_profile')
human = _owner('human_review')
comparison = _owner('process_comparison')
inventory = _owner('inventory')


def _reject(actual, mutant, oracle):
    # Reusing the positive oracle on each mutant prevents reject-everything
    # validators. Rechecking actual also detects accidental mutation of it.
    oracle(actual)
    with pytest.raises(AssertionError):
        oracle(mutant)
    oracle(actual)


def _count(out, field):
    row = outcomes.leaf(out, field)
    return {'execution_state': row.execution_state, 'result_state': row.result_state,
            'value': row.value.value, 'members': tuple(
                (ref.case_ref.identifier, ref.before_ref.identifier)
                if row.value.population.unit == 'case_target' else ref.identifier
                for ref in row.value.population.member_refs)}


def _count_oracle(value, members):
    def assert_exact(actual):
        assert actual == {'execution_state': 'completed', 'result_state': 'available',
                          'value': value, 'members': members}
    return assert_exact


@pytest.fixture(scope='module')
def h7_outcomes():
    source = outcomes.h.hero()
    return source, outcomes.run(source)[0]


@pytest.fixture(scope='module')
def failed_handling():
    source = outcomes.small()
    failed = outcomes.duplicate(source, 'handling', 'handling-failed')
    failed['data']['details'].update(outcome='failed', reason='A later supplied native failure.')
    failed['data']['occurred_at'] = {
        'state': 'known', 'value': '2026-01-10T15:00:00Z', 'precision': 'instant'}
    return source, outcomes.run(source)[0]


def test_vf005_n_nonseed_support_artifacts_are_not_unassigned_seeds():
    """VALIDATION_PLAN12.1 VF005-N excludes every H7 support Artifact."""
    source = inventory.hero()
    out = inventory.run(source)[0]
    row = inventory.leaf(out, inventory.FIELDS[4])
    inventory.assert_cell(row, inventory.FIELDS[4], ())
    support_artifacts = ('H7-DOC-ACQ', 'H7-DOC-CHAIN', 'H7-DOC-COMPARE',
                         'H7-DOC-CONTEXT', 'H7-DOC-CORR', 'H7-DOC-GRANT',
                         'H7-DOC-MODEL', 'H7-DOC-PIPE')
    assert {ref['artifact_ref'] for ref in source['evidence_references']} == set(support_artifacts)
    mutant = inventory.replace_members(row, support_artifacts)
    with pytest.raises(AssertionError):
        inventory.assert_cell(mutant, inventory.FIELDS[4], ())
    inventory.assert_cell(row, inventory.FIELDS[4], ())


@pytest.mark.parametrize('inflation', ('sum_pairs', 'merge_members'))
def test_vf009_n_two_named_pairs_cannot_become_one_larger_comparison(inflation):
    """VALIDATION_PLAN12.3 VF009-N, W7-12: pairwise counts never aggregate."""
    source = comparison.setwise()
    first = comparison.cases.by_id(source, 'H7-IND12')
    first['data']['subject_refs'] = ['H7-O1', 'H7-O2']
    first['data']['details']['comparison_form'] = 'pairwise'
    other = copy.deepcopy(first)
    other['id'] = 'W14-IND23'
    other['data']['subject_refs'] = ['H7-O2', 'H7-O3']
    source['assertions'].append(other)
    expected = {'H7-IND12': (2, ('H7-O1', 'H7-O2')),
                'W14-IND23': (2, ('H7-O2', 'H7-O3'))}
    actual = {}
    for identifier in expected:
        out = comparison.run(source, identifier)[0]
        row = comparison.leaf(out, comparison.FIELDS[0])
        actual[identifier] = (row.value.value,
                             tuple(ref.identifier for ref in row.value.population.member_refs))
    mutant = copy.deepcopy(actual)
    mutant['H7-IND12'] = ((4, ('H7-O1', 'H7-O2', 'H7-O2', 'H7-O3'))
                         if inflation == 'sum_pairs' else (3, ('H7-O1', 'H7-O2', 'H7-O3')))
    def oracle(value):
        assert value == expected
    _reject(actual, mutant, oracle)


def test_vf038_n_four_target_tuples_cannot_become_four_independent_channels():
    """VALIDATION_PLAN12.11 VF038-N: H7 is one channel with four targets."""
    source = routes.h.hero()
    actual = {target: routes.path(routes.run(source, target=target)[0])[0]
              for target in routes.H7_TARGETS}
    def oracle(value):
        assert set(value) == {'H7-R1-V1', 'H7-A', 'H7-D', 'H7-E'}
        for target, path in value.items():
            assert path == ('H7-CHANNEL', target)
        assert {path[0] for path in value.values()} == {'H7-CHANNEL'}
    mutant = {target: ('independent-channel-' + str(index), target)
              for index, target in enumerate(routes.H7_TARGETS)}
    _reject(actual, mutant, oracle)


@pytest.mark.parametrize('promotion', ('institutional_authority', 'observed_correction'))
def test_vf040_n_mailbox_and_owner_disclosure_cannot_become_authority_or_effect(promotion):
    """VALIDATION_PLAN12.11 VF040-N keeps channel metadata attributable."""
    source = routes.small(authority=False)
    out = routes.run(source)[0]
    routes.assert_route(out, routes.direct_path())
    routes.assert_no_authority(out, 'authority_unestablished')
    actual = routes.payload(out)['channel']['native_record']
    expected = routes.h.cases.by_id(source, 'channel')
    def oracle(value):
        assert value['data'] == expected['data']
        assert value['provenance'] == expected['provenance']
        assert value['data']['contact_locator'] == 'mailto:inert@example.invalid'
        assert not {'institutional_authority', 'observed_correction'} & set(value['data'])
    mutant = copy.deepcopy(actual)
    mutant['data'][promotion] = {'established': True,
                                 'basis': mutant['data']['contact_locator']}
    _reject(actual, mutant, oracle)


def test_vf041_n_handling_and_change_events_cannot_become_five_submissions(h7_outcomes):
    """VALIDATION_PLAN12.12 VF041-N requires acceptance before corruption."""
    _, out = h7_outcomes
    actual = _count(out, outcomes.FIELDS[0])
    mutant = dict(actual, value=5, members=('H7-CASE1', 'H7-HAND1',
                  'H7-CHANGE-A', 'H7-CHANGE-D', 'H7-CHANGE-R1'))
    _reject(actual, mutant, _count_oracle(1, ('H7-CASE1',)))


def test_vf042_n_latest_failed_event_cannot_erase_accepted_handling(failed_handling):
    """VALIDATION_PLAN12.12 VF042-N: two event IDs survive native chronology."""
    _, out = failed_handling
    actual = _count(out, outcomes.FIELDS[1])
    mutant = dict(actual, value=1, members=('handling-failed',))
    _reject(actual, mutant, _count_oracle(2, ('handling', 'handling-failed')))


@pytest.mark.parametrize('invented', ('handling', 'later-version'))
def test_vf043_n_accepted_request_or_unlinked_version_is_not_a_change_event(invented):
    """VALIDATION_PLAN12.12 VF043-N: no source change-event record exists."""
    source = outcomes.remove_events(outcomes.small(), 'change')
    later = outcomes.duplicate(source, 'claim2', 'later-version')
    later['data']['version_label'] = 'v3'
    out = outcomes.run(source)[0]
    outcomes.assert_effect(out, available=False)
    actual = _count(out, outcomes.FIELDS[2])
    mutant = dict(actual, value=1, members=(invented,))
    _reject(actual, mutant, _count_oracle(0, ()))


def test_vf044_n_two_events_on_one_case_target_cannot_be_two_documentary_targets():
    """VALIDATION_PLAN12.12 VF044-N, W7-22: events and pairs differ."""
    source = outcomes.small()
    outcomes.duplicate(source, 'change', 'change2')
    out = outcomes.run(source)[0]
    _count_oracle(2, ('change', 'change2'))(_count(out, outcomes.FIELDS[2]))
    actual = _count(out, outcomes.FIELDS[3])
    mutant = dict(actual, value=2, members=(('submission', 'claim'), ('submission', 'claim')))
    _reject(actual, mutant, _count_oracle(1, (('submission', 'claim'),)))


def test_vf045_n_three_changed_targets_cannot_be_three_cases(h7_outcomes):
    """VALIDATION_PLAN12.12 VF045-N: the three H7 pairs belong to CASE1."""
    _, out = h7_outcomes
    assert outcomes.pairs(out) == outcomes.H7_PAIRS
    actual = _count(out, outcomes.FIELDS[4])
    mutant = dict(actual, value=3, members=('H7-CASE1', 'H7-CASE1', 'H7-CASE1'))
    _reject(actual, mutant, _count_oracle(1, ('H7-CASE1',)))


@pytest.mark.parametrize('corruption', ('runtime_failure', 'delete_accepted'))
def test_vf046_n_native_failed_never_becomes_runtime_failure_or_latest_only(failed_handling, corruption):
    """VALIDATION_PLAN12.12 VF046-N preserves both native handling records."""
    source, out = failed_handling
    actual = {'execution_state': outcomes.leaf(out, outcomes.FIELDS[5]).execution_state,
              'records': outcomes.disclosures(out)}
    def oracle(value):
        assert value['execution_state'] == 'completed'
        for identifier, native in (('handling', 'accepted'), ('handling-failed', 'failed')):
            assert identifier in value['records']
            record = value['records'][identifier]['native_record']
            assert record['data'] == outcomes.h.cases.by_id(source, identifier)['data']
            assert record['data']['details']['outcome'] == native
    mutant = copy.deepcopy(actual)
    if corruption == 'runtime_failure':
        mutant['execution_state'] = 'failed'
    else:
        del mutant['records']['handling']
    _reject(actual, mutant, oracle)


@pytest.mark.parametrize('corruption', ('failed_effect', 'add_unselected_targets'))
def test_vf047_n_undocumented_e_cannot_be_failed_or_enlarged_to_b_c(h7_outcomes, corruption):
    """VALIDATION_PLAN12.12 VF047-N retains CASE1's exact selected targets."""
    _, out = h7_outcomes
    actual = outcomes.disclosures(out, outcomes.FIELDS[6])
    def oracle(value):
        assert set(value) == {'H7-R1-V1', 'H7-A', 'H7-D', 'H7-E'}
        row = next(row for row in value['H7-E']['case_rows'] if row['case_ref'] == 'H7-CASE1')
        assert row['requested_effect_state'] == 'unavailable'
        assert row['qualified_change_event_refs'] == []
        assert 'change_evidence_missing' in row['reason_codes']
        assert 'failed' not in str(row)
    mutant = copy.deepcopy(actual)
    if corruption == 'failed_effect':
        mutant['H7-E']['case_rows'][0]['requested_effect_state'] = 'failed'
    else:
        mutant['H7-B'] = copy.deepcopy(actual['H7-E'])
        mutant['H7-C'] = copy.deepcopy(actual['H7-E'])
    _reject(actual, mutant, oracle)


def test_vf048_n_capacity_strings_cannot_become_a_utilization_score():
    """VALIDATION_PLAN12.12 VF048-N leaves externally reported strings exact."""
    source = outcomes.small()
    outcomes.capacity(source, value='10 cases/day', load='7 cases/day')
    out = outcomes.run(source)[0]
    actual = outcomes.disclosures(out, outcomes.FIELDS[7])['capacity']
    def oracle(value):
        assert value['native_record']['data'] == outcomes.h.cases.by_id(source, 'capacity')['data']
        assert value['native_record']['data']['details']['reported_capacity'] == '10 cases/day'
        assert not {'utilization', 'adequacy', 'capacity_estimate'} & set(value)
    mutant = copy.deepcopy(actual)
    mutant['utilization'] = 0.7
    _reject(actual, mutant, oracle)


@pytest.mark.parametrize('kind', ('software_agent', 'organization'))
def test_vf050_n_nonhuman_actor_cannot_be_presented_as_human_reviewer(kind):
    """VALIDATION_PLAN12.13 VF050-N also requires structural rejection."""
    source = human.h.hero()
    out = human.run(source)[0]
    actual = human.disclosures(out)
    expected_actor = human.h.cases.by_id(source, 'H7-REVIEWER')['data']
    def oracle(value):
        human.assert_review(value, source)
        assert value['H7-REVIEWER']['data'] == expected_actor
        assert value['H7-REVIEWER']['data']['actor_kind'] == 'human'
    mutant = copy.deepcopy(actual)
    mutant['H7-REVIEWER']['data']['actor_kind'] = kind
    _reject(actual, mutant, oracle)
    # The same substitution as input is rejected by the actual admission gate.
    changed = copy.deepcopy(source)
    human.h.cases.by_id(changed, 'H7-REVIEWER')['data']['actor_kind'] = kind
    rejected = human._prepare_value(changed)
    assert type(rejected) is human._SafeDiagnostic
    assert (rejected.input_state, rejected.code) == ('rejected', 'endpoint_or_claim_mismatch')


@pytest.mark.parametrize('corruption', ('acquisition_as_model', 'acquisition_as_correction', 'complete_model'))
def test_vf054_n_acquisition_completeness_cannot_replace_other_history(corruption):
    """VALIDATION_PLAN12.15 VF054-N binds coverage to its exact native scope."""
    source = provenance.hero()
    out = provenance.run_profile(source)[0]
    actual = provenance.disclosures(out, 'coverage_disclosures')
    def oracle(value):
        for identifier in ('H7-COV-ACQ', 'H7-COV-MODEL', 'H7-COV-ROUTE'):
            original = provenance.cases.by_id(source, identifier)
            actual_data, expected_data = value[identifier]['data'], original['data']
            assert actual_data['assessment_kind'] == expected_data['assessment_kind']
            assert set(actual_data['subject_refs']) == set(expected_data['subject_refs'])
            for key, expected in expected_data['details'].items():
                if key in ('relation_types', 'dimensions', 'member_refs', 'omitted_refs'):
                    assert set(actual_data['details'][key]) == set(expected)
                else:
                    assert actual_data['details'][key] == expected
            assert value[identifier]['scope'] == original['scope']
        assert value['H7-COV-ACQ']['data']['details']['state'] == 'complete_for_scope'
        assert value['H7-COV-MODEL']['data']['details']['state'] == 'partial'
        assert value['H7-COV-ROUTE']['data']['details']['coverage_kind'] == 'correction_routes'
    mutant = copy.deepcopy(actual)
    if corruption == 'complete_model':
        mutant['H7-COV-MODEL']['data']['details']['state'] = 'complete_for_scope'
    else:
        mutant['H7-COV-ACQ']['data']['details']['coverage_kind'] = (
            'model_history' if corruption == 'acquisition_as_model' else 'correction_routes')
    _reject(actual, mutant, oracle)


def _replace_literal(value, before, after):
    if type(value) is dict:
        return {key: _replace_literal(item, before, after) for key, item in value.items()}
    if type(value) is list:
        return [_replace_literal(item, before, after) for item in value]
    return after if value == before else value


def test_vf055_n_uninspectable_support_cannot_rewrite_native_documentary_basis():
    """VALIDATION_PLAN12.15 VF055-N keeps declared label beside its basis gap."""
    source = provenance.hero()
    support = provenance.cases.by_id(source, 'H7-SUP-CHAIN')
    support.update(reference_kind='external_locator', availability='locator_only',
                   locator='https://example.invalid/w14-inert-document', excerpt=None)
    out = provenance.run_profile(source)[0]
    actual = provenance.disclosures(out, 'documentary_basis_gap_disclosures')['H7-L01']
    def oracle(value):
        tokens = provenance.tokens(value)
        assert 'documented_record' in tokens
        assert 'support_uninspectable' in tokens
        assert provenance.cases.by_id(source, 'H7-L01')['provenance']['basis_kind'] == 'documented_record'
    mutant = _replace_literal(actual, 'documented_record', 'upstream_inference')
    _reject(actual, mutant, oracle)


@pytest.mark.parametrize('corruption', ('qualified_only', 'upgrade_inference'))
def test_vf056_n_declared_inventory_cannot_drop_weak_rows_or_upgrade_inference(corruption):
    """VALIDATION_PLAN12.15 VF056-N counts declared labels, including weak rows."""
    source = provenance.hero()
    provenance.cases.by_id(source, 'H7-L01')['provenance']['basis_kind'] = 'upstream_inference'
    support = provenance.cases.by_id(source, 'H7-SUP-CHAIN')
    support.update(reference_kind='external_locator', availability='withheld',
                   locator='https://example.invalid/w14-withheld', excerpt=None)
    out = provenance.run_profile(source)[0]
    actual = provenance.partition(out, 'declared_basis_inventory')
    expected = {'declaration': (0, ()),
                'documented_record': (6, tuple('H7-L%02d' % number for number in range(2, 8))),
                'upstream_inference': (1, ('H7-L01',)),
                'protected_attestation': (0, ()), 'unspecified': (0, ())}
    def oracle(value):
        assert value == expected
        assert sum(count for count, _ in value.values()) == 7
    mutant = copy.deepcopy(actual)
    if corruption == 'qualified_only':
        mutant = {key: (0, ()) for key in expected}
    else:
        mutant['upstream_inference'] = (0, ())
        mutant['direct_observation'] = (1, ('H7-L01',))
    _reject(actual, mutant, oracle)


@pytest.mark.parametrize('availability', ('locator_only', 'withheld'))
def test_vf057_n_a_pointer_cannot_upgrade_unavailable_content_to_supplied(availability):
    """VALIDATION_PLAN12.15 VF057-N counts actual reference availability."""
    source = provenance.hero()
    support = provenance.cases.by_id(source, 'H7-SUP-CHAIN')
    support.update(reference_kind='external_locator', availability=availability,
                   locator='https://example.invalid/w14-pointer', excerpt=None)
    out = provenance.run_profile(source)[0]
    actual = provenance.partition(out, 'reference_availability_inventory')
    expected = {state: (0, ()) for state in provenance.AVAILABILITY}
    expected['supplied'] = (7, tuple(name for name in provenance.H7_SUPPORT if name != 'H7-SUP-CHAIN'))
    expected[availability] = (1, ('H7-SUP-CHAIN',))
    def oracle(value):
        assert value == expected
        assert sum(count for count, _ in value.values()) == 8
    mutant = copy.deepcopy(actual)
    mutant['supplied'] = (8, provenance.H7_SUPPORT)
    mutant[availability] = (0, ())
    _reject(actual, mutant, oracle)
