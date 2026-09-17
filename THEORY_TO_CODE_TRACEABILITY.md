# THEORY_TO_CODE_TRACEABILITY

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Target release | v0.1 |
| Phase / work unit | Phase 0 / Work Unit 8: Validation and traceability |
| Revision | 0.1 |
| Date | 2026-09-17 |
| Status | PROPOSED FOR REVIEW; logical ownership and future tests only |
| Theory Owner | Xiangyu Guo |
| Technical Owner | Unassigned |
| Primary inputs | Source map 0.1; definitions 0.2; lineage 0.3; product 0.4; reporting 0.2; threat 0.1 |
| Companion outputs | VALIDATION_PLAN.md revision 0.2; SUCCESS_CRITERIA.md revision 0.3 |
| Trace inventory | SIT-TR001-SIT-TR035 |
| Field-test inventory | SIT-VF001-SIT-VF057, each with P/N/M/B obligations |
| Shared test families | SIT-VG001-SIT-VG026 |
| Future module paths | Assigned in WU10; no code path or API frozen here |
| Runtime implementation / test execution | None / not performed |
| Full Phase 0 approval | Not issued |

## 1. Purpose, authority and interpretation

This document binds the existing theory map to approved product meaning, the current registered report fields and the Work Unit 8 test obligations. A Trace ID names a responsibility that later implementation must discharge. It does not assert that code exists.

The user's contextual acceptance of the Work Unit 7 handoff, including its named WU6 reporting dependency, is recorded in [VALIDATION_PLAN.md](VALIDATION_PLAN.md) §9. Earlier central decisions and supplements retain their scope. This unit does not modify the plan, theory papers, source map, decision register, definitions, lineage, reporting, product or threat contracts.

Use these distinct namespaces:

| Namespace | Role |
|---|---|
| SIT-T001-SIT-T040 | Existing source-map entry with its original classification and page locator |
| SIT-P001-SIT-P016 | Existing product requirement |
| SIT-M001-SIT-M015 | Existing analytical family |
| SIT-TR001-SIT-TR035 | Current primary future responsibility and validation ownership |
| SIT-VF001-SIT-VF057 | One existing analytical output leaf and four test obligations |
| SIT-VG001-SIT-VG026 | Shared contract/integration test family |
| SIT-SC001-SIT-SC066 | Cumulative success criteria, with the first 46 preserved |
| PC01-PC24 | Existing runtime prerequisite semantics, not theory or implementation Trace IDs |
| W3/W4/W5/W6/W7 and H7 IDs | Existing representation, threat, reporting and canonical input/oracle witnesses |

A code module cannot cite a theory ID as proof that its algorithm is correct. Its public behavior needs the corresponding product rule, field prerequisite, finite oracle and executable validation evidence. The theory entries containing mathematical results retain their original assumptions and are not silently converted into graph formulas.

The primary source references remain [SPEC_AUDIT.md](SPEC_AUDIT.md) and [THEORY_SOURCE_MAP.md](THEORY_SOURCE_MAP.md). Their one-based PDF locations identify supplied source versions. This unit does not verify outside standards, republish papers, update empirical findings or add new theory claims.

## 2. Current operationalization and future binding rules

### 2.1 One primary responsibility per registered leaf

Each of the 57 reporting §17 fields has one primary Trace ID. Cross-cutting result state, evidence, time, privacy and formatting rules are additional dependencies. Sharing those dependencies does not permit duplicate implementations with inconsistent definitions.

Logical owner names below describe **prospective module responsibilities**. They are deliberately independent of package/file naming and implementation libraries. WU10 must assign concrete module, public-interface and test paths while preserving these IDs and meanings. It may split an owner across internal modules only with one designated public semantic authority for each field.

### 2.2 Deferred numerical and structural choices stay deferred

No Trace selects a library, CLI spelling, function signature, canonical byte representation, resource budget or disclosure permission. WU9/WU10 gates are copied into the test plan and remain visible. An in-scope behavior cannot be marked passed merely because its exact code path is deferred.

An unresolved choice that changes a public result must be resolved by its contract owner before executable expectations are frozen. A prototype or helper function cannot decide it implicitly. A new analytical leaf requires a product/report change and its own tests; a free-form disclosure is not a route around the registered catalog.

### 2.3 Source-derived concepts and toolkit mechanisms

Every Trace below is a toolkit implementation responsibility. Its linked source entries keep their own SOURCE_DEFINITION, STRUCTURAL_CLAIM, FORMAL_MODEL_RESULT, GOVERNANCE_PROPOSAL, SOURCE_BOUNDARY or TOOLKIT_OPERATIONALIZATION classification.

The 57 field keys, report states, HHI convention, test IDs, finite fixtures and logical owners are product operationalizations. The papers motivate the constraints, but do not provide these exact schemas or certify this program. Exclusion/control traces are first-class responsibilities even when they produce no standalone analytical leaf.

## 3. Logical owner registry

| Prospective responsibility owner | Owned meaning | Concrete implementation status |
|---|---|---|
| INGESTION_CONTRACT | Closed local bundle, structural admission, typed references and entry-point equivalence. | No module created; concrete path binding belongs to WU10 |
| EVIDENCE_BASIS | Attribution, inspectable support, documentary qualification, native classifications, coverage and conflicts. | No module created; concrete path binding belongs to WU10 |
| SOURCE_INVENTORY | Explicit seed-Artifact and Claim-bound contribution units. | No module created; concrete path binding belongs to WU10 |
| ORIGIN_ANALYSIS | Typed origin reachability, boundary qualification and represented unresolved frontiers. | No module created; concrete path binding belongs to WU10 |
| PROCESS_COMPARISON | Qualification of one supplied process-comparison set and its dimension. | No module created; concrete path binding belongs to WU10 |
| CONTRIBUTION_PROFILE | Seed-origin incidence, restricted HHI and immediate inheritance, with exact denominators. | No module created; concrete path binding belongs to WU10 |
| EVALUATOR_LINEAGE | Actual Evaluation roles, typed model/material history and bounded overlap. | No module created; concrete path binding belongs to WU10 |
| PRESENCE_RECORDS | Boundary-relative externality and independently evidenced stages/cohorts. | No module created; concrete path binding belongs to WU10 |
| CORRECTION_ROUTES | Declared routes, target/action/time matching and each required authority grant. | No module created; concrete path binding belongs to WU10 |
| CORRECTION_OUTCOMES | Submissions, handling, before/after or removal linkage, and reported capacity. | No module created; concrete path binding belongs to WU10 |
| HUMAN_REVIEW_RECORDS | Substantive human contribution and separately qualified corrective-process independence. | No module created; concrete path binding belongs to WU10 |
| CONTEXT_PRESERVATION | Original anomaly context, supplied contestation and existing stage-result links. | No module created; concrete path binding belongs to WU10 |
| GRAPH_VIEW_CONTRACT | Permitted typed graph projections and finite witness semantics. | No module created; concrete path binding belongs to WU10 |
| TEMPORAL_CONTRACT | Source time precision, lifecycle and immutable snapshot boundaries. | No module created; concrete path binding belongs to WU10 |
| REPORT_CONTRACT | Run/result states, scope/population/basis references, capabilities and evidence navigation. | No module created; concrete path binding belongs to WU10 |
| FINDING_CONTRACT | Narrow condition meanings and evidence-bounded threat associations. | No module created; concrete path binding belongs to WU10 |
| REPORT_PRESENTATION | Exact value display, inert output, cross-format parity and substantive determinism. | No module created; concrete path binding belongs to WU10 |
| RUNTIME_BOUNDARY | No-network/no-intervention behavior, protected disclosure, faults and adopted resource limits. | No module created; concrete path binding belongs to WU10 |
| VALIDATION_GOVERNANCE | Golden expectations, Trace closure, source boundaries, counterexamples and approval evidence. | No module created; concrete path binding belongs to WU10 |

The current technical owner is unassigned. These responsibility labels are not names of appointed human maintainers. Actual reviewer/maintainer identities belong to later governance records.

## 4. Stable Trace register

Each row's validation families supplement the leaf-specific obligations listed in §5. The exact source locations are supplied through §6 and the original map. All references below concern the current attached specification versions.

