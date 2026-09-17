# SOURCE_INTEGRITY_THREAT_MODEL

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Target release | v0.1 |
| Phase / work unit | Phase 0 / Work Unit 5: Threat model and failure taxonomy |
| Revision | 0.1 |
| Date | 2026-09-17 |
| Status | PROPOSED FOR REVIEW; WU3 and WU4 input contracts accepted for continued Phase 0 design |
| Theory Owner | Xiangyu Guo |
| Technical Owner | Unassigned |
| Accepted decision basis | SIT-D001-SIT-D018 directions; SIT-D019-SIT-D025 detailed contracts, as recorded in register revision 0.5 |
| New decisions | SIT-D026-SIT-D027 |
| Input contract | `CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` revision 0.1 |
| Analytical contract | `DEFINITIONS_AND_UNITS.md` revision 0.2; `OBSERVABILITY_AND_REPORTING.md` revision 0.1 |
| Product companion | `V0.1_PRODUCT_SPEC.md` revision 0.3 |
| Current outputs | This document, product revision 0.3 and decision register revision 0.5 |
| Scope reserved | WU6 final output states and capability matrix; WU7 hero; WU8 tests; WU9 security/privacy limits; WU10 architecture |
| Implementation / full Phase 0 approval | Neither is authorized by this delivery |

## 1. Purpose, authority and source basis

This document specifies which source-integrity failure conditions a future v0.1 audit can expose from a supplied local dossier, which mechanisms require an attributed external assessment, and which remain outside the release's detection capability. It covers all fourteen threat classes required by the approved plan's Work Unit 5. It also models ways the dossier, auditor or exported report can mislead its user.

The preceding handoff offered acceptance of SIT-D019-SIT-D025 and the Work Unit 4 package before this unit. The user replied “可以，继续”. Register revision 0.5 records that contextual acceptance, including the exact selected options, without backdating earlier approval. The accepted detailed inputs now govern this proposal. This event does not approve the new threat decisions, complete Phase 0 or authorize code.

`MUST` and `must` in this document express the submitted threat contract. Input records, relation types, numerical rules and documentary qualification remain owned by the accepted input and analytical documents. No threat card introduces an extra input key, canonical predicate, automatic identity merge, numerical threshold or source-trust classifier.

### 1.1 Source-derived requirements and product operationalizations

The six source IDs retain their Work Unit 1 identities and one-based PDF page locators. Source statements below are used through the existing forty-entry theory map. No current case history, market claim, standards update, empirical attack rate or named actor is independently evaluated here.

| Source basis | Requirement carried into this unit | Boundary retained |
|---|---|---|
| SIL pp. 7, 11-12 | Preserve both external presence and integrity; avoid a universal whitelist | A sparse dossier cannot establish epistemic starvation in an entire system. [SIT-T001-SIT-T004, SIT-T016] |
| SIL pp. 12-15, including the four-layer table on p. 13 | Preserve Open Web, Verified, Contested and Judgment functions and their different failure modes; keep audit and appeal possible | These are governance functions, not credibility tiers. No registry, ranking, sanitation service or appeal institution is operated here. [SIT-T006-SIT-T013] |
| UIL pp. 5-9, 15-16 | Examine repeated ancestry and the quality of external input; preserve the conditions under which concentration becomes harmful | Common ancestry and concentration alone do not establish falsehood or functional collapse. [SIT-T014-SIT-T017] |
| EC §§3.2, 6, 7 and 11 | Expose evaluator lineage; retain type-appropriate validation, anomalies and the power to correct | An overlap is not a measured error correlation. A recorded route is insufficient evidence of a completed correction. [SIT-T018-SIT-T026] |
| HDL §§4.6, 5.4-5.5, 7.2-7.3, 9 and 11 | Preserve transformation lineage, epistemic type, four replenishment stages and contestation | Surface patterns do not identify reality-information loss or successful manipulation by themselves. [SIT-T027-SIT-T032] |
| EBC pp. 3-4, 7-11; BVL pp. 22-25 | Keep descriptions separate from mechanisms; keep routing, authority and carrying capacity separate | No entropy, queueing, capture-probability or capacity-normalization engine is introduced. [SIT-T033-SIT-T034] |

The threat cards, their identifiers, evidence thresholds, output-language constraints and self-protection requirements are **toolkit operationalizations**. The papers supply the motivating mechanisms and boundaries. They do not contain the exact fourteen-card catalog or a calibrated detector for each label. [SIT-T035-SIT-T040]

The SIL p. 13 table keeps four different failure surfaces visible. Open input can carry pollution; verified processes can acquire an unwarranted aura of truth; contested material can lose its disagreement structure; judgment input can become concentrated or captured. The v0.1 treatment preserves the supplied role and evidence for each. It assigns no default trust weight to any row.

### 1.2 Allowed files and stop boundary

The WU5 write allowlist is exactly `SOURCE_INTEGRITY_THREAT_MODEL.md`, `V0.1_PRODUCT_SPEC.md` and `UNRESOLVED_DECISIONS.md`. The prior plan, papers, audit, map, instructions, definitions, lineage specification, reporting document and archives remain read-only. The new package contains only these three Markdown files.

WU5 does not finish WU6 by inventing serialized result enums or a capability-level ladder. It supplies the meanings and prerequisite obligations that WU6 must represent. It does not perform threat detection, graph traversal, source verification, live crawling, sanitation, content classification or an external security test. Written witness cases are specification examples.

## 2. System boundary, assets and possible failure agents

### 2.1 Audited system and auditor boundary

The future caller prepares one `sit-bundle/0.1` snapshot containing one or more bounded inquiries. Each inquiry identifies exact claims, versions, seeds, dependency dimensions, time and coverage. The future auditor checks that payload and derives only the permitted relationships. Its report goes back to the caller for review.

| Boundary | Permitted crossing | Information that does not acquire authority by crossing |
|---|---|---|
| External reality to caller-prepared dossier | Attributed records, supplied excerpts, observations and documented process assessments | A supplied assertion does not become independently verified reality |
| Dossier to structural validation | The canonical local JSON payload | URLs, excerpts, method text and extensions do not become executable instructions |
| Validated records to typed analysis | Eligible relations and canonical record links in their own views | A citation cannot become an acquisition edge; a label cannot create an origin |
| Graph evidence to qualified result | Scoped witnesses, comparison assessments, coverage and explicit limitations | A graph path does not authenticate its premises or prove claim truth |
| Recorded correction institution to report | Channel, authority, handling and linked-change evidence | The auditor receives no institutional intervention power |
| Result to Markdown or JSON | The same substantive result and qualifications | A concise summary cannot upgrade assurance or discard unknowns |
| Local report to another person/system | Only a separately authorized disclosure | Creating a report does not authorize publication of protected evidence |

The sole runtime evidence payload in the accepted v0.1 design is the explicit local bundle. Local and external source locators remain inert. No network-enabled mode, automatic attachment opening, remote model or live credential lookup is added here.

### 2.2 Assets the threat model protects

The protected assets are the inquiry's meaning and versions; the distinction between artifacts, contributions and origins; assertion provenance; documentary qualifications; known commonality; unknown and disputed branches; exact analytical populations and denominators; evidence of human and other type-appropriate validation; correction histories; anomaly context; protected identities; and the integrity of the report's own scope and limitations.

Availability also matters. A large or cyclic graph must not force the future system to invent completed results when processing cannot finish. Detailed resource controls remain a required WU9/WU10 design gate.

### 2.3 Failure agents and assumptions

A source publisher, upstream summarizer, model pipeline, evaluator, data exporter, dossier preparer, auditor maintainer or report consumer can introduce distortion. The same condition can arise through a mistake, a lossy export, an inherited convention, selective documentation or deliberate action. The tool does not determine motives.

