# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: FINDING_CONTRACT. Paid, finite observations of supplied evidence.

Reporting section 18: original owners establish graph and qualification facts
in this job. No content classifier, threat score, intervention or public report.
"""
from dataclasses import dataclass

from ..contracts.bundle import _require, _lookup_pair
from ..contracts.evidence import _QualificationContext, _SourceAddress
from ..contracts import results as _r
from ..contracts.report import _charge_scope, _charge_link, _charge_frozen
from ..validation.structure import _field
from ..validation.semantics import (
    _analysis_start, _analysis_lookup, _analysis_text, _analysis_contains,
    _analysis_subset, _analysis_scope, _profile_ref,
)
from ..graph.projections import _project, _check_edge_eligibility
from ..graph.traversal import _reachable, _shortest_path
from ..graph.cycles import _components
from ..graph.witnesses import _path_witness, _cycle_witness, _absence_witness
from . import origins as _o
from . import process_comparison as _p
from . import evaluator_lineage as _e
from . import presence as _s
from . import correction_routes as _cr
from . import correction_outcomes as _co
from . import human_review as _h
from . import contribution_profile as _cp
from . import inventory as _i
from . import context as _c

_OBSERVATION_KINDS = ('positive_witness', 'no_witness_in_examined_view',
    'bounded_absence_under_declared_coverage', 'attributed_observation',
    'qualification_gap', 'recorded_conflict')
_CONDITIONS = (
    'shared_origin_witness', 'citation_path_witness', 'transformation_path_witness',
    'model_mediated_derivation_witness', 'view_cycle_witness', 'assurance_loop_limitation',
    'evaluator_overlap_witness', 'family_label_match', 'provenance_gap',
    'verification_scope_limitation', 'independence_record_conflict',
    'correction_dependency_witness', 'correction_route_limitation',
    'case_handling_disclosure', 'linked_change_disclosure', 'downstream_change_undocumented',
    'externality_stage_limitation', 'recorded_stage_exclusion',
    'anomaly_or_contestation_disclosure', 'attributed_external_observation',
    'scoped_no_witness', 'recorded_data_conflict')
_LIMIT = ('Conditional on the exact supplied scope, versions, premises and evidence basis. '
    'This finite observation cannot establish motive, censorship, authenticity, substantive truth, '
    'independence outside the examined dimension, causal success or a universal threat verdict. '
    'Threat associations are nonexclusive explanatory links, with no incident total or severity. '
    'No source contact, quarantine, removal, down-weighting, sanction or other intervention follows.')
_RELEASE_LIMITS = ('Content-level poisoning, injection and authorship detection was not performed '
    'by this product. A supplied report or allegation remains attributed evidence; no passed '
    'content-detector check, clean-source certificate or automatic threat classification is produced.',)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _FindingWitness:
    prepared: object
    context: object
    job_port: object
    input_refs: tuple
    owner_witnesses: tuple
    member_count: int


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Finding:
    observation_kind: str
    condition_code: str
    diagnostic_refs: tuple
    threat_family_refs: tuple
    scope_ref: object
    population_refs: tuple
    basis_refs: tuple
    witness: _FindingWitness
    contrary_input_refs: tuple
    reason_refs: tuple
    result_refs: tuple
    statement: str
    interpretation_limit: str
    native_records: tuple


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _FindingProfile:
    prepared: object
    context: object
    job_port: object
    findings: tuple
    release_limits: tuple


def _compatible(prepared, parent, local, port):
    _require(type(local) is _QualificationContext)
    _analysis_start(prepared, local, port)
    for text in (parent.inquiry_ref, local.inquiry_ref):
        _analysis_text(text, port)
    port.charge(4)
    _require(parent.inquiry_ref == local.inquiry_ref and
             parent.temporal_basis == local.temporal_basis and
             parent.requested_time is local.requested_time)
    inquiry = _analysis_lookup(prepared, parent.inquiry_ref, port)
    selected = parent.claim_refs or _field(inquiry.node.fields, 'target_claim_refs', port).items
    _require(_analysis_subset(local.claim_refs, selected, port))
    if parent.subject_refs:
        _require(bool(local.subject_refs) and
                 _analysis_subset(local.subject_refs, parent.subject_refs, port))
    if parent.dependency_dimension is not None:
        _require(local.dependency_dimension == parent.dependency_dimension)
    if parent.graph_view is not None:
        _require(local.graph_view == parent.graph_view)


def _refs(entities, port):
    rows = []
    for entity in entities:
        port.charge(1)
        rows.append(_profile_ref(entity, port))
    return _o._tuple(rows, port)


def _unique_links(links, port):
    rows, seen = [], set()
    for link in links:
        _charge_link(link, port)
        port.charge(4)
        key = link._key()
        if key not in seen:
            seen.add(key)
            rows.append(link)
    return _o._tuple(rows, port)


def _scope(prepared, context, entities, port):
    inquiry = _analysis_lookup(prepared, context.inquiry_ref, port)
    claims = []
    for identifier in context.claim_refs:
        port.charge(1)
        claims.append(_profile_ref(_analysis_lookup(prepared, identifier, port), port))
    targets = _refs(_o._unique_entities(prepared, entities, port), port)
    anchor = []
    for part in context.operation_anchor:
        port.charge(1)
        anchor.append(_o._source_ref(part, port) if type(part) is _SourceAddress else part)
    port.charge(len(claims) ** 2 + len(targets) ** 2 + 16)
    result = _r._Scope(_profile_ref(inquiry, port), _o._tuple(claims, port), targets,
        context.dependency_dimension, context.graph_view, context.temporal_basis,
        context.requested_time, (), ('Finite supplied input selection; omitted dimensions and '
        'unexamined histories remain outside this observation.',), _o._tuple(anchor, port))
    _charge_scope(result, port)
    return result


def _emit(rows, prepared, context, ledger, port, code, form, statement, *,
          result=None, entities=(), inputs=(), contrary=(), reasons=(), witnesses=(),
          scope=None, threats=(), limit='', native=()):
    _require(code in _CONDITIONS and form in _OBSERVATION_KINDS)
    port.charge(12)
    if result is not None:
        _require(type(result) is _r._Result and result.execution_state == 'completed')
        scope = result.ref.scope
    elif scope is None:
        scope = _scope(prepared, context, entities, port)
    _charge_scope(scope, port)
    if result is None and native:
        more_inputs, more_reasons, more_contrary = _premises(prepared, context, native, scope, port)
        port.charge(len(inputs) + len(reasons) + len(contrary) +
                    len(more_inputs) + len(more_reasons) + len(more_contrary) + 3)
        inputs += more_inputs
        reasons += more_reasons
        contrary += more_contrary
    source_refs = _unique_links(_refs(entities, port) + inputs, port)
    contrary = _unique_links(contrary, port)
    reasons = _unique_links(reasons, port)
    basis, populations, refs, diagnostics = [], (), (), ()
    if result is not None:
        port.charge(4)
        populations, refs, diagnostics = result.population_refs, (result.ref,), (result.ref.diagnostic_id,)
    for source in source_refs:
        port.charge(2)
        basis.append(_r._BasisRef(source))
    basis = _unique_links(_o._tuple(basis, port), port)
    # Original witness payloads retain their paid quota; these are new links.
    count = len(source_refs) + len(witnesses)
    token = ledger.reserve(witnesses=1, members=count)
    port.charge(count + 8)
    witness = _FindingWitness(prepared, context, port, source_refs, witnesses, count)
    for collection in (populations, refs, basis, reasons, contrary):
        for link in collection:
            _charge_link(link, port)
    disclosures = []
    for entity in native:
        _charge_frozen(entity.node.fields, port)
        port.charge(4)
        disclosures.append(_r._Disclosure(_profile_ref(entity, port), entity.node.fields,
            ('Source-native content and provenance retained without toolkit endorsement.',)))
    interpretation = _LIMIT + (' ' + limit if limit else '')
    for text in (statement, interpretation):
        _analysis_text(text, port)
    for text in threats:
        _analysis_text(text, port)
    port.charge(17)
    row = _Finding(form, code, diagnostics, threats, scope, populations, basis,
        witness, contrary, reasons, refs, statement, interpretation, _o._tuple(disclosures, port))
    port.check()
    ledger.retain(token)
    port.charge(1)
    rows.append(row)


def _result(profile, field, port):
    for result in profile.results:
        port.charge(2)
        _analysis_text(result.ref.field_key, port)
        if result.ref.field_key == field:
            return result
    raise TypeError('finding_owner_result_missing')


def _localized(reasons, entities, port):
    refs = _refs(entities, port)
    selected = []
    for reason in reasons:
        matches = []
        for source in reason.input_refs:
            for ref in refs:
                _charge_link(source, port)
                _charge_link(ref, port)
                if source.collection == ref.collection and source.identifier == ref.identifier:
                    port.charge(1)
                    matches.append(source)
                    break
        if matches:
            port.charge(len(matches) * len(matches) + 10)
            selected.append(_r._Reason(reason.code, reason.scope, reason.affected_result_refs,
                _o._tuple(matches, port), reason.detail, reason.classification))
    return _unique_links(_o._tuple(selected, port), port)


def _premises(prepared, context, entities, scope, port):
    """Retain actual support/conflict qualification beside structural evidence."""
    inputs, reasons, contrary, cache = [], [], [], []
    # Graph selection already binds the exact path endpoints. A proposition's
    # support question must not require every path endpoint in each edge.
    local = _p._context(context, port, subjects=(), predicates=context.relation_types,
        coverage_kind=context.coverage_kind, view=context.graph_view)
    for entity in _o._unique_entities(prepared, entities, port):
        source = _profile_ref(entity, port)
        if entity.collection == 'evidence_references':
            port.charge(1)
            inputs.append(source)
            if _field(entity.node.fields, 'availability', port) != 'supplied':
                port.charge(10)
                reasons.append(_r._Reason('support_uninspectable', scope, (), (source,),
                    'The linked evidence reference is not supplied for inspection.', 'evidence_gap'))
            continue
        premise = _p._premise(prepared, entity, local, cache, port)
        for qualification in (premise.basis, premise.conflict):
            for address in qualification.support_refs:
                ref = _o._source_ref(address, port)
                port.charge(1)
                inputs.append(ref)
                if qualification is premise.conflict and qualification.state != 'met':
                    port.charge(1)
                    contrary.append(ref)
        for code in _p._codes(premise, port):
            port.charge(10)
            classification = 'conflict' if code in ('premise_disputed', 'temporal_inconsistency') else 'evidence_gap'
            reasons.append(_r._Reason(code, scope, (), (source,),
                'Original premise qualification retains this local limitation: ' + code + '.',
                classification))
    return (_unique_links(_o._tuple(inputs, port), port),
            _unique_links(_o._tuple(reasons, port), port),
            _unique_links(_o._tuple(contrary, port), port))


def _reason_findings(rows, prepared, ledger, port, profile):
    facts = profile.facts
    for result in profile.results:
        for reason in result.reason_refs:
            port.charge(2)
            code = None
            if reason.code == 'self_supporting_assurance':
                code = 'assurance_loop_limitation'
            elif reason.code in ('unknown_endpoint', 'upstream_coverage_incomplete',
                    'unqualified_origin_boundary', 'before_after_unresolved'):
                code = 'provenance_gap'
            elif reason.classification == 'conflict':
                code = 'recorded_data_conflict'
            if code is None:
                continue
            _emit(rows, prepared, facts.context, ledger, port, code,
                'recorded_conflict' if reason.classification == 'conflict' else 'qualification_gap',
                reason.detail, result=result, inputs=reason.input_refs,
                contrary=reason.input_refs if reason.classification == 'conflict' else (),
                reasons=(reason,), witnesses=profile.witnesses,
                threats=('SIT-TH005',) if code == 'assurance_loop_limitation' else
                    ('SIT-TH008',) if code == 'provenance_gap' else (),
                limit=result.interpretation_limit)


def _origin_findings(rows, prepared, ledger, port, profile):
    facts = profile.facts
    for origin in facts.reached_origins:
        seeds, witnesses, relied = [], [], []
        for trace in facts.seed_traces:
            for reached in trace.reached_origins:
                port.charge(2)
                if reached is origin:
                    port.charge(len(trace.witnesses) + 2)
                    seeds.append(trace.seed)
                    witnesses.extend(trace.witnesses)
                    port.charge(len(trace.reachability.edges))
                    relied.extend(trace.reachability.edges)
                    break
        if len(seeds) < 2:
            continue
        scope = profile.results[0].ref.scope
        entities, inputs, reasons, contrary = _origin_support(facts, scope, port, _o._tuple(relied, port))
        _emit(rows, prepared, facts.context, ledger, port, 'shared_origin_witness',
            'positive_witness', 'Distinct supplied contributions reach this same recorded origin '
            'in the selected Claim and dependency dimension.', result=profile.results[0],
            entities=_o._tuple(seeds, port) + (origin,) + entities, inputs=inputs,
            reasons=reasons, contrary=contrary, witnesses=_o._tuple(witnesses, port),
            threats=('SIT-TH001',), limit='Shared recorded ancestry does not establish misconduct '
            'or exhaustive origin coverage. Unresolved alternate branches remain disclosed.')
    # The original origin owner has already executed these exact edge support
    # questions. Retain its facts without repeating qualification scans.
    for edge in facts.edge_facts:
        if 'self_supporting_assurance' not in edge.reason_codes:
            continue
        scope = profile.results[0].ref.scope
        entities, inputs, reasons, contrary = _origin_support(facts, scope, port, (edge.edge,))
        _emit(rows, prepared, facts.context, ledger, port, 'assurance_loop_limitation',
            'qualification_gap', 'A supplied premise relies on circular or self-supporting '
            'assurance and cannot independently certify itself.', entities=entities,
            inputs=inputs, reasons=reasons, contrary=contrary, scope=scope,
            witnesses=profile.witnesses, threats=('SIT-TH005',))


def _origin_support(facts, scope, port, edges):
    entities, inputs, reasons, contrary = [], [], [], []
    for fact in facts.edge_facts:
        selected = False
        for edge in edges:
            port.charge(1)
            if fact.edge is edge:
                selected = True
                break
        if not selected:
            continue
        entity = _analysis_lookup(facts.prepared, fact.edge.source_ref.record_id, port)
        source = _profile_ref(entity, port)
        port.charge(1)
        entities.append(entity)
        for qualification in (fact.basis, fact.conflict):
            if qualification is None:
                continue
            for address in qualification.support_refs:
                ref = _o._source_ref(address, port)
                port.charge(1)
                inputs.append(ref)
                if qualification is fact.conflict and qualification.state != 'met':
                    port.charge(1)
                    contrary.append(ref)
        for code in fact.reason_codes:
            port.charge(10)
            reasons.append(_r._Reason(code, scope, (), (source,),
                'Original origin-edge qualification retains this limitation: ' + code + '.',
                'conflict' if code in ('premise_disputed', 'temporal_inconsistency') else 'evidence_gap'))
    return (_o._unique_entities(facts.prepared, entities, port),
        _unique_links(_o._tuple(inputs, port), port), _unique_links(_o._tuple(reasons, port), port),
        _unique_links(_o._tuple(contrary, port), port))


def _comparison_findings(rows, prepared, ledger, port, profile):
    facts = profile.facts
    if facts.assessment is not None and facts.contrary:
        result = _result(profile, 'independence_assessment_disclosures', port)
        _emit(rows, prepared, facts.context, ledger, port, 'independence_record_conflict',
            'recorded_conflict', 'The supplied independence assessment has relevant contrary '
            'process or ancestry records in its actual dimension.', result=result,
            entities=(facts.assessment,) + facts.contrary, contrary=_refs(facts.contrary, port),
            witnesses=profile.witnesses, reasons=result.reason_refs,
            native=(facts.assessment,) + facts.contrary)


def _evaluator_findings(rows, prepared, ledger, port, profile):
    facts = profile.facts
    if facts.shared_objects or facts.common_ancestors or facts.one_sided:
        result = _result(profile, 'evaluator_overlap_disclosures', port)
        _emit(rows, prepared, facts.context, ledger, port, 'evaluator_overlap_witness',
            'positive_witness', 'Actual represented evaluator roles share a recorded object, '
            'strict common ancestor or one-sided ancestry; those cases retain separate disclosures.',
            result=result, entities=(facts.evaluation,) + facts.shared_objects + facts.common_ancestors,
            witnesses=profile.witnesses,
            threats=('SIT-TH006',), limit=result.interpretation_limit)
    if facts.matching_family_labels:
        result = _result(profile, 'matching_family_label_count', port)
        _emit(rows, prepared, facts.context, ledger, port, 'family_label_match',
            'attributed_observation', 'Exact supplied model-family label strings match. '
            'This is a label match, with no lineage or process-independence inference.',
            result=result, entities=(facts.evaluation,) + facts.left_objects + facts.right_objects,
            witnesses=profile.witnesses, threats=('SIT-TH006',),
            native=facts.left_objects + facts.right_objects,
            limit='Only exact supplied label equality is established; labels do not establish ancestry.')


def _route_findings(rows, prepared, ledger, port, profile):
    facts = profile.facts
    result = _result(profile, 'applicable_authorized_route_witnesses', port)
    if result.result_state != 'available' or (facts.declared_path is None and not facts.bounded_absence):
        _emit(rows, prepared, facts.context, ledger, port, 'correction_route_limitation',
            'qualification_gap', 'The requested correction route, grant, action or temporal '
            'applicability is unestablished or inapplicable at this exact scope.', result=result,
            entities=(facts.channel, facts.target) + _o._tuple(
                [qualified.coverage for qualified in facts.coverage], port), witnesses=profile.witnesses,
            reasons=result.reason_refs, threats=('SIT-TH010', 'SIT-TH011'),
            limit=result.interpretation_limit)
    if facts.declared_path is None:
        result = _result(profile, 'declared_correction_route_witnesses', port)
        form = ('bounded_absence_under_declared_coverage' if facts.bounded_absence else
                'no_witness_in_examined_view')
        _emit(rows, prepared, facts.context, ledger, port, 'scoped_no_witness', form,
            'Completed declared-route search found no eligible route between these exact '
            'endpoints in the examined supplied view.', result=result,
            entities=(facts.channel, facts.target) + _o._tuple(
                [qualified.coverage for qualified in facts.coverage], port), witnesses=profile.witnesses,
            reasons=result.reason_refs, limit='The coverage description is conditional on the '
            'original route owner\'s qualified coverage. No threat check passed.')
    _channel_overlap(rows, prepared, ledger, port, profile)


def _outcome_findings(rows, prepared, ledger, port, profile):
    facts = profile.facts
    result = _result(profile, 'correction_case_disclosures', port)
    for case in facts.cases:
        selected = [case]
        for event in facts.handling:
            data = _field(event.node.fields, 'data', port)
            port.charge(2)
            if _field(data, 'case_ref', port) == case.identifier:
                selected.append(event)
        selected = _o._tuple(selected, port)
        _emit(rows, prepared, facts.context, ledger, port, 'case_handling_disclosure',
            'attributed_observation', 'This case retains its submission and all supplied '
            'handling outcomes, including nonexclusive accepted and failed outcomes.',
            result=result, entities=selected, native=selected, witnesses=profile.witnesses,
            threats=('SIT-TH011',), limit='A source-native failed outcome is not a toolkit runtime failure.')
    result = _result(profile, 'correction_target_change_disclosures', port)
    for change in facts.change_facts:
        entities = (change.source, change.case, change.before)
        if change.after is not None:
            port.charge(1)
            entities += (change.after,)
        _emit(rows, prepared, facts.context, ledger, port, 'linked_change_disclosure',
            'attributed_observation', 'A supplied change event links its exact case and '
            'before-state to an after-state or stated removal; documentary qualification '
            'retains the original owner\'s separate result.', result=result, entities=entities,
            native=(change.source,), witnesses=profile.witnesses,
            limit='This event does not imply resolved endpoints or documentary qualification; '
            'causal success, downstream propagation and authority remain separate.')
    for target in facts.target_changes:
        if not target.selected or target.documentary_state == 'met':
            continue
        _emit(rows, prepared, facts.context, ledger, port, 'downstream_change_undocumented',
            'qualification_gap', 'The examined supplied set lacks sufficient documentary '
            'linked-change evidence for this selected case/target pair.', result=result,
            entities=(target.case, target.before), witnesses=profile.witnesses,
            reasons=_localized(result.reason_refs, (target.case, target.before), port),
            threats=('SIT-TH011',),
            limit='Undocumented effect does not establish failed correction or censorship.')


def _presence_findings(rows, prepared, ledger, port, profile):
    facts = profile.facts
    field = ('externality_stage_links' if facts.family == 'SIT-M009' else 'cohort_transition_disclosures')
    result = _result(profile, field, port)
    stage_limits = []
    for stage_result in profile.results:
        for reason in stage_result.reason_refs:
            if reason.code in ('externality_unestablished', 'stage_classification_unresolved',
                    'cohort_universe_unestablished', 'cohort_anchor_missing', 'cohort_anchor_ambiguous',
                    'transition_baseline_unestablished', 'premise_disputed', 'documentary_basis_incomplete'):
                port.charge(1)
                stage_limits.append((stage_result, reason))
    if not stage_limits and (facts.reason_codes or facts.qualified_state != 'met'):
        entities = facts.subjects if facts.assessment is None else (facts.assessment,)
        _emit(rows, prepared, facts.context, ledger, port, 'externality_stage_limitation',
            'qualification_gap', 'Externality, intake and use stages retain separate qualification, '
            'missing records and contradictions; no implicit baseline or adequate renewal is inferred.',
            result=result, entities=entities, reasons=result.reason_refs,
            witnesses=profile.witnesses, threats=('SIT-TH012',), limit=result.interpretation_limit)
    for result, reason in stage_limits:
        _emit(rows, prepared, facts.context, ledger, port, 'externality_stage_limitation',
            'qualification_gap', 'This exact externality, stage or transition result retains '
            'an unresolved qualification; other stage results keep their own state.',
            result=result, inputs=reason.input_refs, reasons=(reason,),
            witnesses=profile.witnesses, threats=('SIT-TH012',), limit=result.interpretation_limit)
    if facts.family == 'SIT-M009':
        result = _result(profile, 'externality_stage_links', port)
        for stage in facts.stage_facts:
            state = _field(_field(stage.record.node.fields, 'data', port), 'state', port)
            if state != 'unknown' and not stage.reason_codes:
                continue
            codes = stage.reason_codes or ('stage_classification_unresolved',)
            reasons = []
            source = _profile_ref(stage.record, port)
            for code in codes:
                port.charge(12)
                reasons.append(_r._Reason(code, result.ref.scope, (result.ref,), (source,),
                    'This linked stage record retains its native unknown state or actual qualification limit.',
                    'conflict' if code == 'premise_disputed' else 'evidence_gap'))
            _emit(rows, prepared, facts.context, ledger, port, 'externality_stage_limitation',
                'qualification_gap', 'A separately linked stage record remains unknown or '
                'insufficiently qualified even when the externality assessment is qualified.',
                result=result, entities=(stage.record,), reasons=_o._tuple(reasons, port),
                witnesses=profile.witnesses, native=(stage.record,), threats=('SIT-TH012',))
    if facts.family == 'SIT-M010' and facts.target.eligible:
        result = _result(profile, 'stage_member_partition', port)
        for member in facts.target.rows:
            if member.classification != 'F':
                continue
            records = []
            for stage in member.records:
                port.charge(1)
                records.append(stage)
            entities = (member.member,) + _o._tuple(records, port)
            _emit(rows, prepared, facts.context, ledger, port, 'recorded_stage_exclusion',
                'attributed_observation', 'This explicit cohort member has an evidence-bearing '
                'non-occurrence at the exact supplied run/stage key.', result=result,
                entities=entities, native=_o._tuple(records, port), witnesses=profile.witnesses,
                threats=('SIT-TH014',), limit='A stage-specific non-occurrence does not establish '
                'motive, censorship, earlier-stage failure or a universal absence.')


def _context_findings(rows, prepared, ledger, port, profile):
    for field in ('anomaly_context_disclosures', 'contestation_disclosures'):
        result = _result(profile, field, port)
        if result.result_state != 'available':
            continue
        for disclosure in result.value.records:
            if type(disclosure.source) is not _r._InputRef:
                continue
            entity = _analysis_lookup(prepared, disclosure.source.identifier, port)
            _emit(rows, prepared, profile.facts.context, ledger, port,
                'anomaly_or_contestation_disclosure', 'attributed_observation',
                'Supplied anomaly, stance and context remain visible with native attribution '
                'and classification, including a missing Claim where allowed.', result=result,
                entities=(entity,), native=(entity,), witnesses=profile.witnesses,
                reasons=_localized(result.reason_refs, (entity,), port),
                limit=result.interpretation_limit)
    for stage in profile.facts.stage_profiles:
        _presence_findings(rows, prepared, ledger, port, stage)


def _human_findings(rows, prepared, ledger, port, profile):
    facts = profile.facts
    # An ordinary review dependency alone does not establish overlap with the
    # process under review. Explicit channel/target overlap is handled below.
    for comparison in facts.comparisons:
        _comparison_findings(rows, prepared, ledger, port, comparison)


def _channel_overlap(rows, prepared, ledger, port, profile):
    facts = profile.facts
    dimensions = _field(facts.inquiry.node.fields, 'dependency_dimensions', port).items
    if not _analysis_contains(dimensions, 'organizational_control', port):
        return
    # The registered organizational graph owns channel-owner and control links.
    # Each exact Claim scope and inquiry metadata are examined separately.
    contexts = [facts.context.claim_refs]
    if facts.context.claim_refs:
        contexts.append(())
    for claims in contexts:
        local = _s._local(facts.context, port, claims=claims,
            dimension='organizational_control', view='organizational', predicates=('owned_by',))
        local = _p._context(local, port, subjects=(facts.channel.identifier, facts.target.identifier),
            predicates=('owned_by',), view='organizational')
        graph = _project(prepared, local, port)
        channel = _o._node(graph, facts.channel, port)
        target = _o._node(graph, facts.target, port)
        for node in graph.nodes:
            port.charge(2)
            if node.kind not in ('actor', 'model') or node is channel or node is target:
                continue
            left = _shortest_path(graph, channel, node, port)
            right = _shortest_path(graph, target, node, port)
            if left is None or right is None or not left.edges or not right.edges:
                continue
            entities = [facts.channel, facts.target, _analysis_lookup(prepared, node.identifier, port)]
            for edge in left.edges + right.edges:
                if edge.source_entity is not None:
                    port.charge(1)
                    entities.append(edge.source_entity)
            entities = _o._unique_entities(prepared, entities, port)
            scope = _scope(prepared, local, (facts.channel, facts.target), port)
            inputs, reasons, contrary = _premises(prepared, local, entities, scope, port)
            _check_edge_eligibility(graph, left.edges + right.edges, port)
            witnesses = (_path_witness(left, ledger, port), _path_witness(right, ledger, port))
            _emit(rows, prepared, local, ledger, port, 'correction_dependency_witness',
                'positive_witness', 'The selected correction channel and exact reviewed target '
                'have a recorded common control ancestor in the organizational view.',
                entities=entities, inputs=inputs, reasons=reasons, contrary=contrary,
                witnesses=witnesses, scope=scope, threats=('SIT-TH010',),
                limit='Organizational commonality does not establish coerced judgment, '
                'institutional capture or invalid correction.')


def _graph_findings(rows, prepared, parent, ledger, port, request):
    _require(type(request) is tuple and len(request) == 3)
    context, start_id, target_id = request
    _compatible(prepared, parent, context, port)
    _require(context.graph_view in ('citation', 'material_transformation', 'claim_origin',
                                  'model_evaluation', 'succession', 'assertion_assurance'))
    start = _analysis_lookup(prepared, start_id, port)
    target = _analysis_lookup(prepared, target_id, port)
    if parent.subject_refs:
        _require(_analysis_contains(parent.subject_refs, start_id, port) and
                 _analysis_contains(parent.subject_refs, target_id, port))
    context = _p._context(context, port,
        subjects=(start_id,) if start_id == target_id else (start_id, target_id),
        predicates=context.relation_types, coverage_kind=context.coverage_kind,
        view=context.graph_view)
    graph = _project(prepared, context, port)
    start_node, target_node = _o._node(graph, start, port), _o._node(graph, target, port)
    reach = _reachable(graph, (start_node,), port)
    path = _shortest_path(graph, start_node, target_node, port)
    scope = _scope(prepared, context, (start, target), port)
    if path is not None and path.edges:
        provider = _check_edge_eligibility(graph, path.edges, port)
        _require(provider.state == 'met')
        witness = _path_witness(path, ledger, port)
        entities = []
        for edge in path.edges:
            if edge.source_entity is not None:
                port.charge(1)
                entities.append(edge.source_entity)
        sources = _o._unique_entities(prepared, (start, target) + _o._tuple(entities, port), port)
        inputs, reasons, contrary = _premises(prepared, context, sources, scope, port)
        if context.graph_view == 'citation':
            code, threats = 'citation_path_witness', ('SIT-TH002',)
        elif context.graph_view in ('material_transformation', 'claim_origin'):
            code, threats = 'transformation_path_witness', ('SIT-TH002',)
        else:
            code, threats = None, ()
        if code is not None:
            _emit(rows, prepared, context, ledger, port, code, 'positive_witness',
                'An eligible explicit path connects these exact endpoints in the named typed view.',
                entities=sources, inputs=inputs, reasons=reasons, contrary=contrary,
                witnesses=(witness,), scope=scope, threats=threats,
                limit='Citation and material paths do not create Claim-specific acquisition '
                'dependence, independent corroboration or a syndication accusation.')
        transformers = []
        transformed = False
        for edge in path.edges:
            port.charge(1)
            if (edge.source_entity is not None and edge.predicate in
                    ('derived_from', 'copies', 'syndicated_from', 'summarizes', 'translates', 'quotes')):
                transformed = True
                details = _field(_field(edge.source_entity.node.fields, 'data', port), 'details', port)
                transformer = _lookup_pair(details.items, 'transformer_ref', port)
                if transformer is not None:
                    entity = _analysis_lookup(prepared, transformer[1], port)
                    if entity.kind == 'model':
                        port.charge(1)
                        transformers.append(entity)
        if transformers:
            _emit(rows, prepared, context, ledger, port, 'model_mediated_derivation_witness',
                'positive_witness', 'The explicit transformation chain discloses a model-generation '
                'role at its supplied basis.', entities=sources + _o._tuple(transformers, port),
                inputs=inputs, reasons=reasons, contrary=contrary, witnesses=(witness,), scope=scope,
                threats=('SIT-TH004',), limit='Model mediation neither detects synthetic authorship '
                'from prose nor establishes absent new reality contact.')
        elif transformed:
            _generation_findings(rows, prepared, context, ledger, port, path, witness, scope,
                sources, inputs, reasons, contrary)
    elif path is None:
        witness = _absence_witness(reach, target_node, ledger, port)
        _emit(rows, prepared, context, ledger, port, 'scoped_no_witness',
            'no_witness_in_examined_view', 'The completed typed search found no eligible witness '
            'between these endpoints in this examined supplied view.', entities=(start, target),
            witnesses=(witness,), scope=scope,
            limit='Examined nodes, predicates, observations and unknown frontiers remain in the '
            'finite witness. No outside-world independence or passed threat check follows.')
    for frontier in reach.frontiers:
        entity = _analysis_lookup(prepared, frontier.identifier, port)
        _emit(rows, prepared, context, ledger, port, 'provenance_gap', 'qualification_gap',
            'A reached explicit unresolved endpoint terminates the supplied history. '
            'Its missing ancestry remains unknown.', entities=(entity,), scope=scope,
            threats=('SIT-TH008',), native=(entity,),
            limit='An unknown frontier is a provenance gap, with no proof of erased history.')
    for component in _components(graph, port):
        if component.cycle is None:
            continue
        relevant = False
        for member in component.members:
            for reached in reach.nodes:
                port.charge(2)
                if member is reached:
                    relevant = True
        if relevant:
            witness = _cycle_witness(component, ledger, port)
            entities = [start]
            for edge in component.cycle.edges:
                if edge.source_entity is not None:
                    port.charge(1)
                    entities.append(edge.source_entity)
            entities = _o._unique_entities(prepared, entities, port)
            inputs, reasons, contrary = _premises(prepared, context, entities, scope, port)
            assurance = context.graph_view == 'assertion_assurance'
            _emit(rows, prepared, context, ledger, port,
                'assurance_loop_limitation' if assurance else 'view_cycle_witness',
                'qualification_gap' if assurance else 'positive_witness',
                'A finite cycle is witnessed in this exact typed view within the requested '
                'start\'s reachable area.', entities=entities, inputs=inputs, reasons=reasons,
                contrary=contrary, witnesses=(witness,), scope=scope,
                threats=('SIT-TH005',), limit='A cycle does not establish falsity, misconduct, '
                'absence of reality contact or represented benchmark feedback.')


def _generation_findings(rows, prepared, context, ledger, port, path, witness, scope,
                         sources, base_inputs, base_reasons, base_contrary):
    """A separately eligible generated_by role can qualify a real derivation.

    An EvidenceItem's exact Artifact link is retained when the generation role
    is stated at material granularity. No shared text or label is consulted.
    """
    ids, linked = [], []
    for node in path.nodes:
        entity = _analysis_lookup(prepared, node.identifier, port)
        port.charge(2)
        ids.append(entity.identifier)
        linked.append(entity)
        if entity.kind == 'evidence_item':
            artifact_id = _field(_field(entity.node.fields, 'data', port), 'artifact_ref', port)
            port.charge(2)
            ids.append(artifact_id)
            linked.append(_analysis_lookup(prepared, artifact_id, port))
    ids = _o._tuple(ids, port)
    claims = [context.claim_refs]
    if context.claim_refs:
        port.charge(1)
        claims.append(())
    for selected in claims:
        local = _s._local(context, port, claims=selected, dimension='model_ancestry',
            view='model_evaluation', predicates=('generated_by',))
        graph = _project(prepared, local, port)
        for edge in graph.edges:
            port.charge(3)
            if (edge.predicate != 'generated_by' or edge.target.kind != 'model' or
                    not _analysis_contains(ids, edge.source.identifier, port)):
                continue
            _check_edge_eligibility(graph, (edge,), port)
            role_path = _shortest_path(graph, edge.source, edge.target, port)
            _require(role_path is not None and bool(role_path.edges))
            role = _path_witness(role_path, ledger, port)
            model = _analysis_lookup(prepared, edge.target.identifier, port)
            entities = _o._unique_entities(prepared,
                sources + _o._tuple(linked, port) + (edge.source_entity, model), port)
            inputs, reasons, contrary = _premises(prepared, local, (edge.source_entity,), scope, port)
            port.charge(len(base_inputs) + len(base_reasons) + len(base_contrary) +
                        len(inputs) + len(reasons) + len(contrary) + 3)
            _emit(rows, prepared, context, ledger, port, 'model_mediated_derivation_witness',
                'positive_witness', 'The actual derivation chain has a separately recorded '
                'model-generation role on one of its exact contribution or material nodes.',
                entities=entities, inputs=base_inputs + inputs, reasons=base_reasons + reasons,
                contrary=base_contrary + contrary,
                witnesses=(witness, role), scope=scope, threats=('SIT-TH004',),
                limit='The derivation and model-role witnesses retain their distinct typed '
                'views and dimensions. No content detector or absent reality contact is inferred.')


def _claim_compatible(prepared, context, identifiers, port):
    if not context.claim_refs:
        return True
    for identifier in identifiers:
        entity = _analysis_lookup(prepared, identifier, port)
        claim = None
        if entity.kind == 'claim':
            claim = entity.identifier
        elif entity.kind == 'evidence_item':
            claim = _field(_field(entity.node.fields, 'data', port), 'claim_ref', port)
        if claim is not None and not _analysis_contains(context.claim_refs, claim, port):
            return False
    return True


def _native_findings(rows, prepared, context, ledger, port):
    inquiry = _analysis_lookup(prepared, context.inquiry_ref, port)
    targets = _field(inquiry.node.fields, 'target_object_refs', port).items
    for entity in prepared.entities:
        port.charge(2)
        local = context
        if entity.collection == 'assertions':
            obj = entity.node.fields
            if _field(obj, 'assertion_kind', port) != 'assessment':
                continue
            claim_ids = _field(_field(obj, 'scope', port), 'claim_refs', port).items
            if not claim_ids:
                local = _p._context(context, port, claims=())
            if not _analysis_scope(entity, local, port, subjects=False, relation_types=False):
                continue
            data = _field(obj, 'data', port)
            if not _claim_compatible(prepared, context, _field(data, 'subject_refs', port).items, port):
                continue
            if context.subject_refs:
                subjects = _field(data, 'subject_refs', port).items
                if not _analysis_subset(context.subject_refs, subjects, port):
                    continue
            kind = _field(data, 'assessment_kind', port)
            if kind == 'verification':
                detail = _field(data, 'details', port)
                if _field(detail, 'verification_scope', port) in ('identity', 'process', 'byte_integrity'):
                    _emit(rows, prepared, local, ledger, port, 'verification_scope_limitation',
                        'qualification_gap', 'The supplied verification is limited to its native '
                        'identity, process or byte-integrity scope; it cannot establish substantive '
                        'accuracy or a stronger source status.', entities=(entity,), native=(entity,),
                        threats=('SIT-TH009',))
            elif kind == 'classification':
                detail = _field(data, 'details', port)
                if (_field(detail, 'axis', port) == 'sil_governance_layer' and
                        _analysis_contains(_field(detail, 'labels', port).items, 'verified', port)):
                    _emit(rows, prepared, local, ledger, port, 'verification_scope_limitation',
                        'qualification_gap', 'A supplied verified-layer label cannot establish '
                        'substantive accuracy. Referenced verification, if any, retains its '
                        'separate native identity, process or byte-integrity scope.',
                        entities=(entity,), native=(entity,), threats=('SIT-TH009',))
            elif kind == 'conflict':
                subjects = []
                for identifier in _field(data, 'subject_refs', port).items:
                    subjects.append(_analysis_lookup(prepared, identifier, port))
                refs = _refs(_o._tuple(subjects, port), port)
                _emit(rows, prepared, local, ledger, port, 'recorded_data_conflict',
                    'recorded_conflict', 'An explicit supplied conflict retains its subjects, '
                    'resolution state and scope without majority or newest-wins selection.',
                    entities=(entity,) + _o._tuple(subjects, port), contrary=refs, native=(entity,))
        elif entity.kind == 'evaluation' and _analysis_contains(
                context.subject_refs or targets, entity.identifier, port):
            target_ids = _field(_field(entity.node.fields, 'data', port), 'target_refs', port).items
            if not _claim_compatible(prepared, context, target_ids, port):
                continue
            _emit(rows, prepared, local, ledger, port, 'attributed_external_observation',
                'attributed_observation', 'A supplied Evaluation and its reported result remain '
                'attributed input evidence with their original method, outcome and provenance.',
                entities=(entity,), native=(entity,),
                limit='Free text, external labels and extensions cannot assign a threat family '
                'or turn this report into a toolkit detector result.')
        elif entity.kind == 'evidence_item':
            data = _field(entity.node.fields, 'data', port)
            claim_id = _field(data, 'claim_ref', port)
            artifact_id = _field(data, 'artifact_ref', port)
            claims = context.claim_refs or _field(inquiry.node.fields, 'target_claim_refs', port).items
            seeds = _field(inquiry.node.fields, 'seed_evidence_refs', port).items
            kind = _field(data, 'epistemic_type', port)
            if (kind not in ('allegation', 'analytical_inference') or
                    not _analysis_contains(claims, claim_id, port) or
                    not _analysis_contains(seeds, entity.identifier, port)):
                continue
            if context.subject_refs and not any(_analysis_contains(context.subject_refs, value, port)
                    for value in (entity.identifier, claim_id, artifact_id)):
                continue
            claim = _analysis_lookup(prepared, claim_id, port)
            artifact = _analysis_lookup(prepared, artifact_id, port)
            _emit(rows, prepared, local, ledger, port, 'attributed_external_observation',
                'attributed_observation', 'A supplied source allegation or analytical inference '
                'remains attributed to its exact EvidenceItem, Claim and Artifact, without '
                'automatic assignment to a threat family.', entities=(entity, claim, artifact),
                native=(entity, claim, artifact), limit='No supplied Evaluation is required to '
                'retain an allegation; absent test evidence cannot become toolkit verification.')


def _findings(prepared, context, ledger, port, *, stage_profiles=(), graph_requests=()):
    """Build an atomic observation set from original current-job owners.

    Graph requests are (query_context, start_id, target_id). No source text
    supplies a condition, predicate program, detector or coverage boolean.
    """
    _analysis_start(prepared, context, port)
    _p._ledger(ledger, port)
    _require(type(stage_profiles) is tuple and type(graph_requests) is tuple)
    rows = []
    owners = (_o._OriginProfile, _p._ComparisonProfile, _e._EvaluatorProfile,
        _s._PresenceProfile, _cr._CorrectionProfile, _co._OutcomeProfile,
        _h._HumanReviewProfile, _cp._ContributionProfile, _i._InventoryProfile,
        _c._ContextProfile)
    for profile in stage_profiles:
        port.charge(5)
        _require(type(profile) in owners)
        facts = profile.facts
        _require(facts.prepared is prepared and facts.job_port is port)
        _compatible(prepared, context, facts.context, port)
        for result in profile.results:
            _require(type(result) is _r._Result and result.execution_state == 'completed')
            _charge_link(result.ref, port)
        _reason_findings(rows, prepared, ledger, port, profile)
        for owner, handler in ((_o._OriginProfile, _origin_findings),
                (_p._ComparisonProfile, _comparison_findings), (_e._EvaluatorProfile, _evaluator_findings),
                (_cr._CorrectionProfile, _route_findings), (_co._OutcomeProfile, _outcome_findings),
                (_s._PresenceProfile, _presence_findings), (_h._HumanReviewProfile, _human_findings),
                (_c._ContextProfile, _context_findings)):
            port.charge(1)
            if type(profile) is owner:
                handler(rows, prepared, ledger, port, profile)
                break
    for request in graph_requests:
        port.charge(1)
        _graph_findings(rows, prepared, context, ledger, port, request)
    _native_findings(rows, prepared, context, ledger, port)
    for text in _RELEASE_LIMITS:
        _analysis_text(text, port)
    port.charge(7)
    result = _FindingProfile(prepared, context, port, _o._tuple(rows, port), _RELEASE_LIMITS)
    port.check()
    return result
