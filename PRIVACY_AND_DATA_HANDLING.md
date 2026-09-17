# PRIVACY_AND_DATA_HANDLING

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Target release | v0.1 |
| Phase / work unit | Phase 0 / Work Unit 9 |
| Revision | 0.1 |
| Date | 2026-09-17 |
| Status | PROPOSED FOR REVIEW; documentation only |
| Theory Owner | Xiangyu Guo |
| Technical Owner | Unassigned |
| Repository baseline | `bfebc1095ff000f816e21fecf34df32debe6727b` |
| Controlling inputs | Definitions 0.2; lineage 0.3; reporting 0.2; product 0.4; validation 0.2; traceability 0.1 |
| Review items | WU9-C01: handling and disclosure; WU9-C02: bounded processing |
| Companion files | Licensing notes 0.1; threat model 0.2 |
| Implementation / final Phase 0 approval | Neither is created by this document |

## 1. Purpose, authority and source basis

This contract specifies how the planned local auditor handles supplied evidence without exposing protected identities, treating content as instructions, or overstating what a redacted dossier establishes. It realizes PLAN Work Unit 9, SIT-D014/SIT-D021/SIT-D027 and the later gates in SIT-TR029-SIT-TR031. The current instruction explicitly requests Work Unit 9 and direct GitHub delivery. It authorizes these three specification files, not a software implementation or a new license grant.

The theory basis remains the supplied papers, through the existing map. SIL pp. 13-15 and HDL §§9.3-9.8 motivate inspectable provenance, source functions and correction; EC §§7.3-7.5 requires preservation of epistemic status, uncertainty and corrective capacity. These sources do not prescribe filesystem permissions, parser budgets, retention periods or the disclosure design below. Those details are proposed toolkit operationalizations. No legal-compliance, anonymity or security certification follows from adopting them.

The output allowlist is `PRIVACY_AND_DATA_HANDLING.md`, `LICENSING_NOTES.md` and `SOURCE_INTEGRITY_THREAT_MODEL.md`. Existing input/output record types, fifteen analytical families, fifty-seven leaves, twenty-four prerequisite checks and forty reason codes remain unchanged. Central decision-register updates and architecture belong to later authorized units. Earlier approval records remain historical; the present contract does not backdate them.

The offline rules below govern the future auditing runtime. The owner's authorized use of GitHub to publish project specifications is a separate authoring operation.

## 2. Actors, authority and data classes

The caller chooses the inquiry and must have authority to process the supplied material. A protected-source custodian may prepare an opaque, disclosure-appropriate dossier. The toolkit receives the selected payload and explicit local output authority only. A report recipient acquires no right to resolve confidential identities, inspect an external locator or alter an audited system through the report.

Sensitivity is an operational handling concern, independent of truth, source quality, governance layer and `epistemic_type`. The following classes are review categories, not new JSON enums or an automatic classifier.

| Material | Required treatment |
|---|---|
| Public URL or document citation | Keep as inert supplied data; public availability does not authorize fetching, republication or automatic trust |
| Private document or excerpt | Minimize before ingestion; keep the source read-only; do not copy its entire content into a report |
| Confidential identity, contact address or whistleblower metadata | Prefer a dossier-local opaque reference; keep the identity mapping outside the bundle and outside the runtime |
| Personal or high-consequence case data | Include only inquiry-relevant, authorized information; no additional profiling or demographic inference |
| Internal model, benchmark, evaluator or dataset lineage | Treat names, versions, relationships and evaluation targets as potentially confidential, even without personal names |
| Keys, credentials and authenticated URLs | Exclude secrets before ingestion; a locator cannot authorize authentication or external access |
| Derived graph, population, witness or exact timestamp | Review as potentially identifying; aggregation and pseudonyms do not establish anonymity |
| Theory and specification reference material | Preserve authorship and existing rights notices; follow the separate licensing contract |
| Example and test material | Use fictional records and synthetic canaries; no real protected evidence in the public repository |

A disclosure label supplied in an extension cannot change runtime permissions or analytical rules. The tool does not detect every secret or determine whether the caller's legal authority is sufficient.

