# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W03 scalar/J/index oracles. No full input, report or graph claim."""
from decimal import Decimal, localcontext
from fractions import Fraction
from dataclasses import FrozenInstanceError
from unittest.mock import patch
import random
import pytest
from source_integrity_toolkit.contracts.bundle import (
    _Number, _Array, _Object, _number_from_token, _number_from_builtin,
    _number_bytes, _j_scalar, _string_lengths, _sorted_pairs, _lookup_pair,
)
from source_integrity_toolkit.contracts.execution import _PreparationAborted
from source_integrity_toolkit.runtime.resources import _new_budget


@pytest.mark.parametrize("token,expected,kind", [
    ("0", b"0", "integer"), ("-0", b"0", "integer"),
    ("0.00", b"0", "decimal"), ("0.50", b"0.5", "decimal"),
    ("1e-4", b"1e-4", "decimal"), ("0.001", b"1e-3", "decimal"),
    ("0.01", b"0.01", "decimal"), ("1.2500", b"1.25", "decimal"),
    ("1.00e2", b"100", "decimal"), ("-1.25E+2", b"-125", "decimal"),
    ("123.450", b"123.45", "decimal"), ("1000", b"1000", "integer"),
    ("9007199254740991", b"9007199254740991", "integer"),
    ("-9007199254740991", b"-9007199254740991", "integer"),
])
def test_exact_token_spelling_and_source_category(token, expected, kind):
    budget = _new_budget()
    atom = _number_from_token(token, budget)
    assert atom.source_kind == kind
    assert _j_scalar(atom, budget) == expected
    assert Decimal(token) == Decimal(expected.decode())
    assert budget.input_state == "not_completed"


@pytest.mark.parametrize("token", ["", "+1", "01", "-01", "-", ".1", "1.", "1e", "1e+", "1e-", "1x", " 1", "1 ", "NaN", "Infinity", "0x1", "1_0", "١", "1.2.3", "--1"])
def test_malformed_numbers_never_default_or_coerce(token):
    with pytest.raises(_PreparationAborted) as raised:
        _number_from_token(token, _new_budget())
    assert raised.value.stop.input_state == "rejected"
    assert raised.value.diagnostic_code == "invalid_syntax"


@pytest.mark.parametrize("token", ["9007199254740992", "-9007199254740992", "9007199254740992.0", "1e999999999999999999999", "1" + "0" * 100])
def test_integral_range_is_structural_before_expansion(token):
    with pytest.raises(_PreparationAborted) as raised:
        _number_from_token(token, _new_budget())
    assert raised.value.stop.execution_state == "rejected"
    assert raised.value.constraint == "exact_integer_range"


@pytest.mark.parametrize("size", [127, 128, 129])
def test_raw_numeric_token_limit_is_resource_not_schema(size):
    token = "0." + "0" * (size - 3) + "1"
    budget = _new_budget()
    if size <= 128:
        assert _number_from_token(token, budget).coefficient == "1"
    else:
        with pytest.raises(_PreparationAborted) as raised:
            _number_from_token(token, budget)
        assert raised.value.limit_id == "WU9-L09"
        assert raised.value.stop.input_state == "not_completed"


def test_extreme_exponent_remains_compact_and_zero_never_expands():
    token = "1e-" + "9" * 125
    budget = _new_budget()
    atom = _number_from_token(token, budget)
    assert _j_scalar(atom, budget) == token.encode()
    assert budget.used < 10000
    assert _j_scalar(_number_from_token("0e" + "9" * 126, budget), budget) == b"0"
    with pytest.raises(_PreparationAborted) as raised:
        _number_from_token("1e-" + "9" * 126, _new_budget())
    assert raised.value.limit_id == "WU9-L09"


@pytest.mark.parametrize("value", [0.0, -0.0, 0.5, -1.25, 0.1, 1e-20, 123456.125])
def test_finite_binary_float_is_preserved_exactly(value):
    budget = _new_budget()
    atom = _number_from_builtin(value, budget)
    result = _j_scalar(atom, budget).decode()
    assert atom.source_kind == "binary_float"
    assert Decimal(result) == Decimal.from_float(value)
    assert Fraction(Decimal(result)) == Fraction(*value.as_integer_ratio())


def test_file_decimal_and_binary_float_remain_distinct():
    budget = _new_budget()
    a, b = _number_from_token("0.1", budget), _number_from_builtin(0.1, budget)
    assert _number_bytes(a, budget) != _number_bytes(b, budget)
    assert _number_bytes(_number_from_token("0.50", budget), budget) == _number_bytes(_number_from_builtin(0.5, budget), budget)


@pytest.mark.parametrize("value", [1e-100, 5e-324, -5e-324])
def test_exact_float_overlength_is_resource_stop_without_rounding(value):
    with pytest.raises(_PreparationAborted) as raised:
        _number_from_builtin(value, _new_budget())
    assert raised.value.limit_id == "WU9-L09"


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf"), True, False, Decimal("0.5"), "1", None])
def test_nonfinite_boolean_and_custom_numeric_types_are_rejected(value):
    with pytest.raises(_PreparationAborted) as raised:
        _number_from_builtin(value, _new_budget())
    assert raised.value.stop.execution_state == "rejected"


def test_huge_builtin_integer_is_rejected_without_str_or_abs_expansion():
    for value in (10 ** 10000, -(10 ** 10000)):
        with pytest.raises(_PreparationAborted) as raised:
            _number_from_builtin(value, _new_budget())
        assert raised.value.constraint == "exact_integer_range"