Assume a caller can supply incomplete or false metadata, fabricate consistent assertions, split one real identity into several IDs, omit contradictory records, alter a claimed review history, or quote a qualified report without its limits. The local audit can expose represented contradictions and enforce its own semantic boundary. It cannot discover every omitted or coherently fabricated fact outside the supplied snapshot.

This limit is part of the product claim. A documentary-qualified result describes the evidence supplied under the contract. It is never a guarantee that the source process actually occurred as asserted.

## 3. Detection, attribution and non-results

### 3.1 Three evidentiary outputs and a separate control obligation

| Treatment | Meaning in v0.1 | Typical example |
|---|---|---|
| Derived structural observation | A deterministic consequence of eligible supplied records, with witness and scope | Two claim contributions reach the same documented acquisition origin |
| Attributed assessment or event | A caller-supplied conclusion, incident report or process outcome, displayed with its evidence and qualifications | An external evaluator reports that a particular poisoned document changed an answer |
| Limitation or unassessed mechanism | The required input, qualification or detector is absent | No intake universe is supplied, so earlier suppression cannot be assessed |
| Auditor control obligation | A design requirement on the future local implementation | Source text cannot request a network call or suppress a finding |

These descriptions are not final machine-readable status values. WU6 owns their serialization and capability treatment. Several can coexist for one target: a recorded shared-origin path, an attributed allegation of laundering and an unresolved upstream branch.

A taxonomy name such as **citation laundering**, **capture** or **starvation** is not an automatically supported verdict. A future report may associate a structural observation with a threat family only when it immediately states the narrower condition actually established. The family name cannot replace the witness or become a label on a person, publisher, institution or viewpoint.

### 3.2 Eligibility and assurance rules

A positive relationship must satisfy the lineage specification's eligibility rules: valid structure, compatible endpoints, affirmed polarity, active lifecycle, applicable inquiry/claim/dimension, and the relevant temporal interpretation. Documentary qualification uses supplied method and evidence or a qualified protected attestation; a bare `documented_record` label supplies no independent assurance.

Declaration-based and upstream-inference-based paths remain reportable with their basis. A disputed relationship remains visible as an attributed possibility. A conclusion requiring uncontested evidence cannot silently use it as an uncontested premise. An unaffected positive witness remains visible even when other branches are disputed, but it cannot certify the entire population as complete.

Missing data, supported negative observations, disputed premises, inapplicability, unperformed analysis and structural rejection retain their different meanings. “No eligible witness in this supplied view” cannot become “the threat is absent in the world.” A stronger bounded absence description requires supported complete coverage of the relevant scope, and still remains conditional on that coverage.

No global assurance recursion is required. Self-supporting or circular attestation chains are displayed as assurance limitations; the tool does not demand proof of every proof or fabricate a trusted root.

### 3.3 Minimum content of a threat-related observation

WU6 must be able to carry the threat-family reference; narrow observed condition or attributed allegation; bundle/snapshot and inquiry; exact claim/target versions; dimension and typed view; occurrence versus assertion times; finite witness and premise IDs; assertion provenance and support references; relevant population and coverage; contrary or unknown evidence; and a statement of what the observation cannot establish.

A quoted incident conclusion must retain its external assessor, target material, method, outcome record and qualification. A locator-only report remains locator-only. A supporting excerpt is supplied evidence, not proof that the toolkit fetched or authenticated the external report.

No threat total, severity score, probability, universal pass/fail, “high/low/extreme” threshold or source ranking is selected. Existing SIT-M001-SIT-M015 quantities retain their definitions. Threat-family associations are nonexclusive; one record can relate to several cards without becoming several independent incidents.

### 3.4 Mapping allegations without extending the input schema

An externally reported manipulation can use a Claim describing the allegation, an Artifact containing the report, an EvidenceItem with `allegation` or `analytical_inference`, relevant stance assertions, and an Evaluation with targets, role bindings and result artifacts when a process result is available. An unmatched concern can remain an Anomaly with original context. A dispute between assertions uses the existing `conflict` assessment.

There is no new `attack`, `incident`, `sanction`, `trusted_source` or `risk_score` record type. Caller text explaining an incident can be displayed with attribution; v0.1 does not semantically classify that prose or convert an extension's threat label into a supported finding. Unrecognized mechanisms remain visible in their supplied records without automatic assignment to a taxonomy card.

## 4. Threat catalog and capability summary

`SIT-TH001` through `SIT-TH014` identify the fourteen plan-required threat families. They do not replace product, diagnostic or implementation Trace IDs.

| ID | Plan threat family | Permitted narrow v0.1 surface | Full mechanism beyond automatic detection |
|---|---|---|---|
| SIT-TH001 | False plurality | Shared claim-origin witnesses and conflicts with supplied independence assessments | Deliberate creation of a false consensus or complete real-world root count |
| SIT-TH002 | Citation laundering | Typed citation/transformation paths, represented gaps and attribution discrepancies | Whether text strategically concealed provenance or semantically misrepresented support |
| SIT-TH003 | Syndication inflation | Supplied syndication/copy relationships and claim-specific inherited contribution | Hidden syndication or unreported new reporting |
| SIT-TH004 | Synthetic derivative inflation | Supplied model-generation and transformation lineage, retained new-origin branches | Authorship inferred from style or unsupported estimates of novel information |
| SIT-TH005 | Circular support | View-specific finite cycles and assurance-loop limitations | Falsity, deception or complete epistemic closure inferred from a cycle alone |
| SIT-TH006 | Evaluator self-validation | Role identity and model/data/rubric/control overlap with witnesses | Statistical error correlation or reviewer competence |
| SIT-TH007 | Benchmark lineage closure | Recorded benchmark/reference/rubric ancestry and evaluator reuse | Whether the task space omits deployment-relevant structures |
| SIT-TH008 | Provenance erasure | Missing/unsupported history and supplied evidence of a specific loss across versions | Hidden deletion or deliberate erasure inferred from current absence |
| SIT-TH009 | Authority laundering | Verification/classification qualification limits and explicit common-origin evidence | Ideological, rhetorical or institutional legitimacy judgments |
| SIT-TH010 | Corrective-channel capture | Disclosed process/control dependence and action-specific authority limitations | Hidden coercion, incentives, institutional capture or capacity adequacy |
| SIT-TH011 | Correction sink | Route, authority, handling and linked-effect distinctions; attributed failure evidence | No-effect conclusions from a missing change record |
| SIT-TH012 | External-presence starvation | Boundary-qualified externality and stage-specific inflow/selection evidence | System-wide adequacy of continuing reality contact |
| SIT-TH013 | Open-input pollution | Provenance limitations and attributed manipulation/poisoning reports | Active content-level injection, poisoning or deception detection |
| SIT-TH014 | Tail suppression | Preserved anomalies and documented stage exclusions under an explicit cohort | Hidden omissions, rarity or exclusion motives inferred from a final answer |

## 5. Threat cards

### 5.1 SIT-TH001: False plurality

**Source and contract basis.** SIT-T008, SIT-T016, SIT-T029, SIT-T035-SIT-T037; HDL §4.6; UIL pp. 8-9. Product SIT-P003-SIT-P007; diagnostics SIT-M001-SIT-M004, SIT-M007, SIT-M015.

**Mechanism and observable condition.** Several listed source artifacts can carry contributions from one acquisition process. In the supplied graph, two or more seed Artifact versions may bind different EvidenceItems for the same Claim and reach a common origin in the same dimension. The observable condition is shared-origin plurality. A separate contradiction may exist between that ancestry and an explicit supplied `independent_process` assessment in the same dimension.

**Minimum evidence.** Exact seed bindings, eligible EvidenceItem transformation/origin relations, any OriginEvent `depends_on` links, a scoped `origin_boundary` assessment and the qualification needed for the stated origin description. Independence-conflict reporting additionally identifies the affected assessment and its subjects. An Artifact-only citation path cannot supply claim-origin ancestry.

