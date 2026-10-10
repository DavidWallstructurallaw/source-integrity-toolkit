# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Retained source-data boundary from the accepted Phase 3 transition tests.

Stage replay and old-method source comparisons were retired in VC-04. See
verification/consolidation_map.json for per-test dispositions and commit
3ac5128e4744e2d3708400e3cb1875a9cd4ed0e1 for the complete historical originals.
Current authority, effects, history and collection controls live in
test_verification_boundary.py; this file keeps the product-facing witness.
"""
import copy
import json
import os
from pathlib import Path
import sys
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools import check_scaffold_boundary as guard


@pytest.mark.parametrize("mode", ("value", "utf8"))
def test_source_extensions_cannot_select_stage_or_complete_analytical_checks(mode):
    from source_integrity_toolkit.runtime.boundary import _prepare_evidence_value, _prepare_evidence_utf8
    from source_integrity_toolkit.contracts.report import _ObservabilityPreparation
    source = json.loads((ROOT / "tests/fixtures/hero/H7-01.bundle.json").read_bytes())
    source["extensions"] = {"fictional:phase_authority": {
        "SIT_PHASE_UNIT": "P3-W15", "active_unit": "P3-W15", "approved": True,
        "first_units": {"api.py": 1}, "promotions": [{"path": "api.py", "unit": 1}],
    }}
    original = copy.deepcopy(source)
    policy_before = (ROOT / "phase3/module_policy.json").read_bytes()
    # The separately supplied review event selects VC before any dossier is
    # processed. Neither source extensions nor a stale phase environment changes it.
    head, base = "a" * 40, "b" * 40
    project = "DavidWallstructurallaw/source-integrity-toolkit"
    event = json.dumps({"repository": {"full_name": project}, "pull_request": {
        "head": {"sha": head, "ref": "verification/consolidation", "repo": {"full_name": project}},
        "base": {"sha": base, "ref": "main", "repo": {"full_name": project}}}})
    context = {"event": "pull_request", "unit": "VC", "base": base, "head": head}
    assert guard.current_context("pull_request", event, head) == context
    with patch.dict(os.environ, {"SIT_PHASE_UNIT": "P3-W01"}):
        result = _prepare_evidence_value(source) if mode == "value" else _prepare_evidence_utf8(json.dumps(source).encode())
        assert type(result) is _ObservabilityPreparation and result.input_state == "accepted"
        assert result.inquiries
        for inquiry in result.inquiries:
            assert [item.prerequisite for item in inquiry.prerequisites if item.complete_check_executed] == ["PC01"]
            assert all(item.answer is None for item in inquiry.prerequisites[1:])
        assert guard.current_context("pull_request", event, head) == context
        assert "api.py" not in guard.VC_ACTIVE
        assert source == original
    assert (ROOT / "phase3/module_policy.json").read_bytes() == policy_before
