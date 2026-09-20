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


# P2-W02-R01 developer-only regression coverage. No product module imports CI.
def _repair_driver():
    import importlib.util
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    spec = importlib.util.spec_from_file_location(
        "sit_w02_repair_ci_driver", root / "tests/scaffold/test_ci_contract.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_repair_exception_names_exactly_two_paths():
    ci = _repair_driver()
    paths = ci.phase_guard.plan_paths(ci.ROOT)
    expected = frozenset(("tests/security/test_scaffold_inertness.py",
                          "tests/scaffold/test_ci_contract.py"))
    assert ci.P2_W02_R01_PATHS == expected
    assert len(paths["P2-W02"]) == 15
    assert not expected & paths["P2-W02"]
    assert ci.effective_paths(paths, "P2-W02") == paths["P2-W02"] | expected
    ci.check_changed_paths(paths, "P2-W02", paths["P2-W02"] | expected)


def test_repair_does_not_expand_another_units_immediate_diff():
    ci = _repair_driver()
    paths = ci.phase_guard.plan_paths(ci.ROOT)
    for step in (1, 3, 4, 5, 6, 7, 8, 9):
        unit = f"P2-W{step:02}"
        # W04 and W05 each have a separate, exact owner-approved exception.
        extra = (ci.P2_W04_R01_PATHS if step == 4 else
                 (ci.P2_W05_R01_PATHS | ci.P2_W05_R02_PATHS) if step == 5 else frozenset())
        if step == 7:
            extra = extra | ci.P2_W07_R01_PATHS
        assert ci.effective_paths(paths, unit) == paths[unit] | extra
        for path in ci.P2_W02_R01_PATHS - paths[unit] - extra:
            with pytest.raises(ValueError, match="^work_unit_allowlist_exceeded$"):
                ci.check_changed_paths(paths, unit, {path})


def test_repair_cumulative_accounting_retains_only_authorized_extras():
    ci = _repair_driver()
    paths = ci.phase_guard.plan_paths(ci.ROOT)
    for step in range(1, 10):
        unit = f"P2-W{step:02}"
        original = set().union(*(paths[f"P2-W{i:02}"] for i in range(1, step + 1)))
        extras = ci.P2_W02_R01_PATHS if step >= 2 else frozenset()
        if step >= 4:
            extras = extras | ci.P2_W04_R01_PATHS
        if step >= 5:
            extras = extras | ci.P2_W05_R01_PATHS | ci.P2_W05_R02_PATHS
        if step >= 7:
            extras = extras | ci.P2_W07_R01_PATHS
        assert ci.effective_paths(paths, unit, cumulative=True) == original | extras


def test_repair_rejects_unlisted_and_similarly_named_paths():
    ci = _repair_driver()
    paths = ci.phase_guard.plan_paths(ci.ROOT)
    valid = ci.effective_paths(paths, "P2-W02")
    for path in ("tests/security/test_scaffold_no_network.py",
                 "tests/security/test_scaffold_no_native_loading.py",
                 "tests/security/test_scaffold_inertness.py.bak",
                 "tests/security/../scaffold/test_ci_contract.py",
                 "tests/security/TEST_scaffold_inertness.py",
                 ".github/workflows/phase1-ci.yml",
                 "tools/check_scaffold_boundary.py", "PHASE_2_PLAN.md"):
        assert path not in valid
        with pytest.raises(ValueError, match="^work_unit_allowlist_exceeded$"):
            ci.check_changed_paths(paths, "P2-W02", valid | {path})


def test_repair_rejects_invalid_context_without_mutating_plan():
    ci = _repair_driver()
    paths = ci.phase_guard.plan_paths(ci.ROOT)
    snapshot = dict(paths)
    for unit in ("P2-W00", "P2-W10", "P3-W02", "P2-W02; injected", 2):
        with pytest.raises(ValueError):
            ci.effective_paths(paths, unit)
    assert paths == snapshot
    assert ci.phase_guard.plan_paths(ci.ROOT) == snapshot


def test_repair_preserves_original_observer_and_every_old_assertion():
    import ast
    import hashlib
    import subprocess
    from pathlib import Path
    root = Path(__file__).resolve().parents[2]
    relative = "tests/security/test_scaffold_inertness.py"
    raw = subprocess.check_output([
        "git", "show", "22d43e003eae9b84ed5868696ec3847216a8a16f:" + relative],
        cwd=root, stderr=subprocess.PIPE, timeout=30)
    assert hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest() == (
        "a7a876006eb75ab5c3542e01f4b72c8a7483519f")
    old, new = ast.parse(raw), ast.parse((root / relative).read_bytes())
    def probe(tree):
        return next(n.value.value for n in tree.body if isinstance(n, ast.Assign)
                    and any(isinstance(t, ast.Name) and t.id == "PROBE" for t in n.targets))
    inserted = ("# P2-W02-R01: load this approved declaration helper before observation.\n"
                "import dataclasses\n")
    assert probe(new).count(inserted) == 1
    assert probe(new).replace(inserted, "") == probe(old)
    # Only PROBE's explicit preload and the one new test differ at AST level.
    for tree in (old, new):
        for node in tree.body:
            if isinstance(node, ast.Assign) and any(
                    isinstance(t, ast.Name) and t.id == "PROBE" for t in node.targets):
                node.value = ast.Constant(value="independently_checked_probe")
    for node in new.body:
        if isinstance(node, ast.ClassDef) and node.name == "ScaffoldInertnessTests":
            added = [m for m in node.body if isinstance(m, ast.FunctionDef)
                     and m.name == "test_dataclasses_preload_in_clean_interpreter"]
            assert len(added) == 1
            node.body.remove(added[0])
    assert ast.dump(old, include_attributes=False) == ast.dump(new, include_attributes=False)
