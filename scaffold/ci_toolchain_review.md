# P1-W06 CI Toolchain Review

## Control record

| Field | Value |
|---|---|
| Revision | 0.2, first matrix findings and summary correction |
| Date | 2026-09-18 UTC |
| Owner instruction | `批准并合并 PR #6，然后进入 P1-W06` |
| Intake merge | `ecf4eb5126201a7c31250c6dae8cbe2c64f9066a` |
| Branch / PR | `phase1/p1-w06`, draft PR #7 |
| First tested head | `668d4af4382b03aad19852aef2bdaa9252dc66d9` |
| First run | `35357942013`, attempt 1; failed |
| Current gate | Earlier-unit test repairs need P1-W06-R01 approval |
| Product runtime dependencies / analytics | None / unimplemented |

The complete pre-execution revision 0.1 is preserved at the first tested head, this path. This current record retains its selected tools, exact action identities, security scope and primary references while adding observed results. It does not rewrite failed history.

## 1. Selected and executed matrix

Ubuntu 24.04 x64 and Windows Server 2025 x64 each run CPython 3.11 and 3.13. The official hosted-runner labels and Python support table were checked before submission. Actual first-run environments were Ubuntu 24.04.5, image 20260907.300.1, Python 3.11.16/3.13.15; and Windows-2025Server-10.0.26100, image 20260907.229.1, Python 3.11.9/3.13.15.

The requested minors are resolved with check-latest and prereleases disabled. An installed patch is reported exactly, not described as the newest security release. These ephemeral hosted images and successful import/build probes do not certify the later Windows 11/NTFS native adapter or supported production deployment.

Sources: `https://docs.github.com/en/actions/reference/runners/github-hosted-runners`; `https://devguide.python.org/versions/`.

## 2. Fixed actions and authority

Official tag refs, pinned action.yml and LICENSE files were read through the connector before submission. The actual runner logs confirm execution of these selected commits.

| Action | Release | Commit | Runtime / license |
|---|---|---|---|
| actions/checkout | v7.0.1 | `3d3c42e5aac5ba805825da76410c181273ba90b1` | Node 24 / MIT |
| actions/setup-python | v7.0.0 | `5fda3b95a4ea91299a34e894583c3862153e4b97` | Node 24 / MIT |
| actions/upload-artifact | v7.0.1 | `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a` | Node 24 / MIT |

Pinned action manifest blobs: checkout `5b0524f730db83f9513c18ab31a6c086c7239076`; setup-python `df6c8235b476652b6402d31d92a2a89cdea74bb9`; upload-artifact `7cb4d1e81db55320b41217e1a78a1a46e3d2baef`. License blobs are `a67dca8b4f65d6bd351f6b1e333ce2cd84d843a5`, `a426ef259d6c5d705e9c1405075c3b318093c65e`, and `a67dca8b4f65d6bd351f6b1e333ce2cd84d843a5` respectively.

The new workflow replaces neither the old dedicated W02 workflow nor any product dependency. It uses contents-read permission, exact candidate head checkout, no persisted checkout credentials, no cache configuration, no privileged trigger, no deployment/merge/publication step and no repository-secret reference. Job timeouts are 25 minutes; fail-fast is false. No insecure Node runtime override is set. Actions' internal token use for checkout/Python acquisition is separate from explicitly passing secrets to tests.

The workflow is JSON-form YAML accepted by GitHub and validated with duplicate-key rejection and closed structural comparisons. Fourteen policy tests guard permissions, pins, matrix, stage execution, credential persistence, shell interpolation and upload boundaries. Full commit selection follows `https://docs.github.com/en/actions/reference/security/secure-use`. This is an interface/identity/authority review, not an audit of every bundled action dependency.

## 3. Actual development dependency installation

The unchanged requirements blob is `e037242d849f827a6c968a0f97830610a1718138`. Every row downloaded binary wheels, checked exact allowed name/version sets, complete SHA-256/size against PyPI release records and non-yanked status, inventoried licenses and vendored metadata, installed offline and passed pip check. The existing selected direct hashes were separately enforced.

Pins remain setuptools 84.0.0, pytest 9.1.1, iniconfig 2.3.0, packaging 25.0, pluggy 1.6.0 and Pygments 2.20.0. Windows additionally resolves the already approved Colorama 0.4.6 marker. No new runtime library, plugin or build frontend is introduced. Actual complete wheel metadata and notice hashes are in each reviewed-wheels.json. The prior setuptools vendored-license and archive_util applicability qualifications remain in the immutable W02 toolchain review; they are not replaced by a claim that every included component is MIT or vulnerability-free.

