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


# P3-W03: paid owner-local analysis. The preparation declarations above remain
# unchanged. These components inspect this admitted snapshot only; they neither
# authenticate the source nor execute future graph/population providers.
from ..contracts.bundle import _require, _freeze_object
from ..contracts.evidence import (
    _Node, _Entity, _PreparedBundle, _SourceAddress, _QualificationContext,
    _BasisQualification, _CoverageQualification, _TimeComparison,
    _TimeQualification, _ProviderFact,
)
from ..contracts import results as _results
from ..contracts.report import (
    _charge_frozen, _charge_scope, _charge_input_ref, _charge_link,
    _ScopeCheckFact, _PopulationCompletion, _ComponentCompletion,
    _CompletionRecord, _scope_check, _completion_check,
)


def _analysis_port(port):
    try:
        port.check_analysis()
    except AttributeError:
        raise TypeError('analysis_job_port_required') from None


def _analysis_text(text, port):
    _require(type(text) is str)
    _byte_work(port, 4 * len(text), 2)


def _analysis_lookup(prepared, identifier, port):
    _analysis_text(identifier, port)
    low, high = 0, len(prepared.entities)
    while low < high:
        port.charge(3)
        middle = (low + high) // 2
        entity = prepared.entities[middle]
        comparison = _compare_text(entity.identifier, identifier, port)
        if comparison < 0:
            low = middle + 1
        elif comparison > 0:
            high = middle
        else:
            return entity
    raise TypeError('unknown_private_source_reference')


def _analysis_ids(values, port):
    _require(type(values) is tuple)
    for value in values:
        _analysis_text(value, port)
    return _id_membership(values, port)


def _analysis_contains(values, identifier, port):
    for value in values:
        port.charge(1)
        if _compare_text(value, identifier, port) == 0:
            return True
    return False


def _analysis_subset(wanted, supplied, port):
    for identifier in wanted:
        port.charge(1)
        if not _analysis_contains(supplied, identifier, port):
            return False
    return True


def _analysis_start(prepared, context, port):
    _analysis_port(port)
    port.charge(3)
    _require(type(prepared) is _PreparedBundle and type(context) is _QualificationContext)
    inquiry = _analysis_lookup(prepared, context.inquiry_ref, port)
    _require(inquiry.collection == 'inquiries')
    for identifiers, kind in ((context.claim_refs, 'claim'), (context.subject_refs, None)):
        for identifier in identifiers:
            port.charge(1)
            entity = _analysis_lookup(prepared, identifier, port)
            _require(kind is None or entity.kind == kind)
    for texts in (context.relation_types,):
        for text in texts:
            _analysis_text(text, port)
    for text in (context.dependency_dimension, context.temporal_basis,
                 context.coverage_kind, context.graph_view):
        if text is not None:
            _analysis_text(text, port)
    for part in context.operation_anchor:
        port.charge(1)
        if type(part) is str:
            _analysis_text(part, port)
        elif type(part) is _SourceAddress:
            anchor_entity = _analysis_lookup(prepared, part.record_id, port)
            _require(anchor_entity.collection == part.collection)
            _analysis_text(part.selector, port)
    if context.requested_time is not None:
        _charge_frozen(context.requested_time.fields, port)
    return inquiry


def _analysis_address(entity, port, selector=''):
    port.charge(4)
    _analysis_text(entity.identifier, port)
    _analysis_text(selector, port)
    return _SourceAddress(entity.collection, entity.identifier, selector)


def _analysis_unique_addresses(addresses, port):
    # These are source IDs, not retained Finding occurrences. A source appears
    # once; every encountered edge/reference was still examined and charged.
    result = []
    for address in addresses:
        port.charge(1)
        found = False
        for previous in result:
            port.charge(2)
            if (_compare_text(previous.record_id, address.record_id, port) == 0 and
                    _compare_text(previous.selector, address.selector, port) == 0):
                found = True
                break
        if not found:
            port.charge(1)
            result.append(address)
    port.charge(len(result) + 1)
    return tuple(result)


def _analysis_codes(codes, port):
    result = []
    for code in codes:
        port.charge(len(result) + 2)
        if code not in result:
            result.append(code)
    port.charge(len(result) + 1)
    return tuple(result)


def _time_parts(node, port):
    port.charge(2)
    _require(type(node) is _Node and node.shape == 'TimeValue')
    # The parser is unchanged; this seam accepts already admitted TimeValues.
    # Invalid private parts are contract errors, not a new admission outcome.
    try:
        return _time_value(node.fields, port)
    except AttributeError:
        raise TypeError('invalid_private_time_value') from None


