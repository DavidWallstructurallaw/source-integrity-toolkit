# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: REPORT_CONTRACT.

Closed declarations transcribed from adopted lineage sections 2-9. Type labels
are inert descriptors for later project-owned validation, never executable
mapping expressions. Numeric conversion, field checks and acceptance are not
implemented here. Each row is (shape, source section, (name, type, required)).
Union '|null' preserves null separately from absent optional fields. '+'/'*'
mark nonempty/arbitrary arrays; '&' records snapshot-local distinct-ID arrays.
These are private implementation declarations, not a second public schema.
"""
from types import MappingProxyType

SCAFFOLD_VERSION = "0.1.0.dev0"
BUNDLE_VERSION = "sit-bundle/0.1"
REPORT_VERSION = "sit-report/0.1"
VOCABULARIES = MappingProxyType({
    'record_kind': ('claim', 'artifact', 'actor', 'evidence_item', 'origin_event', 'model', 'evaluation', 'correction_channel', 'correction_event', 'pipeline_record', 'anomaly', 'unresolved_reference'),
    'predicate': ('supports', 'contradicts', 'describes', 'qualifies', 'contextualizes', 'corroborates', 'cites', 'derived_from', 'copies', 'syndicated_from', 'summarizes', 'translates', 'quotes', 'originates_from', 'depends_on', 'generated_by', 'published_by', 'model_derived_from', 'trained_on', 'owned_by', 'retrieved_from', 'propagates_to', 'supersedes', 'same_identity_as'),
    'assessment_kind': ('origin_boundary', 'independence', 'coverage', 'classification', 'verification', 'externality', 'authority', 'capacity', 'conflict'),
    'dimension': ('acquisition', 'analytical_method', 'model_ancestry', 'evaluation_rubric', 'organizational_control'),
    'time_state': ('known', 'unknown', 'withheld', 'not_applicable'),
    'precision': ('date', 'instant'),
    'basis_kind': ('declaration', 'documented_record', 'upstream_inference', 'protected_attestation', 'unspecified'),
    'gap_reason': ('not_recorded', 'not_examined', 'withheld', 'unavailable', 'identity_ambiguous', 'outside_snapshot', 'not_applicable', 'other'),
    'reference_kind': ('supplied_excerpt', 'record_pointer', 'local_locator', 'external_locator', 'protected_attestation'),
    'availability': ('supplied', 'locator_only', 'withheld', 'unavailable'),
    'artifact_kind': ('document', 'dataset', 'answer', 'reference_answer', 'rubric', 'benchmark', 'judgment', 'observation_record', 'execution_result', 'other', 'unknown'),
    'actor_kind': ('human', 'organization', 'software_agent', 'unknown'),
    'identity_disclosure': ('named', 'pseudonymous', 'protected', 'unknown'),
    'epistemic_type': ('measurement', 'testimony', 'documentary_statement', 'estimate', 'formal_derivation', 'execution_result', 'analytical_inference', 'evaluative_judgment', 'allegation', 'fictional_example', 'unclassified'),
    'origin_event_kind': ('observation', 'data_collection', 'testimony', 'documentary_issuance', 'analysis', 'formal_check', 'execution', 'other', 'unknown'),
    'evaluation_kind': ('judgment', 'formal_check', 'execution', 'empirical_review', 'human_review', 'identity_process_review', 'other', 'unknown'),
    'role': ('candidate', 'generator', 'judge', 'executor', 'human_reviewer', 'reference_answer', 'rubric', 'validation_environment', 'method_input'),
    'action': ('review', 'amend', 'annotate', 'retract', 'rerun', 'rollback', 'replace_evaluator', 'restrict_scope', 'withdraw', 'metadata_correction', 'other'),
    'correction_event_kind': ('submission', 'handling', 'change'),
    'submission_kind': ('objection', 'proposed_correction', 'appeal'),
    'outcome': ('acknowledged', 'under_review', 'accepted', 'rejected', 'withdrawn', 'failed', 'unknown'),
    'stage': ('admission', 'preservation', 'selection', 'influence'),
    'pipeline_state': ('occurred', 'did_not_occur', 'unknown'),
    'linkage_kind': ('use_record', 'comparison_record', 'experimental_attribution', 'declaration', 'unspecified'),
    'classification_state': ('unclassified', 'caller_classified'),
    'assertion_kind': ('relation', 'assessment'),
    'lifecycle_state': ('active', 'withdrawn', 'superseded'),
    'polarity': ('affirmed', 'denied'),
    'identity_level': ('artifact_version', 'actor', 'origin_event', 'model_version'),
    'boundary_role': ('documented_origin', 'declared_origin', 'reference_baseline', 'scope_cut', 'unresolved'),
    'comparison_form': ('pairwise', 'setwise'),
    'independence_conclusion': ('independent_process', 'shared_dependency', 'partial_overlap', 'unknown', 'not_assessed', 'not_applicable'),
    'coverage_kind': ('upstream_history', 'citation_list', 'identity', 'model_history', 'correction_routes', 'pipeline_universe', 'other'),
    'coverage_state': ('complete_for_scope', 'partial', 'not_examined'),
    'axis': ('sil_data_role', 'hdl_structure_role', 'sil_governance_layer'),
    'sil_data_role': ('surface_linguistic', 'world_model', 'judgment'),
    'hdl_structure_role': ('surface_linguistic_structure', 'world_structure', 'judgment_structure'),
    'sil_governance_layer': ('open_web', 'verified', 'contested', 'judgment'),
    'verification_scope': ('identity', 'process', 'byte_integrity', 'other'),
    'reported_outcome': ('verified', 'not_verified', 'inconclusive', 'revoked', 'unknown'),
    'externality_conclusion': ('external', 'internal', 'mixed', 'unknown'),
    'grant_state': ('granted', 'denied', 'expired', 'unknown'),
    'conflict_kind': ('affirmation_denial', 'incompatible_origin', 'incompatible_independence', 'identity_dispute', 'scope_dispute', 'other'),
    'resolution_state': ('unresolved', 'externally_resolved'),
    'resolved_kind': ('claim', 'artifact', 'actor', 'evidence_item', 'origin_event', 'model', 'evaluation', 'correction_channel', 'correction_event', 'pipeline_record', 'anomaly'),
    'endpoint_gap_reason': ('not_recorded', 'not_examined', 'withheld', 'unavailable', 'identity_ambiguous', 'outside_snapshot', 'other'),
})
SHAPES = (
    ('Bundle', '2', (('contract_version', '=sit-bundle/0.1', True), ('bundle_id', 'id', True), ('snapshot_id', 'id', True), ('recorded_at', '#TimeValue', True), ('predecessor', '#Predecessor|null', True), ('inquiries', '+#Inquiry', True), ('records', '*#Record', True), ('assertions', '*#Assertion', True), ('evidence_references', '*#EvidenceReference', True), ('extensions', 'extensions', False))),
    ('Predecessor', '2', (('bundle_id', 'id', True), ('snapshot_id', 'id', True))),
    ('TimeValue', '3.1', (('state', '@time_state', True), ('value', 'str|null', True), ('precision', '@precision|null', True), ('reason', 'str', False))),
    ('TimeWindow', '3.1', (('start', '#TimeValue', True), ('end', '#TimeValue', True), ('note', 'str', False))),
    ('Provenance', '3.2', (('attributed_to_ref', 'id|null', True), ('basis_kind', '@basis_kind', True), ('evidence_ref_ids', '*&id', True), ('method', 'str|null', True), ('qualifications', '*str', True))),
    ('Gap', '3.3', (('field', 'str', True), ('reason', '@gap_reason', True), ('detail', 'text', True))),
    ('EvidenceReference', '4.1', (('id', 'id', True), ('reference_kind', '@reference_kind', True), ('availability', '@availability', True), ('artifact_ref', 'id|null', True), ('record_ref', 'id|null', True), ('locator', 'str|null', True), ('excerpt', 'str|null', True), ('provided_by_ref', 'id|null', True), ('attestor_ref', 'id|null', True), ('scope_note', 'text', True), ('gaps', '*#Gap', False), ('extensions', 'extensions', False))),
    ('Inquiry', '5', (('id', 'id', True), ('label', 'str', False), ('target_claim_refs', '+&id', True), ('target_object_refs', '*&id', True), ('seed_artifact_refs', '*&id', True), ('seed_evidence_refs', '*&id', True), ('boundary', '#Boundary', True), ('time_window', '#TimeWindow', True), ('as_of', '#TimeValue', True), ('dependency_dimensions', '*@dimension', True), ('coverage_assertion_refs', '*&id', True), ('provenance', '#Provenance', True), ('gaps', '*#Gap', False), ('extensions', 'extensions', False))),
    ('Boundary', '5', (('description', 'text', True), ('criterion', 'text', True), ('system_refs', '*&id', True))),
    ('Record', '6', (('id', 'id', True), ('kind', '@record_kind', True), ('data', '#RecordData', True), ('provenance', '#Provenance', True), ('label', 'str', False), ('gaps', '*#Gap', False), ('extensions', 'extensions', False))),
    ('ClaimData', '6.1', (('claim_key', 'str', True), ('version_label', 'str|null', True), ('text', 'text|null', True), ('content_evidence_ref', 'id', False), ('context', 'str', True))),
    ('ArtifactData', '6.2', (('artifact_kind', '@artifact_kind', True), ('work_key', 'str|null', True), ('version_label', 'str|null', True), ('locators', '*str', True), ('published_at', '#TimeValue', True), ('retrieved_at', '#TimeValue', True), ('content_evidence_refs', '*&id', True), ('checksums', '*#Checksum', False))),
    ('Checksum', '6.2', (('algorithm', 'str', True), ('value', 'str', True), ('covered_material', 'str', True))),
    ('ActorData', '6.3', (('actor_kind', '@actor_kind', True), ('identity_disclosure', '@identity_disclosure', True), ('display_name', 'str|null', True), ('identity_key', 'str', False))),
    ('EvidenceItemData', '6.4', (('claim_ref', 'id', True), ('artifact_ref', 'id', True), ('locator', 'str|null', True), ('epistemic_type', '@epistemic_type', True), ('description', 'text', True))),
    ('OriginEventData', '6.5', (('event_kind', '@origin_event_kind', True), ('event_key', 'str|null', True), ('performed_by_refs', '*&id', True), ('method_ref', 'id|null', True), ('occurred_at', '#TimeValue', True), ('description', 'text', True))),
    ('ModelData', '6.6', (('model_key', 'str', True), ('version_label', 'str|null', True), ('family_label', 'str|null', True), ('provider_ref', 'id|null', True))),
    ('EvaluationData', '6.7', (('evaluation_kind', '@evaluation_kind', True), ('target_refs', '+&id', True), ('role_bindings', '*#RoleBinding', True), ('result_refs', '*&id', True), ('occurred_at', '#TimeValue', True), ('review_contribution', 'str|null', True))),
    ('RoleBinding', '6.7', (('role', '@role', True), ('object_ref', 'id', True), ('evidence_ref_ids', '*&id', True), ('qualifications', '*str', True))),
    ('CorrectionChannelData', '6.8', (('owner_refs', '*&id', True), ('target_refs', '*&id', True), ('contact_locator', 'str|null', True), ('declared_action_types', '*@action', True), ('valid_window', '#TimeWindow', True))),
    ('CorrectionEventData', '6.9', (('event_kind', '@correction_event_kind', True), ('case_ref', 'id|null', True), ('channel_ref', 'id|null', True), ('target_refs', '+&id', True), ('occurred_at', '#TimeValue', True), ('details', '#CorrectionDetails', True))),
    ('SubmissionDetails', '6.9', (('submission_kind', '@submission_kind', True), ('summary', 'text', True))),
    ('HandlingDetails', '6.9', (('outcome', '@outcome', True), ('reason', 'str|null', True))),
    ('ChangeDetails', '6.9', (('action_type', '@action', True), ('before_ref', 'id', True), ('after_ref', 'id|null', True), ('after_absence_reason', 'str|null', True), ('linkage_description', 'text', True))),
    ('PipelineRecordData', '6.10', (('subject_ref', 'id', True), ('run_key', 'text', True), ('stage_key', 'text', True), ('stage', '@stage', True), ('state', '@pipeline_state', True), ('output_refs', '*&id', True), ('observed_at', '#TimeValue', True), ('linkage_kind', '@linkage_kind', True), ('detail', 'text', True))),
    ('AnomalyData', '6.11', (('inquiry_refs', '+&id', True), ('claim_ref', 'id|null', True), ('original_context', 'text|null', True), ('context_evidence_ref', 'id|null', True), ('classification_state', '@classification_state', True), ('caller_label', 'str|null', True), ('comparison_note', 'str|null', True))),
    ('UnresolvedReferenceData', '6.12', (('expected_kinds', '+@resolved_kind', True), ('reason', '@endpoint_gap_reason', True), ('description', 'text', True), ('external_locator', 'str', False), ('protected_key', 'str', False))),
    ('Assertion', '7', (('id', 'id', True), ('assertion_kind', '@assertion_kind', True), ('scope', '#Scope', True), ('provenance', '#Provenance', True), ('asserted_at', '#TimeValue', True), ('lifecycle_state', '@lifecycle_state', True), ('lifecycle_basis_ref_ids', '*&id', True), ('data', '#AssertionData', True), ('gaps', '*#Gap', False), ('extensions', 'extensions', False))),
    ('Scope', '7', (('inquiry_refs', '+&id', True), ('claim_refs', '*&id', True), ('effective_window', '#TimeWindow', True))),
    ('RelationData', '8.1', (('predicate', '@predicate', True), ('from_ref', 'id', True), ('to_ref', 'id', True), ('polarity', '@polarity', True), ('dimension', '@dimension|null', True), ('details', '#RelationDetails', True))),
    ('StanceDetails', '8.3', (('note', 'str', False),)),
    ('CitationDetails', '8.3', (('citation_locator', 'str', False), ('note', 'str', False))),
    ('TransformationDetails', '8.3', (('transformer_ref', 'id', False), ('method_ref', 'id', False), ('occurred_at', '#TimeValue', False), ('portion_note', 'str', False))),
    ('OriginDetails', '8.3', (('dependency_note', 'str', False), ('portion_note', 'str', False))),
    ('AgentDetails', '8.3', (('role_note', 'str', False), ('valid_window', '#TimeWindow', False))),
    ('ModelDetails', '8.3', (('stage_note', 'str', False), ('subset_descriptor', 'str', False), ('occurred_at', '#TimeValue', False))),
    ('RetrievalDetails', '8.3', (('retrieval_time', '#TimeValue', False), ('portion_note', 'str', False))),
    ('RouteDetails', '8.3', (('action_type', '@action', True), ('valid_window', '#TimeWindow', True), ('route_note', 'str', False))),
    ('SupersessionDetails', '8.3', (('reason', 'str', True), ('effective_at', '#TimeValue', False))),
    ('IdentityDetails', '8.3', (('identity_level', '@identity_level', True), ('identity_note', 'str', False))),
    ('AssessmentData', '9', (('assessment_kind', '@assessment_kind', True), ('subject_refs', '*&id', True), ('details', '#AssessmentDetails', True))),
    ('OriginBoundaryDetails', '9.1', (('dimension', '@dimension', True), ('boundary_role', '@boundary_role', True), ('coverage_ref', 'id|null', True), ('termination_reason', 'text', True))),
    ('IndependenceDetails', '9.2', (('comparison_form', '@comparison_form', True), ('dimension', '@dimension', True), ('conclusion', '@independence_conclusion', True), ('examined_dependency_refs', '*&id', True), ('unexamined_dimensions', '*@dimension', True), ('coverage_ref', 'id|null', True), ('scope_note', 'text', True))),
    ('CoverageDetails', '9.3', (('coverage_kind', '@coverage_kind', True), ('state', '@coverage_state', True), ('relation_types', '*@predicate', True), ('dimensions', '*@dimension', True), ('member_refs', '*&id', True), ('omitted_refs', '*&id', True), ('universe_enumerated', 'bool', True), ('scope_note', 'text', True))),
    ('ClassificationDetails', '9.4', (('axis', '@axis', True), ('labels', '+str', True), ('verification_assessment_refs', '*&id', True), ('scope_note', 'str', True))),
    ('VerificationDetails', '9.5', (('verification_scope', '@verification_scope', True), ('evaluation_ref', 'id|null', True), ('reported_outcome', '@reported_outcome', True), ('valid_window', '#TimeWindow', True), ('scope_note', 'str', True))),
    ('ExternalityDetails', '9.6', (('boundary_inquiry_ref', 'id', True), ('conclusion', '@externality_conclusion', True), ('grounding_basis', 'text|null', True), ('relevant_time', '#TimeValue', True))),
    ('AuthorityDetails', '9.7', (('target_refs', '*&id', True), ('action_types', '*@action', True), ('valid_window', '#TimeWindow', True), ('authorized_by_ref', 'id', True), ('grant_state', '@grant_state', True), ('authority_basis', 'text|null', True), ('coverage_ref', 'id|null', True))),
    ('CapacityDetails', '9.8', (('reported_capacity', 'str|null', True), ('unit', 'str|null', True), ('horizon', '#TimeWindow', True), ('reported_load', 'str|null', True), ('scope_note', 'str', True))),
    ('ConflictDetails', '9.9', (('conflict_kind', '@conflict_kind', True), ('resolution_state', '@resolution_state', True), ('resolution_evaluation_ref', 'id|null', True), ('scope_note', 'str', True))),
)
RECORD_SHAPES = MappingProxyType({'claim': 'ClaimData', 'artifact': 'ArtifactData', 'actor': 'ActorData', 'evidence_item': 'EvidenceItemData', 'origin_event': 'OriginEventData', 'model': 'ModelData', 'evaluation': 'EvaluationData', 'correction_channel': 'CorrectionChannelData', 'correction_event': 'CorrectionEventData', 'pipeline_record': 'PipelineRecordData', 'anomaly': 'AnomalyData', 'unresolved_reference': 'UnresolvedReferenceData'})
RELATION_SHAPES = MappingProxyType({'supports': 'StanceDetails', 'contradicts': 'StanceDetails', 'describes': 'StanceDetails', 'qualifies': 'StanceDetails', 'contextualizes': 'StanceDetails', 'corroborates': 'StanceDetails', 'cites': 'CitationDetails', 'derived_from': 'TransformationDetails', 'copies': 'TransformationDetails', 'syndicated_from': 'TransformationDetails', 'summarizes': 'TransformationDetails', 'translates': 'TransformationDetails', 'quotes': 'TransformationDetails', 'originates_from': 'OriginDetails', 'depends_on': 'OriginDetails', 'generated_by': 'AgentDetails', 'published_by': 'AgentDetails', 'owned_by': 'AgentDetails', 'model_derived_from': 'ModelDetails', 'trained_on': 'ModelDetails', 'retrieved_from': 'RetrievalDetails', 'propagates_to': 'RouteDetails', 'supersedes': 'SupersessionDetails', 'same_identity_as': 'IdentityDetails'})
ASSESSMENT_SHAPES = MappingProxyType({'origin_boundary': 'OriginBoundaryDetails', 'independence': 'IndependenceDetails', 'coverage': 'CoverageDetails', 'classification': 'ClassificationDetails', 'verification': 'VerificationDetails', 'externality': 'ExternalityDetails', 'authority': 'AuthorityDetails', 'capacity': 'CapacityDetails', 'conflict': 'ConflictDetails'})
CORE_KIND_COUNT = 12
RELATION_COUNT = 24
ASSESSMENT_COUNT = 9
