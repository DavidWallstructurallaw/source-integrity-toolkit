# SUCCESS_CRITERIA

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Target release | v0.1 |
| Phase / work unit | Phase 0 / Work Unit 8: Validation and traceability acceptance |
| Revision | 0.3 |
| Date | 2026-09-17 |
| Status | PROPOSED FOR REVIEW; current checks concern documents and coverage only |
| Theory Owner | Xiangyu Guo |
| Technical Owner | Unassigned |
| Current instruction | Accept the Work Unit 7 handoff and continue |
| New review packages | WU8-C01-WU8-C03; scoped WU7 adoption and its WU6 dependency recorded in validation §9 |
| Current criteria | SIT-SC001-SIT-SC046 preserved; SIT-SC047-SIT-SC066 added |
| Case inventory | One hero, three isolated variants, twenty-eight micro-cases |
| Current companions | Product 0.4; lineage 0.3; validation 0.2; reporting 0.2; definitions 0.2; traceability 0.1 |
| Full Phase 0 approval / runtime tests | Not issued / not executed |

**Revision 0.3 reading rule.** Numbered sections 1-14 retain revision 0.2 verbatim, including the historical WU6/WU7 checks and then-pending states. Sections 15-20 contain the current Work Unit 8 extension. Current acceptance is recorded as a later event; no prior file is rewritten to imply earlier approval. Document coverage checks and future executable acceptance remain separate.

## 1. Purpose and acceptance layers

This document defines observable acceptance conditions for WU6's report contract and places them inside the still-incomplete Phase 0 and v0.1 delivery process. It does not certify that the toolkit exists, that tests have passed in a running product, or that the source theories are empirically validated.

The source basis remains the six supplied papers and the forty-entry [THEORY_SOURCE_MAP.md](THEORY_SOURCE_MAP.md). Requirements about preserved provenance, appropriate validation, independent correction, separate replenishment stages and profile reporting derive from that map. The exact acceptance IDs, output states and reference structures are toolkit operationalizations, specified in [OBSERVABILITY_AND_REPORTING.md](OBSERVABILITY_AND_REPORTING.md) §§11-23 and the bridge in [CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md](CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md) §§18-22.

Four decisions remain separate:

| Acceptance layer | What can establish it | Current state |
|---|---|---|
| Local document checks | File, reference, preservation and packaging checks performed on this delivery | Recorded in §8 |
| Owner adoption of WU6 | Acceptance of the submitted WU6 documents and WU6-C01-WU6-C03 | Pending this delivery's review |
| Final Phase 0 baseline approval | All planned specifications, no unaddressed in-scope blockers, final audit and actual owner approval | Not reached |
| Implemented v0.1 acceptance | Separately authorized implementation plus executable tests and release evidence | Not performed |

A completed specification check is not evidence that a future runtime feature works. A runtime's completed processing state will likewise not establish substantive source truth. These two distinctions apply to this project and to its eventual reports.

## 2. Accepted baseline and WU6 boundary

The user's “可以，继续” after the WU5 handoff is recorded as contextual acceptance of Option B for SIT-D026 and SIT-D027 in reporting §11.1. It does not approve this new report realization in advance. Register revision 0.5 remains unchanged under the WU6 three-file allowlist. Its historical pending entries must be synchronized at the next authorized update using the scoped acceptance record, without changing original recommendations.

The following baseline meanings must remain unchanged: claim-specific evidence; twelve core record kinds; twenty-four relation predicates; nine assessment kinds; five separate dependency dimensions; explicit unresolved endpoints; provenance and documentary qualification; source-identity distinctions; fifteen analytical families; exact seed/cohort denominators; restricted HHI; separate route, authority, handling and change; fourteen threat families; seven auditor-control risks; no active content detector; and no automatic intervention.

WU6 adds a state/check/reason vocabulary, complete capability matrix, non-cumulative Level 0-4 navigation, a logical report envelope, native-state mapping, bounded findings, safe presentation requirements and written conformance cases. It creates no new input key, metric, resolver, schema file, implementation, fixture, dependency or workflow.

## 3. Stable WU6 acceptance criteria

`SIT-SC001` through `SIT-SC032` are success-criterion IDs introduced in this file. They do not replace product IDs, M-family IDs, central decisions or later implementation Trace IDs. The contract locations below define how to judge each criterion; the W6 witnesses supply written examples. Runtime validation remains future work.

