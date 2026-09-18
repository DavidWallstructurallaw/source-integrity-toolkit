# Scaffold Toolchain Review

## Current record

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Review revision | 0.4 |
| Date | 2026-09-17 project-local; run timestamps are UTC |
| Work unit | P1-W02 with scoped exception P1-W02-A01 |
| Selected and actually installed direct pins | setuptools 84.0.0; pytest 9.1.1 |
| Hosted gate | PASSED at `a5000f5a65ae094d7c6762a9fe8557ffa0ba1928` |
| Product runtime dependencies | None |
| Owner acceptance / merge | Pending |

## 1. Preserved review chain

Revision 0.2 remains at commit `1126eff7d98023b9bc835dc00026ea5629f64a77`, this path. It preserves W01 sources, the original artifact/permission assessment, the failed local download, the older-tool supplemental checks and the strict failed version assertion. Revision 0.3 at `a5000f5a65ae094d7c6762a9fe8557ffa0ba1928` records the owner-authorized early workflow, reviewed action identities and pre-execution limits.

This revision adds the observed hosted result. It does not rewrite the historical local failure, change requirements-dev.txt, or substitute a metadata-only compatibility statement for executed tests.

## 2. Actual resolved Linux environment

GitHub Actions run `35307307901`, attempt 1, job `105482030736`, completed successfully on Ubuntu 24.04.5/x86_64 with CPython 3.13.15 and glibc 2.39. The bootstrap installer was pip 26.2.1. It was supplied through the selected Python/venv environment, not introduced as a product dependency or new build frontend.

The job downloaded the following exact wheels from PyPI, read their metadata and notice material, verified complete-byte digests and sizes against the exact-release records, then installed offline into a fresh venv. pip check succeeded. The direct-tool hashes also matched those previously recorded before download.

| Distribution | Version | Wheel bytes | Observed SHA-256 |
|---|---|---:|---|
| setuptools | 84.0.0 | 818216 | `51a52592b3b99e102b609654876bd65f19f999935166d1352678931132b0c670` |
| pytest | 9.1.1 | 386536 | `37a86b45efb9a47a61a36449063e8e18d0cab3161329fc099eb21783169c4f0c` |
| iniconfig | 2.3.0 | 7484 | `f631c04d2c48c52b84d0d0549c99ff3859c98df65b3101406327ecc7d53fbf12` |
| packaging | 25.0 | 66469 | `29572ef2b1f17581046b3a2227d5c611fb25ec70ca1ba8554b24b0e69331a484` |
| pluggy | 1.6.0 | 20538 | `e920276dd6813095e9377c0bc5566d94c932c33b27a3e3945d8389c374dd4746` |
| Pygments | 2.20.0 | 1231151 | `81a9e26dd42fd28a23a2d169d86d7ac03b46e2f8b59ed4698fb4785f946d0176` |

All six selected wheel records were non-yanked at the run. Colorama's existing Windows marker was inactive; that platform's resolution and tests remain later work. No extras, exceptiongroup/tomli for Python <3.11, graph library, HTTP client or model SDK entered the selected environment.

The full decoded job log and step summaries were read through the connector after completion. The actual downloaded-wheel review, included notice texts/hashes, install report, distribution list, JUnit file and build inventories are retained in Actions artifact `10532775110`, with archive SHA-256 `7bab6bd98fd2cea8f31dd59b782be36235e86fb1fcf4bd9b2030425cdaa00043`. This session checked the artifact metadata and log summaries; it did not separately download the evidence ZIP through the local offline runtime.

## 3. Rights and vendored-material interpretation

The downloaded root metadata identifies setuptools, pytest, iniconfig and pluggy as MIT, and Pygments as BSD-2-Clause. Packaging 25.0 has a null license string in this particular METADATA view; its reviewed license files supply the Apache-2.0/BSD alternatives. Null metadata is not treated as missing all permission or as a new Apache grant by this project.

The workflow's notice-candidate inventory is intentionally inclusive of license-named paths; its raw match count is not a count of distinct legal licenses. Exact member paths and hashes remain in the artifact for review. Upstream notice texts retain their own rights. Their collection is review evidence, not copied project implementation or a claim of comprehensive legal clearance.

