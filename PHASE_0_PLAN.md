# PHASE_0_PLAN

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Planned repository | `source-integrity-toolkit` |
| Target release | v0.1 |
| Phase | Phase 0: Theory-to-Product Baseline |
| Status | PROPOSED FOR APPROVAL |
| Theory Owner | Xiangyu Guo |
| Technical Owner | To be assigned |
| Primary objective | Convert the source-integrity theory stack into an auditable, implementation-ready product specification without writing analytical code |
| Phase result | An approved Phase 0 specification bundle that defines product scope, ontology, lineage semantics, integrity dimensions, threat model, observability, validation, privacy, governance, repository architecture, and Phase 1 boundaries |
| Next phase after approval | Phase 1: Repository Scaffold |
| Analytical implementation during Phase 0 | Prohibited |

Phase 0 establishes what the Source Integrity Toolkit is allowed to mean before software begins to encode that meaning.

The project is intended to audit source systems, evidence chains, citations, evaluators, datasets, model lineages, and corrective paths. Its central question is whether apparent plurality corresponds to genuine independent contact with external reality, and whether a system retains a real path through which error can be detected and corrected.

Phase 0 does not create a crawler, search engine, ranking system, fact checker, trust authority, content moderation layer, benchmark engine, or universal truth score.

---

## 1. Phase 0 purpose

The Source Integrity Toolkit draws from a theory stack in which source integrity depends on continuing external presence, preserved provenance, genuine difference, independence of corrective input, and the capacity for correction to alter the downstream system.

The theory sources already establish several core constraints:

- closed recursive systems lose corrective difference and accumulate correlated error;
- nominal source count does not establish structural independence;
- external presence must contain genuine reality-bearing difference;
- provenance, epistemic status, transformation lineage, model lineage, and validation status must remain distinguishable;
- a verified source is not automatically true;
- an unverified source is not automatically worthless;
- disagreement can contain corrective information and must not be flattened into false consensus;
- open input without integrity can become a poisoning channel;
- integrity controls without sufficient presence can create epistemic starvation;
- evaluation itself can become recursively closed when generators, references, judges, and benchmarks share ancestry;
- corrective capacity requires more than observing failure; the correction path must be capable of changing the system.

Phase 0 converts those principles into a software contract.

The result must be precise enough that later implementation cannot quietly replace source independence with domain count, provenance with reputation, verification with truth, disagreement with error, or correction with passive logging.

---

## 2. Authority and theory-source order

Phase 0 uses dual authority:

1. the Theory Owner's approved product decisions;
2. the canonical theory sources.

Where a product decision has not yet been made, the theory-source map must identify the relevant source claim and create an explicit unresolved decision.

### 2.1 Primary theory sources

The Phase 0 source audit must begin with the following texts:

1. **The Source Integrity Layer: Presence × Integrity and the Governance of AI-Native Information Distribution**
   - primary product-architecture source;
   - establishes Presence × Integrity;
   - establishes open registry, provenance metadata, trust-weighted retrieval, manipulation detection, human audit nodes, source-return mechanisms, and appeals;
   - distinguishes open presence from verified process, contested evidence, and judgment input.

2. **The Universal Inbreeding Law: Closure, Diversity Loss, Correlated Error, and Integrity Decay in Self-Organizing Systems**
   - primary structural-law source;
   - establishes closure, loss of difference, inherited deviation, correlated error, external correction, and the structural role of Presence;
   - provides the rule that nominal openness is insufficient when external input is contaminated, derivative, or generated from the same closed source.

3. **Evaluation Closure: Benchmark Inbreeding and the Design of Open AI Evaluation**
   - primary evaluator-lineage and corrective-capacity source;
   - establishes external presence, source integrity, tail retention, corrective capacity, evaluator lineage, and structural reopening;
   - establishes that the relevant integrity conditions are conjunctive gates rather than interchangeable points in one aggregate score.

4. **The Heat Death of Language: Reality-Coupled Information, Semantic Gradient Collapse, and the Source Integrity of AI**
   - primary source-transformation and reality-coupling source;
   - establishes provenance preservation, source-function separation, correction, manipulation resistance, independent reality-bearing input, and the distinction between surface abundance and reality-coupled information.

5. **Entropy as a Structural Boundary Condition, Not a Causal Force**
   - background structural source;
   - supplies the boundary-condition interpretation of closed systems and external replenishment;
   - must not be converted into a causal "entropy score."

### 2.2 Secondary or adjacent theory sources

The following source may be used only where an explicit mapping is justified:

- **The Boundary Vacuum Law**
  - may inform analysis of authority capture, oversight overload, validator separation, and correction-path capture;
  - must not introduce unrelated social-system claims into the v0.1 product without a recorded product decision.

### 2.3 Conflict rule

If two theory sources appear to support incompatible software semantics:

1. record the conflict in `UNRESOLVED_DECISIONS.md`;
2. identify the exact source passages and affected product fields;
3. stop work on the affected specification;
4. obtain Theory Owner approval before proceeding.

No Phase 0 file may silently reconcile a theory conflict.

---