| ID | Acceptance condition | Required documentary or future runtime evidence |
|---|---|---|
| SIT-SC001 | Every result identifies its exact inquiry, Claim version where applicable, target, dimension/view and temporal basis | Scope object plus input references; no implicit all-claim scope. Reporting §§16.2, 18; W6-01, W6-26 |
| SIT-SC002 | Structural rejection produces diagnostics without analytical inventories, levels or findings | Allowed envelope pairing and empty analytical arrays. Reporting §12.2; W6-02-W6-03 |
| SIT-SC003 | Valid sparse and protected inputs remain admissible | Explicit unresolved records and their limitations; no invented origin. Lineage §§14, 19.2; W6-01-W6-02, W6-24 |
| SIT-SC004 | Per-result execution and availability use only the prescribed combinations | Completed/available versus interrupted/not_evaluated, with non-result values null. Reporting §12.3; W6-27, W6-32 |
| SIT-SC005 | Original assertion basis and report derivation remain distinguishable | Basis index retains declarations, upstream inferences and protected attestations. Reporting §§12.5, 16.6; W6-10, W6-25 |
| SIT-SC006 | Checks and reasons are scoped and complete for their dependent result | PC01-PC24 and the reason registry are referenced with input evidence and field scope. Reporting §13; W6-05, W6-08, W6-23 |
| SIT-SC007 | Every audit exposes all fifteen capability families, including unavailable and unexamined parts | Matrix entries and atomic state-reference partitions agree. Reporting §§14, 16.7; W6-31-W6-32 |
| SIT-SC008 | Level 0-4 labels remain non-cumulative evidence navigation | No maximum/overall quality level; lower ancestry gaps coexist with observed change. Reporting §15; W6-13, W6-18 |
| SIT-SC009 | Counts use the approved record, contribution, origin, case or member unit | Exact selected IDs and populations accompany count values. Definitions §§20-21, 27; W6-01, W6-04, W6-16 |
| SIT-SC010 | Qualified independence counts apply to each exact supplied comparison and required dimension | No pairwise union, unqualified singleton or global independent-source total. Definitions §21.3; W6-09-W6-10 |
| SIT-SC011 | All origin branches and the five seed dispositions remain visible | Known incidence plus baseline/declared/unresolved/multi-origin states retained in N. Definitions §22; W6-05-W6-08 |
| SIT-SC012 | Restricted HHI is available only for the complete single-origin eligible seed population | N, every n_r, exact sum-of-squares numerator and N² denominator; no known-only fallback. Definitions §23; W6-04-W6-06 |
| SIT-SC013 | Immediate inheritance and distant origin resolution use different prerequisites | A direct copy relation may qualify while distant ancestry remains unknown. Definitions §24; W6-07 |
| SIT-SC014 | Frontier counts describe represented gaps, never concealed origin totals | One shared unresolved reference counted once, all affected seeds disclosed. Definitions §22.4; W6-02, W6-24 |
| SIT-SC015 | Evaluator identity, strict common ancestors, one-sided ancestry and family strings remain separate | Actual role-pair witnesses and unexamined dimensions; no error-correlation score. Definitions §25.1; W6-11-W6-12 |
| SIT-SC016 | Externality requires the actual boundary, time and grounding assessment | Stage logs, human labels and remote URLs cannot supply it. Definitions §25.2; W6-18 |
| SIT-SC017 | Pipeline stage records remain keyed and do not imply missing stages | Admission/preservation/selection/influence are separately evidenced. Definitions §26; W6-18-W6-20 |
| SIT-SC018 | Finite-cohort ratios retain Y/F/U and the full eligible denominator | Unknown point classification with optional [Y/T,(Y+U)/T] interval; no Y/(Y+F). Definitions §26.3; W6-19-W6-20 |
| SIT-SC019 | Retention transitions require one compatible evidenced baseline/target pairing | Same member IDs, run and admitted population; ambiguous baselines withhold transition only. Definitions §26.4; W6-21-W6-23 |
| SIT-SC020 | Correction routes and grant applicability are independently reported | Target/action/time matching on required legs; no mailbox-to-authority shortcut. Definitions §27.1; W6-14-W6-15 |
| SIT-SC021 | Submissions, nonexclusive handling outcomes and linked changes use separate records and counts | Qualified before/after or explicit-removal linkage; missing change stays undocumented. Definitions §27.2; W6-13, W6-16-W6-17 |
| SIT-SC022 | Substantive human contribution and corrective-process independence remain inspectable | Actual review contribution, protected basis and unresolved dependencies; execution remains a distinct constraint. Definitions §25.3; W3-08, W3-16 and W6-24 |
| SIT-SC023 | Anomalies and disagreements retain their context without invented suppression | Claim-unassigned anomaly remains valid; stage exclusion needs its actual baseline. Definitions §26.5; W3-14, W6-21 |
| SIT-SC024 | Native input states never become toolkit assurance or run status | Input handling failed can be disclosed in a completed audit; identity verification remains attributed. Lineage §19.1; W6-17, W6-25 |
| SIT-SC025 | Scoped negatives retain their actual evidence form | Explicit non-occurrence, no witness in partial history and bounded absence are separate. Reporting §14.3; W6-11, W6-16, W6-27 |
| SIT-SC026 | Threat associations retain narrow observations and do not inflate incidents | Finite witness plus basis/limits; no taxonomy verdict, severity total or automatic actor label. Reporting §18; W5-01-W5-14, W6-29 |
| SIT-SC027 | Available exact counts, unavailable values and empty populations remain distinguishable | Zero only for a defined completed inventory; null with reason for a ratio with zero/unknown denominator. Reporting §§12.3, 16.5; W6-01, W6-22 |
| SIT-SC028 | Numerical values retain exact rational structure and labeled completion intervals | Original denominator, six-place optional decimal, no rounded status; interval is not statistical confidence. Reporting §16.5; W6-04, W6-19 |
| SIT-SC029 | JSON and Markdown preserve the same substantive result and limitations | Main-table qualifiers, unavailable capabilities and detail links remain visible. Reporting §19.1; W6-31 |
| SIT-SC030 | Reordering source arrays does not change substantive outcomes | Deterministic memberships/reasons/witness meaning, with volatile metadata separated. Reporting §19.2; W6-30 |
| SIT-SC031 | Input text and report rendering cannot create execution, retrieval or source intervention | Safe presentation, inert locators, no detector/clean-source claim; concrete security checks before release. Reporting §19.3; W6-28-W6-29 |
| SIT-SC032 | Processing interruption, execution failure and protected disclosure never produce unjustified complete results | Finished independent values only, incomplete enumeration not zero, protection limits visible. Reporting §§12.2-12.4, 19.3; W6-24, W6-27 |

### 3.1 Evidence expected from a future implementation

Each criterion must eventually link to positive, negative, missing-data and boundary tests for the relevant public fields. WU8 assigns executable-test ownership and trace IDs; no test filename is invented in this unit. Tests must use controlled fixtures with expected scopes, member sets, states, reasons, basis and exact values, rather than merely checking that a report file was written.

Every public state pairing and used reason/check code needs a test of its semantics. Not every source gap needs a separate user decision. The contract must already determine whether it limits a local result, prevents a ratio, blocks a qualified count, remains a disclosed input observation or causes structural rejection.

A software test showing that the tool faithfully reports a supplied independence assessment does not establish that the assessment is correct in the world. The test must preserve that disclaimer in both formats. A runtime rejection test does not prove the absence of all injection or fabrication risk.

## 4. Coverage of all fifteen analytical families

| Family | Primary success criteria | Critical prohibited shortcut |
|---|---|---|
| SIT-M001 | SIT-SC001-SIT-SC003, SIT-SC009, SIT-SC027 | Artifact count equals independent observations |
| SIT-M002 | SIT-SC005-SIT-SC006, SIT-SC009, SIT-SC011 | Parentless node equals documentary root |
| SIT-M003 | SIT-SC005-SIT-SC006, SIT-SC010 | Qualified pair counts union into joint independence |
| SIT-M004 | SIT-SC006, SIT-SC011, SIT-SC014 | Unknown or multi-parent seeds disappear from N |
| SIT-M005 | SIT-SC011-SIT-SC012, SIT-SC028 | HHI over only the favorable resolved subset |
| SIT-M006 | SIT-SC009, SIT-SC013, SIT-SC027-SIT-SC028 | First-step direct link means new independent information |
| SIT-M007 | SIT-SC003, SIT-SC014, SIT-SC025 | Number of frontier placeholders equals hidden roots |
| SIT-M008 | SIT-SC005, SIT-SC015, SIT-SC025 | Zero recorded overlap proves independence |
| SIT-M009 | SIT-SC008, SIT-SC016-SIT-SC017 | Recent external-looking URL means effective Presence |
| SIT-M010 | SIT-SC017-SIT-SC019, SIT-SC027-SIT-SC028 | Exclude unknown cohort members or multiply stage rates |
| SIT-M011 | SIT-SC020, SIT-SC025, SIT-SC032 | Declared channel means effective correction |
| SIT-M012 | SIT-SC021, SIT-SC024, SIT-SC032 | Accepted request means success; missing revision means failure |
| SIT-M013 | SIT-SC010, SIT-SC015, SIT-SC022 | Human/model-role label supplies independent human judgment |
| SIT-M014 | SIT-SC017-SIT-SC019, SIT-SC023 | Final-only dossier proves suppression |
| SIT-M015 | SIT-SC005-SIT-SC006, SIT-SC024, SIT-SC029 | Documentary metadata or coverage label proves truth |

SIT-SC004, SIT-SC007, SIT-SC026 and SIT-SC029-SIT-SC032 apply across the included families. They cannot be satisfied only on a favorable hero input while failing for sparse, disputed, protected or interrupted cases.

## 5. WU6 completion and stop rules

### 5.1 Documentation unit acceptance

The WU6 document package is ready for review when it contains only the three permitted Markdown files; retains the inherited numbered bodies; specifies all fifteen capabilities; assigns output states/reasons/checks; preserves native input states and analytical meanings; explains the five non-cumulative observability labels; supplies coherent logical envelope and reference rules; and maps written cases to explicit success criteria.

The local document checks in §8 verify structure and preservation. They do not replace owner adoption of WU6-C01-WU6-C03. A hard contradiction in an approved definition must stop the affected contract rather than being fixed silently by output naming.

