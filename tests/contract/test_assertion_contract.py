# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Typed relation and assessment admission, never analytical qualification."""
import copy
import importlib.util
from pathlib import Path
import pytest
from source_integrity_toolkit.runtime.boundary import _prepare_value
from source_integrity_toolkit.contracts.evidence import _PreparedBundle

_spec = importlib.util.spec_from_file_location("sit_w05_synthetic_cases", Path(__file__).with_name("test_typed_records.py"))
case = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(case)


@pytest.mark.parametrize("predicate", list(case.RELATIONS))
@pytest.mark.parametrize("polarity", ["affirmed", "denied"])
def test_all_twenty_four_relations_are_admitted_in_both_polarities(predicate, polarity):
    b = case.pool(); a = case.relation(predicate); a["data"]["polarity"] = polarity; b["assertions"] = [a]
    result = _prepare_value(b)
    assert isinstance(result, _PreparedBundle)
    saved = next(e for e in result.entities if e.identifier == a["id"])
    assert dict(dict(saved.node.fields.items)["data"].items)["polarity"] == polarity
    assert not hasattr(result, "findings")


@pytest.mark.parametrize("predicate", list(case.RELATIONS))
def test_each_relation_refuses_an_inquiry_as_an_endpoint(predicate):
    b = case.pool(); a = case.relation(predicate); b["assertions"] = [a]
    for field in ("from_ref", "to_ref"):
        bad = copy.deepcopy(b); bad["assertions"][0]["data"][field] = "inquiry"
        case.check_rejected(bad, "endpoint_or_claim_mismatch")


@pytest.mark.parametrize("predicate", list(case.RELATIONS))
def test_each_relation_preserves_parallel_assertions_and_inactive_history(predicate):
    b = case.pool(); a = case.relation(predicate); other = copy.deepcopy(a); other["id"] += "-parallel"
    other["lifecycle_state"] = "withdrawn"; other["lifecycle_basis_ref_ids"] = ["support"]
    b["assertions"] = [a, other]
    result = _prepare_value(b)
    assert isinstance(result, _PreparedBundle)
    assert {e.identifier for e in result.entities if e.kind == "assertion"} == {a["id"], other["id"]}
    assert set(result.plan[0].assertion_refs) == {a["id"], other["id"]}


@pytest.mark.parametrize("kind", list(case.assessments()))
def test_each_assessment_kind_preserves_its_supplied_claim_without_qualification(kind):
    b = case.rich(); result = _prepare_value(b)
    assert isinstance(result, _PreparedBundle)
    entity = next(e for e in result.entities if e.identifier == "a-" + kind)
    assert dict(dict(entity.node.fields.items)["data"].items)["assessment_kind"] == kind
    assert not any(hasattr(result, name) for name in ("results", "overall_level", "independent_count", "hhi", "authority"))


@pytest.mark.parametrize("kind", list(case.assessments()))
def test_assessment_subject_kind_constraints_are_not_inferred_from_names(kind):
    b = case.rich(); a = case.by_id(b, "a-" + kind)
    a["data"]["subject_refs"] = ["support", "support2"] if kind in ("independence", "conflict") else ["support"]
    other = copy.deepcopy(b["evidence_references"][0]); other["id"] = "support2"; b["evidence_references"].append(other)
    case.check_rejected(b, "endpoint_or_claim_mismatch")


@pytest.mark.parametrize("kind,count", [("origin_boundary", 0), ("origin_boundary", 2), ("authority", 0), ("authority", 2),
    ("coverage", 0), ("conflict", 0), ("conflict", 1), ("independence", 0), ("independence", 1)])
def test_explicit_assessment_cardinality_is_checked(kind, count):
    b = case.rich(); a = case.by_id(b, "a-" + kind)
    a["data"]["subject_refs"] = a["data"]["subject_refs"][:count]
    if count == 2 and kind == "origin_boundary": a["data"]["subject_refs"] = ["origin", "origin2"]
    if count == 2 and kind == "authority":
        h = copy.deepcopy(case.by_id(b, "channel")); h["id"] = "channel2"; b["records"].append(h)
        a["data"]["subject_refs"] = ["channel", "channel2"]
    case.check_rejected(b, "endpoint_or_claim_mismatch")