**v0.1 treatment.** Derive the shared-origin witness, retain distinct artifacts and contributions, and disclose unresolved alternate branches. Report an independence inconsistency only within its actual comparison and dependency dimension. Several method-independent analyses of one dataset remain method-independent assessments alongside their shared acquisition origin. The tool does not deduce statistical independence or decide truth by counting supporters.

**False-positive and missing-data controls.** Transparent reuse of a trustworthy original is ordinary shared ancestry. Two separately collected observations of the same event remain distinct unless their process dependence is documented. With no eligible shared path and incomplete history, preserve unknown ancestry; disconnected components are insufficient for an independent-source conclusion. With one known root and an unknown branch, report the known commonality without an exclusive root total or HHI.

**Required witness W5-01.** Five artifact-bound contributions have acquisition paths to O1; a sixth independently documented origin O2 is represented. The result retains the six contributions and both origin records. A benign alternative with disclosed republication gets the same narrow shared-origin observation and no accusation. Removing ancestry records changes coverage, not the obligation to provide positive independence evidence.

**Future extension.** Automatic discovery or stronger independence assessment requires a separately approved resolver, evidence model and validation plan.

### 5.2 SIT-TH002: Citation laundering

**Source and contract basis.** SIT-T008, SIT-T010, SIT-T022, SIT-T032; HDL §§5.4, 9.6; SIL pp. 11, 14. Product SIT-P003-SIT-P006, SIT-P012; diagnostics SIT-M002, SIT-M004, SIT-M007, SIT-M015.

**Mechanism and observable condition.** Repeated citation and transformation can make an original evidentiary basis difficult to inspect. v0.1 can disclose a recorded citation chain, a separately recorded derivation chain, their unresolved endpoints and any explicitly represented attribution discrepancy. Citation alone establishes a reference relationship.

**Minimum evidence.** `cites` links with Artifact versions for a citation path; claim-scoped transformation/origin assertions for an evidentiary path; supporting material and a bounded list/coverage record for any asserted omission. An allegation that a writer concealed or falsely described the source requires an attributed external assessment or supplied report. The software does not interpret the prose to discover that allegation.

**v0.1 treatment.** Keep citation and derivation witnesses in different views. Preserve the input report's laundering claim as attributed content alongside the narrower graph findings. An unresolved cited artifact remains an explicit frontier. The tool cannot fill missing source content from a URL, infer endorsement from a citation or convert several citations into independent confirmation.

**False-positive and missing-data controls.** A review article can legitimately cite another review and disclose its limitations. A source can be uncited yet still used according to an independently supplied process record. A citation list and an evidence-use history answer different questions. Without prior attribution or complete relevant coverage, current missing history is a provenance gap, not demonstrated removal.

**Required witness W5-02.** A cites B and B cites R; E_A's acquisition history is absent. Report a two-link supplied citation path with unresolved claim ancestry. Adding documented claim-specific derivation permits a separate origin result. It still does not establish concealment or intent. A correctly attributed review chain is the negative control.

**Future extension.** Semantic support checking or cross-version attribution comparison needs its own narrowly specified inputs and external validation.

### 5.3 SIT-TH003: Syndication inflation

**Source and contract basis.** SIT-T008, SIT-T029, SIT-T036-SIT-T037; HDL §§4.6, 5.2, 9.3. Product SIT-P003-SIT-P007; diagnostics SIT-M001, SIT-M004-SIT-M007.

**Mechanism and observable condition.** Republication can enlarge the visible artifact list while preserving an acquisition origin. The relevant evidence is the supplied `syndicated_from` or `copies` relation, distinguished from a shared event, publisher or citation.

**Minimum evidence.** Two or more supplied material versions and eligible transformation assertions. Claim-origin and inherited-contribution results additionally require same-Claim EvidenceItem relations in the chosen dimension. A material-level syndication link by itself supports only material-history disclosure.

**v0.1 treatment.** Retain each artifact record and the asserted republication history. Count original processes and inherited first-step contribution only under SIT-M002/SIT-M004/SIT-M006. Repeated assertions or several paths to O1 do not multiply O1. New local reporting within a republished article remains representable as its own contribution and origin.

**False-positive and missing-data controls.** Licensed, transparent republication does not become fraud. Partial republication plus a new interview need not be wholly derivative for every claim. A `portion_note` containing “half original” remains prose and supplies no operational allocation. Hidden syndication cannot be detected from an absent edge or a domain-name resemblance.

**Required witness W5-03.** Three Artifact-level syndication records disclose common material history. Without corresponding claim-bound parents, acquisition classification remains limited. Adding a new claim-specific local observation preserves that branch rather than merging all reporting into the syndicated origin.

**Future extension.** Matching undisclosed syndicated passages would require a separate similarity/discovery capability, currently excluded.

### 5.4 SIT-TH004: Synthetic derivative inflation

**Source and contract basis.** SIT-T005, SIT-T008, SIT-T014, SIT-T016, SIT-T029; SIL pp. 6-7; HDL §§4.6, 5.5. Product SIT-P003-SIT-P009, SIT-P016; diagnostics SIT-M004, SIT-M006-SIT-M010, SIT-M013.

**Mechanism and observable condition.** Model-produced summaries, paraphrases and translations can multiply artifacts while reproducing earlier source structure. The same transformation can also incorporate independent measurements or other external constraints. Both kinds of branch must survive.

**Minimum evidence.** `generated_by` or supplied transformation actor/model disclosure; applicable `summarizes`, `translates`, `derived_from` or related edges; claim-specific origins where an acquisition result is requested. Human judgment requires the actual review role, contribution and basis. A model's name or writing style cannot supply these relationships.

**v0.1 treatment.** Disclose model-mediated ancestry and immediate inheritance at the represented EvidenceItem layer. Preserve separately documented new-origin branches and externality/stage evidence. A generated artifact alone cannot be called independent or invalid. Model judgment stays model judgment; a `human_review` label without a substantive contribution cannot manufacture renewable human input.

**False-positive and missing-data controls.** Translation can improve access without creating a new observation. A synthetic report constrained by a fresh instrument record can retain that origin. Unknown generation history stays unknown. No lexical novelty, probability of synthetic authorship or amount of new knowledge is estimated.

**Required witness W5-04.** Four model summaries share one documented acquisition origin. Report shared lineage and their supplied generation history. Add a fifth model-produced artifact with a separately documented measurement and retain its new branch. Merely changing the displayed author to a human cannot create new evidence.

**Future extension.** Authorship detection, semantic novelty and synthetic-data experimentation remain outside v0.1 and cannot be introduced through this card.

### 5.5 SIT-TH005: Circular support

**Source and contract basis.** SIT-T008, SIT-T014, SIT-T018, SIT-T022, SIT-T036; EC §3.2; lineage specification §§10, 12. Product SIT-P002, SIT-P004-SIT-P006; diagnostics SIT-M004, SIT-M007, SIT-M008, SIT-M015.

**Mechanism and observable condition.** References, dependency assertions or assurance records can return to an earlier node. The resulting cycle has meaning only in the specific view and version structure where it occurs.

**Minimum evidence.** A finite closed witness composed entirely of eligible links in one specified view, with exact record and assertion IDs. An assurance-support loop uses support references; a citation cycle uses `cites`; a claim-origin cycle uses same-Claim, same-dimension dependency relations. These witness types are kept separate.

**v0.1 treatment.** Report the cycle and its premise basis. A claim-origin cycle with an exit to O1 retains O1's positive witness while keeping the affected seed `unresolved_or_conflicted`; it cannot qualify the entire row as single-origin. Self-citation is retained for citation analysis. A circular assurance chain does not become independent evidence by pointing back to itself.

