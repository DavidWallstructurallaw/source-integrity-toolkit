# Source Integrity Toolkit

A local, supplied-evidence toolkit for examining source lineage, evidence independence, external presence and corrective capacity in AI-native information systems.

**Status: P3-W15 private-core handoff, with approved R01 reason repair, R02 history-verification optimization and R03 complete-CI budget amendment implemented. The final hosted gate and owner acceptance remain pending; Phase 3 is not accepted. Public auditing remains unavailable.** The package remains installable as `0.1.0.dev0`. The private core implements fifteen analytical families in the planned twenty-nine active modules; nineteen protected modules retain their accepted bytes. Public audit calls raise `NotImplementedError`; CLI auditing refuses with exit 1 without reading dossiers or producing reports.


## Intended purpose

The planned v0.1 auditor consumes a caller-prepared local JSON dossier containing claims, evidence, origin and transformation records, evaluator relationships and correction history. It distinguishes supplied assertions, supported structural deductions and unresolved information. Different material counts and evidence roles remain distinct. Missing ancestry cannot become an independent source, and a structurally consistent dossier cannot certify its own authenticity.

The adopted scope provides a multidimensional evidence profile. It excludes a universal truth or integrity score, live crawling, hidden-lineage discovery, an LLM judge, automatic source sanctions and automatic correction. Source locators and extensions remain inert. Source Integrity Toolkit is independent of Recursive Integrity Toolkit, with no shared internals or runtime dependency.

## Accepted baseline and current work

The eighteen Phase 0 specifications remain approved at `7d2e5fcaff591641b5cefce00e71e88941dd1f95`; [PHASE_0_APPROVAL.md](PHASE_0_APPROVAL.md) revision 1.1 preserves the authorized digest correction. [PHASE_1_COMPLETION.md](PHASE_1_COMPLETION.md) revision 1.0 was accepted with PR #8, merged at `d7d73a790a2a627d19307c9dd48281eff3017023`. Its historical pending header is read with that later acceptance event.

[PHASE_2_PLAN.md](PHASE_2_PLAN.md) and [PHASE_2_COMPLETION.md](PHASE_2_COMPLETION.md) were accepted through PR #18 at `3a9b75ab6ca4ed9d7c97207043a5c8f54c2e2547`. The accepted preparation supports supplied values and UTF-8 bytes, bounded validation, references, time syntax and evidence navigation. The preparation entry points retain their original PC01 admission behavior.

The owner approved [PHASE_3_PLAN.md](PHASE_3_PLAN.md) revision 0.1 with `批准，启动 P3-W01`; PR #19 merged at `80aa943f577f4a7deaeb8a0f3253c62d1263ca62`. [PHASE_3_PROGRESS.md](PHASE_3_PROGRESS.md) records subsequent authority and evidence while prior reviewed documents remain byte-identical. W13 was accepted through [PR #32](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/pull/32), merged at `332e94a007ceb2a955b8e047f45284b431300995`. W14 was accepted through [PR #33](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/pull/33), merged at `6dbca96f3314d537beed4ccb6202147bd9248dd9`. W15 audits the completed component work and records its approved reason-code repair, history-verification optimization, finite CI budgets and remaining acceptance gates in [PHASE_3_COMPLETION.md](PHASE_3_COMPLETION.md).

The private analysis accepts exact built-in values or supplied UTF-8 bytes and executes actual scoped owners, prerequisites, graph witnesses and immutable result delivery. It preserves supplied assertions, unresolved ancestry, qualified populations, correction history and missing evidence as separate facts. It has a fixed invocation budget and cooperative deadline. A complete supplied dossier can legitimately end with a safe resource interruption; the four original H7 examples currently stop under the unchanged work limits. Partial or interrupted execution cannot certify unperformed fields. These private entry points are implementation seams, with no stable public API or public report format promised.

All 228 field obligations have accepted owner-local core evidence. W14 added source-clause and counterexample checks. W15 identified and repaired the missing `dimension_not_selected` distinction for empty dimension selection, with exact paired value/UTF-8 tests and separate absent-subject/incomplete-role controls. The 228 historical rows remain unchanged and do not close public-envelope, rendering or release clauses. See [phase3/obligation_coverage.json](phase3/obligation_coverage.json) for the per-obligation evidence and remaining duties.

## Developer installation and checks

