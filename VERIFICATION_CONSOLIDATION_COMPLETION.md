# Source Integrity Toolkit Verification Consolidation

Revision: 0.1  
Checkpoint: VC-01  
Status: VC-01 completed; VC-02 through VC-06 remain unexecuted.  
Owner instruction: `批准整合计划，启动 VC-01`  
Instruction time: 2026-10-01 19:54:10 America/Phoenix / 2026-10-02 02:54:10 UTC.

## Accepted authority and scope

The owner approved [VERIFICATION_CONSOLIDATION_PLAN.md](VERIFICATION_CONSOLIDATION_PLAN.md), SHA-256 `a94b59a0bfdbde3c70c7286fd48c5e0cbdb4a538afeb094ba97dce718bd7d11d`, and started VC-01. The plan is stored with its originally reviewed bytes. Its drafting-time pending header is superseded by this later instruction, without rewriting the approved document.

This checkpoint performs baseline verification, one-time guarantee mapping and bounded historical-cost measurement. It does not implement the proposed current controls, retire tests, modify CI or claim completion of the whole consolidation.

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

**Next: VC-02, establish current direct controls.** Start with accepted-anchor/frozen-byte authority, exact external context and scope, then actual current module/effect, collection/JUnit and post-anchor history controls. Use the map's proposed witnesses and keep all original checks until their replacement gate is met.

VC-02 has not started in this checkpoint. The complete candidate will use the one planned implementation PR. Main is not merged, and public auditing, report/native work, the next major phase and release remain outside this checkpoint.
