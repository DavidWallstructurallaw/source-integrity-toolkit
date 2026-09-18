# Integration test reservation

Phase 1 / P1-W05. Original engineering material: Apache-2.0.

No operational integration suite is implemented here. The installed audit API
still refuses immediately and produces no `sit-report/0.1` result. Later tests
must use the adopted input, reporting and native-boundary contracts, the fixed
H7 fixtures and the separate logical oracles. Static fixture checks do not
satisfy end-to-end analytical obligations.

The present repository-level checks are:

```text
python tools/check_phase0_baseline.py
python tools/check_scaffold_boundary.py
python -m unittest discover -s tests/security -p "test_scaffold*.py" -v
```

Use a complete, trusted, quiescent checkout for the first command. It checks all
18 specification files, the corrected approval and the Phase 1 plan against the
independently pinned W01 manifest. An incomplete local view must fail; no fetch,
repair, rehash-and-accept or partial-pass switch exists.

The security subprocesses preload test-harness standard libraries, then monitor
application-originated effects while importing all 48 byte-matched module slots
and exercising refusal/help/version. Test-harness setup and Python module
loading are separated from source access. This finite observation is not a
production sandbox, native filesystem validation or general security proof.

P1-W06 owns full-checkout CI and the platform/interpreter matrix. Its runs must
identify actual commits and must not reuse earlier W02/W04 evidence as new guard
execution. Future integration behavior remains pending.
