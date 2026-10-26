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
from source_integrity_toolkit.reporting import markdown_report
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


_MARKDOWN_ROOTS = (
    'contract_version', 'report_kind', 'report_id', 'run', 'input_identity',
    'input_validation', 'scopes', 'populations', 'basis_index', 'capabilities',
    'checks', 'observability_domains', 'results', 'findings', 'reasons',
    'release_limits',
)


@pytest.fixture(scope='module')
def markdown_reference(reference):
    frozen, _ = reference
    expected = (ROOT / 'tests/golden/phase4_reference_report.md').read_bytes()
    return frozen, expected


@pytest.fixture(scope='module')
def small_markdown_document():
    """Accepted diagnostic component derived from the independent reference.

    It has no analytical rows. The one safe string deliberately needs a
    four-backtick fence; its scalar spelling has no special JSON controls.
    This fixture is not emitted by a renderer or an actual failed invocation.
    """
    document = json.loads((ROOT / 'tests/golden/phase4_reference_report.json').read_bytes())
    document['report_kind'] = 'processing_diagnostics'
    document['run']['processing_state'] = 'failed'
    document['run']['completed_diagnostic_ids'] = []
    document['run']['diagnostics'] = [{
        'code': 'execution_failed', 'location': None,
        'safe_message': 'Finite ``` fence and 雪 fixture.',
        'qualifications': ['No source-quality conclusion.'],
    }]
    for key in ('scopes', 'populations', 'basis_index', 'capabilities', 'checks',
                'observability_domains', 'results', 'findings', 'reasons'):
        document[key] = []
    frozen = report_contract._freeze_report_document(document, CapturePort())
    # Independent literal layout plus stdlib pretty JSON is valid for these
    # fixed scalars, which have none of J's special escaped control ranges.
    expected = ('# Source Integrity Audit\n\n'
                'Report kind: processing_diagnostics\n'
                'Processing state: failed\nInput state: accepted\n\n')
    for index, name in enumerate(_MARKDOWN_ROOTS):
        body = json.dumps(document[name], ensure_ascii=False, sort_keys=True, indent=2)
        fence = '````' if name == 'run' else '```'
        expected += '## ' + name + '\n\n' + fence + 'json\n' + body + '\n' + fence + '\n'
        if index < len(_MARKDOWN_ROOTS) - 1:
            expected += '\n'
    return frozen, expected.encode('utf-8')


@pytest.mark.parametrize('extra', (-1, 0, 1))
def test_markdown_final_lf_uses_actual_cap_without_prefix_delivery(clock, markdown_reference, extra):
    frozen, expected = markdown_reference
    assert expected.endswith(b'\n') and not expected.endswith(b'\n\n')
    owner, _, real = encoding_context()
    allowed = len(expected) + extra
    real.charge_output('markdown', OUTPUT_LIMIT - allowed)
    port = ObservedPort(real)
    returned = []
    if extra < 0:
        with pytest.raises(_ReportAborted) as stopped:
            returned.append(markdown_report._encode_markdown_report(frozen, port))
        accepted = sum(count for _, count in port.accepted)
        assert stopped.value.limit_id == 'WU9-L14' and returned == []
        assert 0 < accepted <= allowed
        assert accepted + port.attempted[-1][1] > allowed
        assert counters(owner) == (0, OUTPUT_LIMIT - allowed + accepted)
    else:
        actual = markdown_report._encode_markdown_report(frozen, port)
        assert actual == expected
        assert counters(owner) == (0, OUTPUT_LIMIT - extra)
        assert sum(count for _, count in port.accepted) == len(expected)
    assert all(name == 'markdown' for name, _ in port.attempted)


def test_markdown_cap_includes_pretty_spaces_fences_and_all_linefeeds(clock, small_markdown_document):
    frozen, expected = small_markdown_document
    assert b'````json\n' in expected and b'\n      "code": ' in expected
    owner, _, real = encoding_context()
    real.charge_output('markdown', OUTPUT_LIMIT - len(expected))
    port = ObservedPort(real)
    actual = markdown_report._encode_markdown_report(frozen, port)
    assert actual == expected and counters(owner) == (0, OUTPUT_LIMIT)
    assert sum(count for _, count in port.accepted) == len(expected)
    with pytest.raises(_ReportAborted) as stopped:
        real.charge_output('markdown', 1)
    assert stopped.value.limit_id == 'WU9-L14'


