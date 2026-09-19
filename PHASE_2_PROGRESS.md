# PHASE_2_PROGRESS

## Document control

| Field | Value |
|---|---|
| Revision | 0.12 |
| Work unit | P2-W05 / approved P2-W05-R01 migration |
| Owner instructions | 批准 P2-W05-R01; 完成远程交付，再继续 W05 |
| Accepted W04 merge | a1f102d82b7321f47df98f2672b91491cbd7fc9f |
| W05 intake | fb698272165303660092f02974a99ebbb2748a4c |
| Approved plan | PHASE_2_PLAN.md revision 0.1, sections 3, 6 and 11 |
| Plan SHA-256 | bea21992edf58b77cfe0f9a128bb31cee9226a9ea5e87b829663a47768227918 |
| Branch | phase2/p2-w05 |
| Status | Materialized R01 migration submitted as an intermediate W05 commit; full validation and exact-head CI remain pending |
| W05 acceptance / W06 | Not granted / not started |

## 1. Authority, source and history

The owner approved the five-path P2-W05-R01 migration described in intake revision 0.11 and requested remote delivery before continuing W05. That intake remains unabridged at fb698272165303660092f02974a99ebbb2748a4c. The accepted W04 code and its complete 724-test four-profile evidence remain at 80ea8ab34f5881dcb8b6a307391464c752aa6310 and PR #13. Main remains on the accepted W04 merge. This work does not amend a frozen specification, source paper or analytical oracle.

The preceding turn produced a hash-guarded local changeset but had no remote write action. This turn re-read the unchanged branch and obtained the Git write actions. Local Git still cannot resolve github.com. The remote write restriction is therefore resolved through the existing authorized connector, not by changing repository permissions, secrets or CI authority.

## 2. Exact migration materialization

The migration changes exactly eight existing paths. Seven implementation/test/ledger files were reconstructed as complete bytes and verified against both the changeset's accepted Git blob identity and SHA-256 before applying any edit. Every exact replacement was required to occur once. The eighth file is this updated progress record. No source file was normalized to make a fingerprint match.

runtime/boundary.py adds _capture_value and _capture_utf8 over the existing capture implementation. All existing functions remain byte-equivalent. The three W04 component test files import those names under their original local aliases, including inside the isolated probe. Inputs, expected capture outcomes, numerical and resource rules, parameter identities, audit-hook body and real negative controls remain unchanged.

The CI driver registers exactly the five approved W05 exception paths. Only the named immediate/cumulative scope assertions in test_bundle_contract.py and test_input_capture.py are refined. W02 and W04 exceptions remain intact. The transition ledger retains its full historical bytes with the previously prepared append; its local/pending wording describes the preparation of that append and is superseded for remote transport by this progress record and the subsequent commit/PR evidence.

## 3. Actual verification and current limits

All seven preimages matched their expected Git blobs and SHA-256. All six Python postimages parse successfully. The two unit-test files differ only by the specified import line. The isolated probe differs only by its import target. This materialization is in a partial workspace, not a fabricated full Git checkout. No hosted matrix, complete W05 validator or successful input acceptance is claimed by these checks.

The original _prepare_value and _prepare_utf8 still have temporary W04 capture behavior in this intermediate commit. W05 must replace that behavior with complete bounded structural, identity, reference, endpoint, time and immutable scope-plan validation. Public audit exports and CLI remain refusal stubs. A migrated component test cannot substitute for a full-preparation test.

The phase policy still describes accepted W04 behavior until the following W05 implementation commit records the actual promoted modules. No CI pass is borrowed from W04 or manufactured for this intermediate record. Final delivery requires all 724 predecessor identities plus the added W05 tests, full Linux/Windows and Python 3.11/3.13 checks, actual frozen/entry bytes, package inventories and clean-install verification.

## 4. Continuation gate

Continue W05 under its seventeen original paths and the five expressly approved R01 additions. A genuine fixture, specification or further out-of-scope defect retains the plan's stop rule. Do not edit frozen fixtures, lower limits, weaken observers, add a public bypass, mark analytical prerequisites complete or begin W06. Final acceptance and merge remain with the owner.
