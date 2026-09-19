# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Bounded supplied-byte capture; no file-interface or accepted-input claim."""
import json
from dataclasses import fields
from unittest.mock import patch
import pytest
from source_integrity_toolkit.runtime.boundary import _prepare_utf8, _prepare_value
from source_integrity_toolkit.runtime.resources import _new_budget
from source_integrity_toolkit.runtime.diagnostics import _SafeDiagnostic
from source_integrity_toolkit.contracts.bundle import _CapturedBundle, _Array, _Object, _Number
from source_integrity_toolkit.contracts.execution import _PreparationAborted
from source_integrity_toolkit.io.input_file import _preflight, _decode_utf8
from source_integrity_toolkit.validation.limits import _InputLedger


def tag(value):
    if type(value) is _Object:
        return ("object", tuple((k, tag(v)) for k, v in value.items))
    if type(value) is _Array:
        return ("array", tuple(tag(v) for v in value.items))
    if type(value) is _Number:
        return ("number", value.sign, value.coefficient, value.exponent)
    return (type(value).__name__, value)


@pytest.mark.parametrize("source", [
    {}, {"b": 2, "a": 1}, {"null": None, "bool": False, "array": [], "object": {}},
    {"text": "中文 café 🚀"}, {"escapes": "\"\\/\b\f\n\r\t\x00\u202e"},
    {"A": 1, "a": 2, "é": "é", "e\u0301": "e\u0301"},
    {"unknown": {"ordered": [3, 1, 2]}, "states": ["failed", "denied", "inactive"]},
    {"numbers": [0, -0.0, 0.5, 1.25, -8, 9007199254740991]},
])
@pytest.mark.parametrize("ascii_only", [False, True])
def test_byte_and_value_capture_have_equal_content_for_exact_values(source, ascii_only):
    raw = json.dumps(source, ensure_ascii=ascii_only, separators=(",", ":")).encode()
    a, b = _prepare_utf8(raw), _prepare_value(source)
    assert type(a) is _CapturedBundle and type(b) is _CapturedBundle
    assert a.source_mode == "supplied_utf8" and b.source_mode == "constructed_value"
    assert tag(a.tree) == tag(b.tree)
    assert {f.name for f in fields(a)} == {"tree", "source_mode"}


@pytest.mark.parametrize("raw", [
    b"", b" ", b"{", b"[", b'{"a":}', b'{"a" 1}', b'{"a":1,}', b'{,"a":1}',
    b'{"a":[1,]}', b'{"a":[,1]}', b'{"a":[1 2]}', b'{"a":01}', b'{"a":+1}',
    b'{"a":1.}', b'{"a":.1}', b'{"a":1e}', b'{"a":1e+}', b'{"a":--1}',
    b'{"a":NaN}', b'{"a":Infinity}', b'{"a":-Infinity}', b'{"a":undefined}',
    b'{"a":True}', b'{"a":falseX}', b'{"a":"x}', b'{"a":"\\x00"}',
    b'{"a":"\\uqqqq"}', b'{"a":"\n"}', b'{"a":1}garbage', b'{}{}', b'{}\0',
    b'{}/*comment*/', b'\xef\xbb\xbf{}', '{}\u00a0'.encode(),
])
def test_invalid_grammar_never_reaches_full_decoder(raw):
    with patch("source_integrity_toolkit.io.input_file.json.loads", side_effect=AssertionError("decoder_called")) as decoder:
        outcome = _prepare_utf8(raw)
    assert decoder.call_count == 0
    assert type(outcome) is _SafeDiagnostic and outcome.input_state == "rejected"
    assert outcome.code == "invalid_syntax"


@pytest.mark.parametrize("raw", [b'{"a":"\xff"}', b'{"a":"\xc0\xaf"}', b'{"a":"\xed\xa0\x80"}',
    b'{"a":"\xf4\x90\x80\x80"}', b'{"a":"\xe2\x82"}', b'\xff\xfe{\x00}\x00'])
def test_invalid_utf8_cannot_be_replaced_or_autodetected(raw):
    with patch("source_integrity_toolkit.io.input_file.json.loads") as decoder:
        result = _prepare_utf8(raw)
    assert decoder.call_count == 0 and result.code == "invalid_syntax"


@pytest.mark.parametrize("raw", [b'{"a":"\\ud800"}', b'{"a":"\\udc00"}',
    b'{"a":"\\ud800\\u0041"}', b'{"a":"\\ud800x"}', b'{"\\udfff":0}'])
def test_lone_surrogates_are_specific_scalar_constraint_rejections(raw):
    result = _prepare_utf8(raw)
    assert result.code == "input_constraint_violation" and result.input_state == "rejected"
    assert "17.2" in result.qualifications[0]


@pytest.mark.parametrize("raw", [b'{"a":1,"a":2}', b'{"a":1,"\\u0061":2}',
    b'{"x":{"b":null,"b":true}}', '{"𝄞":1,"\\ud834\\udd1e":2}'.encode(),
    b'{"":{},"":[]}'])
