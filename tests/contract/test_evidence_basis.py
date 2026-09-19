# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Attributed immutable shape tags and safe private transport declarations."""
from dataclasses import FrozenInstanceError, fields
import pytest
from source_integrity_toolkit.contracts.bundle import _Object
from source_integrity_toolkit.contracts.evidence import _Node, _Attribution
from source_integrity_toolkit.contracts.constants import SHAPES, RECORD_SHAPES, RELATION_SHAPES, ASSESSMENT_SHAPES, VOCABULARIES
from source_integrity_toolkit.contracts.execution import _PreparationStop, _AuditCancelled
from source_integrity_toolkit.contracts.report import _PendingCheck, _SuppliedSelector, _DomainPreparation, DOMAIN_LABELS, PREREQUISITES, FAMILIES


@pytest.mark.parametrize("shape", [r[0] for r in SHAPES])
def test_every_declared_shape_has_one_noncertifying_immutable_representation(shape):
    node = _Node(shape,_Object(()))
    assert node.shape == shape and node.fields.items == ()
    assert {f.name for f in fields(node)} == {"shape","fields"}
    with pytest.raises(FrozenInstanceError): node.shape = "ClaimData"
    # Missing required source fields remain a future validation obligation.
    assert not hasattr(node,"accepted") and not hasattr(node,"is_valid")


def test_source_vocabularies_and_nested_declarations_are_immutable():
    for mapping in (VOCABULARIES,RECORD_SHAPES,RELATION_SHAPES,ASSESSMENT_SHAPES):
        with pytest.raises(TypeError): mapping["forged"] = "value"
    assert type(SHAPES) is tuple
    assert all(type(r) is tuple and type(r[2]) is tuple for r in SHAPES)
    assert all(type(v) is tuple for v in VOCABULARIES.values())


def test_unknown_shape_or_mutable_payload_is_rejected():
    with pytest.raises(TypeError): _Node("is_independent",_Object(()))
    with pytest.raises(TypeError): _Node("ClaimData",{})
    with pytest.raises(TypeError): _Attribution(_Node("ClaimData",_Object(())),_Node("TimeValue",_Object(())))


def test_documented_label_and_unknown_basis_remain_supplied_values():
    for kind in VOCABULARIES["basis_kind"]:
        p=_Node("Provenance",_Object((("basis_kind",kind),)))
        a=_Attribution(_Node("ClaimData",_Object((("text","FICTIONAL_SECRET"),))),p)
        assert a.provenance.fields.items == (("basis_kind",kind),)
        assert "FICTIONAL_SECRET" not in repr(a)
        assert not hasattr(a,"verified")


def test_no_false_private_completed_report_transport():
    assert _PreparationStop("rejected","rejected","input_not_accepted").input_state == "rejected"
    for state in ("accepted","not_completed"):
        assert _PreparationStop(state,"interrupted","resource_limit_reached").input_state == state
        assert _PreparationStop(state,"failed","execution_failed").input_state == state
    for args in [("accepted","completed","input_not_accepted"),("rejected","interrupted","resource_limit_reached"),
                 ("not_completed","interrupted","execution_failed"),("accepted","failed","FICTIONAL_SECRET")]:
        with pytest.raises(TypeError,match="^invalid_private_representation$"): _PreparationStop(*args)


def test_cancellation_is_not_a_resource_or_failure_code():
    for state in ("accepted","not_completed"):
        with pytest.raises(_AuditCancelled) as raised:
            raise _AuditCancelled(state)
        assert raised.value.input_state == state
        assert not hasattr(raised.value,"reason_code")
    with pytest.raises(TypeError,match="^invalid_private_representation$"):
        _AuditCancelled("FICTIONAL_SECRET")


def test_domain_slots_do_not_invent_available_results_or_maximum():
    assert [n for n,label in DOMAIN_LABELS] == list(range(5))
    assert PREREQUISITES == tuple(f"PC{i:02}" for i in range(1,25))
    assert FAMILIES == tuple(f"SIT-M{i:03}" for i in range(1,16))
    selector=_SuppliedSelector("records","opaque","data.state")
    domain=_DomainPreparation(4,(selector,),(_PendingCheck("PC01"),_PendingCheck("PC20")))
    assert {f.name for f in fields(domain)} == {"level_index","supplied","pending"}
    with pytest.raises(TypeError): _DomainPreparation(True,(),())
    with pytest.raises(TypeError): _DomainPreparation(5,(),())
    with pytest.raises(TypeError): _DomainPreparation(0,[],())
    with pytest.raises(TypeError): _PendingCheck("met")