Use a complete Git checkout and a clean CPython 3.11 or 3.13 development environment. The six migrated test files load only their exact, SHA-256-checked historical source from the fixed intake commit, then adapt the named phase-specific assertions. Full Git history is required; no network or mutable-ref fallback occurs during test loading. This retains the original assertions and all 194 historical test identities instead of silently replacing them. See [phase2/transition_ledger.md](phase2/transition_ledger.md).

Use the unit context for this checkout. Local execution is separate from the required four-profile hosted gate. In a POSIX shell:

```sh
export SIT_PHASE_UNIT=P3-W15
```

In PowerShell:

```powershell
$env:SIT_PHASE_UNIT = 'P3-W15'
```

Then run:

```sh
python -m pip install -r requirements-dev.txt
python -m pip install --no-build-isolation --no-deps .
sit --version
sit --help
python -B tools/check_phase0_baseline.py
python -B tools/check_scaffold_boundary.py --unit P3-W15
python -m pytest tests -q
```

A missing context retains the conservative Phase 2 W01 default and cannot validate this Phase 3 checkout. Keep `SIT_PHASE_UNIT=P3-W15` set for both guard and pytest. CI derives Phase 3 context from the actual `phase3/p3-wNN` branch or a single `SIT-Phase-Unit: P3-WNN` main merge footer. Metadata cannot authorize a unit. The original 1,650 Phase 2 identities and method-level adaptations are recorded in [phase3/transition_ledger.md](phase3/transition_ledger.md).

Dependency installation is a developer operation and may access the package index. The installed product has zero third-party runtime dependencies and never imports the developer guards, catalogs or historical tests. Source distributions retain the four permitted repository-context tests; running those tests requires the complete developer checkout. Building the sdist/wheel and using the installed package do not require this test loader or Git history.

The older pytest default covers only tests/scaffold. Use the explicit tests root or the cumulative CI driver to include all present security, contract, unit and integration tests. Stored logical expectations need actual source-bound analytical assertions to count as behavior evidence.

## CI and evidence

[Phase 3 cumulative CI](.github/workflows/phase1-ci.yml) retains Ubuntu 24.04 and Windows Server 2025, each with Python 3.11 and 3.13, immutable action pins, read-only permissions, no stored checkout credentials and finite timeouts. It validates actual entry trees, history and current-unit scope, frozen artifacts, module boundaries and the retained test collection. Raw JUnit outcomes, separately counted subtests, tracked bytes before/after, packaging and offline installed-runtime witnesses remain required.

Accepted W14 code `5146a2e41dfdddfccebd85367655109288fe313f` passed [run 35832693910](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/actions/runs/35832693910), attempt 1, in all four profiles with 3,918 tests and 428 separately counted subtests, zero failures/errors/skips. Its final three-record successor passed the affected existing controls and preserved all other 202 blobs and modes. These remain W14 results. W15 R01 repair precursor `2a8697ea23e315e74c7cc8d7632c95725332b45b` passed source-bound direct controls. Its checkpoint `4d480f2cc5400e96e724d949ed00c82d62f5aeb7` collected 3,937 tests. [Run 36268092968](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/actions/runs/36268092968) passed that collection and 428 separate subtests in Ubuntu 3.11, Ubuntu 3.13 and Windows 3.11; Windows 2025 / Python 3.13 timed out at the unchanged 1,800-second suite limit on both attempts. The retained five artifact ZIPs passed integrity checks, while the acceptance gate remained blocked.

The owner approved `批准 P3-W15-R02` on 2026-09-27 UTC to batch only actual Git parents/tree metadata within each history-validation call. Its nine-path segment preserves product/API behavior, R01 semantic assertions, every existing test identity, live ancestry/diff/archive checks, pins and the then-current 1,800-second suite / 40-minute job limits. One local paired history measurement reduced Git subprocesses from 443 to 335 and elapsed time from 12.326 to 10.270 seconds, with all 57 history rows identical; it does not predict Windows or full-suite savings.

R02 precursor `fae43fcdae0341a6f596545f700bc8932b5d8444` passed 371 affected controls in 342.81 pytest seconds, with 343.616 seconds of process elapsed time. Its final collection was 3,962 tests, preserving all 3,937 R01 identities and adding 25 controls. Actual head `3a8c6f99a2aa71ce8e67454801e16a1c5c5caed7` ran [CI 36296729627](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/actions/runs/36296729627), attempt 1. Both Ubuntu profiles passed all 3,962 tests and 428 subtests; Windows 3.11 completed with three temporary-Git-object deletion failures; Windows 3.13 timed out at 1,800 seconds without complete JUnit. All four original ZIPs remain retained. Follow-up `d32c1499fe7969b9415468ef62c966c38110a090` repaired the temporary object write permission and passed 12 local controls in 15.36 pytest seconds. That local pass provides no Windows CI certification.

