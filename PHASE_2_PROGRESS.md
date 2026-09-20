# PHASE_2_PROGRESS

## Document control

| Field | Value |
|---|---|
| Revision | 0.15 |
| Work unit | P2-W05 with approved R01 and R02 |
| Owner instructions | 批准 P2-W05-R02; 继续; 可以继续工作吗 |
| Accepted W04 merge | a1f102d82b7321f47df98f2672b91491cbd7fc9f |
| Verified R01 predecessor | 655f99e35052d56790f28d0c7971515c92b9ea6d |
| Verified W05 code head | 8e6c3df38267b21db8d11b5d047c8883c430648c |
| Verified W05 code tree | caf598a7b7fe00149f4ca1d5d85f984541e5ded4 |
| Approved plan | PHASE_2_PLAN.md revision 0.1, sections 3-6 and 11 |
| Plan SHA-256 | bea21992edf58b77cfe0f9a128bb31cee9226a9ea5e87b829663a47768227918 |
| Branch / review | phase2/p2-w05 / PR #14 |
| Status | Code-head four-profile CI and complete artifacts verified; exact successor-record gate pending |
| W05 owner acceptance / merge | Not granted |
| W06 / release | Not started / not authorized |

## 1. Resumption and preserved authority

The owner has already authorized W05, R01 and R02. This resumption does not
request those approvals again. It re-read PR #14 and found the W05 code candidate
above already present, with cumulative run 35473989542 completed successfully.
The preceding conversation's inability to confirm later work did not establish
that no remote commit existed. This record verifies the actual existing candidate;
it does not claim to have recreated its implementation or its earlier local runs.

The complete revision 0.14, original local results, scope decisions and code
candidate are retained at 8e6c3df38267b21db8d11b5d047c8883c430648c. Earlier R01
materialization, accepted W04 and all recorded failures remain in Git and PR #14.
The R01 migration run 35436261547 remains historical evidence for 724 tests,
not evidence of W05 validation.

The attached theory manuscripts do not amend the frozen engineering baseline,
input contract, analytical meanings or licensing. No additional repair or new
execution scope is introduced by this resumption.

## 2. Exact verified implementation scope

The complete W05 diff from accepted W04 contains twenty-one paths, including
five new test files. It fits the original seventeen paths plus five approved
R01 paths and the one approved R02 path. The unused allowed paths remain
contracts/bundle.py and tests/contract/test_evidence_basis.py. No path was deleted
or renamed.

Five product files differ from W04: contracts/evidence.py, runtime/boundary.py,
validation/structure.py, validation/references.py and validation/semantics.py.
The last two promotions bring the reviewed implementation ceiling to thirteen
slots; thirty-five installed modules retain their Phase 1 bytes. The complete
package still contains forty-eight modules.

This successor changes only PHASE_2_PROGRESS.md and
phase2/implementation_evidence.json. No product code, existing or new test,
schema, input-coverage map, module policy, transition ledger, fixture, oracle,
frozen source/plan, dependency, license, package configuration or workflow changes.
The final record head requires its own complete four-profile gate.

## 3. Private input preparation and retained boundaries

The private _prepare_value and _prepare_utf8 entry points now complete bounded
capture, closed-shape checks, snapshot-wide identity and reference checks,
endpoint and exact Claim compatibility, time syntax, immutable normalization
and indexes, and the finite explicit scope plan under one nonresetting budget.
The trusted boundary records acceptance only after all those operations and
construction of the complete result. No partial tree is returned after failure.

_capture_value and _capture_utf8 remain separate, noncertifying capture
components. The same empty object can be captured and rejected by full
preparation. Public audit_bundle, audit_file and the CLI remain refusal stubs;
there is no public validation bypass or file-opening claim.

The implemented source-bound input checks cover fifty declared shapes and
242 fields, twelve record kinds, twenty-four predicates and nine assessments.
Valid sparse, protected, unresolved, disputed, denied/inactive and cyclic
evidence remains input. Supplied labels, Gaps, attributions and native correction
states do not become qualified analytical conclusions.

Captured source context remains separate from normalized order. Top-level
entities, typed reference sets and role bindings use their specified ordering;
narrative and extension arrays preserve order. Rebased role-indexed Gap selectors
address the normalized structure while captured_tree retains original context.
No source identity is merged or fetched through a locator or predecessor.

Time syntax is checked without local timezone assumptions or float rounding.
Known same-precision reversed windows produce a private observation while
remaining admissible. Unspecified mixed-precision boundary conventions, grant
applicability, event causality and analytical eligibility remain deferred.

Only PC01's input-admission check is implemented. PC02-PC24, all fifteen
analytical families, the 228 analytical test obligations, graph qualification,
origin/independence/HHI calculations, correction judgments, report assembly,
native file I/O and public auditing remain pending. W06 observability assembly
has not begun.

## 4. R01/R02 and actual test identity preservation

R01 retargets the original W04 component tests to their capture-only boundary.
R02 replaces only the named schema test's unconditional pending/empty status
assertion with strict private-admission status and real runtime witnesses.
The historical test name and every unrelated old assertion remain. Git/AST
regressions enforce the named allowance. No permissive status-or condition,
blanket skip, xfail, deselection or generic-exception success was substituted.

