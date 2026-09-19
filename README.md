# Source Integrity Toolkit

A local, supplied-evidence toolkit for examining source lineage, evidence independence, external presence and corrective capacity in AI-native information systems.

**Status: Phase 1 accepted; Phase 2 P2-W01 developer controls under review. No audit functionality is implemented.** The source package remains installable as `0.1.0.dev0`. All 48 product modules retain their accepted scaffold bytes in this unit. Public audit calls immediately raise `NotImplementedError`; the CLI provides help/version and refuses audits with exit 1, without reading dossiers or producing reports.

## Intended purpose

The planned v0.1 auditor consumes a caller-prepared local JSON dossier containing claims, evidence, origin and transformation records, evaluator relationships and correction history. It distinguishes supplied assertions, supported structural deductions and unresolved information. Different material counts and evidence roles remain distinct. Missing ancestry cannot become an independent source, and a structurally consistent dossier cannot certify its own authenticity.

The adopted scope provides a multidimensional evidence profile. It excludes a universal truth or integrity score, live crawling, hidden-lineage discovery, an LLM judge, automatic source sanctions and automatic correction. Source locators and extensions remain inert. Source Integrity Toolkit is independent of Recursive Integrity Toolkit, with no shared internals or runtime dependency.

## Accepted baseline and current work

The eighteen Phase 0 specifications remain approved at `7d2e5fcaff591641b5cefce00e71e88941dd1f95`; [PHASE_0_APPROVAL.md](PHASE_0_APPROVAL.md) revision 1.1 preserves the authorized digest correction. [PHASE_1_COMPLETION.md](PHASE_1_COMPLETION.md) revision 1.0 was accepted with PR #8, merged at `d7d73a790a2a627d19307c9dd48281eff3017023`. Its historical pending header is read with that later acceptance event.

[PHASE_2_PLAN.md](PHASE_2_PLAN.md) revision 0.1 was approved and PR #9 merged at `eb730dda31d189c8487b5247a45bae47b678821b`. Only P2-W01 is currently authorized for execution. [PHASE_2_PROGRESS.md](PHASE_2_PROGRESS.md) records exact work, evidence and review stops. The entry manifest resolves all 125 intake file hashes from a pinned prior manifest plus four disjoint records; it has no self-reference.

P2-W01 establishes the phase-aware module guard, the historical-to-current test transition and cumulative CI. It creates no product implementation or executable schema. Later authorized Phase 2 units may implement thirteen existing internal preparation modules; thirty-five other modules remain frozen. Public API/CLI auditing remains unavailable throughout Phase 2. No analysis result, source independence, HHI, correction finding, audit report, native filesystem implementation or release is delivered here.

## Developer installation and checks

Use a complete Git checkout and a clean CPython 3.11 or 3.13 development environment. The six migrated test files load only their exact, SHA-256-checked historical source from the fixed intake commit, then adapt the named phase-specific assertions. Full Git history is required; no network or mutable-ref fallback occurs during test loading. This retains the original assertions and all 194 historical test identities instead of silently replacing them. See [phase2/transition_ledger.md](phase2/transition_ledger.md).

```sh
python -m pip install -r requirements-dev.txt
python -m pip install --no-build-isolation --no-deps .
sit --version
sit --help
python -B tools/check_phase0_baseline.py
python -B tools/check_scaffold_boundary.py --unit P2-W01
python -m pytest tests -q
```

W01 is the conservative default developer unit. Later reviewed units supply the corresponding `SIT_PHASE_UNIT` context before running tests, independently of candidate policy files. It is a mechanical test context, not proof of owner approval. CI derives it from the exact `phase2/p2-wNN` review branch. A main-branch work-unit merge must include exactly one `SIT-Phase-Unit: P2-WNN` footer, preserving the separately authorized unit context after merge.

