# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""P3-W02 execution primitives, with independent source-bound limit oracles.

Authority: PRIVACY_AND_DATA_HANDLING 8.1 WU9-L11-L13; architecture 19.1-19.3;
governance 22.3; PHASE_3_PLAN 3.4 and 7. Literal thresholds below come from
those specifications. Private test clock patching grants no caller authority.
These are component checks, not complete W13 orchestration/report execution.
"""
import inspect
import copy

import pytest

from source_integrity_toolkit.contracts.execution import _AnalysisAborted, _AuditCancelled, _byte_work
from source_integrity_toolkit.runtime import resources


@pytest.fixture
def clock(monkeypatch):
    now = [100]
    monkeypatch.setattr(resources, "monotonic_ns", lambda: now[0])
    return now


def accepted_job():
    budget = resources._new_analysis_budget()
    budget.record_input_acceptance()  # Trusted component fact; no claim PC01 ran.
    return budget, budget.start_job()


def test_one_reserved_emergency_is_inside_fixed_invocation_limit(clock, monkeypatch):
    monkeypatch.setenv("SIT_MAX_WORK", "999999999999")
    monkeypatch.setenv("SIT_TIMEOUT", "999999")
    budget = resources._new_analysis_budget()
    assert budget.used == 1024 and budget.remaining == 9_998_976
    assert budget.input_state == "not_completed"
    assert not inspect.signature(resources._new_analysis_budget).parameters
    for key in ("limit", "clock", "deadline", "options", "callback"):
        with pytest.raises(TypeError):
            resources._new_analysis_budget(**{key: lambda: 0})


def test_job_and_global_ledgers_debit_once_including_zero_charges(clock):
    budget, job = accepted_job()
    assert budget.used == 1025 and job.used == 0
    job.charge(7)
    assert (budget.used, job.used) == (1032, 7)
    budget.charge(3)  # A current-job helper cannot hide work in a global-only call.
    assert (budget.used, job.used) == (1035, 10)
    job.charge(0)
    assert (budget.used, job.used) == (1035, 10)
    _byte_work(job, 257, visits=2)  # Two visits and two started 256-byte blocks.
    assert (budget.used, job.used) == (1039, 14)
    _byte_work(job, 257, visits=2)
    assert (budget.used, job.used) == (1043, 18)


def test_per_job_below_equal_above_is_prospective_and_stops_all_further_analysis(clock):
    budget, job = accepted_job()
    job.charge(999_999)
    assert job.used == 999_999
    job.charge(1)
    assert (job.used, budget.used) == (1_000_000, 1_001_025)
    with pytest.raises(_AnalysisAborted) as stopped:
        job.charge(1)
    assert stopped.value.limit_id == "WU9-L11"
    assert stopped.value.stop.input_state == "accepted"
    assert (job.used, budget.used) == (1_000_000, 1_001_025)
    for action in (job.check, lambda: job.charge(0), budget.start_job, lambda: budget.charge(0)):
        with pytest.raises(_AnalysisAborted) as repeat:
            action()
        assert repeat.value is stopped.value


@pytest.mark.parametrize("value", (-1, True, False, 1.0, "1", None))
def test_invalid_job_units_fail_without_refund_or_count_coercion(clock, value):
    budget, job = accepted_job()
    job.charge(11)
    before = (budget.used, job.used)
    with pytest.raises(_AnalysisAborted) as stopped:
        job.charge(value)
    assert stopped.value.stop.reason_code == "execution_failed"
    assert (budget.used, job.used) == before


def test_integer_protocol_is_not_used_to_turn_source_objects_into_work_units(clock):
    called = []
    class Hostile:
        def __index__(self):
            called.append("index")
            return 1
        def __int__(self):
            called.append("int")
            return 1
    budget, job = accepted_job()
    with pytest.raises(_AnalysisAborted) as stopped:
        job.charge(Hostile())
    assert stopped.value.stop.reason_code == "execution_failed"
    assert called == [] and (budget.used, job.used) == (1025, 0)


def test_global_limit_includes_preparation_and_current_job_without_new_reserve(clock):
    budget = resources._new_analysis_budget()
    budget.charge(9_998_974)  # Leaves two units, including next port allocation.
    budget.record_input_acceptance()
    job = budget.start_job()
    assert budget.used == 9_999_999 and job.used == 0
    job.charge(1)
    assert (budget.used, job.used, budget.remaining) == (10_000_000, 1, 0)
    with pytest.raises(_AnalysisAborted) as stopped:
        job.charge(1)
    assert stopped.value.limit_id == "WU9-L11"
    assert (budget.used, job.used) == (10_000_000, 1)
    with pytest.raises(_AnalysisAborted) as finalization:
        budget.begin_finalization()
    assert finalization.value is stopped.value
    assert budget.take_emergency() is stopped.value
    assert budget.used == 10_000_000
    with pytest.raises(RuntimeError, match="^emergency_delivery_already_used$"):
        budget.take_emergency()


def test_successive_jobs_keep_global_work_and_each_get_the_declared_local_counter(clock):
    budget, first = accepted_job()
    first.charge(41)
    budget.finish_job(first)
    assert first.used == 42 and budget.used == 1067
    second = budget.start_job()
    assert second.used == 0 and budget.used == 1068
    second.charge(999_999)
    budget.finish_job(second)
    assert second.used == 1_000_000 and budget.used == 1_001_068
    third = budget.start_job()
    assert third.used == 0 and budget.used == 1_001_069
    with pytest.raises(_AnalysisAborted) as stopped:
        first.charge(1)
    assert stopped.value.stop.reason_code == "execution_failed"


def test_per_job_stop_allows_only_paid_bounded_finalization_not_analysis_resumption(clock):
    budget, job = accepted_job()
    job.charge(1_000_000)
    with pytest.raises(_AnalysisAborted) as stopped:
        job.charge(1)
    before = budget.used
    final = budget.begin_finalization()
    assert budget.used == before + 1
    final.charge(7)
    final.check()
    assert budget.used == before + 8 and job.used == 1_000_000
    for action in (lambda: job.charge(1), budget.start_job, lambda: budget.charge(1), budget.begin_finalization):
        with pytest.raises(_AnalysisAborted) as repeat:
            action()
        assert repeat.value is stopped.value
    assert budget.take_emergency() is stopped.value
    assert budget.used == before + 8


@pytest.mark.parametrize("boundary", ("global", "time"))
def test_finalization_cannot_reset_global_or_deadline_and_keeps_first_cause(clock, boundary):
    budget, job = accepted_job()
    job.charge(1_000_000)
    with pytest.raises(_AnalysisAborted) as original:
        job.charge(1)
    final = budget.begin_finalization()
    if boundary == "global":
        final.charge(8_998_974)
        assert budget.used == 10_000_000
        action = lambda: final.charge(1)
    else:
        clock[0] += 60_000_000_001
        action = final.check
    with pytest.raises(_AnalysisAborted) as stopped:
        action()
    assert stopped.value is original.value
    with pytest.raises(_AnalysisAborted) as repeated:
        final.charge(0)
    assert repeated.value is original.value
    assert budget.take_emergency() is original.value


def test_sixty_second_deadline_does_not_restart_on_new_job_or_finalization(clock):
    budget, first = accepted_job()
    clock[0] += 59_999_999_999
    first.charge(1)
    budget.finish_job(first)
    second = budget.start_job()
    clock[0] += 1
    second.check()  # Equality is allowed.
    clock[0] += 1
    before = (budget.used, second.used)
    with pytest.raises(_AnalysisAborted) as stopped:
        second.charge(0)
    assert stopped.value.limit_id == "WU9-L12"
    assert (budget.used, second.used) == before
    with pytest.raises(_AnalysisAborted) as finalization:
        budget.begin_finalization()
    assert finalization.value is stopped.value


@pytest.mark.parametrize("bad", (True, False, None, 1.5, "100"))
def test_noninteger_clock_is_execution_failure_without_coercion(clock, bad):
    budget, job = accepted_job()
    before = (budget.used, job.used)
    clock[0] = bad
    with pytest.raises(_AnalysisAborted) as stopped:
        job.charge(1)
    assert stopped.value.stop.reason_code == "execution_failed"
    assert stopped.value.stop.input_state == "accepted"
    assert (budget.used, job.used) == before


def test_backward_clock_is_failure_without_refreshing_deadline(clock):
    budget, job = accepted_job()
    clock[0] = 99
    with pytest.raises(_AnalysisAborted) as stopped:
        job.check()
    assert stopped.value.stop.reason_code == "execution_failed"
    assert budget.used == 1025 and job.used == 0


def test_ports_do_not_offer_clock_limits_restart_or_job_factory_authority(clock):
    budget, job = accepted_job()
    budget.finish_job(job)
    final = budget.begin_finalization()
    for port in (job, final):
        for name in ("clock", "deadline", "limits", "options", "callback", "start_job", "begin_finalization",
                     "record_input_acceptance", "take_emergency", "reset", "refund", "restart"):
            assert not hasattr(port, name), name
        for kwargs in ({"clock": lambda: 0}, {"limit": 2_000_000}, {"options": {}}):
            with pytest.raises(TypeError):
                port.charge(1, **kwargs)
    assert not hasattr(job, "__dict__") and not hasattr(final, "__dict__")


def retained_counts(ledger):
    """Test-only observation after stop; no stopped product operation resumes."""
    return (ledger._reserved_witnesses, ledger._reserved_members,
            ledger._retained_witnesses, ledger._retained_members)


def test_witness_bookkeeping_and_emission_charge_each_occurrence_once(clock):
    budget, job = accepted_job()
    ledger = budget.witnesses
    assert budget.used == 1030 and job.used == 5  # One five-slot ledger allocation.
    assert ledger.snapshot() == (0, 0, 0, 0)
    assert budget.used == 1035 and job.used == 10
    token = ledger.reserve(witnesses=1, members=2)
    assert retained_counts(ledger) == (1, 2, 0, 0)
    assert (budget.used, job.used) == (1039, 14)
    ledger.retain(token)  # One state transition and each of three emitted entries.
    assert retained_counts(ledger) == (0, 0, 1, 2)
    assert (budget.used, job.used) == (1043, 18)
    assert budget.witnesses is ledger and (budget.used, job.used) == (1043, 18)


@pytest.mark.parametrize("dimension,ceiling", (("witnesses", 20_000), ("members", 100_000)))
def test_each_witness_retention_ceiling_below_at_above_counts_pending_and_retained(clock, dimension, ceiling):
    budget, job = accepted_job()
    ledger = budget.witnesses
    first = ledger.reserve(**{dimension: ceiling - 1})
    second = ledger.reserve(**{dimension: 1})
    if dimension == "witnesses":
        assert retained_counts(ledger) == (20_000, 0, 0, 0)
    else:
        assert retained_counts(ledger) == (0, 100_000, 0, 0)
    ledger.retain(first)
    ledger.retain(second)
    expected = (0, 0, 20_000, 0) if dimension == "witnesses" else (0, 0, 0, 100_000)
    assert retained_counts(ledger) == expected
    with pytest.raises(_AnalysisAborted) as stopped:
        ledger.reserve(**{dimension: 1})
    assert stopped.value.limit_id == "WU9-L13"
    assert stopped.value.stop.input_state == "accepted"
    assert retained_counts(ledger) == expected
    for operation in (ledger.snapshot, lambda: ledger.release(first), lambda: ledger.retain(second)):
        with pytest.raises(_AnalysisAborted) as repeat:
            operation()
        assert repeat.value is stopped.value
    final = budget.begin_finalization()
    final.charge(3)
    assert retained_counts(ledger) == expected


@pytest.mark.parametrize("witnesses,members", ((2, 1), (1, 2)))
def test_joint_reservation_is_atomic_when_either_counter_would_exceed(clock, witnesses, members):
    budget, _ = accepted_job()
    ledger = budget.witnesses
    ledger.reserve(witnesses=19_999, members=99_999)
    before = retained_counts(ledger)
    with pytest.raises(_AnalysisAborted) as stopped:
        ledger.reserve(witnesses=witnesses, members=members)
    assert stopped.value.limit_id == "WU9-L13"
    assert retained_counts(ledger) == before


def test_pending_release_returns_only_capacity_without_refunding_work(clock):
    budget, job = accepted_job()
    ledger = budget.witnesses
    token = ledger.reserve(witnesses=20_000, members=100_000)
    before = (budget.used, job.used)
    ledger.release(token)
    assert retained_counts(ledger) == (0, 0, 0, 0)
    assert (budget.used, job.used) == (before[0] + 1, before[1] + 1)
    replacement = ledger.reserve(witnesses=20_000, members=100_000)
    ledger.retain(replacement)
    before = retained_counts(ledger)
    with pytest.raises(TypeError, match="^invalid_private_reservation$"):
        ledger.release(replacement)
    assert retained_counts(ledger) == before == (0, 0, 20_000, 100_000)
    with pytest.raises(TypeError, match="^invalid_private_reservation$"):
        ledger.retain(token)
    assert retained_counts(ledger) == before


def test_existing_witness_with_additional_member_occurrence_and_next_job_share_counts(clock):
    budget, first = accepted_job()
    ledger = budget.witnesses
    ledger.retain(ledger.reserve(witnesses=1, members=1))
    ledger.retain(ledger.reserve(witnesses=0, members=1))
    assert retained_counts(ledger) == (0, 0, 1, 2)
    budget.finish_job(first)
    second = budget.start_job()
    assert budget.witnesses is ledger
    ledger.retain(ledger.reserve(witnesses=1, members=2))
    assert retained_counts(ledger) == (0, 0, 2, 4)
    assert second.used > 0


@pytest.mark.parametrize("name", ("witnesses", "members"))
@pytest.mark.parametrize("value", (-1, True, False, 1.0, "1", None))
def test_invalid_witness_counts_preserve_both_counters_and_do_not_coerce(clock, name, value):
    budget, _ = accepted_job()
    ledger = budget.witnesses
    before = retained_counts(ledger)
    with pytest.raises(TypeError, match="^invalid_private_counter$"):
        ledger.reserve(**{name: value})
    assert retained_counts(ledger) == before
    token = ledger.reserve(witnesses=1, members=1)
    ledger.retain(token)
    assert retained_counts(ledger) == (0, 0, 1, 1)


@pytest.mark.parametrize("operation", ("retain", "release"))
def test_foreign_copied_unknown_and_reused_tokens_cannot_change_retention(clock, operation):
    first, _ = accepted_job()
    second, _ = accepted_job()
    ledger = first.witnesses
    other = second.witnesses
    token = ledger.reserve(witnesses=1, members=2)
    for candidate in (token, copy.copy(token), object()):
        with pytest.raises(TypeError, match="^invalid_private_reservation$"):
            getattr(other, operation)(candidate)
        assert retained_counts(other) == (0, 0, 0, 0)
    with pytest.raises(TypeError, match="^invalid_private_reservation$"):
        getattr(ledger, operation)(copy.copy(token))
    getattr(ledger, operation)(token)
    before = retained_counts(ledger)
    with pytest.raises(TypeError, match="^invalid_private_reservation$"):
        getattr(ledger, operation)(token)
    assert retained_counts(ledger) == before


@pytest.mark.parametrize("phase", ("between_jobs", "finalization"))
@pytest.mark.parametrize("operation", ("reserve", "retain", "release", "snapshot"))
def test_saved_witness_ledger_cannot_bypass_job_accounting_or_resume_during_finalization(clock, phase, operation):
    budget, job = accepted_job()
    ledger = budget.witnesses
    token = ledger.reserve(witnesses=1, members=2)
    budget.finish_job(job)
    if phase == "finalization":
        budget.begin_finalization()
    before = retained_counts(ledger)
    action = (lambda: ledger.reserve(witnesses=1)) if operation == "reserve" else (
        ledger.snapshot if operation == "snapshot" else lambda: getattr(ledger, operation)(token))
    with pytest.raises(_AnalysisAborted) as stopped:
        action()
    assert stopped.value.stop.reason_code == "execution_failed"
    assert retained_counts(ledger) == before
    with pytest.raises(_AnalysisAborted) as repeated:
        budget.start_job()
    assert repeated.value is stopped.value


@pytest.mark.parametrize("boundary", ("job", "global", "deadline"))
@pytest.mark.parametrize("operation", ("retain", "release"))
def test_work_or_time_stop_cannot_partially_retain_or_release_reserved_occurrences(clock, boundary, operation):
    budget = resources._new_analysis_budget()
    if boundary == "global":
        budget.charge(9_998_966)  # Exactly ten units for job/ledger/reservation setup.
    budget.record_input_acceptance()
    job = budget.start_job()
    ledger = budget.witnesses
    token = ledger.reserve(witnesses=1, members=2)
    assert job.used == 9 and retained_counts(ledger) == (1, 2, 0, 0)
    if boundary == "job":
        job.charge(999_991)
        assert job.used == 1_000_000
    elif boundary == "global":
        assert budget.used == 10_000_000
    else:
        clock[0] += 60_000_000_001
    before = (budget.used, job.used)
    with pytest.raises(_AnalysisAborted) as stopped:
        getattr(ledger, operation)(token)
    assert stopped.value.limit_id == ("WU9-L12" if boundary == "deadline" else "WU9-L11")
    assert retained_counts(ledger) == (1, 2, 0, 0)
    assert (budget.used, job.used) == before
    with pytest.raises(_AnalysisAborted) as again:
        ledger.retain(token)
    assert again.value is stopped.value
    assert retained_counts(ledger) == (1, 2, 0, 0)


@pytest.mark.parametrize("opened_finalization", (False, True))
def test_fixed_emergency_delivery_cannot_restart_or_continue_normal_finalization(clock, opened_finalization):
    budget, job = accepted_job()
    job.charge(1_000_000)
    with pytest.raises(_AnalysisAborted) as stopped:
        job.charge(1)
    final = budget.begin_finalization() if opened_finalization else None
    if final is not None:
        final.charge(3)
    before = budget.used
    assert budget.take_emergency() is stopped.value
    actions = [budget.begin_finalization, budget.start_job, lambda: job.charge(0), lambda: budget.charge(0)]
    if final is not None:
        actions.extend((final.check, lambda: final.charge(0)))
    for action in actions:
        with pytest.raises(_AnalysisAborted) as repeat:
            action()
        assert repeat.value is stopped.value
    assert budget.used == before
    with pytest.raises(RuntimeError, match="^emergency_delivery_already_used$"):
        budget.take_emergency()
