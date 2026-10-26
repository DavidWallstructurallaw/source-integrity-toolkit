# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""P4-W02 direct report-contract checks against independent source examples.

The finite schema evaluator below is a test aid for the keywords actually used
by this repository's report schema. It is not a general JSON Schema service or
a claim of Draft 2020-12 conformance. Runtime code never reads the schema.
"""
import copy
import itertools
import json
import math
from pathlib import Path
import re

import pytest

from source_integrity_toolkit.contracts import report as report_contract
from source_integrity_toolkit.contracts import execution


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT / "schemas/report/sit-report-0.1.schema.json"
REFERENCE_PATH = ROOT / "tests/golden/phase4_reference_report.json"
ROOT_MEMBERS = (
    "contract_version", "report_kind", "report_id", "run", "input_identity",
    "input_validation", "scopes", "populations", "basis_index", "capabilities",
    "checks", "observability_domains", "results", "findings", "reasons",
    "release_limits",
)
RUN_PAIRS = (
    ("audit_report", "completed", "accepted"),
    ("audit_report", "interrupted", "accepted"),
    ("validation_diagnostics", "rejected", "rejected"),
    ("processing_diagnostics", "interrupted", "not_completed"),
    ("processing_diagnostics", "failed", "accepted"),
    ("processing_diagnostics", "failed", "not_completed"),
)
RESULT_PAIRS = (
    ("completed", "available"), ("completed", "unavailable"),
    ("completed", "not_applicable"), ("not_performed", "not_evaluated"),
    ("interrupted", "not_evaluated"), ("failed", "not_evaluated"),
)
MAX_INTEGER = 9_007_199_254_740_991
SCHEMA_KEYWORDS = {
    "$schema", "$id", "$comment", "title", "description", "$defs", "$ref",
    "type", "enum", "const", "properties", "required", "additionalProperties",
    "items", "minItems", "maxItems", "uniqueItems", "minLength", "maxLength",
    "pattern", "minimum", "maximum", "allOf", "anyOf", "oneOf", "not",
    "if", "then", "else",
}


def load_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            assert key not in result, ("duplicate_json_key", key)
            result[key] = value
        return result
    return json.loads(path.read_bytes(), object_pairs_hook=unique)


_REPORT_SCHEMA = None


def report_schema():
    """Reuse only the file schema's decoded, test-read-only value."""
    global _REPORT_SCHEMA
    if _REPORT_SCHEMA is None:
        _REPORT_SCHEMA = load_json(SCHEMA_PATH)
    return _REPORT_SCHEMA


@pytest.fixture(scope="module", autouse=True)
def _verify_report_schema_remains_unchanged():
    original_bytes = SCHEMA_PATH.read_bytes()
    cached = report_schema()
    fresh = load_json(SCHEMA_PATH)
    assert cached == fresh
    assert json.dumps(cached, sort_keys=True) == json.dumps(fresh, sort_keys=True)
    try:
        yield
    finally:
        fresh = load_json(SCHEMA_PATH)
        assert report_schema() is cached
        assert cached == fresh
        assert json.dumps(cached, sort_keys=True) == json.dumps(fresh, sort_keys=True)
        assert SCHEMA_PATH.read_bytes() == original_bytes


def json_equal(left, right):
    """JSON scalar equality keeps booleans separate from numbers."""
    if type(left) in (int, float) and type(right) in (int, float):
        return left == right
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return left.keys() == right.keys() and all(
            json_equal(left[key], right[key]) for key in left)
    if type(left) is list:
        return len(left) == len(right) and all(
            json_equal(a, b) for a, b in zip(left, right))
    return left == right


def schema_accepts(value, rule, schema):
    """Finite JSON-value evaluator; unsupported assertions fail loudly.

    JSON Schema integers include integral JSON numbers such as 1.0. The
    in-process Python report contract separately requires exact built-in ints.
    """
    if type(rule) is bool:
        return rule
    assert type(rule) is dict and set(rule) <= SCHEMA_KEYWORDS, set(rule) - SCHEMA_KEYWORDS
    if "$ref" in rule:
        ref = rule["$ref"]
        assert ref.startswith("#/$defs/") and ref.count("/") == 2
        if not schema_accepts(value, schema["$defs"][ref.split("/")[-1]], schema):
            return False
    if "type" in rule:
        kinds = rule["type"] if type(rule["type"]) is list else [rule["type"]]
        accepted = {"null": value is None, "boolean": type(value) is bool,
                    "integer": type(value) is int or (type(value) is float and
                        math.isfinite(value) and value.is_integer()),
                    "number": type(value) is int or (type(value) is float and math.isfinite(value)),
                    "string": type(value) is str, "array": type(value) is list,
                    "object": type(value) is dict}
        assert set(kinds) <= set(accepted)
        if not any(accepted[kind] for kind in kinds):
            return False
    if "const" in rule and not json_equal(value, rule["const"]):
        return False
    if "enum" in rule and not any(json_equal(value, item) for item in rule["enum"]):
        return False
    if type(value) is dict:
        if any(key not in value for key in rule.get("required", [])):
            return False
        props = rule.get("properties", {})
        for key, item in value.items():
            if key in props:
                if not schema_accepts(item, props[key], schema):
                    return False
            elif "additionalProperties" in rule and not schema_accepts(
                    item, rule["additionalProperties"], schema):
                return False
    if type(value) is list:
        if len(value) < rule.get("minItems", 0) or len(value) > rule.get("maxItems", len(value)):
            return False
        if "items" in rule and not all(schema_accepts(item, rule["items"], schema) for item in value):
            return False
        if rule.get("uniqueItems") and any(json_equal(value[i], value[j])
                for i in range(len(value)) for j in range(i)):
            return False
    if type(value) is str:
        if len(value) < rule.get("minLength", 0) or len(value) > rule.get("maxLength", len(value)):
            return False
        if "pattern" in rule and re.search(rule["pattern"], value) is None:
            return False
    if type(value) in (int, float):
        if "minimum" in rule and value < rule["minimum"]:
            return False
        if "maximum" in rule and value > rule["maximum"]:
            return False
    for keyword in ("allOf", "anyOf", "oneOf"):
        if keyword in rule:
            accepted = [schema_accepts(value, item, schema) for item in rule[keyword]]
            if keyword == "allOf" and not all(accepted):
                return False
            if keyword == "anyOf" and not any(accepted):
                return False
            if keyword == "oneOf" and sum(accepted) != 1:
                return False
    if "not" in rule and schema_accepts(value, rule["not"], schema):
        return False
    if "if" in rule:
        branch = "then" if schema_accepts(value, rule["if"], schema) else "else"
        if branch in rule and not schema_accepts(value, rule[branch], schema):
            return False
    return True


class RecordingPort:
    """Project test-owned port; no public invocation accepts this object."""
    def __init__(self, stop_after=None):
        self.units = 0
        self.checks = 0
        self.stop_after = stop_after

    def charge(self, units):
        assert type(units) is int and units >= 0
        if self.stop_after is not None and self.units + units > self.stop_after:
            raise RuntimeError("controlled_test_stop")
        self.units += units

    def check(self):
        self.checks += 1


def validate(document):
    port = RecordingPort()
    report_contract._validate_report_document(document, port)
    return port


def test_finite_schema_evaluator_positive_and_single_constraint_negatives():
    schema = {"$defs": {"Item": {"type": "integer", "minimum": 0, "maximum": 2}}}
    rule = {"type": "object", "properties": {"items": {"type": "array",
            "items": {"$ref": "#/$defs/Item"}, "minItems": 1, "maxItems": 2,
            "uniqueItems": True}}, "required": ["items"], "additionalProperties": False}
    assert schema_accepts({"items": [0, 2]}, rule, schema)
    for bad in ({}, {"items": []}, {"items": [0, 1, 2]}, {"items": [0, 0]},
                {"items": [True]}, {"items": [-1]}, {"items": [3]},
                {"items": [0], "extra": None}):
        assert not schema_accepts(bad, rule, schema)
    assert schema_accepts("a", {"oneOf": [{"const": "a"}, {"const": "b"}]}, schema)
    assert not schema_accepts("a", {"oneOf": [{"const": "a"}, {"type": "string"}]}, schema)
    assert not schema_accepts(True, {"enum": [1]}, schema)
    assert not schema_accepts(0, {"not": {"const": 0}}, schema)
    conditional = {"if": {"type": "integer"}, "then": {"minimum": 2},
                   "else": {"type": "string", "pattern": "^a$", "minLength": 1}}
    assert schema_accepts(2, conditional, schema)
    assert schema_accepts("a", conditional, schema)
    assert not schema_accepts(1, conditional, schema)
    assert not schema_accepts("b", conditional, schema)
    with pytest.raises(AssertionError):
        schema_accepts({}, {"unsupportedValidation": True}, schema)


RELEASE_LIMITS = [
    "Offline analysis of caller-supplied records only.",
    "Source identity, authenticity and external events are not independently authenticated.",
    "No live monitoring or active content-level poisoning, injection or authorship detection was performed.",
    "No universal truth, integrity, independence or safety score is produced.",
    "No automatic intervention, source contact or changes to the audited system are performed.",
    "Scope-specific evidence gaps and qualifications remain as recorded; missing records do not establish outside-world absence.",
]


def diagnostic_document(kind="processing_diagnostics", state="failed", input_state="not_completed"):
    """Literal source-shaped example; not produced by a runtime or renderer."""
    code = "input_constraint_violation" if state == "rejected" else (
        "resource_limit_reached" if state == "interrupted" else "execution_failed")
    diagnostic = {"code": code, "location": None,
                  "safe_message": "Processing did not complete.",
                  "qualifications": ["No source-quality conclusion."]}
    if state == "rejected":
        diagnostic["code"] = "invalid_syntax"
    clock = {"state": "unknown", "value": None, "precision": None,
             "reason": "not_recorded_by_SIT-RP-0.1"}
    document = {
        "contract_version": "sit-report/0.1", "report_kind": kind,
        "report_id": "SIT-RPT-000001",
        "run": {"processing_state": state, "tool_name": "Source Integrity Toolkit",
                "tool_version": "0.1.0.dev0", "input_contract_version": "sit-bundle/0.1",
                "requested_diagnostic_ids": ["SIT-M%03d" % n for n in range(1, 16)],
                "completed_diagnostic_ids": [], "started_at": dict(clock),
                "finished_at": dict(clock), "diagnostics": [diagnostic],
                "qualifications": ["SIT-RP-0.1",
                    "Wall-clock start and finish times are not recorded by SIT-RP-0.1."]},
        "input_identity": {"source_mode": "in_process", "input_contract_version": None,
                           "bundle_id": None, "snapshot_id": None,
                           "declared_predecessor": None, "raw_file_digest": None,
                           "qualifications": ["In-process input has no raw file bytes.",
                                              "Identifiers unavailable before completed parsing."]},
        "input_validation": {"state": input_state,
                             "diagnostics": [copy.deepcopy(diagnostic)] if state == "rejected" else []},
        "scopes": [], "populations": [], "basis_index": [], "capabilities": [],
        "checks": [], "observability_domains": [], "results": [], "findings": [],
        "reasons": [], "release_limits": list(RELEASE_LIMITS),
    }
    if input_state == "accepted":
        # Accepted input has already passed the required bundle identity
        # fields. A later processing failure does not erase that known fact.
        document["input_identity"].update(
            input_contract_version="sit-bundle/0.1", bundle_id="BUNDLE-1",
            snapshot_id="SNAPSHOT-1", qualifications=[
                "In-process input has no raw file bytes.",
                "Input identity was accepted before the later processing failure."])
    return document


def assert_both(document):
    schema = report_schema()
    assert schema_accepts(document, schema, schema)
    return validate(document)


def assert_rejected(document, *, schema_too=True):
    if schema_too:
        schema = report_schema()
        assert not schema_accepts(document, schema, schema)
    with pytest.raises(TypeError):
        validate(document)


@pytest.mark.parametrize("kind,state,input_state", RUN_PAIRS[2:])
def test_all_four_diagnostic_state_combinations_preserve_actual_acceptance(kind, state, input_state):
    doc = diagnostic_document(kind, state, input_state)
    port = assert_both(doc)
    assert port.units > 0
    frozen = report_contract._freeze_report_document(doc, RecordingPort())
    assert frozen["run"]["processing_state"] == state
    assert frozen["input_validation"]["state"] == input_state


@pytest.mark.parametrize("kind,state,input_state", [p for p in itertools.product(
    ("audit_report", "validation_diagnostics", "processing_diagnostics"),
    ("completed", "interrupted", "rejected", "failed"),
    ("accepted", "rejected", "not_completed")) if p not in RUN_PAIRS])
def test_forbidden_run_state_combinations_do_not_promote_acceptance(kind, state, input_state):
    baseline = diagnostic_document()
    assert_both(baseline)
    baseline["report_kind"] = kind
    baseline["run"]["processing_state"] = state
    baseline["input_validation"]["state"] = input_state
    assert_rejected(baseline)


@pytest.mark.parametrize("member", ROOT_MEMBERS)
@pytest.mark.parametrize("mode", ("missing", "wrong_type"))
def test_each_of_sixteen_root_members_is_required_and_typed(member, mode):
    doc = diagnostic_document()
    assert set(doc) == set(ROOT_MEMBERS)
    assert_both(doc)
    if mode == "missing":
        del doc[member]
    else:
        doc[member] = True
    assert_rejected(doc)


@pytest.mark.parametrize("member", ("witnesses", "overall_level", "max_level", "integrity_score",
                                    "publication_state", "_prepared", "_json_bytes"))
def test_report_root_rejects_new_scores_private_trees_and_transport_members(member):
    doc = diagnostic_document()
    assert_both(doc)
    doc[member] = None
    assert_rejected(doc)


def test_immutable_document_is_deeply_detached_and_has_no_mutable_mapping_backing():
    from collections.abc import Mapping
    doc = diagnostic_document()
    frozen = report_contract._freeze_report_document(doc, RecordingPort())
    assert isinstance(frozen, Mapping)
    assert tuple(frozen) == ROOT_MEMBERS or set(frozen) == set(ROOT_MEMBERS)
    doc["run"]["qualifications"].append("caller mutation")
    doc["run"]["tool_name"] = "caller replacement"
    doc["release_limits"].clear()
    assert frozen["run"]["tool_name"] == "Source Integrity Toolkit"
    assert frozen["run"]["qualifications"] == (
        "SIT-RP-0.1", "Wall-clock start and finish times are not recorded by SIT-RP-0.1.")
    assert frozen["release_limits"] == tuple(RELEASE_LIMITS)
    stack = [frozen]
    while stack:
        item = stack.pop()
        assert not isinstance(item, (dict, list))
        if isinstance(item, Mapping):
            assert not hasattr(item, "__dict__")
            with pytest.raises((TypeError, AttributeError)):
                item["intruder"] = None
            stack.extend(item.values())
        elif type(item) is tuple:
            stack.extend(item)
        else:
            assert type(item) in (str, bool, int, type(None))


@pytest.mark.parametrize("amount", (0, 1, 20, 100))
def test_contract_work_propagates_controlled_stop_without_returning_a_partial_document(amount):
    with pytest.raises(RuntimeError, match="^controlled_test_stop$"):
        report_contract._freeze_report_document(diagnostic_document(), RecordingPort(amount))


@pytest.mark.parametrize("bad", (True, 1, 1.0, None, [], (), "document"))
def test_root_requires_exact_owned_object_shape(bad):
    with pytest.raises(TypeError):
        validate(bad)


def test_cyclic_containers_are_rejected_without_recursion_escape():
    doc = diagnostic_document()
    doc["run"]["diagnostics"].append(doc)
    with pytest.raises(TypeError):
        validate(doc)


def test_public_report_type_is_declared_without_a_fabricated_success_constructor():
    assert isinstance(report_contract.AuditReport, type)
    for args in ((), ({},), (diagnostic_document(),)):
        with pytest.raises(TypeError):
            report_contract.AuditReport(*args)
    for name in ROOT_MEMBERS:
        assert isinstance(report_contract.AuditReport.__dict__[name], property)
        assert report_contract.AuditReport.__dict__[name].fset is None
    assert callable(report_contract.AuditReport.to_json_bytes)
    assert callable(report_contract.AuditReport.to_markdown_bytes)


def test_reference_envelope_is_accepted_by_both_independent_contract_surfaces():
    doc = load_json(REFERENCE_PATH)
    assert set(doc) == set(ROOT_MEMBERS)
    assert doc["report_kind"] == "audit_report"
    assert doc["run"]["processing_state"] == "completed"
    assert doc["input_validation"]["state"] == "accepted"
    assert_both(doc)


@pytest.mark.parametrize("state,reason", (("interrupted", "resource_limit_reached"),
                                         ("failed", "execution_failed")))
@pytest.mark.parametrize("input_state", ("accepted", "not_completed"))
def test_abort_retains_actual_states_and_only_fixed_safe_text(state, reason, input_state):
    error = execution.AuditAbort(state, input_state, reason)
    assert isinstance(error, Exception)
    assert error.processing_state == state
    assert error.input_validation_state == input_state
    assert error.reason_code == reason
    assert error.publication_state == "not_published"
    assert error.args == ("Audit could not be completed.",)
    assert str(error) == error.safe_message == "Audit could not be completed."
    assert repr(error) == "AuditAbort()"
    with pytest.raises((AttributeError, TypeError)):
        error.input_validation_state = "accepted" if input_state != "accepted" else "rejected"
    with pytest.raises(execution.AuditAbort) as caught:
        raise error
    assert caught.value is error


@pytest.mark.parametrize("state,reason", (("completed", "resource_limit_reached"),
    ("failed", "resource_limit_reached"), ("interrupted", "execution_failed"),
    ("failed", "caller_secret"), ("cancelled", "resource_limit_reached")))
def test_abort_rejects_invented_or_mismatched_stop_classification(state, reason):
    with pytest.raises(TypeError, match="^invalid_audit_transport$"):
        execution.AuditAbort(state, "accepted", reason)


