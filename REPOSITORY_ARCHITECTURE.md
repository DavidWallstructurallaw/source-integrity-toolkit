# REPOSITORY_ARCHITECTURE

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Target release | v0.1 |
| Phase / work unit | Phase 0 / Work Unit 10 |
| Revision | 0.1 |
| Date | 2026-09-17 |
| Status | PROPOSED FOR REVIEW; architecture only, no implementation |
| Theory Owner | Xiangyu Guo |
| Technical Owner | Unassigned |
| Current authorization | Work Unit 10 documentation only |
| Accepted prior controls | WU9-C01 and WU9-C02 accepted by the instruction to continue WU10; WU9-C03 already approved as Apache-2.0 |
| Primary traceability input | `THEORY_TO_CODE_TRACEABILITY.md` revision 0.1 |
| Companion outputs | `DEPENDENCY_STRATEGY.md`, `GOVERNANCE_AND_HANDOFF.md` |
| Implementation / Phase 1 authorization | Not granted by this document |

## 1. Purpose and architectural rule

This document assigns concrete future repository and module ownership to the logical responsibilities already defined in `THEORY_TO_CODE_TRACEABILITY.md`. It does not implement those modules, create the package tree, freeze executable schemas, or authorize Phase 1.

The architectural objective is a small, deterministic, local Python toolkit whose public behavior is governed by the approved dossier, analysis, observability, privacy and validation contracts. The implementation must make it difficult for one module to silently change the meaning owned by another.

The central ownership rule is:

```text
Theory / product requirement
        ↓
SIT-TR responsibility
        ↓
logical owner in THEORY_TO_CODE_TRACEABILITY.md
        ↓
concrete module owner in this document
        ↓
public contract + executable tests in later phases
```

No module may bypass that chain by interpreting paper prose directly at runtime.

## 2. Architectural principles

1. **One semantic authority per concept.** Counting, origin qualification, independence, correction, report state and privacy rules each have one primary implementation owner.
2. **Typed views before generic graph convenience.** Citation, transformation, origin, evaluator and correction relations remain separate projections. A generic graph traversal cannot decide which edges are epistemically valid for a particular result.
3. **Pure analysis core.** Analytical modules consume an immutable normalized snapshot and return structured results. They do not read files, write reports, fetch URLs, log user content, call models or mutate input.
4. **Boundary isolation.** File opening, resource limits, output publication, safe rendering and disclosure policy remain outside analytical modules.
5. **No hidden inference layer.** v0.1 contains no model judge, embedding system, semantic provenance resolver, source-reputation service or network client.
6. **Exact result ownership.** JSON and Markdown render one frozen report model. Markdown does not recompute analytical results.
7. **Fail closed on structural authority, fail bounded on evidence.** Invalid structure is rejected; valid sparse evidence produces explicit unavailable/unknown results under the reporting contract.
8. **No cross-project runtime dependency.** Recursive Integrity Toolkit and Source Integrity Toolkit remain independent packages and repositories.
9. **No plugin execution in v0.1.** Extensions remain inert data and cannot register code, predicates, renderers or policies.
10. **Phase discipline.** Phase 1 may scaffold paths and contracts approved here, while analytical behavior remains prohibited until separately approved later phases.

## 3. Proposed repository layout

The following is the planned target layout. Phase 0 creates none of these implementation paths.

