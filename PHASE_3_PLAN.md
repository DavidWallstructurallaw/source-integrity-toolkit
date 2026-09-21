# PHASE_3_PLAN

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Phase | Phase 3: Bounded Private Analytical Core |
| Target release | v0.1; this phase does not publish a release |
| Plan revision | 0.1 |
| Date | 2026-09-20 |
| Status | PROPOSED FOR OWNER APPROVAL |
| Theory Owner | Xiangyu Guo |
| Technical Owner | Unassigned |
| Repository | `DavidWallstructurallaw/source-integrity-toolkit` |
| Current instruction | `制定 PHASE_3_PLAN.md` |
| Current write scope | This file only, on the `phase3/plan` review branch |
| Accepted Phase 2 merge | `3a9b75ab6ca4ed9d7c97207043a5c8f54c2e2547`, PR #18 |
| Accepted tree | `8e07404371fc9128ebdfcd85aab64936b15f7201` |
| Reviewed W09 head | `652ec2f434197ce657bc30c16927a9be66d8378e`; same tree |
| Accepted completion | `PHASE_2_COMPLETION.md` revision 1.0 and subsequent owner approval `批准` |
| Proposed work units | P3-W01 through P3-W15, sequential, each with its own review stop |
| Execution authorization | Pending approval of this plan and authorization of the named unit |
| Public interface | Existing API/CLI refusal behavior remains throughout Phase 3 |

## 1. Authority and actual entry

The owner accepted the completed W09 package and PR #18 was merged. The reviewed head passed Phase 2 cumulative CI run `35519939650`, attempt 1, in all four required profiles. Each profile collected 1,650 unique top-level tests, with zero failures, errors or skips, and 428 separately counted successful subtest events. Independent raw-artifact and Git/history audits passed. The merge's own run `35544450516`, attempt 1, also completed successfully in all four profiles. The latter is a GitHub service result supplementary to the independently audited review-head evidence.

The merge has parents `a189065d78a0256326a29b1c34a900b8673fc606` and the reviewed W09 head, and preserves the reviewed tree. Phase 2's pending-acceptance headers and `phase2_complete: false` describe their creation time; the subsequent owner approval and actual merge establish acceptance without rewriting those reviewed bytes. Phase 2 contains 156 tracked files, 48 product-module paths, thirteen implemented preparation modules and thirty-five protected modules.

Phase 0 fixes product semantics and module ownership. It does not prescribe all later phase numbers. The allocation, internal seams and implementation schedule below are explicit proposals for approval. Drafting this file authorizes no product implementation, migration, plan merge, Phase 4 plan or release.

### 1.1 Controlling sources

| Source | Controlling responsibility |
|---|---|
| `PHASE_0_APPROVAL.md` revision 1.1 | Adopted eighteen-file baseline at `7d2e5fcaff591641b5cefce00e71e88941dd1f95`, including its authorized digest correction |
| `PROJECT_INSTRUCTIONS.md`, `PHASE_0_PLAN.md` | Authority, exact work scope, source discipline, independent oracles and review gates |
| `V0.1_PRODUCT_SPEC.md`, `DEFINITIONS_AND_UNITS.md` sections 19-28 | Included analyses, exact populations, quantities, qualifications and exclusions |
| `CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` sections 2-14, 18-21, 24-28 | Canonical inputs, typed views, support, scope/time, conflicts and immutable H7 cases |
| `OBSERVABILITY_AND_REPORTING.md` sections 12-19 | Execution/result states, PC01-PC24, forty reasons, fifteen families, fifty-seven fields, findings and output obligations |
| `REPOSITORY_ARCHITECTURE.md` sections 5-8, 16-19 | Concrete module ownership, import direction, normalization, witnesses, schedule and accounting |
| `GOVERNANCE_AND_HANDOFF.md` section 22 | Binding precision supplements, particularly cancellation and complete-path tie breaking |
| `VALIDATION_PLAN.md` sections 10-17; `SUCCESS_CRITERIA.md`; `THEORY_TO_CODE_TRACEABILITY.md` | 228 field obligations, 26 shared families, counterexamples, exact expectations and 35 Trace owners |
| `PRIVACY_AND_DATA_HANDLING.md`, `SOURCE_INTEGRITY_THREAT_MODEL.md`, `DEPENDENCY_STRATEGY.md` | Fixed limits, privacy, standard-library runtime and bounded capability claims |
| `PHASE_1_COMPLETION.md`, `PHASE_2_PLAN.md`, `PHASE_2_COMPLETION.md`, PR #18 | Accepted scaffold/preparation behavior and its precise limitations |
| `scaffold/` catalogs and `phase2/` records | Source-bound indexes and historical evidence, never runtime policy inputs |

Read each source row with its surrounding binding clauses. Governance section 22 controls the points it refines. Preserve every earlier approval and repair as history. The six supplied theory papers remain inputs through the adopted source map; their presence in this conversation does not replace frozen operational definitions or authorize new formulas. No PDF, private dossier or theory text is added to the distributions.

### 1.2 Planning PR and the inherited CI limitation

This planning delivery adds only `PHASE_3_PLAN.md`. Verify the exact one-file diff from accepted Phase 2, the unchanged 156 existing tracked files, the accepted tree and the source/module/obligation mappings in this plan. Record the actual planning head and validation evidence in its PR after the commit exists.

The inherited driver in `tests/scaffold/test_ci_contract.py` accepts review branches only in the form `phase2/p2-w0[1-9]`. A genuine `phase3/plan` PR into main triggers that workflow but fails `review_branch_requires_explicit_unit` before test collection. Its immediate/cumulative scope rules also do not authorize this new plan. The old P1 workflow is unrelated to Phase 3 acceptance. An unsupported-context failure must remain visible; it is neither an analytical test failure nor passing Phase 3 verification.

