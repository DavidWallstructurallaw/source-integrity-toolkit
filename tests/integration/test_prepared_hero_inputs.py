# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Actual frozen H7 preparation, safe stops and component/full-boundary isolation.

The harness reads fictional fixtures before handing bytes to the product. These
checks neither implement public file opening nor certify any analytical oracle.
"""
import ast
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
from dataclasses import FrozenInstanceError, fields
from unittest.mock import patch
import pytest
from source_integrity_toolkit.contracts.bundle import _Object, _Array, _Number, _CapturedBundle
from source_integrity_toolkit.contracts.evidence import _PreparedBundle
from source_integrity_toolkit.contracts.execution import _PreparationAborted
from source_integrity_toolkit.runtime import boundary
from source_integrity_toolkit.runtime.boundary import _prepare_value, _prepare_utf8, _capture_value
from source_integrity_toolkit.runtime.resources import _new_budget, _PreparationBudget
from source_integrity_toolkit.runtime.diagnostics import _SafeDiagnostic
from source_integrity_toolkit.validation.structure import _validate_structure, _capture_tree
from source_integrity_toolkit.validation.limits import _InputLedger

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location("sit_w05_integration_cases", ROOT / "tests/contract/test_typed_records.py")
cases = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cases)
CANARY = "FICTIONAL_SECRET_KEY_PATH_PAYLOAD_553981"
HEROES = ("H7-01", "H7-V01", "H7-V02", "H7-V03")


def logical(value):
    if type(value) is _Object:
        return {k: logical(v) for k, v in value.items}
    if type(value) is _Array:
        return [logical(v) for v in value.items]
    if type(value) is _Number:
        return (value.sign, value.coefficient, value.exponent, value.source_kind)
    return value


def outcome_surface(value):
    # This helper is used only for payload-free stop records, never for a
    # successful prepared object whose private tree intentionally holds input.
    return repr(value) + str(value) + "|".join(str(getattr(value, f.name)) for f in fields(value))


@pytest.mark.parametrize("case", HEROES)
@pytest.mark.parametrize("mode", ["value", "bytes"])
def test_all_frozen_hero_inputs_pass_actual_full_preparation(case, mode):
    raw = (ROOT / "tests/fixtures/hero" / (case + ".bundle.json")).read_bytes()
    source = json.loads(raw)
    result = _prepare_value(source) if mode == "value" else _prepare_utf8(raw)
    assert isinstance(result, _PreparedBundle) and result.input_state == "accepted"
    assert result.preparation_kind == "private_prepared_input"
    normalized = logical(result.tree)
    for collection in ("inquiries", "records", "assertions", "evidence_references"):
        assert len(normalized[collection]) == len(source[collection])
        assert [r["id"] for r in normalized[collection]] == sorted(r["id"] for r in source[collection])
        assert {r["id"] for r in normalized[collection]} == {r["id"] for r in source[collection]}
    assert len(result.entities) == sum(len(source[c]) for c in ("inquiries", "records", "assertions", "evidence_references"))
    original_seeds = {i["id"]: set(i["seed_evidence_refs"]) for i in source["inquiries"]}
    assert {i["id"]: set(i["seed_evidence_refs"]) for i in normalized["inquiries"]} == original_seeds
    assert len(result.plan) == len(source["inquiries"])
    for plan in result.plan:
        inquiry = plan.inquiry.identifier
        assert set(plan.assertion_refs) == {a["id"] for a in source["assertions"] if inquiry in a["scope"]["inquiry_refs"]}
        assert set(plan.anomaly_refs) == {r["id"] for r in source["records"] if r["kind"] == "anomaly" and inquiry in r["data"]["inquiry_refs"]}
    for r in normalized["records"]:
        before = cases.by_id(source, r["id"])
        assert r["kind"] == before["kind"]
        if r["kind"] in ("correction_event", "pipeline_record", "unresolved_reference"):
            expected_data = copy.deepcopy(before["data"])
            collections = {obj["id"]: name for name in ("inquiries", "records", "assertions", "evidence_references") for obj in source[name]}
            for field in ("target_refs", "output_refs"):
                if field in expected_data:
                    expected_data[field] = sorted(expected_data[field], key=lambda ref: (collections[ref], ref))
            assert r["data"] == expected_data
    for name in ("report_kind", "results", "findings", "available_result_refs", "processing_state", "hhi", "independent"):
        assert not hasattr(result, name)
    assert result.source_mode == ("constructed_value" if mode == "value" else "supplied_utf8")


def test_only_set_valued_fields_are_normalized_and_all_declared_content_survives():
    first = cases.rich()
    first["extensions"] = {"fictional:ordered": ["z", "a", [3, 1, 2]], "fictional:control": {"skip_validation": True}}
    first["inquiries"][0]["provenance"]["qualifications"] = ["z narrative", "a narrative"]
    second = copy.deepcopy(first)
    for name in ("inquiries", "records", "assertions", "evidence_references"):
        second[name].reverse()
    second["inquiries"][0]["seed_evidence_refs"].reverse()
    second["inquiries"][0]["seed_artifact_refs"].reverse()
    cases.by_id(second, "evaluation")["data"]["role_bindings"].reverse()
    cases.by_id(second, "a-coverage")["data"]["details"]["member_refs"].reverse()
    a, b = _prepare_value(first), _prepare_value(second)
    assert isinstance(a, _PreparedBundle) and isinstance(b, _PreparedBundle)
    assert logical(a.tree) == logical(b.tree)
    assert logical(a.tree)["extensions"]["fictional:ordered"][:2] == ["z", "a"]
    assert logical(a.tree)["inquiries"][0]["provenance"]["qualifications"] == ["z narrative", "a narrative"]
    assert [(x.owner.identifier, x.selector, x.target.identifier) for x in a.links] == [(x.owner.identifier, x.selector, x.target.identifier) for x in b.links]


def test_typed_reference_order_and_role_order_do_not_merge_identities():
    b = cases.rich()
    cases.by_id(b, "channel")["data"]["target_refs"] = ["claim", "a-coverage", "e"]
    out = logical(_prepare_value(b).tree)
    # Collection names precede IDs: assertions first, then records by ID.
    assert cases.by_id(out, "channel")["data"]["target_refs"] == ["a-coverage", "claim", "e"]
    roles = cases.by_id(out, "evaluation")["data"]["role_bindings"]
    assert [(r["role"], r["object_ref"]) for r in roles] == sorted((r["role"], r["object_ref"]) for r in roles)


def test_accepted_tree_is_deeply_immutable_and_does_not_retain_mutable_caller_storage():
    source = cases.rich()
    out = _prepare_value(source)
    before = logical(out.tree)
    source["records"].clear(); source["inquiries"][0]["target_claim_refs"].append(CANARY)
    assert logical(out.tree) == before
    stack = [out.tree]
    while stack:
        value = stack.pop()
        if type(value) is _Object:
            with pytest.raises(FrozenInstanceError): value.items = ()
            stack.extend(v for k, v in value.items)
        elif type(value) is _Array:
            with pytest.raises(FrozenInstanceError): value.items = ()
            stack.extend(value.items)
        else:
            assert value is None or type(value) in (str, bool, _Number)
    for record in (out, *out.entities, *out.links, *out.plan, *out.observations):
        assert not hasattr(record, "__dict__") and CANARY not in repr(record)


@pytest.mark.parametrize("mode", ["value", "bytes"])
@pytest.mark.parametrize("stage", ["_validate_structure", "_validate_references", "_validate_semantics", "_normalize", "_index", "_check_links", "_scope_plan", "_PreparedBundle"])
@pytest.mark.parametrize("fault", ["error", "cancel", "resource"])
def test_every_preacceptance_stage_stops_without_a_partial_usable_tree(mode, stage, fault):
    budget = _new_budget()
    def fail(*args, **kwargs):
        if fault == "error": raise RuntimeError(CANARY)
        if fault == "cancel": raise KeyboardInterrupt(CANARY)
        budget.interrupt("WU9-L11")
    source = cases.sparse()
    with patch.object(boundary, "_new_budget", return_value=budget), patch.object(boundary, stage, fail):
        out = _prepare_value(source) if mode == "value" else _prepare_utf8(json.dumps(source).encode())
    assert type(out) is _SafeDiagnostic and out.input_state == "not_completed"
    assert out.execution_state == {"error": "failed", "cancel": "cancelled", "resource": "interrupted"}[fault]
    assert not hasattr(out, "tree") and CANARY not in outcome_surface(out)
    assert budget.input_state == "not_completed"


@pytest.mark.parametrize("fault", ["error", "cancel", "resource"])
def test_after_acceptance_stop_preserves_actual_state_without_returning_partial_input(fault):
    original = _PreparationBudget.record_input_acceptance
    def record_then_stop(budget):
        original(budget)
        if fault == "error": raise RuntimeError(CANARY)
        if fault == "cancel": raise KeyboardInterrupt(CANARY)
        budget.interrupt("WU9-L11")
    with patch.object(_PreparationBudget, "record_input_acceptance", record_then_stop):
        out = _prepare_value(cases.sparse())
    assert type(out) is _SafeDiagnostic and out.input_state == "accepted"
    assert out.execution_state == {"error": "failed", "cancel": "cancelled", "resource": "interrupted"}[fault]
    assert CANARY not in outcome_surface(out) and not hasattr(out, "tree")


@pytest.mark.parametrize("delta", [-1, 0, 1])
@pytest.mark.parametrize("collection,ceiling,limit", [("inquiries", 32, "WU9-L03"), ("records", 10000, "WU9-L04"),
    ("assertions", 30000, "WU9-L05"), ("evidence_references", 10000, "WU9-L06")])
def test_whole_collection_guard_precedes_invalid_child_expansion(collection, ceiling, limit, delta):
    source = cases.sparse()
    source[collection] = [{}] * (ceiling + delta)
    # Capture is independently paid. This checks the exact W05 collection guard
    # before child shape checks, not acceptance of an otherwise invalid dossier.
    captured = _capture_value(source)
    assert type(captured) is _CapturedBundle
    budget = _new_budget(); ledger = _InputLedger(budget, "constructed_value")
    with pytest.raises(_PreparationAborted) as raised:
        _validate_structure(captured, ledger)
    if delta > 0:
        assert raised.value.limit_id == limit
    else:
        assert raised.value.diagnostic_code == "missing_required_field" and raised.value.limit_id is None


@pytest.mark.parametrize("remaining", [0, 1, 2])
def test_reference_occurrence_ledger_is_integrated_before_resolution(remaining):
    source = cases.sparse()
    captured = _capture_value(source)
    b = _new_budget(); ledger = _InputLedger(b, "constructed_value")
    ledger.add("reference_occurrences", 200000 - remaining)
    with pytest.raises(_PreparationAborted) as raised:
        _validate_structure(captured, ledger)
    assert raised.value.limit_id == "WU9-L07"


def test_semantic_second_pass_does_not_double_count_the_input_occurrences():
    from source_integrity_toolkit.validation import structure
    source = cases.rich(); counts = []; original = structure._shape_walk
    def observe(tree, ledger, *, count=True):
        result = original(tree, ledger, count=count)
        counts.append(ledger.snapshot())
        return result
    with patch.object(structure, "_shape_walk", observe), patch.object(boundary, "_shape_walk", observe):
        out = _prepare_value(source)
    assert isinstance(out, _PreparedBundle) and len(counts) == 2 and counts[0] == counts[1]
    assert counts[0][1:5] == (len(source["inquiries"]), len(source["records"]), len(source["assertions"]), len(source["evidence_references"]))
    assert counts[0][5] == len(out.links)


@pytest.mark.parametrize("size", [4095, 4096, 4097])
@pytest.mark.parametrize("mode", ["value", "bytes"])
def test_locator_bytes_have_their_own_guard_after_capture(size, mode):
    source = cases.rich(); cases.by_id(source, "artifact")["data"]["locators"] = ["x" * size]
    out = _prepare_value(source) if mode == "value" else _prepare_utf8(json.dumps(source).encode())
    if size <= 4096: assert isinstance(out, _PreparedBundle)
    else: assert out.code == "input_constraint_violation" and "locator" in out.qualifications[0]


def test_failures_do_not_leak_sensitive_values_to_diagnostics_stdout_or_stderr(capsys):
    source = cases.rich(); source[CANARY] = {"path": "/private/" + CANARY}
    out = _prepare_value(source)
    assert type(out) is _SafeDiagnostic and CANARY not in outcome_surface(out)
    assert capsys.readouterr() == ("", "")
    good = _prepare_value(cases.sparse())
    assert isinstance(good, _PreparedBundle)
    bad = _prepare_value({})
    assert type(bad) is _SafeDiagnostic and not hasattr(bad, "tree")
    next_good = _prepare_value(cases.sparse())
    assert isinstance(next_good, _PreparedBundle) and next_good is not good and next_good.tree is not good.tree


ISOLATED = r'''
import sys,json,dataclasses,typing,ctypes,socket
import encodings.idna
sys.path.insert(0,sys.argv[1])
from source_integrity_toolkit.runtime.boundary import _prepare_value,_prepare_utf8
from source_integrity_toolkit.contracts.evidence import _PreparedBundle
mode=sys.argv[2]
# The harness reads the fictional fixture before observation; product receives
# only already-owned bytes. This is never attributed to native file conformance.
with open(sys.argv[3],'rb') as f: raw=f.read()
source=json.loads(raw)
events=[]
def audit(event,args):
    if event=='open' or event.startswith('socket.') or event=='ctypes.dlopen':
        events.append(event)
        raise RuntimeError('blocked_effect')
sys.addaudithook(audit)
if mode=='negative-open':
    try: open('FICTIONAL_MUST_NOT_OPEN','rb')
    except RuntimeError: pass
elif mode=='negative-network':
    try: socket.getaddrinfo('fictional.invalid',443)
    except RuntimeError: pass
elif mode=='negative-native':
    try: ctypes.CDLL('FICTIONAL_MUST_NOT_LOAD')
    except RuntimeError: pass
else:
    if mode=='invalid': source['FICTIONAL_SECRET_KEY_PATH_PAYLOAD_553981']=True
    a=_prepare_value(source); b=_prepare_utf8(raw)
    assert type(b) is _PreparedBundle
    assert (type(a) is _PreparedBundle)==(mode=='success')
print(json.dumps({'events':events,'ok':True}))
'''


@pytest.mark.parametrize("mode", ["success", "invalid", "negative-open", "negative-network", "negative-native"])
def test_full_preparation_has_no_source_io_network_or_native_load(mode):
    result = subprocess.run([sys.executable, "-I", "-S", "-B", "-c", ISOLATED, str(ROOT / "src"), mode,
        str(ROOT / "tests/fixtures/hero/H7-01.bundle.json")], capture_output=True, text=True, timeout=60)
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    expected = {"negative-open": "open", "negative-network": "socket.getaddrinfo", "negative-native": "ctypes.dlopen"}
    assert data == {"ok": True, "events": [expected[mode]] if mode in expected else []}
    assert CANARY not in result.stdout + result.stderr


def test_input_does_not_select_private_budget_mode_or_validation_bypass():
    source = cases.sparse(); source["extensions"] = {"fictional:options": {"skip_validation": True, "budget": 999999999999}}
    source["inquiries"][0]["target_claim_refs"] = ["missing"]
    assert _prepare_value(source).code == "dangling_reference"
    for function, value in ((_prepare_value, cases.sparse()), (_prepare_utf8, b"{}")):
        with pytest.raises(TypeError): function(value, skip_validation=True)
        with pytest.raises(TypeError): function(value, budget=_new_budget())
    assert _prepare_value(_capture_value({})).code == "type_or_enum_violation"


def test_role_ordering_rebases_gap_selectors_and_retains_exact_original_context():
    first = cases.pool()
    evaluation = cases.by_id(first, "evaluation")
    evaluation["data"]["role_bindings"].reverse()
    evaluation["gaps"] = [{"field": "data.role_bindings[0].qualifications", "reason": "not_examined", "detail": "Executor-specific original qualification gap"}]
    second = copy.deepcopy(first)
    cases.by_id(second, "evaluation")["data"]["role_bindings"].reverse()
    cases.by_id(second, "evaluation")["gaps"][0]["field"] = "data.role_bindings[1].qualifications"
    a, b = _prepare_value(first), _prepare_value(second)
    assert isinstance(a, _PreparedBundle) and isinstance(b, _PreparedBundle)
    assert logical(a.tree) == logical(b.tree)
    assert logical(a.captured_tree) == first and logical(b.captured_tree) == second
    normalized = cases.by_id(logical(a.tree), "evaluation")
    assert normalized["gaps"][0]["field"] == "data.role_bindings[1].qualifications"
    assert normalized["data"]["role_bindings"][1]["role"] == "executor"
    assert normalized["gaps"][0]["detail"] == evaluation["gaps"][0]["detail"]


@pytest.mark.parametrize("case", HEROES)
def test_hero_input_populations_match_frozen_oracles_without_calculating_their_results(case):
    # Only the harness opens an oracle. No expected analytical value is passed
    # to the product. A successful preparation leaves all metric work pending.
    source = json.loads((ROOT / "tests/fixtures/hero" / (case + ".bundle.json")).read_bytes())
    oracle = json.loads((ROOT / "tests/golden" / (case + ".logical.json")).read_bytes())
    out = _prepare_value(source)
    assert isinstance(out, _PreparedBundle)
    normalized = logical(out.tree); populations = oracle["populations"]
    inquiry = cases.by_id(normalized, "H7-I1")
    assert set(inquiry["seed_artifact_refs"]) == set(populations["source_artifacts"])
    assert set(inquiry["seed_evidence_refs"]) == set(populations["source_contributions"])
    for identifier in ("H7-COV-ADM", "H7-COV-PRES", "H7-COV-SEL", "H7-COV-USE"):
        assert set(cases.by_id(normalized, identifier)["data"]["details"]["member_refs"]) == set(populations["pipeline_cohort"])
    assert set(cases.by_id(normalized, "H7-CHANNEL")["data"]["target_refs"]) == set(populations["correction_targets"])
    assert set(cases.by_id(normalized, "H7-IND12")["data"]["subject_refs"]) == set(populations["comparison_members"])
    assert cases.by_id(normalized, populations["ancestor_only_contribution"])["kind"] == "evidence_item"
    assert cases.by_id(normalized, populations["anomaly_outside_seeds_and_pipeline"])["kind"] == "anomaly"
    assert not hasattr(out, "results") and not hasattr(out, "selected_field_expectations")
