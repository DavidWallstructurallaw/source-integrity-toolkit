# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W02 source-bound registry and scoped PC02/PC24 construction facts.

Reporting §§13.1,16.2–16.7,17; architecture §§18.1,19.3. Test-owned facts
check representation/completion consistency, not a performed domain analysis.
"""
from dataclasses import fields, replace
import hashlib
import importlib.util
from pathlib import Path
import re
import pytest
from source_integrity_toolkit.contracts import report, results as r
from source_integrity_toolkit.contracts.bundle import _Object
from source_integrity_toolkit.contracts.evidence import _Node
from source_integrity_toolkit.contracts.execution import _AnalysisAborted
from source_integrity_toolkit.runtime import resources

ROOT = Path(__file__).resolve().parents[2]
SOURCE_HASH = "44daa3c86fc7d12e7be16a3aedfe10d16b99f55aa69141f90319ce2b5e63ff6a"
spec = importlib.util.spec_from_file_location("sit_w02_result_fixtures", ROOT / "tests/contract/test_result_contract.py")
cases = importlib.util.module_from_spec(spec); spec.loader.exec_module(cases)


def source_fields():
    raw = (ROOT / "OBSERVABILITY_AND_REPORTING.md").read_bytes()
    assert hashlib.sha256(raw).hexdigest() == SOURCE_HASH
    block = raw.decode().split("## 17. Output leaf catalog")[1].split("M003 keeps each comparison")[0]
    rows=[]
    for family, body in re.findall(r"^\| M(\d{3}) \| (.*?) \|$", block, re.M):
        for group in body.split(";"):
            names, kind = group.rsplit(":",1)
            rows.extend(("SIT-M"+family,name,kind.strip().split()[0]) for name in re.findall(r"`([^`]+)`",names))
    assert len(rows) == 57 and len(set(rows)) == 57
    return tuple(rows)


EXPECTED_FIELDS = source_fields()


def result_ref(**scope_changes):
    return r._ResultRef("SIT-M001","seed_evidence_item_count",cases.scope(**scope_changes))


def analysis_job():
    """Test-owned accepted-state setup, not evidence of real input admission."""
    owner=resources._new_analysis_budget()
    owner.record_input_acceptance()
    return owner.start_job()


def complete_record(pop=None, **changes):
    if pop is None: pop=cases.population()
    slot = r._ResultRef("SIT-M001","seed_evidence_item_count",pop.scope)
    components = tuple(report._ComponentCompletion(name, (slot,) if name == "value" else (),
                                                   (slot,) if name == "value" else ())
                       for name in ("premises","conflicts","value","basis","reasons","witnesses"))
    values=dict(result_ref=slot,required_populations=(pop,),
                population_completions=(report._PopulationCompletion(pop,pop.member_refs),),components=components)
    values.update(changes)
    return report._CompletionRecord(**values)


def test_all_57_declarative_field_bindings_match_frozen_source_in_order():
    assert r.FIELD_BINDINGS == EXPECTED_FIELDS
    assert len({family for family,field,kind in r.FIELD_BINDINGS}) == 15
    assert {kind for family,field,kind in r.FIELD_BINDINGS} == set(cases.VALUE_KINDS)
    assert tuple((family,field) for family,leaves,checks,domains in report.FAMILY_PREPARATION_BINDINGS
                 for field in leaves) == tuple((family,field) for family,field,kind in EXPECTED_FIELDS)
    assert set(r.STATE_PAIRS) == set(cases.STATE_PAIRS)


@pytest.mark.parametrize("family,field,kind", EXPECTED_FIELDS, ids=[row[1] for row in EXPECTED_FIELDS])
def test_each_registered_slot_uses_its_own_family_without_claiming_execution(family, field, kind):
    slot = r._ResultRef(family,field,cases.scope())
    assert (slot.diagnostic_id,slot.field_key) == (family,field)
    assert not hasattr(slot,"result_state") and not hasattr(slot,"value")
    wrong = "SIT-M002" if family == "SIT-M001" else "SIT-M001"
    with pytest.raises(TypeError): r._ResultRef(wrong,field,cases.scope())


def test_closed_reason_codes_are_source_derived_without_new_detector_or_cancellation_code():
    text=(ROOT / "OBSERVABILITY_AND_REPORTING.md").read_text()
    block=text.split("### 13.2 Reason objects")[1].split("## 14.")[0]
    expected=tuple(re.findall(r"^\| `([^`]+)` \|",block,re.M))
    assert len(expected)==40 and tuple(r.REASON_CODES)==expected
    assert "cancelled" not in expected and "source_verified" not in expected
    slot=result_ref()
    with pytest.raises(TypeError):
        r._Reason("source_verified",slot.scope,(slot,),(),"Not an approved result.","evidence_gap")
    with pytest.raises(TypeError):
        r._Reason("unknown_endpoint",slot.scope,(slot,),(),"A declared gap.","high_severity")


@pytest.mark.parametrize("state", ["met","unmet","unknown","not_applicable"])
def test_prerequisite_state_is_scoped_representation_not_execution(state):
    slot=result_ref()
    reason=r._Reason("upstream_coverage_incomplete",slot.scope,(slot,),(),"Fictional limited history.","evidence_gap")
    check=r._PrerequisiteCheck("PC06",slot,state,(),(reason,),"Declared component case only.")
    assert check.state==state and check.result_ref is slot
    assert not hasattr(check,"complete_check_executed")
    assert not hasattr(check,"accepted")


@pytest.mark.parametrize("bad", ["PC00","PC25","PC2","pc02","PC02 ",True])
def test_check_identity_cannot_invent_or_alias_a_registry_question(bad):
    with pytest.raises(TypeError):
        r._PrerequisiteCheck(bad,result_ref(),"met",(),(),"Bounded representation.")


def test_same_pc_in_different_claim_scopes_is_not_a_global_coverage_answer():
    first=result_ref();second=result_ref(claim_refs=(cases.ref("C2"),))
    a=r._PrerequisiteCheck("PC06",first,"met",(),(),"First scoped coverage.")
    reason=r._Reason("upstream_coverage_incomplete",second.scope,(second,),(),"Second scope has no coverage.","evidence_gap")
    b=r._PrerequisiteCheck("PC06",second,"unknown",(),(reason,),"Second scoped question.")
    assert a.state=="met" and b.state=="unknown"
    assert a.result_ref.scope.claim_refs[0].identifier=="C1"
    assert b.result_ref.scope.claim_refs[0].identifier=="C2"


def test_pc02_requires_evaluating_exact_scope_fact_and_charges_actual_work():
    slot=result_ref()
    fact=report._ScopeCheckFact(slot,slot.scope)
    assert not hasattr(fact,"state") and not hasattr(fact,"met")
    port=analysis_job();before=port.used
    check=report._scope_check(fact,port)
    assert check.check_id=="PC02" and check.state=="met" and check.result_ref is slot
    assert port.used>before


@pytest.mark.parametrize("change", ["inquiry","claim_version","targets","dimension","view","time","anchor"])
def test_pc02_does_not_match_a_neighboring_scope_or_infer_wildcards(change):
    slot=result_ref()
    changes={
        "inquiry":{"inquiry_ref":cases.ref("I2","inquiries")},
        "claim_version":{"claim_refs":(cases.ref("C1-V2"),)},
        "targets":{"target_refs":(cases.ref("A2"),)},
        "dimension":{"dependency_dimension":"acquisition"},
        "view":{"graph_view":"claim_origin"},
        "time":{"temporal_basis":"time_specific","requested_time":_Node("TimeValue",_Object((("state","known"),("value","2026-01-01"),("precision","date"),("reason",None))))},
        "anchor":{"operation_anchor":(cases.ref("ASSESSMENT-2","assertions"),)},
    }[change]
    fact=report._ScopeCheckFact(slot,cases.scope(**changes))
    check=report._scope_check(fact,analysis_job())
    assert check.check_id=="PC02" and check.state=="unmet"
    assert any(reason.code=="scope_unestablished" for reason in check.reason_refs)
    assert check.result_ref is slot


def test_pc24_is_met_only_for_complete_population_and_all_commit_components():
    record=complete_record()
    assert not hasattr(record,"state") and not hasattr(record,"completed")
    port=analysis_job();before=port.used
    check=report._completion_check(record,port)
    assert check.check_id=="PC24" and check.state=="met"
    assert check.result_ref is record.result_ref and port.used>before
    assert {component.component for component in record.components}=={
        "premises","conflicts","value","basis","reasons","witnesses"}


@pytest.mark.parametrize("missing", ["premises","conflicts","value","basis","reasons","witnesses"])
def test_pc24_cannot_complete_after_omitting_a_required_commit_component(missing):
    record=complete_record()
    partial=replace(record,components=tuple(c for c in record.components if c.component!=missing))
    check=report._completion_check(partial,analysis_job())
    assert check.state in ("unmet","unknown") and check.note
    assert not hasattr(check,"value")
    # Missing completion facts alone do not establish a runtime stop cause.
    assert not any(reason.code in ("resource_limit_reached","execution_failed") for reason in check.reason_refs)


def test_pc24_does_not_turn_partial_member_visits_into_zero_or_completed_enumeration():
    pop=cases.population((cases.ref("E1"),cases.ref("E2")))
    partial=complete_record(pop,population_completions=(report._PopulationCompletion(pop,(pop.member_refs[0],)),))
    check=report._completion_check(partial,analysis_job())
    assert check.state in ("unmet","unknown")
    assert len(pop.member_refs)==2 and not hasattr(check,"value")
    finished=complete_record(pop,population_completions=(report._PopulationCompletion(pop,tuple(reversed(pop.member_refs))),))
    assert report._completion_check(finished,analysis_job()).state=="met"


def test_pc24_retains_empty_known_population_versus_unestablished_membership():
    known=complete_record(cases.population(()))
    unknown=complete_record(cases.population((),membership_state="unestablished"))
    assert report._completion_check(known,analysis_job()).state=="met"
    assert report._completion_check(unknown,analysis_job()).state in ("unknown","unmet")


def test_pc24_other_result_value_cannot_complete_this_result():
    record=complete_record();other=result_ref(claim_refs=(cases.ref("C2"),))
    changed=tuple(report._ComponentCompletion("value",(other,),(other,)) if c.component=="value" else c for c in record.components)
    with pytest.raises(TypeError): replace(record,components=changed)


@pytest.mark.parametrize("bad", [True,False,{"all_met":True},[],"completed"])
def test_completion_metadata_flags_cannot_replace_typed_execution_facts(bad):
    with pytest.raises(TypeError):
        report._CompletionRecord(result_ref(),(),(),bad)
    with pytest.raises(TypeError):
        report._PopulationCompletion(cases.population(),bad)


def test_preparation_pending_pc02_pc24_stays_distinct_from_new_construction_facts():
    for pc in ("PC02","PC24"):
        pending=report._PendingCheck(pc)
        assert {f.name for f in fields(pending)}=={"prerequisite"}
        assert pending.prerequisite==pc and not hasattr(pending,"state")
    assert dict(report.PREREQUISITE_OWNERS)["PC02"]=="REPORT_CONTRACT"
    assert dict(report.PREREQUISITE_OWNERS)["PC24"]=="REPORT_CONTRACT"


def helper_input(check_id):
    if check_id=="PC02":
        slot=result_ref()
        return report._scope_check, report._ScopeCheckFact(slot,slot.scope)
    return report._completion_check, complete_record()


@pytest.mark.parametrize("check_id", ["PC02","PC24"])
@pytest.mark.parametrize("factory", [resources._new_budget,resources._new_analysis_budget],
                         ids=["preparation","admission"])
def test_scoped_checks_refuse_non_job_accounting_ports(check_id, factory):
    helper,fact=helper_input(check_id)
    port=factory();before=port.used
    with pytest.raises(TypeError,match="^analysis_job_port_required$"):
        helper(fact,port)
    assert port.used==before


@pytest.mark.parametrize("check_id", ["PC02","PC24"])
@pytest.mark.parametrize("stopped", [False,True], ids=["finished_analysis","resource_stopped_analysis"])
def test_scoped_checks_cannot_execute_through_a_working_finalization_port(check_id, stopped):
    helper,fact=helper_input(check_id)
    owner=resources._new_analysis_budget()
    owner.record_input_acceptance()  # Test setup does not perform admission.
    job=owner.start_job()
    if stopped:
        with pytest.raises(_AnalysisAborted) as original:
            job.charge(1_000_001)
        assert original.value.limit_id=="WU9-L11"
    else:
        owner.finish_job(job)
    finalizer=owner.begin_finalization()
    finalizer.charge(1)  # Delivery accounting remains usable in both cases.
    before=owner.used
    with pytest.raises(TypeError,match="^analysis_job_port_required$"):
        helper(fact,finalizer)
    assert owner.used==before
    finalizer.check()


@pytest.mark.parametrize("check_id", ["PC02","PC24"])
@pytest.mark.parametrize("finalizing", [False,True], ids=["stopped_job","obsolete_job_after_finalization"])
def test_scoped_checks_preserve_the_original_stop_without_executing(check_id, finalizing, monkeypatch):
    helper,fact=helper_input(check_id)
    owner=resources._new_analysis_budget()
    owner.record_input_acceptance()
    job=owner.start_job()
    with pytest.raises(_AnalysisAborted) as original:
        job.charge(1_000_001)
    if finalizing:
        owner.begin_finalization()
    before=(owner.used,job.used)
    def unexpected_construction(*args,**kwargs):
        raise AssertionError("Stopped analysis must not construct a prerequisite check.")
    monkeypatch.setattr(report,"_PrerequisiteCheck",unexpected_construction)
    with pytest.raises(_AnalysisAborted) as repeated:
        helper(fact,job)
    assert repeated.value is original.value
    assert repeated.value.limit_id=="WU9-L11"
    assert (owner.used,job.used)==before


@pytest.mark.parametrize("check_id", ["PC02","PC24"])
@pytest.mark.parametrize("expires", ["before_helper","during_check_construction"])
def test_scoped_checks_observe_deadline_before_work_and_after_check_construction(check_id, expires, monkeypatch):
    helper,fact=helper_input(check_id)
    now=[0]
    monkeypatch.setattr(resources,"monotonic_ns",lambda:now[0])
    job=analysis_job();before=job.used
    constructed=[]
    original_constructor=report._PrerequisiteCheck
    def observed_constructor(*args,**kwargs):
        value=original_constructor(*args,**kwargs)
        constructed.append(value.check_id)
        if expires=="during_check_construction":
            now[0]=60_000_000_001
        return value
    monkeypatch.setattr(report,"_PrerequisiteCheck",observed_constructor)
    if expires=="before_helper":
        now[0]=60_000_000_001
    with pytest.raises(_AnalysisAborted) as stopped:
        helper(fact,job)
    assert stopped.value.limit_id=="WU9-L12"
    assert stopped.value.stop.execution_state=="interrupted"
    assert stopped.value.stop.reason_code=="resource_limit_reached"
    if expires=="before_helper":
        assert constructed==[] and job.used==before
    else:
        assert constructed==[check_id] and job.used>before
    after=job.used
    with pytest.raises(_AnalysisAborted) as repeated:
        job.check()
    assert repeated.value is stopped.value and job.used==after
