# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: REPORT_CONTRACT.

Private preparation declarations and bounded analytical delivery contracts.
No public audit envelope, report identifiers or renderer are constructed here.
Level labels are independent evidence domains, never a score or maximum level.
The preparation-only contracts retain their earlier meaning: only PC01 has
completed after W05 admission and PC02-PC24 remain execution-pending. W13
delivery links the separate actual owners' analytical facts and complete cells.
"""
from dataclasses import dataclass
from .bundle import _require

DOMAIN_LABELS = (
    (0, "Artifact and contribution inventory"),
    (1, "Declared provenance and process metadata"),
    (2, "Origin-resolution and scoped process-assessment evidence"),
    (3, "Evaluator, correction-route and authority evidence"),
    (4, "Boundary-qualified external input, stage histories and documented correction outcomes"),
)
PREREQUISITES = (
    "PC01", "PC02", "PC03", "PC04", "PC05", "PC06", "PC07", "PC08",
    "PC09", "PC10", "PC11", "PC12", "PC13", "PC14", "PC15", "PC16",
    "PC17", "PC18", "PC19", "PC20", "PC21", "PC22", "PC23", "PC24",
)
FAMILIES = (
    "SIT-M001", "SIT-M002", "SIT-M003", "SIT-M004", "SIT-M005",
    "SIT-M006", "SIT-M007", "SIT-M008", "SIT-M009", "SIT-M010",
    "SIT-M011", "SIT-M012", "SIT-M013", "SIT-M014", "SIT-M015",
)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _PendingCheck:
    """No boolean or unknown-evidence substitute for unfinished execution."""
    prerequisite: str

    def __post_init__(self) -> None:
        _require(type(self.prerequisite) is str and self.prerequisite in PREREQUISITES)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _SuppliedSelector:
    """Inert locator within the one supplied snapshot; no file/URI authority."""
    collection: str
    record_id: str
    field_path: str

    def __post_init__(self) -> None:
        _require(type(self.collection) is str and self.collection in
                 ("inquiries", "records", "assertions", "evidence_references"))
        _require(type(self.record_id) is str and type(self.field_path) is str)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _DomainPreparation:
    """Explicit supplied selectors and pending checks; not public domain output."""
    level_index: int
    supplied: tuple
    pending: tuple

    def __post_init__(self) -> None:
        _require(type(self.level_index) is int and 0 <= self.level_index <= 4)
        _require(type(self.supplied) is tuple and type(self.pending) is tuple)
        _require(all(type(s) is _SuppliedSelector for s in self.supplied))
        _require(all(type(p) is _PendingCheck for p in self.pending))


# W06 compiled declarations from reporting sections 13-17. No runtime reads.
from .bundle import _is_value, _Array, _Object
from .evidence import _PreparedBundle

FAMILY_PREPARATION_BINDINGS = (
    ('SIT-M001', ('nominal_seed_artifact_record_count', 'unresolved_seed_artifact_reference_count', 'seed_evidence_item_count', 'claim_artifact_record_count', 'claim_unassigned_seed_artifact_record_count'), ('PC01', 'PC02', 'PC03', 'PC24'), (0,)),
    ('SIT-M002', ('reached_origin_record_count', 'documentary_origin_boundary_record_count', 'origin_boundary_disclosures'), ('PC01', 'PC02', 'PC03', 'PC04', 'PC05', 'PC06', 'PC07', 'PC08', 'PC09', 'PC10', 'PC24'), (1, 2)),
    ('SIT-M003', ('submitted_comparison_member_count', 'qualified_process_set_member_count', 'qualified_origin_set_member_count', 'independence_assessment_disclosures'), ('PC01', 'PC02', 'PC03', 'PC04', 'PC05', 'PC06', 'PC07', 'PC08', 'PC09', 'PC10', 'PC11', 'PC24'), (2,)),
    ('SIT-M004', ('per_seed_origin_memberships', 'origin_incidence_counts', 'seed_origin_dispositions', 'documentary_origin_resolution_fraction'), ('PC01', 'PC02', 'PC03', 'PC04', 'PC05', 'PC06', 'PC07', 'PC08', 'PC09', 'PC10', 'PC24'), (2,)),
    ('SIT-M005', ('single_origin_contribution_hhi',), ('PC01', 'PC02', 'PC03', 'PC04', 'PC05', 'PC06', 'PC07', 'PC08', 'PC09', 'PC10', 'PC11', 'PC12', 'PC24'), (2,)),
    ('SIT-M006', ('immediate_evidence_layer_dispositions', 'inherited_only_seed_fraction', 'inherited_only_completion_interval'), ('PC01', 'PC02', 'PC03', 'PC04', 'PC05', 'PC06', 'PC08', 'PC09', 'PC10', 'PC13', 'PC24'), (1, 2)),
    ('SIT-M007', ('unresolved_frontier_reference_count', 'unqualified_terminal_record_count', 'seed_items_with_unresolved_ancestry_count', 'ancestry_gap_disclosures'), ('PC01', 'PC02', 'PC03', 'PC04', 'PC24'), (1,)),
    ('SIT-M008', ('shared_recorded_ancestor_count', 'matching_family_label_count', 'evaluator_overlap_disclosures', 'evaluator_overlap_witnesses'), ('PC01', 'PC02', 'PC03', 'PC04', 'PC05', 'PC06', 'PC07', 'PC08', 'PC09', 'PC10', 'PC14', 'PC24'), (3,)),
    ('SIT-M009', ('externality_assessment_disclosures', 'externality_stage_links'), ('PC01', 'PC02', 'PC05', 'PC09', 'PC10', 'PC15', 'PC24'), (4,)),
    ('SIT-M010', ('pipeline_stage_disclosures', 'stage_member_partition', 'stage_occurrence_fraction', 'stage_occurrence_completion_interval', 'cohort_transition_disclosures', 'cohort_transition_fraction', 'cohort_transition_completion_interval'), ('PC01', 'PC16', 'PC17', 'PC18', 'PC24'), (4,)),
    ('SIT-M011', ('declared_correction_route_witnesses', 'applicable_authorized_route_witnesses', 'correction_route_disclosures'), ('PC01', 'PC02', 'PC04', 'PC05', 'PC06', 'PC09', 'PC10', 'PC19', 'PC20', 'PC24'), (3,)),
    ('SIT-M012', ('correction_case_record_count', 'handling_event_record_count', 'linked_change_event_record_count', 'documentary_linked_change_target_count', 'cases_with_documentary_linked_change_count', 'correction_case_disclosures', 'correction_target_change_disclosures', 'reported_capacity_disclosures'), ('PC01', 'PC02', 'PC03', 'PC04', 'PC05', 'PC08', 'PC09', 'PC10', 'PC21', 'PC24'), (4,)),
    ('SIT-M013', ('corrective_independence_disclosures', 'human_contribution_disclosures'), ('PC01', 'PC02', 'PC05', 'PC08', 'PC09', 'PC10', 'PC11', 'PC14', 'PC22', 'PC24'), (3,)),
    ('SIT-M014', ('anomaly_context_disclosures', 'contestation_disclosures', 'tail_stage_result_links'), ('PC01', 'PC02', 'PC05', 'PC09', 'PC10', 'PC16', 'PC17', 'PC18', 'PC23', 'PC24'), (4,)),
    ('SIT-M015', ('coverage_disclosures', 'documentary_basis_gap_disclosures', 'declared_basis_inventory', 'reference_availability_inventory'), ('PC01', 'PC02', 'PC03', 'PC04', 'PC05', 'PC06', 'PC09', 'PC10', 'PC24'), (1, 3)),
)

PREREQUISITE_OWNERS = (
    ('PC01', 'INGESTION_CONTRACT'),
    ('PC02', 'REPORT_CONTRACT'),
    ('PC03', 'SOURCE_INVENTORY'),
    ('PC04', 'GRAPH_VIEW_CONTRACT'),
    ('PC05', 'EVIDENCE_BASIS'),
    ('PC06', 'EVIDENCE_BASIS'),
    ('PC07', 'ORIGIN_ANALYSIS'),
    ('PC08', 'EVIDENCE_BASIS'),
    ('PC09', 'EVIDENCE_BASIS'),
    ('PC10', 'TEMPORAL_CONTRACT'),
    ('PC11', 'PROCESS_COMPARISON'),
    ('PC12', 'CONTRIBUTION_PROFILE'),
    ('PC13', 'CONTRIBUTION_PROFILE'),
    ('PC14', 'EVALUATOR_LINEAGE'),
    ('PC15', 'PRESENCE_RECORDS'),
    ('PC16', 'PRESENCE_RECORDS'),
    ('PC17', 'PRESENCE_RECORDS'),
    ('PC18', 'PRESENCE_RECORDS'),
    ('PC19', 'CORRECTION_ROUTES'),
    ('PC20', 'CORRECTION_ROUTES'),
    ('PC21', 'CORRECTION_OUTCOMES'),
    ('PC22', 'HUMAN_REVIEW_RECORDS'),
    ('PC23', 'CONTEXT_PRESERVATION'),
    ('PC24', 'REPORT_CONTRACT'),
)

FACET_BINDINGS = (
    ('inquiry', (1, 2, 4, 5, 6, 7, 15), (0, 1), ('PC02', 'PC03', 'PC06', 'PC10', 'PC12'), ('target_claim_refs', 'target_object_refs', 'seed_artifact_refs', 'seed_evidence_refs', 'boundary', 'dependency_dimensions', 'time_window', 'as_of', 'coverage_assertion_refs')),
    ('claim', (1, 2, 4, 5, 6, 7), (0, 1), ('PC02', 'PC03', 'PC08'), ('data', 'data.claim_key', 'data.version_label', 'data.text', 'data.content_evidence_ref')),
    ('artifact', (1, 6, 8, 15), (0, 1), ('PC03', 'PC08', 'PC13'), ('data', 'data.locators', 'data.content_evidence_refs', 'data.published_at', 'data.retrieved_at')),
    ('evidence_item', (1, 2, 4, 5, 6, 7), (0, 1), ('PC02', 'PC03', 'PC08', 'PC12', 'PC13'), ('data', 'data.claim_ref', 'data.artifact_ref', 'data.locator', 'data.epistemic_type')),
    ('actor', (8, 13, 15), (1, 3), ('PC08', 'PC14', 'PC22'), ('data', 'data.actor_kind', 'data.identity_disclosure', 'data.display_name', 'data.identity_key')),
    ('model', (8, 13, 15), (1, 3), ('PC08', 'PC14', 'PC22'), ('data', 'data.model_key', 'data.version_label', 'data.family_label')),
    ('origin_event', (2, 3, 4, 5, 7), (1, 2), ('PC07', 'PC08', 'PC11', 'PC12'), ('data', 'data.event_kind', 'data.performed_by_refs', 'data.method_ref', 'data.occurred_at')),
    ('evaluation', (8, 13), (3,), ('PC14', 'PC22'), ('data', 'data.evaluation_kind', 'data.target_refs', 'data.role_bindings', 'data.result_refs', 'data.occurred_at', 'data.review_contribution')),
    ('correction_channel', (11,), (3,), ('PC19', 'PC20'), ('data', 'data.owner_refs', 'data.target_refs', 'data.contact_locator', 'data.declared_action_types', 'data.valid_window')),
    ('correction_event', (12,), (4,), ('PC21',), ('data', 'data.event_kind', 'data.case_ref', 'data.channel_ref', 'data.target_refs', 'data.occurred_at', 'data.details')),
    ('pipeline_record', (10, 14), (4,), ('PC16', 'PC17', 'PC18'), ('data', 'data.subject_ref', 'data.run_key', 'data.stage_key', 'data.stage', 'data.state', 'data.output_refs', 'data.observed_at', 'data.linkage_kind')),
    ('anomaly', (14,), (4,), ('PC23',), ('data', 'data.inquiry_refs', 'data.claim_ref', 'data.original_context', 'data.context_evidence_ref', 'data.classification_state', 'data.caller_label', 'data.comparison_note')),
    ('unresolved_reference', (7, 15), (1, 2), ('PC08', 'PC12'), ('data', 'data.expected_kinds', 'data.reason', 'data.description', 'data.external_locator', 'data.protected_key')),
    ('evidence_reference', (15,), (0, 1), ('PC05', 'PC08'), ('reference_kind', 'availability', 'artifact_ref', 'record_ref', 'locator', 'excerpt', 'provided_by_ref', 'attestor_ref', 'scope_note')),
    ('relation', (2, 4, 5, 6, 7, 8), (1, 2), ('PC04', 'PC08', 'PC09', 'PC13'), ('data', 'data.predicate', 'data.from_ref', 'data.to_ref', 'data.polarity', 'data.dimension', 'data.details')),
    ('relation:stance', (14,), (4,), ('PC09', 'PC23'), ('data', 'data.predicate', 'data.from_ref', 'data.to_ref', 'data.polarity', 'data.dimension', 'data.details')),
    ('relation:propagates_to', (11,), (3,), ('PC04', 'PC19', 'PC20'), ('data', 'data.from_ref', 'data.to_ref', 'data.polarity', 'data.details.action_type', 'data.details.valid_window')),
    ('relation:same_identity_as', (8, 15), (1, 3), ('PC08',), ('data', 'data.from_ref', 'data.to_ref', 'data.polarity', 'data.details.identity_level')),
    ('assessment:origin_boundary', (2, 4, 5), (1, 2), ('PC06', 'PC07', 'PC12'), ('data', 'data.subject_refs', 'data.details', 'data.details.dimension', 'data.details.boundary_role', 'data.details.coverage_ref')),
    ('assessment:independence', (3, 13), (2, 3), ('PC11', 'PC22'), ('data', 'data.subject_refs', 'data.details', 'data.details.dimension', 'data.details.conclusion', 'data.details.examined_dependency_refs', 'data.details.coverage_ref')),
    ('assessment:coverage', (15, 10, 14), (1, 4), ('PC06', 'PC16', 'PC18'), ('data', 'data.subject_refs', 'data.details', 'data.details.coverage_kind', 'data.details.state', 'data.details.member_refs', 'data.details.omitted_refs', 'data.details.universe_enumerated')),
    ('assessment:classification', (15, 13), (1, 3), ('PC05', 'PC22'), ('data', 'data.subject_refs', 'data.details', 'data.details.axis', 'data.details.labels', 'data.details.verification_assessment_refs')),
    ('assessment:verification', (15,), (1,), ('PC05',), ('data', 'data.subject_refs', 'data.details', 'data.details.verification_scope', 'data.details.evaluation_ref', 'data.details.reported_outcome', 'data.details.valid_window')),
    ('assessment:externality', (9,), (4,), ('PC15',), ('data', 'data.subject_refs', 'data.details', 'data.details.boundary_inquiry_ref')),
    ('assessment:authority', (11,), (3,), ('PC19', 'PC20'), ('data', 'data.subject_refs', 'data.details', 'data.details.target_refs', 'data.details.authorized_by_ref', 'data.details.coverage_ref')),
    ('assessment:capacity', (12,), (4,), ('PC21',), ('data', 'data.subject_refs', 'data.details')),
    ('assessment:conflict', (14, 15), (1, 4), ('PC09', 'PC23'), ('data', 'data.subject_refs', 'data.details', 'data.details.resolution_evaluation_ref')),
)

COMMON_FACET_PATHS = (
    'provenance',
    'provenance.attributed_to_ref',
    'provenance.basis_kind',
    'provenance.evidence_ref_ids',
    'provenance.method',
    'provenance.qualifications',
    'gaps',
)

ASSERTION_FACET_PATHS = (
    'scope',
    'scope.inquiry_refs',
    'scope.claim_refs',
    'scope.effective_window',
    'asserted_at',
    'lifecycle_state',
    'lifecycle_basis_ref_ids',
)

DIRECT_SUBJECT_BINDINGS = (
    ('evidence_item', ('data.claim_ref',)),
    ('evaluation', ('data.target_refs',)),
    ('correction_channel', ('data.target_refs',)),
    ('correction_event', ('data.target_refs',)),
    ('pipeline_record', ('data.subject_ref',)),
)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _InputFacet:
    """Observed source field and its exact immutable value. Missing is distinct
    from a supplied null/empty value and from an unexecuted semantic check.
    """
    selector: _SuppliedSelector
    present: bool
    value: object
    questions: tuple

    def __post_init__(self) -> None:
        _require(type(self.selector) is _SuppliedSelector and type(self.present) is bool)
        _require(_is_value(self.value) and (self.present or self.value is None))
        _require(type(self.questions) is tuple)
        _require(all(type(q) is str and q in PREREQUISITES[1:] for q in self.questions))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _RecordEvidence:
    """Raw tagged source fields. Family/domain membership grants no result."""
    collection: str
    record_id: str
    families: tuple
    domains: tuple
    facets: tuple

    def __post_init__(self) -> None:
        _require(type(self.collection) is str and type(self.record_id) is str)
        _require(type(self.families) is tuple and all(type(x) is str and x in FAMILIES for x in self.families))
        _require(type(self.domains) is tuple and all(type(x) is int and 0 <= x <= 4 for x in self.domains))
        _require(type(self.facets) is tuple and all(type(x) is _InputFacet for x in self.facets))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _BoundRecord:
    """One direct declared binding and the source selector that supplies it.
    This is not reachability, relevance qualification or a graph witness.
    """
    record_id: str
    basis: _SuppliedSelector

    def __post_init__(self) -> None:
        _require(type(self.record_id) is str and type(self.basis) is _SuppliedSelector)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _PrerequisitePreparation:
    prerequisite: str
    complete_check_executed: bool
    answer: str | None
    deferred_owner: str | None
    constituent_fields: tuple

    def __post_init__(self) -> None:
        _require(type(self.prerequisite) is str and self.prerequisite in PREREQUISITES)
        _require(type(self.complete_check_executed) is bool and type(self.constituent_fields) is tuple)
        _require(all(type(x) is _InputFacet for x in self.constituent_fields))
        if self.prerequisite == "PC01":
            _require(self.complete_check_executed is True and self.answer == "met" and self.deferred_owner is None)
        else:
            _require(self.complete_check_executed is False and self.answer is None)
            _require((self.prerequisite, self.deferred_owner) in PREREQUISITE_OWNERS)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _FamilyPreparation:
    """All registered leaves stay visible. Questions are navigation candidates
    from the family matrix, NOT a conjunction imposed on each leaf. Detailed
    Claim/dimension, actual role and stage/case tuples remain in anchor fields;
    no Cartesian product or eligible operation is manufactured here.
    """
    family: str
    field_keys: tuple
    relevant_questions: tuple
    explicit_record_refs: tuple
    binding_note: str

    def __post_init__(self) -> None:
        _require(type(self.family) is str and self.family in FAMILIES)
        row = FAMILY_PREPARATION_BINDINGS[FAMILIES.index(self.family)]
        _require(self.field_keys == row[1] and self.relevant_questions == row[2])
        _require(type(self.explicit_record_refs) is tuple and all(type(x) is str for x in self.explicit_record_refs))
        expected = "direct_supplied_bindings_only" if self.explicit_record_refs else "no_direct_binding_after_finite_scan"
        _require(self.binding_note == expected)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _InquiryEvidence:
    inquiry_ref: str
    bindings: tuple
    records: tuple
    families: tuple
    domains: tuple
    prerequisites: tuple

    def __post_init__(self) -> None:
        _require(type(self.inquiry_ref) is str)
        for values, kind in ((self.bindings, _BoundRecord), (self.records, _RecordEvidence),
                             (self.families, _FamilyPreparation), (self.domains, _DomainPreparation),
                             (self.prerequisites, _PrerequisitePreparation)):
            _require(type(values) is tuple and all(type(x) is kind for x in values))
        _require(tuple(x.family for x in self.families) == FAMILIES)
        _require(tuple(x.level_index for x in self.domains) == (0, 1, 2, 3, 4))
        _require(tuple(x.prerequisite for x in self.prerequisites) == PREREQUISITES)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _ObservabilityPreparation:
    """Private component output, no analytical/public report fields. Snapshot
    records not directly bound to an Inquiry stay visible in snapshot_records.
    The constructor trusts bounded tool-owned inputs; it is not an authenticator.
    """
    prepared: _PreparedBundle
    snapshot_records: tuple
    inquiries: tuple

    def __post_init__(self) -> None:
        _require(type(self.prepared) is _PreparedBundle)
        _require(type(self.snapshot_records) is tuple and all(type(x) is _RecordEvidence for x in self.snapshot_records))
        _require(type(self.inquiries) is tuple and all(type(x) is _InquiryEvidence for x in self.inquiries))

    @property
    def input_state(self) -> str:
        return "accepted"

    @property
    def preparation_kind(self) -> str:
        return "private_observability_preparation"


# P3-W02: separate analytical facts. All preparation declarations above retain
# their earlier meanings; constructing these facts does not execute an analysis.
from .execution import _BudgetPort, _JobPort, _byte_work
from .bundle import _Number
from .results import (
    _InputRef, _Scope, _Population, _CaseTarget, _BasisRef, _ResultRef, _Reason,
    _PrerequisiteCheck, _WitnessRef, _unique,
)

_COMPLETION_COMPONENTS = ('premises', 'conflicts', 'value', 'basis', 'reasons', 'witnesses')
_COMPLETION_REF_TYPES = (_InputRef, _ResultRef, _BasisRef, _WitnessRef, _PrerequisiteCheck, _Reason)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _ScopeCheckFact:
    """The expected cell and the exact scope examined by its actual owner.

    This is a private operation record, not proof of source authenticity or a
    substitute for the component's paid examination of the admitted snapshot.
    """
    result_ref: _ResultRef
    examined_scope: _Scope

    def __post_init__(self):
        _require(type(self.result_ref) is _ResultRef and type(self.examined_scope) is _Scope)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _PopulationCompletion:
    """Concrete visited members, rather than a caller-supplied complete flag."""
    population: _Population
    processed_member_refs: tuple

    def __post_init__(self):
        _require(type(self.population) is _Population)
        processed = _unique(self.processed_member_refs, (_InputRef, _CaseTarget))
        _require(processed <= {ref._key() for ref in self.population.member_refs})


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _ComponentCompletion:
    """Finite required and actually finished links for one commit component.

    An explicitly empty examined conflict set can finish. An omitted component
    cannot. Only the semantic owner can supply these project-owned facts after
    doing the work; their representation does not authenticate that history.
    """
    component: str
    required_refs: tuple
    processed_refs: tuple

    def __post_init__(self):
        _require(type(self.component) is str and self.component in _COMPLETION_COMPONENTS)
        required = _unique(self.required_refs, _COMPLETION_REF_TYPES)
        processed = _unique(self.processed_refs, _COMPLETION_REF_TYPES)
        _require(processed <= required)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _CompletionRecord:
    result_ref: _ResultRef
    required_populations: tuple
    population_completions: tuple
    components: tuple

    def __post_init__(self):
        _require(type(self.result_ref) is _ResultRef)
        required = _unique(self.required_populations, (_Population,))
        _require(all(pop.scope is self.result_ref.scope for pop in self.required_populations))
        _require(type(self.population_completions) is tuple and type(self.components) is tuple)
        populations, components = set(), set()
        for fact in self.population_completions:
            _require(type(fact) is _PopulationCompletion)
            key = fact.population._key()
            _require(key in required and key not in populations
                     and any(fact.population is pop for pop in self.required_populations))
            populations.add(key)
        for fact in self.components:
            _require(type(fact) is _ComponentCompletion and fact.component not in components)
            components.add(fact.component)
            if fact.component == 'value':
                _require(len(fact.required_refs) == 1 and type(fact.required_refs[0]) is _ResultRef
                         and fact.required_refs[0] is self.result_ref)


def _charge_scope(scope: _Scope, port: _BudgetPort) -> None:
    """Prospective bounded passes for keys, comparisons and constructor checks.

    Scope-key canonicalization compares sets. The quadratic bound prepaid here
    deliberately covers every possible pair rather than hiding a native sort.
    These private primitives are small; family algorithms use their paid index.
    """
    port.charge(12)
    _charge_input_ref(scope.inquiry_ref, port)
    for refs in (scope.claim_refs, scope.target_refs, scope.coverage_refs):
        port.charge(len(refs) * len(refs) + 2 * len(refs) + 1)
        for ref in refs:
            _charge_input_ref(ref, port, repeats=len(refs) + 3)
    for text in (scope.dependency_dimension, scope.graph_view, scope.temporal_basis):
        if text is not None:
            _byte_work(port, 4 * len(text), 1)
    if scope.requested_time is not None:
        _charge_frozen(scope.requested_time.fields, port)
    for text in scope.qualifications:
        _byte_work(port, 4 * len(text), 1)
    _charge_anchor(scope.operation_anchor, port)
    port.check()


def _charge_input_ref(ref: _InputRef, port: _BudgetPort, *, repeats: int = 1) -> None:
    for _ in range(repeats):
        port.charge(4)
        for text in (ref.collection, ref.identifier, ref.selector):
            if text is not None:
                _byte_work(port, 4 * len(text), 1)


def _charge_anchor(anchor: tuple, port: _BudgetPort) -> None:
    for part in anchor:
        port.charge(1)
        if type(part) is _InputRef:
            _charge_input_ref(part, port)
        elif type(part) is str:
            _byte_work(port, 4 * len(part), 1)


def _charge_frozen(value, port: _BudgetPort) -> None:
    port.charge(1)
    if type(value) is str:
        _byte_work(port, 4 * len(value), 1)
    elif type(value) is _Array:
        for child in value.items:
            _charge_frozen(child, port)
    elif type(value) is _Object:
        port.charge(len(value.items) * len(value.items) + len(value.items) + 1)
        for key, child in value.items:
            for _ in range(len(value.items) + 2):
                _byte_work(port, 4 * len(key), 1)
            _charge_frozen(child, port)
    elif type(value) is _Number:
        _byte_work(port, len(value.coefficient) + 32, 4)


def _charge_link(ref, port: _BudgetPort) -> None:
    port.charge(1)
    if type(ref) is _InputRef:
        _charge_input_ref(ref, port)
    elif type(ref) is _CaseTarget:
        _charge_input_ref(ref.case_ref, port)
        _charge_input_ref(ref.before_ref, port)
    elif type(ref) is _BasisRef:
        _charge_input_ref(ref.source, port)
    elif type(ref) is _ResultRef:
        _charge_scope(ref.scope, port)
        _byte_work(port, 4 * (len(ref.diagnostic_id) + len(ref.field_key)), 2)
    elif type(ref) is _WitnessRef:
        _charge_scope(ref.scope, port)
        _byte_work(port, 4 * len(ref.kind), 1)
        _charge_anchor(ref.anchor, port)
    elif type(ref) is _PrerequisiteCheck:
        _charge_link(ref.result_ref, port)
        _byte_work(port, 4 * len(ref.check_id), 1)
    elif type(ref) is _Reason:
        _charge_scope(ref.scope, port)
        _byte_work(port, 4 * (len(ref.code) + len(ref.detail) + len(ref.classification)), 3)
        for source in ref.input_refs:
            _charge_input_ref(source, port, repeats=len(ref.input_refs) + 3)
    elif type(ref) is _Population:
        _charge_scope(ref.scope, port)
        _byte_work(port, 4 * (len(ref.unit) + len(ref.selection_rule)), 2)
        for member in ref.member_refs:
            for _ in range(len(ref.member_refs) + 3):
                _charge_link(member, port)
    else:
        raise TypeError('invalid_private_representation')


def _same_links(required: tuple, processed: tuple, port: _BudgetPort) -> bool:
    """Paid finite matching; duplicates were refused at fact construction."""
    port.charge(1)
    if len(required) != len(processed):
        return False
    for expected in required:
        found = False
        for observed in processed:
            port.charge(1)
            _charge_link(expected, port)
            _charge_link(observed, port)
            if expected._key() == observed._key():
                found = True
                break
        if not found:
            return False
    return True


def _scope_check(fact: _ScopeCheckFact, port: _JobPort) -> _PrerequisiteCheck:
    """Execute only the PC02 exact-scope comparison on a current analysis job."""
    try:
        port.check_analysis()
    except AttributeError:
        raise TypeError('analysis_job_port_required') from None
    port.charge(1)
    _require(type(fact) is _ScopeCheckFact)
    # Separate passes cover the comparison and construction of linked output.
    for _ in range(4):
        _charge_link(fact.result_ref, port)
        _charge_scope(fact.examined_scope, port)
    matched = fact.result_ref.scope._key() == fact.examined_scope._key()
    reasons = ()
    if not matched:
        port.charge(12)
        _byte_work(port, 256, 1)
        reasons = (_Reason('scope_unestablished', fact.result_ref.scope, (fact.result_ref,), (),
                           'The examined scope differs from this exact result cell.', 'evidence_gap'),)
    port.charge(12)
    _byte_work(port, 256, 1)
    port.check()
    result = _PrerequisiteCheck('PC02', fact.result_ref, 'met' if matched else 'unmet', (), reasons,
                                'Exact operation scope comparison; supplied evidence is not authenticated.')
    port.check()
    return result


def _completion_check(record: _CompletionRecord, port: _JobPort) -> _PrerequisiteCheck:
    """PC24 checks the owner's finite completion record, not metadata flags.

    Unfinished work must not publish this check as an epistemic non-result:
    the owning operation retains its interrupted/not_performed result pairing.
    A later orchestrator cannot manufacture missing component records.
    """
    try:
        port.check_analysis()
    except AttributeError:
        raise TypeError('analysis_job_port_required') from None
    port.charge(1)
    _require(type(record) is _CompletionRecord)
    port.charge(len(record.population_completions) + 1)
    matched = _same_links(record.required_populations,
                          tuple(fact.population for fact in record.population_completions), port)
    for fact in record.population_completions:
        port.charge(2)
        if fact.population.membership_state != 'enumerated_for_scope':
            matched = False
        if not _same_links(fact.population.member_refs, fact.processed_member_refs, port):
            matched = False
    port.charge(len(record.components) + len(_COMPLETION_COMPONENTS) + 2)
    if len(record.components) != len(_COMPLETION_COMPONENTS):
        matched = False
    for component in record.components:
        port.charge(1)
        if not _same_links(component.required_refs, component.processed_refs, port):
            matched = False
    for _ in range(4):
        _charge_link(record.result_ref, port)
    port.charge(12)
    _byte_work(port, 256, 1)
    port.check()
    result = _PrerequisiteCheck('PC24', record.result_ref, 'met' if matched else 'unmet', (), (),
                                'Owner-recorded finite processing is complete.' if matched else
                                'Required population or commit component remains unfinished; no value may commit.')
    port.check()
    return result


# W13 delivery contains private analytical objects only. It deliberately has no
# public report root, output identifiers, serializer, timestamps or score level.
from dataclasses import replace as _replace
from . import results as _results
from .evidence import _Entity, _Node, _QualificationContext, _SourceAddress
from .bundle import _lookup_pair


def _plan_part(value):
    if value is None or type(value) in (str, bool, int, _SourceAddress):
        return True
    return type(value) is tuple and all(_plan_part(part) for part in value)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _AnalyticalJobSpec:
    """Pre-acceptance structural selection, without qualification authority.

    Runtime prospectively charges construction and sorts the finite job list.
    The existing compiled catalog supplies required leaves, with no new registry.
    """
    inquiry_ref: str
    family: str
    operation_key: tuple
    context: _QualificationContext
    parameters: tuple = ()

    def __post_init__(self):
        _require(type(self.inquiry_ref) is str and bool(self.inquiry_ref))
        _require(type(self.family) is str and self.family in FAMILIES)
        _require(type(self.context) is _QualificationContext and
                 self.context.inquiry_ref == self.inquiry_ref)
        _require(type(self.operation_key) is tuple and bool(self.operation_key) and
                 _plan_part(self.operation_key))
        _require(type(self.parameters) is tuple and _plan_part(self.parameters))

    @property
    def field_keys(self):
        return FAMILY_PREPARATION_BINDINGS[FAMILIES.index(self.family)][1]


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _AnalyticalPlan:
    """Complete finite structural jobs, with no result or public request."""
    jobs: tuple

    def __post_init__(self):
        _require(type(self.jobs) is tuple and
                 all(type(job) is _AnalyticalJobSpec for job in self.jobs))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _JobOutcome:
    job: _AnalyticalJobSpec
    result_refs: tuple
    execution_state: str
    no_subject: bool = False

    def __post_init__(self):
        _require(type(self.job) is _AnalyticalJobSpec)
        _unique(self.result_refs, (_ResultRef,))
        _require(type(self.execution_state) is str and self.execution_state in
                 ('completed', 'interrupted', 'not_performed'))
        _require(type(self.no_subject) is bool)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _WitnessRecord:
    """Detached completed owner payload backing a finite group of links.

    Shared links do not copy the payload or reserve a second witness. The
    runtime adapter retains actual ordered owner members and record links;
    symbolic references alone cannot stand in for that completed payload.
    """
    refs: tuple
    payload: tuple
    input_refs: tuple
    member_count: int

    def __post_init__(self):
        _unique(self.refs, (_WitnessRef,))
        _require(bool(self.refs) and type(self.payload) is tuple)
        _require(type(self.input_refs) is tuple and
                 all(type(ref) is _InputRef for ref in self.input_refs))
        _require(type(self.member_count) is int and self.member_count >= 0)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _DetachedFindingWitness:
    input_refs: tuple
    owner_witnesses: tuple
    member_count: int

    def __post_init__(self):
        _require(type(self.input_refs) is tuple and
                 all(type(ref) is _InputRef for ref in self.input_refs))
        _require(type(self.owner_witnesses) is tuple)
        _require(type(self.member_count) is int and self.member_count >= 0)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _PrivateFinding:
    observation_kind: str
    condition_code: str
    diagnostic_refs: tuple
    threat_family_refs: tuple
    scope_ref: _Scope
    population_refs: tuple
    basis_refs: tuple
    witness: _DetachedFindingWitness
    contrary_input_refs: tuple
    reason_refs: tuple
    result_refs: tuple
    statement: str
    interpretation_limit: str
    native_records: tuple

    def __post_init__(self):
        for text in (self.observation_kind, self.condition_code, self.statement,
                     self.interpretation_limit):
            _require(type(text) is str and bool(text))
        _require(type(self.scope_ref) is _Scope and
                 type(self.witness) is _DetachedFindingWitness)
        for values in (self.diagnostic_refs, self.threat_family_refs, self.native_records):
            _require(type(values) is tuple)
        _unique(self.population_refs, (_Population,))
        _unique(self.basis_refs, (_BasisRef,))
        _unique(self.contrary_input_refs, (_InputRef,))
        _unique(self.reason_refs, (_Reason,))
        _unique(self.result_refs, (_ResultRef,))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Capability:
    inquiry_ref: str
    family: str
    result_refs: tuple
    available_result_refs: tuple
    unavailable_result_refs: tuple
    not_applicable_result_refs: tuple
    not_evaluated_result_refs: tuple
    check_refs: tuple
    reason_refs: tuple
    required_checks: tuple
    scope_note: str
    execution_state: str

    def __post_init__(self):
        _require(type(self.inquiry_ref) is str and type(self.family) is str and self.family in FAMILIES)
        for refs in (self.result_refs, self.available_result_refs, self.unavailable_result_refs,
                     self.not_applicable_result_refs, self.not_evaluated_result_refs):
            _require(type(refs) is tuple and all(type(ref) is _ResultRef for ref in refs))
        _require(type(self.check_refs) is tuple and
                 all(type(check) is _PrerequisiteCheck for check in self.check_refs))
        _require(type(self.reason_refs) is tuple and
                 all(type(reason) is _Reason for reason in self.reason_refs))
        _require(self.required_checks == FAMILY_PREPARATION_BINDINGS[FAMILIES.index(self.family)][2])
        _require(type(self.scope_note) is str and bool(self.scope_note))
        _require(self.execution_state in ('completed', 'interrupted', 'not_performed'))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _DomainOutcome:
    inquiry_ref: str
    level_index: int
    result_refs: tuple
    available_result_refs: tuple
    unavailable_result_refs: tuple
    not_applicable_result_refs: tuple
    not_evaluated_result_refs: tuple
    reason_refs: tuple

    def __post_init__(self):
        _require(type(self.inquiry_ref) is str and type(self.level_index) is int and
                 0 <= self.level_index <= 4)
        for refs in (self.result_refs, self.available_result_refs, self.unavailable_result_refs,
                     self.not_applicable_result_refs, self.not_evaluated_result_refs):
            _require(type(refs) is tuple and all(type(ref) is _ResultRef for ref in refs))
        _require(type(self.reason_refs) is tuple and
                 all(type(reason) is _Reason for reason in self.reason_refs))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _AnalyticalOutcome:
    """Private immutable delivery. Domain labels never imply cumulative rank."""
    prepared: _PreparedBundle
    plan: _AnalyticalPlan
    jobs: tuple
    results: tuple
    findings: tuple
    witnesses: tuple
    capabilities: tuple
    domains: tuple
    execution_state: str

    def __post_init__(self):
        _require(type(self.prepared) is _PreparedBundle and type(self.plan) is _AnalyticalPlan)
        for rows, kind in ((self.jobs, _JobOutcome), (self.results, _results._Result),
                           (self.findings, _PrivateFinding), (self.witnesses, _WitnessRecord),
                           (self.capabilities, _Capability), (self.domains, _DomainOutcome)):
            _require(type(rows) is tuple and all(type(row) is kind for row in rows))
        _require(self.execution_state in ('completed', 'interrupted'))

    @property
    def input_state(self):
        return 'accepted'

    @property
    def outcome_kind(self):
        return 'private_analytical_outcome'


_DELIVERY_TYPES = (
    _InputRef, _Scope, _CaseTarget, _BasisRef, _Population,
    _results._Count, _results._Fraction, _results._CompletionInterval,
    _results._PartitionCategory, _results._Partition, _results._IncidenceRow,
    _results._Incidence, _ResultRef, _results._Disclosure,
    _results._RecordDisclosures, _WitnessRef, _results._WitnessCollection,
    _Reason, _PrerequisiteCheck, _results._Result, _Entity, _Node,
    _QualificationContext, _SourceAddress, _WitnessRecord,
    _DetachedFindingWitness, _PrivateFinding,
)
_SET_FIELDS = (
    (_Scope, ('claim_refs', 'target_refs', 'coverage_refs')),
    (_Population, ('member_refs', 'coverage_refs', 'basis_refs')),
    (_Reason, ('affected_result_refs', 'input_refs')),
    (_PrerequisiteCheck, ('input_refs', 'reason_refs')),
    (_results._Result, ('population_refs', 'check_refs', 'basis_refs', 'witness_refs', 'reason_refs')),
    (_results._PartitionCategory, ('member_refs',)),
    (_results._IncidenceRow, ('origin_refs',)),
)


def _delivery_parts(value, port):
    """Explicit contract projection; no arbitrary attribute introspection."""
    kind = type(value)
    if kind is _InputRef:
        port.charge(8)
        return 'InputRef', (
            ('collection', value.collection),
            ('identifier', value.identifier),
            ('selector', value.selector),
        )
    if kind is _Scope:
        port.charge(22)
        return 'Scope', (
            ('inquiry_ref', value.inquiry_ref),
            ('claim_refs', value.claim_refs),
            ('target_refs', value.target_refs),
            ('dependency_dimension', value.dependency_dimension),
            ('graph_view', value.graph_view),
            ('temporal_basis', value.temporal_basis),
            ('requested_time', value.requested_time),
            ('coverage_refs', value.coverage_refs),
            ('qualifications', value.qualifications),
            ('operation_anchor', value.operation_anchor),
        )
    if kind is _CaseTarget:
        port.charge(6)
        return 'CaseTarget', (
            ('case_ref', value.case_ref),
            ('before_ref', value.before_ref),
        )
    if kind is _BasisRef:
        port.charge(4)
        return 'BasisRef', (
            ('source', value.source),
        )
    if kind is _Population:
        port.charge(18)
        return 'Population', (
            ('scope', value.scope),
            ('unit', value.unit),
            ('member_refs', value.member_refs),
            ('selection_rule', value.selection_rule),
            ('coverage_refs', value.coverage_refs),
            ('basis_refs', value.basis_refs),
            ('membership_state', value.membership_state),
            ('qualifications', value.qualifications),
        )
    if kind is _results._Count:
        port.charge(6)
        return 'Count', (
            ('value', value.value),
            ('population', value.population),
        )
    if kind is _results._Fraction:
        port.charge(8)
        return 'Fraction', (
            ('numerator', value.numerator),
            ('denominator', value.denominator),
            ('population', value.population),
        )
    if kind is _results._CompletionInterval:
        port.charge(10)
        return 'CompletionInterval', (
            ('lower', value.lower),
            ('upper', value.upper),
            ('interval_kind', value.interval_kind),
            ('partition', value.partition),
        )
    if kind is _results._PartitionCategory:
        port.charge(8)
        return 'PartitionCategory', (
            ('label', value.label),
            ('member_refs', value.member_refs),
            ('count', value.count),
        )
    if kind is _results._Partition:
        port.charge(6)
        return 'Partition', (
            ('population', value.population),
            ('categories', value.categories),
        )
    if kind is _results._IncidenceRow:
        port.charge(6)
        return 'IncidenceRow', (
            ('member_ref', value.member_ref),
            ('origin_refs', value.origin_refs),
        )
    if kind is _results._Incidence:
        port.charge(6)
        return 'Incidence', (
            ('population', value.population),
            ('memberships', value.memberships),
        )
    if kind is _ResultRef:
        port.charge(8)
        return 'ResultRef', (
            ('diagnostic_id', value.diagnostic_id),
            ('field_key', value.field_key),
            ('scope', value.scope),
        )
    if kind is _results._Disclosure:
        port.charge(8)
        return 'Disclosure', (
            ('source', value.source),
            ('fields', value.fields),
            ('qualifications', value.qualifications),
        )
    if kind is _results._RecordDisclosures:
        port.charge(4)
        return 'RecordDisclosures', (
            ('records', value.records),
        )
    if kind is _WitnessRef:
        port.charge(8)
        return 'WitnessRef', (
            ('scope', value.scope),
            ('kind', value.kind),
            ('anchor', value.anchor),
        )
    if kind is _results._WitnessCollection:
        port.charge(4)
        return 'WitnessCollection', (
            ('witness_refs', value.witness_refs),
        )
    if kind is _Reason:
        port.charge(14)
        return 'Reason', (
            ('code', value.code),
            ('scope', value.scope),
            ('affected_result_refs', value.affected_result_refs),
            ('input_refs', value.input_refs),
            ('detail', value.detail),
            ('classification', value.classification),
        )
    if kind is _PrerequisiteCheck:
        port.charge(14)
        return 'PrerequisiteCheck', (
            ('check_id', value.check_id),
            ('result_ref', value.result_ref),
            ('state', value.state),
            ('input_refs', value.input_refs),
            ('reason_refs', value.reason_refs),
            ('note', value.note),
        )
    if kind is _results._Result:
        port.charge(26)
        return 'Result', (
            ('ref', value.ref),
            ('population_refs', value.population_refs),
            ('execution_state', value.execution_state),
            ('result_state', value.result_state),
            ('result_origin', value.result_origin),
            ('value_kind', value.value_kind),
            ('value', value.value),
            ('check_refs', value.check_refs),
            ('basis_refs', value.basis_refs),
            ('witness_refs', value.witness_refs),
            ('reason_refs', value.reason_refs),
            ('interpretation_limit', value.interpretation_limit),
        )
    if kind is _Entity:
        port.charge(10)
        return 'Entity', (
            ('collection', value.collection),
            ('identifier', value.identifier),
            ('kind', value.kind),
            ('node', value.node),
        )
    if kind is _Node:
        port.charge(6)
        return 'Node', (
            ('shape', value.shape),
            ('fields', value.fields),
        )
    if kind is _QualificationContext:
        port.charge(22)
        return 'QualificationContext', (
            ('inquiry_ref', value.inquiry_ref),
            ('claim_refs', value.claim_refs),
            ('subject_refs', value.subject_refs),
            ('dependency_dimension', value.dependency_dimension),
            ('temporal_basis', value.temporal_basis),
            ('requested_time', value.requested_time),
            ('coverage_kind', value.coverage_kind),
            ('relation_types', value.relation_types),
            ('graph_view', value.graph_view),
            ('operation_anchor', value.operation_anchor),
        )
    if kind is _SourceAddress:
        port.charge(8)
        return 'SourceAddress', (
            ('collection', value.collection),
            ('record_id', value.record_id),
            ('selector', value.selector),
        )
    if kind is _WitnessRecord:
        port.charge(10)
        return 'WitnessRecord', (
            ('refs', value.refs),
            ('payload', value.payload),
            ('input_refs', value.input_refs),
            ('member_count', value.member_count),
        )
    if kind is _DetachedFindingWitness:
        port.charge(8)
        return 'DetachedFindingWitness', (
            ('input_refs', value.input_refs),
            ('owner_witnesses', value.owner_witnesses),
            ('member_count', value.member_count),
        )
    if kind is _PrivateFinding:
        port.charge(30)
        return 'PrivateFinding', (
            ('observation_kind', value.observation_kind),
            ('condition_code', value.condition_code),
            ('diagnostic_refs', value.diagnostic_refs),
            ('threat_family_refs', value.threat_family_refs),
            ('scope_ref', value.scope_ref),
            ('population_refs', value.population_refs),
            ('basis_refs', value.basis_refs),
            ('witness', value.witness),
            ('contrary_input_refs', value.contrary_input_refs),
            ('reason_refs', value.reason_refs),
            ('result_refs', value.result_refs),
            ('statement', value.statement),
            ('interpretation_limit', value.interpretation_limit),
            ('native_records', value.native_records),
        )
    raise TypeError('invalid_private_representation')

def _paid_tuple(values, port):
    port.charge(len(values) + 1)
    return tuple(values)


def _key_charge(key, port):
    """Pay comparisons/hash passes over complete finite structural keys."""
    port.charge(1)
    if type(key) is str:
        _byte_work(port, 4 * len(key), 1)
    elif type(key) is tuple:
        for child in key:
            _key_charge(child, port)


def _key_sort(keys, port):
    """Stable bottom-up merge under prospective comparison/copy charges."""
    port.charge(len(keys) + 1)
    source = list(keys)
    width = 1
    while width < len(source):
        target = []
        for start in range(0, len(source), 2 * width):
            port.charge(5)
            middle = min(start + width, len(source))
            end = min(start + 2 * width, len(source))
            left, right = start, middle
            while left < middle or right < end:
                port.charge(4)
                if left < middle and right < end:
                    _key_charge(source[left], port)
                    _key_charge(source[right], port)
                    take_left = source[left] <= source[right]
                else:
                    take_left = left < middle
                if take_left:
                    target.append(source[left])
                    left += 1
                else:
                    target.append(source[right])
                    right += 1
        port.charge(2)
        source = target
        width *= 2
    return _paid_tuple(source, port)


def _semantic_key(value, port):
    """Full body identity; native source arrays retain their supplied order.

    Only project-owned immutable contract values are accepted. No arbitrary
    object properties, port identities, repr, hash callback or source code run.
    """
    port.charge(1)
    kind = type(value)
    if value is None:
        return ('null',)
    if kind is str:
        _byte_work(port, 4 * len(value), 2)
        return ('str', value)
    if kind is bool:
        return ('bool', value)
    if kind is int:
        _require(-9_007_199_254_740_991 <= value <= 9_007_199_254_740_991)
        port.charge(4)
        return ('int', value)
    if kind is tuple:
        return ('tuple', _paid_tuple([_semantic_key(part, port) for part in value], port))
    if kind is _Object:
        keys = []
        for name, child in value.items:
            port.charge(2)
            keys.append((_semantic_key(name, port), _semantic_key(child, port)))
        return ('object', _key_sort(keys, port))
    if kind is _Array:
        return ('array', _semantic_key(value.items, port))
    if kind is _Number:
        _byte_work(port, len(value.coefficient) + len(value.source_kind), 6)
        return ('number', value.sign, value.coefficient, value.exponent, value.source_kind)
    _require(kind in _DELIVERY_TYPES)
    tag, supplied = _delivery_parts(value, port)
    parts = []
    for name, child in supplied:
        port.charge(2)
        unordered = any(kind is owner and name in names for owner, names in _SET_FIELDS)
        if unordered:
            keys = [_semantic_key(part, port) for part in child]
            key = ('set', _key_sort(keys, port))
        else:
            key = _semantic_key(child, port)
        parts.append((name, key))
    port.charge(len(parts) + 2)
    return (tag, tuple(parts))


def _slot_key(ref, port):
    _charge_link(ref, port)
    key = ref._key()
    _key_charge(key, port)
    return key


def _coalesce_results(results, port):
    """Equal repeated inquiry slots coalesce; contradictory bodies fail."""
    rows, index, bodies = [], {}, {}
    _require(type(results) is tuple)
    for result in results:
        port.charge(3)
        _require(type(result) is _results._Result)
        key = _slot_key(result.ref, port)
        body = _semantic_key(result, port)
        # Some earlier owners retain execution order (PC02 before PC01).
        # Final navigation uses registry order while preserving each actual
        # check object and all of its original scope, state and evidence.
        port.charge(len(result.check_refs) * len(PREREQUISITES) + 2)
        ordered = tuple(check for name in PREREQUISITES for check in result.check_refs
                        if check.check_id == name)
        if ordered != result.check_refs:
            # The full prospective body pass above covers this immutable copy
            # and its constructor's linked representation checks.
            port.charge(16 + len(ordered))
            result = _replace(result, check_refs=ordered)
        _key_charge(key, port)
        if key in index:
            _key_charge(body, port)
            _key_charge(bodies[key], port)
            _require(body == bodies[key])
        else:
            port.charge(4)
            index[key], bodies[key] = result, body
            rows.append(result)
    return _paid_tuple(rows, port), index


def _selector_value(fields, selector, port):
    """Resolve inert field/role selectors against an admitted source record."""
    _byte_work(port, 4 * len(selector), len(selector) + 1)
    segments, start, depth = [], 0, 0
    for offset, char in enumerate(selector):
        port.charge(1)
        if char == '[':
            depth += 1
        elif char == ']':
            depth -= 1
            _require(depth >= 0)
        elif char == '.' and depth == 0:
            segments.append(selector[start:offset])
            start = offset + 1
    _require(depth == 0)
    segments.append(selector[start:])
    value = fields
    for segment in segments:
        port.charge(2)
        bracket = segment.find('[')
        name = segment if bracket < 0 else segment[:bracket]
        _require(type(value) is _Object)
        pair = _lookup_pair(value.items, name, port)
        _require(pair is not None)
        value = pair[1]
        if bracket < 0:
            continue
        _require(segment.endswith(']') and type(value) is _Array)
        selection = segment[bracket + 1:-1]
        if selection.isascii() and selection.isdecimal():
            _require(len(selection) <= 9)
            selected = int(selection)
            _require(selected < len(value.items))
            value = value.items[selected]
        else:
            conditions = selection.split(';')
            matches = []
            for candidate in value.items:
                port.charge(2)
                _require(type(candidate) is _Object)
                matched = True
                for condition in conditions:
                    _byte_work(port, 4 * len(condition), 2)
                    _require('=' in condition)
                    field, wanted = condition.split('=', 1)
                    pair = _lookup_pair(candidate.items, field, port)
                    matched = matched and pair is not None and pair[1] == wanted
                if matched:
                    matches.append(candidate)
            _require(len(matches) == 1)
            value = matches[0]
    return value


def _input_index(prepared, port):
    index = {}
    for entity in prepared.entities:
        port.charge(3)
        _byte_work(port, 4 * (len(entity.collection) + len(entity.identifier)), 2)
        key = (entity.collection, entity.identifier)
        _require(key not in index)
        index[key] = entity
    return index


def _resolve_input(ref, inputs, port):
    _charge_input_ref(ref, port)
    key = (ref.collection, ref.identifier)
    port.charge(2)
    _require(key in inputs)
    if ref.selector:
        _selector_value(inputs[key].node.fields, ref.selector, port)


def _walk_links(value, inputs, results, witnesses, port):
    """Resolve every typed private reference; strings stay inert source data."""
    port.charge(1)
    kind = type(value)
    if value is None or kind in (str, bool, int, _Number):
        _semantic_key(value, port)
        return
    if kind is _InputRef:
        _resolve_input(value, inputs, port)
        return
    if kind is _ResultRef:
        key = _slot_key(value, port)
        _require(key in results)
        _require(_semantic_key(value, port) == _semantic_key(results[key].ref, port))
        _walk_links(value.scope, inputs, results, witnesses, port)
        return
    if kind is _WitnessRef:
        key = _slot_key(value, port)
        _require(key in witnesses)
        original, unused_body, original_ref = witnesses[key]
        _require(_semantic_key(value, port) == _semantic_key(original_ref, port))
        _walk_links(value.scope, inputs, results, witnesses, port)
        _walk_links(value.anchor, inputs, results, witnesses, port)
        return
    if kind is _SourceAddress:
        port.charge(4)
        _resolve_input(_InputRef(value.collection, value.record_id, value.selector or None), inputs, port)
        return
    if kind is tuple:
        for part in value:
            _walk_links(part, inputs, results, witnesses, port)
        return
    if kind in (_Object, _Array):
        _charge_frozen(value, port)
        return
    _require(kind in _DELIVERY_TYPES)
    unused_tag, parts = _delivery_parts(value, port)
    for unused_name, part in parts:
        port.charge(1)
        _walk_links(part, inputs, results, witnesses, port)


def _dedup_links(links, port):
    rows, seen = [], set()
    for link in links:
        # Reason identity deliberately excludes affected_result_refs in the
        # earlier primitive. Navigation must retain distinct field bindings
        # instead of dropping the later reason with the same prose/scope key.
        key = _semantic_key(link, port) if type(link) is _Reason else _slot_key(link, port)
        _key_charge(key, port)
        port.charge(3)
        if key not in seen:
            seen.add(key)
            rows.append(link)
    return _paid_tuple(rows, port)


def _state_links(rows, port):
    states = ('available', 'unavailable', 'not_applicable', 'not_evaluated')
    groups = [[], [], [], []]
    for result in rows:
        port.charge(6)
        groups[states.index(result.result_state)].append(result.ref)
    return _paid_tuple([_paid_tuple(group, port) for group in groups], port)


def _assemble_analysis(prepared, plan, job_outcomes, results, findings, witnesses,
                       port, execution_state='completed'):
    """Paid pure assembly after owners finish; never resumes analytical work.

    Failure of any closure, whole-field or completed-check invariant rejects
    the entire private delivery. Runtime maps that defect to its fixed safe
    failed transport; this function cannot relabel it as an evidence gap.
    """
    port.check()
    port.charge(12)
    _require(type(prepared) is _PreparedBundle and type(plan) is _AnalyticalPlan)
    _require(type(job_outcomes) is tuple and len(job_outcomes) == len(plan.jobs))
    _require(type(findings) is tuple and type(witnesses) is tuple)
    _require(execution_state in ('completed', 'interrupted'))
    rows, result_index = _coalesce_results(results, port)
    inputs = _input_index(prepared, port)
    witness_index, retained_witnesses = {}, []
    for witness in witnesses:
        port.charge(2)
        _require(type(witness) is _WitnessRecord)
        body = _semantic_key((witness.payload, witness.input_refs, witness.member_count), port)
        unseen = False
        for ref in witness.refs:
            key = _slot_key(ref, port)
            port.charge(2)
            if key in witness_index:
                old, previous, unused_ref = witness_index[key]
                _key_charge(body, port)
                _key_charge(previous, port)
                _require(body == previous)
            else:
                witness_index[key] = (witness, body, ref)
                unseen = True
        if unseen:
            port.charge(1)
            retained_witnesses.append(witness)
    inquiries = []
    for entity in prepared.entities:
        port.charge(1)
        if entity.collection == 'inquiries':
            inquiries.append(entity.identifier)
    inquiries = _key_sort(inquiries, port)
    declared, represented, scheduled = set(), set(), {}
    for position, outcome in enumerate(job_outcomes):
        port.charge(5)
        _require(type(outcome) is _JobOutcome and outcome.job is plan.jobs[position])
        job = outcome.job
        _require(job.inquiry_ref in inquiries)
        key = _semantic_key((job.inquiry_ref, job.family, job.operation_key), port)
        _key_charge(key, port)
        _require(key not in declared)
        declared.add(key)
        slot = (job.inquiry_ref, job.family)
        if slot not in scheduled:
            scheduled[slot] = []
        scheduled[slot].append(outcome)
        fields = set()
        for ref in outcome.result_refs:
            rkey = _slot_key(ref, port)
            _require(rkey in result_index and ref.scope.inquiry_ref.identifier == job.inquiry_ref)
            result = result_index[rkey]
            represented.add(rkey)
            if ref.diagnostic_id == job.family:
                fields.add(ref.field_key)
            if outcome.execution_state == 'completed':
                _require(result.execution_state == 'completed')
            if outcome.execution_state == 'not_performed':
                _require(result.execution_state == 'not_performed')
        port.charge(len(fields) + len(job.field_keys) + 2)
        _require(fields == set(job.field_keys))
        if execution_state == 'completed':
            _require(outcome.execution_state == 'completed')
    port.charge(len(represented) + len(result_index) + 2)
    _require(represented == set(result_index))
    for result in rows:
        port.charge(2)
        checks = tuple(check.check_id for check in result.check_refs)
        port.charge(len(checks) * len(PREREQUISITES) + 1)
        _require(checks == tuple(key for key in PREREQUISITES if key in checks))
        if result.execution_state == 'completed':
            _require(all(key in checks for key in ('PC01', 'PC02', 'PC24')))
            _require(all(check.state == 'met' for check in result.check_refs
                         if check.check_id in ('PC01', 'PC24')))
        _walk_links(result, inputs, result_index, witness_index, port)
    for witness in retained_witnesses:
        _walk_links(witness, inputs, result_index, witness_index, port)
    for finding in findings:
        _require(type(finding) is _PrivateFinding)
        _walk_links(finding, inputs, result_index, witness_index, port)
    capabilities, domains = [], []
    for inquiry in inquiries:
        for family, unused_fields, questions, unused_domains in FAMILY_PREPARATION_BINDINGS:
            port.charge(5)
            _require((inquiry, family) in scheduled)
            selected = []
            for result in rows:
                port.charge(2)
                if (result.ref.scope.inquiry_ref.identifier == inquiry and
                        result.ref.diagnostic_id == family):
                    selected.append(result)
            _require(bool(selected))
            partitions = _state_links(selected, port)
            refs = _paid_tuple([result.ref for result in selected], port)
            checks, reasons = [], []
            for result in selected:
                port.charge(len(result.check_refs) + len(result.reason_refs) + 2)
                checks.extend(result.check_refs)
                reasons.extend(result.reason_refs)
            jobs = scheduled[(inquiry, family)]
            port.charge(len(jobs) * 3 + 6)
            state = ('completed' if all(job.execution_state == 'completed' for job in jobs)
                     else 'not_performed' if all(job.execution_state == 'not_performed' for job in jobs)
                     else 'interrupted')
            no_subject = any(job.no_subject for job in jobs)
            note = ('The finite structural plan includes a missing-subject scope; its explicit '
                    'non-results retain the actual limitation.' if no_subject else
                    'Every planned finite scope is linked separately; available values do not '
                    'upgrade unavailable or unfinished results in this family.')
            port.charge(18 + 2 * len(refs) + len(checks) + len(reasons))
            _byte_work(port, 4 * len(note), 1)
            capabilities.append(_Capability(inquiry, family, refs, *partitions,
                _dedup_links(checks, port), _dedup_links(reasons, port), questions, note, state))
        for level in range(5):
            selected = []
            for result in rows:
                port.charge(5)
                if result.ref.scope.inquiry_ref.identifier != inquiry:
                    continue
                binding = FAMILY_PREPARATION_BINDINGS[FAMILIES.index(result.ref.diagnostic_id)]
                if level in binding[3]:
                    selected.append(result)
            refs = _paid_tuple([result.ref for result in selected], port)
            reasons = []
            for result in selected:
                port.charge(len(result.reason_refs) + 1)
                reasons.extend(result.reason_refs)
            port.charge(12 + 2 * len(refs) + len(reasons))
            domains.append(_DomainOutcome(inquiry, level, refs, *_state_links(selected, port),
                                          _dedup_links(reasons, port)))
    port.charge(14 + len(job_outcomes) + len(rows) + len(findings) +
                len(retained_witnesses) + len(capabilities) + len(domains))
    result = _AnalyticalOutcome(prepared, plan, job_outcomes, rows, findings,
        _paid_tuple(retained_witnesses, port), _paid_tuple(capabilities, port),
        _paid_tuple(domains, port), execution_state)
    port.check()
    return result
