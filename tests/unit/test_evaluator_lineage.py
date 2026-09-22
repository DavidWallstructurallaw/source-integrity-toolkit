# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W08 direct evaluator oracles for Definitions 25.1 and VF025--VF028.

The finite H7 and W7 expectations below are independent source expectations.
Admission, projections, traversals and witness accounting execute in a real
component job; no public W13 orchestration or outside authentication is claimed.
"""
import copy
from dataclasses import FrozenInstanceError, replace
import importlib.util
from pathlib import Path

import pytest

from source_integrity_toolkit.analysis import evaluator_lineage as evaluator
from source_integrity_toolkit.contracts.bundle import _Object
from source_integrity_toolkit.contracts.evidence import _Node
from source_integrity_toolkit.contracts.execution import _AnalysisAborted
from source_integrity_toolkit.runtime import resources
from source_integrity_toolkit.validation.limits import _WitnessLedger

_spec = importlib.util.spec_from_file_location(
    'sit_w08_evaluator_helpers', Path(__file__).with_name('test_origins.py'))
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)

FIELDS = ('shared_recorded_ancestor_count', 'matching_family_label_count',
          'evaluator_overlap_disclosures', 'evaluator_overlap_witnesses')
MODEL_PREDICATES = ('generated_by', 'model_derived_from', 'trained_on')


def context(source, *, evaluation=None, roles=('generator', 'judge'),
            dimension='model_ancestry', view='model_evaluation', **changes):
    inquiry = source['inquiries'][0]
    identifier = evaluation or ('H7-EVAL' if inquiry['id'] == 'H7-I1' else 'evaluation')
    values = dict(subject_refs=(identifier,), operation_anchor=roles,
                  graph_view=view, dependency_dimension=dimension,
                  coverage_kind='model_history', relation_types=MODEL_PREDICATES)
    values.update(changes)
    return replace(h.context(source), **values)


def run(source, **changes):
    snapshot = h.prepared(source)
    ctx = context(source, **changes)
    owner, job = h.job_pair()
    ledger = owner.witnesses
    before = (owner.used, job.used, ledger._retained_witnesses, ledger._retained_members)
    out = evaluator._evaluator_lineage(snapshot, ctx, ledger, job)
    assert owner.used - before[0] == job.used - before[1] > 0
    assert out.facts.prepared is snapshot and out.facts.context is ctx
    assert out.facts.job_port is job
    assert ledger._retained_witnesses - before[2] == len(out.witnesses)
    assert ledger._retained_members - before[3] == sum(w.member_count for w in out.witnesses)
    assert tuple(row.ref.field_key for row in out.results) == FIELDS
    for row in out.results:
        assert row.ref.diagnostic_id == 'SIT-M008'
        scope = row.ref.scope
        assert scope.inquiry_ref.identifier == ctx.inquiry_ref
        assert tuple(ref.identifier for ref in scope.claim_refs) == ctx.claim_refs
        assert tuple(ref.identifier for ref in scope.target_refs) == ctx.subject_refs
        assert scope.graph_view == ctx.graph_view
        assert scope.dependency_dimension == ctx.dependency_dimension
        assert scope.temporal_basis == ctx.temporal_basis
        assert scope.operation_anchor == ctx.operation_anchor
        assert row.basis_refs and row.interpretation_limit
        assert all(check.result_ref is row.ref for check in row.check_refs)
        assert all(reason.scope is scope and row.ref in reason.affected_result_refs for reason in row.reason_refs)
        assert all(witness.scope is scope for witness in row.witness_refs)
        checks = {check.check_id: check.state for check in row.check_refs}
        assert checks['PC01'] == checks['PC02'] == checks['PC24'] == 'met'
        assert {'PC03', 'PC04', 'PC05', 'PC06', 'PC08', 'PC09', 'PC10', 'PC14'} <= checks.keys()
        provider = out.facts.pc04
        actual = next(check for check in row.check_refs if check.check_id == 'PC04')
        assert actual.state == provider.state
        assert {(ref.collection, ref.identifier, ref.selector or '') for ref in actual.input_refs} == {
            (ref.collection, ref.record_id, ref.selector) for ref in provider.input_refs}
    return out, snapshot, owner, job


def leaf(out, field):
    return next(row for row in out.results if row.ref.field_key == field)


def codes(row):
    return {reason.code for reason in row.reason_refs}


def identifiers(entities):
    return tuple(entity.identifier for entity in entities)


def count(out, field=FIELDS[0]):
    row = leaf(out, field)
    assert row.execution_state == 'completed'
    assert row.value_kind == 'count'
    if row.value is not None:
        assert row.value.population in row.population_refs
        assert row.value.population.membership_state == 'enumerated_for_scope'
        assert row.value.population.selection_rule
        assert row.value.population.unit == ('family_label' if field == FIELDS[1] else 'record')
    return {'state': row.result_state, 'value': None if row.value is None else row.value.value,
            'reasons': codes(row)}


def assert_count(actual, value, *, state='available', reasons=()):
    assert actual['state'] == state and actual['value'] == value
    assert set(reasons) <= actual['reasons']


def payload(out):
    row = leaf(out, FIELDS[2])
    assert (row.execution_state, row.result_state, row.value_kind) == (
        'completed', 'available', 'record_disclosures')
    return {item.source.identifier: h.native(item.fields) for item in row.value.records}


def tokens(value):
    if isinstance(value, dict):
        return [part for key, item in value.items() for part in (key, *tokens(item))]
    if isinstance(value, (list, tuple)):
        return [part for item in value for part in tokens(item)]
    return [value]


def paths(out):
    return {(tuple(n.identifier for n in w.nodes), tuple(e.source_ref.record_id for e in w.edges))
            for w in out.witnesses if w.kind == 'path'}


def binding(role, object_ref):
    return {'role': role, 'object_ref': object_ref,
            'evidence_ref_ids': ['support'], 'qualifications': ['Supplied role, no independent vote.']}


def add_model(source, identifier, *, family='F'):
    model = copy.deepcopy(h.cases.by_id(source, 'model'))
    model['id'] = identifier
    model['data'].update(model_key=identifier, family_label=family)
    source['records'].append(model)
    return model


def small(*, edges=(('left', 'model_derived_from', 'model', 'model3'),
                    ('right', 'model_derived_from', 'model2', 'model3')),
          bindings=None):
    source = h.cases.pool()
    source['inquiries'][0]['dependency_dimensions'] = [
        'model_ancestry', 'evaluation_rubric', 'analytical_method', 'organizational_control']
    source['assertions'] = [h.relation(*edge, dimension='model_ancestry') for edge in edges]
    for name in ('model', 'model2'):
        h.cases.by_id(source, name)['data']['family_label'] = 'F'
        h.supplied(h.cases.by_id(source, name))
    add_model(source, 'model3', family='ancestor-family')
    evaluation = h.cases.by_id(source, 'evaluation')
    evaluation['data'].update(evaluation_kind='judgment', role_bindings=bindings or [
        binding('generator', 'model'), binding('judge', 'model2')])
    h.supplied(evaluation)
    coverage = h.add_coverage(source, ['model', 'model2', 'model3', 'dataset'],
        state='partial', dimension='model_ancestry', predicates=MODEL_PREDICATES)
    coverage['data']['details']['coverage_kind'] = 'model_history'
    return source


@pytest.fixture(scope='module')
def hero():
    return run(h.hero())[0]


def test_vf025_p_h7_two_strict_ancestors_retain_partial_history(hero):
    assert_count(count(hero), 2, reasons=('upstream_coverage_incomplete',))
    assert identifiers(hero.facts.common_ancestors) == ('H7-MBASE', 'H7-TRAINING')
    assert identifiers(hero.facts.shared_objects) == ()
    assert hero.facts.one_sided == ()
    row = leaf(hero, FIELDS[0])
    assert row.result_origin == 'graph_derivation'
    assert tuple(ref.identifier for ref in row.value.population.member_refs) == ('H7-MBASE', 'H7-TRAINING')


def test_vf025_n_removing_ancestry_keeps_family_match_without_invented_parent(hero):
    assert_count(count(hero), 2)
    source = h.hero()
    source['assertions'] = [row for row in source['assertions'] if row['id'] not in
                            ('H7-ML01', 'H7-ML02', 'H7-ML03', 'H7-ML04')]
    out = run(source)[0]
    assert_count(count(out), 0, reasons=('upstream_coverage_incomplete',))
    assert_count(count(out, FIELDS[1]), 1)
    assert not out.facts.common_ancestors
    mutant = copy.deepcopy(count(out)); mutant['value'] = 1
    with pytest.raises(AssertionError):
        assert_count(mutant, 0)


@pytest.mark.parametrize('mode', ('missing', 'unresolved'))
def test_vf025_m_missing_or_unresolved_role_is_unavailable(mode):
    source = small()
    evaluation = h.cases.by_id(source, 'evaluation')
    if mode == 'missing':
        evaluation['data']['role_bindings'].pop()
        evaluation['gaps'] = [{'field': 'data.role_bindings', 'reason': 'not_recorded',
                               'detail': 'Judge binding has not been supplied.'}]
    else:
        h.cases.by_id(source, 'unresolved')['data']['expected_kinds'] = ['model']
        evaluation['data']['role_bindings'][1]['object_ref'] = 'unresolved'
    out = run(source)[0]
    assert_count(count(out), None, state='unavailable', reasons=(
        'roles_incomplete' if mode == 'missing' else 'unknown_endpoint',))
    assert payload(out)
    assert next(check for check in leaf(out, FIELDS[0]).check_refs if check.check_id == 'PC14').state != 'met'
    mutant = dict(count(out), state='available', value=0)
    with pytest.raises(AssertionError):
        assert_count(mutant, None, state='unavailable')


def test_vf025_b_w705_one_ancestor_and_zero_length_identity_are_separate():
    related = run(small())[0]
    assert_count(count(related), 1)
    assert identifiers(related.facts.common_ancestors) == ('model3',)
    identical = small(edges=(), bindings=[binding('generator', 'model'), binding('judge', 'model')])
    same = run(identical)[0]
    assert_count(count(same), 0)
    assert identifiers(same.facts.shared_objects) == ('model',)
    assert not same.facts.common_ancestors
    assert_count(count(same, FIELDS[1]), 1)


def test_vf025_b_one_sided_ancestry_survives_zero_shared_count():
    out = run(small(edges=(('one-way', 'model_derived_from', 'model', 'model2'),)))[0]
    assert_count(count(out), 0)
    assert not out.facts.shared_objects
    assert out.facts.one_sided
    assert (('model', 'model2'), ('one-way',)) in paths(out)


def test_vf025_b_common_dataset_with_distinct_subsets_stays_dataset_level(hero):
    assert_count(count(hero), 2)
    values = tokens(payload(hero))
    assert all(value in values for value in ('H7-TRAINING', 'split-A', 'split-B'))
    limits = ' '.join(row.interpretation_limit for row in hero.results).lower()
    assert 'dataset' in limits and ('row' in limits or 'granular' in limits)


def test_vf026_p_exact_h7_family_is_separate_from_model_ancestry(hero):
    assert_count(count(hero, FIELDS[1]), 1)
    assert hero.facts.matching_family_labels == ('H7-family',)
    assert leaf(hero, FIELDS[1]).result_origin == 'inventory'
    assert_count(count(hero), 2)


@pytest.mark.parametrize('different', ('f', ' F', 'F ', 'same-provider-new-family'))
def test_vf026_n_only_exact_family_strings_match(different):
    source = small()
    positive = run(source)[0]
    assert_count(count(positive, FIELDS[1]), 1)
    h.cases.by_id(source, 'model2')['data']['family_label'] = different
    out = run(source)[0]
    assert_count(count(out, FIELDS[1]), 0)
    assert out.facts.matching_family_labels == ()
    assert_count(count(out), 1)
    mutant = dict(count(out, FIELDS[1]), value=1)
    with pytest.raises(AssertionError):
        assert_count(mutant, 0)


def test_vf026_m_unknown_label_preserves_gap_without_modelkey_provider_fallback():
    source = small()
    model = h.cases.by_id(source, 'model2')
    model['data'].update(family_label=None, model_key='F')
    model['gaps'] = [{'field': 'data.family_label', 'reason': 'not_recorded',
                     'detail': 'Family exposure unexamined; provider is no substitute.'}]
    out = run(source)[0]
    assert_count(count(out, FIELDS[1]), 0)
    assert identifiers(out.facts.missing_family_models) == ('model2',)
    values = tokens(payload(out))
    assert 'data.family_label' in values and model['gaps'][0]['detail'] in values
    assert_count(count(out), 1)
    assert codes(leaf(out, FIELDS[1]))


def test_vf026_b_repeated_bindings_and_labelled_ancestors_do_not_add_matches():
    source = small()
    add_model(source, 'model4')
    add_model(source, 'model5')
    h.cases.by_id(source, 'evaluation')['data']['role_bindings'].extend([
        binding('generator', 'model4'), binding('judge', 'model5'), binding('judge', 'model2')])
    out = run(source)[0]
    assert_count(count(out, FIELDS[1]), 1)
    assert out.facts.matching_family_labels == ('F',)
    assert 'ancestor-family' not in out.facts.matching_family_labels
    assert_count(count(out), 1)


def test_vf027_p_h7_discloses_exact_actual_rolepair_native_basis_and_partial_history(hero):
    values = tokens(payload(hero))
    for item in ('H7-EVAL', 'generator', 'judge', 'H7-MGEN', 'H7-MJUDGE',
                 'H7-COV-MODEL', 'partial', 'documented_record'):
        assert item in values
    assert hero.facts.roles == ('generator', 'judge')
    assert identifiers(hero.facts.left_objects) == ('H7-MGEN',)
    assert identifiers(hero.facts.right_objects) == ('H7-MJUDGE',)
    assert all('correlation' in row.interpretation_limit.lower() for row in hero.results)


def test_vf027_n_common_reviewed_target_does_not_become_process_ancestor():
    source = small(edges=())
    first = h.cases.by_id(source, 'evaluation')
    first['data'].update(evaluation_kind='human_review', review_contribution='Compare the supplied calculation.',
        role_bindings=[binding('human_reviewer', 'actor'), binding('method_input', 'artifact')])
    other = copy.deepcopy(first); other['id'] = 'review2'
    other['data']['role_bindings'][1]['object_ref'] = 'artifact2'
    source['records'].append(other)
    source['inquiries'][0]['target_object_refs'].append('review2')
    for identifier in ('evaluation', 'review2'):
        out = run(source, evaluation=identifier, roles=('human_reviewer', 'method_input'))[0]
        assert_count(count(out), 0)
        assert 'claim' in tokens(payload(out))
        mutant = dict(count(out), value=1)
        with pytest.raises(AssertionError):
            assert_count(mutant, 0)


def test_vf027_m_unexamined_training_and_rubric_remain_disclosed(hero):
    values = tokens(payload(hero))
    assert 'partial' in values
    assert any(isinstance(value, str) and 'training' in value.lower() and 'examin' in value.lower()
               for value in values)
    assert 'upstream_coverage_incomplete' in codes(leaf(hero, FIELDS[2]))
    # A recorded positive commonality cannot silently complete other dimensions.
    assert next(c for c in leaf(hero, FIELDS[2]).check_refs if c.check_id == 'PC06').state != 'met'


def test_vf027_m_qualified_method_comparison_does_not_complete_model_or_rubric_exposure():
    spec = importlib.util.spec_from_file_location(
        'sit_w08_human_exposure_case', Path(__file__).with_name('test_human_review.py'))
    human_cases = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(human_cases)
    source = human_cases.method_pair()
    review = human_cases.run(source, human_cases.REVIEWS)[0]
    disclosure = human_cases.assert_process(review, source)
    assert disclosure['process_qualification_state'] == 'met'
    for dimension in ('model_ancestry', 'evaluation_rubric'):
        out = run(source, evaluation='H7-HREVIEW', roles=('human_reviewer', 'method_input'),
                  dimension=dimension)[0]
        assert_count(count(out), 0, reasons=('upstream_coverage_incomplete',))
        assert 'upstream_coverage_incomplete' in codes(leaf(out, FIELDS[2]))
        assert next(c for c in leaf(out, FIELDS[2]).check_refs if c.check_id == 'PC06').state != 'met'


def test_vf027_b_actor_identity_models_and_shared_rubric_are_distinct():
    source = small(edges=(), bindings=[binding('generator', 'actor'), binding('judge', 'actor')])
    out = run(source)[0]
    assert_count(count(out), 0)
    assert identifiers(out.facts.shared_objects) == ('actor',)
    assert out.facts.matching_family_labels == ()
    material = small(edges=(), bindings=[binding('reference_answer', 'artifact'), binding('rubric', 'artifact2')])
    material['assertions'].extend([
        h.relation('reference-history', 'copies', 'artifact', 'dataset', dimension=None),
        h.relation('rubric-history', 'copies', 'artifact2', 'dataset', dimension=None)])
    profile = run(material, roles=('reference_answer', 'rubric'), dimension='evaluation_rubric',
                  view='material_transformation', relation_types=('copies',))[0]
    assert_count(count(profile), 1)
    assert identifiers(profile.facts.common_ancestors) == ('dataset',)
    assert (('artifact', 'dataset'), ('reference-history',)) in paths(profile)
    assert (('artifact2', 'dataset'), ('rubric-history',)) in paths(profile)


def test_vf028_p_h7_paired_paths_preserve_exact_ordered_edges(hero):
    expected = {(('H7-MGEN', 'H7-MBASE'), ('H7-ML01',)),
                (('H7-MJUDGE', 'H7-MBASE'), ('H7-ML02',)),
                (('H7-MGEN', 'H7-TRAINING'), ('H7-ML03',)),
                (('H7-MJUDGE', 'H7-TRAINING'), ('H7-ML04',))}
    assert expected <= paths(hero)
    witness = leaf(hero, FIELDS[3])
    assert witness.execution_state == 'completed' and witness.result_state == 'available'
    assert witness.value.witness_refs == witness.witness_refs
    assert witness.witness_refs


def test_vf028_n_no_ancestry_path_can_be_fabricated_from_family_or_prose():
    out = run(small(edges=()))[0]
    assert_count(count(out, FIELDS[1]), 1)
    assert_count(count(out), 0)
    actual = paths(out)
    assert actual == set()
    fabricated = actual | {(('model', 'model2'), ('family-label-F',))}
    with pytest.raises(AssertionError):
        assert fabricated == set()
    row = leaf(out, FIELDS[3])
    assert row.result_state == 'available'
    assert all(ref.kind != 'path' for ref in row.value.witness_refs)


def test_vf028_m_completed_partial_history_empty_witness_has_scoped_limit():
    source = small(edges=())
    h.cases.by_id(source, 'model2')['data']['family_label'] = 'unrelated-supplied-label'
    out = run(source)[0]
    row = leaf(out, FIELDS[3])
    assert (row.execution_state, row.result_state) == ('completed', 'available')
    assert row.value.witness_refs == ()
    assert 'upstream_coverage_incomplete' in codes(row)
    assert next(c for c in row.check_refs if c.check_id == 'PC24').state == 'met'
    assert 'independen' in row.interpretation_limit.lower()


def test_vf028_b_diamond_paths_are_finite_and_do_not_multiply_ancestor_ids():
    source = small(edges=(('left-a', 'model_derived_from', 'model', 'model3'),
        ('left-b', 'model_derived_from', 'model', 'model4'),
        ('a-root', 'model_derived_from', 'model3', 'model5'),
        ('b-root', 'model_derived_from', 'model4', 'model5'),
        ('right-root', 'model_derived_from', 'model2', 'model5')))
    add_model(source, 'model4'); add_model(source, 'model5')
    out = run(source)[0]
    assert_count(count(out), 1)
    assert identifiers(out.facts.common_ancestors) == ('model5',)
    assert (('model2', 'model5'), ('right-root',)) in paths(out)
    assert ({(('model', 'model3', 'model5'), ('left-a', 'a-root')),
             (('model', 'model4', 'model5'), ('left-b', 'b-root'))} & paths(out))


def test_vf028_b_cycle_return_never_counts_identical_subject_as_own_ancestor():
    source = small(edges=(('outward', 'model_derived_from', 'model', 'model3'),
        ('return', 'model_derived_from', 'model3', 'model')),
        bindings=[binding('generator', 'model'), binding('judge', 'model')])
    out = run(source)[0]
    assert_count(count(out), 1, reasons=('lineage_cycle',))
    assert identifiers(out.facts.common_ancestors) == ('model3',)
    assert identifiers(out.facts.shared_objects) == ('model',)
    cycles = [w for w in out.witnesses if w.kind == 'cycle']
    assert cycles
    for witness in cycles:
        assert witness.nodes[0] is witness.nodes[-1]
        assert {e.source_ref.record_id for e in witness.edges} == {'outward', 'return'}


def test_common_unresolved_reference_never_instantiates_shared_model_ancestor():
    source = small(edges=(('left-hidden', 'model_derived_from', 'model', 'unresolved'),
                          ('right-hidden', 'model_derived_from', 'model2', 'unresolved')))
    h.cases.by_id(source, 'unresolved')['data']['expected_kinds'] = ['model']
    out = run(source)[0]
    assert_count(count(out), 0, reasons=('unknown_endpoint', 'upstream_coverage_incomplete'))
    assert identifiers(out.facts.common_ancestors) == ()
    assert 'unresolved' in tokens(payload(out))


def test_multiple_role_bindings_keep_nonreflexive_path_from_another_bound_model():
    source = small(edges=(('left-parent', 'model_derived_from', 'model2', 'model'),
        ('right-parent', 'model_derived_from', 'model3', 'model')),
        bindings=[binding('generator', 'model'), binding('generator', 'model2'), binding('judge', 'model3')])
    out = run(source)[0]
    assert_count(count(out), 1)
    assert identifiers(out.facts.common_ancestors) == ('model',)
    assert (('model2', 'model'), ('left-parent',)) in paths(out)
    assert (('model3', 'model'), ('right-parent',)) in paths(out)


def test_unbound_models_and_other_evaluations_do_not_expand_requested_pair():
    source = small()
    for identifier in ('unbound-left', 'unbound-right', 'unbound-parent'):
        add_model(source, identifier)
    source['assertions'].extend([
        h.relation('unbound-a', 'model_derived_from', 'unbound-left', 'unbound-parent', dimension='model_ancestry'),
        h.relation('unbound-b', 'model_derived_from', 'unbound-right', 'unbound-parent', dimension='model_ancestry')])
    extra = copy.deepcopy(h.cases.by_id(source, 'evaluation')); extra['id'] = 'unselected'
    extra['data']['role_bindings'] = [binding('generator', 'unbound-left'), binding('judge', 'unbound-right')]
    source['records'].append(extra)
    out = run(source)[0]
    assert_count(count(out), 1)
    assert identifiers(out.facts.common_ancestors) == ('model3',)
    assert all('unbound-parent' not in sequence for sequence, _ in paths(out))
    assert len(out.results) == 4


def test_denied_model_relation_cannot_supply_positive_common_ancestry():
    source = small()
    assert_count(count(run(source)[0]), 1)
    h.cases.by_id(source, 'right')['data']['polarity'] = 'denied'
    out = run(source)[0]
    assert_count(count(out), 0)
    assert not out.facts.common_ancestors
    assert all('right' not in edge_refs for unused, edge_refs in paths(out))


def test_model_history_does_not_cross_selected_dependency_dimension():
    source = small()
    assert_count(count(run(source)[0]), 1)
    out = run(source, dimension='analytical_method')[0]
    assert_count(count(out), 0)
    assert_count(count(out, FIELDS[1]), 1)
    assert not out.facts.common_ancestors
    assert all(row.ref.scope.dependency_dimension == 'analytical_method' for row in out.results)


def test_claim_scoped_and_inquiry_only_chain_excludes_another_claims_parent():
    source = small(edges=(('left', 'model_derived_from', 'model', 'model3'),
        ('right', 'model_derived_from', 'model2', 'model3'),
        ('generic-tail', 'trained_on', 'model3', 'dataset'),
        ('wrong-claim', 'trained_on', 'model', 'artifact2'),
        ('other-side', 'trained_on', 'model2', 'artifact2')))
    h.cases.by_id(source, 'generic-tail')['scope']['claim_refs'] = []
    h.cases.by_id(source, 'other-side')['scope']['claim_refs'] = []
    h.cases.by_id(source, 'wrong-claim')['scope']['claim_refs'] = ['claim2']
    source['inquiries'][0]['target_claim_refs'].append('claim2')
    h.cases.by_id(source, 'artifact2')['data']['artifact_kind'] = 'dataset'
    out = run(source)[0]
    assert_count(count(out), 2)
    assert identifiers(out.facts.common_ancestors) == ('dataset', 'model3')
    assert (('model', 'model3', 'dataset'), ('left', 'generic-tail')) in paths(out)
    assert (('model2', 'model3', 'dataset'), ('right', 'generic-tail')) in paths(out)
    assert all('wrong-claim' not in edge_refs for unused, edge_refs in paths(out))


def test_explicit_relation_subset_is_not_widened_by_evaluator_owner():
    source = small()
    source['assertions'].extend([
        h.relation('left-training', 'trained_on', 'model', 'dataset', dimension='model_ancestry'),
        h.relation('right-training', 'trained_on', 'model2', 'dataset', dimension='model_ancestry')])
    assert_count(count(run(source)[0]), 2)
    out = run(source, relation_types=('trained_on',))[0]
    assert_count(count(out), 1)
    assert identifiers(out.facts.common_ancestors) == ('dataset',)
    assert (('model', 'dataset'), ('left-training',)) in paths(out)
    assert (('model2', 'dataset'), ('right-training',)) in paths(out)


@pytest.mark.parametrize('dimensions', ((), ('analytical_method',)))
def test_unselected_dimension_cannot_produce_available_model_comparison(dimensions):
    source = small()
    source['inquiries'][0]['dependency_dimensions'] = list(dimensions)
    snapshot = h.prepared(source)
    owner, job = h.job_pair()
    with pytest.raises(TypeError):
        evaluator._evaluator_lineage(snapshot, context(source), owner.witnesses, job)


@pytest.mark.parametrize('view', ('model_evaluation', 'material_transformation'))
def test_unknown_role_time_does_not_become_time_specific_available_comparison(view):
    source = small()
    assert_count(count(run(source)[0]), 1)
    stamp = _Node('TimeValue', _Object(tuple(sorted({
        'state': 'known', 'value': '2026-01-10T13:00:00Z', 'precision': 'instant'}.items()))))
    changes = {}
    if view == 'material_transformation':
        h.cases.by_id(source, 'evaluation')['data']['role_bindings'] = [
            binding('reference_answer', 'artifact'), binding('rubric', 'artifact2')]
        changes = dict(roles=('reference_answer', 'rubric'), dimension='evaluation_rubric',
                       relation_types=('copies',))
    out = run(source, temporal_basis='time_specific', requested_time=stamp, view=view, **changes)[0]
    assert_count(count(out), None, state='unavailable', reasons=('time_applicability_unknown',))
    assert not out.facts.roles_complete
    assert payload(out)
    assert next(c for c in leaf(out, FIELDS[0]).check_refs if c.check_id == 'PC14').state != 'met'


@pytest.mark.parametrize('remaining', (25, 2500))
def test_interrupted_search_never_returns_completed_empty_overlap(remaining, monkeypatch):
    monkeypatch.setattr(resources, 'monotonic_ns', lambda: 100)
    source = small(); snapshot = h.prepared(source); ctx = context(source)
    owner, job = h.job_pair(); ledger = owner.witnesses
    job.charge(1_000_000 - job.used - remaining)
    with pytest.raises(_AnalysisAborted) as stopped:
        evaluator._evaluator_lineage(snapshot, ctx, ledger, job)
    assert stopped.value.limit_id == 'WU9-L11'
    assert stopped.value.stop.input_state == 'accepted'
    with pytest.raises(_AnalysisAborted) as repeated:
        evaluator._evaluator_lineage(snapshot, ctx, ledger, job)
    assert repeated.value is stopped.value


def test_results_are_immutable_and_foreign_witness_ledger_cannot_supply_proofs():
    source = small(); original = copy.deepcopy(source)
    out, snapshot, owner, job = run(source)
    assert source == original
    for obj, attr in ((out, 'results'), (out.facts, 'common_ancestors'), (out.results[0].value, 'value')):
        with pytest.raises((FrozenInstanceError, AttributeError)):
            setattr(obj, attr, ())
    other, unused = h.job_pair()
    for ledger in (other.witnesses, _WitnessLedger(owner.witnesses.port)):
        with pytest.raises(TypeError):
            evaluator._evaluator_lineage(snapshot, context(source), ledger, job)
    assert other.witnesses._retained_witnesses == 0


def test_invocation_witness_quota_stops_before_complete_overlap_claim(monkeypatch):
    monkeypatch.setattr(resources, 'monotonic_ns', lambda: 100)
    source = small(); snapshot = h.prepared(source); ctx = context(source)
    owner, job = h.job_pair(); ledger = owner.witnesses
    ledger.retain(ledger.reserve(witnesses=20_000, members=0))
    with pytest.raises(_AnalysisAborted) as stopped:
        evaluator._evaluator_lineage(snapshot, ctx, ledger, job)
    assert stopped.value.limit_id == 'WU9-L13'
    assert ledger._retained_witnesses == 20_000
    with pytest.raises(_AnalysisAborted) as repeated:
        evaluator._evaluator_lineage(snapshot, ctx, ledger, job)
    assert repeated.value is stopped.value


def test_permuted_records_and_bindings_preserve_exact_rolepair_membership():
    source = small()
    expected = run(source)[0]
    source['records'].reverse(); source['assertions'].reverse()
    h.cases.by_id(source, 'evaluation')['data']['role_bindings'].reverse()
    actual = run(source)[0]
    for out in (expected, actual):
        assert_count(count(out), 1)
        assert_count(count(out, FIELDS[1]), 1)
        assert identifiers(out.facts.common_ancestors) == ('model3',)
        assert {(('model', 'model3'), ('left',)), (('model2', 'model3'), ('right',))} <= paths(out)