## 3. Product identity to be locked in Phase 0

Phase 0 must establish the following product identity as either approved or explicitly revised.

### 3.1 Proposed v0.1 identity

**Source Integrity Toolkit is a local-first analytical toolkit for representing and auditing source, evidence, claim, transformation, evaluator, dataset, model, and correction lineages.**

Its primary job is to reveal:

- false plurality;
- shared upstream ancestry;
- derivative-source inflation;
- source and evaluator lineage concentration;
- missing or unknown provenance;
- circular evidence chains;
- synthetic or model-mediated recursion;
- weak external presence;
- corrective-channel dependence;
- correction paths that exist nominally but cannot change downstream outputs;
- loss or suppression of contested, anomalous, or minority evidence;
- gaps between declared source diversity and structurally independent evidence.

### 3.2 Proposed first-domain focus

The v0.1 primary domain should be:

**AI-native evidence and provenance systems**, including:

- AI answer source sets;
- RAG evidence bundles;
- research citation bundles;
- benchmark and reference-answer provenance;
- LLM-judge and evaluator lineages;
- dataset source chains;
- model-generated or model-transformed evidence chains.

General news, OSINT, institutional evidence, and public-information auditing may be supported by the same schema where the required provenance is available, but v0.1 should not claim universal domain completeness.

### 3.3 Relationship to Recursive Integrity Toolkit

The two projects remain separate repositories and separate products.

**Source Integrity Toolkit owns:**

- claim and evidence provenance;
- source ancestry;
- independent-root analysis;
- source transformation lineage;
- evaluator and model lineage overlap;
- external-presence representation;
- corrective-channel representation;
- correction reachability;
- source-integrity observability and reporting.

**Recursive Integrity Toolkit owns:**

- recursive data-generation integrity;
- structural diversity through repeated generations;
- support loss;
- closed-resampling behavior;
- recursive system degradation across versions.

Phase 0 may define a future interoperability boundary. It must not create a shared package, shared runtime dependency, or shared internal codebase.

---

## 4. Phase boundary

### 4.1 Allowed work

Phase 0 may produce specification and planning documents only.

Allowed activities include:

- theory audit;
- theory-to-product mapping;
- terminology definition;
- ontology design;
- graph-semantics design;
- metric and diagnostic definitions;
- observability classification;
- input and output contract design;
- threat-model design;
- hero-case design;
- falsification criteria;
- privacy and data-handling rules;
- licensing decisions;
- future repository architecture;
- dependency strategy;
- validation planning;
- governance and approval procedures.

### 4.2 Forbidden work

Phase 0 must not create:

- production source code;
- Python packages;
- CLI implementation;
- JSON Schema files;
- database migrations;
- crawlers;
- web fetchers;
- browser automation;
- live-source verification;
- search APIs;
- trust-ranking algorithms;
- automated source reputation scores;
- fact-checking classifiers;
- semantic similarity systems;
- near-duplicate models;
- LLM-based lineage inference;
- LLM judges;
- embedding pipelines;
- source-quality models;
- prompt-injection detectors;
- RAG-poisoning detectors;
- external API integrations;
- GitHub Actions workflows;
- package metadata;
- runtime dependencies;
- dashboards;
- HTML applications;
- source registries;
- publisher payment or source-return infrastructure.

### 4.3 Prohibited semantic shortcuts

Phase 0 must explicitly prohibit the following substitutions:

- source count as source independence;
- domain count as source independence;
- publisher count as observation count;
- citation count as evidence strength;
- verified identity as truth;
- institutional prestige as epistemic correctness;
- disagreement as low integrity;
- consensus as independence;
- recency as external presence;
- human authorship as external grounding;
- synthetic authorship as automatic invalidity;
- unknown provenance as independent provenance;
- missing lineage as a root source;
- a logged correction as effective corrective capacity;
- a human reviewer as an independent reviewer without lineage evidence;
- a different model endpoint as an independent evaluator without model-lineage evidence;
- a universal integrity score as a substitute for an integrity profile.

---

## 5. Core design rules Phase 0 must settle

The following rules are proposed as mandatory v0.1 design principles.

### Rule 1: Independence is claim-relative

A document or publisher is not globally "independent."

Independence must be evaluated relative to a specific claim, observation, evidence unit, or evaluative judgment.

The same source may be an original observation for one claim and a derivative source for another.

### Rule 2: Unknown ancestry remains unknown

When an upstream lineage cannot be resolved, the toolkit must represent uncertainty.

It must not convert missing provenance into independence.

### Rule 3: Identity verification remains separate from epistemic integrity

A verified source identity means the system has stronger evidence about who produced or published an artifact.

It does not establish that the claim is true.

### Rule 4: Source type remains separate from integrity

Primary, secondary, institutional, local, human, synthetic, model-generated, and anonymous are descriptive source properties.

No type receives automatic truth status.

### Rule 5: Transformations preserve ancestry unless genuine new evidence enters

Summarization, translation, syndication, paraphrase, formatting, model rewriting, and citation laundering do not create a new independent root by themselves.

A transformation may create a new artifact while preserving the upstream evidentiary lineage.

