# GOVERNANCE_AND_HANDOFF

> Current audit supplement: revision 0.2, Phase 0 / Work Unit 11, dated 2026-09-17. Sections 16-20 record the first final-audit pass and its BLOCKING disposition. The original document-control table and sections 1-15 below remain historical WU10 revision 0.1 text. No final Phase 0 approval or Phase 1 authorization has been issued.

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

## 16. Work Unit 11 first final-audit record

### 16.1 Audit control and disposition

| Field | Current value |
|---|---|
| Audit revision | 0.2 supplement to this document |
| Audit date | 2026-09-17 |
| Audited input commit | `e9262d7a14bfb0df18f7444d60c0d06d59581e9f` |
| Input inventory | 18 Phase 0 Markdown files, listed in §19 |
| Owner instruction | `可以，继续Work Unit 11` |
| Approval interpretation | WU10-C01-WU10-C03 accepted as the submitted design for final review; no final baseline approval |
| Audit disposition | BLOCKING: four incomplete realization contracts |
| Decision register | `UNRESOLVED_DECISIONS.md` revision 0.6, §§17-20 |
| Prior decisions consolidated | SIT-D001-SIT-D027 and the recorded WU6-WU10 supplements |
| New decisions | SIT-D028-SIT-D031 |
| Outputs of this audit pass | This supplement and decision-register revision 0.6 |
| Final approval artifact | Not created |
| Runtime / CI tests | Not run; no product implementation exists in this baseline |

The approved plan permits a final consistency audit and requires unresolved blockers to remain visible. The present pass completes that inspection and records the findings. It does not satisfy the no-blocker condition for approving Phase 0.

Acceptance of a work-unit submission and verification that it discharged every assigned obligation are separate events. The WU10 package provides a useful layout, owner mapping and dependency posture, but its completion handoff overstated readiness: several requirements explicitly assigned to WU10 in WU6-WU9 remain stated only as future implementation responsibilities. The four findings below identify those missing contracts. No earlier theory, analytical definition or canonical oracle is rejected by this audit.

### 16.2 Approval-history reconciliation

The decision register's original WU5 status table left SIT-D026-SIT-D027 pending because subsequent units could not edit that file. Reporting §11.1 contains their later acceptance. Validation §9 and the later unit intakes record the reporting/case/test-planning basis. This document §1 records WU9-C01/WU9-C02 acceptance, and licensing revision 0.2 records the explicit Apache-2.0 selection.

Register revision 0.6 consolidates those events with their original scope. It also records the current WU11 intake as acceptance of the submitted WU10 design for final review. The preceding original decision text remains historical; a later acceptance is not backdated into it. Current status is 27 prior central decisions accepted in their recorded scope and four newly identified blockers.

WU9-C03's current choice is uniform Apache-2.0 for original engineering repository materials. The earlier split Apache/CC BY recommendation is superseded. Historical companion-version references and then-pending labels are interpreted using this reconciliation and licensing revision 0.2, rather than as new contradictory approvals. None of this grants a license over theory papers, third-party material or user evidence by association.

## 17. Final-audit findings

### 17.1 Blocking realization gaps

| Finding / decision | Exact missing realization | Controlling evidence | Required closure |
|---|---|---|---|
| W11-A01 / SIT-D028 | Bounded in-process capture, immutable normalization, compact byte measurement and loss-aware numbers | Privacy §§3.1, 8.1-8.2; validation §§11,17; architecture §§4,8,10 | One explicit input/capture/measurement protocol with paired file/library and boundary witnesses |
| W11-A02 / SIT-D029 | Deterministic report IDs, witness selection, exact serialization and library/CLI outcome mapping | Reporting §19.2; traceability §9; validation §17; architecture §§4,7,9 | One realization profile, fixed trusted option/outcome table and deterministic representative-witness rules |
| W11-A03 / SIT-D030 | Work-unit accounting, scope scheduling, shared-work charging and cancellation/result-commit points | Privacy §8.1; validation SIT-VG022 and §17; architecture §10 | A bounded execution protocol preserving the pure-core boundary and existing interruption semantics |
| W11-A04 / SIT-D031 | Supported filesystem primitives, private staging, path-race handling and no-clobber complete-pair publication | Privacy §§5-6; threat §14; architecture §§10-11; dependency §2 | A platform/operation/failure profile checked against official primitive behavior, with unsupported cases explicitly bounded |

