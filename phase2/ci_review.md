# P2-W01 CI transition review

Revision 0.1. Scope: PHASE_2_PLAN.md section 7. Status: candidate; hosted evidence pending at initial submission.

## Retained toolchain and permissions

No package version, Python minor, runner family or action revision is changed. The selected action definitions were re-read from the official repositories at their exact commits during this unit:

| Action | Retained commit | Re-read action.yml blob |
|---|---|---|
| actions/checkout | 3d3c42e5aac5ba805825da76410c181273ba90b1 | 5b0524f730db83f9513c18ab31a6c086c7239076 |
| actions/setup-python | 5fda3b95a4ea91299a34e894583c3862153e4b97 | df6c8235b476652b6402d31d92a2a89cdea74bb9 |
| actions/upload-artifact | 043fb46d1a93c77aae656e7c1c64a875d1fc6a0a | 7cb4d1e81db55320b41217e1a78a1a46e3d2baef |

The inherited dependency-review/install function executes unchanged from its exact hash-pinned prior source. It checks selected versions, actual downloaded wheel bytes and PyPI metadata, non-yanked status, notices, vendored metadata, installation and dependency consistency. Direct choices remain setuptools 84.0.0 and pytest 9.1.1; the prior resolved support set remains iniconfig 2.3.0, packaging 25.0, pluggy 1.6.0, pygments 2.20.0, with colorama 0.4.6 on Windows. No transitive or direct version is silently substituted.

Repository permissions stay `contents: read`; persist-credentials stays false. No secrets, elevated trigger, cache, subprocess shell expression from source/PR text, reusable third-party workflow, networked auditor or auto-publish/merge action is added. The four existing OS/minor combinations, 25-minute timeout, fail-fast false and fourteen-day verification-artifact retention remain.

## Enumerated migration

The existing workflow path stays `.github/workflows/phase1-ci.yml`. Display labels, concurrency group and artifact names now identify Phase 2. Checkout fetch-depth changes from 1 to 0 so the driver can inspect exact prior commit archives and the migrated tests can execute only their immutable historical assertions. This adds developer Git-history availability; it grants no product access and uploads no source archive.

The six migrated test files use a closed, hash-verified historical test loader. The loader accepts only fixed test paths, verifies source bytes against the independently pinned composed entry manifest, suppresses the old direct-main dispatcher and supplies no network/mutable-ref fallback. Its execution authority is developer test code, never a dossier, source locator, arbitrary callback or product import. All 194 collected historical test identities remain required.

The original twenty workflow-policy/JUnit tests are inherited unchanged. The new policy validates each enumerated migration delta, then checks the original closed policy. New transition tests exercise the added invariants. Exact result/collection matching, failures/skips and subtest accounting remain inherited and controlling.

## Stage and file authority

The runner event provides a separately validated work-unit context: exact `phase2/p2-wNN` for PRs, or one explicit `SIT-Phase-Unit: P2-WNN` footer for a main push. The actual head and base SHA are checked. Candidate policy must match the context and cannot advance it. The context does not authenticate conversational approval; work-unit execution and merge still require the owner.

The pinned plan supplies closed per-unit path lists. CI compares the actual base-to-head delta against the current list and rejects deletions/renames. It verifies every resolved intake hash against actual local Git archives, then protects current files outside the cumulative authorized lists. Product guards separately protect 48 paths and all unpromoted modules; W01 permits no product promotion.

Collection includes all present scaffold/security/contract/unit/integration directories. Every present test file must collect, all 194 original node IDs must remain, and raw JUnit must cover exactly the collected IDs. No skip, xfail, ignore-failure or count-only success is accepted. New test totals are determined by real collection, not set in advance.

## Primary reference and limits

GitHub's official secure-use guidance was checked for minimum token permissions and immutable full-commit pins: `https://docs.github.com/en/actions/reference/security/secure-use`. Pytest's official node-ID and collect-only documentation was checked for collection identity semantics: `https://docs.pytest.org/en/9.0.x/example/markers.html`.

These sources support narrow tooling choices. No complete fresh audit of all vendor source, new supply-chain certification or vulnerability-database clearance is claimed. The selected actions must resolve and every required step must pass on the actual W01 head. Actual runner images, patch versions, packages, run/job/artifact IDs and failures are recorded after execution. Phase 2 input/schema/analysis/native functionality remains unimplemented in W01.

## P2-W08 intake and required phase-transition repair

Review revision 0.2 is appended here. The complete W01 review above is retained as historical evidence, with its original scope and pending-at-submission wording.

### Authority and actual state

Owner instruction: `批准并合并 PR #16，再进入 P2-W08`.

PR #16 was merged at `22bd51454e425cf9eca87adbebecb09191fb925d` with expected head `384615aeba3e48b3e22486065c5f5e21e092e368`. The merge tree is `7b50c48453f99ed8fbaaf4faaf43b038e07e12da`, identical to the accepted W07 tree. The merge message records W07 acceptance and W08 authorization while retaining the W07 CI footer for the unchanged merged tree.

This intake changes only `phase2/ci_review.md`, a W08-allowed path. No product, test, policy, workflow, source, fixture, dependency or historical ledger is changed. W08 is started but blocked before implementation or its exact-head matrix. No W08 delivery PR is opened merely to trigger a known phase mismatch.

### Evidence reinspection, not a W08 pass

