# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Bounded explicit report disclosure selection over accepted private owners.

Owner: RUNTIME_BOUNDARY. The literal named-field selections below implement
PRIVACY_AND_DATA_HANDLING section 4 and the approved SelectedNative fragments.
Unlisted source values are never recursively copied or inspected for content.
This module does not anonymize inputs, qualify premises, or activate public APIs.
"""
from ..contracts import report as _c
from ..contracts import results as _r
from ..contracts.bundle import _Object, _Array, _Number
from ..contracts.evidence import _PreparedBundle
from ..contracts.execution import _byte_work
from ..reporting import assemble as _a

# Explicit source-field allowlists, transcribed from the frozen Selected* and
# TimeValue/TimeWindow definitions. Only these named fields are read into output;
# optional fields retain actual absence. This is not a source-record serializer.
_SHAPES = {'TimeValue': (('state', 'scalar', True),
               ('value', ('nullable', 'scalar'), True),
               ('precision', ('nullable', 'scalar'), True),
               ('reason', 'scalar', False)),
 'TimeWindow': (('start', 'TimeValue', True), ('end', 'TimeValue', True), ('note', 'scalar', False)),
 'SelectedProvenance': (('attributed_to_ref', ('nullable', 'scalar'), True),
                        ('basis_kind', 'scalar', True),
                        ('evidence_ref_ids', ('array', 'scalar'), True),
                        ('method', ('nullable', 'scalar'), True),
                        ('qualifications', ('array', 'scalar'), True)),
 'SelectedGap': (('field', 'scalar', True), ('reason', 'scalar', True), ('detail', 'scalar', True)),
 'SelectedEvidenceReference': (('id', 'scalar', True),
                               ('reference_kind', 'scalar', True),
                               ('availability', 'scalar', True),
                               ('artifact_ref', ('nullable', 'scalar'), True),
                               ('record_ref', ('nullable', 'scalar'), True),
                               ('provided_by_ref', ('nullable', 'scalar'), True),
                               ('attestor_ref', ('nullable', 'scalar'), True),
                               ('scope_note', 'scalar', True),
                               ('gaps', ('array', 'SelectedGap'), False)),
 'SelectedInquiry': (('id', 'scalar', True),
                     ('target_claim_refs', ('array', 'scalar'), True),
                     ('target_object_refs', ('array', 'scalar'), True),
                     ('seed_artifact_refs', ('array', 'scalar'), True),
                     ('seed_evidence_refs', ('array', 'scalar'), True),
                     ('boundary', 'SelectedBoundary', True),
                     ('time_window', 'TimeWindow', True),
                     ('as_of', 'TimeValue', True),
                     ('dependency_dimensions', ('array', 'scalar'), True),
                     ('coverage_assertion_refs', ('array', 'scalar'), True),
                     ('provenance', 'SelectedProvenance', True),
                     ('gaps', ('array', 'SelectedGap'), False)),
 'SelectedBoundary': (('description', 'scalar', True),
                      ('criterion', 'scalar', True),
                      ('system_refs', ('array', 'scalar'), True)),
 'SelectedRecord': (('id', 'scalar', True),
                    ('kind', 'scalar', True),
                    ('data', 'SelectedRecordData', True),
                    ('provenance', 'SelectedProvenance', True),
                    ('gaps', ('array', 'SelectedGap'), False)),
 'SelectedClaimData': (('claim_key', 'scalar', True),
                       ('version_label', ('nullable', 'scalar'), True),
                       ('content_evidence_ref', 'scalar', False),
                       ('context', 'scalar', True)),
 'SelectedArtifactData': (('artifact_kind', 'scalar', True),
                          ('version_label', ('nullable', 'scalar'), True),
                          ('published_at', 'TimeValue', True),
                          ('retrieved_at', 'TimeValue', True),
                          ('content_evidence_refs', ('array', 'scalar'), True)),
 'SelectedActorData': (('actor_kind', 'scalar', True), ('identity_disclosure', 'scalar', True)),
 'SelectedEvidenceItemData': (('claim_ref', 'scalar', True),
                              ('artifact_ref', 'scalar', True),
                              ('epistemic_type', 'scalar', True),
                              ('description', 'scalar', True)),
 'SelectedOriginEventData': (('event_kind', 'scalar', True),
                             ('event_key', ('nullable', 'scalar'), True),
                             ('performed_by_refs', ('array', 'scalar'), True),
                             ('method_ref', ('nullable', 'scalar'), True),
                             ('occurred_at', 'TimeValue', True),
                             ('description', 'scalar', True)),
 'SelectedModelData': (('model_key', 'scalar', True),
                       ('version_label', ('nullable', 'scalar'), True),
                       ('family_label', ('nullable', 'scalar'), True),
                       ('provider_ref', ('nullable', 'scalar'), True)),
 'SelectedEvaluationData': (('evaluation_kind', 'scalar', True),
                            ('target_refs', ('array', 'scalar'), True),
                            ('role_bindings', ('array', 'SelectedRoleBinding'), True),
                            ('result_refs', ('array', 'scalar'), True),
                            ('occurred_at', 'TimeValue', True),
                            ('review_contribution', ('nullable', 'scalar'), True)),
 'SelectedRoleBinding': (('role', 'scalar', True),
                         ('object_ref', 'scalar', True),
                         ('evidence_ref_ids', ('array', 'scalar'), True),
                         ('qualifications', ('array', 'scalar'), True)),
 'SelectedCorrectionChannelData': (('owner_refs', ('array', 'scalar'), True),
                                   ('target_refs', ('array', 'scalar'), True),
                                   ('declared_action_types', ('array', 'scalar'), True),
                                   ('valid_window', 'TimeWindow', True)),
 'SelectedCorrectionEventData': (('event_kind', 'scalar', True),
                                 ('case_ref', ('nullable', 'scalar'), True),
                                 ('channel_ref', ('nullable', 'scalar'), True),
                                 ('target_refs', ('array', 'scalar'), True),
                                 ('occurred_at', 'TimeValue', True),
                                 ('details', 'SelectedCorrectionDetails', True)),
 'SelectedSubmissionDetails': (('submission_kind', 'scalar', True), ('summary', 'scalar', True)),
 'SelectedHandlingDetails': (('outcome', 'scalar', True), ('reason', ('nullable', 'scalar'), True)),
 'SelectedChangeDetails': (('action_type', 'scalar', True),
                           ('before_ref', 'scalar', True),
                           ('after_ref', ('nullable', 'scalar'), True),
                           ('after_absence_reason', ('nullable', 'scalar'), True),
                           ('linkage_description', 'scalar', True)),
 'SelectedPipelineRecordData': (('subject_ref', 'scalar', True),
                                ('run_key', 'scalar', True),
                                ('stage_key', 'scalar', True),
                                ('stage', 'scalar', True),
                                ('state', 'scalar', True),
                                ('output_refs', ('array', 'scalar'), True),
                                ('observed_at', 'TimeValue', True),
                                ('linkage_kind', 'scalar', True),
                                ('detail', 'scalar', True)),
 'SelectedAnomalyData': (('inquiry_refs', ('array', 'scalar'), True),
                         ('claim_ref', ('nullable', 'scalar'), True),
                         ('original_context', ('nullable', 'scalar'), True),
                         ('context_evidence_ref', ('nullable', 'scalar'), True),
                         ('classification_state', 'scalar', True),
                         ('caller_label', ('nullable', 'scalar'), True),
                         ('comparison_note', ('nullable', 'scalar'), True)),
 'SelectedUnresolvedReferenceData': (('expected_kinds', ('array', 'scalar'), True),
                                     ('reason', 'scalar', True),
                                     ('description', 'scalar', True)),
 'SelectedAssertion': (('id', 'scalar', True),
                       ('assertion_kind', 'scalar', True),
                       ('scope', 'SelectedAssertionScope', True),
                       ('provenance', 'SelectedProvenance', True),
                       ('asserted_at', 'TimeValue', True),
                       ('lifecycle_state', 'scalar', True),
                       ('lifecycle_basis_ref_ids', ('array', 'scalar'), True),
                       ('data', 'SelectedAssertionData', True),
                       ('gaps', ('array', 'SelectedGap'), False)),
 'SelectedAssertionScope': (('inquiry_refs', ('array', 'scalar'), True),
                            ('claim_refs', ('array', 'scalar'), True),
                            ('effective_window', 'TimeWindow', True)),
 'SelectedRelationData': (('predicate', 'scalar', True),
                          ('from_ref', 'scalar', True),
                          ('to_ref', 'scalar', True),
                          ('polarity', 'scalar', True),
                          ('dimension', ('nullable', 'scalar'), True),
                          ('details', 'SelectedRelationDetails', True)),
 'SelectedStanceDetails': (('note', 'scalar', False),),
 'SelectedCitationDetails': (('note', 'scalar', False),),
 'SelectedTransformationDetails': (('transformer_ref', 'scalar', False),
                                   ('method_ref', 'scalar', False),
                                   ('occurred_at', 'TimeValue', False),
                                   ('portion_note', 'scalar', False)),
 'SelectedOriginDetails': (('dependency_note', 'scalar', False), ('portion_note', 'scalar', False)),
 'SelectedAgentDetails': (('role_note', 'scalar', False), ('valid_window', 'TimeWindow', False)),
 'SelectedModelDetails': (('stage_note', 'scalar', False),
                          ('subset_descriptor', 'scalar', False),
                          ('occurred_at', 'TimeValue', False)),
 'SelectedRetrievalDetails': (('retrieval_time', 'TimeValue', False), ('portion_note', 'scalar', False)),
 'SelectedRouteDetails': (('action_type', 'scalar', True),
                          ('valid_window', 'TimeWindow', True),
                          ('route_note', 'scalar', False)),
 'SelectedSupersessionDetails': (('reason', 'scalar', True), ('effective_at', 'TimeValue', False)),
 'SelectedIdentityDetails': (('identity_level', 'scalar', True), ('identity_note', 'scalar', False)),
 'SelectedAssessmentData': (('assessment_kind', 'scalar', True),
                            ('subject_refs', ('array', 'scalar'), True),
                            ('details', 'SelectedAssessmentDetails', True)),
 'SelectedOriginBoundaryDetails': (('dimension', 'scalar', True),
                                   ('boundary_role', 'scalar', True),
                                   ('coverage_ref', ('nullable', 'scalar'), True),
                                   ('termination_reason', 'scalar', True)),
 'SelectedIndependenceDetails': (('comparison_form', 'scalar', True),
                                 ('dimension', 'scalar', True),
                                 ('conclusion', 'scalar', True),
                                 ('examined_dependency_refs', ('array', 'scalar'), True),
                                 ('unexamined_dimensions', ('array', 'scalar'), True),
                                 ('coverage_ref', ('nullable', 'scalar'), True),
                                 ('scope_note', 'scalar', True)),
 'SelectedCoverageDetails': (('coverage_kind', 'scalar', True),
                             ('state', 'scalar', True),
                             ('relation_types', ('array', 'scalar'), True),
                             ('dimensions', ('array', 'scalar'), True),
                             ('member_refs', ('array', 'scalar'), True),
                             ('omitted_refs', ('array', 'scalar'), True),
                             ('universe_enumerated', 'scalar', True),
                             ('scope_note', 'scalar', True)),
 'SelectedClassificationDetails': (('axis', 'scalar', True),
                                   ('labels', ('array', 'scalar'), True),
                                   ('verification_assessment_refs', ('array', 'scalar'), True),
                                   ('scope_note', 'scalar', True)),
 'SelectedVerificationDetails': (('verification_scope', 'scalar', True),
                                 ('evaluation_ref', ('nullable', 'scalar'), True),
                                 ('reported_outcome', 'scalar', True),
                                 ('valid_window', 'TimeWindow', True),
                                 ('scope_note', 'scalar', True)),
 'SelectedExternalityDetails': (('boundary_inquiry_ref', 'scalar', True),
                                ('conclusion', 'scalar', True),
                                ('grounding_basis', ('nullable', 'scalar'), True),
                                ('relevant_time', 'TimeValue', True)),
 'SelectedAuthorityDetails': (('target_refs', ('array', 'scalar'), True),
                              ('action_types', ('array', 'scalar'), True),
                              ('valid_window', 'TimeWindow', True),
                              ('authorized_by_ref', 'scalar', True),
                              ('grant_state', 'scalar', True),
                              ('authority_basis', ('nullable', 'scalar'), True),
                              ('coverage_ref', ('nullable', 'scalar'), True)),
 'SelectedCapacityDetails': (('reported_capacity', ('nullable', 'scalar'), True),
                             ('unit', ('nullable', 'scalar'), True),
                             ('horizon', 'TimeWindow', True),
                             ('reported_load', ('nullable', 'scalar'), True),
                             ('scope_note', 'scalar', True)),
 'SelectedConflictDetails': (('conflict_kind', 'scalar', True),
                             ('resolution_state', 'scalar', True),
                             ('resolution_evaluation_ref', ('nullable', 'scalar'), True),
                             ('scope_note', 'scalar', True))}

_DISCRIMINATORS = {
    'SelectedRecord': ('kind', 'data', {
        'claim': 'SelectedClaimData', 'artifact': 'SelectedArtifactData',
        'actor': 'SelectedActorData', 'evidence_item': 'SelectedEvidenceItemData',
        'origin_event': 'SelectedOriginEventData', 'model': 'SelectedModelData',
        'evaluation': 'SelectedEvaluationData', 'correction_channel': 'SelectedCorrectionChannelData',
        'correction_event': 'SelectedCorrectionEventData', 'pipeline_record': 'SelectedPipelineRecordData',
        'anomaly': 'SelectedAnomalyData', 'unresolved_reference': 'SelectedUnresolvedReferenceData'}),
    'SelectedAssertion': ('assertion_kind', 'data', {
        'relation': 'SelectedRelationData', 'assessment': 'SelectedAssessmentData'}),
    'SelectedCorrectionEventData': ('event_kind', 'details', {
        'submission': 'SelectedSubmissionDetails', 'handling': 'SelectedHandlingDetails',
        'change': 'SelectedChangeDetails'}),
    'SelectedRelationData': ('predicate', 'details', {
        'supports': 'SelectedStanceDetails', 'contradicts': 'SelectedStanceDetails',
        'describes': 'SelectedStanceDetails', 'qualifies': 'SelectedStanceDetails',
        'contextualizes': 'SelectedStanceDetails', 'corroborates': 'SelectedStanceDetails',
        'cites': 'SelectedCitationDetails', 'derived_from': 'SelectedTransformationDetails',
        'copies': 'SelectedTransformationDetails', 'syndicated_from': 'SelectedTransformationDetails',
        'summarizes': 'SelectedTransformationDetails', 'translates': 'SelectedTransformationDetails',
        'quotes': 'SelectedTransformationDetails', 'originates_from': 'SelectedOriginDetails',
        'depends_on': 'SelectedOriginDetails', 'generated_by': 'SelectedAgentDetails',
        'published_by': 'SelectedAgentDetails', 'owned_by': 'SelectedAgentDetails',
        'model_derived_from': 'SelectedModelDetails', 'trained_on': 'SelectedModelDetails',
        'retrieved_from': 'SelectedRetrievalDetails', 'propagates_to': 'SelectedRouteDetails',
        'supersedes': 'SelectedSupersessionDetails', 'same_identity_as': 'SelectedIdentityDetails'}),
    'SelectedAssessmentData': ('assessment_kind', 'details', {
        'origin_boundary': 'SelectedOriginBoundaryDetails', 'independence': 'SelectedIndependenceDetails',
        'coverage': 'SelectedCoverageDetails', 'classification': 'SelectedClassificationDetails',
        'verification': 'SelectedVerificationDetails', 'externality': 'SelectedExternalityDetails',
        'authority': 'SelectedAuthorityDetails', 'capacity': 'SelectedCapacityDetails',
        'conflict': 'SelectedConflictDetails'}),
}
_DISCLOSURE_FIELDS = (
    'origin_boundary_disclosures', 'ancestry_gap_disclosures', 'independence_assessment_disclosures',
    'evaluator_overlap_disclosures', 'externality_assessment_disclosures', 'externality_stage_links',
    'pipeline_stage_disclosures', 'cohort_transition_disclosures', 'correction_route_disclosures',
    'correction_case_disclosures', 'correction_target_change_disclosures', 'reported_capacity_disclosures',
    'corrective_independence_disclosures', 'human_contribution_disclosures', 'anomaly_context_disclosures',
    'contestation_disclosures', 'tail_stage_result_links', 'coverage_disclosures',
    'documentary_basis_gap_disclosures')
_SCAN_QUALIFICATION = ('Examined assessment only; this scan does not establish applicability '
    'or qualification for the selected review scope.')
_SOURCE_QUALIFICATION = ('Actual owner selection/source reference slot; this record does not '
    'establish an applicable review or independent process.')


def _require(ok):
    _c._report_require(ok)


def _fields(value, port):
    """Index one trusted field bag without traversing unselected child values."""
    _require(type(value) is _Object)
    port.charge(2 * len(value.items) + 2)
    result = {}
    for name, child in value.items:
        _require(type(name) is str)
        _byte_work(port, 4 * len(name), 2)
        _require(name not in result)
        result[name] = child
    return result


def _scalar(value, port):
    port.charge(2)
    if type(value) is str:
        _byte_work(port, 4 * len(value), 1)
        return value
    if value is None or type(value) is bool:
        return value
    if type(value) is _Number:
        _require(value.exponent >= 0 and len(value.coefficient) + value.exponent <= 16)
        _byte_work(port, 17, 5)
        value = value.sign * int(value.coefficient) * 10 ** value.exponent
    _require(type(value) is int and -9007199254740991 <= value <= 9007199254740991)
    port.charge(2)
    return value


def _array(value, port):
    _require(type(value) in (_Array, tuple))
    values = value.items if type(value) is _Array else value
    port.charge(len(values) + 1)
    return values


def _shape(value, shape, port):
    """Follow only a named closed field rule; source keys never select output."""
    port.charge(3)
    if type(shape) is tuple:
        kind, child = shape
        if kind == 'nullable':
            return None if value is None else _shape(value, child, port)
        _require(kind == 'array')
        return tuple(_shape(item, child, port) for item in _array(value, port))
    if shape == 'scalar':
        return _scalar(value, port)
    _require(shape in _SHAPES)
    fields, selected = _fields(value, port), {}
    dispatch = _DISCRIMINATORS.get(shape)
    child_field = child_shape = None
    if dispatch is not None:
        discriminator, child_field, choices = dispatch
        tag = _scalar(fields[discriminator], port)
        _require(type(tag) is str and tag in choices)
        child_shape = choices[tag]
    for name, child, required in _SHAPES[shape]:
        _byte_work(port, 4 * len(name), 3)
        if name not in fields:
            _require(not required)
            continue
        selected[name] = _shape(fields[name], child_shape if name == child_field else child, port)
    return selected


def _native(value, port):
    fields = _fields(value, port)
    if 'kind' in fields:
        shape = 'SelectedRecord'
    elif 'assertion_kind' in fields:
        shape = 'SelectedAssertion'
    elif 'reference_kind' in fields:
        shape = 'SelectedEvidenceReference'
    else:
        _require('target_claim_refs' in fields and 'boundary' in fields)
        shape = 'SelectedInquiry'
    return _shape(value, shape, port)


def _key(ref, port):
    _require(type(ref) is _r._InputRef)
    _c._charge_input_ref(ref, port)
    port.charge(3)
    return ref.collection, ref.identifier, ref.selector


def _ref(value, collection, port):
    if type(value) is _r._InputRef:
        _require(value.collection == collection)
        _c._charge_input_ref(value, port)
        return value
    _require(type(value) is str)
    _byte_work(port, 4 * len(value), 5)
    return _r._InputRef(collection, value)


def _refs(value, collection, port):
    return tuple(_ref(item, collection, port) for item in _array(value, port))


def _input_fields(value, port):
    """The one explicit private InputRef-shaped field bag used by gap rows."""
    if type(value) is _r._InputRef:
        _c._charge_input_ref(value, port)
        return value
    fields = _fields(value, port)
    _require(set(fields) == {'collection', 'identifier', 'selector'})
    port.charge(7)
    collection, identifier, selector = (
        _scalar(fields[name], port) for name in ('collection', 'identifier', 'selector'))
    # Private SourceAddress spells the whole-entity selector as an empty
    # string. Public InputRef has one representation for that same slot.
    return _r._InputRef(collection, identifier, None if selector == '' else selector)


def _source(ref, index, port):
    _c._resolve_input(ref, index, port)
    port.charge(2)
    return index[(ref.collection, ref.identifier)].node.fields


def _unique_refs(refs, port):
    found = {}
    for ref in refs:
        key = _key(ref, port)
        port.charge(2)
        found.setdefault(key, ref)
    port.charge(4 * len(found) + 1)
    keys = _a._sort([(a, b, '' if c is None else c) for a, b, c in found], port)
    port.charge(len(keys) + 1)
    return tuple(found[(a, b, None if c == '' else c)] for a, b, c in keys)


def _basis(owner, index, checks, port):
    source = owner.source
    fields = _fields(_source(source, index, port), port)
    port.charge(14)
    body = {'basis_kind': None, 'asserter_ref': None, 'attestor_ref': None,
        'method': None, 'support_refs': (), 'availability': None, 'scope': None,
        'time': {}, 'lifecycle': None, 'qualifications': (), 'check_refs': checks}
    if source.collection == 'evidence_references':
        for name, source_name in (('asserter_ref', 'provided_by_ref'), ('attestor_ref', 'attestor_ref')):
            value = fields[source_name]
            body[name] = None if value is None else _ref(value, 'records', port)
        body['availability'] = _scalar(fields['availability'], port)
        body['qualifications'] = (_scalar(fields['scope_note'], port),)
        return body
    provenance = _fields(fields['provenance'], port)
    body['basis_kind'] = _scalar(provenance['basis_kind'], port)
    attributed = provenance['attributed_to_ref']
    body['asserter_ref'] = None if attributed is None else _ref(attributed, 'records', port)
    body['method'] = _scalar(provenance['method'], port)
    body['support_refs'] = _refs(provenance['evidence_ref_ids'], 'evidence_references', port)
    body['qualifications'] = _shape(provenance['qualifications'], ('array', 'scalar'), port)
    time_fields = fields
    if source.collection == 'assertions':
        scope = _fields(fields['scope'], port)
        body['scope'] = {'inquiry_refs': _refs(scope['inquiry_refs'], 'inquiries', port),
            'claim_refs': _refs(scope['claim_refs'], 'records', port),
            'effective_window': _shape(scope['effective_window'], 'TimeWindow', port)}
        body['lifecycle'] = {'state': _scalar(fields['lifecycle_state'], port),
            'basis_refs': _refs(fields['lifecycle_basis_ref_ids'], 'evidence_references', port)}
    elif source.collection == 'records':
        time_fields = _fields(fields['data'], port)
    for name in ('asserted_at', 'occurred_at', 'observed_at', 'published_at', 'retrieved_at',
                 'as_of', 'valid_window', 'time_window'):
        _byte_work(port, 4 * len(name), 2)
        if name in time_fields:
            body['time'][name] = _shape(time_fields[name],
                'TimeWindow' if name in ('valid_window', 'time_window') else 'TimeValue', port)
    return body


def _add_fields(target, fields, names, port):
    for name in names:
        _byte_work(port, 4 * len(name), 3)
        _require(name in fields)
        target[name] = _shape(fields[name], ('array', 'scalar') if name.endswith('reason_codes')
            or name in ('roles', 'matching_family_labels') else 'scalar', port)


def _ancestry(fields, port):
    port.charge(10)
    body = {'seed_ref': _ref(fields['seed_ref'], 'records', port),
        'dimension': _scalar(fields['dimension'], port), 'gaps': [], 'frontiers': [],
        'coverage': [], 'witness_paths': []}
    for value in _array(fields['gaps'], port):
        row = _fields(value, port)
        body['gaps'].append({'source': _input_fields(row['source'], port),
            'reason_codes': _shape(row['reason_codes'], ('array', 'scalar'), port)})
    for value in _array(fields['frontiers'], port):
        body['frontiers'].append(_native(value, port))
    for value in _array(fields['coverage'], port):
        row = _fields(value, port)
        selected = {'coverage_ref': _ref(row['coverage_ref'], 'assertions', port)}
        _add_fields(selected, row, ('qualification_state', 'reason_codes'), port)
        body['coverage'].append(selected)
    for value in _array(fields['witness_paths'], port):
        row = _fields(value, port)
        body['witness_paths'].append({'nodes': _refs(row['nodes'], 'records', port),
            'assertions': _refs(row['assertions'], 'assertions', port)})
    return body


def _disclosure_fields(field, row, index, port):
    fields = _fields(row.fields, port)
    if field == 'tail_stage_result_links':
        _require(type(row.source) is _r._ResultRef)
        selected = {}
        _add_fields(selected, fields, ('source_result_state', 'source_value_kind'), port)
        return selected
    _require(type(row.source) is _r._InputRef)
    if field == 'ancestry_gap_disclosures':
        return _ancestry(fields, port)
    selected = {'native_record': _native(_source(row.source, index, port), port)}
    if field in ('origin_boundary_disclosures', 'coverage_disclosures',
                 'documentary_basis_gap_disclosures', 'pipeline_stage_disclosures'):
        _add_fields(selected, fields, ('qualification_state', 'reason_codes'), port)
    elif field in ('independence_assessment_disclosures', 'corrective_independence_disclosures'):
        if 'process_qualification_state' in fields:
            _add_fields(selected, fields, ('process_qualification_state', 'origin_qualification_state',
                'reason_codes'), port)
        elif 'contribution_status' in fields:
            _require(field == 'corrective_independence_disclosures')
            _add_fields(selected, fields, ('contribution_status', 'documentary_state',
                'identity_state', 'reason_codes'), port)
    elif field == 'human_contribution_disclosures':
        if 'contribution_status' in fields:
            _add_fields(selected, fields, ('contribution_status', 'documentary_state',
                'identity_state', 'reason_codes'), port)
    elif field == 'externality_assessment_disclosures':
        if 'qualification_state' in fields:
            _add_fields(selected, fields, ('qualification_state', 'qualified_externality', 'reason_codes'), port)
    elif field == 'externality_stage_links':
        _add_fields(selected, fields, ('qualification_state', 'reason_codes'), port)
        selected['externality_subject_refs'] = _refs(fields['externality_subject_refs'], 'records', port)
        selected['mapping_assertion_refs'] = _refs(fields['mapping_assertion_refs'], 'assertions', port)
    elif field == 'cohort_transition_disclosures':
        anchor = _array(fields['stage_anchor'], port)
        _require(len(anchor) in (0, 3))
        selected['stage_anchor'] = None if not anchor else {
            name: _scalar(value, port) for name, value in zip(('run_key', 'stage_key', 'stage'), anchor)}
        _add_fields(selected, fields, ('cohort_qualification_state', 'transition_qualification_state',
            'reason_codes'), port)
    elif field == 'correction_route_disclosures':
        if 'target_ref' in fields:
            selected['target_ref'] = _ref(fields['target_ref'], 'records', port)
            _add_fields(selected, fields, ('action_type', 'declared_route_recorded',
                'authorized_route_recorded', 'authorized_route_state', 'absence_description'), port)
        elif 'grant_qualification_state' in fields:
            _add_fields(selected, fields, ('grant_qualification_state', 'grant_matches_tuple',
                'grant_reason_codes'), port)
    elif field in ('correction_case_disclosures', 'reported_capacity_disclosures'):
        if 'documentary_state' in fields:
            _add_fields(selected, fields, ('documentary_state', 'reason_codes'), port)
            if field == 'correction_case_disclosures':
                _add_fields(selected, fields, ('explicit_removal',), port)
    elif field == 'correction_target_change_disclosures':
        cases = []
        for value in _array(fields['case_rows'], port):
            item = _fields(value, port)
            case = {'case_ref': _ref(item['case_ref'], 'records', port)}
            for name in ('change_event_refs', 'qualified_change_event_refs'):
                case[name] = _refs(item[name], 'records', port)
            _add_fields(case, item, ('declared', 'selected', 'documentary_state',
                'requested_effect_state', 'reason_codes'), port)
            cases.append(case)
        selected['case_rows'] = cases
    elif field in ('anomaly_context_disclosures', 'contestation_disclosures'):
        selected['context_records'] = tuple(_native(value, port)
            for value in _array(fields['context_records'], port))
        _add_fields(selected, fields, ('reason_codes',), port)
    elif field == 'evaluator_overlap_disclosures':
        if 'roles' in fields:
            _add_fields(selected, fields, ('roles', 'matching_family_labels', 'roles_complete'), port)
            for name in ('left_object_refs', 'right_object_refs', 'shared_object_refs',
                         'common_ancestor_refs', 'missing_family_model_refs'):
                selected[name] = _refs(fields[name], 'records', port)
            pairs = []
            for value in _array(fields['one_sided_ancestry'], port):
                item = _fields(value, port)
                pairs.append({'from_ref': _ref(item['from_ref'], 'records', port),
                    'to_ref': _ref(item['to_ref'], 'records', port)})
            selected['one_sided_ancestry'] = pairs
    else:
        _require(False)
    return selected


def _disclosures(result, outcome, index, port):
    field = result.ref.field_key
    _require(field in _DISCLOSURE_FIELDS and type(result.value) is _r._RecordDisclosures)
    port.charge(4)
    selected = []
    for row in result.value.records:
        port.charge(5)
        selected.append({'source': row.source, 'fields': _disclosure_fields(field, row, index, port),
            'qualifications': _shape(row.qualifications, ('array', 'scalar'), port)})
    if field == 'corrective_independence_disclosures':
        wanted = _a._ref_keys(result.witness_refs, port)
        for record in outcome.witnesses:
            matches = False
            for ref in record.refs:
                key = _a._anchor(ref, port)
                _a._charge_key((key, wanted), port)
                if key in wanted:
                    matches = True
            if not matches:
                continue
            for payload in record.payload:
                port.charge(2)
                if payload[0] != 'human_review_witness':
                    continue
                _require(len(payload) == 5)
                for refs, qualification in ((payload[2], _SCAN_QUALIFICATION),
                                            (payload[3], _SOURCE_QUALIFICATION)):
                    for ref in refs:
                        port.charge(5)
                        selected.append({'source': ref,
                            'fields': {'native_record': _native(_source(ref, index, port), port)},
                            'qualifications': (qualification,)})
    return {'records': selected}


def _graph_inputs(record, components, index, port):
    """Select retained material and its explicit documentary reference IDs.

    This is field projection, not premise qualification or a new graph search.
    Native support remains attributable even when its availability is unknown.
    """
    port.charge(len(record.input_refs) + 1)
    refs = list(record.input_refs)
    for component in components:
        port.charge(12)
        for name in ('nodes', 'members', 'starts', 'examined_nodes', 'frontiers', 'terminals'):
            for node in component[name]:
                port.charge(2)
                refs.append(node['ref'])
        if component['target'] is not None:
            port.charge(2)
            refs.append(component['target']['ref'])
        for name in ('edges', 'internal_edges', 'exit_edges', 'examined_edges', 'observations'):
            for edge in component[name]:
                port.charge(10)
                refs.extend((edge['source']['ref'], edge['target']['ref'], edge['source_ref']))
    material = _unique_refs(refs, port)
    for ref in material:
        fields = _fields(_source(ref, index, port), port)
        if 'provenance' in fields:
            provenance = _fields(fields['provenance'], port)
            support = _refs(provenance['evidence_ref_ids'], 'evidence_references', port)
            port.charge(len(support) + 1)
            refs.extend(support)
    return _unique_refs(refs, port)


def _basis_links(outcome, port):
    port.charge(3)
    owners, checks = {}, {}
    for result in outcome.results:
        port.charge(2)
        relevant = {}
        for check in result.check_refs:
            port.charge(2)
            if check.check_id not in ('PC05', 'PC06', 'PC07', 'PC08', 'PC09', 'PC10'):
                continue
            seen = set()
            for ref in check.input_refs:
                key = _key(ref, port)[:2]
                port.charge(3)
                if key not in seen:
                    relevant.setdefault(key, []).append(check)
                    seen.add(key)
        for owner in result.basis_refs:
            key = _key(owner.source, port)
            port.charge(4)
            owners.setdefault(key, owner)
            group = relevant.get(key[:2], ())
            port.charge(len(group) + 1)
            checks.setdefault(key, []).extend(group)
        for population in result.population_refs:
            port.charge(1)
            for owner in population.basis_refs:
                key = _key(owner.source, port)
                port.charge(2)
                owners.setdefault(key, owner)
    for finding in outcome.findings:
        port.charge(2)
        groups = [finding.basis_refs]
        for population in finding.population_refs:
            port.charge(1)
            groups.append(population.basis_refs)
        for group in groups:
            for owner in group:
                key = _key(owner.source, port)
                port.charge(2)
                owners.setdefault(key, owner)
    return owners, checks


def _select_report_disclosure(outcome, port):
    """The product's explicit selected-field source for logical assembly."""
    port.check()
    _require(type(outcome) is _c._AnalyticalOutcome and type(outcome.prepared) is _PreparedBundle)
    index = _c._input_index(outcome.prepared, port)
    owners, checks = _basis_links(outcome, port)
    port.charge(8)
    basis, disclosures, findings, witnesses = [], [], [], []
    for key, owner in owners.items():
        port.charge(4)
        linked = _c._paid_tuple(checks.get(key, ()), port)
        basis.append((owner, _basis(owner, index, linked, port)))
    for result in outcome.results:
        port.charge(2)
        if type(result.value) is _r._RecordDisclosures:
            disclosures.append((result.ref, _disclosures(result, outcome, index, port)))
    for finding in outcome.findings:
        port.charge(len(finding.witness.owner_witnesses) + 5)
        components = tuple(_a._selected_component(payload, port)
            for payload in finding.witness.owner_witnesses)
        findings.append((finding, {'input_refs': _unique_refs(finding.witness.input_refs, port),
            'components': components}))
    for record in outcome.witnesses:
        port.charge(len(record.payload) + 2)
        if record.payload and all(payload[0] == 'graph_witness' for payload in record.payload):
            port.charge(len(record.payload) + 1)
            components = tuple(_a._selected_component(payload, port) for payload in record.payload)
            witnesses.append((record, {'input_refs': _graph_inputs(record, components, index, port),
                'components': components}))
    selection = _c._capture_report_disclosure(_c._paid_tuple(basis, port),
        _c._paid_tuple(disclosures, port), _c._paid_tuple(findings, port), port,
        owner_witnesses=_c._paid_tuple(witnesses, port))
    port.check()
    return selection


def _assemble_selected_report(outcome, port, *, tool_version='0.1.0.dev0', reserve_witnesses=False):
    """Select and assemble under the same caller-owned bounded internal port."""
    selected = _select_report_disclosure(outcome, port)
    return _a._assemble_report(outcome, selected, port, tool_version=tool_version,
        reserve_witnesses=reserve_witnesses)
