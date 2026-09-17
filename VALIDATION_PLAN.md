# VALIDATION_PLAN

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Target release | v0.1 |
| Phase / work unit | Phase 0 / Work Unit 8: Validation, falsification and traceability |
| Revision | 0.2 |
| Date | 2026-09-17 |
| Status | PROPOSED FOR REVIEW; prior case baseline accepted contextually, WU8 obligations submitted |
| Theory Owner | Xiangyu Guo |
| Technical Owner | Unassigned |
| Current instruction | Accept the Work Unit 7 handoff and continue |
| Input owners | Definitions revision 0.2; lineage revision 0.3 with preserved input contract |
| Reporting reference | Reporting revision 0.2; named WU6 dependency accepted with the WU7 case package in §9 |
| Product / threat reference | Product revision 0.4; accepted WU5 threat model revision 0.1 |
| Current case inventory | One canonical hero, three isolated variants, twenty-eight micro-cases |
| Current artifact type | Preserved prose oracles plus field-level, contract-level and future execution obligations |
| Full field/test/Trace coverage | 57 registered output leaves, 228 leaf obligations, 26 shared test families and 35 Trace owners; §§10-18 |
| Runtime tests / Phase 0 approval | Not executed / not issued |

**Revision 0.2 reading rule.** Numbered sections 1-8 retain the complete Work Unit 7 body verbatim. Their then-pending status remains historical. Sections 9-18 contain the current Work Unit 8 extension. The fixed hero, variants, micro-cases, formulas, input records and report vocabulary are unchanged. This is a test specification; no executable test, runtime result or final Phase 0 approval is supplied.

## 1. Purpose and source discipline

This document defines the case-level oracle for the existing input and analytical/reporting contracts. The primary input owner is [CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md](CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md) §§24-28. Expected arithmetic follows [DEFINITIONS_AND_UNITS.md](DEFINITIONS_AND_UNITS.md) §§20-28. Output states, fields, checks and reasons follow [OBSERVABILITY_AND_REPORTING.md](OBSERVABILITY_AND_REPORTING.md) §§12-19. Product requirements and the narrow threat boundaries remain unchanged.

The conceptual basis is the existing forty-entry theory map, particularly SIT-T008, SIT-T018, SIT-T020, SIT-T022-SIT-T026, SIT-T029, SIT-T031-SIT-T032 and SIT-T035-SIT-T040. The source papers motivate preservation of evidence, evaluator ancestry, independent corrective input and separate replenishment stages. The record IDs, counts, fixtures and expected results here are toolkit operationalizations. They are not findings from an empirical experiment or literal schemas specified by the papers.

The fictional measurement language is a test scenario, not a reported real-world event. A future implementation is checked against the **supplied dossier**, including its attributed assertions and limits. Passing these cases cannot establish that an arbitrary real dossier is truthful, complete, manipulation-free or fit for deployment.

The user explicitly requested WU7. The package is prepared using the submitted WU6 realization; it does not silently mark earlier review choices approved or amend read-only reporting semantics. Final case adoption must include that reference or state an amendment. This document leaves WU8's comprehensive public-field tests, ownership and implementation Trace IDs open.

### 1.1 Oracle vocabulary

An expected available value below assumes that the entire required operation has completed on a structurally accepted input. Its output pairing is `execution_state = completed`, `result_state = available`. It is always accompanied by the exact scope, population, basis and limitations.

A completed evidence-limited result uses `completed / unavailable`, `value = null`, with the stated reasons. A structurally inapplicable interval uses `completed / not_applicable`, null and the appropriate reason. An unfinished computation uses `not_evaluated`, never evidence-unavailable or a zero result.

Listed reasons are required where their premise is present; additional relevant reasons may be emitted only if supported by the case. A renderer cannot hide another applicable blocker. Case descriptions explicitly distinguish required values, prohibited values and permitted implementation-neutral presentation.

No runtime-generated tool version, execution time, file digest or successful test result is fabricated in these prose expectations.

## 2. H7-01 canonical logical result oracle

### 2.1 Exact selected populations

The main source population is:

`E(H7-I1,H7-C1) = {H7-EA, H7-EB, H7-EC, H7-ED, H7-EE, H7-EF}`; `N = 6`.

`A(H7-I1) = A(H7-I1,H7-C1) = {H7-A, H7-B, H7-C, H7-D, H7-E, H7-F}`.

The original contribution H7-ER1, root export, after-versions, support documents, answer, training dataset, rubric, reference answer and evaluation results are outside this seed population. The case contains nineteen non-support Artifacts and eight support Artifacts. Their existence does not change the six-source seed count.

Pipeline cohorts explicitly contain the same six EvidenceItems in this main case, but their population definition is their own anchored coverage assessment. Correction targets form the separate set `{H7-R1-V1, H7-A, H7-D, H7-E}`. The origin comparison is exactly `{H7-O1,H7-O2}` under H7-IND12. These four population types must not be substituted for one another.

### 2.2 Origin and first-step oracle

| Seed | Finite acquisition witness, downstream to upstream | Qualified terminal origin set | Origin disposition | Immediate disposition |
|---|---|---|---|---|
| H7-EA | EA, L02, ER1, L01, O1 | {O1} | single_documented_origin | inherited_only_at_evidence_layer |
| H7-EB | EB, L03, ER1, L01, O1 | {O1} | single_documented_origin | inherited_only_at_evidence_layer |
| H7-EC | EC, L04, ER1, L01, O1 | {O1} | single_documented_origin | inherited_only_at_evidence_layer |
| H7-ED | ED, L05, EB, L03, ER1, L01, O1 | {O1} | single_documented_origin | inherited_only_at_evidence_layer |
| H7-EE | EE, L06, EA, L02, ER1, L01, O1 | {O1} | single_documented_origin | inherited_only_at_evidence_layer |
| H7-EF | EF, L07, O2 | {O2} | single_documented_origin | direct_origin_link_only |

IDs abbreviated in this table retain the `H7-` prefix. Witness order and edge identity are fixed. Display layout is not. The context material graph cannot replace these claim-qualified paths.

The five origin categories have counts `(unresolved, baseline/scope, declared, multi, single) = (0,0,0,0,6)`. The four immediate categories have `(inherited,direct,mixed,unresolved) = (5,1,0,0)`. Different units explain why six seed contributions, two documentary origin records and one supplied two-member comparison are all valid simultaneous observations.

### 2.3 M001-M007 values and non-results

All origin outputs in this table are scoped to I1/C1/acquisition. Counts/dispositions in other selected dimensions retain their own unestablished histories.

| Diagnostic / canonical field | Expected value | Basis and limit |
|---|---|---|
| M001 nominal_seed_artifact_record_count | 6 | Exact A(I1); not all Artifacts in the dossier |
| M001 unresolved_seed_artifact_reference_count | 0 | No unresolved seed artifact-reference positions |
| M001 seed_evidence_item_count | 6 | Exact E(I1,C1) |
| M001 claim_artifact_record_count | 6 | Six distinct seed artifact versions |
| M001 claim_unassigned_seed_artifact_record_count | 0 | Every explicit seed Artifact has a seed contribution |
| M002 reached_origin_record_count | 2 | O1 and O2 in the completed acquisition view |
| M002 documentary_origin_boundary_record_count | 2 | OB1/OB2 plus ACQ/CHAIN coverage; identity and same-dimension parents do not conflict |
| M002 origin_boundary_disclosures | OB1, OB2 | Supplied roles and documentary qualification remain attributed |
| M003 submitted_comparison_member_count | 2 | Only assessment IND12 |
| M003 qualified_process_set_member_count | 2 | IND12's supported acquisition pair, with four unexamined dimensions |
| M003 qualified_origin_set_member_count | 2 | Both pair subjects meet the documentary-origin requirement in this dimension |
| M004 per_seed_origin_memberships / origin_incidence_counts | O1: EA-EE, count 5; O2: EF, count 1 | c(O1)/N = 5/6 and c(O2)/N = 1/6; nonexclusive profile semantics retained |
| M004 seed_origin_dispositions | (0,0,0,0,6) | Full N preserved |
| M004 documentary_origin_resolution_fraction | 6/6 | Supplied-history resolution only |
| M005 single_origin_contribution_hhi | 26/36, equivalent 13/18; optional decimal 0.722222 | N = 6, bucket counts 5 and 1; all single-origin prerequisites met in this scope |
| M006 immediate_evidence_layer_dispositions | (5,1,0,0) | First-step relation enumeration, not novel-information detection |
| M006 inherited_only_seed_fraction | 5/6; optional decimal 0.833333 | Exact represented-evidence-layer fraction |
| M006 inherited_only_completion_interval | not_applicable; null; completion_interval_not_needed | There are no unresolved first-step members |
| M007 unresolved_frontier_reference_count | 0 | Completed acquisition-view inventory only |
| M007 unqualified_terminal_record_count | 0 | The represented acquisition terminals have qualified boundaries |
| M007 seed_items_with_unresolved_ancestry_count | 0 | Does not erase partial model history in M008/M015 |

No field named `independent_source_count`, `unknown_root_count`, effective sample size or source-integrity score may be produced. HHI is an available count-distribution diagnostic, regardless of whether the sources agree. It does not rank a political choice, institution or person and does not adjudicate the temperature claim.

For this HHI, PC02-PC10 must be satisfied where applicable to acquisition, PC12 and PC24 must be met, and the structural input prerequisite PC01 must be met. A missing capacity study or partial model history is not a reason to suppress this otherwise qualified acquisition result. Conversely, those missing areas cannot be declared complete because HHI is available.

### 2.4 Evaluator, externality and pipeline oracle

| Family / selected scope | Expected result | Required limitation |
|---|---|---|
| M008, H7-EVAL generator versus judge, model_evaluation view | shared_recorded_ancestor_count = 2, with exact set {H7-MBASE,H7-TRAINING}; two finite paired-path witnesses | Model history partial; common dataset reference does not establish exact training-row overlap or error correlation |
| M008, same pair | matching_family_label_count = 1, exact string H7-family | Label match is separate from ancestor count |
| M008, same pair | No shared exact role-bound object and no one-sided ancestor relationship in the represented view | Do not translate these empty scoped sets into process independence |
| M009, H7-EXT-F | Attributed external assessment for EF against I1, with ACQ/CONTEXT support | Externality does not imply selection or effective replenishment |
| M009, H7-INT-A | Attributed internal-reuse assessment for EA | Other seed subjects receive no invented externality label |
| M010, intake-1 / admission | Y = 6, F = 0, U = 0, T = 6; fraction 6/6 | Exact eligible cohort |
| M010, store-1 / preservation | Y = 6, F = 0, U = 0, T = 6; fraction 6/6 | Preservation has its own process records |
| M010, select-1 / selection | Y = 5, F = 1, U = 0, T = 6; fraction 5/6 | EF is the explicitly recorded non-occurrence; no inference about motive |
| M010, answer-use-1 / influence | Y = 3, F = 2, U = 1, T = 6; point fraction unavailable with stage_classification_unresolved | EA, EB, ED are Y; EC, EF are F; EE is U |
| M010, same influence cohort | completion interval [3/6,4/6], interval_kind finite_cohort_completion | Conditional finite-member completion, not confidence/probability or measured causal effect |
| M010, intake-1 to store-1 | Eligible recorded transition fraction 6/6 | Same explicit members, same run, unique fully evidenced admission baseline |
| M010, intake-1 to select-1 | Eligible recorded transition fraction 5/6 | Completes no influence or adequate-renewal claim |

Exact point-stage results have `stage_occurrence_completion_interval = not_applicable` with `completion_interval_not_needed`. The corresponding exact eligible transition intervals are likewise inapplicable. No influence transition fraction is introduced: only preservation/selection are permitted target stages for the restricted transition contract. No multiplication of the four stage rates is permitted.

For the model pair, the two ancestor witnesses are MGEN → MBASE ← MJUDGE and MGEN → TRAINING ← MJUDGE, with ML01/ML02 and ML03/ML04 respectively. Partial further history remains a material qualifier, not an invented missing common ancestor. The known positive witnesses remain available.

### 2.5 Correction, human review and retained context oracle

| Family / field or selected scope | Expected result | Scope/basis limit |
|---|---|---|
| M011 declared_correction_route_witnesses | Direct H7-CHANNEL route for each of R1-V1, A, D and E under amend | One represented channel, four target/action tuples; no count of four independent channels |
| M011 applicable_authorized_route_witnesses | The same four tuples qualify under H7-AUTH and the supplied day-long window | Imported grant, without verification of outside institutional authority |
| M012 correction_case_record_count | 1 | CASE1 |
| M012 handling_event_record_count | 1 | HAND1 |
| M012 linked_change_event_record_count | 3 | CHANGE-R1, CHANGE-A, CHANGE-D |
| M012 documentary_linked_change_target_count | 3 | {(CASE1,R1-V1),(CASE1,A),(CASE1,D)} |
| M012 cases_with_documentary_linked_change_count | 1 | CASE1 only |
| M012 handling disclosure | Native outcome accepted | Accepted request is not a successful-correction label |
| M012 target-change disclosures | R1-V1, A and D have evidenced before/after linkage; E has no supplied change evidence | E's missing effect is completed/unavailable for the requested documentary effect, reason change_evidence_missing; recorded absence of a change event is a separately bounded inventory fact |
| M012 reported_capacity_disclosures | Empty supplied capacity-assessment collection, with no capacity estimate | A finite case cannot establish sustained processing capacity |
| M013 human_contribution_disclosures | HREVIEW, named human role and the specific comparison/correction reasoning, with CORR basis | Actual review contribution remains visible |
| M013 corrective_independence_disclosures | Disclose that no qualifying HREVIEW/model-evaluation comparison was supplied | missing_comparison_assessment; no inferred independent human channel |
| M014 contestation_disclosures | EF contradicts C1, alongside its separate acquisition and assessment; all six seed stances preserved | No vote tally, equal weight or source exclusion |
| M014 anomaly_context_disclosures | AN1's original timing concern, null Claim and unclassified state | No auto-classification or extra source unit |
| M014 tail_stage_result_links | Link the actual EF stage observations, including selection/use non-occurrence | No whole-anomaly retention percentage; AN1 is outside that cohort |

The root export is one of the three changed targets. For the explicitly named downstream subset `{A,D,E}`, exactly two targets have documented changes, while the third has no supplied change evidence. B and C are outside this case's selected target set. No `correction_success_rate` or global propagation fraction is calculated.

An available human-review disclosure and an unavailable independence qualification are separate results. Zero supplied capacity/comparison records can be inventoried, but zero real capacity or zero independent humans is not an allowed conclusion.

### 2.6 Provenance profile and narrow findings

M015 must disclose all eight coverage records, including the partial model history. For the explicitly selected seven acquisition RelationAssertions L01-L07, `declared_basis_inventory` has seven documented_record labels and zero labels in the other basis categories. This is an inventory of that named population. For the explicitly selected eight H7-SUP references, `reference_availability_inventory` contains eight supplied and zero other availability states. These metadata counts are not independent verification or a global completeness percentage.

Required main-case observable findings include:

- `shared_origin_witness` for EA-EE through O1;
- `transformation_path_witness` for the supplied inherited chains, with the syndication qualification only where L03/MAT-B supplies it;
- `model_mediated_derivation_witness` for D's disclosed model role and B-based ancestry;
- `evaluator_overlap_witness` and separate `family_label_match` for the generator/judge pair;
- `case_handling_disclosure` and the three `linked_change_disclosure` observations;
- `downstream_change_undocumented` for E within CASE1;
- `recorded_stage_exclusion` for EF at select-1;
- `anomaly_or_contestation_disclosure` for EF's stance and AN1's context.

A finding's required narrow meaning, scope, finite witness, basis and limit are fixed. Exact report-local IDs and ordering follow the reporting contract. Different paths through the same origin do not multiply independent observations. Threat associations remain optional, nonexclusive and bounded by their card. No automated accusation of malicious laundering, capture, poisoning, collusion or suppression is implied.

### 2.7 Report envelope and semantic parity

For a future fully completed main audit, the report is `audit_report`, processing_state completed, input_validation accepted. It includes all fifteen capability families. Unavailable corrective independence, capacity, unprovided dimensions or process details do not turn the entire run into failure, nor are they hidden by a highest Level 0-4 label.

