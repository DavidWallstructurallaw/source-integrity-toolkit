# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W04 graph stopping and authority controls, from architecture 18.2/19,
privacy WU9-L11-L13, governance 22.3 and approved Phase 3 sections 3.2/3.4.

Trusted component graphs and accounting preloads below are test construction,
not a claim of whole-invocation admission or end-to-end analytical execution.
The numeric thresholds are independent specification literals.
"""
import builtins
import ctypes
from dataclasses import FrozenInstanceError
import importlib.util
import inspect
from pathlib import Path
import socket
import subprocess

import pytest

from source_integrity_toolkit.contracts.evidence import (
    _PreparedBundle, _QualificationContext, _SourceAddress,
)
from source_integrity_toolkit.contracts.execution import _AnalysisAborted, _AuditCancelled
from source_integrity_toolkit.graph import projections, traversal, cycles, witnesses
from source_integrity_toolkit.runtime import resources
from source_integrity_toolkit.runtime.boundary import _prepare_value
from source_integrity_toolkit.validation.limits import _WitnessLedger

ROOT = Path(__file__).resolve().parents[2]
SPEC = importlib.util.spec_from_file_location('sit_w04_security_cases', ROOT / 'tests/contract/test_typed_records.py')
CASES = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CASES)


@pytest.fixture
def clock(monkeypatch):
    now = [100]
    monkeypatch.setattr(resources, 'monotonic_ns', lambda: now[0])
    return now


@pytest.fixture(scope='module')
def snapshot():
    value = CASES.pool()
    value['assertions'] = [CASES.relation('cites')]
    result = _prepare_value(value)
    assert type(result) is _PreparedBundle
    return result


def context():
    return _QualificationContext('inquiry', ('claim',), ('artifact', 'artifact2'),
        None, 'snapshot_structural', None, None, ('cites',), 'citation', ())


def job_pair():
    budget = resources._new_analysis_budget()
    budget.record_input_acceptance()
    return budget, budget.start_job()


def graph(snapshot, job):
    nodes = tuple(projections._GraphNode('records', name, 'artifact', ('records', name))
                  for name in ('artifact', 'artifact2', 'dataset'))
    address = _SourceAddress('assertions', 'r-cites')
    source = next(item for item in snapshot.entities if item.identifier == 'r-cites')
    edge = projections._GraphEdge(nodes[0], nodes[1],
        ('assertions', 'r-cites', '', 'records', 'artifact2'), address, 'cites', True, (), source)
    return projections._Projection(snapshot, context(), nodes, (edge,), (edge,), (), None, job)


def action(name, g, job, ledger):
    if name == 'projection':
        return lambda: projections._project(g.prepared, g.context, job)
    if name == 'path':
        return lambda: traversal._shortest_path(g, g.nodes[0], g.nodes[1], job)
    if name == 'absent_path':
        return lambda: traversal._shortest_path(g, g.nodes[0], g.nodes[2], job)
    if name == 'reachable':
        return lambda: traversal._reachable(g, (g.nodes[0],), job)
    if name == 'components':
        return lambda: cycles._components(g, job)
    if name == 'prerequisite':
        return lambda: projections._check_edge_eligibility(g, g.edges, job)
    if name == 'members':
        return lambda: witnesses._member_witness(g, g.nodes, ledger, job)
    raise AssertionError('unknown test operation')


OPERATIONS = ('projection', 'path', 'absent_path', 'reachable', 'components', 'prerequisite', 'members')


@pytest.mark.parametrize('operation', OPERATIONS)
def test_graph_work_cannot_start_after_per_job_ceiling(snapshot, clock, operation):
    owner, job = job_pair()
    g, ledger = graph(snapshot, job), owner.witnesses
    job.charge(1_000_000 - job.used)
    before = (owner.used, job.used)
    with pytest.raises(_AnalysisAborted) as stopped:
        action(operation, g, job, ledger)()
    assert stopped.value.limit_id == 'WU9-L11'
    assert stopped.value.stop.input_state == 'accepted'
    assert (owner.used, job.used) == before
    assert ledger._retained_witnesses == ledger._retained_members == 0


@pytest.mark.parametrize('operation', OPERATIONS)
def test_graph_work_cannot_create_new_invocation_budget(snapshot, clock, operation):
    owner = resources._new_analysis_budget()
    owner.charge(9_998_970)  # Six units remain for one job and its shared ledger.
    owner.record_input_acceptance()
    job = owner.start_job()
    g, ledger = graph(snapshot, job), owner.witnesses
    assert owner.used == 10_000_000
    with pytest.raises(_AnalysisAborted) as stopped:
        action(operation, g, job, ledger)()
    assert stopped.value.limit_id == 'WU9-L11'
    assert owner.used == 10_000_000
    assert ledger._retained_witnesses == 0


@pytest.mark.parametrize('operation', OPERATIONS)
def test_deadline_expiry_never_becomes_no_path_or_empty_success(snapshot, clock, operation):
    owner, job = job_pair()
    g, ledger = graph(snapshot, job), owner.witnesses
    before = (owner.used, job.used)
    clock[0] += 60_000_000_001
    with pytest.raises(_AnalysisAborted) as stopped:
        action(operation, g, job, ledger)()
    assert stopped.value.limit_id == 'WU9-L12'
    assert (owner.used, job.used) == before
    assert ledger._retained_witnesses == 0


@pytest.mark.parametrize('operation', OPERATIONS)
def test_interrupt_during_graph_work_does_not_deliver_partial_evidence(snapshot, clock, monkeypatch, operation):
    owner, job = job_pair()
    g, ledger = graph(snapshot, job), owner.witnesses
    before = job.used
    calls = [0]
    def interrupted_clock():
        calls[0] += 1
        return 100 if calls[0] <= 12 else 60_000_000_101
    monkeypatch.setattr(resources, 'monotonic_ns', interrupted_clock)
    with pytest.raises(_AnalysisAborted) as stopped:
        action(operation, g, job, ledger)()
    assert stopped.value.limit_id == 'WU9-L12' and job.used > before
    assert ledger._retained_witnesses == ledger._retained_members == 0
    with pytest.raises(_AnalysisAborted) as repeated:
        action(operation, g, job, ledger)()
    assert repeated.value is stopped.value


@pytest.mark.parametrize('operation', OPERATIONS)
def test_cancellation_propagates_payload_free_actual_state(snapshot, clock, monkeypatch, operation):
    owner, job = job_pair()
    g, ledger = graph(snapshot, job), owner.witnesses
    def cancelled():
        raise KeyboardInterrupt('FICTIONAL_PRIVATE_CANCEL_CANARY')
    monkeypatch.setattr(resources, 'monotonic_ns', cancelled)
    with pytest.raises(_AuditCancelled) as stopped:
        action(operation, g, job, ledger)()
    assert stopped.value.input_state == 'accepted'
    assert 'FICTIONAL_PRIVATE_CANCEL_CANARY' not in str(stopped.value)
    assert ledger._retained_witnesses == 0


@pytest.mark.parametrize('operation', OPERATIONS)
def test_finalization_only_port_cannot_restart_graph_analysis(snapshot, clock, operation):
    owner, job = job_pair()
    g, ledger = graph(snapshot, job), owner.witnesses
    job.charge(1_000_000 - job.used)
    with pytest.raises(_AnalysisAborted):
        job.charge(1)
    finalizer = owner.begin_finalization()
    before = owner.used
    with pytest.raises(TypeError, match='analysis_job_port_required'):
        action(operation, g, finalizer, ledger)()
    assert owner.used == before


@pytest.mark.parametrize('operation', ('path', 'absent_path', 'reachable', 'components', 'prerequisite', 'members'))
def test_semantic_projection_cannot_cross_jobs(snapshot, clock, operation):
    owner, first = job_pair()
    g, ledger = graph(snapshot, first), owner.witnesses
    owner.finish_job(first)
    second = owner.start_job()
    with pytest.raises(TypeError):
        action(operation, g, second, ledger)()
    assert ledger._retained_witnesses == 0


@pytest.mark.parametrize('operation', OPERATIONS)
def test_stale_port_preserves_failure_and_never_returns_graph_fact(snapshot, clock, operation):
    owner, first = job_pair()
    g, ledger = graph(snapshot, first), owner.witnesses
    owner.finish_job(first)
    owner.start_job()
    with pytest.raises(_AnalysisAborted) as stopped:
        action(operation, g, first, ledger)()
    assert stopped.value.stop.reason_code == 'execution_failed'
    assert ledger._retained_witnesses == 0


def test_foreign_invocation_witness_ledger_is_rejected(snapshot, clock):
    owner, job = job_pair()
    foreign_owner, foreign_job = job_pair()
    g, own_ledger, foreign_ledger = graph(snapshot, job), owner.witnesses, foreign_owner.witnesses
    with pytest.raises(TypeError):
        witnesses._member_witness(g, g.nodes, foreign_ledger, job)
    assert own_ledger._retained_witnesses == foreign_ledger._retained_witnesses == 0


def test_second_ledger_cannot_reset_the_same_invocation_witness_count(snapshot, clock):
    owner, job = job_pair()
    g, ledger = graph(snapshot, job), owner.witnesses
    ledger.retain(ledger.reserve(witnesses=20_000))
    duplicate = _WitnessLedger(job)  # Test-only forged private pairing.
    assert duplicate.port._owner is job._owner
    with pytest.raises(TypeError):
        witnesses._member_witness(g, g.nodes, duplicate, job)
    assert ledger._retained_witnesses == 20_000 and duplicate._retained_witnesses == 0


@pytest.mark.parametrize('existing,passes', ((19_998, True), (19_999, True), (20_000, False)))
def test_real_graph_witness_respects_exact_global_witness_ceiling(snapshot, clock, existing, passes):
    owner, job = job_pair()
    g, ledger = graph(snapshot, job), owner.witnesses
    ledger.retain(ledger.reserve(witnesses=existing))
    if passes:
        witnesses._member_witness(g, g.nodes, ledger, job)
        assert ledger._retained_witnesses == existing + 1
    else:
        with pytest.raises(_AnalysisAborted) as stopped:
            witnesses._member_witness(g, g.nodes, ledger, job)
        assert stopped.value.limit_id == 'WU9-L13'
        assert ledger._retained_witnesses == existing


@pytest.mark.parametrize('remaining,passes', ((4, True), (3, True), (2, False)))
def test_member_limit_keeps_whole_required_finite_set_or_interrupts(snapshot, clock, remaining, passes):
    owner, job = job_pair()
    g, ledger = graph(snapshot, job), owner.witnesses
    ledger.retain(ledger.reserve(members=100_000 - remaining))
    if passes:
        witnesses._member_witness(g, g.nodes, ledger, job)
        assert ledger._retained_members == 100_000 - remaining + 3
    else:
        with pytest.raises(_AnalysisAborted) as stopped:
            witnesses._member_witness(g, g.nodes, ledger, job)
        assert stopped.value.limit_id == 'WU9-L13'
        assert ledger._retained_members == 100_000 - remaining
        assert ledger._retained_witnesses == 0


@pytest.mark.parametrize('remaining,passes', ((3, True), (2, False)))
def test_path_quota_counts_edge_and_node_occurrences(snapshot, clock, remaining, passes):
    owner, job = job_pair()
    g, ledger = graph(snapshot, job), owner.witnesses
    path = traversal._shortest_path(g, g.nodes[0], g.nodes[1], job)
    assert len(path.nodes) == 2 and len(path.edges) == 1
    ledger.retain(ledger.reserve(members=100_000 - remaining))
    if passes:
        witnesses._path_witness(path, ledger, job)
        assert ledger._retained_members == 100_000
    else:
        with pytest.raises(_AnalysisAborted) as stopped:
            witnesses._path_witness(path, ledger, job)
        assert stopped.value.limit_id == 'WU9-L13'
        assert ledger._retained_members == 100_000 - remaining
        assert ledger._retained_witnesses == 0


def test_completed_search_is_required_before_an_absence_witness(snapshot, clock):
    owner, job = job_pair()
    g, ledger = graph(snapshot, job), owner.witnesses
    result = traversal._reachable(g, (g.nodes[0],), job)
    job.charge(1_000_000 - job.used)
    with pytest.raises(_AnalysisAborted) as stopped:
        witnesses._absence_witness(result, g.nodes[2], ledger, job)
    assert stopped.value.limit_id == 'WU9-L11'
    assert ledger._retained_witnesses == 0


def test_repeated_searches_charge_each_examination_and_do_not_reuse_free_results(snapshot, clock):
    owner, job = job_pair()
    g = graph(snapshot, job)
    before = job.used
    first = traversal._shortest_path(g, g.nodes[0], g.nodes[1], job)
    cost = job.used - before
    second = traversal._shortest_path(g, g.nodes[0], g.nodes[1], job)
    assert cost > 0 and job.used - before == cost * 2
    assert first is not second and first.edges == second.edges
    assert owner.used == 1025 + job.used


def test_projection_and_witness_do_not_open_locators_or_execute_source_text(clock, monkeypatch):
    value = CASES.pool()
    value['assertions'] = [CASES.relation('cites')]
    canary = 'FICTIONAL_GRAPH_CANARY__import__(os).system(command)'
    value['assertions'][0]['provenance']['method'] = canary
    CASES.by_id(value, 'artifact')['data']['locators'] = ['file:///FICTIONAL/' + canary, 'https://fictional.invalid/' + canary]
    prepared = _prepare_value(value)
    assert type(prepared) is _PreparedBundle
    owner, job = job_pair()
    ledger = owner.witnesses
    calls = []
    def forbidden(*args, **kwargs):
        calls.append('side_effect')
        raise AssertionError('graph_side_effect')
    with monkeypatch.context() as patch:
        for module, name in ((builtins, 'open'), (socket, 'socket'), (socket, 'getaddrinfo'),
                             (ctypes, 'CDLL'), (subprocess, 'Popen')):
            patch.setattr(module, name, forbidden)
        g = projections._project(prepared, context(), job)
        start = next(n for n in g.nodes if n.identifier == 'artifact')
        target = next(n for n in g.nodes if n.identifier == 'artifact2')
        path = traversal._shortest_path(g, start, target, job)
        assert path is not None
        witness = witnesses._path_witness(path, ledger, job)
    assert calls == [] and canary not in repr(witness)


def test_private_graph_primitives_offer_no_policy_or_io_options():
    for function in (projections._project, traversal._shortest_path, traversal._reachable,
                     witnesses._member_witness, witnesses._path_witness):
        parameters = inspect.signature(function).parameters
        assert not {'clock', 'quota', 'max_work', 'deadline', 'callback', 'fetch', 'path', 'options'} & (set(parameters) - {'path'})


def test_graph_snapshot_is_immutable_and_does_not_mutate_input(snapshot, clock):
    owner, job = job_pair()
    g = graph(snapshot, job)
    captured = snapshot.captured_tree
    with pytest.raises(FrozenInstanceError):
        g.edges = ()
    with pytest.raises(FrozenInstanceError):
        g.nodes[0].identifier = 'changed'
    traversal._reachable(g, (g.nodes[0],), job)
    assert snapshot.captured_tree is captured
