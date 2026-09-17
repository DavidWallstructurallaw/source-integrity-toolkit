# DEPENDENCY_STRATEGY

## Document control

| Field | Value |
|---|---|
| Project | Source Integrity Toolkit |
| Target release | v0.1 |
| Phase / work unit | Phase 0 / WU10 completion and WU11 re-audit |
| Revision | 0.2 |
| Date | 2026-09-17 |
| Status | Completed specification candidate; final baseline adoption pending |
| Theory Owner | Xiangyu Guo |
| Technical Owner | Unassigned |
| Runtime dependency target | CPython standard library; zero third-party Python runtime packages |
| Cross-project / network / model dependency | None |
| Governing realization | REPOSITORY_ARCHITECTURE.md sections 16-22, SIT-RP-0.1 |
| Historical version | Revision 0.1 at commit 2a19833c53fd9a7b1065f568f470919d79583bfd |
| Implementation / Phase 1 authorization | Not granted |

## 1. Purpose and retained decision

The owner's instruction authorizes completing SIT-D028-SIT-D031 and then performing the WU11 re-audit. The retained dependency decision is a deterministic, local runtime using CPython's standard library and no required third-party Python packages. This document completes that decision's platform-ABI boundary. It does not install packages, introduce a live resolver or implement the proposed adapters.

The complete earlier dependency rationale remains available at the immutable revision 0.1 reference in section 18. The current version retains its standard-library-only, no-model/no-network/no-shared-core decisions and its build/test separation. The additions make the required OS dependencies explicit; Python's standard library does not eliminate dependency on the host kernel and system runtime.

## 2. Runtime target

The Python lower-bound design remains CPython 3.11. A release claims support only for the concrete interpreter/OS combinations that pass its conformance matrix; an open-ended package lower bound is not certification of untested future interpreters.

The admitted dossier, exact scalar representation, compact measuring form J, immutable capture, execution port and report profile are specified in architecture sections 17-19. These are project-owned semantics. A standard JSON decoder's permissive defaults, an external graph algorithm or a library's numeric conversion cannot override them.

Normal execution performs no package installation, dependency lookup, schema download, update check, telemetry or remote model call. In-process auditing performs no filesystem lookup of source locators and no native platform-adapter loading.

## 3. Excluded runtime dependencies

No mandatory or optional v0.1 runtime dependency is selected for HTTP/browser automation, model SDKs, embeddings/vector stores, NetworkX or other graph engines, pandas/dataframes, Pydantic or generic object validators, JSON Schema validators, databases/ORMs, caches, template engines, plugin discovery, telemetry or crash reporting. Recursive Integrity Toolkit and a shared integrity-core package are excluded.

A later integration requires an explicit reviewed change. It cannot be activated by an extension field, environment variable, source text or an installed Python entry point.

## 4. Build and test tools

Setuptools remains the recommended later PEP 517 build backend. Pytest remains the recommended test-only tool. Exact versions, resolved dependency trees and licenses must be checked by the later approved scaffold/release work. Neither belongs to runtime requirements, and neither has been installed for this project in Phase 0.

A formatter, static checker or coverage tool may be proposed under the later phase plan; none is mandatory here. Developer tooling cannot rewrite approved specifications silently. A coverage percentage never substitutes for the 228 named field-test obligations, shared contract tests or canonical case oracles.

## 5. Graph and validation ownership

The project owns eligible typed projections, deterministic finite traversal, scope/polarity/lifecycle checks, documentary qualification and witness meaning. A general graph package would not supply those epistemic rules. The reference implementation therefore uses bounded project-owned data structures and procedures.

Likewise, duplicate decoded keys, explicit unresolved endpoints, closed core fields, protected references, contract versions and the distinction between malformed input and valid disputed evidence remain project-owned validation rules. A future machine-readable schema is a public artifact, not permission to delegate all runtime semantics to a generic validator.

## 6. Determinism and isolation

Completed substantive results depend only on admitted normalized content, the explicit invocation and the actual contract/tool/profile versions. Locale, unordered iteration, an optional developer package, network state or an unavailable external executable cannot alter those results.

