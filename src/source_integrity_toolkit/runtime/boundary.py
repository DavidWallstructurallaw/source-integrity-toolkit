# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: RUNTIME_BOUNDARY.

Private capture, preparation and complete bounded analytical orchestration.
The existing preparation seams retain their return types. Analytical admission
uses the same helpers and accepts only after its full finite structural job
plan. One execution context owns admission, current-job work and delivery.
No public auditing, file access, options, callbacks or report export is added.
"""
from ..contracts.execution import _PreparationAborted, _AuditCancelled
from ..io.input_file import _decode_utf8
from ..validation.structure import _capture_tree
from ..validation.limits import _InputLedger
from .resources import _new_budget
from .diagnostics import _diagnostic, _emergency_diagnostic


def _capture(value: object, *, supplied_utf8: bool):
    # Mode is a tool-owned constant selected by the two private entry points.
    # The budget and ledger are never supplied by source data or callers.
    budget = None
    try:
        budget = _new_budget()
        mode = "supplied_utf8" if supplied_utf8 else "constructed_value"
        ledger = _InputLedger(budget, mode)
        try:
            result = _decode_utf8(value, ledger) if supplied_utf8 else _capture_tree(value, ledger)
            budget.check()
            return result
        except (_PreparationAborted, _AuditCancelled):
            raise
        except KeyboardInterrupt:
            budget.cancel()
        except Exception:
            budget.fail()
    except (_PreparationAborted, _AuditCancelled) as cause:
        # Return a constant diagnostic, never the raw exception or a partial
        # snapshot. A constructor failure can precede assignment of the budget.
        return _diagnostic(cause) if budget is None else _emergency_diagnostic(budget)


def _prepare_value(value: object):
    """Private full preparation of an exact built-in root dict."""
    return _prepare(value, supplied_utf8=False)


def _prepare_utf8(raw: object):
    """Private full preparation of supplied bytes; no file-open claim."""
    return _prepare(raw, supplied_utf8=True)


def _capture_value(value: object):
    """Private capture-only seam retained for W04 component conformance.

    This does not perform W05 dossier validation or establish input acceptance.
    No options, validation bypass, public export or caller budget is introduced.
    """
    return _capture(value, supplied_utf8=False)


def _capture_utf8(raw: object):
    """Private capture of already supplied bytes; no complete-dossier claim."""
    return _capture(raw, supplied_utf8=True)


from ..contracts.evidence import _PreparedBundle
from ..validation.structure import _validate_structure, _shape_walk, _local_rules, _validate_gaps
from ..validation.references import _validate_references, _normalize, _index, _check_links, _scope_plan
from ..validation.semantics import _validate_semantics


def _admit(value: object, *, supplied_utf8: bool, budget):
    """Shared bounded admission work; the caller owns the acceptance boundary."""
    mode = "supplied_utf8" if supplied_utf8 else "constructed_value"
    ledger = _InputLedger(budget, mode)
    captured = _decode_utf8(value, ledger) if supplied_utf8 else _capture_tree(value, ledger)
    occurrences = _validate_structure(captured, ledger)
    entities = _validate_references(captured, occurrences, budget)
    _validate_semantics(occurrences, budget)
    normalized = _normalize(captured.tree, entities, budget)
    # A second paid pass addresses normalized selectors. It never counts
    # the same payload twice against input-size/occurrence ceilings.
    final_occurrences = _shape_walk(normalized, ledger, count=False)
    _local_rules(final_occurrences, budget)
    _validate_gaps(final_occurrences, budget)
    final_entities = _index(normalized, budget)
    links = _check_links(final_occurrences, final_entities, budget, retain=True)
    observations = _validate_semantics(final_occurrences, budget)
    plan = _scope_plan(final_entities, budget)
    budget.charge(len(final_entities) + len(links) + len(plan) + len(observations) + 10)
    result = _PreparedBundle(normalized, mode, final_entities, links, plan, observations, captured.tree)
    return result


def _run_preparation(value: object, *, supplied_utf8: bool, evidence_domains: bool):
    """One nonresetting budget; no partial snapshot on any stopping path."""
    budget = None
    try:
        budget = _new_budget()
        try:
            result = _admit(value, supplied_utf8=supplied_utf8, budget=budget)
            budget.record_input_acceptance()
            budget.check()
            if evidence_domains:
                observed = _observe_evidence_input(result, budget)
                result = _assemble_observability(result, observed, budget)
                budget.check()
            return result
        except (_PreparationAborted, _AuditCancelled):
            raise
        except KeyboardInterrupt:
            budget.cancel()
        except Exception:
            budget.fail()
    except (_PreparationAborted, _AuditCancelled) as cause:
        return _diagnostic(cause) if budget is None else _emergency_diagnostic(budget)


from ..contracts.report import (
    FAMILY_PREPARATION_BINDINGS, PREREQUISITE_OWNERS, PREREQUISITES,
    DOMAIN_LABELS, _PendingCheck, _DomainPreparation, _PrerequisitePreparation,
    _FamilyPreparation, _InquiryEvidence, _ObservabilityPreparation,
)
from ..validation.semantics import _observe_evidence_input


def _prepare(value: object, *, supplied_utf8: bool):
    # Preserve the W05 component seam and its exact outcome type.
    return _run_preparation(value, supplied_utf8=supplied_utf8, evidence_domains=False)


def _prepare_evidence_value(value: object):
    """W06 private pipeline: admission then evidence navigation, one budget."""
    return _run_preparation(value, supplied_utf8=False, evidence_domains=True)


def _prepare_evidence_utf8(raw: object):
    """Already supplied bytes only. No path, options or caller budget."""
    return _run_preparation(raw, supplied_utf8=True, evidence_domains=True)


def _assemble_observability(prepared, observed, budget):
    """Assemble the compiled contract; interpretation stays with later owners.

    Family question sets are navigation unions, not all-leaf mandatory gates.
    Empty binding lists describe this completed finite scan only. Unbound
    snapshot material is retained and no real-world absence is asserted.
    """
    snapshot, observed_inquiries = observed
    inquiries = []
    for inquiry_ref, bindings, records in observed_inquiries:
        families, domains, checks = [], [], []
        for name, fields, questions, unused_domains in FAMILY_PREPARATION_BINDINGS:
            refs = []
            for record in records:
                budget.charge(len(record.families) + 1)
                if name in record.families:
                    refs.append(record.record_id)
            note = "direct_supplied_bindings_only" if refs else "no_direct_binding_after_finite_scan"
            budget.charge(len(refs) + len(fields) + len(questions) + 30)
            families.append(_FamilyPreparation(name, fields, questions, tuple(refs), note))
        for index, unused_label in DOMAIN_LABELS:
            supplied = []
            for record in records:
                budget.charge(len(record.domains) + 1)
                if index not in record.domains:
                    continue
                for facet in record.facets:
                    budget.charge(2)
                    if facet.present:
                        supplied.append(facet.selector)
            pending = []
            for pc in PREREQUISITES[1:]:
                relevant = False
                for unused_name, unused_fields, questions, domain_ids in FAMILY_PREPARATION_BINDINGS:
                    budget.charge(len(questions) + len(domain_ids) + 2)
                    if index in domain_ids and pc in questions:
                        relevant = True
                if relevant:
                    budget.charge(30)
                    pending.append(_PendingCheck(pc))
            budget.charge(2 * len(supplied) + 2 * len(pending) + 5)
            domains.append(_DomainPreparation(index, tuple(supplied), tuple(pending)))
        for pc, owner in PREREQUISITE_OWNERS:
            constituents = []
            if pc != "PC01":
                for record in records:
                    for facet in record.facets:
                        budget.charge(len(facet.questions) + 2)
                        if pc in facet.questions:
                            constituents.append(facet)
            budget.charge(2 * len(constituents) + 35)
            checks.append(_PrerequisitePreparation(pc, pc == "PC01", "met" if pc == "PC01" else None,
                None if pc == "PC01" else owner, tuple(constituents)))
        budget.charge(3 * (len(bindings) + len(records) + len(families) + len(domains) + len(checks)) + 10)
        inquiries.append(_InquiryEvidence(inquiry_ref, bindings, records, tuple(families), tuple(domains), tuple(checks)))
    budget.charge(2 * len(snapshot) + 2 * len(inquiries) + 10)
    result = _ObservabilityPreparation(prepared, snapshot, tuple(inquiries))
    budget.check()
    return result


# W13 private analytical invocation. The preparation seams above retain their
# original return types and do not acquire analytical completion authority.
from ..contracts.bundle import _require, _Object, _Array, _Number, _compare_text
from ..contracts.evidence import _QualificationContext, _Entity, _Node, _SourceAddress
from ..contracts.execution import _AnalysisAborted, _byte_work
from ..contracts import results as _r
from ..contracts.report import (_charge_link, _charge_scope, _charge_frozen,
    _ScopeCheckFact, _scope_check, _ComponentCompletion, _CompletionRecord, _completion_check)
from ..validation.structure import _field
from ..validation.semantics import (
    _analysis_lookup, _analysis_ids, _analysis_text, _analysis_contains,
    _analysis_subset, _profile_ref, _provenance_profile, _observe_inquiry_bindings, _is_member,
)
from ..analysis import inventory as _inventory_owner
from ..analysis import origins as _origin_owner
from ..analysis import process_comparison as _comparison_owner
from ..analysis import contribution_profile as _contribution_owner
from ..analysis import evaluator_lineage as _evaluator_owner
from ..analysis import presence as _presence_owner
from ..analysis import correction_routes as _route_owner
from ..analysis import correction_outcomes as _outcome_owner
from ..analysis import human_review as _human_owner
from ..analysis import context as _context_owner
from ..analysis import findings as _finding_owner
from ..graph.projections import _project, _check_edge_eligibility, _GraphNode, _GraphEdge, _relation_view, _record_view, _native_selector
from ..graph.witnesses import _GraphWitness
from .resources import _new_analysis_budget
from .diagnostics import _analytical_diagnostic, _emergency_analytical_diagnostic


def _ordered_text(values, port):
    """Paid exact ID ordering with no qualification during admission."""
    port.charge(len(values) + 1)
    pairs = _analysis_ids(tuple(values), port)
    port.charge(len(pairs) + 1)
    return tuple(pair[0] for pair in pairs)


def _plan_context(inquiry, claims, port, *, subjects=(), dimension=None,
                  view=None, coverage=None, predicates=(), anchor=()):
    for values in (claims, subjects, predicates, anchor):
        port.charge(len(values) + 1)
        for value in values:
            if type(value) is str:
                _analysis_text(value, port)
    # The Inquiry supplies an as-of request; no runtime timestamp is invented.
    at = _field(inquiry.node.fields, 'as_of', port)
    known = _field(at, 'state', port) == 'known'
    if known:
        _charge_frozen(at, port)
    port.charge(20)
    return _QualificationContext(inquiry.identifier, claims, subjects, dimension,
        'time_specific' if known else 'snapshot_structural', _Node('TimeValue', at) if known else None,
        coverage, predicates, view, anchor)


def _structural_scope(entity, inquiry, claims, port):
    scope = _field(entity.node.fields, 'scope', port)
    if not _analysis_contains(_field(scope, 'inquiry_refs', port).items, inquiry.identifier, port):
        return False
    native = _field(scope, 'claim_refs', port).items
    return not native or _analysis_subset(claims, native, port)


def _raw_stage_anchor(entity, port):
    data = _field(entity.node.fields, 'data', port)
    values = []
    for name in ('run_key', 'stage_key', 'stage'):
        value = _field(data, name, port)
        _analysis_text(value, port)
        port.charge(1)
        values.append(value)
    port.charge(4)
    return tuple(values)


def _plan_compare(left, right, port):
    """Keys contain only bounded strings and tuples of bounded strings."""
    port.charge(2)
    if type(left) is str:
        return _compare_text(left, right, port)
    for a, b in zip(left, right):
        port.charge(1)
        result = _plan_compare(a, b, port)
        if result:
            return result
    port.charge(1)
    return (len(left) > len(right)) - (len(left) < len(right))


def _plan_analysis(prepared, budget):
    """Complete finite structural scheduling before input acceptance.

    Selection reads admitted native IDs/bindings only. It performs no premise,
    ancestry, documentary, availability or time qualification. All semantic
    helpers run later under their current capability/scope job.
    """
    from ..contracts.report import _AnalyticalJobSpec, _AnalyticalPlan
    jobs = []
    for binding in prepared.plan:
        inquiry = binding.inquiry
        claims = _ordered_text(_field(inquiry.node.fields, 'target_claim_refs', budget).items, budget)
        dimensions = _ordered_text(_field(inquiry.node.fields, 'dependency_dimensions', budget).items, budget)
        object_ids = _field(inquiry.node.fields, 'target_object_refs', budget).items
        records, assertions, coverages, externalities, comparisons, stages, anomalies, stances = [], [], [], [], [], [], [], []
        inquiry_members = claims + object_ids + _field(inquiry.node.fields, 'seed_artifact_refs', budget).items + _field(inquiry.node.fields, 'seed_evidence_refs', budget).items
        for entity in prepared.entities:
            budget.charge(1)
            if entity.kind == 'anomaly' and _analysis_contains(_field(_field(entity.node.fields, 'data', budget), 'inquiry_refs', budget).items, inquiry.identifier, budget):
                budget.charge(len(inquiry_members) + 1)
                inquiry_members += (entity.identifier,)
        for entity in prepared.entities:
            budget.charge(1)
            if entity.collection == 'assertions':
                scope = _field(entity.node.fields, 'scope', budget)
                if not _analysis_contains(_field(scope, 'inquiry_refs', budget).items, inquiry.identifier, budget):
                    continue
                budget.charge(1)
                assertions.append(entity)
                data = _field(entity.node.fields, 'data', budget)
                if _field(entity.node.fields, 'assertion_kind', budget) == 'assessment':
                    kind = _field(data, 'assessment_kind', budget)
                    if kind == 'coverage':
                        coverages.append(entity)
                    elif kind == 'externality':
                        externalities.append(entity)
                    elif kind == 'independence':
                        comparisons.append(entity)
                elif _field(data, 'predicate', budget) in _context_owner._STANCES:
                    stances.append(entity)
            elif entity.collection == 'records':
                budget.charge(1)
                records.append(entity)
                if entity.kind == 'pipeline_record':
                    data = _field(entity.node.fields, 'data', budget)
                    if _analysis_contains(inquiry_members, _field(data, 'subject_ref', budget), budget):
                        stages.append(entity)
                elif entity.kind == 'anomaly':
                    data = _field(entity.node.fields, 'data', budget)
                    if _analysis_contains(_field(data, 'inquiry_refs', budget).items, inquiry.identifier, budget):
                        anomalies.append(entity)
        def add(family, key, context, parameters=()):
            budget.charge(len(parameters) + len(key) + 20)
            fields = next(row[1] for row in FAMILY_PREPARATION_BINDINGS if row[0] == family)
            budget.charge(15 + len(fields))
            jobs.append(_AnalyticalJobSpec(inquiry.identifier, family, key, context, parameters))
        review_bindings = []
        for entity in records:
            budget.charge(1)
            if entity.kind != 'evaluation':
                continue
            native_targets = _field(_field(entity.node.fields, 'data', budget), 'target_refs', budget).items
            if not (_analysis_contains(object_ids, entity.identifier, budget) or any(
                    _analysis_contains(inquiry_members, identifier, budget) for identifier in native_targets)):
                continue
            selected_claims = []
            for claim in claims:
                tied = _analysis_contains(native_targets, claim, budget)
                for target in native_targets:
                    native = _analysis_lookup(prepared, target, budget)
                    if native.kind == 'evidence_item':
                        bound = _field(_field(native.node.fields, 'data', budget), 'claim_ref', budget)
                        tied = _compare_text(bound, claim, budget) == 0 or tied
                    elif native.kind == 'artifact':
                        for identifier in _field(inquiry.node.fields, 'seed_evidence_refs', budget).items:
                            evidence = _analysis_lookup(prepared, identifier, budget)
                            data = _field(evidence.node.fields, 'data', budget)
                            tied = (_field(data, 'artifact_ref', budget) == target and
                                    _field(data, 'claim_ref', budget) == claim) or tied
                if tied:
                    budget.charge(1)
                    selected_claims.append(claim)
            budget.charge(len(selected_claims) + 3)
            review_bindings.append((entity, tuple(selected_claims)))
        base = _plan_context(inquiry, claims, budget)
        for claim in claims:
            add('SIT-M001', ('inventory', claim), _plan_context(inquiry, (claim,), budget))
            for dimension in dimensions:
                for family in ('SIT-M002', 'SIT-M004', 'SIT-M005', 'SIT-M006', 'SIT-M007'):
                    add(family, ('claim_dimension', claim, dimension), _plan_context(inquiry, (claim,), budget,
                        dimension=dimension, view='claim_origin', coverage='upstream_history', predicates=_origin_owner._PARENTS))
                selected = []
                for assessment in comparisons:
                    data = _field(assessment.node.fields, 'data', budget)
                    detail = _field(data, 'details', budget)
                    if (_field(detail, 'dimension', budget) == dimension and
                            _structural_scope(assessment, inquiry, (claim,), budget)):
                        selected.append(assessment)
                for assessment in selected or (None,):
                    identifier = None if assessment is None else assessment.identifier
                    add('SIT-M003', ('assessment', claim, dimension, identifier or 'no_assessment'),
                        _plan_context(inquiry, (claim,), budget, dimension=dimension), (identifier,))
                # Only actual Claim-bound Evaluations enter this Claim job.
                # A missing selection must not invoke the owner's empty-tuple
                # default when it would import another Claim's Evaluation.
                selected_reviews = tuple(entity.identifier for entity, tied in review_bindings
                    if _analysis_contains(tied, claim, budget))
                budget.charge(len(selected_reviews) + 1)
                if selected_reviews or not review_bindings:
                    add('SIT-M013', ('human_contribution', claim, dimension),
                        _plan_context(inquiry, (claim,), budget, subjects=selected_reviews, dimension=dimension))
            add('SIT-M015', ('provenance', claim), _plan_context(inquiry, (claim,), budget,
                view='assertion_assurance'))
        for evaluation, evaluation_claims in review_bindings:
            if not evaluation_claims:
                for dimension in dimensions:
                    add('SIT-M013', ('inquiry_evaluation', evaluation.identifier, dimension),
                        _plan_context(inquiry, claims, budget, subjects=(evaluation.identifier,), dimension=dimension))
            native = _field(_field(evaluation.node.fields, 'data', budget), 'role_bindings', budget).items
            supplied_roles = [_field(item, 'role', budget) for item in native]
            roles = []
            for role in _evaluator_owner._ROLES:
                if _analysis_contains(tuple(supplied_roles), role, budget):
                    budget.charge(1)
                    roles.append(role)
            if len(roles) < 2:
                add('SIT-M008', ('incomplete_roles', evaluation.identifier),
                    _plan_context(inquiry, evaluation_claims, budget, subjects=(evaluation.identifier,)))
            for index, first in enumerate(roles):
                for second in roles[index + 1:]:
                    budget.charge(2)
                    for dimension in dimensions:
                        view = ('organizational' if dimension == 'organizational_control' else
                            'material_transformation' if dimension == 'acquisition' else 'model_evaluation')
                        budget.charge(3)
                        mapping = next(row for row in _evaluator_owner._VIEWS if row[0] == view)
                        add('SIT-M008', ('role_pair', evaluation.identifier, first, second, dimension, view),
                            _plan_context(inquiry, evaluation_claims, budget, subjects=(evaluation.identifier,), dimension=dimension,
                                view=view, coverage=mapping[2], predicates=mapping[1], anchor=(first, second)))
        for assessment in externalities:
            native_claims = _field(_field(assessment.node.fields, 'scope', budget), 'claim_refs', budget).items
            selected_claims = tuple(claim for claim in claims if _analysis_contains(native_claims, claim, budget))
            budget.charge(len(selected_claims) + 1)
            add('SIT-M009', ('externality', assessment.identifier),
                _plan_context(inquiry, selected_claims or claims, budget), (assessment.identifier,))
        stage_specs = []
        covered_anchors = []
        for coverage in coverages:
            data = _field(coverage.node.fields, 'data', budget)
            details = _field(data, 'details', budget)
            if _field(details, 'coverage_kind', budget) != 'pipeline_universe':
                continue
            native_claims = _field(_field(coverage.node.fields, 'scope', budget), 'claim_refs', budget).items
            selected_claims = tuple(claim for claim in claims if _analysis_contains(native_claims, claim, budget))
            anchors = []
            for identifier in _field(data, 'subject_refs', budget).items:
                subject = _analysis_lookup(prepared, identifier, budget)
                if subject.kind == 'pipeline_record':
                    anchor = _raw_stage_anchor(subject, budget)
                    if not any(_plan_compare(anchor, old, budget) == 0 for old in anchors):
                        budget.charge(1)
                        anchors.append(anchor)
            anchor = anchors[0] if len(anchors) == 1 else None
            if anchor is not None:
                budget.charge(1)
                covered_anchors.append(anchor)
            key = ('cohort', coverage.identifier) + (anchor or ('unestablished',))
            add('SIT-M010', key, _plan_context(inquiry, selected_claims or claims, budget,
                view='pipeline_stages'), (coverage.identifier, anchor))
            budget.charge(4)
            stage_specs.append((coverage.identifier, anchor, selected_claims or claims,
                _field(details, 'member_refs', budget).items))
        uncov = []
        for stage in stages:
            anchor = _raw_stage_anchor(stage, budget)
            if any(_plan_compare(anchor, old, budget) == 0 for old in uncov):
                continue
            budget.charge(1)
            uncov.append(anchor)
            add('SIT-M010', ('stage',) + anchor, _plan_context(inquiry, claims, budget,
                view='pipeline_stages'), (None, anchor))
            members = []
            for source in stages:
                if _plan_compare(_raw_stage_anchor(source, budget), anchor, budget) == 0:
                    budget.charge(1)
                    members.append(_field(_field(source.node.fields, 'data', budget), 'subject_ref', budget))
            budget.charge(len(members) + 4)
            stage_specs.append((None, anchor, claims, tuple(members)))
        # Native channel target/action tuples and structurally reachable supplied
        # propagation records define a finite request set. No dossier all-pairs.
        for channel in records:
            budget.charge(1)
            if channel.kind != 'correction_channel':
                continue
            data = _field(channel.node.fields, 'data', budget)
            actions = _ordered_text(_field(data, 'declared_action_types', budget).items, budget)
            for action in actions:
                targets = list(_field(data, 'target_refs', budget).items)
                frontier = [channel.identifier] + targets
                seen = []
                while frontier:
                    budget.charge(len(frontier) + 2)
                    current = frontier.pop()
                    if _analysis_contains(tuple(seen), current, budget):
                        continue
                    seen.append(current)
                    for assertion in assertions:
                        obj = assertion.node.fields
                        if _field(obj, 'assertion_kind', budget) != 'relation':
                            continue
                        relation = _field(obj, 'data', budget)
                        if (_field(relation, 'predicate', budget) == 'propagates_to' and
                                _field(relation, 'from_ref', budget) == current and
                                _field(_field(relation, 'details', budget), 'action_type', budget) == action):
                            destination = _field(relation, 'to_ref', budget)
                            budget.charge(2)
                            targets.append(destination)
                            frontier.append(destination)
                for identifier in _ordered_text(tuple(targets), budget):
                    if not _analysis_contains(inquiry_members, identifier, budget):
                        continue
                    target = _analysis_lookup(prepared, identifier, budget)
                    if target.kind not in _route_owner._TARGETS and target.collection != 'assertions':
                        continue
                    add('SIT-M011', ('route', channel.identifier, identifier, action),
                        _plan_context(inquiry, claims, budget, subjects=(channel.identifier, identifier),
                            view='correction_routing', coverage='correction_routes', predicates=('propagates_to',), anchor=(action,)))
        # Cases are selected by an actual Inquiry Claim/object/seed binding.
        relevant = claims + object_ids + _field(inquiry.node.fields, 'seed_artifact_refs', budget).items + _field(inquiry.node.fields, 'seed_evidence_refs', budget).items
        for case in records:
            if case.kind != 'correction_event':
                continue
            data = _field(case.node.fields, 'data', budget)
            if (_field(data, 'event_kind', budget) == 'submission' and
                    any(_analysis_contains(relevant, target, budget) for target in _field(data, 'target_refs', budget).items)):
                add('SIT-M012', ('case', case.identifier), _plan_context(inquiry, claims, budget,
                    subjects=(case.identifier,), view='correction_outcomes'))
        for selected_claim in claims:
            add('SIT-M014', ('native_context', selected_claim), _plan_context(inquiry, (selected_claim,), budget,
                view='stance_contestation', anchor=('native_context', selected_claim)), ())
        add('SIT-M014', ('inquiry_context',), _plan_context(inquiry, (), budget,
            view='stance_contestation', anchor=('inquiry_context',)), ())
        tail_subjects = [entity.identifier for entity in anomalies]
        for stance in stances:
            data = _field(stance.node.fields, 'data', budget)
            for name in ('from_ref', 'to_ref'):
                entity = _analysis_lookup(prepared, _field(data, name, budget), budget)
                if entity.kind == 'evidence_item':
                    budget.charge(1)
                    tail_subjects.append(entity.identifier)
        for coverage, anchor, selected_claims, members in stage_specs:
            selected = _ordered_text(tuple(subject for subject in tail_subjects
                if _analysis_contains(members, subject, budget)), budget)
            if selected:
                key = ('tail_stage', coverage or 'native_stage') + (anchor or ('unestablished',))
                add('SIT-M014', key, _plan_context(inquiry, selected_claims, budget, subjects=selected,
                    view='stance_contestation', anchor=key), ((coverage, anchor),))
        # Each explicit scoped relation supplies only its own endpoint query.
        # No unrequested pairwise product or future semantic owner is executed.
        for assertion in assertions:
            obj = assertion.node.fields
            if _field(obj, 'assertion_kind', budget) != 'relation':
                continue
            data = _field(obj, 'data', budget)
            predicate = _field(data, 'predicate', budget)
            dimension = _field(data, 'dimension', budget)
            budget.charge(12)
            view = _relation_view(predicate, dimension)
            if view not in ('citation', 'material_transformation', 'claim_origin', 'model_evaluation',
                            'succession', 'assertion_assurance'):
                continue
            if dimension is not None and not _analysis_contains(dimensions, dimension, budget):
                continue
            native_claims = _field(_field(obj, 'scope', budget), 'claim_refs', budget).items
            selected_claims = tuple(claim for claim in claims if _analysis_contains(native_claims, claim, budget))
            if native_claims and not selected_claims:
                continue
            selections = tuple((claim,) for claim in selected_claims) if view == 'claim_origin' else (selected_claims,)
            start = _field(data, 'from_ref', budget)
            target = _field(data, 'to_ref', budget)
            predicates = (_origin_owner._PARENTS if view == 'claim_origin' else
                _evaluator_owner._VIEWS[1][1] if view == 'material_transformation' else
                _evaluator_owner._VIEWS[0][1] if view == 'model_evaluation' else (predicate,))
            for selected in selections:
                key = ('graph_witness', assertion.identifier) + selected
                coverage = 'upstream_history' if view in ('claim_origin', 'material_transformation') else 'model_history' if view == 'model_evaluation' else None
                parameters = ('graph_request', view, dimension, selected, predicates, coverage, start, target)
                add('SIT-M014', key, _plan_context(inquiry, claims, budget, anchor=key), parameters)
        unused_bindings, bound_members = _observe_inquiry_bindings(prepared, binding, budget)
        canonical_keys = []
        for link in prepared.links:
            budget.charge(1)
            if not _is_member(bound_members, link.owner.identifier, budget):
                continue
            selector = _native_selector(link, budget)
            if _record_view(link.owner, selector, budget) != 'assertion_assurance':
                continue
            key = ('canonical_assurance', link.owner.identifier, selector, link.target.identifier)
            if any(_plan_compare(key, old, budget) == 0 for old in canonical_keys):
                continue
            budget.charge(1)
            canonical_keys.append(key)
            # Canonical metadata links preserve the source's actual Claim
            # scope. A multi-Claim Inquiry must not make a C2-only assurance
            # relation disappear behind an invented (C1, C2) conjunction.
            explicit_claims = None
            native_claims = []
            for endpoint in (link.owner, link.target):
                budget.charge(1)
                if endpoint.collection == 'assertions':
                    if explicit_claims is None:
                        explicit_claims = _field(_field(endpoint.node.fields, 'scope', budget), 'claim_refs', budget).items
                elif endpoint.kind == 'claim':
                    native_claims.append(endpoint.identifier)
                elif endpoint.kind == 'evidence_item':
                    native_claims.append(_field(_field(endpoint.node.fields, 'data', budget), 'claim_ref', budget))
            candidates = tuple(native_claims) if explicit_claims is None else explicit_claims
            selected = tuple(claim for claim in claims if _analysis_contains(candidates, claim, budget))
            budget.charge(len(native_claims) + len(selected) + 2)
            parameters = ('graph_request', 'assertion_assurance', None, selected, (), None,
                link.owner.identifier, link.target.identifier)
            add('SIT-M014', key, _plan_context(inquiry, claims, budget, anchor=key), parameters)
        for family in (row[0] for row in FAMILY_PREPARATION_BINDINGS):
            present = False
            for job in jobs:
                budget.charge(2)
                if job.inquiry_ref == inquiry.identifier and job.family == family:
                    present = True
            if not present:
                if family == 'SIT-M009':
                    add(family, ('missing_assessment',), base, (None,))
                elif family == 'SIT-M010':
                    add(family, ('missing_stage_history',), _plan_context(inquiry, claims, budget, view='pipeline_stages'), (None, None))
                elif family == 'SIT-M012':
                    add(family, ('case_inventory',), _plan_context(inquiry, claims, budget, view='correction_outcomes'), ())
                else:
                    add(family, ('no_subject',), base, ())
    # Architecture 19.2 requires a paid bottom-up stable merge schedule.
    budget.charge(len(jobs) + 1)
    ordered = list(jobs)
    width = 1
    while width < len(ordered):
        merged = []
        for start in range(0, len(ordered), 2 * width):
            middle, end = min(start + width, len(ordered)), min(start + 2 * width, len(ordered))
            left, right = start, middle
            while left < middle or right < end:
                budget.charge(3)
                if right == end:
                    take_left = True
                elif left == middle:
                    take_left = False
                else:
                    a, b = ordered[left], ordered[right]
                    compared = _plan_compare((a.inquiry_ref, a.family, a.operation_key),
                        (b.inquiry_ref, b.family, b.operation_key), budget)
                    _require(compared != 0)
                    take_left = compared < 0
                budget.charge(1)
                if take_left:
                    merged.append(ordered[left]); left += 1
                else:
                    merged.append(ordered[right]); right += 1
        ordered = merged
        budget.charge(1)
        width *= 2
    # The contract independently revisits every job/key; prepay its finite pass.
    for job in ordered:
        _plan_compare((job.inquiry_ref, job.family, job.operation_key),
            (job.inquiry_ref, job.family, job.operation_key), budget)
    budget.charge(len(ordered) * 20 + 20)
    result = _AnalyticalPlan(tuple(ordered))
    budget.check()
    return result


def _planned_nonresults(prepared, spec, port, *, execution='completed', code='no_applicable_subject', fields=None):
    """Explicit finite scope explanations or unexecuted cells, without values."""
    context = spec.context
    inquiry = _profile_ref(_analysis_lookup(prepared, spec.inquiry_ref, port), port)
    claims = tuple(_profile_ref(_analysis_lookup(prepared, identifier, port), port) for identifier in context.claim_refs)
    targets = tuple(_profile_ref(_analysis_lookup(prepared, identifier, port), port) for identifier in context.subject_refs)
    port.charge(len(claims) + len(targets) + len(spec.operation_key) + 20)
    scope = _r._Scope(inquiry, claims, targets, context.dependency_dimension, context.graph_view,
        context.temporal_basis, context.requested_time, (),
        ('The structural job key identifies the exact planned operation; no outside-world absence is inferred.',),
        spec.operation_key)
    output = []
    for field in spec.field_keys if fields is None else fields:
        _charge_scope(scope, port)
        port.charge(30)
        ref = _r._ResultRef(spec.family, field, scope)
        classification = ('execution' if execution != 'completed' else
            'structural_inapplicability' if code == 'no_applicable_subject' else 'evidence_gap')
        state = ('not_evaluated' if execution != 'completed' else
            'not_applicable' if code == 'no_applicable_subject' else 'unavailable')
        detail = ('No eligible subject tuple was supplied for this finite operation.' if code == 'no_applicable_subject'
            else 'An actual Evaluation lacks a pair of supplied distinct roles.' if code == 'roles_incomplete'
            else 'Processing stopped before this cell made a complete availability decision.')
        reason = _r._Reason(code, scope, (ref,), targets, detail, classification)
        kind = _r._field_kind(spec.family, field)
        checks = ()
        if execution == 'completed':
            port.charge(15)
            admitted = _r._PrerequisiteCheck('PC01', ref, 'met', (inquiry,), (),
                'The same invocation completed admission before this scheduled structural scope explanation.')
            scoped = _scope_check(_ScopeCheckFact(ref, scope), port)
            components = []
            for name, links in (('premises', (inquiry,) + targets), ('conflicts', ()),
                    ('value', (ref,)), ('basis', ()), ('reasons', (reason,)), ('witnesses', ())):
                for link in links:
                    _charge_link(link, port)
                    _charge_link(link, port)
                port.charge(len(links) * len(links) + 8)
                components.append(_ComponentCompletion(name, links, links))
            port.charge(len(components) + 8)
            complete = _completion_check(_CompletionRecord(ref, (), (), tuple(components)), port)
            checks = (admitted, scoped, complete)
        output.append(_r._Result(ref, (), execution, state, 'qualification_check', kind, None,
            checks, (), (), (reason,), detail))
    port.charge(len(output) + 1)
    return tuple(output)


def _payload(value, port):
    """Detach actual immutable witness material without execution authorities."""
    port.charge(1)
    if value is None or type(value) in (bool, int):
        return value
    if type(value) is str:
        _analysis_text(value, port)
        return value
    if type(value) is tuple:
        parts = [_payload(part, port) for part in value]
        port.charge(len(parts) + 1)
        return tuple(parts)
    if type(value) is _Entity:
        port.charge(5)
        result = _r._InputRef(value.collection, value.identifier)
        _charge_link(result, port)
        return result
    if type(value) is _GraphNode:
        return _payload(('node', _r._InputRef(value.collection, value.identifier), value.kind), port)
    if type(value) is _GraphEdge:
        return _payload(('edge', value.source, value.target, value.key, value.source_ref,
            value.predicate, value.eligible, value.reason_codes), port)
    if type(value) is _SourceAddress:
        port.charge(5)
        result = _r._InputRef(value.collection, value.record_id, value.selector or None)
        _charge_link(result, port)
        return result
    if type(value) is _r._InputRef:
        _charge_link(value, port)
        return value
    if type(value) in (_Object, _Array, _Number):
        _charge_frozen(value, port)
        return value
    if type(value) is _GraphWitness:
        context = value.graph.context
        material = []
        for name, items in (('nodes', value.nodes), ('edges', value.edges), ('members', value.members),
                ('internal_edges', value.internal_edges), ('exit_edges', value.exit_edges), ('starts', value.starts),
                ('target', value.target), ('examined_nodes', value.examined_nodes), ('examined_edges', value.examined_edges),
                ('frontiers', value.frontiers), ('terminals', value.terminals), ('observations', value.observations)):
            port.charge(1)
            material.append((name, _payload(items, port)))
        port.charge(len(material) + 8)
        return ('graph_witness', value.kind, context.inquiry_ref, context.claim_refs,
            context.dependency_dimension, context.graph_view, context.operation_anchor,
            tuple(material), value.member_count)
    if type(value) is _inventory_owner._InventoryWitness:
        return _payload(('inventory_witness', value.members, value.member_count), port)
    if type(value) is _comparison_owner._ComparisonWitness:
        return _payload(('comparison_witness', value.assessment, value.members,
            value.examined_assessments, value.member_count), port)
    if type(value) in (_presence_owner._PresenceWitness, _context_owner._ContextWitness):
        return _payload(('selected_members', value.members, value.member_count), port)
    if type(value) is _human_owner._ReviewWitness:
        return _payload(('human_review_witness', value.members, value.examined_assessments,
            value.source_refs, value.member_count), port)
    if type(value) is _outcome_owner._OutcomeWitness:
        return _payload(('correction_outcome_witness', value.members, value.source_refs, value.member_count), port)
    raise TypeError('unsupported_private_witness_payload')


def _matching_witnesses(profile, ref, port):
    """Resolve the original owner's finite witness anchor without widening it."""
    anchor = ref.anchor
    head = anchor[0]
    witnesses = profile.witnesses
    if type(profile) is _inventory_owner._InventoryProfile:
        matches = []
        for witness in witnesses:
            _charge_link(witness.ref, port)
            _charge_link(ref, port)
            if witness.ref._key() == ref._key():
                matches.append(witness)
        return tuple(matches)
    if type(profile) in (_evaluator_owner._EvaluatorProfile, _route_owner._CorrectionProfile):
        port.charge(len(witnesses) + 4)
        matches = tuple(witness for index, witness in enumerate(witnesses) if str(index) == anchor[-1])
        _require(len(matches) == 1)
        return matches
    if head == 'corrective_comparison':
        for comparison in profile.facts.comparisons:
            _analysis_text(comparison.facts.assessment.identifier, port)
            _charge_link(anchor[1], port)
            if comparison.facts.assessment.identifier == anchor[1].identifier:
                port.charge(len(anchor) + 5)
                local = _r._WitnessRef(ref.scope, ref.kind, anchor[2:])
                return _matching_witnesses(comparison, local, port)
        raise TypeError('unresolved_private_comparison_witness')
    selected = []
    for witness in witnesses:
        port.charge(3)
        if head == 'comparison_selection' and type(witness) is _comparison_owner._ComparisonWitness:
            selected.append(witness)
        elif head == 'human_review_selection' and type(witness) is _human_owner._ReviewWitness:
            selected.append(witness)
        elif head == 'correction_case_selection' and type(witness) is _outcome_owner._OutcomeWitness:
            selected.append(witness)
        elif head == 'context_preservation' and type(witness) is _context_owner._ContextWitness:
            selected.append(witness)
        elif head == 'presence_selection' and type(witness) is _presence_owner._PresenceWitness:
            selected.append(witness)
        elif type(witness) is _GraphWitness:
            if type(profile) is _contribution_owner._ContributionProfile:
                if head == 'complete_trace' and witness is profile.facts.origin_facts.inventory_witness:
                    selected.append(witness)
                elif head == 'immediate_complete_trace' and witness.starts:
                    _analysis_text(witness.starts[0].identifier, port)
                    _charge_link(anchor[1], port)
                    if witness.starts[0].identifier == anchor[1].identifier:
                        selected.append(witness)
            elif witness.kind == head:
                expected = []
                if type(profile) is _comparison_owner._ComparisonProfile:
                    for claim in witness.graph.context.claim_refs:
                        expected.append(_profile_ref(_analysis_lookup(profile.facts.prepared, claim, port), port))
                nodes = ((witness.nodes[0],) if witness.kind == 'cycle' else
                    (witness.nodes[0], witness.nodes[-1]) if witness.kind == 'path' else witness.starts)
                for node in nodes:
                    expected.append(_profile_ref(_analysis_lookup(profile.facts.prepared, node.identifier, port), port))
                port.charge(len(expected) + len(anchor) + 2)
                if len(expected) != len(anchor) - 1:
                    continue
                same = True
                for actual, wanted in zip(expected, anchor[1:]):
                    _charge_link(actual, port); _charge_link(wanted, port)
                    if actual._key() != wanted._key():
                        same = False
                if same:
                    selected.append(witness)
    port.charge(len(selected) + 1)
    _require(bool(selected))
    return tuple(selected)