@pytest.mark.parametrize('boundary', ('work', 'time', 'failure', 'cancel'))
def test_markdown_mid_output_stop_returns_no_partial_bytes(clock, small_markdown_document, boundary):
    frozen, expected = small_markdown_document
    owner, _, real = encoding_context()
    class StopDuringMarkdown(ObservedPort):
        def charge_output(self, encoding, count):
            super().charge_output(encoding, count)
            if len(self.accepted) == 5:
                if boundary == 'work':
                    self.delegate.charge(owner.remaining)
                elif boundary == 'time':
                    clock[0] += 60_000_000_001
                elif boundary == 'failure':
                    owner.fail()
                else:
                    owner.cancel()
    port = StopDuringMarkdown(real)
    returned = []
    stopped_type = _AuditCancelled if boundary == 'cancel' else _AnalysisAborted
    with pytest.raises(stopped_type) as stopped:
        returned.append(markdown_report._encode_markdown_report(frozen, port))
    assert returned == [] and len(port.accepted) == 5
    charged = sum(count for _, count in port.accepted)
    assert 0 < charged < len(expected)
    assert counters(owner) == (0, charged)
    public = diagnostics._report_abort(stopped.value)
    assert public.input_validation_state == 'accepted' and public.publication_state == 'not_published'
    assert type(public) is (AuditCancelled if boundary == 'cancel' else AuditAbort)
    if boundary != 'cancel':
        assert public.reason_code == ('execution_failed' if boundary == 'failure' else 'resource_limit_reached')
    for name in ('json', 'markdown'):
        with pytest.raises(stopped_type) as repeated:
            port.charge_output(name, 0)
        assert repeated.value is stopped.value


def test_two_encoders_share_one_ledger_and_keep_distinct_byte_counts(clock, small_markdown_document):
    frozen, expected_markdown = small_markdown_document
    owner, finalizer, port = encoding_context()
    start, initial_work = owner._start, owner.used
    json_bytes = json_report._encode_json_report(frozen, port)
    after_json = owner.used
    assert initial_work < after_json and counters(owner) == (len(json_bytes), 0)
    markdown_bytes = markdown_report._encode_markdown_report(frozen, port)
    assert markdown_bytes == expected_markdown
    assert owner._start == start and owner.used > after_json
    assert counters(owner) == (len(json_bytes), len(expected_markdown))
    assert owner.remaining == 10_000_000 - owner.used
    finalizer.check()
    with pytest.raises(TypeError, match='AuditReport is delivered only by audit_bundle'):
        report_contract.AuditReport()


def test_complete_json_does_not_make_later_failed_markdown_a_delivered_pair(clock, small_markdown_document):
    frozen, expected_markdown = small_markdown_document
    owner, _, port = encoding_context()
    json_bytes = json_report._encode_json_report(frozen, port)
    assert json_bytes.endswith(b'\n')
    port.charge_output('markdown', OUTPUT_LIMIT - len(expected_markdown) + 1)
    returned_pairs = []
    with pytest.raises(_ReportAborted) as stopped:
        markdown_bytes = markdown_report._encode_markdown_report(frozen, port)
        returned_pairs.append((json_bytes, markdown_bytes))
    assert returned_pairs == [] and counters(owner)[0] == len(json_bytes)
    assert stopped.value.limit_id == 'WU9-L14'
    public = diagnostics._report_abort(stopped.value)
    assert public.input_validation_state == 'accepted' and public.publication_state == 'not_published'
    assert not hasattr(public, 'report') and not hasattr(public, 'prefix')


# W07 controls below execute the internal whole invocation, including actual
# admission, analysis, selection, logical assembly and both bounded encoders.
# The earlier W05/W06 component controls remain unchanged above.
@pytest.fixture
def invocation_source():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'p4_w07_resource_pipeline_helpers', ROOT / 'tests/integration/test_public_audit.py')
    helpers = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(helpers)
    return helpers._minimal_value()


