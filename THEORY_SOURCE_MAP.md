# THEORY_SOURCE_MAP

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Target | v0.1 definition work |
| Phase / work unit | Phase 0 / Work Unit 1 |
| Revision | 0.1 |
| Date | 2026-09-16 |
| Status | SUBMITTED FOR REVIEW; affected semantics await recorded decisions |
| Execution authority | The user approved `PHASE_0_PLAN.md` in this conversation |
| Companion documents | `SPEC_AUDIT.md`; `UNRESOLVED_DECISIONS.md` |
| Implemented capabilities | None |

## 1. Reading this map

This map assigns stable IDs to the source claims and proposed translations relevant to the approved planning task. It preserves the papers’ terminology and separates their arguments from new software conventions.

Source aliases, exact filenames, version observations and input SHA-256 values are in [SPEC_AUDIT.md](SPEC_AUDIT.md), §2. Page references use the PDF page order, starting at 1. A source locator such as `[EC, §7.5, p. 11]` points to the supplied attachment, not an independently verified publication edition.

The proposed owner on each entry is a conceptual responsibility. It neither creates a module nor freezes a repository path. Public field names and executable Trace IDs remain work for later units.

### Classification vocabulary

| Classification | Meaning in this map |
|---|---|
| SOURCE_DEFINITION | A meaning or distinction explicitly introduced in a supplied paper |
| STRUCTURAL_LAW / STRUCTURAL_CLAIM | A structural proposition advanced by the author, retaining its stated conditions and domain |
| FORMAL_MODEL_RESULT | A mathematical result stated within a specified model in the supplied text |
| INHERITED_THEOREM | A theorem the supplied paper attributes to prior mathematical literature |
| SOURCE_COROLLARY | A consequence developed in the supplied paper using a stated formal result |
| SOURCE_BOUNDARY | A limitation or countercondition explicitly retained by the paper |
| GOVERNANCE_PROPOSAL / GOVERNANCE_PRINCIPLE | A proposed architecture, institutional function or governing requirement |
| EMPIRICAL_REPORT / MEASUREMENT_PROPOSAL | A reported empirical result or a proposed measurement procedure; neither means this work unit reproduced it |
| TOOLKIT_OPERATIONALIZATION | A proposed convention translating source concepts into this product |
| PLAN_RULE | A requirement or planning direction in the approved plan |

The classification of an entry does not certify the evidence supporting every claim in the original paper. Bibliographic references inside the attachments remain uninspected upstream sources unless specifically supplied. Multiple papers by the same author are separate theoretical texts; their repetition of a claim does not create independent empirical corroboration.

## 2. Stable-ID index

| ID | Subject | Main classification |
|---|---|---|
| SIT-T001 | Presence preserves continuing contact with reality | SOURCE_DEFINITION |
| SIT-T002 | Integrity includes provenance, accountability and disclosed conflicts | SOURCE_DEFINITION |
| SIT-T003 | Presence × Integrity is a joint structural requirement | STRUCTURAL_LAW |
| SIT-T004 | Verification has a limited scope | GOVERNANCE_PROPOSAL |
| SIT-T005 | Three data layers and the special role of human judgment | SOURCE_DEFINITION + STRUCTURAL_CLAIM |
| SIT-T006 | Four governance layers | GOVERNANCE_PROPOSAL |
| SIT-T007 | Seven components and nine functions retain separate source organization | GOVERNANCE_PROPOSAL |
| SIT-T008 | Minimum provenance survives transformations | GOVERNANCE_PROPOSAL |
| SIT-T009 | Trust weighting must remain contestable | GOVERNANCE_PROPOSAL |
| SIT-T010 | Manipulation is a source-integrity concern | GOVERNANCE_PROPOSAL + EMPIRICAL_REPORT |
| SIT-T011 | Human audit nodes must themselves be auditable | GOVERNANCE_PROPOSAL |
| SIT-T012 | Source return is distinct from epistemic correction | GOVERNANCE_PROPOSAL |
| SIT-T013 | Appeal and correction also apply to the integrity layer | GOVERNANCE_PROPOSAL |
| SIT-T014 | Closed recursion loses corrective difference under the stated conditions | STRUCTURAL_LAW |
| SIT-T015 | Finite-resampling results retain their state-space assumptions | FORMAL_MODEL_RESULT |
| SIT-T016 | External supply must carry genuine difference and integrity | STRUCTURAL_LAW + FORMAL_MODEL_RESULT |
| SIT-T017 | Concentration can be functional in the appropriate domain | SOURCE_BOUNDARY |
| SIT-T018 | Evaluator lineage can reproduce shared blind spots | STRUCTURAL_CLAIM |
| SIT-T019 | Structural validity precedes reliable measurement of a chosen object | SOURCE_DEFINITION + STRUCTURAL_CLAIM |
| SIT-T020 | Validation must match the type of claim | GOVERNANCE_PRINCIPLE |
| SIT-T021 | Distributional and structural reopening are different operations | SOURCE_DEFINITION + FORMAL_MODEL_RESULT |
| SIT-T022 | The durable evaluation record preserves epistemic distinctions | GOVERNANCE_PROPOSAL |
| SIT-T023 | Tail retention preserves consequential rare cases | GOVERNANCE_PROPOSAL |
| SIT-T024 | Corrective capacity includes power to change the system | GOVERNANCE_PROPOSAL |
| SIT-T025 | Open evaluation uses conjunctive conditions | GOVERNANCE_PRINCIPLE |
| SIT-T026 | Evaluation changes across time and interaction | STRUCTURAL_CLAIM + GOVERNANCE_PROPOSAL |
| SIT-T027 | Surface entropy, reality coupling and semantic gradient are distinct | SOURCE_DEFINITION |
| SIT-T028 | Garbling results are conditional and need not imply strict decay | INHERITED_THEOREM + SOURCE_COROLLARY |
| SIT-T029 | Effective replenishment has four stages | SOURCE_DEFINITION + STRUCTURAL_CLAIM |
| SIT-T030 | Independent measurement and frozen representations are required for information estimates | MEASUREMENT_PROPOSAL + SOURCE_BOUNDARY |
| SIT-T031 | Deployable diagnostics remain a profile | MEASUREMENT_PROPOSAL |
| SIT-T032 | Epistemic status survives answer synthesis | GOVERNANCE_PROPOSAL |
| SIT-T033 | Entropy remains a boundary and descriptive concept | STRUCTURAL_CLAIM + SOURCE_BOUNDARY |
| SIT-T034 | Reachability, authority and capacity require separate evidence | ADJACENT_STRUCTURAL_CLAIM + FORMAL_MODEL_RESULT |
| SIT-T035 | Claim-relative independence is a toolkit rule with source support | TOOLKIT_OPERATIONALIZATION + PLAN_RULE |
| SIT-T036 | Root counts and unresolved boundaries need explicit product conventions | TOOLKIT_OPERATIONALIZATION |
| SIT-T037 | Concentration and derivative-share measurements are operationalizations | TOOLKIT_OPERATIONALIZATION |
| SIT-T038 | Observability levels describe available evidence | TOOLKIT_OPERATIONALIZATION |
| SIT-T039 | Correction reachability is narrower than demonstrated correction | TOOLKIT_OPERATIONALIZATION |
| SIT-T040 | Local-first execution and project separation are product-governance choices | PLAN_RULE + TOOLKIT_OPERATIONALIZATION |

