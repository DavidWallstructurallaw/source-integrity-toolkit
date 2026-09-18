# PHASE_1_PROGRESS

## Current control record

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Progress revision | 0.5 |
| Date | 2026-09-17, project-local date; hosted timestamps below use UTC |
| Approved plan | Revision 0.1, Git blob `27ed33cb1c2afc78b12ca099ee7ccb4e68d63bfb` |
| Accepted predecessor | P1-W01, merged PR #2, commit `ae61bb6fa36d53fb2138542ee69e36585ee7bc72` |
| W02 original candidate | `1126eff7d98023b9bc835dc00026ea5629f64a77` |
| Executed hosted candidate | `a5000f5a65ae094d7c6762a9fe8557ffa0ba1928` |
| Review branch / PR | `phase1/p1-w02` / #3 |
| Work-unit result | P1-W02 technical acceptance checks PASSED; submitted for owner acceptance |
| Owner acceptance / merge | Pending; neither inferred from successful CI |
| W03 and later work | Not started |

## 1. Preserved history and authorization

The complete P1-W01 progress remains at `63c03ee82ebffd5f4dc73972b2baa158c20cdf33`, this path. Its merge is `ae61bb6fa36d53fb2138542ee69e36585ee7bc72`. The W02 preparation record at `1126eff7d98023b9bc835dc00026ea5629f64a77`, this path, preserves the 57-path scaffold delivery, the older-tool packaging evidence, two repaired test-construction issues and the actual 77-pass/1-fail result. No failed historical run is relabeled successful.

After the handoff proposed early GitHub Actions verification limited to the selected W02 toolchain and existing tests, the owner replied `可以`. Scoped exception **P1-W02-A01** therefore adds exactly `.github/workflows/p1-w02-verify.yml` to the W02 file allowlist, together with updates to the already permitted progress/toolchain records. Its preparation checkpoint is preserved at `a5000f5a65ae094d7c6762a9fe8557ffa0ba1928`.

The exception does not amend Phase 0 semantics, alter the frozen Phase 1 plan, authorize the general W06 matrix, permit repository settings/secrets changes, publish packages, merge PR #3 or start W03.

## 2. Delivered scope

The original 48 Python module slots, three packaging/developer files and four scaffold test files remain byte-identical to the W02 candidate. The new workflow and the two progress/toolchain updates are the only changes after that candidate. The complete PR therefore changes 58 permitted paths: 56 additions and two updates relative to the accepted W01 merge.

The distribution remains `source-integrity-toolkit`, import name `source_integrity_toolkit`, unreleased version `0.1.0.dev0`, Python >=3.11 and zero required third-party runtime packages. Forty-four package files are docstring-only slots. The two public API stubs immediately raise NotImplementedError without inspecting arguments. The CLI exposes help/version and fixed audit refusal with temporary scaffold exit 1. It performs no dossier access and emits no analytical report.

No production parser, schema mapper, validator, graph algorithm, source analysis, exact serializer, native binding, ACL logic or quota engine is implemented. No analytical Trace or domain-test obligation has been marked complete.

## 3. Actual hosted verification

| Evidence | Observed value |
|---|---|
| Workflow | P1-W02 selected-toolchain verification |
| Workflow commit | `a5000f5a65ae094d7c6762a9fe8557ffa0ba1928` |
| Run / attempt | `35307307901` / 1 |
| Job | `105482030736`, verify |
| Event | pull_request, same-repository PR #3 |
| Conclusion | completed / success |
| Job log time range | 2026-09-18 04:31:49 through 04:32:03 UTC |
| Actual interpreter | CPython 3.13.15 |
| Actual platform | Ubuntu 24.04.5, Linux x86_64, glibc 2.39 |
| Runner image | ubuntu-24.04, 20260907.300.1 |
| Installer | pip 26.2.1 in the isolated tools venv |
| Build / test tools | setuptools 84.0.0 / pytest 9.1.1 |
| Test result | 78 passed, 0 failed, 0 errors, 0 skipped; pytest elapsed 1.92 seconds |
| Evidence artifact | `10532775110`, `p1-w02-evidence-35307307901-1` |
| Evidence archive size / SHA-256 | 66,573 bytes / `7bab6bd98fd2cea8f31dd59b782be36235e86fb1fcf4bd9b2030425cdaa00043` |
| Evidence expiry | 2026-10-02, subject to GitHub retention/deletion |