All four locally available complete archives from accepted W07 run `35493868977` were rechecked for service-record byte lengths, SHA-256 and CRC. Their raw JUnit identities equal the collected 1,629 unique nodes, with no failure, error or skipped element. Logs separately show 428 successful subtest events per profile. Sorted LF-joined node IDs, including the final LF, retain SHA-256 `24ae0b74787beee49af3abb9a6eae8fbd24f2aeb0686ddbd37d9220c0c44f1bf`.

The twenty-file and forty-eight-module before/after guard logs pass. All 154 tracked hashes agree across profiles. Executed archive inventories retain 65 ordinary source-distribution members and 55 members in each original/rebuilt wheel; wheel member content hashes agree. These archives hold executed results and inventories, not binary distributions. This reinspection does not claim new package execution or independent rereading of absent binaries.

Post-merge run `35494895328` executes `22bd51454e425cf9eca87adbebecb09191fb925d`. All four jobs and required steps were subsequently read as completed/success. That check is at job/step level; the detailed raw-result reinspection above concerns the accepted W07 run. Neither result certifies a future W08 candidate. Earlier failed W07 runs and repairs remain at their recorded commits and runs.

### Located transition dependency

The pinned plan, revision 0.1 section 14, gives W08 six paths. It omits `phase2/module_policy.json`. The inherited policy says `P2-W07`; the trusted context for `phase2/p2-w08` must be `P2-W08`. The unchanged checker requires equality and will reject the mismatch. The W07-only repair exception does not grant W08 immediate permission to edit the policy.

An isolated execution of the retrieved `policy_promotions` routine reproduced `policy_cannot_select_unit` for the accepted policy under W08. Its 1,492-byte preimage matched Git blob `524697001b70fc83f0ca11b7f0ccc0366bf692af` and the accepted archive's SHA-256. Hypothetically changing only the marker admits the same thirteen promotions; an older trusted context or an added analysis promotion still fails. No repository repair or W08 product-suite run is represented by this probe.

The connected source review also found the downstream test dependencies before making that edit: three older exact-permission test files; W07's literal CI/test-source preservation checks; and four temporary-package cases that call the checker with a hard-coded W07 context. Advancing only the policy would therefore leave further test-context conflicts. This is a plan/test-harness transition gap, not a newly executed product failure. No weakened checker, false W07 context or skipped test is proposed.

### Proposed P2-W08-R01, awaiting explicit approval

Request exactly seven additional immediate W08 paths:

| Path | Bounded change |
|---|---|
| `phase2/module_policy.json` | Only `active_unit`: W07 to W08. Keep format, plan hash, first-unit map and all thirteen promotions byte-identical otherwise. |
| `tests/contract/test_bundle_contract.py` | Only the two named immediate/cumulative permission-test bodies recognize the distinct W08 authorization. |
| `tests/security/test_input_capture.py` | Only `test_r01_exact_four_paths_and_no_other_unit_permission_expansion` recognizes W08 immediate/cumulative scope; all capture observers and other assertions stay intact. |
| `tests/contract/test_input_schema_mapping.py` | Only `test_r02_exact_extra_path_and_other_units_keep_their_immediate_scope` recognizes W08; no field, schema, status or source assertion changes. |
| `tests/contract/test_phase2_transition.py` | Adapt the four W07R01Tests methods named below for the exact W08 delta and add a separately named W08R01Tests regression class. Preserve every other original statement and identity. |
| `tests/security/test_preparation_inertness.py` | Only the temporary-package guard test takes its unit from independently supplied trusted context instead of four hard-coded W07 calls. Preserve its four target parameters, pristine positive controls, mutation and rejection assertions. |
| `phase2/transition_ledger.md` | Append the named assertion migrations, retaining every historical row and result. |

The four W07R01Tests methods are `test_exact_six_paths_are_w07_only_and_history_is_cumulative`, `test_only_four_named_permission_test_bodies_change`, `test_ci_context_collection_and_failure_controls_are_unchanged`, and `test_prior_phase2_transition_tests_keep_every_statement`. Their historical W07 scope and expected transformations remain explicit. Live comparisons must include only the approved W08 delta, with independent fixed-Git-byte and AST regressions protecting all other code; a broad historical-only bypass is not acceptable.

`tests/scaffold/test_ci_contract.py` is already in W08's original list. Its supporting change would register exactly the seven extra paths for W08 and their later cumulative accounting, with an explicit repair evidence label. Preserve event-derived trusted context, the checker, previous immediate scopes, collection, failure handling, workflow and dependency pins. Other units acquire no new immediate permission. Necessary progress/evidence/review updates already belong to W08.

After approval, execute every one of the 1,629 predecessor identities plus actually collected new regressions in all four required profiles. Inspect exact-head raw results, guard outcomes, installed-runtime behavior, exclusions and build/rebuild inventories. Retain any failure. A later product defect or another out-of-scope change still requires a named repair. Do not close any analytical obligation with these engineering tests.

### Stop and later boundary

R01 has not been approved and none of its seven paths has changed in this intake. Public API/CLI refusals remain intact. Only PC01 is complete; PC02-PC24, all fifteen analytical families and all 228 analytical obligations remain pending. No W09 work, public auditing, native file interface or release is authorized.

Section 15 also omits the policy path from W09. That future handoff has a related maintenance dependency; noting it here neither executes W09 nor extends this proposed W08-only authorization. The full preceding review and all approval/failure history remain preserved.
