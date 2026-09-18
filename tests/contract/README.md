# Contract test reservation

Phase 1 / P1-W05. Original engineering material: Apache-2.0.

The adopted logical contracts are `sit-bundle/0.1` and `sit-report/0.1` with the
SIT-RP-0.1 realization and binding WU11 refinements. Executable schemas,
normalization, qualification, serialization and native publication are absent.
Their reserved test homes remain the paths in the frozen architecture and the
W03 catalogs, not completed tests.

The current developer tests can be run independently without installing pytest:

```text
python -m unittest discover -s tests/scaffold -p test_baseline_integrity.py -v
python -m unittest discover -s tests/scaffold -p test_no_runtime_implementation.py -v
python -m unittest discover -s tests/scaffold -p test_layer_boundaries.py -v
python -m unittest discover -s tests/security -p "test_scaffold*.py" -v
```

These are repository checks, not an alternative input validator or public API.
The software-import graph is used only to detect forbidden module dependencies;
it never evaluates claim/evidence ancestry. Layer permission alone does not
authorize runtime behavior: the separate strict AST guard still rejects code in
an inert slot, including dormant imports and annotation/default side effects.

Same-repository source/manifest edits cannot authorize themselves. Actual changes
to a frozen specification, package body or accepted catalog require the existing
scoped owner-approval process. A full-checkout baseline run and later CI retain
their own execution evidence, separate from synthetic guard-unit controls.