### Rule 6: Genuine external presence requires external difference

External presence must identify input capable of carrying information not generated by the current closed lineage.

A newly published derivative copy of an existing source does not automatically increase presence.

### Rule 7: Multiple independent observations may disagree

Independent evidence need not converge.

The toolkit must preserve independent disagreement as an observed structure.

### Rule 8: Correction requires reachability

A corrective channel is structurally meaningful only when a detected correction can reach and alter the relevant downstream object, decision, score, answer, dataset, benchmark, or deployment state.

### Rule 9: Correction independence must be inspectable

A reviewer, judge, benchmark, or audit node may share lineage with the object it evaluates.

The toolkit must be capable of representing that overlap.

### Rule 10: Integrity is reported as a profile

v0.1 should report multiple dimensions and unresolved uncertainty.

A single universal Source Integrity Score is prohibited unless a future phase separately justifies and approves one.

---

## 6. Proposed Phase 0 deliverable bundle

Phase 0 should produce the following specification files.

```text
PHASE_0_PLAN.md
SPEC_AUDIT.md
THEORY_SOURCE_MAP.md
UNRESOLVED_DECISIONS.md
PROJECT_INSTRUCTIONS.md
V0.1_PRODUCT_SPEC.md
DEFINITIONS_AND_UNITS.md
CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md
SOURCE_INTEGRITY_THREAT_MODEL.md
OBSERVABILITY_AND_REPORTING.md
THEORY_TO_CODE_TRACEABILITY.md
VALIDATION_PLAN.md
PRIVACY_AND_DATA_HANDLING.md
LICENSING_NOTES.md
SUCCESS_CRITERIA.md
GOVERNANCE_AND_HANDOFF.md
REPOSITORY_ARCHITECTURE.md
DEPENDENCY_STRATEGY.md
```

After explicit Theory Owner approval, create:

```text
PHASE_0_APPROVAL.md
```

`PHASE_0_APPROVAL.md` is an approval artifact. It is not created as a substitute for approval.

---

## 7. Work sequence

Phase 0 should be completed in eleven controlled work units.

Each work unit has:

- an objective;
- an allowed file set;
- required decisions;
- acceptance criteria;
- a stop condition.

No later work unit may silently repair an unresolved blocker from an earlier unit.

---

## 8. Work Unit 1: Theory audit and source map

### Objective

Extract the product-relevant claims from the canonical theory stack and separate:

- direct theory claims;
- mathematical results inherited from cited literature;
- proposed toolkit operationalizations;
- open empirical questions;
- governance proposals;
- claims that should remain outside v0.1.

### Allowed files

```text
SPEC_AUDIT.md
THEORY_SOURCE_MAP.md
UNRESOLVED_DECISIONS.md
```

### `SPEC_AUDIT.md` must identify

- each canonical source;
- source version or date where available;
- theory claims relevant to the toolkit;
- repeated claims across papers;
- apparent conflicts;
- undefined terms;
- claims that need software operationalization;
- claims that should remain non-computational;
- claims that require explicit domain evidence;
- candidate v0.1 and post-v0.1 boundaries.

### `THEORY_SOURCE_MAP.md` must assign stable Theory Map IDs

Recommended form:

```text
SIT-T001
SIT-T002
...
```

Each entry should include:

- theory statement;
- source title;
- source location;
- product implication;
- proposed software owner;
- status;
- limits;
- whether the mapping is direct or an operationalization.

### `UNRESOLVED_DECISIONS.md` must contain

- decision ID;
- question;
- alternatives;
- recommended option;
- affected theory IDs;
- affected future public fields;
- downstream consequences;
- approval status.

### Acceptance criteria

- every v0.1 feature idea can point to at least one theory source or be marked as a toolkit operationalization;
- no operationalization is presented as if it appeared directly in the theory;
- no theory claim is converted into a software metric without stating assumptions;
- no unresolved conflict is hidden.

### Stop condition

Stop if the project cannot distinguish a direct theory requirement from a proposed product convention.

---

## 9. Work Unit 2: Product boundary and v0.1 contract

### Objective

Define exactly what the first usable release audits.

### Allowed files

```text
V0.1_PRODUCT_SPEC.md
PROJECT_INSTRUCTIONS.md
UNRESOLVED_DECISIONS.md
```

### Required decisions

Phase 0 must decide:

1. primary v0.1 user;
2. primary v0.1 workflow;
3. accepted input modes;
4. required provenance completeness;
5. supported claim and evidence granularity;
6. graph scope;
7. supported evaluator/model lineage representation;
8. correction-path representation;
9. reporting formats;
10. prohibited score claims;
11. local-first or network-enabled baseline;
12. whether any automatic inference is permitted in v0.1;
13. relationship to Recursive Integrity Toolkit;
14. explicit post-v0.1 features.

### Proposed v0.1 workflow

```text
structured source/evidence bundle
        ↓
schema normalization
        ↓
claim-scoped lineage graph
        ↓
declared and observed relationship validation
        ↓
independence / presence / concentration / correction analysis
        ↓
profile report with uncertainty and unresolved lineage
```

