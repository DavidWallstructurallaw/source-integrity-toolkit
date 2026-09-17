# UNRESOLVED_DECISIONS

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Target release | v0.1 |
| Phase / current work unit | Phase 0 / Work Unit 5 |
| Revision | 0.5 |
| Date | 2026-09-17 |
| Theory Owner | Xiangyu Guo |
| Decision authority | Theory Owner; product and technical choices remain explicit |
| Current register state | SIT-D001-SIT-D018 directions remain approved; SIT-D019-SIT-D025 accepted in the current instruction; SIT-D026-SIT-D027 submitted |
| Execution authorization | “可以，继续”, following the WU4 offer to approve the detailed package and proceed to WU5 |
| Supersedes for current register state | Work Unit 4 revision 0.4; prior files remain unchanged |
| Formal complete Phase 0 approval | Not issued |
| Implementation authorization | None |

**Current reading rule.** Section 2 and each individual approval record carry the current dispositions. Earlier handoffs, intake statements and recommendation text are retained as history; their once-pending wording cannot override later scoped approvals. WU5 adds the approval update for SIT-D019-SIT-D025 and two new threat decisions. It does not backdate approval or alter any original recommendation body. Duplicate historical heading numbers have been made non-numbered editorial headings; decision IDs are unchanged.

## 1. How this register is used

The plan approved the controlled Phase 0 workflow and its existing prohibitions. The named user acceptance events select recommendation packages within their documented scope. The current “可以，继续” follows the prior offer to accept SIT-D019-SIT-D025 and move to Work Unit 5; it is recorded as that contextual approval.

A recommended option remains a proposal until accepted. Approval of a direction is distinguished from approval of its later detailed realization. Previous acceptance of a named detailed contract likewise does not pre-approve a new threat, report, test or implementation choice.

The approved plan's final dispositions remain `APPROVED`, `DEFERRED`, `REJECTED` and `BLOCKING`. A blocking gate applies when the relevant document or feature is consumed, rather than retroactively forbidding preparation of alternatives. No in-scope blocker may be left unresolved at final Phase 0 approval.

No approval of this unit authorizes code, schemas, fixtures, CI or Phase 1. Where this register recommends a concrete input, output or metric convention, the recommendation is a toolkit operationalization rather than a formula or schema already contained in the source papers. IDs and source aliases retain their original meanings from [SPEC_AUDIT.md](SPEC_AUDIT.md) and [THEORY_SOURCE_MAP.md](THEORY_SOURCE_MAP.md).

### 1.1 Current approval chronology

| Event | Scope and evidence | Effect |
|---|---|---|
| The owner approved the delivered Phase 0 plan and requested the next unit | Explicit plan approval in this conversation | Controlled documentation workflow authorized; no final Phase 0 approval |
| WU1 and WU2 delivered recommended directions; the owner replied “可以，继续” after an offer to approve the package and proceed | Eighteen enumerated recommended directions | SIT-D001-SIT-D018 accepted for their stated scope |
| WU3 detailed contracts were delivered; the next request was “继续” | Continuation without a new explicit detailed-option record | WU4 conditional drafting authorized; SIT-D019-SIT-D021 then remained pending |
| WU4 delivered the analytical package and offered acceptance of SIT-D019-SIT-D025 before WU5; the owner replied “可以，继续” | Current contextually scoped acceptance | SIT-D019-SIT-D025 accepted; WU5 drafting authorized |
| WU5 delivers this revision | New threat and self-protection choices | SIT-D026-SIT-D027 submitted; neither is pre-approved |

## 2. Decision index and current gates

| ID | Decision | Original consumer gate | Recommended option | Current disposition |
|---|---|---|---|---|
| SIT-D001 | Preserve source-local entropy meanings | Before product claims / analytical semantics | B | APPROVED DIRECTION; no entropy diagnostic |
| SIT-D002 | Represent synthetic judgment without replacing human corrective input | Before product/ontology definition | C | APPROVED DIRECTION; contribution/evidence distinctions retained |
| SIT-D003 | Bounded caller-prepared local dossier workflow | Before Work Unit 2 adoption | B | APPROVED DIRECTION; offline deterministic scope |
| SIT-D004 | Artifact, actor, origin and claim-contribution separation | Before Work Unit 3 | B | APPROVED DIRECTION; realized by accepted SIT-D019 |
| SIT-D005 | Evidence-qualified, scoped process independence | Before Work Unit 3 | B | APPROVED DIRECTION; realized by accepted SIT-D020/SIT-D022 |
| SIT-D006 | Explicit unresolved boundaries and hidden multiplicity limits | Before Work Units 3-4 | B | APPROVED DIRECTION; realized by accepted SIT-D020-SIT-D023 |
| SIT-D007 | Typed attributed assertions and conflict/version preservation | Before Work Unit 3 | B | APPROVED DIRECTION; realized by accepted SIT-D020/SIT-D021 |
| SIT-D008 | Externality, time and four stage distinctions | Before Work Unit 4 | B | APPROVED DIRECTION; realized by accepted SIT-D024 |
| SIT-D009 | Route, authority, handling, linked effect and capacity separation | Before Work Units 3-4 | B | APPROVED DIRECTION; realized by accepted SIT-D019/SIT-D024 |
| SIT-D010 | Descriptive profiles before restricted numerical diagnostics | Before Work Unit 4 | B | APPROVED DIRECTION; realized by accepted SIT-D023/SIT-D025 |
| SIT-D011 | Separate layer/role axes | Before Work Unit 3 | B | APPROVED DIRECTION; realized by accepted SIT-D019/SIT-D020 |
| SIT-D012 | Per-capability observability with non-result reasons | Before Work Unit 6 | B | APPROVED DIRECTION; final matrix/statuses remain WU6 work |
| SIT-D013 | Context and finite-universe retention | Before Work Units 4-5 | B | APPROVED DIRECTION; realized by accepted SIT-D024 |
| SIT-D014 | Local privacy-preserving, inert-data baseline | Before Work Units 3 and 9 | B | APPROVED DIRECTION; identity realized; controls/license remain WU9 |
| SIT-D015 | Separate products and no implicit shared runtime | Before product / architecture | B | APPROVED DIRECTION; WU10 owns exact interchange |
| SIT-D016 | Canonical local JSON bundle | Before Work Unit 3 | B | APPROVED DIRECTION; realized by accepted SIT-D021 |
| SIT-D017 | Required structural audit plus explicit numerical boundary | Before Work Units 3-4 | B | APPROVED DIRECTION; analytical boundary accepted |
| SIT-D018 | Equivalent JSON/Markdown and local CLI/library semantics | Before reporting / architecture | B | APPROVED DIRECTION; exact interfaces remain WU10 |
| SIT-D019 | Twelve core records and role/origin separation | Before Work Unit 3 adoption | B | APPROVED; original detailed scope retained |
| SIT-D020 | Evidence-bearing typed graph and nine assessments | Before Work Unit 3 adoption | B | APPROVED; no blanket ancestry or automatic verification |
| SIT-D021 | Versioned `sit-bundle/0.1` and structural handling | Before Work Unit 3 adoption | B | APPROVED; no executable schema authorized |
| SIT-D022 | Exact seed populations and assessment-scoped counts | Before Work Unit 4 adoption | B | APPROVED; no global independent-source count |
| SIT-D023 | Incidence and restricted HHI without allocation | Before Work Unit 4 adoption | B | APPROVED; no weighted multi-parent HHI or score |
| SIT-D024 | Evidence-specific stage/cohort/correction profiles | Before Work Unit 4 adoption | B | APPROVED; documentary process profiles only |
| SIT-D025 | Non-result, precision and comparison rules | Before Work Unit 4 adoption | B | APPROVED; final report enum remains WU6 |
| SIT-D026 | Narrow threat observations and evidentiary reporting | Before Work Unit 5 adoption | B | BLOCKING; submitted in WU5 |
| SIT-D027 | Auditor self-protection and no active detector/intervention | Before Work Unit 5 adoption | B | BLOCKING; submitted in WU5 |

The original alternative/recommendation bodies below remain intact. Historical no-approval records have been retained or explicitly quoted beside their later acceptance record; none is silently replaced with an earlier effective date. New detailed contracts remain scoped to their own unit and cannot authorize implementation.

## 3. Decision records

### SIT-D001: Preserve source-local entropy meanings

**Status:** APPROVED DIRECTION; Option B accepted.  
**Gate:** Cleared for the recorded direction; exact analytical definitions remain assigned to later units.  
**Audit finding:** SIT-A001  
**Theory map:** SIT-T003, SIT-T015, SIT-T027, SIT-T028, SIT-T033

**Question.** How should the toolkit use EBC’s AI entropy discussion while UIL formalizes diversity contraction and HDL distinguishes surface entropy from reality-coupled information?

**Alternatives**

- **Option A.** Select one global entropy interpretation and make every source conform to it in product language.
- **Option B.** Preserve each source’s variables and assumptions; keep EBC in its background role; prohibit a generic entropy diagnostic and do not equate support contraction, output entropy or mutual information.
- **Option C.** Require a new consolidated theory revision before any product planning proceeds.

**Recommended option.** B. This preserves the source texts and confines the product to meanings it can actually represent. The audit is not authorized to revise EBC, UIL or HDL. A later measurement project can select its own explicitly named quantity and experiment.

**Affected future public families.** Theory attribution, explanatory text, metric names, warning interpretations and any proposed collapse diagnosis.

**Downstream consequences.** The source-integrity report cannot contain a universal entropy, collapse or decay-probability field. No resampling result is calculated from graph depth or source count. Formal information quantities remain a separate research scope.

**Acceptance test for the decision.** A later spec can explain a shared upstream source without assigning the claim an entropy value or pretending that every summary is strictly destructive.

**Approval record:** On 2026-09-16, the user accepted the Work Unit 2 package and all recommended directions in the immediately preceding handoff by replying “可以，继续”. This records Option B only in the scope above; it does not approve the new Work Unit 3 details, a final Phase 0 baseline or implementation. Historical Work Unit 1/2 records remain unchanged.

### SIT-D002: Synthetic judgment, human input and type-appropriate validation

**Status:** APPROVED DIRECTION; Option C accepted.  
**Gate:** Cleared for the recorded direction; exact contribution and validation records remain later definitions.  
**Audit finding:** SIT-A002  
**Theory map:** SIT-T005, SIT-T011, SIT-T016, SIT-T020, SIT-T029

**Question.** What product rule preserves SIL’s strong judgment-layer claim alongside the plan’s no-automatic-source-type shortcut and EC/HDL’s distinctions among external constraints?

**Alternatives**

- **Option A.** Treat every synthetic judgment artifact as automatically invalid and exclude it from the dossier.
- **Option B.** Admit any synthetic judge as equivalent to independent human correction once its identity differs from the generator.
- **Option C.** Represent synthetic judgment with its disclosed lineage; never count a synthetic judge, model consensus or mere human authorship as proof of renewable human judgment. Preserve actual human contribution separately from formal or empirical validation and from external reality-bearing constraints.

