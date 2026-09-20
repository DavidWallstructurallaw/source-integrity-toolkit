# PHASE_2_PROGRESS

## Document control

| Field | Value |
|---|---|
| Revision | 0.16 |
| Work unit | P2-W06: non-cumulative observability preparation |
| Owner instruction | 批准并合并 PR #14，再进入 P2-W06 |
| Accepted W05 head | bf9d7152569495f3eca8fd6b514fe98f6a4bd1f4 |
| Accepted W05 merge | 913f0a3d56b6c0f969e8a36ef7aa909e8ecab470 |
| Accepted tree | 3c3217607a7a26a13fe9f8fdea1fe60b0e50331c |
| Plan | PHASE_2_PLAN.md revision 0.1, sections 3.4 and 12 |
| Plan SHA-256 | bea21992edf58b77cfe0f9a128bb31cee9226a9ea5e87b829663a47768227918 |
| Branch | phase2/p2-w06 |
| Status | Candidate authored; exact-head cumulative verification pending |
| W06 acceptance / W07 | Not granted / not started |

## 1. Acceptance and source boundary

The owner accepted W05 and authorized PR #14 merge and W06. The connector merged
the exact reviewed W05 head after checking the current PR and successful workflow.
The merge tree equals the accepted final tree. W05 retains its 1,320-test, four-profile
final run 35481024914 and the separate 428 subtest events. Its original failures and
R01/R02 repairs remain in history. No W05 evidence is relabeled as W06 execution.

The source of the implementation is the frozen reporting, input and architecture
contract and the approved Phase 2 plan. The six theory papers remain source context;
this work does not replace a frozen specification, license or mathematical claim.

## 2. Exact scope

Only the ten paths in section 12 are used. Three existing product modules change:
contracts/report.py, validation/semantics.py and runtime/boundary.py. Three test files
and prerequisite_partition.json are introduced. Progress, module policy and the
implementation evidence record are updated. No extra path authorization is needed.
The thirteen promoted slots remain the same, and thirty-five protected slots retain
Phase 1 bytes. Existing W05 validators, capture/scalar/limit/budget/diagnostic modules,
old tests, schema, fixtures/oracles, source documents, pins, workflow and public
refusal entry points are unchanged.

The original three module preimages were reconstructed and matched against their
remote Git blob identities before edits. The full local plan and reporting document
match their approved fingerprints. This is a partial workspace, not a full Git clone;
local Git still reports github.com DNS failure. Syntax checks and source mapping
checks do not count as execution of the full candidate or a hosted CI pass.

## 3. Private evidence navigation

The existing W05 _prepare_value/_prepare_utf8 and W04 capture seams keep their
outcome types. Two additional private seams, _prepare_evidence_value and
_prepare_evidence_utf8, run the same admission sequence and then evidence indexing
under the same context, budget and deadline. A tool-owned internal mode selects
navigation, never skips validation and is not a public option. There is one copy of
the admission implementation; its original AST is checked by the new tests after
removing only the post-admission navigation branch and wrapper name.

contracts/report.py owns immutable declarations and source-bound bindings. The
fifteen families and all 57 leaf keys remain visible in every Inquiry. Family-level
question sets are relevance unions from reporting section 14.1, not conjunctive
requirements imposed on every leaf. The five domain labels retain their exact
non-cumulative meanings. No max level, quality score, Result, report-local identity,
public PrerequisiteCheck or available_result_refs is constructed.

validation/semantics.py adds only bounded input observations. Every supplied entity
has a snapshot record with exact selectors, immutable values and explicit field
presence. Missing, null, empty and supplied content remain distinct. Source-native
verified/denied/unknown/failed labels and Gaps are retained without qualification.
No semantic interpretation, source authentication or corrective effect is computed.

Inquiry bindings use a fixed finite sequence: explicit Inquiry/scoped Assertion/
Anomaly anchors; their direct record links; direct subject/target backlinks; and one
final direct-reference pass. Every inclusion preserves its source selector. There is
no repeated reachability expansion, ancestry search, eligible graph, role-pair product
or route/case inference. Other-Inquiry Assertions stay scoped separately. All material
without a direct binding remains visible in the complete snapshot index; an empty
family binding list describes only this finite scan and never real-world absence.
Exact roles, Claims, dimensions, stage/cohort keys and correction tuples stay in the
original source fields rather than being multiplied into hypothetical operations.

runtime/boundary.py assembles those observations according to the compiled bindings.
Only PC01 receives an executed whole-check answer after actual W05 acceptance.
PC02-PC24 retain no whole-check answer and explicitly record their deferred logical
owners and inspected constituent fields. Partial observations cannot certify a PC.
Acquisition gaps do not erase independently supplied correction/process records.

Any failure after admission preserves accepted input state but returns only a safe
diagnostic, never partial navigation. The original emergency reserve, resource
limits, cooperative deadline and cancellation distinctions remain unchanged.

## 4. Verification gate

New tests cover exact source/family/field/domain/PC coverage; stale or inflated
metadata; source selector/value correspondence; null/missing/empty distinctions;
all nine native assessment kinds; inactive/denied assertions; unknown pipeline and
handling outcomes; scope separation; unbound-material retention; immutable ordering;
all four frozen H7 inputs in both modes; per-stage safe stops; the single nonresetting
budget; repeated calls; and genuine file/DNS/native negative controls. Tests do not
pass golden metric answers into the product. Existing 1,320 test identities remain
required and all 428 predecessor subtest events are counted separately.

Commit the exact candidate, run the original four-profile cumulative workflow,
download complete artifacts and inspect actual collection/JUnit, entry/frozen guards,
tracked byte maps and package inventories. No code-path, skip, xfail, failed-platform
exclusion or observation downgrade is permitted merely to obtain a green result.
Record code-head evidence, then verify the final documentation successor on its own
exact head. Keep the review draft until evidence is inspected. Stop for W06 owner
acceptance; do not merge this work, start W07 or publish a release automatically.
