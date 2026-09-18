# P1-W06 CI Toolchain Review

## Current record

| Field | Value |
|---|---|
| Revision | 0.3, authorized R01 rerun |
| Date | 2026-09-18 UTC |
| Repair authority | Owner approved P1-W06-R01 with `批准` |
| Tested executable candidate | `641f2b9711aad9812a0c709eb949798a4f4ebee7` |
| Inspected run | `35363039474`, attempt 1 |
| Result | Linux rows pass; one Windows-only native-canary test remains failed on each Windows row |
| PR / merge | Draft PR #7; not merged |
| Product dependencies / analysis | None / unimplemented |

## 1. Preserved toolchain review

The complete revision 0.2 at commit `8ea5becfe11165e745bec72b5f42e467fa92c69f`, this path, remains the unchanged toolchain selection, permissions, license, source-reference and initial failure record. The earlier W02 vendored-material and archive_util applicability qualifications also remain controlling. This successor adds execution evidence; it selects no new tool, runtime, dependency, license or platform.

The retained action pins are checkout v7.0.1 at `3d3c42e5aac5ba805825da76410c181273ba90b1`, setup-python v7.0.0 at `5fda3b95a4ea91299a34e894583c3862153e4b97`, and upload-artifact v7.0.1 at `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a`. All target Node 24; their reviewed root licenses are MIT. Original action manifest/notice identities and source links remain in revision 0.2.

The workflow and evidence driver are unchanged by R01: contents-read permission, exact-head checkout without persisted credentials, finite 25-minute jobs, no cache input, privileged trigger, configured secret, package publication, deployment or merge. Only verification JSON/XML/logs are uploaded for fourteen-day retention. Setup network activity remains separate from application no-network tests. A skipped old W02 workflow is not a passing W06 job.

## 2. Actual rerun environments and dependency boundary

The exact four environments in run `35363039474` are Ubuntu 24.04.5 with CPython 3.11.16 and 3.13.15, plus Windows Server 2025 build 26100 with CPython 3.11.9 and 3.13.15. These are actual installed patches, not claims that they are the newest security releases. They test the scaffold, not the future Windows 11/NTFS native design.

Every row verified and installed the unchanged selected wheels: setuptools 84.0.0, pytest 9.1.1, iniconfig 2.3.0, packaging 25.0, pluggy 1.6.0 and Pygments 2.20.0; Windows also installed its preselected Colorama 0.4.6. Requirements blob remains `e037242d849f827a6c968a0f97830610a1718138`. Bootstrap pip was 24.0 on the 3.11 rows and 26.2.1 on the 3.13 rows, separate from the product. No pin was lowered, added or removed.

The four downloaded evidence archives were fully SHA-256 checked against Actions metadata, then their environment, reviewed-wheel, install, collection, pytest, JUnit, guard and build records inspected. Complete artifact IDs and hashes are in PHASE_1_PROGRESS.md section 4. The actual 65-member source distributions and 55-member wheels passed all package tests on both operating systems, including exact platform-specific generated setup.cfg bytes. Clean offline installations contain only the project; rebuild checks preserve wheel member bytes. No developer wheel or product package binary was published.

## 3. Repairs and test outcomes

R01 modifies only the previously approved two test files. The isolated observer now explicitly preloads importlib.util and the IDNA hostname codec before interception. Its observer body and all adverse operations remain unchanged. Its clean-interpreter regression checks both explicit dependencies. The packaging repair accepts only the precise generated file for the current platform and adds exact positive/negative controls without transforming source bytes.

Run `35362756160` preserves the intermediate R01 failure: the cache-helper repair exposed IDNA's deferred file load before the DNS audit event; Windows also exposed the None native-canary issue below. The IDNA preload was completed inside the same authorized initialization repair. Its source inspection and isolated reproduction are retained locally and in progress revision 0.13.

Run `35363039474` collected 194 top-level instances per row, with 420 separate successful subtest events. Linux reports 194 passed/0 failed on both Python minors. Windows reports 193 passed/1 failed on both minors. All rows have zero errors/skips, matching collection identities, unchanged tracked bytes, and passing before/after twenty-file baseline and forty-eight-module guards. Every packaging test, all socket/DNS controls, and the additional R01 regressions pass.

The only remaining failure is `test_deliberate_cdll_is_blocked_before_loading` in the unchanged `tests/security/test_scaffold_no_native_loading.py`. Its None argument fails Windows' argument handling before a real ctypes.dlopen audit event. The other named-library canary passes. Do not count absence of an event caused by invalid arguments as successful interception.

## 4. Narrow primary-source verification and next gate

Python 3.11 importlib documentation identifies source_from_cache in the importlib.util submodule. Python's open documentation explains platform newline translation for text output. These support the repair mechanics; actual acceptance still comes from the executed cases.

- `https://docs.python.org/3.11/library/importlib.html#importlib.util.source_from_cache`
- `https://docs.python.org/3.11/library/functions.html#open`
- `https://docs.python.org/3.13/library/ctypes.html`

The remaining failure was checked against CPython's exact primary implementations: tag v3.11.9, Lib/ctypes/__init__.py; tag v3.13.15, Lib/ctypes/__init__.py and Modules/_ctypes/callproc.c. Their concrete blobs and the before-audit argument checks are recorded in progress section 3. No third-party implementation was copied.

P1-W06-R02 proposes permission for one additional earlier test file to use a valid fixed fictional library-name argument on Windows while retaining the POSIX None case and mandatory actual-event assertion. The file remains unchanged pending approval. All matrix rows must then rerun. These findings provide no permission to weaken the observer, skip Windows, report a green CI result, merge W06 or begin W07.
