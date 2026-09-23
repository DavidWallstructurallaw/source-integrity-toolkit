# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: CONTEXT_PRESERVATION. Paid finite M014 native context and links.

Definitions 26.5: preserve supplied anomalies and contestation, including
protected or unclassified context. M010 keeps ownership of every stage value.
"""
from dataclasses import dataclass

from ..contracts.bundle import _require, _Array, _freeze_object
from ..contracts.evidence import _SourceAddress
from ..contracts import results as _r
from ..contracts.report import (
    _charge_scope, _charge_input_ref, _charge_link, _charge_frozen,
    _ScopeCheckFact, _scope_check, _PopulationCompletion, _ComponentCompletion,
    _CompletionRecord, _completion_check,
)
from ..validation.structure import _field
from ..validation.semantics import (
    _analysis_start, _analysis_port, _analysis_lookup, _analysis_contains,
    _analysis_text, _analysis_address, _analysis_codes, _profile_ref,
)
from . import origins as _o
from . import process_comparison as _p
from . import presence as _presence_owner

_FIELDS = ('anomaly_context_disclosures', 'contestation_disclosures', 'tail_stage_result_links')
_STANCES = ('supports', 'contradicts', 'describes', 'qualifies', 'contextualizes', 'corroborates')
_ANCESTRY = ('originates_from', 'depends_on', 'derived_from', 'copies', 'syndicated_from',
             'summarizes', 'translates', 'quotes')
_LIMIT = ('Exact supplied context and attributed statements only. Unclassified anomalies may lack '
    'a Claim. No automatic rarity, demographic, ideological, truth, motive, suppression or equal-weight '
    'vote inference. Protected content remains withheld. Stance does not alter source membership or '
    'provenance qualification. Stage links retain the original M010 cohort and scope; no second '
    'retention metric or final-only suppression percentage is computed.')


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _ContextWitness:
    prepared: object
    context: object
    job_port: object
    members: tuple
    member_count: int


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _ContextFacts:
    prepared: object
    context: object
    job_port: object
    inquiry: object
    anomalies: tuple
    contestation: tuple
    context_entities: tuple
    documentary_links: tuple
    native_records: tuple
    record_contexts: tuple
    premises: tuple
    stage_profiles: tuple
    stage_results: tuple
    basis_entities: tuple
    problems: tuple
    stage_problems: tuple
    witnesses: tuple


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _ContextProfile:
    facts: _ContextFacts
    results: tuple
    witnesses: tuple


def _refs(entities, port):
    values = []
    for entity in entities:
        port.charge(1)
        values.append(_profile_ref(entity, port))
    return _o._tuple(values, port)


def _ids(entities, port):
    values = []
    for entity in entities:
        port.charge(1)
        values.append(entity.identifier)
    return _o._tuple(values, port)


def _native_scope(entity, context, port):
    """Attributed context is retained across native dimensions, never projected."""
    scope = _field(entity.node.fields, 'scope', port)
    claims = _field(scope, 'claim_refs', port).items
    inquiry_match = _analysis_contains(_field(scope, 'inquiry_refs', port).items, context.inquiry_ref, port)
    if not inquiry_match or bool(claims) != bool(context.claim_refs):
        return False
    if not claims:
        return True
    for claim in context.claim_refs:
        port.charge(1)
        if _analysis_contains(claims, claim, port):
            return True
    return False


def _connected_context(prepared, sources, documentary_links, port):
    # Object identity comes from this admitted bundle, not caller identifiers.
    # Each native source is visited once. Documentary references never become
    # affirmative graph edges or introduce a second selected cohort.
    port.charge(len(sources) * 2 + 2)
    retained, frontier = set(sources), set(sources)
    while frontier:
        additions = set()
        for link in prepared.links:
            port.charge(3)
            if link.owner not in frontier or link.target.collection == 'inquiries':
                continue
            port.charge(40)
            # Preserve the original coverage assertion, without traversing its
            # declared member universe as another source's original context.
            if (link.selector.startswith('data.details.member_refs[')
                    or link.selector.startswith('data.details.omitted_refs[')):
                continue
            if link.target not in retained:
                port.charge(1)
                additions.add(link.target)
        for candidate, start in documentary_links:
            port.charge(3)
            if start in frontier and candidate not in retained:
                port.charge(1)
                additions.add(candidate)
        port.charge(len(additions) + 1)
        retained.update(additions)
        frontier = additions
    ordered = []
    for entity in prepared.entities:
        port.charge(1)
        if entity in retained:
            port.charge(1)
            ordered.append(entity)
    return _o._unique_entities(prepared, ordered, port)


def _record_context(facts, entity, port):
    for source, retained in facts.record_contexts:
        port.charge(1)
        if source is entity:
            return retained
    raise TypeError('missing_context_selection')


def _context_facts(prepared, context, ledger, port, *, stage_requests=()):
    inquiry = _analysis_start(prepared, context, port)
    _p._ledger(ledger, port)
    _require(context.dependency_dimension is None and not context.relation_types)
    _require(context.graph_view in (None, 'stance_contestation'))
    _require(type(stage_requests) is tuple)
    for claim in context.claim_refs:
        _require(_analysis_contains(_field(inquiry.node.fields, 'target_claim_refs', port).items, claim, port))
    anomalies, contestation, documentary, contextual_assessments = [], [], [], []
    for entity in prepared.entities:
        port.charge(1)
        if entity.kind == 'anomaly':
            data = _field(entity.node.fields, 'data', port)
            claim = _field(data, 'claim_ref', port)
            if (not _analysis_contains(_field(data, 'inquiry_refs', port).items, context.inquiry_ref, port)
                    or claim is not None and not _analysis_contains(context.claim_refs, claim, port)):
                continue
            if context.subject_refs and not _analysis_contains(context.subject_refs, entity.identifier, port):
                continue
            port.charge(1)
            anomalies.append(entity)
        elif entity.collection == 'assertions' and _native_scope(entity, context, port):
            data = _field(entity.node.fields, 'data', port)
            kind = _field(entity.node.fields, 'assertion_kind', port)
            if kind == 'relation':
                predicate = _field(data, 'predicate', port)
                if predicate in _STANCES:
                    source = _analysis_lookup(prepared, _field(data, 'from_ref', port), port)
                    # A broad declared assertion scope does not bind a stance
                    # about another actual Claim to this selected Claim.
                    destination = _analysis_lookup(prepared, _field(data, 'to_ref', port), port)
                    bound_claims = []
                    for endpoint in (source, destination):
                        port.charge(1)
                        if endpoint.kind == 'claim':
                            bound_claims.append(endpoint.identifier)
                        elif endpoint.kind == 'evidence_item':
                            bound_claims.append(_field(_field(endpoint.node.fields, 'data', port), 'claim_ref', port))
                    if bound_claims and not any(_analysis_contains(context.claim_refs, claim, port)
                                               for claim in bound_claims):
                        continue
                    endpoints = (_field(data, 'from_ref', port), _field(data, 'to_ref', port), entity.identifier)
                    if context.subject_refs and not any(
                            _analysis_contains(context.subject_refs, endpoint, port) for endpoint in endpoints):
                        continue
                    port.charge(1)
                    contestation.append(entity)
                elif predicate in _ANCESTRY and _field(data, 'dimension', port) == 'acquisition':
                    port.charge(1)
                    documentary.append(entity)
            else:
                assessment_kind = _field(data, 'assessment_kind', port)
                if assessment_kind in ('classification', 'conflict'):
                    port.charge(1)
                    contextual_assessments.append(entity)
                elif assessment_kind == 'origin_boundary':
                    port.charge(1)
                    documentary.append(entity)
    anomalies = _o._unique_entities(prepared, anomalies, port)
    contestation = _o._unique_entities(prepared, contestation, port)
    documentary_links = []
    for entity in documentary:
        data = _field(entity.node.fields, 'data', port)
        if _field(entity.node.fields, 'assertion_kind', port) == 'relation':
            start = _analysis_lookup(prepared, _field(data, 'from_ref', port), port)
            port.charge(1)
            documentary_links.append((entity, start))
        else:
            for identifier in _field(data, 'subject_refs', port).items:
                start = _analysis_lookup(prepared, identifier, port)
                port.charge(1)
                documentary_links.append((entity, start))
    documentary_links = _o._tuple(documentary_links, port)
    port.charge(len(anomalies) + len(contestation))
    context_entities = _connected_context(prepared, anomalies + contestation, documentary_links, port)
    contextual = []
    known_ids = _ids(context_entities, port)
    for assessment in contextual_assessments:
        data = _field(assessment.node.fields, 'data', port)
        relevant = not context.subject_refs or _analysis_contains(context.subject_refs, assessment.identifier, port)
        for identifier in _field(data, 'subject_refs', port).items:
            port.charge(1)
            relevant = (relevant or _analysis_contains(known_ids, identifier, port)
                        or _analysis_contains(context.subject_refs, identifier, port))
        if relevant:
            port.charge(1)
            contextual.append(assessment)
    port.charge(len(contestation) + len(contextual))
    contestation = _o._unique_entities(prepared, contestation + _o._tuple(contextual, port), port)
    if contextual:
        port.charge(len(anomalies) + len(contestation))
        context_entities = _connected_context(prepared, anomalies + contestation, documentary_links, port)
    record_contexts = []
    port.charge(len(anomalies) + len(contestation) + 1)
    primary = anomalies + contestation
    for entity in primary:
        retained = context_entities if len(primary) == 1 else _connected_context(
            prepared, (entity,), documentary_links, port)
        port.charge(1)
        record_contexts.append((entity, retained))
    native_records = []
    for collection in ('records', 'assertions', 'evidence_references'):
        for native in _field(prepared.captured_tree, collection, port).items:
            identifier = _field(native, 'id', port)
            entity = _analysis_lookup(prepared, identifier, port)
            port.charge(len(context_entities) + 1)
            if entity in context_entities:
                port.charge(1)
                native_records.append((entity, native))
    premises, problems = [], []
    local = _p._context(context, port, subjects=(), view='stance_contestation')
    for entity in anomalies + contestation:
        premise_context = local
        if entity.collection == 'assertions':
            native_claims = _field(_field(entity.node.fields, 'scope', port), 'claim_refs', port).items
            claims = []
            for claim in context.claim_refs:
                port.charge(1)
                if _analysis_contains(native_claims, claim, port):
                    claims.append(claim)
            premise_context = _p._context(local, port, claims=_o._tuple(claims, port), view='stance_contestation')
        premise = _p._premise(prepared, entity, premise_context, premises, port)
        for code in _p._codes(premise, port):
            port.charge(1)
            problems.append((code, entity))
        if entity.kind == 'anomaly':
            data = _field(entity.node.fields, 'data', port)
            if _field(data, 'original_context', port) is None:
                port.charge(1)
                problems.append(('context_withheld_or_unavailable', entity))
    profiles, stage_results, nested_witnesses, stage_problems = [], [], [], []
    request_keys = []
    for request in stage_requests:
        port.charge(1)
        _require(type(request) is tuple and len(request) == 2)
        coverage, anchor = request
        _require(coverage is None or type(coverage) is str and bool(coverage))
        if coverage is not None:
            _analysis_text(coverage, port)
        _require(anchor is None or type(anchor) is tuple and len(anchor) == 3)
        if anchor is not None:
            for part in anchor:
                _analysis_text(part, port)
        duplicate = False
        for old_coverage, old_anchor in request_keys:
            port.charge(2)
            if old_coverage == coverage and _presence_owner._same(old_anchor, anchor, port):
                duplicate = True
        _require(not duplicate)
        port.charge(1)
        request_keys.append(request)
        claims = context.claim_refs
        if coverage is not None:
            coverage_entity = _analysis_lookup(prepared, coverage, port)
            _require(coverage_entity.collection == 'assertions')
            native_claims = _field(_field(coverage_entity.node.fields, 'scope', port), 'claim_refs', port).items
            chosen = []
            for claim in context.claim_refs:
                port.charge(1)
                if _analysis_contains(native_claims, claim, port):
                    chosen.append(claim)
            _require(not native_claims or bool(chosen))
            claims = _o._tuple(chosen, port)
        stage_context = _p._context(context, port, claims=claims, subjects=(), view='pipeline_stages')
        profile = _presence_owner._presence(prepared, stage_context, ledger, port,
            family='SIT-M010', coverage_ref=coverage, stage_anchor=anchor)
        port.charge(len(anomalies) + 1)
        selected_stage_subjects = list(anomalies)
        for identifier in context.subject_refs:
            entity = _analysis_lookup(prepared, identifier, port)
            if _presence_owner._member_scope(entity, context, port):
                port.charge(1)
                selected_stage_subjects.append(entity)
        for stance in contestation:
            fields = stance.node.fields
            if _field(fields, 'assertion_kind', port) == 'relation':
                data = _field(fields, 'data', port)
                for key in ('from_ref', 'to_ref'):
                    endpoint = _analysis_lookup(prepared, _field(data, key, port), port)
                    if endpoint.kind == 'evidence_item':
                        port.charge(1)
                        selected_stage_subjects.append(endpoint)
        selected_ids = _ids(_o._unique_entities(prepared, selected_stage_subjects, port), port)
        relevant = coverage is None and anchor is None
        for member in profile.facts.subjects:
            port.charge(1)
            relevant = relevant or _analysis_contains(selected_ids, member.identifier, port)
        if coverage is None:
            for record in profile.facts.stages:
                subject_id = _field(_field(record.node.fields, 'data', port), 'subject_ref', port)
                relevant = relevant or _analysis_contains(selected_ids, subject_id, port)
            # No observed stage can still be an explicitly missing history
            # question for the selected anomaly/contestation population.
            relevant = relevant or bool(selected_ids) and not profile.facts.stages
        _require(relevant)
        port.charge(len(profile.witnesses) + 2)
        profiles.append(profile)
        nested_witnesses.extend(profile.witnesses)
        for result in profile.results:
            port.charge(1)
            if result.result_state == 'available':
                port.charge(1)
                stage_results.append(result)
            for reason in result.reason_refs:
                for source in reason.input_refs:
                    port.charge(1)
                    stage_problems.append((reason.code, _analysis_lookup(prepared, source.identifier, port)))
    basis = [inquiry]
    port.charge(len(context_entities) + 1)
    basis.extend(context_entities)
    for premise in premises:
        for fact in (premise.basis, premise.conflict):
            for address in fact.support_refs:
                port.charge(1)
                basis.append(_analysis_lookup(prepared, address.record_id, port))
    basis = _o._unique_entities(prepared, basis, port)
    reservation = ledger.reserve(witnesses=1, members=len(basis))
    for entity in basis:
        _analysis_address(entity, port)
    port.charge(7)
    witness = _ContextWitness(prepared, context, port, basis, len(basis))
    ledger.retain(reservation)
    port.charge(len(nested_witnesses) + 18)
    facts = _ContextFacts(prepared, context, port, inquiry, anomalies, contestation,
        context_entities, _o._tuple(documentary_links, port), _o._tuple(native_records, port),
        _o._tuple(record_contexts, port), _o._tuple(premises, port), _o._tuple(profiles, port),
        _o._tuple(stage_results, port), basis, _o._tuple(problems, port), _o._tuple(stage_problems, port),
        _o._tuple(nested_witnesses + [witness], port))
    port.check()
    return facts


def _check_facts(facts, port):
    _analysis_port(port)
    port.charge(3)
    _require(type(facts) is _ContextFacts and facts.job_port is port)


def _scope(facts, field, port):
    context, anchor = facts.context, []
    claims = _refs(_presence_owner._entities(facts.prepared, context.claim_refs, port), port)
    selected = facts.anomalies if field == _FIELDS[0] else facts.contestation if field == _FIELDS[1] else facts.anomalies + facts.contestation
    targets = _refs(_o._unique_entities(facts.prepared, selected, port), port)
    for part in context.operation_anchor:
        port.charge(1)
        if type(part) is _SourceAddress:
            part = _o._source_ref(part, port)
        elif type(part) is str:
            _analysis_text(part, port)
        anchor.append(part)
    for profile in facts.stage_profiles if field == _FIELDS[2] else ():
        target = profile.facts.target
        if target.coverage is not None:
            port.charge(1)
            anchor.append(_profile_ref(target.coverage, port))
        for part in target.anchor or ('unestablished_stage',):
            _analysis_text(part, port)
            port.charge(1)
            anchor.append(part)
    for items in (claims, targets):
        for ref in items:
            _charge_input_ref(ref, port, repeats=len(items) + 3)
    if context.requested_time is not None:
        _charge_frozen(context.requested_time.fields, port)
    port.charge(len(claims) + len(targets) + len(anchor) + 20)
    scope = _r._Scope(_profile_ref(facts.inquiry, port), claims, targets, None, 'stance_contestation',
        context.temporal_basis, context.requested_time, (),
        ('Supplied Inquiry/Claim context; null-Claim anomalies keep their structural null. '
         'Every linked stage retains its separate original cohort scope.',), _o._tuple(anchor, port))
    _charge_scope(scope, port)
    return scope


def _frozen(pairs, port):
    # Values are existing immutable admitted bags or locally frozen arrays.
    # This constructor links them without traversing/re-encoding their trees.
    # _freeze_object pays its actual keys, entry checks and sorting work.
    for key, value in pairs:
        _analysis_text(key, port)
        port.charge(1)
    return _freeze_object(pairs, port)


def _native_record(facts, entity, port):
    for source, native in facts.native_records:
        port.charge(1)
        if source is entity:
            return native
    raise TypeError('missing_context_record')


def _disclosures(facts, field, port):
    records = []
    if field == _FIELDS[2]:
        for result in facts.stage_results:
            _charge_link(result.ref, port)
            values = _frozen((('source_result_state', result.result_state),
                             ('source_value_kind', result.value_kind)), port)
            port.charge(7)
            records.append(_r._Disclosure(result.ref, values,
                ('Exact result under M010 and this job. Its source cohort and qualification remain authoritative; '
                 'no copied numerator, denominator, fraction, interval or inferred suppression.',)))
    else:
        selected = facts.anomalies if field == _FIELDS[0] else facts.contestation
        for entity in selected:
            context_records = []
            for source in _record_context(facts, entity, port):
                port.charge(1)
                context_records.append(_native_record(facts, source, port))
            port.charge(len(context_records) + 2)
            native_context = _Array(_o._tuple(context_records, port))
            codes = []
            for code, source in facts.problems:
                port.charge(1)
                if source is entity:
                    port.charge(1)
                    codes.append(code)
            fields = _frozen((('native_record', _native_record(facts, entity, port)),
                ('context_records', native_context), ('reason_codes', _Array(_analysis_codes(codes, port)))), port)
            _charge_input_ref(_profile_ref(entity, port), port)
            port.charge(7)
            records.append(_r._Disclosure(_profile_ref(entity, port), fields,
                ('Original native context, classification, provenance, gaps and reference availability are retained. '
                 'Scoped documentary context is separate from the supplied stance; neither is a truth verdict.',)))
    port.charge(len(records) + 3)
    return _r._RecordDisclosures(_o._tuple(records, port))


def _reasons(facts, scope, ref, field, port):
    reasons = []
    selected = facts.anomalies if field == _FIELDS[0] else facts.contestation
    problems = facts.stage_problems if field == _FIELDS[2] else facts.problems
    for code in _r.REASON_CODES:
        sources = []
        for incoming, source in problems:
            port.charge(1)
            if incoming == code and (field == _FIELDS[2] or source in selected):
                port.charge(1)
                sources.append(source)
        if not sources:
            continue
        inputs = _refs(_o._unique_entities(facts.prepared, sources, port), port)
        for source in inputs:
            _charge_input_ref(source, port, repeats=len(inputs) + 3)
        for unused in range(3):
            _charge_scope(scope, port)
        port.charge(len(inputs) + 18)
        reasons.append(_r._Reason(code, scope, (ref,), inputs,
            'Exact supplied context or requested stage evidence retains this limitation. '
            'Unavailable content or intake history is not evidence of suppression or agreement.',
            'conflict' if code == 'premise_disputed' else 'structural_inapplicability'
            if code in ('no_applicable_subject', 'completion_interval_not_needed') else 'evidence_gap'))
    return _o._tuple(reasons, port)


def _checks(facts, ref, field, port):
    selected = facts.anomalies if field == _FIELDS[0] else facts.contestation
    checks = []
    for key in ('PC01', 'PC02', 'PC05', 'PC09', 'PC10', 'PC16', 'PC17', 'PC18', 'PC23'):
        if key == 'PC02':
            checks.append(_scope_check(_ScopeCheckFact(ref, ref.scope), port))
            continue
        values, entities = [], []
        if key in ('PC05', 'PC09', 'PC10') and field != _FIELDS[2]:
            for premise in facts.premises:
                port.charge(1)
                if premise.source not in selected:
                    continue
                value = (premise.basis.state if key == 'PC05' else premise.conflict.state if key == 'PC09'
                    else premise.time.state if premise.time is not None else 'not_applicable')
                port.charge(2)
                values.append(value)
                entities.append(premise.source)
        elif field == _FIELDS[2] and key in ('PC05', 'PC09', 'PC10', 'PC16', 'PC17', 'PC18'):
            for profile in facts.stage_profiles:
                for result in profile.results:
                    for check in result.check_refs:
                        port.charge(1)
                        if check.check_id == key:
                            port.charge(1)
                            values.append(check.state)
                            for source in check.input_refs:
                                port.charge(1)
                                entities.append(_analysis_lookup(facts.prepared, source.identifier, port))
        state = ('met' if key in ('PC01', 'PC23') else _p._aggregate(values, port))
        seen, distinct = set(), []
        for entity in entities:
            port.charge(3)
            if entity not in seen:
                port.charge(2)
                seen.add(entity)
                distinct.append(entity)
        inputs = _refs(_o._unique_entities(facts.prepared, distinct, port), port)
        if key == 'PC23':
            inputs = _refs(_o._unique_entities(facts.prepared, facts.anomalies + facts.contestation, port), port)
        for source in inputs:
            _charge_input_ref(source, port, repeats=len(inputs) + 3)
        _charge_link(ref, port)
        port.charge(len(inputs) + 14)
        checks.append(_r._PrerequisiteCheck(key, ref, state, inputs, (),
            'Context retention is executed independently of native truth or documentary qualification. '
            'PC16-PC18 are supplied only by the original requested M010 execution.'))
    return checks


def _context_results(facts, port):
    _check_facts(facts, port)
    outputs = []
    for field in _FIELDS:
        _check_facts(facts, port)
        scope = _scope(facts, field, port)
        selected = facts.anomalies if field == _FIELDS[0] else facts.contestation if field == _FIELDS[1] else ()
        used = [facts.inquiry]
        if field == _FIELDS[2]:
            for profile in facts.stage_profiles:
                if profile.facts.target.coverage is not None:
                    port.charge(1)
                    used.append(profile.facts.target.coverage)
        else:
            for entity in selected:
                related = _record_context(facts, entity, port)
                port.charge(len(related))
                used.extend(related)
            for premise in facts.premises:
                port.charge(len(selected) + 1)
                if premise.source in selected:
                    for qualification in (premise.basis, premise.conflict):
                        for address in qualification.support_refs:
                            port.charge(1)
                            used.append(_analysis_lookup(facts.prepared, address.record_id, port))
        basis = []
        for entity in _o._unique_entities(facts.prepared, used, port):
            source = _profile_ref(entity, port)
            _charge_input_ref(source, port)
            port.charge(3)
            basis.append(_r._BasisRef(source))
        basis = _o._tuple(basis, port)
        _charge_scope(scope, port)
        port.charge(8)
        witnesses = (_r._WitnessRef(scope, 'member_set', ('context_preservation',)),)
        _charge_scope(scope, port)
        port.charge(180)
        ref = _r._ResultRef('SIT-M014', field, scope)
        members = _refs(selected, port)
        for member in members:
            _charge_input_ref(member, port, repeats=len(members) + 3)
        for item in basis:
            _charge_link(item, port)
        port.charge(len(members) * len(members) + len(basis) + 16)
        population = _r._Population(scope, 'record', members,
            'Exact finite supplied context records; stage references retain M010 populations separately.',
            (), basis, 'enumerated_for_scope', ('No outside-world consensus or anomaly denominator.',))
        value = _disclosures(facts, field, port)
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
        completion = _CompletionRecord(ref, (population,), (_PopulationCompletion(population, members),),
            _o._tuple(components, port))
        checks.append(_completion_check(completion, port))
        for unused in range(2):
            _charge_link(ref, port)
            _charge_link(population, port)
            for links in (checks, basis, reasons, witnesses):
                for link in links:
                    _charge_link(link, port)
        port.charge(len(checks) + len(basis) + len(reasons) + 30)
        outputs.append(_r._Result(ref, (population,), 'completed', 'available', 'attributed_record',
            'record_disclosures', value, _o._tuple(checks, port), basis, witnesses, reasons, _LIMIT))
    port.check()
    return _o._tuple(outputs, port)


def _context_preservation(prepared, context, ledger, port, *, stage_requests=()):
    facts = _context_facts(prepared, context, ledger, port, stage_requests=stage_requests)
    results = _context_results(facts, port)
    port.charge(4)
    profile = _ContextProfile(facts, results, facts.witnesses)
    port.check()
    return profile
