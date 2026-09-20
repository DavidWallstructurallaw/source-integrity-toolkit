# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Hand-authored canonical cases and full W05 closed-shape counterexamples."""
import copy
import json
import pytest
from source_integrity_toolkit.runtime.boundary import _prepare_value, _prepare_utf8, _capture_value
from source_integrity_toolkit.contracts.evidence import _PreparedBundle
from source_integrity_toolkit.runtime.diagnostics import _SafeDiagnostic
from source_integrity_toolkit.contracts.constants import SHAPES


def unknown():
    return {"state": "unknown", "value": None, "precision": None, "reason": "Fictional timing not supplied."}


def window():
    return {"start": unknown(), "end": unknown()}


def provenance():
    return {"attributed_to_ref": "actor", "basis_kind": "declaration", "evidence_ref_ids": [],
            "method": "Hand-authored fictional conformance case.", "qualifications": ["Unverified supplied declaration."]}


def record(identifier, kind, data):
    return {"id": identifier, "kind": kind, "data": data, "provenance": provenance()}


def sparse():
    return {"contract_version": "sit-bundle/0.1", "bundle_id": "bundle", "snapshot_id": "snapshot",
        "recorded_at": unknown(), "predecessor": None,
        "inquiries": [{"id": "inquiry", "target_claim_refs": ["claim"], "target_object_refs": [],
            "seed_artifact_refs": [], "seed_evidence_refs": [],
            "boundary": {"description": "Fictional boundary", "criterion": "Only supplied source bindings", "system_refs": []},
            "time_window": window(), "as_of": unknown(), "dependency_dimensions": [],
            "coverage_assertion_refs": [], "provenance": provenance()}],
        "records": [record("actor", "actor", {"actor_kind": "human", "identity_disclosure": "pseudonymous", "display_name": "Fictional reviewer"}),
            record("claim", "claim", {"claim_key": "claim-family", "version_label": "v1", "text": "Fictional claim", "context": "Synthetic context"})],
        "assertions": [], "evidence_references": []}


