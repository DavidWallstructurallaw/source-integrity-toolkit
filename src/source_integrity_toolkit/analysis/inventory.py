# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: SOURCE_INVENTORY. Private finite M001 populations and PC03.

Definitions 20.1/21.1: source positions, not the entire dossier, determine
membership. Inquiry-wide artifact unions and unassigned seeds are independent
of the selected Claim; contribution and Claim-artifact populations are not.
Counting supplied records grants no identity, truth or graph qualification.
"""
from dataclasses import dataclass

from ..contracts.bundle import _require, _compare_text
from ..contracts.evidence import _ProviderFact, _SourceAddress
from ..contracts import results as _results
from ..contracts.report import (
    _ScopeCheckFact, _PopulationCompletion, _ComponentCompletion,
    _CompletionRecord, _scope_check, _completion_check,
    _charge_scope, _charge_input_ref, _charge_link,
)
from ..validation.limits import _WitnessLedger
from ..validation.structure import _field
from ..validation.semantics import (
    _analysis_port, _analysis_start, _analysis_lookup, _analysis_ids,
    _analysis_contains, _analysis_text, _analysis_address,
    _analysis_unique_addresses, _profile_ref,
)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _InventoryFacts:
    prepared: object
    context: object
    job_port: object
    inquiry: object
    artifacts: tuple
    unresolved_artifacts: tuple
    unassigned_artifacts: tuple
    seed_evidence: tuple
    claim_artifacts: tuple
    selection_refs: tuple
    pc03: _ProviderFact


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _InventoryWitness:
    ref: _results._WitnessRef
    population: _results._Population
    members: tuple
    member_count: int


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _InventoryProfile:
    facts: _InventoryFacts
    results: tuple
    witnesses: tuple


def _entities(prepared, identifiers, port):
    """Paid ID ordering and deduplication; no locator/label identity rule."""
    port.charge(len(identifiers) + 1)
    pairs = _analysis_ids(tuple(identifiers), port)
    rows = []
    for identifier, unused in pairs:
        port.charge(2)
        rows.append(_analysis_lookup(prepared, identifier, port))
    port.charge(len(rows) + 1)
    return tuple(rows)


def _inventory_facts(prepared, context, port):
    """Examine one exact target Claim and the complete Inquiry seed positions.

    Empty subjects derive E(I,C). Nonempty subjects must name that same entire
    population. The raw snapshot may be reused, but these semantic facts are
    bound to this actual current job, without cross-job completion authority.
    """
    inquiry = _analysis_start(prepared, context, port)
    port.charge(2)
    _require(len(context.claim_refs) == 1)
    claim = context.claim_refs[0]
    targets = _field(inquiry.node.fields, 'target_claim_refs', port).items
    _require(_analysis_contains(targets, claim, port))
    explicit = _field(inquiry.node.fields, 'seed_artifact_refs', port).items
    seed_ids = _field(inquiry.node.fields, 'seed_evidence_refs', port).items
    all_seeds = _entities(prepared, seed_ids, port)
    port.charge(10)
    artifacts, unknown, explicit_resolved, assigned, selected, claim_artifacts = [], [], [], [], [], []
    sources = [_analysis_address(inquiry, port, 'seed_artifact_refs'),
               _analysis_address(inquiry, port, 'seed_evidence_refs')]
    for identifier in explicit:
        port.charge(2)
        entity = _analysis_lookup(prepared, identifier, port)
        _require(entity.kind in ('artifact', 'unresolved_reference'))
        if entity.kind == 'artifact':
            port.charge(2)
            artifacts.append(identifier)
            explicit_resolved.append(identifier)
        else:
            port.charge(1)
            unknown.append(identifier)
    for entity in all_seeds:
        port.charge(2)
        _require(entity.kind == 'evidence_item')
        data = _field(entity.node.fields, 'data', port)
        bound_claim = _field(data, 'claim_ref', port)
        artifact_id = _field(data, 'artifact_ref', port)
        artifact = _analysis_lookup(prepared, artifact_id, port)
        _require(artifact.kind in ('artifact', 'unresolved_reference'))
        port.charge(2)
        sources.append(_analysis_address(entity, port, 'data.claim_ref'))
        sources.append(_analysis_address(entity, port, 'data.artifact_ref'))
        if artifact.kind == 'artifact':
            port.charge(2)
            artifacts.append(artifact_id)
            assigned.append(artifact_id)
        else:
            port.charge(1)
            unknown.append(artifact_id)
        if _compare_text(bound_claim, claim, port) == 0:
            port.charge(1)
            selected.append(entity.identifier)
            if artifact.kind == 'artifact':
                port.charge(1)
                claim_artifacts.append(artifact_id)
    unassigned = []
    for identifier in explicit_resolved:
        port.charge(1)
        if not _analysis_contains(assigned, identifier, port):
            port.charge(1)
            unassigned.append(identifier)
    seed_evidence = _entities(prepared, selected, port)
    if context.subject_refs:
        supplied = _analysis_ids(context.subject_refs, port)
        port.charge(1)
        _require(len(supplied) == len(seed_evidence))
        for pair, entity in zip(supplied, seed_evidence):
            port.charge(2)
            _require(_compare_text(pair[0], entity.identifier, port) == 0)
    port.charge(len(sources) + 1)
    source_refs = _analysis_unique_addresses(tuple(sources), port)
    for source in source_refs:
        for _ in range(3):
            _analysis_text(source.collection, port)
            _analysis_text(source.record_id, port)
            _analysis_text(source.selector, port)
    port.charge(16 + 4 * len(source_refs))
    provider = _ProviderFact('PC03', 'SOURCE_INVENTORY', context, 'met', source_refs, prepared)
    populations = []
    for identifiers in (artifacts, unknown, unassigned, claim_artifacts):
        port.charge(1)
        populations.append(_entities(prepared, identifiers, port))
    port.charge(13)
    answer = _InventoryFacts(prepared, context, port, inquiry,
        populations[0], populations[1], populations[2], seed_evidence,
        populations[3], source_refs, provider)
    port.check()
    return answer


def _check_inventory(facts, port):
    _analysis_port(port)
    port.charge(2)
    _require(type(facts) is _InventoryFacts and facts.job_port is port)


def _inventory_ledger(facts, ledger, port):
    _check_inventory(facts, port)
    port.charge(3)
    _require(type(ledger) is _WitnessLedger)
    try:
        owner = port._owner
        _require(ledger.port._owner is owner and owner._witness_ledger is ledger)
    except AttributeError:
        raise TypeError('invalid_private_representation') from None
    ledger.port.check()


def _inventory_scope(facts, claim_bound, port):
    _check_inventory(facts, port)
    inquiry = _profile_ref(facts.inquiry, port)
    claims = ()
    if claim_bound:
        claim = _analysis_lookup(facts.prepared, facts.context.claim_refs[0], port)
        claims = (_profile_ref(claim, port),)
        _charge_input_ref(claims[0], port, repeats=3)
    # Raw supplied positions do not acquire a dimension or graph qualification.
    # Retaining a requested time does not reconstruct a historical snapshot.
    anchor = []
    for part in facts.context.operation_anchor:
        port.charge(2)
        if type(part) is _SourceAddress:
            entity = _analysis_lookup(facts.prepared, part.record_id, port)
            part = _profile_ref(entity, port, part.selector or None)
        elif type(part) is str:
            _analysis_text(part, port)
        anchor.append(part)
    port.charge(len(anchor) + 18)
    scope = _results._Scope(inquiry, claims, (), None, None,
        facts.context.temporal_basis, facts.context.requested_time, (),
        ('Explicit supplied seed positions only; no dimension, graph eligibility, '
         'historical reconstruction or complete outside-world source inventory is asserted.',), tuple(anchor))
    _charge_scope(scope, port)
    return scope


def _inventory_basis(facts, port):
    refs, basis = [], []
    for source in facts.selection_refs:
        port.charge(2)
        entity = _analysis_lookup(facts.prepared, source.record_id, port)
        ref = _profile_ref(entity, port, source.selector or None)
        _charge_input_ref(ref, port)
        refs.append(ref)
        basis.append(_results._BasisRef(ref))
    port.charge(len(refs) + len(basis) + 2)
    return tuple(refs), tuple(basis)


def _claim_unknowns(facts, port):
    """A Claim-local gap cannot be inferred from another Claim's seed binding."""
    identifiers = []
    for entity in facts.seed_evidence:
        port.charge(2)
        data = _field(entity.node.fields, 'data', port)
        identifier = _field(data, 'artifact_ref', port)
        artifact = _analysis_lookup(facts.prepared, identifier, port)
        if artifact.kind == 'unresolved_reference':
            port.charge(1)
            identifiers.append(identifier)
    return _entities(facts.prepared, identifiers, port)


