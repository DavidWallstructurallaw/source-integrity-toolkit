# DEFINITIONS_AND_UNITS

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Target release | v0.1 |
| Phase / work unit | Phase 0 / Work Unit 4: Integrity dimensions and analytical semantics |
| Revision | 0.2 |
| Date | 2026-09-17 |
| Status | CONDITIONAL PROPOSAL FOR REVIEW: WU3 definitions retained; WU4 analytical extension submitted |
| Theory Owner | Xiangyu Guo |
| Technical Owner | Unassigned |
| Adopted input directions | SIT-D001-SIT-D018, following the user's acceptance of the Work Unit 2 recommendation package |
| Pending detailed input choices | SIT-D019-SIT-D021 |
| New analytical choices submitted | SIT-D022-SIT-D025 |
| Companion specification | `CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` revision 0.1 |
| Current register | `UNRESOLVED_DECISIONS.md` revision 0.4 |
| Added analytical scope | Sections 19-29; SIT-M001-SIT-M015 |
| Scope reserved | WU5 threats; WU6 final status/capability contract; WU7 hero; WU8 tests |
| Implementation / final Phase 0 approval | Neither is authorized by this delivery |

**Revision 0.2 reading note.** Sections 1-18 below are retained verbatim from the Work Unit 3 submission, including its historical work-unit and approval descriptions. The current Work Unit 4 proposal is §§19-29. Its adoption is conditional on the pending input choices and the new analytical decisions. The latest “继续” is recorded as authorization to draft, not as a new detailed approval. No prior file is overwritten.

## 1. Authority, provenance and reading rule

The latest instruction, “可以，继续”, follows the offer to approve the Work Unit 2 files and all enumerated recommended directions and then proceed to Work Unit 3. The active decision register records that acceptance with its exact scope. Historical Work Unit 1 and Work Unit 2 files retain their original bytes and their then-current status statements. No approval is backdated into those snapshots.

The inherited product boundary is [V0.1_PRODUCT_SPEC.md](V0.1_PRODUCT_SPEC.md). Work instructions are [PROJECT_INSTRUCTIONS.md](PROJECT_INSTRUCTIONS.md). Their acceptance establishes directions for this definition work; it does not pre-approve the exact new ontology below. MUST and MUST NOT express the submitted contract. Adoption of this unit remains subject to owner review.

The source basis remains the six supplied PDFs indexed by [SPEC_AUDIT.md](SPEC_AUDIT.md) and the forty entries in [THEORY_SOURCE_MAP.md](THEORY_SOURCE_MAP.md). Source aliases and one-based PDF page references retain their existing meanings. All exact record names, field names, enums and graph rules in these two documents are **toolkit operationalizations** unless expressly identified as source terminology. No paper is represented as having specified this JSON contract.

The unit defines a local, caller-prepared evidence dossier. It creates no parser, schema file, graph algorithm, numerical diagnostic, runtime test, live verification, network operation or corrective intervention.

### 1.1 Responsibility of the two documents

This document owns term meanings, distinctions, qualification rules and the units that must stay separate. [CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md](CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md) owns the proposed record fields, reference rules, relation registry, view construction and structural rejection behavior.

Work Unit 4 will extend this document with approved analytical formulas, denominators, allocation and comparison rules. Work Unit 6 will define the result/status envelope and capability matrix. An input-state enum in this unit is not an authorization to invent a report score or observability level.

## 2. Source concepts retained without numerical substitution

| Source concept | Meaning retained from the supplied text | Product boundary |
|---|---|---|
| Presence | Broad, living contact with reality in SIL; external reality-bearing input in UIL and EC | Record the audited boundary, time, origin and input stages. Do not infer adequate presence from document count. [SIT-T001, SIT-T016] |
| Integrity | Provenance, accountability, auditable process, manipulation resistance and disclosed conflicts in SIL | Preserve evidence for separate dimensions. Do not assign a universal integrity percentage. [SIT-T002] |
| Presence × Integrity | Joint structural requirement | No multiplication of arbitrary input-completeness and source-count percentages. [SIT-T003] |
| Evaluative independence | Lineage and validation distinctions in EC | Compare documented role and dependency relations. Shared ancestry is not a measured error-correlation coefficient. [SIT-T018, SIT-T022] |
| Type-appropriate validation | Claims answer to the kinds of constraint capable of testing them | Retain formal checks, execution, observation and human judgment as distinct recorded processes. [SIT-T020] |
| Tail and anomaly retention | Preserve consequential rare cases and anomalies that may challenge the current cut | Preserve supplied records, their context and known selection history. No automatic minority demographic inference. [SIT-T019, SIT-T021, SIT-T023] |
| Corrective capacity | Power to change a system after detecting error | Keep route, authority, handling, linked change and capacity evidence separate. [SIT-T024, SIT-T034, SIT-T039] |
| Effective replenishment | Entry, preservation, selection and downstream influence in HDL §4.6 | Four separately evidenced stages. A stage record does not manufacture evidence for another stage. [SIT-T029] |
| Entropy and formal information quantities | Source-local variables and assumptions | No entropy, mutual-information, semantic-gradient, fixation or collapse output is defined here. [SIT-T015, SIT-T027-SIT-T028, SIT-T033] |

SIL's judgment-layer requirement remains explicit: renewable human judgment cannot be replaced by repeated model judgment under a different label. A synthetic judgment is still a representable artifact. Its source, role and relevant validation remain visible. These are the adopted SIT-D002 product-use rules, preserving SIL pp. 6-7 and 14-16, EC §6 and HDL §5.5 without rewriting any of those passages.

## 3. Unit of analysis

### 3.1 Evidence bundle

An **evidence bundle** is one caller-supplied, versioned collection of inquiries, records, assertions and supporting references. It records what the caller supplies for an audit. Its size does not establish coverage of the outside world.

### 3.2 Audit snapshot

An **audit snapshot** is the immutable supplied state identified by a bundle ID and a snapshot ID. All local references resolve inside that snapshot. A later corrected dossier receives another snapshot ID. The earlier dossier remains a separate input.

A predecessor link documents chronology only. It cannot import missing records, establish byte identity, or authorize retrieval of an earlier snapshot.

### 3.3 Inquiry

An **Inquiry** identifies target claim versions, a system boundary, time, relevant evidence roles and the declared dependency dimensions being examined. A bundle may contain multiple inquiries and claims. Each analytical conclusion must retain its inquiry and claim scope.

The **system boundary** states what counts as the audited generator, retriever, corpus, evaluation process or answer system. Internal and external are meaningful only relative to that boundary. A record's presence in the input file does not make its origin internal to the audited real-world system.

### 3.4 Claim

A **Claim** is an explicitly represented statement version. It preserves its wording or an authorized locator, its scope/context and its claim family identity where supplied. The toolkit does not atomize prose or decide that two differently worded claims are equivalent.

Changing the meaning, time, population, object or asserted outcome creates a distinct claim version. A corrected claim does not overwrite the old statement. A caller may relate the versions explicitly.

### 3.5 Claim-bound evidence contribution

An **EvidenceItem** represents one contribution offered for one Claim version from one Artifact version or an explicitly unresolved artifact reference. It preserves the portion of the artifact used and its epistemic type.

The same article can produce several EvidenceItems. Two EvidenceItems pointing to one article do not constitute two documents or two observations. An EvidenceItem can support, contradict, qualify, describe or contextualize its bound claim through separate attributed assertions. No stance is inferred from the existence of the item.

Where a paragraph mixes testimony, an estimate and a judgment, the caller may separate those contributions or retain it as `unclassified` with qualifications. The toolkit cannot invent a decomposition.

**Source basis:** HDL §3.1 and §§5.4, 9.4; EC §§2, 6-7; SIT-T020, SIT-T032, SIT-T035. Exact contribution granularity is the SIT-D004/SIT-D019 operationalization.

## 4. Canonical object inventory

Twelve record kinds are proposed. Inquiry and EvidenceReference have their own top-level collections; an Assertion has its own collection and may express a relation or an assessment. They do not require an additional graph node for every descriptive label.

| Record kind | Canonical name | Owns | Cannot establish by itself |
|---|---|---|---|
| `claim` | Claim | Statement version and inquiry-relevant context | Truth or equivalence with another claim |
| `artifact` | Artifact | A represented document, dataset, answer, rubric, benchmark, result or other material version | Authentic identity, original acquisition or independence |
| `actor` | SourceActor | Person, organization, software agent or protected/unknown actor identity | Credibility, human contribution or shared content ancestry |
| `evidence_item` | EvidenceItem | One artifact contribution for one claim version | Support, originality or independence without corresponding assertions |
| `origin_event` | OriginEvent | A recorded acquisition, testimony, documentary issuance, analysis or constraint-producing activity | A universally independent root or correct observation |
| `model` | Model | A declared model instance/version and identity descriptors | Full training history or independent error behavior |
| `evaluation` | Evaluation | Candidate, reference, rubric, judge, reviewer, executor and result roles for a recorded process | Successful validation or independence of those roles |
| `correction_channel` | CorrectionChannel | Declared route, targets, owner and possible actions | Applicable authority, actual use or effective correction |
| `correction_event` | CorrectionEvent | Submission, handling or linked change in a recorded correction case | Substantive correctness of the objection or sustained capacity |
| `pipeline_record` | PipelineRecord | A scoped observation about admission, preservation, selection or influence | Unrecorded earlier stages or causal effect magnitude |
| `anomaly` | Anomaly | Original context for an unclassified or caller-labeled anomalous/contested item | Error, suppression, novelty or a new taxonomy accepted by the tool |
| `unresolved_reference` | UnresolvedReference | A known gap, protected endpoint or unexamined boundary | Number or identity of hidden origins |

