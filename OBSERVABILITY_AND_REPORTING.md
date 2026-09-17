# OBSERVABILITY_AND_REPORTING

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Target release | v0.1 |
| Phase / work unit | Phase 0 / Work Unit 6: Observability and uncertainty |
| Revision | 0.2 |
| Date | 2026-09-17 |
| Status | PROPOSED FOR REVIEW; accepted WU4 analytical body retained, WU6 reporting realization submitted |
| Theory Owner | Xiangyu Guo |
| Technical Owner | Unassigned |
| Accepted input basis | SIT-D001-SIT-D025 in register revision 0.5; SIT-D026-SIT-D027 Option B accepted as recorded in §11.1 |
| Central register | Revision 0.5 retained unchanged; scoped acceptance supplement in §11.1 |
| Current review choices | WU6-C01-WU6-C03 in §23 |
| Definition owner | `DEFINITIONS_AND_UNITS.md` revision 0.2 |
| Input and bridge owner | `CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` revision 0.2 |
| Threat reference | `SOURCE_INTEGRITY_THREAT_MODEL.md` revision 0.1 |
| Current output contract | Reserved `sit-report/0.1`; specification only |
| New material | Sections 11-24; result/check/reason contract, complete capability matrix, report envelope and 32 written witnesses |
| Remaining work | WU7 hero; WU8 executable-test obligations/trace ownership; WU9 privacy/resources; WU10 architecture; WU11 final audit |
| Full Phase 0 approval / implementation | Not issued / not implemented |

**Revision 0.2 reading rule.** Sections 1-10 below retain the complete WU4 numbered body verbatim, including its historical status, checks and then-future work assignments. Its current approval is established by the later register and §11.1, not by those historical descriptions. Sections 11-24 are the current WU6 submission. They realize the previously reserved reporting details without changing the inherited metric definitions or exclusions. Acceptance of the preceding unit does not pre-approve this new realization.

## 1. Purpose, authority and source basis

This document supplies the reporting-facing part of Work Unit 4. It answers what the proposed v0.1 profile can count, what each number means, which inputs permit it, and what remains unavailable. The complete report envelope and final observability vocabulary are still Work Unit 6 tasks.

The latest request is “继续”. Following the existing approval discipline, it authorizes preparing the next conditional specification package. It is not recorded as explicit approval of the three pending detailed choices from Work Unit 3. This document therefore uses that submitted ontology as a named provisional dependency. It cannot freeze or bypass its adoption gates.

Theory references retain the source aliases and page locators from [SPEC_AUDIT.md](SPEC_AUDIT.md) and [THEORY_SOURCE_MAP.md](THEORY_SOURCE_MAP.md). Primary support comes from SIL pp. 7 and 11-16, UIL pp. 8-9 and 15-16, EC §§3.2 and 6-7, and HDL §§3.1, 4.6, 9-11. BVL's separation of routing and capacity is used only for the correction-limit distinction. No current market, political, regulatory or software-standard claim is asserted or independently verified here.

The papers motivate the dimensions. Exact counts, the restricted HHI, the row classifications and completion intervals are toolkit operationalizations. Their assumptions are owned by [DEFINITIONS_AND_UNITS.md](DEFINITIONS_AND_UNITS.md), §§19-29. The sources are not claimed to contain these field names or to calibrate numerical thresholds.

### 1.1 Work-unit boundary

The four permitted files for this unit are the updated definitions, this new document, the updated product specification and the updated decision register. The lineage/data contract, prior archives, plan, source audit/map and papers remain read-only.

No new input field or schema is introduced by a reporting requirement. No graph algorithm, implementation test, parser, application, library, detector, network integration or GitHub change is performed. Simple arithmetic used to check written examples is an authoring check.

### 1.2 Reporting objective

The report must keep these distinctions visible:

- supplied record inventory versus the unknown outside population;
- artifact versions versus claim-bound contributions versus origin processes;
- recorded common ancestry versus positive evidence of process independence;
- known multiple parents versus unknown parents;
- a declared route versus applicable authority, handling and linked change;
- externality versus admission, preservation, selection and downstream use;
- context-preserving disagreement versus truth adjudication.

A missing numerical scalar does not erase useful structural findings. A high-coverage graph can expose extensive dependency. Neither observation coverage nor a low concentration value certifies truth, independent judgment or deployment readiness. [SIT-T017, SIT-T025, SIT-T031, SIT-T038]

## 2. Analytical contract catalog

`SIT-M001` through `SIT-M015` are stable diagnostic IDs first introduced in this unit. They identify field families and their obligations. They do not replace the existing forty Theory Map IDs, sixteen Product IDs or later implementation Trace IDs.

Every emitted numerical leaf inherits the population, unit, missing-data rule and interpretation of its contract. Optional display counts must state their exact selected IDs; they cannot introduce a new ratio or quality score outside the catalog.

| ID | Proposed public analytical family | Governing definition | Required result or honest non-result |
|---|---|---|---|
| SIT-M001 | Seed Artifact/EvidenceItem inventories, including unresolved artifact references and claim-unassigned seeds | Definitions §§20.1, 21.1 | Exact record counts with separate units; sparse input does not become zero real-world sources |
| SIT-M002 | Reached origins and qualified/declared/baseline boundary inventories | Definitions §21.2 | Record and boundary membership; no original observation inferred from a parentless node |
| SIT-M003 | Submitted comparison size and qualified process/origin-set member counts, per assessment | Definitions §21.3 | Exact supplied comparison set, dimension and qualification; no global independent-source total |
| SIT-M004 | Per-seed origin sets, nonexclusive root incidence, exhaustive seed dispositions and documentary resolution fraction | Definitions §22 | Known branches remain visible; mixed/unresolved contribution stays in the full seed denominator |
| SIT-M005 | `single_origin_contribution_hhi` | Definitions §23 | Supplementary rational value only for the complete single-origin population; otherwise unavailable with blockers |
| SIT-M006 | First-step direct/inherited/mixed/unresolved profile, inherited-only fraction or finite-record completion interval | Definitions §24 | Precisely labeled EvidenceItem-layer dependence; no estimate of semantic novelty |
| SIT-M007 | Frontier reference, unqualified terminal and affected-seed inventories | Definitions §22.4 | Counts of represented gaps; hidden-origin count remains unknown |
| SIT-M008 | Role-pair evaluator/model/rubric/control overlap and supplied family-label matches | Definitions §25.1 | Witnessed commonality at the disclosed granularity; no behavioral correlation coefficient |
| SIT-M009 | Boundary-qualified externality assessments and linked stage disclosures | Definitions §25.2 | Separate asserted external/internal/mixed/unknown relations; no scalar Presence |
| SIT-M010 | Exact-key pipeline observations and finite-cohort stage occurrence/retention profiles | Definitions §26 | Member counts plus exact fraction or completion interval only with the declared population |
| SIT-M011 | Channel/target/action/time route witnesses and authority applicability | Definitions §27.1 | Scoped declared or authorized-route evidence; no path-to-effect substitution |
| SIT-M012 | Correction case, handling, change-record and distinct linked-target inventories | Definitions §27.2 | Imported process evidence without inferred success rate or unobserved failures |
| SIT-M013 | Corrective-process independence and substantive human-contribution disclosures | Definitions §25.3 | Attributed assessments and actual recorded contribution, with unresolved dependencies retained |
| SIT-M014 | Supplied anomalies/contestation, context preservation and eligible tail-stage comparisons | Definitions §26.5 | Preserve material and stated cohort; no undocumented suppression or motive claim |
| SIT-M015 | Scope-specific coverage and provenance/reference-basis inventories | Definitions §28.1 | Declared metadata plus its evidence gaps; no universal provenance-quality percentage |

### 2.1 Product and source crosswalk

| Diagnostic IDs | Product requirements | Principal source-map basis |
|---|---|---|
| SIT-M001-SIT-M002 | SIT-P001-SIT-P004, SIT-P006 | SIT-T008, SIT-T022, SIT-T035-SIT-T036 |
| SIT-M003 | SIT-P005-SIT-P006 | SIT-T016, SIT-T020, SIT-T035-SIT-T036 |
| SIT-M004-SIT-M007 | SIT-P006-SIT-P007, SIT-P016 | SIT-T017, SIT-T036-SIT-T037 |
| SIT-M008 | SIT-P008 | SIT-T018, SIT-T020, SIT-T022 |
| SIT-M009-SIT-M010 | SIT-P009, SIT-P012 | SIT-T001, SIT-T016, SIT-T029 |
| SIT-M011-SIT-M013 | SIT-P008, SIT-P010, SIT-P012 | SIT-T005, SIT-T011, SIT-T024, SIT-T034, SIT-T039 |
| SIT-M014 | SIT-P011 | SIT-T019, SIT-T021, SIT-T023, SIT-T032 |
| SIT-M015 | SIT-P002, SIT-P012-SIT-P014 | SIT-T004, SIT-T008, SIT-T022, SIT-T026, SIT-T038, SIT-T040 |

The operational source-map boundary SIT-T037 is especially important: the supplied papers do not calibrate HHI, inverse concentration or high/low bands for this product. The selected diagnostic remains count-distribution bookkeeping.

## 3. Disposition of every candidate integrity dimension

| Plan candidate | Proposed v0.1 disposition | Important limit |
|---|---|---|
| Nominal Source Count | SIT-M001, explicit Artifact-record inventory and separate contribution count | Distinct URLs, publishers and records are different units |
| Resolved Source Count | Resolved local Artifact references and supporting record disclosure | Local reference resolution does not authenticate source identity |
| Independent Root Count | SIT-M003, qualified origin-set members for each supplied assessment | No all-source, maximum-set or statistical independence total |
| Unknown Root Count | Replaced by SIT-M007 represented frontier/terminal counts | One gap can conceal many roots and several gaps can share one root |
| Lineage Concentration | SIT-M004 incidence profile; SIT-M005 restricted supplementary HHI | No weights for mixed parents; no scalar over a filtered resolved subset |
| Derivative Share | SIT-M006 represented immediate-evidence-layer profile and conditional fraction | Inherited-only labeling does not measure lost or new semantic information |
| External Presence | SIT-M009 and SIT-M010 boundary/stage evidence | No date-based score, global percentage or multiplied stage funnel |
| Corrective Independence | SIT-M013, individual qualified assessments plus documented overlap | Human title, different endpoint or mailbox supplies no independence |
| Correction Reachability | SIT-M011, action/time/target-specific route analysis | A connected path does not demonstrate a handled or effective correction |
| Evaluator Lineage Overlap | SIT-M008, separate role-pair witnesses and named dependency dimensions | Shared family/data reference does not establish correlated errors numerically |
| Tail / Contestation Retention | SIT-M014 with SIT-M010 only for a supplied eligible universe | A final-only dossier cannot establish what was suppressed |
| Provenance Completeness | SIT-M015, scope-specific coverage; SIT-M004's narrow resolution fraction | Metadata completeness does not supply truth, semantic completeness or independence |

### 3.1 Numerical choices explicitly outside v0.1

The following are not hidden future implementation tasks within this release: multi-parent weighted concentration, reciprocal/effective-root count, partial-provenance HHI bounds, global independence percentage, effective independent sample size, universal source-trust score, source reputation rankings, weighted human-judgment quality, scalar external-presence adequacy, aggregate correction-success rate, causal correction elasticity, queueing/cascade estimates, semantic-gradient/mutual-information estimation and high/low/extreme interpretation thresholds.

The restricted SIT-M005 scalar is a selected supplementary release capability if SIT-D023 is adopted: return its eligible value or a specific non-result. It is not an opt-out substitute for missing implementation. These exclusions do not remove the required structural profile. A later change can reconsider a diagnostic only with a new data/measurement contract, source mapping, decision and tests. Existing numerical source examples or institutional labels are not calibration data for such a change.

## 4. Required analytical result content

