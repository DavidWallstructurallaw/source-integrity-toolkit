# PHASE_1_PROGRESS

## Current control record

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Progress revision | 0.9 |
| Record date | 2026-09-18 UTC |
| Approved plan | PHASE_1_PLAN.md revision 0.1, blob `27ed33cb1c2afc78b12ca099ee7ccb4e68d63bfb` |
| Owner authorization | `可以，继续P1-W05`, followed by acceptance of the explicitly proposed P1-W04-T01 import, verified merge and W05 continuation |
| Accepted predecessor | W04, PR #5, head `9b3478b394305f4367642fba56f49d443143e565` |
| Actual W04 merge / W05 intake | `391a69aa351bef4ec00b580d97e3e87e6f2df10d` |
| Review branch | `phase1/p1-w05` |
| W05 delivery | Twelve-path developer guard/test candidate; 42 local tests passed; submitted for review |
| Owner W05 acceptance / merge | Pending |
| W06 and later work | Not executed or authorized by this delivery |

## 1. Predecessor delivery closed

The owner-approved one-time importer ran successfully on the isolated transport branch. Run `35330401864`, attempt 1, job `105553187836`, used Ubuntu 24.04.5 and CPython 3.12.3. Its logs were read through the connector. All fifteen accepted W04 candidate files were imported with their exact original bytes, and the existing 29 static fixture checks passed with no failures, errors or skips.

The importer independently checked complete stored bytes of all eighteen specifications, corrected approval and Phase 1 plan before and after tests. It created `38d16d713bda963a53bd131d171e02bc90602e41`; the progress-only successor recorded those results without changing tested data. PR #5 was inspected and merged using expected-head protection at 2026-09-18T09:41:58Z, producing the intake commit above. The connector subsequently confirmed merged=true.

The temporary workflow was never included in main or the W05 branch. It was removed from `transport/p1-w04` after successful delivery at commit `072990829fb28e25522d05e1985222549c5a28c5`. Its historical source and run remain inspectable, but the current transport branch no longer contains the importer. No repository settings, secrets or general CI permissions were changed.

Complete W04 history remains in PR #5 and progress revision 0.8 at its accepted head. Earlier failed transfer attempts, the accepted local ZIP, and the progress-only gate record at `89b313a` remain historical facts. They are not overwritten with a claim that transfer had succeeded earlier.

## 2. Exact W05 scope

Only these twelve plan-section-9 paths are created or updated:

```text
tools/check_phase0_baseline.py
tools/check_scaffold_boundary.py
tests/scaffold/test_baseline_integrity.py
tests/scaffold/test_no_runtime_implementation.py
tests/scaffold/test_layer_boundaries.py
tests/security/test_scaffold_inertness.py
tests/security/test_scaffold_no_native_loading.py
tests/security/test_scaffold_no_network.py
tests/integration/README.md
tests/unit/README.md
tests/contract/README.md
PHASE_1_PROGRESS.md
```

The two tools are repository-only developer commands. They are not imported by the installed auditor, do not accept evidence dossiers and do not implement runtime parsing, source analysis, native filesystem publication or report generation. No package, dependency, packaging rule, earlier test, catalog, fixture, logical oracle or frozen file is modified.

## 3. Guard design and independent controls

The baseline checker pins the accepted W01 manifest object independently, checks its closed eighteen-file contract, then compares complete stored bytes, SHA-256 and Git object identities, including the separately protected approval and plan. Editing a source and its manifest together cannot authorize a new freeze. Missing or altered bytes fail; there is no repair, network fetch, partial-pass or rehash-and-accept mode. Its ordinary CLI has no test-anchor override.

The package checker independently enumerates all 48 accepted W02 paths and their Git blobs. It separately checks executable AST forms, import targets, software-layer direction and dependency cycles. Hash matching is not the only test: the AST and layer routines receive deliberately wrong source strings directly, with no accepted-byte check to mask their behavior. An otherwise permissible layer import still fails the inert-body contract. Extra code, native/data files, mutable registries, side-effecting annotations/defaults/decorators, argument inspection and fake successful audit results are rejected.