### 4.1 Artifact

Artifact identity is version-specific. URLs, titles, publisher names and checksums are attributes with declared meanings. A URL may identify changing material. A checksum may establish equality of supplied bytes while leaving authorship and epistemic origin unresolved.

A dataset is an Artifact with `artifact_kind = dataset`. Benchmark, rubric, reference answer, judgment and execution result are other material kinds. A benchmark's existence does not prove deployment validity. A dataset's identity does not disclose all constituent records or acquisition processes.

### 4.2 SourceActor and roles

A SourceActor can occupy publishing, observing, generating, reviewing or administering roles. Those roles are represented in the appropriate records and relation assertions. They are not global prestige classes.

One person can be both generator and reviewer. One organization can publish separately collected observations. Two organizations can distribute one acquired record. A protected actor can retain one stable opaque ID across several artifacts without a public name.

A model's owner or provider can be an organization actor; the model is separately recorded as a Model. An organization described as a human audit institution does not automatically prove that a particular review involved a human contribution.

### 4.3 OriginEvent and Observation

An OriginEvent identifies a particular recorded process producing evidence or a constraint. `observation` and `data_collection` concern acquisition. `testimony` concerns an act of testimony. `documentary_issuance` can be the origin of evidence about what an institution stated. `analysis`, `formal_check` and `execution` represent other type-appropriate origins.

An **Observation** is the `observation` role of OriginEvent. It is not the external event itself. Several people may independently observe the same external event; a single observation may then be copied many times.

An OriginEvent may depend on other origins. Two analyses of the same data can have two analysis origins and one acquisition origin. An execution result can constrain an execution claim while sharing code, environment or instrumentation with other runs.

No OriginEvent automatically becomes a root. Root status is separately scoped in §8.

### 4.4 Evaluation and Judgment

An Evaluation preserves who or what generated a candidate, reference, rubric and judgment, which method was used, what result was produced, and any subsequent review contribution.

A **Judgment** is an Artifact with judgment content, used in an Evaluation or as an EvidenceItem. Its asserted epistemic role is separate from the origin of the text. A model-produced judgment can remain a model-produced judgment even when a human later reads it.

A **ValidationEvent** is an Evaluation with a specified validation method and an imported result. A recorded test run is not a test run performed by this toolkit. Identity/process verification additionally requires the scoped verification assessment described in the companion specification.

### 4.5 Transformation

A **Transformation** is an attributed relationship between material versions or claim-bound contributions. Summarization, translation, copying, quotation, syndication and general derivation preserve the fact of upstream dependence where asserted. Transformation metadata may identify an agent/model, method and occurrence time.

A transformed artifact may add an independently documented contribution. That contribution receives its own EvidenceItem or OriginEvent. Transformation alone supplies no such addition. An entire article's derivation history cannot silently be applied to every claim it contains.

### 4.6 ExternalReference and RootSource

An **ExternalReference** is a supporting EvidenceReference or a represented object with a separately asserted relation to the audited boundary. A remote URL is not proof of external grounding.

**RootSource** remains a claim-, dimension- and boundary-relative result role. It is not a global serialized source class or a label assigned by a missing-parent default.

## 5. Mapping the plan's candidate terminology

| Plan / earlier candidate | Submitted representation | Reason for the choice |
|---|---|---|
| Source | Artifact plus SourceActor, EvidenceItem, OriginEvent and relevant assertions | Avoid one object conflating material, identity and evidentiary origin |
| RootSource / independent root | Scoped origin-boundary and independence assessments; derived result role | Preserve evidence conditions and unknown upstream history |
| Observation | OriginEvent with `event_kind = observation` | Separate observed world event from acquisition activity |
| Claim | Claim | Retain statement and version |
| Evidence / EvidenceItem | EvidenceItem | Preserve claim-relative contribution |
| Publisher | SourceActor in a `published_by` relation | One actor can occupy several roles |
| Dataset / Benchmark | Artifact material kinds | Dataset or benchmark status does not imply a separate acquisition |
| Model | Model | Preserve model version and ancestry descriptors |
| Evaluator | Actor or Model occupying an Evaluation role | Human label and independence are separate |
| Judgment | Artifact kind `judgment` plus Evaluation role/result linkage | Preserve content, origin and use |
| Transformation | Typed relation and its transformation metadata | Avoid a second, inconsistent parent list |
| Citation | `cites` relation between Artifact versions | Citation has its own view and cannot imply support |
| LineageEdge | RelationAssertion with scope, dimension and provenance | Prevent unrestricted traversal across relation types |
| ValidationEvent | Evaluation with explicit method and result references | Preserve type-appropriate validation |
| CorrectionChannel / CorrectionEvent | Separate canonical records | Separate capability declaration from handling and change |
| ExternalReference | EvidenceReference or represented object plus externality assessment | A locator and grounding have different meanings |

This table is a product design under SIT-D019. It does not rename the source theories.

## 6. Assertions, evidence references and evidence qualification

### 6.1 Assertion

An **Assertion** is an attributed, scoped statement supplied by the caller. A RelationAssertion connects typed endpoints. An AssessmentAssertion records a qualified assessment, such as acquisition independence, coverage or authorization.

Each assertion retains its asserter or an explicit attribution gap, method, supporting EvidenceReferences, qualifications, scope, time and lifecycle. A structurally valid assertion can be inaccurate. Ingestion creates no verified fact.

### 6.2 EvidenceReference

An **EvidenceReference** points to the specific supplied record, excerpt, local material, external locator or protected attestation offered as support for an assertion. It records whether the supporting material was supplied, is locator-only, is protected, or is unavailable.

A citation to a paper in this documentation and an EvidenceReference in a future dossier have different purposes. Neither is automatically followed by the toolkit. A URL-only reference does not mean its contents were inspected. A protected attestation remains distinguishable from publicly inspectable material.

An assertion's attribution chain is metadata about the assertion. It must not create infinite validation requirements or manufacture an evidentiary origin for the target claim. Self-declarations are valid inputs, reported at their actual basis.

### 6.3 Qualification levels are descriptive

The following phrases describe available record basis, without creating a universal assurance score:

| Basis | Meaning |
|---|---|
| Supplied declaration | The caller records that an asserter made the statement; supporting material may be absent |
| Supplied documentary record | A referenced document or excerpt is supplied and its relevant location is identified; the statement remains attributed |
| Supplied upstream inference | An investigator or external system inferred the relationship; the inference and method are preserved |
| Protected attestation | A named or protected attestor makes a scope-limited assertion with disclosure limitations |
| Graph-derived finding | A later deterministic rule operates on eligible recorded relationships; it exposes its witness IDs and limitations |

These categories must not be ordered into a automatic truth ladder. A method can be weak, a document can be wrong, and an attestation can be challenged. The toolkit verifies that the supporting structure is present; semantic adequacy remains an attributed external assessment.

### 6.4 No laundering through graph computation

A path obtained from declared edges remains a path in declared relationships. Repeated traversal, several equivalent paths, or conversion to Markdown cannot promote the premises to direct observation. A result based partly on imported inferences retains that fact.

Exact serialized input basis values are in the companion specification §4. Final output status names belong to Work Unit 6.

## 7. Separate axes of classification

SIT-D011 adopts separate, provenance-bearing axes. Classifications are AssessmentAssertions, not implicit labels obtained from names, political posture or writing style.

### 7.1 Epistemic type

An EvidenceItem's declared epistemic type concerns how it is offered as evidence: measurement, testimony, documentary statement, estimate, formal derivation, execution result, analytical inference, evaluative judgment, allegation, fictional example or unclassified material.

A source may contain several types. A fictional example is representable in tests and explanation, but does not become external observation of an actual event.

### 7.2 SIL data roles

The SIL vocabulary is preserved as `surface_linguistic`, `world_model` and `judgment`. A classification uses axis `sil_data_role` and can attach more than one role to a relevant artifact or contribution. Nonexclusive role assignment is an explicit software operationalization, not an asserted rule already specified by the source paper. [SIL, pp. 6-7; SIT-T005]

### 7.3 HDL descriptive roles

HDL's terms are preserved under axis `hdl_structure_role`: `surface_linguistic_structure`, `world_structure`, `judgment_structure`. No silent equivalence map turns an HDL label into a SIL label. An external assessor can record both with qualifications. [HDL, §2, pp. 4-5]

### 7.4 SIL governance functions

Axis `sil_governance_layer` preserves `open_web`, `verified`, `contested`, `judgment`, corresponding to SIL's four-row table on p. 13. These describe different contributions and governance requirements. They are not mutually exclusive ranks.

A qualified verified-process description requires reference to an attributed identity/process verification assessment. An unsupported supplied `verified` label remains an unsupported classification. Neither supplies a truth certificate. A `judgment` governance classification retains SIL's human-judgment function; a model artifact with a data-layer judgment role does not automatically fill that function. A `contested` classification preserves the recorded dispute without adjudicating it.

### 7.5 Identity and content remain separable

A verified publisher can issue a disputed judgment. The dossier preserves the publisher verification, the contribution's epistemic type, its generation origin and the dispute simultaneously. None of those properties erases another. [SIT-T004-SIT-T006, SIT-T032]

## 8. Origins, roots and termination boundaries

### 8.1 Documented origin inventory

The inventory contains the OriginEvent records supplied for the inquiry. Calling an item an origin record describes its modeled role and provenance. It does not prove that it is the first origin anywhere or that two such records are independent.

