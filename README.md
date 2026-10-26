# Source Integrity Toolkit

A local, supplied-evidence toolkit for examining source lineage, evidence independence, external presence and corrective capacity in AI-native information systems.

**Status: public in-memory auditing is available on the Phase 4 development branch through P4-W08.** `audit_bundle` accepts a caller-prepared dossier and returns an immutable report with complete JSON and Markdown bytes when the existing resource limits permit delivery. The package remains `0.1.0.dev0`; [PR #36](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/pull/36) is a draft. Field-by-field public obligation closure and final four-environment acceptance remain for W09 and W10. `audit_file` still immediately raises `NotImplementedError`; CLI auditing still refuses with exit 1 without reading dossiers or producing reports.

## In-memory use

Prepare `dossier` as an exact built-in `dict` following the [bundle contract](schemas/bundle/sit-bundle-0.1.schema.json). Input capture and validation occur inside the audit call; callers must not mutate their containers concurrently.

```python
from source_integrity_toolkit import (
    audit_bundle, AuditAbort, AuditCancelled, AuditUsageError,
)

try:
    report = audit_bundle(dossier)
except AuditUsageError:
    # Correct the invocation options before trying again.
    raise
except AuditCancelled:
    # Cancellation has no partial report to consume.
    raise
except AuditAbort as error:
    # Only fixed safe state and reason fields are exposed.
    print(error.input_validation_state, error.reason_code)
else:
    print(report.report_kind, report.run["processing_state"])
    print(report.input_validation["state"])
    json_bytes = report.to_json_bytes()
    markdown_bytes = report.to_markdown_bytes()
```

Check the report states before interpreting results. A delivered report may describe rejected input, an interrupted audit or a processing failure. Completed analysis may legitimately contain unavailable results. A safe `AuditAbort` means a complete conforming report could not be delivered. `AuditCancelled` preserves cancellation separately.

The 16 report roots are read-only named attributes, nested objects are immutable mappings, and arrays are tuples. Both byte methods return the encodings completed during that same call; reading them performs no new analysis, encoding or I/O. The toolkit does not write or publish those bytes. Report fields can remain identifying, so successful delivery provides no anonymization or permission-to-publish guarantee.

`options=None`, `options={}` and `options={"raw_file_digest": False}` are equivalent. No other option is supported for in-memory input. `True`, unknown keys, custom mappings, non-boolean values and caller callbacks raise `AuditUsageError` before the dossier is accessed. Input records cannot configure budgets, clocks or execution policy.

The package exports `audit_bundle`, `audit_file`, `AuditReport`, `AuditAbort`, `AuditCancelled`, `AuditUsageError` and `__version__`. File capture, native adapters, CLI auditing and formal release remain later work.


## Intended purpose

The planned v0.1 auditor consumes a caller-prepared local JSON dossier containing claims, evidence, origin and transformation records, evaluator relationships and correction history. It distinguishes supplied assertions, supported structural deductions and unresolved information. Different material counts and evidence roles remain distinct. Missing ancestry cannot become an independent source, and a structurally consistent dossier cannot certify its own authenticity.

The adopted scope provides a multidimensional evidence profile. It excludes a universal truth or integrity score, live crawling, hidden-lineage discovery, an LLM judge, automatic source sanctions and automatic correction. Source locators and extensions remain inert. Source Integrity Toolkit is independent of Recursive Integrity Toolkit, with no shared internals or runtime dependency.

## Accepted baseline and current work

The eighteen Phase 0 specifications remain approved at `7d2e5fcaff591641b5cefce00e71e88941dd1f95`; [PHASE_0_APPROVAL.md](PHASE_0_APPROVAL.md) revision 1.1 preserves the authorized digest correction. [PHASE_1_COMPLETION.md](PHASE_1_COMPLETION.md) revision 1.0 was accepted with PR #8, merged at `d7d73a790a2a627d19307c9dd48281eff3017023`. Its historical pending header is read with that later acceptance event.

[PHASE_2_PLAN.md](PHASE_2_PLAN.md) and [PHASE_2_COMPLETION.md](PHASE_2_COMPLETION.md) were accepted through PR #18 at `3a9b75ab6ca4ed9d7c97207043a5c8f54c2e2547`. The accepted preparation supports supplied values and UTF-8 bytes, bounded validation, references, time syntax and evidence navigation. The preparation entry points retain their original PC01 admission behavior.

The owner approved [PHASE_3_PLAN.md](PHASE_3_PLAN.md) revision 0.1 with `批准，启动 P3-W01`; PR #19 merged at `80aa943f577f4a7deaeb8a0f3253c62d1263ca62`. [PHASE_3_PROGRESS.md](PHASE_3_PROGRESS.md) records subsequent authority and evidence while prior reviewed documents remain byte-identical. W13 was accepted through [PR #32](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/pull/32), merged at `332e94a007ceb2a955b8e047f45284b431300995`. W14 was accepted through [PR #33](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/pull/33), merged at `6dbca96f3314d537beed4ccb6202147bd9248dd9`. W15 audits the completed component work and records its approved reason-code repair, history-verification optimization, finite CI budgets and remaining acceptance gates in [PHASE_3_COMPLETION.md](PHASE_3_COMPLETION.md).

The private analysis accepts exact built-in values or supplied UTF-8 bytes and executes actual scoped owners, prerequisites, graph witnesses and immutable result delivery. It preserves supplied assertions, unresolved ancestry, qualified populations, correction history and missing evidence as separate facts. It has a fixed invocation budget and cooperative deadline. A complete supplied dossier can legitimately end with a safe resource interruption; the four original H7 examples currently stop under the unchanged work limits. Partial or interrupted execution cannot certify unperformed fields. These private entry points are implementation seams, with no stable public API or public report format promised.

All 228 field obligations have accepted owner-local core evidence. W14 added source-clause and counterexample checks. W15 identified and repaired the missing `dimension_not_selected` distinction for empty dimension selection, with exact paired value/UTF-8 tests and separate absent-subject/incomplete-role controls. The 228 historical rows remain unchanged and do not close public-envelope, rendering or release clauses. See [phase3/obligation_coverage.json](phase3/obligation_coverage.json) for the per-obligation evidence and remaining duties.

The accepted Phase 4 entry is `fdad8c3449d2d223420c5d52bb9b4c1e863a9e3c`, tree `f6fbb8965520f33a09ca38cf413e11ca561110dd`. It is the normal merge of PR #35 and preserves the directly tested VC candidate's exact tree. The owner approved the exact [PHASE_4_PLAN.md](PHASE_4_PLAN.md) bytes and subsequently authorized W01 through W08. The plan's authoring-time draft header is historical; later approvals and current execution are recorded separately in [phase4/implementation_evidence.json](phase4/implementation_evidence.json).

W01 established the ten work units' closed path and activation policy. W02 through W07 added the report contract, explicit projection and disclosure, exact JSON/Markdown encodings and same-invocation budget integration. W08 activates the public memory API and migrates the former refusal checks to actual public behavior. The [report coverage map](phase4/report_contract_coverage.json) keeps all 228 field obligations distinct from this interface checkpoint; their public-envelope/rendering closure is W09 work. W10 retains final installation/platform acceptance and handoff. File auditing, CLI auditing and release require their later approved stages.

## Developer installation and checks

Use a complete Git checkout and a clean CPython 3.11 or 3.13 development environment. Install the existing pinned development requirements, then use the single current verification entry:

```sh
python -m pip install -r requirements-dev.txt
python -B tests/scaffold/test_ci_contract.py --local --evidence-dir ../sit-p4-local-evidence
```

Choose a new evidence directory for each attempt. The entry verifies the actual tool versions, current module/workflow boundaries and frozen Phase 0 baseline, explicitly collects all five directories (scaffold, security, contract, unit and integration), runs the complete suite with third-party pytest plugin autoload disabled, and reconciles exact collected identities with JUnit. Successful subtest events are counted separately. It checks tracked bytes before/after and retains raw logs, failure records, distribution inventories and available installed-runtime evidence. Missing directories, an empty collection, failure/error/skip outcomes or incomplete evidence fail the command. The complete-suite process budget is 2,400 seconds.

This local command requires no `SIT_PHASE_UNIT` or fabricated GitHub event. It checks the local working tree and records its source hashes. It cannot attest hosted context, authorize a checkout or replace the four required hosted profiles. Installed-runtime receipts record the actual tested distribution, module hashes, inputs, independent expectations and execution scope. Use the resulting `summary.json` and raw logs to inspect the attempt, including a failed or timed-out attempt.

Dependency installation is a developer operation and may access the package index. The installed product has zero third-party runtime dependencies. Package construction, clean offline installation, all 48 installed module hashes, private preparation and analytical witnesses, actual public memory reports, and the remaining file/CLI refusals are tested. The product never imports developer guards, catalogs or tests. Six former historical wrappers now contain their current assertions directly; normal test collection does not fetch or execute historical Git blobs. Some developer boundary tests intentionally use real temporary Git repositories. Building and using the installed package does not require that history.

Bare `pytest` retains its older scaffold-only configuration. Use the current entry above for complete local verification. Existing targeted pytest invocations are useful diagnostics and must be reported with their actual selected scope.

## CI and evidence

[Current verification](.github/workflows/phase1-ci.yml) keeps Ubuntu 24.04 and Windows Server 2025, each with Python 3.11 and 3.13, immutable Action pins, read-only permissions, no stored checkout credentials, a 50-minute job budget and the 2,400-second suite budget. The seven existing workflow stages remain visible. Evidence reconciliation and artifact upload run with `always()`; the existing fourteen-day retention and `sit-p3/evidence` receipt destination remain intact.

CI resolves the actual GitHub event, base and checked-out head. Phase 4 uses the same-repository `phase4/public-report` branch targeting `main`, with one exact `SIT-Phase-Unit: P4-Wnn` footer identifying a real approved work unit. The accepted PR #35 merge, exact approved plan, every post-anchor commit and parent edge, stage activation and actual index/worktree must independently pass. Footer text, dossier extensions and candidate records cannot grant authority. Missing or inconsistent external context fails closed; prior VC labels cannot authorize Phase 4 work.

Risk routing uses every parent edge in the actual event change interval, including intermediate edits restored before the final head and merge sides. After verified activation reaches W10, only changes confined to the two exact non-executable Phase 4 records, `PHASE_4_COMPLETION.md` and `phase4/implementation_evidence.json`, can use the explicit documentation scope. That scope still checks current authority, complete history, checkout, frozen bytes, module boundaries and workflow policy, and reports that no full suite was run. It does not acquire test tools or claim package/installed-runtime execution. Empty, unknown or mixed changes require the full scope. README changes also require the full scope because README is package metadata. File suffixes and candidate declarations cannot select the reduced route.

Full scope requires all five test directories, exact collection/JUnit identity reconciliation, separately observed subtests, unchanged tracked bytes, pinned installed tools, package inventories and both current-head installed receipts. Each attempt binds evidence to its actual head, event, run/attempt and matrix profile. Raw partial output and failure records remain evidence of failure. A successful documentation check or local check is never reported as full-matrix acceptance.

The accepted Phase 3 anchor was `2413a29b839b7e1de8f76a449762f031de19d52b`, with the same tree as directly tested head `90684996eac568af6129973764fe40f3b666a15f`. [Run 36736103966, attempt 1](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/actions/runs/36736103966) passed all four original profiles with 3,963 tests and 428 separate subtest events each. The later VC candidate `ce05c5dda9368182dbee074253d3a7c829af7719` passed [run 38128491330, attempt 1](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/actions/runs/38128491330), with 3,724 tests and 431 separate successful subtest events per profile; raw evidence was reviewed and the owner accepted VC-06. [Main-push run 38164028893, attempt 1](https://github.com/DavidWallstructurallaw/source-integrity-toolkit/actions/runs/38164028893) also passed all four profiles after PR #35 merged. These are accepted baseline results, not Phase 4 implementation evidence or a test-count floor.

Phase 4 records each current candidate's actual collection and result. Its final executable candidate requires all four hosted profiles and raw-evidence review. Local checks and documentation-only checks retain their limited meaning. CI success does not automatically authorize owner acceptance, merge, another work unit or release.

Current Phase 4 work and actual validation status are in [phase4/implementation_evidence.json](phase4/implementation_evidence.json); the scoped verification and toolchain review is in [phase4/ci_review.md](phase4/ci_review.md). [VERIFICATION_CONSOLIDATION_COMPLETION.md](VERIFICATION_CONSOLIDATION_COMPLETION.md) and the one-time [consolidation map](verification/consolidation_map.json) preserve their original checkpoint wording; later PR acceptance and merge records establish VC completion. These maps are review artifacts, never product input or an approval switch for current verification. Historical stage evidence remains in [PHASE_3_COMPLETION.md](PHASE_3_COMPLETION.md), [phase3/implementation_evidence.json](phase3/implementation_evidence.json) and their immutable Git history. The complete pre-retirement test implementation is available at `3ac5128e4744e2d3708400e3cb1875a9cd4ed0e1`; inspect any historical replay in an isolated checkout with its original tooling and label it as historical investigation. Earlier failed attempts and missing W01-W07 raw ZIPs and some W08 profile artifacts remain disclosed. Existing CI artifacts contain JSON/XML/log records, not the wheel/sdist archive bytes or original GitHub event payloads. W08 temporary-archive member corroboration and W14 exact archive records have different evidence scope; no whole-archive reproducibility claim is made. The different VC event digests between runner groups have no established byte-level explanation.

Windows Server component tests do not certify a future Windows 11/NTFS native adapter. Public in-memory report delivery is implemented; per-field public acceptance, final platform acceptance, CLI auditing, native file adapters and release remain unfinished. The product's 60-second cooperative deadline and existing work quotas are unchanged; a safe resource interruption is not certification of unperformed analysis.

## Specifications, security and rights

Start with [V0.1_PRODUCT_SPEC.md](V0.1_PRODUCT_SPEC.md), [DEFINITIONS_AND_UNITS.md](DEFINITIONS_AND_UNITS.md), [CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md](CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md) and [OBSERVABILITY_AND_REPORTING.md](OBSERVABILITY_AND_REPORTING.md). [THEORY_SOURCE_MAP.md](THEORY_SOURCE_MAP.md), [THEORY_TO_CODE_TRACEABILITY.md](THEORY_TO_CODE_TRACEABILITY.md) and [VALIDATION_PLAN.md](VALIDATION_PLAN.md) preserve source interpretation, responsibilities and future behavior tests. Historical catalogs and the approved plans remain unchanged; implementation evidence is tracked separately.

See [CONTRIBUTING.md](CONTRIBUTING.md) and [SECURITY.md](SECURITY.md). Do not post private evidence, credentials or protected-source identities in this public repository. Use fictional development examples. Private vulnerability reporting remains subject to the existing unverified-channel limitation. Build/test tools and their original reviews remain in [scaffold/toolchain_review.md](scaffold/toolchain_review.md) and [scaffold/ci_toolchain_review.md](scaffold/ci_toolchain_review.md); the historical Phase 3 transition remains in [phase3/ci_review.md](phase3/ci_review.md), and current Phase 4 findings are recorded separately.

## License

Copyright 2026 Xiangyu Guo.

Original engineering repository materials are licensed under the **Apache License, Version 2.0**, in [LICENSE](LICENSE), with attribution in [NOTICE](NOTICE). This covers original engineering specifications, documentation, fictional examples, code, schemas and tests that the project has authority to license.

The grant does not automatically cover theory papers or their extracts, page images, translations or adaptations; third-party material; user-supplied evidence; confidential identity maps; or input-derived report content. Theory papers retain their own **CC BY-NC-ND 4.0** notices. Excluded materials retain their own terms and permissions. Successful processing does not transfer rights.

[LICENSING_NOTES.md](LICENSING_NOTES.md) controls these boundaries. Its historical root-license statement refers to Phase 0; accepted P1-W01 applied the license without changing that frozen specification. Upstream contribution/governance rules add no downstream conditions to Apache-2.0. No package-index release has been published by this work.
