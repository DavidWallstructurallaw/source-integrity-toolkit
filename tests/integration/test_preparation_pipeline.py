# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W07 independent integration cases from the frozen input contract.

Authority: lineage sections 2-5, 6-9, 13-14; architecture 17; plan 13.
Fixtures below are independently authored, not generated from SHAPES, schema,
validator answers or a golden analytical result. All material is fictional.
"""
import copy
from dataclasses import fields, is_dataclass
import hashlib
import json
from pathlib import Path
import pytest
from source_integrity_toolkit.contracts.bundle import _Object, _Array, _Number
from source_integrity_toolkit.contracts.evidence import _PreparedBundle
from source_integrity_toolkit.contracts.report import _ObservabilityPreparation
from source_integrity_toolkit.runtime import boundary
from source_integrity_toolkit.runtime.diagnostics import _SafeDiagnostic

ROOT = Path(__file__).resolve().parents[2]
COLLECTIONS = ("inquiries", "records", "assertions", "evidence_references")
MODES = ("admit-value", "admit-bytes", "navigate-value", "navigate-bytes")
CANARY = "FICTIONAL_W07_PRIVATE_318472"


def unknown():
    return {"state": "unknown", "value": None, "precision": None, "reason": "Fictional unknown time"}


def provenance():
    return {"attributed_to_ref": "A", "basis_kind": "declaration", "evidence_ref_ids": [],
            "method": "Independent fictional W07 case", "qualifications": []}


def record(identifier, kind, data):
    return {"id": identifier, "kind": kind, "data": data, "provenance": provenance()}


def dossier():
    records = [record("A", "actor", {"actor_kind": "human", "identity_disclosure": "pseudonymous", "display_name": "Fictional A"})]
    inquiries = []
    for suffix in ("a", "z"):
        c, a, e = "C-" + suffix, "AR-" + suffix, "E-" + suffix
        records.extend([
            record(c, "claim", {"claim_key": "shared-family", "version_label": suffix, "text": "Fictional claim " + suffix, "context": "Independent context " + suffix}),
            record(a, "artifact", {"artifact_kind": "document", "work_key": "same-work-label", "version_label": "v1", "locators": ["https://fictional.invalid/shared"], "published_at": unknown(), "retrieved_at": unknown(), "content_evidence_refs": []}),
            record(e, "evidence_item", {"claim_ref": c, "artifact_ref": a, "locator": "paragraph 1", "epistemic_type": "fictional_example", "description": "Independent contribution " + suffix}),
        ])
        inquiries.append({"id": "I-" + suffix, "target_claim_refs": [c], "target_object_refs": [],
            "seed_artifact_refs": [a], "seed_evidence_refs": [e],
            "boundary": {"description": "Fictional boundary " + suffix, "criterion": "Explicit supplied bindings", "system_refs": []},
            "time_window": {"start": unknown(), "end": unknown()}, "as_of": unknown(),
            "dependency_dimensions": [], "coverage_assertion_refs": [], "provenance": provenance()})
    for identifier in ("U-a", "U-z"):
        records.append(record(identifier, "unresolved_reference", {"expected_kinds": ["artifact"], "reason": "withheld", "description": "Fictional unavailable object", "protected_key": "same-protected-key"}))
    return {"contract_version": "sit-bundle/0.1", "bundle_id": "W07", "snapshot_id": "S1", "recorded_at": unknown(),
            "predecessor": None, "inquiries": inquiries, "records": records, "assertions": [], "evidence_references": []}


def find(source, identifier):
    return next(obj for collection in COLLECTIONS for obj in source[collection] if obj["id"] == identifier)


def execute(source, mode):
    functions = {"admit-value": boundary._prepare_value, "admit-bytes": boundary._prepare_utf8,
        "navigate-value": boundary._prepare_evidence_value, "navigate-bytes": boundary._prepare_evidence_utf8}
    value = json.dumps(source, ensure_ascii=True).encode("utf-8") if mode.endswith("bytes") else source
    return functions[mode](value)


def prepared(out):
    return out.prepared if type(out) is _ObservabilityPreparation else out


def plain(value):
    if type(value) is _Object: return {k: plain(v) for k, v in value.items}
    if type(value) is _Array: return [plain(v) for v in value.items]
    if type(value) is _Number: return (value.sign, value.coefficient, value.exponent, value.source_kind)
    return value


def assert_admitted(out, mode):
    expected = _ObservabilityPreparation if mode.startswith("navigate") else _PreparedBundle
    assert type(out) is expected and out.input_state == "accepted"
    if type(out) is _ObservabilityPreparation:
        for row in out.inquiries:
            assert [p.prerequisite for p in row.prerequisites if p.complete_check_executed] == ["PC01"]
            assert row.prerequisites[0].answer == "met"
            assert all(p.answer is None and not p.complete_check_executed for p in row.prerequisites[1:])
            assert len(row.families) == 15 and sum(len(f.field_keys) for f in row.families) == 57
            assert [d.level_index for d in row.domains] == [0, 1, 2, 3, 4]
    for name in ("results", "findings", "report_id", "max_level", "overall_level", "hhi", "available_result_refs"):
        assert not hasattr(out, name)


def assert_projection_matches_source(out):
    """Independent oracle: each observed value must resolve in retained source."""
    source = plain(out.prepared.tree)
    all_ids = {x["id"] for collection in COLLECTIONS for x in source[collection]}
    assert {x.record_id for x in out.snapshot_records} == all_ids
    for row in out.snapshot_records:
        owner = find(source, row.record_id)
        for facet in row.facets:
            current, present = owner, True
            for key in facet.selector.field_path.split("."):
                if type(current) is not dict or key not in current:
                    current, present = None, False
                    break
                current = current[key]
            assert facet.selector.record_id == row.record_id
            assert facet.selector.collection == row.collection
            assert (facet.present, plain(facet.value)) == (present, current)
    for inquiry in out.inquiries:
        assert all(b.record_id in all_ids and b.basis.record_id in all_ids for b in inquiry.bindings)
        assert all(p.answer is None for p in inquiry.prerequisites[1:])


@pytest.mark.parametrize("mode", MODES)
def test_independently_authored_two_inquiry_bundle_is_admitted_without_identity_merging(mode):
    source = dossier(); before = copy.deepcopy(source)
    out = execute(source, mode); assert_admitted(out, mode)
    raw = plain(prepared(out).tree)
    assert {x["id"] for x in raw["records"]} == {x["id"] for x in source["records"]}
    assert len(raw["records"]) == 9 and len(prepared(out).entities) == 11
    assert find(raw, "AR-a")["data"]["locators"] == find(raw, "AR-z")["data"]["locators"]
    assert find(raw, "U-a")["data"]["protected_key"] == find(raw, "U-z")["data"]["protected_key"]
    assert source == before and plain(prepared(out).captured_tree) == before
    if type(out) is _ObservabilityPreparation: assert_projection_matches_source(out)


DEFECTS = ("missing_root", "extra_root", "contract", "duplicate_global_id", "duplicate_ref",
    "dangling_seed", "wrong_seed_kind", "wrong_claim", "bad_time", "bad_enum", "absent_gap",
    "late_unbound_dangling", "late_unbound_extra", "predecessor_not_imported", "case_sensitive_ref")


def defect(source, name):
    if name == "missing_root": del source["snapshot_id"]
    elif name == "extra_root": source[CANARY] = True
    elif name == "contract": source["contract_version"] = "sit-bundle/unapproved"
    elif name == "duplicate_global_id": source["records"].append(copy.deepcopy(find(source, "A"))); source["records"][-1]["id"] = "I-a"
    elif name == "duplicate_ref": source["inquiries"][0]["seed_artifact_refs"] *= 2
    elif name == "dangling_seed": source["inquiries"][0]["seed_artifact_refs"] = ["absent"]
    elif name == "wrong_seed_kind": source["inquiries"][0]["seed_evidence_refs"] = ["AR-a"]
    elif name == "wrong_claim": source["inquiries"][0]["seed_evidence_refs"] = ["E-z"]
    elif name == "bad_time": source["recorded_at"] = {"state": "known", "value": "2026-09-19T12:00:00", "precision": "instant"}
    elif name == "bad_enum": find(source, "AR-a")["data"]["artifact_kind"] = "unregistered"
    elif name == "absent_gap": find(source, "C-a")["data"]["version_label"] = None
    elif name == "late_unbound_dangling": find(source, "U-z")["provenance"]["attributed_to_ref"] = "absent"
    elif name == "late_unbound_extra": find(source, "U-z")["data"]["is_verified"] = True
    elif name == "predecessor_not_imported": source["predecessor"] = {"bundle_id": "prior", "snapshot_id": "old"}; source["inquiries"][0]["seed_artifact_refs"] = ["prior-artifact"]
    elif name == "case_sensitive_ref": source["inquiries"][0]["seed_artifact_refs"] = ["ar-a"]
    else: raise AssertionError("unregistered_test_defect")
    return source


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("name", DEFECTS)
def test_late_or_selected_structural_defect_rejects_the_whole_snapshot(mode, name):
    source = defect(dossier(), name); before = copy.deepcopy(source)
    out = execute(source, mode)
    assert type(out) is _SafeDiagnostic and out.input_state == "rejected" and out.execution_state == "rejected"
    assert out.code not in ("execution_failed", "resource_limit_reached")
    assert not hasattr(out, "tree") and not hasattr(out, "inquiries") and not hasattr(out, "prepared")
    assert source == before and CANARY not in out.safe_message + repr(out)
    assert_admitted(execute(dossier(), mode), mode)


@pytest.mark.parametrize("mode", MODES)
@pytest.mark.parametrize("variant", ["null_with_gap", "unsupported_documentary", "unresolved", "valid_evidence_cycle", "artifact_only"])
def test_lawful_incompleteness_is_not_repaired_filtered_or_certified(mode, variant):
    source = dossier()
    if variant == "null_with_gap":
        obj = find(source, "C-a"); obj["data"]["version_label"] = None
        obj["gaps"] = [{"field": "data.version_label", "reason": "not_recorded", "detail": "Fictional missing version"}]
    elif variant == "unsupported_documentary": find(source, "C-a")["provenance"]["basis_kind"] = "documented_record"
    elif variant == "unresolved": find(source, "E-a")["data"]["artifact_ref"] = "U-a"
    elif variant == "artifact_only": source["inquiries"][0]["seed_evidence_refs"] = []
    else:
        source["assertions"] = [{"id": "cycle", "assertion_kind": "relation",
            "scope": {"inquiry_refs": ["I-a"], "claim_refs": ["C-a"], "effective_window": {"start": unknown(), "end": unknown()}},
            "provenance": provenance(), "asserted_at": unknown(), "lifecycle_state": "active", "lifecycle_basis_ref_ids": [],
            "data": {"predicate": "copies", "from_ref": "E-a", "to_ref": "E-a", "polarity": "affirmed", "dimension": "acquisition", "details": {}}}]
    before = copy.deepcopy(source); out = execute(source, mode); assert_admitted(out, mode)
    assert plain(prepared(out).captured_tree) == before and source == before
    if type(out) is _ObservabilityPreparation: assert_projection_matches_source(out)


def signature(value):
    # Logical comparison excludes only mode and original representation order.
    if type(value) in (_Object, _Array, _Number): return plain(value)
    if type(value) is tuple: return tuple(signature(x) for x in value)
    if is_dataclass(value):
        return tuple((f.name, signature(getattr(value, f.name))) for f in fields(value) if f.name not in ("source_mode", "captured_tree"))
    return value


@pytest.mark.parametrize("mode", ["navigate-value", "navigate-bytes"])
@pytest.mark.parametrize("variant", ["reverse", "object_keys", "transport_spacing"])
def test_semantically_equivalent_permutations_preserve_complete_navigation(mode, variant):
    a = dossier(); b = copy.deepcopy(a)
    if variant == "reverse":
        for name in COLLECTIONS: b[name].reverse()
    elif variant == "object_keys":
        def reverse(v):
            if type(v) is dict: return {k: reverse(x) for k, x in reversed(tuple(v.items()))}
            if type(v) is list: return [reverse(x) for x in v]
            return v
        b = reverse(b)
    x = execute(a, mode)
    y = boundary._prepare_evidence_utf8(json.dumps(b, indent=3, ensure_ascii=True).encode()) if variant == "transport_spacing" else execute(b, mode)
    assert_admitted(x, mode); assert_admitted(y, mode)
    assert signature(x) == signature(y)
    assert_projection_matches_source(y)


@pytest.mark.parametrize("mode", ["navigate-value", "navigate-bytes"])
def test_other_claim_material_changes_cannot_rewrite_this_inquiry_navigation(mode):
    a = dossier(); x = execute(a, mode); b = copy.deepcopy(a)
    find(b, "C-z")["data"]["text"] = CANARY
    find(b, "AR-z")["provenance"]["basis_kind"] = "documented_record"
    y = execute(b, mode); assert_admitted(y, mode)
    first = lambda out: next(i for i in out.inquiries if i.inquiry_ref == "I-a")
    assert signature(first(x)) == signature(first(y))
    assert find(plain(y.prepared.tree), "C-z")["data"]["text"] == CANARY
    assert "C-z" not in {r.record_id for r in first(y).records}
    assert "C-z" in {r.record_id for r in y.snapshot_records}


@pytest.mark.parametrize("mode", ["navigate-value", "navigate-bytes"])
def test_reused_snapshot_identifiers_never_reuse_previous_contents(mode):
    a = dossier(); old = execute(a, mode); before = signature(old)
    b = dossier(); find(b, "C-a")["data"]["text"] = "New caller-owned fictional payload"
    new = execute(b, mode); assert_admitted(new, mode)
    assert signature(old) == before and new is not old and new.prepared is not old.prepared
    assert find(plain(new.prepared.captured_tree), "C-a")["data"]["text"] == b["records"][1]["data"]["text"]
    assert signature(new) != before


@pytest.mark.parametrize("mode", ["navigate-value", "navigate-bytes"])
@pytest.mark.parametrize("lists", [29, 30, 31])
def test_actual_full_pipeline_nested_extension_depth_boundary(mode, lists):
    source = dossier(); value = None
    for unused in range(lists): value = [value]
    source["extensions"] = {"fictional:depth": value}
    out = execute(source, mode)
    # Root + extension object + list nesting: 31, 32 and 33 containers.
    if lists <= 30: assert_admitted(out, mode)
    else:
        assert type(out) is _SafeDiagnostic and out.execution_state == "interrupted"
        assert out.code == "resource_limit_reached" and out.qualifications == ("WU9-L02",)
        assert out.input_state == "not_completed"


@pytest.mark.parametrize("digits", [127, 128, 129])
def test_numeric_token_boundary_is_separate_from_exact_integer_range(digits):
    source = dossier(); source["extensions"] = {"fictional:number": "TOKEN_PLACEHOLDER"}
    raw = json.dumps(source).encode().replace(b'"TOKEN_PLACEHOLDER"', b"1" * digits)
    out = boundary._prepare_evidence_utf8(raw)
    assert type(out) is _SafeDiagnostic
    if digits <= 128:
        assert out.input_state == "rejected" and out.code == "input_constraint_violation"
        assert "exact integer" in out.qualifications[0]
    else:
        assert out.input_state == "not_completed" and out.code == "resource_limit_reached"
        assert out.execution_state == "interrupted"


@pytest.mark.parametrize("mode", ["navigate-value", "navigate-bytes"])
@pytest.mark.parametrize("hero", ["H7-01", "H7-V01", "H7-V02", "H7-V03"])
def test_frozen_hero_every_retained_facet_matches_its_real_source_selector(mode, hero):
    raw = (ROOT / "tests/fixtures/hero" / (hero + ".bundle.json")).read_bytes()
    out = execute(json.loads(raw), mode); assert_admitted(out, mode)
    assert_projection_matches_source(out)
    # The harness never imports or injects an HHI oracle into the product.
    assert not hasattr(out, "selected_field_expectations")


@pytest.mark.parametrize("mutation", ["missing_record", "wrong_presence", "wrong_value", "wrong_collection"])
def test_independent_projection_oracle_detects_deliberate_navigation_corruption(mutation):
    from dataclasses import replace
    out = boundary._prepare_evidence_value(dossier())
    assert_projection_matches_source(out)
    records = list(out.snapshot_records)
    if mutation == "missing_record": records.pop()
    else:
        index = next(i for i, r in enumerate(records) if r.record_id == "A")
        row = records[index]; facets = list(row.facets)
        at = next(i for i, f in enumerate(facets) if f.selector.field_path == "provenance.method")
        if mutation == "wrong_presence": facets[at] = replace(facets[at], present=False, value=None)
        elif mutation == "wrong_value": facets[at] = replace(facets[at], value="fabricated method")
        else: row = replace(row, collection="assertions")
        records[index] = replace(row, facets=tuple(facets))
    changed = replace(out, snapshot_records=tuple(records))
    with pytest.raises(AssertionError): assert_projection_matches_source(changed)


def test_w07_evidence_records_bind_exact_sources_and_independent_fixture_bytes():
    ledger = json.loads((ROOT / "phase2/implementation_evidence.json").read_bytes())
    for path, expected in ledger["source_identities"].items():
        assert hashlib.sha256((ROOT / path).read_bytes()).hexdigest() == expected
    row = ledger["input_identities"][0]
    assert row["factory"] == "tests/integration/test_preparation_pipeline.py::dossier"
    assert hashlib.sha256(Path(__file__).read_bytes()).hexdigest() == row["factory_file_sha256"]
    raw = json.dumps(dossier(), sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()
    assert hashlib.sha256(raw).hexdigest() == row["canonical_json_sha256"]
    for row in ledger["input_identities"][1:]:
        assert hashlib.sha256((ROOT / row["path"]).read_bytes()).hexdigest() == row["sha256"]
    assert ledger["domain_traces_closed"] == [] and ledger["domain_test_obligations"]["count"] == 228
    assert ledger["whole_prerequisites_implemented"] == ["PC01"]
