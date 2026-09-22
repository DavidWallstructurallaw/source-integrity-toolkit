# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: HUMAN_REVIEW_RECORDS. Paid M013 attributed process and contribution facts.

Definitions 25.3: actual supplied process comparisons use the original M003
owner in this job. A recorded human role/contribution, an assessed procedure,
and institutional execution remain distinct. No public orchestration.
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
    _analysis_port, _analysis_start, _analysis_lookup, _analysis_contains,
    _analysis_subset, _analysis_text, _analysis_address, _analysis_codes,
    _analysis_scope, _qualify_basis, _qualify_conflicts, _qualify_identity,
    _profile_ref,
)
from .origins import _tuple, _unique_entities, _source_ref
from . import process_comparison as _comparison

_FIELDS = ('corrective_independence_disclosures', 'human_contribution_disclosures')
_DEPENDENCIES = ('depends_on', 'model_derived_from', 'trained_on', 'generated_by', 'owned_by')
_LIMIT = ('Attributed supplied review and exact process assessment only. A human title, employer, '
          'endpoint or recorded contribution establishes neither independence nor renewable human judgment. '
          'A qualified procedure does not establish institutional execution. Unexamined dimensions and '
          'protected or unresolved dependencies remain unestablished; formal checks and execution retain '
          'their own constraint kinds. No total independent-human capacity or judgment score follows.')


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Review:
    evaluation: object
    human_refs: tuple
    role_refs: tuple
    contribution_status: str
    basis: object
    conflict: object
    identity: object
    reason_codes: tuple


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _ReviewWitness:
    prepared: object
    context: object
    job_port: object
    members: tuple
    examined_assessments: tuple
    source_refs: tuple
    member_count: int


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _HumanReviewFacts:
    prepared: object
    context: object
    job_port: object
    inquiry: object
    subjects: tuple
    reviews: tuple
    comparisons: tuple
    dependencies: tuple
    disclosure_entities: tuple
    basis_entities: tuple
    problems: tuple
    witnesses: tuple


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _HumanReviewProfile:
    facts: _HumanReviewFacts
    results: tuple
    witnesses: tuple


def _refs(entities, port):
    rows = []
    for entity in entities:
        port.charge(1)
        rows.append(_profile_ref(entity, port))
    return _tuple(rows, port)


def _selected(prepared, inquiry, context, port):
    """Use requested actual subjects, or explicit Inquiry Evaluation targets."""
    if context.subject_refs:
        identifiers = context.subject_refs
    else:
        identifiers = _field(inquiry.node.fields, 'target_object_refs', port).items
    selected = []
    for identifier in identifiers:
        entity = _analysis_lookup(prepared, identifier, port)
        port.charge(2)
        if context.subject_refs:
            _require(entity.kind in ('evaluation', 'actor', 'model', 'unresolved_reference'))
        elif entity.kind != 'evaluation':
            continue
        selected.append(entity)
    return _unique_entities(prepared, selected, port)


def _related_scope(entity, context, port):
    """Native metadata can be Inquiry-scoped; no other Claim is imported."""
    scope = _field(entity.node.fields, 'scope', port)
    claims = _field(scope, 'claim_refs', port).items
    return (_analysis_contains(_field(scope, 'inquiry_refs', port).items, context.inquiry_ref, port)
            and (not claims or bool(context.claim_refs) and
                 _analysis_subset(context.claim_refs, claims, port)))


