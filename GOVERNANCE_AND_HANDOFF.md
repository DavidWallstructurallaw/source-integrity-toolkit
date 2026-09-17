# GOVERNANCE_AND_HANDOFF

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Target release | v0.1 |
| Phase / work unit | Phase 0 / Work Unit 10 |
| Revision | 0.1 |
| Date | 2026-09-17 |
| Status | PROPOSED FOR REVIEW; governance and handoff only |
| Theory Owner | Xiangyu Guo |
| Technical Owner | Unassigned |
| Repository | `DavidWallstructurallaw/source-integrity-toolkit` |
| Prior accepted WU9 policy | WU9-C01 and WU9-C02 accepted by the instruction to proceed to WU10; WU9-C03 approved as Apache-2.0 |
| Companion outputs | `REPOSITORY_ARCHITECTURE.md`, `DEPENDENCY_STRATEGY.md` |
| Next planned unit | Work Unit 11 final Phase 0 audit |
| Full Phase 0 approval | Not issued |
| Implementation / Phase 1 authorization | Not issued |

## 1. Purpose

This document defines how the Source Integrity Toolkit specification moves from the current Phase 0 baseline into final audit, later scaffold work and future releases without losing the distinctions established in the theory, product, lineage, observability, security and validation contracts.

It also records the current contextual acceptance of Work Unit 9. The preceding handoff explicitly stated that WU9-C01 and WU9-C02 required confirmation before entering Work Unit 10. The owner replied `可以，继续 Work Unit 10`. That instruction is recorded as acceptance of those two proposals in their stated scope. WU9-C03 had already been explicitly resolved to Apache-2.0.

This record does not alter historical Work Unit 9 files. The final Work Unit 11 audit may consolidate status and decision history in the documents permitted by its allowlist.

## 2. Governance roles

### 2.1 Theory Owner

The Theory Owner has authority to:

- approve or reject Phase 0 product operationalizations;
- decide how ambiguous source theory is represented in the product;
- approve changes to product scope, public analytical semantics and theory attribution;
- approve phase completion and progression;
- decide whether a counterexample requires reopening the product specification.

The Theory Owner does not by that role become the technical author of every code contribution or third-party asset.

### 2.2 Technical Owner

The Technical Owner, once assigned, owns implementation consistency with the approved contracts. Responsibilities include:

- module boundaries and implementation quality;
- dependency and platform conformance;
- resource/failure behavior;
- CI and executable tests;
- release artifact integrity;
- architecture-compliance checks.

The Technical Owner cannot change theory meaning or public analytical semantics solely through code review.

### 2.3 Maintainers and reviewers

Later maintainers may approve ordinary code changes inside an already approved contract. Changes that alter public fields, qualification rules, resource/security guarantees, license scope, or cross-project semantics require the appropriate higher-level review described below.

No current document appoints a specific maintainer or claims an independent security review.

## 3. Change classes

| Class | Examples | Required treatment |
|---|---|---|
| C0: implementation-preserving | refactor, internal performance work, test cleanup | Technical review plus regression suite; no spec change if behavior is unchanged |
| C1: contract clarification | wording that removes ambiguity without changing outcomes | Update owning spec and traceability; Theory Owner review when public interpretation is affected |
| C2: public behavioral change | new field, changed denominator, new relation meaning, different non-result behavior | Reopen product/report/validation contracts; Theory Owner approval; new/updated Trace and tests |
| C3: boundary/security change | network mode, changed resource ceiling, weaker output protections, new plugin mechanism | Security/privacy and architecture review; explicit owner approval; expanded adversarial tests |
| C4: theory mapping change | new paper version, changed source interpretation, theory conflict | Reopen source map/audit and affected product decisions before implementation |
| C5: licensing/distribution change | different project license, bundled theory paper, new third-party asset class | Rights review and explicit license/governance approval |
| C6: cross-project semantic coupling | direct import from another toolkit, shared core, schema compatibility promise | Separate interoperability proposal and approval; cannot be hidden in implementation |

A change is classified by its strongest effect. Labeling a change “refactor” does not make a semantic change C0.

