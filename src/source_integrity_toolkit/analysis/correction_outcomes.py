# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: CORRECTION_OUTCOMES. Paid finite M012 case and linked-change facts.

Definitions 20.2 and 27.2-27.3: each inventory retains its actual counting
unit. Native handling, observations and capacity remain attributed records.
"""
from dataclasses import dataclass

from ..contracts.bundle import _require, _Array, _freeze_object
from ..contracts.evidence import _SourceAddress, _Node
from ..contracts import results as _r
from ..contracts.report import (
    _charge_scope, _charge_input_ref, _charge_link, _charge_frozen,
    _ScopeCheckFact, _scope_check, _PopulationCompletion, _ComponentCompletion,
    _CompletionRecord, _completion_check,
)
from ..validation.structure import _field
from ..validation.semantics import (
    _analysis_start, _analysis_port, _analysis_lookup, _analysis_contains,
    _analysis_text, _analysis_address, _analysis_codes, _analysis_scope,
    _qualify_identity, _profile_ref, _compare_times,
)
from . import origins as _o
from . import process_comparison as _p

_FIELDS = ('correction_case_record_count', 'handling_event_record_count',
           'linked_change_event_record_count', 'documentary_linked_change_target_count',
           'cases_with_documentary_linked_change_count', 'correction_case_disclosures',
           'correction_target_change_disclosures', 'reported_capacity_disclosures')
_LIMIT = ('Finite supplied case and process-evidence inventory only. Native handling outcomes '
    'are nonexclusive records. Documentary linkage establishes neither substantive correctness '
    'nor authority, causal success, complete downstream propagation or sustained capacity. '
    'Missing change evidence leaves the requested effect unavailable. Reported capacity, load, '
    'unit and horizon remain supplied statements without normalization or an adequacy formula.')


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Change:
    source: object
    case: object
    before: object
    after: object
    removal: bool
    premise: object
    identity: object
    time_state: str
    documentary_state: str
    reason_codes: tuple


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _TargetChange:
    case: object
    before: object
    events: tuple
    qualified_events: tuple
    declared: bool
    selected: bool
    documentary_state: str
    reason_codes: tuple


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _OutcomeWitness:
    prepared: object
    context: object
    job_port: object
    members: tuple
    source_refs: tuple
    member_count: int


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _OutcomeFacts:
    prepared: object
    context: object
    job_port: object
    inquiry: object
    cases: tuple
    handling: tuple
    changes: tuple
    change_facts: tuple
    target_changes: tuple
    selected_targets: tuple
    explicit_target_selection: bool
    observations: tuple
    observation_results: tuple
    capacities: tuple
    premises: tuple
    basis_entities: tuple
    problems: tuple
    witnesses: tuple


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _OutcomeProfile:
    facts: _OutcomeFacts
    results: tuple
    witnesses: tuple


def _refs(entities, port):
    rows = []
    for entity in entities:
        port.charge(1)
        rows.append(_profile_ref(entity, port))
    return _o._tuple(rows, port)


def _ids(entities, port):
    rows = []
    for entity in entities:
        port.charge(1)
        _analysis_text(entity.identifier, port)
        rows.append(entity.identifier)
    return _o._tuple(rows, port)


def _intersects(identifiers, population, port):
    for identifier in identifiers:
        port.charge(1)
        if _analysis_contains(population, identifier, port):
            return True
    return False


def _inquiry_targets(prepared, inquiry, context, port):
    """Definitions 20.2's explicit population, preserving selected Claim IDs."""
    targets = []
    all_claims = _field(inquiry.node.fields, 'target_claim_refs', port).items
    for claim in context.claim_refs:
        _require(_analysis_contains(all_claims, claim, port))
    for identifiers in (context.claim_refs or all_claims,
            _field(inquiry.node.fields, 'target_object_refs', port).items,
            _field(inquiry.node.fields, 'seed_artifact_refs', port).items):
        for identifier in identifiers:
            port.charge(1)
            targets.append(_analysis_lookup(prepared, identifier, port))
    for identifier in _field(inquiry.node.fields, 'seed_evidence_refs', port).items:
        entity = _analysis_lookup(prepared, identifier, port)
        if entity.kind != 'evidence_item':
            continue
        data = _field(entity.node.fields, 'data', port)
        if context.claim_refs and not _analysis_contains(
                context.claim_refs, _field(data, 'claim_ref', port), port):
            continue
        port.charge(1)
        targets.append(entity)
        artifact = _analysis_lookup(prepared, _field(data, 'artifact_ref', port), port)
        if artifact.kind == 'artifact':
            port.charge(1)
            targets.append(artifact)
    return _o._unique_entities(prepared, targets, port)


