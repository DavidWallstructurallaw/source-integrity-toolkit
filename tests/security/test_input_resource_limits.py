# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Preparation ledger thresholds, not parser/analytical/native certification."""
from unittest.mock import patch
import pytest
from source_integrity_toolkit.runtime.resources import _new_budget
from source_integrity_toolkit.contracts.execution import _PreparationAborted, _AuditCancelled
from source_integrity_toolkit.validation.limits import _InputLedger, _AGGREGATES, _DEFERRED
from source_integrity_toolkit.contracts.bundle import _string_lengths, _number_from_token


@pytest.mark.parametrize("name,ceiling,limit", [
    ("bytes",16777216,"WU9-L01"),("inquiries",32,"WU9-L03"),
    ("records",10000,"WU9-L04"),("assertions",30000,"WU9-L05"),
    ("evidence_references",10000,"WU9-L06"),("reference_occurrences",200000,"WU9-L07"),
    ("nodes",500000,"WU9-L08"),
])
@pytest.mark.parametrize("mode", ["supplied_utf8","constructed_value"])
def test_each_aggregate_below_at_above_without_constructing_fake_input(name,ceiling,limit,mode):
    budget=_new_budget(); ledger=_InputLedger(budget,mode)
    ledger.add(name,ceiling-1)
    ledger.add(name,1)
    before=ledger.snapshot()
    with pytest.raises(_PreparationAborted) as raised:
        ledger.add(name,1)
    assert raised.value.limit_id == limit
    assert raised.value.stop.input_state == "not_completed"
    assert tuple(ledger._counts)+(ledger._peak_depth,) == before
    with pytest.raises(_PreparationAborted) as again:
        ledger.add(name,0)
    assert again.value is raised.value


def test_depth_is_a_nonresetting_peak_not_the_count_of_all_containers():
    budget=_new_budget(); ledger=_InputLedger(budget,"constructed_value")
    for level in (1,31,32,2): ledger.depth(level)
    assert ledger.snapshot()[-1] == 32
    with pytest.raises(_PreparationAborted) as raised: ledger.depth(33)
    assert raised.value.limit_id == "WU9-L02" and ledger._peak_depth == 32


@pytest.mark.parametrize("kwargs,limit", [({},65536),({"locator":True},4096),({"identifier":True},128)])
def test_field_byte_lengths_have_structural_below_at_above_rules(kwargs,limit):
    for length in (limit-1,limit):
        assert _string_lengths("a"*length,_new_budget(),**kwargs) == (length,length+2)
    with pytest.raises(_PreparationAborted) as raised:
        _string_lengths("a"*(limit+1),_new_budget(),**kwargs)
    assert raised.value.diagnostic_code == "input_constraint_violation"
    assert raised.value.stop.execution_state == "rejected"


def test_decoded_multibyte_string_count_differs_from_j_escape_count():
    assert _string_lengths("é"*32768,_new_budget()) == (65536,65538)
    assert _string_lengths("\x00"*65536,_new_budget()) == (65536,393218)
    with pytest.raises(_PreparationAborted): _string_lengths("😀"*16385,_new_budget())
    with pytest.raises(_PreparationAborted) as raised:
        _string_lengths("é",_new_budget(),identifier=True)
    assert raised.value.constraint == "identifier_ascii"


def test_reserve_is_inside_total_and_never_refunded_or_recreated():
    with patch("source_integrity_toolkit.runtime.resources.monotonic_ns",return_value=0):
        b=_new_budget()
        assert b.used == 1024 and b.remaining == 9998976
        b.charge(b.remaining)
        assert b.used == 10000000 and b.remaining == 0
        b.check()
        with pytest.raises(_PreparationAborted) as raised: b.charge(1)
        assert raised.value.limit_id == "WU9-L11" and b.used == 10000000
        assert b.take_emergency() is raised.value
        assert b.used == 10000000
        with pytest.raises(RuntimeError,match="^emergency_delivery_already_used$"): b.take_emergency()
        with pytest.raises(_PreparationAborted): b.charge(0)


@pytest.mark.parametrize("units", [-1,True,False,1.0,"1",None])
def test_invalid_or_negative_charges_cannot_lower_accounting(units):
    b=_new_budget(); prior=b.used
    with pytest.raises(_PreparationAborted) as raised: b.charge(units)
    assert raised.value.stop.reason_code == "execution_failed" and b.used == prior


