# PHASE_1_PROGRESS

## Current control record

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Progress revision | 0.10, P1-W06 execution candidate |
| Record date | 2026-09-18 UTC |
| Approved plan | PHASE_1_PLAN.md revision 0.1, blob `27ed33cb1c2afc78b12ca099ee7ccb4e68d63bfb` |
| Owner instruction | `批准并合并 PR #6，然后进入 P1-W06` |
| Accepted W05 head | `6bf3ef93fd90471da709d6f90e598e9d84f95908` |
| Actual PR #6 merge / W06 intake | `ecf4eb5126201a7c31250c6dae8cbe2c64f9066a` |
| Review branch | `phase1/p1-w06` |
| W06 state | Five-path candidate; local policy tests passed; hosted matrix pending |
| W06 owner acceptance / merge | Pending |
| P1-W07 / Phase 2 | Not authorized or executed |

## 1. Accepted predecessor and history

The owner explicitly accepted PR #6 and requested its merge before W06. The connector confirmed its exact head, open/non-draft and mergeable state. The remote comparison listed the same twelve authorized W05 paths. The expected-head-protected merge succeeded and returned the intake commit above. W06 starts from that actual commit; no history was rewritten or force-pushed.

W05's 42 local tests and precise execution limits remain preserved in PR #6 and progress revision 0.9 at `6bf3ef93fd90471da709d6f90e598e9d84f95908`. Its new baseline command had not been exercised against a complete actual local checkout. W06 explicitly runs that command on all twenty actual protected files in each required hosted matrix row. A future pass will supplement, not rewrite, that historical limitation.

W04's accepted exact-byte import, 29 hosted static checks, PR #5 merge and removal of its isolated temporary transport workflow remain preserved in the predecessor records. The one-time import mechanism is not reused or included in W06.

## 2. Closed W06 change scope

Only these five paths are created or updated:

```text
.github/workflows/phase1-ci.yml
scaffold/ci_toolchain_review.md
tests/scaffold/test_ci_contract.py
README.md
PHASE_1_PROGRESS.md
```

The frozen eighteen specifications, corrected approval, approved plan, baseline manifest, all product modules, existing tests, fixture/oracle assets, catalogs, development pins, packaging configuration, licenses and existing dedicated W02 workflow are unchanged. The new CI helper lives in the allowed developer test file and implements no source-audit operation.

## 3. Workflow and verification design

The four-row matrix selects ubuntu-24.04 and windows-2025, each with CPython 3.11 and 3.13. The official action refs, action manifests, LICENSE files, runner labels, Python support status and relevant PyPI records were checked at execution time. Exact reviewed action SHAs are in scaffold/ci_toolchain_review.md. All three selected actions declare Node 24. No insecure Node override, new runtime dependency or build frontend is introduced.

The workflow uses contents-read permission, exact candidate checkout without stored credentials, no cache, no privileged trigger, no deployment/publication, finite timeouts and no repository-secret reference. It operates on review PRs and main pushes. Only verification JSON/XML/log files under a fixed runner-temp evidence directory are uploaded for fourteen days. User dossiers, source-paper PDFs, arbitrary workspace contents and package binaries are excluded.

Preflight verifies the actual checked SHA, records actual environment and tracked-file digests, and executes both W05 developer guards on the full checkout. Preparation reviews the exact selected development wheels before offline installation. The test stage explicitly collects and runs tests/scaffold plus tests/security, including the earlier packaging and clean-runtime tests. The always-run evidence stage preserves actual outcomes, inspects self-built archive inventories and reruns guards while checking all tracked bytes remain unchanged.

A declared workflow matrix is not a test result. Collection failures, omitted test files, skips, setup failures, missing build evidence and guard failures remain blocking. A failed prior-unit file is not edited under this unit's five-path scope.

## 4. Actual preparation evidence

The fourteen new standard-library policy tests passed locally with zero failures/errors/skips. They include deliberate mutations of permission, privileged trigger, action pin, stored credential, required platform/minor, skipped stage, ignored failure, untrusted shell expression, upload scope and secret environment settings, plus duplicate-key rejection. The helper's suite-running function is deliberately not named as a pytest test.

Direct local Git access still fails DNS resolution for github.com. The local workspace was used for authoring and policy controls only. No full local repository test or selected-toolchain installation is claimed. The hosted workflow will provide the actual-checkout and matrix evidence. Current candidate commits add only the allowed files; final compare and byte checks remain required before handoff.

## 5. Current gate

Create the W06 draft review PR, run its four required jobs, inspect their logs and artifacts, and record actual failures or success at the exact tested head. Keep the PR unmerged. P1-W06 remains pending until all required results exist and pass; P1-W07 remains a separate owner-authorized unit. No general platform certification, production security proof, domain-test success or final Phase 1 completion follows from these scaffold checks.
