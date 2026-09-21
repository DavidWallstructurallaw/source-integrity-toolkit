# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: RUNTIME_BOUNDARY. Private preparation and analytical work ledgers.

SIT-RP-0.1 section 19 and Phase 2 section 3.1: fixed 10,000,000 total,
1,024 prepaid emergency units inside that total, cooperative sixty seconds.
The analytical factory adds per-job accounting and witness reservations.
No full analytical orchestration, report, I/O or public invocation is implemented.
Only the zero-argument project factory creates a context. Tests patch the fixed
clock symbol outside the product; no caller-supplied clock/limit is accepted.
This is not isolation from malicious same-process mutation or hard real time.
"""
from dataclasses import dataclass, field
from time import monotonic_ns
from ..contracts.execution import (
    _PreparationStop, _PreparationAborted, _AuditCancelled,
    _STRUCTURAL_CODES, _PREPARATION_LIMIT_IDS, _CONSTRAINT_CODES,
    _AnalysisAborted, _ANALYSIS_LIMIT_IDS,
)

from ..validation.limits import _WitnessLedger

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


_JOB_WORK_LIMIT = 1_000_000


@dataclass(slots=True, repr=False, eq=False)
class _AnalyticalJob:
    """Project-owned, current-job port; never accepted from a public caller."""
    _owner: object
    _used: int = field(default=0, init=False)

    @property
    def used(self) -> int:
        return self._used

    def _current(self) -> None:
        if self._owner._job is not self or self._owner._phase != "analysis":
            self._owner.fail()

    def check(self) -> None:
        self._current()
        self._owner.check()

    def check_analysis(self) -> None:
        """An analytical helper cannot run through a finalization-only port."""
        self.check()

    def charge(self, units: int) -> None:
        self._current()
        self._owner.charge(units)

    def interrupt(self, limit_id: str) -> None:
        self._current()
        self._owner.interrupt(limit_id)

    def reject(self, code: str, constraint: str | None = None) -> None:
        self._current()
        self._owner.reject(code, constraint)


@dataclass(slots=True, repr=False, eq=False)
class _BoundedFinalization:
    """Charge/check only: cannot create jobs, change acceptance or add quotas."""
    _owner: object

    def check(self) -> None:
        self._owner._finalization_check(self)

    def charge(self, units: int) -> None:
        self._owner._finalization_charge(self, units)


@dataclass(slots=True, repr=False, eq=False)
class _WitnessJobAccounting:
    """The shared witness quota always charges the currently active job."""
    _owner: object

    def check(self) -> None:
        self._owner.check()
        if self._owner._job is None or self._owner._phase != "analysis":
            self._owner.fail()

    def charge(self, units: int) -> None:
        self.check()
        self._owner.charge(units)

    def interrupt(self, limit_id: str) -> None:
        self.check()
        self._owner.interrupt(limit_id)

    def reject(self, code: str, constraint: str | None = None) -> None:
        self.check()
        self._owner.reject(code, constraint)


@dataclass(slots=True, repr=False, eq=False)
class _AnalysisBudget(_PreparationBudget):
    """One entry-to-finalization ledger, with separate job and delivery ports.

    Admission may use this object through _BudgetPort before acceptance. The
    future orchestrator must finish the structural job plan before recording
    acceptance. W02 supplies accounting primitives, not that orchestration.
    The existing preparation factory continues to construct its original type.
    """
    _phase: str = field(default="admission", init=False)
    _job: object = field(default=None, init=False)
    _finalizer: object = field(default=None, init=False)
    _witness_ledger: object = field(default=None, init=False)
    _stop_kind: str | None = field(default=None, init=False)
    _finalization_blocked: bool = field(default=False, init=False)

    def _clock_check(self) -> None:
        now = self._now()
        if now < self._last:
            self.fail()
        self._last = now
        if now - self._start > _DEADLINE_NS:
            self._stop("time", "WU9-L12")

    def check(self) -> None:
        self._raise_existing()
        if self._phase not in ("admission", "analysis"):
            self.fail()
        self._clock_check()

    def charge(self, units: int) -> None:
        self.check()
        if type(units) is not int or units < 0:
            self.fail()
        if units > _WORK_LIMIT - self._used:
            self._stop("global", "WU9-L11")
        if self._job is not None and units > _JOB_WORK_LIMIT - self._job._used:
            self._stop("job", "WU9-L11")
        self._used += units
        if self._job is not None:
            self._job._used += units

    def _stop(self, kind: str, limit_id: str) -> None:
        if self._phase == "finalization":
            self._finalization_blocked = True
        self._raise_existing()
        self._stop_kind = kind
        self._cause = _AnalysisAborted(
            _PreparationStop(self._state, "interrupted", "resource_limit_reached"), limit_id,
        )
        raise self._cause from None

    def interrupt(self, limit_id: str) -> None:
        self._raise_existing()
        if type(limit_id) is not str or limit_id not in _ANALYSIS_LIMIT_IDS:
            self.fail()
        if limit_id == "WU9-L12":
            kind = "time"
        elif limit_id == "WU9-L13":
            kind = "witness"
        elif limit_id == "WU9-L11":
            kind = "job" if self._job is not None else "global"
        else:
            kind = "admission_resource"
        self._stop(kind, limit_id)

    def fail(self) -> None:
        if self._phase == "finalization":
            self._finalization_blocked = True
        self._raise_existing()
        self._stop_kind = "failure"
        self._cause = _AnalysisAborted(_PreparationStop(self._state, "failed", "execution_failed"))
        raise self._cause from None

    def cancel(self) -> None:
        if self._phase == "finalization":
            self._finalization_blocked = True
        self._raise_existing()
        self._stop_kind = "cancel"
        self._cause = _AuditCancelled(self._state)
        raise self._cause from None

    def reject(self, code: str, constraint: str | None = None) -> None:
        self.check()
        # Structural admission still uses the unchanged preparation transport.
        _PreparationBudget.reject(self, code, constraint)

    def record_input_acceptance(self) -> None:
        _PreparationBudget.record_input_acceptance(self)
        self._phase = "analysis"

    def start_job(self) -> _AnalyticalJob:
        self.check()
        if self._state != "accepted" or self._phase != "analysis" or self._job is not None:
            self.fail()
        self.charge(1)
        job = _AnalyticalJob(self)
        self._job = job
        return job

    def finish_job(self, job: object) -> None:
        self.check()
        if type(job) is not _AnalyticalJob or self._job is not job:
            self.fail()
        job.charge(1)
        self._job = None

    @property
    def witnesses(self) -> _WitnessLedger:
        self.check()
        if self._job is None:
            self.fail()
        if self._witness_ledger is None:
            self.charge(5)
            self._witness_ledger = _WitnessLedger(_WitnessJobAccounting(self))
        return self._witness_ledger

    def begin_finalization(self) -> _BoundedFinalization:
        # Only resource-stopped analysis can finalize earlier committed cells.
        # Governance 22.3 refines cancellation into its separate safe transport.
        if self._cause is not None and self._stop_kind not in ("job", "witness"):
            self._raise_existing()
        if self._phase != "analysis" or self._state != "accepted":
            self.fail()
        if self._cause is None and self._job is not None:
            self.fail()
        self._phase = "finalization"
        self._job = None
        finalizer = _BoundedFinalization(self)
        self._finalizer = finalizer
        self._finalization_charge(finalizer, 1)
        return finalizer

    def take_emergency(self) -> object:
        """The one safe abort is terminal, including any earlier delivery port."""
        cause = _PreparationBudget.take_emergency(self)
        self._finalization_blocked = True
        self._phase = "stopped"
        self._job = None
        return cause

    def _finalization_check(self, port: object) -> None:
        if (type(port) is not _BoundedFinalization or self._finalizer is not port or
                self._phase != "finalization"):
            self.fail()
        if self._finalization_blocked:
            self._raise_existing()
            self.fail()
        if self._cause is not None and self._stop_kind not in ("job", "witness"):
            self._raise_existing()
        self._clock_check()

    def _finalization_charge(self, port: object, units: int) -> None:
        self._finalization_check(port)
        if type(units) is not int or units < 0:
            self.fail()
        if units > _WORK_LIMIT - self._used:
            self._stop("global", "WU9-L11")
        self._used += units


def _new_analysis_budget() -> _AnalysisBudget:
    """Zero-argument project factory; no independent post-preparation reset."""
    return _AnalysisBudget()
