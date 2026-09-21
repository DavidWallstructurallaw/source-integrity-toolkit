# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: RUNTIME_BOUNDARY.

Private authority-free execution port and payload-free stopping vocabulary.
Ports are supplied only by project-owned runtime construction, never evidence,
public options or callbacks. Type hints do not authenticate an arbitrary port.
No input acceptance, audit envelope, filesystem or clock is constructed here.
"""
from dataclasses import dataclass
from typing import Protocol


def _require(ok: bool) -> None:
    if not ok:
        raise TypeError("invalid_private_representation")


class _BudgetPort(Protocol):
    """Private precondition: the runtime has supplied its own budget instance."""
    def charge(self, units: int) -> None:
        ...

    def check(self) -> None:
        ...

    def reject(self, code: str, constraint: str | None = None) -> None:
        ...

    def interrupt(self, limit_id: str) -> None:
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


_STRUCTURAL_CODES = (
    "invalid_syntax", "duplicate_key", "unsupported_input_contract",
    "duplicate_identifier", "dangling_reference", "type_or_enum_violation",
    "missing_required_field", "endpoint_or_claim_mismatch", "invalid_time",
    "input_constraint_violation",
)
_CONSTRAINT_CODES = (
    "exact_integer_range", "unicode_scalar", "identifier_ascii",
    "identifier_length", "string_length", "locator_length", "container_cycle",
)
_PREPARATION_LIMIT_IDS = (
    "WU9-L01", "WU9-L02", "WU9-L03", "WU9-L04", "WU9-L05", "WU9-L06",
    "WU9-L07", "WU9-L08", "WU9-L09", "WU9-L11", "WU9-L12",
)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _PreparationAborted(Exception):
    """Finite constant classification only, with no input or native exception."""
    stop: _PreparationStop
    diagnostic_code: str | None = None
    limit_id: str | None = None
    constraint: str | None = None

    def __post_init__(self) -> None:
        _require(type(self.stop) is _PreparationStop)
        if self.stop.execution_state == "rejected":
            _require(type(self.diagnostic_code) is str and
                     self.diagnostic_code in _STRUCTURAL_CODES and self.limit_id is None)
            if self.diagnostic_code == "input_constraint_violation":
                _require(type(self.constraint) is str and self.constraint in _CONSTRAINT_CODES)
            else:
                _require(self.constraint is None)
        elif self.stop.execution_state == "interrupted":
            _require(self.diagnostic_code is None and type(self.limit_id) is str and
                     self.limit_id in _PREPARATION_LIMIT_IDS and self.constraint is None)
        else:
            _require(self.diagnostic_code is None and self.limit_id is None and self.constraint is None)

    def __str__(self) -> str:
        return "input_preparation_stopped"

    def __repr__(self) -> str:
        return "_PreparationAborted()"


def _byte_work(port: _BudgetPort, length: int, visits: int = 0) -> None:
    """Precharge a bounded native pass; cooperative check at each <=256 bytes.

    length and visits are project-calculated nonnegative exact integers. This
    is a conservative reference work model, not a CPU-instruction estimate.
    """
    if type(length) is not int or length < 0 or type(visits) is not int or visits < 0:
        raise TypeError("invalid_private_representation")
    port.charge(visits)
    remaining = length
    while remaining:
        port.charge(1)
        remaining -= min(256, remaining)
    port.check()


class _JobPort(_BudgetPort, Protocol):
    """One project-owned job's charges debit its quota and global ledger once.

    This contract confers no I/O, clock, configurable limit or caller callback.
    A port is valid only for its current job; it cannot start or resume jobs.
    """
    def check_analysis(self) -> None:
        """Require current analysis work, excluding a finalization-only port."""
        ...


class _FinalizationPort(Protocol):
    """Restricted accounting for bounded delivery after analysis has stopped."""
    def charge(self, units: int) -> None:
        ...

    def check(self) -> None:
        ...


_ANALYSIS_LIMIT_IDS = _PREPARATION_LIMIT_IDS + ("WU9-L13",)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _AnalysisAborted(Exception):
    """Payload-free resource/failure transport, separate from cancellation."""
    stop: _PreparationStop
    limit_id: str | None = None

    def __post_init__(self) -> None:
        _require(type(self.stop) is _PreparationStop)
        _require(self.stop.input_state in ("accepted", "not_completed"))
        if self.stop.execution_state == "interrupted":
            _require(type(self.limit_id) is str and self.limit_id in _ANALYSIS_LIMIT_IDS)
        else:
            _require(self.stop.execution_state == "failed" and self.limit_id is None)

    def __str__(self) -> str:
        return "analytical_processing_stopped"

    def __repr__(self) -> str:
        return "_AnalysisAborted()"