**Recommended option.** C. Keep SIL’s concern about replacement of human judgment explicit. A model-derived judgment can be recorded without satisfying that requirement. A human review may supply substantive new judgment, or it may merely repeat a model; the contribution must be documented. Execution, physical measurement and formal checking remain type-appropriate constraints rather than being relabeled human judgment.

**Affected future public families.** Judgment origin, evaluator role, human contribution, correction source, validation method, generation history and epistemic status.

**Downstream consequences.** No automatic quality rule based solely on human/synthetic tags. No synthetic-only evaluation chain can be called independent human correction. Any unresolved stronger normative reading of SIL remains visible for the owner rather than being settled by the schema designer.

**Acceptance test for the decision.** The future spec can distinguish a model summary, a model judge, a human’s substantive independent review and an independently produced execution result, without forcing all four into one validity flag.

**Approval record:** On 2026-09-16, the user accepted the Work Unit 2 package and all recommended directions in the immediately preceding handoff by replying “可以，继续”. This records Option C only in the scope above; it does not approve the new Work Unit 3 details, a final Phase 0 baseline or implementation. Historical Work Unit 1/2 records remain unchanged.

### SIT-D003: Primary v0.1 workflow and automation boundary

**Status:** APPROVED DIRECTION; Option B accepted.  
**Gate:** Cleared for the recorded direction; exact input and outputs remain subject to the adopted detailed contract.  
**Audit finding:** SIT-A003  
**Theory map:** SIT-T007-T010, SIT-T022, SIT-T035, SIT-T040

**Question.** What does the first release accept and analyze without claiming to discover hidden ancestry or operate the full Source Integrity Layer?

**Alternatives**

- **Option A.** Live web crawling, automatic claim extraction, entity resolution, source classification and trust-ranked retrieval.
- **Option B.** A local, caller-prepared structured evidence dossier with explicit claims, artifact versions, provenance assertions, evaluator roles, correction records and declared coverage; deterministic analysis of the supplied relationships.
- **Option C.** A documentation-only checklist with no planned graph analysis.

**Recommended option.** B. Start with claim-scoped AI-answer or RAG evidence bundles, while allowing citation, benchmark and dataset dossiers that use the same schema. The actual file format is decided in Work Unit 2; the graph record contract is decided in Work Unit 3. Text excerpts can serve as evidence, but the initial runtime does not extract hidden relationships from them.

**Affected future public families.** Input contract, claims, evidence records, supplied assertions, analysis boundary, tool requirements and result limitations.

**Downstream consequences.** No required LLM, network call, crawler, reputation service or intervention authority. Every asserted source relation retains its supplier and supporting evidence. A provenance audit cannot certify unobserved outside history.

**Acceptance test for the decision.** A complete hypothetical source chain can be analyzed without browsing, and an incomplete chain produces a bounded report rather than invented ancestors.

**Approval record:** On 2026-09-16, the user accepted the Work Unit 2 package and all recommended directions in the immediately preceding handoff by replying “可以，继续”. This records Option B only in the scope above; it does not approve the new Work Unit 3 details, a final Phase 0 baseline or implementation. Historical Work Unit 1/2 records remain unchanged.

### SIT-D004: Artifact, actor, origin and claim contribution

**Status:** APPROVED DIRECTION; Option B accepted.  
**Gate:** Cleared as an ontology direction; exact realization is submitted in SIT-D019.  
**Audit finding:** SIT-A004  
**Theory map:** SIT-T008, SIT-T020, SIT-T022, SIT-T032, SIT-T035, SIT-T036

**Question.** What distinctions prevent one Source object from conflating a webpage, a person, a measurement and a piece of claim support?

**Alternatives**

- **Option A.** One generic Source class with a global independent flag and source type.
- **Option B.** Separate versioned artifacts, source actors, claim-specific evidence contributions, origin or acquisition/validation activities, and typed assertions linking them. Final object names remain a Work Unit 3 decision.
- **Option C.** A publication-only graph with no claims or evidence roles.

**Recommended option.** B. An origin can be a measurement or testimony event, an authoritative document for a documentary claim, or a type-appropriate validation artifact/process. The origin role remains explicit. A data-collection origin is distinct from later reanalysis of the same data.

**Affected future public families.** Claim identity, artifact version, source actor, acquisition or validation activity, evidence role, transformation and origin role.

**Downstream consequences.** One artifact can be derivative for one claim and original for another. Mixed artifacts retain both contributions. Several observations of the same event can remain separate if their acquisition independence is supported.

**Acceptance test for the decision.** The spec can represent two independent measurements of one event, two analyses of one measurement dataset, and one publication containing both copied and newly gathered material without conflating their units.

**Approval record:** On 2026-09-16, the user accepted the Work Unit 2 package and all recommended directions in the immediately preceding handoff by replying “可以，继续”. This records Option B only in the scope above; it does not approve the new Work Unit 3 details, a final Phase 0 baseline or implementation. Historical Work Unit 1/2 records remain unchanged.

### SIT-D005: Independence standard and dependency dimensions

**Status:** APPROVED DIRECTION; Option B accepted.  
**Gate:** Cleared as a product direction; detailed qualification is submitted in SIT-D020 and counts remain Work Unit 4.  
**Audit finding:** SIT-A005  
**Theory map:** SIT-T011, SIT-T016, SIT-T018, SIT-T020, SIT-T030, SIT-T035, SIT-T036

**Question.** What evidence can support an independence description without pretending to prove statistical independence from a partial graph?

**Alternatives**

- **Option A.** Classify disconnected components or different domains as independent.
- **Option B.** Use scoped process-independence assessments with explicit evidence and dependency dimensions; distinguish demonstrated overlap, supported separation and unexamined dimensions.
- **Option C.** Require a full probabilistic model of all dependencies before any independence discussion.

**Recommended option.** B. Specify at least the relevant acquisition, analytical-method, model/training, evaluative-rubric and organizational-control dependencies where the inquiry requires them. Do not automatically propagate one dimension into another. A common owner can be relevant without proving copied observation; common data can remain relevant despite separate authors.

**Affected future public families.** Comparison set, independence basis, process identity, known overlaps, assessed dimensions, unexamined dimensions and assertion evidence.

**Downstream consequences.** Independence is claim- and task-relative. No transitive closure of independence and no conversion of pairwise process assessments into mutual statistical independence. Any group count must disclose the required dimensions and comparison set.

**Acceptance test for the decision.** A shared-data pair can be described as separate analyses with a common collection origin. A same-model-family candidate/judge pair retains its known overlap. Three disconnected fragments with unexamined ancestry cannot become three independent sources.

**Approval record:** On 2026-09-16, the user accepted the Work Unit 2 package and all recommended directions in the immediately preceding handoff by replying “可以，继续”. This records Option B only in the scope above; it does not approve the new Work Unit 3 details, a final Phase 0 baseline or implementation. Historical Work Unit 1/2 records remain unchanged.

### SIT-D006: Unknown ancestry and root-count claims

**Status:** APPROVED DIRECTION; Option B accepted.  
**Gate:** Cleared for unknown preservation; exact endpoints are SIT-D020-SIT-D021 and numeric handling remains Work Unit 4.  
**Audit finding:** SIT-A006  
**Theory map:** SIT-T008, SIT-T022, SIT-T036, SIT-T038, SIT-T039

**Question.** How should the system report unresolved ancestry without creating fictitious root cardinality?

**Alternatives**

- **Option A.** Treat every terminal or unresolved node as a separate root.
- **Option B.** Separate documented origins, supported independent origin sets and unresolved upstream boundaries; expose unknown multiplicity and withhold unsupported totals.
- **Option C.** Reject every dossier containing any unknown provenance.

**Recommended option.** B. Replace the plan’s unqualified Unknown Root Count with a clearly defined count of observed unresolved boundaries if useful. Do not claim this equals the number of unknown roots. Numeric bounds require a specific finite candidate universe and stated assumptions; otherwise the result remains unavailable rather than falsely precise.

**Affected future public families.** Root inventory, unresolved references, origin multiplicity, assurance basis, coverage declarations and numeric nullability.

**Downstream consequences.** Unknowns cannot increase a certified independence count. Concentration reports retain unresolved contribution separately and never silently renormalize it away. Absence in a partial graph does not prove a source or route absent outside the graph.

**Acceptance test for the decision.** Three unresolved parent references remain three unresolved references, even when they could conceal one shared origin or many different origins. The report cannot assign a finite upper bound without a supporting universe.

**Approval record:** On 2026-09-16, the user accepted the Work Unit 2 package and all recommended directions in the immediately preceding handoff by replying “可以，继续”. This records Option B only in the scope above; it does not approve the new Work Unit 3 details, a final Phase 0 baseline or implementation. Historical Work Unit 1/2 records remain unchanged.

### SIT-D007: Assertions, edge semantics and conflicting histories

**Status:** APPROVED DIRECTION; Option B accepted.  
**Gate:** Cleared as a direction; exact record and relation realization is submitted in SIT-D020-SIT-D021.  
**Audit finding:** SIT-A007  
**Theory map:** SIT-T008, SIT-T013, SIT-T022, SIT-T026, SIT-T032, SIT-T036

**Question.** Are input relations facts, or attributed assertions that may have different knowledge status, time and support?

**Alternatives**

- **Option A.** Store unqualified edges and use all edge types interchangeably in ancestry analysis.
- **Option B.** Store typed, scoped assertions with their asserter, evidence, method, time and qualifications; construct analysis-specific views without erasing conflicts.
- **Option C.** Let an LLM infer and resolve all disputed edge meanings.

**Recommended option.** B. Citation, derivation, identity, ownership, evidence support, validation and correction are different relation families. Artifact versions remain distinct. Directly observed metadata, source declarations and investigator inferences remain distinguishable. Conflicting evidence is represented rather than silently overwritten.

**Affected future public families.** Relation identity, endpoint types, direction, assertion origin, provenance evidence, scope, timestamps, supersession and conflicts.

**Downstream consequences.** Graph traversal uses approved edge semantics. A malformed derivation history may be invalid for that analysis, while an ordinary citation cycle can be a valid observable pattern. Exact rejection rules are specified later.

**Acceptance test for the decision.** A citing source does not become an original observation, and a later correction or source version does not delete the historical artifact that an earlier answer used.

**Approval record:** On 2026-09-16, the user accepted the Work Unit 2 package and all recommended directions in the immediately preceding handoff by replying “可以，继续”. This records Option B only in the scope above; it does not approve the new Work Unit 3 details, a final Phase 0 baseline or implementation. Historical Work Unit 1/2 records remain unchanged.

### SIT-D008: External presence, currency and downstream influence

**Status:** APPROVED DIRECTION; Option B accepted.  
**Gate:** Cleared for staged evidence direction; exact fractions/rates remain Work Unit 4 and reporting remains Work Unit 6.  
**Audit finding:** SIT-A008  
**Theory map:** SIT-T001, SIT-T016, SIT-T026, SIT-T029, SIT-T031

**Question.** Can presence be computed from a recently ingested record, or must the source and pipeline stages remain separate?

**Alternatives**