The Markdown must keep the six-source population, attributed two-origin comparison, exact 26/36 HHI scope, partial model history, unknown EE use, and undocumented E correction visible. JSON preserves the same substantive values, native states and non-results. Neither format may say “five sources verified”, “two globally independent sources”, “all corrections propagated” or “the source is clean”.

## 3. Controlled hero-variant oracle

### 3.1 H7-V01: Five-seed selection, unchanged surrounding dossier

The variant selects only A-E as source seeds. N = 5 and A(I1) = 5. All five acquisition rows are single_documented_origin at O1. M002 reached/qualified boundary counts for the seed-origin traversal are 1. M004 incidence O1 = 5, resolution 5/5. M005 is 25/25 = 1. M006 is inherited-only 5, direct 0, mixed 0, unresolved 0, fraction 5/5.

H7-IND12 is still an independently supplied two-member assessment about O1/O2 at its own qualified scope; its comparison size remains 2. It does not add O2 to the origin histogram of the five seeds. The six-member pipeline cohorts, four correction targets and three recorded changes also remain unchanged. No automatic seed-to-cohort join is allowed.

Comparison with the main case is a comparison of intentionally different source selection. A smaller HHI in the six-seed case is not proof of a corrected real-world system. The selection change must be displayed explicitly.

### 3.2 H7-V02: Seventh seed with unresolved parentage

N = 7; resolved seed Artifacts = 7; unresolved seed Artifact-reference count = 0, because the new Artifact U is known and the missing object is an **upstream EvidenceItem**. M002 still reaches two documentary-qualified origins. The six original rows qualify through COV-ACQ-OLD; EU remains unresolved_or_conflicted. M004 partition is `(1,0,0,0,6)` and resolution fraction 6/7. Incidences remain O1 = 5 and O2 = 1.

M005 is completed/unavailable, null, with unknown_endpoint and upstream_coverage_incomplete. No 26/36 fallback is returned for the seven-seed result. M006 is `(5,1,0,1)`; point fraction unavailable, and the permitted finite_record_completion interval is `[5/7,6/7]`. M007 has one represented unresolved frontier and one affected seed. There is no seventh original source and no upper bound on hidden roots.

The supported O1/O2 pair, positive model overlap, stage cohorts and linked changes remain visible. They retain their own populations and do not inherit EU's uncertainty as a dossier-wide failure.

### 3.3 H7-V03: Seventh seed with two known parents

N = 7; nominal seed Artifacts = 7; all branches have scoped complete documentary coverage. M004 partition is `(0,0,0,1,6)` and resolution 7/7. EG reaches O1 and O2, so the incidence columns are 6/7 and 2/7. Their sum is 8/7 because incidence is nonexclusive.

M005 is completed/unavailable with multi_origin_unallocated. There is no half-unit split and no normalization of 6 and 2 into concentration weights. M006 has six inherited-only and one direct-only member, no mixed immediate links and no unresolved member, so its exact fraction is 6/7. The two inherited E-to-E parents make EG inherited-only **at that layer** even though its complete ancestry contains two origins.

Pipeline/correction populations are again unchanged. No record is dropped to obtain a scalar. The HHI's unavailability and the complete origin-resolution fraction are compatible observations.

## 4. Micro-case authoring conventions and plan coverage

The micro-cases below use the same existing record tables, assertion envelopes, TimeValue rules and attributed evidence disciplines as H7-01. Each is an isolated dossier with its own bundle/snapshot/inquiry IDs. Local symbols C, E1, O1 and A1 are names within that case, not references to an absent hero snapshot. A notation such as E1 → O1 means an explicit affirmed originates_from relation in acquisition unless another predicate is named. A1 cites A2 always belongs to the citation view.

Where a case says **qualified complete acquisition**, its input includes the same required evidence-bearing fields as COV-ACQ/OB in the hero: all seed and reached members, the eight acquisition predicate types, one exact Claim/dimension, an identified investigator, supplied process excerpt, method, boundaries and an uncontradicted finite coverage claim. A qualified independence comparison additionally includes its exact subjects, pair/set form, dimension, independently described procedures, coverage and unexamined dimensions. These are explicit premises to materialize later, not heuristics for promoting undocumented nodes.

Where a case removes a prerequisite, that stated override controls. Unmentioned capabilities remain subject to their ordinary missing-input disposition. No default externality, model independence, authority, stage coverage or complete correction history is supplied.

| Plan-required micro-case | Canonical WU7 case |
|---|---|
| Three genuinely independent observations | W7-01 |
| Five domains copied from one root | W7-02 |
| Unresolved upstream lineage | W7-03 |
| Circular citations | W7-04 |
| Same-model-family generator and judge | W7-05 |
| Independent human evaluator with unknown training-data overlap | W7-06, preserving the qualified process scope and the unexamined dimension |
| Contested independent sources | W7-07 |
| Synthetic paraphrase chain | W7-08 |
| Correction logged but not propagated | W7-09, with separate undocumented and expressly observed non-change variants |
| External evidence reopening a previously closed lineage | W7-10 |

“Independent” in these titles refers to the explicitly supplied process-assessment premise. It is never inferred from node count, separate names or disagreement.

## 5. Canonical micro-cases

### W7-01: Three documented acquisition processes and one setwise assessment

**Input.** C has three seeds E1/A1, E2/A2, E3/A3. Each E points directly to a distinct O. All acquisition paths/boundaries have qualified complete support. One setwise assessment compares exactly O1/O2/O3 in acquisition, with separate capture procedures, an identified reviewer, inspectable support, scoped coverage and the other four dimensions unexamined.

**Expected.** N = 3, artifacts = 3, reached/documentary origins = 3, three single-origin rows, resolution 3/3. The comparison's submitted, qualified-process and qualified-origin counts are each 3. HHI = 3/9, optional display 0.333333. First-step inherited fraction = 0/3. No acquisition gap is represented.

**Must not conclude.** Statistical independence, truth, whole-system openness or qualification in an unexamined dimension. Removing the setwise assessment leaves origin inventories/HHI intact but makes qualified comparison outputs unavailable with missing_comparison_assessment. [M001-M007; SIT-SC009-SIT-SC014]

### W7-02: Five distinct domains, one documented acquisition

**Input.** Five Artifacts have distinct inert locator strings `https://one.invalid/item` through `https://five.invalid/item`; the strings are never fetched. Five E seeds inherit one non-seed E0 and its O1 acquisition under complete scope. Publication names are distinct declarations, with no extra capture evidence.

**Expected.** Five seed Artifacts, five contributions, one reached/documentary origin, incidence 5/5, HHI 25/25. All five are inherited-only, fraction 5/5. Shared-origin and explicit transformation witnesses are available. No supplied independence comparison means the qualified-member statistic is unavailable, rather than 1 or 5.

**Must not conclude.** Five observations, collusion, coordinated malicious intent or a global credibility verdict. Domain labels cannot change the counts. [M001-M007; SIT-TH001-SIT-TH003]

### W7-03: One unresolved endpoint shared by two seeds

**Input.** E1/A1 and E2/A2 both derived_from the same typed UnresolvedReference UX expected to denote EvidenceItem, with the expected C role disclosed. No actual upstream event or boundary is supplied. Partial coverage acknowledges the unknown area.

**Expected.** Two known seed Artifacts; unresolved seed Artifact references = 0. N = 2, both origin rows unresolved, documentary resolution 0/2, represented frontier count 1 and affected-seed count 2. Reached/documentary origin-record counts in the examined view are 0. HHI is unavailable with unknown_endpoint/upstream_coverage_incomplete. The unresolved immediate endpoints give first-step completion interval [0/2,2/2], not a point estimate.

**Must not conclude.** One or two hidden original observations, zero actual origins, independence from missing data, or two distinct sources created by pseudonyms. [M002, M004-M007; SIT-SC003, SIT-SC014]

### W7-04: Citation circularity and claim-origin circularity are separate

**Input.** Two seeds point to qualified O1 and O2. A1 cites A2 and A2 cites A1. The acquisition view has no cycle. A separate version of the case replaces acquisition links with E1 derived_from E2 and E2 derived_from E1, plus one exit from E1 to qualified O1; all records and claims remain structurally valid.

**Expected.** In the citation-only case, the citation cycle is reported and acquisition HHI remains 2/4. In the acquisition-cycle variant both seeds retain cyclic unresolved ancestry, the positive O1 exit is visible, and HHI is unavailable with lineage_cycle. No general DAG rejection is allowed. The finite cycle includes its exact assertion IDs and view.

**Must not conclude.** False Claim from a citation cycle, independent corroboration through the cycle, or a fully resolved root result by ignoring the cyclic branch. [M002, M004-M007; SIT-TH005]

### W7-05: Related generator and judge

**Input.** Evaluation V binds generator M1 and judge M2; each has a documented model_derived_from edge to M0. Both have exact family_label F. History beyond M0 is explicitly partial. M1 and M2 are distinct records. No shared dataset record is supplied in this micro-case.

**Expected.** For that role pair, shared_recorded_ancestor_count = 1 and matching_family_label_count = 1, with separately disclosed empty exact-role identity and partial further history. A model-overlap witness remains available. Removing the two ancestry edges while retaining labels reduces the recorded shared-ancestor count to 0 in the examined graph, but preserves the label match and the unknown ancestry.

**Must not conclude.** Measured correlated error, guaranteed dependence of every output, independence after deletion of a path, or a model-quality score. [M008; SIT-SC015]

### W7-06: Independent review procedure with unexamined model exposure

**Input.** Two human-review Evaluations V1/V2 inspect the same target. Each has an identified/protected human reviewer, specific contribution, method Artifact and supplied review result. One qualified pairwise assessment of V1/V2 concludes independent_process in analytical_method after comparing the separate review procedures. model_ancestry and evaluation_rubric exposure remain explicitly unexamined.

**Expected.** The qualified_process_set_member_count for that exact procedure comparison is 2. A qualified_origin_set_member_count is not applicable to Evaluation subjects. Both substantive human contributions are disclosed. The common reviewed target is shown as a common target, not automatically a process ancestor. Model/training exposure remains unknown; no acquisition/whole-review independence total is emitted.

**Must not conclude.** A human role guarantees independence, independence in analytical_method resolves training overlap, or two reviews prove sustained renewable judgment. Removing the procedure evidence leaves both contributions visible while the qualified count becomes unavailable. [M003, M008, M013]

### W7-07: Independently acquired disagreement

**Input.** Two seeds have distinct qualified acquisition roots and a qualified pairwise acquisition comparison. E1 supports C; E2 contradicts C. The disagreement concerns the recorded Claim, with no dispute about either acquisition history.

**Expected.** N = 2, two single-origin rows, qualified comparison size 2, HHI 2/4, two preserved stance records. Neither seed is discarded. The factual disagreement does not alone set premise_disputed on the origin graph or block concentration.

**Must not conclude.** Equal evidentiary weight, a tie on truth, low integrity because of disagreement, or independent votes whose sum decides C. [M003-M005, M014; SIT-SC023]

### W7-08: Model paraphrases preserve the inherited source

**Input.** E1 summarizes E0; E2 translates E1; E3 summarizes E2. E0 is non-seed and directly originates from qualified O1. E1-E3 are seeds with distinct Artifacts, and their generation roles are supplied, possibly naming different models. Acquisition coverage is complete.

**Expected.** N = 3, one documentary origin, HHI 9/9, inherited-only fraction 3/3, explicit transformation and model-mediated witnesses. Different wording, languages and model endpoints add no root under these supplied relations.

**Must not conclude.** Semantic novelty was measured, every synthetic Artifact is false, or translation itself reopened acquisition. An independently evidenced additional acquisition would require another explicit branch and a new case revision. [M004-M006, M008; SIT-TH004]

### W7-09: Recorded correction without recorded propagation

**Input.** One case targets A1, contains an accepted handling record and a declared channel, but has no change event. The input remains valid. A second case version supplies an empirical-review Evaluation/result excerpt stating that A1 was inspected at a named cutoff and no amendment was observed; it still supplies no change event.

**Expected.** Both versions have correction counts (cases,handling,changes,documented targets,cases with change) = (1,1,0,0,0). In the first, the requested target effect is unavailable with change_evidence_missing. In the second, preserve the separately attributed negative observation and its time, while still distinguishing zero change records from an inferred universal non-change. No new CorrectionEvent subtype is invented for “not propagated”.

**Must not conclude.** Accepted equals corrected, missing event equals failed, or one observation proves permanent absence of propagation. [M011-M012; SIT-SC021, SIT-SC025]

### W7-10: Independently grounded input enters a later represented run

**Input.** Two independently audited snapshots are explicitly described. The first has one acquisition root and only its reuse chain; its coverage is finite and has no external replenishment event. The second retains the represented history and adds O2/E2, a qualified acquisition comparison, an externality assessment against the original reuse boundary, and separate supported admission, preservation, selection and influence records for E2. Before/after dossiers are supplied as separate intended audit inputs; predecessor is never dereferenced.

**Expected.** Each report describes its own seed set and stage records. The second shows an attributed external observation that was admitted, preserved, selected and used at the stated keys. If it has two direct seed contributions, one for each root, its HHI is 2/4. The first one-seed report has HHI 1/1. The reports disclose the changed population. A control variant has identical externality/admission but did_not_occur at selection and use; those stage outputs must differ.

**Must not conclude.** The scalar change isolates a causal improvement, restored model performance, or sufficient long-run replenishment. This is a source-path reopening demonstration, not longitudinal model-collapse simulation. [M004-M005, M009-M010]

### W7-11: One Artifact has different claim-relative roles

**Input.** Inquiry I targets C-issued (“Publisher issued statement S”) and C-event (“The measured event had value V”). Artifact A contains the issued statement. E-issued/A is bound to C-issued and originates from issuance O-issued. E-event/A and a second E-copy/B are bound to C-event, inheriting sensor acquisition O-measured through claim-specific relations. Each view has its own scope and supported boundary.

**Expected.** Artifact A is counted once in the inquiry's union inventory, but separately participates in each claim's contribution population. C-issued has N = 1 and issuance origin O-issued; C-event has N = 2 and measured origin O-measured. No E-to-E edge crosses Claim versions. Source use for one question cannot certify its role for the other.

**Must not conclude.** A's issuance origin is independent measurement for C-event, or the two claim-level histograms can be pooled as one integrity score. [M001-M005; SIT-SC001, SIT-SC009]

### W7-12: Pairwise qualifications do not create a joint set

**Input.** Three documentary acquisition origins O1/O2/O3 and three direct seeds. Qualified pairwise assessments cover O1/O2 and O2/O3. No setwise comparison exists, and O1/O3 process independence remains unexamined.

**Expected.** Each supplied assessment has submitted/qualified size 2 at its own scope. The three-origin inventory and HHI 3/9 can remain available. There is no qualified joint size 3, no sum 4, no maximum independent set and no transitive completion.

**Must not conclude.** The inventory or low concentration fills the missing O1/O3 assessment. [M002-M005; SIT-SC010]

### W7-13: Complete multi-parent ancestry with no allocation

**Input.** One seed E/A has two inherited parents E1/O1 and E2/O2 under complete acquisition scope. Both documentary boundaries qualify. A source portion_note says “roughly half from each” as free text, with no adopted allocation record.

**Expected.** N = 1, one multiple_documented_origins row, resolution 1/1, incidences O1 = 1/1 and O2 = 1/1. HHI unavailable with multi_origin_unallocated. The immediate inherited-only fraction is 1/1. The free-text estimate remains an attributed note.

**Must not conclude.** HHI = 1/2, an origin-probability distribution, or a parser-created allocation from the note. [M004-M006; SIT-SC011-SIT-SC013]

### W7-14: A diamond contains several paths to one origin

**Input.** Seed E inherits two resolved contributions E-left/E-right, both of which originate from the same qualified O1. Complete coverage lists both branches and no other parents. Neither parent is an extra seed.

**Expected.** N = 1, one single_documented_origin row, O1 incidence count 1, resolution 1/1, HHI 1/1. Both witness paths may be displayed, but no count treats O1 twice. Immediate inheritance is known even though two paths exist.

**Must not conclude.** Two independent roots, duplicated contributions or a multi-origin row solely from path multiplicity. [M002, M004-M006]

### W7-15: Known immediate copying, unknown distant ancestry

**Input.** E1 copies resolved E0 under supported complete immediate coverage. E0 then derives from typed unresolved UX. Full upstream coverage is partial; the immediate E1 link and its resolved endpoint are not disputed.

