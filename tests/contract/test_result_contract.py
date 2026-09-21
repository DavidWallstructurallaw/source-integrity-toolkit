# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""W02 private result primitives; reporting §§12.3,16.2–16.6 and architecture18.1.

These are bounded project-owned construction cases, not executed analysis or
sit-report/0.1 conformance. Frozen source numbers remain independent oracles.
"""
from dataclasses import FrozenInstanceError, fields, replace
import itertools
import pytest
from source_integrity_toolkit.contracts import results as r
from source_integrity_toolkit.contracts.bundle import _Object, _Array


LIMIT = 9_007_199_254_740_991
STATE_PAIRS = (("completed", "available"), ("completed", "unavailable"),
               ("completed", "not_applicable"), ("not_performed", "not_evaluated"),
               ("interrupted", "not_evaluated"), ("failed", "not_evaluated"))
VALUE_KINDS = ("count", "fraction", "completion_interval", "partition", "incidence",
               "record_disclosures", "witness_collection")


def ref(identifier="E1", collection="records", selector=None):
    return r._InputRef(collection, identifier, selector)


def scope(**changes):
    values = dict(inquiry_ref=ref("I1", "inquiries"), claim_refs=(ref("C1"),),
                  target_refs=(), dependency_dimension=None, graph_view=None,
                  temporal_basis="snapshot_structural", requested_time=None,
                  coverage_refs=(), qualifications=("Explicit inventory; no graph inference.",),
                  operation_anchor=())
    values.update(changes)
    return r._Scope(**values)


def population(members=None, **changes):
    values = dict(scope=scope(), unit="evidence_item", member_refs=(ref(),) if members is None else members,
                  selection_rule="E(I,C)", coverage_refs=(), basis_refs=(),
                  membership_state="enumerated_for_scope", qualifications=())
    values.update(changes)
    return r._Population(**values)


def result(execution="completed", state="available", **changes):
    populations = changes.get("population_refs", ())
    pop = populations[0] if populations else population()
    candidate = changes.get("ref")
    slot = candidate if type(candidate) is r._ResultRef else r._ResultRef("SIT-M001", "seed_evidence_item_count", pop.scope)
    code = {"interrupted":"resource_limit_reached", "failed":"execution_failed",
            "not_performed":"input_not_accepted"}.get(execution,
            "no_applicable_subject" if state == "not_applicable" else "scope_unestablished")
    classification = "structural_inapplicability" if state == "not_applicable" else (
        "execution" if execution != "completed" else "evidence_gap")
    reason = r._Reason(code, pop.scope, (slot,), (),
                       "Fictional scoped test limitation.", classification)
    values = dict(ref=slot, population_refs=(pop,), execution_state=execution,
                  result_state=state, result_origin="inventory", value_kind="count",
                  value=(changes["value"] if "value" in changes else r._Count(len(pop.member_refs), pop)) if state == "available" else None,
                  check_refs=(), basis_refs=(), witness_refs=(),
                  reason_refs=() if state == "available" else (reason,),
                  interpretation_limit="Supplied finite inventory only; no outside-world source count.")
    values.update(changes)
    return r._Result(**values)


def interval_partition(pop, kind, known, unknown):
    members=pop.member_refs;end=len(members)-unknown
    labels=(("inherited_only_at_evidence_layer","direct_origin_link_only",
             "mixed_direct_and_inherited","unresolved_at_evidence_layer")
            if kind=="finite_record_completion" else ("Y","F","U"))
    groups=(members[:known],members[known:end],(),members[end:]) if len(labels)==4 else (members[:known],members[known:end],members[end:])
    return r._Partition(pop,tuple(r._PartitionCategory(label,rows,len(rows)) for label,rows in zip(labels,groups)))


@pytest.mark.parametrize("execution,state", STATE_PAIRS)
def test_all_six_state_pairs_preserve_execution_separately_from_availability(execution, state):
    out = result(execution, state)
    assert (out.execution_state, out.result_state) == (execution, state)
    assert (out.value is None) is (state != "available")
    assert out.interpretation_limit and out.ref.scope.claim_refs[0].identifier == "C1"


@pytest.mark.parametrize("execution,state", [pair for pair in itertools.product(
    ("completed", "not_performed", "interrupted", "failed"),
    ("available", "unavailable", "not_applicable", "not_evaluated")) if pair not in STATE_PAIRS])
def test_other_ten_state_pairs_cannot_turn_unfinished_work_into_a_result(execution, state):
    with pytest.raises(TypeError, match="^invalid_private_representation$"):
        result(execution, state)


@pytest.mark.parametrize("execution,state", STATE_PAIRS[1:])
def test_non_results_require_null_and_actual_reason(execution, state):
    with pytest.raises(TypeError):
        result(execution, state, value=r._Count(0, population(())))
    with pytest.raises(TypeError):
        result(execution, state, reason_refs=())


def test_available_zero_names_an_explicit_empty_population():
    pop = population(())
    out = result(value=r._Count(0, pop), population_refs=(pop,))
    assert out.value.value == 0 and out.value.population.member_refs == ()
    assert pop.membership_state == "enumerated_for_scope"
    unknown = population((), membership_state="unestablished")
    assert unknown.membership_state != pop.membership_state
    with pytest.raises(TypeError):
        r._Count(0, unknown)
    with pytest.raises(TypeError):
        result(value=None)


@pytest.mark.parametrize("bad", [True, False, -1, 1.0, float("nan"), float("inf"), "1", LIMIT + 1])
def test_count_rejects_boolean_inexact_negative_and_out_of_range_values(bad):
    with pytest.raises(TypeError):
        r._Count(bad, population())


@pytest.mark.parametrize("n,d", [(26,36), (25,25), (0,6), (1,LIMIT), (6,7)])
def test_exact_fraction_keeps_original_denominator_and_does_not_round(n, d):
    value = r._Fraction(n, d, population())
    assert (value.numerator, value.denominator) == (n, d)
    assert type(value.numerator) is int and type(value.denominator) is int
    assert not hasattr(value, "display_decimal")


@pytest.mark.parametrize("n,d", [(True,1), (1,True), (-1,7), (1,0), (1,-7),
                                  (1.0,7), (1,7.0), (LIMIT+1,1), (1,LIMIT+1)])
def test_fraction_components_require_portable_exact_nonnegative_integers(n, d):
    with pytest.raises(TypeError):
        r._Fraction(n, d, population())


@pytest.mark.parametrize("kind", ["finite_record_completion", "finite_cohort_completion"])
def test_interval_retains_same_population_and_unreduced_endpoints(kind):
    pop = population(tuple(ref("E" + str(i)) for i in range(7)))
    lower, upper = r._Fraction(5,7,pop), r._Fraction(6,7,pop)
    value = r._CompletionInterval(lower, upper, kind, interval_partition(pop,kind,5,1))
    assert (value.lower.numerator, value.upper.numerator, value.upper.denominator) == (5,6,7)
    assert value.lower.population is pop and value.upper.population is pop
    assert value.interval_kind == kind


@pytest.mark.parametrize("change", ["reversed", "different_denominator", "over_one", "different_population", "confidence_label"])
def test_interval_cannot_hide_population_change_or_claim_a_confidence_interval(change):
    pop = population((ref("E1"), ref("E2")))
    lower, upper, kind = r._Fraction(0,2,pop), r._Fraction(2,2,pop), "finite_record_completion"
    if change == "reversed": lower, upper = upper, lower
    elif change == "different_denominator": upper = r._Fraction(1,1,pop)
    elif change == "over_one": upper = r._Fraction(3,2,pop)
    elif change == "different_population": upper = r._Fraction(2,2,population((ref("E3"),ref("E4"))))
    else: kind = "confidence_interval"
    with pytest.raises(TypeError):
        r._CompletionInterval(lower, upper, kind, interval_partition(pop,"finite_record_completion",0,2))


def test_population_preserves_typed_identities_and_correction_pairs():
    a, b = ref("same", "records"), ref("same", "assertions")
    assert len(population((a,b),unit="record").member_refs) == 2
    pair1 = r._CaseTarget(ref("CASE1"), ref("A1"))
    pair2 = r._CaseTarget(ref("CASE2"), ref("A1"))
    selected = population((pair1,pair2), unit="case_target", selection_rule="(case_ref,before_ref)")
    assert len(selected.member_refs) == 2
    assert selected.member_refs[0].before_ref.identifier == "A1"
    with pytest.raises(TypeError):
        population((a, ref("same", "records")))
    with pytest.raises(TypeError):
        population((pair1, r._CaseTarget(ref("CASE1"),ref("A1"))), unit="case_target")


@pytest.mark.parametrize("field,bad", [("member_refs", []), ("coverage_refs", []),
                                      ("basis_refs", {}), ("qualifications", []),
                                      ("membership_state", "complete"), ("scope", {})])
def test_population_does_not_capture_mutable_parts_or_invent_membership_states(field, bad):
    with pytest.raises(TypeError):
        population(**{field:bad})


@pytest.mark.parametrize("collection", ["records", "assertions", "evidence_references", "inquiries"])
def test_input_reference_retains_collection_and_canonical_field_selector(collection):
    value = ref("opaque-same", collection, "data.role_bindings.judge")
    assert (value.collection, value.identifier, value.selector) == (collection, "opaque-same", "data.role_bindings.judge")
    assert not hasattr(value, "report_id")


@pytest.mark.parametrize("collection", ["results", "SIT-RES", "all", "records ", None])
def test_input_reference_cannot_use_a_private_result_namespace(collection):
    with pytest.raises(TypeError):
        ref("same", collection)


@pytest.mark.parametrize("field,bad", [("dependency_dimension", "citation"), ("graph_view", "all_edges"),
                                      ("temporal_basis", "latest_wins"), ("claim_refs", []),
                                      ("target_refs", []), ("operation_anchor", {})])
def test_scope_has_no_open_control_vocabulary_or_mutable_selectors(field,bad):
    with pytest.raises(TypeError):
        scope(**{field:bad})


@pytest.mark.parametrize("field,bad", [("result_origin", "verified"), ("result_state", "passed"),
                                      ("execution_state", "success"), ("value_kind", "integrity_score"),
                                      ("interpretation_limit", ""), ("check_refs", []),
                                      ("basis_refs", ["basis"]), ("witness_refs", ["witness"])])
def test_result_rejects_invented_status_and_untyped_mutable_links(field,bad):
    with pytest.raises(TypeError):
        result(**{field:bad})


def test_private_result_link_is_typed_and_distinct_from_input_identity():
    out = result()
    assert isinstance(out.ref, r._ResultRef)
    assert out.ref.diagnostic_id == "SIT-M001" and out.ref.field_key == "seed_evidence_item_count"
    with pytest.raises(TypeError):
        result(ref=ref("SIT-RES-000001"))
    with pytest.raises(TypeError):
        result(check_refs=(ref("PC02"),))
    with pytest.raises(TypeError):
        result(reason_refs=(ref("unknown_endpoint"),))


def test_duplicate_unequal_semantic_result_slots_fail_without_newest_wins():
    first = result()
    conflicting = result("completed", "unavailable", ref=first.ref, population_refs=first.population_refs)
    assert r._ResultSet((first,)).results == (first,)
    with pytest.raises(TypeError):
        r._ResultSet((first,conflicting))
    pop2 = population(scope=scope(claim_refs=(ref("C2"),)))
    separate = result(ref=r._ResultRef("SIT-M001","seed_evidence_item_count",pop2.scope),
                      population_refs=(pop2,),value=r._Count(1,pop2))
    assert len(r._ResultSet((first,separate)).results) == 2


def test_private_objects_are_frozen_and_never_retain_mutable_caller_containers():
    out = result()
    for value in (out, out.ref, out.ref.scope, out.population_refs[0], out.value, ref()):
        with pytest.raises(FrozenInstanceError):
            setattr(value, fields(value)[0].name, None)
        assert not hasattr(value, "__dict__")
    mutable = {"state":"failed"}
    with pytest.raises(TypeError):
        r._Disclosure(ref("EVENT1"), mutable)
    frozen = _Object((("state","failed"),("reported_outcome","verified")))
    disclosure = r._Disclosure(ref("EVENT1"), frozen)
    value = r._RecordDisclosures((disclosure,))
    assert value.records[0].fields.items == frozen.items
    assert not hasattr(value, "verified") and not hasattr(value, "execution_state")


def test_hostile_container_and_scalar_protocols_are_not_invoked():
    calls=[]
    def touched(*args,**kwargs):
        calls.append("called"); raise AssertionError("caller_protocol_executed")
    class HostileTuple(tuple):
        __iter__ = __len__ = touched
    class HostileInt(int):
        __lt__ = __le__ = __eq__ = __int__ = touched
    class HostileString(str):
        __eq__ = __hash__ = __str__ = touched
    for make in (lambda:population(HostileTuple()),lambda:r._Count(HostileInt(1),population()),
                 lambda:ref(HostileString("opaque"))):
        with pytest.raises(TypeError): make()
    assert calls == []


def test_partition_retains_unknown_members_and_exact_exclusive_counts():
    members=tuple(ref("E"+str(i)) for i in range(3));pop=population(members)
    categories=tuple(r._PartitionCategory(label,(member,),1) for label,member in zip(("Y","F","U"),members))
    part=r._Partition(pop,categories)
    assert tuple((c.label,c.count) for c in part.categories)==(("Y",1),("F",1),("U",1))
    assert sum(c.count for c in part.categories)==len(pop.member_refs)==3
    with pytest.raises(TypeError): r._Partition(pop,categories[:-1])
    with pytest.raises(TypeError): r._Partition(pop,categories+(r._PartitionCategory("supplied",(members[0],),1),))
    with pytest.raises(TypeError): r._PartitionCategory("Y",(members[0],),True)
    with pytest.raises(TypeError): r._PartitionCategory("Y",(members[0],),2)
    with pytest.raises(TypeError): r._PartitionCategory("negative",(members[0],),1)


def test_incidence_is_nonexclusive_and_keeps_empty_unknown_rows_in_population():
    e1,e2,e3=ref("E1"),ref("E2"),ref("E3");o1,o2=ref("O1"),ref("O2")
    pop=population((e1,e2,e3))
    rows=(r._IncidenceRow(e1,(o1,o2)),r._IncidenceRow(e2,(o1,o2)),r._IncidenceRow(e3,()))
    value=r._Incidence(pop,rows)
    assert value.nonexclusive is True
    assert [(origin.identifier,count) for origin,count in value.origin_counts]==[("O1",2),("O2",2)]
    assert sum(count for origin,count in value.origin_counts)>len(pop.member_refs)
    assert value.memberships[-1].member_ref.identifier=="E3" and value.memberships[-1].origin_refs==()
    with pytest.raises(TypeError): r._Incidence(pop,rows[:-1])
    with pytest.raises(TypeError): r._Incidence(pop,rows+(rows[0],))
    with pytest.raises(TypeError): r._IncidenceRow(e1,(o1,ref("O1")))


def test_all_seven_value_kinds_have_live_typed_positive_results():
    pop=population((ref("E1"),ref("E2")))
    scope1=pop.scope
    witness=r._WitnessRef(scope1,"path",(ref("E1"),ref("O1")))
    disclosure=r._RecordDisclosures((r._Disclosure(ref("EVENT1"),_Object((("outcome","failed"),))),))
    variants=(
        ("SIT-M001","seed_evidence_item_count","count",r._Count(2,pop)),
        ("SIT-M005","single_origin_contribution_hhi","fraction",r._Fraction(2,4,pop)),
        ("SIT-M006","inherited_only_completion_interval","completion_interval",
         r._CompletionInterval(r._Fraction(0,2,pop),r._Fraction(1,2,pop),"finite_record_completion",
                               interval_partition(pop,"finite_record_completion",0,1))),
        ("SIT-M010","stage_member_partition","partition",r._Partition(pop,(
            r._PartitionCategory("Y",(pop.member_refs[0],),1),r._PartitionCategory("F",(),0),
            r._PartitionCategory("U",(pop.member_refs[1],),1)))),
        ("SIT-M004","per_seed_origin_memberships","incidence",r._Incidence(pop,(
            r._IncidenceRow(pop.member_refs[0],(ref("O1"),)),r._IncidenceRow(pop.member_refs[1],())))),
        ("SIT-M012","correction_case_disclosures","record_disclosures",disclosure),
        ("SIT-M011","declared_correction_route_witnesses","witness_collection",r._WitnessCollection((witness,))),
    )
    for family,field,kind,value in variants:
        out=result(ref=r._ResultRef(family,field,scope1),population_refs=(pop,),value_kind=kind,
                   value=value,witness_refs=(witness,) if kind=="witness_collection" else ())
        assert out.value is value and out.value_kind==kind
        with pytest.raises(TypeError): replace(out,value=True)
    assert {row[2] for row in variants}==set(VALUE_KINDS)


def test_typed_links_reject_check_reason_witness_and_population_from_other_scope():
    current=result();other=scope(claim_refs=(ref("C2"),))
    other_ref=r._ResultRef("SIT-M001","seed_evidence_item_count",other)
    with pytest.raises(TypeError):
        replace(current,check_refs=(r._PrerequisiteCheck("PC02",other_ref,"met",(),(),"Another scope."),))
    with pytest.raises(TypeError):
        replace(current,reason_refs=(r._Reason("scope_unestablished",other,(other_ref,),(),"Another scope.","evidence_gap"),))
    with pytest.raises(TypeError):
        replace(current,witness_refs=(r._WitnessRef(other,"member_set",(ref("E1"),)),))
    with pytest.raises(TypeError):
        replace(current,population_refs=(population(scope=other),))


def test_semantically_equal_reordered_scope_cannot_bypass_duplicate_slot_check():
    a,b=ref("C1"),ref("C2")
    pop1=population(scope=scope(claim_refs=(a,b)))
    pop2=population(scope=scope(claim_refs=(b,a)))
    first=result(ref=r._ResultRef("SIT-M001","seed_evidence_item_count",pop1.scope),population_refs=(pop1,),value=r._Count(1,pop1))
    second=result(ref=r._ResultRef("SIT-M001","seed_evidence_item_count",pop2.scope),population_refs=(pop2,),value=r._Count(1,pop2))
    with pytest.raises(TypeError): r._ResultSet((first,second))


def test_same_semantic_population_key_cannot_hide_unestablished_result_membership():
    pop=population();out=result(population_refs=(pop,),value=r._Count(1,pop))
    forged=replace(pop,membership_state="unestablished",qualifications=("Membership is unknown.",))
    assert out.value.population is pop
    with pytest.raises(TypeError): replace(out,population_refs=(forged,))
    with pytest.raises(TypeError): replace(out,ref=r._ResultRef(out.ref.diagnostic_id,out.ref.field_key,scope()))


@pytest.mark.parametrize("kind", ["finite_record_completion","finite_cohort_completion"])
def test_interval_requires_its_actual_classification_rows_and_unknown_members(kind):
    pop=population(tuple(ref("E"+str(i)) for i in range(7)))
    partition=interval_partition(pop,kind,5,1)
    lower,upper=r._Fraction(5,7,pop),r._Fraction(6,7,pop)
    value=r._CompletionInterval(lower,upper,kind,partition)
    assert value.partition is partition
    assert sum(row.count for row in value.partition.categories)==7
    with pytest.raises(TypeError): r._CompletionInterval(lower,upper,kind,interval_partition(pop,kind,4,2))
    with pytest.raises(TypeError): r._CompletionInterval(lower,upper,kind,interval_partition(pop,kind,5,0))
    # Equal semantic membership is insufficient when the attached population
    # is a separately constructed fact bag with different qualification.
    other=replace(pop,qualifications=("Different supplied coverage basis.",))
    with pytest.raises(TypeError): r._CompletionInterval(lower,r._Fraction(6,7,other),kind,partition)
    with pytest.raises(TypeError): r._CompletionInterval(lower,upper,kind,interval_partition(other,kind,5,1))


def test_hhi_exact_result_keeps_six_seed_population_and_26_over_36():
    pop=population(tuple(ref("E"+str(i)) for i in range(6)))
    slot=r._ResultRef("SIT-M005","single_origin_contribution_hhi",pop.scope)
    out=result(ref=slot,population_refs=(pop,),value_kind="fraction",value=r._Fraction(26,36,pop))
    assert (out.value.numerator,out.value.denominator,len(out.value.population.member_refs))==(26,36,6)
    with pytest.raises(TypeError): replace(out,value=r._Fraction(13,18,pop))


@pytest.mark.parametrize("pc", ["PC02","PC24"])
@pytest.mark.parametrize("state", ["unmet","unknown","not_applicable"])
def test_available_result_cannot_contradict_its_explicit_scope_or_completion_check(pc,state):
    # Reporting12.4/16.4: a value and its exact scope/full-population premises
    # commit together. This checks a carried fact, not an all-PC prerequisite gate.
    out=result()
    check=r._PrerequisiteCheck(pc,out.ref,state,(),(),"Fictional incomplete scope or operation fact.")
    with pytest.raises(TypeError,match="^invalid_private_representation$"):
        replace(out,check_refs=(check,))


@pytest.mark.parametrize("checks", [("PC02",),("PC24",),("PC02","PC24")])
def test_available_result_accepts_met_scope_and_completion_checks_for_its_own_cell(checks):
    out=result()
    carried=tuple(r._PrerequisiteCheck(pc,out.ref,"met",(),(),"Matching bounded component fact.") for pc in checks)
    checked=replace(out,check_refs=carried)
    assert checked.result_state=="available" and checked.value is out.value
    assert all(check.result_ref is checked.ref and check.state=="met" for check in checked.check_refs)


def test_available_inventory_keeps_a_nonblocking_unknown_coverage_check():
    out=result()
    reason=r._Reason("upstream_coverage_incomplete",out.ref.scope,(out.ref,),(),
                     "Unknown upstream history does not erase this explicit inventory.","evidence_gap")
    unknown=r._PrerequisiteCheck("PC06",out.ref,"unknown",(),(reason,),
                                  "Nonblocking coverage limitation for this inventory.")
    exact=tuple(r._PrerequisiteCheck(pc,out.ref,"met",(),(),"Matching inventory fact.") for pc in ("PC02","PC24"))
    checked=replace(out,check_refs=exact+(unknown,),reason_refs=(reason,))
    assert checked.result_state=="available" and checked.value is out.value
    assert checked.check_refs[-1].state=="unknown" and checked.reason_refs==(reason,)
    # A bare private construction remains a representation, not proof of a run.
    assert out.check_refs==() and not hasattr(out,"processing_state")
