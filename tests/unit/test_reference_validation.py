# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Snapshot-global identity, typed endpoints and preservation counterexamples."""
import copy
import importlib.util
from pathlib import Path
import pytest
from source_integrity_toolkit.runtime.boundary import _prepare_value
from source_integrity_toolkit.contracts.evidence import _PreparedBundle

_spec = importlib.util.spec_from_file_location("sit_w05_reference_cases", Path(__file__).resolve().parents[1] / "contract/test_typed_records.py")
case = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(case)


@pytest.mark.parametrize("left", ["inquiries", "records", "assertions", "evidence_references"])
@pytest.mark.parametrize("right", ["inquiries", "records", "assertions", "evidence_references"])
def test_duplicate_ids_are_global_even_across_collections(left, right):
    b = case.rich()
    if left == right:
        b[right].append(copy.deepcopy(b[left][0]))
    else:
        b[right][0]["id"] = b[left][0]["id"]
    case.check_rejected(b, "duplicate_identifier")


@pytest.mark.parametrize("identifier", ["", " bad", "bad ", "a/b", "/a", ".bad", "_bad", "-bad", "a\\b", "a\n", "a\0", "é", "a" * 129])
def test_identifiers_are_exact_bounded_ascii_tokens(identifier):
    b = case.sparse(); b["bundle_id"] = identifier
    case.check_rejected(b, "input_constraint_violation")


@pytest.mark.parametrize("field", ["target_claim_refs", "target_object_refs", "seed_artifact_refs", "seed_evidence_refs", "coverage_assertion_refs"])
def test_dangling_local_references_cannot_import_a_predecessor(field):
    b = case.rich(); b["inquiries"][0][field] = ["outside-snapshot"]
    b["predecessor"] = {"bundle_id": "outside-snapshot", "snapshot_id": "older"}
    case.check_rejected(b, "dangling_reference")


@pytest.mark.parametrize("field", ["target_claim_refs", "seed_artifact_refs", "seed_evidence_refs", "coverage_assertion_refs"])
def test_reference_arrays_do_not_silently_deduplicate(field):
    b = case.rich(); b["inquiries"][0][field] *= 2
    case.check_rejected(b, "type_or_enum_violation")


def test_compatible_unresolved_material_is_admitted_but_not_resolved():
    b = case.pool(); case.by_id(b, "e")["data"]["artifact_ref"] = "unresolved"
    b["inquiries"][0]["seed_artifact_refs"].append("unresolved")
    result = _prepare_value(b)
    assert isinstance(result, _PreparedBundle)
    unresolved = next(e for e in result.entities if e.identifier == "unresolved")
    assert unresolved.kind == "unresolved_reference"
    assert sum(link.target.identifier == "unresolved" for link in result.links) == 2
    case.by_id(b, "unresolved")["data"]["expected_kinds"] = ["actor"]
    case.check_rejected(b, "endpoint_or_claim_mismatch")


def test_same_protected_key_and_same_names_do_not_merge_ids():
    b = case.pool(); u = copy.deepcopy(case.by_id(b, "unresolved")); u["id"] = "Unresolved"; b["records"].append(u)
    result = _prepare_value(b)
    assert isinstance(result, _PreparedBundle)
    assert {e.identifier for e in result.entities if e.kind == "unresolved_reference"} == {"unresolved", "Unresolved"}


def test_unrelated_and_late_malformed_records_cannot_be_salvaged_away():
    b = case.pool(); unrelated = copy.deepcopy(case.by_id(b, "model")); unrelated["id"] = "zz-late"
    unrelated["data"]["provider_ref"] = "not-in-snapshot"; b["records"].append(unrelated)
    case.check_rejected(b, "dangling_reference")


@pytest.mark.parametrize("role,target", [("candidate", "channel"), ("generator", "artifact"), ("judge", "claim"), ("executor", "e"),
    ("human_reviewer", "model"), ("reference_answer", "actor"), ("rubric", "actor"), ("validation_environment", "model"), ("method_input", "claim")])
