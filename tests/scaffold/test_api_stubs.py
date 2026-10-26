# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Public in-memory activation and the retained immediate file refusal."""

import ast
import builtins
import inspect
import json
import os
from pathlib import Path

import pytest

from source_integrity_toolkit import AuditReport, AuditUsageError, audit_bundle, audit_file

MESSAGE = "Source Integrity Toolkit audit is not implemented in the Phase 1 scaffold."


class Hostile:
    def touched(self, *args, **kwargs):
        raise AssertionError("Argument behavior executed")

    __repr__ = __str__ = __iter__ = __len__ = __bool__ = touched
    __getitem__ = __getattr__ = __fspath__ = __eq__ = __hash__ = touched
    keys = items = values = read = write = touched


@pytest.mark.parametrize("function", [audit_file])
def test_first_executable_statement_is_refusal(function):
    tree = ast.parse(inspect.getsource(function))
    body = tree.body[0].body
    assert isinstance(body[0], ast.Expr)  # The public docstring.
    assert len(body) == 2
    assert isinstance(body[1], ast.Raise)


@pytest.mark.parametrize("function", [audit_bundle, audit_file])
def test_hostile_arguments_and_options_remain_untouched(function, monkeypatch):
    obj = Hostile()
    args = (obj,) if function is audit_bundle else (obj, obj)
    with monkeypatch.context() as patch:
        patch.setattr(builtins, "open", obj.touched)
        patch.setattr(os, "open", obj.touched)
        failure = AuditUsageError if function is audit_bundle else NotImplementedError
        with pytest.raises(failure) as caught:
            function(*args, options=obj)
    assert str(caught.value) == ("Invalid audit invocation." if function is audit_bundle else MESSAGE)


def test_plain_bundle_remains_unchanged():
    bundle = {"opaque": [1, None, {"text": "fictional"}]}
    nested = bundle["opaque"]
    report = audit_bundle(bundle)
    assert type(report) is AuditReport
    assert report.report_kind == "validation_diagnostics"
    assert report.input_validation["state"] == "rejected"
    document = json.loads(report.to_json_bytes())
    assert document["report_kind"] == "validation_diagnostics"
    assert document["input_validation"]["state"] == "rejected"
    assert b'"state": "rejected"' in report.to_markdown_bytes()
    assert bundle == {"opaque": [1, None, {"text": "fictional"}]}
    assert bundle["opaque"] is nested


def test_file_stub_neither_reads_nor_creates(tmp_path):
    source = tmp_path / "fictional-input.json"
    output = tmp_path / "must-not-exist"
    original = b'{"canary": "SYNTHETIC_ONLY"}\n'
    source.write_bytes(original)
    with pytest.raises(NotImplementedError) as caught:
        audit_file(source, output, options={"raw_file_digest": True})
    assert str(caught.value) == MESSAGE
    assert source.read_bytes() == original
    assert not output.exists()
    assert set(tmp_path.iterdir()) == {source}


def test_reserved_signatures():
    assert list(inspect.signature(audit_bundle).parameters) == ["bundle", "options"]
    assert list(inspect.signature(audit_file).parameters) == ["input_path", "output_directory", "options"]
    for function in (audit_bundle, audit_file):
        option = inspect.signature(function).parameters["options"]
        assert option.kind is inspect.Parameter.KEYWORD_ONLY
        assert option.default is None
