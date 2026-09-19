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