The following are conceptual requirements for WU6's serialized envelope. They are not a completed JSON Schema or final status enum.

### 4.1 Scope and reproducibility

Each result carries the diagnostic ID; bundle/snapshot identity; inquiry and Claim version where relevant; target object or assessment; dependency dimension and graph view; seed/cohort member IDs; snapshot-structural or time-specific basis; and coverage qualifications.

A number additionally carries its counted unit, exact numerator/denominator or bucket counts, treatment of duplicate references, and whether categories are exclusive. A number without that context is not a conforming standalone finding.

### 4.2 Evidence and derivation

Each derived result identifies premise Assertion/Evaluation/record IDs and their supplied evidence references. It preserves declaration, documentary, imported-inference and protected-attestation basis. Graph-derived findings remain conditional on those premises.

For existence findings, at least one finite witness and its basis are required. Where different witness paths have different assurance limitations, a preferred displayed path cannot conceal relevant disputes or unknown alternate dependencies. For complete-set and negative results, the full considered member/coverage boundary must be identifiable; one positive witness cannot establish exhaustive ancestry.

No full expansion of every possible path is required. Cycle witnesses remain finite and view-specific. Later algorithm selection may optimize representation but cannot count path multiplicity as origin multiplicity or alter the defined sets.

### 4.3 Availability and reasons

A missing result needs a concrete reason: no seed contributions, missing comparison assessment, unknown parent, unsupported boundary, mixed-parent allocation unavailable, identity dispute, unestablished relevant coverage, no cohort anchor, missing intake universe, uncertain applicable time, missing authority or analysis not performed, as appropriate.

Several reasons can apply. Do not replace them with a generic “low integrity” flag. An unavailable concentration value and a valid linked correction can coexist in the same report.

### 4.4 Protected material

Report identifiers and witness references must respect the future privacy/export contract. A public report must not reveal protected names merely to make a graph readable. Any exported redaction must preserve disclosed commonality where authorized and otherwise signal the resulting limitation; it cannot manufacture independence.

Exact export transformations, consent, overwrite behavior, permitted local destinations and sensitive metadata handling remain WU9 requirements. This unit grants no authority to publish the dossier or its evidence.

## 5. Report language and number presentation

JSON and Markdown must preserve the same substantive scope, value, uncertainty and limitations. Markdown may summarize, but it cannot remove the unknown seed share or change a qualified supplied assessment into an unqualified assertion about the world.

### 5.1 Required wording patterns

| Situation | Conforming wording example | Wording that would exceed the result |
|---|---|---|
| Five listed artifacts trace to one supplied origin | “Five listed Artifact records have paths to origin O1 in the supplied acquisition view.” | “There is only one possible source.” |
| Qualified three-member assessment | “Assessment Q1 documents a three-member acquisition-process comparison under its stated scope.” | “The system verified three statistically independent sources.” |
| Partial root data | “O1 is documented; one seed has unresolved ancestry. Concentration is unavailable for the full seed set.” | “Unknown ancestry was treated as a new independent source.” |
| All six seeds have single qualified roots | “Contribution-count HHI is 13/18, conditional on the stated six-seed population and recorded origin boundaries.” | “Source integrity is 72.2 percent.” |
| Same model ancestry | “The candidate generator and judge share recorded ancestor M0.” | “Their errors have correlation 1.” |
| No route in a partial graph | “No route was found in the supplied view; route coverage is partial.” | “No correction is possible.” |
| Accepted case and linked revision | “The request was accepted; a supplied process record links it to A_old → A_new.” | “The correction was proved right and the system is correctable.” |
| Three stage positives, one negative, one unknown | “The five-member cohort contains three evidenced occurrences, one evidenced non-occurrence and one unresolved member.” | “Retention is 75 percent after excluding the unknown.” |
| External origin, intake only | “Externality and admission are recorded; selection and downstream use remain undocumented.” | “External presence is adequate.” |

These are deterministic narrative templates proposed for later implementation, not generated sample runtime reports.

### 5.2 Exact and displayed values

Use the definitions §28.3 rational-number convention. For example, `13/18` may appear as `0.722222`, always with the exact underlying ratio available. Completion intervals retain their endpoints and full denominator. They are named finite-record or finite-cohort completion intervals rather than confidence intervals.

No decimal is rounded into a status or a warning threshold. A count of zero is meaningful only with the exact counted set. An unavailable value appears as unavailable/null with a reason in both formats, never as `0`, `-1`, `NaN` or a blank cell with ambiguous meaning.

### 5.3 Structural facts and evaluative judgments

Source graphs, layer labels and disagreement records do not supply a mandate for political, ideological, institutional or personal rankings. The report shows attributed statements, dependency evidence and specific missing information. It does not decide which viewpoint or actor should be preferred.

No chart or summary converts the source profile into an overall verdict. Qualitative risk/threat labels, their observable prerequisites and false-positive limits belong to WU5 and must remain source-bound and scope-specific.

## 6. Written analytical witnesses

These cases check the proposed definitions, not a running toolkit. All IDs and quantities are fictional and local to the individual case. Unless a case changes the premise, its relevant relations have matching inquiry/claim/dimension, active uncontested status, supplied supporting basis, adequate scoped coverage and applicable time. No real organization, source, political claim or product is being scored.

The actual hero, micro-fixtures and golden outputs remain WU7 work. These cases supplement rather than overwrite W3-01 through W3-16.

### W4-01: Five inherited representations and a second origin

Six seed contributions for C1 resolve completely: E1-E5 to O1 and E6 to O2. Their six Artifact versions are listed. O1 and O2 have qualifying origin boundaries. No independence assessment is supplied.

Expected: N = 6, two origin-record buckets, incidence counts 5 and 1, six single-origin rows. `single_origin_contribution_hhi = (25 + 1)/36 = 13/18`, displayed optionally as 0.722222. A qualified independent-origin set count remains unavailable. Two buckets do not certify two independent acquisitions.

Whether E1 is the original documentary record or one of several direct links changes the immediate-inheritance profile only according to its own first-step links; it does not alter the root histogram without a changed origin relation.

### W4-02: An unresolved seventh contribution

Add E7, whose ancestry is unresolved, to W4-01's seed set. Do not remove it from the inquiry.

Expected: N = 7; six single-origin rows and one unresolved row. Known incidences remain 5 and 1, now displayed as 5/7 and 1/7 if fractions are shown. Resolution coverage is 6/7. HHI for the full seed population is unavailable. The earlier 13/18 is not reused as a full-population result and the unresolved endpoint is not a third independent origin.

### W4-03: Known multiple origins without allocation

E1 resolves to O1; E2 to O2; E3 to both O1 and O2. All three rows are completely documented. No quantitative allocation exists.

Expected: two single-origin rows, one multi-origin row, and resolution fraction 3/3. Incidence counts are 2 and 2; incidence fractions are 2/3 and 2/3 and intentionally sum to 4/3. HHI is unavailable. Computing 1/2 by normalizing the incidence counts or splitting E3 in half would violate the contract.

### W4-04: A diamond of paths to one origin

One seed has two recorded branches that converge on the same O1, with complete supported ancestry and no other contribution.

Expected: N = 1, one origin bucket, one incidence and one single-origin row. HHI = 1. The additional branch adds witness structure, not a second origin. This is a concentration description without a truth verdict.

### W4-05: Pairwise assessments do not manufacture a setwise count

Three origins have qualified pairwise assessments Q12 and Q23. No setwise assessment covers all three.

Expected: two separate two-member process-assessment rows, with their origin qualification where applicable. No three-member joint total, four-independent-source total or transitive Q13 is created. Adding a separately supplied, qualified setwise Q123 permits that assessment's own three-member count; it does not erase the pairwise records.

### W4-06: Contradictory content and independent acquisition

E1 supports C1 and E2 contradicts C1. They resolve to two origins with a qualified two-member acquisition assessment and no contrary ancestry evidence.

Expected: the stated acquisition comparison can retain two qualified members. The support and contradiction both remain. If the two seed rows satisfy HHI prerequisites, HHI = 1/2. Neither the disagreement nor the concentration determines which substantive claim is right.

### W4-07: Different contribution and artifact units

One Artifact supplies three distinct seed EvidenceItems for C1. Each resolves to the same O1.

Expected: one claim Artifact record, three seed EvidenceItems, one origin bucket and HHI = 1. Splitting or combining contribution records can change a contribution-frequency statistic; the report discloses the supplied granularity. It cannot describe three independent documents.

### W4-08: Immediate inheritance with uncertain classification

Six seeds have complete supported immediate-link classifications for five rows: three inherited-only, one direct-only and one mixed. The sixth row lacks complete immediate ancestry.

Expected: D = 3, O = 1, M = 1, U = 1, N = 6. The point inherited-only fraction is unavailable. Its finite-record completion interval is `[3/6, 4/6]`, or `[1/2, 2/3]`. The mixed row is not halved. The unknown row remains in N. No fraction measures novel information.

### W4-09: Stage cohort with an unknown member

An admissible stage-anchored coverage record lists five cohort members. At the exact run/stage key, three have evidenced `occurred`, one has evidenced `did_not_occur`, and one has no sufficient observation.

Expected: T = 5, Y = 3, F = 1, U = 1. No point stage-occurrence fraction. The completion interval is `[3/5, 4/5]`, or `[0.6, 0.8]`. A value of 3/4 would improperly drop the unresolved member.

### W4-10: Empty population versus missing population

An inquiry supplies no seed EvidenceItems. Separately, a caller explicitly enumerates an empty pipeline population. Another dossier gives only final outputs and no intake universe.

Expected: the seed count is zero, while HHI and seed fractions are unavailable for zero denominator. The enumerated empty cohort's membership count can be zero; its stage fraction is unavailable, including where no stage anchor exists. The final-only dossier has an unknown intake population, not an empty intake population and not perfect retention.

### W4-11: One gap does not mean one hidden root

Two seeds reach the same protected UnresolvedReference U1. U1 has no qualifying origin-boundary record.

Expected: one unresolved frontier reference and two affected seeds. The common opaque reference survives redaction. The hidden origin count is unknown, and neither two independent sources nor exactly one fully resolved root is reported.

### W4-12: Two linked changes and one undocumented target

A correction submission has three explicit target versions. Supplied change records link that case to revisions of the first two targets; the third has no change record.

Expected: one case and two documentary linked target changes. The third target is undocumented with respect to change. No 2/3 correction-success rate or definite failure of the third is emitted. Additional handling records affect handling inventory, not the count of distinct cases.

### W4-13: Observed change with uncertain route authority

A case has a well-supported before/after change, but its channel authorization window is unknown or expired for the queried time.

Expected: preserve the linked change evidence; report unknown or nonapplicable authorization separately. Lack of authority evidence cannot delete the observed change, and the observed change cannot manufacture an authorized route or sustained capacity.

### W4-14: Shared model dataset at limited granularity

The candidate generator and judge each have explicit `trained_on` links to dataset D. Their free-text subset descriptors differ. No structured row-overlap evidence is supplied.

Expected: one shared dataset reference in that role-pair view, retaining both subset descriptors. No identical-training-data finding, zero overlap assertion or error-correlation coefficient is inferred.

### W4-15: A cycle with an exit

E1 and E2 have a claim-origin dependency cycle. Another eligible link reaches O1.

Expected: preserve the O1 incidence and the cycle witness. The seed remains unresolved/conflicted for complete-origin disposition and HHI stays unavailable. A cycle in a separate citation view would not itself invalidate an otherwise fully documented acquisition view.

### W4-16: Unsupported label and disputed identity

A declared `documented_origin` boundary has only an external locator. Two origin IDs additionally have an unresolved `same_identity_as` assertion.

Expected: preserve the declaration and locator-only support, with no documentary upgrade from the label. Identity ambiguity blocks distinct-origin qualification and the restricted HHI where relevant. Local record inventories remain available; no automatic merge occurs.

