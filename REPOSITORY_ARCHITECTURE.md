# REPOSITORY_ARCHITECTURE

> Current revision 0.2: §§16-22 complete SIT-D028-SIT-D031 for WU11 re-audit. The original control table and §§1-15 below are retained history. Final Phase 0 approval and implementation remain pending.

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

## 16. WU11 remediation authority and realization profile

This supplement is revision 0.2, dated 2026-09-17. Sections 1-15 and their historical control table remain unchanged. The owner authorized completion of the four recorded gaps followed by WU11 re-audit: `可以，执行补齐，再进行 WU11 复审`. This authorizes the recommended completion direction, not a claim that the resulting software or final Phase 0 baseline has been approved.

Sections 17-20 supply the previously reserved realization for SIT-D028-SIT-D031. They refine the prospective interface sketches in §4 and platform statement in §11. They preserve `sit-bundle/0.1`, `sit-report/0.1`, all existing analytical fields, states, reasons, limits and H7/W7 oracles. No other project's internals are imported. New choices are engineering operationalizations, not quotations or new results from the theory papers.

The profile identifier is **SIT-RP-0.1**. It is a specification label used in the existing `run.qualifications`, not an added root field. The input/report schemas remain owned by the lineage/reporting documents. Technical reference facts are separated in §22 from the chosen composition below.

Additional future internal paths are `contracts/execution.py`, `io/platform_linux.py` and `io/platform_windows.py`. The first holds the authority-free execution interface and safe transport types; the latter two own the fixed native file operations. They create no new logical owner or analytical capability. `REPORT_PRESENTATION` has one semantic authority in `reporting/assemble.py`; its two renderers implement the same frozen contract. The layer arrows in §6 describe composition, not permission for reporting to import analysis and recalculate results.

## 17. SIT-D028: bounded capture and normalization

### 17.1 Accepted in-process domain and caller obligation

The accepted caller value is an exact built-in `dict` at the root. Recursively permitted concrete types are `dict`, `list`, `str`, `int`, `float`, `bool` and `NoneType`. Dictionary keys must be exact `str`. Subclasses, tuples, sets, Decimal objects, generators, custom mappings, PathLike objects inside evidence, and serialization callbacks are not admitted. Type checks precede conversion, equality, repr, hashing into a new map, or iteration through any custom object.

The caller must keep the entire reachable object graph unchanged throughout capture, using its own exclusive ownership or synchronization. The auditor neither acquires a supplied lock nor promises to detect arbitrary concurrent mutation. Observable size changes, failed indexed access, or other detected capture inconsistency abort with `execution_failed`; they never produce a claimed stable snapshot. Undetectable concurrent mutation is outside the supported library-call precondition. The file interface has its separately stated capture boundary in §20.

Capture uses an explicit bounded stack. Objects are inspected without modifying the caller's objects. An active-ancestor identity set detects a container referencing itself through any depth; this cannot represent a JSON tree and is `input_constraint_violation`. Repeated aliases outside the active ancestry are copied as separate JSON occurrences, and each occurrence consumes its own node/byte/work allowance. Aliasing is not evidence identity. No deep-copy protocol or user conversion method is invoked.

After capture, private immutable tagged values hold object pairs, array elements, scalars and exact number atoms. No reference to a caller-owned mutable container reaches analysis. Objects are ordered by key; dossier entity collections and contract-defined reference sets receive the semantic ordering in §17.4. Original narrative strings, time precision, native states and explicit gaps are preserved.

### 17.2 File decoding and exact numbers

The file reader supplies a bounded immutable byte sequence. UTF-8 decoding is strict: no replacement characters, BOM interpretation, invalid scalar values or lone surrogate acceptance. A bounded lexical preflight handles strings, escapes, number lengths, container depth and aggregate value counts before full object construction. The JSON decoder uses only project-owned duplicate-key and numeric hooks. Duplicate keys are checked after escape decoding; `a` and `\u0061` therefore cannot become two keys. Nonstandard NaN/Infinity forms are rejected. Python JSON defaults alone do not constitute admission. [W11-REF01]

Each numeric token is first checked against the 128-character ceiling. Integers and finite decimal tokens are then represented exactly by sign, coefficient digits and a base-ten exponent, without binary floating conversion, global Decimal-context dependence, exponent-sized zero allocation or expansion of a huge power. Internal number atoms are project values, not extra accepted caller types. [W11-REF02]

Zero has one mathematical representation, `0`; raw negative-zero spelling and trailing zeros are formatting, not additional evidence. For a nonzero atom, remove leading coefficient zeros and move trailing coefficient zeros into the exponent. If the mathematical value is integral, compare its decimal magnitude against 9007199254740991 before expansion, and reject an out-of-range value even when written with a decimal point or exponent. Emit admitted integral values as ordinary integer digits.

For a non-integral atom, consider two exact representations: ordinary decimal notation and the normalized coefficient followed by lowercase `e` and the exponent, with no plus sign or redundant exponent zeros. Compute candidate lengths before allocating. Choose the shorter representation; choose ordinary notation on a tie. Thus `0.50` becomes `0.5`, and `0.0001` becomes `1e-4`. Extremely small exponents remain compact. No rounding or underflow is permitted.