**False-positive and missing-data controls.** Reciprocal literature references do not prove that the underlying observations were circular. An acyclic versioned feedback chain can revisit the same roles without revisiting the same node. Missing version detail remains a limitation. No cycle proves falsity, misconduct or complete absence of reality contact. An unknown endpoint terminates the trace rather than completing an imagined loop.

**Required witness W5-05.** E1 depends on E2, E2 on E1, and E2 also reaches O1 in the acquisition view. Report the finite cycle plus the origin witness, keep HHI unavailable for the full affected population, and preserve all records. A mutual citation pair with independent acquisition records is the benign control.

**Future extension.** Richer temporal loop analysis needs explicit version histories and a separate interpretation contract; no global all-edge cycle score is permitted.

### 5.6 SIT-TH006: Evaluator self-validation

**Source and contract basis.** SIT-T005, SIT-T011, SIT-T018, SIT-T020, SIT-T022; EC §§3.2, 5.4, 6; SIL pp. 14-16. Product SIT-P005, SIT-P008, SIT-P010; diagnostics SIT-M003, SIT-M008, SIT-M013.

**Mechanism and observable condition.** A candidate, its reference, its rubric and its judge can share documented model, data, method or control ancestry. Interface separation alone does not discharge that dependence.

**Minimum evidence.** Evaluation role bindings; generator links where the candidate is an artifact; eligible model/material/organizational relations; exact target versions and comparison dimension. A family label match remains a supplied label match. Independence uses the applicable supplied assessment and its documentary qualification.

**v0.1 treatment.** Distinguish an exact shared role object, a one-sided ancestor relationship, strict common ancestors reached from both sides, and label-only matches. Follow only the relevant view. Shared dataset D can be reported at dataset granularity even when row overlap is unknown. Role-pair observations remain separate; there is no overall evaluator-independence percentage.

**False-positive and missing-data controls.** Two independent tests must often inspect the same target. Common target identity alone does not establish dependent checking. A human reviewer can share source inputs yet perform a distinct documented review. Shared ancestry does not imply identical errors, intentional endorsement, bad performance or reviewer incompetence. Missing model ancestry prevents a zero recorded overlap from becoming independence.

**Required witness W5-06.** Candidate generator M1 and judge M2 have eligible `model_derived_from` paths to M0. Report the two role paths and shared ancestor. A separate pair of human empirical reviews of one target retains common-target disclosure without an automatic process-dependence finding. Different provider labels with missing histories remain unassessed.

**Future extension.** Error-correlation measurement, task execution and independent reviewer certification require evidence outside this release.

### 5.7 SIT-TH007: Benchmark lineage closure

**Source and contract basis.** SIT-T018-SIT-T023, SIT-T025-SIT-T026; EC §§2-5, 7, 11-12; HDL §7.3. Product SIT-P004, SIT-P008-SIT-P012; diagnostics SIT-M008-SIT-M010, SIT-M014-SIT-M015.

**Mechanism and observable condition.** New benchmark, reference or rubric versions can inherit the same generative and evaluative lineage. That topology is one observable component of evaluation closure. Whether the benchmark's structural cut is wrong requires deployment-native evidence.

**Minimum evidence.** Artifact kinds `benchmark`, `reference_answer` or `rubric`; version-specific material transformation/generation assertions; Evaluation roles; and any supplied incident, anomaly or independent-input records. A title containing “new” or a recent publication time supplies no structural-reopening evidence.

**v0.1 treatment.** Expose recorded reuse of generators, rubrics, references and evaluation processes. Show available external-input and anomaly records without inferring missing task classes. Separately identify absent or unassessed deployment evidence. No benchmark is run, capability score calculated, task taxonomy discovered or state-space recut by this tool.

**False-positive and missing-data controls.** A fixed regression test can intentionally reuse a task and remain useful for its narrow purpose. A shared rubric alone does not establish failure. An incomplete benchmark dossier cannot support a universal closed-evaluation verdict. Evidence of an external case remains visible even when benchmark ancestry is concentrated.

**Required witness W5-07.** B2 derives from B1; both have references and judges with recorded M0 ancestry. Report versioned lineage reuse. A separately recorded new incident retained in B2 is also disclosed. The graph alone cannot determine whether B2's task partition now matches deployment.

**Future extension.** Testing structural omission or reopening belongs to separately validated task/environment analysis. It cannot be silently inherited from Recursive Integrity Toolkit or StructDet-Bench.

### 5.8 SIT-TH008: Provenance erasure

**Source and contract basis.** SIT-T008, SIT-T022, SIT-T026, SIT-T032; SIL p. 14; HDL §§5.4, 9.3-9.4. Product SIT-P002-SIT-P006, SIT-P012-SIT-P014; diagnostics SIT-M002, SIT-M004, SIT-M007, SIT-M015.

**Mechanism and observable condition.** A transformation or export may omit origin, epistemic type, model lineage or revision history. Present absence and evidenced historical removal are separate conditions.

**Minimum evidence.** A present gap can be represented by Gap, UnresolvedReference, unsupported terminal or incomplete coverage. To describe a particular removal, supply exact before/after versions, the relevant transformation or change record, and evidence of which metadata was previously present and subsequently lost. The software does not scan two arbitrary prose documents to infer removal.

**v0.1 treatment.** Derive missing or unsupported provenance within the supplied contract and retain attributed evidence of historical loss. A dangling ID is a structural error rather than a valid unknown; an explicit compatible unresolved endpoint is a valid limitation. A provenance label without supplied support does not close a missing branch.

**False-positive and missing-data controls.** Privacy-preserving withholding, incomplete export and deliberate erasure can look similar in a final snapshot. Keep the recorded reason and avoid motive inference. Protected commonality remains representable through stable opaque references; disclosure limits do not automatically indicate low source integrity. A predecessor locator alone neither imports the prior snapshot nor authorizes a comparison.

**Required witness W5-08.** One final record lacks history: report the gap. A separately supplied before/after process record documents loss of a transformer reference: display that attributed loss. A protected reference preserving the known shared origin is the benign control. No case creates a fresh independent root from a blank field.

**Future extension.** Automated provenance-loss comparison would require an explicit cross-version contract and safe material processing.

### 5.9 SIT-TH009: Authority laundering

**Source and contract basis.** SIT-T004, SIT-T006, SIT-T009-SIT-T011, SIT-T032; SIL pp. 11-14; HDL §§5.3, 9.2, 9.5. Product SIT-P002, SIT-P005, SIT-P008, SIT-P016; diagnostics SIT-M003, SIT-M008, SIT-M015.

**Mechanism and observable condition.** Identity, prestige or repeated institutional citation can be treated as evidence of truth or independent confirmation. v0.1 can expose the precise scope and documentary limits of supplied verification/classification records and the actual lineage separately.

**Minimum evidence.** A `verification` assessment with its identity/process scope, Evaluation reference, reported outcome, validity window and evidence; a governance classification's verification reference where applicable; any relevant origins or independence assessments. Public prominence and organization names are inert attributes.

**v0.1 treatment.** Report an unsupported `verified` classification when its required verification basis is absent. Disclose a supported identity/process verification strictly in that scope. Preserve record-supported revocation or expiration at the relevant time. If several prestigious sources share an origin, report the ancestry without assigning a prestige multiplier. Broader rhetorical laundering claims remain attributed assessments.

**False-positive and missing-data controls.** Authentic institutional or expert evidence can be highly relevant to a claim. A valid identity check remains useful even though it does not determine substantive accuracy. Missing credentials do not disqualify a local observation. Unknown dates cannot be silently converted into a current verification. Contested status does not automatically lower integrity or mandate equal weighting.

**Required witness W5-09.** An Artifact is tagged `verified` but supplies no verification assessment: retain the label with its qualification gap. Adding a complete identity-process review changes that qualification, without creating a truth or independence badge. A supplied source-prestige label has no numerical effect.