### W4-17: A recorded use without earlier stage logs

A PipelineRecord with supplied process evidence records that E1 influenced an output by a use log. Admission and preservation are not recorded; externality is unknown.

Expected: disclose the recorded use at its actual basis. Do not infer missing earlier stage events, independent reality contact, adequate replenishment or a causal effect magnitude. Lack of those other records does not erase the supported use record.

### W4-18: A scope change is not an isolated system improvement

Two inquiries have different seed populations: one includes ten derivative contributions and a disputed anomaly, while the other excludes the anomaly and several derivatives. Each reports its own coverage.

Expected: disclose the different seed selections and denominators. Neither reduced missingness nor a lower concentration in the second dossier is an unqualified before/after improvement. The source system may be unchanged; the represented audit population changed.

## 7. Capability prerequisites without a global quality ladder

WU4 specifies the following analytical prerequisite relationships. WU6 will turn these into the full capability matrix and final state vocabulary.

| Capability | Evidence sufficient for its own result | Evidence that it must not require unnecessarily |
|---|---|---|
| Supplied source inventory | Structurally valid inquiry and seed references | Fully resolved roots, source verification or correction logs |
| Recorded common ancestry | Eligible typed witness paths in the chosen scope | A global independent-source assessment |
| Qualified process-set count | An individual supplied comparison satisfying documentary and conflict checks | A blanket public identity disclosure |
| Restricted HHI | Complete single-origin seed rows, exact record buckets and coverage conditions | A claim that those buckets are statistically independent |
| Inherited-only layer fraction | Complete immediate-link classification or explicit completion interval | Fully resolved distant ancestry, when the immediate-copy structure is already established |
| Evaluator overlap | Relevant role bindings and recorded common object/ancestor paths | Complete source-acquisition ancestry for unrelated claims |
| A stage occurrence record | Applicable supplied stage evidence | Logs for all three other stages |
| A cohort fraction | Unambiguous anchor, complete enumerated cohort and per-member classifications | A global system-wide intake census |
| A declared correction route | Matching recorded route witness | Proof the route has ever been used |
| An applicable authorized route | Matching action/time/target grant evidence at every required leg | A completed correction case |
| An observed linked change | Case linkage and adequate before/after or removal evidence | A sustained-capacity measurement or fully resolved source roots |
| Tail-stage comparison | Explicit eligible cohort and stage evidence | Automatic semantic classification of rarity or viewpoint |

Failure of one capability is localized to its dependent fields. Final report sections must not suppress valid outcomes merely because an unrelated global level is low. Conversely, a detailed correction history cannot elevate unknown source ancestry to resolved status.

## 8. Specification acceptance obligations

Each family below has positive, negative, missing-data and boundary obligations. They are requirements for WU7-WU8 and later implementation, not executable tests completed in this phase.

| Contract | Positive obligation | Negative obligation | Missing-data obligation | Boundary obligation |
|---|---|---|---|---|
| SIT-M001 | Count explicit seed records by unit | Metadata-only ancestors do not enter seed totals | Explicit unresolved artifact references stay separate | Empty list gives record-count zero only |
| SIT-M002 | Preserve supported origin boundaries and witnesses | Parentless nodes do not become origins | Unqualified terminal remains visible | Baseline/scope-cut result remains labeled |
| SIT-M003 | Count members of a qualifying supplied assessment | No pairwise union or global independent total | Missing support makes qualified count unavailable | One origin without a comparison stays an origin |
| SIT-M004 | Preserve complete and partial per-seed origin sets | Do not normalize overlapping incidence | Unknown branches remain in N | Diamond paths count one origin; cycles retain a blocker |
| SIT-M005 | W4-01 yields exact 13/18 under the stated premise | Multi-parent or filtered-known HHI prohibited | W4-02 returns no scalar for full N | N = 0 unavailable; N = 1 and qualified yields 1 |
| SIT-M006 | Complete immediate-link profile yields stated fraction | Direct linkage does not mean independent acquisition | Unknown rows create interval, not dropped denominator | Mixed rows receive no fractional allocation |
| SIT-M007 | Count shared unresolved reference once | No hidden-root count from gap count | Coverage gap without an endpoint is still displayed | One gap may affect many seeds |
| SIT-M008 | Identify exact shared role-pair ancestor | Family label does not create an ancestry edge | Unknown training retains an unexamined dimension | Shared target differs from dependent checking method |
| SIT-M009 | Preserve externality with exact boundary/time | URL/recency does not create externality | Unknown grounding remains unknown | Admission may exist without externality |
| SIT-M010 | Complete keyed cohort yields reproducible counts | Different stage keys/runs cannot form a hidden funnel | W4-09 interval keeps all five members | Empty cohort has no fraction; duplicates do not add members |
| SIT-M011 | Match route, grant, action, target and time | Route does not prove effect | Partial coverage prevents universal no-route | Expired/mismatched grant cannot authorize another action |
| SIT-M012 | Count cases and linked target changes separately | Acceptance does not become success | Missing third change remains undocumented | Retraction uses explicit supported absence, not unknown after-state |
| SIT-M013 | Show substantive human contribution and its evidence | Model output/human label cannot manufacture human correction | Protected dependencies retain assurance limits | Execution remains a distinct constraint type |
| SIT-M014 | Preserve anomalies and eligible cohort comparisons | No motive or truth verdict from disagreement | Final-only dossier has no suppression rate | Unclassified anomaly is valid without a Claim match |
| SIT-M015 | Inventory declared basis and relevant support gaps | Complete citations do not imply complete model history | Locator-only support stays uninspected | Coverage declaration is attributed, never universal |

### 8.1 Metamorphic properties for future verification

Reordering set members or assertions must not change substantive results. Repeating a reference to the same ID cannot add origins. A second witness to O1 cannot increase root count. Adding a known unresolved seed cannot create a full-population HHI. Deleting a dependency witness cannot itself create a qualified independence assessment.

Changing a target Claim, selected dimension, seed set or count unit may change the answer, but the scope change must be explicit. Adding a valid correction record must not silently resolve unknown acquisition history. Withholding protected names must not create new independent origins from a known common reference.

These are specification properties over supplied data. They do not promise detection of secretly omitted real-world information or prove the underlying theories empirically.

## 9. Changes, pending gates and next stop

### 9.1 Current package

The incremental WU4 package contains exactly:

| File | Revision / role |
|---|---|
| `DEFINITIONS_AND_UNITS.md` | 0.2; retains WU3 definitions and adds §§19-29 analytical semantics |
| `OBSERVABILITY_AND_REPORTING.md` | 0.1; this analytical catalog and written checks |
| `V0.1_PRODUCT_SPEC.md` | 0.2; updates the release's diagnostic scope and explicit scalar exclusions |
| `UNRESOLVED_DECISIONS.md` | 0.4; preserves the previous twenty-one decisions and adds SIT-D022-SIT-D025 |

Use the new versions as working copies alongside the unchanged WU3 lineage specification and WU2 project instructions. Preserve the earlier ZIPs as history. Relative links are intended for that assembled working set, not a new standalone four-file project.

### 9.2 Decisions awaiting acceptance

SIT-D019-SIT-D021 remain pending detailed ontology/input choices. WU4 finalization is conditional on their acceptance. SIT-D022-SIT-D025 submit the additional analytical choices. No decision is silently approved by writing its recommended consequence into these files.

This unit stops after the documentation package. On acceptance, the next planned unit is WU5: `SOURCE_INTEGRITY_THREAT_MODEL.md`, with only its plan-authorized companion revisions. WU6 subsequently completes the reporting statuses and observability contract. Neither unit, the final Phase 0 approval nor Phase 1 is executed here.

## 10. Input identities and checks

The following hashes identify the exact inputs reviewed for this proposed extension. Their historical status headers remain unchanged. A file hash supplies byte identity only.

| Reviewed input | SHA-256 |
|---|---|
| `PHASE_0_PLAN_Source_Integrity_Toolkit.md` | `2d97a820ae218c33cfd00dd96a762853e887f867973a2b2da0945fc4414495b1` |
| `source-integrity-toolkit-phase0-work-unit1/SPEC_AUDIT.md` | `3565ab8f1b08f30e06f4983ffd26adbe8bc977b655ebf410b634918a7ae7949a` |
| `source-integrity-toolkit-phase0-work-unit1/THEORY_SOURCE_MAP.md` | `015e65baf3fcad8ce78a2285df8f2de8d5b7b4cbdd347707ba3cc5d5ba46b627` |
| `source-integrity-toolkit-phase0-work-unit2/PROJECT_INSTRUCTIONS.md` | `cb5cf8f4d367bceacc313189469b3327370bed0450468d62a968825fee4a7746` |
| `source-integrity-toolkit-phase0-work-unit2/V0.1_PRODUCT_SPEC.md` | `117c3ac96e6101508ff8cb643a94c3544cc111ba93dee054b2fafecb65c1db83` |
| `source-integrity-toolkit-phase0-work-unit3/DEFINITIONS_AND_UNITS.md` | `81290ac5b442bfbe17e8302a3cb9dbeb9312d0c752899aa32693885a056cf48a` |
| `source-integrity-toolkit-phase0-work-unit3/CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` | `8d697b6eb556bbe8476f59e48664996fe12003a42efdce179648d25d9ffb924f` |
| `source-integrity-toolkit-phase0-work-unit3/UNRESOLVED_DECISIONS.md` | `4c8611476bdb6151948284b77443958779d76d00b82f4a30e04af25928def32d` |

### 10.1 Scope of checks

The delivery is checked for its four-file allowlist, preserved input hashes, decision-ID continuity, source/product/diagnostic references, Markdown structure, links against the assembled specification set, exact arithmetic of the written examples and ZIP/file byte agreement.

The same assistant drafted and checked these files. No independent external review, production graph execution, source authentication, scientific experiment, runtime security test, CI run or GitHub write is claimed. The results of the local authoring checks are recorded after packaging verification in the final handoff.

### 10.2 Completed local document checks

The local authoring checks passed for the four-file allowlist and all sixteen read-only input hashes. The six theory PDF hashes agree with the WU1 source register. The WU3 numbered definition body is retained verbatim inside the new definition revision, and all twenty-one inherited decision bodies and their approval records are preserved. The sixteen core product requirement rows retain their original wording and IDs; their analytical realization and acceptance details are extended explicitly in this unit.

The catalog contains fifteen unique diagnostic families and eighteen numbered analytical witnesses. Identifier ranges, relative links in the assembled working set, UTF-8 text, heading uniqueness, table column widths and fenced-block boundaries were checked. Written rational-number examples, completion-interval endpoints and the proposed six-decimal presentation were checked with local arithmetic only. These checks do not execute a source-lineage or correction algorithm.

The delivery archive contains only the four listed Markdown files. Its member bytes are compared with the delivered copies when packaged; no earlier source document, theory PDF, implementation code or internal checking utility is included.

## 11. Work Unit 6 authority, approval record and specification ownership

### 11.1 Current instruction and acceptance scope

The user replied “可以，继续” to the Work Unit 5 delivery identifying SIT-D026 and SIT-D027 as its two submitted choices and WU6 as the next unit. This document records acceptance of **Option B for SIT-D026 and Option B for SIT-D027**, together with the WU5 threat/product extension, for continued Phase 0 design. The record is dated 2026-09-17; no precise approval time or separate signed instrument is asserted.

SIT-D001-SIT-D025 retain the dispositions and qualifications in decision-register revision 0.5. The accepted WU5 choices preserve fourteen threat families, seven auditor-control risks, evidence-bounded findings, residual fabrication risk, and the non-detector/non-intervention boundary. They do not approve a runtime control, security certification or a new implementation phase.

The WU6 allowlist contains only this file, `CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` and `SUCCESS_CRITERIA.md`. Accordingly, `UNRESOLVED_DECISIONS.md` revision 0.5 is unchanged. This acceptance record is the scoped supplement to its historical pending entries and must be carried into the next authorized register update. No approval is backdated into an earlier file.

