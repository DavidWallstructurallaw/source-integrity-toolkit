# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: REPORT_PRESENTATION. Exact JSON bytes for one frozen report.

The caller supplies the already validated, selected logical document and its
restricted same-context encoding port. No source projection, analytical work,
new budget, public AuditReport construction or filesystem access occurs here.
"""
from ..contracts.report import _ReportMapping, _ReportContractError
from .escaping import _JWriter, _CheckingWriter


def _encode_json_report(document, port):
    """Return J(document) and exactly one LF, both under the JSON byte cap.

    A partial encoding is never returned. This internal component alone is
    not public report delivery; the Markdown sibling and final consistency
    checks still belong to subsequent approved work units.
    """
    port.charge(1)
    if type(document) is not _ReportMapping:
        raise _ReportContractError('invalid_report_contract') from None
    writer = _JWriter(port, 'json')
    writer.value(document)
    writer.literal(b'\n')
    return writer.finish()


def _verify_json_report(document, encoded, port):
    """Check complete framing and scalar content against the frozen document."""
    port.charge(1)
    if type(document) is not _ReportMapping:
        raise _ReportContractError('invalid_report_contract') from None
    writer = _CheckingWriter(port, 'json', encoded)
    writer.value(document)
    writer.literal(b'\n')
    writer.finish()
