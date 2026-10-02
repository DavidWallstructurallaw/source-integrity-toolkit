# Source Integrity Toolkit Verification Consolidation

Revision: 0.2
Checkpoint: VC-02
Status: VC-01 and VC-02 completed; VC-03 through VC-06 remain pending.
Latest owner instruction: `VC-02 go`.
Execution date: 2026-10-02 UTC.

## Accepted authority and scope

The owner approved [VERIFICATION_CONSOLIDATION_PLAN.md](VERIFICATION_CONSOLIDATION_PLAN.md), SHA-256 `a94b59a0bfdbde3c70c7286fd48c5e0cbdb4a538afeb094ba97dce718bd7d11d`, and started VC-01. The plan is stored with its originally reviewed bytes. Its drafting-time pending header is superseded by this later instruction, without rewriting the approved document.

VC-01 performed baseline verification, one-time guarantee mapping and bounded historical-cost measurement. Its published checkpoint is `a47ea2480043c2bb267c047b2d99a67ab4428e53`. The following baseline sections retain that checkpoint's findings. The VC-02 section below records the newly implemented direct controls. Neither checkpoint retires tests, changes the default CI workflow or claims completion of the whole consolidation.

The consolidation branch starts at accepted Phase 3 merge `2413a29b839b7e1de8f76a449762f031de19d52b`. Remote main and merged PR #34 were rechecked. The accepted tree `e2f230bdf6f838f3d12df233559732aa1d5c1699` equals directly tested head `90684996eac568af6129973764fe40f3b666a15f`.

Only these records are added at VC-01:

```text
VERIFICATION_CONSOLIDATION_PLAN.md
verification/consolidation_map.json
VERIFICATION_CONSOLIDATION_COMPLETION.md
```

All 207 inherited files retain their accepted contents and modes, including all 48 product modules, all tests, the workflow, dependencies, normative specifications, fixtures and golden expectations. The one-time probe and inventory-generation helpers were executed outside the repository. They are not imported by tests or CI.

## Baseline and original execution evidence

The fresh local collection contains exactly the original 3,963 unique test identities in 72 files. No test was removed or added. Directory counts remain:

| Directory | Identities |
| --- | ---: |
| contract | 2,044 |
| unit | 1,021 |
| security | 393 |
| integration | 314 |
| scaffold | 191 |
| Total | 3,963 |

The four original artifact ZIPs for [run 36736103966, attempt 1](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/actions/runs/36736103966) were read directly. Their collections, exact JUnit identities, successful summaries and before/after source hashes were checked against the accepted baseline. Each profile passed 3,963 tests and 428 separately counted subtest events, with zero failures, errors and skips.

| Original profile | Full pytest seconds | Phase 2 transition case seconds | Phase 3 transition case seconds |
| --- | ---: | ---: | ---: |
| Ubuntu 24.04 / Python 3.11 | 1,551.97 | 133.962 | 114.031 |
| Ubuntu 24.04 / Python 3.13 | 1,468.30 | 101.094 | 79.260 |
| Windows 2025 / Python 3.11 | 2,198.76 | 148.211 | 529.608 |
| Windows 2025 / Python 3.13 | 1,973.83 | 113.598 | 424.429 |

The last two columns sum original top-level testcase durations. Those files also contain valid current controls and an installed-runtime test. Their entire execution time cannot be classified as removable overhead. These are original Phase 3 results, not a new VC matrix or an optimization claim.

Original package/member, installed-runtime, public-refusal and hero outcome limitations remain unchanged. The immutable R03 review package retains SHA-256 `81d7e9b02f71405ff0f3c13a7dd2fc198d9ae1e05762a94390582f49c6a63267`. Missing earlier W01-W07 raw ZIPs and three W08 profiles remain disclosed; no missing original artifact was fabricated or reconstructed as an original.

## Guarantee inventory

[verification/consolidation_map.json](verification/consolidation_map.json) accounts for **550 identities, grouped under 211 test functions, across 13 files**. Grouping keeps parameterized cases explicit without repeating every function's source description. Each row records the effective function source, its immutable commit and digest, assertion locations and helper calls, the concrete case and fault class, planned disposition, existing or proposed target nodes, original execution provenance and the retirement gate.

| Covered area | Identities |
| --- | ---: |
| Six historical-loader wrapper files | 118 |
| Phase 2 transition file | 57 |
| Phase 3 transition file | 352 |
| Five mixed files, only the plan-enumerated portions | 23 |
| Total | 550 |

The other **3,413 identities** are retained outside this migration inventory. Their set digest and all original source digests are recorded. Entire mixed files are not retirement candidates.

| Planned disposition | Identities | Present status |
| --- | ---: | --- |
| Materialize current assertions from the six wrappers | 118 | Existing behavior retained; direct source materialization pending |
| Retain direct behavior and adapt context wiring | 7 | Existing behavior retained; adaptation pending |
| Replace historical coupling with current direct controls | 410 | Replacement targets specified; equivalence not yet executed |
| Archive obsolete historical implementation forms | 15 | Archive conditions specified; nothing retired |

