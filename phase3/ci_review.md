# Phase 3 CI transition review

The W01 sections below retain their historical execution and review context. The current W14 applicability review follows them; its hosted execution remains pending at record creation.

W01 retains `.github/workflows/phase1-ci.yml` as the single cumulative engineering workflow. Required profiles remain Ubuntu 24.04 and Windows Server 2025, each on CPython 3.11 and 3.13. The historical P1 workflow stays frozen and is not acceptance evidence for Phase 3.

Action revisions, developer dependency pins, read-only permissions, credential-free checkout, finite timeouts and fourteen-day artifact retention remain unchanged. Actual patch/image versions and installation results belong to the hosted evidence, not inferred support claims.

## Independent context and historical scope

Only actual `phase3/p3-wNN` PR branches or one valid main merge footer select the current Phase 3 unit. Candidate policy and source data cannot select their authority. Explicit Phase 2 scope and repair APIs retain their original meanings. Entry, ancestry, intermediate commits, final work-unit diff and frozen bytes are independently verified.

The retained suite maps all 1,650 accepted W09 identities against actual collection and JUnit. Its 428 subtest events are separately counted. Full tracked-byte inventories before and after, raw logs, JUnit, guards, package inventories and installed-runtime evidence are required.

## Execution and applicability

The fixed-pin applicability review below is complete as of 2026-09-21; the code-head four-profile run `35548424303` has passed with independently audited raw evidence. No dependency replacement or relaxed check is authorized. The disclosed plan-context failure is historical, not a passing W01 run.

The planning head failed run `35545499745` with `review_branch_requires_explicit_unit`. Its accepted merge failed inherited run `35546955084` in all four profiles before collection; decoded job `106174464579` confirms `main_merge_requires_unit_footer`. Neither result is reported as a W01 pass. The plan-merge message carries `SIT-Phase-Plan: P3`, not a fictitious work-unit footer.

## Fixed-pin applicability review, 2026-09-21

The three official action definitions at their unchanged commits still use Node 24. The workflow keeps read-only `contents`, credential-free checkout, PR/push-to-main events, no dependency cache, no supplied secrets or publishing, a 25-minute job limit and fourteen-day verification-artifact retention. This is a scoped execution review, not a general security certification.