A finite built-in float is captured through its exact integer ratio. Convert the power-of-two denominator to an exact finite base-ten atom, then apply the same representation. This intentionally distinguishes a Python binary float `0.1` from the exact file decimal token `0.1`. A float `0.5` and file token `0.50` agree. A caller requiring an exact decimal unavailable as a short binary-float representation should use the file interface; Decimal/custom numeric objects are not implicitly admitted. If the exact shortest emitted numeric token exceeds 128 characters, reject it under that concrete numeric-token constraint. No float is silently rounded to make it fit. [W11-REF02]

### 17.3 Compact measuring representation J

`J` is the following deterministic UTF-8 JSON representation of an admitted value. It is an internal byte-measurement/serialization rule, not a source authenticity hash or a claim of RFC 8785 conformance.

| Component | Exact rule |
|---|---|
| Object | Keys in ascending Unicode scalar-value order; comma/colon separators with no surrounding space |
| Array | Original order for measurement; semantic set ordering only where §17.4 permits it |
| String | Double quotes; escape quote and backslash; no slash escape; no Unicode normalization |
| Escaped scalars | U+0000-U+001F, U+007F-U+009F, U+061C, U+200E-U+200F, U+2028-U+202E and U+2066-U+2069 use lowercase four-digit `\u` escapes |
| Other scalar values | Their ordinary UTF-8 encoding, including legitimate non-ASCII language |
| Number | The exact representation in §17.2 |
| Boolean/null | `true`, `false`, `null` |
| Framing | No BOM, indentation, trailing space or final newline |

The in-process WU9-L01 size is exactly the number of bytes J would emit, counted incrementally without materializing an over-limit string. A file is charged its actual raw bytes under WU9-L01. Thus whitespace or short escape spelling can affect the file boundary, while the constructed-object boundary has one fixed spelling. Cross-mode equivalence concerns successfully admitted equivalent values, not a promise that every padded file and object encounter the same transport-size guard. All other whole-payload limits apply in both modes, including inert extensions and unselected records.

WU9-L10 string lengths are measured after escape decoding as UTF-8 lengths, separately from J's encoded length. Structural string/identifier/range violations use the existing structural diagnostic. Aggregate byte/depth/node/work exhaustion uses the existing resource-interruption outcome. A local digest, when requested, covers only the original complete file byte sequence and never J for an in-process object.

### 17.4 Semantic normalization and validation order

Object key order has no semantics. Top-level inquiries, records, assertions and evidence references are sorted by their unique ASCII IDs. Contract-defined `*_refs` and `*_ref_ids` sets are sorted by target collection and ID after type/reference checks. Role bindings are ordered by their existing role name and bound reference. Paths retain traversal order. Narrative arrays and arrays inside inert extensions retain order unless the owning contract explicitly declares them sets. No universal recursive sort or deduplication is permitted.

The admission sequence is: trusted invocation validation; bounded capture and lexical/type checks; closed-key/required-field checks; unique identity and reference resolution; endpoint/claim and time-syntax checks; immutable indexing; bounded structural scope planning. Only then can `input_validation.state` become `accepted`. Qualification, conflict and completeness checks that affect analytical conclusions remain subsequent operations. A late asserted contradiction must already be present in the immutable index; it cannot be discarded as an unselected late input.

Normalized indexes use sorted entity/field tables with bounded binary lookup. No content hash, URL, publisher name or disconnected component merges identities. Source array permutation cannot affect completed analytical results. Raw-file position may still appear in a safe structural diagnostic before acceptance, since it describes that actual input representation.

## 18. SIT-D029: reports, representative witnesses and invocation outcomes

### 18.1 Report-local identity without hidden source fingerprints

The reference profile uses `report_id = SIT-RPT-000001`. It identifies the single report within an invocation, and is deliberately not globally unique or a hash of protected material. Report references must travel with input identity and contract/tool version; this constant cannot identify a report across dossiers.

Other report-local IDs are typed sequential identifiers with a six-digit minimum width: `SIT-SCP-`, `SIT-POP-`, `SIT-BAS-`, `SIT-CAP-`, `SIT-CHK-`, `SIT-RES-`, `SIT-FND-`, `SIT-RSN-`. Each collection starts at 000001. Distinct prefixes ensure report-local uniqueness. Input references remain in their separate typed namespace.

IDs are assigned after sorting semantic keys, never discovery order. A scope key consists of its Inquiry, exact Claim set, target set, dimension, view, temporal basis/time and the existing operation anchor. The operation anchor is the relevant assessment, evaluator role pair, pipeline run/stage/cohort, or correction channel/target/action/case tuple already required by the contract. Null has a fixed position before non-null values. Sets sort by typed reference; strings sort by scalar value; registered family IDs sort numerically.

