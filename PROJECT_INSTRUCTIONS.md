# PROJECT_INSTRUCTIONS

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Target release | v0.1 |
| Phase / work unit | Phase 0 / Work Unit 2 |
| Revision | 0.1 |
| Date | 2026-09-16 |
| Status | PROPOSED FOR REVIEW; existing approved-plan boundaries remain controlling |
| Theory Owner | Xiangyu Guo |
| Technical Owner | Unassigned |
| Purpose | Execution, authority, evidence and handoff rules for this independent project |
| Current permitted outputs | `V0.1_PRODUCT_SPEC.md`, `PROJECT_INSTRUCTIONS.md`, `UNRESOLVED_DECISIONS.md` |
| Final Phase 0 approval / Phase 1 authorization | Not issued |

## 1. Project objective and current state

Source Integrity Toolkit is being specified as a deterministic, local auditor of supplied claim, evidence, provenance, evaluator and correction records. It is intended to distinguish apparent plurality from documented origins and qualified independence, while preserving unknowns and evidence of correction.

The operative release proposal is [V0.1_PRODUCT_SPEC.md](V0.1_PRODUCT_SPEC.md). The theory basis remains [THEORY_SOURCE_MAP.md](THEORY_SOURCE_MAP.md) and the six source files inventoried in [SPEC_AUDIT.md](SPEC_AUDIT.md). Decisions are tracked in [UNRESOLVED_DECISIONS.md](UNRESOLVED_DECISIONS.md).

The current work is specification drafting. There is no Source Integrity Toolkit implementation in this delivery. No repository, package, schema, fixture, CI workflow or runtime result is created here.

### 1.1 Approval history

The following events have different meanings:

| Event | Recorded effect |
|---|---|
| The user approved the delivered Phase 0 plan and requested the next unit | The plan's controlled documentation workflow was authorized |
| Work Unit 1 delivered an audit, 40-entry theory map and 15 recommended decisions | Those documents became review inputs; delivery alone did not approve the recommendations |
| The user then requested continuation | Preparation of the next documentation package is authorized; this is not recorded as an explicit option selection for all decisions |
| Work Unit 2 is delivered | Its requirements and new choices are submitted for review; the full Phase 0 baseline and implementation remain unapproved |

The source plan's file header and historical Work Unit 1 headers are preserved. Actual later approval events must be recorded separately, rather than rewriting historical bytes to imply earlier approval.

### 1.2 Conditional drafting and hard gates

This package presents the proposed consequence of following the recommended directions. It does not clear the Work Unit 1 consumer gates. In particular, product adoption remains held at SIT-D001, SIT-D002, SIT-D003 and SIT-D015, together with the new product choices SIT-D016-SIT-D018.

A proposed text is not an approved consumer contract. It cannot authorize implementation, certify a passed work unit, or be used to evade an unresolved stop condition. Where a gate blocks finalization, the next action is an owner decision or an explicitly requested alternative proposal. No subsequent work unit is executed in this delivery.

## 2. Authority and source discipline

### 2.1 Product authority

Use the following authority structure after approval events exist:

1. The Theory Owner's explicit, scoped decisions and plan amendments.
2. The approved Phase 0 plan and its file/write boundaries.
3. Approved decisions in the current decision register.
4. Approved product, object, data, reporting and validation specifications within their assigned responsibilities.
5. Approved architecture, dependency, privacy, licensing and handoff rules.
6. Examples, drafts and convenience conventions.

A lower item cannot silently change a higher item. If two approved consumer specifications conflict, stop the affected work and expose the conflict. Ordering is not permission to edit a losing document without authorization.

The current documents are proposals. The already approved plan remains binding irrespective of their status.

### 2.2 Theory authority

Preserve the source hierarchy in the plan: SIL, UIL, EC and HDL provide the primary theory stack; EBC is background; BVL supplies only explicitly mapped adjacent concepts.

Product authority selects a software representation. It does not retroactively change what a paper says. Retain separate labels for source definitions, structural claims, formal-model results, inherited theorems, source corollaries, empirical reports, governance proposals and toolkit operationalizations.

Use the original Work Unit 1 source IDs and one-based PDF page locators. Do not invent a publication date, DOI, missing author attribution or independent empirical confirmation. Repeated arguments across the author's papers are theoretical connections, not additional independent experimental replications.

This documentation does not update cited standards or verify real-world case histories. A later request for external research must identify that expanded evidence scope and distinguish it from the supplied-source baseline.

### 2.3 Approval granularity

Keep four events separate: accepting a delivered document, selecting a recommended direction, freezing the complete Phase 0 baseline, and authorizing an implementation phase.

A single clear instruction can approve a whole enumerated recommendation package. Separate ceremonies for each ID are unnecessary. Record the scope, selected options, exact qualification and date, and retain the original recommendation history. A generic continuation request is insufficient evidence for claiming that every pending option or the complete baseline was approved.

