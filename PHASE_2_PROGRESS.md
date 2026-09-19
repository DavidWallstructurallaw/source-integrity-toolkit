# PHASE_2_PROGRESS

## Document control

| Field | Value |
|---|---|
| Revision | 0.8 |
| Work unit | P2-W04 intake |
| Owner instruction | 批准并合并 PR #12，再开始 P2-W04 |
| Approved plan | PHASE_2_PLAN.md revision 0.1, sections 6 and 10 |
| Plan SHA-256 | bea21992edf58b77cfe0f9a128bb31cee9226a9ea5e87b829663a47768227918 |
| Accepted W03 merge | e292bf6023a59d3019221a768d9f2d4ac5c4d4cf |
| Entry tree | ad16a08dc2382b3d007038c4861d010f52a15e4b |
| Branch | phase2/p2-w04 |
| Status | Entry dependency review blocked at proposed P2-W04-R01; implementation has not begun |
| W04 execution | Authorized within the existing plan; additional repair paths await explicit approval |
| W04 acceptance / W05 execution | Not granted |

## 1. Accepted predecessor and preserved history

PR #12 was merged with expected-head protection at the owner's instruction. The accepted head is 4189edc62a9c321dd6eed71c5106cea7311907e6. Its cumulative runs 35419147787 and 35419301845 were confirmed successful before merge. The merge's tree is identical to the reviewed tree and its message contains exactly one SIT-Phase-Unit: P2-W03 footer. W03 is accepted and W04 execution is authorized under the existing plan.

The unabridged preceding progress revision 0.7 and implementation evidence remain at 4189edc62a9c321dd6eed71c5106cea7311907e6. PR #12 records the final exact-head 537-instance four-row verification and its separate 428 subtest events. The initial owner-annotation failure and its correction remain in that history. This intake review does not rerun or relabel those results.

The attached theory sources do not replace any frozen specification. The present issue concerns an implementation seam and its immediate file allowance, not a new theory or public diagnostic rule.

## 2. P2-W04 entry finding: a required cycle rejection has no truthful current qualifier

REPOSITORY_ARCHITECTURE section 17.1 requires an active-ancestor container cycle to be classified as input_constraint_violation. PHASE_2_PLAN section 10 requires that detection during bounded caller-value capture. This concerns a Python container referencing itself through the active ancestry, not a valid cycle in evidence relationships and not a repeated non-cyclic alias.

The accepted contracts/execution.py declares six private constraint qualifiers: exact_integer_range, unicode_scalar, identifier_ascii, identifier_length, string_length and locator_length. runtime/resources.py requires one of these whenever input_constraint_violation is requested. runtime/diagnostics.py accepts the corresponding six fixed normative bases. None describes a container cycle.

A read-only local reproduction against exact accepted source blobs confirmed the seam behavior. Calling the current budget rejection with input_constraint_violation and either no qualifier or the proposed container_cycle qualifier results in execution_failed with input not_completed. Using an existing number/Unicode qualifier instead yields structural rejection with the wrong normative basis. Neither is an acceptable implementation of the cycle rule. The caller-value parser does not yet exist; this is a manually established downstream diagnostic-seam reproduction, not a claim that a completed parser was tested.

| Exact file inspected and executed locally | Accepted Git blob | Bytes |
|---|---|---:|
| src/source_integrity_toolkit/contracts/execution.py | a5d66263f572c2b888d148727b97797a3aa0a521 | 4893 |
| src/source_integrity_toolkit/runtime/resources.py | f27b66d3a2e073aded7f31c6fb30ebff4db90d93 | 4838 |
| src/source_integrity_toolkit/runtime/diagnostics.py | 1873edfdf9379991cb4750b6a8e41f8dd7ccb85c | 5354 |

All three local copies matched their connected-repository Git blob identities before execution. The reproduction ran under CPython 3.13.5 in a partial local workspace. Full local Git access failed DNS resolution. No complete-checkout, selected-toolchain or W04 cumulative-test claim is made from this reproduction.

## 3. Proposed bounded repair P2-W04-R01

This proposal is not yet authorized. Preserve the existing public input_constraint_violation code and all stop states. Add one private constant qualifier, container_cycle, and its fixed REPOSITORY_ARCHITECTURE section 17.1 basis. Do not allow arbitrary qualifiers or source-supplied diagnostic text. The existing resources implementation already imports the constraint vocabulary and does not need modification for this proposal.

The four additional immediate write paths requested are:

| Path outside the original W04 allowlist | Exact proposed purpose |
|---|---|
| src/source_integrity_toolkit/contracts/execution.py | Add the one fixed container_cycle qualifier; preserve existing transport fields, states and validation |
| src/source_integrity_toolkit/runtime/diagnostics.py | Add the matching fixed cycle basis; preserve constant messages, null locations and no-payload rules |
| tests/scaffold/test_ci_contract.py | Record exactly these four owner-authorized W04 repair paths, retaining cumulative accounting without granting other units new immediate permissions |
| tests/contract/test_bundle_contract.py | Refine only the two existing immediate/cumulative exception-accounting regressions for the new explicit W04 exception; retain W02's exact two-path exception, all test identities and observer-preservation assertions |

The last test file is included deliberately: its current R01 regression asserts every other unit has no exception. Changing only the CI driver would therefore contradict that existing assertion. The refinement must explicitly separate the two named owner authorizations instead of removing the no-expansion requirement.

New cycle, repeated-alias, missing/unknown-qualifier, canary, state and scope-counterexample regressions belong to W04's already allowed test paths, especially tests/security/test_input_capture.py. No existing security observer needs weakening or modification. Retain all 537 predecessor test identities, supplement them with the new tests, and execute the complete four-profile matrix before claiming W04 completion.

No frozen specification, approved plan, schema, fixture, expected analytical result, dependency pin, workflow permission, public API/CLI or boundary checker is part of this requested exception. The repair does not authorize graph cycle analysis, new public diagnostic codes, native loading or source access.

## 4. Actual write scope and stopping point

This intake changes PHASE_2_PROGRESS.md only on the W04 branch. All 48 installed module bodies, existing tests, schemas, fixtures, plans, catalogs, manifests, policy and implementation-evidence files remain at the accepted entry bytes. The unchanged module policy still describes the accepted W03 implementation; no W04 slot has been promoted.

No W04 parser/capture implementation, partial-success substitute or diagnostic workaround is committed. A W04 delivery PR has not been opened, because the candidate stops before implementation and its live policy has not advanced. Hosted checks triggered by the preceding authorized main merge concern the accepted W03 tree, not W04 behavior.

Plan section 6 requires a named authorization for repairs outside the current allowlist. Stop for approval of P2-W04-R01, then implement that bounded vocabulary/scope repair together with the already authorized W04 capture work. Preserve the error taxonomy, all limits, independent test expectations and the complete history. W05 remains unauthorized.
