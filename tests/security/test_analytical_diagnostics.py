# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""P3-W02 safe analytical stop transport with fictional privacy canaries.

Authority: PRIVACY_AND_DATA_HANDLING 6.1, 8.3; architecture 19.2-19.3;
GOVERNANCE_AND_HANDOFF 22.3; PHASE_3_PLAN 3.4 and 7. Cancellation remains
separate from resource/failure reasons. No public reports or CLI are invoked.
Ordinary formatted tracebacks are checked; hostile debugger/local inspection
and memory zeroization remain outside the adopted protection claim.
"""
from dataclasses import fields, FrozenInstanceError
import traceback

import pytest

from source_integrity_toolkit.contracts.execution import (
    _AnalysisAborted, _AuditCancelled, _PreparationAborted,
)
from source_integrity_toolkit.runtime import resources, diagnostics


CANARY = "FICTIONAL_ANALYTICAL_ID_PATH_CREDENTIAL_EXCEPTION_7491"


@pytest.fixture
def clock(monkeypatch):
    now = [100]
    monkeypatch.setattr(resources, "monotonic_ns", lambda: now[0])
    return now


def visible(record):
    return repr(record) + str(record) + "|".join(str(getattr(record, item.name)) for item in fields(record))


def safe_transport(cause):
    surface = str(cause) + repr(cause) + str(cause.args) + "".join(traceback.format_exception(cause))
    assert CANARY not in surface
    assert not any(hasattr(cause, name) for name in ("snapshot", "results", "report", "original_exception", "source", "payload"))


@pytest.mark.parametrize("accepted", (False, True))
@pytest.mark.parametrize("kind", ("resource", "failure", "cancel"))
def test_every_stop_preserves_actual_input_state_and_safe_distinct_outcome(clock, accepted, kind, capsys):
    budget = resources._new_analysis_budget()
    if accepted:
        budget.record_input_acceptance()  # Trusted component setup, not actual admission.
    expected_exception = _AuditCancelled if kind == "cancel" else _AnalysisAborted
    with pytest.raises(expected_exception) as stopped:
        if kind == "resource":
            budget.charge(9_998_977)
        elif kind == "failure":
            budget.fail()
        else:
            budget.cancel()
    state = "accepted" if accepted else "not_completed"
    record = diagnostics._emergency_analytical_diagnostic(budget)
    assert type(record) is diagnostics._AnalyticalDiagnostic
    assert record.input_state == state
    assert record.execution_state == {"resource": "interrupted", "failure": "failed", "cancel": "cancelled"}[kind]
    assert record.code == {"resource": "resource_limit_reached", "failure": "execution_failed", "cancel": None}[kind]
    assert record.location is None
    assert CANARY not in visible(record) and len(visible(record).encode()) < 4096
    assert not any(hasattr(record, name) for name in ("report_kind", "results", "snapshot", "original_exception"))
    if kind == "cancel":
        assert stopped.value.input_state == state
        assert not hasattr(stopped.value, "reason_code") and not hasattr(stopped.value, "limit_id")
    else:
        assert stopped.value.stop.input_state == state
    safe_transport(stopped.value)
    with pytest.raises(FrozenInstanceError):
        record.code = CANARY
    before = budget.used
    with pytest.raises(RuntimeError, match="^emergency_delivery_already_used$"):
        diagnostics._emergency_analytical_diagnostic(budget)
    assert budget.used == before
    assert capsys.readouterr() == ("", "")


@pytest.mark.parametrize("accepted", (False, True))
def test_keyboard_interrupt_is_payload_free_cancellation_with_actual_state(clock, monkeypatch, accepted):
    budget = resources._new_analysis_budget()
    if accepted:
        budget.record_input_acceptance()
    def cancelled_clock():
        raise KeyboardInterrupt(CANARY)
    monkeypatch.setattr(resources, "monotonic_ns", cancelled_clock)
    with pytest.raises(_AuditCancelled) as stopped:
        budget.check()
    safe_transport(stopped.value)
    diagnostic = diagnostics._emergency_analytical_diagnostic(budget)
    assert diagnostic.input_state == ("accepted" if accepted else "not_completed")
    assert diagnostic.execution_state == "cancelled" and diagnostic.code is None
    assert CANARY not in visible(diagnostic)
    with pytest.raises(_AuditCancelled) as finalization:
        budget.begin_finalization()
    assert finalization.value is stopped.value


@pytest.mark.parametrize("accepted", (False, True))
def test_clock_fault_exception_text_and_repr_never_enter_stop_or_diagnostic(clock, monkeypatch, accepted, capsys):
    budget = resources._new_analysis_budget()
    if accepted:
        budget.record_input_acceptance()
    touched = []
    class SecretFault(Exception):
        def __str__(self):
            touched.append("str")
            raise AssertionError("unexpected_fault_formatting")
        def __repr__(self):
            touched.append("repr")
            raise AssertionError("unexpected_fault_formatting")
    def broken_clock():
        raise SecretFault(CANARY)
    monkeypatch.setattr(resources, "monotonic_ns", broken_clock)
    with pytest.raises(_AnalysisAborted) as stopped:
        budget.check()
    assert stopped.value.stop.reason_code == "execution_failed"
    safe_transport(stopped.value)
    record = diagnostics._emergency_analytical_diagnostic(budget)
    assert record.input_state == ("accepted" if accepted else "not_completed")
    assert record.execution_state == "failed" and record.code == "execution_failed"
    assert CANARY not in visible(record) and touched == []
    assert capsys.readouterr() == ("", "")


@pytest.mark.parametrize("kind", ("failure", "cancel"))
def test_constructor_clock_fault_is_safe_even_before_context_returns(monkeypatch, kind):
    def broken_clock():
        if kind == "cancel":
            raise KeyboardInterrupt(CANARY)
        raise RuntimeError(CANARY)
    monkeypatch.setattr(resources, "monotonic_ns", broken_clock)
    expected = _AuditCancelled if kind == "cancel" else _AnalysisAborted
    with pytest.raises(expected) as stopped:
        resources._new_analysis_budget()
    safe_transport(stopped.value)
    record = diagnostics._analytical_diagnostic(stopped.value)
    assert record.input_state == "not_completed"
    assert record.code == (None if kind == "cancel" else "execution_failed")
    assert CANARY not in visible(record)


@pytest.mark.parametrize("first", ("job", "witness", "global", "deadline", "failure", "cancel"))
def test_first_established_cause_is_sticky_across_later_stop_methods(clock, first):
    budget = resources._new_analysis_budget()
    budget.record_input_acceptance()
    job = budget.start_job()
    expected = _AuditCancelled if first == "cancel" else _AnalysisAborted
    with pytest.raises(expected) as original:
        if first == "job":
            job.charge(1_000_001)
        elif first == "witness":
            budget.witnesses.reserve(witnesses=20_001)
        elif first == "global":
            job.charge(10_000_001)
        elif first == "deadline":
            clock[0] += 60_000_000_001
            job.check()
        elif first == "failure":
            budget.fail()
        else:
            budget.cancel()
    used = budget.used
    for action in (budget.cancel, budget.fail, job.check, lambda: job.charge(0), budget.start_job):
        with pytest.raises(expected) as repeat:
            action()
        assert repeat.value is original.value
    assert budget.used == used
    safe_transport(original.value)
    assert budget.take_emergency() is original.value


@pytest.mark.parametrize("first", ("failure", "cancel"))
def test_failure_and_cancellation_never_open_an_ordinary_salvage_path(clock, first):
    budget = resources._new_analysis_budget()
    budget.record_input_acceptance()
    job = budget.start_job()
    job.charge(3)
    expected = _AuditCancelled if first == "cancel" else _AnalysisAborted
    with pytest.raises(expected) as original:
        (budget.cancel if first == "cancel" else budget.fail)()
    for action in (budget.begin_finalization, budget.start_job, lambda: job.charge(1)):
        with pytest.raises(expected) as refused:
            action()
        assert refused.value is original.value
    record = diagnostics._emergency_analytical_diagnostic(budget)
    assert record.input_state == "accepted"
    assert record.execution_state == ("cancelled" if first == "cancel" else "failed")
    assert not hasattr(record, "results")


def test_unknown_diagnostic_objects_are_refused_before_any_source_protocol(clock):
    touched = []
    class Poison:
        def __getattribute__(self, name):
            touched.append(name)
            raise AssertionError("unexpected_attribute")
        def __str__(self):
            touched.append("str")
            raise AssertionError("unexpected_str")
        def __repr__(self):
            touched.append("repr")
            raise AssertionError("unexpected_repr")
    for value in (Poison(), RuntimeError(CANARY), {"reason": CANARY}, resources._new_budget()):
        with pytest.raises(TypeError):
            diagnostics._analytical_diagnostic(value)
        with pytest.raises(TypeError):
            diagnostics._emergency_analytical_diagnostic(value)
    assert touched == []


@pytest.mark.parametrize("field", ("input_state", "execution_state", "code", "location", "safe_message", "qualifications"))
def test_direct_diagnostic_construction_cannot_smuggle_incidental_source_values(field):
    values = dict(input_state="accepted", execution_state="failed", code="execution_failed", location=None,
                  safe_message="Processing could not complete safely.", qualifications=())
    baseline = diagnostics._AnalyticalDiagnostic(**values)
    assert baseline.input_state == "accepted"
    values[field] = (CANARY,) if field == "qualifications" else CANARY
    with pytest.raises(TypeError) as refused:
        diagnostics._AnalyticalDiagnostic(**values)
    assert CANARY not in str(refused.value) + repr(refused.value) + str(refused.value.args)


def test_new_transport_does_not_relabel_structural_preparation_rejection(clock):
    budget = resources._new_analysis_budget()
    with pytest.raises(_PreparationAborted) as stopped:
        budget.reject("invalid_syntax")
    record = diagnostics._analytical_diagnostic(stopped.value)
    assert type(record) is diagnostics._SafeDiagnostic
    assert (record.input_state, record.execution_state, record.code) == ("rejected", "rejected", "invalid_syntax")
    assert not isinstance(stopped.value, _AnalysisAborted)


def test_unknown_limit_id_cannot_become_source_selected_reason_or_diagnostic(clock):
    budget = resources._new_analysis_budget()
    budget.record_input_acceptance()
    job = budget.start_job()
    with pytest.raises(_AnalysisAborted) as stopped:
        job.interrupt(CANARY)
    assert stopped.value.stop.reason_code == "execution_failed"
    safe_transport(stopped.value)
    record = diagnostics._emergency_analytical_diagnostic(budget)
    assert record.code == "execution_failed" and CANARY not in visible(record)
