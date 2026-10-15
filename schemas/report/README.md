# sit-report/0.1 structural contract

Copyright 2026 Xiangyu Guo. SPDX-License-Identifier: Apache-2.0.

Status: structural schema delivered for P4-W02; public audit execution remains unavailable.

[sit-report-0.1.schema.json](sit-report-0.1.schema.json) declares the closed logical
report structure for the accepted SIT-RP-0.1 reference profile. It does not construct
a report, run analysis, authorize disclosure, encode either format, or activate a
public audit function. A type or schema existing does not establish a completed audit.

## Authority and limits

The controlling sources remain:

- [OBSERVABILITY_AND_REPORTING.md](../../OBSERVABILITY_AND_REPORTING.md) §§12-19:
  six run/input combinations, six Result state pairings, 16 root members, nested
  objects, seven value kinds, 57 field bindings, 40 Reason codes, 24 prerequisites,
  five domains and 22 finding conditions.
- [REPOSITORY_ARCHITECTURE.md](../../REPOSITORY_ARCHITECTURE.md) §§17-18 and
  [GOVERNANCE_AND_HANDOFF.md](../../GOVERNANCE_AND_HANDOFF.md) §22: exact scalars,
  typed local identities, ordered witnesses, fixed clock metadata and no JSON
  `display_decimal`.
- [CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md](../../CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md)
  §§3-11: native source shapes, time, lifecycle, classifications, role bindings,
  relation details, assessment conclusions, pipeline states and correction outcomes.
- [PRIVACY_AND_DATA_HANDLING.md](../../PRIVACY_AND_DATA_HANDLING.md) §§4, 6-8 and
  [PHASE_4_PLAN.md](../../PHASE_4_PLAN.md) §§4.1-4.4, 6/P4-W02, 7.3: explicit
  disclosure selection, safe diagnostics, exact integers, finite payloads,
  repository-only schema and the current implementation stop.

The historical [Trace catalog](../../scaffold/trace_catalog.json) and
[obligation catalog](../../scaffold/obligation_catalog.json) retain their original
status and source mappings. Their existence does not complete later public report,
native-file, CLI or release obligations.

The declaration uses the same Draft 2020-12 style as the bundle schema. Every
`$ref` resolves inside this file. Fixed objects have `additionalProperties: false`;
source variants and disclosure/witness alternatives have explicit member types.
There is no arbitrary JSON value, extension dictionary, remote reference, default,
executable selector or runtime schema lookup.

Schema validation is structural evidence, not full Draft conformance certification.
JSON Schema's mathematical integer convention does not establish the Python
transport's exact built-in-int requirement. Raw duplicate keys, Unicode scalar
validity, byte counts, source time syntax, operation provenance, global reference
closure, semantic identities, reference partitions, count/member equality, interval
ordering, documentary qualification, disclosure selection, budgets and format parity
require separate direct checks. Schema acceptance does not authenticate input or
certify analysis. This file is development contract material; current package-data
rules do not place it in the wheel, and installed runtime code does not read
repository schema or test files.

## Core representations

The root is `AuditReport`, with exactly reporting §16.1's 16 fields. Diagnostic
envelopes require the eight analytical arrays to be empty; Reasons may remain with
a null scope for an unscoped diagnostic. Audits have five domain entries. Domains
have six fields and no `not_applicable_result_refs`; that state remains in Results
and Capabilities. Requested diagnostic IDs always cover all fifteen families.

`InputRef` is `{collection, identifier, selector}`. Its collection is `inquiries`,
`records`, `assertions` or `evidence_references`; selector is null or a complete
source field/role selector. A selector is not split on dots in embedded input IDs
and never executed. Local references require their own `SIT-...-` prefix and a
positive sequence of at least six digits. Input IDs resembling local IDs retain
their separate typed namespace. A case-target pair uses a record case reference and
a before reference to either a Record or an Assertion, as the native correction
target contract permits.

TimeValue preserves state/value/precision and optional reason. Known time may omit
reason; other states require a nonempty reason and null value/precision. Run times
are the fixed unknown TimeValues with `not_recorded_by_SIT-RP-0.1`. Diagnostic
location is null in this profile, matching existing safe private diagnostics;
source-supplied IDs and exception representations do not become locations.

| Value kind | Public representation |
| --- | --- |
| count | Nonnegative portable integer; unit/membership belong to the referenced Population |
| fraction | `{numerator, denominator}` with the original positive denominator |
| completion_interval | `{lower, upper, interval_kind, population_ref, partition}` |
| partition | `{population_ref, categories, total}`; each category is `{label, member_refs, count}` |
| incidence | `{population_ref, memberships, origin_counts, total, nonexclusive}`; nonexclusive is true; memberships retain member/origin references and origin rows retain members/count |
| record_disclosures | `{records}`; each entry is `{source, fields, qualifications}` with a field-specific closed payload |
| witness_collection | `{witness_refs}` referencing this report's Findings |

