# Schema artifacts

The only implemented schema artifact is `bundle/sit-bundle-0.1.schema.json`, the
Draft 2020-12 structural aid for the adopted `sit-bundle/0.1` input contract.
The report directory remains a reservation. No report schema or audit renderer
is delivered in P2-W02.

The input schema uses local fragment references only. Its `$schema` and `$id`
identify the format/document; neither is a runtime fetch instruction. Runtime
modules never load a schema from disk or resolve an external schema URL.

See `bundle/README.md` for the exact scope and mandatory parser/global-validator
layers. Passing a JSON-expressible structure check alone cannot establish
bounded input acceptance, authenticity, independence or completed auditing.