def _observe_invocation(monkeypatch):
    from source_integrity_toolkit.runtime import boundary
    created = []
    factory = boundary._new_analysis_budget

    def observed_factory():
        owner = factory()
        created.append(owner)
        assert owner.used == 1024 and not owner._emergency_taken
        return owner

    monkeypatch.setattr(boundary, '_new_analysis_budget', observed_factory)
    return boundary, created


def _actual_port(owner):
    return owner._finalizer if owner._phase == 'finalization' else owner


def _assert_public_abort(stopped, input_state, reason='resource_limit_reached'):
    assert type(stopped) is AuditAbort
    assert (stopped.input_validation_state, stopped.reason_code,
            stopped.publication_state) == (input_state, reason, 'not_published')
    assert stopped.processing_state == ('failed' if reason == 'execution_failed' else 'interrupted')
    assert stopped.args == ('Audit could not be completed.',)
    for name in ('report', 'prefix', 'source', 'snapshot', 'budget', 'original_exception'):
        assert not hasattr(stopped, name)


_INVOCATION_STAGES = (
    '_admit', '_plan_analysis', '_execute_job', '_assemble_analysis',
    '_assemble_selected_report', '_encode_json_report',
    '_encode_markdown_report', '_verify_json_report', '_verify_markdown_report',
    '_deliver_report',
)


def test_whole_invocation_uses_one_factory_ledger_deadline_and_reserved_emergency(
        monkeypatch, clock, invocation_source):
    boundary, created = _observe_invocation(monkeypatch)
    stages = []
    made = []
    initialize = resources._AnalysisBudget.__post_init__

    def initialization(owner):
        initialize(owner)
        made.append(owner)

    monkeypatch.setattr(resources._AnalysisBudget, '__post_init__', initialization)
    for name in _INVOCATION_STAGES:
        original = getattr(boundary, name)

        def observed(*args, _name=name, _original=original, **kwargs):
            assert len(created) == 1 and made == created
            owner = created[0]
            assert owner._start == 100 and owner.used >= 1024
            if _name == '_admit':
                assert kwargs['budget'] is owner and owner.input_state == 'not_completed'
            elif _name == '_plan_analysis':
                assert args[1] is owner and owner.input_state == 'not_completed'
            else:
                assert args[-1]._owner is owner and owner.input_state == 'accepted'
            before = owner.used
            result = _original(*args, **kwargs)
            assert owner.used > before
            stages.append((_name, before, owner.used))
            return result

        monkeypatch.setattr(boundary, name, observed)
    delivered = boundary._audit_value(invocation_source)
    assert type(delivered) is report_contract.AuditReport
    assert {row[0] for row in stages} == set(_INVOCATION_STAGES)
    assert len(created) == len(made) == 1
    owner = created[0]
    assert owner._start == 100 and not owner._emergency_taken
    assert 1024 < owner.used < 10_000_000
    assert counters(owner) == (len(delivered.to_json_bytes()), len(delivered.to_markdown_bytes()))
    before = owner.used
    json_bytes, markdown_bytes = delivered.to_json_bytes(), delivered.to_markdown_bytes()
    clock[0] = owner._start + 60_000_000_001
    for _ in range(3):
        assert delivered.to_json_bytes() is json_bytes
        assert delivered.to_markdown_bytes() is markdown_bytes
    assert owner.used == before and not owner._emergency_taken


