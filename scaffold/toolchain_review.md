# P1-W01 Toolchain Review

## Review record

| Item | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Work unit | P1-W01 |
| Review date | 2026-09-17 |
| Review revision | 0.1 |
| Governing decision | Approved DEPENDENCY_STRATEGY.md and PHASE_1_PLAN.md |
| Proposed build pin | `setuptools==84.0.0` |
| Proposed test pin | `pytest==9.1.1` |
| Product runtime dependencies | None |
| Review level | Published metadata, versioned license/source inspection and scoped risk review |
| Installation, resolution, build or compatibility execution | Not performed in P1-W01; assigned to P1-W02 |

These pins select the two tool classes already allowed by the plan. They introduce no runtime dependency, optional framework, additional build frontend or product capability. Metadata compatibility is distinct from successful installation or tests on an actual platform.

## 1. Exact direct-tool choices

| Tool | Published compatibility and license | Intended use and limits |
|---|---|---|
| setuptools 84.0.0 | Published `Requires-Python: >=3.10`; project MIT license; versioned tag `v84.0.0` | PEP 517 build backend `setuptools.build_meta`, only in the isolated build/development environment |
| pytest 9.1.1 | Published `Requires-Python: >=3.10`; project MIT license; versioned tag `9.1.1` | Scaffold test runner only; no `pytest[dev]` extras or external test plugins selected |

Both published lower bounds admit the project's CPython 3.11 lower-bound target. No claim is made that every later Python minor, PyPy, Windows filesystem adapter or Linux native ABI is supported. Actual interpreter choices and resolved environments must be recorded when executed. A project's classifiers are not this toolkit's conformance evidence.

The proposed backend exposes the standard wheel/source-distribution build hooks. P1-W02 may use those hooks in its controlled authoring environment without adding an unreviewed frontend. Any extra frontend or developer tool still needs the plan's scoped review before adoption. There is no `setup.py` or packaging declaration in P1-W01.

## 2. Dependency implications

Setuptools 84.0.0 declares no unconditional separately installed project dependencies in its base metadata. It nevertheless includes vendored components and distutils-derived code. The reviewed `_vendor` directory includes, among other entries, autocommand 2.2.2, backports.tarfile 1.2.0, importlib_metadata 8.7.1, jaraco components, more_itertools 10.8.0 and packaging 26.0. An empty top-level dependency list does not make those components disappear or relicense them as project-owned MIT code.

Do not request setuptools test/doc/core/check/cover/type extras. Their additional dependencies are outside the selected minimal toolchain. Preserve upstream vendored and distutils notices in the installed tool environment. Do not copy the backend or its vendored tree into the toolkit wheel. P1-W02 must inspect the actual downloaded artifact and any files it places in generated distributions; this source-directory inspection is not a completed wheel audit.

Pytest 9.1.1 publishes the following base requirements. The constraints are copied from its metadata; they are not an already resolved lockfile.

| Dependency constraint | Applicability for the planned environment |
|---|---|
| `iniconfig>=1.0.1` | Test environment |
| `packaging>=22` | Test environment |
| `pluggy>=1.5,<2` | Test environment |
| `pygments>=2.7.2` | Test environment |
| `colorama>=0.4; sys_platform == "win32"` | Windows test environment only |
| `exceptiongroup>=1; python_version < "3.11"` | Inactive for the project's Python 3.11+ target |
| `tomli>=1; python_version < "3.11"` | Inactive for the project's Python 3.11+ target |

P1-W02 owns the actual resolver result, exact transitive versions, applicable artifact licenses and environment-specific differences. Those transitive packages remain developer dependencies even though pytest calls them its runtime requirements. They must not appear as runtime requirements of Source Integrity Toolkit. No `pytest[dev]` dependency such as requests, hypothesis or xmlschema is adopted by this review.

A third-party license retains its own attribution and redistribution conditions. Review the resolved artifact's notices before redistributing any part of it. This work unit distributes none of these tool packages and makes no claim of complete legal clearance for a future dependency graph.

## 3. Execution and supply-chain boundary

Use isolated project environments when P1-W02 is authorized. Record exact artifacts/versions and the actual installer environment; do not silently install latest versions in place of these pins. Do not add a global package, native binding or product dependency to make a scaffold check pass. The installed toolkit must work without pytest or setuptools in its runtime dependency set.

