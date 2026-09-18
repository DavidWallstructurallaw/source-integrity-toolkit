# PHASE_1_PLAN

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Phase | Phase 1: Repository Scaffold |
| Target product release | v0.1 |
| Plan revision | 0.1 |
| Date | 2026-09-17 |
| Status | PROPOSED FOR APPROVAL |
| Theory Owner | Xiangyu Guo |
| Technical Owner | Unassigned |
| Repository | `DavidWallstructurallaw/source-integrity-toolkit` |
| Approved Phase 0 snapshot | `7d2e5fcaff591641b5cefce00e71e88941dd1f95` |
| Approval authority | `PHASE_0_APPROVAL.md`, recording `批准，进入phase 1` |
| Approval-record commit | `6650984502637bb167c38e7e370c46e246591480` |
| Current authorization | Prepare and submit this plan |
| Execution authorization | Pending approval of this exact plan |
| Planned work units | P1-W01 through P1-W07, executed in order |
| Analytical implementation | Prohibited throughout Phase 1 |

## 1. Purpose and controlling inputs

Phase 1 establishes an installable, inspectable and testable repository scaffold for the approved local auditor. Its public audit functions remain explicitly unimplemented. A successful scaffold demonstrates packaging, boundaries, trace preservation and fixture preparation; it does not demonstrate source-integrity analysis.

The controlling baseline is the eighteen-file manifest in `PHASE_0_APPROVAL.md`. In particular:

| Authority | Phase 1 use |
|---|---|
| `PHASE_0_PLAN.md` section 23 | Allowed scaffold and forbidden analytical behavior |
| `PROJECT_INSTRUCTIONS.md` | Work-unit permissions, change discipline and approval separation |
| `V0.1_PRODUCT_SPEC.md` | Sixteen requirements and bounded first-release purpose |
| `DEFINITIONS_AND_UNITS.md`; `CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` | Object, relationship, unit and supplied-evidence meanings |
| `OBSERVABILITY_AND_REPORTING.md` | Fifteen analytical families, fifty-seven leaves and report-state contract |
| `VALIDATION_PLAN.md`; `SUCCESS_CRITERIA.md` | Logical cases, pending executable obligations and acceptance limits |
| `THEORY_TO_CODE_TRACEABILITY.md` | Thirty-five Trace responsibilities and nineteen logical owners |
| `PRIVACY_AND_DATA_HANDLING.md`; threat model | Inert input, protected sources and bounded authority |
| `LICENSING_NOTES.md` | Uniform Apache-2.0 engineering policy with exclusions |
| `REPOSITORY_ARCHITECTURE.md` sections 3-6 and 16-22 | Concrete module ownership and completed SIT-RP-0.1 realization |
| `DEPENDENCY_STRATEGY.md` | Zero third-party Python runtime packages; reviewed build/test tools |
| `GOVERNANCE_AND_HANDOFF.md`, especially section 22 | Final precision resolutions and phase transitions |
| `UNRESOLVED_DECISIONS.md` | Current decisions and pinned historical decision records |

The source audit and theory map remain authoritative provenance records. This phase does not reopen their research, update paper versions or copy the theory PDFs into the repository.

Where a detail is explicitly assigned to a later implementation phase, a placeholder and a pending obligation preserve it. Where a new conflict would change a public meaning, stop and submit a scoped amendment instead of completing it by convenience.

## 2. Scope and non-goals

### 2.1 Permitted work after plan approval

Create repository governance and Apache-2.0 notices; packaging metadata; import-safe module slots; explicit public-operation stubs; schema reservation documents; static trace and obligation catalogs; static fictional hero fixtures and logical expectations; scaffold-only tests; developer verification scripts; and minimally privileged CI.

Build and install the scaffold in a controlled development environment. Run only tests whose behavior is permitted by this plan. Developer tests may inspect repository files, parse static fixture JSON and verify finite identifier references. Those checks must stay outside the installed auditor and cannot become an undeclared production ingestion path.

### 2.2 Prohibited work

Do not implement the runtime parser, capture/normalization protocol, schema mapper, semantic validator, observability classifier, typed graph construction/traversal/cycle detection, origin qualification, independence comparison, HHI, evaluator overlap, external-presence analysis, correction analysis, threat classification or analytical report rendering.