The proposed planning acceptance gate is the document audit and exact preservation check above, with the successful accepted-parent matrix recorded separately. Owner approval may accept this specifically disclosed planning limitation. It does not override branch protection, required checks or access controls. If repository rules require a green executable planning check before merge, stop the merge and obtain a narrowly scoped CI migration authorization. Do not disguise the branch as W09, invent a Phase 2 context, change CI during this document-only task or count the parent's run as a run on the plan commit.

After the plan is accepted and merged, P3-W01 installs the approved Phase 3 context and cumulative verification. A push of the plan-only merge may encounter the same inherited limitation; its failure remains recorded until the actual migration provides new passing evidence. Implementation cannot start merely because this plan exists.

## 2. Proposed delivery boundary

Phase 3 implements all fifteen analytical families over the accepted immutable preparation model:

`supplied value or UTF-8 bytes -> bounded admission and finite structural job plan -> scoped evidence qualification and typed graph operations -> atomic analytical results -> private immutable analysis outcome`

The deliverable is a complete **private analytical core**. It computes the fifty-seven registered fields or their correct scoped non-results, evaluates their actual prerequisite questions, retains basis/conflicts/witnesses, and exposes honest execution status. It provides capability and non-cumulative domain navigation over real results. No required family is left as a placeholder at phase completion.

The proposed private seams are `_analyze_value(value)` and `_analyze_utf8(raw)` in `runtime/boundary.py`. They accept exactly the existing built-in root-dict and immutable-bytes domains, respectively. They have no options, paths, callbacks, user-supplied budgets, model selection or public exports. Their names are internal integration choices, not stable public API promises. Tests may exercise already admitted component inputs only under explicit trusted-construction preconditions.

These outcomes are internal representations with complete semantic links and validated value/state rules. They are not `AuditReport`, `sit-report/0.1`, a report-validation service or a new interchange schema. Semantic anchor keys may link private objects; final report-local IDs, root envelopes and serialization belong to the later reporting phase. Do not serialize the private object under the public contract label.

### 2.1 Deferred surfaces

Keep `audit_bundle`, `audit_file`, package exports and CLI audit refusal unchanged. Defer all four `reporting/` implementations, `runtime/disclosure.py`, native platform modules, output-directory handling and publication. Full report root/run/input-identity assembly, report-local naming and explanatory-object deduplication, JSON/Markdown parity and exact bytes, report schema, rendering controls, WU9-L14's per-representation limits, safe file capture, public options and release certification remain future work.

Private `supplied_utf8` means already supplied bytes. It does not establish `local_file` capture, a raw-file digest or native-file security. Keep internal source modes distinct from the formal report's `in_process`/`local_file` vocabulary. No new public source-mode enum is proposed.

No new package path, dependency, graph library, schema engine, network access, model call, plugin execution, telemetry, persistent cache, cross-project internal import, truth/trust score or automated intervention is included. The installed version stays `0.1.0.dev0`. The 48-module layout and existing package-member allowlists remain controlling.

## 3. Semantic and execution rules

### 3.1 Inputs, scopes and evidence qualification

Preserve Phase 2 admission and exact normalization. Compatible explicit gaps, denied assertions, conflicts, cycles and protected records remain valid input. Documentary qualification follows admission; failure to qualify an otherwise valid record does not retroactively reject its syntax. Input arrays, identity, Claim versions and five dependency dimensions retain their specified meaning.

Implement source-addressed checks for attribution, support availability, non-self-supporting documentary basis, scoped coverage, applicable lifecycle/time, relevant conflict and identity limitations. A supplied label, attestation or complete-coverage assertion remains attributed evidence. The toolkit does not authenticate it externally. Missing/withheld/locator-only support cannot be repaired by fetching it or inventing a passage.

Shared evidence primitives retain the `EVIDENCE_BASIS` owner in `contracts/evidence.py`, with paid qualification and time helpers in `validation/semantics.py`. Domain decisions remain with their named analysis owner. Contract modules cannot import validation or analysis. M015 retains SIT-TR017's ownership; it is not moved to the seed-inventory module for convenience.

Compute each prerequisite per exact result scope. Registry/family question lists are navigation unions, not an instruction to require every listed PC for every field. A known origin witness can survive incomplete other branches; HHI needs the whole population. A documented change can survive unknown authority. Model-history gaps do not automatically invalidate acquisition results. Relevant unsupported denials and late conflicts must remain visible and block only the conclusions they actually affect.

### 3.2 Typed graphs and finite witnesses

Use only the named projections and input-to-output view bridge in the lineage contract. Keep citations, transformations, acquisition, evaluator/training and correction routes distinct. Canonical record links retain their real selector identity without invented RelationAssertions. No name, locator, checksum, disconnected component or parentless node merges identities or certifies independence/origins.

Choose the shortest eligible simple path for the exact start/target/view/scope. Equal-length ties compare the **complete edge-key sequence**, including Assertion identity or the canonical record-link selector. Use bounded distance passes and complete-prefix ranking. For each cyclic SCC, choose its smallest typed node and canonical shortest cycle through that node; retain the relevant component evidence. A self-loop is a cycle. Do not enumerate all walks.

Representative selection is separate from complete parent, conflict, coverage and frontier inspection. A short path does not erase another parent. A cycle with an exit remains unresolved cyclic ancestry. No-witness output requires a finished search and states the examined scope; incomplete traversal cannot commit zero. Witness limits interrupt instead of clipping evidence.

### 3.3 Atomic analytical values

Carry each field's exact scope, population/membership state, execution/result pairing, result origin, value kind, basis, checks, witnesses, reasons and interpretation limit. Preserve all six legal execution/result combinations from reporting section 12.3. Available values have the declared kind; every non-result has null value and its actual reason. Source-native `unknown`, `failed` or `verified` remain attributed input data.