## 4. Specification authority and conflict handling

The approved plan and explicit owner decisions remain controlling. Within their scopes, later approved detailed specifications supersede earlier proposals but do not rewrite historical records.

Implementation resolves no specification conflict by choosing whichever text is easiest to code.

When two current specifications appear incompatible:

1. identify the exact fields/rules and owning documents;
2. stop affected implementation or audit conclusion;
3. preserve existing behavior only if it is already approved and unambiguous;
4. open a scoped decision for the owner;
5. update traceability and tests after resolution.

No CI green status can overrule a documented contract conflict.

## 5. Traceability governance

`THEORY_TO_CODE_TRACEABILITY.md` retains SIT-TR001 through SIT-TR035 as stable responsibility IDs.

`REPOSITORY_ARCHITECTURE.md` supplies the concrete module/test mapping for the logical owners already named there. The composite binding is:

```text
SIT-TR → logical owner → concrete module/test owner
```

The original trace file need not duplicate every path to make the binding effective, provided both documents are included in the approved baseline and the Work Unit 11 audit verifies that every logical owner resolves exactly once.

A future code path can move without changing a Trace ID when the semantic owner remains the same. A change in semantic ownership requires an architecture/traceability update.

All 57 analytical output leaves retain their Work Unit 8 positive, negative, missing-data and boundary obligations. Architecture does not replace those tests with generic unit coverage.

## 6. Test and validation governance

The hierarchy of executable evidence in later phases is:

1. structural schema/contract tests;
2. field-level SIT-VF obligations;
3. shared SIT-VG contract/integration tests;
4. canonical hero/golden cases;
5. privacy/security/resource adversarial cases from Work Unit 9;
6. trace-closure and architecture-compliance checks;
7. release packaging and no-network checks.

A test may expose a code bug, a specification ambiguity, bad fixture evidence or a product-model failure. `VALIDATION_PLAN.md` already requires distinguishing those cases. Never change a golden expected result only to make a failing implementation pass.

A report that is numerically correct but loses scope, denominator, witness or uncertainty fails the contract.

## 7. Security and privacy governance

The accepted Work Unit 9 controls are now architectural requirements for later implementation.

The v0.1 reference implementation remains local, no-network, no-telemetry and non-intervening. Protected-source handling, report minimization, safe rendering, private output publication and resource ceilings cannot be weakened by a convenience option without a C3 change.

Resource ceilings WU9-L01 through WU9-L14 are release contract values until an approved successor changes them. Source data cannot override them.

A platform is supported only after its filesystem/ACL behavior satisfies the approved disclosure contract in tests. “Works on my machine” is insufficient for a privacy-support claim.

## 8. Licensing governance

WU9-C03 selects Apache-2.0 for original engineering repository materials.

The later scaffold should create the standard Apache-2.0 license artifacts and clear exclusion language for theory papers, third-party assets and user evidence. No current Phase 0 document applies Apache-2.0 to material whose rights are not controlled by the project.

Dependencies retain their own licenses. Release review must inspect actual included versions and artifacts.

Changing the project license or adding source-paper expression to ordinary distributions is a C5 change.

## 9. Versioning policy

### 9.1 Contract versions

Bundle/report contract versions change when a consumer must interpret data differently.

Backward-compatible additions require explicit extension rules and cannot be smuggled into closed core fields. A breaking semantic change requires a new contract version and migration guidance.

Historical snapshots keep their original declared version. A reader must not reinterpret an old snapshot as a new schema without an explicit, provenance-recorded conversion.

### 9.2 Package versions

Package semantic versioning should reflect public API and contract behavior once the first implementation release exists.

Internal refactors can be patch releases when public behavior is unchanged. New backward-compatible public capabilities can be minor releases. Breaking public API or contract behavior requires a major-version decision or a documented pre-1.0 compatibility policy before release.

No package version is assigned by Phase 0.

## 10. Repository and branch governance

The current Phase 0 work is committed directly to `main` under explicit owner instructions. Later implementation should use reviewed branches or pull requests for nontrivial code changes once CI exists.

