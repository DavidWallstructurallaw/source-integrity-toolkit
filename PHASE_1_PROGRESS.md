# PHASE_1_PROGRESS

## Current control record

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Revision | 0.15, P1-W07 final scaffold audit and handoff |
| Date | 2026-09-18 UTC |
| Owner instruction | `批准并合并 PR #7，然后进入 P1-W07` |
| Approved plan | Revision 0.1, blob `27ed33cb1c2afc78b12ca099ee7ccb4e68d63bfb` |
| Accepted main / W06 merge | `6d7f7e3f54bebf5f7f3b680988b10cee096ae8ba` |
| W07 audited precursor | `d00f4faeeed414b1729bc2e5643af5b65737093a` |
| Inspected W07 run | `35384829099`, attempt 1 |
| Branch / PR | `phase1/p1-w07`, PR #8 |
| Current technical result | Precursor audit PASS; final record-set CI gate recorded separately in PR #8 |
| W07 owner acceptance / merge | Pending / not performed |
| Phase 2 | No plan, code or execution authorized |

## 1. Acceptance and merge actually performed

The current instruction accepted W06 and authorized PR #7's merger plus W07. The PR was re-read at `c24b9b6ccc5ce178f52f989f80dfde1cc26a7e39`; its exact-head run 35365621100 and four successful jobs were rechecked. Expected-head-protected merge returned `6d7f7e3f54bebf5f7f3b680988b10cee096ae8ba`. The merge tree equals the accepted W06 tree `d231330752a888048559a7be5b5deb11bc5827f8`.

The complete W06/R02 progress revision 0.14 remains at that merge and at `c24b9b6ccc5ce178f52f989f80dfde1cc26a7e39`, this path. Revision 0.13 at `c6d8969d8b82d86900fbd36c6d657538f47af35a` preserves the R01 evidence and R02 proposal before approval. These histories retain the initial failures and the exact permissions for each repair. This successor does not relabel them as passing.

## 2. W07 closed file scope

Only PHASE_1_COMPLETION.md, PHASE_1_PROGRESS.md, scaffold/delivery_manifest.json and README.md are authorized by plan section 11. The precursor updates README only. Its tested tree is `9b645fd7cc3a13d5661a80138f23381fd02b4822`. The final record-set successor adds completion and delivery manifest, updates this progress record and changes no manifested byte.

No product module, prior test, dependency pin, package selection, workflow, license, catalog, input/oracle, baseline manifest, frozen specification, approval or Phase 1 plan is edited. No tests or skip markers are added. All new metadata is delivery/governance material outside the runtime.

## 3. Scope audit and acceptance chain

PRs #2-#7 were read and their full changed-path lists checked against the plan plus explicit exceptions. Counts are 11, 58, 9, 15, 12 and 8. Their union and the twenty pre-scaffold paths account for all 122 accepted files, with no missing or unexpected path. The temporary W04 importer is absent. The old draft PR #1 remains unmerged history, superseded for acceptance by PR #2; no cleanup mutation was performed.

The accepted heads, merge commits and original local/hosted test scopes are tabulated in PHASE_1_COMPLETION.md section 2. W05's documented lack of a local twenty-actual-file check is closed by the later W06 and current W07 hosted full-checkout executions, not backdated to W05.

## 4. Actual W07 precursor results

Run 35384829099, attempt 1, checks exactly d00f4faeeed414b1729bc2e5643af5b65737093a. All four jobs succeed. Each collects and passes the same 194 top-level instances as W06, with zero failures, errors or skips and 420 separately counted successful subtest events. The four environments are Ubuntu 24.04 x64 with CPython 3.11.16 and 3.13.15, and Windows Server 2025 x64 with CPython 3.11.9 and 3.13.15. Image versions remain 20260907.300.1 and 20260907.229.1 respectively.

Both actual twenty-file baseline and forty-eight-module guards pass before and after. Tracked bytes remain unchanged during tests; all four tracked maps are identical and differ from W06 only in README. Pinned developer-wheel review/install, all fourteen test files, exact source/wheel inventories, clean offline installation and source-rebuild wheel member-byte equality pass. The source archive includes its four approved original scaffold tests; the wheel includes no tests or logical expectations. Counts remain 65 regular sdist members and 55 wheel members.

All four evidence ZIPs were downloaded and matched to Actions byte counts and SHA-256 values. Local inspection independently matches collection IDs to 194 JUnit elements, checks the aggregate/subtest distinction, all zero error/failure/skip counts, pytest exit, guard logs, tracked hashes, installed versions and archive members. Artifact IDs, hashes and job IDs are retained in completion section 6. Source locators and real evidence were not used.

A direct local Git clone failed DNS resolution. No local full-checkout test run is claimed. Local evidence verification initially used an overbroad assertion excluding every test from the sdist. The accepted MANIFEST.in expressly includes four original tests; the supplemental checker was corrected to compare the complete accepted inventory. That authoring-check error altered no repository file or hosted test, and is retained in the local verification notes.

## 5. Manifest and final delivery evidence

The delivery manifest pins the exact d00f4fa precursor and 121 complete-file SHA-256 values, excluding itself and the completion/progress records. Its local bytes match created Git blob `706db89ddb69fb8f0c8db80f27b4128c50afab54`; its own SHA-256 is `c354ec51acbe4ad90cb2f15037b3a3d043eec21e39cd348d8b5ecb2afae3fc5a`. The final record-set contains 124 tracked files. This is a predecessor manifest with an explicit boundary, not a self-hashing claim.

The final record-set commit must receive its own four-row CI rerun. Its actual commit/run/artifact pairing and four-path diff are recorded in PR #8 after creation and inspection, rather than trying to embed this file's future commit inside itself. The final downloaded tracked map must match all 121 manifest entries and introduce only the two planned new files plus the updated progress. Prior green results do not waive that gate.

## 6. Historical failures and remaining boundary

The W01 digest errors, W02 local tool-version mismatch and W04 transport delay retain their accepted repair/verification records. W06 runs 35357942013, 35358820107, 35362756160 and 35363039474 retain their original failures. R02 runs 35365045308 and 35365621100 retain the actual passing repairs. No failing test was dropped, no product boundary relaxed and no source oracle rewritten.

The 228 domain obligations remain pending. Passing static catalogs/fixtures, imports, package inspection and scaffold probes does not implement parsing, qualification, source graphs, HHI, correction, report serialization, resource enforcement or native adapters. SECURITY.md's private-reporting limitation and the prior dependency/security applicability qualifications remain visible.

## 7. Stop

W07 ends after submitting PHASE_1_COMPLETION.md and its final checked review package for owner acceptance. Main remains at the accepted W06 merge unless a later owner instruction authorizes PR #8. No Phase 2 plan, release, deployment, source-paper update or cross-project integration is created.