def test_role_kind_rules_hold_without_implied_voting_or_execution(role, target):
    b = case.pool(); case.by_id(b, "evaluation")["data"]["role_bindings"] = [{"role": role, "object_ref": target, "evidence_ref_ids": [], "qualifications": []}]
    case.check_rejected(b, "endpoint_or_claim_mismatch")


def test_human_reviewer_specialization_does_not_accept_an_organization_label():
    b = case.pool(); case.by_id(b, "actor")["data"]["actor_kind"] = "organization"
    case.by_id(b, "evaluation")["data"]["role_bindings"][1]["role"] = "human_reviewer"
    case.check_rejected(b, "endpoint_or_claim_mismatch")
    case.by_id(b, "unresolved")["data"].update(expected_kinds=["actor"], description="Protected fictional human reviewer; identity withheld")
    case.by_id(b, "evaluation")["data"]["role_bindings"][1]["object_ref"] = "unresolved"
    assert isinstance(_prepare_value(b), _PreparedBundle)


def test_correction_case_and_before_target_checks_do_not_compute_authority():
    b = case.pool(); case.by_id(b, "handling")["data"]["case_ref"] = "change"
    case.check_rejected(b, "endpoint_or_claim_mismatch")
    case.by_id(b, "handling")["data"]["case_ref"] = "submission"
    case.by_id(b, "change")["data"]["details"]["before_ref"] = "claim2"
    case.check_rejected(b, "endpoint_or_claim_mismatch")


def test_removal_and_unknown_after_state_remain_distinct():
    b = case.pool(); details = case.by_id(b, "change")["data"]["details"]
    details.update(action_type="withdraw", after_ref=None, after_absence_reason="Explicit recorded withdrawal")
    assert isinstance(_prepare_value(b), _PreparedBundle)
    details["after_absence_reason"] = None; case.check_rejected(b, "type_or_enum_violation")
    details.update(after_ref="unresolved", after_absence_reason=None)
    case.by_id(b, "unresolved")["data"]["expected_kinds"] = ["claim"]
    assert isinstance(_prepare_value(b), _PreparedBundle)


def test_claim_scope_must_fit_every_named_inquiry_and_seed():
    b = case.pool(); a = case.relation("supports"); b["assertions"] = [a]
    second = copy.deepcopy(b["inquiries"][0]); second["id"] = "inquiry2"; second["target_claim_refs"] = ["claim2"]
    second["seed_evidence_refs"] = []; b["inquiries"].append(second); a["scope"]["inquiry_refs"].append("inquiry2")
    case.check_rejected(b, "endpoint_or_claim_mismatch")
    a["scope"]["inquiry_refs"] = ["inquiry"]
    second["seed_evidence_refs"] = ["e"]
    case.check_rejected(b, "endpoint_or_claim_mismatch")


def test_externality_cannot_reference_an_inquiry_outside_its_declared_scope():
    b = case.rich(); second = copy.deepcopy(b["inquiries"][0]); second["id"] = "inquiry2"; b["inquiries"].append(second)
    case.by_id(b, "a-externality")["data"]["details"]["boundary_inquiry_ref"] = "inquiry2"
    case.check_rejected(b, "endpoint_or_claim_mismatch")


def test_trained_on_dataset_specialization_is_separate_from_an_artifact_name():
    b = case.pool(); a = case.relation("trained_on"); b["assertions"] = [a]; a["data"]["to_ref"] = "artifact"
    case.check_rejected(b, "endpoint_or_claim_mismatch")
    a["data"]["to_ref"] = "unresolved"
    assert isinstance(_prepare_value(b), _PreparedBundle)


def test_coverage_and_verification_links_require_the_specific_assertion_kind():
    b = case.rich(); case.by_id(b, "a-origin_boundary")["data"]["details"]["coverage_ref"] = "a-verification"
    case.check_rejected(b, "endpoint_or_claim_mismatch")
    case.by_id(b, "a-origin_boundary")["data"]["details"]["coverage_ref"] = "a-coverage"
    case.by_id(b, "a-classification")["data"]["details"]["verification_assessment_refs"] = ["a-coverage"]
    case.check_rejected(b, "endpoint_or_claim_mismatch")