### 5.2 Material stop conditions

Stop the affected specification or future implementation when a report field changes its denominator, invents an independent root, merges unknown and multi-parent contributions, treats a supplied verification as truth, uses a summary level to authorize unsupported fields, turns a missing revision into failure, assigns ideological/source rankings, or requires a new input capability to work without a scoped amendment.

Also stop when the report contract cannot identify the premise for a stronger result, a negative search did not process the necessary finite view, a state/code has competing meanings, JSON and Markdown diverge materially, or protected output cannot preserve its assurance limits. Runtime interruption may instead return the explicit incomplete envelope when the integrity of already finished values is established.

An out-of-allowlist earlier document or central register is not automatically editable because a cleanup would be convenient. Record the issue in an allowed document, preserve evidence and request the relevant authorization or return to an authorized unit.

## 6. Remaining Phase 0 and release gates

| Gate | Required evidence before it can pass | State at this handoff |
|---|---|---|
| WU1 source audit and map | Exact source identities, source claims versus operationalizations, mapped limits | Existing inputs preserved; no new scientific verification asserted |
| WU2 product boundary | Explicit local dossier workflow, supported/excluded capabilities and separate project authority | Accepted design directions retained |
| WU3 ontology and graph | Canonical records, relations, assertions, unknowns, versions and evidence rules | Accepted numbered body preserved; WU6 bridge submitted |
| WU4 analytical meanings | Exact units, denominators, allocation limits and M001-M015 | Accepted contract retained without new metric |
| WU5 threat model | Fourteen narrow threat surfaces, seven auditor risks, no active detector/intervention | Accepted contextually; central register sync pending an authorized update |
| WU6 reporting | Owner accepts the three submitted review packages and documents | Submitted in this delivery |
| WU7 hero/micro-cases | One canonical hero plus required micro-cases with exact structural expectations | Not performed here; W6 prose cases do not substitute for the hero |
| WU8 validation/traceability | Full field-level tests and future module/Trace ownership | Not performed here |
| WU9 privacy/security/licensing | Concrete resource limits, file/report safety, protected disclosure, permissions and license choices | Open; report requirements are obligations only |
| WU10 architecture/dependencies/handoff | Actual future ownership, interface shape, stable serialization decisions and dependency rationale | Open; no package or runtime dependency selected here |
| WU11 final audit/approval | Consistent complete bundle, no in-scope blocking decision, actual owner approval and final hashes | Not reached; no approval file created |
| Phase 1 scaffold | Separate approval and approved scaffold-only scope | Not authorized by this unit |
| Analytical implementation and release | Separate phase plans plus executable conformance, safety and distribution evidence | Not started |

The report's logical schema and labels can be reviewed now while resource limits and exact serialization mechanics remain explicit later gates. Those bounded tasks cannot be defaulted during implementation. An unresolved necessary release choice must be closed, explicitly removed from scope or kept blocking before final approval.

## 7. Reviewed inputs and byte identities

The following files formed the exact read-only WU6 baseline. Full relative paths identify which revision was read. Original status headers remain historical. SHA-256 fingerprints identify file bytes only; they do not authenticate sources or scientific content.

| Reviewed read-only input | SHA-256 |
|---|---|
| `PHASE_0_PLAN_Source_Integrity_Toolkit.md` | `2d97a820ae218c33cfd00dd96a762853e887f867973a2b2da0945fc4414495b1` |
| `source-integrity-toolkit-phase0-work-unit1/SPEC_AUDIT.md` | `3565ab8f1b08f30e06f4983ffd26adbe8bc977b655ebf410b634918a7ae7949a` |
| `source-integrity-toolkit-phase0-work-unit1/THEORY_SOURCE_MAP.md` | `015e65baf3fcad8ce78a2285df8f2de8d5b7b4cbdd347707ba3cc5d5ba46b627` |
| `source-integrity-toolkit-phase0-work-unit2/PROJECT_INSTRUCTIONS.md` | `cb5cf8f4d367bceacc313189469b3327370bed0450468d62a968825fee4a7746` |
| `source-integrity-toolkit-phase0-work-unit4/DEFINITIONS_AND_UNITS.md` | `913697e733d4430a64696b36a7893fe2113da7e2cfbcadbb54247a36c1792e9d` |
| `source-integrity-toolkit-phase0-work-unit4/OBSERVABILITY_AND_REPORTING.md` | `224a2db1080b69c6d359da327585abd8b035915411cd34782b7c2de90c2c29ad` |
| `source-integrity-toolkit-phase0-work-unit3/CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` | `8d697b6eb556bbe8476f59e48664996fe12003a42efdce179648d25d9ffb924f` |
| `source-integrity-toolkit-phase0-work-unit5/V0.1_PRODUCT_SPEC.md` | `33e61809a50d74acde409e48509a3c0028315add2aace0b57d506e03753a7188` |
| `source-integrity-toolkit-phase0-work-unit5/SOURCE_INTEGRITY_THREAT_MODEL.md` | `d62d1fab2ea6891404193eda3bab4dc23c77c05bd608a6e55e2f6cb97f2a7e82` |
| `source-integrity-toolkit-phase0-work-unit5/UNRESOLVED_DECISIONS.md` | `06aefb57436c2f8e79238f87078b98e00e13a7feb1204fa6f1b1f6cab83656f9` |
| `Entropy as a Structural Boundary Condition, Not a Causal Force v2(2).pdf` | `7e5dbfb7cc270c68d0533b3ba74fbee1e96374004761cb46ffe6a4e56ef5bab4` |
| `The Universal Inbreeding Law v2(2).pdf` | `b788c18b7a66886b623ea7c35b777643146b38e78b540acedde87cc5e019f2ee` |
| `The Boundary Vacuum Law_ Gradient, Boundary Failure, Topological Flow, and Pressure Capture in Social Systems v2(1).pdf` | `1323813d59152bc2d87ebab90dadce6d7a9232e14b67bb2b50a45e43b5e1e530` |
| `The Heat Death of Language v2.pdf` | `75af9e29467c5a4fae412e910fbac8b6945fa606d2567b1ac6fda98d41c691fb` |
| `Evaluation Closure Benchmark Inbreeding and the Design of Open AI Evaluation.pdf` | `002d2393d05cb2c8b1db0a70e844e3d775e2be2155db7b2ffaadaa8080c8b950` |
| `The Source Integrity Layer_ Presence × Integrity and the Governance of AI-Native Information Distribution.pdf` | `bc233063e153fdcee83ad6e6088764f20dd24e3f4c7ae094b88f35905b52c3b3` |

The six theory PDF identities are compared with the WU1 source audit. This unit uses their supplied conceptual content and existing page locators; it performs no web research or current empirical/source authentication. The SIL p. 13 governance table is already supplied with the source and its separate layers remain reflected in the contract.

## 8. Local checks and archive integrity

### 8.1 Check boundary

The drafting assistant performs the authoring checks. There is no independent second reviewer. Internal utilities may read Markdown, compare text, inspect identifiers, check arithmetic, hash files and create the archive. They are excluded from the delivery and are not a toolkit implementation.

The local authoring checks passed for:

| Check | Verified result |
|---|---|
| Allowed outputs | Exactly the three WU6 Markdown files; no earlier register/product/definition file modified |
| Read-only baseline | All twenty-eight pre-delivery Markdown, ZIP and PDF files retain their original SHA-256 values |
| Reviewed input manifest | The sixteen inputs in §7 match the pre-delivery identities |
| Theory identity | All six PDF hashes agree with the WU1 source register |
| Inherited text preservation | WU4 reporting §§1-10 and WU3 lineage §§1-17 retained verbatim |
| Contract continuity | Existing 15 M-families, 12 record kinds, 24 predicates and 9 assessment kinds preserved |
| New coverage | 24 scoped prerequisite checks, 32 W6 written cases and 32 success criteria present with unique IDs |
| Reference consistency | Referenced theory/product/decision/metric/threat/control/success IDs and written-case ranges resolve to the existing or current catalogs |
| Markdown structure | Numbered sections are contiguous; tables parse with matching column widths; fences are balanced; text is UTF-8 without replacement characters |
| Working-folder links | Relative document links resolve against the intended assembled specification set; earlier files are intentionally absent from this increment |
| Written arithmetic | 26/36 = 13/18; six-place half-up display is 0.722222; the five-member completion interval retains [3/5, 4/5] |
| Archive check | ZIP contains exactly the three permitted Markdown basenames and its member bytes match the delivered files |

These checks inspect documentation and authoring arithmetic. They do not execute the proposed graph, state machine, renderer or source-audit product. The archive is constructed and checked against the final file bytes before handoff.

No production graph/lineage algorithm, live verifier, runtime test suite, CI run, source detector, external API, dependency installation, GitHub modification or scientific experiment was performed. Safe rendering, time-specific applicability and runtime budget requirements are specified for later tests; this delivery does not claim they were executed by a working product.

## 9. Incremental assembly and next unit

The archive contains exactly:

| File | Revision | Use |
|---|---|---|
| `OBSERVABILITY_AND_REPORTING.md` | 0.2 | Current reporting extension plus preserved WU4 body |
| `CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` | 0.2 | Current input/output bridge plus preserved WU3 body |
| `SUCCESS_CRITERIA.md` | 0.1 | New acceptance catalog, gates and authoring check record |

Use these three working copies with the latest unchanged definitions 0.2, product 0.3, threat model 0.1, instructions 0.1, audit/map and decision register 0.5. The WU5 acceptance supplement is reporting §11.1. Do not overwrite the earlier delivery directories or ZIPs. Relative links are intended for the assembled specification folder, not a standalone replacement of the whole project.

After acceptance of WU6-C01-WU6-C03, the next planned unit is **Work Unit 7: canonical hero and adversarial micro-cases**, within its own four-file allowlist. It will use the established objects, metrics, reason/state meanings and evidence limits to define exact expected outputs. This unit stops here. It creates no `PHASE_0_APPROVAL.md` and authorizes no implementation.


## 10. Work Unit 7 acceptance scope and reading rule

The current instruction, “继续Work Unit 7”, authorizes this four-file documentation package. The submitted WU6 report realization is used as the proposed case reference; final WU7 adoption must include that reference or identify an amendment. This continuation is not entered as an invented retrospective signature or a full Phase 0 approval. The WU5 acceptance supplement remains reporting §11.1; the central register stays revision 0.5.

Numbered sections 1-9 above preserve the WU6 success document verbatim, including its historical review status and checks. Sections 10-14 are the current WU7 extension. The existing SIT-SC001-SIT-SC032 obligations remain controlling for case interpretation. New SIT-SC033-SIT-SC046 below concern case/oracle completeness and future reproduction, without claiming that a toolkit implementation has run.

The delivery contains one main hero, three distinct-snapshot variants and twenty-eight micro-cases. Prose fixture inputs are in lineage §§24-28. Their logical output oracle is in validation §§2-6. Product §§17-19 connect those examples to the existing sixteen product requirements. None of these files introduces a new analysis family or executable schema.

## 11. Stable Work Unit 7 acceptance criteria

| Criterion | Required observable result | Exact WU7 witness / limit |
|---|---|---|
| SIT-SC033 | Hero input can be expanded into the existing logical fields without inventing a predicate, type, identity or source role | Lineage §§24-27: exact envelope, IDs, defaults, bindings and supplied evidence; `sit-bundle/0.1` unchanged |
| SIT-SC034 | Every seed/ancestor/support/revision population retains its own counted unit | Main six seed Artifacts and contributions, ancestor-only ER1, separate process cohorts and correction targets; validation §2.1 |
| SIT-SC035 | Main origin, first-step and HHI values follow the fixed full seed population | Five O1 incidences, one O2; N = 6; HHI 26/36; inherited 5/6; validation §§2.2-2.3 |
| SIT-SC036 | Qualified comparison output is tied to one supported process assessment | Main IND12 pair size 2; W7-01, W7-06 and W7-12 distinguish origin, procedure and joint-set scopes |
| SIT-SC037 | Evaluator witnesses retain exact-role, strict-ancestor and family-label distinctions | Main generator/judge ancestors {MBASE,TRAINING}, family label {H7-family}, partial row/history limits; W7-05 |
| SIT-SC038 | Separate stage evidence and full finite-cohort denominators survive | Main six-member stage matrix, influence [3/6,4/6], two eligible admission transitions; W7-19-W7-20 |
| SIT-SC039 | Root correction, downstream amendment and undocumented targets remain distinguishable | Main counts 1/1/3/3/1; root plus two downstream changes; E undocumented; B/C not in the case targets |
| SIT-SC040 | Human contribution and contested/unclassified input survive without manufactured qualification | Main HREVIEW, EF contradiction and AN1; W7-06-W7-07, W7-20 |
| SIT-SC041 | The three controlled variants change only their stated inputs and preserve unaffected cohorts/cases | H7-V01 seed-only selection; H7-V02 unknown seventh contribution; H7-V03 known multi-parent contribution |
| SIT-SC042 | All ten plan-required micro-case topics have explicit positive/missing/boundary meanings at case level | Validation §4 mapping and W7-01-W7-10; no claim that WU8's complete field matrix is done |
| SIT-SC043 | Materially different structures remain distinguishable without truth/intent overclaim | W7-03-W7-04, W7-09, W7-13-W7-15, W7-21-W7-25 and validation §6.3 |
| SIT-SC044 | Documentation-only adversarial cases preserve rejection, interruption, inert data and parity rules | W7-24-W7-28 are future test obligations; no security or runtime test passage claimed here |
| SIT-SC045 | Exact rational oracle is independent of future implementation output | Original N/T, bucket/member sets and integer numerators; validation §6.2 and §7 |
| SIT-SC046 | Handoff preserves source bytes, permitted files, review state and next-unit boundaries | Input manifest below; four Markdown outputs only; no central register, reporting or definition edit; stop at WU7 |

### 11.1 Adoption and later execution are different checks

The local authoring checks below establish document and arithmetic consistency within their stated scope. Owner adoption establishes the case baseline. Later runtime verification requires actual accepted inputs, executed code, recorded output and comparison against that adopted oracle.

The same drafting assistant authors and checks this package. No independent second reviewer, real acquisition study, source authentication, scientific replication, live correction or external security audit is claimed.

### 11.2 Material stop conditions

Hold the affected case if an exact public result needs a new record kind, unregistered core field/reason, extra semantic inference, unsupported statistical assumption or out-of-scope source lookup. A mismatch with the fixed oracle requires locating the input premise and governing definition before any expected value is changed.