## 3. Source statements and proposed translations

### SIT-T001: Presence preserves continuing contact with reality

**Classification:** SOURCE_DEFINITION  
**Source locations:** [SIL, p. 7, “Source Integrity Is a Structural Requirement”; p. 12]; [EC, §7.2, p. 10]

**Source basis.** SIL defines Presence through broad, living and continuous contact with people, institutions, local realities, minority experiences, edge cases and expertise. EC adds a temporal and causal requirement: continued contact matters, and previously real data can become structurally internal through repeated optimization.

**Proposed toolkit implication.** Keep the external reference, inquiry, system boundary and observation time visible when a later specification describes external presence.

**Evidence needed.** An identified observation or input channel, its relationship to the audited system, and evidence about when and how it entered.

**Boundary.** Publication recency, a human author tag and an additional URL do not individually establish this source-defined property. A static bundle alone cannot establish continuing inflow.

**Decision links:** SIT-D008  
**Proposed conceptual owner:** External-presence representation  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T002: Integrity includes provenance, accountability and disclosed conflicts

**Classification:** SOURCE_DEFINITION  
**Source locations:** [SIL, pp. 7 and 12, Presence × Integrity discussion]

**Source basis.** SIL describes Integrity through provenance, accountability, resistance to manipulation, auditable process and conflict disclosure. Its later description includes origin, editorial process, ownership, revision history and credential status.

**Proposed toolkit implication.** Preserve evidence about these dimensions separately. An identity record should not erase an unresolved process or conflict question.

**Evidence needed.** Records supporting identity, origin, process, revisions, verification scope, and disclosed or disputed conflicts.

**Boundary.** The paper supplies a substantive definition rather than a normalized numerical scale. A complete record does not by itself prove the underlying assertions.

**Decision links:** SIT-D004; SIT-D007; SIT-D014  
**Proposed conceptual owner:** Provenance and assurance records  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T003: Presence × Integrity is a joint structural requirement

**Classification:** STRUCTURAL_LAW  
**Source locations:** [SIL, pp. 7 and 11-12]; [UIL, p. 5, “Closed Recursion and the Compact Formulas”]

**Source basis.** SIL identifies both pollution under weak integrity and starvation under narrowed presence. UIL gives S = P × I as a compact structural dependence and explicitly distinguishes these compact relations from a full dynamical model.

**Proposed toolkit implication.** Report evidence about presence and integrity together, without allowing one well-documented property to conceal an absent correction channel.

**Evidence needed.** Separate evidence supporting each property and the scope in which it is assessed.

**Boundary.** No supplied source defines calibrated P and I values for this toolkit. Multiplying arbitrary percentages would be a new measurement instrument. The approved plan forbids a universal v0.1 score.

**Decision links:** SIT-D001; SIT-D010  
**Proposed conceptual owner:** Integrity-profile semantics  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T004: Verification has a limited scope

**Classification:** GOVERNANCE_PROPOSAL  
**Source locations:** [SIL, pp. 11-14, verification and registry discussion]; [HDL, §9.2, pp. 22-23]

**Source basis.** The papers assign verification to identity, provenance and process. SIL preserves the value of non-verified, local and contested sources; HDL states that registration supplies accountability without automatic authority.

**Proposed toolkit implication.** Represent what was checked, by whom, against which evidence, and when. Preserve non-verified evidence without upgrading or rejecting it automatically.

**Evidence needed.** Verification records with subjects, scopes, methods, evidence and time bounds.

**Boundary.** Identity verification, source correctness, evidentiary independence and claim validation remain distinct. Anonymous and falsified identities also require different representations.

**Decision links:** SIT-D004; SIT-D007; SIT-D014  
**Proposed conceptual owner:** Identity and verification scope  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T005: Three data layers and the special role of human judgment

**Classification:** SOURCE_DEFINITION + STRUCTURAL_CLAIM  
**Source locations:** [SIL, pp. 6-7, “Source Integrity Is a Structural Requirement”; pp. 14-16]; [HDL, §2, pp. 4-5]

**Source basis.** SIL distinguishes surface-linguistic data, world-model data and judgment data. It makes a strong claim about model-generated judgment reinforcing inherited frames, and requires renewable human judgment input. HDL distinguishes surface-linguistic structure, world structure and judgment structure using its own wording.

**Proposed toolkit implication.** Carry these distinctions into the source audit and preserve the origin of judgment input. Do not silently rename the two papers’ terminology into one final enum.

**Evidence needed.** A declared data role, generation and review history, the actual human contribution where claimed, and external constraints used for validation.

**Boundary.** SIL p. 6 uses a stronger formulation about synthetic judgment than the general conditional treatment of synthetic provenance in UIL and HDL. Software admissibility remains blocked on SIT-D002.

