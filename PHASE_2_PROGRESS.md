# PHASE_2_PROGRESS

## Document control

| Field | Value |
|---|---|
| Revision | 0.11 |
| Work unit | P2-W05 intake |
| Owner instruction | 批准并合并 PR #13，再进入 P2-W05 |
| Approved plan | PHASE_2_PLAN.md revision 0.1, sections 2.2, 3, 5-6 and 11 |
| Plan SHA-256 | bea21992edf58b77cfe0f9a128bb31cee9226a9ea5e87b829663a47768227918 |
| Accepted W04 head | 80ea8ab34f5881dcb8b6a307391464c752aa6310 |
| Accepted W04 merge | a1f102d82b7321f47df98f2672b91491cbd7fc9f |
| Entry tree | 351ac074ac2d988a59758b6584168fef9af989a6 |
| Branch | phase2/p2-w05 |
| Status | Intake blocked at proposed P2-W05-R01 test-transition scope; W05 implementation has not begun |
| W05 execution | Authorized within the plan; extra repair paths require explicit approval |
| W05 acceptance / W06 execution | Not granted |

## 1. Accepted predecessor and preserved evidence

PR #13 was merged with expected-head protection after confirming its reviewed head and successful cumulative runs 35422618560 and 35422727694. The resulting merge tree is exactly the reviewed W04 tree. The merge message records owner acceptance and contains exactly one SIT-Phase-Unit: P2-W04 footer. This accepts W04 and authorizes W05 only.

The complete W04 progress revision 0.10 and implementation evidence remain at 80ea8ab34f5881dcb8b6a307391464c752aa6310. PR #13 records its final-head verification, 724 tests per profile and 428 separately counted subtest events. W04's R01 cycle-diagnostic repair, earlier intake and local authoring corrections remain in that history. No failed result or prior approval is rewritten.

Attached theory papers do not replace a frozen engineering source or authorize a new field, diagnostic, analytical algorithm or licensing change. This intake finding concerns the transition between component tests and their planned integration.

## 2. Finding: W04 tests still target the seams that W05 must complete

Plan section 2.2 names _prepare_value and _prepare_utf8 as the private preparation entry points. Section 10 allows them temporarily to return captured data without acceptance while W05 remains pending. Section 11 requires the full captured bundle's structural, identity, reference, endpoint, time and scope-plan checks to finish before acceptance.

The accepted runtime/boundary.py currently routes both names directly to _capture. Its docstrings explicitly identify this as W04-only capture. Three W04 test files call these names and intentionally require a _CapturedBundle for payloads that are valid capture inputs but invalid complete dossiers.

| Source-bound witness | Accepted W04 expectation | Required full-preparation treatment |
|---|---|---|
| test_input_decoding.py::test_byte_and_value_capture_have_equal_content_for_exact_values, source0 | Both {} and its UTF-8 form return _CapturedBundle | The empty root omits all nine required envelope fields in lineage section 2; it cannot be accepted as a dossier |
| test_input_decoding.py::test_captured_unknown_fields_are_not_falsely_claimed_schema_valid | The object containing not_a_declared_field and contract_version=wrong is captured without an acceptance flag | The declared contract label and closed root fields must be checked; full preparation cannot return this as an admitted dossier |
| test_value_capture.py::test_source_relationship_cycles_and_control_words_remain_inert_data | A generic object with relations/instructions/state remains inert captured data | Its generic keys do not constitute the canonical dossier envelope; a separate well-formed cyclic-evidence test is needed for full validation |
| test_input_capture.py::test_isolated_capture_has_no_source_io_network_or_native_loading | The isolated probe expects captured objects from generic path/url/nested inputs | Preserve this capture isolation probe, and separately test complete preparation with valid canonical data and invalid inputs |

These W04 expectations are correct at the capture layer. The missing element is their transition to a clearly named capture-only target when the existing _prepare entry points acquire full W05 behavior. The original W05 allowlist has seventeen paths and omits all three W04 test files. Silently keeping _prepare capture-only and calling W05 complete would leave the planned integration unfinished. Special-casing tests, returning partial captures after structural failure, or dropping existing identities would violate the plan.

This is a test-transition scope gap in the implementation plan/test arrangement. It is not evidence that W04's accepted capture implementation failed, and no unimplemented W05 validator has been reported as an executed failure.

## 3. Actual intake checks and their limits

The current plan, capture wrapper, three affected tests, CI exception logic and transition ledger were read from the connected repository at the accepted merge. Complete local bytes for PHASE_2_PLAN.md and CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md were checked against their connected Git blob identities and the accepted artifact hashes:

| File | Git blob | SHA-256 |
|---|---|---|
| PHASE_2_PLAN.md | 17b91fd2851006d8bd5c14f6ff922a9d8abbeb0c | bea21992edf58b77cfe0f9a128bb31cee9226a9ea5e87b829663a47768227918 |
| CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md | a08e94bee1e4c8aaa4a47fcdd79b1e8db0fe6911 | 32272903b45a8749115ed6b4ec9904dd864a2190f9e1a2ba43ced4c8256c0374 |

