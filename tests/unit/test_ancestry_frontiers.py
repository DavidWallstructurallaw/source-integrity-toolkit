# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Independent W05 M007 represented-gap oracles, never hidden-root totals.

Definitions 22.4, Validation VF021--VF024 and W7-03/15/18 fix different
frontier, terminal and affected-seed units. Output mutants are challenged
only after the matching conforming result has passed its literal oracle.
"""
import copy
import importlib.util
from pathlib import Path

import pytest

spec=importlib.util.spec_from_file_location('sit_w05_origin_test_helpers',Path(__file__).with_name('test_origins.py'))
h=importlib.util.module_from_spec(spec)
spec.loader.exec_module(h)


def shared_unknown(*, expected='evidence_item'):
    predicate='derived_from' if expected=='evidence_item' else 'originates_from'
    source=h.small(edges=(('a-unknown',predicate,'e','unresolved'),
                           ('b-unknown',predicate,'e2','unresolved')),
                   seeds=('e','e2'),roles=(),coverage_state='partial')
    h.cases.by_id(source,'unresolved')['data'].update(expected_kinds=[expected],reason='withheld',
        description='One shared opaque upstream contribution for exact Claim claim acquisition.',
        protected_key='shared-opaque-source')
    return source


def assert_shared_gap(rows,seeds=('e','e2'),*,endpoint='unresolved',reason='withheld',coverage='coverage'):
    assert tuple(rows)==tuple(seeds)
    expected_paths={'e':(('e','unresolved'),('a-unknown',)),
                    'e2':(('e2','unresolved'),('b-unknown',)),
                    'H7-EU':(('H7-EU','H7-UX'),('H7-LU',))}
    for seed in seeds:
        row=rows[seed]
        assert row['seed_ref']==seed and row['dimension']=='acquisition'
        frontiers={frontier['id']:frontier for frontier in row['frontiers']}
        assert tuple(frontiers)==(endpoint,)
        frontier=frontiers[endpoint]
        assert frontier['kind']=='unresolved_reference'
        assert frontier['data']['expected_kinds']==['evidence_item']
        assert frontier['data']['reason']==reason
        gaps=[gap for gap in row['gaps'] if gap['source']['collection']=='records' and
              gap['source']['identifier']==endpoint]
        assert gaps and any('unknown_endpoint' in gap['reason_codes'] for gap in gaps)
        coverages={item['coverage_ref']:item for item in row['coverage']}
        assert coverage in coverages and coverages[coverage]['qualification_state']!='met'
        paths={(tuple(path['nodes']),tuple(path['assertions'])) for path in row['witness_paths']}
        assert expected_paths[seed] in paths


@pytest.fixture(scope='module')
def shared_run():
    return h.run(shared_unknown())


def test_vf006_m_and_vf021_p_shared_unknown_is_one_frontier_and_zero_reached_origins(shared_run):
    out,facts,_,_=shared_run
    h.assert_count(h.count_view(out,'reached_origin_record_count'),())
    h.assert_count(h.count_view(out,'documentary_origin_boundary_record_count'),())
    h.assert_count(h.count_view(out,'unresolved_frontier_reference_count'),('unresolved',))
    h.assert_count(h.count_view(out,'seed_items_with_unresolved_ancestry_count'),('e','e2'))
    assert h.path_view(facts)=={
        'e':((('e','unresolved'),('a-unknown',)),),
        'e2':((('e2','unresolved'),('b-unknown',)),)}
    assert not hasattr(facts,'unknown_root_count') and not hasattr(facts,'hidden_origin_upper_bound')


def test_vf021_n_output_mutant_cannot_count_one_shared_unknown_twice(shared_run):
    actual=h.count_view(shared_run[0],'unresolved_frontier_reference_count')
    h.assert_count(actual,('unresolved',))
    mutant=copy.deepcopy(actual);mutant['value']=2
    with pytest.raises(AssertionError):h.assert_count(mutant,('unresolved',))


def test_vf021_m_h7_complete_acquisition_frontier_inventory_is_explicit_zero():
    source=h.hero();out,facts,_,_=h.run(source)
    h.assert_count(h.count_view(out,'unresolved_frontier_reference_count'),())
    h.assert_count(h.count_view(out,'unqualified_terminal_record_count'),())
    h.assert_count(h.count_view(out,'seed_items_with_unresolved_ancestry_count'),())
    assert tuple(trace.seed.identifier for trace in facts.seed_traces)==h.H7_SEEDS
    # The unrelated model-history gap remains in the admitted source.
    model=h.cases.by_id(source,'H7-COV-MODEL')
    assert model['data']['details']['state']=='partial'


def test_vf021_b_typed_unknown_origin_is_one_reference_not_an_origin_record():
    out=h.run(shared_unknown(expected='origin_event'))[0]
    h.assert_count(h.count_view(out,'unresolved_frontier_reference_count'),('unresolved',))
    h.assert_count(h.count_view(out,'reached_origin_record_count'),())
    h.assert_count(h.count_view(out,'seed_items_with_unresolved_ancestry_count'),('e','e2'))


def test_vf022_p_and_m_missing_qualification_leaves_one_visible_terminal():
    source=h.small(roles=());out=h.run(source)[0]
    h.assert_count(h.count_view(out,'reached_origin_record_count'),('origin',))
    h.assert_count(h.count_view(out,'unqualified_terminal_record_count'),('origin',))
    h.assert_count(h.count_view(out,'documentary_origin_boundary_record_count'),())
    h.assert_count(h.count_view(out,'seed_items_with_unresolved_ancestry_count'),('e',))
    assert 'unqualified_origin_boundary' in h.tokens(h.disclosures(out,'ancestry_gap_disclosures'))


def test_vf022_n_output_mutant_cannot_promote_a_parentless_terminal_to_documentary_root():
    out=h.run(h.small(roles=()))[0]
    baseline=h.count_view(out,'documentary_origin_boundary_record_count')
    h.assert_count(baseline,())
    h.assert_count(h.count_view(out,'unqualified_terminal_record_count'),('origin',))
    mutant=copy.deepcopy(baseline);mutant.update(value=1,members=('origin',))
    with pytest.raises(AssertionError):h.assert_count(mutant,())


def test_vf022_b_shared_terminal_is_one_record_with_two_affected_seeds():
    source=h.small(edges=(('a-root','originates_from','e','origin'),
                          ('b-root','originates_from','e2','origin')),seeds=('e','e2'),roles=())
    out=h.run(source)[0]
    h.assert_count(h.count_view(out,'unqualified_terminal_record_count'),('origin',))
    h.assert_count(h.count_view(out,'seed_items_with_unresolved_ancestry_count'),('e','e2'))
    h.assert_count(h.count_view(out,'unresolved_frontier_reference_count'),())


def test_vf022_b_explicit_scope_cut_is_separate_from_an_unqualified_terminal():
    source=h.small(roles=(('origin','scope_cut'),));out=h.run(source)[0]
    h.assert_count(h.count_view(out,'unqualified_terminal_record_count'),())
    h.assert_count(h.count_view(out,'seed_items_with_unresolved_ancestry_count'),())
    h.assert_count(h.count_view(out,'documentary_origin_boundary_record_count'),())
    assert 'scope_cut' in h.tokens(h.disclosures(out,'origin_boundary_disclosures'))


def test_vf023_p_h7_v02_only_added_seed_is_affected_and_original_origins_survive():
    out,facts,_,_=h.run(h.hero('H7-V02'))
    h.assert_count(h.count_view(out,'reached_origin_record_count'),('H7-O1','H7-O2'))
    h.assert_count(h.count_view(out,'documentary_origin_boundary_record_count'),('H7-O1','H7-O2'))
    h.assert_count(h.count_view(out,'unresolved_frontier_reference_count'),('H7-UX',))
    h.assert_count(h.count_view(out,'seed_items_with_unresolved_ancestry_count'),('H7-EU',))
    paths=h.path_view(facts)
    for seed,path in h.H7_PATHS.items():assert path in paths[seed]
    assert (('H7-EU','H7-UX'),('H7-LU',)) in paths['H7-EU']


def test_vf023_n_output_mutant_cannot_copy_frontier_count_into_affected_seed_count(shared_run):
    h.assert_count(h.count_view(shared_run[0],'unresolved_frontier_reference_count'),('unresolved',))
    baseline=h.count_view(shared_run[0],'seed_items_with_unresolved_ancestry_count')
    h.assert_count(baseline,('e','e2'))
    mutant=copy.deepcopy(baseline);mutant['value']=1
    with pytest.raises(AssertionError):h.assert_count(mutant,('e','e2'))


def test_vf023_m_all_selected_ancestry_unknown_keeps_the_completed_seed_population(shared_run):
    h.assert_count(h.count_view(shared_run[0],'seed_items_with_unresolved_ancestry_count'),('e','e2'))
    assert_shared_gap(h.disclosures(shared_run[0],'ancestry_gap_disclosures'))
    assert set(h.result_paths(h.leaf(shared_run[0],'ancestry_gap_disclosures'),shared_run[1]))=={
        (('e','unresolved'),('a-unknown',)),(('e2','unresolved'),('b-unknown',))}


def test_vf023_b_distant_unknown_does_not_erase_the_known_immediate_copy():
    source=h.small(edges=(('known-copy','copies','e','e2'),
                          ('upstream-gap','derived_from','e2','unresolved')),
                   roles=(),coverage_state='partial')
    h.cases.by_id(source,'unresolved')['data'].update(expected_kinds=['evidence_item'],
        description='Missing upstream contribution for exact Claim claim.')
    out,facts,_,_=h.run(source)
    h.assert_count(h.count_view(out,'seed_items_with_unresolved_ancestry_count'),('e',))
    h.assert_count(h.count_view(out,'unresolved_frontier_reference_count'),('unresolved',))
    assert h.reached_edge_ids(facts,'e')=={'known-copy','upstream-gap'}
    assert (('e','e2','unresolved'),('known-copy','upstream-gap')) in h.path_view(facts)['e']
    # W07 owns the immediate fraction; W05 preserves the paid first edge.
    trace=facts.seed_traces[0]
    first=[edge for edge in trace.reachability.edges if edge.source.identifier=='e']
    assert len(first)==1 and first[0].predicate=='copies' and first[0].target.kind=='evidence_item'


def test_vf024_p_h7_v02_keeps_gap_reason_expected_kind_branch_and_coverage():
    out,facts,_,_=h.run(h.hero('H7-V02'))
    rows=h.disclosures(out,'ancestry_gap_disclosures')
    assert_shared_gap(rows,('H7-EU',),endpoint='H7-UX',reason='not_recorded',coverage='H7-COV-ACQ')
    assert (('H7-EU','H7-UX'),('H7-LU',)) in h.path_view(facts)['H7-EU']
    assert (('H7-EU','H7-UX'),('H7-LU',)) in h.result_paths(h.leaf(out,'ancestry_gap_disclosures'),facts)


def test_vf024_n_output_mutants_cannot_split_opaque_identity_or_erase_the_gap(shared_run):
    rows=h.disclosures(shared_run[0],'ancestry_gap_disclosures')
    assert_shared_gap(rows)
    def rename(value,old,new):
        if type(value) is dict:return {key:rename(item,old,new) for key,item in value.items()}
        if type(value) is list:return [rename(item,old,new) for item in value]
        return new if value==old else value
    mutant=copy.deepcopy(rows)
    for seed in ('e','e2'):mutant[seed]=rename(mutant[seed],'unresolved','private-'+seed)
    with pytest.raises(AssertionError):assert_shared_gap(mutant)
    with pytest.raises(AssertionError):assert_shared_gap({})


def test_vf024_n_output_mutant_cannot_move_required_expected_kind_into_free_text(shared_run):
    rows=h.disclosures(shared_run[0],'ancestry_gap_disclosures');assert_shared_gap(rows)
    mutant=copy.deepcopy(rows)
    frontier=mutant['e']['frontiers'][0]
    frontier['data']['description']+=' Expected kind evidence_item retained only as free text.'
    frontier['data']['expected_kinds']=[]
    with pytest.raises(AssertionError):assert_shared_gap(mutant)


def test_vf024_m_gap_only_locator_stays_inert_and_preserves_shared_unknown(monkeypatch):
    import socket
    import urllib.request
    source=shared_unknown()
    support=h.cases.by_id(source,'support')
    support.update(reference_kind='external_locator',availability='locator_only',excerpt=None,
        locator='https://example.invalid/INERT_ORIGIN_PAYLOAD')
    def forbidden(*args,**kwargs):raise AssertionError('origin attempted network access')
    monkeypatch.setattr(socket,'socket',forbidden)
    monkeypatch.setattr(urllib.request,'urlopen',forbidden)
    out=h.run(source)[0]
    h.assert_count(h.count_view(out,'unresolved_frontier_reference_count'),('unresolved',))
    h.assert_count(h.count_view(out,'seed_items_with_unresolved_ancestry_count'),('e','e2'))
    assert_shared_gap(h.disclosures(out,'ancestry_gap_disclosures'))


def test_vf024_b_protected_shared_endpoint_preserves_opaque_commonality(shared_run):
    rows=h.disclosures(shared_run[0],'ancestry_gap_disclosures')
    assert_shared_gap(rows)
    assert all(row['frontiers'][0]['data']['protected_key']=='shared-opaque-source' for row in rows.values())
    assert all('hidden_origin_upper_bound' not in h.tokens(row) for row in rows.values())


def test_coverage_gap_without_unknown_node_still_affects_the_seed():
    source=h.small(coverage_state='partial');out=h.run(source)[0]
    h.assert_count(h.count_view(out,'unresolved_frontier_reference_count'),())
    h.assert_count(h.count_view(out,'seed_items_with_unresolved_ancestry_count'),('e',))
    assert 'upstream_coverage_incomplete' in h.tokens(h.disclosures(out,'ancestry_gap_disclosures'))


def test_origin_only_coverage_cannot_establish_all_prior_evidence_parentage():
    source=h.small();coverage=h.cases.by_id(source,'coverage')
    coverage['data']['subject_refs']=['origin']
    coverage['data']['details'].update(member_refs=['origin'],relation_types=['depends_on'])
    out=h.run(source)[0]
    h.assert_count(h.count_view(out,'reached_origin_record_count'),('origin',))
    h.assert_count(h.count_view(out,'seed_items_with_unresolved_ancestry_count'),('e',))
    assert 'upstream_coverage_incomplete' in h.tokens(h.disclosures(out,'ancestry_gap_disclosures'))
