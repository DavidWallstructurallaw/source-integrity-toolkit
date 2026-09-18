# P1-W06 CI Toolchain Review

## Current record

| Field | Value |
|---|---|
| Revision | 0.4, R02 four-row passing evidence |
| Date | 2026-09-18 UTC |
| Repair authority | Owner approved P1-W06-R02 with `批准` |
| Tested executable candidate | `e102b7f31427f5a0dce288517284eaf4e3a6a7dd` |
| Inspected run | `35365045308`, attempt 1 |
| Technical result | Four successful jobs; 194 passed per row; zero failures/errors/skips |
| PR / merge | PR #7 awaiting owner acceptance; not merged |
| Product dependencies / analysis | None / unimplemented |

## 1. Preserved selections and review scope

Full selection/permission/license/source review revision 0.2 remains at `8ea5becfe11165e745bec72b5f42e467fa92c69f`, this path. R01 evidence and the verified Windows canary diagnosis remain in revision 0.3 at `c6d8969d8b82d86900fbd36c6d657538f47af35a`. The earlier W02 vendored-material and archive_util qualifications are also retained. This revision supplies new execution evidence without adopting another dependency, action, native capability, license or production platform.

The unchanged action pins are checkout v7.0.1 at `3d3c42e5aac5ba805825da76410c181273ba90b1`, setup-python v7.0.0 at `5fda3b95a4ea91299a34e894583c3862153e4b97`, and upload-artifact v7.0.1 at `043fb46d1a93c77aae656e7c1c64a875d1fc6a0a`. Their reviewed manifest and notice identities remain in revision 0.2.

The workflow/helper remains unchanged by R02: contents-read permission, exact-head checkout without saved credentials, four finite 25-minute jobs, no cache, privileged trigger, configured repository secret, package publication, deployment or automatic merge. Uploads contain only verification JSON/XML/log records with fourteen-day retention. Dependency acquisition is CI setup; application-originated network/native effects remain prohibited by the scaffold tests.

## 2. Actual environments and pins

The passing run used Ubuntu 24.04 x64 image 20260907.300.1 with CPython 3.11.16/3.13.15, and Windows Server 2025 x64 image 20260907.229.1 with CPython 3.11.9/3.13.15. The evidence reports the actual kernel/build, interpreter and patch string. No claim is made that these are the newest releases or that hosted scaffold tests certify the future Windows 11/NTFS adapter.

Every row verified and installed the same six selected developer wheels: setuptools 84.0.0, pytest 9.1.1, iniconfig 2.3.0, packaging 25.0, pluggy 1.6.0 and Pygments 2.20.0. Windows also installed the already approved Colorama 0.4.6 marker. Requirements blob remains `e037242d849f827a6c968a0f97830610a1718138`. Actual wheel identities, metadata and notice hashes remain in each reviewed-wheels.json. Bootstrap pip is an environment tool, not a toolkit runtime dependency.

All selected-wheel verification, offline installation and pip check stages passed. The installed project has zero third-party runtime dependencies. R02 does not change pyproject.toml, MANIFEST.in, dependency pins or the archive member allowlists.

## 3. Narrow repair and evidence

R02 changes only the argument used by one existing native-loading canary: Windows receives a fixed fictional string name, while POSIX retains None. Its module slot, every assertion, other native controls and shared interception rules are retained. An actual `ctypes.dlopen` event is still mandatory, so ordinary argument failure or an empty interception list cannot pass.

The inspected CPython implementations and pre-audit argument boundary are preserved in progress revision 0.13. Python's ctypes documentation identifies the named-library audit event: `https://docs.python.org/3.13/library/ctypes.html`. This documentation supports the event contract; actual acceptance comes from the executed positive and adverse probes. No third-party code is copied and no native adapter is implemented.

The local patch check matched the fetched blob, compiled the file, compared all retained method/assertion ASTs and checked fixed argument selection. It did not substitute a simulated Windows result for the hosted run. No collected test was added or removed by R02.

## 4. Passing matrix and artifact verification

Run `35365045308` executed `e102b7f31427f5a0dce288517284eaf4e3a6a7dd`. Each of its four jobs collected and passed the same 194 test instances, with zero failures, errors or skips. The 420 successful subtest events are recorded separately; 614 JUnit events do not become 614 collected functions. All original R01 collection identities remain present, including the three native methods and the strict platform-specific generated setup.cfg check.

All rows passed both actual-checkout guards before/after, preserved tracked bytes, and passed every packaging/clean-install/rebuild test. Source inventories contain 65 regular files; each original/rebuilt wheel has 55 members with equal member-content hashes. A successful scaffold build does not implement source analysis or certify native filesystem behavior.

All four complete ZIPs were downloaded and checked against Actions byte counts and full SHA-256 digests. Their environment, collection, JUnit, pytest, guard, reviewed/installed-wheel and archive records were inspected independently of the displayed green job state. Exact job/artifact IDs and hashes are in PHASE_1_PROGRESS.md section 4. No package binary, source dossier, theory PDF or secret dump is uploaded.

## 5. Handoff

Historical failed runs remain recorded and unmodified. Both scoped repairs R01 and R02 now have passing four-row evidence. The documentation-only review successor requires an exact-head CI recheck, recorded in PR #7 and the verification export; it cannot inherit an unobserved green result solely from equal executable bytes.

W06 technical verification and owner acceptance remain distinct. PR #7 is not merged, main remains at `ecf4eb5126201a7c31250c6dae8cbe2c64f9066a`, and W07/Phase 2 are not started. Future native ABI, security-race and analytical validations remain pending their own implementation plans.