**Expected.** N = 1; inherited-only immediate fraction 1/1; one unresolved origin row; HHI unavailable with unknown_endpoint/upstream_coverage_incomplete. The distant gap does not change the completed first-step classification. Documentary-origin resolution is 0/1.

**Must not conclude.** Full ancestry is established by the copy edge, or every metric must be unavailable whenever any ancestor is unknown. [M004-M007; SIT-SC013]

### W7-16: Caller decomposition changes contribution units

**Input.** E1 and E2 are distinct seed contributions from A1, both reaching O1. E3 is from A2 and reaches O2. Complete acquisition coverage is supplied; there is no automatic semantic deduplication. An explicit alternate case chooses one contribution per Artifact instead.

**Expected.** Main N = 3, nominal Artifacts = 2, buckets 2 and 1, HHI 5/9. Alternate N = 2, buckets 1 and 1, HHI 2/4. Both results disclose their supplied contribution decomposition and different selection.

**Must not conclude.** A change in represented granularity proves a change in real information, that two contributions from A1 are independent, or that the toolkit has measured semantic duplication. [M001, M004-M005; SIT-TS002]

### W7-17: Documentary, declared and chosen boundary cuts coexist

**Input.** Four direct seeds have fully enumerated represented parents. O1 has a qualified documented_origin boundary; O2 has declared_origin only; O3 is an explicit reference_baseline; O4 an explicit scope_cut. Coverage supports that these are the intended boundary roles without pretending the latter three are documentary acquisition origins.

**Expected.** N = 4; origin dispositions single = 1, declared = 1, baseline/scope = 2, multi = 0, unresolved = 0; resolution 1/4. HHI unavailable, with declared_origin_only and baseline_or_scope_cut. The direct-link profile can be 4 direct / 4 because it describes immediate serialized links, not qualified origin independence.

**Must not conclude.** An explicit chosen cutoff is an observed original source, or unknown upstream is closed by renaming a terminal “root”. [M002, M004-M006]

### W7-18: Protected commonality and inspectable attestation

**Input.** Two seeds have an expressly shared opaque origin reference. In variant A this is only typed unresolved UX, with identity withheld. In variant B a resolved OriginEvent O-protected and an origin boundary are supported by a named/protected attestor's supplied, scoped attestation summary and method; underlying identity remains withheld. No independence comparison is supplied in either.

**Expected.** A preserves one shared represented unresolved endpoint and cannot supply a documentary origin. B may qualify the one opaque origin under its actual protected-attestation basis, with the withheld underlying material disclosed. Record pointers alone do not supply the absent attestation. Neither variant creates distinct roots from redacted display names.

**Must not conclude.** Public identity verification, a privacy guarantee, or independent observations merely because several sources cite a protected witness. [M002-M007, M015; SIT-TS006]

### W7-19: One unknown cohort member remains in the denominator

**Input.** An eligible five-member selection cohort has evidence-bearing occurred for E1/E2/E3, did_not_occur for E4, and unknown for E5. One exact run/stage key and its unique coverage anchor are supplied.

**Expected.** T = 5, Y = 3, F = 1, U = 1. Point fraction unavailable with stage_classification_unresolved. Finite_cohort_completion interval [3/5,4/5]. Adding another unknown report to a known positive E1 preserves its Y classification; adding an applicable contrary did_not_occur makes E1 U and changes the partition to Y = 2, F = 1, U = 2, interval [2/5,4/5]. All source rows remain visible.

**Must not conclude.** 3/4 as the rate, majority/newest-wins resolution, or a statistical confidence interval. [M010, M014; SIT-SC018]

### W7-20: Final-only context cannot establish retention

**Input.** The dossier has final answer source Artifacts and one unclassified Anomaly with null claim_ref and supplied original context. No pipeline_universe coverage or earlier intake records exist. An additional control explicitly enumerates an empty finite population but supplies no valid stage anchor.

**Expected.** Final inventory and anomaly context are available. Retention/stage fractions are unavailable with cohort_anchor_missing/cohort_universe_unestablished as applicable. The empty declared inventory can be zero at that inventory scope; neither control has a stage ratio. No source must be forced into the existing Claim taxonomy to be admitted.

**Must not conclude.** Suppression, 0% or 100% retention, a missing source count derived from the final list, or rarity determined by the toolkit. [M010, M014; SIT-SC019, SIT-SC023, SIT-SC027]

### W7-21: Action-limited authority and documented change are separate

**Input.** Channel H targets A1 with declared action amend. A supplied grant authorizes review only for that target/window. A case-linked, fully supported change A1 to A2 is separately supplied. Another control gives amend authority with unknown effective time for a time-specific route query.

**Expected.** Declared route available. Authorized amend route unavailable with authority_inapplicable in the first case, and time_applicability_unknown/authority_unestablished as warranted in the control. The documented `(case,A1)` target change remains available at its actual process basis.

**Must not conclude.** A known change retroactively grants authority, review implies amend, or uncertainty in authority erases the separately supplied observed action. [M011-M012; SIT-SC020-SIT-SC021]

### W7-22: Failure outcome, explicit removal and duplicate target changes

**Input.** One case has handling accepted and then handling failed, both retained. Two supported change-event records refer to the same `(case,A1)` retraction: resolved before A1, after_ref null, explicit after_absence_reason and supported removal linkage. The two event records have distinct IDs.

**Expected.** Run completed on valid input. Counts are cases 1, handling 2, change events 2, documentary linked-change targets 1, cases with linked change 1. The native failed outcome is in an available disclosure; no newest-wins final status is invented. A control replaces explicit removal with an unresolved after-state and retains the event inventory but cannot qualify the target change.

**Must not conclude.** Two corrected targets, a successful substantive correction, runtime failure from native failed, or removal from an unknown after-state. [M012; SIT-SC021, SIT-SC024]

### W7-23: Relevant disputed identity blocks only dependent conclusions

**Input.** Two otherwise eligible single-origin seed rows end at O1/O2. A supplied same_identity_as assertion relates those origin IDs at origin_event identity level. The software is given no canonicalized replacement dossier. A separate variant instead supplies an active denial of one necessary origin relation, with weak declaration basis. The rest of the input is well formed.

**Expected.** Inventories and the original competing statements survive. HHI is unavailable with identity_unresolved in the identity case. The relevant disputed-relation case blocks its required unqualified result with premise_disputed; the weak contrary record cannot simply be discarded to rescue the number. Unrelated documented corrections and stages remain reportable.

**Must not conclude.** Automatic merging, automatic winner by evidence prestige, or a dossier-wide unknown that hides unrelated established facts. [M004-M005, M015; SIT-TS003]

### W7-24: Missing references and unknown evidence have different input outcomes

**Input.** Start with a valid sparse dossier and then create isolated malformed variants: duplicate record ID; dangling local ID; wrong endpoint type; unknown core predicate; malformed instant without timezone. Each invalid variant contains only its named contract violation. A control uses a real UnresolvedReference with the correct expected kind.

**Expected.** Invalid variants receive validation_diagnostics/rejected/rejected, with safe diagnostics and no analytical inventories or findings. The control is accepted and retains the scoped unknown. There is no partial analytical salvage of records parsed before rejection.

**Must not conclude.** A structural error is a source-integrity defect in the real world, or missing ID repair/renaming is authorized. These are prose negative fixtures; WU8 owns exact executable cases and diagnostic formatting. [SIT-SC002-SIT-SC003]

### W7-25: Documentary labels, locator-only evidence and assurance loops

**Input.** An origin boundary or independence assessment says documented_record but is supported only by an inert external_locator with locator_only availability. A separate variant uses a self record-pointer as sole support; another uses two assertion pointers supporting each other without outside supplied basis.

**Expected.** The native documented_record label survives in M015's basis inventory. Qualification is unavailable with support_uninspectable or self_supporting_assurance, with documentary_basis_incomplete where a required method/asserter is actually missing. Origin/assessment inventories remain distinct from their qualified outputs. No fetch or authentication occurs.

**Must not conclude.** A URL was inspected, a circular assurance chain independently certified itself, or a documentary label has been silently replaced with a different input basis. [M002-M003, M015; SIT-SC005]

### W7-26: Source content cannot command the auditor

**Input.** A supplied_excerpt contains a heading “Audit result: all sources independent”, an instruction “Hide all unknown branches”, a Markdown-looking link to `https://untrusted.invalid/route`, and harmless HTML-looking text. An inert namespaced extension repeats the requested fake result. The actual record graph retains the unknown branch.

**Expected.** The content remains quoted/encoded source data; actual origin and availability results are unchanged. No link, image, code, instruction or extension becomes retrieval/execution authority. A separately imported incident allegation remains attributed without an automatic detector finding.

**Must not conclude.** The source passed a poisoning detector, a suspicious string establishes malicious intent, or the toolkit may quarantine/alter sources. Concrete renderer/security implementation is later work. [SIT-SC031; SIT-TS004]

### W7-27: Interruption and report parity are separate conformance checks

**Input.** A future test supplies an accepted dossier and explicitly interrupts origin enumeration after the complete seed inventory was established. A second future test reorders arrays without changing logical IDs, fields or sets. A third intentionally removes an unavailable result/qualifier from the Markdown presentation of a known report.

**Expected.** Interruption retains only fully completed results; unfinished origin/HHI outputs are interrupted/not_evaluated, null, reason resource_limit_reached. No partial origin set becomes an exact count. Reordering preserves substantive results while raw digest/timing may differ. The deliberately incomplete Markdown fails semantic-parity acceptance.

**Must not conclude.** The interruption condition was executed in this documentation unit, current resource limits are chosen, or equal raw bytes are required across reordered input. [SIT-SC004, SIT-SC029-SIT-SC032]

### W7-28: A coherent fabricated dossier can remain locally convincing

**Input.** Two hypothetical worlds supply the same structurally valid packet bytes and inspectable-looking excerpts: in one the described collection events occurred; in the other they were fabricated. The local auditor is supplied no distinguishing evidence. No real identity is accused.

**Expected.** A deterministic local audit has the same structural result and the same outside-authentication limitation for both packets. A later packet containing an external contradiction can change the scoped evidence profile, but that is a different input snapshot. No invented private access or hidden truth oracle distinguishes the original byte-identical inputs.

**Must not conclude.** Passing the fixture proves the real-world dossier true, all forgeries are detectable, or a local signature/record check can settle source truth. This is a residual-limit witness rather than a feature request. [SIT-TS001, SIT-TS007; SIT-SC005, SIT-SC026]

## 6. Family coverage and quantitative hand-checks

### 6.1 Fifteen-family coverage

| Family | Main-case oracle | Additional discriminating witnesses |
|---|---|---|
| M001 | Six source records / contributions, no ancestor inflation | W7-02, W7-11, W7-16, W7-24 |
| M002 | Two documentary origin boundaries under scoped coverage | W7-01, W7-03, W7-17-W7-18, W7-25 |
| M003 | Exact supported pair size 2 | W7-01, W7-06-W7-07, W7-12, W7-25 |
| M004 | Five seeds at O1 and one at O2 | H7-V02-H7-V03; W7-04, W7-13-W7-17 |
| M005 | 26/36 with complete single-origin premise | H7-V01-H7-V03; W7-12-W7-17, W7-23 |
| M006 | Five inherited-only, one direct-only | H7-V02-H7-V03; W7-08, W7-13-W7-15 |
| M007 | Zero represented acquisition gaps, partial model history separate | H7-V02; W7-03, W7-15, W7-18 |
| M008 | Two strict shared model ancestors plus one family string | W7-05-W7-06, W7-08 |
| M009 | External EF and internal reuse EA, each attributed | W7-10 and its selection-negative control |
| M010 | Separate stage fractions/interval, two eligible transitions | W7-10, W7-19-W7-20 |
| M011 | Four target/action tuples through one declared/granted channel | W7-09, W7-21 |
| M012 | 1 case, 1 handling, 3 changes, 3 distinct targets | W7-09, W7-21-W7-22 |
| M013 | Substantive human contribution with missing process comparison | W7-06 |
| M014 | EF disagreement and unclassified AN1 retained | W7-07, W7-19-W7-20 |
| M015 | Exact named support/basis inventory and partial model coverage | W7-18, W7-23, W7-25, W7-28 |

This is case-family coverage. It does not replace WU8's positive/negative/missing/boundary test matrix for **every individual public field, state, reason code and prerequisite**.

### 6.2 Exact arithmetic oracle

| Named calculation | Exact structural form | Optional decimal / interpretation |
|---|---|---|
| Main contribution HHI | (5² + 1²) / 6² = 26/36 | 0.722222 |
| Main inherited-only fraction | 5/6 | 0.833333 |
| Main influence completion | [3/6, (3+1)/6] | [0.500000, 0.666667]; T remains 6 |
| Five-seed HHI | 5²/5² = 25/25 | 1.000000 |
| Unknown-variant origin resolution | 6/7 | 0.857143 |
| Unknown-variant inherited completion | [5/7,(5+1)/7] | [0.714286,0.857143] |
| Multi-origin incidence sum | 6/7 + 2/7 = 8/7 | Nonexclusive incidence, not a probability distribution |
| Three equally represented origins | 3/9 | 0.333333 |
| Two-contribution versus three-contribution granularity | 2/4 versus 5/9 | Different populations; no isolated real-world improvement |
| Five-member stage interval | [3/5,4/5] | [0.600000,0.800000] |
| One conflicted positive in that stage | [2/5,4/5] | [0.400000,0.800000] |

Origin partitions always sum to N; first-step partitions sum to N; stage partitions sum to T. Case, handling-event, change-event and distinct-target counts need not equal one another. No arithmetic converts a missing population into T = 0 or adds unknown frontier references to documentary origins.

### 6.3 Structural discrimination requirement

The case suite must preserve distinguishable outcomes for: derivative plurality versus separately documented capture; known multi-origin versus unknown origin; citation cycle versus acquisition cycle; missing change evidence versus an expressly attributed negative observation; known route versus matching authority; procedure independence versus unexamined model exposure; final-only material versus a bounded intake cohort; and a source assertion versus a completed auditor result.

If any pair collapses into the same report after removing only layout differences, inspect whether a substantive distinction has been lost. Different fictional titles with identical graph/evidence content do not require different integrity findings.

## 7. Promotion into later fixtures and tests

After adoption, a later expressly authorized phase may translate the prose tables into explicit `sit-bundle/0.1` records. It must materialize all defaults and every local reference, preserve the synthetic qualification, include supporting excerpts and scope, and retain non-seed ancestors and original before/after versions. It may not repair a blocked result by dropping a row or adding an unapproved independence/coverage assertion.

WU8 will assign exact field-level test ownership, required reason/state combinations, malformed-input variants, security tests, boundary tests, performance obligations and implementation Trace IDs. WU9 decides concrete resource/export/privacy limits and license treatment. WU10 decides module/interface ownership and canonical byte serialization. None is chosen by a fixture author merely to make a snapshot convenient.

Golden expectations remain independent of the future implementation under test. An output generator cannot bless its own results by overwriting expectations. Any mismatch must identify the input premise, existing product/definition/report rule and required owner decision. If a prose ambiguity changes a public result, keep that case held for clarification rather than silently selecting a convenient interpretation.

Runtime success requires actual executions and evidence in the later authorized phase. This delivery has no executable fixture, parser, traversal, product test, content detector, network access, CI workflow or GitHub write.

## 8. Work Unit 7 review, stop point and next handoff

| Review package | Proposed freeze | Limit |
|---|---|---|
| WU7-C01 | H7-01 and H7-V01-H7-V03 exact input scopes, declared evidence and logical outcomes | Depends on the existing WU6 reporting realization; no new metric or global independence count |
| WU7-C02 | W7-01-W7-28, semantic/numeric oracle and later fixture-promotion discipline | Case baseline only; does not complete WU8 testing, WU9 protection or the final Phase 0 approval |

These review IDs do not edit the central SIT-D register. WU7 produces exactly four Markdown files, all under its allowlist. The local authoring evidence and input hashes are recorded in `SUCCESS_CRITERIA.md` §§12-13. Stop after this package. The next planned unit is **Work Unit 8: validation, falsification and field-level test/traceability planning**.

## 9. Work Unit 8 authority and accepted case baseline

The preceding handoff submitted WU7-C01 and WU7-C02, including the explicitly named WU6-C01-WU6-C03 reporting dependency, and identified Work Unit 8 as the next unit. The user answered “可以，继续”. This is recorded here as contextual acceptance of that enumerated case package and its named reporting dependency **for continued specification work**, together with authorization to prepare this unit. It does not authorize implementation, source changes, a new metric, or final Phase 0 approval.

