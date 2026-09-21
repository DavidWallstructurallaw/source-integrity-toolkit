# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W03 temporal components, with independent frozen-source expectations.

Oracles: Lineage 3.1, 7, 10.7, 12.3, 14; Definitions 14.2-14.3, 20.5;
Reporting 16 and W6-26; PHASE_3_PLAN 3.4 and 8; Governance 22.3.
Date intervals are not instants. The sources give no window endpoint closure
rule, so the positive applicability cases use strictly interior instants.
These private component jobs do not claim W13 orchestration or a whole PC.
"""
import importlib.util
from pathlib import Path

import pytest

from source_integrity_toolkit.contracts.bundle import _Object
from source_integrity_toolkit.contracts.evidence import _Node, _PreparedBundle, _QualificationContext
from source_integrity_toolkit.contracts.execution import _AnalysisAborted, _AuditCancelled
from source_integrity_toolkit.runtime import resources
from source_integrity_toolkit.runtime.boundary import _prepare_value
from source_integrity_toolkit.validation import semantics


_spec = importlib.util.spec_from_file_location(
    "sit_w03_temporal_input_cases", Path(__file__).with_name("test_typed_records.py"))
cases = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(cases)


def known(text, precision="instant"):
    return {"state": "known", "value": text, "precision": precision}


def unknown(state="unknown"):
    return {"state": state, "value": None, "precision": None,
            "reason": "Fictional effective time is not supplied."}


def time_node(value):
    # Valid bounded source constants satisfy this component's precondition.
    # _Node is a representation constructor, not an admission certificate.
    return _Node("TimeValue", _Object(tuple(sorted(value.items()))))


def window_node(start, end, note=None):
    fields = {"start": time_node(start).fields, "end": time_node(end).fields}
    if note is not None:
        fields["note"] = note
    return _Node("TimeWindow", _Object(tuple(sorted(fields.items()))))


@pytest.fixture
def clock(monkeypatch):
    now = [100]
    monkeypatch.setattr(resources, "monotonic_ns", lambda: now[0])
    return now


def accepted_job():
    owner = resources._new_analysis_budget()
    owner.record_input_acceptance()  # Explicit trusted component fact only.
    return owner, owner.start_job()


def temporal_context(basis, requested=None):
    return _QualificationContext("inquiry", ("claim",), ("origin", "origin2"),
                                 "acquisition", basis, requested, None, ("depends_on",), "claim_origin")


def supported_assertion(lifecycle="active"):
    value = cases.pool()
    assertion = cases.relation("depends_on")
    assertion["id"] = "temporal-assertion"
    assertion["provenance"].update(basis_kind="documented_record", evidence_ref_ids=["support"])
    assertion["lifecycle_state"] = lifecycle
    if lifecycle != "active":
        assertion["lifecycle_basis_ref_ids"] = ["support"]
        assertion["provenance"]["qualifications"].append("Supplied current lifecycle; no historical status inferred.")
    value["assertions"] = [assertion]
    return value, assertion


# Literal relationships follow calendar and UTC arithmetic, independently of
# the product's parser. There is no datetime/float conversion oracle here.
@pytest.mark.parametrize("left,right,expected", [
    ("2026-09-19T03:00:00.50+03:00", "2026-09-19T00:00:00.500Z", "equal"),
    ("2026-09-20T00:15:00+01:00", "2026-09-19T23:15:00Z", "equal"),
    ("2000-03-01T00:00:00+01:00", "2000-02-29T23:00:00Z", "equal"),
    ("2027-01-01T00:00:00+14:00", "2026-12-31T10:00:00Z", "equal"),
    ("2026-12-31T23:30:00-01:00", "2027-01-01T00:30:00Z", "equal"),
    ("0001-01-01T00:00:00+23:59", "0001-01-01T00:00:00Z", "before"),
    ("9999-12-31T23:59:59-23:59", "9999-12-31T23:59:59Z", "after"),
    ("1900-02-28T23:59:59Z", "1900-03-01T00:00:00Z", "before"),
    ("2000-02-29T00:00:00Z", "2000-02-28T23:59:59Z", "after"),
    ("2026-09-19T00:00:00.000000000000000001Z",
     "2026-09-19T00:00:00.000000000000000002Z", "before"),
    ("2026-09-19T00:00:00.1001Z", "2026-09-19T00:00:00.1Z", "after"),
])
def test_known_instants_compare_exactly_across_fraction_offset_and_calendar_boundaries(
        clock, left, right, expected):
    owner, job = accepted_job()
    nodes = time_node(known(left)), time_node(known(right))
    result = semantics._compare_times(*nodes, job)
    assert result.comparison == expected and result.reason_codes == ()
    assert result.source_times == nodes
    assert dict(nodes[0].fields.items) == known(left)
    assert dict(nodes[1].fields.items) == known(right)
    inverse = {"before": "after", "after": "before", "equal": "equal"}[expected]
    reversed_result = semantics._compare_times(nodes[1], nodes[0], job)
    assert reversed_result.comparison == inverse
    assert reversed_result.source_times == (nodes[1], nodes[0])
    assert owner.input_state == "accepted"


@pytest.mark.parametrize("left,right,expected", [
    ("0001-01-01", "9999-12-31", "before"),
    ("2024-03-01", "2024-02-29", "after"),
    ("1900-02-28", "1900-03-01", "before"),
    ("2026-09-19", "2026-09-19", "overlap"),
])
def test_date_precision_establishes_only_interval_order(clock, left, right, expected):
    _, job = accepted_job()
    nodes = time_node(known(left, "date")), time_node(known(right, "date"))
    result = semantics._compare_times(*nodes, job)
    assert result.comparison == expected
    assert result.reason_codes == (("time_applicability_unknown",) if expected == "overlap" else ())
    assert result.source_times == nodes


@pytest.mark.parametrize("state", ("unknown", "withheld", "not_applicable"))
@pytest.mark.parametrize("side", ("left", "right"))
def test_nonknown_times_remain_unknown_without_structural_rejection(clock, state, side):
    owner, job = accepted_job()
    nodes = [time_node(unknown(state)), time_node(known("2026-09-19T00:00:00Z"))]
    if side == "right":
        nodes.reverse()
    result = semantics._compare_times(*nodes, job)
    assert result.comparison == "unknown"
    assert result.reason_codes == ("time_applicability_unknown",)
    assert result.source_times == tuple(nodes) and owner.input_state == "accepted"


@pytest.mark.parametrize("timezone", ("UTC", "Pacific/Kiritimati", "America/Los_Angeles"))
@pytest.mark.parametrize("instant", ("2026-09-18T23:59:59Z", "2026-09-19T00:00:00Z",
                                     "2026-09-20T00:00:00Z"))
def test_mixed_precision_never_invents_midnight_or_a_host_timezone(clock, monkeypatch, timezone, instant):
    monkeypatch.setenv("TZ", timezone)
    _, job = accepted_job()
    date = time_node(known("2026-09-19", "date"))
    point = time_node(known(instant))
    for nodes in ((date, point), (point, date)):
        result = semantics._compare_times(*nodes, job)
        assert result.comparison == "unknown"
        assert result.reason_codes == ("time_applicability_unknown",)
        assert result.source_times == nodes


def test_fractional_tail_beyond_native_integer_and_float_precision_is_exact_and_paid(clock):
    owner, job = accepted_job()
    tail = "0" * 6000
    left = time_node(known("2026-09-19T00:00:00." + tail + "1Z"))
    right = time_node(known("2026-09-19T00:00:00." + tail + "2Z"))
    before = owner.used
    result = semantics._compare_times(left, right, job)
    assert result.comparison == "before" and result.reason_codes == ()
    delta = owner.used - before
    assert delta == job.used and delta > 6000 // 256
    # A repeated semantic call is paid again, not a free cross-job cache hit.
    before = owner.used
    again = semantics._compare_times(left, right, job)
    assert again.comparison == "before" and owner.used - before == delta


@pytest.mark.parametrize("requested,expected", [
    ("2026-09-19T00:00:00Z", "met"),
    ("2026-09-18T23:59:58Z", "unmet"),
    ("2026-09-19T00:00:02Z", "unmet"),
])
def test_strict_window_interior_and_exterior_need_no_endpoint_convention(clock, requested, expected):
    owner, job = accepted_job()
    window = window_node(known("2026-09-18T23:59:59Z"), known("2026-09-19T00:00:01Z"))
    point = time_node(known(requested))
    result = semantics._time_applicability(window, point, job)
    assert result.state == expected
    if expected == "met":
        assert result.reason_codes == ()
    else:
        assert result.reason_codes == ("time_applicability_unknown",)
    assert len(result.source_times) == 3 and result.source_times[-1] is point
    assert dict(result.source_times[0].fields.items) == known("2026-09-18T23:59:59Z")
    assert dict(result.source_times[1].fields.items) == known("2026-09-19T00:00:01Z")
    assert owner.input_state == "accepted"


@pytest.mark.parametrize("endpoint", ("2026-09-19T00:00:00Z", "2026-09-20T03:00:00+03:00"))
@pytest.mark.parametrize("note", (None, "Both endpoints are inclusive.", "Both endpoints are exclusive."))
def test_endpoint_and_unstructured_note_cannot_supply_an_unstated_closure_rule(clock, endpoint, note):
    _, job = accepted_job()
    window = window_node(known("2026-09-19T00:00:00Z"), known("2026-09-20T00:00:00Z"), note)
    result = semantics._time_applicability(window, time_node(known(endpoint)), job)
    assert result.state == "unknown" and result.reason_codes == ("time_applicability_unknown",)


def test_equal_window_endpoints_do_not_invent_an_inclusive_singleton(clock):
    _, job = accepted_job()
    window = window_node(known("2026-09-19T00:00:00.50Z"), known("2026-09-19T03:00:00.500+03:00"))
    result = semantics._time_applicability(window, time_node(known("2026-09-19T00:00:00.5Z")), job)
    assert result.state == "unknown" and result.reason_codes == ("time_applicability_unknown",)


@pytest.mark.parametrize("position", ("start", "end", "requested"))
@pytest.mark.parametrize("state", ("unknown", "withheld", "not_applicable"))
def test_unknown_effective_time_cannot_satisfy_a_time_specific_request(clock, position, state):
    owner, job = accepted_job()
    values = {"start": known("2026-09-18T00:00:00Z"), "end": known("2026-09-20T00:00:00Z"),
              "requested": known("2026-09-19T00:00:00Z")}
    values[position] = unknown(state)
    result = semantics._time_applicability(window_node(values["start"], values["end"]),
                                          time_node(values["requested"]), job)
    assert result.state == "unknown" and result.reason_codes == ("time_applicability_unknown",)
    assert owner.input_state == "accepted"


@pytest.mark.parametrize("start,end,requested", [
    (known("2026-09-18", "date"), known("2026-09-20", "date"), known("2026-09-19T00:00:00Z")),
    (known("2026-09-18T00:00:00Z"), known("2026-09-20T00:00:00Z"), known("2026-09-19", "date")),
    (known("2026-09-18", "date"), known("2026-09-20T00:00:00Z"), known("2026-09-19T00:00:00Z")),
    (known("2026-09-19", "date"), known("2026-09-20", "date"), known("2026-09-19", "date")),
])
def test_date_precision_does_not_become_instant_grant_eligibility(clock, start, end, requested):
    _, job = accepted_job()
    result = semantics._time_applicability(window_node(start, end), time_node(requested), job)
    assert result.state == "unknown" and result.reason_codes == ("time_applicability_unknown",)


@pytest.mark.parametrize("start,end,precision", [
    ("2026-09-20", "2026-09-18", "date"),
    ("2026-09-20T00:00:00Z", "2026-09-18T00:00:00Z", "instant"),
])
def test_reversed_known_window_remains_admitted_data_with_an_analytical_limitation(clock, start, end, precision):
    raw = cases.sparse()
    raw["inquiries"][0]["time_window"] = {"start": known(start, precision), "end": known(end, precision)}
    admitted = _prepare_value(raw)
    assert type(admitted) is _PreparedBundle and admitted.input_state == "accepted"
    assert tuple(item.kind for item in admitted.observations) == ("known_window_reversed",)
    owner, job = accepted_job()
    request = known("2026-09-19", "date") if precision == "date" else known("2026-09-19T00:00:00Z")
    result = semantics._time_applicability(window_node(known(start, precision), known(end, precision)),
                                          time_node(request), job)
    assert result.state == "unmet" and result.reason_codes == ("temporal_inconsistency",)
    assert owner.input_state == "accepted"


@pytest.mark.parametrize("lifecycle", ("active", "withdrawn", "superseded"))
def test_current_lifecycle_and_source_creation_dates_do_not_reconstruct_past_effective_time(clock, lifecycle):
    raw, assertion = supported_assertion(lifecycle)
    # Lineage 7 and Definitions 14.2 distinguish assertion creation and bundle
    # assembly from the relation's effective time. Neither is a substitute.
    assertion["asserted_at"] = known("2026-09-19T00:00:00Z")
    raw["recorded_at"] = known("2026-09-20T00:00:00Z")
    requested = time_node(known("2025-06-15T00:00:00Z"))
    context = temporal_context("time_specific", requested)
    admitted = _prepare_value(raw)
    assert type(admitted) is _PreparedBundle
    owner, job = accepted_job()
    result = semantics._qualify_basis(admitted, "temporal-assertion", context, job)
    assert result.state == "unmet" and result.reason_codes == ("time_applicability_unknown",)
    assert result.context is context and owner.input_state == "accepted"
    native = next(item for item in admitted.entities if item.identifier == "temporal-assertion")
    assert dict(native.node.fields.items)["lifecycle_state"] == lifecycle
    # Restoring documentary effective time repairs this one qualification.
    # Even with a later assertion date, PC05 cannot claim historical PC04.
    assertion["scope"]["effective_window"] = {
        "start": known("2025-01-01T00:00:00Z"), "end": known("2026-01-01T00:00:00Z")}
    repaired = _prepare_value(raw)
    assert type(repaired) is _PreparedBundle
    result = semantics._qualify_basis(repaired, "temporal-assertion", context, job)
    assert result.state == "met" and result.reason_codes == ()
    assert not hasattr(result, "eligible_positive_relation") and not hasattr(result, "historical_lifecycle")


def test_snapshot_disclosure_and_time_specific_qualification_keep_separate_questions(clock):
    raw, assertion = supported_assertion()
    assertion["scope"]["effective_window"]["note"] = "Applies to every past and future time."
    admitted = _prepare_value(raw)
    assert type(admitted) is _PreparedBundle and admitted.input_state == "accepted"
    _, job = accepted_job()
    snapshot = semantics._qualify_basis(admitted, "temporal-assertion", temporal_context("snapshot_structural"), job)
    at_time = semantics._qualify_basis(admitted, "temporal-assertion",
                                     temporal_context("time_specific", time_node(known("2026-09-19T00:00:00Z"))), job)
    assert snapshot.state == "met" and snapshot.reason_codes == ()
    assert snapshot.context.temporal_basis == "snapshot_structural" and snapshot.context.requested_time is None
    assert at_time.state == "unmet" and at_time.reason_codes == ("time_applicability_unknown",)
    native = next(item for item in admitted.entities if item.identifier == "temporal-assertion")
    scope = dict(dict(native.node.fields.items)["scope"].items)
    effective = dict(scope["effective_window"].items)
    assert dict(effective["start"].items) == cases.unknown()
    assert dict(effective["end"].items) == cases.unknown()
    assert effective["note"] == "Applies to every past and future time."


@pytest.mark.parametrize("case,start,end,outside", [
    ("inside", "2026-09-18T00:00:00Z", "2026-09-20T00:00:00Z", False),
    ("before", "2026-09-20T00:00:00Z", "2026-09-21T00:00:00Z", True),
    ("after", "2026-09-17T00:00:00Z", "2026-09-18T00:00:00Z", True),
    ("unknown", None, None, False),
    ("unknown_start", None, "2026-09-20T00:00:00Z", False),
    ("unknown_end", "2026-09-18T00:00:00Z", None, False),
    ("reversed", "2026-09-20T00:00:00Z", "2026-09-18T00:00:00Z", False),
    ("start_boundary", "2026-09-19T03:00:00+03:00", "2026-09-20T00:00:00Z", False),
    ("end_boundary", "2026-09-18T00:00:00Z", "2026-09-19T03:00:00+03:00", False),
], ids=("inside", "before", "after", "unknown", "unknown_start", "unknown_end",
        "reversed", "start_boundary", "end_boundary"))
def test_identity_alias_limits_only_its_applicable_time_without_merging_records(clock, case, start, end, outside):
    # Definitions 20.5 and Lineage 7/12.2: aliases are scoped supplied
    # assertions. Definite temporal exclusion is different from unresolved
    # applicability; neither permits canonicalizing the underlying records.
    raw = cases.pool()
    alias = cases.relation("same_identity_as")
    alias["id"] = "time-scoped-alias"
    alias["data"].update(from_ref="origin", to_ref="origin2", details={"identity_level": "origin_event"})
    alias["scope"]["effective_window"] = {
        "start": unknown() if start is None else known(start),
        "end": unknown() if end is None else known(end)}
    raw["assertions"] = [alias]
    admitted = _prepare_value(raw)
    assert type(admitted) is _PreparedBundle and admitted.input_state == "accepted"
    originals = {item.identifier: item for item in admitted.entities}
    owner, job = accepted_job()
    requested = time_node(known("2026-09-19T00:00:00Z"))
    result = semantics._qualify_identity(admitted, ("origin", "origin2"),
                                         temporal_context("time_specific", requested), job)
    assert result.state == ("met" if outside else "unmet"), case
    assert ("identity_unresolved" in result.reason_codes) is (not outside)
    assert ("time-scoped-alias" in {ref.record_id for ref in result.support_refs}) is (not outside)
    if outside:
        assert result.reason_codes == ()
    elif case == "inside":
        assert result.reason_codes == ("identity_unresolved",)
    elif case == "reversed":
        assert set(result.reason_codes) == {"identity_unresolved", "temporal_inconsistency"}
    else:
        assert set(result.reason_codes) == {"identity_unresolved", "time_applicability_unknown"}
    # The same active alias still limits the snapshot question, regardless
    # of where its known effective interval lies relative to requested time.
    snapshot = semantics._qualify_identity(admitted, ("origin", "origin2"),
                                           temporal_context("snapshot_structural"), job)
    assert snapshot.state == "unmet" and "identity_unresolved" in snapshot.reason_codes
    assert "time-scoped-alias" in {ref.record_id for ref in snapshot.support_refs}
    assert {item.identifier: item for item in admitted.entities} == originals
    assert originals["origin"] is not originals["origin2"]
    assert dict(originals["time-scoped-alias"].node.fields.items)["lifecycle_state"] == "active"
    assert not hasattr(result, "canonical_ids") and not hasattr(result, "merged_records")
    assert owner.input_state == "accepted" and job.used > 0


@pytest.mark.parametrize("operation", ("compare", "applicability"))
@pytest.mark.parametrize("state", ("known", "unknown"))
def test_temporal_helpers_stop_prospectively_with_the_actual_job_and_sticky_cause(clock, operation, state):
    owner, job = accepted_job()
    first, second = known("2026-09-18T00:00:00Z"), known("2026-09-20T00:00:00Z")
    if state == "unknown":
        first, second = unknown(), unknown()
    action = (lambda: semantics._compare_times(time_node(first), time_node(second), job)) if operation == "compare" else (
        lambda: semantics._time_applicability(window_node(first, second), time_node(known("2026-09-19T00:00:00Z")), job))
    job.charge(1_000_000)
    before = owner.used, job.used
    with pytest.raises(_AnalysisAborted) as stopped:
        action()
    assert stopped.value.limit_id == "WU9-L11"
    assert stopped.value.stop.input_state == "accepted"
    assert (owner.used, job.used) == before
    for retry in (action, owner.start_job, job.check):
        with pytest.raises(_AnalysisAborted) as repeated:
            retry()
        assert repeated.value is stopped.value


def test_large_legal_fraction_cannot_hide_an_unbounded_scan_in_one_unit(clock):
    owner, job = accepted_job()
    # WU9-L10 permits at most 65,536 UTF-8 bytes per string. Architecture
    # 19.2 requires more than 200 inspected blocks even for one prefix pass.
    prefix = "2026-09-19T00:00:00." + "0" * 65_000
    assert len((prefix + "1Z").encode("utf-8")) <= 65_536
    left, right = time_node(known(prefix + "1Z")), time_node(known(prefix + "2Z"))
    job.charge(999_800)
    with pytest.raises(_AnalysisAborted) as stopped:
        semantics._compare_times(left, right, job)
    assert stopped.value.limit_id == "WU9-L11"
    assert stopped.value.stop.input_state == "accepted"
    assert 999_800 < job.used <= 1_000_000 and owner.used == 1025 + job.used


def test_temporal_deadline_has_one_origin_and_retries_do_not_resample_after_stop(clock, monkeypatch):
    owner, job = accepted_job()
    nodes = time_node(known("2026-09-18T00:00:00Z")), time_node(known("2026-09-20T00:00:00Z"))
    clock[0] += 60_000_000_000
    assert semantics._compare_times(*nodes, job).comparison == "before"
    clock[0] += 1
    before = owner.used, job.used
    with pytest.raises(_AnalysisAborted) as stopped:
        semantics._compare_times(*nodes, job)
    assert stopped.value.limit_id == "WU9-L12"
    sampled = []
    monkeypatch.setattr(resources, "monotonic_ns", lambda: sampled.append(True) or 0)
    with pytest.raises(_AnalysisAborted) as repeated:
        semantics._compare_times(*nodes, job)
    assert repeated.value is stopped.value and sampled == []
    assert (owner.used, job.used) == before


@pytest.mark.parametrize("bad_clock", (False, 99))
def test_clock_fault_is_execution_failure_not_unknown_time_evidence(clock, bad_clock):
    owner, job = accepted_job()
    clock[0] = bad_clock
    with pytest.raises(_AnalysisAborted) as stopped:
        semantics._compare_times(time_node(unknown()), time_node(unknown()), job)
    assert stopped.value.stop.reason_code == "execution_failed"
    assert stopped.value.stop.input_state == "accepted"
    assert owner.used == 1025 and job.used == 0


def test_temporal_cancellation_does_not_become_a_qualification_reason(clock, monkeypatch):
    owner, job = accepted_job()
    def interrupted_clock():
        raise KeyboardInterrupt("Fictional private time payload")
    monkeypatch.setattr(resources, "monotonic_ns", interrupted_clock)
    with pytest.raises(_AuditCancelled) as stopped:
        semantics._compare_times(time_node(unknown()), time_node(unknown()), job)
    assert stopped.value.input_state == "accepted" and owner.input_state == "accepted"
    assert "Fictional private time payload" not in repr(stopped.value)
    assert "Fictional private time payload" not in str(stopped.value)
    assert not hasattr(stopped.value, "reason_codes")


@pytest.mark.parametrize("port_kind", ("preparation", "admission", "active_owner", "finalization"))
@pytest.mark.parametrize("operation", ("compare", "applicability"))
def test_temporal_components_cannot_use_a_nonjob_port_or_promote_input_state(clock, port_kind, operation):
    if port_kind == "preparation":
        owner = port = resources._new_budget()
    elif port_kind == "admission":
        owner = port = resources._new_analysis_budget()
    else:
        owner, job = accepted_job()
        if port_kind == "active_owner":
            port = owner
        else:
            owner.finish_job(job)
            port = owner.begin_finalization()
    before = owner.used, owner.input_state
    with pytest.raises(TypeError, match="^analysis_job_port_required$"):
        if operation == "compare":
            semantics._compare_times(time_node(unknown()), time_node(unknown()), port)
        else:
            semantics._time_applicability(window_node(unknown(), unknown()), time_node(unknown()), port)
    assert (owner.used, owner.input_state) == before


def test_finished_job_cannot_evaluate_under_a_new_jobs_authority(clock):
    owner, first = accepted_job()
    owner.finish_job(first)
    second = owner.start_job()
    before = owner.used, second.used
    with pytest.raises(_AnalysisAborted) as stopped:
        semantics._compare_times(time_node(unknown()), time_node(unknown()), first)
    assert stopped.value.stop.reason_code == "execution_failed"
    assert (owner.used, second.used) == before
    with pytest.raises(_AnalysisAborted) as repeated:
        semantics._compare_times(time_node(unknown()), time_node(unknown()), second)
    assert repeated.value is stopped.value
