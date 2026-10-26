# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""P4-W05 exact JSON controls against independent bytes and literal rules.

The full reference is the existing W02 independent golden. Small expectations
below follow architecture 17.2, 17.3 and 18.3 directly; no product output is
recorded as an expectation. The real private analysis is followed by W04's
selector/assembler and W05's encoder. This does not exercise the future W07
single analytical invocation or deliver a public AuditReport.
"""
import copy
from decimal import Decimal
import json
from pathlib import Path

import pytest

from source_integrity_toolkit.contracts.bundle import _Array, _Number, _Object
from source_integrity_toolkit.contracts.report import (
    _AnalyticalOutcome, _ReportContractError, _ReportMapping,
)
from source_integrity_toolkit.reporting.escaping import _encode_j
from source_integrity_toolkit.reporting.json_report import _encode_json_report
from source_integrity_toolkit.runtime.boundary import _analyze_value
from source_integrity_toolkit.runtime.disclosure import _assemble_selected_report
from test_report_test_oracles import _assert_reference_json


ROOT = Path(__file__).resolve().parents[2]


class JsonPort:
    """Finite test-owned component port, never a public invocation option."""
    def __init__(self):
        self.units = 0
        self.checks = 0
        self.output = {'json': 0, 'markdown': 0}

    def charge(self, units):
        assert type(units) is int and units >= 0
        assert self.units + units <= 10_000_000, 'component work limit'
        self.units += units

    def check(self):
        self.checks += 1

    def charge_output(self, encoding, byte_count):
        assert type(encoding) is str and encoding in self.output
        assert type(byte_count) is int and byte_count >= 0
        assert self.output[encoding] + byte_count <= 67_108_864
        self.output[encoding] += byte_count


def _j(value):
    port = JsonPort()
    raw = _encode_j(value, port)
    assert type(raw) is bytes
    assert port.output == {'json': len(raw), 'markdown': 0}
    assert 0 < port.units <= 10_000_000 and port.checks > 0
    return raw


def test_actual_selected_report_matches_independent_reference_bytes():
    fixture = json.loads((ROOT / 'tests/fixtures/micro/phase4_public_cases.json').read_bytes())
    assert fixture['cases'][0]['id'] == 'P4-REFERENCE-ONE-ORIGIN'
    dossier = fixture['cases'][0]['dossier']
    original = copy.deepcopy(dossier)
    outcome = _analyze_value(dossier)
    assert type(outcome) is _AnalyticalOutcome
    assert outcome.execution_state == 'completed' and len(outcome.results) == 78
    assert dossier == original

    port = JsonPort()
    document = _assemble_selected_report(outcome, port)
    before_encoding = port.units
    raw = _encode_json_report(document, port)
    expected = (ROOT / 'tests/golden/phase4_reference_report.json').read_bytes()
    assert type(document) is _ReportMapping
    assert raw == expected
    _assert_reference_json(raw)
    assert port.output == {'json': len(expected), 'markdown': 0}
    assert before_encoding < port.units <= 10_000_000
    assert raw.endswith(b'\n') and not raw.endswith(b'\n\n')
    assert not raw.startswith(b'\xef\xbb\xbf') and b'\r' not in raw
    assert dossier == original


def test_report_wrapper_adds_exactly_one_lf_to_j():
    # A project-owned component root isolates framing from the full reference.
    value = _ReportMapping((('z', 'last\n'), ('a', True)))
    port = JsonPort()
    raw = _encode_json_report(value, port)
    assert raw == b'{"a":true,"z":"last\\u000a"}\n'
    assert port.output == {'json': len(raw), 'markdown': 0}
    assert _j(value) == raw[:-1]


@pytest.mark.parametrize(('value', 'expected'), (
    (None, b'null'), (True, b'true'), (False, b'false'),
    (0, b'0'), (1, b'1'), (-1, b'-1'),
    (9007199254740991, b'9007199254740991'),
    (-9007199254740991, b'-9007199254740991'),
    ('', b'""'), ((), b'[]'), (_ReportMapping(()), b'{}'),
    ((True, 1, False, 0, None), b'[true,1,false,0,null]'),
))
def test_exact_scalar_types_and_empty_containers(value, expected):
    assert _j(value) == expected


def test_keys_use_unicode_scalar_order_without_normalization():
    pairs = (('\U00010000', 9), ('\ue000', 8), ('é', 7), ('e\u0301', 6),
             ('a', 5), ('A', 4), ('/', 3), ('"', 2), ('\n', 1))
    value = _ReportMapping(pairs)
    expected = ('{"\\u000a":1,"\\\"":2,"/":3,"A":4,"a":5,'
                '"e\u0301":6,"é":7,"\ue000":8,"\U00010000":9}').encode('utf-8')
    assert _j(value) == expected
    assert value._pairs is pairs
    assert _j(_ReportMapping(tuple(reversed(pairs)))) == expected


ESCAPED_CODEPOINTS = (
    *range(0x00, 0x20), *range(0x7F, 0xA0), 0x061C, 0x200E, 0x200F,
    *range(0x2028, 0x202F), *range(0x2066, 0x206A),
)


@pytest.mark.parametrize('codepoint', ESCAPED_CODEPOINTS,
                         ids=lambda value: 'U+' + format(value, '04X'))
def test_every_required_control_scalar_has_lowercase_long_escape(codepoint):
    expected = ('"\\u' + format(codepoint, '04x') + '"').encode('ascii')
    assert _j(chr(codepoint)) == expected


@pytest.mark.parametrize('codepoint', (
    0x20, 0x7E, 0xA0, 0x061B, 0x061D, 0x200D, 0x2010, 0x2027,
    0x202F, 0x2065, 0x206A, 0xFEFF, 0x10000, 0x10FFFF,
), ids=lambda value: 'U+' + format(value, '04X'))
def test_allowed_scalars_adjacent_to_control_ranges_keep_utf8(codepoint):
    text = chr(codepoint)
    assert _j(text) == b'"' + text.encode('utf-8') + b'"'


def test_quotes_backslash_slash_multilingual_and_combining_forms():
    value = ('"\\/\n', '中文 العربية Ελληνικά 日本語 😀', 'é', 'e\u0301')
    expected = ('["\\\"\\\\/\\u000a","中文 العربية Ελληνικά 日本語 😀",'
                '"é","e\u0301"]').encode('utf-8')
    raw = _j(value)
    assert raw == expected
    assert _j('/') == b'"/"' and b'\\n' not in raw
    assert json.loads(raw) == list(value)


@pytest.mark.parametrize(('atom', 'expected'), (
    (_Number(0, '0', 0, 'decimal'), b'0'),
    (_Number(1, '5', -1, 'decimal'), b'0.5'),
    (_Number(1, '5', -1, 'binary_float'), b'0.5'),
    (_Number(-1, '5', -1, 'decimal'), b'-0.5'),
    (_Number(1, '1', -2, 'decimal'), b'0.01'),
    (_Number(1, '1', -3, 'decimal'), b'1e-3'),
    (_Number(1, '1', -4, 'decimal'), b'1e-4'),
    (_Number(1, '123', -2, 'decimal'), b'1.23'),
    (_Number(1, '1', 3, 'decimal'), b'1000'),
    (_Number(1, '9007199254740991', 0, 'integer'), b'9007199254740991'),
    (_Number(-1, '9007199254740991', 0, 'integer'), b'-9007199254740991'),
    (_Number(1, '1', -1000000, 'decimal'), b'1e-1000000'),
    (_Number(1, '1', -int('9' * 124), 'decimal'), b'1e-' + b'9' * 124),
    (_Number(-1, '1', -int('9' * 124), 'decimal'), b'-1e-' + b'9' * 124),
    (_Number(1, '1000000000000000055511151231257827021181583404541015625',
             -55, 'binary_float'),
     b'0.1000000000000000055511151231257827021181583404541015625'),
), ids=('zero', 'half', 'binary_half', 'negative_half', 'ordinary_tie', 'short_exponent',
        'tiny', 'decimal_point', 'integral_exponent', 'max_integer',
        'min_integer', 'very_small', 'huge_negative_exponent',
        'maximal_exact_token', 'exact_binary_tenth'))
def test_exact_private_atoms_use_literal_shortest_representations(atom, expected):
    assert _j(atom) == expected


def test_original_fractions_ordered_arrays_and_duplicate_occurrences_survive():
    fraction = _ReportMapping((('numerator', 26), ('denominator', 36)))
    value = _ReportMapping((('fraction', fraction), ('ordered', ('third', 'first', 'first'))))
    raw = _j(value)
    assert raw == (b'{"fraction":{"denominator":36,"numerator":26},'
                   b'"ordered":["third","first","first"]}')
    assert b'display_decimal' not in raw and b'0.722222' not in raw
    assert fraction._pairs == (('numerator', 26), ('denominator', 36))


class Hostile:
    calls = []

    def _touch(self, *args, **kwargs):
        self.calls.append('custom_protocol')
        raise AssertionError('custom protocol was invoked')

    __repr__ = __str__ = __iter__ = __len__ = __getitem__ = _touch
    __eq__ = __hash__ = __int__ = __float__ = _touch

    def default(self, *args):
        return self._touch()


class HostileString(str):
    def __str__(self):
        return Hostile()._touch()

    def __iter__(self):
        return Hostile()._touch()


class HostileInt(int):
    def __repr__(self):
        return Hostile()._touch()

    def __str__(self):
        return Hostile()._touch()

    def __int__(self):
        return Hostile()._touch()


@pytest.mark.parametrize(('label', 'value'), (
    ('object', Hostile()), ('string_subclass', HostileString('secret')),
    ('int_subclass', HostileInt(7)), ('decimal', Decimal('0.1')),
    ('float', 0.5), ('nan', float('nan')), ('infinity', float('inf')),
    ('mutable_list', []), ('mutable_dict', {}), ('bytes', b'secret'),
    ('private_source_object', _Object(())), ('private_source_array', _Array(())),
), ids=('object', 'string_subclass', 'int_subclass', 'decimal', 'float',
        'nan', 'infinity', 'mutable_list', 'mutable_dict', 'bytes',
        'private_source_object', 'private_source_array'))
def test_encoder_rejects_untrusted_types_before_custom_protocols(label, value):
    Hostile.calls.clear()
    with pytest.raises(_ReportContractError, match='^invalid_report_contract$'):
        _encode_j(value, JsonPort())
    assert Hostile.calls == []


@pytest.mark.parametrize(('label', 'value'), (
    ('high_int', 9007199254740992), ('low_int', -9007199254740992),
    ('surrogate_high', '\ud800'), ('surrogate_low', '\udfff'),
    ('duplicate_keys', _ReportMapping((('a', 1), ('a', 2)))),
    ('hostile_key', _ReportMapping(((Hostile(), 1),))),
    ('hostile_child', _ReportMapping((('a', Hostile()),))),
    ('hostile_array_child', (Hostile(),)),
    ('large_atom', _Number(1, '9007199254740992', 0, 'decimal')),
    ('oversize_atom_token', _Number(1, '1', -int('9' * 126), 'decimal')),
), ids=('high_int', 'low_int', 'surrogate_high', 'surrogate_low',
        'duplicate_keys', 'hostile_key', 'hostile_child',
        'hostile_array_child', 'large_atom', 'oversize_atom_token'))
def test_invalid_trusted_components_fail_without_values_in_exception(label, value):
    Hostile.calls.clear()
    with pytest.raises(_ReportContractError) as caught:
        _encode_j(value, JsonPort())
    assert str(caught.value) == 'invalid_report_contract'
    assert Hostile.calls == []


def test_report_entry_requires_frozen_project_root():
    Hostile.calls.clear()
    for value in ({}, (), None, Hostile()):
        with pytest.raises(_ReportContractError, match='^invalid_report_contract$'):
            _encode_json_report(value, JsonPort())
    assert Hostile.calls == []