@pytest.mark.parametrize('stage', _INVOCATION_STAGES)
@pytest.mark.parametrize('limit', ('work', 'time'))
def test_each_invocation_stage_obeys_same_global_work_and_original_deadline(
        monkeypatch, clock, invocation_source, stage, limit):
    boundary, created = _observe_invocation(monkeypatch)
    original = getattr(boundary, stage)
    reached = []

    def stopped_stage(*args, **kwargs):
        assert len(created) == 1
        owner = created[0]
        reached.append((owner.used, owner.input_state))
        port = _actual_port(owner)
        if limit == 'work':
            port.charge(owner.remaining + 1)
        else:
            clock[0] = owner._start + 60_000_000_001
            port.check()
        return original(*args, **kwargs)

    monkeypatch.setattr(boundary, stage, stopped_stage)
    with pytest.raises(AuditAbort) as stopped:
        boundary._audit_value(invocation_source)
    assert len(created) == len(reached) == 1
    owner = created[0]
    expected = 'not_completed' if stage in ('_admit', '_plan_analysis') else 'accepted'
    _assert_public_abort(stopped.value, expected)
    assert reached[0][1] == expected and owner._start == 100
    assert owner._emergency_taken and owner.used == reached[0][0]
    assert owner._cause.limit_id == ('WU9-L11' if limit == 'work' else 'WU9-L12')
    with pytest.raises(RuntimeError, match='^emergency_delivery_already_used$'):
        owner.take_emergency()


@pytest.mark.parametrize('stage', _INVOCATION_STAGES)
def test_cancellation_at_each_stage_has_actual_state_and_never_returns_report(
        monkeypatch, clock, invocation_source, stage):
    boundary, created = _observe_invocation(monkeypatch)
    reached = []

    def cancelled(*args, **kwargs):
        reached.append(created[0].input_state)
        raise KeyboardInterrupt('PRIVATE_W07_CANCEL_DETAILS')

    monkeypatch.setattr(boundary, stage, cancelled)
    with pytest.raises(AuditCancelled) as stopped:
        boundary._audit_value(invocation_source)
    expected = 'not_completed' if stage in ('_admit', '_plan_analysis') else 'accepted'
    assert reached == [expected] and len(created) == 1
    assert stopped.value.input_validation_state == expected
    assert stopped.value.publication_state == 'not_published'
    assert not hasattr(stopped.value, 'reason_code') and not hasattr(stopped.value, 'report')
    assert 'PRIVATE_W07_CANCEL_DETAILS' not in str(stopped.value) + repr(stopped.value)
    assert created[0]._emergency_taken


@pytest.mark.parametrize('stage', ('_admit', '_execute_job'))
def test_failure_before_finalization_can_deliver_only_safe_diagnostic_on_same_budget(
        monkeypatch, clock, invocation_source, stage):
    boundary, created = _observe_invocation(monkeypatch)

    def failed(*args, **kwargs):
        raise RuntimeError('PRIVATE_W07_FAILURE_DETAILS')

    monkeypatch.setattr(boundary, stage, failed)
    delivered = boundary._audit_value(invocation_source)
    assert type(delivered) is report_contract.AuditReport and len(created) == 1
    document = json.loads(delivered.to_json_bytes())
    assert document['report_kind'] == 'processing_diagnostics'
    assert document['run']['processing_state'] == 'failed'
    assert document['input_validation']['state'] == ('not_completed' if stage == '_admit' else 'accepted')
    assert document['run']['diagnostics'][0]['code'] == 'execution_failed'
    for name in ('scopes', 'populations', 'basis_index', 'capabilities', 'checks',
                 'observability_domains', 'results', 'findings'):
        assert document[name] == []
    # Reporting 16.1 empties analytical arrays, retaining safe execution Reasons.
    assert document['reasons'] and all(reason['code'] == 'execution_failed' and
        reason['classification'] == 'execution' and reason['scope_ref'] is None and
        reason['affected_result_refs'] == [] and reason['input_refs'] == []
        for reason in document['reasons'])
    assert b'PRIVATE_W07_FAILURE_DETAILS' not in delivered.to_json_bytes()
    assert b'PRIVATE_W07_FAILURE_DETAILS' not in delivered.to_markdown_bytes()
    assert counters(created[0]) == (len(delivered.to_json_bytes()), len(delivered.to_markdown_bytes()))
    assert created[0]._start == 100 and 1024 < created[0].used <= 10_000_000


@pytest.mark.parametrize('stage', ('_assemble_analysis', '_assemble_selected_report',
                                 '_encode_json_report', '_encode_markdown_report',
                                 '_verify_json_report', '_verify_markdown_report', '_deliver_report'))