def test_finite_numeric_oracles_do_not_depend_on_decimal_context():
    rng = random.Random(3203)
    for _ in range(180):
        coefficient = rng.randint(-999999, 999999)
        exponent = rng.randint(-24, 3)
        token = str(coefficient) + "e" + str(exponent)
        with localcontext() as context:
            context.prec = 2
            context.Emin, context.Emax = -2, 2
            budget = _new_budget()
            text = _j_scalar(_number_from_token(token, budget), budget).decode()
        assert Decimal(text) == Decimal(token)
        assert len(text) <= len(token) or "e" not in text


@pytest.mark.parametrize("value,expected", [
    (None,b"null"), (True,b"true"), (False,b"false"), ("",b'""'),
    ("é", '"é"'.encode()), ("😀", '"😀"'.encode()),
    ("a/b",b'"a/b"'), ('"',b'"\\\""'), ("\\",b'"\\\\"'),
    ("\n",b'"\\u000a"'), ("\x00",b'"\\u0000"'),
    ("\x7f",b'"\\u007f"'), ("\u009f",b'"\\u009f"'),
    ("\u061c",b'"\\u061c"'), ("\u200e",b'"\\u200e"'),
    ("\u2028",b'"\\u2028"'), ("\u202e",b'"\\u202e"'),
    ("\u2066",b'"\\u2066"'), ("\u2069",b'"\\u2069"'),
    ("\u00a0",'"\u00a0"'.encode()), ("\u206a",'"\u206a"'.encode()),
    ("e\u0301",'"e\u0301"'.encode()),
])
def test_j_scalar_exact_utf8_and_controls(value, expected):
    budget = _new_budget()
    assert _j_scalar(value, budget) == expected
    if type(value) is str:
        decoded, encoded = _string_lengths(value, budget)
        assert decoded == len(value.encode("utf-8"))
        assert encoded == len(expected)


@pytest.mark.parametrize("text", ["\ud800", "\udfff", "x\udc00"])
def test_lone_surrogates_are_structural_errors(text):
    with pytest.raises(_PreparationAborted) as raised:
        _j_scalar(text, _new_budget())
    assert raised.value.constraint == "unicode_scalar"


def test_scalar_primitives_cannot_serialize_a_report_or_tree():
    for value in ({}, [], _Object(()), _Array(()), 1, 0.5):
        with pytest.raises(_PreparationAborted) as raised:
            _j_scalar(value, _new_budget())
        assert raised.value.diagnostic_code == "type_or_enum_violation"


def test_hostile_subclass_hooks_and_metaclass_hooks_never_run():
    class Meta(type):
        def __eq__(self, other): raise AssertionError("metaclass")
        def __hash__(self): raise AssertionError("metaclass")
    class Poison(metaclass=Meta):
        def __str__(self): raise AssertionError("str")
        def __repr__(self): raise AssertionError("repr")
    class Text(str):
        def __len__(self): raise AssertionError("len")
        def __iter__(self): raise AssertionError("iter")
    class Float(float):
        def as_integer_ratio(self): raise AssertionError("ratio")
    for operation, value in ((_number_from_token,Text("1")), (_number_from_builtin,Float(1)),
                             (_j_scalar,Text("secret")), (_j_scalar,Poison())):
        with pytest.raises(_PreparationAborted): operation(value,_new_budget())


def test_stable_index_sort_lookup_and_unchanged_values():
    payload = _Array((None, False))
    pairs = (("z",payload),("a",None),("A",False),("a",True),("é",None),("e\u0301",True))
    budget = _new_budget()
    ordered = _sorted_pairs(pairs,budget)
    assert ordered == tuple(sorted(pairs,key=lambda p:p[0]))
    assert [v for k,v in ordered if k == "a"] == [None,True]
    assert _lookup_pair(ordered,"a",budget) == ("a",None)
    assert _lookup_pair(ordered,"absent",budget) is None
    assert pairs[0][1] is payload and payload.items == (None,False)
    assert budget.input_state == "not_completed"


def test_index_comparisons_charge_long_prefix_and_repeat_work():
    pairs = (("a" * 500 + "z",None),("a" * 500 + "a",False))
    budget = _new_budget()
    ordered = _sorted_pairs(pairs,budget)
    prior = budget.used
    _lookup_pair(ordered,pairs[0][0],budget)
    first = budget.used-prior
    _lookup_pair(ordered,pairs[0][0],budget)
    assert budget.used-prior == first*2
    assert first > 100


def test_interrupted_sort_returns_no_partial_index():
    budget = _new_budget()
    budget.charge(budget.remaining-20)
    received=[]
    with pytest.raises(_PreparationAborted) as raised:
        received.append(_sorted_pairs((("z"*50,None),("a",False)),budget))
    assert raised.value.limit_id == "WU9-L11"
    assert received == []


def test_atomic_scalar_value_is_not_returned_after_deadline():
    for expire in (2,4):
        calls=[]
        def clock():
            calls.append(1)
            return 60_000_000_001 if len(calls)>=expire else 0
        with patch("source_integrity_toolkit.runtime.resources.monotonic_ns",clock):
            budget=_new_budget(); received=[]
            with pytest.raises(_PreparationAborted) as raised:
                received.append(_j_scalar(False,budget))
            assert raised.value.limit_id == "WU9-L12" and received == []
