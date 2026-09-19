# PHASE_2_PROGRESS

## Document control

| Field | Value |
|---|---|
| Revision | 0.6 |
| Work unit | P2-W03 |
| Owner instruction | 批准并合并 PR #11，再进入 P2-W03 |
| Approved plan | PHASE_2_PLAN.md revision 0.1, section 9 |
| Plan SHA-256 | bea21992edf58b77cfe0f9a128bb31cee9226a9ea5e87b829663a47768227918 |
| Accepted W02 merge | d3e314c9da12ad886b09885bbc9b71166c24d10b |
| Entry tree | d30f18a6f55cbe8aedebfb3b83e96ef8eae2ae8c |
| Branch | phase2/p2-w03 |
| Status | Candidate; exact-head cumulative verification pending |
| W03 acceptance / W04 execution | Not granted |

## 1. Accepted predecessor and preserved history

PR #11 was merged with expected-head protection at the owner's instruction after checking that its reviewed head d6f6a42663f5857e99f90cec3fd88e923cd28790 remained unchanged and its cumulative runs 35414897827 and 35415022956 succeeded. The merge tree is identical to the reviewed tree and contains one SIT-Phase-Unit: P2-W02 footer. This records W02 acceptance and W03 execution authority only.

The unabridged preceding progress revision 0.5 and implementation evidence remain at d6f6a42663f5857e99f90cec3fd88e923cd28790. That delivery preserves its initial failures, R01 repair and final 374-instance four-row pass. No original approval, source, failure record or golden expectation is rewritten. The six attached papers do not replace the frozen engineering baseline or expand this work unit.

## 2. Exact scope

This candidate changes only the eleven paths in plan section 9. Five product modules change: contracts/bundle.py, contracts/execution.py, validation/limits.py, runtime/resources.py and runtime/diagnostics.py. The three new W03 slots raise the cumulative promotion count from five to eight. Forty installed modules still retain Phase 1 bytes; the other three W02-only contract modules remain unchanged. All 48 package paths, public API/CLI refusals, frozen sources/plans, original catalogs/fixtures/oracles, schema, existing tests, dependency pins, packaging files, live workflow and both boundary checkers remain unchanged.

No extra-path exception is requested. W02-R01's approved cumulative exception remains as implemented; it grants no additional W03 direct write authority.

## 3. Implemented private components and exact boundaries

The zero-argument runtime factory uses the fixed monotonic_ns clock, a 10,000,000-unit total and a single prepaid 1,024-unit reserve inside it. The ordinary balance begins at 9,998,976. Charges cannot be negative or Boolean, the sixty-second deadline never resets, equality is admitted, and the first established stop remains sticky. Tests control clocks by patching the fixed symbol outside the product. Source values, public options and environment variables do not select limits, clocks or cancellation callbacks.

The charge/check port remains in contracts; runtime owns clock and ledger implementation. execution no longer imports bundle solely for its private invariant helper, preventing a cycle when bundle consumes the port. Existing value and stop fields are preserved. A trusted future boundary may record actual input acceptance only after W05's full work; calling this state recorder in a transport test does not implement validation or PC01.

The input ledger supplies whole-payload count/depth primitives for L01-L08 and fixed string/locator/identifier length helpers. Raw supplied byte length and constructed-value J length remain separate transport meanings. Repeated occurrences consume repeated counts; no counter refund exists. W04/W05 must still integrate these guards into all capture, extension and reference paths. Analytical per-scope work, witnesses and report-output budgets are recorded but remain unimplemented and unvalidated.

Exact scalar conversion preserves source numeric category, normalizes coefficient/sign/exponent without rounding and compares integral magnitude before exponent expansion. A raw numeric token longer than 128 characters, or a built-in float whose exact emitted token is too long, interrupts through WU9-L09. Prohibited integral values and field/scalar errors remain structural. Huge negative exponents stay compact; a zero with a huge exponent remains zero. The sole bounded power calculation converts a finite binary float's denominator, capped at 1074 binary places; raw exponent values never become a power or an exponent-sized allocation.

J scalar bytes and decoded UTF-8 lengths are separate. Controls use the frozen escape ranges, ordinary multilingual text is preserved, slash is not escaped, and no Unicode normalization occurs. There is no complete dossier/report serializer. Stable bottom-up pair sorting and binary lookup are charged internal index primitives; they do not deduplicate records, discover ancestry, or interpret text. Constructors/index consumers retain explicit bounded-project-owned-input preconditions.

Safe private stops distinguish structural rejection, resource interruption, actual failure and cancellation. Diagnostics accept only known typed stops and fixed rule identifiers, with null locations and constant, bounded messages. Specific input_constraint_violation cases retain a fixed normative condition reference. The emergency path delivers at most one small record from its prepaid reserve; it never resumes work or returns a partial snapshot. These transports are not sit-report/0.1 envelopes or new public reason states.

## 4. Source and implementation evidence

The controlling requirements were re-read from the accepted repository: plan sections 3.1-3.2 and 9; privacy section 8; architecture sections 17 and 19; governance sections 22.1 and 22.3; dependency section 16. No new scalar limits, analytical formulas, source classifications or permissions are introduced.

Primary Python documentation was checked for monotonic_ns and finite float integer-ratio facilities: https://docs.python.org/3.11/library/time.html and https://docs.python.org/3.11/library/stdtypes.html. These are implementation-facility references only. The project sources determine numeric spelling, guard categories, resource arithmetic and acceptance meanings.

New local tests: 163 passed on CPython 3.13.5 / pytest 9.0.2 in a partial workspace. They include exact scalar examples, independent Decimal/Fraction oracles and 180 fixed-seed finite numeric cases; hostile subclasses; giant exponents and exact float tails; control/multibyte byte accounting; each applicable counter threshold; nonresetting reserve/deadline behavior; before/after component-action interruption; independent cancellation; stable sorting and charged lookup; and canaries across fixed diagnostic surfaces. Loop iterations are not additional top-level tests. No old test or source expectation was changed.

The first complete new-test run passed. Full local Git clone failed because github.com did not resolve. The local run is not a selected-toolchain or complete-repository verification. Hosted CI must check the actual entry archives, all 374 predecessor test identities, all new instances, exact file scope, original pins, full matrix, package contents, clean installation and unchanged checkout bytes before readiness is claimed.

## 5. Stop

Keep the W03 review unmerged until its exact final-head matrix and full artifacts have been inspected and the owner accepts the delivery. No W04 capture, W05 acceptance, observability execution, graph analysis, report generation, native I/O, network/model runtime or release is enabled. All analytical Trace closures and 228 domain obligations remain pending.
