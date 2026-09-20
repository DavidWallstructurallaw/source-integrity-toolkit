# PHASE_2_PROGRESS

## Document control

| Field | Value |
|---|---|
| Revision | 0.20 |
| Work unit | P2-W07: integration, counterexamples and isolation regression |
| Owner repair instruction | 批准 P2-W07-R01 继续 |
| Accepted W06 merge | 4f55252d98f9b57975c2bc241c9079ac259a53cd |
| Accepted W06 head | d02d32051c595ea1aa64652f536e497d93be2763 |
| Approved plan | PHASE_2_PLAN.md revision 0.1, sections 13, 16 and 17 |
| Plan SHA-256 | bea21992edf58b77cfe0f9a128bb31cee9226a9ea5e87b829663a47768227918 |
| Repair | P2-W07-R01: six additional paths, expressly approved |
| Branch / PR | phase2/p2-w07 / 16 |
| Code head | f0b237d1c4f045110b495db1046a06383c848a02 |
| Code-head tree | c151d8cc5c7d2f52d73c06e9356bfc72fa5a605f |
| Code-head run | 35493411483, attempt 1 |
| Status | Code-head four-profile evidence verified; final record-head gate pending |
| W07 acceptance / merge / W08 | Pending / not authorized / not started |

## 1. Accepted implementation and preserved failures

The accepted implementation is W06 merge 4f55252d98f9b57975c2bc241c9079ac259a53cd.
All 48 product modules keep those exact bytes. No input, analytical or public
behavior was changed in this test-focused work unit.

The original W07 test candidate b0128e542aec927f708a461dca1a92b98754f6e6 and its
record successor 067802f8df5b6958adde60bc7ced3ca8a06a7f33 remain in history.
Runs 35488938338 and 35489414729 each failed in four profiles before test
collection. Their module policy still said W06 while the trusted review branch
resolved to W07. The earlier assumption that the old marker could be retained
was incorrect. Those failures are preserved, including progress revision 0.19,
the exact predecessor evidence ledger, PR #16 and eight failure archives.
They provide no W07 product-test pass. Earlier W04/W05 repairs and W06 acceptance
continue to be documented at their original commits and PRs.

The owner then explicitly approved P2-W07-R01. The repair commit above is a new
execution candidate. All seven repaired blob identities matched independently
prepared local bytes before tree construction. No failed run was overwritten,
relabeled, skipped or made successful by weakening a guard.

## 2. Exact repair and scope

module_policy.json changes only active_unit from P2-W06 to P2-W07. Its thirteen
promotions, earliest-unit map, format and plan digest are unchanged. The trusted
unit still comes from the review event, independently of candidate metadata.

The CI driver registers exactly the six approved W07 extra paths. The four named
permission-test bodies recognize that exception through guarded insertions;
all their original assertions remain. The append-only transition ledger retains
every historical byte and all 194 original identity rows. Other units gain no
new immediate modification authority. The checker itself remains unchanged.

Nine additional W07R01Tests in the already allowed transition-test file verify
exact pinned preimages and replacements, mismatch refusal, forbidden promotions,
the six-path boundary, append-only history, all 48 unchanged product files and
the unchanged checker, plus every statement in the original transition tests.
These tests ran in the complete hosted Git checkouts; local syntax inspection
was not substituted for their runtime result.

The complete branch changes eleven paths: nine existing files and two new test
files. The new files remain test_preparation_pipeline.py and
test_preparation_inertness.py. The repair introduced no new installed module,
product behavior, observer relaxation, fixture, schema, oracle, dependency pin,
workflow permission, source-license or frozen-specification change.

## 3. Executed W07 integration checks

The independently authored fictional two-Inquiry dossier checks the complete
private admission and navigation pipeline. Distinct IDs survive identical
labels, locators and protected keys. Selected or late-unbound structural defects
reject the entire snapshot; lawful gaps, unsupported documentary assertions,
protected references and source relation cycles remain preserved.

The independent projection oracle resolves retained facets against their actual
normalized source fields. Deliberately removing a record or corrupting presence,
value or collection must be detected. All four unchanged H7 fixtures run through
both private input modes, preserving input populations and every retained facet.
The 26/36 and 25/25 analytical expectations are not computed or passed to the
product. Unknown and multiparent input distinctions remain source data.

