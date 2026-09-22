# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: CORRECTION_ROUTES. Paid M011 exact channel/target/action/time queries.

Definitions 27.1 and lineage 6.8/9.7/11.1: finite declared routes and
applicable documentary grants remain separate. No routing action is taken.
"""
from dataclasses import dataclass

from ..contracts.bundle import _require, _Array, _freeze_object
from ..contracts.evidence import _Node
from ..contracts import results as _r
from ..contracts.report import (
    _charge_scope, _charge_input_ref, _charge_link, _charge_frozen,
    _ScopeCheckFact, _scope_check, _PopulationCompletion, _ComponentCompletion,
    _CompletionRecord, _completion_check,
)
from ..validation.structure import _field
from ..validation.semantics import (
    _analysis_start, _analysis_port, _analysis_lookup, _analysis_contains,
    _analysis_subset, _analysis_text, _analysis_address, _analysis_codes,
    _analysis_unique_addresses, _analysis_scope, _analysis_current,
    _analysis_temporal, _time_applicability, _qualify_basis, _qualify_conflicts,
    _qualify_coverage, _profile_ref,
)
from ..graph.projections import _Projection, _GraphEdge, _project, _check_edge_eligibility
from ..graph.traversal import _ranked_search, _path_from_search, _reachable, _node_index
from ..graph.cycles import _components
from ..graph.witnesses import _path_witness, _cycle_witness, _absence_witness
from . import origins as _o
from . import process_comparison as _p

_FIELDS = ('declared_correction_route_witnesses', 'applicable_authorized_route_witnesses',
           'correction_route_disclosures')
_ACTIONS = ('review', 'amend', 'annotate', 'retract', 'rerun', 'rollback',
            'replace_evaluator', 'restrict_scope', 'withdraw', 'metadata_correction', 'other')
_TARGETS = ('claim', 'artifact', 'evidence_item', 'model', 'evaluation',
            'relation', 'assessment', 'unresolved_reference')
_LIMIT = ('Exact supplied channel, target identity/version, action and time only. '
    'A declared path is a routing possibility. Applicable grants remain attributed documentary '
    'evidence without institutional authentication. Neither path demonstrates use, a handled '
    'correction, effect, capacity, independence or universal outside-world reachability. '
    'Cycles and alternative paths do not create additional channels or walk counts.')


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Grant:
    source: object
    channel: object
    native_state: str
    applicable: bool
    state: str
    basis: object
    conflict: object
    time: object
    coverage: object
    reason_codes: tuple


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Leg:
    edge: object
    grants: tuple
    selected_grant: object
    time: object
    state: str
    reason_codes: tuple
    premises: tuple


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _CorrectionFacts:
    prepared: object
    context: object
    job_port: object
    inquiry: object
    channel: object
    target: object
    action: str
    source_graph: object
    declared_graph: object
    authorized_graph: object
    declared_path: object
    authorized_path: object
    declared_reach: object
    grants: tuple
    legs: tuple
    coverage: tuple
    bounded_absence: bool
    authorized_state: str
    authority_check_state: str
    disclosures: tuple
    premises: tuple
    problems: tuple
    pc04: object
    witnesses: tuple
    positive_witnesses: tuple


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _CorrectionProfile:
    facts: _CorrectionFacts
    results: tuple
    witnesses: tuple


def _problem(rows, code, entity, port):
    port.charge(3)
    rows.append((code, _analysis_address(entity, port)))


def _subgraph(graph, edges, port):
    port.charge(len(edges) + 14)
    return _Projection(graph.prepared, graph.context, graph.nodes, _o._tuple(edges, port),
        graph.observations, graph.annotations, None, port)


def _time(window, context, port):
    if context.temporal_basis != 'time_specific':
        port.charge(1)
        return None
    port.charge(2)
    return _time_applicability(_Node('TimeWindow', window), context.requested_time, port)


def _grant(prepared, source, channel, target, action, context, port):
    local = _p._context(context, port, subjects=(channel.identifier,),
                         coverage_kind='correction_routes', view='correction_routing')
    data = _field(source.node.fields, 'data', port)
    details = _field(data, 'details', port)
    basis = _qualify_basis(prepared, source.identifier, local, port)
    conflict = _qualify_conflicts(prepared, source.identifier, local, port)
    timing = _time(_field(details, 'valid_window', port), context, port)
    scoped_time = _analysis_temporal(source, local, port)
    native = _field(details, 'grant_state', port)
    codes, states = [], []
    applicable = (_analysis_scope(source, local, port)
        and _field(source.node.fields, 'lifecycle_state', port) == 'active'
        and _analysis_contains(_field(details, 'target_refs', port).items, target.identifier, port)
        and _analysis_contains(_field(details, 'action_types', port).items, action, port))
    if not applicable:
        codes.append('authority_inapplicable')
    for fact in (timing, scoped_time):
        if fact is None:
            codes.append('time_applicability_unknown')
            states.append('unknown')
        else:
            states.append(fact.state)
            port.charge(len(fact.reason_codes))
            codes.extend(fact.reason_codes)
            if fact.state == 'unmet':
                applicable = False
                codes.append('authority_inapplicable')
    coverage = None
    coverage_ref = _field(details, 'coverage_ref', port)
    if coverage_ref is not None:
        coverage = _analysis_lookup(prepared, coverage_ref, port)
        coverage_local = _p._context(context, port, subjects=(channel.identifier,),
            predicates=('propagates_to',), coverage_kind='correction_routes', view='correction_routing')
        coverage_fact = _qualify_coverage(prepared, (coverage.identifier,), coverage_local, port)[0]
        port.charge(len(coverage_fact.reason_codes))
        codes.extend(coverage_fact.reason_codes)
    else:
        codes.append('upstream_coverage_incomplete')
    authorizer = _analysis_lookup(prepared, _field(details, 'authorized_by_ref', port), port)
    authority_basis = _field(details, 'authority_basis', port)
    if authority_basis is not None:
        _analysis_text(authority_basis, port)
    for fact in (basis, conflict):
        port.charge(len(fact.reason_codes))
        codes.extend(fact.reason_codes)
    documented = (basis.state == 'met' and conflict.state == 'met'
                  and authorizer.kind == 'actor' and bool(authority_basis))
    if native in ('denied', 'expired'):
        codes.append('authority_inapplicable')
    elif native == 'unknown' or not documented:
        codes.append('authority_unestablished')
    state = ('unmet' if not applicable or native in ('denied', 'expired') else
        'met' if native == 'granted' and documented and _p._aggregate(states, port) == 'met'
        else 'unknown')
    port.charge(16)
    return _Grant(source, channel, native, applicable, state, basis, conflict, timing,
                  coverage, _analysis_codes(codes, port))


def _leg(prepared, edge, grants, target, context, port):
    channel = _analysis_lookup(prepared, edge.source.identifier, port)
    local = _p._context(context, port, subjects=(), predicates=('propagates_to',),
                        view='correction_routing')
    premises, codes = [], []
    for source in _o._unique_entities(prepared, (channel, edge.source_entity), port):
        premise = _p._premise(prepared, source, local, premises, port)
        premise_codes = _p._codes(premise, port)
        port.charge(len(premise_codes))
        codes.extend(premise_codes)
    data = _field(channel.node.fields, 'data', port)
    timing = _time(_field(data, 'valid_window', port), context, port)
    if timing is None:
        codes.append('time_applicability_unknown')
    else:
        port.charge(len(timing.reason_codes))
        codes.extend(timing.reason_codes)
    relevant, valid, opposed = [], [], []
    for grant in grants:
        port.charge(2)
        if grant.channel is not channel:
            continue
        relevant.append(grant)
        if grant.state == 'met':
            valid.append(grant)
        if grant.applicable and grant.native_state in ('denied', 'expired'):
            opposed.append(grant)
    if opposed and valid:
        codes.append('premise_disputed')
    documentary = True
    for fact in premises:
        if fact.basis.state != 'met' or fact.conflict.state != 'met' or (
                fact.time is not None and fact.time.state != 'met'):
            documentary = False
    selected = valid[0] if valid else None
    if target.kind == 'unresolved_reference':
        codes.append('unknown_endpoint')
    eligible = (target.kind != 'unresolved_reference' and selected is not None and not opposed and documentary
                and timing is not None and timing.state == 'met')
    if not eligible:
        codes.append('authority_unestablished' if not opposed else 'authority_inapplicable')
    for grant in relevant:
        port.charge(len(grant.reason_codes))
        codes.extend(grant.reason_codes)
    known_inapplicable = bool(opposed) or (timing is not None and timing.state == 'unmet')
    if relevant and not valid:
        port.charge(len(relevant) + 1)
        known_inapplicable = known_inapplicable or all(grant.state == 'unmet' for grant in relevant)
    port.charge(13)
    return _Leg(edge, _o._tuple(relevant, port), selected, timing, 'met' if eligible else
        'unmet' if known_inapplicable else 'unknown', _analysis_codes(codes, port), _o._tuple(premises, port))


def _correction_routes_facts(prepared, context, ledger, port):
    inquiry = _analysis_start(prepared, context, port)
    _p._ledger(ledger, port)
    port.charge(12)
    _require(context.graph_view == 'correction_routing'
        and context.coverage_kind == 'correction_routes'
        and context.relation_types == ('propagates_to',)
        and len(context.subject_refs) == 2 and len(context.operation_anchor) == 1)
    action = context.operation_anchor[0]
    _require(type(action) is str and action in _ACTIONS)
    channel, target = (_analysis_lookup(prepared, identifier, port) for identifier in context.subject_refs)
    _require(channel.kind == 'correction_channel' and
             (target.kind in _TARGETS or target.collection == 'assertions'))
    graph = _project(prepared, context, port)
    start, end = _o._node(graph, channel, port), _o._node(graph, target, port)
    declared, possible, problems = [], [], []
    local = _p._context(context, port, subjects=(), predicates=('propagates_to',),
                        coverage_kind='correction_routes', view='correction_routing')
    for edge in graph.observations:
        source = edge.source_entity
        data = _field(source.node.fields, 'data', port)
        if edge.predicate is None:
            actions = _field(data, 'declared_action_types', port).items
            matches = _analysis_contains(actions, action, port)
            timing = _time(_field(data, 'valid_window', port), context, port)
            possible_scope = True
            times = (timing,)
        else:
            detail = _field(data, 'details', port)
            native_action = _field(detail, 'action_type', port)
            _analysis_text(native_action, port)
            matches = native_action == action
            possible_scope = (_analysis_scope(source, local, port, subjects=False)
                and _field(source.node.fields, 'lifecycle_state', port) == 'active'
                and _field(data, 'polarity', port) == 'affirmed')
            times = (_analysis_temporal(source, local, port),
                     _time(_field(detail, 'valid_window', port), context, port))
        if not matches:
            continue
        if edge.eligible:
            port.charge(1)
            declared.append(edge)
        time_possible = True
        for timing in times:
            port.charge(1)
            if timing is not None and timing.state == 'unmet':
                time_possible = False
        if possible_scope and time_possible and edge.source.kind != 'unresolved_reference':
            port.charge(16)
            possible.append(edge if edge.eligible else _GraphEdge(edge.source, edge.target,
                edge.key, edge.source_ref, edge.predicate, True, edge.reason_codes, source))
    declared_graph = _subgraph(graph, declared, port)
    search = _ranked_search(declared_graph, start, port)
    declared_path = _path_from_search(search, end, port)
    reach = _reachable(declared_graph, (start,), port)
    possible_graph = _subgraph(graph, possible, port)
    possible_reach = _reachable(possible_graph, (start,), port)
    possible_path = _path_from_search(_ranked_search(possible_graph, start, port), end, port)
    involved = [channel, target]
    channels, relevant_edges = [], []
    for node in possible_reach.nodes:
        entity = _analysis_lookup(prepared, node.identifier, port)
        port.charge(2)
        involved.append(entity)
        if entity.kind == 'correction_channel':
            channels.append(entity)
    for edge in possible_reach.observations:
        port.charge(1)
        involved.append(edge.source_entity)
        for code in edge.reason_codes:
            _problem(problems, code, edge.source_entity, port)
    for edge in declared_graph.edges:
        if _node_index(reach.nodes, edge.source, port) >= 0:
            port.charge(1)
            relevant_edges.append(edge)
    grants, coverage = [], []
    for entity in prepared.entities:
        port.charge(2)
        if entity.collection != 'assertions' or _field(entity.node.fields, 'assertion_kind', port) != 'assessment':
            continue
        data = _field(entity.node.fields, 'data', port)
        kind = _field(data, 'assessment_kind', port)
        subjects = _field(data, 'subject_refs', port).items
        if kind == 'authority':
            for owner in channels:
                if not _analysis_contains(subjects, owner.identifier, port):
                    continue
                grant = _grant(prepared, entity, owner, target, action, context, port)
                grants.append(grant)
                involved.append(entity)
                if grant.coverage is not None:
                    involved.append(grant.coverage)
                for code in grant.reason_codes:
                    _problem(problems, code, entity, port)
        elif kind == 'coverage':
            detail = _field(data, 'details', port)
            if (_field(detail, 'coverage_kind', port) != 'correction_routes' or
                not (_analysis_contains(subjects, channel.identifier, port) or
                     _analysis_contains(subjects, inquiry.identifier, port))):
                continue
            local = _p._context(context, port, subjects=(channel.identifier,), predicates=('propagates_to',),
                coverage_kind='correction_routes', view='correction_routing')
            qualified = _qualify_coverage(prepared, (entity.identifier,), local, port)[0]
            port.charge(2)
            coverage.append(qualified)
            involved.append(entity)
            for code in qualified.reason_codes:
                _problem(problems, code, entity, port)
    grants = _o._tuple(grants, port)
    legs, eligible, premises = [], [], []
    for edge in relevant_edges:
        leg = _leg(prepared, edge, grants, target, context, port)
        port.charge(len(leg.premises) + 3)
        legs.append(leg)
        premises.extend(leg.premises)
        if leg.state == 'met':
            eligible.append(edge)
        for code in leg.reason_codes:
            _problem(problems, code, edge.source_entity, port)
    authorized_graph = _subgraph(graph, eligible, port)
    authorized_path = _path_from_search(_ranked_search(authorized_graph, start, port), end, port)
    # A completed empty declared search remains bounded to its supplied graph.
    # Unknown grants for an actual possible route cannot become an authorized zero.
    authorized_state = 'available' if authorized_path is not None else 'unavailable' if (
        possible_path is not None or context.temporal_basis != 'time_specific') else 'available'
    unresolved_legs = []
    for leg in legs:
        port.charge(1)
        if leg.state != 'unmet':
            unresolved_legs.append(leg.edge)
    authority_possible = _path_from_search(_ranked_search(
        _subgraph(graph, unresolved_legs, port), start, port), end, port)
    authority_check_state = ('met' if authorized_path is not None else 'unknown' if
        authority_possible is not None or context.temporal_basis != 'time_specific' or
        declared_path is None and possible_path is not None else 'unmet')
    if declared_path is None:
        _problem(problems, 'route_not_recorded', channel, port)
    if authorized_state == 'unavailable':
        _problem(problems, 'authority_unestablished', channel, port)
    if context.temporal_basis != 'time_specific':
        _problem(problems, 'time_applicability_unknown', channel, port)
    bounded = False
    uncertain_route = declared_path is None and possible_path is not None
    for fact in coverage:
        if fact.state != 'met':
            continue
        detail = _field(_field(fact.coverage.node.fields, 'data', port), 'details', port)
        members = _field(detail, 'member_refs', port).items
        closed = _analysis_contains(members, target.identifier, port)
        for edge in reach.observations:
            if not _analysis_contains(members, edge.target.identifier, port):
                closed = False
            for code in edge.reason_codes:
                port.charge(1)
                if code in ('unknown_endpoint', 'time_applicability_unknown', 'temporal_inconsistency', 'premise_disputed'):
                    closed = False
        if closed and not uncertain_route:
            bounded = True
    if not bounded:
        _problem(problems, 'upstream_coverage_incomplete', channel, port)
    witnesses, positives = [], []
    for meaning, path in (('declared', declared_path), ('authorized', authorized_path)):
        if path is not None:
            witness = _path_witness(path, ledger, port)
            port.charge(3)
            witnesses.append(witness)
            positives.append((meaning, witness))
    if declared_path is None:
        witnesses.append(_absence_witness(reach, end, ledger, port))
    # Retain canonical cycles in the reached supplied view, never walk counts.
    cycle_edges = []
    for edge in declared_graph.edges:
        if _node_index(reach.nodes, edge.source, port) >= 0:
            cycle_edges.append(edge)
    for component in _components(_subgraph(declared_graph, cycle_edges, port), port):
        if component.cycle is not None:
            witnesses.append(_cycle_witness(component, ledger, port))
    # All support and conflict sources stay addressable in the disclosure set.
    basis_context = _p._context(context, port, subjects=(), predicates=('propagates_to',), view='correction_routing')
    for entity in _o._unique_entities(prepared, involved, port):
        if entity.collection == 'evidence_references':
            continue
        premise = _p._premise(prepared, entity, basis_context, premises, port)
        for fact in (premise.basis, premise.conflict):
            for address in fact.support_refs:
                involved.append(_analysis_lookup(prepared, address.record_id, port))
    relied = () if declared_path is None else declared_path.edges
    pc04 = _check_edge_eligibility(graph, relied, port)
    port.charge(40)
    facts = _CorrectionFacts(prepared, context, port, inquiry, channel, target, action, graph,
        declared_graph, authorized_graph, declared_path, authorized_path, reach, grants,
        _o._tuple(legs, port), _o._tuple(coverage, port), bounded, authorized_state, authority_check_state,
        _o._unique_entities(prepared, involved, port), _o._tuple(premises, port),
        _o._tuple(problems, port), pc04, _o._tuple(witnesses, port), _o._tuple(positives, port))
    port.check()
    return facts


def _scope(facts, port):
    claims, coverages = [], []
    for identifier in facts.context.claim_refs:
        claims.append(_profile_ref(_analysis_lookup(facts.prepared, identifier, port), port))
    for fact in facts.coverage:
        coverages.append(_profile_ref(fact.coverage, port))
    targets = (_profile_ref(facts.channel, port), _profile_ref(facts.target, port))
    for refs in (claims, coverages, targets):
        for ref in refs:
            _charge_input_ref(ref, port, repeats=len(refs) + 3)
    if facts.context.requested_time is not None:
        _charge_frozen(facts.context.requested_time.fields, port)
    port.charge(24)
    return _r._Scope(_profile_ref(facts.inquiry, port), _o._tuple(claims, port), targets,
        facts.context.dependency_dimension, 'correction_routing', facts.context.temporal_basis,
        facts.context.requested_time, _o._tuple(coverages, port), (_LIMIT,), (facts.action,))


def _disclosures(facts, port):
    rows = []
    for entity in facts.disclosures:
        native = _p._native_fields(facts.prepared, entity, port)
        _charge_frozen(native, port)
        fields = [('native_record', native)]
        if entity is facts.channel:
            fields.extend((('target_ref', facts.target.identifier), ('action_type', facts.action),
                ('declared_route_recorded', facts.declared_path is not None),
                ('authorized_route_recorded', facts.authorized_path is not None),
                ('authorized_route_state', facts.authorized_state),
                ('absence_description', 'bounded_absence_under_declared_coverage' if
                 facts.declared_path is None and facts.bounded_absence else
                 'no_witness_in_examined_view' if facts.declared_path is None else 'positive_witness')))
        for grant in facts.grants:
            port.charge(1)
            if grant.source is entity:
                port.charge(len(grant.reason_codes) + 5)
                fields.extend((('grant_qualification_state', grant.state),
                    ('grant_matches_tuple', grant.applicable),
                    ('grant_reason_codes', _Array(grant.reason_codes))))
        frozen = _freeze_object(fields, port)
        port.charge(6)
        rows.append(_r._Disclosure(_profile_ref(entity, port), frozen, (_LIMIT,)))
    port.charge(len(rows) + 3)
    return _r._RecordDisclosures(_o._tuple(rows, port))


def _reasons(facts, scope, ref, port):
    rows = []
    for code in _r.REASON_CODES:
        addresses = []
        for candidate, address in facts.problems:
            port.charge(1)
            if candidate == code:
                addresses.append(address)
        if not addresses:
            continue
        refs = []
        for address in _analysis_unique_addresses(_o._tuple(addresses, port), port):
            refs.append(_o._source_ref(address, port))
        for source in refs:
            _charge_input_ref(source, port, repeats=len(refs) + 3)
        for unused in range(3):
            _charge_scope(scope, port)
        port.charge(len(refs) + 15)
        rows.append(_r._Reason(code, scope, (ref,), _o._tuple(refs, port),
            'Exact route/leg or disclosed alternative limitation; a positive eligible witness survives unrelated gaps.',
            'conflict' if code == 'premise_disputed' else 'evidence_gap'))
    return _o._tuple(rows, port)


def _checks(facts, ref, port):
    checks = [_scope_check(_ScopeCheckFact(ref, ref.scope), port)]
    sources = (_analysis_address(facts.channel, port), _analysis_address(facts.target, port))
    rows = [('PC01', 'met', ()), ('PC04', facts.pc04.state, facts.pc04.input_refs),
        ('PC06', 'met' if facts.bounded_absence else 'unknown', sources),
        ('PC19', 'met' if facts.declared_path is not None else 'unmet', sources),
        ('PC20', facts.authority_check_state, sources)]
    selected = []
    path = (facts.authorized_path or facts.declared_path) if ref.field_key == _FIELDS[1] else facts.declared_path
    grant_conflict = False
    required_times = []
    if path is not None:
        for leg in facts.legs:
            for edge in path.edges:
                port.charge(1)
                if edge is leg.edge:
                    port.charge(len(leg.premises))
                    selected.extend(leg.premises)
                    if ref.field_key == _FIELDS[1]:
                        port.charge(2)
                        required_times.append('unknown' if leg.time is None else leg.time.state)
                        grant_conflict = grant_conflict or (leg.state != 'met' and
                            _analysis_contains(leg.reason_codes, 'premise_disputed', port))
                        for grant in leg.grants:
                            if grant is not leg.selected_grant and leg.state == 'met':
                                continue
                            port.charge(2)
                            required_times.append('unknown' if grant.time is None else grant.time.state)
                            for fact in facts.premises:
                                port.charge(2)
                                if fact.source is grant.source:
                                    selected.append(fact)
    for check, state, addresses, unused in _p._premise_checks(_o._tuple(selected, port), port):
        if check == 'PC09' and grant_conflict:
            state = 'unmet'
        if check == 'PC10' and ref.field_key == _FIELDS[1]:
            if facts.context.temporal_basis != 'time_specific':
                state = 'unknown'
            elif required_times:
                port.charge(len(required_times) + 1)
                state = _p._aggregate((state,) + _o._tuple(required_times, port), port)
        rows.append((check, state, addresses))
    for check, state, addresses in rows:
        refs = []
        for address in _analysis_unique_addresses(addresses, port):
            refs.append(_o._source_ref(address, port))
        for source in refs:
            _charge_input_ref(source, port, repeats=len(refs) + 3)
        port.charge(len(refs) + 12)
        checks.append(_r._PrerequisiteCheck(check, ref, state, _o._tuple(refs, port), (),
            'Executed exact route question. Positive routes do not require complete outside coverage; grants remain attributed.'))
    return checks


def _correction_routes_results(facts, port):
    _analysis_port(port)
    port.charge(4)
    _require(type(facts) is _CorrectionFacts and facts.job_port is port)
    scope = _scope(facts, port)
    addresses = []
    for entity in facts.disclosures:
        addresses.append(_analysis_address(entity, port))
    basis = []
    for address in _analysis_unique_addresses(_o._tuple(addresses, port), port):
        source = _o._source_ref(address, port)
        _charge_input_ref(source, port)
        port.charge(3)
        basis.append(_r._BasisRef(source))
    basis = _o._tuple(basis, port)
    witness_rows = []
    for index, witness in enumerate(facts.witnesses):
        meaning = witness.kind
        for selected, candidate in facts.positive_witnesses:
            port.charge(1)
            if candidate is witness:
                meaning = selected
        _charge_scope(scope, port)
        port.charge(8)
        link = _r._WitnessRef(scope, 'path' if witness.kind == 'path' else
            'cycle' if witness.kind == 'cycle' else 'member_set', (meaning, str(index)))
        witness_rows.append((meaning, link))
    outputs = []
    for field in _FIELDS:
        _charge_scope(scope, port)
        port.charge(160)
        ref = _r._ResultRef('SIT-M011', field, scope)
        witnesses, positives = [], []
        meaning = 'declared' if field == _FIELDS[0] else 'authorized'
        for selected, link in witness_rows:
            port.charge(2)
            if field == _FIELDS[2] or selected == meaning or selected not in ('declared', 'authorized'):
                witnesses.append(link)
            if selected == meaning:
                positives.append(link)
        witnesses = _o._tuple(witnesses if field == _FIELDS[2] else positives, port)
        members = (_profile_ref(facts.channel, port), _profile_ref(facts.target, port))
        for member in members:
            _charge_input_ref(member, port, repeats=5)
        port.charge(24)
        population = _r._Population(scope, 'record', members,
            'One explicitly represented channel/target/action/time question; paths do not multiply channel or target identities.',
            (), (), 'enumerated_for_scope', (_LIMIT,))
        state = facts.authorized_state if field == _FIELDS[1] else 'available'
        if state != 'available':
            value = None
        elif field == _FIELDS[2]:
            value = _disclosures(facts, port)
        else:
            port.charge(len(positives) * len(positives) + 4)
            value = _r._WitnessCollection(_o._tuple(positives, port))
        reasons = _reasons(facts, scope, ref, port)
        checks = _checks(facts, ref, port)
        components = []
        for name, links in (('premises', members), ('conflicts', reasons), ('value', (ref,)),
                            ('basis', basis), ('reasons', reasons), ('witnesses', witnesses)):
            for link in links:
                for unused in range(3):
                    _charge_link(link, port)
            port.charge(len(links) * len(links) + 10)
            components.append(_ComponentCompletion(name, links, links))
        for unused in range(3):
            _charge_link(population, port)
        port.charge(24)
        completion = _CompletionRecord(ref, (population,), (_PopulationCompletion(population, members),),
            _o._tuple(components, port))
        checks.append(_completion_check(completion, port))
        for unused in range(2):
            _charge_link(ref, port)
            _charge_link(population, port)
            for links in (checks, basis, witnesses, reasons):
                for link in links:
                    _charge_link(link, port)
        port.charge(len(checks) + len(basis) + len(witnesses) + len(reasons) + 32)
        outputs.append(_r._Result(ref, (population,), 'completed', state,
            'attributed_record' if field == _FIELDS[2] else 'graph_derivation',
            _r._field_kind('SIT-M011', field), value, _o._tuple(checks, port),
            basis, witnesses, reasons, _LIMIT))
    result = _o._tuple(outputs, port)
    port.check()
    return result


def _correction_routes(prepared, context, ledger, port):
    facts = _correction_routes_facts(prepared, context, ledger, port)
    results = _correction_routes_results(facts, port)
    port.charge(4)
    result = _CorrectionProfile(facts, results, facts.witnesses)
    port.check()
    return result
