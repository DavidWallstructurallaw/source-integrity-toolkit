# PHASE_1_PROGRESS

## Current control record

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Revision | 0.14, P1-W06-R02 complete matrix verification |
| Date | 2026-09-18 UTC |
| Owner repair approval | `批准`, responding to the single-file P1-W06-R02 request |
| Approved plan | Revision 0.1, blob `27ed33cb1c2afc78b12ca099ee7ccb4e68d63bfb` |
| W05 merge / unchanged main | `ecf4eb5126201a7c31250c6dae8cbe2c64f9066a` |
| R02 intake | `c6d8969d8b82d86900fbd36c6d657538f47af35a` |
| Repaired executable candidate | `e102b7f31427f5a0dce288517284eaf4e3a6a7dd` |
| Inspected passing run | `35365045308`, attempt 1 |
| Branch / PR | `phase1/p1-w06`, PR #7 |
| W06 technical status | Four-row matrix PASS on the named repaired candidate; final review-head checks recorded separately in PR #7 |
| W06 owner acceptance / merge | Pending / not performed |
| P1-W07 and Phase 2 | Not authorized or executed |

## 1. Authority and closed scope

The owner approved P1-W06-R02 after the R01 handoff identified the remaining Windows canary failure. The additional authority covers only `tests/security/test_scaffold_no_native_loading.py`, necessary existing W06 evidence/status records, and the complete four-row rerun. It does not authorize product implementation, another earlier test repair, merger or W07.

The full W06 PR now has eight permitted paths: its original workflow, CI review, CI policy/evidence helper, README and progress record; the two R01 test files; and the single R02 test file. This R02 pass changes the latter test and three documentation records only. No further test, workflow/helper, product module, dependency pin, packaging rule, fixture/oracle, catalog, license, approved plan or frozen specification changes.

## 2. Exact R02 repair

The existing `test_deliberate_cdll_is_blocked_before_loading` now selects the fixed string `SYNTHETIC_NONEXISTENT_LIBRARY` as its CDLL argument on Windows. Other platforms retain None. The probe remains injected into `io/platform_linux.py`, because all package slots must remain inert on every tested host, irrespective of a slot's prospective platform role.

The three original native-test methods and every original assertion are unchanged. In particular, the canary must fail as an application operation and retain an actual `ctypes.dlopen` entry. A TypeError, missing event or skipped test cannot satisfy it. The other-slot named-library control remains intact. No actual native loading is granted and the shared observer is unchanged by R02.

The fetched input blob was `7f80974968f5636b4f6aa87d4efc8c13d9bc834c`, SHA-256 `3875064a1222480e2ee1611fcbef033099887cfb43e0a9684ce9425aa355e5b6`. The committed repaired blob is `69d06755fa425d8508369b744277b2f47e4694af`, SHA-256 `add4a523f73deba8380a257a1846d8c044249996ec88ca56be1f4903563a96a6`.

Local checks established matching input bytes, Python syntax, unchanged methods/assertions and the fixed Windows/POSIX argument selection. They did not pretend to execute Windows locally. Acceptance evidence is the actual hosted matrix below. R02 adds no collected test and removes none.

## 3. Complete passing matrix

Run `35365045308`, attempt 1, executed commit `e102b7f31427f5a0dce288517284eaf4e3a6a7dd`. All four jobs completed successfully. Their complete evidence ZIPs were downloaded through the connector and matched against Actions byte counts and SHA-256 digests before inspection.

| Hosted profile | Actual Python | Collected / passed | Failed | Errors / skipped |
|---|---|---:|---:|---|
| Ubuntu 24.04 x64, image 20260907.300.1 | 3.11.16 | 194 / 194 | 0 | 0 / 0 |
| Ubuntu 24.04 x64, image 20260907.300.1 | 3.13.15 | 194 / 194 | 0 | 0 / 0 |
| Windows Server 2025 x64, image 20260907.229.1 | 3.11.9 | 194 / 194 | 0 | 0 / 0 |
| Windows Server 2025 x64, image 20260907.229.1 | 3.13.15 | 194 / 194 | 0 | 0 / 0 |