def pool():
    b = sparse()
    b["predecessor"] = {"bundle_id": "older", "snapshot_id": "old-snapshot"}
    for name, kind in (("artifact", "document"), ("artifact2", "document"), ("dataset", "dataset")):
        b["records"].append(record(name, "artifact", {"artifact_kind": kind, "work_key": name,
            "version_label": "v1", "locators": [], "published_at": unknown(), "retrieved_at": unknown(),
            "content_evidence_refs": [], "checksums": [{"algorithm": "declared", "value": "not-verified", "covered_material": "fictional"}]}))
    b["records"].append(record("claim2", "claim", {"claim_key": "claim-family", "version_label": "v2", "text": "Different fictional claim version", "context": "Synthetic"}))
    for name, artifact in (("e", "artifact"), ("e2", "artifact2")):
        b["records"].append(record(name, "evidence_item", {"claim_ref": "claim", "artifact_ref": artifact, "locator": "paragraph", "epistemic_type": "fictional_example", "description": "Supplied contribution"}))
    for name in ("origin", "origin2"):
        b["records"].append(record(name, "origin_event", {"event_kind": "data_collection", "event_key": name,
            "performed_by_refs": ["actor"], "method_ref": "artifact", "occurred_at": unknown(), "description": "Fictional acquisition"}))
    for name in ("model", "model2"):
        b["records"].append(record(name, "model", {"model_key": name, "version_label": "v1", "family_label": "same label is no identity proof", "provider_ref": "actor"}))
    b["records"].append(record("evaluation", "evaluation", {"evaluation_kind": "execution", "target_refs": ["claim"],
        "role_bindings": [{"role": "candidate", "object_ref": "claim", "evidence_ref_ids": [], "qualifications": []},
                          {"role": "executor", "object_ref": "actor", "evidence_ref_ids": [], "qualifications": []}],
        "result_refs": ["artifact"], "occurred_at": unknown(), "review_contribution": None}))
    channel = record("channel", "correction_channel", {"owner_refs": ["actor"], "target_refs": ["claim"],
        "contact_locator": None, "declared_action_types": ["review", "withdraw"], "valid_window": window()})
    channel["gaps"] = [{"field": "data.contact_locator", "reason": "withheld", "detail": "No source contact is authorized."}]
    b["records"].append(channel)
    for name, details in (("submission", {"submission_kind": "objection", "summary": "Fictional correction request"}),
        ("handling", {"outcome": "accepted", "reason": "Recorded handling only"}),
        ("change", {"action_type": "amend", "before_ref": "claim", "after_ref": "claim2", "after_absence_reason": None, "linkage_description": "Supplied change link"})):
        b["records"].append(record(name, "correction_event", {"event_kind": name, "case_ref": None if name == "submission" else "submission",
            "channel_ref": "channel", "target_refs": ["claim"], "occurred_at": unknown(), "details": details}))
    b["records"].append(record("pipeline", "pipeline_record", {"subject_ref": "e", "run_key": "run", "stage_key": "stage", "stage": "influence",
        "state": "unknown", "output_refs": ["artifact"], "observed_at": unknown(), "linkage_kind": "unspecified", "detail": "No inference from missing evidence"}))
    b["records"].append(record("anomaly", "anomaly", {"inquiry_refs": ["inquiry"], "claim_ref": None, "original_context": "Fictional unclassified anomaly",
        "context_evidence_ref": None, "classification_state": "unclassified", "caller_label": None, "comparison_note": "No frequency asserted"}))
    b["records"].append(record("unresolved", "unresolved_reference", {"expected_kinds": ["artifact"], "reason": "withheld",
        "description": "Protected fictional material", "protected_key": "opaque shared label"}))
    b["evidence_references"] = [{"id": "support", "reference_kind": "supplied_excerpt", "availability": "supplied", "artifact_ref": "artifact",
        "record_ref": None, "locator": None, "excerpt": "Fictional supplied excerpt", "provided_by_ref": "actor", "attestor_ref": None, "scope_note": "Only a supplied basis"}]
    b["inquiries"][0]["seed_artifact_refs"] = ["artifact", "artifact2"]
    b["inquiries"][0]["seed_evidence_refs"] = ["e", "e2"]
    b["inquiries"][0]["target_object_refs"] = ["evaluation"]
    b["inquiries"][0]["dependency_dimensions"] = ["acquisition"]
    return b


def assertion(identifier, assertion_kind, data):
    return {"id": identifier, "assertion_kind": assertion_kind,
        "scope": {"inquiry_refs": ["inquiry"], "claim_refs": ["claim"], "effective_window": window()},
        "provenance": provenance(), "asserted_at": unknown(), "lifecycle_state": "active", "lifecycle_basis_ref_ids": [], "data": data}


RELATIONS = {
    "supports": ("e", "claim", None, {}), "contradicts": ("e", "claim", None, {}),
    "describes": ("e", "claim", None, {}), "qualifies": ("e", "claim", None, {}),
    "contextualizes": ("e", "claim", None, {}), "corroborates": ("e", "e2", None, {}),
    "cites": ("artifact", "artifact2", None, {"citation_locator": "line"}),
    "derived_from": ("e", "e2", "acquisition", {"transformer_ref": "actor", "method_ref": "artifact", "occurred_at": unknown(), "portion_note": "Fictional"}),
    "copies": ("e", "e2", "acquisition", {}), "syndicated_from": ("e", "e2", "acquisition", {}),
    "summarizes": ("e", "e2", "acquisition", {}), "translates": ("e", "e2", "acquisition", {}),
    "quotes": ("e", "e2", "acquisition", {}), "originates_from": ("e", "origin", "acquisition", {}),
    "depends_on": ("origin", "origin2", "acquisition", {}), "generated_by": ("artifact", "model", None, {"valid_window": window()}),
    "published_by": ("artifact", "actor", None, {}), "model_derived_from": ("model", "model2", "model_ancestry", {"occurred_at": unknown()}),
    "trained_on": ("model", "dataset", "model_ancestry", {}), "owned_by": ("model", "actor", "organizational_control", {}),
    "retrieved_from": ("artifact", "artifact2", None, {"retrieval_time": unknown()}),
    "propagates_to": ("channel", "claim", None, {"action_type": "review", "valid_window": window()}),
    "supersedes": ("claim", "claim2", None, {"reason": "Supplied succession"}),
    "same_identity_as": ("artifact", "artifact2", None, {"identity_level": "artifact_version"}),
}