### 8.2 Scoped origin boundary

An **origin boundary assessment** identifies where inquiry-specific tracing may stop in one dependency dimension and why. It distinguishes:

- an origin process for which relevant supporting records are supplied;
- a declared origin with limited support;
- an explicitly selected reference baseline;
- a scope cut at which earlier history was deliberately left outside the audit;
- unresolved ancestry.

Only the first two are assertions of origin. A baseline or scope cut cannot silently become an independent reality observation.

### 8.3 Required root qualification

A later root-related result must identify the inquiry, claim version, dependency dimension, eligible traversal relations, boundary assessment and relevant coverage. It must expose any active conflicting parent or identity assertion and any unresolved frontier.

No parent in the file is insufficient. The tool may say that a supplied graph path ends at a node. It may call that node a supported or declared origin boundary only with the corresponding scoped assessment. A node with known upstream acquisition dependence does not become an acquisition root by attaching another label.

A boundary assessment can intentionally stop at a baseline despite earlier history. That result must retain `reference_baseline` or `scope_cut`; it cannot be promoted to full independent-origin status.

### 8.4 Unresolved frontier

An **unresolved frontier** is a known place where further relevant tracing is unavailable, withheld, unexamined or outside the snapshot. The uncertainty may be represented by an UnresolvedReference, an explicit coverage gap or an unqualified terminal node.

One unresolved frontier may conceal many origins; several frontiers may share one origin. A finite file does not justify a finite bound on all hidden ancestors. Unknown ancestry and unknown cardinality remain separate facts. [SIT-D006; SIT-T036]

### 8.5 Mixed and multi-parent contribution

A contribution can have several relevant parents, a direct original contribution and inherited material, or an unresolved additional parent. The proposed graph retains each branch. It does not divide contribution equally among parents or count paths as evidence weight.

Work Unit 4 owns any allocation policy or concentration formula. Until that specification exists, ancestry sets and unresolved branches can be described without a derived percentage.

## 9. Independence and dependency dimensions

### 9.1 Process independence

A **process-independence assessment** is a supplied assessment about a finite, explicitly listed comparison set under one inquiry, claim scope and dependency dimension. It identifies its assessor, basis, method, unexamined dimensions and qualifications.

It does not assert universal statistical independence. It can be pairwise or setwise. A setwise process assessment is not silently inferred from pairwise statements. Independence is not transitive by default.

### 9.2 Core dependency dimensions

| Dimension | Examines | Example of a scoped dependency | Limitation |
|---|---|---|---|
| `acquisition` | Observation, collection, testimony or documentary origin | Two analyses rely on the same collection event | Shared external event alone is insufficient |
| `analytical_method` | Method, transformation procedure or analytical construction | Separately written analyses use the same supplied model/template | Different wording does not establish distinct methods |
| `model_ancestry` | Model derivation and disclosed training/material lineage | Candidate and judge derive from one recorded model ancestor | Common ancestry does not measure error correlation |
| `evaluation_rubric` | Reference, rubric and evaluator construction | Rubric and reference answer inherit one generative record | A different judge name does not remove rubric dependence |
| `organizational_control` | Ownership, operational control or recorded authority | Two source actors share a documented controller | Common control does not automatically mean copied evidence |

Additional named dimensions can be preserved in extensions as unassessed metadata. They cannot silently introduce new v0.1 traversal rules. Adding an operational dimension requires a recorded specification change.

### 9.3 Positive evidence required for an independence description

For a qualified process-independence description, the submitted contract requires:

1. At least two explicitly identified comparison members of compatible type and role.
2. A named inquiry, claim scope, dimension and comparison form.
3. A disclosed assessor or a protected attestation with its assurance limits.
4. A method explaining what independence was examined.
5. Supporting supplied material or an identified protected attestation, rather than only disconnected graph components.
6. Explicit unexamined dimensions and completeness limitations.
7. No unresolved, relevant contrary evidence that the report silently ignores.

Meeting these documentary conditions permits reporting an evidence-bearing assessment **as supplied**. It does not mean the software has independently verified the process in the world.

A declaration missing those conditions remains usable as a declaration. A document can be a relevant observation without qualifying an independent-source count. Unavailable supporting evidence must reduce the qualification rather than erase the source's existence.

### 9.4 Joint sets, identity and contradictory evidence

An assessment of acquisition independence between O1 and O2 does not imply independence between O1 and O3 because O2 and O3 were separately assessed. A same-identity assertion affecting O1 and O2 prevents their being silently treated as two distinct qualified origins until the identity question is resolved.

A shared acquisition origin is contrary to a claim of fully independent acquisition for the affected contributions, while it may coexist with independence of analytical method. Detecting such a conflict is a consistency finding about the recorded dossier. The tool preserves both assertions and their evidence.

### 9.5 Removing a recorded dependency

Deletion can remove a witness from a later snapshot, but it does not create new positive independence evidence. An independently assessed comparison still needs its own scoped records. If a predecessor was not supplied, the tool cannot know which evidence was deleted and must not claim that it compared snapshots. A supplied change history may identify removal explicitly.

### 9.6 Counts reserved for Work Unit 4

No unqualified `independent_source_count` is established here. A future count must declare a comparison set, the required dimension or dimensions, the documentary qualification, treatment of disputes and the counted unit. Counting members of a qualified process set must not be described as computing effective independent sample size or discovering all independent roots.

## 10. Evaluator lineage and human contribution

The evaluation roles `candidate`, `generator`, `reference_answer`, `rubric`, `judge`, `human_reviewer`, `executor`, `validation_environment` and `method_input` remain separately bound to their supplied objects.

A role-specific overlap finding identifies both roles, the common object or ancestor, the relation dimension and the witness records. A shared dataset reference can establish shared dataset identity at its supplied granularity; it does not necessarily establish overlapping rows. Any supplied partition descriptors must be retained.

Matching family labels can be reported as matching supplied labels. A shared model ancestor requires explicit model identities and ancestry relationships. A different provider, endpoint, family spelling or version label cannot serve as positive independence evidence.

A human review contribution requires a recorded person or protected human actor, a review activity, what was reviewed, what contribution was made and its basis. A bare `human_reviewed` label does not satisfy that description. Formal verification and execution retain their own type-appropriate contribution even when no human judgment event is recorded. [SIT-D002; SIL, pp. 14-16; EC, §6]

## 11. Externality, currency and four input stages

**Externality** is an attributed relation between an origin or contribution and the declared system boundary at the relevant time. It remains separate from the fact that an item was imported into the local audit bundle.

**Currency** concerns relevance to the inquiry's time and consequence horizon. There is no universal freshness threshold. An old original record can be suitable for a historical inquiry; a recent copy can have no independent new observation.

| Stage | Records can establish | Additional evidence still required |
|---|---|---|
| `admission` | A particular contribution entered the identified pipeline/stage | Retention, selection, use or independence |
| `preservation` | The identified distinction/contribution survived a specified transformation or storage step | Whether later ranking selected it |
| `selection` | It was selected or explicitly not selected for a specified use | Whether the final output actually used it |
| `influence` | A supplied use, linkage, comparison or experiment connects it to an output | Adequacy of continual renewal or causal effect magnitude |

The four stage names follow HDL §4.6, p. 13. Exact PipelineRecord fields are an operationalization. An `influence` record based on a usage log supports a recorded-use description. An experimental attribution remains the external investigator's claim and method. The toolkit performs no causal experiment.

An influence observation may be supplied without earlier stage logs. Preserve it with its own basis and keep the missing stages missing. Temporal and process order is examined only to the extent the recorded pipeline identifies the same run and relevant process.

## 12. Correction ontology

### 12.1 Channel

A CorrectionChannel records a possible route toward a target. Its contact locator is inert. A declared action list states what the source says the channel may do. Applicable authority requires its own scoped assessment.

### 12.2 Case, handling and change

A correction case begins with a CorrectionEvent of kind `submission`, identified as an objection, proposed correction or appeal. Later `handling` and `change` records point to that submission through `case_ref`.

Handling can include acknowledgment, review, acceptance, rejection, withdrawal or failure. A reasoned rejection demonstrates recorded handling; it does not prove that the rejection was right. Acceptance of a request does not by itself establish a changed downstream object.

A change record identifies the target before the change, the resulting target or explicit absence, the applied action, occurrence time and the supplied linkage to the case. A later unlinked edit cannot be attributed to the case merely because its timestamp is later.

### 12.3 Route, authority, observed outcome and capacity

| Concept | Minimum interpretive distinction |
|---|---|
| Declared route | A supplied route specification connects the channel to a target |
| Applicable authorized route | Target, action, time and scope match an attributed authority assessment |
| Observed handling | A process record shows how the submitted case was handled |
| Linked downstream effect | A change record links the case to identified before/after target records with its evidence |
| Sustained capacity | Separate evidence concerns throughput, workload, resources or continued performance over an identified horizon |

None of these automatically entails all the others. Missing capacity measurements do not erase a recorded individual correction. One successful correction does not establish adequate sustained capacity.

A route-search failure supports a bounded absence statement only for the relevant recorded graph and its scoped coverage. It cannot establish that no correction route exists anywhere. [EC, §7.5, p. 11; BVL, pp. 22-25; SIT-T034, SIT-T039]

### 12.4 Source return stays separate

Publisher compensation, referral and licensing return are SIL's economic source-return functions. A correction channel concerns epistemic or operational revision. A payment event is not a correction event merely because value returns to a source. Economic infrastructure remains outside this release. [SIT-T012]

## 13. Unknown, disputed, absent and inapplicable

