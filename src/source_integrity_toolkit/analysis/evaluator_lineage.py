# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: EVALUATOR_LINEAGE. Paid M008 facts for one actual role pair.

Definitions 25.1 and lineage 10.6: identities, strict recorded ancestry,
one-sided paths and exact supplied family strings retain separate units.
The explicit query names one Evaluation and two roles; no model-pair scan.
"""
from dataclasses import dataclass

from ..contracts.bundle import _require, _Array, _freeze_object, _lookup_pair
from ..contracts import results as _r
from ..contracts.report import (
    _charge_scope, _charge_input_ref, _charge_link, _charge_frozen,
    _ScopeCheckFact, _scope_check, _PopulationCompletion, _ComponentCompletion,
    _CompletionRecord, _completion_check,
)
from ..validation.structure import _field
from ..validation.semantics import (
    _analysis_start, _analysis_port, _analysis_lookup, _analysis_contains,
    _analysis_text, _analysis_ids, _analysis_address, _analysis_codes, _analysis_subset,
    _analysis_unique_addresses, _analysis_scope, _qualify_identity,
    _qualify_coverage, _profile_ref,
)
from ..graph.projections import (
    _Projection, _GraphEdge, _project, _check_projection, _check_edge_eligibility,
    _graph_sort, _compare_key, _record_time,
)
from ..graph.traversal import _reachable, _ranked_search, _path_from_search, _node_index
from ..graph.witnesses import _path_witness, _member_witness
from ..graph.cycles import _components
from ..graph.witnesses import _cycle_witness
from . import origins as _o
from . import process_comparison as _p

_FIELDS = ('shared_recorded_ancestor_count', 'matching_family_label_count',
           'evaluator_overlap_disclosures', 'evaluator_overlap_witnesses')
_ROLES = ('candidate', 'generator', 'judge', 'executor', 'human_reviewer',
          'reference_answer', 'rubric', 'validation_environment', 'method_input')
_VIEWS = (('model_evaluation', ('generated_by', 'model_derived_from', 'trained_on'), 'model_history'),
          ('material_transformation', ('derived_from', 'copies', 'syndicated_from', 'summarizes',
                                      'translates', 'quotes', 'retrieved_from'), 'upstream_history'),
          ('organizational', ('owned_by',), 'other'))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _LineageEligibility:
    """Local conjunction of completed source-graph PC04 provider facts."""
    state: str
    input_refs: tuple
    providers: tuple


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _IdentitySelection:
    state: str
    support_refs: tuple
    reason_codes: tuple
    facts: tuple


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _EvaluatorFacts:
    prepared: object
    context: object
    job_port: object
    inquiry: object
    evaluation: object
    roles: tuple
    role_bindings: tuple
    role_supports: tuple
    left_objects: tuple
    right_objects: tuple
    graph: object
    reaches: tuple
    shared_objects: tuple
    common_ancestors: tuple
    common_paths: tuple
    one_sided: tuple
    matching_family_labels: tuple
    family_representatives: tuple
    missing_family_models: tuple
    coverage: tuple
    identity: object
    premises: tuple
    disclosures: tuple
    problems: tuple
    roles_complete: bool
    pc04: object
    witnesses: tuple
    positive_witnesses: tuple


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _EvaluatorProfile:
    facts: _EvaluatorFacts
    results: tuple
    witnesses: tuple


def _problem(rows, code, entity, port):
    port.charge(3)
    rows.append((code, _analysis_address(entity, port)))


def _entities(prepared, nodes, port):
    rows = []
    for node in nodes:
        port.charge(1)
        rows.append(_analysis_lookup(prepared, node.identifier, port))
    return _o._unique_entities(prepared, rows, port)


def _role_edge(edge, evaluation, roles, port):
    port.charge(3)
    if edge.source_entity is not evaluation or edge.predicate is not None:
        return False
    selector = edge.source_ref.selector
    _analysis_text(selector, port)
    for role in roles:
        _analysis_text(role, port)
        if selector == 'data.role_bindings[role=' + role + '].object_ref':
            return True
    return False


def _strict_path(searches, target, port):
    """Choose a real nonreflexive path, including multi-binding role sides."""
    for search in searches:
        port.charge(3)
        if search.nodes[search.start_index] is target:
            continue
        path = _path_from_search(search, target, port)
        if path is not None and path.edges:
            return path
    return None



def _metadata_graph(prepared, context, roots, predicates, coverage_kind, port):
    """Compose exact query scope and inquiry metadata in one named view.

    The two source contexts remain attached to their original graph edges.
    Their actual providers are invoked after selection; this local composite
    neither impersonates a graph provider nor widens to other Claim versions.
    """
    contexts = [_p._context(context, port, subjects=roots, predicates=predicates,
        coverage_kind=coverage_kind, view=context.graph_view)]
    if context.claim_refs:
        contexts.append(_p._context(context, port, claims=(), subjects=roots,
            predicates=predicates, coverage_kind=coverage_kind, view=context.graph_view))
    projections, nodes, annotations = [], [], []
    for local in contexts:
        projected = _project(prepared, local, port)
        projections.append(projected)
        port.charge(len(projected.nodes) + len(projected.annotations) + 2)
        nodes.extend(projected.nodes)
        annotations.extend(projected.annotations)
    ordered = _graph_sort(_o._tuple(nodes, port), port, 'node')
    unique = []
    for node in ordered:
        port.charge(2)
        if not unique or _compare_key(unique[-1].key, node.key, port):
            unique.append(node)
    unique = _o._tuple(unique, port)
    edge_rows = []
    for projected in projections:
        for edge in projected.observations:
            local = projected.context
            if not _analysis_scope(edge.source_entity, local, port, subjects=False):
                continue
            duplicate = False
            for old, unused, unused2 in edge_rows:
                if _compare_key(old.key, edge.key, port) == 0:
                    duplicate = True
                    break
            if duplicate:
                continue
            source = unique[_node_index(unique, edge.source, port)]
            target = unique[_node_index(unique, edge.target, port)]
            port.charge(14)
            clone = _GraphEdge(source, target, edge.key, edge.source_ref,
                edge.predicate, edge.eligible, edge.reason_codes, edge.source_entity)
            edge_rows.append((clone, projected, edge))
    return contexts[0], unique, _o._tuple(edge_rows, port), _o._unique_entities(prepared, annotations, port), _o._tuple(projections, port)


def _edge_providers(edge_rows, used_edges, projections, port):
    facts, sources, states = [], [], []
    for projected in projections:
        selected = []
        for clone, origin, original in edge_rows:
            port.charge(2)
            if origin is not projected:
                continue
            for used in used_edges:
                port.charge(1)
                if used is clone:
                    selected.append(original)
                    break
        fact = _check_edge_eligibility(projected, _o._tuple(selected, port), port)
        facts.append(fact)
        states.append(fact.state)
        port.charge(len(fact.input_refs))
        sources.extend(fact.input_refs)
    port.charge(8)
    return _LineageEligibility(_p._aggregate(states, port),
        _analysis_unique_addresses(_o._tuple(sources, port), port), _o._tuple(facts, port))

def _evaluator_lineage_facts(prepared, context, ledger, port):
    inquiry = _analysis_start(prepared, context, port)
    _p._ledger(ledger, port)
    port.charge(15)
    _require(len(context.subject_refs) == 1 and len(context.operation_anchor) == 2)
    roles = context.operation_anchor
    _require(all(type(role) is str and role in _ROLES for role in roles) and roles[0] != roles[1])
    evaluation = _analysis_lookup(prepared, context.subject_refs[0], port)
    _require(evaluation.kind == 'evaluation')
    predicates, coverage_kind = None, None
    for view, candidates, kind in _VIEWS:
        port.charge(2)
        if context.graph_view == view:
            predicates, coverage_kind = candidates, kind
    _require(predicates is not None and context.dependency_dimension is not None)
    _require(_analysis_contains(_field(inquiry.node.fields, 'dependency_dimensions', port).items,
        context.dependency_dimension, port))
    _require(_analysis_subset(context.relation_types, predicates, port))
    predicates = context.relation_types
    data = _field(evaluation.node.fields, 'data', port)
    native = _field(data, 'role_bindings', port).items
    bindings, sides, problems, role_supports = [], [], [], []
    complete, role_time_codes = _record_time(prepared, evaluation, context, port)
    for code in role_time_codes:
        _problem(problems, code, evaluation, port)
    for role in roles:
        selected, objects = [], []
        for binding in native:
            port.charge(2)
            if _field(binding, 'role', port) == role:
                selected.append(binding)
                for identifier in _field(binding, 'evidence_ref_ids', port).items:
                    reference = _analysis_lookup(prepared, identifier, port)
                    port.charge(1)
                    role_supports.append(reference)
                    if _field(reference.node.fields, 'availability', port) != 'supplied':
                        _problem(problems, 'support_uninspectable', reference, port)
                entity = _analysis_lookup(prepared, _field(binding, 'object_ref', port), port)
                objects.append(entity)
                if entity.kind == 'unresolved_reference':
                    complete = False
                    _problem(problems, 'unknown_endpoint', entity, port)
        if not selected:
            complete = False
            _problem(problems, 'roles_incomplete', evaluation, port)
        bindings.append(_o._tuple(selected, port))
        sides.append(_o._unique_entities(prepared, objects, port))
    roots = _o._unique_entities(prepared, sides[0] + sides[1], port)
    ids = []
    for entity in roots:
        port.charge(1)
        ids.append(entity.identifier)
    local, nodes, edge_rows, annotations, projections = _metadata_graph(prepared, context,
        _o._tuple(ids, port), predicates, coverage_kind, port)
    observations, edges, role_edges = [], [], []
    for edge, unused, unused2 in edge_rows:
        port.charge(3)
        if _role_edge(edge, evaluation, roles, port):
            role_edges.append(edge)
            if not edge.eligible:
                complete = False
                for code in edge.reason_codes:
                    _problem(problems, code, evaluation, port)
        # Role objects are starts. Evaluation target/result links never
        # become ancestry, and native role links cannot create another pair.
        if edge.predicate is not None:
            observations.append(edge)
            if edge.eligible:
                edges.append(edge)
    port.charge(len(nodes) + len(edges) + len(observations) + 15)
    graph = _Projection(prepared, local, nodes, _graph_sort(_o._tuple(edges, port), port),
        _graph_sort(_o._tuple(observations, port), port), annotations, None, port)
    reaches, searches, witnesses, positive = [], [], [], []
    for side in sides:
        starts = []
        side_searches = []
        for entity in side:
            node = _o._node(graph, entity, port)
            starts.append(node)
            side_searches.append(_ranked_search(graph, node, port))
        reach = _reachable(graph, _o._tuple(starts, port), port)
        reaches.append(reach)
        searches.append(_o._tuple(side_searches, port))
        witnesses.append(_o._trace_witness(reach, ledger, port))
        for frontier in reach.frontiers:
            _problem(problems, 'unknown_endpoint', _analysis_lookup(prepared, frontier.identifier, port), port)
    shared = []
    for entity in sides[0]:
        for other in sides[1]:
            port.charge(2)
            if entity is other:
                shared.append(entity)
    shared = _o._unique_entities(prepared, shared, port)
    if shared:
        nodes = []
        for entity in shared:
            nodes.append(_o._node(graph, entity, port))
        witness = _member_witness(graph, _o._tuple(nodes, port), ledger, port)
        witnesses.append(witness)
        positive.append(('shared_role_identity', witness))
    common, paired, one_sided = [], [], []
    for node in graph.nodes:
        port.charge(3)
        if node.kind == 'unresolved_reference':
            continue
        left = _strict_path(searches[0], node, port)
        if left is None:
            continue
        right = _strict_path(searches[1], node, port)
        if right is None:
            continue
        entity = _analysis_lookup(prepared, node.identifier, port)
        lw, rw = _path_witness(left, ledger, port), _path_witness(right, ledger, port)
        common.append(entity)
        paired.append((entity, lw, rw))
        witnesses.extend((lw, rw))
        positive.extend((('strict_common_ancestor_left', lw), ('strict_common_ancestor_right', rw)))
    for index in (0, 1):
        for entity in sides[1 - index]:
            port.charge(2)
            if entity.kind == 'unresolved_reference':
                continue
            target = _o._node(graph, entity, port)
            path = _strict_path(searches[index], target, port)
            if path is not None:
                witness = _path_witness(path, ledger, port)
                start = _analysis_lookup(prepared, path.start.identifier, port)
                one_sided.append((start, entity, witness))
                witnesses.append(witness)
                positive.append(('one_sided_ancestry', witness))
    for component in _components(graph, port):
        if component.cycle is None:
            continue
        reached = False
        for reach in reaches:
            port.charge(1)
            if _node_index(reach.nodes, component.members[0], port) >= 0:
                reached = True
        if reached:
            witness = _cycle_witness(component, ledger, port)
            witnesses.append(witness)
            _problem(problems, 'lineage_cycle', evaluation, port)
    label_sides, missing = [], []
    for side in sides:
        labels = []
        for entity in side:
            port.charge(2)
            if entity.kind != 'model':
                continue
            label = _field(_field(entity.node.fields, 'data', port), 'family_label', port)
            if label is None:
                missing.append(entity)
                _problem(problems, 'context_withheld_or_unavailable', entity, port)
            else:
                _analysis_text(label, port)
                labels.append((label, entity))
        label_sides.append(_o._tuple(labels, port))
    label_rows = []
    for label, entity in label_sides[0]:
        for other, unused in label_sides[1]:
            _analysis_text(label, port)
            _analysis_text(other, port)
            if label == other:
                label_rows.append((label, entity))
                break
    matches, representatives = [], []
    port.charge(len(label_rows) + 1)
    for label, unused in _analysis_ids(_o._tuple([row[0] for row in label_rows], port), port):
        for candidate, entity in label_rows:
            _analysis_text(candidate, port)
            if candidate == label:
                matches.append(label)
                representatives.append(entity)
                break
    if representatives:
        nodes = []
        for entity in representatives:
            nodes.append(_o._node(graph, entity, port))
        witness = _member_witness(graph, _o._tuple(nodes, port), ledger, port)
        witnesses.append(witness)
        positive.append(('exact_family_label_match', witness))
    involved, used_edges = [evaluation], []
    port.charge(len(roots))
    involved.extend(roots)
    for reach in reaches:
        port.charge(len(reach.edges) + len(reach.nodes) + len(reach.observations))
        used_edges.extend(reach.edges)
        involved.extend(_entities(prepared, reach.nodes, port))
        for edge in reach.observations:
            involved.append(edge.source_entity)
            for code in edge.reason_codes:
                _problem(problems, code, edge.source_entity, port)
    used_edges.extend(role_edges)
    pc04 = _edge_providers(edge_rows, _o._tuple(used_edges, port), projections, port)
    identity_facts, identity_sources, identity_codes, identity_states = [], [], [], []
    for projected in projections:
        fact = _qualify_identity(prepared, _o._tuple(ids, port), projected.context, port)
        identity_facts.append(fact)
        identity_states.append(fact.state)
        port.charge(len(fact.support_refs) + len(fact.reason_codes) + 2)
        identity_sources.extend(fact.support_refs)
        identity_codes.extend(fact.reason_codes)
        for source in fact.support_refs:
            involved.append(_analysis_lookup(prepared, source.record_id, port))
    port.charge(8)
    identity = _IdentitySelection(_p._aggregate(identity_states, port),
        _analysis_unique_addresses(_o._tuple(identity_sources, port), port),
        _analysis_codes(identity_codes, port), _o._tuple(identity_facts, port))
    for code in identity.reason_codes:
        for source in identity.support_refs:
            _problem(problems, code, _analysis_lookup(prepared, source.record_id, port), port)
    coverage, premises = [], []
    coverage_context = _p._context(context, port, subjects=_o._tuple(ids, port),
        predicates=predicates, coverage_kind=coverage_kind, view=context.graph_view)
    for entity in prepared.entities:
        port.charge(2)
        if entity.collection != 'assertions' or _field(entity.node.fields, 'assertion_kind', port) != 'assessment':
            continue
        supplied = _field(entity.node.fields, 'data', port)
        if _field(supplied, 'assessment_kind', port) != 'coverage':
            continue
        detail = _field(supplied, 'details', port)
        if _field(detail, 'coverage_kind', port) != coverage_kind:
            continue
        relevant = False
        subjects = _field(supplied, 'subject_refs', port).items
        for identifier in (context.inquiry_ref, evaluation.identifier) + _o._tuple(ids, port):
            if _analysis_contains(subjects, identifier, port):
                relevant = True
        if not relevant:
            continue
        native_context = coverage_context
        if not _analysis_scope(entity, native_context, port, subjects=False):
            native_context = projections[-1].context
            if not _analysis_scope(entity, native_context, port, subjects=False):
                continue
        qualification = _qualify_coverage(prepared, (entity.identifier,), native_context, port)[0]
        coverage.append(qualification)
        involved.append(entity)
        for code in qualification.reason_codes:
            _problem(problems, code, entity, port)
    if not coverage:
        _problem(problems, 'upstream_coverage_incomplete', evaluation, port)
    disclosures = _o._unique_entities(prepared, involved, port)
    basis_context = _p._context(local, port, subjects=())
    metadata_basis_context = _p._context(projections[-1].context, port, subjects=())
    for entity in disclosures:
        premise_context = basis_context
        if entity.collection == 'assertions' and not _field(_field(entity.node.fields, 'scope', port), 'claim_refs', port).items:
            premise_context = metadata_basis_context
        for qualification in coverage:
            port.charge(1)
            if qualification.coverage is entity:
                premise_context = qualification.context
        premise = _p._premise(prepared, entity, premise_context, premises, port)
        for code in _p._codes(premise, port):
            _problem(problems, code, entity, port)
    role_supports = _o._unique_entities(prepared, role_supports, port)
    port.charge(len(disclosures) + len(role_supports) + 2)
    disclosures = _o._unique_entities(prepared, disclosures + role_supports, port)
    port.charge(39)
    facts = _EvaluatorFacts(prepared, context, port, inquiry, evaluation, roles,
        _o._tuple(bindings, port), role_supports, sides[0], sides[1], graph, _o._tuple(reaches, port), shared,
        _o._tuple(common, port), _o._tuple(paired, port), _o._tuple(one_sided, port),
        _o._tuple(matches, port), _o._tuple(representatives, port), _o._unique_entities(prepared, missing, port),
        _o._tuple(coverage, port), identity, _o._tuple(premises, port), disclosures,
        _o._tuple(problems, port), complete, pc04, _o._tuple(witnesses, port), _o._tuple(positive, port))
    port.check()
    return facts


def _scope(facts, port):
    claims, coverage = [], []
    for identifier in facts.context.claim_refs:
        claims.append(_profile_ref(_analysis_lookup(facts.prepared, identifier, port), port))
    for fact in facts.coverage:
        coverage.append(_profile_ref(fact.coverage, port))
    for refs in (claims, coverage):
        for ref in refs:
            _charge_input_ref(ref, port, repeats=len(refs) + 3)
    for role in facts.roles:
        _analysis_text(role, port)
    context = facts.context
    if context.requested_time is not None:
        _charge_frozen(context.requested_time.fields, port)
    port.charge(24)
    return _r._Scope(_profile_ref(facts.inquiry, port), _o._tuple(claims, port),
        (_profile_ref(facts.evaluation, port),), context.dependency_dimension, context.graph_view,
        context.temporal_basis, context.requested_time, _o._tuple(coverage, port),
        ('Exactly two supplied Evaluation roles in one named view; exact selected Claims and separately scoped inquiry metadata. '
         'Incomplete outside history and unexamined dimensions remain unresolved.',),
        facts.roles)


def _disclosures(facts, port):
    rows = []
    for entity in facts.disclosures:
        native = _p._native_fields(facts.prepared, entity, port)
        _charge_frozen(native, port)
        fields = [('native_record', native)]
        if entity is facts.evaluation:
            port.charge(len(facts.left_objects) + len(facts.right_objects) + len(facts.shared_objects) +
                len(facts.common_ancestors) + len(facts.missing_family_models) + 8)
            for name, values in (('roles', facts.roles),
                                 ('left_object_refs', tuple(e.identifier for e in facts.left_objects)),
                                 ('right_object_refs', tuple(e.identifier for e in facts.right_objects)),
                                 ('shared_object_refs', tuple(e.identifier for e in facts.shared_objects)),
                                 ('common_ancestor_refs', tuple(e.identifier for e in facts.common_ancestors)),
                                 ('matching_family_labels', facts.matching_family_labels),
                                 ('missing_family_model_refs', tuple(e.identifier for e in facts.missing_family_models))):
                for value in values:
                    _analysis_text(value, port)
                port.charge(len(values) + 3)
                fields.append((name, _Array(values)))
            one_sided = []
            for start, target, unused in facts.one_sided:
                _analysis_text(start.identifier, port)
                _analysis_text(target.identifier, port)
                one_sided.append(_freeze_object([('from_ref', start.identifier), ('to_ref', target.identifier)], port))
            fields.append(('one_sided_ancestry', _Array(_o._tuple(one_sided, port))))
            fields.append(('roles_complete', facts.roles_complete))
        frozen = _freeze_object(fields, port)
        port.charge(6)
        rows.append(_r._Disclosure(_profile_ref(entity, port), frozen,
            ('Native supplied record with provenance, role qualifications, gaps and subset descriptors retained. '
             'A common reviewed target is not review-process ancestry. Dataset identity describes only the '
             'supplied dataset granularity; exact training-row overlap and error correlation are unestablished.',)))
    port.charge(len(rows) + 3)
    return _r._RecordDisclosures(_o._tuple(rows, port))


def _reasons(facts, scope, ref, port):
    output = []
    for code in _r.REASON_CODES:
        sources = []
        for candidate, source in facts.problems:
            port.charge(1)
            if candidate == code:
                sources.append(source)
        if not sources:
            continue
        refs = []
        for source in _analysis_unique_addresses(_o._tuple(sources, port), port):
            refs.append(_o._source_ref(source, port))
        for source in refs:
            _charge_input_ref(source, port, repeats=len(refs) + 3)
        for unused in range(3):
            _charge_scope(scope, port)
        port.charge(len(refs) + 15)
        output.append(_r._Reason(code, scope, (ref,), _o._tuple(refs, port),
            'Exact role-pair limitation; known positive records survive partial history, and no absence implies independence.',
            'conflict' if code == 'premise_disputed' else 'evidence_gap'))
    return _o._tuple(output, port)


def _checks(facts, ref, port):
    checks = [_scope_check(_ScopeCheckFact(ref, ref.scope), port)]
    rows = [('PC01', 'met', (), ()), ('PC03', 'not_applicable', (), ()),
            ('PC04', facts.pc04.state, facts.pc04.input_refs, ()),
            ('PC08', facts.identity.state, facts.identity.support_refs, facts.identity.reason_codes),
            ('PC14', 'met' if facts.roles_complete else 'unmet',
             (_analysis_address(facts.evaluation, port),), ())]
    port.charge(len(facts.premises) + 1)
    rows.extend(_p._premise_checks(facts.premises, port))
    coverage_sources, coverage_states, coverage_codes = [], [], []
    for fact in facts.coverage:
        port.charge(len(fact.reason_codes) + 3)
        coverage_sources.append(fact.source)
        coverage_states.append(fact.state)
        coverage_codes.extend(fact.reason_codes)
    rows.append(('PC06', _p._aggregate(coverage_states, port, empty='unknown'),
        _o._tuple(coverage_sources, port), _analysis_codes(coverage_codes, port)))
    for check_id, state, sources, unused in rows:
        refs = []
        for address in _analysis_unique_addresses(sources, port):
            refs.append(_o._source_ref(address, port))
        for source in refs:
            _charge_input_ref(source, port, repeats=len(refs) + 3)
        port.charge(len(refs) + 12)
        checks.append(_r._PrerequisiteCheck(check_id, ref, state, _o._tuple(refs, port), (),
            'Executed selected role-pair prerequisite. PC03 seed-source enumeration is inapplicable. '
            'Recorded positive lineage does not require complete outside history or documentary authentication.'))
    return checks


def _evaluator_lineage_results(facts, port):
    _analysis_port(port)
    port.charge(5)
    _require(type(facts) is _EvaluatorFacts and facts.job_port is port)
    _check_projection(facts.graph, port)
    scope = _scope(facts, port)
    basis_addresses = [_analysis_address(facts.evaluation, port)]
    for reference in facts.role_supports:
        basis_addresses.append(_analysis_address(reference, port))
    for fact in facts.premises:
        port.charge(len(fact.basis.support_refs) + len(fact.conflict.support_refs) + 3)
        basis_addresses.append(_analysis_address(fact.source, port))
        basis_addresses.extend(fact.basis.support_refs)
        basis_addresses.extend(fact.conflict.support_refs)
    basis = []
    for address in _analysis_unique_addresses(_o._tuple(basis_addresses, port), port):
        source = _o._source_ref(address, port)
        _charge_input_ref(source, port)
        port.charge(3)
        basis.append(_r._BasisRef(source))
    basis = _o._tuple(basis, port)
    all_witness_refs, positive_refs = [], []
    for index, witness in enumerate(facts.witnesses):
        meaning, is_positive = witness.kind, False
        for candidate, retained in facts.positive_witnesses:
            port.charge(1)
            if retained is witness:
                meaning, is_positive = candidate, True
                break
        _analysis_text(meaning, port)
        _charge_scope(scope, port)
        port.charge(8)
        link = _r._WitnessRef(scope, 'path' if witness.kind == 'path' else
            'cycle' if witness.kind == 'cycle' else 'member_set', (meaning, str(index)))
        all_witness_refs.append(link)
        if is_positive:
            positive_refs.append(link)
    all_witness_refs = _o._tuple(all_witness_refs, port)
    positive_refs = _o._tuple(positive_refs, port)
    outputs = []
    for field in _FIELDS:
        witness_refs = positive_refs if field == _FIELDS[3] else all_witness_refs
        _charge_scope(scope, port)
        port.charge(180)
        ref = _r._ResultRef('SIT-M008', field, scope)
        members = []
        if field == _FIELDS[0]:
            for entity in facts.common_ancestors:
                members.append(_profile_ref(entity, port))
            unit, origin = 'record', 'graph_derivation'
        elif field == _FIELDS[1]:
            for entity in facts.family_representatives:
                members.append(_profile_ref(entity, port, 'data.family_label'))
            unit, origin = 'family_label', 'inventory'
        else:
            members = [_profile_ref(facts.evaluation, port)]
            unit, origin = 'evaluation', 'attributed_record' if field == _FIELDS[2] else 'graph_derivation'
        members = _o._tuple(members, port)
        for member in members:
            _charge_input_ref(member, port, repeats=len(members) + 3)
        port.charge(len(members) * len(members) + 18)
        population = _r._Population(scope, unit, members,
            'Unique strict common recorded ancestors, or exact supplied family strings represented by one native label field; '
            'disclosures and witnesses concern only the explicitly selected Evaluation role pair.',
            (), (), 'enumerated_for_scope',
            ('Recorded-view inventory only. No hidden records, additional roles, fuzzy labels or independent votes are inferred.',))
        state = 'available'
        if field in (_FIELDS[0], _FIELDS[1]) and not facts.roles_complete:
            state, value = 'unavailable', None
        elif field == _FIELDS[2]:
            value = _disclosures(facts, port)
        elif field == _FIELDS[3]:
            port.charge(len(witness_refs) * len(witness_refs) + 4)
            value = _r._WitnessCollection(witness_refs)
        else:
            port.charge(4)
            value = _r._Count(len(members), population)
        reasons = _reasons(facts, scope, ref, port)
        checks = _checks(facts, ref, port)
        components = []
        for name, links in (('premises', members), ('conflicts', reasons), ('value', (ref,)),
                            ('basis', basis), ('reasons', reasons), ('witnesses', witness_refs)):
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
            for links in (checks, basis, witness_refs, reasons):
                for link in links:
                    _charge_link(link, port)
        port.charge(len(checks) + len(basis) + len(witness_refs) + len(reasons) + 32)
        outputs.append(_r._Result(ref, (population,), 'completed', state, origin,
            _r._field_kind('SIT-M008', field), value, _o._tuple(checks, port), basis, witness_refs, reasons,
            'Actual represented roles in the named view only. Exact identity, nonreflexive strict ancestry, one-sided '
            'paths and family strings are separate. A completed zero is restricted to the inspected supplied graph or '
            'labels. Partial training and rubric history, missing labels and dataset-row granularity remain disclosed. '
            'No behavioral error correlation, model quality, process independence or global independence follows.'))
    result = _o._tuple(outputs, port)
    port.check()
    return result


def _evaluator_lineage(prepared, context, ledger, port):
    facts = _evaluator_lineage_facts(prepared, context, ledger, port)
    results = _evaluator_lineage_results(facts, port)
    port.charge(4)
    answer = _EvaluatorProfile(facts, results, facts.witnesses)
    port.check()
    return answer