The subprocess harness imports all 48 real byte-matched slots and exercises four API refusal calls plus CLI help/version/refusal. Synthetic input/output canaries are checked before and after. The harness preloads its own standard libraries, then distinguishes Python module-loader reads from application-originated file/path/native/network effects. Deliberate socket/DNS/native-library probes are intercepted before executing those operations. Even a module that catches an interception exception leaves a recorded violation and cannot turn the probe into a pass.

All deliberate mutations live in temporary copies. No mutated source, private evidence or paper PDF enters the actual package or repository. These finite checks are not a production sandbox or a complete security proof.

## 4. Actual W05 execution

The six new test files ran locally with Python standard-library unittest, CPython 3.13.5, Linux x86_64 and glibc 2.41. The selected combined run reported:

```text
Ran 42 tests in 13.035s
OK
```

There were zero failures, zero errors and zero skipped tests in that final run. The counts are:

| New test surface | Test methods |
|---|---:|
| Baseline guard controls | 11 |
| Package inventory and non-implementation controls | 12 |
| Software layer controls | 7 |
| Inertness, filesystem and argument probes | 6 |
| Application native-binding probes | 3 |
| Application network probes | 3 |
| Total | 42 |

Per-file commands are recorded in tests/contract/README.md. The actual package checker also passed its complete 48-module CLI invocation. Its tests execute both positive and negative CLI cases under Python -O; guard enforcement does not disappear when assert statements would be optimized away.

### Evidence scope

The local W05 view contains all 48 accepted package files as independently byte-matched copies, the exact W01 manifest, eleven complete original specification files and the accepted W04 artifacts. The 48 package blobs all matched before testing and were not modified. Eleven available full specification files were rehashed against their approved values; newer full specification/approval/plan files were not reconstructed in this local view.

The baseline unit tests therefore explicitly distinguish a synthetic full twenty-file workspace, real manifest-anchor validation and a complete actual reference-document check. The synthetic fixture changes only the test process's trust anchor; it does not change the production developer command or the real repository manifest. These are positive/adverse tests of guard logic, not a claim that synthetic strings are the approved baseline.

A new full-checkout invocation of tools/check_phase0_baseline.py over all twenty actual files was not executed locally in W05. The complete actual-byte baseline evidence comes from the successful W04 hosted importer; remote object/diff preservation connects that unchanged baseline to W05. Full-checkout execution of the new command and the combined suite remains an explicit P1-W06 CI duty. The absence of that later run is not hidden as a skipped test or relabeled as a local pass.

No selected setuptools/pytest installation, W02 packaging rerun, W03 full-suite rerun, Windows/CPython 3.11 run, W05 hosted workflow or package publication occurred in this unit. Earlier passing runs retain their own checked commits and scopes. The 42 methods do not satisfy the 228 pending analytical obligations.

### Corrected test-harness defect

The first security-harness run failed all twelve security methods before completing any package import. Stack inspection via sys._getframe generated another audit event, recursively re-entering the observer. The observer was corrected to filter to monitored operations before stack inspection. The final unchanged positive and adverse assertions then all passed. No product code, approved expectation or source contract was changed to obtain the pass; no failing test was skipped. The raw initial failure log is retained with the local verification artifacts.

## 5. Preservation and handoff

Remote final tree and PR checks must confirm exactly eleven additions plus this progress update relative to the actual W04 merge. All twelve outgoing file identities are compared with the tested/reviewed local bytes. Final commit/PR identifiers belong in the PR handoff after they exist, avoiding a document that tries to contain its own hash.

The eighteen frozen specifications, corrected approval, Phase 1 plan, baseline manifest, accepted catalogs, 48 product modules, W04 fixture/oracle files, license notices, development pins and existing W02 workflow remain unchanged. The earlier broad scientific and theoretical material is not reinterpreted in W05.

Submit the W05 review PR and stop for owner acceptance. Do not merge W05, change the CI workflow, execute W06 or begin Phase 2 automatically. On the next authorized step, W06 must run the complete checkout, new developer guards and accumulated suite on its reviewed interpreter/platform matrix and preserve any actual failures.