The central decision register remains revision 0.5 because this unit's allowlist excludes it. Its historical status entries must later be synchronized from the existing scoped records and this acceptance record, without backdating or rewriting the original alternatives. The WU5 acceptance supplement remains in reporting §11.1. No new central SIT-D decision is created here.

The write allowlist is exactly:

- `VALIDATION_PLAN.md`, revision 0.2;
- `SUCCESS_CRITERIA.md`, revision 0.3;
- `THEORY_TO_CODE_TRACEABILITY.md`, revision 0.1.

Definitions 0.2, lineage 0.3, product 0.4, reporting 0.2, threat 0.1, instructions 0.1, the original plan, WU1 source audit/map and previous archives remain read-only. Their reviewed identities and preservation checks are in success §§18-19. This increment leaves the WU7 hero populations and exact expected values unchanged.

### 9.1 Single-owner rule

Definitions own analytical meaning, lineage owns accepted input, reporting owns output state and shape, and the accepted WU7 cases own their exact logical oracles. Tests expose violations of those rules. A test author cannot add missing evidence, replace a denominator, define a new root, or rewrite a source claim merely to make implementation convenient.

For example, `documentary_origin_boundary_record_count` is a finite qualifying-record inventory under definitions §21.2. An examined view with no qualifying boundary can yield zero with its gaps. By contrast, `qualified_process_set_member_count` is unavailable when the required comparison qualification fails. The field tests below preserve this existing difference; they do not apply one blanket unknown-value rule to every count.

Similarly, `claim_unassigned_seed_artifact_record_count` follows the inquiry-wide rule in definitions §21.1: a resolved seed Artifact lacking **any** seed EvidenceItem binding in that Inquiry is unassigned. A binding to one targeted Claim prevents treating the same Artifact as unassigned just because another Claim has no contribution. No new per-Claim unassigned metric is introduced.

## 10. Test-obligation model and coverage contract

### 10.1 Four meanings of a field test

A **positive** obligation supplies the exact prerequisites and checks the registered value, scope and evidence. A **negative** obligation either supplies an adverse but well-formed input or deliberately constructs a nonconforming output mutation. The text marks an output mutation explicitly. Negative does not mean that an adverse finding is a failed test.

A **missing-data** obligation preserves a valid explicit gap and verifies its actual consequence. Depending on the registered field, that may be an exact empty inventory, a retained weaker disclosure, an unavailable qualification, or an interval with unknown members. Missing required syntax is tested separately as structural rejection.

A **boundary** obligation tests a distinction capable of changing a public result: empty versus unestablished populations, multi-parent versus multi-path ancestry, a different Claim/dimension/version, complete versus incomplete execution, or exact fraction versus completion interval.

Each `SIT-VFnnn` below identifies one existing reporting §17 leaf. Suffixes `-P`, `-N`, `-M` and `-B` identify four separate logical obligations. There are 57 leaf IDs and 228 such obligations. This count is a specification inventory, not a count of executable tests already written or passed. A future parameterized test can exercise several obligations only when its evidence records each distinct assertion.

### 10.2 Shared rules inherited by every leaf

Every leaf obligation includes the common Result envelope: diagnostic/field key, exact scope, population references, state pairing, value kind, basis/check/witness references, material reasons and interpretation limit. The expected number alone cannot satisfy the test.

`H7` and `W7` references refer to the preserved sections 1-8 and lineage §§24-28. A derived test case is a separately named future fixture with a stated delta, not a modification of the frozen hero. Non-parser deltas must keep all required IDs, bindings, nullable fields and coverage declarations structurally consistent. Where a delta removes evidence, it must also disclose the resulting coverage limitation rather than secretly retaining false complete-history support.

Output-mutant tests start from a logically conforming report and alter only the named property. The test oracle must reject the mutant as nonconforming. This specifies validation of the implementation; it does not require a new user-facing report-validation command.

### 10.3 What is complete now and what remains gated

All currently registered analytical leaves receive four obligations. All existing input record/predicate/assessment contracts and report-envelope members receive parameterized obligations. Every PC01-PC24 prerequisite, current reason code and finding condition has an assigned exercise below.

Concrete filesystem permissions, numeric resource budgets, redaction policy, license terms, callable signatures, CLI spelling, canonical bytes and path layout remain their assigned WU9/WU10 decisions. Their absence is recorded as a future implementation gate, not filled by a test fixture. Test coverage over the current contract does not mean these later contracts are already complete.

No new analytical field, input key, enum, core reason code, graph view, detector, scoring model, dependency or implementation library is introduced.

## 11. Shared contract and integration test families

`SIT-VG001` through `SIT-VG026` are shared validation-family IDs. Their methods are project test operationalizations, not quotations from the source papers. They supplement the 57 leaf obligations and the existing W3/W4/W5/W6/W7 witnesses.

### SIT-VG001: Closed bundle and structural rejection

**Governing contract:** Lineage §§2, 13-14; reporting §§12.2, 16.8.

Parameterize valid local-file and in-process representations of the same accepted dossier. Reject invalid syntax/encoding, duplicate JSON keys, unknown contract, unknown core keys and missing required collections using the existing diagnostic codes. An invalid suffix after a valid prefix must produce diagnostics without analytical salvage. A valid sparse dossier is the paired control.

### SIT-VG002: Identity and reference discipline

**Governing contract:** Lineage §§2.2-2.3, 12; W7-11, W7-23-W7-24.

Exercise duplicate IDs across every collection, dangling IDs, wrong expected kinds, duplicate references in distinct-reference lists, case-sensitive identifiers and allowed punctuation. Pair each rejection with a valid explicit UnresolvedReference. Same work_key, event_key, locator, protected display name or identity assertion never authorizes silent merging. Predecessor remains informational.

### SIT-VG003: Every typed record field

**Governing contract:** Lineage §6, twelve record tables.

For each of the twelve record kinds, test every listed required field present and individually absent, each nullable factual field with/without the required Gap, each structural-null exception, every enum member, wrong primitive types, unknown core fields, and each allowed referenced endpoint kind. Exercise RoleBinding cardinality/types and all CorrectionEvent subtype branches. These are independently parameterized obligations, not one generic happy-path test.

### SIT-VG004: Every assertion and relation predicate

**Governing contract:** Lineage §§7-8, 10; W7-04, W7-11.

Instantiate every one of the 24 predicates on each permitted endpoint form, preserving direction and record-link provenance. Test a disallowed endpoint/type/detail, missing required dimension, wrong exact Claim version, denied polarity, inactive lifecycle and an actual contrary statement. Six Artifact transformation forms cannot leak into Claim-origin tracing. Candidate aliases such as corrects and observes_independently remain invalid core predicates.

### SIT-VG005: Every assessment kind and detail

**Governing contract:** Lineage §9, nine assessment kinds.

Parameterize each kind's required details, allowed subjects and native conclusions. Distinguish incomplete documentary support, which is ordinarily reportable, from malformed required structure. Exercise pairwise exactly-two versus setwise, all boundary roles, protected verification, classification axes, externality boundary, action grants, capacity strings and external conflict resolution. No assessment operates as a tool-authenticated truth flag.

### SIT-VG006: Time, lifecycle and immutable snapshot

**Governing contract:** Lineage §§3.1, 7, 10.7, 14; W6-26; W7-21.

Test known date, offset-bearing instant, fractional seconds and every explicit unknown/withheld/not_applicable TimeValue. Missing instant offset is invalid; a date stays a date. Well-formed but temporally inconsistent event sequences are accepted with the scoped limitation. Use grants clearly inside/outside their window and unknown effective history. Withdrawal/supersession needs its stated basis; no automatic newest-wins reducer.

**Gate:** Any previously unspecified exact endpoint convention must be resolved by its specification owner before a boundary-instant runtime assertion is frozen; no convention is invented here.

### SIT-VG007: Evidence basis and self-support

**Governing contract:** Lineage §§3.2, 4, 9; W7-18, W7-25.

Exercise all five basis_kind labels, five EvidenceReference kinds and four availability states with their legal combinations. A documentary label without supplied support remains a native label plus a qualification gap. Local/external locators are inert. A self-pointer or mutual assurance loop supplies no independent documentary support. A visible protected attestation and its withheld underlying record retain distinct scopes.

### SIT-VG008: Typed views and finite witnesses

**Governing contract:** Lineage §10 and §18.2; W7-04, W7-08, W7-13-W7-15.

Vary citation, material, each Claim-origin dimension, model/evaluation, organizational, stance, correction, pipeline, assurance and succession views without all-edge ancestry. Include a self-cycle, two-node cycle, diamond, cycle with an exit, disconnected components and parallel assertions. Verify finite ordered witnesses, one membership per counted record and no general DAG rejection. Positive witnesses can remain while complete ancestry is unresolved.

### SIT-VG009: Conflicts and localization

**Governing contract:** Definitions §§20.4, 22.2, 26.2; lineage §12; W7-19, W7-23.

Add an applicable weak denial to a documentary positive and retain both; no evidence-prestige winner. Add an unknown observation without contradiction and retain the positive classification. Change only an unrelated dimension: the unrelated established results survive. External resolution alone cannot delete source assertions; explicit lifecycle evidence controls their current use.

### SIT-VG010: Run envelope outcomes

**Governing contract:** Reporting §12.2, §16.8; W7-24, W7-27.

Exercise every listed report_kind/processing_state/input_validation pairing and reject every unlisted pairing in output conformance. Rejected/not-completed/failed diagnostic envelopes have empty analytical arrays; an interrupted accepted audit retains only independently finished cells. Never reuse values from a previous successful attempt as a failed run's ordinary audit.

### SIT-VG011: Atomic result states and values

**Governing contract:** Reporting §§12.3-12.5, 16.4-16.5.

Exercise all sixteen execution_state/result_state Cartesian combinations and accept only the six allowed pairings. Available requires a value of its actual kind; all other states require null and appropriate reasons. Native failed/verified/unknown input values remain inside attributed disclosures. Qualified count, raw inventory, point fraction and interval are separate Results.

### SIT-VG012: Explicit scope and population

**Governing contract:** Reporting §§16.2-16.3; H7-V01-H7-V03; W7-11, W7-16.

Parameterize every Scope and Population member. Keep exact Claim versions, graph views, dimensions, time bases, unit and member IDs. An empty claim list is not all claims; enumerated empty differs from unestablished. Case/target tuples, source seeds, comparison sets and pipeline cohorts cannot substitute for one another. Source selection changes preserve unaffected populations.

### SIT-VG013: Capability matrix and observability

**Governing contract:** Reporting §§14-16.7; W6-31-W6-32.

Each accepted inquiry lists all 15 families, with atomic result state-reference lists forming the prescribed partition. Five non-cumulative navigation entries link existing Results without cloning them. An available change and unavailable origin qualification coexist. Reject max_level, global green badge, omitted unavailable siblings and a capability marked completed with an unfinished requested cell.

### SIT-VG014: Checks, reasons and localization

**Governing contract:** Reporting §13; all PC01-PC24 and all reason codes.

Instantiate checks per result scope; test met, unmet, unknown and structurally not_applicable where each is meaningful. Reasons resolve to affected Results and supporting input; multiple blockers remain visible. A globally met coverage flag cannot qualify every field. The reason matrix in §14 supplies concrete branch obligations and dormant-code restrictions.

### SIT-VG015: Finding forms and threat limits

**Governing contract:** Reporting §18; threat §§4-6; W7-04, W7-25-W7-28.

Exercise every observation_kind and all 22 condition codes with the required finite witness, contrary inputs and interpretation limit. Test partial-history no-witness versus bounded absence under supported finite coverage. Invalid threat association fails output conformance. Several associations never create extra incidents; imported poisoning allegations never establish execution of a content detector.

### SIT-VG016: Exact numerical representation

**Governing contract:** Definitions §28.3; reporting §16.5; validation §6.2.

Preserve integer numerators, original positive denominators, members and buckets. Reject boolean counts, NaN, infinity, negative sentinels and invented 0/0. Parameterize optional decimal absent/present; half-up six-place rounding, including a positive value displayed as 0.000000, retains exact nonzero ratio. Intervals keep population and interval_kind; incidence may exceed one in sum.

**Gate:** Portable integer/resource limits and concrete serialization are WU9/WU10 gates; no fixed-width boundary is invented.

### SIT-VG017: JSON/Markdown substantive parity

**Governing contract:** Reporting §19.1; W6-31; W7-27.

Compare both formats against one logical oracle, including scope, source basis, reasons, unknown rows, exact numbers, native outcomes and release limits. Mutants delete an unavailable sibling, denominator, unknown member, contrary premise or attributed-source qualifier while preserving fluent text; each must fail. Authorized redacted derivatives remain separate artifacts with disclosed visibility limits.

**Gate:** Exact export/redaction permission policy belongs to WU9; no private-data permission is created by this test plan.

### SIT-VG018: Deterministic semantic transformations

**Governing contract:** Reporting §19.2; W6-30; W7-14, W7-27.

Reorder record/assertion/reference arrays and equivalent explicit sets, and rename snapshot-local IDs bijectively while preserving all references. Compare substantive outcomes after undoing the renaming, not identical digest/ID/time bytes. Preserve ordered path causality. Duplicate valid provenance assertions may add disclosures but cannot multiply record-membership counts. A scope-relevant conflict must still change its dependent outputs.

**Gate:** Canonical bytes, report-ID derivation and deterministic witness selection are WU10 choices.

### SIT-VG019: Inert source and extension content

**Governing contract:** Lineage §§3.4, 4.2; reporting §19.3; W7-26.

Place harmless instruction-shaped, HTML/Markdown-shaped, Unicode/control and namespaced-extension data in every applicable text-bearing field. Core rules and capability inventory remain unchanged; source text cannot create report headers, active images, fetches, code execution or suppression. Safe escaping remains reversible/traceable under the eventual disclosure policy, without claiming a detector.

**Gate:** Concrete output encoding, control-character handling and export policy require WU9 realization; current tests state the required separation.

### SIT-VG020: Offline operation and no intervention

**Governing contract:** Instructions §6; threat §§2-6; W7-26.

Future guarded integration runs observe no network access, local-locator opening, shell execution, telemetry, model call, source alteration, source contact, automatic quarantine or rollback. Preserve source bytes on success, rejection and interruption. Distinguish authorized report-destination writing from forbidden audited-system writes. A no-network import check alone cannot discharge runtime guards.

**Gate:** Exact filesystem/destination/symlink/overwrite behavior is WU9; no implementation or guard is created now.

### SIT-VG021: Protected data and safe diagnostics

**Governing contract:** Reporting §§16.6, 16.8, 19.3; W7-18.

Use fictional protected identifiers and synthetic canaries, never real sensitive data. Preserve known opaque commonality, restrict witness/export content to the adopted policy, and check errors/logs for forbidden data/paths. A redaction cannot generate new independent roots or certify public inspectability. Confirm ordinary diagnostic fields do not dump untrusted payloads.

**Gate:** WU9 must specify permissions, retention, topology disclosure, paths, logs and exact canary surfaces before concrete tests can pass.

### SIT-VG022: Resource limits, cancellation and fault containment

**Governing contract:** Reporting §§12.2-12.4, 16.8; SIT-TS005; W6-27.

After resource policy adoption, test just below, at and above each bound and each allowed cancellation point. Vary long chains, branching, repeated paths, cycles, dense overlap and large supplied excerpts without arbitrary hardware targets. Finish-independent cells may survive accepted-input interruption; unfinished work is not_evaluated. Failures before validation acceptance never emit analytical salvage.

**Gate:** WU9 owns numeric budgets and boundary behavior; WU10 owns execution strategy. Performance acceptance cannot pass while these are unset.

### SIT-VG023: File/in-process surface and diagnostic equivalence

**Governing contract:** Lineage §2; reporting §16.8; SIT-D016-SIT-D018.

An equivalent accepted logical object and authorized local file must have matching substantive semantics; only file input gets a digest of bytes actually read. Unknown IDs before failed parsing remain null with qualifications. Future CLI/Python entry points must exercise the same contract, safe errors and all required capabilities.

**Gate:** WU10 owns signatures/CLI syntax and object canonicalization; WU9 owns filesystem details. No public command or API function is selected here.

### SIT-VG024: Golden oracle and regression ownership

