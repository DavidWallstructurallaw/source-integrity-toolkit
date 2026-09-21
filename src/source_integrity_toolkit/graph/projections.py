# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: GRAPH_VIEW_CONTRACT.

Private finite typed views over admitted immutable records. Projection is a
mechanical scoped eligibility decision, never an origin, truth, independence,
authority or documentary qualification. Canonical link identity uses source
field/role and target identity, never a normalized array position.
"""
from dataclasses import dataclass

from ..contracts.bundle import _require, _compare_text, _lookup_pair
from ..contracts.evidence import (
    _Entity, _PreparedBundle, _QualificationContext, _ProviderFact,
    _SourceAddress, _Node,
)
from ..contracts.execution import _byte_work
from ..validation.structure import _field
from ..validation.semantics import (
    _analysis_port, _analysis_lookup, _analysis_start, _analysis_current,
    _analysis_scope, _analysis_temporal, _qualify_conflicts, _time_applicability,
    _analysis_codes, _analysis_text,
)


_GRAPH_VIEWS = (
    'citation', 'material_transformation', 'claim_origin', 'model_evaluation',
    'organizational', 'stance_contestation', 'correction_routing',
    'correction_outcomes', 'pipeline_stages', 'assertion_assurance', 'succession',
)
_TRANSFORMS = ('derived_from', 'copies', 'syndicated_from', 'summarizes', 'translates', 'quotes')
_STANCES = ('supports', 'contradicts', 'describes', 'qualifies', 'contextualizes', 'corroborates')


@dataclass(frozen=True, slots=True, repr=False)
class _GraphNode:
    collection: str
    identifier: str
    kind: str
    key: tuple

    def __post_init__(self):
        _require(type(self.collection) is str and self.collection in
                 ('inquiries', 'records', 'assertions', 'evidence_references'))
        _require(type(self.identifier) is str and bool(self.identifier))
        _require(type(self.kind) is str and bool(self.kind))
        _require(type(self.key) is tuple and len(self.key) == 2 and
                 all(type(part) is str for part in self.key) and
                 self.key == (self.collection, self.identifier))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _GraphEdge:
    source: _GraphNode
    target: _GraphNode
    key: tuple
    source_ref: _SourceAddress
    predicate: str | None
    eligible: bool
    reason_codes: tuple
    source_entity: _Entity | None = None

    def __post_init__(self):
        _require(type(self.source) is _GraphNode and type(self.target) is _GraphNode)
        _require(type(self.key) is tuple and len(self.key) == 5 and
                 all(type(part) is str for part in self.key))
        _require(type(self.source_ref) is _SourceAddress)
        _require(self.key == (self.source_ref.collection, self.source_ref.record_id,
                             self.source_ref.selector, self.target.collection, self.target.identifier))
        _require(self.predicate is None or type(self.predicate) is str)
        _require(type(self.eligible) is bool and type(self.reason_codes) is tuple)
        _require(all(type(code) is str for code in self.reason_codes))
        _require(self.source_entity is None or type(self.source_entity) is _Entity)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Projection:
    """Frozen job-local representation; construction does not prove execution."""
    prepared: _PreparedBundle
    context: _QualificationContext
    nodes: tuple
    edges: tuple
    observations: tuple
    annotations: tuple
    pc04: _ProviderFact | None
    job_port: object

    def __post_init__(self):
        _require(type(self.prepared) is _PreparedBundle and type(self.context) is _QualificationContext)
        _require(self.context.graph_view in _GRAPH_VIEWS)
        for rows, kind in ((self.nodes, _GraphNode), (self.edges, _GraphEdge),
                           (self.observations, _GraphEdge), (self.annotations, _Entity)):
            _require(type(rows) is tuple and all(type(row) is kind for row in rows))
        _require(all(edge.eligible for edge in self.edges))
        _require(self.pc04 is None or (type(self.pc04) is _ProviderFact and
                 self.pc04.check_id == 'PC04' and self.pc04.prepared is self.prepared and
                 self.pc04.context is self.context))


def _compare_key(left, right, port):
    """Scalar-value lexical order of a stored finite string key, fully paid."""
    _require(type(left) is tuple and type(right) is tuple)
    for a, b in zip(left, right):
        port.charge(2)
        result = _compare_text(a, b, port)
        if result:
            return result
    port.charge(2)
    return (len(left) > len(right)) - (len(left) < len(right))


def _graph_sort(rows, port, key_kind='edge'):
    """Stable bottom-up merge ordering of existing immutable graph entries."""
    _analysis_port(port)
    _require(type(rows) is tuple and key_kind in ('node', 'edge'))
    kind = _GraphNode if key_kind == 'node' else _GraphEdge
    for row in rows:
        port.charge(1)
        _require(type(row) is kind)
    port.charge(len(rows) + 2)
    current = list(rows)
    width = 1
    while width < len(current):
        port.charge(len(current) + 1)
        merged = [None] * len(current)
        for start in range(0, len(current), 2 * width):
            port.charge(4)
            mid, stop = min(start + width, len(current)), min(start + 2 * width, len(current))
            left, right, output = start, mid, start
            while left < mid or right < stop:
                port.charge(3)
                if right == stop or (left < mid and _compare_key(current[left].key, current[right].key, port) <= 0):
                    merged[output] = current[left]
                    left += 1
                else:
                    merged[output] = current[right]
                    right += 1
                output += 1
        current = merged
        port.charge(1)
        width *= 2
    port.charge(len(current) + 1)
    result = tuple(current)
    port.check()
    return result


def _check_projection(projection, port):
    _analysis_port(port)
    port.charge(2)
    _require(type(projection) is _Projection and projection.job_port is port)


def _node_key(node):
    return node.key


def _edge_key(edge):
    return edge.key


def _graph_node(entity, port):
    for text in (entity.collection, entity.identifier, entity.kind):
        _analysis_text(text, port)
    port.charge(12)
    return _GraphNode(entity.collection, entity.identifier, entity.kind,
                      (entity.collection, entity.identifier))


def _find_node(nodes, identifier, port):
    low, high = 0, len(nodes)
    while low < high:
        port.charge(3)
        middle = (low + high) // 2
        comparison = _compare_text(nodes[middle].identifier, identifier, port)
        if comparison < 0:
            low = middle + 1
        elif comparison > 0:
            high = middle
        else:
            return nodes[middle]
    raise TypeError('unknown_private_graph_node')


def _graph_context(context, port):
    # Query subjects are roots/targets, not a filter on every intermediate edge.
    for values in (context.claim_refs, context.relation_types, context.operation_anchor):
        port.charge(len(values) + 1)
        for value in values:
            if type(value) is str:
                _analysis_text(value, port)
                _analysis_text(value, port)
                port.charge(3)
            elif type(value) is _SourceAddress:
                for text in (value.collection, value.record_id, value.selector):
                    _analysis_text(text, port)
    port.charge(14)
    return _QualificationContext(context.inquiry_ref, context.claim_refs, (),
        context.dependency_dimension, context.temporal_basis, context.requested_time,
        context.coverage_kind, context.relation_types, context.graph_view, context.operation_anchor)


def _relation_view(predicate, dimension):
    if predicate == 'cites':
        return 'citation'
    if predicate in _TRANSFORMS:
        return 'material_transformation' if dimension is None else 'claim_origin'
    if predicate == 'retrieved_from':
        return 'material_transformation'
    if predicate in ('originates_from', 'depends_on'):
        return 'claim_origin'
    if predicate in ('generated_by', 'model_derived_from', 'trained_on'):
        return 'model_evaluation'
    if predicate == 'owned_by':
        return 'organizational'
    if predicate in _STANCES:
        return 'stance_contestation'
    if predicate == 'propagates_to':
        return 'correction_routing'
    if predicate == 'supersedes':
        return 'succession'
    return None


def _native_selector(link, port):
    """Retain role identity while removing array occurrence identity."""
    text = link.selector
    _analysis_text(text, port)
    if text.startswith('data.role_bindings['):
        port.charge(8)
        close = text.index(']')
        index_text = text[len('data.role_bindings['):close]
        _byte_work(port, len(index_text), 2)
        index = int(index_text)
        data = _field(link.owner.node.fields, 'data', port)
        roles = _field(data, 'role_bindings', port).items
        port.charge(2)
        role = _field(roles[index], 'role', port)
        object_ref = _field(roles[index], 'object_ref', port)
        suffix = text[close + 1:]
        _analysis_text(role, port)
        _analysis_text(suffix, port)
        port.charge(len(role) + len(suffix) + 4)
        if suffix.startswith('.evidence_ref_ids'):
            _analysis_text(object_ref, port)
            port.charge(len(object_ref) + 16)
            # Admitted IDs use only ASCII alnum/._:- and role is an enum;
            # these delimiters therefore cannot collide with either identity.
            selector = ('data.role_bindings[role=' + role + ';object_ref=' +
                        object_ref + '].evidence_ref_ids')
        else:
            selector = 'data.role_bindings[role=' + role + ']' + suffix.split('[')[0]
    else:
        port.charge(len(text) + 1)
        selector = text.split('[')[0]
    port.check()
    return selector


def _record_view(owner, selector, port):
    """Only fields named by Lineage 10.2/18.2 become directed links."""
    if selector == 'provenance.evidence_ref_ids':
        return 'assertion_assurance'
    if selector.startswith('data.role_bindings[role=') and selector.endswith('].evidence_ref_ids'):
        return 'assertion_assurance'
    if owner.collection == 'evidence_references' and selector == 'record_ref':
        return 'assertion_assurance'
    if owner.kind == 'evaluation' and (selector.startswith('data.role_bindings[role=') and
                                      selector.endswith('].object_ref') or
                                      selector in ('data.target_refs', 'data.result_refs')):
        return 'model_evaluation'
    if ((owner.kind == 'origin_event' and selector == 'data.performed_by_refs') or
            (owner.kind == 'model' and selector == 'data.provider_ref') or
            (owner.kind == 'correction_channel' and selector == 'data.owner_refs')):
        return 'organizational'
    if owner.kind == 'correction_channel' and selector == 'data.target_refs':
        return 'correction_routing'
    if owner.kind == 'correction_event' and selector in (
            'data.case_ref', 'data.channel_ref', 'data.target_refs',
            'data.details.before_ref', 'data.details.after_ref'):
        return 'correction_outcomes'
    if owner.kind == 'pipeline_record' and selector in ('data.subject_ref', 'data.output_refs'):
        return 'pipeline_stages'
    if owner.collection == 'assertions':
        obj = owner.node.fields
        if _field(obj, 'assertion_kind', port) != 'assessment':
            return None
        data = _field(obj, 'data', port)
        kind = _field(data, 'assessment_kind', port)
        if kind in ('classification', 'conflict') and selector == 'data.subject_refs':
            return 'stance_contestation'
        if kind == 'verification' and selector in ('data.subject_refs', 'data.details.evaluation_ref'):
            return 'assertion_assurance'
    return None


def _record_scope(prepared, entity, context, port):
    if entity.collection == 'assertions':
        return _analysis_scope(entity, context, port, subjects=False)
    if entity.collection == 'inquiries':
        return _compare_text(entity.identifier, context.inquiry_ref, port) == 0
    if entity.kind == 'evidence_item':
        claim = _field(_field(entity.node.fields, 'data', port), 'claim_ref', port)
        for selected in context.claim_refs:
            if _compare_text(claim, selected, port) == 0:
                return True
        return False
    if entity.kind == 'anomaly':
        data = _field(entity.node.fields, 'data', port)
        for inquiry in _field(data, 'inquiry_refs', port).items:
            if _compare_text(inquiry, context.inquiry_ref, port) == 0:
                return True
        return False
    # Other native records carry no invented Inquiry/Claim binding. Their
    # disconnected links are snapshot inventory, never a domain population.
    return True


def _record_time(prepared, owner, context, port):
    if context.temporal_basis == 'snapshot_structural':
        return True, ()
    if owner.collection == 'assertions':
        timing = _analysis_temporal(owner, context, port)
    elif owner.kind == 'correction_channel':
        data = _field(owner.node.fields, 'data', port)
        timing = _time_applicability(_Node('TimeWindow', _field(data, 'valid_window', port)),
                                     context.requested_time, port)
    else:
        return False, ('time_applicability_unknown',)
    return timing.state == 'met', timing.reason_codes


def _edge_scope(prepared, owner, source, target, context, port):
    compatible = _record_scope(prepared, owner, context, port)
    # A multi-Claim assertion scope does not rebind an actual contribution.
    # Keep Claim version transitions intact: this tests EvidenceItem bindings,
    # not equality of arbitrary endpoint IDs or query root membership.
    for node in (source, target):
        port.charge(2)
        if node.kind == 'evidence_item':
            endpoint = _analysis_lookup(prepared, node.identifier, port)
            if not _record_scope(prepared, endpoint, context, port):
                compatible = False
    return compatible


def _make_edge(owner, source, target, selector, predicate, eligible, codes, port):
    for text in (owner.collection, owner.identifier, selector,
                 target.collection, target.identifier):
        _analysis_text(text, port)
    for code in codes:
        _analysis_text(code, port)
    port.charge(len(codes) + 24)
    address = _SourceAddress(owner.collection, owner.identifier, selector)
    key = (owner.collection, owner.identifier, selector, target.collection, target.identifier)
    return _GraphEdge(source, target, key, address, predicate, eligible, codes, owner)


def _project(prepared, context, port):
    """Project only one explicit view; retain all mapped eligibility decisions.

    All source records remain in prepared. Observations retain denied,
    inactive, temporally uncertain and disputed candidates beside positive
    edges. Projection completion creates no PC04 fact; callers select actual
    relied-on edges for _check_edge_eligibility. Neither operation certifies
    documentary qualification, exhaustive outside history or truth.
    """
    _analysis_start(prepared, context, port)
    _require(context.graph_view in _GRAPH_VIEWS)
    if context.graph_view == 'claim_origin':
        _require(context.dependency_dimension is not None and len(context.claim_refs) == 1)
    local = _graph_context(context, port)
    all_nodes = []
    for entity in prepared.entities:
        port.charge(1)
        all_nodes.append(_graph_node(entity, port))
    port.charge(len(all_nodes) + 1)
    all_nodes = tuple(all_nodes)
    observations, annotations, used_nodes = [], [], []
    for identifier in context.subject_refs:
        port.charge(1)
        used_nodes.append(_find_node(all_nodes, identifier, port))
    for entity in prepared.entities:
        port.charge(2)
        if entity.collection != 'assertions':
            continue
        obj = entity.node.fields
        if _field(obj, 'assertion_kind', port) != 'relation':
            if _analysis_scope(entity, local, port, subjects=False):
                port.charge(1)
                annotations.append(entity)
            continue
        data = _field(obj, 'data', port)
        predicate, dimension = _field(data, 'predicate', port), _field(data, 'dimension', port)
        _analysis_text(predicate, port)
        port.charge(24)
        if _relation_view(predicate, dimension) != context.graph_view:
            if predicate in ('published_by', 'same_identity_as') and _analysis_scope(
                    entity, local, port, subjects=False, relation_types=False):
                port.charge(1)
                annotations.append(entity)
            continue
        selected = False
        for requested in context.relation_types:
            port.charge(1)
            if _compare_text(predicate, requested, port) == 0:
                selected = True
        if not selected:
            continue
        source = _find_node(all_nodes, _field(data, 'from_ref', port), port)
        target = _find_node(all_nodes, _field(data, 'to_ref', port), port)
        compatible = _edge_scope(prepared, entity, source, target, local, port)
        codes = []
        if not compatible:
            codes.append('scope_unestablished')
        lifecycle = _field(obj, 'lifecycle_state', port)
        positive = _field(data, 'polarity', port) == 'affirmed'
        current = lifecycle == 'active'
        if not current:
            unused, uncertain = _analysis_current(prepared, entity, port)
            if uncertain:
                codes.append('documentary_basis_incomplete')
        timing = _analysis_temporal(entity, local, port)
        time_ok = timing is None or timing.state == 'met'
        if timing is not None:
            port.charge(len(timing.reason_codes))
            codes.extend(timing.reason_codes)
        if context.temporal_basis == 'time_specific':
            details = _field(data, 'details', port)
            window = _lookup_pair(details.items, 'valid_window', port)
            if window is not None:
                role_time = _time_applicability(_Node('TimeWindow', window[1]), context.requested_time, port)
                time_ok = time_ok and role_time.state == 'met'
                port.charge(len(role_time.reason_codes))
                codes.extend(role_time.reason_codes)
        if compatible:
            conflict = _qualify_conflicts(prepared, entity.identifier, local, port)
            port.charge(len(conflict.reason_codes))
            codes.extend(conflict.reason_codes)
        if source.kind == 'unresolved_reference' or target.kind == 'unresolved_reference':
            codes.append('unknown_endpoint')
        eligible = compatible and current and positive and time_ok and source.kind != 'unresolved_reference'
        port.charge(4)
        observations.append(_make_edge(entity, source, target, '', predicate, eligible,
                                        _analysis_codes(codes, port), port))
        used_nodes.extend((source, target))
    for link in prepared.links:
        port.charge(2)
        selector = _native_selector(link, port)
        port.charge(14)
        mapped = _record_view(link.owner, selector, port)
        # Conflict assessments are contextual links in both registry views.
        shared_conflict = (context.graph_view == 'assertion_assurance' and
                           mapped == 'stance_contestation' and link.owner.collection == 'assertions' and
                           _field(_field(link.owner.node.fields, 'data', port), 'assessment_kind', port) == 'conflict')
        shared_actor_role = (context.graph_view == 'organizational' and link.owner.kind == 'evaluation' and
                             selector.startswith('data.role_bindings[role=') and selector.endswith('].object_ref') and
                             link.target.kind in ('actor', 'model', 'unresolved_reference'))
        if mapped != context.graph_view and not shared_conflict and not shared_actor_role:
            continue
        source, target = _find_node(all_nodes, link.owner.identifier, port), _find_node(all_nodes, link.target.identifier, port)
        compatible = _edge_scope(prepared, link.owner, source, target, local, port)
        codes = [] if compatible else ['scope_unestablished']
        current = True
        if link.owner.collection == 'assertions':
            current = _field(link.owner.node.fields, 'lifecycle_state', port) == 'active'
            if not current:
                unused, uncertain = _analysis_current(prepared, link.owner, port)
                if uncertain:
                    codes.append('documentary_basis_incomplete')
        time_ok, time_codes = _record_time(prepared, link.owner, local, port)
        port.charge(len(time_codes))
        codes.extend(time_codes)
        if source.kind == 'unresolved_reference' or target.kind == 'unresolved_reference':
            codes.append('unknown_endpoint')
        eligible = compatible and current and time_ok and source.kind != 'unresolved_reference'
        port.charge(4)
        observations.append(_make_edge(link.owner, source, target, selector, None, eligible,
                                        _analysis_codes(codes, port), port))
        used_nodes.extend((source, target))
    port.charge(len(observations) + len(used_nodes) + 2)
    ordered_with_occurrences = _graph_sort(tuple(observations), port)
    unique_edges = []
    for edge in ordered_with_occurrences:
        port.charge(2)
        if not unique_edges or _compare_key(unique_edges[-1].key, edge.key, port):
            unique_edges.append(edge)
        else:
            # Duplicate role slots can be valid input. Their entire original
            # record (including every slot/qualification) remains source_entity;
            # the same semantic field/role/target is one canonical graph link.
            _require(edge.source_entity is unique_edges[-1].source_entity)
    port.charge(len(unique_edges) + 1)
    ordered = tuple(unique_edges)
    sorted_nodes = _graph_sort(tuple(used_nodes), port, 'node')
    nodes = []
    for node in sorted_nodes:
        port.charge(2)
        if not nodes or _compare_key(nodes[-1].key, node.key, port):
            nodes.append(node)
    edges = []
    for edge in ordered:
        port.charge(2)
        if edge.eligible:
            edges.append(edge)
    port.charge(len(nodes) + len(edges) + len(ordered) + len(annotations) + 18)
    result = _Projection(prepared, context, tuple(nodes), tuple(edges), ordered, tuple(annotations), None, port)
    port.check()
    return result


def _selected_edge(projection, requested, port):
    _require(type(requested) is _GraphEdge)
    low, high = 0, len(projection.observations)
    while low < high:
        port.charge(3)
        middle = (low + high) // 2
        edge = projection.observations[middle]
        comparison = _compare_key(edge.key, requested.key, port)
        if comparison < 0:
            low = middle + 1
        elif comparison > 0:
            high = middle
        else:
            _require(edge is requested)
            return edge
    raise TypeError('edge_not_in_this_projection')


def _check_edge_eligibility(projection, selected_edges, port):
    """PC04 for the actual relied-on edge set, separate from PC05/08/09/10.

    Projection completion supplies no provider fact. Conflicts, documentary
    gaps and unresolved identities remain separate qualifications; a met PC04
    does not certify uncontested evidence, a known origin or complete history.
    """
    _check_projection(projection, port)
    _require(type(selected_edges) is tuple)
    local = _graph_context(projection.context, port)
    states, addresses, previous = [], [], None
    ordered = _graph_sort(selected_edges, port)
    for candidate in ordered:
        edge = _selected_edge(projection, candidate, port)
        if previous is not None and _compare_key(previous.key, edge.key, port) == 0:
            continue
        previous = edge
        owner = _analysis_lookup(projection.prepared, edge.source_ref.record_id, port)
        _require(owner is edge.source_entity)
        compatible = _edge_scope(projection.prepared, owner, edge.source, edge.target, local, port)
        state = 'met'
        if not compatible:
            state = 'unmet'
        elif owner.collection == 'assertions':
            obj = owner.node.fields
            if _field(obj, 'assertion_kind', port) == 'relation':
                data = _field(obj, 'data', port)
                if _field(data, 'polarity', port) != 'affirmed':
                    state = 'unmet'
            if state == 'met' and _field(obj, 'lifecycle_state', port) != 'active':
                state = 'unmet'
        if state == 'met' and projection.context.temporal_basis == 'time_specific':
            if owner.collection == 'assertions':
                timing = _analysis_temporal(owner, local, port)
                state = timing.state
                if state == 'met' and _field(owner.node.fields, 'assertion_kind', port) == 'relation':
                    details = _field(_field(owner.node.fields, 'data', port), 'details', port)
                    window = _lookup_pair(details.items, 'valid_window', port)
                    if window is not None:
                        state = _time_applicability(_Node('TimeWindow', window[1]), local.requested_time, port).state
            elif owner.kind == 'correction_channel':
                window = _field(_field(owner.node.fields, 'data', port), 'valid_window', port)
                state = _time_applicability(_Node('TimeWindow', window), local.requested_time, port).state
            else:
                state = 'unknown'
        port.charge(3)
        states.append(state)
        address = edge.source_ref
        port.charge(8)
        if not addresses or _compare_key(
                (addresses[-1].collection, addresses[-1].record_id, addresses[-1].selector),
                (address.collection, address.record_id, address.selector), port):
            port.charge(1)
            addresses.append(address)
    port.charge(len(states) * 2 + 2)
    state = 'unmet' if 'unmet' in states else 'unknown' if 'unknown' in states else 'met' if states else 'not_applicable'
    for address in addresses:
        for text in (address.collection, address.record_id, address.selector):
            _analysis_text(text, port)
            _analysis_text(text, port)
        port.charge(12)
    port.charge(len(addresses) + 14)
    result = _ProviderFact('PC04', 'GRAPH_VIEW_CONTRACT', projection.context, state,
                           tuple(addresses), projection.prepared)
    port.check()
    return result