Also hold a case if it hides an unknown branch, substitutes the seed set for an independently enumerated stage cohort, merges origin identities automatically, overstates the reach of an authority grant, reads predecessor data without explicit input, or turns a missing change event into a failure outcome. These are implementation restrictions as well as documentary checks.

## 12. Work Unit 7 input identity manifest

The following read-only input snapshots were used for WU7. SHA-256 values identify bytes, not truth or authorship. Theory content remains governed by the existing WU1 audit/map and supplied source versions; the six PDF identities are retained separately in the preservation check. No outside empirical case, vendor status or standard version is updated.

| Input snapshot | SHA-256 |
|---|---|
| `PHASE_0_PLAN_Source_Integrity_Toolkit.md` | `2d97a820ae218c33cfd00dd96a762853e887f867973a2b2da0945fc4414495b1` |
| `source-integrity-toolkit-phase0-work-unit1/SPEC_AUDIT.md` | `3565ab8f1b08f30e06f4983ffd26adbe8bc977b655ebf410b634918a7ae7949a` |
| `source-integrity-toolkit-phase0-work-unit1/THEORY_SOURCE_MAP.md` | `015e65baf3fcad8ce78a2285df8f2de8d5b7b4cbdd347707ba3cc5d5ba46b627` |
| `source-integrity-toolkit-phase0-work-unit2/PROJECT_INSTRUCTIONS.md` | `cb5cf8f4d367bceacc313189469b3327370bed0450468d62a968825fee4a7746` |
| `source-integrity-toolkit-phase0-work-unit4/DEFINITIONS_AND_UNITS.md` | `913697e733d4430a64696b36a7893fe2113da7e2cfbcadbb54247a36c1792e9d` |
| `source-integrity-toolkit-phase0-work-unit5/V0.1_PRODUCT_SPEC.md` | `33e61809a50d74acde409e48509a3c0028315add2aace0b57d506e03753a7188` |
| `source-integrity-toolkit-phase0-work-unit5/SOURCE_INTEGRITY_THREAT_MODEL.md` | `d62d1fab2ea6891404193eda3bab4dc23c77c05bd608a6e55e2f6cb97f2a7e82` |
| `source-integrity-toolkit-phase0-work-unit5/UNRESOLVED_DECISIONS.md` | `06aefb57436c2f8e79238f87078b98e00e13a7feb1204fa6f1b1f6cab83656f9` |
| `source-integrity-toolkit-phase0-work-unit6/CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` | `2e267bf916295b3a2d00876e9a69e40e3b47c67abb1ad39b99a29a6b6e36b722` |
| `source-integrity-toolkit-phase0-work-unit6/OBSERVABILITY_AND_REPORTING.md` | `44daa3c86fc7d12e7be16a3aedfe10d16b99f55aa69141f90319ce2b5e63ff6a` |
| `source-integrity-toolkit-phase0-work-unit6/SUCCESS_CRITERIA.md` | `5414d3541c2cde9c37688dd3545baf1060d1dace48627a4e61ccfacd8fbe1646` |

The complete pre-delivery preservation set consists of thirty-two existing Markdown, ZIP and PDF files at the project paths. Ancillary rendered images and temporary authoring utilities are outside that counted set. Historical deliverables stay in their original directories and archives.

## 13. Local authoring checks and artifact integrity

Only non-product authoring checks are performed: text comparison, identifier/reference inspection, Markdown table/fence review, simple finite-set counts and exact rational arithmetic, byte hashes and archive inspection. There is no implementation of source traversal, classifier, correction routing, input parser, renderer or runtime test framework.

| Check | Evidence / checked scope |
|---|---|
| Allowed output names | Product, validation, success and lineage Markdown only; four archive members |
| Original preservation | All thirty-two pre-delivery Markdown/ZIP/PDF hashes compared after authoring |
| Body preservation | Product §§1-16, lineage §§1-22 and success §§1-9 compared verbatim with their immediate predecessor files |
| Input identities | Eleven reference-document SHA-256 values match §12; six theory PDFs retain the WU1 recorded identities |
| Case inventory | H7-01, three separately labeled variants and W7-01-W7-28 each have a defined purpose/input/expected-result boundary |
| Requirement coverage | Ten plan micro-cases and all fifteen analytical families have explicit case references |
| New criterion IDs | SIT-SC033-SIT-SC046 extend rather than replace SIT-SC001-SIT-SC032 |
| Contract continuity | No new input kind, predicate, assessment, M-family, result state, reason code or metric formula selected |
| Table and text structure | UTF-8 text, balanced fences, contiguous numbered sections and consistent table column counts |
| Logical record accounting | Main-case inventory and fixed seven acquisition links checked against the prose tables; source seed population remains six |
| Arithmetic | Partitions, 26/36 HHI, case 1/1/3/3/1 counts, finite-cohort intervals and variant incidence calculations hand-checked with simple authoring arithmetic |
| Archive agreement | ZIP membership and each member's bytes compared with final delivered Markdown |

These checks do not certify all future parser/schema branches or every future public output leaf. WU8 supplies the field-level testing plan; WU9/WU10 supply concrete controls, interfaces and serialization choices. The written limit/interruption examples have not been executed by an implemented auditor.

No source theories, previous deliveries or GitHub repository were modified. No dependency installation, live source collection, runtime fixture, executable golden output, test implementation, CI run or release approval is included.

## 14. Incremental assembly and next unit

| File | Revision | Current use |
|---|---|---|
| `V0.1_PRODUCT_SPEC.md` | 0.4 | Prior product body plus canonical demonstration and product crosswalk |
| `VALIDATION_PLAN.md` | 0.1 | New prose hero/variant/micro-case input and logical-result oracle; WU8 expansion pending |
| `CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` | 0.3 | Preserved input/report bridge plus precise hero record/assessment/stage/correction specification |
| `SUCCESS_CRITERIA.md` | 0.2 | Preserved WU6 criteria and checks plus WU7 criteria, manifest and handoff |

Use these four current working copies with reporting 0.2, definitions 0.2, threat 0.1, instructions 0.1, the WU1 audit/map and decision register 0.5. The increment is not a full replacement repository. Preserve earlier ZIPs and original working directories as history. Relative links resolve in the assembled specification folder.

Current review packages are WU7-C01 and WU7-C02 in validation §8, including their explicit WU6 reporting dependency. Full Phase 0 approval remains WU11 work. After the case baseline is accepted, the next unit is **Work Unit 8**, restricted to validation, success and theory-to-code traceability documents. This delivery stops here.

## 15. Work Unit 8 acceptance scope

The user's “可以，继续” after the WU7 handoff accepts its enumerated WU7-C01/WU7-C02 case package, with the named WU6 reporting dependency, for continuing the controlled specification workflow. The scoped record is in validation §9. It does not approve the new WU8 realization, complete the Phase 0 baseline or authorize code.

WU8 completes the current **written** field-level testing/Trace assignment. The prior H7-01, H7-V01-H7-V03 and W7-01-W7-28 definitions remain unchanged. This unit's prospective execution obligations must later be materialized under approved implementation plans and checked against the fixed oracle.

### 15.1 Three different coverage statements

The reporting catalog currently has 57 registered analytical field keys. Every key is matched by exactly one SIT-VF entry and one primary Trace. Every entry has four logical test obligations. These are document facts that can be inspected now.

