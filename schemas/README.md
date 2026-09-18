# Schema reservations and static contract indexes

Copyright 2026 Xiangyu Guo. SPDX-License-Identifier: Apache-2.0.

P1-W03 reserves the adopted logical contracts `sit-bundle/0.1` and
`sit-report/0.1`. Executable schemas are not delivered in Phase 1.
There is no permissive empty schema, validation service or operational audit here.

The governing files remain the frozen specifications identified by
[PHASE_0_APPROVAL.md](../PHASE_0_APPROVAL.md), as corrected in revision 1.1.
The approval controls historical proposal headers. This directory does not
redefine record kinds, field names, qualification rules, native states or limits.

## Read the indexes

[Module manifest](../scaffold/module_manifest.json) records the 48 existing
package slots, their owner labels, layer constraints and future test homes.
[Trace catalog](../scaffold/trace_catalog.json) binds the 35 Trace IDs and 19
logical owners to the 15 analytical families and 57 registered output fields.
[Obligation catalog](../scaffold/obligation_catalog.json) indexes all 228 P/N/M/B
field-test obligations, 26 shared families, and the existing control references.

Each `*_columns` array names the columns of the associated row arrays. Source
line numbers are one-based in the frozen UTF-8 Markdown file. Field expectations
use the original validation-table cell, numbered from zero; P, N, M and B select
cells 1, 2, 3 and 4. A pointer includes the whole referenced condition and its
surrounding contract. It is not permission to use only a title or a numerical
example. Full source-file identities accompany the references. References must
be reopened under change control if the baseline is amended.

For example, `SIT-VF017-P` points to the original HHI positive obligation in
`VALIDATION_PLAN.md` section 12.5. Its negative, missing-data and boundary cells
remain independently indexed. The index computes no HHI and supplies no result
to the package. Source qualification, the complete population gate and exact
fractions remain in the original specifications.

The catalog status separates **specification adopted**, **scaffold catalog/slot
present**, and **behavior implementation/tests pending**. The last two behavior
statuses remain pending for every analytical and native-runtime obligation.
Passing an index test never means that the corresponding audit behavior passed.
No blank passing domain test or blanket skip/xfail suite is created.

The executable W03 tests inspect these static indexes and their source references
only. They use Python's standard-library `unittest` and can also be collected by
the already selected pytest runner. No new dependency or change to the selected
setuptools/pytest pins is required. In a repository checkout:

```text
python -m unittest discover -s tests/scaffold -p test_contract_catalogs.py -v
python -m unittest discover -s tests/scaffold -p test_module_manifest.py -v
```

W9 and W11 references retain their native names and exact document sections.
Architecture section 16 supplies the later presentation-owner refinement;
governance section 22 supplies the binding WU11 precision resolutions. A W9
family without an adopted file-specific test path stays mapped to its existing
shared/logical owner. The index does not invent a path or mark that work complete.

These JSON catalogs are developer artifacts. They are not JSON Schema documents,
plugin registries, evidence dossiers, runtime configuration, or generated reports.
The installed package never reads them. Existing packaging selection is unchanged.

## Reserved contracts

[Bundle reservation](bundle/README.md) identifies input authorities.
[Report reservation](report/README.md) identifies output authorities.
Actual schema implementation requires its own later approved phase.
