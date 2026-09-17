# UNRESOLVED_DECISIONS

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Phase / work unit | Phase 0 / WU11 remediation re-audit |
| Revision | 0.7 |
| Date | 2026-09-17 |
| Decision owner | Xiangyu Guo |
| Current authority | Complete SIT-D028-SIT-D031 and perform WU11 re-audit |
| Central decision inventory | SIT-D001-SIT-D031; no ID reassigned |
| Technical disposition | Four specification gaps completed and re-audited; no unresolved technical blocker identified in the candidate |
| Approval disposition | Final owner adoption of the completed 18-file Phase 0 baseline remains required |
| Phase 1 / implementation | Not authorized |

## 1. Current register and immutable historical records

This revision is a current-status index plus the four completed remediation records. It consolidates repeated historical status tables so a previous BLOCKING label cannot be mistaken for the present technical result. It does not replace or revise an earlier theory statement, decision alternative, recommendation, qualification or owner instruction.

The full, unabridged revision 0.6 is incorporated by this immutable reference:

`https://github.com/DavidWallstructurallaw/source-integrity-toolkit/blob/2a19833c53fd9a7b1065f568f470919d79583bfd/UNRESOLVED_DECISIONS.md`

Its Git blob is `0245b20b77a41a9f7a0fad510dd4dc5553715592`. It retains the complete revision 0.5 record, all SIT-D001-SIT-D027 alternatives and approvals, and the original SIT-D028-SIT-D031 findings. Those historical bytes remain in repository history. Original questions/options remain authoritative historical evidence; the current dispositions below govern present status. References to a historical section or alternative are resolved in that pinned version, not reinterpreted as a new approval.

Canonical input, analytical, report and test semantics remain in their owning specification documents. This index does not replace them with summaries.

## 2. Approval evidence and its scope

The recorded WU3 and WU5 intake events approved SIT-D001-SIT-D025 in their stated scope. Reporting section 11.1 records the later acceptance of SIT-D026-SIT-D027. Validation section 9 and the WU8/WU9 handoffs record acceptance of the reporting/case/test-planning supplements. Governance records WU9-C01/C02 acceptance on entering WU10; LICENSING_NOTES.md revision 0.2 records the explicit Apache-2.0 selection. The instruction to proceed to WU11 accepted the WU10 submission for final review.

The latest instruction is:

> 可以，执行补齐，再进行 WU11 复审

This accepts the recommended completion direction and authorizes both writing the missing protocols and re-auditing them. It does not require another authorization merely to perform that requested re-audit. It also does not pre-certify the protocols, appoint a technical maintainer, grant third-party rights, or constitute the final owner approval of the completed Phase 0 baseline.

Accordingly, SIT-D028-SIT-D031 are APPROVED completion directions with documented, technically reviewed candidate realizations. Their exact delivered details remain subject to final baseline adoption. This distinction follows the project's established separation of direction selection, detailed realization and final phase approval.

## 3. Current central decision index