The plan's final dispositions remain `APPROVED`, `DEFERRED`, `REJECTED` and `BLOCKING`. A decision may be approved as a direction while its exact fields remain assigned to a later unit, but that distinction must be explicit in its record. Deferral also requires limiting or excluding the affected feature. It cannot conceal an in-scope implementation blocker.

## 3. Controlled work and file boundaries

The approved plan defines eleven work units. Paths below refer to the intended specification root, not a statement that a GitHub repository already exists.

| Work unit | Allowed specification files | Boundary |
|---|---|---|
| 1. Theory audit and source map | `SPEC_AUDIT.md`; `THEORY_SOURCE_MAP.md`; `UNRESOLVED_DECISIONS.md` | Source extraction, translation issues and recommendations |
| 2. Product boundary | `V0.1_PRODUCT_SPEC.md`; `PROJECT_INSTRUCTIONS.md`; `UNRESOLVED_DECISIONS.md` | User, workflow, input/output surface, included capabilities and exclusions |
| 3. Ontology and graph | `DEFINITIONS_AND_UNITS.md`; `CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md`; `UNRESOLVED_DECISIONS.md` | Canonical objects, typed relations and their evidence semantics |
| 4. Analytical semantics | `DEFINITIONS_AND_UNITS.md`; `OBSERVABILITY_AND_REPORTING.md`; `V0.1_PRODUCT_SPEC.md`; `UNRESOLVED_DECISIONS.md` | Units, denominators, allocation, uncertainty and diagnostic selection |
| 5. Threat model | `SOURCE_INTEGRITY_THREAT_MODEL.md`; `V0.1_PRODUCT_SPEC.md`; `UNRESOLVED_DECISIONS.md` | Observable failure conditions and detection limits |
| 6. Observability | `OBSERVABILITY_AND_REPORTING.md`; `CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md`; `SUCCESS_CRITERIA.md` | Field-specific prerequisites, capability matrix and reporting limits |
| 7. Hero and micro-cases | `V0.1_PRODUCT_SPEC.md`; `VALIDATION_PLAN.md`; `SUCCESS_CRITERIA.md`; `CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` | Prose fixtures and expected structural conclusions |
| 8. Validation and traceability | `VALIDATION_PLAN.md`; `SUCCESS_CRITERIA.md`; `THEORY_TO_CODE_TRACEABILITY.md` | Test obligations and future ownership, without test implementations |
| 9. Privacy and licensing | `PRIVACY_AND_DATA_HANDLING.md`; `LICENSING_NOTES.md`; `SOURCE_INTEGRITY_THREAT_MODEL.md` | Data handling, security requirements and explicit license decisions |
| 10. Architecture and handoff | `THEORY_TO_CODE_TRACEABILITY.md`; `REPOSITORY_ARCHITECTURE.md`; `DEPENDENCY_STRATEGY.md`; `GOVERNANCE_AND_HANDOFF.md` | Future module ownership, dependencies and interchange |
| 11. Final audit | The Phase 0 Markdown bundle listed in the approved plan | Consistency audit and approval preparation; approval record only after actual approval |

The allowlist is controlling. Updating a shared register or convenient earlier document outside a unit's allowed set requires explicit authorization or a return to an authorized unit. No automatic exception is created for cleanup, formatting or status changes.

### 3.1 Work Unit 2 exact output contract

Create only the two new specifications and an updated decision-register snapshot. Archive packaging may contain those three files. Packaging does not authorize additional project files.

Keep the Work Unit 1 input directory unchanged. The Work Unit 2 register is revision 0.2 and is the proposed active successor to revision 0.1. Preserve the old version in its delivery archive. The audit and theory map remain historical source-basis records; their headers are not silently rewritten.

No `PHASE_0_APPROVAL.md`, Phase 1 plan, product code, machine-readable schema, executable fixture, dependency manifest or CI file belongs to this delivery. No remote write is authorized.

### 3.2 Out-of-order work

Before starting a unit, identify its inputs, current authorizations, decision gates and allowed files. Stop if a needed approved baseline cannot be located or conflicts materially with another input.

Do not make progress appear complete by prematurely assigning a schema, metric or fixture that belongs to another unit. Product-level choices can define what later work must specify; they do not constitute that later specification.

## 4. Evidence rules for every specification

### 4.1 Preserve the inquiry

Every evidence or independence conclusion needs a target, scope and time. Keep artifact identity, actor identity, origin event, claim contribution and validation activity separate until the approved ontology determines their representation. An artifact's role can differ between claims.

A shared event does not by itself establish shared acquisition. Different analyses of one dataset do not create different data-collection origins. Different model names or publishers cannot prove independence. [SIT-T020, SIT-T035-SIT-T036]