SIT-D028-SIT-D031 each include alternatives, a recommended direction, affected trace/test families and acceptance evidence in the register. All remain BLOCKING. This audit records no selected implementation primitive, new dependency, changed ceiling, additional public analytical field or code.

**W11-A01.** The limit on a constructed Python dossier needs a specified compact measuring representation. Number and string representation can affect that measurement. The immutable-snapshot promise also needs an explicit capture and caller-concurrency contract; it cannot be justified by a module name alone. Existing input constraints remain valid while the realization is completed.

**W11-A02.** Two valid paths can support the same finding. Their selection and report-local identities need a stable rule before byte-level golden outputs can be frozen. Public invocation must also preserve the distinction between input rejection, an interrupted run, a completed audit with unavailable evidence, and a source-native failure record. The existing report schema supplies those meanings; the interface and renderer must realize them consistently.

**W11-A03.** Numeric resource ceilings are already fixed. What remains is the protocol that charges work and commits complete results under those ceilings. Uncharged preprocessing, shared support scans or implementation-specific scheduling cannot silently determine compliance. A cooperative time guard is retained; the audit demands no hard real-time or cross-host identical interruption guarantee.

**W11-A04.** Naming prospective Linux and Windows runners does not select the file-handle, permission or publication sequence required by the privacy contract. The issue concerns a missing bounded design, not a conclusion that the required protections are impossible. Choosing a narrower initial support profile would be a separate explicit scope decision, not an automatic fallback.

### 17.2 Reconciled and retained matters

**W11-A05: historical approval and license labels.** Reconciled through register §17 and this supplement. The original labels remain evidence of what was proposed at that time. The current Apache policy and later approval events control their respective scopes. No original approval is fabricated or silently rewritten.

**W11-A06: transitive trace ownership.** The architecture's nineteen logical-owner rows provide concrete module/test homes for the nineteen owner labels in traceability §3. The 35 stable Trace IDs do not need new numbers. Reporting's two renderer paths share one frozen result authority; validation governance is realized through tests/review rather than a new analytical runtime module. This ownership mapping passes the documentary check, while realization details in W11-A01-W11-A04 remain open.

**W11-A07: later-phase dependencies and executable evidence.** Exact build/test package versions, installed platform tests, measured performance and executable golden outputs remain intentionally assigned to later approved phases. Their absence alone is not a new Phase 0 blocker. The blockers above are narrower: earlier accepted documents specifically assigned their missing prose protocols to WU10.

## 18. Verification results and evidence limits

### 18.1 Registry and cross-document checks

The following are specification checks. They do not report product runtime success.

| Check | Observed result | Interpretation |
|---|---|---|
| Phase 0 input inventory | 18 expected Markdown paths present at the pinned commit | File presence verified; semantic readiness is evaluated separately |
| Theory map | 40 stable SIT-T IDs | No missing or additional numbered entry in the checked range |
| Product requirements | 16 stable SIT-P IDs | Existing product scope retained |
| Logical dossier | 12 canonical record kinds, 24 relation predicates, 9 assessment kinds | The WU3 vocabulary remains the input authority |
| Analytical families | 15 SIT-M families | No new analytical family introduced by WU9/WU10 |
| Trace register | 35 SIT-TR responsibilities | Each has source-map references; referenced source IDs resolve |
| Logical implementation owners | 19 | Each has an architecture owner row; no owner disappears during transitive mapping |
| Public analytical leaves | 57 | Reporting §17, traceability §5 and validation §12 contain the same leaf set |
| Field-test obligations | 228 distinct IDs | Exactly P/N/M/B for each of SIT-VF001-SIT-VF057 |
| Shared validation families | 26 SIT-VG sections | Cross-cutting rules remain additional obligations |
| Prerequisite catalog | 24 PC codes | Reporting and validation catalogs match |
| Non-result reasons | 40 codes | Reporting and validation catalogs match |
| Narrow finding conditions | 22 codes | Reporting and validation catalogs match |
| Success criteria | 66 stable SIT-SC IDs | Existing acceptance obligations retained; their existence is not a pass claim |
| Canonical case catalog | H7-01, three controlled variants and 28 W7 micro-cases | Logical oracles preserved; no machine-readable fixtures or byte oracles generated |