@pytest.mark.parametrize("input_state", ("rejected", "unknown", True, None, "private input"))
def test_abort_and_cancellation_cannot_invent_a_validation_state(input_state):
    if input_state == "rejected":
        # W07 reaches diagnostic output after structural rejection. Architecture
        # 18.4 preserves actual validation state when later output failure wins.
        error = execution.AuditAbort("failed", input_state, "execution_failed")
        assert error.input_validation_state == "rejected"
        assert error.processing_state == "failed"
        assert error.reason_code == "execution_failed"
    else:
        with pytest.raises(TypeError, match="^invalid_audit_transport$"):
            execution.AuditAbort("failed", input_state, "execution_failed")
    with pytest.raises(TypeError, match="^invalid_audit_transport$"):
        execution.AuditCancelled(input_state)


@pytest.mark.parametrize("publication", ("published", "unknown", "private path", True, None))
def test_phase4_transports_cannot_claim_publication(publication):
    with pytest.raises(TypeError):
        execution.AuditAbort("failed", "accepted", "execution_failed", publication)
    with pytest.raises(TypeError):
        execution.AuditCancelled("accepted", publication)


@pytest.mark.parametrize("input_state", ("accepted", "not_completed"))
def test_cancellation_is_payload_free_and_does_not_fabricate_a_report_reason(input_state):
    error = execution.AuditCancelled(input_state)
    assert error.input_validation_state == input_state
    assert error.publication_state == "not_published"
    assert error.args == ("Audit cancelled.",)
    assert str(error) == error.safe_message == "Audit cancelled."
    assert repr(error) == "AuditCancelled()"
    assert not hasattr(error, "reason_code")


def test_usage_error_has_only_the_fixed_trusted_invocation_message_and_code():
    error = execution.AuditUsageError()
    assert isinstance(error, ValueError)
    assert error.code == "invalid_invocation"
    assert error.args == ("Invalid audit invocation.",)
    assert str(error) == error.safe_message == "Invalid audit invocation."
    assert repr(error) == "AuditUsageError()"
    for value in ("secret key", {"secret": "value"}, ValueError("private path")):
        with pytest.raises(TypeError):
            execution.AuditUsageError(value)


def test_hostile_protocols_cannot_run_during_contract_or_transport_rejection():
    calls = []

    def trip(self, *args, **kwargs):
        calls.append("protocol")
        raise AssertionError("hostile_protocol_executed")

    class Hostile:
        __iter__ = __eq__ = __hash__ = __repr__ = __str__ = __bool__ = __index__ = trip

    class HostileDict(dict):
        __iter__ = __getitem__ = items = keys = values = __len__ = trip

    class HostileList(list):
        __iter__ = __getitem__ = __len__ = trip

    class HostileStr(str):
        __iter__ = __eq__ = __hash__ = __repr__ = __str__ = __len__ = trip

    class HostileInt(int):
        __eq__ = __hash__ = __repr__ = __str__ = __index__ = trip

    for bad in (Hostile(), HostileDict(), HostileList(), HostileStr("x"), HostileInt(1)):
        with pytest.raises(TypeError):
            validate(bad)
        doc = diagnostic_document()
        doc["run"]["tool_name"] = bad
        with pytest.raises(TypeError):
            validate(doc)
        with pytest.raises(TypeError):
            execution.AuditAbort(bad, "accepted", "execution_failed")
        with pytest.raises(TypeError):
            execution.AuditCancelled(bad)
        assert calls == []


def test_w02_keeps_both_public_audit_functions_in_their_existing_refusal_state():
    import source_integrity_toolkit as package
    from tools import check_scaffold_boundary as guard

    state = guard.current_local_state(ROOT)
    if state["activation_stage"] < 8:
        assert package.__all__ == ("audit_bundle", "audit_file", "__version__")
        with pytest.raises(NotImplementedError):
            package.audit_bundle({})
    else:
        assert package.__all__ == ("audit_bundle", "audit_file", "__version__",
            "AuditReport", "AuditAbort", "AuditCancelled", "AuditUsageError")
        source = {}
        report = package.audit_bundle(source)
        assert type(report) is package.AuditReport and source == {}
        assert report.report_kind == "validation_diagnostics"
        assert report.input_validation["state"] == "rejected"
        json_bytes, markdown_bytes = report.to_json_bytes(), report.to_markdown_bytes()
        assert type(json_bytes) is bytes and type(markdown_bytes) is bytes
        document = json.loads(json_bytes)
        assert_both(document)
        assert document["run"]["processing_state"] == "rejected"
        assert document["input_validation"]["state"] == "rejected"
        assert b'"state": "rejected"' in markdown_bytes
        assert report.to_json_bytes() is json_bytes
        assert report.to_markdown_bytes() is markdown_bytes

        calls = []

        def touch(*args, **kwargs):
            calls.append("dossier touched")
            raise AssertionError("invalid options accessed the dossier")

        class Hostile:
            __getattribute__ = __repr__ = __str__ = __iter__ = __len__ = touch
            __bool__ = __getitem__ = __eq__ = __hash__ = touch

        with pytest.raises(package.AuditUsageError) as caught:
            package.audit_bundle(Hostile(), options={"raw_file_digest": True})
        assert str(caught.value) == "Invalid audit invocation."
        assert caught.value.code == "invalid_invocation"
        assert calls == []
    with pytest.raises(NotImplementedError):
        package.audit_file(object(), object())


# These are literal component examples derived from Reporting sections 12-18,
# Lineage 3.1, and the approved W02 projection choices. They intentionally do
# not claim assembly, disclosure execution, public delivery, or graph closure.
FIELD_CASES = tuple(
    ("SIT-M%03d" % family, field, kind)
    for family, kind, fields in (
        (1, "count", "nominal_seed_artifact_record_count unresolved_seed_artifact_reference_count seed_evidence_item_count claim_artifact_record_count claim_unassigned_seed_artifact_record_count"),
        (2, "count", "reached_origin_record_count documentary_origin_boundary_record_count"),
        (2, "record_disclosures", "origin_boundary_disclosures"),
        (3, "count", "submitted_comparison_member_count qualified_process_set_member_count qualified_origin_set_member_count"),
        (3, "record_disclosures", "independence_assessment_disclosures"),
        (4, "incidence", "per_seed_origin_memberships origin_incidence_counts"),
        (4, "partition", "seed_origin_dispositions"),
        (4, "fraction", "documentary_origin_resolution_fraction"),
        (5, "fraction", "single_origin_contribution_hhi"),
        (6, "partition", "immediate_evidence_layer_dispositions"),
        (6, "fraction", "inherited_only_seed_fraction"),
        (6, "completion_interval", "inherited_only_completion_interval"),
        (7, "count", "unresolved_frontier_reference_count unqualified_terminal_record_count seed_items_with_unresolved_ancestry_count"),
        (7, "record_disclosures", "ancestry_gap_disclosures"),
        (8, "count", "shared_recorded_ancestor_count matching_family_label_count"),
        (8, "record_disclosures", "evaluator_overlap_disclosures"),
        (8, "witness_collection", "evaluator_overlap_witnesses"),
        (9, "record_disclosures", "externality_assessment_disclosures externality_stage_links"),
        (10, "record_disclosures", "pipeline_stage_disclosures cohort_transition_disclosures"),
        (10, "partition", "stage_member_partition"),
        (10, "fraction", "stage_occurrence_fraction cohort_transition_fraction"),
        (10, "completion_interval", "stage_occurrence_completion_interval cohort_transition_completion_interval"),
        (11, "witness_collection", "declared_correction_route_witnesses applicable_authorized_route_witnesses"),
        (11, "record_disclosures", "correction_route_disclosures"),
        (12, "count", "correction_case_record_count handling_event_record_count linked_change_event_record_count documentary_linked_change_target_count cases_with_documentary_linked_change_count"),
        (12, "record_disclosures", "correction_case_disclosures correction_target_change_disclosures reported_capacity_disclosures"),
        (13, "record_disclosures", "corrective_independence_disclosures human_contribution_disclosures"),
        (14, "record_disclosures", "anomaly_context_disclosures contestation_disclosures tail_stage_result_links"),
        (15, "record_disclosures", "coverage_disclosures documentary_basis_gap_disclosures"),
        (15, "partition", "declared_basis_inventory reference_availability_inventory"),
    ) for field in fields.split()
)


def input_ref(identifier="REC-1", collection="records", selector=None):
    return {"collection": collection, "identifier": identifier, "selector": selector}


def time_value(state="unknown", value=None, precision=None, reason="Not recorded in this example."):
    result = {"state": state, "value": value, "precision": precision}
    if reason is not None:
        result["reason"] = reason
    return result


def result_example(family="SIT-M001", field="seed_evidence_item_count", kind="count"):
    return {
        "id": "SIT-RES-000001", "diagnostic_id": family, "field_key": field,
        "scope_ref": "SIT-SCP-000001", "population_refs": ["SIT-POP-000001"],
        "execution_state": "completed", "result_state": "available",
        "result_origin": "inventory", "value_kind": kind, "value": 2,
        "check_refs": ["SIT-CHK-000001"], "basis_refs": ["SIT-BAS-000001"],
        "witness_refs": [], "reason_refs": [],
        "interpretation_limit": "Counts supplied records in the named finite population only.",
    }


def partition_example(labels=("Y", "F", "U")):
    members = [input_ref("MEMBER-1"), input_ref("MEMBER-2")]
    return {"population_ref": "SIT-POP-000001", "categories": [
        {"label": label, "member_refs": ([members[0]] if i == 0 else
             [members[1]] if i == len(labels) - 1 else []),
         "count": 1 if i in (0, len(labels) - 1) else 0}
        for i, label in enumerate(labels)], "total": 2}


def interval_example():
    return {"lower": {"numerator": 1, "denominator": 2},
            "upper": {"numerator": 2, "denominator": 2},
            "interval_kind": "finite_cohort_completion",
            "population_ref": "SIT-POP-000001", "partition": partition_example()}


def incidence_example():
    first, second = input_ref("E1"), input_ref("E2")
    origin1, origin2 = input_ref("O1"), input_ref("O2")
    return {"population_ref": "SIT-POP-000001",
            "memberships": [{"member_ref": first, "origin_refs": [origin1, origin2]},
                            {"member_ref": second, "origin_refs": [origin1]}],
            "origin_counts": [{"origin_ref": origin1, "member_refs": [first, second], "count": 2},
                              {"origin_ref": origin2, "member_refs": [first], "count": 1}],
            "total": 2, "nonexclusive": True}


def provenance_example():
    return {"attributed_to_ref": "ACTOR-1", "basis_kind": "declaration",
            "evidence_ref_ids": [], "method": "Supplied source record.",
            "qualifications": ["No external authentication was performed."]}


def pipeline_record_example(state="unknown"):
    return {"id": "PIPE-1", "kind": "pipeline_record",
            "data": {"subject_ref": "ANOMALY-1", "run_key": "RUN-1", "stage_key": "STAGE-1",
                     "stage": "admission", "state": state, "output_refs": [],
                     "observed_at": time_value(), "linkage_kind": "declaration",
                     "detail": "The source records this stage state with an explicit limitation."},
            "provenance": provenance_example()}


def disclosure_example():
    return {"source": input_ref("PIPE-1"),
            "fields": {"native_record": pipeline_record_example(),
                       "qualification_state": "unmet", "reason_codes": ["support_uninspectable"]},
            "qualifications": ["Source-native unknown remains visible as data."]}


def graph_node(identifier="E1", kind="evidence_item"):
    return {"ref": input_ref(identifier), "kind": kind}


def graph_edge():
    return {"source": graph_node(), "target": graph_node("O1", "origin_event"),
            "source_ref": input_ref("A-1", "assertions"), "predicate": "originates_from",
            "eligible": True, "reason_codes": []}


def graph_component():
    return {"type": "graph_witness", "kind": "path", "nodes": [graph_node(), graph_node("O1", "origin_event")],
            "members": [], "starts": [], "examined_nodes": [],
            "frontiers": [], "terminals": [], "edges": [graph_edge()],
            "internal_edges": [], "exit_edges": [], "examined_edges": [], "observations": [],
            "target": None, "member_count": 3}


def component_examples():
    examples = {
        "InputRef": input_ref(),
        "InquiryRef": input_ref("I-1", "inquiries"),
        "RecordRef": input_ref(),
        "AssertionRef": input_ref("A-1", "assertions"),
        "EvidenceRef": input_ref("ER-1", "evidence_references"),
        "TimeValue": time_value(),
        "TimeWindow": {"start": time_value("known", "2024-02-29", "date", None),
                       "end": time_value(), "note": "The ending date was not recorded."},
        "Scope": {"id": "SIT-SCP-000001", "inquiry_ref": input_ref("I-1", "inquiries"),
                  "claim_refs": [input_ref("C-1")], "target_refs": [input_ref("E-1")],
                  "dependency_dimension": "acquisition", "graph_view": "claim_origin",
                  "temporal_basis": "snapshot_structural", "requested_time": None,
                  "coverage_refs": [], "qualifications": ["Supplied current snapshot only."]},
        "CaseTarget": {"case_ref": input_ref("CASE-1"), "before_ref": input_ref("TARGET-1")},
        "Population": {"id": "SIT-POP-000001", "scope_ref": "SIT-SCP-000001",
                       "unit": "evidence_item", "member_refs": [input_ref("E1"), input_ref("E2")],
                       "selection_rule": "E(I,C)", "coverage_refs": [], "basis_refs": [],
                       "membership_state": "enumerated_for_scope", "qualifications": []},
        "PrerequisiteCheck": {"id": "SIT-CHK-000001", "check_id": "PC02",
                              "scope_ref": "SIT-SCP-000001", "state": "met",
                              "input_refs": [input_ref("E1")], "reason_refs": [],
                              "note": "This finite supplied population is enumerated."},
        "Reason": {"id": "SIT-RSN-000001", "code": "upstream_coverage_incomplete",
                   "scope_ref": "SIT-SCP-000001", "affected_result_refs": ["SIT-RES-000001"],
                   "input_refs": [input_ref("E1")], "detail": "A supplied history remains incomplete.",
                   "classification": "evidence_gap"},
        "Capability": {"id": "SIT-CAP-000001", "diagnostic_id": "SIT-M001",
                       "inquiry_ref": input_ref("I-1", "inquiries"),
                       "scope_refs": ["SIT-SCP-000001"], "check_refs": ["SIT-CHK-000001"],
                       "result_refs": ["SIT-RES-000001"], "available_result_refs": ["SIT-RES-000001"],
                       "unavailable_result_refs": [], "not_applicable_result_refs": [],
                       "not_evaluated_result_refs": [], "reason_refs": [],
                       "scope_note": "One finite requested inventory cell."},
        "ObservabilityDomain": {"level_index": 0, "label": "Artifact and contribution inventory",
                                "available_result_refs": ["SIT-RES-000001"],
                                "unavailable_result_refs": [], "not_evaluated_result_refs": [],
                                "reason_refs": []},
        "Result": result_example(),
        "Fraction": {"numerator": 26, "denominator": 36},
        "PartitionCategory": {"label": "Y", "member_refs": [input_ref("MEMBER-1")], "count": 1},
        "Partition": partition_example(),
        "CompletionInterval": interval_example(),
        "IncidenceMembership": incidence_example()["memberships"][0],
        "OriginIncidenceCount": incidence_example()["origin_counts"][0],
        "Incidence": incidence_example(),
    }
    doc = diagnostic_document()
    examples.update({name: copy.deepcopy(doc[key]) for name, key in (
        ("Run", "run"), ("InputIdentity", "input_identity"),
        ("InputValidation", "input_validation"))})
    examples["Diagnostic"] = copy.deepcopy(doc["run"]["diagnostics"][0])
    examples.update({
        "Predecessor": {"bundle_id": "BUNDLE-1", "snapshot_id": "SNAPSHOT-0"},
        "BasisScope": {"inquiry_refs": [input_ref("I-1", "inquiries")],
                       "claim_refs": [input_ref("C-1")],
                       "effective_window": {"start": time_value(), "end": time_value()}},
        "BasisTime": {"asserted_at": time_value("known", "2024-02-29", "date", None)},
        "Lifecycle": {"state": "withdrawn", "basis_refs": [input_ref("ER-2", "evidence_references")]},
        "BasisEntry": {"id": "SIT-BAS-000001", "source": input_ref("A-1", "assertions"),
                       "basis_kind": "declaration", "asserter_ref": input_ref("ACTOR-1"),
                       "attestor_ref": None, "method": "Recorded assertion supplied by its asserter.",
                       "support_refs": [input_ref("ER-1", "evidence_references")],
                       "availability": None, "scope": {
                           "inquiry_refs": [input_ref("I-1", "inquiries")],
                           "claim_refs": [input_ref("C-1")],
                           "effective_window": {"start": time_value(), "end": time_value()}},
                       "time": {"asserted_at": time_value()},
                       "lifecycle": {"state": "active", "basis_refs": []},
                       "qualifications": ["Attribution does not establish documentary qualification."],
                       "check_refs": ["SIT-CHK-000001"]},
        "SelectedProvenance": provenance_example(),
        "SelectedPipelineRecordData": pipeline_record_example()["data"],
        "SelectedPipelineRecord": pipeline_record_example(),
        "Disclosure": disclosure_example(),
        "RecordDisclosures": {"records": [disclosure_example()]},
        "WitnessCollection": {"witness_refs": ["SIT-FND-000001"]},
        "GraphNode": graph_node(), "GraphEdge": graph_edge(),
        "GraphWitnessComponent": graph_component(),
        "InventoryWitnessComponent": {"type": "inventory_witness", "members": [input_ref("E1")], "member_count": 1},
        "ComparisonWitnessComponent": {"type": "comparison_witness", "members": [input_ref("E1"), input_ref("E2")],
                                       "assessment": input_ref("A-1", "assertions"),
                                       "examined_assessments": [input_ref("A-1", "assertions")], "member_count": 3},
        "SelectedMembersComponent": {"type": "selected_members", "members": [input_ref("E1")], "member_count": 1},
        "HumanReviewWitnessComponent": {"type": "human_review_witness", "members": [input_ref("ACTOR-1")],
                                        "examined_assessments": [], "source_refs": [input_ref("EVAL-1")], "member_count": 2},
        "CorrectionOutcomeWitnessComponent": {"type": "correction_outcome_witness", "members": [input_ref("TARGET-1")],
                                              "source_refs": [input_ref("CHANGE-1")], "member_count": 2},
        "FindingWitness": {"input_refs": [input_ref("E1"), input_ref("O1")], "components": [graph_component()]},
        "Finding": {"id": "SIT-FND-000001", "observation_kind": "positive_witness",
                    "condition_code": "shared_origin_witness", "diagnostic_refs": ["SIT-M004"],
                    "threat_family_refs": ["SIT-TH001"], "scope_ref": "SIT-SCP-000001",
                    "population_refs": ["SIT-POP-000001"], "basis_refs": ["SIT-BAS-000001"],
                    "witness": {"input_refs": [input_ref("E1"), input_ref("O1")], "components": [graph_component()]},
                    "contrary_input_refs": [], "reason_refs": [],
                    "statement": "A supplied claim-scoped path reaches the named origin.",
                    "interpretation_limit": "This finite path does not authenticate the source or outside world."},
    })
    return examples