### SIT-TR001: Closed local input, typed records and references

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `INGESTION_CONTRACT` |
| Existing source entries | `SIT-T008`, `SIT-T022`, `SIT-T035`, `SIT-T040` |
| Existing product requirements | `SIT-P001`, `SIT-P002`, `SIT-P003`, `SIT-P014` |
| Owned analytical families | Cross-cutting/control Trace; no extra analytical field |
| Controlling specification | Lineage §§2-9, 13-14 |
| Required shared validation | `SIT-VG001`, `SIT-VG002`, `SIT-VG003`, `SIT-VG004`, `SIT-VG005`, `SIT-VG023` |
| Existing acceptance criteria | `SIT-SC002`, `SIT-SC003`, `SIT-SC009` |
| Non-negotiable interpretation limit | Admissibility and record structure never authenticate sources. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR002: Preserved epistemic type, attribution and classification

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `EVIDENCE_BASIS` |
| Existing source entries | `SIT-T002`, `SIT-T004`, `SIT-T005`, `SIT-T006`, `SIT-T008`, `SIT-T011`, `SIT-T022`, `SIT-T032` |
| Existing product requirements | `SIT-P002`, `SIT-P003`, `SIT-P008`, `SIT-P014`, `SIT-P016` |
| Owned analytical families | Cross-cutting/control Trace; no extra analytical field |
| Controlling specification | Lineage §§3-4, 6-9; definitions §§6-7 |
| Required shared validation | `SIT-VG003`, `SIT-VG005`, `SIT-VG007`, `SIT-VG011` |
| Existing acceptance criteria | `SIT-SC005`, `SIT-SC022`, `SIT-SC024` |
| Non-negotiable interpretation limit | SIL and HDL axes retain source-local meanings; model judgment is not automatically human contribution. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR003: Seed Artifact and EvidenceItem inventory

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `SOURCE_INVENTORY` |
| Existing source entries | `SIT-T008`, `SIT-T022`, `SIT-T035`, `SIT-T036` |
| Existing product requirements | `SIT-P001`, `SIT-P003`, `SIT-P006` |
| Owned analytical families | `SIT-M001` |
| Controlling specification | Definitions §§20.1, 21.1; reporting §17 |
| Required shared validation | `SIT-VG002`, `SIT-VG012`, `SIT-VG016` |
| Existing acceptance criteria | `SIT-SC009`, `SIT-SC034` |
| Non-negotiable interpretation limit | The inquiry-wide unassigned count is not a separate count of unassigned Artifacts for each Claim. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR004: Reached origins and documentary boundaries

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `ORIGIN_ANALYSIS` |
| Existing source entries | `SIT-T008`, `SIT-T014`, `SIT-T016`, `SIT-T022`, `SIT-T036` |
| Existing product requirements | `SIT-P004`, `SIT-P006` |
| Owned analytical families | `SIT-M002` |
| Controlling specification | Definitions §21.2; lineage §9.1 |
| Required shared validation | `SIT-VG007`, `SIT-VG008`, `SIT-VG009` |
| Existing acceptance criteria | `SIT-SC011`, `SIT-SC014`, `SIT-SC035` |
| Non-negotiable interpretation limit | Zero qualifying records in a fully examined supplied view can be reported; it means neither zero actual origins nor unavailable record inventory. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR005: Supplied process and origin-set qualification

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `PROCESS_COMPARISON` |
| Existing source entries | `SIT-T016`, `SIT-T020`, `SIT-T035`, `SIT-T036` |
| Existing product requirements | `SIT-P005`, `SIT-P006` |
| Owned analytical families | `SIT-M003` |
| Controlling specification | Definitions §21.3; lineage §9.2 |
| Required shared validation | `SIT-VG005`, `SIT-VG007`, `SIT-VG009` |
| Existing acceptance criteria | `SIT-SC010`, `SIT-SC036` |
| Non-negotiable interpretation limit | No transitive union, maximal independent set, singleton certificate or statistical independence claim. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR006: Per-seed origin incidence and exhaustive dispositions

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `CONTRIBUTION_PROFILE` |
| Existing source entries | `SIT-T014`, `SIT-T017`, `SIT-T035`, `SIT-T036`, `SIT-T037` |
| Existing product requirements | `SIT-P004`, `SIT-P006`, `SIT-P007` |
| Owned analytical families | `SIT-M004` |
| Controlling specification | Definitions §22; reporting §17 |
| Required shared validation | `SIT-VG008`, `SIT-VG009`, `SIT-VG012`, `SIT-VG016` |
| Existing acceptance criteria | `SIT-SC011`, `SIT-SC034`, `SIT-SC035`, `SIT-SC041` |
| Non-negotiable interpretation limit | Known multi-parent incidence and unknown branches stay distinct in the original N. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR007: Restricted single-origin contribution HHI

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `CONTRIBUTION_PROFILE` |
| Existing source entries | `SIT-T017`, `SIT-T031`, `SIT-T037` |
| Existing product requirements | `SIT-P006`, `SIT-P007`, `SIT-P016` |
| Owned analytical families | `SIT-M005` |
| Controlling specification | Definitions §23; reporting §§16.5,17 |
| Required shared validation | `SIT-VG007`, `SIT-VG009`, `SIT-VG012`, `SIT-VG016` |
| Existing acceptance criteria | `SIT-SC012`, `SIT-SC035`, `SIT-SC041`, `SIT-SC045` |
| Non-negotiable interpretation limit | Exact count distribution only; no independence, truth, effective sample size or quality bands. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR008: Immediate EvidenceItem-layer inheritance

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `CONTRIBUTION_PROFILE` |
| Existing source entries | `SIT-T008`, `SIT-T014`, `SIT-T036`, `SIT-T037` |
| Existing product requirements | `SIT-P004`, `SIT-P006`, `SIT-P007` |
| Owned analytical families | `SIT-M006` |
| Controlling specification | Definitions §24 |
| Required shared validation | `SIT-VG004`, `SIT-VG008`, `SIT-VG012`, `SIT-VG016` |
| Existing acceptance criteria | `SIT-SC013`, `SIT-SC035`, `SIT-SC041` |
| Non-negotiable interpretation limit | Immediate inherited status may survive distant unknown ancestry; no semantic novelty test. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR009: Explicit frontiers, unqualified terminals and affected seeds

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `ORIGIN_ANALYSIS` |
| Existing source entries | `SIT-T008`, `SIT-T022`, `SIT-T036`, `SIT-T038` |
| Existing product requirements | `SIT-P004`, `SIT-P006` |
| Owned analytical families | `SIT-M007` |
| Controlling specification | Definitions §22.4 |
| Required shared validation | `SIT-VG002`, `SIT-VG008`, `SIT-VG022` |
| Existing acceptance criteria | `SIT-SC003`, `SIT-SC014`, `SIT-SC041` |
| Non-negotiable interpretation limit | A represented unresolved reference is not a count or upper bound of concealed roots. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR010: Role-specific evaluator and model overlap

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `EVALUATOR_LINEAGE` |
| Existing source entries | `SIT-T018`, `SIT-T020`, `SIT-T022`, `SIT-T026` |
| Existing product requirements | `SIT-P008` |
| Owned analytical families | `SIT-M008` |
| Controlling specification | Definitions §25.1; lineage §§6.7,10.6 |
| Required shared validation | `SIT-VG004`, `SIT-VG008`, `SIT-VG009` |
| Existing acceptance criteria | `SIT-SC015`, `SIT-SC037` |
| Non-negotiable interpretation limit | Strict common ancestors, exact shared roles, one-sided ancestry and family strings stay separate. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR011: Boundary-qualified externality and stage links

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `PRESENCE_RECORDS` |
| Existing source entries | `SIT-T001`, `SIT-T003`, `SIT-T016`, `SIT-T029` |
| Existing product requirements | `SIT-P009` |
| Owned analytical families | `SIT-M009` |
| Controlling specification | Definitions §25.2; lineage §9.6 |
| Required shared validation | `SIT-VG005`, `SIT-VG006`, `SIT-VG012` |
| Existing acceptance criteria | `SIT-SC016`, `SIT-SC017`, `SIT-SC038` |
| Non-negotiable interpretation limit | Dates, source type and admission do not establish externality or sufficiency. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR012: Exact-key stages and finite-cohort transitions

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `PRESENCE_RECORDS` |
| Existing source entries | `SIT-T001`, `SIT-T021`, `SIT-T023`, `SIT-T029` |
| Existing product requirements | `SIT-P009`, `SIT-P011`, `SIT-P012` |
| Owned analytical families | `SIT-M010` |
| Controlling specification | Definitions §26.1-§26.4 |
| Required shared validation | `SIT-VG006`, `SIT-VG009`, `SIT-VG012`, `SIT-VG016` |
| Existing acceptance criteria | `SIT-SC017`, `SIT-SC018`, `SIT-SC019`, `SIT-SC038` |
| Non-negotiable interpretation limit | Same-member evidenced admission baseline; preservation/selection targets only; no multiplied funnel. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR013: Declared correction routes and grant applicability

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `CORRECTION_ROUTES` |
| Existing source entries | `SIT-T013`, `SIT-T024`, `SIT-T026`, `SIT-T034`, `SIT-T039` |
| Existing product requirements | `SIT-P010` |
| Owned analytical families | `SIT-M011` |
| Controlling specification | Definitions §27.1; lineage §§9.7,11.1 |
| Required shared validation | `SIT-VG004`, `SIT-VG006`, `SIT-VG008`, `SIT-VG009` |
| Existing acceptance criteria | `SIT-SC020`, `SIT-SC039` |
| Non-negotiable interpretation limit | Finite route and every required leg's applicable authority do not establish observed use. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR014: Correction handling and documentary target changes

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `CORRECTION_OUTCOMES` |
| Existing source entries | `SIT-T012`, `SIT-T013`, `SIT-T024`, `SIT-T026`, `SIT-T034`, `SIT-T039` |
| Existing product requirements | `SIT-P010` |
| Owned analytical families | `SIT-M012` |
| Controlling specification | Definitions §27.2-§27.3; lineage §6.9 |
| Required shared validation | `SIT-VG003`, `SIT-VG006`, `SIT-VG009`, `SIT-VG011` |
| Existing acceptance criteria | `SIT-SC021`, `SIT-SC024`, `SIT-SC039` |
| Non-negotiable interpretation limit | Change-event count, case/target pairs and case count differ; capacity stays attributed strings. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR015: Corrective process independence and human contribution

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `HUMAN_REVIEW_RECORDS` |
| Existing source entries | `SIT-T005`, `SIT-T011`, `SIT-T020`, `SIT-T024`, `SIT-T035`, `SIT-T039` |
| Existing product requirements | `SIT-P008`, `SIT-P010` |
| Owned analytical families | `SIT-M013` |
| Controlling specification | Definitions §25.3; lineage §6.7 |
| Required shared validation | `SIT-VG003`, `SIT-VG005`, `SIT-VG007` |
| Existing acceptance criteria | `SIT-SC022`, `SIT-SC040` |
| Non-negotiable interpretation limit | One human review does not establish process independence or a renewable judgment stream. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR016: Anomalies, contestation and linked tail stages

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `CONTEXT_PRESERVATION` |
| Existing source entries | `SIT-T019`, `SIT-T021`, `SIT-T023`, `SIT-T029`, `SIT-T032` |
| Existing product requirements | `SIT-P011` |
| Owned analytical families | `SIT-M014` |
| Controlling specification | Definitions §26.5; lineage §6.11 |
| Required shared validation | `SIT-VG003`, `SIT-VG009`, `SIT-VG012` |
| Existing acceptance criteria | `SIT-SC023`, `SIT-SC040` |
| Non-negotiable interpretation limit | No automatic rarity labels, equal-weight votes, suppression inference or second retention metric. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR017: Scoped coverage and declared-basis inventory

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `EVIDENCE_BASIS` |
| Existing source entries | `SIT-T002`, `SIT-T004`, `SIT-T008`, `SIT-T022`, `SIT-T026`, `SIT-T038` |
| Existing product requirements | `SIT-P002`, `SIT-P006`, `SIT-P012` |
| Owned analytical families | `SIT-M015` |
| Controlling specification | Definitions §28.1; lineage §§3-4,9.3 |
| Required shared validation | `SIT-VG005`, `SIT-VG007`, `SIT-VG009`, `SIT-VG012` |
| Existing acceptance criteria | `SIT-SC005`, `SIT-SC006`, `SIT-SC025` |
| Non-negotiable interpretation limit | Native metadata inventory and documentary qualification can differ without relabeling the input. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR018: Typed graph view and finite witness discipline

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `GRAPH_VIEW_CONTRACT` |
| Existing source entries | `SIT-T008`, `SIT-T018`, `SIT-T020`, `SIT-T035`, `SIT-T036` |
| Existing product requirements | `SIT-P003`, `SIT-P004`, `SIT-P006`, `SIT-P008` |
| Owned analytical families | Cross-cutting/control Trace; no extra analytical field |
| Controlling specification | Lineage §§8,10,18.2; reporting §18 |
| Required shared validation | `SIT-VG004`, `SIT-VG008`, `SIT-VG015` |
| Existing acceptance criteria | `SIT-SC011`, `SIT-SC015`, `SIT-SC025`, `SIT-SC043` |
| Non-negotiable interpretation limit | No unrestricted all-edge ancestry, general DAG rejection or false cycle-to-truth inference. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR019: Conflict, identity and lifecycle localization

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `EVIDENCE_BASIS` |
| Existing source entries | `SIT-T004`, `SIT-T013`, `SIT-T022`, `SIT-T026`, `SIT-T032`, `SIT-T035` |
| Existing product requirements | `SIT-P002`, `SIT-P005`, `SIT-P006`, `SIT-P012` |
| Owned analytical families | Cross-cutting/control Trace; no extra analytical field |
| Controlling specification | Lineage §§7,9.9,12; definitions §§20.4,26.2 |
| Required shared validation | `SIT-VG002`, `SIT-VG005`, `SIT-VG009` |
| Existing acceptance criteria | `SIT-SC005`, `SIT-SC006`, `SIT-SC024`, `SIT-SC043` |
| Non-negotiable interpretation limit | External resolution does not silently discard contradictory records or merge identities. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR020: Temporal precision and snapshot boundary

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `TEMPORAL_CONTRACT` |
| Existing source entries | `SIT-T022`, `SIT-T024`, `SIT-T026`, `SIT-T035`, `SIT-T039` |
| Existing product requirements | `SIT-P001`, `SIT-P004`, `SIT-P009`, `SIT-P010` |
| Owned analytical families | Cross-cutting/control Trace; no extra analytical field |
| Controlling specification | Lineage §§2.3,3.1,10.7; reporting §16.2 |
| Required shared validation | `SIT-VG002`, `SIT-VG006`, `SIT-VG012` |
| Existing acceptance criteria | `SIT-SC001`, `SIT-SC020`, `SIT-SC034` |
| Non-negotiable interpretation limit | No hidden predecessor fetch, machine-timezone default or audit time substituted for source occurrence. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR021: Accepted, rejected, interrupted and failed run envelopes

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `REPORT_CONTRACT` |
| Existing source entries | `SIT-T004`, `SIT-T022`, `SIT-T038`, `SIT-T040` |
| Existing product requirements | `SIT-P002`, `SIT-P012`, `SIT-P013` |
| Owned analytical families | Cross-cutting/control Trace; no extra analytical field |
| Controlling specification | Reporting §§12.2,16.1,16.8 |
| Required shared validation | `SIT-VG001`, `SIT-VG010`, `SIT-VG022` |
| Existing acceptance criteria | `SIT-SC002`, `SIT-SC004`, `SIT-SC032`, `SIT-SC044` |
| Non-negotiable interpretation limit | Processing diagnostics contain no salvaged analytical arrays. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR022: Atomic values, checks, reasons and native states

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `REPORT_CONTRACT` |
| Existing source entries | `SIT-T004`, `SIT-T020`, `SIT-T022`, `SIT-T025`, `SIT-T031`, `SIT-T038` |
| Existing product requirements | `SIT-P002`, `SIT-P012`, `SIT-P013`, `SIT-P016` |
| Owned analytical families | Cross-cutting/control Trace; no extra analytical field |
| Controlling specification | Reporting §§12.3-13,16.4-16.5 |
| Required shared validation | `SIT-VG011`, `SIT-VG014`, `SIT-VG016` |
| Existing acceptance criteria | `SIT-SC004`, `SIT-SC005`, `SIT-SC006`, `SIT-SC024`, `SIT-SC027`, `SIT-SC028` |
| Non-negotiable interpretation limit | Six allowed execution/availability pairings; no result-origin ranking or native-state promotion. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR023: Scope, population and basis-reference envelope

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `REPORT_CONTRACT` |
| Existing source entries | `SIT-T008`, `SIT-T022`, `SIT-T026`, `SIT-T035`, `SIT-T036`, `SIT-T038` |
| Existing product requirements | `SIT-P001`, `SIT-P003`, `SIT-P006`, `SIT-P012`, `SIT-P013` |
| Owned analytical families | Cross-cutting/control Trace; no extra analytical field |
| Controlling specification | Reporting §§16.2-16.6; lineage §20 |
| Required shared validation | `SIT-VG002`, `SIT-VG007`, `SIT-VG012`, `SIT-VG023` |
| Existing acceptance criteria | `SIT-SC001`, `SIT-SC005`, `SIT-SC009`, `SIT-SC034` |
| Non-negotiable interpretation limit | Report-local and typed input references do not merge; exact counted units remain explicit. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR024: Capability and non-cumulative evidence navigation

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `REPORT_CONTRACT` |
| Existing source entries | `SIT-T003`, `SIT-T006`, `SIT-T025`, `SIT-T031`, `SIT-T038` |
| Existing product requirements | `SIT-P012`, `SIT-P013`, `SIT-P016` |
| Owned analytical families | Cross-cutting/control Trace; no extra analytical field |
| Controlling specification | Reporting §§14-16.7 |
| Required shared validation | `SIT-VG011`, `SIT-VG013`, `SIT-VG014` |
| Existing acceptance criteria | `SIT-SC007`, `SIT-SC008`, `SIT-SC044` |
| Non-negotiable interpretation limit | All fifteen families remain visible; source-governance layers and Level labels never become scores. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR025: Narrow findings and evidence-bounded threat associations

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `FINDING_CONTRACT` |
| Existing source entries | `SIT-T004`, `SIT-T010`, `SIT-T013`, `SIT-T017`, `SIT-T018`, `SIT-T024`, `SIT-T031`, `SIT-T034`, `SIT-T039` |
| Existing product requirements | `SIT-P004`, `SIT-P008`, `SIT-P010`, `SIT-P012`, `SIT-P016` |
| Owned analytical families | Cross-cutting/control Trace; no extra analytical field |
| Controlling specification | Reporting §18; threat cards |
| Required shared validation | `SIT-VG008`, `SIT-VG009`, `SIT-VG014`, `SIT-VG015`, `SIT-VG026` |
| Existing acceptance criteria | `SIT-SC025`, `SIT-SC026`, `SIT-SC031`, `SIT-SC043`, `SIT-SC044` |
| Non-negotiable interpretation limit | No automatic intent, incident total, severity, detector verdict or intervention. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR026: Semantic parity and inert report presentation

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `REPORT_PRESENTATION` |
| Existing source entries | `SIT-T008`, `SIT-T010`, `SIT-T022`, `SIT-T031`, `SIT-T032`, `SIT-T038`, `SIT-T040` |
| Existing product requirements | `SIT-P012`, `SIT-P013`, `SIT-P014` |
| Owned analytical families | Cross-cutting/control Trace; no extra analytical field |
| Controlling specification | Reporting §19.1 and §19.3 |
| Required shared validation | `SIT-VG017`, `SIT-VG019`, `SIT-VG021` |
| Existing acceptance criteria | `SIT-SC029`, `SIT-SC031`, `SIT-SC032`, `SIT-SC044` |
| Non-negotiable interpretation limit | Disclosure cannot hide materially unavailable siblings; exact safe-export implementation remains WU9. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR027: Exact values and deterministic substantive output

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `REPORT_PRESENTATION` |
| Existing source entries | `SIT-T017`, `SIT-T022`, `SIT-T031`, `SIT-T037`, `SIT-T040` |
| Existing product requirements | `SIT-P007`, `SIT-P012`, `SIT-P013` |
| Owned analytical families | Cross-cutting/control Trace; no extra analytical field |
| Controlling specification | Definitions §28.3-§28.4; reporting §19.2 |
| Required shared validation | `SIT-VG016`, `SIT-VG018` |
| Existing acceptance criteria | `SIT-SC009`, `SIT-SC012`, `SIT-SC028`, `SIT-SC030`, `SIT-SC045` |
| Non-negotiable interpretation limit | Semantic equivalence excludes named volatile metadata; canonical bytes remain WU10. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR028: Local file and in-process contract surfaces

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `INGESTION_CONTRACT` |
| Existing source entries | `SIT-T008`, `SIT-T022`, `SIT-T040` |
| Existing product requirements | `SIT-P002`, `SIT-P013`, `SIT-P014`, `SIT-P015` |
| Owned analytical families | Cross-cutting/control Trace; no extra analytical field |
| Controlling specification | SIT-D016-SIT-D018; lineage §2; reporting §16.8 |
| Required shared validation | `SIT-VG001`, `SIT-VG002`, `SIT-VG023` |
| Existing acceptance criteria | `SIT-SC002`, `SIT-SC003`, `SIT-SC029` |
| Non-negotiable interpretation limit | CLI symbols, Python signatures, serialization and filesystem details require WU9/WU10 adoption. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR029: Offline, non-executing and non-intervening runtime boundary

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `RUNTIME_BOUNDARY` |
| Existing source entries | `SIT-T004`, `SIT-T008`, `SIT-T010`, `SIT-T013`, `SIT-T040` |
| Existing product requirements | `SIT-P014`, `SIT-P015`, `SIT-P016` |
| Owned analytical families | Cross-cutting/control Trace; no extra analytical field |
| Controlling specification | Instructions §6; product §11; threat boundary |
| Required shared validation | `SIT-VG019`, `SIT-VG020`, `SIT-VG023`, `SIT-VG026` |
| Existing acceptance criteria | `SIT-SC031`, `SIT-SC044` |
| Non-negotiable interpretation limit | Only authorized report output may be written; no other repository's authority is inherited. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR030: Protected source and export safety

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `RUNTIME_BOUNDARY` |
| Existing source entries | `SIT-T002`, `SIT-T004`, `SIT-T008`, `SIT-T011`, `SIT-T013`, `SIT-T022`, `SIT-T040` |
| Existing product requirements | `SIT-P003`, `SIT-P014` |
| Owned analytical families | Cross-cutting/control Trace; no extra analytical field |
| Controlling specification | Lineage §§3-4; reporting §§16.6,19.3 |
| Required shared validation | `SIT-VG002`, `SIT-VG007`, `SIT-VG017`, `SIT-VG021` |
| Existing acceptance criteria | `SIT-SC003`, `SIT-SC005`, `SIT-SC031`, `SIT-SC032`, `SIT-SC044` |
| Non-negotiable interpretation limit | Privacy requirements have future tests, but no redaction policy or security guarantee is fabricated. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR031: Bounded work, fault injection and honest interruption

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `RUNTIME_BOUNDARY` |
| Existing source entries | `SIT-T010`, `SIT-T022`, `SIT-T038`, `SIT-T040` |
| Existing product requirements | `SIT-P002`, `SIT-P012`, `SIT-P014` |
| Owned analytical families | Cross-cutting/control Trace; no extra analytical field |
| Controlling specification | SIT-TS005; reporting §§12.2-12.4,16.8 |
| Required shared validation | `SIT-VG010`, `SIT-VG011`, `SIT-VG022` |
| Existing acceptance criteria | `SIT-SC004`, `SIT-SC032`, `SIT-SC044` |
| Non-negotiable interpretation limit | Concrete budgets and boundary behavior are WU9 gates; unfinished searches never become zeros. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR032: Golden oracle, trace coverage and change control

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `VALIDATION_GOVERNANCE` |
| Existing source entries | `SIT-T019`, `SIT-T020`, `SIT-T022`, `SIT-T026`, `SIT-T040` |
| Existing product requirements | `SIT-P001`, `SIT-P002`, `SIT-P012`, `SIT-P013`, `SIT-P015` |
| Owned analytical families | Cross-cutting/control Trace; no extra analytical field |
| Controlling specification | Plan §15; instructions §§5-8; validation §§1-8 |
| Required shared validation | `SIT-VG024`, `SIT-VG025` |
| Existing acceptance criteria | `SIT-SC033`, `SIT-SC042`, `SIT-SC045`, `SIT-SC046` |
| Non-negotiable interpretation limit | This document freezes test obligations, not executable fixtures or runtime success. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR033: Counterexamples and structural reopening of the product specification

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `VALIDATION_GOVERNANCE` |
| Existing source entries | `SIT-T011`, `SIT-T013`, `SIT-T019`, `SIT-T020`, `SIT-T021`, `SIT-T023`, `SIT-T025`, `SIT-T030` |
| Existing product requirements | `SIT-P006`, `SIT-P011`, `SIT-P012`, `SIT-P016` |
| Owned analytical families | Cross-cutting/control Trace; no extra analytical field |
| Controlling specification | EC §§2,6-7 via map; W7-28; validation §16 |
| Required shared validation | `SIT-VG024`, `SIT-VG025`, `SIT-VG026` |
| Existing acceptance criteria | `SIT-SC023`, `SIT-SC043` |
| Non-negotiable interpretation limit | Preserve out-of-cut counterexamples for owner review; no autonomous recutting or empirical validation claim. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR034: Source-local mathematical and interpretive exclusions

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `VALIDATION_GOVERNANCE` |
| Existing source entries | `SIT-T003`, `SIT-T005`, `SIT-T014`, `SIT-T015`, `SIT-T017`, `SIT-T025`, `SIT-T027`, `SIT-T028`, `SIT-T030`, `SIT-T031`, `SIT-T033`, `SIT-T037` |
| Existing product requirements | `SIT-P007`, `SIT-P012`, `SIT-P016` |
| Owned analytical families | Cross-cutting/control Trace; no extra analytical field |
| Controlling specification | Map §6; product §10; definitions §§2,23.3,28 |
| Required shared validation | `SIT-VG016`, `SIT-VG025`, `SIT-VG026` |
| Existing acceptance criteria | `SIT-SC008`, `SIT-SC012`, `SIT-SC027`, `SIT-SC028`, `SIT-SC045` |
| Non-negotiable interpretation limit | Formal theorems retain assumptions; no entropy/MI/Blackwell/collapse estimator is implied by graph tests. |
| Current code / runtime status | Not implemented; no executable test results |