| Condition | Meaning | Required consequence |
|---|---|---|
| Not recorded | The supplied dossier does not provide the field/history | Preserve a gap; do not assign a favorable value |
| Not examined | The investigator says the area was not inspected | Limit coverage and keep it outside affirmative qualification |
| Withheld | Relevant information exists or is referenced but disclosure is restricted | Preserve assurance limits and known common references |
| Unavailable | Material could not be supplied or accessed | Locator-only existence cannot become inspected evidence |
| Identity ambiguous | One or several modeled identities cannot be resolved | Preserve the ambiguity; do not count them as independent by default |
| Disputed | Structurally valid competing assertions challenge one another | Preserve both and limit affected results |
| Explicitly absent in a declared scope | A scoped complete enumeration or negative assessment asserts absence | Report its bounded basis; no universal absence claim |
| Not applicable | The question has no meaning under the named object/role/scope | Require a reason; do not use it as a substitute for unknown |
| Not performed | An analysis or review was not run | Do not present this as a negative finding |

`Not performed` concerns operations and future report output. It is not a replacement for an input reference or a missing object. Final report status labels remain Work Unit 6 work.

## 14. Identity, time and lifecycle

### 14.1 Identity

Snapshot-local IDs are unique opaque identifiers. The identity of an object in a snapshot is the tuple of bundle, snapshot and local ID. Identical strings in different bundles have no automatic relation.

The same URL or name under several IDs is not automatically merged. A supplied identity-match assertion makes the relationship inspectable, but v0.1 does not perform hidden entity resolution. If identity ambiguity affects a qualified count, that count must remain limited until an explicit scoped identity resolution is supplied.

An artifact's logical `work_key` and a claim's `claim_key` can connect versions descriptively. Neither collapses the versions. A `supersedes` relation records version precedence without automatically declaring the newer claim true or deleting the older evidence.

### 14.2 Time

Record separately what happened, when an artifact was published, when it was retrieved, when an assertion was made, when a review occurred and when the dossier was assembled. A bundle date cannot fill these dates.

Times use declared precision and a timezone where clock time is known. Unknown or date-only values are accepted with their limitations. Strict temporal claims require the available intervals to support the ordering. Equal or overlapping date intervals do not establish which event happened first.

### 14.3 Lifecycle

Active, withdrawn and superseded assertions remain stored. Withdrawal or supersession requires a reason/basis. It limits that assertion's use as a current positive premise while preserving history. A competing active assertion is not removed because another asserter has higher prestige or more repetitions.

An old artifact can still be the material a prior answer actually used. Later correction or supersession must not silently rewrite that historical dependence.

## 15. Counting units and denominator discipline

This section identifies units; it does not approve numerical diagnostics or weights.

| Unit | What one unit means | It cannot be substituted for |
|---|---|---|
| Artifact record | One represented material version | URL, publisher, observation or independent source |
| Locator | One recorded address/location | Distinct material version or root |
| Actor record | One represented identity | Independent acquisition or validator |
| EvidenceItem | One claim-bound contribution | Independent observation or complete artifact |
| OriginEvent | One represented evidence-producing process | Qualified independent root |
| Relation assertion | One supplied statement about an edge | Additional independent corroboration of that edge |
| Witness path | One route through eligible recorded relations | Evidence weight or new origin |
| Qualified comparison member | One object in a specific documented comparison set | Effective independent statistical sample |
| UnresolvedReference | One explicitly modeled uncertainty endpoint | One hidden source |
| Frontier occurrence | One place traversal encounters a gap | Distinct underlying hidden origin |
| Evaluation | One recorded evaluation process | Independent check |
| Correction case | One submission with associated events | Successful correction |
| Correction change record | One supplied linked action on a target | Sustained corrective capacity |
| PipelineRecord | One recorded stage observation | Full replenishment cycle |

If many assertions describe the same edge, retain all their provenance without multiplying the edge into extra independent origins. If several paths reach the same origin, retain witnessability without treating path multiplicity as additional source count.

Work Unit 4 must define assessed sets, mixed-parent treatment, unresolved contribution, allocation, zero denominators and comparability before adding percentages or concentration measures. No default equal split, HHI, reciprocal count, high/low label or finite hidden-root bound is selected here.

## 16. Normative invariants for later specifications

| Invariant | Required behavior | Basis |
|---|---|---|
| Claim separation | Each EvidenceItem binds one claim version; roles do not leak to other claims | SIT-D004; SIT-P001-P003 |
| Artifact/actor/origin separation | More publications can share one acquired record | SIT-D004-D006; SIT-P004-P007 |
| Assertion provenance | Every derived finding preserves the premise assertions and their limitations | SIT-D007; SIT-P002-P006 |
| Relation discipline | Citation, support, acquisition, ownership and correction use different views | SIT-D007; SIT-P004, SIT-P008-P010 |
| Positive independence evidence | Disconnection, recency, disagreement and names cannot establish independence | SIT-D005; SIT-P005 |
| Unknown preservation | Missing upstream references never become independent roots | SIT-D006; SIT-P006 |
| Stage separation | Input admission cannot stand for retained, selected or influential input | SIT-D008; SIT-P009 |
| Correction separation | Route, authority, handling, linked change and capacity retain distinct evidence | SIT-D009; SIT-P010 |
| Role separation | Data-layer judgment, model origin and human judgment contribution stay distinguishable | SIT-D002, SIT-D011; SIT-P008, SIT-P016 |
| Anomaly preservation | Unclassified context survives without forced taxonomy or automatic truth status | SIT-D013; SIT-P011 |
| Protected identity | Opaque identifiers can preserve common ancestry without public disclosure | SIT-D014; SIT-P014 |
| Bounded interpretation | Output remains scoped to supplied records and available coverage | SIT-D012, SIT-D018; SIT-P012-P013 |

## 17. Work Unit 3 acceptance and later gates

The companion specification provides representation witnesses for the plan's eight required ontology cases and additional boundary cases. They test the proposed meanings in prose; they are not the final hero fixtures or runtime golden outputs.

This unit supplies definitions and record semantics for SIT-D004-D007, SIT-D009, SIT-D011 and the identity portion of SIT-D014. It also instantiates the logical bundle choice in SIT-D016. The proposed design packages SIT-D019-SIT-D021 require review before they become a frozen consumer contract.

The following remain deliberately outside this unit: numerical allocation and concentration, interpretation thresholds, a global observability ladder, final analytical status names, final hero datasets, runtime budgets, export protection mechanics, licenses, dependencies, module paths and CLI/API names. Each remains at its assigned later gate. Their absence cannot be treated as permission to improvise in code.

## 18. Handoff

The three-file Work Unit 3 package consists of this document, `CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` and decision register revision 0.3. It is incremental. Assemble it alongside the accepted Work Unit 1 audit/map and Work Unit 2 product/instruction files. Use revision 0.3 as the active decision register and retain earlier deliveries as history.

No earlier file or paper is modified. No remote repository is touched. On acceptance of this unit and its submitted details, the next work unit is Work Unit 4: integrity dimensions and analytical semantics. No work in that unit or in Phase 1 is authorized by this handoff alone.

## 19. Work Unit 4 analytical contract and authorization

Sections 19-29 are the Work Unit 4 addition. Sections 1-18 retain the Work Unit 3 submission as historical definition text; references there to a future Work Unit 4 are now answered by this addition, subject to adoption. Exact ontology choices SIT-D019-SIT-D021 remain pending. The user's latest “继续” authorizes preparation of this conditional proposal; no approval of those choices is invented.

The new analytical choices are SIT-D022-SIT-D025. They specify descriptive populations, qualified comparison-set counts, nonexclusive origin incidence, one restricted concentration diagnostic, finite-cohort fractions and evidence-specific non-results. None changes `CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` revision 0.1. Adoption of a dependent analytical contract remains held until its ontology and analytical decisions are accepted.

MUST and MUST NOT below express the submitted contract. They do not assert implemented functionality. Mathematical examples are specification witnesses, not program output or empirical measurements.

### 19.1 Source-derived requirements and toolkit choices

The papers require provenance, external difference, type-appropriate validation, preservation of anomalies and the power to correct. They do not prescribe this toolkit's seed population, origin-bucket histogram, row classification, denominator or numerical thresholds. [SIT-T016-SIT-T024, SIT-T029, SIT-T035-SIT-T039]

Every diagnostic ID `SIT-M001` through `SIT-M015` introduced here is a **toolkit operationalization**. These IDs identify analytical contracts, not new theory-map entries or implementation Trace IDs. The conventional expression `sum(p_r^2)` is selected below for a deliberately narrow count-distribution summary; this selection is not a new theorem derived from UIL, SIL or EC.

No scalar in this unit estimates truth, information content, statistical independence, error correlation, effective sample size, correction causality, adequate human judgment or whole-system safety. No adverse condition can be compensated for by multiplying or averaging other dimensions. [SIT-T003, SIT-T015, SIT-T017, SIT-T025, SIT-T027-SIT-T031]

### 19.2 Two levels of exactness

A record count can be exact for a supplied set while the corresponding population in the world is unknown. A graph summary can be exact conditional on eligible assertions while those assertions remain declarations, imported inferences or protected attestations.

Every count therefore retains the counted member IDs, inquiry, claim where applicable, snapshot, view, selected dimension, time basis and premise provenance. The word `documented` means a documentary basis was supplied in the dossier, subject to §6. It never means that the toolkit authenticated the material or independently checked the external event.

### 19.3 No new executable input policy

