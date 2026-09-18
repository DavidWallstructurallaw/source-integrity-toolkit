# PHASE_1_PROGRESS

## Current control record

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Progress revision | 0.7 local candidate |
| Date | 2026-09-18 |
| Approved plan | PHASE_1_PLAN.md revision 0.1; Git blob `27ed33cb1c2afc78b12ca099ee7ccb4e68d63bfb` |
| Owner instruction | `批准并合并 PR #4，再进入 P1-W04` |
| Accepted predecessor | P1-W03, head `bad936b4e224857e6073720afebe83fc7df9eb64` |
| Verified PR #4 merge | `bfac2e69dd653823201a16069615cc9044a4b39c`; merged at 2026-09-18T07:22:10Z |
| P1-W04 intake | `bfac2e69dd653823201a16069615cc9044a4b39c` |
| Existing review branch | `phase1/p1-w04`, observed at the intake commit |
| Local work | Four full static inputs, four logical oracles, indexes, manifest, documentation and tests prepared |
| Static test result | 29 passed; 0 failures; 0 errors; 0 skipped |
| Remote delivery | NOT SUBMITTED in this execution; write capability unavailable |
| P1-W04 completion / owner acceptance | Pending remote delivery and review |
| P1-W05 and later | Not started |

## 1. Accepted predecessor and authority

The owner accepted P1-W03 and requested merge of PR #4 followed by P1-W04. The first connected read in this execution found PR #4 already closed and merged, with the expected W03 head. A separate main-ref read confirmed the merge commit above. This execution verifies the existing merge rather than claiming to have issued a second merge.

The existing `phase1/p1-w04` branch was also found at that merge commit. No branch replacement, force push or history rewrite is authorized or performed.

The complete W03 progress remains in `PHASE_1_PROGRESS.md` at commit `bad936b4e224857e6073720afebe83fc7df9eb64`, Git blob `c407cb1e3d6eafadd6e510228260311000586dbb`. Its 19 static tests and the earlier W02 hosted runs remain historical evidence with their original scope. They are not W04 execution results.

## 2. P1-W04 closed file scope

The local candidate contains exactly the fifteen paths permitted by plan section 8, consisting of fourteen new files and this updated progress file:

```text
tests/fixtures/README.md
tests/fixtures/hero/H7-01.bundle.json
tests/fixtures/hero/H7-V01.bundle.json
tests/fixtures/hero/H7-V02.bundle.json
tests/fixtures/hero/H7-V03.bundle.json
tests/fixtures/hero/fixture_manifest.json
tests/fixtures/micro/case_index.json
tests/fixtures/adversarial/case_index.json
tests/golden/README.md
tests/golden/H7-01.logical.json
tests/golden/H7-V01.logical.json
tests/golden/H7-V02.logical.json
tests/golden/H7-V03.logical.json
tests/scaffold/test_fixture_integrity.py
PHASE_1_PROGRESS.md
```

One-off authoring utilities, logs and local verification JSON live outside this delivery. No authoring generator is proposed as a repository or runtime addition. Local copies of four frozen specifications are test inputs, not outgoing modifications.

## 3. Static input and oracle contents

The four input files are independent complete snapshots. The main fixture has 78 records, 50 assertions and eight supporting references. V01 retains that complete object inventory and changes only the snapshot identity and two seed lists. V02 has 82 records, 52 assertions and nine references; V03 has 81 records, 52 assertions and nine references.

Only the prescribed source populations change. Every variant preserves the six-member pipeline cohorts, four correction targets and independently scoped O1/O2 comparison. V02's unknown object is the upstream EvidenceItem UX, while Artifact U is present. Its old complete acquisition subview has an explicit coverage assertion. V03's two recorded parents have no numerical allocation.

The main and five-seed logical HHI expectations retain 26/36 and 25/25 respectively. The two seven-seed cases require unavailable full-population HHI with their distinct causes. The files preserve the source scope, origin and immediate-layer partitions, exact fractions and intervals, supplied independence limitations, partial model history, native handling, three linked changes and E's missing change evidence. No temperature-truth conclusion or successful-correction rate is added.

The 28 W7 micro-case index entries point to complete frozen sections, with full source and section hashes. The adverse/control index retains 24 W9 cases, six licensing cases and 32 W11 cases. Its existing W03 control-case bindings and WU11 refinements are preserved; no unassigned W9 test filename is invented.

The fixtures README records conservative prose-expansion choices. Descriptions of the amended Artifacts use their existing CORR-bound provenance qualifications rather than adding an unsupported Artifact data key. The eight original supporting excerpts remain exact copies. Newly materialized variant supplements express only the parentage/coverage facts already prescribed in lineage section 28.1.

## 4. Source verification and actual tests

The complete local lineage, validation, reporting and definitions files were hashed and matched to the current connected Git blob identities. Those bytes came from preserved original deliveries. The approved plan, PR state, main and review-branch refs, current progress and the W03 control-case catalog were read through the connector at the intake snapshot.

Actual local command:

```text
PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests/scaffold -p test_fixture_integrity.py -v
```

Environment: CPython 3.13.5, Linux x86_64, glibc 2.41. The final new file ran 29 test methods, with no failures, errors or skips. The checks include eight deliberately damaged in-memory fixture/oracle probes and a separate duplicate-JSON-key probe. They exercise direct-reference integrity, exact original support text, original acquisition-table transcription, variant preservation, all pipeline native states, correction identities, source-scoped fractions/non-results and full-section pointers.

The first 27-method run passed its checks. Manual source review then found an overly abbreviated `unresolved` label in the V02 test-only immediate disposition. It was corrected to the adopted `unresolved_at_evidence_layer`, and two tests were added for exact disposition vocabulary and the source-table witness transcription. The final 29-method run passed. No frozen source or expected substantive result changed.

These tests read fixed repository test assets and inspect direct references. They do not construct or traverse a source graph, qualify independence, compute HHI, classify observability, serialize a toolkit report or invoke native operations. No analytical obligation is promoted from pending to passed.

No W02/W03 full-suite rerun, fresh selected-toolchain installation, package build, hosted W04 CI, Windows run or native-security test is claimed. No private evidence or source-paper PDF is used as test data.

## 5. Remote-delivery blocker

The GitHub tools exposed in this execution support reads but do not expose file creation/update, Git object/ref writes or PR creation. Plugin discovery confirmed the existing GitHub integration, with no alternative available write action. The local CLI does not have `gh`; an ordinary Git clone failed because github.com could not be resolved. No credentials were requested, inspected or transferred.

Therefore the local candidate is preserved without claiming a remote commit, push, PR number or completed W04 delivery. The repository's underlying account permission is not inferred from the available action set. This is a limitation of this execution path, not a new project dependency or an authorization to weaken the workflow.

No existing repository file was written by this execution. The local candidate must later be checked against the actual remote branch head before any authorized submission. A changed base requires reconciliation instead of overwriting it.

## 6. Remaining gate

The local candidate is ready for remote delivery review. The remaining tasks are to submit the fifteen permitted paths to the existing review branch, verify exact outgoing blobs and the allowed diff, and create an unmerged review PR. No remote submission or automatic future work is promised by this record.

P1-W04 owner acceptance and merge remain separate. P1-W05 must not start until this delivery has actually been submitted and accepted. The Phase 0 baseline, approval, Phase 1 plan, package code, earlier catalogs, packaging configuration, tool pins, LICENSE, NOTICE and workflows remain outside this unit's outgoing scope.
