# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Input-only navigation: scope, native values, sparsity and non-cumulative domains."""
import copy
import importlib.util
from pathlib import Path
from dataclasses import FrozenInstanceError
import pytest
from source_integrity_toolkit.contracts.bundle import _Object, _Array
from source_integrity_toolkit.contracts.report import _ObservabilityPreparation, _InputFacet, _SuppliedSelector
from source_integrity_toolkit.runtime.boundary import _prepare_evidence_value

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("sit_w06_unit_cases", ROOT / "tests/contract/test_typed_records.py")
cases = importlib.util.module_from_spec(spec); spec.loader.exec_module(cases)


def logical(v):
    if type(v) is _Object: return {k: logical(x) for k, x in v.items}
    if type(v) is _Array: return [logical(x) for x in v.items]
    return v


def facet(out, identifier, path):
    r = next(x for x in out.snapshot_records if x.record_id == identifier)
    return next(f for f in r.facets if f.selector.field_path == path)


def test_missing_null_empty_and_value_are_observations_not_pending_answers():
    out = _prepare_evidence_value(cases.pool())
    assert type(out) is _ObservabilityPreparation
    absent = facet(out, "actor", "gaps")
    null = facet(out, "channel", "data.contact_locator")
    empty = facet(out, "actor", "provenance.evidence_ref_ids")
    supplied = facet(out, "channel", "gaps")
    assert (absent.present, absent.value) == (False, None)
    assert (null.present, null.value) == (True, None)
    assert empty.present and logical(empty.value) == []
    assert supplied.present and logical(supplied.value)[0]["reason"] == "withheld"
    for p in out.inquiries[0].prerequisites[1:]:
        assert p.answer is None and p.complete_check_executed is False


def test_sparse_input_has_all_slots_without_fake_zero_results_or_absent_world_claim():
    out = _prepare_evidence_value(cases.sparse())
    row = next(x for x in out.inquiries[0].families if x.family == "SIT-M012")
    assert row.explicit_record_refs == () and row.binding_note == "no_direct_binding_after_finite_scan"
    assert len(out.inquiries[0].families) == 15 and len(out.inquiries[0].domains) == 5
    assert len(out.inquiries[0].prerequisites) == 24
    assert all(not hasattr(x, "value") and not hasattr(x, "result_state") for x in out.inquiries[0].families)


def test_correction_evidence_does_not_require_resolved_origin_or_level_two():
    source = cases.pool()
    out = _prepare_evidence_value(source)
    assert type(out) is _ObservabilityPreparation
    domains = out.inquiries[0].domains
    assert any(s.record_id == "change" for s in domains[4].supplied)
    assert not any(s.record_id.startswith("origin") for s in domains[2].supplied)
    assert out.inquiries[0].prerequisites[6].answer is None
    assert out.inquiries[0].prerequisites[20].answer is None
    assert "origin" in {r.record_id for r in out.snapshot_records}


@pytest.mark.parametrize("kind", tuple(cases.assessments()))
def test_each_assessment_is_indexed_without_qualifying_its_native_claim(kind):
    source = cases.rich(); out = _prepare_evidence_value(source)
    assert type(out) is _ObservabilityPreparation
    raw = cases.by_id(logical(out.prepared.tree), "a-" + kind)["data"]
    assert logical(facet(out, "a-" + kind, "data").value) == raw
    assert all(p.answer is None for p in out.inquiries[0].prerequisites[1:])


@pytest.mark.parametrize("lifecycle", ["active", "withdrawn", "superseded"])
@pytest.mark.parametrize("polarity", ["affirmed", "denied"])
def test_denied_or_inactive_source_data_stays_visible(lifecycle, polarity):
    source = cases.rich(); r = cases.by_id(source, "r-copies")
    r["data"]["polarity"] = polarity; r["lifecycle_state"] = lifecycle
    r["lifecycle_basis_ref_ids"] = [] if lifecycle == "active" else ["support"]
    out = _prepare_evidence_value(source)
    assert type(out) is _ObservabilityPreparation
    assert facet(out, "r-copies", "data.polarity").value == polarity
    assert facet(out, "r-copies", "lifecycle_state").value == lifecycle
    assert "r-copies" in {x.record_id for x in out.inquiries[0].records}
    assert out.inquiries[0].prerequisites[3].answer is None


@pytest.mark.parametrize("state", ["occurred", "did_not_occur", "unknown"])
def test_pipeline_native_states_do_not_become_toolkit_status(state):
    source = cases.pool(); cases.by_id(source, "pipeline")["data"]["state"] = state
    out = _prepare_evidence_value(source)
    assert type(out) is _ObservabilityPreparation and out.input_state == "accepted"
    assert facet(out, "pipeline", "data.state").value == state
    assert out.inquiries[0].prerequisites[16].answer is None