### SIT-TR035: Full governance, source return and cross-project separation

| Binding | Current assignment |
|---|---|
| Primary prospective owner | `VALIDATION_GOVERNANCE` |
| Existing source entries | `SIT-T006`, `SIT-T007`, `SIT-T009`, `SIT-T010`, `SIT-T011`, `SIT-T012`, `SIT-T013`, `SIT-T040` |
| Existing product requirements | `SIT-P014`, `SIT-P015`, `SIT-P016` |
| Owned analytical families | Cross-cutting/control Trace; no extra analytical field |
| Controlling specification | SIL architecture through map; plan §§3.3-4; instructions §6.3 |
| Required shared validation | `SIT-VG019`, `SIT-VG020`, `SIT-VG024`, `SIT-VG026` |
| Existing acceptance criteria | `SIT-SC031`, `SIT-SC046` |
| Non-negotiable interpretation limit | Registration, ranking, compensation, live appeals, active detectors and shared internal toolkit code remain excluded. |
| Current code / runtime status | Not implemented; no executable test results |

## 5. Complete field-to-Trace and test crosswalk

The field keys below exactly match reporting §17, including spelling and family. The four test IDs named by each row are fully specified in validation §12. Common Result/nested payload tests in validation §§11 and 13 apply to every row.

An optional completion interval, decimal or inventory presentation retains its conditional exposure rule. The crosswalk does not make a required semantic result optional.
| Existing family / field | Primary Trace | Positive | Negative | Missing-data | Boundary |
|---|---|---|---|---|---|
| `SIT-M001`<br>`nominal_seed_artifact_record_count` | `SIT-TR003` | `SIT-VF001-P` | `SIT-VF001-N` | `SIT-VF001-M` | `SIT-VF001-B` |
| `SIT-M001`<br>`unresolved_seed_artifact_reference_count` | `SIT-TR003` | `SIT-VF002-P` | `SIT-VF002-N` | `SIT-VF002-M` | `SIT-VF002-B` |
| `SIT-M001`<br>`seed_evidence_item_count` | `SIT-TR003` | `SIT-VF003-P` | `SIT-VF003-N` | `SIT-VF003-M` | `SIT-VF003-B` |
| `SIT-M001`<br>`claim_artifact_record_count` | `SIT-TR003` | `SIT-VF004-P` | `SIT-VF004-N` | `SIT-VF004-M` | `SIT-VF004-B` |
| `SIT-M001`<br>`claim_unassigned_seed_artifact_record_count` | `SIT-TR003` | `SIT-VF005-P` | `SIT-VF005-N` | `SIT-VF005-M` | `SIT-VF005-B` |
| `SIT-M002`<br>`reached_origin_record_count` | `SIT-TR004` | `SIT-VF006-P` | `SIT-VF006-N` | `SIT-VF006-M` | `SIT-VF006-B` |
| `SIT-M002`<br>`documentary_origin_boundary_record_count` | `SIT-TR004` | `SIT-VF007-P` | `SIT-VF007-N` | `SIT-VF007-M` | `SIT-VF007-B` |
| `SIT-M002`<br>`origin_boundary_disclosures` | `SIT-TR004` | `SIT-VF008-P` | `SIT-VF008-N` | `SIT-VF008-M` | `SIT-VF008-B` |
| `SIT-M003`<br>`submitted_comparison_member_count` | `SIT-TR005` | `SIT-VF009-P` | `SIT-VF009-N` | `SIT-VF009-M` | `SIT-VF009-B` |
| `SIT-M003`<br>`qualified_process_set_member_count` | `SIT-TR005` | `SIT-VF010-P` | `SIT-VF010-N` | `SIT-VF010-M` | `SIT-VF010-B` |
| `SIT-M003`<br>`qualified_origin_set_member_count` | `SIT-TR005` | `SIT-VF011-P` | `SIT-VF011-N` | `SIT-VF011-M` | `SIT-VF011-B` |
| `SIT-M003`<br>`independence_assessment_disclosures` | `SIT-TR005` | `SIT-VF012-P` | `SIT-VF012-N` | `SIT-VF012-M` | `SIT-VF012-B` |
| `SIT-M004`<br>`per_seed_origin_memberships` | `SIT-TR006` | `SIT-VF013-P` | `SIT-VF013-N` | `SIT-VF013-M` | `SIT-VF013-B` |
| `SIT-M004`<br>`origin_incidence_counts` | `SIT-TR006` | `SIT-VF014-P` | `SIT-VF014-N` | `SIT-VF014-M` | `SIT-VF014-B` |
| `SIT-M004`<br>`seed_origin_dispositions` | `SIT-TR006` | `SIT-VF015-P` | `SIT-VF015-N` | `SIT-VF015-M` | `SIT-VF015-B` |
| `SIT-M004`<br>`documentary_origin_resolution_fraction` | `SIT-TR006` | `SIT-VF016-P` | `SIT-VF016-N` | `SIT-VF016-M` | `SIT-VF016-B` |
| `SIT-M005`<br>`single_origin_contribution_hhi` | `SIT-TR007` | `SIT-VF017-P` | `SIT-VF017-N` | `SIT-VF017-M` | `SIT-VF017-B` |
| `SIT-M006`<br>`immediate_evidence_layer_dispositions` | `SIT-TR008` | `SIT-VF018-P` | `SIT-VF018-N` | `SIT-VF018-M` | `SIT-VF018-B` |
| `SIT-M006`<br>`inherited_only_seed_fraction` | `SIT-TR008` | `SIT-VF019-P` | `SIT-VF019-N` | `SIT-VF019-M` | `SIT-VF019-B` |
| `SIT-M006`<br>`inherited_only_completion_interval` | `SIT-TR008` | `SIT-VF020-P` | `SIT-VF020-N` | `SIT-VF020-M` | `SIT-VF020-B` |
| `SIT-M007`<br>`unresolved_frontier_reference_count` | `SIT-TR009` | `SIT-VF021-P` | `SIT-VF021-N` | `SIT-VF021-M` | `SIT-VF021-B` |
| `SIT-M007`<br>`unqualified_terminal_record_count` | `SIT-TR009` | `SIT-VF022-P` | `SIT-VF022-N` | `SIT-VF022-M` | `SIT-VF022-B` |
| `SIT-M007`<br>`seed_items_with_unresolved_ancestry_count` | `SIT-TR009` | `SIT-VF023-P` | `SIT-VF023-N` | `SIT-VF023-M` | `SIT-VF023-B` |
| `SIT-M007`<br>`ancestry_gap_disclosures` | `SIT-TR009` | `SIT-VF024-P` | `SIT-VF024-N` | `SIT-VF024-M` | `SIT-VF024-B` |
| `SIT-M008`<br>`shared_recorded_ancestor_count` | `SIT-TR010` | `SIT-VF025-P` | `SIT-VF025-N` | `SIT-VF025-M` | `SIT-VF025-B` |
| `SIT-M008`<br>`matching_family_label_count` | `SIT-TR010` | `SIT-VF026-P` | `SIT-VF026-N` | `SIT-VF026-M` | `SIT-VF026-B` |
| `SIT-M008`<br>`evaluator_overlap_disclosures` | `SIT-TR010` | `SIT-VF027-P` | `SIT-VF027-N` | `SIT-VF027-M` | `SIT-VF027-B` |
| `SIT-M008`<br>`evaluator_overlap_witnesses` | `SIT-TR010` | `SIT-VF028-P` | `SIT-VF028-N` | `SIT-VF028-M` | `SIT-VF028-B` |
| `SIT-M009`<br>`externality_assessment_disclosures` | `SIT-TR011` | `SIT-VF029-P` | `SIT-VF029-N` | `SIT-VF029-M` | `SIT-VF029-B` |
| `SIT-M009`<br>`externality_stage_links` | `SIT-TR011` | `SIT-VF030-P` | `SIT-VF030-N` | `SIT-VF030-M` | `SIT-VF030-B` |
| `SIT-M010`<br>`pipeline_stage_disclosures` | `SIT-TR012` | `SIT-VF031-P` | `SIT-VF031-N` | `SIT-VF031-M` | `SIT-VF031-B` |
| `SIT-M010`<br>`stage_member_partition` | `SIT-TR012` | `SIT-VF032-P` | `SIT-VF032-N` | `SIT-VF032-M` | `SIT-VF032-B` |
| `SIT-M010`<br>`stage_occurrence_fraction` | `SIT-TR012` | `SIT-VF033-P` | `SIT-VF033-N` | `SIT-VF033-M` | `SIT-VF033-B` |
| `SIT-M010`<br>`stage_occurrence_completion_interval` | `SIT-TR012` | `SIT-VF034-P` | `SIT-VF034-N` | `SIT-VF034-M` | `SIT-VF034-B` |
| `SIT-M010`<br>`cohort_transition_disclosures` | `SIT-TR012` | `SIT-VF035-P` | `SIT-VF035-N` | `SIT-VF035-M` | `SIT-VF035-B` |
| `SIT-M010`<br>`cohort_transition_fraction` | `SIT-TR012` | `SIT-VF036-P` | `SIT-VF036-N` | `SIT-VF036-M` | `SIT-VF036-B` |
| `SIT-M010`<br>`cohort_transition_completion_interval` | `SIT-TR012` | `SIT-VF037-P` | `SIT-VF037-N` | `SIT-VF037-M` | `SIT-VF037-B` |
| `SIT-M011`<br>`declared_correction_route_witnesses` | `SIT-TR013` | `SIT-VF038-P` | `SIT-VF038-N` | `SIT-VF038-M` | `SIT-VF038-B` |
| `SIT-M011`<br>`applicable_authorized_route_witnesses` | `SIT-TR013` | `SIT-VF039-P` | `SIT-VF039-N` | `SIT-VF039-M` | `SIT-VF039-B` |
| `SIT-M011`<br>`correction_route_disclosures` | `SIT-TR013` | `SIT-VF040-P` | `SIT-VF040-N` | `SIT-VF040-M` | `SIT-VF040-B` |
| `SIT-M012`<br>`correction_case_record_count` | `SIT-TR014` | `SIT-VF041-P` | `SIT-VF041-N` | `SIT-VF041-M` | `SIT-VF041-B` |
| `SIT-M012`<br>`handling_event_record_count` | `SIT-TR014` | `SIT-VF042-P` | `SIT-VF042-N` | `SIT-VF042-M` | `SIT-VF042-B` |
| `SIT-M012`<br>`linked_change_event_record_count` | `SIT-TR014` | `SIT-VF043-P` | `SIT-VF043-N` | `SIT-VF043-M` | `SIT-VF043-B` |
| `SIT-M012`<br>`documentary_linked_change_target_count` | `SIT-TR014` | `SIT-VF044-P` | `SIT-VF044-N` | `SIT-VF044-M` | `SIT-VF044-B` |
| `SIT-M012`<br>`cases_with_documentary_linked_change_count` | `SIT-TR014` | `SIT-VF045-P` | `SIT-VF045-N` | `SIT-VF045-M` | `SIT-VF045-B` |
| `SIT-M012`<br>`correction_case_disclosures` | `SIT-TR014` | `SIT-VF046-P` | `SIT-VF046-N` | `SIT-VF046-M` | `SIT-VF046-B` |
| `SIT-M012`<br>`correction_target_change_disclosures` | `SIT-TR014` | `SIT-VF047-P` | `SIT-VF047-N` | `SIT-VF047-M` | `SIT-VF047-B` |
| `SIT-M012`<br>`reported_capacity_disclosures` | `SIT-TR014` | `SIT-VF048-P` | `SIT-VF048-N` | `SIT-VF048-M` | `SIT-VF048-B` |
| `SIT-M013`<br>`corrective_independence_disclosures` | `SIT-TR015` | `SIT-VF049-P` | `SIT-VF049-N` | `SIT-VF049-M` | `SIT-VF049-B` |
| `SIT-M013`<br>`human_contribution_disclosures` | `SIT-TR015` | `SIT-VF050-P` | `SIT-VF050-N` | `SIT-VF050-M` | `SIT-VF050-B` |
| `SIT-M014`<br>`anomaly_context_disclosures` | `SIT-TR016` | `SIT-VF051-P` | `SIT-VF051-N` | `SIT-VF051-M` | `SIT-VF051-B` |
| `SIT-M014`<br>`contestation_disclosures` | `SIT-TR016` | `SIT-VF052-P` | `SIT-VF052-N` | `SIT-VF052-M` | `SIT-VF052-B` |
| `SIT-M014`<br>`tail_stage_result_links` | `SIT-TR016` | `SIT-VF053-P` | `SIT-VF053-N` | `SIT-VF053-M` | `SIT-VF053-B` |
| `SIT-M015`<br>`coverage_disclosures` | `SIT-TR017` | `SIT-VF054-P` | `SIT-VF054-N` | `SIT-VF054-M` | `SIT-VF054-B` |
| `SIT-M015`<br>`documentary_basis_gap_disclosures` | `SIT-TR017` | `SIT-VF055-P` | `SIT-VF055-N` | `SIT-VF055-M` | `SIT-VF055-B` |
| `SIT-M015`<br>`declared_basis_inventory` | `SIT-TR017` | `SIT-VF056-P` | `SIT-VF056-N` | `SIT-VF056-M` | `SIT-VF056-B` |
| `SIT-M015`<br>`reference_availability_inventory` | `SIT-TR017` | `SIT-VF057-P` | `SIT-VF057-N` | `SIT-VF057-M` | `SIT-VF057-B` |