def _change(prepared, event, case, local, premises, port):
    data = _field(event.node.fields, 'data', port)
    details = _field(data, 'details', port)
    before = _analysis_lookup(prepared, _field(details, 'before_ref', port), port)
    after_id = _field(details, 'after_ref', port)
    after = None if after_id is None else _analysis_lookup(prepared, after_id, port)
    removal = after is None and bool(_field(details, 'after_absence_reason', port))
    premise = _p._premise(prepared, event, local, premises, port)
    endpoints = (before.identifier,) if after is None else (before.identifier, after.identifier)
    identity = _qualify_identity(prepared, endpoints, local, port)
    values = _p._codes(premise, port)
    port.charge(len(values) + len(identity.reason_codes) + 2)
    codes = list(values + identity.reason_codes)
    resolved = before.kind != 'unresolved_reference' and (
        removal or after is not None and after.kind != 'unresolved_reference')
    if not resolved:
        port.charge(1)
        codes.append('before_after_unresolved')
    time_state = 'not_applicable'
    occurrence = _Node('TimeValue', _field(data, 'occurred_at', port))
    if local.temporal_basis == 'time_specific':
        comparison = _compare_times(occurrence, local.requested_time, port)
        time_state = ('met' if comparison.comparison in ('before', 'equal') else
                      'unmet' if comparison.comparison == 'after' else 'unknown')
        if time_state != 'met':
            port.charge(1)
            codes.append('time_applicability_unknown')
    elif _field(occurrence.fields, 'state', port) != 'known':
        port.charge(1)
        codes.append('time_applicability_unknown')
    qualified = (resolved and identity.state == 'met' and premise.basis.state == 'met'
        and premise.conflict.state == 'met' and time_state in ('met', 'not_applicable'))
    if not qualified:
        port.charge(1)
        codes.append('change_evidence_missing')
    port.charge(13)
    return _Change(event, case, before, after, removal, premise, identity, time_state,
                   'met' if qualified else 'unknown', _analysis_codes(codes, port))