**Decision links:** SIT-D002; SIT-D011  
**Proposed conceptual owner:** Judgment-origin and role representation  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T006: Four governance layers

**Classification:** GOVERNANCE_PROPOSAL  
**Source locations:** [SIL, p. 13, source-layer table]

**Source basis.** The table contains Open Web, Verified, Contested and Judgment. It assigns each a contribution, failure mode and governance requirement. These are the paper’s source-governance layers.

**Proposed toolkit implication.** Preserve the four source terms and their distinct purposes when deciding the ontology. Review whether a record can occupy more than one role.

**Evidence needed.** Evidence for authentication status, contestation, source function and judgment contribution.

**Boundary.** The source table does not specify a disjoint software enum, an ordinal quality scale or automatic assignment rules. Treating the four labels as such would add product semantics.

**Decision links:** SIT-D011  
**Proposed conceptual owner:** Source-function representation  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T007: Seven components and nine functions retain separate source organization

**Classification:** GOVERNANCE_PROPOSAL  
**Source locations:** [SIL, pp. 12-15, “The Source Integrity Layer”]; [HDL, §9.1-9.9, pp. 22-24]

**Source basis.** SIL organizes the architecture into seven components: registry, provenance, trust-weighted retrieval, manipulation detection, human audit nodes, source return and appeals. HDL presents nine functions, explicitly separating crawler identity, epistemic-status preservation and anomaly retention, while grouping audit and appeal.

**Proposed toolkit implication.** Map both enumerations without replacing either one. Distinguish information this toolkit may represent from institutions or services it would have to operate.

**Evidence needed.** A component-to-artifact mapping and a declared v0.1 scope for every mapped function.

**Boundary.** These are architecture proposals. Their presence in the theory does not authorize implementation of all components in this project or phase.

**Decision links:** SIT-D003; SIT-D011  
**Proposed conceptual owner:** Product scope and theory traceability  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T008: Minimum provenance survives transformations

**Classification:** GOVERNANCE_PROPOSAL  
**Source locations:** [SIL, p. 14, provenance paragraph]; [HDL, §9.3, p. 23]

**Source basis.** SIL identifies author, publisher, timestamp, version history, original-versus-syndicated status, machine-generation disclosure, signatures or checksums and licensing metadata. HDL distinguishes original observation, human editing, summarization, translation, moderation, retrieval and synthesis.

**Proposed toolkit implication.** Plan separate artifact versions, actors and transformation assertions. Record missing fields rather than supplying inferred metadata as fact.

**Evidence needed.** Artifact identifiers, version-specific evidence, transformation records and assertion provenance.

**Boundary.** A checksum anchors bytes. It does not certify factual correctness or independence. The cited provenance standards were not separately inspected during this work unit.

**Decision links:** SIT-D004; SIT-D007; SIT-D014  
**Proposed conceptual owner:** Artifact and transformation provenance  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T009: Trust weighting must remain contestable

**Classification:** GOVERNANCE_PROPOSAL  
**Source locations:** [SIL, p. 14, trust-weighted retrieval paragraph]; [HDL, §9.5, p. 23]

**Source basis.** The sources propose weighting by provenance, relevance, correction behavior, expertise and disclosed conflicts, together with visible criteria and contestation. SIL calls for displaying substantive disagreement instead of compressing it into apparent consensus.

**Proposed toolkit implication.** The bounded toolkit can retain supplied weighting and selection records for audit. Its v0.1 scope should be decided separately from an operational retriever.

**Evidence needed.** Declared criteria, selected and omitted items where known, and supporting evidence for any supplied weight.

**Boundary.** Neither paper supplies this toolkit’s ranking formula or calibration. Preserving disagreement does not imply equal evidentiary weight.

**Decision links:** SIT-D003; SIT-D010; SIT-D013  
**Proposed conceptual owner:** Selection and weighting audit  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T010: Manipulation is a source-integrity concern

**Classification:** GOVERNANCE_PROPOSAL + EMPIRICAL_REPORT  
**Source locations:** [SIL, pp. 8-10 and 14]; [HDL, §7.2, p. 20; §9.6, p. 23]

**Source basis.** The sources discuss hidden instructions, poisoning, repetition, laundering and contamination at the source interface. They propose sanitation, quarantine or down-weighting in the broader architecture.

**Proposed toolkit implication.** Separate a supplied incident allegation, observed lineage pattern and demonstrated attack effect. Record the evidence and reporting actor for each.

**Evidence needed.** Version-specific material, incident records, methods and results; controlled outcome evidence for a claim of successful manipulation.

**Boundary.** A shared root, a repeated phrase or an optimized page does not independently prove malicious intent. This work unit neither runs a detector nor validates the cited attack studies.

**Decision links:** SIT-D003; SIT-D007; SIT-D014  
**Proposed conceptual owner:** Threat evidence and ingestion boundary  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T011: Human audit nodes must themselves be auditable

**Classification:** GOVERNANCE_PROPOSAL  
**Source locations:** [SIL, pp. 14-15, human audit nodes]; [HDL, §9.8, p. 23]

**Source basis.** SIL calls for distributed, compensated, conflict-disclosed and auditable human review, especially for the judgment layer. HDL requires authority to inspect sources, transformation lineage, omitted evidence and model-family correlation.

**Proposed toolkit implication.** Represent reviewer roles, contributions, relationships, conflicts and authority rather than relying on a human-reviewed badge.

**Evidence needed.** Review scope, reviewer provenance, supplied evidence, authority and documented actions.

**Boundary.** A human identity does not establish an independent process or an adequate intervention. The toolkit would audit records of review rather than operate the human institution.

**Decision links:** SIT-D002; SIT-D005; SIT-D009  
**Proposed conceptual owner:** Evaluator and human-review lineage  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T012: Source return is distinct from epistemic correction

**Classification:** GOVERNANCE_PROPOSAL  
**Source locations:** [SIL, p. 8 and p. 15, source-return paragraph]; [HDL, §9.9, p. 24]