Dependency installation is a developer operation and may access the package index. The installed product has zero third-party runtime dependencies and never imports the developer guards, catalogs or historical tests. Source distributions retain the four permitted repository-context tests; running those tests requires the complete developer checkout. Building the sdist/wheel and using the installed package do not require this test loader or Git history.

The older pytest default covers only tests/scaffold. Use the explicit tests root or the cumulative CI driver to include all present security, contract, unit and integration tests. Static fixture checks and stored logical expectations do not execute any of the 228 pending domain obligations.

## CI and evidence

[Phase 2 cumulative CI](.github/workflows/phase1-ci.yml) retains four required rows: Ubuntu 24.04 and Windows Server 2025, each with Python 3.11 and 3.13. It retains read-only repository permissions, exact-head checkout, immutable action pins, no stored checkout credentials, finite timeouts, reviewed developer wheels and explicit verification-only artifact uploads. Full history supports pinned historical test loading and actual entry-commit byte checks. No source archive, user dossier, package or secret is uploaded.

The driver validates the complete actual 124-file accepted Phase 1 commit and 125-file plan-merge intake, the current work-unit path delta, the actual twenty-file frozen baseline and all forty-eight product slots. It checks the old-to-new collection identity mapping, raw JUnit outcomes, tracked bytes before/after, packaging, clean offline installation and source-rebuild member contents. Tests and subtest events remain separate counts. Missing or failed evidence is not a successful result.

W01 execution results belong to its exact-head PR and progress record. The earlier four-row 194-test Phase 1 evidence remains historical and is not relabeled as a Phase 2 execution. The W01 candidate requires its own four-row run before technical completion and separate owner acceptance before merge.

Windows Server component tests do not certify the future Windows 11/NTFS native adapter. No production platform support or general security proof is asserted. Artifacts retain the existing fourteen-day retention.

## Specifications, security and rights

Start with [V0.1_PRODUCT_SPEC.md](V0.1_PRODUCT_SPEC.md), [DEFINITIONS_AND_UNITS.md](DEFINITIONS_AND_UNITS.md), [CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md](CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md) and [OBSERVABILITY_AND_REPORTING.md](OBSERVABILITY_AND_REPORTING.md). [THEORY_SOURCE_MAP.md](THEORY_SOURCE_MAP.md), [THEORY_TO_CODE_TRACEABILITY.md](THEORY_TO_CODE_TRACEABILITY.md) and [VALIDATION_PLAN.md](VALIDATION_PLAN.md) preserve source interpretation, responsibilities and future behavior tests. Historical catalogs and the approved plans remain unchanged; implementation evidence is tracked separately.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Do not post private evidence, credentials or protected-source identities in this public repository. Use fictional development examples. Private vulnerability reporting remains subject to the existing unverified-channel limitation. Build/test tools and their original reviews remain in [scaffold/toolchain_review.md](scaffold/toolchain_review.md) and [scaffold/ci_toolchain_review.md](scaffold/ci_toolchain_review.md); the scoped transition is recorded in [phase2/ci_review.md](phase2/ci_review.md).

## License

Copyright 2026 Xiangyu Guo.

Original engineering repository materials are licensed under the **Apache License, Version 2.0**, in [LICENSE](LICENSE), with attribution in [NOTICE](NOTICE). This covers original engineering specifications, documentation, fictional examples, code, schemas and tests that the project has authority to license.

The grant does not automatically cover theory papers or their extracts, page images, translations or adaptations; third-party material; user-supplied evidence; confidential identity maps; or input-derived report content. Theory papers retain their own **CC BY-NC-ND 4.0** notices. Excluded materials retain their own terms and permissions. Successful processing does not transfer rights.

[LICENSING_NOTES.md](LICENSING_NOTES.md) controls these boundaries. Its historical root-license statement refers to Phase 0; accepted P1-W01 applied the license without changing that frozen specification. Upstream contribution/governance rules add no downstream conditions to Apache-2.0. No package-index release has been published by this work.