def relation(pred):
    left, right, dim, details = copy.deepcopy(RELATIONS[pred])
    return assertion("r-" + pred, "relation", {"predicate": pred, "from_ref": left, "to_ref": right, "polarity": "affirmed", "dimension": dim, "details": details})


def assessments():
    return {
        "origin_boundary": (["origin"], {"dimension": "acquisition", "boundary_role": "declared_origin", "coverage_ref": "a-coverage", "termination_reason": "Supplied boundary only"}),
        "independence": (["origin", "origin2"], {"comparison_form": "pairwise", "dimension": "acquisition", "conclusion": "independent_process",
            "examined_dependency_refs": [], "unexamined_dimensions": [], "coverage_ref": "a-coverage", "scope_note": "Recorded comparison is not qualified"}),
        "coverage": (["inquiry"], {"coverage_kind": "upstream_history", "state": "complete_for_scope", "relation_types": ["originates_from"],
            "dimensions": ["acquisition"], "member_refs": ["e", "e2"], "omitted_refs": [], "universe_enumerated": True, "scope_note": "Supplied finite scope"}),
        "classification": (["artifact"], {"axis": "sil_governance_layer", "labels": ["verified"], "verification_assessment_refs": [], "scope_note": "Unsupported label retained"}),
        "verification": (["actor"], {"verification_scope": "identity", "evaluation_ref": "evaluation", "reported_outcome": "verified", "valid_window": window(), "scope_note": "Reported outcome only"}),
        "externality": (["origin"], {"boundary_inquiry_ref": "inquiry", "conclusion": "external", "grounding_basis": "Supplied description", "relevant_time": unknown()}),
        "authority": (["channel"], {"target_refs": ["claim"], "action_types": ["review"], "valid_window": window(), "authorized_by_ref": "actor", "grant_state": "denied", "authority_basis": "Supplied denial", "coverage_ref": "a-coverage"}),
        "capacity": (["channel"], {"reported_capacity": "unmeasured", "unit": "cases", "horizon": window(), "reported_load": "unmeasured", "scope_note": "No adequacy calculation"}),
        "conflict": (["r-supports", "r-contradicts"], {"conflict_kind": "affirmation_denial", "resolution_state": "unresolved", "resolution_evaluation_ref": None, "scope_note": "No automatic winner"}),
    }


def rich():
    b = pool()
    b["assertions"] = [relation(p) for p in RELATIONS]
    for kind, (subjects, details) in assessments().items():
        b["assertions"].append(assertion("a-" + kind, "assessment", {"assessment_kind": kind, "subject_refs": subjects, "details": details}))
    b["inquiries"][0]["coverage_assertion_refs"] = ["a-coverage"]
    return b


def by_id(b, identifier):
    for collection in ("inquiries", "records", "assertions", "evidence_references"):
        for obj in b[collection]:
            if obj["id"] == identifier:
                return obj
    raise AssertionError("synthetic_fixture_id_missing")


