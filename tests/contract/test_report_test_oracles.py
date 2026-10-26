# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Case-bound, product-independent Phase 4 report and byte oracles.

The accepted specifications and an independently authored finite dossier supply
these expectations. This module neither imports the product nor generates or
updates golden files. Its equality rule deliberately applies only to the named
reference case; it is not another report validator or a new production API.
"""
import copy
import hashlib
import json
from pathlib import Path
import re

import pytest

ROOT = Path(__file__).resolve().parents[2]
GOLDEN = ROOT / 'tests' / 'golden'
FIXTURE = ROOT / 'tests' / 'fixtures' / 'micro' / 'phase4_public_cases.json'
ROOT_ORDER = (
    'contract_version', 'report_kind', 'report_id', 'run', 'input_identity',
    'input_validation', 'scopes', 'populations', 'basis_index', 'capabilities',
    'checks', 'observability_domains', 'results', 'findings', 'reasons',
    'release_limits',
)


def _expectations():
    return json.loads((GOLDEN / 'phase4_report_expectations.json').read_bytes())


def _reference():
    return _expectations()['reference_document']


def _strict_equal(actual, expected, path='$'):
    """Types matter: Python's True == 1 must not erase a count mutation."""
    assert type(actual) is type(expected), path + ': type'
    if type(expected) is dict:
        assert actual.keys() == expected.keys(), path + ': object members'
        for key in expected:
            _strict_equal(actual[key], expected[key], path + '.' + key)
    elif type(expected) is list:
        assert len(actual) == len(expected), path + ': array length'
        for index, value in enumerate(expected):
            _strict_equal(actual[index], value, path + '[' + str(index) + ']')
    else:
        assert actual == expected, path + ': value'


def _assert_reference_document(candidate):
    _strict_equal(candidate, _reference())


def _pairs_no_duplicates(pairs):
    result = {}
    for key, value in pairs:
        assert key not in result, 'duplicate JSON member'
        result[key] = value
    return result


def _decode_json(raw):
    return json.loads(raw, object_pairs_hook=_pairs_no_duplicates,
                      parse_constant=lambda value: (_ for _ in ()).throw(AssertionError(value)))


def _assert_reference_json(raw):
    assert type(raw) is bytes
    assert raw.endswith(b'\n') and not raw.endswith(b'\n\n')
    assert b'\r' not in raw and b'\xef\xbb\xbf' not in raw
    _assert_reference_document(_decode_json(raw))
    record = _expectations()['exact_bytes']['json']
    assert len(raw) == record['size_bytes']
    assert hashlib.sha256(raw).hexdigest() == record['sha256']


