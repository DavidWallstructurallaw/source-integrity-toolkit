# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: REPORT_CONTRACT.

Private observability-preparation declarations only. No Result, audit envelope,
report identifiers, renderer or available_result_refs are constructed here.
Level labels are independent evidence domains, never a score or maximum level.
W06 adds private navigation over supplied fields. Only PC01 is completed after
full W05 admission. PC02-PC24 remain execution-pending; constituent observations
remain distinct from whole-check qualification.
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