def _human_review_facts(prepared, context, ledger, port):
    inquiry = _analysis_start(prepared, context, port)
    _comparison._ledger(ledger, port)
    port.charge(4)
    _require(bool(context.claim_refs) and context.dependency_dimension is not None)
    targets = _field(inquiry.node.fields, 'target_claim_refs', port).items
    for claim in context.claim_refs:
        _require(_analysis_contains(targets, claim, port))
    dimensions = _field(inquiry.node.fields, 'dependency_dimensions', port).items
    _require(_analysis_contains(dimensions, context.dependency_dimension, port))
    expected_view = 'organizational' if context.dependency_dimension == 'organizational_control' else 'model_evaluation'
    _require(context.graph_view is None or context.graph_view == expected_view)
    subjects = _selected(prepared, inquiry, context, port)
    local = _comparison._context(context, port, subjects=(), predicates=(), view=None)
    port.charge(12)
    reviews, comparisons, dependencies, disclosures, basis_entities = [], [], [], [], []
    associated, problems, examined, source_refs = [], [], [], []
    port.charge(2)
    basis_entities.append(inquiry)
    source_refs.append(_analysis_address(inquiry, port, 'target_object_refs'))
    for entity in subjects:
        port.charge(3)
        associated.append(entity.identifier)
        disclosures.append(entity)
        basis_entities.append(entity)
        source_refs.append(_analysis_address(entity, port))
        if entity.kind != 'evaluation':
            continue
        data = _field(entity.node.fields, 'data', port)
        humans, roles, codes = [], [], []
        for role in _field(data, 'role_bindings', port).items:
            target = _analysis_lookup(prepared, _field(role, 'object_ref', port), port)
            port.charge(4)
            roles.append(target)
            disclosures.append(target)
            basis_entities.append(target)
            source_refs.append(_analysis_address(target, port))
            if target.kind in ('actor', 'model', 'unresolved_reference'):
                associated.append(target.identifier)
            name = _field(role, 'role', port)
            if name == 'human_reviewer':
                port.charge(1)
                humans.append(target)
            for identifier in _field(role, 'evidence_ref_ids', port).items:
                support = _analysis_lookup(prepared, identifier, port)
                port.charge(2)
                basis_entities.append(support)
                disclosures.append(support)
        roles = _unique_entities(prepared, roles, port)
        humans = _unique_entities(prepared, humans, port)
        basis = _qualify_basis(prepared, entity.identifier, local, port)
        conflict = _qualify_conflicts(prepared, entity.identifier, local, port)
        identifiers = []
        for target in roles:
            port.charge(1)
            identifiers.append(target.identifier)
        identity = _qualify_identity(prepared, _tuple(identifiers, port), local, port)
        for qualification in (basis, conflict, identity):
            port.charge(len(qualification.reason_codes) + len(qualification.support_refs))
            codes.extend(qualification.reason_codes)
            for address in qualification.support_refs:
                target = _analysis_lookup(prepared, address.record_id, port)
                port.charge(2)
                basis_entities.append(target)
                disclosures.append(target)
        kind = _field(data, 'evaluation_kind', port)
        contribution = _field(data, 'review_contribution', port)
        if contribution is not None:
            _analysis_text(contribution, port)
        if kind in ('formal_check', 'execution'):
            status = 'distinct_constraint'
        elif not humans:
            status = 'no_human_role'
            port.charge(1)
            codes.append('roles_incomplete')
        elif not contribution:
            status = 'missing_contribution'
            port.charge(1)
            codes.append('documentary_basis_incomplete')
        else:
            status = 'recorded_human_contribution'
        if context.temporal_basis != 'snapshot_structural':
            port.charge(1)
            codes.append('time_applicability_unknown')
        for key in ('target_refs', 'result_refs'):
            for identifier in _field(data, key, port).items:
                port.charge(1)
                basis_entities.append(_analysis_lookup(prepared, identifier, port))
        codes = _analysis_codes(codes, port)
        port.charge(10)
        reviews.append(_Review(entity, humans, roles, status, basis, conflict, identity, codes))
        for code in codes:
            port.charge(1)
            problems.append((code, entity))
    # Discovery examines actual finite supplied assessments. Matching one
    # selected process does not trim, union or invent its comparison members.
    for candidate in prepared.entities:
        port.charge(2)
        if candidate.collection != 'assertions':
            continue
        obj = candidate.node.fields
        data = _field(obj, 'data', port)
        if _field(obj, 'assertion_kind', port) == 'assessment':
            if _field(data, 'assessment_kind', port) != 'independence':
                continue
            port.charge(1)
            examined.append(candidate)
            subjects_in_assessment = _field(data, 'subject_refs', port).items
            relevant = False
            for identifier in associated:
                port.charge(1)
                if _analysis_contains(subjects_in_assessment, identifier, port):
                    relevant = True
            if not relevant or not _related_scope(candidate, context, port):
                continue
            port.charge(2)
            disclosures.append(candidate)
            basis_entities.append(candidate)
            # Other native dimensions remain disclosed, never silently
            # qualified through the selected dimension's assessment.
            if not _analysis_scope(candidate, local, port, subjects=False, relation_types=False):
                continue
            profile = _comparison._comparison_profile(prepared, local, candidate.identifier, ledger, port)
            port.charge(1)
            comparisons.append(profile)
            for code, address in profile.facts.problems:
                port.charge(1)
                problems.append((code, _analysis_lookup(prepared, address.record_id, port)))
            for entity in profile.facts.disclosures:
                port.charge(2)
                disclosures.append(entity)
                basis_entities.append(entity)
        else:
            if _field(data, 'predicate', port) not in _DEPENDENCIES:
                continue
            relevant = (_analysis_contains(associated, _field(data, 'from_ref', port), port)
                        or _analysis_contains(associated, _field(data, 'to_ref', port), port))
            if relevant and _related_scope(candidate, context, port):
                port.charge(3)
                dependencies.append(candidate)
                disclosures.append(candidate)
                basis_entities.append(candidate)
                for key in ('from_ref', 'to_ref'):
                    target = _analysis_lookup(prepared, _field(data, key, port), port)
                    port.charge(2)
                    disclosures.append(target)
                    basis_entities.append(target)
    if not comparisons:
        port.charge(1)
        problems.append(('missing_comparison_assessment', inquiry))
    # Reservation represents the actual selected records, role positions and
    # assessment scan. Original M003 witnesses retain their own payloads/quota.
    members = _unique_entities(prepared, subjects, port)
    examined = _unique_entities(prepared, examined, port)
    port.charge(len(source_refs) + 3)
    total = len(members) + len(examined) + len(source_refs)
    reservation = ledger.reserve(witnesses=1, members=total)
    port.charge(len(members) + len(examined) + 1)
    for entity in members + examined:
        _analysis_address(entity, port)
    port.charge(10)
    witness = _ReviewWitness(prepared, context, port, members, examined,
                            _tuple(source_refs, port), total)
    ledger.retain(reservation)
    witnesses = [witness]
    for profile in comparisons:
        port.charge(len(profile.witnesses))
        witnesses.extend(profile.witnesses)
    port.charge(16)
    facts = _HumanReviewFacts(prepared, context, port, inquiry, subjects,
        _tuple(reviews, port), _tuple(comparisons, port), _unique_entities(prepared, dependencies, port),
        _unique_entities(prepared, disclosures, port), _unique_entities(prepared, basis_entities, port),
        _tuple(problems, port), _tuple(witnesses, port))
    port.check()
    return facts


