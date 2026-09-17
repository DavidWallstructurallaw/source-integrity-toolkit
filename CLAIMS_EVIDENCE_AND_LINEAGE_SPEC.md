# CLAIMS_EVIDENCE_AND_LINEAGE_SPEC

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Target release | v0.1 |
| Phase / work unit | Phase 0 / Work Unit 7: Canonical hero record contract |
| Revision | 0.3 |
| Date | 2026-09-17 |
| Status | PROPOSED FOR REVIEW; preserved input/report bridge plus WU7 prose cases |
| Theory Owner | Xiangyu Guo |
| Technical Owner | Unassigned |
| Current instruction | Continue Work Unit 7 |
| Definition / reporting owners | Definitions 0.2; reporting 0.2 in its submitted WU6 form |
| Central decisions | Revision 0.5 unchanged; WU5 acceptance supplement in reporting §11.1 |
| Logical input contract | sit-bundle/0.1, unchanged |
| New material | Sections 23-28: case authority, exact hero records and isolated variants |
| Input kinds / predicates / assessment kinds added | None |
| Final Phase 0 approval / implementation | Not issued / not implemented |

**Revision 0.3 reading rule.** Numbered sections 1-22 retain lineage revision 0.2 verbatim. Their historical status, prior-unit approvals and future-unit references remain history. The current WU7 extension is §§23-28. It supplies candidate case inputs using the existing fields; it does not edit the WU6 reporting owner, central register or approved analytical definitions. The current instruction authorizes this proposal; final case adoption must include or amend the submitted WU6 reporting reference.

## 1. Purpose and contract boundary

This specification defines how a caller-prepared evidence bundle can preserve claim scope, artifact versions, origins, assertions, evaluator roles, external-input stages and corrective paths. It instantiates the meanings in [DEFINITIONS_AND_UNITS.md](DEFINITIONS_AND_UNITS.md).

Its inputs are the accepted directions in [V0.1_PRODUCT_SPEC.md](V0.1_PRODUCT_SPEC.md), [PROJECT_INSTRUCTIONS.md](PROJECT_INSTRUCTIONS.md), [THEORY_SOURCE_MAP.md](THEORY_SOURCE_MAP.md) and the approved Phase 0 plan. Source concepts use the existing SIL, UIL, EC, HDL, EBC and BVL aliases. Page locators refer to the supplied PDFs.

The exact representation below is a toolkit operationalization. The papers support the distinctions and limits; they do not specify these object keys, edge directions or enums. No external standard compliance is claimed.

No executable JSON Schema, sample JSON file, code, graph traversal implementation, metric formula, fixture generator, network resolver or report generator is included. Tables define the proposed future contract. Prose examples in §15 are representation witnesses, not a frozen hero dataset.

### 1.1 Three separate outcomes of validation

A future parser must keep three questions separate:

| Question | Meaning |
|---|---|
| Is the bundle structurally valid? | Its types, keys, required fields and local references satisfy this contract |
| Does it support an analysis? | The relevant inquiry, relationships and evidence prerequisites are present |
| Are its statements true in the world? | A substantive question requiring external, type-appropriate validation |

Only the first two are local toolkit operations. Structurally accepted source assertions remain attributed source assertions. A valid sparse bundle is permitted even when it supports only inventory and explicit gaps. [SIT-P001-P006; SIT-D003-D007]

## 2. Logical bundle envelope

The file and future in-process interface use the same logical structure. The file representation is one UTF-8 JSON object. Unknown keys outside explicitly designated extension containers are invalid; no inferred field aliases are accepted.

| Top-level key | Type | Requirement / meaning |
|---|---|---|
| `contract_version` | String | Required; the exact adopted contract label |
| `bundle_id` | Identifier | Required; caller-assigned dossier identity |
| `snapshot_id` | Identifier | Required; immutable snapshot identity within the bundle |
| `recorded_at` | TimeValue | Required; bundle assembly time or explicit unknown |
| `predecessor` | Object or null | Required; null or exactly `bundle_id`, `snapshot_id`; informational only |
| `inquiries` | Array of Inquiry | Required; at least one inquiry |
| `records` | Array of typed records | Required; includes every locally referenced record, including target claims |
| `assertions` | Array of Assertion | Required; may be empty |
| `evidence_references` | Array of EvidenceReference | Required; may be empty |
| `extensions` | Namespaced metadata object | Optional; inert metadata with no core semantic authority |

There is no top-level executable mapping, inline program, remote schema import, network-resolution option or scoring policy. Numeric analysis configuration belongs to later approved specifications; this envelope cannot smuggle it in through extensions.

### 2.1 Sparse bundle

A minimum useful dossier contains one Inquiry and its Claim, with empty source, assertion and supporting-reference collections where nothing else is known. The Claim can have unknown attribution and version metadata using explicit gaps. The inquiry still states the target and boundary description.

Artifact-only source inventory is represented by `seed_artifact_refs`, without pretending that claim-bound contributions or ancestry have been established. Full provenance is an analytical prerequisite for some findings, not a mandatory condition for every admitted record.

### 2.2 Identifiers and references

All Inquiry, record, Assertion and EvidenceReference IDs are unique across the entire snapshot, including across collections. Duplicate IDs are rejected even when the duplicated payloads match.

An identifier is a nonempty, case-sensitive ASCII token beginning with a letter or digit and containing only letters, digits, period, underscore, colon and hyphen. It has no path, execution or fetch meaning. Maximum lengths and aggregate resource budgets remain Work Unit 9 gates before executable-schema or parser adoption.

A `*_ref` is one snapshot-local identifier. A `*_refs` or `*_ref_ids` field is an array of distinct snapshot-local identifiers. Each field has the endpoint-type restrictions below. A missing local ID is a structural error. To represent unknown or unavailable material, supply an actual `unresolved_reference` record with the expected type and reason.

The effective identity of an object is `(bundle_id, snapshot_id, id)`. No reference traverses `predecessor`. Prior material needed for this audit must be explicitly represented in this snapshot with its provenance. Copying a predecessor identifier into a field does not import it.

### 2.3 Snapshot immutability

Changing a statement version, artifact version, assertion basis or relevant scope produces a new snapshot. The same local ID can continue to refer to the same underlying object in a later snapshot, but cross-snapshot identity requires explicit caller provenance. No implicit merge, overwrite or claim of historical comparison is performed.

## 3. Shared value structures

### 3.1 TimeValue

TimeValue has exactly `state`, `value`, `precision` and `reason`.

| Field | Allowed values |
|---|---|
| `state` | `known`, `unknown`, `withheld`, `not_applicable` |
| `value` | String for `known`; null otherwise |
| `precision` | `date` or `instant` for `known`; null otherwise |
| `reason` | Optional explanatory string for `known`; nonempty string otherwise |

A known date uses `YYYY-MM-DD`. A known instant includes date, time, seconds and `Z` or an explicit numeric UTC offset; fractional seconds are permitted. Local clock time without an offset is not converted using the machine's timezone. Date-only values denote a date interval, not a fabricated midnight instant.

A TimeWindow has `start` and `end`, each a TimeValue, plus an optional `note`. Unknown endpoints remain unknown. An inconsistent known interval is a data-quality issue requiring correction, with structural acceptance handled as described in §14.

### 3.2 Provenance

Every Inquiry, typed record and Assertion carries a required `provenance` object:

| Field | Type / meaning |
|---|---|
| `attributed_to_ref` | Actor, Model or UnresolvedReference expected to denote either; null permitted with an attribution gap |
| `basis_kind` | `declaration`, `documented_record`, `upstream_inference`, `protected_attestation`, `unspecified` |
| `evidence_ref_ids` | Array of supporting EvidenceReference IDs; may be empty |
| `method` | String or null; a scoped description of how the information was obtained |
| `qualifications` | Array of limitation strings; required, possibly empty |

These fields describe the supplied record, including its classifications. They do not authenticate the asserter or certify the supporting material. A record marked `documented_record` with no supplied supporting material is retained as an unsupported documentary assertion, with an evidence-basis issue. It does not acquire documentary qualification from its label.

A self-declared Actor may reference itself as its asserter. That is attribution, not independent verification. EvidenceReference support is not recursively required to terminate in a proof of the entire record universe. The audit exposes the stated basis and limits.

### 3.3 Gap

An optional `gaps` array contains objects with exactly `field`, `reason` and `detail`. `field` names a field path in the containing record, or `unmodeled_history` for an unavailable upstream area. Paths are inert strings.

`reason` is one of `not_recorded`, `not_examined`, `withheld`, `unavailable`, `identity_ambiguous`, `outside_snapshot`, `not_applicable`, `other`. `detail` is a nonempty explanation.

Required nullable factual fields must have a Gap when null, except where the relevant record subtype explicitly gives null a structural meaning, such as a submission having no parent case. TimeValue already carries its own reason. An empty list of unknown historical parents must not be used as a complete-history assertion.

### 3.4 Extension container

`extensions` is an optional JSON object whose keys contain a namespace prefix followed by a colon. Values are JSON-compatible data only. Core processing preserves the metadata without allowing it to define predicates, suppress gaps, supply authority, grant independence or change the contract version.

No code callback, import, template evaluation or URL resolution is supported. An extension needed to interpret an included analysis means the core contract is insufficient and requires an explicit specification revision. Extensions are not a compatibility promise to another toolkit.

## 4. Supporting references and attribution

### 4.1 EvidenceReference fields

| Field | Type / requirement |
|---|---|
| `id` | Required unique identifier |
| `reference_kind` | Required: `supplied_excerpt`, `record_pointer`, `local_locator`, `external_locator`, `protected_attestation` |
| `availability` | Required: `supplied`, `locator_only`, `withheld`, `unavailable` |
| `artifact_ref` | Artifact or compatible UnresolvedReference; nullable |
| `record_ref` | Any typed record or Assertion ID; nullable |
| `locator` | String or null; document section, local address or external address, always inert |
| `excerpt` | String or null; caller-supplied text, retained as untrusted data |
| `provided_by_ref` | Actor, Model or compatible UnresolvedReference; nullable with Gap |
| `attestor_ref` | Actor or compatible UnresolvedReference; required for a protected attestation, otherwise nullable |
| `scope_note` | Required nonempty string explaining what this reference is offered to support |
| `gaps`, `extensions` | Optional shared structures |

Nullable `artifact_ref`, `record_ref`, `locator` and `excerpt` use structural null when irrelevant to that reference kind. The kind-specific rules below ensure that at least one meaningful support form exists.

### 4.2 Kind-specific rules

A `supplied_excerpt` has nonempty `excerpt` and `availability = supplied`. It identifies its artifact or records an origin/location gap. A `record_pointer` identifies an existing record or assertion. A local or external locator has nonempty `locator`; `availability = locator_only` means the toolkit has no supplied content from it.

A `protected_attestation` identifies an attestor or protected attestor reference, a scope note and a supplied attestation summary/excerpt or an identified attestation artifact. Its unavailable underlying material and its visible attestation must remain distinguishable. A completely unavailable attestation is not counted as inspectable evidence.

An assertion cannot use a record pointer to itself as its sole documentary support and become evidence-qualified. Cyclic assertion-support chains are preserved as an assurance limitation, distinct from source-origin graph cycles.

Local locators are not opened automatically. External locators are not fetched. The input file is the sole runtime evidence payload in this release proposal. Callers can provide excerpts or structured records themselves. Neither ingestion nor a checksum makes an external reference independently verified. [SIT-D003, SIT-D014, SIT-D016]

## 5. Inquiry contract

| Field | Type / requirement |
|---|---|
| `id` | Required unique identifier |
| `label` | Optional human-readable string |
| `target_claim_refs` | Required nonempty list of resolved Claim IDs |
| `target_object_refs` | Required list of Artifact, Model, Evaluation or compatible UnresolvedReference IDs; may be empty |
| `seed_artifact_refs` | Required list of Artifact or compatible UnresolvedReference IDs; may be empty |
| `seed_evidence_refs` | Required list of EvidenceItem IDs; may be empty |
| `boundary` | Required object: nonempty `description`, nonempty `criterion`, and `system_refs` list |
| `time_window` | Required TimeWindow |
| `as_of` | Required TimeValue specifying the audit's relevant cutoff |
| `dependency_dimensions` | Required list drawn from the five core dimensions in definitions §9; may be empty for inventory-only work |
| `coverage_assertion_refs` | Required list of coverage AssessmentAssertion IDs; may be empty |
| `provenance` | Required Provenance |
| `gaps`, `extensions` | Optional shared structures |

`boundary.system_refs` can point to Actors, Models, Artifacts, Evaluations or corresponding UnresolvedReferences. The description and criterion make externality interpretable even when some system objects are unknown. They are descriptive text, never execution instructions.

All seed EvidenceItems must bind a claim in `target_claim_refs`. Seed artifacts can be listed before their evidentiary role is known. Artifacts included only as supporting metadata are not silently added to the seed source set or a later nominal-source denominator.

The declared dimensions select the kinds of dependence under consideration. An empty list creates no default claim that all dimensions were checked. Completeness of a citation list never implies completeness of model ancestry or correction routes.

## 6. Typed record contract

Every record has required `id`, `kind`, `data` and `provenance`. `label`, `gaps` and `extensions` are optional. `kind` is one of the twelve values below. The `data` object permits only the fields in its record table. Every field listed as required must exist, including required arrays that may be empty.

Record field links inherit that record's provenance. They are distinct from separate RelationAssertions. A role or binding must have one canonical location; candidate aliases cannot create a second unsynchronized relationship source.

### 6.1 Claim: `claim`

| Data field | Requirement |
|---|---|
| `claim_key` | Required string; caller's logical statement-family key |
| `version_label` | Required string or null with Gap |
| `text` | Required nonempty string or null with protected/context Gap |
| `content_evidence_ref` | Optional EvidenceReference; required when text is null |
| `context` | Required string defining relevant object, time or inquiry qualification |

Claim content can be protected if an authorized reference and meaningful scope survive. Claim equivalence, atomization and factual evaluation remain external tasks. Two claim versions can share `claim_key` without having identical meaning.

### 6.2 Artifact: `artifact`