## 3. Local runtime and input discipline

### 3.1 Authorized input

The future runtime accepts the single selected local UTF-8 JSON file or the equivalent in-process logical value, as already specified. It reads no neighboring document, predecessor snapshot, credential store, identity map, attachment, URL or locator to supplement the evidence. External schemas, update checks, telemetry, remote model calls and plugin loading are excluded from v0.1.

The input remains unchanged after success, structural rejection, cancellation, output failure and execution failure. An in-process value is validated and frozen for this invocation without mutating the caller's object. WU10 must specify the snapshot-copy and concurrent-mutation handling strategy. A failed or inconsistent capture cannot produce a completed audit of an invented stable input.

Only ordinary JSON-compatible built-in containers/scalars are admitted at the library boundary. Custom mappings, lazy iterables, objects with serialization callbacks and executable object wrappers are rejected before invoking their custom behavior. Their conversion belongs to the caller, outside the auditor. Duplicate JSON keys are checked for raw files; an already constructed dictionary cannot prove that an upstream parser never discarded duplicates.

### 3.2 Inert data

Methods, descriptions, URLs, names, `extensions`, code-looking strings and protected attestations remain data. No `eval`, template execution, dynamic import, shell expansion, object deserialization, external entity resolution or user-defined predicate is permitted. The approved relation registry alone determines graph meaning.

A local locator does not become a file-read instruction. A URI beginning with a file, network or executable scheme is still an inert value in an admitted text field. At the invocation boundary, such a URI is not a permitted input-file path. Structural parser checks and output escaping are required; they do not constitute an active content-injection or poisoning detector.

### 3.3 Input evidence and protection

Use existing `SourceActor.identity_disclosure`, nullable fields with `Gap`, `UnresolvedReference`, `Provenance` and `EvidenceReference` structures. A protected attestation must distinguish its inspectable summary from unavailable underlying material. A name can be withheld while a known shared reference remains visible.

Neither a protected label nor an opaque `identity_key` qualifies an origin or an independent process. Several pseudonyms do not establish several people. An unresolved protected reference does not establish its hidden origin count. If the relevant method, scope or support cannot be supplied even in a permitted attestation, the affected stronger result remains unavailable under the existing qualification rules.

## 4. Disclosure and redaction contract

### 4.1 Selected v0.1 approach

The recommended design uses **caller-prepared disclosure-appropriate snapshots and complete local reports over those snapshots**. It adds no automated identity resolver, anonymizer, secret scanner, public-report certification, policy-expression language or post-audit semantic redaction engine.

The same bundle can be processed for authorized local review without being suitable for public distribution. Report creation is not publication permission. The caller must review intended recipients and the allowed disclosure of graph topology, time, methods, qualifications and supporting references before distributing any result.

A report includes its exact analytical basis at the level supplied and allowed by the existing reporting contract. It must not require publication of the real name behind an opaque reference.

### 4.2 Report data minimization

Both JSON and Markdown use the same disclosure selection. The future renderer selects only the fields needed for the report's defined scope, populations, basis, native outcomes, reasons and witnesses.

Do not automatically export full input records, source excerpts, contact locators, actor display names, `identity_key` values, arbitrary extensions, absolute local paths or identity-mapping material. Input IDs and relevant basis/method/qualification text still appear where the established report contract requires them. The caller must therefore make those fields suitable for the intended recipient; identifiers are not automatically non-identifying.

Evidence-reference availability and permitted reference IDs remain visible when an excerpt is not reproduced. A report cannot replace a specific substantive qualification with a generic reassuring statement. If a required explanation contains information that cannot be disclosed, prepare a new protected snapshot with an adequate permitted explanation or refrain from distributing the full audit. Do not silently remove the qualification from one format.

### 4.3 Preparing a shareable snapshot

A custodian preparing a separate shareable input must:

1. assign a new snapshot identity and record that a disclosure transformation occurred using existing provenance, qualifications, gaps and predecessor fields;
2. replace identifiers consistently within that snapshot, preserving equality and known commonality where authorized;
3. remove unnecessary identity/contact text and supply permitted context, protected attestations or explicit unresolved records where required;
4. retain claim/version scope, disputed premises and population meaning, or explicitly declare changes;
5. re-run the audit on that actual supplied snapshot before presenting its output as a toolkit report.

This is a caller-authoring procedure. v0.1 does not implement the transformation or open the original snapshot through the `predecessor` field.

A purely consistent renaming preserves the represented topology. Removing support can weaken qualification; removing a seed changes the statistical population. The new report must show those consequences. Counts or HHI from the private input cannot be pasted into the new report as if computed from its reduced evidence.

Where even commonality is confidential, do not invent several independent roots to conceal it. Use an explicit undisclosed frontier and limit the conclusions, or keep the result restricted. An incomplete extract made by a person must be labeled as an extract with its omitted context, not as a complete `sit-report/0.1` audit.

### 4.4 Residual disclosure risk

A graph's shape, rare role, date, institution, document title, quoted phrase or case membership may reveal identity. A raw checksum can link copies or enable comparison with guessed material. No k-anonymity, differential-privacy, cryptographic-attestation or secure-erasure guarantee is selected here. The runtime cannot prevent downstream recipients from combining an exported report with other information.

## 5. Filesystem and destination boundary

### 5.1 Input opening

The caller supplies an explicit path to a regular file on a filesystem authorized for this invocation. Directories, devices, sockets, named pipes and executable/remote resources are not input payloads. Reject symbolic links and platform-equivalent junction/reparse redirections in the selected path rather than following them silently. WU10 must choose handle-based operations and platform checks that preserve this condition through opening.

Reject explicit network shares and URI-form invocation paths. A filesystem mounted by the host may conceal remote storage; the caller must ensure the selected volume is local. The no-network runtime claim concerns the auditor's own behavior and cannot certify the host's mount, backup or synchronization configuration.

Record identity and file metadata around the read where supported; observable replacement or mutation aborts the invocation. File metadata checks do not prove absence of an undetectable hostile host. The evidence of an accepted audit is the bounded byte sequence actually read, not a promise that an external path remained immutable forever.

### 5.2 Output publication

The proposed v0.1 writer uses a new output directory under an explicitly authorized parent. It never overwrites an existing report directory or file. The caller chooses a fresh destination when retaining another report. There is no force-overwrite option in this release contract.

Reject output redirections, symbolic links, junctions, special files and any destination that aliases the selected input. Filenames inside the directory are tool-controlled; source labels, input IDs, locators and extension values cannot become paths. WU10 owns the exact CLI/API names and final fixed filenames.

New report directories must be private to the invoking principal: owner-only access on POSIX-like systems, and an equivalent supported ACL policy on other supported systems. Directory creation and file publication must not briefly expose permissive intermediate files. If the required protection cannot be established, fail the write rather than emit a report with a privacy-success claim. Do not modify global process permissions or the caller's unrelated ACLs to achieve this.

### 5.3 Pair integrity and temporary files

Produce both representations from one frozen logical result. Stage them in an exclusively created private directory in the authorized parent, using non-source-derived names. Final publication must be a no-clobber operation on the report directory after both files pass their completeness and parity checks. The implementation must not silently replace a concurrent destination that appears after preflight.

Before publication failure, remove only staging files created by this invocation, when safe. Never recursively clean an arbitrary caller directory, follow a cleanup link or remove source evidence. A crash can leave a private, clearly uncommitted staging directory. Recovery and cleanup must be explicit and scoped to that known directory; no automatic scan of unrelated files is authorized.

Ordinary deletion is not secure erasure. Host backups, snapshots, swap, crash dumps and cloud synchronization remain outside this toolkit's controls. There is no mandatory background retention service or scheduled cleanup worker.

## 6. Logs, diagnostics and retention

### 6.1 Default surfaces

No telemetry, automatic crash upload, persistent application log, cache, database or source-copy archive is enabled in v0.1. The library returns its result or safe failure to the caller and does not print the dossier. The CLI's default terminal output contains tool-controlled completion/error information only; full reports go to the explicitly selected private destination. A report-to-stdout mode is not selected by this contract.