def _detach_witnesses(profile, port):
    from ..contracts.report import _WitnessRecord
    refs, seen, records = [], set(), []
    for result in profile.results:
        for ref in result.witness_refs:
            _charge_link(ref, port)
            port.charge(3)
            key = ref._key()
            if key not in seen:
                seen.add(key)
                refs.append(ref)
    # Each symbolic anchor retains exactly its actual owner payload. Shared
    # payload tuples are immutable; no new witness reservation is invented.
    payload_cache = []
    for ref in refs:
        selected = _matching_witnesses(profile, ref, port)
        parts, members = [], 0
        for witness in selected:
            cached = None
            for old, value in payload_cache:
                port.charge(1)
                if old is witness:
                    cached = value
                    break
            if cached is None:
                cached = _payload(witness, port)
                port.charge(1)
                payload_cache.append((witness, cached))
            port.charge(2)
            parts.append(cached)
            members += witness.member_count
        port.charge(len(parts) + 10)
        records.append(_WitnessRecord((ref,), tuple(parts), (), members))
    port.charge(len(records) + 1)
    return tuple(records)


def _detach_findings(findings, port):
    from ..contracts.report import _DetachedFindingWitness, _PrivateFinding
    output = []
    for finding in findings:
        witness = finding.witness
        payloads = tuple(_payload(value, port) for value in witness.owner_witnesses)
        for source in witness.input_refs:
            _charge_link(source, port)
        port.charge(len(payloads) + len(witness.input_refs) + 10)
        detached = _DetachedFindingWitness(witness.input_refs, payloads, witness.member_count)
        for links in (finding.population_refs, finding.basis_refs, finding.contrary_input_refs,
                      finding.reason_refs, finding.result_refs):
            for link in links:
                _charge_link(link, port)
        _charge_scope(finding.scope_ref, port)
        for disclosure in finding.native_records:
            _charge_frozen(disclosure.fields, port)
            _charge_link(disclosure.source, port)
        for text in (finding.statement, finding.interpretation_limit):
            _analysis_text(text, port)
        port.charge(len(finding.native_records) + 22)
        output.append(_PrivateFinding(finding.observation_kind, finding.condition_code,
            finding.diagnostic_refs, finding.threat_family_refs, finding.scope_ref, finding.population_refs,
            finding.basis_refs, detached, finding.contrary_input_refs, finding.reason_refs,
            finding.result_refs, finding.statement, finding.interpretation_limit, finding.native_records))
    port.charge(len(output) + 1)
    return tuple(output)