| Data field | Requirement |
|---|---|
| `artifact_kind` | Required: `document`, `dataset`, `answer`, `reference_answer`, `rubric`, `benchmark`, `judgment`, `observation_record`, `execution_result`, `other`, `unknown` |
| `work_key` | Required string or null with Gap; logical material family |
| `version_label` | Required string or null with Gap |
| `locators` | Required list of inert strings; may be empty |
| `published_at` | Required TimeValue |
| `retrieved_at` | Required TimeValue |
| `content_evidence_refs` | Required list of EvidenceReference IDs; may be empty |
| `checksums` | Optional list of objects with `algorithm`, `value`, `covered_material`; strings identifying supplied byte claims |

Checksums are recorded evidence attributes, not automatically verified signatures. One URL used at two times can refer to two Artifact records. An unknown version is permissible but limits version-specific comparisons.

### 6.3 SourceActor: `actor`

| Data field | Requirement |
|---|---|
| `actor_kind` | Required: `human`, `organization`, `software_agent`, `unknown` |
| `identity_disclosure` | Required: `named`, `pseudonymous`, `protected`, `unknown` |
| `display_name` | Required string or null with Gap |
| `identity_key` | Optional caller-defined opaque string; no external identity proof implied |

Names, contact data, organization size and reputation are not mandatory. No mandatory real-world name, public profile or publisher credential is introduced.

### 6.4 EvidenceItem: `evidence_item`

| Data field | Requirement |
|---|---|
| `claim_ref` | Required resolved Claim ID; exactly one |
| `artifact_ref` | Required Artifact or UnresolvedReference expected to denote an Artifact; exactly one |
| `locator` | Required string or null with Gap; the relevant contribution in the artifact |
| `epistemic_type` | Required: `measurement`, `testimony`, `documentary_statement`, `estimate`, `formal_derivation`, `execution_result`, `analytical_inference`, `evaluative_judgment`, `allegation`, `fictional_example`, `unclassified` |
| `description` | Required nonempty contribution description |

There is no automatic `is_original`, `is_independent` or `is_true` flag. Stance and ancestry are separately asserted. EvidenceItems with the same artifact and claim remain separate supplied contributions; they are not automatically merged or assumed independent.

### 6.5 OriginEvent: `origin_event`

| Data field | Requirement |
|---|---|
| `event_kind` | Required: `observation`, `data_collection`, `testimony`, `documentary_issuance`, `analysis`, `formal_check`, `execution`, `other`, `unknown` |
| `event_key` | Required string or null with Gap; optional shared external-event descriptor, not acquisition identity |
| `performed_by_refs` | Required list of Actor, Model or compatible UnresolvedReference IDs; may be empty with Gap when unknown |
| `method_ref` | Artifact or compatible UnresolvedReference; nullable with Gap |
| `occurred_at` | Required TimeValue |
| `description` | Required nonempty string |

An acquisition root requires the scoped boundary assessment in §9.1. Shared `event_key` values alone do not establish shared acquisition. A separate analysis event cannot erase a shared data-collection parent.

### 6.6 Model: `model`

| Data field | Requirement |
|---|---|
| `model_key` | Required string; declared model identity label |
| `version_label` | Required string or null with Gap |
| `family_label` | Required string or null with Gap |
| `provider_ref` | Actor or compatible UnresolvedReference; nullable with Gap |

Provider and family labels are declared metadata. Actual ancestry and training references use the relation registry. A provider match is not automatically a copy edge.

### 6.7 Evaluation: `evaluation`

| Data field | Requirement |
|---|---|
| `evaluation_kind` | Required: `judgment`, `formal_check`, `execution`, `empirical_review`, `human_review`, `identity_process_review`, `other`, `unknown` |
| `target_refs` | Required nonempty list of Claim, Artifact, EvidenceItem, Model or Assertion IDs, or compatible UnresolvedReferences |
| `role_bindings` | Required list of RoleBinding objects; may be empty with a role gap |
| `result_refs` | Required list of Artifact or compatible UnresolvedReference IDs; may be empty |
| `occurred_at` | Required TimeValue |
| `review_contribution` | Required string or null; null is structural for non-review activities, otherwise has a Gap |

A RoleBinding contains exactly `role`, `object_ref`, `evidence_ref_ids` and `qualifications`. Its provenance inherits the Evaluation record, supplemented by the binding's references and qualifications.

| Role | Allowed object types |
|---|---|
| `candidate` | Claim, Artifact, EvidenceItem, Model |
| `generator`, `judge`, `executor` | Actor or Model |
| `human_reviewer` | Actor declared `human`, or a protected unresolved human-actor reference |
| `reference_answer`, `rubric`, `validation_environment`, `method_input` | Artifact |

Every role also permits an UnresolvedReference with the corresponding expected type. One role can have multiple bindings and one object can occupy several roles. Arrays preserve attribution without implying independent votes.

An organizational review service is an Actor. A human-reviewer binding requires a recorded human or protected human-actor reference. The toolkit imports outcomes through `result_refs`; it does not execute the validation.

### 6.8 CorrectionChannel: `correction_channel`

| Data field | Requirement |
|---|---|
| `owner_refs` | Required list of Actor, Model or compatible UnresolvedReference IDs; may be empty with Gap |
| `target_refs` | Required list of Claim, Artifact, EvidenceItem, Model, Evaluation or Assertion IDs, or compatible UnresolvedReferences; may be empty with target gap |
| `contact_locator` | Required inert string or null with Gap |
| `declared_action_types` | Required list of Action values; may be empty |
| `valid_window` | Required TimeWindow |

Action values are `review`, `amend`, `annotate`, `retract`, `rerun`, `rollback`, `replace_evaluator`, `restrict_scope`, `withdraw`, `metadata_correction`, `other`. The values describe claimed capability, with no execution authority conferred on the toolkit.


A correction can target an Evaluation record, for example to replace its evaluator-role assignment. A change then refers to the before/after Evaluation records with the altered bindings. It does not imply that the model weights or the original judgment artifact were modified.

### 6.9 CorrectionEvent: `correction_event`

Common data fields are required `event_kind`, `case_ref`, `channel_ref`, `target_refs`, `occurred_at` and `details`.

`event_kind` is `submission`, `handling` or `change`. `channel_ref` is a CorrectionChannel, compatible UnresolvedReference or null with Gap. `target_refs` uses the same target kinds as CorrectionChannel and must be nonempty. `occurred_at` is a TimeValue.

| Subtype | `case_ref` | Required fields inside `details` |
|---|---|---|
| `submission` | Null, structurally | `submission_kind`: `objection`, `proposed_correction` or `appeal`; `summary`: nonempty string |
| `handling` | A CorrectionEvent of kind `submission` | `outcome`: `acknowledged`, `under_review`, `accepted`, `rejected`, `withdrawn`, `failed`, `unknown`; `reason`: string or null with Gap |
| `change` | A CorrectionEvent of kind `submission` | `action_type`: Action; `before_ref`: target record or compatible UnresolvedReference; `after_ref`: target record, compatible UnresolvedReference or null; `after_absence_reason`: string or null; `linkage_description`: nonempty string |

For a change, `before_ref` must occur in the record's targets. `after_ref = null` is allowed only for explicitly described removal/withdrawal/retraction with an `after_absence_reason`; it must not conceal an unknown after-state. Unknown after-state uses an UnresolvedReference. A nonnull after-state has a structural null absence reason.

Change linkage comes from the supplied process/provenance evidence. A linkage description without evidence remains a declaration. The event does not establish that the correction is substantively correct, that the route had authority, or that it can sustain an arbitrary workload.

### 6.10 PipelineRecord: `pipeline_record`

| Data field | Requirement |
|---|---|
| `subject_ref` | Required EvidenceItem or Anomaly ID |
| `run_key` | Required nonempty string identifying the external pipeline/run |
| `stage_key` | Required nonempty string identifying the external process step |
| `stage` | Required: `admission`, `preservation`, `selection`, `influence` |
| `state` | Required: `occurred`, `did_not_occur`, `unknown` |
| `output_refs` | Required list of EvidenceItem, Artifact or Anomaly IDs, or compatible UnresolvedReferences; may be empty |
| `observed_at` | Required TimeValue |
| `linkage_kind` | Required: `use_record`, `comparison_record`, `experimental_attribution`, `declaration`, `unspecified` |
| `detail` | Required nonempty string explaining the observed or missing stage relation |

`state = did_not_occur` is an attributed negative observation at that stage. Missing stage records do not create that value. A preservation claim identifies the contribution or distinction preserved and any output mapping; content similarity is not computed. An influence record with `use_record` describes observed use, not an estimated causal effect.

An eligible input universe for retention uses a coverage assessment with enumerated members. A bundle's final artifact list alone does not establish that universe.

### 6.11 Anomaly: `anomaly`

| Data field | Requirement |
|---|---|
| `inquiry_refs` | Required nonempty list of Inquiry IDs |
| `claim_ref` | Claim or null; null is structural when the anomaly does not fit a current claim |
| `original_context` | Required nonempty string or null with protected Gap |
| `context_evidence_ref` | EvidenceReference or null; required when original context is protected |
| `classification_state` | Required: `unclassified`, `caller_classified` |
| `caller_label` | Required string for `caller_classified`; structural null for `unclassified` |
| `comparison_note` | Required string or null with Gap describing the stated rarity/contestation comparison |

Unclassified anomalies are valid. They do not need to be forced into a current claim, demographic group or benchmark class. Other supplied material can point to them without creating a truth judgment.

### 6.12 UnresolvedReference: `unresolved_reference`

| Data field | Requirement |
|---|---|
| `expected_kinds` | Required nonempty list of record kinds excluding `unresolved_reference` |
| `reason` | Required Gap reason, excluding `not_applicable` for an endpoint asserted to exist |
| `description` | Required nonempty explanation of the missing area or identity |
| `external_locator` | Optional inert string |
| `protected_key` | Optional stable opaque identifier, with no automatic identity or independence assurance |

An unresolved endpoint is a valid represented gap. Its expected kind does not instantiate that missing object. Several links to one protected unresolved ID preserve known commonality of the reference, while leaving the nature and upstream history of the represented source unresolved.

## 7. Assertion envelope and scope

Each Assertion has required `id`, `assertion_kind`, `scope`, `provenance`, `asserted_at`, `lifecycle_state`, `lifecycle_basis_ref_ids` and `data`. `gaps` and `extensions` are optional.

| Field | Meaning |
|---|---|
| `assertion_kind` | `relation` or `assessment` |
| `scope` | Object with `inquiry_refs`, `claim_refs` and `effective_window` |
| `asserted_at` | TimeValue for assertion creation, distinct from occurrence time |
| `lifecycle_state` | `active`, `withdrawn`, `superseded` |
| `lifecycle_basis_ref_ids` | EvidenceReference IDs supporting withdrawal/supersession; empty for a newly active assertion |

`scope.inquiry_refs` is nonempty. `scope.claim_refs` names the exact Claim versions to which the assertion applies, all within the targeted claims of each named inquiry. It can be empty for inquiry-scoped identity/organizational metadata. Empty does not mean every claim.

A claim-lineage or stance assertion must include the bound claim. Origin-boundary, independence and externality assessments require nonempty claim scope as well. When a compared subject is an EvidenceItem, its bound claim must be in that scope. A Metadata assertion with no claim scope can support model/actor role disclosure inside its inquiry, but cannot become acquisition evidence for every contribution. `effective_window` is a TimeWindow; unknown time limits conclusions but does not erase the assertion.

A nonactive lifecycle state requires supporting reference(s) and a qualification explaining the change. A mere assertion from someone else that a claim was superseded is not permission to delete the original. History remains in the snapshot. Explicit competing assertions are preserved; no newest-wins or authority-prestige-wins rule is applied.

## 8. Relation registry

### 8.1 RelationAssertion data

A relation's `data` has exactly `predicate`, `from_ref`, `to_ref`, `polarity`, `dimension` and `details`.

`polarity` is `affirmed` or `denied`. A denial is retained as a supplied statement. It is never turned into an affirmative independence claim. Only affirmed, applicable relations can supply positive traversal edges, subject to disputes and evidence qualification.

`dimension` is a core dependency dimension where required; otherwise it is null. `details` contains only the fields permitted by the predicate group in §8.3. Every edge has one direction. Displaying a reverse relationship cannot create a second independent assertion.

For the table, E = EvidenceItem, A = Artifact, O = OriginEvent, M = Model, S = SourceActor, C = Claim, V = Evaluation, H = CorrectionChannel, and R = any Assertion. Compatible UnresolvedReferences can substitute for endpoints except a stance relation's bound Claim, which must be resolved. Unknown endpoints stop the relevant traversal.

| Predicate | Allowed endpoints, from → to | Dimension | Permitted use |
|---|---|---|---|
| `supports` | E → its bound C | Null | Supplied supporting stance; no truth certification |
| `contradicts` | E → its bound C | Null | Supplied opposing stance; no automatic falsity |
| `describes` | E → its bound C | Null | Documentary/descriptive role |
| `qualifies` | E → its bound C | Null | Supplied qualification |
| `contextualizes` | E → its bound C | Null | Supplied contextual role |
| `corroborates` | E → E, both bound to the same C | Null | Supplied agreement; no independence inference |
| `cites` | A → A | Null | Citation graph only |
| `derived_from` | A → A or E → E, same kind at both endpoints | Null for A; a core dimension for E | Material or claim-bound ancestry, in separate views |
| `copies` | A → A or E → E, same kind | As for `derived_from` | Recorded copying |
| `syndicated_from` | A → A or E → E, same kind | As for `derived_from` | Recorded republication |
| `summarizes` | A → A or E → E, same kind | As for `derived_from` | Recorded summary transformation |
| `translates` | A → A or E → E, same kind | As for `derived_from` | Recorded translation transformation |
| `quotes` | A → A or E → E, same kind | As for `derived_from` | Recorded quoted-material ancestry; no inherited stance |
| `originates_from` | E → O | A core dimension | Associates a contribution with a recorded evidence-producing process |
| `depends_on` | O → O | A core dimension | Dependencies among origins in the named dimension |
| `generated_by` | A or E → S or M | Null | Generator disclosure; not an acquisition-root edge |
| `published_by` | A → S | Null | Publisher role; not acquisition ancestry |
| `model_derived_from` | M → M | `model_ancestry` | Recorded model derivation |
| `trained_on` | M → A of kind `dataset`, or an explicit unresolved dataset endpoint | `model_ancestry` | Disclosed training-material reference at recorded granularity |
| `owned_by` | S or M → S | `organizational_control` | Organizational/control view only |
| `retrieved_from` | A → A | Null | Source of a retrieved material copy; no automatic independent observation |
| `propagates_to` | H → H, C, A, E, M, V or R | Null | Declared correction-routing possibility, subject to action and authority |
| `supersedes` | A → A, C → C, M → M, or R → R; same kind | Null | Explicit version/statement succession, never automatic truth or ancestry |
| `same_identity_as` | A → A, S → S, O → O or M → M; same kind | Null | Identity-match assertion at its specified identity level; no automatic merge |

