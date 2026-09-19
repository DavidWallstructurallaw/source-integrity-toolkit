# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: RUNTIME_BOUNDARY. Fixed private input-stop records only.

No arbitrary source, key, ID, exception, locator or method string is accepted.
No report envelope, logging, rendering, serialization or I/O is implemented.
One emergency record consumes the prepaid reserve without restarting work.
Traceback locals and hostile debugger/same-process access are outside the claim.
"""
from dataclasses import dataclass
from ..contracts.execution import (
    _PreparationAborted, _AuditCancelled, _STRUCTURAL_CODES,
    _PREPARATION_LIMIT_IDS,
)
from .resources import _PreparationBudget

_CONSTRAINT_BASIS = (
    ("exact_integer_range", "PRIVACY_AND_DATA_HANDLING section 8.2: exact integer magnitude."),
    ("unicode_scalar", "REPOSITORY_ARCHITECTURE section 17.2: valid Unicode scalar values."),
    ("identifier_ascii", "PRIVACY_AND_DATA_HANDLING section 8.1 WU9-L09: ASCII identifiers."),
    ("identifier_length", "PRIVACY_AND_DATA_HANDLING section 8.1 WU9-L09: identifier byte length."),
    ("string_length", "PRIVACY_AND_DATA_HANDLING section 8.1 WU9-L10: decoded string/key byte length."),
    ("locator_length", "PRIVACY_AND_DATA_HANDLING section 8.1 WU9-L10: decoded locator byte length."),
)
_STRUCTURAL_BASIS = "OBSERVABILITY_AND_REPORTING section 12.2: declared structural diagnostic."
_CANCEL_BASIS = "GOVERNANCE_AND_HANDOFF section 22.3: private cancellation transport."


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _SafeDiagnostic:
    input_state: str
    execution_state: str
    code: str | None
    location: None
    safe_message: str
    qualifications: tuple

    def __post_init__(self) -> None:
        if type(self.input_state) is not str or self.input_state not in ("accepted", "rejected", "not_completed"):
            raise TypeError("invalid_safe_diagnostic")
        if self.location is not None or type(self.qualifications) is not tuple or len(self.qualifications) > 1:
            raise TypeError("invalid_safe_diagnostic")
        if any(type(q) is not str or len(q) > 160 for q in self.qualifications):
            raise TypeError("invalid_safe_diagnostic")
        if type(self.execution_state) is not str or type(self.safe_message) is not str or (self.code is not None and type(self.code) is not str):
            raise TypeError("invalid_safe_diagnostic")
        allowed = False
        if self.execution_state == "rejected" and self.input_state == "rejected":
            basis_ok = self.qualifications == (_STRUCTURAL_BASIS,)
            if self.code == "input_constraint_violation":
                basis_ok = any(self.qualifications == (row[1],) for row in _CONSTRAINT_BASIS)
            allowed = self.code in _STRUCTURAL_CODES and self.safe_message == "Input violates a declared structural constraint." and basis_ok
        elif self.execution_state == "interrupted" and self.input_state in ("accepted", "not_completed"):
            allowed = (self.code == "resource_limit_reached" and self.safe_message == "Input preparation stopped at a resource boundary." and
                       len(self.qualifications) == 1 and self.qualifications[0] in _PREPARATION_LIMIT_IDS)
        elif self.execution_state == "failed" and self.input_state in ("accepted", "not_completed"):
            allowed = self.code == "execution_failed" and self.safe_message == "Input preparation could not complete safely." and self.qualifications == ()
        elif self.execution_state == "cancelled" and self.input_state in ("accepted", "not_completed"):
            allowed = self.code is None and self.safe_message == "Input preparation was cancelled." and self.qualifications == (_CANCEL_BASIS,)
        if not allowed:
            raise TypeError("invalid_safe_diagnostic")


def _diagnostic(cause: object) -> _SafeDiagnostic:
    """Unknown objects are refused before repr, str, fields or type-name access."""
    if type(cause) is _AuditCancelled:
        return _SafeDiagnostic(cause.input_state, "cancelled", None, None,
            "Input preparation was cancelled.", (_CANCEL_BASIS,))
    if type(cause) is not _PreparationAborted:
        raise TypeError("unrecognized_private_stop") from None
    stop = cause.stop
    if stop.execution_state == "rejected":
        basis = _STRUCTURAL_BASIS
        if cause.diagnostic_code == "input_constraint_violation":
            for code, text in _CONSTRAINT_BASIS:
                if code == cause.constraint:
                    basis = text
                    break
        return _SafeDiagnostic("rejected", "rejected", cause.diagnostic_code, None,
            "Input violates a declared structural constraint.", (basis,))
    if stop.execution_state == "interrupted":
        return _SafeDiagnostic(stop.input_state, "interrupted", "resource_limit_reached", None,
            "Input preparation stopped at a resource boundary.", (cause.limit_id,))
    return _SafeDiagnostic(stop.input_state, "failed", "execution_failed", None,
        "Input preparation could not complete safely.", ())


def _emergency_diagnostic(budget: object) -> _SafeDiagnostic:
    """One bounded diagnostic from the actual stopped project context."""
    if type(budget) is not _PreparationBudget:
        raise TypeError("invalid_private_budget") from None
    return _diagnostic(budget.take_emergency())