def _commit_job(port, results, findings, witnesses):
    """Publish only fully built immutable cells under the actual current job."""
    for result in results:
        _charge_link(result.ref, port)
    port.charge(len(results) + len(findings) + len(witnesses) + 4)
    previous = port._committed
    if previous is None:
        previous = ((), (), ())
    port.charge(sum(len(rows) for rows in previous) + 3)
    committed = (previous[0] + results, previous[1] + findings, previous[2] + witnesses)
    port.check()
    port._committed = committed


def _provenance_selection(prepared, context, port):
    """Reuse the original finite source-binding owner in this current job."""
    members = None
    for binding in prepared.plan:
        port.charge(1)
        if binding.inquiry.identifier == context.inquiry_ref:
            unused, members = _observe_inquiry_bindings(prepared, binding, port)
            break
    _require(members is not None)
    records, references, coverage = [], [], []
    for entity in prepared.entities:
        port.charge(1)
        if not _is_member(members, entity.identifier, port):
            continue
        if entity.collection == 'evidence_references':
            references.append(entity.identifier)
        else:
            records.append(entity.identifier)
        if entity.collection == 'assertions':
            obj = entity.node.fields
            if (_field(obj, 'assertion_kind', port) == 'assessment' and
                    _field(_field(obj, 'data', port), 'assessment_kind', port) == 'coverage'):
                coverage.append(entity.identifier)
    port.charge(len(records) + len(references) + len(coverage) + 3)
    return tuple(records), tuple(references), tuple(coverage)