A later test suite must actually implement those obligations, along with the input/enum/envelope sweeps, and record its executions. The current field/ID count cannot substitute for those executions.

Concrete WU9 safety/resource/license and WU10 interface/serialization decisions remain open. Their tests have explicit requirements and gates; no false default or test-pass status closes them. Final Phase 0 readiness requires completing those assigned specifications.

## 16. Stable Work Unit 8 acceptance criteria

The new IDs extend the previous 46 criteria without changing their meanings.
| ID | Acceptance condition | Required evidence / scope |
|---|---|---|
| SIT-SC047 | WU7 adoption and named reporting dependency are recorded without backdating or granting implementation authority | Validation §9; existing central register remains unchanged; WU8-C01-WU8-C03 remain submitted. |
| SIT-SC048 | The field registry matches all 57 reporting §17 keys across exactly 15 analytical families | Validation §12 and traceability §5; set equality and one primary owner per leaf. |
| SIT-SC049 | Every registered leaf has a positive, negative, missing-data and boundary obligation | SIT-VF001-SIT-VF057 with P/N/M/B suffixes: 228 distinct logical obligations; no executed-test claim. |
| SIT-SC050 | Every current input field receives a parameterized structural and missingness test obligation | SIT-VG001-SIT-VG007; lineage §§2-9 inventory; all 12 record kinds, 5 reference kinds and shared structures. |
| SIT-SC051 | All typed relation and assessment alternatives retain their exact semantics | 24 predicates, 9 assessment kinds, 5 dimensions and canonical record links; no inferred aliases, global graph or silently merged Claim versions. |
| SIT-SC052 | All prerequisite and reason branches have scoped tests and controls | PC01-PC24 and all 40 current reason codes in validation §14; dormant request/representation codes do not create unauthorized features. |
| SIT-SC053 | Run and atomic result states remain independent of native source outcomes | SIT-VG010-SIT-VG011; every allowed envelope pairing and all 16 atomic state combinations checked against 6 permitted pairs. |
| SIT-SC054 | Finding tests preserve narrow conditions, contrary evidence and bounded absence | All 22 condition codes and 6 observation kinds in SIT-VG015; no detector, malicious-intent, incident-total or severity inference. |
| SIT-SC055 | View-specific cycles and multi-path structures remain distinguishable | SIT-VG004/SIT-VG008; citation versus acquisition cycle, self-cycle, cycle with exit, diamond and separate dimensional paths. |
| SIT-SC056 | Inventory zeros, unavailable qualification and unknown populations follow each field's own rule | Definitions §§21,28; SIT-VF001-SIT-VF024; no blanket missingness conversion or known-only denominator. |
| SIT-SC057 | Correction routes, grants, records, targets and outcomes have independent assertions | SIT-VF038-SIT-VF050; every required route leg, action/time/version, nonexclusive handling and distinct case/target pair. |
| SIT-SC058 | Stage and transition tests preserve independent evidence and finite cohort membership | SIT-VF029-SIT-VF037 and SIT-VF053; exact keys, Y/F/U, optional completion intervals and unique same-member admission baseline. |
| SIT-SC059 | Numerical tests preserve exact rational values and prohibit invalid sentinels | SIT-VG016; original N/T, bucket counts, optional half-up decimals, all valid value kinds and explicit non-results. |
| SIT-SC060 | Nested report fields, references and both presentation formats have conformance tests | Validation §13.2; SIT-VG012-SIT-VG018; state-list partition, finite witnesses, semantic parity and volatile exclusions. |
| SIT-SC061 | Runtime safety and resource tests remain explicit without invented policies or successful executions | SIT-VG019-SIT-VG023; WU9 permissions/budgets and WU10 serialization gates are named and held. |
| SIT-SC062 | All theory, product and output-field entries have reverse Trace coverage | 35 Traces, 40 existing theory entries, 16 product requirements, 57 leaf mappings and 19 logical responsibility owners. |
| SIT-SC063 | Prospective ownership does not prematurely create module/API/test paths or dependencies | Traceability §§2-4,9; WU10 binds concrete paths while preserving one semantic owner per leaf. |
| SIT-SC064 | Conformance failures are distinguished from input dishonesty and product-cut inadequacy | Validation §16; W7-28 remains a residual limitation; no synthetic test is scientific or source-authenticity validation. |
| SIT-SC065 | Golden expectations and counterexamples cannot be rewritten by the implementation under test | SIT-VG024-SIT-VG026; exact WU7 bodies/oracles retained, future mismatch evidence and scoped owner change control required. |
| SIT-SC066 | The incremental handoff preserves files, review status, later gates and actual authoring evidence | Three permitted Markdown files only; 37 prior files preserved; no code/schema/fixture/GitHub changes; stop after WU8. |

### 16.1 What would fail this document review

A missing reporting field, duplicate primary leaf owner, reused Trace ID, incorrect governing definition, absent negative/missing/boundary cell, unresolved cited ID or hidden future-policy assumption fails the affected WU8 document criterion.

Substantive examples include counting an unsupported documentary-origin inventory as real origins, treating an inquiry-assigned Artifact as per-Claim unassigned, collapsing multiple handling outcomes into a final state, using source seeds as an unrelated pipeline denominator, or dropping a contradictory premise to recover HHI. These must be corrected in the test specification without changing the accepted source contract.

If a governing contract genuinely does not determine a material output, identify that exact ambiguity and hold its executable expectation for the owner. Tests must not resolve it through a convenient implementation choice.

## 17. Current and future acceptance evidence

| Layer | Evidence required | State of this delivery |
|---|---|---|
| WU7 case and named reporting adoption | Contextual owner acceptance recorded at the next step | Recorded in validation §9; central register synchronization remains a later authorized edit |
| WU8 document/coverage checks | Current files, coverage/mapping checks, preserved bodies and archive agreement | Performed within the checked scope in §19 |
| WU8 owner adoption | Acceptance of WU8-C01-WU8-C03 and their stated limits | Submitted for review |
| Concrete safety/licensing specification | WU9 policy, limits and license decisions | Not performed by WU8 |
| Concrete architecture/interface specification | WU10 module paths, signatures, dependencies, serialization and witness policy | Not performed by WU8 |
| Final Phase 0 audit and approval | Complete consistent bundle, resolved in-scope blockers, actual owner approval and final file identities | Not reached |
| Scaffold or analytical implementation | Separately approved phase plan and actual permitted source files | Not started in this delivery |
| Runtime conformance/security/performance | Actual executions with adopted input/oracle, implementation revision, limits and result evidence | Not executed |

The same assistant authored and checked this increment. No independent second reviewer, empirical experiment, source authentication, live model run, CI result or security certification is represented as completed.

### 17.1 Future execution gate

All required obligations for an implemented capability must be exercised and pass before that capability's implementation/release gate passes. A parameterized test records each covered obligation. Skipped, unimplemented, policy-held or interrupted tests remain visible and cannot enter a passing count.

Positive/missing-data outputs are checked against the actual field semantics. A sparse accepted audit may legitimately complete with unavailable qualifications. A crashed or unfinished operation cannot claim the same evidence-limited completion. Golden fixtures remain immutable unless a documented owner change selects a new version.

## 18. Work Unit 8 read-only input identity manifest

