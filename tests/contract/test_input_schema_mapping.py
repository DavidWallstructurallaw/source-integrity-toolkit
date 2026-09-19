# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Finite source/declaration/schema checks; no JSON Schema interpreter.

These tests inspect exact schema fragments and source-bound mappings. They do
not claim full input validation or Draft metaschema/conformance certification.
"""
import copy
import hashlib
import json
from pathlib import Path
import re
import pytest
from source_integrity_toolkit.contracts.constants import SHAPES, VOCABULARIES, RECORD_SHAPES, RELATION_SHAPES, ASSESSMENT_SHAPES

ROOT=Path(__file__).resolve().parents[2]
SOURCE="CLAIMS_EVIDENCE_AND_LINEAGE_SPEC.md"
SOURCE_HASH="32272903b45a8749115ed6b4ec9904dd864a2190f9e1a2ba43ced4c8256c0374"
SCHEMA="schemas/bundle/sit-bundle-0.1.schema.json"


def unique(pairs):
    result={}
    for k,v in pairs:
        if k in result: raise ValueError("duplicate_schema_key")
        result[k]=v
    return result


def load(path):
    return json.loads((ROOT/path).read_bytes(),object_pairs_hook=unique)


def reference(name): return {"$ref":"#/$defs/"+name}


def fragment(t):
    # Finite declaration-to-schema comparison, never execution over a dossier.
    if "|" in t: return {"anyOf":[fragment(x) for x in t.split("|")]}
    if t.startswith(("+","*")):
        rest=t[1:]; distinct=rest.startswith("&"); rest=rest.removeprefix("&")
        result={"type":"array","items":fragment(rest)}
        if t[0]=="+":result["minItems"]=1
        if distinct:result["uniqueItems"]=True
        return result
    if t.startswith("@"):return reference("enum_"+t[1:])
    if t.startswith("#"):return reference(t[1:])
    if t.startswith("="):return {"const":t[1:]}
    return {"str":{"type":"string"},"text":{"type":"string","minLength":1},
            "id":reference("Identifier"),"bool":{"type":"boolean"},"null":{"type":"null"},
            "extensions":reference("Extensions")}[t]


def verify_shape(shape,definition):
    name,section,fs=shape
    assert definition["type"]=="object" and definition["additionalProperties"] is False
    assert definition["properties"]=={f:fragment(t) for f,t,r in fs}
    assert definition.get("required",[])==[f for f,t,r in fs if r]


@pytest.mark.parametrize("shape",SHAPES,ids=[s[0] for s in SHAPES])
def test_shape_mapping_positive(shape):
    verify_shape(shape,load(SCHEMA)["$defs"][shape[0]])


def test_shape_mapping_mutations():
    d=load(SCHEMA)["$defs"]
    for shape in SHAPES:
        name,section,fs=shape
        for f,t,r in fs:
            for mode in ("field","type","presence","open"):
                bad=copy.deepcopy(d[name])
                if mode=="field":bad["properties"].pop(f)
                elif mode=="type":
                    bad["properties"][f]=({"type":"string"} if t=="bool" else {"type":"boolean"})
                elif mode=="presence":
                    required=list(bad.get("required",[]))
                    required.remove(f) if r else required.append(f)
                    bad["required"]=required
                else:bad["additionalProperties"]=True
                with pytest.raises(AssertionError):verify_shape(shape,bad)


def test_required_and_optional_presence():
    d=load(SCHEMA)["$defs"]
    for name,section,fs in SHAPES:
        for f,t,required in fs:
            assert (f in d[name].get("required",[])) is required
    assert "reason" not in d["TimeValue"]["required"]
    assert d["TimeValue"]["allOf"][0]["else"]["required"]==["reason"]
    assert "content_evidence_ref" not in d["ClaimData"]["required"]
    assert d["ClaimData"]["allOf"][0]["then"]["required"]==["content_evidence_ref"]


def test_nullable_and_boundary_branches():
    d=load(SCHEMA)["$defs"]
    assert d["CorrectionEventData"]["allOf"][0]["then"]["properties"]["case_ref"]=={"type":"null"}
    assert d["CorrectionEventData"]["allOf"][1]["then"]["properties"]["case_ref"]==reference("Identifier")
    assert d["ChangeDetails"]["allOf"][0]["then"]["properties"]["after_absence_reason"]=={"type":"string","minLength":1}
    assert d["ChangeDetails"]["allOf"][0]["else"]["properties"]["after_absence_reason"]=={"type":"null"}
    assert d["ConflictDetails"]["allOf"][0]["then"]["properties"]["resolution_evaluation_ref"]=={"type":"null"}
    assert d["AnomalyData"]["allOf"][0]["then"]["properties"]["caller_label"]=={"type":"null"}
    assert d["EvidenceReference"]["allOf"][-1]["then"]["properties"]["attestor_ref"]==reference("Identifier")
    structural = {
        ("Bundle", "predecessor"), ("TimeValue", "value"), ("TimeValue", "precision"),
        ("EvidenceReference", "artifact_ref"), ("EvidenceReference", "record_ref"),
        ("EvidenceReference", "locator"), ("EvidenceReference", "excerpt"),
        ("EvidenceReference", "attestor_ref"), ("EvaluationData", "review_contribution"),
        ("CorrectionEventData", "case_ref"), ("ChangeDetails", "after_ref"),
        ("ChangeDetails", "after_absence_reason"), ("AnomalyData", "claim_ref"),
        ("AnomalyData", "context_evidence_ref"), ("AnomalyData", "caller_label"),
        ("RelationData", "dimension"), ("ConflictDetails", "resolution_evaluation_ref"),
    }
    coverage=load("phase2/input_contract_coverage.json")
    for row in coverage["shapes"]:
        for field,t,required,null_rule,owner,case in row["fields"]:
            key=(row["shape"],field)
            expected=("structural_or_conditional" if key in structural else
                      "factual_gap_required") if "|null" in t else "not_nullable"
            assert null_rule==expected, key
            if "|null" in t:
                assert {"type":"null"} in d[row["shape"]]["properties"][field]["anyOf"]


def test_exact_sources_and_closed_kind_predicate_assessment_sets():
    raw=(ROOT/SOURCE).read_bytes()
    assert hashlib.sha256(raw).hexdigest()==SOURCE_HASH
    source=raw.decode()
    record=re.findall(r"^### 6\.\d+[^\n]+: `([^`]+)`",source,re.M)
    predicates=re.findall(r"^\| `([^`]+)` \|",source[source.index("## 8. Relation registry"):source.index("### 8.2")],re.M)
    assessments=re.findall(r"^### 9\.\d+ `([^`]+)`",source,re.M)
    assert tuple(record)==VOCABULARIES["record_kind"] and len(record)==12
    assert tuple(predicates)==VOCABULARIES["predicate"] and len(predicates)==24
    assert tuple(assessments)==VOCABULARIES["assessment_kind"] and len(assessments)==9
    assert set(RECORD_SHAPES)==set(record) and set(RELATION_SHAPES)==set(predicates) and set(ASSESSMENT_SHAPES)==set(assessments)


def test_enum_schema_agreement_and_no_aliases():
    d=load(SCHEMA)["$defs"]
    for name,values in VOCABULARIES.items():
        assert d["enum_"+name]=={"type":"string","enum":list(values)}
    for alias in ("corrects","observed_by","validated_by","appeals","observes_independently"):
        assert alias not in VOCABULARIES["predicate"]
    assert "unresolved_reference" not in VOCABULARIES["resolved_kind"]
    assert "not_applicable" not in VOCABULARIES["endpoint_gap_reason"]


def test_every_kind_dispatches_to_its_own_closed_local_shape():
    d=load(SCHEMA)["$defs"]
    for name,selector,field,mapping in (("Record","kind","data",RECORD_SHAPES),
            ("RelationData","predicate","details",RELATION_SHAPES),
            ("AssessmentData","assessment_kind","details",ASSESSMENT_SHAPES)):
        branches=d[name]["allOf"][:len(mapping)]
        assert len(branches)==len(mapping)
        for branch,(value,shape) in zip(branches,mapping.items()):
            assert branch["if"]["required"]==[selector]
            assert branch["if"]["properties"][selector]=={"const":value}
            assert branch["then"]["properties"][field]==reference(shape)
            assert d[shape]["additionalProperties"] is False


def test_all_refs_resolve_locally_without_schema_lookup():
    schema=load(SCHEMA)
    assert schema["$schema"]=="https://json-schema.org/draft/2020-12/schema"
    stack=[schema]
    while stack:
        v=stack.pop()
        if isinstance(v,dict):
            if "$ref" in v:
                assert v["$ref"].startswith("#/$defs/")
                assert v["$ref"].split("/")[-1] in schema["$defs"]
            assert "$dynamicRef" not in v and "default" not in v and "format" not in v
            assert "maxLength" not in v and "maximum" not in v
            if "maxItems" in v:
                assert v in ({"minItems":1,"maxItems":1},{"minItems":2,"maxItems":2})
            stack.extend(v.values())
        elif isinstance(v,list):stack.extend(v)


def test_coverage_is_complete_per_field_and_preserves_pending_runtime():
    c=load("phase2/input_contract_coverage.json")
    assert c["source"]=={"path":SOURCE,"sha256":SOURCE_HASH}
    assert c["runtime_checks"]=="pending" and c["whole_prerequisites_completed"]==[]
    assert c["analytical_traces_closed"]==[]
    assert len(c["shapes"])==len(SHAPES)
    seen=set(); source=(ROOT/SOURCE).read_text().splitlines()
    for row,decl in zip(c["shapes"],SHAPES):
        name,section,fs=decl
        assert (row["shape"],row["section"])==(name,section)
        a,b=row["source_lines"]; context="\n".join(source[a-1:b])
        assert context.startswith(("## "+section+".","### "+section+" "))
        assert [tuple(r[:3]) for r in row["fields"]]==list(fs)
        for field,t,required,null_rule,owner,case in row["fields"]:
            assert "`"+field+"`" in context, (name,field)
            assert case not in seen;seen.add(case)
            assert owner.startswith("validation/")
            assert null_rule=="not_nullable" or "|null" in t
    assert len(seen)==242
    assert len(c["mandatory_remaining_rules"])==30


def test_complete_shared_field_sets_against_source_tables():
    # Independent exact field names, not derived from candidate schema.
    expected={
      "TimeValue":{"state","value","precision","reason"},
      "Gap":{"field","reason","detail"},
      "Provenance":{"attributed_to_ref","basis_kind","evidence_ref_ids","method","qualifications"},
      "RoleBinding":{"role","object_ref","evidence_ref_ids","qualifications"},
      "RelationData":{"predicate","from_ref","to_ref","polarity","dimension","details"},
      "AssessmentData":{"assessment_kind","subject_refs","details"},
    }
    d=load(SCHEMA)["$defs"]
    for shape,names in expected.items():assert set(d[shape]["properties"])==names


def test_scoring_and_control_fields_are_not_added_to_core():
    d=load(SCHEMA)["$defs"]
    forbidden={"is_true","is_independent","is_original","overall_level","max_level","trust_weight","score","report_kind","analysis_policy"}
    for shape,sec,fs in SHAPES:
        assert not set(d[shape]["properties"]) & forbidden
    assert d["Extensions"]["additionalProperties"]==reference("JsonValue")
    assert d["Bundle"]["properties"]["predecessor"]=={"anyOf":[reference("Predecessor"),{"type":"null"}]}


def test_no_runtime_schema_or_source_reads():
    for name in ("bundle","constants","evidence","execution","report"):
        text=(ROOT/f"src/source_integrity_toolkit/contracts/{name}.py").read_text()
        for forbidden in ("read_bytes(","read_text(","json.load(","urlopen(","open(","eval("):
            assert forbidden not in text
    assert not (ROOT/"schemas/report/sit-report-0.1.schema.json").exists()


def test_duplicate_schema_key_is_not_silently_overwritten():
    with pytest.raises(ValueError):json.loads('{"x":1,"x":2}',object_pairs_hook=unique)
