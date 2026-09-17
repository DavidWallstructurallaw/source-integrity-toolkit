# GOVERNANCE_AND_HANDOFF

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Target release | v0.1 |
| Phase / work unit | Phase 0 / WU11 remediation and re-audit |
| Revision | 0.3 |
| Date | 2026-09-17 |
| Theory Owner | Xiangyu Guo |
| Technical Owner | Unassigned |
| Repository | DavidWallstructurallaw/source-integrity-toolkit |
| Technical review | PASS at specification-candidate level, with the declared implementation evidence limits |
| Final Phase 0 owner approval | Not issued |
| Phase 1 / implementation authorization | Not issued |
| Historical first-audit snapshot | 2a19833c53fd9a7b1065f568f470919d79583bfd |
| Completed architecture input | Revision 0.2, blob f9123f217e567b6aed34f876824c3dcd13dab467 |

## 1. Purpose and current authority

The owner requested: `可以，执行补齐，再进行 WU11 复审`. This authorizes completing the four identified realization gaps and performing their re-audit in this work item. That re-audit is performed here; it is not deferred for another permission to inspect the documents.

The complete earlier governance and first blocked-audit record remain preserved at the immutable historical reference in section 16. This current document consolidates the operative governance, records the completed review, and supplies the precision clarifications in section 22. It does not revise source papers or represent new detailed design as having been approved before it was written.

Technical readiness of a candidate, owner adoption of the complete Phase 0 baseline, and permission to implement the next phase are distinct events. Only the first is reported as passed here.

## 2. Governance roles

The Theory Owner approves product operationalizations, source interpretation, scope and public analytical changes, phase completion and responses to counterexamples. That role does not assign authorship of all contributions or ownership of third-party material.

The Technical Owner, when appointed, owns conformance of implementation, module boundaries, resource/failure behavior, dependencies, CI and release artifacts. This role cannot change theory meaning, qualification rules or denominators through a convenient code change. No specific technical maintainer or independent reviewer has been appointed by this document.

Maintainers can review work within an adopted contract. Public behavior, security, license or cross-project changes use the higher-level review gates below.

## 3. Change classes

| Class | Effect | Required treatment |
|---|---|---|
| C0 | Implementation-preserving refactor | Technical review and regression evidence |
| C1 | Contract clarification without changed outcomes | Owning specification and traceability review |
| C2 | Public field, denominator, relation or result-state change | Product/report/validation review and owner approval |
| C3 | Security, network, resource or protection change | Privacy/security/architecture review and explicit approval |
| C4 | Theory source/version or interpretation change | Source map/audit and affected product decision review |
| C5 | Licensing/distribution change | Actual rights review and explicit approval |
| C6 | Shared internals or cross-project semantic coupling | Separate interoperability proposal and approval |

Classify by strongest effect. Neither a refactor label nor passing tests can conceal a semantic change.

## 4. Authority and conflict handling

The approved Phase 0 plan and explicit owner decisions control their scopes. Later adopted detail supersedes an earlier proposal without rewriting its historical status. A candidate clarification becomes part of the proposed baseline; it is not a hidden runtime default.

On conflicting current requirements, identify the affected fields/documents, stop the affected conclusion or implementation, and obtain a scoped resolution. Update traceability and expected tests after resolution. CI cannot overrule a contract conflict. A failed future feasibility test reopens the relevant design rather than authorizing an insecure fallback.

## 5. Traceability governance

The binding remains SIT-TR ID to logical owner to concrete module/test owner. All 35 Trace IDs and 19 logical owners retain their identities. Architecture section 5 supplies their module homes; its completion sections add only internal execution/platform slots to existing owners.

Every one of the 57 analytical output fields keeps one primary Trace and its four SIT-VF obligations. Cross-cutting state, evidence, privacy, time and rendering rules remain additional requirements. A source-map citation alone never proves an implementation correct.

Moving a path without changing meaning is possible through an explicit binding update. Changing meaning requires its public-contract gate. The WU11 precision rules in section 22 bind to the existing normalization, report and runtime owners and their shared tests.

## 6. Validation governance

Later executable evidence includes structural contracts, the 228 field obligations, 26 shared families, H7/W7 golden cases, W9 security/resource cases, W11 realization cases, trace closure and packaging checks. An ordinary unit-test count or coverage percentage cannot substitute for these named duties.