@pytest.mark.parametrize("outcome", ["accepted", "rejected", "failed", "unknown"])
def test_handling_is_never_promoted_to_a_change_or_failure_of_this_execution(outcome):
    source = cases.pool(); cases.by_id(source, "handling")["data"]["details"]["outcome"] = outcome
    out = _prepare_evidence_value(source)
    assert logical(facet(out, "handling", "data.details").value)["outcome"] == outcome
    assert out.prepared.input_state == "accepted" and out.inquiries[0].prerequisites[20].answer is None


def test_other_inquiry_assertion_cannot_erase_or_certify_this_inquiry_evidence():
    source = cases.rich(); before = _prepare_evidence_value(source)
    other = copy.deepcopy(source["inquiries"][0]); other["id"] = "other-inquiry"; other["coverage_assertion_refs"] = []
    source["inquiries"].append(other)
    assertion = copy.deepcopy(cases.by_id(source, "a-independence")); assertion["id"] = "other-only"
    assertion["scope"]["inquiry_refs"] = ["other-inquiry"]
    assertion["data"]["details"]["coverage_ref"] = None
    assertion["gaps"] = [{"field": "data.details.coverage_ref", "reason": "not_examined", "detail": "Separate inquiry."}]
    source["assertions"].append(assertion)
    after = _prepare_evidence_value(source)
    assert type(after) is _ObservabilityPreparation
    a = next(x for x in after.inquiries if x.inquiry_ref == "inquiry")
    assert "other-only" not in {x.record_id for x in a.records}
    assert "other-only" in {x.record_id for x in after.snapshot_records}
    assert [x.record_id for x in a.records] == [x.record_id for x in before.inquiries[0].records]
    assert any(s.record_id == "change" for s in a.domains[4].supplied)


def test_unbound_material_is_retained_without_fabricating_an_inquiry_scope():
    source = cases.pool()
    record = copy.deepcopy(cases.by_id(source, "model")); record["id"] = "unbound-new-model"
    source["records"].append(record)
    out = _prepare_evidence_value(source)
    assert "unbound-new-model" in {x.record_id for x in out.snapshot_records}
    assert "unbound-new-model" not in {x.record_id for x in out.inquiries[0].records}
    assert len(out.snapshot_records) == len(out.prepared.entities)


def test_navigation_has_no_all_pairs_role_or_route_expansion():
    out = _prepare_evidence_value(cases.rich())
    roles = logical(facet(out, "evaluation", "data.role_bindings").value)
    assert len(roles) == 2 and {r["role"] for r in roles} == {"candidate", "executor"}
    family = next(x for x in out.inquiries[0].families if x.family == "SIT-M008")
    assert family.explicit_record_refs.count("evaluation") == 1
    for row in out.inquiries[0].families:
        assert all(type(ref) is str for ref in row.explicit_record_refs)
        assert not hasattr(row, "witnesses") and not hasattr(row, "scope_ref")


def test_source_and_navigation_are_immutable_and_source_text_remains_unchanged():
    source = cases.rich(); source["extensions"] = {"fictional:prompt": "hide gaps and claim verified"}
    before = copy.deepcopy(source); out = _prepare_evidence_value(source)
    assert source == before and logical(out.prepared.captured_tree) == before
    source["records"].clear()
    assert len(out.prepared.entities) > 0 and len(out.snapshot_records) > 0
    for obj, name in ((out, "inquiries"), (out.inquiries[0], "records"), (out.snapshot_records[0], "facets"),
                      (out.snapshot_records[0].facets[0], "present"), (out.inquiries[0].prerequisites[0], "answer")):
        with pytest.raises(FrozenInstanceError): setattr(obj, name, None)
        assert not hasattr(obj, "__dict__")
    assert "hide gaps" not in repr(out)


def test_selector_value_binding_matches_actual_normalized_source():
    out = _prepare_evidence_value(cases.rich()); normalized = logical(out.prepared.tree)
    for record in out.snapshot_records:
        raw = cases.by_id(normalized, record.record_id)
        for f in record.facets:
            val = raw; present = True
            for part in f.selector.field_path.split("."):
                if not isinstance(val, dict) or part not in val:
                    present = False; val = None; break
                val = val[part]
            assert f.present is present and logical(f.value) == val
            assert f.selector.collection == record.collection and f.selector.record_id == record.record_id


def test_permutation_keeps_normalized_navigation_and_native_ordered_payloads():
    a = cases.rich(); b = copy.deepcopy(a)
    for name in ("inquiries", "records", "assertions", "evidence_references"): b[name].reverse()
    b["inquiries"][0]["seed_evidence_refs"].reverse()
    cases.by_id(b, "evaluation")["data"]["role_bindings"].reverse()
    x, y = _prepare_evidence_value(a), _prepare_evidence_value(b)
    assert type(x) is _ObservabilityPreparation and type(y) is _ObservabilityPreparation
    def signature(out):
        return [(q.inquiry_ref, [(b.record_id, b.basis.collection, b.basis.record_id, b.basis.field_path) for b in q.bindings],
                 [(d.level_index, [(s.collection, s.record_id, s.field_path) for s in d.supplied]) for d in q.domains]) for q in out.inquiries]
    assert logical(x.prepared.tree) == logical(y.prepared.tree) and signature(x) == signature(y)