### 5.1 Cross-cutting dependencies for every field

Each primary field Trace also consumes SIT-TR001-SIT-TR002 for admitted typed input and basis, SIT-TR019-SIT-TR023 for applicable conflict/time/result/scope rules, SIT-TR024-SIT-TR027 for capability/findings/presentation/exactness where relevant, and SIT-TR029-SIT-TR032 for runtime boundaries and regression governance.

A primary owner cannot use those dependencies as blanket prerequisites. For example, unavailable authority cannot erase a documentary historical change, and partial model ancestry cannot block a complete acquisition HHI. Reporting §14.2 controls that localization.

### 5.2 Unregistered stronger results remain prohibited

No owner may add `independent_source_count`, hidden-root count, effective independent sample size, correlation coefficient, total incident count, global provenance percentage, correction-success rate, entropy/MI score or overall Level grade. The accepted M003 counts concern an actual supplied comparison, and the HHI concerns the defined contribution-frequency distribution.

The native source field `reported_outcome = verified` is preserved as input attribution. It does not become a source-verification result produced by the toolkit.

## 6. Reverse theory-source coverage

All forty existing map entries have an explicit destination below. Locations are carried from the supplied WU1 map, with its terminology intact. They are not independently retrieved citations. The source papers remain reference assets and are not included in this archive.