def _correction_outcome_facts(prepared, context, ledger, port, *, selected_targets=None):
    inquiry = _analysis_start(prepared, context, port)
    _p._ledger(ledger, port)
    port.charge(5)
    _require(context.dependency_dimension is None and not context.relation_types)
    _require(context.graph_view in (None, 'correction_outcomes'))
    _require(selected_targets is None or type(selected_targets) is tuple)
    inquiry_targets = _inquiry_targets(prepared, inquiry, context, port)
    relevant_ids = _ids(inquiry_targets, port)
    cases, handling, changes, all_events = [], [], [], []
    for entity in prepared.entities:
        port.charge(1)
        if entity.kind != 'correction_event':
            continue
        port.charge(1)
        all_events.append(entity)
        data = _field(entity.node.fields, 'data', port)
        if _field(data, 'event_kind', port) != 'submission':
            continue
        if not _intersects(_field(data, 'target_refs', port).items, relevant_ids, port):
            continue
        if context.subject_refs and not _analysis_contains(context.subject_refs, entity.identifier, port):
            continue
        port.charge(1)
        cases.append(entity)
    cases = _o._unique_entities(prepared, cases, port)
    case_ids = _ids(cases, port)
    for identifier in context.subject_refs:
        _require(_analysis_contains(case_ids, identifier, port))
    declared, channels = [], []
    sources = [_analysis_address(inquiry, port)]
    for case in cases:
        data = _field(case.node.fields, 'data', port)
        for identifier in _field(data, 'target_refs', port).items:
            port.charge(1)
            declared.append(_analysis_lookup(prepared, identifier, port))
        port.charge(1)
        sources.append(_analysis_address(case, port, 'data.target_refs'))
    declared = _o._unique_entities(prepared, declared, port)
    declared_ids = _ids(declared, port)
    selected = []
    for identifier in declared_ids if selected_targets is None else selected_targets:
        _analysis_text(identifier, port)
        _require(_analysis_contains(declared_ids, identifier, port))
        port.charge(1)
        selected.append(_analysis_lookup(prepared, identifier, port))
    selected = _o._unique_entities(prepared, selected, port)
    selected_ids = _ids(selected, port)
    local = _p._context(context, port, subjects=(), predicates=(), view='correction_outcomes')
    premises, change_facts, target_changes, problems = [], [], [], []
    basis_entities = [inquiry]
    for case in cases:
        _p._premise(prepared, case, local, premises, port)
    for event in all_events:
        data = _field(event.node.fields, 'data', port)
        kind = _field(data, 'event_kind', port)
        case_id = event.identifier if kind == 'submission' else _field(data, 'case_ref', port)
        if not _analysis_contains(case_ids, case_id, port):
            continue
        port.charge(2)
        basis_entities.append(event)
        sources.append(_analysis_address(event, port, 'data.case_ref'))
        channel_id = _field(data, 'channel_ref', port)
        if channel_id is not None:
            port.charge(1)
            channels.append(_analysis_lookup(prepared, channel_id, port))
        if kind == 'handling':
            port.charge(1)
            handling.append(event)
            _p._premise(prepared, event, local, premises, port)
        elif kind == 'change':
            fact = _change(prepared, event, _analysis_lookup(prepared, case_id, port), local, premises, port)
            port.charge(4)
            changes.append(event)
            change_facts.append(fact)
            basis_entities.append(fact.before)
            if fact.after is not None:
                port.charge(1)
                basis_entities.append(fact.after)
            for selector in ('data.details.before_ref', 'data.details.after_ref'):
                port.charge(1)
                sources.append(_analysis_address(event, port, selector))
    for case in cases:
        case_targets = _field(_field(case.node.fields, 'data', port), 'target_refs', port).items
        before_entities = []
        for identifier in case_targets:
            port.charge(1)
            before_entities.append(_analysis_lookup(prepared, identifier, port))
        for change in change_facts:
            port.charge(1)
            if change.case is case:
                port.charge(1)
                before_entities.append(change.before)
        for before in _o._unique_entities(prepared, before_entities, port):
            events, qualified, codes = [], [], []
            for change in change_facts:
                port.charge(1)
                if change.case is case and change.before is before:
                    port.charge(len(change.reason_codes) + 2)
                    events.append(change.source)
                    codes.extend(change.reason_codes)
                    if change.documentary_state == 'met':
                        port.charge(1)
                        qualified.append(change.source)
            if not qualified:
                port.charge(1)
                codes.append('change_evidence_missing')
            codes = _analysis_codes(codes, port)
            native_target = _analysis_contains(case_targets, before.identifier, port)
            chosen = native_target and _analysis_contains(selected_ids, before.identifier, port)
            port.charge(14)
            target_changes.append(_TargetChange(case, before, _o._tuple(events, port),
                _o._tuple(qualified, port), native_target, chosen,
                'met' if qualified else 'unknown', codes))
            for code in codes:
                port.charge(1)
                problems.append((code, before))
            port.charge(1)
            basis_entities.append(before)
    # A target-bound review/result remains an attributed observation. No prose
    # parser invents a non-propagation subtype or a change from a later edit.
    observed_targets = []
    for target in target_changes:
        port.charge(1)
        observed_targets.append(target.before.identifier)
    observations, observation_results, capacities, relevant_evaluations = [], [], [], []
    for entity in prepared.entities:
        port.charge(1)
        if entity.kind != 'evaluation':
            continue
        data = _field(entity.node.fields, 'data', port)
        if (_analysis_contains(relevant_ids, entity.identifier, port) or
                _intersects(_field(data, 'target_refs', port).items, relevant_ids, port)):
            port.charge(1)
            relevant_evaluations.append(entity)
        if not _intersects(_field(data, 'target_refs', port).items, observed_targets, port):
            continue
        if _field(data, 'evaluation_kind', port) not in ('empirical_review', 'human_review'):
            continue
        port.charge(2)
        observations.append(entity)
        basis_entities.append(entity)
        _p._premise(prepared, entity, local, premises, port)
        for identifier in _field(data, 'result_refs', port).items:
            result = _analysis_lookup(prepared, identifier, port)
            port.charge(2)
            observation_results.append(result)
            basis_entities.append(result)
    port.charge(len(channels) + len(observations) + len(declared) +
                len(inquiry_targets) + len(relevant_evaluations))
    capacity_subjects = _ids(_o._unique_entities(prepared, channels + observations +
        list(declared) + list(inquiry_targets) + relevant_evaluations, port), port)
    for entity in prepared.entities:
        port.charge(1)
        if (entity.collection != 'assertions' or
                _field(entity.node.fields, 'assertion_kind', port) != 'assessment'):
            continue
        data = _field(entity.node.fields, 'data', port)
        if (_field(data, 'assessment_kind', port) != 'capacity' or
                not _intersects(_field(data, 'subject_refs', port).items, capacity_subjects, port)):
            continue
        scope = _field(entity.node.fields, 'scope', port)
        claims = _field(scope, 'claim_refs', port).items
        capacity_context = local if claims else _p._context(local, port, claims=(), view='correction_outcomes')
        if not _analysis_scope(entity, capacity_context, port, subjects=False, relation_types=False):
            continue
        port.charge(2)
        capacities.append(entity)
        basis_entities.append(entity)
        _p._premise(prepared, entity, capacity_context, premises, port)
    for premise in premises:
        for qualification in (premise.basis, premise.conflict):
            for address in qualification.support_refs:
                port.charge(1)
                basis_entities.append(_analysis_lookup(prepared, address.record_id, port))
        for code in _p._codes(premise, port):
            port.charge(1)
            problems.append((code, premise.source))
    for change in change_facts:
        for address in change.identity.support_refs:
            port.charge(1)
            basis_entities.append(_analysis_lookup(prepared, address.record_id, port))
    basis_entities = _o._unique_entities(prepared, basis_entities, port)
    source_refs = _o._tuple(sources, port)
    port.charge(len(basis_entities) + len(source_refs) + 3)
    total = len(basis_entities) + len(source_refs)
    reservation = ledger.reserve(witnesses=1, members=total)
    for entity in basis_entities:
        _analysis_address(entity, port)
    port.charge(10)
    witness = _OutcomeWitness(prepared, context, port, basis_entities, source_refs, total)
    ledger.retain(reservation)
    port.charge(24)
    facts = _OutcomeFacts(prepared, context, port, inquiry, cases,
        _o._unique_entities(prepared, handling, port), _o._unique_entities(prepared, changes, port),
        _o._tuple(change_facts, port), _o._tuple(target_changes, port), selected,
        selected_targets is not None, _o._unique_entities(prepared, observations, port),
        _o._unique_entities(prepared, observation_results, port),
        _o._unique_entities(prepared, capacities, port), _o._tuple(premises, port),
        basis_entities, _o._tuple(problems, port), (witness,))
    port.check()
    return facts