def validate_component(value, shape):
    port = RecordingPort()
    report_contract._validate_report_component(value, shape, port)
    return port


def assert_component(value, shape):
    schema = report_schema()
    assert schema_accepts(value, schema["$defs"][shape], schema), shape
    port = validate_component(value, shape)
    assert port.units > 0 and port.checks > 0
    return port


def reject_component(value, shape, *, schema_too=True):
    if schema_too:
        schema = report_schema()
        assert not schema_accepts(value, schema["$defs"][shape], schema), shape
    with pytest.raises(TypeError, match="^invalid_report_contract$"):
        validate_component(value, shape)


@pytest.mark.parametrize("shape", tuple(component_examples()))
def test_independent_source_shaped_component_is_accepted(shape):
    assert_component(component_examples()[shape], shape)


@pytest.mark.parametrize("shape,member", [
    (shape, member) for shape, example in component_examples().items()
    for member in example if (shape, member) not in (("TimeWindow", "note"), ("BasisTime", "asserted_at"))
])
@pytest.mark.parametrize("mutation", ("missing", "wrong_type"))
def test_each_component_member_has_a_direct_required_and_type_check(shape, member, mutation):
    baseline = component_examples()[shape]
    assert_component(baseline, shape)
    if mutation == "missing":
        del baseline[member]
    else:
        baseline[member] = {"undeclared_member": "wrong shape"}
    reject_component(baseline, shape)


@pytest.mark.parametrize("shape", tuple(component_examples()))
def test_every_fixed_component_rejects_an_extra_member(shape):
    baseline = component_examples()[shape]
    assert_component(baseline, shape)
    baseline["undeclared_member"] = "No extension slot is specified here."
    reject_component(baseline, shape)


@pytest.mark.parametrize("family,field,kind", FIELD_CASES)
def test_all_fifty_seven_field_bindings_are_exact_without_claiming_execution(family, field, kind):
    assert len(FIELD_CASES) == 57 and len({row[1] for row in FIELD_CASES}) == 57
    baseline = result_example(family, field, kind)
    baseline.update(execution_state="not_performed", result_state="not_evaluated", value=None,
                    reason_refs=["SIT-RSN-000001"])
    assert_component(baseline, "Result")
    wrong_family = copy.deepcopy(baseline)
    wrong_family["diagnostic_id"] = "SIT-M015" if family != "SIT-M015" else "SIT-M001"
    reject_component(wrong_family, "Result")
    wrong_kind = copy.deepcopy(baseline)
    wrong_kind["value_kind"] = "count" if kind != "count" else "fraction"
    reject_component(wrong_kind, "Result")


@pytest.mark.parametrize("state,result_state", RESULT_PAIRS)
def test_all_six_result_state_pairs_keep_value_and_nonresult_distinct(state, result_state):
    baseline = result_example()
    baseline.update(execution_state=state, result_state=result_state)
    if result_state != "available":
        baseline.update(value=None, reason_refs=["SIT-RSN-000001"])
    assert_component(baseline, "Result")
    wrong = copy.deepcopy(baseline)
    wrong["value"] = None if result_state == "available" else 0
    reject_component(wrong, "Result")


@pytest.mark.parametrize("state,result_state", [row for row in itertools.product(
    ("completed", "not_performed", "interrupted", "failed"),
    ("available", "unavailable", "not_applicable", "not_evaluated")) if row not in RESULT_PAIRS])
def test_disallowed_result_state_pairs_are_rejected(state, result_state):
    baseline = result_example()
    assert_component(baseline, "Result")
    baseline.update(execution_state=state, result_state=result_state)
    reject_component(baseline, "Result")


@pytest.mark.parametrize("bad", (True, False, -1, MAX_INTEGER + 1, 1.5, "2"))
def test_count_rejects_boolean_negative_nonportable_and_noninteger_values(bad):
    baseline = result_example()
    assert_component(baseline, "Result")
    baseline["value"] = bad
    reject_component(baseline, "Result")


def test_python_count_rejects_integral_float_despite_json_schema_integer_semantics():
    baseline = result_example()
    assert_component(baseline, "Result")
    baseline["value"] = 2.0
    schema = report_schema()
    assert schema_accepts(baseline, schema["$defs"]["Result"], schema)
    reject_component(baseline, "Result", schema_too=False)


@pytest.mark.parametrize("state", ("unknown", "withheld", "not_applicable"))
def test_nonknown_time_values_require_reason_and_null_value_precision(state):
    baseline = time_value(state)
    assert_component(baseline, "TimeValue")
    for member, bad in (("reason", ""), ("value", "2024-02-29"), ("precision", "date")):
        changed = copy.deepcopy(baseline)
        changed[member] = bad
        reject_component(changed, "TimeValue")
    del baseline["reason"]
    reject_component(baseline, "TimeValue")


@pytest.mark.parametrize("value,precision", (("2024-02-29", "date"),
    ("2026-10-11T19:18:40-07:00", "instant"),
    ("2026-10-12T02:18:40.125Z", "instant")))
def test_known_time_preserves_precision_offset_and_optional_reason(value, precision):
    # Lineage 3.1 permits omission of the reason for a known TimeValue.
    baseline = time_value("known", value, precision, None)
    assert_component(baseline, "TimeValue")
    baseline["reason"] = "Original source time; no timezone conversion."
    assert_component(baseline, "TimeValue")


@pytest.mark.parametrize("value,precision", (("2023-02-29", "date"),
    ("2024-04-31", "date"), ("2026-10-11T19:18:40", "instant"),
    ("2026-10-11T24:00:00Z", "instant"), ("2026-10-11T19:18:60Z", "instant")))
def test_invalid_time_is_not_made_known_by_a_string_shaped_payload(value, precision):
    # Calendar and clock validity are runtime semantic checks, not a claim
    # that this finite schema evaluator implements a date-time format engine.
    with pytest.raises(TypeError, match="^invalid_report_contract$"):
        validate_component(time_value("known", value, precision, None), "TimeValue")


@pytest.mark.parametrize("collection", ("inquiries", "records", "assertions", "evidence_references"))
@pytest.mark.parametrize("identifier", ("R-1", "R.with:parts_1", "SIT-RES-000001"))
def test_input_reference_namespace_is_typed_and_not_inferred_from_id_spelling(collection, identifier):
    assert_component(input_ref(identifier, collection), "InputRef")


@pytest.mark.parametrize("selector", (None, "data.claim_ref", "provenance.evidence_ref_ids",
    "data.role_bindings[role=judge].object_ref",
    "data.role_bindings[role=judge;object_ref=MODEL.v1:main_1].evidence_ref_ids"))
def test_input_reference_preserves_named_field_and_role_selectors(selector):
    assert_component(input_ref("EVAL-1", selector=selector), "InputRef")


@pytest.mark.parametrize("collection", ("results", "findings", "scopes", "unknown"))
def test_input_reference_cannot_use_a_report_collection(collection):
    reject_component(input_ref("R-1", collection), "InputRef")


@pytest.mark.parametrize("shape,wrong_collection", (("InquiryRef", "records"),
    ("RecordRef", "inquiries"), ("AssertionRef", "evidence_references"),
    ("EvidenceRef", "assertions")))
def test_specialized_input_references_keep_their_collection(shape, wrong_collection):
    baseline = component_examples()[shape]
    assert_component(baseline, shape)
    baseline["collection"] = wrong_collection
    reject_component(baseline, shape)


@pytest.mark.parametrize("shape,prefix", (("ScopeId", "SIT-SCP-"),
    ("PopulationId", "SIT-POP-"), ("BasisId", "SIT-BAS-"), ("CapabilityId", "SIT-CAP-"),
    ("CheckId", "SIT-CHK-"), ("ResultId", "SIT-RES-"), ("FindingId", "SIT-FND-"),
    ("ReasonId", "SIT-RSN-")))
def test_report_local_id_prefix_and_minimum_width_are_typed(shape, prefix):
    assert_component(prefix + "000001", shape)
    assert_component(prefix + "1000000", shape)
    for bad in (prefix + "1", prefix + "000000", "INPUT-1", "SIT-RPT-000001"):
        reject_component(bad, shape)


@pytest.mark.parametrize("member,bad", (("numerator", True), ("numerator", -1),
    ("numerator", MAX_INTEGER + 1), ("denominator", False), ("denominator", 0),
    ("denominator", -1), ("denominator", MAX_INTEGER + 1), ("denominator", "36")))
def test_fraction_components_keep_exact_portable_nonnegative_arithmetic(member, bad):
    baseline = {"numerator": 26, "denominator": 36}
    assert_component(baseline, "Fraction")
    baseline[member] = bad
    reject_component(baseline, "Fraction")


def test_fraction_json_contract_omits_decimal_display_without_reducing_original_ratio():
    value = {"numerator": 26, "denominator": 36}
    assert_component(value, "Fraction")
    frozen = report_contract._copy_report_value(value, RecordingPort())
    assert frozen["numerator"] == 26 and frozen["denominator"] == 36
    value["display_decimal"] = "0.722222"
    reject_component(value, "Fraction")


def test_interval_retains_two_exact_endpoints_and_finite_completion_classification():
    value = interval_example()
    assert_component(value, "CompletionInterval")
    for forbidden in ("confidence", "credible", "probability"):
        changed = copy.deepcopy(value)
        changed["interval_kind"] = forbidden
        reject_component(changed, "CompletionInterval")
    for endpoint in ("lower", "upper"):
        changed = copy.deepcopy(value)
        changed[endpoint] = 0.5
        reject_component(changed, "CompletionInterval")


@pytest.mark.parametrize("mutation", ("reversed", "different_denominators", "different_population",
    "missing_unresolved_member", "wrong_lower", "wrong_upper"))
def test_interval_local_payload_relationships_cannot_change_the_finite_completion_meaning(mutation):
    # These are local payload relations, not W03 report-reference resolution.
    value = interval_example()
    assert_component(value, "CompletionInterval")
    if mutation == "reversed":
        value["lower"], value["upper"] = value["upper"], value["lower"]
    elif mutation == "different_denominators":
        value["upper"]["denominator"] = 3
    elif mutation == "different_population":
        value["partition"]["population_ref"] = "SIT-POP-000002"
    elif mutation == "missing_unresolved_member":
        value["partition"]["categories"][1]["member_refs"] = [input_ref("MEMBER-2")]
        value["partition"]["categories"][1]["count"] = 1
        value["partition"]["categories"][2]["member_refs"] = []
        value["partition"]["categories"][2]["count"] = 0
    elif mutation == "wrong_lower":
        value["lower"]["numerator"] = 0
    else:
        value["upper"]["numerator"] = 1
    reject_component(value, "CompletionInterval", schema_too=False)


def test_record_completion_interval_uses_the_four_immediate_layer_dispositions():
    # Definitions 24's exact four labels, without invented display spellings.
    labels = ("direct_origin_link_only", "inherited_only_at_evidence_layer",
              "mixed_direct_and_inherited", "unresolved_at_evidence_layer")
    value = interval_example()
    value["interval_kind"] = "finite_record_completion"
    value["partition"] = {"population_ref": "SIT-POP-000001", "categories": [
        {"label": label, "member_refs": [input_ref("E1")] if i == 1 else
            [input_ref("E2")] if i == 3 else [], "count": 1 if i in (1, 3) else 0}
        for i, label in enumerate(labels)], "total": 2}
    assert_component(value, "CompletionInterval")


@pytest.mark.parametrize("mutation", ("repeated_category", "overlap", "wrong_category_count", "wrong_total"))
def test_partition_payload_is_exclusive_and_its_declared_counts_are_coherent(mutation):
    value = partition_example()
    assert_component(value, "Partition")
    if mutation == "repeated_category":
        value["categories"][1]["label"] = "Y"
    elif mutation == "overlap":
        value["categories"][2]["member_refs"] = [input_ref("MEMBER-1")]
    elif mutation == "wrong_category_count":
        value["categories"][0]["count"] = 2
    else:
        value["total"] = 3
    reject_component(value, "Partition", schema_too=False)


def test_nonexclusive_incidence_preserves_members_and_counts_in_both_directions():
    value = incidence_example()
    assert_component(value, "Incidence")
    assert value["total"] == 2
    assert sum(row["count"] for row in value["origin_counts"]) == 3
    value["nonexclusive"] = False
    reject_component(value, "Incidence")


@pytest.mark.parametrize("mutation", ("duplicate_seed", "duplicate_origin", "wrong_origin_members",
    "wrong_origin_count", "missing_origin_count", "wrong_total"))
def test_incidence_local_payload_cannot_drop_or_invent_an_origin_membership(mutation):
    value = incidence_example()
    assert_component(value, "Incidence")
    if mutation == "duplicate_seed":
        value["memberships"][1]["member_ref"] = input_ref("E1")
    elif mutation == "duplicate_origin":
        value["memberships"][0]["origin_refs"].append(input_ref("O1"))
    elif mutation == "wrong_origin_members":
        value["origin_counts"][1]["member_refs"] = [input_ref("E2")]
    elif mutation == "wrong_origin_count":
        value["origin_counts"][0]["count"] = 1
    elif mutation == "missing_origin_count":
        value["origin_counts"].pop()
    else:
        value["total"] = 3
    reject_component(value, "Incidence", schema_too=False)


@pytest.mark.parametrize("mutation", ("unknown_member", "duplicate_state", "missing_state"))
def test_capability_local_state_lists_are_an_exact_partition(mutation):
    value = component_examples()["Capability"]
    assert_component(value, "Capability")
    if mutation == "unknown_member":
        value["available_result_refs"] = ["SIT-RES-000002"]
    elif mutation == "duplicate_state":
        value["unavailable_result_refs"] = ["SIT-RES-000001"]
    else:
        value["available_result_refs"] = []
    reject_component(value, "Capability", schema_too=False)


def test_domain_does_not_gain_a_fourth_state_column_or_an_overall_score():
    value = component_examples()["ObservabilityDomain"]
    assert_component(value, "ObservabilityDomain")
    for name in ("not_applicable_result_refs", "overall_level", "quality_score"):
        changed = copy.deepcopy(value)
        changed[name] = []
        reject_component(changed, "ObservabilityDomain")


def test_contract_preserves_legitimate_unicode_but_rejects_surrogates():
    value = component_examples()["Reason"]
    value["detail"] = "原始记录: e\u0301 / é / العربية / 🧪"
    assert_component(value, "Reason")
    frozen = report_contract._copy_report_value(value, RecordingPort())
    assert frozen["detail"] == value["detail"]
    value["detail"] = "unpaired \ud800"
    reject_component(value, "Reason", schema_too=False)


def test_component_work_propagates_stops_without_a_second_budget_or_partial_value():
    value = incidence_example()
    for amount in (0, 1, 20):
        with pytest.raises(RuntimeError, match="^controlled_test_stop$"):
            report_contract._validate_report_component(value, "Incidence", RecordingPort(amount))


def test_capture_counts_repeated_aliases_as_occurrences_and_detaches_each_copy():
    # W02 private capture is paid representation work, not input admission.
    row = {"detail": "same supplied text"}
    aliased = {"first": row, "second": row}
    copied = {"first": dict(row), "second": dict(row)}
    aliased_port, copied_port = RecordingPort(), RecordingPort()
    frozen_alias = report_contract._copy_report_value(aliased, aliased_port)
    frozen_copy = report_contract._copy_report_value(copied, copied_port)
    assert aliased_port.units == copied_port.units > 0
    row["detail"] = "changed caller container"
    for member in ("first", "second"):
        assert frozen_alias[member]["detail"] == frozen_copy[member]["detail"] == "same supplied text"


def test_hostile_dict_key_is_rejected_before_hash_comparison_or_representation():
    calls = []

    class Key:
        armed = False

        def __hash__(self):
            if self.armed:
                calls.append("hash")
                raise AssertionError("hostile key was hashed")
            return 0

        def __eq__(self, other):
            calls.append("equality")
            raise AssertionError("hostile key was compared")

        def __repr__(self):
            calls.append("repr")
            raise AssertionError("hostile key was represented")

    key = Key()
    value = {key: "private payload"}
    key.armed = True
    with pytest.raises(TypeError, match="^invalid_report_contract$"):
        report_contract._copy_report_value(value, RecordingPort())
    assert calls == []


def test_immutable_mapping_rejects_hostile_lookup_key_without_its_protocols():
    calls = []

    class Key:
        def __eq__(self, other):
            calls.append("equality")
            raise AssertionError("lookup ran caller equality")

        def __hash__(self):
            calls.append("hash")
            raise AssertionError("lookup ran caller hashing")

        def __repr__(self):
            calls.append("repr")
            raise AssertionError("lookup ran caller repr")

    frozen = report_contract._copy_report_value({"member": "safe"}, RecordingPort())
    with pytest.raises(KeyError):
        frozen[Key()]
    assert calls == []


@pytest.mark.parametrize("mutation", ("empty", "subset", "duplicate", "unknown"))
def test_requested_diagnostics_cannot_create_an_unapproved_public_subset(mutation):
    doc = diagnostic_document()
    assert_both(doc)
    requested = doc["run"]["requested_diagnostic_ids"]
    if mutation == "empty":
        requested.clear()
    elif mutation == "subset":
        requested.pop()
    elif mutation == "duplicate":
        requested[-1] = requested[0]
    else:
        requested[-1] = "SIT-M016"
    assert_rejected(doc)


