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
    schema = load_json(SCHEMA_PATH)
    assert schema_accepts(document, schema, schema)
    return validate(document)


def assert_rejected(document, *, schema_too=True):
    if schema_too:
        schema = load_json(SCHEMA_PATH)
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
    assert package.__all__ == ("audit_bundle", "audit_file", "__version__")
    with pytest.raises(NotImplementedError):
        package.audit_bundle({})
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
    schema = load_json(SCHEMA_PATH)
    assert schema_accepts(value, schema["$defs"][shape], schema), shape
    port = validate_component(value, shape)
    assert port.units > 0 and port.checks > 0
    return port


def reject_component(value, shape, *, schema_too=True):
    if schema_too:
        schema = load_json(SCHEMA_PATH)
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
    schema = load_json(SCHEMA_PATH)
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