Preserve original finite denominators and member sets. HHI retains N, every bucket and `sum(n_r^2)/N^2`; H7-01 is `26/36`, and H7-V01 is `25/25`. Unknown rows stay in N. H7-V02 has unresolved ancestry and unavailable HHI; H7-V03 has known multi-origin unallocated contribution and unavailable HHI. Nonexclusive origin incidences can sum above one. Do not normalize them into weights, infer allocation or compute reciprocal/effective-root scores.

Phase 3 selects the already registered optional completion intervals when their prerequisites hold: M006's finite-record interval and M010's finite-cohort intervals. Preserve the unavailable point and all D/O/M/U or Y/F/U rows. For U=0, use the exact point and the specified `completion_interval_not_needed` non-result for the interval slot. Empty/unestablished populations supply no fabricated endpoints. Decimal formatting remains deferred with rendering.

Supplied pairwise and setwise comparisons stay distinct. Do not infer transitivity or construct a maximum independent set. Exact seed contributions, inquiry-wide Artifact inventory, origin records, origin incidences and assessment member counts remain different units. A qualified-record count can legitimately be zero where its owner defines it; failed qualification of a supplied comparison does not become a zero independence estimate.

### 3.4 One invocation budget and honest stopping

Retain WU9-L01-L10 and activate the analytical portion of WU9-L11 plus WU9-L13: 1,000,000 work units per capability/scope job; 10,000,000 per invocation including the existing 1,024-unit emergency reserve; a single 60-second cooperative deadline; 20,000 retained witnesses and 100,000 retained witness-member occurrences. Equality is allowed; the next excess charge stops before work. WU9-L14 remains a later encoded-report duty.

The current Phase 2 `_run_preparation` creates its own budget and marks acceptance after its preparation scope plan. Phase 3 must share tool-owned admission helpers and one execution context across capture, validation, **complete finite analytical job planning**, analysis and private finalization. Calling `_prepare_*` and starting a new analysis budget is prohibited. `_scope_plan`'s present Inquiry bindings alone are not the complete family/scope job plan. Plan all structural jobs before input acceptance, without semantic qualification or an implicit all-pairs expansion. Planning exhaustion leaves input `not_completed`.

Keep the existing preparation entry points' accepted behavior and return types. `_prepare_evidence_*` still reports only PC01 whole-check completion and pending analytical checks. New analysis seams perform the additional work. Project-owned component tests may use internal contexts; public callers and evidence cannot set clocks, quotas or cancellation callbacks.

Jobs run by Inquiry ID, numeric family and semantic operation/scope key; prerequisites and fields use registry order. Every visit, edge, repeated lookup, comparison, numeric operation, allocation/copy, emitted entry and inspected 256-byte block receives its specified prospective charge. Job charges also debit the single global ledger once. Share only the immutable raw index globally. Pure helpers may be called within another job under their original owner and charged to that job; no cross-job semantic cache supplies free work.

A value commits only with its complete finite population, relevant conflicts, qualifications, basis, reasons and witnesses. A family completes only after every planned cell makes an availability decision. Per-job interruption may retain earlier committed cells and mark current/unstarted cells correctly if charged finalization fits remaining global/time limits. Stopping analysis does not reset counters or permit more analysis through a finalization path. If complete private delivery cannot fit, use the fixed safe abort preserving actual accepted/not_completed state. Internal failure yields failed processing without ordinary analytical salvage.

Cancellation follows governance section 22.3: a separate payload-free transport event preserving actual input state. Do not relabel it resource exhaustion, execution failure, analysis-not-selected or a newly invented Reason. Diagnostics contain safe constants, not arbitrary source/exception text. Cooperative checks do not claim hard real-time enforcement or a hostile same-process sandbox.

## 4. Closed module ceiling and preserved artifacts

The following sixteen existing modules may acquire behavior for the first time, at the named unit only. All paths are relative to `src/source_integrity_toolkit/`.

| Existing module | First unit | Responsibility |
|---|---|---|
| `contracts/results.py` | P3-W02 | Private atomic analytical values and linked result primitives |
| `graph/projections.py` | P3-W04 | Explicit typed views and eligible record-link projection |
| `graph/traversal.py` | P3-W04 | Bounded deterministic finite traversal |
| `graph/cycles.py` | P3-W04 | Typed SCCs and cyclic-component evidence |
| `graph/witnesses.py` | P3-W04 | Canonical finite paths, cycles and member witnesses |
| `analysis/inventory.py` | P3-W05 | M001, seed and Artifact inventory |
| `analysis/origins.py` | P3-W05 | M002/M007, full origin tracing and limitations |
| `analysis/process_comparison.py` | P3-W06 | M003, exact supplied comparison qualification |
| `analysis/contribution_profile.py` | P3-W07 | M004/M005/M006, dispositions, incidence, HHI and immediate inheritance |
| `analysis/evaluator_lineage.py` | P3-W08 | M008, actual role-pair lineage |
| `analysis/human_review.py` | P3-W08 | M013, human contribution and corrective independence |
| `analysis/presence.py` | P3-W09 | M009/M010, boundary externality and stages/cohorts |
| `analysis/correction_routes.py` | P3-W10 | M011, declared routes and applicable grants |
| `analysis/correction_outcomes.py` | P3-W11 | M012, handling and linked target changes |
| `analysis/context.py` | P3-W12 | M014, anomalies, contestation and tail-stage context |
| `analysis/findings.py` | P3-W12 | Existing finding conditions and bounded observation forms |

Eight already implemented preparation modules may be extended only where listed in unit scopes: `contracts/evidence.py`, `contracts/execution.py`, `contracts/report.py`, `validation/semantics.py`, `validation/limits.py`, `runtime/resources.py`, `runtime/diagnostics.py` and `runtime/boundary.py`. Preserve their earlier behavior. The other five preparation modules, including input shapes/constants and the supplied-byte decoder, remain byte-identical to accepted Phase 2.