def _check_facts(facts, port):
    _analysis_port(port)
    port.charge(4)
    _require(type(facts) is _HumanReviewFacts and facts.job_port is port)
    for profile in facts.comparisons:
        port.charge(1)
        _comparison._check_facts(profile.facts, port)


def _scope(facts, port):
    context = facts.context
    claims, anchor = [], ['SIT-M013']
    for identifier in context.claim_refs:
        port.charge(1)
        claims.append(_profile_ref(_analysis_lookup(facts.prepared, identifier, port), port))
    for part in context.operation_anchor:
        port.charge(1)
        if type(part) is _SourceAddress:
            part = _source_ref(part, port)
        elif type(part) is str:
            _analysis_text(part, port)
        anchor.append(part)
    targets = _refs(facts.subjects, port)
    for rows in (claims, targets):
        port.charge(len(rows) * len(rows) + len(rows) + 1)
        for ref in rows:
            _charge_input_ref(ref, port, repeats=len(rows) + 3)
    if context.requested_time is not None:
        _charge_frozen(context.requested_time.fields, port)
    port.charge(len(anchor) + 18)
    result = _r._Scope(_profile_ref(facts.inquiry, port), _tuple(claims, port), targets,
        context.dependency_dimension, context.graph_view, context.temporal_basis,
        context.requested_time, (), ('Selected actual review/process subjects only; '
        'the comparison owner retains each complete native comparison set and scope.',), _tuple(anchor, port))
    _charge_scope(result, port)
    return result


def _record(entity, facts, port, *, review=None):
    native = _comparison._native_fields(facts.prepared, entity, port)
    port.charge(len(native.items) + 2)
    fields = list(native.items)
    if review is not None:
        state = _comparison._aggregate((review.basis.state, review.conflict.state), port)
        port.charge(6)
        fields.extend((('contribution_status', review.contribution_status),
                       ('documentary_state', state), ('identity_state', review.identity.state),
                       ('reason_codes', _Array(review.reason_codes))))
    for name, value in fields:
        _analysis_text(name, port)
        _charge_frozen(value, port)
    value = _freeze_object(fields, port)
    port.charge(6)
    return _r._Disclosure(_profile_ref(entity, port), value,
        ('Original supplied record fields and attribution are retained. Recorded contribution is a '
         'source description, not semantic authentication, independent human judgment or institutional execution.',))