A failure must be distinguished as an implementation defect, ambiguous specification, bad fixture evidence or product-model limitation. Preserve inconvenient counterexamples. Do not change golden expectations solely to make an implementation pass.

A correct number with a missing population, basis, qualification or uncertainty state fails. Documentation checks in this phase are not runtime tests.

## 7. Privacy and security governance

The accepted local/no-network/no-telemetry/non-intervention requirements remain controlling. Input locators and extensions stay inert. Protected-source references must preserve known commonality and explicitly represent withheld information. No anonymous/public-safe certificate is added.

The fourteen WU9-L limits remain unchanged. Their accounting and stopping interpretation is completed in architecture section 19. Platform support requires the later native/permission/fault tests, including no-clobber publication and failure before sensitive writes. Kernel, host configuration and privileged/same-principal compromise remain explicitly outside the claimed boundary.

## 8. Licensing governance

The owner selected Apache-2.0 for original engineering repository material, including documentation and fictional examples. The actual license/notice/scaffold files remain a later authorized step. Existing theory-paper licenses, third-party rights and user evidence are excluded from automatic relicensing.

A dependency or source asset keeps its own terms. Review actual versions and distribution contents. No license change, rights assignment, source-return charge or endorsement is inferred from a successful audit.

## 9. Versioning

Contract versions change when interpretation changes. Closed fields cannot acquire undocumented meanings through an alleged compatible extension. Old snapshots retain their original version; conversions must be explicit and provenance-preserving.

Package versioning begins with implementation and its release policy. No package release is fabricated here. Internal byte-profile refinements before initial release are recorded in the candidate and locked only with the approved baseline. After adoption, changing those bytes or outcomes follows the appropriate C1/C2/C3 process.

## 10. Repository workflow

Direct specification commits to main remain authorized for this project. Later substantive implementation should use reviewed branches/PRs and phase-appropriate CI. This document does not claim branch protection or CI has been installed.

No real private dossier, hidden identity map, source-paper PDF, executable fixture or generated user report belongs in this Phase 0 repository. The current work changes documentation only. Historical documents remain retrievable through immutable commits, and current-status indexes explicitly identify their historical references.

## 11. Cross-project separation

Source Integrity Toolkit and Recursive Integrity Toolkit remain peer products. No internal import, submodule, shared database, vendored internal package or integrity-core dependency is selected for v0.1.

A later public-artifact adapter must preserve contract versions, query/claim scope, types, assertion provenance, unknown/disputed states, population meaning and privacy boundaries. Unsupported mappings must be rejected or explicitly qualified; successful conversion is not independent validation. This candidate creates no adapter.

## 12. Phase 0 to Phase 1 gate

The complete 18-file candidate is ready for the owner's final adoption after the documentation writes and readback checks for this re-audit. That adoption has not occurred merely because the owner requested the audit.

After adoption, PHASE_0_APPROVAL.md must identify the exact final candidate commit and SHA-256 of every approved file, its approved decision effects, exclusions and authorized next planning boundary. The approval document must not hash itself as a member of its own input baseline.

A separately authorized PHASE_1_PLAN.md then supplies the exact scaffold file allowlist. Final Phase 0 approval cannot be presented as blanket analytical implementation authority.

## 13. Phase 1 handoff payload

The candidate hands off the plan, product/ontology/analysis/report specifications, source map, current decision register, 35 Trace bindings, field/shared validation obligations, H7/W7 cases, W9 privacy/limits, the completed SIT-RP-0.1 realization and Apache-2.0 policy.

Phase 1 may scaffold imports, contract placeholders, fixture/test structure, metadata, licensing files and CI only within its own approved plan. It must not implement ancestry traversal, qualification, concentration, evaluator overlap, correction analysis, report generation or native security behavior prematurely. Empty modules cannot be described as satisfying their Trace obligations.

## 14. Release stops

Stop if a public result lacks a semantic/test owner, an output loses uncertainty, a dependency introduces hidden authority, source data can override limits, native protection is unverified, JSON and Markdown disagree, an unfinished search becomes an absence, rights are swept into the project license, or an adapter loses provenance.

Also stop when a later actual platform test contradicts the selected primitive composition. This document's source checks establish the facilities being specified, not successful execution of the eventual composition.

## 15. Accepted work-unit directions

WU9-C01/C02 were accepted on explicit entry to WU10. WU9-C03 was explicitly resolved to Apache-2.0. WU10-C01-C03 were accepted as submissions for final audit. The first WU11 pass correctly exposed four missing protocols. The present owner instruction authorized completing those protocols and conducting this second pass.

