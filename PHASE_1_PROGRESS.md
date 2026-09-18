# PHASE_1_PROGRESS

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Phase / work unit | Phase 1 / P1-W01 |
| Revision | 0.1 |
| Record date | 2026-09-17 |
| Status | BLOCKED at freeze verification; work unit not complete |
| Owner instruction | `批准，开始P1-W01` |
| Plan approved by that instruction | PHASE_1_PLAN.md revision 0.1 at 2fa58fce603e28f1160bd68eeadbe315db941501 |
| Approved plan Git blob | 27ed33cb1c2afc78b12ca099ee7ccb4e68d63bfb |
| Intake main commit | 2fa58fce603e28f1160bd68eeadbe315db941501 |
| Approved Phase 0 content commit | 7d2e5fcaff591641b5cefce00e71e88941dd1f95 |
| Approval-record commit | 6650984502637bb167c38e7e370c46e246591480 |
| Review branch | phase1/p1-w01-governance |
| Theory Owner | Xiangyu Guo |
| Technical Owner | Unassigned |
| P1-W02 and later execution | Not authorized by this work item |

## 1. Authorization and exact stop

The owner's instruction approves the submitted Phase 1 plan and starts P1-W01 only. The plan and all eighteen Phase 0 files remain frozen. This progress record does not edit their historical approval headers.

PHASE_1_PLAN.md section 5 requires verification of all eighteen approval-manifest hashes before successful delivery. Its stop rule prohibits silently repairing a frozen file. Section 13 requires the observed discrepancy and a narrow proposed repair to be recorded here.

The entry check found five concrete defects in PHASE_0_APPROVAL.md section 2. One stored SHA-256 disagrees with the actual bytes of the corresponding approved Git blob. Four other stored digest strings have 63 hexadecimal characters instead of a complete 64-character SHA-256 encoding. The repository source files were not changed by this work item.

**Disposition: P1-W01 is blocked. No successful baseline manifest, license application, package scaffold or subsequent unit is claimed.**

## 2. Evidence identity and method

Read the connected repository's main ref and complete twenty-file tree at the intake commit. The eighteen specification blobs remain those of the approved Phase 0 snapshot. The other two files are PHASE_0_APPROVAL.md and PHASE_1_PLAN.md. The tree contains none of this unit's proposed new project files at intake.

Read the complete approval record and DEPENDENCY_STRATEGY.md through the GitHub connector at the pinned intake snapshot. Reconstruct their returned UTF-8 bytes locally and require the locally calculated Git blob identity and byte count to match the remote tree before using those bytes for SHA-256 calculation. Existing local WU1-WU8 delivery files were used only where the same byte-count and Git-blob checks matched the current remote files. Older local threat/register copies were not treated as current evidence.

The approval record itself was reproduced exactly:

| Property | Observed value |
|---|---|
| Path | PHASE_0_APPROVAL.md |
| Bytes | 11830 |
| Git blob SHA-1 | 5f9732b2ab1cf51c513e2bcf71a0cdb8a4f055d3 |
| Separately calculated SHA-256 | 73c10235549ffc725f9035f07281818f560a9262361acca2ba81c3d7a01e7ccd |

The approval table has eighteen paths and its listed byte counts sum to 1,094,920. Correct row count and total size do not validate incorrect digest fields.

The authoring workspace's direct network download route was unavailable. No download error was interpreted as an absent repository file. Connected GitHub reads and content-identity-matched local bytes supplied the checks reported below.

## 3. P1-W01-F01: incorrect SHA-256 for an unchanged approved file

| Property | Value |
|---|---|
| Affected manifest row | DEPENDENCY_STRATEGY.md |
| Approved and intake Git blob | 74849cc4b4ee3ab927e6de3a721ddc3edba10b15 |
| Actual and listed byte count | 15029 |
| SHA-256 written in PHASE_0_APPROVAL.md | 6f266470bcd812965debd889df8c533a68b2aa8374da1541676162f0a74ebc9f |
| SHA-256 calculated from the exact blob bytes | 65b5c4f1f91be019e1fb09329ff5214980e5956579c1c8ccec7f4b6f7b4174ad |
| Result | FAIL: approval-manifest digest mismatch |

Python hashlib.sha256, GNU sha256sum and openssl dgst -sha256 independently returned the observed SHA-256 above. Python's Git-blob calculation and git hash-object --no-filters both returned the same remote Git blob identity. The evidence locates this mismatch in the approval manifest; it does not show that the approved dependency specification was altered.

## 4. P1-W01-F02: four incomplete digest encodings

These are the exact strings read from PHASE_0_APPROVAL.md; no leading zero, missing character or replacement digest is guessed.

