# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W05 output-boundary controls, with literal limits from architecture 19.

These tests exercise the real existing ledger's restricted encoding port and
the internal encoder. Trusted component acceptance below is not a claim that
the public invocation or W07 runtime composition has run. Small remaining-byte
windows are created by actual fixed-counter charges, never by changing limits.
"""
import json
from pathlib import Path
import traceback

import pytest

from source_integrity_toolkit.contracts import report as report_contract
from source_integrity_toolkit.contracts.execution import (
    AuditAbort, AuditCancelled, _AnalysisAborted, _AuditCancelled, _ReportAborted,
)
from source_integrity_toolkit.reporting import escaping, json_report
from source_integrity_toolkit.runtime import diagnostics, resources


OUTPUT_LIMIT = 67_108_864
ROOT = Path(__file__).resolve().parents[2]


@pytest.fixture
def clock(monkeypatch):
    now = [100]
    monkeypatch.setattr(resources, 'monotonic_ns', lambda: now[0])
    return now


def encoding_context():
    owner = resources._new_analysis_budget()
    owner.record_input_acceptance()  # Trusted component fact, not input validation.
    finalizer = owner.begin_finalization()
    return owner, finalizer, owner.begin_report_encoding(finalizer)


def counters(owner):
    return owner._json_output_bytes, owner._markdown_output_bytes


class CapturePort:
    """Finite test-only freeze budget; no completed AuditReport is delivered."""
    def __init__(self):
        self.used = 0

    def charge(self, units):
        assert type(units) is int and units >= 0
        assert self.used + units <= 10_000_000
        self.used += units

    def check(self):
        pass


@pytest.fixture(scope='module')
def reference():
    expected = (ROOT / 'tests/golden/phase4_reference_report.json').read_bytes()
    frozen = report_contract._freeze_report_document(json.loads(expected), CapturePort())
    return frozen, expected


class ObservedPort:
    """Observe public-to-the-encoder operations on a genuine restricted port."""
    def __init__(self, delegate):
        self.delegate = delegate
        self.accepted = []
        self.attempted = []
        self.work = 0

    def charge(self, units):
        self.delegate.charge(units)
        self.work += units

    def check(self):
        self.delegate.check()

    def charge_output(self, encoding, count):
        self.attempted.append((encoding, count))
        self.delegate.charge_output(encoding, count)
        self.accepted.append((encoding, count))


@pytest.mark.parametrize('encoding', ('json', 'markdown'))
def test_actual_output_cap_below_equal_next_byte_is_rejected_prospectively(clock, encoding):
    owner, finalizer, port = encoding_context()
    port.charge_output(encoding, OUTPUT_LIMIT - 1)
    expected = (OUTPUT_LIMIT - 1, 0) if encoding == 'json' else (0, OUTPUT_LIMIT - 1)
    assert counters(owner) == expected
    port.charge_output(encoding, 1)
    expected = (OUTPUT_LIMIT, 0) if encoding == 'json' else (0, OUTPUT_LIMIT)
    assert counters(owner) == expected
    port.charge_output(encoding, 0)  # Equality does not itself stop processing.
    operation = []
    with pytest.raises(_ReportAborted) as stopped:
        port.charge_output(encoding, 1)
        operation.append('would emit forbidden byte')
    assert operation == [] and counters(owner) == expected
    assert stopped.value.limit_id == 'WU9-L14'
    assert stopped.value.stop.input_state == 'accepted'
    assert stopped.value.stop.reason_code == 'resource_limit_reached'
    for action in (port.check, lambda: port.charge(0),
                   lambda: port.charge_output('json', 0),
                   lambda: port.charge_output('markdown', 0), finalizer.check):
        with pytest.raises(_ReportAborted) as repeated:
            action()
        assert repeated.value is stopped.value


def test_fixed_output_counters_are_separate_cumulative_and_not_new_work_allowances(clock):
    owner = resources._new_analysis_budget()
    owner.charge(37)
    original_start = owner._start
    owner.record_input_acceptance()
    finalizer = owner.begin_finalization()
    before = owner.used
    port = owner.begin_report_encoding(finalizer)
    assert owner.used >= before and owner._start == original_start
    assert owner.used >= 1024 + 37
    port.charge_output('json', OUTPUT_LIMIT // 2)
    port.charge_output('markdown', OUTPUT_LIMIT - 1)
    port.charge_output('json', OUTPUT_LIMIT // 2)
    port.charge_output('markdown', 1)
    assert counters(owner) == (OUTPUT_LIMIT, OUTPUT_LIMIT)
    assert owner.used > before and owner.remaining == 10_000_000 - owner.used
    port.charge(17)
    assert owner.remaining == 10_000_000 - owner.used


@pytest.mark.parametrize('kind', ('negative', 'bool', 'float', 'text', 'none', 'hostile'))
def test_output_count_requires_exact_nonnegative_integer_without_protocols(clock, kind):
    calls = []
    class Hostile:
        def __int__(self):
            calls.append('int')
            return 0
        def __index__(self):
            calls.append('index')
            return 0
        def __repr__(self):
            calls.append('repr')
            return 'FICTIONAL_REPORT_PRIVATE_COUNT_5830'
    value = {'negative': -1, 'bool': True, 'float': 1.0, 'text': '1',
             'none': None, 'hostile': Hostile()}[kind]
    owner, _, port = encoding_context()
    port.charge_output('json', 9)
    with pytest.raises(_AnalysisAborted) as stopped:
        port.charge_output('json', value)
    assert stopped.value.stop.reason_code == 'execution_failed'
    assert counters(owner) == (9, 0) and calls == []


@pytest.mark.parametrize('kind', ('unknown', 'case', 'bytes', 'subclass', 'hostile'))
def test_encoding_name_cannot_select_extra_counter_or_invoke_custom_comparison(clock, kind):
    calls = []
    class Name(str):
        def __eq__(self, other):
            calls.append('eq')
            return True
        def __hash__(self):
            calls.append('hash')
            return 1
    class Hostile:
        def __eq__(self, other):
            calls.append('eq')
            return True
        def __repr__(self):
            calls.append('repr')
            return 'FICTIONAL_REPORT_FORMAT_5830'
    value = {'unknown': 'yaml', 'case': 'JSON', 'bytes': b'json',
             'subclass': Name('json'), 'hostile': Hostile()}[kind]
    owner, _, port = encoding_context()
    with pytest.raises(_AnalysisAborted) as stopped:
        port.charge_output(value, 1)
    assert stopped.value.stop.reason_code == 'execution_failed'
    assert counters(owner) == (0, 0) and calls == []


def test_report_port_has_no_new_clock_job_acceptance_or_reset_authority(clock):
    _, _, port = encoding_context()
    for name in ('clock', 'deadline', 'limits', 'options', 'callback', 'start_job',
                 'begin_finalization', 'begin_report_encoding', 'record_input_acceptance',
                 'take_emergency', 'reset', 'refund', 'restart', '__dict__'):
        assert not hasattr(port, name), name
    for kwargs in ({'limit': OUTPUT_LIMIT * 2}, {'clock': lambda: 0}, {'options': {}}):
        with pytest.raises(TypeError):
            port.charge_output('json', 1, **kwargs)


def test_duplicate_encoding_port_request_cannot_reset_existing_output_counts(clock):
    owner, finalizer, port = encoding_context()
    port.charge_output('json', 29)
    before = owner.used
    with pytest.raises(_AnalysisAborted) as stopped:
        owner.begin_report_encoding(finalizer)
    assert stopped.value.stop.reason_code == 'execution_failed'
    assert counters(owner) == (29, 0) and owner.used >= before
    with pytest.raises(_AnalysisAborted) as stale:
        port.charge_output('json', 0)
    assert stale.value is stopped.value


@pytest.mark.parametrize('remaining', (6, 7, 8))
def test_real_utf8_encoder_obeys_remaining_fixed_byte_cap_without_clipping(clock, remaining):
    # The literal J of this exact scalar is seven bytes: quotes + 3 + 2 UTF-8 bytes.
    expected = b'"\xe9\x9b\xaa\xc3\xa9"'
    assert len(expected) == 7
    owner, _, real = encoding_context()
    real.charge_output('json', OUTPUT_LIMIT - remaining)
    port = ObservedPort(real)
    returned = []
    if remaining < len(expected):
        with pytest.raises(_ReportAborted) as stopped:
            returned.append(escaping._encode_j('雪é', port))
        assert stopped.value.limit_id == 'WU9-L14' and returned == []
        accepted = sum(count for _, count in port.accepted)
        assert accepted <= remaining and counters(owner)[0] == OUTPUT_LIMIT - remaining + accepted
    else:
        actual = escaping._encode_j('雪é', port)
        assert actual == expected and counters(owner)[0] == OUTPUT_LIMIT - remaining + len(expected)
        assert sum(count for _, count in port.accepted) == len(expected)
    assert all(name == 'json' for name, _ in port.attempted)


@pytest.mark.parametrize('extra', (-1, 0, 1))
def test_report_final_lf_counts_against_actual_cap_and_no_partial_report_returns(clock, reference, extra):
    frozen, expected = reference
    assert expected.endswith(b'\n') and not expected.endswith(b'\n\n')
    owner, _, real = encoding_context()
    real.charge_output('json', OUTPUT_LIMIT - len(expected) - extra)
    port = ObservedPort(real)
    returned = []
    if extra < 0:
        with pytest.raises(_ReportAborted) as stopped:
            returned.append(json_report._encode_json_report(frozen, port))
        assert stopped.value.limit_id == 'WU9-L14'
        assert returned == []
        assert sum(count for _, count in port.accepted) == len(expected) - 1
        assert port.attempted[-1] == ('json', 1)
        assert counters(owner) == (OUTPUT_LIMIT, 0)
    else:
        result = json_report._encode_json_report(frozen, port)
        assert result == expected
        assert sum(count for _, count in port.accepted) == len(expected)
        assert counters(owner) == (OUTPUT_LIMIT - extra, 0)
    assert port.work > 0


@pytest.mark.parametrize('boundary', ('work', 'time', 'failure', 'cancel'))
def test_mid_encoding_stop_returns_no_prefix_and_preserves_actual_acceptance(clock, boundary):
    owner, _, real = encoding_context()
    class StopAfterOutput(ObservedPort):
        def charge_output(self, encoding, count):
            super().charge_output(encoding, count)
            if len(self.accepted) == 2:
                if boundary == 'work':
                    self.delegate.charge(owner.remaining)
                elif boundary == 'time':
                    clock[0] += 60_000_000_001
                elif boundary == 'failure':
                    owner.fail()
                else:
                    owner.cancel()
    port = StopAfterOutput(real)
    returned = []
    expected_type = _AuditCancelled if boundary == 'cancel' else _AnalysisAborted
    with pytest.raises(expected_type) as stopped:
        returned.append(escaping._encode_j(('first', 'second', 'third'), port))
    assert returned == [] and len(port.accepted) == 2
    assert counters(owner)[0] == sum(count for _, count in port.accepted)
    public = diagnostics._report_abort(stopped.value)
    assert public.input_validation_state == 'accepted'
    assert public.publication_state == 'not_published'
    if boundary == 'cancel':
        assert type(public) is AuditCancelled and not hasattr(public, 'reason_code')
    else:
        assert type(public) is AuditAbort
        assert public.reason_code == ('execution_failed' if boundary == 'failure' else 'resource_limit_reached')
        if boundary in ('work', 'time'):
            assert stopped.value.limit_id == ('WU9-L11' if boundary == 'work' else 'WU9-L12')
    with pytest.raises(expected_type) as repeated:
        port.charge_output('markdown', 0)
    assert repeated.value is stopped.value


def test_report_phase_keeps_original_deadline_at_equality_and_next_nanosecond(clock):
    owner = resources._new_analysis_budget()
    clock[0] += 59_999_999_999
    owner.record_input_acceptance()
    final = owner.begin_finalization()
    port = owner.begin_report_encoding(final)
    clock[0] += 1
    port.charge_output('json', 1)
    clock[0] += 1
    with pytest.raises(_AnalysisAborted) as stopped:
        port.charge_output('json', 1)
    assert stopped.value.limit_id == 'WU9-L12'
    assert counters(owner) == (1, 0)


@pytest.mark.parametrize('first', ('job', 'witness'))
@pytest.mark.parametrize('later', ('output', 'work', 'time'))
def test_late_report_limit_preserves_earlier_analytical_stop_and_blocks_both_ports(clock, first, later):
    owner = resources._new_analysis_budget()
    owner.record_input_acceptance()
    job = owner.start_job()
    with pytest.raises(_AnalysisAborted) as original:
        job.interrupt('WU9-L11' if first == 'job' else 'WU9-L13')
    finalizer = owner.begin_finalization()
    port = owner.begin_report_encoding(finalizer)
    port.charge_output('json', 7)
    if later == 'output':
        port.charge_output('json', OUTPUT_LIMIT - 7)
        action = lambda: port.charge_output('json', 1)
    elif later == 'work':
        port.charge(owner.remaining)
        action = lambda: port.charge_output('json', 1)
    else:
        clock[0] += 60_000_000_001
        action = lambda: port.charge_output('json', 1)
    before = counters(owner)
    with pytest.raises(_AnalysisAborted) as stopped:
        action()
    assert stopped.value is original.value
    for action in (finalizer.check, port.check, lambda: port.charge_output('markdown', 0)):
        with pytest.raises(_AnalysisAborted) as repeated:
            action()
        assert repeated.value is original.value
    assert counters(owner) == before
    assert diagnostics._report_abort(stopped.value).input_validation_state == 'accepted'


@pytest.mark.parametrize('kind', ('admission', 'foreign_finalizer', 'forged_port'))
def test_report_encoding_requires_current_owner_and_existing_finalization(clock, kind):
    owner = resources._new_analysis_budget()
    if kind == 'admission':
        action = lambda: owner.begin_report_encoding(None)
    else:
        owner.record_input_acceptance()
        finalizer = owner.begin_finalization()
        if kind == 'foreign_finalizer':
            other, other_finalizer, _ = encoding_context()
            other_before = (other.used, counters(other))
            action = lambda: owner.begin_report_encoding(other_finalizer)
        else:
            owner.begin_report_encoding(finalizer)
            forged = resources._BoundedReportEncoding(owner)
            action = lambda: forged.charge_output('json', 1)
    with pytest.raises(_AnalysisAborted) as stopped:
        action()
    assert stopped.value.stop.reason_code == 'execution_failed'
    assert stopped.value.stop.input_state == ('not_completed' if kind == 'admission' else 'accepted')
    assert counters(owner) == (0, 0)
    if kind == 'foreign_finalizer':
        assert (other.used, counters(other)) == other_before
        other_finalizer.check()


def test_l14_emergency_delivery_uses_existing_reserve_once_without_payload(clock, capsys):
    owner, finalizer, port = encoding_context()
    with pytest.raises(_ReportAborted) as stopped:
        port.charge_output('json', OUTPUT_LIMIT + 1)
    before = owner.used
    public = diagnostics._emergency_report_abort(owner)
    assert type(public) is AuditAbort
    assert (public.processing_state, public.input_validation_state, public.reason_code,
            public.publication_state) == ('interrupted', 'accepted', 'resource_limit_reached', 'not_published')
    assert owner.used == before
    assert public.args == ('Audit could not be completed.',)
    assert len((str(public) + repr(public)).encode()) < 4096
    for name in ('report', 'results', 'prefix', 'source', 'snapshot', 'original_exception', 'payload'):
        assert not hasattr(public, name) and not hasattr(stopped.value, name)
    for action in (finalizer.check, port.check):
        with pytest.raises(_ReportAborted) as repeated:
            action()
        assert repeated.value is stopped.value
    with pytest.raises(RuntimeError, match='^emergency_delivery_already_used$'):
        diagnostics._emergency_report_abort(owner)
    assert capsys.readouterr() == ('', '')


def test_report_abort_mapping_rejects_unknown_exception_without_private_protocols():
    calls = []
    class Hostile(Exception):
        def __str__(self):
            calls.append('str')
            return 'FICTIONAL_REPORT_EXCEPTION_SECRET_8392'
        def __repr__(self):
            calls.append('repr')
            return 'FICTIONAL_REPORT_EXCEPTION_SECRET_8392'
    with pytest.raises(TypeError) as stopped:
        diagnostics._report_abort(Hostile())
    assert calls == []
    visible = str(stopped.value) + repr(stopped.value) + ''.join(traceback.format_exception(stopped.value))
    assert 'FICTIONAL_REPORT_EXCEPTION_SECRET_8392' not in visible
