# PHASE_2_PLAN

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Phase | Phase 2: Bounded Ingestion, Schema Mapping, Validation and Observability Preparation |
| Target release | v0.1; no release or publication in this phase |
| Plan revision | 0.1 |
| Date | 2026-09-18 |
| Status | PROPOSED FOR OWNER APPROVAL |
| Theory Owner | Xiangyu Guo |
| Technical Owner | Unassigned |
| Repository | `DavidWallstructurallaw/source-integrity-toolkit` |
| Planning intake / accepted Phase 1 merge | `d7d73a790a2a627d19307c9dd48281eff3017023` |
| Intake tree | `837cb01265c22cb17bea66b2e7e1f8a7e1006924` |
| Accepted completion | `PHASE_1_COMPLETION.md` revision 1.0; PR #8 merged |
| Current instruction | `制定并提交 PHASE_2_PLAN.md` |
| Current write scope | This file only, on a planning review branch |
| Execution authorization | Not granted; requires approval of this plan and the named work unit |
| Proposed work units | P2-W01 through P2-W09, sequential, with review stops |
| Public auditing / analytical implementation | Remains unavailable throughout this phase |

## 1. Authority, source basis and planning boundary

The owner accepted `PHASE_1_COMPLETION.md` and merged PR #8. The merge records that acceptance and preserves the reviewed tree. The current instruction authorizes drafting and submitting this plan. It does not authorize any implementation described below, merge of the planning PR, or execution of all work units in advance.

Phase 0 specifies v0.1 behavior and Phase 1 establishes its scaffold. Neither fixes a complete numbered implementation schedule after Phase 1. The component allocation, private integration seams, schema delivery choice and test transition in this document are therefore explicit Phase 2 proposals. Approval adopts this allocation within the existing product contract; it does not amend the frozen theory or public input/report meanings.

### 1.1 Controlling records

| Source | Governing use |
|---|---|
| `PHASE_0_APPROVAL.md` revision 1.1 | Exact eighteen-file Phase 0 baseline; original approved snapshot `7d2e5fcaff591641b5cefce00e71e88941dd1f95`; authorized W01 digest correction |
| `PHASE_0_PLAN.md`, `PROJECT_INSTRUCTIONS.md` | Authority, scope, source discipline, work-unit acceptance and no silent repair |
| `V0.1_PRODUCT_SPEC.md`, `DEFINITIONS_AND_UNITS.md` | Product boundary, units and epistemic distinctions |
| `CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` sections 2-9, 12-14, 18-20, 24-28 | Canonical records, assertions, references, input preservation and immutable H7 cases |
| `OBSERVABILITY_AND_REPORTING.md` sections 12-17 | Input/result/processing distinctions, 24 prerequisites, 40 reasons, per-scope capabilities and five non-cumulative domains |
| `REPOSITORY_ARCHITECTURE.md` sections 5-6, 16-20 | Module ownership, dependency direction, exact input capture/J representation, execution accounting and deferred native I/O |
| `GOVERNANCE_AND_HANDOFF.md` section 22 | Binding numeric-guard, cancellation and other WU11 precision resolutions |
| `DEPENDENCY_STRATEGY.md` sections 2-9, 14-16 | Standard-library runtime, native restrictions and numeric-guard classification |
| `PRIVACY_AND_DATA_HANDLING.md`, `SOURCE_INTEGRITY_THREAT_MODEL.md` | Inert content, protected commonality, safe diagnostics, fixed ceilings and non-intervention |
| `VALIDATION_PLAN.md`, `SUCCESS_CRITERIA.md`, `THEORY_TO_CODE_TRACEABILITY.md` | Field/shared tests, success criteria, exact oracles and Trace ownership |
| `SPEC_AUDIT.md`, `THEORY_SOURCE_MAP.md`, `UNRESOLVED_DECISIONS.md` | Adopted source interpretation, distinctions and historical decisions |
| `LICENSING_NOTES.md`, `LICENSE`, `NOTICE` | Apache-2.0 engineering scope and exclusions |
| `PHASE_1_PLAN.md`, `PHASE_1_COMPLETION.md`, merged PR #8 | Accepted scaffold, limitations, repairs, retained tests and completion evidence |
| `scaffold/` catalogs and delivery/baseline manifests | Historical source-bound indexes and byte identities, not runtime policy files |

Earlier pending headers remain historical. Later approval and merge records establish adoption without changing those bytes. Governance section 22 controls the points it explicitly refines; the older architecture shorthand cannot override it.

The six theory sources remain EBC, UIL, BVL, HDL, EC and SIL under the adopted source register. The papers supplied in this conversation do not silently replace a frozen version or expand this implementation phase. Phase 2 consumes their adopted engineering operationalizations through the source map. It does not implement entropy, mutual information, semantic-gradient, capture-flow, trust-weighting or universal-integrity scores. It does not copy paper PDFs or long source extracts into the repository or distributions.

### 1.2 Present deliverable

Submit only `PHASE_2_PLAN.md`. Do not create progress files, schemas, test fixtures, code, dependency changes or workflows while submitting the plan. Existing Phase 1 CI may run normally on the planning PR; such a run tests the unchanged scaffold and does not validate unimplemented Phase 2 behavior.

## 2. Proposed Phase 2 product slice

Phase 2 builds the internal, bounded preparation path that later analysis will consume:

`caller-owned built-in value OR already supplied immutable UTF-8 bytes -> bounded capture/decoding -> canonical mapping -> structural/reference/time validation -> immutable indexes and explicit scope plan -> evidence-domain preparation`