Build only the explicitly reviewed checkout. Do not use the backend to process caller evidence or arbitrary archive uploads. Treat tests and build hooks as executable developer code, with only the authority required by the current step. Future CI installation networking is distinct from the auditor's local-only runtime requirement. Disable unrequested pytest plugin autoload in the controlled test invocation so unrelated installed plugins cannot change the test environment; this is a future invocation requirement, not configuration created in this unit.

### Current risk note

The upstream setuptools history viewed during this review contains an unreleased archive-util extraction-safety change associated with `GHSA-grgh-hr87-3jpw`. The separately linked advisory page could not be retrieved. This review therefore does not assert its complete affected-version range or that 84.0.0 contains the unreleased fix. P1-W02 must recheck the current upstream advisory/release status before installation and keep untrusted archive extraction outside the build workflow. If a required operation is affected, review an appropriate fixed pin before proceeding. An empty vulnerability array in package-index metadata is not a security certification.

No dependency installation, archive extraction, resolver run, package build or product test was performed here. This residual review requirement does not authorize substituting an unreviewed tool or disabling a guard.

## 4. License text applied in this work unit

The root `LICENSE` contains the standard Apache License 2.0 text, including its unmodified appendix. Project attribution is in `NOTICE` and README; no project-specific condition is inserted into the standard license.

The official Apache plain-text license was viewed at execution time. The byte reference was also fetched from Apache's own website source repository, `apache/www-site`, path `content/licenses/LICENSE-2.0.txt`, Git blob `d645695673349e3947e8e5ae42332d0ac3164cd7`, 11,358 bytes. The local license copy matches that entire blob byte-for-byte. Its file SHA-256 is `cfc7749b96f63bd31c3c42b5c471bf756814053e847c10f3eb003417bc523d30`.

The selected license applies only to the original engineering material identified by LICENSING_NOTES.md. It does not relicense theory works, third-party components or user evidence. MIT tool notices are not replaced with Apache-2.0 notices. No upstream Apache project endorsement or software contribution is claimed by using the standard license text.

## 5. Primary sources inspected

| Source | Locator and reviewed use |
|---|---|
| Apache standard license | `https://www.apache.org/licenses/LICENSE-2.0.txt`; legal text viewed at execution |
| Apache website source | `https://github.com/apache/www-site/blob/main/content/licenses/LICENSE-2.0.txt`; whole-file identity recorded in section 4 |
| setuptools release metadata | `https://pypi.org/pypi/setuptools/84.0.0/json`; version, Requires-Python, license expression and declared dependency markers |
| setuptools versioned source | `https://github.com/pypa/setuptools/blob/v84.0.0/pyproject.toml`; project metadata |
| setuptools versioned license | `https://github.com/pypa/setuptools/blob/v84.0.0/LICENSE`; MIT text, blob `1bb5a44356f00884a71ceeefd24ded6caaba2418` |
| setuptools vendored inventory | `https://github.com/pypa/setuptools/tree/v84.0.0/setuptools/_vendor`; source-level component inventory, not installed-wheel clearance |
| setuptools backend documentation | `https://setuptools.pypa.io/en/latest/build_meta.html`; standard backend hooks |
| setuptools history | `https://setuptools.pypa.io/en/latest/history.html`; current unreleased extraction-safety note, with the limitation in section 3 |
| pytest release metadata | `https://pypi.org/pypi/pytest/9.1.1/json`; version, Python bound, license and base requirements |
| pytest versioned source | `https://github.com/pytest-dev/pytest/blob/9.1.1/pyproject.toml`; requirement markers and extras |
| pytest versioned license | `https://github.com/pytest-dev/pytest/blob/9.1.1/LICENSE`; MIT text, blob `c3f1657fce94589bd1ec7cead810639047f3d359` |
| Git attributes documentation | `https://git-scm.com/docs/gitattributes`; explicit unset text behavior and path-level attributes |

Versioned locators and recorded blob identities preserve what was inspected. Unversioned documentation may change; later execution must review actual resolved tools and operations. These are engineering-tool sources, not additional evidence for the project's source theory.

## 6. Handoff to P1-W02

The next unit may declare the two reviewed direct pins, resolve and inspect the necessary developer dependencies, build and inspect its source/wheel artifacts, and run the permitted scaffold smoke tests. It must record the actual interpreter/platform, installer, transitive dependency graph, license review, current security observations and test outcomes in this file and PHASE_1_PROGRESS.md.

No application runtime dependency, package publication, production parser, source retrieval, analytical computation or native platform implementation follows from this toolchain review. W01 review completion does not mark later installation, packaging or CI checks as passed.
