# PHASE_1_PROGRESS

## Current control record

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Progress revision | 0.3 |
| Date | 2026-09-17 |
| Approved plan | PHASE_1_PLAN.md revision 0.1, blob `27ed33cb1c2afc78b12ca099ee7ccb4e68d63bfb` |
| Current owner instruction | `可以，合并 PR #2，并开始 P1-W02` |
| Accepted predecessor | P1-W01 at `63c03ee82ebffd5f4dc73972b2baa158c20cdf33` |
| Merged PR | #2 |
| Merge / W02 intake commit | `ae61bb6fa36d53fb2138542ee69e36585ee7bc72` |
| Current branch | `phase1/p1-w02` |
| Work status | W02 scaffold prepared; selected-toolchain verification BLOCKED |
| W02 acceptance / merge | Pending; not claimed complete |
| W03 and later work | Not started |

## 1. Preserved predecessor and merge evidence

The owner accepted the submitted W01 delivery and explicitly authorized its merge. GitHub confirmed a merge of PR #2 using expected head `63c03ee82ebffd5f4dc73972b2baa158c20cdf33`, producing `ae61bb6fa36d53fb2138542ee69e36585ee7bc72`. No force push, squash of the correction history, or branch-protection change was used.

The complete prior progress record remains at:

`https://github.com/DavidWallstructurallaw/source-integrity-toolkit/blob/63c03ee82ebffd5f4dc73972b2baa158c20cdf33/PHASE_1_PROGRESS.md`

It preserves the original entry hold, seven approval-manifest corrections, eighteen-file rehash evidence, licensing and governance delivery, and W01 test limitations. The initial blocked record also remains at commit `6e37659bdf345484babc4eb37ef7b547980998d1`.

The accepted eighteen-file Phase 0 candidate remains `7d2e5fcaff591641b5cefce00e71e88941dd1f95`, interpreted through approval revision 1.1. W02 does not change any specification, that approval record, the Phase 1 plan, W01 licensing files or the baseline manifest.

## 2. W02 delivered scope

The candidate changes only the section 6 allowlist: 48 explicitly named Python package files; pyproject.toml, MANIFEST.in and requirements-dev.txt; the four named tests/scaffold files; scaffold/toolchain_review.md; and this progress file. This is 57 paths, consisting of 55 new paths and the two allowed progress/toolchain updates.

The package name is source-integrity-toolkit, import name source_integrity_toolkit and unreleased scaffold version 0.1.0.dev0. Package initializers and future domain/native modules are import-safe slots. Forty-four Python files contain only an explanatory docstring and copyright/license comments. The remaining four contain the package exports, two immediate-refusal API functions, fixed CLI help/version/refusal and the literal scaffold version.

`audit_bundle` and `audit_file` immediately raise NotImplementedError without inspecting arguments, options or paths. The CLI displays tool-authored help/version or emits a fixed refusal with exit 1. It does not parse the future audit grammar, validate a dossier, call the API to inspect evidence, create a report or emit sit-report/0.1 states. Unknown switches and argument text are not echoed. Exit 1 is explicitly the temporary scaffold refusal.

No executable schema, static trace/obligation catalog, hero fixture, domain test, native binding or CI workflow is added. Those belong to later work units. No analytical obligation has been marked implemented or tested.

## 3. Packaging selection and actual checks

The source archive selection names individual project files rather than including all repository data. LICENSE and NOTICE are included unchanged. Wheel package-data discovery is disabled, and both artifact inventories are checked for exact membership. Normative specifications remain in the repository and are not relabeled as package output.

The local build view was assembled from new candidate files and connector-read README/NOTICE plus an identical copy of the standard Apache text. All three unchanged packaging inputs were checked against their repository Git blobs and byte counts. This is a controlled packaging view, not a claim that a full remote git clone succeeded. Frozen-file preservation is separately checked through remote tree/diff identity.

Actual supplemental run:

```text
PYTHONPATH=src PYTEST_DISABLE_PLUGIN_AUTOLOAD=1 PYTHONDONTWRITEBYTECODE=1 python -m pytest tests/scaffold -q
```

The exact executed command additionally set an external temporary directory and an external JUnit output path. It did not add logs, wheels or temporary environments to the repository. The final suite collected 78 checks: **77 passed, 1 failed, 0 skipped, 0 errors**.