This unit defines fixed interpretation rules over the proposed WU3 fields. It adds no JSON keys, allocation table, executable schema, plugin, source-ranking policy or general-purpose numerical configuration. Free-text `portion_note`, `scope_note`, `subset_descriptor`, capacity strings and namespaced extensions cannot be parsed into authoritative weights or hidden selection commands.

If a requested statistic requires structured information the existing contract cannot express, that statistic remains unavailable or explicitly outside v0.1. Changing the input contract requires a scoped amendment to its owning document. It must not be achieved through an output field or an undocumented extension.

## 20. Populations, units and evidence eligibility

### 20.1 Fixed populations

For one Inquiry `I` in snapshot `S`, and one Claim version `C` in its target claims, define:

- `E(I,C)`: the unique resolved EvidenceItem IDs explicitly in `I.seed_evidence_refs` whose `claim_ref` equals `C`.
- `A(I)`: the union of resolved Artifact IDs explicitly in `I.seed_artifact_refs` and resolved `artifact_ref` values of the inquiry's seed EvidenceItems.
- `A(I,C)`: the unique resolved Artifact IDs referenced by `E(I,C)`.
- `U_A(I)`: unresolved artifact-reference IDs in the same explicit source positions used to form `A(I)`.
- `N(I,C) = |E(I,C)|`: the seed-contribution denominator for the analytical profiles in §§22-24.

An artifact present only as assertion support, an ancestor or an evaluator rubric is not added to `A(I)` unless it occurs in the specified seed positions. Ancestor EvidenceItems are not added to `E(I,C)`. Repeated references to the same local ID do not add units; duplicate IDs in the input are structural errors under WU3, rather than extra observations.

`A(I)` is an inquiry inventory. Explicit seed artifacts without a claim-specific EvidenceItem remain claim-unassigned inventory. They cannot silently be assigned to every claim or added to a claim's concentration denominator. The report discloses this unassigned portion.

Different EvidenceItems can describe different contributions from the same artifact. They remain different seed units because their decomposition is supplied by the caller. No semantic deduplication, URL canonicalization, name merger or content-similarity inference is introduced. This granularity is a substantive limitation of a contribution-count statistic, and MUST accompany it.

### 20.2 Supplemental record populations

Origin inventories, evaluator profiles, correction profiles and pipeline cohorts use their own explicitly stated populations. They are never added to the seed-source total.

Relevant Evaluations are those explicitly listed in `I.target_object_refs`, or whose `target_refs` intersect an inquiry target claim, explicit target object, seed EvidenceItem or its artifact. Evaluations supplied only as supporting verification/process evidence retain that supporting role and are identified separately.

Correction cases are submissions whose targets intersect that same inquiry target population. Their handling/change records are included through exact `case_ref`. A linked change to an additional downstream target is displayed for that case, without pretending that all possible downstream targets have been enumerated.

Correction-routing results are keyed by a specific channel, target, action and applicable time. Candidate tuples come from supplied channel targets/action lists, scoped propagation/authority records and included case targets. A tuple not represented by these records is not silently invented. Missing action or target data produces an explicit gap.

Pipeline cohorts follow §26. They require an explicitly enumerated population; a complete final output list supplies no earlier intake population.

### 20.3 Views and dimension separation

Claim-origin profiles use only the view in WU3 lineage specification §10.2, with exact inquiry, Claim version and dependency dimension. The five dimensions remain `acquisition`, `analytical_method`, `model_ancestry`, `evaluation_rubric` and `organizational_control`.

A result is not duplicated into every dimension merely because the same nodes are available. The acquisition view cannot traverse a publisher, owner, citation, stance, correction or generated-by edge as an acquisition parent. Evaluation and organizational profiles have their own permitted views. Per-dimension findings remain separate even when they concern the same seed contribution.

### 20.4 Positive relations, disputed relations and basis

Eligible positive relations are structurally valid, affirmed, active, scope-compatible and type-compatible under WU3. Their supplied basis remains visible. Active denials and unresolved relevant conflicts are retained. A disputed relationship can appear as a disputed possibility; it cannot silently support an uncontested complete-origin result.

A documentary qualification requires the WU3 supporting structure: an identified asserter or protected attestor, a method, scoped supporting material or an available protected attestation, and explicit limitations. A `documented_record` label alone is insufficient. An external/local locator is inert and is not inspected merely because its `availability` field says `supplied`. A self-pointer or circular support chain cannot serve as its own sole documentary support.

An upstream inference with supplied support remains an upstream inference. Documentary presence is a structural qualification, not an ordered confidence scale. Qualification records should identify which necessary premises use declarations, documentary records, imported inferences or protected attestations.

### 20.5 Snapshot and time basis

The default structural question concerns the active assertions in the supplied snapshot. Its results must be labeled as snapshot-structural, with unknown effective times disclosed. It cannot answer a historical “as of” question by reconstructing missing lifecycle history.

A time-specific question requires evidence that the relied-on relations, coverage and authorizations apply at that time. An unknown time cannot silently satisfy a time-specific prerequisite. Contradictory ordering limits the affected result. Date-only intervals cannot be turned into fabricated instants. A source's age never creates an automatic quality adjustment.

### 20.6 Completeness is scoped evidence

A completeness prerequisite means a relevant coverage assessment is present and usable under its stated basis. It does not mean the toolkit proved that the investigator found every outside source.

For a complete claim-origin trace, coverage must address the in-scope outgoing dependency types for every seed or reached branch, including possible direct origin links and inherited contribution links. A coverage assertion scoped only to an OriginEvent does not establish complete parentage for a preceding EvidenceItem. An inquiry-scoped assessment may cover that finite view only when its declared dimensions, relation types and enumerated members actually include the required area.

Contrary active branches, unresolved in-scope omissions, unsupported coverage or an ambiguous scope do not get discarded to preserve a favorable completeness label. If the supplied structure cannot establish the required scope without interpreting free prose as a program, the complete-result prerequisite is unestablished. Positive witnesses remain reportable.

## 21. Inventory and qualified comparison counts

### 21.1 SIT-M001: Seed-source inventory

| Proposed field | Counted unit / rule | Non-result and interpretation |
|---|---|---|
| `nominal_seed_artifact_record_count` | `count(A(I))`; one resolved Artifact ID/version | Exact supplied inventory; no source-identity or independence claim |
| `unresolved_seed_artifact_reference_count` | `count(U_A(I))`; one uncertainty endpoint ID | Does not count hidden artifacts or hidden sources |
| `seed_evidence_item_count` | `N(I,C)`; one explicit contribution for C | Exact for the seed list; may exceed artifact count |
| `claim_artifact_record_count` | `count(A(I,C))` | Other claim-unassigned seed artifacts remain outside this number |
| `claim_unassigned_seed_artifact_record_count` | Explicit resolved seed Artifact IDs lacking any seed EvidenceItem binding in I | Unassigned means no represented claim binding, not irrelevant content |

If the relevant explicit set is empty, its inventory count is zero. This does not assert that the real system had zero sources. No combined `source_count` adds resolved records and unresolved endpoints into a purported real-world total.

Actor, publisher, locator and model inventories may be disclosed as separately named record inventories with their exact selected IDs. They cannot replace any field above or create an independence proxy.

### 21.2 SIT-M002: Origin and boundary inventory

For each `(I,C,dimension)`, disclose reached OriginEvent IDs and applicable boundary assessments. Distinguish `documented_origin`, `declared_origin`, `reference_baseline`, `scope_cut`, `unresolved` and unqualified terminals.

`reached_origin_record_count` counts unique OriginEvent IDs encountered in the supplied view. `documentary_origin_boundary_record_count` counts unique origins having an applicable documentary-qualified origin boundary with no unresolved contrary parent or identity assertion. A node with an in-scope upstream dependency in that dimension cannot qualify as its terminal origin merely by carrying a label.

Boundary assessment counts, origin record counts and reached baseline counts remain separate. Several assessments of O1 still describe one O1 record. Counts of documented boundary records do not imply independent acquisition or complete upstream coverage for every seed that reaches them.

If an examined recorded view contains no qualifying documentary boundary, the qualifying-record count can be zero, with its universe and gaps shown. The number of actual independent roots remains unavailable; zero documentary records cannot be relabeled zero actual roots.

### 21.3 SIT-M003: Qualified supplied process sets

Evaluate each supplied independence assessment separately. Its exact `subject_refs`, `comparison_form`, dimension, claim scope, method, evidence and unexamined dimensions define the row.

`qualified_process_set_member_count` is the number of subjects in that particular assessment when the WU3 §9.3 documentary requirements are met, its conclusion is `independent_process`, and no relevant unresolved contradiction or identity problem defeats that qualification. The result describes **members of a supplied, evidence-bearing process-independence assessment**. It does not establish universal statistical independence.

`qualified_origin_set_member_count` is available only as a further qualified field for that same assessment when every subject is an OriginEvent qualifying as a documentary origin boundary in the same `(I,C,dimension)`, and relevant tracing/coverage exposes no contrary dependency. This is the only proposed v0.1 numerical use of an independent-origin set. Its label must retain the assessment ID and dimension. The bare name `independent_source_count` is excluded.

Qualification failure makes the qualified-member field unavailable with reasons. `submitted_comparison_member_count` remains the exact size of the supplied subject list. A supplied `shared_dependency` conclusion or an unsupported independence declaration does not produce a qualified count of zero.

Pairwise assessments remain separate two-member assessments. Setwise assessments count only their listed sets. No union, transitive closure, maximal set, majority choice or summation across overlapping assessments is performed. Independent acquisition for one pair and independent methods for another cannot create a joint multi-dimensional independence total.

