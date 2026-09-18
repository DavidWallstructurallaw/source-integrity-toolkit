# PHASE_1_PROGRESS

## Current control record

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Progress revision | 0.6 |
| Date | 2026-09-17, project-local date; merge timestamps use UTC |
| Approved plan | PHASE_1_PLAN.md revision 0.1, blob `27ed33cb1c2afc78b12ca099ee7ccb4e68d63bfb` |
| Owner instruction | `合并 PR #3，再开始 P1-W03` |
| Accepted predecessor | P1-W02 at `9fb556f2035d84abc03f83c422259f7a8d588110` |
| Merged PR | #3, merge method preserving commit history |
| Merge / W03 intake | `0ff5644349b31214aa0691d8d94385f374f530a8` |
| Review branch | `phase1/p1-w03` |
| Work-unit result | W03 static catalog and reservation checks passed; submitted for owner review |
| Owner acceptance / W03 merge | Pending |
| W04 and later execution | Not started |

## 1. Accepted predecessor and preserved history

The owner explicitly accepted the W02 handoff by requesting its merge and the next named unit. Before merging, the connected PR record still showed the expected head, an open non-draft PR and successful selected-toolchain run `35307485434`. The merge used expected-head protection and produced the intake commit above. GitHub subsequently confirmed `merged: true` and merge time 2026-09-18 04:50:52 UTC.

The full W02 progress and review evidence remain at commit `9fb556f2035d84abc03f83c422259f7a8d588110`, in `PHASE_1_PROGRESS.md` and `scaffold/toolchain_review.md`. They preserve the local 77-pass/1-fail history, the selected-toolchain hosted passes, and their exact evidence scope. That prior CI result is not relabeled as a W03 run.

The eighteen-file Phase 0 baseline, corrected approval revision 1.1, Phase 1 plan, baseline manifest, licenses, package files, tool pins and W02 tests remain unchanged. The W03 branch begins at the actual merge, not a reconstructed or independently advanced base.

## 2. Exact W03 delivery scope

This unit creates the eight new paths and updates the common progress record allowed by plan section 7:

```text
schemas/README.md
schemas/bundle/README.md
schemas/report/README.md
scaffold/module_manifest.json
scaffold/trace_catalog.json
scaffold/obligation_catalog.json
tests/scaffold/test_contract_catalogs.py
tests/scaffold/test_module_manifest.py
PHASE_1_PROGRESS.md
```

The three schema documents reserve the adopted logical names `sit-bundle/0.1` and `sit-report/0.1`. No executable or permissive empty schema is added.

The finite module manifest covers the exact 48 accepted W02 Python files and records their accepted Git blob identities, layer restrictions, owner labels and scaffold form. It retains all nineteen owner bindings, including the non-runtime test/CI home of VALIDATION_GOVERNANCE. REPORT_PRESENTATION retains the later section 16 semantic authority in `reporting/assemble.py`, with both renderers and escaping as supporting homes. A wildcard in a source responsibility label never enables dynamic discovery or new files.

The trace and obligation indexes transcribe the following adopted registries:

| Registry | Entries |
|---|---:|
| Trace responsibilities | 35 |
| Logical owners | 19 |
| Analytical families | 15 |
| Registered output fields | 57 |
| P/N/M/B field obligations | 228 |
| Shared validation families | 26 |
| Prerequisite codes | 24 |
| Reason codes | 40 |
| Finding conditions | 22 |
| Data-handling control references | 20 |
| Resource-limit references | 14 |
| W9 control cases | 24 |
| W9 licensing cases | 6 |
| W11 realization cases | 32 |

## 3. Source fidelity and reference design

The primary registry rows come from the frozen traceability, reporting and validation documents. Trace records preserve their exact controlling specification text, source/product/acceptance IDs and non-negotiable interpretation limits. Every field retains one primary Trace, its value kind and four separately named test obligations.

