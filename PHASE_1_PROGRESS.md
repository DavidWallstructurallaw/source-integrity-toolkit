# PHASE_1_PROGRESS

## Current control record

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Progress revision | 0.8 |
| Record date | 2026-09-18 UTC |
| Approved plan | PHASE_1_PLAN.md revision 0.1; blob `27ed33cb1c2afc78b12ca099ee7ccb4e68d63bfb` |
| W04 intake main | `bfac2e69dd653823201a16069615cc9044a4b39c` |
| Accepted candidate | Original fifteen-path W04 ZIP, SHA-256 `a74a1e661d103e58b820bd976f9ebf2827faed6e6038686cd02a4a89a3cf80fd` |
| Transport authority | P1-W04-T01, explicitly proposed and accepted with `可以，继续` |
| Imported candidate | `38d16d713bda963a53bd131d171e02bc90602e41` |
| Import tree | `c95c828d597194a3a0b81625d5b586c7f2a2df65` |
| Review branch | `phase1/p1-w04` |
| W04 technical result | Exact accepted bytes imported; hosted static checks passed |
| W04 acceptance and merge | Owner accepted the local candidate and authorized merge after verified import; merge result recorded separately once it exists |
| W05 authorization | Granted; start after actual W04 merge |
| W06 and later | Not authorized or executed |

## 1. Authority and preserved history

The owner first accepted the W04 local delivery through `可以，继续P1-W05`. The following handoff proposed P1-W04-T01: a temporary isolated importer, exact fifteen-path delivery, verification, W04 merge, then the already authorized W05. The current `可以，继续` accepts that specific proposal. This closes the transport authorization gate without changing source, fixture, licensing or product decisions.

Historical progress records remain in Git: W03 at `bfac2e69dd653823201a16069615cc9044a4b39c`, the delivery-gate intake at `89b313aed8223af95c4b1999802d0f5b379eeccb`, and the unchanged accepted local-candidate record at `38d16d713bda963a53bd131d171e02bc90602e41`. This successor corrects current status; it does not make those earlier pending states retroactively successful. W02's selected-toolchain run remains separate evidence.

## 2. Completed exact-byte transport

The ZIP contains exactly fifteen allowed paths and 877,728 uncompressed bytes. A lossless path-to-text representation was compressed and split into six content-addressed temporary Git blobs. They add no branch paths. The importer pins and checks every piece plus the complete compressed and decoded SHA-256 before materializing any candidate file.

The sole temporary branch path is `.github/workflows/p1-w04-import.yml` on `transport/p1-w04`, commit `4bcae12a8bb9d1bfef315b95b12c7ffebf10100d`. It is excluded from the W04 tree and must never be merged into main. Its authority is a fixed same-repository authoring operation, not part of the installed toolkit or general W06 CI.

The workflow uses a fixed checkout without persisted credentials, no dependencies, no package publication, and no merge action. The job has contents-write permission for the authorized import; it checks the exact main and W04 heads before and after its non-force ref update. The token is removed from the test subprocess environment. The old-head check makes another run refuse after this successful import rather than overwrite subsequent work.

All fifteen imported blobs matched the accepted local byte identities. The remote tree comparison against the guarded predecessor contained exactly those paths. Main remained at the W03 merge. Fourteen fixture, oracle, index, README and test files remain untouched by this progress-only successor.

## 3. Actual hosted evidence

Run `35330401864`, attempt 1, job `105553187836`, completed successfully at 2026-09-18T09:36:35Z. The job log and step results were read through the GitHub connector. It ran Ubuntu 24.04.5, CPython 3.12.3, Linux x86_64 and glibc 2.39.

Before import, the job verified the pinned baseline manifest and complete stored bytes of all eighteen specifications, the corrected approval record and the Phase 1 plan. It checked their byte counts, Git blobs and applicable SHA-256 entries. These checks ran again after the static tests to detect input changes.

The existing unchanged `tests/scaffold/test_fixture_integrity.py` ran with Python's standard-library unittest:

```text
python3 -m unittest discover -s tests/scaffold -p test_fixture_integrity.py -v
Ran 29 tests in 0.070s
OK
```

All twenty-nine methods passed, with zero failures, errors or skips. This is static transcription/reference/oracle verification, not a production audit or execution of the 228 future analytical obligations. No setuptools/pytest version check, W02 full-suite rerun, Windows run or W05 test is claimed here.

The successful import produced commit `38d16d713bda963a53bd131d171e02bc90602e41`, parent `89b313aed8223af95c4b1999802d0f5b379eeccb`. This progress-only successor records that already completed run. A new run on the successor is not claimed; tested input, oracle and test blobs are unchanged.

The runner forced the pinned checkout action's deprecated Node 20 target onto Node 24 and reported that warning. No insecure Node-version override was enabled. No broad platform or security certification follows from the successful transport.

## 4. Retained W04 scope

The delivery contains four static `sit-bundle/0.1` dossiers, four test-only logical expectation files, a fixture hash manifest, W7/W9/W11 case indexes, two READMEs and one static test file. They preserve the main 26/36 and V01 25/25 fractions, the distinct unknown and unallocated-multiparent reasons, unchanged pipeline/correction populations, and separate submission, handling and three linked changes.

The remote compare from W03 to the imported candidate lists fifteen changed paths, fourteen additions and this common progress file. No frozen specification, approval, Phase 1 plan, module, catalog, dependency, packaging rule, existing test, license or main-branch workflow changed. No live source, theory PDF, private evidence or runtime analytical behavior was introduced.

## 5. Handoff

Create and inspect the W04 review PR, verify its exact head and fifteen-path scope, then perform the already authorized merge preserving history. Record the returned merge identity before creating the W05 branch. Do not merge the transport branch or broaden its permissions.

W05 is limited to the twelve paths in plan section 9: two repository-only guards, six scaffold/security tests, three test-surface reservation READMEs and this progress record. W05 delivery and acceptance remain separate from W04's now-verified transport. W06 CI work remains outside this instruction.
