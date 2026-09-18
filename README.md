# Source Integrity Toolkit

A local, supplied-evidence toolkit for examining source lineage, evidence independence, external presence and corrective capacity in AI-native information systems.

**Status: Phase 1 repository scaffold. No audit functionality is implemented.** The source package is installable as version `0.1.0.dev0`. Its 48 import-safe modules, static contract catalogs, fictional inputs and test-only logical expectations are present. Public audit calls immediately raise `NotImplementedError`. The CLI provides help/version and refuses audit execution with exit code 1; it reads no dossier and creates no report.

## Intended purpose

The planned v0.1 auditor will work from a caller-prepared local JSON dossier containing claims, evidence, origin and transformation records, evaluator relationships and correction history. Its outputs will distinguish supplied assertions, supported structural deductions and unresolved information.

A typical question is whether several cited materials trace back to the same acquisition, whether evaluator roles share recorded ancestry, or whether a correction has a documented route and a linked downstream change. Different material counts and evidence roles remain distinct. Missing ancestry cannot become an independent source, and a structurally consistent dossier cannot certify its own authenticity.

The adopted scope provides a multidimensional evidence profile. It excludes a universal truth or integrity score, live crawling, hidden-lineage discovery, an LLM judge, automatic source sanctions and automatic correction. Source locators and extension fields remain inert data. These are design requirements whose implementation and tests remain ahead.

The project is independent of Recursive Integrity Toolkit. No shared internal package, runtime dependency or implicit schema compatibility is established.

## Current baseline and roadmap

The eighteen Phase 0 specifications are approved at commit `7d2e5fcaff591641b5cefce00e71e88941dd1f95`. [PHASE_0_APPROVAL.md](PHASE_0_APPROVAL.md) records that approval and its corrected exact-byte manifest. Original approvals and the manifest correction retain their history.

| Phase 1 work unit | Purpose |
|---|---|
| P1-W01 | Baseline verification, governance and Apache-2.0 application |
| P1-W02 | Packaging, import-safe modules and explicitly unimplemented audit entry points |
| P1-W03 | Static contract/trace catalogs and schema reservations |
| P1-W04 | Fictional hero dossiers and separately identified logical expectations |
| P1-W05 | Scaffold boundary, baseline and architecture guards |
| P1-W06 | Reviewed, minimally privileged scaffold CI |
| P1-W07 | Final scaffold audit and handoff |

[PHASE_1_PLAN.md](PHASE_1_PLAN.md) controls the work-unit sequence and closed file allowlists. [PHASE_1_PROGRESS.md](PHASE_1_PROGRESS.md) records actual execution and review status. Each work unit has its own acceptance gate. Phase 1 does not implement source tracing, independence qualification, concentration, correction analysis, report rendering or native filesystem security.

## Developer installation and checks

Use a clean CPython 3.11 or 3.13 development environment. From this source checkout, install the already reviewed development pins, then the scaffold without resolving new build/runtime dependencies:

```sh
python -m pip install -r requirements-dev.txt
python -m pip install --no-build-isolation --no-deps .
sit --version
sit --help
python -B tools/check_phase0_baseline.py
python -B tools/check_scaffold_boundary.py
python -m pytest tests/scaffold tests/security -q
```

Dependency installation is a developer operation that may access the package index. It does not enable source retrieval in the product. The installed product has zero third-party runtime dependencies. An invocation such as `sit audit input.json --output result` deliberately returns exit 1 and a fixed unimplemented message. This is a scaffold refusal, not an audit result or a final report-protocol exit code. No package-index release has been published.

Both test directories are explicit in the command above. The earlier pytest default covers only tests/scaffold and must not be mistaken for the entire security suite. Neither passing static fixture checks nor reading stored logical expectations establishes any of the 228 pending domain-test obligations.

## CI scope and evidence

[Phase 1 scaffold CI](.github/workflows/phase1-ci.yml) defines four required rows: Ubuntu 24.04 and Windows Server 2025, each with Python 3.11 and 3.13. It uses read-only repository permissions and full-commit action pins, checks the exact candidate head, runs both full-checkout guards, reviews and installs pinned developer wheels, collects and runs the accumulated tests, and checks source/wheel contents plus an offline clean installation. It uploads only verification records for fourteen days, with no package publication or automatic merge.