def _disclosures(facts, field, port):
    records, seen = [], []
    # Reuse the original M003 assertion disclosure so that actual executed
    # process-state and native conclusion/limits cannot diverge in a wrapper.
    if field == _FIELDS[0]:
        # Every actually assessed primary row wins over an incidental raw
        # support disclosure of that same assertion from another comparison.
        for primary in (True, False):
            for profile in facts.comparisons:
                for result in profile.results:
                    port.charge(1)
                    if result.ref.field_key != 'independence_assessment_disclosures':
                        continue
                    for row in result.value.records:
                        port.charge(2)
                        _analysis_text(row.source.identifier, port)
                        _analysis_text(profile.facts.assessment.identifier, port)
                        is_primary = row.source.identifier == profile.facts.assessment.identifier
                        if is_primary != primary:
                            continue
                        if not _analysis_contains(seen, row.source.identifier, port):
                            records.append(row)
                            seen.append(row.source.identifier)
    for entity in facts.disclosure_entities:
        port.charge(1)
        if _analysis_contains(seen, entity.identifier, port):
            continue
        review = None
        for candidate in facts.reviews:
            port.charge(1)
            if candidate.evaluation is entity:
                review = candidate
                break
        # A full comparison may include an unselected Evaluation. Preserve
        # that native process in the corrective leaf without importing its
        # human contribution into this independently selected review scope.
        if field == _FIELDS[1] and entity.kind == 'evaluation' and review is None:
            continue
        # Human disclosures retain role/dependency limits; unrelated native
        # comparison records belong to the corrective-process disclosure.
        if field == _FIELDS[1] and entity.collection == 'assertions':
            port.charge(len(facts.dependencies) + 1)
            if entity not in facts.dependencies:
                continue
        port.charge(2)
        records.append(_record(entity, facts, port, review=review))
        seen.append(entity.identifier)
    port.charge(len(records) + 3)
    return _r._RecordDisclosures(_tuple(records, port))


def _reasons(facts, scope, ref, field, port):
    result = []
    for code in _r.REASON_CODES:
        entities = []
        if field == _FIELDS[0]:
            source_rows = facts.problems
        else:
            source_rows = []
            for review in facts.reviews:
                for reason in review.reason_codes:
                    port.charge(1)
                    source_rows.append((reason, review.evaluation))
        for incoming, entity in source_rows:
            port.charge(1)
            if incoming == code:
                port.charge(1)
                entities.append(entity)
        if not entities:
            continue
        inputs = _refs(_unique_entities(facts.prepared, entities, port), port)
        for source in inputs:
            _charge_input_ref(source, port, repeats=len(inputs) + 3)
        for unused in range(3):
            _charge_scope(scope, port)
        port.charge(18)
        result.append(_r._Reason(code, scope, (ref,), inputs,
            'The supplied review/process record retains this exact qualification limit. '
            'Visible contribution does not resolve missing process evidence or dependencies.',
            'conflict' if code == 'premise_disputed' else 'evidence_gap'))
    return _tuple(result, port)


