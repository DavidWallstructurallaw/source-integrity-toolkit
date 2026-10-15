# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: REPORT_CONTRACT.

Private preparation declarations and bounded analytical delivery contracts.
Public report types are declared; no audit execution or renderer is activated here.
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


# Phase 4 public representation declarations. Construction of a delivered report
# remains unavailable until one invocation has completed both encodings and
# their consistency check. The validation helpers below are private, bounded
# contract checks, not audit/renderer entry points or authenticity claims.
from typing import Mapping
import re

_REPORT_ROOT_FIELDS = (
    'contract_version', 'report_kind', 'report_id', 'run', 'input_identity',
    'input_validation', 'scopes', 'populations', 'basis_index', 'capabilities',
    'checks', 'observability_domains', 'results', 'findings', 'reasons',
    'release_limits',
)
_REPORT_RUN_QUALIFICATIONS = (
    'SIT-RP-0.1',
    'Wall-clock start and finish times are not recorded by SIT-RP-0.1.',
)
_REPORT_RELEASE_LIMITS = (
    'Offline analysis of caller-supplied records only.',
    'Source identity, authenticity and external events are not independently authenticated.',
    'No live monitoring or active content-level poisoning, injection or authorship detection was performed.',
    'No universal truth, integrity, independence or safety score is produced.',
    'No automatic intervention, source contact or changes to the audited system are performed.',
    'Scope-specific evidence gaps and qualifications remain as recorded; missing records do not establish outside-world absence.',
)


class _ReportContractError(TypeError):
    pass


def _report_require(ok):
    if not ok:
        raise _ReportContractError('invalid_report_contract')


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _ReportMapping(Mapping):
    """Project-owned immutable JSON object with no mutable backing mapping.

    Construction is private and receives only already copied immutable pairs.
    External keys cannot invoke a caller equality/hash/representation protocol.
    """
    _pairs: tuple

    def __len__(self):
        return len(self._pairs)

    def __iter__(self):
        return (pair[0] for pair in self._pairs)

    def __getitem__(self, key):
        if type(key) is not str:
            raise KeyError('unknown report member')
        for name, value in self._pairs:
            if name == key:
                return value
        raise KeyError('unknown report member')

    def __repr__(self):
        return '_ReportMapping()'


class AuditReport:
    """Read-only report interface; W02 cannot construct a completed audit.

    The future private completion owner must store only a frozen document and
    the two already complete immutable byte strings. No budget, source tree,
    prepared snapshot, private index or encoder is retained by this interface.
    """
    __slots__ = ('_document', '_json_bytes', '_markdown_bytes')

    def __new__(cls, *args, **kwargs):
        raise TypeError('AuditReport is delivered only by audit_bundle.')

    def __init_subclass__(cls, **kwargs):
        raise TypeError('AuditReport cannot be subclassed.')

    def __setattr__(self, name, value):
        raise TypeError('AuditReport is immutable.')

    def __delattr__(self, name):
        raise TypeError('AuditReport is immutable.')

    def __repr__(self):
        return 'AuditReport()'

    def to_json_bytes(self):
        return self._json_bytes

    def to_markdown_bytes(self):
        return self._markdown_bytes

    @property
    def contract_version(self):
        return self._document['contract_version']

    @property
    def report_kind(self):
        return self._document['report_kind']

    @property
    def report_id(self):
        return self._document['report_id']

    @property
    def run(self):
        return self._document['run']

    @property
    def input_identity(self):
        return self._document['input_identity']

    @property
    def input_validation(self):
        return self._document['input_validation']

    @property
    def scopes(self):
        return self._document['scopes']

    @property
    def populations(self):
        return self._document['populations']

    @property
    def basis_index(self):
        return self._document['basis_index']

    @property
    def capabilities(self):
        return self._document['capabilities']

    @property
    def checks(self):
        return self._document['checks']

    @property
    def observability_domains(self):
        return self._document['observability_domains']

    @property
    def results(self):
        return self._document['results']

    @property
    def findings(self):
        return self._document['findings']

    @property
    def reasons(self):
        return self._document['reasons']

    @property
    def release_limits(self):
        return self._document['release_limits']


def _report_text_work(value, port):
    """Conservative UTF-8 work, paid before scalar inspection in <=64-char blocks."""
    _report_require(type(value) is str)
    for start in range(0, len(value), 64):
        port.charge(2)
        for char in value[start:start + 64]:
            if 0xD800 <= ord(char) <= 0xDFFF:
                raise _ReportContractError('invalid_report_contract')
    port.check()


def _copy_report_value(value, port):
    """Explicit-stack private capture; aliases are copied as separate occurrences.

    Exact-type checks precede every protocol-sensitive operation. Active
    ancestry detects cycles without hashing/comparing caller objects. Each
    creation, traversal, comparison and copying pass is prospectively charged.
    """
    result = []
    stack = [('visit', value, result)]
    active = set()
    while stack:
        port.charge(1)
        operation, current, destination = stack.pop()
        if operation == 'object':
            pairs, source_id = current
            port.charge(1 + 2 * len(pairs))
            destination.append(_ReportMapping(tuple((key, child[0]) for key, child in pairs)))
            active.remove(source_id)
            continue
        if operation == 'array':
            children, source_id = current
            port.charge(1 + len(children))
            destination.append(tuple(child[0] for child in children))
            active.remove(source_id)
            continue
        kind = type(current)
        _report_require(current is None or kind is str or kind is bool or
                        kind is int or kind is dict or kind is list)
        if kind is str:
            _report_text_work(current, port)
            port.charge(1)
            destination.append(current)
        elif kind is int:
            port.charge(3)
            _report_require(-9007199254740991 <= current <= 9007199254740991)
            destination.append(current)
        elif current is None or kind is bool:
            port.charge(1)
            destination.append(current)
        else:
            port.charge(2)
            source_id = id(current)
            _report_require(source_id not in active)
            active.add(source_id)
            size = len(current)
            port.charge(1 + 3 * size)
            if kind is dict:
                # items() on an exact dict retrieves entries without hashing
                # its untrusted keys; all key types precede any comparison.
                source_pairs = tuple(current.items())
                _report_require(len(source_pairs) == size)
                pairs = []
                for key, child in source_pairs:
                    port.charge(2)
                    _report_require(type(key) is str)
                    _report_text_work(key, port)
                    pairs.append((key, []))
                stack.append(('object', (pairs, source_id), destination))
                for position in range(size - 1, -1, -1):
                    port.charge(2)
                    stack.append(('visit', source_pairs[position][1], pairs[position][1]))
            else:
                children = [[] for unused in range(size)]
                stack.append(('array', (children, source_id), destination))
                for position in range(size - 1, -1, -1):
                    port.charge(2)
                    stack.append(('visit', current[position], children[position]))
    port.check()
    _report_require(len(result) == 1)
    return result[0]


def _report_key(value, port):
    """Paid equality key for already frozen values; never a source fingerprint."""
    port.charge(1)
    if type(value) is _ReportMapping:
        pairs = []
        for name, child in value._pairs:
            _byte_work(port, 4 * len(name), 3)
            pairs.append((name, _report_key(child, port)))
        return ('object', _key_sort(pairs, port))
    if type(value) is tuple:
        return ('array', _paid_tuple([_report_key(child, port) for child in value], port))
    return _semantic_key(value, port)


def _report_equal(left, right, port):
    """Iterative comparison of copied values; no recursion on rejected input."""
    if type(right) is dict or type(right) is list:
        right = _copy_report_value(right, port)
    pending = [(left, right)]
    while pending:
        port.charge(1)
        a, b = pending.pop()
        if type(a) is not type(b):
            return False
        if type(a) is _ReportMapping:
            aa, bb = _report_fields(a, port), _report_fields(b, port)
            port.charge(1)
            if len(aa) != len(bb):
                return False
            for name, child in aa.items():
                _byte_work(port, 4 * len(name), 3)
                if name not in bb:
                    return False
                pending.append((child, bb[name]))
        elif type(a) is tuple:
            port.charge(1)
            if len(a) != len(b):
                return False
            port.charge(2 * len(a))
            pending.extend(zip(a, b))
        else:
            if type(a) is str:
                _byte_work(port, 4 * (len(a) + len(b)), 1)
            else:
                port.charge(1)
            if a != b:
                return False
    port.check()
    return True


def _report_fields(value, port):
    _report_require(type(value) is _ReportMapping)
    fields = {}
    for key, child in value._pairs:
        _byte_work(port, 4 * len(key), 3)
        fields[key] = child
    port.check()
    return fields


def _report_unique(values, port):
    """Merge-sort every complete key, charging moves and comparisons."""
    keys = _key_sort([_report_key(value, port) for value in values], port)
    for position in range(1, len(keys)):
        port.charge(1)
        _key_charge(keys[position - 1], port)
        _key_charge(keys[position], port)
        _report_require(keys[position - 1] != keys[position])


def _report_type(value, kind):
    return ((kind == 'object' and type(value) is _ReportMapping) or
            (kind == 'array' and type(value) is tuple) or
            (kind == 'string' and type(value) is str) or
            (kind == 'integer' and type(value) is int) or
            (kind == 'number' and type(value) is int) or
            (kind == 'boolean' and type(value) is bool) or
            (kind == 'null' and value is None))


def _report_matches(value, specification, port):
    try:
        _report_schema(value, specification, port)
    except _ReportContractError:
        return False
    return True


def _report_schema(value, specification, port):
    """Interpret only the compiled local report grammar, never supplied schemas.

    This private fixed-contract walker accepts only the keyword subset used in
    the pinned report declaration. Every alternative, scalar scan, member
    examination and collection comparison consumes the caller's existing port.
    """
    port.charge(1)
    if specification is False:
        _report_require(False)
    if specification is True:
        return
    if '$ref' in specification:
        reference = specification['$ref']
        name = reference.removeprefix('#/$defs/')
        _report_require(reference.startswith('#/$defs/') and name in _REPORT_SHAPES)
        _report_shape(value, name, port)
    if 'type' in specification:
        kinds = specification['type']
        kinds = (kinds,) if type(kinds) is str else kinds
        port.charge(len(kinds))
        _report_require(any(_report_type(value, kind) for kind in kinds))
    if 'const' in specification:
        _report_require(_report_equal(value, specification['const'], port))
    if 'enum' in specification:
        matched = False
        for choice in specification['enum']:
            port.charge(1)
            if _report_equal(value, choice, port):
                matched = True
                break
        _report_require(matched)
    for key in ('allOf', 'anyOf', 'oneOf'):
        if key in specification:
            successes = 0
            for branch in specification[key]:
                port.charge(1)
                successes += int(_report_matches(value, branch, port))
            _report_require(successes == len(specification[key]) if key == 'allOf' else
                            successes >= 1 if key == 'anyOf' else successes == 1)
    if 'not' in specification:
        _report_require(not _report_matches(value, specification['not'], port))
    if 'if' in specification:
        which = 'then' if _report_matches(value, specification['if'], port) else 'else'
        if which in specification:
            _report_schema(value, specification[which], port)
    if type(value) is str:
        _report_text_work(value, port)
        _report_require(len(value) >= specification.get('minLength', 0))
        if 'maxLength' in specification:
            _report_require(len(value) <= specification['maxLength'])
        if 'pattern' in specification:
            _byte_work(port, 4 * len(value), 2)
            matched = re.search(specification['pattern'], value)
            port.check()
            _report_require(matched is not None)
    elif type(value) is int:
        port.charge(4)
        if 'minimum' in specification:
            _report_require(value >= specification['minimum'])
        if 'maximum' in specification:
            _report_require(value <= specification['maximum'])
        if 'exclusiveMinimum' in specification:
            _report_require(value > specification['exclusiveMinimum'])
        if 'exclusiveMaximum' in specification:
            _report_require(value < specification['exclusiveMaximum'])
    elif type(value) is tuple:
        port.charge(2)
        _report_require(len(value) >= specification.get('minItems', 0))
        if 'maxItems' in specification:
            _report_require(len(value) <= specification['maxItems'])
        prefix = specification.get('prefixItems', ())
        for position, child in enumerate(value):
            port.charge(1)
            if position < len(prefix):
                _report_schema(child, prefix[position], port)
            elif 'items' in specification:
                _report_schema(child, specification['items'], port)
        if specification.get('uniqueItems') is True:
            _report_unique(value, port)
        if 'contains' in specification:
            matches = 0
            for child in value:
                port.charge(1)
                matches += int(_report_matches(child, specification['contains'], port))
            _report_require(matches >= specification.get('minContains', 1))
            if 'maxContains' in specification:
                _report_require(matches <= specification['maxContains'])
    elif type(value) is _ReportMapping:
        fields = _report_fields(value, port)
        _report_require(len(fields) >= specification.get('minProperties', 0))
        if 'maxProperties' in specification:
            _report_require(len(fields) <= specification['maxProperties'])
        for name in specification.get('required', ()):
            port.charge(1)
            _report_require(name in fields)
        properties = specification.get('properties', {})
        for name, child in fields.items():
            _byte_work(port, 4 * len(name), 2)
            if 'propertyNames' in specification:
                _report_schema(name, specification['propertyNames'], port)
            if name in properties:
                _report_schema(child, properties[name], port)
            elif 'additionalProperties' in specification:
                _report_schema(child, specification['additionalProperties'], port)
        for name, required in specification.get('dependentRequired', {}).items():
            port.charge(1)
            if name in fields:
                for member in required:
                    port.charge(1)
                    _report_require(member in fields)
    port.check()


def _report_shape(value, shape, port):
    _report_require(type(shape) is str)
    _report_require(shape in _REPORT_SHAPES)
    _report_schema(value, _REPORT_SHAPES[shape], port)
    _report_semantics(value, shape, port)


def _validate_report_component(value, shape, port):
    """Validate one fixed private construction component without delivering it."""
    _report_require(type(shape) is str)
    _byte_work(port, 4 * len(shape), 1)
    _report_require(shape in _REPORT_SHAPES)
    frozen = _copy_report_value(value, port)
    _report_shape(frozen, shape, port)
    port.check()


def _freeze_report_document(document, port):
    """Check and detach a logical document, not a finished AuditReport.

    A successful result contains only immutable, project-owned mappings,
    tuples and exact permitted scalar values. It contains no input-owned
    container, execution port or encoding claim. No public constructor uses
    this seam; later assembly must additionally close all references and
    complete both encoded siblings before an AuditReport can be delivered.
    """
    _report_require(type(document) is dict)
    frozen = _copy_report_value(document, port)
    _report_shape(frozen, 'AuditReport', port)
    port.check()
    return frozen


def _validate_report_document(document, port):
    _freeze_report_document(document, port)


# These local relations are compiled from reporting 16 and the already frozen
# private result contracts. They validate representations, not source facts.
from .results import PARTITION_BINDINGS, IMMEDIATE_DISPOSITIONS, STAGE_DISPOSITIONS


def _report_same_members(left, right, port):
    """Compare finite multisets with paid complete keys; source order is intact."""
    a = _key_sort([_report_key(item, port) for item in left], port)
    b = _key_sort([_report_key(item, port) for item in right], port)
    _key_charge(a, port)
    _key_charge(b, port)
    return a == b


def _report_join(groups, port):
    combined = []
    for group in groups:
        port.charge(len(group) + 1)
        combined.extend(group)
    return _paid_tuple(combined, port)