def test_duplicate_keys_are_checked_after_escape_decoding(raw):
    result = _prepare_utf8(raw)
    assert result.input_state == "rejected" and result.code == "duplicate_key"


@pytest.mark.parametrize("raw", [b"[]", b"null", b"1", b"true", b'"text"'])
def test_valid_nonobject_root_is_still_outside_bundle_capture_domain(raw):
    assert _prepare_utf8(raw).code == "type_or_enum_violation"


@pytest.mark.parametrize("token", ["9007199254740992", "-9007199254740992", "9.007199254740992e15", "1e999999999999999"])
def test_integral_magnitude_is_rejected_before_expansion(token):
    outcome = _prepare_utf8(('{"x":' + token + '}').encode())
    assert outcome.code == "input_constraint_violation" and "8.2" in outcome.qualifications[0]


def test_exact_decimal_tail_and_source_category_are_preserved():
    parsed = _prepare_utf8(b'{"a":0.1,"b":0.50,"c":1.0,"d":1e-99999999999999999999}')
    values = dict(parsed.tree.items)
    assert (values["a"].coefficient, values["a"].exponent, values["a"].source_kind) == ("1", -1, "decimal")
    assert tag(values["a"]) != tag(dict(_prepare_value({"a":0.1}).tree.items)["a"])
    assert tag(values["b"]) == tag(dict(_prepare_value({"b":0.5}).tree.items)["b"])
    assert values["c"].source_kind == "decimal" and values["c"].exponent == 0
    assert values["d"].exponent == -99999999999999999999


@pytest.mark.parametrize("length", [127, 128, 129])
def test_raw_number_token_guard_is_resource_classified(length):
    token = "0e-" + "0" * (length - 4) + "1"
    result = _prepare_utf8(('{"x":' + token + '}').encode())
    if length <= 128:
        assert type(result) is _CapturedBundle
    else:
        assert result.code == "resource_limit_reached" and result.qualifications == ("WU9-L09",)


@pytest.mark.parametrize("levels", [31, 32, 33, 2000])
def test_container_depth_is_bounded_before_json_tree_allocation(levels):
    raw = b'{"x":' + b'[' * (levels - 1) + b']' * (levels - 1) + b'}'
    if levels <= 32:
        assert type(_prepare_utf8(raw)) is _CapturedBundle
    else:
        with patch("source_integrity_toolkit.io.input_file.json.loads") as decoder:
            outcome = _prepare_utf8(raw)
        assert decoder.call_count == 0 and outcome.qualifications == ("WU9-L02",)


@pytest.mark.parametrize("count", [65535, 65536, 65537])
@pytest.mark.parametrize("escaped", [False, True])
def test_decoded_string_ceiling_counts_decoded_bytes(count, escaped):
    value = b'\\u0061' * count if escaped else b'a' * count
    result = _prepare_utf8(b'{"x":"' + value + b'"}')
    if count <= 65536:
        assert type(result) is _CapturedBundle and len(dict(result.tree.items)["x"]) == count
    else:
        assert result.code == "input_constraint_violation" and "string/key" in result.qualifications[0]


@pytest.mark.parametrize("delta", [-1, 0, 1])
def test_whitespace_affects_only_actual_raw_transport_size(delta):
    raw = b'{}' + b' ' * (16_777_216 + delta - 2)
    b = _new_budget()
    ledger = _InputLedger(b, "supplied_utf8")
    if delta <= 0:
        result = _decode_utf8(raw, ledger)
        assert type(result) is _CapturedBundle
        assert ledger.snapshot()[0] == len(raw)
    else:
        with pytest.raises(_PreparationAborted) as raised:
            _decode_utf8(raw, ledger)
        assert raised.value.limit_id == "WU9-L01"


def test_preflight_value_node_count_excludes_keys_and_decoder_does_not_double_count():
    b = _new_budget(); ledger = _InputLedger(b, "supplied_utf8")
    result = _decode_utf8(b'{"a":[true,null,{}],"b":"x"}', ledger)
    assert type(result) is _CapturedBundle and ledger.snapshot()[6] == 6
    assert ledger.snapshot()[7] == 3


def test_preflight_node_stop_prevents_full_decode():
    b = _new_budget(); ledger = _InputLedger(b, "supplied_utf8")
    ledger.add("nodes", 499999)
    with patch("source_integrity_toolkit.io.input_file.json.loads") as decoder:
        with pytest.raises(_PreparationAborted) as raised:
            _decode_utf8(b'{"a":[]}', ledger)
    assert raised.value.limit_id == "WU9-L08" and decoder.call_count == 0


def test_captured_unknown_fields_are_not_falsely_claimed_schema_valid():
    result = _prepare_utf8(b'{"not_a_declared_field":1,"contract_version":"wrong"}')
    assert type(result) is _CapturedBundle
    assert not any(hasattr(result, k) for k in ("accepted", "is_valid", "results", "report_kind"))