**Source basis.** SIL distinguishes the economic feedback sustaining sources from the epistemic feedback sustaining reality contact. It proposes records of crawling, retrieval, citation, answer use and compensation or traffic credit. HDL similarly treats source production as part of long-run integrity.

**Proposed toolkit implication.** Retain this requirement in the theory map even when payment and referral infrastructure are outside v0.1.

**Evidence needed.** Use and return records would be needed to audit fulfillment; a citation alone supplies incomplete evidence.

**Boundary.** No payment, entitlement, source-valuation or legal-compliance algorithm is specified here. Deferring infrastructure must not be described as satisfying the full source-return requirement.

**Decision links:** SIT-D003; SIT-D015  
**Proposed conceptual owner:** Source-return boundary  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T013: Appeal and correction also apply to the integrity layer

**Classification:** GOVERNANCE_PROPOSAL  
**Source locations:** [SIL, p. 15, appeals paragraph]; [HDL, §9.8, p. 23]

**Source basis.** The proposed integrity layer can make erroneous flags, metadata assignments and weighting choices. SIL requires reasoned, logged review and a route to contest them.

**Proposed toolkit implication.** Plan for disputed lineage assertions and superseded audit findings. The toolkit’s own outputs should retain enough provenance to be corrected.

**Evidence needed.** Challenged finding, evidence, reviewer decision, affected version and resulting change or reasoned rejection.

**Boundary.** Recording a dispute neither validates the objection nor establishes a functioning public appeal institution.

**Decision links:** SIT-D007; SIT-D009  
**Proposed conceptual owner:** Audit-output correction lineage  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T014: Closed recursion loses corrective difference under the stated conditions

**Classification:** STRUCTURAL_LAW  
**Source locations:** [UIL, pp. 2-5 and 9-10; pp. 15-17]

**Source basis.** UIL states the structural sequence of closure, loss of difference, inherited deviations or correlated error, and integrity decay. It locates exact stochastic commonality in specified finite-resampling settings and presents other domains as structural extensions.

**Proposed toolkit implication.** Audit recorded dependency and correction structure while preserving the distinction between closure exposure and demonstrated functional degradation.

**Evidence needed.** An identified system, recurrence or dependency history, external-reference obligation and evidence of replenishment or its absence.

**Boundary.** A static citation bundle does not supply the complete dynamics of a recursively trained system. A structural dependency finding cannot establish a collapse date or measured performance loss.

**Decision links:** SIT-D001; SIT-D003  
**Proposed conceptual owner:** Closure interpretation  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T015: Finite-resampling results retain their state-space assumptions

**Classification:** FORMAL_MODEL_RESULT  
**Source locations:** [UIL, pp. 6-9, mathematical core]; [EC, §4.1-4.4, pp. 6-7]

**Source basis.** The supplied texts state finite multinomial reconstruction, expected Gini-Simpson contraction, one-step omission probability, absorbing loss of support and expected squared-distance growth relative to a fixed reference. These are results for the specified generational model.

**Proposed toolkit implication.** Use these results to explain why finite closed reuse is an important failure family. Preserve a separate boundary around graph-based source diagnostics.

**Evidence needed.** Direct numerical application would require a declared state distribution, sample size, transition mechanism and external reference.

**Boundary.** Document count is not automatically sample size, lineage depth is not automatically generation count, and a root graph is not a multinomial transition model. No simulation is authorized.

**Decision links:** SIT-D001; SIT-D010  
**Proposed conceptual owner:** Formal-model boundary  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T016: External supply must carry genuine difference and integrity

**Classification:** STRUCTURAL_LAW + FORMAL_MODEL_RESULT  
**Source locations:** [UIL, pp. 8-9]; [EC, §4.4, p. 7]

**Source basis.** UIL reopens resampling with an external distribution and warns that a large mixing coefficient does not protect the system when the input is contaminated, unrepresentative or derived from the same closed source. EC applies the distinction to evaluation input.

**Proposed toolkit implication.** Record the relationship of an incoming artifact to the existing lineage and the basis for its claimed external contribution.

**Evidence needed.** An explicit external source, its ancestry, relevant new constraint and time of introduction.

**Boundary.** The mixing coefficient cannot be estimated from domain count without a separately justified model. An external label supplied by a user remains an assertion with a provenance basis.

**Decision links:** SIT-D005; SIT-D008  
**Proposed conceptual owner:** External-origin qualification  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T017: Concentration can be functional in the appropriate domain

**Classification:** SOURCE_BOUNDARY  
**Source locations:** [UIL, p. 9 and p. 16]; [EC, §12, p. 14]

**Source basis.** The sources state that convergence can be functional when a correct stable optimum or genuinely closed task makes broader variation unnecessary. Integrity loss depends on continuing external obligations.

**Proposed toolkit implication.** Keep concentration as a structural description and disclose the declared task and reference before attaching risk interpretations.

**Evidence needed.** Task requirements, relevant state space and external-reference obligations.

**Boundary.** One root can be adequate for a narrowly scoped documentary question. Numerous independent observations can still be wrong. Neither root count determines truth.

**Decision links:** SIT-D004; SIT-D010  
**Proposed conceptual owner:** Interpretation and false-positive controls  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T018: Evaluator lineage can reproduce shared blind spots

**Classification:** STRUCTURAL_CLAIM  
**Source locations:** [EC, §3.2, p. 5; §5.4, p. 9; §11, pp. 13-14]; [HDL, §7.3, pp. 20-21]

**Source basis.** EC identifies shared generators, reference answers, rubric conventions, training data and model judges as a route for correlated evaluative error. It proposes representing model families and evaluator ancestors in a provenance graph.

**Proposed toolkit implication.** Represent the roles of generator, candidate, reference, rubric and judge separately, including known and unknown common ancestors.

**Evidence needed.** Versioned model and data identifiers, process records, rubric origins and evaluation roles.

**Boundary.** Known shared ancestry supports an overlap finding. It does not measure error covariance. Different endpoints or provider names do not prove independence.

**Decision links:** SIT-D002; SIT-D005; SIT-D007  
**Proposed conceptual owner:** Evaluator lineage  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T019: Structural validity precedes reliable measurement of a chosen object