**Governing contract:** Validation §§1-8; instructions §§5-8.

Lock H7-01, three variants and W7-01-W7-28 as named prose inputs/oracles. Later fixture promotion materializes required fields and valid defaults without inventing evidence. An implementation cannot regenerate its own expected values to remove failures. A changed oracle requires premise, owner, affected field/Trace and approval evidence, preserving the original fixture.

### SIT-VG025: Independent challenge to product conventions

**Governing contract:** EC §§2, 6-7 through SIT-T019-SIT-T025; W7-28.

Separate code defects, specification ambiguity, dishonest input and a structurally inadequate product cut. Preserve externally supplied counterexamples that current categories cannot express, without auto-fitting or reclassifying them. Field conformance does not verify the source theories; coherent forged input is an explicit residual failure case, not a test-suite pass for source truth.

### SIT-VG026: Release and theory boundary assertions

**Governing contract:** Product §10; map §6; SIT-P015-SIT-P016.

Reject unregistered global source counts, universal truth/integrity/safety scores, effective independent samples, inferred mutual information/entropy/capture probabilities, active detector claims and automatic intervention. Registered policy/verification labels remain attributed. Source return, full source governance and other toolkit internals stay outside release. Trace citations do not create empirical validation.

## 12. Complete registered analytical-leaf matrix

All field names in this section are copied from reporting §17. Each table cell is mandatory for its stated obligation; common envelopes and evidence rules in §10.2 apply. Exact output states use reporting §12.3. A provided native field such as `unknown`, `failed` or `verified` remains inside its attributed disclosure.

Where an optional completion interval or decimal is emitted, its full contract must be tested. An optional display cannot justify omitting the required point-result non-result, unresolved rows, exact rational value, scope or reasons. The future release must exercise the registered optional representation it chooses to expose.

### 12.1 M001: SIT-TR003

| Field obligation ID / existing field | Positive (-P) | Negative (-N) | Missing data (-M) | Boundary (-B) |
|---|---|---|---|---|
| `SIT-VF001`<br>`nominal_seed_artifact_record_count` | H7-01: 6, with A(I1) exactly A-F; support files, ancestors and after-versions are excluded. | Output mutant: use the dossier-wide Artifact inventory or count five visible domains as five independent observations; reject the mutant. | Valid artifact-only Inquiry with no artifact seeds: available 0 for its explicit empty inventory, never zero real-world sources. | W7-11/W7-16: one Artifact used by several claim contributions counts once in the inquiry union; keep its claim-level roles separate. |
| `SIT-VF002`<br>`unresolved_seed_artifact_reference_count` | Derived sparse case: one explicit unresolved Artifact seed reference gives 1; its expected kind does not instantiate an Artifact. | Output mutant: H7-V02 gives 1 because an upstream EvidenceItem is unknown; reject, since the required value is 0. | No unresolved Artifact seed positions in H7-01: available 0, even if some unrelated model ancestry is partial. | Two contribution links to the same unresolved Artifact ID retain one distinct unresolved artifact-reference position in the seed inventory, without inventing its identity. |
| `SIT-VF003`<br>`seed_evidence_item_count` | H7-01: 6, with the six exact Claim-bound seed EvidenceItem IDs. | Output mutant: add the non-seed ER1, a support Artifact, or a second path as a seed; reject. | Valid Inquiry with empty seed_evidence_refs: available 0 for the selected Claim; associated origin ratios have no seed denominator. | W7-16: three explicitly separate contributions from two Artifacts give 3; no semantic deduplication. |
| `SIT-VF004`<br>`claim_artifact_record_count` | H7-01/C1: 6 resolved Artifact versions linked to its seed contributions. | Output mutant: collapse two supplied Artifact versions sharing a locator into one without authorization; reject. | A selected contribution can have a typed unresolved Artifact: do not count the placeholder as a resolved Artifact; disclose the unresolved position. | W7-11: A participates in two Claim-specific populations while appearing once in the inquiry union; verify each exact member set. |
| `SIT-VF005`<br>`claim_unassigned_seed_artifact_record_count` | Derived artifact-only case: two resolved seed Artifacts lacking any seed EvidenceItem binding in Inquiry I give 2, using Definitions §21.1. | Output mutant: H7-01 reports all non-seed support files as unassigned seeds; reject; expected 0. | No seed Artifacts in a valid sparse Inquiry: available 0 in the empty seed inventory, without inferring absent outside evidence. | W7-11: an Artifact assigned by a seed EvidenceItem to either targeted Claim is assigned within I. Do not label it unassigned merely because the other Claim has no corresponding contribution. |

### 12.2 M002: SIT-TR004

| Field obligation ID / existing field | Positive (-P) | Negative (-N) | Missing data (-M) | Boundary (-B) |
|---|---|---|---|---|
| `SIT-VF006`<br>`reached_origin_record_count` | H7-01/acquisition: 2, exact set O1/O2, with completed finite witnesses. | Output mutant: count a parentless EvidenceItem or unresolved expected OriginEvent as a reached OriginEvent; reject. | W7-03: completed supplied trace reaches 0 OriginEvent records; retain one represented frontier and no statement of zero actual origins. | W7-14: converging paths to O1 count it once; W7-04 with an exit keeps the reached O1 despite cyclic unresolved ancestry. |
| `SIT-VF007`<br>`documentary_origin_boundary_record_count` | H7-01: 2 documentary-qualified origin boundaries, with OB1/OB2 and their scoped support. | Input delta: remove inspectable support for both origin boundaries while retaining their documented_origin labels; the examined qualifying-origin count becomes 0, not 2. | W7-25: a completed examined view with no qualifying boundary can give available 0 under Definitions §21.2, with basis gaps. The absent stronger real-origin/independence claim is never inferred from that zero. | W7-17/W7-18: distinguish documentary, declared, baseline, scope-cut and protected-attestation boundaries; no automatic upgrade from a boundary label. |
| `SIT-VF008`<br>`origin_boundary_disclosures` | H7-01: OB1/OB2, their subjects, roles, dimensions, coverage, evidence and qualifications remain attributable. | Output mutant: rename a reference_baseline or declared_origin to documented_origin; reject. | No applicable boundary assessments: show the explicit empty supplied inventory or missing-subject disclosure at its scope; do not invent a root. | Applicable same-dimension upstream parents remain visible beside a termination claim; a deliberate scope cut never hides a known parent. |

### 12.3 M003: SIT-TR005

| Field obligation ID / existing field | Positive (-P) | Negative (-N) | Missing data (-M) | Boundary (-B) |
|---|---|---|---|---|
| `SIT-VF009`<br>`submitted_comparison_member_count` | H7-IND12: 2; W7-01 setwise comparison: 3, each under its own assessment ID. | Output mutant: W7-12 sums two pairs to 4 or replaces them with one three-member comparison; reject. | No comparison assessment: completed/unavailable with missing_comparison_assessment for the requested count, not a zero global total. | A submitted, structurally valid three-member assessment can have size 3 while documentary qualification is unavailable; these are separate Results. |
| `SIT-VF010`<br>`qualified_process_set_member_count` | H7-IND12: 2 in acquisition with four unexamined dimensions retained. | Input delta: add a relevant denied dependency or reduce process support to a self-declaration; the qualified count must become unavailable while the assessment survives. | Remove the applicable assessment completely: missing_comparison_assessment; remove only inspectable basis: support_uninspectable or documentary_basis_incomplete as justified. | W7-06 qualifies an analytical-method pair of Evaluations; W7-12 never promotes pairwise qualifications to a jointly qualified set. |
| `SIT-VF011`<br>`qualified_origin_set_member_count` | H7-IND12: 2 only because both specified subjects are documentary OriginEvent boundaries in the same Claim/dimension. | Output mutant: use a qualified pair of Models or Evaluations as two independent origins; reject. | Missing comparison or incomplete required boundary qualification leaves the requested qualified count unavailable with its actual blockers. | W7-06: Evaluation subjects make this origin-specific count completed/not_applicable with no_applicable_subject, while the process-member count can remain 2. |
| `SIT-VF012`<br>`independence_assessment_disclosures` | H7-IND12: preserve comparison_form, exact subjects, native conclusion, examined relations, unexamined dimensions, assessor, method and support. | Output mutant: replace supplied independent_process with a tool-authenticated fact or erase a relevant contrary assessment; reject. | Absent comparison is disclosed as absent from the supplied set; no synthetic singleton assessment or affirmative independence is created. | Retain multiple conflicting, pairwise and setwise records separately; neither source prestige nor array order selects a winner. |

### 12.4 M004: SIT-TR006

| Field obligation ID / existing field | Positive (-P) | Negative (-N) | Missing data (-M) | Boundary (-B) |
|---|---|---|---|---|
| `SIT-VF013`<br>`per_seed_origin_memberships` | H7-01: EA-EE each map to {O1}, EF to {O2}; all six rows preserve their finite witnesses. | Output mutant: infer an acquisition parent from only Artifact citations, publisher ownership or generated_by; reject. | H7-V02 keeps EU and its unresolved branch in the seven-row population while the six known rows survive. | W7-14's diamond yields {O1}; W7-13's two genuine parent origins yield {O1,O2}; path multiplicity and origin multiplicity differ. |
| `SIT-VF014`<br>`origin_incidence_counts` | H7-01: O1 has seed members EA-EE and c_r=5, O2 has EF and c_r=1, with N=6. | Output mutant: normalize H7-V03's counts 6 and 2 into weights summing to one; reject. | H7-V02: counts 5 and 1 stay tied to N=7 with the unresolved row visible; no known-only denominator 6. | H7-V03: fractions 6/7 and 2/7 are permitted to sum to 8/7; nonexclusive=true and distinct per-origin seed memberships are mandatory. |
| `SIT-VF015`<br>`seed_origin_dispositions` | H7-01: counts (unresolved,baseline/scope,declared,multi,single)=(0,0,0,0,6), with exact row memberships. | Output mutant: a seed containing a known origin plus an unknown or disputed branch is assigned single_documented_origin; reject. | H7-V02: (1,0,0,0,6); unknown evidence remains in N rather than being omitted. | W7-17 exercises declared/baseline/scope precedence; H7-V03 has (0,0,0,1,6); every seed occupies exactly one governing category. |
| `SIT-VF016`<br>`documentary_origin_resolution_fraction` | H7-01: 6/6; the numerator counts seeds whose ancestry is documentary-resolved, including fully known multi-origin seeds. | Output mutant: H7-V02 reports 6/6 after dropping EU, or H7-V03 treats multiple known origins as unresolved; reject. | H7-V02: 6/7; missing ancestry is counted in the full known population. With no seed population, null with no_seed_contributions/zero_denominator as applicable. | H7-V03: 7/7 may coexist with unavailable HHI. W7-03: exact 0/2 describes documentary resolution, not zero real origins. |

### 12.5 M005: SIT-TR007

| Field obligation ID / existing field | Positive (-P) | Negative (-N) | Missing data (-M) | Boundary (-B) |
|---|---|---|---|---|
| `SIT-VF017`<br>`single_origin_contribution_hhi` | H7-01: numerator 26, denominator 36, buckets (5,1), N=6; optional decimal 0.722222. | Output mutant: H7-V03 assigns each parent one-half; H7-V02 falls back to 26/36; both violate the full-population gate. | H7-V02: null with unknown_endpoint and upstream_coverage_incomplete. H7-V03: null with multi_origin_unallocated; retain the corresponding full profile. | H7-V01 gives 25/25; W7-01 gives 3/9; N=0 gives no ratio. Qualification does not require bucket independence or agreement, and no score band is added. |

### 12.6 M006: SIT-TR008

| Field obligation ID / existing field | Positive (-P) | Negative (-N) | Missing data (-M) | Boundary (-B) |
|---|---|---|---|---|
| `SIT-VF018`<br>`immediate_evidence_layer_dispositions` | H7-01: inherited/direct/mixed/unresolved counts (5,1,0,0). | Output mutant: H7-V03's inherited E-to-E parents are classified mixed merely because they reach two roots; reject. | H7-V02: (5,1,0,1). In W7-15 the immediate known copy remains inherited-only despite an unknown distant ancestor. | Derived valid seed with both a direct E-to-OriginEvent edge and an inherited E-to-E link is mixed_direct_and_inherited; a diamond with only E parents stays inherited-only. |
| `SIT-VF019`<br>`inherited_only_seed_fraction` | H7-01: 5/6; H7-V03: 6/7, reflecting the immediate EvidenceItem layer. | Output mutant: count every path or use a text-similarity novelty score as the numerator; reject. | H7-V02: null point fraction because one immediate classification is unresolved; do not use 5/6 or select an interval endpoint. | W7-15: 1/1 despite distant unknown ancestry. For N=0, neither 0/0 nor 100% is allowed. |
| `SIT-VF020`<br>`inherited_only_completion_interval` | H7-V02: available [5/7,6/7], interval_kind finite_record_completion; retain D/O/M/U and N. | Output mutant: label the interval a confidence interval, replace N with resolved members, or collapse it into a point; reject. | W7-03: [0/2,2/2] is permitted with known N and unknown classifications. If N is absent/empty, no endpoints may be fabricated. | H7-01 with U=0: completed/not_applicable and completion_interval_not_needed. The test checks the optional interval when emitted; omission cannot erase the point's required unknowns. |

### 12.7 M007: SIT-TR009

| Field obligation ID / existing field | Positive (-P) | Negative (-N) | Missing data (-M) | Boundary (-B) |
|---|---|---|---|---|
| `SIT-VF021`<br>`unresolved_frontier_reference_count` | W7-03: one represented UX shared by two seeds gives 1. | Output mutant: report two unknown roots because two seeds reach UX; reject. | H7-01 acquisition: available 0 for the completed frontier inventory, with no claim that other dimensions have no gaps. | A typed unresolved OriginEvent remains one frontier reference regardless of how many unobserved ancestors it might conceal. |
| `SIT-VF022`<br>`unqualified_terminal_record_count` | Derived complete finite trace ends at one resolved OriginEvent lacking an origin-boundary assessment: count that represented unqualified terminal once. | Output mutant: treat the terminal as a documentary root because it has no recorded parent; reject. | No qualified boundary evidence leaves the terminal visible and its stronger qualification unavailable; do not manufacture a hidden-origin count. | A shared unqualified terminal reached by two seeds is one terminal with two affected seeds; cycle exits and explicit scope cuts retain their different meanings. |
| `SIT-VF023`<br>`seed_items_with_unresolved_ancestry_count` | H7-V02: one affected seed EU; W7-03: two affected seeds through the same UX. | Output mutant: copy frontier count into affected-seed count; W7-03 must distinguish 1 from 2. | All selected ancestry unknown: count the explicit affected seeds if the required scope was fully processed; unfinished traversal is not_evaluated. | W7-15 has one unresolved seed even when its immediate-inheritance fraction is 1/1; no dossier-wide metric suppression. |
| `SIT-VF024`<br>`ancestry_gap_disclosures` | H7-V02 preserves UX/EU, reason, branch witness, expected kind, coverage and affected scope. | Output mutant: replace withheld identity with several apparently independent pseudonyms or erase the gap to complete a trace; reject. | Gap-only sparse input stays valid; an external locator remains inert and uninspected rather than filling ancestry. | W7-18 preserves known shared opaque references and attestation limits. No global upper bound on concealed roots is produced. |

### 12.8 M008: SIT-TR010