“Boundary/control” means the theory constrains interpretation or defines a function outside release; it does not require an implementation of the broader theory. No result about physical entropy, universal stochastic collapse, information-theoretic state contraction or social network pressure is inferred from a provenance graph.
| Existing theory entry | Original supplied-source locations | Consuming Traces | Operationalization / exclusion boundary |
|---|---|---|---|
| `SIT-T001`<br>Presence preserves continuing contact with reality | [SIL, p. 7, “Source Integrity Is a Structural Requirement”; p. 12]; [EC, §7.2, p. 10] | `SIT-TR011`, `SIT-TR012` | Active bounded preservation/qualification responsibility; see linked Trace limits. |
| `SIT-T002`<br>Integrity includes provenance, accountability and disclosed conflicts | [SIL, pp. 7 and 12, Presence × Integrity discussion] | `SIT-TR002`, `SIT-TR017`, `SIT-TR030` | Active bounded preservation/qualification responsibility; see linked Trace limits. |
| `SIT-T003`<br>Presence × Integrity is a joint structural requirement | [SIL, pp. 7 and 11-12]; [UIL, p. 5, “Closed Recursion and the Compact Formulas”] | `SIT-TR011`, `SIT-TR024`, `SIT-TR034` | Joint-dependence guard; no multiplication of proxy percentages. |
| `SIT-T004`<br>Verification has a limited scope | [SIL, pp. 11-14, verification and registry discussion]; [HDL, §9.2, pp. 22-23] | `SIT-TR002`, `SIT-TR017`, `SIT-TR019`, `SIT-TR021`, `SIT-TR022`, `SIT-TR025`, `SIT-TR029`, `SIT-TR030` | Active bounded preservation/qualification responsibility; see linked Trace limits. |
| `SIT-T005`<br>Three data layers and the special role of human judgment | [SIL, pp. 6-7, “Source Integrity Is a Structural Requirement”; pp. 14-16]; [HDL, §2, pp. 4-5] | `SIT-TR002`, `SIT-TR015`, `SIT-TR034` | Human judgment and three data-layer meanings preserved; no authorship-only truth rule. |
| `SIT-T006`<br>Four governance layers | [SIL, p. 13, source-layer table] | `SIT-TR002`, `SIT-TR024`, `SIT-TR035` | Four SIL governance functions retained as source classifications; no credibility tiers. |
| `SIT-T007`<br>Seven components and nine functions retain separate source organization | [SIL, pp. 12-15, “The Source Integrity Layer”]; [HDL, §9.1-9.9, pp. 22-24] | `SIT-TR035` | Full seven-component/nine-function architectures remain distinct and outside runtime scope. |
| `SIT-T008`<br>Minimum provenance survives transformations | [SIL, p. 14, provenance paragraph]; [HDL, §9.3, p. 23] | `SIT-TR001`, `SIT-TR002`, `SIT-TR003`, `SIT-TR004`, `SIT-TR008`, `SIT-TR009`, `SIT-TR017`, `SIT-TR018`, `SIT-TR023`, `SIT-TR026`, `SIT-TR028`, `SIT-TR029`, `SIT-TR030` | Active bounded preservation/qualification responsibility; see linked Trace limits. |
| `SIT-T009`<br>Trust weighting must remain contestable | [SIL, p. 14, trust-weighted retrieval paragraph]; [HDL, §9.5, p. 23] | `SIT-TR035` | Contestability motivates preserved evidence/appeals; no trust-ranking implementation. |
| `SIT-T010`<br>Manipulation is a source-integrity concern | [SIL, pp. 8-10 and 14]; [HDL, §7.2, p. 20; §9.6, p. 23] | `SIT-TR025`, `SIT-TR026`, `SIT-TR029`, `SIT-TR031`, `SIT-TR035` | Threat/inert-data obligations and attributed incidents; no active content detector. |
| `SIT-T011`<br>Human audit nodes must themselves be auditable | [SIL, pp. 14-15, human audit nodes]; [HDL, §9.8, p. 23] | `SIT-TR002`, `SIT-TR015`, `SIT-TR030`, `SIT-TR033`, `SIT-TR035` | Active bounded preservation/qualification responsibility; see linked Trace limits. |
| `SIT-T012`<br>Source return is distinct from epistemic correction | [SIL, p. 8 and p. 15, source-return paragraph]; [HDL, §9.9, p. 24] | `SIT-TR014`, `SIT-TR035` | Source return stays distinct from epistemic correction; no payment or referral service. |
| `SIT-T013`<br>Appeal and correction also apply to the integrity layer | [SIL, p. 15, appeals paragraph]; [HDL, §9.8, p. 23] | `SIT-TR013`, `SIT-TR014`, `SIT-TR019`, `SIT-TR025`, `SIT-TR029`, `SIT-TR030`, `SIT-TR033`, `SIT-TR035` | Active bounded preservation/qualification responsibility; see linked Trace limits. |
| `SIT-T014`<br>Closed recursion loses corrective difference under the stated conditions | [UIL, pp. 2-5 and 9-10; pp. 15-17] | `SIT-TR004`, `SIT-TR006`, `SIT-TR008`, `SIT-TR034` | Motivates bounded lineage diagnosis; no universal failure from concentration alone. |
| `SIT-T015`<br>Finite-resampling results retain their state-space assumptions | [UIL, pp. 6-9, mathematical core]; [EC, §4.1-4.4, pp. 6-7] | `SIT-TR034` | Formal resampling assumptions retained; no resampling or extinction estimator implemented. |
| `SIT-T016`<br>External supply must carry genuine difference and integrity | [UIL, pp. 8-9]; [EC, §4.4, p. 7] | `SIT-TR004`, `SIT-TR005`, `SIT-TR011` | Active bounded preservation/qualification responsibility; see linked Trace limits. |
| `SIT-T017`<br>Concentration can be functional in the appropriate domain | [UIL, p. 9 and p. 16]; [EC, §12, p. 14] | `SIT-TR006`, `SIT-TR007`, `SIT-TR025`, `SIT-TR027`, `SIT-TR034` | Concentration does not establish functional failure; HHI is narrow bookkeeping. |
| `SIT-T018`<br>Evaluator lineage can reproduce shared blind spots | [EC, §3.2, p. 5; §5.4, p. 9; §11, pp. 13-14]; [HDL, §7.3, pp. 20-21] | `SIT-TR010`, `SIT-TR018`, `SIT-TR025` | Active bounded preservation/qualification responsibility; see linked Trace limits. |
| `SIT-T019`<br>Structural validity precedes reliable measurement of a chosen object | [EC, §2.1-2.3, pp. 3-4; §7.1, p. 10] | `SIT-TR016`, `SIT-TR032`, `SIT-TR033` | Active bounded preservation/qualification responsibility; see linked Trace limits. |
| `SIT-T020`<br>Validation must match the type of claim | [EC, §6, pp. 9-10] | `SIT-TR005`, `SIT-TR010`, `SIT-TR015`, `SIT-TR018`, `SIT-TR022`, `SIT-TR032`, `SIT-TR033` | Active bounded preservation/qualification responsibility; see linked Trace limits. |
| `SIT-T021`<br>Distributional and structural reopening are different operations | [EC, §4.4-4.5, pp. 7-8] | `SIT-TR012`, `SIT-TR016`, `SIT-TR033` | Anomaly preservation and external counterexamples; no autonomous state-space recutting. |
| `SIT-T022`<br>The durable evaluation record preserves epistemic distinctions | [EC, §7.3, p. 11] | `SIT-TR001`, `SIT-TR002`, `SIT-TR003`, `SIT-TR004`, `SIT-TR009`, `SIT-TR010`, `SIT-TR017`, `SIT-TR019`, `SIT-TR020`, `SIT-TR021`, `SIT-TR022`, `SIT-TR023`, `SIT-TR026`, `SIT-TR027`, `SIT-TR028`, `SIT-TR030`, `SIT-TR031`, `SIT-TR032` | Active bounded preservation/qualification responsibility; see linked Trace limits. |
| `SIT-T023`<br>Tail retention preserves consequential rare cases | [EC, §7.1 and §7.4, pp. 10-11]; [HDL, §9.7, p. 23] | `SIT-TR012`, `SIT-TR016`, `SIT-TR033` | Active bounded preservation/qualification responsibility; see linked Trace limits. |
| `SIT-T024`<br>Corrective capacity includes power to change the system | [EC, §7.5, p. 11] | `SIT-TR013`, `SIT-TR014`, `SIT-TR015`, `SIT-TR020`, `SIT-TR025` | Active bounded preservation/qualification responsibility; see linked Trace limits. |
| `SIT-T025`<br>Open evaluation uses conjunctive conditions | [EC, §7, pp. 10-11] | `SIT-TR022`, `SIT-TR024`, `SIT-TR033`, `SIT-TR034` | Conjunctive evidence requirements; no compensating aggregate score. |
| `SIT-T026`<br>Evaluation changes across time and interaction | [EC, §8-10, pp. 12-13] | `SIT-TR010`, `SIT-TR013`, `SIT-TR014`, `SIT-TR017`, `SIT-TR019`, `SIT-TR020`, `SIT-TR023`, `SIT-TR032` | Active bounded preservation/qualification responsibility; see linked Trace limits. |
| `SIT-T027`<br>Surface entropy, reality coupling and semantic gradient are distinct | [HDL, §3.1-3.4, pp. 5-8; §11.1, p. 28] | `SIT-TR034` | Information-theoretic quantities remain separate from surface variation and truth. |
| `SIT-T028`<br>Garbling results are conditional and need not imply strict decay | [HDL, §4.1-4.5, pp. 8-13; §11.2-11.5, pp. 28-29] | `SIT-TR034` | Garbling and Blackwell conditions retained; no forced rankings or contraction estimator. |
| `SIT-T029`<br>Effective replenishment has four stages | [HDL, §4.6, p. 13; §5.5, pp. 16-17] | `SIT-TR011`, `SIT-TR012`, `SIT-TR016` | Active bounded preservation/qualification responsibility; see linked Trace limits. |
| `SIT-T030`<br>Independent measurement and frozen representations are required for information estimates | [HDL, §10.1-10.4, pp. 24-26] | `SIT-TR033`, `SIT-TR034` | Independent measurement requirement constrains claims; no information estimator provided. |
| `SIT-T031`<br>Deployable diagnostics remain a profile | [HDL, §10.5-10.6, pp. 27-28] | `SIT-TR007`, `SIT-TR022`, `SIT-TR024`, `SIT-TR025`, `SIT-TR026`, `SIT-TR027`, `SIT-TR034` | Active bounded preservation/qualification responsibility; see linked Trace limits. |
| `SIT-T032`<br>Epistemic status survives answer synthesis | [HDL, §5.4, p. 16; §9.4 and §9.8, p. 23] | `SIT-TR002`, `SIT-TR016`, `SIT-TR019`, `SIT-TR026` | Active bounded preservation/qualification responsibility; see linked Trace limits. |
| `SIT-T033`<br>Entropy remains a boundary and descriptive concept | [EBC, pp. 1 and 3-4; pp. 7-11] | `SIT-TR034` | Entropy is not a causal score or universal diagnostic in the toolkit. |
| `SIT-T034`<br>Reachability, authority and capacity require separate evidence | [BVL, pp. 10-15, network core; pp. 22-23, oversight; p. 25, model limits] | `SIT-TR013`, `SIT-TR014`, `SIT-TR025` | Routes, authority, outcome and capacity separated; network flow/queueing models excluded. |
| `SIT-T035`<br>Claim-relative independence is a toolkit rule with source support | [PLAN, §5, Rule 1]; supporting basis: [HDL, §3.1, pp. 5-6]; [EC, §6, pp. 9-10] | `SIT-TR001`, `SIT-TR003`, `SIT-TR005`, `SIT-TR006`, `SIT-TR015`, `SIT-TR018`, `SIT-TR019`, `SIT-TR020`, `SIT-TR023` | Active bounded preservation/qualification responsibility; see linked Trace limits. |
| `SIT-T036`<br>Root counts and unresolved boundaries need explicit product conventions | [PLAN, §§5, 10-11]; supporting basis: [UIL, pp. 8-9]; [HDL, §4.6, p. 13] | `SIT-TR003`, `SIT-TR004`, `SIT-TR005`, `SIT-TR006`, `SIT-TR008`, `SIT-TR009`, `SIT-TR018`, `SIT-TR023` | Active bounded preservation/qualification responsibility; see linked Trace limits. |
| `SIT-T037`<br>Concentration and derivative-share measurements are operationalizations | [PLAN, §11]; supporting basis: [UIL, pp. 9 and 16]; [EC, §3.2, p. 5]; [HDL, §4.6, p. 13] | `SIT-TR006`, `SIT-TR007`, `SIT-TR008`, `SIT-TR027`, `SIT-TR034` | HHI, incidence and first-step share are explicitly identified operationalizations. |
| `SIT-T038`<br>Observability levels describe available evidence | [PLAN, §13]; supporting basis: [EC, §10, p. 13]; [HDL, §10-11, pp. 24-29] | `SIT-TR009`, `SIT-TR017`, `SIT-TR021`, `SIT-TR022`, `SIT-TR023`, `SIT-TR024`, `SIT-TR026`, `SIT-TR031` | Observability is field-specific evidence navigation with non-results, not a maturity score. |
| `SIT-T039`<br>Correction reachability is narrower than demonstrated correction | [PLAN, §5, Rules 8-9; §§11 and 14]; supporting basis: [EC, §7.5, p. 11]; [HDL, §4.6, p. 13; §10.5, p. 27]; [BVL, pp. 22-23] | `SIT-TR013`, `SIT-TR014`, `SIT-TR015`, `SIT-TR020`, `SIT-TR025` | Active bounded preservation/qualification responsibility; see linked Trace limits. |
| `SIT-T040`<br>Local-first execution and project separation are product-governance choices | [PLAN, §§3.3-4, 16-18 and 23]; supporting basis: [SIL, pp. 14-15, auditability and appeals] | `SIT-TR001`, `SIT-TR021`, `SIT-TR026`, `SIT-TR027`, `SIT-TR028`, `SIT-TR029`, `SIT-TR030`, `SIT-TR031`, `SIT-TR032`, `SIT-TR035` | Local-first/project boundaries and later governance are explicit product choices. |

