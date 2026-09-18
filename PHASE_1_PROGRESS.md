# PHASE_1_PROGRESS

## Current control record

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Revision | 0.12, P1-W06-R01 authorized repair candidate |
| Date | 2026-09-18 UTC |
| Owner repair instruction | `批准`, responding to the explicit P1-W06-R01 two-file repair and four-row rerun request |
| Approved plan | Revision 0.1, Git blob `27ed33cb1c2afc78b12ca099ee7ccb4e68d63bfb` |
| W05 merge / unchanged main | `ecf4eb5126201a7c31250c6dae8cbe2c64f9066a` |
| Pre-repair W06 head | `8ea5becfe11165e745bec72b5f42e467fa92c69f` |
| Branch / PR | `phase1/p1-w06`, draft PR #7 |
| Current gate | Two scoped repairs submitted; full required hosted rerun pending |
| W06 acceptance / merge | Not issued / not performed |
| P1-W07 and Phase 2 | Not authorized or executed |

## 1. Authority and preserved history

The owner accepted W05, authorized its merge and W06, then approved exactly the proposed P1-W06-R01 exception. This expands the W06 five-path allowlist only to the two identified earlier-unit test files and their stated repairs. It does not authorize product changes, changed source oracles, new dependencies, skipped checks, removal of a matrix row, W06 merger or W07.

Progress revision 0.11, the full first-run findings and the toolchain/source review remain preserved at the pre-repair commit above. PR #7 records both failed runs and artifact identities. The first run `35357942013` checked `668d4af4382b03aad19852aef2bdaa9252dc66d9`: 182 collected tests, with 170/12 on each Linux row and 169/13 on each Windows row. The second run `35358820107` checked the pre-repair head: 188 collected tests, with 176/12 Linux and 175/13 Windows. All rows had zero test errors/skips and 420 separate successful subtests. Neither run is relabeled as passing.

The six extra tests in the second run belong to the W06 JUnit-accounting correction. The suite aggregate and top-level collected results now remain distinct, and failures from either layer are retained. That earlier correction does not remove the security/preload or Windows-metadata failures.

## 2. Exact authorized repairs

### P1-W06-R01-A: security observer initialization

`tests/security/test_scaffold_inertness.py` now explicitly imports `importlib.util` inside the embedded probe, before reading its request or installing the audit hook. Every existing interception rule, application boundary, canary, API/CLI check and positive/adverse method is retained. There is no monkeypatch from the CI driver and no change to the product's imports.

One new regression method inspects the actual probe preamble for the explicit submodule import and executes that preamble in a fresh `-I -S -B` interpreter. It calls the actual cache/source helpers and checks their round trip without reading a source file. This prevents a parent test process or site initialization from silently supplying the missing submodule.

### P1-W06-R01-B: backend-generated metadata bytes

`tests/scaffold/test_packaging.py` now checks generated setup.cfg against one exact platform-specific byte string: LF on POSIX, CRLF on Windows. The complete egg_info content, ordering, spacing and terminal blank line remain fixed. The checked payload is not decoded, stripped, normalized or accepted under either spelling indiscriminately.

Five new parametrized test instances cover both exact spellings, an unreviewed platform, and nine malformed/extra-content variants per platform. Extra sections, changed values, removed spaces, truncated endings, BOMs, wrong-platform endings, mixed endings and reordered fields are rejected. The existing archive inventory, exclusion canaries, license/source bytes, build pin, clean install and rebuild checks are preserved. No repository source file receives newline normalization.

## 3. Byte identities and local checks

Both original complete files were fetched at the pre-repair commit and matched to their Git blobs before editing. Outgoing complete files match these independently computed identities:

| File | Original Git blob | Repaired Git blob | Repaired SHA-256 |
|---|---|---|---|
| Security probe | `066401e56b9008c4bb6bb758ddb95b877995b82c` | `8fc709df830824aad145ac612c0c70f2dec61a72` | `2c90906eeadc51d8701dd6efa0169770291f827067af460c711fff26a06ea692` |
| Packaging test | `97b4c8940c6b814e0450312668caf4b73ca1f11d` | `c872c4080d08e331b9253cd3cdd9467050d540a4` | `cfc891098830d9adf1f2ee3a0c3bcc06e884fb00f356aa5a8e1822feb1aa5d93` |

The five new metadata instances passed locally, including both newline profiles. The single new clean-interpreter method passed separately using the identical delivered probe/class definition. The previous preamble failed an isolated local reproduction as expected. AST/source comparisons confirmed preservation of the original outer functions and the entire observer body apart from the explicit preload; the sole modified pre-existing packaging test replaces only the targeted generated-file assertion.

These are six targeted local checks, not a new full-checkout suite, Windows execution or selected-toolchain certification. The remaining existing tests were outside that targeted local command, not skipped to obtain CI acceptance. Full CI must collect them all. The expected collected population is the previous 188 plus six added instances; actual counts must come from the new run.

## 4. Preserved boundaries and rerun gate

The eighteen specifications, approval, plan, forty-eight product modules, accepted case/oracle assets, catalogs, baseline manifest, dependency pins, MANIFEST.in and existing workflow/helper are unchanged by these repairs. The new commit changes only the two test files and this record. The entire W06 PR therefore has seven authorized paths relative to main.

The existing read-only workflow must rerun Ubuntu 24.04 and Windows Server 2025 with CPython 3.11 and 3.13, including actual baseline/module guards before and after, pinned wheel review/install, full scaffold and security collection, package inspection, clean runtime and source rebuild. Record the actual head/run/jobs/results after completion; pending evidence cannot close W06.

Keep PR #7 in draft until every required job passes and its evidence is inspected. Preserve any new failure, stop for another specifically scoped decision only if it falls outside this approved repair, and do not merge or begin W07 automatically.