def test_completed_family_metadata_uses_registered_unique_families():
    value = component_examples()["Run"]
    value["completed_diagnostic_ids"] = ["SIT-M001", "SIT-M004"]
    assert_component(value, "Run")
    for bad in (["SIT-M016"], ["SIT-M001", "SIT-M001"], [True]):
        changed = copy.deepcopy(value)
        changed["completed_diagnostic_ids"] = bad
        reject_component(changed, "Run")


@pytest.mark.parametrize("member", ("release_limits", "qualifications"))
@pytest.mark.parametrize("mutation", ("empty", "missing", "source_override"))
def test_fixed_profile_and_release_statements_cannot_be_overwritten_by_source_text(member, mutation):
    doc = diagnostic_document()
    assert_both(doc)
    target = doc if member == "release_limits" else doc["run"]
    if mutation == "empty":
        target[member] = []
    elif mutation == "missing":
        target[member].pop()
    else:
        target[member][0] = "Source says this is universally true and authenticated."
    assert_rejected(doc)


@pytest.mark.parametrize("which", ("started_at", "finished_at"))
def test_run_clock_metadata_cannot_fabricate_a_wall_clock_measurement(which):
    doc = diagnostic_document()
    assert_both(doc)
    doc["run"][which] = time_value("known", "2026-10-11T19:18:40-07:00", "instant", None)
    assert_rejected(doc)


def test_in_process_identity_cannot_claim_reconstructed_raw_file_bytes():
    value = component_examples()["InputIdentity"]
    assert_component(value, "InputIdentity")
    value["raw_file_digest"] = {"algorithm": "sha256", "value": "0" * 64,
                                "covered_material": "Reconstructed JSON for an in-process object."}
    reject_component(value, "InputIdentity")


@pytest.mark.parametrize("basis_kind", ("declaration", "documented_record", "upstream_inference",
                                        "protected_attestation", "unspecified"))
def test_basis_entry_keeps_original_basis_label_and_explicit_qualification(basis_kind):
    value = component_examples()["BasisEntry"]
    value["basis_kind"] = basis_kind
    if basis_kind == "protected_attestation":
        value["attestor_ref"] = input_ref("ATTESTOR-OPAQUE")
    assert_component(value, "BasisEntry")
    frozen = report_contract._copy_report_value(value, RecordingPort())
    assert frozen["basis_kind"] == basis_kind
    assert frozen["qualifications"] == tuple(value["qualifications"])
    value["basis_kind"] = "independently_verified"
    reject_component(value, "BasisEntry")


@pytest.mark.parametrize("method", (None, "", "A narrowly described supplied method."))
def test_basis_method_preserves_nullable_string_without_new_nonempty_restriction(method):
    # Lineage 3.2 and frozen Provenance use str|null, not text|null.
    for shape in ("BasisEntry", "SelectedProvenance"):
        value = component_examples()[shape]
        value["method"] = method
        assert_component(value, shape)


def test_basis_time_is_an_explicit_optional_field_map_not_arbitrary_metadata():
    assert_component({}, "BasisTime")
    value = {"observed_at": time_value(), "valid_window": {
        "start": time_value("known", "2024-02-29", "date", None), "end": time_value()}}
    assert_component(value, "BasisTime")
    value["source_secret_timestamp"] = "unbounded metadata"
    reject_component(value, "BasisTime")


@pytest.mark.parametrize("state", ("occurred", "did_not_occur", "unknown"))
def test_native_pipeline_states_survive_disclosure_as_source_data(state):
    value = disclosure_example()
    value["fields"]["native_record"] = pipeline_record_example(state)
    assert_component(value, "Disclosure")
    result = result_example("SIT-M010", "pipeline_stage_disclosures", "record_disclosures")
    result.update(result_origin="attributed_record", value={"records": [value]})
    assert_component(result, "Result")
    assert result["execution_state"] == "completed" and result["result_state"] == "available"
    frozen = report_contract._copy_report_value(result, RecordingPort())
    assert frozen["value"]["records"][0]["fields"]["native_record"]["data"]["state"] == state


@pytest.mark.parametrize("outcome", ("accepted", "rejected", "failed", "unknown"))
def test_native_handling_outcome_is_a_closed_attributed_value_not_a_run_state(outcome):
    value = {"outcome": outcome, "reason": "The source records this handling disposition."}
    assert_component(value, "SelectedHandlingDetails")
    value["outcome"] = "toolkit_certified_correction"
    reject_component(value, "SelectedHandlingDetails")


@pytest.mark.parametrize("outcome", ("verified", "not_verified", "inconclusive", "revoked", "unknown"))
def test_native_verification_outcome_keeps_its_scope_and_does_not_become_a_badge(outcome):
    value = {"verification_scope": "process", "evaluation_ref": "EVAL-1", "reported_outcome": outcome,
             "valid_window": {"start": time_value(), "end": time_value()},
             "scope_note": "Only the supplied process assessment is represented."}
    assert_component(value, "SelectedVerificationDetails")
    value["truth_badge"] = True
    reject_component(value, "SelectedVerificationDetails")


@pytest.mark.parametrize("member", ("excerpt", "contact", "display_name", "identity_key", "extensions", "path"))
def test_selected_native_shape_has_no_implicit_whole_record_or_secret_export_slot(member):
    # Structural whitelist only; actual field selection remains P4-W04 work.
    value = pipeline_record_example()
    assert_component(value, "SelectedPipelineRecord")
    value[member] = "PRIVATE_CANARY_NOT_AN_APPROVED_FIELD"
    reject_component(value, "SelectedPipelineRecord")


def test_record_disclosure_payload_cannot_hide_an_unregistered_scalar_metric():
    value = disclosure_example()
    assert_component(value, "Disclosure")
    value["fields"]["integrity_score"] = 100
    reject_component(value, "Disclosure")


def test_record_disclosure_family_rejects_a_valid_payload_from_another_owner():
    value = result_example("SIT-M010", "pipeline_stage_disclosures", "record_disclosures")
    value.update(result_origin="attributed_record", value={"records": [disclosure_example()]})
    assert_component(value, "Result")
    value["diagnostic_id"] = "SIT-M013"
    value["field_key"] = "human_contribution_disclosures"
    reject_component(value, "Result")


def test_witness_collection_references_findings_and_has_no_inline_private_witness():
    value = component_examples()["WitnessCollection"]
    assert_component(value, "WitnessCollection")
    for wrong in (["SIT-RES-000001"], ["SIT-SCP-000001"], [{"kind": "path", "anchor": []}]):
        reject_component({"witness_refs": wrong}, "WitnessCollection")


@pytest.mark.parametrize("shape", ("GraphWitnessComponent", "InventoryWitnessComponent",
    "ComparisonWitnessComponent", "SelectedMembersComponent", "HumanReviewWitnessComponent",
    "CorrectionOutcomeWitnessComponent"))
def test_all_six_typed_witness_components_are_admitted_without_running_their_search(shape):
    value = component_examples()[shape]
    assert_component(value, shape)
    assert_component(value, "WitnessComponent")
    value["type"] = "external_full_world_proof"
    reject_component(value, "WitnessComponent")


@pytest.mark.parametrize("family,field,kind,value", (
    ("SIT-M001", "seed_evidence_item_count", "count", 2),
    ("SIT-M005", "single_origin_contribution_hhi", "fraction", {"numerator": 26, "denominator": 36}),
    ("SIT-M010", "stage_occurrence_completion_interval", "completion_interval", interval_example()),
    ("SIT-M010", "stage_member_partition", "partition", partition_example()),
    ("SIT-M004", "per_seed_origin_memberships", "incidence", incidence_example()),
    ("SIT-M010", "pipeline_stage_disclosures", "record_disclosures", {"records": [disclosure_example()]}),
    ("SIT-M008", "evaluator_overlap_witnesses", "witness_collection", {"witness_refs": ["SIT-FND-000001"]}),
))
def test_all_seven_available_value_kinds_have_their_own_complete_payload(family, field, kind, value):
    baseline = result_example(family, field, kind)
    baseline["value"] = copy.deepcopy(value)
    if kind == "witness_collection":
        baseline["witness_refs"] = ["SIT-FND-000001"]
    if kind == "record_disclosures":
        baseline["result_origin"] = "attributed_record"
    assert_component(baseline, "Result")
    for wrong in (None, True, {"arbitrary_json": "not this value's closed payload"}):
        changed = copy.deepcopy(baseline)
        changed["value"] = wrong
        reject_component(changed, "Result")


@pytest.mark.parametrize("member,shape", (("scopes", "Scope"), ("populations", "Population"),
    ("basis_index", "BasisEntry"), ("capabilities", "Capability"),
    ("checks", "PrerequisiteCheck"), ("observability_domains", "ObservabilityDomain"),
    ("results", "Result"), ("findings", "Finding")))
def test_diagnostic_envelope_cannot_smuggle_valid_analytical_components(member, shape):
    doc = diagnostic_document()
    assert_both(doc)
    component = component_examples()[shape]
    assert_component(component, shape)
    doc[member] = [component]
    assert_rejected(doc)


def test_diagnostic_reason_can_preserve_a_safe_execution_limit_without_an_analytical_scope():
    doc = diagnostic_document()
    doc["reasons"] = [{"id": "SIT-RSN-000001", "code": "execution_failed", "scope_ref": None,
                       "affected_result_refs": [], "input_refs": [],
                       "detail": "Processing did not complete.", "classification": "execution"}]
    # Reporting 16.1 empties the eight analytical arrays, not all reasons.
    assert_both(doc)


def test_every_abort_transport_argument_checks_exact_type_before_value_protocols():
    calls = []

    class Hostile:
        def attack(self, *args, **kwargs):
            calls.append("protocol")
            raise AssertionError("transport executed a caller protocol")
        __eq__ = __hash__ = __iter__ = __repr__ = __str__ = __bool__ = attack

    for index in range(4):
        args = ["failed", "accepted", "execution_failed", "not_published"]
        args[index] = Hostile()
        with pytest.raises(TypeError):
            execution.AuditAbort(*args)
    for index in range(2):
        args = ["accepted", "not_published"]
        args[index] = Hostile()
        with pytest.raises(TypeError):
            execution.AuditCancelled(*args)
    assert calls == []


def test_nested_selected_source_cannot_trigger_a_conversion_or_copy_hook():
    calls = []

    class Hostile:
        def attack(self, *args, **kwargs):
            calls.append("protocol")
            raise AssertionError("report capture executed a caller protocol")
        __iter__ = __repr__ = __str__ = __float__ = __int__ = __index__ = attack
        __copy__ = __deepcopy__ = __reduce__ = __reduce_ex__ = attack

    value = disclosure_example()
    value["fields"]["native_record"]["data"]["detail"] = Hostile()
    with pytest.raises(TypeError, match="^invalid_report_contract$"):
        validate_component(value, "Disclosure")
    assert calls == []


def test_complete_trace_witness_kind_preserves_the_existing_private_trace_shape():
    # origins._complete_witness retains starts, examined nodes/edges and
    # terminals. These occurrences all contribute to the finite member count.
    value = graph_component()
    value.update(kind="complete_trace", nodes=[], edges=[], starts=[graph_node()],
                 examined_nodes=[graph_node(), graph_node("O1", "origin_event")],
                 examined_edges=[graph_edge()], terminals=[graph_node("O1", "origin_event")],
                 member_count=5)
    assert_component(value, "GraphWitnessComponent")


def test_basis_time_retains_inquiry_cutoff_and_window_without_replacing_them_with_run_time():
    value = {"as_of": time_value("known", "2026-10-11", "date", None),
             "time_window": {"start": time_value("known", "2026-10-01", "date", None),
                             "end": time_value("known", "2026-10-11", "date", None)}}
    assert_component(value, "BasisTime")


def test_input_identifiers_respect_the_existing_128_ascii_byte_boundary():
    value = input_ref("R" * 128)
    assert_component(value, "InputRef")
    value["identifier"] += "R"
    reject_component(value, "InputRef")


def test_comparison_witness_can_retain_a_missing_assessment_without_inventing_independence():
    value = component_examples()["ComparisonWitnessComponent"]
    value.update(assessment=None, examined_assessments=[], member_count=2)
    assert_component(value, "ComparisonWitnessComponent")


@pytest.mark.parametrize("shape", ("GraphWitnessComponent", "InventoryWitnessComponent",
    "ComparisonWitnessComponent", "SelectedMembersComponent", "HumanReviewWitnessComponent",
    "CorrectionOutcomeWitnessComponent"))
def test_witness_member_count_accounts_for_every_retained_local_occurrence(shape):
    value = component_examples()[shape]
    assert_component(value, shape)
    value["member_count"] += 1
    reject_component(value, shape, schema_too=False)


@pytest.mark.parametrize("shape", ("HumanReviewWitnessComponent", "CorrectionOutcomeWitnessComponent"))
def test_witness_source_slots_preserve_repeated_occurrences_and_charge_each(shape):
    # The private review/outcome owners count source_refs occurrences. A
    # repeated role/source slot is not a second independently acquired source.
    value = component_examples()[shape]
    value["source_refs"].append(copy.deepcopy(value["source_refs"][0]))
    value["member_count"] += 1
    assert_component(value, shape)


@pytest.mark.parametrize("mutation", ("mismatch", "omitted", "extra"))
def test_witness_collection_payload_matches_its_own_result_witness_references(mutation):
    # Reporting 16.4/16.5 and the accepted private _Result require one local
    # witness set. Resolving the Finding IDs themselves is separate W03 work.
    value = result_example("SIT-M008", "evaluator_overlap_witnesses", "witness_collection")
    value.update(value={"witness_refs": ["SIT-FND-000001"]}, witness_refs=["SIT-FND-000001"])
    assert_component(value, "Result")
    if mutation == "mismatch":
        value["witness_refs"] = ["SIT-FND-000002"]
    elif mutation == "omitted":
        value["witness_refs"] = []
    else:
        value["witness_refs"].append("SIT-FND-000002")
    reject_component(value, "Result", schema_too=False)


@pytest.mark.parametrize("collection", ("records", "assertions"))
def test_case_target_keeps_legal_assertion_and_record_before_states(collection):
    # Lineage 6.8/6.9 allow Assertion targets; private _CaseTarget preserves
    # that collection instead of coercing an assertion into a record ref.
    value = {"case_ref": input_ref("CASE-1"), "before_ref": input_ref("BEFORE-1", collection)}
    assert_component(value, "CaseTarget")
    population = component_examples()["Population"]
    population.update(unit="case_target", member_refs=[value])
    assert_component(population, "Population")


@pytest.mark.parametrize("collection", ("inquiries", "evidence_references"))
def test_case_target_does_not_expand_before_state_into_an_unapproved_collection(collection):
    value = {"case_ref": input_ref("CASE-1"), "before_ref": input_ref("BEFORE-1", collection)}
    reject_component(value, "CaseTarget")


@pytest.mark.parametrize("collection,kind", [
    ("records", kind) for kind in ("claim", "artifact", "actor", "evidence_item", "origin_event",
        "model", "evaluation", "correction_channel", "correction_event", "pipeline_record",
        "anomaly", "unresolved_reference")
] + [("inquiries", "inquiry"), ("assertions", "assertion"),
     ("evidence_references", "evidence_reference")])
def test_graph_node_uses_the_existing_whole_entity_collection_and_kind(collection, kind):
    # Frozen validation.references._index and graph.projections._graph_node
    # bind the node to one complete typed entity, without a field selector.
    value = {"ref": input_ref("NODE-1", collection), "kind": kind}
    assert_component(value, "GraphNode")
    for other in ("inquiries", "records", "assertions", "evidence_references"):
        if other != collection:
            changed = copy.deepcopy(value)
            changed["ref"]["collection"] = other
            reject_component(changed, "GraphNode")
    value["ref"]["selector"] = "data.role_bindings[role=judge].object_ref"
    reject_component(value, "GraphNode")


@pytest.mark.parametrize("mutation", ("record_owner", "inquiry_owner", "evidence_reference_owner", "field_selector"))
def test_relation_edge_keeps_its_whole_assertion_identity(mutation):
    value = graph_edge()
    assert_component(value, "GraphEdge")
    if mutation == "field_selector":
        value["source_ref"]["selector"] = "data.from_ref"
    else:
        value["source_ref"]["collection"] = {
            "record_owner": "records", "inquiry_owner": "inquiries",
            "evidence_reference_owner": "evidence_references"}[mutation]
    reject_component(value, "GraphEdge")


def canonical_edge_example():
    # Evaluation role links are canonical record links without an invented
    # RelationAssertion. The selected role remains part of their identity.
    return {"source": graph_node("EVAL-1", "evaluation"),
            "target": graph_node("MODEL-1", "model"),
            "source_ref": input_ref("EVAL-1", selector="data.role_bindings[role=judge].object_ref"),
            "predicate": None, "eligible": True, "reason_codes": []}


@pytest.mark.parametrize("mutation", ("missing_selector", "empty_selector", "wrong_owner_id", "wrong_owner_collection"))
def test_canonical_record_edge_retains_its_source_entity_and_named_role(mutation):
    value = canonical_edge_example()
    assert_component(value, "GraphEdge")
    if mutation == "missing_selector":
        value["source_ref"]["selector"] = None
    elif mutation == "empty_selector":
        value["source_ref"]["selector"] = ""
    elif mutation == "wrong_owner_id":
        value["source_ref"]["identifier"] = "EVAL-2"
    else:
        value["source_ref"]["collection"] = "assertions"
    reject_component(value, "GraphEdge", schema_too=mutation in ("missing_selector", "empty_selector"))


@pytest.mark.parametrize("shape,member", (("Scope", "inquiry_ref"),
    ("Scope", "claim_refs"), ("Capability", "inquiry_ref")))
def test_scope_and_capability_owners_are_whole_inquiry_or_claim_entities(shape, member):
    # Accepted _Scope explicitly uses selector-free Inquiry/Claim references;
    # _Capability stores the whole Inquiry ID. General InputRefs retain their
    # field selectors in other slots such as basis and canonical edge links.
    value = component_examples()[shape]
    assert_component(value, shape)
    if member == "claim_refs":
        value[member][0]["selector"] = "data.claim_key"
    else:
        value[member]["selector"] = "boundary.system_refs"
    reject_component(value, shape)


# W02 exhaustive nested/selected-object contract specimens and member controls.