Structured correction target members use `{case_ref, before_ref}` only for unit
`case_target`. Counts, totals, membership equality and HHI bucket meaning are
independently checked; the schema does not recompute analysis.

BasisEntry has exactly `id`, `source`, `basis_kind`, `asserter_ref`, `attestor_ref`,
`method`, `support_refs`, `availability`, `scope`, `time`, `lifecycle`,
`qualifications`, `check_refs`. Missing source metadata stays null where declared.
Scope retains inquiry/claim references and effective window. The closed time bag
allows only actual asserted/occurred/observed/published/retrieved/as-of TimeValues
and valid/inquiry time windows; absent source fields are omitted. Lifecycle is null or `{state,
basis_refs}`. Documentary outcomes remain linked Checks, not source-verification
flags. Empty method text remains representable without qualifying its basis.

Run identity is `Source Integrity Toolkit`, version `0.1.0.dev0`, with supported
input contract `sit-bundle/0.1`. Run qualifications and six release-limit statements
are exact tool-owned arrays. Source metadata cannot override them. Source-specific
limitations stay in Scope, Result, Finding, Reason, Basis and disclosure qualifications.

## Selected native fields and disclosure mappings

Private analytical disclosures can contain complete immutable input records. Those
are not public values. Public `fields.native_record` is an explicitly selected
`SelectedNative` fragment. Its closed Inquiry/Record/Assertion/EvidenceReference
branch preserves source layering and native conclusions; family qualification
fields sit beside it. Input records are not mutated.

Every record data, relation detail, assessment detail and correction detail uses an
explicit property allowlist. The schema rejects `extensions`, `excerpt`,
`contact_locator`, `display_name`, `identity_key`, `locator`, `locators`,
`citation_locator`, `external_locator`, `protected_key`, source record labels and
full artifact checksums. Claim text and Artifact work keys are not selected. IDs,
exact family labels, methods, role bindings, pertinent context, original outcomes,
coverage, time, lifecycle, scope notes, attribution and qualifications remain where
the fragment requires them. Allowed strings and topology can still identify people
or material; this is not anonymization or publication approval.

| Field key | Closed fields definition | Existing private owner |
| --- | --- | --- |
| origin_boundary_disclosures | OriginBoundaryFields | analysis/origins.py |
| ancestry_gap_disclosures | AncestryGapFields | analysis/origins.py |
| independence_assessment_disclosures | IndependenceAssessmentFields | analysis/process_comparison.py |
| evaluator_overlap_disclosures | EvaluatorOverlapFields | analysis/evaluator_lineage.py |
| externality_assessment_disclosures | ExternalityAssessmentFields | analysis/presence.py |
| externality_stage_links | ExternalityStageFields | analysis/presence.py |
| pipeline_stage_disclosures | PipelineStageFields | analysis/presence.py |
| cohort_transition_disclosures | CohortTransitionFields | analysis/presence.py |
| correction_route_disclosures | CorrectionRouteFields | analysis/correction_routes.py |
| correction_case_disclosures | CorrectionCaseFields | analysis/correction_outcomes.py |
| correction_target_change_disclosures | CorrectionTargetChangeFields | analysis/correction_outcomes.py |
| reported_capacity_disclosures | ReportedCapacityFields | analysis/correction_outcomes.py |
| corrective_independence_disclosures | CorrectiveIndependenceFields | analysis/human_review.py |
| human_contribution_disclosures | HumanContributionFields | analysis/human_review.py |
| anomaly_context_disclosures | AnomalyContextFields | analysis/context.py |
| contestation_disclosures | ContestationFields | analysis/context.py |
| tail_stage_result_links | TailStageResultLinkFields | analysis/context.py |
| coverage_disclosures | CoverageFields | validation/semantics.py |
| documentary_basis_gap_disclosures | DocumentaryBasisGapFields | validation/semantics.py |

These are explicit representations of the frozen meanings, never recursive
serialization or a permissive replacement for the private tree. Ancestry gaps keep
typed seeds, source gaps, selected frontier records, coverage qualifications and
ordered paths. Tail-stage links use a local Result ID as source and retain its
state/value kind; others use InputRef. A private stage-anchor tuple becomes null or
`{run_key, stage_key, stage}`. Private spreads become `native_record`; required
family qualification groups remain complete, not partly supplied.

## Findings and witness components

