# Domain unit test reservation

Phase 1 / P1-W05. Original engineering material: Apache-2.0.

The 15 analytical families and 57 public fields retain the definitions, primary
Trace owners and 228 P/N/M/B obligations indexed by `scaffold/trace_catalog.json`
and `scaffold/obligation_catalog.json`. Those domain tests remain pending. This
README creates no empty passing tests or blanket skip/xfail entries.

Current tests under `tests/scaffold` verify developer guard behavior. The freeze
guard has an independently generated synthetic twenty-file positive workspace,
byte/manifest/approval/plan mutation controls, real manifest-anchor validation
and a complete real reference-document byte check. Synthetic files are never
represented as the project's approved specifications. The developer guard CLI
always uses the real pinned manifest and has no test-anchor override.

The package guard separately checks all actual accepted module bytes, closed
AST forms, imports and software-module dependency directions. Its adverse cases
introduce extra source/data/native files, mutable registries, callbacks,
decorators, computed defaults, argument inspection and a fake successful result
only in controlled temporary copies. The actual package remains unchanged.

Later implementation must test real calculations against source-bound logical
oracles. Never import expected results into production as audit answers, change
a frozen oracle to fit a wrong implementation, or equate a scaffold pass count
with analytical evidence.
