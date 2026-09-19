# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: RUNTIME_BOUNDARY.

Private W04 capture seams, not public ingestion or completed preparation.
Success returns only _CapturedBundle, which has no accepted/pass flag. W05 must
complete all global validation and scope planning before recording acceptance.
No file access, options, callbacks, report, cache or public export is added.
"""
from ..contracts.execution import _PreparationAborted, _AuditCancelled
from ..io.input_file import _decode_utf8
from ..validation.structure import _capture_tree
from ..validation.limits import _InputLedger
from .resources import _new_budget
from .diagnostics import _diagnostic, _emergency_diagnostic


def _capture(value: object, *, supplied_utf8: bool):
    # Mode is a tool-owned constant selected by the two private entry points.
    # The budget and ledger are never supplied by source data or callers.
    budget = None
    try:
        budget = _new_budget()
        mode = "supplied_utf8" if supplied_utf8 else "constructed_value"
        ledger = _InputLedger(budget, mode)
        try:
            result = _decode_utf8(value, ledger) if supplied_utf8 else _capture_tree(value, ledger)
            budget.check()
            return result
        except (_PreparationAborted, _AuditCancelled):
            raise
        except KeyboardInterrupt:
            budget.cancel()
        except Exception:
            budget.fail()
    except (_PreparationAborted, _AuditCancelled) as cause:
        # Return a constant diagnostic, never the raw exception or a partial
        # snapshot. A constructor failure can precede assignment of the budget.
        return _diagnostic(cause) if budget is None else _emergency_diagnostic(budget)


def _prepare_value(value: object):
    """W04: capture an exact built-in root dict; full preparation is pending."""
    return _capture(value, supplied_utf8=False)


def _prepare_utf8(raw: object):
    """W04: capture already supplied exact bytes; no file-open claim."""
    return _capture(raw, supplied_utf8=True)


def _capture_value(value: object):
    """Private capture-only seam retained for W04 component conformance.

    This does not perform W05 dossier validation or establish input acceptance.
    No options, validation bypass, public export or caller budget is introduced.
    """
    return _capture(value, supplied_utf8=False)


def _capture_utf8(raw: object):
    """Private capture of already supplied bytes; no complete-dossier claim."""
    return _capture(raw, supplied_utf8=True)
