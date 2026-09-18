# PHASE_1_PROGRESS

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Progress revision | 0.2 |
| Record date | 2026-09-17 |
| Approved Phase 1 plan | Revision 0.1 at `2fa58fce603e28f1160bd68eeadbe315db941501` |
| Plan Git blob | `27ed33cb1c2afc78b12ca099ee7ccb4e68d63bfb` |
| Plan approval and initial execution instruction | `批准，开始 P1-W01` |
| Scoped repair and continuation instruction | `批准，继续`, following the approval-manifest repair request |
| Current work unit | P1-W01: Freeze verification, project governance and license application |
| Execution intake commit | `2fa58fce603e28f1160bd68eeadbe315db941501` |
| Approved Phase 0 candidate | `7d2e5fcaff591641b5cefce00e71e88941dd1f95` |
| Original approval-record commit | `6650984502637bb167c38e7e370c46e246591480` |
| Corrected approval-record commit | `f84c58cf6ca93b57020fd9b271de4c33e1bf1ebd` |
| Reviewed pre-progress candidate | `4a998023ec3a4a87702b023481b14ba48366435f` |
| Review branch / pull request | `phase1/p1-w01` / PR #2 |
| Current disposition | P1-W01 artifacts completed and checked; submitted for owner review |
| Owner acceptance of this delivery / merge | Pending |
| P1-W02 and later units | Not started |

## 1. Authority and immutable failed-gate history

The original instruction approved PHASE_1_PLAN.md and authorized P1-W01. Its historical PROPOSED header remains unchanged. The first attempt stopped at the required freeze check and recorded four malformed approval-manifest digests. That complete entry-hold record is preserved at:

`https://github.com/DavidWallstructurallaw/source-integrity-toolkit/blob/6e37659bdf345484babc4eb37ef7b547980998d1/PHASE_1_PROGRESS.md`

Its blob is `3c4ddf4f6e1a5c313c83a3246e32732fecf4029e`. This revision preserves the failed-gate event by that immutable reference. It does not claim that the first check passed or erase the earlier limitation that only eleven files had then been independently rehashed.

The owner subsequently approved the proposed narrow repair with `批准，继续`. That authorizes correcting erroneous digest/revision-history metadata in PHASE_0_APPROVAL.md, after recomputing all eighteen entries, then resuming the existing W01 allowlist. It does not authorize changing any underlying specification, the approved design or PHASE_1_PLAN.md.

## 2. P1-W01-B01 resolved: complete manifest recomputation

All eighteen complete file byte sequences were matched against the approved commit's Git blob identities and byte counts. Local SHA-256 calculations with hashlib were independently cross-checked using sha256sum. There was no checkout normalization, missing-character guess or substitution of Git SHA-1 for file SHA-256.

The eleven previously checked entries matched. Full verification found seven erroneous values in the approval record: the four previously reported 63-character entries plus three 64-character mismatches for DEPENDENCY_STRATEGY.md, GOVERNANCE_AND_HANDOFF.md and LICENSING_NOTES.md. Those are approval-record defects; the corresponding specification blobs still match the approved candidate.

The authorized repair changed only the approval record's revision to 1.1, the seven incorrect table values and a correction-history section. All eighteen specification paths and byte counts, their 1,094,920-byte total, the approved commit and the original semantic approval remain unchanged. Original revision 1.0 remains available in Git. The earlier assertion of a fully checked manifest is explicitly corrected rather than retroactively treated as true.

| Corrected approval identity | Value |
|---|---|
| Commit | `f84c58cf6ca93b57020fd9b271de4c33e1bf1ebd` |
| Bytes | 14670 |
| Git blob SHA-1 | `3e61806e3df5afc7d88fae27db765c5e5eb4bdb9` |
| File SHA-256 | `92915c24758dc8cbcdfb075c15361b2beedad469fe69b821a5e13003a4804a9c` |

The remote updated blob equals the complete locally checked outgoing document. Its manifest contains exactly eighteen valid 64-character digests, each equal to the recomputed value. The entry blocker is resolved within the approved repair scope. The machine-readable manifest records the approval hash separately from the eighteen-file baseline and keeps the original and correction commits distinct.

## 3. W01 artifacts delivered

