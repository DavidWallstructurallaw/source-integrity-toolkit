# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: INGESTION_CONTRACT.

Bounded capture and source-bound W05 closed-shape validation. Capture alone
carries no acceptance status. Runtime completes reference/time/index/scope work
before acceptance. Caller containers must remain quiescent during capture;
arbitrary same-size concurrent mutation is outside the supported precondition.
"""
from ..contracts.bundle import (
    _Number, _DecodedObject, _CapturedBundle, _number_from_builtin,
    _number_bytes, _string_lengths, _freeze_array, _freeze_object,
)
from .limits import _InputLedger


def _size(source: object) -> int:
    return len(source.items) if type(source) is _DecodedObject else len(source)


def _next_child(frame: list, ledger: _InputLedger, decoded: bool) -> object:
    # Every frame and iterator is project-owned, over an exact admitted type.
    port = ledger.port
    port.charge(3)
    source, count, index, iterator, parts, key, mapping = frame
    if _size(source) != count:
        raise RuntimeError("capture_changed")
    if not decoded and index:
        ledger.add("bytes", 1)  # comma
    if mapping:
        try:
            key, child = next(iterator)
        except StopIteration:
            raise RuntimeError("capture_changed") from None
        if type(key) is not str:
            port.reject("type_or_enum_violation")
        _, encoded = _string_lengths(key, port)
        if not decoded:
            ledger.add("bytes", encoded + 1)  # colon; no key normalization
        frame[5] = key
    else:
        child = source[index]
    frame[2] = index + 1
    port.check()
    return child


def _finish(frame: list, ledger: _InputLedger) -> object:
    port = ledger.port
    port.charge(3)
    source, count, index, iterator, parts, key, mapping = frame
    if _size(source) != count or index != count:
        raise RuntimeError("capture_changed")
    if mapping:
        try:
            next(iterator)
        except StopIteration:
            pass
        else:
            raise RuntimeError("capture_changed")
        return _freeze_object(parts, port)
    return _freeze_array(parts, port)


def _capture_tree(value: object, ledger: _InputLedger, *, decoded: bool = False) -> _CapturedBundle:
    """Private seam; runtime owns ledger and decoded-mode selection.

    decoded=True is only for the completely preflighted project decoder tree.
    Its payload nodes were counted in preflight; repeated traversal is charged
    as work, without counting the same raw payload twice. No caller can supply
    that internal mode through _prepare_value or _prepare_utf8.
    """
    port = ledger.port
    port.charge(1)
    if type(decoded) is not bool:
        raise TypeError("invalid_private_capture_mode")
    if (decoded and type(value) is not _DecodedObject) or (not decoded and type(value) is not dict):
        port.reject("type_or_enum_violation")
    port.charge(2)
    frames, active = [], set()
    current = value
    while True:
        port.charge(1)
        if not decoded:
            ledger.add("nodes")
        kind = type(current)
        mapping = kind is dict if not decoded else kind is _DecodedObject
        if mapping or kind is list:
            port.charge(2 * len(active) + 2)  # active ancestry is bounded by 32
            identity = id(current)
            if identity in active:
                port.reject("input_constraint_violation", "container_cycle")
            ledger.depth(len(frames) + 1)
            count = _size(current)
            if not decoded:
                ledger.children_fit(count)
                ledger.add("bytes", 2)  # braces/brackets, including empty
            port.charge(10)
            if mapping:
                iterator = iter(current.items) if decoded else iter(dict.items(current))
            else:
                iterator = None
            frame = [current, count, 0, iterator, [], None, mapping]
            frames.append(frame)
            active.add(identity)
            if count:
                current = _next_child(frame, ledger, decoded)
                continue
            result = _finish(frame, ledger)
            frames.pop()
            active.remove(identity)
        else:
            if current is None or kind is bool:
                result = current
                length = 4 if current is None or current is True else 5
            elif kind is str:
                _, length = _string_lengths(current, port)
                result = current  # exact immutable str; no mutable source alias
            elif not decoded and (kind is int or kind is float):
                result = _number_from_builtin(current, port)
                length = len(_number_bytes(result, port))
            elif decoded and kind is _Number:
                result = current
                length = len(_number_bytes(result, port))
            else:
                port.reject("type_or_enum_violation")
            if not decoded:
                ledger.add("bytes", length)
            port.charge(1)
        # Retain a complete child, then descend into one next child only.
        # Stack depth is container depth, never the number of siblings.
        while frames:
            port.charge(2)
            frame = frames[-1]
            frame[4].append((frame[5], result) if frame[6] else result)
            if frame[2] < frame[1]:
                current = _next_child(frame, ledger, decoded)
                break
            result = _finish(frame, ledger)
            port.charge(2 * len(active) + 2)
            active.remove(id(frame[0]))
            frames.pop()
        else:
            port.charge(1)
            captured = _CapturedBundle(result, ledger.source_mode)
            port.check()
            return captured


# W05: source-bound closed-shape validation. No runtime schema/file lookup.
from ..contracts.bundle import _Object, _Array, _lookup_pair, _sorted_pairs, _compare_text
from ..contracts.constants import SHAPES, VOCABULARIES, RECORD_SHAPES, RELATION_SHAPES, ASSESSMENT_SHAPES
from ..contracts.execution import _byte_work

_COLLECTIONS = ("inquiries", "records", "assertions", "evidence_references")
_NULL_MEANINGS = (
    ("Bundle", "predecessor"), ("TimeValue", "value"), ("TimeValue", "precision"),
    ("EvidenceReference", "artifact_ref"), ("EvidenceReference", "record_ref"),
    ("EvidenceReference", "locator"), ("EvidenceReference", "excerpt"),
    ("EvidenceReference", "attestor_ref"), ("EvaluationData", "review_contribution"),
    ("CorrectionEventData", "case_ref"), ("ChangeDetails", "after_ref"),
    ("ChangeDetails", "after_absence_reason"), ("AnomalyData", "claim_ref"),
    ("AnomalyData", "context_evidence_ref"), ("AnomalyData", "caller_label"),
    ("RelationData", "dimension"), ("ConflictDetails", "resolution_evaluation_ref"),
)


def _field(obj, key, port, *, optional=False):
    port.charge(1)
    if type(obj) is not _Object:
        port.reject("type_or_enum_violation")
    pair = _lookup_pair(obj.items, key, port)
    if pair is None:
        if optional:
            return None
        port.reject("missing_required_field")
    return pair[1]


def _has(obj, key, port):
    return _lookup_pair(obj.items, key, port) is not None


def _identifier(value, port):
    _string_lengths(value, port, identifier=True)
    if not value:
        port.reject("input_constraint_violation", "identifier_ascii")
    for i, ch in enumerate(value):
        port.charge(2)
        alnum = "A" <= ch <= "Z" or "a" <= ch <= "z" or "0" <= ch <= "9"
        if not alnum and (i == 0 or ch not in "._:-"):
            port.reject("input_constraint_violation", "identifier_ascii")


def _enum(value, options, port):
    port.charge(1)
    if type(value) is not str:
        port.reject("type_or_enum_violation")
    for option in options:
        port.charge(1)
        if _compare_text(value, option, port) == 0:
            return
    port.reject("type_or_enum_violation")


def _shape_fields(shape, port):
    for name, section, fields in SHAPES:
        port.charge(1)
        if name == shape:
            return fields
    raise RuntimeError("undeclared_private_shape")


def _branch(shape, parent, port):
    if shape == "RecordData":
        value, mapping = _field(parent, "kind", port), RECORD_SHAPES
    elif shape == "AssertionData":
        value = _field(parent, "assertion_kind", port)
        _enum(value, ("relation", "assessment"), port)
        return "RelationData" if value == "relation" else "AssessmentData"
    elif shape == "RelationDetails":
        value, mapping = _field(parent, "predicate", port), RELATION_SHAPES
    elif shape == "AssessmentDetails":
        value, mapping = _field(parent, "assessment_kind", port), ASSESSMENT_SHAPES
    elif shape == "CorrectionDetails":
        value = _field(parent, "event_kind", port)
        _enum(value, ("submission", "handling", "change"), port)
        return {"submission": "SubmissionDetails", "handling": "HandlingDetails", "change": "ChangeDetails"}[value]
    else:
        return shape
    _enum(value, tuple(mapping), port)
    port.charge(2)
    return mapping[value]


def _path(prefix, name, port):
    _byte_work(port, 4 * (len(prefix) + len(name) + 1), 1)
    return prefix + "." + name if prefix else name


def _distinct(values, port):
    port.charge(len(values) + 1)
    pairs = _sorted_pairs(tuple((v, None) for v in values), port)
    previous = None
    for key, unused in pairs:
        port.charge(1)
        if previous is not None and _compare_text(previous, key, port) == 0:
            port.reject("type_or_enum_violation")
        previous = key


def _shape_walk(tree, ledger, *, count=True):
    """Bounded depth-first pass over the finite adopted declarations.

    Capture has already bounded the input tree to 32 container levels. This
    walker visits one sibling at a time, never allocating a wide pending stack.
    Returned occurrences are private, complete, and still pre-acceptance.
    """
    port = ledger.port
    occurrences = []

    def visit(desc, value, parent, owner, collection, prefix):
        port.charge(2)
        if desc.endswith("|null"):
            if value is None:
                return
            desc = desc[:-5]
        if desc.startswith(("*", "+")):
            if type(value) is not _Array:
                port.reject("type_or_enum_violation")
            if desc[0] == "+" and not value.items:
                port.reject("type_or_enum_violation")
            rest = desc[1:]
            distinct = rest.startswith("&")
            rest = rest.removeprefix("&")
            if distinct and count:
                ledger.add("reference_occurrences", len(value.items))
            for index, child in enumerate(value.items):
                port.charge(2)
                suffix = "[" + str(index) + "]"
                _byte_work(port, 4 * (len(prefix) + len(suffix)), 2)
                visit(rest, child, parent, owner, collection, prefix + suffix)
            if distinct:
                _distinct(value.items, port)
            return
        if desc.startswith("#"):
            if type(value) is not _Object:
                port.reject("type_or_enum_violation")
            shape = _branch(desc[1:], parent, port)
            fields = _shape_fields(shape, port)
            if shape in ("Inquiry", "Record", "Assertion", "EvidenceReference"):
                owner, prefix = value, ""
                collection = {"Inquiry": "inquiries", "Record": "records",
                              "Assertion": "assertions", "EvidenceReference": "evidence_references"}[shape]
            for key, unused in value.items:
                port.charge(1)
                # Every comparison is charged even for an unexpected long key.
                if not any(_compare_text(key, f[0], port) == 0 for f in fields):
                    port.reject("type_or_enum_violation")
            port.charge(1)
            occurrences.append((shape, value, owner, collection, prefix))
            for name, dtype, required in fields:
                pair = _lookup_pair(value.items, name, port)
                if pair is None:
                    if required:
                        port.reject("missing_required_field")
                    continue
                child = pair[1]
                if shape == "Bundle" and name in _COLLECTIONS:
                    if type(child) is not _Array:
                        port.reject("type_or_enum_violation")
                    if count:
                        ledger.add(name, len(child.items))
                if count and dtype in ("id", "id|null") and name.endswith("_ref") and child is not None:
                    ledger.add("reference_occurrences")
                if child is not None and (name.endswith("locator") or name == "locators"):
                    if name == "locators":
                        if type(child) is not _Array:
                            port.reject("type_or_enum_violation")
                        for locator in child.items:
                            ledger.field_bytes(locator, locator=True)
                    else:
                        ledger.field_bytes(child, locator=True)
                visit(dtype, child, value, owner, collection, _path(prefix, name, port))
            return
        if desc.startswith("@"):
            _enum(value, VOCABULARIES[desc[1:]], port)
        elif desc.startswith("="):
            if type(value) is not str:
                port.reject("type_or_enum_violation")
            if _compare_text(value, desc[1:], port) != 0:
                port.reject("unsupported_input_contract")
        elif desc == "id":
            _identifier(value, port)
        elif desc in ("str", "text"):
            _string_lengths(value, port)
            if desc == "text" and not value:
                port.reject("type_or_enum_violation")
        elif desc == "bool":
            if type(value) is not bool:
                port.reject("type_or_enum_violation")
        elif desc == "extensions":
            if type(value) is not _Object:
                port.reject("type_or_enum_violation")
            for key, unused in value.items:
                _byte_work(port, 4 * len(key), 1)
                if key.find(":") <= 0:
                    port.reject("type_or_enum_violation")
            # All descendant types/bytes/nodes were already fully captured.
        else:
            raise RuntimeError("undeclared_private_field_type")
        port.check()

    visit("#Bundle", tree, tree, tree, "bundle", "")
    port.charge(len(occurrences) + 1)
    return tuple(occurrences)


def _gap_fields(owner, port):
    value = _field(owner, "gaps", port, optional=True)
    if value is None:
        return ()
    port.charge(len(value.items) + 1)
    return tuple(_field(gap, "field", port) for gap in value.items)


def _need_gap(owner, name, port):
    for given in _gap_fields(owner, port):
        if _compare_text(given, name, port) == 0:
            return
    port.reject("missing_required_field")


def _nonempty(value, port, code="type_or_enum_violation"):
    port.charge(1)
    if type(value) is not str or not value:
        port.reject(code)


def _local_rules(occurrences, port):
    for shape, obj, owner, collection, prefix in occurrences:
        port.charge(2)
        def get(key):
            return _field(obj, key, port)
        for name, desc, required in _shape_fields(shape, port):
            if required and desc.endswith("|null") and get(name) is None:
                port.charge(len(_NULL_MEANINGS))
                if (shape, name) not in _NULL_MEANINGS:
                    _need_gap(owner, _path(prefix, name, port), port)
        if shape == "ClaimData" and get("text") is None:
            _field(obj, "content_evidence_ref", port)
        elif shape == "EvidenceReference":
            kind = get("reference_kind")
            if kind == "supplied_excerpt":
                _nonempty(get("excerpt"), port)
                if get("availability") != "supplied":
                    port.reject("type_or_enum_violation")
                if get("artifact_ref") is None:
                    gaps = _gap_fields(owner, port)
                    if not any(_compare_text(g, name, port) == 0 for g in gaps
                               for name in ("artifact_ref", "locator", "unmodeled_history")):
                        port.reject("missing_required_field")
            elif kind == "record_pointer" and get("record_ref") is None:
                port.reject("missing_required_field")
            elif kind in ("local_locator", "external_locator"):
                _nonempty(get("locator"), port)
            elif kind == "protected_attestation":
                if get("attestor_ref") is None:
                    port.reject("missing_required_field")
                if get("artifact_ref") is None:
                    _nonempty(get("excerpt"), port)
        elif shape == "OriginEventData" and not get("performed_by_refs").items:
            _need_gap(owner, "data.performed_by_refs", port)
        elif shape == "EvaluationData":
            if not get("role_bindings").items:
                _need_gap(owner, "data.role_bindings", port)
            if get("evaluation_kind") in ("empirical_review", "human_review", "identity_process_review") and get("review_contribution") is None:
                _need_gap(owner, "data.review_contribution", port)
        elif shape == "CorrectionChannelData":
            for name in ("owner_refs", "target_refs"):
                if not get(name).items:
                    _need_gap(owner, "data." + name, port)
        elif shape == "CorrectionEventData":
            if get("event_kind") == "submission":
                if get("case_ref") is not None:
                    port.reject("endpoint_or_claim_mismatch")
            elif get("case_ref") is None:
                port.reject("missing_required_field")
        elif shape == "ChangeDetails":
            if get("after_ref") is None:
                _nonempty(get("after_absence_reason"), port)
                # Free text remains supplied explanation. No semantic classifier
                # tries to infer whether a declared action actually removed it.
            elif get("after_absence_reason") is not None:
                port.reject("type_or_enum_violation")
        elif shape == "AnomalyData":
            if get("original_context") is None and get("context_evidence_ref") is None:
                port.reject("missing_required_field")
            if get("classification_state") == "unclassified":
                if get("caller_label") is not None:
                    port.reject("type_or_enum_violation")
            elif type(get("caller_label")) is not str:
                port.reject("type_or_enum_violation")
        elif shape == "Assertion" and get("lifecycle_state") != "active":
            if not get("lifecycle_basis_ref_ids").items or not _field(get("provenance"), "qualifications", port).items:
                port.reject("missing_required_field")
        elif shape == "ClassificationDetails":
            for label in get("labels").items:
                _enum(label, VOCABULARIES[get("axis")], port)
        elif shape == "VerificationDetails" and get("verification_scope") == "other":
            _nonempty(get("scope_note"), port)
        elif shape == "ConflictDetails":
            if get("resolution_state") == "unresolved":
                if get("resolution_evaluation_ref") is not None:
                    port.reject("type_or_enum_violation")
            elif get("resolution_evaluation_ref") is None:
                port.reject("missing_required_field")
    port.check()


def _validate_gaps(occurrences, port):
    # Index declared field paths per owner. Optional declared fields remain
    # nameable even when absent; extensions never erase a required factual Gap.
    owners = {}
    for shape, obj, owner, collection, prefix in occurrences:
        if collection == "bundle":
            continue
        identity = _field(owner, "id", port)
        _byte_work(port, len(identity), 2)
        key = (collection, identity)
        if key not in owners:
            owners[key] = (owner, [])
        for name, desc, required in _shape_fields(shape, port):
            port.charge(1)
            owners[key][1].append(_path(prefix, name, port))
    for owner, paths in owners.values():
        port.charge(len(paths) + 1)
        sorted_paths = _sorted_pairs(tuple((p, None) for p in paths), port)
        for name in _gap_fields(owner, port):
            if _compare_text(name, "unmodeled_history", port) != 0 and _lookup_pair(sorted_paths, name, port) is None:
                port.reject("type_or_enum_violation")
    port.check()


def _validate_structure(captured, ledger):
    if type(captured) is not _CapturedBundle:
        ledger.port.reject("type_or_enum_violation")
    occurrences = _shape_walk(captured.tree, ledger)
    _local_rules(occurrences, ledger.port)
    _validate_gaps(occurrences, ledger.port)
    ledger.port.check()
    return occurrences