### 4.2 Preserve assertion provenance

Supplied assertions must retain their author or attestor, method, supporting references, scope and uncertainty. Inferred relationships supplied by another investigator remain attributed inferences. Derived graph findings identify their input assertions and permitted derivation rule.

Citation, derivation, ownership, support, validation and correction have different meanings. No generic traversal may substitute one for another. Conflicting assertions and cross-version history must survive; exact invalidity and supersession rules belong to Work Unit 3. [SIT-T008, SIT-T022, SIT-T032]

### 4.3 Preserve unknowns

Missing upstream history is not a new root. A count of unresolved references says how many references were observed, not how many hidden origins exist. Missing, undisclosed, disputed and inapplicable evidence require distinct treatment where they affect interpretation.

Removing a known dependency from a bundle may change the observed graph. It cannot, without new evidence, create a stronger qualified independence finding. Do not fabricate finite bounds on hidden multiplicity from a finite file size. [SIT-D005-D006]

### 4.4 Preserve types of validation and judgment

Keep identity/process verification separate from validation of a claim. Keep human contribution, model judgment, formal checking and empirical constraint separate. A human-reviewed badge does not show what a human contributed. A model review cannot replenish human judgment by relabeling its origin.

Record SIL's strong judgment-layer requirement alongside EC's type-appropriate validation and HDL's external-constraint boundaries. The recommended product handling is traceable through SIT-D002; it does not modify the sources. [SIT-T004-SIT-T005, SIT-T011, SIT-T020]

### 4.5 Preserve the stages of presence and correction

External-input admission, preservation, selection and downstream influence need separate evidence. Correction requires attention to a declared route, applicable authority, actual handling and linked downstream effects. A record of one successful action need not establish sustained capacity. A partial graph cannot support a universal no-route conclusion.

Keep objections, accepted corrections, reasoned rejections and actual changes distinct. The toolkit does not decide that an objection is right merely because it was submitted. [SIT-T024, SIT-T026, SIT-T029, SIT-T034, SIT-T039]

### 4.6 Preserve anomalous and contested material

Retain original context or an authorized protected reference for evidence that does not fit the current classification. Do not infer suppression without intake, exclusion or stage evidence. Do not treat disagreement as corruption, equal evidentiary strength, or a requirement for automated adjudication. [SIT-T019, SIT-T021, SIT-T023, SIT-T032]

### 4.7 Preserve limits of numbers

Every proposed number requires a unit, scope, denominator, attribution rule, missing-data treatment and interpretation. No high/low labels, concentration index or default allocation is selected for convenience. Optional numerical diagnostics remain gated at Work Unit 4.

Presence × Integrity and EC's conjunctive requirements cannot be implemented by multiplying arbitrary percentages. No source graph alone measures mutual information, semantic gradient, causal correction elasticity, model safety or statistical error correlation. [SIT-T003, SIT-T015, SIT-T017, SIT-T027-SIT-T031, SIT-T037]

## 5. Identifier and change discipline

Preserve SIT-A001-SIT-A015, SIT-T001-SIT-T040 and SIT-D001-SIT-D015 with their Work Unit 1 meanings. This unit adds SIT-D016-SIT-D018 and product requirements SIT-P001-SIT-P016.

A new issue receives a new ID. Do not reuse a prior ID for a different question. Product IDs do not substitute for the later implementation Trace IDs. Do not assign a module path, test path or public field name solely to make a traceability table look complete before the relevant unit.

Each material change must identify the affected source IDs, decision IDs, product requirements, field families, consuming documents and test obligations. Separate a clarification from a change in product scope. A source revision requires its own version/byte identity review; filename suffixes do not establish precedence.

Later acceptance of recommendations must be recorded in the active register with its evidence. The historical Work Unit 1 package remains an immutable snapshot of what was proposed at that point.

## 6. Documentation-only execution and future runtime constraints

### 6.1 Current drafting boundary

Phase 0 may use general document utilities to read local files, inspect source pages, check references, hash files and package Markdown. Those are authoring operations, not a product implementation.

No production package, graph algorithm, schema, runtime dependency, CLI, live fetcher, model judge, test suite or workflow may be created during this phase. Do not install an implementation library merely to illustrate a future design.

Theories remain reference assets. No full theory PDF, copied font, private evidence or unrelated file is included in the delivery ZIP.

### 6.2 Planned runtime boundary

Subject to the pending directions, v0.1 is offline and local. Text, URLs, metadata and mapping values remain inert data. They cannot authorize network calls, script execution, policy changes or removal of findings.

Do not add network-enabled opt-ins, telemetry, extensible code hooks or remote model calls through a convenience adapter. Report writing is limited to an explicit authorized destination and must preserve source inputs. Concrete parser limits, resource budgets and export controls are specified later, before implementation.