| Affected manifest row | Stored digest | Hexadecimal characters |
|---|---|---:|
| PRIVACY_AND_DATA_HANDLING.md | a364119c0a9cde098cf3f2f84d3c053e67c9871d492ba62a0ca7d1d9e695610 | 63 |
| REPOSITORY_ARCHITECTURE.md | 4bde46a39961bff9e99f7e5f82b6e57c7a911f437a79c1436d37cdcfa9ff1f3 | 63 |
| SOURCE_INTEGRITY_THREAT_MODEL.md | bdb82719e05a7c7a41b0f9bdce409b37f31f7a08d6327f710ba5da0d6044f13 | 63 |
| UNRESOLVED_DECISIONS.md | e562031d15d14ea74724b520db9cbe6a5b62b85105c611fb1430c9a6cddf4a0 | 63 |

These four entries fail the manifest's full-digest encoding check. Their actual current SHA-256 values were not recalculated in this stopped pass. Padding or correcting the strings by intuition would conceal the failure and is prohibited.

## 5. Coverage of this stopped verification pass

| Result | Count | Files |
|---|---:|---|
| Exact bytes matched remote Git blob and SHA-256 matched approval | 11 | CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md; DEFINITIONS_AND_UNITS.md; OBSERVABILITY_AND_REPORTING.md; PHASE_0_PLAN.md; PROJECT_INSTRUCTIONS.md; SPEC_AUDIT.md; SUCCESS_CRITERIA.md; THEORY_SOURCE_MAP.md; THEORY_TO_CODE_TRACEABILITY.md; V0.1_PRODUCT_SPEC.md; VALIDATION_PLAN.md |
| Exact bytes matched remote Git blob but SHA-256 failed approval | 1 | DEPENDENCY_STRATEGY.md |
| Manifest digest encoding failed; actual SHA-256 not recalculated | 4 | PRIVACY_AND_DATA_HANDLING.md; REPOSITORY_ARCHITECTURE.md; SOURCE_INTEGRITY_THREAT_MODEL.md; UNRESOLVED_DECISIONS.md |
| SHA-256 not recalculated in this pass | 2 | GOVERNANCE_AND_HANDOFF.md; LICENSING_NOTES.md |

The last two entries are unverified here, not passed. This is not a completed eighteen-file integrity certification. No machine-readable baseline_manifest.json is issued from this defective approval table.

## 6. Execution environment and checks actually performed

Authoring verification ran on Linux with CPython 3.13.5, Git 2.47.3, GNU coreutils 9.7 and OpenSSL 3.5.5. These describe the verification environment only; they are not selected project dependency pins or claims of supported runtime platforms.

Checks performed: pinned ref/tree reads; approval-table parsing and row/size totals; complete digest-format inspection; exact-byte/Git-blob matching for twelve current specification files and the approval record; SHA-256 comparison for those twelve specification files; independent digest and Git-object cross-checks for the failed dependency entry.

The first strict manifest parser rejected the incomplete digests. A diagnostic pass then retained the malformed strings to enumerate the defects without normalizing them. The gate remained failed throughout; no permissive parser replaced the acceptance rule.

No toolkit package was installed, no product test or CI workflow was run, and no runtime or analytical behavior was implemented. Official licensing/toolchain pages were consulted before the stop; no toolchain selection or license-source byte-comparison pass is claimed.

## 7. Changed files and repository delivery boundary

The only new repository path in this stopped work item is PHASE_1_PROGRESS.md, an allowed P1-W01 output. Publish it on the named review branch and submit a draft review pull request. Keep main at the intake commit pending resolution and review. Do not merge a failed gate or treat a draft PR as completion.

README.md, LICENSE, NOTICE, CONTRIBUTING.md, SECURITY.md, .gitignore, .gitattributes, scaffold/baseline_manifest.json and scaffold/toolchain_review.md have not been created. All eighteen approved specifications, PHASE_0_APPROVAL.md and PHASE_1_PLAN.md are unchanged.

The actual progress commit and PR are recorded in the repository review conversation after their creation. This file does not invent or embed its own future commit hash.

## 8. Narrow repair authorization required

Request a scoped metadata correction of PHASE_0_APPROVAL.md outside the ordinary W01 allowlist. The proposed repair is to obtain all eighteen complete files from the already approved immutable snapshot, verify their Git blob identities, recompute every SHA-256 and correct the approval table with an explicit revision/correction record.

Preserve the approved content commit, owner approval event, analytical decisions, eighteen specification byte sequences, license choice and phase boundaries. Do not rewrite Git history or treat the correction as a new theory/design approval. Recheck the two previously unrecomputed entries rather than assuming only the five demonstrated defects exist.

After that correction is explicitly authorized and completed, calculate the repaired approval file's new independent hash, rerun the full W01 freeze gate, and resume the remaining W01 work. No frozen file may be edited under the present authorization merely to make its hash match a prior claim.

The approval event for the Phase 1 plan is recorded and remains intact. P1-W01 completion, acceptance, merge and authorization of P1-W02 remain pending.