The following source snapshots were read as the current governing documentation. Hashes identify exact bytes, not truth, authorship or empirical verification. Theory passages are used through the unchanged source map and the supplied source texts; no external study, regulation, standard or vendor state was updated.
| Current reference snapshot | SHA-256 |
|---|---|
| `PHASE_0_PLAN_Source_Integrity_Toolkit.md` | 2d97a820ae218c33cfd00dd96a762853e887f867973a2b2da0945fc4414495b1 |
| `source-integrity-toolkit-phase0-work-unit1/SPEC_AUDIT.md` | 3565ab8f1b08f30e06f4983ffd26adbe8bc977b655ebf410b634918a7ae7949a |
| `source-integrity-toolkit-phase0-work-unit1/THEORY_SOURCE_MAP.md` | 015e65baf3fcad8ce78a2285df8f2de8d5b7b4cbdd347707ba3cc5d5ba46b627 |
| `source-integrity-toolkit-phase0-work-unit2/PROJECT_INSTRUCTIONS.md` | cb5cf8f4d367bceacc313189469b3327370bed0450468d62a968825fee4a7746 |
| `source-integrity-toolkit-phase0-work-unit4/DEFINITIONS_AND_UNITS.md` | 913697e733d4430a64696b36a7893fe2113da7e2cfbcadbb54247a36c1792e9d |
| `source-integrity-toolkit-phase0-work-unit5/SOURCE_INTEGRITY_THREAT_MODEL.md` | d62d1fab2ea6891404193eda3bab4dc23c77c05bd608a6e55e2f6cb97f2a7e82 |
| `source-integrity-toolkit-phase0-work-unit5/UNRESOLVED_DECISIONS.md` | 06aefb57436c2f8e79238f87078b98e00e13a7feb1204fa6f1b1f6cab83656f9 |
| `source-integrity-toolkit-phase0-work-unit6/OBSERVABILITY_AND_REPORTING.md` | 44daa3c86fc7d12e7be16a3aedfe10d16b99f55aa69141f90319ce2b5e63ff6a |
| `source-integrity-toolkit-phase0-work-unit7/CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` | 32272903b45a8749115ed6b4ec9904dd864a2190f9e1a2ba43ced4c8256c0374 |
| `source-integrity-toolkit-phase0-work-unit7/V0.1_PRODUCT_SPEC.md` | 70ab331662741c0177908ec5ccac09ff7538f98643567eb3066e0ed8c9cb84e1 |
| `source-integrity-toolkit-phase0-work-unit7/VALIDATION_PLAN.md` | d4fd46e0b13af5fc37a84490007fd8cdfc7ee51f42745bb658f22fa7d9a4518a |
| `source-integrity-toolkit-phase0-work-unit7/SUCCESS_CRITERIA.md` | 563e4699abba3503a79731fa17fbe9fb5cc4428fef8e6332e3462bc6474f49e8 |

### 18.1 Complete preservation set

All 37 pre-delivery Markdown, ZIP and PDF files at the project paths were fingerprinted before authoring and checked again afterward. Ancillary image renders and temporary authoring utilities are outside this count. The new Work Unit 8 documents/archive are not part of this historical preservation set.
| Read-only historical artifact | SHA-256 |
|---|---|
| `Entropy as a Structural Boundary Condition, Not a Causal Force v2(2).pdf` | 7e5dbfb7cc270c68d0533b3ba74fbee1e96374004761cb46ffe6a4e56ef5bab4 |
| `Evaluation Closure Benchmark Inbreeding and the Design of Open AI Evaluation.pdf` | 002d2393d05cb2c8b1db0a70e844e3d775e2be2155db7b2ffaadaa8080c8b950 |
| `PHASE_0_PLAN_Source_Integrity_Toolkit.md` | 2d97a820ae218c33cfd00dd96a762853e887f867973a2b2da0945fc4414495b1 |
| `Source_Integrity_Toolkit_Phase_0_Work_Unit_1.zip` | 2f34db2d6d5b083d79e4339d32cd61c03047396db13e91ca632eb2d5de1dc3ec |
| `Source_Integrity_Toolkit_Phase_0_Work_Unit_2.zip` | 02364faefc55041998c72c79972e834bebd03fd73f5d497ab548577351ac39d0 |
| `Source_Integrity_Toolkit_Phase_0_Work_Unit_3.zip` | 02509a2e1f6ce5eee73aae2a70ae864d06e8cbc8657ebe8f3079c85a26b35f34 |
| `Source_Integrity_Toolkit_Phase_0_Work_Unit_4.zip` | 3137e587412b5304e9a80f09b3153247b4efbe1795a163d015e8fd29cfd19909 |
| `Source_Integrity_Toolkit_Phase_0_Work_Unit_5.zip` | 9cfdf8268ef7e2c33bf96ad7c4924b0a0b6c208e8a36851544697d2b5e3069dd |
| `Source_Integrity_Toolkit_Phase_0_Work_Unit_6.zip` | fe0eddeffdb345f6caa60695b177936f206eb9d3ad5ed492bed829091633ce6b |
| `Source_Integrity_Toolkit_Phase_0_Work_Unit_7.zip` | 64b58a99b4ab06076e32193b8db091c76e0914b578fb48249b4dc052ea1966ac |
| `The Boundary Vacuum Law_ Gradient, Boundary Failure, Topological Flow, and Pressure Capture in Social Systems v2(1).pdf` | 1323813d59152bc2d87ebab90dadce6d7a9232e14b67bb2b50a45e43b5e1e530 |
| `The Heat Death of Language v2.pdf` | 75af9e29467c5a4fae412e910fbac8b6945fa606d2567b1ac6fda98d41c691fb |
| `The Source Integrity Layer_ Presence × Integrity and the Governance of AI-Native Information Distribution.pdf` | bc233063e153fdcee83ad6e6088764f20dd24e3f4c7ae094b88f35905b52c3b3 |
| `The Universal Inbreeding Law v2(2).pdf` | b788c18b7a66886b623ea7c35b777643146b38e78b540acedde87cc5e019f2ee |
| `source-integrity-toolkit-phase0-work-unit1/SPEC_AUDIT.md` | 3565ab8f1b08f30e06f4983ffd26adbe8bc977b655ebf410b634918a7ae7949a |
| `source-integrity-toolkit-phase0-work-unit1/THEORY_SOURCE_MAP.md` | 015e65baf3fcad8ce78a2285df8f2de8d5b7b4cbdd347707ba3cc5d5ba46b627 |
| `source-integrity-toolkit-phase0-work-unit1/UNRESOLVED_DECISIONS.md` | 8025f25217c44eb39f1314a4ad5cc197ca46522f2af154a2039758e6a815a372 |
| `source-integrity-toolkit-phase0-work-unit2/PROJECT_INSTRUCTIONS.md` | cb5cf8f4d367bceacc313189469b3327370bed0450468d62a968825fee4a7746 |
| `source-integrity-toolkit-phase0-work-unit2/UNRESOLVED_DECISIONS.md` | 904e55c4df0adf7614b990b004c3a90e54e01a382c7b0a271580e056a05fd84c |
| `source-integrity-toolkit-phase0-work-unit2/V0.1_PRODUCT_SPEC.md` | 117c3ac96e6101508ff8cb643a94c3544cc111ba93dee054b2fafecb65c1db83 |
| `source-integrity-toolkit-phase0-work-unit3/CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` | 8d697b6eb556bbe8476f59e48664996fe12003a42efdce179648d25d9ffb924f |
| `source-integrity-toolkit-phase0-work-unit3/DEFINITIONS_AND_UNITS.md` | 81290ac5b442bfbe17e8302a3cb9dbeb9312d0c752899aa32693885a056cf48a |
| `source-integrity-toolkit-phase0-work-unit3/UNRESOLVED_DECISIONS.md` | 4c8611476bdb6151948284b77443958779d76d00b82f4a30e04af25928def32d |
| `source-integrity-toolkit-phase0-work-unit4/DEFINITIONS_AND_UNITS.md` | 913697e733d4430a64696b36a7893fe2113da7e2cfbcadbb54247a36c1792e9d |
| `source-integrity-toolkit-phase0-work-unit4/OBSERVABILITY_AND_REPORTING.md` | 224a2db1080b69c6d359da327585abd8b035915411cd34782b7c2de90c2c29ad |
| `source-integrity-toolkit-phase0-work-unit4/UNRESOLVED_DECISIONS.md` | d89d65beccbd59fe752d2ed9a8af37534d0c77de9d5b3b4450074afb7ce01e61 |
| `source-integrity-toolkit-phase0-work-unit4/V0.1_PRODUCT_SPEC.md` | f8bdaeb179189992eba5eb3ea544a94586468670de492b77f8faa521f58455d1 |
| `source-integrity-toolkit-phase0-work-unit5/SOURCE_INTEGRITY_THREAT_MODEL.md` | d62d1fab2ea6891404193eda3bab4dc23c77c05bd608a6e55e2f6cb97f2a7e82 |
| `source-integrity-toolkit-phase0-work-unit5/UNRESOLVED_DECISIONS.md` | 06aefb57436c2f8e79238f87078b98e00e13a7feb1204fa6f1b1f6cab83656f9 |
| `source-integrity-toolkit-phase0-work-unit5/V0.1_PRODUCT_SPEC.md` | 33e61809a50d74acde409e48509a3c0028315add2aace0b57d506e03753a7188 |
| `source-integrity-toolkit-phase0-work-unit6/CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` | 2e267bf916295b3a2d00876e9a69e40e3b47c67abb1ad39b99a29a6b6e36b722 |
| `source-integrity-toolkit-phase0-work-unit6/OBSERVABILITY_AND_REPORTING.md` | 44daa3c86fc7d12e7be16a3aedfe10d16b99f55aa69141f90319ce2b5e63ff6a |
| `source-integrity-toolkit-phase0-work-unit6/SUCCESS_CRITERIA.md` | 5414d3541c2cde9c37688dd3545baf1060d1dace48627a4e61ccfacd8fbe1646 |
| `source-integrity-toolkit-phase0-work-unit7/CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` | 32272903b45a8749115ed6b4ec9904dd864a2190f9e1a2ba43ced4c8256c0374 |
| `source-integrity-toolkit-phase0-work-unit7/SUCCESS_CRITERIA.md` | 563e4699abba3503a79731fa17fbe9fb5cc4428fef8e6332e3462bc6474f49e8 |
| `source-integrity-toolkit-phase0-work-unit7/V0.1_PRODUCT_SPEC.md` | 70ab331662741c0177908ec5ccac09ff7538f98643567eb3066e0ed8c9cb84e1 |
| `source-integrity-toolkit-phase0-work-unit7/VALIDATION_PLAN.md` | d4fd46e0b13af5fc37a84490007fd8cdfc7ee51f42745bb658f22fa7d9a4518a |

