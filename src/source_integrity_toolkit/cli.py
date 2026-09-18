# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Non-operational CLI; PHASE_1_PLAN.md section 4.1.

Owner: RUNTIME_BOUNDARY, public composition surface.
This dispatcher displays scaffold help/version or refuses with exit 1.
It does not implement the future audit argument grammar or report outcomes.
"""

import sys

from .contracts.constants import SCAFFOLD_VERSION

_HELP = """Source Integrity Toolkit: Phase 1 scaffold

Usage:
  sit --help
  sit --version
  sit audit INPUT --output OUTPUT_DIR [--raw-file-digest]

Audit functionality is not implemented. Audit requests exit 1 without reading
input, inspecting paths, or producing a report. This temporary refusal is not
a sit-report/0.1 processing result. The audit grammar is reserved for later work.
"""
_REFUSAL = "Source Integrity Toolkit audit is not implemented in the Phase 1 scaffold."


def main(argv: list[str] | None = None) -> int:
    """Display fixed help/version text or refuse without echoing arguments."""
    args = sys.argv[1:] if argv is None else argv
    if args in ([], ["--help"], ["-h"], ["audit", "--help"], ["audit", "-h"]):
        print(_HELP, end="")
        return 0
    if args == ["--version"]:
        print(f"source-integrity-toolkit {SCAFFOLD_VERSION}")
        return 0
    print(_REFUSAL, file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
