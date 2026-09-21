# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Independent mechanical oracles: plan 3.2/W04, architecture 18.2/19,
lineage 10/18.2 and governance 22.5. Tool-owned tiny projections do not claim
structural admission, documentary qualification, independent origins or HHI.
"""
from dataclasses import FrozenInstanceError, replace
import importlib.util
from itertools import permutations
from pathlib import Path

import pytest

from source_integrity_toolkit.contracts.bundle import _Object
from source_integrity_toolkit.contracts.evidence import _PreparedBundle, _QualificationContext, _SourceAddress
from source_integrity_toolkit.contracts.execution import _AnalysisAborted
from source_integrity_toolkit.graph.projections import _GraphNode, _GraphEdge, _Projection, _project
from source_integrity_toolkit.graph import traversal as t
from source_integrity_toolkit.runtime import resources
from source_integrity_toolkit.runtime.boundary import _prepare_value


def fixture(specs, *, node_ids=(), unknown=(), extra_observations=(), reverse_nodes=False, reverse_edges=False):
    """Explicit trusted mechanics fixture, with no claimed PC04 execution."""
    identifiers=set(node_ids)
    for source,target,identity in specs: identifiers.update((source,target))
    for source,target,identity,reason in extra_observations: identifiers.update((source,target))
    nodes={name:_GraphNode('records',name,'unresolved_reference' if name in unknown else 'origin_event',
                           ('records',name)) for name in sorted(identifiers)}
    edges=tuple(_GraphEdge(nodes[a],nodes[b],('assertions',identifier,'','records',b),
                          _SourceAddress('assertions',identifier),'depends_on',True,())
                for a,b,identifier in specs)
    observed=tuple(_GraphEdge(nodes[a],nodes[b],('assertions',identifier,'','records',b),
                              _SourceAddress('assertions',identifier),'depends_on',False,(reason,))
                   for a,b,identifier,reason in extra_observations)
    context=_QualificationContext('I',('C',),tuple(sorted(identifiers)),'acquisition',
                                  'snapshot_structural',None,'upstream_history',('depends_on',),'claim_origin')
    empty=_Object(())
    prepared=_PreparedBundle(empty,'constructed_value',(),(),(),(),empty)
    owner=resources._new_analysis_budget();owner.record_input_acceptance();job=owner.start_job()
    node_rows=tuple(nodes.values())
    graph=_Projection(prepared,context,tuple(reversed(node_rows)) if reverse_nodes else node_rows,
                      tuple(reversed(edges)) if reverse_edges else edges,edges+observed,(),None,job)
    return graph,nodes,owner,job


def edge_ids(path):
    return tuple(edge.source_ref.record_id for edge in path.edges)


def node_ids(rows):
    return tuple(node.identifier for node in rows)


def test_shortest_distance_precedes_lexicographic_preference():
    graph,nodes,owner,job=fixture((('S','A','a'),('A','T','b'),('S','T','z')))
    path=t._shortest_path(graph,nodes['S'],nodes['T'],job)
    assert edge_ids(path)==('z',) and node_ids(path.nodes)==('S','T')
    assert path.graph is graph and path.start is nodes['S'] and path.target is nodes['T']
    assert not any(hasattr(path,name) for name in ('independent','documented_origin','result_state','value'))


@pytest.mark.parametrize('reverse_nodes,reverse_edges',[(False,False),(False,True),(True,False),(True,True)])
def test_equal_paths_compare_complete_edge_sequence_not_last_parent_or_last_edge(reverse_nodes,reverse_edges):
    specs=(('S','A','z-first'),('A','T','a-last'),('S','B','a-first'),('B','T','z-last'))
    graph,nodes,owner,job=fixture(specs,reverse_nodes=reverse_nodes,reverse_edges=reverse_edges)
    path=t._shortest_path(graph,nodes['S'],nodes['T'],job)
    # A is the earlier local parent and its final edge is earlier, but the
    # complete path through B starts with a-first and must win.
    assert edge_ids(path)==('a-first','z-last') and node_ids(path.nodes)==('S','B','T')


def test_complete_prefix_rank_survives_several_layers_and_converging_paths():
    graph,nodes,owner,job=fixture((('S','L','a-first'),('S','R','b-first'),
        ('L','Z','z-middle'),('R','A','a-middle'),('Z','M','z-merge'),('A','M','a-merge'),('M','T','last')))
    search=t._ranked_search(graph,nodes['S'],job)
    path=t._path_from_search(search,nodes['T'],job)
    assert edge_ids(path)==('a-first','z-middle','z-merge','last')
    z=t._node_index(search.nodes,nodes['Z'],job);a=t._node_index(search.nodes,nodes['A'],job)
    assert search.distances[z]==search.distances[a]==2 and search.ranks[z]<search.ranks[a]


@pytest.mark.parametrize('order',list(permutations(range(4))))
def test_each_small_diamond_edge_permutation_has_the_same_source_bound_witness(order):
    original=(('S','A','z-first'),('A','T','a-last'),('S','B','a-first'),('B','T','z-last'))
    graph,nodes,owner,job=fixture(tuple(original[index] for index in order))
    assert edge_ids(t._shortest_path(graph,nodes['S'],nodes['T'],job))==('a-first','z-last')


def test_parallel_assertion_ids_are_not_deduplicated_by_endpoints():
    graph,nodes,owner,job=fixture((('S','T','z-assertion'),('S','T','a-assertion')))
    assert edge_ids(t._shortest_path(graph,nodes['S'],nodes['T'],job))==('a-assertion',)
    reach=t._reachable(graph,(nodes['S'],),job)
    assert node_ids(reach.nodes)==('S','T')
    assert tuple(edge.source_ref.record_id for edge in reach.edges)==('a-assertion','z-assertion')


def test_canonical_record_link_selector_participates_without_inventing_assertions():
    graph,nodes,owner,job=fixture((),node_ids=('S','T'))
    rows=[]
    for selector in ('data.role_bindings.judge.object_ref','data.role_bindings.candidate.object_ref'):
        source=_SourceAddress('records','evaluation',selector)
        rows.append(_GraphEdge(nodes['S'],nodes['T'],('records','evaluation',selector,'records','T'),
                               source,None,True,()))
    graph=replace(graph,edges=tuple(rows),observations=tuple(rows))
    path=t._shortest_path(graph,nodes['S'],nodes['T'],job)
    assert path.edges[0].source_ref.collection=='records'
    assert path.edges[0].source_ref.record_id=='evaluation'
    assert path.edges[0].source_ref.selector=='data.role_bindings.candidate.object_ref'
    assert len(t._reachable(graph,(nodes['S'],),job).edges)==2


def test_shared_root_diamond_counts_reachable_nodes_not_paths_and_keeps_both_parents():
    graph,nodes,owner,job=fixture((('S','A','sa'),('S','B','sb'),('A','O','ao'),('B','O','bo')))
    path=t._shortest_path(graph,nodes['S'],nodes['O'],job)
    reach=t._reachable(graph,(nodes['S'],),job)
    assert edge_ids(path)==('sa','ao')
    assert node_ids(reach.nodes)==('A','B','O','S') and node_ids(reach.terminals)==('O',)
    assert tuple(edge.source_ref.record_id for edge in reach.edges)==('ao','bo','sa','sb')
    assert not hasattr(reach,'independent_root_count')


def test_multiple_terminals_and_late_conflict_are_not_erased_by_a_short_representative():
    graph,nodes,owner,job=fixture((('S','O1','short'),('S','A','other'),('A','O2','late')),
        extra_observations=(('A','O2','denial','premise_disputed'),('A','U','time-gap','time_applicability_unknown')),
        unknown=('U',))
    assert edge_ids(t._shortest_path(graph,nodes['S'],nodes['O1'],job))==('short',)
    reach=t._reachable(graph,(nodes['S'],),job)
    assert node_ids(reach.terminals)==('O1','O2') and len(reach.edges)==3
    assert {'denial','time-gap'} <= {edge.source_ref.record_id for edge in reach.observations}
    assert 'U' not in node_ids(reach.nodes)  # A noneligible possibility is still disclosed.
    assert node_ids(reach.frontiers)==()


def test_unknown_reached_endpoint_is_a_frontier_and_never_a_traversal_intermediate():
    # The raw fixture even contains an outgoing unknown edge. A real projection
    # additionally marks that edge ineligible; traversal independently stops.
    graph,nodes,owner,job=fixture((('S','U','to-gap'),('U','T','unsupported-continuation')),
                                 unknown=('U',))
    assert edge_ids(t._shortest_path(graph,nodes['S'],nodes['U'],job))==('to-gap',)
    assert t._shortest_path(graph,nodes['S'],nodes['T'],job) is None
    reach=t._reachable(graph,(nodes['S'],),job)
    assert node_ids(reach.nodes)==('S','U') and node_ids(reach.frontiers)==('U',)
    assert reach.terminals==() and tuple(e.source_ref.record_id for e in reach.edges)==('to-gap',)
    assert 'unsupported-continuation' in {e.source_ref.record_id for e in reach.observations}


def test_cycle_with_exit_remains_finite_and_all_cycle_edges_survive_path_selection():
    graph,nodes,owner,job=fixture((('S','A','sa'),('A','B','ab'),('B','A','ba'),('B','O','bo')))
    path=t._shortest_path(graph,nodes['S'],nodes['O'],job)
    reach=t._reachable(graph,(nodes['S'],),job)
    assert edge_ids(path)==('sa','ab','bo') and len(path.nodes)==len(set(node_ids(path.nodes)))
    assert {e.source_ref.record_id for e in reach.edges}=={'sa','ab','ba','bo'}
    assert node_ids(reach.terminals)==('O',)


def test_zero_edge_self_path_is_not_a_cycle_witness_and_missing_nodes_are_not_absence():
    graph,nodes,owner,job=fixture((('S','S','self-loop'),),node_ids=('T',))
    path=t._shortest_path(graph,nodes['S'],nodes['S'],job)
    assert path.nodes==(nodes['S'],) and path.edges==()
    assert t._shortest_path(graph,nodes['S'],nodes['T'],job) is None
    absent=_GraphNode('records','missing','origin_event',('records','missing'))
    with pytest.raises(TypeError): t._shortest_path(graph,nodes['S'],absent,job)
    assert tuple(e.source_ref.record_id for e in t._reachable(graph,(nodes['S'],),job).edges)==('self-loop',)


def test_multi_start_and_empty_start_queries_preserve_their_exact_finite_scope():
    graph,nodes,owner,job=fixture((('S','O','so'),('A','O','ao')),node_ids=('isolated',))
    reach=t._reachable(graph,(nodes['S'],nodes['A']),job)
    assert node_ids(reach.starts)==('A','S') and node_ids(reach.nodes)==('A','O','S')
    assert reach.graph is graph and reach.graph.context is graph.context
    empty=t._reachable(graph,(),job)
    assert empty.starts==empty.nodes==empty.edges==empty.frontiers==empty.observations==()
    with pytest.raises(TypeError): t._reachable(graph,(nodes['S'],nodes['S']),job)


def test_allowed_component_nodes_constrain_search_without_altering_the_source_projection():
    graph,nodes,owner,job=fixture((('S','A','sa'),('A','T','at'),('S','B','sb'),('B','T','bt')))
    path=t._shortest_path(graph,nodes['S'],nodes['T'],job,allowed_nodes=(nodes['T'],nodes['B'],nodes['S']))
    assert edge_ids(path)==('sb','bt') and len(graph.edges)==4
    assert t._shortest_path(graph,nodes['S'],nodes['T'],job,allowed_nodes=(nodes['S'],)) is None
    with pytest.raises(TypeError): t._ranked_search(graph,nodes['S'],job,allowed_nodes=(nodes['A'],))


POSSIBLE=(('A','B','z-ab'),('A','C','b-ac'),('B','A','c-ba'),
          ('B','C','a-bc'),('C','A','d-ca'),('C','B','e-cb'))


def independent_simple_path_oracle(specs,start,target):
    # Tests only: enumerate the at-most-three-node fixture's simple paths.
    candidates=[]
    def visit(current,visited,path):
        if current==target:
            keys=tuple(('assertions',identity,'','records',right) for left,right,identity in path)
            candidates.append((len(path),keys,tuple(identity for left,right,identity in path)))
            return
        for left,right,identity in specs:
            if left==current and right not in visited:
                visit(right,visited|{right},path+((left,right,identity),))
    visit(start,{start},())
    return None if not candidates else min(candidates)[2]


@pytest.mark.parametrize('mask',range(64))
def test_all_three_node_directed_graphs_match_an_independent_simple_path_oracle(mask):
    specs=tuple(edge for index,edge in enumerate(POSSIBLE) if mask & (1<<index))
    graph,nodes,owner,job=fixture(specs,node_ids=('A','B','C'))
    expected=independent_simple_path_oracle(specs,'A','C')
    actual=t._shortest_path(graph,nodes['A'],nodes['C'],job)
    assert (None if actual is None else edge_ids(actual))==expected


@pytest.mark.parametrize('shape',['deep','wide','many_walks'])
def test_finite_large_shapes_use_bounded_passes_instead_of_recursion_or_walk_enumeration(shape):
    if shape=='deep':
        specs=tuple((f'N{i:04}',f'N{i+1:04}',f'edge-{i:04}') for i in range(384))
        start,target,expected_nodes,expected_edges='N0000','N0384',385,384
    elif shape=='wide':
        specs=tuple(edge for i in range(160) for edge in
                    (('S',f'B{i:04}',f'first-{i:04}'),(f'B{i:04}','T',f'last-{i:04}')))
        start,target,expected_nodes,expected_edges='S','T',162,2
    else:
        specs=tuple((f'L{layer:02}-{left}',f'L{layer+1:02}-{right}',f'e-{layer:02}-{left}-{right}')
                    for layer in range(20) for left in range(3) for right in range(3))
        start,target,expected_nodes,expected_edges='L00-0','L20-2',61,20
    graph,nodes,owner,job=fixture(specs)
    path=t._shortest_path(graph,nodes[start],nodes[target],job)
    reach=t._reachable(graph,(nodes[start],),job)
    assert len(path.edges)==expected_edges and len(reach.nodes)==expected_nodes
    assert len(path.nodes)==len(set(node_ids(path.nodes)))
    assert job.used>0 and job.used<=1_000_000


def test_same_graph_queries_are_paid_each_time_and_results_are_frozen():
    graph,nodes,owner,job=fixture((('S','T','edge'),))
    before=(owner.used,job.used)
    first=t._shortest_path(graph,nodes['S'],nodes['T'],job)
    after_first=job.used
    second=t._shortest_path(graph,nodes['S'],nodes['T'],job)
    assert job.used>after_first>before[1] and owner.used-before[0]==job.used-before[1]
    assert first is not second and edge_ids(first)==edge_ids(second)==('edge',)
    with pytest.raises(FrozenInstanceError): first.edges=()
    with pytest.raises(TypeError): first.nodes[0]=nodes['T']


@pytest.mark.parametrize('field',['starts','nodes','edges','frontiers','terminals','observations'])
def test_complete_reachability_transport_refuses_mutable_replacement_containers(field):
    graph,nodes,owner,job=fixture((('S','T','edge'),))
    reach=t._reachable(graph,(nodes['S'],),job)
    assert node_ids(reach.nodes)==('S','T')
    with pytest.raises(TypeError): replace(reach,**{field:list(getattr(reach,field))})


@pytest.mark.parametrize('field',['nodes','distances','ranks','predecessors'])
def test_ranked_search_transport_refuses_mutable_tables(field):
    graph,nodes,owner,job=fixture((('S','T','edge'),))
    search=t._ranked_search(graph,nodes['S'],job)
    assert edge_ids(t._path_from_search(search,nodes['T'],job))==('edge',)
    with pytest.raises(TypeError): replace(search,**{field:list(getattr(search,field))})


@pytest.mark.parametrize('seam',['path','reachable'])
def test_interruption_before_completion_never_returns_absence_or_a_partial_population(seam):
    graph,nodes,owner,job=fixture((('S','A','sa'),),node_ids=('T',))
    job.charge(999_995)
    with pytest.raises(_AnalysisAborted) as stopped:
        t._shortest_path(graph,nodes['S'],nodes['T'],job) if seam=='path' else t._reachable(graph,(nodes['S'],),job)
    assert stopped.value.limit_id=='WU9-L11' and stopped.value.stop.execution_state=='interrupted'
    before=job.used
    with pytest.raises(_AnalysisAborted) as repeated:
        t._shortest_path(graph,nodes['S'],nodes['T'],job) if seam=='path' else t._reachable(graph,(nodes['S'],),job)
    assert repeated.value is stopped.value and job.used==before


def test_projection_and_ranked_search_cannot_become_cross_job_semantic_caches():
    graph,nodes,owner,job=fixture((('S','T','edge'),))
    search=t._ranked_search(graph,nodes['S'],job)
    owner.finish_job(job);new_job=owner.start_job()
    with pytest.raises(TypeError): t._shortest_path(graph,nodes['S'],nodes['T'],new_job)
    with pytest.raises(TypeError): t._path_from_search(search,nodes['T'],new_job)
    owner.finish_job(new_job);finalizer=owner.begin_finalization()
    with pytest.raises((TypeError,AttributeError)): t._reachable(graph,(nodes['S'],),finalizer)


def test_actual_projection_preserves_the_bound_scope_and_assertion_identity_in_the_path():
    root=Path(__file__).resolve().parents[2]
    spec=importlib.util.spec_from_file_location('sit_w04_traversal_records',root/'tests/contract/test_typed_records.py')
    cases=importlib.util.module_from_spec(spec);spec.loader.exec_module(cases)
    value=cases.pool();value['assertions']=[cases.relation('originates_from')]
    prepared=_prepare_value(value)
    assert type(prepared) is _PreparedBundle
    context=_QualificationContext('inquiry',('claim',),('e','origin'),'acquisition','snapshot_structural',None,
                                  'upstream_history',('originates_from',),'claim_origin')
    owner=resources._new_analysis_budget();owner.record_input_acceptance();job=owner.start_job()
    graph=_project(prepared,context,job)
    nodes={node.identifier:node for node in graph.nodes}
    path=t._shortest_path(graph,nodes['e'],nodes['origin'],job)
    assert edge_ids(path)==('r-originates_from',)
    assert path.graph.context is context and path.graph.prepared is prepared
    assert path.edges[0].source_ref.collection=='assertions'
    assert not hasattr(path,'documentary_qualified')