"""Independent literal candidates for N01; not a production projection.

Sources: CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md sections 3--6.12 and the
previously admitted tests/fixtures/hero/H7-01.bundle.json. Source field names
and enum members are transcribed here; public selection is explicitly written.
No product constants, report schema, renderer or W04 disclosure code is used.
The host N01 module supplies time_value() and provenance_example().
"""


def native_record_examples():
    """Return independently authored selected-native and nested positives."""
    source = "CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md"
    gap = {
        "field": "data.version_label", "reason": "not_recorded",
        "detail": "The supplied source does not record a version label.",
    }
    window = {
        "start": time_value("known", "2026-01-01", "date"),
        "end": time_value("known", "2026-01-31", "date"),
    }
    boundary = {
        "description": "The represented answer and review workflow.",
        "criterion": "An independently acquired observation lies outside this workflow.",
        "system_refs": ["ART-1", "MODEL-1", "ACTOR-1", "EVAL-1"],
    }
    role = {
        "role": "human_reviewer", "object_ref": "ACTOR-1",
        "evidence_ref_ids": ["REF-1"],
        "qualifications": ["The role is supplied metadata, not an independent vote."],
    }
    inquiry = {
        "id": "INQ-1", "target_claim_refs": ["CLAIM-1"],
        "target_object_refs": ["ART-1", "MODEL-1", "EVAL-1"],
        "seed_artifact_refs": ["ART-1"], "seed_evidence_refs": ["EVID-1"],
        "boundary": boundary, "time_window": window,
        "as_of": time_value("known", "2026-01-31", "date"),
        "dependency_dimensions": ["acquisition", "analytical_method"],
        "coverage_assertion_refs": ["ASS-COVERAGE-1"],
        "provenance": provenance_example(),
    }
    evidence = {
        "id": "REF-1", "reference_kind": "supplied_excerpt",
        "availability": "supplied", "artifact_ref": "ART-1",
        "record_ref": None, "provided_by_ref": "ACTOR-1",
        "attestor_ref": None,
        "scope_note": "The supplied source excerpt supports this process description.",
    }
    submission = {
        "submission_kind": "proposed_correction",
        "summary": "The submitter proposes replacing the recorded review assignment.",
    }
    handling = {
        "outcome": "accepted", "reason": "The supplied handling record accepts the request.",
    }
    change = {
        "action_type": "replace_evaluator", "before_ref": "EVAL-1",
        "after_ref": "EVAL-2", "after_absence_reason": None,
        "linkage_description": "The supplied change links the old and new evaluation records.",
    }
    # Each payload is typed directly from the corresponding frozen source table.
    # Suppressed fields are intentionally absent from these literal public bags.
    data = {
        "claim": {
            "claim_key": "CLAIM-FAMILY-1", "version_label": "v1",
            "context": "The statement concerns the declared inquiry and January window.",
        },
        "artifact": {
            "artifact_kind": "document", "version_label": "v1",
            "published_at": time_value("known", "2026-01-02", "date"),
            "retrieved_at": time_value("known", "2026-01-03", "date"),
            "content_evidence_refs": ["REF-1"],
        },
        "actor": {"actor_kind": "human", "identity_disclosure": "pseudonymous"},
        "evidence_item": {
            "claim_ref": "CLAIM-1", "artifact_ref": "ART-1",
            "epistemic_type": "documentary_statement",
            "description": "The source contributes a scoped documentary statement.",
        },
        "origin_event": {
            "event_kind": "observation", "event_key": "OBSERVATION-1",
            "performed_by_refs": ["ACTOR-1"], "method_ref": "ART-METHOD-1",
            "occurred_at": time_value("known", "2026-01-02", "date"),
            "description": "A supplied observation event with an attributed method.",
        },
        "model": {
            "model_key": "MODEL-FAMILY-1", "version_label": "v1",
            "family_label": "Declared family", "provider_ref": "ACTOR-ORG-1",
        },
        "evaluation": {
            "evaluation_kind": "human_review", "target_refs": ["CLAIM-1", "ART-1"],
            "role_bindings": [role], "result_refs": ["ART-RESULT-1"],
            "occurred_at": time_value("known", "2026-01-05", "date"),
            "review_contribution": "The reviewer supplied an external comparison record.",
        },
        "correction_channel": {
            "owner_refs": ["ACTOR-1"], "target_refs": ["CLAIM-1", "EVAL-1"],
            "declared_action_types": ["review", "replace_evaluator"],
            "valid_window": window,
        },
        "correction_event_submission": {
            "event_kind": "submission", "case_ref": None, "channel_ref": "CHANNEL-1",
            "target_refs": ["EVAL-1"],
            "occurred_at": time_value("known", "2026-01-06", "date"),
            "details": submission,
        },
        "correction_event_handling": {
            "event_kind": "handling", "case_ref": "CASE-1", "channel_ref": "CHANNEL-1",
            "target_refs": ["EVAL-1"],
            "occurred_at": time_value("known", "2026-01-07", "date"),
            "details": handling,
        },
        "correction_event_change": {
            "event_kind": "change", "case_ref": "CASE-1", "channel_ref": "CHANNEL-1",
            "target_refs": ["EVAL-1"],
            "occurred_at": time_value("known", "2026-01-08", "date"),
            "details": change,
        },
        "pipeline_record": {
            "subject_ref": "EVID-1", "run_key": "RUN-1", "stage_key": "STEP-1",
            "stage": "preservation", "state": "occurred", "output_refs": ["ART-OUTPUT-1"],
            "observed_at": time_value("known", "2026-01-09", "date"),
            "linkage_kind": "use_record",
            "detail": "The source records preservation of this contribution in the output.",
        },
        "anomaly": {
            "inquiry_refs": ["INQ-1"], "claim_ref": None,
            "original_context": "An observation does not fit the current claim classification.",
            "context_evidence_ref": None, "classification_state": "unclassified",
            "caller_label": None,
            "comparison_note": "The caller supplied a comparison; no rarity estimate is inferred.",
        },
        "unresolved_reference": {
            "expected_kinds": ["origin_event", "evidence_item"],
            "reason": "outside_snapshot",
            "description": "The referenced upstream process lies outside the supplied snapshot.",
        },
    }
    # IDs, kinds and shape bindings are handwritten and independent of product
    # RECORD_SHAPES; they provide the positive baseline for wrong-binding tests.
    bindings = (
        ("claim", "CLAIM-1", "claim", "SelectedClaimData", "6.1"),
        ("artifact", "ART-1", "artifact", "SelectedArtifactData", "6.2"),
        ("actor", "ACTOR-1", "actor", "SelectedActorData", "6.3"),
        ("evidence_item", "EVID-1", "evidence_item", "SelectedEvidenceItemData", "6.4"),
        ("origin_event", "ORIGIN-1", "origin_event", "SelectedOriginEventData", "6.5"),
        ("model", "MODEL-1", "model", "SelectedModelData", "6.6"),
        ("evaluation", "EVAL-1", "evaluation", "SelectedEvaluationData", "6.7"),
        ("correction_channel", "CHANNEL-1", "correction_channel", "SelectedCorrectionChannelData", "6.8"),
        ("correction_event_submission", "CASE-1", "correction_event", "SelectedCorrectionEventData", "6.9"),
        ("correction_event_handling", "HANDLING-1", "correction_event", "SelectedCorrectionEventData", "6.9"),
        ("correction_event_change", "CHANGE-1", "correction_event", "SelectedCorrectionEventData", "6.9"),
        ("pipeline_record", "PIPE-1", "pipeline_record", "SelectedPipelineRecordData", "6.10"),
        ("anomaly", "ANOMALY-1", "anomaly", "SelectedAnomalyData", "6.11"),
        ("unresolved_reference", "UNRESOLVED-1", "unresolved_reference", "SelectedUnresolvedReferenceData", "6.12"),
    )
    examples = {
        "gap": {"shape": "SelectedGap", "value": gap, "source": source + " §3.3"},
        "boundary": {"shape": "SelectedBoundary", "value": boundary, "source": source + " §5"},
        "role_binding": {"shape": "SelectedRoleBinding", "value": role, "source": source + " §6.7"},
        "inquiry": {"shape": "SelectedInquiry", "value": inquiry, "source": source + " §5"},
        "native_inquiry": {"shape": "SelectedNative", "value": inquiry, "source": source + " §5"},
        "evidence_reference": {"shape": "SelectedEvidenceReference", "value": evidence, "source": source + " §4"},
        "native_evidence_reference": {"shape": "SelectedNative", "value": evidence, "source": source + " §4"},
        "submission_details": {"shape": "SelectedSubmissionDetails", "value": submission, "source": source + " §6.9"},
        "handling_details": {"shape": "SelectedHandlingDetails", "value": handling, "source": source + " §6.9"},
        "change_details": {"shape": "SelectedChangeDetails", "value": change, "source": source + " §6.9"},
    }
    for label, identifier, kind, shape, section in bindings:
        origin = source + " §" + section
        envelope = {"id": identifier, "kind": kind, "data": data[label],
                    "provenance": provenance_example()}
        examples["data_" + label] = {"shape": shape, "value": data[label], "source": origin}
        examples["record_" + label] = {"shape": "SelectedRecord", "value": envelope, "source": origin}
        examples["native_" + label] = {"shape": "SelectedNative", "value": envelope, "source": origin}
    # Presence/absence are intentional source distinctions. No automatic labels,
    # identifiers, locator fields or arbitrary extension fields are introduced.
    examples.update({
        "inquiry_gaps_present": {
            "shape": "SelectedInquiry",
            "value": {**inquiry, "gaps": [{"field": "coverage_assertion_refs",
                       "reason": "not_examined", "detail": "Some dimensions were not examined."}]},
            "source": source + " §§3.3,5",
        },
        "inquiry_gaps_empty": {
            "shape": "SelectedInquiry", "value": {**inquiry, "gaps": []},
            "source": source + " §§3.3,5",
        },
        "inquiry_window_note_present": {
            "shape": "SelectedInquiry",
            "value": {**inquiry, "time_window": {**window, "note": "January source window."}},
            "source": source + " §§3.1,5",
        },
        "claim_content_ref_present": {
            "shape": "SelectedClaimData", "value": {**data["claim"], "content_evidence_ref": "REF-1"},
            "source": source + " §6.1",
        },
        "claim_unknown_version_with_gap": {
            "shape": "SelectedRecord",
            "value": {"id": "CLAIM-UNKNOWN", "kind": "claim",
                      "data": {**data["claim"], "version_label": None},
                      "provenance": provenance_example(), "gaps": [gap]},
            "source": source + " §§3.3,6.1",
        },
        "record_gaps_empty": {
            "shape": "SelectedRecord", "value": {**examples["record_actor"]["value"], "gaps": []},
            "source": source + " §§3.3,6",
        },
        "change_explicit_removal": {
            "shape": "SelectedChangeDetails",
            "value": {"action_type": "retract", "before_ref": "EVAL-1", "after_ref": None,
                      "after_absence_reason": "The source explicitly records removal of this evaluation.",
                      "linkage_description": "The supplied removal event names the before-state."},
            "source": source + " §6.9",
        },
        "anomaly_caller_classified": {
            "shape": "SelectedAnomalyData",
            "value": {**data["anomaly"], "classification_state": "caller_classified",
                      "caller_label": "Caller supplied class"},
            "source": source + " §6.11",
        },
        "anomaly_protected_context_with_gap": {
            "shape": "SelectedRecord",
            "value": {"id": "ANOMALY-PROTECTED", "kind": "anomaly",
                      "data": {**data["anomaly"], "original_context": None,
                               "context_evidence_ref": "REF-ATTESTATION"},
                      "provenance": provenance_example(),
                      "gaps": [{"field": "data.original_context", "reason": "withheld",
                                "detail": "The original context survives through the protected reference."}]},
            "source": source + " §§3.3,6.11",
        },
        "evidence_record_pointer": {
            "shape": "SelectedEvidenceReference",
            "value": {**evidence, "reference_kind": "record_pointer", "record_ref": "EVAL-1"},
            "source": source + " §4.2",
        },
        "evidence_local_locator": {
            "shape": "SelectedEvidenceReference",
            "value": {**evidence, "reference_kind": "local_locator", "availability": "locator_only"},
            "source": source + " §4.2 (inert source locator is not a selected member)",
        },
        "evidence_external_locator": {
            "shape": "SelectedEvidenceReference",
            "value": {**evidence, "reference_kind": "external_locator", "availability": "locator_only"},
            "source": source + " §4.2 (inert source locator is not a selected member)",
        },
        "evidence_protected_attestation": {
            "shape": "SelectedEvidenceReference",
            "value": {**evidence, "reference_kind": "protected_attestation", "attestor_ref": "ACTOR-1",
                      "scope_note": "A supplied attestation supports only its stated process scope."},
            "source": source + " §4.2",
        },
        "evidence_protected_unavailable": {
            "shape": "SelectedEvidenceReference",
            "value": {**evidence, "reference_kind": "protected_attestation", "availability": "unavailable",
                      "attestor_ref": "ACTOR-1",
                      "gaps": [{"field": "excerpt", "reason": "unavailable",
                                "detail": "The unavailable attestation is not inspectable support."}]},
            "source": source + " §§3.3,4.2",
        },
        "evidence_protected_withheld": {
            "shape": "SelectedEvidenceReference",
            "value": {**evidence, "reference_kind": "protected_attestation", "availability": "withheld",
                      "attestor_ref": "ACTOR-1",
                      "gaps": [{"field": "excerpt", "reason": "withheld",
                                "detail": "The attestation content is withheld from this snapshot."}]},
            "source": source + " §§3.3,4.2",
        },
        "evidence_gaps_empty": {
            "shape": "SelectedEvidenceReference", "value": {**evidence, "gaps": []},
            "source": source + " §§3.3,4.1",
        },
        "selected_pipeline_record": {
            "shape": "SelectedPipelineRecord", "value": examples["record_pipeline_record"]["value"],
            "source": source + " §6.10",
        },
        "selected_unresolved_record": {
            "shape": "SelectedUnresolvedRecord", "value": examples["record_unresolved_reference"]["value"],
            "source": source + " §6.12",
        },
    })
    # Explicit top-level optional-member inventory for deletion tests. The
    # lists are source-authored, never read from schema.required/properties.
    optional_by_shape = {
        "SelectedInquiry": ("gaps",), "SelectedRecord": ("gaps",),
        "SelectedNative": ("gaps",), "SelectedEvidenceReference": ("gaps",),
        "SelectedClaimData": ("content_evidence_ref",),
        "SelectedPipelineRecord": ("gaps",), "SelectedUnresolvedRecord": ("gaps",),
    }
    for example in examples.values():
        example["optional"] = optional_by_shape.get(example["shape"], ())
    return examples


def selected_record(kind, event_kind=None):
    """Convenience source-shaped fixture for the owner's disclosure examples.

    Each call rebuilds literals. The caller can mutate its result independently.
    CorrectionEvent callers explicitly select submission, handling or change.
    """
    if kind == "correction_event":
        if event_kind not in ("submission", "handling", "change"):
            raise ValueError("Specify one frozen CorrectionEvent subtype")
        label = "record_correction_event_" + event_kind
    else:
        if event_kind is not None:
            raise ValueError("event_kind only selects a CorrectionEvent subtype")
        label = "record_" + kind
    return native_record_examples()[label]["value"]


def native_record_binding_cases():
    """(baseline label, discriminator path, invalid value, source section).

    Deep-copy the baseline, assert it accepts, then change just the given leaf.
    Other source/data branches remain valid by themselves. These mismatches test
    kind/data binding, not reference resolution, source loading or projection.
    """
    return (
        ("record_claim", ("kind",), "artifact", "6.1--6.2"),
        ("record_artifact", ("kind",), "actor", "6.2--6.3"),
        ("record_actor", ("kind",), "evidence_item", "6.3--6.4"),
        ("record_evidence_item", ("kind",), "origin_event", "6.4--6.5"),
        ("record_origin_event", ("kind",), "model", "6.5--6.6"),
        ("record_model", ("kind",), "evaluation", "6.6--6.7"),
        ("record_evaluation", ("kind",), "correction_channel", "6.7--6.8"),
        ("record_correction_channel", ("kind",), "correction_event", "6.8--6.9"),
        ("record_correction_event_submission", ("kind",), "pipeline_record", "6.9--6.10"),
        ("record_pipeline_record", ("kind",), "anomaly", "6.10--6.11"),
        ("record_anomaly", ("kind",), "unresolved_reference", "6.11--6.12"),
        ("record_unresolved_reference", ("kind",), "claim", "6.12,6.1"),
        ("data_correction_event_submission", ("event_kind",), "handling", "6.9"),
        ("data_correction_event_handling", ("event_kind",), "change", "6.9"),
        ("data_correction_event_change", ("event_kind",), "handling", "6.9"),
    )