def shape_objects(b):
    # Independent hand-selected witnesses for every adopted shape. No validator
    # output is used to locate or construct the expected branch.
    r = lambda name: by_id(b, name)["data"]
    a = lambda name: by_id(b, "a-" + name)["data"]["details"]
    rel = lambda name: by_id(b, "r-" + name)["data"]["details"]
    return {"Bundle": b, "Predecessor": b["predecessor"], "TimeValue": b["recorded_at"], "TimeWindow": b["inquiries"][0]["time_window"],
        "Provenance": b["records"][0]["provenance"], "Gap": by_id(b, "channel")["gaps"][0], "EvidenceReference": b["evidence_references"][0],
        "Inquiry": b["inquiries"][0], "Boundary": b["inquiries"][0]["boundary"], "Record": b["records"][0],
        "ClaimData": r("claim"), "ArtifactData": r("artifact"), "Checksum": r("artifact")["checksums"][0], "ActorData": r("actor"),
        "EvidenceItemData": r("e"), "OriginEventData": r("origin"), "ModelData": r("model"), "EvaluationData": r("evaluation"),
        "RoleBinding": r("evaluation")["role_bindings"][0], "CorrectionChannelData": r("channel"), "CorrectionEventData": r("submission"),
        "SubmissionDetails": r("submission")["details"], "HandlingDetails": r("handling")["details"], "ChangeDetails": r("change")["details"],
        "PipelineRecordData": r("pipeline"), "AnomalyData": r("anomaly"), "UnresolvedReferenceData": r("unresolved"),
        "Assertion": by_id(b, "r-supports"), "Scope": by_id(b, "r-supports")["scope"], "RelationData": by_id(b, "r-supports")["data"],
        "StanceDetails": rel("supports"), "CitationDetails": rel("cites"), "TransformationDetails": rel("derived_from"),
        "OriginDetails": rel("originates_from"), "AgentDetails": rel("generated_by"), "ModelDetails": rel("model_derived_from"),
        "RetrievalDetails": rel("retrieved_from"), "RouteDetails": rel("propagates_to"), "SupersessionDetails": rel("supersedes"),
        "IdentityDetails": rel("same_identity_as"), "AssessmentData": by_id(b, "a-origin_boundary")["data"],
        "OriginBoundaryDetails": a("origin_boundary"), "IndependenceDetails": a("independence"), "CoverageDetails": a("coverage"),
        "ClassificationDetails": a("classification"), "VerificationDetails": a("verification"), "ExternalityDetails": a("externality"),
        "AuthorityDetails": a("authority"), "CapacityDetails": a("capacity"), "ConflictDetails": a("conflict")}


def check_rejected(value, code=None):
    result = _prepare_value(value)
    assert type(result) is _SafeDiagnostic and result.input_state == "rejected"
    if code is not None:
        assert result.code == code
    assert not hasattr(result, "tree")
    return result


def test_hand_authored_witnesses_cover_fifty_shapes_and_all_record_kinds():
    b = rich()
    assert set(shape_objects(b)) == {s[0] for s in SHAPES} and len(shape_objects(b)) == 50
    assert {r["kind"] for r in b["records"]} == {"claim", "artifact", "actor", "evidence_item", "origin_event", "model", "evaluation", "correction_channel", "correction_event", "pipeline_record", "anomaly", "unresolved_reference"}
    assert isinstance(_prepare_value(b), _PreparedBundle)
    assert isinstance(_prepare_utf8(json.dumps(b).encode()), _PreparedBundle)


@pytest.mark.parametrize("shape", [s[0] for s in SHAPES])
def test_each_required_field_is_enforced_at_the_real_preparation_boundary(shape):
    fields = next(s[2] for s in SHAPES if s[0] == shape)
    for field, desc, required in fields:
        if not required:
            continue
        b = rich(); obj = shape_objects(b)[shape]; del obj[field]
        check_rejected(b, "missing_required_field")


@pytest.mark.parametrize("shape", [s[0] for s in SHAPES])
def test_every_closed_shape_rejects_unknown_fields_even_on_unselected_records(shape):
    b = rich(); shape_objects(b)[shape]["FICTIONAL_UNDECLARED_SECRET"] = None
    out = check_rejected(b, "type_or_enum_violation")
    assert "FICTIONAL_UNDECLARED_SECRET" not in repr(out) + str(out)


