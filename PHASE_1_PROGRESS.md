# PHASE_1_PROGRESS

## Current control record

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Progress revision | 0.7 |
| Record date | 2026-09-18 UTC |
| Approved plan | PHASE_1_PLAN.md revision 0.1; blob 27ed33cb1c2afc78b12ca099ee7ccb4e68d63bfb |
| Current owner instruction | `可以，继续P1-W05` |
| Accepted repository predecessor | P1-W03, PR #4, merged at bfac2e69dd653823201a16069615cc9044a4b39c |
| Accepted local successor | The previously delivered P1-W04 fifteen-path candidate, identified below |
| W04 remote delivery | Pending; this commit records the intake only |
| W05 authorization | Granted by the current owner instruction |
| W05 execution | Held at the predecessor repository-delivery gate; no W05 implementation or test result claimed |
| Current review branch | phase1/p1-w04 |
| W06 and later | Not authorized or executed |

## 1. Preserved history

The complete accepted W03 progress record remains at bfac2e69dd653823201a16069615cc9044a4b39c:PHASE_1_PROGRESS.md, blob c407cb1e3d6eafadd6e510228260311000586dbb. Its original candidate and test evidence remain in PR #4 and commit bad936b4e224857e6073720afebe83fc7df9eb64. The W02 hosted verification remains separate evidence and is not a W04 or W05 run.

The current owner continuation accepts the submitted W04 local candidate and requests W05. Acceptance of the local material does not assert that its remote commit, PR or merge has occurred. At this intake, both main and phase1/p1-w04 still pointed to bfac2e69dd653823201a16069615cc9044a4b39c, before this progress-only update.

## 2. Exact accepted local W04 candidate

Artifact: Source_Integrity_Toolkit_P1_W04_Local_Candidate.zip.

ZIP size: 87,385 bytes.

ZIP SHA-256: a74a1e661d103e58b820bd976f9ebf2827faed6e6038686cd02a4a89a3cf80fd.

The archive contains exactly the fifteen paths in PHASE_1_PLAN.md section 8, totaling 877,728 uncompressed bytes. Fourteen paths are additions and PHASE_1_PROGRESS.md is an update. The separate P1_W04_VERIFICATION.json records each complete file's byte count, SHA-256 and Git blob identity.

At this intake the archive hash, exact entry set and all fifteen file identities were recomputed and matched to that prior verification record. Four complete local source documents were also rehashed: CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md, DEFINITIONS_AND_UNITS.md, OBSERVABILITY_AND_REPORTING.md and VALIDATION_PLAN.md. Each matched the recorded approved source bytes. No fixture or logical expectation was edited.

The unchanged test_fixture_integrity.py was rerun in a controlled local view of those exact files with Python's standard-library unittest. Result: 29 tests passed, zero failures, zero errors and zero skipped; 0.122 seconds reported by unittest. This is a W04 static-transcription recheck. It is not a W05 boundary test, hosted CI result, production audit or fresh full eighteen-document baseline run.

## 3. Repository-delivery gate

Current discovery does expose GitHub text/blob/tree/commit write actions. Do not repeat the earlier claim that this connection is read-only. However, it exposes no mounted-local-file upload argument for transferring this candidate directly. The local Git transport attempt failed because github.com could not be resolved. A lookup of the first candidate fixture's known blob returned not found; no remote fixture commit is assumed from the local hashes.

This update deliberately writes only the common progress record. It does not claim that the remaining fourteen candidate paths have been uploaded, or that an absent W04 PR has been merged. Main and the frozen specifications remain untouched.

A proposed transfer exception, P1-W04-T01, would allow one temporary, narrowly scoped importer workflow on an isolated transport branch. Its sole purpose would be to materialize the already accepted fifteen files from an embedded losslessly compressed payload, verify every expected byte identity and path, rerun the existing static fixture checks, and commit to the existing W04 review branch using a guarded non-force update. The workflow would not be merged into main, publish a package, implement analytics, modify dependencies or alter frozen files. Contents-write permission would be limited to that explicitly authorized authoring operation.

That additional workflow path and permission are outside the current work-unit allowlists, so this transfer method remains a proposal until specifically authorized. No importer workflow or payload has been committed here.

## 4. Next gate

Complete and verify the accepted W04 repository delivery before representing W05 as based on a delivered predecessor. Then execute only the twelve paths in PHASE_1_PLAN.md section 9: the two developer guards, six scaffold/security tests, three test-surface reservation READMEs and this progress record.

The already granted W05 authorization remains recorded. No new theory, product, licensing or source-schema decision is requested by this gate. W05 acceptance, its review-branch merge and any W06 work remain separate later events.