**Classification:** SOURCE_DEFINITION + STRUCTURAL_CLAIM  
**Source locations:** [EC, §2.1-2.3, pp. 3-4; §7.1, p. 10]

**Source basis.** EC distinguishes measurement, distributional and structural validity. Its structural cut determines which states, boundaries, relations, horizons and consequences can become visible.

**Proposed toolkit implication.** Require an inquiry scope and explicitly omitted conditions in a future audit contract; retain anomalies that challenge that scope.

**Evidence needed.** Declared audit target, represented relationships, consequence horizon and documented omissions.

**Boundary.** A consistent provenance graph does not certify that the inquiry represents every deployment-relevant condition. The toolkit itself has a structural cut.

**Decision links:** SIT-D004; SIT-D013  
**Proposed conceptual owner:** Audit-scope contract  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T020: Validation must match the type of claim

**Classification:** GOVERNANCE_PRINCIPLE  
**Source locations:** [EC, §6, pp. 9-10]

**Source basis.** EC assigns different constraints to formal, empirical, causal, coding, agentic, safety and human-consequence claims. It explicitly identifies execution as a constraint for coding and observation or replication for empirical claims.

**Proposed toolkit implication.** Preserve claim and evidence roles so an independent analysis, formal verification or observation is represented according to what it can validate.

**Evidence needed.** Claim type, validation method, relevant outputs and known scope limits.

**Boundary.** A common dataset can support independent analyses without becoming multiple data-collection events. Source-count semantics must not erase this distinction. No proof checker or execution engine is implemented here.

**Decision links:** SIT-D002; SIT-D004; SIT-D005  
**Proposed conceptual owner:** Evidence-role and validation-method contract  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T021: Distributional and structural reopening are different operations

**Classification:** SOURCE_DEFINITION + FORMAL_MODEL_RESULT  
**Source locations:** [EC, §4.4-4.5, pp. 7-8]

**Source basis.** Distributional reopening supplies fresh cases within represented states. Structural reopening changes the state space when preserved anomalies reveal a problem with the inherited cut.

**Proposed toolkit implication.** Distinguish a new artifact, new origin and revised inquiry or taxonomy in future change records.

**Evidence needed.** Before-and-after scope definitions, anomaly evidence, accepted changes and source lineage.

**Boundary.** A new benchmark item does not establish a new structural class. The toolkit can preserve change evidence without independently inventing a superior classification.

**Decision links:** SIT-D004; SIT-D013  
**Proposed conceptual owner:** Anomaly and scope-revision records  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T022: The durable evaluation record preserves epistemic distinctions

**Classification:** GOVERNANCE_PROPOSAL  
**Source locations:** [EC, §7.3, p. 11]

**Source basis.** EC lists content, source, knowledge type, transformation history, model lineage, validation status and unresolved uncertainty as the minimum conceptual record.

**Proposed toolkit implication.** Use this list as a source-derived coverage requirement for later data specifications, while naming exact fields only through approved product decisions.

**Evidence needed.** The corresponding supplied records and references for every assessed claim or item.

**Boundary.** A populated field is evidence of a declaration; it does not establish that the declaration is verified. Unknown and disputed entries must remain possible.

**Decision links:** SIT-D004; SIT-D007  
**Proposed conceptual owner:** Canonical evidence record  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T023: Tail retention preserves consequential rare cases

**Classification:** GOVERNANCE_PROPOSAL  
**Source locations:** [EC, §7.1 and §7.4, pp. 10-11]; [HDL, §9.7, p. 23]

**Source basis.** The papers require preservation of anomalies, low-frequency conditions, minority descriptions, contradictions and unresolved reports long enough to challenge current representations.

**Proposed toolkit implication.** Keep supplied anomaly and contestation evidence visible. Compare retention only against a declared input set or documented processing stage.

**Evidence needed.** Input universe or stage logs, relevant classifications, exclusions and transformations.

**Boundary.** An item’s absence from the final bundle does not by itself prove suppression. A world-wide retention percentage requires a denominator that the bundle may not provide.

**Decision links:** SIT-D013  
**Proposed conceptual owner:** Tail and contestation audit  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T024: Corrective capacity includes power to change the system

**Classification:** GOVERNANCE_PROPOSAL  
**Source locations:** [EC, §7.5, p. 11]

**Source basis.** EC requires escalation, override, rollback, scope restriction, benchmark revision, incident incorporation, evaluator replacement or model withdrawal where appropriate. Passive monitoring does not complete this loop.

**Proposed toolkit implication.** Record the relevant correction target, authority, permissible actions and evidence of outcome, separately from detection.

**Evidence needed.** Authorized routes, accepted findings, action records, versions and results.

**Boundary.** A generic communication edge cannot prove an operative intervention. A reasoned rejection can be a valid review outcome; every incoming objection need not alter the answer.

**Decision links:** SIT-D009  
**Proposed conceptual owner:** Corrective-capacity evidence  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T025: Open evaluation uses conjunctive conditions

**Classification:** GOVERNANCE_PRINCIPLE  
**Source locations:** [EC, §7, pp. 10-11]

**Source basis.** EC presents structural validity, external presence, source integrity, tail retention and corrective capacity as jointly required conditions. The formula on p. 11 is logical conjunction.

**Proposed toolkit implication.** Preserve the separate status and evidence of these conditions in a future profile.

**Evidence needed.** Evidence specific to each condition and its declared assessment scope.

**Boundary.** The toolkit will inspect only a bounded subset of each condition. A populated five-part report cannot certify general capability, safety or deployment readiness.

**Decision links:** SIT-D010; SIT-D012  
**Proposed conceptual owner:** Profile and claim-limitation contract  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T026: Evaluation changes across time and interaction

**Classification:** STRUCTURAL_CLAIM + GOVERNANCE_PROPOSAL  
**Source locations:** [EC, §8-10, pp. 12-13]

**Source basis.** EC requires attention to coherence, propagation, recovery and environmental feedback over time, and requires reports to state measurement context and currency limits.