One documented origin without a qualifying comparison can still be useful evidence. It does not need an invented one-member independence certificate. [SIT-T020, SIT-T035-SIT-T036; SIT-D005, SIT-D022]

## 22. Origin incidence and unresolved contribution

### 22.1 SIT-M004: Claim-origin incidence profile

For each seed `e` in `E(I,C)`, preserve the set `R_e` of documentary-qualified terminal OriginEvent IDs reached through eligible uncontested paths, together with declared boundaries, baselines, scope cuts and every unresolved/conflicted branch. A positive known origin can remain in `R_e` even when another branch is unresolved. Its presence cannot make the entire row complete.

For each origin `r`, define the **recorded incidence count**:

`c_r = |{e in E(I,C) : r is in R_e}|`.

When `N > 0`, `c_r / N` may be displayed as the fraction of supplied seed contributions with that recorded origin incidence. Each seed counts at most once for an origin, regardless of how many paths reach it. With multiple origins per seed, different origin rows overlap and their fractions may sum above one.

These incidence fractions are neither attribution weights nor percentages of independent information. The report must state that they are nonexclusive. It must not normalize the column counts merely to make a pie chart or derive concentration from them.

### 22.2 Exhaustive row disposition

Each seed receives one primary analytical disposition, applied in the following precedence, with all underlying facts/flags retained:

| Disposition | Required meaning |
|---|---|
| `unresolved_or_conflicted` | A relevant gap, unsupported terminal, incomplete coverage, cycle, unresolved identity, time inconsistency or disputed dependency prevents a complete origin classification |
| `contains_baseline_or_scope_cut` | No preceding blocker, but at least one branch terminates at a declared reference baseline or intentional scope cut |
| `contains_declared_origin` | No preceding blocker, but at least one branch terminates only at a declared, non-documentary-qualified origin |
| `multiple_documented_origins` | Every relevant branch is covered and ends at a documentary-qualified origin; at least two distinct qualified origin IDs are reached |
| `single_documented_origin` | Same completeness conditions, with exactly one distinct qualified origin ID reached |

These names are proposed analytical classifications under SIT-D023, not the final report-status enum reserved for WU6. A cycle with an exit to O1 still carries unresolved cyclic dependence; it cannot become a completely resolved single-origin row by ignoring the cycle. A one-root diamond with complete supported paths can be single-origin because path multiplicity is not origin multiplicity.

Let the five disposition counts be `n_U`, `n_B`, `n_D`, `n_M` and `n_S`. They satisfy:

`n_U + n_B + n_D + n_M + n_S = N`.

For `N > 0`, `documentary_origin_resolution_fraction = (n_S + n_M) / N` summarizes the fraction of seed rows completely resolved to documentary origin boundaries in this view. It is a resolution-coverage statistic, not a source-quality percentage. The other four/five categories remain visible rather than being discarded from its denominator.

### 22.3 Multi-parent allocation policy

v0.1 records sets and incidence. It performs no default equal split, path-proportional split, author-reputation weighting, evidence-strength weighting or inferred contribution allocation for a multi-parent row.

The existing WU3 contract does not provide a structured, adopted quantitative allocation record. Free-text percentages in `portion_note` or an extension do not supply one. Such notes remain source declarations; no parser converts them into operational weights.

A complete two-parent row has **known ancestry with unallocated contribution**. A row with an unknown parent has **unresolved ancestry**, possibly with known positive origin incidences. These are different reasons for refusing a scalar concentration result. Neither erases the row or its membership in N.

### 22.4 SIT-M007: Frontier and limitation inventory

Count known uncertainty representations rather than hidden roots:

- `unresolved_frontier_reference_count`: unique UnresolvedReference IDs encountered in the selected view;
- `unqualified_terminal_record_count`: unique terminal EvidenceItem/OriginEvent IDs without an applicable qualifying boundary;
- `seed_items_with_unresolved_ancestry_count`: unique seeds whose traces have a relevant unresolved frontier or incomplete history;
- per-seed gap records: identify the endpoint or field gap, affected dimension, supporting assertions and reason.

A gap counted for two seeds need not be two hidden origins. One unresolved endpoint can conceal many origins. Missing represented endpoints also include explicit coverage gaps without an UnresolvedReference; these appear in per-seed limitations rather than disappearing from the analysis.

There is no `unknown_root_count`, finite upper bound on all hidden roots, or world-level total formed by adding these numbers to documented origins. Redaction preserves any known common opaque reference. [SIT-T036]

## 23. Restricted concentration diagnostic

### 23.1 SIT-M005: Single-origin contribution HHI

The proposed optional numerical result is `single_origin_contribution_hhi`. It is computed only for an eligible complete seed-contribution population in one `(I,C,dimension)`.

All of the following are required:

1. `N > 0` and every seed row is `single_documented_origin` under §22.2.
2. The trace, origin-boundary and relevant coverage prerequisites apply to the whole declared seed set, not a selected resolved subset.
3. Each resulting origin identity is represented unambiguously for this question. A supplied same-identity assertion linking different bucket IDs, or an unresolved alias/identity dispute, blocks the scalar until a corrected canonical representation is supplied. Even an uncontested same-identity assertion does not authorize an implicit merger; the software does not silently merge IDs.
4. The time basis is explicit. Any time-specific applicability requirement is satisfied; an untimed snapshot result does not claim historical validity.
5. Required premise qualifications and the caller-selected EvidenceItem granularity are disclosed.

Let `R` be the set of unique origin-record buckets reached by these seeds. Let `n_r` be the number of seeds whose sole qualified origin is r. Then:

`sum over r of n_r = N`,

`p_r = n_r / N`,

`single_origin_contribution_hhi = sum over r in R of p_r^2`.

One seed contribution carries one counting unit. This is a **frequency convention for represented contributions**, not equal reliability assigned to sources and not a multi-parent allocation. It does not require that the distinct buckets are independently acquired; independence is separately reported through SIT-M003.

For `K = |R| > 0`, the mathematical range for this count distribution is `1/K <= HHI <= 1`. Equality at one means all included seed contributions reach the same origin-record bucket. It supplies no truth or failure verdict. The lower endpoint is attainable when the counts are equal; integer counts may prevent equality for a particular N and K.

### 23.2 Missingness and ineligible populations

When any seed is multi-origin, declared-only, baseline-cut, unresolved or conflicted, this scalar is unavailable. The report must still show N, all disposition counts, origin incidences and the specific blockers.

The tool MUST NOT:

- compute HHI only over resolved seeds while retaining a label suggesting the full population;
- allocate a multi-origin row equally without an adopted input allocation contract;
- aggregate all unknowns into one invented origin;
- assign each unknown endpoint its own invented origin;
- normalize nonexclusive incidence counts to a distribution;
- infer weights from citation counts, stance, model confidence, names or narrative percentages;
- present a smaller HHI caused by omitted evidence as improved independence.

An explicit different Inquiry with a narrower seed population can produce its own result, but that result must identify the changed scope. It is not an automatic fallback result for the original Inquiry.

### 23.3 v0.1 scalar exclusions

The reciprocal `1/HHI`, an effective-root number, statistical effective sample size, multi-parent weighted HHI, partial-provenance HHI bounds, normalized 0-100 concentration scores and interpretation bands such as high/low/extreme are **outside the proposed v0.1 numerical contract**.

The required core remains the incidence/profile result. SIT-D023 proposes selecting this restricted HHI as an included supplementary capability: on adoption it must return a value when its prerequisites hold, or a specific non-result when they do not. It is not a silently omitted optional module. Its absence must not suppress the rest of the report. It cannot become a general source reputation field. [SIT-T017, SIT-T037; SIT-D010, SIT-D023]

## 24. Inherited contribution at the represented evidence layer

### 24.1 SIT-M006: First-step contribution profile

This diagnostic concerns the immediate, claim-scoped EvidenceItem layer, normally in `acquisition`. It does not estimate novel semantic information.

For a seed e, inspect the six permitted E-to-E transformation predicates and E-to-OriginEvent `originates_from` links in the chosen dimension. Classify the row only where the relevant immediate-link enumeration is adequately covered and uncontested:

| Class | Immediate recorded structure |
|---|---|
| `inherited_only_at_evidence_layer` | At least one eligible E-to-E transformation link and no direct E-to-OriginEvent contribution link within the complete stated immediate-link scope |
| `direct_origin_link_only` | At least one eligible direct E-to-OriginEvent link and no E-to-E transformation link within that same scope |
| `mixed_direct_and_inherited` | Both forms are present within a complete stated immediate-link scope |
| `unresolved_at_evidence_layer` | Neither form is established, enumeration is incomplete, an immediate endpoint/link is unknown or disputed, or relevant time/identity inconsistency prevents classification |

The phrase “direct origin link” refers to the serialized relation. Several seeds may link directly to the same origin, and an analysis origin can itself inherit acquisition data. Direct linkage supplies no originality, externality or independence certificate.

An explicit copy edge can support an inherited-only classification even when the ancestor's more distant origin is unknown, provided the immediate endpoint is resolved and the complete immediate-link scope and documentary conditions are satisfied. The separate root profile must still show the unknown distant origin. This illustrates why immediate inheritance and full root resolution have different prerequisites.

### 24.2 Fractions and unresolved rows

Let `D` be the inherited-only count, `O` the direct-only count, `M` the mixed count and `U` the unresolved immediate-layer count. Then `D + O + M + U = N`.

Always display all four counts and N. With `N > 0` and `U = 0`, report the exact represented-layer fraction:

`inherited_only_seed_fraction = D / N`.