def _report_time(fields, port):
    if fields['state'] != 'known':
        return
    value = fields['value']
    _byte_work(port, 4 * len(value), 4)
    if fields['precision'] == 'date':
        matched = re.fullmatch(r'([0-9]{4})-([0-9]{2})-([0-9]{2})', value)
    else:
        matched = re.fullmatch(
            r'([0-9]{4})-([0-9]{2})-([0-9]{2})T([0-9]{2}):([0-9]{2}):([0-9]{2})'
            r'(?:\.[0-9]+)?(Z|[+-][0-9]{2}:[0-9]{2})', value)
    port.check()
    _report_require(matched is not None)
    port.charge(24)
    year, month, day = int(matched[1]), int(matched[2]), int(matched[3])
    _report_require(1 <= year <= 9999 and 1 <= month <= 12)
    leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    days = (31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    _report_require(1 <= day <= days[month - 1])
    if fields['precision'] == 'instant':
        _report_require(int(matched[4]) <= 23 and int(matched[5]) <= 59 and int(matched[6]) <= 59)
        offset = matched[7]
        if offset != 'Z':
            _report_require(int(offset[1:3]) <= 23 and int(offset[4:6]) <= 59)
    port.check()


def _report_partition(fields, port):
    categories = fields['categories']
    _report_require(bool(categories))
    labels, groups, total = [], [], 0
    for category in categories:
        row = _report_fields(category, port)
        port.charge(4)
        labels.append(row['label'])
        groups.append(row['member_refs'])
        total += row['count']
        _report_require(total <= 9007199254740991)
    _report_unique(labels, port)
    members = _report_join(groups, port)
    _report_unique(members, port)
    port.charge(2)
    _report_require(total == fields['total'] == len(members))


def _report_interval(fields, port):
    lower = _report_fields(fields['lower'], port)
    upper = _report_fields(fields['upper'], port)
    partition = _report_fields(fields['partition'], port)
    _report_require(_report_equal(fields['population_ref'], partition['population_ref'], port))
    port.charge(5)
    _report_require(lower['denominator'] == upper['denominator'] == partition['total'])
    _report_require(lower['numerator'] <= upper['numerator'] <= lower['denominator'])
    expected = (IMMEDIATE_DISPOSITIONS if fields['interval_kind'] == 'finite_record_completion'
                else STAGE_DISPOSITIONS)
    counts = {}
    for category in partition['categories']:
        row = _report_fields(category, port)
        _byte_work(port, 4 * len(row['label']), 2)
        counts[row['label']] = row['count']
    _report_require(_report_same_members(tuple(counts), expected, port))
    port.charge(6)
    if fields['interval_kind'] == 'finite_record_completion':
        positive, unresolved = counts['inherited_only_at_evidence_layer'], counts['unresolved_at_evidence_layer']
    else:
        positive, unresolved = counts['Y'], counts['U']
    _report_require(unresolved > 0 and lower['numerator'] == positive and
                    upper['numerator'] == positive + unresolved)


def _report_incidence(fields, port):
    members, declared_origins, expected_pairs, declared_pairs = [], [], [], []
    for membership in fields['memberships']:
        row = _report_fields(membership, port)
        port.charge(2)
        members.append(row['member_ref'])
        for origin in row['origin_refs']:
            port.charge(2)
            expected_pairs.append((row['member_ref'], origin))
    _report_unique(members, port)
    for origin_count in fields['origin_counts']:
        row = _report_fields(origin_count, port)
        port.charge(2)
        declared_origins.append(row['origin_ref'])
        _report_require(row['count'] > 0)
        for member in row['member_refs']:
            port.charge(2)
            declared_pairs.append((member, row['origin_ref']))
    _report_unique(declared_origins, port)
    _report_require(_report_same_members(expected_pairs, declared_pairs, port))
    port.charge(1)
    _report_require(fields['total'] == len(members))


def _report_result(fields, port):
    port.charge(2)
    if fields['result_state'] != 'available':
        _report_require(bool(fields['reason_refs']))
        return
    kind = fields['value_kind']
    if kind in ('count', 'fraction', 'completion_interval', 'partition', 'incidence'):
        _report_require(bool(fields['population_refs']))
    if kind == 'witness_collection':
        collection = _report_fields(fields['value'], port)
        _report_require(_report_same_members(collection['witness_refs'], fields['witness_refs'], port))
    if kind == 'fraction':
        ratio = _report_fields(fields['value'], port)
        port.charge(1)
        _report_require(ratio['numerator'] <= ratio['denominator'])
    if kind not in ('completion_interval', 'partition', 'incidence'):
        return
    value = _report_fields(fields['value'], port)
    _report_require(any(_report_equal(value['population_ref'], item, port)
                        for item in fields['population_refs']))
    if kind == 'partition':
        labels = []
        for category in value['categories']:
            row = _report_fields(category, port)
            port.charge(1)
            labels.append(row['label'])
        for field, expected in PARTITION_BINDINGS:
            _byte_work(port, 4 * (len(field) + len(fields['field_key'])), 1)
            if fields['field_key'] == field:
                _report_require(_report_same_members(labels, expected, port))
                break
    elif kind == 'completion_interval':
        expected = ('finite_record_completion' if fields['diagnostic_id'] == 'SIT-M006'
                    else 'finite_cohort_completion')
        _report_require(_report_equal(value['interval_kind'], expected, port))


def _report_root(fields, port):
    # This is local envelope consistency. W03 separately resolves source IDs,
    # every foreign key, scope joins, completed cells and actual source facts.
    identifiers = []
    for name in ('scopes', 'populations', 'basis_index', 'capabilities', 'checks',
                 'results', 'findings', 'reasons'):
        for item in fields[name]:
            row = _report_fields(item, port)
            port.charge(1)
            identifiers.append(row['id'])
    _report_unique(identifiers, port)
    run = _report_fields(fields['run'], port)
    if fields['report_kind'] == 'audit_report':
        domains = []
        for domain in fields['observability_domains']:
            row = _report_fields(domain, port)
            port.charge(1)
            domains.append(row['level_index'])
        _report_require(_report_equal(tuple(domains), (0, 1, 2, 3, 4), port))
        if run['processing_state'] == 'completed':
            _report_require(_report_equal(run['completed_diagnostic_ids'], FAMILIES, port))
        for reason in fields['reasons']:
            row = _report_fields(reason, port)
            _report_require(row['scope_ref'] is not None)
    else:
        _report_require(not run['completed_diagnostic_ids'])
        for reason in fields['reasons']:
            row = _report_fields(reason, port)
            _report_require(row['scope_ref'] is None and not row['affected_result_refs'] and
                            not row['input_refs'] and row['classification'] == 'execution')
            _report_require(row['code'] in ('resource_limit_reached', 'execution_failed', 'input_not_accepted'))
            port.charge(3)
            if row['code'] == 'resource_limit_reached':
                _report_require(run['processing_state'] == 'interrupted')
            elif row['code'] == 'execution_failed':
                _report_require(run['processing_state'] == 'failed')
            else:
                validation = _report_fields(fields['input_validation'], port)
                _report_require(validation['state'] != 'accepted')


def _report_semantics(value, shape, port):
    """Validate finite local relations after their exact closed shape passes.

    No input lookup, graph search, analysis, rendering, ID allocation or public
    report construction occurs here. Every scan receives the current port.
    """
    port.charge(1)
    if shape == 'Identifier':
        _report_require(len(value) <= 128)
        return
    if type(value) is not _ReportMapping:
        return
    fields = _report_fields(value, port)
    if shape == 'TimeValue':
        _report_time(fields, port)
    elif shape == 'Run':
        _report_require(_report_equal(fields['requested_diagnostic_ids'], FAMILIES, port))
        previous = -1
        for family in fields['completed_diagnostic_ids']:
            port.charge(16)
            index = FAMILIES.index(family)
            _report_require(index > previous)
            previous = index
    elif shape == 'InputIdentity':
        if fields['source_mode'] == 'in_process' or fields['bundle_id'] is None or fields['snapshot_id'] is None:
            _report_require(bool(fields['qualifications']))
    elif shape == 'Diagnostic':
        if fields['code'] == 'input_constraint_violation':
            port.charge(len(fields['qualifications']) + 1)
            _report_require(bool(fields['qualifications']) and any(fields['qualifications']))
    elif shape == 'Scope':
        inquiry = _report_fields(fields['inquiry_ref'], port)
        _report_require(inquiry['selector'] is None)
        for claim in fields['claim_refs']:
            reference = _report_fields(claim, port)
            _report_require(reference['selector'] is None)
        if not fields['claim_refs'] or fields['dependency_dimension'] is None or fields['graph_view'] is None:
            _report_require(bool(fields['qualifications']))
    elif shape == 'Reason' and fields['scope_ref'] is None:
        _report_require(fields['classification'] == 'execution' and
                        not fields['affected_result_refs'] and not fields['input_refs'])
        _report_require(fields['code'] in ('resource_limit_reached', 'execution_failed', 'input_not_accepted'))
    elif shape == 'PartitionCategory' or shape == 'OriginIncidenceCount':
        port.charge(1)
        _report_require(fields['count'] == len(fields['member_refs']))
    elif shape == 'Partition':
        _report_partition(fields, port)
    elif shape == 'CompletionInterval':
        _report_interval(fields, port)
    elif shape == 'Incidence':
        _report_incidence(fields, port)
    elif shape == 'Capability':
        inquiry = _report_fields(fields['inquiry_ref'], port)
        _report_require(inquiry['selector'] is None)
        parts = _report_join((fields['available_result_refs'], fields['unavailable_result_refs'],
                              fields['not_applicable_result_refs'], fields['not_evaluated_result_refs']), port)
        _report_unique(parts, port)
        _report_require(_report_same_members(parts, fields['result_refs'], port))
    elif shape == 'ObservabilityDomain':
        parts = _report_join((fields['available_result_refs'], fields['unavailable_result_refs'],
                              fields['not_evaluated_result_refs']), port)
        _report_unique(parts, port)
    elif shape == 'Result':
        _report_result(fields, port)
    elif shape == 'GraphNode':
        reference = _report_fields(fields['ref'], port)
        _report_require(reference['selector'] is None)
        if reference['collection'] == 'records':
            _report_require(fields['kind'] not in ('inquiry', 'assertion', 'evidence_reference'))
        else:
            expected = {'inquiries': 'inquiry', 'assertions': 'assertion',
                        'evidence_references': 'evidence_reference'}
            _report_require(_report_equal(fields['kind'], expected[reference['collection']], port))
    elif shape == 'GraphEdge':
        reference = _report_fields(fields['source_ref'], port)
        if fields['predicate'] is not None:
            _report_require(reference['collection'] == 'assertions' and reference['selector'] is None)
        else:
            source = _report_fields(fields['source'], port)
            source_ref = _report_fields(source['ref'], port)
            _report_require(reference['selector'] is not None)
            _report_require(_report_equal(reference['collection'], source_ref['collection'], port))
            _report_require(_report_equal(reference['identifier'], source_ref['identifier'], port))
    elif shape in ('InventoryWitnessComponent', 'ComparisonWitnessComponent', 'SelectedMembersComponent',
                   'HumanReviewWitnessComponent', 'CorrectionOutcomeWitnessComponent'):
        port.charge(5)
        count = len(fields['members'])
        if shape in ('ComparisonWitnessComponent', 'HumanReviewWitnessComponent'):
            count += len(fields['examined_assessments'])
        if shape in ('HumanReviewWitnessComponent', 'CorrectionOutcomeWitnessComponent'):
            count += len(fields['source_refs'])
        _report_require(fields['member_count'] == count)
    elif shape == 'GraphWitnessComponent':
        count = int(fields['target'] is not None)
        for name in ('nodes', 'members', 'starts', 'examined_nodes', 'frontiers', 'terminals',
                     'edges', 'internal_edges', 'exit_edges', 'examined_edges', 'observations'):
            port.charge(2)
            count += len(fields[name])
        _report_require(fields['member_count'] == count)
    elif shape == 'AuditReport':
        _report_root(fields, port)
    port.check()


# Fixed SIT-RP-0.1 grammar, authored alongside schemas/report/sit-report-0.1.schema.json.
# This declaration is inert data. Runtime never locates, reads or evaluates a schema file.
_REPORT_SHAPES = {
    'Identifier': {'type': 'string', 'minLength': 1, 'pattern': '^[A-Za-z0-9][A-Za-z0-9._:-]*$', 'not': {'pattern': '[^A-Za-z0-9._:-]'}, 'maxLength': 128},
    'TimeValue': {'type': 'object', 'properties': {'state': {'$ref': '#/$defs/enum_time_state'}, 'value': {'anyOf': [{'type': 'string'}, {'type': 'null'}]}, 'precision': {'anyOf': [{'$ref': '#/$defs/enum_precision'}, {'type': 'null'}]}, 'reason': {'type': 'string'}}, 'additionalProperties': False, 'required': ['state', 'value', 'precision'], 'allOf': [{'if': {'required': ['state'], 'properties': {'state': {'const': 'known'}}}, 'then': {'properties': {'value': {'type': 'string'}, 'precision': {'$ref': '#/$defs/enum_precision'}}}, 'else': {'required': ['reason'], 'properties': {'value': {'type': 'null'}, 'precision': {'type': 'null'}, 'reason': {'type': 'string', 'minLength': 1}}}}]},
    'TimeWindow': {'type': 'object', 'properties': {'start': {'$ref': '#/$defs/TimeValue'}, 'end': {'$ref': '#/$defs/TimeValue'}, 'note': {'type': 'string'}}, 'additionalProperties': False, 'required': ['start', 'end']},
    'Predecessor': {'type': 'object', 'properties': {'bundle_id': {'$ref': '#/$defs/Identifier'}, 'snapshot_id': {'$ref': '#/$defs/Identifier'}}, 'additionalProperties': False, 'required': ['bundle_id', 'snapshot_id']},
    'enum_time_state': {'type': 'string', 'enum': ['known', 'unknown', 'withheld', 'not_applicable']},
    'enum_precision': {'type': 'string', 'enum': ['date', 'instant']},
    'DiagnosticId': {'type': 'string', 'enum': ['SIT-M001', 'SIT-M002', 'SIT-M003', 'SIT-M004', 'SIT-M005', 'SIT-M006', 'SIT-M007', 'SIT-M008', 'SIT-M009', 'SIT-M010', 'SIT-M011', 'SIT-M012', 'SIT-M013', 'SIT-M014', 'SIT-M015']},
    'ReasonCode': {'type': 'string', 'enum': ['no_seed_contributions', 'zero_denominator', 'missing_comparison_assessment', 'scope_unestablished', 'dimension_not_selected', 'unknown_endpoint', 'upstream_coverage_incomplete', 'unqualified_origin_boundary', 'baseline_or_scope_cut', 'declared_origin_only', 'multi_origin_unallocated', 'identity_unresolved', 'premise_disputed', 'lineage_cycle', 'support_uninspectable', 'documentary_basis_incomplete', 'self_supporting_assurance', 'time_applicability_unknown', 'temporal_inconsistency', 'roles_incomplete', 'externality_unestablished', 'cohort_anchor_missing', 'cohort_anchor_ambiguous', 'cohort_universe_unestablished', 'stage_classification_unresolved', 'transition_baseline_unestablished', 'route_not_recorded', 'authority_unestablished', 'authority_inapplicable', 'change_evidence_missing', 'before_after_unresolved', 'context_withheld_or_unavailable', 'no_applicable_subject', 'outside_v01', 'analysis_not_selected', 'resource_limit_reached', 'execution_failed', 'input_not_accepted', 'completion_interval_not_needed', 'comparison_scope_mismatch']},
    'ResultOrigin': {'type': 'string', 'enum': ['inventory', 'graph_derivation', 'attributed_record', 'qualification_check']},
    'ValueKind': {'type': 'string', 'enum': ['count', 'fraction', 'completion_interval', 'partition', 'incidence', 'record_disclosures', 'witness_collection']},
    'CheckState': {'type': 'string', 'enum': ['met', 'unmet', 'unknown', 'not_applicable']},
    'ReasonClassification': {'type': 'string', 'enum': ['evidence_gap', 'conflict', 'structural_inapplicability', 'release_boundary', 'execution']},
    'DependencyDimension': {'type': 'string', 'enum': ['acquisition', 'analytical_method', 'model_ancestry', 'evaluation_rubric', 'organizational_control']},
    'GraphView': {'type': 'string', 'enum': ['citation', 'material_transformation', 'claim_origin', 'model_evaluation', 'organizational', 'stance_contestation', 'correction_routing', 'correction_outcomes', 'pipeline_stages', 'assertion_assurance', 'succession']},
    'PopulationUnit': {'type': 'string', 'enum': ['artifact_record', 'locator', 'actor_record', 'evidence_item', 'origin_event', 'relation_assertion', 'witness_path', 'comparison_member', 'unresolved_reference', 'frontier_occurrence', 'evaluation', 'correction_case', 'correction_change_record', 'pipeline_record', 'pipeline_member', 'case_target', 'record', 'evidence_reference', 'family_label', 'handling_event']},
    'BasisKind': {'type': 'string', 'enum': ['declaration', 'documented_record', 'upstream_inference', 'protected_attestation', 'unspecified']},
    'Availability': {'type': 'string', 'enum': ['supplied', 'locator_only', 'withheld', 'unavailable']},
    'ScopeId': {'type': 'string', 'pattern': '^SIT-SCP-[0-9]{6,}$', 'not': {'anyOf': [{'pattern': '[^A-Z0-9-]'}, {'pattern': '^SIT-SCP-0+$'}]}},
    'PopulationId': {'type': 'string', 'pattern': '^SIT-POP-[0-9]{6,}$', 'not': {'anyOf': [{'pattern': '[^A-Z0-9-]'}, {'pattern': '^SIT-POP-0+$'}]}},
    'BasisId': {'type': 'string', 'pattern': '^SIT-BAS-[0-9]{6,}$', 'not': {'anyOf': [{'pattern': '[^A-Z0-9-]'}, {'pattern': '^SIT-BAS-0+$'}]}},
    'CapabilityId': {'type': 'string', 'pattern': '^SIT-CAP-[0-9]{6,}$', 'not': {'anyOf': [{'pattern': '[^A-Z0-9-]'}, {'pattern': '^SIT-CAP-0+$'}]}},
    'CheckId': {'type': 'string', 'pattern': '^SIT-CHK-[0-9]{6,}$', 'not': {'anyOf': [{'pattern': '[^A-Z0-9-]'}, {'pattern': '^SIT-CHK-0+$'}]}},
    'ResultId': {'type': 'string', 'pattern': '^SIT-RES-[0-9]{6,}$', 'not': {'anyOf': [{'pattern': '[^A-Z0-9-]'}, {'pattern': '^SIT-RES-0+$'}]}},
    'FindingId': {'type': 'string', 'pattern': '^SIT-FND-[0-9]{6,}$', 'not': {'anyOf': [{'pattern': '[^A-Z0-9-]'}, {'pattern': '^SIT-FND-0+$'}]}},
    'ReasonId': {'type': 'string', 'pattern': '^SIT-RSN-[0-9]{6,}$', 'not': {'anyOf': [{'pattern': '[^A-Z0-9-]'}, {'pattern': '^SIT-RSN-0+$'}]}},
    'InputRef': {'type': 'object', 'properties': {'collection': {'type': 'string', 'enum': ['inquiries', 'records', 'assertions', 'evidence_references']}, 'identifier': {'$ref': '#/$defs/Identifier'}, 'selector': {'anyOf': [{'type': 'string', 'minLength': 1}, {'type': 'null'}]}}, 'additionalProperties': False, 'required': ['collection', 'identifier', 'selector']},
    'InquiryRef': {'allOf': [{'$ref': '#/$defs/InputRef'}, {'properties': {'collection': {'const': 'inquiries'}}}]},
    'RecordRef': {'allOf': [{'$ref': '#/$defs/InputRef'}, {'properties': {'collection': {'const': 'records'}}}]},
    'AssertionRef': {'allOf': [{'$ref': '#/$defs/InputRef'}, {'properties': {'collection': {'const': 'assertions'}}}]},
    'EvidenceRef': {'allOf': [{'$ref': '#/$defs/InputRef'}, {'properties': {'collection': {'const': 'evidence_references'}}}]},
    'CaseTarget': {'type': 'object', 'properties': {'case_ref': {'$ref': '#/$defs/RecordRef'}, 'before_ref': {'anyOf': [{'$ref': '#/$defs/RecordRef'}, {'$ref': '#/$defs/AssertionRef'}]}}, 'additionalProperties': False, 'required': ['case_ref', 'before_ref']},
    'PopulationMember': {'anyOf': [{'$ref': '#/$defs/InputRef'}, {'$ref': '#/$defs/CaseTarget'}]},
    'Scope': {'type': 'object', 'properties': {'id': {'$ref': '#/$defs/ScopeId'}, 'inquiry_ref': {'allOf': [{'$ref': '#/$defs/InquiryRef'}, {'properties': {'selector': {'type': 'null'}}}]}, 'claim_refs': {'type': 'array', 'items': {'allOf': [{'$ref': '#/$defs/RecordRef'}, {'properties': {'selector': {'type': 'null'}}}]}, 'uniqueItems': True}, 'target_refs': {'type': 'array', 'items': {'$ref': '#/$defs/InputRef'}, 'uniqueItems': True}, 'dependency_dimension': {'anyOf': [{'$ref': '#/$defs/DependencyDimension'}, {'type': 'null'}]}, 'graph_view': {'anyOf': [{'$ref': '#/$defs/GraphView'}, {'type': 'null'}]}, 'temporal_basis': {'type': 'string', 'enum': ['snapshot_structural', 'time_specific']}, 'requested_time': {'anyOf': [{'$ref': '#/$defs/TimeValue'}, {'type': 'null'}]}, 'coverage_refs': {'type': 'array', 'items': {'$ref': '#/$defs/AssertionRef'}, 'uniqueItems': True}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['id', 'inquiry_ref', 'claim_refs', 'target_refs', 'dependency_dimension', 'graph_view', 'temporal_basis', 'requested_time', 'coverage_refs', 'qualifications'], 'allOf': [{'if': {'required': ['temporal_basis'], 'properties': {'temporal_basis': {'const': 'time_specific'}}}, 'then': {'properties': {'requested_time': {'$ref': '#/$defs/TimeValue'}}}}]},
    'Population': {'type': 'object', 'properties': {'id': {'$ref': '#/$defs/PopulationId'}, 'scope_ref': {'$ref': '#/$defs/ScopeId'}, 'unit': {'$ref': '#/$defs/PopulationUnit'}, 'member_refs': {'type': 'array', 'items': {'$ref': '#/$defs/PopulationMember'}, 'uniqueItems': True}, 'selection_rule': {'type': 'string', 'minLength': 1}, 'coverage_refs': {'type': 'array', 'items': {'$ref': '#/$defs/AssertionRef'}, 'uniqueItems': True}, 'basis_refs': {'type': 'array', 'items': {'$ref': '#/$defs/BasisId'}, 'uniqueItems': True}, 'membership_state': {'type': 'string', 'enum': ['enumerated_for_scope', 'unestablished']}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['id', 'scope_ref', 'unit', 'member_refs', 'selection_rule', 'coverage_refs', 'basis_refs', 'membership_state', 'qualifications'], 'allOf': [{'if': {'required': ['unit'], 'properties': {'unit': {'const': 'case_target'}}}, 'then': {'properties': {'member_refs': {'type': 'array', 'items': {'$ref': '#/$defs/CaseTarget'}, 'uniqueItems': True}}}, 'else': {'properties': {'member_refs': {'type': 'array', 'items': {'$ref': '#/$defs/InputRef'}, 'uniqueItems': True}}}}]},
    'BasisScope': {'type': 'object', 'properties': {'inquiry_refs': {'type': 'array', 'items': {'$ref': '#/$defs/InquiryRef'}, 'uniqueItems': True, 'minItems': 1}, 'claim_refs': {'type': 'array', 'items': {'$ref': '#/$defs/RecordRef'}, 'uniqueItems': True}, 'effective_window': {'$ref': '#/$defs/TimeWindow'}}, 'additionalProperties': False, 'required': ['inquiry_refs', 'claim_refs', 'effective_window']},
    'BasisTime': {'type': 'object', 'properties': {'asserted_at': {'$ref': '#/$defs/TimeValue'}, 'occurred_at': {'$ref': '#/$defs/TimeValue'}, 'observed_at': {'$ref': '#/$defs/TimeValue'}, 'published_at': {'$ref': '#/$defs/TimeValue'}, 'retrieved_at': {'$ref': '#/$defs/TimeValue'}, 'as_of': {'$ref': '#/$defs/TimeValue'}, 'valid_window': {'$ref': '#/$defs/TimeWindow'}, 'time_window': {'$ref': '#/$defs/TimeWindow'}}, 'additionalProperties': False, 'required': []},
    'Lifecycle': {'type': 'object', 'properties': {'state': {'type': 'string', 'enum': ['active', 'withdrawn', 'superseded']}, 'basis_refs': {'type': 'array', 'items': {'$ref': '#/$defs/EvidenceRef'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['state', 'basis_refs']},
    'BasisEntry': {'type': 'object', 'properties': {'id': {'$ref': '#/$defs/BasisId'}, 'source': {'$ref': '#/$defs/InputRef'}, 'basis_kind': {'anyOf': [{'$ref': '#/$defs/BasisKind'}, {'type': 'null'}]}, 'asserter_ref': {'anyOf': [{'$ref': '#/$defs/RecordRef'}, {'type': 'null'}]}, 'attestor_ref': {'anyOf': [{'$ref': '#/$defs/RecordRef'}, {'type': 'null'}]}, 'method': {'anyOf': [{'type': 'string'}, {'type': 'null'}]}, 'support_refs': {'type': 'array', 'items': {'$ref': '#/$defs/EvidenceRef'}, 'uniqueItems': True}, 'availability': {'anyOf': [{'$ref': '#/$defs/Availability'}, {'type': 'null'}]}, 'scope': {'anyOf': [{'$ref': '#/$defs/BasisScope'}, {'type': 'null'}]}, 'time': {'$ref': '#/$defs/BasisTime'}, 'lifecycle': {'anyOf': [{'$ref': '#/$defs/Lifecycle'}, {'type': 'null'}]}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}, 'check_refs': {'type': 'array', 'items': {'$ref': '#/$defs/CheckId'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['id', 'source', 'basis_kind', 'asserter_ref', 'attestor_ref', 'method', 'support_refs', 'availability', 'scope', 'time', 'lifecycle', 'qualifications', 'check_refs']},
    'Capability': {'type': 'object', 'properties': {'id': {'$ref': '#/$defs/CapabilityId'}, 'diagnostic_id': {'$ref': '#/$defs/DiagnosticId'}, 'inquiry_ref': {'allOf': [{'$ref': '#/$defs/InquiryRef'}, {'properties': {'selector': {'type': 'null'}}}]}, 'scope_refs': {'type': 'array', 'items': {'$ref': '#/$defs/ScopeId'}, 'uniqueItems': True}, 'check_refs': {'type': 'array', 'items': {'$ref': '#/$defs/CheckId'}, 'uniqueItems': True}, 'result_refs': {'type': 'array', 'items': {'$ref': '#/$defs/ResultId'}, 'uniqueItems': True}, 'available_result_refs': {'type': 'array', 'items': {'$ref': '#/$defs/ResultId'}, 'uniqueItems': True}, 'unavailable_result_refs': {'type': 'array', 'items': {'$ref': '#/$defs/ResultId'}, 'uniqueItems': True}, 'not_applicable_result_refs': {'type': 'array', 'items': {'$ref': '#/$defs/ResultId'}, 'uniqueItems': True}, 'not_evaluated_result_refs': {'type': 'array', 'items': {'$ref': '#/$defs/ResultId'}, 'uniqueItems': True}, 'reason_refs': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonId'}, 'uniqueItems': True}, 'scope_note': {'type': 'string', 'minLength': 1}}, 'additionalProperties': False, 'required': ['id', 'diagnostic_id', 'inquiry_ref', 'scope_refs', 'check_refs', 'result_refs', 'available_result_refs', 'unavailable_result_refs', 'not_applicable_result_refs', 'not_evaluated_result_refs', 'reason_refs', 'scope_note']},
    'PrerequisiteCheck': {'type': 'object', 'properties': {'id': {'$ref': '#/$defs/CheckId'}, 'check_id': {'type': 'string', 'enum': ['PC01', 'PC02', 'PC03', 'PC04', 'PC05', 'PC06', 'PC07', 'PC08', 'PC09', 'PC10', 'PC11', 'PC12', 'PC13', 'PC14', 'PC15', 'PC16', 'PC17', 'PC18', 'PC19', 'PC20', 'PC21', 'PC22', 'PC23', 'PC24']}, 'scope_ref': {'$ref': '#/$defs/ScopeId'}, 'state': {'$ref': '#/$defs/CheckState'}, 'input_refs': {'type': 'array', 'items': {'$ref': '#/$defs/InputRef'}, 'uniqueItems': True}, 'reason_refs': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonId'}, 'uniqueItems': True}, 'note': {'type': 'string'}}, 'additionalProperties': False, 'required': ['id', 'check_id', 'scope_ref', 'state', 'input_refs', 'reason_refs', 'note']},
    'ObservabilityDomain': {'type': 'object', 'properties': {'level_index': {'type': 'integer', 'minimum': 0, 'maximum': 4}, 'label': {'type': 'string', 'enum': ['Artifact and contribution inventory', 'Declared provenance and process metadata', 'Origin-resolution and scoped process-assessment evidence', 'Evaluator, correction-route and authority evidence', 'Boundary-qualified external input, stage histories and documented correction outcomes']}, 'available_result_refs': {'type': 'array', 'items': {'$ref': '#/$defs/ResultId'}, 'uniqueItems': True}, 'unavailable_result_refs': {'type': 'array', 'items': {'$ref': '#/$defs/ResultId'}, 'uniqueItems': True}, 'not_evaluated_result_refs': {'type': 'array', 'items': {'$ref': '#/$defs/ResultId'}, 'uniqueItems': True}, 'reason_refs': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonId'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['level_index', 'label', 'available_result_refs', 'unavailable_result_refs', 'not_evaluated_result_refs', 'reason_refs'], 'allOf': [{'if': {'required': ['level_index'], 'properties': {'level_index': {'const': 0}}}, 'then': {'properties': {'label': {'const': 'Artifact and contribution inventory'}}}}, {'if': {'required': ['level_index'], 'properties': {'level_index': {'const': 1}}}, 'then': {'properties': {'label': {'const': 'Declared provenance and process metadata'}}}}, {'if': {'required': ['level_index'], 'properties': {'level_index': {'const': 2}}}, 'then': {'properties': {'label': {'const': 'Origin-resolution and scoped process-assessment evidence'}}}}, {'if': {'required': ['level_index'], 'properties': {'level_index': {'const': 3}}}, 'then': {'properties': {'label': {'const': 'Evaluator, correction-route and authority evidence'}}}}, {'if': {'required': ['level_index'], 'properties': {'level_index': {'const': 4}}}, 'then': {'properties': {'label': {'const': 'Boundary-qualified external input, stage histories and documented correction outcomes'}}}}]},
    'Reason': {'type': 'object', 'properties': {'id': {'$ref': '#/$defs/ReasonId'}, 'code': {'$ref': '#/$defs/ReasonCode'}, 'scope_ref': {'anyOf': [{'$ref': '#/$defs/ScopeId'}, {'type': 'null'}]}, 'affected_result_refs': {'type': 'array', 'items': {'$ref': '#/$defs/ResultId'}, 'uniqueItems': True}, 'input_refs': {'type': 'array', 'items': {'$ref': '#/$defs/InputRef'}, 'uniqueItems': True}, 'detail': {'type': 'string', 'minLength': 1}, 'classification': {'$ref': '#/$defs/ReasonClassification'}}, 'additionalProperties': False, 'required': ['id', 'code', 'scope_ref', 'affected_result_refs', 'input_refs', 'detail', 'classification']},
    'Fraction': {'type': 'object', 'properties': {'numerator': {'type': 'integer', 'minimum': 0, 'maximum': 9007199254740991}, 'denominator': {'type': 'integer', 'minimum': 1, 'maximum': 9007199254740991}}, 'additionalProperties': False, 'required': ['numerator', 'denominator']},
    'PartitionCategory': {'type': 'object', 'properties': {'label': {'type': 'string', 'minLength': 1}, 'member_refs': {'type': 'array', 'items': {'$ref': '#/$defs/PopulationMember'}, 'uniqueItems': True}, 'count': {'type': 'integer', 'minimum': 0, 'maximum': 9007199254740991}}, 'additionalProperties': False, 'required': ['label', 'member_refs', 'count']},
    'Partition': {'type': 'object', 'properties': {'population_ref': {'$ref': '#/$defs/PopulationId'}, 'categories': {'type': 'array', 'items': {'$ref': '#/$defs/PartitionCategory'}}, 'total': {'type': 'integer', 'minimum': 0, 'maximum': 9007199254740991}}, 'additionalProperties': False, 'required': ['population_ref', 'categories', 'total']},
    'CompletionInterval': {'type': 'object', 'properties': {'lower': {'$ref': '#/$defs/Fraction'}, 'upper': {'$ref': '#/$defs/Fraction'}, 'interval_kind': {'type': 'string', 'enum': ['finite_record_completion', 'finite_cohort_completion']}, 'population_ref': {'$ref': '#/$defs/PopulationId'}, 'partition': {'$ref': '#/$defs/Partition'}}, 'additionalProperties': False, 'required': ['lower', 'upper', 'interval_kind', 'population_ref', 'partition']},
    'IncidenceMembership': {'type': 'object', 'properties': {'member_ref': {'$ref': '#/$defs/InputRef'}, 'origin_refs': {'type': 'array', 'items': {'$ref': '#/$defs/RecordRef'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['member_ref', 'origin_refs']},
    'OriginIncidenceCount': {'type': 'object', 'properties': {'origin_ref': {'$ref': '#/$defs/RecordRef'}, 'member_refs': {'type': 'array', 'items': {'$ref': '#/$defs/InputRef'}, 'uniqueItems': True}, 'count': {'type': 'integer', 'minimum': 0, 'maximum': 9007199254740991}}, 'additionalProperties': False, 'required': ['origin_ref', 'member_refs', 'count']},
    'Incidence': {'type': 'object', 'properties': {'population_ref': {'$ref': '#/$defs/PopulationId'}, 'memberships': {'type': 'array', 'items': {'$ref': '#/$defs/IncidenceMembership'}}, 'origin_counts': {'type': 'array', 'items': {'$ref': '#/$defs/OriginIncidenceCount'}}, 'total': {'type': 'integer', 'minimum': 0, 'maximum': 9007199254740991}, 'nonexclusive': {'const': True}}, 'additionalProperties': False, 'required': ['population_ref', 'memberships', 'origin_counts', 'total', 'nonexclusive']},
    'WitnessCollection': {'type': 'object', 'properties': {'witness_refs': {'type': 'array', 'items': {'$ref': '#/$defs/FindingId'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['witness_refs']},
    'RecordDisclosures': {'type': 'object', 'properties': {'records': {'type': 'array', 'items': {'$ref': '#/$defs/Disclosure'}}}, 'additionalProperties': False, 'required': ['records']},
    'Result': {'type': 'object', 'properties': {'id': {'$ref': '#/$defs/ResultId'}, 'diagnostic_id': {'$ref': '#/$defs/DiagnosticId'}, 'field_key': {'type': 'string', 'enum': ['nominal_seed_artifact_record_count', 'unresolved_seed_artifact_reference_count', 'seed_evidence_item_count', 'claim_artifact_record_count', 'claim_unassigned_seed_artifact_record_count', 'reached_origin_record_count', 'documentary_origin_boundary_record_count', 'origin_boundary_disclosures', 'submitted_comparison_member_count', 'qualified_process_set_member_count', 'qualified_origin_set_member_count', 'independence_assessment_disclosures', 'per_seed_origin_memberships', 'origin_incidence_counts', 'seed_origin_dispositions', 'documentary_origin_resolution_fraction', 'single_origin_contribution_hhi', 'immediate_evidence_layer_dispositions', 'inherited_only_seed_fraction', 'inherited_only_completion_interval', 'unresolved_frontier_reference_count', 'unqualified_terminal_record_count', 'seed_items_with_unresolved_ancestry_count', 'ancestry_gap_disclosures', 'shared_recorded_ancestor_count', 'matching_family_label_count', 'evaluator_overlap_disclosures', 'evaluator_overlap_witnesses', 'externality_assessment_disclosures', 'externality_stage_links', 'pipeline_stage_disclosures', 'stage_member_partition', 'stage_occurrence_fraction', 'stage_occurrence_completion_interval', 'cohort_transition_disclosures', 'cohort_transition_fraction', 'cohort_transition_completion_interval', 'declared_correction_route_witnesses', 'applicable_authorized_route_witnesses', 'correction_route_disclosures', 'correction_case_record_count', 'handling_event_record_count', 'linked_change_event_record_count', 'documentary_linked_change_target_count', 'cases_with_documentary_linked_change_count', 'correction_case_disclosures', 'correction_target_change_disclosures', 'reported_capacity_disclosures', 'corrective_independence_disclosures', 'human_contribution_disclosures', 'anomaly_context_disclosures', 'contestation_disclosures', 'tail_stage_result_links', 'coverage_disclosures', 'documentary_basis_gap_disclosures', 'declared_basis_inventory', 'reference_availability_inventory']}, 'scope_ref': {'$ref': '#/$defs/ScopeId'}, 'population_refs': {'type': 'array', 'items': {'$ref': '#/$defs/PopulationId'}, 'uniqueItems': True}, 'execution_state': {'type': 'string', 'enum': ['completed', 'not_performed', 'interrupted', 'failed']}, 'result_state': {'type': 'string', 'enum': ['available', 'unavailable', 'not_applicable', 'not_evaluated']}, 'result_origin': {'$ref': '#/$defs/ResultOrigin'}, 'value_kind': {'$ref': '#/$defs/ValueKind'}, 'value': {'anyOf': [{'type': 'null'}, {'type': 'integer', 'minimum': 0, 'maximum': 9007199254740991}, {'$ref': '#/$defs/Fraction'}, {'$ref': '#/$defs/CompletionInterval'}, {'$ref': '#/$defs/Partition'}, {'$ref': '#/$defs/Incidence'}, {'$ref': '#/$defs/RecordDisclosures'}, {'$ref': '#/$defs/WitnessCollection'}]}, 'check_refs': {'type': 'array', 'items': {'$ref': '#/$defs/CheckId'}, 'uniqueItems': True}, 'basis_refs': {'type': 'array', 'items': {'$ref': '#/$defs/BasisId'}, 'uniqueItems': True}, 'witness_refs': {'type': 'array', 'items': {'$ref': '#/$defs/FindingId'}, 'uniqueItems': True}, 'reason_refs': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonId'}, 'uniqueItems': True}, 'interpretation_limit': {'type': 'string', 'minLength': 1}}, 'additionalProperties': False, 'required': ['id', 'diagnostic_id', 'field_key', 'scope_ref', 'population_refs', 'execution_state', 'result_state', 'result_origin', 'value_kind', 'value', 'check_refs', 'basis_refs', 'witness_refs', 'reason_refs', 'interpretation_limit'], 'allOf': [{'anyOf': [{'properties': {'execution_state': {'const': 'completed'}, 'result_state': {'const': 'available'}}}, {'properties': {'execution_state': {'const': 'completed'}, 'result_state': {'const': 'unavailable'}}}, {'properties': {'execution_state': {'const': 'completed'}, 'result_state': {'const': 'not_applicable'}}}, {'properties': {'execution_state': {'const': 'not_performed'}, 'result_state': {'const': 'not_evaluated'}}}, {'properties': {'execution_state': {'const': 'interrupted'}, 'result_state': {'const': 'not_evaluated'}}}, {'properties': {'execution_state': {'const': 'failed'}, 'result_state': {'const': 'not_evaluated'}}}]}, {'if': {'required': ['result_state'], 'properties': {'result_state': {'const': 'available'}}}, 'then': {'properties': {'value': {'not': {'type': 'null'}}}}, 'else': {'properties': {'value': {'type': 'null'}, 'reason_refs': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonId'}, 'uniqueItems': True, 'minItems': 1}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'nominal_seed_artifact_record_count'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M001'}, 'value_kind': {'const': 'count'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'unresolved_seed_artifact_reference_count'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M001'}, 'value_kind': {'const': 'count'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'seed_evidence_item_count'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M001'}, 'value_kind': {'const': 'count'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'claim_artifact_record_count'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M001'}, 'value_kind': {'const': 'count'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'claim_unassigned_seed_artifact_record_count'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M001'}, 'value_kind': {'const': 'count'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'reached_origin_record_count'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M002'}, 'value_kind': {'const': 'count'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'documentary_origin_boundary_record_count'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M002'}, 'value_kind': {'const': 'count'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'origin_boundary_disclosures'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M002'}, 'value_kind': {'const': 'record_disclosures'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'submitted_comparison_member_count'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M003'}, 'value_kind': {'const': 'count'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'qualified_process_set_member_count'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M003'}, 'value_kind': {'const': 'count'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'qualified_origin_set_member_count'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M003'}, 'value_kind': {'const': 'count'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'independence_assessment_disclosures'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M003'}, 'value_kind': {'const': 'record_disclosures'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'per_seed_origin_memberships'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M004'}, 'value_kind': {'const': 'incidence'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'origin_incidence_counts'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M004'}, 'value_kind': {'const': 'incidence'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'seed_origin_dispositions'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M004'}, 'value_kind': {'const': 'partition'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'documentary_origin_resolution_fraction'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M004'}, 'value_kind': {'const': 'fraction'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'single_origin_contribution_hhi'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M005'}, 'value_kind': {'const': 'fraction'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'immediate_evidence_layer_dispositions'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M006'}, 'value_kind': {'const': 'partition'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'inherited_only_seed_fraction'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M006'}, 'value_kind': {'const': 'fraction'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'inherited_only_completion_interval'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M006'}, 'value_kind': {'const': 'completion_interval'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'unresolved_frontier_reference_count'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M007'}, 'value_kind': {'const': 'count'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'unqualified_terminal_record_count'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M007'}, 'value_kind': {'const': 'count'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'seed_items_with_unresolved_ancestry_count'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M007'}, 'value_kind': {'const': 'count'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'ancestry_gap_disclosures'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M007'}, 'value_kind': {'const': 'record_disclosures'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'shared_recorded_ancestor_count'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M008'}, 'value_kind': {'const': 'count'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'matching_family_label_count'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M008'}, 'value_kind': {'const': 'count'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'evaluator_overlap_disclosures'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M008'}, 'value_kind': {'const': 'record_disclosures'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'evaluator_overlap_witnesses'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M008'}, 'value_kind': {'const': 'witness_collection'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'externality_assessment_disclosures'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M009'}, 'value_kind': {'const': 'record_disclosures'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'externality_stage_links'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M009'}, 'value_kind': {'const': 'record_disclosures'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'pipeline_stage_disclosures'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M010'}, 'value_kind': {'const': 'record_disclosures'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'stage_member_partition'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M010'}, 'value_kind': {'const': 'partition'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'stage_occurrence_fraction'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M010'}, 'value_kind': {'const': 'fraction'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'stage_occurrence_completion_interval'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M010'}, 'value_kind': {'const': 'completion_interval'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'cohort_transition_disclosures'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M010'}, 'value_kind': {'const': 'record_disclosures'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'cohort_transition_fraction'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M010'}, 'value_kind': {'const': 'fraction'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'cohort_transition_completion_interval'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M010'}, 'value_kind': {'const': 'completion_interval'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'declared_correction_route_witnesses'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M011'}, 'value_kind': {'const': 'witness_collection'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'applicable_authorized_route_witnesses'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M011'}, 'value_kind': {'const': 'witness_collection'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'correction_route_disclosures'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M011'}, 'value_kind': {'const': 'record_disclosures'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'correction_case_record_count'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M012'}, 'value_kind': {'const': 'count'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'handling_event_record_count'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M012'}, 'value_kind': {'const': 'count'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'linked_change_event_record_count'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M012'}, 'value_kind': {'const': 'count'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'documentary_linked_change_target_count'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M012'}, 'value_kind': {'const': 'count'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'cases_with_documentary_linked_change_count'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M012'}, 'value_kind': {'const': 'count'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'correction_case_disclosures'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M012'}, 'value_kind': {'const': 'record_disclosures'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'correction_target_change_disclosures'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M012'}, 'value_kind': {'const': 'record_disclosures'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'reported_capacity_disclosures'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M012'}, 'value_kind': {'const': 'record_disclosures'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'corrective_independence_disclosures'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M013'}, 'value_kind': {'const': 'record_disclosures'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'human_contribution_disclosures'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M013'}, 'value_kind': {'const': 'record_disclosures'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'anomaly_context_disclosures'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M014'}, 'value_kind': {'const': 'record_disclosures'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'contestation_disclosures'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M014'}, 'value_kind': {'const': 'record_disclosures'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'tail_stage_result_links'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M014'}, 'value_kind': {'const': 'record_disclosures'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'coverage_disclosures'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M015'}, 'value_kind': {'const': 'record_disclosures'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'documentary_basis_gap_disclosures'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M015'}, 'value_kind': {'const': 'record_disclosures'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'declared_basis_inventory'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M015'}, 'value_kind': {'const': 'partition'}}}}, {'if': {'required': ['field_key'], 'properties': {'field_key': {'const': 'reference_availability_inventory'}}}, 'then': {'properties': {'diagnostic_id': {'const': 'SIT-M015'}, 'value_kind': {'const': 'partition'}}}}, {'if': {'required': ['result_state', 'value_kind'], 'properties': {'result_state': {'const': 'available'}, 'value_kind': {'const': 'count'}}}, 'then': {'properties': {'value': {'type': 'integer', 'minimum': 0, 'maximum': 9007199254740991}}}}, {'if': {'required': ['result_state', 'value_kind'], 'properties': {'result_state': {'const': 'available'}, 'value_kind': {'const': 'fraction'}}}, 'then': {'properties': {'value': {'$ref': '#/$defs/Fraction'}}}}, {'if': {'required': ['result_state', 'value_kind'], 'properties': {'result_state': {'const': 'available'}, 'value_kind': {'const': 'completion_interval'}}}, 'then': {'properties': {'value': {'$ref': '#/$defs/CompletionInterval'}}}}, {'if': {'required': ['result_state', 'value_kind'], 'properties': {'result_state': {'const': 'available'}, 'value_kind': {'const': 'partition'}}}, 'then': {'properties': {'value': {'$ref': '#/$defs/Partition'}}}}, {'if': {'required': ['result_state', 'value_kind'], 'properties': {'result_state': {'const': 'available'}, 'value_kind': {'const': 'incidence'}}}, 'then': {'properties': {'value': {'$ref': '#/$defs/Incidence'}}}}, {'if': {'required': ['result_state', 'value_kind'], 'properties': {'result_state': {'const': 'available'}, 'value_kind': {'const': 'record_disclosures'}}}, 'then': {'properties': {'value': {'$ref': '#/$defs/RecordDisclosures'}}}}, {'if': {'required': ['result_state', 'value_kind'], 'properties': {'result_state': {'const': 'available'}, 'value_kind': {'const': 'witness_collection'}}}, 'then': {'properties': {'value': {'$ref': '#/$defs/WitnessCollection'}}}}, {'if': {'required': ['field_key', 'result_state'], 'properties': {'field_key': {'const': 'origin_boundary_disclosures'}, 'result_state': {'const': 'available'}}}, 'then': {'properties': {'value': {'type': 'object', 'properties': {'records': {'type': 'array', 'items': {'type': 'object', 'properties': {'source': {'$ref': '#/$defs/InputRef'}, 'fields': {'$ref': '#/$defs/OriginBoundaryFields'}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['source', 'fields', 'qualifications']}}}, 'additionalProperties': False, 'required': ['records']}}}}, {'if': {'required': ['field_key', 'result_state'], 'properties': {'field_key': {'const': 'coverage_disclosures'}, 'result_state': {'const': 'available'}}}, 'then': {'properties': {'value': {'type': 'object', 'properties': {'records': {'type': 'array', 'items': {'type': 'object', 'properties': {'source': {'$ref': '#/$defs/InputRef'}, 'fields': {'$ref': '#/$defs/CoverageFields'}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['source', 'fields', 'qualifications']}}}, 'additionalProperties': False, 'required': ['records']}}}}, {'if': {'required': ['field_key', 'result_state'], 'properties': {'field_key': {'const': 'documentary_basis_gap_disclosures'}, 'result_state': {'const': 'available'}}}, 'then': {'properties': {'value': {'type': 'object', 'properties': {'records': {'type': 'array', 'items': {'type': 'object', 'properties': {'source': {'$ref': '#/$defs/InputRef'}, 'fields': {'$ref': '#/$defs/DocumentaryBasisGapFields'}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['source', 'fields', 'qualifications']}}}, 'additionalProperties': False, 'required': ['records']}}}}, {'if': {'required': ['field_key', 'result_state'], 'properties': {'field_key': {'const': 'independence_assessment_disclosures'}, 'result_state': {'const': 'available'}}}, 'then': {'properties': {'value': {'type': 'object', 'properties': {'records': {'type': 'array', 'items': {'type': 'object', 'properties': {'source': {'$ref': '#/$defs/InputRef'}, 'fields': {'$ref': '#/$defs/IndependenceAssessmentFields'}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['source', 'fields', 'qualifications']}}}, 'additionalProperties': False, 'required': ['records']}}}}, {'if': {'required': ['field_key', 'result_state'], 'properties': {'field_key': {'const': 'ancestry_gap_disclosures'}, 'result_state': {'const': 'available'}}}, 'then': {'properties': {'value': {'type': 'object', 'properties': {'records': {'type': 'array', 'items': {'type': 'object', 'properties': {'source': {'$ref': '#/$defs/InputRef'}, 'fields': {'$ref': '#/$defs/AncestryGapFields'}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['source', 'fields', 'qualifications']}}}, 'additionalProperties': False, 'required': ['records']}}}}, {'if': {'required': ['field_key', 'result_state'], 'properties': {'field_key': {'const': 'evaluator_overlap_disclosures'}, 'result_state': {'const': 'available'}}}, 'then': {'properties': {'value': {'type': 'object', 'properties': {'records': {'type': 'array', 'items': {'type': 'object', 'properties': {'source': {'$ref': '#/$defs/InputRef'}, 'fields': {'$ref': '#/$defs/EvaluatorOverlapFields'}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['source', 'fields', 'qualifications']}}}, 'additionalProperties': False, 'required': ['records']}}}}, {'if': {'required': ['field_key', 'result_state'], 'properties': {'field_key': {'const': 'externality_assessment_disclosures'}, 'result_state': {'const': 'available'}}}, 'then': {'properties': {'value': {'type': 'object', 'properties': {'records': {'type': 'array', 'items': {'type': 'object', 'properties': {'source': {'$ref': '#/$defs/InputRef'}, 'fields': {'$ref': '#/$defs/ExternalityAssessmentFields'}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['source', 'fields', 'qualifications']}}}, 'additionalProperties': False, 'required': ['records']}}}}, {'if': {'required': ['field_key', 'result_state'], 'properties': {'field_key': {'const': 'pipeline_stage_disclosures'}, 'result_state': {'const': 'available'}}}, 'then': {'properties': {'value': {'type': 'object', 'properties': {'records': {'type': 'array', 'items': {'type': 'object', 'properties': {'source': {'$ref': '#/$defs/InputRef'}, 'fields': {'$ref': '#/$defs/PipelineStageFields'}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['source', 'fields', 'qualifications']}}}, 'additionalProperties': False, 'required': ['records']}}}}, {'if': {'required': ['field_key', 'result_state'], 'properties': {'field_key': {'const': 'externality_stage_links'}, 'result_state': {'const': 'available'}}}, 'then': {'properties': {'value': {'type': 'object', 'properties': {'records': {'type': 'array', 'items': {'type': 'object', 'properties': {'source': {'$ref': '#/$defs/InputRef'}, 'fields': {'$ref': '#/$defs/ExternalityStageFields'}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['source', 'fields', 'qualifications']}}}, 'additionalProperties': False, 'required': ['records']}}}}, {'if': {'required': ['field_key', 'result_state'], 'properties': {'field_key': {'const': 'cohort_transition_disclosures'}, 'result_state': {'const': 'available'}}}, 'then': {'properties': {'value': {'type': 'object', 'properties': {'records': {'type': 'array', 'items': {'type': 'object', 'properties': {'source': {'$ref': '#/$defs/InputRef'}, 'fields': {'$ref': '#/$defs/CohortTransitionFields'}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['source', 'fields', 'qualifications']}}}, 'additionalProperties': False, 'required': ['records']}}}}, {'if': {'required': ['field_key', 'result_state'], 'properties': {'field_key': {'const': 'correction_route_disclosures'}, 'result_state': {'const': 'available'}}}, 'then': {'properties': {'value': {'type': 'object', 'properties': {'records': {'type': 'array', 'items': {'type': 'object', 'properties': {'source': {'$ref': '#/$defs/InputRef'}, 'fields': {'$ref': '#/$defs/CorrectionRouteFields'}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['source', 'fields', 'qualifications']}}}, 'additionalProperties': False, 'required': ['records']}}}}, {'if': {'required': ['field_key', 'result_state'], 'properties': {'field_key': {'const': 'correction_case_disclosures'}, 'result_state': {'const': 'available'}}}, 'then': {'properties': {'value': {'type': 'object', 'properties': {'records': {'type': 'array', 'items': {'type': 'object', 'properties': {'source': {'$ref': '#/$defs/InputRef'}, 'fields': {'$ref': '#/$defs/CorrectionCaseFields'}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['source', 'fields', 'qualifications']}}}, 'additionalProperties': False, 'required': ['records']}}}}, {'if': {'required': ['field_key', 'result_state'], 'properties': {'field_key': {'const': 'correction_target_change_disclosures'}, 'result_state': {'const': 'available'}}}, 'then': {'properties': {'value': {'type': 'object', 'properties': {'records': {'type': 'array', 'items': {'type': 'object', 'properties': {'source': {'$ref': '#/$defs/InputRef'}, 'fields': {'$ref': '#/$defs/CorrectionTargetChangeFields'}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['source', 'fields', 'qualifications']}}}, 'additionalProperties': False, 'required': ['records']}}}}, {'if': {'required': ['field_key', 'result_state'], 'properties': {'field_key': {'const': 'reported_capacity_disclosures'}, 'result_state': {'const': 'available'}}}, 'then': {'properties': {'value': {'type': 'object', 'properties': {'records': {'type': 'array', 'items': {'type': 'object', 'properties': {'source': {'$ref': '#/$defs/InputRef'}, 'fields': {'$ref': '#/$defs/ReportedCapacityFields'}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['source', 'fields', 'qualifications']}}}, 'additionalProperties': False, 'required': ['records']}}}}, {'if': {'required': ['field_key', 'result_state'], 'properties': {'field_key': {'const': 'human_contribution_disclosures'}, 'result_state': {'const': 'available'}}}, 'then': {'properties': {'value': {'type': 'object', 'properties': {'records': {'type': 'array', 'items': {'type': 'object', 'properties': {'source': {'$ref': '#/$defs/InputRef'}, 'fields': {'$ref': '#/$defs/HumanContributionFields'}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['source', 'fields', 'qualifications']}}}, 'additionalProperties': False, 'required': ['records']}}}}, {'if': {'required': ['field_key', 'result_state'], 'properties': {'field_key': {'const': 'corrective_independence_disclosures'}, 'result_state': {'const': 'available'}}}, 'then': {'properties': {'value': {'type': 'object', 'properties': {'records': {'type': 'array', 'items': {'type': 'object', 'properties': {'source': {'$ref': '#/$defs/InputRef'}, 'fields': {'$ref': '#/$defs/CorrectiveIndependenceFields'}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['source', 'fields', 'qualifications']}}}, 'additionalProperties': False, 'required': ['records']}}}}, {'if': {'required': ['field_key', 'result_state'], 'properties': {'field_key': {'const': 'anomaly_context_disclosures'}, 'result_state': {'const': 'available'}}}, 'then': {'properties': {'value': {'type': 'object', 'properties': {'records': {'type': 'array', 'items': {'type': 'object', 'properties': {'source': {'$ref': '#/$defs/InputRef'}, 'fields': {'$ref': '#/$defs/AnomalyContextFields'}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['source', 'fields', 'qualifications']}}}, 'additionalProperties': False, 'required': ['records']}}}}, {'if': {'required': ['field_key', 'result_state'], 'properties': {'field_key': {'const': 'contestation_disclosures'}, 'result_state': {'const': 'available'}}}, 'then': {'properties': {'value': {'type': 'object', 'properties': {'records': {'type': 'array', 'items': {'type': 'object', 'properties': {'source': {'$ref': '#/$defs/InputRef'}, 'fields': {'$ref': '#/$defs/ContestationFields'}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['source', 'fields', 'qualifications']}}}, 'additionalProperties': False, 'required': ['records']}}}}, {'if': {'required': ['field_key', 'result_state'], 'properties': {'field_key': {'const': 'tail_stage_result_links'}, 'result_state': {'const': 'available'}}}, 'then': {'properties': {'value': {'type': 'object', 'properties': {'records': {'type': 'array', 'items': {'type': 'object', 'properties': {'source': {'$ref': '#/$defs/ResultId'}, 'fields': {'$ref': '#/$defs/TailStageResultLinkFields'}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['source', 'fields', 'qualifications']}}}, 'additionalProperties': False, 'required': ['records']}}}}]},
    'Diagnostic': {'type': 'object', 'properties': {'code': {'type': 'string', 'enum': ['invalid_syntax', 'duplicate_key', 'unsupported_input_contract', 'duplicate_identifier', 'dangling_reference', 'type_or_enum_violation', 'missing_required_field', 'endpoint_or_claim_mismatch', 'invalid_time', 'input_constraint_violation', 'resource_limit_reached', 'execution_failed']}, 'location': {'type': 'null'}, 'safe_message': {'type': 'string', 'minLength': 1}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['code', 'location', 'safe_message', 'qualifications']},
    'RunTime': {'const': {'state': 'unknown', 'value': None, 'precision': None, 'reason': 'not_recorded_by_SIT-RP-0.1'}},
    'Run': {'type': 'object', 'properties': {'processing_state': {'type': 'string', 'enum': ['completed', 'interrupted', 'rejected', 'failed']}, 'tool_name': {'const': 'Source Integrity Toolkit'}, 'tool_version': {'const': '0.1.0.dev0'}, 'input_contract_version': {'const': 'sit-bundle/0.1'}, 'requested_diagnostic_ids': {'type': 'array', 'items': {'$ref': '#/$defs/DiagnosticId'}, 'uniqueItems': True, 'minItems': 15, 'maxItems': 15}, 'completed_diagnostic_ids': {'type': 'array', 'items': {'$ref': '#/$defs/DiagnosticId'}, 'uniqueItems': True}, 'started_at': {'$ref': '#/$defs/RunTime'}, 'finished_at': {'$ref': '#/$defs/RunTime'}, 'diagnostics': {'type': 'array', 'items': {'$ref': '#/$defs/Diagnostic'}}, 'qualifications': {'const': ['SIT-RP-0.1', 'Wall-clock start and finish times are not recorded by SIT-RP-0.1.']}}, 'additionalProperties': False, 'required': ['processing_state', 'tool_name', 'tool_version', 'input_contract_version', 'requested_diagnostic_ids', 'completed_diagnostic_ids', 'started_at', 'finished_at', 'diagnostics', 'qualifications']},
    'RawFileDigest': {'type': 'object', 'properties': {'algorithm': {'const': 'sha256'}, 'value': {'type': 'string', 'pattern': '^[0-9a-f]{64}$', 'not': {'pattern': '[^0-9a-f]'}}, 'covered_material': {'type': 'string', 'minLength': 1}}, 'additionalProperties': False, 'required': ['algorithm', 'value', 'covered_material']},
    'InputIdentity': {'type': 'object', 'properties': {'source_mode': {'type': 'string', 'enum': ['local_file', 'in_process']}, 'input_contract_version': {'anyOf': [{'type': 'string'}, {'type': 'null'}]}, 'bundle_id': {'anyOf': [{'$ref': '#/$defs/Identifier'}, {'type': 'null'}]}, 'snapshot_id': {'anyOf': [{'$ref': '#/$defs/Identifier'}, {'type': 'null'}]}, 'declared_predecessor': {'anyOf': [{'$ref': '#/$defs/Predecessor'}, {'type': 'null'}]}, 'raw_file_digest': {'anyOf': [{'$ref': '#/$defs/RawFileDigest'}, {'type': 'null'}]}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['source_mode', 'input_contract_version', 'bundle_id', 'snapshot_id', 'declared_predecessor', 'raw_file_digest', 'qualifications'], 'allOf': [{'if': {'required': ['source_mode'], 'properties': {'source_mode': {'const': 'in_process'}}}, 'then': {'properties': {'raw_file_digest': {'type': 'null'}}}}]},
    'InputValidation': {'type': 'object', 'properties': {'state': {'type': 'string', 'enum': ['accepted', 'rejected', 'not_completed']}, 'diagnostics': {'type': 'array', 'items': {'$ref': '#/$defs/Diagnostic'}}}, 'additionalProperties': False, 'required': ['state', 'diagnostics']},
    'AuditReport': {'type': 'object', 'properties': {'contract_version': {'const': 'sit-report/0.1'}, 'report_kind': {'type': 'string', 'enum': ['audit_report', 'validation_diagnostics', 'processing_diagnostics']}, 'report_id': {'const': 'SIT-RPT-000001'}, 'run': {'$ref': '#/$defs/Run'}, 'input_identity': {'$ref': '#/$defs/InputIdentity'}, 'input_validation': {'$ref': '#/$defs/InputValidation'}, 'scopes': {'type': 'array', 'items': {'$ref': '#/$defs/Scope'}}, 'populations': {'type': 'array', 'items': {'$ref': '#/$defs/Population'}}, 'basis_index': {'type': 'array', 'items': {'$ref': '#/$defs/BasisEntry'}}, 'capabilities': {'type': 'array', 'items': {'$ref': '#/$defs/Capability'}}, 'checks': {'type': 'array', 'items': {'$ref': '#/$defs/PrerequisiteCheck'}}, 'observability_domains': {'type': 'array', 'items': {'$ref': '#/$defs/ObservabilityDomain'}}, 'results': {'type': 'array', 'items': {'$ref': '#/$defs/Result'}}, 'findings': {'type': 'array', 'items': {'$ref': '#/$defs/Finding'}}, 'reasons': {'type': 'array', 'items': {'$ref': '#/$defs/Reason'}}, 'release_limits': {'const': ['Offline analysis of caller-supplied records only.', 'Source identity, authenticity and external events are not independently authenticated.', 'No live monitoring or active content-level poisoning, injection or authorship detection was performed.', 'No universal truth, integrity, independence or safety score is produced.', 'No automatic intervention, source contact or changes to the audited system are performed.', 'Scope-specific evidence gaps and qualifications remain as recorded; missing records do not establish outside-world absence.']}}, 'additionalProperties': False, 'required': ['contract_version', 'report_kind', 'report_id', 'run', 'input_identity', 'input_validation', 'scopes', 'populations', 'basis_index', 'capabilities', 'checks', 'observability_domains', 'results', 'findings', 'reasons', 'release_limits'], 'allOf': [{'anyOf': [{'properties': {'report_kind': {'const': 'audit_report'}, 'run': {'properties': {'processing_state': {'const': 'completed'}}}, 'input_validation': {'properties': {'state': {'const': 'accepted'}}}}}, {'properties': {'report_kind': {'const': 'audit_report'}, 'run': {'properties': {'processing_state': {'const': 'interrupted'}}}, 'input_validation': {'properties': {'state': {'const': 'accepted'}}}}}, {'properties': {'report_kind': {'const': 'validation_diagnostics'}, 'run': {'properties': {'processing_state': {'const': 'rejected'}}}, 'input_validation': {'properties': {'state': {'const': 'rejected'}}}}}, {'properties': {'report_kind': {'const': 'processing_diagnostics'}, 'run': {'properties': {'processing_state': {'const': 'interrupted'}}}, 'input_validation': {'properties': {'state': {'const': 'not_completed'}}}}}, {'properties': {'report_kind': {'const': 'processing_diagnostics'}, 'run': {'properties': {'processing_state': {'const': 'failed'}}}, 'input_validation': {'properties': {'state': {'const': 'accepted'}}}}}, {'properties': {'report_kind': {'const': 'processing_diagnostics'}, 'run': {'properties': {'processing_state': {'const': 'failed'}}}, 'input_validation': {'properties': {'state': {'const': 'not_completed'}}}}}]}, {'if': {'required': ['report_kind'], 'properties': {'report_kind': {'const': 'audit_report'}}}, 'then': {'properties': {'observability_domains': {'minItems': 5, 'maxItems': 5}}}, 'else': {'properties': {'scopes': {'maxItems': 0}, 'populations': {'maxItems': 0}, 'basis_index': {'maxItems': 0}, 'capabilities': {'maxItems': 0}, 'checks': {'maxItems': 0}, 'observability_domains': {'maxItems': 0}, 'results': {'maxItems': 0}, 'findings': {'maxItems': 0}}}}]},
    'SelectedProvenance': {'type': 'object', 'properties': {'attributed_to_ref': {'anyOf': [{'$ref': '#/$defs/Identifier'}, {'type': 'null'}]}, 'basis_kind': {'$ref': '#/$defs/enum_basis_kind'}, 'evidence_ref_ids': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'uniqueItems': True}, 'method': {'anyOf': [{'type': 'string'}, {'type': 'null'}]}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['attributed_to_ref', 'basis_kind', 'evidence_ref_ids', 'method', 'qualifications']},
    'SelectedGap': {'type': 'object', 'properties': {'field': {'type': 'string'}, 'reason': {'$ref': '#/$defs/enum_gap_reason'}, 'detail': {'type': 'string', 'minLength': 1}}, 'additionalProperties': False, 'required': ['field', 'reason', 'detail']},
    'SelectedEvidenceReference': {'type': 'object', 'properties': {'id': {'$ref': '#/$defs/Identifier'}, 'reference_kind': {'$ref': '#/$defs/enum_reference_kind'}, 'availability': {'$ref': '#/$defs/enum_availability'}, 'artifact_ref': {'anyOf': [{'$ref': '#/$defs/Identifier'}, {'type': 'null'}]}, 'record_ref': {'anyOf': [{'$ref': '#/$defs/Identifier'}, {'type': 'null'}]}, 'provided_by_ref': {'anyOf': [{'$ref': '#/$defs/Identifier'}, {'type': 'null'}]}, 'attestor_ref': {'anyOf': [{'$ref': '#/$defs/Identifier'}, {'type': 'null'}]}, 'scope_note': {'type': 'string', 'minLength': 1}, 'gaps': {'type': 'array', 'items': {'$ref': '#/$defs/SelectedGap'}}}, 'additionalProperties': False, 'required': ['id', 'reference_kind', 'availability', 'artifact_ref', 'record_ref', 'provided_by_ref', 'attestor_ref', 'scope_note']},
    'SelectedInquiry': {'type': 'object', 'properties': {'id': {'$ref': '#/$defs/Identifier'}, 'target_claim_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'minItems': 1, 'uniqueItems': True}, 'target_object_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'uniqueItems': True}, 'seed_artifact_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'uniqueItems': True}, 'seed_evidence_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'uniqueItems': True}, 'boundary': {'$ref': '#/$defs/SelectedBoundary'}, 'time_window': {'$ref': '#/$defs/TimeWindow'}, 'as_of': {'$ref': '#/$defs/TimeValue'}, 'dependency_dimensions': {'type': 'array', 'items': {'$ref': '#/$defs/enum_dimension'}}, 'coverage_assertion_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'uniqueItems': True}, 'provenance': {'$ref': '#/$defs/SelectedProvenance'}, 'gaps': {'type': 'array', 'items': {'$ref': '#/$defs/SelectedGap'}}}, 'additionalProperties': False, 'required': ['id', 'target_claim_refs', 'target_object_refs', 'seed_artifact_refs', 'seed_evidence_refs', 'boundary', 'time_window', 'as_of', 'dependency_dimensions', 'coverage_assertion_refs', 'provenance']},
    'SelectedBoundary': {'type': 'object', 'properties': {'description': {'type': 'string', 'minLength': 1}, 'criterion': {'type': 'string', 'minLength': 1}, 'system_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['description', 'criterion', 'system_refs']},
    'SelectedRecord': {'type': 'object', 'properties': {'id': {'$ref': '#/$defs/Identifier'}, 'kind': {'$ref': '#/$defs/enum_record_kind'}, 'data': {'$ref': '#/$defs/SelectedRecordData'}, 'provenance': {'$ref': '#/$defs/SelectedProvenance'}, 'gaps': {'type': 'array', 'items': {'$ref': '#/$defs/SelectedGap'}}}, 'additionalProperties': False, 'required': ['id', 'kind', 'data', 'provenance'], 'allOf': [{'if': {'required': ['kind'], 'properties': {'kind': {'const': 'claim'}}}, 'then': {'properties': {'data': {'$ref': '#/$defs/SelectedClaimData'}}}}, {'if': {'required': ['kind'], 'properties': {'kind': {'const': 'artifact'}}}, 'then': {'properties': {'data': {'$ref': '#/$defs/SelectedArtifactData'}}}}, {'if': {'required': ['kind'], 'properties': {'kind': {'const': 'actor'}}}, 'then': {'properties': {'data': {'$ref': '#/$defs/SelectedActorData'}}}}, {'if': {'required': ['kind'], 'properties': {'kind': {'const': 'evidence_item'}}}, 'then': {'properties': {'data': {'$ref': '#/$defs/SelectedEvidenceItemData'}}}}, {'if': {'required': ['kind'], 'properties': {'kind': {'const': 'origin_event'}}}, 'then': {'properties': {'data': {'$ref': '#/$defs/SelectedOriginEventData'}}}}, {'if': {'required': ['kind'], 'properties': {'kind': {'const': 'model'}}}, 'then': {'properties': {'data': {'$ref': '#/$defs/SelectedModelData'}}}}, {'if': {'required': ['kind'], 'properties': {'kind': {'const': 'evaluation'}}}, 'then': {'properties': {'data': {'$ref': '#/$defs/SelectedEvaluationData'}}}}, {'if': {'required': ['kind'], 'properties': {'kind': {'const': 'correction_channel'}}}, 'then': {'properties': {'data': {'$ref': '#/$defs/SelectedCorrectionChannelData'}}}}, {'if': {'required': ['kind'], 'properties': {'kind': {'const': 'correction_event'}}}, 'then': {'properties': {'data': {'$ref': '#/$defs/SelectedCorrectionEventData'}}}}, {'if': {'required': ['kind'], 'properties': {'kind': {'const': 'pipeline_record'}}}, 'then': {'properties': {'data': {'$ref': '#/$defs/SelectedPipelineRecordData'}}}}, {'if': {'required': ['kind'], 'properties': {'kind': {'const': 'anomaly'}}}, 'then': {'properties': {'data': {'$ref': '#/$defs/SelectedAnomalyData'}}}}, {'if': {'required': ['kind'], 'properties': {'kind': {'const': 'unresolved_reference'}}}, 'then': {'properties': {'data': {'$ref': '#/$defs/SelectedUnresolvedReferenceData'}}}}]},
    'SelectedClaimData': {'type': 'object', 'properties': {'claim_key': {'type': 'string'}, 'version_label': {'anyOf': [{'type': 'string'}, {'type': 'null'}]}, 'content_evidence_ref': {'$ref': '#/$defs/Identifier'}, 'context': {'type': 'string'}}, 'additionalProperties': False, 'required': ['claim_key', 'version_label', 'context']},
    'SelectedArtifactData': {'type': 'object', 'properties': {'artifact_kind': {'$ref': '#/$defs/enum_artifact_kind'}, 'version_label': {'anyOf': [{'type': 'string'}, {'type': 'null'}]}, 'published_at': {'$ref': '#/$defs/TimeValue'}, 'retrieved_at': {'$ref': '#/$defs/TimeValue'}, 'content_evidence_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['artifact_kind', 'version_label', 'published_at', 'retrieved_at', 'content_evidence_refs']},
    'SelectedActorData': {'type': 'object', 'properties': {'actor_kind': {'$ref': '#/$defs/enum_actor_kind'}, 'identity_disclosure': {'$ref': '#/$defs/enum_identity_disclosure'}}, 'additionalProperties': False, 'required': ['actor_kind', 'identity_disclosure']},
    'SelectedEvidenceItemData': {'type': 'object', 'properties': {'claim_ref': {'$ref': '#/$defs/Identifier'}, 'artifact_ref': {'$ref': '#/$defs/Identifier'}, 'epistemic_type': {'$ref': '#/$defs/enum_epistemic_type'}, 'description': {'type': 'string', 'minLength': 1}}, 'additionalProperties': False, 'required': ['claim_ref', 'artifact_ref', 'epistemic_type', 'description']},
    'SelectedOriginEventData': {'type': 'object', 'properties': {'event_kind': {'$ref': '#/$defs/enum_origin_event_kind'}, 'event_key': {'anyOf': [{'type': 'string'}, {'type': 'null'}]}, 'performed_by_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'uniqueItems': True}, 'method_ref': {'anyOf': [{'$ref': '#/$defs/Identifier'}, {'type': 'null'}]}, 'occurred_at': {'$ref': '#/$defs/TimeValue'}, 'description': {'type': 'string', 'minLength': 1}}, 'additionalProperties': False, 'required': ['event_kind', 'event_key', 'performed_by_refs', 'method_ref', 'occurred_at', 'description']},
    'SelectedModelData': {'type': 'object', 'properties': {'model_key': {'type': 'string'}, 'version_label': {'anyOf': [{'type': 'string'}, {'type': 'null'}]}, 'family_label': {'anyOf': [{'type': 'string'}, {'type': 'null'}]}, 'provider_ref': {'anyOf': [{'$ref': '#/$defs/Identifier'}, {'type': 'null'}]}}, 'additionalProperties': False, 'required': ['model_key', 'version_label', 'family_label', 'provider_ref']},
    'SelectedEvaluationData': {'type': 'object', 'properties': {'evaluation_kind': {'$ref': '#/$defs/enum_evaluation_kind'}, 'target_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'minItems': 1, 'uniqueItems': True}, 'role_bindings': {'type': 'array', 'items': {'$ref': '#/$defs/SelectedRoleBinding'}}, 'result_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'uniqueItems': True}, 'occurred_at': {'$ref': '#/$defs/TimeValue'}, 'review_contribution': {'anyOf': [{'type': 'string'}, {'type': 'null'}]}}, 'additionalProperties': False, 'required': ['evaluation_kind', 'target_refs', 'role_bindings', 'result_refs', 'occurred_at', 'review_contribution']},
    'SelectedRoleBinding': {'type': 'object', 'properties': {'role': {'$ref': '#/$defs/enum_role'}, 'object_ref': {'$ref': '#/$defs/Identifier'}, 'evidence_ref_ids': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'uniqueItems': True}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['role', 'object_ref', 'evidence_ref_ids', 'qualifications']},
    'SelectedCorrectionChannelData': {'type': 'object', 'properties': {'owner_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'uniqueItems': True}, 'target_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'uniqueItems': True}, 'declared_action_types': {'type': 'array', 'items': {'$ref': '#/$defs/enum_action'}}, 'valid_window': {'$ref': '#/$defs/TimeWindow'}}, 'additionalProperties': False, 'required': ['owner_refs', 'target_refs', 'declared_action_types', 'valid_window']},
    'SelectedCorrectionEventData': {'type': 'object', 'properties': {'event_kind': {'$ref': '#/$defs/enum_correction_event_kind'}, 'case_ref': {'anyOf': [{'$ref': '#/$defs/Identifier'}, {'type': 'null'}]}, 'channel_ref': {'anyOf': [{'$ref': '#/$defs/Identifier'}, {'type': 'null'}]}, 'target_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'minItems': 1, 'uniqueItems': True}, 'occurred_at': {'$ref': '#/$defs/TimeValue'}, 'details': {'$ref': '#/$defs/SelectedCorrectionDetails'}}, 'additionalProperties': False, 'required': ['event_kind', 'case_ref', 'channel_ref', 'target_refs', 'occurred_at', 'details'], 'allOf': [{'if': {'required': ['event_kind'], 'properties': {'event_kind': {'const': 'submission'}}}, 'then': {'properties': {'case_ref': {'type': 'null'}, 'details': {'$ref': '#/$defs/SelectedSubmissionDetails'}}}}, {'if': {'required': ['event_kind'], 'properties': {'event_kind': {'const': 'handling'}}}, 'then': {'properties': {'case_ref': {'$ref': '#/$defs/Identifier'}, 'details': {'$ref': '#/$defs/SelectedHandlingDetails'}}}}, {'if': {'required': ['event_kind'], 'properties': {'event_kind': {'const': 'change'}}}, 'then': {'properties': {'case_ref': {'$ref': '#/$defs/Identifier'}, 'details': {'$ref': '#/$defs/SelectedChangeDetails'}}}}]},
    'SelectedSubmissionDetails': {'type': 'object', 'properties': {'submission_kind': {'$ref': '#/$defs/enum_submission_kind'}, 'summary': {'type': 'string', 'minLength': 1}}, 'additionalProperties': False, 'required': ['submission_kind', 'summary']},
    'SelectedHandlingDetails': {'type': 'object', 'properties': {'outcome': {'$ref': '#/$defs/enum_outcome'}, 'reason': {'anyOf': [{'type': 'string'}, {'type': 'null'}]}}, 'additionalProperties': False, 'required': ['outcome', 'reason']},
    'SelectedChangeDetails': {'type': 'object', 'properties': {'action_type': {'$ref': '#/$defs/enum_action'}, 'before_ref': {'$ref': '#/$defs/Identifier'}, 'after_ref': {'anyOf': [{'$ref': '#/$defs/Identifier'}, {'type': 'null'}]}, 'after_absence_reason': {'anyOf': [{'type': 'string'}, {'type': 'null'}]}, 'linkage_description': {'type': 'string', 'minLength': 1}}, 'additionalProperties': False, 'required': ['action_type', 'before_ref', 'after_ref', 'after_absence_reason', 'linkage_description'], 'allOf': [{'if': {'required': ['after_ref'], 'properties': {'after_ref': {'type': 'null'}}}, 'then': {'properties': {'after_absence_reason': {'type': 'string', 'minLength': 1}}}, 'else': {'properties': {'after_absence_reason': {'type': 'null'}}}}]},
    'SelectedPipelineRecordData': {'type': 'object', 'properties': {'subject_ref': {'$ref': '#/$defs/Identifier'}, 'run_key': {'type': 'string', 'minLength': 1}, 'stage_key': {'type': 'string', 'minLength': 1}, 'stage': {'$ref': '#/$defs/enum_stage'}, 'state': {'$ref': '#/$defs/enum_pipeline_state'}, 'output_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'uniqueItems': True}, 'observed_at': {'$ref': '#/$defs/TimeValue'}, 'linkage_kind': {'$ref': '#/$defs/enum_linkage_kind'}, 'detail': {'type': 'string', 'minLength': 1}}, 'additionalProperties': False, 'required': ['subject_ref', 'run_key', 'stage_key', 'stage', 'state', 'output_refs', 'observed_at', 'linkage_kind', 'detail']},
    'SelectedAnomalyData': {'type': 'object', 'properties': {'inquiry_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'minItems': 1, 'uniqueItems': True}, 'claim_ref': {'anyOf': [{'$ref': '#/$defs/Identifier'}, {'type': 'null'}]}, 'original_context': {'anyOf': [{'type': 'string', 'minLength': 1}, {'type': 'null'}]}, 'context_evidence_ref': {'anyOf': [{'$ref': '#/$defs/Identifier'}, {'type': 'null'}]}, 'classification_state': {'$ref': '#/$defs/enum_classification_state'}, 'caller_label': {'anyOf': [{'type': 'string'}, {'type': 'null'}]}, 'comparison_note': {'anyOf': [{'type': 'string'}, {'type': 'null'}]}}, 'additionalProperties': False, 'required': ['inquiry_refs', 'claim_ref', 'original_context', 'context_evidence_ref', 'classification_state', 'caller_label', 'comparison_note'], 'allOf': [{'if': {'required': ['classification_state'], 'properties': {'classification_state': {'const': 'unclassified'}}}, 'then': {'properties': {'caller_label': {'type': 'null'}}}, 'else': {'properties': {'caller_label': {'type': 'string'}}}}, {'if': {'required': ['original_context'], 'properties': {'original_context': {'type': 'null'}}}, 'then': {'properties': {'context_evidence_ref': {'$ref': '#/$defs/Identifier'}}}}]},
    'SelectedUnresolvedReferenceData': {'type': 'object', 'properties': {'expected_kinds': {'type': 'array', 'items': {'$ref': '#/$defs/enum_resolved_kind'}, 'minItems': 1}, 'reason': {'$ref': '#/$defs/enum_endpoint_gap_reason'}, 'description': {'type': 'string', 'minLength': 1}}, 'additionalProperties': False, 'required': ['expected_kinds', 'reason', 'description']},
    'SelectedAssertion': {'type': 'object', 'properties': {'id': {'$ref': '#/$defs/Identifier'}, 'assertion_kind': {'$ref': '#/$defs/enum_assertion_kind'}, 'scope': {'$ref': '#/$defs/SelectedAssertionScope'}, 'provenance': {'$ref': '#/$defs/SelectedProvenance'}, 'asserted_at': {'$ref': '#/$defs/TimeValue'}, 'lifecycle_state': {'$ref': '#/$defs/enum_lifecycle_state'}, 'lifecycle_basis_ref_ids': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'uniqueItems': True}, 'data': {'$ref': '#/$defs/SelectedAssertionData'}, 'gaps': {'type': 'array', 'items': {'$ref': '#/$defs/SelectedGap'}}}, 'additionalProperties': False, 'required': ['id', 'assertion_kind', 'scope', 'provenance', 'asserted_at', 'lifecycle_state', 'lifecycle_basis_ref_ids', 'data'], 'allOf': [{'if': {'required': ['assertion_kind'], 'properties': {'assertion_kind': {'const': 'relation'}}}, 'then': {'properties': {'data': {'$ref': '#/$defs/SelectedRelationData'}}}}, {'if': {'required': ['assertion_kind'], 'properties': {'assertion_kind': {'const': 'assessment'}}}, 'then': {'properties': {'data': {'$ref': '#/$defs/SelectedAssessmentData'}}}}]},
    'SelectedAssertionScope': {'type': 'object', 'properties': {'inquiry_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'minItems': 1, 'uniqueItems': True}, 'claim_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'uniqueItems': True}, 'effective_window': {'$ref': '#/$defs/TimeWindow'}}, 'additionalProperties': False, 'required': ['inquiry_refs', 'claim_refs', 'effective_window']},
    'SelectedRelationData': {'type': 'object', 'properties': {'predicate': {'$ref': '#/$defs/enum_predicate'}, 'from_ref': {'$ref': '#/$defs/Identifier'}, 'to_ref': {'$ref': '#/$defs/Identifier'}, 'polarity': {'$ref': '#/$defs/enum_polarity'}, 'dimension': {'anyOf': [{'$ref': '#/$defs/enum_dimension'}, {'type': 'null'}]}, 'details': {'$ref': '#/$defs/SelectedRelationDetails'}}, 'additionalProperties': False, 'required': ['predicate', 'from_ref', 'to_ref', 'polarity', 'dimension', 'details'], 'allOf': [{'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'supports'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedStanceDetails'}, 'dimension': {'type': 'null'}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'contradicts'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedStanceDetails'}, 'dimension': {'type': 'null'}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'describes'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedStanceDetails'}, 'dimension': {'type': 'null'}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'qualifies'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedStanceDetails'}, 'dimension': {'type': 'null'}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'contextualizes'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedStanceDetails'}, 'dimension': {'type': 'null'}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'corroborates'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedStanceDetails'}, 'dimension': {'type': 'null'}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'cites'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedCitationDetails'}, 'dimension': {'type': 'null'}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'derived_from'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedTransformationDetails'}, 'dimension': {'anyOf': [{'$ref': '#/$defs/enum_dimension'}, {'type': 'null'}]}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'copies'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedTransformationDetails'}, 'dimension': {'anyOf': [{'$ref': '#/$defs/enum_dimension'}, {'type': 'null'}]}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'syndicated_from'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedTransformationDetails'}, 'dimension': {'anyOf': [{'$ref': '#/$defs/enum_dimension'}, {'type': 'null'}]}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'summarizes'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedTransformationDetails'}, 'dimension': {'anyOf': [{'$ref': '#/$defs/enum_dimension'}, {'type': 'null'}]}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'translates'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedTransformationDetails'}, 'dimension': {'anyOf': [{'$ref': '#/$defs/enum_dimension'}, {'type': 'null'}]}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'quotes'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedTransformationDetails'}, 'dimension': {'anyOf': [{'$ref': '#/$defs/enum_dimension'}, {'type': 'null'}]}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'originates_from'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedOriginDetails'}, 'dimension': {'$ref': '#/$defs/enum_dimension'}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'depends_on'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedOriginDetails'}, 'dimension': {'$ref': '#/$defs/enum_dimension'}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'generated_by'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedAgentDetails'}, 'dimension': {'type': 'null'}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'published_by'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedAgentDetails'}, 'dimension': {'type': 'null'}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'owned_by'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedAgentDetails'}, 'dimension': {'const': 'organizational_control'}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'model_derived_from'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedModelDetails'}, 'dimension': {'const': 'model_ancestry'}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'trained_on'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedModelDetails'}, 'dimension': {'const': 'model_ancestry'}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'retrieved_from'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedRetrievalDetails'}, 'dimension': {'type': 'null'}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'propagates_to'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedRouteDetails'}, 'dimension': {'type': 'null'}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'supersedes'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedSupersessionDetails'}, 'dimension': {'type': 'null'}}}}, {'if': {'required': ['predicate'], 'properties': {'predicate': {'const': 'same_identity_as'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedIdentityDetails'}, 'dimension': {'type': 'null'}}}}]},
    'SelectedStanceDetails': {'type': 'object', 'properties': {'note': {'type': 'string'}}, 'additionalProperties': False, 'required': []},
    'SelectedCitationDetails': {'type': 'object', 'properties': {'note': {'type': 'string'}}, 'additionalProperties': False, 'required': []},
    'SelectedTransformationDetails': {'type': 'object', 'properties': {'transformer_ref': {'$ref': '#/$defs/Identifier'}, 'method_ref': {'$ref': '#/$defs/Identifier'}, 'occurred_at': {'$ref': '#/$defs/TimeValue'}, 'portion_note': {'type': 'string'}}, 'additionalProperties': False, 'required': []},
    'SelectedOriginDetails': {'type': 'object', 'properties': {'dependency_note': {'type': 'string'}, 'portion_note': {'type': 'string'}}, 'additionalProperties': False, 'required': []},
    'SelectedAgentDetails': {'type': 'object', 'properties': {'role_note': {'type': 'string'}, 'valid_window': {'$ref': '#/$defs/TimeWindow'}}, 'additionalProperties': False, 'required': []},
    'SelectedModelDetails': {'type': 'object', 'properties': {'stage_note': {'type': 'string'}, 'subset_descriptor': {'type': 'string'}, 'occurred_at': {'$ref': '#/$defs/TimeValue'}}, 'additionalProperties': False, 'required': []},
    'SelectedRetrievalDetails': {'type': 'object', 'properties': {'retrieval_time': {'$ref': '#/$defs/TimeValue'}, 'portion_note': {'type': 'string'}}, 'additionalProperties': False, 'required': []},
    'SelectedRouteDetails': {'type': 'object', 'properties': {'action_type': {'$ref': '#/$defs/enum_action'}, 'valid_window': {'$ref': '#/$defs/TimeWindow'}, 'route_note': {'type': 'string'}}, 'additionalProperties': False, 'required': ['action_type', 'valid_window']},
    'SelectedSupersessionDetails': {'type': 'object', 'properties': {'reason': {'type': 'string'}, 'effective_at': {'$ref': '#/$defs/TimeValue'}}, 'additionalProperties': False, 'required': ['reason']},
    'SelectedIdentityDetails': {'type': 'object', 'properties': {'identity_level': {'$ref': '#/$defs/enum_identity_level'}, 'identity_note': {'type': 'string'}}, 'additionalProperties': False, 'required': ['identity_level']},
    'SelectedAssessmentData': {'type': 'object', 'properties': {'assessment_kind': {'$ref': '#/$defs/enum_assessment_kind'}, 'subject_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'uniqueItems': True}, 'details': {'$ref': '#/$defs/SelectedAssessmentDetails'}}, 'additionalProperties': False, 'required': ['assessment_kind', 'subject_refs', 'details'], 'allOf': [{'if': {'required': ['assessment_kind'], 'properties': {'assessment_kind': {'const': 'origin_boundary'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedOriginBoundaryDetails'}}}}, {'if': {'required': ['assessment_kind'], 'properties': {'assessment_kind': {'const': 'independence'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedIndependenceDetails'}}}}, {'if': {'required': ['assessment_kind'], 'properties': {'assessment_kind': {'const': 'coverage'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedCoverageDetails'}}}}, {'if': {'required': ['assessment_kind'], 'properties': {'assessment_kind': {'const': 'classification'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedClassificationDetails'}}}}, {'if': {'required': ['assessment_kind'], 'properties': {'assessment_kind': {'const': 'verification'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedVerificationDetails'}}}}, {'if': {'required': ['assessment_kind'], 'properties': {'assessment_kind': {'const': 'externality'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedExternalityDetails'}}}}, {'if': {'required': ['assessment_kind'], 'properties': {'assessment_kind': {'const': 'authority'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedAuthorityDetails'}}}}, {'if': {'required': ['assessment_kind'], 'properties': {'assessment_kind': {'const': 'capacity'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedCapacityDetails'}}}}, {'if': {'required': ['assessment_kind'], 'properties': {'assessment_kind': {'const': 'conflict'}}}, 'then': {'properties': {'details': {'$ref': '#/$defs/SelectedConflictDetails'}}}}, {'if': {'required': ['assessment_kind'], 'properties': {'assessment_kind': {'const': 'origin_boundary'}}}, 'then': {'properties': {'subject_refs': {'minItems': 1, 'maxItems': 1}}}}, {'if': {'required': ['assessment_kind'], 'properties': {'assessment_kind': {'const': 'authority'}}}, 'then': {'properties': {'subject_refs': {'minItems': 1, 'maxItems': 1}}}}, {'if': {'required': ['assessment_kind'], 'properties': {'assessment_kind': {'const': 'independence'}}}, 'then': {'properties': {'subject_refs': {'minItems': 2}}}}, {'if': {'required': ['assessment_kind'], 'properties': {'assessment_kind': {'const': 'conflict'}}}, 'then': {'properties': {'subject_refs': {'minItems': 2}}}}, {'if': {'required': ['assessment_kind'], 'properties': {'assessment_kind': {'const': 'coverage'}}}, 'then': {'properties': {'subject_refs': {'minItems': 1}}}}, {'if': {'required': ['assessment_kind', 'details'], 'properties': {'assessment_kind': {'const': 'independence'}, 'details': {'required': ['comparison_form'], 'properties': {'comparison_form': {'const': 'pairwise'}}}}}, 'then': {'properties': {'subject_refs': {'minItems': 2, 'maxItems': 2}}}}]},
    'SelectedOriginBoundaryDetails': {'type': 'object', 'properties': {'dimension': {'$ref': '#/$defs/enum_dimension'}, 'boundary_role': {'$ref': '#/$defs/enum_boundary_role'}, 'coverage_ref': {'anyOf': [{'$ref': '#/$defs/Identifier'}, {'type': 'null'}]}, 'termination_reason': {'type': 'string', 'minLength': 1}}, 'additionalProperties': False, 'required': ['dimension', 'boundary_role', 'coverage_ref', 'termination_reason']},
    'SelectedIndependenceDetails': {'type': 'object', 'properties': {'comparison_form': {'$ref': '#/$defs/enum_comparison_form'}, 'dimension': {'$ref': '#/$defs/enum_dimension'}, 'conclusion': {'$ref': '#/$defs/enum_independence_conclusion'}, 'examined_dependency_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'uniqueItems': True}, 'unexamined_dimensions': {'type': 'array', 'items': {'$ref': '#/$defs/enum_dimension'}}, 'coverage_ref': {'anyOf': [{'$ref': '#/$defs/Identifier'}, {'type': 'null'}]}, 'scope_note': {'type': 'string', 'minLength': 1}}, 'additionalProperties': False, 'required': ['comparison_form', 'dimension', 'conclusion', 'examined_dependency_refs', 'unexamined_dimensions', 'coverage_ref', 'scope_note']},
    'SelectedCoverageDetails': {'type': 'object', 'properties': {'coverage_kind': {'$ref': '#/$defs/enum_coverage_kind'}, 'state': {'$ref': '#/$defs/enum_coverage_state'}, 'relation_types': {'type': 'array', 'items': {'$ref': '#/$defs/enum_predicate'}}, 'dimensions': {'type': 'array', 'items': {'$ref': '#/$defs/enum_dimension'}}, 'member_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'uniqueItems': True}, 'omitted_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'uniqueItems': True}, 'universe_enumerated': {'type': 'boolean'}, 'scope_note': {'type': 'string', 'minLength': 1}}, 'additionalProperties': False, 'required': ['coverage_kind', 'state', 'relation_types', 'dimensions', 'member_refs', 'omitted_refs', 'universe_enumerated', 'scope_note']},
    'SelectedClassificationDetails': {'type': 'object', 'properties': {'axis': {'$ref': '#/$defs/enum_axis'}, 'labels': {'type': 'array', 'items': {'type': 'string'}, 'minItems': 1}, 'verification_assessment_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'uniqueItems': True}, 'scope_note': {'type': 'string'}}, 'additionalProperties': False, 'required': ['axis', 'labels', 'verification_assessment_refs', 'scope_note'], 'allOf': [{'if': {'required': ['axis'], 'properties': {'axis': {'const': 'sil_data_role'}}}, 'then': {'properties': {'labels': {'items': {'$ref': '#/$defs/enum_sil_data_role'}}}}}, {'if': {'required': ['axis'], 'properties': {'axis': {'const': 'hdl_structure_role'}}}, 'then': {'properties': {'labels': {'items': {'$ref': '#/$defs/enum_hdl_structure_role'}}}}}, {'if': {'required': ['axis'], 'properties': {'axis': {'const': 'sil_governance_layer'}}}, 'then': {'properties': {'labels': {'items': {'$ref': '#/$defs/enum_sil_governance_layer'}}}}}]},
    'SelectedVerificationDetails': {'type': 'object', 'properties': {'verification_scope': {'$ref': '#/$defs/enum_verification_scope'}, 'evaluation_ref': {'anyOf': [{'$ref': '#/$defs/Identifier'}, {'type': 'null'}]}, 'reported_outcome': {'$ref': '#/$defs/enum_reported_outcome'}, 'valid_window': {'$ref': '#/$defs/TimeWindow'}, 'scope_note': {'type': 'string'}}, 'additionalProperties': False, 'required': ['verification_scope', 'evaluation_ref', 'reported_outcome', 'valid_window', 'scope_note']},
    'SelectedExternalityDetails': {'type': 'object', 'properties': {'boundary_inquiry_ref': {'$ref': '#/$defs/Identifier'}, 'conclusion': {'$ref': '#/$defs/enum_externality_conclusion'}, 'grounding_basis': {'anyOf': [{'type': 'string', 'minLength': 1}, {'type': 'null'}]}, 'relevant_time': {'$ref': '#/$defs/TimeValue'}}, 'additionalProperties': False, 'required': ['boundary_inquiry_ref', 'conclusion', 'grounding_basis', 'relevant_time']},
    'SelectedAuthorityDetails': {'type': 'object', 'properties': {'target_refs': {'type': 'array', 'items': {'$ref': '#/$defs/Identifier'}, 'uniqueItems': True}, 'action_types': {'type': 'array', 'items': {'$ref': '#/$defs/enum_action'}}, 'valid_window': {'$ref': '#/$defs/TimeWindow'}, 'authorized_by_ref': {'$ref': '#/$defs/Identifier'}, 'grant_state': {'$ref': '#/$defs/enum_grant_state'}, 'authority_basis': {'anyOf': [{'type': 'string', 'minLength': 1}, {'type': 'null'}]}, 'coverage_ref': {'anyOf': [{'$ref': '#/$defs/Identifier'}, {'type': 'null'}]}}, 'additionalProperties': False, 'required': ['target_refs', 'action_types', 'valid_window', 'authorized_by_ref', 'grant_state', 'authority_basis', 'coverage_ref']},
    'SelectedCapacityDetails': {'type': 'object', 'properties': {'reported_capacity': {'anyOf': [{'type': 'string'}, {'type': 'null'}]}, 'unit': {'anyOf': [{'type': 'string'}, {'type': 'null'}]}, 'horizon': {'$ref': '#/$defs/TimeWindow'}, 'reported_load': {'anyOf': [{'type': 'string'}, {'type': 'null'}]}, 'scope_note': {'type': 'string'}}, 'additionalProperties': False, 'required': ['reported_capacity', 'unit', 'horizon', 'reported_load', 'scope_note']},
    'SelectedConflictDetails': {'type': 'object', 'properties': {'conflict_kind': {'$ref': '#/$defs/enum_conflict_kind'}, 'resolution_state': {'$ref': '#/$defs/enum_resolution_state'}, 'resolution_evaluation_ref': {'anyOf': [{'$ref': '#/$defs/Identifier'}, {'type': 'null'}]}, 'scope_note': {'type': 'string'}}, 'additionalProperties': False, 'required': ['conflict_kind', 'resolution_state', 'resolution_evaluation_ref', 'scope_note'], 'allOf': [{'if': {'required': ['resolution_state'], 'properties': {'resolution_state': {'const': 'unresolved'}}}, 'then': {'properties': {'resolution_evaluation_ref': {'type': 'null'}}}, 'else': {'properties': {'resolution_evaluation_ref': {'$ref': '#/$defs/Identifier'}}}}]},
    'SelectedRecordData': {'anyOf': [{'$ref': '#/$defs/SelectedClaimData'}, {'$ref': '#/$defs/SelectedArtifactData'}, {'$ref': '#/$defs/SelectedActorData'}, {'$ref': '#/$defs/SelectedEvidenceItemData'}, {'$ref': '#/$defs/SelectedOriginEventData'}, {'$ref': '#/$defs/SelectedModelData'}, {'$ref': '#/$defs/SelectedEvaluationData'}, {'$ref': '#/$defs/SelectedCorrectionChannelData'}, {'$ref': '#/$defs/SelectedCorrectionEventData'}, {'$ref': '#/$defs/SelectedPipelineRecordData'}, {'$ref': '#/$defs/SelectedAnomalyData'}, {'$ref': '#/$defs/SelectedUnresolvedReferenceData'}]},
    'SelectedAssertionData': {'anyOf': [{'$ref': '#/$defs/SelectedRelationData'}, {'$ref': '#/$defs/SelectedAssessmentData'}]},
    'SelectedCorrectionDetails': {'anyOf': [{'$ref': '#/$defs/SelectedSubmissionDetails'}, {'$ref': '#/$defs/SelectedHandlingDetails'}, {'$ref': '#/$defs/SelectedChangeDetails'}]},
    'SelectedRelationDetails': {'anyOf': [{'$ref': '#/$defs/SelectedStanceDetails'}, {'$ref': '#/$defs/SelectedCitationDetails'}, {'$ref': '#/$defs/SelectedTransformationDetails'}, {'$ref': '#/$defs/SelectedOriginDetails'}, {'$ref': '#/$defs/SelectedAgentDetails'}, {'$ref': '#/$defs/SelectedModelDetails'}, {'$ref': '#/$defs/SelectedRetrievalDetails'}, {'$ref': '#/$defs/SelectedRouteDetails'}, {'$ref': '#/$defs/SelectedSupersessionDetails'}, {'$ref': '#/$defs/SelectedIdentityDetails'}]},
    'SelectedAssessmentDetails': {'anyOf': [{'$ref': '#/$defs/SelectedOriginBoundaryDetails'}, {'$ref': '#/$defs/SelectedIndependenceDetails'}, {'$ref': '#/$defs/SelectedCoverageDetails'}, {'$ref': '#/$defs/SelectedClassificationDetails'}, {'$ref': '#/$defs/SelectedVerificationDetails'}, {'$ref': '#/$defs/SelectedExternalityDetails'}, {'$ref': '#/$defs/SelectedAuthorityDetails'}, {'$ref': '#/$defs/SelectedCapacityDetails'}, {'$ref': '#/$defs/SelectedConflictDetails'}]},
    'enum_record_kind': {'type': 'string', 'enum': ['claim', 'artifact', 'actor', 'evidence_item', 'origin_event', 'model', 'evaluation', 'correction_channel', 'correction_event', 'pipeline_record', 'anomaly', 'unresolved_reference']},
    'enum_predicate': {'type': 'string', 'enum': ['supports', 'contradicts', 'describes', 'qualifies', 'contextualizes', 'corroborates', 'cites', 'derived_from', 'copies', 'syndicated_from', 'summarizes', 'translates', 'quotes', 'originates_from', 'depends_on', 'generated_by', 'published_by', 'model_derived_from', 'trained_on', 'owned_by', 'retrieved_from', 'propagates_to', 'supersedes', 'same_identity_as']},
    'enum_assessment_kind': {'type': 'string', 'enum': ['origin_boundary', 'independence', 'coverage', 'classification', 'verification', 'externality', 'authority', 'capacity', 'conflict']},
    'enum_dimension': {'type': 'string', 'enum': ['acquisition', 'analytical_method', 'model_ancestry', 'evaluation_rubric', 'organizational_control']},
    'enum_basis_kind': {'type': 'string', 'enum': ['declaration', 'documented_record', 'upstream_inference', 'protected_attestation', 'unspecified']},
    'enum_gap_reason': {'type': 'string', 'enum': ['not_recorded', 'not_examined', 'withheld', 'unavailable', 'identity_ambiguous', 'outside_snapshot', 'not_applicable', 'other']},
    'enum_reference_kind': {'type': 'string', 'enum': ['supplied_excerpt', 'record_pointer', 'local_locator', 'external_locator', 'protected_attestation']},
    'enum_availability': {'type': 'string', 'enum': ['supplied', 'locator_only', 'withheld', 'unavailable']},
    'enum_artifact_kind': {'type': 'string', 'enum': ['document', 'dataset', 'answer', 'reference_answer', 'rubric', 'benchmark', 'judgment', 'observation_record', 'execution_result', 'other', 'unknown']},
    'enum_actor_kind': {'type': 'string', 'enum': ['human', 'organization', 'software_agent', 'unknown']},
    'enum_identity_disclosure': {'type': 'string', 'enum': ['named', 'pseudonymous', 'protected', 'unknown']},
    'enum_epistemic_type': {'type': 'string', 'enum': ['measurement', 'testimony', 'documentary_statement', 'estimate', 'formal_derivation', 'execution_result', 'analytical_inference', 'evaluative_judgment', 'allegation', 'fictional_example', 'unclassified']},
    'enum_origin_event_kind': {'type': 'string', 'enum': ['observation', 'data_collection', 'testimony', 'documentary_issuance', 'analysis', 'formal_check', 'execution', 'other', 'unknown']},
    'enum_evaluation_kind': {'type': 'string', 'enum': ['judgment', 'formal_check', 'execution', 'empirical_review', 'human_review', 'identity_process_review', 'other', 'unknown']},
    'enum_role': {'type': 'string', 'enum': ['candidate', 'generator', 'judge', 'executor', 'human_reviewer', 'reference_answer', 'rubric', 'validation_environment', 'method_input']},
    'enum_action': {'type': 'string', 'enum': ['review', 'amend', 'annotate', 'retract', 'rerun', 'rollback', 'replace_evaluator', 'restrict_scope', 'withdraw', 'metadata_correction', 'other']},
    'enum_correction_event_kind': {'type': 'string', 'enum': ['submission', 'handling', 'change']},
    'enum_submission_kind': {'type': 'string', 'enum': ['objection', 'proposed_correction', 'appeal']},
    'enum_outcome': {'type': 'string', 'enum': ['acknowledged', 'under_review', 'accepted', 'rejected', 'withdrawn', 'failed', 'unknown']},
    'enum_stage': {'type': 'string', 'enum': ['admission', 'preservation', 'selection', 'influence']},
    'enum_pipeline_state': {'type': 'string', 'enum': ['occurred', 'did_not_occur', 'unknown']},
    'enum_linkage_kind': {'type': 'string', 'enum': ['use_record', 'comparison_record', 'experimental_attribution', 'declaration', 'unspecified']},
    'enum_classification_state': {'type': 'string', 'enum': ['unclassified', 'caller_classified']},
    'enum_assertion_kind': {'type': 'string', 'enum': ['relation', 'assessment']},
    'enum_lifecycle_state': {'type': 'string', 'enum': ['active', 'withdrawn', 'superseded']},
    'enum_polarity': {'type': 'string', 'enum': ['affirmed', 'denied']},
    'enum_identity_level': {'type': 'string', 'enum': ['artifact_version', 'actor', 'origin_event', 'model_version']},
    'enum_boundary_role': {'type': 'string', 'enum': ['documented_origin', 'declared_origin', 'reference_baseline', 'scope_cut', 'unresolved']},
    'enum_comparison_form': {'type': 'string', 'enum': ['pairwise', 'setwise']},
    'enum_independence_conclusion': {'type': 'string', 'enum': ['independent_process', 'shared_dependency', 'partial_overlap', 'unknown', 'not_assessed', 'not_applicable']},
    'enum_coverage_kind': {'type': 'string', 'enum': ['upstream_history', 'citation_list', 'identity', 'model_history', 'correction_routes', 'pipeline_universe', 'other']},
    'enum_coverage_state': {'type': 'string', 'enum': ['complete_for_scope', 'partial', 'not_examined']},
    'enum_axis': {'type': 'string', 'enum': ['sil_data_role', 'hdl_structure_role', 'sil_governance_layer']},
    'enum_sil_data_role': {'type': 'string', 'enum': ['surface_linguistic', 'world_model', 'judgment']},
    'enum_hdl_structure_role': {'type': 'string', 'enum': ['surface_linguistic_structure', 'world_structure', 'judgment_structure']},
    'enum_sil_governance_layer': {'type': 'string', 'enum': ['open_web', 'verified', 'contested', 'judgment']},
    'enum_verification_scope': {'type': 'string', 'enum': ['identity', 'process', 'byte_integrity', 'other']},
    'enum_reported_outcome': {'type': 'string', 'enum': ['verified', 'not_verified', 'inconclusive', 'revoked', 'unknown']},
    'enum_externality_conclusion': {'type': 'string', 'enum': ['external', 'internal', 'mixed', 'unknown']},
    'enum_grant_state': {'type': 'string', 'enum': ['granted', 'denied', 'expired', 'unknown']},
    'enum_conflict_kind': {'type': 'string', 'enum': ['affirmation_denial', 'incompatible_origin', 'incompatible_independence', 'identity_dispute', 'scope_dispute', 'other']},
    'enum_resolution_state': {'type': 'string', 'enum': ['unresolved', 'externally_resolved']},
    'enum_resolved_kind': {'type': 'string', 'enum': ['claim', 'artifact', 'actor', 'evidence_item', 'origin_event', 'model', 'evaluation', 'correction_channel', 'correction_event', 'pipeline_record', 'anomaly']},
    'enum_endpoint_gap_reason': {'type': 'string', 'enum': ['not_recorded', 'not_examined', 'withheld', 'unavailable', 'identity_ambiguous', 'outside_snapshot', 'other']},
    'SelectedNative': {'oneOf': [{'$ref': '#/$defs/SelectedInquiry'}, {'$ref': '#/$defs/SelectedRecord'}, {'$ref': '#/$defs/SelectedAssertion'}, {'$ref': '#/$defs/SelectedEvidenceReference'}]},
    'SelectedPipelineRecord': {'allOf': [{'$ref': '#/$defs/SelectedRecord'}, {'properties': {'kind': {'const': 'pipeline_record'}}}]},
    'SelectedUnresolvedRecord': {'allOf': [{'$ref': '#/$defs/SelectedRecord'}, {'properties': {'kind': {'const': 'unresolved_reference'}}}]},
    'SelectedCoverageAssertion': {'allOf': [{'$ref': '#/$defs/SelectedAssertion'}, {'properties': {'assertion_kind': {'const': 'assessment'}, 'data': {'properties': {'assessment_kind': {'const': 'coverage'}}}}}]},
    'SelectedCapacityAssertion': {'allOf': [{'$ref': '#/$defs/SelectedAssertion'}, {'properties': {'assertion_kind': {'const': 'assessment'}, 'data': {'properties': {'assessment_kind': {'const': 'capacity'}}}}}]},
    'OriginBoundaryFields': {'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedNative'}, 'qualification_state': {'type': 'string', 'enum': ['met', 'unmet']}, 'reason_codes': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonCode'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['native_record', 'qualification_state', 'reason_codes']},
    'CoverageFields': {'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedCoverageAssertion'}, 'qualification_state': {'type': 'string', 'enum': ['met', 'unmet']}, 'reason_codes': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonCode'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['native_record', 'qualification_state', 'reason_codes']},
    'DocumentaryBasisGapFields': {'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedNative'}, 'qualification_state': {'type': 'string', 'enum': ['met', 'unmet']}, 'reason_codes': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonCode'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['native_record', 'qualification_state', 'reason_codes']},
    'IndependenceAssessmentFields': {'anyOf': [{'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedNative'}}, 'additionalProperties': False, 'required': ['native_record']}, {'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedNative'}, 'process_qualification_state': {'type': 'string', 'enum': ['met', 'unmet']}, 'origin_qualification_state': {'type': 'string', 'enum': ['met', 'unmet', 'not_applicable']}, 'reason_codes': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonCode'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['native_record', 'process_qualification_state', 'origin_qualification_state', 'reason_codes']}]},
    'GapSource': {'type': 'object', 'properties': {'source': {'$ref': '#/$defs/InputRef'}, 'reason_codes': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonCode'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['source', 'reason_codes']},
    'GapCoverage': {'type': 'object', 'properties': {'coverage_ref': {'$ref': '#/$defs/AssertionRef'}, 'qualification_state': {'type': 'string', 'enum': ['met', 'unmet']}, 'reason_codes': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonCode'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['coverage_ref', 'qualification_state', 'reason_codes']},
    'GapWitnessPath': {'type': 'object', 'properties': {'nodes': {'type': 'array', 'items': {'$ref': '#/$defs/InputRef'}}, 'assertions': {'type': 'array', 'items': {'$ref': '#/$defs/AssertionRef'}}}, 'additionalProperties': False, 'required': ['nodes', 'assertions']},
    'AncestryGapFields': {'type': 'object', 'properties': {'seed_ref': {'$ref': '#/$defs/RecordRef'}, 'dimension': {'$ref': '#/$defs/DependencyDimension'}, 'gaps': {'type': 'array', 'items': {'$ref': '#/$defs/GapSource'}}, 'frontiers': {'type': 'array', 'items': {'$ref': '#/$defs/SelectedUnresolvedRecord'}}, 'coverage': {'type': 'array', 'items': {'$ref': '#/$defs/GapCoverage'}}, 'witness_paths': {'type': 'array', 'items': {'$ref': '#/$defs/GapWitnessPath'}}}, 'additionalProperties': False, 'required': ['seed_ref', 'dimension', 'gaps', 'frontiers', 'coverage', 'witness_paths']},
    'OneSidedAncestry': {'type': 'object', 'properties': {'from_ref': {'$ref': '#/$defs/InputRef'}, 'to_ref': {'$ref': '#/$defs/InputRef'}}, 'additionalProperties': False, 'required': ['from_ref', 'to_ref']},
    'EvaluatorOverlapFields': {'anyOf': [{'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedNative'}}, 'additionalProperties': False, 'required': ['native_record']}, {'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedNative'}, 'roles': {'type': 'array', 'items': {'$ref': '#/$defs/enum_role'}}, 'left_object_refs': {'type': 'array', 'items': {'$ref': '#/$defs/InputRef'}, 'uniqueItems': True}, 'right_object_refs': {'type': 'array', 'items': {'$ref': '#/$defs/InputRef'}, 'uniqueItems': True}, 'shared_object_refs': {'type': 'array', 'items': {'$ref': '#/$defs/InputRef'}, 'uniqueItems': True}, 'common_ancestor_refs': {'type': 'array', 'items': {'$ref': '#/$defs/InputRef'}, 'uniqueItems': True}, 'matching_family_labels': {'type': 'array', 'items': {'type': 'string'}}, 'missing_family_model_refs': {'type': 'array', 'items': {'$ref': '#/$defs/RecordRef'}, 'uniqueItems': True}, 'one_sided_ancestry': {'type': 'array', 'items': {'$ref': '#/$defs/OneSidedAncestry'}}, 'roles_complete': {'type': 'boolean'}}, 'additionalProperties': False, 'required': ['native_record', 'roles', 'left_object_refs', 'right_object_refs', 'shared_object_refs', 'common_ancestor_refs', 'matching_family_labels', 'missing_family_model_refs', 'one_sided_ancestry', 'roles_complete']}]},
    'ExternalityAssessmentFields': {'anyOf': [{'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedNative'}}, 'additionalProperties': False, 'required': ['native_record']}, {'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedNative'}, 'qualification_state': {'type': 'string', 'enum': ['met', 'unmet']}, 'qualified_externality': {'type': 'string', 'enum': ['available', 'unavailable']}, 'reason_codes': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonCode'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['native_record', 'qualification_state', 'qualified_externality', 'reason_codes']}]},
    'PipelineStageFields': {'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedPipelineRecord'}, 'qualification_state': {'type': 'string', 'enum': ['met', 'unmet']}, 'reason_codes': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonCode'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['native_record', 'qualification_state', 'reason_codes']},
    'ExternalityStageFields': {'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedPipelineRecord'}, 'qualification_state': {'type': 'string', 'enum': ['met', 'unmet']}, 'reason_codes': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonCode'}, 'uniqueItems': True}, 'externality_subject_refs': {'type': 'array', 'items': {'$ref': '#/$defs/InputRef'}, 'uniqueItems': True}, 'mapping_assertion_refs': {'type': 'array', 'items': {'$ref': '#/$defs/AssertionRef'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['native_record', 'qualification_state', 'reason_codes', 'externality_subject_refs', 'mapping_assertion_refs']},
    'StageAnchor': {'type': 'object', 'properties': {'run_key': {'type': 'string'}, 'stage_key': {'type': 'string'}, 'stage': {'$ref': '#/$defs/enum_stage'}}, 'additionalProperties': False, 'required': ['run_key', 'stage_key', 'stage']},
    'CohortTransitionFields': {'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedCoverageAssertion'}, 'stage_anchor': {'anyOf': [{'$ref': '#/$defs/StageAnchor'}, {'type': 'null'}]}, 'cohort_qualification_state': {'type': 'string', 'enum': ['met', 'unmet']}, 'transition_qualification_state': {'type': 'string', 'enum': ['met', 'unmet']}, 'reason_codes': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonCode'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['native_record', 'stage_anchor', 'cohort_qualification_state', 'transition_qualification_state', 'reason_codes']},
    'CorrectionRouteFields': {'anyOf': [{'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedNative'}}, 'additionalProperties': False, 'required': ['native_record']}, {'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedNative'}, 'target_ref': {'$ref': '#/$defs/InputRef'}, 'action_type': {'$ref': '#/$defs/enum_action'}, 'declared_route_recorded': {'type': 'boolean'}, 'authorized_route_recorded': {'type': 'boolean'}, 'authorized_route_state': {'type': 'string', 'enum': ['available', 'unavailable']}, 'absence_description': {'type': 'string', 'enum': ['bounded_absence_under_declared_coverage', 'no_witness_in_examined_view', 'positive_witness']}}, 'additionalProperties': False, 'required': ['native_record', 'target_ref', 'action_type', 'declared_route_recorded', 'authorized_route_recorded', 'authorized_route_state', 'absence_description']}, {'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedNative'}, 'grant_qualification_state': {'type': 'string', 'enum': ['met', 'unmet', 'unknown']}, 'grant_matches_tuple': {'type': 'boolean'}, 'grant_reason_codes': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonCode'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['native_record', 'grant_qualification_state', 'grant_matches_tuple', 'grant_reason_codes']}]},
    'CorrectionCaseFields': {'anyOf': [{'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedNative'}}, 'additionalProperties': False, 'required': ['native_record']}, {'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedNative'}, 'documentary_state': {'type': 'string', 'enum': ['met', 'unknown']}, 'explicit_removal': {'type': 'boolean'}, 'reason_codes': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonCode'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['native_record', 'documentary_state', 'explicit_removal', 'reason_codes']}]},
    'CaseChangeRow': {'type': 'object', 'properties': {'case_ref': {'$ref': '#/$defs/RecordRef'}, 'declared': {'type': 'boolean'}, 'selected': {'type': 'boolean'}, 'change_event_refs': {'type': 'array', 'items': {'$ref': '#/$defs/RecordRef'}, 'uniqueItems': True}, 'qualified_change_event_refs': {'type': 'array', 'items': {'$ref': '#/$defs/RecordRef'}, 'uniqueItems': True}, 'documentary_state': {'type': 'string', 'enum': ['met', 'unknown']}, 'requested_effect_state': {'type': 'string', 'enum': ['available', 'unavailable']}, 'reason_codes': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonCode'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['case_ref', 'declared', 'selected', 'change_event_refs', 'qualified_change_event_refs', 'documentary_state', 'requested_effect_state', 'reason_codes']},
    'CorrectionTargetChangeFields': {'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedNative'}, 'case_rows': {'type': 'array', 'items': {'$ref': '#/$defs/CaseChangeRow'}}}, 'additionalProperties': False, 'required': ['native_record', 'case_rows']},
    'ReportedCapacityFields': {'anyOf': [{'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedCapacityAssertion'}}, 'additionalProperties': False, 'required': ['native_record']}, {'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedCapacityAssertion'}, 'documentary_state': {'type': 'string', 'enum': ['met', 'unmet']}, 'reason_codes': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonCode'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['native_record', 'documentary_state', 'reason_codes']}]},
    'HumanContributionFields': {'anyOf': [{'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedNative'}}, 'additionalProperties': False, 'required': ['native_record']}, {'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedNative'}, 'contribution_status': {'type': 'string', 'enum': ['distinct_constraint', 'no_human_role', 'missing_contribution', 'recorded_human_contribution']}, 'documentary_state': {'type': 'string', 'enum': ['met', 'unmet']}, 'identity_state': {'type': 'string', 'enum': ['met', 'unmet']}, 'reason_codes': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonCode'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['native_record', 'contribution_status', 'documentary_state', 'identity_state', 'reason_codes']}]},
    'CorrectiveIndependenceFields': {'anyOf': [{'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedNative'}}, 'additionalProperties': False, 'required': ['native_record']}, {'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedNative'}, 'contribution_status': {'type': 'string', 'enum': ['distinct_constraint', 'no_human_role', 'missing_contribution', 'recorded_human_contribution']}, 'documentary_state': {'type': 'string', 'enum': ['met', 'unmet']}, 'identity_state': {'type': 'string', 'enum': ['met', 'unmet']}, 'reason_codes': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonCode'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['native_record', 'contribution_status', 'documentary_state', 'identity_state', 'reason_codes']}, {'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedNative'}, 'process_qualification_state': {'type': 'string', 'enum': ['met', 'unmet']}, 'origin_qualification_state': {'type': 'string', 'enum': ['met', 'unmet', 'not_applicable']}, 'reason_codes': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonCode'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['native_record', 'process_qualification_state', 'origin_qualification_state', 'reason_codes']}]},
    'AnomalyContextFields': {'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedNative'}, 'context_records': {'type': 'array', 'items': {'$ref': '#/$defs/SelectedNative'}}, 'reason_codes': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonCode'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['native_record', 'context_records', 'reason_codes']},
    'ContestationFields': {'type': 'object', 'properties': {'native_record': {'$ref': '#/$defs/SelectedNative'}, 'context_records': {'type': 'array', 'items': {'$ref': '#/$defs/SelectedNative'}}, 'reason_codes': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonCode'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['native_record', 'context_records', 'reason_codes']},
    'TailStageResultLinkFields': {'type': 'object', 'properties': {'source_result_state': {'type': 'string', 'enum': ['available', 'unavailable', 'not_applicable', 'not_evaluated']}, 'source_value_kind': {'$ref': '#/$defs/ValueKind'}}, 'additionalProperties': False, 'required': ['source_result_state', 'source_value_kind']},
    'Disclosure': {'type': 'object', 'properties': {'source': {'anyOf': [{'$ref': '#/$defs/InputRef'}, {'$ref': '#/$defs/ResultId'}]}, 'fields': {'anyOf': [{'$ref': '#/$defs/OriginBoundaryFields'}, {'$ref': '#/$defs/CoverageFields'}, {'$ref': '#/$defs/DocumentaryBasisGapFields'}, {'$ref': '#/$defs/IndependenceAssessmentFields'}, {'$ref': '#/$defs/AncestryGapFields'}, {'$ref': '#/$defs/EvaluatorOverlapFields'}, {'$ref': '#/$defs/ExternalityAssessmentFields'}, {'$ref': '#/$defs/PipelineStageFields'}, {'$ref': '#/$defs/ExternalityStageFields'}, {'$ref': '#/$defs/CohortTransitionFields'}, {'$ref': '#/$defs/CorrectionRouteFields'}, {'$ref': '#/$defs/CorrectionCaseFields'}, {'$ref': '#/$defs/CorrectionTargetChangeFields'}, {'$ref': '#/$defs/ReportedCapacityFields'}, {'$ref': '#/$defs/HumanContributionFields'}, {'$ref': '#/$defs/CorrectiveIndependenceFields'}, {'$ref': '#/$defs/AnomalyContextFields'}, {'$ref': '#/$defs/ContestationFields'}, {'$ref': '#/$defs/TailStageResultLinkFields'}]}, 'qualifications': {'type': 'array', 'items': {'type': 'string'}}}, 'additionalProperties': False, 'required': ['source', 'fields', 'qualifications']},
    'GraphNode': {'type': 'object', 'properties': {'ref': {'allOf': [{'$ref': '#/$defs/InputRef'}, {'properties': {'selector': {'type': 'null'}}}]}, 'kind': {'type': 'string', 'enum': ['claim', 'artifact', 'actor', 'evidence_item', 'origin_event', 'model', 'evaluation', 'correction_channel', 'correction_event', 'pipeline_record', 'anomaly', 'unresolved_reference', 'inquiry', 'assertion', 'evidence_reference']}}, 'additionalProperties': False, 'required': ['ref', 'kind'], 'allOf': [{'if': {'required': ['kind'], 'properties': {'kind': {'const': 'inquiry'}}}, 'then': {'properties': {'ref': {'$ref': '#/$defs/InquiryRef'}}}}, {'if': {'required': ['kind'], 'properties': {'kind': {'const': 'assertion'}}}, 'then': {'properties': {'ref': {'$ref': '#/$defs/AssertionRef'}}}}, {'if': {'required': ['kind'], 'properties': {'kind': {'const': 'evidence_reference'}}}, 'then': {'properties': {'ref': {'$ref': '#/$defs/EvidenceRef'}}}}, {'if': {'required': ['kind'], 'properties': {'kind': {'type': 'string', 'enum': ['claim', 'artifact', 'actor', 'evidence_item', 'origin_event', 'model', 'evaluation', 'correction_channel', 'correction_event', 'pipeline_record', 'anomaly', 'unresolved_reference']}}}, 'then': {'properties': {'ref': {'$ref': '#/$defs/RecordRef'}}}}]},
    'GraphEdge': {'type': 'object', 'properties': {'source': {'$ref': '#/$defs/GraphNode'}, 'target': {'$ref': '#/$defs/GraphNode'}, 'source_ref': {'$ref': '#/$defs/InputRef'}, 'predicate': {'anyOf': [{'$ref': '#/$defs/enum_predicate'}, {'type': 'null'}]}, 'eligible': {'type': 'boolean'}, 'reason_codes': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonCode'}, 'uniqueItems': True}}, 'additionalProperties': False, 'required': ['source', 'target', 'source_ref', 'predicate', 'eligible', 'reason_codes'], 'allOf': [{'if': {'required': ['predicate'], 'properties': {'predicate': {'type': 'null'}}}, 'then': {'properties': {'source_ref': {'allOf': [{'$ref': '#/$defs/InputRef'}, {'properties': {'selector': {'type': 'string', 'minLength': 1}}}]}}}, 'else': {'properties': {'source_ref': {'allOf': [{'$ref': '#/$defs/AssertionRef'}, {'properties': {'selector': {'type': 'null'}}}]}}}}]},
    'GraphWitnessComponent': {'type': 'object', 'properties': {'type': {'const': 'graph_witness'}, 'kind': {'type': 'string', 'enum': ['path', 'cycle', 'members', 'complete_trace', 'no_witness_in_examined_view']}, 'nodes': {'type': 'array', 'items': {'$ref': '#/$defs/GraphNode'}}, 'members': {'type': 'array', 'items': {'$ref': '#/$defs/GraphNode'}}, 'starts': {'type': 'array', 'items': {'$ref': '#/$defs/GraphNode'}}, 'examined_nodes': {'type': 'array', 'items': {'$ref': '#/$defs/GraphNode'}}, 'frontiers': {'type': 'array', 'items': {'$ref': '#/$defs/GraphNode'}}, 'terminals': {'type': 'array', 'items': {'$ref': '#/$defs/GraphNode'}}, 'edges': {'type': 'array', 'items': {'$ref': '#/$defs/GraphEdge'}}, 'internal_edges': {'type': 'array', 'items': {'$ref': '#/$defs/GraphEdge'}}, 'exit_edges': {'type': 'array', 'items': {'$ref': '#/$defs/GraphEdge'}}, 'examined_edges': {'type': 'array', 'items': {'$ref': '#/$defs/GraphEdge'}}, 'observations': {'type': 'array', 'items': {'$ref': '#/$defs/GraphEdge'}}, 'target': {'anyOf': [{'$ref': '#/$defs/GraphNode'}, {'type': 'null'}]}, 'member_count': {'type': 'integer', 'minimum': 0, 'maximum': 9007199254740991}}, 'additionalProperties': False, 'required': ['type', 'kind', 'nodes', 'members', 'starts', 'examined_nodes', 'frontiers', 'terminals', 'edges', 'internal_edges', 'exit_edges', 'examined_edges', 'observations', 'target', 'member_count']},
    'InventoryWitnessComponent': {'type': 'object', 'properties': {'type': {'const': 'inventory_witness'}, 'members': {'type': 'array', 'items': {'$ref': '#/$defs/InputRef'}, 'uniqueItems': True}, 'member_count': {'type': 'integer', 'minimum': 0, 'maximum': 9007199254740991}}, 'additionalProperties': False, 'required': ['type', 'members', 'member_count']},
    'ComparisonWitnessComponent': {'type': 'object', 'properties': {'type': {'const': 'comparison_witness'}, 'members': {'type': 'array', 'items': {'$ref': '#/$defs/InputRef'}, 'uniqueItems': True}, 'assessment': {'anyOf': [{'$ref': '#/$defs/AssertionRef'}, {'type': 'null'}]}, 'examined_assessments': {'type': 'array', 'items': {'$ref': '#/$defs/AssertionRef'}, 'uniqueItems': True}, 'member_count': {'type': 'integer', 'minimum': 0, 'maximum': 9007199254740991}}, 'additionalProperties': False, 'required': ['type', 'members', 'assessment', 'examined_assessments', 'member_count']},
    'SelectedMembersComponent': {'type': 'object', 'properties': {'type': {'const': 'selected_members'}, 'members': {'type': 'array', 'items': {'$ref': '#/$defs/InputRef'}, 'uniqueItems': True}, 'member_count': {'type': 'integer', 'minimum': 0, 'maximum': 9007199254740991}}, 'additionalProperties': False, 'required': ['type', 'members', 'member_count']},
    'HumanReviewWitnessComponent': {'type': 'object', 'properties': {'type': {'const': 'human_review_witness'}, 'members': {'type': 'array', 'items': {'$ref': '#/$defs/InputRef'}, 'uniqueItems': True}, 'examined_assessments': {'type': 'array', 'items': {'$ref': '#/$defs/AssertionRef'}, 'uniqueItems': True}, 'source_refs': {'type': 'array', 'items': {'$ref': '#/$defs/InputRef'}}, 'member_count': {'type': 'integer', 'minimum': 0, 'maximum': 9007199254740991}}, 'additionalProperties': False, 'required': ['type', 'members', 'examined_assessments', 'source_refs', 'member_count']},
    'CorrectionOutcomeWitnessComponent': {'type': 'object', 'properties': {'type': {'const': 'correction_outcome_witness'}, 'members': {'type': 'array', 'items': {'$ref': '#/$defs/InputRef'}, 'uniqueItems': True}, 'source_refs': {'type': 'array', 'items': {'$ref': '#/$defs/InputRef'}}, 'member_count': {'type': 'integer', 'minimum': 0, 'maximum': 9007199254740991}}, 'additionalProperties': False, 'required': ['type', 'members', 'source_refs', 'member_count']},
    'WitnessComponent': {'oneOf': [{'$ref': '#/$defs/GraphWitnessComponent'}, {'$ref': '#/$defs/InventoryWitnessComponent'}, {'$ref': '#/$defs/ComparisonWitnessComponent'}, {'$ref': '#/$defs/SelectedMembersComponent'}, {'$ref': '#/$defs/HumanReviewWitnessComponent'}, {'$ref': '#/$defs/CorrectionOutcomeWitnessComponent'}]},
    'FindingWitness': {'type': 'object', 'properties': {'input_refs': {'type': 'array', 'items': {'$ref': '#/$defs/InputRef'}, 'uniqueItems': True}, 'components': {'type': 'array', 'items': {'$ref': '#/$defs/WitnessComponent'}}}, 'additionalProperties': False, 'required': ['input_refs', 'components']},
    'Finding': {'type': 'object', 'properties': {'id': {'$ref': '#/$defs/FindingId'}, 'observation_kind': {'type': 'string', 'enum': ['positive_witness', 'no_witness_in_examined_view', 'bounded_absence_under_declared_coverage', 'attributed_observation', 'qualification_gap', 'recorded_conflict']}, 'condition_code': {'type': 'string', 'enum': ['shared_origin_witness', 'citation_path_witness', 'transformation_path_witness', 'model_mediated_derivation_witness', 'view_cycle_witness', 'assurance_loop_limitation', 'evaluator_overlap_witness', 'family_label_match', 'provenance_gap', 'verification_scope_limitation', 'independence_record_conflict', 'correction_dependency_witness', 'correction_route_limitation', 'case_handling_disclosure', 'linked_change_disclosure', 'downstream_change_undocumented', 'externality_stage_limitation', 'recorded_stage_exclusion', 'anomaly_or_contestation_disclosure', 'attributed_external_observation', 'scoped_no_witness', 'recorded_data_conflict']}, 'diagnostic_refs': {'type': 'array', 'items': {'$ref': '#/$defs/DiagnosticId'}, 'uniqueItems': True}, 'threat_family_refs': {'type': 'array', 'items': {'type': 'string', 'enum': ['SIT-TH001', 'SIT-TH002', 'SIT-TH003', 'SIT-TH004', 'SIT-TH005', 'SIT-TH006', 'SIT-TH007', 'SIT-TH008', 'SIT-TH009', 'SIT-TH010', 'SIT-TH011', 'SIT-TH012', 'SIT-TH013', 'SIT-TH014']}, 'uniqueItems': True}, 'scope_ref': {'$ref': '#/$defs/ScopeId'}, 'population_refs': {'type': 'array', 'items': {'$ref': '#/$defs/PopulationId'}, 'uniqueItems': True}, 'basis_refs': {'type': 'array', 'items': {'$ref': '#/$defs/BasisId'}, 'uniqueItems': True}, 'witness': {'$ref': '#/$defs/FindingWitness'}, 'contrary_input_refs': {'type': 'array', 'items': {'$ref': '#/$defs/InputRef'}, 'uniqueItems': True}, 'reason_refs': {'type': 'array', 'items': {'$ref': '#/$defs/ReasonId'}, 'uniqueItems': True}, 'statement': {'type': 'string', 'minLength': 1}, 'interpretation_limit': {'type': 'string', 'minLength': 1}}, 'additionalProperties': False, 'required': ['id', 'observation_kind', 'condition_code', 'diagnostic_refs', 'threat_family_refs', 'scope_ref', 'population_refs', 'basis_refs', 'witness', 'contrary_input_refs', 'reason_refs', 'statement', 'interpretation_limit']},
}
