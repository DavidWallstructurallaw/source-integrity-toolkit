# PHASE_1_PROGRESS

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Progress revision | 0.1 |
| Date | 2026-09-17 |
| Approved Phase 1 plan | Revision 0.1 at `2fa58fce603e28f1160bd68eeadbe315db941501` |
| Plan Git blob | `27ed33cb1c2afc78b12ca099ee7ccb4e68d63bfb` |
| Plan approval and execution instruction | `批准，开始 P1-W01` |
| Current work unit | P1-W01: Freeze verification, project governance and license application |
| Execution intake commit | `2fa58fce603e28f1160bd68eeadbe315db941501` |
| Approved Phase 0 candidate | `7d2e5fcaff591641b5cefce00e71e88941dd1f95` |
| Original approval-record commit | `6650984502637bb167c38e7e370c46e246591480` |
| Review branch | `phase1/p1-w01` |
| Current result | BLOCKED_AT_ENTRY: four malformed SHA-256 entries in the frozen approval record |
| P1-W01 completion | Not claimed |
| P1-W02 and later units | Not started |

## 1. Authorization and scope

The owner's instruction approves the exact Phase 1 plan identified above and authorizes P1-W01 only. The plan remains byte-identical; its historical PROPOSED header is read with this later approval event. No separate approval of an unwritten later step is inferred.

PHASE_1_PLAN.md section 5 requires an exact-byte approval-manifest check before license and governance application. Section 3 freezes the eighteen Phase 0 files, PHASE_0_APPROVAL.md and the approved plan. Section 13 requires recording a failed gate here and obtaining scoped authorization before changing a frozen record.

The current permitted write is this progress record. No other P1-W01 artifact is represented as completed, and no approval file or specification has been changed.

## 2. Entry verification performed

The connected repository's main branch was read at the intake commit. Its complete tree contains the eighteen original Phase 0 paths plus PHASE_0_APPROVAL.md and PHASE_1_PLAN.md. The eighteen original Git blob identities and byte counts agree with the tree at the approved candidate commit. This establishes snapshot continuity at the Git-object level; it does not validate a malformed printed SHA-256 value.

PHASE_0_APPROVAL.md was fetched in full. The byte-preserving local copy was checked against its remote blob before inspection:

| Property | Verified value |
|---|---|
| Bytes | 11830 |
| Git blob SHA-1 | `5f9732b2ab1cf51c513e2bcf71a0cdb8a4f055d3` |
| Independently computed file SHA-256 | `73c10235549ffc725f9035f07281818f560a9262361acca2ba81c3d7a01e7ccd` |
| Manifest rows | 18 |
| Sum of listed baseline bytes | 1094920 |
| Rows containing exactly 64 lowercase hexadecimal characters | 14 |
| Rows containing only 63 hexadecimal characters | 4 |

Eleven locally available original baseline files were independently hashed after their complete bytes were matched to the current remote Git blobs. Those eleven SHA-256 values and lengths match the approval table: CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md, DEFINITIONS_AND_UNITS.md, OBSERVABILITY_AND_REPORTING.md, PHASE_0_PLAN.md, PROJECT_INSTRUCTIONS.md, SPEC_AUDIT.md, SUCCESS_CRITERIA.md, THEORY_SOURCE_MAP.md, THEORY_TO_CODE_TRACEABILITY.md, V0.1_PRODUCT_SPEC.md and VALIDATION_PLAN.md.

The other seven baseline SHA-256 values have not been independently rehashed in this unit. Four of those seven fail even the digest-format check. Correct length in the other three is not evidence that their values are correct. No claim of eighteen successfully recomputed digests is made.

## 3. P1-W01-B01: malformed approval-manifest digests

**Status:** BLOCKING at the P1-W01 freeze-verification gate.

**Affected file:** PHASE_0_APPROVAL.md, section 2, at the exact approval blob above.

| Baseline path named in the approval | Printed SHA-256 value | Hex characters |
|---|---|---:|
| PRIVACY_AND_DATA_HANDLING.md | `a364119c0a9cde098cf3f2f84d3c053e67c9871d492ba62a0ca7d1d9e695610` | 63 |
| REPOSITORY_ARCHITECTURE.md | `4bde46a39961bff9e99f7e5f82b6e57c7a911f437a79c1436d37cdcfa9ff1f3` | 63 |
| SOURCE_INTEGRITY_THREAT_MODEL.md | `bdb82719e05a7c7a41b0f9bdce409b37f31f7a08d6327f710ba5da0d6044f13` | 63 |
| UNRESOLVED_DECISIONS.md | `e562031d15d14ea74724b520db9cbe6a5b62b85105c611fb1430c9a6cddf4a0` | 63 |