The workflow is expressed in JSON-form YAML so the standard library can inspect its complete permission/trigger/matrix structure without an extra parser dependency. Policy tests include deliberate unsafe mutations. Networked dependency setup is separate from the application's no-network probes. Runner images and Python patch releases are recorded at execution time.

**P1-W06 remains blocked on one Windows-only test-canary repair.** After the authorized observer-preload and generated-metadata fixes, run `35363039474` at `641f2b9711aad9812a0c709eb949798a4f4ebee7` passed all 194 collected tests on both Linux rows and 193 of 194 on each Windows row. Both full-checkout guards and all package/clean-install checks passed everywhere. The remaining native-loading canary supplies None, which Windows rejects before the expected audit event. Its additional one-file repair is proposed as P1-W06-R02 and has not been applied. Full evidence and retained failures are in [PHASE_1_PROGRESS.md](PHASE_1_PROGRESS.md). No failing test has been skipped, and subtest events remain separate from top-level instances.

Windows Server scaffold checks do not certify the future Windows 11/NTFS file adapter, and no production platform support is asserted.

## Specifications

Start with [V0.1_PRODUCT_SPEC.md](V0.1_PRODUCT_SPEC.md), [DEFINITIONS_AND_UNITS.md](DEFINITIONS_AND_UNITS.md) and [CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md](CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md). [OBSERVABILITY_AND_REPORTING.md](OBSERVABILITY_AND_REPORTING.md) defines result states and report meaning.

[THEORY_SOURCE_MAP.md](THEORY_SOURCE_MAP.md) preserves the theoretical source basis, and [THEORY_TO_CODE_TRACEABILITY.md](THEORY_TO_CODE_TRACEABILITY.md) links it to engineering responsibilities. [VALIDATION_PLAN.md](VALIDATION_PLAN.md) specifies future tests; its logical expectations are not executed product results.

The frozen specifications and approved plan remain at their root paths. Their historical pending headers are interpreted through later approval records, rather than rewritten. [scaffold/baseline_manifest.json](scaffold/baseline_manifest.json) is a machine-readable copy of the freeze evidence. `.gitattributes` protects those paths against checkout text conversion; it does not prevent deliberate edits or replace hash verification.

## Contributions, security and data

See [CONTRIBUTING.md](CONTRIBUTING.md) for scoped changes, rights and review rules, and [SECURITY.md](SECURITY.md) for the present reporting limitations. Do not post private evidence, credentials, confidential identity maps or real protected-source dossiers in this public repository. Use fictional examples for development.

The installed runtime has no required third-party Python dependencies. Build/test tools and their actual historical results are reviewed separately in [scaffold/toolchain_review.md](scaffold/toolchain_review.md). Current matrix/action choices are documented in [scaffold/ci_toolchain_review.md](scaffold/ci_toolchain_review.md). Developer tools retain their own rights and are excluded from the product wheel.

## License

Copyright 2026 Xiangyu Guo.

The project's original engineering repository materials are licensed under the **Apache License, Version 2.0**, provided in [LICENSE](LICENSE). This includes original engineering specifications, documentation, and fictional examples as well as project code, schemas and tests when added. [NOTICE](NOTICE) supplies attribution.

The grant covers material the project has authority to license. It does not automatically cover the underlying theory papers, their extracts, page images, translations or adaptations; third-party materials; user-supplied evidence; confidential identity mappings; or input-derived portions of audit reports. The theory papers retain their own **CC BY-NC-ND 4.0** notices. Other excluded materials retain their applicable terms and permissions. References and successful processing do not transfer rights.

[LICENSING_NOTES.md](LICENSING_NOTES.md) describes these boundaries. Its historical statement that the root license had not yet been applied refers to Phase 0; P1-W01 supplies that file without changing the frozen specification. Contribution and project-governance rules govern changes accepted upstream and add no downstream conditions to Apache-2.0.
