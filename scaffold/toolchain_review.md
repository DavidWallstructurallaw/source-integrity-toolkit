# Scaffold Toolchain Review

## Current record

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Review revision | 0.3 |
| Date | 2026-09-17 |
| Work unit | P1-W02, scoped early hosted verification |
| Selected direct pins | setuptools 84.0.0; pytest 9.1.1, unchanged |
| Runtime dependencies | None |
| Current hosted evidence | Pending execution at this preparation checkpoint |

## 1. Preserved review and selected environment

The complete revision 0.2 review remains at `1126eff7d98023b9bc835dc00026ea5629f64a77`, this path. It incorporates the pinned W01 version/license source record and preserves the failed local acquisition, exact older-tool results, initial mechanical test repairs and unresolved hosted gate. Those events are not restated as selected-toolchain success.

The Linux development set remains setuptools 84.0.0, pytest 9.1.1, iniconfig 2.3.0, packaging 25.0, pluggy 1.6.0 and Pygments 2.20.0. The existing colorama 0.4.6 Windows marker is inactive in this job. No Python <3.11 dependency, pytest extra, product dependency, extra frontend or replacement tool is selected.

The direct wheel identities remain the previously reviewed 64-character SHA-256 values: setuptools `51a52592b3b99e102b609654876bd65f19f999935166d1352678931132b0c670`; pytest `37a86b45efb9a47a61a36449063e8e18d0cab3161329fc099eb21783169c4f0c`. Hosted verification must calculate those hashes over downloaded bytes, not merely quote metadata.

The selected tools are installed into a new venv. Its bootstrap pip comes with the selected CPython environment and its actual version is logged; pip is the already permitted installer, not a product dependency. No new build frontend is introduced. Source/wheel builds call setuptools.build_meta directly, with the existing independent exact-version assertion enforced.

## 2. Approved Actions-only additions

P1-W02-A01 authorizes the dedicated workflow `.github/workflows/p1-w02-verify.yml`. Its actions are orchestration dependencies of hosted verification only. They are not bundled in the toolkit or available to an audit caller.

| Action | Reviewed tag | Pinned commit | Reviewed project license |
|---|---|---|---|
| actions/checkout | v4.4.0 | `11d5960a326750d5838078e36cf38b85af677262` | MIT |
| actions/setup-python | v7.0.0 | `5fda3b95a4ea91299a34e894583c3862153e4b97` | MIT |
| actions/upload-artifact | v7.0.1 | `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` | MIT |

The tags were resolved through each official repository and the LICENSE file read at the pinned commit. setup-python and upload-artifact action manifests were checked for their Node 24 runtime and used inputs. The hosted runner supplies action execution infrastructure; no native auditor binding is enabled. This is a scoped review of inputs, permissions and release identities, not a line-by-line audit of all bundled JavaScript dependencies.

The workflow uses only contents:read, no persisted checkout token, no cache, no pull_request_target, no arbitrary branch input, no repository-secret input, no self-hosted runner and no deployment or publication action. It runs only for the existing same-repository PR #3 and its named branch. upload-artifact receives only explicit verification-record globs, with fourteen-day retention and no hidden files or package binaries.

## 3. Actual-artifact review obligations

Before installing any downloaded wheel, the job checks its expected name/version, whole-byte hash and size against exact-release PyPI metadata and checks that the selected file is not yanked. It records base dependency markers, Python requirement, license expression or legacy license field, included license/notice text and its hash, and setuptools' vendored dist-info metadata where present. A missing identity or notice fails the check. It does not execute wheel content during inspection.

Installation uses only that inspected wheelhouse with --no-index. pip check and installed-distribution records establish the actual Linux dependency result. Installed direct-version assertions remain unchanged. Third-party notice text in verification evidence retains upstream rights; it is not relicensed as project Apache-2.0 material.

The project package inventory tests keep those developer tools outside the product wheel. A separate runtime venv contains only the project distribution. Review of the actual downloaded records and hosted logs is still required before W02 is marked complete; preparing this workflow does not satisfy those checks.

## 4. Upstream security recheck

The primary setuptools history was checked again. Its heading still identifies the archive_util traversal/UnsafeMember changes as an unreleased draft dated September 8, 2026 and references GHSA-grgh-hr87-3jpw. The separately linked advisory could not be retrieved through this recheck, so no complete affected-version range or claim that 84.0.0 includes that fix is made.

This workflow uses binary-only developer wheels, a controlled reviewed project tree and self-built source archives. Its tests inspect and copy only regular checked relative members of those self-created archives; they do not invoke setuptools.archive_util to extract externally supplied material. The known extraction concern is outside these selected operations. The pin is retained on that bounded applicability assessment; no general vulnerability-free certification follows. Any expansion into externally supplied archives or contrary applicable advisory reopens the review.

## 5. Primary reference record

The versioned sources and earlier Python-package notices remain in revision 0.2 and its W01 predecessor. This supplement additionally consulted:

- GitHub official action repositories, the exact tags/commits and LICENSE files in section 2.
- `https://github.com/actions/setup-python/blob/5fda3b95a4ea91299a34e894583c3862153e4b97/action.yml`
- `https://github.com/actions/upload-artifact/blob/043fb46d1a93c77aae656e7c1c64a875d1fc6a0a/action.yml`
- `https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax`
- `https://docs.github.com/en/actions/reference/workflows-and-actions/events-that-trigger-workflows`
- `https://docs.github.com/en/actions/reference/security/secure-use`
- `https://setuptools.pypa.io/en/latest/history.html`
- `https://pypi.org/project/setuptools/` and `https://pypi.org/project/pytest/9.1.1/`

These are developer-infrastructure sources and add no theory mapping or analytical capability. Runtime source-network access remains prohibited. The next review records actual run identifiers, downloaded identities, resolver/install results and all test outcomes without modifying prior failure history.
