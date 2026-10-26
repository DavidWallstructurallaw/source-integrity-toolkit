# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: REPORT_PRESENTATION. Fixed bounded Markdown of the frozen report.

Governance 22.2 selects the exact framing. Both renderers consume the same
already selected document. Source text occurs only inside pretty-J blocks;
headings and display lines use checked report identifiers or registered values.
No source projection, analysis, runtime context or public report is created.
"""
from ..contracts.bundle import _compare_text
from ..contracts.execution import _byte_work
from ..contracts.report import _ReportMapping, _REPORT_ROOT_FIELDS
from ..contracts.results import FIELD_BINDINGS
from .escaping import (
    _JWriter, _CheckingWriter, _require, _sorted_report_pairs, _fence_length,
    _repeat_syntax, _write_pretty_j, _MAX_INTEGER,
)


def _fields(value, port):
    """Build a charged local lookup only after exact keys and uniqueness."""
    port.charge(1)
    fields = {}
    _require(type(value) is _ReportMapping)
    for key, child in _sorted_report_pairs(value, port):
        _byte_work(port, len(key) * 4, 3)
        fields[key] = child
    port.check()
    return fields


def _member(fields, name, port):
    _byte_work(port, len(name), 2)
    _require(name in fields)
    return fields[name]


def _token(value, allowed, port):
    _require(type(value) is str)
    for token in allowed:
        _byte_work(port, 4 * (len(value) + len(token)), 1)
        if value == token:
            return token
    _require(False)


def _identifier(value, prefix, port):
    _require(type(value) is str)
    _byte_work(port, len(prefix), 2)
    _require(len(value) >= len(prefix) + 6 and value.startswith(prefix))
    nonzero = False
    for start in range(len(prefix), len(value), 64):
        size = min(64, len(value) - start)
        _byte_work(port, size * 4, 1)
        block = value[start:start + size]
        _byte_work(port, size * 4, size + 1)
        for char in block:
            _require('0' <= char <= '9')
            nonzero = nonzero or char != '0'
        port.check()
    _require(nonzero)
    return value


def _field_key(value, port):
    _require(type(value) is str)
    for _, field, _ in FIELD_BINDINGS:
        _byte_work(port, 4 * (len(value) + len(field)), 2)
        if value == field:
            return field
    _require(False)


def _ascii(writer, value):
    """Only checked identifiers or tool-owned tokens reach this helper."""
    length = len(value)
    writer._reserve(length)
    _byte_work(writer._port, length, 2)
    fragment = value.encode('ascii')
    writer._port.check()
    writer._retain(fragment)


def _block(writer, value, *, last=False):
    length = _fence_length(value, writer._port)
    _repeat_syntax(writer, b'`', length)
    writer.literal(b'json\n')
    _write_pretty_j(writer, value)
    writer.literal(b'\n')
    _repeat_syntax(writer, b'`', length)
    writer.literal(b'\n' if last else b'\n\n')


def _reason_index(reasons, port):
    _require(type(reasons) is tuple)
    port.charge(1)
    pairs = []
    for position, reason in enumerate(reasons):
        port.charge(1)
        fields = _fields(reason, port)
        key = _identifier(_member(fields, 'id', port), 'SIT-RSN-', port)
        port.charge(3)
        pairs.append((key, (position, reason)))
    port.charge(len(pairs) + 2)
    return _sorted_report_pairs(_ReportMapping(tuple(pairs)), port)


def _reason_details(refs, reasons, index, port):
    """Resolve with bounded binary search; retain canonical root Reason order."""
    _require(type(refs) is tuple)
    port.charge(len(reasons) + 1)
    selected = [False] * len(reasons)
    for ref in refs:
        port.charge(1)
        _identifier(ref, 'SIT-RSN-', port)
        lower, upper, found = 0, len(index), False
        while lower < upper:
            port.charge(1)
            middle = (lower + upper) // 2
            key, item = index[middle]
            comparison = _compare_text(ref, key, port)
            if comparison < 0:
                upper = middle
            elif comparison > 0:
                lower = middle + 1
            else:
                port.charge(2)
                position, _ = item
                _require(not selected[position])
                selected[position] = True
                found = True
                break
        _require(found)
    port.charge(1)
    result = []
    for position, reason in enumerate(reasons):
        port.charge(1)
        if selected[position]:
            port.charge(1)
            result.append(reason)
    port.charge(len(result) + 1)
    result = tuple(result)
    port.check()
    return result


def _decimal_display(writer, fraction):
    port = writer._port
    fields = _fields(fraction, port)
    numerator = _member(fields, 'numerator', port)
    denominator = _member(fields, 'denominator', port)
    port.charge(4)
    _require(type(numerator) is int and type(denominator) is int)
    _require(0 <= numerator <= _MAX_INTEGER and 0 < denominator <= _MAX_INTEGER)
    # Portable operands bound all intermediate decimal lengths to 23 digits.
    # Each multiplication/division/rounding step is charged before arithmetic.
    _byte_work(port, 128, 1)
    scaled = numerator * 1_000_000
    _byte_work(port, 128, 2)
    quotient, remainder = divmod(scaled, denominator)
    _byte_work(port, 128, 1)
    round_up = remainder * 2 >= denominator
    if round_up:
        _byte_work(port, 128, 1)
        quotient += 1
    _byte_work(port, 128, 2)
    whole, decimal = divmod(quotient, 1_000_000)
    writer.literal(b'Decimal display: ')
    writer.integer(numerator)
    writer.literal(b'/')
    writer.integer(denominator)
    writer.literal(b' = ')
    writer.integer(whole)
    writer.literal(b'.')
    writer._reserve(6)
    _byte_work(port, 18, 3)
    fragment = str(decimal).zfill(6).encode('ascii')
    port.check()
    writer._retain(fragment)
    writer.literal(b'\n\n')


def _encode_markdown_report(document, port):
    """Return exact complete Markdown bytes, or propagate a bounded stop.

    Only this one immutable document supplies both ordinary sections and
    repeated Result/Reason details. No partial bytes or report escape failure.
    """
    return _write_markdown_report(document, port, _JWriter(port, 'markdown'))


def _verify_markdown_report(document, encoded, port):
    """Check all framing and scalar content, including repeated details."""
    _write_markdown_report(document, port, _CheckingWriter(port, 'markdown', encoded))


def _write_markdown_report(document, port, writer):
    fields = _fields(document, port)
    port.charge(len(_REPORT_ROOT_FIELDS) + 1)
    _require(len(fields) == len(_REPORT_ROOT_FIELDS))
    for name in _REPORT_ROOT_FIELDS:
        _member(fields, name, port)
    kind = _token(_member(fields, 'report_kind', port),
                  ('audit_report', 'validation_diagnostics', 'processing_diagnostics'), port)
    run = _fields(_member(fields, 'run', port), port)
    processing = _token(_member(run, 'processing_state', port),
                        ('completed', 'interrupted', 'rejected', 'failed'), port)
    admission = _fields(_member(fields, 'input_validation', port), port)
    state = _token(_member(admission, 'state', port),
                   ('accepted', 'rejected', 'not_completed'), port)
    reasons = _member(fields, 'reasons', port)
    index = _reason_index(reasons, port)
    results = _member(fields, 'results', port)
    _require(type(results) is tuple)
    writer.literal(b'# Source Integrity Audit\n\nReport kind: ')
    _ascii(writer, kind)
    writer.literal(b'\nProcessing state: ')
    _ascii(writer, processing)
    writer.literal(b'\nInput state: ')
    _ascii(writer, state)
    writer.literal(b'\n\n')
    for position, name in enumerate(_REPORT_ROOT_FIELDS):
        port.charge(1)
        writer.literal(b'## ')
        _ascii(writer, name)
        writer.literal(b'\n\n')
        if name != 'results' or not results:
            _block(writer, _member(fields, name, port),
                   last=position == len(_REPORT_ROOT_FIELDS) - 1)
            continue
        for result in results:
            port.charge(1)
            row = _fields(result, port)
            identifier = _identifier(_member(row, 'id', port), 'SIT-RES-', port)
            field = _field_key(_member(row, 'field_key', port), port)
            writer.literal(b'### ')
            _ascii(writer, identifier)
            writer.literal(b': ')
            _ascii(writer, field)
            writer.literal(b'\n\n')
            _block(writer, result)
            result_state = _token(_member(row, 'result_state', port),
                                  ('available', 'unavailable', 'not_applicable', 'not_evaluated'), port)
            value_kind = _token(_member(row, 'value_kind', port),
                                ('count', 'fraction', 'completion_interval', 'partition',
                                 'incidence', 'record_disclosures', 'witness_collection'), port)
            if result_state == 'available' and value_kind == 'fraction':
                _decimal_display(writer, _member(row, 'value', port))
            writer.literal(b'Reason details\n\n')
            details = _reason_details(_member(row, 'reason_refs', port), reasons, index, port)
            _block(writer, details)
    return writer.finish()