At phase completion, at most 29 of the 48 modules have implementation behavior. The other nineteen retain accepted bytes: every package `__init__.py`, `api.py`, `cli.py`, the four reporting modules, `runtime/disclosure.py`, `io/output_directory.py`, `io/publication.py`, `io/platform_linux.py` and `io/platform_windows.py`.

Freeze all Phase 0 specifications/approval, Phase 1 and Phase 2 plans/progress/completion, `scaffold/` catalogs/manifests, every existing `phase2/` record, the bundle schema, H7 fixtures and logical oracles, existing case indexes, license/notice/build metadata, dependency locks/pins and the old P1 workflow. Historical delivery manifests retain their named snapshots. New Phase 3 records describe the new entry and deltas. Existing tests remain live except precisely documented stage/history assertions adapted in W01; a test migration cannot weaken a product assertion.

## 5. Execution and scope rules common to all units

Each unit begins from the latest accepted predecessor on `phase3/p3-wNN`. Implement only the authorized unit, collect actual evidence, submit a review package and stop. A later unit's listed paths do not authorize early edits. Do not merge, force-push, delete branches, alter secrets/protection, release or start another phase automatically.

The exact common record paths for W01-W15 are:

```text
PHASE_3_PROGRESS.md
phase3/module_policy.json
phase3/implementation_evidence.json
phase3/obligation_coverage.json
```

For each unit, its effective allowlist is these four paths plus that unit's explicit list below. Directory mentions elsewhere are descriptive only. Common records permit truthful status, actual approval/predecessor/test evidence and that unit's scheduled policy advance. They cannot enlarge paths, change first-unit assignments, bless arbitrary code or close unperformed obligations. All other files are read-only unless explicitly listed. No deletion/rename is proposed.

W01 establishes all fifteen exact unit scopes and the entire promotion schedule in the guard/driver. Later normal advances update the separate Phase 3 policy without repeatedly changing historical scope tests. Current phase/unit comes independently from the actual PR branch or a single `SIT-Phase-Unit: P3-WNN` main merge footer. Unknown, duplicate, mismatched or future contexts fail. Candidate metadata never supplies its own authority.

Pin the actual approved plan bytes and accepted planning merge in `phase3/entry_manifest.json` after they exist. The expected plan-only entry contains 157 files; verify the actual tree rather than assuming it. A later out-of-scope correction requires a named narrow amendment and actual approval, recorded without retroactively enlarging earlier units. Missing dependency support or a genuine specification ambiguity is an affected-work stop.

Retain Ubuntu 24.04 / Windows Server 2025 with CPython 3.11 / 3.13, fixed action revisions, read-only CI permissions, no stored credentials, finite timeouts and all approved development pins. Recheck their actual installation and security applicability at execution. No replacement version or package is selected by this plan. Collect all existing and new tests, compare node identities with JUnit, and record real patch/image versions. Skips, xfails, missing collection, unrun cases and cancelled runs are not passes.

Use only fictional fixtures and synthetic canaries. New cases are separately named input deltas with independent source-bound expectations; existing H7 files/oracles stay immutable. Temporary destructive mutations occur only in isolated test copies. Product code never reads schemas, catalogs, fixtures, golden files or Phase 3 evidence records to calculate an answer.

## 6. P3-W01: Entry, guard and cumulative CI migration

Additional allowed paths:

```text
phase3/entry_manifest.json
phase3/transition_ledger.md
phase3/ci_review.md
tools/check_scaffold_boundary.py
tests/scaffold/test_ci_contract.py
tests/scaffold/test_imports.py
tests/scaffold/test_module_manifest.py
tests/scaffold/test_no_runtime_implementation.py
tests/scaffold/test_layer_boundaries.py
tests/scaffold/test_contract_catalogs.py
tests/contract/test_phase2_transition.py
tests/contract/test_phase3_transition.py
tests/contract/test_bundle_contract.py
tests/contract/test_input_schema_mapping.py
tests/contract/test_observability_preparation.py
tests/security/test_input_capture.py
tests/security/test_preparation_inertness.py
.github/workflows/phase1-ci.yml
README.md
```

Verify accepted Phase 2, all 156 prior files, the actual accepted plan entry and all frozen bytes. No product module changes in W01. The thirteen preparation implementations remain live and the thirty-five other modules retain their accepted bytes. Add the independently anchored Phase 3 ceiling and per-unit earliest promotions, import/isolation checks and exact immediate/cumulative path accounting. Test paired policy-plus-code mutation, forbidden path lookalikes, premature promotion, old-context mismatch and source-data attempts to set phase.

Preserve Phase 2's exact historical allowlists and repair meanings. Evaluate historical segments against their actual commits, then independently check current Phase 3 segments. Do not insert Phase 3 paths into Phase 2 permissions. A historical snapshot test cannot replace a current behavioral test.

Before adapting each assertion, record its old entry point/source, semantic purpose, actual replacement and rejecting mutation in the transition ledger. Retain the 1,650 predecessor top-level identities across all 34 test files, together with the separately accounted 428 subtest events; additions use their actual collection. Preserve all behavior, malicious mutation, privacy interception and fixture checks. No blanket historical execution, skip, deselection, xfail or generic-exception success can make the migration pass.

Explicit migration targets include the old W07/W08/W09 source-byte bridges and checker/workflow fixed-byte assertions; `test_observability_preparation.py::test_only_ten_w06_paths_and_no_old_test_permissions_changed`, whose historical W05-to-HEAD comparison must become a historical-segment check plus an independent current check; and `test_preparation_inertness.py::test_whole_package_guard_rejects_forbidden_implementation_in_temporary_copy`, whose trusted context and copied metadata must become stage-correct while retaining its positive and malicious controls. Also audit `test_observability_preparation.py::test_preserves_existing_report_declarations_and_w05_admission_body`: retain its historical AST witness and current preparation-behavior checks while explicitly accounting for the later authorized private-analysis integration. The listed file authority covers stage/history assumptions only.

