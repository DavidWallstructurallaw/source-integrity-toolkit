# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: RUNTIME_BOUNDARY.

Private capture components and full bounded W05 preparation. The capture
components retain their noncertifying result. Preparation records acceptance
only after complete structural/reference/time/index/scope checks. No public
auditing, file access, options, callbacks, report or persistent cache is added.
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
    """Private full preparation of an exact built-in root dict."""
    return _prepare(value, supplied_utf8=False)


def _prepare_utf8(raw: object):
    """Private full preparation of supplied bytes; no file-open claim."""
    return _prepare(raw, supplied_utf8=True)


def _capture_value(value: object):
    """Private capture-only seam retained for W04 component conformance.

    This does not perform W05 dossier validation or establish input acceptance.
    No options, validation bypass, public export or caller budget is introduced.
    """
    return _capture(value, supplied_utf8=False)


def _capture_utf8(raw: object):
    """Private capture of already supplied bytes; no complete-dossier claim."""
    return _capture(raw, supplied_utf8=True)


from ..contracts.evidence import _PreparedBundle
from ..validation.structure import _validate_structure, _shape_walk, _local_rules, _validate_gaps
from ..validation.references import _validate_references, _normalize, _index, _check_links, _scope_plan
from ..validation.semantics import _validate_semantics


def _prepare(value: object, *, supplied_utf8: bool):
    """One nonresetting budget; no partial snapshot on any stopping path."""
    budget = None
    try:
        budget = _new_budget()
        mode = "supplied_utf8" if supplied_utf8 else "constructed_value"
        ledger = _InputLedger(budget, mode)
        try:
            captured = _decode_utf8(value, ledger) if supplied_utf8 else _capture_tree(value, ledger)
            occurrences = _validate_structure(captured, ledger)
            entities = _validate_references(captured, occurrences, budget)
            _validate_semantics(occurrences, budget)
            normalized = _normalize(captured.tree, entities, budget)
            # A second paid pass addresses normalized selectors. It never counts
            # the same payload twice against input-size/occurrence ceilings.
            final_occurrences = _shape_walk(normalized, ledger, count=False)
            _local_rules(final_occurrences, budget)
            _validate_gaps(final_occurrences, budget)
            final_entities = _index(normalized, budget)
            links = _check_links(final_occurrences, final_entities, budget, retain=True)
            observations = _validate_semantics(final_occurrences, budget)
            plan = _scope_plan(final_entities, budget)
            budget.charge(len(final_entities) + len(links) + len(plan) + len(observations) + 10)
            result = _PreparedBundle(normalized, mode, final_entities, links, plan, observations, captured.tree)
            budget.record_input_acceptance()
            budget.check()
            return result
        except (_PreparationAborted, _AuditCancelled):
            raise
        except KeyboardInterrupt:
            budget.cancel()
        except Exception:
            budget.fail()
    except (_PreparationAborted, _AuditCancelled) as cause:
        return _diagnostic(cause) if budget is None else _emergency_diagnostic(budget)
