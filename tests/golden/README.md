# Test-only logical expectations

Copyright 2026 Xiangyu Guo. SPDX-License-Identifier: Apache-2.0.

These four `.logical.json` files transcribe expected observations for H7-01 and its three isolated variants. They are not `sit-report/0.1` documents, public output schemas, or output from an executed auditor. Actual domain tests remain pending.

## Meaning of the contents

`selected_field_expectations` pairs exact registered family/field names with the available value or required non-result. Descriptive collections outside this mapping use a test-only organization for the approved witnesses, scopes, populations, stages and corrections. They do not define an alternative public report shape. The exact strings and semantics in the adopted input/report/validation documents continue to control later implementation.

An expected `completed` state describes a future fully performed operation; it does not record a completed test today. `required_reason_codes` is a required subset, not permission to suppress another relevant reason. Where the case states unavailability without fixing the full reason collection, the file preserves that limit rather than inventing a reason. Fields not specifically fixed by the case oracle are not silently assigned zero or an empty result.

Every oracle includes source-section pointers with the complete source-file and section SHA-256. Those sections, including scope and qualification paragraphs outside tables, are mandatory. The pointers prevent a shortened local description from replacing the source. The main case's non-acquisition dimensions remain unestablished where evidence is absent.

| Case | Restricted HHI expectation | Separate conditions preserved |
|---|---|---|
| H7-01 | 26/36, with six contributions and bucket counts five and one | Qualified supplied O1/O2 pair; partial model history; EE use unknown; E amendment undocumented |
| H7-V01 | 25/25 over the five selected contributions | Comparison still has two subjects; pipeline still has six members; four correction targets remain |
| H7-V02 | Unavailable: `unknown_endpoint`, `upstream_coverage_incomplete` | Original six rows qualify via COV-ACQ-OLD; no resolved-subset fallback; unknown contribution remains in N=7 |
| H7-V03 | Unavailable: `multi_origin_unallocated` | Complete origin resolution 7/7; nonexclusive incidences 6/7 and 2/7; no equal split |

Fractions retain their original numerator and denominator. The main 26/36 is not replaced by a lone reduced 13/18 or a rounded decimal. Influence retains the finite-cohort completion interval [3/6,4/6]. V02 retains the separate immediate-layer finite-record completion interval [5/7,6/7]. Neither interval is a probability/confidence statement.

Submission, accepted handling and three linked changes remain distinct. Those three include the original export plus A and D. E's requested effect is unavailable with `change_evidence_missing`. No correction-success rate, global propagation rate, measured temperature truth or source-cleanliness certificate is expected.

The files intentionally omit a produced report ID, tool version, execution time, input digest and exact JSON/Markdown output bytes. Future byte-golden reports must be created through the separately authorized implementation and tested against the adopted SIT-RP-0.1 realization and WU11 precision rules.

Do not import these oracle assets into `src/source_integrity_toolkit/`. A constant stored answer would violate the Phase 1 refusal contract and the later analytical validation discipline.