Canonical run: `https://github.com/DavidWallstructurallaw/source-integrity-toolkit/actions/runs/35307307901`.

The connected job summary, full decoded job log, run conclusion and artifact metadata were read after completion. The log confirms actual download/installation of the selected versions, not a result obtained with preinstalled older tools. The existing strict version assertion was unchanged. No failed check was converted into skip, xfail or a version waiver.

### Verification coverage

| Check | Actual evidence |
|---|---|
| Frozen baseline | Pinned baseline-manifest blob plus all 18 specification byte counts/SHA-256/Git blobs, corrected approval record and Phase 1 plan passed |
| Selected wheel identities | Six pinned Linux development wheels downloaded and checked against release metadata; both direct-tool digests also matched prior reviewed values |
| Dependency installation | Offline installation from the inspected wheelhouse in a new venv; pip check found no broken requirements |
| Imports and inert slots | All 48 slots and fresh guarded imports passed |
| API/CLI refusal | Hostile arguments, help/version and refused audit paths passed without report creation |
| Source distribution | Exact 65-regular-file inventory and fictional exclusion probes passed |
| Wheel | Exact 55-member inventory, package metadata, empty runtime requirements and unchanged LICENSE/NOTICE passed |
| Clean runtime | Self-built wheel installed offline into a pip-less venv; only the project distribution present; API/CLI smoke checks passed |
| Rebuild | Inspected self-generated source archive rebuilt to the same wheel member bytes |
| Evidence delivery | Nine verification records uploaded; no wheel/source archive, private input or arbitrary workspace uploaded |

The original local 77-pass/1-fail record remains valid evidence about its older environment. The separately observed hosted 78-pass run resolves the selected-toolchain gate. Windows and CPython 3.11 execution remain unperformed; their later matrix is not claimed here.

## 4. Observed build artifacts

These are temporary, self-generated test artifacts, not published distributions.

| Artifact | Bytes | SHA-256 | Members |
|---|---:|---|---:|
| Original wheel | 34573 | `0a5358f0fe046961c1b81cf4299a94d09db9d1c89a5de8a52f78c1f8aa184016` | 55 |
| Source archive | 21928 | `4e3ff731e5f11177436285183281d42cbf3705a1848838867b763986b0a7812f` | 65 regular files |
| Rebuilt wheel | 34573 | `02edb45f3eb43c1a20a8fb0c28a26eec291541e0c3c2b8469280e90352c6c6e9` | 55 |

Whole ZIP digests differ because container metadata can differ. The existing test compared every member name and byte sequence, and passed. No archive-wide reproducible-build claim is substituted for that check.

## 5. Workflow boundary and remaining limitations

The workflow is restricted to same-repository PR #3 from `phase1/p1-w02`. It checks out the exact PR head, uses contents:read and full-SHA official actions, disables credential persistence and has no repository-secret input, write permission, package-index publication, self-hosted runner or pull_request_target trigger. The 15-minute job deadline and fourteen-day evidence retention bound this verification service. No application network capability was added.

The hosted runner reported checkout's Node 20 target as deprecated and executed it with Node 24. No insecure legacy-runtime override was enabled. This informational warning did not fail a check and is recorded in the toolchain review.

The setuptools archive-extraction advisory range remains unavailable; the upstream unreleased note was rechecked. The selected operations use binary-only developer wheels, controlled repository content and inspected self-built archives, without calling archive_util on external inputs. A passing scaffold does not certify the backend or the future auditor generally secure.

## 6. Review and next gate

This revision records an already completed run at the named commit. It changes progress and review documentation only. A new branch-head CI run will independently check the documentation-only successor; its exact identifiers belong in the PR conversation after they exist. The earlier successful commit is never mislabeled as a run on its successor.

P1-W02 is ready for owner review once the current PR head's check is confirmed. Keep PR #3 unmerged until the owner accepts the delivery and requests merge. W03 begins only under its named authorization. The Phase 0 specifications, approval, plan, W01 license and other protected files remain unchanged.