**Proposed toolkit implication.** Use version-specific evidence and an audit time boundary. Differentiate an available route from observed propagation across versions.

**Evidence needed.** Versions, event times, observation times and before-and-after records.

**Boundary.** A static input supports a snapshot. A recorded temporal association alone does not identify the causal effect of a correction.

**Decision links:** SIT-D007; SIT-D008; SIT-D009  
**Proposed conceptual owner:** Temporal evidence and report scope  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T027: Surface entropy, reality coupling and semantic gradient are distinct

**Classification:** SOURCE_DEFINITION  
**Source locations:** [HDL, §3.1-3.4, pp. 5-8; §11.1, p. 28]

**Source basis.** HDL defines reality-coupled information as mutual information with a declared reality state and semantic gradient using pairwise Jensen-Shannon separation. It distinguishes both from surface entropy and notes that mutual information depends on the chosen state variable.

**Proposed toolkit implication.** Keep these quantities in the theory map as distinct objects. Source-artifact diversity cannot be relabeled as any of them.

**Evidence needed.** Direct measurement would require specified states, distributions, priors, pair weights and an estimation protocol.

**Boundary.** The present provenance bundle supplies none of these quantities automatically. There is no approved entropy-to-truth conversion. EBC’s broader entropy language creates a translation issue recorded in SIT-D001.

**Decision links:** SIT-D001; SIT-D010  
**Proposed conceptual owner:** Information-theoretic boundary  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T028: Garbling results are conditional and need not imply strict decay

**Classification:** INHERITED_THEOREM + SOURCE_COROLLARY  
**Source locations:** [HDL, §4.1-4.5, pp. 8-13; §11.2-11.5, pp. 28-29]

**Source basis.** HDL applies data processing to a closed Markov channel, derives semantic-gradient non-expansion, adds an explicit strict-contraction assumption for exponential decay and applies Blackwell comparison to attainable decision value. It allows lossless transformations, task-specific benefits and incomparable experiments.

**Proposed toolkit implication.** Preserve transformation lineage without declaring every rewrite harmful or every pair of evidence systems rankable.

**Evidence needed.** An explicitly established channel, reality variable, relevant assumptions and distributions would be required for a numerical theorem-based claim.

**Boundary.** A citation or summarization edge alone does not establish the Markov condition, a contraction coefficient or a semantic half-life. No general leaderboard follows from these results.

**Decision links:** SIT-D001; SIT-D010  
**Proposed conceptual owner:** Transformation interpretation  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T029: Effective replenishment has four stages

**Classification:** SOURCE_DEFINITION + STRUCTURAL_CLAIM  
**Source locations:** [HDL, §4.6, p. 13; §5.5, pp. 16-17]

**Source basis.** HDL requires independent reality-bearing difference to enter, survive preprocessing, receive sufficient selection weight and affect training, retrieval or generation. It explicitly distinguishes many derivative summaries from an independent observed anomaly.

**Proposed toolkit implication.** Plan an evidence profile that distinguishes admission, retention, selection and downstream influence.

**Evidence needed.** Origin evidence, pipeline-stage records, selection logs and downstream observations.

**Boundary.** Admission into storage establishes only the observed admission. Synthetic provenance alone does not settle integrity; the relation to independent structure and correction remains material.

**Decision links:** SIT-D002; SIT-D008  
**Proposed conceptual owner:** Replenishment-stage representation  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T030: Independent measurement and frozen representations are required for information estimates

**Classification:** MEASUREMENT_PROPOSAL + SOURCE_BOUNDARY  
**Source locations:** [HDL, §10.1-10.4, pp. 24-26]

**Source basis.** HDL warns about direct high-dimensional mutual-information estimation, proposes held-out approaches, requires independent reality records and separates representation drift from measured language change.

**Proposed toolkit implication.** Keep source-topology findings distinct from empirical estimates of information or decision loss. Record the evidence origin of any externally supplied estimate.

**Evidence needed.** Independent state labels, event-level held-out data, fixed representation, uncertainty and controls.

**Boundary.** Many articles about one event are not automatically independent statistical samples. The source also does not imply that separately gathered observations of one event must share one evidentiary origin.

**Decision links:** SIT-D004; SIT-D005; SIT-D010  
**Proposed conceptual owner:** Empirical-measurement boundary  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T031: Deployable diagnostics remain a profile

**Classification:** MEASUREMENT_PROPOSAL  
**Source locations:** [HDL, §10.5-10.6, pp. 27-28]

**Source basis.** HDL proposes multiple operational audit metrics, including contestation exposure and correction elasticity, and explicitly keeps the profile separate from a single aggregate score. It identifies observations that could weaken its empirical diagnosis.

**Proposed toolkit implication.** Use this as support for multi-dimensional reporting and falsifiable claims. Record which proposed metrics need data outside v0.1.

**Evidence needed.** Metric-specific sampling units, denominators, independent evidence and uncertainty.

**Boundary.** The proposed metrics do not calibrate Independent Root Count, lineage HHI or observability levels. Those remain toolkit operationalizations.

**Decision links:** SIT-D008; SIT-D010; SIT-D012; SIT-D013  
**Proposed conceptual owner:** Metric provenance and falsification  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T032: Epistemic status survives answer synthesis

**Classification:** GOVERNANCE_PROPOSAL  
**Source locations:** [HDL, §5.4, p. 16; §9.4 and §9.8, p. 23]

**Source basis.** HDL distinguishes measurements, testimony, official statements, allegations, estimates, editorial judgments, model inferences and fictional examples. It warns that answer compression can erase their differences and omitted conflicts.

**Proposed toolkit implication.** Require later specifications to preserve supplied knowledge types, uncertainty and transformation history at the scope of the claim being audited.

**Evidence needed.** Claim spans or identifiers, evidence roles, transformations and attribution.

**Boundary.** Representing a supports or contradicts assertion cannot silently become automated semantic verification of that relation.

**Decision links:** SIT-D004; SIT-D007; SIT-D013  
**Proposed conceptual owner:** Epistemic-status representation  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T033: Entropy remains a boundary and descriptive concept

