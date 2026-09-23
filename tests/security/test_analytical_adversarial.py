# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W14 exact payment and commit-boundary adversaries, plan 3.4/19.

Existing cumulative input/analytical ledgers cover every implemented ceiling;
graph tests cover large deep/wide/many-walk finite populations. These additional
controls cross real helper work with its exact remaining allowance and inject
faults at the final check before immutable job publication. No product limit is
changed and no caller receives a clock, budget or fault-injection option.
"""
import copy
from dataclasses import fields
import importlib.util
import json
from pathlib import Path
import sys

import pytest

from source_integrity_toolkit.contracts import bundle, report
from source_integrity_toolkit.contracts.execution import _AnalysisAborted
from source_integrity_toolkit.runtime import boundary, resources
from source_integrity_toolkit.runtime.diagnostics import _AnalyticalDiagnostic


ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    'sit_w14_adversarial_cases', ROOT / 'tests/integration/test_analytical_pipeline.py')
cases = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cases)
CANARY = 'FICTIONAL_W14_COMMIT_PRIVATE_361947'


@pytest.fixture
def clock(monkeypatch):
    monkeypatch.setattr(resources, 'monotonic_ns', lambda: 100)


def port_for(limit):
    owner = resources._new_analysis_budget()
    owner.record_input_acceptance()
    port = owner.start_job() if limit == 'job' else owner.begin_finalization()
    return owner, port


def operation(name, port):
    if name == 'source_sort':
        return bundle._sorted_pairs((('z', True), ('a', None), ('middle', False)), port)
    if name == 'source_lookup':
        return bundle._lookup_pair((('a', None), ('middle', False), ('z', True)), 'middle', port)
    if name == 'exact_number':
        return bundle._number_from_token('1.2500e-10', port)
    if name == 'delivery_sort':
        return report._key_sort((('z', 2), ('a', 9), ('a', 1)), port)
    raise AssertionError('unknown_test_operation')


def assert_value(name, value):
    if name == 'source_sort':
        assert value == (('a', None), ('middle', False), ('z', True))
    elif name == 'source_lookup':
        assert value == ('middle', False)
    elif name == 'exact_number':
        assert type(value) is bundle._Number
        assert (value.sign, value.coefficient, value.exponent, value.source_kind) == (1, '125', -12, 'decimal')
    else:
        assert value == (('a', 1), ('a', 9), ('z', 2))


@pytest.mark.parametrize('name', ('source_sort', 'source_lookup', 'exact_number', 'delivery_sort'))
@pytest.mark.parametrize('limit', ('job', 'global'))
@pytest.mark.parametrize('delta', (-1, 0, 1))
def test_paid_helper_completes_only_when_every_comparison_copy_and_numeric_step_fits(clock, name, limit, delta):
    control_owner, control = port_for(limit)
    before = control_owner.used
    assert_value(name, operation(name, control))
    cost = control_owner.used - before
    assert cost > 1
    assert_value(name, operation(name, control))
    assert control_owner.used - before == 2 * cost

    owner, port = port_for(limit)
    ceiling = 1_000_000 if limit == 'job' else 10_000_000
    used = port.used if limit == 'job' else owner.used
    port.charge(ceiling - used - cost + delta)
    if delta <= 0:
        assert_value(name, operation(name, port))
        assert (port.used if limit == 'job' else owner.used) == ceiling + delta
    else:
        with pytest.raises(_AnalysisAborted) as stopped:
            operation(name, port)
        assert stopped.value.limit_id == 'WU9-L11'
        assert stopped.value.stop.input_state == 'accepted'
        assert owner._stop_kind == limit
        used = owner.used
        with pytest.raises(_AnalysisAborted) as repeated:
            operation(name, port)
        assert repeated.value is stopped.value and owner.used == used
        assert (port.used if limit == 'job' else owner.used) <= ceiling


def source():
    value = cases._minimal_value()
    value['inquiries'][0].update(seed_artifact_refs=['artifact'], dependency_dimensions=['acquisition'])
    value['records'].append(cases._record('artifact', 'artifact', {
        'artifact_kind': 'document', 'work_key': 'work', 'version_label': 'v1',
        'locators': [], 'published_at': cases._unknown(), 'retrieved_at': cases._unknown(),
        'content_evidence_refs': []}))
    return value


@pytest.mark.parametrize('mode', ('constructed_value', 'supplied_utf8'))
@pytest.mark.parametrize('fault', ('memory', 'opaque_exception', 'cancel', 'job_work'))
def test_failure_at_final_commit_check_cannot_publish_current_cells_or_source_exception(clock, monkeypatch,
                                                                                       mode, fault, capsys):
    value = source()
    original_value = copy.deepcopy(value)
    control = boundary._analyze_value(value)
    assert type(control) is report._AnalyticalOutcome and control.execution_state == 'completed'
    assert any(row.ref.diagnostic_id == 'SIT-M002' and row.execution_state == 'completed'
               for row in control.results)
    commit, check = boundary._commit_job, resources._AnalyticalJob.check
    active = []
    observations = []

    class Opaque(Exception):
        def __repr__(self):
            raise AssertionError('source_exception_repr_called')
        def __str__(self):
            raise AssertionError('source_exception_str_called')

    def committing(port, results, findings, witnesses):
        chosen = bool(results and results[0].ref.diagnostic_id == 'SIT-M002')
        if chosen:
            assert port._committed is None
            active.append(port)
        try:
            return commit(port, results, findings, witnesses)
        finally:
            if chosen:
                active.pop()

    def checked(port):
        # Direct final check in the real commit function, after its tuple was
        # built and before the only publication assignment. Earlier charged
        # link/scalar helper checks remain real and unmodified.
        if active and active[-1] is port and sys._getframe(1).f_code.co_name == '_commit_job':
            observations.append(port)
            assert port._committed is None
            if fault == 'job_work':
                port.charge(1_000_000 - port.used + 1)
            if fault == 'memory':
                raise MemoryError(CANARY)
            if fault == 'cancel':
                raise KeyboardInterrupt(CANARY)
            raise Opaque(CANARY)
        return check(port)

    monkeypatch.setattr(boundary, '_commit_job', committing)
    monkeypatch.setattr(resources._AnalyticalJob, 'check', checked)
    out = (boundary._analyze_value(value) if mode == 'constructed_value'
           else boundary._analyze_utf8(json.dumps(value).encode()))
    assert len(observations) == 1 and observations[0]._committed is None
    assert value == original_value and capsys.readouterr() == ('', '')
    if fault == 'job_work':
        assert type(out) is report._AnalyticalOutcome
        assert (out.input_state, out.execution_state) == ('accepted', 'interrupted')
        earlier = [row for row in out.results if row.ref.diagnostic_id == 'SIT-M001']
        assert len(earlier) == 5 and all(row.execution_state == 'completed' for row in earlier)
        current = [row for row in out.results if row.ref.diagnostic_id == 'SIT-M002']
        assert len(current) == 3 and all(row.execution_state == 'interrupted' for row in current)
        for row in out.results:
            if row.ref.diagnostic_id != 'SIT-M001':
                assert row.result_state == 'not_evaluated' and row.value is None
                assert not any(check.check_id == 'PC24' and check.state == 'met' for check in row.check_refs)
    else:
        assert type(out) is _AnalyticalDiagnostic and out.input_state == 'accepted'
        assert out.execution_state == ('cancelled' if fault == 'cancel' else 'failed')
        assert out.code == (None if fault == 'cancel' else 'execution_failed')
        assert out.location is None and not hasattr(out, 'prepared') and not hasattr(out, 'results')
        assert all(CANARY not in str(getattr(out, field.name)) for field in fields(out))