Diagnostics must not echo arbitrary input values, excerpts, credentials, full paths, record IDs supplied by a source, or exception representations containing them. Use fixed codes, generic messages and safe canonical field locations or array positions. For unknown keys or malformed identifiers, report the location/type condition without printing the rejected string. The existing diagnostic `qualifications` can identify this suppression without adding a source-quality judgment.

Sensitive methods and qualifications belong only to the approved report disclosure, never incidental debug logs. No user-content debug-dump switch is selected for v0.1.

### 6.2 Byte digests and correlation

Raw-file digest calculation is an explicit invocation choice, disabled by default. When not requested, `input_identity.raw_file_digest` is null and its existing `qualifications` explains why. No new reason code or schema field is introduced.

When requested, compute SHA-256 only over the entire input byte sequence actually read and identify that coverage. An interrupted partial read must not be labeled as a whole-file digest. In-process input has no raw-file digest. Do not generate a stable pseudonym by hashing a person's name, contact detail or secret.

This setting does not change analytical results. It affects one documented metadata choice and must be the same in JSON and Markdown. Public specification-file hashes used during project authoring are separate from runtime disclosure of a private dossier.

### 6.3 Retention and later correction

Inputs remain caller-owned read-only material. Results returned in memory and published reports remain under the caller's retention controls. The tool releases its working references on completion; it does not claim cryptographic memory zeroization. A failed invocation must not reuse cached results from a previous snapshot.

Keep historical evidence only where the custodian's authority permits. Snapshot immutability is an identity rule, not an instruction to retain prohibited personal data indefinitely. A later corrected, minimized or withdrawn dossier receives a new identity with appropriate disclosure limits. No toolkit action automatically edits external sources, deletes published histories or contacts an affected person.

## 7. Safe rendering

Untrusted strings cannot define report structure. Use tool-authored headings, field labels and interpretation rules. Encode source text so HTML tags, images, autolinks, table separators, heading markers and fence delimiters cannot become active Markdown structure. Escape HTML metacharacters before introducing renderer-owned presentation. Represent line breaks inside table cells safely. Locators stay literal text; no preview, active image, automatic browser launch or local-file link is emitted.

In displayed source values, expose rather than execute terminal escape/control sequences and bidirectional formatting controls. Preserve the original value in the authorized input, with the displayed transformation identifiable through existing basis selectors and report qualifications. Avoid hidden markup comments containing source data. JSON string encoding preserves literal data, and a downstream viewer must not treat it as trusted HTML or executable configuration.

This policy is deterministic output encoding. It does not classify the author as malicious or infer what an instruction-shaped sentence intended. Legitimate multilingual text remains admitted; control handling must not erase substantive text or merge distinct identifiers. WU10 must choose and test the exact escaping implementation against both ordinary and adversarial cases.

## 8. Bounded processing and portable numbers

### 8.1 Proposed v0.1 limits

These are design ceilings for a bounded first release, not measured performance claims or calibrated integrity thresholds. Equality is allowed unless another independent condition fails. A caller may request stricter ceilings through a future trusted invocation surface; source data cannot raise or disable them. Raising a release ceiling requires a documented specification change and renewed boundary tests.