def _compare_times(left, right, port):
    """Compare retained native precision, with exact timezone/fraction math."""
    _analysis_port(port)
    a, b = _time_parts(left, port), _time_parts(right, port)
    port.charge(8)
    reasons = ()
    if a is None or b is None or a[0] != b[0]:
        comparison = 'unknown'
    elif a[1] < b[1]:
        comparison = 'before'
    elif a[1] > b[1]:
        comparison = 'after'
    elif a[0] == 'date':
        comparison = 'overlap'
    else:
        order = _compare_text(a[2], b[2], port)
        comparison = 'before' if order < 0 else 'after' if order > 0 else 'equal'
    if comparison in ('unknown', 'overlap'):
        reasons = ('time_applicability_unknown',)
    port.charge(12)
    result = _TimeComparison(comparison, reasons, (left, right))
    port.check()
    return result


def _time_applicability(window, requested, port):
    """Strict interior/exterior only: the source specifies no endpoint rule."""
    _analysis_port(port)
    port.charge(3)
    _require(type(window) is _Node and window.shape == 'TimeWindow')
    start = _Node('TimeValue', _field(window.fields, 'start', port))
    end = _Node('TimeValue', _field(window.fields, 'end', port))
    bounds = _compare_times(start, end, port)
    lower, upper = _compare_times(requested, start, port), _compare_times(requested, end, port)
    if bounds.comparison == 'after':
        state, reasons = 'unmet', ('temporal_inconsistency',)
    elif lower.comparison == 'before' or upper.comparison == 'after':
        state, reasons = 'unmet', ('time_applicability_unknown',)
    elif lower.comparison == 'after' and upper.comparison == 'before':
        state, reasons = 'met', ()
    else:
        state, reasons = 'unknown', ('time_applicability_unknown',)
    port.charge(14)
    result = _TimeQualification(state, reasons, None, (start, end, requested))
    port.check()
    return result


def _analysis_scope(entity, context, port, *, subjects=True, relation_types=True):
    """Exact input IDs, never Claim-key/version or empty-scope expansion."""
    if entity.collection != 'assertions':
        return True
    scope = _field(entity.node.fields, 'scope', port)
    inquiries = _field(scope, 'inquiry_refs', port).items
    claims = _field(scope, 'claim_refs', port).items
    if (not _analysis_contains(inquiries, context.inquiry_ref, port) or
            (bool(context.claim_refs) != bool(claims)) or
            not _analysis_subset(context.claim_refs, claims, port)):
        return False
    data = _field(entity.node.fields, 'data', port)
    if _field(entity.node.fields, 'assertion_kind', port) == 'relation':
        dimension = _field(data, 'dimension', port)
        if dimension is not None and dimension != context.dependency_dimension:
            return False
        if relation_types and context.relation_types and not _analysis_contains(
                context.relation_types, _field(data, 'predicate', port), port):
            return False
        if subjects and context.subject_refs:
            endpoints = (_field(data, 'from_ref', port), _field(data, 'to_ref', port))
            if not _analysis_subset(context.subject_refs, endpoints, port):
                return False
    else:
        details = _field(data, 'details', port)
        dimension = _lookup_pair(details.items, 'dimension', port)
        if dimension is not None and dimension[1] is not None and dimension[1] != context.dependency_dimension:
            return False
        kind = _field(data, 'assessment_kind', port)
        if subjects and context.subject_refs and kind not in ('coverage', 'conflict'):
            if not _analysis_subset(context.subject_refs, _field(data, 'subject_refs', port).items, port):
                return False
    return True


def _analysis_temporal(entity, context, port):
    if entity.collection != 'assertions' or context.temporal_basis == 'snapshot_structural':
        port.charge(1)
        return None
    scope = _field(entity.node.fields, 'scope', port)
    window = _Node('TimeWindow', _field(scope, 'effective_window', port))
    return _time_applicability(window, context.requested_time, port)


def _analysis_native(entity, port):
    provenance = _field(entity.node.fields, 'provenance', port)
    return provenance, _field(provenance, 'basis_kind', port)


def _analysis_attributor(prepared, identifier, port, *, protected=False):
    if identifier is None:
        return False
    entity = _analysis_lookup(prepared, identifier, port)
    if entity.kind in ('actor', 'model'):
        return True
    if protected and entity.kind == 'unresolved_reference':
        data = _field(entity.node.fields, 'data', port)
        key = _lookup_pair(data.items, 'protected_key', port)
        if key is not None and key[1] is not None:
            _analysis_text(key[1], port)
        protected_identity = (key is not None and bool(key[1])) or _field(data, 'reason', port) == 'withheld'
        expected = _field(data, 'expected_kinds', port).items
        return protected_identity and (_analysis_contains(expected, 'actor', port) or
                                       _analysis_contains(expected, 'model', port))
    return False


