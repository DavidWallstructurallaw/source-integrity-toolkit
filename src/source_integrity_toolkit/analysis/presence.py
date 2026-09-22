# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: PRESENCE_RECORDS. Private paid M009/M010 finite supplied profiles.

Definitions 25.2/26: externality, each keyed stage, and the restricted same-
population transition remain distinct. No scalar Presence or implicit funnel.
"""
from dataclasses import dataclass

from ..contracts.bundle import _require, _Array, _freeze_object, _compare_text
from ..contracts.evidence import _Node, _QualificationContext, _SourceAddress
from ..contracts import results as _r
from ..contracts.report import (
    _charge_scope, _charge_input_ref, _charge_link, _charge_frozen,
    _ScopeCheckFact, _scope_check, _PopulationCompletion, _ComponentCompletion,
    _CompletionRecord, _completion_check,
)
from ..validation.structure import _field
from ..validation.semantics import (
    _analysis_port, _analysis_start, _analysis_lookup, _analysis_contains,
    _analysis_subset, _analysis_text, _analysis_address, _analysis_codes,
    _analysis_scope, _analysis_current, _analysis_temporal, _qualify_basis,
    _qualify_conflicts, _qualify_identity, _qualify_coverage, _compare_times,
    _profile_ref,
)
from ..graph.projections import _project, _check_edge_eligibility
from .origins import _tuple, _unique_entities
from . import process_comparison as _shared

_EXTERNAL = ('externality_assessment_disclosures', 'externality_stage_links')
_PIPELINE = ('pipeline_stage_disclosures', 'stage_member_partition',
    'stage_occurrence_fraction', 'stage_occurrence_completion_interval',
    'cohort_transition_disclosures', 'cohort_transition_fraction',
    'cohort_transition_completion_interval')
_LIMIT = ('Supplied boundary and stage observations only. Unknowns remain in the full declared '
    'cohort. Native conclusions, use records and experimental attributions are not toolkit '
    'authentication or causal estimates. No date, human label, missing log, multiplied funnel, '
    'global Presence score or adequate-renewal claim follows. Transition quantities require '
    'the same exact members and one evidenced admission baseline; influence has no such transition.')


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Stage:
    record: object
    basis: object
    conflict: object
    identity: object
    temporal_state: str
    reason_codes: tuple


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Member:
    member: object
    classification: str
    records: tuple
    reason_codes: tuple


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Cohort:
    coverage: object
    anchor: object
    members: tuple
    rows: tuple
    eligible: bool
    reason_codes: tuple
    qualification: object
    qualifications: tuple
    conflicts: tuple
    identity: object
    stages: tuple
    basis_entities: tuple


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Mapping:
    subject: object
    stage_subject: object
    assertion: object
    graph: object
    provider: object


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _PresenceWitness:
    prepared: object
    context: object
    job_port: object
    members: tuple
    member_count: int


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _PresenceFacts:
    prepared: object
    context: object
    job_port: object
    inquiry: object
    family: str
    assessment: object
    subjects: tuple
    qualified_state: str
    assessment_basis: object
    assessment_conflict: object
    assessment_temporal: object
    assessment_native_time: str
    stages: tuple
    conflicts: tuple
    reason_codes: tuple
    target: object
    baselines: tuple
    baseline: object
    mappings: tuple
    basis_entities: tuple
    transition_basis: tuple
    stage_facts: tuple
    witnesses: tuple


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _PresenceProfile:
    facts: _PresenceFacts
    results: tuple
    witnesses: tuple


def _entities(prepared, identifiers, port):
    rows = []
    for identifier in identifiers:
        port.charge(1)
        rows.append(_analysis_lookup(prepared, identifier, port))
    return _unique_entities(prepared, rows, port)


def _ids(entities, port):
    rows = []
    for entity in entities:
        port.charge(1)
        rows.append(entity.identifier)
    return _tuple(rows, port)


def _refs(entities, port):
    rows = []
    for entity in entities:
        port.charge(1)
        rows.append(_profile_ref(entity, port))
    return _tuple(rows, port)


def _local(context, port, *, claims=None, dimension=None, view=None, kind=None, predicates=()):
    # Copying this context does not import subject-membership authority into
    # the generic helper. The owner separately checks exact native anchors.
    local = _shared._context(context, port, claims=claims, subjects=(), predicates=predicates,
                             coverage_kind=kind, view=view)
    port.charge(20)
    return _QualificationContext(local.inquiry_ref, local.claim_refs, (), dimension,
        local.temporal_basis, local.requested_time, kind, predicates, view, local.operation_anchor)


def _member_scope(entity, context, port):
    if entity.kind == 'evidence_item':
        return _analysis_contains(context.claim_refs, _field(_field(entity.node.fields, 'data', port), 'claim_ref', port), port)
    if entity.kind == 'anomaly':
        data = _field(entity.node.fields, 'data', port)
        claim = _field(data, 'claim_ref', port)
        return (_analysis_contains(_field(data, 'inquiry_refs', port).items, context.inquiry_ref, port)
                and (claim is None or _analysis_contains(context.claim_refs, claim, port)))
    return False


def _anchor(record, port):
    data = _field(record.node.fields, 'data', port)
    values = []
    for key in ('run_key', 'stage_key', 'stage'):
        value = _field(data, key, port)
        _analysis_text(value, port)
        port.charge(1)
        values.append(value)
    return _tuple(values, port)


def _same(left, right, port):
    port.charge(2)
    if left is None or right is None or len(left) != len(right):
        return left is right
    for a, b in zip(left, right):
        if _compare_text(a, b, port) != 0:
            return False
    return True


def _native_time(fields, context, port):
    if context.temporal_basis == 'snapshot_structural':
        port.charge(1)
        return 'not_applicable', ()
    port.charge(8)
    observed = _Node('TimeValue', fields)
    comparison = _compare_times(observed, context.requested_time, port)
    exact = (_field(fields, 'precision', port) == 'instant' and
             _field(context.requested_time.fields, 'precision', port) == 'instant' and
             comparison.comparison == 'equal')
    return ('met', ()) if exact else ('unknown', ('time_applicability_unknown',))


def _support_entities(prepared, qualifications, port):
    entities = []
    for fact in qualifications:
        if fact is None:
            continue
        for address in fact.support_refs:
            port.charge(1)
            entities.append(_analysis_lookup(prepared, address.record_id, port))
    return _unique_entities(prepared, entities, port)


def _stage(prepared, record, context, cache, port):
    for old in cache:
        port.charge(1)
        if old.record is record:
            return old
    data = _field(record.node.fields, 'data', port)
    subject = _analysis_lookup(prepared, _field(data, 'subject_ref', port), port)
    basis = _qualify_basis(prepared, record.identifier, context, port)
    conflict = _qualify_conflicts(prepared, record.identifier, context, port)
    identity = _qualify_identity(prepared, (subject.identifier,), context, port)
    temporal, time_codes = _native_time(_field(data, 'observed_at', port), context, port)
    port.charge(len(basis.reason_codes) + len(conflict.reason_codes) + len(identity.reason_codes) + len(time_codes) + 8)
    codes = list(basis.reason_codes + conflict.reason_codes + identity.reason_codes + time_codes)
    if not _member_scope(subject, context, port):
        codes.append('scope_unestablished')
    row = _Stage(record, basis, conflict, identity, temporal, _analysis_codes(codes, port))
    port.charge(1)
    cache.append(row)
    return row


def _stage_records(prepared, context, anchor, subjects, port):
    rows = []
    ids = _ids(subjects, port)
    for entity in prepared.entities:
        port.charge(1)
        if entity.kind != 'pipeline_record':
            continue
        data = _field(entity.node.fields, 'data', port)
        subject = _analysis_lookup(prepared, _field(data, 'subject_ref', port), port)
        if not _member_scope(subject, context, port):
            continue
        if subjects and not _analysis_contains(ids, subject.identifier, port):
            continue
        if anchor is not None and not _same(_anchor(entity, port), anchor, port):
            continue
        port.charge(1)
        rows.append(entity)
    return _unique_entities(prepared, rows, port)


def _coverage_anchor(prepared, coverage, port):
    data = _field(coverage.node.fields, 'data', port)
    anchors, codes = [], []
    for identifier in _field(data, 'subject_refs', port).items:
        subject = _analysis_lookup(prepared, identifier, port)
        if subject.kind == 'pipeline_record':
            key = _anchor(subject, port)
            found = False
            for old in anchors:
                port.charge(1)
                found = _same(old, key, port) or found
            if not found:
                port.charge(1)
                anchors.append(key)
        elif subject.collection != 'inquiries':
            port.charge(1)
            codes.append('cohort_anchor_ambiguous')
    if not anchors:
        codes.append('cohort_anchor_missing')
    elif len(anchors) != 1:
        codes.append('cohort_anchor_ambiguous')
    port.charge(3)
    return anchors[0] if len(anchors) == 1 and not codes else None, _analysis_codes(codes, port)


def _cohort(prepared, inquiry, context, coverage, requested, cache, port):
    codes, members, qualification, basis = [], (), None, [inquiry]
    qualifications = []
    conflicts, identity = [], None
    qualification_met = identity_met = False
    anchor = requested
    if coverage is None:
        codes.append('cohort_universe_unestablished')
    else:
        port.charge(1)
        basis.append(coverage)
        data = _field(coverage.node.fields, 'data', port)
        details = _field(data, 'details', port)
        native_anchor, anchor_codes = _coverage_anchor(prepared, coverage, port)
        port.charge(len(anchor_codes))
        codes.extend(anchor_codes)
        if requested is None:
            anchor = native_anchor
        elif native_anchor is not None and not _same(requested, native_anchor, port):
            codes.append('scope_unestablished')
        members = _entities(prepared, _field(details, 'member_refs', port).items, port)
        dimensions = _field(details, 'dimensions', port).items
        for dimension in dimensions or (None,):
            local = _local(context, port, dimension=dimension, kind='pipeline_universe', view='pipeline_stages')
            fact = _qualify_coverage(prepared, (coverage.identifier,), local, port)[0]
            # The generic coverage fact exposes its basis support, but not
            # the conflict provider's source addresses. Retain that actual
            # provider result in this same job for source-complete reporting.
            conflict = _qualify_conflicts(prepared, coverage.identifier, local, port)
            port.charge(len(fact.reason_codes) + 2)
            qualifications.append(fact)
            conflicts.append(conflict)
            codes.extend(fact.reason_codes)
        port.charge(len(qualifications) + 1)
        qualification = qualifications[0]
        qualification_met = all(fact.state == 'met' for fact in qualifications)
        for entity in _support_entities(prepared, qualifications, port):
            port.charge(1)
            basis.append(entity)
        for entity in _support_entities(prepared, conflicts, port):
            port.charge(1)
            basis.append(entity)
        if _field(details, 'coverage_kind', port) != 'pipeline_universe':
            codes.append('cohort_universe_unestablished')
        for member in members:
            port.charge(1)
            if not _member_scope(member, context, port):
                codes.append('scope_unestablished' if member.kind != 'unresolved_reference' else 'unknown_endpoint')
        member_ids = _ids(members, port)
        if context.subject_refs and not (_analysis_subset(context.subject_refs, member_ids, port) and
                                        _analysis_subset(member_ids, context.subject_refs, port)):
            codes.append('scope_unestablished')
        identity = _qualify_identity(prepared, member_ids, _local(context, port), port)
        identity_met = identity.state == 'met'
        port.charge(len(identity.reason_codes))
        codes.extend(identity.reason_codes)
        for entity in _support_entities(prepared, (identity,), port):
            port.charge(1)
            basis.append(entity)
    if anchor is None:
        codes.append('cohort_anchor_missing')
    records = _stage_records(prepared, context, anchor, (), port) if anchor is not None else ()
    stages, rows = [], []
    local = _local(context, port, view='pipeline_stages')
    for record in records:
        fact = _stage(prepared, record, local, cache, port)
        port.charge(2)
        stages.append(fact)
        basis.append(record)
        for entity in _support_entities(prepared, (fact.basis, fact.conflict, fact.identity), port):
            port.charge(1)
            basis.append(entity)
    for member in members:
        selected, row_codes, positives, negatives, yes, no = [], [], False, False, False, False
        for fact in stages:
            data = _field(fact.record.node.fields, 'data', port)
            if _compare_text(_field(data, 'subject_ref', port), member.identifier, port) != 0:
                continue
            port.charge(len(fact.reason_codes) + 1)
            selected.append(fact.record)
            row_codes.extend(fact.reason_codes)
            state = _field(data, 'state', port)
            # Even a bare contrary declaration survives. An unknown row is
            # additional uncertainty, never a positive/negative denial.
            positives = positives or state == 'occurred'
            negatives = negatives or state == 'did_not_occur'
            qualified = (fact.basis.state == fact.conflict.state == fact.identity.state == 'met'
                         and fact.temporal_state in ('met', 'not_applicable')
                         and _member_scope(member, context, port))
            yes = yes or state == 'occurred' and qualified
            no = no or state == 'did_not_occur' and qualified
        if positives and negatives:
            classification = 'U'
            row_codes.append('premise_disputed')
        elif yes:
            classification = 'Y'
        elif no:
            classification = 'F'
        else:
            classification = 'U'
            row_codes.append('stage_classification_unresolved')
        port.charge(7)
        rows.append(_Member(member, classification, _tuple(selected, port), _analysis_codes(row_codes, port)))
    codes = _analysis_codes(codes, port)
    port.charge(len(codes) + 3)
    eligible = (qualification_met and identity_met and
                not any(code != 'self_supporting_assurance' for code in codes))
    if not eligible:
        port.charge(len(codes) + 2)
        codes = _analysis_codes(codes + ('cohort_universe_unestablished',), port)
    port.charge(12)
    return _Cohort(coverage, anchor, members, _tuple(rows, port), eligible, codes,
        qualification, _tuple(qualifications, port), _tuple(conflicts, port), identity,
        _tuple(stages, port), _unique_entities(prepared, basis, port))


def _externality(prepared, inquiry, context, assessment_ref, cache, port):
    local = _local(context, port)
    assessment = None if assessment_ref is None else _analysis_lookup(prepared, assessment_ref, port)
    subjects = _entities(prepared, context.subject_refs, port)
    codes, conflicts, basis, mappings = [], [], [inquiry], []
    qualified = 'unknown'
    premise = conflict = timing = None
    temporal = 'unknown'
    if assessment is not None:
        _require(assessment.collection == 'assertions')
        data = _field(assessment.node.fields, 'data', port)
        _require(_field(data, 'assessment_kind', port) == 'externality')
        subjects = _entities(prepared, _field(data, 'subject_refs', port).items, port)
        details = _field(data, 'details', port)
        premise = _qualify_basis(prepared, assessment.identifier, local, port)
        conflict = _qualify_conflicts(prepared, assessment.identifier, local, port)
        timing = _analysis_temporal(assessment, local, port)
        temporal, native_time_codes = _native_time(_field(details, 'relevant_time', port), local, port)
        port.charge(len(premise.reason_codes) + len(conflict.reason_codes) + len(native_time_codes) + 2)
        codes.extend(premise.reason_codes + conflict.reason_codes + native_time_codes)
        basis.append(assessment)
        for source in _support_entities(prepared, (premise, conflict), port):
            port.charge(1)
            basis.append(source)
        if timing is not None:
            port.charge(len(timing.reason_codes))
            codes.extend(timing.reason_codes)
        ids = _ids(subjects, port)
        compatible = (_analysis_scope(assessment, local, port, subjects=False) and
            _compare_text(_field(details, 'boundary_inquiry_ref', port), context.inquiry_ref, port) == 0 and
            (not context.subject_refs or _analysis_subset(context.subject_refs, ids, port) and
             _analysis_subset(ids, context.subject_refs, port)))
        for subject in subjects:
            if subject.kind == 'evidence_item' and not _member_scope(subject, context, port):
                compatible = False
            elif subject.kind == 'unresolved_reference':
                codes.append('unknown_endpoint')
        if not compatible:
            codes.append('scope_unestablished')
        if (_field(details, 'grounding_basis', port) is None or
                _field(details, 'conclusion', port) == 'unknown' or
                _field(assessment.node.fields, 'lifecycle_state', port) != 'active'):
            codes.append('externality_unestablished')
        for candidate in prepared.entities:
            port.charge(1)
            if candidate.collection != 'assertions' or candidate is assessment:
                continue
            obj = candidate.node.fields
            if _field(obj, 'assertion_kind', port) != 'assessment':
                continue
            other = _field(obj, 'data', port)
            if _field(other, 'assessment_kind', port) != 'externality' or not _analysis_scope(candidate, local, port, subjects=False):
                continue
            other_details = _field(other, 'details', port)
            if _compare_text(_field(other_details, 'boundary_inquiry_ref', port), context.inquiry_ref, port) != 0:
                continue
            current, unused = _analysis_current(prepared, candidate, port)
            if not current:
                continue
            other_time = _analysis_temporal(candidate, local, port)
            if other_time is not None and other_time.state == 'unmet' and 'temporal_inconsistency' not in other_time.reason_codes:
                continue
            # Distinct known observation times are different boundary claims,
            # not a global contradiction across the entire snapshot.
            relevant = _compare_times(_Node('TimeValue', _field(details, 'relevant_time', port)),
                _Node('TimeValue', _field(other_details, 'relevant_time', port)), port)
            if relevant.comparison in ('before', 'after'):
                continue
            overlap = False
            for identifier in _field(other, 'subject_refs', port).items:
                overlap = _analysis_contains(ids, identifier, port) or overlap
            conclusion = _field(other_details, 'conclusion', port)
            native_conclusion = _field(details, 'conclusion', port)
            if overlap and conclusion != 'unknown' and native_conclusion != 'unknown' and conclusion != native_conclusion:
                port.charge(3)
                conflicts.append(candidate)
                basis.append(candidate)
                codes.append('premise_disputed')
        port.charge(len(codes) + 2)
        blockers = [code for code in codes if code != 'self_supporting_assurance']
        qualified = 'met' if not blockers and premise.state == conflict.state == 'met' else 'unmet'
    if qualified != 'met':
        codes.append('externality_unestablished')
    linked = []
    for subject in subjects:
        if subject.kind == 'evidence_item' and _member_scope(subject, context, port):
            port.charge(1)
            linked.append(subject)
        elif subject.kind == 'origin_event':
            # Actual single supplied E -> O links only, in their own native
            # dimension; there is no ancestor closure or Artifact join.
            for assertion in prepared.entities:
                port.charge(1)
                if assertion.collection != 'assertions' or _field(assertion.node.fields, 'assertion_kind', port) != 'relation':
                    continue
                data = _field(assertion.node.fields, 'data', port)
                if (_field(data, 'predicate', port) != 'originates_from' or
                        _compare_text(_field(data, 'to_ref', port), subject.identifier, port) != 0):
                    continue
                source = _analysis_lookup(prepared, _field(data, 'from_ref', port), port)
                if not _member_scope(source, context, port):
                    continue
                source_claim = _field(_field(source.node.fields, 'data', port), 'claim_ref', port)
                mapping_context = _local(context, port, claims=(source_claim,), dimension=_field(data, 'dimension', port),
                    view='claim_origin', predicates=('originates_from',))
                graph = _project(prepared, mapping_context, port)
                for edge in graph.edges:
                    port.charge(1)
                    if edge.source_entity is not assertion:
                        continue
                    proof = _qualify_basis(prepared, assertion.identifier, mapping_context, port)
                    if proof.state != 'met' or edge.reason_codes:
                        continue
                    provider = _check_edge_eligibility(graph, (edge,), port)
                    port.charge(6)
                    mappings.append(_Mapping(subject, source, assertion, graph, provider))
                    linked.append(source)
                    basis.append(assertion)
                    basis.extend(_support_entities(prepared, (proof,), port))
    linked = _unique_entities(prepared, linked, port)
    stages = _stage_records(prepared, context, None, linked, port) if linked else ()
    stage_facts = []
    for record in stages:
        fact = _stage(prepared, record, local, cache, port)
        port.charge(2)
        stage_facts.append(fact)
        basis.append(record)
        for source in _support_entities(prepared, (fact.basis, fact.conflict, fact.identity), port):
            port.charge(1)
            basis.append(source)
    return (assessment, subjects, qualified, stages, _unique_entities(prepared, conflicts, port),
        _analysis_codes(codes, port), _tuple(mappings, port), _unique_entities(prepared, basis, port),
        _tuple(stage_facts, port), premise, conflict, timing, temporal)


def _presence_facts(prepared, context, ledger, port, *, family, assessment_ref=None,
                    coverage_ref=None, stage_anchor=None):
    inquiry = _analysis_start(prepared, context, port)
    _shared._ledger(ledger, port)
    _require(family in ('SIT-M009', 'SIT-M010') and context.dependency_dimension is None)
    for claim in context.claim_refs:
        _require(_analysis_contains(_field(inquiry.node.fields, 'target_claim_refs', port).items, claim, port))
    if stage_anchor is not None:
        _require(type(stage_anchor) is tuple and len(stage_anchor) == 3 and stage_anchor[2] in
                 ('admission', 'preservation', 'selection', 'influence'))
        for part in stage_anchor:
            _analysis_text(part, port)
    cache, baselines = [], []
    target = baseline = None
    if family == 'SIT-M009':
        _require(coverage_ref is None and stage_anchor is None)
        (assessment, subjects, qualified, stages, conflicts, codes, mappings, basis, stage_facts,
         assessment_basis, assessment_conflict, assessment_temporal, assessment_native_time) = _externality(
            prepared, inquiry, context, assessment_ref, cache, port)
        transition_basis = basis
    else:
        _require(assessment_ref is None)
        coverage = None if coverage_ref is None else _analysis_lookup(prepared, coverage_ref, port)
        if coverage is not None:
            _require(coverage.collection == 'assertions')
            _require(_field(_field(coverage.node.fields, 'data', port), 'assessment_kind', port) == 'coverage')
        target = _cohort(prepared, inquiry, context, coverage, stage_anchor, cache, port)
        basis, codes, subjects = target.basis_entities, target.reason_codes, target.members
        stage_facts = target.stages
        stages = _unique_entities(prepared, [fact.record for fact in target.stages], port)
        transition_entities = list(basis)
        assessment, conflicts, mappings, qualified = None, (), (), 'met' if target.eligible else 'unmet'
        assessment_basis = assessment_conflict = assessment_temporal = None
        assessment_native_time = 'not_applicable'
        if target.anchor is not None and target.anchor[2] in ('preservation', 'selection'):
            local = _local(context, port)
            target_ids = _ids(target.members, port)
            keys = []
            for candidate in prepared.entities:
                port.charge(1)
                if candidate.collection != 'assertions' or candidate is coverage:
                    continue
                obj = candidate.node.fields
                if _field(obj, 'assertion_kind', port) != 'assessment':
                    continue
                data = _field(obj, 'data', port)
                if _field(data, 'assessment_kind', port) != 'coverage':
                    continue
                details = _field(data, 'details', port)
                if _field(details, 'coverage_kind', port) != 'pipeline_universe' or not _analysis_scope(candidate, local, port, subjects=False):
                    continue
                key, unused = _coverage_anchor(prepared, candidate, port)
                if key is None or key[2] != 'admission' or _compare_text(key[0], target.anchor[0], port) != 0:
                    continue
                current, unused = _analysis_current(prepared, candidate, port)
                if not current:
                    continue
                timing = _analysis_temporal(candidate, local, port)
                if timing is not None and timing.state == 'unmet' and 'temporal_inconsistency' not in timing.reason_codes:
                    continue
                candidate_members = _field(details, 'member_refs', port).items
                if not (_analysis_subset(candidate_members, target_ids, port) and _analysis_subset(target_ids, candidate_members, port)):
                    continue
                candidate_fact = _cohort(prepared, inquiry, context, candidate, key, cache, port)
                port.charge(len(candidate_fact.basis_entities) + 1)
                baselines.append(candidate_fact)
                transition_entities.extend(candidate_fact.basis_entities)
                found = False
                for previous in keys:
                    found = _same(previous, key, port) or found
                if not found:
                    port.charge(1)
                    keys.append(key)
            if target.eligible and len(keys) == 1:
                for candidate in baselines:
                    port.charge(len(candidate.rows) + 1)
                    if candidate.eligible and all(row.classification == 'Y' for row in candidate.rows):
                        baseline = candidate
                        break
        transition_basis = _unique_entities(prepared, transition_entities, port)
    # The retained finite source witness covers real selections and qualified
    # mapping assertions. Empty selections still have their Inquiry scan.
    port.charge(len(basis) + len(transition_basis) + 2)
    examined = _unique_entities(prepared, basis + transition_basis, port)
    reservation = ledger.reserve(witnesses=1, members=len(examined))
    for entity in examined:
        _analysis_address(entity, port)
    port.charge(8)
    witness = _PresenceWitness(prepared, context, port, examined, len(examined))
    ledger.retain(reservation)
    port.charge(24)
    facts = _PresenceFacts(prepared, context, port, inquiry, family, assessment, subjects,
        qualified, assessment_basis, assessment_conflict, assessment_temporal, assessment_native_time,
        stages, conflicts, codes, target, _tuple(baselines, port), baseline,
        mappings, basis, transition_basis, stage_facts, (witness,))
    port.check()
    return facts


def _check_facts(facts, port):
    _analysis_port(port)
    port.charge(3)
    _require(type(facts) is _PresenceFacts and facts.job_port is port)


def _scope(facts, transition, port):
    context = facts.context
    claims = _refs(_entities(facts.prepared, context.claim_refs, port), port)
    coverage, targets, anchor = [], [], []
    if facts.family == 'SIT-M009':
        targets = [facts.assessment] if facts.assessment is not None else list(facts.subjects)
        port.charge(len(context.operation_anchor) + 2)
        anchor = list(context.operation_anchor) or ['SIT-M009']
    else:
        if facts.target.coverage is not None:
            coverage.append(facts.target.coverage)
            targets.append(facts.target.coverage)
        port.charge(4)
        anchor = list(facts.target.anchor) if facts.target.anchor is not None else ['unestablished_stage']
        if transition:
            if facts.baseline is not None:
                port.charge(5)
                coverage.append(facts.baseline.coverage)
                anchor.extend(('from_admission',) + facts.baseline.anchor)
            else:
                anchor.append('unestablished_admission')
    targets = _refs(_unique_entities(facts.prepared, targets, port), port)
    coverage = _refs(_unique_entities(facts.prepared, coverage, port), port)
    for rows in (claims, targets, coverage):
        port.charge(len(rows) * len(rows) + len(rows) + 1)
        for ref in rows:
            _charge_input_ref(ref, port, repeats=len(rows) + 3)
    for part in anchor:
        if type(part) is str:
            _analysis_text(part, port)
    if context.requested_time is not None:
        _charge_frozen(context.requested_time.fields, port)
    port.charge(20)
    scope = _r._Scope(_profile_ref(facts.inquiry, port), claims, targets, None,
        context.graph_view, context.temporal_basis, context.requested_time, coverage,
        ('Native exact subject/key and declared finite coverage only; no implicit stage sequence or temporal persistence.',),
        _tuple(anchor, port))
    _charge_scope(scope, port)
    return scope


def _record(prepared, entity, additions, port):
    native = _shared._native_fields(prepared, entity, port)
    port.charge(len(native.items) + len(additions) + 2)
    fields = list(native.items) + list(additions)
    for name, value in fields:
        _analysis_text(name, port)
        _charge_frozen(value, port)
    fields = _freeze_object(fields, port)
    port.charge(6)
    return _r._Disclosure(_profile_ref(entity, port), fields,
        ('Unchanged native fields plus explicit documentary qualification. Supplied evidence is not authenticated; '
         'recorded use and external experimental attribution remain their original kinds.',))


def _disclosures(facts, field, port):
    rows = []
    if field == _EXTERNAL[0]:
        if facts.assessment is not None:
            rows.append(_record(facts.prepared, facts.assessment,
                (('qualification_state', facts.qualified_state),
                 ('qualified_externality', 'available' if facts.qualified_state == 'met' else 'unavailable'),
                 ('reason_codes', _Array(facts.reason_codes))), port))
        for entity in facts.conflicts:
            port.charge(1)
            rows.append(_record(facts.prepared, entity, (), port))
    elif field in (_EXTERNAL[1], _PIPELINE[0]):
        for fact in facts.stage_facts:
            additions = [('qualification_state', 'met' if fact.basis.state == fact.conflict.state == fact.identity.state == 'met'
                          and fact.temporal_state in ('met', 'not_applicable') else 'unmet'),
                         ('reason_codes', _Array(fact.reason_codes))]
            if field == _EXTERNAL[1]:
                subject = _field(_field(fact.record.node.fields, 'data', port), 'subject_ref', port)
                mapped, external = [], []
                for item in facts.subjects:
                    if _compare_text(subject, item.identifier, port) == 0:
                        external.append(item.identifier)
                for mapping in facts.mappings:
                    if _compare_text(subject, mapping.stage_subject.identifier, port) == 0:
                        port.charge(2)
                        mapped.append(mapping.assertion.identifier)
                        external.append(mapping.subject.identifier)
                port.charge(len(external) + len(mapped) + 3)
                additions.extend((('externality_subject_refs', _Array(_tuple(external, port))),
                                  ('mapping_assertion_refs', _Array(_tuple(mapped, port)))))
            port.charge(1)
            rows.append(_record(facts.prepared, fact.record, additions, port))
    else:
        cohorts = list(facts.baselines)
        if facts.target.coverage is not None:
            cohorts.insert(0, facts.target)
        port.charge(len(cohorts) + 2)
        for cohort in cohorts:
            anchor = () if cohort.anchor is None else cohort.anchor
            rows.append(_record(facts.prepared, cohort.coverage,
                (('stage_anchor', _Array(anchor)), ('cohort_qualification_state', 'met' if cohort.eligible else 'unmet'),
                 ('transition_qualification_state', 'met' if facts.baseline is not None else 'unmet'),
                 ('reason_codes', _Array(cohort.reason_codes))), port))
    port.charge(len(rows) + 3)
    return _r._RecordDisclosures(_tuple(rows, port))


def _partition(cohort, population, port):
    categories = []
    for label in ('Y', 'F', 'U'):
        members = []
        for row in cohort.rows:
            port.charge(1)
            if row.classification == label:
                members.append(_profile_ref(row.member, port))
        for ref in members:
            _charge_input_ref(ref, port, repeats=len(members) + 3)
        port.charge(len(members) * len(members) + 8)
        categories.append(_r._PartitionCategory(label, _tuple(members, port), len(members)))
    for member in population.member_refs:
        _charge_input_ref(member, port, repeats=4)
    port.charge(len(population.member_refs) * 3 + 12)
    return _r._Partition(population, _tuple(categories, port))


def _reason_entities(facts, code, transition, port):
    """Link the actual limiting observations, retaining full support in basis.

    A stage's absent basis is a statement about that stage record; it is not
    a statement about every unrelated source in the dossier or baseline.
    """
    selected = []
    if facts.family == 'SIT-M009':
        if facts.assessment is not None:
            port.charge(1)
            selected.append(facts.assessment)
        if code == 'premise_disputed':
            port.charge(len(facts.conflicts))
            selected.extend(facts.conflicts)
        if facts.assessment_conflict is not None and code in facts.assessment_conflict.reason_codes:
            for entity in _support_entities(facts.prepared, (facts.assessment_conflict,), port):
                port.charge(1)
                selected.append(entity)
    else:
        cohorts = (facts.target,) + (facts.baselines if transition else ())
        port.charge(len(cohorts) + 1)
        for cohort in cohorts:
            port.charge(1)
            if cohort.coverage is not None and (code in cohort.reason_codes or
                    code in ('transition_baseline_unestablished', 'zero_denominator',
                             'completion_interval_not_needed', 'no_applicable_subject')):
                selected.append(cohort.coverage)
            for row in cohort.rows:
                port.charge(1)
                if code in row.reason_codes:
                    port.charge(len(row.records) + 1)
                    selected.append(row.member)
                    selected.extend(row.records)
            if code in ('scope_unestablished', 'unknown_endpoint'):
                for member in cohort.members:
                    port.charge(1)
                    if not _member_scope(member, facts.context, port):
                        selected.append(member)
            port.charge(len(cohort.conflicts) + 1)
            for qualification in cohort.conflicts + (cohort.identity,):
                if qualification is not None and code in qualification.reason_codes:
                    for entity in _support_entities(facts.prepared, (qualification,), port):
                        port.charge(1)
                        selected.append(entity)
    port.charge(len(facts.stage_facts) + 1)
    stage_facts = list(facts.stage_facts)
    if facts.family == 'SIT-M010' and transition:
        for cohort in facts.baselines:
            port.charge(len(cohort.stages) + 1)
            stage_facts.extend(cohort.stages)
    for fact in stage_facts:
        port.charge(1)
        if code in fact.reason_codes:
            port.charge(1)
            selected.append(fact.record)
            for qualification in (fact.conflict, fact.identity):
                if code in qualification.reason_codes:
                    for entity in _support_entities(facts.prepared, (qualification,), port):
                        port.charge(1)
                        selected.append(entity)
    if not selected:
        port.charge(1)
        selected.append(facts.inquiry)
    return _unique_entities(facts.prepared, selected, port)


def _reason_refs(facts, scope, ref, codes, transition, port):
    rows = []
    for code in _analysis_codes(codes, port):
        inputs = _refs(_reason_entities(facts, code, transition, port), port)
        for item in inputs:
            _charge_input_ref(item, port, repeats=len(inputs) + 3)
        for unused in range(3):
            _charge_scope(scope, port)
        port.charge(18)
        rows.append(_r._Reason(code, scope, (ref,), inputs,
            'This exact boundary/stage/cohort question retains the supplied limitation; no missing evidence '
            'is converted into a negative observation or a smaller denominator.',
            'structural_inapplicability' if code in ('no_applicable_subject', 'completion_interval_not_needed') else
            'conflict' if code == 'premise_disputed' else 'evidence_gap'))
    return _tuple(rows, port)


def _checks(facts, ref, field, sources, port):
    values = [('PC01', 'met', (facts.inquiry,)), ('PC02', 'met', ())]
    if facts.family == 'SIT-M009':
        assessment = (facts.assessment,) if facts.assessment is not None else ()
        basis_states = [facts.assessment_basis.state] if facts.assessment_basis is not None else ['unknown']
        conflict_states = [facts.assessment_conflict.state] if facts.assessment_conflict is not None else ['unknown']
        time_states = ['met' if facts.context.temporal_basis == 'snapshot_structural' else facts.assessment_native_time]
        if facts.assessment_temporal is not None:
            time_states.append(facts.assessment_temporal.state)
        if facts.conflicts:
            conflict_states.append('unmet')
        basis_sources, conflict_sources, time_sources = list(assessment), list(assessment + facts.conflicts), list(assessment)
        port.charge(len(assessment) * 3 + len(facts.conflicts) + 12)
        for entity in _support_entities(facts.prepared, (facts.assessment_conflict,), port):
            port.charge(1)
            conflict_sources.append(entity)
        if field == _EXTERNAL[1]:
            for fact in facts.stage_facts:
                port.charge(6)
                basis_states.append(fact.basis.state)
                conflict_states.append(fact.conflict.state)
                time_states.append('met' if fact.temporal_state == 'not_applicable' else fact.temporal_state)
                basis_sources.append(fact.record)
                conflict_sources.append(fact.record)
                time_sources.append(fact.record)
                for entity in _support_entities(facts.prepared, (fact.conflict,), port):
                    port.charge(1)
                    conflict_sources.append(entity)
        values.extend((('PC05', _shared._aggregate(basis_states, port), basis_sources),
            ('PC09', _shared._aggregate(conflict_states, port), conflict_sources),
            ('PC10', _shared._aggregate(time_states, port), time_sources),
            ('PC15', facts.qualified_state, assessment)))
    else:
        target = facts.target
        port.charge(len(target.rows) + len(target.stages) + len(facts.baselines) + 8)
        coverage = (target.coverage,) if target.coverage is not None else (facts.inquiry,)
        stage_sources = tuple(fact.record for fact in target.stages)
        baseline_sources = tuple(cohort.coverage for cohort in facts.baselines)
        target_conflicts = _support_entities(facts.prepared, target.conflicts + (target.identity,), port)
        port.charge(len(coverage) + len(target.members) + len(target_conflicts) + 1)
        values.extend((('PC16', 'met' if target.eligible else 'unknown', coverage + target.members + target_conflicts),
            ('PC17', 'met' if target.eligible and all(row.classification != 'U' for row in target.rows) else 'unknown', stage_sources or target.members),
            ('PC18', 'not_applicable' if field not in _PIPELINE[4:] or target.anchor is not None and target.anchor[2] not in ('preservation', 'selection')
             else 'met' if facts.baseline is not None else 'unknown', coverage + baseline_sources)))
    checks = []
    for key, state, entities in values:
        if key == 'PC02':
            checks.append(_scope_check(_ScopeCheckFact(ref, ref.scope), port))
            continue
        inputs = _refs(_unique_entities(facts.prepared, entities, port), port)
        for source in inputs:
            _charge_input_ref(source, port, repeats=len(inputs) + 3)
        _charge_link(ref, port)
        port.charge(len(inputs) + 14)
        checks.append(_r._PrerequisiteCheck(key, ref, state, inputs, (),
            'Executed field-specific source, boundary, finite membership or baseline check. '
            'Individual native disclosures survive unmet stronger prerequisites.'))
    return checks


def _presence_results(facts, port):
    _check_facts(facts, port)
    fields = _EXTERNAL if facts.family == 'SIT-M009' else _PIPELINE
    scopes, populations, bases, partitions = [], [], [], []
    for transition in (False, True) if facts.family == 'SIT-M010' else (False,):
        scope = _scope(facts, transition, port)
        entities = facts.transition_basis if transition else facts.basis_entities
        basis = []
        for entity in entities:
            source = _profile_ref(entity, port)
            _charge_input_ref(source, port)
            port.charge(3)
            basis.append(_r._BasisRef(source))
        basis = _tuple(basis, port)
        members = _refs(facts.subjects, port)
        for member in members:
            _charge_input_ref(member, port, repeats=len(members) + 3)
        for link in basis:
            _charge_link(link, port)
        known = facts.family == 'SIT-M009' or facts.target.eligible
        port.charge(len(members) * len(members) + len(basis) + 18)
        population = _r._Population(scope, 'record' if facts.family == 'SIT-M009' else 'pipeline_member', members,
            'Exact native assessment subjects or the unchanged full member_refs of the selected finite coverage.',
            scope.coverage_refs, basis, 'enumerated_for_scope' if known else 'unestablished',
            ('Unestablished native membership is retained as a declaration; it supplies no numerical denominator.',))
        partition = _partition(facts.target, population, port) if facts.family == 'SIT-M010' and known else None
        port.charge(4)
        scopes.append(scope); populations.append(population); bases.append(basis); partitions.append(partition)
    outputs = []
    for field in fields:
        _check_facts(facts, port)
        transition = facts.family == 'SIT-M010' and field in _PIPELINE[4:]
        index = 1 if transition else 0
        scope, population, basis, partition = scopes[index], populations[index], bases[index], partitions[index]
        source_entities = facts.transition_basis if transition else facts.basis_entities
        port.charge(len(facts.reason_codes) + 180)
        ref = _r._ResultRef(facts.family, field, scope)
        codes = list(facts.reason_codes)
        state, value, origin = 'available', None, 'qualification_check'
        if field in (_EXTERNAL[0], _EXTERNAL[1], _PIPELINE[0], _PIPELINE[4]):
            origin = 'attributed_record'
            if field == _EXTERNAL[0] and facts.assessment is None:
                state = 'unavailable'
            else:
                value = _disclosures(facts, field, port)
            if field == _PIPELINE[4] and facts.baseline is None:
                codes.append('transition_baseline_unestablished')
        else:
            target = facts.target
            if not target.eligible:
                state = 'unavailable'
            elif field == _PIPELINE[1]:
                value = partition
            else:
                total = len(target.members)
                port.charge(len(target.rows) * 2 + 4)
                yes = sum(row.classification == 'Y' for row in target.rows)
                unknown = sum(row.classification == 'U' for row in target.rows)
                interval = field in (_PIPELINE[3], _PIPELINE[6])
                if transition and (target.anchor is None or target.anchor[2] not in ('preservation', 'selection')):
                    state = 'not_applicable'
                    codes.append('no_applicable_subject')
                elif transition and facts.baseline is None:
                    state = 'unavailable'
                    codes.append('transition_baseline_unestablished')
                elif total == 0:
                    state = 'unavailable'
                    codes.append('zero_denominator')
                elif interval and unknown == 0:
                    state = 'not_applicable'
                    codes.append('completion_interval_not_needed')
                elif not interval and unknown:
                    state = 'unavailable'
                    codes.append('stage_classification_unresolved')
                else:
                    _charge_link(population, port)
                    port.charge(20)
                    lower = _r._Fraction(yes, total, population)
                    if interval:
                        for member in population.member_refs:
                            _charge_input_ref(member, port, repeats=4)
                        port.charge(len(population.member_refs) * 4 + 18)
                        value = _r._CompletionInterval(lower, _r._Fraction(yes + unknown, total, population),
                            'finite_cohort_completion', partition)
                    else:
                        value = lower
            for row in target.rows:
                if row.classification == 'U':
                    port.charge(len(row.reason_codes))
                    codes.extend(row.reason_codes)
        reasons = _reason_refs(facts, scope, ref, codes, transition, port)
        checks = _checks(facts, ref, field, source_entities, port)
        _charge_scope(scope, port)
        port.charge(8)
        witnesses = (_r._WitnessRef(scope, 'member_set', ('presence_selection',)),)
        components = []
        port.charge(len(reasons) + 1)
        conflict_sources = _refs(_reason_entities(facts, 'premise_disputed', transition, port), port) if any(
            reason.code == 'premise_disputed' for reason in reasons) else ()
        for name, links in (('premises', population.member_refs), ('conflicts', conflict_sources), ('value', (ref,)),
                            ('basis', basis), ('reasons', reasons), ('witnesses', witnesses)):
            for link in links:
                for unused in range(3):
                    _charge_link(link, port)
            port.charge(len(links) * len(links) + 10)
            components.append(_ComponentCompletion(name, links, links))
        for unused in range(3):
            _charge_link(population, port)
        port.charge(24)
        known = population.membership_state == 'enumerated_for_scope'
        complete = _CompletionRecord(ref, (population,) if known else (),
            (_PopulationCompletion(population, population.member_refs),) if known else (), _tuple(components, port))
        checks.append(_completion_check(complete, port))
        for unused in range(2):
            _charge_link(ref, port)
            _charge_link(population, port)
            for links in (checks, basis, reasons, witnesses):
                for link in links:
                    _charge_link(link, port)
        port.charge(len(checks) + len(basis) + len(reasons) + 32)
        kind = 'record_disclosures' if field in (_EXTERNAL + (_PIPELINE[0], _PIPELINE[4])) else (
            'partition' if field == _PIPELINE[1] else 'completion_interval' if field in (_PIPELINE[3], _PIPELINE[6]) else 'fraction')
        outputs.append(_r._Result(ref, (population,), 'completed', state, origin, kind, value,
            _tuple(checks, port), basis, witnesses, reasons, _LIMIT))
    port.check()
    return _tuple(outputs, port)


def _presence(prepared, context, ledger, port, *, family, assessment_ref=None,
              coverage_ref=None, stage_anchor=None):
    facts = _presence_facts(prepared, context, ledger, port, family=family,
        assessment_ref=assessment_ref, coverage_ref=coverage_ref, stage_anchor=stage_anchor)
    results = _presence_results(facts, port)
    port.charge(4)
    profile = _PresenceProfile(facts, results, facts.witnesses)
    port.check()
    return profile