| Limit ID | Maximum | Counting rule |
|---|---|---|
| WU9-L01 | 16,777,216 bytes | Entire raw UTF-8 bundle; in-process measurement uses the equivalent bounded compact JSON representation defined by WU10 |
| WU9-L02 | 32 container levels | Root object has depth 1; each nested object/array increases depth, including extensions |
| WU9-L03 | 32 inquiries | Whole supplied bundle, not only a selected target |
| WU9-L04 | 10,000 typed records | Includes unresolved references and records irrelevant to a selected result |
| WU9-L05 | 30,000 assertions | All polarities, lifecycle states and assessment kinds |
| WU9-L06 | 10,000 evidence references | All reference kinds and availability states |
| WU9-L07 | 200,000 reference occurrences | Each canonical record/assessment/reference-link occurrence, including repeats in different fields |
| WU9-L08 | 500,000 JSON value nodes | Containers and scalar values, including inert extensions; keys are separately byte-limited |
| WU9-L09 | 128 ASCII bytes per identifier; 128 characters per numeric token | IDs retain the existing grammar; numerical-token scanning is bounded before number construction |
| WU9-L10 | 65,536 UTF-8 bytes per string/key; 4,096 bytes per locator | After JSON escape decoding; includes narrative, qualification and extension strings |
| WU9-L11 | 1,000,000 work units per capability/scope; 10,000,000 per invocation | Each examined node/link/support record, comparison or emitted result/witness item consumes at least one unit |
| WU9-L12 | 60 seconds cooperative processing time | Monotonic elapsed guard over validation/analysis/rendering; checks at bounded work intervals |
| WU9-L13 | 20,000 witnesses; 100,000 total witness members | Entire report, counting retained reference entries; no silent truncation |
| WU9-L14 | 67,108,864 bytes per report representation | Separate encoded JSON/Markdown ceilings; check during bounded staging |

WU10 must specify traversal scheduling, amortized/container work accounting, compact in-process byte measurement and cancellation points. No operation may hide an unbounded scan inside one declared work unit. Time guards are cooperative; this document makes no hard latency or resident-memory guarantee. A hostile host or uninterruptible OS operation remains a deployment boundary.

A resource-exhausted invocation cannot drop a late contradiction, keep an early count and call the whole dossier complete. WU8's positive/negative/missing/boundary tests must cover extension payloads and objects outside the selected analytical subgraph as well as ordinary inputs.

### 8.2 Integer compatibility

Every serialized exact integer is within `[-9007199254740991, 9007199254740991]`; analytical counts and fraction components are nonnegative, with positive denominators. Booleans are never integer counts. Integer magnitude is checked without first coercing a large token to an inexact floating value. NaN, infinity and non-JSON numeric forms are rejected.

Non-integer numbers admitted by an existing metadata/extension field remain inert and cannot supply weights or a new quantitative policy. WU10 must specify their loss-aware parse/serialization behavior; accepting a value and silently changing it is forbidden. No numeric strings replace the established integer/fraction fields. If a consumer cannot preserve a permitted exact value, it must reject that presentation rather than round it.

The selected record ceiling places the contribution-count HHI denominator N squared at no more than 100,000,000 for the defined EvidenceItem population. This is a consequence of the input bound, not a change to the formula or hero oracle. Keep 26/36 and its bucket/membership evidence in H7-01; do not replace the stored denominator with a rounded decimal.

### 8.3 Failure mapping

| Event | Existing contract treatment |
|---|---|
| Invalid syntax, duplicate key, invalid identifier/type/time, prohibited exact integer magnitude | Structural rejection with the corresponding existing diagnostic code; length/range constraints use `input_constraint_violation` with this section as basis |
| Aggregate byte/depth/count/work/time guard stops processing before acceptance | `processing_diagnostics`, `interrupted`, input `not_completed`; reason `resource_limit_reached`; no analytical salvage |
| Guard stops after accepted input | Interrupted `audit_report` only when the valid interrupted envelope can be emitted; independently completed cells may remain, unfinished cells are `not_evaluated` |
| Missing dossier evidence after a completed check | Existing field-specific `unavailable` result; not a processing failure |
| Unexpected exception, inaccessible/prohibited destination or inability to preserve required file protection | Safe processing failure; existing `execution_failed` meaning; no completed publication claim |
| Output size/pair-publication failure | No final report pair; safe failure or interruption through the caller channel; do not publish a clipped successful report |
| Caller cancellation or hard host termination | No completed result is fabricated; record interruption if safely possible; a killed process may emit nothing |

Identifier and string lengths are structural field constraints. Aggregate budgets and numeric-token scanning are resource guards. Several simultaneous failures do not authorize a stronger assertion about unexamined input. The first safely established outcome is reported with its scope. Source-native states such as a correction record's `failed` remain data and do not set run status.

## 9. Stable control obligations

These control IDs bind the new specification; they add no analytical field or central decision ID.

