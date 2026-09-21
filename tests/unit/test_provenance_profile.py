# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Source-derived W03 M015 component oracles.

Definitions 28.1 and VALIDATION_PLAN VF054--VF057 supply the expected
populations and classifications.  Admission is real; the analytical context
below is a project-owned component harness, not the deferred W13 entry point.
Explicit PC03/PC04 facts are test preconditions, never evidence that either
future provider executed.  The frozen H7 fixture and its logical oracle are
read-only inputs.
"""
import copy
from dataclasses import FrozenInstanceError
import importlib.util
import json
from pathlib import Path

import pytest

from source_integrity_toolkit.contracts.bundle import _Array, _Object
from source_integrity_toolkit.contracts import evidence
from source_integrity_toolkit.contracts import report
from source_integrity_toolkit.contracts import results
from source_integrity_toolkit.contracts.execution import _AnalysisAborted
from source_integrity_toolkit.runtime.boundary import _prepare_value
from source_integrity_toolkit.runtime.resources import _new_analysis_budget
from source_integrity_toolkit.validation import semantics


ROOT = Path(__file__).resolve().parents[2]
spec = importlib.util.spec_from_file_location(
    "sit_w03_provenance_cases", ROOT / "tests/contract/test_typed_records.py")
cases = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cases)

# Literal source expectations, deliberately independent of product registries.
LEAVES = (
    ("coverage_disclosures", "record_disclosures"),
    ("documentary_basis_gap_disclosures", "record_disclosures"),
    ("declared_basis_inventory", "partition"),
    ("reference_availability_inventory", "partition"),
)
BASIS = ("declaration", "documented_record", "upstream_inference",
         "protected_attestation", "unspecified")
AVAILABILITY = ("supplied", "locator_only", "withheld", "unavailable")
H7_RECORDS = tuple("H7-L%02d" % n for n in range(1, 8))
H7_SUPPORT = ("H7-SUP-ACQ", "H7-SUP-CHAIN", "H7-SUP-COMPARE",
              "H7-SUP-CONTEXT", "H7-SUP-CORR", "H7-SUP-GRANT",
              "H7-SUP-MODEL", "H7-SUP-PIPE")
H7_COVERAGE = ("H7-COV-ACQ", "H7-COV-ADM", "H7-COV-COMP",
               "H7-COV-MODEL", "H7-COV-PRES", "H7-COV-ROUTE",
               "H7-COV-SEL", "H7-COV-USE")


def hero():
    return json.loads((ROOT / "tests/fixtures/hero/H7-01.bundle.json").read_bytes())


def logical(value):
    if type(value) is _Object:
        return {key: logical(item) for key, item in value.items}
    if type(value) is _Array:
        return [logical(item) for item in value.items]
    return value


def context(source, **changes):
    inquiry = source["inquiries"][0]
    values = dict(inquiry_ref=inquiry["id"],
                  claim_refs=tuple(inquiry["target_claim_refs"]),
                  subject_refs=(), dependency_dimension=None,
                  temporal_basis="snapshot_structural", requested_time=None,
                  coverage_kind=None, relation_types=(), graph_view=None,
                  operation_anchor=("M015", "explicit_component_population"))
    values.update(changes)
    return evidence._QualificationContext(**values)


def run_profile(source=None, *, record_refs=H7_RECORDS,
                reference_refs=H7_SUPPORT, coverage_refs=H7_COVERAGE,
                with_providers=False, context_changes=None):
    source = hero() if source is None else source
    prepared = _prepare_value(source)
    assert type(prepared) is evidence._PreparedBundle
    ctx = context(source, **(context_changes or {}))
    budget = _new_analysis_budget()
    # The admitted immutable input is a trusted component precondition here.
    # No full analytical admission/job planner is claimed by this harness.
    budget.record_input_acceptance()
    port = budget.start_job()
    provider_facts = ()
    if with_providers:
        addresses = tuple(evidence._SourceAddress("assertions", name)
                          for name in record_refs)
        provider_facts = (
            evidence._ProviderFact("PC03", "SOURCE_INVENTORY", ctx,
                                   "met", addresses, prepared),
            evidence._ProviderFact("PC04", "GRAPH_VIEW_CONTRACT", ctx,
                                   "met", addresses, prepared),
        )
    before = port.used
    out = semantics._provenance_profile(
        prepared, ctx, record_refs, reference_refs, coverage_refs, port,
        provider_facts=provider_facts)
    assert type(out) is results._ResultSet
    assert port.used > before
    return out, prepared, budget, port


def leaf(out, name):
    return next(row for row in out.results if row.ref.field_key == name)


def partition(out, name):
    row = leaf(out, name)
    assert (row.execution_state, row.result_state) == ("completed", "available")
    assert type(row.value) is results._Partition
    return {category.label: (category.count,
                            tuple(ref.identifier for ref in category.member_refs))
            for category in row.value.categories}


def disclosures(out, name):
    row = leaf(out, name)
    assert (row.execution_state, row.result_state) == ("completed", "available")
    assert type(row.value) is results._RecordDisclosures
    answer = {item.source.identifier: logical(item.fields)
              for item in row.value.records}
    assert len(answer) == len(row.value.records)
    return answer


def tokens(value):
    """Read a selected immutable disclosure without assuming incidental nesting."""
    if type(value) is dict:
        return [part for key, item in value.items()
                for part in [key, *tokens(item)]]
    if type(value) in (list, tuple):
        return [part for item in value for part in tokens(item)]
    return [value]


def reason_codes(row):
    return {reason.code for reason in row.reason_refs}


def test_vf054_to_vf057_have_only_the_four_registered_atomic_leaves():
    out, prepared, _, _ = run_profile()
    assert [(row.ref.field_key, row.value_kind) for row in out.results] == list(LEAVES)
    assert {row.ref.diagnostic_id for row in out.results} == {"SIT-M015"}
    assert prepared.input_state == "accepted"
    for row in out.results:
        assert row.execution_state == "completed"
        assert row.result_state == "available"
        assert row.interpretation_limit
        assert row.witness_refs == ()
        assert not hasattr(row, "provenance_quality")
        assert not hasattr(row, "verification_score")


def test_vf054_h7_retains_all_eight_separate_coverage_records():
    source = hero()
    out, _, _, _ = run_profile(source)
    rows = disclosures(out, "coverage_disclosures")
    assert set(rows) == set(H7_COVERAGE)
    # Each scope-bearing raw field is expected from its source, without using
    # the implementation's normalized or qualified output as an oracle.
    for identifier in H7_COVERAGE:
        original = cases.by_id(source, identifier)
        payload = rows[identifier]
        values = tokens(payload)
        for key in ("coverage_kind", "state", "universe_enumerated", "scope_note"):
            assert original["data"]["details"][key] in values
        for key in ("subject_refs",):
            assert all(member in values for member in original["data"][key])
        for key in ("relation_types", "dimensions", "member_refs", "omitted_refs"):
            assert key in values
            assert all(member in values for member in original["data"]["details"][key])
        assert original["provenance"]["basis_kind"] in values
        assert original["provenance"]["method"] in values
    assert "partial" in tokens(rows["H7-COV-MODEL"])
    assert "complete_for_scope" not in tokens(rows["H7-COV-MODEL"])
    assert "model_history" in tokens(rows["H7-COV-MODEL"])
    assert "upstream_history" in tokens(rows["H7-COV-ACQ"])
    assert "correction_routes" in tokens(rows["H7-COV-ROUTE"])


def test_vf056_h7_declared_basis_is_seven_named_relation_records():
    out, _, _, _ = run_profile()
    actual = partition(out, "declared_basis_inventory")
    assert set(actual) == set(BASIS)
    assert actual["documented_record"] == (7, H7_RECORDS)
    assert all(actual[label] == (0, ()) for label in BASIS if label != "documented_record")
    population = leaf(out, "declared_basis_inventory").value.population
    assert population.membership_state == "enumerated_for_scope"
    assert {member.identifier for member in population.member_refs} == set(H7_RECORDS)
    assert population.selection_rule


def test_vf057_h7_inventory_counts_eight_references_not_support_occurrences():
    out, _, _, _ = run_profile()
    actual = partition(out, "reference_availability_inventory")
    assert set(actual) == set(AVAILABILITY)
    assert actual["supplied"] == (8, H7_SUPPORT)
    assert all(actual[label] == (0, ()) for label in AVAILABILITY if label != "supplied")
    population = leaf(out, "reference_availability_inventory").value.population
    assert {member.identifier for member in population.member_refs} == set(H7_SUPPORT)


def test_fully_supplied_h7_basis_has_no_invented_documentary_gap_in_exact_acquisition_scope():
    out, _, _, _ = run_profile(context_changes={"dependency_dimension": "acquisition"})
    gaps = disclosures(out, "documentary_basis_gap_disclosures")
    for identifier in H7_RECORDS:
        reasons = tokens(gaps.get(identifier, {}))
        assert "documentary_basis_incomplete" not in reasons
        assert "support_uninspectable" not in reasons
        assert "scope_unestablished" not in reasons
    assert partition(out, "declared_basis_inventory")["documented_record"] == (7, H7_RECORDS)


@pytest.mark.parametrize("selected", ["records", "references", "coverage"])
def test_each_explicit_population_counts_duplicate_selected_ids_once(selected):
    params = {"record_refs": H7_RECORDS, "reference_refs": H7_SUPPORT,
              "coverage_refs": H7_COVERAGE}
    key = {"records": "record_refs", "references": "reference_refs",
           "coverage": "coverage_refs"}[selected]
    params[key] = params[key] + params[key][::-1] + params[key][:1]
    out, _, _, _ = run_profile(**params)
    assert partition(out, "declared_basis_inventory")["documented_record"] == (7, H7_RECORDS)
    assert partition(out, "reference_availability_inventory")["supplied"] == (8, H7_SUPPORT)
    assert set(disclosures(out, "coverage_disclosures")) == set(H7_COVERAGE)


def test_vf056_and_vf057_explicit_empty_populations_have_all_zero_categories():
    out, _, _, _ = run_profile(record_refs=(), reference_refs=(), coverage_refs=())
    assert partition(out, "declared_basis_inventory") == {label: (0, ()) for label in BASIS}
    assert partition(out, "reference_availability_inventory") == {label: (0, ()) for label in AVAILABILITY}
    assert disclosures(out, "coverage_disclosures") == {}
    assert disclosures(out, "documentary_basis_gap_disclosures") == {}
    for row in out.results:
        assert all(pop.membership_state == "enumerated_for_scope" for pop in row.population_refs)
        assert row.value_kind not in ("fraction", "completion_interval")


def test_vf056_all_five_declared_basis_categories_ignore_qualification_success():
    source = hero()
    for identifier, label in zip(H7_RECORDS[:5], BASIS):
        cases.by_id(source, identifier)["provenance"]["basis_kind"] = label
    out, _, _, _ = run_profile(source, record_refs=H7_RECORDS[:5])
    actual = partition(out, "declared_basis_inventory")
    assert {label: count for label, (count, _) in actual.items()} == {label: 1 for label in BASIS}
    assert sum(count for count, _ in actual.values()) == 5
    for identifier, label in zip(H7_RECORDS[:5], BASIS):
        assert actual[label][1] == (identifier,)


@pytest.mark.parametrize("availability", ("locator_only", "withheld", "unavailable"))
def test_vf055_support_gaps_preserve_all_seven_documentary_labels(availability):
    source = hero()
    support = cases.by_id(source, "H7-SUP-CHAIN")
    support.update(reference_kind="external_locator", availability=availability,
                   locator="https://example.invalid/fictional-uninspected", excerpt=None)
    out, prepared, _, _ = run_profile(source)
    assert prepared.input_state == "accepted"
    assert partition(out, "declared_basis_inventory")["documented_record"] == (7, H7_RECORDS)
    refs = partition(out, "reference_availability_inventory")
    assert refs[availability] == (1, ("H7-SUP-CHAIN",))
    assert refs["supplied"][0] == 7
    gaps = disclosures(out, "documentary_basis_gap_disclosures")
    for identifier in H7_RECORDS:
        assert identifier in gaps
        assert "documented_record" in tokens(gaps[identifier])
        assert "support_uninspectable" in tokens(gaps[identifier])


@pytest.mark.parametrize("missing", ("asserter", "method", "support"))
def test_vf055_independent_missing_documentary_members_are_reportable_gaps(missing):
    source = hero()
    row = cases.by_id(source, "H7-L01")
    if missing == "asserter":
        row["provenance"]["attributed_to_ref"] = None
        row["gaps"] = [{"field": "provenance.attributed_to_ref", "reason": "not_recorded",
                        "detail": "Fictional asserter was not supplied."}]
    elif missing == "method":
        row["provenance"]["method"] = None
        row["gaps"] = [{"field": "provenance.method", "reason": "not_recorded",
                        "detail": "Fictional method was not supplied."}]
    else:
        row["provenance"]["evidence_ref_ids"] = []
    out, prepared, _, _ = run_profile(source, record_refs=("H7-L01",))
    assert prepared.input_state == "accepted"
    assert partition(out, "declared_basis_inventory")["documented_record"] == (1, ("H7-L01",))
    payload = disclosures(out, "documentary_basis_gap_disclosures")["H7-L01"]
    assert "documented_record" in tokens(payload)
    assert "documentary_basis_incomplete" in tokens(payload)


def test_vf057_all_four_availability_states_are_exclusive_reference_records():
    source = hero()
    for identifier, availability in zip(H7_SUPPORT[:4], AVAILABILITY):
        if availability != "supplied":
            cases.by_id(source, identifier).update(
                reference_kind="external_locator", availability=availability,
                locator="https://example.invalid/fictional-reference", excerpt=None)
    out, _, _, _ = run_profile(source, reference_refs=H7_SUPPORT[:4])
    actual = partition(out, "reference_availability_inventory")
    assert {state: count for state, (count, _) in actual.items()} == {state: 1 for state in AVAILABILITY}
    for identifier, availability in zip(H7_SUPPORT[:4], AVAILABILITY):
        assert actual[availability][1] == (identifier,)


def test_vf057_visible_protected_attestation_and_withheld_material_stay_distinct():
    source = hero()
    visible = cases.by_id(source, "H7-SUP-CHAIN")
    visible.update(reference_kind="protected_attestation", attestor_ref="H7-PREP",
                   excerpt="A supplied protected attestation with bounded disclosed scope.")
    hidden = copy.deepcopy(visible)
    hidden.update(id="H7-SUP-HIDDEN", reference_kind="external_locator",
                  availability="withheld", attestor_ref=None, excerpt=None,
                  locator="https://example.invalid/withheld-underlying-material")
    source["evidence_references"].append(hidden)
    out, _, _, _ = run_profile(source, reference_refs=("H7-SUP-CHAIN", "H7-SUP-HIDDEN"))
    actual = partition(out, "reference_availability_inventory")
    assert actual["supplied"] == (1, ("H7-SUP-CHAIN",))
    assert actual["withheld"] == (1, ("H7-SUP-HIDDEN",))
    assert actual["locator_only"] == actual["unavailable"] == (0, ())


@pytest.mark.parametrize("shape", ("self_pointer", "closed_two_record_loop"))
def test_vf055_self_supporting_assurance_cannot_qualify_itself(shape):
    source = hero()
    first = cases.by_id(source, "H7-L01")
    second = cases.by_id(source, "H7-L02")
    pointer = copy.deepcopy(cases.by_id(source, "H7-SUP-CHAIN"))
    pointer.update(id="H7-POINTER-1", reference_kind="record_pointer",
                   record_ref="H7-L01" if shape == "self_pointer" else "H7-L02",
                   excerpt=None, artifact_ref=None, locator=None)
    source["evidence_references"].append(pointer)
    first["provenance"]["evidence_ref_ids"] = ["H7-POINTER-1"]
    if shape == "closed_two_record_loop":
        reverse = copy.deepcopy(pointer)
        reverse.update(id="H7-POINTER-2", record_ref="H7-L01")
        source["evidence_references"].append(reverse)
        second["provenance"]["evidence_ref_ids"] = ["H7-POINTER-2"]
    out, prepared, _, _ = run_profile(source, record_refs=("H7-L01",))
    assert prepared.input_state == "accepted"
    assert partition(out, "declared_basis_inventory")["documented_record"] == (1, ("H7-L01",))
    gap = disclosures(out, "documentary_basis_gap_disclosures")["H7-L01"]
    assert "self_supporting_assurance" in tokens(gap)
    assert "documented_record" in tokens(gap)


@pytest.mark.parametrize("relevant", (False, True))
def test_weak_denial_limits_its_exact_scope_without_erasing_inventory(relevant):
    source = hero()
    denial = copy.deepcopy(cases.by_id(source, "H7-L01"))
    denial["id"] = "ZZ-LATE-DENIAL"
    denial["data"]["polarity"] = "denied"
    denial["provenance"]["basis_kind"] = "declaration"
    denial["provenance"]["evidence_ref_ids"] = []
    if not relevant:
        other_inquiry = copy.deepcopy(source["inquiries"][0])
        other_inquiry["id"] = "H7-I-OTHER"
        other_inquiry["coverage_assertion_refs"] = []
        source["inquiries"].append(other_inquiry)
        denial["scope"]["inquiry_refs"] = ["H7-I-OTHER"]
    source["assertions"].append(denial)
    out, _, _, _ = run_profile(source, record_refs=("H7-L01",),
                               context_changes={"dependency_dimension": "acquisition"})
    assert partition(out, "declared_basis_inventory")["documented_record"] == (1, ("H7-L01",))
    gaps = disclosures(out, "documentary_basis_gap_disclosures")
    source_reasons = tokens(gaps.get("H7-L01", {}))
    assert ("premise_disputed" in source_reasons) is relevant


@pytest.mark.parametrize("lifecycle,polarity", (
    ("active", "affirmed"), ("active", "denied"),
    ("withdrawn", "affirmed"), ("superseded", "affirmed"),
))
def test_native_lifecycle_and_polarity_do_not_remove_declared_basis_members(lifecycle, polarity):
    source = hero()
    row = cases.by_id(source, "H7-L01")
    row["lifecycle_state"] = lifecycle
    row["lifecycle_basis_ref_ids"] = [] if lifecycle == "active" else ["H7-SUP-CHAIN"]
    row["data"]["polarity"] = polarity
    out, prepared, _, _ = run_profile(source, record_refs=("H7-L01",))
    assert partition(out, "declared_basis_inventory")["documented_record"] == (1, ("H7-L01",))
    retained = cases.by_id(logical(prepared.tree), "H7-L01")
    assert retained["lifecycle_state"] == lifecycle
    assert retained["data"]["polarity"] == polarity
    assert all(row.execution_state == "completed" for row in out.results)


@pytest.mark.parametrize("native", ("verified", "not_verified", "inconclusive", "revoked", "unknown"))
def test_source_verification_outcomes_never_set_tool_execution_or_quality(native):
    source = cases.rich()
    row = cases.by_id(source, "a-verification")
    row["data"]["details"]["reported_outcome"] = native
    row["provenance"]["basis_kind"] = "upstream_inference"
    out, prepared, _, _ = run_profile(source, record_refs=("a-verification",),
                                      reference_refs=("support",), coverage_refs=("a-coverage",))
    assert partition(out, "declared_basis_inventory")["upstream_inference"] == (1, ("a-verification",))
    retained = cases.by_id(logical(prepared.tree), "a-verification")
    assert retained["data"]["details"]["reported_outcome"] == native
    assert all((result.execution_state, result.result_state) == ("completed", "available")
               for result in out.results)
    assert all(result.result_origin in ("inventory", "attributed_record", "qualification_check")
               for result in out.results)


def test_native_failed_handling_remains_available_metadata_without_execution_failure():
    source = cases.pool()
    cases.by_id(source, "handling")["data"]["details"]["outcome"] = "failed"
    out, prepared, _, _ = run_profile(source, record_refs=("handling",),
                                      reference_refs=("support",), coverage_refs=())
    assert partition(out, "declared_basis_inventory")["declaration"] == (1, ("handling",))
    retained = cases.by_id(logical(prepared.tree), "handling")
    assert retained["data"]["details"]["outcome"] == "failed"
    assert all((result.execution_state, result.result_state) == ("completed", "available")
               for result in out.results)


def test_vf054_inconsistent_complete_label_keeps_omitted_branch_and_source_claim():
    source = hero()
    unresolved = cases.record("H7-UNKNOWN-BRANCH", "unresolved_reference", {
        "expected_kinds": ["evidence_item"], "reason": "not_recorded",
        "description": "A represented unknown acquisition branch.",
        "protected_key": "fictional-unresolved-branch"})
    unresolved["provenance"] = copy.deepcopy(source["inquiries"][0]["provenance"])
    source["records"].append(unresolved)
    coverage = cases.by_id(source, "H7-COV-ACQ")
    coverage["data"]["details"]["omitted_refs"] = ["H7-UNKNOWN-BRANCH"]
    out, _, _, _ = run_profile(source)
    payload = disclosures(out, "coverage_disclosures")["H7-COV-ACQ"]
    assert "complete_for_scope" in tokens(payload)
    assert "H7-UNKNOWN-BRANCH" in tokens(payload)
    assert "upstream_coverage_incomplete" in tokens(payload)
    assert partition(out, "declared_basis_inventory")["documented_record"] == (7, H7_RECORDS)


def test_source_mutation_and_input_order_cannot_change_selected_population_output():
    source = hero()
    reversed_source = copy.deepcopy(source)
    for name in ("records", "assertions", "evidence_references", "inquiries"):
        reversed_source[name].reverse()
    out, prepared, _, _ = run_profile(source)
    reordered, _, _, _ = run_profile(reversed_source, record_refs=H7_RECORDS[::-1],
                                    reference_refs=H7_SUPPORT[::-1], coverage_refs=H7_COVERAGE[::-1])
    for name in ("declared_basis_inventory", "reference_availability_inventory"):
        assert partition(out, name) == partition(reordered, name)
    for name in ("coverage_disclosures", "documentary_basis_gap_disclosures"):
        assert disclosures(out, name) == disclosures(reordered, name)
    source["assertions"].clear()
    assert partition(out, "declared_basis_inventory")["documented_record"] == (7, H7_RECORDS)
    assert prepared.entities
    with pytest.raises(FrozenInstanceError):
        out.results = ()
    with pytest.raises(FrozenInstanceError):
        out.results[0].value = None


def test_owner_local_metadata_never_fabricates_missing_pc03_or_pc04_execution():
    out, _, _, _ = run_profile()
    assert dict(report.PREREQUISITE_OWNERS)["PC03"] == "SOURCE_INVENTORY"
    assert dict(report.PREREQUISITE_OWNERS)["PC04"] == "GRAPH_VIEW_CONTRACT"
    for row in out.results:
        assert {"PC03", "PC04"} <= {check.check_id for check in row.check_refs}
        assert {"PC02", "PC24"} <= {check.check_id for check in row.check_refs}
        for check in row.check_refs:
            if check.check_id in ("PC03", "PC04"):
                assert check.state == "unknown"
                assert check.note
            if check.check_id in ("PC02", "PC24"):
                assert check.state == "met"


def test_explicit_trusted_provider_preconditions_do_not_change_declared_metadata():
    without, _, _, _ = run_profile()
    with_facts, _, _, _ = run_profile(with_providers=True)
    for name in ("declared_basis_inventory", "reference_availability_inventory"):
        assert partition(without, name) == partition(with_facts, name)
    for name in ("coverage_disclosures", "documentary_basis_gap_disclosures"):
        assert disclosures(without, name) == disclosures(with_facts, name)
    assert any(check.check_id == "PC03" and check.state == "met"
               for row in with_facts.results for check in row.check_refs)


def component_parts():
    source = hero()
    prepared = _prepare_value(source)
    assert type(prepared) is evidence._PreparedBundle
    return prepared, context(source)


def invoke(prepared, ctx, port, facts=()):
    return semantics._provenance_profile(
        prepared, ctx, H7_RECORDS, H7_SUPPORT, H7_COVERAGE, port,
        provider_facts=facts)


def trusted_fact(prepared, ctx, state="met"):
    addresses = tuple(evidence._SourceAddress("assertions", name) for name in H7_RECORDS)
    return evidence._ProviderFact("PC03", "SOURCE_INVENTORY", ctx, state, addresses, prepared)


def test_each_m015_job_prospectively_debits_one_shared_global_ledger():
    prepared, ctx = component_parts()
    budget = _new_analysis_budget()
    budget.record_input_acceptance()
    costs = []
    for _ in range(2):
        job = budget.start_job()
        before = (budget.used, job.used)
        out = invoke(prepared, ctx, job)
        delta = (budget.used - before[0], job.used - before[1])
        assert delta[0] == delta[1] and delta[0] > 0
        assert partition(out, "declared_basis_inventory")["documented_record"][0] == 7
        costs.append(delta[0])
        budget.finish_job(job)
    # Reusing only the admitted raw snapshot supplies no free semantic cache.
    assert costs[0] == costs[1]


@pytest.mark.parametrize("ceiling", ("job", "global"))
def test_mid_operation_budget_exhaustion_never_returns_a_completed_profile(ceiling):
    prepared, ctx = component_parts()
    budget = _new_analysis_budget()
    if ceiling == "global":
        budget.charge(9_998_475)  # The single prepaid reserve is already 1,024.
    budget.record_input_acceptance()
    job = budget.start_job()
    if ceiling == "job":
        job.charge(999_500)
    before = (budget.used, job.used)
    with pytest.raises(_AnalysisAborted) as stopped:
        invoke(prepared, ctx, job)
    assert stopped.value.stop.input_state == "accepted"
    assert stopped.value.stop.execution_state == "interrupted"
    assert stopped.value.stop.reason_code == "resource_limit_reached"
    assert stopped.value.limit_id == "WU9-L11"
    assert budget.used <= 10_000_000 and job.used <= 1_000_000
    assert budget.used - before[0] == job.used - before[1]
    assert budget.used > before[0]
    retained = (budget.used, job.used)
    with pytest.raises(_AnalysisAborted) as again:
        invoke(prepared, ctx, job)
    assert again.value is stopped.value
    assert (budget.used, job.used) == retained
    assert not hasattr(stopped.value, "results")


def test_previous_job_port_cannot_run_m015_after_another_job_starts():
    prepared, ctx = component_parts()
    budget = _new_analysis_budget()
    budget.record_input_acceptance()
    old = budget.start_job()
    assert partition(invoke(prepared, ctx, old), "declared_basis_inventory")["documented_record"][0] == 7
    budget.finish_job(old)
    current = budget.start_job()
    before = (budget.used, current.used)
    with pytest.raises(_AnalysisAborted) as stopped:
        invoke(prepared, ctx, old)
    assert stopped.value.stop.reason_code == "execution_failed"
    assert (budget.used, current.used) == before


def test_bounded_finalization_port_cannot_execute_m015_analysis():
    prepared, ctx = component_parts()
    budget = _new_analysis_budget()
    budget.record_input_acceptance()
    job = budget.start_job()
    assert partition(invoke(prepared, ctx, job), "declared_basis_inventory")["documented_record"][0] == 7
    budget.finish_job(job)
    finalizer = budget.begin_finalization()
    before = budget.used
    with pytest.raises(TypeError):
        invoke(prepared, ctx, finalizer)
    assert budget.used == before


@pytest.mark.parametrize("different", ("context", "snapshot", "wrong_type"))
def test_provider_facts_must_belong_to_this_exact_component_input(different):
    prepared, ctx = component_parts()
    fact = trusted_fact(prepared, ctx)
    budget = _new_analysis_budget()
    budget.record_input_acceptance()
    job = budget.start_job()
    valid = invoke(prepared, ctx, job, (fact,))
    assert any(check.check_id == "PC03" and check.state == "met"
               for row in valid.results for check in row.check_refs)
    budget.finish_job(job)
    job = budget.start_job()
    if different == "context":
        fact = trusted_fact(prepared, context(hero()))
    elif different == "snapshot":
        other_prepared = _prepare_value(hero())
        fact = trusted_fact(other_prepared, ctx)
    else:
        fact = ("PC03", "SOURCE_INVENTORY", "met")
    with pytest.raises(TypeError):
        invoke(prepared, ctx, job, (fact,))


def test_provider_owner_is_closed_and_cannot_be_reassigned_to_evidence_basis():
    prepared, ctx = component_parts()
    correct = trusted_fact(prepared, ctx)
    assert correct.owner == "SOURCE_INVENTORY"
    with pytest.raises(TypeError):
        evidence._ProviderFact("PC03", "EVIDENCE_BASIS", ctx, "met", (), prepared)
    with pytest.raises(TypeError):
        evidence._ProviderFact("PC04", "SOURCE_INVENTORY", ctx, "met", (), prepared)


@pytest.mark.parametrize("state", ("unmet", "unknown", "not_applicable"))
def test_nonmet_provider_fact_is_not_upgraded_by_available_metadata_inventory(state):
    prepared, ctx = component_parts()
    budget = _new_analysis_budget()
    budget.record_input_acceptance()
    out = invoke(prepared, ctx, budget.start_job(), (trusted_fact(prepared, ctx, state),))
    assert partition(out, "declared_basis_inventory")["documented_record"][0] == 7
    actual = [check for row in out.results for check in row.check_refs if check.check_id == "PC03"]
    assert actual and {check.state for check in actual} == {state}