All 724 predecessor identities were independently matched against the inspected
R01 and W04 collections and retained in the W05 raw results. The 596 additions are:

| Test file | Added collected instances |
|---|---:|
| tests/contract/test_typed_records.py | 225 |
| tests/contract/test_assertion_contract.py | 146 |
| tests/contract/test_temporal_contract.py | 57 |
| tests/unit/test_reference_validation.py | 57 |
| tests/integration/test_prepared_hero_inputs.py | 96 |
| tests/contract/test_input_schema_mapping.py | 15 |

The two new Git-dependent R02 controls that could not execute in the earlier
partial local workspace now executed and passed in all four full checkouts.
The original capture observer, real file/DNS/native negative controls and
prior constant-only diagnostic regressions remain in the cumulative suite.

All four unchanged H7 inputs passed full preparation through both object and
supplied-byte seams. Population/oracle tests check retained input membership
and separate scopes without supplying or calculating analytical result values.

## 5. Inspected code-head hosted evidence

Run 35473989542, attempt 1, checked the exact W05 code head and tree listed above.
Every required step in all four jobs succeeded.

| Profile | Actual CPython | Runner image | Job ID | Collected / passed | Failures / errors / skips |
|---|---|---|---:|---:|---|
| Ubuntu 24.04 | 3.11.16 | 20260907.300.1 | 105979927694 | 1320 / 1320 | 0 / 0 / 0 |
| Ubuntu 24.04 | 3.13.15 | 20260907.300.1 | 105979927596 | 1320 / 1320 | 0 / 0 / 0 |
| Windows Server 2025 | 3.11.9 | 20260907.229.1 | 105979927967 | 1320 / 1320 | 0 / 0 / 0 |
| Windows Server 2025 | 3.13.15 | 20260907.229.1 | 105979927686 | 1320 / 1320 | 0 / 0 / 0 |

Each raw JUnit document has 1,320 direct testcase elements. Every classname/name
pair was matched independently to collected node IDs. The 428 successful subtest
events per profile are separate, giving 1,748 reported events. The four profiles
repeat one suite; they are not 5,280 distinct test designs.

SHA-256 of sorted 1,320 node IDs joined by LF with one final LF:
83400fa1c4a3cb9592630dc119167f9cd00936788d5803c64ed1f983bcb82f62.

| Profile | Artifact ID | ZIP bytes | SHA-256 |
|---|---:|---:|---|
| Ubuntu 3.11 | 10593887639 | 77516 | 22a6b1a3c24e49170745fffc4e254e660881446009b7c4b83c966ca5a3486a3c |
| Ubuntu 3.13 | 10594027542 | 77397 | 7607c5e22f8079d868629364c82e5ba54a513623590ea43369add29020124699 |
| Windows 3.11 | 10593192348 | 83835 | eac5b8ff6e20ef88a61f88a3d91938b79388f439c32e516094e7495d4d38fc68 |
| Windows 3.13 | 10593491885 | 83704 | fa364c73a915e7aab6fd3dd64c9f3f07fcdf7e637132e11f18c0f0a06e2c6624 |

All complete ZIPs were downloaded, matched to service byte counts and SHA-256,
CRC checked and inspected. No job-status badge alone was used as test evidence.
Environment, exact commit/run, collection, raw JUnit, pytest logs, exit code,
entry/scope, dependency records and before/after guards agree.

The full hosted checkouts recomputed the 124-file Phase 1 and 125-file Phase 2
entry snapshots. Twenty frozen files and forty-eight modules passed before and
after tests. All 148 tracked-file hash maps agree across profiles and remained
unchanged during execution. Their comparison against accepted W04 confirms
twenty-one changed paths and five additions, with no other byte differences.

The approved setuptools 84.0.0, pytest 9.1.1 and supporting development pins were
installed and checked. Executed package tests and inventory evidence show
65 regular sdist members and 55 members in both original and rebuilt wheels.
Wheel member names and hashes agree; tracked source-member hashes agree with
the actual checkout. Clean offline installation tests passed.

## 6. Evidence limits and final gate

This resumption performed connected-source checks and independent inspection of
downloaded evidence. A local full-clone attempt still failed DNS resolution.
No complete local checkout or new local product-test run is claimed. The evidence
ZIPs contain package inventories and executed test results, not the package
binaries; the resuming assistant did not independently reopen absent binaries.
Whole-archive byte reproducibility, native-platform security certification,
arbitrary same-process isolation and scientific validation are not claimed.

The prior local 83-pass/eight-failure integration run, corrected test ordering,
594 selected local passes and unavailable local Git controls remain recorded
at revision 0.14 and in the unchanged local-evidence object. No failure history
was deleted or replaced with a pass.

The code-head gate is complete. This two-record successor must pass the same
four-profile cumulative CI on its exact head. Record final-head run and complete
artifact evidence in PR #14 rather than inventing a circular self-commit hash
inside these records. Do not mark ready until that evidence is inspected.

Stop after W05 technical delivery for owner acceptance. Do not merge PR #14,
advance main, start W06 or publish a release under the present instruction.
