# PHASE_2_PROGRESS

## Document control

| Field | Value |
|---|---|
| Revision | 0.4 |
| Work unit | P2-W02 |
| Owner instruction | 批准并合并 PR #10，再开始 P2-W02 |
| Approved plan | PHASE_2_PLAN.md revision 0.1 |
| Plan SHA-256 | bea21992edf58b77cfe0f9a128bb31cee9226a9ea5e87b829663a47768227918 |
| Accepted W01 / PR #10 merge | 41e7ba2f8046b3791f860313ea3ad54dcd4cb25c |
| Intake tree | ac8bb232d929d18fc56fc053be1b37fb354957ce |
| Branch / review | phase2/p2-w02; draft PR #11 |
| Tested candidate | ff6c1eb401590454069e23bcdacaa7d4d627d2df |
| Status | BLOCKED: seven cumulative security-test failures; W02 component tests pass |
| W02 acceptance / merge | Not granted |
| W03 and later | Not started |

## 1. Acceptance and retained history

The owner accepted W01 and authorized W02 only. PR #10 was merged with expected-head protection after rechecking its exact 8e3af5e5b5f4ca9879add9bdd934603e307e6abf head, sixteen-path diff and successful cumulative runs. The merge tree equals that reviewed tree. Its single SIT-Phase-Unit: P2-W01 footer preserves the post-merge CI context.

Unabridged W01 progress revision 0.2 remains at 8e3af5e5b5f4ca9879add9bdd934603e307e6abf. W02 candidate progress revision 0.3 remains at f7a1f9f69351951162142d4bf41a554de89dcb53, including local source verification, design details, initial local failure and fixes. This current record supersedes only their present-status statements. No history is rewritten.

The original plan, frozen specifications, source versions and Phase 1 records remain unchanged. The six paper attachments do not replace a frozen source or authorize a theory, schema, metric or product-scope change.

## 2. Candidate scope

Exactly fifteen plan-section-8 paths change. Five existing contract modules gain private immutable representations, exact number-atom declarations, closed vocabulary/field tables and safe preparation/cancellation/observability declarations. Forty-three installed modules retain their accepted bytes, including public API/CLI refusal, all graph/analysis/rendering code and native file/output adapters. No new installed module or dependency is added. Version remains 0.1.0.dev0.

Fifty shape declarations and 242 named fields cover Inquiry, twelve record kinds, twenty-four predicates, nine assessment kinds and shared support structures. An immutable _Object field bag tagged by _Node preserves explicit null, absent fields and supplied attribution. Local constructor invariants require bounded project-owned parts. They do not parse input, validate all required source fields or establish accepted input.

The Draft 2020-12 input structural aid has local references, closed keys, exact vocabularies and explicit nullable/subtype branches. The coverage record connects each field to its complete frozen-source section/range, representation, schema pointer, validator owner and four-way declaration tests. Thirty mandatory parser/global/semantic duties remain pending. No general schema evaluator or dependency is introduced; no metaschema or complete-instance conformance is claimed.

Number conversion, rounding, J measurement, quotas, bounded decoding/capture, global validation and observability execution remain later work. All whole prerequisite completions and analytical Trace closures remain empty. The 228 domain behavior obligations stay pending.

## 3. Local evidence and transmission repair

The full 129967-byte lineage source was checked against Git blob a08e94bee1e4c8aaa4a47fcdd79b1e8db0fe6911 and SHA-256 32272903b45a8749115ed6b4ec9904dd864a2190f9e1a2ba43ced4c8256c0374. Primary JSON Schema and dataclass documentation supplies format/representation facilities only; adopted project sources supply field meaning.

Local new-component tests used a partial workspace, CPython 3.13.5 and pytest 9.0.2: 146 passed. An initial run had 144 passes and one overly broad no-maxItems assertion failure. The corrected check permits only adopted exact one/two-subject cardinalities, retaining the resource-category restriction. A source review corrected RelationData.dimension's structural-null coverage and added an independent nullable-field check. Exact-type comparisons were hardened against hostile metaclass hooks. Full local clone failed DNS resolution; no full local checkout or selected-toolchain pass is claimed.