def _execute_job(prepared, spec, ledger, port):
    """Run only the scheduled job; pure owner helpers debit this same port."""
    family, context, parameters = spec.family, spec.context, spec.parameters
    if spec.operation_key[0] in ('no_subject', 'incomplete_roles'):
        code = 'roles_incomplete' if spec.operation_key[0] == 'incomplete_roles' else 'no_applicable_subject'
        output = _planned_nonresults(prepared, spec, port, code=code)
        _commit_job(port, output, (), ())
        return port._committed
    if family == 'SIT-M015':
        inventory = _inventory_owner._inventory_facts(prepared, context, port)
        graph = _project(prepared, context, port)
        provider = _check_edge_eligibility(graph, graph.observations, port)
        records, references, coverage = _provenance_selection(prepared, context, port)
        output = _provenance_profile(prepared, context, records, references, coverage, port,
            provider_facts=(inventory.pc03, provider))
        admitted_rows = []
        for result in output.results:
            _charge_link(result.ref, port)
            for links in (result.population_refs, result.check_refs, result.basis_refs,
                          result.witness_refs, result.reason_refs):
                for link in links:
                    _charge_link(link, port)
                port.charge(len(links) * len(links) + len(links) + 1)
            # This is a second Result construction, including its key walks
            # and interpretation-text replacement, so the first owner's debit
            # cannot be reused for it. Prepay all additional inspected bytes.
            _byte_work(port, 4 * (len(result.interpretation_limit) + 100), 3)
            interpretation = result.interpretation_limit.replace('provider integration remains pending.',
                'Actual same-job PC03 and PC04 provider facts are linked.')
            port.charge(len(result.check_refs) + 30)
            pc01 = _r._PrerequisiteCheck('PC01', result.ref, 'met', (), (),
                'The same invocation completed structural admission and its full analytical plan before acceptance.')
            admitted_rows.append(_r._Result(result.ref, result.population_refs, result.execution_state,
                result.result_state, result.result_origin, result.value_kind, result.value,
                (pc01,) + result.check_refs, result.basis_refs, result.witness_refs, result.reason_refs, interpretation))
        port.charge(len(admitted_rows) + 1)
        _commit_job(port, tuple(admitted_rows), (), ())
        return port._committed
    if family == 'SIT-M001':
        profile = _inventory_owner._inventory_profile(prepared, context, ledger, port)
    elif family in ('SIT-M002', 'SIT-M007'):
        profile = _origin_owner._origin_profile(prepared, context, ledger, port, family=family)
    elif family == 'SIT-M003':
        profile = _comparison_owner._comparison_profile(prepared, context, parameters[0], ledger, port)
    elif family in ('SIT-M004', 'SIT-M005', 'SIT-M006'):
        profile = _contribution_owner._contribution_profile(prepared, context, ledger, port, family=family)
    elif family == 'SIT-M008':
        profile = _evaluator_owner._evaluator_lineage(prepared, context, ledger, port)
    elif family == 'SIT-M009':
        profile = _presence_owner._presence(prepared, context, ledger, port, family=family, assessment_ref=parameters[0])
    elif family == 'SIT-M010':
        profile = _presence_owner._presence(prepared, context, ledger, port, family=family,
            coverage_ref=parameters[0], stage_anchor=parameters[1])
    elif family == 'SIT-M011':
        profile = _route_owner._correction_routes(prepared, context, ledger, port)
    elif family == 'SIT-M012':
        profile = _outcome_owner._correction_outcomes(prepared, context, ledger, port)
    elif family == 'SIT-M013':
        profile = _human_owner._human_review(prepared, context, ledger, port)
    elif family == 'SIT-M014':
        profile = _context_owner._context_preservation(prepared, context, ledger, port,
            stage_requests=() if parameters and parameters[0] == 'graph_request' else parameters)
    else:
        raise TypeError('unregistered_analytical_family')
    # M014 owns its native context. Its original M010 helper outcomes are also
    # retained, so every actual tail link resolves without a copied metric.
    profiles = []
    if family == 'SIT-M014':
        port.charge(len(profile.facts.stage_profiles))
        profiles.extend(profile.facts.stage_profiles)
    port.charge(1)
    profiles.append(profile)
    for local in profiles:
        witnesses = _detach_witnesses(local, port)
        _commit_job(port, local.results, (), witnesses)
    # Completed owner cells survive a later findings interruption in this same
    # current job. No result can be supplied by an earlier semantic cache.
    graph_requests = ()
    if family == 'SIT-M014' and parameters and parameters[0] == 'graph_request':
        unused, view, dimension, claims, predicates, coverage, start, target = parameters
        port.charge(len(claims) + len(predicates) + 20)
        query = _QualificationContext(context.inquiry_ref, claims, (), dimension, context.temporal_basis,
            context.requested_time, coverage, predicates, view, context.operation_anchor)
        graph_requests = ((query, start, target),)
    finding_profile = _finding_owner._findings(prepared, context, ledger, port,
        stage_profiles=(profile,), graph_requests=graph_requests)
    findings = _detach_findings(finding_profile.findings, port)
    _commit_job(port, (), findings, ())
    return port._committed