The output is a private in-memory preparation outcome. It contains accepted input or safe rejection/interruption information and an honest account of which evidence has been supplied and which analytical checks remain unperformed. It contains no computed source-integrity result and is not a `sit-report/0.1` audit.

### 2.1 Included work

Implement the adopted closed object/record/assertion structure, exact scalar preservation, J byte measurement, duplicate-key and identifier discipline, required/nullable fields, canonical enums and references, structurally checkable time and claim compatibility, immutable input capture, bounded work and safe input diagnostics. Build a finite structural job/scope plan from explicit input bindings. Prepare non-cumulative evidence-domain navigation without qualifying origins, independence or correction effects.

Create the machine-readable input structure schema and a source-to-code/schema coverage record. Runtime validation remains project-owned. Preserve missing, withheld, disputed and attributed information without treating successful admission as authenticity.

### 2.2 Public interfaces and file boundary

`audit_bundle`, `audit_file`, the package-root exports and the current CLI remain their accepted Phase 1 refusal interfaces. The two audit functions still immediately raise `NotImplementedError`; an audit command still returns scaffold exit 1 without inspecting paths or producing a report. No new public CLI command, public byte-input mode, installed validator service or misleading successful audit is added.

The private component entry points are proposed as `_prepare_value(value)` and `_prepare_utf8(raw)` in `runtime/boundary.py`. The former accepts the adopted exact built-in root-dict domain. The latter accepts exact immutable `bytes` only, representing bytes already obtained outside the component. It does not accept paths, streams, callbacks, bytearray, memoryview or arbitrary coercible objects. These names are internal integration seams and are not re-exported or a compatibility promise.

The bytes seam realizes the decoding component needed by the future file interface. It does not claim to have safely opened a file. Native path traversal, Linux descriptor-opening policy, Windows handle/ACL logic, raw-file digest publication, output directories and report-pair publication remain unimplemented. Tests may read fictional repository fixtures before passing their bytes to the component; that test-harness read cannot be attributed to product file-interface conformance.

This allocation defers the complete file/public-audit path to a separately approved implementation plan. None of its existing v0.1 obligations is removed or marked passed.

### 2.3 Explicit exclusions

Do not implement graph projections, ancestor traversal, cycle detection over evidence relationships, finite path/cycle witness selection, origin boundaries, process-independence qualification, source inventories as public metrics, HHI, source allocation, evaluator overlap, externality qualification, stage/retention fractions, correction reachability/grants/effects, human-judgment qualification, threat findings, semantic interpretation of text or any M001-M015 result value.

Do not implement JSON/Markdown audit rendering, report-local identifiers, report publication, native bindings, live fetching, external schema resolution, model calls, active poisoning/prompt detectors, automatic quarantine, source contact, background jobs, caching across invocations, registry services, shared toolkit internals or package publication.

A container cycle in a Python object is an admission defect to detect. A cycle in correctly formed supplied provenance is data to preserve. The permission to detect the first does not authorize the second algorithm.

## 3. Fixed semantics at the implementation boundary

### 3.1 Capture, precision and resource behavior

Use architecture section 17 exactly, including exact-type admission, no custom conversion callbacks, active-ancestor container-cycle detection, separately counted repeated aliases, strict UTF-8, duplicate decoded JSON keys and preservation of ordered versus set-valued arrays. Do not trim, case-fold or merge IDs, names, locators, models or versions.

Use the adopted exact decimal-number atoms and finite-float integer-ratio conversion. A file decimal `0.1` and a built-in binary float `0.1` need not capture as the same exact value. `0.50` and exactly representable float `0.5` do. Preserve stricter field-type rules even where generic numeric normalization would yield an integer. No bool becomes a count.

J is required here for input measurement and deterministic normalized data. That permission does not authorize the later report serializer. The byte-input ceiling measures actual supplied bytes; the constructed-object ceiling measures J. No raw-file digest is invented for either internal seam.

The existing resource ceilings and accounting rules are unchanged. WU9-L01-L10 and the preparation-relevant global work/time portions of L11-L12 must be enforced before or during the work they bound. Charge scans, copying, comparisons, sorting, reference checks and decoding; include inert extensions and records outside selected analytical scopes. Retain the 1,024-unit emergency reserve within the 10,000,000-unit total and the cooperative, non-resetting 60-second processing guard.

L11's later analytical capability/scope accounting and L13-L14's witness/report limits stay recorded but unexercised for absent operations. No preparation test closes them as implemented. Do not raise a ceiling to admit a difficult fixture. Below/at/above tests must identify the particular guard reached rather than assuming every threshold is independently reachable under all other limits.

The 128-character numeric-token ceiling is a resource guard, including exact emitted in-process numeric tokens. Out-of-range exact integers, malformed scalar values and field-type violations are structural errors. Governance section 22.1 and dependency section 16 govern this distinction.

### 3.2 Preparation outcomes and diagnostics

The internal outcome records preparation execution separately from input acceptance. It may establish `accepted` only after full bounded capture, all structural/reference/type/time-syntax checks, immutable indexes and the finite structural scope plan are complete. Decoding alone cannot establish acceptance. No partly admitted snapshot may be consumed after rejection, capture failure or pre-acceptance interruption.

Preparation completion never sets `report_kind=audit_report` or claims `run.processing_state=completed` for a full audit. Private transport records must be labeled as preparation records, contain no public analytical arrays and never masquerade as a new output schema. They may preserve existing diagnostic codes and input-state meanings without serializing a report.

