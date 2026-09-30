# PHASE_3_COMPLETION

## Current decision

Status: **Private-core handoff with approved P3-W15-R01, P3-W15-R02 and P3-W15-R03 implemented; the final four-profile gate and owner acceptance remain pending.** The R01 and R02 hosted runs failed their required gates. R03 authorizes a fixed 2,400-second complete-test process limit and 50-minute CI job limit at a new historical boundary. Its local checks do not establish a hosted pass. [PR #34](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/pull/34) remains unmerged. Acceptance requires a successful exact-final-head four-profile run and its raw-evidence audit. This document is not a Phase 3 completion approval. The owner instructed `验收 W14、合并 PR #33，再启动 W15` on 2026-09-26. W14 PR #33 was accepted and merged at `6dbca96f3314d537beed4ccb6202147bd9248dd9`, preserving reviewed head `016c9d818e556f060edb929104159d057e9ce510` and tree `acedd751af602609c7c228083d770fd7904b7939`.

W15 completed its authorized history, component, source, package-evidence and verification-normalization reviews. It found one concrete required reason distinction missing from the private pipeline. The owner then approved `批准 P3-W15-R01` on 2026-09-26, and the narrow repair and direct controls passed. The existing 228 field assertions and W14 four-profile passes remain actual historical evidence; the new branch has its own source-bound tests.

## Confirmed finding and approved repair

**P3-W15-R01: preserve the unselected-dimension reason.** `VALIDATION_PLAN.md` section 14.2, `SIT-VG014/dimension_not_selected`, explicitly requires an inventory-only Inquiry with empty dimensions and a paired explicitly selected acquisition case. `OBSERVABILITY_AND_REPORTING.md` section 13.2 distinguishes an unselected dimension from a missing applicable subject.

At accepted W14 bytes, `_plan_analysis` falls back to `no_subject`; `_execute_job` and `_planned_nonresults` consequently emit `no_applicable_subject`. The existing `test_no_declared_dimension_cannot_execute_an_implicit_world_dimension` verifies null/not-applicable/no hidden dimension and presence of a reason, but omits the exact code assertion.

Four actual unmodified private calls reproduced the distinction. Both value and UTF-8 empty-dimension modes complete with fifteen affected M002/M004/M005/M006/M007 results carrying only `no_applicable_subject`. The two acquisition-selected controls complete with normal selected-dimension behavior and scoped seed/denominator reasons. All supplied values and tracked source hashes remain unchanged. Reproduction SHA256: `74cef16d42da5094b232d1567f4bced9018a330b3cbeaf38c757c57ba00db462`.

The correction retains completed/not_applicable state, null value, null unselected dimension and structural_inapplicability, and attributes `dimension_not_selected` to the actual Inquiry and affected results. M002/M003/M004/M005/M006/M007/M013 empty-selection cells preserve this declared cause. Actual M008 Evaluations with a role pair receive their own scoped selection reason, including alongside an Evaluation with incomplete roles. Genuine no-subject, incomplete-role and selected missing-comparison meanings remain separate. New selection and input-reference work is charged prospectively under the original quotas.

The original W15 scope contains seven document/record paths. Plan sections 5, 20 and 22 require a named owner-approved amendment before product/test edits. The actual approval adds exactly four paths, for eleven total:

| Additional path | Narrow purpose |
|---|---|
| `src/source_integrity_toolkit/runtime/boundary.py` | Implement the source-mandated dimension_not_selected reason for empty dependency selection on otherwise planned dimension-dependent nonresult cells. Keep no implicit dimension, exact null values/scopes, existing resource accounting and execution/availability separation. |
| `tests/integration/test_analytical_pipeline.py` | Strengthen the existing value/UTF-8 empty-dimension test with exact reason and structural-inapplicability assertions; add or parameterize the paired explicit acquisition case and preserve genuine no-subject/incomplete-role reasons. Retain all existing identities and assertions. |
| `tests/scaffold/test_ci_contract.py` | Add fixed literal W15-only immediate scope exception and history ancestry boundary; retain all preceding scope rules and every intermediate-commit check. |
| `tests/contract/test_phase3_transition.py` | Update narrowly enumerated source-delta oracle and existing scope/history assertions to permit exactly this approved W15 exception. Reuse inherited negative controls against path expansion, future/retroactive permission, missing ancestry and dropped history. |

`tools/check_scaffold_boundary.py` is unchanged: the boundary module has been mutable since W13 and the reason is already registered. R01 left the guard, workflow, pins, timeouts, quotas, frozen specifications/fixtures/oracles and public refusals unchanged. The driver pins actual preapproval checkpoint `e8cf08296f6d335a501a451c777b9de4677ff934`, tree `2f26ad5ae8357d972b61464e42f5229f21ae2ec4` and sole parent `6dbca96f3314d537beed4ccb6202147bd9248dd9`. That checkpoint retains seven-path permission. Its approved R01 successors through the fixed R02 proposal checkpoint receive eleven paths; later R02 successors have the narrower scope below. All prior unit scopes and negative controls remain active; candidate metadata cannot authorize an exception.

The directly tested repair precursor is `2a8697ea23e315e74c7cc8d7632c95725332b45b`, tree `b77e6b508aeee653dd822c7a3414c26c517545eb`. Local CPython 3.12.14 passed 98 semantic/observability/interruption controls, 326 complete transition checks before a test-cache adjustment, 20 unchanged driver controls, and 27 final affected controls after that adjustment. The new tests reuse actual history checks and cache only immutable Git archive hashes by commit ID; every ancestry/path/mutation assertion still executes. First-attempt test-authoring errors and their original failed JUnit are retained. Corrected paired tests passed 13 checks. These local results are distinct from the final hosted matrix.

At the R01 checkpoint, actual collection was 3,937 tests, preserving every 3,918 W14 identity and adding ten semantic cases plus nine scope cases. The hosted gate must also retain 428 separately counted subtests with zero failures/errors/skips. No existing identity, quota or timeout was removed or relaxed.

## Approved verification repair and the blocked hosted gate

**P3-W15-R02: batch actual Git parents/tree metadata within each history-validation call.** The owner approved `批准 P3-W15-R02` at `2026-09-27T04:50:25Z`. The approved proposal SHA256 is `2669a9caae914001cbf9234714670dfadf7fa032843ce4416c55a8dc5c97559f`. Its fixed checkpoint is `4d480f2cc5400e96e724d949ed00c82d62f5aeb7`, tree `bf667ea9d1e46379eee610793c9ecf317ca77276`, with sole parent `2a8697ea23e315e74c7cc8d7632c95725332b45b`. This approval preserves the R01 implementation, original approval checkpoint and semantic assertions.

The actual checkpoint [run 36268092968](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/actions/runs/36268092968) remains blocked:

| Profile | Attempt | Actual result | Pytest time |
|---|---:|---|---:|
| Ubuntu 24.04 / Python 3.11 | 1 | 3,937 tests and 428 separate subtests passed | 1,470.44 seconds |
| Ubuntu 24.04 / Python 3.13 | 1 | 3,937 tests and 428 separate subtests passed | 833.77 seconds |
| Windows 2025 / Python 3.11 | 1 | 3,937 tests and 428 separate subtests passed | 1,554.55 seconds |
| Windows 2025 / Python 3.13 | 1 | `TimeoutExpired`; no complete JUnit | 1,800-second limit |
| Windows 2025 / Python 3.13 | 2 | Same-commit single-job retry: `TimeoutExpired`; no complete JUnit | 1,800-second limit |

All five original artifact ZIPs, service metadata and original/normalized logs remain evidence. Their integrity audit passed; the acceptance audit failed. Successful old profiles cannot be combined with a later profile or a new commit to claim a new four-profile pass. Observed late installation progress does not identify the last executing test or prove an infrastructure cause.

R02 permits only `tests/scaffold/test_ci_contract.py`, `tests/contract/test_phase3_transition.py` and the original seven W15 document/record paths after its fixed checkpoint through the R03 proposal checkpoint. Each commit in that segment must descend from the actual R02 checkpoint and stay within these nine paths. All product sources and `tests/integration/test_analytical_pipeline.py` retain their checkpoint bytes. Earlier commits keep their original scopes; R02 grants no retroactive permission. R02 left the guard, workflows, dependency/action pins, frozen specifications/fixtures/oracles, product quotas and clocks, 1,800-second suite limit and 40-minute job limit unchanged.

The driver uses Git's `%H`, `%T` and `%P` formatting with explicit full commit IDs, no traversal and preserved input order. It rejects missing, duplicate, extra, reordered, malformed or truncated batch records and invalid fields. Metadata lives only within the current `phase3_history` call. Actual `%B` message reads, live `rev-list` and ancestry checks, diff/deletion checks, real archive hashes, every history row and final coverage accounting remain active. Direct controls compare old and new metadata and rejection behavior across ordinary, shallow, missing-object, changed-ROOT, replace-ref and graft scenarios; they preserve the R01 fault assertions and add R02 boundary and batch-integrity controls.

The read-only proposal measurement of nine original history cases passed in 118.663 seconds and observed 2,734 `git_text`, 944 `changed_between` and 1,530 `require_ancestor` calls, without substituting cached query results. After implementation, one sequential local comparison of complete old and candidate history validation used Linux x86_64, CPython 3.12.14 and Git 2.51.1. Actual Git subprocesses fell from 443 to 335; elapsed time was 12.326 seconds versus 10.270 seconds. All 57 returned records were identical. Both executions retained the same archive, diff and `%B` counts; `rev-list` and ancestry counts did not decrease. All 207 tracked file hashes were unchanged during the comparison. The paired receipt SHA256 is `b0aaf79aecd34876c26b0e1656b163982d868db588e375f995d07c456645bde7`; it binds old driver SHA256 `768287a2be11c12a4d35d515307c430d1b48419657826c917813e008e3af9fe0` and candidate SHA256 `48c78cd0f729d96b5cec2ec4c4bae8419edca2bfe8fcf38d86453c14ff256878`. This single local pair does not predict Windows or full-suite savings.

The actual R02 verification precursor `fae43fcdae0341a6f596545f700bc8932b5d8444`, tree `3eea2f22566a262167be115f9be142772cc41a1e`, passed 371 affected controls with 342.81 seconds reported by pytest and 343.616 seconds recorded for the process. Its final collection was 3,962 tests, retaining all 3,937 R01 identities and all 3,918 W14 identities, with 25 individually recorded additions and no removals. The 25 new controls contributed 50.399 seconds of recorded case time, including 33.461 seconds for the complete R02 authority control. No independent paired full-suite timing claim is made.

The actual R02 final head `3a8c6f99a2aa71ce8e67454801e16a1c5c5caed7` executed [run 36296729627](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/actions/runs/36296729627), attempt 1:

| Profile | Actual result | Complete JUnit time |
|---|---|---:|
| Ubuntu 24.04 / Python 3.11 | 3,962 tests and 428 separate subtests passed | 1,330.116 seconds |
| Ubuntu 24.04 / Python 3.13 | 3,962 tests and 428 separate subtests passed | 1,468.238 seconds |
| Windows 2025 / Python 3.11 | 3,959 tests passed, 3 tests failed, 428 separate subtests passed | 1,630.316 seconds |
| Windows 2025 / Python 3.13 | `TimeoutExpired`; no complete JUnit, pytest log or exit receipt | 1,800-second process limit |

The three Windows 3.11 failures occurred when the new missing-parent, missing-tree and missing-commit cases tried to delete read-only temporary Git objects. Each raised `PermissionError [WinError 5]` before its intended fault injection. Follow-up `d32c1499fe7969b9415468ef62c966c38110a090`, tree `1234a087200c5e56d20c7f53aa0d71a828f167fb`, with sole parent `3a8c6f99a2aa71ce8e67454801e16a1c5c5caed7`, preserves the target object's existing mode and adds owner-write permission before actual deletion. The seven real Git scenarios and five source controls passed locally: 12 tests in 15.36 pytest seconds, with all 3,962 identities retained. This follow-up has no hosted certification of its own.

All four original R02 ZIPs passed service-size, SHA256 and CRC checks; both failed jobs retain their original and normalized logs. The evidence-integrity audit passed and the acceptance audit remained failed. The Windows 3.13 timeout has no completed-test count or known complete-run duration. Neither Ubuntu success nor the local object-mode repair establishes the new head's four-profile gate.

## Approved complete-CI budget amendment

**P3-W15-R03: fixed outer CI execution budgets.** The owner approved `批准 R03 继续` at `2026-09-30T15:08:59Z` (`2026-09-30T08:08:59-07:00`). The amendment binds actual proposal checkpoint `d32c1499fe7969b9415468ef62c966c38110a090`, tree `1234a087200c5e56d20c7f53aa0d71a828f167fb`, and sole parent `3a8c6f99a2aa71ce8e67454801e16a1c5c5caed7`.

Only the complete pytest subprocess limit changes from 1,800 to 2,400 seconds and the workflow job limit from 40 to 50 minutes. The existing driver enforces those exact values; its source and workflow controls retain the earlier historical budgets and reject unauthorized alternatives. The fixed product 60-second cooperative deadline, work and witness quotas, all other internal timeouts, four profiles, steps, permissions and dependency/action pins remain unchanged. All 48 product modules and `tests/integration/test_analytical_pipeline.py` retain their R03 checkpoint bytes.

R03 permits ten paths after its checkpoint: the original seven records, the two existing verification files, and `.github/workflows/phase1-ci.yml` solely for the named job-budget change. The historical authority segments remain separate: original W15 seven paths, R01 eleven paths, R02 nine paths, then R03 ten paths. A successor requires actual descent from the R03 checkpoint before it can use this permission. The cumulative accepted-W14-to-final union contains twelve authorized paths; that union does not grant current authority to edit the earlier R01 product or integration-test paths.

The directly tested R03 precursor is `95368b54d17721ff7e975773ea4f3a22e5888ecf`, tree `f8340702fb6793499b1ff9290ea2930363ee79d8`, with sole parent `d32c1499fe7969b9415468ef62c966c38110a090`. Its affected controls passed 372 tests in 67.57 pytest seconds. Actual collection on the directly tested source is 3963 tests, retaining all 3,962 R02 identities and adding 1 individually recorded controls, with no removed identities. The final hosted gate must independently retain 428 separate subtests per profile, with zero failures, errors or skips.

The 2,400-second budget is a finite authorized ceiling. Prior incomplete Windows 3.13 runs do not prove that it will suffice. Any remaining failure or timeout keeps the gate blocked; no automatic budget expansion or blind retry is authorized. A new four-profile run on the actual final head and its original artifacts must be audited before owner acceptance. Earlier successful profiles cannot be carried into this gate.

## Accepted history and preserved implementation

The read-only history audit checked 54 commits through the accepted W14 merge, all fourteen reviewed/merge tree pairs, every intermediate and final changed path, and seven named historical repairs. No unauthorized path, rename or deletion was found. Exactly sixteen planned modules gained analytical behavior, eight preparation modules were extended, five preparation modules retained their entry bytes and nineteen modules remain protected. This yields twenty-nine active modules and forty-eight installed modules. All 118 always-frozen entry files remain preserved.

| Unit / PR | Reviewed head | Accepted merge | Recorded code run | Tests/profile |
|---|---|---|---:|---:|
| P3-W01 / #20 | `ca028b0616a3d345032e0a9d667bf55c56759534` | `4105f840ef3eaaa98da5d9e21c1ed7742bbaa1d6` | 35548424303 | 1786 |
| P3-W02 / #21 | `df670e36b8e0df46ad6d7f66bc03c57932089d6e` | `f5208ac8df7d6e137741a53b7738e66149de34f1` | 35552824387 | 2089 |
| P3-W03 / #22 | `4fba5568cbddd8ac17f07b6268d3d0f8ea5edaeb` | `b932bef422b4ec67b1b313ecae51b0f7e48d72a2` | 35583223616 | 2364 |
| P3-W04 / #23 | `f8fd0c91320e536e46c1e46f1dc5908f9f0f93cb` | `a175d6d4b4153ddc9147301f9db8d247d12e4852` | 35600424202 | 2979 |
| P3-W05 / #24 | `3430368a71e5dc6392c714465e880ad7130abaf0` | `3dd10f987816dffd73e56631b1c4593e9c3f1b54` | 35658806356 | 3179 |
| P3-W06 / #25 | `886fbf5ff6fa541e799c45c9c979696c48ade850` | `5c520dc15010c7f86d4bcfa5f760ff5e11e7e9d4` | 35715623138 | 3341 |
| P3-W07 / #26 | `968d21dc26bbe98358007f863b1e32037d9f9e5d` | `5b685e80585fe19adb0d9b0324b698cf5bb54e42` | 35720935198 | 3397 |
| P3-W08 / #27 | `8ae74d1236342d8e0938d4b56ef1ac537d5c7487` | `c25c827b9c0c2cf84075c79ebbf6c238dee4ca74` | 35771613781 | 3464 |
| P3-W09 / #28 | `eb650a9cccb7ac9b031823fcaac414a1662c14ae` | `06854e067ba849a3699412d54d778fc2abbe1caa` | 35785828269 | 3549 |
| P3-W10 / #29 | `8f22612ea110fca1e5c140bc0f442816c1c94c68` | `82dc7de63e1007f007e527f53ef0ba719e9c1db4` | 35791081540 | 3590 |
| P3-W11 / #30 | `232a72be866ab32f3076e538d4d237aa4aae0970` | `b5cc98b9264e3921fce2dbdba838c63e786cced7` | 35810064794 | 3638 |
| P3-W12 / #31 | `e42e32d9c2f2628204fa3ba12b09c9cab3438bd9` | `db019ea54faf7a08bc841811c3f261a60aa9eb54` | 35814342581 | 3722 |
| P3-W13 / #32 | `cce4d1b11571617b457cbe8a59c52ac0556d852e` | `332e94a007ceb2a955b8e047f45284b431300995` | 35819087672 | 3810 |
| P3-W14 / #33 | `016c9d818e556f060edb929104159d057e9ce510` | `6dbca96f3314d537beed4ccb6202147bd9248dd9` | 35832693910 | 3918 |

The full history receipt and manifest distinguish recorded earlier acceptance from newly inspected raw artifacts. This handoff directly retains W09-W14 four-profile artifacts and W08 Ubuntu 3.11, twenty-five raw CI ZIPs. Earlier W01-W07 raw ZIPs and the other three W08 profiles are absent from the retained handoff; accepted Git records retain their heads, hashes and results. Current retention of all original 1,650 identities is directly checked. The damaged standalone scratch W11 duplicate is preserved; its complete manifest-verified nested copy is the authoritative retained source. Historical W09 reconstructed approval/local-receipt limitations remain disclosed.

## Component accounting and evidence meaning

`phase3/delivery_manifest.json` contains current per-ID dispositions for 57 fields, 24 prerequisites, 40 reasons, 22 finding conditions, 26 shared validation families and 35 Traces. All 228 original field-obligation rows remain unchanged in `phase3/obligation_coverage.json`; their complete source-cell and passed entry-point mapping remains in the source-bound audit receipt. The 49 prescribed output mutants remain distinct from eight input-delta negatives.

Reason accounting has 37 implemented private or safe-transport branches, including the directly verified R01 distinction, and three explicitly dormant/prohibited future-interface meanings. This count describes audited scope, not forty newly executed positive emissions. All twenty-two finding conditions have private implementations and named source-bound behavior evidence. The SIT-VG014 private selection gap is repaired; its public clauses remain open. SIT-VG017 JSON/Markdown parity is unperformed. Public-envelope, report-local IDs, rendering, file capture, native protection, WU9-L14, API/CLI audit activation and release duties remain deferred. Shared-family and Trace entries keep those future clauses open.

Original H7 cases genuinely execute in both modes under unchanged limits, then safely interrupt with the first job cause preserved and zero delivered analytical results. Five committed M001 observations are internal evidence. Separate finite installed cases complete in both modes with exact counts, members and HHI 4/4. These facts provide no complete all-field H7 report, public release, whole-archive byte reproducibility or Windows 11 native certification.

## Verification normalization review

The accepted Verification Governance and Evidence-Semantics Protection policy requires strong analytical/security controls and reduced permanent historical machinery. This W15 review classifies the actual 3,918-node, 72-file collection without deleting any identity:

| Current file-purpose group | Identities |
|---|---:|
| analytical_admission_contracts | 2656 |
| security_evidence_boundary | 393 |
| integration_public_refusal | 303 |
| release_package_current_scaffold_controls | 192 |
| historical_transition_mixed_current_guarantees | 374 |

These are disjoint accounting groups for the historical W14 collection, not automatic retirement lists. R01 added ten integration identities and nine scoped transition identities, bringing its checkpoint total to 3,937. R02 retained every identity and added 25 explicitly enumerated batch-integrity, Git-equivalence and boundary controls, reaching 3,962. R03 preserves those identities and adds 1 named controls, reaching 3963. The original 374 transition identities mix live security/authority controls and historical migration assertions. Retain canonical analytical/admission tests, scope/graph/correction mutation controls, adversarial boundaries, private integration and public refusals, plus the actual cross-platform installed/package matrix.

The concrete consolidation candidates are six hash-pinned historical test loaders, Phase 2 inverse-patch/AST reconstruction, and Phase 3 repair-specific method-preservation chains. Replace each historical mechanism only after an equivalent current positive/negative behavioral guarantee is demonstrated. Keep trusted external context, current path authority, protected modules, forbidden effects, frozen baseline and intermediate-scope checks. Preserve original history, failed attempts and receipts in Git and accepted evidence.

**Executable consolidation has not been performed.** It requires a separately scoped transition authorization and must be completed before the next major implementation phase starts. This review and the three approved repairs do not authorize wholesale removal of historical tests, new registries or another default full-matrix layer. Permanent verification consolidation remains separately scoped.

## Manifest, current checks and remaining gates

The delivery manifest hashes all 207 tracked files at the actual directly tested R03 precursor `95368b54d17721ff7e975773ea4f3a22e5888ecf`, including its then-current checkpoint documents. It preserves the R01 precursor `2a8697ea23e315e74c7cc8d7632c95725332b45b` and R02 precursor `fae43fcdae0341a6f596545f700bc8932b5d8444` as distinct historical snapshots. The failed hosted heads `4d480f2cc5400e96e724d949ed00c82d62f5aeb7` and `3a8c6f99a2aa71ce8e67454801e16a1c5c5caed7`, and the R02 follow-up `d32c1499fe7969b9415468ef62c966c38110a090`, retain their own source-bound receipts. It separately preserves the complete 205-file tested W14 snapshot `5146a2e41dfdddfccebd85367655109288fe313f`, tree `f98de05ee65a7dc20136ea307d84ce04157cab14`, run 35832693910 attempt 1. That earlier run passed 3,918 tests and 428 separately counted subtests per profile. Neither the W14 matrix nor the local direct checks are attributed to the final W15 head.

The cumulative W15 diff from accepted W14 is restricted to twelve separately authorized paths: the prior eleven and the R03 workflow-budget change. The R02 segment remains restricted to its nine paths and the R03 segment to its ten paths; all 48 product modules and the analytical integration test retain their `d32c1499fe7969b9415468ef62c966c38110a090` bytes. All frozen sources and all 228 historical field rows are preserved. The final R03 commit requires a new actual exact-head four-profile cumulative pass, original artifacts, full collection/JUnit identity agreement, all 207 tracked hashes, package members, installed behavior and scope audit. Results will be recorded in PR #34 and the review package after execution, without circular self-hashes or another documentation-only matrix. A failure keeps acceptance blocked; no further timeout increase or blind retry is authorized. Final acceptance must inspect that exact-head receipt.

The 2026-09-26 bounded fixed-pin review found no required change for the current CI path. Actual W15 installations are part of the exact-final-head gate; the known unavailable archive_util advisory-body limitation remains explicit. The source-review receipt supplies the retrieved primary references and limited applicability statement.

All authors and reviewers here are cooperating instances of the same assistant using shared tools and sources. No independent external review is claimed. W15 acceptance, Phase 3 completion, merge, next-phase plan/implementation and release remain unperformed.
