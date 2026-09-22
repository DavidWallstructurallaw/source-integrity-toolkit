# Phase 3 progress

W08 was accepted through the owner's continuation instruction and PR #27 merged at `c25c827b9c0c2cf84075c79ebbf6c238dee4ca74`, with reviewed tree `f465bc0ba24b7ceb3ae513705ff61de710ee2c70` unchanged.

W09 implements M009 attributed boundary externality and M010 independent stage observations, exact finite-cohort partitions/fractions/completion intervals, and restricted same-population transitions. Direct verification passed 26 presence and 59 cohort tests on the final source. The final limited internal code review closed the identified source-binding and time-scope defects; it is not independent external certification.

Code `59a25116bfe5fe8f4f9b407852bb29fa692e542d`, tree `199651e190be5357e74b7280ac0437366d8afb41`, was submitted as draft PR #28 within the exact seven authorized paths. All 3,464 W08 test identities are retained; W09 adds 85 identities for 3,549 total. CI run `35779540524`, attempt 1, completed with three successful profiles: Ubuntu 24.04 / CPython 3.11 and 3.13, and Windows Server 2025 / CPython 3.11. Each passed 3,549 tests and 428 separately reported subtests, with zero failures, errors or skips.

Windows Server 2025 / CPython 3.13 exceeded the existing 1,200-second full-pytest subprocess limit. Its original test-failure record and job log identify `TimeoutExpired`. The ZIP has no junit.xml, pytest.log or pytest-exit.json, so its passed tests and subtests cannot be counted. This is an incomplete fourth result and the required matrix gate is failed. All four original ZIPs match service digests/sizes and CRC; their 187 source files before and after match the submitted code. Full raw-gate failure is preserved.

No W09 core row is promoted. All 228 field-row objects remain identical to accepted W08: 136 verified cores, 92 pending cores, and all integration/release obligations pending. The 36 W09 target cores remain pending. Public API/CLI auditing, reporting and complete private orchestration remain future work.

P3-W09-R01 is proposed, with approval pending: raise the full-pytest subprocess limit from 1,200 to 1,800 seconds and the workflow job limit from 25 to 40 minutes, together with exact current/historical control adaptations in the same three proposed additional paths. These are tests/scaffold/test_ci_contract.py, tests/contract/test_phase3_transition.py and .github/workflows/phase1-ci.yml. All semantic tests, four profiles, pins, product budgets and no-skip rules remain required. The current seven-path authority is unchanged; no out-of-scope repair is applied.

This blocked checkpoint changes only progress and the two evidence/coverage records. Its affected existing controls and exact 184-blob preservation check are recorded separately after execution. W09 remains unaccepted, PR #28 remains draft, and W10 is not authorized or started.