Population keys use scope key, unit, selection rule and typed membership. Result keys use family, field key, scope key and operation anchor. Check keys use PC code and the Result key whose prerequisite they test. Reason keys use code, scope key, input references and exact detail/classification. Finding keys use condition, observation kind, scope key, subject references and selected witness. Basis keys use typed source reference and field/role selector; capability keys use Inquiry and family. Ties use J of the semantic body with report-local links represented by their already defined semantic keys. Dependency cycles among reasons/results do not recurse during naming: links use the target's anchor key, not its full linked body.

Identical explanatory objects may share one report-local entry. Distinct input records never disappear through this deduplication. Two unequal results with the same field/scope/operation anchor indicate an internal contract failure, not permission to pick one. All resulting links are checked before publication.

### 18.2 Finite witness policy

For a fixed start, target, view and scope, select the shortest eligible simple path; break equal-length ties by the lexicographic sequence of typed edge identities and destination node identities. A relation edge's identity includes its Assertion ID. A canonical record link uses collection, record ID, field/role selector and target ID, with no invented RelationAssertion. Array position is never a canonical record-link identity.

A bounded breadth-first distance pass followed by lexicographic predecessor selection provides the required mechanical strategy. A later implementation may optimize it only while preserving this representative rule and §19's charging behavior. It must not enumerate all walks or infer completeness from finding one short route.

For cycles, compute the strongly connected components of the eligible directed view with bounded deterministic node/edge order. For each cyclic component, choose its smallest typed node, then the shortest cycle through that node, with the same tie rule. A self-loop is a one-edge cycle. Retain the component's member/edge evidence needed for the stated finding; do not turn a representative cycle into a list of all cycles. For unordered positive member findings, retain the full required finite member set in typed-reference order.

All relevant conflicting assertions, frontiers and qualification blockers are collected independently of representative selection. A short origin path cannot certify that alternative parents were resolved. HHI still requires the full population gate. When witness/member limits would be exceeded, interrupt the affected operation rather than clip it and report success. No source rank is implied by lexical tie-breaking.

### 18.3 Exact output profile

JSON output is J of the frozen report followed by exactly one LF. Mathematical fractions retain original numerators/denominators. The reference profile omits optional `display_decimal` fields in JSON; For every available Result of value_kind fraction, Markdown also emits the fixed line `Decimal display: <numerator>/<denominator> = <six-place half-up value>` immediately after that Result block. Completion-interval endpoints retain their exact fractions without an extra decimal line. This selects an allowed presentation, not a new result. H7 remains 26/36, never a replacement decimal or 13/18-only payload.

The reference profile records start/end TimeValues as unknown, with null value/precision and the fixed explanation `not_recorded_by_SIT-RP-0.1`. The monotonic time guard still operates. No fabricated time, random report ID or timing field enters the report. `run.tool_name` is the project name, and `run.tool_version` is the actual installed package version once one exists. Before implementation no version is invented. `run.qualifications` identifies SIT-RP-0.1 and the omitted clock metadata.

Report arrays follow §18.1 and reporting §19.2. Source-native ordered arrays remain ordered. JSON bytes are identical for the same admitted normalized content, actual tool/contract/profile version, source mode, requested digest value and completed-operation state. Semantic comparison across file/object modes or raw-byte permutations excludes the already documented source-mode/digest metadata. Interrupted results can differ across machines because the wall-clock guard is real; that is outside byte-equality claims.

Markdown has the fixed title `# Source Integrity Audit`, then explicit report kind, processing state and input state. Root sections follow reporting §16.1's table order. Each root value is shown as JSON using J's string/number rules with two-space indentation, LF separators and one final LF. Results receive their own `### <Result ID>: <field_key>` headings, their complete object and a `Reason details` block containing their referenced reasons in canonical order. Thus an unavailable result is visible with its concrete reasons rather than a blank cell. The basis and finding sections preserve the remaining navigable detail.

Untrusted text appears only inside these code blocks, never as headings, link labels or raw HTML. The backtick fence length for a block is max(3, one plus the longest consecutive backtick run in its encoded body); the opening info string is `json`. The block contains no literal source newline/control escape that can terminate its structure. Locators remain inert inside code. Raw ordinary multilingual characters remain readable; the fixed control ranges in §17.3 appear as visible escapes. This uses CommonMark's code-block semantics and avoids placing user text in Markdown table cells. [W11-REF14]

The exact final filenames are `report.json` and `report.md`. Renderers receive no source-derived filename and never write independently. Both encode one frozen logical document, including diagnostic-only envelopes where applicable. Report parity means semantic agreement of all fields and disclosed limits; extra JSON indentation in Markdown does not change that meaning.

### 18.4 Closed invocation surface and outcome table

The future callable names remain `audit_bundle` and `audit_file`; the return sketches in §4 are completed as follows. `audit_bundle` returns the existing frozen report envelope, including its permitted diagnostic variants. `audit_file` returns a transport-only immutable outcome containing `document`, `publication_state` and `exit_code`. `publication_state` is `not_published`, `published` or `unknown`; it is not an analytical field or a new `sit-report/0.1` member. It records the I/O commit fact only.

