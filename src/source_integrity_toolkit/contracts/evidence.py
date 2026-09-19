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
