# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: EVIDENCE_BASIS.

Private schema-tagged immutable records. The tag selects a declared shape,
including every shared structure, record payload and assertion detail branch.
The exact supplied fields live in _Node.fields.items; there is no transformed
truth/independence flag, defaulted Gap or extra source field. A shape tag is an
internal interpretation target, never evidence that its fields are valid.

Only the later bounded mapper may create validated nodes from admitted input.
These local constructors require bounded immutable parts and validate that
representation precondition, not field semantics or snapshot references.
"""
from dataclasses import dataclass
from .bundle import _Object, _require
from .constants import SHAPES


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Node:
    """One exact field bag with a declared shape; no admission status."""
    shape: str
    fields: _Object

    def __post_init__(self) -> None:
        _require(type(self.shape) is str)
        _require(any(self.shape == row[0] for row in SHAPES))
        _require(type(self.fields) is _Object)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Attribution:
    """Keep an attributed node and its explicit source provenance together."""
    node: _Node
    provenance: _Node

    def __post_init__(self) -> None:
        _require(type(self.node) is _Node and type(self.provenance) is _Node)
        _require(self.provenance.shape == "Provenance")


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Entity:
    """Private indexed source record, preserving its complete field bag."""
    collection: str
    identifier: str
    kind: str
    node: _Node

    def __post_init__(self) -> None:
        _require(type(self.collection) is str and self.collection in
                 ("inquiries", "records", "assertions", "evidence_references"))
        _require(type(self.identifier) is str and type(self.kind) is str)
        _require(type(self.node) is _Node)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _RecordLink:
    """One supplied field occurrence, never a qualified graph edge.

    Selector addresses the normalized source object. The full owner and any
    role-specific basis stay in the snapshot; no synthetic assertion is added.
    """
    owner: _Entity
    selector: str
    target: _Entity

    def __post_init__(self) -> None:
        _require(type(self.owner) is _Entity and type(self.target) is _Entity)
        _require(type(self.selector) is str)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _InquiryPlan:
    """Finite explicit bindings, with no graph search or analytical result."""
    inquiry: _Entity
    assertion_refs: tuple
    anomaly_refs: tuple

    def __post_init__(self) -> None:
        _require(type(self.inquiry) is _Entity and self.inquiry.collection == "inquiries")
        for refs in (self.assertion_refs, self.anomaly_refs):
            _require(type(refs) is tuple)
            _require(all(type(ref) is str for ref in refs))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _InputObservation:
    """Private input fact only; no public Reason, PC result or finding."""
    kind: str
    collection: str
    identifier: str
    selector: str

    def __post_init__(self) -> None:
        _require(type(self.kind) is str and self.kind == "known_window_reversed")
        _require(type(self.collection) is str and type(self.identifier) is str)
        _require(type(self.selector) is str)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _PreparedBundle:
    """Trusted W05 construction after every bounded admission step.

    The private constructor is no independent validator. Runtime alone returns
    this object after completing capture, structure, references, time, indexes
    and the finite plan. It is not an audit-report schema or a truth certificate.
    """
    tree: _Object
    source_mode: str
    entities: tuple
    links: tuple
    plan: tuple
    observations: tuple
    captured_tree: _Object

    def __post_init__(self) -> None:
        _require(type(self.tree) is _Object and type(self.captured_tree) is _Object)
        _require(type(self.source_mode) is str and self.source_mode in
                 ("constructed_value", "supplied_utf8"))
        for values, kind in ((self.entities, _Entity), (self.links, _RecordLink),
                             (self.plan, _InquiryPlan), (self.observations, _InputObservation)):
            _require(type(values) is tuple)
            _require(all(type(value) is kind for value in values))

    @property
    def input_state(self) -> str:
        return "accepted"

    @property
    def preparation_kind(self) -> str:
        return "private_prepared_input"


# P3-W03 shared documentary facts. The accepted preparation definitions above
# retain their original meaning. These representations add no input admission,
# graph eligibility provider, semantic authority or public report contract.
from .constants import VOCABULARIES

_QUALIFICATION_STATES = ('met', 'unmet', 'unknown')
_QUALIFICATION_REASON_CODES = (
    'scope_unestablished', 'dimension_not_selected', 'unknown_endpoint',
    'upstream_coverage_incomplete', 'identity_unresolved', 'premise_disputed',
    'support_uninspectable', 'documentary_basis_incomplete', 'self_supporting_assurance',
    'time_applicability_unknown', 'temporal_inconsistency',
)
_QUALIFICATION_GRAPH_VIEWS = (
    'citation', 'material_transformation', 'claim_origin', 'model_evaluation',
    'organizational', 'stance_contestation', 'correction_routing',
    'correction_outcomes', 'pipeline_stages', 'assertion_assurance', 'succession',
)
_TIME_COMPARISONS = ('before', 'equal', 'after', 'overlap', 'unknown')
_PROVIDER_OWNERS = (('PC03', 'SOURCE_INVENTORY'), ('PC04', 'GRAPH_VIEW_CONTRACT'))


def _qualification_text(value: object, *, empty: bool = False) -> None:
    _require(type(value) is str and (empty or bool(value)))


def _qualification_texts(values: object, *, unique: bool = False) -> None:
    _require(type(values) is tuple)
    seen = set()
    for value in values:
        _qualification_text(value)
        if unique:
            _require(value not in seen)
            seen.add(value)


def _qualification_reasons(values: object) -> None:
    _qualification_texts(values, unique=True)
    _require(all(value in _QUALIFICATION_REASON_CODES for value in values))


def _qualification_state(state: object, reasons: object) -> None:
    _require(type(state) is str and state in _QUALIFICATION_STATES)
    _qualification_reasons(reasons)
    if state != 'met':
        _require(bool(reasons))


@dataclass(frozen=True, slots=True, repr=False)
class _SourceAddress:
    """Inert location in the one admitted snapshot, never a path to open.

    The empty selector names the original record; a nonempty selector names
    its original field or role. No supplied content is copied into an ID.
    """
    collection: str
    record_id: str
    selector: str = ''

    def __post_init__(self) -> None:
        _require(type(self.collection) is str and self.collection in
                 ('inquiries', 'records', 'assertions', 'evidence_references'))
        _qualification_text(self.record_id)
        _qualification_text(self.selector, empty=True)


def _qualification_addresses(values: object) -> None:
    _require(type(values) is tuple)
    seen = set()
    for value in values:
        _require(type(value) is _SourceAddress)
        key = (value.collection, value.record_id, value.selector)
        _require(key not in seen)
        seen.add(key)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _QualificationContext:
    """The exact source question used by one paid component operation.

    IDs still refer to the admitted snapshot. The semantic helper resolves
    their types and supplied bindings; construction cannot manufacture that
    resolution, scope applicability, an enumerated population or PC03/PC04.
    Empty Claim/member lists remain empty; they never denote a wildcard.
    """
    inquiry_ref: str
    claim_refs: tuple
    subject_refs: tuple
    dependency_dimension: str | None
    temporal_basis: str
    requested_time: _Node | None
    coverage_kind: str | None
    relation_types: tuple
    graph_view: str | None = None
    operation_anchor: tuple = ()

    def __post_init__(self) -> None:
        _qualification_text(self.inquiry_ref)
        _qualification_texts(self.claim_refs, unique=True)
        _qualification_texts(self.subject_refs, unique=True)
        _require(self.dependency_dimension is None or
                 (type(self.dependency_dimension) is str and
                  self.dependency_dimension in VOCABULARIES['dimension']))
        _require(type(self.temporal_basis) is str and
                 self.temporal_basis in ('snapshot_structural', 'time_specific'))
        _require(self.requested_time is None or
                 (type(self.requested_time) is _Node and self.requested_time.shape == 'TimeValue'))
        if self.temporal_basis == 'time_specific':
            _require(self.requested_time is not None)
        _require(self.coverage_kind is None or
                 (type(self.coverage_kind) is str and self.coverage_kind in VOCABULARIES['coverage_kind']))
        _qualification_texts(self.relation_types, unique=True)
        _require(all(value in VOCABULARIES['predicate'] for value in self.relation_types))
        _require(self.graph_view is None or
                 (type(self.graph_view) is str and self.graph_view in _QUALIFICATION_GRAPH_VIEWS))
        _require(type(self.operation_anchor) is tuple)
        for part in self.operation_anchor:
            _require(part is None or type(part) in (str, _SourceAddress))
            if type(part) is str:
                _qualification_text(part)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _BasisQualification:
    """One component's attributed documentary/identity/conflict assessment.

    declared_basis retains the original label. state describes the particular
    checked prerequisite, not truth, independence, graph eligibility or rank.
    The paid owner supplies bounded, already frozen parts after examination;
    this constructor checks representation and is not proof the work occurred.
    """
    source: _SourceAddress
    declared_basis: str
    state: str
    reason_codes: tuple
    support_refs: tuple
    qualifications: tuple
    context: _QualificationContext

    def __post_init__(self) -> None:
        _require(type(self.source) is _SourceAddress)
        _require(type(self.declared_basis) is str and self.declared_basis in VOCABULARIES['basis_kind'])
        _qualification_state(self.state, self.reason_codes)
        _qualification_addresses(self.support_refs)
        _qualification_texts(self.qualifications)
        _require(type(self.context) is _QualificationContext)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _CoverageQualification:
    """Qualification beside the complete original coverage Assertion.

    A complete_for_scope source label is never overwritten by this outcome.
    The exact context and source distinguish citation, model, upstream, route
    and pipeline coverage. No universal completeness percentage is implied.
    """
    source: _SourceAddress
    state: str
    reason_codes: tuple
    support_refs: tuple
    qualifications: tuple
    coverage: _Entity
    context: _QualificationContext

    def __post_init__(self) -> None:
        _require(type(self.source) is _SourceAddress and self.source.collection == 'assertions')
        _qualification_state(self.state, self.reason_codes)
        _qualification_addresses(self.support_refs)
        _qualification_texts(self.qualifications)
        _require(type(self.coverage) is _Entity and self.coverage.collection == 'assertions'
                 and self.coverage.identifier == self.source.record_id)
        _require(type(self.context) is _QualificationContext)


def _qualification_times(values: object) -> None:
    _require(type(values) is tuple)
    _require(all(type(value) is _Node and value.shape == 'TimeValue' for value in values))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _TimeComparison:
    """A comparison of the retained TimeValues, with their native precision.

    This representation does not choose TimeWindow endpoint inclusion or turn
    dates into midnight instants. overlap/unknown remain distinct from equal.
    """
    comparison: str
    reason_codes: tuple
    source_times: tuple

    def __post_init__(self) -> None:
        _require(type(self.comparison) is str and self.comparison in _TIME_COMPARISONS)
        _qualification_reasons(self.reason_codes)
        _qualification_times(self.source_times)
        _require(len(self.source_times) == 2)
        if self.comparison in ('overlap', 'unknown'):
            _require(bool(self.reason_codes))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _TimeQualification:
    """Scope-specific temporal support, not a reconstructed event history."""
    state: str
    reason_codes: tuple
    comparison: str | None = None
    source_times: tuple = ()

    def __post_init__(self) -> None:
        _qualification_state(self.state, self.reason_codes)
        _require(self.comparison is None or
                 (type(self.comparison) is str and self.comparison in _TIME_COMPARISONS))
        _qualification_times(self.source_times)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _ProviderFact:
    """Trusted component input from the named future semantic owner.

    PC03 remains SOURCE_INVENTORY and PC04 remains GRAPH_VIEW_CONTRACT. W03
    component fixtures may construct these explicit facts; that does not mean
    either provider or the W13 integration has run. A consuming helper checks
    the exact prepared-object and context identities before using the fact.
    There is no caller-controlled port, callback, lookup or authority grant.
    """
    check_id: str
    owner: str
    context: _QualificationContext
    state: str
    input_refs: tuple
    prepared: _PreparedBundle

    def __post_init__(self) -> None:
        _require(type(self.check_id) is str and type(self.owner) is str and
                 (self.check_id, self.owner) in _PROVIDER_OWNERS)
        _require(type(self.context) is _QualificationContext)
        _require(type(self.state) is str and self.state in
                 ('met', 'unmet', 'unknown', 'not_applicable'))
        _qualification_addresses(self.input_refs)
        _require(type(self.prepared) is _PreparedBundle)