@pytest.mark.parametrize("shape", [s[0] for s in SHAPES])
def test_each_field_rejects_wrong_concrete_type_without_coercion(shape):
    for field, desc, required in next(s[2] for s in SHAPES if s[0] == shape):
        b = rich(); obj = shape_objects(b)[shape]
        obj[field] = "not-a-boolean" if desc == "bool" else True
        check_rejected(b)


@pytest.mark.parametrize("bad", [{}, {"not_a_declared_field": 1, "contract_version": "wrong"}])
def test_captured_values_cannot_masquerade_as_prepared_dossiers(bad):
    assert type(_capture_value(bad)).__name__ == "_CapturedBundle"
    check_rejected(bad)
    assert _prepare_utf8(json.dumps(bad).encode()).input_state == "rejected"


@pytest.mark.parametrize("mode", ["value", "bytes"])
def test_sparse_and_declared_unsupported_documentary_inputs_remain_valid(mode):
    b = sparse()
    for obj in b["records"] + b["inquiries"]:
        obj["provenance"]["basis_kind"] = "documented_record"
    result = _prepare_value(b) if mode == "value" else _prepare_utf8(json.dumps(b).encode())
    assert isinstance(result, _PreparedBundle)
    assert result.input_state == "accepted" and result.preparation_kind == "private_prepared_input"
    assert not any(hasattr(result, k) for k in ("results", "report_kind", "independent", "verified", "processing_state"))


@pytest.mark.parametrize("missing", ["data.version_label", "data.text", "provenance.attributed_to_ref", "provenance.method"])
def test_factual_nulls_require_an_exact_gap_and_retain_protected_content(missing):
    b = sparse(); obj = by_id(b, "claim"); parent, field = missing.split("."); obj[parent][field] = None
    if missing == "data.text":
        b["evidence_references"] = [{"id": "protected", "reference_kind": "external_locator", "availability": "withheld", "artifact_ref": None,
            "record_ref": None, "locator": "https://fictional.invalid/private", "excerpt": None, "provided_by_ref": "actor", "attestor_ref": None, "scope_note": "Protected claim"}]
        obj["data"]["content_evidence_ref"] = "protected"
    check_rejected(b, "missing_required_field")
    obj["gaps"] = [{"field": missing, "reason": "withheld", "detail": "Explicit fictional gap"}]
    assert isinstance(_prepare_value(b), _PreparedBundle)
    obj["gaps"][0]["field"] = "data.nonexistent"
    check_rejected(b)


@pytest.mark.parametrize("key", ["ns:", "namespace:payload", "中文:说明"])
def test_extensions_remain_opaque_ordered_and_cannot_grant_authority(key):
    b = sparse(); b["extensions"] = {key: {"score": 0.1, "steps": [3, 1, 2], "execute": "FICTIONAL_DO_NOT_EXECUTE"}}
    assert isinstance(_prepare_value(b), _PreparedBundle)
    b["extensions"] = {"no_namespace": None}
    check_rejected(b, "type_or_enum_violation")


def owner_path(bundle, target):
    def search(value, path):
        if value is target:
            return path
        if type(value) is dict:
            for key, child in value.items():
                found = search(child, path + "." + key if path else key)
                if found is not None: return found
        elif type(value) is list:
            for i, child in enumerate(value):
                found = search(child, path + "[" + str(i) + "]")
                if found is not None: return found
        return None
    for collection in ("inquiries", "records", "assertions", "evidence_references"):
        for owner in bundle[collection]:
            found = search(owner, "")
            if found is not None: return owner, found
    return bundle, search(bundle, "")


