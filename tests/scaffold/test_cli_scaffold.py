# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""CLI scaffold behavior only, including payload-free refusal."""

import os
from pathlib import Path
import subprocess
import sys

import pytest

ROOT = Path(__file__).resolve().parents[2]
MESSAGE = "Source Integrity Toolkit audit is not implemented in the Phase 1 scaffold.\n"


def invoke(args, directory):
    env = {**os.environ, "PYTHONPATH": str(ROOT / "src"), "PYTHONDONTWRITEBYTECODE": "1"}
    return subprocess.run([sys.executable, "-B", "-S", "-m", "source_integrity_toolkit.cli", *args],
                          cwd=directory, env=env, capture_output=True, text=True, timeout=20)


@pytest.mark.parametrize("args", [[], ["--help"], ["-h"], ["audit", "--help"], ["audit", "-h"]])
def test_help(args, tmp_path):
    result = invoke(args, tmp_path)
    assert result.returncode == 0
    assert "not implemented" in result.stdout
    assert "temporary refusal" in result.stdout
    assert result.stderr == ""
    assert not list(tmp_path.iterdir())


def test_version(tmp_path):
    result = invoke(["--version"], tmp_path)
    assert result.returncode == 0
    assert result.stdout == "source-integrity-toolkit 0.1.0.dev0\n"
    assert result.stderr == ""


@pytest.mark.parametrize("extra", [[], ["--raw-file-digest"], ["--force"], ["--help", "SYNTHETIC_SECRET"], ["--output", "second"]])
def test_audit_refuses_without_touching_paths(extra, tmp_path):
    source = tmp_path / "source.json"
    source.write_bytes(b"SYNTHETIC_SECRET\n")
    output = tmp_path / "new-report"
    result = invoke(["audit", str(source), "--output", str(output), *extra], tmp_path)
    assert result.returncode == 1
    assert result.stderr == MESSAGE
    assert result.stdout == ""
    assert source.read_bytes() == b"SYNTHETIC_SECRET\n"
    assert set(tmp_path.iterdir()) == {source}


@pytest.mark.parametrize("args", [["audit"], ["audit", "https://invalid.example/SYNTHETIC_SECRET"],
                                  ["unknown", "SYNTHETIC_SECRET"], ["--version", "SYNTHETIC_SECRET"]])
def test_other_requests_refuse_without_argument_echo(args, tmp_path):
    result = invoke(args, tmp_path)
    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr == MESSAGE
    assert not list(tmp_path.iterdir())