- **Option A.** Use ingestion recency or source freshness as the presence measure.
- **Option B.** Record external-origin qualification, inquiry/time relevance and separate evidence for admission, preservation, selection and downstream effect.
- **Option C.** Require controlled causal experiments for every stored source.

**Recommended option.** B. Support a partial profile where evidence exists. Do not claim effective replenishment when only admission is known. Relevance to the inquiry’s time and boundary is required; no universal age threshold is introduced. Direct causal-effect claims require stronger evidence than ordinary pipeline logs.

**Affected future public families.** Source observation time, publication time, acquisition time, audit horizon, boundary, pipeline stage, retention and output-effect evidence.

**Downstream consequences.** A static dossier may leave effective presence unobservable. An older original source can remain appropriate to a historical claim. A freshly published derivative can add no new observation.

**Acceptance test for the decision.** The report can distinguish an external anomaly accepted into storage but filtered out before retrieval from one that demonstrably alters a later output.

**Approval record:** On 2026-09-16, the user accepted the Work Unit 2 package and all recommended directions in the immediately preceding handoff by replying “可以，继续”. This records Option B only in the scope above; it does not approve the new Work Unit 3 details, a final Phase 0 baseline or implementation. Historical Work Unit 1/2 records remain unchanged.

### SIT-D009: Correction channels and evidence of effectiveness

**Status:** APPROVED DIRECTION; Option B accepted.  
**Gate:** Cleared for evidence separation; ontology realization is SIT-D019-SIT-D020 and numeric/report treatment remains later.  
**Audit finding:** SIT-A009  
**Theory map:** SIT-T011, SIT-T013, SIT-T024, SIT-T026, SIT-T034, SIT-T039

**Question.** What is required to distinguish a declared correction route from operative correction?

**Alternatives**

- **Option A.** Treat any reachable review or complaint node as effective corrective capacity.
- **Option B.** Separate declared route, applicable authority and timing, observed handling, linked downstream change and sustained capacity evidence.
- **Option C.** Require a full queueing and causal intervention model before any correction record can be represented.

**Recommended option.** B. Permit recording each layer separately. A route with unknown authority cannot be presented as an authorized intervention. A linked before-and-after change is stronger than a mailbox but does not establish unlimited capacity. Keep the submitted objection, the reviewed finding, acceptance/rejection and actual change distinct.

**Affected future public families.** Channel, target, authority, permitted action, applicability, submission, review outcome, change linkage, time horizon and capacity evidence.

**Downstream consequences.** No global correction-effective flag from topology alone. No forced action on every objection. A reasoned rejection can demonstrate handling without proving the objection correct. Negative reachability is scoped to known graph coverage.

**Acceptance test for the decision.** The spec can distinguish a mailbox, an authorized rollback route, a successful specific rollback, a rejected invalid objection and an overloaded but nominally authorized review process.

**Approval record:** On 2026-09-16, the user accepted the Work Unit 2 package and all recommended directions in the immediately preceding handoff by replying “可以，继续”. This records Option B only in the scope above; it does not approve the new Work Unit 3 details, a final Phase 0 baseline or implementation. Historical Work Unit 1/2 records remain unchanged.

### SIT-D010: Metrics, denominators and concentration

**Status:** APPROVED DIRECTION; Option B accepted.  
**Gate:** Cleared for profile-first direction; no formula or weight is approved here, Work Unit 4 remains required.  
**Audit finding:** SIT-A010  
**Theory map:** SIT-T003, SIT-T017, SIT-T025, SIT-T031, SIT-T036, SIT-T037

**Question.** Should this source audit freeze numerical diagnostics now, or first require units, attribution and missing-data rules?

**Alternatives**

- **Option A.** Immediately define an aggregate integrity score and default root-weighted HHI.
- **Option B.** Require descriptive inventories and profiles first; permit a separately approved concentration or share metric only after its unit, weights, allocation, denominator and unknowns are defined in Work Unit 4.
- **Option C.** Prohibit all descriptive quantitative outputs permanently.

**Recommended option.** B. The existing v0.1 no-universal-score rule remains binding. Possible concentration metrics are explicitly toolkit operationalizations. Do not choose equal allocation among multiple roots, path-weighted ancestry or resolved-only normalization as a default in this work unit.

**Affected future public families.** Nominal counts, supported independence sets, origin contributions, derivative share, concentration, missingness, comparability and interpretation.

**Downstream consequences.** No high/low/extreme labels without an approved interpretation basis. An inverse concentration value, if ever approved, must not be called effective independent sample size. Results from different claim scopes or provenance coverage cannot be compared as if identical.

**Acceptance test for the decision.** A single accurate documentary source can produce a concentrated profile without a falsehood verdict, and a mixed-origin item with unknown attribution cannot receive silently fabricated weights.

**Approval record:** On 2026-09-16, the user accepted the Work Unit 2 package and all recommended directions in the immediately preceding handoff by replying “可以，继续”. This records Option B only in the scope above; it does not approve the new Work Unit 3 details, a final Phase 0 baseline or implementation. Historical Work Unit 1/2 records remain unchanged.

### SIT-D011: Layer and role classification

**Status:** APPROVED DIRECTION; Option B accepted.  
**Gate:** Cleared for separate-axis direction; exact classification payload is submitted in SIT-D019-SIT-D020.  
**Audit finding:** SIT-A011  
**Theory map:** SIT-T004-T007, SIT-T011, SIT-T032

**Question.** How should the three data layers and four governance layers be represented without inventing a credibility ladder?

**Alternatives**

- **Option A.** Merge all labels into a mutually exclusive ordered SourceType enum.
- **Option B.** Preserve the original source terminology and represent data roles, source-governance functions, verification scope and contestation on separate axes or nonexclusive role assertions.
- **Option C.** Omit SIL’s layer architecture from the product model.

**Recommended option.** B. Retain Surface-linguistic, World-model and Judgment as SIL’s data-layer terms. Retain Open Web, Verified, Contested and Judgment as its four governance-layer terms. HDL’s World structure and Judgment structure wording remains attributed to HDL. Final field names are a product decision.

**Affected future public families.** Data role, governance function, verification, contestation, judgment origin and human-review evidence.

**Downstream consequences.** One artifact can be verified as to origin and contested as to a claim. Judgment content can be human or model-generated, with the origin and corrective role separately assessed. No layer carries automatic truth or rank.

**Acceptance test for the decision.** A verified institutional statement about a disputed event retains verification scope, contested claim status and judgment origin simultaneously.

**Approval record:** On 2026-09-16, the user accepted the Work Unit 2 package and all recommended directions in the immediately preceding handoff by replying “可以，继续”. This records Option B only in the scope above; it does not approve the new Work Unit 3 details, a final Phase 0 baseline or implementation. Historical Work Unit 1/2 records remain unchanged.

### SIT-D012: Observability levels and per-capability prerequisites

**Status:** APPROVED DIRECTION; Option B accepted.  
**Gate:** Work Unit 6 must still define the exact capability matrix and report statuses.  
**Audit finding:** SIT-A012  
**Theory map:** SIT-T025, SIT-T030, SIT-T031, SIT-T038

**Question.** Does the plan’s proposed Level 0-4 structure gate every analysis, or summarize evidence availability while capabilities remain individually qualified?

**Alternatives**

- **Option A.** Use one cumulative level as both evidence coverage and overall source-integrity quality.
- **Option B.** Make the capability matrix authoritative. If levels remain, use them only as non-certifying coverage summaries that cannot override a field’s prerequisites.
- **Option C.** Omit all coverage and capability reporting.

**Recommended option.** B. A field with missing inputs remains unavailable even if a summary level is high. An independently observed correction can still be reported when root ancestry is incomplete. Exact labels and aggregation are deferred to Work Unit 6.

**Affected future public families.** Evidence availability, result eligibility, reasons for missing results, confidence/assurance limits and any level display.

**Downstream consequences.** High observability can expose poor integrity. No maturity badge or deployment certificate emerges from Level 4. Separate not observed, disputed, not applicable and not assessed where necessary.

**Acceptance test for the decision.** A dossier with proven correction to one output but unknown source ancestors reports both facts, rather than suppressing the correction or upgrading the ancestry.

**Approval record:** On 2026-09-16, the user accepted the Work Unit 2 package and all recommended directions in the immediately preceding handoff by replying “可以，继续”. This records Option B only in the scope above; it does not approve the new Work Unit 3 details, a final Phase 0 baseline or implementation. Historical Work Unit 1/2 records remain unchanged.

### SIT-D013: Tail, anomaly and contestation retention

**Status:** APPROVED DIRECTION; Option B accepted.  
**Gate:** Input context preservation is submitted here; denominators and threat rules remain Work Units 4-5.  
**Audit finding:** SIT-A013  
**Theory map:** SIT-T019, SIT-T021, SIT-T023, SIT-T029, SIT-T032

**Question.** What can the toolkit say about retained or suppressed evidence from an incomplete final bundle?

**Alternatives**

- **Option A.** Infer suppression whenever a final answer lacks disagreement, or count disagreement as reduced integrity.
- **Option B.** Preserve supplied anomalies and contested evidence with their context; measure retention only against a known intake or comparison set and recorded selection stages.
- **Option C.** Ignore anomaly and contestation records entirely.

**Recommended option.** B. A source’s disagreement with another is a claim-specific relation with epistemic type and provenance. An unclassified anomaly can remain unclassified long enough to challenge the current schema or rubric. A missing upstream universe is disclosed.

**Affected future public families.** Anomaly record, contested claim, original context, intake set, selection/exclusion record, stage history and denominator.

**Downstream consequences.** No inferred motive from omission alone. No automatic rarity, minority or tail classification from a source name. No equal weighting of every disputed claim as a consequence of preserving it.

**Acceptance test for the decision.** Two independent contradictory observations remain visible, and a final-only dossier cannot produce a whole-pipeline retention percentage without intake evidence.

**Approval record:** On 2026-09-16, the user accepted the Work Unit 2 package and all recommended directions in the immediately preceding handoff by replying “可以，继续”. This records Option B only in the scope above; it does not approve the new Work Unit 3 details, a final Phase 0 baseline or implementation. Historical Work Unit 1/2 records remain unchanged.

### SIT-D014: Protected identities, privacy and untrusted input

**Status:** APPROVED DIRECTION; Option B accepted.  
**Gate:** Identity/gap representation is submitted here; concrete security and export controls remain Work Unit 9.  
**Audit finding:** SIT-A014  
**Theory map:** SIT-T004, SIT-T008, SIT-T011, SIT-T013, SIT-T040

**Question.** How can a dossier preserve provenance without forcing public source disclosure or treating source content as instructions?

**Alternatives**

- **Option A.** Require public source names and external online identity verification for every origin.
- **Option B.** Use a local-first baseline with opaque identifiers, scoped attestations and explicit disclosure/assurance limits; treat all content as inert untrusted data and require separate authority for any future external action.
- **Option C.** Treat every undisclosed identity as independent because it cannot be compared.

**Recommended option.** B. Preserve known shared identities and relationships through redaction where authorized. A protected source need not reveal a name publicly, but an unsupported protected assertion cannot become verified provenance. Concrete security controls, storage limits and redaction procedures remain Work Unit 9 work.