A Finding retains exactly reporting §18.1's members; there are no public
`native_records`, `result_refs` or root `witnesses` additions. Its `witness` is
`{input_refs, components}`. Components are the six existing finite owner forms:
`graph_witness`, `inventory_witness`, `comparison_witness`, `selected_members`,
`human_review_witness`, `correction_outcome_witness`. Component `type` selects the
closed shape. Graph components retain path/cycle/member/complete-trace/examined material,
frontiers, terminals and observation edges. Absence is named
`no_witness_in_examined_view`, not a positive empty path.

GraphNode is `{ref, kind}`; its whole-entity reference has a null selector and a
collection matching the node kind, including Inquiry, Assertion and EvidenceReference
nodes as well as the twelve Record kinds. GraphEdge is `{source, target, source_ref, predicate,
eligible, reason_codes}`. Its identity is recoverable from the complete source
selector and target; no private tuple key or `operation_anchor` is serialized.
A non-null predicate identifies a whole Assertion source with null selector. A
canonical link has null predicate and a nonempty selector; its source reference
collection and identifier match the source node. The schema enforces the two
structural forms; the cross-field identity equality has a separate direct check.
Each projected component must retain its actual inquiry/claim/dimension/operation
meaning through the matching public Scope and explicit subject payload. A permitted
component shape alone does not establish a valid Finding home or completed
projection. Conditions cannot be invented to accommodate a private payload.
Source-native ordered arrays and causal path order remain ordered. This
schema does not deduplicate, shorten or select witnesses, or change reserved counts.

Component `member_count` preserves the existing owner occurrence count: inventory
and selected-members use member length; comparison adds examined-assessment
length, with nullable assessment anchor not separately counted; human-review adds
examined-assessment and source-reference lengths; correction-outcome adds
source-reference length. Graph counts all eleven material arrays and a non-null
target. Human-review and correction-outcome source references preserve repeated
slots. These local counts differ from a private Finding wrapper count and from
the shared reservation ledger; neither is recomputed by deduplicating identifiers.

### Existing owner material and public homes

A private reservation is not itself an additional Finding condition. Existing
same-owner Findings retain their complete finite components. When pure member or
selection lists already have a complete public home, the projection keeps those
facts there and preserves ledger accounting separately:

- Inventory member references and count remain in that same Result's Population
  and count. Comparison members remain in Population; its assessment remains in
  Scope and native disclosure, and its examined assessments remain in PC03's
  exact selector inputs and corresponding basis sources.
- Presence selected-members remain in the corresponding transition Result's full
  basis sources. Context selected-members remain in the combined basis sources
  of anomaly and contestation disclosures, without mixing in tail-stage links.
- Graph path, complete-trace, eligibility and ordered search material remains in
  Findings under the actual original scope. A different path Finding's scope
  cannot silently replace the trace's targets or coverage.
- Correction outcomes with cases already have a case-handling Finding carrying
  the complete owner component. With no cases, the owner source-slot list is only
  the Inquiry root; owner members are the Result's full basis source list.

Human-review material has an explicit selection projection into the existing
`corrective_independence_disclosures` field. Its selected members remain in that
scope's Population. After all original disclosure rows, including primary and
support rows, each actually
examined assessment contributes a native-only row in the original scan order,
with its actual AssertionRef as `source`. Each actual owner source-reference slot
then contributes a native-only row in slot order, with its complete InputRef
selector and selected original record fields. Repeated slots remain repeated
rows; no source-ID deduplication or primary-row replacement occurs.

The scan row's `qualifications` is exactly this one-element array:

```json
["Examined assessment only; this scan does not establish applicability or qualification for the selected review scope."]
```

The source-slot row's `qualifications` is exactly this one-element array:

```json
["Actual owner selection/source reference slot; this record does not establish an applicable review or independent process."]
```

These fixed SIT-RP-0.1 markers distinguish the two original owner sequences; they
are not imported qualifications or new analysis. Selected Inquiry fields retain
`target_object_refs`; selected assessment fields retain their original scope,
subjects and dimension. The member count reconciles Population member count plus
scan-row count plus source-slot-row count. This projection neither adds Basis or
Check qualification nor creates a Finding, condition, reason or metric. It is
based on the actual selections in `analysis/human_review.py`, the ordered
reference/selected-field representation in reporting §16.5, finite disclosures in
§17 and the corrective-process meaning in Definitions §25.3. Shape availability
in W02 does not implement the later disclosure projection or ledger integration.

## Current verification boundary

P4-W02 tests cover closed root/nested declarations, normal variants before mutations,
state/family bindings, local references and safe typed contracts. The limited
test-side schema reader rejects unsupported validation keywords; it is not a general
Draft validator. Semantic reference, partition and value checks are separate.
Existing private tests keep their meaning. Public execution, disclosure selection,
ID allocation, budget integration, rendering and installed public receipts remain
assigned to later approved work units.