Use fixed, bounded diagnostics that omit arbitrary source values, local paths, unknown key strings and exception representations. Preserve authorized input content only in the prepared private object, not in logs, repr, debug dumps or failure messages. No telemetry or persistent input copies are permitted.

Resource interruption, actual execution failure and caller cancellation remain distinct. Propagate `AuditCancelled` or the equivalent adopted payload-free cancellation transport, with the actual input state; never relabel cancellation as `resource_limit_reached`, missing evidence or `execution_failed`. Public CLI cancellation behavior remains deferred with public auditing. An internal error must not produce a usable partial snapshot or a recycled successful outcome.

The caller retains the adopted no-concurrent-mutation obligation. Detectable capture inconsistency fails safely. No test or documentation may promise detection of arbitrary concurrent mutation or hostile same-process code.

### 3.3 Structural acceptance preserves semantic uncertainty

Reject malformed envelopes, duplicate IDs, accidental dangling references, forbidden canonical keys/predicates/enums, invalid reference kinds, prohibited claim-binding combinations and malformed time syntax under the existing input contract.

Accept compatible explicit `UnresolvedReference` records, lawful nulls with their required Gaps, protected identifiers, unsupported documentary labels, correctly formed denied/inactive assertions, conflicting records and provenance cycles. Preserve them for later scoped analysis. A well-formed temporal inconsistency can receive a scoped input observation; it cannot become a structural rejection merely because later analysis would be limited.

Do not resolve grant applicability, causal change attribution, relevant ancestry conflicts or boundary-instant conventions that have not been specified for the owning analysis. Retain their raw values and pending duties. A reference/type check must not silently become a graph or epistemic-qualification check.

### 3.4 Observability preparation has a deliberately limited claim

The five Level 0-4 labels retain reporting section 15's evidence-domain meanings and remain non-cumulative. Preparation indexes the exact supplied records and declared anchors associated with those domains. It never emits an overall/max level or turns a source-type label into evidence of quality.

For every Inquiry, retain all fifteen family slots and their applicable explicit anchors. Retain all 57 field obligations and the 24-PC vocabulary in the coverage record. Absence of an applicable binding may be recorded after the required finite structural scan. A missing lineage record cannot establish no real-world lineage or automatic `not_applicable`.

**Only PC01 is completed as a public prerequisite question by Phase 2.** Parts of PC02-PC24 may have finite input observations, such as an explicit seed list, time field, role binding or reference availability. Record these as constituent observations with their exact source selectors. Do not publish a full `met`, `unmet` or `unknown` PC outcome unless the complete owning check has actually been implemented under a later authorized unit.

The other 23 whole checks remain execution-pending in private preparation metadata, separately from observed missing/withheld input. A missing implementation is not unknown provenance. There is no new PC state, report reason code or public result state. In particular, do not evaluate PC07, PC11, PC12 or PC19-PC21 as a shortcut to origin, independence, HHI or correction analysis.

The prepared domain index contains supplied-record references and pending-check references, not fabricated `available_result_refs`. All M001-M015 calculations remain unperformed. A domain may contain supplied correction evidence despite unresolved acquisition ancestry; preserve both without claiming a qualified correction result. Full public `observability_domains` assembly waits for real Results and the report phase.

## 4. Schema mapping and contract representation

Schema mapping means mapping the one canonical `sit-bundle/0.1` dossier to the internal immutable record model. No CSV, JSON Lines, PDF, HTML, arbitrary key alias, user-authored mapping expression, compatibility coercion or inferred relationship is added.

The proposed schema artifact is `schemas/bundle/sit-bundle-0.1.schema.json`, using JSON Schema Draft 2020-12 with local references only. It describes the JSON-expressible structural portion: core keys, required fields, kinds, nullable branches, enums and local shape constraints. Its title/description and README must state its exact coverage and the mandatory parser/global-validator layers.

Duplicate raw keys, raw bytes, exact Python types, UTF-8 byte lengths, global identity/reference constraints, budget exhaustion and epistemic qualification are not all represented by JSON Schema. `format` alone is not the toolkit's date validator; JSON Schema's mathematical integer type does not override a stricter input field rule. Do not imply that passing this structural aid establishes full dossier acceptance. [EXT01]

Runtime modules do not read this schema or any `scaffold/`, `phase2/`, fixture or golden file. Project-owned validation uses source-bound compiled declarations and explicit checks in the authorized modules. No generic JSON Schema engine, dynamic predicate registry or new dependency is installed. Static schema/declaration checks and independently authored branch cases must detect drift. Do not implement an unrelated general-purpose schema interpreter merely to claim meta-schema validation.

Input schema delivery does not deliver `sit-report/0.1` schema. Leave the report reservation truthful. Any unsupported or ambiguous mapping is a stop condition, not permission to relax the schema or edit the original fixture.

## 5. Phase transition, frozen artifacts and regression policy

### 5.1 What remains frozen

Keep the eighteen Phase 0 files, corrected approval, Phase 1 plan/completion/progress, Phase 1 delivery manifest, baseline manifest, original trace/obligation/module catalogs and all H7 inputs/logical expectations byte-identical. Their historical snapshot meanings remain valid when later authorized implementation files change.

The Phase 1 delivery manifest is bound to its named predecessor snapshot. Do not rewrite it to current implementation hashes and do not use it as a requirement that approved Phase 2 code can never change. Create separate entry/delta records under `phase2/`.