**Affected future public families.** Identity disclosure, protected references, attestor, assurance basis, export scope, log content and input trust boundary.

**Downstream consequences.** No network access, code execution, embedded-instruction execution or automatic public disclosure can be authorized by input text. No cryptographic verification feature is implied by merely representing a signature field.

**Acceptance test for the decision.** Several redacted artifacts can remain linked to a common protected origin without publishing its identity. A hostile text excerpt cannot modify the analysis contract.

**Approval record:** On 2026-09-16, the user accepted the Work Unit 2 package and all recommended directions in the immediately preceding handoff by replying “可以，继续”. This records Option B only in the scope above; it does not approve the new Work Unit 3 details, a final Phase 0 baseline or implementation. Historical Work Unit 1/2 records remain unchanged.

### SIT-D015: Cross-project boundary and inherited governance

**Status:** APPROVED DIRECTION; Option B accepted.  
**Gate:** Separation is adopted; exact interchange, architecture and licensing remain later work.  
**Audit finding:** SIT-A015  
**Theory map:** SIT-T007, SIT-T040

**Question.** What is inherited from Recursive Integrity Toolkit, and what remains independently specified?

**Alternatives**

- **Option A.** Reuse its internal schema, algorithms, package and code license by default.
- **Option B.** Reuse only the controlled phase-governance pattern and relevant theoretical vocabulary. Keep separate product authority, specifications and runtime; permit later versioned artifact exchange after an explicit semantic mapping.
- **Option C.** Require completely different terms and prohibit any overlapping provenance method.

**Recommended option.** B. The responsibility list in the plan describes this toolkit’s focus and does not claim exclusive ownership of every lineage technique. Other toolkits can legitimately analyze provenance. No existing project file, dependency or approved scope is modified by this decision.

**Affected future public families.** Project identity, interchange boundary, version mapping, dependency strategy, licensing and governance.

**Downstream consequences.** No shared package, runtime import or automatic schema compatibility. No code-license selection is imported from another project. Exact interoperability and license choices remain Work Units 9-10.

**Acceptance test for the decision.** Source Integrity Toolkit can accept a self-contained dossier without installing Recursive Integrity Toolkit, and future artifact exchange cannot erase unknowns or assume field-name equivalence.

**Approval record:** On 2026-09-16, the user accepted the Work Unit 2 package and all recommended directions in the immediately preceding handoff by replying “可以，继续”. This records Option B only in the scope above; it does not approve the new Work Unit 3 details, a final Phase 0 baseline or implementation. Historical Work Unit 1/2 records remain unchanged.

## 4. Historical Work Unit 1 minimal approval sequence

The first product-definition step needs explicit choices for SIT-D001, SIT-D002 and SIT-D003. SIT-D015 also governs the separation between the new product and the existing toolkit. The recommended options for the full register are:

| Decision | Recommendation |
|---|---|
| SIT-D001 | B |
| SIT-D002 | C |
| SIT-D003-SIT-D015 | B |

Approving all recommendations together is permitted. Such approval adopts these design directions and does not freeze the exact schema, metrics, examples or module architecture. Those details are produced and reviewed in their designated work units.

If a recommendation is rejected, record the chosen alternative and its product consequences. If deferred, explicitly exclude or hold the affected capability; do not leave it implied as implemented.

## 5. Historical Work Unit 1 stop rules and change record

When a later step consumes an undecided meaning, pause that part of the specification and return the applicable decision to the Theory Owner. A later document may not convert a recommendation into approval merely by relying on it.

Revisions to a decision must preserve its prior disposition, source evidence, affected fields and downstream consequences. New issues receive new IDs rather than reusing an existing one for a different question.

| Date | Register event |
|---|---|
| 2026-09-16 | Revision 0.1 created in Work Unit 1; all 15 recommendations await explicit acceptance |

This Work Unit 1 package stops before product specification, ontology, metrics or implementation. `PHASE_0_APPROVAL.md` is not created.

### 5.1 Original Work Unit 1 artifact identity

This register first formed the Work Unit 1 package together with `SPEC_AUDIT.md` and `THEORY_SOURCE_MAP.md`. Both relative links resolve when the working specification folder is assembled. The original three-file archive remains historical; the active decision record is this revision 0.4, subject to its recorded approval scope.


## 6. Historical Work Unit 2 extension

The original fifteen decision bodies above preserve their Work Unit 1 recommendations and then-current no-approval records. That history is intentionally retained. The latest instruction to continue authorizes a proposed Work Unit 2 package, while explicit acceptance of the directions remains unrecorded.

Work Unit 2 adds three product choices that the original register intentionally left to this unit: the accepted input surface, minimum usable-release capability boundary, and reporting/interface surfaces. Their detailed data structures, metric formulas and command/function names remain later-unit work.

### SIT-D016: Canonical input format and local entry surface

**Status:** APPROVED DIRECTION; Option B accepted.  
**Gate:** Format direction cleared; exact logical envelope and rejection behavior are submitted in SIT-D021.  
**Basis:** PLAN §9 requirements 3 and 11; SIT-D003, SIT-D006-SIT-D007, SIT-D014; SIT-P001-SIT-P003, SIT-P014.

**Question.** Which input surface should v0.1 support without adding extraction and mapping systems before the ontology is stable?

**Alternatives**

- **Option A.** Direct support for PDF, HTML, URLs, arbitrary CSV/JSON Lines and raw prose, including automatic relationship extraction.
- **Option B.** One canonical, versioned UTF-8 JSON bundle read from an explicitly selected local file; an in-process library accepts the same logical payload. Supporting text and locators remain supplied evidence and inert references.
- **Option C.** Database-specific or network-service-specific input requiring a hosted registry or source resolver.

**Recommended option.** B. It provides a transport for a heterogeneous, scoped record graph without introducing a separate extraction or inference product. Caller-created exports can be accepted if they meet the eventual canonical contract and preserve their extraction/inference provenance.

**Affected future public families.** Bundle identity and version, inquiry scope, typed records, assertion evidence, reference resolution, structural errors and input provenance.

**Downstream consequences.** Work Unit 3 specifies the logical object model and reference contract. Executable schemas belong to a later authorized phase. Exact Python input types and file-size/encoding limits remain architecture and security decisions. URLs and predecessor references cannot trigger automatic network or filesystem reads.

**Acceptance test for the decision.** A locally supplied dossier can be audited without extra services. A locator-only upstream document remains uninspected, and a malformed canonical record cannot be silently repaired by an LLM.

**Approval record:** On 2026-09-16, the user accepted the Work Unit 2 package and all recommended directions in the immediately preceding handoff by replying “可以，继续”. This records Option B only in the scope above; it does not approve the new Work Unit 3 details, a final Phase 0 baseline or implementation. Historical Work Unit 1/2 records remain unchanged.

### SIT-D017: Required analytical slice and optional numerical diagnostics

**Status:** APPROVED DIRECTION; Option B accepted.  
**Gate:** Required-slice direction cleared; numerical selection remains Work Unit 4.  
**Basis:** PLAN §§3, 9 and 11; SIT-D003-SIT-D010, SIT-D012-SIT-D013; SIT-P001-SIT-P016.

**Question.** What must make v0.1 an actual source-structure auditor while preventing a premature score engine?

**Alternatives**

- **Option A.** Make every candidate scalar and level mandatory immediately, including a root-weighted concentration value and generic presence strength.
- **Option B.** Require claim-scoped inventories, permitted origin/common-ancestry and cycle analysis, qualified independence and unknowns, contribution profiles, evaluator overlap, staged presence, correction evidence and anomaly/context preservation. Include numeric concentration/share summaries only when Work Unit 4 explicitly approves their semantics and release status.
- **Option C.** Release only a source checklist or raw graph viewer, with no origin or correction analysis.

**Recommended option.** B. Every included analysis must yield either an evidence-supported result or a reason it cannot be performed on that input. This does not make unsupported data mandatory. It requires the capability and its honest non-result behavior, rather than a fabricated number.

**Affected future public families.** Product requirement catalog SIT-P001-SIT-P016; origin and comparison sets; contribution and uncertainty profiles; evaluator roles; presence stages; correction records; report capability matrix.

**Downstream consequences.** Optional numeric diagnostics are distinguishable from included analyses whose prerequisites are unmet. No silent default root allocation, high/low label, effective independent sample size or universal score is selected. A later phase must either specify a required field or explicitly revise its scope before implementation.

**Acceptance test for the decision.** v0.1 can expose five artifacts sharing one documented origin and a correction that reaches only some targets, while an incomplete dossier still produces a bounded inventory and explicit unavailable analyses.

**Approval record:** On 2026-09-16, the user accepted the Work Unit 2 package and all recommended directions in the immediately preceding handoff by replying “可以，继续”. This records Option B only in the scope above; it does not approve the new Work Unit 3 details, a final Phase 0 baseline or implementation. Historical Work Unit 1/2 records remain unchanged.

### SIT-D018: Interface surfaces and equivalent reports

**Status:** APPROVED DIRECTION; Option B accepted.  
**Gate:** Interface/report direction cleared; command names, API signatures and result envelope remain later work.  
**Basis:** PLAN §9 requirements 9 and 13; SIT-D012, SIT-D014-SIT-D015; SIT-P012-SIT-P016.

**Question.** How should the usable toolkit be invoked and how should findings be delivered without creating a hosted platform?

**Alternatives**

- **Option A.** Hosted web interface, source dashboard, remote model narration and an operational trust service.
- **Option B.** A local CLI and a local Python library over one result contract, with required JSON and Markdown reports. Exact entry-point names, signatures, package layout and output-state schemas remain later specifications.
- **Option C.** One human-readable report only, with no machine-readable evidence trail.

**Recommended option.** B. Programmatic use and human inspection should expose the same substantive assertions, unknowns, basis and limitations. Narration can be deterministic and rule-bound; a generative model is unnecessary.

**Affected future public families.** Result identity, scope, input reference, run metadata, capability matrix, evidence/witness references, report sections and deterministic presentation.

**Downstream consequences.** HTML, dashboards, hosted services and model-based narration remain outside v0.1. Volatile run metadata is separated from substantive results. Report writing requires an explicit local destination and cannot silently overwrite source inputs. License and packaging choices are not selected by this decision.

**Acceptance test for the decision.** JSON and Markdown cannot disagree about whether independence was demonstrated, merely asserted or unobservable. Reordering equivalent input assertions cannot change substantive results under a fixed approved contract.

**Approval record:** On 2026-09-16, the user accepted the Work Unit 2 package and all recommended directions in the immediately preceding handoff by replying “可以，继续”. This records Option B only in the scope above; it does not approve the new Work Unit 3 details, a final Phase 0 baseline or implementation. Historical Work Unit 1/2 records remain unchanged.

### Historical Work Unit 2 realization map and unresolved consumers

This table records where Work Unit 2 uses each recommended direction. A reference is traceability, not proof that the direction was approved.

