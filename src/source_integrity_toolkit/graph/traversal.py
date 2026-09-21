# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: GRAPH_VIEW_CONTRACT. Paid finite directed graph mechanics.

Architecture sections 18.2,19 and governance 22.5: distance first, then ranks
of complete edge-key prefixes. Separate complete reachability retains every
examined branch and source observation. An unresolved endpoint is terminal,
not a hidden origin. Inputs are project-owned projections of the current job.
"""
from dataclasses import dataclass
from ..contracts.bundle import _require
from .projections import (
    _GraphNode, _GraphEdge, _Projection, _check_projection, _compare_key, _graph_sort,
)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Path:
    """Mechanical path; a cycle may explicitly repeat its start.

    The creating owner prepays visits/comparisons over these frozen parts.
    This is no public witness, documentary qualification or outside-world claim.
    """
    graph: _Projection
    start: _GraphNode
    target: _GraphNode
    nodes: tuple
    edges: tuple

    def __post_init__(self):
        _require(type(self.graph) is _Projection)
        _require(type(self.start) is _GraphNode and type(self.target) is _GraphNode)
        _require(type(self.nodes) is tuple and type(self.edges) is tuple)
        _require(len(self.nodes) == len(self.edges) + 1)
        _require(all(type(node) is _GraphNode for node in self.nodes))
        _require(all(type(edge) is _GraphEdge for edge in self.edges))
        _require(self.nodes[0] is self.start and self.nodes[-1] is self.target)
        for index, edge in enumerate(self.edges):
            _require(edge.source is self.nodes[index] and edge.target is self.nodes[index + 1])


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _RankedSearch:
    """Finished distance/prefix pass; -1 marks unreachable distance and rank.

    Aligned predecessor entries are edges, or None at the start/unreachable
    nodes. The graph binding confines reuse to the same current job.
    """
    graph: _Projection
    nodes: tuple
    distances: tuple
    ranks: tuple
    predecessors: tuple
    start_index: int

    def __post_init__(self):
        _require(type(self.graph) is _Projection)
        for values in (self.nodes, self.distances, self.ranks, self.predecessors):
            _require(type(values) is tuple)
        _require(len(self.nodes) == len(self.distances) == len(self.ranks) == len(self.predecessors))
        _require(all(type(node) is _GraphNode for node in self.nodes))
        _require(all(type(value) is int and value >= -1 for value in self.distances))
        _require(all(type(value) is int and value >= -1 for value in self.ranks))
        _require(all(edge is None or type(edge) is _GraphEdge for edge in self.predecessors))
        _require(type(self.start_index) is int and 0 <= self.start_index < len(self.nodes))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Reachability:
    """Complete reachable-area scan, independent of a representative path.

    frontiers are reached unknown nodes; terminals are reached known nodes
    without eligible outgoing edges. Neither category qualifies an origin.
    observations retains negative/inactive/conflicted source edges as supplied.
    """
    graph: _Projection
    starts: tuple
    nodes: tuple
    edges: tuple
    frontiers: tuple
    terminals: tuple
    observations: tuple

    def __post_init__(self):
        _require(type(self.graph) is _Projection)
        for rows in (self.starts, self.nodes, self.frontiers, self.terminals):
            _require(type(rows) is tuple and all(type(node) is _GraphNode for node in rows))
        for rows in (self.edges, self.observations):
            _require(type(rows) is tuple and all(type(edge) is _GraphEdge for edge in rows))


def _node_index(nodes, node, port):
    """Paid binary lookup in the mechanically ordered typed node table."""
    port.check_analysis()
    port.charge(4)
    _require(type(nodes) is tuple and type(node) is _GraphNode)
    low, high = 0, len(nodes)
    while low < high:
        port.charge(5)
        middle = (low + high) // 2
        comparison = _compare_key(nodes[middle].key, node.key, port)
        if comparison < 0:
            low = middle + 1
        else:
            high = middle
    port.charge(2)
    if low < len(nodes) and _compare_key(nodes[low].key, node.key, port) == 0:
        _require(_compare_key((nodes[low].kind,), (node.kind,), port) == 0)
        port.check()
        return low
    port.check()
    return -1


def _indexed(graph, port):
    """Fresh paid adjacency; no source merge or cross-job semantic cache."""
    _check_projection(graph, port)
    nodes = _graph_sort(graph.nodes, port, 'node')
    edges = _graph_sort(graph.edges, port)
    port.charge(3 * len(nodes) + 4 * len(edges) + 16)
    outgoing, incoming, sources, targets = [], [], [], []
    previous = None
    for node in nodes:
        port.charge(4)
        if previous is not None:
            _require(_compare_key(previous.key, node.key, port) < 0)
        outgoing.append([])
        incoming.append([])
        previous = node
    previous_edge = None
    for index, edge in enumerate(edges):
        port.charge(10)
        if previous_edge is not None:
            _require(_compare_key(previous_edge.key, edge.key, port) < 0)
        source = _node_index(nodes, edge.source, port)
        target = _node_index(nodes, edge.target, port)
        _require(source >= 0 and target >= 0)
        sources.append(source)
        targets.append(target)
        outgoing[source].append(index)
        incoming[target].append(index)
        previous_edge = edge
    port.check()
    return nodes, edges, sources, targets, outgoing, incoming


def _rank_compare(left, right, port):
    # Equal-distance predecessor ranks summarize COMPLETE earlier prefixes.
    port.charge(5)
    if left[0] != right[0]:
        return -1 if left[0] < right[0] else 1
    return _compare_key(left[1].key, right[1].key, port)


def _rank_sort(rows, port):
    """Stable bottom-up merge; each compare and moved entry is charged."""
    port.charge(len(rows) + 3)
    current = list(rows)
    width = 1
    while width < len(current):
        port.charge(len(current) + 3)
        merged = [None] * len(current)
        for start in range(0, len(current), 2 * width):
            port.charge(10)
            middle, stop = min(start + width, len(current)), min(start + 2 * width, len(current))
            left, right, output = start, middle, start
            while left < middle or right < stop:
                port.charge(6)
                if right == stop or (left < middle and _rank_compare(current[left], current[right], port) <= 0):
                    merged[output] = current[left]
                    left += 1
                else:
                    merged[output] = current[right]
                    right += 1
                output += 1
        current = merged
        width *= 2
    port.check()
    return current


def _ranked_search(graph, start, port, *, allowed_nodes=None):
    """BFS distances followed by complete-prefix ranking per distance layer.

    No complete paths are copied while ranking, and no walks are enumerated.
    The finite restriction supports the SCC owner's anchored cycle search.
    """
    _check_projection(graph, port)
    nodes, edges, sources, targets, outgoing, incoming = _indexed(graph, port)
    start_index = _node_index(nodes, start, port)
    _require(start_index >= 0)
    port.charge(5 * len(nodes) + 14)
    distances, ranks, predecessors = [-1] * len(nodes), [-1] * len(nodes), [None] * len(nodes)
    allowed = [allowed_nodes is None] * len(nodes)
    if allowed_nodes is not None:
        _require(type(allowed_nodes) is tuple)
        for node in allowed_nodes:
            port.charge(3)
            index = _node_index(nodes, node, port)
            _require(index >= 0 and not allowed[index])
            allowed[index] = True
    _require(allowed[start_index])
    distances[start_index] = ranks[start_index] = 0
    layers = [[start_index]]
    frontier, depth = layers[0], 0
    while frontier:
        port.charge(4)
        next_layer = []
        for source in frontier:
            port.charge(3)
            if nodes[source].kind == 'unresolved_reference':
                continue
            for edge_index in outgoing[source]:
                port.charge(8)
                target = targets[edge_index]
                if allowed[target] and distances[target] < 0:
                    distances[target] = depth + 1
                    next_layer.append(target)
        port.charge(4)
        if next_layer:
            layers.append(next_layer)
        frontier = next_layer
        depth += 1
    # A node's best parent uses the full predecessor prefix rank, not the
    # local parent ID or last edge. Ranking examines each incoming edge once.
    depth = 1
    while depth < len(layers):
        port.charge(4)
        rows = []
        for target in layers[depth]:
            port.charge(4)
            best = None
            for edge_index in incoming[target]:
                port.charge(8)
                source = sources[edge_index]
                if distances[source] != depth - 1 or nodes[source].kind == 'unresolved_reference':
                    continue
                port.charge(4)
                candidate = (ranks[source], edges[edge_index], target)
                if best is None or _rank_compare(candidate, best, port) < 0:
                    best = candidate
            _require(best is not None)
            port.charge(3)
            predecessors[target] = best[1]
            rows.append(best)
        ordered = _rank_sort(rows, port)
        for rank, row in enumerate(ordered):
            port.charge(3)
            ranks[row[2]] = rank
        depth += 1
    # Three copied tables plus four constructor validation passes.
    port.charge(7 * len(nodes) + 24)
    result = _RankedSearch(graph, nodes, tuple(distances), tuple(ranks), tuple(predecessors), start_index)
    port.check()
    return result


def _path_from_search(search, target, port):
    """Reconstruct just the selected path after the complete ranked pass."""
    port.check_analysis()
    port.charge(3)
    _require(type(search) is _RankedSearch)
    _check_projection(search.graph, port)
    target_index = _node_index(search.nodes, target, port)
    _require(target_index >= 0)
    port.charge(4)
    if search.distances[target_index] < 0:
        port.check()
        return None
    current = target_index
    reverse_nodes, reverse_edges = [], []
    while current != search.start_index:
        port.charge(8)
        reverse_nodes.append(search.nodes[current])
        edge = search.predecessors[current]
        _require(type(edge) is _GraphEdge)
        reverse_edges.append(edge)
        previous = _node_index(search.nodes, edge.source, port)
        _require(previous >= 0 and search.distances[previous] == search.distances[current] - 1)
        current = previous
    port.charge(3)
    reverse_nodes.append(search.nodes[search.start_index])
    # Copies, reversal, constructor visits and bounded key comparisons are
    # prepaid before the immutable path is made visible.
    port.charge(6 * len(reverse_nodes) + 6 * len(reverse_edges) + 15)
    path_nodes = tuple(reversed(reverse_nodes))
    path_edges = tuple(reversed(reverse_edges))
    for index, edge in enumerate(path_edges):
        port.charge(2)
        _compare_key(edge.source.key, path_nodes[index].key, port)
        _compare_key(edge.target.key, path_nodes[index + 1].key, port)
    port.check()
    result = _Path(search.graph, path_nodes[0], path_nodes[-1], path_nodes, path_edges)
    port.check()
    return result


def _shortest_path(graph, start, target, port, *, allowed_nodes=None):
    """Shortest eligible simple path in this exact projection, or None.

    The self path has zero edges, distinct from the cycle query. None follows
    a completed search only, never a budget/time/cancellation exception.
    """
    search = _ranked_search(graph, start, port, allowed_nodes=allowed_nodes)
    return _path_from_search(search, target, port)


def _reachable(graph, starts, port):
    """Inspect every eligible reachable branch and its source observations."""
    _check_projection(graph, port)
    _require(type(starts) is tuple)
    nodes, edges, sources, targets, outgoing, incoming = _indexed(graph, port)
    port.charge(3 * len(nodes) + 12)
    visited, selected, queue = [False] * len(nodes), [False] * len(nodes), []
    for node in starts:
        port.charge(5)
        index = _node_index(nodes, node, port)
        _require(index >= 0 and not selected[index])
        selected[index] = visited[index] = True
        queue.append(index)
    cursor = 0
    while cursor < len(queue):
        port.charge(5)
        source = queue[cursor]
        cursor += 1
        if nodes[source].kind == 'unresolved_reference':
            continue
        for edge_index in outgoing[source]:
            port.charge(6)
            target = targets[edge_index]
            if not visited[target]:
                visited[target] = True
                queue.append(target)
    port.charge(6)
    found, initial, frontiers, terminals, examined, observations = [], [], [], [], [], []
    for index, node in enumerate(nodes):
        port.charge(6)
        if selected[index]:
            initial.append(node)
        if visited[index]:
            found.append(node)
            if node.kind == 'unresolved_reference':
                frontiers.append(node)
            elif not outgoing[index]:
                terminals.append(node)
    for index, edge in enumerate(edges):
        port.charge(5)
        if visited[sources[index]] and nodes[sources[index]].kind != 'unresolved_reference':
            examined.append(edge)
    # Preferred witnesses never discard late denied/conflicted alternatives.
    for edge in graph.observations:
        port.charge(3)
        source = _node_index(nodes, edge.source, port)
        _require(source >= 0)
        if visited[source]:
            port.charge(1)
            observations.append(edge)
    port.charge(len(observations) + 1)
    ordered_observations = _graph_sort(tuple(observations), port)
    port.charge(2 * (len(found) + len(initial) + len(frontiers) + len(terminals) + len(examined)) +
                len(ordered_observations) + 32)
    result = _Reachability(graph, tuple(initial), tuple(found), tuple(examined), tuple(frontiers),
                           tuple(terminals), ordered_observations)
    port.check()
    return result