### 11.2 Current contract and retained material

Sections 1-10 above preserve the WU4 numbered body verbatim, including its historical status and then-future assignments. Its fifteen analytical contracts, eighteen analytical witnesses, definitions and exclusions remain the substantive baseline. Sections 11-24 complete the reporting tasks that body reserved for WU6. Historical references to pending WU3/WU4 approval are superseded only by the actual approval records, not by rewriting their source text.

This unit submits the exact reporting realization for review. Local review packages WU6-C01 through WU6-C03 in §23 identify the new choices within WU6's assigned scope. They are not new entries or renumberings in the central SIT-D register. No new metric, source inference, threat detector, input record or predicate is selected.

| Responsibility | Owning document and current meaning |
|---|---|
| Terms, units, qualification, populations and arithmetic | `DEFINITIONS_AND_UNITS.md` revision 0.2, especially §§19-28 |
| Input fields, enums, edges, scope and structural rejection | `CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md`, retained §§1-17 |
| Threat mechanisms, narrow reportable conditions and residual risks | `SOURCE_INTEGRITY_THREAT_MODEL.md` revision 0.1, accepted through SIT-D026-SIT-D027 |
| Output states, evidence prerequisites, capabilities and logical report shape | This document §§12-22 |
| Input-to-output semantic bridge | Lineage specification §§18-22 added in WU6 |
| WU6 acceptance obligations and remaining phase gates | `SUCCESS_CRITERIA.md` revision 0.1 |

### 11.3 Source basis and operationalization boundary

The documentary requirements continue to use SIL pp. 7, 11-16; EC §§6-7 and 10; HDL §§4.6, 9, 10.5 and 11; and UIL pp. 8-9 and 15-16. In particular, the four governance functions in SIL's p. 13 table remain distinct from the observability labels below. EC's five joint conditions cannot be replaced by an average of available outputs. HDL's four replenishment stages require separate evidence. [SIT-T004, SIT-T006, SIT-T022-SIT-T026, SIT-T029, SIT-T031-SIT-T032]

The state codes, report paths, evidence checklist and five navigation labels below are **toolkit operationalizations**. They are not quoted definitions or validated measurement scales from those papers. No external standards, vendors, political cases or empirical study results are updated in this unit. [SIT-T035-SIT-T040]

## 12. Observable evidence, qualified results and processing states

### 12.1 The three questions stay separate

Structural acceptance concerns the local input contract. Analytical availability concerns whether a particular result can be supported. Substantive truth concerns the world described by the input. A successful parse establishes only the first. A completed calculation does not authenticate its premises.

The report therefore uses separate axes for processing, result availability and evidentiary basis. No axis is named `integrity_status`, `truth_status`, `source_pass` or `trust_level`.

### 12.2 Run outcome contract

`report_kind`, `run.processing_state` and `input_validation.state` have exactly the following combinations:

| `report_kind` | `run.processing_state` | `input_validation.state` | Permitted content |
|---|---|---|---|
| `audit_report` | `completed` | `accepted` | Every requested in-scope capability has a completed availability decision; legitimate unavailable results remain explicit |
| `audit_report` | `interrupted` | `accepted` | Only independently finished results may remain available; unfinished cells identify interruption and make no absence claim |
| `validation_diagnostics` | `rejected` | `rejected` | Structural error diagnostics only; no analytical results, levels or source findings |
| `processing_diagnostics` | `interrupted` | `not_completed` | Validation/processing interruption without accepted-input status; no analytical results |
| `processing_diagnostics` | `failed` | `accepted` or `not_completed` | Execution failure diagnostics; no ordinary analytical report or recycled values from an earlier attempt |

A completed run can legitimately contain unavailable metrics because the evidence is sparse. An interrupted run cannot use unavailable evidence as an explanation for an unfinished computation. An implementation defect is `failed`, not an epistemic unknown. Unknown or unsupported input-contract versions are rejected under the existing input rules.

The default future audit attempts all fifteen in-scope families for the supplied inquiries and their applicable scopes. If a later approved interface permits a request subset, its selection must be recorded; it cannot remove required release capabilities. This unit supplies no command syntax, request option, new input selection key or optional escape from implementing SIT-M001-SIT-M015.

### 12.3 Per-result execution and availability

Each atomic `Result` has two independent fields:

| Field | Values | Meaning |
|---|---|---|
| `execution_state` | `completed`, `not_performed`, `interrupted`, `failed` | Whether this result's prescribed operation finished |
| `result_state` | `available`, `unavailable`, `not_applicable`, `not_evaluated` | Whether a supported value exists for this exact question |

Allowed pairings are:

- `completed` with `available`, `unavailable` or `not_applicable`;
- `not_performed`, `interrupted` or `failed` with `not_evaluated` only.

`available` means that the value is supported **at its stated scope and basis**. An available inventory count may be zero. An available collection of attributed assessments may contain unknown, denied or failed outcomes. An available finite-cohort interval still contains unresolved classifications. None is a favorable quality verdict.

`unavailable` means an applicable requested value cannot be established from this payload. Its value is null and its reasons identify the failed or unknown prerequisites. `not_applicable` requires a structural explanation that the question has no applicable subject in the selected scope. It cannot be inferred from missing records, incomplete roles or unknown external history. Such cases are unavailable or receive an explicit no-eligible-subject disclosure.

`not_evaluated` records unperformed or unfinished work. It never means that a threat, dependency or correction was absent. An in-scope capability cannot be called outside-release merely because it has not yet been implemented.

### 12.4 Atomicity and localization

Results are atomic with respect to their value and prerequisites. A complete record inventory and an unavailable qualified subset count must be separate results. An exact stage partition, unavailable point fraction and available completion interval likewise have separate entries.

A parent capability row links these results; it does not inherit the state of its best child. A disputed origin can block HHI while leaving artifact counts, a witnessed common ancestor, a documented correction and a pipeline-use record available. There is no file-wide `unknown` flag that suppresses all useful observations.

If processing stops, a previously finished inventory may remain available only if its full input population was frozen and processed. A partly visited origin set is unfinished, not an exact origin count. Partial witnesses may be retained only as already completed, explicitly scoped witness results. No incomplete traversal becomes a completed no-path or zero-overlap result. [SIT-TS005; SIT-D027]

### 12.5 Evidentiary origin and premise qualification

Every Result declares `result_origin` as one of `inventory`, `graph_derivation`, `attributed_record` or `qualification_check`. These categories describe how this output was obtained. They are not confidence ranks.

The underlying `Provenance.basis_kind` values remain unchanged: `declaration`, `documented_record`, `upstream_inference`, `protected_attestation`, `unspecified`. A result's `basis_refs` identify the records and assertions it uses. Mixed bases remain a list, never a highest-basis upgrade. Documentary qualification is accompanied by its checks, method, supporting references and limitations.

An EvidenceReference having an external locator remains uninspected by the runtime. A supplied excerpt is caller-supplied material. An opaque protected attestation identifies what can be examined and what is withheld. A supported upstream inference remains an upstream inference. None of these is renamed independent verification. [SIT-M015; SIT-TS003]

## 13. Prerequisite checks and reason vocabulary

### 13.1 Check representation

A `PrerequisiteCheck` contains a report-local `id`, its registry `check_id`, `scope_ref`, `state`, `input_refs`, `reason_refs` and `note`. Its state is `met`, `unmet`, `unknown` or `not_applicable`. `met` means the documentary/structural prerequisite is met under the supplied basis; it does not authenticate the outside event.

A missing coverage assertion is `unknown`. A supplied record proving that an explicit grant is for a different action can make that route's action match `unmet`. A safely processed declaration-only origin can make the documentary requirement unmet while origin identity remains a recorded fact. Keep these reasons separate.

| Check ID | Question | Owning rule |
|---|---|---|
| PC01 | Was the complete bundle structurally accepted? | Lineage §§2-9, 13-14 |
| PC02 | Are the exact inquiry, Claim version, subject, dimension and view identified? | Definitions §20; lineage §§5, 7, 10 |
| PC03 | Is the required seed/comparison/target population explicitly identifiable? | Definitions §§20-21, 27 |
| PC04 | Are the relied-on typed relations active, affirmed and scope-compatible? | Lineage §10.1; definitions §20.4 |
| PC05 | Is the required supporting basis supplied and non-self-certifying? | Lineage §§3-4; definitions §20.4 |
| PC06 | Does relevant coverage address the required finite dependency area? | Definitions §20.6 |
| PC07 | Are documentary origin boundaries qualified in the selected dimension? | Definitions §21.2; lineage §9.1 |
| PC08 | Is identity sufficiently resolved for the particular qualified statistic? | Definitions §23.1; lineage §12.2 |
| PC09 | Is the necessary premise free of a relevant unresolved conflict? | Lineage §12; definitions §§20.4, 26.2 |
| PC10 | Does the explicit snapshot/time basis support this temporal claim? | Definitions §20.5; lineage §§3.1, 10.7 |
| PC11 | Does one supplied comparison assessment satisfy its full qualification? | Definitions §21.3; lineage §9.2 |
| PC12 | Do all seeds satisfy the complete single-origin HHI gate? | Definitions §23 |
| PC13 | Is the immediate EvidenceItem-link enumeration sufficient for its profile? | Definitions §24 |
| PC14 | Are applicable evaluator roles, subjects and dimensions represented? | Definitions §25.1; lineage §6.7 |
| PC15 | Is externality grounded against the exact declared system boundary? | Definitions §25.2; lineage §9.6 |
| PC16 | Is the target run/stage key unambiguous and the finite cohort enumerated? | Definitions §26.1 |
| PC17 | Are the cohort's individual stage classifications established? | Definitions §26.2 |
| PC18 | Is there one eligible evidenced admission-to-target comparison? | Definitions §26.4 |
| PC19 | Does a finite declared correction route match this channel/target/action? | Definitions §27.1; lineage §11.1 |
| PC20 | Are all required route grants, scope and time applicable and supported? | Definitions §27.1; lineage §9.7 |
| PC21 | Does a case-linked change have qualified before/after or removal evidence? | Definitions §27.2; lineage §6.9 |
| PC22 | Are human contribution, process identity and dependency limits disclosed? | Definitions §25.3; lineage §6.7 |
| PC23 | Are anomaly/contestation context and any eligible baseline retained? | Definitions §26.5; lineage §6.11 |
| PC24 | Has the operation processed the whole population required for this value? | This document §§12.2-12.4; SIT-TS005 |

Checks are evaluated per result scope. PC12 is the HHI gate, not a prerequisite for all ancestry output. PC18 is unnecessary for a standalone influence-use record. PC20 is unnecessary for reporting a separately documented historical change. PC06 is required for an exhaustive negative or complete set, not for every positive witness.

### 13.2 Reason objects

A `Reason` contains `id`, `code`, `scope_ref`, `affected_result_refs`, `input_refs`, `detail` and `classification`. `classification` is `evidence_gap`, `conflict`, `structural_inapplicability`, `release_boundary` or `execution`. It does not express severity. Every unavailable/non-evaluated result has at least one reason. Relevant nonblocking limitations can also be attached to available results.

Codes are a closed reporting vocabulary for this proposed version. Several codes can apply; sorted presentation creates no priority or winning cause.

