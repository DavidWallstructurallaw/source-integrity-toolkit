# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W08's public memory surface, with real calls and independent expectations.

The finite dossier is the existing independently authored W07 case. These
checks cover the public interface; field-by-field closure remains W09 work.
"""
from collections.abc import Mapping
from contextlib import contextmanager
import copy
import importlib.util
import inspect
import json
from pathlib import Path
import traceback

import pytest

import source_integrity_toolkit as package
from source_integrity_toolkit import api
from source_integrity_toolkit.contracts import execution, report as contract
from source_integrity_toolkit.runtime import boundary, resources


ROOT = Path(__file__).resolve().parents[2]
EXPORTS = ("audit_bundle", "audit_file", "__version__", "AuditReport",
           "AuditAbort", "AuditCancelled", "AuditUsageError")
ROOT_MEMBERS = (
    "contract_version", "report_kind", "report_id", "run", "input_identity",
    "input_validation", "scopes", "populations", "basis_index", "capabilities",
    "checks", "observability_domains", "results", "findings", "reasons",
    "release_limits",
)


def _case_module():
    spec = importlib.util.spec_from_file_location(
        "sit_w08_api_finite_case", ROOT / "tests/integration/test_public_audit.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _plain(value):
    if isinstance(value, Mapping):
        assert all(type(key) is str for key in value)
        return {key: _plain(item) for key, item in value.items()}
    if type(value) is tuple:
        return [_plain(item) for item in value]
    assert value is None or type(value) in (str, bool, int)
    return value


@pytest.fixture(scope="module")
def option_reports():
    case = _case_module()
    source = case._minimal_value()
    before = copy.deepcopy(source)
    results = []
    for options in (None, {}, {"raw_file_digest": False}):
        options_before = copy.deepcopy(options)
        result = package.audit_bundle(source, options=options)
        assert type(result) is package.AuditReport
        assert result.report_kind == "audit_report"
        assert result.run["processing_state"] == "completed"
        assert result.input_validation["state"] == "accepted"
        assert source == before and options == options_before
        # Independent JSON spelling, Markdown parser, and the report schema
        # check the actual result rather than a product-generated snapshot.
        case._assert_complete_formats(result)
        results.append(result)
    return tuple(results)


def test_public_exports_have_exact_order_identity_and_unchanged_development_version():
    assert package.__all__ == EXPORTS
    assert package.audit_bundle is api.audit_bundle
    assert package.audit_file is api.audit_file
    assert package.AuditReport is contract.AuditReport
    for name in ("AuditAbort", "AuditCancelled", "AuditUsageError"):
        assert getattr(package, name) is getattr(execution, name)
    assert package.__version__ == "0.1.0.dev0"
    names = {}
    exec("from source_integrity_toolkit import *", names)
    assert set(names) - {"__builtins__"} == set(EXPORTS)
    assert all(names[name] is getattr(package, name) for name in EXPORTS)


def test_public_signatures_and_cached_methods_have_no_runtime_controls():
    signature = inspect.signature(package.audit_bundle)
    assert tuple(signature.parameters) == ("bundle", "options")
    assert signature.parameters["bundle"].kind is inspect.Parameter.POSITIONAL_OR_KEYWORD
    assert signature.parameters["bundle"].default is inspect.Parameter.empty
    assert signature.parameters["options"].kind is inspect.Parameter.KEYWORD_ONLY
    assert signature.parameters["options"].default is None
    assert signature.return_annotation is package.AuditReport
    file_signature = inspect.signature(package.audit_file)
    assert tuple(file_signature.parameters) == ("input_path", "output_directory", "options")
    assert file_signature.parameters["options"].kind is inspect.Parameter.KEYWORD_ONLY
    assert file_signature.parameters["options"].default is None
    for name in ("to_json_bytes", "to_markdown_bytes"):
        assert tuple(inspect.signature(getattr(package.AuditReport, name)).parameters) == ("self",)


def test_none_empty_and_false_options_deliver_identical_complete_public_bytes(option_reports):
    first = option_reports[0]
    for report in option_reports:
        assert report.to_json_bytes() == first.to_json_bytes()
        assert report.to_markdown_bytes() == first.to_markdown_bytes()
        assert report.input_identity["source_mode"] == "in_process"
        assert report.input_identity["raw_file_digest"] is None
        assert report.input_identity["qualifications"]


def test_public_report_exposes_exact_logical_roots_and_private_cache_is_not_schema(option_reports):
    report = option_reports[0]
    document = json.loads(report.to_json_bytes())
    assert set(document) == set(ROOT_MEMBERS)
    assert document == {name: _plain(getattr(report, name)) for name in ROOT_MEMBERS}
    assert document["report_id"] == "SIT-RPT-000001"
    assert document["contract_version"] == "sit-report/0.1"
    assert len(report.capabilities) == 15 and len(report.observability_domains) == 5
    assert not hasattr(report, "__dict__")
    assert set(package.AuditReport.__slots__) == {"_document", "_json_bytes", "_markdown_bytes"}
    with pytest.raises(TypeError):
        json.dumps(report)


def test_public_roots_nested_mappings_and_arrays_are_read_only(option_reports):
    report = option_reports[0]
    before_json, before_markdown = report.to_json_bytes(), report.to_markdown_bytes()
    for name in ROOT_MEMBERS:
        with pytest.raises((AttributeError, TypeError)):
            setattr(report, name, None)
        with pytest.raises((AttributeError, TypeError)):
            delattr(report, name)
    with pytest.raises(TypeError):
        report.run["processing_state"] = "failed"
    with pytest.raises(TypeError):
        report.results[0]["value"] = "PRIVATE-MUTATION"
    with pytest.raises(TypeError):
        report.run["requested_diagnostic_ids"][0] = "PRIVATE-MUTATION"
    with pytest.raises((AttributeError, TypeError)):
        report.results += ()
    assert report.to_json_bytes() is before_json
    assert report.to_markdown_bytes() is before_markdown


def test_public_cached_methods_never_restart_runtime_renderers_or_clocks(option_reports, monkeypatch):
    report = option_reports[0]
    json_raw, markdown_raw = report.to_json_bytes(), report.to_markdown_bytes()
    from source_integrity_toolkit.reporting import json_report, markdown_report

    def forbidden(*args, **kwargs):
        raise AssertionError("cached public method started new work")

    monkeypatch.setattr(api, "_audit_value", forbidden)
    monkeypatch.setattr(boundary, "_audit_value", forbidden)
    monkeypatch.setattr(boundary, "_new_analysis_budget", forbidden)
    monkeypatch.setattr(resources, "monotonic_ns", forbidden)
    monkeypatch.setattr(json_report, "_encode_json_report", forbidden)
    monkeypatch.setattr(markdown_report, "_encode_markdown_report", forbidden)
    for unused in range(3):
        assert type(report.to_json_bytes()) is bytes
        assert type(report.to_markdown_bytes()) is bytes
        assert report.to_json_bytes() is json_raw
        assert report.to_markdown_bytes() is markdown_raw


@pytest.mark.parametrize("options", (
    True, False, 0, 1, "", "raw_file_digest", [], (),
    {"raw_file_digest": True}, {"raw_file_digest": 0}, {"raw_file_digest": 1},
    {"raw_file_digest": None}, {"raw_file_digest": "false"},
    {"raw_file_digest": []}, {"unknown": False}, {0: False},
    {"clock": None}, {"budget": 10_000_000}, {"profile": "default"},
    {"diagnostic_ids": []}, {"raw_file_digest": False, "extra": None},
))
def test_invalid_options_are_safe_usage_errors_before_an_invocation(options, monkeypatch, capsys):
    entered = []

    def forbidden(*args, **kwargs):
        entered.append(True)
        raise AssertionError("invalid options entered runtime")

    monkeypatch.setattr(api, "_audit_value", forbidden)
    monkeypatch.setattr(boundary, "_new_analysis_budget", forbidden)
    with pytest.raises(package.AuditUsageError) as captured:
        package.audit_bundle(object(), options=options)
    error = captured.value
    assert type(error) is package.AuditUsageError and isinstance(error, ValueError)
    assert error.code == "invalid_invocation"
    assert str(error) == error.safe_message == "Invalid audit invocation."
    assert repr(error) == "AuditUsageError()"
    assert error.args == ("Invalid audit invocation.",)
    assert error.__cause__ is None and error.__suppress_context__
    assert entered == [] and capsys.readouterr() == ("", "")


@pytest.mark.parametrize("kind", ("usage", "abort", "cancel"))
def test_exported_safe_failures_preserve_identity_through_python_context_managers(kind):
    if kind == "usage":
        error = package.AuditUsageError()
        message, representation = "Invalid audit invocation.", "AuditUsageError()"
    elif kind == "abort":
        error = package.AuditAbort("failed", "not_completed", "execution_failed")
        message, representation = "Audit could not be completed.", "AuditAbort()"
    else:
        error = package.AuditCancelled("accepted")
        message, representation = "Audit cancelled.", "AuditCancelled()"

    @contextmanager
    def passthrough():
        yield

    with pytest.raises(type(error)) as captured:
        with passthrough():
            raise error
    assert captured.value is error
    assert str(error) == error.safe_message == message
    assert error.args == (message,) and repr(error) == representation
    assert message in "".join(traceback.format_exception(error))
    for name in ("args", "safe_message", "code", "arbitrary_payload"):
        with pytest.raises(AttributeError):
            setattr(error, name, "PRIVATE-PAYLOAD")
        with pytest.raises(AttributeError):
            delattr(error, name)
    if kind != "usage":
        assert error.publication_state == "not_published"
    if kind == "cancel":
        assert not hasattr(error, "reason_code")


def test_public_direct_report_construction_cannot_fabricate_an_audit():
    with pytest.raises(TypeError, match=r"^AuditReport is delivered only by audit_bundle\.$"):
        package.AuditReport()
