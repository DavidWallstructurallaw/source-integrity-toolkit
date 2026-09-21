# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: GRAPH_VIEW_CONTRACT. Paid finite SCCs and representative cycles.

Architecture 18.2/19 and Governance 22.5: complete components are separate
from their smallest-node, shortest-cycle representative. Exits remain visible.
The iterative passes never enumerate walks or recurse with source depth.
Private inputs are project-owned, admitted projections for the current job;
these mechanical graph facts establish no origin or documentary conclusion.
"""
from dataclasses import dataclass

from ..contracts.bundle import _require
from .projections import _check_projection, _compare_key, _graph_sort
from .traversal import _Path, _ranked_search, _path_from_search, _node_index


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _StrongComponent:
    graph: object
    members: tuple
    internal_edges: tuple
    exit_edges: tuple
    cycle: _Path | None


def _canonical_cycle(graph, members, internal_edges, port):
    """One ranked distance pass, then compare complete prefixes and closing edges."""
    port.charge(2)
    anchor = members[0]
    search = _ranked_search(graph, anchor, port, allowed_nodes=members)
    best, best_length, best_rank = None, 0, 0
    for edge in internal_edges:
        port.charge(2)
        if _compare_key(edge.target.key, anchor.key, port) != 0:
            continue
        index = _node_index(search.nodes, edge.source, port)
        _require(index >= 0)
        port.charge(4)
        distance, rank = search.distances[index], search.ranks[index]
        if distance < 0:
            continue
        length = distance + 1
        if (best is None or length < best_length or
                (length == best_length and (rank < best_rank or
                 (rank == best_rank and _compare_key(edge.key, best.key, port) < 0)))):
            port.charge(3)
            best, best_length, best_rank = edge, length, rank
    _require(best is not None)
    prefix = _path_from_search(search, best.source, port)
    _require(prefix is not None)
    # Both tuple copies and the Path constructor's repeated type/continuity
    # passes are new work, independent of the already paid prefix search.
    port.charge(6 * (len(prefix.nodes) + len(prefix.edges)) + 27)
    nodes, edges = prefix.nodes + (anchor,), prefix.edges + (best,)
    result = _Path(graph, anchor, anchor, nodes, edges)
    port.check()
    return result


def _components(graph, port):
    """Return every SCC in smallest-typed-member order, including isolated nodes.

    ``internal_edges`` and ``exit_edges`` retain every eligible occurrence in
    their own canonical order. Unknown endpoints are frontiers, never bridges
    traversed during either SCC pass. Noneligible assertions remain separately
    accessible through the exact projection's observations and annotations.
    """
    _check_projection(graph, port)
    nodes = _graph_sort(graph.nodes, port, key_kind='node')
    edges = _graph_sort(graph.edges, port, key_kind='edge')
    for i in range(1, len(nodes)):
        port.charge(2)
        _require(_compare_key(nodes[i - 1].key, nodes[i].key, port) < 0)
    for i in range(1, len(edges)):
        port.charge(2)
        _require(_compare_key(edges[i - 1].key, edges[i].key, port) < 0)
    port.charge(4 * len(nodes) + 3)
    outgoing = [[] for _ in nodes]
    incoming = [[] for _ in nodes]
    endpoints = []
    for edge in edges:
        port.charge(3)
        source = _node_index(nodes, edge.source, port)
        target = _node_index(nodes, edge.target, port)
        _require(source >= 0 and target >= 0)
        _require(nodes[source] is edge.source and nodes[target] is edge.target)
        port.charge(4)
        endpoints.append((source, target, edge))
        if nodes[source].kind == 'unresolved_reference' or nodes[target].kind == 'unresolved_reference':
            continue
        port.charge(2)
        outgoing[source].append(target)
        incoming[target].append(source)

    # Kosaraju's finishing pass with explicit frames, including isolated nodes.
    port.charge(len(nodes) + 2)
    seen, finish = [False] * len(nodes), []
    for root in range(len(nodes)):
        port.charge(1)
        if seen[root]:
            continue
        port.charge(4)
        seen[root] = True
        stack = [(root, 0)]
        while stack:
            port.charge(3)
            node, cursor = stack[-1]
            if cursor == len(outgoing[node]):
                port.charge(2)
                stack.pop()
                finish.append(node)
                continue
            port.charge(4)
            target = outgoing[node][cursor]
            stack[-1] = (node, cursor + 1)
            if not seen[target]:
                port.charge(3)
                seen[target] = True
                stack.append((target, 0))

    # Reverse-pass indices are local paid array coordinates, not input hashes.
    port.charge(len(nodes) + 2)
    assigned, groups = [-1] * len(nodes), []
    for position in range(len(finish) - 1, -1, -1):
        port.charge(2)
        root = finish[position]
        if assigned[root] >= 0:
            continue
        port.charge(5)
        group_id = len(groups)
        assigned[root] = group_id
        stack, members = [root], []
        while stack:
            port.charge(3)
            node = stack.pop()
            members.append(nodes[node])
            for source in incoming[node]:
                port.charge(2)
                if assigned[source] < 0:
                    port.charge(2)
                    assigned[source] = group_id
                    stack.append(source)
        port.charge(len(members) + 2)
        groups.append(_graph_sort(tuple(members), port, key_kind='node'))

    port.charge(4 * len(groups) + len(nodes) + 4)
    internal = [[] for _ in groups]
    exits = [[] for _ in groups]
    ordered = [None] * len(nodes)
    for source, target, edge in endpoints:
        port.charge(4)
        left, right = assigned[source], assigned[target]
        if left == right:
            internal[left].append(edge)
        else:
            exits[left].append(edge)
    for group_id, members in enumerate(groups):
        port.charge(3)
        cyclic = len(members) > 1
        if not cyclic and members[0].kind != 'unresolved_reference':
            for edge in internal[group_id]:
                port.charge(1)
                if _compare_key(edge.source.key, edge.target.key, port) == 0:
                    cyclic = True
        port.charge(len(internal[group_id]) + len(exits[group_id]) + 3)
        member_edges, exit_edges = tuple(internal[group_id]), tuple(exits[group_id])
        cycle = _canonical_cycle(graph, members, member_edges, port) if cyclic else None
        first = _node_index(nodes, members[0], port)
        port.charge(7)
        ordered[first] = _StrongComponent(graph, members, member_edges, exit_edges, cycle)
    result = []
    for component in ordered:
        port.charge(1)
        if component is not None:
            port.charge(1)
            result.append(component)
    port.charge(len(result) + 1)
    completed = tuple(result)
    port.check()
    return completed
