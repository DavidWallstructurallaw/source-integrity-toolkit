# PHASE_2_PROGRESS

## Document control

| Field | Value |
|---|---|
| Revision | 0.5 |
| Work unit | P2-W02; limited repair P2-W02-R01 |
| Current owner instruction | 批准限定修复 P2-W02-R01 |
| Approved plan | PHASE_2_PLAN.md revision 0.1 |
| Plan SHA-256 | bea21992edf58b77cfe0f9a128bb31cee9226a9ea5e87b829663a47768227918 |
| Accepted W01 / PR #10 merge | 41e7ba2f8046b3791f860313ea3ad54dcd4cb25c |
| Repair intake | 22d43e003eae9b84ed5868696ec3847216a8a16f |
| Branch / review | phase2/p2-w02; PR #11 |
| Tested repair code | 405b16f1d8d713cd6776fe16793757eb313bbdf2 |
| Tested code tree | 527151ee97ca3f705379b0a7d5d5a65e37bee3b4 |
| Status | Four-row repair-code verification PASS; exact successor-head check remains the final delivery gate |
| W02 acceptance / merge | Not granted |
| W03 and later | Not started |

## 1. Authority and preserved history

The owner accepted W01 and requested W02 through `批准并合并 PR #10，再开始 P2-W02`. The actual expected-head-protected merge is recorded above. Its tree equals reviewed W01 tree ac8bb232d929d18fc56fc053be1b37fb354957ce. The later instruction `批准限定修复 P2-W02-R01` authorizes only the previously described test-harness repair, bounded CI path exception, associated regressions and necessary evidence records.

Unabridged W01 progress revision 0.2 remains at 8e3af5e5b5f4ca9879add9bdd934603e307e6abf. W02 candidate revision 0.3 remains at f7a1f9f69351951162142d4bf41a554de89dcb53. Blocked revision 0.4 remains at repair intake 22d43e003eae9b84ed5868696ec3847216a8a16f. These records preserve source checks, original design, local and hosted failures, diagnosis and the exact requested exception. This revision updates current status without rewriting that history or the approved plan.

## 2. W02 implementation scope remains unchanged

The original fifteen plan-section-8 paths contain five private contract modules, the local-reference input structural schema, coverage records and component tests. There are fifty closed shapes, 242 named field declarations, twelve record kinds, twenty-four relation predicates and nine assessment kinds. Local immutable representations preserve missing fields, explicit null, supplied attribution and unresolved context. Their constructors take bounded project-owned parts and do not establish whole-bundle acceptance.

R01 does not change any product module or schema. Forty-three installed modules still retain their Phase 1 bytes. The same five W02 contract modules remain the only active implementation slots. Public API/CLI refusal, version 0.1.0.dev0, frozen specifications/plans, fixtures, logical oracles, original catalogs, dependency pins, package configuration, boundary checker and workflow remain unchanged by the repair.

Number conversion, J measurement, quotas, bounded parsing/capture, global validation and observability execution remain later work. All whole-prerequisite completions and analytical Trace closures remain empty. Thirty identified runtime validation duties and 228 domain behavior obligations remain pending. Structural-aid tests do not claim metaschema or complete-instance validation.

## 3. Exact P2-W02-R01 changes

Only three test files change in the repair-code commit:

| Path | Authorized change |
|---|---|
| tests/security/test_scaffold_inertness.py | Preload the specific dataclasses helper before the existing observer; add one isolated regression with positive and deliberately omitted-preload controls |
| tests/scaffold/test_ci_contract.py | Add exactly these two existing-file exceptions to W02's immediate path allowance; retain them in cumulative accounting without granting later units new immediate edit permissions |
| tests/contract/test_bundle_contract.py | Append six repair tests for exact scope, future-unit boundaries, unlisted paths, invalid contexts and preservation of the complete original observer/assertions |

The entire existing security PROBE string is byte-identical after removing the two explicitly inserted comment/import lines. A regression loads the prior harness from its fixed Git commit, checks blob a7a876006eb75ab5c3542e01f4b72c8a7483519f, and compares the old/new syntax trees after accounting only for that preload and the one added test. Every existing observation rule, filesystem wrapper, API refusal, mutation probe and event-specific assertion remains intact. Original W02 contract tests remain an exact prefix of their repaired file.

The clean-interpreter regression uses -I -S -B, installs an all-open rejection hook after preloading, creates and freezes a synthetic dataclass, and requires success without a file-read event. Removing only the dataclasses preload must fail on the real post-preload read. This does not broaden the shared observer's read permission.

The two-file exception is fixed in developer code; neither evidence nor module-policy metadata can supply an extra path. Immediate allowances for all other units remain their exact approved-plan sets. Cumulative accounting remembers the accepted W02 exception, and does not itself authorize a later edit. The actual raw plan pin and runner-derived unit context remain controlling.

