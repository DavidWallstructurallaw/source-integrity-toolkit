# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W04 SCC mechanics against frozen, independently specified graph oracles.

Authority: PHASE_3_PLAN 3.2/3.4/9; architecture 18.2/19; governance
22.5; lineage 10.1-10.7; reporting W4-15 and 18.1. Synthetic private
projections isolate mechanics. Their construction is not admission, a PC04
certificate, origin resolution, an independence result or a W13 audit run.
"""
import importlib.util
from pathlib import Path

import pytest

from source_integrity_toolkit.contracts.evidence import _QualificationContext, _SourceAddress
from source_integrity_toolkit.contracts.execution import _AnalysisAborted
from source_integrity_toolkit.graph.cycles import _components
from source_integrity_toolkit.graph.projections import _GraphEdge, _GraphNode, _Projection
from source_integrity_toolkit.runtime import resources
from source_integrity_toolkit.runtime.boundary import _prepare_value


_spec = importlib.util.spec_from_file_location(
    "sit_w04_cycle_input", Path(__file__).parents[1] / "contract/test_typed_records.py")
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
    return budget, budget.start_job()


def node(identifier, collection="records", kind="evidence_item"):
    return _GraphNode(collection, identifier, kind, (collection, identifier))


def edge(source, target, identifier, selector="", collection="assertions"):
    address = _SourceAddress(collection, identifier, selector)
    key = (collection, identifier, selector, target.collection, target.identifier)
    return _GraphEdge(source, target, key, address, "derived_from", True, ())


def graph(prepared, port, nodes, edges, view="claim_origin", observations=None):
    context = _QualificationContext("inquiry", ("claim",), (), "acquisition",
                                    "snapshot_structural", None, None,
                                    ("derived_from",), view)
    edges = tuple(edges)
    return _Projection(prepared, context, tuple(nodes), edges,
                       edges if observations is None else tuple(observations), (), None, port)


def member_keys(component):
    return tuple(row.key for row in component.members)


def edge_ids(rows):
    return tuple(row.source_ref.record_id for row in rows)


def test_empty_and_acyclic_graphs_have_complete_singleton_components(prepared):
    _, port = job()
    assert _components(graph(prepared, port, (), ()), port) == ()
    a, b, c, isolated = (node(name) for name in ("a", "b", "c", "isolated"))
    ab, bc = edge(a, b, "ab"), edge(b, c, "bc")
    projection = graph(prepared, port, (isolated, c, a, b), (bc, ab))
    rows = _components(projection, port)
    assert tuple(member_keys(row) for row in rows) == (
        (("records", "a"),), (("records", "b"),),
        (("records", "c"),), (("records", "isolated"),))
    assert all(row.graph is projection and row.cycle is None for row in rows)
    assert tuple(edge_ids(row.exit_edges) for row in rows) == (("ab",), ("bc",), (), ())
    assert all(row.internal_edges == () for row in rows)


@pytest.mark.parametrize("reverse", (False, True))
def test_self_loop_is_one_edge_cycle_and_keeps_parallel_assertion_identities(prepared, reverse):
    _, port = job()
    a = node("a")
    loops = (edge(a, a, "z-loop"), edge(a, a, "a-loop"))
    projection = graph(prepared, port, (a,), loops[::-1] if reverse else loops)
    (component,) = _components(projection, port)
    assert member_keys(component) == (("records", "a"),)
    assert edge_ids(component.internal_edges) == ("a-loop", "z-loop")
    assert component.exit_edges == ()
    assert component.cycle.graph is projection
    assert component.cycle.start == component.cycle.target == a
    assert component.cycle.nodes == (a, a)
    assert edge_ids(component.cycle.edges) == ("a-loop",)


def test_cycle_must_pass_through_component_minimum_even_if_other_node_has_self_loop(prepared):
    _, port = job()
    a, b, c = (node(name) for name in ("a", "b", "c"))
    edges = (edge(a, b, "ab"), edge(b, c, "bc"), edge(c, a, "ca"), edge(c, c, "cc"))
    (component,) = _components(graph(prepared, port, (c, a, b), edges), port)
    assert component.cycle.nodes == (a, b, c, a)
    assert edge_ids(component.cycle.edges) == ("ab", "bc", "ca")
    assert edge_ids(component.internal_edges) == ("ab", "bc", "ca", "cc")


def test_minimum_node_uses_typed_collection_identity_before_local_identifier(prepared):
    _, port = job()
    assertion = node("z-assertion", "assertions", "relation")
    reference = node("a-reference", "evidence_references", "record_pointer")
    forward = edge(assertion, reference, "z-assertion", "provenance.evidence_ref_ids")
    back = edge(reference, assertion, "a-reference", "record_ref", "evidence_references")
    (component,) = _components(graph(prepared, port, (reference, assertion), (back, forward),
                                    view="assertion_assurance"), port)
    assert member_keys(component) == (("assertions", "z-assertion"),
                                      ("evidence_references", "a-reference"))
    assert component.cycle.nodes == (assertion, reference, assertion)


@pytest.mark.parametrize("order", ((0, 1, 2, 3), (3, 2, 1, 0), (2, 0, 3, 1)))
def test_complete_edge_prefix_wins_over_smaller_last_predecessor(prepared, order):
    _, port = job()
    a, b, z = (node(name) for name in ("a", "b", "z"))
    # Both cycles have two edges. The aa prefix wins despite predecessor z.
    edges = (edge(a, z, "aa-first"), edge(z, a, "zz-last"),
             edge(a, b, "ab-first"), edge(b, a, "aa-last"))
    (component,) = _components(graph(prepared, port, (z, b, a),
                                    tuple(edges[index] for index in order)), port)
    assert component.cycle.nodes == (a, z, a)
    assert edge_ids(component.cycle.edges) == ("aa-first", "zz-last")
    assert len(component.internal_edges) == 4


def test_shortest_cycle_precedes_lexically_smaller_longer_cycle(prepared):
    _, port = job()
    a, b, c, d = (node(name) for name in ("a", "b", "c", "d"))
    edges = (edge(a, b, "a-long"), edge(b, c, "bc"), edge(c, a, "ca"),
             edge(a, d, "z-short"), edge(d, a, "da"))
    (component,) = _components(graph(prepared, port, (a, b, c, d), edges), port)
    assert component.cycle.nodes == (a, d, a)
    assert edge_ids(component.cycle.edges) == ("z-short", "da")


def test_all_component_members_internal_edges_and_exits_survive_representative_selection(prepared):
    _, port = job()
    a, b, c, d, origin = (node(name) for name in ("a", "b", "c", "d", "origin"))
    edges = (edge(a, b, "ab"), edge(b, a, "ba"), edge(a, c, "ac"), edge(c, a, "ca"),
             edge(b, c, "bc"), edge(c, b, "cb"), edge(b, origin, "bo"),
             edge(c, d, "cd"), edge(d, d, "dd"))
    projection = graph(prepared, port, (origin, d, c, b, a), edges[::-1])
    first, second, third = _components(projection, port)
    assert member_keys(first) == (("records", "a"), ("records", "b"), ("records", "c"))
    assert edge_ids(first.internal_edges) == ("ab", "ac", "ba", "bc", "ca", "cb")
    assert edge_ids(first.exit_edges) == ("bo", "cd")
    assert first.cycle.nodes == (a, b, a)
    assert member_keys(second) == (("records", "d"),) and second.cycle.nodes == (d, d)
    assert member_keys(third) == (("records", "origin"),) and third.cycle is None
    assert len(projection.edges) == 9


def test_unknown_endpoint_does_not_supply_a_bridge_that_closes_a_known_cycle(prepared):
    _, port = job()
    a, unknown = node("a"), node("unknown", kind="unresolved_reference")
    to_gap, from_gap = edge(a, unknown, "to-gap"), edge(unknown, a, "from-gap")
    projection = graph(prepared, port, (unknown, a), (from_gap, to_gap))
    known, missing = _components(projection, port)
    assert known.members == (a,) and missing.members == (unknown,)
    assert known.cycle is missing.cycle is None
    assert known.exit_edges == (to_gap,) and missing.exit_edges == (from_gap,)
    assert len(projection.observations) == 2


def test_dense_component_is_finite_and_does_not_enumerate_all_cycles(prepared):
    budget, port = job()
    nodes = tuple(node(f"n{index:02}") for index in range(14))
    edges = tuple(edge(left, right, f"e{i:02}-{j:02}")
                  for i, left in enumerate(nodes) for j, right in enumerate(nodes) if i != j)
    (component,) = _components(graph(prepared, port, nodes[::-1], edges[::-1]), port)
    assert component.members == nodes
    assert len(component.internal_edges) == 14 * 13 and component.exit_edges == ()
    assert component.cycle.nodes == (nodes[0], nodes[1], nodes[0])
    assert edge_ids(component.cycle.edges) == ("e00-01", "e01-00")
    assert 0 < port.used < 1_000_000 and budget.used == 1025 + port.used


def test_completed_long_cycle_keeps_every_member_and_edge(prepared):
    budget, port = job()
    nodes = tuple(node(f"n{index:04}") for index in range(128))
    edges = tuple(edge(nodes[index], nodes[(index + 1) % len(nodes)], f"e{index:04}")
                  for index in range(len(nodes)))
    (component,) = _components(graph(prepared, port, nodes, edges), port)
    assert component.members == nodes and component.internal_edges == edges
    assert component.cycle.nodes == nodes + (nodes[0],)
    assert component.cycle.edges == edges and component.exit_edges == ()
    assert 0 < port.used < 1_000_000 and budget.used == 1025 + port.used


def test_deep_cycle_obeys_real_job_stop_instead_of_recursion_or_partial_components(prepared):
    budget, port = job()
    nodes = tuple(node(f"n{index:04}") for index in range(1100))
    edges = tuple(edge(nodes[index], nodes[(index + 1) % len(nodes)], f"e{index:04}")
                  for index in range(len(nodes)))
    projection = graph(prepared, port, nodes, edges)
    with pytest.raises(_AnalysisAborted) as stopped:
        _components(projection, port)
    assert stopped.value.limit_id == "WU9-L11"
    assert stopped.value.stop.input_state == "accepted"
    assert stopped.value.stop.execution_state == "interrupted"
    assert 0 < port.used <= 1_000_000 and budget.used == 1025 + port.used
    # No catch-and-empty fallback, recurrence failure or uncharged retry.
    with pytest.raises(_AnalysisAborted) as repeated:
        _components(projection, port)
    assert repeated.value is stopped.value


def test_interrupted_component_search_cannot_return_complete_or_empty_components(prepared):
    budget, port = job()
    a, b = node("a"), node("b")
    projection = graph(prepared, port, (a, b), (edge(a, b, "ab"), edge(b, a, "ba")))
    port.charge(999_990)
    with pytest.raises(_AnalysisAborted) as stopped:
        _components(projection, port)
    assert stopped.value.limit_id == "WU9-L11"
    assert stopped.value.stop.input_state == "accepted"
    charged = (budget.used, port.used)
    with pytest.raises(_AnalysisAborted) as repeat:
        _components(projection, port)
    assert repeat.value is stopped.value and (budget.used, port.used) == charged