For every E → E relation, both resolved EvidenceItems must bind the same Claim version, and that claim must be in the assertion scope. An unresolved E endpoint requires the source item's bound claim in the scope and an explicit statement of the expected claim role in its gap description. Cross-claim material dependence must be represented by claim-specific EvidenceItems or artifact-level history; it cannot be introduced through implicit equivalence.

A generic `depends_on` edge is deliberately restricted to OriginEvents. It cannot connect arbitrary objects and thereby bypass the typed views.

### 8.2 Cardinality and reuse

All relation families permit multiple supplied assertions about the same endpoints. One EvidenceItem can have several stance assertions or several relevant parents. Conflicting stance or parent assertions survive.

Repeated assertions do not create additional observations. Multiple paths to one supplied OriginEvent do not create additional OriginEvents. Parallel edges retain their assertion IDs and basis, while a later count must explicitly select its counted unit.

`supersedes` to the same ID is structurally invalid. Other self-reference, including self-citation or self-derivation, is retained for the appropriate cycle finding. No general DAG constraint rejects all cycles at ingestion.

### 8.3 Predicate details

| Predicate family | Permitted fields in `details` |
|---|---|
| Stance and `corroborates` | Optional `note` string |
| `cites` | Optional `citation_locator` string, `note` string |
| Six material transformation predicates | Optional `transformer_ref` (Actor/Model/compatible unresolved), `method_ref` (Artifact/compatible unresolved), `occurred_at` (TimeValue), `portion_note` string |
| `originates_from`, `depends_on` | Optional `dependency_note` string, `portion_note` string |
| `generated_by`, `published_by`, `owned_by` | Optional `role_note` string, `valid_window` (TimeWindow) |
| `model_derived_from`, `trained_on` | Optional `stage_note` string, `subset_descriptor` string, `occurred_at` (TimeValue) |
| `retrieved_from` | Optional `retrieval_time` (TimeValue), `portion_note` string |
| `propagates_to` | Required `action_type` (Action), `valid_window` (TimeWindow); optional `route_note` string |
| `supersedes` | Required `reason` string; optional `effective_at` (TimeValue) |
| `same_identity_as` | Required `identity_level`: `artifact_version`, `actor`, `origin_event` or `model_version`; optional `identity_note` string |

The `same_identity_as` level must match the endpoint kind. Shared work families or model-family labels cannot be encoded as same-version identity. Assertions of matching identity are preserved and reported; canonical replacement of IDs is not performed implicitly.

### 8.4 Candidate predicates represented through record links

Several plan candidates express roles or process stages that need more detail than a bare edge. They are represented canonically as follows:

| Candidate wording | Canonical storage | Effect |
|---|---|---|
| `observed_by` | OriginEvent `performed_by_refs` with observation kind | A record-provenance-bearing role link |
| `validated_by`, `evaluated_by`, `judged_by` | Evaluation `target_refs`, `evaluation_kind` and `role_bindings` | Preserve candidate, method and actual reviewer/judge separately |
| `corrects` | CorrectionEvent submission, handling and change records | Prevent an objection or accepted request from masquerading as an observed change |
| `appeals` | CorrectionEvent `submission_kind = appeal` plus targets and later handling | Preserve request and outcome without operating an appeals service |
| `observes_independently` | Independence assessment of specified OriginEvents in `acquisition` | Require positive scoped process evidence |

These candidate names are not accepted predicate aliases in this contract. A caller's adapter must construct the canonical records explicitly and retain its transformation provenance. The future runtime will not guess the intended alias.

## 9. Assessment registry

AssessmentAssertion `data` has exactly `assessment_kind`, `subject_refs` and `details`. Its shared assertion envelope supplies scope, attribution, method, evidence, time and lifecycle. The nine kinds below are exhaustive for the core proposal.

A subject can be an explicit compatible UnresolvedReference where the concept is meaningful, but no qualified result is created from its placeholder status.

### 9.1 `origin_boundary`

Subject: exactly one OriginEvent.

Required detail fields: `dimension`, `boundary_role`, `coverage_ref`, `termination_reason`.

`dimension` is one core dependency dimension. `boundary_role` is `documented_origin`, `declared_origin`, `reference_baseline`, `scope_cut` or `unresolved`. `coverage_ref` is a coverage assessment or null with a Gap. `termination_reason` is a nonempty string specifying why tracing is asserted to stop.

The assessment must include the relevant claim scope. `documented_origin` additionally needs supporting supplied material or a protected attestation and a method. A label without this basis remains a declared documentary assertion with a qualification gap. Neither `documented_origin` nor `declared_origin` implies independence.

Any applicable upstream dependency in the same dimension must remain visible. A caller can name a baseline intentionally, but the result keeps that baseline status. Unknown or disputed upstream history cannot be silently closed by this assessment.

### 9.2 `independence`

Subjects: at least two distinct records, all of one compatible kind chosen from EvidenceItem, OriginEvent, Evaluation, Model or Actor. Mixed-role questions use separate assessments and a common inquiry context.

Required detail fields:

| Field | Meaning |
|---|---|
| `comparison_form` | `pairwise` for exactly two subjects, or `setwise` for an explicitly supplied finite set |
| `dimension` | One core dependency dimension |
| `conclusion` | `independent_process`, `shared_dependency`, `partial_overlap`, `unknown`, `not_assessed`, `not_applicable` |
| `examined_dependency_refs` | List of relevant relation/assessment Assertion IDs; may be empty |
| `unexamined_dimensions` | List of core dimension names; required, possibly empty with an explicit method qualification |
| `coverage_ref` | Coverage assessment or null with Gap |
| `scope_note` | Nonempty statement of what the process assessment covers and omits |

The documentary conditions in definitions §9.3 control how this assessment may be described. `independent_process` is a supplied conclusion, not a runtime fact flag. A self-declaration, locator-only support or unknown assessor remains disclosed at that basis. A protected attestation can support a protected-assessment description with its limitations; it does not become public independent verification.

A relevant unresolved conflict prevents an unqualified independence conclusion. Pairwise input cannot be silently promoted to a jointly independent set, and there is no transitive completion. Work Unit 4 separately owns any qualified count.

### 9.3 `coverage`

Subjects: one or more Inquiry, Artifact, OriginEvent, Model, Evaluation, CorrectionChannel or PipelineRecord IDs.

Required detail fields: `coverage_kind`, `state`, `relation_types`, `dimensions`, `member_refs`, `omitted_refs`, `universe_enumerated`, `scope_note`.

`coverage_kind` is `upstream_history`, `citation_list`, `identity`, `model_history`, `correction_routes`, `pipeline_universe` or `other`. `state` is `complete_for_scope`, `partial` or `not_examined`. `relation_types` is a list from the core relation registry; `dimensions` uses the core dimensions. `member_refs` and `omitted_refs` identify supplied records or explicit unresolved references. `universe_enumerated` is a boolean describing whether the relevant finite population is listed. `scope_note` is nonempty.

`complete_for_scope` is attributed completeness, limited by the assertion's inquiry, time, kinds and scope note. It can be challenged. It cannot authorize a universal statement about all sources or routes. An unknown branch inside the claimed complete scope produces a coverage inconsistency; the tool does not discard the unknown branch.

A retention population requires `coverage_kind = pipeline_universe`, an explicit subject/stage comparison and `universe_enumerated = true`. Empty enumerated membership may mean a known empty set; a missing population does not mean zero eligible items. The later metric specification handles zero denominators.

### 9.4 `classification`

Subjects: relevant Artifacts, EvidenceItems, Actors, Evaluations or Anomalies.

Required detail fields: `axis`, `labels`, `verification_assessment_refs`, `scope_note`.

| Axis | Core labels |
|---|---|
| `sil_data_role` | `surface_linguistic`, `world_model`, `judgment` |
| `hdl_structure_role` | `surface_linguistic_structure`, `world_structure`, `judgment_structure` |
| `sil_governance_layer` | `open_web`, `verified`, `contested`, `judgment` |

`labels` is a nonempty list in one axis. Multiple classification assertions can coexist. A `verified` governance label needs a referenced verification assessment; otherwise it remains an unsupported classification, with no verified-process qualification. No content-level trust weight is calculated.

A governance `judgment` label needs an explanation of the recorded human contribution to fulfill the SIL function. A model artifact can have a SIL data-role judgment classification without satisfying that governance function. [SIL, pp. 6-7, 13-16; SIT-D002, SIT-D011]

### 9.5 `verification`

Subjects: Actor, Artifact or Assertion records concerning identity/process.

Required detail fields: `verification_scope`, `evaluation_ref`, `reported_outcome`, `valid_window`, `scope_note`.

`verification_scope` is `identity`, `process`, `byte_integrity` or `other`, with `other` requiring an explicit identity/process explanation. `evaluation_ref` identifies an Evaluation or is null with a Gap. `reported_outcome` is `verified`, `not_verified`, `inconclusive`, `revoked` or `unknown`. `valid_window` is a TimeWindow. A claim's substantive truth is outside this verification assessment.

This records a verifier's reported outcome. It does not cause the toolkit to perform signature checking, external identity verification or source authentication. The verifier and evidence need their own disclosed basis. Expiry and revocation remain time-sensitive record facts.

### 9.6 `externality`

Subjects: OriginEvent or EvidenceItem records.

Required detail fields: `boundary_inquiry_ref`, `conclusion`, `grounding_basis`, `relevant_time`.

The referenced inquiry must occur in the assertion scope. `conclusion` is `external`, `internal`, `mixed` or `unknown`. `grounding_basis` is a nonempty scoped explanation or null with Gap. `relevant_time` is a TimeValue.

This assertion must explain the relationship to that inquiry's system boundary. Neither a remote locator, a human label nor a recent timestamp is sufficient by itself. The underlying origin's integrity and influence remain separate questions.

### 9.7 `authority`

Subject: exactly one CorrectionChannel.

Required detail fields: `target_refs`, `action_types`, `valid_window`, `authorized_by_ref`, `grant_state`, `authority_basis`, `coverage_ref`.

Targets use the CorrectionChannel target types. `action_types` uses Action values. `authorized_by_ref` is an Actor or compatible UnresolvedReference. `grant_state` is `granted`, `denied`, `expired` or `unknown`. `authority_basis` is a nonempty explanation or null with Gap; `coverage_ref` is a coverage assessment or null with Gap.

Applicable authority requires target, action, time and scope alignment, together with the reported grant and its basis. A channel's owner, mailbox or action list cannot create its own authority by structural existence alone. Unknown timing limits time-specific applicability; it does not erase a separately documented past action.

### 9.8 `capacity`

Subjects: CorrectionChannel or Evaluation records.

Required detail fields: `reported_capacity`, `unit`, `horizon`, `reported_load`, `scope_note`.

Capacity and load are strings or null with Gap, preserving the external assessor's description. `unit` is a string or null with Gap. `horizon` is a TimeWindow. No capacity normalization, queueing model, adequacy threshold or forecast is computed in this contract. The records support disclosure of what was measured or asserted about sustained handling. [SIT-T034, SIT-T039]

### 9.9 `conflict`

Subjects: at least two Assertion IDs.

Required detail fields: `conflict_kind`, `resolution_state`, `resolution_evaluation_ref`, `scope_note`.

`conflict_kind` is `affirmation_denial`, `incompatible_origin`, `incompatible_independence`, `identity_dispute`, `scope_dispute` or `other`. `resolution_state` is `unresolved` or `externally_resolved`. `resolution_evaluation_ref` is null for unresolved conflicts or a supplied Evaluation record for an externally resolved conflict.

An external resolution record is retained with its attribution and authority limits. It does not automatically delete assertions or choose a winner. Current use of an assertion changes only through an explicit lifecycle update with basis. An appeal or counter-resolution can remain visible. No prestige-weighted adjudication occurs.

## 10. Graph views and permitted derivation

The audit graph contains different relation families. Every traversal must name its view, inquiry, claim where relevant, dimension and temporal/coverage limits. There is no unrestricted all-edge ancestry operation.

### 10.1 Eligibility of supplied relations

A relationship can be used as a current positive premise only when it is structurally valid, affirmed, active, applicable to the specified inquiry and scope, and compatible with the view's endpoint rules. Unknown effective time is disclosed as a limitation; it must not silently pass a time-specific eligibility requirement.

An active denial of an otherwise matching relationship, an explicit conflict assessment, or a directly incompatible recorded dependency produces a dispute. A disputed edge may be shown as an attributed possible relationship, but a finding requiring uncontested evidence cannot use it without that limitation.

All original records remain available. There is no global confidence threshold that deletes unattributed or weaker sources. The view's eligibility and the result's evidence qualification are separate operations. A declaration-only path can still be reported as a declaration-based path.

### 10.2 View registry

| View | Edges / record links | Allowed conclusion | Forbidden shortcut |
|---|---|---|---|
| Citation | `cites` on Artifact versions | Supplied citations and citation cycles | Citation implies endorsement, derivation or independent observation |
| Material transformation | Artifact-level six transformation predicates plus `retrieved_from` | Document transformation/history | Apply every artifact parent to every claim |
| Claim-origin, for one dimension | E-level six transformation predicates, `originates_from`, OriginEvent `depends_on`; exact claim/dimension scope | Recorded parent paths, origin boundaries and unresolved frontiers | Follow publisher, support or correction edges as acquisition ancestry |
| Model/evaluation | Evaluation role bindings, `generated_by`, `model_derived_from`, `trained_on` | Role-specific disclosed common model/material ancestors | Family label or endpoint count proves independent behavior |
| Organizational | `owned_by`, with relevant supplied actor/model roles | Disclosed common ownership/control | Common ownership proves copied content |
| Stance/contestation | Five E → Claim stances, `corroborates`, classification/conflict records | Preserved supplied support, disagreement and qualifications | Count stances as independent votes or propagate truth |
| Correction routing | CorrectionChannel targets and `propagates_to`, with action/time/authority assessments | Declared or applicable scoped routing evidence | A path proves a handled correction |
| Correction outcomes | `case_ref`, before/after links and event provenance | Recorded handling and linked changes | A later edit or acknowledgment proves substantive success |
| Pipeline stages | PipelineRecord subject/output links and scoped coverage | Recorded admission, retention, selection and use | Reconstruct missing stages or adequate renewal from one log |
| Assertion assurance | Provenance support pointers, verification and conflict assessments | Disclosure of basis, support cycles and disputes | A circular attestation chain certifies itself |