| Decision | Work Unit 2 consumer | Detailed consumer still to be written |
|---|---|---|
| SIT-D001 | Product §§2.1, 10.1; instructions §4.7 | Work Unit 4 names only quantities with approved semantics |
| SIT-D002 | Product §§2.2, 7.4; instructions §4.4 | Work Unit 3 judgment, evaluator and validation records |
| SIT-D003 | Product §§1, 3, 5-6, 11 | Work Unit 3 canonical input and graph contract |
| SIT-D004 | Product §§4-5, 7.2 | Work Unit 3 ontology, versions and claim contributions |
| SIT-D005 | Product §§6-7.2, 7.4 | Work Unit 3 evidence standard; Work Unit 4 any count rules |
| SIT-D006 | Product §§5.3-5.4, 7.2-7.3, 8.2 | Work Unit 3 unresolved endpoint model; Work Unit 4 denominators |
| SIT-D007 | Product §§5-6, 8; instructions §4.2 | Work Unit 3 relation registry, conflict and rejection rules |
| SIT-D008 | Product §7.5 | Work Units 3-4 stages, time and effect semantics |
| SIT-D009 | Product §7.5 | Work Units 3-4 channel/authority/event/target model |
| SIT-D010 | Product §§7.3, 10.3 | Work Unit 4 metric definition or explicit deferral |
| SIT-D011 | Product §2.3 | Work Unit 3 independent role axes |
| SIT-D012 | Product §§7.1, 8.2 | Work Unit 6 authoritative per-capability matrix |
| SIT-D013 | Product §7.6 | Work Units 3-4 context and intake/stage records |
| SIT-D014 | Product §§5.4, 11; instructions §6.2 | Work Unit 9 concrete privacy, retention, resource and write controls |
| SIT-D015 | Product §11; instructions §6.3 | Work Units 9-10 license, interchange and dependency decisions |
| SIT-D016 | Product §5.1 | Work Unit 3 logical bundle; later executable schema |
| SIT-D017 | Product §7 and requirement catalog | Work Unit 4 numerical boundaries and Work Unit 8 trace/test ownership |
| SIT-D018 | Product §8 | Work Unit 6 report schema; Work Unit 10 interface and architecture |

### Historical Work Unit 2 review request and gates

The submitted package recommends **B for SIT-D001, C for SIT-D002, and B for SIT-D003-SIT-D018**. A single explicit acceptance may approve the package and all enumerated directions together. That action would not freeze numerical formulas, object fields, relation names, command signatures or module paths before their designated work units.

This revision records **no such new approval event**. The current continuation instruction permitted the proposed Work Unit 2 package to be drafted. Product adoption remains held until the relevant directions and Work Unit 2 choices are accepted. An owner may instead select alternatives or request a narrower proposal.

The next planned production unit is Work Unit 3, restricted to `DEFINITIONS_AND_UNITS.md`, `CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` and an authorized update of this register. It is not executed in this delivery. No `PHASE_0_APPROVAL.md` or Phase 1 plan is created.

### Historical Work Unit 2 revision history

| Date | Register event | Approval consequence |
|---|---|---|
| 2026-09-16 | Revision 0.1 delivered in Work Unit 1 | Fifteen recommended directions submitted |
| 2026-09-16 | Revision 0.2 created in Work Unit 2 | Prior records preserved; SIT-D016-SIT-D018 added; no new approval claimed |

Revision 0.2 is the active proposed successor to revision 0.1. The Work Unit 1 files and archive remain unchanged. The Work Unit 2 archive contains only `V0.1_PRODUCT_SPEC.md`, `PROJECT_INSTRUCTIONS.md` and this updated register. Relative links to the source audit/map are intended to resolve in the assembled specification folder.


## 7. Work Unit 3 detailed design choices

The Work Unit 2 handoff requested approval of the current files and all recommended directions before Work Unit 3. The user replied “可以，继续”. This revision records that approval contextually for SIT-D001-SIT-D018. The selected options are B for SIT-D001, C for SIT-D002 and B for SIT-D003-SIT-D018.

That acceptance chooses the directions. It does not retroactively make the previous submissions approved at their creation date. Their original files remain unchanged. The new detailed choices below are submitted now and require review. They do not introduce code, schema files, metrics, final report levels or implementation authority.

### SIT-D019: Canonical objects, origins, evaluative roles and correction records

**Status:** APPROVED; Option B accepted in the current WU5 intake.  
**Gate:** Cleared for the submitted WU3 definition/input realization and its stated limits; no new implementation authority.  
**Basis:** SIT-D002, SIT-D004, SIT-D008-SIT-D009, SIT-D011, SIT-D013-SIT-D014; SIT-P001-SIT-P011, SIT-P014; SIT-T005-SIT-T008, SIT-T011, SIT-T020-SIT-T024, SIT-T029, SIT-T032, SIT-T035-SIT-T039.

**Question.** Which concrete record model realizes the accepted source/claim/origin distinctions without multiplying interchangeable classes?

**Alternatives**

- **Option A.** One general Source node with type, confidence, independent and correction-effective flags.
- **Option B.** Twelve core record kinds: Claim, Artifact, SourceActor, EvidenceItem, OriginEvent, Model, Evaluation, CorrectionChannel, CorrectionEvent, PipelineRecord, Anomaly and UnresolvedReference. Inquiry, Assertion and EvidenceReference remain separate top-level collections. Roles and source vocabularies are preserved through typed links and classification assessments.
- **Option C.** A distinct class for every candidate term, including Publisher, Observation, Dataset, Benchmark, Judgment, ValidationEvent, Transformation and RootSource, with independently maintained identity and parent fields.

**Recommended option.** B as specified in `DEFINITIONS_AND_UNITS.md` §§3-7 and `CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` §§5-6. Observation is an OriginEvent kind; publisher is an actor role; dataset, benchmark, rubric and judgment are Artifact kinds; validation is an Evaluation process; root is a scoped analytical role. Correction submission, handling and change are separate variants linked to a case. PipelineRecord preserves each replenishment stage independently. Anomaly preserves context without mandatory binding to an existing Claim.

The logical roles that define what an Evaluation did are part of its `role_bindings`; there is no second competing `judged_by` parent list. Output/input Artifact metadata and acquisition OriginEvent mappings do not silently derive claim-specific ancestry. Controlled values and concrete fields are the submitted specification, not source-paper formulas.

**Affected future public families.** Core object identities, Claim/Artifact versioning, evidence contributions, typed origins, model and evaluator roles, human contributions, correction channels/cases, stage observations, anomalies and protected references.

**Downstream consequences.** Work Unit 4 uses these objects without inventing a global independent-source property. Work Unit 6 can report different evidence availability by capability. Work Unit 9 must refine export protection without requiring public identities. Adding operational record kinds later requires an explicit versioned contract change.

**Acceptance tests for the decision.** The sixteen representation witnesses in the lineage specification cover mixed artifacts, two data acquisitions, shared-data analyses, synthetic generation, independent human review with unknown dependencies, separate stage logs, partial correction and unclassified anomalies. One case acceptance does not establish runtime behavior.

**Scope of approval requested.** Adopt the exact proposed twelve-kind model and supporting record fields for Phase 0 specification purposes, including the source vocabulary separation. Numerical diagnostics, final report schemas and implementation are excluded.

**Approval record:** On 2026-09-17, following the WU4 handoff's explicit offer to approve SIT-D019-SIT-D025 and proceed to WU5, the user replied “可以，继续”. This accepts Option B and the named WU3 model/field contract only within the scope above. No runtime schema, metric beyond the separately accepted analytical package, Phase 0 completion or implementation is authorized. **Previous record retained:** No acceptance of this new detailed choice has yet been recorded. Submitted in Work Unit 3.

### SIT-D020: Evidence-bearing relation/assessment registry and conservative views

**Status:** APPROVED; Option B accepted in the current WU5 intake.  
**Gate:** Cleared for the submitted typed graph/evidence semantics; later threat/status work must preserve them.  
**Basis:** SIT-D005-SIT-D007, SIT-D009, SIT-D011-SIT-D012; SIT-P002-SIT-P006, SIT-P008-SIT-P012; SIT-T008, SIT-T018, SIT-T020, SIT-T022, SIT-T026, SIT-T035-SIT-T039.

**Question.** What makes a graph path or independence assertion interpretable enough for deterministic local analysis?

**Alternatives**

- **Option A.** Treat all edges as verified facts and traverse every edge to a parentless node; classify disconnected components as independent.
- **Option B.** Adopt the explicit 24-predicate registry and nine assessment kinds, full assertion provenance, five dependency dimensions, exact typed views and evidence-qualified comparison sets. Preserve conflicts, unknowns and source labels. Require a scoped origin-boundary assessment rather than a parentless-node default.
- **Option C.** Infer edge meanings, identity, authority and independence automatically from free text using an LLM.

**Recommended option.** B as specified in definitions §§6-14 and lineage specification §§3-4, 7-12. Relation endpoints, mandatory dimension and permitted structural links determine each view. Citation, material transformation, claim contribution, model ancestry, organizational control and correction routes remain separate.

The exact nine assessment kinds are `origin_boundary`, `independence`, `coverage`, `externality`, `authorization`, `verification`, `capacity`, `classification` and `conflict`. Their enum labels remain caller assertions. Documentary support requires an inspectable supplied basis or a scoped protected attestation; metadata labels alone do not verify a claim.

An independence result concerns one explicitly listed pair or set, one dependency dimension, a Claim scope, a method and supporting evidence. It cannot be transitively united into a larger set. Known unresolved identities or contrary dependencies remain constraints. The input retains unresolved frontiers without converting them into root cardinality. Multi-parent relationships have no default allocation.

Positive traversal uses structurally valid, affirmed, active and scope-compatible relations. Disputed possibilities remain visible but cannot yield uncontested completeness. Record-specific source times, assertion times and version identities are retained. Inert method strings, free text and extension metadata have no executable semantics.

**Affected future public families.** Assertion provenance and evidence references; typed links and views; origin qualification; independence comparison; coverage; externality; authority and verification; source-function axes; capacity limits; conflict, denial and supersession behavior.

**Downstream consequences.** The local tool may find a recorded path without claiming its premises true in the world. A qualified process assessment remains attributed. No exact confidence score, generalized common-ancestor algorithm, semantic contradiction checker or legal-authority certification follows from this design.

**Acceptance tests for the decision.** Citation-only chains cannot produce claim-origin results. Known multi-parent branches survive intact. Unknown frontiers cannot improve independence. Pairwise claims cannot form a joint independent total. A granted amend action cannot become a granted withdraw action. Conflicting ownership, origin and verification records remain scoped to their affected view.

**Scope of approval requested.** Adopt the concrete registry, assessment payloads, provenance/qualification conditions and view rules as the Phase 0 input semantics. Work Unit 4 still defines formulas, count units and numerically eligible populations; Work Unit 6 defines final report states and levels.

**Approval record:** On 2026-09-17, the same contextual acceptance of the enumerated SIT-D019-SIT-D025 package selects Option B for this detailed typed-relation, assessment and view contract. Its documentary/attribution limits remain mandatory; approval does not authenticate outside facts or pre-approve new threat findings. **Previous record retained:** No acceptance of this new detailed choice has yet been recorded. Submitted in Work Unit 3.

