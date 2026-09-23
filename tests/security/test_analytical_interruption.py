# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W13 invocation tests for plan 3.4 and governance 22.3.

Faults are injected at tool-owned seams, never offered to callers. Fixed work,
time and witness ceilings are exercised without changing product constants.
The source fixture is tiny so each control completes before its paired fault.
"""
from dataclasses import fields
import importlib.util
import json
from pathlib import Path

import pytest

from source_integrity_toolkit.runtime import boundary, resources
from source_integrity_toolkit.contracts import report
from source_integrity_toolkit.runtime.diagnostics import _AnalyticalDiagnostic


ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    'sit_w13_interruption_cases', ROOT / 'tests/contract/test_typed_records.py')
cases = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cases)


def source():
    value = cases.sparse()
    value['inquiries'][0]['dependency_dimensions'] = ['acquisition']
    value['records'].append(cases.by_id(cases.pool(), 'artifact'))
    value['inquiries'][0]['seed_artifact_refs'] = ['artifact']
    return value


def analyze(value, mode):
    return (boundary._analyze_value(value) if mode == 'constructed_value' else
            boundary._analyze_utf8(json.dumps(value).encode('utf-8')))


def complete(value=None):
    out = boundary._analyze_value(source() if value is None else value)
    assert out.input_state == 'accepted' and out.execution_state == 'completed'
    assert out.results
    return out


def safe_stop(out, state, execution, code):
    assert type(out) is _AnalyticalDiagnostic
    assert (out.input_state, out.execution_state, out.code) == (state, execution, code)
    assert out.location is None
    assert not hasattr(out, 'results') and not hasattr(out, 'prepared')
    assert all('PRIVATE_SENTINEL' not in str(getattr(out, item.name)) for item in fields(out))


@pytest.fixture
def fixed_clock(monkeypatch):
    now = [100]
    monkeypatch.setattr(resources, 'monotonic_ns', lambda: now[0])
    return now


@pytest.mark.parametrize('mode', ('constructed_value', 'supplied_utf8'))
def test_whole_planning_exhaustion_precedes_acceptance_and_any_job(monkeypatch, fixed_clock, mode):
    complete()
    original = boundary._plan_analysis
    seen = []

    def stop_after_real_plan(prepared, budget):
        plan = original(prepared, budget)
        assert plan.jobs and budget.input_state == 'not_completed'
        seen.append((budget, budget.used))
        budget.charge(budget.remaining + 1)
        raise AssertionError('unreachable_after_prospective_stop')

    def no_job(*args):
        raise AssertionError('job_started_before_complete_plan')

    monkeypatch.setattr(boundary, '_plan_analysis', stop_after_real_plan)
    monkeypatch.setattr(boundary, '_execute_job', no_job)
    out = analyze(source(), mode)
    safe_stop(out, 'not_completed', 'interrupted', 'resource_limit_reached')
    assert out.qualifications == ('WU9-L11',)
    assert len(seen) == 1 and seen[0][0].used == seen[0][1]


def test_capture_planning_jobs_and_delivery_use_one_entry_budget(monkeypatch, fixed_clock):
    made, stages, ledgers = [], [], []
    factory, plan = boundary._new_analysis_budget, boundary._plan_analysis
    execute, assemble = boundary._execute_job, report._assemble_analysis

    def new_budget():
        budget = factory()
        made.append(budget)
        assert budget.used == 1024 and budget._start == 100
        return budget

    def no_preparation_budget():
        raise AssertionError('analysis_started_a_separate_preparation_budget')

    def planning(prepared, budget):
        assert budget is made[0] and budget.input_state == 'not_completed'
        assert budget.used > 1024
        result = plan(prepared, budget)
        stages.append(('plan', budget.used))
        return result

    def execution(prepared, spec, ledger, port):
        assert port._owner is made[0] and port._owner.input_state == 'accepted'
        assert port._owner._start == 100
        ledgers.append(ledger)
        stages.append(('job', port._owner.used))
        return execute(prepared, spec, ledger, port)

    def delivery(prepared, plan, outcomes, results, findings, witnesses, port, **kwargs):
        assert port._owner is made[0] and port._owner._start == 100
        stages.append(('finalization', port._owner.used))
        return assemble(prepared, plan, outcomes, results, findings, witnesses, port, **kwargs)

    monkeypatch.setattr(boundary, '_new_analysis_budget', new_budget)
    monkeypatch.setattr(boundary, '_new_budget', no_preparation_budget)
    monkeypatch.setattr(boundary, '_plan_analysis', planning)
    monkeypatch.setattr(boundary, '_execute_job', execution)
    monkeypatch.setattr(report, '_assemble_analysis', delivery)
    complete()
    assert len(made) == 1 and stages[0][0] == 'plan' and stages[-1][0] == 'finalization'
    assert len(ledgers) > 1 and all(item is ledgers[0] for item in ledgers)
    assert all(left[1] < right[1] for left, right in zip(stages, stages[1:]))
    assert made[0].used > stages[-1][1] and made[0]._start == 100


def test_job_stop_before_owner_retains_previous_complete_jobs_and_marks_later_cells(monkeypatch, fixed_clock):
    control = complete()
    execute = boundary._execute_job
    calls = []

    def stopped(prepared, spec, ledger, port):
        calls.append(spec.family)
        if len(calls) == 2:
            port.charge(1_000_000 - port.used + 1)
        return execute(prepared, spec, ledger, port)

    monkeypatch.setattr(boundary, '_execute_job', stopped)
    out = boundary._analyze_value(source())
    assert out.input_state == 'accepted' and out.execution_state == 'interrupted'
    assert calls == ['SIT-M001', 'SIT-M002']
    earlier = [row for row in out.results if row.ref.diagnostic_id == 'SIT-M001']
    assert len(earlier) == 5 and all(row.execution_state == 'completed' for row in earlier)
    assert [row.value.value for row in earlier] == [
        row.value.value for row in control.results if row.ref.diagnostic_id == 'SIT-M001']
    current = [row for row in out.results if row.ref.diagnostic_id == 'SIT-M002']
    assert len(current) == 3 and all(row.execution_state == 'interrupted' for row in current)
    later = [row for row in out.results if row.ref.diagnostic_id not in calls]
    assert later and all(row.execution_state == 'not_performed' for row in later)
    for row in current + later:
        assert row.result_state == 'not_evaluated' and row.value is None
        assert 'resource_limit_reached' in {reason.code for reason in row.reason_refs}
        assert not any(check.check_id == 'PC24' and check.state == 'met' for check in row.check_refs)


@pytest.mark.parametrize('limit', ('work', 'time'))
def test_delivery_must_fit_remaining_global_work_and_entry_deadline(monkeypatch, fixed_clock, limit):
    complete()
    assemble = report._assemble_analysis
    observed = []

    def exhausted(prepared, plan, outcomes, results, findings, witnesses, port, **kwargs):
        assert results and all(row.execution_state == 'completed' for row in results)
        observed.append(port._owner)
        if limit == 'work':
            port.charge(port._owner.remaining)
            assert port._owner.used == 10_000_000
        else:
            fixed_clock[0] = 60_000_000_101
        return assemble(prepared, plan, outcomes, results, findings, witnesses, port, **kwargs)

    monkeypatch.setattr(report, '_assemble_analysis', exhausted)
    out = boundary._analyze_value(source())
    safe_stop(out, 'accepted', 'interrupted', 'resource_limit_reached')
    assert out.qualifications == (('WU9-L11',) if limit == 'work' else ('WU9-L12',))
    assert len(observed) == 1 and observed[0]._emergency_taken


def test_later_findings_stop_keeps_actual_committed_cells_in_the_same_job(monkeypatch, fixed_clock):
    control = complete()
    owner = boundary._finding_owner
    original = owner._findings
    interrupted = []

    def unfinished_findings(prepared, context, ledger, port, **kwargs):
        profiles = kwargs.get('stage_profiles', ())
        if profiles and profiles[0].results[0].ref.diagnostic_id == 'SIT-M002':
            assert port._committed and len(port._committed[0]) == 3
            interrupted.append(port)
            port.charge(1_000_000 - port.used + 1)
        return original(prepared, context, ledger, port, **kwargs)

    monkeypatch.setattr(owner, '_findings', unfinished_findings)
    out = boundary._analyze_value(source())
    assert out.input_state == 'accepted' and out.execution_state == 'interrupted'
    assert len(interrupted) == 1
    current = [row for row in out.results if row.ref.diagnostic_id == 'SIT-M002']
    expected = [row for row in control.results if row.ref.diagnostic_id == 'SIT-M002']
    assert len(current) == len(expected) == 3
    assert [(row.ref.field_key, row.execution_state, row.result_state) for row in current] == [
        (row.ref.field_key, row.execution_state, row.result_state) for row in expected]
    assert all(row.execution_state == 'completed' for row in current)
    assert any(row.execution_state == 'not_performed' for row in out.results)
    assert not any('SIT-M002' in finding.diagnostic_refs for finding in out.findings)


@pytest.mark.parametrize('later_limit', ('work', 'time'))
def test_stopped_job_salvage_still_requires_delivery_budget_and_preserves_first_cause(monkeypatch, fixed_clock,
                                                                                   later_limit):
    complete()
    execute, assemble = boundary._execute_job, report._assemble_analysis
    calls = []

    def witness_stop(prepared, spec, ledger, port):
        calls.append(spec.family)
        if len(calls) == 2:
            ledger.reserve(witnesses=20_001)
        return execute(prepared, spec, ledger, port)

    def exhausted_delivery(prepared, plan, outcomes, results, findings, witnesses, port, **kwargs):
        assert kwargs['execution_state'] == 'interrupted'
        assert any(row.execution_state == 'completed' for row in results)
        assert any(row.execution_state == 'not_performed' for row in results)
        if later_limit == 'work':
            port.charge(port._owner.remaining)
        else:
            fixed_clock[0] = 60_000_000_101
        return assemble(prepared, plan, outcomes, results, findings, witnesses, port, **kwargs)

    monkeypatch.setattr(boundary, '_execute_job', witness_stop)
    monkeypatch.setattr(report, '_assemble_analysis', exhausted_delivery)
    out = boundary._analyze_value(source())
    safe_stop(out, 'accepted', 'interrupted', 'resource_limit_reached')
    assert calls == ['SIT-M001', 'SIT-M002']
    assert out.qualifications == ('WU9-L13',)


def test_nested_stage_targets_commit_before_context_referrers_and_survive_local_stop(monkeypatch, fixed_clock):
    value = source()
    value['inquiries'][0]['dependency_dimensions'] = []
    value['inquiries'][0]['seed_evidence_refs'] = ['e']
    pool = cases.pool()
    value['records'].extend((cases.by_id(pool, 'e'), cases.by_id(pool, 'pipeline')))
    value['assertions'] = [cases.relation('contradicts')]
    complete(value)
    execute, commit = boundary._execute_job, boundary._commit_job
    active, stopped = [], []

    def current_job(prepared, spec, ledger, port):
        active[:] = [spec]
        return execute(prepared, spec, ledger, port)

    def stop_before_context(port, values, findings, witnesses):
        if (values and active[0].family == 'SIT-M014' and
                active[0].operation_key[0] == 'tail_stage' and values[0].ref.diagnostic_id == 'SIT-M014'):
            assert port._committed and len(port._committed[0]) == 7
            assert all(row.ref.diagnostic_id == 'SIT-M010' and row.execution_state == 'completed'
                       for row in port._committed[0])
            stopped.append(active[0])
            port.charge(1_000_000 - port.used + 1)
        return commit(port, values, findings, witnesses)

    monkeypatch.setattr(boundary, '_execute_job', current_job)
    monkeypatch.setattr(boundary, '_commit_job', stop_before_context)
    out = boundary._analyze_value(value)
    assert out.input_state == 'accepted' and out.execution_state == 'interrupted'
    assert len(stopped) == 1
    stopped_job = next(job for job in out.jobs if job.job is stopped[0])
    assert stopped_job.execution_state == 'interrupted'
    delivered = {row.ref._key(): row for row in out.results}
    nested = [delivered[ref._key()] for ref in stopped_job.result_refs if ref.diagnostic_id == 'SIT-M010']
    context = [delivered[ref._key()] for ref in stopped_job.result_refs if ref.diagnostic_id == 'SIT-M014']
    assert len(nested) == 7 and all(row.execution_state == 'completed' for row in nested)
    assert len(context) == 3 and all(row.execution_state == 'interrupted' and row.value is None for row in context)
    for row in out.results:
        if row.ref.field_key == 'tail_stage_result_links' and row.result_state == 'available':
            assert all(item.source._key() in delivered for item in row.value.records)


@pytest.mark.parametrize('phase', ('planning', 'job'))
def test_single_deadline_includes_admission_and_all_prior_jobs(monkeypatch, fixed_clock, phase):
    complete()
    name = '_plan_analysis' if phase == 'planning' else '_execute_job'
    original = getattr(boundary, name)

    def elapsed(*args):
        fixed_clock[0] = 60_000_000_101
        return original(*args)

    monkeypatch.setattr(boundary, name, elapsed)
    out = boundary._analyze_value(source())
    safe_stop(out, 'not_completed' if phase == 'planning' else 'accepted',
              'interrupted', 'resource_limit_reached')
    assert out.qualifications == ('WU9-L12',)


@pytest.mark.parametrize('dimension,ceiling', (('witnesses', 20_000), ('members', 100_000)))
def test_shared_witness_ceiling_interrupts_without_clipping_or_continuation(monkeypatch, fixed_clock, dimension, ceiling):
    complete()
    execute = boundary._execute_job
    seen = []

    def overflow(prepared, spec, ledger, port):
        seen.append(spec.family)
        if len(seen) == 2:
            retained = ledger._retained_witnesses if dimension == 'witnesses' else ledger._retained_members
            reserved = ledger._reserved_witnesses if dimension == 'witnesses' else ledger._reserved_members
            assert retained > 0
            token = ledger.reserve(**{dimension: ceiling - retained - reserved})
            ledger.retain(token)
            ledger.reserve(**{dimension: 1})
        return execute(prepared, spec, ledger, port)

    monkeypatch.setattr(boundary, '_execute_job', overflow)
    out = boundary._analyze_value(source())
    assert out.execution_state == 'interrupted' and out.input_state == 'accepted'
    assert seen == ['SIT-M001', 'SIT-M002']
    assert all(row.execution_state == 'completed' for row in out.results if row.ref.diagnostic_id == 'SIT-M001')
    assert all(row.value is None for row in out.results if row.ref.diagnostic_id != 'SIT-M001')


@pytest.mark.parametrize('phase,state', (('_plan_analysis', 'not_completed'),
                                        ('_execute_job', 'accepted'),
                                        ('_assemble_analysis', 'accepted')))
@pytest.mark.parametrize('fault,execution,code', ((RuntimeError, 'failed', 'execution_failed'),
                                                 (KeyboardInterrupt, 'cancelled', None)))
def test_cancellation_and_engine_failure_are_distinct_payload_free_no_salvage(monkeypatch, fixed_clock,
                                                                          phase, state, fault, execution, code):
    complete()

    def broken(*args, **kwargs):
        raise fault('PRIVATE_SENTINEL source excerpt or exception text')

    monkeypatch.setattr(report if phase == '_assemble_analysis' else boundary, phase, broken)
    out = boundary._analyze_value(source())
    safe_stop(out, state, execution, code)
    if execution == 'cancelled':
        assert out.safe_message == 'Processing was cancelled.'
        assert out.qualifications == ('GOVERNANCE_AND_HANDOFF section 22.3: private cancellation transport.',)
    else:
        assert out.safe_message == 'Processing could not complete safely.' and out.qualifications == ()


def test_full_original_h7_keeps_fixed_quotas_and_only_completed_atomic_inventory(monkeypatch, fixed_clock):
    value = json.loads((ROOT / 'tests/fixtures/hero/H7-01.bundle.json').read_bytes())
    budgets = []
    factory = boundary._new_analysis_budget

    def tracked():
        budget = factory()
        budgets.append(budget)
        return budget

    monkeypatch.setattr(boundary, '_new_analysis_budget', tracked)
    out = boundary._analyze_value(value)
    assert len(budgets) == 1 and budgets[0].used <= 10_000_000
    assert resources._JOB_WORK_LIMIT == 1_000_000 and resources._WORK_LIMIT == 10_000_000
    assert out.input_state == 'accepted'
    if type(out) is _AnalyticalDiagnostic:
        safe_stop(out, 'accepted', 'interrupted', 'resource_limit_reached')
        assert out.qualifications == ('WU9-L11',)
        return
    assert out.execution_state in ('completed', 'interrupted')
    inventory = {row.ref.field_key: row for row in out.results if row.ref.diagnostic_id == 'SIT-M001'}
    assert inventory['nominal_seed_artifact_record_count'].value.value == 6
    assert inventory['seed_evidence_item_count'].value.value == 6
    for row in out.results:
        if row.execution_state != 'completed':
            assert row.result_state == 'not_evaluated' and row.value is None
        elif row.result_state == 'available':
            checks = {check.check_id: check.state for check in row.check_refs}
            assert checks['PC24'] == 'met'
    if out.execution_state == 'interrupted':
        assert any(row.result_state == 'not_evaluated' for row in out.results)
