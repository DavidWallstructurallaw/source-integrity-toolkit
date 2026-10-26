# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Public in-memory audit composition; PHASE_4_PLAN.md section 4.1.

Owner: RUNTIME_BOUNDARY. Trusted invocation options are checked before the
dossier reaches the existing bounded runtime. File auditing remains reserved.
"""

from typing import NoReturn

from .contracts.execution import AuditUsageError
from .contracts.report import AuditReport
from .runtime.boundary import _audit_value


def audit_bundle(bundle: object, *, options: object = None) -> AuditReport:
    """Audit an in-memory dossier and return its complete immutable report.

    Options are limited to an exact dict containing raw_file_digest=False.
    None and an empty dict select the same fixed in-process behavior. Invalid
    options fail before input access and cannot supply a budget or callback.
    """
    if options is not None:
        if type(options) is not dict or len(options) > 1:
            raise AuditUsageError() from None
        # Native iteration over at most one pair avoids dictionary lookup:
        # an untrusted key must never participate in a hash or equality call.
        for key, value in options.items():
            if (type(key) is not str or key != "raw_file_digest" or
                    type(value) is not bool or value):
                raise AuditUsageError() from None
    return _audit_value(bundle)


def audit_file(
    input_path: object, output_directory: object, *, options: object = None
) -> NoReturn:
    """Refuse immediately; never resolve, read or create a supplied path."""
    raise NotImplementedError(
        "Source Integrity Toolkit audit is not implemented in the Phase 1 scaffold."
    )