**Future extension.** Reputation services, live credential checks, rhetorical classifiers and political or ideological rankings are outside v0.1.

### 5.10 SIT-TH010: Corrective-channel capture

**Source and contract basis.** SIT-T011, SIT-T013, SIT-T018, SIT-T024, SIT-T034, SIT-T039; EC §7.5; SIL pp. 14-15; BVL pp. 22-25. Product SIT-P005, SIT-P008, SIT-P010; diagnostics SIT-M008, SIT-M011-SIT-M013, SIT-M015.

**Mechanism and observable condition.** A reviewing or corrective process can share source, model, rubric or organizational dependence with the process under review, or lack the applicable authority needed to act. These are inspectable dependencies or authority limits; a complete institutional-capture diagnosis needs additional evidence.

**Minimum evidence.** CorrectionChannel owners and targets, Evaluation role bindings, eligible lineage/control assertions, supplied independence assessments, and target/action/time-specific authority records. Incentive, coercion or workload claims require attributed assessments and their stated evidence.

**v0.1 treatment.** Disclose common actors and recorded ancestry/control, compatible qualified process assessments, unexamined dimensions, and applicable or uncertain authority. Keep human contribution distinct from the reviewer's title. Preserve a documented correction even when the reviewer shares organizational affiliation. Capacity assessments remain attributed descriptions; their strings are not converted into utilization or a capture probability.

**False-positive and missing-data controls.** An internal review can have genuine scope, authority and effective action. Organizational commonality alone cannot establish coerced judgment or invalid correction. A separate vendor with undocumented model lineage is not automatically independent. Missing authority limits an authorized-route claim without erasing a separately supported historical change.

**Required witness W5-10.** A correction channel and generator share recorded owner S0; an accepted case also has a supported amendment. Report common control and the amendment together. An `amend` grant cannot be used to certify `withdraw` authority. Unknown reviewer ancestry remains unknown.

**Future extension.** Institutional audit, economic incentives and sustained capacity need domain-specific evidence and separate modeling approval.

### 5.11 SIT-TH011: Correction sink

**Source and contract basis.** SIT-T024, SIT-T026, SIT-T034, SIT-T039; EC §§7.5, 8; BVL pp. 22-25. Product SIT-P010, SIT-P012; diagnostics SIT-M011-SIT-M013.

**Mechanism and observable condition.** A system can accept a complaint or log a proposed correction while the relevant target remains beyond an evidenced route or action. The contract separates route, applicable authority, handling, and linked target change.

**Minimum evidence.** Exact submission, case and target/version records; route/authority evidence for a specified action and time; handling records; and any change's before/after or explicit-removal evidence. A bounded no-route statement additionally requires supported complete relevant route coverage. Missing change documentation does not establish a no-change event.

**v0.1 treatment.** Derive the available route and qualification limits; display attributed handling outcomes such as `failed` with their reasons; and count linked changes under SIT-M012's actual units. A documented failed attempt is reported as that attempt's outcome. It does not prove every correction avenue is permanently blocked. A mailbox plus acknowledgment yields contact/handling evidence only.

**False-positive and missing-data controls.** A reasoned rejection can be valid handling of an incorrect objection. Delay, missing after-state and an unlinked later edit cannot be rewritten as failure or success. For three listed target versions with two linked changes, the third remains undocumented unless explicit evidence supports a stronger statement. An unknown route and an observed change can coexist.

**Required witness W5-11.** Case K is accepted; A1 and B1 have supported linked revisions, while C1 has no change record. Report two linked targets and the undocumented C1. In a separate variant, an action-specific failure record is retained as attributed failure. Neither variant produces a correction-success rate.

**Future extension.** Live intervention, monitoring delivery, sustained throughput and causal effectiveness are separately governed capabilities.

### 5.12 SIT-TH012: External-presence starvation

**Source and contract basis.** SIT-T001, SIT-T003, SIT-T014, SIT-T016, SIT-T021, SIT-T029; SIL pp. 7, 11-12; UIL pp. 8-9; HDL §4.6. Product SIT-P006, SIT-P009, SIT-P011-SIT-P012; diagnostics SIT-M007, SIT-M009-SIT-M010, SIT-M014-SIT-M015.

**Mechanism and observable condition.** A system may reuse its lineage while independent reality-bearing contributions fail to enter, survive processing, get selected or affect an output. The observed dossier can show specific externality and stage records; it rarely establishes the entire continuing information supply.

**Minimum evidence.** Scoped `externality` assessments with grounding basis and relevant time; PipelineRecords at exact run/stage keys; and an anchored, enumerated finite cohort for a whole-cohort statement or fraction. Boundary, currency and source integrity are independently disclosed. A recent publication date or a remote source location supplies none of those conditions by itself.

**v0.1 treatment.** Show each supplied externality conclusion and separately evidenced admission, preservation, selection and influence. Within a qualified cohort, expose evidenced non-occurrences and unknown members under SIT-M010. An input with recorded admission and a recorded selection non-occurrence permits that stage-specific observation. It does not measure an adequate replenishment rate or identify system-wide starvation.

**False-positive and missing-data controls.** A narrow regression task can legitimately use fixed inputs. An older original source can be appropriate for a historical inquiry. Missing stage logs cannot be reconstructed from an output. An external source not selected in one run may still influence another process, which is outside the declared scope. No minimum external-source quota or scalar Presence threshold is selected.

**Required witness W5-12.** O_ext has grounded externality and admission records; its exact run's selection record says `did_not_occur` with evidence. Report those stages separately. A missing selection record produces an unresolved stage. A finite known cohort can support its own fractions, with no assertion about all external reality.

**Future extension.** Ongoing adequacy, renewal and structural reopening require longitudinal/domain evidence and separately approved measurement.

### 5.13 SIT-TH013: Open-input pollution

**Source and contract basis.** SIT-T002, SIT-T010, SIT-T016, SIT-T029; SIL pp. 8-14; HDL §§7.2, 9.6, 11.6. Product SIT-P006, SIT-P009, SIT-P012, SIT-P014-SIT-P016; diagnostics SIT-M007-SIT-M010, SIT-M015.

**Mechanism and observable condition.** External material can carry spoofed provenance, duplicated content, hidden instructions, poisoning or distorted judgment cues. Externality and correctness remain different questions. A reported attack effect requires more evidence than a source's openness or unusual wording.

**Minimum evidence.** For structural findings, use explicit provenance/dependency records and their limits. For an alleged or tested attack, retain the supplied report Claim/Artifact/EvidenceItem and any externally conducted Evaluation, targeted versions, method, outcome records and comparison evidence. Use the existing schema as described in §3.4.

**v0.1 treatment.** Disclose the supplied manipulation allegation and evidence as attributed material, together with independently derivable structural observations. No content detector, hidden-prompt scanner, Unicode-obfuscation classifier, authorship model, sentiment model, poisoning-success estimator or automatic topic-framing classifier is selected. Executable-looking source text stays inert regardless of whether it is recognized as an attack.

**False-positive and missing-data controls.** Legitimate quotations can contain instructions; technical documentation can include executable examples; disputed or anonymous sources can carry useful evidence. Repetition, external origin or an optimized format alone cannot produce a malicious-source finding. A report with no supplied result evidence remains an allegation, and absence of incident records means no incident evidence was provided.

**Required witness W5-13.** A supplied external report alleges that A_v2 changed an answer; its experiment result is only a locator. Preserve the allegation and missing result evidence without a tested-effect claim. A second variant supplies the external Evaluation and result records: report the external assessment, without claiming that this toolkit reproduced it. A quoted security example remains inert and unclassified.

**Future extension.** Every active manipulation detector needs an explicit input, false-positive/negative evaluation, authorization boundary and new product decision. None is smuggled into v0.1 as sanitation.