| Code | Required distinction |
|---|---|
| `no_seed_contributions` | No explicit EvidenceItem seeds for this Claim; zero source observations in reality is not implied |
| `zero_denominator` | A known empty counted population prevents a ratio or interval |
| `missing_comparison_assessment` | No applicable supplied independence comparison; never a zero independent-source estimate |
| `scope_unestablished` | The necessary target, claim, dimension or selected record scope cannot support this result |
| `dimension_not_selected` | The inquiry did not select this dependency dimension |
| `unknown_endpoint` | A typed UnresolvedReference stops the affected trace |
| `upstream_coverage_incomplete` | Required upstream enumeration is partial, unsupported or absent |
| `unqualified_origin_boundary` | A terminal or labeled boundary lacks the necessary qualified origin basis |
| `baseline_or_scope_cut` | A branch ends at a deliberate reference baseline/scope cut |
| `declared_origin_only` | A branch ends only at a declared origin |
| `multi_origin_unallocated` | Known multiple origins have no adopted quantitative allocation |
| `identity_unresolved` | Alias, same-identity or conflicting identity evidence blocks this statistic |
| `premise_disputed` | A necessary relation, assessment, stage or identity has a relevant unresolved contrary statement |
| `lineage_cycle` | A selected dependency view contains unresolved cyclic ancestry |
| `support_uninspectable` | Needed support is locator-only, unavailable, entirely withheld or otherwise not supplied |
| `documentary_basis_incomplete` | Needed asserter/attestor, method or supporting basis is missing |
| `self_supporting_assurance` | Self-pointers or a closed support loop cannot provide sole documentary support |
| `time_applicability_unknown` | A time-specific requirement lacks an established effective time/history |
| `temporal_inconsistency` | Supplied known times contradict the required ordering |
| `roles_incomplete` | Necessary evaluator bindings/role evidence are unknown or missing |
| `externality_unestablished` | No qualifying boundary/grounding assessment supports the requested externality claim |
| `cohort_anchor_missing` | No eligible exact run/stage-key anchor exists |
| `cohort_anchor_ambiguous` | Competing anchors prevent one target-stage choice |
| `cohort_universe_unestablished` | Enumeration, members or eligibility boundary do not satisfy the finite-cohort rule |
| `stage_classification_unresolved` | One or more stage members retain a missing, unsupported or disputed classification |
| `transition_baseline_unestablished` | The admitted baseline is missing, ambiguous, not fully evidenced or not the same member set |
| `route_not_recorded` | No eligible route witness exists in the supplied view; does not assert global impossibility |
| `authority_unestablished` | The needed grant/authority evidence is missing or unsupported |
| `authority_inapplicable` | Supplied grant scope/action/time explicitly does not match the required route |
| `change_evidence_missing` | No sufficiently linked downstream change is supplied |
| `before_after_unresolved` | Before/after identity or supported removal remains unestablished |
| `context_withheld_or_unavailable` | Context is protected or absent; preserve a permitted reference and its limits |
| `no_applicable_subject` | There is no applicable represented subject for this question, with scope explanation |
| `outside_v01` | The requested substantive inference/detector is excluded from this release |
| `analysis_not_selected` | A separately authorized request omitted this analysis; no implied finding |
| `resource_limit_reached` | Processing stopped at a declared runtime limit; exact limits are WU9 work |
| `execution_failed` | A runtime operation failed; do not reclassify the defect as evidence missingness |
| `input_not_accepted` | Structural rejection or unfinished validation prevents analytical reporting |
| `completion_interval_not_needed` | An exact eligible point fraction has no unresolved members; the missing-classification interval is inapplicable |
| `comparison_scope_mismatch` | A proposed comparison changes a required unit, population, claim, time or qualification |

A code can summarize several detailed gaps only when each affected reference remains traceable. Any new reason affecting semantics requires a contract revision; source text cannot define new core reason codes through extensions.

## 14. Complete capability matrix

### 14.1 Matrix interpretation

Every audit includes one matrix entry for each SIT-M001-SIT-M015 family and inquiry, even when it has no eligible subject. Applicable detailed entries are keyed by the actual claim/dimension, assessment, role pair, stage cohort or correction tuple. No all-pairs world query is inferred.

A matrix entry identifies the required checks, links every available/unavailable/not-evaluated atomic result and explains absent subject scopes. It cannot merely display a green tick for a family containing both an inventory and an unavailable stronger result.

All matrices below assume PC01 and PC24 for a completed output. Counts can be available at inventory basis while a stronger complete-population inference fails. Referenced check numbers identify the relevant questions, not an instruction to require every check for every leaf in the family.

| Family / detailed key | Required evidence and checks | Available outputs when prerequisites hold | Retained weaker output or honest non-result |
|---|---|---|---|
| SIT-M001 / inquiry, and Claim for contribution counts | Explicit seed positions and valid bindings; PC02-PC03 | Five seed/artifact/contribution counts from definitions §21.1 with exact member sets | Artifact-only inventory is valid; missing claim contributions do not become zero independent sources |
| SIT-M002 / Claim + dimension | Eligible origin paths and each boundary's scope/basis; PC02-PC10 as relevant | Reached-origin count; boundary inventory; qualified boundary count only when its qualification is established | Reached records, declared boundaries and unsupported terminals remain visible; no original observation invented |
| SIT-M003 / one assessment + dimension | Exact pair/set, process evidence, coverage, identity, time and conflict checks; PC02-PC11 | Submitted comparison size and eligible qualified member counts per assessment | Preserve the assessment and its stated conclusion; qualified count unavailable for failed qualification; no pairwise union |
| SIT-M004 / Claim + dimension + full seed set | All per-seed traces with scoped completeness/boundaries; PC02-PC10 | Per-seed origin sets, five exhaustive dispositions, incidence counts, documentary resolution fraction for N > 0 | Known branches and all unresolved seeds remain in N; nonexclusive incidence is never normalized into source weights |
| SIT-M005 / same full scope as M004 | Every HHI condition in definitions §23; PC02-PC12, PC24 | Exact restricted HHI and origin-bucket counts | Null scalar with all blockers; no multi-parent split, known-only fallback or hidden effective-root count |
| SIT-M006 / Claim + dimension + immediate-link scope | Immediate E-to-E/E-to-origin enumeration and basis; PC02-PC06, PC08-PC10, PC13 | Four-row partition; exact fraction if U = 0; optional completion interval if U > 0 | Distant ancestry need not resolve immediate inheritance; no semantic novelty claim |
| SIT-M007 / Claim + dimension | Explicit frontier/gap records and affected completed traces; PC02-PC04 | Represented frontier, terminal and affected-seed counts/lists | Number of concealed origins remains unknown; one shared gap is one represented endpoint |
| SIT-M008 / Evaluation + two actual roles + view/dimension | Recorded role bindings and relevant typed history; PC02-PC10, PC14 | Shared-role identity, strict common ancestors, one-sided ancestry and exact family-label matches, separately | Zero matches only within examined records; role/training/rubric gaps remain; no independence from disconnection |
| SIT-M009 / externality assessment + subject + boundary | Externality assertion, relevant boundary, time and evidence; PC02, PC05, PC09-PC10, PC15 | Attributed assessment and its qualification, linked to separate stage evidence where present | No externality inferred from a date, human label or pipeline admission; scalar Presence excluded |
| SIT-M010 / run + stage key + stage, plus explicit cohort/comparison | Individual PipelineRecords; for ratios PC16-PC17; for transition PC18 | Individual observations; eligible T/Y/F/U partition; exact fraction or completion interval; restricted transition if qualified | No cohort means observation inventory only; influence can be shown without earlier logs; no multiplied funnel |
| SIT-M011 / channel + exact target + action + time | Declared route witness; applicable grants for stronger route; PC02, PC04-PC06, PC09-PC10, PC19-PC20 | Declared witness and separately applicable authorized-route evidence | Missing path in partial coverage stays bounded to that view; no correction effect or capacity inferred |
| SIT-M012 / case and its selected targets | Case links, handling and before/after/removal evidence; PC02-PC05, PC08-PC10, PC21 | Five record/process counts from definitions §27.2; supported target changes; all handling outcomes | Missing third change is undocumented, not failed; authority may remain unknown without erasing the observed change |
| SIT-M013 / corrective Evaluation/process comparison | Qualified comparison where present, substantive human contribution and dependency limits; PC02, PC05, PC08-PC11, PC14, PC22 | Attributed corrective-process assessment and human-contribution disclosure | Human presence alone supplies no independence or renewable-judgment score; execution remains a different constraint |
| SIT-M014 / anomaly/contestation, and eligible cohort key | Original context or protected reference; supplied stance/conflict; cohort rules for ratios; PC02, PC05, PC09-PC10, PC16-PC18, PC23 | Context-preserving anomalies/disagreements; eligible stage exclusions and retention profiles | An unclassified anomaly can have no Claim; final-only material cannot establish suppression or its motive |
| SIT-M015 / explicitly named record/reference/coverage population | Original provenance and availability fields plus their support checks; PC02-PC06, PC09-PC10 | Attributed coverage by kind; basis and availability inventories; exact qualification gaps | An unsupported documentary label remains reported as that supplied label with its missing basis; no provenance-quality percentage |

### 14.2 Scope dependencies that must remain independent

A positive common-origin witness does not require a global independence assessment. A qualified comparison-member count does not require every source outside that comparison to be resolved. The restricted HHI requires complete single-origin seed coverage but does not require the buckets to be independently acquired. These outputs answer different questions.

A pipeline stage record does not require an externality assessment. An externality assessment does not require a completed correction. A documented linked change does not require fully resolved acquisition ancestry or prior authority, although those missing properties remain disclosed. A factual disagreement about the target Claim alone does not necessarily dispute its acquisition paths.

A scope conflict affects the claims, fields and dependency dimensions it actually concerns. Metadata irrelevant to a value cannot block it just because it appears elsewhere in the file. The audit must also avoid the converse error of dropping a directly relevant unsupported denial to rescue a desired number. [SIT-D024-SIT-D027]

### 14.3 Negative evidence and absence matrix

| Situation | Available conclusion | Prohibited conclusion |
|---|---|---|
| Zero matches after a finished traversal of partial supplied history | No eligible witness was found in that examined view, with partial coverage | No dependency exists outside the dossier |
| Zero matches plus supported complete coverage for the exact finite view | No matching relation under that attributed coverage and scope | Universal independence or permanent impossibility |
| Explicit evidence-bearing `did_not_occur` for one stage/key | That source records non-occurrence for that member/key | Every stage failed, or the observer independently verified all events |
| Missing stage record | Classification unresolved | `did_not_occur` |
| Missing change after accepted handling | Change evidence unestablished | Failed correction |
| Enumerated empty inventory | Zero records of that selected kind | Zero real-world sources or threats |
| Unfinished traversal | Operation interrupted, no completed no-witness result | Zero matches |
| No active content detector in v0.1 | Content-level detection outside release | Source passed injection/poisoning inspection |

## 15. Five observability labels without a score ladder

The plan's Level 0-4 vocabulary is retained as **navigation over evidence domains**. It is non-cumulative. A report may have correction-outcome evidence while acquisition ancestry is unresolved. It may have complete ancestry showing extensive dependence. Neither case can be summarized by a maximum quality level.

| Label | Evidence domain | Typical results | What the label never grants |
|---|---|---|---|
| Level 0 | Artifact and contribution inventory | M001 and base record/reference inventories | Authentic source identity or independence |
| Level 1 | Declared provenance and process metadata | M002 declared paths/boundaries, M006 direct/inherited disclosures, M007 gaps, M015 | Documentary qualification solely from metadata labels |
| Level 2 | Origin-resolution and scoped process-assessment evidence | M002-M005 and relevant M006 results with qualified premises | A universal independent-root total or source truth |
| Level 3 | Evaluator, correction-route and authority evidence | M008, M011, M013 and associated M015 qualifications | Actual correction from a route, or independence from a job title |
| Level 4 | Boundary-qualified external input, stage histories and documented correction outcomes | M009-M010, M012, eligible M014 stage evidence | Global adequacy, live monitoring, causal effect or sustained capacity |

Each report includes five `observability_domains` entries with `level_index`, `label`, `available_result_refs`, `unavailable_result_refs`, `not_evaluated_result_refs` and `reason_refs`. Links can appear in more than one domain when a family has several kinds of evidence; the result itself is not duplicated.