def native_record_enum_cases():
    """Literal accepted enum candidates: (baseline, path, values, source).

    Replace the selected leaf with each listed value on a fresh deep copy.
    Dependent cases (correction kind, anomaly classification, reference kind /
    availability) have complete positive examples above rather than unsafe
    one-leaf enum substitutions. Role object IDs can require a matching source
    object in W03; these N01 components check only their selected local shape.
    """
    return (
        ("gap", ("reason",), ("not_recorded", "not_examined", "withheld", "unavailable",
          "identity_ambiguous", "outside_snapshot", "not_applicable", "other"), "3.3"),
        ("inquiry", ("dependency_dimensions", 0), ("acquisition", "analytical_method",
          "model_ancestry", "evaluation_rubric", "organizational_control"), "5, definitions §9"),
        ("data_artifact", ("artifact_kind",), ("document", "dataset", "answer", "reference_answer",
          "rubric", "benchmark", "judgment", "observation_record", "execution_result", "other", "unknown"), "6.2"),
        ("data_actor", ("actor_kind",), ("human", "organization", "software_agent", "unknown"), "6.3"),
        ("data_actor", ("identity_disclosure",), ("named", "pseudonymous", "protected", "unknown"), "6.3"),
        ("data_evidence_item", ("epistemic_type",), ("measurement", "testimony", "documentary_statement",
          "estimate", "formal_derivation", "execution_result", "analytical_inference", "evaluative_judgment",
          "allegation", "fictional_example", "unclassified"), "6.4"),
        ("data_origin_event", ("event_kind",), ("observation", "data_collection", "testimony",
          "documentary_issuance", "analysis", "formal_check", "execution", "other", "unknown"), "6.5"),
        ("data_evaluation", ("evaluation_kind",), ("judgment", "formal_check", "execution", "empirical_review",
          "human_review", "identity_process_review", "other", "unknown"), "6.7"),
        ("role_binding", ("role",), ("candidate", "generator", "judge", "executor", "human_reviewer",
          "reference_answer", "rubric", "validation_environment", "method_input"), "6.7"),
        ("data_correction_channel", ("declared_action_types", 0), ("review", "amend", "annotate",
          "retract", "rerun", "rollback", "replace_evaluator", "restrict_scope", "withdraw",
          "metadata_correction", "other"), "6.8"),
        ("submission_details", ("submission_kind",), ("objection", "proposed_correction", "appeal"), "6.9"),
        ("handling_details", ("outcome",), ("acknowledged", "under_review", "accepted", "rejected",
          "withdrawn", "failed", "unknown"), "6.9"),
        ("change_details", ("action_type",), ("review", "amend", "annotate", "retract", "rerun", "rollback",
          "replace_evaluator", "restrict_scope", "withdraw", "metadata_correction", "other"), "6.8--6.9"),
        ("data_pipeline_record", ("stage",), ("admission", "preservation", "selection", "influence"), "6.10"),
        ("data_pipeline_record", ("state",), ("occurred", "did_not_occur", "unknown"), "6.10"),
        ("data_pipeline_record", ("linkage_kind",), ("use_record", "comparison_record", "experimental_attribution",
          "declaration", "unspecified"), "6.10"),
        ("data_unresolved_reference", ("expected_kinds", 0), ("claim", "artifact", "actor", "evidence_item",
          "origin_event", "model", "evaluation", "correction_channel", "correction_event",
          "pipeline_record", "anomaly"), "6.12"),
        ("data_unresolved_reference", ("reason",), ("not_recorded", "not_examined", "withheld", "unavailable",
          "identity_ambiguous", "outside_snapshot", "other"), "6.12"),
    )


"""Independent source-shaped selected assertion witnesses for N01 integration.

Handwritten from CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md sections 7--9 and
tests/contract/test_typed_records.py's already admitted fictional source pool.
Public fields are an explicit selection: citation_locator and extensions are
not copied. No schema, production registry, validator, or audit result supplies
these example values. This file performs no validation or W04 projection.
"""


def _native_assertion_time():
    return {"state": "unknown", "value": None, "precision": None,
            "reason": "Not recorded in this fictional source."}


def _native_assertion_window():
    return {"start": _native_assertion_time(), "end": _native_assertion_time()}


def _native_assertion_scope():
    return {"inquiry_refs": ["inquiry"], "claim_refs": ["claim"],
            "effective_window": _native_assertion_window()}


def _native_assertion_provenance():
    return {"attributed_to_ref": "actor", "basis_kind": "declaration",
            "evidence_ref_ids": [], "method": "Supplied fictional source statement.",
            "qualifications": ["The source statement is retained without qualification as a toolkit fact."]}


def _native_assertion_envelope(identifier, kind, data):
    return {"id": identifier, "assertion_kind": kind,
            "scope": _native_assertion_scope(),
            "provenance": _native_assertion_provenance(),
            "asserted_at": _native_assertion_time(), "lifecycle_state": "active",
            "lifecycle_basis_ref_ids": [], "data": copy.deepcopy(data)}


def _native_relation_detail_examples():
    # Each tuple is (minimal required fields, all selected optional fields,
    # explicitly optional direct member names). None is not used for absence.
    return {
        "StanceDetails": ({}, {"note": "A supplied stance, not a truth judgment."},
                          ("note",)),
        "CitationDetails": ({}, {"note": "A source citation statement; no locator is selected."},
                            ("note",)),
        "TransformationDetails": ({}, {
            "transformer_ref": "actor", "method_ref": "artifact",
            "occurred_at": _native_assertion_time(), "portion_note": "The stated passage only."},
            ("transformer_ref", "method_ref", "occurred_at", "portion_note")),
        "OriginDetails": ({}, {"dependency_note": "The supplied acquisition link.",
                                  "portion_note": "The claim-bound contribution only."},
                          ("dependency_note", "portion_note")),
        "AgentDetails": ({}, {"role_note": "The named source role only.",
                                 "valid_window": _native_assertion_window()},
                         ("role_note", "valid_window")),
        "ModelDetails": ({}, {"stage_note": "The disclosed model derivation stage.",
                                 "subset_descriptor": "The supplied finite subset.",
                                 "occurred_at": _native_assertion_time()},
                         ("stage_note", "subset_descriptor", "occurred_at")),
        "RetrievalDetails": ({}, {"retrieval_time": _native_assertion_time(),
                                     "portion_note": "The source's retrieved copy only."},
                             ("retrieval_time", "portion_note")),
        "RouteDetails": ({"action_type": "review", "valid_window": _native_assertion_window()},
                         {"action_type": "review", "valid_window": _native_assertion_window(),
                          "route_note": "Declared possibility; applicable authority is separate."},
                         ("route_note",)),
        "SupersessionDetails": ({"reason": "The source states this version succession."},
                                {"reason": "The source states this version succession.",
                                 "effective_at": _native_assertion_time()},
                                ("effective_at",)),
        "IdentityDetails": ({"identity_level": "artifact_version"},
                            {"identity_level": "artifact_version",
                             "identity_note": "Matching identity is attributed, not an implicit merge."},
                            ("identity_note",)),
    }


# Explicitly transcribed predicate/endpoint/dimension/detail bindings, lineage
# section 8.1; the identifiers denote the typed source pool in test_typed_records.
NATIVE_RELATION_BINDINGS = (
    ("supports", "e", "claim", None, "StanceDetails"),
    ("contradicts", "e", "claim", None, "StanceDetails"),
    ("describes", "e", "claim", None, "StanceDetails"),
    ("qualifies", "e", "claim", None, "StanceDetails"),
    ("contextualizes", "e", "claim", None, "StanceDetails"),
    ("corroborates", "e", "e2", None, "StanceDetails"),
    ("cites", "artifact", "artifact2", None, "CitationDetails"),
    ("derived_from", "e", "e2", "acquisition", "TransformationDetails"),
    ("copies", "e", "e2", "acquisition", "TransformationDetails"),
    ("syndicated_from", "e", "e2", "acquisition", "TransformationDetails"),
    ("summarizes", "e", "e2", "acquisition", "TransformationDetails"),
    ("translates", "e", "e2", "acquisition", "TransformationDetails"),
    ("quotes", "e", "e2", "acquisition", "TransformationDetails"),
    ("originates_from", "e", "origin", "acquisition", "OriginDetails"),
    ("depends_on", "origin", "origin2", "acquisition", "OriginDetails"),
    ("generated_by", "artifact", "model", None, "AgentDetails"),
    ("published_by", "artifact", "actor", None, "AgentDetails"),
    ("model_derived_from", "model", "model2", "model_ancestry", "ModelDetails"),
    ("trained_on", "model", "dataset", "model_ancestry", "ModelDetails"),
    ("owned_by", "model", "actor", "organizational_control", "AgentDetails"),
    ("retrieved_from", "artifact", "artifact2", None, "RetrievalDetails"),
    ("propagates_to", "channel", "claim", None, "RouteDetails"),
    ("supersedes", "claim", "claim2", None, "SupersessionDetails"),
    ("same_identity_as", "artifact", "artifact2", None, "IdentityDetails"),
)


def selected_relation(predicate, polarity="affirmed", optional_present=True):
    _, left, right, dimension, detail_kind = next(
        row for row in NATIVE_RELATION_BINDINGS if row[0] == predicate)
    detail_pair = _native_relation_detail_examples()[detail_kind]
    data = {"predicate": predicate, "from_ref": left, "to_ref": right,
            "polarity": polarity, "dimension": dimension,
            "details": detail_pair[1 if optional_present else 0]}
    return _native_assertion_envelope("r-" + predicate, "relation", data)


NATIVE_ASSESSMENT_BINDINGS = (
    ("origin_boundary", "OriginBoundaryDetails", ("origin",), "9.1"),
    ("independence", "IndependenceDetails", ("origin", "origin2"), "9.2"),
    ("coverage", "CoverageDetails", ("inquiry",), "9.3"),
    ("classification", "ClassificationDetails", ("artifact",), "9.4"),
    ("verification", "VerificationDetails", ("actor",), "9.5"),
    ("externality", "ExternalityDetails", ("origin",), "9.6"),
    ("authority", "AuthorityDetails", ("channel",), "9.7"),
    ("capacity", "CapacityDetails", ("channel",), "9.8"),
    ("conflict", "ConflictDetails", ("r-supports", "r-contradicts"), "9.9"),
)


def _native_assessment_details():
    return {
        "origin_boundary": {"dimension": "acquisition", "boundary_role": "declared_origin",
                            "coverage_ref": "a-coverage", "termination_reason": "The supplied origin boundary only."},
        "independence": {"comparison_form": "pairwise", "dimension": "acquisition",
                         "conclusion": "independent_process", "examined_dependency_refs": ["r-depends_on"],
                         "unexamined_dimensions": ["model_ancestry"], "coverage_ref": "a-coverage",
                         "scope_note": "An attributed process comparison, not a runtime qualification."},
        "coverage": {"coverage_kind": "upstream_history", "state": "complete_for_scope",
                     "relation_types": ["originates_from"], "dimensions": ["acquisition"],
                     "member_refs": ["e", "e2"], "omitted_refs": [], "universe_enumerated": True,
                     "scope_note": "The supplied finite source population only."},
        "classification": {"axis": "sil_governance_layer", "labels": ["verified"],
                           "verification_assessment_refs": ["a-verification"],
                           "scope_note": "The recorded governance classification only."},
        "verification": {"verification_scope": "identity", "evaluation_ref": "evaluation",
                         "reported_outcome": "verified", "valid_window": _native_assertion_window(),
                         "scope_note": "A supplied verifier outcome; no toolkit authentication."},
        "externality": {"boundary_inquiry_ref": "inquiry", "conclusion": "external",
                        "grounding_basis": "The source describes acquisition outside the inquiry boundary.",
                        "relevant_time": _native_assertion_time()},
        "authority": {"target_refs": ["claim"], "action_types": ["review"],
                      "valid_window": _native_assertion_window(), "authorized_by_ref": "actor",
                      "grant_state": "denied", "authority_basis": "The supplied actor records a denial.",
                      "coverage_ref": "a-coverage"},
        "capacity": {"reported_capacity": "unmeasured", "unit": "cases",
                     "horizon": _native_assertion_window(), "reported_load": "unmeasured",
                     "scope_note": "Supplied descriptions; no adequacy calculation."},
        "conflict": {"conflict_kind": "affirmation_denial", "resolution_state": "unresolved",
                     "resolution_evaluation_ref": None, "scope_note": "Both supplied assertions remain present."},
    }


def selected_assessment(kind):
    _, _, subjects, _ = next(row for row in NATIVE_ASSESSMENT_BINDINGS if row[0] == kind)
    return _native_assertion_envelope("a-" + kind, "assessment", {
        "assessment_kind": kind, "subject_refs": list(subjects),
        "details": _native_assessment_details()[kind]})


def native_assertion_examples():
    """Return independent positive cases; optional marks only direct members.

    A consumer can delete each present optional member as a positive control;
    deletion of a present nonoptional member is a required-member mutant.
    The minimal/all-present pairs avoid an empty-detail wrong-type blind spot.
    """
    cases = {}

    def add(label, shape, value, section, optional=()):
        cases[label] = {"shape": shape, "value": copy.deepcopy(value),
                        "source": "CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md §" + section,
                        "optional": tuple(optional)}

    add("assertion_scope", "SelectedAssertionScope", _native_assertion_scope(), "7")
    scope = _native_assertion_scope()
    scope["claim_refs"] = []
    add("assertion_scope.metadata", "SelectedAssertionScope", scope, "7")

    for name, (minimal, present, optional) in _native_relation_detail_examples().items():
        add("relation_details." + name + ".absent", "Selected" + name, minimal, "8.3", optional)
        add("relation_details." + name + ".present", "Selected" + name, present, "8.3", optional)
        add("relation_details_union." + name, "SelectedRelationDetails", present, "8.3", optional)

    for predicate, _, _, _, _ in NATIVE_RELATION_BINDINGS:
        assertion = selected_relation(predicate)
        add("relation." + predicate, "SelectedAssertion", assertion, "7–8.3", ("gaps",))
        add("relation_data." + predicate, "SelectedRelationData", assertion["data"], "8.1–8.3")
        add("relation_denied." + predicate, "SelectedAssertion",
            selected_relation(predicate, "denied", False), "7–8.3", ("gaps",))

    # The six transformation predicates admit a separate material-history branch.
    for predicate in ("derived_from", "copies", "syndicated_from", "summarizes", "translates", "quotes"):
        assertion = selected_relation(predicate)
        assertion["data"].update(from_ref="artifact", to_ref="artifact2", dimension=None)
        assertion["scope"]["claim_refs"] = []
        add("relation_material." + predicate, "SelectedAssertion", assertion, "7–8.1", ("gaps",))

    for kind, shape, _, section in NATIVE_ASSESSMENT_BINDINGS:
        assertion = selected_assessment(kind)
        add("assessment." + kind, "SelectedAssertion", assertion, "7; " + section, ("gaps",))
        add("assessment_data." + kind, "SelectedAssessmentData", assertion["data"], section)
        add("assessment_details." + kind, "Selected" + shape, assertion["data"]["details"], section)
        add("assessment_details_union." + kind, "SelectedAssessmentDetails", assertion["data"]["details"], section)

    add("assertion_data.relation", "SelectedAssertionData", selected_relation("supports")["data"], "7–8")
    add("assertion_data.assessment", "SelectedAssertionData", selected_assessment("coverage")["data"], "7; 9")
    add("coverage_assertion", "SelectedCoverageAssertion", selected_assessment("coverage"), "7; 9.3", ("gaps",))
    add("capacity_assertion", "SelectedCapacityAssertion", selected_assessment("capacity"), "7; 9.8", ("gaps",))

    # Nullable factual fields remain present. Their selected assertion carries
    # the exact source Gap required by the input contract, not an invented value.
    nullable = (
        ("origin_boundary", "coverage_ref", "OriginBoundaryDetails", "9.1"),
        ("independence", "coverage_ref", "IndependenceDetails", "9.2"),
        ("verification", "evaluation_ref", "VerificationDetails", "9.5"),
        ("externality", "grounding_basis", "ExternalityDetails", "9.6"),
        ("authority", "authority_basis", "AuthorityDetails", "9.7"),
        ("authority", "coverage_ref", "AuthorityDetails", "9.7"),
        ("capacity", "reported_capacity", "CapacityDetails", "9.8"),
        ("capacity", "unit", "CapacityDetails", "9.8"),
        ("capacity", "reported_load", "CapacityDetails", "9.8"),
    )
    for kind, member, shape, section in nullable:
        assertion = selected_assessment(kind)
        assertion["data"]["details"][member] = None
        assertion["gaps"] = [{"field": "data.details." + member, "reason": "not_recorded",
                              "detail": "This source field was not recorded."}]
        add("assessment_null." + kind + "." + member, "SelectedAssertion", assertion,
            "3.3; " + section, ("gaps",))
        add("assessment_details_null." + kind + "." + member, "Selected" + shape,
            assertion["data"]["details"], section)

    resolved = selected_assessment("conflict")
    resolved["data"]["details"].update(resolution_state="externally_resolved",
                                     resolution_evaluation_ref="evaluation")
    add("assessment.conflict.resolved", "SelectedAssertion", resolved, "9.9", ("gaps",))
    add("assessment_details.conflict.resolved", "SelectedConflictDetails", resolved["data"]["details"], "9.9")

    setwise = selected_assessment("independence")
    setwise["data"]["subject_refs"].append("origin3")
    setwise["data"]["details"]["comparison_form"] = "setwise"
    add("assessment.independence.setwise", "SelectedAssertion", setwise, "9.2", ("gaps",))
    add("assessment_data.independence.setwise", "SelectedAssessmentData", setwise["data"], "9.2")

    for axis, labels in (
        ("sil_data_role", ["surface_linguistic", "world_model", "judgment"]),
        ("hdl_structure_role", ["surface_linguistic_structure", "world_structure", "judgment_structure"]),
        ("sil_governance_layer", ["open_web", "verified", "contested", "judgment"]),
    ):
        details = _native_assessment_details()["classification"]
        details.update(axis=axis, labels=labels)
        add("assessment_details.classification." + axis, "SelectedClassificationDetails", details, "9.4")

    for state in ("partial", "not_examined"):
        details = _native_assessment_details()["coverage"]
        details.update(state=state, universe_enumerated=False)
        add("assessment_details.coverage." + state, "SelectedCoverageDetails", details, "9.3")

    for lifecycle in ("withdrawn", "superseded"):
        assertion = selected_relation("supports")
        assertion["lifecycle_state"] = lifecycle
        assertion["lifecycle_basis_ref_ids"] = ["support"]
        assertion["provenance"]["qualifications"].append("The source records this explicit lifecycle change.")
        add("assertion_lifecycle." + lifecycle, "SelectedAssertion", assertion, "7", ("gaps",))

    return cases