Update the existing workflow and driver together to collect the full Phase 3 suite and preserve complete raw evidence, packaging and installed-runtime checks. Do not create an alternate green workflow that bypasses the cumulative suite. Update README's phase boundary honestly.

Acceptance: zero product-byte changes; complete transition ledger; actual predecessor identity retention; negative guard cases; exact W01 four-profile passing matrix, including the final documentation successor. Stop on lost assertions, metadata self-authorization, undisclosed test exclusions or unsupported required CI/dependencies.

## 7. P3-W02: Result contracts and analytical execution primitives

Additional allowed paths:

```text
src/source_integrity_toolkit/contracts/results.py
src/source_integrity_toolkit/contracts/report.py
src/source_integrity_toolkit/contracts/execution.py
src/source_integrity_toolkit/runtime/resources.py
src/source_integrity_toolkit/runtime/diagnostics.py
src/source_integrity_toolkit/validation/limits.py
tests/contract/test_result_contract.py
tests/contract/test_prerequisite_contract.py
tests/security/test_analytical_resource_limits.py
tests/security/test_analytical_diagnostics.py
```

Implement immutable private scope/population/value/check/reason/witness-reference primitives and declarative analytical field bindings, separate from unchanged preparation metadata. Validate closed vocabulary, all legal state pairings, exact count/fraction/interval forms, typed links and duplicate semantic slots. Keep report-root assembly and final IDs deferred. Constructing a private record does not establish that an analysis ran.

Define PC02 scope-check and PC24 completion-record primitives under REPORT_CONTRACT. Each actual component operation must establish its own valid scope and complete-population commit facts when it executes. W13 wires and checks those facts; it cannot retroactively mark earlier unperformed checks as met.

Implement the authority-free per-job port, global debit accounting, WU9-L13 reservation/retention counters, analysis-stop versus bounded-finalization distinction and safe cancellation/failure transports. Preserve every existing preparation outcome. Do not move the clock into lower layers or accept a caller port through an analysis entry point.

Acceptance: state/value mutants are rejected, bool counts fail, original fraction denominators survive, immutable references do not retain caller containers, scope/global charges are exact, below/at/above quota and witness controls pass, one emergency reserve and sticky first cause are preserved. W02 tests exercise primitives; they do not claim a running full analytical pipeline.

## 8. P3-W03: Documentary qualification, time and M015

Additional allowed paths:

```text
src/source_integrity_toolkit/contracts/evidence.py
src/source_integrity_toolkit/validation/semantics.py
tests/contract/test_analytical_basis.py
tests/contract/test_analytical_temporal.py
tests/unit/test_provenance_profile.py
```

Implement paid shared evidence checks and private representations for applicable attribution/support, evidence-reference availability, closed support loops, scoped coverage and conflict/identity/time limitations. Preserve the earlier syntax checks and observed-only preparation seams. Qualification must follow the exact type/dimension/Claim/version/time selector; a self-pointer or closed assurance loop alone cannot supply documentary support. Do not add a convenient unstated time-window endpoint convention.

Implement M015's four leaves under EVIDENCE_BASIS: attributed coverage disclosures, documentary-basis gaps, declared-basis inventory and reference-availability inventory. Count each record/reference once in the stated population. Retain supplied labels alongside failed support qualification.

Acceptance: the owner-local core clauses of SIT-VF054-SIT-VF057, active/denied/retracted/conflicting and time-precision cases, protected/withheld/locator-only support, irrelevant versus relevant conflict, and independent missing-data checks. PC03 retains SOURCE_INVENTORY ownership in W05 and PC04 retains GRAPH_VIEW_CONTRACT ownership in W04. Any M015 end-to-end clause depending on those actual checks stays pending until W13 integration; W03 may test explicit trusted component facts but cannot claim the missing providers executed. Pass typed facts across the later composition boundary without contracts/validation importing analysis/graph or duplicating their semantic owners. Runtime never fetches support or converts incomplete evidence into malformed-input rejection.

## 9. P3-W04: Typed projection, traversal, cycles and witnesses

Additional allowed paths:

```text
src/source_integrity_toolkit/graph/projections.py
src/source_integrity_toolkit/graph/traversal.py
src/source_integrity_toolkit/graph/cycles.py
src/source_integrity_toolkit/graph/witnesses.py
tests/contract/test_graph_views.py
tests/unit/test_graph_traversal.py
tests/unit/test_graph_cycles.py
tests/unit/test_graph_witnesses.py
tests/security/test_graph_limits.py
```

Implement the mechanics in section 3.2 using exact eligible views and project-owned budget ports. Inputs explicitly identify scope/start/target; graph code cannot select an epistemic conclusion. Retain positive edge eligibility separately from denied/unknown/conflicted records needed by domain qualification. All construction, adjacency ordering, repeated examination and witness retention are charged.

Acceptance: every permitted predicate/view/record-link mapping and forbidden cross-view mapping; diamonds versus multiple origins; self-loops and SCCs with exits; complete-path lexical tie counterexamples; input permutations; unknown endpoints; deep/wide/cyclic finite graphs; interruption before absence; untruncated all-member witnesses. Pure graph success supplies no independent-source or documentary-boundary result.

## 10. P3-W05: Seed inventory, reached origins and frontiers

Additional allowed paths:

```text
src/source_integrity_toolkit/analysis/inventory.py
src/source_integrity_toolkit/analysis/origins.py
tests/unit/test_inventory.py
tests/unit/test_origins.py
tests/unit/test_ancestry_frontiers.py
```