Setuptools' actual wheel contains twelve vendored dist-info records: autocommand 2.2.2, backports.tarfile 1.2.0, importlib_metadata 8.7.1, jaraco.text 4.0.0, jaraco.context 6.1.0, jaraco.functools 4.4.0, more-itertools 10.8.0, packaging 26.0, platformdirs 4.4.0, tomli 2.4.0, wheel 0.46.3 and zipp 3.23.0. These remain an upstream developer-tool surface even when not independently installed by pip. In particular, autocommand advertises LGPLv3; no claim that every vendored component is MIT is made.

No backend, vendor module or developer dependency is included in the toolkit's built wheel. Exact product-artifact inventories and the clean runtime installation passed. Redistributing an upstream build environment itself would require its own notice/rights assessment; this task publishes neither that environment nor those wheel binaries.

## 4. Scoped Actions dependencies and actual execution

P1-W02-A01 allows one dedicated workflow. The following official tags were resolved and their LICENSE files read at their pinned commits before submission.

| Action | Tag | Commit | Project license |
|---|---|---|---|
| actions/checkout | v4.4.0 | `11d5960a326750d5838078e36cf38b85af677262` | MIT |
| actions/setup-python | v7.0.0 | `5fda3b95a4ea91299a34e894583c3862153e4b97` | MIT |
| actions/upload-artifact | v7.0.1 | `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` | MIT |

The job log confirms those exact actions, checkout of the intended PR head, Contents:read/Metadata:read permissions and removal of checkout authentication before tests. No configured repository secrets were referenced. No cache input or action was configured. The runner's generic cache-service capability line is not evidence that this workflow stored a dependency cache.

The runner warned that checkout targets deprecated Node 20 and transparently ran it with Node 24. setup-python and upload-artifact declare Node 24 themselves. This execution passed without setting ACTIONS_ALLOW_USE_UNSECURE_NODE_VERSION or other security-weakening overrides. Broader future action-version maintenance belongs to the reviewed W06 setup.

No write-scoped token, pull_request_target, deployment, package publication, automatic merge, arbitrary ref parameter or self-hosted runner is used. The verification job admits only same-repository PR #3 from phase1/p1-w02. Only nine named-pattern verification records were uploaded for fourteen-day retention; no project package binary, arbitrary workspace, source-paper PDF or user dossier was uploaded.

## 5. Security applicability recheck

The primary setuptools history still identifies its archive_util traversal/UnsafeMember change as an unreleased draft dated September 8, 2026, referencing GHSA-grgh-hr87-3jpw. The separately linked advisory could not be retrieved during review. Its complete affected-version range and the presence of that fix in 84.0.0 are therefore not asserted.

The selected build protocol does not call archive_util on external archives. It uses binary-only developer wheels verified before installation, reviewed source and self-built archives whose regular relative members are inspected before copying. The known extraction concern is outside those operations. Retaining the selected pin follows that bounded applicability assessment; it does not certify a vulnerability-free backend. An expanded archive-input surface or a newly confirmed applicable flaw reopens the gate before that operation proceeds.

A successful networked CI setup does not add networking to the auditor. No source retrieval, native security adapter or analytical implementation was written. Tests and wheel inspection run only as authorized developer work.

## 6. Executed test/build result

All 78 existing W02 tests passed with the selected versions, with zero failures, errors or skips. The exact-version check remains present and unchanged. Source inventory (65 regular files), wheel inventory (55 members), fictional exclusions, metadata/license checks, immediate API/CLI refusal, clean offline installation and source-rebuild member-byte equality all passed.

The clean runtime venv contained only source-integrity-toolkit. Setuptools and pytest were unnecessary there. The source and wheel binaries stayed temporary and were not published. ZIP container digests differed between initial/rebuilt wheels; their member bytes matched, which is the precise tested property.

The final documentation-only successor must retain the same workflow and test/source blobs and receive a current-head check before merge. Subsequent run identifiers are recorded in the PR conversation without a self-referential commit hash inside these documents.

## 7. Sources and evidence limits

Canonical run: `https://github.com/DavidWallstructurallaw/source-integrity-toolkit/actions/runs/35307307901`.

Primary reference sources: exact-release PyPI JSON records for each row in section 2; the official action tags, pinned action.yml and LICENSE files in section 4; GitHub workflow syntax, triggering-event and secure-use documentation; and `https://setuptools.pypa.io/en/latest/history.html`. Full earlier source tables remain in the pinned review history.

The actual run resolves W02's Linux selected-toolchain gate. It does not establish Windows or CPython 3.11 test results, future-version compatibility, independent scientific review, full supply-chain certification, production security, working audit functionality or final Phase 1 completion. PR #3 still requires owner acceptance and merge authorization.