def _checks(facts, ref, field, reasons, port):
    states = []
    for key in ('PC05', 'PC08', 'PC09', 'PC10', 'PC11'):
        values, entities = [], []
        for review in facts.reviews:
            port.charge(2)
            if key == 'PC05':
                values.append(review.basis.state)
            elif key == 'PC08':
                values.append(review.identity.state)
            elif key == 'PC09':
                values.append(review.conflict.state)
            elif key == 'PC10':
                values.append('met' if facts.context.temporal_basis == 'snapshot_structural' else 'unknown')
            else:
                continue
            entities.append(review.evaluation)
        if field == _FIELDS[0]:
            for profile in facts.comparisons:
                for check in profile.facts.process_checks:
                    port.charge(1)
                    if check[0] == key:
                        values.append(check[1])
                        entities.append(profile.facts.assessment)
        if key == 'PC11':
            state = ('not_applicable' if field == _FIELDS[1] else
                     _comparison._aggregate(values, port, empty='unknown'))
        else:
            state = _comparison._aggregate(values, port)
        port.charge(1)
        states.append((key, state, _unique_entities(facts.prepared, entities, port)))
    port.charge(6)
    roles = 'met' if facts.reviews else 'not_applicable'
    for review in facts.reviews:
        port.charge(1)
        if not review.role_refs or review.contribution_status == 'no_human_role':
            roles = 'unknown'
        for target in review.role_refs:
            port.charge(1)
            if target.kind == 'unresolved_reference':
                roles = 'unknown'
    states.extend((('PC14', roles, facts.subjects), ('PC22', 'met', facts.subjects)))
    checks = []
    for check_id in ('PC01', 'PC02', 'PC05', 'PC08', 'PC09', 'PC10', 'PC11', 'PC14', 'PC22'):
        if check_id == 'PC02':
            checks.append(_scope_check(_ScopeCheckFact(ref, ref.scope), port))
            continue
        state, inputs = 'met', ()
        for key, value, entities in states:
            port.charge(1)
            if key == check_id:
                state, inputs = value, _refs(entities, port)
        for source in inputs:
            _charge_input_ref(source, port, repeats=len(inputs) + 3)
        _charge_link(ref, port)
        port.charge(len(inputs) + 14)
        checks.append(_r._PrerequisiteCheck(check_id, ref, state, inputs, (),
            'Executed review/process prerequisite. PC22 records disclosure of native contribution, '
            'identity and dependency limits, including the absence of an applicable comparison.'))
    return checks


def _human_review_results(facts, port):
    _check_facts(facts, port)
    scope = _scope(facts, port)
    members = _refs(facts.subjects, port)
    basis = []
    for entity in facts.basis_entities:
        source = _profile_ref(entity, port)
        _charge_input_ref(source, port)
        port.charge(3)
        basis.append(_r._BasisRef(source))
    basis = _tuple(basis, port)
    _charge_scope(scope, port)
    port.charge(8)
    witness = _r._WitnessRef(scope, 'member_set', ('human_review_selection',))
    linked_witnesses = [witness]
    for profile in facts.comparisons:
        assessment = _profile_ref(profile.facts.assessment, port)
        for original in _comparison._witness_refs(profile.facts, scope, port):
            for part in original.anchor:
                port.charge(1)
                if type(part) is _r._InputRef:
                    _charge_input_ref(part, port, repeats=2)
                elif type(part) is str:
                    _analysis_text(part, port)
            _charge_input_ref(assessment, port, repeats=2)
            _charge_scope(scope, port)
            port.charge(len(original.anchor) + 10)
            linked_witnesses.append(_r._WitnessRef(scope, original.kind,
                ('corrective_comparison', assessment) + original.anchor))
    witnesses = _tuple(linked_witnesses, port)
    outputs = []
    for field in _FIELDS:
        _check_facts(facts, port)
        _charge_scope(scope, port)
        port.charge(180)
        ref = _r._ResultRef('SIT-M013', field, scope)
        for member in members:
            _charge_input_ref(member, port, repeats=len(members) + 3)
        for item in basis:
            _charge_link(item, port)
        port.charge(len(members) * len(members) + len(basis) + 16)
        population = _r._Population(scope, 'record', members,
            'Exactly the requested actual subjects, or the explicit Evaluation targets of this Inquiry; '
            'no all-record cohort or hidden human-judgment population.', (), basis, 'enumerated_for_scope',
            ('This finite supplied selection confers no outside-world completeness.',))
        value = _disclosures(facts, field, port)
        reasons = _reasons(facts, scope, ref, field, port)
        checks = _checks(facts, ref, field, reasons, port)
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
        complete = _CompletionRecord(ref, (population,), (_PopulationCompletion(population, members),),
                                     _tuple(components, port))
        checks.append(_completion_check(complete, port))
        for unused in range(2):
            _charge_link(ref, port)
            _charge_link(population, port)
            for links in (checks, basis, reasons, witnesses):
                for link in links:
                    _charge_link(link, port)
        port.charge(len(checks) + len(basis) + len(reasons) + 30)
        outputs.append(_r._Result(ref, (population,), 'completed', 'available', 'attributed_record',
            'record_disclosures', value, _tuple(checks, port), basis, witnesses, reasons, _LIMIT))
    port.check()
    return _tuple(outputs, port)


def _human_review(prepared, context, ledger, port):
    facts = _human_review_facts(prepared, context, ledger, port)
    results = _human_review_results(facts, port)
    port.charge(4)
    profile = _HumanReviewProfile(facts, results, facts.witnesses)
    port.check()
    return profile