The root exports, `api.py`, `cli.py`, all graph/analysis modules, all report renderers, native I/O/output modules and `runtime/disclosure.py` remain exact Phase 1 bytes. License files, developer pins and `MANIFEST.in` remain unchanged. Package version remains `0.1.0.dev0`, with README clearly distinguishing the implemented private preparation components from unavailable public auditing.

### 5.2 Closed implementation module ceiling

Exactly these thirteen existing modules may acquire behavior, only in their authorized units. No new installed package path is proposed; the total stays 48.

| Existing path under `src/source_integrity_toolkit/` | Primary permitted Phase 2 responsibility |
|---|---|
| `contracts/bundle.py` | Immutable captured/normalized structures and exact scalar value types |
| `contracts/evidence.py` | Canonical record, assertion, attribution and reference representations |
| `contracts/constants.py` | Adopted closed vocabularies and constants; preserve package version |
| `contracts/execution.py` | Authority-free budget and safe preparation/cancellation transports |
| `contracts/report.py` | Private observability-preparation structures and declarative domain/check bindings; no report builder |
| `io/input_file.py` | Bounded decoding of already supplied bytes; no file opening |
| `validation/limits.py` | Input-specific ceiling/counting rules |
| `validation/structure.py` | Closed shape and canonical mapping checks |
| `validation/references.py` | Snapshot-wide identity, reference and endpoint compatibility |
| `validation/semantics.py` | Input-only claim/time/lifecycle consistency observations |
| `runtime/resources.py` | Project-owned preparation budget, deadline and stopping mechanism |
| `runtime/diagnostics.py` | Safe fixed input diagnostics |
| `runtime/boundary.py` | Private preparation orchestration and domain preparation using the preceding owned contracts |

Keep the existing logical owners and import direction. Runtime orchestrates; it cannot redefine the record or report semantics. Contract modules cannot import runtime, validation, analysis or I/O. The budget interface is declared in contracts and implemented in runtime; consumers do not acquire filesystem or callback authority.

### 5.3 Transition existing tests before implementing behavior

Phase 1 tests deliberately require docstring-only modules and exact historical implementation blobs. They cannot be reused unchanged against the thirteen authorized live components. P2-W01 explicitly migrates those structural expectations while preserving their intent and historical evidence.

Create a reviewed transition ledger for every retained, adapted or superseded test assertion and its replacement entry point. Preserve actual Phase 1 test identities/results as historical evidence. Never present the old 194 count as a permanent target or silently drop tests to keep that number green. No blanket skip, xfail, marker deselection or generic-exception success is permitted.

The live guard must independently anchor the fixed baseline, 48 paths, protected 35 modules, authorized thirteen-file ceiling, import directions and current accepted step. A phase2 metadata file cannot authorize an extra module or bless a forbidden body by editing its own checksum. Include a paired mutation of policy plus code to test this. Hashes alone do not replace behavior, syntax and isolation tests for authorized implementation modules.

The historical `scaffold/module_manifest.json` stays unchanged. Adapt the live tests to distinguish that historical record from the Phase 2 policy; do not falsely relabel all original catalog entries implemented. New evidence records track component-level implementation and tests without closing entire analytical Traces.

## 6. Execution rules common to all units

Use a review branch based on the latest accepted predecessor for each unit. Record the actual entry commit, plan approval and any scope repairs in `PHASE_2_PROGRESS.md`. Stop after each review package. No automatic merge, force-push, branch deletion, release, repository-secret or branch-protection change is authorized.

`PHASE_2_PROGRESS.md` is the sole universally writable path. Other repeated paths are writable only where explicitly listed. A listed module may be edited only for that unit's described function. Directory labels and test filenames do not authorize arbitrary descendants or behavior. Corrections outside the current allowlist require a separately named narrow authorization.

The accepted plan itself becomes read-only. Pin its actual complete bytes in the entry record after it exists; do not invent its own hash or approval commit. Track later file changes as deltas against the entry snapshot. File deletion/renaming is not proposed by this plan.

Only fictional fixtures and synthetic privacy canaries are permitted. Test mutation occurs in private temporary copies. No new real dossier, identity map, paper PDF, credential or long third-party passage is admitted.

Retain the approved development pins and read-only CI posture. Recheck actual pins/actions and security applicability at execution; an unavailable or newly unacceptable dependency is a recorded stop, not a silent upgrade or fallback. No new runtime or development package is selected here. The existing Linux/Windows and Python 3.11/3.13 matrix remains the required starting matrix; actual patch and runner-image versions are recorded per run.

## 7. P2-W01: Entry verification, guard migration and cumulative CI

### Allowed paths

```text
PHASE_2_PROGRESS.md
phase2/entry_manifest.json
phase2/transition_ledger.md
phase2/module_policy.json
phase2/implementation_evidence.json
phase2/ci_review.md
tools/check_scaffold_boundary.py
tests/scaffold/test_imports.py
tests/scaffold/test_module_manifest.py
tests/scaffold/test_no_runtime_implementation.py
tests/scaffold/test_layer_boundaries.py
tests/scaffold/test_contract_catalogs.py
tests/scaffold/test_ci_contract.py
.github/workflows/phase1-ci.yml
tests/contract/test_phase2_transition.py
README.md
```

### Work and acceptance

Verify the actual 124-file Phase 1 tree, accepted completion, merge record, immutable baseline and planning commit. Run the existing baseline checker on the complete checkout. Record entry hashes without including self-referential future records.