def _inventory_result(facts, scope, field, entities, unit, selection, source_refs, basis, ledger, port):
    _inventory_ledger(facts, ledger, port)
    refs = []
    for entity in entities:
        port.charge(1)
        refs.append(_profile_ref(entity, port))
    for ref in refs:
        _charge_input_ref(ref, port, repeats=3)
    for link in basis:
        _charge_link(link, port)
    _analysis_text(selection, port)
    port.charge(len(refs) * len(refs) + len(refs) + len(basis) + 16)
    population = _results._Population(scope, unit, tuple(refs), selection, (), basis,
        'enumerated_for_scope', ('Complete finite ID set at these supplied positions; '
        'an empty set is a record inventory zero, never zero actual or independent sources.',))
    # All finite payload members survive retention, including empty inventories.
    port.charge(180)
    result_ref = _results._ResultRef('SIT-M001', field, scope)
    value = _results._Count(len(refs), population)
    _charge_scope(scope, port)
    _analysis_text(field, port)
    port.charge(8)
    witness_ref = _results._WitnessRef(scope, 'member_set', ('SIT-M001', field))
    token = ledger.reserve(witnesses=1, members=len(refs))
    port.charge(6)
    witness = _InventoryWitness(witness_ref, population, population.member_refs, len(refs))
    ledger.retain(token)
    checks = [_scope_check(_ScopeCheckFact(result_ref, scope), port)]
    for ref in source_refs:
        _charge_input_ref(ref, port, repeats=3)
    for _ in range(2):
        _charge_link(result_ref, port)
    port.charge(28 + 3 * len(source_refs))
    checks.append(_results._PrerequisiteCheck('PC01', result_ref, 'met', (), (),
        'The owner received the complete admitted immutable snapshot.'))
    checks.append(_results._PrerequisiteCheck('PC03', result_ref, 'met', source_refs, (),
        'The Inquiry seed positions and exact Claim bindings were completely enumerated.'))
    reasons = []
    if not facts.seed_evidence and field in ('seed_evidence_item_count', 'claim_artifact_record_count'):
        for _ in range(3):
            _charge_scope(scope, port)
        port.charge(20)
        reasons.append(_results._Reason('no_seed_contributions', scope, (result_ref,), (),
            'No explicit resolved seed contribution binds this Claim; the finite inventory is empty.', 'evidence_gap'))
    unknown = _claim_unknowns(facts, port) if field == 'claim_artifact_record_count' else facts.unresolved_artifacts
    if unknown and field in ('unresolved_seed_artifact_reference_count',
                            'nominal_seed_artifact_record_count', 'claim_artifact_record_count'):
        unknown_refs = []
        for entity in unknown:
            port.charge(1)
            unknown_refs.append(_profile_ref(entity, port))
        for ref in unknown_refs:
            _charge_input_ref(ref, port, repeats=4)
        for _ in range(3):
            _charge_scope(scope, port)
        port.charge(20 + len(unknown_refs))
        reasons.append(_results._Reason('unknown_endpoint', scope, (result_ref,), tuple(unknown_refs),
            'This inventory scope contains explicit unresolved Artifact positions; they are not resolved Artifact records.', 'evidence_gap'))
    port.charge(len(reasons) + 1)
    reasons = tuple(reasons)
    components = []
    for name, links in (('premises', source_refs), ('conflicts', ()), ('value', (result_ref,)),
                        ('basis', basis), ('reasons', reasons), ('witnesses', (witness_ref,))):
        for link in links:
            for _ in range(3):
                _charge_link(link, port)
        port.charge(len(links) * len(links) + 10)
        components.append(_ComponentCompletion(name, links, links))
    for _ in range(3):
        _charge_link(population, port)
    port.charge(24)
    completion = _CompletionRecord(result_ref, (population,),
        (_PopulationCompletion(population, population.member_refs),), tuple(components))
    checks.append(_completion_check(completion, port))
    for _ in range(2):
        _charge_link(result_ref, port)
        _charge_link(population, port)
        for links in (checks, basis, reasons, (witness_ref,)):
            for link in links:
                _charge_link(link, port)
    port.charge(len(checks) + len(reasons) + 48)
    result = _results._Result(result_ref, (population,), 'completed', 'available',
        'inventory', 'count', value, tuple(checks), basis, (witness_ref,), reasons,
        'Finite supplied record inventory only. Contributions remain distinct by ID; unresolved '
        'references remain unresolved. Counts do not establish actual sources, truth, authenticity, '
        'independence, historical applicability or an end-to-end analytical run.')
    port.check()
    return result, witness


