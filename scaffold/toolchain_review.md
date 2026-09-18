# Scaffold Toolchain Review

## Current record

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Review revision | 0.2 |
| Work unit | P1-W02 |
| Date | 2026-09-17 |
| Governing plan | PHASE_1_PLAN.md revision 0.1, section 6 |
| Selected build pin | `setuptools==84.0.0`, unchanged |
| Selected test pin | `pytest==9.1.1`, unchanged |
| Installed versions available in this session | setuptools 82.0.1; pytest 9.0.2 |
| Selected-toolchain acceptance | BLOCKED: selected versions cannot be acquired in the current execution environment |
| Product runtime dependencies | None |

The complete P1-W01 review, original version/license sources, Apache license byte comparison and initial risk note remain at:

`https://github.com/DavidWallstructurallaw/source-integrity-toolkit/blob/63c03ee82ebffd5f4dc73972b2baa158c20cdf33/scaffold/toolchain_review.md`

This revision records actual W02 work and limits. It does not replace the selected pins with older installed versions or describe supplemental compatibility checks as selected-toolchain acceptance.

## 1. Selected versions and current primary-source check

The current PyPI metadata for setuptools 84.0.0 and pytest 9.1.1 was re-read. Both releases are marked non-yanked, declare Python >=3.10 and MIT licensing. The project retains its approved Python >=3.11 requirement. Published compatibility remains distinct from executed compatibility.

The selected setuptools wheel is listed by PyPI as 818,216 bytes with SHA-256 `51a52592b3b99e102b609654876bd65f19f999935166d1352678931132b0c670`. The selected pytest wheel is listed as 386,536 bytes with SHA-256 `37a86b45efb9a47a61a36449063e8e18d0cab3161329fc099eb21783169c4f0c`. These are upstream advertised identities, not hashes of artifacts downloaded here. Neither selected wheel was obtained or installed in this session.

The metadata continues to show no unconditional separately installed setuptools base dependencies and the pytest requirements already recorded in W01. Vendored setuptools components remain part of its upstream dependency surface even when no separate base requirement is installed. No backend or vendor source is copied into the project package.

## 2. Acquisition failure and preserved gate

An attempted public repository clone failed because the execution environment could not resolve github.com. Explicit DNS checks also failed for pypi.org and files.pythonhosted.org. The GitHub connector continued to read and write the authorized repository successfully; those are separate access paths.

The command below failed without downloading either selected package:

```text
python -m pip download --disable-pip-version-check --retries 0 --timeout 8 --only-binary=:all: --no-deps --dest /mnt/data/sit-p1w02/wheelhouse setuptools==84.0.0 pytest==9.1.1
```

Its diagnostic reported no matching distribution in this environment. That result does not contradict the observed upstream release metadata. The separate binary download path also failed. No package-index release was created, no dependency was silently downgraded, and no GitHub Actions workflow was added ahead of W06 to bypass this limitation.

`test_declared_toolchain_is_actually_available` explicitly compares the installed direct tools with 84.0.0 and 9.1.1. It fails in this session. It is retained, without skip, xfail, environment-variable waiver or relaxed comparison.

## 3. Development dependency declarations

`requirements-dev.txt` keeps the two selected direct pins and names compatible transitive candidates:

| Package | Declared version | Session evidence / license |
|---|---|---|
| setuptools | 84.0.0 | Upstream metadata/license checked; unavailable locally |
| pytest | 9.1.1 | Upstream metadata/license checked; unavailable locally |
| iniconfig | 2.3.0 | Installed metadata and MIT license text inspected |
| packaging | 25.0 | Installed metadata and Apache-2.0/BSD license alternatives inspected |
| pluggy | 1.6.0 | Installed metadata and MIT license text inspected |
| Pygments | 2.20.0 | Installed metadata and BSD-2-Clause license text inspected |
| colorama | 0.4.6, Windows marker only | Not installed or executed here; Windows resolution/license-artifact review remains pending |

The selected direct tools' full transitive resolver result and downloaded-artifact review remain pending. These declarations are not represented as a verified cross-platform lock. Python <3.11-only exceptiongroup/tomli requirements are inactive for the project's target. No pytest extras, unrelated external plugins, runtime dependency or new build frontend is selected.

## 4. Supplemental local compatibility evidence

