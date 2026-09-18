# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Source Integrity Toolkit: unreleased, non-operational Phase 1 scaffold.

Public names are reserved by PHASE_1_PLAN.md section 4.1.
Neither importing the package nor calling its audit stubs audits evidence.
"""

from .api import audit_bundle, audit_file
from .contracts.constants import SCAFFOLD_VERSION as __version__

__all__ = ("audit_bundle", "audit_file", "__version__")