Protected source identifiers must retain their assurance limits and known dependency links. Redaction cannot silently transform a known shared origin into several independent origins. A file checksum identifies bytes; it does not establish author identity or claim truth.

### 6.3 Cross-project boundary

Do not edit Recursive Integrity Toolkit through this project's authority. Do not assume that its code, source schema, licensing or phase approvals apply here. Shared concepts and overlapping provenance techniques are permitted; shared internal implementation is not a current dependency.

Any future interchange must explicitly map scope, versions, relationship types, assertion provenance and uncertainty. If those semantics cannot be preserved, compatibility must remain unclaimed. [SIT-D015]

## 7. Work-unit acceptance and handoff protocol

Every unit should finish with a small, evidence-based handoff containing the files created or changed, applicable decisions, consistency checks, unresolved gates and the precise next stopping point. These details may live in the allowed documents; a new standalone completion file is not automatically permitted.

Do not claim independent review when the same assistant performed all drafting and checks. Do not equate syntactic checks with validation of a scientific theory. Do not claim CI, runtime tests, performance measurements, source verification or GitHub changes unless those actions occurred under authorization.

Approval handling should be compact. One explicit instruction accepting the enumerated recommendation package is sufficient to record its directions. A later schema or algorithm that introduces a genuinely new choice still requires its assigned decision.

### 7.1 Current delivery checks

For this unit, check:

| Check | Evidence required |
|---|---|
| Allowed outputs only | Two new Markdown specifications plus decision register revision 0.2; ZIP contains exactly those files |
| Baseline preserved | Prior plan, Work Unit 1 files and six PDFs retain their reviewed hashes |
| Decision continuity | Original 15 IDs, alternatives and recommendation text preserved; three new IDs appended |
| Product coverage | The fourteen product questions in PLAN §9 have explicit proposed answers or assigned detailed gates |
| Source traceability | Referenced theory IDs exist in the 40-entry map; sources use the existing page-locator scheme |
| No false approval | Pending decisions remain pending; no Phase 0 approval or Phase 1 authorization is issued |
| No premature implementation | No code, schemas, executable fixtures, dependency files or CI artifacts in the delivery |
| Readability and integrity | Markdown headings, tables, links, code fences and archive contents are checked |

These checks concern the documents being delivered. Future analytical acceptance cases in the product specification remain unimplemented.

### 7.2 Assembly of the specification folder

This work-unit archive is an **incremental package**, not the full Phase 0 baseline.

To assemble the working document set, place the two new specification files alongside the unchanged Work Unit 1 audit and source map. Use the revision 0.2 decision register as the active copy and retain revision 0.1 in its previous archive. Keep the originally delivered plan under its existing filename until an authorized repository-assembly step selects the canonical repository name.

Relative links to `SPEC_AUDIT.md` and `THEORY_SOURCE_MAP.md` resolve in that assembled folder. Their absence from this three-file ZIP is deliberate; they have not been regenerated or re-approved.

## 8. Phase 0 completion and Phase 1 protection

Phase 0 completes only when all required documents exist, the final audit finds no in-scope blocking decision, and the Theory Owner explicitly approves the complete baseline. The approval record must refer to actual file identities and actual decisions.

Only then may `PHASE_0_APPROVAL.md` be created. The plan limits Phase 1 to a repository scaffold: approved metadata, import-safe placeholders, structural schema scaffolds, test/fixture structure, governance and CI scaffolding. Analytical graph behavior, metrics, external-presence calculations, correction analysis, live crawling and analytical report generation remain prohibited in Phase 1.

Approval of a direction, a product document or a source audit must never be presented as authorization to skip that phase boundary.

## 9. Current handoff

Work Unit 2 delivers a product contract proposal, these execution instructions and the updated register. The package preserves Work Unit 1's recommended direction, specifies proposed input/output and minimum-release choices, and stops before Work Unit 3.

The next decision can accept the package and the enumerated recommended directions together. The next production unit, once the relevant gates are satisfied, is canonical ontology and graph semantics. Finalization of the full Phase 0 baseline and all implementation remain later actions.

### Document checks performed for this delivery

Local document checks confirmed the three-file allowlist, the unchanged hashes of the plan and three Work Unit 1 inputs, and the six PDF hashes recorded by the source audit. All referenced theory IDs resolve within the existing 40-entry map; the register contains 18 unique decision records and the product table contains 16 unique product requirements.

The original 15 decision records are preserved verbatim inside register revision 0.2. Markdown parsing, table recognition, local-link resolution against the assembled document set, balanced fences and UTF-8 text checks were performed. The ZIP is checked separately for exactly the three permitted Markdown files and byte-for-byte agreement with them.

These are drafting and packaging checks. No runtime product tests, CI, empirical experiments, independent second review or GitHub changes were performed.
