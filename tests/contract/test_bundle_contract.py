# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Local immutable representation tests; bounded ingestion is not implemented."""
from dataclasses import FrozenInstanceError, fields
import pytest
from source_integrity_toolkit.contracts.bundle import _Number, _Array, _Object, _CapturedBundle


class Poison:
    def __repr__(self):
        raise AssertionError("caller_repr_executed")
    def __iter__(self):
        raise AssertionError("caller_iterator_executed")
    def __eq__(self, other):
        raise AssertionError("caller_equality_executed")


@pytest.mark.parametrize("sign,c,e,k", [(0,"0",0,"integer"),(1,"5",-1,"decimal"),
    (-1,"123",-500,"decimal"),(1,"1",100,"integer"),(1,"5",-1,"binary_float")])
def test_exact_atoms_are_representations_not_conversions(sign,c,e,k):
    atom = _Number(sign,c,e,k)
    assert (atom.sign,atom.coefficient,atom.exponent,atom.source_kind) == (sign,c,e,k)
    # No parse, rounding or range-admission claim. W03 supplies those functions.
    assert not hasattr(atom,"accepted")


@pytest.mark.parametrize("args", [(True,"1",0,"integer"),(1,"",0,"integer"),
    (1,"01",0,"integer"),(1,"10",0,"integer"),(0,"1",0,"integer"),
    (1,"0",0,"integer"),(0,"0",1,"integer"),(1,"1",True,"integer"),
    (1,"١",0,"integer"),(1,"1",0,"unknown"),(Poison(),"1",0,"integer")])
def test_noncanonical_atoms_fail_locally_without_coercion(args):
    with pytest.raises(TypeError,match="^invalid_private_representation$"):
        _Number(*args)


def test_private_deep_structure_is_frozen():
    child = _Object((("opaque", "FICTIONAL_PRIVATE_CANARY"),))
    array = _Array((child,None,True,_Number(1,"5",-1,"decimal")))
    root = _Object((("array",array),))
    for obj,attr in ((root,"items"),(array,"items"),(child,"items")):
        with pytest.raises(FrozenInstanceError):
            setattr(obj,attr,())
        assert not hasattr(obj,"__dict__")
        assert "FICTIONAL_PRIVATE_CANARY" not in repr(obj)


@pytest.mark.parametrize("value", [[],{},1,0.5,Poison()])
def test_mutable_untyped_and_custom_values_are_not_coerced(value):
    with pytest.raises(TypeError,match="^invalid_private_representation$"):
        _Array((value,))


def test_exact_container_type_checked_before_iteration():
    class HostileTuple(tuple):
        def __iter__(self): raise AssertionError("subclass_iter")
    for constructor in (_Object,_Array):
        with pytest.raises(TypeError): constructor(HostileTuple())
        with pytest.raises(TypeError): constructor(Poison())


def test_keys_are_exact_and_unique_without_normalization():
    assert len(_Object((("A",None),("a",None))).items) == 2
    with pytest.raises(TypeError): _Object((("A",None),("A",None)))
    class BadString(str):
        def __hash__(self): raise AssertionError("subclass_hash")
    with pytest.raises(TypeError): _Object(((BadString("A"),None),))


def test_missing_null_empty_and_false_remain_distinct():
    x = _Object((("null",None),("empty",_Array(())),("false",False)))
    assert [p[0] for p in x.items] == ["null","empty","false"]
    assert x.items[0][1] is None and x.items[2][1] is False
    assert not any(k == "absent" for k,v in x.items)


def test_no_implicit_sort_merge_or_alias_count():
    shared = _Object((("id","x"),))
    array = _Array((shared,shared))
    assert len(array.items) == 2 and array.items[0] is array.items[1]
    obj = _Object((("z",None),("a",None)))
    assert [k for k,v in obj.items] == ["z","a"]


def test_captured_container_is_not_accepted_input():
    tree = _Object(())
    value = _CapturedBundle(tree,"constructed_value")
    assert {f.name for f in fields(value)} == {"tree","source_mode"}
    with pytest.raises(TypeError): _CapturedBundle({},"constructed_value")
    with pytest.raises(TypeError): _CapturedBundle(tree,"file_path")


def test_hostile_metaclass_is_not_called_by_exact_type_rejection():
    class Meta(type):
        def __eq__(self, other): raise AssertionError("metaclass_equality")
        def __hash__(self): raise AssertionError("metaclass_hash")
    class Custom(metaclass=Meta):
        pass
    with pytest.raises(TypeError,match="^invalid_private_representation$"):
        _Array((Custom(),))
