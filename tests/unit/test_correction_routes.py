# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W10 independent route/grant oracles, Definitions 27.1 and VF038--VF040.

The supplied H7 tuples and finite hand-authored routes fix expected witnesses.
A declared channel, every-leg grant, observed change and capacity remain
separate. These owner-local cases do not claim public W13 orchestration.
"""
import copy
from dataclasses import FrozenInstanceError
import importlib.util
from pathlib import Path

import pytest

from source_integrity_toolkit.analysis import correction_routes as routes
from source_integrity_toolkit.contracts.bundle import _Object
from source_integrity_toolkit.contracts.evidence import _Node
from source_integrity_toolkit.contracts.execution import _AnalysisAborted
from source_integrity_toolkit.runtime import resources
from source_integrity_toolkit.validation.limits import _WitnessLedger

_spec = importlib.util.spec_from_file_location(
    'sit_w10_route_helpers', Path(__file__).with_name('test_process_comparison.py'))
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)
FIELDS = ('declared_correction_route_witnesses', 'applicable_authorized_route_witnesses',
          'correction_route_disclosures')
H7_TARGETS = ('H7-R1-V1', 'H7-A', 'H7-D', 'H7-E')
STAMP = '2026-01-10T13:00:00Z'


def known(value=STAMP, precision='instant'):
    return {'state': 'known', 'value': value, 'precision': precision}


def window(start='2026-01-10T00:00:00Z', end='2026-01-10T23:59:59Z'):
    return {'start': known(start), 'end': known(end)}


def time_node(value=STAMP, precision='instant'):
    return _Node('TimeValue', _Object(tuple(sorted(known(value, precision).items()))))


def supplied(row):
    row['provenance'].update(basis_kind='documented_record', evidence_ref_ids=['support'],
        method='Examine the supplied finite fictional grant and routing record.',
        qualifications=['Attributed documentary material without outside authentication.'])
    return row


def channel(source, identifier, targets=('claim',)):
    row = h.cases.record(identifier, 'correction_channel', {'owner_refs': ['actor'],
        'target_refs': list(targets), 'contact_locator': 'mailto:inert@example.invalid',
        'declared_action_types': ['amend'], 'valid_window': window()})
    if not targets:
        row['gaps'] = [{'field': 'data.target_refs', 'reason': 'not_recorded',
                        'detail': 'Direct targets not recorded; separate propagation is supplied.'}]
    source['records'].append(supplied(row))
    for coverage in source['assertions']:
        if coverage['id'] == 'coverage':
            coverage['data']['subject_refs'].append(identifier)
            coverage['data']['details']['member_refs'].append(identifier)
    return row


def grant(source, identifier, subject, *, state='granted', targets=('claim',), actions=('amend',)):
    row = h.cases.assertion(identifier, 'assessment', {'assessment_kind': 'authority',
        'subject_refs': [subject], 'details': {'target_refs': list(targets),
            'action_types': list(actions), 'valid_window': window(), 'authorized_by_ref': 'actor',
            'grant_state': state, 'authority_basis': 'Supplied authority for the exact tuple only.',
            'coverage_ref': 'coverage'}})
    row['scope']['effective_window'] = window()
    row['asserted_at'] = known()
    source['assertions'].append(supplied(row))
    return row


def edge(source, identifier, start, end, *, action='amend'):
    row = h.cases.assertion(identifier, 'relation', {'predicate': 'propagates_to',
        'from_ref': start, 'to_ref': end, 'polarity': 'affirmed', 'dimension': None,
        'details': {'action_type': action, 'valid_window': window()}})
    row['scope']['effective_window'] = window()
    row['asserted_at'] = known()
    source['assertions'].append(supplied(row))
    return row


def small(*, direct=True, authority=True, coverage='partial'):
    source = h.cases.pool()
    source['records'] = [r for r in source['records'] if r['kind'] not in ('correction_channel', 'correction_event')]
    source['assertions'] = []
    inquiry = source['inquiries'][0]
    inquiry.update(as_of=known(), time_window=window(), coverage_assertion_refs=['coverage'])
    channel(source, 'channel', ('claim',) if direct else ())
    row = h.cases.assertion('coverage', 'assessment', {'assessment_kind': 'coverage',
        'subject_refs': ['channel'], 'details': {'coverage_kind': 'correction_routes',
            'state': coverage, 'relation_types': ['propagates_to'], 'dimensions': [],
            'member_refs': ['channel', 'claim'], 'omitted_refs': [],
            'universe_enumerated': coverage == 'complete_for_scope',
            'scope_note': 'Only this finite supplied direct-target and propagation view for amend.'}})
    row['scope']['effective_window'] = window()
    row['asserted_at'] = known()
    source['assertions'].append(supplied(row))
    if authority:
        grant(source, 'grant', 'channel')
    return source


def two_leg():
    source = small(direct=False)
    channel(source, 'channel2')
    edge(source, 'leg-1', 'channel', 'channel2')
    grant(source, 'grant-2', 'channel2')
    return source


def context(source, *, start=None, target=None, action='amend', temporal_basis='time_specific',
            requested_time=None, claims=None):
    hero = source['inquiries'][0]['id'] == 'H7-I1'
    return h.context(source, subject_refs=(start or ('H7-CHANNEL' if hero else 'channel'),
            target or ('H7-R1-V1' if hero else 'claim')),
        dependency_dimension=None, graph_view='correction_routing',
        coverage_kind='correction_routes', relation_types=('propagates_to',),
        operation_anchor=(action,), temporal_basis=temporal_basis,
        requested_time=(requested_time or time_node()) if temporal_basis == 'time_specific' else None,
        claim_refs=tuple(claims or source['inquiries'][0]['target_claim_refs'][:1]))


def run(source, **changes):
    original = copy.deepcopy(source)
    prepared = h.admit(source)
    ctx = context(source, **changes)
    owner, job = h.job_pair()
    ledger = owner.witnesses
    before = owner.used, job.used, ledger._retained_witnesses, ledger._retained_members
    out = routes._correction_routes(prepared, ctx, ledger, job)
    assert source == original
    assert out.facts.prepared is prepared and out.facts.context is ctx and out.facts.job_port is job
    assert owner.used - before[0] == job.used - before[1] > 0
    assert ledger._retained_witnesses - before[2] == len(out.witnesses)
    assert ledger._retained_members - before[3] == sum(w.member_count for w in out.witnesses)
    assert tuple(row.ref.field_key for row in out.results) == FIELDS
    for row in out.results:
        assert row.ref.diagnostic_id == 'SIT-M011'
        assert row.execution_state == 'completed'
        scope = row.ref.scope
        assert scope.inquiry_ref.identifier == ctx.inquiry_ref
        assert tuple(r.identifier for r in scope.claim_refs) == ctx.claim_refs
        assert tuple(r.identifier for r in scope.target_refs) == ctx.subject_refs
        assert scope.operation_anchor == ctx.operation_anchor
        assert scope.temporal_basis == ctx.temporal_basis and scope.graph_view == 'correction_routing'
        assert row.basis_refs and row.interpretation_limit
        assert all(check.result_ref is row.ref for check in row.check_refs)
        assert all(reason.scope is scope and row.ref in reason.affected_result_refs for reason in row.reason_refs)
        assert all(witness.scope is scope for witness in row.witness_refs)
        checks = {check.check_id: check.state for check in row.check_refs}
        assert checks['PC01'] == checks['PC02'] == checks['PC24'] == 'met'
        assert {'PC04', 'PC05', 'PC06', 'PC09', 'PC10', 'PC19', 'PC20'} <= checks.keys()
    return out, prepared, owner, job


def leaf(out, field=FIELDS[0]):
    return next(row for row in out.results if row.ref.field_key == field)


def codes(out, field=FIELDS[1]):
    return {reason.code for reason in leaf(out, field).reason_refs}


def payload(out):
    row = leaf(out, FIELDS[2])
    assert (row.result_state, row.value_kind) == ('available', 'record_disclosures')
    return {item.source.identifier: h.native(item.fields) for item in row.value.records}


def native_disclosures(out, source, identifiers):
    rows = {identifier: row['native_record'] for identifier, row in payload(out).items()}
    for identifier in identifiers:
        assert identifier in rows
        original = h.cases.by_id(source, identifier)
        for key in h.NATIVE_KEYS if 'assertion_kind' in original else ('data', 'provenance'):
            assert rows[identifier][key] == original[key]
        for key in ('gaps', 'extensions'):
            if key in original:
                assert rows[identifier][key] == original[key]
    return rows


def path(out, *, authorized=False):
    item = out.facts.authorized_path if authorized else out.facts.declared_path
    if item is None:
        return None
    return (tuple(n.identifier for n in item.nodes),
            tuple((e.source_ref.collection, e.source_ref.record_id, e.source_ref.selector, e.target.identifier)
                  for e in item.edges))


def direct_path(start='channel', target='claim'):
    return ((start, target), (('records', start, 'data.target_refs', target),))


def assert_route(out, expected, *, authorized=False):
    row = leaf(out, FIELDS[1] if authorized else FIELDS[0])
    assert row.result_state == 'available' and row.value_kind == 'witness_collection'
    assert path(out, authorized=authorized) == expected
    assert bool(row.value.witness_refs) == (expected is not None)
    assert row.value.witness_refs == tuple(w for w in row.witness_refs if w.kind == 'path')


def assert_no_authority(out, reason=None):
    row = leaf(out, FIELDS[1])
    assert row.result_state == 'unavailable' and row.value is None
    assert path(out, authorized=True) is None
    if reason:
        assert reason in codes(out)


@pytest.fixture(scope='module')
def hero_profiles():
    source = h.hero()
    return source, {target: run(source, target=target)[0] for target in H7_TARGETS}


def test_vf038_p_h7_four_exact_target_tuples_use_real_canonical_links(hero_profiles):
    source, outputs = hero_profiles
    for target, out in outputs.items():
        assert_route(out, direct_path('H7-CHANNEL', target))
        assert not any(e.source_ref.collection == 'assertions' for e in out.facts.declared_path.edges)
    assert {path(out)[0][0] for out in outputs.values()} == {'H7-CHANNEL'}


def test_vf038_n_parallel_routes_and_cycle_never_multiply_channel_or_walks():
    source = two_leg()
    edge(source, 'cycle-return', 'channel2', 'channel')
    edge(source, 'parallel', 'channel', 'channel2')
    out = run(source)[0]
    expected = (('channel', 'channel2', 'claim'), (('assertions', 'leg-1', '', 'channel2'),
                ('records', 'channel2', 'data.target_refs', 'claim')))
    assert_route(out, expected)
    assert len(leaf(out).value.witness_refs) == 1
    assert len(out.facts.declared_path.nodes) == len(set(n.identifier for n in out.facts.declared_path.nodes))
    cycles = [w for w in out.witnesses if w.kind == 'cycle']
    assert len(cycles) == 1
    assert tuple(n.identifier for n in cycles[0].nodes) == ('channel', 'channel2', 'channel')


def test_vf038_m_partial_route_absence_is_scoped_empty_witness():
    out = run(small(direct=False))[0]
    assert_route(out, None)
    assert 'route_not_recorded' in codes(out, FIELDS[0])
    assert 'partial' in str(payload(out)).lower()
    assert 'supplied' in leaf(out).interpretation_limit.lower() or 'recorded' in leaf(out).interpretation_limit.lower()


def test_vf038_b_two_leg_routes_need_each_leg_action_and_survive_cycles():
    source = two_leg()
    edge(source, 'back', 'channel2', 'channel')
    good = run(source)[0]
    assert path(good) and path(good, authorized=True)
    h.cases.by_id(source, 'leg-1')['data']['details']['action_type'] = 'review'
    bad = run(source)[0]
    assert_route(bad, None)
    assert path(bad, authorized=True) is None


def test_vf039_p_h7_each_amend_tuple_has_exact_documented_grant(hero_profiles):
    source, outputs = hero_profiles
    for target, out in outputs.items():
        assert_route(out, direct_path('H7-CHANNEL', target), authorized=True)
        native_disclosures(out, source, ('H7-AUTH', 'H7-COV-ROUTE'))
        assert next(c for c in leaf(out, FIELDS[1]).check_refs if c.check_id == 'PC20').state == 'met'


@pytest.mark.parametrize('change', ('missing', 'wrong_action', 'wrong_version', 'expired_window'))
def test_vf039_n_one_inapplicable_leg_blocks_stronger_route_only(change):
    source = two_leg()
    row = h.cases.by_id(source, 'grant-2')
    if change == 'missing':
        source['assertions'].remove(row)
    elif change == 'wrong_action':
        row['data']['details']['action_types'] = ['review']
    elif change == 'wrong_version':
        row['data']['details']['target_refs'] = ['claim2']
    else:
        row['data']['details']['valid_window'] = window('2025-01-10T00:00:00Z', '2025-01-10T23:59:59Z')
    out = run(source)[0]
    assert path(out) is not None
    assert_no_authority(out, 'authority_unestablished' if change == 'missing' else 'authority_inapplicable')
    pc20 = next(c for c in leaf(out, FIELDS[1]).check_refs if c.check_id == 'PC20')
    assert pc20.state == ('unknown' if change == 'missing' else 'unmet')


@pytest.mark.parametrize('change', ('unknown_grant', 'declaration', 'withheld_support', 'missing_basis'))
def test_vf039_m_unknown_or_unsupported_grant_stays_unestablished(change):
    source = small()
    row = h.cases.by_id(source, 'grant')
    if change == 'unknown_grant':
        row['data']['details']['grant_state'] = 'unknown'
    elif change == 'declaration':
        row['provenance'].update(basis_kind='declaration', evidence_ref_ids=[])
    elif change == 'withheld_support':
        support = source['evidence_references'][0]
        support.update(reference_kind='external_locator', availability='withheld', excerpt=None,
                       locator='https://example.invalid/unavailable-grant')
    else:
        row['data']['details']['authority_basis'] = None
        row['gaps'] = [{'field': 'data.details.authority_basis', 'reason': 'not_recorded',
                        'detail': 'Authority basis not supplied.'}]
    out = run(source)[0]
    assert_route(out, direct_path())
    assert_no_authority(out)
    native_disclosures(out, source, ('grant',))


@pytest.mark.parametrize('mode', ('date', 'unknown', 'snapshot'))
def test_vf039_b_uncertain_effective_time_cannot_authorize_instant(mode):
    source = small()
    changes = {}
    if mode == 'snapshot':
        changes['temporal_basis'] = 'snapshot_structural'
    else:
        stamp = known('2026-01-10', 'date') if mode == 'date' else h.cases.unknown()
        h.cases.by_id(source, 'grant')['data']['details']['valid_window']['start'] = stamp
    out = run(source, **changes)[0]
    assert_route(out, direct_path())
    assert_no_authority(out)
    assert next(c for c in leaf(out, FIELDS[1]).check_refs if c.check_id == 'PC10').state == 'unknown'


def test_vf040_p_native_channel_grant_scope_window_and_basis_stay_together(hero_profiles):
    source, outputs = hero_profiles
    for target, out in outputs.items():
        rows = native_disclosures(out, source, ('H7-CHANNEL', 'H7-AUTH', 'H7-COV-ROUTE'))
        assert rows['H7-AUTH']['data']['details']['action_types'] == ['amend']
        assert rows['H7-CHANNEL']['data']['contact_locator'] is None
        assert path(out)[0] == ('H7-CHANNEL', target)
        assert leaf(out).ref.scope.operation_anchor == ('amend',)


def test_vf040_n_mailbox_owner_and_action_list_never_manufacture_authority_or_effect():
    source = small(authority=False)
    out = run(source)[0]
    assert_route(out, direct_path())
    assert_no_authority(out, 'authority_unestablished')
    native_disclosures(out, source, ('channel',))
    assert all(row.value_kind in ('record_disclosures', 'witness_collection') for row in out.results)
    limits = ' '.join(row.interpretation_limit for row in out.results).lower()
    assert 'effect' in limits and 'capacity' in limits


def test_vf040_m_incomplete_grants_retain_declared_route_and_native_uncertainty():
    source = two_leg()
    h.cases.by_id(source, 'grant-2')['data']['details']['grant_state'] = 'unknown'
    out = run(source)[0]
    assert path(out) is not None
    assert_no_authority(out, 'authority_unestablished')
    rows = native_disclosures(out, source, ('channel', 'channel2', 'grant', 'grant-2', 'leg-1'))
    assert rows['grant-2']['data']['details']['grant_state'] == 'unknown'


@pytest.mark.parametrize('state', ('denied', 'expired', 'unknown'))
def test_vf040_b_grant_states_remain_attributed_without_newest_wins(state):
    source = small()
    row = h.cases.by_id(source, 'grant')
    row['data']['details']['grant_state'] = state
    out = run(source)[0]
    assert_route(out, direct_path())
    assert_no_authority(out)
    assert native_disclosures(out, source, ('grant',))['grant']['data']['details']['grant_state'] == state
    pc20 = next(c for c in leaf(out, FIELDS[1]).check_refs if c.check_id == 'PC20')
    assert pc20.state == ('unknown' if state == 'unknown' else 'unmet')


@pytest.mark.parametrize('denial_supported', (True, False))
def test_conflicting_granted_and_denied_records_block_authority_even_with_later_grant(denial_supported):
    source = small()
    denial = grant(source, 'older-denial', 'channel', state='denied')
    denial['asserted_at'] = known('2026-01-10T01:00:00Z')
    if not denial_supported:
        denial['provenance'].update(basis_kind='declaration', evidence_ref_ids=[])
    out = run(source)[0]
    assert_route(out, direct_path())
    assert_no_authority(out)
    rows = native_disclosures(out, source, ('grant', 'older-denial'))
    assert {rows[key]['data']['details']['grant_state'] for key in ('grant', 'older-denial')} == {'granted', 'denied'}


def test_later_valid_alternative_is_found_after_first_unauthorized_route():
    source = small()
    channel(source, 'a-blocked')
    channel(source, 'z-valid')
    h.cases.by_id(source, 'channel')['data']['target_refs'] = []
    h.cases.by_id(source, 'channel')['gaps'] = [{'field': 'data.target_refs', 'reason': 'not_recorded', 'detail': 'Via recorded propagation only.'}]
    edge(source, '00-blocked', 'channel', 'a-blocked')
    edge(source, '10-valid', 'channel', 'z-valid')
    grant(source, 'valid-tail-grant', 'z-valid')
    out = run(source)[0]
    assert path(out)[0] == ('channel', 'a-blocked', 'claim')
    assert path(out, authorized=True)[0] == ('channel', 'z-valid', 'claim')
    assert_route(out, path(out, authorized=True), authorized=True)


def test_shortest_authorized_path_ignores_longer_lexically_earlier_route():
    source = two_leg()
    channel(source, 'a-detour', ())
    edge(source, '00-detour', 'channel', 'a-detour')
    edge(source, '01-return', 'a-detour', 'channel2')
    grant(source, 'detour-grant', 'a-detour')
    out = run(source)[0]
    assert path(out, authorized=True)[0] == ('channel', 'channel2', 'claim')
    assert path(out, authorized=True)[1][0][1] == 'leg-1'


def test_equal_length_tie_compares_complete_edge_prefix_not_last_predecessor():
    source = small(direct=False)
    for name in ('a-middle', 'z-middle'):
        channel(source, name, ())
        grant(source, name + '-grant', name)
    edge(source, '00-first', 'channel', 'z-middle')
    edge(source, '99-last', 'z-middle', 'claim')
    edge(source, '10-first', 'channel', 'a-middle')
    edge(source, '01-last', 'a-middle', 'claim')
    out = run(source)[0]
    expected = (('channel', 'z-middle', 'claim'),
                (('assertions', '00-first', '', 'z-middle'), ('assertions', '99-last', '', 'claim')))
    assert_route(out, expected)
    assert_route(out, expected, authorized=True)
    source['records'].reverse()
    source['assertions'].reverse()
    other = run(source)[0]
    assert_route(other, expected)
    assert_route(other, expected, authorized=True)


@pytest.mark.parametrize('owner', ('channel', 'edge'))
def test_unknown_required_leg_time_prevents_authorization(owner):
    source = two_leg()
    row = h.cases.by_id(source, 'channel2' if owner == 'channel' else 'leg-1')
    data = row['data'] if owner == 'channel' else row['data']['details']
    data['valid_window'] = h.cases.window()
    coverage = h.cases.by_id(source, 'coverage')['data']['details']
    coverage.update(state='complete_for_scope', universe_enumerated=True)
    out = run(source)[0]
    assert_no_authority(out)
    assert not out.facts.bounded_absence
    assert next(c for c in leaf(out).check_refs if c.check_id == 'PC06').state != 'met'
    assert next(c for c in leaf(out, FIELDS[1]).check_refs if c.check_id == 'PC10').state == 'unknown'


def test_exact_target_version_does_not_follow_same_name_or_supersession():
    source = small()
    source['assertions'].append(h.cases.relation('supersedes'))
    out = run(source, target='claim2')[0]
    assert_route(out, None)
    assert path(out, authorized=True) is None


@pytest.mark.parametrize('coverage_state,supported', (('partial', True), ('complete_for_scope', True), ('complete_for_scope', False)))
def test_no_route_retains_actual_complete_or_partial_coverage_basis(coverage_state, supported):
    source = small(direct=False, coverage=coverage_state)
    channel_row = h.cases.by_id(source, 'channel')
    channel_row['data']['target_refs'] = ['claim2']
    channel_row.pop('gaps')
    row = h.cases.by_id(source, 'coverage')
    row['data']['details']['member_refs'].append('claim2')
    if not supported:
        row['provenance'].update(basis_kind='declaration', evidence_ref_ids=[])
    out = run(source)[0]
    assert_route(out, None)
    assert 'route_not_recorded' in codes(out, FIELDS[0])
    native_disclosures(out, source, ('coverage',))
    pc06 = next(check for check in leaf(out).check_refs if check.check_id == 'PC06')
    assert (pc06.state == 'met') == (coverage_state == 'complete_for_scope' and supported)


def test_unrelated_wrong_claim_grant_does_not_authorize_selected_claim():
    source = small()
    source['inquiries'][0]['target_claim_refs'].append('claim2')
    h.cases.by_id(source, 'grant')['scope']['claim_refs'] = ['claim2']
    out = run(source)[0]
    assert_route(out, direct_path())
    assert_no_authority(out)


@pytest.mark.parametrize('coverage_state', ('absent', 'not_examined'))
def test_positive_exact_grant_does_not_require_global_route_coverage(coverage_state):
    source = small()
    row = h.cases.by_id(source, 'grant')
    if coverage_state == 'absent':
        row['data']['details']['coverage_ref'] = None
        row['gaps'] = [{'field': 'data.details.coverage_ref', 'reason': 'not_recorded',
                        'detail': 'The exact grant is supplied; exhaustive route coverage is not.'}]
    else:
        h.cases.by_id(source, 'coverage')['data']['details']['state'] = 'not_examined'
    out = run(source)[0]
    assert_route(out, direct_path(), authorized=True)
    native_disclosures(out, source, ('grant',))


def test_unresolved_exact_target_retains_declaration_without_authorized_identity():
    source = small()
    h.cases.by_id(source, 'channel')['data']['target_refs'] = ['unresolved']
    h.cases.by_id(source, 'grant')['data']['details']['target_refs'] = ['unresolved']
    h.cases.by_id(source, 'coverage')['data']['details']['member_refs'] = ['channel', 'unresolved']
    out = run(source, target='unresolved')[0]
    assert_route(out, direct_path(target='unresolved'))
    assert_no_authority(out)
    assert 'unknown_endpoint' in codes(out) or 'identity_unresolved' in codes(out)


@pytest.mark.parametrize('remaining', (25, 2500))
def test_interrupted_search_never_returns_completed_empty_route(remaining, monkeypatch):
    monkeypatch.setattr(resources, 'monotonic_ns', lambda: 100)
    source = two_leg()
    prepared = h.admit(source)
    owner, job = h.job_pair()
    job.charge(1_000_000 - job.used - remaining)
    with pytest.raises(_AnalysisAborted) as stopped:
        routes._correction_routes(prepared, context(source), owner.witnesses, job)
    assert stopped.value.limit_id == 'WU9-L11'
    assert stopped.value.stop.input_state == 'accepted'
    with pytest.raises(_AnalysisAborted) as again:
        routes._correction_routes(prepared, context(source), owner.witnesses, job)
    assert again.value is stopped.value


def test_witness_quota_interrupts_before_success_without_clipping(monkeypatch):
    monkeypatch.setattr(resources, 'monotonic_ns', lambda: 100)
    source = two_leg()
    prepared = h.admit(source)
    owner, job = h.job_pair()
    ledger = owner.witnesses
    ledger.retain(ledger.reserve(witnesses=20_000, members=0))
    with pytest.raises(_AnalysisAborted) as stopped:
        routes._correction_routes(prepared, context(source), ledger, job)
    assert stopped.value.limit_id == 'WU9-L13'


def test_immutable_results_and_foreign_ledger_cannot_supply_route_proofs():
    source = small()
    out, prepared, owner, job = run(source)
    for obj, attr in ((out, 'results'), (out.facts, 'declared_path'), (out.results[0], 'value')):
        with pytest.raises((FrozenInstanceError, AttributeError)):
            setattr(obj, attr, ())
    foreign, unused = h.job_pair()
    for ledger in (foreign.witnesses, _WitnessLedger(owner.witnesses.port)):
        with pytest.raises(TypeError):
            routes._correction_routes(prepared, context(source), ledger, job)
    assert foreign.witnesses._retained_witnesses == 0