Every one of the 550 identities has a disposition. The map describes 23 guarantee groups and 20 proposed current-control entrypoints. Those proposed entrypoints are explicitly marked unimplemented. They are a finite implementation checklist, not passed tests or an executable authority registry.

The map permits no retirement at this checkpoint. VC-02 through VC-04 must establish actual positive/negative equivalence, including distinct parameter and subtest cases and delegated helper assertions. A missing proof keeps the old check active.

## Findings that constrain implementation

1. **Preserve the installed preparation witness inside the Phase 2 transition file.** It checks all four original heroes in value/UTF-8 modes, exact installed bytes for 48 modules, PC01-only preparation, empty-input refusal, public refusals, no normal effects, real file/network/native observation probes, and wheel/sdist/rebuilt-wheel membership. The analytical installed witness does not replace this separate preparation coverage.
2. **Preserve current destructive guard observers in the wrappers.** `W04R01LiveGuardTests` and `LiveModuleManifestTests` verify actual syntax, size equality and one-byte excess, optimized-Python CLI behavior, active module effects and owner annotations. Materializing old tests must carry these effective current overrides and helpers with them.
3. **Keep real history rejection controls.** Restored forbidden edits, side branches, mismatched parents/trees, missing ancestry and candidate-selected authority remain distinct failure classes after the old phase replay is removed. A final net diff alone is insufficient.
4. **Keep Git metadata integrity where that helper remains.** Malformed, reordered, truncated and missing batch responses, missing objects, replace/graft behavior and changing ROOT/Git state need current expected outcomes, without an old-implementation equivalence oracle or cross-root cache.
5. **Preserve installed evidence routing.** The protected analytical installed test emits `w14-installed-runtime.json` under `RUNNER_TEMP/sit-p3/evidence`. Keep that directory and both the W08/W14 receipt names in the authorized driver/workflow. The historical W14 test-origin label does not grant current authority; the receipt still binds its real head. This avoids an unnecessary edit to an out-of-scope integration file.
6. **Keep valid frozen-source and packaging checks.** `check_phase0_baseline.py`, current source-effect AST analysis, package inventories and direct normative-source checks remain useful. A historical-looking filename, hash or AST operation is not sufficient reason for retirement.

No additional file permission or product change is needed to begin VC-02 under the approved scope. Any newly discovered requirement outside that scope remains subject to the plan's narrow amendment rule.

## Bounded local measurement

The accepted baseline was measured before adding the VC records. Local tooling was restored into a separate environment from the retained offline wheelhouse, using the existing pins: pytest 9.1.1, setuptools 84.0.0, iniconfig 2.3.0, packaging 25.0, pluggy 1.6.0 and Pygments 2.20.0. No repository dependency changed.

| Probe | Result |
| --- | --- |
| Full collection | 3,963 identities; original set unchanged |
| Collection elapsed | 1.431 seconds; six direct `git show` launches |
| Representative historical checks | 10 passed; pytest reported 14.94 seconds |
| Instrumented measurement elapsed | 14.982 seconds |
| Direct Git launches during that measurement | 257: archive 22, diff 53, ls-files 13, merge-base 33, rev-list 13, rev-parse 5, show 118 |
| Outer measurement bound | 600 seconds; completed within it |
| Source integrity | All 207 inherited file hashes unchanged before/after both probes |

The measurement environment was Linux / CPython 3.12.14. It is not one of the four hosted acceptance profiles. The audit hook counts direct child launches observed inside the pytest process, not descendants' subprocesses. The ten selected cases cover representative inverse-patch, source-shape, authority-chain and finite-budget checks; they do not represent execution of all 550 mapped tests or the whole suite.

The map embeds the selected node list, per-stage results, raw small measurement log, tool/platform details, JUnit digest and the one-off probe source for later comparison. The full collection is tied to its exact set digest and the already preserved original artifacts. Future timing comparisons must use matched environment and workload conditions; this checkpoint establishes no speedup percentage.

## Checkpoint validation and next step

VC-01 validation checks:

- Original accepted merge, tested tree and remote main agree.
- Approved plan bytes are unchanged.
- All 550 mapped identities occur exactly once and exist in the original collection.
- The 211 effective function implementations resolve to one pinned current or intake source each.
- Existing target references resolve; proposed targets are marked pending.
- Original four-profile collection/JUnit/source records agree with the baseline.
- All inherited blobs/modes remain unchanged; only the three authorized records are added.
- No product, test, guard, workflow, dependency, fixture or golden file changes occur.

This is a single-agent inventory and verification exercise; no independent second-review claim is made. No new full matrix is required for the inventory-only checkpoint, and none was started. The final consolidation gate still requires the complete current suite and all four hosted profiles on the actual final candidate head.

The VC-01 handoff was to establish accepted-anchor/frozen-byte authority, exact external context and scope, current module/effect, collection/JUnit and post-anchor history controls. All original checks remain until their replacement gate is met.

## VC-02: current direct controls