| Check group | Actual result and scope |
|---|---|
| 48 module imports | Passed under local CPython 3.13.5 |
| Inert slot/file-set and guarded fresh imports | Passed; no application I/O, mutation, network/process activity or native binding observed in these cases |
| API signatures and hostile arguments | Passed; immediate refusal, unchanged input, no path access or output creation |
| CLI help/version and malformed/ordinary audit requests | Passed; fixed messages, no payload echo or report creation |
| Declared metadata and runtime dependencies | Passed; selected pins unchanged, project Requires-Dist empty |
| Source/wheel inventory and exclusion canaries | Passed using the available older backend; no excluded material packaged |
| Clean runtime installation | Passed for the supplemental wheel; target contained only the project distribution |
| Source-archive rebuild | Passed; same wheel member names and contents |
| Selected build/test versions installed | FAILED: actual setuptools 82.0.1 / pytest 9.0.2 versus selected 84.0.0 / 9.1.1 |

The source archive has 65 regular files; the wheel has 55 members. Supplemental archive identities are:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| source_integrity_toolkit-0.1.0.dev0.tar.gz | 21833 | `9fccf8738ffe2d45b227729cc96b734983b950dc345d635c9e9790e398c3c078` |
| source_integrity_toolkit-0.1.0.dev0-py3-none-any.whl | 34573 | `83db3bba949795bb188b2599c5c6f3f0729d8d1984086828e23058bcdd6622a3` |

These identify local supplemental test artifacts, not published releases. Byte-reproducible ZIP containers are not claimed; the rebuild compared member bytes.

## 4. Failures, repairs and unresolved gate

The initial packaging check did not account for the backend-generated setup.cfg. Its actual content was inspected and compared with the selected upstream backend's documented source behavior. The test now permits only the fixed egg_info tag metadata. No setup.cfg is added to the repository and no executable build hook is invented.

A subsequent canary scan matched the canary's own literal in its test source. That false positive was corrected by assembling the fictional sentinel from separate literals. The exclusion assertion remains active. Both local failure records are retained in the handoff evidence.

The remaining failed check is not repaired by changing expectations. The local execution environment cannot resolve/download the selected packages, while connected GitHub reads/writes and external release-metadata checks work through different paths. The build/test declarations retain setuptools 84.0.0 and pytest 9.1.1. Tests with the older preinstalled tools provide supplemental compatibility evidence only. Their direct backend invocation does not resolve build-system.requires and cannot satisfy the declared environment gate.

The selected tools' isolated installation, actual downloaded-artifact/transitive review and exact-version test run remain pending. scaffold/toolchain_review.md records the rechecked upstream extraction-safety note and its limitations. No developer tool is promoted to an application runtime dependency.

## 5. Environment and execution boundary

Observed authoring environment: CPython 3.13.5, Linux x86_64/glibc 2.41, setuptools 82.0.1, pytest 9.0.2, pip 25.1.1, iniconfig 2.3.0, packaging 25.0, pluggy 1.6.0 and Pygments 2.20.0. Pytest external plugin autoload was disabled. A separate clean runtime venv was created without pip/setuptools/pytest and populated offline with the self-built project wheel using the existing installer.

No selected-version download/installation, Windows run, minimum-version CPython 3.11 run, hosted CI, native platform conformance, production analytics or package publication is claimed. The attached theory papers were not copied into this repository or used to change its frozen requirements.

## 6. Delivery and next gate

The W02 candidate is submitted as a draft PR against the merged main baseline. The actual candidate commit and PR identifiers are recorded by GitHub and the external verification handoff after they exist, avoiding self-referential hashes in this file. Only the W02 branch receives these changes; main retains the accepted W01 merge.

W02 remains BLOCKED_AT_SELECTED_TOOLCHAIN_VERIFICATION. The narrow remaining work is to obtain/install the already selected tools in an authorized network-capable environment, inspect the resolved dependencies/artifacts, rerun the suite including its strict version assertion, and review the resulting diff/evidence. The failed assertion must not be skipped or relaxed. A new execution service or early CI path would require the applicable separate authorization; this candidate adds neither.

Do not merge this draft, mark W02 complete, or enter W03 until that gate and owner acceptance are satisfied. The original software, privacy, license and phase boundaries remain intact.