def _analysis_current(prepared, entity, port):
    """A lifecycle label alone cannot erase a contradictory source assertion.

    Return current-or-uncertain when its status basis has no inspectable
    material. This only controls retention; it does not establish PC04.
    """
    if _field(entity.node.fields, 'lifecycle_state', port) == 'active':
        return True, False
    references = _field(entity.node.fields, 'lifecycle_basis_ref_ids', port).items
    port.charge(len(references) + 2)
    stack = [(identifier, (entity.identifier,)) for identifier in references]
    inspected = False
    while stack:
        port.charge(3)
        identifier, path = stack.pop()
        reference = _analysis_lookup(prepared, identifier, port)
        obj = reference.node.fields
        if _field(obj, 'availability', port) != 'supplied':
            continue
        kind = _field(obj, 'reference_kind', port)
        if kind == 'supplied_excerpt':
            excerpt = _field(obj, 'excerpt', port)
            _analysis_text(excerpt, port)
            inspected = bool(excerpt) or inspected
        elif kind == 'protected_attestation':
            excerpt, artifact = _field(obj, 'excerpt', port), _field(obj, 'artifact_ref', port)
            if excerpt is not None:
                _analysis_text(excerpt, port)
            material = bool(excerpt)
            if artifact is not None:
                material = material or _analysis_lookup(prepared, artifact, port).kind == 'artifact'
            if material and _analysis_attributor(prepared, _field(obj, 'attestor_ref', port), port, protected=True):
                inspected = True
        elif kind == 'record_pointer':
            target = _analysis_lookup(prepared, _field(obj, 'record_ref', port), port)
            if _analysis_contains(path, target.identifier, port) or target.kind == 'unresolved_reference':
                continue
            if target.collection != 'assertions':
                inspected = True
            else:
                prov = _field(target.node.fields, 'provenance', port)
                children = _field(prov, 'evidence_ref_ids', port).items
                port.charge(len(path) + len(children) + 2)
                next_path = path + (target.identifier,)
                for child in children:
                    port.charge(2)
                    stack.append((child, next_path))
    return not inspected, not inspected


def _qualify_basis(prepared, record_ref, context, port):
    """PC05 documentary material, without substituting for PC04 eligibility.

    Assurance Assertion pointers are followed only to determine whether a sole
    closed loop has independent supplied material. An ordinary supplied record
    can be material without recursively proving the entire record universe.
    """
    _analysis_start(prepared, context, port)
    root = _analysis_lookup(prepared, record_ref, port)
    _require(root.collection != 'evidence_references')
    provenance, label = _analysis_native(root, port)
    codes, supports, notes = [], [], ['Attributed documentary support only; no authentication or positive-edge eligibility.']
    if not _analysis_scope(root, context, port):
        codes.append('scope_unestablished')
    timing = _analysis_temporal(root, context, port)
    if timing is not None and timing.state != 'met':
        codes.extend(timing.reason_codes)
    attributed = _field(provenance, 'attributed_to_ref', port)
    identified = _analysis_attributor(prepared, attributed, port)
    method = _field(provenance, 'method', port)
    initial = _field(provenance, 'evidence_ref_ids', port).items
    port.charge(len(initial) + 4)
    stack = [(identifier, (root.identifier,)) for identifier in initial]
    independent, loop, protected_attributor = False, False, False
    while stack:
        port.charge(3)
        identifier, path = stack.pop()
        reference = _analysis_lookup(prepared, identifier, port)
        _require(reference.collection == 'evidence_references')
        supports.append(_analysis_address(reference, port))
        obj = reference.node.fields
        kind, availability = _field(obj, 'reference_kind', port), _field(obj, 'availability', port)
        if availability != 'supplied':
            port.charge(1)
            continue
        if kind == 'supplied_excerpt':
            excerpt = _field(obj, 'excerpt', port)
            _analysis_text(excerpt, port)
            independent = bool(excerpt) or independent
        elif kind == 'protected_attestation':
            attestor = _field(obj, 'attestor_ref', port)
            excerpt = _field(obj, 'excerpt', port)
            artifact = _field(obj, 'artifact_ref', port)
            visible = False
            if excerpt is not None:
                _analysis_text(excerpt, port)
                visible = bool(excerpt)
            if artifact is not None:
                item = _analysis_lookup(prepared, artifact, port)
                visible = visible or item.kind == 'artifact'
            if visible and _analysis_attributor(prepared, attestor, port, protected=True):
                independent, protected_attributor = True, True
                notes.append('Visible protected attestation does not expose or verify underlying withheld material.')
        elif kind == 'record_pointer':
            target = _analysis_lookup(prepared, _field(obj, 'record_ref', port), port)
            if _analysis_contains(path, target.identifier, port):
                loop = True
                continue
            if target.kind == 'unresolved_reference':
                continue
            supports.append(_analysis_address(target, port))
            if target.collection == 'assertions':
                prov = _field(target.node.fields, 'provenance', port)
                references = _field(prov, 'evidence_ref_ids', port).items
                port.charge(len(path) + len(references) + 2)
                next_path = path + (target.identifier,)
                for child in references:
                    port.charge(2)
                    stack.append((child, next_path))
            else:
                # The pointed-to structured record itself was supplied; no
                # ancestry or truth claim is inferred from its own provenance.
                independent = True
        # local/external locators stay inert even when labelled supplied.
    if not identified and not protected_attributor or not method or not initial:
        codes.append('documentary_basis_incomplete')
    if not independent:
        codes.append('support_uninspectable')
    if loop:
        codes.append('self_supporting_assurance')
        notes.append('The historical assurance loop remains disclosed alongside any independent supplied material.')
    if root.collection == 'assertions':
        lifecycle = _field(root.node.fields, 'lifecycle_state', port)
        _analysis_text(lifecycle, port)
        notes.append('Lifecycle and relation polarity are retained; documentary qualification does not make a current positive premise.')
    for note in _field(provenance, 'qualifications', port).items:
        _analysis_text(note, port)
        port.charge(1)
        notes.append(note)
    reasons = _analysis_codes(codes, port)
    port.charge(len(reasons) + 1)
    blockers = tuple(code for code in reasons if code != 'self_supporting_assurance')
    port.charge(len(reasons) + len(notes) + 14)
    for note in notes:
        _analysis_text(note, port)
    result = _BasisQualification(_analysis_address(root, port), label,
        'met' if independent and not blockers else 'unmet', reasons,
        _analysis_unique_addresses(supports, port), tuple(notes), context)
    port.check()
    return result


