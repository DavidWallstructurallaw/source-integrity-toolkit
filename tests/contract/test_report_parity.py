# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W06 exact Markdown and independent cross-format substantive controls.

The existing W02 reference bytes remain authoritative. The parser below reads
the prescribed blocks without rendering Markdown or invoking product helpers.
Component fixtures exercise representation only; actual analytical invocation,
both formats and final delivery on one ledger remain W07 work.
"""
import copy
from decimal import Decimal, ROUND_HALF_UP, localcontext
import importlib.util
import json
from pathlib import Path
import re

import pytest

from source_integrity_toolkit.contracts import report as contract
from source_integrity_toolkit.reporting.json_report import _encode_json_report
from source_integrity_toolkit.reporting.markdown_report import _encode_markdown_report
from source_integrity_toolkit.runtime.boundary import _analyze_value
from source_integrity_toolkit.runtime.disclosure import _assemble_selected_report


ROOT = Path(__file__).resolve().parents[2]
ROOT_ORDER = (
    'contract_version', 'report_kind', 'report_id', 'run', 'input_identity',
    'input_validation', 'scopes', 'populations', 'basis_index', 'capabilities',
    'checks', 'observability_domains', 'results', 'findings', 'reasons',
    'release_limits',
)


class ComponentPort:
    """Finite test-owned port, never an argument accepted by a public API."""
    def __init__(self):
        self.units = 0
        self.checks = 0
        self.output = {'json': 0, 'markdown': 0}

    def charge(self, units):
        assert type(units) is int and units >= 0
        assert self.units + units <= 10_000_000, 'finite component work limit'
        self.units += units

    def check(self):
        self.checks += 1

    def charge_output(self, encoding, count):
        assert type(encoding) is str and encoding in self.output
        assert type(count) is int and count >= 0
        assert self.output[encoding] + count <= 67_108_864
        self.output[encoding] += count


def _freeze_component(value):
    """Test construction of frozen representation components, not admission."""
    if type(value) is dict:
        return contract._ReportMapping(tuple((k, _freeze_component(v)) for k, v in value.items()))
    if type(value) is list:
        return tuple(_freeze_component(v) for v in value)
    assert value is None or type(value) in (str, int, bool)
    return value


def _plain(value):
    if type(value) is contract._ReportMapping:
        return {key: _plain(child) for key, child in value._pairs}
    if type(value) is tuple:
        return [_plain(child) for child in value]
    assert value is None or type(value) in (str, int, bool)
    return value


def _strict_equal(actual, expected, path='$'):
    assert type(actual) is type(expected), path + ': type'
    if type(expected) is dict:
        assert actual.keys() == expected.keys(), path + ': members'
        for key in expected:
            _strict_equal(actual[key], expected[key], path + '.' + key)
    elif type(expected) is list:
        assert len(actual) == len(expected), path + ': length'
        for index, value in enumerate(expected):
            _strict_equal(actual[index], value, path + '[' + str(index) + ']')
    else:
        assert actual == expected, path + ': value'


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        assert key not in result, 'duplicate JSON member'
        result[key] = value
    return result


def _decode(raw):
    def bad_constant(value):
        raise AssertionError('nonstandard JSON constant')
    return json.loads(raw, object_pairs_hook=_pairs, parse_constant=bad_constant)


def _pretty(value):
    """Independent stdlib formatting plus the frozen scalar escape refinements.

    Match complete JSON escapes so a literal backslash followed by n is never
    mistaken for a newline escape. This helper never calls product encoders.
    """
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2,
                     separators=(',', ': '), allow_nan=False)
    short = {'\\b': '\\u0008', '\\f': '\\u000c', '\\n': '\\u000a',
             '\\r': '\\u000d', '\\t': '\\u0009'}
    def replacement(match):
        token = match.group()
        if token.startswith('\\'):
            return short.get(token, token)
        return '\\u' + format(ord(token), '04x')
    return re.sub(r'\\.|[\u007f-\u009f\u061c\u200e\u200f\u2028-\u202e\u2066-\u2069]',
                  replacement, raw)


def _decimal_display(numerator, denominator):
    """Independent high-precision decimal oracle, not product integer code."""
    with localcontext() as context:
        context.prec = 80
        value = (Decimal(numerator) / Decimal(denominator)).quantize(
            Decimal('0.000001'), rounding=ROUND_HALF_UP)
        return format(value, '.6f')


def _parse_markdown(raw, expected):
    """Independently consume every fixed section, block and explanatory line."""
    assert type(raw) is bytes
    text = raw.decode('utf-8')
    assert not text.startswith('\ufeff')
    assert text.endswith('\n') and not text.endswith('\n\n') and '\r' not in text
    prefix = ('# Source Integrity Audit\n\nReport kind: ' + expected['report_kind'] +
              '\nProcessing state: ' + expected['run']['processing_state'] +
              '\nInput state: ' + expected['input_validation']['state'] + '\n\n')
    assert text.startswith(prefix), 'fixed report header'
    position = len(prefix)

    def literal(value):
        nonlocal position
        assert text.startswith(value, position), 'fixed layout at ' + str(position)
        position += len(value)

    def block():
        nonlocal position
        end = text.find('\n', position)
        assert end >= 0
        opening = text[position:end]
        assert re.fullmatch(r'`{3,}json', opening), 'JSON fence'
        fence = opening[:-4]
        position = end + 1
        end = text.find('\n' + fence + '\n', position)
        assert end >= 0, 'closed fence'
        body = text[position:end]
        longest = max((len(m.group()) for m in re.finditer(r'`+', body)), default=0)
        assert len(fence) == max(3, longest + 1), 'minimal safe fence'
        value = _decode(body)
        assert body == _pretty(value), 'exact pretty J formatting/scalars'
        position = end + len(fence) + 2
        return value

    document = {}
    reasons = {row['id']: row for row in expected['reasons']}
    for index, name in enumerate(ROOT_ORDER):
        literal('## ' + name + '\n\n')
        if name != 'results' or not expected['results']:
            document[name] = block()
            if index != len(ROOT_ORDER) - 1:
                literal('\n')
            continue
        rows = []
        for row in expected['results']:
            literal('### ' + row['id'] + ': ' + row['field_key'] + '\n\n')
            actual = block()
            rows.append(actual)
            literal('\n')
            if row['result_state'] == 'available' and row['value_kind'] == 'fraction':
                fraction = row['value']
                n, d = fraction['numerator'], fraction['denominator']
                literal('Decimal display: ' + str(n) + '/' + str(d) + ' = ' +
                        _decimal_display(n, d) + '\n\n')
            literal('Reason details\n\n')
            assert all(identifier in reasons for identifier in row['reason_refs'])
            _strict_equal(block(), [reason for reason in expected['reasons']
                                   if reason['id'] in row['reason_refs']])
            literal('\n')
        document[name] = rows
    assert position == len(text), 'trailing or omitted Markdown content'
    _strict_equal(document, expected)
    return document


def _assert_parity(json_raw, markdown_raw, expected):
    assert type(json_raw) is bytes and json_raw.endswith(b'\n')
    json_document = _decode(json_raw)
    markdown_document = _parse_markdown(markdown_raw, expected)
    _strict_equal(json_document, expected)
    _strict_equal(markdown_document, json_document)


def _reference_document():
    return json.loads((ROOT / 'tests/golden/phase4_report_expectations.json').read_bytes())['reference_document']


def _reference_json():
    return (ROOT / 'tests/golden/phase4_reference_report.json').read_bytes()


def _reference_markdown():
    return (ROOT / 'tests/golden/phase4_reference_report.md').read_bytes()


@pytest.fixture(scope='module')
def actual_reference():
    fixture = json.loads((ROOT / 'tests/fixtures/micro/phase4_public_cases.json').read_bytes())
    assert fixture['cases'][0]['id'] == 'P4-REFERENCE-ONE-ORIGIN'
    dossier = fixture['cases'][0]['dossier']
    original = copy.deepcopy(dossier)
    outcome = _analyze_value(dossier)
    assert type(outcome) is contract._AnalyticalOutcome
    assert outcome.execution_state == 'completed' and len(outcome.results) == 78
    selection_port = ComponentPort()
    frozen = _assemble_selected_report(outcome, selection_port)
    expected = _reference_document()
    _strict_equal(_plain(frozen), expected)
    # W06 exercises the renderer component on the actual selected document.
    # W07 owns the future single-invocation composition with earlier analysis.
    rendering_port = ComponentPort()
    json_raw = _encode_json_report(frozen, rendering_port)
    markdown_raw = _encode_markdown_report(frozen, rendering_port)
    assert dossier == original
    assert rendering_port.output == {'json': len(json_raw), 'markdown': len(markdown_raw)}
    assert 0 < rendering_port.units <= 10_000_000
    return frozen, expected, json_raw, markdown_raw, rendering_port.units


def test_real_selected_document_matches_both_independent_exact_byte_references(actual_reference):
    _, expected, json_raw, markdown_raw, _ = actual_reference
    assert json_raw == _reference_json()
    assert markdown_raw == _reference_markdown()
    assert len(json_raw) == 421307 and len(markdown_raw) == 564555
    _assert_parity(json_raw, markdown_raw, expected)


def test_all_root_members_complete_results_reasons_and_native_qualifications_survive(actual_reference):
    frozen, expected, json_raw, markdown_raw, units = actual_reference
    parsed = _parse_markdown(markdown_raw, expected)
    assert tuple(parsed) == ROOT_ORDER and len(parsed['results']) == 78
    assert len(parsed['checks']) == 671 and len(parsed['reasons']) == 38
    assert len(parsed['findings']) == 22 and len(parsed['observability_domains']) == 5
    assert {row['result_state'] for row in parsed['results']} == {
        'available', 'unavailable', 'not_applicable'}
    available_fraction = [row for row in expected['results']
                          if row['result_state'] == 'available' and row['value_kind'] == 'fraction']
    assert markdown_raw.count(b'Decimal display: ') == len(available_fraction)
    assert markdown_raw.count(b'\nReason details\n') == len(expected['results'])
    assert parsed['run']['started_at']['state'] == 'unknown'
    assert parsed['run']['started_at']['reason'] == 'not_recorded_by_SIT-RP-0.1'
    _strict_equal(_plain(frozen), expected)
    assert units < 10_000_000


def _diagnostic_document(kind, state, input_state):
    # Reuse the existing independently authored valid representation fixture.
    spec = importlib.util.spec_from_file_location('_w06_contract_fixture',
        ROOT / 'tests/contract/test_report_contract.py')
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.diagnostic_document(kind, state, input_state)


@pytest.mark.parametrize(('kind', 'state', 'input_state'), (
    ('validation_diagnostics', 'rejected', 'rejected'),
    ('processing_diagnostics', 'interrupted', 'not_completed'),
    ('processing_diagnostics', 'failed', 'accepted'),
    ('processing_diagnostics', 'failed', 'not_completed'),
))
def test_diagnostic_envelopes_keep_empty_results_safe_diagnostics_and_actual_input_state(kind, state, input_state):
    expected = _diagnostic_document(kind, state, input_state)
    frozen = contract._freeze_report_document(expected, ComponentPort())
    port = ComponentPort()
    json_raw = _encode_json_report(frozen, port)
    raw = _encode_markdown_report(frozen, port)
    _assert_parity(json_raw, raw, expected)
    assert b'## results\n\n```json\n[]\n```\n\n' in raw
    assert b'### SIT-RES-' not in raw and b'Decimal display:' not in raw
    assert b'\nReason details\n' not in raw
    assert port.output == {'json': len(json_raw), 'markdown': len(raw)}


def _render_component(expected):
    frozen = _freeze_component(expected)
    port = ComponentPort()
    json_raw = _encode_json_report(frozen, port)
    markdown_raw = _encode_markdown_report(frozen, port)
    _assert_parity(json_raw, markdown_raw, expected)
    return json_raw, markdown_raw


@pytest.mark.parametrize(('numerator', 'denominator', 'decimal'), (
    (0, 36, '0.000000'), (26, 36, '0.722222'), (1, 128, '0.007813'),
    (1, 2000000, '0.000001'), (1999999, 2000000, '1.000000'),
    (9007199254740990, 9007199254740991, '1.000000'),
))
def test_fraction_display_uses_half_up_six_places_and_keeps_original_components(numerator, denominator, decimal):
    expected = _reference_document()
    row = next(x for x in expected['results'] if x['field_key'] == 'documentary_origin_resolution_fraction')
    row['value'] = {'numerator': numerator, 'denominator': denominator}
    # The changed value is a trusted representation component, not a new
    # analytical result for the reference dossier or a replacement golden.
    json_raw, raw = _render_component(expected)
    line = 'Decimal display: ' + str(numerator) + '/' + str(denominator) + ' = ' + decimal + '\n'
    assert line.encode() in raw
    decoded = _decode(json_raw)
    actual = next(x for x in decoded['results'] if x['id'] == row['id'])
    assert actual['value'] == {'numerator': numerator, 'denominator': denominator}
    assert 'display_decimal' not in actual


@pytest.mark.parametrize(('execution_state', 'result_state'), (
    ('completed', 'unavailable'), ('not_performed', 'not_evaluated'),
    ('interrupted', 'not_evaluated'), ('failed', 'not_evaluated'),
))
def test_nonresults_keep_null_value_reasons_and_never_gain_a_decimal(execution_state, result_state):
    expected = _reference_document()
    row = next(x for x in expected['results'] if x['field_key'] == 'documentary_origin_resolution_fraction')
    row.update(execution_state=execution_state, result_state=result_state,
               value=None, reason_refs=[expected['reasons'][0]['id']])
    _, raw = _render_component(expected)
    section = raw.split(('### ' + row['id'] + ': ' + row['field_key'] + '\n').encode(), 1)[1]
    section = section.split(b'\n### ', 1)[0]
    assert b'Decimal display:' not in section
    assert b'"value": null' in section
    assert expected['reasons'][0]['detail'].encode() in section


def test_available_completion_interval_retains_exact_endpoints_without_extra_decimal_line():
    expected = _reference_document()
    row = next(x for x in expected['results'] if x['field_key'] == 'inherited_only_completion_interval')
    labels = ('direct_origin_link_only', 'inherited_only_at_evidence_layer',
              'mixed_direct_and_inherited', 'unresolved_at_evidence_layer')
    member = lambda identifier: {'collection': 'records', 'identifier': identifier, 'selector': None}
    interval = {'lower': {'numerator': 1, 'denominator': 3},
                'upper': {'numerator': 2, 'denominator': 3},
                'interval_kind': 'finite_record_completion',
                'population_ref': row['population_refs'][0],
                'partition': {'population_ref': row['population_refs'][0],
                    'categories': [
                        {'label': label, 'count': int(index != 2),
                         'member_refs': [member('P4-REP-' + str(index))] if index != 2 else []}
                        for index, label in enumerate(labels)], 'total': 3}}
    contract._validate_report_component(interval, 'CompletionInterval', ComponentPort())
    row.update(result_state='available', value=interval, reason_refs=[])
    _, raw = _render_component(expected)
    section = raw.split(('### ' + row['id'] + ': ' + row['field_key'] + '\n').encode(), 1)[1]
    section = section.split(b'\n### ', 1)[0]
    assert b'Decimal display:' not in section and b'"denominator": 3' in section


def test_reason_details_follow_canonical_reason_order_without_reordering_result_refs():
    expected = _reference_document()
    row = next(x for x in expected['results'] if len(x['reason_refs']) >= 2)
    original = list(row['reason_refs'])
    row['reason_refs'].reverse()
    assert row['reason_refs'] != original
    json_raw, raw = _render_component(expected)
    parsed_json = _decode(json_raw)
    actual = next(x for x in parsed_json['results'] if x['id'] == row['id'])
    assert actual['reason_refs'] == row['reason_refs']
    # _parse_markdown independently selects the linked Reasons in root order,
    # while the complete Result body retains its supplied reference array.
    _parse_markdown(raw, expected)


def _replace_block_after(raw, marker, value):
    """Create one deliberate omission mutant from independently expected bytes."""
    text = raw.decode()
    start = text.index(marker) + len(marker)
    end = text.index('\n', start)
    opening = text[start:end]
    assert re.fullmatch(r'`{3,}json', opening)
    fence = opening[:-4]
    close = text.index('\n' + fence + '\n', end + 1)
    body = _pretty(value)
    longest = max((len(m.group()) for m in re.finditer(r'`+', body)), default=0)
    new_fence = '`' * max(3, longest + 1)
    replacement = new_fence + 'json\n' + body + '\n' + new_fence
    return (text[:start] + replacement + text[close + 1 + len(fence):]).encode()


@pytest.mark.parametrize('omission', ('unknown_time', 'root_reason', 'reason_detail',
                                   'denominator', 'qualification'))
def test_independent_parser_rejects_each_substantive_omission(omission):
    expected = _reference_document()
    raw = _reference_markdown()
    if omission == 'unknown_time':
        value = copy.deepcopy(expected['run']); del value['started_at']['reason']
        mutant = _replace_block_after(raw, '## run\n\n', value)
    elif omission == 'root_reason':
        mutant = _replace_block_after(raw, '## reasons\n\n', expected['reasons'][1:])
    elif omission == 'reason_detail':
        row = next(x for x in expected['results'] if x['reason_refs'])
        marker = '### ' + row['id'] + ': ' + row['field_key'] + '\n\n'
        start = raw.index(marker.encode())
        reason_start = raw.index(b'Reason details\n\n', start)
        mutant = raw[:reason_start] + _replace_block_after(raw[reason_start:], 'Reason details\n\n', [])
    elif omission == 'denominator':
        row = copy.deepcopy(next(x for x in expected['results']
            if x['result_state'] == 'available' and x['value_kind'] == 'fraction'))
        del row['value']['denominator']
        mutant = _replace_block_after(raw, '### ' + row['id'] + ': ' + row['field_key'] + '\n\n', row)
    else:
        value = copy.deepcopy(expected['input_identity']); value['qualifications'] = []
        mutant = _replace_block_after(raw, '## input_identity\n\n', value)
    assert mutant != raw
    with pytest.raises(AssertionError):
        _assert_parity(_reference_json(), mutant, expected)


def test_counterevidence_is_retained_and_independent_parser_rejects_its_omission():
    expected = _reference_document()
    counter = {'collection': 'assertions', 'identifier': 'P4-REL', 'selector': None}
    expected['findings'][0]['contrary_input_refs'] = [counter]
    # Selected representation component only; no claim that the original
    # analytical fixture classified this specific source as counterevidence.
    json_raw, raw = _render_component(expected)
    value = copy.deepcopy(expected['findings'])
    value[0]['contrary_input_refs'] = []
    mutant = _replace_block_after(raw, '## findings\n\n', value)
    with pytest.raises(AssertionError):
        _assert_parity(json_raw, mutant, expected)


@pytest.mark.parametrize('change', ('indent', 'double_final_lf', 'missing_root',
                                  'decimal_rounding', 'decimal_replaces_fraction', 'extra_text'))
def test_exact_layout_oracle_rejects_framing_and_presentation_mutants(change):
    expected = _reference_document(); raw = _reference_markdown()
    if change == 'indent':
        mutant = raw.replace(b'  "completed_diagnostic_ids"', b' "completed_diagnostic_ids"', 1)
    elif change == 'double_final_lf':
        mutant = raw + b'\n'
    elif change == 'missing_root':
        mutant = raw.replace(b'## release_limits\n\n', b'', 1)
    elif change == 'decimal_rounding':
        mutant = raw.replace(b'Decimal display: 1/1 = 1.000000', b'Decimal display: 1/1 = 0.999999', 1)
    elif change == 'decimal_replaces_fraction':
        row = copy.deepcopy(next(x for x in expected['results']
            if x['result_state'] == 'available' and x['value_kind'] == 'fraction'))
        row['value'] = 1
        mutant = _replace_block_after(raw, '### ' + row['id'] + ': ' + row['field_key'] + '\n\n', row)
    else:
        mutant = raw + b'Unrequested footer\n'
    assert mutant != raw
    with pytest.raises(AssertionError):
        _parse_markdown(mutant, expected)