Migrate only phase-specific docstring/hash assertions and the CI collection/driver policy. Retain all independent baseline, ownership, source-bound catalog, malicious mutation, API refusal, native/network, packaging and fixture assertions. Update the same reviewed workflow and driver in lockstep for cumulative Phase 2 collection, labels, artifact identity and phase-aware guard invocation. Include contract, unit and integration tests as they are introduced; prove collection identities match results. Keep all four matrix rows, minimum read permissions, immutable action pins, finite timeouts and explicit evidence uploads. No broad cache or source upload is added.

The current-stage policy begins with all product modules still at their Phase 1 bytes. Future promotions must match this plan's unit/path table and be recorded when implemented; approving this transition alone does not authorize thirteen arbitrary module bodies. Establish deliberate violations for extra paths, unauthorized promotions, dependency cycles, source-file/native/network access, scope-file self-approval and fake report returns.

No product module or schema file changes in W01. README explains the accepted scaffold and proposed/approved implementation boundary accurately.

**Checks:** actual baseline; complete path accounting; old-to-new test obligation mapping; positive and adversarial transition controls; cumulative CI on the exact W01 head; unchanged product/package/fixture bytes.

**Stop:** a missing old test obligation, a metadata-only bypass, a required failed/uncollected test, a workflow permission increase or any product implementation in this unit.

## 8. P2-W02: Canonical representations and input structure schema

### Allowed paths

```text
PHASE_2_PROGRESS.md
phase2/module_policy.json
phase2/implementation_evidence.json
phase2/input_contract_coverage.json
schemas/README.md
schemas/bundle/README.md
schemas/bundle/sit-bundle-0.1.schema.json
src/source_integrity_toolkit/contracts/bundle.py
src/source_integrity_toolkit/contracts/evidence.py
src/source_integrity_toolkit/contracts/constants.py
src/source_integrity_toolkit/contracts/execution.py
src/source_integrity_toolkit/contracts/report.py
tests/contract/test_bundle_contract.py
tests/contract/test_evidence_basis.py
tests/contract/test_input_schema_mapping.py
```

### Work and acceptance

Implement immutable internal value/record structures, exact numeric atoms, declared safe transport types and static vocabulary/field declarations. Cover Inquiry, twelve record kinds, all 24 relation predicates, nine assessment kinds and shared TimeValue, Gap, Provenance, EvidenceReference, RoleBinding and unresolved-reference structures. Preserve structural null exceptions and attribution exactly.

This unit defines internal models and declarative mappings. It does not expose unbounded public constructors as successful ingestion, parse arbitrary caller objects or establish whole-bundle acceptance. Any private constructor precondition must be explicit and checked at the later boundary.

Deliver the structural schema under section 4. `input_contract_coverage.json` maps each authoritative field/branch to representation, schema location where applicable, runtime-validator owner and required positive/negative/missing/boundary tests. Mark unimplemented runtime checks pending. Structural-schema limitations are named, not hidden in a permissive empty branch. All `$ref` targets are local; no external lookup occurs in tests or runtime.

**Checks:** exact enum/kind/predicate sets; required/nullable branch mapping; immutable representation; declaration/schema disagreement mutations; no coercion, hidden default or invented domain field; all existing applicable regression tests.

**Stop:** an input field cannot be mapped without choosing new semantics, a schema constraint contradicts a resource-stop category, any supplied provenance becomes certified, or a framework/dependency is needed without approval.

## 9. P2-W03: Preparation budgets, exact measurement and safe failures

### Allowed paths

```text
PHASE_2_PROGRESS.md
phase2/module_policy.json
phase2/implementation_evidence.json
src/source_integrity_toolkit/contracts/bundle.py
src/source_integrity_toolkit/contracts/execution.py
src/source_integrity_toolkit/validation/limits.py
src/source_integrity_toolkit/runtime/resources.py
src/source_integrity_toolkit/runtime/diagnostics.py
tests/contract/test_normalization_profile.py
tests/security/test_input_resource_limits.py
tests/security/test_input_diagnostics.py
```

### Work and acceptance

Implement the authority-free execution port, preparation-relevant ledgers, reserve, monotonic deadline and exact measuring primitives before untrusted capture/validation can run. Keep project-owned context creation separate from test-only controlled clocks/ledgers. Evidence, public options and environment variables cannot select or raise budgets.

Implement J scalar/length mechanics and exact numeric normalization, including checked exponent arithmetic that never allocates exponent-sized powers or zero strings. Count decoded strings separately from escaped JSON bytes. Budget all copies and sorted-index operations; local helper calls cannot hide uncharged scans. No full report renderer or native I/O is introduced.

Implement payload-free resource/failure/cancellation transports and bounded safe diagnostics using the existing classification rules. Source text, identifiers, keys, methods, exceptions and locators must not leak into incidental output. Preserve the distinction between original source-native states and processing outcomes.

**Checks:** applicable below/at/above limits; reserve arithmetic within the total; adversarial exponents and exact float tokens; Unicode/control accounting; booleans; interruption before/after an atomic component action; separate cancellation/failure; synthetic canaries on every diagnostic surface.

**Stop:** unsafe allocation before a guard, reset/lowered accounting, fake error classification, observable input leakage or a claim that report/witness/native budgets have been validated.

## 10. P2-W04: Bounded UTF-8 decoding and caller-value capture

### Allowed paths