**Classification:** STRUCTURAL_CLAIM + SOURCE_BOUNDARY  
**Source locations:** [EBC, pp. 1 and 3-4; pp. 7-11]

**Source basis.** EBC distinguishes causal interactions from the entropy accounting or structural description of a system. The added derivation discussion states assumptions and distinguishes descriptive scales.

**Proposed toolkit implication.** Use this background to keep causes, diagnostic quantities and observed outcomes separate in the toolkit’s claims.

**Evidence needed.** An identified mechanism and domain-appropriate quantities for any applied diagnosis.

**Boundary.** EBC pp. 5-6 also contain broader directional statements about AI output entropy. Those are preserved as source text and routed to SIT-D001; they cannot silently determine a universal entropy alarm.

**Decision links:** SIT-D001  
**Proposed conceptual owner:** Background explanatory boundary  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T034: Reachability, authority and capacity require separate evidence

**Classification:** ADJACENT_STRUCTURAL_CLAIM + FORMAL_MODEL_RESULT  
**Source locations:** [BVL, pp. 10-15, network core; pp. 22-23, oversight; p. 25, model limits]

**Source basis.** BVL separates capture routing and accessibility from sustainable carrying capacity, and treats network equations as conditional on specified nodes, edges, routing and loads. Its oversight discussion distinguishes nominal review from practical processing capacity.

**Proposed toolkit implication.** Consider authority and capacity evidence when interpreting a correction route. Keep this use confined to the approved adjacent role.

**Evidence needed.** Declared roles, permitted actions, routes, applicable capacity or service records and time horizon.

**Boundary.** A source graph does not supply an absorbing chain, a queue or calibrated social flow. No capture probability, utilization ratio or cascade simulation is authorized.

**Decision links:** SIT-D009  
**Proposed conceptual owner:** Correction-boundary interpretation  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T035: Claim-relative independence is a toolkit rule with source support

**Classification:** TOOLKIT_OPERATIONALIZATION + PLAN_RULE  
**Source locations:** [PLAN, §5, Rule 1]; supporting basis: [HDL, §3.1, pp. 5-6]; [EC, §6, pp. 9-10]

**Source basis.** The approved plan requires independence to be relative to a claim, observation, evidence unit or judgment. The papers support declared inquiries and type-appropriate validation; they do not provide this toolkit’s final claim-scoped independence predicate.

**Proposed toolkit implication.** Specify the target claim, context, evidence role and comparison set before computing any future independence result.

**Evidence needed.** Claim identifiers, source roles and claim-relevant dependency assertions.

**Boundary.** One artifact may be original for one claim and derivative for another. A global source-independent boolean would add an unsupported shortcut.

**Decision links:** SIT-D004; SIT-D005  
**Proposed conceptual owner:** Claim and inquiry model  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T036: Root counts and unresolved boundaries need explicit product conventions

**Classification:** TOOLKIT_OPERATIONALIZATION  
**Source locations:** [PLAN, §§5, 10-11]; supporting basis: [UIL, pp. 8-9]; [HDL, §4.6, p. 13]

**Source basis.** The plan proposes independent and unknown root counts. The sources motivate ancestry and independent replenishment but do not define a complete graph-root counting algorithm or an independence partition.

**Proposed toolkit implication.** Differentiate observed terminal nodes, documented origin events, qualified independent origins and unresolved upstream boundaries.

**Evidence needed.** Typed ancestry, identity resolution, origin evidence, a declared graph boundary and an approved independence rule.

**Boundary.** A terminal node with no recorded parent may simply have missing history. Several unresolved paths may lead to one origin; one unresolved path may conceal many. No unqualified global count follows.

**Decision links:** SIT-D004; SIT-D005; SIT-D006; SIT-D007  
**Proposed conceptual owner:** Origin and uncertainty semantics  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T037: Concentration and derivative-share measurements are operationalizations

**Classification:** TOOLKIT_OPERATIONALIZATION  
**Source locations:** [PLAN, §11]; supporting basis: [UIL, pp. 9 and 16]; [EC, §3.2, p. 5]; [HDL, §4.6, p. 13]

**Source basis.** The plan proposes lineage concentration and derivative share. The theory supports examining common ancestry and distinguishes concentration from functional failure.

**Proposed toolkit implication.** Specify the counted units, attribution policy, denominator, unresolved share and permissible interpretation before selecting a formula.

**Evidence needed.** Claim-scoped contributions, resolved ancestry and any declared allocation weights.

**Boundary.** HHI, inverse concentration, high/low labels and effective-root counts are not calibrated by these sources for this product. A normalized topology measure would not be truth probability or effective independent sample size.

**Decision links:** SIT-D006; SIT-D010  
**Proposed conceptual owner:** Descriptive concentration semantics  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T038: Observability levels describe available evidence

**Classification:** TOOLKIT_OPERATIONALIZATION  
**Source locations:** [PLAN, §13]; supporting basis: [EC, §10, p. 13]; [HDL, §10-11, pp. 24-29]

**Source basis.** The plan proposes Levels 0-4 and a capability matrix. The papers require limited claims and explicit uncertainty; they do not define this level system.

**Proposed toolkit implication.** Make each future output depend on its own evidence prerequisites, with a missing-data reason when unavailable.

**Evidence needed.** Field-specific metadata and a manifest of available evidence.

**Boundary.** A well-observed system can have poor integrity. Evidence of a correction event can exist while origin resolution remains incomplete. A level must not erase such independent capabilities.

**Decision links:** SIT-D006; SIT-D012  
**Proposed conceptual owner:** Observability and reporting  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T039: Correction reachability is narrower than demonstrated correction

**Classification:** TOOLKIT_OPERATIONALIZATION  
**Source locations:** [PLAN, §5, Rules 8-9; §§11 and 14]; supporting basis: [EC, §7.5, p. 11]; [HDL, §4.6, p. 13; §10.5, p. 27]; [BVL, pp. 22-23]

**Source basis.** The plan proposes correction reachability and propagation analysis. The source requirements concern effective corrective capacity and replenishment; a path-finding result represents only part of those requirements.