The 228 expectations are exact pointers to their full validation-table cells, with one-based source line and zero-based cell index. Shared test families reference their complete section spans. Full source-file identities and mandatory surrounding sections accompany these references. These are navigable indexes into the adopted specifications; they do not replace a qualified paragraph with a short title or turn a logical oracle into a computed result.

W9 controls and W11 cases retain their original names, document sections, existing shared-owner links and exact future test bindings where supplied. A W9 case with no assigned individual test filename is not given an invented one. Later governance section 22 and dependency/architecture refinements remain binding. In particular, `outside_v01` is retained exactly, including its digits, and native source failure stays distinct from execution failure.

All analytical and native-runtime implementation/test statuses remain pending. Existing W01 licensing and W02 scaffold evidence are separate historical facts. Catalog completion does not reset those facts or promote future domain obligations to passing.

## 4. Actual tests and review evidence

The two new test files use Python's standard-library unittest. No external dependency was installed, no selected version was changed, and no W02 tool-version assertion was skipped or relaxed. These tests can also be collected by the already selected pytest runner in later authorized CI.

Actual local command, with bytecode writes disabled:

```text
python -m unittest discover -s tests/scaffold -p 'test_*.py' -v
```

The controlled local W03 verification view contains exactly the two new test files in that directory. This run therefore executes W03 tests only. The committed reservation README gives separate per-file commands suitable for a full repository checkout.

Observed environment: CPython 3.13.5 on Linux x86_64, glibc 2.41. Result: **19 tests passed, 0 failures, 0 errors, 0 skipped**. Eleven methods check contract catalogs and eight check the module manifest. Included negative probes exercise twenty mutated catalog copies and one mutated product-file byte sequence; a separate duplicate-key probe is also active. These totals are static test methods and mutation probes, not the 228 unimplemented analytical tests.

Checks cover full-byte identity of the three primary registries; exact table-set equality; field kinds and primary ownership; every P/N/M/B cell reference; complete shared-family spans; registered codes and finding associations; W9/W11 finite cross-links; all 48 accepted package blobs and forms; presentation/governance homes; absent executable schema; and absence of a catalog dependency in product source.

The local view was assembled from preserved original deliverables and byte-matched W02 module files. Relevant newer supplement sections, the approved plan and current repository identities were read through the GitHub connector. A direct clone could not resolve github.com in this execution environment. No successful full clone or fresh local rehash of all eighteen complete newer documents is claimed. Remote tree/diff equality establishes preservation of paths outside the nine-file allowlist; the three complete primary documents and the 48 module files were independently inspected as local bytes.

The authoring extractor initially treated a finding-table header as a data row and initially omitted the digit-bearing `outside_v01` reason. Its count checks rejected both attempts before publication. The extractor was corrected to follow the actual frozen rows; no source or expectation was changed. The final committed test files independently check those registries and include a negative probe removing `outside_v01`.

## 5. Unchanged runtime, packaging and CI boundaries

No package code is modified. The existing API stubs still immediately raise NotImplementedError and the CLI still uses its temporary refusal. No parser, normalizer, validator, observability classifier, graph operation, HHI, correction logic, renderer, native adapter or quota engine is implemented, including inside developer tests.

No new build, wheel publication, Windows run, Python 3.11 run or hosted W03 test execution is claimed. The dedicated early workflow remains limited to PR #3/phase1/p1-w02. A skipped job on another PR would not constitute W03 CI evidence. General CI and packaging expansion remain at their approved later work units. No workflow is altered to bypass this scope.

The catalogs remain repository-level developer data and are not runtime plugin registries, evidence bundles or public report schemas. Existing package selection and runtime dependencies are unchanged. Theory PDFs, private evidence and additional theory interpretations are not introduced.

## 6. Delivery and next gate

The outgoing package is restricted to nine allowed paths. Final remote commit/tree, PR number, exact outgoing hashes and remote preservation checks are recorded in the PR handoff after those identities exist, without self-referential file hashes.

P1-W03 is submitted for owner acceptance. Do not merge its review branch or begin P1-W04 automatically. The next named unit prepares static hero fixtures and logical expectations only after this delivery is accepted and continuation is authorized.
