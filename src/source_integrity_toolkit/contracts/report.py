# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: REPORT_CONTRACT.

Private observability-preparation declarations only. No Result, audit envelope,
report identifiers, renderer or available_result_refs are constructed here.
Level labels are independent evidence domains, never a score or maximum level.
All whole prerequisite checks remain execution-pending in this W02 delivery.
Only a later bounded preparation operation may complete PC01. PC02-PC24
constituent observations remain distinct from whole-check qualification.
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