def _qualify_conflicts(prepared, record_ref, context, port):
    """Relevant supplied contradiction, not a classifier or adjudication."""
    _analysis_start(prepared, context, port)
    root = _analysis_lookup(prepared, record_ref, port)
    _require(root.collection != 'evidence_references')
    provenance, label = _analysis_native(root, port)
    codes, supports = [], []
    if not _analysis_scope(root, context, port):
        codes.append('scope_unestablished')
    root_relation = root.collection == 'assertions' and _field(root.node.fields, 'assertion_kind', port) == 'relation'
    root_data = _field(root.node.fields, 'data', port) if root.collection == 'assertions' else None
    for candidate in prepared.entities:
        port.charge(2)
        if candidate.collection != 'assertions' or candidate is root:
            continue
        obj = candidate.node.fields
        current, status_uncertain = _analysis_current(prepared, candidate, port)
        if not current or not _analysis_scope(candidate, context, port, subjects=False):
            continue
        timing = _analysis_temporal(candidate, context, port)
        if timing is not None and timing.state == 'unmet' and 'temporal_inconsistency' not in timing.reason_codes:
            continue
        data = _field(obj, 'data', port)
        kind = _field(obj, 'assertion_kind', port)
        disputed = False
        if kind == 'relation' and root_relation:
            same = True
            for key in ('predicate', 'from_ref', 'to_ref', 'dimension'):
                left, right = _field(root_data, key, port), _field(data, key, port)
                port.charge(1)
                if (left is None) != (right is None) or left is not None and _compare_text(left, right, port) != 0:
                    same = False
            disputed = same and _field(root_data, 'polarity', port) != _field(data, 'polarity', port)
        elif kind == 'assessment' and _field(data, 'assessment_kind', port) == 'conflict':
            disputed = _analysis_contains(_field(data, 'subject_refs', port).items, root.identifier, port)
        if disputed:
            port.charge(2)
            codes.append('premise_disputed')
            if status_uncertain:
                codes.append('documentary_basis_incomplete')
            if timing is not None and timing.state != 'met':
                codes.extend(timing.reason_codes)
            supports.append(_analysis_address(candidate, port))
    reasons = _analysis_codes(codes, port)
    port.charge(14)
    result = _BasisQualification(_analysis_address(root, port), label,
        'unmet' if reasons else 'met', reasons, _analysis_unique_addresses(supports, port),
        ('Only current exact-scope supplied conflicts are considered; weak denials remain relevant and no winner is selected.',), context)
    port.check()
    return result


def _qualify_identity(prepared, subject_refs, context, port):
    """Opaque/shared/alias identity is preserved, never canonicalized."""
    _analysis_start(prepared, context, port)
    subjects = _analysis_ids(subject_refs, port)
    supports, codes = [], []
    for identifier, unused in subjects:
        entity = _analysis_lookup(prepared, identifier, port)
        if entity.kind == 'unresolved_reference':
            codes.append('identity_unresolved')
            supports.append(_analysis_address(entity, port))
    for entity in prepared.entities:
        port.charge(1)
        if entity.collection != 'assertions':
            continue
        current, status_uncertain = _analysis_current(prepared, entity, port)
        if not current:
            continue
        if not _analysis_scope(entity, context, port, subjects=False, relation_types=False):
            continue
        timing = _analysis_temporal(entity, context, port)
        if timing is not None and timing.state == 'unmet' and 'temporal_inconsistency' not in timing.reason_codes:
            continue
        data = _field(entity.node.fields, 'data', port)
        if (_field(entity.node.fields, 'assertion_kind', port) == 'relation' and
                _field(data, 'predicate', port) == 'same_identity_as'):
            for name in ('from_ref', 'to_ref'):
                if _is_member(subjects, _field(data, name, port), port):
                    codes.append('identity_unresolved')
                    if status_uncertain:
                        codes.append('documentary_basis_incomplete')
                    if timing is not None and timing.state != 'met':
                        codes.extend(timing.reason_codes)
                    supports.append(_analysis_address(entity, port))
                    break
    source = _analysis_lookup(prepared, subjects[0][0] if subjects else context.inquiry_ref, port)
    reasons = _analysis_codes(codes, port)
    port.charge(14)
    result = _BasisQualification(_analysis_address(source, port), 'unspecified',
        'unmet' if reasons else 'met', reasons, _analysis_unique_addresses(supports, port),
        ('Identity qualification is limited to the named subjects; aliases never merge records.',), context)
    port.check()
    return result


