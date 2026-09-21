# Phase 3 CI transition review

W01 retains `.github/workflows/phase1-ci.yml` as the single cumulative engineering workflow. Required profiles remain Ubuntu 24.04 and Windows Server 2025, each on CPython 3.11 and 3.13. The historical P1 workflow stays frozen and is not acceptance evidence for Phase 3.

Action revisions, developer dependency pins, read-only permissions, credential-free checkout, finite timeouts and fourteen-day artifact retention remain unchanged. Actual patch/image versions and installation results belong to the hosted evidence, not inferred support claims.

## Independent context and historical scope

Only actual `phase3/p3-wNN` PR branches or one valid main merge footer select the current Phase 3 unit. Candidate policy and source data cannot select their authority. Explicit Phase 2 scope and repair APIs retain their original meanings. Entry, ancestry, intermediate commits, final work-unit diff and frozen bytes are independently verified.

The retained suite maps all 1,650 accepted W09 identities against actual collection and JUnit. Its 428 subtest events are separately counted. Full tracked-byte inventories before and after, raw logs, JUnit, guards, package inventories and installed-runtime evidence are required.

## Execution and applicability

The fixed-pin applicability review below is complete as of 2026-09-21; exact-head four-profile execution remains pending. No dependency replacement or relaxed check is authorized. The disclosed plan-context failure is historical, not a passing W01 run.

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