@pytest.mark.parametrize("shape", [s[0] for s in SHAPES if any("|null" in t for n, t, required in s[2])])
def test_each_nullable_field_has_an_admitted_explicit_unknown_or_structural_branch(shape):
    # Each conditional branch is hand-selected here. A general nullable marker
    # alone never authorizes null without the branch's required companion data.
    structural = {("Bundle", "predecessor"), ("TimeValue", "value"), ("TimeValue", "precision"),
        ("EvidenceReference", "artifact_ref"), ("EvidenceReference", "record_ref"), ("EvidenceReference", "locator"),
        ("EvidenceReference", "excerpt"), ("EvidenceReference", "attestor_ref"), ("EvaluationData", "review_contribution"),
        ("CorrectionEventData", "case_ref"), ("ChangeDetails", "after_ref"), ("ChangeDetails", "after_absence_reason"),
        ("AnomalyData", "claim_ref"), ("AnomalyData", "context_evidence_ref"), ("AnomalyData", "caller_label"),
        ("RelationData", "dimension"), ("ConflictDetails", "resolution_evaluation_ref")}
    for name, desc, required in next(s[2] for s in SHAPES if s[0] == shape):
        if "|null" not in desc: continue
        b = rich(); obj = shape_objects(b)[shape]; owner, prefix = owner_path(b, obj)
        obj[name] = None
        field = prefix + "." + name if prefix else name
        if (shape, name) not in structural:
            if not any(g["field"] == field for g in owner.get("gaps", [])):
                owner.setdefault("gaps", []).append({"field": field, "reason": "withheld", "detail": "Synthetic explicit missing value"})
        if shape == "ClaimData" and name == "text": obj["content_evidence_ref"] = "support"
        if shape == "AnomalyData" and name == "original_context": obj["context_evidence_ref"] = "support"
        if shape == "ChangeDetails" and name == "after_ref":
            obj["action_type"] = "withdraw"; obj["after_absence_reason"] = "Explicitly declared withdrawal with no after object."
        if shape == "EvidenceReference" and name == "artifact_ref":
            owner.setdefault("gaps", []).append({"field": "artifact_ref", "reason": "not_recorded", "detail": "Supplied excerpt with undisclosed location"})
        if shape == "EvidenceReference" and name == "excerpt":
            obj["reference_kind"] = "record_pointer"; obj["record_ref"] = "claim"
        result = _prepare_value(b)
        assert isinstance(result, _PreparedBundle), (shape, name, result)
        if (shape, name) not in structural:
            owner["gaps"] = [g for g in owner["gaps"] if g["field"] != field]
            check_rejected(b, "missing_required_field")


@pytest.mark.parametrize("shape", [s[0] for s in SHAPES if any("@" in t for n, t, required in s[2])])
def test_each_enum_field_rejects_a_string_outside_its_closed_vocabulary(shape):
    for name, desc, required in next(s[2] for s in SHAPES if s[0] == shape):
        if "@" not in desc: continue
        b = rich(); obj = shape_objects(b)[shape]
        obj[name] = ["FICTIONAL_UNKNOWN_ENUM"] if desc.startswith(("*", "+")) else "FICTIONAL_UNKNOWN_ENUM"
        check_rejected(b, "type_or_enum_violation")


def test_gap_paths_are_real_owner_fields_or_the_exact_unmodeled_history_marker():
    b = rich(); owner = by_id(b, "claim")
    owner["gaps"] = [{"field": "unmodeled_history", "reason": "not_examined", "detail": "No history qualification"}]
    assert isinstance(_prepare_value(b), _PreparedBundle)
    owner["gaps"][0]["field"] = "data.not_a_canonical_field"
    check_rejected(b, "type_or_enum_violation")


@pytest.mark.parametrize("value", [0, 1.0, True, {}, []])
def test_capacity_descriptions_never_coerce_to_quantitative_policy(value):
    b = rich(); by_id(b, "a-capacity")["data"]["details"]["reported_capacity"] = value
    check_rejected(b, "type_or_enum_violation")