def native_assertion_mutant_suggestions():
    """Single-member mutations against accepted baselines; do not execute them.

    Each case has baseline, path (tuple of dict/list accesses), replacement,
    category, and the frozen-source reason. General direct-member wrong types
    should additionally use every example's explicit optional tuple above.
    """
    mutations = []

    def mutation(baseline, path, value, category, reason):
        mutations.append({"baseline": baseline, "path": path, "value": value,
                          "category": category, "reason": reason})

    for predicate, _, _, dimension, detail_kind in NATIVE_RELATION_BINDINGS:
        baseline = "relation_data." + predicate
        wrong_details = ({"identity_level": "artifact_version"}
                         if detail_kind != "IdentityDetails" else {"action_type": "review", "valid_window": _native_assertion_window()})
        mutation(baseline, ("details",), wrong_details, "kind", "§8.3: details must match this predicate family.")
        mutation(baseline, ("polarity",), "unknown", "state", "§8.1: polarity is affirmed or denied.")
        mutation(baseline, ("from_ref",), True, "wrongtype", "§8.1: source endpoint is an identifier.")
        if predicate not in ("derived_from", "copies", "syndicated_from", "summarizes", "translates", "quotes"):
            bad_dimension = "acquisition" if dimension is None else None
            mutation(baseline, ("dimension",), bad_dimension, "value", "§8.1: this predicate binds dimension/null locally.")
        else:
            mutation(baseline, ("dimension",), "truth", "value", "§8.1: only the five core dimensions or null are allowed.")

    for kind, _, _, section in NATIVE_ASSESSMENT_BINDINGS:
        baseline = "assessment_data." + kind
        replacement = (_native_assessment_details()["capacity"] if kind != "capacity"
                       else _native_assessment_details()["coverage"])
        mutation(baseline, ("details",), replacement, "kind", "§" + section + ": the assessment kind selects its detail shape.")
        mutation(baseline, ("subject_refs",), "origin", "wrongtype", "§9: subjects form an array of distinct identifiers.")

    for kind in ("origin_boundary", "authority", "coverage", "independence", "conflict"):
        mutation("assessment_data." + kind, ("subject_refs",), [], "value", "§9: this assessment has an explicit nonzero subject cardinality.")
    for kind in ("origin_boundary", "authority"):
        mutation("assessment_data." + kind, ("subject_refs",), ["one", "two"], "value", "§9: exactly one subject is required.")
    for kind in ("independence", "conflict"):
        mutation("assessment_data." + kind, ("subject_refs",), ["one"], "value", "§9: at least two distinct subjects are required.")
    mutation("assessment_data.independence", ("subject_refs",), ["origin", "origin2", "origin3"], "value", "§9.2: pairwise has exactly two subjects.")
    mutation("assessment_data.independence.setwise", ("subject_refs",), ["origin"], "value", "§9.2: setwise still needs at least two subjects.")
    mutation("assessment_details.classification.sil_data_role", ("labels",), ["verified"], "value", "§9.4: a governance label is not a data-role label.")
    mutation("assessment_details.classification.hdl_structure_role", ("labels",), ["world_model"], "value", "§9.4: a data-role label is not a structure-role label.")
    mutation("assessment_details.classification.sil_governance_layer", ("labels",), ["world_structure"], "value", "§9.4: a structure-role label is not a governance label.")
    mutation("assessment_details.conflict", ("resolution_evaluation_ref",), "evaluation", "state", "§9.9: unresolved conflicts carry a null resolution reference.")
    mutation("assessment_details.conflict.resolved", ("resolution_evaluation_ref",), None, "state", "§9.9: an external resolution requires its Evaluation reference.")
    mutation("relation.supports", ("assertion_kind",), "assessment", "kind", "§7–9: the outer assertion kind binds its data union.")
    mutation("assessment.coverage", ("assertion_kind",), "relation", "kind", "§7–9: the outer assertion kind binds its data union.")
    mutation("relation_details.CitationDetails.present", ("citation_locator",), "private locator", "field", "Explicit selected-field policy excludes native citation locators.")
    mutation("assessment.coverage", ("extensions",), {"private": "not selected"}, "field", "Explicit selected-field policy excludes input extensions.")
    return mutations


# Independently authored contract specimens. Frozen analytical owner functions
# establish field meanings; D03 records the approved public reference spelling.
def disclosure_field_examples():
    cases = {}

    def add(shape, value, field, source, branch=None):
        label = shape if branch is None else shape + '.' + str(branch)
        cases[label] = {'shape': shape, 'value': value, 'source': source,
                        'field': field, 'branch': branch, 'optional': ()}

    def qualified(native):
        return {'native_record': native, 'qualification_state': 'met', 'reason_codes': []}

    boundary = selected_assessment('origin_boundary')
    coverage = selected_assessment('coverage')
    comparison = selected_assessment('independence')
    capacity = selected_assessment('capacity')
    evaluation = selected_record('evaluation')
    channel = selected_record('correction_channel')
    change = selected_record('correction_event', 'change')
    pipeline = selected_record('pipeline_record')
    claim = selected_record('claim')
    gap = {'source': input_ref('FRONTIER-1'), 'reason_codes': ['upstream_coverage_incomplete']}
    gap_coverage = {'coverage_ref': input_ref('COVERAGE-1', 'assertions'),
                    'qualification_state': 'unmet', 'reason_codes': ['upstream_coverage_incomplete']}
    gap_path = {'nodes': [input_ref('E1'), input_ref('FRONTIER-1')],
                'assertions': [input_ref('A-1', 'assertions')]}
    one_sided = {'from_ref': input_ref('MODEL-1'), 'to_ref': input_ref('MODEL-2')}
    anchor = {'run_key': 'RUN-1', 'stage_key': 'STAGE-1', 'stage': 'admission'}
    case_row = {'case_ref': input_ref('CASE-1'), 'declared': True, 'selected': True,
                'change_event_refs': [input_ref('CHANGE-1')],
                'qualified_change_event_refs': [input_ref('CHANGE-1')],
                'documentary_state': 'met', 'requested_effect_state': 'available', 'reason_codes': []}
    for shape, value, source in (
        ('GapSource', gap, 'analysis/origins.py:_gap_disclosure'),
        ('GapCoverage', gap_coverage, 'analysis/origins.py:_gap_disclosure'),
        ('GapWitnessPath', gap_path, 'analysis/origins.py:_gap_disclosure'),
        ('OneSidedAncestry', one_sided, 'analysis/evaluator_lineage.py:_disclosures'),
        ('StageAnchor', anchor, 'analysis/presence.py:_disclosures; D03 stage-anchor projection'),
        ('CaseChangeRow', case_row, 'analysis/correction_outcomes.py:_disclosures'),
    ):
        cases[shape] = {'shape': shape, 'value': value, 'source': source, 'optional': ()}
    add('OriginBoundaryFields', qualified(boundary), 'origin_boundary_disclosures',
        'analysis/origins.py:_boundary_disclosure')
    add('CoverageFields', qualified(coverage), 'coverage_disclosures', 'validation/semantics.py')
    add('DocumentaryBasisGapFields', qualified(claim), 'documentary_basis_gap_disclosures',
        'validation/semantics.py')
    add('IndependenceAssessmentFields', {'native_record': comparison},
        'independence_assessment_disclosures', 'analysis/process_comparison.py:_disclosures', 0)
    comparison_fields = {'native_record': comparison, 'process_qualification_state': 'met',
                         'origin_qualification_state': 'not_applicable', 'reason_codes': []}
    add('IndependenceAssessmentFields', comparison_fields, 'independence_assessment_disclosures',
        'analysis/process_comparison.py:_disclosures', 1)
    add('AncestryGapFields', {'seed_ref': input_ref('E1'), 'dimension': 'acquisition',
        'gaps': [gap], 'frontiers': [selected_record('unresolved_reference')],
        'coverage': [gap_coverage], 'witness_paths': [gap_path]}, 'ancestry_gap_disclosures',
        'analysis/origins.py:_gap_disclosure')
    add('EvaluatorOverlapFields', {'native_record': evaluation}, 'evaluator_overlap_disclosures',
        'analysis/evaluator_lineage.py:_disclosures', 0)
    add('EvaluatorOverlapFields', {'native_record': evaluation, 'roles': ['judge', 'generator'],
        'left_object_refs': [input_ref('MODEL-1')], 'right_object_refs': [input_ref('MODEL-2')],
        'shared_object_refs': [], 'common_ancestor_refs': [input_ref('MODEL-0')],
        'matching_family_labels': ['SOURCE-FAMILY'], 'missing_family_model_refs': [],
        'one_sided_ancestry': [one_sided], 'roles_complete': True}, 'evaluator_overlap_disclosures',
        'analysis/evaluator_lineage.py:_disclosures', 1)
    add('ExternalityAssessmentFields', {'native_record': selected_assessment('conflict')},
        'externality_assessment_disclosures', 'analysis/presence.py:_disclosures', 0)
    externality = qualified(selected_assessment('externality'))
    externality['qualified_externality'] = 'available'
    add('ExternalityAssessmentFields', externality, 'externality_assessment_disclosures',
        'analysis/presence.py:_disclosures', 1)
    add('PipelineStageFields', qualified(pipeline), 'pipeline_stage_disclosures',
        'analysis/presence.py:_disclosures')
    external_stage = qualified(pipeline)
    external_stage.update(externality_subject_refs=[input_ref('ANOMALY-1')],
                          mapping_assertion_refs=[input_ref('MAP-1', 'assertions')])
    add('ExternalityStageFields', external_stage, 'externality_stage_links',
        'analysis/presence.py:_disclosures')
    add('CohortTransitionFields', {'native_record': coverage, 'stage_anchor': anchor,
        'cohort_qualification_state': 'met', 'transition_qualification_state': 'met', 'reason_codes': []},
        'cohort_transition_disclosures', 'analysis/presence.py:_disclosures')
    add('CorrectionRouteFields', {'native_record': claim}, 'correction_route_disclosures',
        'analysis/correction_routes.py:_disclosures', 0)
    add('CorrectionRouteFields', {'native_record': channel, 'target_ref': input_ref('CLAIM-1'),
        'action_type': 'amend', 'declared_route_recorded': True, 'authorized_route_recorded': True,
        'authorized_route_state': 'available', 'absence_description': 'positive_witness'},
        'correction_route_disclosures', 'analysis/correction_routes.py:_disclosures', 1)
    add('CorrectionRouteFields', {'native_record': selected_assessment('authority'),
        'grant_qualification_state': 'met', 'grant_matches_tuple': True, 'grant_reason_codes': []},
        'correction_route_disclosures', 'analysis/correction_routes.py:_disclosures', 2)
    add('CorrectionCaseFields', {'native_record': selected_record('correction_event', 'submission')},
        'correction_case_disclosures', 'analysis/correction_outcomes.py:_disclosures', 0)
    add('CorrectionCaseFields', {'native_record': change, 'documentary_state': 'met',
        'explicit_removal': False, 'reason_codes': []}, 'correction_case_disclosures',
        'analysis/correction_outcomes.py:_disclosures', 1)
    add('CorrectionTargetChangeFields', {'native_record': claim, 'case_rows': [case_row]},
        'correction_target_change_disclosures', 'analysis/correction_outcomes.py:_disclosures')
    add('ReportedCapacityFields', {'native_record': capacity}, 'reported_capacity_disclosures',
        'analysis/correction_outcomes.py:_disclosures', 0)
    add('ReportedCapacityFields', {'native_record': capacity, 'documentary_state': 'met', 'reason_codes': []},
        'reported_capacity_disclosures', 'analysis/correction_outcomes.py:_disclosures', 1)
    review = {'native_record': evaluation, 'contribution_status': 'recorded_human_contribution',
              'documentary_state': 'met', 'identity_state': 'met', 'reason_codes': []}
    for shape, field in (('HumanContributionFields', 'human_contribution_disclosures'),
                         ('CorrectiveIndependenceFields', 'corrective_independence_disclosures')):
        add(shape, {'native_record': evaluation}, field, 'analysis/human_review.py:_disclosures', 0)
        add(shape, copy.deepcopy(review), field, 'analysis/human_review.py:_record', 1)
    add('CorrectiveIndependenceFields', copy.deepcopy(comparison_fields), 'corrective_independence_disclosures',
        'analysis/human_review.py:_disclosures; process_comparison.py:_disclosures', 2)
    add('AnomalyContextFields', {'native_record': selected_record('anomaly'),
        'context_records': [claim], 'reason_codes': []}, 'anomaly_context_disclosures',
        'analysis/context.py:_disclosures')
    add('ContestationFields', {'native_record': selected_relation('contradicts'),
        'context_records': [claim], 'reason_codes': []}, 'contestation_disclosures',
        'analysis/context.py:_disclosures')
    add('TailStageResultLinkFields', {'source_result_state': 'available', 'source_value_kind': 'fraction'},
        'tail_stage_result_links', 'analysis/context.py:_disclosures')
    return cases


def disclosure_result_example(case):
    field = case['field']
    family = next(family for family, candidate, _ in FIELD_CASES if candidate == field)
    value = result_example(family, field, 'record_disclosures')
    value['result_origin'] = 'attributed_record'
    fields = copy.deepcopy(case['value'])
    source = 'SIT-RES-000002' if field == 'tail_stage_result_links' else input_ref('SOURCE-1')
    native = fields.get('native_record')
    if native is not None:
        collection = ('assertions' if 'assertion_kind' in native else
                      'inquiries' if 'target_claim_refs' in native else
                      'evidence_references' if 'reference_kind' in native else 'records')
        source = input_ref(native['id'], collection)
    value['value'] = {'records': [{'source': source, 'fields': fields,
        'qualifications': ['Only this supplied finite source and explicit qualification are represented.']}]}
    return value


def additional_contract_examples():
    cases = {}

    def add(name, shape, value, source, optional=()):
        cases[name] = {'shape': shape, 'value': value, 'source': source, 'optional': optional}

    add('raw_file_digest', 'RawFileDigest', {'algorithm': 'sha256', 'value': '1' * 64,
        'covered_material': 'Exact supplied file bytes.'}, 'Reporting 16.1; Runtime raw-file identity')
    identity = component_examples()['InputIdentity']
    identity.update(source_mode='local_file', raw_file_digest=copy.deepcopy(cases['raw_file_digest']['value']),
                    declared_predecessor={'bundle_id': 'BUNDLE-1', 'snapshot_id': 'SNAPSHOT-0'})
    add('local_file_identity', 'InputIdentity', identity, 'Reporting 16.1; W02 declarations only')
    add('window.optional_note', 'TimeWindow', {'start': time_value(), 'end': time_value(),
        'note': 'The source supplies neither bound.'}, 'Lineage 3.1', ('note',))
    add('known_time.optional_reason', 'TimeValue', time_value('known', '2024-02-29', 'date',
        'Original recorded source date.'), 'Lineage 3.1', ('reason',))
    time = {name: time_value() for name in ('asserted_at', 'occurred_at', 'observed_at',
                                           'published_at', 'retrieved_at', 'as_of')}
    time.update(valid_window={'start': time_value(), 'end': time_value()},
                time_window={'start': time_value(), 'end': time_value()})
    add('basis.all_source_times', 'BasisTime', time, 'Reporting 16.3; Lineage 3.1,4,7', tuple(time))
    scope = component_examples()['Scope']
    scope.update(temporal_basis='time_specific', requested_time=time_value('known', '2024-02-29', 'date', None))
    add('scope.time_specific', 'Scope', scope, 'Reporting 16.2; contracts/results.py:_Scope')
    for kind in ('cycle', 'members', 'no_witness_in_examined_view'):
        component = graph_component()
        component.update(kind=kind, nodes=[], edges=[], member_count=0)
        if kind == 'members':
            component.update(members=[graph_node()], member_count=1)
        elif kind == 'cycle':
            edge = graph_edge()
            edge.update(source=graph_node('O1', 'origin_event'), target=graph_node('O1', 'origin_event'),
                        predicate='depends_on')
            component.update(nodes=[graph_node('O1', 'origin_event'), graph_node('O1', 'origin_event')], edges=[edge],
                members=[graph_node('O1', 'origin_event')], internal_edges=[copy.deepcopy(edge)], member_count=5)
        else:
            component.update(starts=[graph_node()], target=graph_node('UNREACHED-1'),
                examined_nodes=[graph_node(), graph_node('O1', 'origin_event')],
                examined_edges=[graph_edge()], frontiers=[graph_node('O1', 'origin_event')],
                terminals=[graph_node('O1', 'origin_event')], observations=[graph_edge()], member_count=8)
        add('graph.' + kind, 'GraphWitnessComponent', component, 'graph/witnesses.py:_commit and owner constructors')
    add('audit.diagnostic', 'AuditReport', diagnostic_document(), 'Reporting 16.1')
    return cases


def extended_contract_examples():
    cases = {}
    for group in (native_record_examples(), native_assertion_examples(),
                  disclosure_field_examples(), additional_contract_examples()):
        for name, case in group.items():
            assert name not in cases, name
            cases[name] = case
    return cases


EXTENDED_CONTRACT_CASES = extended_contract_examples()


@pytest.mark.parametrize('name', tuple(EXTENDED_CONTRACT_CASES))
def test_each_nested_contract_branch_has_an_independent_positive(name):
    case = EXTENDED_CONTRACT_CASES[name]
    assert case['source']
    assert_component(copy.deepcopy(case['value']), case['shape'])
    if case['shape'] in ('SelectedInquiry', 'SelectedRecord', 'SelectedAssertion', 'SelectedEvidenceReference'):
        assert_component(copy.deepcopy(case['value']), 'SelectedNative')


@pytest.mark.parametrize('name,member', [(name, member)
    for name, case in EXTENDED_CONTRACT_CASES.items() for member in case['value']
    if case['shape'] not in ('SelectedNative', 'SelectedRelationDetails',
        'SelectedAssessmentDetails', 'SelectedAssertionData')])
@pytest.mark.parametrize('mutation', ('missing', 'wrong_type'))
def test_each_nested_contract_branch_member_has_its_own_control(name, member, mutation):
    case = EXTENDED_CONTRACT_CASES[name]
    value = copy.deepcopy(case['value'])
    assert_component(value, case['shape'])
    if mutation == 'missing':
        del value[member]
        if member in case.get('optional', ()):
            assert_component(value, case['shape'])
            return
    else:
        value[member] = {'undeclared_member': 'not the declared member type'}
    reject_component(value, case['shape'])


@pytest.mark.parametrize('name', tuple(EXTENDED_CONTRACT_CASES))
def test_each_nested_contract_branch_is_closed(name):
    case = EXTENDED_CONTRACT_CASES[name]
    value = copy.deepcopy(case['value'])
    assert_component(value, case['shape'])
    value['undeclared_member'] = 'No generic source export or extension slot.'
    reject_component(value, case['shape'])