def test_failure_after_finalization_cannot_restart_or_deliver_a_partial_report(
        monkeypatch, clock, invocation_source, stage):
    boundary, created = _observe_invocation(monkeypatch)

    def failed(*args, **kwargs):
        raise RuntimeError('PRIVATE_W07_FINALIZATION_FAILURE')

    monkeypatch.setattr(boundary, stage, failed)
    with pytest.raises(AuditAbort) as stopped:
        boundary._audit_value(invocation_source)
    _assert_public_abort(stopped.value, 'accepted', 'execution_failed')
    assert len(created) == 1 and created[0]._emergency_taken
    assert 'PRIVATE_W07_FINALIZATION_FAILURE' not in str(stopped.value) + repr(stopped.value)


def test_complete_json_followed_by_real_markdown_cap_refuses_whole_invocation(
        monkeypatch, clock, invocation_source):
    boundary, created = _observe_invocation(monkeypatch)
    original = boundary._encode_markdown_report
    completed_json = []

    def no_markdown_space(document, port):
        owner = created[0]
        assert port._owner is owner and owner._json_output_bytes > 0
        completed_json.append(owner._json_output_bytes)
        port.charge_output('markdown', OUTPUT_LIMIT)
        return original(document, port)

    monkeypatch.setattr(boundary, '_encode_markdown_report', no_markdown_space)
    with pytest.raises(AuditAbort) as stopped:
        boundary._audit_value(invocation_source)
    _assert_public_abort(stopped.value, 'accepted')
    assert len(created) == len(completed_json) == 1
    assert counters(created[0]) == (completed_json[0], OUTPUT_LIMIT)
    assert created[0]._cause.limit_id == 'WU9-L14'


@pytest.mark.parametrize('after_commit', (False, True))
def test_local_job_stop_retains_only_atomically_committed_results_in_complete_report(
        monkeypatch, clock, invocation_source, after_commit):
    from source_integrity_toolkit.runtime import boundary
    control = json.loads(boundary._audit_value(invocation_source).to_json_bytes())
    boundary, created = _observe_invocation(monkeypatch)
    execute = boundary._execute_job
    calls = []

    def local_stop(prepared, spec, ledger, port):
        calls.append(spec.family)
        if len(calls) == 2:
            if after_commit:
                execute(prepared, spec, ledger, port)
                assert port._committed and port._committed[0]
            port.charge(1_000_000 - port.used + 1)
        return execute(prepared, spec, ledger, port)

    monkeypatch.setattr(boundary, '_execute_job', local_stop)
    delivered = boundary._audit_value(invocation_source)
    assert type(delivered) is report_contract.AuditReport and len(created) == 1
    document = json.loads(delivered.to_json_bytes())
    assert calls == ['SIT-M001', 'SIT-M002']
    assert document['run']['processing_state'] == 'interrupted'
    assert document['input_validation']['state'] == 'accepted'
    for family in calls[:2 if after_commit else 1]:
        actual = [row for row in document['results'] if row['diagnostic_id'] == family]
        expected = [row for row in control['results'] if row['diagnostic_id'] == family]
        assert [(row['field_key'], row['execution_state'], row['result_state'], row['value']) for row in actual] == [
            (row['field_key'], row['execution_state'], row['result_state'], row['value']) for row in expected]
    uncompleted = [row for row in document['results']
                   if row['diagnostic_id'] not in calls[:2 if after_commit else 1]]
    assert uncompleted and all(row['result_state'] == 'not_evaluated' and row['value'] is None for row in uncompleted)
    assert all(row['execution_state'] == ('interrupted' if row['diagnostic_id'] == calls[1]
                                         else 'not_performed') for row in uncompleted)
    assert created[0]._cause.limit_id == 'WU9-L11' and created[0]._stop_kind == 'job'
    assert counters(created[0]) == (len(delivered.to_json_bytes()), len(delivered.to_markdown_bytes()))