The bootstrap pip comes from each selected Python/venv environment without an automatic upgrade. Networked acquisition is limited to CI setup. Tests receive PIP_NO_INDEX=1; the product's no-network behavior is separately probed. No developer wheel binaries are included in product packages or uploaded as evidence. Sources checked included exact release JSON for setuptools 84.0.0, pytest 9.1.1 and Colorama 0.4.6 at `https://pypi.org/pypi/<name>/<version>/json`.

## 4. First execution results

The full test collection explicitly included tests/scaffold and tests/security. Each row collected 182 unique top-level instances, covering every existing test file in those scopes. There were no deselections, skipped methods or xfail allowances.

| Row | Passed | Failed | Additional successful subtests |
|---|---:|---:|---:|
| Ubuntu / 3.11 | 170 | 12 | 420 |
| Ubuntu / 3.13 | 170 | 12 | 420 |
| Windows / 3.11 | 169 | 13 | 420 |
| Windows / 3.13 | 169 | 13 | 420 |

All four full-checkout baseline and module guards passed before/after. Tracked bytes remained identical. Both original/rebuilt wheels had 55 members, and each source distribution had 65 regular members. Clean offline installation without developer dependencies and source-rebuild member-byte equality passed on each row. Windows' complete source-inventory test failed because the backend-generated setup.cfg uses CRLF while its historical expected byte string uses LF.

All twelve W05 security methods failed during probe initialization before importing the first product module, reporting AttributeError. Source inspection and an isolated minimal reproduction identify the unpreloaded importlib.util reference in the probe. Passing static module guards does not replace the failing dynamic probes. Two earlier-unit files need the explicitly scoped repair recorded as P1-W06-R01 in PHASE_1_PROGRESS.md; neither has been modified.

## 5. Evidence accounting and local correction

The first helper mistakenly compared the JUnit suite aggregate of 602 events with 182 collected instances. Full XML inspection found 182 testcase elements and suite tests=602, with the log separately reporting 420 successful subtests. This driver defect is repaired inside the authorized W06 test file. The new parser matches each classname/name pair to an actual collected ID, rejects omitted/duplicate/unexpected outcomes and reports the event aggregate separately. Suite or element failures/errors/skips and a nonzero pytest exit still block acceptance.

Six accounting controls join the fourteen policy methods. All twenty methods passed locally, and the corrected parser was applied to all four downloaded original JUnit files, preserving the actual twelve/thirteen failures. A new hosted run on the successor is needed and will be recorded in PR #7. The older run is not relabeled as a pass or attributed to changed executable bytes.

## 6. Downloaded evidence identity

All four complete first-run evidence ZIPs were retrieved through the connector and matched against these Actions SHA-256 records before their JSON/XML/log contents were inspected:

| Row | Artifact ID | Bytes | ZIP SHA-256 |
|---|---:|---:|---|
| Ubuntu / 3.11 | 10552901530 | 38761 | `6d29a54760d9385b8ada06847ac58c2d4da9797740ebf215a644c9b422ad9fb0` |
| Ubuntu / 3.13 | 10552856527 | 38613 | `beadf5644ef1344ac229a1d575e9b03261e9caa2c2bb1ab6b328a38125389e5a` |
| Windows / 3.11 | 10552926653 | 46347 | `9e78f49ab64130b0f57652acdbe2f62c9a8e8a99692ca02ba1866e27eb3709eb` |
| Windows / 3.13 | 10553106403 | 46152 | `daa3937d3e268f0749b5c25747a993e35d5acba9eeee7b19e2a5bf8393f796b5` |

Canonical run: `https://github.com/DavidWallstructurallaw/source-integrity-toolkit/actions/runs/35357942013`.

Uploads are restricted to explicit JSON/XML/log patterns under RUNNER_TEMP/sit-w06/evidence for fourteen days. No workspace dump, user dossier, theory PDF, source archive, wheel binary or credential dump is uploaded. Artifacts preserve failures rather than hiding them behind a missing file or a success-only upload.

## 7. Stop point

P1-W06 is blocked and PR #7 remains draft. The next approval requested is limited to the two test-file repairs, retained adverse controls and full matrix rerun. Original specifications, product code, dependency pins and case oracles remain frozen. No P1-W07, production platform claim, domain implementation or package publication is authorized.