### Proposed v0.1 non-goals

v0.1 should not:

- decide whether a political, scientific, legal, or moral claim is true;
- rank ideological viewpoints;
- produce a universal source-reputation database;
- crawl the public web by default;
- infer hidden ownership from writing style;
- infer collusion from agreement;
- infer independence from disagreement;
- automatically classify "good" and "bad" publishers;
- suppress contested sources;
- create a whitelist;
- implement the full Source Integrity Layer governance architecture;
- decide payment, licensing, crawler policy, or publisher compensation.

### Acceptance criteria

`V0.1_PRODUCT_SPEC.md` must allow a future maintainer to answer:

- what data enters;
- what relationships are represented;
- what the toolkit calculates;
- what it reports;
- what it refuses to claim.

### Stop condition

Stop if the product still requires phrases such as "AI will determine trustworthy sources" without an approved operational definition.

---

## 10. Work Unit 3: Canonical ontology and lineage graph

### Objective

Define the data objects and relations that later code will represent.

### Allowed files

```text
DEFINITIONS_AND_UNITS.md
CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md
UNRESOLVED_DECISIONS.md
```

### Candidate canonical node types

Phase 0 should evaluate and either approve, rename, merge, or reject:

```text
Claim
EvidenceItem
Observation
Artifact
SourceActor
Publisher
Dataset
Model
Evaluator
Benchmark
Judgment
CorrectionEvent
ValidationEvent
ExternalReference
```

The schema should avoid turning one overloaded `Source` object into every epistemic role.

### Candidate canonical edge types

Phase 0 should evaluate:

```text
supports
contradicts
corroborates
cites
quotes
derived_from
summarizes
translates
syndicated_from
copies
generated_by
published_by
observed_by
validated_by
evaluated_by
judged_by
trained_on
retrieved_from
corrects
supersedes
appeals
propagates_to
```

### Required graph semantics

The specification must define:

- edge direction;
- edge cardinality;
- required and optional metadata;
- source-of-assertion for every edge;
- confidence or certainty status where appropriate;
- known, declared, inferred, and unknown relationship classes;
- claim-scoped lineage;
- root definition;
- independent-root definition;
- unresolved-root definition;
- transformation lineage;
- model lineage;
- evaluator lineage;
- cycles;
- self-reference;
- multi-parent derivation;
- partial provenance;
- conflicting provenance assertions.

### Required anti-collapse rule

Artifact identity, source identity, and evidentiary independence must remain separate concepts.

Example:

```text
five URLs
→ three publishers
→ two syndication chains
→ one original observation
```

The ontology must be able to represent all four levels without losing them.

### Acceptance criteria

At minimum, the specification must represent:

1. one source quoted by many publishers;
2. many independent sources supporting one claim;
3. many derivative sources disagreeing with an independent source;
4. unknown upstream ancestry;
5. synthetic summaries of one root source;
6. a model-generated evaluator judging a related model;
7. a correction that propagates downstream;
8. a correction that exists but cannot reach the final answer.

### Stop condition

Stop if independence still has to be inferred from URL count, publisher count, or textual similarity alone.

---

## 11. Work Unit 4: Integrity dimensions and analytical semantics

### Objective

Define the v0.1 analytical dimensions without collapsing them into one score.

### Allowed files

```text
DEFINITIONS_AND_UNITS.md
OBSERVABILITY_AND_REPORTING.md
V0.1_PRODUCT_SPEC.md
UNRESOLVED_DECISIONS.md
```

### Candidate dimensions

Phase 0 should define and decide the status of:

- **Nominal Source Count**
  - number of visible or declared source artifacts.

- **Resolved Source Count**
  - number of source artifacts with resolvable identity and provenance.

- **Independent Root Count**
  - number of claim-relevant upstream roots that qualify as independent under the approved rule.

- **Unknown Root Count**
  - unresolved upstream roots that cannot be classified as independent.

- **Lineage Concentration**
  - concentration of evidentiary dependence among upstream roots.

- **Derivative Share**
  - share of evidence artifacts that add no declared independent observation beyond prior lineage.

- **External Presence**
  - degree to which the evidence system contains current, reality-bearing input outside the closed lineage.

- **Corrective Independence**
  - degree to which correction or validation originates from lineage not already responsible for the object being checked.

- **Correction Reachability**
  - whether corrective evidence can reach and alter the relevant downstream object.

- **Evaluator Lineage Overlap**
  - overlap among generator, reference, judge, benchmark, training, or evaluation lineages.

- **Tail / Contestation Retention**
  - whether anomalous, minority, contradictory, or unresolved evidence remains represented rather than being silently flattened.

- **Provenance Completeness**
  - extent to which required lineage and transformation metadata are known.

### Important metric rule

A metric may be:

- directly theory-defined;
- mathematically inherited from an established result;
- a toolkit operationalization.

The specification must label which category applies.

For toolkit operationalizations such as a concentration index, the theory map must explain why the metric is useful and what it does not establish.

### No aggregate score

The default report should be a structured profile.

Example:

```text
Nominal sources:                 12
Resolved artifacts:              11
Independent roots:                3
Unresolved roots:                 2
Derivative share:              high
Lineage concentration:         high
External presence:             mixed
Corrective independence:        low
Correction reachability:    partial
Evaluator lineage overlap:     high
```

The exact fields and vocabulary remain subject to Phase 0 approval.

### Acceptance criteria

- every metric has a unit, denominator, scope, missing-data rule, and interpretation;
- unknown data cannot silently improve the result;
- no metric is treated as truth probability;
- no metric requires ideological labeling;
- the report can show strong performance on one dimension and weakness on another.

### Stop condition

Stop if any proposed score cannot explain what happens when provenance is unknown.

---

## 12. Work Unit 5: Threat model and failure taxonomy

### Objective

Define what source-integrity failures the toolkit is expected to expose.

### Allowed files

```text
SOURCE_INTEGRITY_THREAT_MODEL.md
V0.1_PRODUCT_SPEC.md
UNRESOLVED_DECISIONS.md
```

### Required threat classes

The threat model should include at least:

#### False plurality

Many visible sources share one upstream evidentiary root.

#### Citation laundering

A derivative source cites another derivative source until the original evidence becomes obscure.

#### Syndication inflation

Republished or syndicated material creates apparent multiplicity.

#### Synthetic derivative inflation

Model-generated summaries, rewrites, translations, or paraphrases increase artifact count without independent observation.

#### Circular support

Evidence chains eventually cite or depend on one another.

#### Evaluator self-validation

Generators, references, judges, or benchmarks share a model or data lineage.

#### Benchmark lineage closure

New evaluation items inherit the same task, model, rubric, and judge ancestry.

#### Provenance erasure

Transformation history is removed or flattened.

#### Authority laundering

Prestige signals or repeated institutional citation create apparent independence without new evidence.

#### Corrective-channel capture

The correction mechanism shares ancestry, incentives, authority, or information constraints with the system being corrected.

#### Correction sink

A correction can be recorded but cannot change the relevant downstream object.

#### External-presence starvation

The system receives little or no new reality-bearing input.

#### Open-input pollution

External input exists but carries weak provenance, manipulation, synthetic duplication, or adversarial contamination.

#### Tail suppression

Contradictory, anomalous, minority, local, or low-frequency evidence disappears from the represented evidence field.

### Explicit threat-model boundary

The v0.1 toolkit may represent evidence of manipulation or poisoning.

Active detection of prompt injection, hidden instructions, semantic deception, or coordinated influence is a separate capability unless Phase 0 approves a narrowly defined deterministic detector.

### Acceptance criteria

Every threat class must identify:

- required observable evidence;
- false-positive risk;
- missing-data behavior;
- whether v0.1 detects, reports, or merely represents the condition;
- future extension points.

### Stop condition

Stop if a threat can only be detected by asking an LLM to make an unconstrained trust judgment.

---

## 13. Work Unit 6: Observability and uncertainty model

### Objective

Define what the toolkit may conclude at different levels of available evidence.

### Allowed files

```text
OBSERVABILITY_AND_REPORTING.md
CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md
SUCCESS_CRITERIA.md
```

### Proposed observability levels

The final labels may change, but Phase 0 should define a hierarchy similar to:

#### Level 0: Artifact-only

Known:

- artifact identifiers;
- visible citations or declared sources.

Unknown:

- upstream provenance;
- independence;
- root observations;
- evaluator lineage;
- correction path.

Allowed result:

- artifact inventory only.

#### Level 1: Declared provenance

Known:

- source identity;
- publisher;
- explicit citations;
- declared transformation type.

Allowed result:

- declared lineage structure;
- unresolved ancestry clearly marked.

#### Level 2: Root-resolved provenance

Known:

- upstream roots for relevant claims;
- derivative relations;
- root independence under approved evidence.

Allowed result:

- independent-root analysis;
- lineage concentration;
- derivative share.

#### Level 3: Evaluator and correction lineage

Known:

- model/evaluator ancestry;
- benchmark/reference relations;
- correction nodes and routing.

Allowed result:

- evaluator overlap;
- corrective independence;
- correction reachability.

#### Level 4: External-presence and live-correction evidence

Known:

- reality-bearing input channels;
- update/correction events;
- demonstrated downstream effect.

Allowed result:

- strongest Source Integrity profile supported by v0.1.

### Capability matrix

The report must state which analyses are possible for the current input.

It must not emit a strong integrity conclusion when the input only supports Level 0 or Level 1.

### Acceptance criteria

- every report field identifies its observability requirement;
- unsupported fields are `unknown`, `not_observable`, or equivalent;
- missing data never silently becomes a pass;
- uncertainty is part of the result contract.

### Stop condition

Stop if the reporting system can output "independent" without an explicit evidence basis.

---

## 14. Work Unit 7: Canonical hero and adversarial examples

### Objective

Create the Phase 0 examples that later phases must preserve exactly.

### Allowed files

```text
V0.1_PRODUCT_SPEC.md
VALIDATION_PLAN.md
SUCCESS_CRITERIA.md
CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md
```