def _check_facts(facts, port):
    _analysis_port(port)
    port.charge(3)
    _require(type(facts) is _OutcomeFacts and facts.job_port is port)


def _scope(facts, port):
    context = facts.context
    claims, anchor = [], []
    for identifier in context.claim_refs:
        port.charge(1)
        claims.append(_profile_ref(_analysis_lookup(facts.prepared, identifier, port), port))
    for part in context.operation_anchor:
        port.charge(1)
        if type(part) is _SourceAddress:
            part = _o._source_ref(part, port)
        elif type(part) is str:
            _analysis_text(part, port)
        anchor.append(part)
    port.charge(1)
    anchor.append('selected_declared_targets' if facts.explicit_target_selection else 'all_declared_targets')
    if facts.explicit_target_selection:
        for target in facts.selected_targets:
            port.charge(1)
            anchor.append(_profile_ref(target, port))
    subjects = _refs(facts.cases, port)
    for items in (claims, subjects):
        for ref in items:
            _charge_input_ref(ref, port, repeats=len(items) + 3)
    if context.requested_time is not None:
        _charge_frozen(context.requested_time.fields, port)
    port.charge(len(claims) + len(subjects) + len(anchor) + 20)
    scope = _r._Scope(_profile_ref(facts.inquiry, port), _o._tuple(claims, port), subjects,
        None, 'correction_outcomes', context.temporal_basis, context.requested_time, (),
        ('Exact relevant selected submissions and their case_ref-linked events. Whole-case counts '
         'remain separate from an explicitly selected declared-target display subset.',), _o._tuple(anchor, port))
    _charge_scope(scope, port)
    return scope