Both operations may raise the documented `AuditAbort` when no conforming envelope can safely be delivered. Its fixed fields are processing state, input-validation state, one existing execution reason code, publication state and a safe constant message. It contains no arbitrary input, OS exception repr or local path. A known committed pair cannot be labeled not_published. An unobservable hard process termination may yield no return at all.

`options` is None or an exact built-in dictionary containing only `raw_file_digest`, an exact Boolean defaulting to false. True is permitted only for `audit_file`; it is a usage error for `audit_bundle`. No public subset, quota-raising/lowering, clock injection, custom output profile or callback option is selected for v0.1. Test harnesses may instantiate controlled internal quota/clock objects under later test authority; evidence and public options cannot do so.

The CLI is `sit audit INPUT --output OUTPUT_DIR`, optionally `--raw-file-digest`. INPUT and OUTPUT_DIR must be explicit absolute paths under §20. Unknown/repeated switches, extra arguments, an invalid option type or a prohibited invocation-path form cause usage failure before input access. No shell expansion, environment mode switch, response-file expansion or `@file` option is enabled. Help/version display contains only tool-controlled text.

| Established outcome | Python delivery | CLI exit | Publication |
|---|---|---:|---|
| Completed accepted audit, including legitimate unavailable fields | Existing completed audit envelope; file wrapper carries it | 0 | New complete pair for file mode |
| Structural rejection | Existing validation_diagnostics envelope | 2 | Diagnostic pair only if safe destination publication succeeds |
| Resource/cancellation interruption before acceptance | Existing processing_diagnostics/interrupted/not_completed envelope when deliverable | 3 | Complete diagnostic pair or no pair |
| Interruption after acceptance with finalization budget available | Existing interrupted audit; unfinished cells not_evaluated | 3 | Complete interrupted pair or no pair |
| Guard prevents conforming finalization | AuditAbort with actual acceptance state and resource_limit_reached; no salvaged scalar | 3 | No incomplete pair |
| Execution defect/I/O/protection/profile failure | Existing failed processing envelope when possible, otherwise AuditAbort/execution_failed | 4 | No pair before commit; preserve actual commit state after commit |
| Invalid trusted invocation | Safe usage exception, before dossier processing | 64 | None |
| Hard termination without a safe return | No result promise | Host-defined | Unknown unless commit was observed |

A native source event saying `failed` does not change exit 0 for an otherwise completed audit. Evidence quality never selects a process exit code. An output failure takes precedence over a prospective exit 0/2/3; it cannot publish an old Markdown report beside a new JSON report. Default terminal output is one fixed status line without user values. Filesystem result delivery and the analytical envelope are distinct, so a completed in-memory document cannot certify that its files were published.

## 19. SIT-D030: execution, accounting and honest stopping

### 19.1 Authority-free execution port

`contracts/execution.py` defines the internal budget/stop interface and transport types. `runtime/resources.py` implements the budget object; only project-owned instances are supplied. Its operations are charge/check and stop-state propagation. It exposes no file handle, network client, source mutation, policy callback or arbitrary caller function. Lower layers import only the contract. The runtime owns monotonic clock sampling and cancellation detection behind this port.

Analysis remains pure with respect to evidence and cannot gain I/O authority. Quota interruption is a controlled execution effect, independent of epistemic availability. Existing family modules have exactly their existing Trace owners.

### 19.2 Charging rules

Limits WU9-L01-WU9-L14 remain numerically unchanged. Check a prospective charge before the corresponding work; equality with a ceiling is permitted and the next charge stops. One invocation has a global ledger. An analytical job also has the existing per-capability/scope ledger; its charges go to both ledgers without double-counting the global ledger.

| Work | Charge |
|---|---|
| Inspect, create, copy or move one scalar/container/entity/reference/index entry | One unit for each visit or emitted occurrence |
| Examine one graph edge, canonical link, support record, prerequisite or lookup comparison | One unit per examination, including repeated examinations |
| Compare keys or process a string/byte sequence | One unit plus one unit per started 256-byte block inspected; bounded native calls precharge the conservative maximum inspected length |
| Read/decode/encode/hash bytes | One unit per started 256-byte block per pass, plus the entry visits above |
| Numeric conversion/arithmetic | One unit plus the started 256-byte blocks of bounded operands and allocated result digits; length/range checks precede expansion |
| Emit a result, reason, witness or witness-member entry | One unit per entry plus recursively visited payload/byte charges |
| Native I/O operation or permission check | One unit plus bounded buffer processing; kernel waiting is governed only cooperatively |

No hidden full scan is charged as a constant lookup. Sorting uses a stable bottom-up merge schedule, with every comparison and moved entry charged. Index lookup uses bounded binary search; equality still examines the relevant exact key. Raw JSON decoding may be a bounded standard-library call after lexical preflight has counted its whole input; precharge its known full byte/node traversal and check time immediately before/after it. The preflight itself is separately charged. These are a specified accounting model, not CPU-instruction counts or measured performance.