def _qualify_coverage(prepared, coverage_refs, context, port):
    """Retain each native coverage declaration beside its finite qualification."""
    _analysis_start(prepared, context, port)
    results = []
    for identifier, unused in _analysis_ids(coverage_refs, port):
        entity = _analysis_lookup(prepared, identifier, port)
        obj = entity.node.fields
        _require(entity.collection == 'assertions' and _field(obj, 'assertion_kind', port) == 'assessment')
        data = _field(obj, 'data', port)
        _require(_field(data, 'assessment_kind', port) == 'coverage')
        details = _field(data, 'details', port)
        basis = _qualify_basis(prepared, identifier, context, port)
        conflict = _qualify_conflicts(prepared, identifier, context, port)
        port.charge(len(basis.reason_codes) + len(conflict.reason_codes) + 3)
        codes = list(basis.reason_codes + conflict.reason_codes)
        incomplete = (_field(obj, 'lifecycle_state', port) != 'active' or
                      _field(details, 'state', port) != 'complete_for_scope' or
                      _field(details, 'coverage_kind', port) != context.coverage_kind or
                      not _field(details, 'universe_enumerated', port) or
                      bool(_field(details, 'omitted_refs', port).items))
        dimensions = _field(details, 'dimensions', port).items
        if context.dependency_dimension is None and len(dimensions) > 1:
            codes.append('scope_unestablished')
            incomplete = True
        if context.dependency_dimension is not None and not _analysis_contains(dimensions, context.dependency_dimension, port):
            incomplete = True
        if not _analysis_subset(context.relation_types, _field(details, 'relation_types', port).items, port):
            incomplete = True
        members = _field(details, 'member_refs', port).items
        subjects = _field(data, 'subject_refs', port).items
        if (not _analysis_subset(context.subject_refs, members, port) or
                not (_analysis_subset(context.subject_refs, subjects, port) or
                     _analysis_contains(subjects, context.inquiry_ref, port))):
            incomplete = True
        for member in members:
            candidate = _analysis_lookup(prepared, member, port)
            if candidate.kind == 'unresolved_reference':
                incomplete = True
        # Direct raw-source contradiction to a claimed finite area, not a
        # graph traversal or a substitution for the later PC04 provider.
        # No named predicates means no relationship-world query: identity or
        # pipeline member inventories can legitimately name an empty set.
        port.charge(1)
        for candidate in prepared.entities if context.relation_types else ():
            port.charge(1)
            if candidate.collection != 'assertions' or _field(candidate.node.fields, 'assertion_kind', port) != 'relation':
                continue
            current, uncertain = _analysis_current(prepared, candidate, port)
            if not current or not _analysis_scope(candidate, context, port, subjects=False):
                continue
            timing = _analysis_temporal(candidate, context, port)
            if timing is not None and timing.state == 'unmet' and 'temporal_inconsistency' not in timing.reason_codes:
                continue
            relation = _field(candidate.node.fields, 'data', port)
            if (_field(relation, 'polarity', port) == 'affirmed' and
                    _analysis_contains(members, _field(relation, 'from_ref', port), port)):
                target = _field(relation, 'to_ref', port)
                if (not _analysis_contains(members, target, port) or
                        _analysis_lookup(prepared, target, port).kind == 'unresolved_reference'):
                    incomplete = True
        if incomplete:
            codes.append('upstream_coverage_incomplete')
        reasons = _analysis_codes(codes, port)
        blocked = incomplete or basis.state != 'met' or conflict.state != 'met'
        port.charge(18)
        results.append(_CoverageQualification(_analysis_address(entity, port),
            'unmet' if blocked else 'met', reasons, basis.support_refs,
            ('Completeness is attributed only to the exact supplied kind, subjects, predicates, dimension and finite member area.',),
            entity, context))
    port.charge(len(results) + 1)
    output = tuple(results)
    port.check()
    return output