def _inventory_profile(prepared, context, ledger, port):
    """Five complete atomic leaves; no public run or partial-profile salvage.

    The explicit ledger must be the runtime-issued shared invocation ledger.
    Source identities and all repeated payload occurrences consume the actual
    current job. A stop retains its original cause and never refunds work.
    """
    facts = _inventory_facts(prepared, context, port)
    _inventory_ledger(facts, ledger, port)
    whole = _inventory_scope(facts, False, port)
    claim = _inventory_scope(facts, True, port)
    sources, basis = _inventory_basis(facts, port)
    values, witnesses = [], []
    for scope, field, entities, unit, selection in (
        (whole, 'nominal_seed_artifact_record_count', facts.artifacts, 'artifact_record',
         'A(I): resolved explicit seed Artifacts union resolved Artifact bindings of every Inquiry seed EvidenceItem.'),
        (whole, 'unresolved_seed_artifact_reference_count', facts.unresolved_artifacts, 'unresolved_reference',
         'U_A(I): unique unresolved Artifact reference IDs at the same explicit Inquiry seed source positions.'),
        (claim, 'seed_evidence_item_count', facts.seed_evidence, 'evidence_item',
         'E(I,C): explicitly listed resolved seed EvidenceItem IDs whose exact Claim binding is C.'),
        (claim, 'claim_artifact_record_count', facts.claim_artifacts, 'artifact_record',
         'A(I,C): unique resolved Artifact IDs bound by E(I,C); unresolved endpoints are excluded.'),
        (whole, 'claim_unassigned_seed_artifact_record_count', facts.unassigned_artifacts, 'artifact_record',
         'Resolved explicit Artifact seeds lacking any seed EvidenceItem binding in this entire Inquiry.')):
        port.charge(4)
        result, witness = _inventory_result(facts, scope, field, entities, unit, selection, sources, basis, ledger, port)
        values.append(result)
        witnesses.append(witness)
    for value in values:
        _charge_link(value.ref, port)
    port.charge(24)
    result_set = _results._ResultSet(tuple(values))
    answer = _InventoryProfile(facts, result_set.results, tuple(witnesses))
    port.check()
    return answer


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _ComparisonInventoryFacts:
    """SOURCE_INVENTORY's exact supplied comparison selection, not PC11.

    In particular, presence, population and scope matching neither authenticate
    the native conclusion nor establish basis, time, identity or independence.
    """
    prepared: object
    context: object
    job_port: object
    inquiry: object
    assessment: object
    members: tuple
    examined_assessments: tuple
    selection_refs: tuple
    scope_compatible: bool
    reason_codes: tuple
    pc03: _ProviderFact