Do not implement native file-opening, ACL, ctypes, no-clobber publication, quota accounting or the SIT-RP-0.1 serializer. Their module slots and future tests can exist; their behavior remains absent.

No crawler, URL opener, network-enabled audit mode, LLM, embedding dependency, plugin execution, automatic source sanction, shared toolkit core, database, dashboard or universal score is admitted. No package-index publication, GitHub release, deployment, signing key, repository-secret change or branch-protection change is authorized.

A fake successful report, empty valid-looking analytical result or constant hero answer is not an acceptable stub.

## 3. Execution and repository controls

The eighteen baseline files and `PHASE_0_APPROVAL.md` stay byte-identical and at their current root paths. Historical pending headers are interpreted through the approval record, not rewritten. `PHASE_1_PLAN.md` becomes read-only when approved; amendments require a new scoped owner decision and revision.

Specification planning commits may use the currently authorized `main` workflow. Scaffold execution should use one review branch per work unit, based on the latest accepted predecessor. Review the diff and available checks before merge. Do not force-push or rewrite history. A failed write or unreadable remote file is not a completed delivery.

Each work unit stops after its own review package. Owner continuation authorizes the next named unit and accepts the preceding submitted result in context. Plan approval alone does not authorize silently executing all seven units or entering Phase 2.

`PHASE_1_PROGRESS.md` is the only common writable file in every execution unit. Record its actual intake commit, approved scope, files changed, tests run, environment, failures, remote commit/PR references and next gate. A commit hash is recorded after it exists, without trying to embed a document's own final hash in itself.

Lists below are closed allowlists. Prefix notation expands to the explicitly enumerated paths only. A directory name does not authorize arbitrary descendants. Returning to an earlier file outside the current unit's list requires a scoped repair authorization.

## 4. Scaffold behavior contract

### 4.1 Package and operations

Use the distribution name `source-integrity-toolkit` and import name `source_integrity_toolkit`, with a `src` layout. The proposed scaffold version is `0.1.0.dev0`, explicitly unreleased and analytically nonfunctional.

`audit_bundle(bundle, *, options=None)` and `audit_file(input_path, output_directory, *, options=None)` exist only as stable-name placeholders. Their bodies immediately raise `NotImplementedError` with fixed tool-authored text. They must not inspect, stringify, iterate, validate, copy or otherwise act on arguments before raising. They produce no dossier/report value and no file.

The CLI may expose help and the scaffold version. An audit invocation returns a fixed non-operational message and process exit 1 without touching input/output paths. Exit 1 is a temporary scaffold refusal, not a `sit-report/0.1` outcome. Document it explicitly and do not use real result-state or reason codes to pretend an audit ran. The final invocation and cancellation semantics remain those adopted in Phase 0.

Package import performs no application-originated evidence/configuration reads, network access, native binding, writes or telemetry. Ordinary Python module loading and controlled test-harness operations are distinct from prohibited application side effects.

### 4.2 Module bodies and schemas

Internal slots contain docstrings identifying their owner, specification section and pending behavior. Literal constants and explicit type/signature reservations may be copied from approved contracts, without validation or interpretation. Placeholder callables fail immediately. Do not install another validation framework or treat a dataclass constructor as completed admission.

Schema slots in this phase are Markdown reservation documents. No permissive empty schema or machine-readable schema that appears complete is published. Executable schema design remains a later approved task.

### 4.3 Evidence-status separation

Keep three statuses separate in catalogs and completion reports: specification adopted, scaffold slot present, and behavior implemented/tested. The last remains pending for all analytical and native-runtime obligations.

Passing fixture JSON syntax, import safety or a hash check does not satisfy the corresponding domain-analysis obligation. Do not bulk-mark the 228 field obligations as passing, create hundreds of empty passing tests, or hide them behind a blanket skip/xfail count.

## 5. P1-W01: Freeze verification, project governance and license application

### Objective

Establish the repository's public identity and apply the already approved engineering license without changing any frozen specification.

### Allowed paths

```text
README.md
LICENSE
NOTICE
CONTRIBUTING.md
SECURITY.md
.gitignore
.gitattributes
PHASE_1_PROGRESS.md
scaffold/baseline_manifest.json
scaffold/toolchain_review.md
```