### SIT-D021: Immutable snapshot bundle, references and structural input handling

**Status:** APPROVED; Option B accepted in the current WU5 intake.  
**Gate:** Cleared for the logical input contract and rejection boundary; concrete implementations remain prohibited.  
**Basis:** SIT-D003, SIT-D006-SIT-D007, SIT-D014-SIT-D018; SIT-P001-SIT-P003, SIT-P006, SIT-P012-SIT-P016; SIT-T008, SIT-T022, SIT-T026, SIT-T040.

**Question.** How should the versioned local JSON bundle preserve sparse evidence while rejecting accidental corruption and preventing implicit external actions?

**Alternatives**

- **Option A.** Guess missing endpoints, coerce unknown values, load predecessor files and fetch URLs as needed, then analyze any salvageable rows.
- **Option B.** Adopt `sit-bundle/0.1` as the documented logical contract: one immutable snapshot, globally unique local IDs, typed references, closed core keys and namespaced inert extensions; explicit unresolved objects for known gaps; one bounded structural rejection policy with no silent salvage.
- **Option C.** Accept only perfectly complete dossiers with publicly verified source identities.

**Recommended option.** B as specified in lineage §§2-4 and §13-14. The root has the explicit bundle/inquiry/record/assertion/evidence collections and version metadata. References resolve within that snapshot. A predecessor link is descriptive and does not import data. Local and external evidence locators remain inert; the only runtime evidence payload read under this contract is the user-selected bundle. Supplied excerpts are carried inside it. Protected references remain possible.

Malformed JSON, duplicate keys/IDs, dangling typed references, prohibited endpoint combinations, unsupported core vocabulary, incompatible Claim bindings and structurally incomplete event variants reject the bundle for normal analytical processing. A validation-diagnostic result may be produced under the later reporting contract; no ordinary analytical audit of a silently reduced subset is allowed.

Valid sparse provenance, locator-only support, protected identities, unexamined dimensions, disputes, cycles and missing times remain representable with their exact analytical limits. No filename, URI, embedded instruction, method description or extension grants read, write, network, code-execution or source-modification authority.

**Affected future public families.** Logical bundle version and keys, ID/reference identity, null/gap distinction, source times, assertions and evidence locators, extension policy, structural rejection and unknown preservation.

**Downstream consequences.** Future file and in-process adapters must share this meaning. Work Unit 9 still selects concrete byte/record/depth limits, privacy/export controls and safe destination rules. Work Unit 10 selects actual API names, canonical serialization and package/dependency layout. There is no implemented parser, schema file or CLI in this delivery.

**Acceptance tests for the decision.** An explicit unresolved artifact endpoint is valid where permitted; an undeclared Artifact ID is rejected. A URL-only citation stays uninspected. A removed target requires explicit absence evidence, while an unknown after-state uses an unresolved endpoint. Unknown contract versions fail closed rather than being inferred from column names.

**Scope of approval requested.** Adopt the proposed logical version/fields, reference identity, extension rule and structural rejection behavior. No runtime schema or implementation phase is authorized.

**Approval record:** On 2026-09-17, the same contextual acceptance selects Option B for `sit-bundle/0.1`, references and structural handling as documented in WU3. Numeric/resource limits, canonical serialized bytes, parser code and external actions are not included. **Previous record retained:** No acceptance of this new detailed choice has yet been recorded. Submitted in Work Unit 3.

## 8. Work Unit 3 realization and remaining consumer gates

| Accepted direction | Work Unit 3 realization | Remaining gate |
|---|---|---|
| SIT-D001 | Source-local quantities retained in definitions §2 | WU4 must continue to avoid generic entropy or collapse values |
| SIT-D002 | Artifact/Evaluation origin and human contribution distinctions; source-role axes | SIT-D019/SIT-D020 review; WU4/WU6 reporting details |
| SIT-D003 | Local caller-prepared bundle and inert external references | SIT-D021 review; WU9 concrete safety limits |
| SIT-D004 | Twelve records, EvidenceItem Claim binding, OriginEvent kinds | SIT-D019 review |
| SIT-D005 | Supplied pair/set process assessments and five dimensions | SIT-D020 review; WU4 count rules |
| SIT-D006 | Explicit gap/reference states and unqualified terminal boundaries | SIT-D020/SIT-D021 review; WU4 numerical unknowns |
| SIT-D007 | Full assertion envelope, typed links, lifecycle and conflict retention | SIT-D020/SIT-D021 review |
| SIT-D008 | Externality assessment and four independent PipelineRecord stages | WU4 presence profiles; WU6 output eligibility |
| SIT-D009 | Channel, authorization assessment, submission/handling/change records | SIT-D019/SIT-D020 review; WU4 route/output meanings |
| SIT-D010 | No metric or default allocation introduced | WU4 remains the numerical gate |
| SIT-D011 | Source-local role/governance axes through classifications | SIT-D019/SIT-D020 review |
| SIT-D012 | Input prerequisites and limitation states only | WU6 final capability matrix and report vocabulary |
| SIT-D013 | Anomaly with optional existing-Claim binding; stage-universe coverage | WU4 denominators; WU5 threat claims |
| SIT-D014 | Opaque identities, protected references, no implicit read/action | WU9 concrete privacy, export, storage and resource controls |
| SIT-D015 | No runtime/schema/license inheritance | WU9 license; WU10 interchange and architecture |
| SIT-D016 | Documented logical `sit-bundle/0.1` | SIT-D021 review; no executable schema |
| SIT-D017 | Records support the required structural slice without score fields | WU4 quantitative selection; WU8 test/Trace ownership |
| SIT-D018 | Shared logical file/library payload and preserved source scope | WU6 report envelope; WU10 names/interfaces |

The three new detailed decisions are one reviewable package. One explicit acceptance may select their Option B recommendations and the two submitted definition documents together. It does not automatically accept later numerical, report, architecture or implementation choices.

## 9. Historical Work Unit 3 review request and next action

Historical WU3 register state: SIT-D001-SIT-D018 are accepted in their stated scopes. SIT-D019-SIT-D021 remain proposed. The next step after adoption of this unit is Work Unit 4, with an allowlist of `DEFINITIONS_AND_UNITS.md`, `OBSERVABILITY_AND_REPORTING.md`, `V0.1_PRODUCT_SPEC.md` and this register. The work must remain documentation-only.

The active WU3 snapshot contains the original alternatives and recommendations for all previous decisions. It changes only their current disposition and approval record, preserves the old explanatory handoffs as history, and adds the three new choices. The Work Unit 1 and 2 files and ZIP archives remain untouched. The historical revision 0.1 content remains in its original archive and is not erased by a later approval event.

No `PHASE_0_APPROVAL.md`, Phase 1 plan, runtime schema, package, metric function, graph algorithm, detector, CI workflow or GitHub write is authorized here.

## 10. Historical Work Unit 3 revision history

| Date | Event | Approval consequence |
|---|---|---|
| 2026-09-16 | User accepts Work Unit 2 package and all recommended directions by “可以，继续” | SIT-D001 Option B, SIT-D002 Option C, SIT-D003-SIT-D018 Option B accepted for their enumerated scope |
| 2026-09-16 | Revision 0.3 created in Work Unit 3 | Current dispositions updated; original decision bodies preserved; SIT-D019-SIT-D021 submitted |

This was the active Work Unit 3 register snapshot. The later revision 0.4 controls the current proposed state, while preserving this history. The WU3 three-file package includes two new specification files and this register revision. No previous file or source is changed in place.


## 11. Work Unit 4 conditional intake and detailed choices

The Work Unit 3 handoff identified SIT-D019-SIT-D021 as new detailed choices. The latest user message is “继续”. This revision records authorization to prepare the next controlled proposal, without inventing explicit acceptance of those detailed choices. The WU4 specifications therefore state their conditional dependence on the submitted WU3 model.

The eighteen accepted directions remain unchanged. In the WU4 intake, no original alternative, recommendation or approval event was changed. The three pending WU3 options and four analytical choices below form the historical WU4 review set. Their later acceptance is recorded in the current approval table and individual records. Historical sections above retain their earlier status statements as history; the current index and approval records control the working disposition.

### SIT-D022: Explicit analytical populations and qualified supplied-set counts

**Status:** APPROVED; Option B accepted in the current WU5 intake.  
**Gate:** Cleared for WU4's population/count contract; later consumers must keep its explicit units and scope.  
**Basis:** SIT-D004-SIT-D007, SIT-D016-SIT-D017; SIT-P001-SIT-P007; SIT-T020, SIT-T022, SIT-T035-SIT-T036.

**Question.** What is counted when a dossier contains several claims, several contributions per artifact, context-only sources and supplied independence assessments?

**Alternatives**

- **Option A.** Count every artifact, ancestor, publisher and comparison member as part of one global source total.
- **Option B.** Fix inventory populations to explicit seed positions and claim-bound EvidenceItems; keep ancestor/support records separate. Count each qualified supplied comparison set independently, without unioning pairs or discovering a maximal independent set.
- **Option C.** Require the user to provide every final count, leaving the toolkit no deterministic inventory responsibility.

**Recommended option.** B as specified in definitions §§20-21 and reporting §2. `E(I,C)` contains explicit seed EvidenceItems for that Claim; inquiry and claim artifact inventories use their own defined source positions. Context-only and ancestor records are not silently added. Claim-unassigned seed artifacts remain disclosed.

Origin records, documentary origin boundaries, frontier references, comparison subjects and artifact versions remain different units. `qualified_process_set_member_count` concerns one evidence-bearing assessment. `qualified_origin_set_member_count` further requires documentary-qualified origin boundaries within that same assessment and dimension. No transitive union, global independent-source count, singleton independence certificate or statistical effective sample size is produced.

**Affected public families.** SIT-M001-SIT-M003, exact populations/IDs, unassigned-artifact disclosure, root/boundary qualification and non-result reasons.

**Acceptance conditions.** Several paths or assessments about O1 do not multiply O1. Two independent pair assessments do not become a three-member joint set. One artifact with several contributions remains one artifact and several contribution units. An unsupported independence assessment keeps its submitted member count while its qualified count is unavailable.

**Scope of approval requested.** Adopt the exact seed-counting and supplied-set qualification rules in the named WU4 sections. This does not approve a field's final JSON layout, graph implementation or unseen-world total.

**Approval record:** On 2026-09-17, following the WU4 handoff's offer to accept SIT-D019-SIT-D025, the user replied “可以，继续”. This accepts Option B and the specified populations/qualified-count rules. It does not certify the truth of supplied independence assessments or authorize implementation. **Previous record retained:** No acceptance of this new decision has been recorded. Submitted in Work Unit 4.

### SIT-D023: Origin incidence, restricted concentration and inheritance without invented allocation

**Status:** APPROVED; Option B accepted in the current WU5 intake.  
**Gate:** Cleared for the exact WU4 numerical/attribution boundary; no broader concentration instrument is implied.  
**Basis:** SIT-D005-SIT-D007, SIT-D010, SIT-D017, pending SIT-D019-SIT-D021; SIT-P004-SIT-P007, SIT-P016; SIT-T017, SIT-T036-SIT-T037.