The repository delta for W02 is now exactly seventeen paths: the original fifteen plus the two expressly approved existing test paths. Necessary final records update only this file and phase2/implementation_evidence.json.

## 4. Local checks and previous failures

All three original test files were re-read and their locally reconstructed bytes matched to connected Git blob identities before editing. New outgoing blobs also matched locally calculated identities before the branch advanced. Local isolated preload and scope-helper checks passed in a partial workspace; no full local Git checkout, cumulative suite or selected-toolchain execution is claimed. Direct local Git access still failed DNS resolution. An authoring-only helper script had a quoting syntax error, corrected before any repository write; this was not a product or hosted-test failure.

The earlier f7a1f9f run 35411043925 failed preflight because the transmitted policy JSON missed a closing brace. ff6c1eb restored the exact locally valid bytes, without changing the guard. Run 35411233144 then executed 367 tests per row with 360 passing and seven shared security failures. Those failures were caused by an unpreloaded dataclasses loader read under the application stack. All old artifacts and failure records remain preserved. They are superseded by the new execution below, not relabeled as passes.

## 5. Actual repaired-code verification

Run 35414689827, attempt 1, executed exact repair-code commit 405b16f1d8d713cd6776fe16793757eb313bbdf2. All four jobs and all required stages succeeded with the original selected toolchain.

| Profile | Actual CPython | Job ID | Top-level passes | Failures / errors / skips |
|---|---|---:|---:|---|
| Ubuntu 24.04 | 3.11.16 | 105820875765 | 374 / 374 | 0 / 0 / 0 |
| Ubuntu 24.04 | 3.13.15 | 105820875898 | 374 / 374 | 0 / 0 / 0 |
| Windows Server 2025 | 3.11.9 | 105820875883 | 374 / 374 | 0 / 0 / 0 |
| Windows Server 2025 | 3.13.15 | 105820875824 | 374 / 374 | 0 / 0 / 0 |

Every row retains the exact prior 367 collected identities and adds seven repair tests. This includes all 221 W01 identities and all 146 original W02 instances. Raw JUnit has 374 top-level testcase elements and 802 total reported events, including 428 separately counted successful subtests. No test is removed, renamed, deselected, skipped or xfailed. All seven previously failing security identities now pass with their original assertions.

Every row recomputed actual 124-file Phase 1 and 125-file intake Git archives, checked the seventeen-path delta and explicit R01 exception, and ran the twenty-file freeze and forty-eight-module guards before and after testing. All 137 tracked file hashes remained unchanged during execution and matched across rows. Three repair-file hashes matched local authoring bytes. All other file hashes agree with prior checked content except the previously recorded progress/evidence updates.

Actual setuptools 84.0.0 and pytest 9.1.1 installation, reviewed development-wheel checks and dependency consistency passed. All packaging and clean offline-installation tests passed. Source distributions retain 65 regular members, wheels retain 55 members, and original/rebuilt wheel member names and content hashes agree. No full compressed-archive reproducibility claim or native file-interface certification follows.

## 6. Inspected complete evidence

All four full ZIP artifacts were downloaded and matched to Actions byte counts and SHA-256, then checked for head/run/environment, collection identities, raw JUnit, original failed identities, new repair tests, all guard logs, entry/scope records, tracked hashes, installed versions and build inventories.

| Profile | Artifact ID | ZIP bytes | SHA-256 |
|---|---:|---:|---|
| Ubuntu 3.11 | 10574943187 | 44986 | 529abc4803a3d26509dcb34d708e705a2e7e394f5878747313ea136169e9f6c3 |
| Ubuntu 3.13 | 10575586311 | 44816 | ae547e5aecf80ae86595fe38f3266e29a9771871a630b3b8ee47a202bdafde3e |
| Windows 3.11 | 10574863299 | 51150 | 814a09b0657fa2b6f1210caa996cc1c7793db734a576088ab35832f71b2339e3 |
| Windows 3.13 | 10575821087 | 50967 | 22d63def81af90b7a4fa7bd74f780678e25c72e9cfd1148278cb5c3a729fcf32 |

## 7. Final record-head gate and stop

The successor containing this progress record and its implementation-evidence update changes only those two records. It must independently pass exact-head four-row CI before PR #11 is marked ready. Record that final successor, run and checked artifacts in the PR to avoid referring circularly to this file's own commit. A green precursor alone cannot satisfy this gate.

R01's code and cumulative tests now pass. Completion of the final gate establishes W02 technical readiness only. Owner acceptance and merger of PR #11 remain separate actions. Main stays at accepted W01 commit 41e7ba2f8046b3791f860313ea3ad54dcd4cb25c until separately authorized. A future authorized merge requires exactly one SIT-Phase-Unit: P2-W02 footer. Do not merge automatically or start W03.