### Work and acceptance

Verify all eighteen approval-manifest hashes and record the approval file's separately computed hash in `scaffold/baseline_manifest.json`. The machine-readable copy records path, byte count and SHA-256; it cannot weaken the authoritative approval. Keep the exact approved commit and the approval-record commit distinct.

Create standard Apache-2.0 license text from the official source at execution time. Keep applicable project attribution in NOTICE. README and CONTRIBUTING clearly exclude theory papers, third-party material and user evidence from automatic relicensing; they do not add new downstream conditions to Apache-2.0.

README states Phase 1 scaffold status, the local supplied-dossier purpose, no implemented audit functionality, and the roadmap boundary. SECURITY states the present support limit and a reporting route actually available to the maintainer; do not invent an email address or claim private vulnerability reporting is enabled without verification. If no private route is verified, disclose that limitation and prohibit posting secrets rather than fabricating one.

Use `.gitattributes` to protect exact baseline/approval bytes from checkout normalization, with explicit protected-path entries. New scaffold text uses UTF-8/LF. Ignore local environments, build artifacts, caches and private runtime data without ignoring required tests or specifications.

Review actual compatible setuptools and pytest versions and their dependency/license implications in `scaffold/toolchain_review.md`. Record sources, exact proposed pins, interpreter compatibility and runtime/development separation. No unreviewed optional tool is introduced. Package declarations and installations belong to W02.

**Tests/checks:** exact-byte manifest comparison; public-license source comparison; exclusion consistency; absence of private material and implementation; explicit path allowlist.

**Stop:** any missing or changed baseline byte, uncertain asset permission, invented security contact capability, or proposed runtime dependency. Do not repair a frozen file silently.

## 6. P1-W02: Packaging and import-safe architecture slots

### Allowed non-package paths

```text
pyproject.toml
MANIFEST.in
requirements-dev.txt
scaffold/toolchain_review.md
tests/scaffold/test_imports.py
tests/scaffold/test_api_stubs.py
tests/scaffold/test_cli_scaffold.py
tests/scaffold/test_packaging.py
PHASE_1_PROGRESS.md
```

### Exact package paths

All paths in the following table are relative to `src/source_integrity_toolkit/`. Include each listed package initializer and file; no other package file is authorized.

| Directory | Files |
|---|---|
| Root | `__init__.py`, `api.py`, `cli.py` |
| `contracts/` | `__init__.py`, `bundle.py`, `evidence.py`, `results.py`, `report.py`, `constants.py`, `execution.py` |
| `io/` | `__init__.py`, `input_file.py`, `output_directory.py`, `publication.py`, `platform_linux.py`, `platform_windows.py` |
| `validation/` | `__init__.py`, `structure.py`, `references.py`, `semantics.py`, `limits.py` |
| `graph/` | `__init__.py`, `projections.py`, `traversal.py`, `cycles.py`, `witnesses.py` |
| `analysis/` | `__init__.py`, `inventory.py`, `origins.py`, `process_comparison.py`, `contribution_profile.py`, `evaluator_lineage.py`, `presence.py`, `correction_routes.py`, `correction_outcomes.py`, `human_review.py`, `context.py`, `findings.py` |
| `reporting/` | `__init__.py`, `assemble.py`, `json_report.py`, `markdown_report.py`, `escaping.py` |
| `runtime/` | `__init__.py`, `boundary.py`, `resources.py`, `disclosure.py`, `diagnostics.py` |

### Work and acceptance

Declare Python's approved lower bound, no third-party runtime requirements, reviewed setuptools build configuration and the `sit` entry point. Keep reviewed pytest/developer pins outside runtime dependencies. Resolve and record the actual development environment, including necessary transitive/version differences, without presenting an untested future Python version as supported.

Create only the bodies permitted by section 4. Preserve the nineteen logical-owner bindings and WU11's execution/platform additions. Do not load ctypes or select native symbols in the platform slots.

Build a source distribution and wheel in a controlled workspace, inspect their contents and install the wheel for smoke tests. Explicit packaging selection includes intended original engineering artifacts and notices; it excludes PDFs, private evidence, identity maps, generated reports, caches and unrelated local files. No package is uploaded anywhere. Any additional build frontend needed beyond the reviewed backend and existing development environment requires an explicit toolchain review and scoped plan amendment before use.