## 7. Reverse product and acceptance coverage

Every existing product requirement retains at least one primary or control Trace. This table is coverage of the current specification, not a claim that executable validation has passed.
| Existing product requirement | Meaning retained | Trace owners |
|---|---|---|
| `SIT-P001` | Explicit inquiry, version, system boundary and evidence coverage | `SIT-TR001`, `SIT-TR003`, `SIT-TR020`, `SIT-TR023`, `SIT-TR032` |
| `SIT-P002` | Structural validation with no promotion to substantive verification | `SIT-TR001`, `SIT-TR002`, `SIT-TR017`, `SIT-TR019`, `SIT-TR021`, `SIT-TR022`, `SIT-TR028`, `SIT-TR031`, `SIT-TR032` |
| `SIT-P003` | Claim-scoped artifact, actor, origin and transformation inventory | `SIT-TR001`, `SIT-TR002`, `SIT-TR003`, `SIT-TR018`, `SIT-TR023`, `SIT-TR030` |
| `SIT-P004` | Documented origin tracing and typed common-ancestry/cycle findings | `SIT-TR004`, `SIT-TR006`, `SIT-TR008`, `SIT-TR009`, `SIT-TR018`, `SIT-TR020`, `SIT-TR025` |
| `SIT-P005` | Evidence-qualified independence reporting | `SIT-TR005`, `SIT-TR019` |
| `SIT-P006` | Explicit unresolved boundaries and coverage-limited conclusions | `SIT-TR003`, `SIT-TR004`, `SIT-TR005`, `SIT-TR006`, `SIT-TR007`, `SIT-TR008`, `SIT-TR009`, `SIT-TR017`, `SIT-TR018`, `SIT-TR019`, `SIT-TR023`, `SIT-TR033` |
| `SIT-P007` | Origin-contribution and derivative-contribution profile | `SIT-TR006`, `SIT-TR007`, `SIT-TR008`, `SIT-TR027`, `SIT-TR034` |
| `SIT-P008` | Role-specific evaluator, rubric and model-lineage overlap | `SIT-TR002`, `SIT-TR010`, `SIT-TR015`, `SIT-TR018`, `SIT-TR025` |
| `SIT-P009` | Boundary- and stage-qualified external-presence evidence | `SIT-TR011`, `SIT-TR012`, `SIT-TR020` |
| `SIT-P010` | Correction route, applicability, authority, handling and outcome evidence | `SIT-TR013`, `SIT-TR014`, `SIT-TR015`, `SIT-TR020`, `SIT-TR025` |
| `SIT-P011` | Anomaly/contestation preservation and evidence-qualified stage retention | `SIT-TR012`, `SIT-TR016`, `SIT-TR033` |
| `SIT-P012` | Capability-specific prerequisites, uncertainty and reasons for non-results | `SIT-TR012`, `SIT-TR017`, `SIT-TR019`, `SIT-TR021`, `SIT-TR022`, `SIT-TR023`, `SIT-TR024`, `SIT-TR025`, `SIT-TR026`, `SIT-TR027`, `SIT-TR031`, `SIT-TR032`, `SIT-TR033`, `SIT-TR034` |
| `SIT-P013` | Reproducible JSON and Markdown reports from one result contract | `SIT-TR021`, `SIT-TR022`, `SIT-TR023`, `SIT-TR024`, `SIT-TR026`, `SIT-TR027`, `SIT-TR028`, `SIT-TR032` |
| `SIT-P014` | Offline, untrusted-data and protected-identity boundaries | `SIT-TR001`, `SIT-TR002`, `SIT-TR026`, `SIT-TR028`, `SIT-TR029`, `SIT-TR030`, `SIT-TR031`, `SIT-TR035` |
| `SIT-P015` | Separate product, no inherited runtime/schema/license authorization | `SIT-TR028`, `SIT-TR029`, `SIT-TR032`, `SIT-TR035` |
| `SIT-P016` | No universal score, automatic truth or unauthorized formal-model claim | `SIT-TR002`, `SIT-TR007`, `SIT-TR022`, `SIT-TR024`, `SIT-TR025`, `SIT-TR029`, `SIT-TR033`, `SIT-TR034`, `SIT-TR035` |