The raw text used for automated ID/set checks was matched to the pinned repository blob identities for the twelve locally available predecessor documents listed in §19. The WU9/WU10 documents were inspected through the connected repository. The audit does not count a repeated statement as a new independent test or a second reviewer.

### 18.2 Analytical and hero consistency

The core distinctions remain present across definitions, lineage, reporting and validation: Artifact versions, claim-bound contributions and origin events have separate units; comparison-set qualification is scope-specific; unknown ancestry cannot create independent roots; disagreement remains representable; and graph-derived findings retain the basis of their supplied premises.

The main six-contribution hero retains its five-to-one origin incidence. Under its qualified complete single-origin premises, the HHI is `(5^2 + 1^2) / 6^2 = 26/36`, displayed as `0.722222` when the defined decimal presentation is used. The one-origin selected variant retains `25/25`. These arithmetic checks concern the finite written oracle, not an implemented graph algorithm or a claim of source truth.

The seventh unresolved contribution remains in its original denominator and withholds full-population HHI. A seventh contribution with two known origins also withholds that scalar under the unallocated multi-parent rule, while preserving the distinction from unknown ancestry. Neither case is repaired by equal splitting or resolved-only filtering.

Correction and stage records retain their own populations. A submission, accepted handling and evidence-linked downstream change remain different records and units. Missing change evidence is not converted to a failed correction. Changing the selected source population does not silently change the pipeline cohort or correction targets. H7 and W7 expected meanings have not been rewritten to conceal the realization gaps.

### 18.3 Theory and licensing scope

The six supplied theory PDF byte identities were recomputed and matched the SHA-256 values already recorded in `SPEC_AUDIT.md`. This checks source version identity. It does not newly verify each cited empirical study, publication metadata, external standard or mathematical result.

The 35 trace responsibilities retain the distinction between source claims and toolkit operationalizations. No count or HHI is relabeled as entropy, mutual information, truth probability or measured error correlation. The local dossier remains caller-supplied evidence; structural consistency does not authenticate a coherently fabricated dossier.

The current licensing decision is the owner's uniform Apache-2.0 engineering policy. Its source-paper, third-party and user-input exclusions remain explicit. The policy's later application is separate from final Phase 0 approval. No root license text, package metadata or new distribution grant is created by WU11.

### 18.4 Boundary and review limitations

The pinned repository contains specification Markdown only. Planned Python paths and command examples are documentation, not executable product files. No package skeleton, runtime algorithm, machine-readable schema, executable fixture or CI workflow was present in the audited tree, and this audit adds none.

Source Integrity Toolkit retains its separate repository/runtime boundary from Recursive Integrity Toolkit. Future public-artifact adapters remain proposals with semantic preservation requirements. No import, shared core, database or compatibility certificate is introduced.

These checks are performed by the drafting assistant, with local authoring utilities and connected repository reads. No independent security review, runtime fault injection, empirical validation, platform support certification or complete distribution license clearance is claimed. Readiness remains blocked even though the identifier and ownership checks pass.

## 19. Pinned audit-input manifest

### 19.1 Repository snapshot

The table identifies the input to this first audit, commit `e9262d7a14bfb0df18f7444d60c0d06d59581e9f`. Git blob identities and byte sizes are taken from the connected repository tree. They identify file versions; they do not establish source truth or approval.