**Tests/checks:** imports of every slot; immediate API refusal with hostile argument objects; CLI help/version and audit refusal; no report/output creation; package identity/version/dependencies; source and wheel inventory.

**Stop:** an operation reads a dossier, emits analytics, activates native bindings, introduces a disallowed dependency, or changes frozen bytes. Passing imports cannot close any analytical Trace.

## 7. P1-W03: Static contract, trace and schema reservations

### Allowed paths

```text
schemas/README.md
schemas/bundle/README.md
schemas/report/README.md
scaffold/module_manifest.json
scaffold/trace_catalog.json
scaffold/obligation_catalog.json
tests/scaffold/test_contract_catalogs.py
tests/scaffold/test_module_manifest.py
PHASE_1_PROGRESS.md
```

### Work and acceptance

Document that `sit-bundle/0.1` and `sit-report/0.1` are adopted logical contracts whose executable schemas are not delivered in this phase.

Create a finite module manifest for the exact W02 paths, their permitted layer dependencies, owner labels and placeholder status. The manifest is a scaffold verification artifact, not a runtime plugin registry.

Transcribe the 35 Trace IDs, 19 owners, 15 analytical families and 57 output fields from their authoritative tables. Preserve exact source-section and future-test mappings, including the 228 P/N/M/B field obligations and 26 shared families. Include the existing W9 and W11 control/case references in the obligation catalog, with pending implementation status.

Do not turn prose-level evidence rules into executable qualification logic. Catalog checks compare membership, uniqueness and references; they do not compute a source graph. The 24 prerequisite codes, 40 reasons and 22 finding conditions must stay aligned with their original catalogs when referenced.

**Tests/checks:** exact set equality against authoritative registries; unique IDs; each field has one primary Trace and four field-test IDs; every owner has a module home; no machine schema or implemented behavior is falsely advertised.

**Stop:** an unknown field/owner/code appears, a catalog loses a qualification, a historical superseded name is treated as current, or a placeholder is labeled operational.

## 8. P1-W04: Static hero fixtures and logical expectations

### Allowed paths

```text
tests/fixtures/README.md
tests/fixtures/hero/H7-01.bundle.json
tests/fixtures/hero/H7-V01.bundle.json
tests/fixtures/hero/H7-V02.bundle.json
tests/fixtures/hero/H7-V03.bundle.json
tests/fixtures/hero/fixture_manifest.json
tests/fixtures/micro/case_index.json
tests/fixtures/adversarial/case_index.json
tests/golden/README.md
tests/golden/H7-01.logical.json
tests/golden/H7-V01.logical.json
tests/golden/H7-V02.logical.json
tests/golden/H7-V03.logical.json
tests/scaffold/test_fixture_integrity.py
PHASE_1_PROGRESS.md
```

### Work and acceptance

Transcribe the approved H7 main dossier and three controlled variants from the lineage and validation specifications. These are fictional static input artifacts. Keep source IDs, claims, roles, assertions, support, coverage, native outcomes and variant boundaries intact. Mechanical envelope completion must follow the approved contract; it cannot invent new substantive evidence to make an expected conclusion work.

Logical expectation files are explicitly labeled as test-only oracle records, not executable toolkit reports or a new public output schema. Preserve exact selected populations, qualifications, non-result reasons and conditional fractions. They must never be imported by the production package to answer an audit.

H7-01 retains six source contributions, its five-to-one origin grouping and conditional 26/36 HHI. H7-V01 retains its selected one-origin population and 25/25. The unknown seventh contribution and known unallocated multiparent seventh contribution both withhold full-population HHI while retaining their different explanations. Pipeline cohorts and correction targets are not silently resized. Submission, handling and the three documented linked changes remain distinct.

Create indexes for W7-01-W7-28 and the W9/W11 adverse/control cases, preserving their specification locations and future status. This unit does not require building a complete executable fixture for every future runtime obligation.

**Tests/checks:** fixture JSON syntax; finite ID uniqueness; listed references; variant delta membership; static expected-value correspondence; SHA-256 of fixture files; separation of inputs from logical expectations. Test-only checks must not grow into ancestry, independence or correction algorithms.