def _profile_ref(entity, port, selector=None):
    port.charge(5)
    _analysis_text(entity.identifier, port)
    if selector is not None:
        _analysis_text(selector, port)
    return _results._InputRef(entity.collection, entity.identifier, selector)


def _profile_selection(prepared, identifiers, port, *, references=False, coverage=False):
    selected = []
    for identifier, unused in _analysis_ids(identifiers, port):
        entity = _analysis_lookup(prepared, identifier, port)
        _require((entity.collection == 'evidence_references') == references)
        if coverage:
            _require(entity.collection == 'assertions' and
                     _field(entity.node.fields, 'assertion_kind', port) == 'assessment' and
                     _field(_field(entity.node.fields, 'data', port), 'assessment_kind', port) == 'coverage')
        port.charge(1)
        selected.append(entity)
    port.charge(len(selected) + 1)
    return tuple(selected)


def _profile_context(entity, context, port):
    """A metadata inventory may name records across distinct native areas.

    Examine each named record in its own declared area when the inventory did
    not select a dimension/kind/predicate. This never establishes a combined
    graph or completeness area. The returned local context remains attached
    to its qualifications, beside the original scope-bearing disclosure.
    """
    if entity.collection != 'assertions':
        return context
    data = _field(entity.node.fields, 'data', port)
    dimension, predicates, kind = context.dependency_dimension, context.relation_types, context.coverage_kind
    if _field(entity.node.fields, 'assertion_kind', port) == 'relation':
        if dimension is None:
            dimension = _field(data, 'dimension', port)
        if not predicates:
            predicates = (_field(data, 'predicate', port),)
    elif _field(data, 'assessment_kind', port) == 'coverage':
        details = _field(data, 'details', port)
        if kind is None:
            kind = _field(details, 'coverage_kind', port)
        dimensions = _field(details, 'dimensions', port).items
        if dimension is None and len(dimensions) == 1:
            dimension = dimensions[0]
        if not predicates:
            predicates = _field(details, 'relation_types', port).items
    else:
        details = _field(data, 'details', port)
        native_dimension = _lookup_pair(details.items, 'dimension', port)
        if dimension is None and native_dimension is not None:
            dimension = native_dimension[1]
    for texts in (context.claim_refs, context.subject_refs, predicates):
        port.charge(len(texts) * len(texts) + 2 * len(texts) + 1)
        for text in texts:
            for _ in range(len(texts) + 3):
                _analysis_text(text, port)
    for part in context.operation_anchor:
        port.charge(1)
        if type(part) is str:
            _analysis_text(part, port)
        elif type(part) is _SourceAddress:
            for text in (part.collection, part.record_id, part.selector):
                _analysis_text(text, port)
    port.charge(30)
    return _QualificationContext(context.inquiry_ref, context.claim_refs, context.subject_refs,
        dimension, context.temporal_basis, context.requested_time, kind, predicates,
        context.graph_view, context.operation_anchor)


def _profile_providers(prepared, context, provider_facts, port):
    _require(type(provider_facts) is tuple)
    validated = []
    for fact in provider_facts:
        port.charge(5)
        _require(type(fact) is _ProviderFact and fact.prepared is prepared and fact.context is context)
        _require((fact.check_id, fact.owner) in (('PC03', 'SOURCE_INVENTORY'), ('PC04', 'GRAPH_VIEW_CONTRACT')))
        for old, unused in validated:
            port.charge(1)
            _require(old.check_id != fact.check_id)
        refs = []
        for source in fact.input_refs:
            entity = _analysis_lookup(prepared, source.record_id, port)
            _require(entity.collection == source.collection)
            refs.append(_profile_ref(entity, port, source.selector or None))
        port.charge(len(refs) + 2)
        validated.append((fact, tuple(refs)))
    port.charge(len(validated) + 1)
    return tuple(validated)


def _profile_scope(prepared, context, port):
    inquiry = _profile_ref(_analysis_lookup(prepared, context.inquiry_ref, port), port)
    claims, targets, anchor = [], [], []
    for identifiers, result in ((context.claim_refs, claims), (context.subject_refs, targets)):
        for identifier in identifiers:
            result.append(_profile_ref(_analysis_lookup(prepared, identifier, port), port))
    for part in context.operation_anchor:
        port.charge(2)
        if type(part) is _SourceAddress:
            part = _profile_ref(_analysis_lookup(prepared, part.record_id, port), port, part.selector or None)
        anchor.append(part)
    # Constructor scope validation hashes source IDs and copies bounded tuples.
    for refs in (claims, targets):
        port.charge(len(refs) * len(refs) + len(refs) + 1)
        for ref in refs:
            _charge_input_ref(ref, port, repeats=len(refs) + 3)
    port.charge(len(anchor) + 16)
    scope = _results._Scope(inquiry, tuple(claims), tuple(targets), context.dependency_dimension,
        context.graph_view, context.temporal_basis, context.requested_time, (),
        ('Explicit named metadata population only; omitted dimensions/views are not generalized.',), tuple(anchor))
    _charge_scope(scope, port)
    return scope