Role bindings and record links in this table are canonical projections of fields, inheriting their parent record provenance. They do not count as independently supplied corroboration merely because a graph display renders them as edges.

### 10.3 Claim-origin tracing

Start from the inquiry's `seed_evidence_refs`, separately for each bound Claim and selected dependency dimension. Trace only the permitted claim-origin edges with matching scope. Artifact identity and provenance references are displayed as context; they cannot substitute for claim-qualified origin edges.

A trace may encounter several parents, a shared ancestor, a supplied origin boundary, a scope cut, an unresolved endpoint, a disputed relationship or a cycle. These outcomes can coexist. Preserve the corresponding record and assertion IDs instead of forcing one root.

An OriginEvent terminates as a supplied origin boundary only through the appropriate assessment. A terminal E or O without such qualification remains an unqualified terminal. A declared baseline or scope cut stays explicitly labeled. Known upstream parents and mismatched completeness assertions remain visible.

There is no automatic zero/one root assignment at an unqualified terminal and no finite global upper bound on omitted ancestry.

### 10.4 Multi-parent attribution

Parentage is many-to-many. Paths can converge and branch. A graph can establish that E depends on O1 and O2 while leaving the share of contribution unresolved. The graph cannot obtain 50/50 weights merely because two parents exist.

Evidence-item counts, ancestor sets and witness paths have separate units. Work Unit 4 owns any allocation and concentration convention, including how unallocated or unresolved contribution stays in a denominator. This unit does not select one.

### 10.5 Common origin and independent process

Recorded common ancestry supports a scoped common-ancestor finding with witness paths and source basis. Absence of a common recorded path does not establish independence.

An independence assessment is evaluated against its own documentary prerequisites and relevant contrary records. Known common acquisition ancestry can conflict with independent acquisition while remaining compatible with independent methods. Identity uncertainty and disputed parentage must limit affirmative qualification.

A group of pairwise assessments does not authorize a new setwise assessment. A graph-derived result cannot relabel a supplied declaration or investigator inference as direct external observation. No maximal-independent-set search or statistical independence test is promised.

### 10.6 Model, reference and rubric overlap

Begin with the explicitly supplied Evaluation roles. A shared object in two roles can be disclosed directly. A shared model or training-material ancestor requires permitted recorded lineage. Rubric and reference material use their own material history, without turning shared formatting into automatically shared judgment.

If both models identify dataset D but their supplied subset descriptors differ, report the shared dataset reference at that granularity. Overlap of exact training examples remains unresolved unless separately provided. Model-family labels and absent training disclosures receive separate limitations.

### 10.7 Temporal and revision behavior

Different versions remain distinct nodes. A versioned feedback chain can be acyclic even when model-development and evaluation roles repeat over time. Reusing one unversioned node for the entire history can create ambiguity; preserve the ambiguity instead of inventing versions.

A citation cycle concerns citations. A claim-origin dependency cycle concerns ancestry assertions. A model cycle concerns model-version lineage. A supersession cycle concerns succession. These are separate findings with their own witness types.

Known dates that make an asserted transformation temporally impossible produce a temporal inconsistency. Unknown dates or overlapping date-only intervals produce uncertainty, not a fabricated ordering. No cycle is itself proof that the target claim is false.

## 11. Corrections and pipeline semantics

### 11.1 Possible route and applicable route

A channel's target list supplies a declared direct route. A `propagates_to` chain supplies additional declared routes. For an action-specific applicable route, every required leg must retain its applicable scope, effective time, action and authority evidence. Channel existence cannot substitute for those records.

The authority assessment is an imported grant or denial, not independent legal or institutional verification. Unknown applicability must remain explicit. A granted action for one target/version does not authorize a different target/version by name similarity.

A lack of recorded route means only that no route was recorded within the examined view. An attributed complete-route assertion can support a narrower absence description for that stated boundary. It cannot prove global impossibility.

### 11.2 Handling and effect

`submission` creates a recorded case. `handling` reports the process outcome for that case. `change` supplies linked before/after evidence. Different records can come from different actors and can conflict. A handling acceptance and a later recorded failure are both retained.

An observed change with unknown channel authority remains an observed change with unknown authority. An authorized route without a change record remains an authorized-route assertion without evidence of use. One case cannot establish sustained throughput.

A supplied before/after link can establish recorded attribution to the case. The report must retain whether the basis was a use log, explicit process record, protected attestation, upstream inference or bare declaration. It does not independently identify causality.

### 11.3 Preservation and retention

PipelineRecords identify the relevant run, stage, subject and observed relation. An earlier admitted item and a later selected item can be compared only when the supplied identity/mapping and inquiry support the comparison.

An omitted final citation is not necessarily an omitted contribution. An answer may have used material without citing it, and citations may be listed without demonstrated use. Preserve supplied selection, use and citation evidence separately.

A known eligible universe must be explicit before a retention ratio can be defined. A caller-provided complete input set is still caller-provided coverage. A final-only dossier cannot reveal all earlier exclusions or infer motive.

## 12. Disputes, identity and assurance handling

### 12.1 Conflicting but well-formed assertions

The following are retained as data-quality/evidence conflicts:

- affirmed and denied relations with the same applicable endpoints, type, dimension and scope;
- a claimed independent-acquisition set with a relevant common acquisition witness;
- an origin-boundary label contradicted by an in-scope upstream dependency;
- claimed complete coverage containing unresolved in-scope branches;
- incompatible same-identity and distinct-origin narratives;
- contradictory correction outcomes or incompatible temporal records.

Textual disagreement not encoded in the records is not automatically discovered. The toolkit is not a semantic conflict classifier. It can preserve an externally supplied conflict assessment and later detect only specifically defined structural incompatibilities.

### 12.2 No silent entity merger

A `same_identity_as` assertion can connect two representations. It is not automatic permission to canonicalize them or count two process roots as one verified origin. The input preparer can submit a corrected snapshot using a common canonical ID with a documented mapping, while retaining the earlier representation in history.

Until identity is sufficiently resolved for the requested question, inventory counts may describe record counts, and a qualified independent-origin count remains limited. Multiple alias IDs do not supply positive process-independence evidence.

### 12.3 No automatic winner

Prestige, more citations, a newer timestamp or majority agreement cannot choose a winning assertion. An externally supplied adjudication is represented as an Evaluation/conflict resolution with its own evidence. It has the authority actually documented, and remains contestable.

Assertions marked withdrawn or superseded are excluded as current positive premises where their lifecycle basis supports that status. They remain in the historical record. A relation asserting supersession cannot rewrite an old answer's actual evidence path. Lifecycle state describes the supplied snapshot. Historical state reconstruction is not inferred from that state alone; a historical analysis requires the relevant earlier state or explicit history to be supplied, with any missing effective time kept unresolved.

### 12.4 Exact runtime findings reserved

This section defines the issues a future implementation must represent. It does not assign final machine report status codes, severities, confidence scores or thresholds. Those require the later threat, observability and validation work units.

## 13. Input normalization and deterministic interpretation

The proposed core is deliberately strict:

1. Parse one UTF-8 JSON object. Reject duplicate object keys, non-finite numerical values, malformed syntax and incompatible envelope versions.
2. Validate known structural types and required fields. A Python boolean cannot be treated as an integer by a permissive implementation shortcut.
3. Reject duplicate IDs and accidental dangling references. Preserve explicitly modeled unresolved references.
4. Keep original text, identifiers, source labels, locators and time precision. Do not lowercase IDs, trim meaning-bearing content, resolve URLs or merge matching names.
5. Check endpoint-kind and exact claim-scope compatibility. A generic source relation cannot be guessed into a canonical edge.
6. Preserve structurally valid disputes, missing evidence, protected identities and cycles for analysis.
7. Keep input order as supplied record metadata where relevant; substantive set membership is unordered. Later output ordering must be deterministic without relying on ingestion order as evidence priority.

There is no global input dictionary that treats a field named `trust`, `verified` or `score` in free text as policy. Unrecognized fields belong only in declared inert extensions; otherwise they are structural errors. Narrative source content cannot change normalization rules.

A textual observation that includes code remains untrusted text. Its presence is not permission to execute it. Exact byte limits, nesting limits, path protections and denial-of-service budgets remain required Work Unit 9 decisions before implementation; this specification supplies no unlimited-processing promise.

## 14. Rejection versus reportable limitations

| Condition | Structural disposition | Analytical consequence |
|---|---|---|
| Invalid JSON, duplicate JSON keys or unknown contract version | Reject the bundle as structurally invalid | Do not issue an ordinary analytical success report |
| Duplicate ID anywhere in the snapshot | Reject | Do not invent renamed IDs or choose one record |
| Dangling local reference | Reject | Caller must supply the record or an explicit UnresolvedReference |
| UnresolvedReference with compatible expected kind | Accept | Stop/limit the relevant trace; preserve the gap |
| Incompatible endpoint type or E → Claim stance aimed at a different claim | Reject | No coercion or implicit claim equivalence |
| Unknown canonical enum/predicate outside extensions | Reject | No similarity-based alias matching |
| Malformed time value, nonconforming date or missing timezone for an instant | Reject | No local-time default |
| Structurally valid records with reversed known event order | Accept with temporal inconsistency | Limit the affected ancestry/correction claim |
| Valid citation or dependency cycle | Accept | Report the appropriate cycle; do not force a DAG |
| Missing evidence for an independence or origin label | Accept | Preserve declaration and qualification gap; no unqualified finding |
| Contradictory assertions or disputed identity | Accept | Preserve competitors and limit affected conclusions |
| All ancestry unknown | Accept | Inventory plus unresolved frontiers; no invented root total |
| Missing correction authority but observed linked change | Accept | Preserve the observed change and unknown authority separately |
| No intake universe for retention | Accept | Preserve final records; retention rate is unavailable |
| Protected source with stable opaque ID | Accept | Preserve known common references and assurance limits |
| Unknown numeric/resource budget for implementation | No runtime judgment made in Phase 0 | Blocks implementation readiness until the assigned specification resolves it |

A rejected bundle may receive a validation-diagnostics artifact under the future report contract. Such diagnostics must not be presented as a completed source-integrity audit. Partial analytical salvage of a structurally rejected bundle is outside this contract proposal.

## 15. Representation witnesses

The cases below instantiate the ontology in prose. IDs are illustrative and belong only to each case. They are not executable fixture files or golden report fields. Their purpose is to show that distinct evidence structures remain distinguishable under these definitions.

### W3-01: Several publishers, one origin

For C1, artifacts A1-A5 have separate publisher records. EvidenceItems E1-E5 bind C1. E1 originates from O1; E2 and E3 copy E1; E4 summarizes E2; E5 is derived from E1. The edges all carry C1/acquisition scope, supporting references and the applicable inquiry. O1 has a scoped origin-boundary assessment.

Expected interpretation: five listed seed artifacts and one shared supplied acquisition origin. Publisher plurality remains visible. No global independence, truth or adequate-presence result follows. Removing the origin-boundary assessment leaves a shared OriginEvent record whose termination is unqualified.

### W3-02: Separately documented observations of one event

O1, O2 and O3 share an external `event_key`, but have distinct performed-by and acquisition records. E1-E3 each originate from the respective origin. A setwise acquisition-independence assessment identifies all three, its method, evidence, coverage and unexamined dimensions.

Expected interpretation: three represented collection processes with a qualified supplied acquisition assessment. The common external event key does not create a copy edge. Other dimensions remain unassessed where specified. A future independent-origin count still requires Work Unit 4's explicit rule.

### W3-03: One artifact, different claim roles

Artifact A records an organization's statement. E1 binds claim C_statement about what that organization said and originates from documentary issuance O_statement. E2 binds C_event about the underlying event and has an explicit derivation from E3, representing A's reliance on another report.

Expected interpretation: A can be a documentary origin for C_statement and derivative evidence for C_event. A single artifact-global original/derivative flag could not represent this case and is therefore absent.

### W3-04: Independent source contradicts many derivatives

E1-E5 are derivatives of O1 and support C1 through supplied stance assertions. E6 originates from O2 and contradicts C1. A qualified acquisition assessment concerns O1 and O2; their disagreement is retained.

Expected interpretation: derivative repetition does not become five independent votes. The tool preserves two source lineages and opposing supplied stances. It does not decide which claim is true or assign equal evidentiary weight.

### W3-05: Unknown upstream and accidental reference error

E1 derives from U1, an UnresolvedReference expected to denote an EvidenceItem. U1 records withheld acquisition history. A second, otherwise identical dossier refers to nonexistent ID U_missing without defining it.

Expected interpretation: the first dossier is valid and contains a disclosed unresolved frontier. The second is structurally invalid. Neither permits a hidden-root count. Three distinct unresolved placeholders would count three represented gaps, without establishing three hidden origins.

### W3-06: Two analyses of one dataset

O_analysis_1 and O_analysis_2 have separate analysts and method records. Both `depends_on` O_collection in the acquisition dimension. E1 and E2 originate from their analyses, with explicit dimension-scoped ancestry connecting their acquisition history to O_collection. A method-independence assessment has its own basis.

Expected interpretation: separate analysis origins and one documented shared collection origin. Method independence can coexist with acquisition dependence. No second data collection is created because a second analysis exists.

### W3-07: Model-generated reference and related judge

Evaluation V targets candidate A_candidate. Its generator binding identifies M_generator, its judge binding identifies M_judge, and its reference/rubric bindings identify artifacts with recorded generation history. M_generator and M_judge derive from M_base.