| Path | Delivery |
|---|---|
| `README.md` | Public purpose, accurate nonfunctional scaffold status, roadmap and license/data exclusions |
| `LICENSE` | Unmodified official Apache License 2.0 text, including appendix |
| `NOTICE` | Project attribution and material-scope information; no extra license condition |
| `CONTRIBUTING.md` | Scoped changes, frozen-byte discipline, evidence and contribution-rights rules |
| `SECURITY.md` | Present support limit, verified public Issues route and unverified private-intake limitation |
| `.gitignore` | Local environments, artifacts and private runtime folders; specifications/tests remain visible |
| `.gitattributes` | Explicit byte-preservation entries for eighteen specifications, approval and Phase 1 plan; new text uses LF |
| `scaffold/baseline_manifest.json` | Eighteen-file byte/SHA-256 manifest, corrected approval identity and approved-plan reference |
| `scaffold/toolchain_review.md` | Exact proposed build/test pins, published compatibility, dependency/license implications and evidence limits |
| `PHASE_1_PROGRESS.md` | This authorization, repair, check and handoff record |

`PHASE_0_APPROVAL.md` is the sole additional changed path, authorized by the narrow repair. No other frozen document or Phase 1 plan byte changed. The original licensing notes remain historical; the root license now applies the previously approved engineering-material policy.

## 4. Checks actually performed

The checking workspace used CPython 3.13.5, Linux x86_64 with glibc 2.41, and Git 2.47.3. These identify the authoring environment, not a supported or tested toolkit release. General-purpose local verification scripts were kept outside the repository delivery.

| Check group | Result and scope |
|---|---|
| Exact baseline bytes | PASS: eighteen full files matched approved Git blobs/lengths; hashlib and sha256sum agree |
| Approval correction scope | PASS: removing the correction section and reversing the seven values/revision reproduces original sections 1-8 exactly |
| Machine-readable manifest | PASS: eighteen rows equal the corrected authoritative table; separate approval digest/bytes/blob verified; no self-hash |
| Official license source | PASS: all 11,358 bytes equal Apache website source blob `d645695673349e3947e8e5ae42332d0ac3164cd7` |
| Allowlist and text integrity | PASS: only the ten W01 paths and authorized approval amendment; new text is UTF-8/LF |
| Protected-path attributes | PASS: twenty explicit path settings checked; all nineteen available complete specification/approval files preserve their blobs under core.autocrlf true and false; approved-plan path settings also checked |
| New-text normalization | PASS: a CRLF README probe produces the intended LF Git content |
| Ignore boundaries | PASS: fourteen local/private-output probes ignored; thirty specification/test/catalog/public/example probes remain visible |
| Public-document consistency | PASS: local references, license exclusions, unimplemented status and security limitations reviewed |
| Remote delivery comparison | PASS at the named pre-progress candidate: all ten outgoing non-progress files match their checked local blobs and lengths; original eighteen specs and approved plan unchanged |

These are authoring, manifest, Git-attribute and documentation checks. They do not implement or test the auditor. No parser, graph algorithm, metric, native file adapter, package skeleton, executable schema, fixture or CI workflow was created. No dependency install, resolver execution, package build, hosted CI run, penetration test or independent review is claimed. The 228 domain field obligations remain unexecuted.

## 5. Toolchain and security handoff

The proposed direct pins are setuptools 84.0.0 for building and pytest 9.1.1 for tests. Published metadata for both admits Python 3.10+, including the project's 3.11 target. Their project licenses were read from versioned sources. The review records pytest's conditional dependencies and the presence of setuptools vendored components without claiming a resolved dependency lock or complete artifact clearance.

P1-W02 must inspect actual installed/resolved versions and licenses, test compatibility, and recheck the recorded upstream archive-extraction safety note before installation. No optional tool, extra build frontend or product runtime dependency is added now.

Issues are available as a public route. The attempted private-reporting status check did not establish a supported confidential channel. SECURITY.md discloses that limitation and requests only a non-sensitive contact request on the public tracker. No private reporting feature, security email, key or response SLA was invented or configured.

## 6. Remote workflow and next stop

The existing PR is:

`https://github.com/DavidWallstructurallaw/source-integrity-toolkit/pull/2`

The pre-progress candidate contains the corrected approval and all nine other W01 artifacts. Its diff against intake has exactly eleven paths, including this progress record already present from the entry hold. This final progress update and PR metadata are verified after their writes; the final candidate commit belongs in the PR/handoff rather than as a self-referential value in this document.

The branch is submitted for owner review. Main has not been changed by this unit, and no merge or P1-W02 execution is claimed. The next step is acceptance and merge of this W01 delivery, followed by explicit authorization of P1-W02 under the unchanged plan.