A complete SHA-256 hexadecimal encoding needs 64 characters: 256 bits divided by four bits per hexadecimal digit. The four values cannot be accepted as complete encodings. Do not guess a missing character, prepend a zero, copy a Git SHA-1 into a SHA-256 field, or weaken the manifest checker.

This observation does not show that the four underlying specification files were altered. Their current Git objects match the approved snapshot. It identifies a defective approval-manifest representation. The preceding delivery's claim that the complete approval manifest had been checked was too strong; that omission is corrected by this entry.

The owner's semantic adoption of the named Phase 0 commit is preserved. Execution remains blocked because the required machine-checkable freeze evidence must be corrected under the frozen-record amendment procedure.

## 4. Narrow proposed repair

The following repair requires explicit owner authorization because PHASE_0_APPROVAL.md is outside P1-W01's writable allowlist:

1. Read the complete eighteen file byte sequences at the existing approved commit, match their lengths and Git blob identities, and compute every SHA-256 without checkout or text normalization.
2. Revise only PHASE_0_APPROVAL.md's erroneous manifest values and necessary revision/correction-history metadata. Preserve the existing approved candidate commit, approval event, design decisions and scope. Keep revision 1.0 available at its immutable original commit.
3. Recheck every manifest row, its exact value and length, and the aggregate file count/byte total. Compute the revised approval record's own separate hash after its bytes are fixed.
4. Record the correction commit and evidence in this progress file, then resume the already authorized P1-W01 allowlist. Create scaffold/baseline_manifest.json only from the corrected verified record.

No change to any of the eighteen baseline specifications or to PHASE_1_PLAN.md is proposed. Any newly observed difference in those source bytes would be a separate stop, not permission to update their content. The repair must not be described as a new theory decision, a full product audit, or authorization to execute P1-W02.

## 5. Other intake observations and incomplete work

Public-source checks were started for the already approved license and build/test tool classes. They are preliminary inputs only. Setuptools 84.0.0 and pytest 9.1.1 were observed as candidate build/test versions with declared Python >=3.10 and MIT project licensing. Their versioned project metadata was read; no package installation, resolver run, complete vendored-license review or compatibility test occurred. Final pins and dependency implications still belong in the pending scaffold/toolchain_review.md.

The official Apache-2.0 plain-text license was viewed, but no root LICENSE or NOTICE has been committed. This record adds no license grant or altered licensing policy.

Repository metadata confirms a public repository with Issues available. The attempted private-vulnerability-reporting status endpoint was rejected by the connector's permitted-route boundary. Private reporting therefore remains unverified; no email address or private reporting capability is invented. The later SECURITY.md must disclose the actual verified route and prohibit posting secrets.

The local shell could not resolve github.com for a public clone, and direct binary/text download attempts did not furnish a complete local repository. Connected GitHub reads remained available. No local clone is presented as successful. This transport limitation is separate from the verified malformed-digest defect, and no credential or security bypass was attempted.

## 6. Check evidence and boundary

Local authoring checks used CPython 3.13.5 on Linux and Git 2.47.3. They checked UTF-8 bytes, standard Git blob hashing, SHA-256, exact digest lengths, manifest row counts and arithmetic. These environment versions describe the checking workspace only; they establish no supported toolkit runtime or tested platform.

The initial strict 64-hex row parser found only fourteen admissible digest rows and failed its expected eighteen-row assertion. A second inspection that retained malformed rows confirmed eighteen rows in total and exactly the four 63-character entries listed above. The first failure is preserved as a failed gate; it was not converted into a pass by accepting shorter hashes.

No runtime parser, schema, API, CLI, native binding, dependency manifest, fixture, test suite, workflow or implementation is created. No product tests, package builds or hosted CI runs are claimed. Existing specifications, the approval record and plan stay unchanged.

The review branch receives this one progress file and a draft pull request describing the hold. Its actual commit and PR are supplied by GitHub after creation and in the handoff, without inserting a self-referential commit ID here. It must not be merged or described as a completed P1-W01 delivery while the recorded gate is unresolved.

## 7. Current stop

P1-W01 has started and is blocked at entry verification. The next owner decision is the scoped approval-record repair in section 4, followed by continuation of P1-W01. Later work units remain unstarted. The approved Phase 1 plan and the substantive Phase 0 design remain in force.