def _analyze_value(value: object):
    """Private full analysis of an exact built-in value, with fixed budgets."""
    return _run_analysis(value, supplied_utf8=False)


def _analyze_utf8(raw: object):
    """Private full analysis of supplied bytes only, without file access."""
    return _run_analysis(raw, supplied_utf8=True)


def _run_analysis(value: object, *, supplied_utf8: bool):
    from ..contracts.report import _JobOutcome, _assemble_analysis
    budget = None
    try:
        budget = _new_analysis_budget()
        try:
            prepared = _admit(value, supplied_utf8=supplied_utf8, budget=budget)
            plan = _plan_analysis(prepared, budget)
            budget.record_input_acceptance()
            results, findings, witnesses, job_outcomes = [], [], [], []
            interrupted = None
            for index, spec in enumerate(plan.jobs):
                job = budget.start_job()
                try:
                    _execute_job(prepared, spec, budget.witnesses, job)
                    budget.finish_job(job)
                except _AnalysisAborted:
                    if budget._stop_kind not in ('job', 'witness'):
                        raise
                    interrupted = index
                committed = job._committed or ((), (), ())
                # Already paid immutable tuples move to the delivery collector.
                # Collection allocation is charged to finalization if stopped.
                if interrupted is not None:
                    break
                budget.charge(sum(len(items) for items in committed) + 10)
                results.extend(committed[0]); findings.extend(committed[1]); witnesses.extend(committed[2])
                job_outcomes.append(_JobOutcome(spec, tuple(result.ref for result in committed[0]), 'completed',
                    spec.operation_key[0] == 'no_subject'))
            port = budget.begin_finalization()
            if interrupted is not None:
                port.charge(sum(len(items) for items in committed) + 10)
                results.extend(committed[0]); findings.extend(committed[1]); witnesses.extend(committed[2])
                for index in range(interrupted, len(plan.jobs)):
                    spec = plan.jobs[index]
                    existing = committed[0] if index == interrupted else ()
                    done = tuple(result.ref.field_key for result in existing if result.ref.diagnostic_id == spec.family)
                    port.charge(len(done) * len(spec.field_keys) + len(done) + 1)
                    missing = tuple(field for field in spec.field_keys if field not in done)
                    state = 'interrupted' if index == interrupted else 'not_performed'
                    unexecuted = _planned_nonresults(prepared, spec, port, execution=state,
                        code='resource_limit_reached', fields=missing)
                    port.charge(len(unexecuted) + len(existing) + 8)
                    results.extend(unexecuted)
                    job_outcomes.append(_JobOutcome(spec, tuple(result.ref for result in existing + unexecuted), state,
                        spec.operation_key[0] == 'no_subject'))
            port.charge(len(results) + len(findings) + len(witnesses) + len(job_outcomes) + 5)
            return _assemble_analysis(prepared, plan, tuple(job_outcomes), tuple(results), tuple(findings),
                tuple(witnesses), port, execution_state='interrupted' if interrupted is not None else 'completed')
        except (_PreparationAborted, _AnalysisAborted, _AuditCancelled):
            raise
        except KeyboardInterrupt:
            budget.cancel()
        except Exception:
            budget.fail()
    except (_PreparationAborted, _AnalysisAborted, _AuditCancelled) as cause:
        return _analytical_diagnostic(cause) if budget is None else _emergency_analytical_diagnostic(budget)
