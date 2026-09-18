# Contributing to Source Integrity Toolkit

## Current scope

Development follows the approved [PHASE_1_PLAN.md](PHASE_1_PLAN.md). P1-W01 is the governance and license step. There is no implemented auditor or working package to test at this point. Consult [PHASE_1_PROGRESS.md](PHASE_1_PROGRESS.md) before proposing work in another unit.

Use a review branch based on the latest accepted predecessor and a pull request describing the intended change. Keep the diff within the currently authorized file allowlist. Approval of one unit does not authorize the remaining phase or analytical implementation. Do not force-push accepted history or silently merge unrelated changes.

## Frozen specifications and change requests

The eighteen specifications identified in [PHASE_0_APPROVAL.md](PHASE_0_APPROVAL.md), the approval record and the approved Phase 1 plan are protected inputs. Do not reformat them, convert line endings, move them or revise historical headers as incidental cleanup. Compare complete bytes with the baseline manifest before and after a scoped change.

A needed correction must identify the exact file and section, observed defect, affected decision/requirement/Trace IDs, expected outcome and the smallest proposed amendment. Obtain explicit scoped authorization before editing a frozen record. Preserve the original version in Git and record the actual approval and resulting evidence. A malformed digest must be recomputed from the original bytes; it cannot be repaired by guessing a character or weakening the checker.

Use the change classes in [GOVERNANCE_AND_HANDOFF.md](GOVERNANCE_AND_HANDOFF.md). Changes to public fields, units, denominators, evidence qualification, security, dependencies, licensing or cross-project coupling require their corresponding review. An implementation convenience cannot silently settle an unresolved specification choice.

## Evidence and review

A pull request should state its work unit and authorization, changed paths, controlling specifications, checks actually run with their environment, failures or limits, and remaining gate. Cite the actual checked commit and CI run when available. Pending tests remain pending.

Preserve supplied assertions, derived observations and unknowns as separate concepts. Retain contrary evidence and missing-data conditions. Never change a logical oracle merely to agree with incorrect code. A correct number without its required population, basis or qualification is insufficient.

Phase 1 audit placeholders must refuse immediately rather than return success-looking empty results. Static fixture syntax checks and scaffold imports do not satisfy domain-analysis tests. No blanket passing/skip count can stand in for the 228 specified field-test obligations. Runtime parsing, graph analysis, report generation, native bindings and resource enforcement remain outside the scaffold phase.

## Data and security

Submit only fictional or explicitly authorized shareable examples. Do not include private dossiers, credentials, access tokens, identity maps, personal case files, full theory PDFs or copied third-party datasets. The ignore file is a convenience, not a confidentiality guarantee. Keep private material outside the checkout and review both staged files and commit history before submission.

Follow [SECURITY.md](SECURITY.md) for a possible vulnerability. Public Issues and PRs are not confidential channels. Do not post sensitive exploit details or real evidence to request help.

## Contributions and licenses

Original engineering contributions intentionally submitted for inclusion are handled under Apache-2.0 as provided by [LICENSE](LICENSE), unless explicitly identified otherwise and separately accepted under an appropriate rights arrangement. Confirm that you have authority to submit the material, including any employer or third-party interests. No copyright assignment or additional contributor agreement is introduced here.

Identify copied material, its origin and exact license or permission before inclusion. Preserve required third-party notices; do not label third-party work Apache-2.0 merely because it is placed in this repository. AI-assisted drafting does not establish originality or ownership by itself.

The theory papers retain their own CC BY-NC-ND 4.0 notices. Paper extracts, page images, translations/adaptations, user evidence, protected identity mappings and input-derived report material are excluded from automatic repository relicensing. Original engineering explanations can refer to the source map without copying those works. See [LICENSING_NOTES.md](LICENSING_NOTES.md).

These contribution and review rules govern upstream acceptance. They do not modify the Apache-2.0 license or impose additional conditions on downstream use of covered material.

## Tooling

[scaffold/toolchain_review.md](scaffold/toolchain_review.md) records the proposed build/test pins and review boundary. P1-W02 owns declarations, installation, resolved dependency inspection and packaging tests. Do not add a runtime package, optional plugin, build frontend or formatter outside the applicable authorization.
