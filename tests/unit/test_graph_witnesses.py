# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W04 finite witness evidence, independently derived from frozen sources.

Authority: architecture 18.2/19.2-19.3, governance 22.5, reporting
14.3/18.1/19.2 and PHASE_3_PLAN 3.2/3.4/9. Synthetic projections
isolate mechanics, without claiming admission, qualification or public report
execution. Quota controls use the actual W02 job and witness ledger.
"""
import importlib.util
from pathlib import Path

import pytest

from source_integrity_toolkit.contracts.evidence import _QualificationContext, _SourceAddress
from source_integrity_toolkit.contracts.execution import _AnalysisAborted
from source_integrity_toolkit.graph.cycles import _StrongComponent, _components
from source_integrity_toolkit.graph.projections import _GraphEdge, _GraphNode, _Projection
from source_integrity_toolkit.graph.traversal import _Path, _reachable, _shortest_path
from source_integrity_toolkit.graph.witnesses import (
    _absence_witness, _cycle_witness, _member_witness, _path_witness,
)
from source_integrity_toolkit.runtime import resources
from source_integrity_toolkit.runtime.boundary import _prepare_value
from source_integrity_toolkit.validation.limits import _WitnessLedger


_spec = importlib.util.spec_from_file_location(
    "sit_w04_witness_input", Path(__file__).parents[1] / "contract/test_typed_records.py")
_cases = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cases)


@pytest.fixture
def clock(monkeypatch):
    now = [100]
    monkeypatch.setattr(resources, "monotonic_ns", lambda: now[0])
    return now


@pytest.fixture
def prepared(clock):
    return _prepare_value(_cases.sparse())


def job():
    budget = resources._new_analysis_budget()
    budget.record_input_acceptance()  # Trusted component setup only.
    port = budget.start_job()
    return budget, port, budget.witnesses


def node(identifier, collection="records", kind="evidence_item"):
    return _GraphNode(collection, identifier, kind, (collection, identifier))


def edge(source, target, identifier, selector="", collection="assertions", eligible=True):
    address = _SourceAddress(collection, identifier, selector)
    key = (collection, identifier, selector, target.collection, target.identifier)
    return _GraphEdge(source, target, key, address,
                      "derived_from" if collection == "assertions" else None, eligible, ())


def graph(prepared, port, nodes, edges, observations=None, view="claim_origin", claim="claim"):
    context = _QualificationContext("inquiry", (claim,), (), "acquisition",
                                    "snapshot_structural", None, None,
                                    ("derived_from",), view)
    edges = tuple(edges)
    return _Projection(prepared, context, tuple(nodes), edges,
                       edges if observations is None else tuple(observations), (), None, port)


def counts(ledger):
    # Read-only test observation after stop never resumes a product operation.
    return (ledger._reserved_witnesses, ledger._reserved_members,
            ledger._retained_witnesses, ledger._retained_members)


def edge_ids(rows):
    return tuple(row.source_ref.record_id for row in rows)


@pytest.mark.parametrize("reverse", (False, True))
def test_path_witness_preserves_complete_prefix_choice_and_causal_order(prepared, reverse):
    budget, port, ledger = job()
    start, small, large, target = (node(name) for name in ("start", "a", "z", "target"))
    edges = (edge(start, large, "aa-first"), edge(large, target, "zz-last"),
             edge(start, small, "ab-first"), edge(small, target, "aa-last"))
    projection = graph(prepared, port, (target, large, small, start),
                       edges[::-1] if reverse else edges)
    path = _shortest_path(projection, start, target, port)
    before = (budget.used, port.used)
    witness = _path_witness(path, ledger, port)
    assert witness.graph is projection
    assert witness.kind == "path" and witness.member_count == 5
    assert witness.nodes == (start, large, target)
    assert edge_ids(witness.edges) == ("aa-first", "zz-last")
    assert counts(ledger) == (0, 0, 1, 5)
    assert budget.used - before[0] == port.used - before[1] > 0


def test_record_link_witness_keeps_canonical_selector_without_invented_assertion(prepared):
    _, port, ledger = job()
    start, target = node("evaluation", kind="evaluation"), node("target", kind="model")
    links = (edge(start, target, "evaluation", "data.role_bindings[role=judge].object_ref", "records"),
             edge(start, target, "evaluation", "data.role_bindings[role=candidate].object_ref", "records"))
    projection = graph(prepared, port, (target, start), links, view="model_evaluation")
    witness = _path_witness(_shortest_path(projection, start, target, port), ledger, port)
    assert witness.nodes == (start, target)
    assert tuple(row.key for row in witness.edges) == (
        ("records", "evaluation", "data.role_bindings[role=candidate].object_ref", "records", "target"),)
    assert witness.edges[0].source_ref.collection == "records" and witness.edges[0].predicate is None
    assert counts(ledger) == (0, 0, 1, 3)


def test_zero_edge_identity_path_is_one_node_witness_not_absence(prepared):
    _, port, ledger = job()
    start = node("start")
    projection = graph(prepared, port, (start,), ())
    witness = _path_witness(_shortest_path(projection, start, start, port), ledger, port)
    assert witness.kind == "path" and witness.member_count == 1
    assert witness.nodes == (start,) and witness.edges == ()
    assert counts(ledger) == (0, 0, 1, 1)


@pytest.mark.parametrize("reverse", (False, True))
def test_unordered_member_witness_keeps_every_distinct_typed_member(prepared, reverse):
    _, port, ledger = job()
    # This exceeds a tempting short-display limit without relying on rendering.
    members = tuple(node(f"member-{index:04}") for index in range(300))
    assertion = node("z-assertion", "assertions", "relation")
    reference = node("a-reference", "evidence_references", "record_pointer")
    required = (assertion, reference) + members
    supplied = required[::-1] if reverse else required
    projection = graph(prepared, port, supplied, ())
    witness = _member_witness(projection, supplied, ledger, port)
    assert witness.graph is projection
    assert witness.kind == "members" and witness.member_count == 302
    assert witness.members == required
    assert counts(ledger) == (0, 0, 1, 302)


def test_cycle_witness_retains_complete_component_and_exit_occurrences(prepared):
    _, port, ledger = job()
    a, b, c, origin = (node(name) for name in ("a", "b", "c", "origin"))
    edges = (edge(a, b, "ab"), edge(b, a, "ba"), edge(a, c, "ac"),
             edge(c, a, "ca"), edge(c, origin, "exit"))
    projection = graph(prepared, port, (origin, c, b, a), edges[::-1])
    component = _components(projection, port)[0]
    witness = _cycle_witness(component, ledger, port)
    assert witness.graph is projection
    assert witness.kind == "cycle" and witness.member_count == 13
    assert witness.nodes == (a, b, a)
    assert edge_ids(witness.edges) == ("ab", "ba")
    assert witness.members == (a, b, c)
    assert edge_ids(witness.internal_edges) == ("ab", "ac", "ba", "ca")
    assert edge_ids(witness.exit_edges) == ("exit",)
    # Three path-node occurrences + two path edges + all three component
    # members + four internal edges + one exit edge are all retained.
    assert counts(ledger) == (0, 0, 1, 13)


def test_single_node_cycle_counts_both_closed_endpoint_occurrences(prepared):
    _, port, ledger = job()
    a = node("a")
    loop = edge(a, a, "loop")
    projection = graph(prepared, port, (a,), (loop,))
    witness = _cycle_witness(_components(projection, port)[0], ledger, port)
    assert witness.nodes == (a, a) and witness.edges == (loop,)
    assert witness.members == (a,)
    assert counts(ledger) == (0, 0, 1, 5)


def test_closed_cycle_path_is_rejected_by_simple_path_factory_with_cycle_positive_control(prepared):
    _, port, ledger = job()
    a, b = node("a"), node("b")
    ab, ba = edge(a, b, "ab"), edge(b, a, "ba")
    projection = graph(prepared, port, (a, b), (ab, ba))
    (component,) = _components(projection, port)
    assert component.cycle.nodes == (a, b, a)
    with pytest.raises(TypeError):
        _path_witness(component.cycle, ledger, port)
    assert counts(ledger) == (0, 0, 0, 0)
    witness = _cycle_witness(component, ledger, port)
    assert witness.kind == "cycle" and witness.nodes == (a, b, a)
    assert witness.member_count == 9 and counts(ledger) == (0, 0, 1, 9)


def test_closed_walk_with_repeated_intermediate_anchor_is_not_a_cycle_witness(prepared):
    _, port, ledger = job()
    a, b, c = node("a"), node("b"), node("c")
    ab, ba = edge(a, b, "ab"), edge(b, a, "ba")
    ac, ca = edge(a, c, "ac"), edge(c, a, "ca")
    projection = graph(prepared, port, (a, b, c), (ab, ba, ac, ca))
    (component,) = _components(projection, port)
    # Constructor continuity is not proof of a simple cycle. This negative
    # private representation has four distinct edges but repeats anchor a
    # before closure, so it cannot replace the conforming component's cycle.
    walk = _Path(projection, a, a, (a, b, a, c, a), (ab, ba, ac, ca))
    invalid = _StrongComponent(projection, component.members, component.internal_edges,
                               component.exit_edges, walk)
    with pytest.raises(TypeError):
        _cycle_witness(invalid, ledger, port)
    assert counts(ledger) == (0, 0, 0, 0)
    witness = _cycle_witness(component, ledger, port)
    assert witness.nodes == (a, b, a) and witness.members == (a, b, c)
    assert witness.member_count == 12 and counts(ledger) == (0, 0, 1, 12)


def test_completed_absence_carries_exact_examined_scope_not_an_empty_positive_path(prepared):
    _, port, ledger = job()
    start, terminal, target = (node(name) for name in ("start", "terminal", "target"))
    link = edge(start, terminal, "visible")
    denial = edge(start, target, "denial", eligible=False)
    projection = graph(prepared, port, (target, terminal, start), (link,),
                       observations=(denial, link))
    reachability = _reachable(projection, (start,), port)
    witness = _absence_witness(reachability, target, ledger, port)
    assert witness.graph is projection and witness.graph.context is projection.context
    assert witness.kind == "no_witness_in_examined_view" and witness.member_count == 8
    assert witness.starts == (start,) and witness.nodes == witness.edges == ()
    assert witness.target == target
    assert witness.examined_nodes == (start, terminal)
    assert witness.examined_edges == (link,)
    assert witness.observations == (denial, link)
    assert witness.terminals == (terminal,)
    assert witness.frontiers == ()
    # start, target, two examined nodes, one edge, one terminal, two observations.
    assert counts(ledger) == (0, 0, 1, 8)


def test_unknown_endpoint_stays_in_absence_frontier_without_becoming_known_terminal(prepared):
    _, port, ledger = job()
    start, target = node("start"), node("target")
    missing = node("unknown", kind="unresolved_reference")
    link = edge(start, missing, "gap")
    projection = graph(prepared, port, (missing, target, start), (link,))
    witness = _absence_witness(_reachable(projection, (start,), port), target, ledger, port)
    assert witness.kind == "no_witness_in_examined_view"
    assert witness.frontiers == (missing,) and witness.terminals == ()
    assert witness.examined_nodes == (start, missing)
    assert witness.graph.context.claim_refs == ("claim",)
    assert witness.graph.context.graph_view == "claim_origin"
    assert witness.graph.context.dependency_dimension == "acquisition"
    assert witness.graph.context.relation_types == ("derived_from",)
    assert witness.member_count == 7 and counts(ledger) == (0, 0, 1, 7)


def test_layered_diamonds_retain_one_shortest_complete_path_without_walk_expansion(prepared):
    budget, port, ledger = job()
    start, target = node("start"), node("target")
    layers = tuple((node(f"n{level:02}a"), node(f"n{level:02}b")) for level in range(24))
    nodes = (start,) + tuple(item for layer in layers for item in layer) + (target,)
    edges = [edge(start, layers[0][choice], f"first-{choice}") for choice in range(2)]
    for level in range(23):
        edges.extend(edge(layers[level][source], layers[level + 1][dest],
                          f"step-{level:02}-{source}-{dest}")
                     for source in range(2) for dest in range(2))
    edges.extend(edge(layers[-1][choice], target, f"last-{choice}") for choice in range(2))
    projection = graph(prepared, port, nodes[::-1], tuple(edges)[::-1])
    witness = _path_witness(_shortest_path(projection, start, target, port), ledger, port)
    assert witness.nodes == (start,) + tuple(layer[0] for layer in layers) + (target,)
    assert edge_ids(witness.edges) == (("first-0",) +
        tuple(f"step-{level:02}-0-0" for level in range(23)) + ("last-0",))
    assert witness.member_count == 51 and counts(ledger) == (0, 0, 1, 51)
    assert 0 < port.used < 1_000_000 and budget.used == 1025 + port.used


def test_reachable_target_cannot_be_emitted_as_absence(prepared):
    _, port, ledger = job()
    a, b = node("a"), node("b")
    projection = graph(prepared, port, (a, b), (edge(a, b, "ab"),))
    completed = _reachable(projection, (a,), port)
    before = counts(ledger)
    with pytest.raises(TypeError):
        _absence_witness(completed, b, ledger, port)
    assert counts(ledger) == before == (0, 0, 0, 0)


def test_unfinished_search_cannot_supply_an_absence_or_consume_witness_capacity(prepared):
    budget, port, ledger = job()
    a, b, target = node("a"), node("b"), node("target")
    projection = graph(prepared, port, (a, b, target), (edge(a, b, "ab"),))
    port.charge(1_000_000 - port.used - 12)
    with pytest.raises(_AnalysisAborted) as stopped:
        _absence_witness(_reachable(projection, (a,), port), target, ledger, port)
    assert stopped.value.limit_id == "WU9-L11"
    assert stopped.value.stop.input_state == "accepted"
    assert counts(ledger) == (0, 0, 0, 0) and budget.used == 1025 + port.used


@pytest.mark.parametrize("remaining,expected", ((4, 99_999), (3, 100_000)))
def test_path_retention_below_and_at_member_ceiling_is_complete(prepared, remaining, expected):
    _, port, ledger = job()
    a, b = node("a"), node("b")
    projection = graph(prepared, port, (a, b), (edge(a, b, "ab"),))
    path = _shortest_path(projection, a, b, port)
    ledger.retain(ledger.reserve(members=100_000 - remaining))
    witness = _path_witness(path, ledger, port)
    assert witness.nodes == (a, b) and len(witness.edges) == 1
    assert counts(ledger) == (0, 0, 1, expected)


def test_excess_member_retention_interrupts_without_clipping_or_partial_commit(prepared):
    budget, port, ledger = job()
    a, b = node("a"), node("b")
    projection = graph(prepared, port, (a, b), (edge(a, b, "ab"),))
    path = _shortest_path(projection, a, b, port)
    ledger.retain(ledger.reserve(members=99_998))
    with pytest.raises(_AnalysisAborted) as stopped:
        _path_witness(path, ledger, port)
    assert stopped.value.limit_id == "WU9-L13"
    assert stopped.value.stop.input_state == "accepted"
    assert counts(ledger) == (0, 0, 0, 99_998)
    before = (budget.used, port.used)
    with pytest.raises(_AnalysisAborted) as repeat:
        _path_witness(path, ledger, port)
    assert repeat.value is stopped.value and (budget.used, port.used) == before


def test_witness_ceiling_keeps_last_complete_witness_and_stops_next(prepared):
    _, port, ledger = job()
    a, b = node("a"), node("b")
    projection = graph(prepared, port, (a, b), (edge(a, b, "ab"),))
    path = _shortest_path(projection, a, b, port)
    ledger.retain(ledger.reserve(witnesses=19_999))
    witness = _path_witness(path, ledger, port)
    assert witness.nodes == (a, b) and counts(ledger) == (0, 0, 20_000, 3)
    with pytest.raises(_AnalysisAborted) as stopped:
        _member_witness(projection, (a, b), ledger, port)
    assert stopped.value.limit_id == "WU9-L13"
    assert counts(ledger) == (0, 0, 20_000, 3)
    assert witness.nodes == (a, b)


def test_cycle_cannot_drop_component_evidence_to_fit_a_representative_only_budget(prepared):
    _, port, ledger = job()
    a, b, c, origin = (node(name) for name in ("a", "b", "c", "origin"))
    edges = (edge(a, b, "ab"), edge(b, a, "ba"), edge(a, c, "ac"),
             edge(c, a, "ca"), edge(c, origin, "exit"))
    projection = graph(prepared, port, (a, b, c, origin), edges)
    component = _components(projection, port)[0]
    ledger.retain(ledger.reserve(members=99_995))
    # Five slots fit the representative alone; all thirteen are required.
    with pytest.raises(_AnalysisAborted) as stopped:
        _cycle_witness(component, ledger, port)
    assert stopped.value.limit_id == "WU9-L13"
    assert counts(ledger) == (0, 0, 0, 99_995)


def test_ledger_from_different_invocation_cannot_authorize_retention(prepared):
    _, port, ledger = job()
    other_budget, other_port, other_ledger = job()
    a, b = node("a"), node("b")
    projection = graph(prepared, port, (a, b), (edge(a, b, "ab"),))
    path = _shortest_path(projection, a, b, port)
    with pytest.raises(TypeError):
        _path_witness(path, other_ledger, port)
    assert counts(ledger) == counts(other_ledger) == (0, 0, 0, 0)
    assert other_budget.input_state == "accepted" and other_port.used >= 5


def test_second_ledger_with_same_owner_cannot_reset_retained_capacity(prepared):
    _, port, ledger = job()
    a, b = node("a"), node("b")
    projection = graph(prepared, port, (a, b), (edge(a, b, "ab"),))
    path = _shortest_path(projection, a, b, port)
    replacement = _WitnessLedger(ledger.port)
    with pytest.raises(TypeError):
        _path_witness(path, replacement, port)
    assert counts(ledger) == counts(replacement) == (0, 0, 0, 0)


def test_result_cannot_be_reused_for_free_in_later_job(prepared):
    budget, first, ledger = job()
    a, b = node("a"), node("b")
    projection = graph(prepared, first, (a, b), (edge(a, b, "ab"),))
    path = _shortest_path(projection, a, b, first)
    budget.finish_job(first)
    second = budget.start_job()
    with pytest.raises(TypeError):
        _path_witness(path, ledger, second)
    assert counts(ledger) == (0, 0, 0, 0)


def test_per_job_work_stop_during_retention_never_returns_a_partial_witness(prepared):
    budget, port, ledger = job()
    members = tuple(node(f"member-{index:03}") for index in range(120))
    projection = graph(prepared, port, members, ())
    port.charge(1_000_000 - port.used - 25)
    with pytest.raises(_AnalysisAborted) as stopped:
        _member_witness(projection, members, ledger, port)
    assert stopped.value.limit_id == "WU9-L11"
    assert stopped.value.stop.input_state == "accepted"
    assert ledger._retained_witnesses == ledger._retained_members == 0
    assert budget.used == 1025 + port.used