```text
PHASE_2_PROGRESS.md
phase2/module_policy.json
phase2/implementation_evidence.json
src/source_integrity_toolkit/contracts/bundle.py
src/source_integrity_toolkit/io/input_file.py
src/source_integrity_toolkit/validation/structure.py
src/source_integrity_toolkit/validation/limits.py
src/source_integrity_toolkit/runtime/boundary.py
tests/unit/test_input_decoding.py
tests/unit/test_value_capture.py
tests/contract/test_normalization_profile.py
tests/security/test_input_capture.py
```

### Work and acceptance

Implement the two private capture paths and bounded lexical preflight. Reject duplicate keys after decoding, invalid UTF-8, lone surrogates, non-JSON forms, unsafe numbers and unsupported exact Python types. Keep keys and ordered narrative content unchanged except for the adopted numerical/string representation rules.

Capture through a bounded explicit stack with alias-occurrence accounting, container-cycle rejection and no mutable caller reference retained. Precharge any bounded standard-library decoding pass as required by the adopted ledger. A schema or application parser cannot be invoked as an unbounded preliminary convenience.

These entry points are incomplete until W05 finishes global validation and scope planning. They may return private captured values to component tests but must not claim `accepted` at this stage. Public audit stubs stay untouched. `io/input_file.py` never opens a file despite its reserved final name.

**Checks:** file-content/object equivalent pairs with transport-size distinctions; decoded duplicate keys; invalid suffix after valid prefix; subclasses with dangerous conversion/iteration/repr methods; aliases/cycles; preserved original input; cancellation/resource stops; no path/network/native activity.

**Stop:** pre-validation acceptance, a user callback/custom method invocation, loss of precision or source text, file opening or silently rounded/trimmed/merged data.

## 11. P2-W05: Full structural, identity, reference and time validation

### Allowed paths

```text
PHASE_2_PROGRESS.md
phase2/module_policy.json
phase2/implementation_evidence.json
phase2/input_contract_coverage.json
src/source_integrity_toolkit/contracts/bundle.py
src/source_integrity_toolkit/contracts/evidence.py
src/source_integrity_toolkit/validation/structure.py
src/source_integrity_toolkit/validation/references.py
src/source_integrity_toolkit/validation/semantics.py
src/source_integrity_toolkit/runtime/boundary.py
tests/contract/test_bundle_contract.py
tests/contract/test_evidence_basis.py
tests/contract/test_typed_records.py
tests/contract/test_assertion_contract.py
tests/contract/test_temporal_contract.py
tests/unit/test_reference_validation.py
tests/integration/test_prepared_hero_inputs.py
```

### Work and acceptance

Complete the existing contract's shape and globally checkable constraints across the full captured bundle. Validate IDs across all collections, reference multiplicity and kinds, exact Claim bindings, relation direction/type compatibility, required assessment detail and time syntax. Construct bounded immutable sorted indexes and the finite structural scope/anchor plan. Establish acceptance only after all these operations finish.

Keep valid sparse, protected, disputed, denied/inactive, unknown and cyclic evidence as input. Preserve complete source tuples and record-link provenance for later eligible-view construction, without creating that graph now. Do not test temporal causality, grant applicability or origin sufficiency by silently using a broader rule than the input specification permits.

Run all four unchanged H7 inputs through actual preparation. Read logical oracle files only from tests to check preserved inputs/populations, never from product code and never to supply a metric. If actual validation exposes a pre-existing fixture or specification defect, record it and stop the affected acceptance. Do not edit frozen fixtures or tolerate invalid structure just to admit them.

**Checks:** required/nullable/enum branches for all twelve kinds and assertion forms; all 24 predicates and nine assessments; duplicate IDs/dangling IDs versus valid unresolved records; protected equality; malicious unselected records; known/unknown time forms; valid cycles preserved; H7 variant scopes unchanged.

**Stop:** a provenance or correction calculation appears in validation, a well-formed uncertainty is rejected, an invalid endpoint is repaired, a late record is omitted, or an ambiguous boundary-time rule is invented.

## 12. P2-W06: Non-cumulative observability preparation

### Allowed paths

```text
PHASE_2_PROGRESS.md
phase2/module_policy.json
phase2/implementation_evidence.json
phase2/prerequisite_partition.json
src/source_integrity_toolkit/contracts/report.py
src/source_integrity_toolkit/validation/semantics.py
src/source_integrity_toolkit/runtime/boundary.py
tests/contract/test_observability_preparation.py
tests/unit/test_evidence_domain_index.py
tests/integration/test_preparation_capability_boundary.py
```

### Work and acceptance

Implement the domain/family/field prerequisite preparation in section 3.4. `contracts/report.py` owns its immutable structures and declarative bindings. `validation/semantics.py` supplies only input observations. `runtime/boundary.py` orchestrates their finite assembly without defining a competing rule set.

Create one source-bound partition entry for each PC01-PC24, recording complete-check execution status, any actually inspected constituent input and the deferred semantic owner. All fifteen families remain visible; retain explicit subject/scope absence and reasons without inventing all-pairs queries. Preserve the five domain labels without scoring them.

PC01 can be completed after W05. Other whole prerequisites remain pending here. Supplied classifications, native conclusions and reference availability may be indexed as attributed input. An independence declaration, existing correction event or complete-looking provenance field cannot turn a pending qualification into a pass.

**Checks:** exact family/field/PC/domain registry coverage; source selectors preserved; missing evidence separated from unimplemented checks; no max level; correction evidence alongside unresolved origins; denied/inactive/withheld values unchanged; unrelated-scope metadata cannot erase supplied evidence in another scope; no analytical Result or audit envelope emitted.