## 19. Local authoring checks and archive integrity

Only document utilities were used for text/registry inspection, source-reference checks, simple exact arithmetic, byte hashing and ZIP inspection. The checks did not implement the toolkit's parser, source-graph traversal, correction routing, renderer, diagnostic engine, test suite or network isolation.

| Check | Evidence actually inspected |
|---|---|
| Write allowlist | Validation, success and theory-to-code traceability Markdown only; exactly three archive members |
| Previous artifacts | All 37 pre-delivery hashes compared with the pre-authoring manifest |
| Numbered-body preservation | Validation §§1-8 and success §§1-14 equal their immediate predecessor bodies byte-for-byte |
| Existing field catalog | Exact set equality with reporting §17: 57 keys in 15 families |
| Leaf obligations | SIT-VF001-SIT-VF057 each has P/N/M/B content; 228 distinct obligation identifiers in the Trace crosswalk |
| Shared test families | SIT-VG001-SIT-VG026 exist and retain their future-policy gates |
| Current prerequisites/reasons | PC01-PC24 and all 40 reason codes have named branch/control exercises |
| Finding conditions | All 22 existing condition codes have witness/control coverage; no new condition or detector |
| Trace register | SIT-TR001-SIT-TR035 unique; all 57 leaves have one primary owner; no orphan M-family |
| Reverse mapping | All 40 source-map IDs and all 16 product requirements have Trace consumers |
| New criteria | SIT-SC047-SIT-SC066 extend the preserved SIT-SC001-SIT-SC046 |
| Key semantics | Inventory-zero versus unavailable qualification, inquiry-wide unassigned unit, exact RoleBinding alternatives, all 16 state pairs with 6 permitted combinations, and source/target/cohort population separation |
| Arithmetic | H7's 26/36 and 5/6, variant incidence 8/7, stage intervals and optional six-place decimals checked as written arithmetic |
| Document syntax | UTF-8, balanced code fences, numbered sections, table column structure, ID references and assembled-folder links |
| Archive agreement | Three allowed names and exact member bytes compared with final Markdown; ZIP integrity inspected |

These checks establish only the stated document consistency. They do not certify every future implementation branch, hidden input authenticity, exact future schema bytes, a second review, production security or empirical theory validity.

No prior document, source PDF, archive or GitHub repository was modified. No project dependency was installed. No source implementation, executable JSON Schema, runtime fixture, product test, CI workflow or Phase 0 approval artifact was created.

## 20. Incremental assembly, review and next unit

| File | Revision | Current role |
|---|---|---|
| `VALIDATION_PLAN.md` | 0.2 | Preserved WU7 prose oracle plus full field/contract/test/negative-control obligations and later gates |
| `SUCCESS_CRITERIA.md` | 0.3 | Preserved prior criteria plus 20 WU8 criteria, current approval scope, hashes and authoring evidence |
| `THEORY_TO_CODE_TRACEABILITY.md` | 0.1 | New stable Trace register, logical responsibility owners and reverse theory/product/field/test mappings |

Use these three working copies alongside product 0.4, lineage 0.3, reporting 0.2, definitions 0.2, threat 0.1, instructions 0.1, the WU1 audit/map and register 0.5 with its scoped supplements. Keep prior files and ZIPs as historical snapshots. Relative document links resolve in that assembled specification directory; unchanged dependencies are intentionally absent from this three-file increment.

Current review items are WU8-C01, WU8-C02 and WU8-C03 in validation §18. One scoped acceptance can adopt the package. It does not authorize runtime implementation or the complete Phase 0 baseline.

Stop after this handoff. The next unit is **Work Unit 9**, restricted to `PRIVACY_AND_DATA_HANDLING.md`, `LICENSING_NOTES.md` and `SOURCE_INTEGRITY_THREAT_MODEL.md`. WU10 then binds concrete architecture/dependencies/handoff, and WU11 performs the complete final audit and approval.