def test_fixed_budget_factory_has_no_source_options_or_environment_overrides(monkeypatch):
    monkeypatch.setenv("SIT_MAX_WORK","999999999")
    monkeypatch.setenv("SIT_TIMEOUT","0")
    b=_new_budget()
    assert b.remaining == 9998976
    for kwargs in ({"limit":1},{"clock":lambda:0},{"options":{}},{"deadline":1}):
        with pytest.raises(TypeError): _new_budget(**kwargs)


def test_monotonic_deadline_equality_and_no_reset_on_work():
    now=[-100]
    with patch("source_integrity_toolkit.runtime.resources.monotonic_ns",lambda:now[0]):
        b=_new_budget()
        now[0]+=59_999_999_999; b.charge(1)
        now[0]+=1; b.check()
        now[0]+=1
        with pytest.raises(_PreparationAborted) as raised: b.check()
        assert raised.value.limit_id == "WU9-L12"
        assert b.used == 1025


def test_backward_clock_is_failure_and_keyboard_interrupt_is_cancellation():
    with patch("source_integrity_toolkit.runtime.resources.monotonic_ns",side_effect=[100,99]):
        b=_new_budget()
        with pytest.raises(_PreparationAborted) as raised: b.check()
        assert raised.value.stop.reason_code == "execution_failed"
    with patch("source_integrity_toolkit.runtime.resources.monotonic_ns",side_effect=[0,KeyboardInterrupt()]):
        b=_new_budget()
        with pytest.raises(_AuditCancelled) as raised: b.check()
        assert raised.value.input_state == "not_completed"


@pytest.mark.parametrize("first", ["resource","cancel","failure","rejection"])
def test_first_established_stop_is_sticky(first):
    b=_new_budget()
    with pytest.raises((_PreparationAborted,_AuditCancelled)) as original:
        if first == "resource": b.interrupt("WU9-L01")
        elif first == "cancel": b.cancel()
        elif first == "failure": b.fail()
        else: b.reject("invalid_syntax")
    used=b.used
    for action in (b.cancel,b.fail,lambda:b.interrupt("WU9-L11"),lambda:b.charge(1)):
        with pytest.raises((_PreparationAborted,_AuditCancelled)) as repeat: action()
        assert repeat.value is original.value
    assert b.used == used


def test_state_recording_does_not_validate_or_publish_a_snapshot():
    b=_new_budget()
    b.record_input_acceptance()  # a trusted simulated later boundary, not PC01
    with pytest.raises(_PreparationAborted) as raised: b.interrupt("WU9-L11")
    assert raised.value.stop.input_state == "accepted"
    assert not hasattr(raised.value,"snapshot") and not hasattr(raised.value,"results")
    b=_new_budget(); b.record_input_acceptance()
    with pytest.raises(_AuditCancelled) as raised: b.cancel()
    assert raised.value.input_state == "accepted" and not hasattr(raised.value,"reason_code")


def test_later_limits_remain_recorded_without_implemented_operations():
    assert _AGGREGATES == (("bytes",16777216,"WU9-L01"),("inquiries",32,"WU9-L03"),
        ("records",10000,"WU9-L04"),("assertions",30000,"WU9-L05"),
        ("evidence_references",10000,"WU9-L06"),("reference_occurrences",200000,"WU9-L07"),
        ("nodes",500000,"WU9-L08"))
    assert _DEFERRED == (("analytical_scope_work",1000000,"WU9-L11"),
        ("witnesses",20000,"WU9-L13"),("witness_members",100000,"WU9-L13"),
        ("report_representation_bytes",67108864,"WU9-L14"))
    ledger=_InputLedger(_new_budget(),"supplied_utf8")
    for name,_,_ in _DEFERRED:
        with pytest.raises(TypeError,match="^invalid_private_counter$"): ledger.add(name)


def test_all_copies_and_repeated_scalar_calls_consume_work():
    b=_new_budget(); before=b.used
    _number_from_token("1.2500",b); first=b.used-before
    _number_from_token("1.2500",b)
    assert first>1 and b.used-before == first*2