SIT-RP-0.1 fixes byte representation and report-local naming. Its monotonic guard is real, so different host speeds can produce different interruption points; the runtime must disclose interruption rather than claim cross-host identical partial reports. Source metadata cannot modify the ledger, input scope, output naming or protocol selection.

## 7. Review gate for a new dependency

Before adopting any new runtime dependency, record its exact package/version range, affected module and Trace responsibilities, need relative to the existing contract, transitive dependencies, actual license/notices, import side effects, I/O/subprocess/plugin exposure, bounded failure behavior, deterministic/offline tests and removal plan.

A proposed dependency must not establish source trust, independence, threat severity or scoring through its defaults. A later optimization must preserve the reference accounting and public result semantics, or receive an approved behavioral change.

## 8. Versions and reproducibility

The later package declares its Python lower bound. Known incompatibilities may justify an upper bound, while support claims remain tied to tested versions. Build/test constraints and resolved CI environments must be reproducible. Parser, ordering, numeric, error-classification or rendering changes caused by upgrades require contract regression review, not an automatic claim of semantic compatibility.

No exact package pin, lockfile or release version is created in this phase.

## 9. Build-time versus runtime networking

Authorized CI setup may retrieve reviewed build/test dependencies. That is distinct from execution of the local auditor and grants no access to sources named in a dossier. The installed runtime neither downloads missing integrations nor discovers schemas, models, registries or rule packs on first use.

## 10. Licensing and distribution

Original engineering repository material follows the owner's approved Apache-2.0 policy, to be applied under the authorized scaffold. Third-party tools and host components retain their own terms. No dependency license is inferred from this project's license.

The six theory papers remain reference works under their recorded CC BY-NC-ND 4.0 notices and are excluded from ordinary packages. User dossiers, identity maps and source excerpts do not become licensed fixture data through processing. Review actual distribution contents and notices before release.

## 11. Phase boundary

A separately approved Phase 1 may create metadata, import-safe placeholders and CI scaffolding. It may declare approved build/test tools. It must not implement parsing, graph analysis, native filesystem security, report rendering or other analytical behavior merely because the module layout names those future files.

## 12. Acceptance requirements

A release must demonstrate zero required third-party Python runtime packages, no runtime source retrieval/model/plugin behavior, preserved graph and validation ownership, isolated developer dependencies, an auditable upgrade gate, no hidden cross-project import and actual license review of included third-party versions.

The present re-audit checks whether those requirements and their concrete realization are specified. It does not substitute for their later executable evidence.

## 13. Existing owner decision

WU10-C02's standard-library runtime direction and minimal build/test strategy were accepted for the final Phase 0 review. That acceptance remains intact. It did not certify a native implementation that does not yet exist.

## 14. Profile consistency

The only current realization names are SIT-RP-0.1 and its measuring/serialization form J. References to architecture sections 17-20 and cases W11-R01-W11-R32 identify the completed candidate. No alternate CM1, JR1 or MR1 protocol is selected.

Architecture owns normalization, witness selection and results; this document owns dependency and native-capability restrictions. The WU11 precision supplement in GOVERNANCE_AND_HANDOFF.md section 22 closes representation and failure-classification details without adding an analytical field or source judgment.

## 15. Fixed native capability profile

The selected file profiles remain the 64-bit Linux/glibc and 64-bit Windows 11/local-NTFS designs in architecture section 20. No third-party Python package is added. The standard-library ctypes bridge is allowed only in the fixed platform adapters. Package import and audit_bundle must not initialize these bindings.

| Surface | Permitted mechanism | Required boundary |
|---|---|---|
| Linux path traversal | os descriptor-relative opens, fstat/stat with no-follow checks, close-on-exec handles | One component at a time, retained parent handles, supported ownership/permission assumptions; no source locator access |
| Linux report publication | Fixed renameat2 symbol from the already loaded trusted C runtime, RENAME_NOREPLACE | No replacing rename, shell, subprocess, generic library discovery or copy fallback |
| Windows path/creation | Fixed NtCreateFile, RootDirectory-relative component names, FILE_OPEN/FILE_CREATE and reparse inspection | Local selected volume, checked handle identities, explicit sharing and private creation descriptors |
| Windows permissions | Fixed process-token/SID, security descriptor and GetSecurityInfo operations | Protected private DACL at creation; reject unsupported security/impersonation conditions |
| Windows publication | SetFileInformationByHandle with FileRenameInfo and ReplaceIfExists false | Complete same-volume staging directory, retained parent handle, no replacement fallback |
| Both platforms | Fixed read/write/flush/close and safe removal of tracked staging objects | Input read-only; no recursive deletion of unknown paths; no rollback after observed commit |