The owner approved `批准 R03 继续` at `2026-09-30T15:08:59Z`. R03 binds `d32c1499fe7969b9415468ef62c966c38110a090`, tree `1234a087200c5e56d20c7f53aa0d71a828f167fb`, and sole parent `3a8c6f99a2aa71ce8e67454801e16a1c5c5caed7`. It sets the complete CI test process limit to exactly 2,400 seconds and the job limit to exactly 50 minutes. All 48 product modules, the analytical integration test, the product's 60-second cooperative deadline and work quotas, other internal timeouts, matrix, permissions and pins remain unchanged. Historical scopes stay separate at seven, eleven, nine and ten paths; the cumulative W15 union has twelve. R03's added workflow permission applies only to actual descendants and the named job-budget edit.

R03 precursor `95368b54d17721ff7e975773ea4f3a22e5888ecf` passed 372 affected controls in 67.57 pytest seconds. Actual collection on the directly tested source is 3963 tests, retaining all 3,962 existing identities and adding 1 named controls. A new run on the actual final head must pass all four profiles, including 428 separate subtests each, and a raw-evidence audit. Earlier successes cannot be reused for that gate, and 2,400 seconds is not a measured guarantee of completion. Remaining failures stay blocked without automatic timeout expansion or blind retries. [PR #34](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/pull/34) remains unmerged; [phase3/implementation_evidence.json](phase3/implementation_evidence.json) distinguishes historical runs, local checks and this final gate. Final execution results will be recorded in the PR and review package. Owner acceptance, permanent verification consolidation, the next phase and release remain pending.

The planning PR's inherited-driver failure remains disclosed in [PHASE_3_PLAN.md](PHASE_3_PLAN.md) section 1.2; it is not relabeled as a successful Phase 3 execution.

Windows Server component tests do not certify the future Windows 11/NTFS native adapter. No production platform support or general security proof is asserted. Artifacts retain the existing fourteen-day retention.

## Specifications, security and rights

Start with [V0.1_PRODUCT_SPEC.md](V0.1_PRODUCT_SPEC.md), [DEFINITIONS_AND_UNITS.md](DEFINITIONS_AND_UNITS.md), [CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md](CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md) and [OBSERVABILITY_AND_REPORTING.md](OBSERVABILITY_AND_REPORTING.md). [THEORY_SOURCE_MAP.md](THEORY_SOURCE_MAP.md), [THEORY_TO_CODE_TRACEABILITY.md](THEORY_TO_CODE_TRACEABILITY.md) and [VALIDATION_PLAN.md](VALIDATION_PLAN.md) preserve source interpretation, responsibilities and future behavior tests. Historical catalogs and the approved plans remain unchanged; implementation evidence is tracked separately.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Do not post private evidence, credentials or protected-source identities in this public repository. Use fictional development examples. Private vulnerability reporting remains subject to the existing unverified-channel limitation. Build/test tools and their original reviews remain in [scaffold/toolchain_review.md](scaffold/toolchain_review.md) and [scaffold/ci_toolchain_review.md](scaffold/ci_toolchain_review.md); the current scoped transition is recorded in [phase3/ci_review.md](phase3/ci_review.md).

## License

Copyright 2026 Xiangyu Guo.

Original engineering repository materials are licensed under the **Apache License, Version 2.0**, in [LICENSE](LICENSE), with attribution in [NOTICE](NOTICE). This covers original engineering specifications, documentation, fictional examples, code, schemas and tests that the project has authority to license.

The grant does not automatically cover theory papers or their extracts, page images, translations or adaptations; third-party material; user-supplied evidence; confidential identity maps; or input-derived report content. Theory papers retain their own **CC BY-NC-ND 4.0** notices. Excluded materials retain their own terms and permissions. Successful processing does not transfer rights.

[LICENSING_NOTES.md](LICENSING_NOTES.md) controls these boundaries. Its historical root-license statement refers to Phase 0; accepted P1-W01 applied the license without changing that frozen specification. Upstream contribution/governance rules add no downstream conditions to Apache-2.0. No package-index release has been published by this work.
