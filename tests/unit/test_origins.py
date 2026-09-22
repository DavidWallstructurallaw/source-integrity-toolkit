# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Independent W05 M002 oracles: Definitions 21.2 and VF006--VF008.

H7/W7 source clauses define the literal sets and paths below. Real admission,
tool-owned jobs and the invocation witness ledger are exercised as components;
this is not the deferred W13 public analytical pipeline.
"""
import copy
from dataclasses import FrozenInstanceError, replace
import importlib.util
import json
from pathlib import Path
from types import SimpleNamespace

import pytest

from source_integrity_toolkit.analysis import origins
from source_integrity_toolkit.contracts.bundle import _Array, _Object
from source_integrity_toolkit.contracts.evidence import _PreparedBundle, _QualificationContext
from source_integrity_toolkit.contracts.execution import _AnalysisAborted, _AuditCancelled
from source_integrity_toolkit.runtime.boundary import _prepare_value
from source_integrity_toolkit.runtime import resources

ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location('sit_w05_origin_cases', ROOT/'tests/contract/test_typed_records.py')
cases = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cases)

PARENTS = ('derived_from', 'copies', 'syndicated_from', 'summarizes', 'translates',
           'quotes', 'originates_from', 'depends_on')
H7_SEEDS = ('H7-EA', 'H7-EB', 'H7-EC', 'H7-ED', 'H7-EE', 'H7-EF')
FAMILY_FIELDS = {
    'SIT-M002':('reached_origin_record_count','documentary_origin_boundary_record_count','origin_boundary_disclosures'),
    'SIT-M007':('unresolved_frontier_reference_count','unqualified_terminal_record_count',
                'seed_items_with_unresolved_ancestry_count','ancestry_gap_disclosures'),
}
RESULT_ORIGINS={'reached_origin_record_count':'graph_derivation',
    'documentary_origin_boundary_record_count':'qualification_check','origin_boundary_disclosures':'attributed_record',
    'unresolved_frontier_reference_count':'graph_derivation','unqualified_terminal_record_count':'graph_derivation',
    'seed_items_with_unresolved_ancestry_count':'graph_derivation','ancestry_gap_disclosures':'graph_derivation'}
H7_PATHS = {
    'H7-EA': (('H7-EA', 'H7-ER1', 'H7-O1'), ('H7-L02', 'H7-L01')),
    'H7-EB': (('H7-EB', 'H7-ER1', 'H7-O1'), ('H7-L03', 'H7-L01')),
    'H7-EC': (('H7-EC', 'H7-ER1', 'H7-O1'), ('H7-L04', 'H7-L01')),
    'H7-ED': (('H7-ED', 'H7-EB', 'H7-ER1', 'H7-O1'), ('H7-L05', 'H7-L03', 'H7-L01')),
    'H7-EE': (('H7-EE', 'H7-EA', 'H7-ER1', 'H7-O1'), ('H7-L06', 'H7-L02', 'H7-L01')),
    'H7-EF': (('H7-EF', 'H7-O2'), ('H7-L07',)),
}


def hero(variant='H7-01'):
    return json.loads((ROOT/'tests/fixtures/hero'/f'{variant}.bundle.json').read_bytes())


def native(value):
    if type(value) is _Object:
        return {key: native(item) for key, item in value.items}
    if type(value) is _Array:
        return [native(item) for item in value.items]
    return value


def context(source, *, claim=None, dimension='acquisition', subjects=()):
    inquiry = source['inquiries'][0]
    return _QualificationContext(inquiry['id'], (claim or inquiry['target_claim_refs'][0],), subjects,
        dimension, 'snapshot_structural', None, 'upstream_history', PARENTS, 'claim_origin', ())


def prepared(source):
    answer = _prepare_value(source)
    assert type(answer) is _PreparedBundle
    return answer


def job_pair():
    owner = resources._new_analysis_budget()
    owner.record_input_acceptance()
    return owner, owner.start_job()


def supplied(record, *, basis='documented_record', support='support'):
    record['provenance'].update(basis_kind=basis, evidence_ref_ids=[support],
        method='Examine the supplied finite fictional process excerpt.',
        qualifications=['Caller-supplied conformance material; no outside authentication.'])
    return record


def relation(identifier, predicate, source, target, *, dimension='acquisition'):
    answer = cases.relation(predicate)
    answer['id'] = identifier
    answer['data'].update(from_ref=source, to_ref=target, dimension=dimension)
    return supplied(answer)


def add_coverage(source, members, *, state='complete_for_scope', subjects=('inquiry',),
                 predicates=PARENTS, identifier='coverage', dimension='acquisition'):
    row = cases.assertion(identifier, 'assessment', {'assessment_kind':'coverage',
        'subject_refs':list(subjects), 'details':{'coverage_kind':'upstream_history',
        'state':state, 'relation_types':list(predicates), 'dimensions':[dimension],
        'member_refs':list(members), 'omitted_refs':[], 'universe_enumerated':state=='complete_for_scope',
        'scope_note':'Exactly the listed fictional records and outgoing parent types.'}})
    if state!='complete_for_scope':
        row['gaps']=[{'field':'data.details.member_refs', 'reason':'not_recorded',
                      'detail':'Further ancestry was not examined.'}]
    source['assertions'].append(supplied(row))
    source['inquiries'][0]['coverage_assertion_refs'].append(identifier)
    return row


def add_boundary(source, origin='origin', *, role='documented_origin', identifier='boundary',
                 coverage='coverage', dimension='acquisition', basis='documented_record'):
    row = cases.assertion(identifier, 'assessment', {'assessment_kind':'origin_boundary',
        'subject_refs':[origin], 'details':{'dimension':dimension, 'boundary_role':role,
        'coverage_ref':coverage, 'termination_reason':'The supplied boundary role of this finite fixture.'}})
    source['assertions'].append(supplied(row, basis=basis))
    return row


def small(*, edges=(('direct','originates_from','e','origin'),), seeds=('e',),
          roles=(('origin','documented_origin'),), coverage_state='complete_for_scope'):
    source = cases.pool()
    source['assertions'] = [relation(*edge) for edge in edges]
    source['inquiries'][0]['seed_evidence_refs'] = list(seeds)
    source['inquiries'][0]['seed_artifact_refs'] = [cases.by_id(source, seed)['data']['artifact_ref'] for seed in seeds]
    source['inquiries'][0]['coverage_assertion_refs'] = []
    members = list(dict.fromkeys(list(seeds)+[item for edge in edges for item in edge[2:]]))
    add_coverage(source, members, state=coverage_state)
    for index, (origin, role) in enumerate(roles):
        add_boundary(source, origin, role=role, identifier='boundary'+str(index))
    for row in source['records']:
        if row['kind'] in ('evidence_item','origin_event'):
            supplied(row)
    return source


def leaf(out, name):
    return next(row for row in out.results if row.ref.field_key==name)


def count_view(out, name):
    row = leaf(out, name)
    assert (row.execution_state,row.result_state)==('completed','available')
    assert row.value_kind=='count'
    expected_units={'reached_origin_record_count':'origin_event','documentary_origin_boundary_record_count':'origin_event',
        'unresolved_frontier_reference_count':'unresolved_reference','unqualified_terminal_record_count':'record',
        'seed_items_with_unresolved_ancestry_count':'evidence_item'}
    assert row.value.population.unit==expected_units[name]
    assert row.value.population.membership_state=='enumerated_for_scope'
    assert row.value.population.selection_rule and row.value.population in row.population_refs
    assert all(ref.collection=='records' and ref.selector is None for ref in row.value.population.member_refs)
    if name=='reached_origin_record_count':
        endpoints={ref.anchor[-1].identifier for ref in row.witness_refs if ref.kind=='path'}
        assert {ref.identifier for ref in row.value.population.member_refs} <= endpoints
    return {'value':row.value.value, 'members':tuple(ref.identifier for ref in row.value.population.member_refs)}


def assert_count(actual, expected):
    assert actual=={'value':len(expected), 'members':tuple(expected)}


def disclosures(out, name):
    row = leaf(out,name)
    assert (row.execution_state,row.result_state)==('completed','available')
    assert row.value_kind=='record_disclosures'
    collection='assertions' if name=='origin_boundary_disclosures' else 'records'
    assert all(record.source.collection==collection and record.source.selector is None for record in row.value.records)
    result = {record.source.identifier:native(record.fields) for record in row.value.records}
    assert len(result)==len(row.value.records)
    return result


def check(out,field,identifier):
    return next(item for item in leaf(out,field).check_refs if item.check_id==identifier)


def tokens(value):
    if type(value) is dict:
        return tuple(token for key,item in value.items() for token in (key,*tokens(item)))
    if type(value) in (tuple,list):
        return tuple(token for item in value for token in tokens(item))
    return (value,)


def resolved_witnesses(row,facts):
    """Compact query identities resolve uniquely to retained full payloads."""
    catalog={}
    for witness in facts.witnesses:
        nodes=(witness.starts if witness.kind=='complete_trace' else
               (witness.nodes[0],) if witness.kind=='cycle' else (witness.nodes[0],witness.nodes[-1]))
        key=(witness.kind,tuple((node.collection,node.identifier) for node in nodes))
        catalog.setdefault(key,[]).append(witness)
    answer=[]
    for ref in row.witness_refs:
        assert type(ref.anchor[0]) is str
        assert all(part.selector is None for part in ref.anchor[1:])
        key=(ref.anchor[0],tuple((part.collection,part.identifier) for part in ref.anchor[1:]))
        matches=catalog.get(key,())
        assert len(matches)==1
        witness=matches[0]
        assert ref.kind==('member_set' if witness.kind=='complete_trace' else witness.kind)
        assert witness.graph is facts.graph
        if witness.kind=='path':
            assert len(witness.nodes)==len(witness.edges)+1
            assert all(edge.source is witness.nodes[index] and edge.target is witness.nodes[index+1]
                       for index,edge in enumerate(witness.edges))
        answer.append(witness)
    return tuple(answer)


def result_paths(row,facts):
    return tuple((tuple(node.identifier for node in witness.nodes),
                  tuple(edge.source_ref.record_id for edge in witness.edges))
                 for witness in resolved_witnesses(row,facts) if witness.kind=='path')


def run(source, *, context_changes=None, family=None):
    snapshot=prepared(source);ctx=context(source,**(context_changes or {}))
    owner,job=job_pair();ledger=owner.witnesses;rows=[]
    families=(family,) if family is not None else ('SIT-M002','SIT-M007')
    for index,selected in enumerate(families):
        if index:
            owner.finish_job(job)
            job=owner.start_job()
        before=(owner.used,job.used)
        before_witnesses=(ledger._retained_witnesses,ledger._retained_members)
        output=origins._origin_profile(snapshot,ctx,ledger,job,family=selected)
        assert type(output.results) is tuple
        assert owner.used-before[0]==job.used-before[1]>0
        assert output.facts.prepared is snapshot and output.facts.context is ctx
        assert output.facts.job_port is job
        assert ledger._retained_witnesses-before_witnesses[0]==len(output.witnesses)
        assert ledger._retained_members-before_witnesses[1]==sum(witness.member_count for witness in output.witnesses)
        assert {row.ref.diagnostic_id for row in output.results}=={selected}
        assert len(output.results)==len(FAMILY_FIELDS[selected])
        assert {row.ref.field_key for row in output.results}==set(FAMILY_FIELDS[selected])
        for row in output.results:
            scope=row.ref.scope
            assert scope.inquiry_ref.identifier==ctx.inquiry_ref
            assert tuple(ref.identifier for ref in scope.claim_refs)==ctx.claim_refs
            assert scope.dependency_dimension==ctx.dependency_dimension
            assert scope.graph_view=='claim_origin' and scope.temporal_basis==ctx.temporal_basis
            # Explicit query subjects and the separately enumerated seed
            # population are different fields; neither is a wildcard.
            assert tuple(ref.identifier for ref in scope.target_refs)==ctx.subject_refs
            assert all(ref.collection=='records' and ref.selector is None for ref in scope.target_refs)
            assert row.basis_refs and row.interpretation_limit
            assert row.result_origin==RESULT_ORIGINS[row.ref.field_key]
            checks={check.check_id:check for check in row.check_refs}
            assert {'PC02','PC03','PC04','PC24'} <= checks.keys()
            assert all(checks[name].state=='met' for name in ('PC02','PC03','PC24'))
            for provider in (output.facts.inventory.pc03,output.facts.pc04):
                actual=checks[provider.check_id]
                assert actual.state==provider.state
                assert {(ref.collection,ref.identifier,ref.selector or '') for ref in actual.input_refs}=={
                    (address.collection,address.record_id,address.selector) for address in provider.input_refs}
            assert all(check.result_ref._key()==row.ref._key() for check in row.check_refs)
            assert all(reason.scope._key()==scope._key() and
                       row.ref._key() in tuple(ref._key() for ref in reason.affected_result_refs) for reason in row.reason_refs)
            assert all(witness.scope._key()==scope._key() for witness in row.witness_refs)
            if output.facts.witnesses:assert row.witness_refs
            paths={path for paths in path_view(output.facts).values() for path in paths}
            assert set(result_paths(row,output.facts)) <= paths
        if selected=='SIT-M002':
            boundary_rows=disclosures(SimpleNamespace(results=output.results),'origin_boundary_disclosures')
            for fact in output.facts.boundaries:
                actual=boundary_rows[fact.assessment.identifier]
                assert actual['qualification_state']==fact.state
                assert actual['reason_codes']==list(fact.reason_codes)
            if output.facts.boundaries:
                for row in output.results:
                    if row.ref.field_key in ('documentary_origin_boundary_record_count','origin_boundary_disclosures'):
                        assert {'PC05','PC06','PC07','PC08','PC09','PC10'} <= {item.check_id for item in row.check_refs}
        rows.extend(output.results)
    # Test-only collection of separately completed jobs, not a product result
    # or a claim that one analytical job executed several diagnostic families.
    return SimpleNamespace(results=tuple(rows)),output.facts,owner,job


def path_view(facts):
    return {trace.seed.identifier:tuple(
        (tuple(node.identifier for node in witness.nodes),
         tuple(edge.source_ref.record_id for edge in witness.edges))
        for witness in trace.witnesses if witness.kind=='path') for trace in facts.seed_traces}


def reached_edge_ids(facts,seed):
    trace=next(trace for trace in facts.seed_traces if trace.seed.identifier==seed)
    return {edge.source_ref.record_id for edge in trace.reachability.edges}


def assert_native_boundaries(actual, source, identifiers):
    assert tuple(actual)==tuple(identifiers)
    for identifier in identifiers:
        original=cases.by_id(source,identifier)
        for field in ('data','scope','provenance','lifecycle_state'):
            assert actual[identifier][field]==original[field]


@pytest.fixture(scope='module')
def h7_run():
    return run(hero())


def test_vf006_p_h7_exact_reached_origins_and_six_finite_source_paths(h7_run):
    out,facts,_,_=h7_run
    assert_count(count_view(out,'reached_origin_record_count'),('H7-O1','H7-O2'))
    # The trace adapter reads completed witness representations only; expected
    # paths are the independent, fixed Lineage 25.1 / Validation 2.2 table.
    actual=path_view(facts)
    for seed,path in H7_PATHS.items():
        assert path in actual[seed]
    assert tuple(sorted(actual))==H7_SEEDS


def test_vf006_n_parentless_evidence_and_unresolved_expected_origin_are_not_origins():
    source=small(edges=(),roles=())
    baseline=run(source)[0]
    actual=count_view(baseline,'reached_origin_record_count')
    assert_count(actual,())
    mutant=copy.deepcopy(actual);mutant.update(value=1,members=('e',))
    with pytest.raises(AssertionError):assert_count(mutant,())
    source=small(edges=(('unknown-origin','originates_from','e','unresolved'),),roles=(),coverage_state='partial')
    cases.by_id(source,'unresolved')['data'].update(expected_kinds=['origin_event'],
        description='Withheld origin of the exact claim acquisition contribution.')
    baseline=run(source)[0];actual=count_view(baseline,'reached_origin_record_count')
    assert_count(actual,())
    mutant=copy.deepcopy(actual);mutant.update(value=1,members=('unresolved',))
    with pytest.raises(AssertionError):assert_count(mutant,())


def test_vf007_p_h7_qualified_count_and_vf008_p_attributed_boundaries(h7_run):
    out,_,_,_=h7_run
    assert_count(count_view(out,'documentary_origin_boundary_record_count'),('H7-O1','H7-O2'))
    actual=disclosures(out,'origin_boundary_disclosures')
    assert_native_boundaries(actual,hero(),('H7-OB1','H7-OB2'))
    assert all('H7-COV-ACQ' in tokens(row) and 'H7-SUP-ACQ' in tokens(row) for row in actual.values())
    assert all(row['qualification_state']=='met' and row['reason_codes']==[] for row in actual.values())
    for identifier in ('PC05','PC06','PC07','PC08','PC09','PC10'):
        assert check(out,'documentary_origin_boundary_record_count',identifier).state=='met'


@pytest.mark.parametrize('availability',('locator_only','withheld','unavailable'))
def test_vf007_n_support_removal_is_an_input_delta_not_boundary_relabeling(availability,h7_run):
    source=hero();baseline=h7_run[0]
    assert_count(count_view(baseline,'documentary_origin_boundary_record_count'),('H7-O1','H7-O2'))
    changed=copy.deepcopy(source)
    support=cases.by_id(changed,'H7-SUP-ACQ')
    support.update(reference_kind='external_locator',availability=availability,
        locator='https://example.invalid/never-fetch-attestation',excerpt=None)
    out=run(changed)[0]
    assert_count(count_view(out,'reached_origin_record_count'),('H7-O1','H7-O2'))
    assert_count(count_view(out,'documentary_origin_boundary_record_count'),())
    rows=disclosures(out,'origin_boundary_disclosures')
    assert_native_boundaries(rows,changed,('H7-OB1','H7-OB2'))
    assert all(row['data']['details']['boundary_role']=='documented_origin' for row in rows.values())
    assert all('support_uninspectable' in tokens(row) for row in rows.values())
    assert all(row['qualification_state']=='unmet' for row in rows.values())
    for identifier in ('PC05','PC07'):
        actual=check(out,'documentary_origin_boundary_record_count',identifier)
        assert actual.state=='unmet'
        assert {'H7-OB1','H7-OB2'} <= {ref.identifier for ref in actual.input_refs}


def test_vf007_m_documentary_label_without_basis_has_explicit_zero_examined_count():
    source=small();boundary=cases.by_id(source,'boundary0')
    boundary['provenance']=cases.provenance()
    out=run(source)[0]
    assert_count(count_view(out,'documentary_origin_boundary_record_count'),())
    assert_count(count_view(out,'reached_origin_record_count'),('origin',))
    rows=disclosures(out,'origin_boundary_disclosures')
    assert_native_boundaries(rows,source,('boundary0',))
    assert 'documentary_basis_incomplete' in tokens(rows)


@pytest.mark.parametrize('role',('declared_origin','reference_baseline','scope_cut','unresolved'))
def test_vf007_b_boundary_roles_remain_distinct_without_label_upgrades(role):
    source=small(roles=(('origin',role),));out=run(source)[0]
    assert_count(count_view(out,'reached_origin_record_count'),('origin',))
    assert_count(count_view(out,'documentary_origin_boundary_record_count'),())
    assert_native_boundaries(disclosures(out,'origin_boundary_disclosures'),source,('boundary0',))


@pytest.mark.parametrize('role',('declared_origin','reference_baseline'))
def test_vf008_n_output_mutant_cannot_rename_a_native_boundary(role):
    source=small(roles=(('origin',role),));out=run(source)[0]
    baseline=disclosures(out,'origin_boundary_disclosures')
    assert_native_boundaries(baseline,source,('boundary0',))
    mutant=copy.deepcopy(baseline)
    mutant['boundary0']['data']['details']['boundary_role']='documented_origin'
    with pytest.raises(AssertionError):assert_native_boundaries(mutant,source,('boundary0',))


def test_vf008_m_no_boundary_assessment_is_an_explicit_empty_inventory():
    out=run(small(roles=()))[0]
    assert disclosures(out,'origin_boundary_disclosures')=={}
    assert_count(count_view(out,'reached_origin_record_count'),('origin',))
    assert_count(count_view(out,'documentary_origin_boundary_record_count'),())


@pytest.mark.parametrize('role',('documented_origin','scope_cut','reference_baseline'))
def test_vf008_b_termination_label_cannot_hide_a_known_same_dimension_parent(role):
    source=small(edges=(('direct','originates_from','e','origin'),
                        ('upstream','depends_on','origin','origin2')),
                 roles=(('origin',role),('origin2','documented_origin')))
    out,facts,_,_=run(source)
    assert_count(count_view(out,'reached_origin_record_count'),('origin','origin2'))
    assert_count(count_view(out,'documentary_origin_boundary_record_count'),('origin2',))
    assert_native_boundaries(disclosures(out,'origin_boundary_disclosures'),source,('boundary0','boundary1'))
    assert (('e','origin','origin2'),('direct','upstream')) in path_view(facts)['e']


def test_vf006_b_diamond_counts_one_origin_after_examining_both_branches():
    source=small(edges=(('left','copies','e','e2'),('right','copies','e','e3'),
                        ('left-root','originates_from','e2','origin'),
                        ('right-root','originates_from','e3','origin')))
    third=copy.deepcopy(cases.by_id(source,'e2'));third['id']='e3';source['records'].append(third)
    out,facts,_,_=run(source)
    assert_count(count_view(out,'reached_origin_record_count'),('origin',))
    assert_count(count_view(out,'documentary_origin_boundary_record_count'),('origin',))
    assert_count(count_view(out,'seed_items_with_unresolved_ancestry_count'),())
    assert reached_edge_ids(facts,'e')=={'left','right','left-root','right-root'}


def test_vf006_b_cycle_exit_preserves_origin_and_unresolved_affected_seeds():
    source=small(edges=(('a-b','derived_from','e','e2'),('b-a','derived_from','e2','e'),
                        ('exit','originates_from','e','origin')),seeds=('e','e2'))
    out,facts,_,_=run(source)
    assert_count(count_view(out,'reached_origin_record_count'),('origin',))
    assert_count(count_view(out,'seed_items_with_unresolved_ancestry_count'),('e','e2'))
    assert 'lineage_cycle' in tokens(disclosures(out,'ancestry_gap_disclosures'))
    assert reached_edge_ids(facts,'e')=={'a-b','b-a','exit'}


def test_several_boundary_assessments_count_one_origin_record():
    source=small();add_boundary(source,identifier='another-boundary')
    out=run(source)[0]
    assert_count(count_view(out,'documentary_origin_boundary_record_count'),('origin',))
    assert_native_boundaries(disclosures(out,'origin_boundary_disclosures'),source,('another-boundary','boundary0'))


def test_h7_seed_selection_controls_reached_origin_population_not_dossier_membership():
    out=run(hero('H7-V01'))[0]
    assert_count(count_view(out,'reached_origin_record_count'),('H7-O1',))
    assert_count(count_view(out,'documentary_origin_boundary_record_count'),('H7-O1',))
    assert tuple(disclosures(out,'origin_boundary_disclosures'))==('H7-OB1',)


def test_explicit_empty_seed_population_does_not_borrow_dossier_origins_or_boundaries():
    source=small();source['inquiries'][0]['seed_evidence_refs']=[]
    # Artifact seed and a fully supplied but disconnected E→O + boundary remain.
    out,facts,_,_=run(source)
    assert facts.seed_traces==() and facts.inventory.seed_evidence==()
    assert tuple(item.identifier for item in facts.inventory.artifacts)==('artifact',)
    for field in ('reached_origin_record_count','documentary_origin_boundary_record_count',
                  'unresolved_frontier_reference_count','unqualified_terminal_record_count',
                  'seed_items_with_unresolved_ancestry_count'):
        assert_count(count_view(out,field),())
    for field in ('origin_boundary_disclosures','ancestry_gap_disclosures'):
        assert disclosures(out,field)=={}
    assert facts.reached_origins==facts.documentary_origins==facts.boundaries==()
    witness=facts.inventory_witness
    assert witness.kind=='complete_trace' and witness.starts==()
    assert witness.examined_nodes==witness.examined_edges==()
    assert witness in facts.witnesses
    for row in out.results:
        assert row.interpretation_limit
        # M002's matching empty query was retained in its own completed job;
        # the M007 facts returned by this harness prove this family's link.
        if row.ref.diagnostic_id=='SIT-M007':assert witness in resolved_witnesses(row,facts)


def test_h7_two_parent_variant_preserves_all_reached_origins_without_allocating():
    out,facts,_,_=run(hero('H7-V03'))
    assert_count(count_view(out,'reached_origin_record_count'),('H7-O1','H7-O2'))
    assert_count(count_view(out,'seed_items_with_unresolved_ancestry_count'),())
    paths=path_view(facts)['H7-EG']
    assert {nodes[-1] for nodes,edges in paths}>={'H7-O1','H7-O2'}
    assert not hasattr(facts,'weights') and not hasattr(facts,'independent_source_count')


def test_vf007_b_protected_attestation_qualifies_one_opaque_origin_with_native_limits():
    source=small(edges=(('a-root','originates_from','e','origin'),
                        ('b-root','originates_from','e2','origin')),seeds=('e','e2'))
    support=cases.by_id(source,'support')
    support.update(reference_kind='protected_attestation',attestor_ref='actor',
        excerpt='Supplied scoped attestation of one shared opaque acquisition; underlying identity is withheld.')
    boundary=cases.by_id(source,'boundary0')
    boundary['provenance'].update(basis_kind='protected_attestation',
        qualifications=['Underlying source identity is withheld; visible scoped attestation only.'])
    out=run(source)[0]
    assert_count(count_view(out,'reached_origin_record_count'),('origin',))
    assert_count(count_view(out,'documentary_origin_boundary_record_count'),('origin',))
    assert_native_boundaries(disclosures(out,'origin_boundary_disclosures'),source,('boundary0',))
    changed=copy.deepcopy(source)
    cases.by_id(changed,'support').update(reference_kind='external_locator',availability='withheld',
        attestor_ref=None,excerpt=None,locator='https://example.invalid/withheld-attestation')
    negative=run(changed)[0]
    assert_count(count_view(negative,'reached_origin_record_count'),('origin',))
    assert_count(count_view(negative,'documentary_origin_boundary_record_count'),())
    assert_native_boundaries(disclosures(negative,'origin_boundary_disclosures'),changed,('boundary0',))


def test_w7_17_all_four_boundary_roles_coexist_without_becoming_unresolved_roots():
    source=small(edges=(('one','originates_from','e','origin'),('two','originates_from','e2','origin2'),
                        ('three','originates_from','e3','origin3'),('four','originates_from','e4','origin4')),
        seeds=('e','e2'),roles=(('origin','documented_origin'),('origin2','declared_origin'),
                               ('origin3','reference_baseline'),('origin4','scope_cut')))
    for index in (3,4):
        item=copy.deepcopy(cases.by_id(source,'e'));item['id']='e'+str(index);source['records'].append(item)
        origin=copy.deepcopy(cases.by_id(source,'origin'));origin['id']='origin'+str(index)
        origin['data']['event_key']='separate-event-'+str(index);source['records'].append(origin)
    source['inquiries'][0]['seed_evidence_refs']=['e','e2','e3','e4']
    out=run(source)[0]
    assert_count(count_view(out,'reached_origin_record_count'),('origin','origin2','origin3','origin4'))
    assert_count(count_view(out,'documentary_origin_boundary_record_count'),('origin',))
    assert_count(count_view(out,'unqualified_terminal_record_count'),())
    assert_count(count_view(out,'seed_items_with_unresolved_ancestry_count'),())
    assert_native_boundaries(disclosures(out,'origin_boundary_disclosures'),source,('boundary0','boundary1','boundary2','boundary3'))


def test_exact_claim_populations_never_borrow_other_claims_origin_paths():
    source=small(edges=(('c1-root','originates_from','e','origin'),
                        ('c2-root','originates_from','e2','origin2')),
                 seeds=('e','e2'),roles=(('origin','documented_origin'),('origin2','documented_origin')))
    source['inquiries'][0]['target_claim_refs']=['claim','claim2']
    cases.by_id(source,'e2')['data']['claim_ref']='claim2'
    for identifier in ('c2-root','boundary1'):
        cases.by_id(source,identifier)['scope']['claim_refs']=['claim2']
    cases.by_id(source,'coverage')['scope']['claim_refs']=['claim','claim2']
    for claim,seeds,origins_set in (('claim',('e',),('origin',)),('claim2',('e2',),('origin2',))):
        out,facts,_,_=run(source,context_changes={'claim':claim})
        assert tuple(trace.seed.identifier for trace in facts.seed_traces)==seeds
        assert_count(count_view(out,'reached_origin_record_count'),origins_set)
        assert_count(count_view(out,'documentary_origin_boundary_record_count'),origins_set)


def test_explicit_full_seed_subject_request_preserves_the_same_finite_population():
    source=small()
    for requested in ((),('e',)):
        out,facts,_,_=run(source,context_changes={'subjects':requested})
        assert tuple(item.identifier for item in facts.inventory.seed_evidence)==('e',)
        assert_count(count_view(out,'reached_origin_record_count'),('origin',))
        assert_count(count_view(out,'documentary_origin_boundary_record_count'),('origin',))
        assert all(tuple(ref.identifier for ref in row.ref.scope.target_refs)==requested for row in out.results)


def test_dependency_dimensions_have_separate_parents_boundaries_and_coverage():
    source=small();source['inquiries'][0]['dependency_dimensions']=['acquisition','analytical_method']
    source['assertions'].append(relation('method-parent','originates_from','e','origin2',dimension='analytical_method'))
    add_coverage(source,('e','origin2'),identifier='method-coverage',dimension='analytical_method')
    add_boundary(source,'origin2',identifier='method-boundary',coverage='method-coverage',dimension='analytical_method')
    for dimension,expected in (('acquisition',('origin',)),('analytical_method',('origin2',))):
        out=run(source,context_changes={'dimension':dimension})[0]
        assert_count(count_view(out,'reached_origin_record_count'),expected)
        assert_count(count_view(out,'documentary_origin_boundary_record_count'),expected)


def test_identity_ambiguity_preserves_both_records_and_blocks_documentary_origin_qualification():
    source=small(edges=(('a-root','originates_from','e','origin'),
                        ('b-root','originates_from','e2','origin2')),
                 seeds=('e','e2'),roles=(('origin','documented_origin'),('origin2','documented_origin')))
    baseline=run(source)[0]
    assert_count(count_view(baseline,'documentary_origin_boundary_record_count'),('origin','origin2'))
    alias=cases.relation('same_identity_as');alias['data'].update(from_ref='origin',to_ref='origin2')
    alias['data']['details']['identity_level']='origin_event'
    source['assertions'].append(alias)
    out=run(source)[0]
    assert_count(count_view(out,'reached_origin_record_count'),('origin','origin2'))
    assert_count(count_view(out,'documentary_origin_boundary_record_count'),())
    assert 'identity_unresolved' in tokens(disclosures(out,'origin_boundary_disclosures'))


def test_relevant_weak_denial_keeps_the_positive_path_as_disputed_and_affects_only_its_seed():
    source=small(edges=(('a-root','originates_from','e','origin'),
                        ('b-root','originates_from','e2','origin2')),
                 seeds=('e','e2'),roles=(('origin','documented_origin'),('origin2','documented_origin')))
    denial=copy.deepcopy(cases.by_id(source,'a-root'));denial['id']='denial'
    denial['data']['polarity']='denied';denial['provenance']=cases.provenance();source['assertions'].append(denial)
    out,facts,_,_=run(source)
    assert_count(count_view(out,'reached_origin_record_count'),('origin','origin2'))
    assert_count(count_view(out,'seed_items_with_unresolved_ancestry_count'),('e',))
    assert 'premise_disputed' in tokens(disclosures(out,'ancestry_gap_disclosures'))
    assert (('e','origin'),('a-root',)) in path_view(facts)['e']


def test_unrelated_claim_or_dimension_denial_does_not_poison_a_complete_seed():
    source=small();source['inquiries'][0]['target_claim_refs']=['claim','claim2']
    source['inquiries'][0]['dependency_dimensions']=['acquisition','analytical_method']
    # Origin-to-Origin is a legal other-Claim relation. Sharing the known
    # origin ID is insufficient to make its explicitly different scope ours.
    other=relation('other-claim','depends_on','origin','origin2')
    other['scope']['claim_refs']=['claim2'];other['data']['polarity']='denied'
    dimension=relation('other-dimension','depends_on','origin','origin2',dimension='analytical_method')
    dimension['data']['polarity']='denied'
    source['assertions'].extend((other,dimension))
    out=run(source)[0]
    assert_count(count_view(out,'documentary_origin_boundary_record_count'),('origin',))
    assert_count(count_view(out,'seed_items_with_unresolved_ancestry_count'),())


def test_documentary_boundary_inventory_keeps_its_own_basis_when_reaching_path_support_is_missing():
    source=small(edges=(('first-path','originates_from','e','origin'),
                        ('other-path','originates_from','e2','origin2')),
                 seeds=('e','e2'),roles=(('origin','documented_origin'),('origin2','documented_origin')))
    support=copy.deepcopy(cases.by_id(source,'support'));support['id']='path-support'
    source['evidence_references'].append(support)
    cases.by_id(source,'first-path')['provenance']['evidence_ref_ids']=['path-support']
    baseline=run(source)[0]
    assert_count(count_view(baseline,'documentary_origin_boundary_record_count'),('origin','origin2'))
    assert check(baseline,'documentary_origin_boundary_record_count','PC05').state=='met'
    support.update(reference_kind='external_locator',availability='locator_only',excerpt=None,
                   locator='https://example.invalid/path-premise-only')
    out=run(source)[0]
    assert_count(count_view(out,'reached_origin_record_count'),('origin','origin2'))
    assert_count(count_view(out,'documentary_origin_boundary_record_count'),('origin','origin2'))
    assert_count(count_view(out,'seed_items_with_unresolved_ancestry_count'),('e',))
    for identifier in ('PC05','PC07'):
        actual=check(out,'documentary_origin_boundary_record_count',identifier)
        assert actual.state=='met'
        refs={ref.identifier for ref in actual.input_refs}
        assert {'boundary0','boundary1'} <= refs
        assert 'first-path' not in refs and 'path-support' not in refs
    assert check(out,'seed_items_with_unresolved_ancestry_count','PC05').state=='unmet'
    assert tuple(disclosures(out,'ancestry_gap_disclosures'))==('e',)
    row=leaf(out,'seed_items_with_unresolved_ancestry_count')
    missing=[reason for reason in row.reason_refs if reason.code=='support_uninspectable']
    assert missing and all('first-path' in {ref.identifier for ref in reason.input_refs} for reason in missing)


def test_boundary_self_pointer_cannot_supply_its_own_documentary_qualification():
    source=small();baseline=run(source)[0]
    assert_count(count_view(baseline,'documentary_origin_boundary_record_count'),('origin',))
    pointer=copy.deepcopy(cases.by_id(source,'support'))
    pointer.update(id='self-pointer',reference_kind='record_pointer',record_ref='boundary0',
                   artifact_ref=None,locator=None,excerpt=None)
    source['evidence_references'].append(pointer)
    cases.by_id(source,'boundary0')['provenance']['evidence_ref_ids']=['self-pointer']
    out=run(source)[0]
    assert_count(count_view(out,'reached_origin_record_count'),('origin',))
    assert_count(count_view(out,'documentary_origin_boundary_record_count'),())
    assert 'self_supporting_assurance' in tokens(disclosures(out,'origin_boundary_disclosures'))


def test_time_specific_unknown_effective_window_is_not_a_complete_temporal_trace():
    from source_integrity_toolkit.contracts.evidence import _Node
    source=small();instant={'state':'known','value':'2026-09-21T12:00:00Z','precision':'instant'}
    ctx=replace(context(source),temporal_basis='time_specific',requested_time=_Node('TimeValue',_Object(tuple(sorted(instant.items())))))
    for known,expected in ((False,()),(True,('origin',))):
        value=copy.deepcopy(source)
        if known:
            for assertion in value['assertions']:
                assertion['scope']['effective_window']={
                    'start':{'state':'known','value':'2026-09-21T00:00:00Z','precision':'instant'},
                    'end':{'state':'known','value':'2026-09-22T00:00:00Z','precision':'instant'}}
        owner,job=job_pair()
        output=origins._origin_profile(prepared(value),ctx,owner.witnesses,job,family='SIT-M002')
        assert_count(count_view(SimpleNamespace(results=output.results),'reached_origin_record_count'),expected)
        assert all(row.ref.scope.temporal_basis=='time_specific' for row in output.results)
        if not known:
            assert any(reason.code=='time_applicability_unknown' for row in output.results for reason in row.reason_refs)


@pytest.mark.parametrize('family',('SIT-M002','SIT-M007'))
@pytest.mark.parametrize('changed',('none','coverage','direct'))
def test_pc10_uses_actual_local_coverage_and_relation_time_qualifications(family,changed):
    from source_integrity_toolkit.contracts.evidence import _Node
    source=small();instant={'state':'known','value':'2026-09-21T12:00:00Z','precision':'instant'}
    ctx=replace(context(source),temporal_basis='time_specific',requested_time=_Node('TimeValue',_Object(tuple(sorted(instant.items())))))
    for assertion in source['assertions']:
        assertion['scope']['effective_window']={
            'start':{'state':'known','value':'2026-09-21T00:00:00Z','precision':'instant'},
            'end':{'state':'known','value':'2026-09-22T00:00:00Z','precision':'instant'}}
    field='reached_origin_record_count' if family=='SIT-M002' else 'seed_items_with_unresolved_ancestry_count'
    owner,job=job_pair();ledger=owner.witnesses
    positive=origins._origin_profile(prepared(source),ctx,ledger,job,family=family)
    baseline=SimpleNamespace(results=positive.results)
    assert check(baseline,field,'PC10').state=='met'
    assert_count(count_view(baseline,field),('origin',) if family=='SIT-M002' else ())
    if changed=='none':return
    cases.by_id(source,changed)['scope']['effective_window']=cases.window()
    owner.finish_job(job);job=owner.start_job()
    output=origins._origin_profile(prepared(source),ctx,ledger,job,family=family)
    out=SimpleNamespace(results=output.results);actual=check(out,field,'PC10')
    assert actual.state=='unknown'
    assert changed in {ref.identifier for ref in actual.input_refs}
    reasons=[reason for reason in leaf(out,field).reason_refs if reason.code=='time_applicability_unknown']
    assert reasons and changed in {ref.identifier for reason in reasons for ref in reason.input_refs}
    expected=('origin',) if family=='SIT-M002' and changed=='coverage' else () if family=='SIT-M002' else ('e',)
    assert_count(count_view(out,field),expected)
    if family=='SIT-M002' and changed=='coverage':
        assert_count(count_view(out,'documentary_origin_boundary_record_count'),())
        assert check(out,'documentary_origin_boundary_record_count','PC10').state=='unknown'


@pytest.mark.parametrize('issue',('basis','conflict'))
def test_boundary_checks_follow_required_coverage_basis_and_conflict_without_poisoning_other_premises(issue):
    source=small();baseline=run(source)[0]
    assert_count(count_view(baseline,'documentary_origin_boundary_record_count'),('origin',))
    assert check(baseline,'documentary_origin_boundary_record_count','PC05').state=='met'
    assert check(baseline,'documentary_origin_boundary_record_count','PC09').state=='met'
    if issue=='basis':
        support=copy.deepcopy(cases.by_id(source,'support'))
        support.update(id='coverage-only-support',reference_kind='external_locator',availability='locator_only',
                       excerpt=None,locator='https://example.invalid/coverage-premise-only')
        source['evidence_references'].append(support)
        cases.by_id(source,'coverage')['provenance']['evidence_ref_ids']=['coverage-only-support']
        failing,unaffected,reason='PC05','PC09','support_uninspectable'
    else:
        counter=copy.deepcopy(cases.by_id(source,'coverage'));counter['id']='coverage-counter'
        counter['data']['details'].update(state='partial',universe_enumerated=False)
        counter['gaps']=[{'field':'data.details.member_refs','reason':'not_recorded',
                         'detail':'Whether the stated finite history is complete is disputed.'}]
        source['assertions'].append(counter)
        source['assertions'].append(cases.assertion('coverage-conflict','assessment',{
            'assessment_kind':'conflict','subject_refs':['coverage','coverage-counter'],
            'details':{'conflict_kind':'scope_dispute','resolution_state':'unresolved',
                       'resolution_evaluation_ref':None,'scope_note':'The upstream coverage premise is disputed.'}}))
        failing,unaffected,reason='PC09','PC05','premise_disputed'
    out=run(source)[0]
    assert_count(count_view(out,'reached_origin_record_count'),('origin',))
    assert_count(count_view(out,'documentary_origin_boundary_record_count'),())
    assert_count(count_view(out,'seed_items_with_unresolved_ancestry_count'),('e',))
    assert check(out,'documentary_origin_boundary_record_count',failing).state=='unmet'
    assert check(out,'documentary_origin_boundary_record_count',unaffected).state=='met'
    refs={ref.identifier for ref in check(out,'documentary_origin_boundary_record_count',failing).input_refs}
    assert 'coverage' in refs
    if issue=='conflict':assert 'coverage-conflict' in refs
    row=leaf(out,'documentary_origin_boundary_record_count')
    actual=[item for item in row.reason_refs if item.code==reason]
    assert actual and 'coverage' in {ref.identifier for item in actual for ref in item.input_refs}
    disclosure=disclosures(out,'origin_boundary_disclosures')['boundary0']
    assert disclosure['provenance']==cases.by_id(source,'boundary0')['provenance']
    assert disclosure['qualification_state']=='unmet' and reason in disclosure['reason_codes']


def test_unrelated_coverage_conflict_does_not_change_applicable_boundary_checks():
    source=small();baseline=run(source)[0]
    assert_count(count_view(baseline,'documentary_origin_boundary_record_count'),('origin',))
    other=add_coverage(source,('e2','origin2'),subjects=('origin2',),identifier='unrelated-coverage')
    counter=copy.deepcopy(other);counter['id']='unrelated-counter'
    counter['data']['details'].update(state='partial',universe_enumerated=False)
    source['assertions'].append(counter)
    source['assertions'].append(cases.assertion('unrelated-conflict','assessment',{
        'assessment_kind':'conflict','subject_refs':['unrelated-coverage','unrelated-counter'],
        'details':{'conflict_kind':'scope_dispute','resolution_state':'unresolved',
                   'resolution_evaluation_ref':None,'scope_note':'Only the disconnected e2 history is disputed.'}}))
    out=run(source)[0]
    assert_count(count_view(out,'documentary_origin_boundary_record_count'),('origin',))
    assert_count(count_view(out,'seed_items_with_unresolved_ancestry_count'),())
    for identifier in ('PC05','PC06','PC07','PC09'):
        actual=check(out,'documentary_origin_boundary_record_count',identifier)
        assert actual.state=='met'
        assert 'unrelated-conflict' not in {ref.identifier for ref in actual.input_refs}


@pytest.mark.parametrize('family',('SIT-M002','SIT-M007'))
@pytest.mark.parametrize('coverage_state',('missing','partial'))
def test_pc06_distinguishes_absent_coverage_from_supplied_incomplete_coverage(family,coverage_state):
    source=small(roles=());baseline=run(source,family=family)[0]
    field='reached_origin_record_count' if family=='SIT-M002' else 'seed_items_with_unresolved_ancestry_count'
    assert check(baseline,field,'PC06').state=='met'
    if coverage_state=='missing':
        source['assertions']=[item for item in source['assertions'] if item['id']!='coverage']
        source['inquiries'][0]['coverage_assertion_refs']=[]
    else:
        cases.by_id(source,'coverage')['data']['details'].update(state='partial',universe_enumerated=False)
    out=run(source,family=family)[0]
    actual=check(out,field,'PC06')
    assert actual.state==('unknown' if coverage_state=='missing' else 'unmet')
    assert_count(count_view(out,field),('origin',) if family=='SIT-M002' else ('e',))
    assert ('coverage' in {ref.identifier for ref in actual.input_refs}) is (coverage_state=='partial')
    assert 'upstream_coverage_incomplete' in {reason.code for reason in leaf(out,field).reason_refs}


def test_family_selection_is_explicit_and_never_emits_the_other_familys_leaves():
    snapshot=prepared(small());ctx=context(small());owner,job=job_pair();ledger=owner.witnesses
    for invalid in ('SIT-M004','both',None):
        with pytest.raises(TypeError):origins._origin_profile(snapshot,ctx,ledger,job,family=invalid)
    with pytest.raises(TypeError):origins._origin_profile(snapshot,ctx,ledger,job)


@pytest.mark.parametrize('invalid',('empty_predicates','partial_predicates','extra_predicate','wrong_view',
                                   'empty_claim','multiple_claims','unselected_dimension'))
def test_origin_context_requires_one_exact_claim_selected_dimension_and_all_parent_types(invalid):
    source=small();source['inquiries'][0]['target_claim_refs']=['claim','claim2']
    snapshot=prepared(source);ctx=context(source);owner,job=job_pair();ledger=owner.witnesses
    baseline=origins._origin_profile(snapshot,ctx,ledger,job,family='SIT-M002')
    assert_count(count_view(SimpleNamespace(results=baseline.results),'reached_origin_record_count'),('origin',))
    changes={
        'empty_predicates':{'relation_types':()},
        'partial_predicates':{'relation_types':PARENTS[:-1]},
        'extra_predicate':{'relation_types':PARENTS+('cites',)},
        'wrong_view':{'graph_view':'citation'},
        'empty_claim':{'claim_refs':()},
        'multiple_claims':{'claim_refs':('claim','claim2')},
        'unselected_dimension':{'dependency_dimension':'analytical_method'},
    }
    owner.finish_job(job);job=owner.start_job()
    with pytest.raises(TypeError):
        origins._origin_profile(snapshot,replace(ctx,**changes[invalid]),ledger,job,family='SIT-M002')


def test_origin_results_reuse_only_completed_facts_in_the_same_current_job():
    out,facts,owner,job=run(small(),family='SIT-M002')
    before=owner.used
    witness_count=owner.witnesses._retained_witnesses
    again=origins._origin_results(facts,job,family='SIT-M002')
    assert type(again) is tuple
    assert {row.ref.field_key for row in again}=={row.ref.field_key for row in out.results}
    assert owner.used>before
    assert owner.witnesses._retained_witnesses==witness_count
    with pytest.raises(FrozenInstanceError):facts.affected_seeds=()
    owner.finish_job(job);next_job=owner.start_job()
    with pytest.raises(TypeError):origins._origin_results(facts,next_job,family='SIT-M002')


@pytest.mark.parametrize('remaining',(0,200))
def test_origin_profile_resource_stop_is_sticky_and_never_returns_partial_counts(remaining,monkeypatch):
    monkeypatch.setattr(resources,'monotonic_ns',lambda:100)
    source=small();snapshot=prepared(source);ctx=context(source);owner,job=job_pair();ledger=owner.witnesses
    job.charge(1_000_000-job.used-remaining);before=job.used
    with pytest.raises(_AnalysisAborted) as stopped:
        origins._origin_profile(snapshot,ctx,ledger,job,family='SIT-M002')
    assert stopped.value.limit_id=='WU9-L11'
    assert stopped.value.stop.input_state=='accepted'
    if remaining:assert job.used>before
    with pytest.raises(_AnalysisAborted) as repeated:
        origins._origin_profile(snapshot,ctx,ledger,job,family='SIT-M007')
    assert repeated.value is stopped.value


def test_origin_profile_global_budget_and_finalization_port_cannot_restart_analysis(monkeypatch):
    monkeypatch.setattr(resources,'monotonic_ns',lambda:100)
    source=small();snapshot=prepared(source);ctx=context(source)
    owner=resources._new_analysis_budget();owner.charge(9_998_964)
    owner.record_input_acceptance();job=owner.start_job();ledger=owner.witnesses
    owner.charge(10_000_000-owner.used)
    with pytest.raises(_AnalysisAborted) as stopped:
        origins._origin_profile(snapshot,ctx,ledger,job,family='SIT-M007')
    assert stopped.value.limit_id=='WU9-L11' and owner.used==10_000_000
    other,port=job_pair();other_ledger=other.witnesses
    port.charge(1_000_000-port.used)
    with pytest.raises(_AnalysisAborted):port.charge(1)
    finalizer=other.begin_finalization();before=other.used
    with pytest.raises(TypeError):origins._origin_profile(snapshot,ctx,other_ledger,finalizer,family='SIT-M002')
    assert other.used==before


def test_origin_profile_deadline_cancellation_and_failure_remain_execution_states(monkeypatch):
    clock=[100];monkeypatch.setattr(resources,'monotonic_ns',lambda:clock[0])
    source=small();snapshot=prepared(source);ctx=context(source)
    owner,job=job_pair();ledger=owner.witnesses;clock[0]+=60_000_000_001
    with pytest.raises(_AnalysisAborted) as timed:
        origins._origin_profile(snapshot,ctx,ledger,job,family='SIT-M007')
    assert timed.value.limit_id=='WU9-L12'
    clock[0]=100;owner,job=job_pair();ledger=owner.witnesses
    def cancelled():raise KeyboardInterrupt('FICTIONAL_PRIVATE_ORIGIN_PAYLOAD')
    monkeypatch.setattr(resources,'monotonic_ns',cancelled)
    with pytest.raises(_AuditCancelled) as cancellation:
        origins._origin_profile(snapshot,ctx,ledger,job,family='SIT-M002')
    assert cancellation.value.input_state=='accepted'
    assert 'FICTIONAL_PRIVATE_ORIGIN_PAYLOAD' not in str(cancellation.value)
    monkeypatch.setattr(resources,'monotonic_ns',lambda:100)
    owner,job=job_pair();ledger=owner.witnesses;owner.finish_job(job);owner.start_job()
    with pytest.raises(_AnalysisAborted) as failure:
        origins._origin_profile(snapshot,ctx,ledger,job,family='SIT-M002')
    assert failure.value.stop.reason_code=='execution_failed'


def test_origin_witnesses_use_the_shared_invocation_ledger_and_cannot_reset_limits(monkeypatch):
    from source_integrity_toolkit.validation.limits import _WitnessLedger
    monkeypatch.setattr(resources,'monotonic_ns',lambda:100)
    source=small();snapshot=prepared(source);ctx=context(source)
    owner,job=job_pair();ledger=owner.witnesses
    with pytest.raises(TypeError):origins._origin_profile(snapshot,ctx,_WitnessLedger(job),job,family='SIT-M002')
    output=origins._origin_profile(snapshot,ctx,ledger,job,family='SIT-M002')
    before=(ledger._retained_witnesses,ledger._retained_members)
    assert before[0]==len(output.witnesses)>0
    assert before[1]==sum(witness.member_count for witness in output.witnesses)>0
    owner.finish_job(job);job=owner.start_job()
    ledger.retain(ledger.reserve(witnesses=20_000-ledger._retained_witnesses))
    with pytest.raises(_AnalysisAborted) as stopped:
        origins._origin_profile(snapshot,ctx,ledger,job,family='SIT-M007')
    assert stopped.value.limit_id=='WU9-L13'
    assert ledger._retained_witnesses==20_000