**Question.** How can the release describe concentration and derivative contribution when one seed has several origins or an unresolved branch?

**Alternatives**

- **Option A.** Split each multi-parent item equally, normalize only known ancestry, and output HHI plus an effective independent-root count.
- **Option B.** Require a nonexclusive origin-incidence/disposition profile; use no operational multi-parent allocation in v0.1. Add one supplementary HHI only for an entirely documentary-qualified single-origin seed population. Keep derivative contribution as a narrow immediate-EvidenceItem-layer profile.
- **Option C.** Remove all concentration and inherited-contribution analysis from v0.1.

**Recommended option.** B as specified in definitions §§22-24 and product §§7.3,15. Known origin membership is counted at most once per seed/origin; multiple membership fractions may exceed one in sum and are labeled nonexclusive. The five exhaustive row dispositions retain unknown, baseline, declared, multi-origin and single-origin cases in N.

`single_origin_contribution_hhi = sum((n_r/N)^2)` is eligible only when every seed resolves completely to exactly one documentary-qualified origin in the same claim/dimension, with the required coverage/identity/time qualifications. One seed is one **contribution-count unit**, not an evidentiary strength weight. Any mixed, unresolved, disputed or baseline row blocks the scalar for the whole population; the profile remains available. No same-identity merger or narrative percentage is parsed into a weighting rule.

The immediate-layer inheritance profile has direct-only, inherited-only, mixed and unresolved categories. Its point fraction is available only without unresolved immediate classifications; a labeled finite-record completion interval [D/N,(D+U)/N] can preserve unresolved members. This does not measure semantic novelty, new acquisition or truth. The interval is not a statistical confidence interval.

General weighted multi-parent HHI, partial-provenance concentration bounds, reciprocal/effective-root count, effective independent sample size and high/low/extreme bands are explicitly outside the proposed v0.1 contract. The existing input model has no approved structured numerical allocation record; adding one is a future schema change.

**Affected public families.** SIT-M004-SIT-M007; origin-incidence counts and sets; seed dispositions; resolution coverage; restricted HHI; first-step inheritance; frontiers and exact denominators.

**Acceptance conditions.** Five O1 seeds plus one O2 seed can yield HHI 26/36 for their explicitly defined complete count population. Adding a seventh unknown seed makes HHI unavailable for the new full population. A known two-parent seed is distinguished from an unknown-parent seed; neither gets equal allocation by default. A citation path alone does not establish inherited acquisition.

**Scope of approval requested.** Adopt the submitted profile, exact scalar eligibility/formula and exclusions. This selects the supplementary HHI capability for the proposed release; it does not certify its premises or make any universal integrity claim.

**Approval record:** On 2026-09-17, the same contextual acceptance selects Option B, including restricted HHI and its complete-population prerequisites, incidence without allocation, inherited-layer classification and the explicit exclusions. The approval is bounded to the WU4 operationalization and adds no truth, independence or failure score. **Previous record retained:** No acceptance of this new decision has been recorded. Submitted in Work Unit 4.

### SIT-D024: Evidence-specific evaluator, presence, correction and retention profiles

**Status:** APPROVED; Option B accepted in the current WU5 intake.  
**Gate:** Cleared for WU4's profile/cohort/correction semantics; WU5/WU6 may not collapse their separate evidence layers.  
**Basis:** SIT-D002, SIT-D008-SIT-D009, SIT-D012-SIT-D013; SIT-P008-SIT-P012; SIT-T005, SIT-T018, SIT-T020-SIT-T024, SIT-T029, SIT-T034, SIT-T039.

**Question.** Which descriptive values can be supported without turning role overlap into error correlation, stage logs into adequate Presence, or route existence into successful correction?

**Alternatives**

- **Option A.** Generate one percentage each for evaluator independence, effective presence, tail retention and correction success from available rows.
- **Option B.** Preserve separate evidence-bearing profiles and add finite-member fractions only under explicit cohort, stage, support and time prerequisites. Count correction cases, handling records and linked target changes as different units.
- **Option C.** Exclude evaluator, presence, correction and tail analysis until every external process can be independently verified.

**Recommended option.** B as specified in definitions §§25-27. Shared evaluator ancestors, exact role identity, family labels, dataset granularity and unexamined dimensions remain distinct. Externality assessments retain their boundary/time basis and cannot be inferred from dates or authorship labels.

A stage fraction requires one evidence-bearing `pipeline_universe` coverage assessment anchored to an unambiguous PipelineRecord key, with a complete resolved EvidenceItem/Anomaly population. The member partition Y/F/U preserves conflicting, unsupported and missing observations. The point is unavailable if U>0, while the labeled completion interval may be reported. No rate drops unknown members. A retention/selection transition additionally needs a unique compatible fully evidenced admission baseline with the same member IDs; general inferred mappings and multiplied funnels are excluded.

Correction profiles retain channel/route, action/target/time authority, case handling, explicit before/after linkage and attributed capacity. Missing authority does not erase a documentary historical change. Accepted/rejected handling and unknown downstream targets remain separate. No correction-success rate, causal elasticity or capacity-adequacy number is selected. Human contribution requires its own record/evidence and is not inferred from a reviewer label.

**Affected public families.** SIT-M008-SIT-M014; exact role-pair witnesses; stage/cohort IDs and ratios; independent process/human contribution; case/event/target counts; anomaly context and retention eligibility.

**Acceptance conditions.** A six-member cohort with four evidenced occurrences, one negative and one unknown has no point rate and may show [4/6,5/6]. Two target changes and one missing target remain exactly that, not two successes and one failure. Matching model-family strings cannot establish shared training history or independence. A final-only list cannot establish tail suppression.

**Scope of approval requested.** Adopt the submitted finite evidence/cohort eligibility and profile meanings. It does not add structured capacity numerics, causal experiments, arbitrary stage mapping or an active correction service.

**Approval record:** On 2026-09-17, the same contextual acceptance selects Option B and its explicit finite-cohort, role, route, handling, human-contribution and linked-outcome rules. It does not authorize live monitoring, causal experiments, new source verification or correction actions. **Previous record retained:** No acceptance of this new decision has been recorded. Submitted in Work Unit 4.

### SIT-D025: Non-results, precision, comparison and supplementary scalar status

**Status:** APPROVED; Option B accepted in the current WU5 intake.  
**Gate:** Cleared for analytical non-result/precision/comparison meaning; WU6 still owns final serialized states.  
**Basis:** SIT-D006, SIT-D010, SIT-D012, SIT-D017-SIT-D018; SIT-P001, SIT-P006-SIT-P007, SIT-P012-SIT-P016; SIT-T022, SIT-T025, SIT-T031, SIT-T037-SIT-T040.

**Question.** How should a future result preserve exact units and missingness without prematurely defining the WU6 report schema?

**Alternatives**

- **Option A.** Fill unavailable values with zero, use floating-point scores, compare different scopes by default, and let optional modules silently disappear.
- **Option B.** Use exact finite counts/ratios and explicit non-result reasons; retain numerator/denominator and qualifications; define comparability; require each selected diagnostic to return a supported result or its unmet prerequisites. Leave final machine status enums/nesting to WU6.
- **Option C.** Produce prose only, with no stable analytical field catalog or exact arithmetic requirements.

**Recommended option.** B as specified in definitions §28 and reporting §§2-8. Exact empty inventories can be zero; unobservable qualified counts and zero-denominator ratios remain unavailable/null with reason. Multiroot-unallocated, unknown-history, disputed premise, missing cohort, inapplicable and unperformed are different non-result meanings.

Preserve integer counts and exact rational values, including the HHI numerator `sum(n_r^2)` and `N^2`. Optional decimal display rounds half-up to six places and never drives a threshold. Comparisons require compatible claim, unit, dimension, population, coverage, qualification, time and counting convention. Changed populations are disclosed rather than interpreted as isolated integrity improvement.

On adoption of SIT-D023, the restricted HHI is an included supplementary diagnostic: it must expose its result or non-result behavior. This supersedes the earlier open choice of whether any numerical concentration capability would be included; it does not make the core profile conditional on scalar availability. It creates no optional hidden extra, report-quality score or additional input configuration.

**Affected public families.** SIT-M001-SIT-M015; value eligibility, units, rational representation, non-result explanations, output parity and comparison limits. Machine report envelope, capabilities/levels and actual field nesting remain Work Unit 6 work.

**Acceptance conditions.** JSON and Markdown cannot disagree about a missing qualified count. An empty seed inventory has zero records but no ratio. Unknowns cannot be removed to make a favorable scalar. A supplementary result cannot silently vanish when a prerequisite fails; its limitation remains visible.

**Scope of approval requested.** Adopt the exact arithmetic/non-result/comparison rules and included-supplementary diagnostic status. No executable report schema or implementation is authorized.

**Approval record:** On 2026-09-17, the same contextual acceptance selects Option B for exact arithmetic, field-specific non-results, parity and comparison limits. This does not pre-approve WU6 machine status names, runtime serialization or WU9 resource controls. **Previous record retained:** No acceptance of this new decision has been recorded. Submitted in Work Unit 4.

### 11.1 Historical Work Unit 4 review set and gates

The recommended WU4 adoption package is Option B for SIT-D019-SIT-D025 together with the named WU3/WU4 consumer documents. The eighteen earlier direction approvals remain in place. A single scoped acceptance can adopt the detailed package; it must not be recorded as approval of the complete Phase 0 baseline or any implementation phase.

| Existing direction / detail | WU4 realization | Remaining gate |
|---|---|---|
| SIT-D004-SIT-D007; SIT-D019-SIT-D021 | Explicit seed sets, typed origin boundaries, assessed comparison sets and frontier units | Pending detailed WU3/WU4 adoption |
| SIT-D010/SIT-D017 | Incidence core, restricted HHI and explicit exclusion of unsupported generalized metrics | SIT-D023/SIT-D025 |
| SIT-D008/SIT-D009/SIT-D013 | Evidence-specific externality, cohorts, retention and correction records | SIT-D024; WU5 threat labels; WU6 status envelope |
| SIT-D012/SIT-D018 | Per-analysis prerequisites and exact rational output meanings | SIT-D025; WU6 capability matrix and final format |
| SIT-D014/SIT-D015 | Protected identity and product separation unchanged | WU9 privacy/license controls; WU10 architecture/interchange |

After adoption, the next planned unit is Work Unit 5: `SOURCE_INTEGRITY_THREAT_MODEL.md`, an authorized product-spec update and an authorized register update. WU5 must define observable failure predicates and false-positive behavior without converting diagnostic counts into truth, political-position or intent classifiers.

## 12. Historical Work Unit 4 delivery and history

| Event | Recorded effect |
|---|---|
| User's latest “继续” after WU3 submission | Authorizes preparation of the next conditional documentation proposal; does not record a new detailed option selection |
| Revision 0.4 created | Preserves original twenty-one decision bodies and their dispositions; appends SIT-D022-SIT-D025 and current consumer gates |
| Current detailed approval request | Accept Option B for SIT-D019-SIT-D025 and the named WU3/WU4 documents, or identify changes |