def _profile_population(scope, entities, unit, selection, port):
    refs = []
    for entity in entities:
        refs.append(_profile_ref(entity, port))
    for ref in refs:
        _charge_input_ref(ref, port, repeats=3)
    port.charge(len(refs) * len(refs) + len(refs) + 12)
    return _results._Population(scope, unit, tuple(refs), selection,
        qualifications=('Each explicit source ID is counted once; this is not a claim that the external universe is complete.',))


def _profile_disclosure(entity, qualification, extra_codes, port, *, coverage=False):
    obj = entity.node.fields
    fields = []
    paths = ('data', 'scope', 'provenance', 'lifecycle_state') if coverage else ('provenance',)
    for name in paths:
        value = _field(obj, name, port)
        # The original bounded immutable value is retained; charge the full
        # validation/copy pass before including it in the new field bag.
        _charge_frozen(value, port)
        fields.append((name, value))
    gap = _lookup_pair(obj.items, 'gaps', port)
    if gap is not None:
        _charge_frozen(gap[1], port)
        fields.append(('gaps', gap[1]))
    reasons = _analysis_codes(qualification.reason_codes + extra_codes, port)
    port.charge(len(reasons) + 6)
    fields.extend((('qualification_state', qualification.state), ('reason_codes', _Array(reasons))))
    frozen = _freeze_object(fields, port)
    for _ in range(3):
        _charge_frozen(frozen, port)
    port.charge(10)
    return _results._Disclosure(_profile_ref(entity, port), frozen, qualification.qualifications)


def _profile_partition(population, entities, labels, field, port):
    categories = []
    for label in labels:
        members = []
        for entity, ref in zip(entities, population.member_refs):
            port.charge(2)
            obj = entity.node.fields
            if field == 'basis_kind':
                obj = _field(obj, 'provenance', port)
            if _compare_text(_field(obj, field, port), label, port) == 0:
                _charge_input_ref(ref, port, repeats=4)
                port.charge(1)
                members.append(ref)
        port.charge(len(members) + 8)
        categories.append(_results._PartitionCategory(label, tuple(members), len(members)))
    for ref in population.member_refs:
        _charge_input_ref(ref, port, repeats=8)
    port.charge(len(population.member_refs) * 8 + len(categories) + 12)
    return _results._Partition(population, tuple(categories))


def _profile_result(scope, field, population, value, providers, qualifications, port):
    """Commit one completed local metadata leaf with its own PC02/PC24."""
    port.charge(160)  # Registered field lookup and fixed representation checks.
    ref = _results._ResultRef('SIT-M015', field, scope)
    checks = [_scope_check(_ScopeCheckFact(ref, scope), port)]
    for check_id, owner in (('PC03', 'SOURCE_INVENTORY'), ('PC04', 'GRAPH_VIEW_CONTRACT')):
        selected = None
        for fact, sources in providers:
            port.charge(1)
            if fact.check_id == check_id:
                selected = (fact, sources)
        if selected is None:
            state, sources = 'unknown', ()
            note = 'No provider fact supplied: ' + owner + ' has not executed here; only named metadata is inventoried.'
        else:
            fact, sources = selected
            state = fact.state
            note = 'Explicit trusted component fact from ' + owner + '; this component does not execute that provider.'
            for source in sources:
                _charge_input_ref(source, port, repeats=len(sources) + 3)
        _analysis_text(note, port)
        port.charge(12)
        checks.append(_results._PrerequisiteCheck(check_id, ref, state, sources, (), note))
    reasons, basis_refs = [], []
    for qualification in qualifications:
        port.charge(1)
        for text in (qualification.source.collection, qualification.source.record_id,
                     qualification.source.selector):
            _analysis_text(text, port)
        port.charge(5)
        source = _results._InputRef(qualification.source.collection, qualification.source.record_id,
                                    qualification.source.selector or None)
        _charge_input_ref(source, port, repeats=8)
        basis_refs.append(_results._BasisRef(source))
        for code in qualification.reason_codes:
            # Reason construction compares one affected result scope and
            # creates/hashes its key: three whole scope passes.
            for _ in range(3):
                _charge_scope(scope, port)
            _charge_input_ref(source, port, repeats=4)
            port.charge(16)
            reasons.append(_results._Reason(code, scope, (ref,), (source,),
                'The attributed named record retains this local qualification; its native inventory label is unchanged.',
                'conflict' if code == 'premise_disputed' else 'evidence_gap'))
    # All selected members, qualifying premises, relevant conflicts and values
    # were processed before this point. No graph/provider work is represented
    # by this completion record, and an interrupted scan never reaches it.
    components = []
    for name, links in (('premises', population.member_refs), ('conflicts', tuple(reasons)),
                        ('value', (ref,)), ('basis', tuple(basis_refs)),
                        ('reasons', tuple(reasons)), ('witnesses', ())):
        for link in links:
            for _ in range(3):
                _charge_link(link, port)
        port.charge(len(links) * len(links) + 10)
        components.append(_ComponentCompletion(name, links, links))
    for _ in range(3):
        _charge_link(population, port)
    port.charge(24)
    completion = _CompletionRecord(ref, (population,),
        (_PopulationCompletion(population, population.member_refs),), tuple(components))
    checks.append(_completion_check(completion, port))
    # Result construction makes and hashes each population/check/reason key
    # once; two full passes cover those operations without pretending that
    # eight complete re-evaluations took place.
    for _ in range(2):
        _charge_link(ref, port)
        _charge_link(population, port)
        for link in checks + basis_refs + reasons:
            _charge_link(link, port)
    port.charge(len(checks) + len(basis_refs) + len(reasons) + 32)
    result = _results._Result(ref, (population,), 'completed', 'available',
        'inventory' if field.endswith('_inventory') else 'attributed_record',
        'partition' if field.endswith('_inventory') else 'record_disclosures', value,
        tuple(checks), tuple(basis_refs), (), tuple(reasons),
        'Owner-local inventory of explicitly named supplied records only. Native labels and availability are not authentication, '
        'graph eligibility, universal completeness, or an end-to-end analytical execution; provider integration remains pending.')
    port.check()
    return result