```text
source-integrity-toolkit/
├── README.md
├── LICENSE
├── NOTICE
├── pyproject.toml
├── src/
│   └── source_integrity_toolkit/
│       ├── __init__.py
│       ├── api.py
│       ├── cli.py
│       │
│       ├── contracts/
│       │   ├── __init__.py
│       │   ├── bundle.py
│       │   ├── evidence.py
│       │   ├── results.py
│       │   ├── report.py
│       │   └── constants.py
│       │
│       ├── io/
│       │   ├── __init__.py
│       │   ├── input_file.py
│       │   ├── output_directory.py
│       │   └── publication.py
│       │
│       ├── validation/
│       │   ├── __init__.py
│       │   ├── structure.py
│       │   ├── references.py
│       │   ├── semantics.py
│       │   └── limits.py
│       │
│       ├── graph/
│       │   ├── __init__.py
│       │   ├── projections.py
│       │   ├── traversal.py
│       │   ├── cycles.py
│       │   └── witnesses.py
│       │
│       ├── analysis/
│       │   ├── __init__.py
│       │   ├── inventory.py
│       │   ├── origins.py
│       │   ├── process_comparison.py
│       │   ├── contribution_profile.py
│       │   ├── evaluator_lineage.py
│       │   ├── presence.py
│       │   ├── correction_routes.py
│       │   ├── correction_outcomes.py
│       │   ├── human_review.py
│       │   ├── context.py
│       │   └── findings.py
│       │
│       ├── reporting/
│       │   ├── __init__.py
│       │   ├── assemble.py
│       │   ├── json_report.py
│       │   ├── markdown_report.py
│       │   └── escaping.py
│       │
│       └── runtime/
│           ├── __init__.py
│           ├── boundary.py
│           ├── resources.py
│           ├── disclosure.py
│           └── diagnostics.py
│
├── tests/
│   ├── unit/
│   ├── contract/
│   ├── integration/
│   ├── security/
│   ├── golden/
│   └── fixtures/
│       ├── hero/
│       ├── micro/
│       └── adversarial/
│
└── docs/
    └── phase0/
```

The exact placement of the existing Phase 0 Markdown files is a Phase 1 repository-assembly choice. Their current root placement remains valid until a separately approved move preserves links and hashes.

## 4. Public interface boundary

v0.1 has two public invocation surfaces over one semantic core.

### 4.1 Python library surface

The intended public package root is `source_integrity_toolkit`.

The public semantic operations are:

```text
audit_bundle(bundle, *, options=None) -> AuditReport
audit_file(input_path, output_directory, *, options=None) -> AuditReportSummary
```

The exact Python type declarations are created later from the approved contracts. `audit_bundle` accepts the already constructed logical dossier and performs no filesystem reads or writes. `audit_file` owns the safe file/open/publish boundary defined by Work Unit 9.

Only public names re-exported from `source_integrity_toolkit.__init__` and documented in the release contract are stable. Internal modules are not compatibility promises.

### 4.2 CLI surface

The planned command is:

```text
sit audit INPUT --output OUTPUT_DIR
```

A future trusted option may request the already approved whole-file digest. There is no network mode, model option, trust ranking, report-to-stdout mode, force-overwrite option or plugin flag in v0.1.

CLI and library results must use the same normalized contracts and analytical functions. CLI-specific behavior is limited to argument validation, exit status and the safe local filesystem boundary.

### 4.3 Public artifacts

The stable artifact families are the already specified logical bundle and report contracts. Architecture does not create a second analytics schema for internal convenience.

Internal graph projections, caches and helper records are ephemeral implementation details. They cannot become undocumented interchange contracts.

## 5. Logical owner to concrete module mapping

The logical-owner names remain authoritative through `THEORY_TO_CODE_TRACEABILITY.md`. This table supplies their concrete v0.1 implementation homes.