@pytest.mark.parametrize('later', ('output', 'failure'))
def test_first_witness_stop_survives_later_finalization_failure_in_actual_invocation(
        monkeypatch, clock, invocation_source, later):
    boundary, created = _observe_invocation(monkeypatch)
    execute = boundary._execute_job
    calls, first_causes = [], []

    def witness_stop(prepared, spec, ledger, port):
        calls.append(spec.family)
        if len(calls) == 2:
            try:
                ledger.reserve(witnesses=20_001)
            except _AnalysisAborted as stopped:
                first_causes.append(stopped)
                raise
        return execute(prepared, spec, ledger, port)

    def later_failure(document, port):
        assert first_causes and port._owner._cause is first_causes[0]
        if later == 'output':
            port.charge_output('markdown', OUTPUT_LIMIT + 1)
        raise RuntimeError('PRIVATE_SECONDARY_FAILURE')

    monkeypatch.setattr(boundary, '_execute_job', witness_stop)
    monkeypatch.setattr(boundary, '_encode_markdown_report', later_failure)
    with pytest.raises(AuditAbort) as stopped:
        boundary._audit_value(invocation_source)
    _assert_public_abort(stopped.value, 'accepted')
    assert len(created) == len(first_causes) == 1 and calls == ['SIT-M001', 'SIT-M002']
    assert created[0]._cause is first_causes[0] and first_causes[0].limit_id == 'WU9-L13'
    assert created[0]._json_output_bytes > 0 and created[0]._markdown_output_bytes == 0


@pytest.mark.parametrize('encoding', ('json', 'markdown'))
def test_same_length_semantic_encoding_corruption_blocks_whole_report_delivery(
        monkeypatch, clock, invocation_source, encoding):
    boundary, created = _observe_invocation(monkeypatch)
    name = '_encode_' + encoding + '_report'
    original = getattr(boundary, name)
    corrupted = []

    def changed(document, port):
        valid = original(document, port)
        assert b'not_recorded_by_SIT-RP-0.1' in valid
        invalid = valid.replace(b'not_recorded_by_SIT-RP-0.1', b'NOT_recorded_by_SIT-RP-0.1', 1)
        assert invalid != valid and len(invalid) == len(valid)
        corrupted.append((valid, invalid))
        return invalid

    monkeypatch.setattr(boundary, name, changed)
    with pytest.raises(AuditAbort) as stopped:
        boundary._audit_value(invocation_source)
    _assert_public_abort(stopped.value, 'accepted', 'execution_failed')
    assert len(created) == len(corrupted) == 1
    assert all(count > 0 for count in counters(created[0]))


@pytest.mark.parametrize('counter,maximum', (('witnesses', 20_000), ('members', 100_000)))
@pytest.mark.parametrize('pending', (False, True))
def test_formal_witness_additions_share_private_pending_and_retained_fixed_ceiling(
        clock, counter, maximum, pending):
    owner = resources._new_analysis_budget()
    owner.record_input_acceptance()  # Trusted component setup for actual quota arithmetic.
    job = owner.start_job()
    ledger = owner.witnesses
    token = ledger.reserve(**{counter: maximum - 1})
    if not pending:
        ledger.retain(token)
    owner.finish_job(job)
    finalizer = owner.begin_finalization()
    port = owner.begin_report_encoding(finalizer)
    before = (ledger._reserved_witnesses, ledger._reserved_members,
              ledger._retained_witnesses, ledger._retained_members)
    port.reserve_report_witness(0, 0)  # Exact reuse has no additional retained occurrence.
    assert owner._witness_ledger is ledger
    assert (ledger._reserved_witnesses, ledger._reserved_members,
            ledger._retained_witnesses, ledger._retained_members) == before
    addition = (1, 0) if counter == 'witnesses' else (0, 1)
    port.reserve_report_witness(*addition)
    count = (ledger._reserved_witnesses + ledger._retained_witnesses if counter == 'witnesses'
             else ledger._reserved_members + ledger._retained_members)
    assert count == maximum
    retained = (ledger._retained_witnesses, ledger._retained_members)
    with pytest.raises(_AnalysisAborted) as stopped:
        port.reserve_report_witness(*addition)
    assert stopped.value.limit_id == 'WU9-L13'
    assert (ledger._retained_witnesses, ledger._retained_members) == retained
    assert owner._witness_ledger is ledger and owner._start == 100
    public = diagnostics._emergency_report_abort(owner)
    _assert_public_abort(public, 'accepted')


