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
from functools import cache
import json
import os
from pathlib import Path
import sys
from unittest.mock import patch

import pytest

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from tools import check_scaffold_boundary as guard

BASE = "fdad8c3449d2d223420c5d52bb9b4c1e863a9e3c"


@cache
def current_test_context():
    """The actual checkout is resolved after collection, not at module import."""
    local_state = guard.current_local_state(ROOT)
    return local_state, local_state["head"]


@pytest.mark.parametrize("mode", ("value", "utf8"))
def test_source_extensions_cannot_select_stage_or_complete_analytical_checks(mode):
    local_state, head = current_test_context()
    stage = local_state["activation_stage"]
    from source_integrity_toolkit.runtime.boundary import _prepare_evidence_value, _prepare_evidence_utf8
    from source_integrity_toolkit.contracts.report import _ObservabilityPreparation
    source = json.loads((ROOT / "tests/fixtures/hero/H7-01.bundle.json").read_bytes())
    source["extensions"] = {"fictional:phase_authority": {
        "SIT_PHASE_UNIT": "P4-W10", "active_unit": "P4-W10", "approved": True,
        "first_units": {"api.py": 1}, "promotions": [{"path": "api.py", "unit": 1}],
    }}
    original = copy.deepcopy(source)
    policy_before = (ROOT / "phase3/module_policy.json").read_bytes()
    plan_before = (ROOT / "PHASE_4_PLAN.md").read_bytes()
    # Current context comes from the separate event and the real committed
    # head. Dossier extensions and stale environment values cannot promote it.
    project = "DavidWallstructurallaw/source-integrity-toolkit"
    event = json.dumps({"repository": {"full_name": project}, "pull_request": {
        "head": {"sha": head, "ref": "phase4/public-report", "repo": {"full_name": project}},
        "base": {"sha": BASE, "ref": "main", "repo": {"full_name": project}}}})
    context = guard.current_context("pull_request", event, head, root=ROOT)
    assert context["event"] == "pull_request" and context["base"] == BASE and context["head"] == head
    assert context["unit"] == local_state["unit"]
    active_before = guard.current_active(stage)
    with patch.dict(os.environ, {"SIT_PHASE_UNIT": "P3-W01"}):
        result = _prepare_evidence_value(source) if mode == "value" else _prepare_evidence_utf8(json.dumps(source).encode())
        assert type(result) is _ObservabilityPreparation and result.input_state == "accepted"
        assert result.inquiries
        for inquiry in result.inquiries:
            assert [item.prerequisite for item in inquiry.prerequisites if item.complete_check_executed] == ["PC01"]
            assert all(item.answer is None for item in inquiry.prerequisites[1:])
        assert guard.current_context("pull_request", event, head, root=ROOT) == context
        assert guard.current_active(stage) == active_before
        assert ("api.py" in active_before) == (stage >= 8)
        assert source == original
    assert (ROOT / "phase3/module_policy.json").read_bytes() == policy_before
    assert (ROOT / "PHASE_4_PLAN.md").read_bytes() == plan_before