There is no `overall_level`, `max_level`, maturity grade, badge, ranking, green/red quality score or arithmetic over domain numbers. The absence of Level 2 results cannot suppress an independently evidenced Level 4 change record. Level 4 means the supplied dossier contains examinable process evidence; the offline toolkit has not observed a live system itself. [SIT-T038; SIT-P012]

## 16. Logical report envelope

### 16.1 Reserved contract and root fields

The proposed logical label is `sit-report/0.1`. It is reserved specification text, not a published schema, package version or compatibility claim. JSON and Markdown represent one logical report.

| Root field | Content / rule |
|---|---|
| `contract_version` | Exact report contract label |
| `report_kind` | One of the three kinds in §12.2 |
| `report_id` | Identifier local to this emitted report; no truth or signature meaning |
| `run` | Processing state, actual tool/version identity when implemented, requested/evaluated capabilities, start/end TimeValues if recorded, interruption/error notes |
| `input_identity` | Source mode, raw file digest where actually computed, input contract, bundle/snapshot IDs and declared predecessor as available |
| `input_validation` | Structural state and safely described diagnostics |
| `scopes` | Explicit result-scope objects for accepted input |
| `populations` | Explicit counted/compared member sets with unit, selection rule and coverage |
| `basis_index` | Relevant supplied premise metadata, evidence-reference availability and documentary check outcomes |
| `capabilities` | Entries covering M001-M015 and their applicable scoped operations |
| `checks` | Scoped prerequisite-check instances with report-local identities |
| `observability_domains` | The five non-cumulative navigation entries |
| `results` | Atomic values or explicit non-results |
| `findings` | Narrow witnessed observations, scoped absences, attributed records, gaps and conflicts |
| `reasons` | Structured reasons/limitations referenced by results and capabilities |
| `release_limits` | The fixed exclusions necessary to interpret the report |

For rejected or processing-diagnostic envelopes, `scopes`, `populations`, `basis_index`, `capabilities`, `checks`, `observability_domains`, `results` and `findings` are empty. Safe validation/processing diagnostics remain in `input_validation` and `run`. This prevents partially parsed data from appearing as an ordinary analytical audit. Claims about the rejected file's contents must not be inferred from those empty arrays.

`input_identity` records parsed bundle/snapshot identifiers only when available and labels them unaccepted when validation failed. A local file digest can use SHA-256 over the bytes actually read, with algorithm and covered-material description. It authenticates no source. For an in-process payload with no raw file, the raw-file digest is null with an explanation; this unit does not invent a canonical-object hash or reconstruct file bytes. WU9/WU10 own concrete privacy, I/O and canonicalization choices before implementation.

Source metadata cannot set `report_kind`, processing state, contract version, tool identity, authoritative timestamps or release limits through free text. Imported source documents can mention those words only as data.

### 16.2 Scope objects

A `Scope` has `id`, `inquiry_ref`, `claim_refs`, `target_refs`, `dependency_dimension`, `graph_view`, `temporal_basis`, `requested_time`, `coverage_refs`, and `qualifications`.

`claim_refs` identifies exact Claim records; it can be empty only for inquiry-level metadata or an unclassified anomaly as allowed by the input. Empty never means every Claim. The dimension is one of the five input dimensions or null with the structural explanation that the result is an inventory/other non-dimensional object. View names follow lineage specification §10 and are serialized as the named views in its WU6 bridge, §18.2.

`temporal_basis` is `snapshot_structural` or `time_specific`. In the first case, current active snapshot assertions are examined and unknown effective time is disclosed. In the second, the requested time and applicable lifecycle/coverage/grant evidence must be supplied. Known source times retain their precision and offset through TimeValue. An audit timestamp cannot fill a missing occurrence time.

Assessment-specific results identify the assessment ID in `target_refs`. Evaluator comparisons identify the Evaluation, exact role names and bound objects in their result payload. Correction-route results identify channel, target, action and time together. Stage results retain Inquiry, run key, stage key and stage. A parent section title cannot silently supply omitted scope.

### 16.3 Population objects

A `Population` has `id`, `scope_ref`, `unit`, `member_refs`, `selection_rule`, `coverage_refs`, `basis_refs`, `membership_state` and `qualifications`.

`membership_state` is `enumerated_for_scope` or `unestablished`. An established empty inventory has an empty member list and `enumerated_for_scope`. An unknown cohort has `unestablished`; it cannot acquire a ratio denominator from an empty list. Members are unique within their declared counting unit.

`selection_rule` names the fixed rule from definitions §§20-28, such as `E(I,C)`, `A(I)`, a specific independence assessment, a role-pair ancestry set or an anchored pipeline universe. It is descriptive contract text, not an executable filter. A subset chosen by a different Inquiry is a different Population. Unknown members or branches are identified in result limitations without quietly removing their parent seed from N.

For distinct correction-target counts, a member is the documented `(case_ref, before_ref)` pair, not a bare target name or a handling-event ID. For population types whose members use structured pairs, the `unit` and fixed tuple fields declare that structure. An array of source IDs cannot substitute for those pairs.

### 16.4 Result objects

A Result contains exactly the following core members; later executable-schema work cannot omit their meaning:

| Member | Requirement |
|---|---|
| `id` | Report-local Result identifier |
| `diagnostic_id` | One SIT-M001-SIT-M015 family |
| `field_key` | Canonical output family/leaf from §17 |
| `scope_ref`, `population_refs` | Exact scope and any selected populations |
| `execution_state`, `result_state` | Allowed pairing from §12.3 |
| `result_origin` | One of the four evidentiary-origin categories |
| `value_kind`, `value` | Typed value in §16.5, or null for a non-result |
| `check_refs` | The prerequisite outcomes used for this value |
| `basis_refs`, `witness_refs` | Supplied-basis entries and report-local finite witnesses as applicable |
| `reason_refs` | All blocking and material nonblocking limitations |
| `interpretation_limit` | Required bounded statement of what this value does not establish |

`available` requires a value of the declared kind. Empty collections and zero counts are permitted only for completed explicit inventories or similarly defined finite sets. All other states require `value = null`. No count sentinel, blank value, NaN, infinity or negative missingness code is allowed.

A derived count of a qualified set names that exact set. An unavailable global independent-source count must not be emitted because such a global field is outside v0.1 altogether. M003 instead emits the correctly scoped comparison output or its non-result.

### 16.5 Value forms and numerical exactness

| `value_kind` | Shape / interpretation |
|---|---|
| `count` | Nonnegative integer; explicit unit and member population required |
| `fraction` | Integer `numerator`, positive integer `denominator`, optional six-place `display_decimal`; population/witness rule retained |
| `completion_interval` | `lower` and `upper` fractions, shared population, and `interval_kind` equal to `finite_record_completion` or `finite_cohort_completion` |
| `partition` | Explicit exclusive categories with member references, integer counts and total population |
| `incidence` | Nonexclusive member-to-origin memberships and counts; `nonexclusive = true` |
| `record_disclosures` | Ordered references and selected original record fields preserving attribution and qualification |
| `witness_collection` | Finite scoped witness references; no inferred outside-world completeness |

HHI uses `fraction` with the numerator `sum(n_r^2)` and denominator `N^2`; its basis also retains N and every bucket n_r. For N = 6, the structural representation is 26/36, and 13/18 may be shown as an equivalent reduced expression. Reduction must not conceal the seed-count denominator or the bucket data. For ordinary fractions use the original finite population denominator even when reducing the display.

A completion interval has endpoints from the same T or N and retains Y/F/U or D/O/M/U. It is not labeled a confidence, probability or credible interval. The point result is unavailable while its optional interval may be available. Optional presentation does not authorize replacing an available exact fraction with an interval or treating unresolved observations as established negatives.

Values are exact integers/rational forms. An optional decimal uses the existing six-place decimal half-up convention. Native JSON booleans are not valid integer counts. A consumer unable to retain an exact integer must reject the incompatible presentation rather than round silently; the concrete portable large-integer/resource policy remains WU9/WU10 work. No illustrative document arithmetic selects an implementation library.

### 16.6 Basis index and input references

Input references and report-local references occupy distinct typed namespaces. An input reference contains its input collection kind and snapshot-local ID, with a named field/role selector when necessary. A report-local reference points only to a Scope, Population, Result, Finding, Reason, PrerequisiteCheck, Capability or basis entry of this report. String collisions between these namespaces cannot merge objects.

A `basis_index` entry has a report-local `id` and identifies the source record/assertion/reference, original basis kind, asserter or protected-attestor reference, method, support reference IDs, availability, applicable scope/time, lifecycle and qualifications relevant to the result. It also links prerequisite outcomes for documentary qualification. It does not silently copy every source excerpt into the public-looking report.

Canonical record links, including an EvidenceItem's claim/artifact binding and Evaluation role bindings, are cited by record ID plus field/role and target identity. They do not need invented RelationAssertions. Reordering input arrays cannot change their semantic identity. A method's prose is not a dependency rule. Exact export permissions, redaction, retention and safe path controls remain WU9 gates.

### 16.7 Capability entries and result references

A `Capability` contains `id`, `diagnostic_id`, `inquiry_ref`, `scope_refs`, `check_refs`, `result_refs`, `available_result_refs`, `unavailable_result_refs`, `not_applicable_result_refs`, `not_evaluated_result_refs`, `reason_refs` and `scope_note`. The four state-specific reference lists partition `result_refs` and agree with each referenced Result. They never summarize the family by its strongest result.

Where no detailed subject can be derived, the inquiry-level entry identifies the missing subject scope and the appropriate non-result or explicitly empty record inventory. All fifteen diagnostic IDs remain listed. Disclosures must not silently create comparison cohorts, role pairs or route tuples outside the supplied contract. Report-local IDs are unique across all derived collections; input-reference namespaces remain separate.

Each PrerequisiteCheck is scoped to its actual field/subject question. Several instances can share PC06 while addressing different histories. A single globally met coverage check cannot authorize every field. Nonblocking check outcomes can remain linked to available results with their reason references.

A positive route witness can be available despite unrelated incomplete routes. A requested exhaustive authorized-route conclusion requires the appropriate coverage and authority evidence. An empty fully examined witness set can describe a bounded recorded absence; unknown required grants instead leave the stronger authorized-route answer unavailable. Record inventories and scoped no-witness findings remain separately displayable. Unknown outside-world routes are never assigned a numerical zero merely because no witness was supplied.

When an eligible fraction is exact and has no unresolved members, its completion-interval field is `not_applicable` with `completion_interval_not_needed`. When the same population has unresolved members, the point fraction is unavailable and the permitted interval may be available. When the population is empty or unestablished, neither point nor interval receives a fabricated endpoint.

### 16.8 Run metadata and safe diagnostics

`run` contains `processing_state`, `tool_name`, `tool_version`, `input_contract_version`, `requested_diagnostic_ids`, `completed_diagnostic_ids`, `started_at`, `finished_at`, `diagnostics` and `qualifications`. When implemented, tool identity and times describe the actual execution. Missing times use TimeValue rather than invented values. A diagnostic family is listed completed only when all of its requested scope cells have finished their availability decisions. A legitimately unavailable value does not prevent completion of that decision.

`input_validation` contains `state` and `diagnostics`. Each diagnostic has `code`, `location`, `safe_message` and `qualifications`. A location is a safe field/identifier reference or null; it does not dump the payload. Structural code meanings map to the existing rejection table: `invalid_syntax`, `duplicate_key`, `unsupported_input_contract`, `duplicate_identifier`, `dangling_reference`, `type_or_enum_violation`, `missing_required_field`, `endpoint_or_claim_mismatch`, `invalid_time`, `input_constraint_violation`. The last code must cite the specific existing contract condition; it cannot reject a valid unresolved/conflicted record for convenience. Resource interruption and execution failure use their separate execution diagnostic meanings.