# Closed vocabulary fields are fixed by the frozen input/report definitions.
# Free source prose (method, note, detail, labels, capacity text) is not treated
# as an enum. This list is independent of the schema keyword implementation.
CLOSED_LITERAL_MEMBERS = frozenset(('kind', 'type', 'state', 'event_kind', 'assertion_kind',
    'assessment_kind', 'predicate', 'polarity', 'stage', 'qualification_state',
    'cohort_qualification_state', 'transition_qualification_state', 'process_qualification_state',
    'origin_qualification_state', 'grant_qualification_state', 'documentary_state', 'identity_state',
    'contribution_status', 'authorized_route_state', 'absence_description', 'requested_effect_state',
    'source_result_state', 'source_value_kind', 'reference_kind', 'availability', 'artifact_kind',
    'actor_kind', 'epistemic_type', 'evaluation_kind', 'role', 'submission_kind', 'outcome', 'action_type',
    'classification_state', 'reason', 'lifecycle_state', 'dimension', 'identity_level', 'boundary_role',
    'comparison_form', 'conclusion', 'coverage_kind', 'axis', 'verification_scope', 'reported_outcome',
    'grant_state', 'conflict_kind', 'resolution_state', 'algorithm'))


@pytest.mark.parametrize('name,member', [(name, member) for name, case in EXTENDED_CONTRACT_CASES.items()
    for member, value in case['value'].items() if member in CLOSED_LITERAL_MEMBERS and type(value) is str
    and (member != 'reason' or case['shape'] in ('SelectedGap', 'SelectedUnresolvedReferenceData'))])
def test_nested_closed_vocabulary_cannot_acquire_an_invented_state(name, member):
    case = EXTENDED_CONTRACT_CASES[name]
    value = copy.deepcopy(case['value'])
    assert_component(value, case['shape'])
    value[member] = 'invented_contract_state'
    reject_component(value, case['shape'])


@pytest.mark.parametrize('name,member', (('handling_details', 'reason'),
    ('relation_details.SupersessionDetails.present', 'reason'),
    ('relation_details_union.SupersessionDetails', 'reason'),
    ('assessment_details.externality', 'grounding_basis')))
def test_selected_source_prose_is_not_reclassified_as_a_toolkit_enum(name, member):
    # Lineage 6.9, 8.3, 9.6 declare source text here, unlike Gap.reason's enum.
    case = EXTENDED_CONTRACT_CASES[name]
    value = copy.deepcopy(case['value'])
    assert_component(value, case['shape'])
    value[member] = 'The source describes its own reason and limitation.'
    assert_component(value, case['shape'])


@pytest.mark.parametrize('name,member', [(name, member) for name, case in EXTENDED_CONTRACT_CASES.items()
    for member, value in case['value'].items() if type(value) is list])
def test_nested_array_member_items_keep_their_declared_scalar_or_object_type(name, member):
    case = EXTENDED_CONTRACT_CASES[name]
    value = copy.deepcopy(case['value'])
    assert_component(value, case['shape'])
    value[member] = [False]
    reject_component(value, case['shape'])


DISCLOSURE_BRANCH_CASES = {name: case for name, case in EXTENDED_CONTRACT_CASES.items() if 'field' in case}


@pytest.mark.parametrize('name', tuple(DISCLOSURE_BRANCH_CASES))
def test_each_disclosure_branch_is_available_under_its_registered_result_field(name):
    case = DISCLOSURE_BRANCH_CASES[name]
    result = disclosure_result_example(case)
    assert_component(result, 'Result')
    wrong = copy.deepcopy(result)
    wrong['value']['records'][0]['source'] = (input_ref('SOURCE-1') if case['field'] ==
        'tail_stage_result_links' else 'SIT-RES-000002')
    reject_component(wrong, 'Result')


@pytest.mark.parametrize('name', tuple(DISCLOSURE_BRANCH_CASES))
@pytest.mark.parametrize('path,member', ((('value',), 'records'), (('value', 'records', 0), 'source'),
    (('value', 'records', 0), 'fields'), (('value', 'records', 0), 'qualifications')))
@pytest.mark.parametrize('mutation', ('missing', 'wrong_type', 'extra'))
def test_each_field_specific_disclosure_container_and_row_is_closed_and_typed(name, path, member, mutation):
    result = disclosure_result_example(DISCLOSURE_BRANCH_CASES[name])
    assert_component(result, 'Result')
    value = result
    for part in path:
        value = value[part]
    if mutation == 'missing':
        del value[member]
    elif mutation == 'wrong_type':
        value[member] = {'undeclared_member': 'wrong type'}
    else:
        value['undeclared_member'] = 'not a field-specific member'
    reject_component(result, 'Result')


def test_optional_scope_time_and_cohort_anchor_branches_are_not_silently_null_only():
    scope = copy.deepcopy(EXTENDED_CONTRACT_CASES['scope.time_specific']['value'])
    assert_component(scope, 'Scope')
    scope['requested_time'] = None
    reject_component(scope, 'Scope')
    case = copy.deepcopy(DISCLOSURE_BRANCH_CASES['CohortTransitionFields']['value'])
    assert_component(case, 'CohortTransitionFields')
    case['stage_anchor'] = None
    assert_component(case, 'CohortTransitionFields')


def test_local_file_digest_rejects_wrong_algorithm_and_non_sha256_bytes():
    baseline = copy.deepcopy(EXTENDED_CONTRACT_CASES['raw_file_digest']['value'])
    assert_component(baseline, 'RawFileDigest')
    for member, value in (('algorithm', 'sha1'), ('value', 'A' * 64), ('value', '1' * 63),
                           ('value', '1' * 65), ('value', 'g' * 64), ('covered_material', '')):
        changed = copy.deepcopy(baseline)
        changed[member] = value
        reject_component(changed, 'RawFileDigest')


def test_interrupted_accepted_audit_has_a_positive_contract_before_illegal_state_mutation():
    # A fully parsed input may stop before any family completes. This is a
    # hand-authored local contract specimen, not a constructed public report.
    document = diagnostic_document('audit_report', 'interrupted', 'accepted')
    labels = ('Artifact and contribution inventory', 'Declared provenance and process metadata',
        'Origin-resolution and scoped process-assessment evidence', 'Evaluator, correction-route and authority evidence',
        'Boundary-qualified external input, stage histories and documented correction outcomes')
    document['observability_domains'] = [{'level_index': index, 'label': label,
        'available_result_refs': [], 'unavailable_result_refs': [], 'not_evaluated_result_refs': [],
        'reason_refs': []} for index, label in enumerate(labels)]
    assert_both(document)
    document['input_validation']['state'] = 'not_completed'
    assert_rejected(document)


@pytest.mark.parametrize('baseline,path,replacement,source', native_record_binding_cases())
def test_native_record_discriminator_selects_its_own_closed_payload(baseline, path, replacement, source):
    case = EXTENDED_CONTRACT_CASES[baseline]
    value = copy.deepcopy(case['value'])
    assert_component(value, case['shape'])
    owner = value
    for part in path[:-1]:
        owner = owner[part]
    owner[path[-1]] = replacement
    reject_component(value, case['shape'])


@pytest.mark.parametrize('baseline,path,candidates,source', native_record_enum_cases())
def test_source_native_record_enums_have_positive_values_before_an_invented_value(baseline, path, candidates, source):
    case = EXTENDED_CONTRACT_CASES[baseline]
    for replacement in candidates:
        value = copy.deepcopy(case['value'])
        owner = value
        for part in path[:-1]:
            owner = owner[part]
        if type(owner) is list:
            # A singleton positive avoids accidentally duplicating a second
            # existing member while sweeping a distinct source enum value.
            owner[:] = [replacement]
        else:
            owner[path[-1]] = replacement
        assert_component(value, case['shape'])
        owner[path[-1]] = 'invented_contract_state'
        reject_component(value, case['shape'])


@pytest.mark.parametrize('case', native_assertion_mutant_suggestions(),
                         ids=lambda case: case['baseline'] + ':' + '.'.join(map(str, case['path'])))
def test_native_assertion_discriminators_cardinality_and_states_are_bound_locally(case):
    baseline = EXTENDED_CONTRACT_CASES[case['baseline']]
    value = copy.deepcopy(baseline['value'])
    assert_component(value, baseline['shape'])
    owner = value
    for part in case['path'][:-1]:
        owner = owner[part]
    owner[case['path'][-1]] = copy.deepcopy(case['value'])
    reject_component(value, baseline['shape'])


def closed_object_coverage():
    """Inventory test destinations, never manufacture positive fixture values.

    Object pointers come from the delivered schema; every value and optional
    member list comes from independently handwritten source specimens above.
    AllOf's repeated per-field record containers remain separately accounted.
    """
    schema = report_schema()
    inventory = {}
    old = {name: {'shape': name, 'value': value, 'source': 'Reporting 12–18; N01 component_examples',
                  'optional': ('note',) if name == 'TimeWindow' else
                              ('asserted_at',) if name == 'BasisTime' else ()}
           for name, value in component_examples().items()}
    for group_name, cases in (('component_examples', old), ('EXTENDED_CONTRACT_CASES', EXTENDED_CONTRACT_CASES)):
        for name, case in cases.items():
            shape = case['shape']
            rule = schema['$defs'][shape]
            pointer = '#/$defs/' + shape
            branch = case.get('branch')
            if branch is not None:
                pointer += '/anyOf/' + str(branch)
                rule = rule['anyOf'][branch]
            if rule.get('type') != 'object':
                continue
            entry = inventory.setdefault(pointer, {'shape': shape, 'specimens': [], 'members': {},
                'extra_member_test': ('test_every_fixed_component_rejects_an_extra_member'
                    if group_name == 'component_examples' else 'test_each_nested_contract_branch_is_closed')})
            entry['specimens'].append({'group': group_name, 'case': name, 'source': case['source']})
            for member in case['value']:
                if group_name == 'component_examples' and (shape, member) in (
                        ('TimeWindow', 'note'), ('BasisTime', 'asserted_at')):
                    continue
                member_entry = entry['members'].setdefault(member, {'positive_cases': [], 'type_cases': [],
                    'missing_rejected_cases': [], 'optional_omission_accepted_cases': []})
                member_entry['positive_cases'].append(name)
                member_entry['type_cases'].append(name)
                key = 'optional_omission_accepted_cases' if member in case.get('optional', ()) else 'missing_rejected_cases'
                member_entry[key].append(name)
    for index, condition in enumerate(schema['$defs']['Result']['allOf']):
        if condition.get('then', {}).get('properties', {}).get('value', {}).get('type') != 'object':
            continue
        field = condition.get('if', {}).get('properties', {}).get('field_key', {}).get('const')
        cases = [(name, case) for name, case in DISCLOSURE_BRANCH_CASES.items() if case['field'] == field]
        if not cases:
            continue
        base = '#/$defs/Result/allOf/' + str(index) + '/then/properties/value'
        for suffix, members in (('', ('records',)), ('/properties/records/items', ('source', 'fields', 'qualifications'))):
            inventory[base + suffix] = {'shape': 'Result field-specific container' if not suffix else 'Result field-specific row',
                'field_key': field, 'specimens': [{'group': 'DISCLOSURE_BRANCH_CASES', 'case': name,
                    'source': case['source']} for name, case in cases],
                'members': {member: {'positive_cases': [name for name, _ in cases],
                    'type_cases': [name for name, _ in cases], 'missing_rejected_cases': [name for name, _ in cases],
                    'optional_omission_accepted_cases': []} for member in members},
                'extra_member_test': 'test_each_field_specific_disclosure_container_and_row_is_closed_and_typed'}
    return inventory


def test_all_160_closed_schema_objects_have_explicit_positive_and_member_controls():
    schema = report_schema()
    objects = {}

    def collect(rule, pointer):
        if type(rule) is dict:
            if rule.get('type') == 'object':
                objects[pointer] = rule
            for name, value in rule.items():
                collect(value, pointer + '/' + name)
        elif type(rule) is list:
            for index, value in enumerate(rule):
                collect(value, pointer + '/' + str(index))

    collect(schema, '#')
    coverage = closed_object_coverage()
    assert len(objects) == 160  # frozen schema census, not an outcome-count gate
    assert set(coverage) == set(objects), sorted(set(objects) - set(coverage))
    for pointer, rule in objects.items():
        assert rule['additionalProperties'] is False
        entry = coverage[pointer]
        assert entry['specimens'] and entry['extra_member_test'], pointer
        assert set(entry['members']) == set(rule['properties']), pointer
        for member, evidence in entry['members'].items():
            assert evidence['positive_cases'] and evidence['type_cases'], (pointer, member)
            if member in rule.get('required', ()):
                assert evidence['missing_rejected_cases'], (pointer, member)
            else:
                assert evidence['optional_omission_accepted_cases'], (pointer, member)


@pytest.mark.parametrize("state,reason", (
    ("interrupted", "resource_limit_reached"),
    ("failed", "execution_failed"),
    ("rejected", "input_not_accepted"),
))
def test_w07_abort_retains_rejection_when_diagnostic_pair_cannot_be_delivered(state, reason):
    # Architecture 18.4: actual acceptance survives output failure. Governance
    # 22.3: an earlier established rejection survives later caller cancellation.
    error = execution.AuditAbort(state, "rejected", reason)
    assert error.processing_state == state
    assert error.input_validation_state == "rejected"
    assert error.reason_code == reason
    assert error.publication_state == "not_published"
    assert error.args == ("Audit could not be completed.",)
    assert repr(error) == "AuditAbort()"
    with pytest.raises((AttributeError, TypeError)):
        error.input_validation_state = "accepted"
    with pytest.raises(TypeError, match="^invalid_audit_transport$"):
        execution.AuditCancelled("rejected")


@pytest.mark.parametrize("state,input_state,reason", (
    ("rejected", "accepted", "input_not_accepted"),
    ("rejected", "not_completed", "input_not_accepted"),
    ("rejected", "rejected", "execution_failed"),
    ("rejected", "rejected", "resource_limit_reached"),
    ("interrupted", "rejected", "input_not_accepted"),
    ("failed", "rejected", "input_not_accepted"),
    ("completed", "rejected", "input_not_accepted"),
    ("cancelled", "rejected", "input_not_accepted"),
))
def test_w07_rejection_transport_extension_does_not_allow_invented_state_pairs(state, input_state, reason):
    with pytest.raises(TypeError, match="^invalid_audit_transport$"):
        execution.AuditAbort(state, input_state, reason)


def test_w07_delivered_report_attributes_and_nested_values_remain_immutable():
    from source_integrity_toolkit.runtime.boundary import _audit_value
    report = _audit_value({})
    assert type(report) is report_contract.AuditReport
    assert report.report_kind == "validation_diagnostics"
    for member in ROOT_MEMBERS:
        original = getattr(report, member)
        with pytest.raises((AttributeError, TypeError)):
            setattr(report, member, None)
        with pytest.raises((AttributeError, TypeError)):
            delattr(report, member)
        assert getattr(report, member) is original
    for member in report_contract.AuditReport.__slots__:
        with pytest.raises((AttributeError, TypeError)):
            setattr(report, member, None)
    with pytest.raises(TypeError):
        report.run["processing_state"] = "completed"
    with pytest.raises(TypeError):
        report.run["started_at"]["state"] = "known"
    with pytest.raises(TypeError):
        report.run["requested_diagnostic_ids"][0] = "invented"
    with pytest.raises((AttributeError, TypeError)):
        report.run._pairs = ()
    with pytest.raises(TypeError):
        report_contract.AuditReport({})
    with pytest.raises(TypeError):
        class CallerReport(report_contract.AuditReport):
            pass


@pytest.mark.parametrize("kind", ("abort", "cancelled"))
def test_w07_safe_transports_cross_contextmanager_with_original_exception_identity(kind):
    from contextlib import contextmanager
    from dataclasses import fields

    error = (execution.AuditAbort("interrupted", "accepted", "resource_limit_reached")
             if kind == "abort" else execution.AuditCancelled("accepted"))

    @contextmanager
    def transparent_context():
        yield

    with pytest.raises(type(error)) as caught:
        with transparent_context():
            raise error
    assert caught.value is error
    assert error.__traceback__ is not None
    assert error.input_validation_state == "accepted"
    assert error.publication_state == "not_published"
    for field in fields(error):
        value = getattr(error, field.name)
        with pytest.raises((AttributeError, TypeError)):
            setattr(error, field.name, "caller_secret")
        with pytest.raises((AttributeError, TypeError)):
            delattr(error, field.name)
        assert getattr(error, field.name) == value
    for name in ("args", "safe_message", "caller_secret"):
        with pytest.raises((AttributeError, TypeError)):
            setattr(error, name, "caller_secret")


@pytest.mark.parametrize("kind", ("abort", "cancelled"))
def test_w07_safe_transport_traceback_slot_rejects_invalid_values_and_hostile_names(kind):
    calls = []

    def touched(*args, **kwargs):
        calls.append("protocol")
        raise AssertionError("transport executed hostile protocol")

    class Hostile:
        __str__ = __repr__ = __eq__ = __bool__ = touched

    class HostileName(str):
        __str__ = __repr__ = __eq__ = touched

    error = (execution.AuditAbort("failed", "not_completed", "execution_failed")
             if kind == "abort" else execution.AuditCancelled("not_completed"))
    for value in (True, 1, {}, Hostile()):
        with pytest.raises(TypeError):
            error.__traceback__ = value
        assert error.__traceback__ is None
    for name in (Hostile(), HostileName("__traceback__")):
        with pytest.raises((AttributeError, TypeError)):
            type(error).__setattr__(error, name, None)
    error.__traceback__ = None
    assert error.__traceback__ is None and calls == []
    assert error.input_validation_state == "not_completed"
    assert error.publication_state == "not_published"


def test_w07_generic_serialization_cannot_dump_private_report_byte_caches():
    from dataclasses import asdict
    from types import MappingProxyType
    from source_integrity_toolkit.runtime.boundary import _audit_value

    report = _audit_value({})
    assert type(report._document) is MappingProxyType
    assert set(report._document) == set(ROOT_MEMBERS)
    original_fields = tuple(getattr(report, name) for name in ROOT_MEMBERS)
    json_bytes, markdown_bytes = report.to_json_bytes(), report.to_markdown_bytes()
    for serialize in (asdict, copy.deepcopy, json.dumps):
        with pytest.raises(TypeError):
            serialize(report)
    with pytest.raises(TypeError):
        json.dumps(report, default=asdict)
    with pytest.raises(TypeError):
        report._document["run"] = None
    for name, original in zip(ROOT_MEMBERS, original_fields):
        assert getattr(report, name) is original
    assert report.to_json_bytes() is json_bytes
    assert report.to_markdown_bytes() is markdown_bytes
