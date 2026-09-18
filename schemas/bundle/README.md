# sit-bundle/0.1 reservation

Copyright 2026 Xiangyu Guo. SPDX-License-Identifier: Apache-2.0.

Status: logical contract adopted; executable schema not delivered.

The input authority is [CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md](../../CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md),
particularly sections 2-9 and 13-14, read with
[DEFINITIONS_AND_UNITS.md](../../DEFINITIONS_AND_UNITS.md).
[REPOSITORY_ARCHITECTURE.md](../../REPOSITORY_ARCHITECTURE.md) sections 17-20,
[PRIVACY_AND_DATA_HANDLING.md](../../PRIVACY_AND_DATA_HANDLING.md), and
[GOVERNANCE_AND_HANDOFF.md](../../GOVERNANCE_AND_HANDOFF.md) section 22 retain
capture, exactness, security, interruption and final-precision authority.

This reservation implements no ingestion, normalization, schema mapping,
reference resolution, semantic qualification or observability classification.
The existing twelve record kinds, typed assertions and explicit unresolved
references remain as specified. This file neither adds optional fields nor
supplies defaults for unavailable evidence. Extensions remain inert.

The reserved `audit_bundle` and `audit_file` entry points still immediately
raise `NotImplementedError`. They do not consult this directory or the catalogs.
A later schema must be tested against the approved record contract and must not
present structural admission as source authentication or proof of independence.

This directory contains documentation only. No `.schema.json` is supplied.
