# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Synthetic-canary checks on every new private diagnostic surface."""
from dataclasses import fields, FrozenInstanceError
from unittest.mock import patch
import traceback
import pytest
from source_integrity_toolkit.contracts.execution import (
    _PreparationAborted,_PreparationStop,_AuditCancelled,_STRUCTURAL_CODES,
)
from source_integrity_toolkit.runtime.resources import _new_budget
from source_integrity_toolkit.runtime.diagnostics import _diagnostic,_emergency_diagnostic,_SafeDiagnostic
from source_integrity_toolkit.contracts.bundle import _number_from_token,_number_from_builtin,_j_scalar,_string_lengths

MARKER="FICTIONAL_SECRET_NAME_ID_KEY_LOCATOR_METHOD_EXCEPTION_9183"


def visible(record):
    return repr(record)+str(record)+"|".join(str(getattr(record,f.name)) for f in fields(record))


@pytest.mark.parametrize("code", [c for c in _STRUCTURAL_CODES if c != "input_constraint_violation"])
def test_structural_diagnostics_are_fixed_bounded_and_immutable(code):
    budget=_new_budget()
    with pytest.raises(_PreparationAborted) as raised: budget.reject(code)
    record=_emergency_diagnostic(budget)
    assert record.code == code and record.location is None and record.input_state == "rejected"
    assert MARKER not in visible(record) and len(visible(record).encode())<4096
    with pytest.raises(FrozenInstanceError): record.code=MARKER
    with pytest.raises(RuntimeError): _emergency_diagnostic(budget)
    assert str(raised.value) == "input_preparation_stopped"


@pytest.mark.parametrize("constraint", ["exact_integer_range","unicode_scalar","identifier_ascii","identifier_length","string_length","locator_length"])
def test_input_constraint_diagnostic_preserves_specific_fixed_rule_basis(constraint):
    budget=_new_budget()
    with pytest.raises(_PreparationAborted): budget.reject("input_constraint_violation",constraint)
    record=_emergency_diagnostic(budget)
    assert record.code=="input_constraint_violation" and len(record.qualifications)==1
    assert "section" in record.qualifications[0]
    assert record.qualifications[0] != "OBSERVABILITY_AND_REPORTING section 12.2: declared structural diagnostic."


@pytest.mark.parametrize("kind", ["resource","failure","cancel"])
@pytest.mark.parametrize("accepted", [False,True])
def test_distinct_stops_preserve_actual_state_and_no_analytical_payload(kind,accepted):
    b=_new_budget()
    if accepted: b.record_input_acceptance()
    with pytest.raises((_PreparationAborted,_AuditCancelled)):
        if kind=="resource": b.interrupt("WU9-L09")
        elif kind=="cancel": b.cancel()
        else: b.fail()
    diagnostic=_emergency_diagnostic(b)
    assert diagnostic.input_state==("accepted" if accepted else "not_completed")
    assert diagnostic.code == {"resource":"resource_limit_reached","failure":"execution_failed","cancel":None}[kind]
    assert not any(hasattr(diagnostic,key) for key in ("report_kind","results","snapshot","original_exception"))
    assert len(visible(diagnostic).encode())<4096 and MARKER not in visible(diagnostic)


def test_unknown_object_is_not_read_or_coerced_by_diagnostic_dispatch():
    class Poison:
        def __getattribute__(self,name): raise AssertionError("attribute")
        def __str__(self): raise AssertionError("str")
        def __repr__(self): raise AssertionError("repr")
    for value in (Poison(),RuntimeError(MARKER),{"key":MARKER}):
        with pytest.raises(TypeError,match="^unrecognized_private_stop$"): _diagnostic(value)
        with pytest.raises(TypeError,match="^invalid_private_budget$"): _emergency_diagnostic(value)


def test_source_native_failed_and_cancellation_words_are_only_data():
    for word in ("failed","cancelled","resource_limit_reached",MARKER):
        b=_new_budget()
        assert _j_scalar(word,b).decode()=='"'+word+'"'
        assert b.input_state=="not_completed"
        b.check()


def test_malformed_source_canaries_do_not_enter_exception_or_diagnostic(capsys):
    operations=(lambda b:_number_from_token(MARKER,b),
        lambda b:_number_from_builtin(MARKER,b),
        lambda b:_string_lengths(MARKER*2000,b),
        lambda b:_string_lengths(MARKER*100,b,locator=True))
    for operation in operations:
        b=_new_budget()
        with pytest.raises(_PreparationAborted) as raised: operation(b)
        assert MARKER not in str(raised.value)+repr(raised.value)+str(raised.value.args)
        assert MARKER not in visible(_emergency_diagnostic(b))
    assert capsys.readouterr()==("","")


def test_clock_failure_does_not_disclose_original_exception_text():
    def broken_clock(): raise RuntimeError(MARKER)
    with patch("source_integrity_toolkit.runtime.resources.monotonic_ns",broken_clock):
        with pytest.raises(_PreparationAborted) as raised: _new_budget()
    formatted="".join(traceback.format_exception(raised.value))
    assert MARKER not in formatted
    assert raised.value.stop.reason_code=="execution_failed"


@pytest.mark.parametrize("field", ["input_state","execution_state","code","location","safe_message","qualifications"])
def test_constructed_diagnostic_cannot_smuggle_source_values(field):
    values=dict(input_state="not_completed",execution_state="failed",code="execution_failed",
                location=None,safe_message="Input preparation could not complete safely.",qualifications=())
    values[field]=(MARKER,) if field=="qualifications" else MARKER
    with pytest.raises(TypeError,match="^invalid_safe_diagnostic$"): _SafeDiagnostic(**values)


def test_invalid_internal_stop_metadata_does_not_become_source_rejection():
    for code,constraint in ((MARKER,None),("input_constraint_violation",MARKER),("input_constraint_violation",None)):
        b=_new_budget()
        with pytest.raises(_PreparationAborted) as raised: b.reject(code,constraint)
        assert raised.value.stop.reason_code=="execution_failed"
        assert MARKER not in visible(_diagnostic(raised.value))
