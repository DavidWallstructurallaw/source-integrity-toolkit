# PHASE_2_PROGRESS

## Document control

| Field | Value |
|---|---|
| Revision | 0.21 |
| Work unit | P2-W08: exact-head matrix, clean installation and evidence audit |
| Owner repair instruction | 批准 P2-W08-R01 继续已授权的 W08 工作 |
| Accepted W07 merge | 22bd51454e425cf9eca87adbebecb09191fb925d |
| Accepted W07 head | 384615aeba3e48b3e22486065c5f5e21e092e368 |
| Approved plan | PHASE_2_PLAN.md revision 0.1, sections 14, 16 and 17 |
| Repair | P2-W08-R01: seven additional paths, expressly approved |
| Branch / PR | phase2/p2-w08 / 17 |
| Code head | 9450b0decc5a02fbcee38beecfe6c4715741efef |
| Code-head tree | 3b14fa3825e46174b2d81d4be3b7373e67a859ac |
| Code-head run | 35500231752, attempt 1 |
| Status | Code-head four-profile evidence verified; final record-head gate pending |
| W08 owner acceptance / merge / W09 | Pending / not authorized / not started |

## 1. Actual continuation and retained history

PR #16 accepted W07 and merged at the SHA above. Its final run 35493868977
executed 1629 tests per profile. The W08 intake a6847f90 recorded a policy-stage
mismatch and proposed R01 without executing a known-invalid W08 matrix.
The owner subsequently approved R01, implemented in code head 9450b0d and
submitted in draft PR #17. This continuation verifies that existing candidate.

W07 progress revision 0.20 and its complete evidence ledger remain byte-pinned
in the predecessor commit. Their pending-at-submission text is historical;
later W07 acceptance is established by PR #16 and its merge. Earlier failed
runs 35488938338 and 35489414729 remain failures, with their original records.
The evidence ledger links the exact history rather than overwriting its meaning.

## 2. Authorized transition

R01 advances only the module-policy active_unit from W07 to W08. The thirteen
promotions, first-unit map and plan identity remain unchanged. The CI driver
recognizes exactly the seven approved additional paths for W08; other units
retain their immediate scopes. Named historical checks include only that exact
delta, and fixed Git bytes plus AST comparisons protect the remaining code.
The four temporary-package mutation cases use independently supplied trusted
context and retain their original positive controls and rejection assertions.

Eleven W08R01Tests were added. All 48 product modules, the checker, workflow,
dependency pins, source schema, fixtures and logical oracles retain accepted
bytes. The code candidate changes nine paths including the earlier intake
review. This record successor changes only the four already allowed files:
progress, implementation evidence, CI review and README. The complete review
branch therefore has twelve changed paths and no new repository path.

## 3. Inspected code-head matrix

| Profile | Actual Python | Job | Artifact | Passed / failed / errors / skips |
|---|---|---|---|---|
| ubuntu-24.04-py3.11 | 3.11.16 | 106050594819 | 10602146363 | 1640 / 0 / 0 / 0 |
| ubuntu-24.04-py3.13 | 3.13.15 | 106050594778 | 10601564336 | 1640 / 0 / 0 / 0 |
| windows-2025-py3.11 | 3.11.9 | 106050594759 | 10601902040 | 1640 / 0 / 0 / 0 |
| windows-2025-py3.13 | 3.13.15 | 106050594671 | 10600999884 | 1640 / 0 / 0 / 0 |

All four jobs and their required steps completed successfully on the exact
code head. Each full evidence archive was downloaded, compared with its
service-record byte length and SHA-256, and checked for CRC errors. Raw JUnit
testcase identities equal the corresponding collection, with no duplicate,
failure, error or skipped element. All 1629 predecessor identities remain,
and the eleven additions are exactly W08R01Tests. Each profile reports 428
successful subtest events separately from its 1640 top-level tests.

Sorted LF-joined top-level node IDs, including the final LF, have SHA-256
`70a5c598be8cb7198eade136504590a65b5e522ea40e443e9c7e05130b142426` in every profile.
The predecessor collection was independently read from verified W07 artifact
10600206895, matching its recorded 1629-node digest.

Actual twenty-file frozen guards and forty-eight-module guards pass before
and after execution. Entry checks cover the actual 124-file Phase 1 and
125-file Phase 2 intake archives. All 154 tracked file hashes agree with the
tested commit, remain unchanged through testing, and agree across profiles.
The metadata records actual Python and runner-image versions, reviewed wheels,
dependency installation and exact job/artifact identities.

## 4. Clean installed runtime and distribution evidence

The additional installed witness builds with the inherited toolchain, installs
offline into a pip-free runtime, and checks that its only distribution is
source-integrity-toolkit. All 48 imported module hashes match the reviewed
source. Both private preparation modes accept each of the four frozen H7
fixtures, totaling eight cases. Both empty-input modes reject; public API
calls still refuse, and the inherited helper checks unchanged CLI refusal.
Only PC01 completes; no analytical results or max-level field are created.

Preparation and public calls produce no observed file, socket or native-loading
effects. Three deliberate negative probes exercise the armed observers for
open, DNS and native loading. Imports occur before this witness arms its hook;
the separate cumulative import-inertness tests remain required and passed.

Both ordinary packaging and the W08 witness record 65 regular source archive
members and 55 members in each original/rebuilt wheel. Original and rebuilt
wheel member contents agree within each profile. Exclusions and absence of
runtime dependencies are exercised by the unchanged packaging tests. No new
module path, package-data selection or schema loader is introduced.

The downloaded evidence contains execution records and member hashes, not
distribution binaries. This review verifies those records and their agreement
with Git source; it does not claim to reread absent binaries or prove whole-archive
reproducibility across operating systems. Windows Server tests do not certify
future native Windows 11/NTFS behavior.

## 5. Final successor and handoff

The separate assistant review found no blocking R01 defect and executed 46
transition checks locally on Python 3.12.14. Those supplemental checks do not
replace the four required hosted profiles.

Commit this documentation/evidence successor, run the unchanged cumulative
matrix on its own exact SHA, and record the raw-result audit in PR #17 after
that commit exists. The external PR record is the final-head gate and prevents
a self-referential evidence-commit claim. Keep the PR draft if any required
job or evidence check fails. W08 owner acceptance and merge remain separate.

PC02-PC24, all fifteen analytical families and 228 analytical obligations remain
pending. Public auditing, report generation, native file interfaces and release
remain unavailable. W09 has not started. Its already identified policy-path
maintenance dependency must be handled under its own authorization; R01 grants
no W09 immediate edit permission. No Phase 2 completion is declared here.