Implement M001, M002 and M007. Preserve A(I), E(I,C), resolved versus unresolved Artifact positions, inquiry-wide unassigned seeds and distinct contribution records. Trace every relevant branch and retain reached origins, applicable boundary evidence, declared origins, reference baselines, scope cuts, unqualified terminals, cycles and frontiers. Boundary labels do not terminate a contrary in-scope parent. Expose reusable paid origin-trace facts for later contribution analysis without taking over M004's owner.

Acceptance: SIT-VF001-SIT-VF008 and SIT-VF021-SIT-VF024 core obligations, exact H7 member sets, shared unknown endpoint versus affected-seed counts, one-root diamonds, cycles with exits, unsupported boundary labels, protected commonality and separate Claim/dimension populations. Every zero has its explicit finite inventory; no hidden-root total is invented.

## 11. P3-W06: Supplied comparison qualification

Additional allowed paths:

```text
src/source_integrity_toolkit/analysis/process_comparison.py
tests/unit/test_process_comparison.py
```

Implement M003 separately for each supplied pair/set assessment. Preserve subjects, form, native conclusion, examined and unexamined dimensions, method, attribution and support. A submitted member count can remain available when its qualified count cannot. Qualified origin membership additionally requires OriginEvent subjects and their scoped documentary origin conditions.

Acceptance: SIT-VF009-SIT-VF012 core obligations; H7's acquisition comparison; Evaluation/model subjects versus OriginEvents; contrary dependency, alias, support/time failure and missing assessment; overlapping pairs and setwise cases without union, summation or transitive independence. No invented singleton certificate or global independent-source count.

## 12. P3-W07: Contribution profile, restricted HHI and immediate inheritance

Additional allowed paths:

```text
src/source_integrity_toolkit/analysis/contribution_profile.py
tests/unit/test_contribution_profile.py
tests/unit/test_immediate_inheritance.py
```

Implement M004/M005/M006 under CONTRIBUTION_PROFILE using the paid origin helper. Apply the five origin dispositions in their specified precedence and preserve positive incidences alongside unresolved branches. Implement the complete PC12 gate, exact HHI bucket arithmetic, immediate EvidenceItem-layer D/O/M/U partition and the selected finite-record completion interval.

Acceptance: SIT-VF013-SIT-VF020 core obligations; all four frozen H7 inputs; H7-V02's full N=7 and `[5/7,6/7]` immediate interval; H7-V03's incidence counts 6 and 2 over N=7, `7/7` resolution and unavailable HHI; distant unknown versus complete immediate inheritance; same-identity blockers, zero denominator, contradictory late parent, order and exact unreduced arithmetic. Reject known-only HHI, implicit allocation and path-count inflation.

## 13. P3-W08: Evaluator lineage and human contribution

Additional allowed paths:

```text
src/source_integrity_toolkit/analysis/evaluator_lineage.py
src/source_integrity_toolkit/analysis/human_review.py
tests/unit/test_evaluator_lineage.py
tests/unit/test_human_review.py
```

Implement M008/M013 for actual represented role pairs and corrective processes. Keep shared role identity, strict common ancestry, one-sided ancestry and exact family-label matches separate. Invoke original comparison helpers for an actual supplied corrective-process assessment, with current-job charging. Preserve substantive human contribution and disclosed process/dependency limits.

Acceptance: SIT-VF025-SIT-VF028 and SIT-VF049-SIT-VF050 core obligations; identical role subjects without counting the subject as its own strict ancestor; missing roles/history; exact family strings without invented genealogy; shared training or rubric evidence; human presence without independent process, and independent process without proven institutional execution. No all-model pair expansion or label-based independence.

## 14. P3-W09: Externality, stages and finite cohorts

Additional allowed paths:

```text
src/source_integrity_toolkit/analysis/presence.py
tests/unit/test_presence.py
tests/unit/test_pipeline_cohorts.py
```

Implement M009/M010. Qualify supplied externality against the exact declared system boundary and retain separate stage links. Inventory admission, preservation, selection and influence records independently. Evidence-reference availability remains a separate concept. A valid influence record does not require invented earlier-stage records. Cohort quantities require one eligible exact run/stage key and an enumerated universe; ambiguity or unknown membership cannot supply a denominator.

Partition eligible finite members as Y/F/U under the specified evidence rule. Implement exact point/finite-cohort interval decisions and only the adopted same-population admission-to-target transition. Preserve contradictory evidence and original classifications. Dates, human labels and admission alone do not establish externality.

Acceptance: SIT-VF029-SIT-VF037 core obligations; ambiguous/missing cohort anchor, incomplete classification, equal versus changed member sets, U=0 versus U>0, unknown versus explicit non-occurrence, no zero/unknown denominator and no multiplied funnel or scalar Presence score.

## 15. P3-W10: Correction routes and grant applicability

Additional allowed paths:

```text
src/source_integrity_toolkit/analysis/correction_routes.py
tests/unit/test_correction_routes.py
```

Implement M011 for explicit channel/target/action/time anchors. Separate a declared route from applicable authority on every required leg. Preserve exact target version, grant scope, action and effective-time evidence. A direct target and a propagates_to chain retain their declared view meaning. Cycles do not justify walk counts or duplicate channels.

Acceptance: SIT-VF038-SIT-VF040 core obligations; wrong action/version/time, missing or conflicting grants, later valid alternatives, supported complete versus partial no-route evidence, shortest applicable witness and interrupted search. Route existence cannot establish use, correction effect or capacity.

## 16. P3-W11: Correction cases and linked effects

Additional allowed paths:

```text
src/source_integrity_toolkit/analysis/correction_outcomes.py
tests/unit/test_correction_outcomes.py
```

Implement M012's five distinct counts and attributed disclosures. Count qualified target changes by `(case_ref, before_ref)`; multiple events do not inflate distinct targets. Require supported before/after or explicit removal evidence for the stronger count while retaining unresolved change events. Preserve all handling outcomes, declared target sets, separately disclosed extra targets and native capacity units/horizons.

