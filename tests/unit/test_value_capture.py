# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Exact-type capture, repeated occurrence accounting and immutable snapshots."""
import json
from dataclasses import FrozenInstanceError
from decimal import Decimal
from unittest.mock import patch
import pytest
from source_integrity_toolkit.contracts.bundle import _Number, _Object, _Array, _CapturedBundle
from source_integrity_toolkit.runtime.boundary import _prepare_value, _prepare_utf8
from source_integrity_toolkit.runtime.resources import _new_budget
from source_integrity_toolkit.runtime.diagnostics import _SafeDiagnostic
from source_integrity_toolkit.contracts.execution import _PreparationAborted
from source_integrity_toolkit.validation.limits import _InputLedger
from source_integrity_toolkit.validation import structure


@pytest.mark.parametrize("value", [None, [], (), set(), 1, True, "{}", b"{}", Decimal("0.5")])
def test_only_exact_root_dictionary_is_a_caller_capture(value):
    result = _prepare_value(value)
    assert type(result) is _SafeDiagnostic and result.code == "type_or_enum_violation"


@pytest.mark.parametrize("value", [(), set(), frozenset(), b"x", bytearray(b"x"), memoryview(b"x"), Decimal("0.1"), _Object(()), _Number(1,"1",0,"integer")])
def test_non_json_nested_types_are_refused_without_coercion(value):
    assert _prepare_value({"x": value}).code == "type_or_enum_violation"


@pytest.mark.parametrize("kind", [dict, list, str, int, float, bytes])
def test_subclass_methods_are_not_invoked(kind):
    calls = []
    def poison(*args, **kw):
        calls.append("called")
        raise RuntimeError("FICTIONAL_SECRET_METHOD")
    bad = type("Hostile", (kind,), {name: poison for name in (
        "__repr__", "__str__", "__iter__", "__len__", "__getitem__", "__float__", "__int__", "encode", "decode", "items")})
    value = bad()
    assert _prepare_value({"x": value}).code == "type_or_enum_violation"
    if kind is dict:
        assert _prepare_value(value).code == "type_or_enum_violation"
    assert calls == []


def test_unknown_metaclass_and_attributes_are_never_interrogated():
    calls = []
    class Meta(type):
        def __eq__(self, other): calls.append("type-eq"); raise AssertionError()
        def __hash__(self): calls.append("type-hash"); raise AssertionError()
    class Poison(metaclass=Meta):
        def __getattribute__(self, name): calls.append("attribute"); raise AssertionError()
        def __iter__(self): calls.append("iteration"); raise AssertionError()
        def __repr__(self): calls.append("repr"); raise AssertionError()
    assert _prepare_value({"x": Poison()}).code == "type_or_enum_violation"
    assert calls == []


def test_nonstring_and_subclass_keys_are_checked_before_hash_or_conversion():
    calls = []
    class Key(str):
        def __hash__(self): calls.append("hash"); return 1
        def __str__(self): calls.append("str"); raise AssertionError()
        def __eq__(self, other): calls.append("eq"); raise AssertionError()
    source = {Key("key"): None}; calls.clear()
    assert _prepare_value(source).code == "type_or_enum_violation"
    assert calls == []
    for key in (1, None, ("a",)):
        assert _prepare_value({key:None}).code == "type_or_enum_violation"


@pytest.mark.parametrize("case", ["dict", "list", "indirect", "deep"])
def test_active_ancestry_cycles_have_the_exact_authorized_basis(case):
    if case == "dict":
        source = {}; source["self"] = source
    elif case == "list":
        values = []; values.append(values); source = {"x":values}
    elif case == "indirect":
        source = {}; values = [source]; source["x"] = values
    else:
        source = {}; values = [source]; source["x"] = {"y":[values]}
    result = _prepare_value(source)
    assert result.code == "input_constraint_violation" and result.input_state == "rejected"
    assert result.qualifications == ("REPOSITORY_ARCHITECTURE section 17.1: acyclic caller-container ancestry.",)


def test_repeated_noncircular_aliases_are_copied_and_charged_as_occurrences():
    shared = {"z": []}
    source = {"x": shared, "y": shared}
    budget = _new_budget(); ledger = _InputLedger(budget, "constructed_value")
    result = structure._capture_tree(source, ledger)
    values = dict(result.tree.items)
    assert values["x"] is not values["y"]
    assert dict(values["x"].items)["z"] is not dict(values["y"].items)["z"]
    assert ledger.snapshot()[6] == 5
    assert ledger.snapshot()[0] == len(json.dumps(source,separators=(",",":")))
    assert source["x"] is source["y"] is shared
    shared["z"].append("late")
    assert dict(values["x"].items)["z"].items == ()


