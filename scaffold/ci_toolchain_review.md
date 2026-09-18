# P1-W06 CI Toolchain Review

## Control record

| Field | Value |
|---|---|
| Revision | 0.1, execution candidate |
| Date | 2026-09-18 UTC |
| Owner instruction | `批准并合并 PR #6，然后进入 P1-W06` |
| Accepted W05 head | `6bf3ef93fd90471da709d6f90e598e9d84f95908` |
| Actual merge / W06 intake | `ecf4eb5126201a7c31250c6dae8cbe2c64f9066a` |
| Review branch | `phase1/p1-w06` |
| Scope | Five paths in PHASE_1_PLAN.md section 10 |
| Hosted execution | Pending; no matrix pass claimed by this version |
| Runtime dependencies / analytical implementation | None / absent |

## 1. Selected matrix

The four required combinations are Ubuntu 24.04 x64 and Windows Server 2025 x64, each with CPython 3.11 and 3.13. These are explicit standard hosted runner labels, not `latest` or self-hosted machines. The GitHub hosted-runner reference was checked on the review date and lists `ubuntu-24.04` and `windows-2025`. The Python Developer's Guide lists 3.11 as security-supported and 3.13 as bugfix-supported. The lower-bound and additional-minor selection remains inside the approved plan.

The workflow resolves the selected minor through setup-python with prereleases and check-latest disabled. Each run records the actual complete Python version, platform, runner image version, exact checked commit, matrix row and attempt. A floating runner image/minor selection is not a claim of immutable system images. Actual package and scaffold compatibility is an execution gate, not inferred solely from release metadata. Windows Server scaffold checks do not certify the future Windows 11/NTFS native profile.

Primary sources:

- `https://docs.github.com/en/actions/reference/runners/github-hosted-runners`
- `https://devguide.python.org/versions/`

## 2. Reviewed immutable action selection

Official repository tag refs, pinned `action.yml` and LICENSE files were read through the GitHub connector on 2026-09-18.

| Action | Release | Exact commit | Declared runtime | License |
|---|---|---|---|---|
| actions/checkout | v7.0.1 | `3d3c42e5aac5ba805825da76410c181273ba90b1` | node24 | MIT |
| actions/setup-python | v7.0.0 | `5fda3b95a4ea91299a34e894583c3862153e4b97` | node24 | MIT |
| actions/upload-artifact | v7.0.1 | `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` | node24 | MIT |

The pinned action.yml Git blobs are respectively `5b0524f730db83f9513c18ab31a6c086c7239076`, `df6c8235b476652b6402d31d92a2a89cdea74bb9`, and `7cb4d1e81db55320b41217e1a78a1a46e3d2baef`. License blobs are respectively `a67dca8b4f65d6bd351f6b1e333ce2cd84d843a5`, `a426ef259d6c5d705e9c1405075c3b318093c65e`, and `a67dca8b4f65d6bd351f6b1e333ce2cd84d843a5`.

Checkout v7.0.1 replaces the earlier dedicated W02 workflow's Node-20-targeted checkout for this new workflow only. No insecure Node override is set and the accepted W02 workflow is unchanged. The checkout manifest exposes exact-ref selection and disabled credential persistence. Setup-python exposes the chosen minor, x64 architecture and disabled prerelease selection without a dependency-cache setting. Upload-artifact exposes finite retention and hidden-file exclusion. This is a review of identity, declared interface, license and selected authority, not an audit of every bundled JavaScript dependency.

Canonical source pattern: `https://github.com/actions/<name>/blob/<exact-commit>/action.yml` and the corresponding LICENSE and `/git/ref/tags/<release>` records. GitHub's secure-use guidance supports full-commit action pinning and least-privilege tokens:

`https://docs.github.com/en/actions/reference/security/secure-use`

## 3. Existing Python development dependencies

The accepted requirements file remains unchanged, Git blob `e037242d849f827a6c968a0f97830610a1718138`. Setuptools 84.0.0, pytest 9.1.1, iniconfig 2.3.0, packaging 25.0, pluggy 1.6.0 and Pygments 2.20.0 are selected. Colorama 0.4.6 is already selected by its Windows-only marker; W06 does not introduce it as a new dependency.

The six Linux wheel identities and previous notice/vendored review remain in `scaffold/toolchain_review.md` at the intake commit. The new driver retains the previously pinned direct-wheel digests, downloads only wheels into a fresh tools environment, checks the exact allowed distribution/version set, checks each complete byte digest/size and non-yanked status against its PyPI release JSON, and inventories license/notice paths and vendored metadata before offline installation. A seventh Windows wheel must be Colorama 0.4.6. No additional dependency is silently accepted if the resolver asks for one.