### Required canonical cases

Phase 0 should define at least one hero case and several micro-cases.

#### Hero case candidate: False plurality with correction

```text
Claim C1
├── Article A
├── Article B
├── Article C
├── Model Summary D
└── Database Entry E
```

Resolved lineage:

```text
A ─┐
B ─┼── Root Observation R1
C ─┘
D ── derived from B
E ── derived from A
```

A separate source provides Root Observation R2.

A correction event later changes R1, but only some downstream artifacts receive the correction.

The hero must let the future toolkit demonstrate:

- nominal count;
- root resolution;
- derivative inflation;
- independent-root count;
- lineage concentration;
- correction reachability;
- partial correction propagation;
- unknowns.

#### Required micro-cases

1. three genuinely independent observations;
2. five domains copied from one root;
3. unresolved upstream lineage;
4. circular citations;
5. same-model-family generator and judge;
6. independent human evaluator with unknown training-data overlap;
7. contested independent sources;
8. synthetic paraphrase chain;
9. correction logged but not propagated;
10. external evidence reopening a previously closed lineage.

### Golden contract

Phase 0 must specify expected structural conclusions in prose.

Exact machine-readable golden outputs may be created in Phase 1.

### Acceptance criteria

The hero must be rich enough to distinguish:

- artifact plurality;
- source plurality;
- root plurality;
- evidence independence;
- evaluator independence;
- correction effectiveness.

### Stop condition

Stop if two materially different source structures produce indistinguishable expected reports.

---

## 15. Work Unit 8: Validation, falsification, and testing plan

### Objective

Define how future implementation will prove that it conforms to the specification.

### Allowed files

```text
VALIDATION_PLAN.md
SUCCESS_CRITERIA.md
THEORY_TO_CODE_TRACEABILITY.md
```

### Required future test families

The validation plan must include:

- schema validation;
- object-identity tests;
- edge-direction tests;
- duplicate-identifier tests;
- lineage-root tests;
- multi-parent derivation tests;
- cycle tests;
- unknown-provenance tests;
- claim-scoped independence tests;
- transformation-lineage tests;
- evaluator-lineage tests;
- correction-reachability tests;
- correction-propagation tests;
- external-presence tests;
- observability-level tests;
- report determinism tests;
- golden hero tests;
- privacy and path-safety tests;
- no-network baseline tests;
- malformed-input rejection tests;
- large-graph performance tests for later phases.

### Falsification requirements

Phase 0 must define cases that would demonstrate a flawed product theory or implementation.

At minimum:

- the toolkit counts derivative copies as independent roots;
- missing provenance increases independence;
- a correction that cannot alter the downstream object is reported as full corrective capacity;
- evaluator lineage overlap is ignored;
- disagreement automatically lowers integrity;
- verified status is treated as truth;
- unknown source ancestry is silently converted into a root;
- different claim scopes cannot produce different independence results for the same artifact.

### Acceptance criteria

Each v0.1 public analytical field must have:

- at least one positive test;
- at least one negative test;
- at least one missing-data test;
- at least one boundary test.

### Stop condition

Stop if a public field cannot be tested without subjective interpretation that the schema does not represent.

---

## 16. Work Unit 9: Privacy, security, and licensing

### Objective

Define safe handling of source and evidence data before code exists.

### Allowed files

```text
PRIVACY_AND_DATA_HANDLING.md
LICENSING_NOTES.md
SOURCE_INTEGRITY_THREAT_MODEL.md
```

### Privacy requirements

The specification must address:

- public URLs;
- private documents;
- confidential source identity;
- personal data;
- whistleblower or protected-source metadata;
- internal model and benchmark lineage;
- export/redaction behavior;
- logs;
- temporary files;
- example data.

### Default privacy posture

Recommended:

- local-first;
- no network access by default;
- no automatic upload;
- no telemetry by default;
- explicit opt-in for future external resolution;
- public fixtures only;
- no real private evidence in repository examples.

### Security requirements

Future ingestion must treat source content as untrusted data.

The Phase 0 architecture must prohibit:

- execution of embedded instructions;
- executable mapping expressions;
- automatic shell expansion;
- unsafe deserialization;
- arbitrary remote code;
- silent network fetches.

### Licensing requirements

The plan must distinguish:

- software code license;
- reusable specification license;
- example-data license;
- theory-paper licenses;
- third-party source licenses.

Theory PDFs remain reference assets under their stated licenses and should not be copied into the public repository unless licensing review explicitly authorizes that use.

### Acceptance criteria

The project can state how to audit sensitive provenance without requiring disclosure of protected identities in public reports.

### Stop condition

Stop if the proposed data model requires public release of confidential source identity to function.

---

## 17. Work Unit 10: Theory-to-code traceability and future architecture

### Objective

Define ownership for future implementation without implementing it.

### Allowed files

```text
THEORY_TO_CODE_TRACEABILITY.md
REPOSITORY_ARCHITECTURE.md
DEPENDENCY_STRATEGY.md
GOVERNANCE_AND_HANDOFF.md
```