Expected interpretation: disclosed shared model ancestry with explicit role witnesses. Distinct model endpoints do not supply independent evaluation. The shared ancestry is not a numerical error correlation or proof of any particular wrong judgment.

### W3-08: Human review with limited known ancestry

Evaluation V includes a protected human-reviewer Actor H, a substantive contribution description and an attestation. H's access to prior model-generated material is unresolved. A separate execution result is recorded as an execution Evaluation.

Expected interpretation: a protected human contribution, unresolved dependencies and a distinct execution constraint are all visible. A human label alone cannot close the dependency gap. The execution record does not become human judgment.

### W3-09: Applicable correction route and observed partial propagation

A submission K0 targets A_old through H0. A handling event K1 accepts the request. H0 has a scoped action grant. A change K2 links K0 to A_new with supplied process evidence. B_old, a downstream derivative, has no linked change record; another derivative C_old has a supplied linked C_new change.

Expected interpretation: accepted handling and two specified linked changes are represented. B's downstream correction remains undocumented unless a scoped negative observation is supplied. Lack of a B change record cannot automatically prove that no B correction happened. Authority and capacity remain separate.

### W3-10: Mailbox, rejection and correction sink

H_mail has a contact locator but no authority assessment. K0 is submitted there. A handling event K1 records a reasoned rejection. Coverage is partial and no change record is supplied.

Expected interpretation: declared contact route and recorded rejection, with authority and downstream effect unestablished. The report cannot declare global no-route status or substantive correctness of the rejection. A demonstrated sink would require additional scope, coverage and handling evidence under the later threat specification.

### W3-11: Citation cycle versus versioned feedback

A1 cites A2 and A2 cites A1. Separately, M1 generates evaluation artifact A_test_1, and a recorded development chain later produces M2. The caller supplies distinct versions and times.

Expected interpretation: a citation cycle in the first graph. Repeated model/evaluation roles over distinct versions do not necessarily constitute a dependency cycle in the second. No version is invented if the caller instead collapses them into one ambiguous model ID.

### W3-12: Protected common origin

E1 and E2 both reference the same opaque O_private record or the same protected U_private endpoint. A supplied attestation discloses only that the underlying acquisition reference is common.

Expected interpretation: shared recorded reference at the attested granularity, with identity and upstream limits preserved. Redacting a public name cannot transform this into two independent sources. A protected unresolved endpoint still lacks a fully documented origin boundary.

### W3-13: New external input admitted but not selected

O_new has a boundary-qualified externality assessment. A PipelineRecord records admission of E_new. A separate selection record says it was not selected. Preservation and influence are not documented.

Expected interpretation: external-origin assessment, admission and recorded nonselection; preservation and downstream influence remain unknown. Freshness and intake do not establish effective replenishment.

### W3-14: Unclassified anomaly and final-only evidence

Anomaly N keeps original context and has no fitting Claim reference. One dossier contains an enumerated eligible pipeline universe and recorded exclusion of N. Another contains only a final set and no intake history.

Expected interpretation: the first supports a scoped recorded-exclusion description. The second cannot establish suppression. Both preserve N's original context without inventing a new accepted taxonomy or personal demographic label.

### W3-15: Contradictory independence, identity and provenance

A supplied assessment declares O1 and O2 independently acquired. Another active assertion states that both analysis origins depend on O0 in acquisition. A third asserts that two artifact records refer to one version, with conflicting identity evidence.

Expected interpretation: retain the independence assessment, the common-parent witness and the identity dispute. No automatic winner, independent-root total or silent entity merge is permitted.

### W3-16: Independent checking of one object

Two formal-check or execution Evaluations inspect the same target artifact. Their methods/environments may be independently documented, while the target material is necessarily shared.

Expected interpretation: shared target identity and separately assessed validation processes. The target's common identity does not by itself defeat process independence, and method independence does not establish source-acquisition independence. The claim type and comparison dimension control the description.

## 16. Traceability and acceptance coverage

| Requirement / source basis | Realization in this specification | Representation witnesses |
|---|---|---|
| SIT-P001-P003; SIT-T008, SIT-T020, SIT-T022, SIT-T035 | Inquiry, Claim, EvidenceItem, Artifact and origin separation | W3-01, W3-03, W3-06 |
| SIT-P004-P006; SIT-T014, SIT-T016, SIT-T035-SIT-T036 | Typed views, boundary assessments, scoped independence and explicit unresolved endpoints | W3-02, W3-05, W3-11, W3-15 |
| SIT-P007; SIT-T017, SIT-T037 | Parent/contribution sets without invented weights or origin multiplicity | W3-01, W3-04, W3-06 |
| SIT-P008; SIT-T005, SIT-T011, SIT-T018, SIT-T020 | Model record, Evaluation role bindings and human contribution basis | W3-07, W3-08, W3-16 |
| SIT-P009; SIT-T001, SIT-T016, SIT-T029 | Externality and separate PipelineRecord stages | W3-13 |
| SIT-P010; SIT-T024, SIT-T034, SIT-T039 | Channel, authority, case, handling, linked change and capacity | W3-09, W3-10 |
| SIT-P011; SIT-T019, SIT-T021, SIT-T023, SIT-T032 | Anomaly context, conflict preservation and enumerated pipeline universe | W3-04, W3-14, W3-15 |
| SIT-P012-P014; SIT-T004, SIT-T038, SIT-T040 | Qualification gaps, typed rejection, inert references and protected IDs | W3-05, W3-08, W3-12 |
| SIT-P015-P016; SIT-T003, SIT-T027-SIT-T028, SIT-T033, SIT-T040 | No inherited schema, universal score, formal-model substitution or network operation | Entire contract |

The plan's eight mandatory representation cases are covered: many copies of one source (W3-01), several independent observations (W3-02), derivative disagreement versus independent evidence (W3-04), unknown ancestry (W3-05), synthetic summaries (W3-01/W3-07), related evaluator lineage (W3-07), propagated correction (W3-09), and nominal/unproven corrective reach (W3-10).

Future tests must include positive, negative, missing-data and boundary behavior for public fields. Runtime test files and module ownership remain Work Units 7-8 and the later implementation phases. These prose witnesses do not claim a second independent review or running software.

## 17. Decisions, deferred details and stop point

SIT-D019 submits the twelve-kind dossier and role-based specializations. SIT-D020 submits typed assertions, evidence-qualified assessments and view-specific graph semantics. SIT-D021 submits snapshot identity, explicit uncertainty endpoints, strict input rejection and inert extensions. Their details remain submitted for approval in register revision 0.3.

The inherited directions SIT-D001-SIT-D018 are recorded as accepted for Phase 0 definition work. That acceptance does not resolve the later numerical or runtime gates by implication. No HHI, reciprocal count, default attribution split, threshold, final report status enum, compatibility layer, public schema, package identity, dependency, license or security resource budget is adopted here.

After review and acceptance, Work Unit 4 can define the analytical profile using these objects and units. It must stay inside its own file allowlist. This unit ends with the three Markdown files and their archive. No full Phase 0 approval record, Phase 1 plan or repository scaffold is created.

### Reviewed input identities

| Input | SHA-256 |
|---|---|
| Original Phase 0 plan | `2d97a820ae218c33cfd00dd96a762853e887f867973a2b2da0945fc4414495b1` |
| Work Unit 1 `SPEC_AUDIT.md` | `3565ab8f1b08f30e06f4983ffd26adbe8bc977b655ebf410b634918a7ae7949a` |
| Work Unit 1 `THEORY_SOURCE_MAP.md` | `015e65baf3fcad8ce78a2285df8f2de8d5b7b4cbdd347707ba3cc5d5ba46b627` |
| Work Unit 2 `V0.1_PRODUCT_SPEC.md` | `117c3ac96e6101508ff8cb643a94c3544cc111ba93dee054b2fafecb65c1db83` |
| Work Unit 2 `PROJECT_INSTRUCTIONS.md` | `cb5cf8f4d367bceacc313189469b3327370bed0450468d62a968825fee4a7746` |
| Work Unit 2 decision register, revision 0.2 | `904e55c4df0adf7614b990b004c3a90e54e01a382c7b0a271580e056a05fd84c` |

These identify reviewed input bytes. They provide no additional scientific, identity or factual certification.


### Document review completed for this delivery

Local checks confirmed the three-file allowlist, unchanged hashes for thirteen prior inputs, and agreement of the six PDF identities with the Work Unit 1 source register. The inherited eighteen decision bodies retain their original questions, alternatives, recommendations and acceptance conditions. Their new approval entries are separate from those preserved bodies.

The two specifications contain twelve core record kinds, twenty-four relation predicates, nine assessment kinds and sixteen prose representation witnesses. Referenced theory, product and decision IDs resolve within the existing registries and this unit's three new choices. Markdown tables, numbered sections, relative links against the assembled specification set and UTF-8 text were checked. Archive contents and bytes are verified when packaged.

These are authoring, consistency and packaging checks by the same assistant that drafted the documents. No independent external review, runtime graph test, security test, empirical experiment, CI run or GitHub write was performed.

## 18. Work Unit 6 bridge from accepted input to report

### 18.1 Authority and preservation

The WU6 intake is the user's “可以，继续” following the WU5 package. `OBSERVABILITY_AND_REPORTING.md` revision 0.2, §11.1 records contextual acceptance of Option B for SIT-D026 and SIT-D027. The central register remains revision 0.5 because the WU6 allowlist does not permit changing it. The existing SIT-D001-SIT-D025 dispositions and all their qualifications remain in force.

Sections 1-17 above retain the WU3 numbered body verbatim. Their historical references to future analytical/reporting work are answered by definitions revision 0.2 and reporting revision 0.2. No prior input field, record kind, relation predicate, assessment kind, TimeValue, Gap, reference rule, evidence requirement or rejection condition is rewritten here.

This addition specifies the boundary between the accepted `sit-bundle/0.1` input and the newly proposed `sit-report/0.1` logical output. Both labels remain documentation contracts without executable schemas. WU6 does not add a caller-supplied report-control object or an alternative input format.

### 18.2 Output names for existing graph views

The following strings are output labels for the meanings already defined in §§10.2 and 10.7. They do not authorize an all-edge traversal or add a new dependency dimension.

| Input-specification view | Output `graph_view` label | Source of edges/links |
|---|---|---|
| Citation | `citation` | `cites` between Artifact versions |
| Material transformation | `material_transformation` | Artifact transformations and `retrieved_from` |
| Claim-origin in one dimension | `claim_origin` | Same-Claim EvidenceItem transformations, `originates_from`, OriginEvent `depends_on` |
| Model/evaluation | `model_evaluation` | Explicit Evaluation roles, `generated_by`, `model_derived_from`, `trained_on` |
| Organizational | `organizational` | `owned_by` and the appropriate recorded roles |
| Stance/contestation | `stance_contestation` | Explicit stances, corroboration, classification and conflicts |
| Correction routing | `correction_routing` | Channel targets, propagation, action/time and authority evidence |
| Correction outcomes | `correction_outcomes` | Submission/handling/change links and their evidence |
| Pipeline stages | `pipeline_stages` | Pipeline subject/output links and keyed cohort coverage |
| Assertion assurance | `assertion_assurance` | Provenance support, verification and conflict records |
| Succession already described in §10.7 | `succession` | Explicit `supersedes` links between same-kind versions; no ancestry or truth inference |

The eleventh label makes the already-described succession findings identifiable in the report; it does not alter the ten-row §10.2 registry or introduce a new source relation. Inventory/non-graph results use null with an explicit non-graph explanation rather than an invented dependency view.

The five input dimensions remain `acquisition`, `analytical_method`, `model_ancestry`, `evaluation_rubric` and `organizational_control`. A material/citation/stance view does not create acquisition relationships. Names used for display are not accepted input predicate aliases.

### 18.3 Input/output namespace separation

Input IDs retain their global uniqueness within one snapshot. Report-local IDs are unique within one report. References explicitly state their namespace and kind. The same literal string appearing once as an input Claim ID and once as a report Result ID is not object identity.

An input record-link witness identifies its record ID, field/role and target reference. It must not invent a RelationAssertion solely to render a canonical field link as a graph edge. Support pointers remain support pointers; they do not become independent corroborating observations.

Report scope carries `(bundle_id, snapshot_id, inquiry, Claim version where applicable, dimension/view, temporal basis)` plus target and population. Report serialization cannot use a document-level title as an implicit missing Claim. The predecessor field remains informational and triggers no record lookup, import or historical comparison.

## 19. Input-state preservation and result-state mapping

### 19.1 Different meanings of state fields

The input contract contains several state vocabularies. Each must survive under its own qualified record meaning. None directly sets `run.processing_state` or a Result's availability.

| Input field or structure | Output treatment | Forbidden conversion |
|---|---|---|
| `Provenance.basis_kind` | Preserve the supplied value and supporting-reference checks in the basis index | `documented_record` alone creates verified evidence |
| `EvidenceReference.availability` | Disclose supplied/locator-only/withheld/unavailable status and the actual support form | A locator's presence means content was fetched or inspected |
| TimeValue `state` and `precision` | Preserve original time/unknown/withheld/inapplicable representation and its limitations | Unknown source time filled by run time; date-only value treated as midnight |
| Assertion `lifecycle_state` | Retain history; qualify current positive use only with required lifecycle basis | A source allegation of supersession silently deletes the previous assertion |
| Relation `polarity` | Affirmed/denied statements stay attributed; an applicable denial may create a relevant dispute | Denied dependence creates positive process independence |
| Origin `boundary_role` | Preserve documented/declared/baseline/cut/unresolved distinctions with qualifications | Parentless node becomes a documentary origin |
| Independence `conclusion` | Preserve original conclusion; qualify exact set only under definitions §21.3 | A failed qualification becomes a count of zero independent sources |
| Coverage `state` | Preserve its kind, scope, members, evidence and contrary information | `complete_for_scope` proves completeness outside the stated view |
| Verification `reported_outcome` | Preserve verifier, identity/process/byte scope, method, time and result | A source's `verified` outcome becomes a toolkit truth badge |
| Externality `conclusion` | Preserve boundary, grounding and time qualification separately from pipeline stages | `external` automatically means admitted, used or reliable |
| Authority `grant_state` | Preserve grant/denial/expiry/unknown and target/action/time checks | Owning a channel or reporting a past change grants future authority |
| PipelineRecord `state` | Retain `occurred`, `did_not_occur` or `unknown`; derive Y/F/U only under exact keyed member rules | Missing record or unknown observation becomes a negative occurrence |
| Handling `outcome` | Preserve all supplied outcomes for the case and their separate times/bases | Input `failed` changes the audit run to failed, or input `accepted` means correct |
| Change `after_ref` | Qualified nonnull state or explicit supported removal; unresolved target stays unresolved | Null unknown after-state becomes successful retraction |
| Conflict `resolution_state` | Preserve the external resolution and Evaluation basis; required lifecycle update still governs current use | A declared resolution creates an automatic winning source |
| `classification_state` and classification labels | Preserve supplied axes and unclassified anomaly context | Governance layers become credibility levels; no Claim means anomaly rejected |
| Capacity strings, units and horizon | Attributed capacity disclosure only | A number in a string becomes a queueing calculation or adequate-capacity verdict |

