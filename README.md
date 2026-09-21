# Source Integrity Toolkit

A local, supplied-evidence toolkit for examining source lineage, evidence independence, external presence and corrective capacity in AI-native information systems.

**Status: Phase 2 accepted; Phase 3 plan approved and P3-W01 transition in verification. Public auditing remains unavailable.** The package remains installable as `0.1.0.dev0`. W01 preserves all 48 product-module bytes: thirteen preparation implementations and thirty-five protected modules. Public audit calls raise `NotImplementedError`; CLI auditing refuses with exit 1 without reading dossiers or producing reports.


## Intended purpose

The planned v0.1 auditor consumes a caller-prepared local JSON dossier containing claims, evidence, origin and transformation records, evaluator relationships and correction history. It distinguishes supplied assertions, supported structural deductions and unresolved information. Different material counts and evidence roles remain distinct. Missing ancestry cannot become an independent source, and a structurally consistent dossier cannot certify its own authenticity.

The adopted scope provides a multidimensional evidence profile. It excludes a universal truth or integrity score, live crawling, hidden-lineage discovery, an LLM judge, automatic source sanctions and automatic correction. Source locators and extensions remain inert. Source Integrity Toolkit is independent of Recursive Integrity Toolkit, with no shared internals or runtime dependency.

## Accepted baseline and current work

The eighteen Phase 0 specifications remain approved at `7d2e5fcaff591641b5cefce00e71e88941dd1f95`; [PHASE_0_APPROVAL.md](PHASE_0_APPROVAL.md) revision 1.1 preserves the authorized digest correction. [PHASE_1_COMPLETION.md](PHASE_1_COMPLETION.md) revision 1.0 was accepted with PR #8, merged at `d7d73a790a2a627d19307c9dd48281eff3017023`. Its historical pending header is read with that later acceptance event.

[PHASE_2_PLAN.md](PHASE_2_PLAN.md) and [PHASE_2_COMPLETION.md](PHASE_2_COMPLETION.md) were accepted through PR #18 at `3a9b75ab6ca4ed9d7c97207043a5c8f54c2e2547`. The accepted preparation supports supplied values and UTF-8 bytes, bounded validation, references, time syntax and evidence navigation. Only PC01 whole-check admission completes; analytical checks and all 228 analytical obligations remain pending.

The owner approved [PHASE_3_PLAN.md](PHASE_3_PLAN.md) revision 0.1 with `批准，启动 P3-W01`; PR #19 merged at `80aa943f577f4a7deaeb8a0f3253c62d1263ca62`. [PHASE_3_PROGRESS.md](PHASE_3_PROGRESS.md) records subsequent authority and evidence while prior reviewed documents remain byte-identical. W01 establishes the actual 157-file entry, independent phase context, exact scopes and cumulative verification. It adds no analytical implementation. Later authorized units will implement the private analytical core; public API, CLI audit, reporting, native capture and release remain deferred.

## Developer installation and checks

Use a complete Git checkout and a clean CPython 3.11 or 3.13 development environment. The six migrated test files load only their exact, SHA-256-checked historical source from the fixed intake commit, then adapt the named phase-specific assertions. Full Git history is required; no network or mutable-ref fallback occurs during test loading. This retains the original assertions and all 194 historical test identities instead of silently replacing them. See [phase2/transition_ledger.md](phase2/transition_ledger.md).

P3-W01 establishes the new independent context. Set it for the commands below. Local execution is separate from the required exact-head four-profile hosted gate. In a POSIX shell:

```sh
export SIT_PHASE_UNIT=P3-W01
```

In PowerShell:

```powershell
$env:SIT_PHASE_UNIT = 'P3-W01'
```

Then run:

```sh
python -m pip install -r requirements-dev.txt
python -m pip install --no-build-isolation --no-deps .
sit --version
sit --help
python -B tools/check_phase0_baseline.py
python -B tools/check_scaffold_boundary.py --unit P3-W01
python -m pytest tests -q
```

A missing context retains the conservative Phase 2 W01 default and cannot validate this Phase 3 checkout. Keep `SIT_PHASE_UNIT=P3-W01` set for both guard and pytest. CI derives Phase 3 context from the actual `phase3/p3-wNN` branch or a single `SIT-Phase-Unit: P3-WNN` main merge footer. Metadata cannot authorize a unit. The exact 1,650 predecessor identities and method-level adaptations are recorded in [phase3/transition_ledger.md](phase3/transition_ledger.md).

Dependency installation is a developer operation and may access the package index. The installed product has zero third-party runtime dependencies and never imports the developer guards, catalogs or historical tests. Source distributions retain the four permitted repository-context tests; running those tests requires the complete developer checkout. Building the sdist/wheel and using the installed package do not require this test loader or Git history.

The older pytest default covers only tests/scaffold. Use the explicit tests root or the cumulative CI driver to include all present security, contract, unit and integration tests. Static fixture checks and stored logical expectations do not execute any of the 228 pending domain obligations.

## CI and evidence

[Phase 3 cumulative CI](.github/workflows/phase1-ci.yml) retains Ubuntu 24.04 and Windows Server 2025, each with Python 3.11 and 3.13, immutable action pins, read-only permissions, no stored checkout credentials and finite timeouts. It validates actual entry trees, history and current-unit scope, frozen artifacts, module boundaries and the retained test collection. Raw JUnit outcomes, separately counted subtests, tracked bytes before/after, packaging and offline installed-runtime witnesses remain required.

Reviewed W09 head `652ec2f434197ce657bc30c16927a9be66d8378e` passed [run 35519939650](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/actions/runs/35519939650), attempt 1, in all four profiles with 1,650 tests and 428 subtest events separately counted, zero failures/errors/skips. Its accepted merge also passed service run `35544450516`. These are predecessor evidence. W01 and its final documentation successor require their own exact-head matrices; current results are recorded in [phase3/implementation_evidence.json](phase3/implementation_evidence.json) and the review PR.

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