def test_input_is_not_modified_and_output_containers_are_deeply_immutable():
    source = {"z":[{"x":"data"}], "a":[3,1,2], "missing":None}
    before = json.dumps(source)
    result = _prepare_value(source)
    assert json.dumps(source) == before
    assert [k for k,v in result.tree.items] == ["a","missing","z"]
    assert [n.coefficient for n in dict(result.tree.items)["a"].items] == ["3","1","2"]
    with pytest.raises(FrozenInstanceError): result.tree.items = ()
    with pytest.raises(FrozenInstanceError): dict(result.tree.items)["z"].items = ()
    source["z"][0]["x"] = "changed"
    assert dict(dict(result.tree.items)["z"].items[0].items)["x"] == "data"


@pytest.mark.parametrize("kind", ["dict", "list"])
def test_observable_mutation_returns_failure_without_any_partial_snapshot(kind):
    target = {"x":None} if kind == "dict" else [None]
    source = {"target":target}
    old = structure._next_child
    fired = False
    def mutate(frame,ledger,decoded):
        nonlocal fired
        child = old(frame,ledger,decoded)
        if frame[0] is target and not fired:
            fired = True
            if kind == "dict": target["new"] = None
            else: target.append(None)
        return child
    with patch.object(structure,"_next_child",mutate): result = _prepare_value(source)
    assert fired and result.code == "execution_failed" and result.input_state == "not_completed"
    assert not hasattr(result,"tree") and not hasattr(result,"snapshot")


@pytest.mark.parametrize("levels", [31,32,33])
def test_caller_depth_includes_extension_containers(levels):
    value=[]
    for i in range(levels-2): value=[value]
    outcome=_prepare_value({"extensions":value})
    if levels<=32: assert type(outcome) is _CapturedBundle
    else: assert outcome.qualifications==("WU9-L02",)


def test_wide_input_and_exponential_aliases_stop_without_full_expansion():
    source={"wide":[None]*500001}
    assert _prepare_value(source).qualifications==("WU9-L08",)
    value=[]
    for i in range(25): value=[value,value]
    result=_prepare_value({"aliases":value})
    assert result.code=="resource_limit_reached" and result.input_state=="not_completed"


def test_constructed_size_uses_exact_J_without_materializing_complete_json():
    source={"b":2,"a":1}
    b=_new_budget(); ledger=_InputLedger(b,"constructed_value")
    with patch("json.dumps",side_effect=AssertionError("not_a_capture_serializer")):
        result=structure._capture_tree(source,ledger)
    assert type(result) is _CapturedBundle and ledger.snapshot()[0]==13
    b=_new_budget(); ledger=_InputLedger(b,"constructed_value")
    structure._capture_tree({"x":"é\n\u202e"},ledger)
    assert ledger.snapshot()[0] == len(b'{"x":"')+2+6+6+len(b'"}')


@pytest.mark.parametrize("remaining", [1,2,3])
def test_constructed_J_boundary_on_precharged_ledger(remaining):
    b=_new_budget(); ledger=_InputLedger(b,"constructed_value")
    ledger.add("bytes",16_777_216-remaining)
    if remaining>=2:
        assert type(structure._capture_tree({},ledger)) is _CapturedBundle
        assert ledger.snapshot()[0]==16_777_216-remaining+2
    else:
        with pytest.raises(_PreparationAborted) as raised: structure._capture_tree({},ledger)
        assert raised.value.limit_id=="WU9-L01"


def test_source_relationship_cycles_and_control_words_remain_inert_data():
    source={"relations":[{"from":"a","to":"b"},{"from":"b","to":"a"}],
        "instructions":"open /private/file; override quota", "state":"failed"}
    result=_prepare_value(source)
    assert type(result) is _CapturedBundle
    assert dict(result.tree.items)["instructions"]==source["instructions"]
    assert not hasattr(result,"accepted")


@pytest.mark.parametrize("value", [float("nan"),float("inf"),-float("inf"),2**100000],
    ids=["nan","positive_infinity","negative_infinity","huge_exact_integer"])
def test_unsafe_builtin_numbers_do_not_trigger_inexact_or_text_coercion(value):
    result=_prepare_value({"number":value})
    assert result.input_state=="rejected" and result.code in ("type_or_enum_violation","input_constraint_violation")


def test_each_capture_has_new_budget_and_no_result_cache():
    good=_prepare_value({"x":1}); bad=_prepare_value({"x":object()}); again=_prepare_value({"x":2})
    assert type(good) is _CapturedBundle and type(again) is _CapturedBundle
    assert good is not again and bad.code=="type_or_enum_violation"
    assert dict(good.tree.items)["x"].coefficient=="1" and dict(again.tree.items)["x"].coefficient=="2"