def _frozen(pairs, port):
    for name, value in pairs:
        _analysis_text(name, port)
        _charge_frozen(value, port)
    return _freeze_object(pairs, port)


def _record(entity, facts, port, extra=()):
    native = _p._native_fields(facts.prepared, entity, port)
    port.charge(len(extra) + 2)
    fields = [('native_record', native)]
    fields.extend(extra)
    value = _frozen(fields, port)
    _charge_input_ref(_profile_ref(entity, port), port)
    port.charge(7)
    return _r._Disclosure(_profile_ref(entity, port), value,
        ('Original native record, references, time, attribution and gaps are retained. '
         'A reported outcome or capacity is not a toolkit success or adequacy verdict.',))


def _disclosures(facts, field, port):
    records = []
    if field == _FIELDS[5]:
        port.charge(len(facts.cases) + len(facts.handling) + len(facts.changes) +
                    len(facts.observations) + len(facts.observation_results))
        entities = _o._unique_entities(facts.prepared,
            facts.cases + facts.handling + facts.changes + facts.observations + facts.observation_results, port)
        for entity in entities:
            extra = []
            for change in facts.change_facts:
                port.charge(1)
                if change.source is entity:
                    port.charge(3)
                    extra.extend((('documentary_state', change.documentary_state),
                        ('explicit_removal', change.removal), ('reason_codes', _Array(change.reason_codes))))
            port.charge(1)
            records.append(_record(entity, facts, port, extra))
    elif field == _FIELDS[7]:
        for entity in facts.capacities:
            extra = []
            for premise in facts.premises:
                port.charge(1)
                if premise.source is entity:
                    port.charge(2)
                    extra.extend((('documentary_state', _p._aggregate(
                        (premise.basis.state, premise.conflict.state), port)),
                        ('reason_codes', _Array(_p._codes(premise, port)))))
            port.charge(1)
            records.append(_record(entity, facts, port, extra))
    else:
        targets = []
        for item in facts.target_changes:
            port.charge(1)
            targets.append(item.before)
        for target in _o._unique_entities(facts.prepared, targets, port):
            rows = []
            for item in facts.target_changes:
                port.charge(1)
                if item.before is not target:
                    continue
                pairs = (('case_ref', item.case.identifier), ('declared', item.declared),
                    ('selected', item.selected), ('change_event_refs', _Array(_ids(item.events, port))),
                    ('qualified_change_event_refs', _Array(_ids(item.qualified_events, port))),
                    ('documentary_state', item.documentary_state),
                    ('requested_effect_state', 'available' if item.qualified_events else 'unavailable'),
                    ('reason_codes', _Array(item.reason_codes)))
                port.charge(1)
                rows.append(_frozen(pairs, port))
            port.charge(len(rows) + 3)
            records.append(_record(target, facts, port, (('case_rows', _Array(_o._tuple(rows, port))),)))
    port.charge(len(records) + 3)
    return _r._RecordDisclosures(_o._tuple(records, port))


def _required_premises(facts, field, port):
    """Only each leaf's actual source prerequisites, with no case-level veto."""
    if field == _FIELDS[0]:
        sources = facts.cases
    elif field == _FIELDS[1]:
        sources = facts.handling
    elif field in (_FIELDS[2], _FIELDS[3], _FIELDS[4], _FIELDS[6]):
        sources = facts.changes
    elif field == _FIELDS[7]:
        sources = facts.capacities
    else:
        port.charge(len(facts.cases) + len(facts.handling) + len(facts.changes) + len(facts.observations))
        sources = facts.cases + facts.handling + facts.changes + facts.observations
    selected = []
    for premise in facts.premises:
        for source in sources:
            port.charge(1)
            if premise.source is source:
                port.charge(1)
                selected.append(premise)
                break
    return _o._tuple(selected, port)