**Stop:** PC12 or another deferred semantic check is computed, a label becomes a certificate, pending work becomes `unknown` evidence, a report reference is fabricated or a new public state/code is introduced.

## 13. P2-W07: Integration, counterexamples and isolation regression

### Allowed paths

```text
PHASE_2_PROGRESS.md
phase2/implementation_evidence.json
phase2/input_contract_coverage.json
phase2/prerequisite_partition.json
tests/integration/test_preparation_pipeline.py
tests/integration/test_prepared_hero_inputs.py
tests/integration/test_preparation_capability_boundary.py
tests/security/test_preparation_inertness.py
tests/security/test_input_diagnostics.py
tests/security/test_input_resource_limits.py
tests/contract/test_normalization_profile.py
tests/contract/test_phase2_transition.py
```

### Work and acceptance

Exercise the full private pipeline and each implemented requirement through positive, negative, missing-data and boundary cases. Add independent counterexamples and deliberate mutations that expose defaults or mistakes shared by a representation and its validator. Expected outcomes must come from the frozen rule and explicit fixture, not the product's own answer.

Test that successful and unsuccessful preparation preserve the caller input, do not open locators or initialize native/network capabilities, and do not leak private synthetic canaries. Test repeated invocations for no stale snapshot or hidden cache. Preserve the Phase 1 real interception controls, including the accepted platform-specific native canaries.

The H7 acceptance tests establish structural input preparation and population preservation only. The 26/36 and 25/25 numbers remain test-only future analytical expectations. Unknown and multiparent seventh inputs stay distinct without computing their HHI conditions.

The evidence ledger must identify exact test entry points, input/expected-source identities, accepted implementation commit and actual result. Mark shared families partially covered where their remaining file, graph, report or native requirements are unimplemented. No full 228-field closure is possible in this phase.

**Checks:** complete cumulative test collection; no skipped/deselected required cases; integrated rejection versus interruption versus failure/cancellation; no stale state; all frozen fixtures and public refusals; phase guards catch intentionally forbidden analysis/report/native additions.

**Stop:** a test requires an invented semantic assumption, a required test fails, or repair needs code outside this unit. Submit a named repair scope rather than converting the integration-test unit into unrestricted implementation.

## 14. P2-W08: Exact-head matrix, clean installation and evidence audit

### Allowed paths

```text
PHASE_2_PROGRESS.md
phase2/implementation_evidence.json
phase2/ci_review.md
tests/scaffold/test_ci_contract.py
.github/workflows/phase1-ci.yml
README.md
```

### Work and acceptance

Run the cumulative suite on Linux and Windows with Python 3.11 and 3.13 using the inherited pins and tested install process. The workflow path may retain its historical name while its displayed scope and evidence labels identify Phase 2. Any driver refinement must preserve all permission, collection, guard and failure controls established in W01.

Test both actual full-checkout frozen-file guards and the phase-aware package guard before/after execution. Compare tracked bytes, collection IDs, raw result elements and documented per-component evidence. Do not count successful subtest events as extra distinct top-level tests.

Build and inspect the existing source/wheel distributions and install offline into a clean runtime. No new installed module path, runtime dependency, schema loader or package-data selection is introduced. The unchanged packaging rules should retain the accepted 65 ordinary source members and 55 wheel members; any different inventory requires explanation and authorization rather than automatic acceptance. Source file bytes may change only where implemented under this plan. Rebuild from the inspected source archive and compare wheel member content, keeping platform-specific generated files and whole-archive reproducibility claims separate.

Record real commit/run/job/artifact identities and actual interpreters/images. A local network failure does not substitute for hosted evidence. An expired artifact is unavailable evidence, not a green result. Preserve failed runs and repairs. Windows Server component tests do not certify native Windows 11/NTFS behavior.

**Checks:** every required matrix job; actual dependency installation and existing wheel verification; all cumulative collection/results; clean installed public refusal and private component imports; exact package exclusions; no source runtime network or native authority; no product mutation during tests.

**Stop:** a required job is pending/failed, only an older commit is green, collection and results disagree, a package/pin changes outside scope or a broad artifact upload exposes fixture/user content.

## 15. P2-W09: Final component audit and Phase 2 handoff

### Allowed paths

```text
PHASE_2_PROGRESS.md
PHASE_2_COMPLETION.md
phase2/delivery_manifest.json
README.md
```

### Work and acceptance

Audit every accepted work unit and its actual changed-path list against this plan and named repairs. Verify frozen source/approval/completion/catalog/fixture bytes and the remaining inert modules. Establish that only the permitted preparation components acquired behavior and that the input contract was not altered by convenience.

The completion document must separately identify: adopted specification; implemented preparation functions; executed tests; implemented-but-unverified items, if any; pending analytical/public-file/report/native obligations. A required Phase 2 component cannot be pending while Phase 2 is called complete. Future release obligations stay explicit without being counted as current successes.

Record exact accepted commits, real test matrix, package contents, privacy limits, unavailable public audit interfaces and any scope repairs. The delivery manifest pins a named candidate/predecessor and complete file hashes, excluding itself and later completion/progress records where necessary to prevent circular hashing. Explain that boundary. Verify the final documentation successor with its own exact-head CI and record the resulting evidence in the review PR after the commit exists.