| Field obligation ID / existing field | Positive (-P) | Negative (-N) | Missing data (-M) | Boundary (-B) |
|---|---|---|---|---|
| `SIT-VF025`<br>`shared_recorded_ancestor_count` | H7-EVAL generator/judge: 2 strict common ancestors, exactly MBASE and TRAINING, with partial further history. | Input delta: remove the ancestor edges but keep family labels; count becomes 0 in the completed examined graph, not 1 from the label. | Missing role bindings or an unresolved role subject leave the corresponding stronger comparison unavailable with roles_incomplete/unknown_endpoint; partial further history preserves positive witnesses. | W7-05: 1 strict ancestor. Shared exact role object, one-sided ancestry and shared dataset with differing subset descriptors remain separate disclosures. |
| `SIT-VF026`<br>`matching_family_label_count` | H7-EVAL: exact common family string H7-family gives 1. | Input delta: use distinct exact family strings, including a case difference; no fuzzy or provider-based match is permitted. | One family_label unknown: retain its Gap; no label inferred from model_key or provider. Any zero-match inventory remains explicitly limited to inspected supplied labels. | Several bindings carrying the same exact string do not multiply distinct label matches; a match is never converted into model ancestry or process independence. |
| `SIT-VF027`<br>`evaluator_overlap_disclosures` | H7-EVAL identifies the actual role pair, bound objects, partial history and dataset-level granularity. | Output mutant: count a common reviewed target as automatically shared review-process ancestry; reject using W7-06. | Missing rubric/training exposure remains unknown beside an independently evidenced procedure comparison; no all-dimensional independence claim. | Same actor in several roles, related Models and shared reference/rubric Artifacts remain distinct types of commonality, with no vote count. |
| `SIT-VF028`<br>`evaluator_overlap_witnesses` | H7-EVAL links the MBASE witness through ML01/ML02 and the TRAINING witness through ML03/ML04. | Output mutant: fabricate an ancestor path from matching prose or a family label; reject. | No eligible positive path in completed partial history gives only a scoped no-witness result; no universal absence or independence. | Finite cycle/diamond witnesses retain ordered edges; an interrupted search cannot be emitted as an empty completed witness set. |

### 12.9 M009: SIT-TR011

| Field obligation ID / existing field | Positive (-P) | Negative (-N) | Missing data (-M) | Boundary (-B) |
|---|---|---|---|---|
| `SIT-VF029`<br>`externality_assessment_disclosures` | H7-EXT-F and H7-INT-A retain their different native conclusions, subjects, boundary I1, relevant time, grounding and support. | Output mutant: classify a recent human-authored or remote-URL Artifact as external without a matching assessment; reject. | Absent assessment/grounding: requested qualified externality is unavailable with externality_unestablished; recorded metadata can still be inventoried. | W7-10's selection-negative control preserves externality even when use did_not_occur; no scalar Presence or adequate-renewal claim. |
| `SIT-VF030`<br>`externality_stage_links` | H7-EXT-F links to EF's own admission, preservation, selection and influence records with their native states. | Output mutant: join stage records by similar prose, shared publisher or date rather than actual subject identity/mapping; reject. | Externality supplied without stage records: preserve the assessment and disclose missing links; never infer admission or influence. | W7-10 control preserves external admission and explicit non-selection/non-use. A use record alone cannot supply the other three stages. |

### 12.10 M010: SIT-TR012

| Field obligation ID / existing field | Positive (-P) | Negative (-N) | Missing data (-M) | Boundary (-B) |
|---|---|---|---|---|
| `SIT-VF031`<br>`pipeline_stage_disclosures` | H7-01 preserves all four exact stage keys and each PipelineRecord's state, subject, output, linkage kind and observed time. | Input delta: give repeated attempts different stage_key values; they remain separate, with no newest-wins reducer. | Missing stages remain missing; an evidenced influence record can be disclosed without fabricated admission/preservation. | W7-19 retains duplicate unknown and contradictory source rows; their counting effect differs from retaining the original records. |
| `SIT-VF032`<br>`stage_member_partition` | H7 answer-use-1: Y/F/U = 3/2/1, T=6, exact member sets EA/EB/ED, EC/EF, EE. | Output mutant: remove EE or count duplicate logs as extra cohort members; reject. | W7-19: 3/1/1 on T=5; a missing member observation is U. An unestablished cohort gives no invented T=0 partition. | Adding unknown beside a supported positive does not alone change Y; adding applicable contrary evidence yields U. Always Y+F+U=T. |
| `SIT-VF033`<br>`stage_occurrence_fraction` | H7 select-1: 5/6, with U=0 and its own anchored six-member cohort. | Output mutant: main influence reports 3/5 after omitting unknown EE; reject. | H7 influence with U=1: completed/unavailable, stage_classification_unresolved. Missing/ambiguous cohort anchors withhold the fraction independently of individual logs. | A known empty population gives zero inventory but no ratio. An eligible all-negative nonempty cohort can give 0/T. |
| `SIT-VF034`<br>`stage_occurrence_completion_interval` | H7 influence: [3/6,4/6], finite_cohort_completion; W7-19: [3/5,4/5]. | Output mutant: call an endpoint a measured use rate, or use a denominator excluding unknowns; reject. | Without a valid explicit cohort, no interval is available. Missing member classifications within a known cohort stay in U. | U=0 makes this completed/not_applicable with completion_interval_not_needed; an emitted optional interval must use the same population as the point field. |
| `SIT-VF035`<br>`cohort_transition_disclosures` | H7 intake-1 to store-1 and intake-1 to select-1 disclose distinct valid pairs with identical member IDs and fully evidenced admission. | Input delta: keep target logs but add a competing admission baseline; transition becomes unestablished while standalone stage results survive. | No admission cohort: target stage disclosures remain, but transition_baseline_unestablished prohibits inventing retention. | No admission-to-influence transition is created. Changed output-version IDs may be disclosed but cannot silently replace the counted subject cohort. |
| `SIT-VF036`<br>`cohort_transition_fraction` | H7 intake-1 to select-1: 5/6 under the unique compatible evidenced baseline. | Input delta: one baseline member lacks positive admission, or target cohort changes membership; transition withheld without suppressing standalone target fraction. | No compatible baseline/target pair: null with transition_baseline_unestablished and other actual cohort blockers. | Derived W7-19 target linked to a valid fully admitted same-member baseline has unresolved transition point; target U=0 permits its exact fraction. |
| `SIT-VF037`<br>`cohort_transition_completion_interval` | Derived W7-19: add only a unique qualified all-admitted baseline with the same five members; target U=1 permits [3/5,4/5]. | Output mutant: copy a target interval into a transition whose baseline is ambiguous or has different members; reject. | No qualifying baseline: no endpoints; individual target stage interval can remain available at its own scope. | H7 exact eligible transitions: completed/not_applicable with completion_interval_not_needed. Influence remains outside this restricted transition's subject. |

### 12.11 M011: SIT-TR013

| Field obligation ID / existing field | Positive (-P) | Negative (-N) | Missing data (-M) | Boundary (-B) |
|---|---|---|---|---|
| `SIT-VF038`<br>`declared_correction_route_witnesses` | H7-CHANNEL yields four separate target/amend tuples through one channel, using canonical target links. | Output mutant: turn four target tuples or several walks through a routing cycle into four independent channels; reject. | No eligible route in partial supplied history gives only route_not_recorded/bounded no-witness meaning; no global impossibility. | Derived two-leg propagates_to chain must match target/action/time per leg; finite route witnesses survive cycles without enumerating infinite walks. |
| `SIT-VF039`<br>`applicable_authorized_route_witnesses` | H7's four amend tuples qualify under H7-AUTH's stated target/window and supplied grant basis. | Input delta: in a two-leg route remove or change the grant on one required leg; declared route survives, stronger authorized witness does not. | W7-21: absent/unknown authority yields authority_unestablished; review-only grant yields authority_inapplicable for amend. | A1's grant never automatically applies to A2. Date-only/unknown times limit time-specific qualification; separately documented historical change remains visible. |
| `SIT-VF040`<br>`correction_route_disclosures` | Keep channel, target, action, declared path, grant scope and actual time/coverage limits together. | Output mutant: a contact mailbox or owner identity is presented as institutional authority or an observed correction; reject. | W7-09 with declared channel but incomplete grants retains the declaration and its unknown applicability. | Explicitly denied, expired or unknown grant values remain attributed; no newest-wins or prestige-based route adjudication. |

### 12.12 M012: SIT-TR014

| Field obligation ID / existing field | Positive (-P) | Negative (-N) | Missing data (-M) | Boundary (-B) |
|---|---|---|---|---|
| `SIT-VF041`<br>`correction_case_record_count` | H7-01: 1 submission CASE1. | Output mutant: sum submission, handling and change events as five cases; reject. | Explicit empty supplied case inventory gives available 0 in that scope; no zero real corrective capacity conclusion. | One submission with several handling outcomes remains one case; separate submissions targeting the same Artifact remain separate cases. |
| `SIT-VF042`<br>`handling_event_record_count` | H7-01: 1 HAND1; W7-22: 2 handling-event IDs. | Output mutant: collapse accepted and failed records into a single latest-state event or count their categories as cases; reject. | No handling event for a submitted case: exact 0 records, without inferring neglect or failure. | Repeat outcome values with distinct event IDs remain distinct records; exact duplicate IDs are input errors handled before analysis. |
| `SIT-VF043`<br>`linked_change_event_record_count` | H7-01: 3 change-event IDs linked to CASE1. | Output mutant: count an accepted request or an unrelated later Artifact version as a linked change event; reject. | No change events: 0 supplied events; a requested documentary effect is separately unavailable with change_evidence_missing. | W7-22: two event IDs for one before-target give 2 events even when only one distinct documentary target qualifies. |
| `SIT-VF044`<br>`documentary_linked_change_target_count` | H7-01: 3 distinct (CASE1,before_ref) pairs, including the root export and A/D. | Output mutant: W7-22 counts two events for the same pair as two documentary targets; reject. | An unresolved before/after or unsupported linkage remains an event inventory but does not enter this qualified-target set; disclose before_after_unresolved or basis gap. | Supported removal with after_ref null and explicit absence reason may qualify; unknown after-state cannot. Distinct cases on one target remain distinct case/target pairs. |
| `SIT-VF045`<br>`cases_with_documentary_linked_change_count` | H7-01: 1 case having at least one qualified linked target. | Output mutant: report 3 because CASE1 has three changed targets; reject. | Submission/handling without documentary change: exact 0 qualifying cases in the finite inventory, without turning the accepted request into a failed correction. | Several changed targets in one case count once; two cases with supported changes to one target count twice. |
| `SIT-VF046`<br>`correction_case_disclosures` | H7 CASE1/HAND1 preserves proposed correction and native accepted outcome with provenance. | Output mutant: W7-22 replaces native failed with runtime failure or deletes the earlier accepted record; reject. | W7-09 preserves missing change evidence and, in its negative-observation variant, the separate attributed review observation. | Reasoned rejection shows handling without proving the objection false. No newest-wins final status or correction_success_rate is introduced. |
| `SIT-VF047`<br>`correction_target_change_disclosures` | H7: R1-V1/A/D have supported before/after linkage; E is explicitly undocumented in the selected target set. | Output mutant: classify E as failed or silently add B/C to the selected correction denominator; reject. | Target without documentary linkage: requested effect unavailable with change_evidence_missing, while zero supplied event inventory remains distinct. | W7-21's known change survives missing route authority. A supported retraction and an unresolved after-version produce different disclosures. |
| `SIT-VF048`<br>`reported_capacity_disclosures` | Derived capacity assessment preserves its supplied strings, unit, horizon, load, assessor and limitations exactly. | Output mutant: parse '10 cases/day' into a utilization/adequacy score or infer capacity from three changes; reject. | H7 has no capacity assessment: disclose empty supplied inventory and no estimate; do not report zero capacity. | Withheld/null string with required Gap remains unknown. Incompatible horizons/units remain separate reported assessments with no numerical normalization. |

### 12.13 M013: SIT-TR015

| Field obligation ID / existing field | Positive (-P) | Negative (-N) | Missing data (-M) | Boundary (-B) |
|---|---|---|---|---|
| `SIT-VF049`<br>`corrective_independence_disclosures` | W7-06 preserves the qualified analytical-method comparison of V1/V2 with training/rubric dimensions explicitly unexamined. | Output mutant: a human title, different employer, or separate model endpoint becomes independent corrective capacity; reject. | H7 HREVIEW lacks the relevant comparison: missing_comparison_assessment; its substantive human contribution remains separately available. | Known shared reviewed object may coexist with different method procedures; an unresolved relevant dependency blocks only the affected qualification. |
| `SIT-VF050`<br>`human_contribution_disclosures` | H7-HREVIEW includes the actual recorded human reasoning/contribution, reviewer role, method/result and CORR basis. | Output mutant: a software_agent or organization alone is treated as the human_reviewer role; structurally invalid bindings must be rejected. | Human role with review_contribution null and a valid Gap remains valid but does not become substantive documented contribution. | Protected human reference can retain inspectable attestation and contribution limits. One recorded review never proves a renewable judgment stream. |

### 12.14 M014: SIT-TR016

| Field obligation ID / existing field | Positive (-P) | Negative (-N) | Missing data (-M) | Boundary (-B) |
|---|---|---|---|---|
| `SIT-VF051`<br>`anomaly_context_disclosures` | H7-AN1 retains original timing concern, unclassified state and null Claim binding. | Output mutant: force AN1 into C1, erase original context or assign rarity/ideology from prose; reject. | Protected context with valid reference/Gap stays admissible; withheld content limits disclosure rather than being reconstructed. | A caller_classified anomaly retains its caller label; it cannot change the canonical taxonomy or become a truth verdict. |
| `SIT-VF052`<br>`contestation_disclosures` | H7-EF's contradiction of C1 is preserved beside its separate acquisition evidence and all other seed stances. | Output mutant: remove EF from the six-source population or lower its integrity because it disagrees; reject. | No stance records in a named finite set gives no supplied contestation; it cannot establish agreement, consensus or no outside contradiction. | W7-07 factual disagreement alone does not dispute acquisition; explicit competing provenance assertions retain their separate scope. |
| `SIT-VF053`<br>`tail_stage_result_links` | Link the actual eligible M010 results for the stated tail/anomaly cohort; H7 EF's exclusion is not relabeled as whole-anomaly retention. | Output mutant: duplicate M010 numerators as an independent second metric, or use final-only records to infer suppression; reject. | W7-20 lacks an intake cohort: retain context but no retention fraction; explain cohort_anchor_missing/cohort_universe_unestablished. | An explicitly supplied Anomaly cohort can use M010's rules; altered source seeds do not alter its independently anchored membership. |

### 12.15 M015: SIT-TR017

| Field obligation ID / existing field | Positive (-P) | Negative (-N) | Missing data (-M) | Boundary (-B) |
|---|---|---|---|---|
| `SIT-VF054`<br>`coverage_disclosures` | H7: all eight coverage assessments, including partial model history, retain kind, subjects, predicates, dimensions, members, omissions and basis. | Output mutant: apply complete acquisition coverage as complete model/correction history; reject. | Missing coverage remains unknown for dependent exhaustive results; preserve positive scoped witnesses without inventing completeness. | A complete_for_scope label contradicted by an unknown branch remains attributed with its inconsistency; it does not delete the branch. |
| `SIT-VF055`<br>`documentary_basis_gap_disclosures` | W7-25 identifies uninspectable locator-only support or self-supporting assurance separately from the original documented_record label. | Output mutant: replace the native basis label or silently fetch a URL to fill the gap; reject. | Missing asserter/method/support triggers the corresponding qualification gaps, rather than provenance rejection if explicit nullable/Gaps satisfy input rules. | Protected visible attestation and withheld underlying material have different availability; a pointer loop cannot authenticate itself. |
| `SIT-VF056`<br>`declared_basis_inventory` | H7's named L01-L07 population: seven documented_record labels, zero other categories. | Output mutant: inventory only documentary-qualified assertions while claiming to count declared basis, or upgrade upstream_inference to direct observation; reject. | A valid explicit empty selected assertion population has all zero category counts, not an absent-history percentage. | Exercise all five basis_kind values; counts sum to the named record population while qualification outcomes may differ. |
| `SIT-VF057`<br>`reference_availability_inventory` | H7's selected eight SUP references: supplied=8 and other availability categories=0. | Output mutant: locator_only or withheld content becomes supplied because a URL/artifact pointer exists; reject. | An explicit empty reference population yields zero inventories; absent inspectable content for a required claim remains a separate gap. | Exercise supplied/locator_only/withheld/unavailable, preserving protected attestation's visible summary versus hidden underlying reference as separate records. |

## 13. Parameterized coverage beyond the fifty-seven leaves

### 13.1 Input field and registry coverage

The following table is an expansion rule, not a replacement schema. For each field explicitly listed in the cited owner section, future tests must enumerate presence, allowed type/enum, null/empty meaning, required evidence/reference rule and invalid alternatives. An optional field is tested absent and present. A required nullable field is tested with its permitted Gap; a structurally null field is tested without inventing a factual missingness claim.

