# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Packaging evidence for the explicitly non-operational scaffold.

Direct backend hooks add no build frontend. Artifacts stay in pytest's temporary
directory. A tool-version gate is deliberately independent from compatibility
checks: running with older preinstalled tools must not satisfy that gate.
"""

from email.parser import BytesParser
import importlib.metadata as metadata
import json
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import sys
import tarfile
import tomllib
import zipfile

import pytest

ROOT = Path(__file__).resolve().parents[2]
PACKAGE = "source_integrity_toolkit"
VERSION = "0.1.0.dev0"
SELECTED = {"setuptools": "84.0.0", "pytest": "9.1.1"}
CANARY = "SYNTHETIC_" + "EXCLUSION_" + "CANARY"


def command(args, *, cwd, env=None):
    proc = subprocess.run(args, cwd=cwd, env=env, capture_output=True, text=True, timeout=90)
    assert proc.returncode == 0, proc.stdout + proc.stderr
    return proc


def test_declared_toolchain_is_actually_available():
    actual = {name: metadata.version(name) for name in SELECTED}
    assert actual == SELECTED, f"Selected toolchain not installed: {actual}; required {SELECTED}"


def test_project_metadata_and_runtime_dependency_boundary():
    config = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))
    project = config["project"]
    assert project["name"] == "source-integrity-toolkit"
    assert project["version"] == VERSION
    assert project["requires-python"] == ">=3.11"
    assert project["dependencies"] == []
    assert project["license"] == "Apache-2.0"
    assert project["license-files"] == ["LICENSE", "NOTICE"]
    assert project["scripts"] == {"sit": PACKAGE + ".cli:main"}
    assert "optional-dependencies" not in project
    assert config["build-system"] == {"requires": ["setuptools==84.0.0"], "build-backend": "setuptools.build_meta"}
    assert config["tool"]["setuptools"]["include-package-data"] is False
    assert len(config["tool"]["setuptools"]["packages"]) == 8


@pytest.fixture(scope="module")
def distributions(tmp_path_factory):
    work = tmp_path_factory.mktemp("scaffold-build")
    for name in ("README.md", "LICENSE", "NOTICE", "pyproject.toml", "MANIFEST.in", "requirements-dev.txt"):
        shutil.copyfile(ROOT / name, work / name)
    shutil.copytree(ROOT / "src", work / "src", ignore=shutil.ignore_patterns("*.egg-info", "__pycache__"))
    shutil.copytree(ROOT / "tests" / "scaffold", work / "tests" / "scaffold", ignore=shutil.ignore_patterns("__pycache__"))
    # Fictional canaries test package selection without copying private data.
    for name in ("theory.pdf", ".env", "private/evidence.json", "report.json", "report.md", "src/source_integrity_toolkit/secret.json"):
        path = work / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(CANARY, encoding="utf-8")
    artifact_dir = work / "dist"
    artifact_dir.mkdir()
    env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTEST_DISABLE_PLUGIN_AUTOLOAD": "1"}
    # These hooks do not resolve build-system.requires. The separate version test
    # must pass before this run can count as selected-toolchain acceptance.
    script = "from setuptools.build_meta import build_sdist, build_wheel; build_sdist('dist'); build_wheel('dist')"
    proc = command([sys.executable, "-c", script], cwd=work, env=env)
    (work / "backend.log").write_text(proc.stdout + proc.stderr, encoding="utf-8")
    return work, next(artifact_dir.glob("*.tar.gz")), next(artifact_dir.glob("*.whl"))


def test_source_distribution_inventory(distributions):
    work, sdist, _ = distributions
    intended = {line.split(" ", 1)[1] for line in (work / "MANIFEST.in").read_text().splitlines() if line.startswith("include ")}
    with tarfile.open(sdist) as archive:
        members = [m for m in archive.getmembers() if m.isfile()]
        prefix = "source_integrity_toolkit-" + VERSION + "/"
        assert all(m.name.startswith(prefix) and not m.issym() and not m.islnk() for m in members)
        relative = {m.name[len(prefix):] for m in members}
        # Setuptools emits this tag-normalization metadata into the sdist.
        # Admit only its fixed, inspected content, never an arbitrary setup.cfg.
        assert relative == intended | {"PKG-INFO", "setup.cfg"}
        assert archive.extractfile(prefix + "setup.cfg").read() == b"[egg_info]\ntag_build = \ntag_date = 0\n\n"
        for member in members:
            assert ".." not in PurePosixPath(member.name).parts
            assert CANARY.encode() not in archive.extractfile(member).read()
        for name in ("README.md", "LICENSE", "NOTICE"):
            assert archive.extractfile(prefix + name).read() == (ROOT / name).read_bytes()


def test_wheel_inventory_and_metadata(distributions):
    _, _, wheel = distributions
    expected_source = {p.relative_to(ROOT / "src").as_posix() for p in (ROOT / "src" / PACKAGE).rglob("*.py")}
    info = PACKAGE + "-" + VERSION + ".dist-info/"
    expected_info = {info + name for name in ("METADATA", "WHEEL", "entry_points.txt", "top_level.txt", "RECORD", "licenses/LICENSE", "licenses/NOTICE")}
    with zipfile.ZipFile(wheel) as archive:
        assert set(archive.namelist()) == expected_source | expected_info
        for name in expected_source:
            assert archive.read(name) == (ROOT / "src" / name).read_bytes()
        meta = BytesParser().parsebytes(archive.read(info + "METADATA"))
        assert meta["Name"] == "source-integrity-toolkit"
        assert meta["Version"] == VERSION
        assert meta["Requires-Python"] == ">=3.11"
        assert meta["License-Expression"] == "Apache-2.0"
        assert meta.get_all("Requires-Dist", []) == []
        assert set(meta.get_all("License-File")) == {"LICENSE", "NOTICE"}
        assert archive.read(info + "licenses/LICENSE") == (ROOT / "LICENSE").read_bytes()
        assert archive.read(info + "licenses/NOTICE") == (ROOT / "NOTICE").read_bytes()


def test_wheel_installs_without_developer_tools(distributions, tmp_path):
    _, _, wheel = distributions
    target = tmp_path / "runtime"
    command([sys.executable, "-m", "venv", "--without-pip", str(target)], cwd=tmp_path)
    python = target / ("Scripts/python.exe" if os.name == "nt" else "bin/python")
    # Existing pip installs the self-built wheel into a clean, offline target.
    command([sys.executable, "-m", "pip", "--python", str(python), "--isolated", "install",
             "--no-index", "--no-deps", "--no-cache-dir", str(wheel)], cwd=tmp_path)
    script = """import importlib.metadata as m