At invocation entry reserve and charge 1,024 global units for a fixed emergency-delivery/cleanup path capped at 4,096 diagnostic bytes and the tracked local handles/files. This is included within the existing 10,000,000-unit total. It cannot fund analysis or an oversized report. No second reserve or emergency restart raises the ceiling. The ordinary ledger therefore has 9,998,976 units after that charge, before other work. The emergency path may emit a safe AuditAbort rather than iterate over an unbounded result set. Any cleanup it cannot safely finish leaves private residue and stops.

### 19.3 Deterministic schedule and commit points

Preflight, capture, full structural validation, immutable index construction and a finite structural job plan occur before input acceptance and charge only the global ledger. The plan enumerates applicable Inquiry/family/scope jobs from existing record bindings; it performs no independence or coverage qualification. If even the job plan exceeds a guard, input remains not_completed and no analysis is salvaged.

Jobs run in ascending Inquiry ID, then numeric SIT-M family, then §18.1 operation/scope key. Within a job, prerequisite IDs and output fields follow their registry order. Fixed graph adjacency order is typed edge identity. No parallel execution or scheduler-dependent cache is selected in this profile.

Only the immutable raw record index is shared globally. Analytical traversal/qualification results may be reused within their current family/scope job; the creation and every consumption are charged. There is no cross-job semantic-result cache in SIT-RP-0.1. Calls to another module's pure helper are charged to the current job and keep that helper's semantic owner. This avoids double interpretation and free work hidden behind cached analysis.

A Result commits only after its required finite population, premises, conflicts, value, basis, reasons and witnesses have completed their checks. The value and its qualification commit together. A family completes only when all its planned scope cells finish an availability decision. Earlier committed cells can survive an interruption; a half-traced ancestor set cannot.

Check cancellation/time at every charge boundary, before and after each native or prepaid bounded call, and before each result commit. Charges processing blocks cannot exceed 256 bytes of source data without another check. A single OS call or bounded decoder call is not a hard real-time guarantee. The sixty-second monotonic deadline begins at processing entry and is never reset for another family, retry or renderer.

A stop aborts the remaining jobs. If the per-job quota or caller cancellation stops a job while global/time budget remains, attempt to finalize the existing interrupted envelope, marking unstarted cells not_performed/not_evaluated and the current unfinished cells interrupted/not_evaluated. Finalization is itself charged. If the global/time/output guard prevents that complete envelope, deliver the fixed safe abort; do not substitute a processing_diagnostics/not_completed envelope for a known accepted input. An internal defect instead uses failed processing and does not expose ordinary analytical salvage.

The witness-entry and witness-member limits count every retained occurrence in the report. Referencing an already retained Finding does not add another witness; adding another member occurrence does. Output byte counters are separate for each format. No byte cap, work cap or witness cap authorizes removal of a late contradiction or silent truncation. The release must test both below/at/above behavior and the honest no-report fallback.

## 20. SIT-D031: selected filesystem and platform protocol

### 20.1 Supported design profile and trust boundary

The proposed reference file profiles are **64-bit Linux with glibc exposing renameat2 on a local filesystem supporting RENAME_NOREPLACE**, and **64-bit Windows 11 on local NTFS**. The in-process profile is independent of these native I/O bindings. Supported CPython minors start at 3.11; actual release support is limited to minors/platforms passing the later test matrix. Future versions and macOS file support are not certified by this document.

The kernel, interpreter, native system libraries, local volume configuration and invoking principal are trusted. Malicious same-principal code, administrator/kernel compromise, hidden network mounts, hostile filesystem providers, backups, swap and cloud synchronization are outside the isolation claim. File inputs must be quiescent while captured. Detected identity/size/write-time changes fail the read; metadata checks cannot prove arbitrary non-mutation. The accepted evidence is the actual bounded bytes read. No claim of ongoing source authenticity follows.

All source locators remain unopened. Native operations below resolve only the explicit invocation paths. Absolute Linux paths and drive-rooted Windows paths are accepted after lexical validation. Reject `.`/`..` components, NUL, URI forms, UNC/network shares, caller-supplied device namespaces, Windows alternate streams and ambiguous trailing-dot/space components. Treat the root anchor as host configuration; every subsequent component is one relative name under a retained directory handle. Do not use realpath/resolve to follow links first and validate afterward.

No third-party Python package or executable is added. The two platform adapters use the standard library and fixed, allowlisted native entry points through `ctypes`. This is an explicit platform ABI dependency, not a claim of having no OS dependencies. It is documented in `DEPENDENCY_STRATEGY.md` §15. Missing symbols, unsupported flags, failed protection checks or unexpected native statuses fail closed. No shell utility, dynamic plugin, remote resolver or unsafe portable fallback is allowed.

### 20.2 Linux operations

Open the root and each intermediate directory with `os.open` using O_DIRECTORY, O_NOFOLLOW and O_CLOEXEC. Pass only one component with the retained parent `dir_fd` for subsequent operations. Verify each opened object with fstat and retain handles until the required operation finishes. Component-wise opening is necessary because O_NOFOLLOW alone concerns the trailing component. [W11-REF03, W11-REF05]