def _reasons(facts, scope, ref, field, port):
    reasons = []
    relevant = []
    for premise in _required_premises(facts, field, port):
        port.charge(1)
        relevant.append(premise.source)
    if field in (_FIELDS[3], _FIELDS[4], _FIELDS[5], _FIELDS[6]):
        for target in facts.target_changes:
            port.charge(1)
            relevant.append(target.before)
    relevant_ids = _ids(_o._unique_entities(facts.prepared, relevant, port), port)
    for code in _r.REASON_CODES:
        entities = []
        for incoming, entity in facts.problems:
            port.charge(1)
            if incoming != code or not _analysis_contains(relevant_ids, entity.identifier, port):
                continue
            port.charge(1)
            entities.append(entity)
        if not entities:
            continue
        inputs = _refs(_o._unique_entities(facts.prepared, entities, port), port)
        for source in inputs:
            _charge_input_ref(source, port, repeats=len(inputs) + 3)
        for unused in range(3):
            _charge_scope(scope, port)
        port.charge(len(inputs) + 18)
        reasons.append(_r._Reason(code, scope, (ref,), inputs,
            'This exact supplied case, target or assessment retains its evidence limit. '
            'Missing linked-change evidence does not assert a failed correction or universal non-change.',
            'conflict' if code == 'premise_disputed' else 'evidence_gap'))
    return _o._tuple(reasons, port)


def _checks(facts, ref, field, port):
    states = []
    required_premises = _required_premises(facts, field, port)
    for key in ('PC05', 'PC08', 'PC09', 'PC10', 'PC21'):
        values, inputs = [], []
        if key in ('PC05', 'PC09', 'PC10'):
            for premise in required_premises:
                port.charge(1)
                value = (premise.basis.state if key == 'PC05' else premise.conflict.state if key == 'PC09'
                    else premise.time.state if premise.time is not None else 'not_applicable')
                port.charge(2)
                values.append(value)
                inputs.append(premise.source)
            if key == 'PC10' and field in (_FIELDS[2], _FIELDS[3], _FIELDS[4], _FIELDS[5], _FIELDS[6]):
                for change in facts.change_facts:
                    port.charge(2)
                    values.append(change.time_state)
                    inputs.append(change.source)
        elif key == 'PC08' and field in (_FIELDS[3], _FIELDS[4], _FIELDS[6]):
            for change in facts.change_facts:
                port.charge(2)
                values.append(change.identity.state)
                inputs.append(change.source)
        elif key == 'PC21' and field in (_FIELDS[3], _FIELDS[4], _FIELDS[6]):
            for target in facts.target_changes:
                port.charge(2)
                values.append(target.documentary_state)
                inputs.append(target.before)
        port.charge(1)
        states.append((key, _p._aggregate(values, port), _o._unique_entities(facts.prepared, inputs, port)))
    checks = []
    for key in ('PC01', 'PC02', 'PC03', 'PC04', 'PC05', 'PC08', 'PC09', 'PC10', 'PC21'):
        if key == 'PC02':
            port.charge(1)
            checks.append(_scope_check(_ScopeCheckFact(ref, ref.scope), port))
            continue
        state, inputs = ('not_applicable' if key == 'PC04' else 'met'), _refs(facts.cases, port)
        if key == 'PC03':
            selection = [_profile_ref(facts.inquiry, port, selector) for selector in
                         ('target_claim_refs', 'target_object_refs', 'seed_artifact_refs', 'seed_evidence_refs')]
            port.charge(len(facts.cases) + 5)
            for case in facts.cases:
                selection.append(_profile_ref(case, port, 'data.target_refs'))
            inputs = _o._tuple(selection, port)
        for name, value, entities in states:
            port.charge(1)
            if key == name:
                state, inputs = value, _refs(entities, port)
        for source in inputs:
            _charge_input_ref(source, port, repeats=len(inputs) + 3)
        _charge_link(ref, port)
        port.charge(len(inputs) + 14)
        note = ('This owner uses admitted native case_ref/before/after identities without relying '
                'on a RelationAssertion as a current affirmative premise.' if key == 'PC04' else
                'Executed case relevance and exact case_ref enumeration, including the explicitly '
                'empty finite inventory. PC21 concerns documentary endpoints/linkage only; '
                'no authority or substantive-success inference.')
        _analysis_text(note, port)
        checks.append(_r._PrerequisiteCheck(key, ref, state, inputs, (), note))
    return checks


