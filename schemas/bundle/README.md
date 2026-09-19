# sit-bundle/0.1 input structure

`sit-bundle-0.1.schema.json` is the P2-W02 structural aid, written in JSON
Schema Draft 2020-12. Its source is the frozen
`CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md` sections 2-9, with later adopted precision
and admission rules retained. All references use local `#/$defs/...` fragments.
No generic validator, external resolver or new dependency is delivered.

## What is represented

Closed envelope and data keys; explicit required/optional presence; nullable
unions; Inquiry and twelve record kinds; 24 predicates and their detail shapes;
nine assessment kinds; shared TimeValue, TimeWindow, Gap, Provenance,
EvidenceReference, RoleBinding and explicit unresolved-reference data. Conditions
include time-state value/precision/reason, protected Claim/Anomaly references,
correction submission/handling/change, removal nulls, classification axes,
conflict resolution and explicitly constrained assessment subject counts.

`phase2/input_contract_coverage.json` gives each field's source interval,
immutable representation, schema pointer, runtime owner and four-way test
binding. The internal representation is a schema-tagged `_Node` containing an
immutable `_Object` field bag, with typed immutable arrays and exact number
atoms. Tags and local constructor checks do not constitute field validation.
Optional absence has no pair; a supplied null remains an explicit None value.
No default inserts provenance, an origin, an assessment or a Gap.

## Mandatory remaining layers

The bounded parser must reject duplicate decoded keys, invalid UTF-8/nonfinite
numbers and wrong exact Python types, preserve numeric lexical category and
apply the approved numerical/scanning resource rules. J measurement and number
conversion are W03 work. Snapshot capture/decoding are W04 work.

The complete W05 validator must check global IDs/references and endpoint kinds,
claim/scope consistency, corresponding Gaps, precise calendar/timezone syntax,
lifecycle support, expected unresolved kinds, role specializations and before/
after bindings. Null structural exceptions stay distinct from unknown facts.
Well-formed conflicts, source cycles, denied/unsupported declarations and
unknown ancestry are preserved. A verified label without support is not
rejected merely to make the schema look stricter.

The schema does not use string/array-length constraints to recategorize a
resource interruption as structural rejection. `format` is not used as the
calendar validator. JSON Schema's mathematical number model cannot replace the
source-token and exact-type rules. Native file opening, analysis, documentary
qualification, output schemas and report generation remain absent.

## Evidence and testing

W02 tests verify frozen-source identity, complete declaration/schema field and
branch agreement, immutable local models, preservation and deliberate corrupted
schema/declaration cases. They use no general schema evaluator. No claim of
metaschema validation, all-instance schema conformance, full H7 input acceptance
or executed domain analytics follows. The original H7 bytes/oracles are unchanged.

Primary format references checked for this implementation:
`https://json-schema.org/draft/2020-12/json-schema-core`
`https://json-schema.org/draft/2020-12/json-schema-validation`
`https://docs.python.org/3.11/library/dataclasses.html`

The format vocabulary comes from those primary documents. Field meanings and
phase limits come from the project's adopted specifications. No external text,
model judgment, source download or paper extract defines runtime policy.
