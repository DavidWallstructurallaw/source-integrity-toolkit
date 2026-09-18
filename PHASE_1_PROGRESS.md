# PHASE_1_PROGRESS

## Current control record

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Revision | 0.13, P1-W06-R01 results and remaining Windows canary |
| Date | 2026-09-18 UTC |
| Owner repair approval | `批准`, responding to P1-W06-R01 |
| Approved plan | Revision 0.1, blob `27ed33cb1c2afc78b12ca099ee7ccb4e68d63bfb` |
| W05 merge / unchanged main | `ecf4eb5126201a7c31250c6dae8cbe2c64f9066a` |
| Repaired executable candidate | `641f2b9711aad9812a0c709eb949798a4f4ebee7` |
| Inspected hosted run | `35363039474`, attempt 1 |
| Branch / PR | `phase1/p1-w06`, draft PR #7 |
| W06 status | BLOCKED on one previously masked Windows-only test-canary defect |
| W06 acceptance / merge | Not issued / not performed |
| P1-W07 and Phase 2 | Not authorized or executed |

## 1. Authority, repairs and history

The owner approved exactly the two earlier-unit test repairs described by P1-W06-R01, plus necessary W06 records and a four-row rerun. The seven-path W06 scope consists of its original five allowed files and `tests/security/test_scaffold_inertness.py` plus `tests/scaffold/test_packaging.py`. No third earlier-unit test is implicitly authorized.

The full first-run record and original review remain at `8ea5becfe11165e745bec72b5f42e467fa92c69f`. The approved-repair intake, initial exact-byte identities and local regression account remain at `a8741ed71317cfdb47c7554fd267624334e901a6`, progress revision 0.12. Those histories are retained rather than relabeled as successful.

R01-A now preloads both `importlib.util` and `encodings.idna` inside the isolated probe, before request processing and interception. The first fixes the cache-helper initialization failure; the second completes the same preloading boundary for the existing DNS canary. No observation rule, native/network exception or product code is changed. The added clean `-I -S -B` regression inspects the actual preamble and exercises both helpers.

The first R01 run `35362756160` checked `a8741ed`: all four jobs failed. Downloaded, hash-matched Linux 3.13 evidence showed 193 passed/1 failed, and Windows 3.13 evidence showed 192 passed/2 failed. The DNS canary was stopped by the observer's file-read rule while the standard library tried to load IDNA, before the DNS event. An isolated local reproduction showed `open` before preloading and `socket.getaddrinfo` after preloading; both operations were intercepted before source access/resolution. The follow-up at `641f2b9` added only the explicit codec preload and its regression checks inside the same authorized file. The original DNS test file and assertion stayed unchanged.

R01-B checks only backend-generated setup.cfg against exact POSIX LF or Windows CRLF bytes. It does not normalize supplied bytes, change any source-file line endings, broaden archive membership or change backend versions. Five new instances retain positive spellings and reject an unreviewed platform plus nine extra/malformed-content variants per platform. All pre-existing package inspection, clean install and rebuild tests remain.

## 2. Actual repaired matrix

Run `35363039474`, attempt 1, executed the exact repaired candidate. All four job statuses, complete evidence ZIPs, their SHA-256 identities and JSON/XML/log contents were inspected.

| Hosted profile | Actual Python | Collected | Passed | Failed | Errors / skipped |
|---|---|---:|---:|---:|---|
| Ubuntu 24.04.5 | 3.11.16 | 194 | 194 | 0 | 0 / 0 |
| Ubuntu 24.04.5 | 3.13.15 | 194 | 194 | 0 | 0 / 0 |
| Windows Server 2025 build 26100 | 3.11.9 | 194 | 193 | 1 | 0 / 0 |
| Windows Server 2025 build 26100 | 3.13.15 | 194 | 193 | 1 | 0 / 0 |

Each row has 420 additional successful subtest events, retained separately from the 194 collected top-level instances. Collection identities match all results. There is no xfail, deselection or test skip in this hosted run. Both Linux jobs completed successfully; both Windows jobs failed on the same one test below.

All four rows passed the actual twenty-file baseline and forty-eight-module guards before and after testing; tracked bytes were unchanged. All packaging tests now pass on every row, including the previously failing Windows source-inventory test, source/wheel exclusions, clean offline installation without developer dependencies and source-rebuild member-byte equality. Existing source distribution and wheel member inventories remain 65 and 55. The development pins and Windows-only Colorama marker are unchanged.