The supported path profile requires root/ancestor directories controlled by root or the invoking UID and no effective group/other write permission. Reject ambiguous or unsupported permission/mount arrangements. The chosen output parent is caller-owned, not group/other-writable, and on the supported local filesystem. These are conservative deployment preconditions; the tool does not chmod unrelated ancestors or use a public temporary directory as its report workspace.

Open the input leaf O_RDONLY | O_NOFOLLOW | O_NONBLOCK | O_CLOEXEC, then require a regular file before reading. O_NONBLOCK is not a hard-latency guarantee for regular files. Read bounded chunks from that descriptor only; compare fstat identity, size and modification metadata before/after and the selected entry's identity where safely checkable. A detected replacement or mutation fails. Do not reopen a source locator or material named inside JSON.

Create an exclusively named `.sit-stage-<32 random hexadecimal digits>` directory under the retained authorized parent with mode 0700. At most eight collision retries are allowed and charged. Open it without following links, verify ownership/mode/identity, and create `report.json` and `report.md` inside it with O_CREAT | O_EXCL | O_NOFOLLOW | O_CLOEXEC, mode 0600. Creation mode and verification must never grant group/other access; default ACL effects remain constrained by that effective mode. A more restrictive umask can make the operation fail; no global umask change is used.

After both complete representations and parity checks, flush their file data and close their file handles. Verify the stage directory and its two tracked entries, with no unexpected entry accepted. The stage remains inaccessible to other unprivileged users. Publish using the already loaded libc `renameat2(parent_fd, stage_name, parent_fd, final_name, RENAME_NOREPLACE)` entry point through a fixed typed ctypes binding. Do not call os.rename/os.replace or implement check-then-rename: those do not supply this no-clobber condition. Filesystem/flag unavailability is an error, with no fallback. [W11-REF04, W11-REF06]

The rename is the publication commit. A destination created concurrently causes failure without replacing it. Parent descriptors bind the authorized directory object; known ancestor/path replacement aborts before commit. Permission checks and the trusted-principal condition bound races that ordinary descriptors cannot prevent against an administrator or malicious same-UID process. Report publication promises a complete pair under one directory entry, not power-loss durability or global filesystem isolation.

### 20.3 Windows operations

Load only the installed system `ntdll.dll`, `kernel32.dll` and `advapi32.dll`, through fixed names and the system-directory search policy. Never use a source-supplied path or generic library discovery. Bind only the documented prototypes needed below, with pointer-size-aware structures, checked lengths and explicit handle lifetimes. No native callbacks are registered. [W11-REF04]

Open the trusted local drive root with user-mode NtCreateFile; then open each single relative child with the retained parent as ObjectAttributes.RootDirectory. Use FILE_OPEN for existing components, FILE_DIRECTORY_FILE for directories, FILE_OPEN_REPARSE_POINT and synchronous non-alert I/O with SYNCHRONIZE. Request only traversal/read-attribute/read-control rights for ancestors; permit ordinary read/write sharing but not delete sharing while their identity matters. Check each returned handle's type, reparse attributes, identity and local-volume profile before using it as the next parent. A reparse point is rejected, not traversed. This design does not depend on the disputed combination of OBJ_DONT_REPARSE with other flags. [W11-REF07, W11-REF08]

For the input leaf use FILE_OPEN, FILE_NON_DIRECTORY_FILE, FILE_OPEN_REPARSE_POINT, read-data/read-attributes and SYNCHRONIZE, with read sharing only. Read and query metadata through the same handle. A share conflict, reparse point, unsupported object or detected change fails safely. Do not treat FILE_OPEN_NO_RECALL as proof that arbitrary cloud/provider activity cannot occur; such volumes/providers are outside the supported local profile.

Determine the invoking process user SID through the process-token APIs. Impersonated invocation is outside this initial profile and is refused. Build a protected security descriptor with that SID as owner and the sole ordinary-access allow ACE granting full access. Apply the descriptor during FILE_CREATE of the stage directory and each report file, not after sensitive bytes have been written. Read the effective owner/DACL back through GetSecurityInfo; require the expected protected DACL and no broader ordinary access. Administrator/kernel privilege bypass remains outside the guarantee. [W11-REF07, W11-REF11, W11-REF12]

The stage name, collision count and fixed filenames are the same as Linux. FILE_CREATE provides exclusive creation. Keep the stage handle with DELETE and the required read-control/traverse rights; use explicit private descriptors for its files. Complete and FlushFileBuffers both files, then close their file handles before renaming the stage, because open children can prevent directory rename. Preserve the stage handle and parent handle. [W11-REF07, W11-REF10, W11-REF13]

Publish through SetFileInformationByHandle with FileRenameInfo, ReplaceIfExists false, the retained target-parent handle as RootDirectory and a single relative final basename. There is no replace flag, copy fallback or second independent file move. The returned success is the commit observation. A collision or sharing/ACL/native failure leaves no newly committed final pair from this invocation. The selected same-volume NTFS behavior must pass the later Windows test matrix; the documentation review does not count as that runtime evidence. [W11-REF09, W11-REF10]

### 20.4 Common completion, faults and cleanup