def _provenance_profile(prepared, context, record_refs, reference_refs, coverage_refs, port, *, provider_facts=()):
    """M015's four atomic leaves over explicit, deduplicated source populations.

    Missing PC03/PC04 providers remain unknown. They cannot erase inspectable
    source metadata or turn a native documentary label into a qualified edge.
    W13 alone will compose this owner-local core with the actual providers.
    """
    _analysis_start(prepared, context, port)
    providers = _profile_providers(prepared, context, provider_facts, port)
    records = _profile_selection(prepared, record_refs, port)
    references = _profile_selection(prepared, reference_refs, port, references=True)
    coverage = _profile_selection(prepared, coverage_refs, port, coverage=True)
    # Selected coverage records are this leaf's disclosed population. They
    # are not automatically coverage premises for all four metadata leaves.
    scope = _profile_scope(prepared, context, port)
    record_population = _profile_population(scope, records, 'record', 'Explicit named record IDs, deduplicated within this snapshot.', port)
    reference_population = _profile_population(scope, references, 'evidence_reference', 'Explicit named EvidenceReference IDs, deduplicated within this snapshot.', port)
    coverage_population = _profile_population(scope, coverage, 'record', 'Explicit named coverage Assertion IDs, deduplicated within this snapshot.', port)
    coverage_rows, coverage_facts = [], []
    for entity in coverage:
        local = _profile_context(entity, context, port)
        qualification = _qualify_coverage(prepared, (entity.identifier,), local, port)[0]
        port.charge(2)
        coverage_rows.append(_profile_disclosure(entity, qualification, (), port, coverage=True))
        coverage_facts.append(qualification)
    gap_rows, record_facts = [], []
    for entity in records:
        local = _profile_context(entity, context, port)
        basis = _qualify_basis(prepared, entity.identifier, local, port)
        conflicts = _qualify_conflicts(prepared, entity.identifier, local, port)
        reasons = _analysis_codes(basis.reason_codes + conflicts.reason_codes, port)
        port.charge(18)
        combined = _BasisQualification(basis.source, basis.declared_basis,
            'met' if basis.state == conflicts.state == 'met' else 'unmet', reasons,
            _analysis_unique_addresses(basis.support_refs + conflicts.support_refs, port), basis.qualifications, local)
        record_facts.append(combined)
        if reasons:
            gap_rows.append(_profile_disclosure(entity, combined, (), port))
    port.charge(len(coverage_rows) + len(gap_rows) + 12)
    coverage_value = _results._RecordDisclosures(tuple(coverage_rows))
    gap_value = _results._RecordDisclosures(tuple(gap_rows))
    basis_value = _profile_partition(record_population, records, _results.BASIS_KINDS, 'basis_kind', port)
    reference_value = _profile_partition(reference_population, references, _results.REFERENCE_AVAILABILITIES, 'availability', port)
    port.charge(len(coverage_facts) + len(record_facts) + 2)
    values = []
    for field, population, value, qualifications in (
            ('coverage_disclosures', coverage_population, coverage_value, tuple(coverage_facts)),
            ('documentary_basis_gap_disclosures', record_population, gap_value, tuple(record_facts)),
            ('declared_basis_inventory', record_population, basis_value, ()),
            ('reference_availability_inventory', reference_population, reference_value, ())):
        values.append(_profile_result(scope, field, population, value, providers, qualifications, port))
    for value in values:
        _charge_link(value.ref, port)
    port.charge(20)
    result = _results._ResultSet(tuple(values))
    port.check()
    return result