The original twelve security methods now pass on Linux. On Windows, eleven pass, including real inert imports, all DNS/socket probes, file/path probes and the separately named-library native probe. The remaining method has reached a Windows-specific canary construction problem that the earlier initialization failure had masked.

## 3. Remaining issue: P1-W06-R02, proposed only

File: `tests/security/test_scaffold_no_native_loading.py`.
Method: `test_deliberate_cdll_is_blocked_before_loading`.

The method injects `ctypes.CDLL(None)` and requires the real `ctypes.dlopen` audit event. Both Windows rows fail because their violation list is empty. CPython 3.11.9's ctypes Python wrapper tests path separators in the name before the loader; None is not a valid string there. In CPython 3.13.15, the Windows C wrapper requires a Unicode argument via `PyArg_ParseTuple(..., "U|i:LoadLibrary", ...)` before `PySys_Audit("ctypes.dlopen", ...)`. Neither path reaches the expected audit event with this argument. These primary implementations explain the observed failure; this is a test-canary portability defect, not evidence that a product library load escaped interception.

Sources checked: `python/cpython` tag `v3.11.9`, `Lib/ctypes/__init__.py` blob `26135ad96296acc6aeda25d8b686f780e0b9e2c4`; tag `v3.13.15`, `Lib/ctypes/__init__.py` blob `7fc1181f25a26430d74044d114afd87be1df3d47`; and `Modules/_ctypes/callproc.c` blob `066cbb99bdd758fe4a91f4b1f70c237178ecfe4a`. No source code from those projects is incorporated into the toolkit.

Recommended scoped repair: permit this one additional test file to use a fixed fictional string library name on Windows, retaining None on POSIX, with the same mandatory actual-event assertion and adverse controls. Never accept a generic TypeError, empty event list or skipped test as proof of interception. Keep the other slot's named-library probe and all existing boundary assertions. No native library should actually be loaded by the probe.

This file is outside R01's exact two-file scope and remains unmodified. P1-W06-R02 requests permission for that targeted canary repair and necessary W06 records, followed by the complete four-row rerun. It does not authorize another module, product implementation, changed dependency, source oracle, W06 merge or W07.

## 4. Evidence identities

| Row | Job ID | Artifact ID | Complete ZIP SHA-256 |
|---|---:|---:|---|
| Ubuntu / 3.11 | 105658728693 | 10555032250 | `bb592ea04d4a1e9951195c4f95aa1a7bfc28c57d4aa9dc07f36b19f71d9205ff` |
| Ubuntu / 3.13 | 105658728963 | 10555158354 | `ddbcaa1477618efa796ef37622587b51ab2cfac47ae83f85416e7a20e5f2a4c2` |
| Windows / 3.11 | 105658728899 | 10555533189 | `0501b3a572065a11f8d52a56a92e45923ca7512aff02546d42402f834f620455` |
| Windows / 3.13 | 105658728999 | 10555048397 | `d930a89ed746fcd53ad87e5efcc1cb807356b829302c4f61f411d6def14bcb92` |

Run URL: `https://github.com/DavidWallstructurallaw/source-integrity-toolkit/actions/runs/35363039474`.

Final repaired security blob: `a7a876006eb75ab5c3542e01f4b72c8a7483519f`, SHA-256 `cd741cf4bde1192b63d6c3951022bdab08dabf7b4fe4bfaf3ed8dba1e2960b3d`. Repaired packaging blob: `c872c4080d08e331b9253cd3cdd9467050d540a4`, SHA-256 `cfc891098830d9adf1f2ee3a0c3bcc06e884fb00f356aa5a8e1822feb1aa5d93`. All original observer/application boundary code and pre-existing functions apart from the targeted metadata assertion were compared locally and preserved.

## 5. Preservation and stop point

This evidence-record successor changes only progress, the CI review and the README status text. The table describes its named executed predecessor; it does not invent results for a later commit. Current-head checks remain independently visible in PR #7.

Frozen specifications, approval, plan, baseline manifest, all product modules, case/oracle data, catalogs, dependency pins, packaging rules, other earlier tests and workflow/helper bytes remain unchanged. Historical source papers are not reinterpreted. No application algorithm, parser, report renderer or native adapter is implemented.

Keep PR #7 in draft and main at the accepted W05 merge. R01's permitted repairs have been executed and tested; full W06 acceptance remains blocked by the unmodified R02 canary. The next required decision concerns that single additional file, not a new design or a rerun of earlier approvals.