Acceptance: SIT-VF041-SIT-VF048 core obligations; H7's whole-case inventory of three linked change events and three documentary target pairs for R1-V1, A and D, kept distinct from its downstream subset {A,D,E}, where A/D have linked changes and E remains undocumented; missing after-state versus supported removal; opaque protected identity; acceptance followed by failure; actual documented change despite unknown authority; unsupported capacity and unlinked later versions. No newest-wins policy, causal-success claim, capacity formula or correction-success rate.

## 17. P3-W12: Context, findings and threat boundaries

Additional allowed paths:

```text
src/source_integrity_toolkit/analysis/context.py
src/source_integrity_toolkit/analysis/findings.py
tests/unit/test_context_preservation.py
tests/unit/test_findings.py
tests/contract/test_finding_boundaries.py
```

Implement M014 and the twenty-two existing finding conditions with the six registered observation forms. Preserve anomalies, disagreement, original or protected context and exact links to eligible stage results. An unclassified anomaly may lack a Claim; do not infer one. Obtain any necessary stage helper result under its original owner and current job, without a cross-job semantic cache.

Findings carry finite witnesses, conditional scope, basis and limitations. A missing content detector cannot yield a passed poisoning/injection check. A witnessed structural pattern cannot establish motive, censorship, authenticity or a universal threat verdict. Relevant negative, gap, attributed and conflict forms remain distinct.

Acceptance: SIT-VF051-SIT-VF053 core obligations, every registered condition/form, protected context and withheld-reference limitations, final-only material versus supplied transition baseline, exact witness/reason localization and mutants that launder source-native claims into tool verification.

## 18. P3-W13: Complete private orchestration and capability navigation

Additional allowed paths:

```text
src/source_integrity_toolkit/runtime/boundary.py
src/source_integrity_toolkit/runtime/resources.py
src/source_integrity_toolkit/runtime/diagnostics.py
src/source_integrity_toolkit/contracts/execution.py
src/source_integrity_toolkit/contracts/report.py
tests/integration/test_analytical_pipeline.py
tests/contract/test_analytical_observability.py
tests/security/test_analytical_interruption.py
```

Connect the private seams, shared admission helpers, full pre-acceptance structural job plan, all fifteen family owners and final immutable outcome. Implement the schedule and commit rules in section 3.4. Helpers do not run future jobs ahead of schedule, and implementation ordering is not runtime family order.

Complete scoped PC01-PC24 execution with exact per-field question applicability. PC24 records completed whole-population work, not a metadata assertion. Retain every required field/non-result for each applicable operation and every Inquiry/family capability slot, including honest no-subject scope explanations. Link actual available/unavailable/not-applicable/not-evaluated results into the five non-cumulative domains. Preserve the old preparation-only contracts beside the new outcomes.

Acceptance: all families execute through both private input modes; equivalent admitted values agree semantically; binary-float versus exact-decimal distinctions remain where required; whole job planning precedes acceptance; no budget/deadline reset; interruptions retain only atomic committed results; cancellation and actual engine defects remain distinct. Every private link resolves, duplicated unequal result slots fail, and no public report envelope or export appears.

## 19. P3-W14: Full core validation, isolation and installed distributions

Additional allowed paths:

```text
phase3/ci_review.md
tests/contract/test_analytical_obligations.py
tests/contract/test_analytical_mutants.py
tests/integration/test_analytical_hero_inputs.py
tests/integration/test_analytical_determinism.py
tests/integration/test_analytical_installed_runtime.py
tests/security/test_analytical_inertness.py
tests/security/test_analytical_adversarial.py
tests/fixtures/micro/phase3_cases.json
tests/fixtures/adversarial/phase3_cases.json
tests/golden/phase3_core_expectations.json
README.md
```

No product repairs are included in this verification unit. A failure records the affected owner and requires an explicitly scoped correction. W01's cumulative collection/driver must already collect these new tests and capture their ordinary evidence without a new workflow path exception.

Exercise every field obligation's core clauses through actual results, not test names or recorded expected values. Read original H7 oracles only from tests. New case files contain independently specified deltas, expected member/state/basis/reason distinctions and source selectors. They cannot overwrite frozen input oracles. Parameterized tests identify each distinct obligation and assertion in the evidence ledger.

Run metamorphic permutations of set-valued input order, exact ID-preserving changes, duplicate paths, added irrelevant data and added relevant contrary evidence. Preserve source-native ordered arrays. Challenge the granularity/frequency convention, eligibility gates and interpretation with independent counterexamples. Record actual authorship and shared tool/source lineage under validation section 16.3; repeated passes by the same assistant do not become independent reviewers. A counterexample requiring a changed product rule becomes a governance item, not a conveniently changed test expectation.

Use actual file/network/native interception with negative controls, import checks, hostile source strings/extensions, repeated invocation and synthetic privacy canaries. Exercise both warm-import behavior and separate import-time isolation. Include large finite graphs, every implemented limit around its boundary, paid sorting/lookup/numeric operations, commit-time faults and stopped finalization. No hidden logging or mutation of supplied content is permitted.

Build the original wheel and sdist, inspect their exact existing 55/65 regular-member allowlists and source hashes, rebuild the wheel from the sdist, compare member content and install offline into a clean runtime. Execute real private analysis on all four heroes in both admitted modes using independently provided test expectations, preserve public refusals and retain all 48 installed module hashes. No tests/oracles/catalogs are installed as a product shortcut. Record platform-generated differences honestly; do not claim whole-archive byte reproducibility or Windows 11 native certification from Windows Server CI.

Acceptance: actual four-profile exact-head cumulative runs, collection/JUnit identity agreement, all required core cases, artifact identities, before/after tracked-byte checks, installed behavior and package inventories, with no silently excluded failures. Package verification is of private core behavior only.

