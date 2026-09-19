# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: INGESTION_CONTRACT.

W04 capture only. Closed keys, identity/reference/type/time validation and the
scope plan remain W05. A captured tree is never accepted input. The caller must
keep all reachable containers quiescent during capture. Observable size/iterator
inconsistencies fail; arbitrary same-size concurrent mutation is not detectable.
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