**Stop:** a case requires a new semantic assumption, an incomplete record is disguised as an unresolved reference, a fraction loses its denominator meaning, or a runtime call returns a stored expected answer. Resolve the source-specification question before promoting that fixture.

## 9. P1-W05: Scaffold boundary and baseline guards

### Allowed paths

```text
tools/check_phase0_baseline.py
tools/check_scaffold_boundary.py
tests/scaffold/test_baseline_integrity.py
tests/scaffold/test_no_runtime_implementation.py
tests/scaffold/test_layer_boundaries.py
tests/security/test_scaffold_inertness.py
tests/security/test_scaffold_no_native_loading.py
tests/security/test_scaffold_no_network.py
tests/integration/README.md
tests/unit/README.md
tests/contract/README.md
PHASE_1_PROGRESS.md
```

### Work and acceptance

Implement developer-only checks for the exact frozen manifest, package path inventory, permitted import layers and placeholder AST/body forms. These tools inspect repository/build artifacts; they are not installed public audit functions.

Boundary checks must reject unexpected runtime functions, data-dependent algorithms, source I/O, native loaders, network clients, mutable registries and imports from the other toolkit. Static and dynamic scaffold tests complement one another. No claim of a complete security proof follows.

Use independently constructed synthetic canaries and controlled temporary directories. API stub tests verify that argument methods are not invoked and no input/output files are touched. Distinguish Python's module loader from application-originated source access. Scope network/native interception to the tested application boundary so ordinary pytest infrastructure is not mistaken for runtime behavior.

Include deliberate temporary mutations of the scaffold under test: altered baseline bytes, a forbidden import, a non-placeholder function body, an extra module and a stub that inspects an argument. Each guard must detect its own adverse case. Do not commit those mutated artifacts into the real package.

**Tests/checks:** positive scaffold acceptance and negative guard controls; layer rules; no input traversal, native binding or application network access; original eighteen hashes and approval hash remain exact.

**Stop:** the guard passes its deliberate violation, tests merely inspect implementation-produced metadata without an independent comparison, or a new helper performs prohibited analytical work.

## 10. P1-W06: Minimal CI and clean-install verification

### Allowed paths

```text
.github/workflows/phase1-ci.yml
scaffold/ci_toolchain_review.md
tests/scaffold/test_ci_contract.py
README.md
PHASE_1_PROGRESS.md
```

### Work and acceptance

Create CI for the scaffold checks, test collection, source/wheel inspection and clean-install smoke tests. Use one reviewed Linux hosted-runner profile and one reviewed Windows hosted-runner profile, with Python 3.11 and one additional currently supported compatible minor selected and recorded at execution time.

Verify actual action revisions, runner labels and Python/build/test compatibility before committing the workflow. Pin external actions to reviewed full commit SHAs, record their source/version and use the already reviewed developer requirements. Selection inside these constraints is a toolchain realization; an added tool or altered runtime requirement needs an explicit plan amendment.

Use minimum permissions, normally `contents: read`; do not grant write tokens, use `pull_request_target`, expose secrets, execute PR-supplied text as shell syntax, or publish a release. Separate dependency-install/build network access from tests of the local auditor's no-network behavior. Set finite job timeouts. Upload only non-sensitive scaffold test/build evidence required for review, never user dossiers.

Run the workflow on review pull requests and accepted branch updates. Record the real workflow run URL, checked commit, matrix and result. A pending job remains pending. A Windows hosted runner verifies only the scaffold/import/package behavior actually exercised; it does not certify the Windows 11 NTFS native profile.

**Tests/checks:** workflow permission/trigger/action-pin inspection; full actual matrix results; clean install without pytest in the installed runtime dependency set; exact baseline guard; no native or analytical work enabled by CI.

**Stop:** missing/failed required jobs, unresolved pins, broader permissions, package publication, secret exposure or a claim of full platform support based on imports.

## 11. P1-W07: Final scaffold audit and handoff

### Allowed paths

```text
PHASE_1_COMPLETION.md
PHASE_1_PROGRESS.md
scaffold/delivery_manifest.json
README.md
```

### Work and acceptance

Audit the accepted scaffold tree against the closed file lists and frozen Phase 0 baseline. Record each completed step's accepted commit, actual tests, environment, build contents and hosted CI evidence. Re-run relevant checks on the final candidate; do not attach an earlier green run to changed executable content.