An available output may contain unknown or failed native outcomes. For example, a completed audit can produce an available record disclosure of a source-reported handling failure. Conversely, a valid input saying that all sources are verified may produce unavailable qualified results because support was not supplied.

### 19.2 Structural rejection versus completed non-results

The exact structural rejection table remains §14. Duplicate keys/IDs, dangling references, incompatible endpoints and unsupported input enums cause rejection. Explicit compatible UnresolvedReferences, protected context, sparse metadata, well-formed conflicts and cycles remain admitted with the corresponding analytical limits.

The report's rejection envelope contains safe structural diagnostics only. It cannot claim M-family inventories or Level 0 coverage from records encountered before validation failed. Unfinished validation yields processing diagnostics, distinct from a rejected structurally invalid input.

For accepted inputs, relevant gaps become scoped reasons and check outcomes. An unavailable HHI, missing independence assessment or unestablished authorized route does not retroactively reject the valid dossier. An implementation exception is an execution failure, never fabricated as a source-integrity failure.

### 19.3 Conflict relevance and non-winner behavior

An explicit contradictory parent assertion affects the specified Claim, dimension and temporal scope. A separately recorded stance disagreement about that Claim does not automatically contradict its parentage. The report retains all applicable statements without converting majority support, prestige or date into authority.

A relevant unsupported denial still remains a contrary supplied assertion; it cannot be dropped solely to make a documentary calculation available. Its own weak support is also disclosed. An unknown observation by itself need not defeat a separately evidenced positive observation, as definitions §26.2 specifies. These cases must not be handled by one global confidence threshold.

A finding that uses an undisputed witness can remain available even when another branch is unresolved. Complete-set claims, HHI and qualified independent-origin sets must retain their stronger prerequisites. Output formatting cannot remove the unresolved branch from N.

## 20. Canonical input-to-report crosswalk

| Existing input owner | Required report realization | Relevant diagnostic families |
|---|---|---|
| Inquiry seed lists and EvidenceItem claim/artifact bindings | Separate A(I), A(I,C), E(I,C), unresolved artifact references and unassigned seeds; no automatic ancestor inclusion | M001 |
| OriginEvent records, claim-origin relations, boundary/coverage assessments | Reached-origin inventories, boundary disclosures, per-seed memberships, exclusive dispositions and frontier gaps | M002, M004, M007 |
| One independence assessment with its exact subjects | Submitted member count, separately qualified process/origin set count, unexamined dimensions and contrary records | M003 |
| Entire single-origin qualified seed population | Restricted HHI with original N, bucket membership, sum-of-squares numerator and N-squared denominator | M005 |
| Immediate E-to-E and E-to-Origin links with coverage | Direct/inherited/mixed/unresolved partition and permitted point/interval forms | M006 |
| Evaluation roles, Models, material/rubric histories, control links | Exact role identity, strict common ancestors, one-sided ancestry, supplied family-label match and unfinished histories | M008 |
| Boundary-qualified externality assessment | Attributed relation to that Inquiry's system and relevant time | M009 |
| PipelineRecords and finite-cohort coverage anchors | Exact-key observations, Y/F/U partition, conditional fraction/interval and restricted compatible transition | M010 |
| Channel targets, propagation and authority assertions | Declared and applicable authorized routes as separate witness queries | M011 |
| Submissions and their handling/change events | Separate case/event/qualified-target counts, nonexclusive outcomes and explicit removal evidence | M012 |
| Corrective Evaluations, human roles and process comparisons | Actual contributed review, protected basis and qualified process assessment without inherited human-judgment units | M013 |
| Anomaly records, stance/classification/conflict assertions | Unclassified original context, attributed disagreements and eligible M010 stage links | M014 |
| Provenance, EvidenceReferences and coverage declarations | Native-basis/availability inventories, documentary gaps and scope-specific coverage | M015 |

### 20.1 Supported metadata versus qualified evidence

The basis index may inventory a caller's documentary label even when its support is inadequate. It simultaneously exposes the support limitation. This is a two-part output, not silent relabeling of the original source field.

An input attestor can provide inspectable protected testimony while withholding the underlying identity. Report that exact assurance regime and the known common opaque links. An entirely unavailable attestation is not inspectable merely because the reference type is `protected_attestation`. The toolkit is not required to prove every proof, but a self-pointer or pure support cycle cannot serve as sole documentary qualification.

### 20.2 What never becomes a new input requirement

The output reasons/checks/result IDs do not need matching caller records. The auditor derives its own processing and qualification information. No new core input field named `observability_level`, `integrity`, `score`, `threat_status`, `report_state`, `trust_weight`, `analysis_policy` or `reason_code` is introduced.

The raw-input hash, where actually produced, describes bytes read by the future runtime. It is not one of the source Artifact's supplied `checksums` and must not be confused with them. A report's assembly time is distinct from the dossier's `recorded_at` and the source events' times.

Extensions remain inert. An extension that claims a source is clean or instructs omission of an unavailable metric cannot set a core result. A proposed future diagnostic that requires new structured input must return to the owning input/product decision gate.

### 20.3 Cohorts, corrections and comparison integrity

A cohort anchor refers to the exact supplied run/stage key and member IDs. Output normalization cannot merge two candidate baselines by text similarity or silently select the first. When no unique baseline/target pair exists, separate stage reports survive while transition results remain unavailable.

A correction case can include several targets and linked changes. Unknown authority cannot erase a documented past change; documented authority cannot create a change that lacks evidence. An unresolved after-reference prevents qualified change-target counting but remains in the supplied change-event inventory. Multiple events concerning the same `(case_ref, before_ref)` do not multiply the distinct target count.

Comparison across a new dossier/snapshot is not performed merely by reading `predecessor`. Different inquiries in one snapshot retain their different populations and meanings. A lower concentration caused by dropping seeds is not automatically an improvement in the audited real-world system.

## 21. Conformance obligations for this bridge

The future implementation must satisfy the corresponding W6 cases and `SUCCESS_CRITERIA.md` criteria. In particular:

| Bridge obligation | WU6 written coverage |
|---|---|
| Valid sparse input versus structurally dangling reference | W6-01-W6-03 |
| Preserved HHI prerequisites, full denominator and multi-parent distinction | W6-04-W6-07 |
| Relevant conflict, qualified comparison and unexamined evaluator history | W6-08-W6-12 |
| Independent source ancestry, authority and actual change evidence | W6-13-W6-17 |
| Stage-native states, exact cohorts and absent/ambiguous baselines | W6-18-W6-23 |
| Protection, actual support availability and time precision | W6-24-W6-26 |
| Interrupted execution distinct from source missingness | W6-27 |
| Inert rendering and no content detector | W6-28-W6-29 |
| Deterministic semantic output and faithful format parity | W6-30-W6-32 |

These are documentary checks and future test obligations. No parser, graph traversal, detector, runtime unit test, JSON Schema or canonical hero fixture is implemented here.

## 22. Revision 0.2 handoff and remaining gates

This revision preserves the existing input contract and adds its output bridge. The twelve record kinds, twenty-four relation predicates, nine assessment kinds and sixteen W3 witnesses remain unchanged. Any new output-label detail is submitted under WU6-C01-WU6-C03 in reporting §23. The source papers, previous input files and central decision register remain untouched.

After review, WU7 can define its hero and micro-cases using this bridge. WU8 assigns detailed executable-test obligations and later trace owners. WU9 supplies exact resource limits, privacy/export and licensing choices. WU10 selects architecture/API/dependency and canonical serialization details. No complete Phase 0 approval or implementation authorization is issued by this revision.

`SUCCESS_CRITERIA.md` carries the reviewed input hashes and local authoring checks. The three-file WU6 archive is incremental: use these updated lineage/reporting files and the new success document alongside the latest other specification versions. Keep all earlier deliveries as history.

## 23. Work Unit 7 case contract and authority

### 23.1 Instruction, scope and approval record

The user instructed **“继续Work Unit 7”**. This authorizes preparation of the canonical hero and micro-case package under the approved plan's four-file WU7 allowlist. WU6-C01-WU6-C03 are used in their submitted form as the reporting reference for these proposed cases. This instruction is not recorded as a separate retrospective signature approving every pending detail. Adoption of the WU7 golden baseline must include or expressly amend that reporting reference. No complete Phase 0 approval or implementation authorization is issued.

SIT-D001-SIT-D025 retain their recorded dispositions. The acceptance of SIT-D026-SIT-D027 remains in reporting §11.1. The central decision register is outside this unit's allowlist and stays revision 0.5. Reporting and definitions also remain read-only. Existing sections 1-22 below the document header are preserved verbatim in this successor.

The new case records are **fictional, hand-authored conformance inputs**. They instantiate the existing contract; they do not add record kinds, predicates, assessment kinds, metrics, input enums or report codes. The fictitious collection logs, grants and process assessments exercise evidentiary qualification inside the dossier. They supply no empirical confirmation of the source theories and no authentication of a real publisher, human or model.

### 23.2 Division of ownership

| Document | WU7 responsibility |
|---|---|
| This specification, §§24-28 | Canonical hero record inventory, exact graph/bindings, supplied evidence and controlled variants |
| `VALIDATION_PLAN.md`, §§1-8 | Expected logical results, mandatory micro-cases, numerical oracle and promotion constraints |
| `V0.1_PRODUCT_SPEC.md`, §§17-19 | User-visible hero contract, capability coverage and unchanged release boundary |
| `SUCCESS_CRITERIA.md`, §§10-14 | WU7 acceptance obligations, input identities and documented authoring checks |

`H7-01` names the main case, `H7-V01` through `H7-V03` name separately audited variants, and `W7-01` through `W7-28` name micro-cases. These are documentation identifiers, outside the input/output contract namespaces. Exact JSON fixtures, byte-golden reports, command syntax, executable tests and Trace IDs remain later work.

## 24. H7-01: False plurality, independent disagreement and partial correction

### 24.1 Inquiry and temporal boundary

The case concerns a fictional chamber log. Claim `H7-C1` says: **“During chamber run RUN-17, the peak temperature was 24 degrees Celsius.”** One collection process supplied an export reporting 24; a separately documented process reported 21. Later records associate a correction to the first export with some downstream amendments. The toolkit preserves the stated disagreement and the correction record. It does not choose a true temperature.

| Envelope / Inquiry field | Exact case value |
|---|---|
| `contract_version` | `sit-bundle/0.1` |
| `bundle_id` | `H7-BUNDLE` |
| `snapshot_id` | `H7-S1` |
| `recorded_at` | Known instant `2026-01-10T14:00:00Z` |
| `predecessor` | Null; all required before/after material is explicitly in this snapshot |
| Inquiry ID | `H7-I1` |
| `target_claim_refs` | `[H7-C1]` |
| `target_object_refs` | `[H7-ANSWER, H7-EVAL, H7-HREVIEW]` |
| `seed_artifact_refs` | `[H7-A, H7-B, H7-C, H7-D, H7-E, H7-F]` |
| `seed_evidence_refs` | `[H7-EA, H7-EB, H7-EC, H7-ED, H7-EE, H7-EF]` |
| `dependency_dimensions` | `[acquisition, analytical_method, model_ancestry, evaluation_rubric, organizational_control]` |
| `as_of` | Known instant `2026-01-10T14:00:00Z` |
| `time_window` | Known instants `2026-01-10T00:00:00Z` through `2026-01-10T14:00:00Z` |
| `boundary.description` | The represented answer workflow consuming the first export and its A-E derivative chain |
| `boundary.criterion` | External input means a separately acquired observation outside that represented reuse chain, under an attributed process assessment |
| `boundary.system_refs` | `[H7-R1-V1, H7-A, H7-B, H7-C, H7-D, H7-E, H7-MGEN, H7-MJUDGE, H7-ANSWER]` |
| `coverage_assertion_refs` | The eight `H7-COV-*` assessments enumerated in §26 |

The origin/contribution and evaluator results use `snapshot_structural` scope. Action-specific route witnesses use the supplied grant window and the corresponding change/request times; no occurrence time is inferred from dossier assembly. Selection of all five dimensions does not manufacture an acquisition trace for another dimension. Unsupported dimensions retain their own gaps.

### 24.2 Common field conventions for the prose fixture

The following conventions make the tables complete at the logical level without introducing an input macro language. A later fixture author expands them into the existing fields explicitly.

All records/assertions/references have distinct IDs. Record labels are their IDs unless a label is stated. Claim `claim_key = H7-TEMPERATURE`, `version_label = v1`, context is RUN-17 and the quoted peak-temperature statement. Every ordinary Artifact has `work_key` equal to its ID, `version_label = v1`, `locators = []`, `content_evidence_refs = []`, and no checksums, unless overridden below. Artifact `published_at` and `retrieved_at` are TimeValues with state `unknown`, value/precision null and reason “Publication/retrieval time is not part of this supplied fixture record.” The case's process times come from OriginEvents, Evaluations, PipelineRecords and CorrectionEvents.

Every assertion is `active`, has an empty `lifecycle_basis_ref_ids`, and an `asserted_at` of `2026-01-10T14:00:00Z`. Its effective window is `2026-01-10T00:00:00Z` through `2026-01-10T23:59:59Z`. Its scope is `inquiry_refs = [H7-I1]`, `claim_refs = [H7-C1]`, except the model/material metadata assertions in §25.3, whose claim scope is empty. These default times are fictional records supplied for the case, not an inference about a historical system.