The official release records checked during preparation include:

- `https://pypi.org/pypi/setuptools/84.0.0/json`
- `https://pypi.org/pypi/pytest/9.1.1/json`
- `https://pypi.org/pypi/colorama/0.4.6/json`

Colorama's record describes a BSD license and no non-stdlib requirements. Its use inside the developer runner is distinct from the tested product's native-loading boundary. The existing setuptools vendored-license qualifications, including the previously recorded LGPLv3 metadata, remain unchanged. No claim that every developer component is Apache-2.0 or MIT is made. Developer wheels and action bundles are not redistributed in the product wheel or uploaded as CI evidence.

The bootstrap pip is supplied by the selected Python/venv installation; its actual version is logged without an automatic pip upgrade or a new build frontend. `pip check` and exact installed-version checks follow offline installation. The existing source/wheel, clean-runtime and source-rebuild tests run unchanged.

## 4. Authority and workflow contract

The workflow runs on pull requests into main and pushes to main. PR jobs check out the actual PR head SHA; push jobs check out github.sha. The driver verifies HEAD before running repository code. The matrix has fail-fast disabled so one failure cannot hide another platform result. Each job has a 25-minute timeout, bounded subprocesses, and only contents-read permission. There is no privileged trigger, write token, deployment, package upload, automatic merge, arbitrary user ref input, repository-secret reference, cache or pull-request title/body interpolation into a shell command.

The file `.github/workflows/phase1-ci.yml` uses JSON-form YAML. This permits a strict standard-library JSON parser with duplicate-key rejection, without adding PyYAML. Fourteen independent policy tests check the approved structure and deliberate changes to permissions, triggers, pins, retained credentials, matrix coverage, skipped stages, ignored failures, shell interpolation and artifact scope. Successful parsing or policy tests do not establish hosted success; GitHub's actual workflow execution remains required.

The bounded CI driver resides in the same allowed developer test file, `tests/scaffold/test_ci_contract.py`. It is never imported by the installed auditor. Its explicit stages are preflight, prepare, test and evidence. CI-stage invocation requires GITHUB_ACTIONS=true; ordinary test collection executes no dependency acquisition. All application modules remain the exact W02 placeholders.

## 5. Actual-checkout and test evidence design

Before dependency installation the driver records all tracked-file SHA-256 identities and runs both W05 developer commands against the full actual checkout. This closes W05's expressly deferred full-checkout test when it succeeds. The driver records the true result rather than substituting the prior synthetic-workspace check.

The accumulated suite explicitly selects both tests/scaffold and tests/security. The original pytest default selects only tests/scaffold, so relying on that default would omit W05 security tests. The collection gate requires every existing test file in those two scopes, unique collected node IDs and at least the 168 earlier test instances. W06 contributes fourteen policy tests. No deselection, skip/xfail allowance, parallel test plugin or modified historical test is selected.

Test execution uses the isolated tools interpreter. Package-index access is disabled during the tests; the existing application network probes still independently test application-originated effects. The build tests use the reviewed backend directly and perform offline installation into a no-pip runtime venv. They inspect source/wheel contents, exclusions, original license bytes, lack of runtime requirements, refusal behavior and source-rebuild member-byte equality. Native files, logical expected answers and domain algorithms remain absent from the product package.

Always-run evidence recording captures JUnit totals, collection IDs, pytest exit, dependency/installation records, guards, tracked-byte preservation, and member hashes of self-built archives. It requires all collected tests to finish without failure/error/skip, both guards to pass, tracked files to remain unchanged and the expected build evidence to exist. A setup or execution failure stays failed even if some other checks pass.

Only explicit JSON, XML and log patterns under RUNNER_TEMP/sit-w06/evidence are uploaded for fourteen days. No source-paper PDFs, real user dossiers, whole workspace, package binaries, wheelhouse or environment dump is uploaded. Evidence contains hashes and synthetic-test diagnostics. No credentials are explicitly injected into the driver or child tests.

## 6. Execution record and next gate

Local standard-library policy testing passed all fourteen methods before submission. Local direct Git transport still cannot resolve github.com; no complete local clone or full local accumulated-suite result is claimed. The connected repository is the authority, and the hosted matrix will operate on its full checkout.

Hosted results, failures and final candidate identity will be recorded after they exist in PHASE_1_PROGRESS.md and the W06 PR. P1-W06 must remain unaccepted while a required matrix job is failed or missing. A defect in a previous unit's file requires a scoped repair authorization rather than a silent edit. No P1-W07 work or final Phase 1 completion is authorized by this document.