The existing environment contains CPython 3.13.5, setuptools 82.0.1, pytest 9.0.2 and pip 25.1.1 on Linux x86_64/glibc 2.41. The four installed transitive packages above were used. This environment was not installed from requirements-dev.txt and is not the required isolated selected-toolchain environment.

With pytest plugin autoload disabled, the committed test bodies were exercised against only the approved scaffold and fictional canaries. Direct calls to the existing setuptools.build_meta hooks built a source archive and wheel. Those hooks do not resolve build-system.requires, so this execution deliberately remains supplemental and the independent version test stays failed.

The supplemental wheel was installed using the existing pip into a new venv created with `--without-pip`, with `--no-index --no-deps --no-cache-dir`. The target contained only the project distribution. Its CLI help/version and fixed audit refusal worked, and its API stubs raised without returning a report. This demonstrates that the built wheel did not require pytest, setuptools or another third-party runtime package. It does not demonstrate a build with setuptools 84.0.0.

The source archive contained 65 regular files; the wheel contained 55 members, including the 48 approved Python files and seven dist-info/license entries. Rebuilding from the inspected self-created source archive produced the same member bytes. ZIP timestamps may differ; archive-wide reproducible build identity is not claimed.

The tests initially exposed an omitted generated `setup.cfg` expectation and a canary appearing in its own test source. The packaging test now permits only the inspected fixed egg_info tag metadata, and assembles its fictional canary from separate literals. Neither repair relaxes a source-integrity contract or a package exclusion. The upstream setuptools 84.0.0 sdist implementation also explicitly writes setup.cfg through save_version_info.

Final supplemental suite result: **77 passed, 1 failed, 0 skipped, 0 errors**. The remaining failure is the unchanged selected-toolchain gate.

## 5. Packaging and authority boundaries

The source distribution explicitly selects the 48 package slots, four scaffold test files, build/developer metadata, README, LICENSE and NOTICE, plus known backend-generated metadata. Normative specifications and approval/history records remain repository authorities and are not silently copied into the wheel or source archive. No paper PDF, private evidence, identity map, generated user report or unrelated data file is selected.

The wheel includes the named packages, metadata and the original license/notice. Package data discovery is disabled. Artifact inventory tests reject additional members; an unexpected Python source file cannot be accepted merely because setuptools discovered it. Fictional excluded-file probes were used. Root README retains its W01 wording because editing it is outside W02; PHASE_1_PROGRESS.md is the current work record.

No dossier parser, semantic validator, graph operation, analytical computation, serializer, native binding, clock/budget engine, HTTP client or model integration is implemented. Build and test tools exercise developer code only. Installing the scaffold creates no operational auditing claim.

## 6. Upstream risk recheck

The upstream setuptools history still labels its archive_util extraction-safety changes as unreleased. It states that backslash/drive/UNC traversal handling and an UnsafeMember exception are being changed, referencing GHSA-grgh-hr87-3jpw. The separately linked advisory remained unavailable with a 404 response. No complete affected-version range or claim that 84.0.0 contains that fix is asserted.

Only a controlled project snapshot and self-generated archives were used for supplemental builds. No untrusted archive was handed to setuptools.archive_util. Source rebuild tests copy only inspected regular members under a checked relative prefix using the standard library; they do not call the backend's archive extractor. The known operation boundary is retained while the selected-toolchain and applicable security review stay open.

An empty vulnerability array is not a security certification. Before W02 acceptance, obtain the selected packages in an authorized network-capable environment, review their actual artifacts and transitive notices, repeat the advisory/release check, install the declared environment and run every test including the strict version gate. A necessary version or policy change must be documented and approved within its proper scope.

## 7. Current source locators

- `https://pypi.org/pypi/setuptools/84.0.0/json`
- `https://pypi.org/pypi/pytest/9.1.1/json`
- `https://setuptools.pypa.io/en/latest/history.html`
- `https://github.com/pypa/setuptools/security/advisories/GHSA-grgh-hr87-3jpw` (unavailable during this recheck)
- `https://github.com/pypa/setuptools/blob/v84.0.0/setuptools/command/sdist.py`, make_release_tree / save_version_info, blob `c86f540bf59302f316f014eb48f4f9f8704f1d81`

These are engineering-tool references. They add no theory source or analytical finding. The preserved W01 source table retains its original versioned licenses and metadata references.