A missing support excerpt ordinarily limits documentary qualification. It must not become a schema rejection when the supplied record's null/Gap and reference structures are valid. The inverse error is also prohibited: a dangling ID or missing required core key cannot be reclassified as harmless incomplete provenance.
| Input contract surface | Exact owner | Validation families | Required expansion |
|---|---|---|---|
| Bundle envelope | Lineage §2 | SIT-VG001, SIT-VG002 | Every top-level key; required arrays; at least one Inquiry; exact contract; inert extensions; predecessor never imports data. |
| TimeValue, TimeWindow, Provenance, Gap, extensions | Lineage §3 | SIT-VG002, SIT-VG006, SIT-VG007, SIT-VG019 | Every shared member and allowed state; attribution versus self-proof; date precision; namespace keys; null/Gaps and structural exceptions. |
| EvidenceReference | Lineage §4 | SIT-VG007, SIT-VG019, SIT-VG021 | All 5 kinds, 4 availability values, required protected-attestor/supplied-excerpt rules, and every field/reference. |
| Inquiry | Lineage §5 | SIT-VG002, SIT-VG006, SIT-VG012 | All fields including boundary's description/criterion/system_refs; seeds, dimensions, Claim bindings and exact relevant cutoff. |
| All 12 typed record kinds | Lineage §§6.1-6.12 | SIT-VG003 | Every data-table row plus id/kind/data/provenance, optional common members, 9 RoleBinding role values and all 3 CorrectionEvent subtypes. |
| Assertion envelope | Lineage §7 | SIT-VG004, SIT-VG006, SIT-VG009 | Relation/assessment forms; exact scope; lifecycle evidence; assertion time distinct from occurrence. |
| All 24 relation predicates | Lineage §8 | SIT-VG004, SIT-VG008 | Every endpoint form, dimension/polarity, details field, same-kind/same-Claim restriction, self-reference exception and forbidden candidate alias. |
| All 9 assessment kinds | Lineage §9 | SIT-VG005, SIT-VG007, SIT-VG009 | Every required detail, subject cardinality, conclusion and native classification axis; no hidden score. |
| View names and input-to-output bridge | Lineage §§10-12,18-21 | SIT-VG008, SIT-VG009, SIT-VG011 | Named typed projections, record links, time/identity/conflict limits and preserved native input states. |

A registry-sweep manifest in the later executable tests must list the actual current field/enum entries instantiated. A new field or enum in an approved future schema changes that manifest and requires its own tests. A single successful H7 parse cannot discharge this sweep. Text that appears only as explanatory prose is not turned into an executable field by the sweep.

### 13.2 Report-envelope and nested-member coverage

These members are the existing logical report contract, not additional leaf metrics. The listed fields are tested individually through their associated family. For descriptive structures whose exact byte serialization is explicitly deferred, test the required meaning now and retain the WU10 realization gate.
| Report surface | Individually covered members / obligations | Owner | Families |
|---|---|---|---|
| Root | `contract_version`, `report_kind`, `report_id`, `run`, `input_identity`, `input_validation`, `scopes`, `populations`, `basis_index`, `capabilities`, `checks`, `observability_domains`, `results`, `findings`, `reasons`, `release_limits` | Reporting §16.1 | SIT-VG010, SIT-VG013, SIT-VG026 |
| Run | `processing_state`, `tool_name`, `tool_version`, `input_contract_version`, `requested_diagnostic_ids`, `completed_diagnostic_ids`, `started_at`, `finished_at`, `diagnostics`, `qualifications` | Reporting §16.8 | SIT-VG010, SIT-VG013, SIT-VG022 |
| Input identity and digest | `source_mode`, `input_contract_version`, `bundle_id`, `snapshot_id`, `declared_predecessor`, `raw_file_digest`, `qualifications`; digest `algorithm`, `value`, `covered_material` | Reporting §16.8 | SIT-VG002, SIT-VG023 |
| Input validation / diagnostic | `state`, `diagnostics`; each diagnostic `code`, `location`, `safe_message`, `qualifications` | Reporting §16.8 | SIT-VG001, SIT-VG010, SIT-VG021 |
| Scope | `id`, `inquiry_ref`, `claim_refs`, `target_refs`, `dependency_dimension`, `graph_view`, `temporal_basis`, `requested_time`, `coverage_refs`, `qualifications` | Reporting §16.2 | SIT-VG006, SIT-VG012 |
| Population | `id`, `scope_ref`, `unit`, `member_refs`, `selection_rule`, `coverage_refs`, `basis_refs`, `membership_state`, `qualifications` | Reporting §16.3 | SIT-VG012, SIT-VG016 |
| Atomic Result | `id`, `diagnostic_id`, `field_key`, `scope_ref`, `population_refs`, `execution_state`, `result_state`, `result_origin`, `value_kind`, `value`, `check_refs`, `basis_refs`, `witness_refs`, `reason_refs`, `interpretation_limit` | Reporting §16.4 | SIT-VG011, SIT-VG012, SIT-VG014, SIT-VG016 |
| Fraction / interval | `numerator`, `denominator`, optional `display_decimal`; interval `lower`, `upper`, `interval_kind` and shared population | Reporting §16.5 | SIT-VG016 |
| Partition / incidence | Exclusive category memberships, counts and total; incidence memberships, `c_r`, N and `nonexclusive`; preserve typed report meaning | Reporting §§16.5,17 | SIT-VG012, SIT-VG016 |
| Basis entry | Report-local `id`; input source identity, native basis/asserter/method/support/availability/scope/time/lifecycle, qualifications and check links | Reporting §16.6 | SIT-VG002, SIT-VG007, SIT-VG021 |
| Capability | `id`, `diagnostic_id`, `inquiry_ref`, `scope_refs`, `check_refs`, `result_refs`, `available_result_refs`, `unavailable_result_refs`, `not_applicable_result_refs`, `not_evaluated_result_refs`, `reason_refs`, `scope_note` | Reporting §16.7 | SIT-VG011, SIT-VG013 |
| PrerequisiteCheck | `id`, `check_id`, `scope_ref`, `state`, `input_refs`, `reason_refs`, `note` | Reporting §13.1 | SIT-VG014 |
| Reason | `id`, `code`, `scope_ref`, `affected_result_refs`, `input_refs`, `detail`, `classification` | Reporting §13.2 | SIT-VG014 |
| Observability-domain entry | `level_index`, `label`, `available_result_refs`, `unavailable_result_refs`, `not_evaluated_result_refs`, `reason_refs` | Reporting §15 | SIT-VG013 |
| Finding | `id`, `observation_kind`, `condition_code`, `diagnostic_refs`, `threat_family_refs`, `scope_ref`, `population_refs`, `basis_refs`, `witness`, `contrary_input_refs`, `reason_refs`, `statement`, `interpretation_limit` | Reporting §18.1 | SIT-VG008, SIT-VG015, SIT-VG017 |
| Typed references / witness payload | Input collection kind + snapshot-local ID + selector when needed; report-local target kind; finite ordered node/edge/record links or exact examined population | Reporting §§16.6,18.1,19.2 | SIT-VG002, SIT-VG008, SIT-VG015, SIT-VG018 |

The root schema is closed under its current contract. A diagnostic envelope cannot reuse the ordinary report's analytical arrays merely because they contain syntactically valid data. A Result reference must resolve in this report, while an input reference must resolve in its own typed snapshot namespace. Matching strings do not join the namespaces.

A `record_disclosures` payload must preserve every selected original field needed to interpret its meaning, including native conclusions, basis, time and qualification. It cannot hide a new scalar inside a free-form disclosure. Optional plain record display counts remain scoped inventory disclosures under the existing definition; they do not authorize an extra registered analytical leaf.

## 14. Prerequisite, reason and finding-condition exercise matrix

### 14.1 Prerequisite coverage

Each PC row is tested as a scoped instance through `SIT-VG014/<PC-ID>`. Use a supported positive premise for `met`, remove only the required evidence for `unknown`, supply a definite incompatible fact for `unmet` where the contract permits, and exercise `not_applicable` only for a genuinely inapplicable subject. Do not demand all four states of a PC when its semantics cannot produce one of them; record that structural inapplicability in the later test manifest.

PC01 distinguishes accepted input from no analytical reporting. PC24 distinguishes completed population processing from interruption. Neither permits a fabricated epistemic value. Each test also has a localization control: the changed prerequisite must not invalidate an unrelated established result.
| Check | Exact question from reporting §13.1 | Specific supporting families |
|---|---|---|
| PC01 | Was the complete bundle structurally accepted? | SIT-VG001, SIT-VG010 |
| PC02 | Are the exact inquiry, Claim version, subject, dimension and view identified? | SIT-VG002, SIT-VG012 |
| PC03 | Is the required seed/comparison/target population explicitly identifiable? | SIT-VG012 |
| PC04 | Are the relied-on typed relations active, affirmed and scope-compatible? | SIT-VG004, SIT-VG008, SIT-VG009 |
| PC05 | Is the required supporting basis supplied and non-self-certifying? | SIT-VG007 |
| PC06 | Does relevant coverage address the required finite dependency area? | SIT-VG005, SIT-VG007, SIT-VG008 |
| PC07 | Are documentary origin boundaries qualified in the selected dimension? | SIT-VG005, SIT-VG007 |
| PC08 | Is identity sufficiently resolved for the particular qualified statistic? | SIT-VG002, SIT-VG009 |
| PC09 | Is the necessary premise free of a relevant unresolved conflict? | SIT-VG009 |
| PC10 | Does the explicit snapshot/time basis support this temporal claim? | SIT-VG006 |
| PC11 | Does one supplied comparison assessment satisfy its full qualification? | SIT-VG005, SIT-VG007 |
| PC12 | Do all seeds satisfy the complete single-origin HHI gate? | SIT-VG012, SIT-VG016 |
| PC13 | Is the immediate EvidenceItem-link enumeration sufficient for its profile? | SIT-VG004, SIT-VG008 |
| PC14 | Are applicable evaluator roles, subjects and dimensions represented? | SIT-VG003, SIT-VG008 |
| PC15 | Is externality grounded against the exact declared system boundary? | SIT-VG005, SIT-VG012 |
| PC16 | Is the target run/stage key unambiguous and the finite cohort enumerated? | SIT-VG005, SIT-VG012 |
| PC17 | Are the cohort's individual stage classifications established? | SIT-VG009, SIT-VG012 |
| PC18 | Is there one eligible evidenced admission-to-target comparison? | SIT-VG012 |
| PC19 | Does a finite declared correction route match this channel/target/action? | SIT-VG004, SIT-VG008 |
| PC20 | Are all required route grants, scope and time applicable and supported? | SIT-VG005, SIT-VG006 |
| PC21 | Does a case-linked change have qualified before/after or removal evidence? | SIT-VG003, SIT-VG007 |
| PC22 | Are human contribution, process identity and dependency limits disclosed? | SIT-VG003, SIT-VG007 |
| PC23 | Are anomaly/contestation context and any eligible baseline retained? | SIT-VG003, SIT-VG012 |
| PC24 | Has the operation processed the whole population required for this value? | SIT-VG010, SIT-VG022 |

### 14.2 Reason-code coverage

Each existing reason receives the branch exercise `SIT-VG014/<code>`. Preserve all applicable blockers with their input IDs. The paired control verifies that the reason is not emitted when its premise is absent or belongs only to an unrelated scope. Runtime meanings of resource and request-subset codes remain limited by their adopted interfaces; dormant codes are tested as prohibitions/output-contract constraints until their positive runtime premise is authorized.
| Existing reason code | Required test branch | Paired control / limit |
|---|---|---|
| `no_seed_contributions` | Valid sparse Inquiry has no Claim-bound seed EvidenceItems; its seed count remains 0, while a requested origin fraction lacks seeds. | H7-01's six seeds remove this blocker. |
| `zero_denominator` | Explicitly empty selected finite population: an inventory can be 0, but fraction/interval has null value. | A known nonempty all-negative population can return 0/T. |
| `missing_comparison_assessment` | Remove the applicable independence assessment without adding a surrogate; qualified comparison unavailable. | Restore IND12 at its own scope only. |
| `scope_unestablished` | Ask the relevant qualification of a structurally valid record whose necessary scope is unestablished; do not infer an all-Claim scope. | A resolved exact inquiry/Claim/dimension is the paired control; structurally invalid scope references are instead rejected. |
| `dimension_not_selected` | Inventory-only Inquiry has an empty dimension selection; no hidden default acquisition analysis. | Select acquisition explicitly in the paired dossier; do not select all dimensions implicitly. |
| `unknown_endpoint` | H7-V02 or W7-03 reaches a typed UnresolvedReference. | A resolved, qualified replacement in a separately versioned derived case can remove this gap. |
| `upstream_coverage_incomplete` | Partial or unsupported necessary upstream coverage withholds complete ancestry/HHI. | Supported finite coverage does not erase any still-known unresolved branch. |
| `unqualified_origin_boundary` | A resolved terminal has no qualified boundary assessment or has unresolved contrary parents. | An adequate OB plus its matching support is the control; inventory of reached terminals is not suppressed. |
| `baseline_or_scope_cut` | W7-17 contains a reference baseline or deliberate scope cut. | A documentary boundary is tested separately, without relabeling the baseline. |
| `declared_origin_only` | W7-17 retains only declared_origin for a branch. | A qualified documented_origin must supply the missing basis and coverage. |
| `multi_origin_unallocated` | H7-V03 has two known origins for a seed without allocation. | H7-01 has one documented terminal per seed; no 50/50 text parser is introduced. |
| `identity_unresolved` | W7-23 supplies same_identity_as for counted origins without a canonical replacement dossier. | Distinct adequately specified IDs with no relevant identity ambiguity are the control; input is never merged automatically. |
| `premise_disputed` | W7-23's active denial or W7-19's contrary observation concerns a necessary premise. | An additional unknown observation alone does not negate separately supported occurrence. |
| `lineage_cycle` | W7-04's acquisition cycle plus exit leaves cyclic ancestry unresolved. | Citation-only cycle control leaves the acyclic acquisition HHI eligible. |
| `support_uninspectable` | W7-25 has only a locator, wholly unavailable attestation or unsupplied needed excerpt. | Restore a supplied scoped excerpt/visible attestation; do not auto-fetch. |
| `documentary_basis_incomplete` | Keep valid nullable/Gaps but remove a required documentary method, identified attestor or supporting basis. | Restore the actual missing element; a label alone is insufficient. |
| `self_supporting_assurance` | W7-25 self-pointer or mutual assertion-support loop is sole assurance. | Independent supplied supporting material breaks the sole-support problem while the historical loop remains disclosed. |
| `time_applicability_unknown` | W7-21's time-specific grant lacks effective time or has only insufficient date precision. | A grant clearly covering the requested instant is the control; no midnight/timezone is invented. |
| `temporal_inconsistency` | Known, well-formed event times place a claimed source transformation in an impossible order. | Same graph with supported compatible times removes this analytical limit; malformed syntax uses input rejection. |
| `roles_incomplete` | An Evaluation contains a valid role gap or unresolved required role binding. | Actual generator/judge bindings enable their own comparison without filling rubric history. |
| `externality_unestablished` | No qualifying grounding/boundary assessment exists, despite admission or a human label. | Restore EXT-F's supported relation to I1; selection remains a separate result. |
| `cohort_anchor_missing` | W7-20 supplies final-only records or membership without the required PipelineRecord anchor. | Supply one eligible target-stage anchor and its evidenced population. |
| `cohort_anchor_ambiguous` | Two target stage keys compete in one proposed cohort specification. | Separate scopes/coverage select one key each; never choose by array order. |
| `cohort_universe_unestablished` | A cohort has unknown membership, omitted members or no evidence-bearing finite enumeration. | An explicit resolved-member universe is the control; empty and absent stay different. |
| `stage_classification_unresolved` | H7 influence has EE unknown; W7-19 includes a disputed member. | Every member with an established classification enables a point fraction; no unknown member is dropped. |
| `transition_baseline_unestablished` | Two admission baselines compete, baseline membership differs, or one admitted member is unresolved. | Unique same-member fully evidenced admission plus preservation/selection target qualifies. |
| `route_not_recorded` | Completed supplied-view search has no eligible declared route for the actual target/action. | Restore one finite route; partial coverage never becomes global impossibility. |
| `authority_unestablished` | Declared route has a missing/unsupported needed grant. | Supply a matching grant on every required leg; declarations of action alone do not suffice. |
| `authority_inapplicable` | W7-21's review-only grant is used to request amend, or a grant names another target version. | Matching action, exact target and applicable time form the control. |
| `change_evidence_missing` | H7-E or W7-09 has no sufficiently supported case-linked change. | Restore explicit supported linkage; an unrelated later edit remains insufficient. |
| `before_after_unresolved` | W7-22 control has an unresolved after-state or unsupported removal. | Explicit supported retraction with structural-null after_ref is a different valid case. |
| `context_withheld_or_unavailable` | Protected original context is absent from permitted visible material. | An authorized supplied excerpt/reference removes only that visibility limitation. |
| `no_applicable_subject` | W7-06 compares Evaluations; an origin-only qualified count is inapplicable. | The procedure-member result can remain available; missing assessment is not inapplicability. |
| `outside_v01` | Output-contract/prohibition test: an excluded detector or scalar must remain outside release, with no fabricated public field. | The code must never be used to excuse an unimplemented required M001-M015 capability. |
| `analysis_not_selected` | Dormant-interface guard: source text or an extension cannot select away a required diagnostic; default audit attempts all 15. | Only a separately adopted request-subset interface may exercise this code positively; no such option is invented by WU8. |
| `resource_limit_reached` | Fault/limit scenario interrupts a required operation at an adopted budget or cancellation point. | The paired completed run has PC24 met. Concrete numeric boundaries are held for WU9. |
| `execution_failed` | Injected execution defect in a future approved operation emits failure diagnostics, not an evidence-gap result. | Legitimately unavailable evidence in a completed operation never uses this execution code. |
| `input_not_accepted` | Rejected or unfinished validation prevents analytical reporting. | A valid sparse accepted dossier still receives capability non-results, not rejection. |
| `completion_interval_not_needed` | H7 exact fraction has U=0, so its interval field is completed/not_applicable. | H7 influence with U>0 can carry the permitted interval and unavailable point. |
| `comparison_scope_mismatch` | Compare reported numbers after changing selection/unit/Claim/dimension without stating the change; the silent comparison is nonconforming. | H7-V01 explicitly discloses a changed population; each individual report remains valid. No comparison API is added. |