The four stored final W04 artifact ZIPs from run 35422618560 were rechecked against their recorded service byte counts and SHA-256. Each contains the correct W04 head, 724 collected identities and 724 direct successful JUnit testcase elements. Five selected witness identities, including both empty-root encodings, passed in every profile. The four 143-file checkout hash maps agree. The sorted 724-node list, joined by LF with one final LF, has SHA-256 4013eaf4cc7ee9c9c8b413300e49ad9ee98bd80db8f43437ac7868c431613a46.

An intake-only check extracted the nine required root keys from the frozen lineage table and identified the missing/undeclared keys in the source-bound examples above. It did not select a new error-precedence rule. This is source-contract compatibility checking plus reinspection of accepted W04 evidence, not a new W05 parser/validator test or a new four-profile run.

A full local Git clone was attempted and failed to resolve github.com. This environmental limitation does not cause the present scope gate and does not alter the connected merge result. No complete local checkout or new selected-toolchain execution is claimed.

## 4. Proposed P2-W05-R01: preserve component tests while integrating preparation

This proposal awaits explicit owner authorization. Keep a plainly named private capture-only seam over the existing capture implementation. Redirect W04 component tests to that seam without changing their inputs, numerical expectations, cycle/alias rules, resource classifications, immutability requirements or event-interception assertions. Complete _prepare_value and _prepare_utf8 as the real full-preparation seams under the already authorized W05 code paths. No public mode switch or caller-controlled validation bypass is introduced.

The five additional immediate write paths requested are:

| Path outside W05's original allowlist | Exact purpose |
|---|---|
| tests/unit/test_input_decoding.py | Explicitly retarget capture-only tests to the capture layer; preserve test names, parameter identities, payloads and all existing capture expectations |
| tests/unit/test_value_capture.py | Retarget the same component boundary, retaining hostile-type, alias, cycle, quota, mutation and immutable-copy checks |
| tests/security/test_input_capture.py | Retarget capture probes, including their isolated process; preserve the audit-hook body and real negative-control events; refine only named scope/preservation regressions needed to recognize this authorization and additive W05 tests |
| tests/scaffold/test_ci_contract.py | Add exactly these five P2-W05-R01 paths to W05 immediate scope and retain them only for cumulative accounting afterward; keep prior W02/W04 exceptions and all workflow/collection/guard controls |
| phase2/transition_ledger.md | Append the explicit old-test-to-component mapping and new full-preparation coverage; preserve historical rows and results |

Within W05's already allowed tests/contract/test_bundle_contract.py, refine the two existing immediate/cumulative exception-accounting tests for this named authorization. The W04 test that pins old test_bundle_contract bodies must continue to verify the original identities and unchanged unrelated assertions, while allowing explicitly identified W05 additions. It cannot be removed or replaced with a count-only check. Original R01 constant-only checks on execution.py and diagnostics.py remain intact; neither product path is requested by this proposal.

New integration tests in W05's existing allowed paths must distinguish the two levels explicitly: the empty or unknown-field object can be captured, but complete preparation rejects it; a valid sparse canonical dossier can complete preparation only after every required check; all four unchanged H7 inputs must pass actual full preparation without importing oracle values into product code. Preserve attributions, lawful gaps and valid evidence cycles. A declaration or successful preparation must never become an independence or truth certificate.

Retain all 724 predecessor collected identities, add new tests, preserve real source-I/O/network/native counterexamples and execute the complete four-profile cumulative suite before W05 delivery. No blanket skip, xfail, deselection, generic-exception pass, test-dependent product behavior or hidden monkeypatch may simulate success.

No frozen specification, approved plan, input schema, fixture, analytical oracle, dependency version, workflow permission, boundary checker, public API/CLI or additional installed package path is included in the repair. The original seventeen-path W05 implementation authority otherwise remains unchanged.

## 5. Actual write scope and stopping point

This intake changes PHASE_2_PROGRESS.md only on phase2/p2-w05. All 48 installed product modules, existing tests, policy, implementation evidence, schemas, catalogs, fixtures, frozen documents and plans retain their accepted W04 bytes. The unchanged policy continues to describe W04; no W05 module has been promoted.

No W05 validator, incomplete-success workaround, test migration or new public interface is committed. No W05 review PR has been opened and no W05 CI result is claimed. The preceding authorized main merge may run the existing W04 CI normally; it cannot certify W05 behavior.

Stop for the named five-path repair authorization under plan sections 6 and 17. After approval, perform that bounded migration together with the already authorized W05 validation work. Any separate specification/fixture defect or additional out-of-scope repair found later retains its own stop rule. W06 and release remain unauthorized.
