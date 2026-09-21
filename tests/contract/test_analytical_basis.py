# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Source-derived W03 documentary qualification and localization cases.

Definitions §§6,20.4–20.6,28.1; Lineage §§3.2,4,7,10.1,12,19.3,20.1;
Reporting §§12.4–12.5,13.1–13.2,16.6; Validation VG007/VG009,W7-23/W7-25.
Fixtures pass the unchanged preparation boundary. Separate test-owned jobs
exercise private components; this is not a composed analytical audit.
"""
import copy
from dataclasses import FrozenInstanceError, replace
import hashlib
import importlib.util
from pathlib import Path

import pytest

from source_integrity_toolkit.contracts import evidence
from source_integrity_toolkit.contracts.bundle import _Object
from source_integrity_toolkit.contracts.execution import _AnalysisAborted
from source_integrity_toolkit.runtime.boundary import _prepare_value
from source_integrity_toolkit.runtime import resources
from source_integrity_toolkit.validation import semantics


ROOT=Path(__file__).resolve().parents[2]
SOURCE_HASHES={
    "PHASE_3_PLAN.md":"e56da603271a489092ccfb9f9fe9086540bbb947ada8f4e7a676c8ed8f0feaae",
    "DEFINITIONS_AND_UNITS.md":"913697e733d4430a64696b36a7893fe2113da7e2cfbcadbb54247a36c1792e9d",
    "CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md":"32272903b45a8749115ed6b4ec9904dd864a2190f9e1a2ba43ced4c8256c0374",
    "OBSERVABILITY_AND_REPORTING.md":"44daa3c86fc7d12e7be16a3aedfe10d16b99f55aa69141f90319ce2b5e63ff6a",
    "VALIDATION_PLAN.md":"f958a12bda396cd12bfec096353ec17ec786e8c7fe30e07ee987f7d52874b707",
}
spec=importlib.util.spec_from_file_location("sit_w03_basis_input_cases",ROOT / "tests/contract/test_typed_records.py")
cases=importlib.util.module_from_spec(spec);spec.loader.exec_module(cases)

# These are independent source vocabularies, never copied from product output.
BASIS_KINDS=("declaration","documented_record","upstream_inference","protected_attestation","unspecified")
AVAILABILITIES=("supplied","locator_only","withheld","unavailable")


def dossier():
    value=cases.pool()
    assertion=cases.relation("depends_on")
    assertion["id"]="A"
    assertion["provenance"].update(basis_kind="documented_record",evidence_ref_ids=["support"])
    value["assertions"]=[assertion]
    return value


def named(value,identifier):
    return cases.by_id(value,identifier)


def prepared(value):
    result=_prepare_value(value)
    assert type(result) is evidence._PreparedBundle, repr(result)
    assert result.input_state=="accepted"
    return result


def source_entity(snapshot,identifier):
    return next(item for item in snapshot.entities if item.identifier==identifier)


def analysis_context():
    owner=resources._new_analysis_budget()
    owner.record_input_acceptance()  # Tool-owned fixture, not admission execution.
    return owner,owner.start_job()


def pointer(identifier,target):
    return {"id":identifier,"reference_kind":"record_pointer","availability":"supplied",
            "artifact_ref":None,"record_ref":target,"locator":None,"excerpt":None,
            "provided_by_ref":"actor","attestor_ref":None,"scope_note":"Fictional assurance pointer."}


def contrary(value,**changes):
    denial=copy.deepcopy(named(value,"A"))
    denial["id"]="B"
    denial["data"]["polarity"]="denied"
    denial["provenance"].update(basis_kind="declaration",evidence_ref_ids=[])
    for path,new in changes.items():
        keys=path.split(".");target=denial
        for key in keys[:-1]: target=target[key]
        target[keys[-1]]=new
    value["assertions"].append(denial)
    return denial


def context(**changes):
    values=dict(inquiry_ref="inquiry",claim_refs=("claim",),subject_refs=("origin","origin2"),
                dependency_dimension="acquisition",temporal_basis="snapshot_structural",
                requested_time=None,coverage_kind="upstream_history",relation_types=("depends_on",),
                graph_view="claim_origin",operation_anchor=())
    values.update(changes)
    return evidence._QualificationContext(**values)


def qualify(value,identifier="A",**scope_changes):
    snapshot=prepared(value)
    owner,job=analysis_context()
    out=semantics._qualify_basis(snapshot,identifier,context(**scope_changes),job)
    return out,snapshot,owner,job


def source_ids(addresses):
    return {address.record_id for address in addresses}


@pytest.mark.parametrize("name,digest",tuple(SOURCE_HASHES.items()),ids=tuple(SOURCE_HASHES))
def test_qualification_oracles_keep_the_accepted_normative_sources(name,digest):
    assert hashlib.sha256((ROOT/name).read_bytes()).hexdigest()==digest


def constructed_fact():
    """A typed representation witness; construction never proves execution."""
    return evidence._BasisQualification(evidence._SourceAddress("assertions","A","provenance"),
        "documented_record","met",(),(evidence._SourceAddress("evidence_references","support"),),
        ("Representation fixture only; documentary inspection has not run.",),context())


@pytest.mark.parametrize("change",[
    {"state":"available"},{"declared_basis":"verified"},{"reason_codes":("new_truth_score",)},
    {"state":"unmet","reason_codes":()},{"support_refs":[]},{"qualifications":[]},
    {"reason_codes":[]},
],ids=["result_state_namespace","invented_native_basis","invented_reason","unexplained_nonmet",
       "mutable_addresses","mutable_qualifications","mutable_reasons"])
def test_qualification_representation_rejects_semantically_wrong_or_mutable_fields(change):
    baseline=constructed_fact()
    assert baseline.state=="met" and baseline.declared_basis=="documented_record"
    assert not hasattr(baseline,"completed_check_executed")
    with pytest.raises(TypeError): replace(baseline,**change)
    assert baseline.support_refs[0].record_id=="support" and baseline.state=="met"


@pytest.mark.parametrize("collection",["results","populations","reasons","/tmp/evidence"])
def test_source_addresses_cannot_alias_report_local_or_filesystem_namespaces(collection):
    positive=evidence._SourceAddress("records","same-text-id","data.claim_ref")
    assert (positive.collection,positive.record_id,positive.selector)==("records","same-text-id","data.claim_ref")
    with pytest.raises(TypeError): evidence._SourceAddress(collection,"same-text-id")


@pytest.mark.parametrize("field",["claim_refs","subject_refs","relation_types","operation_anchor"])
def test_qualification_context_does_not_retain_mutable_caller_containers(field):
    baseline=context()
    mutable=list(getattr(baseline,field))
    with pytest.raises(TypeError): replace(baseline,**{field:mutable})
    mutable.append("forged")
    assert "forged" not in getattr(baseline,field)


def test_temporal_context_requires_a_typed_frozen_timevalue_without_filling_unknown_time():
    time=evidence._Node("TimeValue",_Object((("state","unknown"),("value",None),("precision",None),
                                            ("reason","Effective time is not supplied."))))
    positive=context(temporal_basis="time_specific",requested_time=time)
    assert positive.requested_time is time and dict(time.fields.items)["value"] is None
    for invalid in ({"state":"known"},[],evidence._Node("Provenance",_Object(()))):
        with pytest.raises(TypeError): context(temporal_basis="time_specific",requested_time=invalid)
    with pytest.raises(FrozenInstanceError): positive.requested_time=None


def test_private_qualification_parts_reject_callbacks_and_custom_objects_without_invoking_them():
    calls=[]
    def callback(): calls.append("callback");raise AssertionError("Must remain inert.")
    class Hostile:
        def __iter__(self): calls.append("iteration");raise AssertionError("Must not iterate.")
        def __str__(self): calls.append("string");raise AssertionError("Must not coerce.")
        def __eq__(self,other): calls.append("equality");raise AssertionError("Must not compare.")
    for invalid in (callback,Hostile()):
        with pytest.raises(TypeError): context(claim_refs=(invalid,))
        with pytest.raises(TypeError): context(operation_anchor=(invalid,))
        with pytest.raises(TypeError): replace(constructed_fact(),source=invalid)
    assert calls==[]


@pytest.mark.parametrize("basis_kind",BASIS_KINDS)
def test_supported_native_basis_labels_are_preserved_without_a_confidence_ladder(basis_kind):
    value=dossier();named(value,"A")["provenance"]["basis_kind"]=basis_kind
    before=copy.deepcopy(value)
    out,snapshot,owner,job=qualify(value)
    assert out.declared_basis==basis_kind and out.state=="met"
    assert out.source.collection=="assertions" and out.source.record_id=="A"
    assert "support" in source_ids(out.support_refs) and job.used>0
    assert out.context.claim_refs==("claim",) and out.context.dependency_dimension=="acquisition"
    assert out.qualifications and value==before
    assert not any(hasattr(out,name) for name in ("authenticated","verified","confidence","result_state"))
    with pytest.raises(FrozenInstanceError): out.declared_basis="verified"


@pytest.mark.parametrize("missing",["attributed_to_ref","method","evidence_ref_ids"])
def test_each_missing_documentary_component_has_an_independent_gap_and_restoring_control(missing):
    value=dossier();record=named(value,"A")
    if missing=="evidence_ref_ids":
        record["provenance"][missing]=[]
    else:
        record["provenance"][missing]=None
        record["gaps"]=[{"field":"provenance."+missing,"reason":"not_recorded",
                         "detail":"The component is explicitly absent in this derived case."}]
    out,snapshot,owner,job=qualify(value)
    assert out.state!="met" and "documentary_basis_incomplete" in out.reason_codes
    assert out.declared_basis=="documented_record" and snapshot.input_state=="accepted"
    restored,*_=qualify(dossier())
    assert restored.state=="met" and "documentary_basis_incomplete" not in restored.reason_codes


@pytest.mark.parametrize("kind",["local_locator","external_locator"])
@pytest.mark.parametrize("availability",AVAILABILITIES)
def test_a_locator_never_becomes_inspected_material_even_with_a_supplied_label(kind,availability):
    value=dossier();support=named(value,"support")
    support.update(reference_kind=kind,availability=availability,excerpt=None,
                   locator="https://fictional.invalid/support" if kind=="external_locator" else "fictional/local/support")
    out,snapshot,owner,job=qualify(value)
    assert out.state!="met" and "support_uninspectable" in out.reason_codes
    native=dict(source_entity(snapshot,"support").node.fields.items)
    assert native["availability"]==availability and native["reference_kind"]==kind
    assert native["locator"]==support["locator"] and out.declared_basis=="documented_record"


@pytest.mark.parametrize("kind",["local_locator","external_locator"])
def test_qualification_does_not_open_or_fetch_inert_support_locators(kind,monkeypatch):
    import builtins
    import io
    import os
    import socket
    import urllib.request
    value=dossier();named(value,"support").update(reference_kind=kind,availability="locator_only",excerpt=None,
        locator="https://fictional.invalid/not-a-runtime-resource" if kind=="external_locator" else "fictional/no-file")
    snapshot=prepared(value);owner,job=analysis_context();attempts=[]
    def forbidden(*args,**kwargs):
        attempts.append("I/O attempted")
        raise AssertionError("Qualification may inspect only the admitted evidence payload.")
    with monkeypatch.context() as patch:
        for module,name in ((builtins,"open"),(io,"open"),(os,"open"),(socket,"create_connection"),(urllib.request,"urlopen")):
            patch.setattr(module,name,forbidden)
        out=semantics._qualify_basis(snapshot,"A",context(),job)
    assert attempts==[] and out.state!="met" and "support_uninspectable" in out.reason_codes


@pytest.mark.parametrize("availability",AVAILABILITIES)
def test_visible_protected_attestation_is_distinct_from_its_withheld_underlying_material(availability):
    value=dossier();support=named(value,"support")
    support.update(reference_kind="protected_attestation",availability=availability,attestor_ref="actor",
                   excerpt="Supplied protected testimony limited to this dependency.")
    hidden=copy.deepcopy(support)
    hidden.update(id="hidden",reference_kind="external_locator",availability="withheld",attestor_ref=None,
                  excerpt=None,locator="https://fictional.invalid/withheld",artifact_ref="unresolved")
    value["evidence_references"].append(hidden)
    out,snapshot,owner,job=qualify(value)
    assert out.declared_basis=="documented_record"
    if availability=="supplied":
        assert out.state=="met" and "support" in source_ids(out.support_refs)
        assert "hidden" not in source_ids(out.support_refs)
    else:
        assert out.state!="met" and "support_uninspectable" in out.reason_codes
    assert dict(source_entity(snapshot,"hidden").node.fields.items)["availability"]=="withheld"
    assert dict(source_entity(snapshot,"support").node.fields.items)["availability"]==availability


@pytest.mark.parametrize("loop",["self","mutual"])
@pytest.mark.parametrize("independent_support",[False,True])
def test_assurance_loop_requires_independent_supplied_support_and_remains_disclosed(loop,independent_support):
    value=dossier();a=named(value,"A")
    a["provenance"]["evidence_ref_ids"]=["to-A" if loop=="self" else "to-B"]
    value["evidence_references"].append(pointer("to-A","A"))
    if loop=="mutual":
        b=copy.deepcopy(a);b["id"]="B";b["provenance"]["evidence_ref_ids"]=["to-A"]
        value["assertions"].append(b)
        value["evidence_references"].append(pointer("to-B","B"))
    if independent_support: a["provenance"]["evidence_ref_ids"].append("support")
    out,snapshot,owner,job=qualify(value)
    assert "self_supporting_assurance" in out.reason_codes
    assert out.state==("met" if independent_support else "unmet")
    assert out.declared_basis=="documented_record"
    assert ("support" in source_ids(out.support_refs)) is independent_support
    assert "A" in {entity.identifier for entity in snapshot.entities}
    if loop=="mutual": assert "B" in {entity.identifier for entity in snapshot.entities}


@pytest.mark.parametrize("lifecycle",["active","withdrawn","superseded"])
@pytest.mark.parametrize("polarity",["affirmed","denied"])
def test_documentary_basis_does_not_claim_current_positive_edge_eligibility(lifecycle,polarity):
    value=dossier();a=named(value,"A")
    a["lifecycle_state"]=lifecycle;a["data"]["polarity"]=polarity
    if lifecycle!="active":
        a["lifecycle_basis_ref_ids"]=["support"]
        a["provenance"]["qualifications"].append("Supplied lifecycle evidence; history is retained.")
    out,snapshot,owner,job=qualify(value)
    assert out.state=="met" and out.declared_basis=="documented_record"
    native=dict(source_entity(snapshot,"A").node.fields.items)
    assert native["lifecycle_state"]==lifecycle and dict(native["data"].items)["polarity"]==polarity
    assert not hasattr(out,"eligible_positive_relation") and not hasattr(out,"PC04")


@pytest.mark.parametrize("changed",["inquiry","claim_version","dimension","empty_claim_scope"])
def test_support_qualification_cannot_borrow_a_different_exact_assertion_scope(changed):
    value=dossier()
    if changed=="inquiry":
        other=copy.deepcopy(value["inquiries"][0]);other["id"]="other-inquiry";value["inquiries"].append(other)
        changes={"inquiry_ref":"other-inquiry"}
    elif changed=="claim_version":
        value["inquiries"][0]["target_claim_refs"].append("claim2")
        changes={"claim_refs":("claim2",)}
    elif changed=="dimension":
        value["inquiries"][0]["dependency_dimensions"].append("analytical_method")
        changes={"dependency_dimension":"analytical_method"}
    else:
        named(value,"A")["scope"]["claim_refs"]=[]
        # Inquiry-scoped identity metadata is valid, but is not all-Claim
        # acquisition support. A claim-lineage assertion with no Claim would
        # instead fail structural admission and cannot test this distinction.
        named(value,"A")["data"].update(predicate="same_identity_as",dimension=None,
                                          details={"identity_level":"origin_event"})
        changes={}
    out,*_=qualify(value,**changes)
    assert out.state!="met" and "scope_unestablished" in out.reason_codes
    assert out.declared_basis=="documented_record"


def test_both_empty_claim_scopes_are_a_valid_inquiry_metadata_question_not_a_wildcard():
    value=dossier();a=named(value,"A")
    a["scope"]["claim_refs"]=[]
    a["data"].update(predicate="same_identity_as",dimension=None,details={"identity_level":"origin_event"})
    out,*_=qualify(value,claim_refs=(),dependency_dimension=None,
                   relation_types=("same_identity_as",),graph_view="assertion_assurance")
    assert out.state=="met" and out.context.claim_refs==()
    assert "scope_unestablished" not in out.reason_codes
    acquisition,*_=qualify(value)
    assert acquisition.state!="met" and "scope_unestablished" in acquisition.reason_codes


@pytest.mark.parametrize("kind",["origin_boundary","independence"])
def test_assessment_documentary_basis_preserves_its_explicit_dependency_dimension(kind):
    value=coverage_dossier();value["inquiries"][0]["dependency_dimensions"].append("analytical_method")
    subjects,details=copy.deepcopy(cases.assessments()[kind]);details["coverage_ref"]="coverage"
    assessment=cases.assertion("dimension-assessment","assessment",{
        "assessment_kind":kind,"subject_refs":subjects,"details":details})
    assessment["provenance"].update(basis_kind="documented_record",evidence_ref_ids=["support"])
    value["assertions"].append(assessment)
    matching,*_=qualify(value,"dimension-assessment",subject_refs=tuple(subjects))
    assert matching.state=="met" and "scope_unestablished" not in matching.reason_codes
    mismatch,*_=qualify(value,"dimension-assessment",subject_refs=tuple(subjects),
                       dependency_dimension="analytical_method")
    assert mismatch.state!="met" and "scope_unestablished" in mismatch.reason_codes
    assert matching.declared_basis==mismatch.declared_basis=="documented_record"
    assert matching.context.dependency_dimension=="acquisition"
    assert mismatch.context.dependency_dimension=="analytical_method"


@pytest.mark.parametrize("change",[None,"other_claim","other_dimension","other_endpoints","other_predicate","withdrawn","superseded"])
def test_only_current_matching_weak_denials_block_the_necessary_premise(change):
    value=dossier();b=contrary(value)
    if change=="other_claim":
        value["inquiries"][0]["target_claim_refs"].append("claim2");b["scope"]["claim_refs"]=["claim2"]
    elif change=="other_dimension":
        value["inquiries"][0]["dependency_dimensions"].append("analytical_method");b["data"]["dimension"]="analytical_method"
    elif change=="other_endpoints":
        b["data"]["from_ref"],b["data"]["to_ref"]="origin2","origin"
    elif change=="other_predicate":
        b["data"].update(predicate="same_identity_as",dimension=None,details={"identity_level":"origin_event"})
    elif change in ("withdrawn","superseded"):
        b["lifecycle_state"]=change;b["lifecycle_basis_ref_ids"]=["support"]
        b["provenance"]["qualifications"].append("Supplied lifecycle change.")
    snapshot=prepared(value);owner,job=analysis_context()
    out=semantics._qualify_conflicts(snapshot,"A",context(),job)
    assert out.state==("unmet" if change is None else "met")
    assert ("premise_disputed" in out.reason_codes) is (change is None)
    assert source_entity(snapshot,"B").identifier=="B" and out.source.record_id=="A"
    if change is None:
        assert "B" in source_ids(out.support_refs)
        assert dict(dict(source_entity(snapshot,"B").node.fields.items)["provenance"].items)["basis_kind"]=="declaration"


@pytest.mark.parametrize("lifecycle",["withdrawn","superseded"])
@pytest.mark.parametrize("availability",["supplied","locator_only","withheld","unavailable"])
def test_nonactive_status_needs_inspectable_lifecycle_basis_to_exclude_a_relevant_denial(lifecycle,availability):
    value=dossier();b=contrary(value)
    b["lifecycle_state"]=lifecycle;b["lifecycle_basis_ref_ids"]=["lifecycle-support"]
    b["provenance"]["qualifications"].append("Lifecycle is attributed separately from the denial itself.")
    ref=copy.deepcopy(named(value,"support"));ref["id"]="lifecycle-support"
    if availability!="supplied":
        ref.update(reference_kind="external_locator",availability=availability,excerpt=None,
                   locator="https://fictional.invalid/lifecycle-status")
    value["evidence_references"].append(ref)
    snapshot=prepared(value);owner,job=analysis_context()
    out=semantics._qualify_conflicts(snapshot,"A",context(),job)
    assert out.state==("met" if availability=="supplied" else "unmet")
    assert ("premise_disputed" in out.reason_codes) is (availability!="supplied")
    native=dict(source_entity(snapshot,"B").node.fields.items)
    assert native["lifecycle_state"]==lifecycle and native["lifecycle_basis_ref_ids"].items==("lifecycle-support",)


def test_stance_disagreement_does_not_become_a_parentage_conflict():
    value=dossier();stance=cases.relation("contradicts");stance["id"]="B";value["assertions"].append(stance)
    snapshot=prepared(value);owner,job=analysis_context()
    out=semantics._qualify_conflicts(snapshot,"A",context(),job)
    assert out.state=="met" and "premise_disputed" not in out.reason_codes
    assert source_entity(snapshot,"B").identifier=="B"


@pytest.mark.parametrize("dimension",["analytical_method","model_ancestry","evaluation_rubric","organizational_control"])
def test_denials_in_each_other_dependency_dimension_do_not_block_acquisition(dimension):
    value=dossier();value["inquiries"][0]["dependency_dimensions"].append(dimension)
    contrary(value,**{"data.dimension":dimension})
    snapshot=prepared(value);owner,job=analysis_context()
    out=semantics._qualify_conflicts(snapshot,"A",context(),job)
    assert out.state=="met" and "premise_disputed" not in out.reason_codes
    assert dict(dict(source_entity(snapshot,"B").node.fields.items)["data"].items)["dimension"]==dimension


def test_identified_opaque_attestor_can_supply_visible_scope_limited_testimony():
    value=dossier()
    actor=cases.record("protected-actor","actor",{
        "actor_kind":"human","identity_disclosure":"protected","display_name":None})
    actor["gaps"]=[{"field":"data.display_name","reason":"withheld","detail":"Identity intentionally opaque."}]
    value["records"].append(actor)
    named(value,"A")["provenance"].update(attributed_to_ref="protected-actor",basis_kind="protected_attestation")
    named(value,"support").update(reference_kind="protected_attestation",attestor_ref="protected-actor",
                                   excerpt="Visible limited testimony; underlying identity is withheld.")
    out,snapshot,owner,job=qualify(value)
    assert out.state=="met" and out.declared_basis=="protected_attestation"
    assert "support" in source_ids(out.support_refs)
    native=dict(dict(source_entity(snapshot,"protected-actor").node.fields.items)["data"].items)
    assert native["identity_disclosure"]=="protected" and native["display_name"] is None


@pytest.mark.parametrize("reason",["not_recorded","outside_snapshot"])
@pytest.mark.parametrize("expected_kind",["actor","model"])
def test_an_expected_asserter_kind_does_not_instantiate_a_missing_asserter(reason,expected_kind):
    value=dossier()
    missing=cases.record("missing-asserter","unresolved_reference",{
        "expected_kinds":[expected_kind],"reason":reason,"description":"The attributed identity is not supplied."})
    value["records"].append(missing)
    named(value,"A")["provenance"]["attributed_to_ref"]="missing-asserter"
    out,snapshot,owner,job=qualify(value)
    assert out.state!="met" and "documentary_basis_incomplete" in out.reason_codes
    assert source_entity(snapshot,"missing-asserter").kind=="unresolved_reference"
    named(value,"A")["provenance"]["attributed_to_ref"]="actor"
    restored,*_=qualify(value)
    assert restored.state=="met" and "documentary_basis_incomplete" not in restored.reason_codes


def test_active_alias_limits_only_identity_qualification_without_merging_records():
    value=dossier();alias=cases.relation("same_identity_as")
    alias["id"]="alias";alias["data"].update(from_ref="origin",to_ref="origin2",details={"identity_level":"origin_event"})
    value["assertions"].append(alias)
    snapshot=prepared(value);owner,job=analysis_context()
    affected=semantics._qualify_identity(snapshot,("origin","origin2"),context(),job)
    assert affected.state!="met" and "identity_unresolved" in affected.reason_codes
    assert "alias" in source_ids(affected.support_refs)
    owner,job=analysis_context()
    unrelated=semantics._qualify_identity(snapshot,("artifact","artifact2"),context(subject_refs=("artifact","artifact2")),job)
    assert unrelated.state=="met" and "identity_unresolved" not in unrelated.reason_codes
    assert source_entity(snapshot,"origin") is not source_entity(snapshot,"origin2")


@pytest.mark.parametrize("relevant",[False,True])
def test_explicit_unresolved_conflicts_are_localized_to_the_named_assertions(relevant):
    value=dossier()
    b=copy.deepcopy(named(value,"A"));b["id"]="B"
    c=copy.deepcopy(named(value,"A"));c["id"]="C"
    conflict=cases.assertion("dispute","assessment",{
        "assessment_kind":"conflict","subject_refs":["A","B"] if relevant else ["B","C"],
        "details":{"conflict_kind":"scope_dispute","resolution_state":"unresolved",
                   "resolution_evaluation_ref":None,"scope_note":"Only the two explicitly named assertions are disputed."}})
    value["assertions"].extend([b,c,conflict])
    snapshot=prepared(value);owner,job=analysis_context()
    out=semantics._qualify_conflicts(snapshot,"A",context(),job)
    assert out.state==("unmet" if relevant else "met")
    assert ("premise_disputed" in out.reason_codes) is relevant
    if relevant: assert "dispute" in source_ids(out.support_refs)


def test_external_resolution_does_not_delete_a_still_active_denial_or_select_a_winner():
    value=dossier();contrary(value)
    resolution=cases.assertion("resolution","assessment",{
        "assessment_kind":"conflict","subject_refs":["A","B"],
        "details":{"conflict_kind":"affirmation_denial","resolution_state":"externally_resolved",
                   "resolution_evaluation_ref":"evaluation","scope_note":"External adjudication remains attributed."}})
    value["assertions"].append(resolution)
    snapshot=prepared(value);owner,job=analysis_context()
    out=semantics._qualify_conflicts(snapshot,"A",context(),job)
    assert out.state=="unmet" and "premise_disputed" in out.reason_codes
    assert {"A","B","resolution"} <= {item.identifier for item in snapshot.entities}
    assert dict(source_entity(snapshot,"B").node.fields.items)["lifecycle_state"]=="active"


def coverage_dossier():
    value=dossier()
    cov=cases.assertion("coverage","assessment",{
        "assessment_kind":"coverage","subject_refs":["origin","origin2"],
        "details":{"coverage_kind":"upstream_history","state":"complete_for_scope",
                   "relation_types":["depends_on"],"dimensions":["acquisition"],
                   "member_refs":["origin","origin2"],"omitted_refs":[],"universe_enumerated":True,
                   "scope_note":"Explicit finite origin dependency area; no other view is covered."}})
    cov["provenance"].update(basis_kind="documented_record",evidence_ref_ids=["support"])
    value["assertions"].append(cov)
    value["inquiries"][0]["coverage_assertion_refs"]=["coverage"]
    return value


def coverage_check(value,**scope_changes):
    snapshot=prepared(value);owner,job=analysis_context()
    out=semantics._qualify_coverage(snapshot,("coverage",),context(**scope_changes),job)
    assert type(out) is tuple and len(out)==1
    return out[0],snapshot,job


def test_coverage_qualification_retains_the_complete_attributed_source_and_exact_area():
    out,snapshot,job=coverage_check(coverage_dossier())
    assert out.state=="met" and out.source.record_id=="coverage"
    assert out.coverage is source_entity(snapshot,"coverage")
    detail=dict(dict(out.coverage.node.fields.items)["data"].items)["details"]
    detail=dict(detail.items)
    assert detail["coverage_kind"]=="upstream_history" and detail["state"]=="complete_for_scope"
    assert detail["member_refs"].items==("origin","origin2")
    assert out.context.dependency_dimension=="acquisition" and out.context.relation_types==("depends_on",)
    assert "support" in source_ids(out.support_refs) and job.used>0


@pytest.mark.parametrize("change",["partial","not_examined","wrong_kind","wrong_dimension","missing_predicate",
                                   "missing_member","omitted_member","unknown_member","not_enumerated","unsupported","withdrawn"])
def test_complete_label_cannot_override_the_required_coverage_area_or_its_limits(change):
    value=coverage_dossier();cov=named(value,"coverage");details=cov["data"]["details"]
    if change in ("partial","not_examined"): details["state"]=change
    elif change=="wrong_kind": details["coverage_kind"]="citation_list"
    elif change=="wrong_dimension": details["dimensions"]=["model_ancestry"]
    elif change=="missing_predicate": details["relation_types"]=[]
    elif change=="missing_member": details["member_refs"]=["origin"]
    elif change=="omitted_member": details["omitted_refs"]=["origin2"]
    elif change=="unknown_member": details["member_refs"].append("unresolved")
    elif change=="not_enumerated": details["universe_enumerated"]=False
    elif change=="unsupported": cov["provenance"]["evidence_ref_ids"]=[]
    else:
        cov["lifecycle_state"]="withdrawn";cov["lifecycle_basis_ref_ids"]=["support"]
        cov["provenance"]["qualifications"].append("Supported withdrawal of this coverage declaration.")
    out,snapshot,job=coverage_check(value)
    assert out.state!="met" and out.reason_codes
    assert out.coverage is source_entity(snapshot,"coverage")
    native=dict(dict(out.coverage.node.fields.items)["data"].items)["details"]
    assert dict(native.items)["state"]==details["state"]
    assert {entity.identifier for entity in snapshot.entities} >= {"origin","origin2","A","coverage"}


def test_absent_coverage_does_not_invent_a_record_or_erase_independent_supported_basis():
    value=dossier();snapshot=prepared(value);owner,job=analysis_context()
    assert semantics._qualify_coverage(snapshot,(),context(),job)==()
    positive=semantics._qualify_basis(snapshot,"A",context(),job)
    assert positive.state=="met" and "support" in source_ids(positive.support_refs)


@pytest.mark.parametrize("branch_scope",["matching","other_claim","other_dimension","other_inquiry"])
def test_actual_matching_outgoing_branch_cannot_be_omitted_from_complete_coverage(branch_scope):
    value=coverage_dossier()
    third=copy.deepcopy(named(value,"origin2"));third["id"]="origin3";third["data"]["event_key"]="origin3"
    value["records"].append(third)
    branch=copy.deepcopy(named(value,"A"));branch["id"]="branch";branch["data"].update(from_ref="origin2",to_ref="origin3")
    if branch_scope=="other_claim":
        value["inquiries"][0]["target_claim_refs"].append("claim2");branch["scope"]["claim_refs"]=["claim2"]
    elif branch_scope=="other_dimension":
        value["inquiries"][0]["dependency_dimensions"].append("analytical_method")
        branch["data"]["dimension"]="analytical_method"
    elif branch_scope=="other_inquiry":
        other=copy.deepcopy(value["inquiries"][0]);other["id"]="other-inquiry";other["coverage_assertion_refs"]=[]
        value["inquiries"].append(other);branch["scope"]["inquiry_refs"]=["other-inquiry"]
    value["assertions"].append(branch)
    out,snapshot,job=coverage_check(value)
    assert out.state==("unmet" if branch_scope=="matching" else "met")
    assert ("upstream_coverage_incomplete" in out.reason_codes) is (branch_scope=="matching")
    assert source_entity(snapshot,"branch").identifier=="branch"
    if branch_scope=="matching":
        named(value,"coverage")["data"]["details"]["member_refs"].append("origin3")
        repaired,*_=coverage_check(value)
        assert repaired.state=="met"


def test_empty_coverage_relation_types_do_not_query_unrelated_outgoing_predicates():
    value=coverage_dossier();cov=named(value,"coverage")
    cov["data"]["subject_refs"]=["inquiry","pipeline"]
    cov["data"]["details"].update(coverage_kind="pipeline_universe",relation_types=[],dimensions=[],
                                  member_refs=["artifact"])
    scope=dict(subject_refs=("artifact",),dependency_dimension=None,relation_types=(),
               coverage_kind="pipeline_universe",graph_view="pipeline_stages")
    # PC06-local finite record coverage is the question here. This does not
    # execute the later stage eligibility/classification or calculate M010.
    baseline,*_=coverage_check(value,**scope)
    assert baseline.state=="met" and "upstream_coverage_incomplete" not in baseline.reason_codes
    publisher=cases.relation("published_by");publisher["id"]="unrelated-publication"
    value["assertions"].append(publisher)  # artifact -> actor, with no dimension.
    augmented,snapshot,job=coverage_check(value,**scope)
    assert augmented.state=="met" and "upstream_coverage_incomplete" not in augmented.reason_codes
    assert augmented.context.relation_types==() and augmented.context.subject_refs==("artifact",)
    native=dict(dict(augmented.coverage.node.fields.items)["data"].items)["details"]
    assert dict(native.items)["member_refs"].items==("artifact",)
    assert source_entity(snapshot,"unrelated-publication").identifier=="unrelated-publication"


@pytest.mark.parametrize("subject",["inquiry","other-inquiry"])
def test_inquiry_coverage_can_cover_only_its_explicit_finite_area(subject):
    value=coverage_dossier()
    other=copy.deepcopy(value["inquiries"][0]);other["id"]="other-inquiry";other["coverage_assertion_refs"]=[]
    value["inquiries"].append(other)
    named(value,"coverage")["data"]["subject_refs"]=[subject]
    out,snapshot,job=coverage_check(value)
    assert out.state==("met" if subject=="inquiry" else "unmet")
    assert out.coverage is source_entity(snapshot,"coverage")
    assert out.context.subject_refs==("origin","origin2")


@pytest.mark.parametrize("subject",["inquiry","origin"])
def test_origin_only_coverage_cannot_establish_parentage_of_a_preceding_evidence_item(subject):
    value=coverage_dossier();cov=named(value,"coverage")
    cov["data"]["subject_refs"]=[subject]
    cov["data"]["details"].update(member_refs=["e","origin"],relation_types=["originates_from"])
    relation=cases.relation("originates_from");relation["id"]="seed-origin"
    relation["provenance"].update(basis_kind="documented_record",evidence_ref_ids=["support"])
    value["assertions"].append(relation)
    out,snapshot,job=coverage_check(value,subject_refs=("e",),relation_types=("originates_from",))
    assert out.state==("met" if subject=="inquiry" else "unmet")
    assert ("upstream_coverage_incomplete" in out.reason_codes) is (subject=="origin")
    assert source_entity(snapshot,"seed-origin").identifier=="seed-origin"


def seam_call(name,snapshot,job):
    if name=="basis": return semantics._qualify_basis(snapshot,"A",context(),job)
    if name=="conflicts": return semantics._qualify_conflicts(snapshot,"A",context(),job)
    if name=="identity": return semantics._qualify_identity(snapshot,("origin","origin2"),context(),job)
    return semantics._qualify_coverage(snapshot,("coverage",),context(),job)


@pytest.mark.parametrize("name",["basis","conflicts","identity","coverage"])
def test_each_qualification_performs_paid_work_in_the_current_analysis_job(name):
    snapshot=prepared(coverage_dossier());owner,job=analysis_context()
    before=(owner.used,job.used)
    out=seam_call(name,snapshot,job)
    assert out is not None and job.used>before[1]
    assert owner.used-before[0]==job.used-before[1]
    assert not hasattr(out,"processing_state")


@pytest.mark.parametrize("name",["basis","conflicts","identity","coverage"])
@pytest.mark.parametrize("stopped",[False,True],ids=["finished","resource_stopped"])
def test_finalization_cannot_resume_documentary_analysis(name,stopped):
    snapshot=prepared(coverage_dossier());owner,job=analysis_context()
    if stopped:
        with pytest.raises(_AnalysisAborted): job.charge(1_000_001)
    else:
        owner.finish_job(job)
    finalizer=owner.begin_finalization();finalizer.charge(1)
    before=owner.used
    with pytest.raises((TypeError,AttributeError)):
        seam_call(name,snapshot,finalizer)
    assert owner.used==before
    finalizer.check()


@pytest.mark.parametrize("name",["basis","conflicts","identity","coverage"])
@pytest.mark.parametrize("finalizing",[False,True])
def test_interrupted_qualification_cannot_become_an_epistemic_nonresult_or_complete_check(name,finalizing):
    snapshot=prepared(coverage_dossier());owner,job=analysis_context()
    with pytest.raises(_AnalysisAborted) as original: job.charge(1_000_001)
    if finalizing: owner.begin_finalization()
    before=(owner.used,job.used)
    with pytest.raises(_AnalysisAborted) as repeated: seam_call(name,snapshot,job)
    assert repeated.value is original.value and repeated.value.limit_id=="WU9-L11"
    assert repeated.value.stop.reason_code=="resource_limit_reached"
    assert (owner.used,job.used)==before


@pytest.mark.parametrize("name",["basis","conflicts","identity","coverage"])
def test_exhaustion_during_qualification_never_returns_a_completed_fact(name):
    snapshot=prepared(coverage_dossier());owner,job=analysis_context()
    job.charge(999_995)
    with pytest.raises(_AnalysisAborted) as stopped:
        seam_call(name,snapshot,job)
    assert stopped.value.limit_id=="WU9-L11"
    assert stopped.value.stop.execution_state=="interrupted"
    assert stopped.value.stop.reason_code=="resource_limit_reached"
    assert 999_995<=job.used<=1_000_000
    after=(owner.used,job.used)
    with pytest.raises(_AnalysisAborted) as repeated: seam_call(name,snapshot,job)
    assert repeated.value is stopped.value and (owner.used,job.used)==after


@pytest.mark.parametrize("name",["basis","conflicts","identity","coverage"])
def test_deadline_stops_qualification_before_work_without_fabricating_evidence_gaps(name,monkeypatch):
    snapshot=prepared(coverage_dossier());now=[0]
    monkeypatch.setattr(resources,"monotonic_ns",lambda:now[0])
    owner,job=analysis_context();before=(owner.used,job.used)
    now[0]=60_000_000_001
    with pytest.raises(_AnalysisAborted) as stopped: seam_call(name,snapshot,job)
    assert stopped.value.limit_id=="WU9-L12"
    assert stopped.value.stop.reason_code=="resource_limit_reached"
    assert (owner.used,job.used)==before