def _six_places(numerator, denominator):
    """Independent integer half-up; no floating point or product encoder."""
    whole, remainder = divmod(numerator * 1000000, denominator)
    if remainder * 2 >= denominator:
        whole += 1
    return str(whole // 1000000) + '.' + str(whole % 1000000).zfill(6)


def _parse_reference_markdown(raw):
    """Read fixed blocks independently; never execute or render source text."""
    assert type(raw) is bytes
    text = raw.decode('utf-8')
    assert text.endswith('\n') and not text.endswith('\n\n') and '\r' not in text
    expected = _reference()
    prefix = ('# Source Integrity Audit\n\nReport kind: ' + expected['report_kind'] +
              '\nProcessing state: ' + expected['run']['processing_state'] +
              '\nInput state: ' + expected['input_validation']['state'] + '\n\n')
    assert text.startswith(prefix)
    position = len(prefix)

    def literal(value):
        nonlocal position
        assert text.startswith(value, position), 'fixed Markdown layout at ' + str(position)
        position += len(value)

    def block():
        nonlocal position
        start = position
        end = text.find('\n', start)
        assert end >= 0
        opening = text[start:end]
        assert re.fullmatch(r'`{3,}json', opening), 'JSON fence'
        fence = opening[:-4]
        position = end + 1
        end = text.find('\n' + fence + '\n', position)
        assert end >= 0, 'closed fence'
        body = text[position:end]
        longest = max((len(run) for run in re.findall(r'`+', body)), default=0)
        assert len(fence) == max(3, longest + 1), 'minimal safe fence'
        value = _decode_json(body)
        # Indentation is independently checked per line; exact bytes are pinned
        # separately, so parsing cannot bless whitespace/canonicalization drift.
        for line in body.split('\n'):
            assert '\t' not in line
            assert (len(line) - len(line.lstrip(' '))) % 2 == 0
        position = end + 1 + len(fence) + 1
        return value

    document = {}
    reasons = {row['id']: row for row in expected['reasons']}
    for root_index, name in enumerate(ROOT_ORDER):
        literal('## ' + name + '\n\n')
        if name != 'results' or not expected['results']:
            document[name] = block()
            if root_index != len(ROOT_ORDER) - 1:
                literal('\n')
            continue
        rows = []
        for result in expected['results']:
            literal('### ' + result['id'] + ': ' + result['field_key'] + '\n\n')
            row = block(); rows.append(row); literal('\n')
            if result['result_state'] == 'available' and result['value_kind'] == 'fraction':
                fraction = result['value']; n, d = fraction['numerator'], fraction['denominator']
                literal('Decimal display: ' + str(n) + '/' + str(d) + ' = ' + _six_places(n, d) + '\n\n')
            literal('Reason details\n\n')
            actual_reasons = block()
            _strict_equal(actual_reasons, [reasons[identifier] for identifier in result['reason_refs']])
            literal('\n')
        document[name] = rows
    assert position == len(text), 'trailing/omitted Markdown content'
    return document


def _assert_reference_markdown(raw):
    _assert_reference_document(_parse_reference_markdown(raw))
    record = _expectations()['exact_bytes']['markdown']
    assert len(raw) == record['size_bytes']
    assert hashlib.sha256(raw).hexdigest() == record['sha256']


def _result(document, field):
    rows = [row for row in document['results'] if row['field_key'] == field]
    assert len(rows) == 1, 'mutant target must be one exact cell'
    return rows[0]


def test_reference_baseline_matches_dossier_and_both_exact_formats():
    fixture = json.loads(FIXTURE.read_bytes())['cases'][0]
    source = fixture['dossier']
    assert fixture['id'] == 'P4-REFERENCE-ONE-ORIGIN'
    assert source['inquiries'][0]['seed_evidence_refs'] == ['P4-E1']
    assert source['inquiries'][0]['dependency_dimensions'] == ['acquisition']
    records = {row['id']: row for row in source['records']}
    assert records['P4-E1']['data']['claim_ref'] == 'P4-CLAIM'
    assert records['P4-E1']['data']['artifact_ref'] == 'P4-ART'
    relations = [row for row in source['assertions'] if row['assertion_kind'] == 'relation']
    assert len(relations) == 1
    assert relations[0]['data'] == {'predicate': 'originates_from', 'from_ref': 'P4-E1',
                                   'to_ref': 'P4-O1', 'polarity': 'affirmed',
                                   'dimension': 'acquisition', 'details': {}}
    document = _reference()
    assert tuple(document) == ROOT_ORDER
    assert len(document['results']) == 78
    assert len({row['field_key'] for row in document['results']}) == 57
    assert len(document['findings']) == 22
    assert len(document['checks']) == 671
    assert len(document['reasons']) == 38
    findings = {row['id']: row for row in document['findings']}
    traces = [(row, component) for row in document['findings']
              for component in row['witness']['components']
              if component['type'] == 'graph_witness' and component['kind'] == 'complete_trace']
    assert sorted(component['member_count'] for _, component in traces) == [5, 6]
    for field, count in [('single_origin_contribution_hhi', 6), ('inherited_only_seed_fraction', 5)]:
        result = _result(document, field)
        assert len(result['witness_refs']) == 1
        finding = findings[result['witness_refs'][0]]
        assert finding['scope_ref'] == result['scope_ref']
        assert finding['condition_code'] == 'transformation_path_witness'
        trace = next(c for c in finding['witness']['components'] if c['kind'] == 'complete_trace')
        assert trace['member_count'] == count
        assert len(trace['observations']) == 1
    scan_rows = _result(document, 'corrective_independence_disclosures')['value']['records']
    assert len(scan_rows) == 1
    assert scan_rows[0]['source'] == {'collection': 'inquiries', 'identifier': 'P4-I001', 'selector': 'target_object_refs'}
    assert scan_rows[0]['fields']['native_record']['target_object_refs'] == []
    assert scan_rows[0]['qualifications'] == [
        'Actual owner selection/source reference slot; this record does not establish an applicable review or independent process.']
    assert len(document['capabilities']) == 15
    assert len(document['observability_domains']) == 5
    for field, wanted in [('documentary_origin_resolution_fraction', {'numerator': 1, 'denominator': 1}),
                          ('single_origin_contribution_hhi', {'numerator': 1, 'denominator': 1}),
                          ('inherited_only_seed_fraction', {'numerator': 0, 'denominator': 1})]:
        row = _result(document, field)
        assert row['execution_state'] == 'completed' and row['result_state'] == 'available'
        _strict_equal(row['value'], wanted)
    interval = _result(document, 'inherited_only_completion_interval')
    assert interval['result_state'] == 'not_applicable' and interval['value'] is None
    reasons = {row['id']: row for row in document['reasons']}
    assert 'completion_interval_not_needed' in [reasons[r]['code'] for r in interval['reason_refs']]
    json_bytes = (GOLDEN / 'phase4_reference_report.json').read_bytes()
    markdown_bytes = (GOLDEN / 'phase4_reference_report.md').read_bytes()
    _assert_reference_json(json_bytes)
    _assert_reference_markdown(markdown_bytes)
    for excluded in fixture['disclosure_controls']['excluded_values']:
        assert excluded.encode() not in json_bytes and excluded.encode() not in markdown_bytes
    for name in ('retained_method', 'retained_qualification'):
        assert fixture['disclosure_controls'][name].encode() in json_bytes
        assert fixture['disclosure_controls'][name].encode() in markdown_bytes
    assert b'````json\n' in markdown_bytes


@pytest.mark.parametrize('name', ROOT_ORDER)
@pytest.mark.parametrize('change', ('missing', 'extra'))
def test_root_member_mutants_are_rejected_after_positive(name, change):
    baseline = _reference(); _assert_reference_document(baseline)
    changed = copy.deepcopy(baseline)
    if change == 'missing':
        del changed[name]
    else:
        changed['extra_' + name] = None
    with pytest.raises(AssertionError):
        _assert_reference_document(changed)


@pytest.mark.parametrize('collection', ('run', 'input_identity', 'input_validation', 'scopes',
    'populations', 'basis_index', 'capabilities', 'checks', 'observability_domains',
    'results', 'findings', 'reasons'))
@pytest.mark.parametrize('change', ('missing', 'extra'))
def test_nested_member_mutants_are_rejected_after_positive(collection, change):
    baseline = _reference(); _assert_reference_document(baseline)
    changed = copy.deepcopy(baseline)
    value = changed[collection]
    if type(value) is list:
        assert value, 'this reference intentionally exercises the nested type'
        value = value[0]
    if change == 'missing':
        del value[next(iter(value))]
    else:
        value['unexpected_member'] = None
    with pytest.raises(AssertionError):
        _assert_reference_document(changed)


@pytest.mark.parametrize('mutation', ('boolean_count', 'wrong_numerator', 'wrong_denominator',
    'fabricated_missing_count', 'illegal_execution_pair', 'missing_reason', 'lost_qualification',
    'input_report_namespace', 'lost_scope', 'native_state_upgrade', 'basis_upgrade',
    'invented_score', 'private_excerpt', 'drop_trace_observation', 'wrong_trace_scope',
    'human_selector_loss', 'native_unknown_time', 'incidence_origin_loss'))
def test_semantic_single_property_mutants_are_rejected_after_positive(mutation):
    baseline = _reference(); _assert_reference_document(baseline)
    changed = copy.deepcopy(baseline)
    if mutation == 'boolean_count':
        _result(changed, 'seed_evidence_item_count')['value'] = True
    elif mutation == 'wrong_numerator':
        _result(changed, 'single_origin_contribution_hhi')['value']['numerator'] = 0
    elif mutation == 'wrong_denominator':
        _result(changed, 'inherited_only_seed_fraction')['value']['denominator'] = 0
    elif mutation == 'fabricated_missing_count':
        _result(changed, 'submitted_comparison_member_count')['value'] = 0
    elif mutation == 'illegal_execution_pair':
        _result(changed, 'seed_evidence_item_count')['execution_state'] = 'interrupted'
    elif mutation == 'missing_reason':
        _result(changed, 'submitted_comparison_member_count')['reason_refs'] = []
    elif mutation == 'lost_qualification':
        next(row for row in changed['basis_index'] if row['qualifications'])['qualifications'] = []
    elif mutation == 'input_report_namespace':
        changed['scopes'][0]['inquiry_ref'] = changed['report_id']
    elif mutation == 'lost_scope':
        changed['results'].pop(next(i for i, row in enumerate(changed['results']) if row['field_key'] == 'anomaly_context_disclosures'))
    elif mutation == 'native_state_upgrade':
        value = _result(changed, 'coverage_disclosures')['value']['records'][0]['fields']
        value['native_record']['data']['details']['state'] = 'unknown'
    elif mutation == 'basis_upgrade':
        next(row for row in changed['basis_index'] if row['basis_kind'] == 'declaration')['basis_kind'] = 'documented_record'
    elif mutation == 'invented_score':
        changed['integrity_score'] = 1
    elif mutation == 'private_excerpt':
        changed['basis_index'][0]['excerpt'] = 'P4-PRIVATE-EXCERPT-NOT-EXPORTED'
    elif mutation == 'drop_trace_observation':
        next(c for f in changed['findings'] for c in f['witness']['components']
             if c['type'] == 'graph_witness' and c['kind'] == 'complete_trace')['observations'] = []
    elif mutation == 'wrong_trace_scope':
        finding = next(f for f in changed['findings'] if any(
            c['type'] == 'graph_witness' and c['kind'] == 'complete_trace'
            for c in f['witness']['components']))
        finding['scope_ref'] = next(s['id'] for s in changed['scopes'] if s['id'] != finding['scope_ref'])
    elif mutation == 'human_selector_loss':
        _result(changed, 'corrective_independence_disclosures')['value']['records'][0]['source']['selector'] = None
    elif mutation == 'native_unknown_time':
        next(b for b in changed['basis_index'] if 'asserted_at' in b['time'])['time']['asserted_at']['state'] = 'known'
    elif mutation == 'incidence_origin_loss':
        _result(changed, 'origin_incidence_counts')['value']['origin_counts'] = []
    with pytest.raises(AssertionError):
        _assert_reference_document(changed)


@pytest.mark.parametrize('format_name', ('json', 'markdown'))
@pytest.mark.parametrize('mutation', ('extra_lf', 'crlf', 'changed_denominator', 'lost_qualification'))
def test_byte_mutants_are_rejected_after_positive(format_name, mutation):
    filename = 'phase4_reference_report.' + ('json' if format_name == 'json' else 'md')
    original = (GOLDEN / filename).read_bytes()
    check = _assert_reference_json if format_name == 'json' else _assert_reference_markdown
    check(original)
    if mutation == 'extra_lf':
        changed = original + b'\n'
    elif mutation == 'crlf':
        changed = original.replace(b'\n', b'\r\n')
    elif mutation == 'changed_denominator':
        pattern = rb'("denominator"\s*:\s*)1'
        changed, count = re.subn(pattern, rb'\g<1>2', original, count=1)
        assert count == 1
    else:
        phrase = b'Caller-supplied documentary premise ('
        assert phrase in original
        changed = original.replace(phrase, b'Independently authenticated premise (', 1)
    assert changed != original
    with pytest.raises((AssertionError, ValueError, UnicodeError)):
        check(changed)


@pytest.mark.parametrize('mutation', ('none', 'drop_duplicate', 'sort_scan', 'lose_selector', 'lose_limit', 'invent_qualification'))
def test_constructed_human_scan_slots_preserve_exact_source_material(mutation):
    example = _expectations()['constructed_mapping_oracles']['human_review_scan']
    expected = example['projected_rows']
    assert example['owner_member_count'] == (len(example['members']) +
        len(example['examined_assessments']) + len(example['source_refs'])) == 5
    assert [row['source'] for row in expected[:2]] == example['examined_assessments']
    assert [row['source'] for row in expected[2:]] == example['source_refs']
    assert expected[2] == expected[3]
    assert all(row['qualifications'] == [example['scan_qualification']] for row in expected[:2])
    assert all(row['qualifications'] == [example['source_qualification']] for row in expected[2:])
    _strict_equal(copy.deepcopy(expected), expected)  # accept before mutation
    if mutation == 'none':
        return
    changed = copy.deepcopy(expected)
    if mutation == 'drop_duplicate':
        changed.pop()
    elif mutation == 'sort_scan':
        changed[:2] = sorted(changed[:2], key=lambda row: row['source']['identifier'])
    elif mutation == 'lose_selector':
        changed[2]['source']['selector'] = None
    elif mutation == 'lose_limit':
        changed[0]['qualifications'] = []
    else:
        changed[0]['fields']['process_qualification_state'] = 'met'
    with pytest.raises(AssertionError):
        _strict_equal(changed, expected)