| Logical owner | Primary module owner | Supporting modules | Primary future tests |
|---|---|---|---|
| `INGESTION_CONTRACT` | `contracts/bundle.py` | `validation/structure.py`, `validation/references.py`, `io/input_file.py` | `tests/contract/test_bundle_contract.py`, `tests/security/test_input_boundary.py` |
| `EVIDENCE_BASIS` | `contracts/evidence.py` | `validation/semantics.py` | `tests/contract/test_evidence_basis.py` |
| `SOURCE_INVENTORY` | `analysis/inventory.py` | `contracts/results.py` | `tests/unit/test_inventory.py` |
| `ORIGIN_ANALYSIS` | `analysis/origins.py` | `graph/projections.py`, `graph/traversal.py`, `graph/witnesses.py` | `tests/unit/test_origins.py` |
| `PROCESS_COMPARISON` | `analysis/process_comparison.py` | `validation/semantics.py` | `tests/unit/test_process_comparison.py` |
| `CONTRIBUTION_PROFILE` | `analysis/contribution_profile.py` | `analysis/origins.py` | `tests/unit/test_contribution_profile.py` |
| `EVALUATOR_LINEAGE` | `analysis/evaluator_lineage.py` | `graph/projections.py`, `graph/traversal.py` | `tests/unit/test_evaluator_lineage.py` |
| `PRESENCE_RECORDS` | `analysis/presence.py` | `validation/semantics.py` | `tests/unit/test_presence.py` |
| `CORRECTION_ROUTES` | `analysis/correction_routes.py` | `graph/projections.py`, `graph/traversal.py` | `tests/unit/test_correction_routes.py` |
| `CORRECTION_OUTCOMES` | `analysis/correction_outcomes.py` | `analysis/correction_routes.py` | `tests/unit/test_correction_outcomes.py` |
| `HUMAN_REVIEW_RECORDS` | `analysis/human_review.py` | `contracts/evidence.py` | `tests/unit/test_human_review.py` |
| `CONTEXT_PRESERVATION` | `analysis/context.py` | `contracts/evidence.py` | `tests/unit/test_context_preservation.py` |
| `GRAPH_VIEW_CONTRACT` | `graph/projections.py` | `graph/traversal.py`, `graph/cycles.py`, `graph/witnesses.py` | `tests/contract/test_graph_views.py` |
| `TEMPORAL_CONTRACT` | `validation/semantics.py` | `contracts/bundle.py` | `tests/contract/test_temporal_contract.py` |
| `REPORT_CONTRACT` | `contracts/report.py` | `reporting/assemble.py`, `contracts/results.py` | `tests/contract/test_report_contract.py` |
| `FINDING_CONTRACT` | `analysis/findings.py` | `contracts/results.py` | `tests/unit/test_findings.py` |
| `REPORT_PRESENTATION` | `reporting/json_report.py` and `reporting/markdown_report.py` | `reporting/escaping.py`, `reporting/assemble.py` | `tests/contract/test_report_parity.py`, `tests/security/test_rendering.py` |
| `RUNTIME_BOUNDARY` | `runtime/boundary.py` | `runtime/resources.py`, `runtime/disclosure.py`, `runtime/diagnostics.py`, `io/*` | `tests/security/`, `tests/integration/test_runtime_boundary.py` |
| `VALIDATION_GOVERNANCE` | executable tests and CI, not one runtime module | `tests/golden/`, `tests/contract/`, repository CI | `tests/golden/`, trace-coverage checks |

Trace closure is transitive: every existing `SIT-TR001` through `SIT-TR035` retains its logical owner, and this table supplies the concrete path owner. A future change to one of these path owners must preserve one semantic authority and update traceability before release.

## 6. Internal dependency direction

Allowed dependency direction is intentionally one-way:

```text
contracts
   ↑
validation    graph
   ↑          ↑
      analysis
         ↑
      reporting
         ↑
runtime / io / api / cli
```

More precisely:

- `contracts` imports only standard-library support and other contract primitives.
- `validation` may import `contracts`, but not analysis or reporting.
- `graph` may import contract types and validation-safe primitives, but not analysis policy.
- `analysis` may import `contracts`, `validation` and `graph`.
- `reporting` may import frozen result/report contracts. It cannot call analytical modules to recalculate a field.
- `runtime` and `io` may orchestrate validation, analysis and reporting but cannot redefine their semantics.
- `api.py` and `cli.py` are composition surfaces only.

Circular imports between domain layers are prohibited. A cycle in source evidence is data; a cycle in implementation ownership is an architecture defect.

## 7. Graph architecture

The graph layer is a deterministic typed-projection service over admitted assertions. It owns graph mechanics, not epistemic policy.

`projections.py` builds only views named by the approved relation registry. `traversal.py` accepts an explicit projection/view and bounded start set. `cycles.py` reports cycles in the requested typed view. `witnesses.py` constructs finite paths/member sets for downstream results.

The graph package must never:

- infer an edge from text similarity;
- merge identities from names, URLs or checksums;
- convert citation into derivation;
- convert disconnection into independence;
- assign trust/reputation;
- fetch an endpoint;
- decide that a conflict assertion is true.

Those constraints keep generic graph utility from becoming an undeclared epistemic engine.

## 8. Analysis architecture

Each analytical module owns a bounded family of results and is pure with respect to the audited dossier.

A module receives the normalized immutable snapshot plus an explicit inquiry/scope. It returns result objects with state, scope, population, basis, witnesses, qualifications and values as defined by the report contract.

No analytical module may silently drop an unknown member to make a scalar calculable. No analytical module logs source content. No module can widen the inquiry or use an unselected claim to improve a result.

The restricted HHI remains in `contribution_profile.py`; it is not a generic scoring utility. Externality stays in `presence.py`; it is not a source-quality score. Corrective route and observed correction effect remain separate modules.

## 9. Reporting architecture