| ID | Obligation | Existing trace / validation owner |
|---|---|---|
| SIT-DH001 | Explicit single input; read-only bytes and frozen in-process value | SIT-TR028, SIT-TR029; SIT-VG020, SIT-VG023 |
| SIT-DH002 | No network, locator opening, model or external resolver | SIT-TR029; SIT-VG020 |
| SIT-DH003 | Inert content and no custom object execution | SIT-TR001, SIT-TR029; SIT-VG001, SIT-VG019 |
| SIT-DH004 | Opaque identities with distinct visible/withheld evidence | SIT-TR030; SIT-VG007, SIT-VG021 |
| SIT-DH005 | Preserve commonality, uncertainty and assurance under protection | SIT-TR005, SIT-TR009, SIT-TR030; SIT-VG002, SIT-VG021 |
| SIT-DH006 | Disclosure-appropriate snapshots; no automatic public-safe claim | SIT-TR030; SIT-VG021 |
| SIT-DH007 | Minimal report fields and identical format disclosure | SIT-TR026, SIT-TR030; SIT-VG017, SIT-VG021 |
| SIT-DH008 | New identity and re-audit for materially redacted evidence | SIT-TR020, SIT-TR030; SIT-VG006, SIT-VG021 |
| SIT-DH009 | No symbolic/redirection or unsafe file-opening paths | SIT-TR029; SIT-VG020, SIT-VG023 |
| SIT-DH010 | Private new destination and no overwrite | SIT-TR030; SIT-VG020, SIT-VG021 |
| SIT-DH011 | Complete pair publication; scoped staging cleanup | SIT-TR026, SIT-TR030; SIT-VG017, SIT-VG021 |
| SIT-DH012 | No payload logs, caches or automatic uploads | SIT-TR029, SIT-TR030; SIT-VG020, SIT-VG021 |
| SIT-DH013 | Safe diagnostics and suppressed incidental identifiers | SIT-TR021, SIT-TR030; SIT-VG010, SIT-VG021 |
| SIT-DH014 | Optional whole-file digest with explicit coverage | SIT-TR023, SIT-TR030; SIT-VG012, SIT-VG021 |
| SIT-DH015 | Caller-controlled retention; no secure-erasure claim | SIT-TR030; SIT-VG021 |
| SIT-DH016 | Non-executing, traceable text rendering | SIT-TR026; SIT-VG017, SIT-VG019 |
| SIT-DH017 | Whole-payload limits and portable exact integers | SIT-TR027, SIT-TR031; SIT-VG016, SIT-VG022 |
| SIT-DH018 | Honest resource interruption and no partial absence | SIT-TR021, SIT-TR031; SIT-VG010, SIT-VG022 |
| SIT-DH019 | Synthetic-only sensitive examples and reproducible canaries | SIT-TR030, SIT-TR032; SIT-VG021, SIT-VG024 |
| SIT-DH020 | No source sanction, live correction or automatic contact | SIT-TR029, SIT-TR035; SIT-VG020, SIT-VG026 |

## 10. Acceptance and consumer gates

Threat model §§12-13 supplies W9-01-W9-24, the concrete written cases for these controls. Tests remain future implementation obligations. WU10 must assign their code/test paths to the existing logical owners, choose supported platforms and primitives, and realize the fixed numeric limits without weakening the reporting state machine.

Before release, every output/error/staging surface must be tested with synthetic canaries in names, IDs, excerpts, locators, methods, qualifications, extensions and malformed fields. Some fields are intentionally included in an authorized report; those expected disclosures are explicitly distinguished from forbidden incidental logs or public exposure. Test both ordinary and protected dossiers, race/fault cases, boundary values and cleanup failure. A static document review cannot satisfy those runtime tests.

If the established schema cannot express a necessary permitted limitation, stop and request a scoped contract amendment. Do not invent a privacy-success state, silently suppress a required basis, or implement an undeclared report projection.

The current unit stops after three-document delivery. WU9-C01 and WU9-C02 remain submitted choices until accepted. Work Unit 10 and complete Phase 0 approval are separate actions.