| ID | Subject | Current status | Governing realization / qualification |
|---|---|---|---|
| SIT-D001 | Source-local entropy/formal quantities | APPROVED direction, B | Source map and traceability preserve each source's assumptions; no entropy diagnostic |
| SIT-D002 | Synthetic judgment and renewed human input | APPROVED direction, B | Human, model and external validation roles remain distinct |
| SIT-D003 | Local structured-bundle workflow | APPROVED direction, A | Caller-supplied dossier; no live discovery |
| SIT-D004 | Inquiry, artifact, actor and origin separation | APPROVED direction, B | Definitions and lineage contract |
| SIT-D005 | Positive scoped independence evidence | APPROVED direction, B | Individual supplied comparison sets; no inferred independence from disconnection |
| SIT-D006 | Unknown ancestry and coverage | APPROVED direction, B | Explicit frontiers; hidden origin multiplicity remains unknown |
| SIT-D007 | Typed assertions, provenance and time | APPROVED direction, B | Typed views, lifecycle and original assertion basis retained |
| SIT-D008 | External input stages | APPROVED direction, B | Admission, preservation, selection and influence require their own evidence |
| SIT-D009 | Correction routes, authority and outcomes | APPROVED direction, B | Route, handling and linked change remain separate |
| SIT-D010 | Metrics and profile claims | APPROVED direction, B | Restricted descriptive profile; no aggregate truth/integrity score |
| SIT-D011 | Data and governance vocabularies | APPROVED direction, B | Source-local axes preserved |
| SIT-D012 | Capability-specific observability | APPROVED direction, B | No cumulative quality level |
| SIT-D013 | Contestation, tail retention and omission | APPROVED direction, B | Finite known cohorts; no suppression inferred from final absence alone |
| SIT-D014 | Protected sources and untrusted input | APPROVED direction, B | Opaque commonality, explicit gaps, inert content |
| SIT-D015 | Independent project and licensing/architecture gates | APPROVED direction, B | No shared runtime; later license choice recorded separately |
| SIT-D016 | Canonical local input modes | APPROVED direction, A | One JSON dossier and equivalent supported in-process values |
| SIT-D017 | Minimum usable structural audit | APPROVED direction, B | Required analyses return supported values or explicit non-results |
| SIT-D018 | Local CLI/library and JSON/Markdown | APPROVED direction, A | One semantic report, explicit transport outcomes |
| SIT-D019 | Twelve-kind ontology and role specializations | APPROVED detailed contract, A | Existing lineage schema vocabulary unchanged |
| SIT-D020 | Typed qualification, graph views and conflicts | APPROVED detailed contract, B | Existing assessment/view rules unchanged |
| SIT-D021 | Immutable snapshots and strict references | APPROVED detailed contract, A | No implicit predecessor reads or hidden repair |
| SIT-D022 | Counting populations and comparison sets | APPROVED detailed contract, B | Explicit units and per-assessment counts |
| SIT-D023 | Incidence, restricted HHI and inheritance | APPROVED detailed contract, B | Exact denominators, no multiparent weight invention |
| SIT-D024 | Stages, evaluators and correction profiles | APPROVED detailed contract, B | Independent evidence requirements and populations |
| SIT-D025 | Non-results, precision and comparability | APPROVED detailed contract, B | Field-specific states and exact values |
| SIT-D026 | Threat taxonomy and bounded findings | APPROVED detailed contract, B | Fourteen concern families; intent and authenticity are not inferred |
| SIT-D027 | Auditor protection and no intervention | APPROVED detailed contract, B | Seven self-threats; no active source detector or automatic sanction |
| SIT-D028 | Capture, measurement and exact numbers | APPROVED completion direction, A | Architecture section 17; dependency section 16; candidate reviewed in section 5 below |
| SIT-D029 | IDs, witnesses, bytes and public outcomes | APPROVED completion direction, A | Architecture section 18; governance section 22 precision completion |
| SIT-D030 | Accounting, schedule and interruption | APPROVED completion direction, A | Architecture section 19; existing WU9 ceilings retained |
| SIT-D031 | Native file profiles and publication | APPROVED completion direction, A | Architecture section 20; dependency sections 15-17; no platform test certification |

No current decision authorizes implementation. There is no remaining undocumented technical choice among the four recorded blockers. Final Phase 0 approval remains a separate required owner event.

## 4. Work-unit supplements

| Supplement | Current status and evidence |
|---|---|
| WU6-C01-C03 | Accepted for continued design through the later recorded reporting/case dependency; no earlier bare continuation is backdated |
| WU7-C01-C02 | Accepted case baseline, as recorded in validation section 9 |
| WU8-C01-C03 | Accepted specification/test-planning basis for WU9; no executable test pass inferred |
| WU9-C01-C02 | Accepted Option B directions on explicit entry to WU10 |
| WU9-C03 | Approved uniform Apache-2.0 for original engineering material; split Apache/CC BY proposal superseded |
| WU10-C01-C03 | Accepted submission for final audit, with the four realization gaps now supplied |
| WU11 first pass | Historical BLOCKING result preserved at the pinned revision 0.6 |
| WU11 remediation re-audit | Technical candidate review passes with the precise limits in governance; final adoption not yet issued |

## 5. SIT-D028: input/capture/measurement closure

The original question and alternatives remain in revision 0.6 section 18. The completion supplies exact built-in caller types, a no-callback boundary, an explicit caller non-mutation precondition, iterative cycle-aware capture, alias-by-occurrence treatment, immutable private values, bounded lexical preflight and exact decimal/float handling.

Architecture section 17 fixes measuring form J, decoded-string versus encoded-byte counting, semantic set ordering and input acceptance. Dependency section 16 fixes the resource classification of an overlong numeric token. A precise binary float is not silently rounded into a different exact decimal. Host/caller concurrency that the runtime cannot prove absent is named as a precondition rather than falsely certified.

Witnesses W11-R01-R10 and the existing SIT-VG001/VG006/VG016/VG018/VG019/VG022/VG023 obligations give the future tests. Re-audit checked the represented distinctions and concrete arithmetic examples. No runtime parser/capture implementation was executed.

