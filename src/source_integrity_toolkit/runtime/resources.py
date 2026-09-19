# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: RUNTIME_BOUNDARY. Preparation-only global work/deadline ledger.

SIT-RP-0.1 section 19 and Phase 2 section 3.1: fixed 10,000,000 total,
1,024 prepaid emergency units inside that total, cooperative sixty seconds.
No per-analysis scope, report, witness, I/O or public invocation is implemented.
Only the zero-argument project factory creates a context. Tests patch the fixed
clock symbol outside the product; no caller-supplied clock/limit is accepted.
This is not isolation from malicious same-process mutation or hard real time.
"""
from dataclasses import dataclass, field
from time import monotonic_ns
from ..contracts.execution import (
    _PreparationStop, _PreparationAborted, _AuditCancelled,
    _STRUCTURAL_CODES, _PREPARATION_LIMIT_IDS, _CONSTRAINT_CODES,
)

_WORK_LIMIT = 10_000_000
_EMERGENCY_RESERVE = 1_024
_DEADLINE_NS = 60_000_000_000


@dataclass(slots=True, repr=False, eq=False)
class _PreparationBudget:
    _used: int = field(default=_EMERGENCY_RESERVE, init=False)
    _start: int = field(default=0, init=False)
    _last: int = field(default=0, init=False)
    _state: str = field(default="not_completed", init=False)
    _cause: object = field(default=None, init=False)
    _emergency_taken: bool = field(default=False, init=False)

    def __post_init__(self) -> None:
        now = self._now()
        self._start = now
        self._last = now

    @property
    def used(self) -> int:
        return self._used

    @property
    def remaining(self) -> int:
        return _WORK_LIMIT - self._used

    @property
    def input_state(self) -> str:
        return self._state

    def _raise_existing(self) -> None:
        if self._cause is not None:
            raise self._cause from None

    def _now(self) -> int:
        try:
            value = monotonic_ns()
        except KeyboardInterrupt:
            self.cancel()
        except Exception:
            self.fail()
        if type(value) is not int:
            self.fail()
        return value

    def check(self) -> None:
        self._raise_existing()
        now = self._now()
        if now < self._last:
            self.fail()
        self._last = now
        if now - self._start > _DEADLINE_NS:
            self.interrupt("WU9-L12")

    def charge(self, units: int) -> None:
        self.check()
        if type(units) is not int or units < 0:
            self.fail()
        if units > _WORK_LIMIT - self._used:
            self.interrupt("WU9-L11")
        self._used += units

    def interrupt(self, limit_id: str) -> None:
        self._raise_existing()
        if type(limit_id) is not str or limit_id not in _PREPARATION_LIMIT_IDS:
            self.fail()
        self._cause = _PreparationAborted(
            _PreparationStop(self._state, "interrupted", "resource_limit_reached"),
            limit_id=limit_id,
        )
        raise self._cause from None

    def reject(self, code: str, constraint: str | None = None) -> None:
        self._raise_existing()
        if type(code) is not str or code not in _STRUCTURAL_CODES or self._state != "not_completed":
            self.fail()
        if code == "input_constraint_violation":
            if type(constraint) is not str or constraint not in _CONSTRAINT_CODES:
                self.fail()
        elif constraint is not None:
            self.fail()
        self._state = "rejected"
        self._cause = _PreparationAborted(
            _PreparationStop("rejected", "rejected", "input_not_accepted"), code, constraint=constraint,
        )
        raise self._cause from None

    def fail(self) -> None:
        self._raise_existing()
        self._cause = _PreparationAborted(
            _PreparationStop(self._state, "failed", "execution_failed"),
        )
        raise self._cause from None

    def cancel(self) -> None:
        self._raise_existing()
        self._cause = _AuditCancelled(self._state)
        raise self._cause from None

    def record_input_acceptance(self) -> None:
        """Trusted future W05 boundary only, after all admission work completes.

        This records a caller-established fact; it performs no validation and is
        never exposed through the public API or selected by source data.
        """
        self.check()
        if self._state != "not_completed":
            self.fail()
        self._state = "accepted"

    def take_emergency(self) -> object:
        """One prepaid, constant-size delivery; no reset, resumption or refund."""
        if self._cause is None:
            self.fail()
        if self._emergency_taken:
            raise RuntimeError("emergency_delivery_already_used") from None
        self._emergency_taken = True
        return self._cause


def _new_budget() -> _PreparationBudget:
    return _PreparationBudget()
