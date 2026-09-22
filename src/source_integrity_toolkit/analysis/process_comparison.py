# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: PROCESS_COMPARISON. Paid, exact supplied M003 assessments.

Definitions 9.3/21.3 and reporting 14.2: an assessment is neither an
independence flag nor a global source total. Its listed population survives
failed qualification. Origin qualification starts at those listed origins,
never at an unrelated Inquiry seed population. No public orchestration.
"""
from dataclasses import dataclass

from ..contracts.bundle import _require, _Array, _freeze_object, _lookup_pair, _compare_text
from ..contracts.evidence import _QualificationContext, _SourceAddress
from ..contracts import results as _r
from ..contracts.report import (
    _charge_scope, _charge_input_ref, _charge_link, _charge_frozen,
    _ScopeCheckFact, _scope_check, _PopulationCompletion, _ComponentCompletion,
    _CompletionRecord, _completion_check,
)
from ..validation.limits import _WitnessLedger
from ..validation.structure import _field
from ..validation.semantics import (
    _analysis_port, _analysis_start, _analysis_lookup, _analysis_ids,
    _analysis_contains, _analysis_subset, _analysis_text, _analysis_address,
    _analysis_unique_addresses, _analysis_codes, _analysis_scope,
    _analysis_current, _analysis_temporal, _qualify_basis, _qualify_conflicts,
    _qualify_identity, _qualify_coverage, _profile_ref,
)
from ..graph.projections import _Projection, _project, _check_edge_eligibility
from ..graph.traversal import _reachable, _node_index
from ..graph.cycles import _components
from ..graph.witnesses import _cycle_witness
from .origins import _tuple, _node, _unique_entities, _trace_witness, _source_ref
from .inventory import _comparison_inventory_facts, _check_comparison_inventory

_FIELDS = ('submitted_comparison_member_count', 'qualified_process_set_member_count',
           'qualified_origin_set_member_count', 'independence_assessment_disclosures')
_PARENTS = ('derived_from', 'copies', 'syndicated_from', 'summarizes',
            'translates', 'quotes', 'originates_from', 'depends_on')


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Premise:
    source: object
    basis: object
    conflict: object
    time: object


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _CoverageUse:
    """An executed base qualification plus a separately paid subject binding.

    The base is never promoted. Its exact Claim/time/kind/predicate question is
    reused only within this job; every use still checks its actual population.
    """
    qualification: object
    context: object
    scope_compatible: bool
    state: str
    reason_codes: tuple

    @property
    def source(self):
        return self.qualification.source

    @property
    def coverage(self):
        return self.qualification.coverage

    @property
    def support_refs(self):
        return self.qualification.support_refs


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _ComparedOrigin:
    origin: object
    claim_ref: str
    assessments: tuple
    qualified_assessments: tuple
    reason_codes: tuple


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _ComparisonWitness:
    """Actual finite source selection; an empty selection is not independence."""
    prepared: object
    context: object
    job_port: object
    assessment: object
    members: tuple
    examined_assessments: tuple
    member_count: int


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _ComparisonFacts:
    prepared: object
    context: object
    job_port: object
    inquiry: object
    assessment: object
    members: tuple
    compatible: bool
    premises: tuple
    coverage: tuple
    origins: tuple
    graphs: tuple
    reaches: tuple
    providers: tuple
    identity: object
    contrary: tuple
    disclosures: tuple
    process_checks: tuple
    origin_checks: tuple
    process_state: str
    origin_state: str
    problems: tuple
    witnesses: tuple
    inventory: object
    origin_problems: tuple


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _ComparisonProfile:
    facts: _ComparisonFacts
    results: tuple
    witnesses: tuple


def _context(context, port, *, claims=None, subjects=(), predicates=(),
             coverage_kind=None, view=None):
    claims = context.claim_refs if claims is None else claims
    for values in (claims, subjects, predicates):
        port.charge(len(values) * len(values) + len(values) + 1)
        for value in values:
            _analysis_text(value, port)
            _analysis_text(value, port)
    if context.requested_time is not None:
        _charge_frozen(context.requested_time.fields, port)
    for part in context.operation_anchor:
        port.charge(1)
        if type(part) is str:
            _analysis_text(part, port)
        elif type(part) is _SourceAddress:
            for text in (part.collection, part.record_id, part.selector):
                _analysis_text(text, port)
    port.charge(20)
    return _QualificationContext(context.inquiry_ref, claims, subjects,
        context.dependency_dimension, context.temporal_basis, context.requested_time,
        coverage_kind, predicates, view, context.operation_anchor)


def _ledger(ledger, port):
    _analysis_port(port)
    port.charge(4)
    _require(type(ledger) is _WitnessLedger)
    try:
        _require(ledger.port._owner is port._owner and port._owner._witness_ledger is ledger)
    except AttributeError:
        raise TypeError('invalid_private_representation') from None
    ledger.port.check()


def _problem(problems, code, source, port):
    port.charge(3)
    problems.append((code, _analysis_address(source, port)))


def _premise(prepared, entity, context, cache, port):
    for fact in cache:
        port.charge(1)
        if fact.source is entity and fact.basis.context is context:
            return fact
    port.charge(6)
    fact = _Premise(entity, _qualify_basis(prepared, entity.identifier, context, port),
        _qualify_conflicts(prepared, entity.identifier, context, port),
        _analysis_temporal(entity, context, port))
    port.charge(1)
    cache.append(fact)
    return fact


def _codes(fact, port):
    port.charge(len(fact.basis.reason_codes) + len(fact.conflict.reason_codes) + 2)
    rows = list(fact.basis.reason_codes + fact.conflict.reason_codes)
    if fact.time is not None:
        port.charge(len(fact.time.reason_codes))
        rows.extend(fact.time.reason_codes)
    return _analysis_codes(rows, port)


def _current(entity, prepared, context, port):
    port.charge(1)
    if entity.collection != 'assertions':
        # Native records have no assertion lifecycle. Their retained links
        # still receive the graph owner's separate scope/time eligibility.
        return True
    if not _analysis_scope(entity, context, port, subjects=False, relation_types=False):
        return False
    current, unused = _analysis_current(prepared, entity, port)
    time = _analysis_temporal(entity, context, port)
    return current and not (time is not None and time.state == 'unmet' and
                           'temporal_inconsistency' not in time.reason_codes)


def _aggregate(states, port, *, empty='not_applicable'):
    state, seen = 'not_applicable', False
    for value in states:
        port.charge(2)
        seen = True
        if value == 'unmet':
            state = 'unmet'
        elif value == 'unknown' and state != 'unmet':
            state = 'unknown'
        elif value == 'met' and state not in ('unmet', 'unknown'):
            state = 'met'
    return state if seen else empty


def _check(check_id, state, sources, codes, port):
    port.charge(6)
    return (check_id, state, _analysis_unique_addresses(_tuple(sources, port), port),
            _analysis_codes(codes, port))


def _view(kind, dimension):
    if kind in ('origin_event', 'evidence_item'):
        return 'claim_origin', ('depends_on',) if kind == 'origin_event' else _PARENTS
    if dimension == 'organizational_control':
        return 'organizational', ('owned_by',)
    return 'model_evaluation', ('model_derived_from', 'trained_on', 'generated_by')


def _process_edge(edge, dimension, port):
    """Keep dimension-appropriate native roles, never a reviewed target."""
    port.charge(2)
    if edge.predicate is not None:
        if edge.predicate in ('model_derived_from', 'trained_on'):
            return dimension == 'model_ancestry'
        if edge.predicate == 'generated_by':
            return dimension in ('model_ancestry', 'analytical_method')
        return True
    selector = edge.source_ref.selector
    _analysis_text(selector, port)
    if dimension == 'organizational_control':
        return edge.target.kind in ('actor', 'model', 'unresolved_reference')
    if not selector.startswith('data.role_bindings[role=') or not selector.endswith('].object_ref'):
        return False
    if dimension == 'analytical_method':
        return selector == 'data.role_bindings[role=method_input].object_ref'
    if dimension == 'evaluation_rubric':
        return selector in ('data.role_bindings[role=rubric].object_ref',
                            'data.role_bindings[role=reference_answer].object_ref')
    if dimension == 'model_ancestry':
        return edge.target.kind in ('model', 'unresolved_reference')
    return False


def _comparison_graph(prepared, context, members, claim, port):
    kind = None
    for member in members:
        port.charge(1)
        if member.kind != 'unresolved_reference':
            kind = member.kind
            break
    if kind is None:
        # Selecting a finite view does not instantiate an unresolved record.
        # Unknown roots still stop traversal and cannot pass identity.
        kind = 'origin_event'
    view, predicates = _view(kind, context.dependency_dimension)
    port.charge(2)
    _require(context.graph_view is None or context.graph_view == view)
    ids = []
    for member in members:
        port.charge(1)
        ids.append(member.identifier)
    local = _context(context, port, claims=(claim,), subjects=_tuple(ids, port),
        predicates=predicates, coverage_kind='upstream_history', view=view)
    graph = _project(prepared, local, port)
    if view == 'claim_origin':
        return graph
    observations, edges = [], []
    for edge in graph.observations:
        if _process_edge(edge, context.dependency_dimension, port):
            port.charge(2)
            observations.append(edge)
            if edge.eligible:
                edges.append(edge)
    port.charge(len(graph.nodes) + len(edges) * 2 + len(observations) + len(graph.annotations) + 12)
    return _Projection(prepared, local, graph.nodes, _tuple(edges, port),
        _tuple(observations, port), graph.annotations, None, port)


def _coverage(prepared, entity, context, subjects, predicates, cache, port, *, required_kind=None):
    data = _field(entity.node.fields, 'data', port)
    details = _field(data, 'details', port)
    kind = _field(details, 'coverage_kind', port) if required_kind is None else required_kind
    base = None
    for used in cache:
        port.charge(6)
        previous = used.qualification
        old = previous.context
        if (previous.coverage is not entity or old.requested_time is not context.requested_time or
                old.temporal_basis != context.temporal_basis or old.dependency_dimension != context.dependency_dimension or
                old.coverage_kind != kind or len(old.claim_refs) != len(context.claim_refs) or
                len(old.relation_types) != len(predicates)):
            continue
        if (_compare_text(old.inquiry_ref, context.inquiry_ref, port) == 0 and
                _analysis_subset(context.claim_refs, old.claim_refs, port) and
                _analysis_subset(predicates, old.relation_types, port)):
            base = previous
            break
    if base is None:
        question = _context(context, port, predicates=predicates, coverage_kind=kind)
        base = _qualify_coverage(prepared, (entity.identifier,), question, port)[0]
    local = _context(context, port, subjects=subjects, predicates=predicates, coverage_kind=kind)
    members = _field(details, 'member_refs', port).items
    source_subjects = _field(data, 'subject_refs', port).items
    compatible = (_analysis_scope(entity, local, port, subjects=False) and
        _analysis_contains(_field(details, 'dimensions', port).items, context.dependency_dimension, port) and
        _analysis_subset(predicates, _field(details, 'relation_types', port).items, port) and
        _analysis_subset(subjects, members, port) and
        (_analysis_subset(subjects, source_subjects, port) or
         _analysis_contains(source_subjects, context.inquiry_ref, port)))
    port.charge(len(base.reason_codes) + 10)
    reasons = base.reason_codes if compatible else _analysis_codes(base.reason_codes + ('scope_unestablished',), port)
    result = _CoverageUse(base, local, compatible, base.state if compatible else 'unmet', reasons)
    port.charge(1)
    cache.append(result)
    return result


def _selected_witness(inventory, ledger, port):
    port.charge(len(inventory.members) + len(inventory.examined_assessments) + 6)
    count = len(inventory.members) + len(inventory.examined_assessments)
    token = ledger.reserve(witnesses=1, members=count)
    port.charge(9)
    witness = _ComparisonWitness(inventory.prepared, inventory.context, port,
        inventory.assessment, inventory.members, inventory.examined_assessments, count)
    ledger.retain(token)
    port.check()
    return witness


def _premise_inputs(facts, port):
    refs = []
    for fact in facts:
        port.charge(1)
        refs.append(_analysis_address(fact.source, port))
        for qualification in (fact.basis, fact.conflict):
            port.charge(len(qualification.support_refs))
            refs.extend(qualification.support_refs)
    return _analysis_unique_addresses(_tuple(refs, port), port)


def _premise_checks(premises, port, *, basis_premises=None, native_time_sources=()):
    port.charge(8)
    bases, conflicts, times, codes = [], [], [], []
    for fact in premises:
        port.charge(4)
        bases.append(fact.basis.state)
        conflicts.append(fact.conflict.state)
        times.append('met' if fact.time is None else fact.time.state)
        reason_codes = _codes(fact, port)
        port.charge(len(reason_codes))
        codes.extend(reason_codes)
    if basis_premises is not None:
        port.charge(len(basis_premises) + 1)
        bases = [fact.basis.state for fact in basis_premises]
    sources = _premise_inputs(premises, port)
    if native_time_sources:
        # Native records have no assertion window. Their actual graph-link
        # temporal limitations must survive beside the assertion premises.
        port.charge(len(native_time_sources) + len(sources) + 3)
        times.append('unknown')
        codes.append('time_applicability_unknown')
        sources = _analysis_unique_addresses(sources + native_time_sources, port)
    return (_check('PC05', _aggregate(bases, port, empty='unknown'), sources, codes, port),
            _check('PC09', _aggregate(conflicts, port, empty='unknown'), sources, codes, port),
            _check('PC10', _aggregate(times, port, empty='unknown'), sources, codes, port))


def _origin_boundaries(prepared, context, origin, graph, identity, cache,
                       coverages, disclosures, problems, port):
    """The named origin's own boundary/coverage; no seed-derived membership.

    A boundary's required coverage_ref is not replaced by a comparison's
    coverage declaration. Every selected Claim gets its own exact examination.
    """
    local = context
    subject = _node(graph, origin, port)
    candidates, qualified, needed, row_codes, coverage_states = [], [], [], [], []
    parent = False
    for edge in graph.observations:
        port.charge(1)
        if edge.source is not subject or not _current(edge.source_entity, prepared, local, port):
            continue
        data = _field(edge.source_entity.node.fields, 'data', port)
        if _field(data, 'polarity', port) == 'affirmed':
            parent = True
    for entity in prepared.entities:
        port.charge(2)
        if entity.collection != 'assertions' or _field(entity.node.fields, 'assertion_kind', port) != 'assessment':
            continue
        data = _field(entity.node.fields, 'data', port)
        if _field(data, 'assessment_kind', port) != 'origin_boundary':
            continue
        if not _analysis_contains(_field(data, 'subject_refs', port).items, origin.identifier, port):
            continue
        if not _analysis_scope(entity, local, port, subjects=False):
            continue
        port.charge(3)
        candidates.append(entity)
        disclosures.append(entity)
        fact = _premise(prepared, entity, local, cache, port)
        needed.append(fact)
        details = _field(data, 'details', port)
        role = _field(details, 'boundary_role', port)
        coverage_ref = _field(details, 'coverage_ref', port)
        coverage = None
        if coverage_ref is not None:
            coverage_entity = _analysis_lookup(prepared, coverage_ref, port)
            port.charge(1)
            disclosures.append(coverage_entity)
            coverage = _coverage(prepared, coverage_entity, local, (origin.identifier,), ('depends_on',), coverages, port,
                                 required_kind='upstream_history')
            coverage_fact = _premise(prepared, coverage_entity, local, cache, port)
            port.charge(1)
            needed.append(coverage_fact)
        port.charge(2)
        coverage_states.append('unknown' if coverage is None else coverage.state)
        valid = (role == 'documented_origin' and _field(entity.node.fields, 'lifecycle_state', port) == 'active' and
                 fact.basis.state == 'met' and fact.conflict.state == 'met' and
                 (fact.time is None or fact.time.state == 'met') and coverage is not None and
                 coverage.state == 'met' and identity.state == 'met' and not parent)
        if valid:
            port.charge(1)
            qualified.append(entity)
        reasons = _codes(fact, port)
        port.charge(len(reasons))
        row_codes.extend(reasons)
        for code in reasons:
            _problem(problems, code, entity, port)
        if coverage is not None:
            port.charge(len(coverage.reason_codes))
            row_codes.extend(coverage.reason_codes)
            for code in coverage.reason_codes:
                _problem(problems, code, coverage_entity, port)
        if role != 'documented_origin' or parent or not valid:
            port.charge(1)
            row_codes.append('unqualified_origin_boundary')
    if not qualified:
        port.charge(len(coverage_states) + 3)
        row_codes.append('unqualified_origin_boundary')
        if not candidates or not coverage_states or 'unknown' in coverage_states:
            row_codes.append('upstream_coverage_incomplete')
    codes = _analysis_codes(row_codes, port)
    for code in codes:
        _problem(problems, code, origin, port)
    port.charge(9)
    row = _ComparedOrigin(origin, graph.context.claim_refs[0], _tuple(candidates, port),
        _tuple(qualified, port), codes)
    return row, _tuple(needed, port), _aggregate(coverage_states, port, empty='unknown')


def _comparison_facts(prepared, context, assessment_ref, ledger, port):
    """Complete exact-assessment facts, confined to the actual current job."""
    _analysis_port(port)
    _ledger(ledger, port)
    inventory = _comparison_inventory_facts(prepared, context, assessment_ref, port)
    _check_comparison_inventory(inventory, prepared, context, port)
    witness = _selected_witness(inventory, ledger, port)
    port.charge(26)
    premises, coverage, origins, graphs, reaches, providers = [], [], [], [], [], []
    identities, contrary, disclosures, problems, witnesses = [], [], [], [], [witness]
    process_required, process_basis, origin_required, origin_coverage_states, boundary_problems = [], [], [], [], []
    process_checks, origin_checks = [], []
    port.charge(1)
    native_time_sources = []
    assessment, members = inventory.assessment, inventory.members
    process_state, origin_state = 'unmet', 'unmet'
    if assessment is None:
        _problem(problems, 'missing_comparison_assessment', inventory.inquiry, port)
    else:
        port.charge(1)
        disclosures.append(assessment)
        local = _context(context, port)
        principal = _premise(prepared, assessment, local, premises, port)
        port.charge(2)
        process_required.append(principal)
        process_basis.append(principal)
        data = _field(assessment.node.fields, 'data', port)
        details = _field(data, 'details', port)
        conclusion = _field(details, 'conclusion', port)
        if not inventory.scope_compatible:
            _problem(problems, 'scope_unestablished', assessment, port)
        if _analysis_contains(_field(details, 'unexamined_dimensions', port).items,
                              context.dependency_dimension, port):
            _problem(problems, 'scope_unestablished', assessment, port)
        if _field(assessment.node.fields, 'lifecycle_state', port) != 'active':
            _problem(problems, 'scope_unestablished', assessment, port)
        if conclusion != 'independent_process':
            _problem(problems, 'scope_unestablished', assessment, port)
        for code in _codes(principal, port):
            _problem(problems, code, assessment, port)
        declared_coverage = _field(details, 'coverage_ref', port)
        if declared_coverage is not None:
            entity = _analysis_lookup(prepared, declared_coverage, port)
            port.charge(1)
            disclosures.append(entity)
            # Process documentation explicitly states its own limitations.
            # A complete upstream universe is an additional origin gate, not
            # a condition silently imposed on every positive process record.
            cov_details = _field(_field(entity.node.fields, 'data', port), 'details', port)
            predicates = _field(cov_details, 'relation_types', port).items
            subjects = _field(data, 'subject_refs', port).items
            declared_use = _coverage(prepared, entity, local, subjects, predicates, coverage, port)
            declared_fact = _premise(prepared, entity, local, premises, port)
            port.charge(2)
            process_required.append(declared_fact)
            process_basis.append(declared_fact)
            for code in _codes(declared_fact, port):
                _problem(problems, code, entity, port)
            if not declared_use.scope_compatible or _field(entity.node.fields, 'lifecycle_state', port) != 'active':
                _problem(problems, 'scope_unestablished', entity, port)
        # Examined source assertions survive even if the author supplied an
        # irrelevant or unsupported item; they are not automatically ALL-AND
        # necessary premises of this distinct process question.
        for identifier in _field(details, 'examined_dependency_refs', port).items:
            entity = _analysis_lookup(prepared, identifier, port)
            port.charge(1)
            disclosures.append(entity)
        all_origins, has_unknown = True, False
        for member in members:
            port.charge(1)
            if member.kind == 'unresolved_reference':
                has_unknown = True
            elif member.kind != 'origin_event':
                all_origins = False
        for claim in context.claim_refs:
            claim_context = local if len(context.claim_refs) == 1 else _context(context, port, claims=(claim,))
            selected_ids = []
            for member in members:
                port.charge(1)
                selected_ids.append(member.identifier)
            identity = _qualify_identity(prepared, _tuple(selected_ids, port), claim_context, port)
            port.charge(1)
            identities.append(identity)
            for code in identity.reason_codes:
                _problem(problems, code, assessment, port)
            for address in identity.support_refs:
                entity = _analysis_lookup(prepared, address.record_id, port)
                if entity.collection == 'assertions':
                    port.charge(1)
                    disclosures.append(entity)
                for code in identity.reason_codes:
                    _problem(problems, code, entity, port)
            # Explicit conflicts may concern one of several selected Claims.
            scoped = _premise(prepared, assessment, claim_context, premises, port)
            port.charge(1)
            process_required.append(scoped)
            for code in _codes(scoped, port):
                _problem(problems, code, assessment, port)
            graph = _comparison_graph(prepared, context, members, claim, port)
            port.charge(1)
            graphs.append(graph)
            starts = []
            for member in members:
                port.charge(1)
                starts.append(_node(graph, member, port))
            combined = _reachable(graph, _tuple(starts, port), port)
            port.charge(2)
            reaches.append(combined)
            witnesses.append(_trace_witness(combined, ledger, port))
            providers.append(_check_edge_eligibility(graph, combined.edges, port))
            per_member = []
            for start in starts:
                reach = _reachable(graph, (start,), port)
                port.charge(1)
                per_member.append(reach)
            # Inspect the whole relevant area independently of any selected
            # representative. Distinct paths to the same ID are commonality,
            # never two independent copies of that ID.
            for index, reach in enumerate(per_member):
                port.charge(1)
                for previous_index in range(index):
                    port.charge(2)
                    other = per_member[previous_index]
                    for node in reach.nodes:
                        port.charge(1)
                        if _node_index(other.nodes, node, port) >= 0:
                            _problem(problems, 'premise_disputed', assessment, port)
                            for edge in combined.edges:
                                port.charge(1)
                                contrary.append(edge.source_entity)
                                _problem(problems, 'premise_disputed', edge.source_entity, port)
                            break
            for frontier in combined.frontiers:
                entity = _analysis_lookup(prepared, frontier.identifier, port)
                _problem(problems, 'unknown_endpoint', entity, port)
            for edge in combined.observations:
                entity = edge.source_entity
                if not _current(entity, prepared, claim_context, port):
                    continue
                port.charge(2)
                disclosures.append(entity)
                if entity.collection == 'assertions':
                    relation = _field(entity.node.fields, 'data', port)
                    denied = _field(relation, 'polarity', port) == 'denied'
                else:
                    denied = False
                    if _analysis_contains(edge.reason_codes, 'time_applicability_unknown', port):
                        port.charge(1)
                        native_time_sources.append(edge.source_ref)
                premise = _premise(prepared, entity, claim_context, premises, port)
                port.charge(1)
                process_required.append(premise)
                port.charge(len(edge.reason_codes) + 1)
                if denied or 'premise_disputed' in edge.reason_codes:
                    contrary.append(entity)
                    _problem(problems, 'premise_disputed', entity, port)
                if not edge.eligible or premise.conflict.state != 'met':
                    for code in edge.reason_codes:
                        _problem(problems, code, entity, port)
                    if premise.time is not None and premise.time.state != 'met':
                        for code in premise.time.reason_codes:
                            _problem(problems, code, entity, port)
            for component in _components(graph, port):
                if component.cycle is not None and _node_index(combined.nodes, component.members[0], port) >= 0:
                    port.charge(1)
                    witnesses.append(_cycle_witness(component, ledger, port))
                    _problem(problems, 'lineage_cycle', assessment, port)
            for candidate in prepared.entities:
                port.charge(2)
                if candidate.collection != 'assertions' or candidate is assessment:
                    continue
                if not _current(candidate, prepared, claim_context, port):
                    continue
                if _field(candidate.node.fields, 'assertion_kind', port) != 'assessment':
                    continue
                candidate_data = _field(candidate.node.fields, 'data', port)
                kind = _field(candidate_data, 'assessment_kind', port)
                if kind != 'independence':
                    continue
                overlap = 0
                for member in members:
                    port.charge(1)
                    if _analysis_contains(_field(candidate_data, 'subject_refs', port).items, member.identifier, port):
                        overlap += 1
                if overlap < 2:
                    continue
                port.charge(1)
                disclosures.append(candidate)
                native = _field(_field(candidate_data, 'details', port), 'conclusion', port)
                if native in ('shared_dependency', 'partial_overlap'):
                    contrary.append(candidate)
                    _problem(problems, 'premise_disputed', candidate, port)
            if all_origins:
                for member in members:
                    port.charge(1)
                    if member.kind == 'unresolved_reference':
                        _problem(boundary_problems, 'unknown_endpoint', member, port)
                        continue
                    row, needed, coverage_state = _origin_boundaries(prepared, claim_context, member, graph,
                        identity, premises, coverage, disclosures, boundary_problems, port)
                    port.charge(len(needed) + 3)
                    origins.append(row)
                    origin_required.extend(needed)
                    origin_coverage_states.append(coverage_state)
        for fact in process_required:
            for address in fact.conflict.support_refs:
                entity = _analysis_lookup(prepared, address.record_id, port)
                if entity.collection == 'assertions':
                    port.charge(2)
                    contrary.append(entity)
                    disclosures.append(entity)
        checks = _premise_checks(_tuple(process_required, port), port,
            basis_premises=_tuple(process_basis, port), native_time_sources=_tuple(native_time_sources, port))
        port.charge(len(checks))
        process_checks.extend(checks)
        identity_states, identity_sources, identity_codes = [], [], []
        for fact in identities:
            port.charge(len(fact.support_refs) + len(fact.reason_codes) + 2)
            identity_states.append(fact.state)
            identity_sources.extend(fact.support_refs)
            identity_codes.extend(fact.reason_codes)
        process_checks.append(_check('PC08', _aggregate(identity_states, port), identity_sources, identity_codes, port))
        process_codes = []
        # Boundary-only failures do not defeat the independently documented
        # process assessment. The origin-specific cell adds those premises.
        for code, address in problems:
            port.charge(1)
            process_codes.append(code)
        process_codes = _analysis_codes(process_codes, port)
        bad_code = False
        for code in process_codes:
            port.charge(1)
            if code != 'self_supporting_assurance':
                bad_code = True
        port.charge(2 * len(process_required) + len(process_basis) + 3)
        process_state = 'met' if (inventory.scope_compatible and not bad_code and
            all(fact.basis.state == 'met' for fact in process_basis) and all(fact.conflict.state == 'met' for fact in process_required) and
            all(fact.time is None or fact.time.state == 'met' for fact in process_required)) else 'unmet'
        if not all_origins:
            origin_state = 'not_applicable'
        else:
            port.charge(len(origins) + 1)
            origin_state = 'met' if process_state == 'met' and not has_unknown and all(row.qualified_assessments for row in origins) else 'unmet'
        port.charge(2)
        process_checks.append(_check('PC11', process_state, (_analysis_address(assessment, port),), process_codes, port))
        needed = _tuple(origin_required, port)
        origin_checks.extend(_premise_checks(needed, port))
        origin_checks.append(_check('PC06', _aggregate(origin_coverage_states, port, empty='unknown'),
            _premise_inputs(needed, port), (), port))
        port.charge(len(origins) + 1)
        origin_checks.append(_check('PC07', 'not_applicable' if not all_origins else
            'unknown' if has_unknown else 'met' if all(row.qualified_assessments for row in origins) else 'unmet',
            _premise_inputs(needed, port), ('unqualified_origin_boundary',) if origin_state == 'unmet' else (), port))
    port.charge(30)
    result = _ComparisonFacts(prepared, context, port, inventory.inquiry, assessment,
        members, inventory.scope_compatible, _tuple(premises, port), _tuple(coverage, port),
        _tuple(origins, port), _tuple(graphs, port), _tuple(reaches, port), _tuple(providers, port),
        _tuple(identities, port), _unique_entities(prepared, contrary, port),
        _unique_entities(prepared, disclosures, port), _tuple(process_checks, port),
        _tuple(origin_checks, port), process_state, origin_state, _tuple(problems, port),
        _tuple(witnesses, port), inventory, _tuple(boundary_problems, port))
    port.check()
    return result


def _check_facts(facts, port):
    _analysis_port(port)
    port.charge(4)
    _require(type(facts) is _ComparisonFacts and facts.job_port is port)
    _check_comparison_inventory(facts.inventory, facts.prepared, facts.context, port)


def _scope(facts, port):
    port.charge(12)
    context = facts.context
    actual_view = context.graph_view
    for graph in facts.graphs:
        port.charge(5)
        _require(graph.job_port is port and graph.prepared is facts.prepared)
        _require(_compare_text(graph.context.inquiry_ref, context.inquiry_ref, port) == 0 and
                 graph.context.dependency_dimension == context.dependency_dimension)
        if actual_view is None:
            actual_view = graph.context.graph_view
        _require(actual_view == graph.context.graph_view)
    claims, targets, coverages, anchor = [], [], [], ['SIT-M003']
    for identifier in context.claim_refs:
        port.charge(1)
        claims.append(_profile_ref(_analysis_lookup(facts.prepared, identifier, port), port))
    if facts.assessment is not None:
        reference = _profile_ref(facts.assessment, port)
        port.charge(2)
        targets.append(reference)
        anchor.append(reference)
    else:
        port.charge(1)
        anchor.append('missing_comparison_assessment')
    if context.subject_refs:
        # Preserve the actual requested set even when no matching assessment
        # exists. These are query anchors, not an invented source population.
        port.charge(1)
        anchor.append('queried_subjects')
        for identifier, unused in _analysis_ids(context.subject_refs, port):
            port.charge(1)
            anchor.append(_profile_ref(_analysis_lookup(facts.prepared, identifier, port), port))
    entities = []
    for fact in facts.coverage:
        port.charge(1)
        entities.append(fact.coverage)
    for entity in _unique_entities(facts.prepared, entities, port):
        port.charge(1)
        coverages.append(_profile_ref(entity, port))
    for part in context.operation_anchor:
        port.charge(1)
        if type(part) is _SourceAddress:
            part = _source_ref(part, port)
        elif type(part) is str:
            _analysis_text(part, port)
        anchor.append(part)
    for refs in (claims, targets, coverages):
        port.charge(len(refs) * len(refs) + len(refs) + 1)
        for ref in refs:
            _charge_input_ref(ref, port, repeats=len(refs) + 3)
    for part in anchor:
        if type(part) is _r._InputRef:
            _charge_input_ref(part, port, repeats=2)
        elif type(part) is str:
            _analysis_text(part, port)
    if context.requested_time is not None:
        _charge_frozen(context.requested_time.fields, port)
    port.charge(20)
    return _r._Scope(_profile_ref(facts.inquiry, port), _tuple(claims, port), _tuple(targets, port),
        context.dependency_dimension, actual_view, context.temporal_basis, context.requested_time,
        _tuple(coverages, port), ('One supplied assessment, or an explicitly absent requested comparison. '
        'Selected exact Claims are a scoped query; the unchanged native assessment retains its full original scope. '
        'Snapshot structure does not reconstruct unknown lifecycle history.',), _tuple(anchor, port))


def _basis(facts, port):
    port.charge(len(facts.inventory.selection_refs) + 1)
    addresses = list(facts.inventory.selection_refs)
    for fact in facts.premises:
        port.charge(1)
        addresses.append(_analysis_address(fact.source, port))
        for qualification in (fact.basis, fact.conflict):
            port.charge(len(qualification.support_refs))
            addresses.extend(qualification.support_refs)
    for entity in facts.contrary:
        port.charge(1)
        addresses.append(_analysis_address(entity, port))
    result = []
    for address in _analysis_unique_addresses(_tuple(addresses, port), port):
        source = _source_ref(address, port)
        _charge_input_ref(source, port)
        port.charge(3)
        result.append(_r._BasisRef(source))
    return _tuple(result, port)


def _witness_refs(facts, scope, port):
    port.charge(4)
    refs = []
    for witness in facts.witnesses:
        port.charge(3)
        if type(witness) is _ComparisonWitness:
            kind, anchor = 'member_set', ['comparison_selection']
        else:
            anchor = [witness.kind]
            kind = 'cycle' if witness.kind == 'cycle' else 'member_set'
            # Different per-Claim traversals remain distinct retained payloads.
            for claim in witness.graph.context.claim_refs:
                port.charge(1)
                anchor.append(_profile_ref(_analysis_lookup(facts.prepared, claim, port), port))
            nodes = (witness.nodes[0],) if witness.kind == 'cycle' else witness.starts
            for node in nodes:
                port.charge(1)
                anchor.append(_profile_ref(_analysis_lookup(facts.prepared, node.identifier, port), port))
        for part in anchor:
            port.charge(1)
            if type(part) is _r._InputRef:
                _charge_input_ref(part, port, repeats=2)
            elif type(part) is str:
                _analysis_text(part, port)
        _charge_scope(scope, port)
        port.charge(len(anchor) + 8)
        refs.append(_r._WitnessRef(scope, kind, _tuple(anchor, port)))
    return _tuple(refs, port)


def _native_fields(prepared, entity, port):
    # Admission keeps the captured field bag separately from its sorted index.
    # Disclosures preserve the caller's native member/reference array order.
    rows = _field(prepared.captured_tree, entity.collection, port).items
    for row in rows:
        port.charge(1)
        if _compare_text(_field(row, 'id', port), entity.identifier, port) == 0:
            return row
    raise TypeError('missing_captured_comparison_source')


def _disclosures(facts, port):
    port.charge(4)
    records = []
    for entity in facts.disclosures:
        port.charge(1)
        if entity.collection != 'assertions':
            continue
        native = _native_fields(facts.prepared, entity, port)
        fields = []
        for name in ('data', 'scope', 'provenance', 'asserted_at', 'lifecycle_state', 'lifecycle_basis_ref_ids'):
            value = _field(native, name, port)
            _charge_frozen(value, port)
            port.charge(1)
            fields.append((name, value))
        for optional in ('gaps', 'extensions'):
            found = _lookup_pair(native.items, optional, port)
            if found is not None:
                _charge_frozen(found[1], port)
                port.charge(1)
                fields.append(found)
        if entity is facts.assessment:
            reasons = []
            for code, source in facts.problems:
                port.charge(1)
                reasons.append(code)
            port.charge(7)
            fields.extend((('process_qualification_state', facts.process_state),
                           ('origin_qualification_state', facts.origin_state),
                           ('reason_codes', _Array(_analysis_codes(reasons, port)))))
        frozen = _freeze_object(fields, port)
        port.charge(8)
        records.append(_r._Disclosure(_profile_ref(entity, port), frozen,
            ('Unchanged supplied assertion, including its native basis, conclusion, limitations and lifecycle. '
             'Documentary qualification is not toolkit authentication or outside-world verification.',)))
    port.charge(len(records) + 3)
    return _r._RecordDisclosures(_tuple(records, port))


def _reasons(facts, scope, ref, field, port):
    port.charge(len(facts.problems) + 1)
    problems = list(facts.problems)
    if field in (_FIELDS[2], _FIELDS[3]):
        port.charge(len(facts.origin_problems))
        problems.extend(facts.origin_problems)
    if field == _FIELDS[2] and facts.origin_state == 'not_applicable':
        port.charge(2)
        problems.append(('no_applicable_subject', _analysis_address(facts.assessment, port)))
    grouped = []
    for code, address in problems:
        found = None
        for old_code, sources in grouped:
            port.charge(1)
            if code == old_code:
                found = sources
                break
        if found is None:
            port.charge(3)
            found = []
            grouped.append((code, found))
        port.charge(1)
        found.append(address)
    result = []
    for code, addresses in grouped:
        sources = []
        for address in _analysis_unique_addresses(_tuple(addresses, port), port):
            port.charge(1)
            sources.append(_source_ref(address, port))
        for source in sources:
            _charge_input_ref(source, port, repeats=len(sources) + 3)
        for unused in range(3):
            _charge_scope(scope, port)
        port.charge(len(sources) + 18)
        classification = ('structural_inapplicability' if code == 'no_applicable_subject' else
                          'conflict' if code == 'premise_disputed' else 'evidence_gap')
        result.append(_r._Reason(code, scope, (ref,), _tuple(sources, port),
            'This exact supplied comparison retains the identified prerequisite limitation. '
            'A missing qualification is not zero independent members or a conclusion about other comparisons.',
            classification))
    return _tuple(result, port)


def _checks(facts, ref, field, port):
    port.charge(8)
    checks = [_scope_check(_ScopeCheckFact(ref, ref.scope), port)]
    port.charge(12)
    checks.append(_r._PrerequisiteCheck('PC01', ref, 'met', (), (),
        'The component received the complete admitted immutable snapshot.'))
    inventory = facts.inventory.pc03
    specifications = [_check('PC03', inventory.state, inventory.input_refs, facts.inventory.reason_codes, port)]
    sources, states = [], []
    for provider in facts.providers:
        port.charge(len(provider.input_refs) + 1)
        sources.extend(provider.input_refs)
        states.append(provider.state)
    specifications.append(_check('PC04', _aggregate(states, port), sources, (), port))
    port.charge(len(facts.process_checks))
    specifications.extend(facts.process_checks)
    if facts.assessment is None:
        for check_id in ('PC05', 'PC08', 'PC09', 'PC10', 'PC11'):
            port.charge(1)
            specifications.append(_check(check_id, 'unknown', facts.inventory.selection_refs,
                ('missing_comparison_assessment',), port))
    # Comparison coverage is disclosed as its own question, rather than a
    # universal prerequisite imported from origin/HHI completeness rules.
    coverage_states, coverage_sources, coverage_codes = [], [], []
    for fact in facts.coverage:
        if facts.assessment is None:
            break
        data = _field(facts.assessment.node.fields, 'data', port)
        named = _field(_field(data, 'details', port), 'coverage_ref', port)
        _analysis_text(fact.source.record_id, port)
        if fact.source.record_id == named:
            port.charge(len(fact.reason_codes) + 2)
            coverage_states.append(fact.state)
            coverage_sources.append(fact.source)
            coverage_codes.extend(fact.reason_codes)
    specifications.append(_check('PC06', _aggregate(coverage_states, port, empty='unknown'),
        coverage_sources, coverage_codes, port))
    if field == _FIELDS[2] and facts.assessment is None:
        specifications.append(_check('PC07', 'unknown', (), ('missing_comparison_assessment',), port))
    elif field == _FIELDS[2]:
        for incoming in facts.origin_checks:
            found = -1
            for index, old in enumerate(specifications):
                port.charge(1)
                if incoming[0] == old[0]:
                    found = index
                    break
            if found >= 0:
                old = specifications[found]
                port.charge(len(old[2]) + len(incoming[2]) + len(old[3]) + len(incoming[3]) + 1)
                state = incoming[1] if incoming[0] in ('PC06', 'PC07') else _aggregate((old[1], incoming[1]), port)
                specifications[found] = _check(incoming[0], state, old[2] + incoming[2], old[3] + incoming[3], port)
            else:
                port.charge(1)
                specifications.append(incoming)
    else:
        specifications.append(_check('PC07', 'not_applicable', (), (), port))
    # Actual contrary dependency/assessment evidence is independent of the
    # basis helper's explicit-conflict discovery and remains PC09 evidence.
    if facts.contrary:
        contrary_sources = []
        for entity in facts.contrary:
            port.charge(1)
            contrary_sources.append(_analysis_address(entity, port))
        for index, old in enumerate(specifications):
            port.charge(1)
            if old[0] == 'PC09':
                port.charge(len(old[2]) + len(contrary_sources))
                specifications[index] = _check('PC09', 'unmet', old[2] + _tuple(contrary_sources, port), ('premise_disputed',), port)
    for check_id, state, addresses, codes in specifications:
        inputs = []
        for address in addresses:
            port.charge(1)
            inputs.append(_source_ref(address, port))
        for source in inputs:
            _charge_input_ref(source, port, repeats=len(inputs) + 3)
        port.charge(len(inputs) + 14)
        checks.append(_r._PrerequisiteCheck(check_id, ref, state, _tuple(inputs, port), (),
            'Executed exact comparison prerequisite; native declarations, supporting material and limitations remain separate.'))
    return checks


def _comparison_results(facts, port):
    """Construct four atomic M003 Results from completed same-job facts."""
    _check_facts(facts, port)
    scope = _scope(facts, port)
    basis = _basis(facts, port)
    witnesses = _witness_refs(facts, scope, port)
    members = []
    for entity in facts.members:
        port.charge(1)
        members.append(_profile_ref(entity, port))
    members = _tuple(members, port)
    outputs = []
    for field in _FIELDS:
        _check_facts(facts, port)
        port.charge(180)
        ref = _r._ResultRef('SIT-M003', field, scope)
        if field == _FIELDS[3]:
            value, state, origin = _disclosures(facts, port), 'available', 'attributed_record'
        elif facts.assessment is None:
            value, state, origin = None, 'unavailable', 'inventory' if field == _FIELDS[0] else 'qualification_check'
        else:
            qualified = facts.process_state if field == _FIELDS[1] else facts.origin_state
            state = 'available' if field == _FIELDS[0] or qualified == 'met' else (
                'not_applicable' if field == _FIELDS[2] and qualified == 'not_applicable' else 'unavailable')
            value, origin = None, 'inventory' if field == _FIELDS[0] else 'qualification_check'
        for member in members:
            _charge_input_ref(member, port, repeats=len(members) + 3)
        for link in basis:
            _charge_link(link, port)
        port.charge(len(members) * len(members) + len(members) + len(basis) + 18)
        population = _r._Population(scope, 'origin_event' if field == _FIELDS[2] else 'comparison_member', members,
            'Exactly the subject_refs of this identified supplied independence assessment; no seed, pair union or inferred set.',
            (), basis, 'unestablished' if facts.assessment is None and field != _FIELDS[3] else 'enumerated_for_scope',
            ('An absent assessment does not establish an empty comparison population. Compatible unresolved members remain placeholders.',))
        if field != _FIELDS[3] and state == 'available':
            port.charge(4)
            value = _r._Count(len(members), population)
        reasons = _reasons(facts, scope, ref, field, port)
        checks = _checks(facts, ref, field, port)
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
        # Missing intended membership is disclosed as unestablished, while
        # the explicit absence scan and its witness really did finish.
        known = population.membership_state == 'enumerated_for_scope'
        completed = (_PopulationCompletion(population, members),) if known else ()
        completion = _CompletionRecord(ref, (population,) if known else (), completed, _tuple(components, port))
        checks.append(_completion_check(completion, port))
        for unused in range(2):
            _charge_link(ref, port)
            _charge_link(population, port)
            for links in (checks, basis, witnesses, reasons):
                for link in links:
                    _charge_link(link, port)
        port.charge(len(checks) + len(basis) + len(witnesses) + len(reasons) + 32)
        outputs.append(_r._Result(ref, (population,), 'completed', state, origin,
            'record_disclosures' if field == _FIELDS[3] else 'count', value,
            _tuple(checks, port), basis, witnesses, reasons,
            'Members of this exact supplied comparison only; qualification is reported separately. Native conclusions and basis remain '
            'attributed, not toolkit verification. No statistical independence, transitivity, union or sum across comparisons, '
            'global independent-source count, or qualification of unexamined dimensions follows. Origin qualification additionally '
            'requires every listed OriginEvent boundary under every selected exact Claim and dimension.'))
    result = _tuple(outputs, port)
    port.check()
    return result


def _comparison_profile(prepared, context, assessment_ref, ledger, port):
    facts = _comparison_facts(prepared, context, assessment_ref, ledger, port)
    results = _comparison_results(facts, port)
    port.charge(4)
    profile = _ComparisonProfile(facts, results, facts.witnesses)
    port.check()
    return profile
