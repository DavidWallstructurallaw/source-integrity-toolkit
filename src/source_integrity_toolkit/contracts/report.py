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