def _comparison_scope(entity, context, port):
    """Only source ID membership; no lifecycle or qualification filtering."""
    scope = _field(entity.node.fields, 'scope', port)
    if not _analysis_contains(_field(scope, 'inquiry_refs', port).items, context.inquiry_ref, port):
        return False
    claims = _field(scope, 'claim_refs', port).items
    for claim in context.claim_refs:
        port.charge(1)
        if not _analysis_contains(claims, claim, port):
            return False
    details = _field(_field(entity.node.fields, 'data', port), 'details', port)
    return _compare_text(_field(details, 'dimension', port), context.dependency_dimension, port) == 0


def _comparison_subjects_match(members, context, port):
    if not context.subject_refs:
        return True
    port.charge(1)
    if len(members) != len(context.subject_refs):
        return False
    for member in members:
        port.charge(1)
        if not _analysis_contains(context.subject_refs, member.identifier, port):
            return False
    return True


def _comparison_inventory_facts(prepared, context, assessment_ref, port):
    """Enumerate one explicit independence assessment's submitted subjects.

    Empty context subjects derive the exact native list. A caller subset or
    superset cannot replace that list: the mismatch is retained as PC03 unmet,
    with the supplied population still present. Multiple selected Claim IDs
    are permitted, each exactly targeted by the Inquiry and required in scope.

    None requests absence of an applicable supplied comparison for this exact
    question. The finite source set is actually scanned. An existing match
    requires explicit selection; overlapping pairs never become a joint set.
    An empty subject query is not a subject wildcard for a selected assessment:
    its population comes only from that explicit source assertion.
    """
    inquiry = _analysis_start(prepared, context, port)
    port.charge(4)
    _require(bool(context.claim_refs) and context.dependency_dimension is not None)
    _require(assessment_ref is None or type(assessment_ref) is str)
    targets = _field(inquiry.node.fields, 'target_claim_refs', port).items
    for claim in context.claim_refs:
        port.charge(1)
        _require(_analysis_contains(targets, claim, port))
    dimensions = _field(inquiry.node.fields, 'dependency_dimensions', port).items
    _require(_analysis_contains(dimensions, context.dependency_dimension, port))
    sources = [_analysis_address(inquiry, port, 'target_claim_refs'),
               _analysis_address(inquiry, port, 'dependency_dimensions')]
    examined, members = [], ()
    assessment, compatible, reasons = None, False, ('missing_comparison_assessment',)
    if assessment_ref is not None:
        assessment = _analysis_lookup(prepared, assessment_ref, port)
        _require(assessment.collection == 'assertions')
        obj = assessment.node.fields
        _require(_field(obj, 'assertion_kind', port) == 'assessment')
        data = _field(obj, 'data', port)
        _require(_field(data, 'assessment_kind', port) == 'independence')
        members = _entities(prepared, _field(data, 'subject_refs', port).items, port)
        compatible = _comparison_scope(assessment, context, port) and _comparison_subjects_match(members, context, port)
        reasons = () if compatible else ('scope_unestablished',)
        port.charge(1)
        examined.append(assessment)
    else:
        # A no-selection request is not an invitation to pick a winner,
        # calculate a maximal set, sum pairs, or synthesize a singleton.
        found = False
        for candidate in prepared.entities:
            port.charge(2)
            if candidate.collection != 'assertions':
                continue
            obj = candidate.node.fields
            if _field(obj, 'assertion_kind', port) != 'assessment':
                continue
            data = _field(obj, 'data', port)
            if _field(data, 'assessment_kind', port) != 'independence':
                continue
            port.charge(1)
            examined.append(candidate)
            if _comparison_scope(candidate, context, port):
                candidate_members = _entities(prepared, _field(data, 'subject_refs', port).items, port)
                if _comparison_subjects_match(candidate_members, context, port):
                    found = True
        if found:
            raise TypeError('explicit_comparison_selection_required')
    for candidate in examined:
        for selector in ('scope.inquiry_refs', 'scope.claim_refs', 'data.subject_refs', 'data.details.dimension'):
            port.charge(1)
            sources.append(_analysis_address(candidate, port, selector))
    port.charge(len(sources) + 1)
    source_refs = _analysis_unique_addresses(tuple(sources), port)
    # Provider construction revisits and hashes all source-address strings;
    # no earlier source lookup's debit stands in for this additional pass.
    for source in source_refs:
        for unused in range(3):
            _analysis_text(source.collection, port)
            _analysis_text(source.record_id, port)
            _analysis_text(source.selector, port)
    port.charge(16 + 4 * len(source_refs))
    state = 'unknown' if assessment is None else 'met' if compatible else 'unmet'
    provider = _ProviderFact('PC03', 'SOURCE_INVENTORY', context, state, source_refs, prepared)
    port.charge(len(examined) + len(reasons) + 16)
    result = _ComparisonInventoryFacts(prepared, context, port, inquiry, assessment,
        members, tuple(examined), source_refs, compatible, reasons, provider)
    port.check()
    return result


def _check_comparison_inventory(facts, prepared, context, port):
    """Facts can be consumed only in their actual current analytical job."""
    _analysis_port(port)
    port.charge(4)
    _require(type(facts) is _ComparisonInventoryFacts and facts.job_port is port and
             facts.prepared is prepared and facts.context is context)