Initial hosted run 35411043925 on f7a1f9f69351951162142d4bf41a554de89dcb53 stopped at all four preflights on invalid_phase_policy. The transmitted policy lacked its final object brace although the local file retained it. Commit ff6c1eb401590454069e23bcdacaa7d4d627d2df restored only that missing brace/newline, matching local blob ed143a9933c76b3b7864ab261e8248d717b87f6d. This was an authoring/transmission error. No guard or expectation was relaxed. That first run executed no tests; its skipped downstream stages are not passes.

## 4. Actual cumulative verification

Run 35411233144 executed ff6c1eb401590454069e23bcdacaa7d4d627d2df with the original reviewed toolchain and unchanged workflow:

| Profile | Actual Python | Passed | Failed | Errors | Skipped |
|---|---|---:|---:|---:|---:|
| Ubuntu 24.04 | 3.11.16 | 360 | 7 | 0 | 0 |
| Ubuntu 24.04 | 3.13.15 | 360 | 7 | 0 | 0 |
| Windows Server 2025 | 3.11.9 | 360 | 7 | 0 | 0 |
| Windows Server 2025 | 3.13.15 | 360 | 7 | 0 | 0 |

Each row has 367 top-level identities: 221 retained W01 instances plus 146 new W02 instances. All 146 new instances pass. Raw JUnit contains 795 events, including 428 separately counted successful subtest events. The same seven old security-test identities fail on every row. No test was skipped, xfailed, removed, renamed or deselected.

All eight complete artifacts across both runs were downloaded, size/SHA-256 checked and inspected. Cumulative artifact IDs are 10574092984 (Ubuntu 3.11), 10574397741 (Ubuntu 3.13), 10574637551 (Windows 3.11) and 10573592532 (Windows 3.13). Collection identities agree with raw JUnit. All fifteen authored file hashes match the tested checkout. All 137 tracked hashes match across rows and remain unchanged during execution.

Actual 124-file Phase 1 and 125-file entry archive checks, fifteen-path scope checks, twenty-file freeze guards and forty-eight-module guards pass before and after. Selected dependency review/install passes. All package tests pass: 65 regular source members, 55 wheel members, clean offline installation and equal original/rebuilt wheel member bytes. These separate successes do not clear the seven failures.

## 5. Shared failure and diagnostic limit

The existing shared security harness reports application_open after 21 module imports, before API refusals. It preloads several standard-library helpers before its observer but omits dataclasses. W02's bundle module imports dataclasses; the observer sees an application frame and permits only package-module loader reads, so it blocks the standard-library loader. This early stop also prevents some deliberately bad API/network/native probes from reaching the specific event each assertion requires.

A local isolated diagnostic using the same preamble and application-open predicate against the actual W02 bundle module identified dataclasses.cpython-313.pyc loaded by importlib._bootstrap_external. Preloading dataclasses before that unchanged observer allowed the same module import with no blocked open. This CPython 3.13.5 diagnostic locates the cause; it does not substitute for a repaired four-row run. No repository test was modified for the diagnostic.

## 6. Proposed P2-W02-R01 and stop

The proposed repair remains unapproved. It needs these narrowly scoped changes:

1. tests/security/test_scaffold_inertness.py: preload the specifically permitted dataclasses module before the observer; add an isolated regression; retain all monitored operations, refusal checks, mutation probes and event-specific assertions.
2. tests/scaffold/test_ci_contract.py: enumerate only the W02 exception paths for the harness and this driver repair, and preserve the harness change explicitly in later cumulative path accounting. Keep the frozen plan/pins unchanged and reject unlisted exceptions. Exercise that exception in the already allowed W02 contract-test path.
3. PHASE_2_PROGRESS.md and phase2/implementation_evidence.json: record actual authorization and exact-head results.

Do not generally allow arbitrary library/file reads, disable the observer, skip tests or refactor the product to evade it. No live workflow, boundary-checker implementation, dependency, oracle, product module or frozen document is included in this repair proposal.

The existing harness and CI driver are outside W02's fifteen-path allowlist and remain unchanged. PR #11 stays draft; main remains at 41e7ba2f8046b3791f860313ea3ad54dcd4cb25c. W02 is incomplete and W03 has not started. This documentation successor records the actual tested candidate; it does not claim a green final-head workflow, publish a package or authorize the proposed repair.
