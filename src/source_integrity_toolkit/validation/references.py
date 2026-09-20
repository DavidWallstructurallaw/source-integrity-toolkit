# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: INGESTION_CONTRACT.

W05 snapshot identity, typed field links and explicit claim compatibility.
All work is source-bound to lineage sections 2-9. No eligibility projection,
ancestry search, independence qualification, correction authority or winner is
computed. A compatible unresolved endpoint remains an unresolved endpoint.
"""
from ..contracts.bundle import _Object, _Array, _sorted_pairs, _lookup_pair, _compare_text, _freeze_array, _freeze_object
from ..contracts.evidence import _Node, _Entity, _RecordLink, _InquiryPlan
from ..contracts.constants import VOCABULARIES
from ..contracts.execution import _byte_work
from .structure import _field, _shape_fields, _branch, _path, _COLLECTIONS

_TARGETS = ("claim", "artifact", "evidence_item", "model", "evaluation", "assertion")
_ALL_RECORDS = VOCABULARIES["record_kind"]
_STANCES = ("supports", "contradicts", "describes", "qualifies", "contextualizes")
_TRANSFORMS = ("derived_from", "copies", "syndicated_from", "summarizes", "translates", "quotes")
# A fixed input field registry. No input selects, replaces or extends a rule.
_REF_RULES = (
    ("Provenance", "attributed_to_ref", ("actor", "model"), True),
    ("Provenance", "evidence_ref_ids", ("evidence_reference",), False),
    ("EvidenceReference", "artifact_ref", ("artifact",), True),
    ("EvidenceReference", "record_ref", _ALL_RECORDS + ("assertion",), True),
    ("EvidenceReference", "provided_by_ref", ("actor", "model"), True),
    ("EvidenceReference", "attestor_ref", ("actor",), True),
    ("Inquiry", "target_claim_refs", ("claim",), False),
    ("Inquiry", "target_object_refs", ("artifact", "model", "evaluation"), True),
    ("Inquiry", "seed_artifact_refs", ("artifact",), True),
    ("Inquiry", "seed_evidence_refs", ("evidence_item",), False),
    ("Inquiry", "coverage_assertion_refs", ("coverage",), False),
    ("Boundary", "system_refs", ("actor", "model", "artifact", "evaluation"), True),
    ("ClaimData", "content_evidence_ref", ("evidence_reference",), False),
    ("ArtifactData", "content_evidence_refs", ("evidence_reference",), False),
    ("EvidenceItemData", "claim_ref", ("claim",), False),
    ("EvidenceItemData", "artifact_ref", ("artifact",), True),
    ("OriginEventData", "performed_by_refs", ("actor", "model"), True),
    ("OriginEventData", "method_ref", ("artifact",), True),
    ("ModelData", "provider_ref", ("actor",), True),
    ("EvaluationData", "target_refs", ("claim", "artifact", "evidence_item", "model", "assertion"), True),
    ("EvaluationData", "result_refs", ("artifact",), True),
    ("RoleBinding", "evidence_ref_ids", ("evidence_reference",), False),
    ("CorrectionChannelData", "owner_refs", ("actor", "model"), True),
    ("CorrectionChannelData", "target_refs", _TARGETS, True),
    ("CorrectionEventData", "case_ref", ("correction_event",), True),
    ("CorrectionEventData", "channel_ref", ("correction_channel",), True),
    ("CorrectionEventData", "target_refs", _TARGETS, True),
    ("ChangeDetails", "before_ref", _TARGETS, True),
    ("ChangeDetails", "after_ref", _TARGETS, True),
    ("PipelineRecordData", "subject_ref", ("evidence_item", "anomaly"), False),
    ("PipelineRecordData", "output_refs", ("evidence_item", "artifact", "anomaly"), True),
    ("AnomalyData", "inquiry_refs", ("inquiry",), False),
    ("AnomalyData", "claim_ref", ("claim",), False),
    ("AnomalyData", "context_evidence_ref", ("evidence_reference",), False),
    ("Assertion", "lifecycle_basis_ref_ids", ("evidence_reference",), False),
    ("Scope", "inquiry_refs", ("inquiry",), False),
    ("Scope", "claim_refs", ("claim",), False),
    ("RelationData", "from_ref", _ALL_RECORDS + ("assertion",), True),
    ("RelationData", "to_ref", _ALL_RECORDS + ("assertion",), True),
    ("TransformationDetails", "transformer_ref", ("actor", "model"), True),
    ("TransformationDetails", "method_ref", ("artifact",), True),
    ("AssessmentData", "subject_refs", _ALL_RECORDS + ("assertion", "inquiry"), True),
    ("OriginBoundaryDetails", "coverage_ref", ("coverage",), False),
    ("IndependenceDetails", "examined_dependency_refs", ("assertion",), False),
    ("IndependenceDetails", "coverage_ref", ("coverage",), False),
    ("CoverageDetails", "member_refs", _ALL_RECORDS, True),
    ("CoverageDetails", "omitted_refs", _ALL_RECORDS, True),
    ("ClassificationDetails", "verification_assessment_refs", ("verification",), False),
    ("VerificationDetails", "evaluation_ref", ("evaluation",), True),
    ("ExternalityDetails", "boundary_inquiry_ref", ("inquiry",), False),
    ("AuthorityDetails", "target_refs", _TARGETS, True),
    ("AuthorityDetails", "authorized_by_ref", ("actor",), True),
    ("AuthorityDetails", "coverage_ref", ("coverage",), False),
    ("ConflictDetails", "resolution_evaluation_ref", ("evaluation",), True),
)
_ROLE_RULES = (
    ("candidate", ("claim", "artifact", "evidence_item", "model")),
    ("generator", ("actor", "model")), ("judge", ("actor", "model")),
    ("executor", ("actor", "model")), ("human_reviewer", ("actor",)),
    ("reference_answer", ("artifact",)), ("rubric", ("artifact",)),
    ("validation_environment", ("artifact",)), ("method_input", ("artifact",)),
)


def _lookup(entities, identifier, port):
    low, high = 0, len(entities)
    while low < high:
        port.charge(2)
        mid = (low + high) // 2
        relation = _compare_text(entities[mid].identifier, identifier, port)
        if relation < 0:
            low = mid + 1
        else:
            high = mid
    if low == len(entities) or _compare_text(entities[low].identifier, identifier, port) != 0:
        port.reject("dangling_reference")
    return entities[low]


def _index(tree, port):
    pairs = []
    for collection in _COLLECTIONS:
        for obj in _field(tree, collection, port).items:
            identifier = _field(obj, "id", port)
            port.charge(5)
            pairs.append((identifier, _Array((collection, obj))))
    port.charge(len(pairs) + 1)
    ordered = _sorted_pairs(tuple(pairs), port)
    entities, previous = [], None
    for identifier, wrapped in ordered:
        port.charge(55)  # constant shape-tag constructor's separate check
        if previous is not None and _compare_text(previous, identifier, port) == 0:
            port.reject("duplicate_identifier")
        collection, obj = wrapped.items
        shape = {"inquiries": "Inquiry", "records": "Record", "assertions": "Assertion",
                 "evidence_references": "EvidenceReference"}[collection]
        kind = _field(obj, "kind", port) if collection == "records" else {
            "inquiries": "inquiry", "assertions": "assertion", "evidence_references": "evidence_reference"}[collection]
        entities.append(_Entity(collection, identifier, kind, _Node(shape, obj)))
        previous = identifier
    port.charge(len(entities) + 1)
    result = tuple(entities)
    port.check()
    return result


def _data(entity, port):
    return _field(entity.node.fields, "data", port)


def _kinds(entity, port, unresolved=True):
    port.charge(1)
    if entity.kind != "unresolved_reference" or not unresolved:
        return frozenset((entity.kind,))
    values = _field(_data(entity, port), "expected_kinds", port).items
    port.charge(2 * len(values) + 1)
    result = frozenset(values)
    port.check()
    return result


def _ensure(entity, kinds, port, unresolved=True):
    port.charge(len(kinds) + 2)
    if kinds in (("coverage",), ("verification",)):
        if entity.kind != "assertion":
            port.reject("endpoint_or_claim_mismatch")
        obj = entity.node.fields
        if _field(obj, "assertion_kind", port) != "assessment" or _field(_data(entity, port), "assessment_kind", port) != kinds[0]:
            port.reject("endpoint_or_claim_mismatch")
        return
    if not _kinds(entity, port, unresolved).intersection(kinds):
        port.reject("endpoint_or_claim_mismatch")


def _contains(values, wanted, port):
    for value in values:
        port.charge(1)
        if _compare_text(value, wanted, port) == 0:
            return True
    return False


def _ref_rule(shape, field, obj, port):
    if shape == "RoleBinding" and field == "object_ref":
        role = _field(obj, "role", port)
        for name, kinds in _ROLE_RULES:
            port.charge(1)
            if name == role:
                return kinds, True
    for s, name, kinds, unresolved in _REF_RULES:
        port.charge(1)
        if shape == s and field == name:
            return kinds, unresolved
    raise RuntimeError("missing_private_reference_rule")


def _check_links(occurrences, entities, port, *, retain=False):
    links = []
    for shape, obj, owner, collection, prefix in occurrences:
        if collection == "bundle":
            continue
        for name, desc, required in _shape_fields(shape, port):
            if not name.endswith(("_ref", "_refs", "_ref_ids")):
                continue
            value = _field(obj, name, port, optional=True)
            if value is None:
                continue
            kinds, unresolved = _ref_rule(shape, name, obj, port)
            many = type(value) is _Array
            values = value.items if many else (value,)
            for i, identifier in enumerate(values):
                port.charge(2)
                target = _lookup(entities, identifier, port)
                _ensure(target, kinds, port, unresolved)
                if shape == "RoleBinding" and name == "object_ref" and _field(obj, "role", port) == "human_reviewer":
                    if target.kind == "actor" and _field(_data(target, port), "actor_kind", port) != "human":
                        port.reject("endpoint_or_claim_mismatch")
                    # An unresolved actor stays unresolved. Its explicit human
                    # role/description is retained, never authenticated here.
                if retain:
                    source = _lookup(entities, _field(owner, "id", port), port)
                    selector = _path(prefix, name, port)
                    if many:
                        _byte_work(port, 4 * len(selector) + 32, 2)
                        selector += "[" + str(i) + "]"
                    port.charge(3)
                    links.append(_RecordLink(source, selector, target))
    port.charge(len(links) + 1)
    result = tuple(links)
    port.check()
    return result


def _require_claim(entity, claims, port):
    if entity.kind == "evidence_item":
        claim = _field(_data(entity, port), "claim_ref", port)
        if not _contains(claims, claim, port):
            port.reject("endpoint_or_claim_mismatch")
        return claim
    return None


def _same_claim(left, right, claims, port):
    a, b = _require_claim(left, claims, port), _require_claim(right, claims, port)
    if not claims or (a is not None and b is not None and _compare_text(a, b, port) != 0):
        port.reject("endpoint_or_claim_mismatch")


def _relation(entity, entities, claims, port):
    data = _data(entity, port)
    pred, dim = _field(data, "predicate", port), _field(data, "dimension", port)
    left = _lookup(entities, _field(data, "from_ref", port), port)
    right = _lookup(entities, _field(data, "to_ref", port), port)
    if pred in _STANCES:
        _ensure(left, ("evidence_item",), port)
        _ensure(right, ("claim",), port, False)
        if dim is not None or not _contains(claims, right.identifier, port):
            port.reject("endpoint_or_claim_mismatch")
        bound = _require_claim(left, claims, port)
        if bound is not None and _compare_text(bound, right.identifier, port) != 0:
            port.reject("endpoint_or_claim_mismatch")
    elif pred == "corroborates":
        _ensure(left, ("evidence_item",), port); _ensure(right, ("evidence_item",), port)
        if dim is not None:
            port.reject("endpoint_or_claim_mismatch")
        _same_claim(left, right, claims, port)
    elif pred in _TRANSFORMS:
        wanted = "artifact" if dim is None else "evidence_item"
        _ensure(left, (wanted,), port); _ensure(right, (wanted,), port)
        if wanted == "evidence_item":
            _same_claim(left, right, claims, port)
    elif pred in ("originates_from", "depends_on"):
        _ensure(left, ("evidence_item" if pred == "originates_from" else "origin_event",), port)
        _ensure(right, ("origin_event",), port)
        if dim is None or not claims:
            port.reject("endpoint_or_claim_mismatch")
        _require_claim(left, claims, port)
    elif pred in ("cites", "retrieved_from"):
        _ensure(left, ("artifact",), port); _ensure(right, ("artifact",), port)
        if dim is not None:
            port.reject("endpoint_or_claim_mismatch")
    elif pred in ("generated_by", "published_by"):
        _ensure(left, ("artifact", "evidence_item") if pred == "generated_by" else ("artifact",), port)
        _ensure(right, ("actor", "model") if pred == "generated_by" else ("actor",), port)
        if dim is not None:
            port.reject("endpoint_or_claim_mismatch")
    elif pred in ("model_derived_from", "trained_on"):
        _ensure(left, ("model",), port)
        _ensure(right, ("model",) if pred == "model_derived_from" else ("artifact",), port)
        if dim != "model_ancestry":
            port.reject("endpoint_or_claim_mismatch")
        if pred == "trained_on" and right.kind == "artifact" and _field(_data(right, port), "artifact_kind", port) != "dataset":
            port.reject("endpoint_or_claim_mismatch")
    elif pred == "owned_by":
        _ensure(left, ("actor", "model"), port); _ensure(right, ("actor",), port)
        if dim != "organizational_control":
            port.reject("endpoint_or_claim_mismatch")
    elif pred == "propagates_to":
        _ensure(left, ("correction_channel",), port)
        _ensure(right, ("correction_channel",) + _TARGETS, port)
        if dim is not None:
            port.reject("endpoint_or_claim_mismatch")
    elif pred in ("supersedes", "same_identity_as"):
        if dim is not None:
            port.reject("endpoint_or_claim_mismatch")
        if pred == "supersedes":
            kinds = ("artifact", "claim", "model", "assertion")
            if _compare_text(left.identifier, right.identifier, port) == 0:
                port.reject("endpoint_or_claim_mismatch")
        else:
            level = _field(_field(data, "details", port), "identity_level", port)
            kinds = ({"artifact_version": "artifact", "actor": "actor",
                      "origin_event": "origin_event", "model_version": "model"}[level],)
        port.charge(20)
        if not (_kinds(left, port) & _kinds(right, port)).intersection(kinds):
            port.reject("endpoint_or_claim_mismatch")
    else:
        raise RuntimeError("missing_private_predicate_rule")


def _assessment(entity, entities, claims, inquiries, port):
    data = _data(entity, port)
    kind = _field(data, "assessment_kind", port)
    details = _field(data, "details", port)
    subjects = _field(data, "subject_refs", port).items
    allowed = {
        "origin_boundary": ("origin_event",),
        "independence": ("evidence_item", "origin_event", "evaluation", "model", "actor"),
        "coverage": ("inquiry", "artifact", "origin_event", "model", "evaluation", "correction_channel", "pipeline_record"),
        "classification": ("artifact", "evidence_item", "actor", "evaluation", "anomaly"),
        "verification": ("actor", "artifact", "assertion"),
        "externality": ("origin_event", "evidence_item"),
        "authority": ("correction_channel",), "capacity": ("correction_channel", "evaluation"),
        "conflict": ("assertion",),
    }[kind]
    if kind in ("origin_boundary", "authority") and len(subjects) != 1:
        port.reject("endpoint_or_claim_mismatch")
    if kind in ("independence", "conflict") and len(subjects) < 2:
        port.reject("endpoint_or_claim_mismatch")
    if kind == "coverage" and not subjects:
        port.reject("endpoint_or_claim_mismatch")
    if kind in ("origin_boundary", "independence", "externality") and not claims:
        port.reject("endpoint_or_claim_mismatch")
    if kind == "independence" and _field(details, "comparison_form", port) == "pairwise" and len(subjects) != 2:
        port.reject("endpoint_or_claim_mismatch")
    compatible = frozenset(allowed)
    for identifier in subjects:
        port.charge(20)
        subject = _lookup(entities, identifier, port)
        _ensure(subject, allowed, port)
        _require_claim(subject, claims, port)
        if kind == "independence":
            compatible = compatible & _kinds(subject, port)
    if kind == "independence" and not compatible:
        port.reject("endpoint_or_claim_mismatch")
    if kind == "externality" and not _contains(inquiries, _field(details, "boundary_inquiry_ref", port), port):
        port.reject("endpoint_or_claim_mismatch")


def _validate_references(captured, occurrences, port):
    entities = _index(captured.tree, port)
    _check_links(occurrences, entities, port)
    for entity in entities:
        port.charge(1)
        obj = entity.node.fields
        if entity.kind == "inquiry":
            claims = _field(obj, "target_claim_refs", port).items
            for identifier in _field(obj, "seed_evidence_refs", port).items:
                _require_claim(_lookup(entities, identifier, port), claims, port)
        elif entity.kind == "correction_event":
            data = _data(entity, port)
            if _field(data, "event_kind", port) != "submission":
                case = _lookup(entities, _field(data, "case_ref", port), port)
                if case.kind == "correction_event" and _field(_data(case, port), "event_kind", port) != "submission":
                    port.reject("endpoint_or_claim_mismatch")
            if _field(data, "event_kind", port) == "change":
                before = _field(_field(data, "details", port), "before_ref", port)
                if not _contains(_field(data, "target_refs", port).items, before, port):
                    port.reject("endpoint_or_claim_mismatch")
        elif entity.kind == "assertion":
            scope = _field(obj, "scope", port)
            claims, inquiries = _field(scope, "claim_refs", port).items, _field(scope, "inquiry_refs", port).items
            for identifier in inquiries:
                inquiry = _lookup(entities, identifier, port)
                targets = _field(inquiry.node.fields, "target_claim_refs", port).items
                for claim in claims:
                    if not _contains(targets, claim, port):
                        port.reject("endpoint_or_claim_mismatch")
            if _field(obj, "assertion_kind", port) == "relation":
                _relation(entity, entities, claims, port)
            else:
                _assessment(entity, entities, claims, inquiries, port)
    port.check()
    return entities


def _normalize(tree, entities, port):
    """Only the declared sets/collections/roles are reordered; no dedup."""
    def shape_map(shape, obj):
        parts = []
        for name, desc, required in _shape_fields(shape, port):
            # Captured object keys are already ordered; optional absence stays absent.
            from_pair = None
            for pair in obj.items:
                port.charge(1)
                if pair[0] == name:
                    from_pair = pair
                    break
            if from_pair is None:
                continue
            value = from_pair[1]
            out = value_map(desc, value, obj)
            if shape == "Bundle" and name in _COLLECTIONS:
                port.charge(len(out.items) + 1)
                pairs = _sorted_pairs(tuple((_field(v, "id", port), v) for v in out.items), port)
                port.charge(len(pairs) + 1)
                out = _freeze_array([v for k, v in pairs], port)
            elif shape == "EvaluationData" and name == "role_bindings":
                pairs = []
                for v in out.items:
                    role, ref = _field(v, "role", port), _field(v, "object_ref", port)
                    _byte_work(port, len(role) + len(ref) + 1, 2)
                    pairs.append((role + "/" + ref, v))
                port.charge(len(pairs) + 1)
                ordered = _sorted_pairs(tuple(pairs), port)
                port.charge(len(ordered) + 1)
                out = _freeze_array([v for k, v in ordered], port)
            port.charge(1)
            parts.append((name, out))
        result = _freeze_object(parts, port)
        if shape == "Record" and _field(obj, "kind", port) == "evaluation":
            result = _rebase_role_gaps(obj, result, port)
        return result

    def value_map(desc, value, parent):
        port.charge(1)
        if value is None:
            return None
        desc = desc.removesuffix("|null")
        if desc.startswith(("*", "+")):
            rest = desc[1:]
            distinct = rest.startswith("&")
            rest = rest.removeprefix("&")
            parts = []
            for v in value.items:
                port.charge(1)
                parts.append(value_map(rest, v, parent))
            if distinct:
                pairs = []
                for identifier in parts:
                    ref = _lookup(entities, identifier, port)
                    _byte_work(port, len(ref.collection) + len(identifier) + 1, 2)
                    pairs.append((ref.collection + "/" + identifier, identifier))
                port.charge(len(pairs) + 1)
                ordered = _sorted_pairs(tuple(pairs), port)
                port.charge(len(ordered) + 1)
                parts = [v for k, v in ordered]
            return _freeze_array(parts, port)
        if desc.startswith("#"):
            return shape_map(_branch(desc[1:], parent, port), value)
        return value  # immutable scalar or opaque, already captured extension

    result = shape_map("Bundle", tree)
    port.check()
    return result


def _scope_plan(entities, port):
    plans = []
    for inquiry in entities:
        port.charge(1)
        if inquiry.kind != "inquiry":
            continue
        assertions, anomalies = [], []
        for entity in entities:
            port.charge(1)
            if entity.kind == "assertion":
                bindings = _field(_field(entity.node.fields, "scope", port), "inquiry_refs", port).items
                if _contains(bindings, inquiry.identifier, port):
                    port.charge(1)
                    assertions.append(entity.identifier)
            elif entity.kind == "anomaly":
                if _contains(_field(_data(entity, port), "inquiry_refs", port).items, inquiry.identifier, port):
                    port.charge(1)
                    anomalies.append(entity.identifier)
        # The inquiry node itself retains exact Claim/seed/target/dimension/time
        # anchors. All evaluator/correction/pipeline field anchors remain in the
        # full immutable link table, without inventing an all-pairs query.
        port.charge(2 * (len(assertions) + len(anomalies)) + 3)
        plans.append(_InquiryPlan(inquiry, tuple(assertions), tuple(anomalies)))
    port.charge(len(plans) + 1)
    result = tuple(plans)
    port.check()
    return result


def _rebase_role_gaps(original, normalized, port):
    """Keep a Gap attached to its role when the role array is reordered.

    Only the canonical field-path selector changes. The complete pre-normalized
    input remains in the prepared object's captured_tree; narrative Gap content
    stays exact. Stable sorting preserves multiplicity even for repeated roles.
    """
    gaps = _field(original, "gaps", port, optional=True)
    if gaps is None:
        return normalized
    roles = _field(_field(original, "data", port), "role_bindings", port)
    pairs = []
    for index, role in enumerate(roles.items):
        name, ref = _field(role, "role", port), _field(role, "object_ref", port)
        _byte_work(port, len(name) + len(ref) + 32, 3)
        pairs.append((name + "/" + ref, str(index)))
    port.charge(len(pairs) + 1)
    ordered = _sorted_pairs(tuple(pairs), port)
    indices = []
    for index, (key, old_index) in enumerate(ordered):
        port.charge(3)
        indices.append((old_index, str(index)))
    port.charge(len(indices) + 1)
    mapping = _sorted_pairs(tuple(indices), port)
    result, prefix = [], "data.role_bindings["
    for gap in gaps.items:
        selector = _field(gap, "field", port)
        _byte_work(port, 4 * len(selector), 3)
        if selector.startswith(prefix):
            end = selector.find("]", len(prefix))
            if end >= 0:
                pair = _lookup_pair(mapping, selector[len(prefix):end], port)
                if pair is not None:
                    _byte_work(port, 4 * len(selector) + 32, len(gap.items) + 2)
                    changed = prefix + pair[1] + selector[end:]
                    gap = _freeze_object([(k, changed if k == "field" else v) for k, v in gap.items], port)
        port.charge(1)
        result.append(gap)
    value = _freeze_array(result, port)
    port.charge(len(normalized.items) + 1)
    return _freeze_object([(k, value if k == "gaps" else v) for k, v in normalized.items], port)