### 5.14 SIT-TH014: Tail suppression

**Source and contract basis.** SIT-T019, SIT-T021, SIT-T023, SIT-T029, SIT-T032; EC §§4.5, 7.1, 7.4; HDL §§5.4, 9.7; SIL pp. 11-14. Product SIT-P009, SIT-P011-SIT-P012; diagnostics SIT-M010, SIT-M014-SIT-M015.

**Mechanism and observable condition.** A consequential anomaly, local contradiction or contested contribution can disappear before it has a chance to challenge the represented categories. This toolkit preserves supplied context and can disclose a documented stage exclusion. It does not infer what was never in the dossier.

**Minimum evidence.** Anomaly or stance records with original context/authorized protected reference; caller-supplied comparison basis for rarity or contestation; exact PipelineRecord subjects and stage keys; and a qualified finite intake universe for any aggregate retention claim. An unclassified Anomaly need not bind a current Claim.

**v0.1 treatment.** Retain original context, caller classifications, supporting and opposing stances, and stage evidence. A documented `did_not_occur` at selection supports an attributed stage non-occurrence. A motive such as suppression remains an external assessment unless further evidence is supplied; the software does not derive it from the fraction. A general semantic change to the taxonomy is outside the contract.

**False-positive and missing-data controls.** Duplicate, irrelevant or unsupported material can legitimately be excluded. Retaining disagreement does not make each side equally strong or multiply independent votes. A final citation list does not reveal intake, selection or influence. Uncited material may have a recorded use. Missing cohort evidence disables the aggregate rate while preserving individual events.

**Required witness W5-14.** A supplied five-member anomaly cohort has three evidenced selections, one evidenced non-selection and one unresolved member. Show all five with the optional completion interval [3/5, 4/5], not 3/4. Explain the documented exclusion without assigning motive. The same final set without intake evidence yields only inventory and limitations.

**Future extension.** Automatic tail discovery, semantic-loss measurement and evaluation recutting require domain-specific validation and later scope approval.

## 6. Threats to the dossier, auditor and report

`SIT-TS001` through `SIT-TS007` identify self-protection risks. They are additional toolkit operationalizations grounded in the accepted evidence, privacy and no-score boundaries. They introduce no automatic authenticity service and no independent source of product authority. [SIT-T004, SIT-T008, SIT-T013, SIT-T022, SIT-T031, SIT-T035-SIT-T040]

### 6.1 SIT-TS001: Fabricated provenance and identity fragmentation

**Failure surface.** A preparer can fabricate an origin, assessor, attestation or separate IDs for one real source. An internally coherent fabricated dossier may satisfy every local structural check.

**Required control.** Keep all qualifications conditional on supplied evidence. Reject duplicate IDs under the existing structural rule; preserve `same_identity_as` assertions and relevant disputes without silently merging identities. A checksum identifies claimed bytes and does not establish source identity. An unsupported documentary label remains unsupported. Never count an unresolved reference as an independently established source.

**Residual limit.** Without externally supplied contradictory evidence, the auditor cannot discover arbitrary hidden identity aliases or prove that an attestation is genuine. False independence evidence can still mislead a local audit. The report must expose its asserters, methods, coverage and limits instead of offering an authenticity guarantee.

**Witness W5-15.** Three independent-looking IDs and consistent invented supporting records cannot be declared externally authenticated. Adding an explicit same-origin identity dispute limits the affected independence/concentration result while retaining the three record identities. No record-merging algorithm or live verification is introduced.

### 6.2 SIT-TS002: Population, decomposition and denominator manipulation

**Failure surface.** A caller can select favorable seeds, split one contribution into many records, omit unknown branches, or present a finite subset as the whole system. A report consumer can normalize only the well-documented rows and conceal the rest.

**Required control.** Retain exact seed/cohort membership, separate artifact/contribution/process units, full denominators and scope-specific coverage. Repeated paths never become repeated origins. SIT-M005 remains unavailable for any mixed, unresolved, disputed or otherwise ineligible full population. Evidence-bearing ratios remain conditional on their documented population.

**Residual limit.** A changed but internally consistent selected population can change a valid descriptive value. The tool has no complete outside corpus from which to detect all omitted seeds. Comparisons must disclose population and decomposition changes rather than assert real-system improvement. It does not deduplicate semantically similar contributions or infer fair weighting.

**Witness W5-16.** Removing an unresolved seventh seed can make a six-seed population eligible for the restricted scalar. The report must identify the new population and cannot treat that alone as better integrity. A two-parent seed remains unallocated even when a free-text note provides a percentage.

### 6.3 SIT-TS003: Self-certifying assurance and dispute-driven overclaim

**Failure surface.** Assertions can cite themselves, mutually certify one another or use unsupported `verified` labels. A hostile preparer can also insert a denial or dispute that blocks an otherwise qualified result, then present the blockage as proof of wrongdoing.

**Required control.** Preserve assertion provenance, finite assurance cycles and relevant conflicts. Do not elevate self-support to independent evidence. Apply disputes only to the claims, dimensions, targets and times they affect. Keep unaffected positive witnesses visible. A relevant unresolved denial may prevent an uncontested result, but it does not establish the denying party's conclusion.

**Residual limit.** The local audit cannot adjudicate every competing account or detect the intent behind a dispute. It must not introduce a reputation-based winner, newest-wins rule, global confidence deletion or an infinite proof-of-proof requirement to resolve that limit.

**Witness W5-17.** A1 uses A2 as its sole support and A2 points back to A1. Report the assurance limitation without creating two confirmations. A bare denial of an origin edge makes the affected premise contested; it cannot erase an unrelated correction record or prove that the original claim is false.

### 6.4 SIT-TS004: Data-to-control and report-content injection

**Failure surface.** A supplied excerpt, URI, path, method description, label or extension can contain instructions to execute a command, change the audit policy, remove limitations or make a report visually impersonate a trusted finding.

**Required control.** The bundle is inert evidence. Only the separately authorized invocation may select the input and output destination. Source locators cannot initiate reads or network access. Extensions cannot supply executable predicates, thresholds, independent-source flags or authority. Future report rendering must distinguish quoted input from generated findings and preserve limitations in both formats. Literal display and safe output requirements must be made concrete in WU6/WU9/WU10.

**Residual limit.** Keeping the local auditor non-agentic does not sanitize a source for a downstream model or browser. A report consumer can still reuse untrusted text unsafely. No prompt-injection classifier or secure-downstream certificate is claimed.

**Witness W5-18.** An excerpt says to mark every source independent and open a remote URL. It remains a supplied string and cannot change results or trigger a read. An extension with a purported trust flag has no core effect. This protection must not depend on detecting the text's intent.

### 6.5 SIT-TS005: Resource exhaustion and incomplete analysis presented as absence

**Failure surface.** Deep, highly branching or cyclic structures, oversized strings and large numbers of conflicting assertions can exhaust future parser, traversal or report resources. Enumerating all walks in a cyclic graph is not an acceptable completion requirement.

**Required control.** Future processing must have explicit resource limits and finite witness representations. Interrupted or unperformed work cannot be reported as a completed empty result, a zero shared-origin count or an absence of threats. Partial positive evidence must carry its non-completion limit. The existing no-salvage rule for structurally rejected input remains intact.

**Residual limit.** Byte, nesting, record, edge, traversal, witness and output limits are still WU9/WU10 decisions, with tests owned by WU8. This unit chooses no numeric budget, algorithm or performance claim.

**Witness W5-19.** A processing budget is exhausted before a route search completes. The required semantic outcome is unperformed/incomplete analysis with a reason, never “no correction route exists.” Exact serialized states are WU6 work. The case is a prose requirement, not a benchmark run.

### 6.6 SIT-TS006: Protected-source leakage and redaction-induced false independence

