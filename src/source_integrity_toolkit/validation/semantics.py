# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: TEMPORAL_CONTRACT; supporting EVIDENCE_BASIS.

W05 input-only time validation under lineage section 3.1. No local timezone,
grant eligibility, event causality or conflict adjudication. Date precision is
retained as a date, never replaced by an assumed midnight instant. Mixed date /
instant window boundaries remain for their later owning analytical operation.
"""
from ..contracts.evidence import _InputObservation
from ..contracts.execution import _byte_work
from ..contracts.bundle import _compare_text
from .structure import _field


def _digits(text, start, stop, port):
    value = 0
    for i in range(start, stop):
        port.charge(2)
        ch = text[i]
        if not "0" <= ch <= "9":
            port.reject("invalid_time")
        value = value * 10 + ord(ch) - 48
    return value


def _date(text, port):
    port.charge(2)
    if len(text) < 10 or text[4] != "-" or text[7] != "-":
        port.reject("invalid_time")
    year, month, day = _digits(text, 0, 4, port), _digits(text, 5, 7, port), _digits(text, 8, 10, port)
    leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    months = (31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    if not 1 <= year <= 9999 or not 1 <= month <= 12 or not 1 <= day <= months[month - 1]:
        port.reject("invalid_time")
    prior = year - 1
    port.charge(25)
    ordinal = 365 * prior + prior // 4 - prior // 100 + prior // 400 + sum(months[:month - 1]) + day
    return ordinal


def _time_value(obj, port):
    state, text, precision = _field(obj, "state", port), _field(obj, "value", port), _field(obj, "precision", port)
    if state != "known":
        reason = _field(obj, "reason", port)
        if text is not None or precision is not None or type(reason) is not str or not reason:
            port.reject("invalid_time")
        return None
    if type(text) is not str or precision not in ("date", "instant"):
        port.reject("invalid_time")
    day = _date(text, port)
    if precision == "date":
        if len(text) != 10:
            port.reject("invalid_time")
        return ("date", day, "")
    if len(text) < 20 or text[10] != "T" or text[13] != ":" or text[16] != ":":
        port.reject("invalid_time")
    hour, minute, second = _digits(text, 11, 13, port), _digits(text, 14, 16, port), _digits(text, 17, 19, port)
    if hour > 23 or minute > 59 or second > 59:
        port.reject("invalid_time")
    i, fraction = 19, ""
    if text[i] == ".":
        i += 1
        start = i
        while i < len(text) and "0" <= text[i] <= "9":
            port.charge(2)
            i += 1
        if start == i:
            port.reject("invalid_time")
        end = i
        while end > start and text[end - 1] == "0":
            port.charge(2)
            end -= 1
        _byte_work(port, end - start, 1)
        fraction = text[start:end]
    offset = 0
    if i < len(text) and text[i] == "Z" and i + 1 == len(text):
        pass
    elif i + 6 == len(text) and text[i] in "+-" and text[i + 3] == ":":
        hours, minutes = _digits(text, i + 1, i + 3, port), _digits(text, i + 4, i + 6, port)
        if hours > 23 or minutes > 59:
            port.reject("invalid_time")
        offset = (hours * 3600 + minutes * 60) * (-1 if text[i] == "-" else 1)
    else:
        port.reject("invalid_time")
    port.charge(5)
    return ("instant", day * 86400 + hour * 3600 + minute * 60 + second - offset, fraction)


def _validate_semantics(occurrences, port):
    observations = []
    for shape, obj, owner, collection, prefix in occurrences:
        port.charge(1)
        if shape == "TimeValue":
            _time_value(obj, port)
        elif shape == "TimeWindow":
            start = _time_value(_field(obj, "start", port), port)
            end = _time_value(_field(obj, "end", port), port)
            # Only a same-precision, fully known inversion is observed. It is
            # accepted source data, not a structural failure or grant verdict.
            if start is not None and end is not None and start[0] == end[0]:
                port.charge(2)
                reverse = start[1] > end[1] or (start[1] == end[1] and _compare_text(start[2], end[2], port) > 0)
                if reverse:
                    identifier = _field(owner, "bundle_id" if collection == "bundle" else "id", port)
                    port.charge(3)
                    observations.append(_InputObservation("known_window_reversed", collection, identifier, prefix))
    port.charge(len(observations) + 1)
    result = tuple(observations)
    port.check()
    return result


# W06: finite observations only; these bindings do not evaluate any whole PC.
from ..contracts.bundle import _Object, _Array, _lookup_pair, _sorted_pairs
from ..contracts.report import (
    FACET_BINDINGS, COMMON_FACET_PATHS, ASSERTION_FACET_PATHS,
    DIRECT_SUBJECT_BINDINGS, FAMILIES, _SuppliedSelector, _InputFacet,
    _RecordEvidence, _BoundRecord,
)


def _observed_value(obj, path, port):
    # path comes only from the compiled recipe, never input expressions.
    port.charge(len(path) + 1)
    for name in path.split("."):
        port.charge(1)
        if type(obj) is not _Object:
            return False, None
        pair = _lookup_pair(obj.items, name, port)
        if pair is None:
            return False, None
        obj = pair[1]
    port.check()
    return True, obj


def _evidence_tag(entity, port):
    port.charge(1)
    if entity.collection != "assertions":
        return entity.kind
    obj = entity.node.fields
    if _field(obj, "assertion_kind", port) == "assessment":
        present, kind = _observed_value(obj, "data.assessment_kind", port)
        port.charge(40)
        return "assessment:" + kind
    present, predicate = _observed_value(obj, "data.predicate", port)
    if predicate in ("supports", "contradicts", "describes", "qualifies", "contextualizes", "corroborates"):
        return "relation:stance"
    if predicate in ("propagates_to", "same_identity_as"):
        port.charge(40)
        return "relation:" + predicate
    return "relation"


def _source_selector(entity, path, port):
    port.charge(5)
    return _SuppliedSelector(entity.collection, entity.identifier, path)


def _observe_record(entity, port):
    tag = _evidence_tag(entity, port)
    recipe = None
    for row in FACET_BINDINGS:
        port.charge(2)
        if tag == row[0]:
            recipe = row
            break
    if recipe is None:
        raise RuntimeError("unregistered_private_evidence_tag")
    tag, families, domains, questions, paths = recipe
    facets = []
    # EvidenceReference has its own attribution fields rather than Provenance.
    common = ("gaps",) if entity.collection == "evidence_references" else COMMON_FACET_PATHS
    envelope = ASSERTION_FACET_PATHS if entity.collection == "assertions" else ()
    for path in common + envelope + paths:
        present, value = _observed_value(entity.node.fields, path, port)
        qs = ("PC05", "PC08", "PC09") if path in common else ("PC02", "PC04", "PC09", "PC10") if path in envelope else questions
        port.charge(2 * len(qs) + 8)
        facets.append(_InputFacet(_source_selector(entity, path, port), present, value, qs))
    # Every source contributes an attributed-metadata slot, with no quality
    # upgrade. This is compiled navigation, not an input-supplied classifier.
    port.charge(len(families) + len(domains) + len(facets) + 10)
    fams = tuple(FAMILIES[i - 1] for i in families)
    if "SIT-M015" not in fams:
        fams += ("SIT-M015",)
    doms = domains if 1 in domains else domains + (1,)
    return _RecordEvidence(entity.collection, entity.identifier, fams, doms, tuple(facets))


def _id_membership(ids, port):
    """Paid sorted membership index; only navigation duplicates are removed."""
    pairs = []
    for identifier in ids:
        port.charge(2)
        pairs.append((identifier, None))
    port.charge(len(pairs) + 1)
    ordered = _sorted_pairs(tuple(pairs), port)
    result, previous = [], None
    for pair in ordered:
        port.charge(2)
        if previous is None or _compare_text(previous, pair[0], port) != 0:
            result.append(pair)
        previous = pair[0]
    port.charge(len(result) + 1)
    return tuple(result)


def _is_member(index, identifier, port):
    return _lookup_pair(index, identifier, port) is not None


def _direct_subject_selector(entity, selector, port):
    # Fixed field patterns, not arbitrary substring or URI interpretation.
    for kind, paths in DIRECT_SUBJECT_BINDINGS:
        port.charge(2)
        if entity.kind != kind:
            continue
        for path in paths:
            _byte_work(port, 4 * len(selector), 2)
            if selector == path or selector.startswith(path + "["):
                return True
    return False


def _observe_inquiry_bindings(prepared, plan, port):
    """A finite structural join, not a fixed-point walk.

    Stage A: inquiry and explicitly scoped assertions/anomalies.
    Stage B: their direct supplied field references.
    Stage C: record subject/target backlinks to A/B.
    Stage D: direct fields of records bound in A/B/C. No repeated expansion.
    Each inclusion retains its exact source selector. An assertion scoped only
    to another inquiry never becomes an assertion of this inquiry. All unbound
    records remain in the full snapshot catalog for later semantic work.
    """
    inquiry = plan.inquiry
    port.charge(len(plan.assertion_refs) + len(plan.anomaly_refs) + 3)
    scope_ids = _id_membership((inquiry.identifier,) + plan.assertion_refs + plan.anomaly_refs, port)
    bindings = [_BoundRecord(inquiry.identifier, _source_selector(inquiry, "id", port))]
    for entity in prepared.entities:
        port.charge(1)
        if entity.identifier == inquiry.identifier or not _is_member(scope_ids, entity.identifier, port):
            continue
        path = "scope.inquiry_refs" if entity.collection == "assertions" else "data.inquiry_refs"
        bindings.append(_BoundRecord(entity.identifier, _source_selector(entity, path, port)))
    for link in prepared.links:
        port.charge(1)
        if _is_member(scope_ids, link.owner.identifier, port):
            # Other Inquiry/Assertion scopes stay separate even when mentioned.
            if link.target.collection in ("inquiries", "assertions") and not _is_member(scope_ids, link.target.identifier, port):
                continue
            port.charge(4)
            bindings.append(_BoundRecord(link.target.identifier, _source_selector(link.owner, link.selector, port)))
    port.charge(len(bindings) + 1)
    direct = _id_membership(tuple(x.record_id for x in bindings), port)
    for link in prepared.links:
        port.charge(1)
        if _direct_subject_selector(link.owner, link.selector, port) and _is_member(direct, link.target.identifier, port):
            port.charge(4)
            bindings.append(_BoundRecord(link.owner.identifier, _source_selector(link.owner, link.selector, port)))
    port.charge(len(bindings) + 1)
    selected = _id_membership(tuple(x.record_id for x in bindings), port)
    for link in prepared.links:
        port.charge(1)
        if link.owner.collection != "records" or not _is_member(selected, link.owner.identifier, port):
            continue
        if link.target.collection in ("inquiries", "assertions") and not _is_member(scope_ids, link.target.identifier, port):
            continue
        port.charge(4)
        bindings.append(_BoundRecord(link.target.identifier, _source_selector(link.owner, link.selector, port)))
    port.charge(len(bindings) + 1)
    members = _id_membership(tuple(x.record_id for x in bindings), port)
    port.charge(len(bindings) + 1)
    return tuple(bindings), members


def _observe_evidence_input(prepared, port):
    """Only input selectors and finite direct bindings, never whole PC answers."""
    records = []
    for entity in prepared.entities:
        port.charge(1)
        records.append(_observe_record(entity, port))
    port.charge(len(records) + 1)
    snapshot = tuple(records)
    rows = []
    for plan in prepared.plan:
        bindings, members = _observe_inquiry_bindings(prepared, plan, port)
        selected = []
        for record in snapshot:
            port.charge(1)
            if _is_member(members, record.record_id, port):
                port.charge(1)
                selected.append(record)
        port.charge(len(selected) + len(bindings) + 3)
        rows.append((plan.inquiry.identifier, bindings, tuple(selected)))
    port.charge(len(rows) + 1)
    result = (snapshot, tuple(rows))
    port.check()
    return result
