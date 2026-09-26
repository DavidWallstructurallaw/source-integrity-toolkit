# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W14 intact hero executions, bounded stops and independently frozen inventory.

The original logical oracles assume completion of each required operation. A
whole-invocation stop cannot certify their later fields. A test-only observer
checks actual completed atomic inventory before any stop; it never supplies
answers, changes limits, resumes a job or returns those cells to a caller.
"""
import copy
import hashlib
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
HEROES = ('H7-01', 'H7-V01', 'H7-V02', 'H7-V03')


def _hero_expectation(case):
    oracle = json.loads((ROOT / 'tests/golden' / (case + '.logical.json')).read_bytes())
    fields = {name.split('.', 1)[1]: value for name, value in
              oracle['selected_field_expectations'].items() if name.startswith('SIT-M001.')}
    artifacts = oracle['populations']['source_artifacts']
    seeds = oracle['populations']['source_contributions']
    members = {
        'nominal_seed_artifact_record_count': artifacts,
        'unresolved_seed_artifact_reference_count': [],
        'seed_evidence_item_count': seeds,
        'claim_artifact_record_count': artifacts,
        'claim_unassigned_seed_artifact_record_count': [],
    }
    return {'case': case, 'fields': fields, 'members': members,
            'inquiry': 'H7-I1', 'claim': 'H7-C1'}


def _hero_analysis(raw, expected, mode):
    """Shared test harness also transmitted as test code to the clean runtime.

    Record the first rejected *actual* charge and prove its fixed inequality.
    Ordinary charge/commit methods execute unchanged. Real monotonic time stays
    enabled, including honest deadline interruption on a slow machine.
    """
    from source_integrity_toolkit.runtime import boundary, resources
    from source_integrity_toolkit.runtime.diagnostics import _AnalyticalDiagnostic
    from source_integrity_toolkit.contracts.execution import _AnalysisAborted
    from source_integrity_toolkit.contracts.report import _AnalyticalOutcome
    source = json.loads(raw)
    before = copy.deepcopy(source)
    budgets, committed, rejected, final_rejected = [], [], [], []
    factory, commit, charge = (boundary._new_analysis_budget, boundary._commit_job,
                               resources._AnalysisBudget.charge)
    final_charge = resources._AnalysisBudget._finalization_charge

    def new_budget():
        owner = factory()
        budgets.append(owner)
        return owner

    def observe_commit(port, results, findings, witnesses):
        result = commit(port, results, findings, witnesses)
        committed.extend(results)
        return result

    def observe_charge(owner, units):
        before_used = owner.used
        before_job = None if owner._job is None else owner._job.used
        first = owner._cause is None
        try:
            return charge(owner, units)
        except _AnalysisAborted:
            if first:
                rejected.append({'used_before': before_used, 'job_before': before_job,
                                 'requested': units, 'kind': owner._stop_kind,
                                 'elapsed_ns': owner._last - owner._start})
            raise

    def observe_final_charge(owner, port, units):
        before_used = owner.used
        unblocked = not owner._finalization_blocked
        try:
            return final_charge(owner, port, units)
        except _AnalysisAborted:
            if unblocked:
                final_rejected.append({'used_before': before_used, 'requested': units,
                                       'elapsed_ns': owner._last - owner._start})
            raise

    boundary._new_analysis_budget = new_budget
    boundary._commit_job = observe_commit
    resources._AnalysisBudget.charge = observe_charge
    resources._AnalysisBudget._finalization_charge = observe_final_charge
    try:
        result = (boundary._analyze_value(source) if mode == 'value' else
                  boundary._analyze_utf8(raw))
    finally:
        boundary._new_analysis_budget = factory
        boundary._commit_job = commit
        resources._AnalysisBudget.charge = charge
        resources._AnalysisBudget._finalization_charge = final_charge
    assert source == before
    assert len(budgets) == 1
    owner = budgets[0]
    assert resources._WORK_LIMIT == 10_000_000
    assert resources._JOB_WORK_LIMIT == 1_000_000
    assert resources._DEADLINE_NS == 60_000_000_000
    assert 1024 < owner.used <= 10_000_000
    assert result.input_state == 'accepted'
    assert result.execution_state in ('completed', 'interrupted')
    checked = []
    for row in committed:
        if row.ref.diagnostic_id != 'SIT-M001':
            continue
        field = row.ref.field_key
        oracle = expected['fields'][field]
        assert row.execution_state == oracle['execution_state'] == 'completed'
        assert row.result_state == oracle['result_state'] == 'available'
        assert row.value.value == oracle['value']
        assert [ref.identifier for ref in row.value.population.member_refs] == expected['members'][field]
        assert row.ref.scope.inquiry_ref.identifier == expected['inquiry']
        claims = [ref.identifier for ref in row.ref.scope.claim_refs]
        assert claims == ([expected['claim']] if field in
                          ('seed_evidence_item_count', 'claim_artifact_record_count') else [])
        assert row.basis_refs and row.witness_refs and row.interpretation_limit
        assert {check.check_id: check.state for check in row.check_refs} == {
            'PC01': 'met', 'PC02': 'met', 'PC03': 'met', 'PC24': 'met'}
        assert not row.reason_refs
        checked.append(field)
    if type(result) is _AnalyticalDiagnostic:
        assert result.execution_state == 'interrupted' and result.code == 'resource_limit_reached'
        assert result.qualifications == (owner._cause.limit_id,)
        assert result.location is None
        assert not hasattr(result, 'results') and not hasattr(result, 'prepared')
        assert owner._stop_kind in ('global', 'job', 'time')
        if owner._stop_kind == 'global':
            assert rejected and rejected[0]['kind'] == 'global'
            assert rejected[0]['requested'] > 10_000_000 - rejected[0]['used_before']
            # The fixed work stop happens after the first completed owner.
            assert set(checked) == set(expected['fields'])
        elif owner._stop_kind == 'job':
            assert rejected and rejected[0]['kind'] == 'job'
            assert rejected[0]['requested'] > 1_000_000 - rejected[0]['job_before']
            assert owner._finalization_blocked
            assert (final_rejected and final_rejected[0]['requested'] >
                    10_000_000 - final_rejected[0]['used_before']) or (
                        owner._last - owner._start > 60_000_000_000)
            assert set(checked) == set(expected['fields'])
        else:
            assert owner._last - owner._start > 60_000_000_000
    else:
        assert type(result) is _AnalyticalOutcome
        assert set(checked) == set(expected['fields'])
        for row in result.results:
            if row.execution_state != 'completed':
                assert row.result_state == 'not_evaluated' and row.value is None
            elif row.result_state == 'available':
                assert next(c.state for c in row.check_refs if c.check_id == 'PC24') == 'met'
    return {'case': expected['case'], 'mode': mode, 'input_state': result.input_state,
            'execution_state': result.execution_state, 'delivery_type': type(result).__name__,
            'used': owner.used, 'stop_kind': owner._stop_kind,
            'limit': None if owner._cause is None else owner._cause.limit_id,
            'first_rejected_charge': rejected[:1], 'finalization_rejected_charge': final_rejected[:1],
            'completed_inventory_fields': sorted(checked),
            'delivered_result_count': len(result.results) if type(result) is _AnalyticalOutcome else 0,
            'input_unchanged': source == before}


@pytest.mark.parametrize('case', HEROES)
@pytest.mark.parametrize('mode', ('value', 'utf8'))
def test_original_hero_actual_analysis_preserves_fixed_limits_and_atomic_oracle(case, mode):
    path = ROOT / 'tests/fixtures/hero' / (case + '.bundle.json')
    raw = path.read_bytes()
    before = hashlib.sha256(raw).hexdigest()
    observed = _hero_analysis(raw, _hero_expectation(case), mode)
    assert observed['input_unchanged']
    assert hashlib.sha256(path.read_bytes()).hexdigest() == before