The WU4 archive contains definitions revision 0.2, new reporting revision 0.1, product revision 0.2 and register revision 0.4. Historical source files, prior work-unit folders and prior ZIPs remain untouched. No full Phase 0 approval record, Phase 1 plan, code, schema, runtime fixture, test implementation or GitHub write is produced.

## 13. Work Unit 5 new decisions

The current instruction accepts the detailed WU3/WU4 contracts identified in §1.1. WU5 now supplies a threat model without altering their schema, numerical formulas, units or documentary meaning. The two new choices below add a threat-to-observation boundary and auditor self-protection requirements. They remain proposals until accepted.

### SIT-D026: Fourteen threat classes with narrow evidence-to-finding semantics

**Status:** BLOCKING before Work Unit 5 adoption; Option B recommended.  
**Gate:** Before the new threat catalog and product §16 are used as an accepted WU6 report requirement.  
**Basis:** PLAN Work Unit 5; accepted SIT-D005-SIT-D013 and SIT-D019-SIT-D025; SIT-P003-SIT-P013, SIT-P016; SIT-T004, SIT-T008, SIT-T010-SIT-T011, SIT-T014, SIT-T016-SIT-T026, SIT-T029, SIT-T032, SIT-T034-SIT-T039. The exact catalog is a toolkit operationalization.

**Question.** What can a v0.1 report claim when source-lineage evidence is associated with laundering, capture, starvation, poisoning or suppression?

**Existing constraints.** Shared ancestry, documentary qualification, assertion provenance, unknowns, action-specific authority and finite-cohort denominators are already defined. None permits automatic truth, intent, source-quality or statistical-error conclusions. WU6 still owns final machine status enums and nesting.

**Alternatives**

- **Option A.** Emit each broad threat label whenever a proxy such as high concentration, common ownership, missing correction or missing disagreement occurs.
- **Option B.** Adopt all fourteen plan threat cards, while separating derived structural observations, attributed external assessments/events and unassessed mechanisms. Every finding retains its narrow condition, scope, premise basis, witness, coverage and limitations.
- **Option C.** Omit a threat taxonomy and reduce the product to a raw inventory with no mechanism-level organization.

**Recommended option.** Approve B as specified in `SOURCE_INTEGRITY_THREAT_MODEL.md` §§1-5, §7.1-§7.2 and §8, with product §16.1-§16.2. Adopt SIT-TH001-SIT-TH014 as threat-family IDs, without turning those family names into allegations against sources or actors. Shared ancestry, typed cycles, unsupported assurance and stage/route limitations are reported at their demonstrated scope. Laundering intent, institutional capture, system-wide starvation, semantic falsity and successful manipulation remain attributed claims or unassessed mechanisms where the dossier does not establish them.

Derived observations preserve the basis of their premises; documentary qualification is still conditional on supplied material. A negative result from a partial graph cannot prove absence outside it. Several threat associations can describe one witness without becoming several independent incidents. A zero recorded overlap cannot become independence; a missing change cannot become failed correction; no incident record cannot become a clean-source certificate. Final serialized statuses and report nesting remain WU6 responsibilities.

**Affected public families.** Conceptual threat association and observation wording across SIT-M001-SIT-M015; witness/basis/coverage/limitation requirements; product §16; later report capability and testing contracts. No new input record, predicate, metric, output status enum or numerical threshold is introduced.

**Acceptance conditions.** Each of the fourteen cards has observable evidence, false-positive/missing-data rules, scope of detection/reporting and a future-extension boundary. W5-01-W5-14 and W5-22-W5-24 keep known shared structure distinct from broad mechanism claims. The four-way coverage matrix and metamorphic obligations in threat §8 are included in later tests. No class requires an unconstrained LLM trust judgment.

**Scope of approval requested.** Adopt the submitted threat meanings and product-capability boundary for later Phase 0 work. This does not execute any check, verify an empirical attack, authorize a source judgment, or complete WU6/WU7/WU8.

**Approval record:** No acceptance of this new decision has been recorded. Submitted in Work Unit 5.

### SIT-D027: Auditor self-protection, residual uncertainty and no active source intervention

**Status:** BLOCKING before Work Unit 5 adoption; Option B recommended.  
**Gate:** Before v0.1 detection claims are frozen and before WU9/WU10 turn these obligations into concrete controls.  
**Basis:** PLAN Work Unit 5's explicit detector boundary; SIT-D003, SIT-D006-SIT-D007, SIT-D014-SIT-D018, SIT-D021-SIT-D025; SIT-P002, SIT-P006, SIT-P012-SIT-P016; SIT-T004, SIT-T008, SIT-T010, SIT-T013, SIT-T022, SIT-T031, SIT-T035-SIT-T040. This is a toolkit operationalization.

**Question.** How should the release protect its own evidence/control boundary while avoiding unsupported guarantees about fabricated dossiers and hidden attacks?

**Existing constraints.** All source content is inert. The only runtime evidence payload is the selected local bundle. No source locator triggers a read. The full source registry, trust ranking, sanitation service, sanctions, public appeals and live interventions are outside v0.1. The plan permits considering a deterministic content detector but does not require selecting one. Resource, privacy and export controls remain later gated work.

**Alternatives**

- **Option A.** Add a minimal keyword/instruction detector, automatic quarantine and clean-input status as a convenience feature, and trust structurally consistent provenance as authenticated.
- **Option B.** Add explicit self-protection obligations for dossier fabrication, population manipulation, assurance/dispute handling, data-to-control injection, resource exhaustion, protected-source leakage and report laundering. Select no active content detector or automatic source action in v0.1; retain residual uncertainty and assign exact controls to their planned units.
- **Option C.** Omit auditor self-threats and leave downstream users to infer whether source metadata, report text and processing completion are trustworthy.

**Recommended option.** Approve B as specified in threat §§2-3, §6, §7.3-§7.4 and product §16.3-§16.4. Adopt SIT-TS001-SIT-TS007 as control-risk IDs. Consistent false metadata can still mislead the audit, so report qualifications must remain conditional. Scope/denominator changes are disclosed. Relevant disputes are preserved without proving the disputant's account or suppressing unrelated results. Self-supporting assurance cannot certify itself.

Source strings, extensions and locators remain data regardless of whether they look malicious. No hidden-prompt, poisoning, authorship or rhetorical-framing detector is selected, including an optional one. Existing structural input and graph checks remain included. A future processing interruption must not be presented as a completed absence. Protected topology can itself reveal identity, so no automatic anonymity guarantee is made. Report replay and selective quotation are constrained by preserved snapshot/target/population identity and limitations, with existing records available to represent challenges to findings.

No threat result triggers quarantine, down-weighting, deletion, source contact, sanction, appeal filing, benchmark/model alteration or rollback. Structural rejection is limited to the existing contract-validation rules. Exact budgets, path protections, display escaping, export/retention rules and module choices remain WU6/WU9/WU10 work; this decision grants no runtime permission.

**Affected public families.** Input/normalization and report-control requirements; structural rejection versus valid sparse/conflicted records; basis and missing-result explanations; future protection/resource/report behavior; all SIT-M001-SIT-M015 interpretations. No new JSON key, dependency, detector plugin, network opt-in or release score is added.

**Acceptance conditions.** W5-15-W5-21 preserve conditional assurance, finite population scope, inert input, incomplete-analysis status and protected identity limitations. W5-24 distinguishes no incident evidence from unperformed content detection. The final product text explicitly excludes automatic intervention and does not promise that a structurally valid dossier is genuine.

**Scope of approval requested.** Adopt the control obligations, residual-risk disclosure and v0.1 non-detector/non-intervention boundary. This is not approval of concrete resource numbers, a security certification, a privacy/export implementation or an additional implementation phase.

**Approval record:** No acceptance of this new decision has been recorded. Submitted in Work Unit 5.

## 14. Work Unit 5 realization and consumer gates

| Accepted contract | WU5 realization | Remaining gate |
|---|---|---|
| SIT-D019-SIT-D021 | Threat evidence uses the existing records, typed views, provenance and unresolved-reference rules | No input changes; WU6 may serialize the result meanings |
| SIT-D022-SIT-D023 | Shared origins, syndication, synthetic reuse and cycles preserve exact populations and scalar exclusions | Threat interpretation under SIT-D026; no new diagnostic |
| SIT-D024 | Evaluator, externality/stage and correction observations remain separate | SIT-D026; WU6 full capabilities and WU7 hero |
| SIT-D025 | Threat claims preserve field-specific reasons, full denominator and comparability | SIT-D026-SIT-D027; WU6 final output statuses |
| SIT-D003, SIT-D014, SIT-D017 | Local inert-data design and no automatic source intervention | SIT-D027; WU9/WU10 exact controls |
| SIT-D015, SIT-D018 | Product separation and equivalent local JSON/Markdown meanings | WU9 license, WU10 module/interface choices |

The detailed WU3/WU4 adoption gates are cleared by the current user acceptance, within their stated scope. No prior source or product rule is reversed. The newly submitted WU5 choices remain pending, with Option B recommended for both. Their adoption does not require separate approval of each threat-card ID.

## 15. Current review package and next action

The WU5 incremental package contains exactly three Markdown files: new `SOURCE_INTEGRITY_THREAT_MODEL.md` revision 0.1, `V0.1_PRODUCT_SPEC.md` revision 0.3 and this register revision 0.5. Earlier files and archives remain unchanged. The next review concerns SIT-D026-SIT-D027 and the WU5 documents only.

After acceptance, WU6 may work on its three allowed files: `OBSERVABILITY_AND_REPORTING.md`, `CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` and `SUCCESS_CRITERIA.md`. Its allowlist does not include this register. It may record the acceptance evidence in an allowed document and carry it into the register at the next authorized update. A genuinely new out-of-scope decision must receive explicit authorization or return to the relevant allowed unit.

No `PHASE_0_APPROVAL.md`, Phase 1 plan, executable schema, fixture, package, algorithm, detector, CI workflow, dependency manifest or GitHub write is authorized here.

## 16. Revision 0.5 history and checks

| Event | Recorded effect |
|---|---|
| Current intake: “可以，继续”, following the WU4 acceptance offer | Accepts SIT-D019-SIT-D025 and the named WU3/WU4 detailed package for continued Phase 0 design |
| Revision 0.5 approval updates | Preserves prior decision bodies; changes current status/approval records for the seven accepted details and retains previous dispositions |
| Revision 0.5 new work | Adds SIT-D026-SIT-D027 and their threat/control crosswalk |
| Editorial history clarification | Marks earlier handoffs historical and removes duplicate level-two numbering without altering decision IDs |
| Current status | Twenty-five accepted decisions in their stated scopes; two pending WU5 choices; no full Phase 0 or implementation authorization |

Local document checks cover decision-body preservation, referenced IDs, allowed file scope, input hashes, Markdown structure and archive contents. The drafting assistant performs those checks; no independent review, runtime security testing, empirical confirmation or CI run is claimed.