### `THEORY_TO_CODE_TRACEABILITY.md`

Every approved v0.1 rule should receive a stable Trace ID.

Recommended form:

```text
SIT-TR001
SIT-TR002
...
```

Each Trace ID should map:

```text
theory source
→ product rule
→ future module owner
→ public fields
→ future tests
→ report section
```

### Proposed future repository domains

Phase 0 should evaluate a later structure such as:

```text
src/source_integrity_toolkit/
    io/
    models/
    claims/
    lineage/
    provenance/
    independence/
    evaluators/
    corrections/
    observability/
    reports/
    security/
    utils/
```

This is a planning structure only.

### Interoperability boundary with Recursive Integrity Toolkit

Phase 0 should define a future neutral interchange artifact such as a provenance graph or normalized lineage manifest.

The Source Integrity Toolkit should not import Recursive Integrity Toolkit internals in v0.1.

The Recursive Integrity Toolkit should not become a required dependency.

### Dependency strategy

Phase 0 should prefer:

- Python standard library where sufficient;
- small, auditable graph/data dependencies where justified;
- deterministic local processing;
- optional dependencies for advanced formats;
- no required LLM dependency;
- no required network dependency.

Exact dependency names should be selected only after the product and graph requirements are approved.

### Acceptance criteria

Every planned future module has a reason to exist and a traceable owner.

No module exists solely because "a toolkit usually has one."

### Stop condition

Stop if architecture is being designed around a library before product semantics are stable.

---

## 18. Work Unit 11: Final Phase 0 audit and approval package

### Objective

Verify that the entire specification bundle is internally consistent and ready for approval.

### Allowed files

All Phase 0 Markdown files.

No code files may be created.

### Final audit requirements

The audit must verify:

#### Theory consistency

- every product rule has a theory basis or explicit operationalization label;
- source quotations and concepts retain their original meaning;
- no theory formula is repurposed without explanation.

#### Product consistency

- all files use the same v0.1 scope;
- all files use the same canonical object names;
- all files use the same edge semantics;
- all files agree on independence;
- all files agree on unknown provenance behavior;
- all files agree on external presence;
- all files agree on correction reachability;
- all files agree that no universal score exists in v0.1.

#### Traceability

- every public field has a Trace ID;
- every Trace ID has a source;
- every planned module has an owner;
- every public field has a future test;
- every hero expected result maps to approved definitions.

#### Phase boundary

- no implementation code exists;
- no runtime package exists;
- no schema files exist;
- no dependency has been installed for project implementation;
- no Phase 1 work has begun.

#### Unresolved decisions

Every unresolved item must be one of:

```text
APPROVED
DEFERRED
REJECTED
BLOCKING
```

No blocking decision may remain when Phase 0 is approved.

### Approval artifact

After explicit Theory Owner approval, create:

```text
PHASE_0_APPROVAL.md
```

It should include:

- project;
- target release;
- approval date;
- Theory Owner;
- decision status;
- approved Phase 0 file list;
- SHA-256 for each approved file;
- approved decision effects;
- deferred features;
- Phase 1 authorization;
- Phase 1 prohibitions.

---

## 19. Testing requirements during Phase 0

Phase 0 contains no executable product tests.

It still requires specification-level validation.

### 19.1 Cross-document consistency checks

Manually or with non-product drafting utilities, verify:

- canonical terms match;
- IDs are unique;
- cross-references resolve;
- no public field has conflicting definitions;
- no decision appears approved in one file and unresolved in another.

### 19.2 Hero reasoning checks

For every canonical case, manually derive the expected structural result from the approved definitions.

If two reviewers cannot reproduce the same result from the specification, the relevant definition remains incomplete.

### 19.3 Negative specification tests

Attempt to misuse the spec in the following ways:

- count five derivative articles as five independent roots;
- classify unknown roots as independent;
- treat a verified publisher as true;
- treat a different model version as automatically independent;
- treat a correction log as effective correction;
- treat high source count as high presence;
- treat disagreement as corruption.

The specification must explicitly reject each misuse.

### 19.4 No implementation leakage

Search the Phase 0 bundle for:

- Python code intended for runtime;
- package installation commands presented as current implementation;
- executable algorithms;
- schema files;
- hidden Phase 1 behavior.

Small mathematical examples and pseudocode are allowed when they clarify the specification. They must not become implementation.

---

## 20. Global stop rules

Phase 0 work must stop when any of the following occurs:

1. **Theory conflict**
   - two authoritative sources imply incompatible semantics and no approved resolution exists.

2. **Product ambiguity**
   - a public field has more than one plausible meaning.

3. **Independence ambiguity**
   - the spec cannot determine what evidence is required to call two roots independent.

4. **Unknown-data ambiguity**
   - missing provenance can be interpreted as either pass or fail without an explicit rule.

5. **Correction ambiguity**
   - the spec cannot distinguish correction existence from correction effectiveness.

6. **Claim-scope ambiguity**
   - the same artifact cannot be analyzed differently for different claims when its evidentiary role changes.

7. **Score pressure**
   - implementation planning starts to collapse the profile into one universal integrity score.

