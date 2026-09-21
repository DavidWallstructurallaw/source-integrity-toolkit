# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: ORIGIN_ANALYSIS. Private, paid M002/M007 finite inventories.

Definitions 20--22, lineage 9.1/10 and reporting 16: all represented branches
remain visible beside positive origins. A boundary label cannot hide a parent.
Facts belong to one current job and the invocation's sole witness ledger.
No M004 disposition, independence, public report or orchestration is provided.
"""
from dataclasses import dataclass
from ..contracts.bundle import _require, _Array, _freeze_object, _lookup_pair
from ..contracts.evidence import _Entity, _PreparedBundle, _QualificationContext, _SourceAddress, _Node, _BasisQualification
from ..contracts import results as _r
from ..contracts.report import (
    _charge_scope, _charge_input_ref, _charge_frozen, _charge_link,
    _ScopeCheckFact, _scope_check, _PopulationCompletion, _ComponentCompletion,
    _CompletionRecord, _completion_check,
)
from ..validation.structure import _field
from ..validation.semantics import (
    _analysis_port, _analysis_start, _analysis_lookup, _analysis_ids,
    _analysis_contains, _analysis_subset, _analysis_text, _analysis_address,
    _analysis_codes, _analysis_scope, _analysis_temporal, _analysis_current,
    _qualify_basis, _qualify_conflicts, _qualify_identity, _qualify_coverage,
    _compare_times, _profile_ref, _profile_population,
)
from ..graph.projections import _Projection, _project, _check_projection, _graph_sort, _check_edge_eligibility
from ..graph.traversal import _reachable, _ranked_search, _path_from_search, _node_index
from ..graph.cycles import _components
from ..graph.witnesses import _check_ledger, _path_witness, _cycle_witness, _GraphWitness
from .inventory import _inventory_facts, _check_inventory

_PARENTS = ('derived_from', 'copies', 'syndicated_from', 'summarizes',
            'translates', 'quotes', 'originates_from', 'depends_on')
_EVIDENCE_PARENTS = _PARENTS[:-1]
_ROLES = ('documented_origin', 'declared_origin', 'reference_baseline', 'scope_cut', 'unresolved')


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _AncestryGap:
    seed: _Entity
    source: _SourceAddress
    reason_codes: tuple
    related_refs: tuple

    def __post_init__(self):
        _require(type(self.seed) is _Entity and self.seed.kind == 'evidence_item')
        _require(type(self.source) is _SourceAddress and type(self.reason_codes) is tuple)
        _require(bool(self.reason_codes) and all(type(code) is str and code in _r.REASON_CODES for code in self.reason_codes))
        _require(type(self.related_refs) is tuple and all(type(ref) is _SourceAddress for ref in self.related_refs))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _BoundaryFact:
    assessment: _Entity
    origin: _Entity
    native_role: str
    state: str
    reason_codes: tuple
    basis: object
    coverage: tuple
    identity: object
    conflict: object

    def __post_init__(self):
        _require(type(self.assessment) is _Entity and type(self.origin) is _Entity)
        _require(type(self.native_role) is str and self.native_role in _ROLES)
        _require(type(self.state) is str and self.state in ('met', 'unmet'))
        _require(type(self.reason_codes) is tuple and type(self.coverage) is tuple)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _NodeFacts:
    entity: _Entity
    coverage: tuple
    identity: object
    reason_codes: tuple


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _EdgeFacts:
    edge: object
    basis: object
    reason_codes: tuple
    documentary: bool
    source_times: tuple
    conflict: object


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _SeedTrace:
    seed: _Entity
    reachability: object
    reached_origins: tuple
    documentary_origins: tuple
    declared_origins: tuple
    baseline_origins: tuple
    scope_cut_origins: tuple
    unqualified_terminals: tuple
    frontiers: tuple
    boundaries: tuple
    gaps: tuple
    cycles: tuple
    witnesses: tuple
    node_facts: tuple
    edge_facts: tuple

    def __post_init__(self):
        _require(type(self.seed) is _Entity and self.seed.kind == 'evidence_item')
        for rows in (self.reached_origins, self.documentary_origins, self.declared_origins,
                     self.baseline_origins, self.scope_cut_origins, self.unqualified_terminals,
                     self.frontiers, self.boundaries, self.gaps, self.cycles, self.witnesses,
                     self.node_facts, self.edge_facts):
            _require(type(rows) is tuple)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _OriginFacts:
    prepared: _PreparedBundle
    context: _QualificationContext
    job_port: object
    inventory: object
    graph: _Projection
    seed_traces: tuple
    reached_origins: tuple
    documentary_origins: tuple
    unresolved_frontiers: tuple
    unqualified_terminals: tuple
    affected_seeds: tuple
    boundaries: tuple
    witnesses: tuple
    pc04: object
    node_facts: tuple
    edge_facts: tuple
    inventory_witness: _GraphWitness
    temporal_facts: tuple
    coverage_bases: tuple
    coverage_conflicts: tuple

    def __post_init__(self):
        _require(type(self.prepared) is _PreparedBundle and type(self.context) is _QualificationContext)
        _require(type(self.graph) is _Projection and self.graph.prepared is self.prepared and self.graph.job_port is self.job_port)
        for rows in (self.seed_traces, self.reached_origins, self.documentary_origins,
                     self.unresolved_frontiers, self.unqualified_terminals, self.affected_seeds,
                     self.boundaries, self.witnesses, self.node_facts, self.edge_facts, self.temporal_facts,
                     self.coverage_bases, self.coverage_conflicts):
            _require(type(rows) is tuple)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _OriginProfile:
    facts: _OriginFacts
    results: tuple
    witnesses: tuple

    def __post_init__(self):
        _require(type(self.facts) is _OriginFacts and type(self.results) is tuple and type(self.witnesses) is tuple)


def _tuple(rows, port):
    port.charge(len(rows) + 1)
    return tuple(rows)


def _context(context, subjects, predicates, port):
    for values in (context.claim_refs, subjects, predicates):
        port.charge(len(values) * len(values) + len(values) + 1)
        for value in values:
            _analysis_text(value, port)
            _analysis_text(value, port)
    if context.requested_time is not None:
        _charge_frozen(context.requested_time.fields, port)
    port.charge(len(context.operation_anchor) + 20)
    for part in context.operation_anchor:
        if type(part) is str:
            _analysis_text(part, port)
        elif type(part) is _SourceAddress:
            _analysis_text(part.record_id, port)
            _analysis_text(part.selector, port)
    return _QualificationContext(context.inquiry_ref, context.claim_refs, subjects,
        context.dependency_dimension, context.temporal_basis, context.requested_time,
        'upstream_history', predicates, 'claim_origin', context.operation_anchor)


def _unique_entities(prepared, rows, port):
    ids = []
    for row in rows:
        port.charge(2)
        ids.append(row.identifier)
    output = []
    for identifier, unused in _analysis_ids(_tuple(ids, port), port):
        port.charge(1)
        output.append(_analysis_lookup(prepared, identifier, port))
    return _tuple(output, port)


def _node(graph, entity, port):
    for node in graph.nodes:
        port.charge(2)
        _analysis_text(entity.identifier, port)
        if node.collection == entity.collection and node.identifier == entity.identifier:
            return node
    raise TypeError('origin_node_missing')


def _coverage_for(prepared, entity, context, candidates, cache, port):
    """Cache paid qualification, then prove each actual node's finite area.

    The cached context has empty subjects; every use additionally requires
    actual membership and subject-or-Inquiry coverage. Origin-only coverage
    therefore cannot establish completeness for a preceding EvidenceItem.
    """
    predicates = ('depends_on',) if entity.kind == 'origin_event' else _EVIDENCE_PARENTS
    output = []
    for candidate in candidates:
        port.charge(1)
        data = _field(candidate.node.fields, 'data', port)
        details = _field(data, 'details', port)
        members, subjects = _field(details, 'member_refs', port).items, _field(data, 'subject_refs', port).items
        if not _analysis_contains(members, entity.identifier, port):
            continue
        if not (_analysis_contains(subjects, entity.identifier, port) or _analysis_contains(subjects, context.inquiry_ref, port)):
            continue
        found = None
        for old, kind, fact in cache:
            port.charge(2)
            if old is candidate and kind == entity.kind:
                found = fact
                break
        if found is None:
            local = _context(context, (), predicates, port)
            found = _qualify_coverage(prepared, (candidate.identifier,), local, port)[0]
            port.charge(4)
            cache.append((candidate, entity.kind, found))
        port.charge(len(found.reason_codes) + len(found.support_refs) + 3)
        output.append(found)
    return _tuple(output, port)


def _edge_times(prepared, edge, port):
    # Only explicit causal OriginEvent times; publication is not creation.
    if edge.predicate != 'depends_on' or edge.source.kind != 'origin_event' or edge.target.kind != 'origin_event':
        port.charge(3)
        return (), ()
    times = []
    for node in (edge.source, edge.target):
        entity = _analysis_lookup(prepared, node.identifier, port)
        value = _field(_field(entity.node.fields, 'data', port), 'occurred_at', port)
        _charge_frozen(value, port)
        port.charge(3)
        times.append(_Node('TimeValue', value))
    comparison = _compare_times(times[1], times[0], port)
    port.charge(3)
    return (('temporal_inconsistency',) if comparison.comparison == 'after' else ()), _tuple(times, port)


def _node_identity(prepared, entity, context, examined, port):
    """Project a completed same-job identity scan onto this exact member.

    Only affected members need the owner's separate local conflict reasons.
    No global identity problem is transferred to an unrelated seed/origin.
    """
    local = _context(context, (entity.identifier,), _PARENTS, port)
    for address in examined.support_refs:
        port.charge(1)
        candidate = _analysis_lookup(prepared, address.record_id, port)
        if candidate.collection != 'assertions':
            continue
        data = _field(candidate.node.fields, 'data', port)
        for field in ('from_ref', 'to_ref'):
            _analysis_text(entity.identifier, port)
            if _field(data, field, port) == entity.identifier:
                return _qualify_identity(prepared, (entity.identifier,), local, port)
    port.charge(16)
    return _BasisQualification(_analysis_address(entity, port), 'unspecified', 'met', (), (),
        ('This exact resolved member had no applicable alias in the completed current-job finite identity scan.',), local)


def _trace_witness(reach, ledger, port):
    _check_ledger(reach.graph, ledger, port)
    count = 0
    for rows in (reach.starts, reach.nodes, reach.edges, reach.frontiers, reach.terminals, reach.observations):
        port.charge(len(rows) + 1)
        count += len(rows)
    token = ledger.reserve(witnesses=1, members=count)
    port.charge(17)
    result = _GraphWitness('complete_trace', reach.graph, starts=reach.starts,
        examined_nodes=reach.nodes, examined_edges=reach.edges, frontiers=reach.frontiers,
        terminals=reach.terminals, observations=reach.observations, member_count=count)
    port.check()
    ledger.retain(token)
    port.check()
    return result


def _gap(seed, source, codes, related, port):
    codes = _analysis_codes(codes, port)
    port.charge(len(codes) * len(_r.REASON_CODES) + len(related) + 12)
    return _AncestryGap(seed, source, codes, related)


def _origin_facts(prepared, context, ledger, port):
    """Complete current-job trace; qualification facts are not M004 outcomes."""
    _analysis_start(prepared, context, port)
    port.charge(30)
    _require(len(context.claim_refs) == 1 and context.dependency_dimension is not None and
             context.graph_view == 'claim_origin' and context.coverage_kind == 'upstream_history')
    _require(len(context.relation_types) == len(_PARENTS) and _analysis_subset(_PARENTS, context.relation_types, port))
    inventory = _inventory_facts(prepared, context, port)
    _require(_analysis_contains(_field(inventory.inquiry.node.fields, 'dependency_dimensions', port).items,
                                context.dependency_dimension, port))
    seed_ids = []
    for seed in inventory.seed_evidence:
        port.charge(1)
        seed_ids.append(seed.identifier)
    graph_context = _context(context, _tuple(seed_ids, port), _PARENTS, port)
    graph = _project(prepared, graph_context, port)
    _check_ledger(graph, ledger, port)
    local = _context(context, (), _PARENTS, port)
    reaches, all_nodes, all_edges = [], [], []
    for seed in inventory.seed_evidence:
        reach = _reachable(graph, (_node(graph, seed, port),), port)
        port.charge(len(reach.nodes) + len(reach.edges) + 3)
        reaches.append((seed, reach))
        all_nodes.extend(reach.nodes)
        all_edges.extend(reach.edges)
    reached_entities = []
    for node in all_nodes:
        port.charge(1)
        reached_entities.append(_analysis_lookup(prepared, node.identifier, port))
    reached_entities = _unique_entities(prepared, reached_entities, port)
    edges = _graph_sort(_tuple(all_edges, port), port)
    unique_edges, previous = [], None
    for edge in edges:
        port.charge(2)
        if edge is not previous:
            unique_edges.append(edge)
        previous = edge
    edges = _tuple(unique_edges, port)
    pc04 = _check_edge_eligibility(graph, edges, port)
    candidates, boundary_candidates = [], []
    for entity in graph.annotations:
        port.charge(1)
        obj = entity.node.fields
        if entity.collection != 'assertions' or _field(obj, 'assertion_kind', port) != 'assessment':
            continue
        if not _analysis_scope(entity, local, port, subjects=False):
            continue
        timing = _analysis_temporal(entity, local, port)
        if timing is not None and timing.state == 'unmet' and 'temporal_inconsistency' not in timing.reason_codes:
            continue
        data = _field(obj, 'data', port)
        kind = _field(data, 'assessment_kind', port)
        if kind == 'coverage' and _field(_field(data, 'details', port), 'coverage_kind', port) == 'upstream_history':
            port.charge(1)
            candidates.append(entity)
        elif kind == 'origin_boundary':
            port.charge(1)
            boundary_candidates.append(entity)
    identity_ids = []
    for entity in reached_entities:
        port.charge(2)
        if entity.kind != 'unresolved_reference':
            identity_ids.append(entity.identifier)
    identity_context = _context(context, _tuple(identity_ids, port), _PARENTS, port)
    examined_identity = _qualify_identity(prepared, identity_context.subject_refs, identity_context, port)
    coverage_cache, node_facts = [], []
    for entity in reached_entities:
        port.charge(1)
        if entity.kind == 'unresolved_reference':
            continue
        coverage = _coverage_for(prepared, entity, local, candidates, coverage_cache, port)
        identity = _node_identity(prepared, entity, local, examined_identity, port)
        port.charge(len(identity.reason_codes) + 2)
        codes = list(identity.reason_codes)
        covered = False
        for fact in coverage:
            port.charge(2)
            covered = covered or fact.state == 'met'
        if not covered:
            codes.append('upstream_coverage_incomplete')
            for fact in coverage:
                port.charge(len(fact.reason_codes))
                codes.extend(fact.reason_codes)
        port.charge(7)
        node_facts.append(_NodeFacts(entity, coverage, identity, _analysis_codes(codes, port)))
    edge_facts, clean_edges = [], []
    for edge in edges:
        basis = _qualify_basis(prepared, edge.source_ref.record_id, local, port)
        time_codes, source_times = _edge_times(prepared, edge, port)
        port.charge(len(basis.reason_codes) + len(edge.reason_codes) + len(time_codes) + 1)
        codes = _analysis_codes(basis.reason_codes + edge.reason_codes + time_codes, port)
        blocked = False
        for code in codes:
            port.charge(2)
            if code != 'self_supporting_assurance':
                blocked = True
        documentary = basis.state == 'met' and not blocked
        conflict = None
        port.charge(len(edge.reason_codes) + 1)
        if 'premise_disputed' in edge.reason_codes:
            conflict = _qualify_conflicts(prepared, edge.source_ref.record_id, local, port)
        port.charge(9)
        edge_facts.append(_EdgeFacts(edge, basis, codes, documentary, source_times, conflict))
        if documentary:
            port.charge(1)
            clean_edges.append(edge)
    port.charge(len(graph.nodes) + len(clean_edges) * 2 + len(graph.observations) + len(graph.annotations) + 15)
    clean_graph = _Projection(prepared, graph_context, graph.nodes, _tuple(clean_edges, port),
                              graph.observations, graph.annotations, None, port)
    boundaries = []
    for entity in reached_entities:
        port.charge(1)
        if entity.kind != 'origin_event':
            continue
        origin_node = _node(graph, entity, port)
        nf = None
        for item in node_facts:
            port.charge(1)
            if item.entity is entity:
                nf = item
                break
        for assessment in boundary_candidates:
            data = _field(assessment.node.fields, 'data', port)
            if not _analysis_contains(_field(data, 'subject_refs', port).items, entity.identifier, port):
                continue
            details = _field(data, 'details', port)
            role = _field(details, 'boundary_role', port)
            boundary_context = _context(context, (entity.identifier,), ('depends_on',), port)
            basis = _qualify_basis(prepared, assessment.identifier, boundary_context, port)
            conflict = _qualify_conflicts(prepared, assessment.identifier, boundary_context, port)
            coverage_ref = _field(details, 'coverage_ref', port)
            coverage, covered = [], False
            for fact in nf.coverage:
                port.charge(2)
                _analysis_text(fact.source.record_id, port)
                if coverage_ref is not None and fact.source.record_id == coverage_ref:
                    coverage.append(fact)
                    covered = fact.state == 'met'
            port.charge(len(basis.reason_codes) + len(conflict.reason_codes) + len(nf.identity.reason_codes) + 5)
            codes = list(basis.reason_codes + conflict.reason_codes + nf.identity.reason_codes)
            for fact in coverage:
                port.charge(len(fact.reason_codes))
                codes.extend(fact.reason_codes)
            active = _field(assessment.node.fields, 'lifecycle_state', port) == 'active'
            timing = _analysis_temporal(assessment, boundary_context, port)
            valid_time = timing is None or timing.state == 'met'
            parent = False
            for edge in graph.observations:
                port.charge(1)
                if edge.source is not origin_node or not _analysis_scope(edge.source_entity, local, port, subjects=False):
                    continue
                current, uncertain = _analysis_current(prepared, edge.source_entity, port)
                timing_edge = _analysis_temporal(edge.source_entity, local, port)
                outside = timing_edge is not None and timing_edge.state == 'unmet' and 'temporal_inconsistency' not in timing_edge.reason_codes
                positive = _field(_field(edge.source_entity.node.fields, 'data', port), 'polarity', port) == 'affirmed'
                if current and positive and not outside:
                    parent = True
            if not active or not valid_time:
                codes.append('time_applicability_unknown' if not valid_time else 'unqualified_origin_boundary')
            if not covered:
                codes.append('upstream_coverage_incomplete')
            if parent or role == 'unresolved':
                codes.append('unqualified_origin_boundary')
            usable = active and valid_time and covered and not parent and nf.identity.state == 'met' and conflict.state == 'met'
            if role == 'documented_origin' and basis.state != 'met' or role == 'unresolved':
                usable = False
            port.charge(14)
            boundaries.append(_BoundaryFact(assessment, entity, role, 'met' if usable else 'unmet',
                _analysis_codes(codes, port), basis, _tuple(coverage, port), nf.identity, conflict))
    components = _components(graph, port)
    cycle_witnesses, witnesses, traces = [], [], []
    for component in components:
        port.charge(1)
        if component.cycle is None:
            continue
        used = False
        for node in all_nodes:
            port.charge(1)
            if _node_index(component.members, node, port) >= 0:
                used = True
                break
        if used:
            witness = _cycle_witness(component, ledger, port)
            port.charge(4)
            cycle_witnesses.append((component, witness))
            witnesses.append(witness)
    for seed, reach in reaches:
        path_search = _ranked_search(graph, _node(graph, seed, port), port)
        clean_search = _ranked_search(clean_graph, _node(graph, seed, port), port)
        port.charge(16)
        row_witnesses = [_trace_witness(reach, ledger, port)]
        gaps, row_boundaries, origins, documentary, declared, baseline, cuts, terminals, frontiers = [], [], [], [], [], [], [], [], []
        row_nodes, row_edges, row_cycles = [], [], []
        for node in reach.nodes:
            entity = _analysis_lookup(prepared, node.identifier, port)
            port.charge(3)
            if entity.kind == 'origin_event':
                origins.append(entity)
            if entity.kind == 'unresolved_reference':
                frontiers.append(entity)
                gaps.append(_gap(seed, _analysis_address(entity, port), ('unknown_endpoint',), (), port))
            else:
                for nf in node_facts:
                    port.charge(1)
                    if nf.entity is entity:
                        row_nodes.append(nf)
                        if nf.reason_codes:
                            gaps.append(_gap(seed, _analysis_address(entity, port), nf.reason_codes, (), port))
                        break
            usable = False
            for fact in boundaries:
                port.charge(1)
                if fact.origin is not entity:
                    continue
                row_boundaries.append(fact)
                if fact.state == 'met':
                    usable = True
                    if fact.native_role == 'documented_origin':
                        if _path_from_search(clean_search, node, port) is not None:
                            documentary.append(entity)
                    elif fact.native_role == 'declared_origin':
                        declared.append(entity)
                    elif fact.native_role == 'reference_baseline':
                        baseline.append(entity)
                    elif fact.native_role == 'scope_cut':
                        cuts.append(entity)
                elif fact.reason_codes:
                    gaps.append(_gap(seed, _analysis_address(fact.assessment, port), fact.reason_codes, (), port))
            is_terminal = _node_index(reach.terminals, node, port) >= 0
            if is_terminal and entity.kind in ('evidence_item', 'origin_event') and not usable:
                terminals.append(entity)
                gaps.append(_gap(seed, _analysis_address(entity, port), ('unqualified_origin_boundary',), (), port))
            if entity.kind in ('origin_event', 'unresolved_reference') or is_terminal:
                path = _path_from_search(path_search, node, port)
                _require(path is not None)
                port.charge(1)
                row_witnesses.append(_path_witness(path, ledger, port))
        for fact in edge_facts:
            for edge in reach.edges:
                port.charge(2)
                if fact.edge is not edge:
                    continue
                row_edges.append(fact)
                blockers = []
                for code in fact.reason_codes:
                    port.charge(1)
                    if code != 'self_supporting_assurance':
                        blockers.append(code)
                if blockers:
                    gaps.append(_gap(seed, edge.source_ref, _tuple(blockers, port), (), port))
                break
        # Wrong Claim/dimension/outside-time records are observations, not
        # gaps in this row. Weak current denial and uncertain lifecycle stay.
        for edge in reach.observations:
            port.charge(1)
            if edge.eligible or edge.source.kind == 'unresolved_reference':
                continue
            entity = edge.source_entity
            if not _analysis_scope(entity, local, port, subjects=False):
                continue
            current, uncertain = _analysis_current(prepared, entity, port)
            timing = _analysis_temporal(entity, local, port)
            if not current or timing is not None and timing.state == 'unmet' and 'temporal_inconsistency' not in timing.reason_codes:
                continue
            positive = _field(_field(entity.node.fields, 'data', port), 'polarity', port) == 'affirmed'
            if positive or 'premise_disputed' in edge.reason_codes:
                gaps.append(_gap(seed, edge.source_ref, edge.reason_codes or ('documentary_basis_incomplete',), (), port))
        for component, witness in cycle_witnesses:
            if _node_index(reach.nodes, component.members[0], port) >= 0:
                port.charge(2)
                row_cycles.append(component)
                row_witnesses.append(witness)
                source = _analysis_lookup(prepared, component.members[0].identifier, port)
                gaps.append(_gap(seed, _analysis_address(source, port), ('lineage_cycle',), (), port))
        for witness in row_witnesses:
            port.charge(1)
            if witness.kind != 'cycle':
                witnesses.append(witness)
        port.charge(24)
        traces.append(_SeedTrace(seed, reach,
            _unique_entities(prepared, origins, port), _unique_entities(prepared, documentary, port),
            _unique_entities(prepared, declared, port), _unique_entities(prepared, baseline, port),
            _unique_entities(prepared, cuts, port), _unique_entities(prepared, terminals, port),
            _unique_entities(prepared, frontiers, port), _tuple(row_boundaries, port), _tuple(gaps, port),
            _tuple(row_cycles, port), _tuple(row_witnesses, port), _tuple(row_nodes, port), _tuple(row_edges, port)))
    origins, documentary, frontiers, terminals, affected = [], [], [], [], []
    for trace in traces:
        port.charge(len(trace.reached_origins) + len(trace.frontiers) + len(trace.unqualified_terminals) + 4)
        origins.extend(trace.reached_origins)
        frontiers.extend(trace.frontiers)
        terminals.extend(trace.unqualified_terminals)
        if trace.gaps:
            affected.append(trace.seed)
    for fact in boundaries:
        port.charge(2)
        if fact.native_role == 'documented_origin' and fact.state == 'met':
            documentary.append(fact.origin)
    port.charge(24)
    # A real complete multi-seed scan is retained once for each cell's finite
    # inventory claim. The per-seed scans and every path remain retained too.
    # No reference stands in for an unexecuted scan or uncounted payload.
    starts = []
    for seed in inventory.seed_evidence:
        starts.append(_node(graph, seed, port))
    if len(traces) == 1:
        inventory_witness = traces[0].witnesses[0]
    else:
        inventory_witness = _trace_witness(_reachable(graph, _tuple(starts, port), port), ledger, port)
        witnesses.append(inventory_witness)
    # Actual temporal-owner outputs are retained once for later atomic checks.
    # A coverage TimeQualification unknown must not turn into a met PC10 just
    # because the boundary and relation windows happened to be known.
    temporal_sources = []
    port.charge(len(candidates) + len(boundary_candidates) + 1)
    for entity in candidates + boundary_candidates:
        port.charge(1)
        temporal_sources.append(entity)
    for trace in traces:
        for edge in trace.reachability.observations:
            port.charge(1)
            temporal_sources.append(edge.source_entity)
    temporal_facts = []
    for entity in _unique_entities(prepared, temporal_sources, port):
        port.charge(2)
        temporal_facts.append((entity, _analysis_temporal(entity, local, port)))
    coverage_sources, coverage_bases, coverage_conflicts = [], [], []
    for entity, kind, qualification in coverage_cache:
        port.charge(1)
        coverage_sources.append(entity)
    for entity in _unique_entities(prepared, coverage_sources, port):
        basis = _qualify_basis(prepared, entity.identifier, local, port)
        port.charge(2)
        coverage_bases.append((entity, basis))
        for candidate, kind, qualification in coverage_cache:
            port.charge(len(qualification.reason_codes) + 2)
            if candidate is entity and 'premise_disputed' in qualification.reason_codes:
                conflict = _qualify_conflicts(prepared, entity.identifier, local, port)
                port.charge(2)
                coverage_conflicts.append((entity, conflict))
                break
    result = _OriginFacts(prepared, context, port, inventory, graph, _tuple(traces, port),
        _unique_entities(prepared, origins, port), _unique_entities(prepared, documentary, port),
        _unique_entities(prepared, frontiers, port), _unique_entities(prepared, terminals, port),
        _unique_entities(prepared, affected, port), _tuple(boundaries, port), _tuple(witnesses, port),
        pc04, _tuple(node_facts, port), _tuple(edge_facts, port), inventory_witness,
        _tuple(temporal_facts, port), _tuple(coverage_bases, port), _tuple(coverage_conflicts, port))
    port.check()
    return result


def _check_facts(facts, port):
    _analysis_port(port)
    port.charge(4)
    _require(type(facts) is _OriginFacts and facts.job_port is port)
    _check_projection(facts.graph, port)
    _check_inventory(facts.inventory, port)


def _source_ref(address, port):
    for text in (address.collection, address.record_id, address.selector):
        _analysis_text(text, port)
    port.charge(5)
    return _r._InputRef(address.collection, address.record_id, address.selector or None)


def _scope(facts, port):
    context = facts.context
    inquiry = _profile_ref(facts.inventory.inquiry, port)
    claims, targets, coverages, anchor = [], [], [], []
    for identifier in context.claim_refs:
        claims.append(_profile_ref(_analysis_lookup(facts.prepared, identifier, port), port))
    # These are full E(I,C) inventories, not separately targeted seed queries.
    # The explicit Inquiry/Claim and actual PC03 population establish the seed
    # scope; copying all population members into target_refs would describe a
    # second, redundant target operation. Per-seed disclosures name their seed.
    # Preserve explicitly supplied targets, which inventory has already
    # checked equal to full E(I,C); never invent targets from an empty request.
    for identifier in context.subject_refs:
        targets.append(_profile_ref(_analysis_lookup(facts.prepared, identifier, port), port))
    coverage_entities = []
    for nf in facts.node_facts:
        for coverage in nf.coverage:
            port.charge(2)
            coverage_entities.append(coverage.coverage)
    for entity in _unique_entities(facts.prepared, coverage_entities, port):
        coverages.append(_profile_ref(entity, port))
    for part in context.operation_anchor:
        port.charge(2)
        if type(part) is _SourceAddress:
            part = _source_ref(part, port)
        anchor.append(part)
    for refs in (claims, targets, coverages):
        port.charge(len(refs) * len(refs) + len(refs) + 1)
        for ref in refs:
            _charge_input_ref(ref, port, repeats=len(refs) + 3)
    if context.requested_time is not None:
        _charge_frozen(context.requested_time.fields, port)
    for part in anchor:
        if type(part) is _r._InputRef:
            _charge_input_ref(part, port, repeats=2)
        elif type(part) is str:
            _analysis_text(part, port)
    port.charge(20)
    return _r._Scope(inquiry, _tuple(claims, port), _tuple(targets, port), context.dependency_dimension,
        'claim_origin', context.temporal_basis, context.requested_time, _tuple(coverages, port),
        ('Complete finite supplied view only; current snapshot does not reconstruct lifecycle history or hidden roots.',),
        _tuple(anchor, port))


def _boundary_disclosure(fact, port):
    fields = []
    for name in ('data', 'scope', 'provenance', 'lifecycle_state'):
        value = _field(fact.assessment.node.fields, name, port)
        _charge_frozen(value, port)
        port.charge(1)
        fields.append((name, value))
    gap = _lookup_pair(fact.assessment.node.fields.items, 'gaps', port)
    if gap is not None:
        _charge_frozen(gap[1], port)
        fields.append(('gaps', gap[1]))
    port.charge(len(fact.reason_codes) + 6)
    fields.extend((('qualification_state', fact.state), ('reason_codes', _Array(fact.reason_codes))))
    frozen = _freeze_object(fields, port)
    port.charge(8)
    for note in fact.basis.qualifications:
        _analysis_text(note, port)
    return _r._Disclosure(_profile_ref(fact.assessment, port), frozen, fact.basis.qualifications)


def _address_object(address, port):
    for text in (address.collection, address.record_id, address.selector):
        _analysis_text(text, port)
    return _freeze_object([('collection', address.collection), ('identifier', address.record_id),
                           ('selector', address.selector)], port)


def _gap_disclosure(trace, dimension, port):
    entries, frontier_rows, coverages, witness_paths = [], [], [], []
    for gap in trace.gaps:
        port.charge(len(gap.reason_codes) + 6)
        entries.append(_freeze_object([('source', _address_object(gap.source, port)),
            ('reason_codes', _Array(gap.reason_codes))], port))
    for entity in trace.frontiers:
        _charge_frozen(entity.node.fields, port)
        port.charge(1)
        frontier_rows.append(entity.node.fields)
    # Retain unique native coverage identities, state and reasons in each row;
    # the prepared source and typed facts retain their complete native record.
    seen = []
    for nf in trace.node_facts:
        for fact in nf.coverage:
            if _analysis_contains(_tuple(seen, port), fact.source.record_id, port):
                continue
            port.charge(len(fact.reason_codes) + 6)
            seen.append(fact.source.record_id)
            coverages.append(_freeze_object([('coverage_ref', fact.source.record_id),
                ('qualification_state', fact.state), ('reason_codes', _Array(fact.reason_codes))], port))
    for witness in trace.witnesses:
        if witness.kind != 'path':
            continue
        nodes, edges = [], []
        for node in witness.nodes:
            _analysis_text(node.identifier, port)
            port.charge(1)
            nodes.append(node.identifier)
        for edge in witness.edges:
            _analysis_text(edge.source_ref.record_id, port)
            port.charge(1)
            edges.append(edge.source_ref.record_id)
        port.charge(len(nodes) + len(edges) + 4)
        witness_paths.append(_freeze_object([('nodes', _Array(_tuple(nodes, port))),
            ('assertions', _Array(_tuple(edges, port)))], port))
    _analysis_text(trace.seed.identifier, port)
    _analysis_text(dimension, port)
    port.charge(len(entries) + len(frontier_rows) + len(coverages) + len(witness_paths) + 10)
    frozen = _freeze_object([('seed_ref', trace.seed.identifier), ('dimension', dimension),
        ('gaps', _Array(_tuple(entries, port))), ('frontiers', _Array(_tuple(frontier_rows, port))),
        ('coverage', _Array(_tuple(coverages, port))), ('witness_paths', _Array(_tuple(witness_paths, port)))], port)
    port.charge(8)
    return _r._Disclosure(_profile_ref(trace.seed, port), frozen,
        ('One affected seed; frontier IDs and terminal IDs retain distinct counting units and opaque commonality.',))


def _witness_refs(facts, scope, field, members, port):
    selected, target_ids, selected_ids = [facts.inventory_witness], [], []
    for entity in members:
        port.charge(1)
        target_ids.append(entity.identifier)
    target_ids = _tuple(target_ids, port)
    per_seed = field in ('seed_items_with_unresolved_ancestry_count', 'ancestry_gap_disclosures')
    if field == 'origin_boundary_disclosures':
        target_ids = []
        for fact in facts.boundaries:
            port.charge(1)
            target_ids.append(fact.origin.identifier)
        target_ids = _tuple(target_ids, port)
    for witness in facts.witnesses:
        port.charge(1)
        if witness.kind == 'cycle':
            if per_seed:
                selected.append(witness)
            continue
        if witness.kind != 'path':
            continue
        identifier = witness.nodes[0 if per_seed else -1].identifier
        if _analysis_contains(target_ids, identifier, port) and (per_seed or not
                _analysis_contains(_tuple(selected_ids, port), identifier, port)):
            port.charge(2)
            selected.append(witness)
            selected_ids.append(identifier)
    refs = []
    for witness in selected:
        anchor = [witness.kind]
        if witness.kind == 'complete_trace':
            nodes = witness.starts
            kind = 'member_set'
        else:
            # A witness reference identifies a completed canonical query;
            # its full path remains in the separately quota-counted payload.
            # The exact scope/start/target uniquely selects that query here.
            port.charge(3)
            nodes = (witness.nodes[0],) if witness.kind == 'cycle' else (witness.nodes[0], witness.nodes[-1])
            kind = witness.kind
        for node in nodes:
            port.charge(1)
            entity = _analysis_lookup(facts.prepared, node.identifier, port)
            anchor.append(_profile_ref(entity, port))
        for part in anchor:
            port.charge(1)
            if type(part) is _r._InputRef:
                _charge_input_ref(part, port, repeats=2)
        _charge_scope(scope, port)
        port.charge(len(anchor) + 8)
        refs.append(_r._WitnessRef(scope, kind, _tuple(anchor, port)))
    return _tuple(refs, port)


def _basis_sources(facts, port):
    entities = [facts.inventory.inquiry]
    for edge in facts.edge_facts:
        port.charge(1)
        entities.append(edge.edge.source_entity)
    for fact in facts.boundaries:
        port.charge(1)
        entities.append(fact.assessment)
    for fact in facts.node_facts:
        for coverage in fact.coverage:
            port.charge(1)
            entities.append(coverage.coverage)
    output = []
    for entity in _unique_entities(facts.prepared, entities, port):
        source = _profile_ref(entity, port)
        _charge_input_ref(source, port)
        port.charge(3)
        output.append(_r._BasisRef(source))
    return _tuple(output, port)


def _reason_sources(facts, port):
    """Paid finite reason grouping; keep each exact affected source once."""
    rows = []
    for code in _r.REASON_CODES:
        entities = []
        for trace in facts.seed_traces:
            for gap in trace.gaps:
                port.charge(len(gap.reason_codes) + 1)
                if code in gap.reason_codes:
                    entities.append(_analysis_lookup(facts.prepared, gap.source.record_id, port))
        for fact in facts.boundaries:
            port.charge(len(fact.reason_codes) + 1)
            if code in fact.reason_codes:
                entities.append(fact.assessment)
                for coverage in fact.coverage:
                    port.charge(len(coverage.reason_codes) + 1)
                    if code in coverage.reason_codes:
                        entities.append(coverage.coverage)
        for nf in facts.node_facts:
            port.charge(len(nf.reason_codes) + 1)
            if code in nf.reason_codes:
                for coverage in nf.coverage:
                    port.charge(len(coverage.reason_codes) + 1)
                    if code in coverage.reason_codes:
                        entities.append(coverage.coverage)
        if code == 'premise_disputed':
            for fact in facts.edge_facts:
                port.charge(1)
                if fact.conflict is not None:
                    for address in fact.conflict.support_refs:
                        entities.append(_analysis_lookup(facts.prepared, address.record_id, port))
            for entity, qualification in facts.coverage_conflicts:
                selected = False
                for candidate in entities:
                    port.charge(1)
                    selected = selected or candidate is entity
                if selected:
                    for address in qualification.support_refs:
                        entities.append(_analysis_lookup(facts.prepared, address.record_id, port))
        if entities:
            sources = []
            for entity in _unique_entities(facts.prepared, entities, port):
                sources.append(_profile_ref(entity, port))
            port.charge(2)
            rows.append((code, _tuple(sources, port)))
    return _tuple(rows, port)


def _time_state(facts, entity, port):
    for source, timing in facts.temporal_facts:
        port.charge(2)
        if source is entity:
            return 'met' if timing is None else timing.state
    raise TypeError('origin_temporal_fact_missing')


def _coverage_premises(facts, coverage, source_groups, bases, conflicts, port):
    for entity, basis in facts.coverage_bases:
        port.charge(2)
        if entity is coverage.coverage:
            bases.append(basis.state)
            source_groups[0].append(entity)
            for address in basis.support_refs:
                port.charge(1)
                source_groups[0].append(_analysis_lookup(facts.prepared, address.record_id, port))
            break
    else:
        raise TypeError('origin_coverage_basis_missing')
    # The coverage owner already executed its exact-scope conflict scan.
    # Only that owner supplies premise_disputed in this typed qualification;
    # native declaration labels or failed completeness cannot create it.
    port.charge(len(coverage.reason_codes) + 3)
    conflicts.append('unmet' if 'premise_disputed' in coverage.reason_codes else 'met')
    source_groups[4].append(coverage.coverage)
    if 'premise_disputed' in coverage.reason_codes:
        for entity, qualification in facts.coverage_conflicts:
            port.charge(1)
            if entity is coverage.coverage:
                for address in qualification.support_refs:
                    source_groups[4].append(_analysis_lookup(facts.prepared, address.record_id, port))
                break


def _qualification_facts(facts, boundary_only, port):
    """Expose the actually examined candidate premises, not an AND gate.

    A failed candidate is still an examined member of a finite inventory.
    PC07 therefore can be unmet beside an available zero qualified-record
    count. Its exact candidate records and their individual facts remain
    attributable; this summary never upgrades the failed candidate.
    """
    source_groups = ([], [], [], [], [], [])
    bases, coverage_states, identity_states, conflicts, times = [], [], [], [], []
    for fact in facts.boundaries:
        port.charge(8)
        source_groups[0].append(fact.assessment)
        source_groups[1].append(fact.origin)
        source_groups[2].extend((fact.assessment, fact.origin))
        source_groups[3].append(fact.origin)
        source_groups[4].append(fact.assessment)
        source_groups[5].append(fact.assessment)
        bases.append(fact.basis.state)
        identity_states.append(fact.identity.state)
        conflicts.append(fact.conflict.state)
        covered = False
        for coverage in fact.coverage:
            port.charge(2)
            covered = covered or coverage.state == 'met'
            source_groups[1].append(coverage.coverage)
            source_groups[5].append(coverage.coverage)
            times.append(_time_state(facts, coverage.coverage, port))
            _coverage_premises(facts, coverage, source_groups, bases, conflicts, port)
        coverage_states.append('met' if covered else 'unmet' if fact.coverage else 'unknown')
        times.append(_time_state(facts, fact.assessment, port))
        for index, qualification in ((0, fact.basis), (4, fact.conflict), (3, fact.identity)):
            for source in qualification.support_refs:
                port.charge(1)
                source_groups[index].append(_analysis_lookup(facts.prepared, source.record_id, port))
    if not boundary_only:
        for fact in facts.edge_facts:
            port.charge(6)
            source_groups[0].append(fact.edge.source_entity)
            source_groups[4].append(fact.edge.source_entity)
            source_groups[5].append(fact.edge.source_entity)
            bases.append(fact.basis.state)
            conflicts.append('unmet' if 'premise_disputed' in fact.reason_codes else 'met')
            if fact.conflict is not None:
                for address in fact.conflict.support_refs:
                    source_groups[4].append(_analysis_lookup(facts.prepared, address.record_id, port))
            times.append('unmet' if 'temporal_inconsistency' in fact.reason_codes else
                         _time_state(facts, fact.edge.source_entity, port))
            for source in fact.basis.support_refs:
                port.charge(1)
                source_groups[0].append(_analysis_lookup(facts.prepared, source.record_id, port))
        for fact in facts.node_facts:
            port.charge(3)
            source_groups[1].append(fact.entity)
            source_groups[3].append(fact.entity)
            for source in fact.identity.support_refs:
                port.charge(1)
                source_groups[3].append(_analysis_lookup(facts.prepared, source.record_id, port))
            identity_states.append(fact.identity.state)
            covered = False
            for coverage in fact.coverage:
                port.charge(2)
                source_groups[1].append(coverage.coverage)
                covered = covered or coverage.state == 'met'
            for coverage in fact.coverage:
                port.charge(1)
                if not covered or coverage.state == 'met':
                    source_groups[5].append(coverage.coverage)
                    times.append(_time_state(facts, coverage.coverage, port))
                    _coverage_premises(facts, coverage, source_groups, bases, conflicts, port)
            coverage_states.append('met' if covered else 'unmet' if fact.coverage else 'unknown')
        for entity in facts.unresolved_frontiers:
            port.charge(2)
            identity_states.append('unknown')
            source_groups[3].append(entity)
        for trace in facts.seed_traces:
            for gap in trace.gaps:
                port.charge(len(gap.reason_codes) + 3)
                if 'time_applicability_unknown' in gap.reason_codes or 'temporal_inconsistency' in gap.reason_codes:
                    entity = _analysis_lookup(facts.prepared, gap.source.record_id, port)
                    if entity.collection == 'assertions':
                        times.append('unmet' if 'temporal_inconsistency' in gap.reason_codes else
                                     _time_state(facts, entity, port))
                        source_groups[5].append(entity)
    boundaries = []
    for fact in facts.boundaries:
        port.charge(2)
        boundaries.append('met' if fact.native_role == 'documented_origin' and fact.state == 'met' else 'unmet')
    checks = []
    for index, (check_id, states) in enumerate((('PC05', bases), ('PC06', coverage_states), ('PC07', boundaries),
                             ('PC08', identity_states), ('PC09', conflicts), ('PC10', times))):
        input_refs = []
        for entity in _unique_entities(facts.prepared, source_groups[index], port):
            input_refs.append(_profile_ref(entity, port))
        input_refs = _tuple(input_refs, port)
        port.charge(len(states) * 2 + 3)
        state = ('unmet' if 'unmet' in states else 'unknown' if 'unknown' in states else
                 'met' if states else 'not_applicable')
        port.charge(4)
        checks.append((check_id, state, input_refs))
    return _tuple(checks, port)


def _qualification_checks(facts, ref, field, cache, port):
    boundary_only = field in ('documentary_origin_boundary_record_count', 'origin_boundary_disclosures')
    rows = None
    for key, value in cache:
        port.charge(2)
        if key == boundary_only:
            rows = value
            break
    if rows is None:
        rows = _qualification_facts(facts, boundary_only, port)
        port.charge(3)
        cache.append((boundary_only, rows))
    output = []
    for check_id, state, input_refs in rows:
        for source in input_refs:
            _charge_input_ref(source, port, repeats=len(input_refs) + 3)
        port.charge(len(input_refs) + 14)
        output.append(_r._PrerequisiteCheck(check_id, ref, state, input_refs, (),
            'Actual finite candidate checks, with individual source-bound facts retained. Failed candidates remain '
            'excluded or disclosed; they do not invalidate the completed inventory count or become actual-world roots.'))
    return _tuple(output, port)


def _result(facts, family, field, scope, population, value, basis, witnesses, reasons, qualification_cache, port):
    port.charge(180)
    ref = _r._ResultRef(family, field, scope)
    checks = [_scope_check(_ScopeCheckFact(ref, scope), port)]
    port.charge(12)
    checks.append(_r._PrerequisiteCheck('PC01', ref, 'met', (), (),
        'This private owner received the admitted immutable PreparedBundle; it does not re-execute admission.'))
    for provider in (facts.inventory.pc03, facts.pc04):
        inputs = []
        for address in provider.input_refs:
            inputs.append(_source_ref(address, port))
        for source in inputs:
            _charge_input_ref(source, port, repeats=len(inputs) + 3)
        port.charge(len(inputs) + 12)
        checks.append(_r._PrerequisiteCheck(provider.check_id, ref, provider.state, _tuple(inputs, port), (),
            'Executed owner-local finite selection/edge eligibility; documentary and ancestry limitations remain separate.'))
    local_checks = _qualification_checks(facts, ref, field, qualification_cache, port)
    port.charge(len(local_checks))
    checks.extend(local_checks)
    reason_refs = []
    for code, sources in reasons:
        for source in sources:
            _charge_input_ref(source, port, repeats=len(sources) + 4)
        for unused in range(3):
            _charge_scope(scope, port)
        port.charge(len(sources) + 16)
        reason_refs.append(_r._Reason(code, scope, (ref,), sources,
            'The finite inventory retains this supplied ancestry limitation; it is not a count of hidden roots.',
            'conflict' if code == 'premise_disputed' else 'evidence_gap'))
    reason_refs = _tuple(reason_refs, port)
    components = []
    for name, links in (('premises', population.member_refs), ('conflicts', reason_refs), ('value', (ref,)),
                        ('basis', basis), ('reasons', reason_refs), ('witnesses', witnesses)):
        for link in links:
            for unused in range(3):
                _charge_link(link, port)
        port.charge(len(links) * len(links) + 10)
        components.append(_ComponentCompletion(name, links, links))
    for unused in range(3):
        _charge_link(population, port)
    port.charge(24)
    completion = _CompletionRecord(ref, (population,), (_PopulationCompletion(population, population.member_refs),),
                                   _tuple(components, port))
    checks.append(_completion_check(completion, port))
    for unused in range(2):
        _charge_link(ref, port)
        _charge_link(population, port)
        for links in (checks, basis, witnesses, reason_refs):
            for link in links:
                _charge_link(link, port)
    port.charge(len(checks) + len(basis) + len(witnesses) + len(reason_refs) + 32)
    origin = ('qualification_check' if field == 'documentary_origin_boundary_record_count' else
              'attributed_record' if field == 'origin_boundary_disclosures' else 'graph_derivation')
    result = _r._Result(ref, (population,), 'completed', 'available', origin,
        'count' if type(value) is _r._Count else 'record_disclosures', value, _tuple(checks, port),
        basis, witnesses, reason_refs,
        'Exact supplied record inventory after complete finite examination. A zero is not zero actual roots; '
        'a documentary boundary is not process independence or complete history for every reaching seed. '
        'Snapshot evidence, native labels, opaque identity, gaps and all relevant branches remain attributable.')
    port.check()
    return result


def _origin_results(facts, port, *, family):
    """Commit only this explicitly selected family from same-job paid facts."""
    _check_facts(facts, port)
    port.charge(3)
    _require(type(family) is str and family in ('SIT-M002', 'SIT-M007'))
    scope = _scope(facts, port)
    basis = _basis_sources(facts, port)
    reasons = _reason_sources(facts, port)
    rows, qualification_cache = [], []
    if family == 'SIT-M002':
        definitions = (('reached_origin_record_count', facts.reached_origins, 'origin_event'),
            ('documentary_origin_boundary_record_count', facts.documentary_origins, 'origin_event'))
    else:
        definitions = (('unresolved_frontier_reference_count', facts.unresolved_frontiers, 'unresolved_reference'),
            ('unqualified_terminal_record_count', facts.unqualified_terminals, 'record'),
            ('seed_items_with_unresolved_ancestry_count', facts.affected_seeds, 'evidence_item'))
    for field, entities, unit in definitions:
        population = _profile_population(scope, entities, unit,
            'Unique exact supplied IDs after every explicit seed and relevant branch was examined: ' + field, port)
        port.charge(8)
        value = _r._Count(len(entities), population)
        witnesses = _witness_refs(facts, scope, field, entities, port)
        rows.append(_result(facts, family, field, scope, population, value, basis, witnesses, reasons, qualification_cache, port))
    disclosure_rows, entities = [], []
    if family == 'SIT-M002':
        field = 'origin_boundary_disclosures'
        for fact in facts.boundaries:
            port.charge(2)
            entities.append(fact.assessment)
            disclosure_rows.append(_boundary_disclosure(fact, port))
    else:
        field = 'ancestry_gap_disclosures'
        for trace in facts.seed_traces:
            port.charge(1)
            if trace.gaps:
                entities.append(trace.seed)
                disclosure_rows.append(_gap_disclosure(trace, facts.context.dependency_dimension, port))
    population = _profile_population(scope, _unique_entities(facts.prepared, entities, port), 'record',
        'Exact source records with completed owner-local disclosures: ' + field, port)
    port.charge(len(disclosure_rows) + 5)
    value = _r._RecordDisclosures(_tuple(disclosure_rows, port))
    witnesses = _witness_refs(facts, scope, field, entities, port)
    rows.append(_result(facts, family, field, scope, population, value, basis, witnesses, reasons, qualification_cache, port))
    for row in rows:
        _charge_link(row.ref, port)
    port.charge(len(rows) * len(rows) + 4)
    output = _r._ResultSet(_tuple(rows, port)).results
    port.check()
    return output


def _origin_profile(prepared, context, ledger, port, *, family):
    _analysis_port(port)
    port.charge(3)
    _require(type(family) is str and family in ('SIT-M002', 'SIT-M007'))
    facts = _origin_facts(prepared, context, ledger, port)
    results = _origin_results(facts, port, family=family)
    port.charge(5)
    output = _OriginProfile(facts, results, facts.witnesses)
    port.check()
    return output
