# PHASE_2_PROGRESS

## Document control

| Field | Value |
|---|---|
| Revision | 0.9 |
| Work unit | P2-W04 with approved P2-W04-R01 |
| Owner instruction | 批准 P2-W04-R01 继续已经授权的 W04 解码与快照捕获工作 |
| Approved plan | PHASE_2_PLAN.md revision 0.1, sections 3, 6 and 10 |
| Plan SHA-256 | bea21992edf58b77cfe0f9a128bb31cee9226a9ea5e87b829663a47768227918 |
| Accepted W03 merge | e292bf6023a59d3019221a768d9f2d4ac5c4d4cf |
| Accepted entry tree | ad16a08dc2382b3d007038c4861d010f52a15e4b |
| W04 intake record | 9333c4e8868bdd1209cb773904b1d2603f5b152f |
| Branch | phase2/p2-w04 |
| Status | Local component candidate passed; full exact-head hosted verification pending |
| W04 acceptance / W05 execution | Not granted |

## 1. Authority and preserved history

PR #12 accepted W03 and merged its exact reviewed tree. The current instruction expressly approves the four additional paths proposed in progress revision 0.8 and continues W04 only. That unabridged intake finding remains at 9333c4e8868bdd1209cb773904b1d2603f5b152f. The complete W03 record, initial annotation failure, correction, final 537-test four-row pass and 428 separate subtest events remain at 4189edc62a9c321dd6eed71c5106cea7311907e6 and PR #12. No historical test or source outcome is rewritten.

The attached theory papers do not change the frozen engineering baseline or this work-unit scope. No paper text, PDF, new metric or theory amendment is imported.

## 2. Exact repair and implementation scope

P2-W04-R01 adds only container_cycle to the closed private qualifier vocabulary and one fixed REPOSITORY_ARCHITECTURE section 17.1 diagnostic basis. Public input_constraint_violation, stop states, payload-free messages and null locations remain unchanged. runtime/resources.py is untouched. Missing and unknown qualifiers still fail closed.

The CI driver recognizes exactly the four approved R01 paths as W04 immediate permissions. Earlier/later units receive no new immediate permissions; cumulative accounting retains the actual approved deltas. Exactly the two existing immediate/cumulative permission regression bodies in test_bundle_contract.py are refined. Their identities and every other body, including the original observer-preservation check, remain unchanged. New tests independently check these boundaries and the exact constant-only product repair against pinned entry blobs.

The complete candidate uses fifteen paths within the twelve original allowed paths plus four approved exception paths. tests/contract/test_normalization_profile.py is not changed; its existing scalar tests remain cumulative. Seven product modules change. Eleven slots are cumulatively promoted; thirty-seven installed modules retain Phase 1 bytes. No schema, field map, frozen specification/plan, public API/CLI/export, existing safety observer, dependency, workflow, package configuration, boundary checker, fixture, catalog or analytical expectation changes.

## 3. Bounded capture implementation

The private _prepare_value and _prepare_utf8 seams create their own fixed W03 budget and input ledger. They currently return only _CapturedBundle or a fixed safe diagnostic. _CapturedBundle retains exactly tree and source_mode and has no accepted/pass field. Whole preparation, PC01, global structure/reference/time checks and scope planning remain W05. Public audit entry points are unchanged refusals.

The bytes path accepts exact immutable bytes only. It checks actual raw size before strict UTF-8 decoding. A separately charged finite grammar/lexical preflight checks the complete input, depth, value nodes, decoded string/key length, escape/surrogate correctness, number-token length and exact scalar range before full JSON tree construction. No valid prefix can suppress an invalid suffix. The bounded decoder pass is prepaid independently. All numeric and duplicate-key hooks are project-owned; duplicate comparison occurs after escape decoding. Nonstandard JSON constants, BOMs, malformed UTF-8, lone surrogates and unsafe exact numbers are not silently repaired. No paths, streams or callbacks are accepted.

Caller capture uses an explicit depth-bounded frame stack and active-container identity set. Exact types are checked before custom operations. Each non-cyclic alias is copied and counted as another occurrence. Active-ancestor cycles use the approved cycle qualifier. The original mutable containers are not retained in the immutable tree. Object keys sort by the existing charged scalar ordering; arrays keep their supplied order. Missing keys, explicit nulls, empty collections, booleans, numeric source categories and source-native states remain distinct.

Observable size/iterator inconsistencies become safe execution failures. The caller must keep the reachable graph quiescent; arbitrary same-size concurrent mutation, hostile same-process mutation and debugger access are not claimed detectable or isolated. This is bounded ordinary execution, not a hard real-time or resident-memory guarantee.

J size is accumulated without constructing a complete JSON serialization for caller values. Supplied-byte size remains its raw byte count. Decoded strings and escaped J size remain separate. Repeated passes charge work but do not double-count one raw payload's value nodes. A prospective child-count lower bound rejects impossible wide caller containers before expansion. All generic nested content, including extensions and currently unselected records, is visited. Typed collection/reference-occurrence integration and field-role-specific validation remain explicit W05 obligations; their existing ledger primitives are not presented as completed capture-time semantic validation.

No graph-relationship cycle analysis, evidence interpretation, identity merge, report, score, native loading, source I/O, model call or persistent cache is introduced. All 228 domain-analysis obligations and analytical Trace closures remain pending.

## 4. Actual local evidence and facility basis

Local reconstruction of the required accepted source files was checked against their Git blob identities before editing. Full local Git clone still failed DNS resolution; this workspace is partial and lacks the historical Git database. The actual package/entry/frozen checks must therefore run in GitHub Actions, not be inferred from these local results.

On CPython 3.13.5 with pytest 9.0.2, all 178 selected new component instances passed. Nine additional Git-dependent R01 scope/preservation tests were explicitly not run locally; the hosted suite must collect and execute them, along with every one of the 537 predecessor identities. No hosted skip or deselection is permitted. New tests include exact-byte/scalar pairs, duplicate escaped keys, suffix errors, surrogate pairs, raw-size/depth/string limits, alias expansion, mutation faults, cancellation, real deadline checks, safe canaries and isolated source-I/O/network/native probes. Existing normalization tests are unchanged.

Two local authoring-test issues were corrected before remote delivery: pytest attempted to stringify a huge integer for a parameter ID, now given an explicit fixed ID; the new isolated DNS counterexample required encodings.idna to be loaded before observation, now explicitly preloaded. No product rule, existing test or safety hook was weakened. The first executed component run had 177 passes and one DNS-probe failure; the corrected run passed all 178. Local collection/failure logs remain retained.

Primary facility references checked for the implementation were Python 3.11 json documentation (numeric/object-pairs hooks, permissive defaults and the untrusted-input warning) and built-in types documentation (strict decoding and dictionary-view mutation limits): https://docs.python.org/3.11/library/json.html and https://docs.python.org/3.11/library/stdtypes.html. These explain available facilities; the frozen project specifications determine admission semantics, numerical spelling, limits and errors.

## 5. Hosted acceptance gate and stop

The exact candidate must pass all four original Linux/Windows and Python 3.11/3.13 profiles with the original reviewed dependencies. Inspect complete artifacts, exact-head metadata, raw collection/JUnit identities, all 537 predecessor tests, entry archives, immediate/cumulative scope, twenty frozen files, forty-eight modules, unchanged tracked bytes, packaging and clean installation. Do not substitute expected test counts or an older code-head run for final evidence.

Keep the W04 PR draft until these checks are complete. Owner acceptance and merge remain separate. W05 is not authorized. No release or public successful audit may be inferred from this capture candidate.