Phase 1 should define required checks before merges, including at minimum contract/static checks appropriate to its scaffold. Later analytical phases add the relevant executable test suites before enabling corresponding behavior.

Generated artifacts, user dossiers and private test evidence must not be committed to the public repository.

The public repository should contain synthetic fixtures only unless a separately reviewed asset is explicitly authorized.

## 11. Cross-project handoff and interoperability

Source Integrity Toolkit and Recursive Integrity Toolkit remain peer projects.

No direct import, submodule, vendored internal package or shared database is permitted in v0.1. A future integration must operate through versioned public artifacts and an explicit adapter.

The adapter must preserve:

- source/target contract versions;
- inquiry and claim scope;
- record/relationship type;
- assertion provenance;
- unknown and disputed state;
- population/denominator meaning;
- protected-source disclosure boundaries.

If the receiving product lacks an equivalent semantic state, the adapter must reject or explicitly downgrade the mapping. It cannot silently coerce unknown ancestry into an independent root or convert a qualified process assessment into a global property.

Interchange success does not certify either product's result.

## 12. Phase 0 to Phase 1 handoff

Work Unit 10 does not authorize Phase 1. After this unit is accepted, Work Unit 11 performs the complete Phase 0 audit.

The Work Unit 11 audit should verify at least:

- no BLOCKING in-scope decision remains;
- all required Phase 0 documents exist;
- terms, object names, analytical fields and result states are consistent;
- WU9-C01 through WU9-C03 acceptance is reflected without rewriting historical bytes;
- every SIT-TR logical owner maps to a concrete architecture owner;
- every public analytical field retains future tests;
- dependency strategy introduces no hidden runtime capability;
- Apache-2.0 policy and theory/user exclusions are consistent;
- cross-project separation is maintained;
- no implementation code, executable schema or Phase 1 behavior has entered Phase 0.

Only after an explicit owner approval of the audited Phase 0 bundle should `PHASE_0_APPROVAL.md` be created.

A later `PHASE_1_PLAN.md` must then enumerate exact scaffold files it may create or modify. Phase 1 cannot rely on this handoff as blanket coding authority.

## 13. Phase 1 architecture handoff payload

Subject to Work Unit 11 approval, Phase 1 planning receives:

- the complete approved Phase 0 Markdown baseline;
- the module layout in `REPOSITORY_ARCHITECTURE.md`;
- the standard-library-only runtime strategy in `DEPENDENCY_STRATEGY.md`;
- the Apache-2.0 repository policy in `LICENSING_NOTES.md`;
- the fixed WU9 privacy/resource controls;
- the existing SIT-TR/SIT-VF/SIT-VG trace and test obligations;
- the canonical hero/micro-case expected behavior;
- the explicit list of Phase 1 analytical prohibitions.

The scaffold should make later implementation slots obvious without pretending those slots already satisfy their Trace obligations.

## 14. Release stop rules

Stop a release or phase transition when any of the following is true:

- a public result has no trace/test owner;
- a dependency introduces undeclared network/model/plugin behavior;
- a protected-source report path has not passed required platform tests;
- a resource failure can appear as a successful negative result;
- JSON and Markdown disagree substantively;
- theory PDFs or third-party data have been swept into Apache-2.0 scope without rights review;
- a cross-project adapter loses uncertainty or provenance;
- a golden oracle was changed without a corresponding approved contract decision;
- a required phase gate has been replaced by “the code works.”

## 15. Work Unit 10 review package

Work Unit 10 has three review items:

- **WU10-C01:** concrete repository/module/public-interface architecture;
- **WU10-C02:** standard-library-only runtime and minimal build/test dependency strategy;
- **WU10-C03:** governance, change classification, traceability binding, cross-project interchange boundary and Phase 0 → Phase 1 handoff.

The recommended action is to approve all three together if no amendment is required, then proceed to Work Unit 11 final Phase 0 audit.

No Phase 1 implementation, licensing file, schema, fixture or CI workflow is created by this Work Unit 10 package.
