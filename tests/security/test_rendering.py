# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W06 literal-data rendering controls over approved frozen report values.

These are renderer component tests. Contract-valid canary documents are frozen
before rendering; no public audit or automatic disclosure/publication safety
claim is made. The parser is test-owned and independent of product formatting.
"""
import copy
import importlib.util
import json
from pathlib import Path
import re

import pytest

from source_integrity_toolkit.contracts import report as contract
from source_integrity_toolkit.reporting.json_report import _encode_json_report
from source_integrity_toolkit.reporting.markdown_report import _encode_markdown_report


ROOT = Path(__file__).resolve().parents[2]
_spec = importlib.util.spec_from_file_location(
    'p4_w06_rendering_parity_helpers', ROOT / 'tests/contract/test_report_parity.py')
h = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(h)


def _reference():
    return json.loads((ROOT / 'tests/golden/phase4_reference_report.json').read_bytes())


def _diagnostic(payload):
    """Small valid execution envelope with literal retained text canaries."""
    document = _reference()
    document['report_kind'] = 'processing_diagnostics'
    document['run']['processing_state'] = 'failed'
    document['run']['completed_diagnostic_ids'] = []
    document['run']['diagnostics'] = [{
        'code': 'execution_failed', 'location': None,
        'safe_message': 'Processing did not complete.',
        'qualifications': ['Synthetic retained qualification: ' + payload],
    }]
    document['input_identity']['qualifications'].append(payload)
    for name in ('scopes', 'populations', 'basis_index', 'capabilities', 'checks',
                 'observability_domains', 'results', 'findings'):
        document[name] = []
    document['reasons'] = [{
        'id': 'SIT-RSN-000001', 'classification': 'execution',
        'code': 'execution_failed', 'scope_ref': None,
        'affected_result_refs': [], 'input_refs': [], 'detail': payload,
    }]
    return document


def _strings(value):
    if type(value) is str:
        yield value
    elif type(value) is dict:
        for child in value.values():
            yield from _strings(child)
    elif type(value) is list:
        for child in value:
            yield from _strings(child)


def _outside_and_blocks(raw):
    """Identify literal fenced data independently, without Markdown execution."""
    text = raw.decode('utf-8')
    lines = text.splitlines(keepends=True)
    outside, blocks = [], []
    position = 0
    while position < len(lines):
        opening = re.fullmatch(r'(`{3,})json\n', lines[position])
        if opening is None:
            outside.append(lines[position])
            position += 1
            continue
        fence = opening[1]
        position += 1
        body_lines = []
        while position < len(lines) and lines[position] != fence + '\n':
            body_lines.append(lines[position])
            position += 1
        assert position < len(lines), 'unclosed data fence'
        body = ''.join(body_lines)
        assert body.endswith('\n')
        longest = max((len(run) for run in re.findall(r'`+', body)), default=0)
        assert len(fence) == max(3, longest + 1), 'minimal safe fence'
        blocks.append((len(fence), body, json.loads(body)))
        position += 1
    assert blocks
    return ''.join(outside), blocks


def _render_valid(document):
    original = copy.deepcopy(document)
    frozen = contract._freeze_report_document(document, h.ComponentPort())
    port = h.ComponentPort()
    markdown = _encode_markdown_report(frozen, port)
    assert type(markdown) is bytes
    assert h._parse_markdown(markdown, original) == original
    assert document == original
    outside, blocks = _outside_and_blocks(markdown)
    return frozen, markdown, outside, blocks


@pytest.mark.parametrize(('name', 'payload'), (
    ('html', 'CANARY_HTML <script>alert("literal")</script><b>bold</b>'),
    ('image', 'CANARY_IMAGE ![literal](https://example.invalid/pixel.png) <img src="https://example.invalid/pixel.png">'),
    ('autolink', 'CANARY_LINK <https://example.invalid/path> <mailto:render@example.invalid>'),
    ('local_link', 'CANARY_FILE [literal](file:///private/canary.txt) [js](javascript:alert(1))'),
    ('headings', 'CANARY_HEADING\n# Not a heading\n## Not a root\n### Not a Result'),
    ('table', 'CANARY_TABLE\n| source | value |\n|---|---|\n> blockquote\n- list'),
    ('comment', 'CANARY_COMMENT <!-- literal source comment -->'),
    ('fence', 'CANARY_FENCE\n```\n![escaped](https://example.invalid/image)\n```json\n'),
))
def test_markup_canaries_stay_in_encoded_blocks_and_retain_exact_values(name, payload):
    document = _diagnostic(payload)
    frozen, markdown, outside, blocks = _render_valid(document)
    assert payload in tuple(_strings(h._parse_markdown(markdown, document)))
    assert any(payload in tuple(_strings(value)) for _, _, value in blocks)
    assert payload.split('\n', 1)[0] not in outside
    for marker in ('CANARY_', '<script', '<img', 'https://', 'file://', 'javascript:',
                   '<!--', 'mailto:', '![', '| source |', '# Not a heading'):
        assert marker not in outside
    # The JSON sibling independently preserves the same selected logical data.
    json_raw = _encode_json_report(frozen, h.ComponentPort())
    assert json.loads(json_raw) == document


@pytest.mark.parametrize('run', (0, 1, 2, 3, 4, 7, 31, 64, 65, 129))
def test_fence_is_one_longer_than_longest_literal_backtick_run(run):
    payload = 'FENCE_RUN_BEGIN' + '`' * run + 'FENCE_RUN_END'
    _, _, outside, blocks = _render_valid(_diagnostic(payload))
    containing = [(width, body, value) for width, body, value in blocks
                  if any(payload in text for text in _strings(value))]
    assert len(containing) == 3
    assert all(width == max(3, run + 1) for width, _, _ in containing)
    assert 'FENCE_RUN_BEGIN' not in outside
    assert any(width == 3 for width, _, value in blocks
               if not any(payload in text for text in _strings(value)))


def test_control_and_bidi_scalars_are_exposed_as_exact_lowercase_json_escapes():
    controls = (*range(0x00, 0x20), *range(0x7F, 0xA0), 0x061C, 0x200E, 0x200F,
                *range(0x2028, 0x202F), *range(0x2066, 0x206A))
    payload = 'CONTROL_BEGIN' + ''.join(chr(code) for code in controls) + 'CONTROL_END'
    _, markdown, outside, blocks = _render_valid(_diagnostic(payload))
    assert 'CONTROL_BEGIN' not in outside
    raw_text = markdown.decode('utf-8')
    for code in controls:
        assert '\\u' + format(code, '04x') in raw_text
        if code != 10:  # Tool-owned structural LF remains literal.
            assert chr(code) not in raw_text
    assert any(payload in tuple(_strings(value)) for _, _, value in blocks)


def test_multilingual_combining_forms_and_terminal_sequences_are_not_dropped():
    payload = ('TEXT_BEGIN 中文 العربية Ελληνικά 日本語 😀 é e\u0301 '
               '\x1b[31mRED\x1b[0m\u202eRTL\u202c TEXT_END')
    _, markdown, outside, blocks = _render_valid(_diagnostic(payload))
    assert 'TEXT_BEGIN' not in outside
    assert any(payload in tuple(_strings(value)) for _, _, value in blocks)
    assert '中文 العربية Ελληνικά 日本語 😀 é e\u0301'.encode() in markdown
    assert b'\\u001b[31mRED\\u001b[0m\\u202eRTL\\u202c' in markdown


def test_result_and_repeated_reason_details_keep_source_text_inside_safe_blocks():
    document = _reference()
    payload = 'RESULT_CANARY\n```````\n<img src="https://example.invalid/r">\u202e'
    reason = document['reasons'][0]
    reason['detail'] = payload
    result = next(row for row in document['results'] if reason['id'] in row['reason_refs'])
    result['interpretation_limit'] = payload
    frozen, markdown, outside, blocks = _render_valid(document)
    matching = [(width, value) for width, _, value in blocks
                if payload in tuple(_strings(value))]
    assert len(matching) >= 3  # Result, its linked Reason details and root Reasons.
    assert all(width == 8 for width, _ in matching)
    assert 'RESULT_CANARY' not in outside and '<img' not in outside
    assert '### ' + result['id'] + ': ' + result['field_key'] + '\n' in outside
    assert json.loads(_encode_json_report(frozen, h.ComponentPort())) == document


@pytest.mark.parametrize('target', ('report_kind', 'processing_state', 'input_state',
                                   'result_id', 'field_key'))
def test_invalid_component_header_text_cannot_become_markdown_structure(target):
    # Deliberately bypass the contract only for a private malformed-value control.
    # The permitted header vocabulary must still reject this before returning bytes.
    document = _reference()
    payload = 'UNTRUSTED_HEADER\n# injected\n<img src="https://example.invalid/h">'
    if target == 'report_kind':
        document['report_kind'] = payload
    elif target == 'processing_state':
        document['run']['processing_state'] = payload
    elif target == 'input_state':
        document['input_validation']['state'] = payload
    elif target == 'result_id':
        document['results'][0]['id'] = payload
    else:
        document['results'][0]['field_key'] = payload
    returned = []
    with pytest.raises(contract._ReportContractError, match='^invalid_report_contract$'):
        returned.append(_encode_markdown_report(h._freeze_component(document), h.ComponentPort()))
    assert returned == []