`input_identity` contains `source_mode` (`local_file` or `in_process`), `input_contract_version`, `bundle_id`, `snapshot_id`, `declared_predecessor`, `raw_file_digest` and `qualifications`. A digest has `algorithm`, `value` and `covered_material`; raw bytes may be fingerprinted even if later validation rejects them, without certifying their content. Identifiers unavailable before parsing remain null with the limitation stated. This metadata does not expose the full local input path by default.

`release_limits` states the fixed offline/caller-supplied basis, absence of external authentication and live monitoring, no active content detectors, no universal truth/integrity/safety score, no automatic intervention, and remaining scope-specific limitations. These are versioned product statements supplied by the tool, never imported from an untrusted source's text.

## 17. Output leaf catalog and native-state preservation

The following fixed field keys instantiate the existing M-family meanings. They add serialization names, not additional metrics. A profile payload is a finite disclosure of its defined records; it cannot contain an unregistered quantitative score.

| Family | Canonical `field_key` values and kinds |
|---|---|
| M001 | `nominal_seed_artifact_record_count`, `unresolved_seed_artifact_reference_count`, `seed_evidence_item_count`, `claim_artifact_record_count`, `claim_unassigned_seed_artifact_record_count`: count |
| M002 | `reached_origin_record_count`, `documentary_origin_boundary_record_count`: count; `origin_boundary_disclosures`: record_disclosures |
| M003 | `submitted_comparison_member_count`, `qualified_process_set_member_count`, `qualified_origin_set_member_count`: count; `independence_assessment_disclosures`: record_disclosures |
| M004 | `per_seed_origin_memberships`: incidence; `origin_incidence_counts`: incidence; `seed_origin_dispositions`: partition; `documentary_origin_resolution_fraction`: fraction |
| M005 | `single_origin_contribution_hhi`: fraction |
| M006 | `immediate_evidence_layer_dispositions`: partition; `inherited_only_seed_fraction`: fraction; `inherited_only_completion_interval`: completion_interval |
| M007 | `unresolved_frontier_reference_count`, `unqualified_terminal_record_count`, `seed_items_with_unresolved_ancestry_count`: count; `ancestry_gap_disclosures`: record_disclosures |
| M008 | `shared_recorded_ancestor_count`, `matching_family_label_count`: count; `evaluator_overlap_disclosures`: record_disclosures; `evaluator_overlap_witnesses`: witness_collection |
| M009 | `externality_assessment_disclosures`: record_disclosures; `externality_stage_links`: record_disclosures |
| M010 | `pipeline_stage_disclosures`: record_disclosures; `stage_member_partition`: partition; `stage_occurrence_fraction`: fraction; `stage_occurrence_completion_interval`: completion_interval; `cohort_transition_disclosures`: record_disclosures; `cohort_transition_fraction`: fraction; `cohort_transition_completion_interval`: completion_interval |
| M011 | `declared_correction_route_witnesses`, `applicable_authorized_route_witnesses`: witness_collection; `correction_route_disclosures`: record_disclosures |
| M012 | `correction_case_record_count`, `handling_event_record_count`, `linked_change_event_record_count`, `documentary_linked_change_target_count`, `cases_with_documentary_linked_change_count`: count; `correction_case_disclosures`, `correction_target_change_disclosures`, `reported_capacity_disclosures`: record_disclosures |
| M013 | `corrective_independence_disclosures`, `human_contribution_disclosures`: record_disclosures |
| M014 | `anomaly_context_disclosures`, `contestation_disclosures`: record_disclosures; `tail_stage_result_links`: record_disclosures referencing eligible M010 results |
| M015 | `coverage_disclosures`, `documentary_basis_gap_disclosures`: record_disclosures; `declared_basis_inventory`, `reference_availability_inventory`: partition |

M003 keeps each comparison separate. `qualified_origin_set_member_count` is applicable when every subject is an eligible documentary-boundary OriginEvent in the same inquiry, Claim and selected dimension, rather than an arbitrary Model or Actor comparison. Required documentary qualification is the one in definitions §21.3. A submitted three-member comparison can have count 3 while its qualified count is unavailable. A claim with no comparison gets the missing-assessment result; no global total is synthesized.

The incidence payload retains each origin ID, its incident seed IDs and `c_r`, together with N. An optional incidence fraction retains `c_r/N` and the nonexclusive qualification. M005 retains its original bucket counts in the same scoped basis; an incidence column cannot be normalized into HHI weights.

M004's five classifications remain `unresolved_or_conflicted`, `contains_baseline_or_scope_cut`, `contains_declared_origin`, `multiple_documented_origins` and `single_documented_origin`, with the precedence in definitions §22.2. They are analytical dispositions rather than execution/result states.

M006's four categories and M010's Y/F/U member classifications retain definitions §§24 and 26. Multiple-origin rows remain complete ancestry without numerical allocation. Unknown/disputed stage rows stay U. M012's handling outcomes remain nonexclusive record inventories unless the input supplies an appropriately supported final-state designation; this contract supplies no newest-wins reducer.

Native input conclusions, `verification.reported_outcome`, authority grants, PipelineRecord states and CorrectionEvent outcomes are displayed verbatim in their attributed fields. They are not converted to toolkit verification or run status. For example, an available `correction_case_disclosures` result can contain a caller's `failed` handling outcome while `run.processing_state = completed`.

M009/M010 linked-stage disclosures require the actual subject identity or supplied mapping. There is no automatic join by similar prose. M014 references eligible M010 stage results instead of duplicating counts under a second metric. Capacity strings in M012 remain string disclosures with unit/horizon; no utilization or adequacy calculation is added.

## 18. Findings, witness scope and threat associations

### 18.1 Finding object

A Finding contains `id`, `observation_kind`, `condition_code`, `diagnostic_refs`, `threat_family_refs`, `scope_ref`, `population_refs`, `basis_refs`, `witness`, `contrary_input_refs`, `reason_refs`, `statement` and `interpretation_limit`.

`observation_kind` is one of `positive_witness`, `no_witness_in_examined_view`, `bounded_absence_under_declared_coverage`, `attributed_observation`, `qualification_gap` or `recorded_conflict`. These values describe evidentiary form; they do not express threat severity.

`witness` contains the finite ordered node references and edge/record-link references relevant to a path/cycle, or the record/member references relevant to a non-path result. It identifies the view and basis through its scope. An absence witness describes the completed search population, predicate set and coverage, rather than inventing an empty positive path. A supplied denial remains an attributed record, even when it participates in a conflict.

### 18.2 Narrow condition catalog

The condition code names the established local observation. A threat-family association is optional and nonexclusive; it is permitted only by the relevant threat card and must remain adjacent to that narrower meaning.

| `condition_code` | Observable scope | Permitted related threat family |
|---|---|---|
| `shared_origin_witness` | Same claim/dimension contributions have a recorded common origin | SIT-TH001 |
| `citation_path_witness` | Explicit Artifact citation path, without inferred evidentiary dependence | SIT-TH002 |
| `transformation_path_witness` | Explicit material or claim-scoped derivation | SIT-TH002; SIT-TH003 only with supplied syndication/copy relation |
| `model_mediated_derivation_witness` | Disclosed model-generation role and transformation chain | SIT-TH004 |
| `view_cycle_witness` | Finite cycle in the named citation/material/claim/model/succession view | SIT-TH005; SIT-TH007 only with represented benchmark context |
| `assurance_loop_limitation` | Self/circular evidence support does not independently certify itself | SIT-TH005 |
| `evaluator_overlap_witness` | Shared object, common ancestor or one-sided ancestry in actual evaluator roles | SIT-TH006; SIT-TH007 with explicit benchmark role/artifact |
| `family_label_match` | Exact supplied model-family label strings match | SIT-TH006, with explicit warning that it is a label match |
| `provenance_gap` | Explicit unresolved or unsupported history | SIT-TH008, as a gap rather than proof of erasure |
| `verification_scope_limitation` | Identity/process verification cannot substantiate the stronger claim | SIT-TH009 |
| `independence_record_conflict` | Relevant supplied process-independence and ancestry assertions conflict | SIT-TH001 or SIT-TH006 as appropriate |
| `correction_dependency_witness` | Recorded control/process overlap in a corrective role | SIT-TH010 |
| `correction_route_limitation` | Declared path, grant, action or temporal applicability is unestablished/inapplicable | SIT-TH010-SIT-TH011 |
| `case_handling_disclosure` | Attributed submission/handling outcome for one case | SIT-TH011 only at that bounded case meaning |
| `linked_change_disclosure` | Attributed before/after or supported-removal linkage | No adverse threat association required |
| `downstream_change_undocumented` | Required linked-change evidence is absent from the examined record set | SIT-TH011, without a failed-correction claim |
| `externality_stage_limitation` | Externality/intake/use stages remain incomplete or separately contradicted | SIT-TH012, without an adequacy verdict |
| `recorded_stage_exclusion` | Evidence-bearing non-occurrence in an explicit cohort/stage | SIT-TH014, without inferred motive |
| `anomaly_or_contestation_disclosure` | Supplied context, stance or unclassified anomaly remains visible | SIT-TH014 where relevant; no threat verdict required |
| `attributed_external_observation` | Source report/evaluation outcome disclosed at its actual basis | No automatic semantic assignment to a threat family |
| `scoped_no_witness` | Completed typed search found no eligible witness at its declared scope | No claim that any threat family passed |
| `recorded_data_conflict` | Explicit well-formed contradictory scope/identity/time/record information | Family association only where a matching threat card applies |

A threat-family name must never be emitted as the value of a source-level status. The software does not read an incident's free text to decide that it is poisoning, propaganda, collusion or capture. Such allegations remain in `attributed_external_observation` with their own wording and source. No new taxonomy annotation is imported through an extension as authoritative evidence.

An external reported manipulation does not activate a v0.1 detector. `release_limits` must state that content-level poisoning/injection/authorship detection was not performed by this product. A matching source report may still be disclosed as input evidence. [SIT-TH013; SIT-D027]

### 18.3 No incident inflation or hidden intervention

One witness can be linked to several threat cards without increasing an incident total. This release defines no total incident count, severity, probability or universal clean-source result. Findings cannot trigger quarantine, removal, down-weighting, source contact, sanctions, appeal filing, rollback or changes to the audited system.

The report may identify the missing evidence needed for a stronger answer, using fixed prerequisite descriptions. It cannot fabricate that evidence, infer hidden actors, select a preferred viewpoint or turn the missing-evidence explanation into an automated repair action.

## 19. JSON/Markdown equivalence, ordering and disclosure

### 19.1 Semantic parity

Both formats must preserve report/input identity, processing state, exact scope, all requested capability outcomes, numerical populations, material reasons, premise attribution and release limits. Markdown may group technical metadata, but every main result must have a visible qualification and a stable route to its detail. A summary cannot hide unavailable metrics or show a restricted HHI without its denominator and scope.

A Markdown table must write an explicit state and reason for a non-result. A blank cell, dash or numeric sentinel is insufficient. Exact ratios remain available alongside decimals. Unknown rows stay in denominators and partitions. Threat headings contain narrow observation text rather than an unsupported accusation.

A full logical report and an authorized redacted derivative are different artifacts. The derivative must disclose its omitted scope and changed evidence visibility. It cannot claim identical analytical completeness merely because both files came from one run. Exact export/redaction mechanics remain WU9 work.

### 19.2 Deterministic representation

For the same accepted logical input, contract version, requested scope and completed operations, substantive values, memberships, reasons and witness meaning must be deterministic. Source array order provides no evidence priority.

Canonical presentation orders inquiries/claims/record IDs by their case-sensitive ASCII identifiers; diagnostic families by numeric ID; reason/condition codes by their fixed strings; and input-set references by collection kind then identifier. Pipeline keys retain exact strings. Role pairs have stable role-name order. Paths retain their causal/traversal order; they are not sorted into a meaningless set.

