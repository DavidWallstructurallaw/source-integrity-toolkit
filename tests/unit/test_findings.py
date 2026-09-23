# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W12 source oracles for the bounded conditions in Reporting 18.

Literal source cases determine the expected evidentiary form. Original owners
run against an admitted snapshot and one live job; findings cannot turn their
native disclosures into authentication, motive or an unperformed detector.
"""
import copy
from dataclasses import FrozenInstanceError, replace
import importlib.util
from pathlib import Path

import pytest

from source_integrity_toolkit.analysis import findings
from source_integrity_toolkit.analysis import origins, evaluator_lineage, presence
from source_integrity_toolkit.analysis import correction_routes, correction_outcomes
from source_integrity_toolkit.analysis import process_comparison, human_review
from source_integrity_toolkit.analysis import context as context_owner
from source_integrity_toolkit.contracts.execution import _AnalysisAborted
from source_integrity_toolkit.validation.limits import _WitnessLedger


def helper(name):
    spec = importlib.util.spec_from_file_location('sit_w12_' + name,
        Path(__file__).with_name('test_' + name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


h = helper('process_comparison')
e = helper('evaluator_lineage')
r = helper('correction_routes')
o = helper('correction_outcomes')
p = helper('pipeline_cohorts')

CONDITIONS = (
    'shared_origin_witness', 'citation_path_witness', 'transformation_path_witness',
    'model_mediated_derivation_witness', 'view_cycle_witness',
    'assurance_loop_limitation', 'evaluator_overlap_witness', 'family_label_match',
    'provenance_gap', 'verification_scope_limitation', 'independence_record_conflict',
    'correction_dependency_witness', 'correction_route_limitation',
    'case_handling_disclosure', 'linked_change_disclosure',
    'downstream_change_undocumented', 'externality_stage_limitation',
    'recorded_stage_exclusion', 'anomaly_or_contestation_disclosure',
    'attributed_external_observation', 'scoped_no_witness', 'recorded_data_conflict',
)
FORMS = ('positive_witness', 'no_witness_in_examined_view',
         'bounded_absence_under_declared_coverage', 'attributed_observation',
         'qualification_gap', 'recorded_conflict')


def context(source, **changes):
    values = dict(subject_refs=(), dependency_dimension=None, graph_view=None,
                  coverage_kind=None, relation_types=(), operation_anchor=())
    values.update(changes)
    return h.context(source, **values)


def relation(source, predicate, identifier=None, **changes):
    row = h.cases.relation(predicate)
    if identifier:
        row['id'] = identifier
    row['data'].update(changes)
    source['assertions'].append(row)
    return row


def assessment(source, kind, identifier=None):
    subjects, details = copy.deepcopy(h.cases.assessments()[kind])
    row = h.cases.assertion(identifier or 'a-' + kind, 'assessment',
        {'assessment_kind': kind, 'subject_refs': subjects, 'details': details})
    source['assertions'].append(row)
    return row


def graph_query(source, view, start, target, *, predicates=(), dimension=None):
    return (context(source, subject_refs=(start, target), graph_view=view, dependency_dimension=dimension,
                    relation_types=predicates), start, target)


def owner_profile(name, source, prepared, job, ledger, parent=None):
    if name == 'context':
        return context_owner._context_preservation(prepared, context(source), ledger, job)
    if name == 'origins':
        return origins._origin_profile(prepared, e.h.context(source), ledger, job, family='SIT-M002')
    if name == 'evaluator':
        return evaluator_lineage._evaluator_lineage(prepared, e.context(source), ledger, job)
    if name == 'comparison':
        return process_comparison._comparison_profile(prepared, h.context(source), 'H7-IND12', ledger, job)
    if name == 'outcomes':
        return correction_outcomes._correction_outcomes(prepared, o.context(source), ledger, job)
    if name == 'route':
        return correction_routes._correction_routes(prepared,
            r.context(source, start=parent.subject_refs[0] if parent is not None else None,
                target=parent.subject_refs[1] if parent is not None else None,
                requested_time=parent.requested_time if parent is not None else None), ledger, job)
    if name == 'selection':
        ctx = p.context(source, 'selection')
        return presence._presence(prepared, ctx, ledger, job, family='SIT-M010',
            coverage_ref='H7-COV-SEL', stage_anchor=ctx.operation_anchor)
    if name == 'externality':
        return presence._presence(prepared, context(source), ledger, job,
            family='SIT-M009', assessment_ref='H7-EXT-F')
    raise AssertionError('unregistered_test_owner')


def run(source, *, owners=(), queries=(), ctx=None):
    original = copy.deepcopy(source)
    prepared = h.admit(source)
    ctx = context(source) if ctx is None else ctx
    budget, job = h.job_pair()
    profiles = tuple(owner_profile(name, source, prepared, job, budget.witnesses, ctx) for name in owners)
    before = budget.used, job.used
    out = findings._findings(prepared, ctx, budget.witnesses, job,
        stage_profiles=profiles, graph_requests=queries)
    assert source == original
    assert out.prepared is prepared and out.context is ctx and out.job_port is job
    assert budget.used - before[0] == job.used - before[1] > 0
    assert out.release_limits
    for row in out.findings:
        assert row.condition_code in CONDITIONS and row.observation_kind in FORMS
        assert row.scope_ref.inquiry_ref.identifier == ctx.inquiry_ref
        assert row.basis_refs and row.statement and row.interpretation_limit
        assert row.witness.input_refs or row.witness.owner_witnesses
        assert all(pop.scope is row.scope_ref for pop in row.population_refs)
        assert all(reason.scope is row.scope_ref for reason in row.reason_refs)
    return out, profiles, prepared, budget, job


def selected(out, code):
    return tuple(row for row in out.findings if row.condition_code == code)


def forms(out, code):
    return {row.observation_kind for row in selected(out, code)}


def input_ids(row):
    return {ref.identifier for ref in row.witness.input_refs}


def citation_source(*, cycle=False, polarity='affirmed', predicate='cites'):
    source = h.cases.pool()
    relation(source, predicate, polarity=polarity)
    if cycle:
        relation(source, 'cites', 'return-citation', from_ref='artifact2', to_ref='artifact')
    return source


def self_support():
    source = h.hero()
    pointer = copy.deepcopy(h.cases.by_id(source, 'H7-SUP-CHAIN'))
    pointer.update(id='W12-SELF', reference_kind='record_pointer', record_ref='H7-L01',
        artifact_ref=None, excerpt=None, locator=None)
    source['evidence_references'].append(pointer)
    h.cases.by_id(source, 'H7-L01')['provenance']['evidence_ref_ids'] = ['W12-SELF']
    return source


def conflicting_independence():
    source = h.hero()
    other = copy.deepcopy(h.cases.by_id(source, 'H7-IND12'))
    other['id'] = 'W12-CONTRARY'
    other['data']['details']['conclusion'] = 'shared_dependency'
    source['assertions'].append(other)
    return source


def witness_paths(row):
    return tuple((tuple(n.identifier for n in w.nodes),
                  tuple(edge.source_ref.record_id for edge in w.edges))
                 for w in row.witness.owner_witnesses if getattr(w, 'kind', None) in ('path', 'cycle'))


def test_literal_citation_path_has_ordered_witness_and_only_citation_meaning():
    source = citation_source()
    relation(source, 'cites', 'citation-tail', from_ref='artifact2', to_ref='dataset')
    out = run(source, queries=(graph_query(source, 'citation', 'artifact', 'dataset',
        predicates=('cites',)),))[0]
    rows = selected(out, 'citation_path_witness')
    assert len(rows) == 1 and rows[0].observation_kind == 'positive_witness'
    assert rows[0].scope_ref.graph_view == 'citation'
    assert ((('artifact', 'artifact2', 'dataset'), ('r-cites', 'citation-tail'))) in witness_paths(rows[0])
    assert {'r-cites', 'citation-tail'} <= {basis.source.identifier for basis in rows[0].basis_refs}
    assert all(reason.code != 'scope_unestablished' for reason in rows[0].reason_refs)
    assert not selected(out, 'shared_origin_witness')
    assert not selected(out, 'transformation_path_witness')


@pytest.mark.parametrize('state', ('denied', 'withdrawn', 'superseded'))
def test_ineligible_citation_cannot_become_positive_path(state):
    source = citation_source(polarity='denied' if state == 'denied' else 'affirmed')
    if state != 'denied':
        row = h.cases.by_id(source, 'r-cites')
        row.update(lifecycle_state=state, lifecycle_basis_ref_ids=['support'])
    out = run(source, queries=(graph_query(source, 'citation', 'artifact', 'artifact2',
        predicates=('cites',)),))[0]
    assert not selected(out, 'citation_path_witness')
    assert 'no_witness_in_examined_view' in forms(out, 'scoped_no_witness')


def test_cycle_keeps_finite_closed_citation_path_without_claim_origin_promotion():
    source = citation_source(cycle=True)
    out = run(source, queries=(graph_query(source, 'citation', 'artifact', 'artifact2',
        predicates=('cites',)),))[0]
    rows = selected(out, 'view_cycle_witness')
    assert rows and all(row.scope_ref.graph_view == 'citation' for row in rows)
    paths = [path for row in rows for path in witness_paths(row)]
    assert any(nodes[0] == nodes[-1] and set(edges) == {'r-cites', 'return-citation'}
               for nodes, edges in paths)
    assert any({'r-cites', 'return-citation'} <=
        {basis.source.identifier for basis in row.basis_refs} for row in rows)
    assert not selected(out, 'shared_origin_witness')


def test_positive_citation_carries_relevant_denial_without_laundering_uncontested_basis():
    source = citation_source()
    relation(source, 'cites', 'citation-denial', polarity='denied')
    out = run(source, queries=(graph_query(source, 'citation', 'artifact', 'artifact2',
        predicates=('cites',)),))[0]
    rows = selected(out, 'citation_path_witness')
    assert rows
    for row in rows:
        assert 'r-cites' in {basis.source.identifier for basis in row.basis_refs}
        assert 'citation-denial' in {ref.identifier for ref in row.contrary_input_refs}
        assert any(reason.code == 'premise_disputed' for reason in row.reason_refs)


def test_examined_empty_view_preserves_search_population_and_never_infers_independence():
    source = h.cases.pool()
    out = run(source, queries=(graph_query(source, 'citation', 'artifact', 'artifact2',
        predicates=('cites',)),))[0]
    rows = selected(out, 'scoped_no_witness')
    assert rows and {row.observation_kind for row in rows} == {'no_witness_in_examined_view'}
    for row in rows:
        assert not row.threat_family_refs
        assert row.witness.owner_witnesses
        assert all(w.kind == 'no_witness_in_examined_view' for w in row.witness.owner_witnesses)
        assert any(w.starts and w.examined_nodes for w in row.witness.owner_witnesses)


def test_h7_shared_origin_keeps_multiple_contributions_and_exact_origin_premises():
    out = run(h.hero(), owners=('origins',))[0]
    rows = selected(out, 'shared_origin_witness')
    assert rows and all(row.observation_kind == 'positive_witness' for row in rows)
    assert any('H7-O1' in input_ids(row) for row in rows)
    assert all(row.scope_ref.dependency_dimension == 'acquisition' for row in rows)
    assert all(set(row.threat_family_refs) <= {'SIT-TH001'} for row in rows)


def test_evaluator_common_ancestor_and_label_match_remain_distinct_observations():
    out = run(e.small(), owners=('evaluator',))[0]
    overlap = selected(out, 'evaluator_overlap_witness')
    labels = selected(out, 'family_label_match')
    assert overlap and labels
    assert all(row.observation_kind == 'positive_witness' for row in overlap)
    assert all(row.observation_kind in ('attributed_observation', 'positive_witness') for row in labels)
    assert any('model3' in nodes for row in overlap for nodes, unused in witness_paths(row))
    assert all('label' in row.interpretation_limit.lower() for row in labels)


def test_family_labels_survive_missing_ancestry_without_creating_shared_ancestor():
    source = e.small(edges=())
    out = run(source, owners=('evaluator',))[0]
    assert selected(out, 'family_label_match')
    assert not selected(out, 'evaluator_overlap_witness')


def test_supported_absence_requires_original_route_coverage_qualification():
    source = r.small(direct=False, authority=False, coverage='complete_for_scope')
    out, profiles, *_ = run(source, owners=('route',), ctx=r.context(source))
    assert profiles[0].facts.bounded_absence
    assert 'bounded_absence_under_declared_coverage' in forms(out, 'scoped_no_witness')
    rows = selected(out, 'scoped_no_witness')
    assert any('coverage' in input_ids(row) | {ref.identifier for ref in row.scope_ref.coverage_refs}
        | {ref.identifier for pop in row.population_refs for ref in pop.coverage_refs}
        | {basis.source.identifier for basis in row.basis_refs} for row in rows)
    assert all(not row.threat_family_refs for row in rows)


def test_partial_route_coverage_cannot_be_promoted_to_bounded_absence():
    source = r.small(direct=False, authority=False, coverage='partial')
    out = run(source, owners=('route',), ctx=r.context(source))[0]
    assert all(row.observation_kind != 'bounded_absence_under_declared_coverage' for row in out.findings)
    assert selected(out, 'correction_route_limitation')


def test_qualified_authorized_route_is_not_reported_as_unestablished():
    source = r.small(coverage='complete_for_scope')
    out, profiles, *_ = run(source, owners=('route',), ctx=r.context(source))
    assert profiles[0].facts.authorized_path is not None
    assert not selected(out, 'correction_route_limitation')


def corrective_control(*, polarity='affirmed'):
    source = r.small(authority=False)
    h.cases.by_id(source, 'channel')['data']['target_refs'] = ['model']
    provider = copy.deepcopy(h.cases.by_id(source, 'actor'))
    provider['id'] = 'unrelated-provider'
    source['records'].append(provider)
    h.cases.by_id(source, 'model')['data']['provider_ref'] = 'unrelated-provider'
    source['inquiries'][0]['dependency_dimensions'].append('organizational_control')
    edge = relation(source, 'owned_by', 'target-owner', from_ref='model', polarity=polarity)
    edge['scope']['effective_window'] = r.window()
    edge['asserted_at'] = r.known()
    r.supplied(edge)
    return source


def test_correction_dependency_requires_actual_channel_and_target_control_paths():
    source = corrective_control()
    out = run(source, owners=('route',), ctx=r.context(source, target='model'))[0]
    rows = selected(out, 'correction_dependency_witness')
    assert rows and all(row.observation_kind == 'positive_witness' for row in rows)
    assert any('target-owner' in input_ids(row) for row in rows)
    assert all(set(row.threat_family_refs) <= {'SIT-TH010'} for row in rows)
    paths = [path for row in rows for path in witness_paths(row)]
    assert any(nodes == ('model', 'actor') for nodes, unused in paths)
    unselected = copy.deepcopy(source)
    unselected['inquiries'][0]['dependency_dimensions'].remove('organizational_control')
    omitted = run(unselected, owners=('route',), ctx=r.context(unselected, target='model'))[0]
    assert not selected(omitted, 'correction_dependency_witness')


def test_denied_target_control_cannot_create_corrective_dependency():
    source = corrective_control(polarity='denied')
    out = run(source, owners=('route',), ctx=r.context(source, target='model'))[0]
    assert not selected(out, 'correction_dependency_witness')


def test_native_failed_handling_remains_attributed_case_outcome():
    source = o.small()
    h.cases.by_id(source, 'handling')['data']['details']['outcome'] = 'failed'
    out = run(source, owners=('outcomes',))[0]
    rows = selected(out, 'case_handling_disclosure')
    assert rows and all(row.observation_kind == 'attributed_observation' for row in rows)
    assert any('handling' in input_ids(row) for row in rows)
    assert selected(out, 'linked_change_disclosure')


def test_missing_target_effect_stays_gap_alongside_supported_change():
    source = o.small()
    h.cases.by_id(source, 'submission')['data']['target_refs'].append('artifact')
    out = run(source, owners=('outcomes',))[0]
    assert selected(out, 'linked_change_disclosure')
    rows = selected(out, 'downstream_change_undocumented')
    assert rows and all(row.observation_kind == 'qualification_gap' for row in rows)
    assert any('artifact' in input_ids(row) for row in rows)


def test_independence_conflict_preserves_original_and_contrary_assessments():
    out = run(conflicting_independence(), owners=('comparison',))[0]
    rows = selected(out, 'independence_record_conflict')
    assert rows and all(row.observation_kind == 'recorded_conflict' for row in rows)
    assert any({'H7-IND12', 'W12-CONTRARY'} <=
        (input_ids(row) | {ref.identifier for ref in row.contrary_input_refs}) for row in rows)


def test_source_assurance_loop_is_gap_and_cannot_authenticate_itself():
    source = self_support()
    out = run(source, queries=(graph_query(source, 'assertion_assurance', 'H7-L01', 'W12-SELF',
        dimension='acquisition'),))[0]
    rows = selected(out, 'assurance_loop_limitation')
    assert rows and all(row.observation_kind == 'qualification_gap' for row in rows)
    assert any('H7-L01' in input_ids(row) for row in rows)


@pytest.mark.parametrize('role_source', ('transformer', 'generated_by'))
def test_model_mediated_derivation_requires_explicit_generator_and_transformation(role_source):
    source = citation_source(predicate='derived_from')
    transform = h.cases.by_id(source, 'r-derived_from')['data']
    if role_source == 'transformer':
        transform['details']['transformer_ref'] = 'model'
        query = graph_query(source, 'claim_origin', 'e', 'e2',
            predicates=('derived_from',), dimension='acquisition')
    else:
        transform.update(from_ref='artifact', to_ref='artifact2', dimension=None)
        del transform['details']['transformer_ref']
        relation(source, 'generated_by')
        query = graph_query(source, 'material_transformation', 'artifact', 'artifact2',
            predicates=('derived_from',))
    out = run(source, queries=(query,))[0]
    rows = selected(out, 'model_mediated_derivation_witness')
    assert rows and all(row.observation_kind == 'positive_witness' for row in rows)
    assert all(set(row.threat_family_refs) <= {'SIT-TH004'} for row in rows)
    assert any('r-derived_from' in input_ids(row) for row in rows)


def test_generation_without_transformation_cannot_manufacture_derivation():
    source = h.cases.pool()
    relation(source, 'generated_by')
    out = run(source, queries=(graph_query(source, 'model_evaluation', 'artifact', 'model',
        predicates=('generated_by',)),))[0]
    assert not selected(out, 'model_mediated_derivation_witness')


def test_array_order_cannot_change_observation_forms_or_premise_sets():
    source = h.cases.rich()
    changed = copy.deepcopy(source)
    for collection in ('records', 'assertions', 'evidence_references'):
        changed[collection].reverse()
    def signatures(out):
        return sorted((row.condition_code, row.observation_kind,
            row.scope_ref._key(), tuple(sorted(ref._key() for ref in row.witness.input_refs)),
            row.threat_family_refs) for row in out.findings)
    assert signatures(run(source)[0]) == signatures(run(changed)[0])


def test_explicit_unknown_endpoint_remains_provenance_gap_without_erasure_claim():
    source = h.cases.pool()
    h.cases.by_id(source, 'unresolved')['data']['expected_kinds'] = ['evidence_item']
    relation(source, 'derived_from', to_ref='unresolved')
    out = run(source, queries=(graph_query(source, 'claim_origin', 'e', 'e2',
        predicates=('derived_from',), dimension='acquisition'),))[0]
    rows = selected(out, 'provenance_gap')
    assert rows and all(row.observation_kind == 'qualification_gap' for row in rows)
    assert any('unresolved' in input_ids(row) for row in rows)
    assert all(set(row.threat_family_refs) <= {'SIT-TH008'} for row in rows)


def test_native_externality_and_unknown_stage_keep_independent_limitations():
    source = h.hero()
    h.cases.by_id(source, 'H7-EXT-F')['data']['details']['conclusion'] = 'unknown'
    out = run(source, owners=('externality',))[0]
    rows = selected(out, 'externality_stage_limitation')
    assert rows and all(row.observation_kind == 'qualification_gap' for row in rows)
    assert any('H7-EXT-F' in input_ids(row) for row in rows)
    assert all(set(row.threat_family_refs) <= {'SIT-TH012'} for row in rows)


def test_documented_cohort_exclusion_keeps_exact_stage_and_no_motive():
    source = h.hero()
    out, profiles, *_ = run(source, owners=('selection',))
    rows = selected(out, 'recorded_stage_exclusion')
    assert rows and all(row.observation_kind == 'attributed_observation' for row in rows)
    assert any('H7-PS-F' in input_ids(row) for row in rows)
    for row in rows:
        assert row.scope_ref.operation_anchor == ('answer-run-1', 'select-1', 'selection')
        assert row.result_refs
        assert all(any(ref is result.ref for result in profiles[0].results)
                   for ref in row.result_refs)
        assert 'motive' in row.interpretation_limit.lower()


def test_unknown_stage_is_not_evidenced_exclusion():
    source = h.hero()
    h.cases.by_id(source, 'H7-PS-F')['data']['state'] = 'unknown'
    out = run(source, owners=('selection',))[0]
    assert not any('H7-PS-F' in input_ids(row) for row in selected(out, 'recorded_stage_exclusion'))
    gaps = selected(out, 'externality_stage_limitation')
    assert gaps and all(row.observation_kind == 'qualification_gap' for row in gaps)
    assert any(reason.code == 'stage_classification_unresolved'
               for row in gaps for reason in row.reason_refs)


def test_findings_and_witnesses_are_frozen():
    out = run(h.cases.pool())[0]
    assert out.findings
    with pytest.raises(FrozenInstanceError):
        out.findings[0].condition_code = 'clean_source'
    with pytest.raises(FrozenInstanceError):
        out.findings[0].witness.input_refs = ()


def test_shared_budget_exhaustion_cannot_return_empty_completed_findings():
    source = h.cases.pool()
    prepared = h.admit(source)
    budget, job = h.job_pair()
    job.charge(1_000_000 - job.used)
    with pytest.raises(_AnalysisAborted):
        findings._findings(prepared, context(source), budget.witnesses, job)


def test_current_job_owner_profiles_cannot_be_replayed_in_another_job():
    source = o.small()
    prepared = h.admit(source)
    budget, job = h.job_pair()
    profile = owner_profile('outcomes', source, prepared, job, budget.witnesses)
    other_budget, other_job = h.job_pair()
    with pytest.raises(TypeError):
        findings._findings(prepared, context(source), other_budget.witnesses, other_job,
            stage_profiles=(profile,))


def test_unrelated_witness_ledger_cannot_be_used_by_findings():
    source = h.cases.pool()
    prepared = h.admit(source)
    budget, job = h.job_pair()
    other_budget, _ = h.job_pair()
    with pytest.raises(TypeError):
        findings._findings(prepared, context(source), other_budget.witnesses, job)


def test_witness_quota_cannot_return_unwitnessed_findings():
    source = h.cases.pool()
    prepared = h.admit(source)
    budget, job = h.job_pair()
    ledger = budget.witnesses
    ledger.retain(ledger.reserve(witnesses=20_000, members=0))
    with pytest.raises(_AnalysisAborted) as stopped:
        findings._findings(prepared, context(source), ledger, job)
    assert stopped.value.limit_id == 'WU9-L13'


def test_graph_request_from_other_inquiry_cannot_be_spliced_into_finding():
    source = citation_source()
    other = copy.deepcopy(source['inquiries'][0])
    other['id'] = 'other-inquiry'
    source['inquiries'].append(other)
    prepared = h.admit(source)
    budget, job = h.job_pair()
    query = graph_query(source, 'citation', 'artifact', 'artifact2', predicates=('cites',))
    query = (replace(query[0], inquiry_ref='other-inquiry'),) + query[1:]
    with pytest.raises(TypeError):
        findings._findings(prepared, context(source), budget.witnesses, job, graph_requests=(query,))