Each row additionally reports 420 successful subtest events. The JUnit aggregate is 614 events, containing 194 top-level result elements. Local evidence inspection independently matched every result identity to collection, confirmed the same 194 collected IDs as the R01 run, checked zero failures/errors/skips and pytest exit zero, and verified all three native methods passed. Subtests do not become additional domain-test implementations.

All four rows passed the actual twenty-file baseline and forty-eight-module guards before and after execution. Tracked bytes remained unchanged during testing. The pinned developer wheels and existing Windows Colorama marker were verified and installed without adding runtime dependencies. All packaging tests passed: exact 65-regular-member source inventory, 55-member wheel, exclusion checks, clean offline installation without developer dependencies, and equal member bytes in the original and source-rebuilt wheels.

The existing API refusal, import, CLI, file/path, DNS/socket, native-loading, architecture, catalog, fixture and CI-policy checks are included. There is no test skip, xfail, deselection, reduced matrix or accepted generic exception. These are scaffold checks, not an implementation of the 228 pending analytical test obligations or the future native adapters.

## 4. Downloaded evidence identities

| Row | Job ID | Artifact ID | ZIP bytes | Complete ZIP SHA-256 |
|---|---:|---:|---:|---|
| Ubuntu / 3.11 | 105665328413 | 10556316686 | 36945 | `07d826b768d5f1dadf186e6277055a3bfa091862c636a144a3ba8efac14666b3` |
| Ubuntu / 3.13 | 105665328371 | 10555379689 | 36791 | `0c7b4e53fba727520501db9ca610fc7ea9e06dfc4aa92536341ff54b212d84cb` |
| Windows / 3.11 | 105665328541 | 10555707419 | 43125 | `dbdc8d09459e3fd427153bd6b9db0c769136ad727f3a9c3124470d17bcdef8bb` |
| Windows / 3.13 | 105665328095 | 10555962094 | 42916 | `4a78be1202842cfc29491d9e8d973ffdf964902883ad784fada922aee603dce1` |

Run URL: `https://github.com/DavidWallstructurallaw/source-integrity-toolkit/actions/runs/35365045308`.

The JSON/XML/log inspection includes environment and commit identity, collection, pytest exit, suite and element counts, before/after guards, reviewed/installed wheels, tracked hashes and archive member hashes. Hosted image/patch details are observed environments, not a newest-release or production-support claim.

## 5. Retained failure history

The complete earlier progress revision 0.13 is preserved at `c6d8969d8b82d86900fbd36c6d657538f47af35a`, this path. It retains the R01 authority, intermediate results, exact CPython source verification and the R02 proposal before approval. Earlier revisions remain reachable through its pinned history.

| Historical run | Outcome retained |
|---|---|
| 35357942013 | Initial W06 matrix failed; isolated-probe initialization, Windows generated newline and summary-accounting defects exposed |
| 35358820107 | Accounting corrected, but twelve Linux and thirteen Windows failures remained |
| 35362756160 | Initial R01 repair exposed deferred IDNA initialization and the Windows None canary |
| 35363039474 | R01 complete; Linux 194/194, Windows 193/194, with only the R02 canary still failing |
| 35365045308 | R02 repaired; all four rows 194/194 |

No previous failure is erased, relabeled or credited to later code. R01's preload and strict generated-metadata repairs remain unchanged. The separate old W02 workflow stays limited to its original scope; its skip on a W06 PR is not counted as W06 evidence.

## 6. Delivery gate

This documentation successor updates only progress, CI review and README after the named passing executable run. It must receive its own passing exact-head checks before delivery; that final commit/run pairing is recorded in PR #7 and the exported verification summary rather than creating a self-referential commit hash in this file.

W06 technical verification is complete on the named candidate. Owner acceptance and merging PR #7 remain separate, unperformed actions. Main stays at the accepted W05 merge. No P1-W07 completion file, Phase 2 work, actual auditing, report generation, native security implementation, package release or deployment is introduced.