**Technical closure:** the missing protocol is supplied. **Adoption:** its exact candidate wording belongs to the final Phase 0 owner decision.

## 6. SIT-D029: report and invocation closure

Architecture section 18 fixes local ID anchors, finite representative paths/cycles, exact J+LF JSON, protected text presentation, explicit options, filenames, envelope/transport separation and execution exit meanings. Governance section 22 completes exact Markdown framing and cancellation transport so neither remains a renderer default or invented reason code.

Report-local IDs convey no global authenticity. A selected short witness never bypasses full ancestry/conflict prerequisites. JSON/Markdown preserve the same 57 analytical leaves and their basis. Native input failure data, validation rejection, interrupted processing, execution failure and publication acknowledgement remain distinct.

Witnesses W11-R11-R17/R31-R32 and the existing graph/report/interface SIT-VG families remain the future test owners. Full byte equality applies to the fixed realization profile and equal complete logical execution state, not arbitrarily different time-triggered interruptions.

**Technical closure:** deterministic rules and outcome mapping are supplied. No analytical field, content detector, overall score or network capability was added.

## 7. SIT-D030: resource and scheduling closure

Architecture section 19 defines the authority-free execution port, per-visit/byte/comparison charges, stable sorting and lookup model, global/per-scope ledgers, deterministic job order, lack of cross-job semantic caching, and atomic Result commits including premises, conflicts and witnesses.

The 1,024-unit emergency reserve is charged within the existing 10,000,000-unit global ceiling; it does not raise that ceiling or fund more analysis. The ordinary remainder is 9,998,976 units. Finalization consumes budget too. If no conforming report can fit, the caller receives an honest safe abort rather than a clipped complete report or a wrong input-validation state.

Witnesses W11-R18-R22 and the existing resource/graph/outcome tests preserve unfinished-search and late-contradiction boundaries. The sixty-second guard remains cooperative, with no hard-real-time or measured performance claim.

**Technical closure:** accounting and execution protocol supplied; numerical WU9-L01-L14 ceilings unchanged.

## 8. SIT-D031: filesystem and platform closure

Architecture section 20 selects descriptor/handle-bound Linux and Windows profiles, protected exclusive staging, fixed report names, source-read-only behavior, native no-replace directory publication, explicit commit acknowledgement and safe tracked-object cleanup. Dependency sections 15-17 make the ctypes/system-library boundary and pre-open regular-file check explicit.

The supported design names host, caller, volume and ownership assumptions. Missing native capability or failed protection disables that file operation; it cannot choose a permissive fallback. Observed successful publication is not relabeled absent after a later acknowledgement failure. No power-loss durability, administrator isolation, general anonymity or secure-erasure promise is made.

Official API facilities were checked as documentation. Witnesses W11-R23-R30 and W9's platform/security cases remain mandatory later executable evidence. No platform is claimed tested or released merely because its operation sequence is now specified.

**Technical closure:** concrete native/protection/publication protocol supplied; implementation and platform support verification remain later release gates.

## 9. Review findings resolved during completion

The final composition uses only SIT-RP-0.1 and J. There is no second CM1/JR1/MR1 contract. The output root vocabulary stays exactly the reporting document's 16-field table. No `not_yet_evaluated` or caller-cancellation reason was invented. Caller cancellation is a separate safe transport event as specified in governance section 22, while resource exhaustion retains `resource_limit_reached`.

The blocked first-pass findings were checked against their original acceptance conditions. Historical BLOCKING labels remain evidence of that first result, not current undocumented gaps. Conversely, this technical review is not the owner's final phase approval and cannot authorize a release or Phase 1.

## 10. Deferred features and remaining gates

Runtime crawling, hidden-lineage inference, active source poisoning/injection detectors, trust ranking, source-return infrastructure, automatic correction, shared toolkit internals and a universal score remain outside v0.1. No dependency or interface convenience reinstates them.

The remaining approval gate is the owner's adoption of the completed 18-document Phase 0 candidate. After that event, the authorized approval artifact must identify the exact candidate commit and SHA-256 of each approved file. A Phase 1 plan then requires its own exact file allowlist and authorization. Neither document is created by this re-audit.

## 11. History preservation and change record

The original decision alternatives, detailed recommendations and first-audit record remain accessible byte-for-byte in Git at the pinned revision 0.6. This revision changes the current index and closure record, not those historical bytes. No repository history was rewritten, no decision ID was reused, and no source paper or existing analytic oracle was modified.

The final candidate commit is reported only after all intended documentation writes and remote readback checks complete. Governance contains the audit methods and evidence limits. Local documentation checks are not product tests, independent review or empirical theory verification.