Permutation and repeat-call tests cover input immutability, cross-Inquiry
isolation, normalization and absence of stale snapshots. Real nested extension
depths and numeric token lengths exercise different structural/resource stops.
Injected monotonic clocks test the actual shared deadline before and after
admission without claiming a wall-clock performance benchmark.

Fresh subprocesses exercise actual open/io.open, directory enumeration, DNS,
native loading and process-launch negative controls. Metadata access uses a
separately named trap, not a fabricated open event. Source text, locators and
forged control-looking metadata remain data. Fault injection includes opaque
exceptions, MemoryError, cancellation and resource interruption; diagnostics
preserve actual input state without exposing source canaries or partial output.
Temporary package copies test forbidden analysis/report/native implementations
with pristine positive controls. The actual checkout is not modified.

## 4. Code-head matrix and independently inspected evidence

| Profile | Actual Python | Job | Artifact | Passed / failed / errors / skips |
|---|---|---|---|---|
| ubuntu-24.04-py3.11 | 3.11.16 | 106032099763 | 10599492725 | 1629 / 0 / 0 / 0 |
| ubuntu-24.04-py3.13 | 3.13.15 | 106032099882 | 10600550118 | 1629 / 0 / 0 / 0 |
| windows-2025-py3.11 | 3.11.9 | 106032099840 | 10600046516 | 1629 / 0 / 0 / 0 |
| windows-2025-py3.13 | 3.13.15 | 106032099844 | 10600031557 | 1629 / 0 / 0 / 0 |

Each profile collected and passed 1629 top-level instances with zero failures,
errors or skips. All 1465 W06 predecessor identities remain. Additions total
164: 116 pipeline instances, 39 integrated security instances and nine R01
regressions. The 428 successful subtest events per profile are counted separately.
The same suite ran four times; this does not create four times as many distinct
test designs.

All four complete ZIPs were downloaded and their lengths, SHA-256 and CRC
verified. Raw JUnit identities independently equal the collection identities,
with no failure/error/skipped element anywhere in the documents. Full source
and test identity digests and exact artifact identities are in
phase2/implementation_evidence.json and the review record.

Each hosted checkout recomputed the real 124-file Phase 1 and 125-file Phase 2
entry snapshots. Twenty frozen files and all 48 product modules passed before
and after tests. All 154 tracked hashes agree across profiles and remain
unchanged. All 48 product hashes match accepted W06, including 35 protected
Phase 1 slots. Exactly the approved eleven branch paths are accounted for.

Pinned development dependencies, including setuptools 84.0.0 and pytest 9.1.1,
were actually installed. Existing offline clean-install and source-rebuild tests
passed. The source distribution has 65 regular members; original and rebuilt
wheels each have 55 members and equal member names/content hashes. The evidence
ZIPs contain reports and inventories, not binary distribution archives; no
independent reread of absent binaries or whole-archive reproducibility is claimed.

## 5. Coverage, limits and final gate

The evidence ledger keeps all seven shared requirement families partial and
identifies exact executed test entry points, source/fixture hashes, independent
expected outcomes and accepted implementation commit. Only PC01 is implemented
as a whole prerequisite. PC02-PC24, all fifteen analytical families, all 228
analytical test obligations, reports, public auditing and native file I/O remain
unimplemented. Passing preparation tests does not certify those operations.

Local work used a partial workspace: exact source fingerprints, replacements,
syntax and AST checks were executed. Git cloning failed DNS. Runtime claims here
come from the hosted four-profile evidence, not an invented local full-suite run.
The finite checks do not constitute scientific validation, a universal hostile
same-process sandbox or native Windows 11/NTFS certification.

This successor updates only PHASE_2_PROGRESS.md and
phase2/implementation_evidence.json. Product and test bytes remain at the verified
code head. The successor must have its own exact-head four-profile CI inspected.
Record the resulting commit/run/job/artifact gate externally in PR #16 to avoid
an endless self-referential documentation cycle. Keep the PR draft on any failure.
After the final gate, request owner acceptance; do not merge PR #16, start W08,
activate auditing or publish a release without separate authorization.
