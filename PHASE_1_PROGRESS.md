# PHASE_1_PROGRESS

## Current control record

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Progress revision | 0.4 |
| Date | 2026-09-17 |
| Approved plan | Revision 0.1, Git blob `27ed33cb1c2afc78b12ca099ee7ccb4e68d63bfb` |
| Accepted predecessor | P1-W01, merged PR #2, commit `ae61bb6fa36d53fb2138542ee69e36585ee7bc72` |
| W02 candidate before this supplement | `1126eff7d98023b9bc835dc00026ea5629f64a77` |
| Review branch / PR | `phase1/p1-w02` / #3 |
| Current work | P1-W02 selected-toolchain verification |
| Current result | Hosted verification authorized and prepared; executed outcome pending |
| Merge / W03 | Not authorized by this supplement |

## 1. Preserved history

The complete W01 repair, acceptance and merge history remains in Git. The W02 preparation record at commit `1126eff7d98023b9bc835dc00026ea5629f64a77`, this path, preserves all 57-path scaffold changes, actual older-tool packaging checks, the 77-pass/1-fail result and its environmental cause. Its toolchain review preserves the exact selected pins and security-review limits.

No historical failure is erased or reclassified as passing. The previous local run used setuptools 82.0.1 and pytest 9.0.2; it did not satisfy the selected 84.0.0/9.1.1 gate.

## 2. Scoped exception P1-W02-A01

After the W02 handoff explicitly proposed an early workflow limited to acquiring the selected tools, inspecting their actual artifacts and running the existing scaffold tests, the owner replied `可以`.

This accepts that narrow proposal. It adds one path to the current W02 allowlist: `.github/workflows/p1-w02-verify.yml`. Inline developer verification inside that workflow and updates to the already allowed progress/toolchain records are included. The approved Phase 1 plan itself stays byte-identical. This is a recorded exception to workflow timing, not general W06 authorization, baseline amendment, package publication, repository-setting change or authority to merge PR #3.

The dedicated job is restricted to same-repository PR #3 from `phase1/p1-w02` against main. It checks out the exact PR head, uses read-only contents permission, does not persist checkout credentials, receives no configured repository secrets and grants no release/package/PR write permission. Official actions are pinned by full commit SHA. The job uses an ephemeral Ubuntu runner and CPython 3.13; the exact executed patch/platform and installer versions are recorded by the run. Windows and the Python 3.11 minimum-version matrix remain later work.

## 3. Verification sequence

The workflow verifies the pinned W01 baseline-manifest blob, then all eighteen specification byte counts and hashes, the corrected approval record and the unchanged Phase 1 plan. It obtains only the six declared Linux development wheels, checks direct wheel hashes against the prior reviewed values and all wheel hashes against exact-release PyPI metadata, records included license and vendored metadata, and installs offline into an isolated tool environment.

It runs the four existing W02 test files without changing their strict version gate. Those tests build and inspect the source archive/wheel, install the project without developer dependencies in a clean runtime environment, and compare rebuilt wheel member bytes. No additional build frontend is installed. A failing, skipped or absent required test keeps the job red.

Verification JSON, JUnit XML and logs are retained as scoped Actions evidence for fourteen days. No package binary, private dossier, theory PDF, arbitrary workspace or environment/secret dump is uploaded. Source artifacts remain temporary test products and are not published to a package index or GitHub release.

## 4. Current actual checks and limits

Before submission, the workflow YAML and embedded Python syntax were checked locally; trigger, permission and full-SHA action settings were inspected. The GitHub PR head was re-read before writing. Application source, tests, packaging declarations, development pins, licensing files and the twenty protected specification/approval/plan paths are unchanged in this supplement.

The local session still cannot resolve github.com or pypi.org. This is not treated as a failed upstream release. Hosted installation/test/build evidence has not yet been observed at this preparation checkpoint. The final run/attempt/job identifiers and outcome must be recorded after they exist.

The upstream setuptools extraction-safety note remains explicitly qualified in scaffold/toolchain_review.md. No untrusted archive is submitted to its extractor. A green scaffold job does not establish production security, source analysis or native platform support.

## 5. Stop and review gate

Keep PR #3 unmerged and W03 unstarted. Retrieve the actual hosted run, steps and logs. If installation, artifact identity, tests or packaging fail, preserve the failure and repair only within the current authorized scope. Do not relax the selected-version assertion or alter frozen semantics to obtain green status.

Once all W02 evidence is complete, submit the candidate for owner acceptance. Actual merge and the next unit require the corresponding owner instruction.