No earlier bare continuation is retroactively changed into a different approval. New precise choices in the completed candidate remain visible for final owner adoption.

## 16. Immutable first-audit history

The unabridged governance revision 0.2, including first-pass findings W11-A01-W11-A07, registry checks and its input manifest, is preserved at:

`https://github.com/DavidWallstructurallaw/source-integrity-toolkit/blob/2a19833c53fd9a7b1065f568f470919d79583bfd/GOVERNANCE_AND_HANDOFF.md`

Its blob is `4cbd35a32e00215f803bc1ffb03508c5fd341cba`. The full contemporaneous decision register is preserved at the same commit, blob `0245b20b77a41a9f7a0fad510dd4dc5553715592`.

This revision consolidates present governance and review status. It does not erase that first BLOCKING result or claim its gaps were already closed then. Historical section references resolve against those immutable versions.

## 17. Re-audit disposition

| Original finding / decision | Supplied realization | Re-audit result |
|---|---|---|
| W11-A01 / SIT-D028 | Architecture section 17 fixes types, immutable capture, exact scalars, J measurement and acceptance; dependency section 16 fixes numeric guard classification | PASS: the missing specification exists; caller/host limitations are explicit |
| W11-A02 / SIT-D029 | Architecture section 18 fixes local IDs, witnesses, output/interface meanings; section 22 below fixes exact framing and cancellation transport | PASS: no renderer default or invented cancellation evidence state remains |
| W11-A03 / SIT-D030 | Architecture section 19 fixes charges, schedule, shared-work rule, reserve, result commits and abort behavior | PASS: ceilings and unfinished-result meanings remain intact |
| W11-A04 / SIT-D031 | Architecture section 20 and dependency sections 15-17 fix native primitives, private creation, non-replacement, commit acknowledgement and cleanup | PASS as a specified design; future native conformance tests remain required |

These are technical documentation closure results. All four recommended completion directions are recorded in the current register. No unresolved engineering gap from the first-pass list remains in this candidate. Overall phase adoption and runtime validation are not represented as passed.

## 18. Verification results

### 18.1 Recomputed checks

Local original WU1-WU8 text was matched to the unchanged repository blobs before it was used for source/field/Trace checks. The current architecture, dependency, governance, licensing, privacy and threat additions were read through the connected repository and/or checked as exact local outgoing documents. No unverified local predecessor is presented as a current remote version.

| Check | Result |
|---|---|
| Source-map identities | 40 SIT-T entries retained |
| Product requirements | 16 SIT-P identities retained |
| Analytical families | 15 SIT-M identities retained |
| Trace ownership | 35 SIT-TR identities and 19 logical owners retained |
| Public field equality | All 57 fields match across reporting, traceability and validation tables |
| Field obligations | Exactly 228 P/N/M/B IDs, four for each of 57 fields |
| Shared validation | 26 SIT-VG families retained |
| Runtime prerequisite vocabulary | 24 PC identities retained |
| Reason vocabulary | 40 existing reason codes; no new cancellation or guessed not_yet_evaluated code |
| Success criteria | 66 SIT-SC identities retained |
| New realization cases | 32 W11-R cases specified with future test-path ownership |
| Basic numeric witnesses | J fragment length 13 bytes; 26/36 rounds half-up to 0.722222; 10,000,000 minus 1,024 is 9,998,976 |

The tests here are document-set, identifier, arithmetic and outgoing-file checks. No production parser, serializer, graph routine or platform adapter was implemented or executed to obtain them.

### 18.2 Unchanged epistemic and analytical requirements

The 12 record kinds, 24 predicates, 9 assessment kinds and 22 finding conditions remain in their existing authoritative documents, which this remediation does not edit. Qualified process independence remains scoped and evidence-based. Missing ancestry cannot become a root. Disagreement remains representable. Structural consistency cannot authenticate a coherently fabricated dossier.

H7-01 retains its six source contributions and the conditional 26/36 HHI. The one-origin selected variant remains 25/25. An added unresolved contribution and a known unallocated multiparent contribution both withhold the full scalar while preserving their distinct profiles and full denominators. Pipeline cohorts and correction target sets are not silently changed by source selection.

The three documented linked changes remain their own evidence. A missing change is not a failed correction, an accepted objection is not proof of truth, and a route is not evidence that it was used.