def test_owned_mapping_order_cache_hit_is_charged_and_encoding_still_visits_values(
        monkeypatch, clock):
    owner, _, real = encoding_context()
    value = report_contract._copy_report_value({'z': 'second', 'a': 'first'}, real)
    assert type(value) is report_contract._ReportMapping
    comparisons = []
    compare = escaping._compare_text

    def observed_compare(left, right, port):
        comparisons.append((left, right))
        return compare(left, right, port)

    monkeypatch.setattr(escaping, '_compare_text', observed_compare)
    wrapped = escaping._CachedEncodingPort(real)
    assert wrapped._owner is owner
    before = owner.used
    first = escaping._sorted_report_pairs(value, wrapped)
    assert first == (('a', 'first'), ('z', 'second'))
    assert comparisons and owner.used > before
    compared, before = len(comparisons), owner.used
    second = escaping._sorted_report_pairs(value, wrapped)
    assert second is first and owner.used > before
    assert len(comparisons) == compared and counters(owner) == (0, 0)
    expected = b'{"a":"first","z":"second"}'
    first_bytes = escaping._encode_j(value, wrapped)
    after_encoding = owner.used
    second_bytes = escaping._encode_j(value, wrapped)
    assert first_bytes == second_bytes == expected and owner.used > after_encoding
    assert len(comparisons) == compared
    assert counters(owner) == (2 * len(expected), 0)


def test_mapping_order_cache_is_local_to_wrapper_and_exact_owned_object(monkeypatch, clock):
    owner, _, real = encoding_context()
    left = report_contract._copy_report_value({'z': 'left-z', 'a': 'left-a'}, real)
    right = report_contract._copy_report_value({'z': 'right-z', 'a': 'right-a'}, real)
    assert type(left) is type(right) is report_contract._ReportMapping and left is not right
    comparisons = []
    compare = escaping._compare_text

    def observed_compare(first, second, port):
        comparisons.append((first, second))
        return compare(first, second, port)

    monkeypatch.setattr(escaping, '_compare_text', observed_compare)
    first_wrapper = escaping._CachedEncodingPort(real)
    left_pairs = escaping._sorted_report_pairs(left, first_wrapper)
    compared, before = len(comparisons), owner.used
    right_pairs = escaping._sorted_report_pairs(right, first_wrapper)
    assert right_pairs == (('a', 'right-a'), ('z', 'right-z'))
    assert right_pairs is not left_pairs and len(comparisons) > compared and owner.used > before
    second_wrapper = escaping._CachedEncodingPort(real)
    compared, before = len(comparisons), owner.used
    second_pairs = escaping._sorted_report_pairs(left, second_wrapper)
    assert second_pairs == left_pairs and second_pairs is not left_pairs
    assert len(comparisons) > compared and owner.used > before
    assert first_wrapper._owner is second_wrapper._owner is owner
    assert escaping._sorted_report_pairs(left, first_wrapper) is left_pairs


def test_new_invocation_cannot_reuse_another_invocations_paid_mapping_order(monkeypatch, clock):
    first_owner, _, first_port = encoding_context()
    value = report_contract._copy_report_value({'z': 'second', 'a': 'first'}, first_port)
    first_wrapper = escaping._CachedEncodingPort(first_port)
    first_pairs = escaping._sorted_report_pairs(value, first_wrapper)
    before_first = first_owner.used
    second_owner, _, second_port = encoding_context()
    assert second_owner is not first_owner
    second_wrapper = escaping._CachedEncodingPort(second_port)
    comparisons = []
    compare = escaping._compare_text

    def observed_compare(left, right, port):
        comparisons.append((left, right))
        assert port._owner is second_owner
        return compare(left, right, port)

    monkeypatch.setattr(escaping, '_compare_text', observed_compare)
    before_second = second_owner.used
    second_pairs = escaping._sorted_report_pairs(value, second_wrapper)
    assert second_pairs == first_pairs and second_pairs is not first_pairs
    assert comparisons and second_owner.used > before_second
    assert first_owner.used == before_first
    assert first_wrapper._owner is first_owner and second_wrapper._owner is second_owner
    assert counters(first_owner) == counters(second_owner) == (0, 0)
