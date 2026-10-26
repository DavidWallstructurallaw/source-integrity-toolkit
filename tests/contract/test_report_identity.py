# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W03 semantic identity controls at the trusted logical-assembly boundary.

Architecture 18.1 and governance 22.5 specify the expectations here. These
tests construct finite private fixtures; they do not claim a public audit ran
or turn the producer's output into an expected golden document.
"""
import copy
from dataclasses import fields, is_dataclass, replace
from types import SimpleNamespace

import pytest

from source_integrity_toolkit.contracts import report, results as r
from source_integrity_toolkit.reporting import assemble as assembly_product
from source_integrity_toolkit.runtime import boundary
from test_report_assembly import (
    RecordingPort, _assemble, _plain, _reference_dossier, _reference_outcome,
    _selected_disclosure,
)


@pytest.fixture(scope='module')
def reference():
    """One actual analysis supplies immutable inputs, never cached verdicts."""
    outcome = _reference_outcome()
    return outcome, _selected_disclosure(outcome)


def _document(reference, *, outcome=None, selection=None, port=None):
    original, selected = reference
    return _plain(_assemble(original if outcome is None else outcome,
                            selected if selection is None else selection,
                            port=port))


def _result_pair(outcome):
    first = next(row for row in outcome.results
                 if row.ref.diagnostic_id == 'SIT-M001' and
                 row.result_state == 'available')
    second = next(row for row in outcome.results
                  if row is not first and row.ref.scope is first.ref.scope and
                  row.result_state == 'available')
    return first, second


def _with_results(outcome, replacements):
    """Update actual navigation while retaining distinct Reason bodies.

    Private Reason._key deliberately excludes affected_result_refs. Object
    identity here only avoids adding the *same* fixture node twice; expected
    public identity is asserted from its full specified contents below.
    """
    rows = tuple(replacements.get(id(row), row) for row in outcome.results)
    by_slot = {row.ref._key(): row for row in rows}

    def reasons(links, originals):
        result = list(originals)
        present = {id(reason) for reason in result}
        for link in links:
            for reason in by_slot[link._key()].reason_refs:
                if id(reason) not in present:
                    result.append(reason)
                    present.add(id(reason))
        return tuple(result)

    capabilities = tuple(replace(cap, reason_refs=reasons(cap.result_refs,
                                                        cap.reason_refs))
                         for cap in outcome.capabilities)
    domains = tuple(replace(domain, reason_refs=reasons(domain.result_refs,
                                                      domain.reason_refs))
                    for domain in outcome.domains)
    return replace(outcome, results=rows, capabilities=capabilities,
                   domains=domains)


def _selection_plain(value):
    """Detach selected JSON containers while preserving explicit typed links."""
    if type(value) is report._ReportMapping:
        return {name: _selection_plain(value[name]) for name in value}
    if type(value) in (tuple, list):
        return [_selection_plain(item) for item in value]
    if type(value) is dict:
        return {name: _selection_plain(item) for name, item in value.items()}
    assert value is None or type(value) in (
        str, bool, int, r._InputRef, r._Scope, r._Population, r._BasisRef,
        r._ResultRef, r._WitnessRef, r._Reason, r._PrerequisiteCheck,
    )
    return value


def _selected_again(selection, *, basis_entries=None, disclosures=None,
                    finding_witnesses=None):

    return report._capture_report_disclosure(
        tuple((owner, _selection_plain(value)) for owner, value in
              (selection.basis_entries if basis_entries is None else basis_entries)),
        tuple((owner, _selection_plain(value)) for owner, value in
              (selection.disclosures if disclosures is None else disclosures)),
        tuple((owner, _selection_plain(value)) for owner, value in
              (selection.finding_witnesses if finding_witnesses is None else finding_witnesses)),
        RecordingPort(),
        owner_witnesses=tuple((owner, _selection_plain(value))
                              for owner, value in selection.owner_witnesses),
    )


def _rewrite_fixture(value, replacements, memo=None):
    """Rebuild only known trusted fixture nodes with coherent shared links.

    This is a test data operation. It never inspects the immutable prepared
    source or analysis plan and cannot supply a production projection rule.
    """
    if memo is None:
        memo = {}
    if id(value) in replacements:
        return replacements[id(value)]
    if id(value) in memo:
        return memo[id(value)]
    if type(value) is tuple:
        items = tuple(_rewrite_fixture(item, replacements, memo) for item in value)
        result = value if all(new is old for old, new in zip(value, items)) else items
    elif type(value) is list:
        items = [_rewrite_fixture(item, replacements, memo) for item in value]
        result = value if all(new is old for old, new in zip(value, items)) else items
    elif type(value) is dict:
        items = {name: _rewrite_fixture(item, replacements, memo)
                 for name, item in value.items()}
        result = value if all(items[name] is old for name, old in value.items()) else items
    elif is_dataclass(value) and (
            type(value).__module__ == r.__name__ or type(value) in (
                report._AnalyticalOutcome, report._Capability,
                report._DomainOutcome, report._PrivateFinding,
                report._JobOutcome, report._WitnessRecord, report._ReportMapping)):
        changes = {
            field.name: _rewrite_fixture(getattr(value, field.name), replacements, memo)
            for field in fields(value)
        }
        # Private Result constructors require their own Scope/Population/
        # WitnessRef links to share object identity. Keep untouched fixture
        # nodes, especially a Scope shared by several Results, exactly intact.
        result = (value if all(child is getattr(value, name)
                               for name, child in changes.items())
                  else replace(value, **changes))
    else:
        return value
    memo[id(value)] = result
    return result


def _coherent_changed_result(reference, original, changed):
    outcome, selected = reference
    replacements = {id(original): changed, id(original.ref): changed.ref}
    for old, new in zip(original.check_refs, changed.check_refs):
        replacements[id(old)] = new
    for old, new in zip(original.witness_refs, changed.witness_refs):
        replacements[id(old)] = new
    memo = {}
    rebuilt = _rewrite_fixture(outcome, replacements, memo)
    parts = [_rewrite_fixture(getattr(selected, name), replacements, memo)
             for name in ('basis_entries', 'disclosures', 'finding_witnesses',
                          'owner_witnesses')]
    selected = report._capture_report_disclosure(
        tuple((owner, _selection_plain(value)) for owner, value in parts[0]),
        tuple((owner, _selection_plain(value)) for owner, value in parts[1]),
        tuple((owner, _selection_plain(value)) for owner, value in parts[2]),
        RecordingPort(),
        owner_witnesses=tuple((owner, _selection_plain(value)) for owner, value in parts[3]),
    )
    return rebuilt, selected


def test_each_local_collection_has_its_own_sequential_identity(reference):
    document = _document(reference)
    assert document['report_id'] == 'SIT-RPT-000001'
    for collection, prefix in (
            ('scopes', 'SIT-SCP-'), ('populations', 'SIT-POP-'),
            ('basis_index', 'SIT-BAS-'), ('capabilities', 'SIT-CAP-'),
            ('checks', 'SIT-CHK-'), ('results', 'SIT-RES-'),
            ('findings', 'SIT-FND-'), ('reasons', 'SIT-RSN-')):
        rows = document[collection]
        assert rows, collection
        assert [row['id'] for row in rows] == [
            prefix + str(number).zfill(6) for number in range(1, len(rows) + 1)
        ], collection
    all_ids = [row['id'] for key in ('scopes', 'populations', 'basis_index',
                                    'capabilities', 'checks', 'results',
                                    'findings', 'reasons')
               for row in document[key]]
    assert len(all_ids) == len(set(all_ids))


def test_discovery_order_does_not_allocate_report_ids(reference):
    outcome, selected = reference
    reordered = replace(outcome,
                        results=tuple(reversed(outcome.results)),
                        findings=tuple(reversed(outcome.findings)),
                        witnesses=tuple(reversed(outcome.witnesses)),
                        capabilities=tuple(reversed(outcome.capabilities)),
                        domains=tuple(reversed(outcome.domains)),
                        jobs=tuple(reversed(outcome.jobs)))
    selection = _selected_again(
        selected, basis_entries=tuple(reversed(selected.basis_entries)),
        disclosures=tuple(reversed(selected.disclosures)),
        finding_witnesses=tuple(reversed(selected.finding_witnesses)))
    assert _document(reference, outcome=reordered, selection=selection) == _document(reference)


def test_input_entity_permutation_preserves_same_logical_report(reference):
    dossier = _reference_dossier()
    original = copy.deepcopy(dossier)
    for collection in ('inquiries', 'records', 'assertions', 'evidence_references'):
        dossier[collection].reverse()
    assert dossier != original
    outcome = boundary._analyze_value(dossier)
    assert outcome.input_state == 'accepted' and outcome.execution_state == 'completed'
    assert _document(reference, outcome=outcome,
                     selection=_selected_disclosure(outcome)) == _document(reference)
    # The assembler did not reorder the caller's mutable input in place.
    for collection in ('inquiries', 'records', 'assertions', 'evidence_references'):
        assert dossier[collection] == list(reversed(original[collection]))


def test_identical_result_and_explanatory_nodes_share_existing_ids(reference):
    outcome, selected = reference
    extra_result = replace(outcome.results[0])
    original_finding = outcome.findings[0]
    extra_finding = replace(original_finding)
    assert extra_result is not outcome.results[0] and extra_finding is not original_finding
    witness = next(body for owner, body in selected.finding_witnesses
                   if owner is original_finding)
    selection = _selected_again(selected,
        finding_witnesses=selected.finding_witnesses + ((extra_finding, witness),))
    duplicate = replace(outcome, results=outcome.results + (extra_result,),
                        findings=outcome.findings + (extra_finding,))
    assert _document(reference, outcome=duplicate, selection=selection) == _document(reference)


def test_unequal_semantic_body_for_one_result_slot_is_an_error(reference):
    outcome, unused = reference
    assert _document(reference)['results'], 'unchanged baseline must assemble first'
    original = outcome.results[0]
    conflicting = replace(original, interpretation_limit=
                          original.interpretation_limit + ' Different limitation.')
    conflicting_outcome = replace(outcome, results=outcome.results + (conflicting,))
    with pytest.raises(report._ReportContractError, match='invalid_report_contract'):
        _document(reference, outcome=conflicting_outcome)


def test_same_reason_anchor_keeps_different_affected_result_bodies(reference):
    outcome, unused = reference
    first, second = _result_pair(outcome)
    detail = 'Identity fixture: the exact affected Result set is part of this Reason.'
    one = r._Reason('premise_disputed', first.ref.scope, (first.ref,), (),
                    detail, 'conflict')
    two = r._Reason('premise_disputed', second.ref.scope, (second.ref,), (),
                    detail, 'conflict')
    assert one._key() == two._key()
    changed = _with_results(outcome, {
        id(first): replace(first, reason_refs=first.reason_refs + (one,)),
        id(second): replace(second, reason_refs=second.reason_refs + (two,)),
    })
    document = _document(reference, outcome=changed)
    reasons = [row for row in document['reasons'] if row['detail'] == detail]
    assert len(reasons) == 2
    assert reasons[0]['id'] != reasons[1]['id']
    expected = {row['id'] for row in document['results']
                if row['diagnostic_id'] == first.ref.diagnostic_id and
                row['field_key'] in (first.ref.field_key, second.ref.field_key)}
    assert {tuple(row['affected_result_refs']) for row in reasons} == {
        (identifier,) for identifier in expected
    }
    for reason in reasons:
        result = next(row for row in document['results']
                      if row['id'] == reason['affected_result_refs'][0])
        assert reason['id'] in result['reason_refs']


def test_same_scope_anchor_keeps_different_qualification_bodies(reference):
    outcome, unused = reference
    first, second = _result_pair(outcome)
    marker = 'Identity fixture: this scope retains a distinct qualification.'
    old_scope = second.ref.scope
    new_scope = replace(old_scope, qualifications=old_scope.qualifications + (marker,))
    assert new_scope._key() == old_scope._key()
    changed = _rewrite_fixture(second, {id(old_scope): new_scope})
    rebuilt, selected = _coherent_changed_result(reference, second, changed)
    document = _document(reference, outcome=rebuilt, selection=selected)
    rows = {row['field_key']: row for row in document['results']
            if row['diagnostic_id'] == first.ref.diagnostic_id}
    first_id = rows[first.ref.field_key]['scope_ref']
    second_id = rows[second.ref.field_key]['scope_ref']
    assert first_id != second_id
    scopes = {row['id']: row for row in document['scopes']}
    assert marker not in scopes[first_id]['qualifications']
    assert scopes[second_id]['qualifications'] == list(new_scope.qualifications)


def test_same_population_anchor_keeps_different_qualification_bodies(reference):
    outcome, unused = reference
    first = next(row for row in outcome.results
                 if row.value_kind == 'incidence' and row.result_state == 'available')
    second = next(row for row in outcome.results
                  if row is not first and row.value_kind == 'incidence' and
                  row.result_state == 'available' and
                  row.value.population is first.value.population)
    original_population = second.value.population
    marker = 'Identity fixture: this population retains a distinct qualification.'
    changed_population = replace(original_population,
                                 qualifications=original_population.qualifications + (marker,))
    assert changed_population._key() == original_population._key()
    changed = _rewrite_fixture(second, {
        id(original_population): changed_population,
        id(second.ref.scope): second.ref.scope,
    })
    rebuilt, selected = _coherent_changed_result(reference, second, changed)
    document = _document(reference, outcome=rebuilt, selection=selected)
    rows = {row['field_key']: row for row in document['results']
            if row['diagnostic_id'] == first.ref.diagnostic_id}
    first_id = rows[first.ref.field_key]['value']['population_ref']
    second_id = rows[second.ref.field_key]['value']['population_ref']
    assert first_id != second_id
    populations = {row['id']: row for row in document['populations']}
    assert marker not in populations[first_id]['qualifications']
    assert populations[second_id]['qualifications'] == list(changed_population.qualifications)


def test_reason_result_cycles_close_without_recursive_body_naming(reference):
    outcome, unused = reference
    first, second = _result_pair(outcome)
    refs = (first.ref, second.ref)
    left = r._Reason('premise_disputed', first.ref.scope, refs, (),
                     'Identity cycle left.', 'conflict')
    right = r._Reason('premise_disputed', first.ref.scope, refs, (),
                      'Identity cycle right.', 'conflict')
    changed = _with_results(outcome, {
        id(first): replace(first, reason_refs=first.reason_refs + (left, right)),
        id(second): replace(second, reason_refs=second.reason_refs + (left, right)),
    })
    port = RecordingPort(stop_after=10_000_000)
    document = _document(reference, outcome=changed, port=port)
    assert 0 < port.units <= 10_000_000 and port.checks > 0
    reasons = [row for row in document['reasons']
               if row['detail'] in ('Identity cycle left.', 'Identity cycle right.')]
    assert len(reasons) == 2
    assert reasons[0]['affected_result_refs'] == reasons[1]['affected_result_refs']
    assert len(reasons[0]['affected_result_refs']) == 2
    linked = set(reasons[0]['affected_result_refs'])
    for row in document['results']:
        if row['id'] in linked:
            assert {reason['id'] for reason in reasons} <= set(row['reason_refs'])
    reversed_left = replace(left, affected_result_refs=tuple(reversed(refs)))
    reversed_right = replace(right, affected_result_refs=tuple(reversed(refs)))
    reversed_outcome = _with_results(outcome, {
        id(first): replace(first, reason_refs=first.reason_refs +
                           (reversed_right, reversed_left)),
        id(second): replace(second, reason_refs=second.reason_refs +
                            (reversed_right, reversed_left)),
    })
    reversed_outcome = replace(reversed_outcome,
                               results=tuple(reversed(reversed_outcome.results)))
    assert _document(reference, outcome=reversed_outcome) == document


def test_registered_families_sort_numerically_and_null_scope_fields_first(reference):
    document = _document(reference)
    assert [row['diagnostic_id'] for row in document['capabilities']] == [
        'SIT-M' + str(number).zfill(3) for number in range(1, 16)
    ]
    family_numbers = [int(row['diagnostic_id'][5:]) for row in document['results']]
    assert family_numbers == sorted(family_numbers)
    first_scope = document['scopes'][0]
    assert first_scope['dependency_dimension'] is None
    assert first_scope['graph_view'] is None
    assert first_scope['requested_time'] is None
    assert any(row['dependency_dimension'] is not None for row in document['scopes'])
    # Hold the Inquiry, claims, targets and remaining scope fields fixed so
    # the null-vs-text comparison is decisive, rather than merely incidental
    # to unrelated earlier components of the reference's scope keys.
    outcome, unused = reference
    first, second = _result_pair(outcome)
    assert first.ref.scope.dependency_dimension is None
    qualified = replace(second.ref.scope, dependency_dimension='acquisition')
    changed = _rewrite_fixture(second, {id(second.ref.scope): qualified})
    rebuilt, selected = _coherent_changed_result(reference, second, changed)
    document = _document(reference, outcome=rebuilt, selection=selected)
    rows = {row['field_key']: row for row in document['results']
            if row['diagnostic_id'] == first.ref.diagnostic_id}
    null_id = rows[first.ref.field_key]['scope_ref']
    text_id = rows[second.ref.field_key]['scope_ref']
    assert null_id < text_id
    scopes = {row['id']: row for row in document['scopes']}
    assert scopes[null_id]['dependency_dimension'] is None
    assert scopes[text_id]['dependency_dimension'] == 'acquisition'


def test_distinct_input_ids_do_not_merge_identical_selected_basis_bodies(reference):
    outcome, selection = reference
    # These two independently named source records already carry exactly the
    # same selected declaration body in the reference; no evidence is altered
    # merely to make this identity control pass.
    first = next(pair for pair in selection.basis_entries
                 if pair[0].source.identifier == 'P4-ACTOR' and
                 pair[0].source.selector is None)
    second_owner, second_body = next(pair for pair in selection.basis_entries
                                    if pair[0].source.identifier == 'P4-CLAIM' and
                                    pair[0].source.selector is None)
    assert _selection_plain(first[1]) == _selection_plain(second_body)
    document = _document(reference)
    sources = {(first[0].source.collection, first[0].source.identifier,
                first[0].source.selector),
               (second_owner.source.collection, second_owner.source.identifier,
                second_owner.source.selector)}
    rows = [row for row in document['basis_index']
            if (row['source']['collection'], row['source']['identifier'],
                row['source']['selector']) in sources]
    assert len(rows) == 2
    assert rows[0]['id'] != rows[1]['id']
    assert {row['source']['identifier'] for row in rows} == {
        first[0].source.identifier, second_owner.source.identifier
    }
    assert {key: value for key, value in rows[0].items() if key not in ('id', 'source')} == {
        key: value for key, value in rows[1].items() if key not in ('id', 'source')
    }


@pytest.mark.parametrize('marker', (
    ['z native first', 'a native second', 'z native first'],
    ['witness_links', 'literal'],
))
def test_selected_native_qualification_sequence_is_not_sorted_or_deduplicated(reference,
                                                                              marker):
    outcome, selection = reference
    owner, frozen = selection.disclosures[0]
    payload = _selection_plain(frozen)
    assert payload['records']
    payload['records'][0]['qualifications'] = marker
    selected = _selected_again(selection,
                               disclosures=((owner, payload),) + selection.disclosures[1:])
    document = _document(reference, selection=selected)
    found = []

    def walk(value):
        if type(value) is dict:
            if value.get('qualifications') == marker:
                found.append(value)
            for nested in value.values():
                walk(nested)
        elif type(value) is list:
            for nested in value:
                walk(nested)

    walk(document)
    assert found, 'native sequence and duplicate occurrence must survive assembly'


def _small_trace_homes(*, same_home, reverse, alias_scope=False):
    """Exercise retained-trace bookkeeping without a fabricated full audit.

    Two trusted immutable trace payloads contain different starts. The tiny
    container deliberately is not _AnalyticalOutcome and cannot enter the
    report entry point; only the isolated internal witness composition runs.
    Every expected member below is independently stated in this fixture.
    """
    inquiry = r._InputRef('inquiries', 'IDENTITY-I')
    scope = r._Scope(inquiry, (), (), None, 'claim_origin',
                     'snapshot_structural', None, (), ('Finite identity fixture.',))
    source_refs = [r._InputRef('records', 'IDENTITY-' + name) for name in ('A', 'B')]
    witness_refs = [r._WitnessRef(scope, 'member_set', ('complete_trace', name))
                    for name in ('A', 'B')]
    owners, selections = [], []
    for source, witness_ref in zip(source_refs, witness_refs):
        node = ('node', source, 'evidence_item')
        material = {name: () for name in ('nodes', 'edges', 'members', 'internal_edges',
                    'exit_edges', 'starts', 'examined_nodes', 'examined_edges',
                    'frontiers', 'terminals', 'observations')}
        material.update(starts=(node,), examined_nodes=(node,), target=None)
        payload = ('graph_witness', 'complete_trace', inquiry, (), None,
                   'claim_origin', (), tuple(material.items()), 2)
        retained_ref = (replace(witness_ref, scope=replace(scope))
                        if alias_scope else witness_ref)
        owner = report._WitnessRecord((retained_ref,), (payload,), (source,), 2)
        owners.append(owner)
        public_node = {'kind': 'evidence_item', 'ref': {
            'collection': 'records', 'identifier': source.identifier, 'selector': None}}
        body = {name: [] for name in ('nodes', 'edges', 'members', 'internal_edges',
                    'exit_edges', 'starts', 'examined_nodes', 'examined_edges',
                    'frontiers', 'terminals', 'observations')}
        body.update(type='graph_witness', kind='complete_trace', member_count=2,
                    starts=[public_node], examined_nodes=[public_node], target=None)
        selections.append((owner, {'input_refs': [source], 'components': [body]}))
    refs = [r._ResultRef('SIT-M008', 'evaluator_overlap_witnesses', scope)]
    if not same_home:
        refs.append(r._ResultRef('SIT-M011', 'declared_correction_route_witnesses', scope))
    results, findings, finding_selections = [], [], []
    for index, ref in enumerate(refs):
        links = tuple(witness_refs) if same_home else (witness_refs[index],)
        result = r._Result(ref, (), 'completed', 'available', 'graph_derivation',
            'witness_collection', r._WitnessCollection(links), (), (), links, (),
            'Trusted witness composition fixture; no analytical execution claim.')
        results.append(result)
        finding = report._PrivateFinding('qualification_gap', 'verification_scope_limitation',
            (ref.diagnostic_id,), (), scope, (), (),
            report._DetachedFindingWitness((inquiry,),
                (('selected_members', (inquiry,), 1),), 2), (), (), (ref,),
            'Existing fixture finding ' + str(index), 'Finite internal scope only.', ())
        findings.append(finding)
        finding_selections.append((finding, {'input_refs': [inquiry], 'components': [{
            'type': 'selected_members', 'members': [inquiry], 'member_count': 1}]}))
    if reverse:
        owners.reverse()
        results.reverse()
        findings.reverse()
        selections.reverse()
        finding_selections.reverse()
    selected = report._capture_report_disclosure((), (), tuple(finding_selections),
                    RecordingPort(), owner_witnesses=tuple(selections))
    container = SimpleNamespace(results=tuple(results), findings=tuple(findings),
                                witnesses=tuple(owners))
    port = RecordingPort(stop_after=10_000_000)
    state = assembly_product._Assembly(container, selected, port)
    for result in container.results:
        state.result(result)
    for finding in container.findings:
        state.finding(finding)
    assembly_product._assemble_witnesses(state)
    state.identities_for_rows()
    actual = {}
    for collection in ('results', 'findings'):
        actual[collection] = []
        for row in state.rows[collection]:
            body = state.resolve(row['body'])
            body['id'] = state.resolve_link(row['owner'])
            actual[collection].append(_selection_plain(body))
    assert 0 < port.units <= 10_000_000
    return actual


def test_small_trace_homes_keep_own_result_links_across_discovery_orders():
    forward = _small_trace_homes(same_home=False, reverse=False)
    backward = _small_trace_homes(same_home=False, reverse=True)
    assert backward == forward
    findings = {row['id']: row for row in forward['findings']}
    assert len(findings) == 2
    for result in forward['results']:
        assert len(result['witness_refs']) == 1
        finding = findings[result['witness_refs'][0]]
        traces = [component for component in finding['witness']['components']
                  if component.get('kind') == 'complete_trace']
        assert len(traces) == 1
        expected = 'IDENTITY-A' if result['diagnostic_id'] == 'SIT-M008' else 'IDENTITY-B'
        assert [node['ref']['identifier'] for node in traces[0]['starts']] == [expected]
        assert [node['ref']['identifier'] for node in traces[0]['examined_nodes']] == [expected]
        assert finding['diagnostic_refs'] == [result['diagnostic_id']]


def test_small_same_finding_keeps_both_sequentially_appended_traces():
    forward = _small_trace_homes(same_home=True, reverse=False)
    backward = _small_trace_homes(same_home=True, reverse=True)
    assert backward == forward
    assert len(forward['findings']) == len(forward['results']) == 1
    finding = forward['findings'][0]
    assert forward['results'][0]['witness_refs'] == [finding['id']]
    components = finding['witness']['components']
    assert components[0]['type'] == 'selected_members'
    traces = [component for component in components if component.get('kind') == 'complete_trace']
    assert len(traces) == 2
    assert {node['ref']['identifier'] for trace in traces for node in trace['starts']} == {
        'IDENTITY-A', 'IDENTITY-B'}
    assert all(trace['member_count'] == 2 for trace in traces)


def test_small_retained_witness_scope_alias_is_value_equal():
    original = _small_trace_homes(same_home=False, reverse=False)
    aliases = _small_trace_homes(same_home=False, reverse=False, alias_scope=True)
    assert aliases == original