Result `witness_refs` point to Finding IDs whose `witness` field carries the finite evidence. Finding `diagnostic_refs` list the associated SIT-M family IDs. Those output links organize an explanation; they do not create additional input evidence.

Several equally valid witnesses may exist. A later implementation may use a fixed deterministic witness-selection rule, but it must retain all relevant conflicts and blockers and cannot use a conveniently short path to certify incomplete ancestry. It need not expand every possible path. A shortened displayed witness links to its preserved detail or states its truncation explicitly.

Volatile run IDs, wall-clock timestamps, resource timings and a raw-file digest that changes because input byte order changed are excluded from semantic-equality claims. Exact byte-for-byte canonical serialization and report-ID derivation are WU10 choices. Until adopted, repeatability means equal substantive report content with those differences disclosed, not invented reproducible bytes.

### 19.3 Safe rendering and privacy boundary

Input text, labels, excerpts, locators and extension values remain inert in both formats. Rendered Markdown must escape raw HTML, unintended links/images, table separators, headings, code fences and control characters sufficiently to prevent source data from changing report structure or causing active retrieval. A locator is displayed as inert text by default; the report never auto-loads previews, remote images or local files. ANSI terminal controls and visually misleading control sequences must not gain execution or presentation authority.

Escaping changes a presentation, not the stored evidence. The original supplied value and any presentation transformation remain traceable under the eventual privacy policy. This is safe output encoding, not a semantic content detector or source-sanitation service.

Do not publish protected identities, contact locators, excerpts or identifying topology merely to make a witness self-contained. If permitted disclosure cannot preserve a conclusion's basis, the public derivative must retain that limitation or withhold the stronger claim. Redaction cannot invent independence. Error messages must not dump source payloads, secrets, stack traces containing private data or local paths by default.

These are required reporting properties under the accepted threat boundary. Exact limits, redaction permissions, overwrite policy, retention, safe destination handling and adversarial rendering tests remain WU9/WU10 and pre-release gates. No runtime protection is claimed to exist in this document.

## 20. Written observability and reporting cases

These are documentary conformance witnesses. They reuse the approved meanings without implementing a graph, freezing the WU7 hero or claiming an independent reviewer. Unless a case says otherwise, its small fictional input is structurally valid and its stated supporting evidence meets the relevant documentary conditions.

| ID | Input / question | Required output states and retained distinction |
|---|---|---|
| W6-01 | Five listed Artifact records, no claim EvidenceItems or ancestry | M001 inventory count available at 5; Claim seed count available at 0; M003 qualified count unavailable, M005 unavailable with no-seed/zero-denominator reasons; no independent-source zero |
| W6-02 | One represented seed has a typed unresolved artifact/origin endpoint | Accept input; relevant inventories and gap disclosures available; complete-origin/HHI results unavailable; unknown endpoint remains a valid record |
| W6-03 | A reference names an ID absent from every input collection | Reject input; validation_diagnostics only; no audit levels or source conclusions |
| W6-04 | Six complete single-origin seeds have buckets 5 and 1; no independence assessment | M005 available at 26/36, display may also show 13/18 and 0.722222; M003 qualified count unavailable; concentration supplies no process independence |
| W6-05 | Add a seventh seed with unresolved ancestry to W6-04 | N = 7 in M004; known O1/O2 incidence retained; HHI unavailable for the full set; no fallback to the previous six |
| W6-06 | A seed has two complete documentary origin parents | Multiple-origin disposition available; no unknown-ancestry claim solely from two parents; HHI unavailable for multi_origin_unallocated |
| W6-07 | A complete immediate copy link reaches an ancestor with unknown distant acquisition | M006 may have available inherited-only classification; M004 unresolved origin and M005 unavailable remain separate |
| W6-08 | An active relevant denial disputes one documentary parent edge | Preserve both sources; necessary qualified origin results blocked; unrelated inventories or correction outcomes remain available |
| W6-09 | Two qualified pairwise comparisons cover O1/O2 and O2/O3 | Each comparison count available at 2; no derived jointly independent count of 3 or union-based score |
| W6-10 | A supplied three-member assessment lacks inspectable basis | Submitted count available at 3; qualified member count unavailable with basis reasons; source's stated conclusion remains attributed |
| W6-11 | No common evaluator ancestor is found in a completely processed but partial model graph | Recorded shared-ancestor count may be available at 0 with partial-coverage limit; no independence finding |
| W6-12 | Candidate and judge have a shared recorded ancestor and matching family label | Show ancestry witness and string match as distinct outputs; neither becomes an error-correlation number |
| W6-13 | A fully supported case-linked change exists, acquisition ancestry and authority are unknown | M012 linked-target evidence remains available; M005 and M011 authorized-route result may be unavailable; Level 4 links do not repair Level 2 or Level 3 gaps |
| W6-14 | Declared channel path exists with no applicable action grant | Declared witness available; applicable authorized-route output unavailable with authority reason; no effect/capacity claim |
| W6-15 | Grant covers review but requested route action is rollback | Action-specific applicability unmet; review grant retained; no accidental rollback authority |
| W6-16 | Accepted case has two documented target changes and a third target with no change record | Two qualified targets counted; third change evidence unavailable; no correction-success rate and no failed-third-target statement |
| W6-17 | Handling record reports failed; input is valid and reporting finishes | Native outcome `failed` retained in available disclosure; run processing completed; no runtime failure confusion |
| W6-18 | Influence-use record is evidenced; admission and preservation not recorded | Influence disclosure available; earlier stages unresolved; no automatic four-stage replenishment or causal effect |
| W6-19 | Eligible five-member cohort has Y = 3, F = 1, U = 1 | Partition available; point fraction unavailable; optional completion interval available at [3/5, 4/5]; no denominator 4 |
| W6-20 | Same cohort has one member with applicable positive and negative observations | That member stays U with conflict references; no majority/newest-wins choice |
| W6-21 | Final answer sources only, no pipeline universe | Final inventory available; retention fraction unavailable with cohort reason; no suppression claim |
| W6-22 | Enumerated empty population versus absent cohort population | Empty inventory count 0 available; empty-set ratio unavailable; absent cohort has unestablished population and no fabricated T = 0 |
| W6-23 | Exact stage cohort exists but two admission baselines compete | Standalone stage result remains available; transition unavailable with baseline ambiguity |
| W6-24 | Public names are withheld; a common opaque reference is disclosed | Shared reference remains shared with protection limitation; no extra roots from pseudonyms; no privacy guarantee from naming alone |
| W6-25 | Documentary label points only to a URL, or a self-supporting reference loop | Original label remains in basis inventory; qualification check exposes uninspectable/self-supporting basis; no fetched or verified claim |
| W6-26 | Date-only/unknown effective times do not establish a time-specific grant | Snapshot disclosure allowed at its stated meaning; historical/applicable grant unavailable; no fabricated midnight/timezone |
| W6-27 | Runtime limit interrupts origin enumeration after an inventory completed | run interrupted; completed inventory retained; unfinished origin and HHI results not_evaluated/interrupted, never zero or evidence-unavailable |
| W6-28 | Input includes report-shaped headings, Markdown links, HTML and instructions to hide gaps | Inert source content; unchanged analytical rules; safely encoded rendering; no live link/image fetch or hidden-prompt detector claim |
| W6-29 | No supplied poisoning report and no content detector in release | No clean-source conclusion; release limit explicit; absence of an incident record does not imply an inspection |
| W6-30 | Same logical sets arrive in different input order | Equal substantive scopes/counts/states; deterministic presentation; raw-file digest/timing may differ without a false semantic change |
| W6-31 | Markdown summary keeps HHI but omits its blocked sibling and unknown population | Nonconforming report; JSON/Markdown parity and capability disclosure criterion fails |
| W6-32 | Valid sparse dossier has every requested availability decision completed | run completed with many unavailable results; no promotion to full evidence coverage or source integrity |

## 21. Review and future test obligations

`SUCCESS_CRITERIA.md` records the measurable WU6 acceptance obligations. Future validation must exercise every public state pairing, count/ratio/interval form, native-state distinction, prerequisite and reason code used by an included capability. Written W6 cases supplement the W3, W4 and W5 cases; they do not replace them.

The next units must cover positive, negative, missing-data and boundary cases for every analytical field, plus state-propagation, malformed-input, nonintervention, privacy, interruption and rendering tests. Determinism tests compare the substantive report while explicitly excluding named volatile fields. A test that catches an instruction-shaped string is not evidence of an injection detector; the security obligation is that all such strings lack control authority.

No result can be published as scientifically validated because these document checks pass. A coherent fabricated dossier can still mislead local analysis. External process validation remains a separate evidence stream. The same drafting assistant performs the authoring checks; no second independent audit is claimed.

## 22. Consumer handoff and remaining work

WU7 may select its canonical hero and micro-cases using the existing records, fifteen metrics and this report contract after review. It must not recover the earlier illustrative global root-count or high/low-score shortcuts. Expected outputs should specify exact scope, basis, availability, reasons and native record outcomes using the WU6 distinctions.

WU8 owns the detailed validation plan and implementation Trace IDs. WU9 owns concrete privacy/resource/export and licensing choices. WU10 owns module/API ownership, dependency and canonical byte-serialization decisions. None is completed by this document. The full Phase 0 audit and approval remain WU11 work.

The incremental package contains reporting revision 0.2, lineage revision 0.2 and new success criteria revision 0.1. Keep definitions revision 0.2, product revision 0.3, threat revision 0.1 and decision register revision 0.5 alongside them, with the scoped WU5 acceptance supplement in §11.1. Earlier archives remain unchanged. The central register must be synchronized only in an authorized update.

## 23. Work Unit 6 review choices and exact stop

| Review item | Submitted realization | Alternatives and rationale | Approval limit |
|---|---|---|---|
| WU6-C01 | Separate processing, atomic result availability and premise basis; field-specific checks; non-cumulative Level 0-4 navigation | A single level/status would hide independent evidence gaps and overstate sparse or interrupted results. A wholly unstructured narrative would prevent consistent testing. The submitted matrix follows the already accepted diagnostic boundaries. | Reporting semantics only; no source-truth or maturity score |
| WU6-C02 | Reserved sit-report/0.1 envelope, scoped populations, typed references, exact value forms and native-state preservation | A flat score table would lose denominators, evidence and distinctions between failure records and run failure. This structure preserves those meanings without adding input records or metrics. | Documentation contract; executable schema, API and canonical byte format remain later work |
| WU6-C03 | Narrow condition codes, bounded threat associations, JSON/Markdown parity, inert rendering and explicit interrupted-work behavior | Taxonomy-only labels, executable Markdown or completed-looking partial output would exceed the accepted threat contract. The proposed output rules make those failures testable. | No detector, intervention, runtime privacy guarantee or security certification |

This delivery records acceptance of the preceding WU5 choices but does not mark WU6-C01-WU6-C03 accepted. One contextual acceptance of this enumerated package can authorize their use by WU7. If review reveals a change to metric meaning, input types or a paper's claim, stop the affected part and obtain the corresponding scoped amendment rather than hiding it in a report field.

No `PHASE_0_APPROVAL.md`, implementation source, JSON Schema file, runtime example, dependency manifest, workflow or remote repository modification is part of this unit. Work stops after WU6 documentation and packaging.

## 24. Input identities and local authoring verification

The input identity manifest and completed local checks are included in `SUCCESS_CRITERIA.md`, §§7-8. The retained WU4 numbered body in this document and WU3 numbered body in the lineage revision are checked byte-for-byte against the corresponding old text. Their historical approval language remains historical.

The package is checked for exactly three allowed Markdown members, source/result ID continuity, table and heading structure, internal/assembled-folder references, explicit non-result meanings, preservation of the fifteen analytical families and original input registries, and archive/member byte agreement. Simple arithmetic checks concern the written examples only. There is no runtime toolkit, graph execution, external authentication, independent review, CI run or GitHub write in this delivery.