All unspecified optional fields are absent. Structural-null fields follow their existing subtype rule. No required nullable factual field is silently null: a listed unknown uses its stated Gap. Required arrays with known empty represented membership are explicitly empty. Empty ancestry arrays do not assert completeness; §26 supplies the only applicable completeness claims.

### 24.3 Actors and models

| ID | Kind / data | Role |
|---|---|---|
| `H7-PREP` | Actor; software_agent; named; display name “Fixture packet preparer” | Dossier transcription and attribution |
| `H7-COL1` | Actor; human; named; “Collector One” | First acquisition |
| `H7-COL2` | Actor; human; named; “Collector Two” | Second acquisition |
| `H7-REVIEWER` | Actor; human; named; “Fixture Process Reviewer” | Supplied collection-process assessment and substantive correction review |
| `H7-EDITOR` | Actor; organization; named; “Fixture Editorial Service” | Declared channel owner and authority grant issuer |
| `H7-MBASE` | Model; model_key H7-base; version v1; family H7-family; provider H7-EDITOR | Shared recorded model ancestor |
| `H7-MGEN` | Model; model_key H7-generator; version v1; family H7-family; provider H7-EDITOR | Answer and summary generator |
| `H7-MJUDGE` | Model; model_key H7-judge; version v1; family H7-family; provider H7-EDITOR | Model judge |

The Actor and Model records use declaration provenance with attribution to H7-PREP, method “Fictional identity/model inventory”, no evidence references, and the limitation that identities are supplied rather than authenticated. Lineage relations have their own documentary support. These declared identities suffice for exact record-label inventories; they do not prove real-world independence.

### 24.4 Artifacts, contributions and observations

| Artifact ID | Artifact kind / version meaning | Contribution / seed role |
|---|---|---|
| `H7-R1-V1` | observation_record; work_key H7-R1; version v1 | Original export; ancestor evidence `H7-ER1`, not a seed |
| `H7-A` | document | Article A, seed `H7-EA` |
| `H7-B` | document | Republished article B, seed `H7-EB` |
| `H7-C` | document | Quoted article C, seed `H7-EC` |
| `H7-D` | document | Model summary D, seed `H7-ED` |
| `H7-E` | dataset | Database record E, seed `H7-EE` |
| `H7-F` | observation_record | Separately acquired log F, seed `H7-EF` |
| `H7-ANSWER` | answer | Answer under review; outside source-seed denominator |
| `H7-REFERENCE` | reference_answer | Model reference answer, outside seed denominator |
| `H7-RUBRIC` | rubric | Evaluation rubric, outside seed denominator |
| `H7-EVAL-RESULT` | judgment | Model evaluation outcome |
| `H7-REVIEW-RESULT` | judgment | Human review outcome |
| `H7-TRAINING` | dataset | Shared named training collection; row overlap unspecified |
| `H7-METHOD1`, `H7-METHOD2`, `H7-CHECK-METHOD` | document, one record per ID | Acquisition/check protocol descriptions |
| `H7-R1-V2` | observation_record; work_key H7-R1; version v2 | Corrected export, outside seeds |
| `H7-A-V2` | document; work_key H7-A; version v2 | Amended A, outside seeds |
| `H7-D-V2` | document; work_key H7-D; version v2 | Amended D, outside seeds |

There are nineteen non-support Artifacts. The eight supporting Artifacts in §24.5 bring the complete artifact-record inventory to twenty-seven. Only the six explicit seeds contribute to M001's nominal source-artifact count. Records used only as ancestors, revisions or validation materials do not become additional independent sources because they exist in the dossier.

| EvidenceItem ID | Artifact | Claim | Epistemic type / contribution |
|---|---|---|---|
| `H7-ER1` | H7-R1-V1 | H7-C1 | measurement; first export's claimed peak 24; ancestor only |
| `H7-EA` | H7-A | H7-C1 | documentary_statement; repeats the first export |
| `H7-EB` | H7-B | H7-C1 | documentary_statement; republishes that report |
| `H7-EC` | H7-C | H7-C1 | documentary_statement; quotes the report |
| `H7-ED` | H7-D | H7-C1 | analytical_inference; model summary based on B, with no new represented acquisition |
| `H7-EE` | H7-E | H7-C1 | documentary_statement; database entry copied from A |
| `H7-EF` | H7-F | H7-C1 | measurement; second collection's claimed peak 21 |

Each EvidenceItem uses locator `entry-1`. Epistemic types describe the **modeled roles within the fictional dossier**. All records retain the fixture qualification; this delivery has collected no physical measurements.

| OriginEvent | Required data |
|---|---|
| `H7-O1` | event_kind data_collection; event_key RUN-17; performed_by_refs [H7-COL1]; method_ref H7-METHOD1; occurred_at 2026-01-10T08:00:00Z; description “First acquisition process and its exported peak record.” |
| `H7-O2` | event_kind data_collection; event_key RUN-17; performed_by_refs [H7-COL2]; method_ref H7-METHOD2; occurred_at 2026-01-10T08:05:00Z; description “Separate acquisition process, distinct raw capture and operator, for the same chamber run.” |

The shared event_key identifies the **observed event**, not a shared acquisition identity. Amendment of H7-R1-V1 does not replace H7-O1 with a new acquisition event. No additional observation is manufactured from the revised export.

### 24.5 Inspectable supporting material and provenance bindings

For each suffix below there is one Artifact `H7-DOC-<suffix>` of kind document and one EvidenceReference `H7-SUP-<suffix>`. The reference has `reference_kind = supplied_excerpt`, `availability = supplied`, `artifact_ref` equal to its support Artifact, `record_ref = null`, locator `fixture-section-1`, `provided_by_ref = H7-PREP`, `attestor_ref = null`, the following excerpt, and a scope note matching the listed use. These eight Artifacts use declaration provenance and point through `content_evidence_refs` to their excerpt. This is ordinary supplied-document linkage; it is not an assertion using itself as sole support.

| Suffix | Supplied fictional excerpt / exact evidentiary use |
|---|---|
| `CHAIN` | “For C1 acquisition, ER1 comes directly from O1. A, B and C inherit ER1; D inherits B; E inherits A; F comes directly from O2. These are all in-scope immediate and upstream acquisition links of the seven listed contributions and two listed processes. No additional acquisition parents are recorded within this enumerated fixture boundary.” Supports the claim-origin edges and finite history coverage. |
| `ACQ` | “O1 and O2 are distinct capture events using different collection instruments, operators and raw capture logs. Both observe RUN-17. Neither capture consumes the other's export within the examined acquisition process. The first export reports 24; the second reports 21. Upstream acquisition enumeration for these two events is complete within the stated boundary.” Supports origins/boundaries and acquisition coverage. |
| `COMPARE` | “The reviewer compared exactly O1 and O2 in acquisition, examined their raw capture receipts and separate collection procedures, and concluded independent_process for that pair only. Shared event context is acknowledged. Analytical-method, model, rubric and organizational independence were not assessed.” Supports one pairwise assessment, without statistical-independence certification. |
| `MODEL` | “Generator MGEN and judge MJUDGE each derive from MBASE and each name TRAINING. Their supplied subset descriptors are split-A and split-B; exact row overlap is not established. No further model ancestry is represented. REFERENCE, RUBRIC, D and ANSWER have generator MGEN.” Supports the eight model/generation relations. |
| `PIPE` | “The finite population is EA, EB, EC, ED, EE, EF in run answer-run-1. All six have admission and preservation records. Selection occurred for EA-EE and did_not_occur for EF. Use occurred for EA, EB, ED; did_not_occur for EC and EF; use of EE is unknown. All observations use their explicitly named stage key; use records do not establish a causal effect.” Supports §27's exact matrix and cohort assessments. |
| `GRANT` | “Editorial Service grants channel H7-CHANNEL amend authority for exactly R1-V1, A, D and E during 2026-01-10T00:00:00Z through 2026-01-10T23:59:59Z. The complete stated routing view for these four tuples consists of this direct channel and these targets. This is the supplied institutional grant, without external authentication.” Supports route coverage and authority. |
| `CORR` | “The human reviewer compared the first export with the capture material, identified an export discrepancy and proposed an amendment. Submission CASE1 targets R1-V1, A, D and E. Handling accepted the request. The process log links changes R1-V1 to R1-V2, A to A-V2, and D to D-V2 to CASE1. No change record for E is included. No claim about unlisted downstream targets or sustained capacity is supplied.” Supports review, submission, handling and the three linked changes. |
| `CONTEXT` | “EF is an attributed contradiction of C1. It is assessed external to the I1 reuse chain because it comes from O2's separately documented acquisition. A represents internal reuse of O1 within that boundary. The original anomaly text concerns a timestamp alignment issue outside the current peak-value claim; it remains unclassified.” Supports stance/externality/context records. |

A documentary provenance group means attribution to H7-PREP, `basis_kind = documented_record`, the named `H7-SUP-*` reference, method “Manual transcription and scope check of the named supplied fixture excerpt”, and qualifications “Fictional conformance material; no independent authentication by the toolkit.” The comparison and human-review groups instead attribute to H7-REVIEWER; the authority assertion attributes to H7-EDITOR. All groups retain their actual source basis rather than upgrading it through calculation.

Use CHAIN for Claim/EvidenceItem bindings and source Artifacts; ACQ for OriginEvents and their protocol Artifacts; MODEL for model/generation relations and evaluation-role records; PIPE for PipelineRecords and cohort assessments; GRANT for the channel/grant/route coverage; CORR for human review and correction events/revisions; CONTEXT for externality, stances and the anomaly. Administrative support Artifacts, identity inventories and Inquiry construction use declaration provenance. Boundary assessments use ACQ, with CHAIN additionally referenced where full contribution coverage matters. These bindings are exact case premises, not a future runtime rule that prose headings confer authority.

## 25. Hero graph, evaluations and documentary qualification

### 25.1 Acquisition and stance assertions

All seven following positive acquisition links have dimension `acquisition`, polarity `affirmed`, matching C1/I1 scope and documentary CHAIN support. `details.portion_note` says “Entire represented contribution for C1”; originates_from uses `details.dependency_note` with the same scope. No additional acquisition edge is implied by a citation, generator, publisher or correction.

| Assertion ID | Predicate | From | To |
|---|---|---|---|
| `H7-L01` | originates_from | H7-ER1 | H7-O1 |
| `H7-L02` | derived_from | H7-EA | H7-ER1 |
| `H7-L03` | syndicated_from | H7-EB | H7-ER1 |
| `H7-L04` | quotes | H7-EC | H7-ER1 |
| `H7-L05` | summarizes | H7-ED | H7-EB |
| `H7-L06` | copies | H7-EE | H7-EA |
| `H7-L07` | originates_from | H7-EF | H7-O2 |

There are seven acquisition links; the six seed paths pass through the ancestor-only ER1 where appropriate. Stance assertions `H7-ST-A` through `H7-ST-E` use `supports` from EA-EE to C1. `H7-ST-F` uses `contradicts` from EF to C1. All stance dimensions are null and carry CONTEXT support plus the corresponding source contribution's CHAIN/ACQ premise. A quote's stance is explicitly supplied here, never inherited automatically.

### 25.2 Material, publication and version context

Artifact-level relations `H7-MAT-A` through `H7-MAT-E` repeat the explicitly supplied material history: A derived_from R1-V1; B syndicated_from R1-V1; C quotes R1-V1; D summarizes B; E copies A. Their dimension is null. These relations are separately supplied material observations, not auto-generated corroboration of the claim graph. Citation assertions `H7-CITE-D` and `H7-CITE-E` are D cites B and E cites A, respectively. They supply citation paths only.

`H7-PUB-A` through `H7-PUB-E` connect A-E to H7-EDITOR through `published_by`, dimension null and CHAIN declaration support. These publisher declarations do not become acquisition parents.

`H7-REV-R1`, `H7-REV-A` and `H7-REV-D` assert that R1-V2 supersedes R1-V1, A-V2 supersedes A, and D-V2 supersedes D. Each has dimension null, CORR support, reason “Revision linked to CASE1”, and an `effective_at` matching its change event. Old artifact versions remain represented and remain the selected seeds. No Claim is rewritten and no EvidenceItem is rebound automatically.

### 25.3 Model and evaluation records

`H7-ML01`: MGEN model_derived_from MBASE; `H7-ML02`: MJUDGE model_derived_from MBASE; `H7-ML03`: MGEN trained_on TRAINING with subset_descriptor split-A; `H7-ML04`: MJUDGE trained_on TRAINING with subset_descriptor split-B. These use model_ancestry and documentary MODEL support.

`H7-GEN-D`, `H7-GEN-ANSWER`, `H7-GEN-REFERENCE` and `H7-GEN-RUBRIC` connect the named Artifacts to MGEN through generated_by, dimension null. No ownership edges are supplied. These eight assertions have inquiry-only scope as permitted for model/material metadata; they confer no acquisition history on another claim.

| Evaluation | Required data and exact bindings |
|---|---|
| `H7-EVAL` | evaluation_kind judgment; target_refs [H7-ANSWER, H7-C1]; result_refs [H7-EVAL-RESULT]; occurred_at 2026-01-10T11:50:00Z; review_contribution null as a non-human-review activity. Roles: candidate H7-ANSWER; generator H7-MGEN; judge H7-MJUDGE; reference_answer H7-REFERENCE; rubric H7-RUBRIC. Each binding cites H7-SUP-MODEL and retains its supplied-role qualification. |
| `H7-HREVIEW` | evaluation_kind human_review; target_refs [H7-R1-V1]; result_refs [H7-REVIEW-RESULT]; occurred_at 2026-01-10T12:00:00Z. Roles: human_reviewer H7-REVIEWER; method_input H7-CHECK-METHOD. Bindings cite H7-SUP-CORR. review_contribution describes comparing the capture/export records, identifying the discrepancy, and reasoning about the proposed correction. |

The case supplies no independence assessment comparing H7-EVAL with H7-HREVIEW and no full training/rubric history for the human. That gap is deliberate. A documented human contribution survives while corrective-process independence remains unestablished.