The owner subsequently instructed `VC-02 go`. This checkpoint changes exactly four approved paths:

```text
tools/check_scaffold_boundary.py
tests/contract/test_verification_boundary.py
verification/consolidation_map.json
VERIFICATION_CONSOLIDATION_COMPLETION.md
```

All 48 product modules, all 72 original test files, the workflow, dependencies, build configuration, schemas, fixtures, golden expectations and historical records retain their accepted bytes. The approved consolidation plan remains SHA-256 `a94b59a0bfdbde3c70c7286fd48c5e0cbdb4a538afeb094ba97dce718bd7d11d`. The mapping remains review data and never supplies executable authorization.

The new explicit `VC` entrypoint checks:

- The accepted merge's exact commit, tree and ordered parents, and the approved plan's actual bytes. Git object batches are size-framed and content-hash verified; missing, reordered, extra, malformed and substituted records fail closed.
- The exact 20-path ceiling, frozen file contents/modes, the actual index and filesystem, and separately supplied runner event/head context. Candidate manifests, map entries and phase environment values cannot enlarge authority. Staged changes restored only in the worktree and assume-unchanged flags do not conceal edits.
- Every commit after the accepted merge, including merge side branches and forbidden edits later restored. Shallow history, grafts, replace refs, missing necessary objects, wrong ancestry and wrong parents are rejected. No pre-acceptance phase DAG is replayed by the new path; no cross-root or cross-invocation trust cache is retained.
- The current 48-module inventory, 29 active / 19 protected slots, byte ceilings, source effects, dependencies and cycles. Source-tree inspection includes ignored files and directory boundaries. These checks are separate from VC's complete product-byte freeze.
- Complete, unique current collection files/identities and exact JUnit identity reconciliation. Successful subtest events are accounted separately; same-count substitution, false zero summaries, hidden failures and skips fail. The legacy driver's historical identity requirements remain active pending retirement.
- The actual workflow's candidate checkout, read-only permissions, fixed Action pins, four profiles, isolation, 50-minute job budget, complete stages and always-run failure evidence/upload. The 2,400-second suite budget is unchanged. The default driver switches to these APIs in VC-05.

The independent new test file has 21 test functions, expanding to 121 cases. Nineteen of the map's twenty proposed canonical entrypoints are exercised. The historical-loader absence entrypoint remains pending VC-03, because all six wrappers still load historical source.

### Executed evidence

Local execution used the same pinned offline tools as VC-01, on Linux / CPython 3.12.14. This is a development checkpoint, not a hosted acceptance profile.

| Check | Result |
| --- | --- |
| All new current controls | 121 passed |
| Six existing wrapper suites, four preparation guard mutations and related dependency controls | 130 passed |
| Combined targeted run | 251 passed, 91 subtests passed, 0 failures/errors/skips; 144.53 seconds |
| Independent collection/JUnit reconciliation of that run | 251 top-level identities plus 91 separate subtest events match |
| Full repository collection | 4,084 unique identities in 73 files; all original 3,963 retained, 121 added, none removed |
| Collection set SHA-256 | `2be0ab4b33375cf01217c28ca0ed19ff45855a6f3ccd9b0dff31cd7575e42e02` |
| Existing live-migration-source diagnostic | 1 passed; its six protected sources remain unchanged |
| Old W04 exact guard-byte oracle diagnostic | 1 failed on the new guard hash; retained pending approved historical-chain retirement |

The targeted run selected affected controls explicitly. It is not a filtered full-suite success claim. The map's `vc02_execution` section retains selectors, expanded new nodes, source hashes, collection accounting, raw logs and JUnit records, including unsuccessful development attempts.

The initial run exposed a footer parser that incorrectly included preceding blank lines: 108 passed and 1 failed. That defect was corrected. A later collection attempt rejected the reserved pytest parameter name `request`; it was renamed to `commit_ids`. The final targeted run includes both corrections and additional ignored-source / missing-object cases. Earlier failures are retained as failures.

The old W04 source hash expects the pre-consolidation guard. Its failure is the intermediate bootstrap situation explicitly approved in plan section 4. The check has not been weakened, skipped, relabelled as passed or deleted. Complete-suite acceptance remains pending the later migration and retirement gates.

### Remaining boundaries

The legacy default driver and all old test identities remain active. Per-node replacement equivalence and retirement approval remain pending. The mixed-file control currently preserves all non-enumerated top-level code; dedicated import/constant cleanup and the preparation witness's fixture adaptation are deferred to VC-03 within the approved scope.

The current control does not establish a security boundary against an actor replacing both the verifier and its trusted event source. Synthetic event tests and local Git checks do not constitute a hosted GitHub event or completed matrix. No full matrix, implementation PR, merge, product change or release was performed at this checkpoint.

**Next: VC-03, materialize the six current test wrappers and adapt the approved mixed-file dependencies.** VC-04 retires proven historical chains, VC-05 switches the CI/developer entrypoints, and VC-06 performs final four-profile acceptance on the exact completed candidate.