**Proposed toolkit implication.** Distinguish declared route, authorized applicable route, observed handling and demonstrated downstream change in the future specification.

**Evidence needed.** Correction target, typed route, authority, time and version records, acceptance or rejection rationale, and observed outcomes.

**Boundary.** In a partial graph, no recorded route supports an unresolved finding rather than proof that no route exists. A received objection need not be valid. A downstream edit alone does not establish its cause.

**Decision links:** SIT-D006; SIT-D009  
**Proposed conceptual owner:** Correction evidence tiers  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

### SIT-T040: Local-first execution and project separation are product-governance choices

**Classification:** PLAN_RULE + TOOLKIT_OPERATIONALIZATION  
**Source locations:** [PLAN, §§3.3-4, 16-18 and 23]; supporting basis: [SIL, pp. 14-15, auditability and appeals]

**Source basis.** The plan requires a separate Source Integrity Toolkit project and a documentation-only Phase 0. It proposes local-first processing, bounded dependencies, protected source handling and later interoperability without shared internals.

**Proposed toolkit implication.** Keep this work unit inside the three authorized Markdown outputs. Preserve private-source uncertainty without inventing identities. Carry license and dependency selection to their designated work units.

**Evidence needed.** The approved plan, explicit authorizations and a record of actual outputs.

**Boundary.** The papers do not prescribe a Python package, CLI, license, folder tree or runtime network policy. Shared concepts do not make either toolkit the exclusive owner of every lineage technique.

**Decision links:** SIT-D003; SIT-D014; SIT-D015  
**Proposed conceptual owner:** Project governance and future boundaries  
**Mapping status:** Recorded for review; no affected software semantics approved by this entry.

## 4. Coverage of the plan’s candidate dimensions

| Candidate dimension in the plan | Source basis | Translation requiring definition |
|---|---|---|
| Nominal Source Count | SIT-T008, SIT-T029, SIT-T036 | What counts as an artifact; whether versions and repeated citations are counted separately |
| Resolved Source Count | SIT-T004, SIT-T008, SIT-T036 | Identity resolution versus provenance resolution; resolution evidence |
| Independent Root Count | SIT-T016, SIT-T020, SIT-T035, SIT-T036 | Origin role, inquiry scope, comparison set and independence rule |
| Unknown Root Count | SIT-T036, SIT-T038 | Whether to use unresolved-boundary count instead; unknown multiplicity |
| Lineage Concentration | SIT-T017, SIT-T018, SIT-T037 | Unit, weights, allocation, denominator, missing share and interpretation |
| Derivative Share | SIT-T008, SIT-T029, SIT-T037 | Claim-specific contribution and mixed original/derivative artifacts |
| External Presence | SIT-T001, SIT-T016, SIT-T029 | Boundary, time, genuine external contribution and four replenishment stages |
| Corrective Independence | SIT-T011, SIT-T018, SIT-T020, SIT-T039 | Independence of reviewer, evidence and process; assurance scope |
| Correction Reachability | SIT-T024, SIT-T026, SIT-T034, SIT-T039 | Applicable authorized paths, partial graphs and actual outcomes |
| Evaluator Lineage Overlap | SIT-T018, SIT-T022 | Relevant ancestry relations and role-specific overlap |
| Tail / Contestation Retention | SIT-T019, SIT-T021, SIT-T023, SIT-T032 | Input universe, excluded-item evidence, context and denominator |
| Provenance Completeness | SIT-T002, SIT-T008, SIT-T022, SIT-T038 | Required fields, assertion evidence, covered graph and redactions |

Each candidate has a source basis or an explicit operationalization label. None receives a final computation rule through this coverage table.

## 5. Coverage of the proposed threat family

| Candidate threat | Supporting map entries | Minimum evidentiary distinction |
|---|---|---|
| False plurality, syndication and derivative inflation | SIT-T008, SIT-T029, SIT-T036, SIT-T037 | Visible items versus documented common origins |
| Citation laundering and provenance erasure | SIT-T008, SIT-T022, SIT-T032 | A represented transformation or attribution gap versus an inferred motive |
| Circular support | SIT-T014, SIT-T018, SIT-T036 | A typed citation cycle versus a cycle being used as unsupported corroboration |
| Evaluator self-validation and benchmark closure | SIT-T018, SIT-T019, SIT-T020 | Shared evaluative ancestry versus measured correlated error |
| Authority laundering and judgment capture | SIT-T005, SIT-T009, SIT-T010, SIT-T011 | Attributed incident evidence versus automated ideological or intent judgments |
| Corrective-channel capture and correction sinks | SIT-T024, SIT-T034, SIT-T039 | Dependence, available authority, processing and demonstrated intervention |
| External-presence starvation | SIT-T001, SIT-T016, SIT-T029 | A documented inflow or stage failure versus a single incomplete snapshot |
| Open-input pollution | SIT-T002, SIT-T010, SIT-T016 | Provenance or attack evidence versus the mere presence of external input |
| Tail suppression | SIT-T021, SIT-T023, SIT-T032 | Observed exclusion against a known input set versus absence of a document |

The source family supports examining these failures. The final labels, conditions and detection claims belong in the later threat specification.

## 6. Formal quantities held outside the v0.1 source-profile claim

The following objects remain separately named: thermodynamic entropy; surface-language entropy; Gini-Simpson diversity; mutual information with a declared reality state; semantic gradient; stochastic mixing strength; queue utilization; capture probability; and logical conjunction of evaluation conditions.

This work unit defines no conversion among them. It does not set an entropy alarm, a collapse probability, a causal correction coefficient, a numerical P × I score or a generalized measure of model safety. Source-based mathematical results remain available for appropriately scoped later research; the required experiment cannot be supplied by renaming graph counts.

## 7. Work-unit boundary

All 40 mapping entries are submitted for review. The semantic holds and other future gating decisions are recorded in [UNRESOLVED_DECISIONS.md](UNRESOLVED_DECISIONS.md). The three Work Unit 1 files may be reviewed as one package. Product specification drafting, final ontology, public field schemas, algorithms and repository writes have not begun.