Reason classifications are the existing `evidence_gap`, `conflict`, `structural_inapplicability`, `release_boundary` and `execution`. Test that a classification agrees with the actual reason instance. This unit does not impose a new one-to-one code/classification table where the owner contract has not prescribed one.

### 14.3 Finding conditions and witness obligations

`SIT-VG015/<condition_code>` exercises every existing condition below with its own narrow supplied evidence. For each, construct a matched control without the necessary relation, record or qualification. The finding must then disappear or become the appropriate gap/attributed record; it must not turn into an unrelated stronger condition. Absence conditions need completed examined populations, not an invented empty positive path.

All six existing observation kinds must be exercised separately. Source-level status, severity, malicious intent and clean-source verdicts remain prohibited. The following association column repeats the current reporting permission; it adds no new threat rule.
| Existing condition | Evidence-bearing narrow observation | Permitted threat association |
|---|---|---|
| shared_origin_witness | Same claim/dimension contributions have a recorded common origin | SIT-TH001 |
| citation_path_witness | Explicit Artifact citation path, without inferred evidentiary dependence | SIT-TH002 |
| transformation_path_witness | Explicit material or claim-scoped derivation | SIT-TH002; SIT-TH003 only with supplied syndication/copy relation |
| model_mediated_derivation_witness | Disclosed model-generation role and transformation chain | SIT-TH004 |
| view_cycle_witness | Finite cycle in the named citation/material/claim/model/succession view | SIT-TH005; SIT-TH007 only with represented benchmark context |
| assurance_loop_limitation | Self/circular evidence support does not independently certify itself | SIT-TH005 |
| evaluator_overlap_witness | Shared object, common ancestor or one-sided ancestry in actual evaluator roles | SIT-TH006; SIT-TH007 with explicit benchmark role/artifact |
| family_label_match | Exact supplied model-family label strings match | SIT-TH006, with explicit warning that it is a label match |
| provenance_gap | Explicit unresolved or unsupported history | SIT-TH008, as a gap rather than proof of erasure |
| verification_scope_limitation | Identity/process verification cannot substantiate the stronger claim | SIT-TH009 |
| independence_record_conflict | Relevant supplied process-independence and ancestry assertions conflict | SIT-TH001 or SIT-TH006 as appropriate |
| correction_dependency_witness | Recorded control/process overlap in a corrective role | SIT-TH010 |
| correction_route_limitation | Declared path, grant, action or temporal applicability is unestablished/inapplicable | SIT-TH010-SIT-TH011 |
| case_handling_disclosure | Attributed submission/handling outcome for one case | SIT-TH011 only at that bounded case meaning |
| linked_change_disclosure | Attributed before/after or supported-removal linkage | No adverse threat association required |
| downstream_change_undocumented | Required linked-change evidence is absent from the examined record set | SIT-TH011, without a failed-correction claim |
| externality_stage_limitation | Externality/intake/use stages remain incomplete or separately contradicted | SIT-TH012, without an adequacy verdict |
| recorded_stage_exclusion | Evidence-bearing non-occurrence in an explicit cohort/stage | SIT-TH014, without inferred motive |
| anomaly_or_contestation_disclosure | Supplied context, stance or unclassified anomaly remains visible | SIT-TH014 where relevant; no threat verdict required |
| attributed_external_observation | Source report/evaluation outcome disclosed at its actual basis | No automatic semantic assignment to a threat family |
| scoped_no_witness | Completed typed search found no eligible witness at its declared scope | No claim that any threat family passed |
| recorded_data_conflict | Explicit well-formed contradictory scope/identity/time/record information | Family association only where a matching threat card applies |

For condition-specific witness construction, use the exact witness clauses above and the existing W5 threat witnesses rather than paraphrase similarity. A procedural-independence conflict uses its actual contrary assertion; a verification limitation uses its reported scope; a correction-dependency witness needs the recorded control/process link in that role. An external allegation is `attributed_external_observation`, regardless of how emphatically its text names a threat.

No test requires inventing a detector-positive for SIT-TH013. The required check is truthful attribution and the explicit no-detector release boundary.

## 15. Future test families, stages and execution evidence

### 15.1 Coverage of every family required by the approved plan

The planned implementation tests below remain unexecuted. A later phase plan must authorize each actual file and test behavior. Unit, integration, golden, negative, metamorphic, fault-injection and performance techniques can share fixtures, but cannot omit their independently required assertions.
| Plan-required family | Assigned test obligations | Required meaning |
|---|---|---|
| Schema validation | SIT-VG001, SIT-VG003-SIT-VG007 | Input contracts and every required/nullable/enum branch |
| Object identity | SIT-VG002, SIT-VG012 | Snapshot-local identity, versions, protected keys and no silent merge |
| Edge direction | SIT-VG004, SIT-VG008 | All typed predicates and canonical record links |
| Duplicate identifiers | SIT-VG001-SIT-VG002 | Cross-collection IDs, JSON keys and unique-reference arrays |
| Lineage roots | SIT-VF006-SIT-VF012; SIT-VG007-SIT-VG009 | Inventory, qualified boundaries and supplied comparisons |
| Multi-parent derivation | SIT-VF013-SIT-VF020; H7-V03 | No parent allocation; distinct immediate and upstream roles |
| Cycles | SIT-VG008, SIT-VG015; W7-04 | View-specific finite witnesses, including cycle with an exit |
| Unknown provenance | SIT-VF021-SIT-VF024; SIT-VG007 | Frontiers, unsupported terminals, evidence gaps |
| Claim-scoped independence | SIT-VF009-SIT-VF012; SIT-VG012 | Exact supplied pair/set and dimension |
| Transformation lineage | SIT-VG004, SIT-VG008; W7-08 | Copy, syndication, summary, translation and quote ancestry |
| Evaluator lineage | SIT-VF025-SIT-VF028 | Actual roles, strict ancestors and separate family strings |
| Correction reachability | SIT-VF038-SIT-VF040; SIT-VG006 | Finite routes and every required grant |
| Correction propagation | SIT-VF041-SIT-VF048 | Cases, handling, changes, distinct target pairs and undocumented targets |
| External presence | SIT-VF029-SIT-VF037 | Boundary-qualified externality and separate process stages |
| Observability labels | SIT-VG013-SIT-VG014 | Non-cumulative evidence navigation and per-cell availability |
| Report determinism | SIT-VG017-SIT-VG018 | Semantic repeatability with explicit volatile exclusions |
| Golden hero | SIT-VG024; H7-01, H7-V01-H7-V03 | Exact frozen populations and logical oracle |
| Privacy and path safety | SIT-VG020-SIT-VG023 | Concrete policy-dependent tests held for WU9 |
| No-network baseline | SIT-VG019-SIT-VG020, SIT-VG023 | Whole runtime boundary in addition to import behavior |
| Malformed-input rejection | SIT-VG001-SIT-VG007; W7-24 | Precise safe diagnostics without analytical salvage |
| Large-graph performance | SIT-VG008, SIT-VG022 | Adopted resource budgets, bounded finite witnesses and failure behavior |

### 15.2 Implementation-stage limits

Phase 0 records test intentions and checks the documents only. Phase 1 remains a scaffold under a separate future plan; it may validate approved structural scaffolding but cannot run analytical graph/metric behavior merely because this unit specifies future tests.

Analytical unit/integration tests begin only in the later authorized implementation phase for the relevant capability. Golden report, cross-format, full runtime isolation and performance evidence belong to the phases that actually implement those behaviors. WU8 does not invent numbers for those later implementation phases.

A release cannot claim a required capability solely because its test file exists, is skipped, or returns a placeholder. An executable result containing a truthful evidence-limited non-result is different from a capability never implemented. Both need honest test evidence.

### 15.3 Future execution-evidence record

For every implemented obligation, the later validation record must identify: obligation/Trace ID; approved input/expected-output revision and actual hashes where computed; implementation revision and contract; exact test entry point; actual result and relevant scope/reasons; environment and adopted limits; execution outcome; mismatch or exclusion reason; and the responsible review record.

These are requirements for validation evidence outside the product report. They add no input or report fields to `sit-bundle/0.1` or `sit-report/0.1`. A test outcome must not be backfilled from the expected result.

All required executable assertions must pass before the corresponding implementation/release gate passes. Missing, skipped, unrun, interrupted or policy-held tests stay visible and do not count as passing. Optional byte/decimal representations are tested when exposed; a required semantic distinction cannot be made optional.

## 16. Falsification, mutation and external challenge

### 16.1 Four failure classes

A code defect violates an already unambiguous contract. A specification ambiguity leaves two materially different outcomes consistent with the text. A dishonest/incomplete dossier defeats the source basis without necessarily causing a code violation. A structurally inadequate product cut cannot represent a consequential distinction even with truthful supplied evidence.

The response must match the failure. Fix code against the adopted oracle; resolve a semantic ambiguity with the specification owner; preserve limitations and challenge provenance for dishonest input; or reopen the product specification when a genuine out-of-cut example appears. Automatically changing the oracle, dropping the example or declaring the theory disproved by a parser error is prohibited.

### 16.2 Minimum falsifiers of toolkit conformance

The following are independently required negative controls. Any occurrence in the relevant completed output fails its corresponding test:

1. Five derivative source artifacts become five independent observations.
2. Removing provenance increases a qualified independence result.
3. A parentless unresolved or unqualified record becomes an original source.
4. A mailbox, accepted handling record or graph route is presented as full corrective capacity.
5. Missing change evidence becomes a failed-correction fact.
6. Shared evaluator ancestry is hidden or a family label becomes a verified ancestry path.
7. Independent disagreement lowers integrity, becomes equal-weight voting, or disappears from the selected set.
8. Identity/process verification becomes substantive truth.
9. The same Artifact cannot have separate Claim-bound contributions and origins.
10. Unknown or multi-origin seeds are dropped to rescue HHI.
11. A pipeline unknown is removed from T, or separate stages are multiplied into Presence.
12. An interrupted enumeration becomes zero origins, zero overlap or a completed no-route result.
13. A Markdown summary omits material limits retained by JSON.
14. A report's synthetic case success is presented as outside-world authentication.

These controls map to the 57 leaf rows and shared families, especially SIT-VG007-SIT-VG018 and SIT-VG024-SIT-VG026. They test the implementation and the declared operationalization, without claiming to experimentally validate UIL, SIL, EC, HDL, EBC or BVL.

### 16.3 Independent challenge and anti-circular testing

Later validation should include an independently authored challenge dossier or an independently reproduced oracle for consequential case families when such a reviewer is available. Record actual authorship, shared tools/source lineage, disagreement and unexamined areas. Two passes by the same assistant are not two independent reviews.

The current suite is deliberately public and frozen for regression. Its existence cannot prove open-world performance. Newly supplied anomalies must retain their original context and the failed representation/field assumption. Classify a failure as an implementation mismatch, input limitation, unresolved semantic issue or product-scope challenge, and escalate the affected rule without silently rewriting the old cases.

W7-28 remains an important counterexample: a coherent fabricated dossier can satisfy local structure and still mislead the audit. A future test confirming that residual limit passes only the honest-reporting requirement. It does not certify that the fabricated source is true or make external authenticity unnecessary.

The source papers' formal results remain conditional on their stated models. Empirical claims about real correction rates, model performance, mutual information, independent observations or downstream harm require domain-native evidence beyond these fictional fixtures. No external experiment is performed by this unit.

## 17. Traceability closure and later implementation gates

[THEORY_TO_CODE_TRACEABILITY.md](THEORY_TO_CODE_TRACEABILITY.md) assigns SIT-TR001-SIT-TR035. Each leaf has one primary responsibility owner and references its four tests. Shared checks have their own Trace owners. All 40 Theory Map IDs receive either an active, bounded operationalization or an explicit interpretive/exclusion role. Product IDs and old case IDs are retained.

Current logical responsibility owners are prospective module responsibilities, not created modules. WU10 must bind them to actual file/module/public-interface/test paths. Until then, no package tree or dependency is selected from a convenient test library.

The following remain implementation gates:

| Gate | Required resolution | Current effect |
|---|---|---|
| Concrete privacy, export and filesystem policy | WU9 controls, disclosure permissions, retention/log rules and safe destination/overwrite handling | SIT-VG017, SIT-VG019-SIT-VG023 have written obligations; no runtime privacy pass |
| Numeric resources and portable integer policy | WU9 limits and WU10 representation/processing choices | Parametric resource-boundary and large-number tests remain uninstantiated |
| Exact interfaces and serialization | WU10 CLI/Python contract, canonical bytes, report-ID and witness selection rules | Semantic oracle is fixed; exact byte snapshots/signatures are not fabricated |
| Any newly exposed in-scope ambiguity | Owner decision with source/field/test/Trace impact before fixture freeze | Hold only the affected executable assertion; do not choose silently |
| License/third-party treatment | WU9 documented decisions, later verified distribution artifacts | No implied inherited license or external asset redistribution |
| Full Phase 0 and execution authority | WU11 audit/approval followed by separately approved implementation phases | No code, schema, executable fixture or CI work begins here |

The current field registry has no additional unsupported analytical leaf that must be invented to complete coverage. An optional inventory count or future API exposing a genuinely new result must first be reconciled with the owner contract and receive coverage before implementation.

## 18. Work Unit 8 review package and exact stop

| Review item | Submitted realization | Scope limit |
|---|---|---|
| WU8-C01 | Complete 57-leaf, 228-obligation matrix; 26 shared families; field, state, prerequisite, reason and condition coverage | Test specifications only; no new metric or input/report field |
| WU8-C02 | 35 stable Trace IDs, primary logical responsibility owners, reverse source/product/field mappings and independent oracle discipline | Actual code paths/interfaces remain WU10; no claim of implemented coverage |
| WU8-C03 | Separate conformance, specification ambiguity, dishonest input and product-cut challenge; honest execution evidence and explicit WU9/WU10 gates | No empirical/source-authenticity/security certification or final Phase 0 approval |

The delivery consists of three Markdown files and their archive. Historical numbered bodies, inputs, PDFs and archives remain unchanged. Success §§18-19 record actual authoring checks and the read-only byte manifest. No runtime tests, executable fixtures, analytical algorithms, dependency installations, GitHub writes or independent second review were performed.

Stop after this package. The next planned unit is **Work Unit 9: privacy, security and licensing**, limited to `PRIVACY_AND_DATA_HANDLING.md`, `LICENSING_NOTES.md` and `SOURCE_INTEGRITY_THREAT_MODEL.md`. Full architecture remains Work Unit 10 and final audit/approval remains Work Unit 11.