The delivery manifest identifies files and hashes at an explicitly named predecessor/candidate snapshot. It excludes itself and completion/progress files whose later evidence record would otherwise create a circular hash. The final handoff gives the actual resulting commit and explains that manifest boundary.

Completion records scaffold functionality only. List the public audit functions as unimplemented, the domain/schema/native tests as pending, and all analytical obligations as awaiting their appropriate implementation phase. No passing scaffold total is presented as passing the 228 domain assertions.

Document any remaining release evidence, including exact native conformance, runtime parser/serializer behavior, analytical tests, performance, platform coverage and distribution rights review. Such future implementation duties do not become claimed Phase 1 successes.

**Tests/checks:** complete allowlist diff; baseline and approval unchanged; all required scaffold tests and CI evidenced; hero fixture/expectation integrity; package exclusions; no runtime dependencies or forbidden behavior; no unapproved file or automatic Phase 2 work.

**Stop:** any earlier step lacks acceptance, a required test remains failed/pending, or the completion language overstates the scaffold. Repair outside this unit's allowlist needs a named scoped authorization. Stop after submitting `PHASE_1_COMPLETION.md` for owner review; do not generate Phase 2 code or a new phase plan automatically.

## 12. Phase-level test and evidence rules

| Test layer | May pass in Phase 1 | Remains unproved |
|---|---|---|
| Baseline and catalogs | Byte identity, complete mappings, unique IDs | Truth of supplied evidence or scientific theory |
| Packaging/imports | Installability and inert module slots | Useful auditing or supported native filesystem behavior |
| Static fixtures | Syntax, declared references and approved case transcription | Runtime ingestion, graph qualification or computed hero reports |
| Scaffold security guards | Tested absence of prohibited side effects/behavior | Full production security, safe native publication or resource enforcement |
| CI | Actual executed matrix at a named commit | Untested interpreters, operating systems, future releases or domain obligations |

Keep raw failure evidence in the work-unit record. Do not change approved expectations to match incorrect code. Distinguish a tool outage, environment incompatibility, fixture defect, specification conflict and implementation defect before deciding the next action.

Scope tests to fictional repository material. Never ask for real private dossiers just to prove a scaffold works. No hidden identity map or theory PDF becomes test data.

## 13. Global stop rules and repair procedure

Stop the affected work when the baseline hash differs; a new file is outside its unit; a semantic or security rule conflicts; a fixture requires unsupported evidence; a build adds runtime dependencies; a stub performs analysis; native/network authority appears; report states are fabricated; CI fails or lacks evidence; licensing excludes material the build nevertheless packages; or cross-project internals are imported.

Record the exact path, observed fact, affected authority and narrow proposed repair in `PHASE_1_PROGRESS.md`. Leave unrelated approved artifacts intact. Do not respond to a stop by weakening the guard, silently editing Phase 0, inventing approval, or moving the same implementation into tests and calling it a placeholder.

Mechanical repair within the current allowed files and approved meaning may occur before resubmission. A change to a frozen contract, another unit's files, release scope or security/dependency policy needs explicit scoped approval.

## 14. Final deliverables and exit criteria

The Phase 1 handoff contains an Apache-2.0-governed original engineering scaffold, reviewed package/dev metadata, the complete named module slots, schema reservation documents, static catalogs, the H7 fixtures and logical expectations, real scaffold tests, developer guards, reviewed CI, progress evidence and `PHASE_1_COMPLETION.md`.

Phase 1 passes only when every executed work unit meets its own acceptance criteria, the final required checks have actual evidence, the frozen baseline remains unchanged and no prohibited analytical/native behavior exists. Owner approval of that completion is a separate event.

No ZIP history, source PDFs, full theory extracts, user data, executable analytics or release publication belongs to this phase. The repository remains separate from Recursive Integrity Toolkit.

## 15. Current handoff and first execution gate

This plan is submitted alongside the now-issued Phase 0 approval record. Preparing these two documents does not execute P1-W01.

The next instruction may approve this exact plan and authorize **P1-W01: Freeze verification, project governance and license application**. After that unit is delivered and accepted, proceed sequentially. Phase 2 remains outside this plan.
