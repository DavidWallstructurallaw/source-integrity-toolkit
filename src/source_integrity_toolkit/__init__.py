# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Source Integrity Toolkit: development in-memory auditing and reports.

audit_bundle delivers an immutable report with completed JSON and Markdown
encodings. File auditing and CLI audit execution remain unavailable.
Importing this package does not start an audit.
"""

from .api import audit_bundle, audit_file
from .contracts.constants import SCAFFOLD_VERSION as __version__
from .contracts.execution import AuditAbort, AuditCancelled, AuditUsageError
from .contracts.report import AuditReport

__all__ = ("audit_bundle", "audit_file", "__version__", "AuditReport", "AuditAbort", "AuditCancelled", "AuditUsageError")