**Failure surface.** A report can disclose protected names, locations, distinctive excerpts or link patterns. Conversely, replacing one common protected identity with unrelated aliases can make dependence appear independent.

**Required control.** The input supports protected actors, opaque identities, scoped attestations and authorized context references. Creating the audit does not grant permission to publish those records. Where authorized commonality survives redaction, preserve it. Where disclosure would reveal too much, report the resulting analytical limitation rather than inventing independence or claiming lossless anonymization.

**Residual limit.** Graph topology itself can reveal identities. The toolkit cannot promise anonymous publication solely because names are removed. Detailed export profiles, consent, log retention and redaction policies remain WU9 work; no public export default is selected here.

**Witness W5-20.** Three contributions reference the same protected upstream ID. They preserve that shared-reference observation without a public name. If an authorized restricted export cannot reveal the linkage, the export must carry the limitation rather than replacing it with three independent origins.

### 6.7 SIT-TS007: Report laundering, replay and uncorrectable audit output

**Failure surface.** A caller can quote one scalar or a threat-family label without its qualifications, replay a report against different source versions, or treat a previous audit as independent evidence for its own premises. An incorrect audit finding may persist if it cannot be challenged.

**Required control.** Preserve bundle/snapshot identity, exact targets and populations, evidence basis, contract/version information and the same qualifications in JSON and Markdown. Never present absence of selected warnings as a truth, safety or source-authenticity certificate. A challenge to a finding can be represented using existing Claim, Artifact, Assertion, Evaluation and CorrectionEvent mechanisms; new supported evidence can be supplied for a later audit without deleting prior history.

**Residual limit.** The toolkit cannot stop an external reader from selectively quoting it and does not operate a public appeal service. A prior report is another artifact with its own lineage. Reading it does not produce a new independent observation. A current timestamp cannot refresh old evidentiary scope.

**Witness W5-21.** A report based on snapshot S1 is presented beside S2. It still describes S1. A later source-record correction can support a new scoped report; it cannot make S1's original source population disappear. A quoted HHI without population/qualification must not be reproduced as an integrity score.

## 7. Cross-threat interpretation and response boundaries

### 7.1 Composition without artificial incident multiplication

A syndicated model summary may exhibit shared acquisition, synthetic transformation and an unresolved upstream reference simultaneously. A later correction can reach one version but leave others undocumented. Each observation retains its witness and narrow meaning. The tool must not sum its associations with SIT-TH001, SIT-TH003, SIT-TH004 and SIT-TH008 into four independent attacks.

No complete route is required just to report a documentary linked change. No complete acquisition graph is required just to disclose a supplied model-family label. A globally high observability label cannot certify a field whose prerequisites are missing. These requirements carry forward the field-specific contracts rather than introducing a universal evidence ladder.

### 7.2 Coexisting positive and limiting evidence

**W5-22: Different dimensions.** Two analyses share a collection origin but have a documentary process-independence assessment for `analytical_method`. Report both. The shared-acquisition observation cannot refute a method-specific assessment merely by changing dimensions. No global independent/dependent verdict is emitted.

**W5-23: Change without known authority.** A protected process record links a submitted correction to an actual target revision; the grant window is unknown. Retain the linked-change evidence and the unknown applicability separately. A threat-family association concerning authority cannot erase the observed change or imply that it was unauthorized.

**W5-24: Finite evidence with unperformed detection.** A dossier has a complete recorded citation list and no manipulation report. The citation inventory can be complete for its declared scope. Content-level prompt-injection or poisoning detection remains unperformed because v0.1 has no such detector. “No listed incident” cannot become “safe input.”

### 7.3 Responses permitted in the release

A report can show missing prerequisites, preserve a disagreement, identify witness records, explain why a scalar is unavailable, and state what type of additional evidence would permit a stronger result. It can support a human's decision to inspect an upstream record or review a correction process.

A threat observation cannot automatically quarantine, delete, down-weight, rank, suppress, relabel, block access to or contact a source. It cannot file an appeal, modify a retriever, alter a benchmark, withdraw a model or perform a rollback. These actions belong to the broader source-governance architecture or another separately authorized system.

Structural rejection remains permitted under the accepted input contract. Rejecting duplicate keys, unknown predicates or incompatible endpoint types protects the payload's interpretability. It does not pass judgment on a source's viewpoint or on a well-formed record's truth.

### 7.4 Active detector boundary

No optional deterministic content detector is selected for v0.1 in this unit. This resolves the choice left open by the plan's threat-model paragraph at the product level. The existing structural graph, field and relationship checks remain included. They are distinct from discovering hidden instructions or deception in arbitrary source text.

A future detector would require an explicit task and material scope, exact output claim, evidence and false-positive/negative evaluation, resource limits, failure behavior, privacy review, external-call permissions where applicable, and an approved product/traceability change. No dependency, detector API or implementation phase is selected here.

## 8. Acceptance and later test obligations

### 8.1 Four-way coverage for every plan threat

Each row below is a specification obligation. Its positive column tests the named **narrow condition**, not an independently verified real-world threat. Missing and boundary inputs must retain valid unaffected observations.

| Threat | Positive witness | Negative / benign control | Missing-data control | Boundary control |
|---|---|---|---|---|
| SIT-TH001 | W5-01: several artifact-bound contributions reach one origin | Transparent reuse with no claim of independent confirmation | Incomplete origin histories yield no independent total | Same acquisition plus independent method retains both dimensions |
| SIT-TH002 | W5-02: supplied citation chain and separately evidenced derivation | Legitimately attributed review chain | Citation-only path leaves claim-origin unresolved | No automatic citation-to-support or citation-to-derivation conversion |
| SIT-TH003 | W5-03: explicit syndication links | A syndicated article adds a documented local observation | Hidden syndication is not guessed | Material-level links cannot establish every claim's inheritance |
| SIT-TH004 | W5-04: supplied model transformation and common origin | Fresh externally constrained input keeps its origin | Undisclosed generation remains unknown | A human label cannot replace documented contribution |
| SIT-TH005 | W5-05: finite typed cycle | Reciprocal citations with independent acquisitions | Unknown endpoint does not close a cycle | A cycle with an exit preserves origin evidence and unresolved row status |
| SIT-TH006 | W5-06: generator/judge paths to common model | Independent reviews inspect the same object | Missing training history leaves independence unassessed | Dataset-level commonality does not assert row overlap |
| SIT-TH007 | W5-07: recorded benchmark/rubric/evaluator reuse | Intentional narrow regression test | Missing deployment cases do not prove structural omission | Fresh publication date does not establish structural reopening |
| SIT-TH008 | W5-08: supported before/after metadata-loss account | Protected identity with preserved known commonality | Current absent history is a gap, not demonstrated erasure | Explicit unresolved endpoint is valid; dangling local ID is rejected |
| SIT-TH009 | W5-09: unsupported verification classification | Properly scoped identity/process verification | Unknown validity time does not certify current status | Verification scope never becomes truth or independent origin |
| SIT-TH010 | W5-10: common control and limited action authority | Internal review with documented amendment | Unknown reviewer/grant history stays unknown | `amend` authority cannot become `withdraw` authority |
| SIT-TH011 | W5-11: documented route/handling/effect mismatch | Reasoned rejection of an objection | Missing target change is not failed correction | Two changed targets and an undocumented third retain separate states |
| SIT-TH012 | W5-12: external admission with evidenced stage non-occurrence | Historical source appropriate to historical inquiry | Missing logs do not supply a no-input conclusion | A cohort result never claims complete system-wide renewal adequacy |
| SIT-TH013 | W5-13: attributed incident report and explicit result evidence | Legitimate quotation of security instructions | Locator-only report cannot become a reproduced attack result | No content detector means unassessed content risk, not a clean bill |
| SIT-TH014 | W5-14: evidenced exclusion in a known anomaly cohort | Exclusion with supplied legitimate process explanation | Final-only set yields no earlier suppression inference | Unknown member remains in [3/5, 4/5] rather than being dropped |