No source-derived value becomes an invocation filename. Refuse an existing destination, including a directory, file or redirection; do not overwrite or reuse it. Permissions are established before content. Both renderers finish under the existing byte/work/time guards before the commit operation. A guard immediately before commit stops publication; a kernel call already in progress remains subject to the cooperative-time limitation.

After observed commit, publication_state is published. Closing handles, terminal delivery failure or a subsequently observed deadline cannot retroactively make that false. Do not roll back or delete a committed report to manufacture a no-publication result. If termination prevents observing the commit result, delivery is unknown/no return. This makes explicit the point-of-no-return boundary of privacy §8.3: its no-final-pair rule applies to failures before a successful publication commit. It never authorizes a false negative statement about an already committed side effect.

Power-loss durability is not promised. File buffers are flushed before commit; no required post-commit write is introduced merely to relabel the visible pair durable. The logical report is frozen before I/O publication and cannot contain an invented claim that publication succeeded. The separate transport outcome carries that fact.

Cleanup before commit may inspect and remove only the two known stage files and the stage directory created by this invocation, using retained handles and verified identities. Never recursively walk arbitrary trees or follow a cleanup link. An unexpected object, changed identity or inability to verify safety leaves private residue; report only a safe fixed failure and stop. Crash recovery is a caller-authorized action on a specifically identified residue, not a background sweep. A new attempt must use a new destination and never recycle partial analytical values.

## 21. Written realization cases and future test binding

All cases below are prose obligations, not executed product tests. They supplement existing SIT-VF/SIT-VG cases without changing their expected meanings.

| Case | Concrete premise | Required outcome |
|---|---|---|
| W11-R01 | File object `{ "b":2, "a":1 }` and constructed object with reversed key order, in an otherwise admissible dossier | Measuring J fragment is `{"a":1,"b":2}` (13 bytes); equivalent completed content, with source-mode metadata distinguished |
| W11-R02 | File string contains literal `é` versus its escaped spelling | J uses two UTF-8 bytes for that scalar; same logical string, different optional raw digest |
| W11-R03 | String contains quote, backslash, LF and U+202E | Exact J escapes from §17.3; decoded length and encoded length remain different counters |
| W11-R04 | File numbers `0.50`, `1e-4`, `9007199254740991` and `9007199254740992` | First three preserve exact values; final integral value is rejected before inexact conversion |
| W11-R05 | File token `0.1`, built-in float 0.1, and float 0.5 | First two retain their distinct exact values; 0.5 agrees with exact file 0.50; no approximate rounding to create equivalence |
| W11-R06 | A list references itself; another ordinary list is reused twice without a cycle | Cycle rejected; alias is copied/counted twice without inventing two evidentiary identities |
| W11-R07 | A dict/list subclass has side-effecting methods | Reject exact type before invoking its methods; no repr-based diagnostic |
| W11-R08 | Caller mutates a container during capture | Observable inconsistency fails; unsupported concurrent access never receives a promise of atomic snapshot detection |
| W11-R09 | Constructed J size L01-1, L01, L01+1, with other limits valid | First two pass that size check; last interrupts. File whitespace affects only the raw-file boundary |
| W11-R10 | Permute entity collections and reference sets; keep narrative sequences unchanged | Same semantic keys, local IDs and completed report bytes at fixed transport metadata |
| W11-R11 | Diamond S→A→T and S→B→T with A before B and eligible equal-length edges | Select lexicographically earlier shortest witness; still examine all required parents/conflicts |
| W11-R12 | A cycle has an exit to an origin; input order is reversed | Same component and canonical cycle; the exit never erases the cyclic-lineage blocker |
| W11-R13 | Two Reasons link to Results that link back to the Reasons | IDs resolve from anchor keys without recursive hashing or discovery-order naming |
| W11-R14 | H7-01 completes | Retain 26/36 and all bucket/population evidence; optional JSON decimal absent; Markdown shows 0.722222 alongside it |
| W11-R15 | Source text contains a code fence, Markdown image, HTML tag and URL | Entire value remains in a sufficiently long code fence; no active image/link/heading; ordinary multilingual text preserved |
| W11-R16 | Native correction outcome says failed, versus malformed input, versus engine fault | Respectively completed audit/exit 0, validation diagnostics/exit 2, failed execution/exit 4 |
| W11-R17 | Unknown option, digest=true in object mode, or relative invocation path | Safe usage failure/exit 64 before reading evidence or creating files |
| W11-R18 | One full inventory commits, then a lineage job exhausts its local quota | Only completed cells survive if finalization fits; current search interrupted/not_evaluated, remaining jobs not_performed/not_evaluated |
| W11-R19 | Global budget or deadline expires during finalization | Safe abort/exit 3; no malformed envelope, invented not_completed state for accepted input, or clipped pair |
| W11-R20 | Charge reaches exactly a local/global ceiling and then requests another unit | Equality allowed; next operation not executed; reserved emergency cost remains within global total |
| W11-R21 | Two jobs use the same origin helper | Raw index may be shared; each job's semantic work is charged to that job/global ledger; no free cross-job cache |
| W11-R22 | The last indexed assertion contradicts a needed independence premise | It remains available to qualification regardless of short witness or source array order |
| W11-R23 | Ancestor or leaf path is a symlink/reparse point | Refuse before following it; retained handles never authorize a new locator read |
| W11-R24 | Destination appears after preflight but before commit | Native no-replace commit fails; pre-existing destination bytes and input bytes remain untouched |
| W11-R25 | Stage permission or ACL is broader than the approved profile | Fail before writing dossier-derived content; no chmod of unrelated parents and no permissive fallback |
| W11-R26 | Windows stage contains still-open report children | Close/flush tracked children before commit; unexpected open-handle failure is safe, not a copy/move fallback |
| W11-R27 | Second renderer or stage write fails | No final pair; only tracked safe cleanup; first staged representation is not a published report |
| W11-R28 | Crash before commit; later cleanup sees an unexpected link | Private residue remains; no automatic recursive cleanup or link following |
| W11-R29 | Native commit succeeds, then terminal delivery fails or process dies | Publication remains published if observed, otherwise unknown to caller; never claim rollback or overwrite |
| W11-R30 | Linux renameat2 missing/unsupported, or Windows non-NTFS/cloud path | Refuse unsupported file profile; no security downgrade; separately valid in-process calls do not load the I/O adapter |
| W11-R31 | Both outputs are complete | JSON is J+LF; Markdown uses root order and complete reasons; all 57 leaf meanings, state partitions and references agree |
| W11-R32 | Profile changes are proposed after this candidate | Reopen the owning semantic/resource/security contract before changing byte oracles; no hidden implementation default |