`reporting/assemble.py` converts completed analytical result objects into one frozen `AuditReport` without changing their meaning.

The JSON and Markdown renderers consume the same report instance. Their differences are representational only. `escaping.py` implements the safe-rendering contract from Work Unit 9 and cannot remove substantive text or change identifiers.

A report pair is published only by `io/publication.py` after both representations are complete and parity checks succeed. Renderers never open external sources or choose output paths.

## 10. Runtime and privacy architecture

`runtime/boundary.py` is the composition point for the adopted local-only behavior. It enforces the invocation mode and owns safe cancellation/failure mapping.

`runtime/resources.py` owns Work Unit 9's WU9-L01 through WU9-L14 ceilings and work/time accounting. Source data and extensions cannot raise those limits.

`runtime/disclosure.py` owns report-field minimization and protected-source handling already approved in WU9-C01. It cannot invent anonymization or remove a required analytical limitation.

`runtime/diagnostics.py` owns safe fixed diagnostic messages and suppression of incidental source values. It does not become an application log.

File-opening, staging, permissions and no-clobber publication remain in `io/`. This keeps filesystem authority out of analytical code.

## 11. Platform support

The v0.1 reference implementation target is CPython 3.11 or later on ordinary local filesystems.

Phase 1 should scaffold tests on at least one current Linux runner and one Windows runner before claiming portable filesystem behavior. macOS support may be included when the same security contract can be tested. Unsupported platform/ACL semantics must fail or remain unclaimed rather than weakening the WU9 private-output requirement.

A POSIX implementation uses owner-only report-directory permissions. Windows support must use an implementation and tests that establish the equivalent project policy before the platform is listed as supported.

No container, server, browser, daemon or hosted API is a v0.1 requirement.

## 12. Cross-project boundary

Source Integrity Toolkit remains independent of Recursive Integrity Toolkit.

v0.1 establishes no shared Python package, internal import, database or common-core repository. A future integration may exchange only an explicitly versioned public artifact. The preferred first integration path is an adapter that consumes a published Source Integrity Toolkit bundle/report and maps it into the other tool's public input contract.

Such an adapter must:

- live outside both tools' analytical internals or in a clearly owned optional integration package;
- declare both source and target contract versions;
- preserve source scope, relation type, provenance, uncertainty and unresolved status;
- reject or disclose any semantics it cannot preserve;
- never treat successful conversion as independent validation.

No `integrity-core` shared package is planned for v0.1. Shared primitives should be extracted only after both independent implementations demonstrate stable duplicate requirements.

## 13. Phase 1 scaffold boundary

On later Phase 1 authorization, the scaffold may create the directory/file skeleton implied by this architecture, subject to the approved Phase 1 plan.

Phase 1 may create import-safe modules, contract placeholders, test/fixture directories, project metadata, Apache-2.0 licensing files, CI scaffolding and architecture-compliance checks.

Phase 1 must not implement:

- graph traversal or cycle detection;
- ancestry resolution;
- process-independence qualification;
- HHI or other analytical calculations;
- evaluator overlap;
- presence/stage calculations;
- correction reachability or outcome analysis;
- report generation beyond structural placeholders;
- runtime filesystem security logic beyond scaffold contracts;
- live network or model integrations.

Architecture names do not authorize behavior earlier than its phase.

## 14. Architecture acceptance criteria

Work Unit 10 architecture passes review when:

1. every logical owner in the traceability registry has a concrete module/test owner;
2. no analytical responsibility depends on live network, LLM or another toolkit's internals;
3. graph mechanics cannot decide epistemic meaning by generic traversal alone;
4. input/output authority is isolated from pure analysis;
5. one frozen report object feeds both JSON and Markdown;
6. WU9 privacy/resource controls have explicit runtime owners;
7. the cross-project boundary uses public artifacts rather than shared internals;
8. Phase 1 can scaffold the layout without implementing analytical behavior;
9. Apache-2.0 release artifacts have an obvious future repository location without relicensing theory/user materials;
10. no public analytical field, threat family, score or result state is added by the architecture itself.

## 15. Review item and stop point

**WU10-C01** asks the owner to approve this module/public-interface architecture, including the concrete logical-owner mapping and no-shared-runtime cross-project boundary.

Approval authorizes the architecture as an input to Work Unit 11 and the later Phase 1 plan. It does not create implementation code or approve Phase 1 itself.
