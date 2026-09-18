# Source Integrity Toolkit

A local, supplied-evidence toolkit for examining source lineage, evidence independence, external presence and corrective capacity in AI-native information systems.

**Status: Phase 1 repository scaffold in progress. No audit functionality is implemented.** P1-W01 establishes the project's license, governance and frozen-baseline controls. The repository does not yet contain an installable auditor, working CLI, runtime schema validator or generated analytical report.

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

The future Python package and `sit` command are design targets. Installation and usage instructions will be added with the relevant scaffold work. No package release or supported production platform is claimed here.

## Specifications

Start with [V0.1_PRODUCT_SPEC.md](V0.1_PRODUCT_SPEC.md), [DEFINITIONS_AND_UNITS.md](DEFINITIONS_AND_UNITS.md) and [CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md](CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md). [OBSERVABILITY_AND_REPORTING.md](OBSERVABILITY_AND_REPORTING.md) defines result states and report meaning.

[THEORY_SOURCE_MAP.md](THEORY_SOURCE_MAP.md) preserves the theoretical source basis, and [THEORY_TO_CODE_TRACEABILITY.md](THEORY_TO_CODE_TRACEABILITY.md) links it to engineering responsibilities. [VALIDATION_PLAN.md](VALIDATION_PLAN.md) specifies future tests; its logical expectations are not executed product results.

The frozen specifications and approved plan remain at their root paths. Their historical pending headers are interpreted through later approval records, rather than rewritten. [scaffold/baseline_manifest.json](scaffold/baseline_manifest.json) is a machine-readable copy of the freeze evidence. `.gitattributes` protects those paths against checkout text conversion; it does not prevent deliberate edits or replace hash verification.

## Contributions, security and data

See [CONTRIBUTING.md](CONTRIBUTING.md) for scoped changes, rights and review rules, and [SECURITY.md](SECURITY.md) for the present reporting limitations. Do not post private evidence, credentials, confidential identity maps or real protected-source dossiers in this public repository. Use fictional examples for development.

The intended runtime has no required third-party Python dependencies. Proposed build/test tools are reviewed separately in [scaffold/toolchain_review.md](scaffold/toolchain_review.md). Those tools have not been installed or exercised for the project in P1-W01.

## License

Copyright 2026 Xiangyu Guo.

The project's original engineering repository materials are licensed under the **Apache License, Version 2.0**, provided in [LICENSE](LICENSE). This includes original engineering specifications, documentation, and fictional examples as well as project code, schemas and tests when added. [NOTICE](NOTICE) supplies attribution.

The grant covers material the project has authority to license. It does not automatically cover the underlying theory papers, their extracts, page images, translations or adaptations; third-party materials; user-supplied evidence; confidential identity mappings; or input-derived portions of audit reports. The theory papers retain their own **CC BY-NC-ND 4.0** notices. Other excluded materials retain their applicable terms and permissions. References and successful processing do not transfer rights.

[LICENSING_NOTES.md](LICENSING_NOTES.md) describes these boundaries. Its historical statement that the root license had not yet been applied refers to Phase 0; P1-W01 supplies that file without changing the frozen specification. Contribution and project-governance rules govern changes accepted upstream and add no downstream conditions to Apache-2.0.