Future paths are `tests/contract/test_normalization_profile.py` for R01-R10; `tests/contract/test_realization_profile.py` for R11-R17/R31-R32; `tests/security/test_resource_profile.py` for R18-R22; and `tests/security/test_filesystem_profiles.py` for R23-R30. Existing owners/Trace IDs remain those listed for SIT-D028-SIT-D031. The additional test paths are planning assignments only.

## 22. Official technical basis and remaining implementation evidence

The following references were consulted on 2026-09-17 to check primitive behavior. No forum answer is treated as an OS contract. These technical facts support the design choices above; they do not appear as new theory-map entries, prove this composition secure, or replace later executable tests.

| Reference | Narrow factual basis | Official source |
|---|---|---|
| W11-REF01 | JSON hooks, duplicate-name/default numeric behavior | `https://docs.python.org/3.11/library/json.html` |
| W11-REF02 | Exact decimal conversion and binary-float distinction | `https://docs.python.org/3.11/library/decimal.html` |
| W11-REF03 | Descriptor-relative operations and platform support checks | `https://docs.python.org/3.11/library/os.html` |
| W11-REF04 | Typed native-library bindings and system-library loading | `https://docs.python.org/3.11/library/ctypes.html` |
| W11-REF05 | openat, leaf O_NOFOLLOW, O_EXCL and open-descriptor identity | `https://man7.org/linux/man-pages/man2/open.2.html` |
| W11-REF06 | Atomic rename and RENAME_NOREPLACE filesystem requirement | `https://man7.org/linux/man-pages/man2/rename.2.html` |
| W11-REF07 | User-mode NtCreateFile, RootDirectory, disposition, sharing and creation descriptor | `https://learn.microsoft.com/en-us/windows/win32/api/winternl/nf-winternl-ntcreatefile` |
| W11-REF08 | FILE_OPEN_REPARSE_POINT and user-mode Nt naming | `https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/nf-ntifs-ntcreatefile` |
| W11-REF09 | Relative target-parent handle and ReplaceIfExists=false | `https://learn.microsoft.com/en-us/windows/win32/api/winbase/ns-winbase-file_rename_info` |
| W11-REF10 | Handle-based rename, same-volume/child-handle constraints | `https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-setfileinformationbyhandle`; `https://learn.microsoft.com/en-us/windows-hardware/drivers/ddi/ntifs/ns-ntifs-_file_rename_information` |
| W11-REF11 | Owner and DACL retrieval by handle | `https://learn.microsoft.com/en-us/windows/win32/api/aclapi/nf-aclapi-getsecurityinfo` |
| W11-REF12 | Creation of a security descriptor from controlled SDDL | `https://learn.microsoft.com/en-us/windows/win32/api/sddl/nf-sddl-convertstringsecuritydescriptortosecuritydescriptorw` |
| W11-REF13 | File-buffer flushing | `https://learn.microsoft.com/en-us/windows/win32/api/fileapi/nf-fileapi-flushfilebuffers` |
| W11-REF14 | Fenced code blocks preserve literal content | `https://spec.commonmark.org/0.31.2/` |

The completion leaves implementation and test execution in later authorized phases. Native ABI layouts, symbol presence, exact bytes, race/fault behavior, selected Python/package versions and platform matrix results must be checked there. These are implementation evidence gates with fixed specification targets, not permission to leave another unspecified Phase 0 protocol. A failed feasibility or security test reopens the corresponding decision before release.
