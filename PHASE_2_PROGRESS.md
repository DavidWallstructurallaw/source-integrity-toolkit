# PHASE_2_PROGRESS

## Document control

| Field | Value |
|---|---|
| Revision | 0.14 |
| Work unit | P2-W05 with approved R01 and R02 |
| Owner instruction | 批准 P2-W05-R02; 继续 |
| Accepted W04 merge | a1f102d82b7321f47df98f2672b91491cbd7fc9f |
| Verified R01 predecessor | 655f99e35052d56790f28d0c7971515c92b9ea6d |
| Predecessor tree | 313bd9ac5268132d628cbed79c2e50acb0f811d6 |
| Approved plan | PHASE_2_PLAN.md revision 0.1, sections 3-6 and 11 |
| Plan SHA-256 | bea21992edf58b77cfe0f9a128bb31cee9226a9ea5e87b829663a47768227918 |
| Branch / review | phase2/p2-w05 / PR #14 |
| Status | Full W05 candidate and approved R02 authored; 594 selected new local tests passed; exact-head hosted matrix pending |
| W05 acceptance / W06 | Not granted / not started |

## 1. Authority and preserved history

The owner has accepted W04 and authorized W05, R01 and R02. R02 adds exactly
one immediate path, tests/contract/test_input_schema_mapping.py, to the seventeen
original W05 paths and five R01 additions. No new approval is requested for those
same changes. No merge, W06, public auditing, native I/O or release is authorized.

The complete earlier intake, R01 materialization and migration evidence remain
in Git and PR #14. The preceding 655f99e3 tree passed run 35436261547 in all four
profiles, preserving 724 test identities and 428 separately counted subtest
events per profile. That was capture-test migration evidence. It is never counted
as execution of the newly implemented W05 validator. W04's accepted source and
failure/repair history remain at 80ea8ab34f5881dcb8b6a307391464c752aa6310 and PR #13.

The supplied theory PDFs do not replace frozen engineering sources, authorize a
new metric, or change their licenses. This work implements the adopted canonical
input contract. Scientific validation and independent external review are not
claimed by software conformance tests.

## 2. Closed scope and R02 test transition

The complete proposed W05 branch uses twenty-one paths within the twenty-three
original-plus-repair paths. Five are new test files. This continuation changes
nineteen paths from 655f99e3. R01's two capture unit-test files remain exactly as
already migrated. contracts/bundle.py and test_evidence_basis.py need no W05 edit.

R02 changes the old test's unconditional pending/empty assertion to a strict
private-admission status: PC01 only implemented, PC02-PC24 execution-pending,
no analytical Trace closed and public auditing still unavailable. Its historical
test name and all other schema/source/field/nullability/local-reference assertions
remain. Added regressions reject both stale pending and inflated full-audit claims,
exercise real capture/rejection/admission, and pin the old assertion bodies in Git.

The CI driver adds only the one R02 path for W05 immediate scope and later
cumulative accounting. It retains all old exceptions and all workflow, collection,
checkout and failure controls. Two named scope-test bodies in test_bundle_contract.py
and one in test_input_capture.py recognize that exact addition. The capture observer,
real negative controls, and W04 constant-only diagnostic checks remain unchanged.
The transition ledger is append-only. Every one of the 724 predecessor identities
must execute in the final hosted suite; no skip, xfail, deselection or rename is used.

Only five product files change: contracts/evidence.py, validation/structure.py,
validation/references.py, validation/semantics.py and runtime/boundary.py. The two
newly promoted slots complete the thirteen-module Phase 2 ceiling; the remaining
thirty-five product files keep Phase 1 bytes. No new installed path is added.
Frozen specifications/plans/approvals, schemas, fixtures, analytical oracles,
licenses, dependency pins, workflows and public audit entry points are unchanged.

## 3. Implemented full private preparation

_prepare_value and _prepare_utf8 now perform the complete W05 sequence under one
fixed, nonresetting budget: bounded capture, closed-shape checks, global identity
and reference resolution, endpoint and exact Claim compatibility, time syntax,
immutable normalization/indexing, and finite explicit inquiry/anchor planning.
Only after those operations and construction of the complete result does the
trusted boundary record input acceptance. The public API and CLI remain refusals.

The original _capture_value and _capture_utf8 still target pure W04 capture.
An empty or generic object may be capturable, while full preparation rejects it
for missing or forbidden canonical fields. No public validation switch, caller
budget, schema expression or callback can bypass the complete preparation path.

The validator covers all fifty declared shapes and 242 fields, twelve record
kinds, twenty-four predicates and nine assessment kinds. Required and optional
presence, structural nulls versus factual nulls with Gaps, exact scalar types,
closed enums, namespace-only inert extensions and field-role byte limits stay
separate. Canonical reference occurrences and all four entity collections now
use the original whole-input ledgers. A valid incomplete or protected dossier is
preserved; a malformed dossier is not repaired or partially salvaged.