With `N > 0` and `U > 0`, the point fraction is unavailable. The optional **finite-record completion interval** is:

`lower = D / N`,

`upper = (D + U) / N`.

This interval describes possible inherited-only membership of the unresolved seed rows, conditional on the existing classifications and supplied coverage. It is not a statistical confidence interval, a bound on truth, or a guarantee about inaccurate supplied assertions. Mixed rows remain mixed; they are not fractionally assigned to inherited-only. The interval preserves the full denominator and is explicitly named as a represented-layer classification interval.

With `N = 0`, all class counts are zero and every fraction/interval is unavailable for lack of a denominator. Unknown classification never becomes a negative or a favorable zero.

### 24.3 Required interpretation

The approved-plan candidate “Derivative Share” is realized narrowly as this profile and fraction. The report must use the represented-evidence-layer qualification. A derivative can preserve useful evidence; a direct contribution can be wrong. The diagnostic cannot determine whether a summary introduced a new inference, whether a source added useful context, or whether an observation was independently collected unless those facts have their own supplied records.

## 25. Evaluator, externality and corrective-independence profiles

### 25.1 SIT-M008: Role-specific evaluator overlap

For each relevant Evaluation, preserve the supplied role bindings and analyze each applicable role pair separately. Identify shared exact objects, common recorded model ancestors, shared dataset references at the supplied granularity, rubric/material derivation, organizational links and unexamined dimensions.

`shared_recorded_ancestor_count` counts unique common upstream record IDs reached by at least one eligible lineage edge from each of the two role sides in the stated view. Exact shared role-bound objects are disclosed separately, including zero-length identity matches. A one-sided ancestor/descendant relationship is also disclosed as its own relationship witness; it cannot disappear merely because it adds no strict shared-ancestor count.

`matching_family_label_count`, if displayed, is the size of the intersection of distinct nonnull, exact family-label strings on Models directly bound to each compared role. Duplicate labels count once per role pair. Missing labels remain disclosed, and a zero intersection cannot imply independent model lineage. These string matches remain outside the ancestry count. No scalar overall evaluator-independence, Jaccard score, pair percentage or error-correlation coefficient is selected.

A zero shared-ancestor count means no shared ancestor found in the eligible recorded view. Incomplete ancestry prevents translating zero into independence. Two models referencing different subsets of dataset D still share the dataset reference at that level; exact row overlap is not inferred from free-text subset descriptors.

When two validation activities necessarily inspect the same target, target identity is shown as a common target. It is not automatically counted as dependence of the validation process. Process independence is separately assessed in the relevant dimension. [EC §6; SIT-T018, SIT-T020]

### 25.2 SIT-M009: Boundary-qualified externality

For each scoped externality assessment, show its subjects, boundary inquiry, conclusion, grounding basis, relevant time and evidence. Count assessment records or unique subjects only with the selected unit stated. Several assessments for one subject do not add external inputs.

There is no universal external-presence percentage. `external`, `internal`, `mixed` and `unknown` remain attributed assessment conclusions. Contradictory conclusions for one subject remain visible rather than being tallied as multiple independent sources. A new date, remote URL, human label or admission record cannot supply the externality assessment.

The profile links externality records to stage records by exact subject identity or supplied mapping. A source can have documented admission and no externality qualification, or an externality assessment with no documented downstream use. Neither condition fills the other's gap. [SIT-T001, SIT-T016, SIT-T029]

### 25.3 SIT-M013: Corrective process and human contribution

Corrective independence uses supplied assessments and witnessable dependencies associated with the relevant Evaluation, source actor or Model. Apply SIT-M003 to each compatible comparison set rather than deriving independence from channel existence, job title or a human-reviewer label.

A human-contribution disclosure retains the human/protected-human Actor, review activity, contribution description and evidence. A fully model-produced review remains model-produced even when its text is later read by a person. A formal-check or execution record remains its own kind of constraint.

No number of model outputs is converted into units of human judgment. No human-to-model ratio is an integrity score. A human contribution with unresolved dependencies remains visible together with those dependencies. Sustained judgment renewal cannot be established by counting review records in one dossier. [SIT-T005, SIT-T011, SIT-T020]

## 26. Pipeline cohorts, retention and contested evidence

### 26.1 SIT-M010: Stage-specific finite population

A stage profile is keyed by Inquiry, `run_key`, `stage_key` and `stage`. Admission, preservation, selection and influence retain their WU3 meanings. No monotone funnel is fabricated from four unrelated logs.

To enable a finite-cohort fraction, a `coverage` assessment must satisfy all of these conditions:

- `coverage_kind = pipeline_universe`, `state = complete_for_scope` and `universe_enumerated = true`;
- its scope includes the relevant Inquiry and claims, where claim-bound subjects are involved;
- its `subject_refs` include PipelineRecord anchor(s) with exactly one unambiguous `(run_key, stage_key, stage)` target key, and no conflicting target-stage anchor;
- any additional Inquiry subject supplies context only; an unrelated subject cannot silently define a second cohort;
- `member_refs` explicitly lists the entire finite cohort as resolved EvidenceItem or Anomaly IDs;
- `omitted_refs` is empty; an omitted, unresolved or ambiguous population prevents a whole-cohort fraction;
- its method and supplied supporting records identify the eligibility boundary without asking the toolkit to derive membership from prose;
- relevant identity, time and cohort assertions are not unresolved in a way that prevents the comparison.

This is a restricted analytical profile over existing WU3 fields, not a new input record type. A valid coverage assertion that does not meet this profile remains usable for disclosure. No new cohort is guessed from `scope_note`, dates or the final answer.

If the coverage has no PipelineRecord anchor, or two possible runs/stage keys, retain the membership/coverage declaration but withhold the automatic fraction. A deliberately supplied known-empty population remains distinguishable from missing membership; where no target-stage anchor exists, no stage-specific fraction is assigned.

### 26.2 Per-member evidence partition

For the stated cohort and exact target key, inspect matching PipelineRecords for each member. All source rows and provenance remain visible. Collapse duplicate reports only for counting **cohort members**, never by deleting the records.

A member is counted as `Y` when an applicable, evidence-bearing record says `occurred` and there is no unresolved relevant contrary record. It is counted as `F` when such a record says `did_not_occur` and there is no unresolved relevant contrary record. Otherwise it is `U`, with the reason: missing record, unknown observation, unsupported assertion, conflicting observations, identity ambiguity, time uncertainty or mapping uncertainty.

A bare opposing declaration can create a relevant unresolved conflict; it is not discarded because another assertion has documentary support. An additional `unknown` observation alone does not negate a separately evidenced positive/negative observation, but it remains disclosed. Positive and negative observations for the same member/key cannot be resolved by newest-wins. Repeated attempts should use distinct stage keys if their outcomes are to be compared separately.

With cohort size `T`, `Y + F + U = T`. Member lists and classifications must accompany the counts. A `did_not_occur` observation is an attributed negative, not a fact independently established by this toolkit.

### 26.3 Stage fractions

For `T > 0` and `U = 0`, report `stage_occurrence_fraction = Y / T`.

For `T > 0` and `U > 0`, withhold the point fraction and optionally report a **finite-cohort completion interval** `[Y/T, (Y+U)/T]`. It concerns missing classifications within this stated population, conditional on the supplied evidence. It is not a confidence interval or a population estimate beyond the cohort.

For `T = 0`, cohort counts may be zero; fractions are unavailable. With no valid finite cohort, only individual stage observations and their record inventories are reported. Counts of records are not substituted for counts of unique cohort members.

Do not report `Y/(Y+F)` as if unknown members had been checked and excluded. Do not multiply stage fractions to obtain Presence, Integrity or effective replenishment.

### 26.4 Preservation versus retention transition

A preservation-stage occurrence fraction is not automatically an admission-to-output retention rate. For the restricted v0.1 transition, supply two separate coverage assessments satisfying §26.1: one anchored to admission and one to preservation or selection. They must identify the same Inquiry, run and exact baseline member-ID set; each assessment still has only one stage-key anchor. Every member must have an evidence-qualified positive admission state, and the target-stage classifications must refer to those same member IDs. Output versions can be linked in the PipelineRecords without changing the counted subject population.

When exactly one compatible baseline/target pair is established for that requested comparison, the target occurrence fraction or completion interval may also be labeled as recorded cohort retention/selection from the evidenced baseline. If several baseline keys compete, member IDs change, mapping is ambiguous, or admission is unresolved for any baseline member, withhold the transition ratio and show the separate stage profiles. Supplied cross-version mappings remain visible, but general mapping-based transition metrics are outside this restricted v0.1 rule. Free prose cannot select a pair or create a hidden transition adapter.

An output can preserve a contribution without citing its source, and a citation can exist without demonstrated use. Neither absence of a final citation nor presence of a bibliography entry supplies a preservation/influence state. A use log is reported as recorded use; an experimental attribution is reported as the external assessor's attribution, not a causal estimate performed here.

### 26.5 SIT-M014: Anomaly, contestation and tail handling

Anomaly and stance records retain their context, caller classification and provenance. No automatic classification of rarity, demographic minority, ideological position, factual correctness or suppressive intent is introduced.

SIT-M010's finite-cohort rule can be used for an explicitly supplied anomaly cohort. Its rate concerns that cohort and stage only. A final-only dossier cannot establish what vanished from the earlier universe. Without an enumerated denominator, display the supplied anomaly/contestation inventory and missing intake history rather than a tail-retention percentage.

