# PHASE_1_PROGRESS

## Current control record

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Revision | 0.11, P1-W06 first matrix review |
| Date | 2026-09-18 UTC |
| Owner instruction | `批准并合并 PR #6，然后进入 P1-W06` |
| Approved plan | Revision 0.1, Git blob `27ed33cb1c2afc78b12ca099ee7ccb4e68d63bfb` |
| Accepted W05 head | `6bf3ef93fd90471da709d6f90e598e9d84f95908` |
| Actual PR #6 merge / W06 intake | `ecf4eb5126201a7c31250c6dae8cbe2c64f9066a` |
| Branch / PR | `phase1/p1-w06`, draft PR #7 |
| First hosted candidate | `668d4af4382b03aad19852aef2bdaa9252dc66d9` |
| Hosted run | `35357942013`, attempt 1 |
| W06 status | BLOCKED: previous-unit test repairs require scoped approval |
| W06 acceptance / merge | Not issued / not performed |
| P1-W07 and Phase 2 | Not authorized or executed |

## 1. Authority and history

The owner accepted W05 and explicitly requested merger followed by W06. The connector verified the exact PR #6 head and twelve-path diff, then performed the merge with expected-head protection. W06 was branched from the returned merge commit. No force push or history rewriting occurred.

W05's original 42 local methods and execution limits remain preserved at its accepted head and PR #6. The first W06 hosted run now supplies the previously missing execution of the new baseline command against all twenty actual protected files. This supplements that evidence; it does not turn the earlier local limited checkout into a full-checkout run.

The complete first W06 candidate, pre-execution review, workflow and helper are preserved at `668d4af4382b03aad19852aef2bdaa9252dc66d9`. Failures below are retained as actual findings, with no skipped tests or relaxed historical assertions. W04's earlier exact import and isolated transport-workflow removal remain in the predecessor history.

## 2. Closed change scope

Only these five plan-section-10 paths change in W06:

```text
.github/workflows/phase1-ci.yml
scaffold/ci_toolchain_review.md
tests/scaffold/test_ci_contract.py
README.md
PHASE_1_PROGRESS.md
```

The eighteen frozen specifications, corrected approval, approved plan, baseline manifest, product modules, accepted earlier tests, fixture/oracle assets, catalogs, dependency pins, packaging rules, licenses and earlier W02 workflow remain unchanged. No application auditing, native loading, source retrieval or report generation is implemented.

## 3. Actual first hosted matrix

Run `35357942013`, attempt 1, executed the exact first candidate. All four evidence ZIPs were downloaded through the connector, their SHA-256 digests matched the Actions metadata, and their complete pytest/JUnit, environment, guard, collection and build records were inspected.

| Hosted profile | Actual Python | Top-level collected | Passed | Failed | Errors / skipped |
|---|---|---:|---:|---:|---|
| Ubuntu 24.04.5 | 3.11.16 | 182 | 170 | 12 | 0 / 0 |
| Ubuntu 24.04.5 | 3.13.15 | 182 | 170 | 12 | 0 / 0 |
| Windows Server 2025, build 26100 | 3.11.9 | 182 | 169 | 13 | 0 / 0 |
| Windows Server 2025, build 26100 | 3.13.15 | 182 | 169 | 13 | 0 / 0 |

Each row also reported 420 successful unittest subtests. These are separate from the 182 collected top-level instances. They do not represent 420 additional independently collected test functions or satisfy the 228 future domain obligations.

All four rows passed the actual twenty-file baseline and forty-eight-module guards before and after execution. All tracked file hashes remained unchanged. The selected development distributions were verified and installed: six Linux wheels and the same six plus the preselected Windows-only Colorama wheel. No runtime dependency was added.

All rows built source/wheel artifacts and passed clean-runtime installation and source-rebuild member-byte equality. Inventories contained 65 regular source-distribution files and 55 wheel members. The Windows source-inventory test failed on backend-generated setup.cfg newline bytes, so the complete Windows source-inventory gate is not marked passed. The real clean-install test remained distinct and passed.

## 4. Failures requiring earlier-unit repair

### P1-W06-R01-A: isolated security-probe initialization

All twelve W05 security methods fail before a product module is imported, with AttributeError and an empty interception list. The embedded probe in `tests/security/test_scaffold_inertness.py` imports importlib, but its audit hook references importlib.util.source_from_cache without explicitly importing importlib.util. A minimal isolated local reproduction using the same preload list produced `AttributeError: module 'importlib' has no attribute 'util'`; explicitly importing the submodule resolved that initialization condition.

Proposed repair: explicitly preload the needed standard-library submodule before installing interception, retain the complete positive/adverse checks, and add a clean-interpreter regression where necessary. Do not inject a monkeypatch from W06 to conceal the earlier test's dependency, change product code or remove the native/network probes. The proposal does not claim that a repaired full matrix has already passed.

### P1-W06-R01-B: generated source-metadata newline expectation

On both Windows rows, `tests/scaffold/test_packaging.py::test_source_distribution_inventory` compares generated setup.cfg against an LF-only byte string. The backend writes the same fixed egg_info fields with Windows CRLF. The inspected failure shows no different fields or unexpected file. The repository's frozen source bytes remain unchanged.

Proposed repair: give this one backend-generated file an explicit platform-specific expected byte spelling, retaining exact field/order/content checks and a negative control for extra settings or malformed/mixed endings. Do not normalize frozen files, change MANIFEST.in, broaden allowed distribution members, skip Windows, or change the backend pin.

Both target files belong to earlier units and are outside the five-path W06 allowlist. They remain unmodified. **P1-W06-R01 requests owner permission for exactly these two file repairs and the necessary existing W06 evidence-record updates, followed by rerunning all four rows.** This request does not approve itself.

## 5. W06-local summary correction

The new driver initially compared JUnit's suite `tests=602` directly with the 182 collected IDs. The selected pytest includes successful subtest events in that aggregate but emits 182 testcase elements. The full downloaded XML established the mismatch. This is a W06 summary defect, separate from the actual twelve/thirteen failing tests.

Within the already authorized W06 helper, accounting now matches exact classname/name pairs against all collected IDs, rejects missing/duplicate/unexpected outcomes, preserves failure/error/skip information from both suite totals and result elements, and reports aggregate events separately. No nonzero pytest exit can be converted to a pass. Six independent accounting controls were added alongside the original fourteen policy tests.

All twenty W06-local methods passed with zero failures/errors/skips. Applying the corrected parser to all four original JUnit files reproduced the table above and retained every failure. These checks do not close the earlier-unit failures. The successor hosted run will be recorded in PR #7 after its identity and outcomes exist; no first-run green result is attached to a changed helper.

## 6. Evidence and stop point

The four original Actions artifact IDs and complete hashes are listed in scaffold/ci_toolchain_review.md. Logs and artifact bytes remain inspectable. The workflow is read-only, exact-head checked, finite, and limited to verification records. Neither the temporary W04 importer nor a write token is reused.

Keep PR #7 in draft and leave main at the accepted W05 merge. Wait for P1-W06-R01 before changing earlier tests. After the scoped repair, rerun all four jobs without omitting existing methods. A new defect outside that repair scope must be recorded rather than silently fixed. P1-W06 acceptance, merger and P1-W07 remain separate gates.