import source_integrity_toolkit as s
assert s.__version__ == '0.1.0.dev0'
assert {d.metadata['Name'] for d in m.distributions()} == {'source-integrity-toolkit'}
for call, args in ((s.audit_bundle, (object(),)), (s.audit_file, (object(), object()))):
    try:
        call(*args, options=object())
    except NotImplementedError:
        pass
    else:
        raise AssertionError('Stub returned a value')
print('CLEAN_RUNTIME_OK')
"""
    result = command([str(python), "-I", "-B", "-c", script], cwd=tmp_path)
    assert result.stdout == "CLEAN_RUNTIME_OK\n"
    sit = target / ("Scripts/sit.exe" if os.name == "nt" else "bin/sit")
    result = command([str(sit), "--version"], cwd=tmp_path)
    assert result.stdout == "source-integrity-toolkit 0.1.0.dev0\n"
    command([str(sit), "--help"], cwd=tmp_path)
    output = tmp_path / "no-report"
    result = subprocess.run([str(sit), "audit", str(tmp_path / "missing.json"), "--output", str(output)],
                            cwd=tmp_path, capture_output=True, text=True, timeout=20)
    assert result.returncode == 1
    assert result.stdout == ""
    assert result.stderr == "Source Integrity Toolkit audit is not implemented in the Phase 1 scaffold.\n"
    assert not output.exists()


def test_source_distribution_rebuilds_same_package(distributions, tmp_path):
    _, sdist, original_wheel = distributions
    # Copy only inspected, regular members of this self-built source archive.
    # This is a developer packaging check, not product archive ingestion.
    with tarfile.open(sdist) as archive:
        for member in archive.getmembers():
            relative = PurePosixPath(member.name)
            assert not relative.is_absolute() and ".." not in relative.parts
            assert not member.issym() and not member.islnk()
            if member.isdir():
                continue
            assert member.isfile()
            target = tmp_path.joinpath(*relative.parts)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(archive.extractfile(member).read())
    source = tmp_path / (PACKAGE + "-" + VERSION)
    (source / "dist").mkdir()
    command([sys.executable, "-c", "from setuptools.build_meta import build_wheel; build_wheel('dist')"], cwd=source)
    rebuilt = next((source / "dist").glob("*.whl"))
    with zipfile.ZipFile(original_wheel) as before, zipfile.ZipFile(rebuilt) as after:
        assert set(before.namelist()) == set(after.namelist())
        for name in before.namelist():
            assert before.read(name) == after.read(name), name