All fourteen cards specify a future-extension boundary. The seven self-protection witnesses W5-15-W5-21 and cross-threat witnesses W5-22-W5-24 add dossier/adversary and report-misuse coverage. WU7 decides the canonical hero; WU8 assigns executable tests and future implementation owners. These prose cases do not create executable fixtures or substitute for later tests.

### 8.2 Metamorphic and non-promotion requirements

The future tests must check the following transformations:

1. Adding an extra path to the same origin cannot create another origin. It may add an assurance witness whose actual basis remains visible.
2. Adding a new **seed** copy can change artifact and contribution counts, but cannot create another acquisition origin by itself. Adding a non-seed context artifact cannot silently change seed denominators.
3. Removing a known dependency cannot create positive independence evidence. If the prior snapshot is absent, the tool must not pretend to know that deletion occurred.
4. Adding a contradictory but well-formed record preserves the dispute and limits affected qualification. It cannot become proof that either party is dishonest.
5. Changing a publisher's name, prestige label or display order cannot supply different lineage or verification evidence.
6. Substituting one declared dependency dimension for another requires a new scoped result. It cannot carry over qualification automatically.
7. Replacing an unknown after-state with explicit supported removal changes correction evidence; merely leaving `after_ref` empty cannot do so.
8. Excluding an unknown cohort member cannot silently improve the original population's rate. A new population must be labeled as a changed scope.
9. A recorded downstream use without earlier logs cannot reconstruct a complete replenishment funnel.
10. A processing interruption cannot be normalized to a completed zero result. Content detection excluded from the release cannot be described as passed.
11. Renaming a model-produced judgment or quoting a prior audit cannot create a new human or independently acquired contribution.
12. Reformatting JSON results into Markdown cannot omit substantive caveats, disputed premises or unavailable analyses.

Some values legitimately depend on supplied contribution decomposition and selected population. The spec does not promise invariance under arbitrary record splitting or missing outside evidence. It requires those dependencies to remain disclosed. [SIT-D022-SIT-D025; SIT-TS001-SIT-TS002]

### 8.3 Work Unit 5 completion criteria

The proposal is complete for review when all plan threat classes have exact IDs, source/product/diagnostic mappings, observable evidence, a narrow permitted result, false-positive controls, missing-data behavior and a future capability boundary. Every threat must avoid an unconstrained LLM trust judgment and remain representable within the accepted input contract.

A card cannot be finalized by adding an input field outside the WU5 allowlist. Any need for additional schema semantics requires a registered change and a return to the responsible unit. No such input change is selected here. In particular, stronger semantic or causal allegations remain attributed records rather than new graph predicates.

## 9. Handoff, new decisions and next gate

SIT-D026 proposes the fourteen-card taxonomy, its narrow evidence-to-finding meanings, nonexclusive family associations and absence/reporting constraints. SIT-D027 proposes the seven self-protection obligations and the explicit boundary of no active content detector or automatic source intervention in v0.1. Both are submitted for acceptance in register revision 0.5.

| Following unit | Required use of this work | Work still owned there |
|---|---|---|
| WU6: observability | Preserve derived/attributed/unassessed meanings, per-field prerequisites, witness basis and incomplete-analysis behavior | Final status names, report envelope, complete capability matrix and meaning of any observability summary |
| WU7: hero | Include common origin, unknown ancestry, evaluator dependence and correction-stage contrasts without overclaim | Canonical scenario, populations and full prose golden outputs |
| WU8: validation | Cover all fourteen cards and self-protection/cross-threat witnesses | Test ownership, executable-test requirements, trace IDs and falsification plan |
| WU9: privacy/security | Carry inert content, safe output, protection and bounded-resource obligations | Exact limits, path/write controls, exports, redaction, retention and licensing |
| WU10: architecture | Preserve typed derivation and no action/network boundary | Modules, interfaces, dependency selection and bounded graph/report implementation design |
| WU11: final audit | Check cross-document consistency and all approval records | Complete Phase 0 baseline audit and owner approval packaging |

SIT-D019-SIT-D025 were accepted only in their submitted scope. WU6 may formalize those approved meanings; it cannot silently reopen numerical choices or adopt new semantic features through an output enum. If this threat proposal is accepted before WU6, its acceptance must be recorded at the next permitted opportunity without altering an out-of-allowlist file.

The next unit's allowed files are `OBSERVABILITY_AND_REPORTING.md`, `CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` and `SUCCESS_CRITERIA.md`. Updating the decision register is not automatically included in that allowlist. An acceptance note can live in an allowed file and be carried into the register when its next authorized update occurs. A genuinely new decision outside that authority requires an explicit permission or a return to an authorized unit.

This delivery stops at WU5. It does not create `PHASE_0_APPROVAL.md`, begin WU6, authorize Phase 1, modify GitHub or implement a detector.

## 10. Reviewed inputs and document checks

### 10.1 Frozen input identities

The following SHA-256 values identify the exact specification inputs read for this unit. Earlier archives and all six PDF source files retain their existing bytes. Checksums identify bytes; they do not authenticate authors or validate theory.

| Input | SHA-256 |
|---|---|
| Approved plan file | `2d97a820ae218c33cfd00dd96a762853e887f867973a2b2da0945fc4414495b1` |
| WU1 `SPEC_AUDIT.md` | `3565ab8f1b08f30e06f4983ffd26adbe8bc977b655ebf410b634918a7ae7949a` |
| WU1 `THEORY_SOURCE_MAP.md` | `015e65baf3fcad8ce78a2285df8f2de8d5b7b4cbdd347707ba3cc5d5ba46b627` |
| WU2 `PROJECT_INSTRUCTIONS.md` | `cb5cf8f4d367bceacc313189469b3327370bed0450468d62a968825fee4a7746` |
| WU3 `CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` | `8d697b6eb556bbe8476f59e48664996fe12003a42efdce179648d25d9ffb924f` |
| WU4 `DEFINITIONS_AND_UNITS.md` | `913697e733d4430a64696b36a7893fe2113da7e2cfbcadbb54247a36c1792e9d` |
| WU4 `OBSERVABILITY_AND_REPORTING.md` | `224a2db1080b69c6d359da327585abd8b035915411cd34782b7c2de90c2c29ad` |
| WU4 `V0.1_PRODUCT_SPEC.md` | `f8bdaeb179189992eba5eb3ea544a94586468670de492b77f8faa521f58455d1` |
| WU4 `UNRESOLVED_DECISIONS.md` | `d89d65beccbd59fe752d2ed9a8af37534d0c77de9d5b3b4450074afb7ce01e61` |

### 10.2 Check scope

The checks are local document-authoring and consistency checks performed by the drafting assistant. They are not independent review, scientific confirmation, runtime tests, source authentication, CI, penetration testing or measured detector accuracy.

The required checks are: exact WU5 file allowlist; preserved input hashes; retained earlier decision alternatives/recommendations; valid references to existing theory/product/diagnostic IDs; complete coverage of fourteen plan classes; distinct seven self-protection IDs and twenty-four prose witnesses; agreement with the twelve-kind/twenty-four-predicate input contract; no new numerical metric or final serialized status; Markdown structure; and ZIP content equality.

### 10.3 Delivery record

The companion product revision updates current authorization references and adds the WU5 threat-capability crosswalk without altering the sixteen product requirement identities or fifteen analytical definitions. The register preserves all prior recommendation bodies, records current acceptance of the seven detailed choices, and submits two new decisions. Historical files remain available in their original unit directories and archives.

Local check results and archive validation are completed before delivery. The next user decision concerns this WU5 submission. No new approval is inferred from the act of creating these files.
