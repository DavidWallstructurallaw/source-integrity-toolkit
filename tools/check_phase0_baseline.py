# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Repository-only exact-byte guard, PHASE_1_PLAN.md section 9.

Never import this tool from the installed package. The independently pinned W01
manifest is the trust anchor; editing a file and its manifest together cannot
make a changed freeze pass. No dossier or external source is processed here.
This is a developer-workspace check, not the future hostile-filesystem adapter.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import stat
from pathlib import Path, PurePosixPath

MANIFEST_PATH = "scaffold/baseline_manifest.json"
MANIFEST_BLOB = "da48da62c4d1dd8e27af43daa0ecdc8e6c4698d8"
APPROVED_COMMIT = "7d2e5fcaff591641b5cefce00e71e88941dd1f95"
BASELINE_NAMES = frozenset((
    "CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md", "DEFINITIONS_AND_UNITS.md",
    "DEPENDENCY_STRATEGY.md", "GOVERNANCE_AND_HANDOFF.md", "LICENSING_NOTES.md",
    "OBSERVABILITY_AND_REPORTING.md", "PHASE_0_PLAN.md",
    "PRIVACY_AND_DATA_HANDLING.md", "PROJECT_INSTRUCTIONS.md",
    "REPOSITORY_ARCHITECTURE.md", "SOURCE_INTEGRITY_THREAT_MODEL.md",
    "SPEC_AUDIT.md", "SUCCESS_CRITERIA.md", "THEORY_SOURCE_MAP.md",
    "THEORY_TO_CODE_TRACEABILITY.md", "UNRESOLVED_DECISIONS.md",
    "V0.1_PRODUCT_SPEC.md", "VALIDATION_PLAN.md",
))


def git_blob(data: bytes) -> str:
    """Git object identity, kept distinct from file SHA-256."""
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def unique_object(pairs: list[tuple[str, object]]) -> dict:
    result: dict = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate_key")
        result[key] = value
    return result


def read_regular(root: Path, relative: str, maximum: int) -> bytes:
    """Bounded read of a regular repository file without following visible links.

    A trusted, quiescent checkout is a precondition. This function is not an
    implementation or certification of the native file protocol in Phase 0.
    """
    parts = PurePosixPath(relative).parts
    if (not parts or PurePosixPath(relative).is_absolute() or
            ".." in parts or "\\" in relative or ":" in relative):
        raise ValueError("unsafe_repository_path")
    current = root
    for part in parts:
        current = current / part
        if current.is_symlink():
            raise ValueError("repository_symlink")
    if not stat.S_ISREG(current.lstat().st_mode):
        raise ValueError("not_regular_file")
    with current.open("rb") as handle:
        data = handle.read(maximum + 1)
    if len(data) > maximum:
        raise ValueError("byte_limit")
    return data


def check_entry(root: Path, row: dict) -> list[str]:
    """Reusable byte comparison; tests use independently made synthetic rows."""
    path = row["path"]
    try:
        if type(row["bytes"]) is not int or row["bytes"] < 0:
            return ["invalid_expected_size"]
        data = read_regular(root, path, row["bytes"])
    except (OSError, ValueError):
        return ["missing_unsafe_or_oversize"]
    issues = []
    if len(data) != row["bytes"]:
        issues.append("size_mismatch")
    if git_blob(data) != row["git_blob_sha1"]:
        issues.append("git_blob_mismatch")
    if "sha256" in row and hashlib.sha256(data).hexdigest() != row["sha256"]:
        issues.append("sha256_mismatch")
    return issues


def load_manifest(root: Path) -> dict:
    raw = read_regular(root, MANIFEST_PATH, 32768)
    if git_blob(raw) != MANIFEST_BLOB:
        raise ValueError("manifest_anchor_mismatch")
    manifest = json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object)
    rows = manifest["baseline_files"]
    if (manifest["approved_phase0_commit"] != APPROVED_COMMIT or
            len(rows) != 18 or {r["path"] for r in rows} != BASELINE_NAMES or
            sum(r["bytes"] for r in rows) != 1094920 or
            manifest["approval_record"]["path"] != "PHASE_0_APPROVAL.md" or
            manifest["approved_phase1_plan"]["path"] != "PHASE_1_PLAN.md"):
        raise ValueError("manifest_contract_mismatch")
    return manifest


def check_repository(root: Path) -> dict:
    """Check the actual checkout; no network, rewriting or repair option exists."""
    try:
        manifest = load_manifest(root)
    except (OSError, ValueError, KeyError, TypeError):
        return {"ok": False, "checked_files": 0,
                "issues": [{"path": MANIFEST_PATH, "code": "manifest_invalid"}]}
    rows = manifest["baseline_files"] + [manifest["approval_record"],
                                        manifest["approved_phase1_plan"]]
    issues = [{"path": row["path"], "code": code}
              for row in rows for code in check_entry(root, row)]
    return {"ok": not issues, "checked_files": len(rows), "issues": issues,
            "scope": "18 frozen specifications, approval and Phase 1 plan; stored bytes"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args(argv)
    result = check_repository(args.root)
    print(json.dumps(result, sort_keys=True))
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