### 18.3 Review limits

This is the drafting assistant's review, not an independent second reviewer, penetration test, platform certification, legal clearance or scientific validation. Primary documentation was checked for the native/API facilities. ABI correctness, runtime determinism, exact byte golden files, actual performance and all fault/race tests remain future executable evidence under their named owners.

A later test failure must reopen the relevant design when necessary. It must not be hidden by replacing the written oracle or lowering the security boundary.

## 19. Candidate file inventory and identity procedure

The candidate consists of exactly these 18 Markdown paths:

| Path | Role |
|---|---|
| PHASE_0_PLAN.md | Approved phase/work-unit boundary |
| SPEC_AUDIT.md | Original source audit |
| THEORY_SOURCE_MAP.md | Forty-entry theory provenance map |
| UNRESOLVED_DECISIONS.md | Current decisions with immutable historical references |
| PROJECT_INSTRUCTIONS.md | Execution rules and historical work-unit authority |
| V0.1_PRODUCT_SPEC.md | Product requirements and scope |
| DEFINITIONS_AND_UNITS.md | Object, analytical and unit semantics |
| CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md | Logical input and hero representation |
| SOURCE_INTEGRITY_THREAT_MODEL.md | Threat/self-protection classes and W9 cases |
| OBSERVABILITY_AND_REPORTING.md | States, prerequisites, field catalog and report envelope |
| THEORY_TO_CODE_TRACEABILITY.md | Thirty-five responsibilities and field/test bindings |
| VALIDATION_PLAN.md | Hero/micro-case oracles and future test obligations |
| PRIVACY_AND_DATA_HANDLING.md | Privacy, safe I/O and fourteen fixed ceilings |
| LICENSING_NOTES.md | Approved Apache-2.0 engineering policy with exclusions |
| SUCCESS_CRITERIA.md | Cumulative specification/release gates |
| REPOSITORY_ARCHITECTURE.md | Module owners and completed SIT-RP-0.1 protocol |
| DEPENDENCY_STRATEGY.md | Runtime/build/test and fixed native dependency boundary |
| GOVERNANCE_AND_HANDOFF.md | Current governance, re-audit and adoption handoff |

Use the final remote commit after the four intended documentation changes as the immutable candidate identity. Compare its full tree with the first-audit commit: no added/deleted path, implementation file, package metadata, LICENSE or CI is permitted in this work item. The fourteen unaffected paths must retain their original blobs.

Git blob identities establish the comparison now. The approval artifact, created only after owner adoption, must calculate the separate requested SHA-256 manifest from that exact final candidate; Git SHA-1 identifiers must not be mislabeled SHA-256. This document avoids a self-referential claim to contain its own final hash. No missing hash is fabricated.

## 20. Current stop point

The requested remediation and WU11 technical re-audit are complete for the candidate described here, subject to final remote write/readback confirmation. The next decision is final owner adoption of this complete Phase 0 baseline, not another authorization to perform the same re-audit.

No PHASE_0_APPROVAL.md, PHASE_1_PLAN.md, LICENSE, implementation package, executable schema, runtime fixture or workflow is created. On adoption, the approval record must use the actual final file identities and preserve the remaining scaffold and implementation prohibitions.

## 21. Re-audit change control

This candidate completes the four previously approved-direction remedies rather than revising theory or adding analytics. It also consolidates the current governance and decision indexes, with the unabridged historical text preserved by pinned Git references. The consolidation is explicit; the previous observations and approval evidence remain available unchanged.

Sections 17-20 of architecture remain the protocol owners. Section 22 below is a binding precision supplement to that same SIT-RP-0.1 candidate, assigned to those existing owners. No implementation may ignore it as non-normative commentary. A later purely editorial relocation into the owning sections must preserve its outcomes.

## 22. Precision resolutions checked in the second pass

### 22.1 Numeric guard and schema vocabulary

The existing numeric-token scan ceiling is a resource guard. An overlong raw token or exact in-process emitted token stops with resource_limit_reached, as required by privacy section 8.3; it is not a new structural source-quality rule. Out-of-range exact integers, non-finite numbers and incompatible field types remain structural errors. No bool is an integer count.

Integral normalization is a mathematical JSON-number convention for fields that admit numbers; it never bypasses a stricter field's declared type or range rule. J changes formatting, not claim/evidence relationships. A derived report introduces none of the speculative root fields used in informal examples: the actual root keys remain reporting section 16.1's exact table.