@pytest.mark.parametrize("pred", ["derived_from", "copies", "syndicated_from", "summarizes", "translates", "quotes"])
def test_material_transformations_and_claim_transformations_stay_separate(pred):
    b = case.pool(); a = case.relation(pred); b["assertions"] = [a]
    assert isinstance(_prepare_value(b), _PreparedBundle)
    a["data"].update(from_ref="artifact", to_ref="artifact2", dimension=None); a["scope"]["claim_refs"] = []
    assert isinstance(_prepare_value(b), _PreparedBundle)
    a["data"]["dimension"] = "acquisition"
    case.check_rejected(b, "endpoint_or_claim_mismatch")


def test_cross_claim_evidence_links_are_rejected_without_claim_equivalence():
    b = case.pool(); a = case.relation("derived_from"); b["assertions"] = [a]
    b["inquiries"][0]["target_claim_refs"].append("claim2")
    case.by_id(b, "e2")["data"]["claim_ref"] = "claim2"; a["scope"]["claim_refs"].append("claim2")
    case.check_rejected(b, "endpoint_or_claim_mismatch")


def test_stance_requires_resolved_exact_bound_claim():
    b = case.pool(); a = case.relation("supports"); b["assertions"] = [a]
    b["inquiries"][0]["target_claim_refs"].append("claim2"); a["scope"]["claim_refs"].append("claim2")
    a["data"]["to_ref"] = "claim2"
    case.check_rejected(b, "endpoint_or_claim_mismatch")
    case.by_id(b, "unresolved")["data"]["expected_kinds"] = ["claim"]
    a["data"]["to_ref"] = "unresolved"
    case.check_rejected(b, "endpoint_or_claim_mismatch")


def test_pairwise_cannot_be_expanded_or_mixed_and_setwise_is_not_transitive():
    b = case.rich(); a = case.by_id(b, "a-independence")
    origin = copy.deepcopy(case.by_id(b, "origin")); origin["id"] = "origin3"; b["records"].append(origin)
    a["data"]["subject_refs"].append("origin3")
    case.check_rejected(b, "endpoint_or_claim_mismatch")
    a["data"]["details"]["comparison_form"] = "setwise"
    assert isinstance(_prepare_value(b), _PreparedBundle)
    a["data"]["subject_refs"][2] = "actor"
    case.check_rejected(b, "endpoint_or_claim_mismatch")


@pytest.mark.parametrize("pred", ["cites", "derived_from", "depends_on", "model_derived_from", "same_identity_as"])
def test_well_formed_self_relationships_survive_without_a_dag_requirement(pred):
    b = case.pool(); a = case.relation(pred); b["assertions"] = [a]
    a["data"]["to_ref"] = a["data"]["from_ref"]
    assert isinstance(_prepare_value(b), _PreparedBundle)


def test_supersedes_self_is_rejected_but_a_two_record_cycle_is_retained():
    b = case.pool(); a = case.relation("supersedes"); b["assertions"] = [a]
    a["data"]["to_ref"] = "claim"; case.check_rejected(b, "endpoint_or_claim_mismatch")
    a["data"]["to_ref"] = "claim2"; reverse = copy.deepcopy(a); reverse["id"] = "reverse"
    reverse["data"].update(from_ref="claim2", to_ref="claim"); b["assertions"].append(reverse)
    assert isinstance(_prepare_value(b), _PreparedBundle)


@pytest.mark.parametrize("alias", ["observed_by", "validated_by", "evaluated_by", "judged_by", "corrects", "appeals", "observes_independently"])
def test_candidate_aliases_never_bypass_the_closed_predicate_registry(alias):
    b = case.pool(); a = case.relation("supports"); a["data"]["predicate"] = alias; b["assertions"] = [a]
    case.check_rejected(b, "type_or_enum_violation")


def test_recorded_conflict_and_denied_authority_do_not_become_validation_failures():
    result = _prepare_value(case.rich())
    assert isinstance(result, _PreparedBundle)
    assert len(result.plan[0].assertion_refs) == 33
    assert not hasattr(result, "available_result_refs")