**Checks:** complete authorized-path accounting; no missing acceptance; actual frozen-file and live component guards; precise coverage-ledger claims; unchanged oracles and numerical meanings; final-head matrix; retained failures; no release or next-phase work.

**Stop:** a required test or predecessor is missing, completion overstates the implementation, a previously unapproved path changed or an input/specification question remains unresolved.

Submit `PHASE_2_COMPLETION.md` for owner acceptance. Do not merge automatically, generate `PHASE_3_PLAN.md`, activate auditing, publish a wheel or declare v0.1 complete.

## 16. Coverage contract and future duties

| Requirement family | Required Phase 2 evidence | Remaining after this phase |
|---|---|---|
| SIT-TR001, SIT-VG001-VG005 | Actual bounded canonical mapping, record branches, identifiers, references, predicates and assessments | File-open path where required; later interpretation of eligible graph/assessment meaning |
| SIT-TR002, SIT-VG007 | Source-local types, basis/availability and protected distinctions preserved | Recursive/self-certification qualification and complete evidence-result reporting |
| SIT-TR019-SIT-TR020, SIT-VG006/VG009 | Exact time syntax, lifecycle/conflict preservation, immutable input | Relevant graph conflict resolution, grants/effects and complete temporal analysis |
| SIT-TR021-SIT-TR024, SIT-VG010-VG014 | Private input outcomes, PC01, source-bound scope/domain preparation and pending-operation separation | Full report envelope, atomic Results, whole prerequisite evaluation and public capability matrix |
| SIT-TR027-SIT-TR028, SIT-VG016/VG018/VG023 | Exact input values/J measurement, equivalent admitted capture paths and deterministic input indexes | Full file interface, report bytes, final IDs and witness determinism |
| SIT-TR029-SIT-TR031, SIT-VG019-VG023 | Component isolation, safe diagnostics, input quotas, cooperative stopping, cancellation, unchanged input | Native path/ACL/publication, witness/report ceilings and full-runtime security |
| SIT-TR032-SIT-TR034, SIT-VG024-VG026 | Frozen oracle/Trace preservation, real ingress counterexamples, no theory-formula substitution | Computed hero/oracle values and remaining domain/release assertions |
| M001-M015 and 228 SIT-VF obligations | Static definitions and future tests preserved; no false executed-result claim | All actual source-integrity analytical values, qualifications and report tests |

A shared family is not wholly passed when only its Phase 2 subcases ran. Each ledger row must identify its precise implemented clause and remaining duties. PC24 cannot certify a population whose analytical operation never executed. Treat incomplete implementation and incomplete evidence as separate facts.

Existing W11-R01-R10 guide input representation/capture tests; W11-R16-R22 supply relevant failure/accounting constraints, with later analytical portions still pending. W9 cases apply only at the surfaces actually implemented. Case references must come from the approved catalogs rather than a fresh renumbering. No new test count is promised before collection.

## 17. Global stop and repair rules

Stop the affected work for any changed frozen byte, unapproved path or dependency, arbitrary source execution, unbounded pre-validation work, callback/native/network authority, silent type coercion, undocumented new enum/state/field, swallowed conflict, invalid fixture repair, unavailable test evidence, unsafe error disclosure or fabricated successful report.

Classify the problem as specification ambiguity, fixture defect, implementation defect, test-harness defect, environmental failure or security/rights issue. Preserve the failing input and exact evidence using synthetic/public material. Record the owning rule and proposed minimal repair. Do not change a golden answer solely because code disagrees.

A repair outside the active unit's list, including previous-unit product code, requires explicit scoped authorization. A public semantic/security/license/source/interoperability change follows governance classes C1-C6 as applicable. This plan does not authorize changing any frozen file to remove a stop.

No “all tests passed” claim may omit required jobs, required collected identities or failed platform cases. No test is satisfied by a filename, pending status or a pass-through placeholder.

## 18. Phase 2 exit and next authorization

Successful Phase 2 delivery consists of the implemented private preparation components, canonical input structure schema with explicit limitations, source-bound field/PC/test coverage records, phase-aware protections, immutable H7 acceptance evidence, cumulative cross-platform CI, clean-install evidence and a reviewed `PHASE_2_COMPLETION.md`.

The resulting engineering capability is precise: bounded supplied bytes or built-in values can be represented, structurally validated, indexed and prepared for later scoped analysis while retaining uncertainty and attribution. A caller still cannot obtain a real source-integrity audit from the public API/CLI. No root count, independence result, HHI, correction finding, report pair or native-security support claim is delivered by this phase.

The immediate next gate is owner approval of this exact plan and authorization of **P2-W01**. Stop after submitting the plan. Preparing it does not begin W01.

## 19. External format reference and review limits

**EXT01:** JSON Schema Draft 2020-12, Core and Validation specifications. Official references consulted during this planning task:

- `https://json-schema.org/draft/2020-12/json-schema-core`
- `https://json-schema.org/draft/2020-12/json-schema-validation`

The narrow external basis is the schema dialect, local-reference organization, mathematical integer semantics and the distinction between format annotation and assertion. The choice to use a structural schema beside the mandatory project-owned parser/global validator is this plan's engineering proposal. These references add no theory-map entry, dependency, source retrieval permission or claim that a schema has already been implemented or independently validated.

All other controlling product meanings come from the adopted repository. This planning review is a source/architecture/scope review, not execution of Phase 2 tests, independent scientific validation, native conformance or legal clearance. Exact new file bytes, planning commit and review URL are recorded after submission; none is guessed here.