Exact PyPI release metadata was checked for [setuptools 84.0.0](https://pypi.org/project/setuptools/84.0.0/), [pytest 9.1.1](https://pypi.org/project/pytest/9.1.1/), [iniconfig 2.3.0](https://pypi.org/project/iniconfig/2.3.0/), [packaging 25.0](https://pypi.org/project/packaging/25.0/), [pluggy 1.6.0](https://pypi.org/project/pluggy/1.6.0/), [Pygments 2.20.0](https://pypi.org/project/Pygments/2.20.0/) and Windows-only [colorama 0.4.6](https://pypi.org/project/colorama/0.4.6/). Their declared Python lower bounds cover the selected minors. No version was changed. Real wheel resolution, hashes, installation and imported versions must still pass in each hosted profile.

| Reviewed advisory | Published fixed boundary | Selected-pin assessment |
|---|---|---|
| [pytest GHSA-6w46-j5rx-g56g](https://github.com/github/advisory-database/blob/main/advisories/github-reviewed/2026/01/GHSA-6w46-j5rx-g56g/GHSA-6w46-j5rx-g56g.json) | 9.0.3 | 9.1.1 is outside the recorded affected range |
| [Pygments GHSA-5239-wwwm-4pmq](https://github.com/github/advisory-database/blob/main/advisories/github-reviewed/2026/03/GHSA-5239-wwwm-4pmq/GHSA-5239-wwwm-4pmq.json) | 2.20.0 | The retained pin is at the fixed boundary |
| [setuptools GHSA-h35f-9h28-mq5c](https://github.com/github/advisory-database/blob/main/advisories/github-reviewed/2026/07/GHSA-h35f-9h28-mq5c/GHSA-h35f-9h28-mq5c.json) | 83.0.0 | 84.0.0 is outside the recorded affected range |
| [jaraco.context GHSA-58pv-8j8x-9vj2](https://github.com/advisories/GHSA-58pv-8j8x-9vj2) | 6.1.0 | Each actual setuptools installation must retain the previously reviewed vendored 6.1.0 |

The [setuptools history](https://setuptools.pypa.io/en/latest/history.html) still lists an `archive_util` backslash/drive/UNC traversal repair, GHSA-grgh-hr87-3jpw, under its 2026-09-08 draft section. This review does not claim setuptools 84 contains that repair. The advisory body could not be retrieved, so no affected-version range is inferred. The present CI installs verified binary wheels, builds this repository through the direct backend, and inspects its own tar members with exact member and regular-relative checks plus `extractfile`; it does not use `archive_util` to extract externally supplied untrusted archives. No applicable path requiring a pin change was identified for that bounded use. That conclusion cannot be generalized to arbitrary package building or archive extraction; the [stdlib extraction-filter documentation](https://docs.python.org/3.13/library/tarfile.html#extraction-filters) states the relevant tar boundary.

The [PSF version status](https://devguide.python.org/versions/) and [Python 3.11.9 release page](https://www.python.org/downloads/release/python-3119/) distinguish the last bugfix binaries from subsequent security releases. Hosted evidence records actual patch and image versions. It does not label Windows 3.11.9 the latest security patch or certify production native-platform support.

The exact action definitions reviewed were [checkout](https://github.com/actions/checkout/blob/3d3c42e5aac5ba805825da76410c181273ba90b1/action.yml), [setup-python](https://github.com/actions/setup-python/blob/5fda3b95a4ea91299a34e894583c3862153e4b97/action.yml) and [upload-artifact](https://github.com/actions/upload-artifact/blob/043fb46d1a93c77aae656e7c1c64a875d1fc6a0a/action.yml); their source blobs are respectively `5b0524f730db83f9513c18ab31a6c086c7239076`, `df6c8235b476652b6402d31d92a2a89cdea74bb9` and `7cb4d1e81db55320b41217e1a78a1a46e3d2baef`. [GitHub's secure-use guidance](https://docs.github.com/en/actions/reference/security/secure-use) supports full commit pins and least privileges. Search non-results are not treated as proof of absence of vulnerabilities.

## Actual W01 code-head execution

Head `ec221258e3a43fa28f4e9d1c5aeb8bc214b1ae15`, tree `1aa6a55eefedec72b32c22a6274fcec14e969786`, passed run `35548424303`, attempt 1, in all four required profiles. Every profile retained the exact selected developer distributions, collected 1,786 top-level nodes across 35 files, passed 428 separate subtest events and reported zero failures/errors/skips. Raw service ZIP identities, tracked before/after hashes, guards, actual commit history,55-member wheel and 65-regular-member sdist inventories, rebuilt wheel member equality and installed 48-module/eight-mode witness were independently audited.

Initial hosted run `35547854833` remains failed with three temporary Git-fixture failures on each Windows profile; the later fixed-head pass does not relabel that history. The transition ledger records the CRLF reproduction and narrow fixture repair.

The final documentation successor's separate exact-head matrix is pending at record creation and must be recorded on PR #20 after commit. These are finite development verification results; no analytical field, full report, native security or release qualification is claimed.

## W14 fixed-pin applicability review, 2026-09-23

The current inherited `.github/workflows/phase1-ci.yml` has a **40-minute** job limit. The cumulative pytest subprocess independently retains its **1,800-second** timeout in `tests/scaffold/test_ci_contract.py::run_suite`; the job limit does not extend that test window. The 25-minute statement above describes W01. W14 changes neither the workflow nor developer/build pins. Required profiles remain Ubuntu 24.04 and Windows Server 2025 with CPython 3.11 and 3.13, read-only `contents`, exact-candidate checkout with `persist-credentials: false`, disabled dependency cache, no supplied secrets or publishing, and fourteen-day artifact retention. The three exact action definitions linked above were retrieved again and each specifies Node 24. Their use remains consistent with [GitHub's secure-use guidance](https://docs.github.com/en/actions/reference/security/secure-use); the review does not certify every transitive action component.

All seven exact PyPI release pages linked above were rechecked. Their declared Python requirements admit both selected minors: setuptools 84.0.0, pytest 9.1.1 and iniconfig 2.3.0 require Python >=3.10; packaging 25.0 requires >=3.8; pluggy 1.6.0 and Pygments 2.20.0 require >=3.9; colorama 0.4.6's exclusions end at Python 3.6 and it remains Windows-only here. These declarations support attempting the retained matrix. Each profile must still establish actual wheel hashes, installation, imported versions and `pip check` results.

The three GitHub advisory-database records linked in the W01 table were retrieved again: pytest GHSA-6w46-j5rx-g56g fixes versions before 9.0.3, Pygments GHSA-5239-wwwm-4pmq fixes versions before 2.20.0, and setuptools GHSA-h35f-9h28-mq5c fixes versions before 83.0.0. The selected pins remain outside those recorded affected ranges. The [jaraco.context advisory](https://github.com/advisories/GHSA-58pv-8j8x-9vj2) still records the affected range >=5.2.0,<6.1.0 and the fixed boundary 6.1.0. The local retained setuptools installation contains vendored jaraco.context 6.1.0 metadata; the four hosted installations remain subject to their actual evidence.

The [setuptools history](https://setuptools.pypa.io/en/latest/history.html) still places the `archive_util` backslash/drive/UNC repair under the unreleased September 8 draft. The direct [GHSA-grgh-hr87-3jpw page](https://github.com/advisories/GHSA-grgh-hr87-3jpw) returned 404 during this review, so its affected-version range remains unverified and setuptools 84.0.0 is not credited with that repair. Inspection of the retained CI and packaging tests confirms binary developer-wheel installation, direct `setuptools.build_meta` builds, exact package member inventories, and regular relative member reconstruction with `tarfile.extractfile` for this repository's own sdist. No `archive_util` extraction of externally supplied archives is used by that path. This bounded source review identifies no applicable dependency correction for the retained use; it supplies no assurance for arbitrary archive extraction or third-party source builds. Search coverage was incomplete and cannot establish absence of additional vulnerabilities.

The [PSF version status](https://devguide.python.org/versions/) continues to list 3.11 in security maintenance and 3.13 in bugfix maintenance. Actual patch/image versions belong to hosted artifacts. The [3.11.9 release record](https://www.python.org/downloads/release/python-3119/) remains relevant to the Windows binary limitation; no latest-security-patch or Windows 11 native certification follows from the selected labels.

This review was authored by a collaborating instance of the same assistant using the shared repository, earlier W01 review and freshly retrieved primary sources. It is not independent external review. W14's exact-code-head four-profile cumulative execution, raw artifact audit, new installed private-analysis results and collection/JUnit identity agreement are pending at this record's creation. The implementation evidence and review package must record their actual results after execution; earlier W01 or W13 passes cannot establish W14 acceptance.