| Input file | Git blob identity | Bytes |
|---|---|---:|
| `CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` | `a08e94bee1e4c8aaa4a47fcdd79b1e8db0fe6911` | 129967 |
| `DEFINITIONS_AND_UNITS.md` | `36fd49115cd7a3a85be93eeeb480042a1b74496f` | 94436 |
| `DEPENDENCY_STRATEGY.md` | `591db2c814e1a924b1c8c474c51cdbe7e52c231d` | 10842 |
| `GOVERNANCE_AND_HANDOFF.md` | `396ecbf52208a1a1cd59cff13c20f436bf3dc582` | 14088 |
| `LICENSING_NOTES.md` | `3468b44ec858ac1068f041affe94f8c183e3289a` | 10911 |
| `OBSERVABILITY_AND_REPORTING.md` | `cf6c1d0aeb069cf5b68c3ea37b490dd6f5912208` | 111615 |
| `PHASE_0_PLAN.md` | `d5ea6f6dd79b5770dfe80a3677d76706c7e78db8` | 45379 |
| `PRIVACY_AND_DATA_HANDLING.md` | `8e7f6a1835104af4714826311db3ba92d1dd1c0f` | 28777 |
| `PROJECT_INSTRUCTIONS.md` | `20c0b8fb6a870ccb21acbfc2024096e95cf317a4` | 22037 |
| `REPOSITORY_ARCHITECTURE.md` | `08d72712b52557474d2f7c6109cf3504cf9421cc` | 19310 |
| `SOURCE_INTEGRITY_THREAT_MODEL.md` | `7ba8945cf68e0069d42ad975d5a9ceaeb047d75e` | 93871 |
| `SPEC_AUDIT.md` | `67f6b4ccb33f6db2aca508a64993661b3e28f3a9` | 42589 |
| `SUCCESS_CRITERIA.md` | `63151e95af72d6aea224858bc356f1528a013661` | 58182 |
| `THEORY_SOURCE_MAP.md` | `9cc299535f71b57f8800f6406723a689a6ce2560` | 56697 |
| `THEORY_TO_CODE_TRACEABILITY.md` | `a6b6c716636bb15bb569b257e9b82086c18185ab` | 65779 |
| `UNRESOLVED_DECISIONS.md` | `3b034483d660b9dcaad8ea2ea47d9c19d98d2ae9` | 108749 |
| `V0.1_PRODUCT_SPEC.md` | `ad896af3b749220b1f4adf979fbae4fa5f01b165` | 62420 |
| `VALIDATION_PLAN.md` | `701ec6a3e215638a02dd1eb82b2f503dd48d16e8` | 148233 |

Twelve files had exact matching local predecessor bytes: the plan, audit, source map, project instructions, definitions, lineage specification, reporting, product, validation, success criteria, traceability and the input decision register. Their Git blob hashes were recomputed before using them for document checks. The six newer files without a matching local predecessor were read through GitHub: dependency, governance, licensing, privacy, architecture and the WU9 threat revision. No whole-file SHA-256 result for those six is invented here.

This is a pinned input manifest for a blocked audit. The plan's final SHA-256 approval manifest remains a requirement for the corrected approval candidate. It must be computed from the actual final files after remediation and re-audit. This table cannot substitute for it.

### 19.2 Output identities and preservation

The decision-register update was committed at `40edd886c816af0f28f4648566ed482140e82c6a`, with returned blob identity `0245b20b77a41a9f7a0fad510dd4dc5553715592`. GitHub's comparison with the input commit reports 140 added lines and no deleted lines for that update. Its banner and sections 17-20 supply the current view while retaining the original history.

This governance update likewise retains the original control table and sections 1-15, adds a current-reading banner and appends sections 16-20. Its final commit/blob identity must be read from GitHub after publication; it is not self-declared inside its own bytes. The combined final comparison for this audit should show only the two allowed Markdown updates. Any unexpected change prevents a preservation claim until examined.

## 20. Stop point, remedy request and re-audit contract

The first WU11 audit pass stops at **SIT-D028-SIT-D031**. Approval readiness is BLOCKING. No `PHASE_0_APPROVAL.md`, `PHASE_1_PLAN.md`, `LICENSE`, package metadata, executable schema or implementation is created.

The recommended next work is a bounded **WU10 completion/remediation pass within Phase 0**. On explicit owner authorization, finish the four missing prose protocols in the architecture and dependency documents, updating reporting/validation only where their owned contracts require clarification, and record each resolution in the decision register. Retain the original source theory, product scope, analytical units, 57 leaves, H7/W7 logical oracles, no-network boundary and WU9 numerical ceilings.

A proposed remedy that changes any of those retained contracts must be identified as a new scoped decision, not presented as an editorial repair. Narrowing platform support, adding a native or third-party dependency, weakening byte determinism, or moving a Phase 0 gate to a later phase requires explicit owner selection and corresponding consumer changes. No such choice is made by this audit record.

The re-audit must verify the actual remedy text against each decision's acceptance conditions, rerun the registry/field/trace checks, review the complete updated dependency and security boundaries, and inspect the final changed-file set. It must then assemble the SHA-256 manifest for the corrected candidate. A missing contract cannot be marked resolved solely because its recommended direction was accepted.

Only after that re-audit finds no in-scope blocker should the complete Phase 0 baseline be presented for the owner's explicit final approval. The approval record may then be created with the approved file identities and exact next-phase authorization. Until then, the project remains in Phase 0.
