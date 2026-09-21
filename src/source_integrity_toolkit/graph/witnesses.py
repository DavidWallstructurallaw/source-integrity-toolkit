# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: GRAPH_VIEW_CONTRACT. Complete finite, invocation-counted witnesses.

Architecture 18.2/19: no clipping, no empty positive path in place of absence,
and no outside-world conclusion from an examined graph. Each populated payload
reference slot counts once, including repeated cycle endpoints and references
retained in more than one evidence slot. ``graph`` identifies the exact query
context; it is not another expansion of all graph members into this witness.

Only project-owned completed graph facts and the runtime-issued shared ledger
are accepted. The private identity checks prevent accidental cross-job or
cross-invocation reuse; they do not claim a hostile same-process sandbox.
"""
from dataclasses import dataclass

from ..contracts.bundle import _require
from ..contracts.execution import _byte_work
from ..validation.limits import _WitnessLedger
from ..validation.semantics import _analysis_port
from .projections import _GraphNode, _GraphEdge, _check_projection, _compare_key, _graph_sort
from .traversal import _Path, _Reachability, _node_index
from .cycles import _StrongComponent


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _GraphWitness:
    kind: str
    graph: object
    nodes: tuple = ()
    edges: tuple = ()
    members: tuple = ()
    internal_edges: tuple = ()
    exit_edges: tuple = ()
    starts: tuple = ()
    target: _GraphNode | None = None
    examined_nodes: tuple = ()
    examined_edges: tuple = ()
    frontiers: tuple = ()
    terminals: tuple = ()
    observations: tuple = ()
    member_count: int = 0


def _check_ledger(graph, ledger, port):
    _check_projection(graph, port)
    _require(type(ledger) is _WitnessLedger)
    port.charge(3)
    try:
        owner = port._owner
        _require(ledger.port._owner is owner and owner._witness_ledger is ledger)
    except AttributeError:
        raise TypeError('invalid_private_representation') from None
    ledger.port.check()


def _charge_node(node, port):
    _require(type(node) is _GraphNode)
    port.charge(4)
    for text in (node.collection, node.identifier, node.kind):
        _byte_work(port, 4 * len(text), 1)


def _charge_edge(edge, port):
    _require(type(edge) is _GraphEdge)
    port.charge(8)
    for text in edge.key:
        _byte_work(port, 4 * len(text), 1)
    for reason in edge.reason_codes:
        _byte_work(port, 4 * len(reason), 1)


def _edge_index(edges, edge, port):
    low, high = 0, len(edges)
    while low < high:
        port.charge(3)
        middle = (low + high) // 2
        compared = _compare_key(edges[middle].key, edge.key, port)
        if compared < 0:
            low = middle + 1
        elif compared > 0:
            high = middle
        else:
            return middle
    return -1


def _checked_nodes(graph, nodes, port, *, unique=True):
    _require(type(nodes) is tuple)
    indexed = _graph_sort(graph.nodes, port, key_kind='node')
    ordered = _graph_sort(nodes, port, key_kind='node')
    previous = None
    for node in ordered:
        _charge_node(node, port)
        index = _node_index(indexed, node, port)
        _require(index >= 0 and indexed[index] is node)
        if unique and previous is not None:
            _require(_compare_key(previous.key, node.key, port) < 0)
        previous = node
    return ordered


def _checked_edges(graph, edges, port):
    _require(type(edges) is tuple)
    indexed = _graph_sort(graph.edges, port, key_kind='edge')
    ordered = _graph_sort(edges, port, key_kind='edge')
    previous = None
    for edge in ordered:
        _charge_edge(edge, port)
        index = _edge_index(indexed, edge, port)
        _require(index >= 0 and indexed[index] is edge)
        if previous is not None:
            _require(_compare_key(previous.key, edge.key, port) < 0)
        previous = edge
    return ordered


def _check_path(path, port, *, cycle=False):
    _require(type(path) is _Path and type(path.nodes) is tuple and type(path.edges) is tuple)
    port.charge(4)
    _require(bool(path.nodes) and len(path.nodes) == len(path.edges) + 1)
    _require(path.nodes[0] is path.start and path.nodes[-1] is path.target)
    ordered = _checked_nodes(path.graph, path.nodes, port, unique=not cycle)
    if cycle:
        port.charge(3)
        _require(bool(path.edges) and path.start is path.target)
        previous, repeats = None, 0
        for node in ordered:
            port.charge(2)
            if node is previous:
                _require(node is path.start)
                repeats += 1
            previous = node
        _require(repeats == 1)
    _checked_edges(path.graph, path.edges, port)
    for i, edge in enumerate(path.edges):
        port.charge(3)
        _require(edge.source is path.nodes[i] and edge.target is path.nodes[i + 1])


def _commit(kind, graph, ledger, port, *, nodes=(), edges=(), members=(),
            internal_edges=(), exit_edges=(), starts=(), target=None,
            examined_nodes=(), examined_edges=(), frontiers=(), terminals=(), observations=()):
    # The finite fields are validated completed component facts. Count and
    # reserve the entire payload before allocating its retained wrapper.
    port.charge(15)
    member_count = (len(nodes) + len(edges) + len(members) + len(internal_edges) + len(exit_edges) +
                    len(starts) + (target is not None) + len(examined_nodes) + len(examined_edges) +
                    len(frontiers) + len(terminals) + len(observations))
    token = ledger.reserve(witnesses=1, members=member_count)
    port.charge(17)
    result = _GraphWitness(kind, graph, nodes, edges, members, internal_edges, exit_edges, starts, target,
                           examined_nodes, examined_edges, frontiers, terminals, observations, member_count)
    port.check()
    ledger.retain(token)
    port.check()
    return result


def _path_witness(path, ledger, port):
    _analysis_port(port)
    _require(type(path) is _Path)
    _check_ledger(path.graph, ledger, port)
    _check_path(path, port)
    return _commit('path', path.graph, ledger, port, nodes=path.nodes, edges=path.edges)


def _cycle_witness(component, ledger, port):
    _analysis_port(port)
    _require(type(component) is _StrongComponent)
    _check_ledger(component.graph, ledger, port)
    path = component.cycle
    _require(type(path) is _Path and path.graph is component.graph)
    _check_path(path, port, cycle=True)
    members = _checked_nodes(component.graph, component.members, port)
    internal = _checked_edges(component.graph, component.internal_edges, port)
    exits = _checked_edges(component.graph, component.exit_edges, port)
    port.charge(4)
    _require(bool(members) and bool(path.edges) and path.start is path.target and path.start is members[0])
    for edge in internal:
        port.charge(1)
        _require(_node_index(members, edge.source, port) >= 0 and _node_index(members, edge.target, port) >= 0)
    for edge in exits:
        port.charge(1)
        _require(_node_index(members, edge.source, port) >= 0 and _node_index(members, edge.target, port) < 0)
    for edge in path.edges:
        port.charge(1)
        index = _edge_index(internal, edge, port)
        _require(index >= 0 and internal[index] is edge)
    return _commit('cycle', component.graph, ledger, port, nodes=path.nodes, edges=path.edges,
                   members=members, internal_edges=internal, exit_edges=exits)


def _member_witness(graph, members, ledger, port):
    _check_ledger(graph, ledger, port)
    ordered = _checked_nodes(graph, members, port)
    return _commit('members', graph, ledger, port, members=ordered)


def _absence_witness(search, target, ledger, port):
    """Retain an executed finite search, not a global or covered-world absence.

    _Reachability is returned only by the completed traversal. Its private
    constructor is a trusted component precondition, not an execution proof.
    The graph context retains the actual view, predicates and scope; a domain
    owner must separately establish any stronger documentary coverage claim.
    """
    _analysis_port(port)
    _require(type(search) is _Reachability)
    _check_ledger(search.graph, ledger, port)
    _checked_nodes(search.graph, (target,), port)
    nodes = _checked_nodes(search.graph, search.nodes, port)
    _require(_node_index(nodes, target, port) < 0)
    starts = _checked_nodes(search.graph, search.starts, port)
    edges = _checked_edges(search.graph, search.edges, port)
    frontiers = _checked_nodes(search.graph, search.frontiers, port)
    terminals = _checked_nodes(search.graph, search.terminals, port)
    observations = _graph_sort(search.observations, port, key_kind='edge')
    port.charge(2 * len(starts) + 2 * len(frontiers) + len(terminals) + 2)
    for node in starts + frontiers + terminals:
        port.charge(1)
        _require(_node_index(nodes, node, port) >= 0)
    for edge in edges:
        port.charge(1)
        _require(_node_index(nodes, edge.source, port) >= 0 and _node_index(nodes, edge.target, port) >= 0)
    for observation in observations:
        _charge_edge(observation, port)
        _require(_node_index(nodes, observation.source, port) >= 0)
    return _commit('no_witness_in_examined_view', search.graph, ledger, port,
                   starts=starts, target=target, examined_nodes=nodes, examined_edges=edges,
                   frontiers=frontiers, terminals=terminals, observations=observations)