On Linux, before the existing architecture section 20.2 data-open step, inspect the leaf with no-follow stat relative to the pinned parent and reject a known nonregular object. After opening, still require a matching regular descriptor identity. This preliminary rejection prevents intentional device/FIFO input from being treated as an ordinary file-open candidate. It is not substituted for the no-follow descriptor and post-open checks. The supported ownership/quiescence assumptions bound replacement by untrusted writers; no stronger same-principal or hostile-kernel protection is claimed.

Native entry points are fixed in project source, never selected by data or options. Linux loads the process's already loaded C runtime with CDLL(None); it does not call find_library or invoke a linker/shell. Windows loads only ntdll.dll, kernel32.dll and advapi32.dll under the system-directory loader policy. Missing symbols, unsupported flags/volumes and failed protections produce the existing safe execution failure, never auto-installation or weaker publication.

## 16. Native binding and source-admission constraints

The Windows allowlist is limited to NtCreateFile; handle read/write/flush/close, type/attribute/volume identity queries; SetFileInformationByHandle; process/thread token queries used to establish the invoking principal and refuse unsupported impersonation; SID/security-descriptor conversion and inspection; GetSecurityInfo; and corresponding native allocation-release operations. Fixed APIs implementing safe cleanup of the two owned files/stage are permitted only with the same identity checks. No callback, arbitrary symbol lookup or foreign user pointer is accepted.

Each ABI declaration must have an exact prototype, checked lengths, pointer-width/alignment tests, checked native status, and explicit handle/memory ownership before a supported build is released. FFI can create memory-safety defects; using ctypes supplies no automatic security assurance. The future tests must exercise errors and races on each claimed platform.

The preflight and exact scalar hooks in architecture section 17 are mandatory even when using Python json. A standard-library module is not authority to accept NaN, discard duplicate keys, coerce an untrusted object or silently round a decimal. The 128-character numeric-token ceiling is a resource-scanning guard: exceeding it interrupts with resource_limit_reached. Integral magnitude and field-type violations remain structural failures. This classification also applies when an in-process float's exact emitted token exceeds the ceiling, completing the word 'reject' used informally in architecture section 17.2.

## 17. Official technical basis

Primary references were checked for the named facilities during this remediation. The composition is a proposed toolkit design; native and runtime tests remain future work. Full reference locators and narrow uses are retained as W11-REF01-W11-REF14 in architecture section 22.

The basis includes Python's json parsing hooks and untrusted-input warning, exact decimal/float conversion, os descriptor operations and ctypes loader/prototype behavior; the Linux open(2) and rename(2) interfaces; Microsoft's NtCreateFile, FILE_RENAME_INFO, SetFileInformationByHandle, security-descriptor/GetSecurityInfo and flushing documentation; and CommonMark fenced-code semantics.

No source code, external library, standards extract, font, paper PDF or real private fixture is copied into this project by recording those references. Native system-library dependencies remain explicit rather than being described as Python package dependencies.

## 18. History, review and next gate

The unabridged revision 0.1 is preserved at:

`https://github.com/DavidWallstructurallaw/source-integrity-toolkit/blob/2a19833c53fd9a7b1065f568f470919d79583bfd/DEPENDENCY_STRATEGY.md`

This current version consolidates that policy and supplies the previously missing native dependency profile. Original analytical owners, limits, license selection and cross-project exclusions are unchanged. It is the dependency input to the requested WU11 re-audit, not a request to postpone that re-audit.

The re-audit disposition is recorded in GOVERNANCE_AND_HANDOFF.md and UNRESOLVED_DECISIONS.md. Final owner adoption of the complete Phase 0 candidate remains required before PHASE_0_APPROVAL.md or a separately authorized Phase 1 plan is created.
