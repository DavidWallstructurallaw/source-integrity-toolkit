# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Independent Lineage 8/10/18.2 view and canonical-link oracles.

These component tests use actual admission and a tool-owned analysis job.
They do not execute a full analytical pipeline or certify source conclusions.
"""
import copy
from dataclasses import FrozenInstanceError, replace
import importlib.util
from pathlib import Path

import pytest
from source_integrity_toolkit.contracts.evidence import _PreparedBundle, _QualificationContext
from source_integrity_toolkit.contracts.bundle import _Object
from source_integrity_toolkit.graph import projections
from source_integrity_toolkit.runtime.boundary import _prepare_value
from source_integrity_toolkit.runtime.resources import _new_analysis_budget

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('sit_w04_graph_cases', ROOT/'tests/contract/test_typed_records.py')
cases = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cases)
VIEWS = ('citation','material_transformation','claim_origin','model_evaluation','organizational',
         'stance_contestation','correction_routing','correction_outcomes','pipeline_stages',
         'assertion_assurance','succession')
# Frozen registry expectations, not populated from product constants.
PREDICATES = {
    'supports':'stance_contestation','contradicts':'stance_contestation','describes':'stance_contestation',
    'qualifies':'stance_contestation','contextualizes':'stance_contestation','corroborates':'stance_contestation',
    'cites':'citation','derived_from':'claim_origin','copies':'claim_origin','syndicated_from':'claim_origin',
    'summarizes':'claim_origin','translates':'claim_origin','quotes':'claim_origin',
    'originates_from':'claim_origin','depends_on':'claim_origin','generated_by':'model_evaluation',
    'published_by':None,'model_derived_from':'model_evaluation','trained_on':'model_evaluation',
    'owned_by':'organizational','retrieved_from':'material_transformation','propagates_to':'correction_routing',
    'supersedes':'succession','same_identity_as':None,
}
DIMENSIONS=('acquisition','analytical_method','model_ancestry','evaluation_rubric','organizational_control')


def admitted(source):
    answer=_prepare_value(source)
    assert type(answer) is _PreparedBundle
    return answer


def ctx(view,dimension='acquisition',subjects=(),claims=('claim',)):
    predicates=tuple(predicate for predicate,owner in PREDICATES.items() if owner==view)
    if view=='material_transformation':
        predicates=('derived_from','copies','syndicated_from','summarizes','translates','quotes','retrieved_from')
    return _QualificationContext('inquiry',claims,subjects,dimension,'snapshot_structural',None,None,predicates,view,())


def project(snapshot,context):
    owner=_new_analysis_budget();owner.record_input_acceptance();job=owner.start_job()
    before=(owner.used,job.used)
    graph=projections._project(snapshot,context,job)
    assert owner.used-before[0]==job.used-before[1]>0
    assert graph.prepared is snapshot and graph.context is context and graph.job_port is job
    return graph,owner,job


@pytest.fixture(scope='module',params=tuple(PREDICATES))
def predicate_case(request):
    source=cases.pool();source['inquiries'][0]['dependency_dimensions']=list(DIMENSIONS)
    relation=cases.relation(request.param);source['assertions']=[relation]
    return request.param,admitted(source),relation['data']['dimension'] or 'acquisition'


@pytest.mark.parametrize('view',VIEWS)
def test_each_of_24_predicates_has_only_its_frozen_view_mapping(predicate_case,view):
    predicate,snapshot,dimension=predicate_case
    graph,owner,job=project(snapshot,ctx(view,dimension))
    found=[edge for edge in graph.edges if edge.predicate==predicate]
    expected=PREDICATES[predicate]==view
    assert bool(found) is expected
    if expected:
        assert len(found)==1
        edge=found[0]
        assert edge.source_ref.collection=='assertions'
        assert edge.source_ref.record_id=='r-'+predicate
        assert edge.source_ref.selector==''
        assert edge.key==('assertions','r-'+predicate,'',edge.target.collection,edge.target.identifier)
        assert edge.source_entity.identifier=='r-'+predicate
    if predicate in ('published_by','same_identity_as'):
        assert any(item.identifier=='r-'+predicate for item in graph.annotations)
        assert all(edge.source.identifier!='r-'+predicate for edge in graph.edges)


@pytest.mark.parametrize('predicate',('derived_from','copies','syndicated_from','summarizes','translates','quotes'))
@pytest.mark.parametrize('view',('material_transformation','claim_origin','citation','model_evaluation'))
def test_artifact_transformations_never_become_claim_or_model_ancestry(predicate,view):
    source=cases.pool();relation=cases.relation(predicate)
    relation['data'].update(from_ref='artifact',to_ref='artifact2',dimension=None)
    source['assertions']=[relation]
    graph,_,_=project(admitted(source),ctx(view))
    assert any(edge.predicate==predicate for edge in graph.edges) is (view=='material_transformation')


def test_current_snapshot_declaration_remains_an_attributed_positive_edge():
    source=cases.pool();source['assertions']=[cases.relation('copies')]
    graph,_,_=project(admitted(source),ctx('claim_origin'))
    edge=next(edge for edge in graph.edges if edge.predicate=='copies')
    provenance=dict(edge.source_entity.node.fields.items)['provenance']
    assert dict(provenance.items)['basis_kind']=='declaration'
    assert dict(provenance.items)['evidence_ref_ids'].items==()
    assert not hasattr(graph,'independent_sources') and not hasattr(edge,'verified')


@pytest.mark.parametrize('lifecycle',('active','withdrawn','superseded'))
@pytest.mark.parametrize('polarity',('affirmed','denied'))
def test_current_positive_eligibility_is_separate_from_retained_native_assertion(lifecycle,polarity):
    source=cases.pool();relation=cases.relation('copies')
    relation['lifecycle_state']=lifecycle;relation['lifecycle_basis_ref_ids']=[] if lifecycle=='active' else ['support']
    relation['data']['polarity']=polarity;source['assertions']=[relation]
    graph,_,_=project(admitted(source),ctx('claim_origin'))
    records=[edge for edge in graph.observations if edge.predicate=='copies']
    assert len(records)==1
    assert records[0].eligible is (lifecycle=='active' and polarity=='affirmed')
    native=dict(records[0].source_entity.node.fields.items)
    assert native['lifecycle_state']==lifecycle
    assert dict(native['data'].items)['polarity']==polarity
    assert (records[0] in graph.edges) is records[0].eligible


@pytest.mark.parametrize('availability',('locator_only','withheld','unavailable'))
def test_unsupported_nonactive_label_cannot_create_a_positive_edge(availability):
    source=cases.pool();relation=cases.relation('copies')
    relation['lifecycle_state']='withdrawn';relation['lifecycle_basis_ref_ids']=['support'];source['assertions']=[relation]
    source['evidence_references'][0].update(reference_kind='external_locator',availability=availability,
        locator='https://example.invalid/inert',excerpt=None)
    graph,_,job=project(admitted(source),ctx('claim_origin'))
    edge=next(edge for edge in graph.observations if edge.predicate=='copies')
    assert not edge.eligible and 'documentary_basis_incomplete' in edge.reason_codes
    assert graph.pc04 is None
    assert projections._check_edge_eligibility(graph,(edge,),job).state=='unmet'


def test_relevant_weak_denial_stays_beside_a_disputed_possible_positive_path():
    source=cases.pool();yes=cases.relation('copies');no=copy.deepcopy(yes)
    no['id']='zz-denial';no['data']['polarity']='denied';source['assertions']=[yes,no]
    graph,_,job=project(admitted(source),ctx('claim_origin'))
    positive=next(edge for edge in graph.edges if edge.source_ref.record_id=='r-copies')
    assert 'premise_disputed' in positive.reason_codes
    assert len([edge for edge in graph.observations if edge.predicate=='copies'])==2
    assert not next(edge for edge in graph.observations if edge.source_ref.record_id=='zz-denial').eligible
    assert graph.pc04 is None
    assert projections._check_edge_eligibility(graph,(positive,),job).state=='met'
    assert projections._check_edge_eligibility(graph,graph.observations,job).state=='unmet'


@pytest.mark.parametrize('mismatch',('claim_version','inquiry','dimension','empty_claim'))
def test_actual_scope_fields_are_not_wildcards_or_equivalent_versions(mismatch):
    source=cases.pool();source['inquiries'][0]['dependency_dimensions']=list(DIMENSIONS)
    source['assertions']=[cases.relation('copies')]
    context=ctx('claim_origin')
    if mismatch=='claim_version': context=ctx('claim_origin',claims=('claim2',))
    elif mismatch=='dimension': context=ctx('claim_origin','analytical_method')
    elif mismatch=='inquiry':
        second=copy.deepcopy(source['inquiries'][0]);second['id']='other';source['inquiries'].append(second)
        context=_QualificationContext('other',('claim',),(),'acquisition','snapshot_structural',None,None,('copies',),'claim_origin',())
    else:
        # A non-claim view still must not borrow scoped assertions through an empty set.
        source['assertions']=[cases.relation('cites')];context=ctx('citation',claims=())
    graph,_,_=project(admitted(source),context)
    selected=[edge for edge in graph.observations if edge.predicate is not None]
    assert selected and all(not edge.eligible for edge in selected)
    assert all('scope_unestablished' in edge.reason_codes for edge in selected)


def test_query_subject_roots_do_not_filter_intermediate_edges_or_create_independence():
    source=cases.pool();a=cases.relation('copies');b=cases.relation('originates_from')
    b['data']['from_ref']='e2';source['assertions']=[a,b]
    graph,_,_=project(admitted(source),ctx('claim_origin',subjects=('e',)))
    assert {(edge.source.identifier,edge.target.identifier) for edge in graph.edges}=={('e','e2'),('e2','origin')}
    assert not hasattr(graph,'origin_count')


def test_unknown_endpoint_is_a_preserved_frontier_and_never_an_invented_resolved_kind():
    source=cases.pool();unknown=cases.by_id(source,'unresolved')
    unknown['data']['expected_kinds']=['evidence_item'];unknown['data']['description']='Unresolved evidence for exact claim role claim.'
    relation=cases.relation('copies');relation['data']['to_ref']='unresolved';source['assertions']=[relation]
    graph,_,_=project(admitted(source),ctx('claim_origin'))
    edge=next(edge for edge in graph.edges if edge.predicate=='copies')
    assert edge.target.kind=='unresolved_reference' and edge.target.identifier=='unresolved'
    assert 'unknown_endpoint' in edge.reason_codes
    assert not hasattr(edge.target,'origin')


def test_same_identity_assertion_never_merges_nodes_or_supplies_a_support_edge():
    source=cases.pool();source['assertions']=[cases.relation('same_identity_as')]
    graph,_,_=project(admitted(source),ctx('assertion_assurance',subjects=('artifact','artifact2')))
    assert {node.identifier for node in graph.nodes}>={'artifact','artifact2'}
    assert all(edge.predicate!='same_identity_as' for edge in graph.edges)
    assert any(item.identifier=='r-same_identity_as' for item in graph.annotations)


@pytest.mark.parametrize('owner,selector,target,view',[
    ('evaluation','data.role_bindings[role=candidate].object_ref','claim','model_evaluation'),
    ('evaluation','data.role_bindings[role=executor].object_ref','actor','model_evaluation'),
    ('evaluation','data.target_refs','claim','model_evaluation'),
    ('evaluation','data.result_refs','artifact','model_evaluation'),
    ('origin','data.performed_by_refs','actor','organizational'),
    ('model','data.provider_ref','actor','organizational'),
    ('evaluation','data.role_bindings[role=executor].object_ref','actor','organizational'),
    ('channel','data.owner_refs','actor','organizational'),
    ('channel','data.target_refs','claim','correction_routing'),
    ('handling','data.case_ref','submission','correction_outcomes'),
    ('change','data.details.before_ref','claim','correction_outcomes'),
    ('change','data.details.after_ref','claim2','correction_outcomes'),
    ('pipeline','data.subject_ref','e','pipeline_stages'),
    ('pipeline','data.output_refs','artifact','pipeline_stages'),
])
def test_registered_native_links_have_semantic_selector_identity(owner,selector,target,view):
    graph,_,_=project(admitted(cases.pool()),ctx(view))
    rows=[edge for edge in graph.edges if edge.source.identifier==owner and edge.target.identifier==target and edge.source_ref.selector==selector]
    assert len(rows)==1 and rows[0].predicate is None
    assert rows[0].key==('records',owner,selector,'records',target)
    assert rows[0].source_entity.identifier==owner
    assert all('[' not in key or '[role=' in key for key in rows[0].key)


def test_role_and_recordlink_identity_survives_source_array_permutations():
    source=cases.pool();other=copy.deepcopy(source)
    cases.by_id(other,'evaluation')['data']['role_bindings'].reverse()
    other['records'].reverse()
    graphs=[project(admitted(value),ctx('model_evaluation'))[0] for value in (source,other)]
    assert [edge.key for edge in graphs[0].edges]==[edge.key for edge in graphs[1].edges]
    assert [node.key for node in graphs[0].nodes]==sorted(node.key for node in graphs[0].nodes)
    for graph in graphs:
        assert all(any(edge.source is node for node in graph.nodes) and
                   any(edge.target is node for node in graph.nodes) for edge in graph.edges)
        with pytest.raises(FrozenInstanceError):graph.edges=()


def test_support_graph_uses_evidence_pointers_and_not_legitimate_self_attribution():
    source=cases.pool();a=cases.relation('copies');a['provenance']['evidence_ref_ids']=['pointer']
    source['assertions']=[a]
    source['evidence_references'].append({'id':'pointer','reference_kind':'record_pointer','availability':'supplied',
        'artifact_ref':None,'record_ref':'r-copies','locator':None,'excerpt':None,'provided_by_ref':'actor',
        'attestor_ref':None,'scope_note':'Fictional self-pointer, no independent support.'})
    graph,_,_=project(admitted(source),ctx('assertion_assurance'))
    links={(edge.source.identifier,edge.source_ref.selector,edge.target.identifier) for edge in graph.edges}
    assert ('r-copies','provenance.evidence_ref_ids','pointer') in links
    assert ('pointer','record_ref','r-copies') in links
    assert all(selector!='provenance.attributed_to_ref' for _,selector,_ in links)
    assert ('actor','provenance.attributed_to_ref','actor') not in links


def test_empty_view_completion_is_not_a_met_missing_subject_check():
    graph,_,job=project(admitted(cases.sparse()),ctx('citation'))
    assert graph.edges==() and graph.observations==()
    assert graph.pc04 is None
    check=projections._check_edge_eligibility(graph,(),job)
    assert check.state=='not_applicable'
    assert check.owner=='GRAPH_VIEW_CONTRACT'
    assert check.prepared is graph.prepared and check.context is graph.context


def test_empty_predicate_selection_never_becomes_all_edges_for_the_named_view():
    source=cases.pool();source['assertions']=[cases.relation('copies')];snapshot=admitted(source)
    selected,_,_=project(snapshot,ctx('claim_origin'))
    empty=_QualificationContext('inquiry',('claim',),(),'acquisition','snapshot_structural',None,None,(),'claim_origin',())
    unselected,_,job=project(snapshot,empty)
    assert any(edge.predicate=='copies' for edge in selected.edges)
    assert not any(edge.predicate is not None for edge in unselected.edges)
    assert unselected.pc04 is None
    assert projections._check_edge_eligibility(unselected,(),job).state=='not_applicable'


def test_out_of_scope_observation_cannot_poison_the_actual_pc04_candidate_scope():
    source=cases.pool();source['inquiries'][0]['dependency_dimensions']=list(DIMENSIONS)
    active=cases.relation('copies');other=copy.deepcopy(active);other['id']='other-dimension'
    other['data']['dimension']='analytical_method';other['data']['polarity']='denied'
    source['assertions']=[active,other]
    graph,_,job=project(admitted(source),ctx('claim_origin'))
    assert graph.pc04 is None
    actual=projections._check_edge_eligibility(graph,graph.edges,job)
    assert actual.state=='met'
    assert {ref.record_id for ref in actual.input_refs}=={'r-copies'}
    assert projections._check_edge_eligibility(graph,graph.observations,job).state=='unmet'
    assert {edge.source_ref.record_id for edge in graph.observations}=={'r-copies','other-dimension'}
    assert {edge.source_ref.record_id for edge in graph.edges}=={'r-copies'}


def test_duplicate_role_slots_share_one_canonical_edge_without_erasing_source_slots():
    source=cases.pool();roles=cases.by_id(source,'evaluation')['data']['role_bindings']
    duplicate=copy.deepcopy(roles[0]);duplicate['qualifications']=['Distinct supplied qualification retained.']
    roles.append(duplicate)
    graph,_,_=project(admitted(source),ctx('model_evaluation'))
    keys=[edge.key for edge in graph.edges]
    assert len(keys)==len(set(keys))
    candidates=[edge for edge in graph.edges if edge.source.identifier=='evaluation' and
                edge.source_ref.selector=='data.role_bindings[role=candidate].object_ref']
    assert len(candidates)==1
    original=dict(dict(candidates[0].source_entity.node.fields.items)['data'].items)['role_bindings'].items
    assert len(original)==3
    assert any(dict(role.items)['qualifications'].items==('Distinct supplied qualification retained.',) for role in original)


def test_role_support_identity_includes_object_and_survives_array_permutation():
    source=cases.pool();roles=cases.by_id(source,'evaluation')['data']['role_bindings']
    roles[1]['evidence_ref_ids']=['support']
    second=copy.deepcopy(roles[1]);second['object_ref']='model';roles.append(second)
    permuted=copy.deepcopy(source);cases.by_id(permuted,'evaluation')['data']['role_bindings'].reverse()
    selected=[]
    for value in (source,permuted):
        graph,_,_=project(admitted(value),ctx('assertion_assurance'))
        edges=[edge for edge in graph.edges if edge.source.identifier=='evaluation' and edge.target.identifier=='support']
        assert len(edges)==2
        assert {edge.source_ref.selector for edge in edges}=={
            'data.role_bindings[role=executor;object_ref=actor].evidence_ref_ids',
            'data.role_bindings[role=executor;object_ref=model].evidence_ref_ids'}
        selected.append([edge.key for edge in edges])
    assert selected[0]==selected[1]


@pytest.mark.parametrize('predicate',('derived_from','originates_from'))
def test_multi_claim_scope_cannot_rebind_actual_evidence_item_endpoints(predicate):
    source=cases.pool();source['inquiries'][0]['target_claim_refs']=['claim','claim2']
    for identifier in ('e','e2'):cases.by_id(source,identifier)['data']['claim_ref']='claim2'
    relation=cases.relation(predicate);relation['scope']['claim_refs']=['claim','claim2'];source['assertions']=[relation]
    snapshot=admitted(source)
    for selected,expected in (('claim',False),('claim2',True)):
        graph,_,job=project(snapshot,ctx('claim_origin',subjects=('e',),claims=(selected,)))
        edge=next(edge for edge in graph.observations if edge.predicate==predicate)
        assert edge.eligible is expected
        assert ('scope_unestablished' in edge.reason_codes) is not expected
        assert projections._check_edge_eligibility(graph,(edge,),job).state==('met' if expected else 'unmet')


def test_pc04_selection_requires_actual_projection_edge_identity_and_deduplicates():
    source=cases.pool();source['assertions']=[cases.relation('copies')]
    graph,_,job=project(admitted(source),ctx('claim_origin'))
    edge=graph.edges[0]
    fact=projections._check_edge_eligibility(graph,(edge,edge),job)
    assert fact.state=='met' and fact.input_refs==(edge.source_ref,)
    with pytest.raises(TypeError):projections._check_edge_eligibility(graph,(replace(edge),),job)


@pytest.mark.parametrize('different',('context','snapshot'))
def test_actual_pc04_provider_bridges_to_m015_only_for_exact_component_input(different):
    from source_integrity_toolkit.validation.semantics import _provenance_profile
    source=cases.pool();source['assertions']=[cases.relation('copies')]
    snapshot=admitted(source);context=ctx('claim_origin')
    graph,_,job=project(snapshot,context)
    fact=projections._check_edge_eligibility(graph,graph.edges,job)
    out=_provenance_profile(snapshot,context,('r-copies',),('support',),(),job,provider_facts=(fact,))
    for row in out.results:
        checks={check.check_id:check.state for check in row.check_refs}
        assert checks['PC04']=='met' and checks['PC03']=='unknown'
    inventory=next(row for row in out.results if row.ref.field_key=='declared_basis_inventory')
    # This is a component bridge, with declaration metadata still native.
    category=next(category for category in inventory.value.categories if category.label=='declaration')
    assert category.count==1 and tuple(ref.identifier for ref in category.member_refs)==('r-copies',)
    bad_snapshot=admitted(source) if different=='snapshot' else snapshot
    bad_context=ctx('claim_origin') if different=='context' else context
    with pytest.raises(TypeError):
        _provenance_profile(bad_snapshot,bad_context,('r-copies',),('support',),(),job,provider_facts=(fact,))


def known(value):
    return {'state':'known','value':value,'precision':'instant'}


def time_context(view,predicates,requested='2026-09-21T12:00:00Z'):
    from source_integrity_toolkit.contracts.evidence import _Node
    time=_Node('TimeValue',_Object(tuple(sorted(known(requested).items()))))
    return _QualificationContext('inquiry',('claim',),(),'acquisition','time_specific',time,None,predicates,view,())


@pytest.mark.parametrize('known_window',(False,True))
def test_time_specific_relation_eligibility_requires_its_actual_effective_window(known_window):
    source=cases.pool();relation=cases.relation('cites')
    if known_window:
        relation['scope']['effective_window']={'start':known('2026-09-21T00:00:00Z'),'end':known('2026-09-22T00:00:00Z')}
    source['assertions']=[relation]
    graph,_,_=project(admitted(source),time_context('citation',('cites',)))
    observation=next(edge for edge in graph.observations if edge.predicate=='cites')
    assert observation.eligible is known_window
    if not known_window:assert 'time_applicability_unknown' in observation.reason_codes


def test_occurrence_time_does_not_supply_an_effective_window_for_a_role_link():
    source=cases.pool();cases.by_id(source,'evaluation')['data']['occurred_at']=known('2026-09-21T12:00:00Z')
    graph,_,_=project(admitted(source),time_context('model_evaluation',('generated_by','model_derived_from','trained_on')))
    roles=[edge for edge in graph.observations if edge.source.identifier=='evaluation']
    assert roles and all(not edge.eligible for edge in roles)
    assert all('time_applicability_unknown' in edge.reason_codes for edge in roles)


def test_route_assertion_window_cannot_replace_its_narrower_role_valid_window():
    source=cases.pool();relation=cases.relation('propagates_to')
    relation['scope']['effective_window']={'start':known('2026-09-21T00:00:00Z'),'end':known('2026-09-22T00:00:00Z')}
    relation['data']['details']['valid_window']={'start':known('2026-09-21T14:00:00Z'),'end':known('2026-09-21T16:00:00Z')}
    source['assertions']=[relation]
    graph,_,_=project(admitted(source),time_context('correction_routing',('propagates_to',)))
    edge=next(edge for edge in graph.observations if edge.predicate=='propagates_to')
    assert not edge.eligible and edge.reason_codes
    assert not hasattr(graph,'authorized_route')