Identity is snapshot-local and case-sensitive. Sorted immutable entity tables
and charged binary lookup retain every supplied object. A predecessor, locator,
checksum, publisher name or protected key cannot import or merge identity.
Compatible explicit unresolved records remain unresolved. Actual endpoint kinds,
role specialization, exact bound Claims and declared scope intersections are
checked without constructing an eligible graph, traversing ancestry or qualifying
independence, authority or corrective effect. Denials, inactive assertions,
parallel assertions and lawful evidence cycles remain available.

Time checking preserves known date/instant syntax, explicit offset and fractional
precision. It uses no local timezone and no float rounding. A fully known
same-precision inverted window produces a private scoped observation and remains
accepted. Date intervals are never replaced by midnight instants. Mixed-precision
boundary conventions, grant timing, event causality and analytical eligibility
remain with later owners. No public time reason or result state is invented.

The captured immutable source tree remains available alongside the normalized
tree. Entity and reference sets and role bindings follow the adopted ordering;
narrative and extension arrays retain their order. Role-indexed Gap paths are
rebased when a role array is reordered, while captured_tree retains their exact
original spelling and context. Source prose, native states and attribution are
not overwritten. Direct record-link selectors address the normalized source;
the full owning record and role-specific basis remain accessible.

The finite plan retains each Inquiry and its explicit Claims, seeds, targets,
dimensions and times, plus directly scoped Assertion and Anomaly IDs. Evaluator,
pipeline and correction anchors remain in the complete immutable record/link
index. No all-pairs query, graph projection, M001-M015 value, HHI allocation,
independence result, public observability report or correction verdict is created.

## 4. Actual local evidence and limits

The local workspace is partial. Ten predecessor product files and four modified
old tests were reconstructed and checked against their exact accepted SHA-256
and Git blob identities before editing. The transition ledger's full 194-row
historical table was reconstructed from the original inspected collection and
connected text; its complete bytes matched the accepted hash before the append.
The full Phase 2 plan, complete lineage specification and all frozen H7 fixture
and logical-oracle bytes used locally match their accepted fingerprints.

Local execution used CPython 3.13.5 and pytest 9.0.2. It does not substitute for
the approved hosted toolchain. The first new component run passed 422 instances.
The first integration run had 83 passes and eight failures because a new test
compared a reference set by incoming order. Its expected input representation
was corrected to the adopted typed ordering; product code and frozen fixtures
were unchanged. The expanded run then passed 576 instances.

Further review added role-indexed Gap rebasing and original captured-tree
preservation, four direct H7 population/oracle checks, and R02 status regressions.
The final selected local run passed 594 instances, zero failures/errors/skips.
Two new Git-dependent R02 controls could not execute in this partial workspace;
they remain required in hosted CI, alongside every predecessor test. The expected
complete hosted collection is 1,320 instances: 724 retained and 596 added. Counts
must be checked against raw collection and JUnit, not assumed from this estimate.

All four unchanged H7 inputs execute through both the object and supplied-byte
preparation paths. Tests preserve the distinct source, pipeline, correction and
comparison populations without calculating their logical-oracle metrics. New
counterexamples exercise closed fields, all enum/nullable branches, duplicate or
dangling identity, compatible unresolved endpoints, claim mismatch, unsupported
labels, late unselected defects, source-native correction states, real resource
and cancellation boundaries, and failures before/after actual input acceptance.

Fresh isolated-process probes preserve real open, DNS and native-load negative
controls. Product preparation performs none of those operations; only the harness
reads the fictional fixture before installing its observer. All source-derived
failure canaries remain out of diagnostics and captured stdout/stderr. These are
finite checks under the stated ordinary-host preconditions, not a same-process
sandbox, universal memory/latency guarantee or native-platform certification.

The local AST comparisons preserve every old schema assertion except the named
stage check, every old capture observer statement, every unrelated old scope-test
body and all original names/decorators. The old execution/diagnostic/resources,
scalar/decoder/limit modules remain byte-identical. Complete Git archive, frozen
baseline, package and selected-version verification still require hosted CI.

## 5. Exact-head delivery gate

Submit the complete candidate atomically on the existing review branch, verify
its remote blobs and full diff, then run the existing four-profile cumulative CI.
Download and inspect complete evidence artifacts, raw test identities/results,
actual entry/frozen bytes, tracked before/after hashes and package inventories.
Do not infer a W05 pass from the previous migration run or this partial local run.

Record the code-head outcome in a successor progress/evidence commit, then inspect
that exact final head's four-profile run. PR #14 carries the final-head evidence
to avoid circular self-commit hashes in these records. Keep draft on any failing
gate and preserve the failure history. After technical verification, stop for the
owner's W05 acceptance; main, W06 and release remain untouched.
