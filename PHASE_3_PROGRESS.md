# Phase 3 progress

W08 was accepted and PR #27 merged at `c25c827b9c0c2cf84075c79ebbf6c238dee4ca74`. Its immutable review evidence retains the original scope and limitations.

W09 implements M009 boundary-qualified externality and M010 separate stage observations, finite-cohort partitions/fractions/completion intervals, and restricted same-population transitions. Final direct tests passed 26 presence and 59 cohort cases. Product source and these two semantic test files are frozen during the CI time repair.

Original code `59a25116bfe5fe8f4f9b407852bb29fa692e542d` ran CI `35779540524`, attempt 1. Ubuntu 3.11, Ubuntu 3.13 and Windows 3.11 each passed 3,549 tests and 428 separately reported subtests. Windows 3.13 hit the existing 1,200-second full-pytest subprocess limit and produced no complete JUnit/pytest result. All original ZIPs, full service metadata and the failed job log are preserved; that matrix remains failed.

The owner explicitly approved P3-W09-R01 with `批准 P3-W09-R01`. The fixed preapproval checkpoint is `5bccceee13995f7ee51ed44339d596aadb309644`, tree `012e520e14977a3ee6a6a1ab143799cfa87ca18a`, sole parent the original code above. Both original W09 commits retain their seven-path scope. Only descendants of that fixed checkpoint receive the three added CI paths, making ten W09 paths. Other units retain their immediate scopes.

The repair raises full-pytest execution from 1,200 to 1,800 seconds and each workflow job from 25 to 40 minutes. It adapts only existing current/historical workflow, scope and source controls in tests/scaffold/test_ci_contract.py, tests/contract/test_phase3_transition.py and .github/workflows/phase1-ci.yml. No product budget, semantic assertion, dependency/action pin, matrix profile, skip rule or test identity is removed or weakened. Zero governance test identities are added.

The authorized repair passed 331 existing affected transition/workflow controls. Complete collection retains the exact same 3,549 test identities, with zero additions or removals. The revised four-profile matrix remains pending. All 228 field-row objects remain unchanged from accepted W08: 136 verified cores, 92 pending cores, including all 36 W09 target cores; every integration and release obligation remains pending. The repaired code requires its own complete four-profile evidence. Public auditing/reporting and full private orchestration remain future work. W09 awaits later acceptance; W10 is not authorized or started.
