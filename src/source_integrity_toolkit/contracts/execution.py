# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: RUNTIME_BOUNDARY.

Authority-free private port and payload-limited declaration types. No budget,
clock, cancellation trigger, decoder or preparation operation is implemented.
Messages cannot carry arbitrary caller content. Construction is internal and
cannot grant input acceptance. Public audit functions remain exact refusals.
"""
from dataclasses import dataclass
from typing import Protocol
from .bundle import _require


class _BudgetPort(Protocol):
    """Only project-owned instances from the later runtime may supply this port."""
    def charge(self, units: int) -> None:
        ...

    def check(self) -> None:
        ...


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _PreparationStop:
    """A safe stopped-input transport, never a completed audit envelope."""
    input_state: str
    execution_state: str
    reason_code: str

    def __post_init__(self) -> None:
        _require(type(self.input_state) is str and
                 self.input_state in ("accepted", "rejected", "not_completed"))
        _require(type(self.execution_state) is str and
                 self.execution_state in ("rejected", "interrupted", "failed"))
        _require(type(self.reason_code) is str)
        if self.execution_state == "rejected":
            _require(self.input_state == "rejected" and self.reason_code == "input_not_accepted")
        elif self.execution_state == "interrupted":
            _require(self.input_state in ("accepted", "not_completed") and
                     self.reason_code == "resource_limit_reached")
        else:
            _require(self.input_state in ("accepted", "not_completed") and
                     self.reason_code == "execution_failed")


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _AuditCancelled(Exception):
    """Payload-free cancellation with actual input state, separate from failure."""
    input_state: str

    def __post_init__(self) -> None:
        _require(type(self.input_state) is str and
                 self.input_state in ("accepted", "not_completed"))
