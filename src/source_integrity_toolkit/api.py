# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Public-operation reservations; PHASE_1_PLAN.md sections 4.1 and 6.

Owner: RUNTIME_BOUNDARY, public composition surface. Behavior unimplemented.
All arguments, including options, remain entirely untouched by these stubs.
"""

from typing import NoReturn


def audit_bundle(bundle: object, *, options: object = None) -> NoReturn:
    """Refuse immediately; never inspect or normalize a supplied dossier."""
    raise NotImplementedError(
        "Source Integrity Toolkit audit is not implemented in the Phase 1 scaffold."
    )


def audit_file(
    input_path: object, output_directory: object, *, options: object = None
) -> NoReturn:
    """Refuse immediately; never resolve, read or create a supplied path."""
    raise NotImplementedError(
        "Source Integrity Toolkit audit is not implemented in the Phase 1 scaffold."
    )
