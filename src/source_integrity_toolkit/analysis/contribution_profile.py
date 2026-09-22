# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: CONTRIBUTION_PROFILE. Private paid M004/M005/M006 finite profiles.

Definitions 22--24: preserve every seed and positive incidence, qualify the
whole HHI population, and keep immediate inheritance independent of distant
ancestry. Exact components remain unreduced. No public runner or allocation.
"""
from dataclasses import dataclass

from ..contracts.bundle import _require
from ..contracts.evidence import _PreparedBundle, _QualificationContext
from ..contracts import results as _r
from ..contracts.report import (
    _charge_scope, _charge_input_ref, _charge_link, _ScopeCheckFact, _scope_check,
    _PopulationCompletion, _ComponentCompletion, _CompletionRecord, _completion_check,
)
from ..validation.structure import _field
from ..validation.semantics import (
    _analysis_port, _analysis_start, _analysis_lookup, _analysis_contains,
    _analysis_subset, _analysis_codes, _analysis_scope, _analysis_temporal,
    _analysis_current, _qualify_basis, _qualify_conflicts, _qualify_identity, _qualify_coverage,
    _profile_ref, _profile_population,
)
from ..graph.projections import _project, _check_projection, _check_edge_eligibility
from ..graph.witnesses import _check_ledger, _GraphWitness, _charge_node, _charge_edge
from .inventory import _inventory_facts, _check_inventory
from . import origins as _o

_FAMILIES = ('SIT-M004', 'SIT-M005', 'SIT-M006')
_IMMEDIATE = _o._EVIDENCE_PARENTS


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _ContributionRow:
    seed: object
    disposition: str
    documentary_origins: tuple
    reason_codes: tuple
    origin_trace: object = None
    immediate_edges: tuple = ()
    coverage: tuple = ()
    identities: tuple = ()


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _ImmediateCoverage:
    coverage: object
    state: str
    reason_codes: tuple
    basis: object
    conflict: object
    timing: object
    premise: object


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _ContributionFacts:
    prepared: _PreparedBundle
    context: _QualificationContext
    job_port: object
    family: str
    inventory: object
    graph: object
    origin_facts: object
    seed_rows: tuple
    bucket_counts: tuple
    hhi_eligible: bool
    pc04: object
    qualification_facts: tuple
    reason_sources: tuple
    basis_entities: tuple
    witnesses: tuple

    def __post_init__(self):
        _require(type(self.prepared) is _PreparedBundle and type(self.context) is _QualificationContext)
        _require(self.family in _FAMILIES and self.graph.job_port is self.job_port)
        for rows in (self.seed_rows, self.bucket_counts, self.qualification_facts,
                     self.reason_sources, self.basis_entities, self.witnesses):
            _require(type(rows) is tuple)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _ContributionProfile:
    facts: _ContributionFacts
    results: tuple
    witnesses: tuple

    def __post_init__(self):
        _require(type(self.facts) is _ContributionFacts and type(self.results) is tuple and type(self.witnesses) is tuple)


def _refs(prepared, entities, port):
    output = []
    for entity in _o._unique_entities(prepared, entities, port):
        output.append(_profile_ref(entity, port))
    return _o._tuple(output, port)


def _reasons(prepared, rows, port):
    """Canonical closed-code grouping, with the actual affected source IDs."""
    output = []
    for code in _r.REASON_CODES:
        entities = []
        for codes, sources in rows:
            port.charge(len(codes) + len(sources) + 1)
            if code in codes:
                entities.extend(sources)
        if entities:
            output.append((code, _refs(prepared, entities, port)))
    return _o._tuple(output, port)


def _root_facts(prepared, context, ledger, port, family):
    origin = _o._origin_facts(prepared, context, ledger, port)
    rows, reason_rows, origins = [], [], []
    for trace in origin.seed_traces:
        port.charge(8)
        codes = []
        for gap in trace.gaps:
            port.charge(len(gap.reason_codes) + 2)
            codes.extend(gap.reason_codes)
            reason_rows.append((gap.reason_codes, (_analysis_lookup(prepared, gap.source.record_id, port),)))
        if trace.gaps or not (trace.documentary_origins or trace.declared_origins or
                             trace.baseline_origins or trace.scope_cut_origins):
            disposition = 'unresolved_or_conflicted'
            if not codes:
                codes.append('unqualified_origin_boundary')
        elif trace.baseline_origins or trace.scope_cut_origins:
            disposition = 'contains_baseline_or_scope_cut'
            codes.append('baseline_or_scope_cut')
        elif trace.declared_origins:
            disposition = 'contains_declared_origin'
            codes.append('declared_origin_only')
        elif len(trace.documentary_origins) > 1:
            disposition = 'multiple_documented_origins'
            codes.append('multi_origin_unallocated')
        else:
            disposition = 'single_documented_origin'
        codes = _analysis_codes(codes, port)
        port.charge(len(trace.documentary_origins) + 8)
        rows.append(_ContributionRow(trace.seed, disposition, trace.documentary_origins, codes, trace))
        reason_rows.append((codes, (trace.seed,)))
        origins.extend(trace.documentary_origins)
    # Preserve exact contributing buckets. A multi-origin row is never split.
    buckets = []
    for origin_entity in _o._unique_entities(prepared, origins, port):
        count = 0
        for row in rows:
            for entity in row.documentary_origins:
                port.charge(2)
                if entity is origin_entity:
                    count += 1
        port.charge(2)
        buckets.append((origin_entity, count))
    eligible = bool(rows)
    for row in rows:
        port.charge(2)
        eligible = eligible and row.disposition == 'single_documented_origin'
    qualifications = _o._qualification_facts(origin, False, port)
    # These are qualifications actually performed by the origin owner. A
    # boundary candidate summary is not an additional global AND gate: all
    # necessary qualifications already belong to each governing seed row.
    reasons = _reasons(prepared, reason_rows, port)
    supplied_reasons = _o._reason_sources(origin, port)
    merged = []
    for code in _r.REASON_CODES:
        entities = []
        for candidate, sources in reasons + supplied_reasons:
            port.charge(2)
            if candidate == code:
                for ref in sources:
                    entities.append(_analysis_lookup(prepared, ref.identifier, port))
        if entities:
            merged.append((code, _refs(prepared, entities, port)))
    basis = []
    for ref in _o._basis_sources(origin, port):
        basis.append(_analysis_lookup(prepared, ref.source.identifier, port))
    port.charge(20)
    return _ContributionFacts(prepared, context, port, family, origin.inventory, origin.graph,
        origin, _o._tuple(rows, port), _o._tuple(buckets, port), eligible, origin.pc04,
        qualifications, _o._tuple(merged, port), _o._tuple(basis, port), origin.witnesses)


def _relevant_edge(prepared, edge, context, port):
    if not _analysis_scope(edge.source_entity, context, port, subjects=False):
        return False
    current, uncertain = _analysis_current(prepared, edge.source_entity, port)
    timing = _analysis_temporal(edge.source_entity, context, port)
    port.charge(3)
    if not current or timing is not None and timing.state == 'unmet' and 'temporal_inconsistency' not in timing.reason_codes:
        return False
    positive = _field(_field(edge.source_entity.node.fields, 'data', port), 'polarity', port) == 'affirmed'
    port.charge(len(edge.reason_codes) + 1)
    return positive or 'premise_disputed' in edge.reason_codes


def _immediate_coverage(prepared, seed, edges, candidates, cache, context, port):
    """Project a supplied coverage area onto one complete immediate row.

    Full ancestry qualification inspects outgoing relations of every member.
    Here only the named seed has to enumerate outgoing relations. Endpoint
    membership remains mandatory; its own outgoing ancestry is outside M006.
    The native record, basis, conflicts and explicit incomplete state survive.
    """
    output = []
    for entity in candidates:
        data = _field(entity.node.fields, 'data', port)
        details = _field(data, 'details', port)
        members = _field(details, 'member_refs', port).items
        subjects = _field(data, 'subject_refs', port).items
        if not _analysis_contains(members, seed.identifier, port) or not (
                _analysis_contains(subjects, seed.identifier, port) or
                _analysis_contains(subjects, context.inquiry_ref, port)):
            continue
        # The shared owner qualifies native completeness, finite members,
        # basis, conflict and time without making an upstream graph claim.
        # PC13 below separately proves the seven-predicate immediate area.
        found = None
        for candidate, qualifications in cache:
            port.charge(2)
            if candidate is entity:
                found = qualifications
                break
        if found is None:
            premise_context = _o._context(context, (), (), port)
            premise = _qualify_coverage(prepared, (entity.identifier,), premise_context, port)[0]
            basis = _qualify_basis(prepared, entity.identifier, premise_context, port)
            conflict = _qualify_conflicts(prepared, entity.identifier, premise_context, port)
            timing = _analysis_temporal(entity, premise_context, port)
            port.charge(6)
            found = (premise, basis, conflict, timing)
            cache.append((entity, found))
        premise, basis, conflict, timing = found
        port.charge(len(premise.reason_codes) + 4)
        codes = list(premise.reason_codes)
        complete = premise.state == 'met' and _analysis_subset(
            _IMMEDIATE, _field(details, 'relation_types', port).items, port)
        for edge in edges:
            port.charge(3)
            if edge.target.kind == 'unresolved_reference' or not _analysis_contains(members, edge.target.identifier, port):
                complete = False
        if timing is not None and timing.state != 'met':
            port.charge(len(timing.reason_codes))
            codes.extend(timing.reason_codes)
            complete = False
        if not complete:
            codes.append('upstream_coverage_incomplete')
        port.charge(10)
        output.append(_ImmediateCoverage(entity,
            'met' if complete and basis.state == conflict.state == 'met' else 'unmet',
            _analysis_codes(codes, port), basis, conflict, timing, premise))
    return _o._tuple(output, port)


def _immediate_witness(graph, seed, edges, observations, ledger, port):
    _check_ledger(graph, ledger, port)
    start = _o._node(graph, seed, port)
    nodes = [start]
    frontiers = []
    for edge in observations:
        port.charge(len(nodes) + 2)
        if not any(node is edge.target for node in nodes):
            nodes.append(edge.target)
        if edge.target.kind == 'unresolved_reference':
            port.charge(len(frontiers) + 1)
            if not any(node is edge.target for node in frontiers):
                frontiers.append(edge.target)
    count = 1 + len(nodes) + len(edges) + len(frontiers) + len(observations)
    for node in nodes:
        _charge_node(node, port)
    for edge in observations:
        _charge_edge(edge, port)
    token = ledger.reserve(witnesses=1, members=count)
    port.charge(count + 17)
    witness = _GraphWitness('complete_trace', graph, starts=(start,),
        examined_nodes=_o._tuple(nodes, port), examined_edges=edges,
        frontiers=_o._tuple(frontiers, port), observations=observations, member_count=count)
    port.check()
    ledger.retain(token)
    return witness


def _immediate_facts(prepared, context, ledger, port):
    inventory = _inventory_facts(prepared, context, port)
    identifiers = []
    for seed in inventory.seed_evidence:
        port.charge(1)
        identifiers.append(seed.identifier)
    graph_context = _o._context(context, _o._tuple(identifiers, port), _IMMEDIATE, port)
    graph = _project(prepared, graph_context, port)
    local = _o._context(context, (), _IMMEDIATE, port)
    _check_ledger(graph, ledger, port)
    candidates = []
    for entity in graph.annotations:
        port.charge(1)
        if entity.collection != 'assertions' or _field(entity.node.fields, 'assertion_kind', port) != 'assessment':
            continue
        data = _field(entity.node.fields, 'data', port)
        if _field(data, 'assessment_kind', port) != 'coverage':
            continue
        if _field(_field(data, 'details', port), 'coverage_kind', port) != 'upstream_history':
            continue
        timing = _analysis_temporal(entity, local, port)
        if timing is not None and timing.state == 'unmet' and 'temporal_inconsistency' not in timing.reason_codes:
            continue
        candidates.append(entity)
    rows, reasons, basis_entities, all_edges, witnesses = [], [], [inventory.inquiry], [], []
    # PC05, PC06, PC08, PC09 and PC10 have local, actually executed facts.
    check_data = tuple((name, [], []) for name in ('PC05', 'PC06', 'PC08', 'PC09', 'PC10'))
    coverage_cache = []
    identity_subjects = list(identifiers)
    for edge in graph.observations:
        port.charge(1)
        if _analysis_contains(identifiers, edge.source.identifier, port) and _relevant_edge(prepared, edge, local, port):
            identity_subjects.append(edge.target.identifier)
    port.charge(len(identity_subjects) * 2 + 1)
    identity_subjects = _o._tuple([entity.identifier for entity in _o._unique_entities(prepared,
        [_analysis_lookup(prepared, identifier, port) for identifier in identity_subjects], port)], port)
    identity_context = _o._context(context, identity_subjects, _IMMEDIATE, port)
    examined_identity = _qualify_identity(prepared, identity_subjects, identity_context, port)
    for seed in inventory.seed_evidence:
        seed_node = _o._node(graph, seed, port)
        examined, relevant, edges, row_codes, endpoints = [], [], [], [], [seed]
        for edge in graph.observations:
            port.charge(2)
            if edge.source is not seed_node:
                continue
            examined.append(edge)
            if _relevant_edge(prepared, edge, local, port):
                relevant.append(edge)
        inherited, direct = False, False
        for edge in relevant:
            basis = _qualify_basis(prepared, edge.source_ref.record_id, local, port)
            timing = _analysis_temporal(edge.source_entity, local, port)
            port.charge(len(basis.reason_codes) + len(edge.reason_codes) + 4)
            codes = list(basis.reason_codes + edge.reason_codes)
            blockers = tuple(code for code in codes if code != 'self_supporting_assurance')
            if not edge.eligible and not blockers:
                blockers = ('documentary_basis_incomplete',)
            row_codes.extend(blockers)
            reasons.append((blockers, (edge.source_entity,)))
            basis_entities.append(edge.source_entity)
            endpoints.append(_analysis_lookup(prepared, edge.target.identifier, port))
            check_data[0][1].append(basis.state)
            check_data[0][2].append(edge.source_entity)
            for address in basis.support_refs:
                check_data[0][2].append(_analysis_lookup(prepared, address.record_id, port))
            if 'premise_disputed' in blockers:
                conflict = _qualify_conflicts(prepared, edge.source_ref.record_id, local, port)
                for address in conflict.support_refs:
                    entity = _analysis_lookup(prepared, address.record_id, port)
                    check_data[3][2].append(entity)
                    reasons.append((('premise_disputed',), (entity,)))
                    basis_entities.append(entity)
            check_data[3][1].append('unmet' if 'premise_disputed' in blockers else 'met')
            check_data[3][2].append(edge.source_entity)
            check_data[4][1].append('unmet' if 'temporal_inconsistency' in blockers else
                'unknown' if 'time_applicability_unknown' in blockers else 'met' if timing is None else timing.state)
            check_data[4][2].append(edge.source_entity)
            if edge.eligible:
                edges.append(edge)
                all_edges.append(edge)
            if edge.eligible and basis.state == 'met' and not blockers:
                inherited = inherited or edge.predicate in _IMMEDIATE[:-1] and edge.target.kind == 'evidence_item'
                direct = direct or edge.predicate == 'originates_from' and edge.target.kind == 'origin_event'
        coverage = _immediate_coverage(prepared, seed, relevant, candidates, coverage_cache, local, port)
        covered = False
        for fact in coverage:
            port.charge(2)
            covered = covered or fact.state == 'met'
            basis_entities.append(fact.coverage)
            check_data[1][2].append(fact.coverage)
        for fact in coverage:
            port.charge(2)
            if covered and fact.state != 'met':
                continue
            for index, state in ((0, fact.basis.state), (3, fact.conflict.state),
                                 (4, 'met' if fact.timing is None else fact.timing.state)):
                check_data[index][1].append(state)
                check_data[index][2].append(fact.coverage)
            for address in fact.basis.support_refs:
                check_data[0][2].append(_analysis_lookup(prepared, address.record_id, port))
            if fact.conflict.state != 'met':
                for address in fact.conflict.support_refs:
                    entity = _analysis_lookup(prepared, address.record_id, port)
                    check_data[3][2].append(entity)
                    reasons.append((fact.conflict.reason_codes, (entity,)))
                    basis_entities.append(entity)
            if not covered:
                port.charge(len(fact.reason_codes))
                row_codes.extend(fact.reason_codes)
                reasons.append((fact.reason_codes, (fact.coverage,)))
        check_data[1][1].append('met' if covered else 'unmet' if coverage else 'unknown')
        check_data[1][2].append(seed)
        if not covered:
            row_codes.append('upstream_coverage_incomplete')
        identities = []
        for endpoint in _o._unique_entities(prepared, endpoints, port):
            if endpoint.kind == 'unresolved_reference':
                endpoint_context = _o._context(context, (endpoint.identifier,), _IMMEDIATE, port)
                identity = _qualify_identity(prepared, endpoint_context.subject_refs, endpoint_context, port)
            else:
                identity = _o._node_identity(prepared, endpoint, local, examined_identity, port)
            identities.append(identity)
            port.charge(len(identity.reason_codes) + 3)
            row_codes.extend(identity.reason_codes)
            reasons.append((identity.reason_codes, (endpoint,)))
            check_data[2][1].append(identity.state)
            check_data[2][2].append(endpoint)
            for address in identity.support_refs:
                entity = _analysis_lookup(prepared, address.record_id, port)
                reasons.append((identity.reason_codes, (entity,)))
                check_data[2][2].append(entity)
                basis_entities.append(entity)
        if not inherited and not direct:
            row_codes.append('documentary_basis_incomplete')
        codes = _analysis_codes(row_codes, port)
        disposition = ('unresolved_at_evidence_layer' if codes else
            'mixed_direct_and_inherited' if inherited and direct else
            'inherited_only_at_evidence_layer' if inherited else 'direct_origin_link_only')
        reasons.append((codes, (seed,)))
        edges = _o._tuple(edges, port)
        witnesses.append(_immediate_witness(graph, seed, edges, _o._tuple(examined, port), ledger, port))
        port.charge(10)
        rows.append(_ContributionRow(seed, disposition, (), codes, None, edges, coverage, _o._tuple(identities, port)))
    checks = []
    for check_id, states, entities in check_data:
        port.charge(len(states) * 2 + 4)
        state = ('unmet' if 'unmet' in states else 'unknown' if 'unknown' in states else
                 'met' if states else 'not_applicable')
        checks.append((check_id, state, _refs(prepared, entities, port)))
    port.charge(20)
    return _ContributionFacts(prepared, context, port, 'SIT-M006', inventory, graph, None,
        _o._tuple(rows, port), (), False, _check_edge_eligibility(graph, _o._tuple(all_edges, port), port),
        _o._tuple(checks, port), _reasons(prepared, reasons, port),
        _o._unique_entities(prepared, basis_entities, port), _o._tuple(witnesses, port))


def _contribution_facts(prepared, context, ledger, port, *, family):
    _analysis_start(prepared, context, port)
    port.charge(10)
    _require(type(family) is str and family in _FAMILIES)
    _require(len(context.claim_refs) == 1 and context.dependency_dimension is not None and
             context.graph_view == 'claim_origin' and context.coverage_kind == 'upstream_history')
    _require(len(context.relation_types) == len(_o._PARENTS) and
             _analysis_subset(_o._PARENTS, context.relation_types, port))
    inquiry = _analysis_lookup(prepared, context.inquiry_ref, port)
    _require(_analysis_contains(_field(inquiry.node.fields, 'dependency_dimensions', port).items,
                                context.dependency_dimension, port))
    answer = (_immediate_facts(prepared, context, ledger, port) if family == 'SIT-M006' else
              _root_facts(prepared, context, ledger, port, family))
    port.check()
    return answer


def _scope(facts, port):
    if facts.origin_facts is not None:
        return _o._scope(facts.origin_facts, port)
    claims = [_analysis_lookup(facts.prepared, identifier, port) for identifier in facts.context.claim_refs]
    targets = [_analysis_lookup(facts.prepared, identifier, port) for identifier in facts.context.subject_refs]
    coverages = []
    for row in facts.seed_rows:
        for fact in row.coverage:
            port.charge(1)
            coverages.append(fact.coverage)
    anchor = []
    for part in facts.context.operation_anchor:
        port.charge(1)
        if type(part) is not str and part is not None:
            part = _o._source_ref(part, port)
        anchor.append(part)
    refs = (_refs(facts.prepared, claims, port), _refs(facts.prepared, targets, port),
            _refs(facts.prepared, coverages, port))
    for group in refs:
        for ref in group:
            _charge_input_ref(ref, port, repeats=len(group) + 3)
    port.charge(22)
    scope = _r._Scope(_profile_ref(facts.inventory.inquiry, port), refs[0], refs[1],
        facts.context.dependency_dimension, 'claim_origin', facts.context.temporal_basis,
        facts.context.requested_time, refs[2],
        ('Immediate EvidenceItem layer only; distant ancestry and semantic novelty are outside this result.',),
        _o._tuple(anchor, port))
    _charge_scope(scope, port)
    return scope


def _partition(facts, population, labels, port):
    categories = []
    for label in labels:
        refs = []
        for row in facts.seed_rows:
            port.charge(2)
            if row.disposition == label:
                refs.append(_profile_ref(row.seed, port))
        for ref in refs:
            _charge_input_ref(ref, port, repeats=len(refs) + 3)
        port.charge(len(refs) * len(refs) + 8)
        categories.append(_r._PartitionCategory(label, _o._tuple(refs, port), len(refs)))
    for ref in population.member_refs:
        _charge_input_ref(ref, port, repeats=4)
    port.charge(len(population.member_refs) * 3 + len(categories) + 6)
    return _r._Partition(population, _o._tuple(categories, port))


def _witness_refs(facts, scope, port):
    if facts.origin_facts is not None:
        # One completed full-population witness links every seed. The paid
        # per-seed traces and paths remain in origin_facts and witnesses;
        # repeating all paths in every result creates no additional evidence.
        refs = []
        for seed in facts.inventory.seed_evidence:
            ref = _profile_ref(seed, port)
            _charge_input_ref(ref, port, repeats=2)
            refs.append(ref)
        _charge_scope(scope, port)
        port.charge(len(refs) + 10)
        return (_r._WitnessRef(scope, 'member_set', ('complete_trace',) + _o._tuple(refs, port)),)
    output = []
    for witness in facts.witnesses:
        seed = _analysis_lookup(facts.prepared, witness.starts[0].identifier, port)
        ref = _profile_ref(seed, port)
        _charge_input_ref(ref, port, repeats=2)
        _charge_scope(scope, port)
        port.charge(10)
        output.append(_r._WitnessRef(scope, 'member_set', ('immediate_complete_trace', ref)))
    return _o._tuple(output, port)


def _result(facts, field, scope, population, value, state, basis, witnesses, extra_reasons, port):
    port.charge(50)
    ref = _r._ResultRef(facts.family, field, scope)
    port.charge(12)
    checks = [_r._PrerequisiteCheck('PC01', ref, 'met', (), (),
        'This private owner received the admitted immutable PreparedBundle.'),
        _scope_check(_ScopeCheckFact(ref, scope), port)]
    for provider in (facts.inventory.pc03, facts.pc04):
        inputs = []
        for address in provider.input_refs:
            inputs.append(_o._source_ref(address, port))
        for source in inputs:
            _charge_input_ref(source, port, repeats=len(inputs) + 3)
        port.charge(len(inputs) + 12)
        checks.append(_r._PrerequisiteCheck(provider.check_id, ref, provider.state,
            _o._tuple(inputs, port), (), 'Actual finite population selection or local typed-edge eligibility.'))
    for check_id, check_state, inputs in facts.qualification_facts:
        for source in inputs:
            _charge_input_ref(source, port, repeats=len(inputs) + 3)
        port.charge(len(inputs) + 12)
        checks.append(_r._PrerequisiteCheck(check_id, ref, check_state, inputs, (),
            'Actual scoped premise qualifications; individual source-bound facts are retained.'))
    if facts.family in ('SIT-M005', 'SIT-M006'):
        check_id = 'PC12' if facts.family == 'SIT-M005' else 'PC13'
        complete = facts.hhi_eligible if facts.family == 'SIT-M005' else True
        if facts.family == 'SIT-M006':
            for row in facts.seed_rows:
                port.charge(2)
                complete = complete and row.disposition != 'unresolved_at_evidence_layer'
        for source in population.member_refs:
            _charge_input_ref(source, port, repeats=len(population.member_refs) + 3)
        port.charge(len(population.member_refs) + 12)
        checks.append(_r._PrerequisiteCheck(check_id, ref, 'met' if complete else 'unmet',
            population.member_refs, (), 'Whole supplied seed population; no resolved-subset fallback.'))
    reason_refs = []
    port.charge(len(facts.reason_sources) + len(extra_reasons) + 2)
    reasons = facts.reason_sources + extra_reasons
    for code, sources in reasons:
        for source in sources:
            _charge_input_ref(source, port, repeats=len(sources) + 4)
        for unused in range(3):
            _charge_scope(scope, port)
        classification = ('structural_inapplicability' if code == 'completion_interval_not_needed' else
                          'conflict' if code == 'premise_disputed' else 'evidence_gap')
        port.charge(len(sources) + 15)
        reason_refs.append(_r._Reason(code, scope, (ref,), sources,
            'Exact scoped contribution limitation; positive records and the full denominator remain visible.', classification))
    reason_refs = _o._tuple(reason_refs, port)
    components = []
    for name, links in (('premises', population.member_refs), ('conflicts', reason_refs),
                        ('value', (ref,)), ('basis', basis), ('reasons', reason_refs), ('witnesses', witnesses)):
        for link in links:
            for unused in range(3):
                _charge_link(link, port)
        port.charge(len(links) * len(links) + 10)
        components.append(_ComponentCompletion(name, links, links))
    for unused in range(3):
        _charge_link(population, port)
    port.charge(24)
    completion = _CompletionRecord(ref, (population,), (_PopulationCompletion(population, population.member_refs),),
        _o._tuple(components, port))
    checks.append(_completion_check(completion, port))
    for unused in range(2):
        _charge_link(ref, port)
        _charge_link(population, port)
        for links in (checks, basis, witnesses, reason_refs):
            for link in links:
                _charge_link(link, port)
    port.charge(len(checks) + len(basis) + len(witnesses) + len(reason_refs) + 35)
    result = _r._Result(ref, (population,), 'completed', state, 'graph_derivation',
        _r._field_kind(facts.family, field), value, _o._tuple(checks, port), basis, witnesses, reason_refs,
        'Full supplied EvidenceItem population and caller-selected granularity in the explicit snapshot/time scope. '
        'Origin incidences are nonexclusive, never allocation weights. HHI measures represented contribution frequency, '
        'not reliability, truth or process independence. Immediate inheritance concerns only the represented evidence '
        'layer, not semantic novelty. Completion intervals are finite-record classification intervals, not statistical '
        'confidence intervals or bounds on hidden origins.')
    port.check()
    return result


def _contribution_results(facts, port, *, family):
    _analysis_port(port)
    port.charge(8)
    _require(type(facts) is _ContributionFacts and facts.job_port is port and
             type(family) is str and family in _FAMILIES and family == facts.family)
    _check_projection(facts.graph, port)
    _check_inventory(facts.inventory, port)
    scope = _scope(facts, port)
    population = _profile_population(scope, facts.inventory.seed_evidence, 'evidence_item',
        'The complete explicit Claim-bound E(I,C), without dropping unresolved or multiple-origin rows.', port)
    basis = []
    for entity in facts.basis_entities:
        source = _profile_ref(entity, port)
        _charge_input_ref(source, port)
        port.charge(3)
        basis.append(_r._BasisRef(source))
    basis = _o._tuple(basis, port)
    witnesses = _witness_refs(facts, scope, port)
    n = len(facts.seed_rows)
    empty = (('no_seed_contributions', ()), ('zero_denominator', ())) if not n else ()
    definitions = []
    if family == 'SIT-M004':
        memberships = []
        for row in facts.seed_rows:
            member = _profile_ref(row.seed, port)
            origins = _refs(facts.prepared, row.documentary_origins, port)
            for source in origins:
                _charge_input_ref(source, port, repeats=len(origins) + 3)
            _charge_input_ref(member, port, repeats=3)
            port.charge(len(origins) * len(origins) + 7)
            memberships.append(_r._IncidenceRow(member, origins))
        for source in population.member_refs:
            _charge_input_ref(source, port, repeats=3)
        port.charge(len(memberships) * 2 + 8)
        incidence = _r._Incidence(population, _o._tuple(memberships, port))
        partition = _partition(facts, population, _r.ORIGIN_DISPOSITIONS, port)
        resolved = 0
        for row in facts.seed_rows:
            port.charge(3)
            resolved += row.disposition in ('multiple_documented_origins', 'single_documented_origin')
        port.charge(8)
        fraction = _r._Fraction(resolved, n, population) if n else None
        definitions = [('per_seed_origin_memberships', incidence, 'available', ()),
            ('origin_incidence_counts', incidence, 'available', ()),
            ('seed_origin_dispositions', partition, 'available', ()),
            ('documentary_origin_resolution_fraction', fraction, 'available' if n else 'unavailable', empty)]
    elif family == 'SIT-M005':
        numerator = 0
        for entity, count in facts.bucket_counts:
            port.charge(3)
            numerator += count * count
        port.charge(10)
        value = _r._Fraction(numerator, n * n, population) if facts.hhi_eligible else None
        definitions = [('single_origin_contribution_hhi', value,
                        'available' if value is not None else 'unavailable', empty)]
    else:
        partition = _partition(facts, population, _r.IMMEDIATE_DISPOSITIONS, port)
        inherited, unresolved = 0, 0
        for row in facts.seed_rows:
            port.charge(4)
            inherited += row.disposition == 'inherited_only_at_evidence_layer'
            unresolved += row.disposition == 'unresolved_at_evidence_layer'
        port.charge(22)
        point = _r._Fraction(inherited, n, population) if n and not unresolved else None
        interval = (_r._CompletionInterval(_r._Fraction(inherited, n, population),
            _r._Fraction(inherited + unresolved, n, population), 'finite_record_completion', partition)
            if n and unresolved else None)
        interval_reasons = empty if not n else () if unresolved else (('completion_interval_not_needed', ()),)
        definitions = [('immediate_evidence_layer_dispositions', partition, 'available', ()),
            ('inherited_only_seed_fraction', point, 'available' if point is not None else 'unavailable', empty),
            ('inherited_only_completion_interval', interval,
             'available' if interval is not None else 'unavailable' if not n else 'not_applicable', interval_reasons)]
    results = []
    for field, value, state, extra in definitions:
        results.append(_result(facts, field, scope, population, value, state, basis, witnesses, extra, port))
    for result in results:
        _charge_link(result.ref, port)
    port.charge(len(results) * len(results) + 5)
    answer = _r._ResultSet(_o._tuple(results, port)).results
    port.check()
    return answer


def _contribution_profile(prepared, context, ledger, port, *, family):
    facts = _contribution_facts(prepared, context, ledger, port, family=family)
    results = _contribution_results(facts, port, family=family)
    port.charge(5)
    answer = _ContributionProfile(facts, results, facts.witnesses)
    port.check()
    return answer