### 22.2 Exact Markdown framing

Complete architecture section 18.3 with this fixed layout. The document starts with `# Source Integrity Audit` followed by two LF characters, then the tool-controlled lines `Report kind: <report_kind>`, `Processing state: <run.processing_state>`, and `Input state: <input_validation.state>`, each followed by LF, then one blank line.

Visit the 16 root keys in reporting section 16.1 table order. Emit `## <root_key>` followed by two LFs. For every root except results, emit its complete value in a fenced pretty-JSON block. Pretty JSON uses J's key ordering/scalars, two spaces per indentation level, comma then LF between entries, colon then one space, no trailing commas/spaces, and compact empty arrays/objects. Nonempty arrays/objects place one entry per indented line and a closing delimiter at the opening indentation. Scalars occupy one line. A block ends with one LF before its closing fence, and the fence is followed by two LFs.

For results, emit one `### <Result ID>: <field_key>` heading followed by two LFs, then that complete Result block. For each available fraction Result, emit the exact decimal-display line from architecture section 18.3 and two LFs. Emit `Reason details` and two LFs, then the complete array of referenced Reasons in their canonical order as another block. An empty results array is represented by a single empty-array block. Do not display a summary number without its Result scope/population/basis references and qualifications; all linked details appear in the corresponding root sections.

Every block has a tool-owned backtick fence of length max(3, one greater than the longest consecutive backtick run in its body), with the opening info string json. Source strings occur only inside encoded block values. After the final block, remove the final extra blank line so the Markdown ends with exactly one LF. The JSON sibling is J of the same frozen envelope plus one LF.

This selects representation bytes only. It adds no report field and does not alter any availability, witness or numeric oracle. Unknown run times use the already allowed TimeValue fields state/value/precision/reason, with a truthful not-recorded reason.

### 22.3 Caller cancellation is not resource exhaustion

The resource/cancellation shorthand in architecture section 18.4 is refined here. A caller/KeyboardInterrupt cancellation is a separate safe transport event: preserve the actual accepted/not_completed state and known publication state in a payload-free AuditCancelled outcome/exception; CLI exits 130. It may suppress report delivery. It does not fabricate resource_limit_reached, execution_failed, analysis_not_selected or a new report reason code merely to label that cancellation.

A resource guard still uses exit 3 and its existing reason. An actual runtime/I/O failure still uses exit 4. A native source record saying failed remains data. First safely established cause controls a simultaneous stop; later cancellation cannot change an already observed publication commit into no publication. Hard termination may have no return. No public cancellation callback or source-provided handler is introduced.

### 22.4 Path and native protection limits

Dependency section 15 adds a no-follow regular-file precheck before Linux's existing descriptor read. The subsequent regular descriptor and identity checks remain necessary; this is not a check-then-open security claim without the accepted parent/owner/quiescence assumptions.

For Windows, the selected output parent must be controlled by the invoking principal or trusted OS administrators/system identities. Refuse unrecognized ordinary write/delete-child authority when it prevents establishing that profile; do not repair the caller's parent ACL. Retained directory handles, private creation descriptors and no-replace publication remain required. Unexpected sharing/permission/ABI behavior fails safely and keeps that platform unclaimed until its tests pass.

The current primary Microsoft documentation permits a relative rename target through RootDirectory and specifies error on an existing target when ReplaceIfExists is false. The complete safe directory transaction remains a project composition requiring future tests. No primitive documentation is presented as a tested proof of the composition.

### 22.5 Deterministic optional choices and witness ordering

For this reference profile, deduplicate identical explanatory report objects by their complete ID-free semantic bodies and anchor keys; do not leave that choice renderer-dependent. Never deduplicate input records or distinct input IDs. Two unequal values for one Result slot are an internal error.

To break equal-length path ties, compare the complete edge-key sequence, not only the final predecessor's local ID. A breadth-first distance pass followed by lexicographic ranking of complete predecessor prefixes meets the rule. Cyclic-component and all-parent/conflict checks remain independent of which representative is selected.

### 22.6 Scope of this pass

These precision resolutions are part of the proposed final baseline and bind the existing normalization/report/runtime owners and W11-R/SIT-VG tests. They were reviewed as documentation now; they were not implemented. They close the identified ambiguity instead of moving a hidden decision into a later code default. Final owner adoption of this candidate remains required.
