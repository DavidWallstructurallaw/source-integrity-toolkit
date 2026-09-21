# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: REPORT_CONTRACT.

Private immutable analytical representations, compiled from reporting sections
12-17, definitions sections 20-28 and architecture 18.1. No public report root,
identifier allocator, serializer or analysis entry point is supplied here.
Constructors check representation, never authenticate evidence or certify that
an operation ran. Only bounded project-owned immutable parts may enter them;
the constructing owner must prospectively charge every validation/allocation
pass through its existing job port. They do not capture arbitrary caller data.
"""
from dataclasses import dataclass
from .bundle import _require, _Object, _Array, _Number, _is_value
from .evidence import _Node

# Reporting 17: independent analytical bindings, not preparation navigation.
FIELD_BINDINGS = (
    ('SIT-M001', 'nominal_seed_artifact_record_count', 'count'),
    ('SIT-M001', 'unresolved_seed_artifact_reference_count', 'count'),
    ('SIT-M001', 'seed_evidence_item_count', 'count'),
    ('SIT-M001', 'claim_artifact_record_count', 'count'),
    ('SIT-M001', 'claim_unassigned_seed_artifact_record_count', 'count'),
    ('SIT-M002', 'reached_origin_record_count', 'count'),
    ('SIT-M002', 'documentary_origin_boundary_record_count', 'count'),
    ('SIT-M002', 'origin_boundary_disclosures', 'record_disclosures'),
    ('SIT-M003', 'submitted_comparison_member_count', 'count'),
    ('SIT-M003', 'qualified_process_set_member_count', 'count'),
    ('SIT-M003', 'qualified_origin_set_member_count', 'count'),
    ('SIT-M003', 'independence_assessment_disclosures', 'record_disclosures'),
    ('SIT-M004', 'per_seed_origin_memberships', 'incidence'),
    ('SIT-M004', 'origin_incidence_counts', 'incidence'),
    ('SIT-M004', 'seed_origin_dispositions', 'partition'),
    ('SIT-M004', 'documentary_origin_resolution_fraction', 'fraction'),
    ('SIT-M005', 'single_origin_contribution_hhi', 'fraction'),
    ('SIT-M006', 'immediate_evidence_layer_dispositions', 'partition'),
    ('SIT-M006', 'inherited_only_seed_fraction', 'fraction'),
    ('SIT-M006', 'inherited_only_completion_interval', 'completion_interval'),
    ('SIT-M007', 'unresolved_frontier_reference_count', 'count'),
    ('SIT-M007', 'unqualified_terminal_record_count', 'count'),
    ('SIT-M007', 'seed_items_with_unresolved_ancestry_count', 'count'),
    ('SIT-M007', 'ancestry_gap_disclosures', 'record_disclosures'),
    ('SIT-M008', 'shared_recorded_ancestor_count', 'count'),
    ('SIT-M008', 'matching_family_label_count', 'count'),
    ('SIT-M008', 'evaluator_overlap_disclosures', 'record_disclosures'),
    ('SIT-M008', 'evaluator_overlap_witnesses', 'witness_collection'),
    ('SIT-M009', 'externality_assessment_disclosures', 'record_disclosures'),
    ('SIT-M009', 'externality_stage_links', 'record_disclosures'),
    ('SIT-M010', 'pipeline_stage_disclosures', 'record_disclosures'),
    ('SIT-M010', 'stage_member_partition', 'partition'),
    ('SIT-M010', 'stage_occurrence_fraction', 'fraction'),
    ('SIT-M010', 'stage_occurrence_completion_interval', 'completion_interval'),
    ('SIT-M010', 'cohort_transition_disclosures', 'record_disclosures'),
    ('SIT-M010', 'cohort_transition_fraction', 'fraction'),
    ('SIT-M010', 'cohort_transition_completion_interval', 'completion_interval'),
    ('SIT-M011', 'declared_correction_route_witnesses', 'witness_collection'),
    ('SIT-M011', 'applicable_authorized_route_witnesses', 'witness_collection'),
    ('SIT-M011', 'correction_route_disclosures', 'record_disclosures'),
    ('SIT-M012', 'correction_case_record_count', 'count'),
    ('SIT-M012', 'handling_event_record_count', 'count'),
    ('SIT-M012', 'linked_change_event_record_count', 'count'),
    ('SIT-M012', 'documentary_linked_change_target_count', 'count'),
    ('SIT-M012', 'cases_with_documentary_linked_change_count', 'count'),
    ('SIT-M012', 'correction_case_disclosures', 'record_disclosures'),
    ('SIT-M012', 'correction_target_change_disclosures', 'record_disclosures'),
    ('SIT-M012', 'reported_capacity_disclosures', 'record_disclosures'),
    ('SIT-M013', 'corrective_independence_disclosures', 'record_disclosures'),
    ('SIT-M013', 'human_contribution_disclosures', 'record_disclosures'),
    ('SIT-M014', 'anomaly_context_disclosures', 'record_disclosures'),
    ('SIT-M014', 'contestation_disclosures', 'record_disclosures'),
    ('SIT-M014', 'tail_stage_result_links', 'record_disclosures'),
    ('SIT-M015', 'coverage_disclosures', 'record_disclosures'),
    ('SIT-M015', 'documentary_basis_gap_disclosures', 'record_disclosures'),
    ('SIT-M015', 'declared_basis_inventory', 'partition'),
    ('SIT-M015', 'reference_availability_inventory', 'partition'),
)

REASON_CODES = (
    'no_seed_contributions',
    'zero_denominator',
    'missing_comparison_assessment',
    'scope_unestablished',
    'dimension_not_selected',
    'unknown_endpoint',
    'upstream_coverage_incomplete',
    'unqualified_origin_boundary',
    'baseline_or_scope_cut',
    'declared_origin_only',
    'multi_origin_unallocated',
    'identity_unresolved',
    'premise_disputed',
    'lineage_cycle',
    'support_uninspectable',
    'documentary_basis_incomplete',
    'self_supporting_assurance',
    'time_applicability_unknown',
    'temporal_inconsistency',
    'roles_incomplete',
    'externality_unestablished',
    'cohort_anchor_missing',
    'cohort_anchor_ambiguous',
    'cohort_universe_unestablished',
    'stage_classification_unresolved',
    'transition_baseline_unestablished',
    'route_not_recorded',
    'authority_unestablished',
    'authority_inapplicable',
    'change_evidence_missing',
    'before_after_unresolved',
    'context_withheld_or_unavailable',
    'no_applicable_subject',
    'outside_v01',
    'analysis_not_selected',
    'resource_limit_reached',
    'execution_failed',
    'input_not_accepted',
    'completion_interval_not_needed',
    'comparison_scope_mismatch',
)

STATE_PAIRS = (
    ('completed', 'available'), ('completed', 'unavailable'),
    ('completed', 'not_applicable'), ('not_performed', 'not_evaluated'),
    ('interrupted', 'not_evaluated'), ('failed', 'not_evaluated'),
)
RESULT_ORIGINS = ('inventory', 'graph_derivation', 'attributed_record', 'qualification_check')
VALUE_KINDS = ('count', 'fraction', 'completion_interval', 'partition', 'incidence',
               'record_disclosures', 'witness_collection')
CHECK_STATES = ('met', 'unmet', 'unknown', 'not_applicable')
REASON_CLASSIFICATIONS = ('evidence_gap', 'conflict', 'structural_inapplicability',
                          'release_boundary', 'execution')
DEPENDENCY_DIMENSIONS = ('acquisition', 'analytical_method', 'model_ancestry',
                         'evaluation_rubric', 'organizational_control')
GRAPH_VIEWS = ('citation', 'material_transformation', 'claim_origin', 'model_evaluation',
               'organizational', 'stance_contestation', 'correction_routing',
               'correction_outcomes', 'pipeline_stages', 'assertion_assurance', 'succession')
# Private spellings for the counting units in definitions 15, 20-28. These
# identify units, not new metrics. case_target is the specified ordered pair.
POPULATION_UNITS = ('artifact_record', 'locator', 'actor_record', 'evidence_item',
                    'origin_event', 'relation_assertion', 'witness_path',
                    'comparison_member', 'unresolved_reference', 'frontier_occurrence',
                    'evaluation', 'correction_case', 'correction_change_record',
                    'pipeline_record', 'pipeline_member', 'case_target', 'record',
                    'evidence_reference', 'family_label', 'handling_event')
ORIGIN_DISPOSITIONS = ('unresolved_or_conflicted', 'contains_baseline_or_scope_cut',
                       'contains_declared_origin', 'multiple_documented_origins',
                       'single_documented_origin')
IMMEDIATE_DISPOSITIONS = ('inherited_only_at_evidence_layer', 'direct_origin_link_only',
                          'mixed_direct_and_inherited', 'unresolved_at_evidence_layer')
STAGE_DISPOSITIONS = ('Y', 'F', 'U')
BASIS_KINDS = ('declaration', 'documented_record', 'upstream_inference',
               'protected_attestation', 'unspecified')
REFERENCE_AVAILABILITIES = ('supplied', 'locator_only', 'withheld', 'unavailable')
PARTITION_BINDINGS = (
    ('seed_origin_dispositions', ORIGIN_DISPOSITIONS),
    ('immediate_evidence_layer_dispositions', IMMEDIATE_DISPOSITIONS),
    ('stage_member_partition', STAGE_DISPOSITIONS),
    ('declared_basis_inventory', BASIS_KINDS),
    ('reference_availability_inventory', REFERENCE_AVAILABILITIES),
)
_MAX_EXACT_INTEGER = 9_007_199_254_740_991


def _text(value, *, empty=False):
    _require(type(value) is str and (empty or bool(value)))


def _texts(values):
    _require(type(values) is tuple)
    for value in values:
        _text(value)


def _integer(value, *, positive=False):
    _require(type(value) is int and (1 if positive else 0) <= value <= _MAX_EXACT_INTEGER)


def _field_kind(family, field):
    _require(type(family) is str and type(field) is str)
    for registered_family, registered_field, kind in FIELD_BINDINGS:
        if (family, field) == (registered_family, registered_field):
            return kind
    raise TypeError('invalid_private_representation')


def _frozen_key(value):
    """Bounded internal scalar/tree identity; no public source fingerprint."""
    if value is None:
        return ('null',)
    if type(value) is str:
        return ('text', value)
    if type(value) is bool:
        return ('boolean', value)
    if type(value) is _Number:
        return ('number', value.sign, value.coefficient, value.exponent, value.source_kind)
    if type(value) is _Array:
        return ('array', tuple(_frozen_key(item) for item in value.items))
    if type(value) is _Object:
        return ('object', tuple(sorted((key, _frozen_key(item)) for key, item in value.items)))
    raise TypeError('invalid_private_representation')


def _unique(values, kinds):
    _require(type(values) is tuple)
    seen = set()
    for value in values:
        _require(type(value) in kinds)
        key = value._key()
        _require(key not in seen)
        seen.add(key)
    return frozenset(seen)


def _anchor_key(anchor):
    _require(type(anchor) is tuple)
    keys = []
    for part in anchor:
        if type(part) is str:
            keys.append(('text', part))
        elif type(part) is _InputRef:
            keys.append(part._key())
        elif part is None:
            keys.append(('null',))
        else:
            raise TypeError('invalid_private_representation')
    return tuple(keys)


@dataclass(frozen=True, slots=True, repr=False)
class _InputRef:
    """An input collection/identity/selector, never a derived-object ID."""
    collection: str
    identifier: str
    selector: str | None = None

    def __post_init__(self):
        _require(type(self.collection) is str and self.collection in
                 ('inquiries', 'records', 'assertions', 'evidence_references'))
        _text(self.identifier)
        if self.selector is not None:
            _text(self.selector)

    def _key(self):
        return ('input', self.collection, self.identifier, self.selector or '')


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Scope:
    inquiry_ref: _InputRef
    claim_refs: tuple
    target_refs: tuple
    dependency_dimension: str | None
    graph_view: str | None
    temporal_basis: str
    requested_time: _Node | None
    coverage_refs: tuple
    qualifications: tuple
    operation_anchor: tuple = ()

    def __post_init__(self):
        _require(type(self.inquiry_ref) is _InputRef and self.inquiry_ref.collection == 'inquiries'
                 and self.inquiry_ref.selector is None)
        _unique(self.claim_refs, (_InputRef,))
        _require(all(ref.collection == 'records' and ref.selector is None for ref in self.claim_refs))
        _unique(self.target_refs, (_InputRef,))
        _unique(self.coverage_refs, (_InputRef,))
        _require(all(ref.collection == 'assertions' for ref in self.coverage_refs))
        _require(self.dependency_dimension is None or
                 (type(self.dependency_dimension) is str and self.dependency_dimension in DEPENDENCY_DIMENSIONS))
        _require(self.graph_view is None or (type(self.graph_view) is str and self.graph_view in GRAPH_VIEWS))
        _require(type(self.temporal_basis) is str and self.temporal_basis in ('snapshot_structural', 'time_specific'))
        _require(self.requested_time is None or
                 (type(self.requested_time) is _Node and self.requested_time.shape == 'TimeValue'))
        if self.temporal_basis == 'time_specific':
            _require(self.requested_time is not None)
        _texts(self.qualifications)
        if not self.claim_refs or self.dependency_dimension is None or self.graph_view is None:
            _require(bool(self.qualifications))
        _anchor_key(self.operation_anchor)

    def _key(self):
        time = ('null',) if self.requested_time is None else _frozen_key(self.requested_time.fields)
        return ('scope', self.inquiry_ref._key(), tuple(sorted(ref._key() for ref in self.claim_refs)),
                tuple(sorted(ref._key() for ref in self.target_refs)), self.dependency_dimension or '',
                self.graph_view or '', self.temporal_basis, time, _anchor_key(self.operation_anchor))


@dataclass(frozen=True, slots=True, repr=False)
class _CaseTarget:
    """A counted (case_ref, before_ref) pair; order and both identities matter."""
    case_ref: _InputRef
    before_ref: _InputRef

    def __post_init__(self):
        _require(type(self.case_ref) is _InputRef and self.case_ref.collection == 'records')
        _require(type(self.before_ref) is _InputRef and self.before_ref.collection == 'records')

    def _key(self):
        return ('case_target', self.case_ref._key(), self.before_ref._key())


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _BasisRef:
    source: _InputRef

    def __post_init__(self):
        _require(type(self.source) is _InputRef)

    def _key(self):
        return ('basis', self.source._key())


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Population:
    scope: _Scope
    unit: str
    member_refs: tuple
    selection_rule: str
    coverage_refs: tuple = ()
    basis_refs: tuple = ()
    membership_state: str = 'enumerated_for_scope'
    qualifications: tuple = ()

    def __post_init__(self):
        _require(type(self.scope) is _Scope and type(self.unit) is str and self.unit in POPULATION_UNITS)
        _unique(self.member_refs, (_CaseTarget,) if self.unit == 'case_target' else (_InputRef,))
        _text(self.selection_rule)
        _unique(self.coverage_refs, (_InputRef,))
        _require(all(ref.collection == 'assertions' for ref in self.coverage_refs))
        _unique(self.basis_refs, (_BasisRef,))
        _require(type(self.membership_state) is str and self.membership_state in
                 ('enumerated_for_scope', 'unestablished'))
        _texts(self.qualifications)

    def _key(self):
        return ('population', self.scope._key(), self.unit, self.selection_rule,
                tuple(sorted(ref._key() for ref in self.member_refs)))


def _enumerated(population):
    _require(type(population) is _Population and population.membership_state == 'enumerated_for_scope')


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Count:
    value: int
    population: _Population

    def __post_init__(self):
        _integer(self.value)
        _enumerated(self.population)
        _require(self.value == len(self.population.member_refs))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Fraction:
    """Unreduced exact components; the owner proves the field's arithmetic."""
    numerator: int
    denominator: int
    population: _Population

    def __post_init__(self):
        _integer(self.numerator)
        _integer(self.denominator, positive=True)
        _enumerated(self.population)
        _require(bool(self.population.member_refs))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _CompletionInterval:
    lower: _Fraction
    upper: _Fraction
    interval_kind: str
    partition: object

    def __post_init__(self):
        _require(type(self.lower) is _Fraction and type(self.upper) is _Fraction)
        _require(type(self.interval_kind) is str and self.interval_kind in
                 ('finite_record_completion', 'finite_cohort_completion'))
        _require(self.lower.population is self.upper.population)
        _require(type(self.partition) is _Partition and self.partition.population is self.lower.population)
        _require(self.lower.denominator == self.upper.denominator == len(self.lower.population.member_refs))
        _require(0 <= self.lower.numerator <= self.upper.numerator <= self.lower.denominator)
        expected = IMMEDIATE_DISPOSITIONS if self.interval_kind == 'finite_record_completion' else STAGE_DISPOSITIONS
        _require({category.label for category in self.partition.categories} == set(expected))
        counts = {category.label: category.count for category in self.partition.categories}
        positive = counts['inherited_only_at_evidence_layer'] if self.interval_kind == 'finite_record_completion' else counts['Y']
        unresolved = counts['unresolved_at_evidence_layer'] if self.interval_kind == 'finite_record_completion' else counts['U']
        _require(unresolved > 0 and self.lower.numerator == positive and self.upper.numerator == positive + unresolved)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _PartitionCategory:
    label: str
    member_refs: tuple
    count: int

    def __post_init__(self):
        _require(type(self.label) is str and self.label in
                 ORIGIN_DISPOSITIONS + IMMEDIATE_DISPOSITIONS + STAGE_DISPOSITIONS + BASIS_KINDS + REFERENCE_AVAILABILITIES)
        _unique(self.member_refs, (_InputRef, _CaseTarget))
        _integer(self.count)
        _require(self.count == len(self.member_refs))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Partition:
    population: _Population
    categories: tuple

    def __post_init__(self):
        _enumerated(self.population)
        _require(type(self.categories) is tuple and bool(self.categories))
        labels, members = set(), set()
        for category in self.categories:
            _require(type(category) is _PartitionCategory and category.label not in labels)
            labels.add(category.label)
            keys = {ref._key() for ref in category.member_refs}
            _require(not keys & members)
            members.update(keys)
        _require(members == {ref._key() for ref in self.population.member_refs})


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _IncidenceRow:
    member_ref: _InputRef
    origin_refs: tuple

    def __post_init__(self):
        _require(type(self.member_ref) is _InputRef)
        _unique(self.origin_refs, (_InputRef,))
        _require(all(ref.collection == 'records' for ref in self.origin_refs))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Incidence:
    population: _Population
    memberships: tuple

    def __post_init__(self):
        _enumerated(self.population)
        _require(self.population.unit == 'evidence_item')
        _require(type(self.memberships) is tuple)
        seen = set()
        for row in self.memberships:
            _require(type(row) is _IncidenceRow and row.member_ref._key() not in seen)
            seen.add(row.member_ref._key())
        _require(seen == {ref._key() for ref in self.population.member_refs})

    @property
    def nonexclusive(self):
        return True

    @property
    def origin_counts(self):
        counts, refs = {}, {}
        for row in self.memberships:
            for origin in row.origin_refs:
                key = origin._key()
                refs[key] = origin
                counts[key] = counts.get(key, 0) + 1
        return tuple((refs[key], counts[key]) for key in sorted(counts))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _ResultRef:
    diagnostic_id: str
    field_key: str
    scope: _Scope

    def __post_init__(self):
        _field_kind(self.diagnostic_id, self.field_key)
        _require(type(self.scope) is _Scope)

    def _key(self):
        return ('result', self.diagnostic_id, self.field_key, self.scope._key())


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Disclosure:
    source: object
    fields: _Object
    qualifications: tuple = ()

    def __post_init__(self):
        _require(type(self.source) in (_InputRef, _ResultRef) and type(self.fields) is _Object)
        _texts(self.qualifications)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _RecordDisclosures:
    records: tuple

    def __post_init__(self):
        _require(type(self.records) is tuple and all(type(row) is _Disclosure for row in self.records))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _WitnessRef:
    """Private semantic link to a finite Finding witness, not a new public ID.

    Its owner must finish the witness before retaining this reference. This
    symbolic primitive neither traverses a graph nor reserves witness quota.
    """
    scope: _Scope
    kind: str
    anchor: tuple

    def __post_init__(self):
        _require(type(self.scope) is _Scope and type(self.kind) is str and
                 self.kind in ('path', 'cycle', 'member_set'))
        _require(type(self.anchor) is tuple and bool(self.anchor))
        _anchor_key(self.anchor)

    def _key(self):
        return ('finding_witness', self.scope._key(), self.kind, _anchor_key(self.anchor))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _WitnessCollection:
    witness_refs: tuple

    def __post_init__(self):
        _unique(self.witness_refs, (_WitnessRef,))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Reason:
    code: str
    scope: _Scope
    affected_result_refs: tuple
    input_refs: tuple
    detail: str
    classification: str

    def __post_init__(self):
        _require(type(self.code) is str and self.code in REASON_CODES and type(self.scope) is _Scope)
        _unique(self.affected_result_refs, (_ResultRef,))
        _require(all(ref.scope._key() == self.scope._key() for ref in self.affected_result_refs))
        _unique(self.input_refs, (_InputRef,))
        _text(self.detail)
        _require(type(self.classification) is str and self.classification in REASON_CLASSIFICATIONS)

    def _key(self):
        return ('reason', self.code, self.scope._key(), tuple(sorted(ref._key() for ref in self.input_refs)),
                self.detail, self.classification)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _PrerequisiteCheck:
    check_id: str
    result_ref: _ResultRef
    state: str
    input_refs: tuple
    reason_refs: tuple
    note: str

    def __post_init__(self):
        _require(type(self.check_id) is str and self.check_id in (
            'PC01', 'PC02', 'PC03', 'PC04', 'PC05', 'PC06', 'PC07', 'PC08',
            'PC09', 'PC10', 'PC11', 'PC12', 'PC13', 'PC14', 'PC15', 'PC16',
            'PC17', 'PC18', 'PC19', 'PC20', 'PC21', 'PC22', 'PC23', 'PC24'))
        _require(type(self.result_ref) is _ResultRef and type(self.state) is str and self.state in CHECK_STATES)
        _unique(self.input_refs, (_InputRef,))
        _unique(self.reason_refs, (_Reason,))
        _require(all(reason.scope._key() == self.result_ref.scope._key() for reason in self.reason_refs))
        _text(self.note)

    def _key(self):
        return ('check', self.check_id, self.result_ref._key())


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Result:
    """A complete representation supplied by its semantic owner, no run claim."""
    ref: _ResultRef
    population_refs: tuple
    execution_state: str
    result_state: str
    result_origin: str
    value_kind: str
    value: object
    check_refs: tuple
    basis_refs: tuple
    witness_refs: tuple
    reason_refs: tuple
    interpretation_limit: str

    def __post_init__(self):
        _require(type(self.ref) is _ResultRef)
        _require(type(self.execution_state) is str and type(self.result_state) is str and
                 (self.execution_state, self.result_state) in STATE_PAIRS)
        _require(type(self.result_origin) is str and self.result_origin in RESULT_ORIGINS)
        _require(type(self.value_kind) is str and self.value_kind == _field_kind(self.ref.diagnostic_id, self.ref.field_key))
        _unique(self.population_refs, (_Population,))
        _require(all(pop.scope is self.ref.scope for pop in self.population_refs))
        _unique(self.check_refs, (_PrerequisiteCheck,))
        _require(all(check.result_ref is self.ref for check in self.check_refs))
        _unique(self.basis_refs, (_BasisRef,))
        _unique(self.witness_refs, (_WitnessRef,))
        _require(all(witness.scope is self.ref.scope for witness in self.witness_refs))
        _unique(self.reason_refs, (_Reason,))
        _require(all(reason.scope is self.ref.scope and
                     any(ref is self.ref for ref in reason.affected_result_refs)
                     for reason in self.reason_refs))
        _text(self.interpretation_limit)
        if self.result_state != 'available':
            _require(self.value is None and bool(self.reason_refs))
            codes = {reason.code for reason in self.reason_refs}
            if self.execution_state == 'interrupted':
                _require('resource_limit_reached' in codes)
            elif self.execution_state == 'failed':
                _require('execution_failed' in codes)
            elif self.execution_state == 'not_performed':
                _require(bool(codes & {'analysis_not_selected', 'resource_limit_reached', 'input_not_accepted'}))
            elif self.result_state == 'not_applicable':
                _require(any(reason.classification == 'structural_inapplicability' for reason in self.reason_refs))
            return
        # A carried exact-scope/completion fact may not contradict a committed value.
        # Other PCs remain field-specific; navigation unions are never an AND gate.
        _require(all(check.state == 'met' for check in self.check_refs
                     if check.check_id in ('PC02', 'PC24')))
        kinds = {'count': _Count, 'fraction': _Fraction, 'completion_interval': _CompletionInterval,
                 'partition': _Partition, 'incidence': _Incidence,
                 'record_disclosures': _RecordDisclosures, 'witness_collection': _WitnessCollection}
        _require(type(self.value) is kinds[self.value_kind])
        population = None
        if self.value_kind in ('count', 'fraction', 'partition', 'incidence'):
            population = self.value.population
        elif self.value_kind == 'completion_interval':
            population = self.value.lower.population
            _require(self.value.lower.numerator < self.value.upper.numerator)
            expected_interval = ('finite_record_completion' if self.ref.diagnostic_id == 'SIT-M006'
                                 else 'finite_cohort_completion')
            _require(self.value.interval_kind == expected_interval)
        if population is not None:
            _require(any(pop is population for pop in self.population_refs))
        if self.value_kind == 'fraction':
            n = len(population.member_refs)
            _require(self.value.denominator == (n * n if self.ref.field_key == 'single_origin_contribution_hhi' else n))
            _require(self.value.numerator <= self.value.denominator)
        elif self.value_kind == 'partition':
            for field, labels in PARTITION_BINDINGS:
                if field == self.ref.field_key:
                    _require({category.label for category in self.value.categories} == set(labels))
        elif self.value_kind == 'witness_collection':
            _require(len(self.value.witness_refs) == len(self.witness_refs) and
                     all(any(link is ref for link in self.witness_refs) for ref in self.value.witness_refs))

    def _key(self):
        return self.ref._key()


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _ResultSet:
    """Local atomic slots only; no capability/run completion or report root."""
    results: tuple

    def __post_init__(self):
        _unique(self.results, (_Result,))