The first 46 acceptance criteria and all original H7/W7/W6/W5/W4/W3 case IDs remain intact. Success §§15-16 add SIT-SC047-SIT-SC066 for this unit's coverage and handoff. Criteria connect to the specific controlling rules and test families there; no new criterion replaces a source definition.

Full field coverage requires three independent checks: every registered field appears in §5 exactly once; every field has all four test obligations; and the actual test wording preserves the owner's scope and missingness. Matching a count of 57 alone does not prove semantic correctness.

## 8. Oracle, counterexample and review independence

Expected values come from the fixed case definitions and the governing contracts. In particular, H7's 26/36 HHI, separate six-member stage cohorts, two-origin comparison and three documentary target changes have different populations. No implementation helper can overwrite those expectations based on its own output.

Future executable tests must record the adopted fixture/oracle version and actual implementation output. A mismatch is first localized to input, contract, Trace and field. An independently supplied counterexample must be retained even when it requires a new product distinction, rather than being edited until the incumbent taxonomy accepts it.

The present documents are authored and checked by the same assistant. No external source verification, second independent reviewer, runtime security assessment, performance benchmark or empirical validation of the papers is claimed. The reproducibility and independent-review requirements are future validation obligations, not fabricated completed events.

## 9. WU9 and WU10 handoff

