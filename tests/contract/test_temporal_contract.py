# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Explicit calendar/offset syntax and preserved source temporal uncertainty."""
import importlib.util
import json
from pathlib import Path
import pytest
from source_integrity_toolkit.runtime.boundary import _prepare_value, _prepare_utf8
from source_integrity_toolkit.contracts.evidence import _PreparedBundle

_spec = importlib.util.spec_from_file_location("sit_w05_time_cases", Path(__file__).with_name("test_typed_records.py"))
case = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(case)


def known(text, precision="instant"):
    return {"state": "known", "value": text, "precision": precision}


@pytest.mark.parametrize("text,precision", [("0001-01-01", "date"), ("9999-12-31", "date"), ("2000-02-29", "date"),
    ("2024-02-29", "date"), ("2026-09-19", "date"), ("2026-09-19T00:00:00Z", "instant"),
    ("2026-09-19T23:59:59+14:00", "instant"), ("2026-09-19T00:00:00-07:00", "instant"),
    ("2026-09-19T00:00:00.000000000000000001Z", "instant"), ("2026-09-19T00:00:00.50+00:00", "instant")])
@pytest.mark.parametrize("mode", ["value", "bytes"])
def test_known_time_preserves_exact_text_and_precision(text, precision, mode):
    b = case.sparse(); b["recorded_at"] = known(text, precision)
    result = _prepare_value(b) if mode == "value" else _prepare_utf8(json.dumps(b).encode())
    assert isinstance(result, _PreparedBundle)
    raw = dict(dict(result.tree.items)["recorded_at"].items)
    assert raw == b["recorded_at"]


@pytest.mark.parametrize("text,precision", [("0000-01-01", "date"), ("2026-00-01", "date"), ("2026-13-01", "date"),
    ("2026-02-29", "date"), ("1900-02-29", "date"), ("2026-04-31", "date"), ("2026-01-00", "date"),
    ("20260919", "date"), ("2026-9-19", "date"), ("２０２６-09-19", "date"), ("2026-09-19Z", "date"),
    ("2026-09-19T00:00:00Z", "date"), ("2026-09-19", "instant"), ("2026-09-19T00:00:00", "instant"),
    ("2026-09-19T24:00:00Z", "instant"), ("2026-09-19T12:60:00Z", "instant"), ("2026-09-19T12:00:99Z", "instant"),
    ("2026-09-19T12:00Z", "instant"), ("2026-09-19T12:00:00.Z", "instant"), ("2026-09-19T12:00:00+24:00", "instant"),
    ("2026-09-19T12:00:00+00:60", "instant"), ("2026-09-19T12:00:00+0700", "instant"), ("2026-09-19T12:00:00Ztail", "instant"),
    ("2026-09-19T12:00:00.1e-4Z", "instant")])
def test_malformed_known_time_is_a_structural_diagnostic(text, precision):
    b = case.sparse(); b["recorded_at"] = known(text, precision)
    case.check_rejected(b, "invalid_time")


@pytest.mark.parametrize("state", ["unknown", "withheld", "not_applicable"])
def test_unknown_time_is_preserved_and_never_uses_host_timezone(state, monkeypatch):
    monkeypatch.setenv("TZ", "Pacific/Kiritimati")
    b = case.sparse(); b["recorded_at"]["state"] = state
    result = _prepare_value(b)
    assert isinstance(result, _PreparedBundle)
    assert dict(dict(result.tree.items)["recorded_at"].items) == b["recorded_at"]
    b["recorded_at"]["value"] = "2026-09-19"; case.check_rejected(b, "invalid_time")


@pytest.mark.parametrize("missing", ["reason", "value", "precision", "state"])
def test_time_state_branch_does_not_invent_missing_fields(missing):
    b = case.sparse(); del b["recorded_at"][missing]
    case.check_rejected(b, "missing_required_field")


@pytest.mark.parametrize("start,end,precision", [("2026-09-20", "2026-09-19", "date"),
    ("2026-09-19T00:00:00Z", "2026-09-18T23:59:59Z", "instant"),
    ("2026-09-19T00:00:00.000000000000000002Z", "2026-09-19T00:00:00.000000000000000001Z", "instant")])
def test_inconsistent_known_windows_are_admitted_as_scoped_input_observations(start, end, precision):
    b = case.sparse(); b["inquiries"][0]["time_window"] = {"start": known(start, precision), "end": known(end, precision)}
    result = _prepare_value(b)
    assert isinstance(result, _PreparedBundle) and len(result.observations) == 1
    observation = result.observations[0]
    assert (observation.kind, observation.collection, observation.identifier, observation.selector) == (
        "known_window_reversed", "inquiries", "inquiry", "time_window")


def test_offsets_and_fractional_zero_do_not_create_false_inversion():
    b = case.sparse(); b["inquiries"][0]["time_window"] = {
        "start": known("2026-09-19T03:00:00.50+03:00"), "end": known("2026-09-19T00:00:00.500Z")}
    result = _prepare_value(b)
    assert isinstance(result, _PreparedBundle) and result.observations == ()


def test_mixed_date_instant_boundary_is_not_decided_as_grant_or_causal_eligibility():
    b = case.sparse(); b["inquiries"][0]["time_window"] = {
        "start": known("2026-09-19", "date"), "end": known("2026-09-18T23:59:59Z")}
    result = _prepare_value(b)
    assert isinstance(result, _PreparedBundle) and result.observations == ()
    assert not hasattr(result, "grant_applicable")


def test_long_fraction_is_compared_without_float_rounding_or_exponent_allocation():
    b = case.sparse(); tail = "0" * 2000
    b["inquiries"][0]["time_window"] = {"start": known("2026-09-19T00:00:00." + tail + "2Z"),
                                         "end": known("2026-09-19T00:00:00." + tail + "1Z")}
    result = _prepare_value(b)
    assert isinstance(result, _PreparedBundle) and len(result.observations) == 1