For the **generator/judge pair**, the strict shared recorded model ancestors are exactly MBASE and TRAINING. The matching family-label set is exactly {H7-family}. Exact shared role-bound objects and one-sided ancestor relations are empty for this pair. Dataset-row overlap remains unknown. Other role comparisons preserve their own object kinds and material histories; this case does not assign them a new combined score.

## 26. Hero assessment inventory and finite coverage

### 26.1 Coverage records

All coverage assertions use `assessment_kind = coverage`, `state = complete_for_scope` except the explicitly partial model record, `universe_enumerated = true`, and `omitted_refs = []`. Their effective scope/time is §24.2. Any other metadata remains unexamined rather than being covered by implication.

| Coverage ID | Kind / subjects | Member set and exact coverage |
|---|---|---|
| `H7-COV-ACQ` | upstream_history; subject_refs [H7-I1, H7-O1, H7-O2] | member_refs [H7-EA, H7-EB, H7-EC, H7-ED, H7-EE, H7-EF, H7-ER1, H7-O1, H7-O2]; dimensions [acquisition]; relation_types [derived_from, copies, syndicated_from, summarizes, translates, quotes, originates_from, depends_on]. CHAIN and ACQ evidence cover all outgoing in-scope parents of every listed member. |
| `H7-COV-COMP` | upstream_history; subject_refs [H7-O1, H7-O2] | member_refs [H7-O1, H7-O2]; acquisition; depends_on; ACQ/COMPARE evidence for the exact acquisition-process pair, without claiming broader independence. |
| `H7-COV-MODEL` | model_history; subject_refs [H7-MGEN, H7-MJUDGE, H7-MBASE] | member_refs [H7-MGEN, H7-MJUDGE, H7-MBASE, H7-TRAINING]; state partial; universe_enumerated false; dimensions [model_ancestry]; relation_types [model_derived_from, trained_on]; MODEL support. Omitted unmodeled training history is recorded as a Gap, not as one hidden root. |
| `H7-COV-ROUTE` | correction_routes; subject_refs [H7-CHANNEL] | member_refs [H7-CHANNEL, H7-R1-V1, H7-A, H7-D, H7-E]; dimensions []; relation_types [propagates_to]; GRANT support and explicit direct-target field coverage for amend during the grant window. |
| `H7-COV-ADM` | pipeline_universe; subject_refs [H7-PA-A] | Six seed EvidenceItems; dimensions []; relation_types []; exact admission key in §27; PIPE evidence. |
| `H7-COV-PRES` | pipeline_universe; subject_refs [H7-PP-A] | Same six members; exact preservation key; PIPE evidence. |
| `H7-COV-SEL` | pipeline_universe; subject_refs [H7-PS-A] | Same six members; exact selection key; PIPE evidence. |
| `H7-COV-USE` | pipeline_universe; subject_refs [H7-PU-A] | Same six members; exact influence key; PIPE evidence. |

The model row overrides the table defaults as stated. Its unmodeled-history gap says “Further model ancestry and exact training rows were not examined.” No contrary acquisition or identity assertions are supplied in the main case. This states the fixture contents and does not prove that the outside world has no such records.

### 26.2 Other assessments

| ID / kind | Subjects | Required detail values |
|---|---|---|
| `H7-OB1`, `origin_boundary` | [H7-O1] | dimension acquisition; boundary_role documented_origin; coverage_ref H7-COV-ACQ; termination_reason “Origin of the first listed acquisition within the complete stated acquisition view.” ACQ basis. |
| `H7-OB2`, `origin_boundary` | [H7-O2] | As OB1 for the second acquisition. |
| `H7-IND12`, `independence` | [H7-O1, H7-O2] | comparison_form pairwise; dimension acquisition; conclusion independent_process; examined_dependency_refs [H7-OB1, H7-OB2, H7-COV-COMP]; unexamined_dimensions [analytical_method, model_ancestry, evaluation_rubric, organizational_control]; coverage_ref H7-COV-COMP; scope_note restricts the conclusion to the two collection processes. COMPARE basis and identified reviewer. |
| `H7-EXT-F`, `externality` | [H7-EF] | boundary_inquiry_ref H7-I1; conclusion external; grounding_basis “Separately documented O2 acquisition outside the named reuse chain”; relevant_time 2026-01-10T10:00:00Z. CONTEXT plus ACQ support. |
| `H7-INT-A`, `externality` | [H7-EA] | Same inquiry; conclusion internal; grounding_basis “Represented reuse of ER1 inside the named chain”; relevant_time 2026-01-10T10:00:00Z. CONTEXT plus CHAIN support. |
| `H7-AUTH`, `authority` | [H7-CHANNEL] | target_refs [H7-R1-V1, H7-A, H7-D, H7-E]; action_types [amend]; valid_window entire stated day; authorized_by_ref H7-EDITOR; grant_state granted; authority_basis is the supplied GRANT excerpt; coverage_ref H7-COV-ROUTE. |

There is no capacity, verification, conflict or governance-layer classification assessment in the main case. Those omissions must not become successful checks. Documentary boundary/independence qualification uses the exact supplied support and coverage; all authoring limits remain attached.

## 27. Hero pipeline, anomaly and correction records

### 27.1 Four stages, one explicit cohort, distinct observations

Every PipelineRecord has run_key `answer-run-1`, an exact subject from the six seeds, PIPE provenance and one of the keys below. There are twenty-four rows. Row IDs append A, B, C, D, E or F to the corresponding prefix. `observed_at` is the listed instant.

| ID prefix | stage / stage_key | Time | EA | EB | EC | ED | EE | EF |
|---|---|---|---|---|---|---|---|---|
| `H7-PA-` | admission / intake-1 | 2026-01-10T11:10:00Z | occurred | occurred | occurred | occurred | occurred | occurred |
| `H7-PP-` | preservation / store-1 | 2026-01-10T11:20:00Z | occurred | occurred | occurred | occurred | occurred | occurred |
| `H7-PS-` | selection / select-1 | 2026-01-10T11:30:00Z | occurred | occurred | occurred | occurred | occurred | did_not_occur |
| `H7-PU-` | influence / answer-use-1 | 2026-01-10T11:40:00Z | occurred | occurred | did_not_occur | occurred | unknown | did_not_occur |

For admission/preservation occurred rows, `output_refs` contains that same EvidenceItem and detail states that the exact contribution was admitted/preserved. For selection/use occurred rows, `output_refs = [H7-ANSWER]`. Negative/unknown rows use `output_refs = []`. Known rows use `linkage_kind = use_record`; the unknown EE use row uses unspecified and detail “Use of EE was not established in the supplied process log.” All rows retain the exact stage/key, so a missing or unknown use never reverses a known admission.

The two eligible transitions are intake-1 to store-1 and intake-1 to select-1. Both have identical member sets, one admitted baseline and an explicit positive admission record for every member. Influence is outside the restricted transition target kinds in definitions §26.4; its stage fraction/interval and individual use records remain available at their own scope.

### 27.2 Unclassified anomaly

Record `H7-AN1` has kind anomaly, inquiry_refs [H7-I1], claim_ref null, classification_state unclassified, caller_label null, and original_context “A local clock alignment difference may affect event ordering; the present peak-value Claim does not represent this timing distinction.” context_evidence_ref is null because context is supplied; comparison_note says no rarity estimate or cohort classification is supplied. CONTEXT provenance is retained.

AN1 is outside the six-member pipeline cohort and the seed-contribution set. It must remain visible without becoming a seventh source, a new Claim or an invented tail-rate denominator.

### 27.3 Channel and correction case

`H7-CHANNEL` has owner_refs [H7-EDITOR], target_refs [H7-R1-V1, H7-A, H7-D, H7-E], contact_locator null with a withheld Gap explaining that no contact endpoint is needed by this offline fixture, declared_action_types [amend], and the GRANT day-long valid_window. GRANT provenance supplies its declared role. The absent mailbox is not a missing local reference and does not defeat the explicitly supplied structural route; no contact attempt occurs.

| Event ID | event_kind / time | Required details |
|---|---|---|
| `H7-CASE1` | submission / 2026-01-10T12:10:00Z | case_ref null; channel_ref H7-CHANNEL; target_refs [H7-R1-V1, H7-A, H7-D, H7-E]; submission_kind proposed_correction; summary identifies the first export discrepancy and requested amendments. |
| `H7-HAND1` | handling / 2026-01-10T12:20:00Z | case_ref H7-CASE1; same channel and four targets; outcome accepted; reason “The service accepts the documented export-correction request.” |
| `H7-CHANGE-R1` | change / 2026-01-10T13:00:00Z | case_ref H7-CASE1; channel_ref H7-CHANNEL; target_refs [H7-R1-V1]; action_type amend; before_ref H7-R1-V1; after_ref H7-R1-V2; after_absence_reason null; linkage_description identifies CASE1 and the export revision. |
| `H7-CHANGE-A` | change / 2026-01-10T13:10:00Z | Same structure; target/before H7-A; after H7-A-V2; explicit CASE1 process linkage. |
| `H7-CHANGE-D` | change / 2026-01-10T13:20:00Z | Same structure; target/before H7-D; after H7-D-V2; explicit CASE1 process linkage. |

All five events use CORR support. The three after-Artifacts carry CORR-supported descriptions of the corrected 21-degree export or amended summary. No before/after relation for E is supplied. B and C are not in this declared correction-target population; the report must not infer their change status. F is independent contradictory material, not automatically a correction target.

M012 therefore has **one case, one handling event, three linked change events, three distinct documented `(case_ref,before_ref)` targets, and one case with a documented change**. The three include the original export and two downstream Artifacts. The downstream subset {A,D,E} has two documented changes and one undocumented target; this is a named subset disclosure, not a new success-rate field.

## 28. Controlled hero variants and logical fixture freeze

### 28.1 Variant discipline

Each variant is a **separate snapshot and separate future audit**, produced from H7-S1 by the listed conceptual changes. These are authoring instructions for prose fixtures, not an executable patch format. Unchanged record content, exact scope and all local references remain represented in the variant. Snapshot IDs are distinct; predecessor remains null. No runtime comparison, filesystem merge or predecessor traversal is required.

| Case / snapshot | Exact controlled change | Expected origin/contribution difference |
|---|---|---|
| `H7-V01` / `H7-S-FIVE` | Remove F from both seed lists only. Keep its records, assessments, contradiction and the explicitly six-member pipeline cohort in the dossier. | N = 5; nominal seed Artifacts = 5; acquisition paths of all seeds end at O1; HHI = 25/25. F's presence elsewhere does not silently restore it to the seed denominator. Comparison IND12 remains a two-member supplied comparison at its own scope. |
| `H7-V02` / `H7-S-UNKNOWN` | Add Artifact H7-U, EvidenceItem H7-EU bound to C1/U, and UnresolvedReference H7-UX expected_kinds [evidence_item], reason not_recorded, description identifying missing upstream contribution for C1. Add affirmed H7-LU: EU derived_from UX in acquisition. Append U/EU to the seed lists and EU/UX to acquisition coverage members; change COV-ACQ state to partial with explicit gap for the branch. Existing six completed traces retain their local positive scope; coverage support is supplemented with an excerpt explicitly certifying their original subview and leaving EU unresolved. | N = 7; first six origin rows stay single_documented_origin; EU unresolved; one represented unresolved frontier; HHI unavailable. The global partial label cannot erase the positively scoped complete six-row subview. A separate supported coverage assessment H7-COV-ACQ-OLD repeats the original finite nine-member scope and is referenced by OB1/OB2, making that subview qualification explicit. |
| `H7-V03` / `H7-S-MULTI` | Add Artifact H7-G, EvidenceItem H7-EG bound to C1/G, and two affirmed acquisition relations H7-LG1: EG derived_from EA and H7-LG2: EG derived_from EF. Append G/EG to the seed lists and EG to complete acquisition coverage. Add supplied CHAIN supplement explicitly enumerating both parents and excluding other immediate parents for EG. | N = 7; six single-origin rows plus one multiple_documented_origins row; origin incidences O1 = 6 and O2 = 2; incidence total 8/7 is nonexclusive; HHI unavailable due to unallocated multiple origins. |

All added EvidenceItems use locator entry-1 and documentary_statement; their descriptions state the variant contribution. Added Artifacts use the ordinary Artifact convention. Added relations have the default scope/time/provenance, supplemented by the named supplied excerpt and its new supporting Artifact/reference. V02's new supporting Artifact and supplied_excerpt are `H7-DOC-V02` and `H7-SUP-V02`; V03 uses `H7-DOC-V03` and `H7-SUP-V03`. Their fields follow §24.5 and the excerpt is the variant's stated parentage/coverage supplement, explicitly fictional. V02 adds `H7-COV-ACQ-OLD` to `coverage_assertion_refs`; V03 adds no new coverage ID. EU/EG and their Artifacts inherit the variant support provenance, with null factual fields avoided by the ordinary Artifact conventions. All required details of COV-ACQ-OLD match the original COV-ACQ, with its ID changed and its retained six-seed subview explained. Additional coverage assertions are appended to `coverage_assertion_refs`. In V02, COV-ACQ-OLD has the original complete nine-member scope, original relation set and supporting material; it never purports to cover EU. The newly partial COV-ACQ makes the larger missing branch explicit. No contradictory completeness assertion over EU is supplied.

The pipeline cohorts and correction populations stay unchanged across all three variants. They were explicitly enumerated process populations, not aliases for the inquiry's evolving seed list. Recomputing them from N would violate the existing contract. No seventh stage record or correction target is invented.

### 28.2 What is frozen by the WU7 proposal

On adoption, freeze the main case's input meaning, seed/member sets, seven acquisition relations, attributed basis, qualified comparison scope, origin and evaluator witnesses, four stage keys, correction identities, all stated unknowns and the logical expected results in `VALIDATION_PLAN.md`.

Textual presentation may vary only when it preserves the same fields, versions, states, evidence and limits. Renaming IDs requires a complete reviewed identity-preserving transformation; changing a population, edge, assessment basis, source text's evidentiary meaning or unknown status requires a new case revision. A changed expected result cannot be approved solely because a new implementation produces it.

This unit creates no fixture JSON, YAML, CSV, expected-output JSON, schema, test runner or graph implementation. WU8 expands field-level verification obligations. A later authorized scaffold can materialize explicit records and their prose expectations. Analytical golden output remains unimplemented until its own approved phase.