WU9 consumes SIT-TR029-SIT-TR031 and the privacy/resource tests in validation §11. It must specify concrete permissions, logging/retention, safe destination handling, overwrite/symlink policy as applicable, protected topology disclosure, numeric resource limits, integer compatibility and licensing. A source checksum does not authenticate a person or grant redistribution rights.

WU10 consumes every logical owner and assigns concrete future module/interface/test paths, dependency rationale, deterministic witness-selection and serialization rules. This document supplies no source tree, package metadata, CLI implementation or runtime dependency. A new implementation split preserves one semantic owner per registered field and keeps the Trace IDs stable.

The central register remains unchanged until an authorized update. WU11 must reconcile scoped approvals, all later gates, the source/field/test ownership map and the exact final file identities before issuing the final approval package.

## 10. Traceability acceptance and exact stop

WU8-C02 submits this register for review alongside validation's WU8-C01 and WU8-C03. Adoption freezes these logical responsibility and validation relationships within their stated boundaries. It does not authorize Phase 1 or any analytical implementation.

The authoring checks recorded in success §19 verify source-ID existence, complete product/field coverage, unique Trace and field-obligation IDs, exactly four suffixes per leaf, read-only input hashes and three-file archive contents. They do not prove that a future module exists or that its tests pass.

Stop after this three-document Work Unit 8 increment. The next unit is Work Unit 9 under its own file allowlist.