def _members(facts, field, port):
    if field == _FIELDS[0]:
        return 'correction_case', _refs(facts.cases, port)
    if field == _FIELDS[1]:
        return 'handling_event', _refs(facts.handling, port)
    if field == _FIELDS[2]:
        return 'correction_change_record', _refs(facts.changes, port)
    if field == _FIELDS[3]:
        members = []
        for target in facts.target_changes:
            port.charge(1)
            if not target.qualified_events:
                continue
            case, before = _profile_ref(target.case, port), _profile_ref(target.before, port)
            _charge_input_ref(case, port)
            _charge_input_ref(before, port)
            port.charge(5)
            members.append(_r._CaseTarget(case, before))
        return 'case_target', _o._tuple(members, port)
    if field == _FIELDS[4]:
        cases = []
        for target in facts.target_changes:
            port.charge(1)
            if target.qualified_events:
                port.charge(1)
                cases.append(target.case)
        return 'correction_case', _refs(_o._unique_entities(facts.prepared, cases, port), port)
    if field == _FIELDS[7]:
        return 'record', _refs(facts.capacities, port)
    return 'record', _refs(facts.cases, port)


def _correction_outcome_results(facts, port):
    _check_facts(facts, port)
    scope = _scope(facts, port)
    basis = []
    for entity in facts.basis_entities:
        source = _profile_ref(entity, port)
        _charge_input_ref(source, port)
        port.charge(3)
        basis.append(_r._BasisRef(source))
    basis = _o._tuple(basis, port)
    _charge_scope(scope, port)
    port.charge(8)
    witnesses = (_r._WitnessRef(scope, 'member_set', ('correction_case_selection',)),)
    outputs = []
    for field in _FIELDS:
        _check_facts(facts, port)
        _charge_scope(scope, port)
        port.charge(180)
        ref = _r._ResultRef('SIT-M012', field, scope)
        unit, members = _members(facts, field, port)
        for member in members:
            for unused in range(len(members) + 3):
                _charge_link(member, port)
        for item in basis:
            _charge_link(item, port)
        port.charge(len(members) * len(members) + len(basis) + 16)
        population = _r._Population(scope, unit, members,
            'Exact whole-case ' + field + '; finite supplied membership under Definitions 20.2/27.2. '
            'A downstream display subset neither replaces this unit nor changes its count.',
            (), basis, 'enumerated_for_scope', ('No outside-world or all-downstream completeness.',))
        if field in _FIELDS[:5]:
            _charge_link(population, port)
            port.charge(5)
            value, kind = _r._Count(len(members), population), 'count'
        else:
            value, kind = _disclosures(facts, field, port), 'record_disclosures'
        reasons = _reasons(facts, scope, ref, field, port)
        checks = _checks(facts, ref, field, port)
        # Pair membership belongs to the population completion. The premise
        # component instead records the actual visited case/before inputs.
        premise_entities = []
        for member in members:
            port.charge(1)
            inputs = (member.case_ref, member.before_ref) if type(member) is _r._CaseTarget else (member,)
            for source in inputs:
                port.charge(1)
                premise_entities.append(_analysis_lookup(facts.prepared, source.identifier, port))
        premise_refs = _refs(_o._unique_entities(facts.prepared, premise_entities, port), port)
        components = []
        for name, links in (('premises', premise_refs), ('conflicts', reasons), ('value', (ref,)),
                            ('basis', basis), ('reasons', reasons), ('witnesses', witnesses)):
            for link in links:
                for unused in range(3):
                    _charge_link(link, port)
            port.charge(len(links) * len(links) + 10)
            components.append(_ComponentCompletion(name, links, links))
        for unused in range(3):
            _charge_link(population, port)
        port.charge(24)
        complete = _CompletionRecord(ref, (population,), (_PopulationCompletion(population, members),),
            _o._tuple(components, port))
        checks.append(_completion_check(complete, port))
        for unused in range(2):
            _charge_link(ref, port)
            _charge_link(population, port)
            for links in (checks, basis, reasons, witnesses):
                for link in links:
                    _charge_link(link, port)
        port.charge(len(checks) + len(basis) + len(reasons) + 30)
        outputs.append(_r._Result(ref, (population,), 'completed', 'available',
            'inventory' if field in _FIELDS[:3] else 'qualification_check' if field in _FIELDS[3:5]
            else 'attributed_record', kind, value, _o._tuple(checks, port), basis, witnesses, reasons, _LIMIT))
    port.check()
    return _o._tuple(outputs, port)


def _correction_outcomes(prepared, context, ledger, port, *, selected_targets=None):
    facts = _correction_outcome_facts(prepared, context, ledger, port, selected_targets=selected_targets)
    results = _correction_outcome_results(facts, port)
    port.charge(4)
    profile = _OutcomeProfile(facts, results, facts.witnesses)
    port.check()
    return profile