## 20. P3-W15: Final component audit and Phase 3 handoff

Additional allowed paths:

```text
PHASE_3_COMPLETION.md
phase3/delivery_manifest.json
README.md
```

Audit every accepted unit, all intermediate/final changed paths, named repairs, original test identity retention, frozen sources/fixtures/oracles, live guard and all 48 installed modules. Confirm that exactly the planned sixteen modules acquired new behavior and the nineteen remaining slots retained their accepted bytes. Account for each of the 57 fields, all 228 obligation IDs, 24 PCs, forty reasons, twenty-two conditions, 26 shared families and 35 Traces at their actual implemented scope.

Record actual accepted commits, real environments/runs, source-bound test entry points, core limitations, deferred report/public/native duties and unresolved counterexamples. The delivery manifest must hash a complete named tested precursor without self-reference. If later completion/progress/manifest edits create a documentation successor, that exact final head needs its own four-profile run; record the resulting run/jobs/artifacts and independent audit in the review PR after the commit exists.

Acceptance: no missing in-scope capability, no unapproved path, no unexplained regression loss, no test-only substitute for implementation, no false report/release claim and a verified final successor. Submit `PHASE_3_COMPLETION.md` for owner acceptance. Do not merge it or generate the next phase plan automatically.

## 21. Coverage accounting and phase-completion meaning

### 21.1 Field ownership and planned evidence

All ranges below are inclusive. Each SIT-VF field has the four separately indexed P/N/M/B obligations from the frozen catalog; they total 228. An obligation count is distinct from the number of collected tests or subtests.

| Family | Field IDs | Primary owner path | Implementation unit |
|---|---|---|---|
| M001 | SIT-VF001-SIT-VF005 | `analysis/inventory.py` | W05 |
| M002 | SIT-VF006-SIT-VF008 | `analysis/origins.py` | W05 |
| M003 | SIT-VF009-SIT-VF012 | `analysis/process_comparison.py` | W06 |
| M004 | SIT-VF013-SIT-VF016 | `analysis/contribution_profile.py` | W07 |
| M005 | SIT-VF017 | `analysis/contribution_profile.py` | W07 |
| M006 | SIT-VF018-SIT-VF020 | `analysis/contribution_profile.py` | W07 |
| M007 | SIT-VF021-SIT-VF024 | `analysis/origins.py` | W05 |
| M008 | SIT-VF025-SIT-VF028 | `analysis/evaluator_lineage.py` | W08 |
| M009 | SIT-VF029-SIT-VF030 | `analysis/presence.py` | W09 |
| M010 | SIT-VF031-SIT-VF037 | `analysis/presence.py` | W09 |
| M011 | SIT-VF038-SIT-VF040 | `analysis/correction_routes.py` | W10 |
| M012 | SIT-VF041-SIT-VF048 | `analysis/correction_outcomes.py` | W11 |
| M013 | SIT-VF049-SIT-VF050 | `analysis/human_review.py` | W08 |
| M014 | SIT-VF051-SIT-VF053 | `analysis/context.py` | W12 |
| M015 | SIT-VF054-SIT-VF057 | `contracts/evidence.py`, `validation/semantics.py` | W03 |

### 21.2 Evidence ledger and remaining obligations

`phase3/obligation_coverage.json` must retain all 228 exact IDs and source cells, not a replacement summary inventory. For each, separately identify the actual core assertions and any remaining public-envelope/rendering requirements inherited from validation section 10.2. Record exact source/input/expectation identities, immutable implementation/test revisions, collection entry points, environment, actual result and relevant reasons. Cross-reference `phase3/implementation_evidence.json` and the review record without inventing a current file's own hash.

Every core field test checks the value together with its scope, population, basis, required checks, witnesses, reasons, state pairing and interpretation. An expected number alone is insufficient. Of the 57 negative cells, 49 explicitly prescribe an output mutant and eight prescribe input deltas. Preserve this distinction per exact ID. For every prescribed mutant, the independently specified test oracle must first accept the unchanged conforming core baseline, then reject the case with only the named property changed. A validator that rejects everything or a normal production result alone supplies no negative-control evidence. Where the source obligation requires a mutant of a conforming public report, the private test supplies core evidence and the full report-mutant/common-envelope portion stays pending for the reporting phase. Do not relabel a private transport as a conforming public report merely to close an ID.

At Phase 3 completion all 228 IDs must have source-bound core coverage or an explicitly justified clause disposition, and no required core clause may remain unimplemented. Public report/serialization clauses remain separately pending. Therefore the phase must not claim 228 fully closed release obligations solely because 228 core assertions passed. Similarly, mark each shared validation family and Trace only to its actually executed scope. Preserve all reporting, disclosure, file/public/native and release clauses for later implementation.

SIT-VG017 substantive JSON/Markdown parity remains unperformed. SIT-VG010/021/023 and SIT-TR021/026/028/030/031, among others, span later report, disclosure or invocation duties; passing their private-core clauses does not close the whole item. WU9-L14 and native protections remain explicit future owners. No Phase 3 percentage conceals these distinctions.

## 22. Stop conditions and owner decision

Stop the affected work on a frozen-source/fixture change, unapproved path, missing actual predecessor acceptance, contradictory authoritative contract, unsupported temporal convention, new field/reason/metric, input-derived authority, weakened regression/security control, lost full-population blocker, silent truncation, insufficient required CI evidence, or an oracle copied from product output. Record real failures and proposed narrow repairs for review.

Successful Phase 3 delivers a verified bounded private analytical core with all fifteen families, fifty-seven field meanings, actual scoped prerequisite execution, finite graph evidence and honest interruption, while retaining the preparation behavior and documented future reporting/public/native duties. It does not declare v0.1 complete.

The next decision is approval of this exact plan and authorization of **P3-W01**. The current task ends with this planning review package.