8. **Premature automation**
   - an LLM, web search, or classifier is required to make a core v0.1 determination that has not been defined structurally.

9. **Scope expansion**
   - work begins implementing the full Source Integrity Layer, including live trust ranking, crawler governance, source payment, or public appeals infrastructure.

10. **Cross-project coupling**
   - Source Integrity Toolkit begins depending on internal code from Recursive Integrity Toolkit before a stable interoperability contract exists.

When a stop rule triggers, record the issue in `UNRESOLVED_DECISIONS.md` and wait for Theory Owner resolution.

---

## 21. Phase 0 success criteria

Phase 0 passes only when all of the following are true.

### Product identity

- the v0.1 user and use case are explicit;
- product boundaries are explicit;
- the relation to Recursive Integrity Toolkit is explicit.

### Theory integrity

- the source stack is mapped;
- direct theory claims and toolkit operationalizations are distinguishable;
- no unresolved theory conflict remains.

### Ontology

- nodes and edges are canonical;
- claim-scoped independence is defined;
- root semantics are defined;
- unknown provenance is defined;
- transformations are defined;
- evaluator lineage is defined;
- correction lineage is defined.

### Analysis semantics

- all v0.1 dimensions are defined;
- missing-data behavior is defined;
- observability requirements are defined;
- no universal score exists.

### Threat model

- false plurality;
- citation laundering;
- derivative inflation;
- circularity;
- evaluator closure;
- provenance erasure;
- corrective capture;
- correction sinks;
- presence starvation;
- open-input pollution;
- tail suppression

are all represented in the threat model.

### Validation

- hero cases exist;
- micro-cases exist;
- expected results are reproducible;
- each public field has future tests.

### Governance

- privacy rules exist;
- licensing rules exist;
- architecture is planned;
- dependency strategy is planned;
- Phase 1 authority and prohibition boundaries are explicit.

### Approval readiness

- no `BLOCKING` decision remains;
- all Phase 0 files pass final audit;
- hashes can be generated;
- the Theory Owner can approve the bundle as a stable baseline.

---

## 22. Phase 0 final deliverables

The final Phase 0 handoff should contain:

```text
PHASE_0_PLAN.md
SPEC_AUDIT.md
THEORY_SOURCE_MAP.md
UNRESOLVED_DECISIONS.md
PROJECT_INSTRUCTIONS.md
V0.1_PRODUCT_SPEC.md
DEFINITIONS_AND_UNITS.md
CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md
SOURCE_INTEGRITY_THREAT_MODEL.md
OBSERVABILITY_AND_REPORTING.md
THEORY_TO_CODE_TRACEABILITY.md
VALIDATION_PLAN.md
PRIVACY_AND_DATA_HANDLING.md
LICENSING_NOTES.md
SUCCESS_CRITERIA.md
GOVERNANCE_AND_HANDOFF.md
REPOSITORY_ARCHITECTURE.md
DEPENDENCY_STRATEGY.md
```

After approval:

```text
PHASE_0_APPROVAL.md
```

The approved bundle becomes the authority for Phase 1.

---

## 23. Phase 1 authorization after approval

Approval of Phase 0 should authorize only a repository scaffold.

Phase 1 may create:

- repository root;
- package metadata;
- package directories;
- import-safe stubs;
- schema placeholders;
- tests and fixture structure;
- hero fixture files;
- governance files;
- CI scaffold;
- architecture-compliance scripts.

Phase 1 should remain prohibited from implementing:

- independent-root algorithms;
- lineage-concentration calculations;
- correction-reachability algorithms;
- graph traversal;
- cycle detection;
- evaluator-overlap analysis;
- external-presence calculations;
- trust ranking;
- source scoring;
- live crawling;
- automatic provenance resolution;
- report-generation logic beyond scaffold contracts.

Analytical implementation should begin only in later phases under separately approved plans.

---

## 24. Recommended execution order after this plan is approved

Once `PHASE_0_PLAN.md` is approved, execute the phase in this order:

```text
1. SPEC_AUDIT.md
2. THEORY_SOURCE_MAP.md
3. UNRESOLVED_DECISIONS.md
4. V0.1_PRODUCT_SPEC.md
5. PROJECT_INSTRUCTIONS.md
6. DEFINITIONS_AND_UNITS.md
7. CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md
8. SOURCE_INTEGRITY_THREAT_MODEL.md
9. OBSERVABILITY_AND_REPORTING.md
10. VALIDATION_PLAN.md
11. THEORY_TO_CODE_TRACEABILITY.md
12. PRIVACY_AND_DATA_HANDLING.md
13. LICENSING_NOTES.md
14. SUCCESS_CRITERIA.md
15. REPOSITORY_ARCHITECTURE.md
16. DEPENDENCY_STRATEGY.md
17. GOVERNANCE_AND_HANDOFF.md
18. Final Phase 0 audit
19. Theory Owner decision
20. PHASE_0_APPROVAL.md
```

The phase should stop after approval packaging.

Do not enter Phase 1 until the Theory Owner explicitly approves the Phase 0 baseline.