Where a source is contested, show its origin and evidence basis alongside the contestation. Disagreement does not remove it from seed populations, count as an independent vote, or force equal evidentiary weight. WU5 retains ownership of threat-detection labels and false-positive rules. This unit does not declare suppression, censorship, capture or manipulation from a low fraction. [SIT-T019, SIT-T021, SIT-T023, SIT-T032]

## 27. Correction routes, handling and linked effects

### 27.1 SIT-M011: Reachability with action and authority

For each represented `(channel, target, action, time)` question, keep separate:

- a route in the declared correction view;
- its recorded authority/applicability at every required leg;
- absence of a recorded route within the examined supplied view;
- any limitation caused by partial route coverage, unknown authority, conflicting grants, time or target-version mismatch.

A direct channel target and a `propagates_to` chain are possibilities. Every leg of an applicable authorized route must match the requested action, exact target scope and effective time and carry the authority evidence required by the WU3 contract. An `amend` grant cannot authorize a `withdraw` action. A grant for A1 cannot be extended to A2 because both versions share a name.

Route existence uses a finite witness. The number of possible walks is not counted, especially when channels form cycles. Multiple paths do not become multiple independent corrective channels. `recorded_reachable_channel_count`, if displayed for a target/action, counts unique represented channel IDs with a qualifying declared route and retains its recorded-view meaning; an authorized-route count must be separately labeled and disclose its prerequisites.

A zero count or failed route search says that no qualifying route was recorded/found in the stated view. A stronger bounded absence description requires an appropriate complete-for-scope route assessment with evidence, and still remains conditional on that assessment. A partial graph cannot demonstrate universal impossibility. The software cannot verify a channel's institutional authority merely by reading a grant record.

No correction-reachability percentage, route-quality score, intervention probability or throughput adequacy calculation is selected for v0.1. [SIT-T024, SIT-T034, SIT-T039]

### 27.2 SIT-M012: Cases, handling and linked changes

Report each relevant correction case and its exact submission, handling and change records. Use these separate counts where appropriate:

| Field | Counted unit |
|---|---|
| `correction_case_record_count` | Unique submission IDs in the selected case population |
| `handling_event_record_count` | Unique handling-event IDs linked to those submissions |
| `linked_change_event_record_count` | Unique supplied change-event IDs linked through `case_ref` |
| `documentary_linked_change_target_count` | Unique `(case_ref, before_ref)` targets with a supplied, adequately supported before/after or explicit-removal linkage |
| `cases_with_documentary_linked_change_count` | Unique cases having at least one such linked target change |

These are record/process-evidence counts. Several handling events can belong to one case; several changes to one target do not inflate the distinct-target count. The documentary distinct-target count additionally needs a resolved before-state and a resolved after-state, or an explicit supported removal; unresolved before/after references remain visible in change-event inventories without satisfying that qualification. A resolved protected Artifact record can retain an opaque identity without public disclosure. Unknown after-state is an unresolved endpoint, not successful removal. An explicit retraction with supported absence can be represented without inventing an after artifact.

The submitted after-state need not be substantively correct to be a documented linked change. Report action, target, before/after identity and attribution basis. Authority remains a separate dimension: an observed linked change can remain visible with unknown authority, while an authorized route may have no observed use.

Outcome categories are nonexclusive inventories of records unless a separate, supported final-state designation is supplied. A case with acceptance and later failure retains both. Counts by handling outcome must not be summed as distinct cases, nor reduced with a newest-wins rule.

There is no v0.1 `correction_success_rate`, aggregate effective-correction count or verified-causality estimate. Missing change records do not imply failure, and an accepted request does not imply success. A downstream target not listed in the case or a supplied coverage population cannot be guessed from all semantically related documents.

### 27.3 Partial propagation and capacity

For a declared finite target set, show which targets have documented linked changes and which remain undocumented or disputed. Extra linked downstream targets are displayed separately rather than silently enlarging the original population. The profile can therefore say “two represented targets have linked changes; no change evidence is supplied for the third.” It cannot say “the third was not corrected” without corresponding negative evidence.

Capacity assessments preserve their imported unit, horizon, reported load, capacity and limitations. String values are not parsed into queue-utilization formulas. One case, even fully documented, does not establish continuing corrective capacity. Missing a capacity study does not erase a recorded individual correction.

Economic source return, referral credit and publisher compensation remain separate from correction. No payment record is counted as an effective epistemic correction. [SIT-T012, SIT-T024, SIT-T034]

## 28. Provenance coverage, unavailable values and numerical form

### 28.1 SIT-M015: Coverage and basis profile

Present coverage assessments separately by kind, scope, dimension and supplied state. A citation-list completeness assertion cannot fill a model-history or correction-route gap.

For a stated record population, a basis inventory may count records by `provenance.basis_kind`. For a stated unique EvidenceReference population, an availability inventory may count its `availability` values. Count each record/reference ID once in that particular population. These are metadata inventories, not independent assurance confirmations.

Supplement labels with their documentary gaps. An asserted `documented_record` whose support is locator-only appears in the declared-basis inventory and in the insufficient-support disclosures. Do not silently rewrite the caller's label; do not treat it as inspected material either.

No universal provenance-completeness percentage is defined. The only quantitative completeness-style field selected here is the specifically scoped `documentary_origin_resolution_fraction` in §22.2. It cannot substitute for process verification, identity assurance, semantic completeness, pipeline coverage or live external presence.

### 28.2 Non-result meanings

The following distinct meanings must survive later serialization:

| Meaning | Numerical treatment |
|---|---|
| Exact empty supplied inventory | Zero count with explicit counted set |
| No qualified supplied assessment | Qualified-member statistic unavailable; assessment inventory can still be zero |
| Missing/partial ancestry | Preserve positive witnesses and gaps; do not invent root totals |
| Known multiple roots, allocation unspecified | Incidence profile remains; scalar concentration unavailable |
| Disputed necessary premise | Preserve disputed records and limit the dependent statistic |
| Zero denominator | Fraction and interval unavailable, never zero or one |
| No comparable intake population | Retention transition unavailable |
| Inapplicable question | Unavailable with the structural reason; not a successful check |
| Analysis not performed | No result; distinguish this from a negative finding |
| Structurally rejected input | Validation diagnostics only; no ordinary completed analytical audit |

Where a numerical field has no valid value, its future representation is null/unavailable with a reason, rather than a numeric sentinel. Final machine state codes, JSON nesting and validation-diagnostic envelopes remain WU6 responsibilities. The exact structural rejection rules remain owned by the unchanged WU3 data specification.

### 28.3 Numbers, units and exact arithmetic contract

Counts are nonnegative integers. All denominators refer to explicit finite member sets. A fraction is stored conceptually with its integer numerator and positive denominator so that the value can be reproduced. Fractions of overlapping sets must be marked nonadditive.

For the restricted HHI, preserve `N`, every `n_r`, and the exact integer numerator `sum(n_r^2)` with denominator `N^2`. A decimal is a presentation of that rational number, not its authoritative replacement. Numerical presentation must not use NaN, infinity, negative missing-data codes or a denominator guessed from supplied list length when the actual population is unknown.

Proposed display convention: fractions are shown as numerator/denominator and, optionally, a decimal rounded to six places using decimal half-up rounding. Positive values smaller than the display resolution must retain the exact ratio, so a rounded `0.000000` cannot imply absence. No thresholds or classifications are computed from rounded text. This is a reproducibility convention under SIT-D025; field nesting remains WU6 work.

### 28.4 Comparison and aggregation rules

A numerical comparison requires matching counted unit, inquiry meaning, Claim version/meaning, dimension, traversal policy, documentary qualification, time basis, seed-selection rule, population boundary and attribution convention. Show any change in N and coverage. A change in a histogram after changing the seed set can describe that set change; it does not isolate a change in the source-generating system.

Different claims, dimensions, independently supplied assessment sets or protected/visible assurance regimes cannot be pooled into one score. Do not average per-claim HHI into project integrity, combine two pairwise counts into a jointly independent count, subtract stances as votes or multiply stage rates.

A later snapshot can expose different evidence because the dossier was corrected or expanded. If the earlier snapshot was not supplied, no historical comparison has been performed. A missing predecessor's records cannot be reconstructed through its ID.

Known missingness cannot be converted into an affirmative improvement. The toolkit cannot discover information a caller secretly omitted while falsely claiming completeness; every result retains that input limitation. This prevents an unsupported promise that structural checks make dishonest dossiers impossible.

## 29. Decision ownership and WU4 acceptance

| Decision | Contract submitted |
|---|---|
| SIT-D022 | Explicit seed populations, exact record units and counts tied to individually qualified supplied comparison sets |
| SIT-D023 | Nonexclusive origin incidence; complete/incomplete row partition; no multi-parent allocation; restricted single-origin contribution HHI; narrowly labeled inherited-only fraction |
| SIT-D024 | Stage/cohort and retention prerequisites; separate evaluator, externality, correction-route, outcome and human-contribution profiles |
| SIT-D025 | Field-specific non-results, denominator/precision/comparison rules and supplementary-scalar release boundary |

The analytical catalog and prose verification cases appear in `OBSERVABILITY_AND_REPORTING.md` revision 0.1. It covers every candidate dimension in the approved plan and identifies every scalar excluded from v0.1. The data/graph specification remains unchanged; any future requirement needing additional structured inputs must return to that document's change gate.

This revision extends definitions only. It does not finish WU5 threat rules, WU6 final statuses/levels, WU7 hero fixtures, WU8 executable tests or WU10 module architecture. All existing source, product and decision IDs retain their meanings. The full Phase 0 baseline and all implementation remain unapproved.
