# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: RUNTIME_BOUNDARY.

W04 byte decoding only: exact caller-supplied immutable bytes, never a path,
stream or file handle. A bounded lexical preflight precedes json.loads. All
hooks are project-owned. No filesystem operation or input acceptance exists.
"""
import json
from ..contracts.bundle import (
    _DecodedObject, _number_from_token, _sorted_pairs, _compare_text,
)
from ..contracts.execution import _byte_work
from ..validation.limits import _InputLedger
from ..validation.structure import _capture_tree


def _hex4(text: str, index: int, port) -> int:
    port.charge(5)
    if index + 4 > len(text):
        port.reject("invalid_syntax")
    value = 0
    for pos in range(index, index + 4):
        code = ord(text[pos])
        digit = code - 48 if 48 <= code <= 57 else code - 87 if 97 <= code <= 102 else code - 55 if 65 <= code <= 70 else -1
        if digit < 0:
            port.reject("invalid_syntax")
        value = value * 16 + digit
    port.check()
    return value


def _scan_string(text: str, index: int, port) -> int:
    # Compute the decoded byte size without materializing a source string.
    index += 1
    decoded_bytes = 0
    while index < len(text):
        port.charge(2)
        code = ord(text[index])
        index += 1
        if code == 34:
            port.check()
            return index
        if code < 32:
            port.reject("invalid_syntax")
        if code == 92:
            port.charge(2)
            if index >= len(text):
                port.reject("invalid_syntax")
            escape = text[index]
            index += 1
            if escape == "u":
                code = _hex4(text, index, port)
                index += 4
                if 0xD800 <= code <= 0xDBFF:
                    port.charge(3)
                    if index + 6 > len(text) or text[index:index + 2] != "\\u":
                        port.reject("input_constraint_violation", "unicode_scalar")
                    low = _hex4(text, index + 2, port)
                    if not 0xDC00 <= low <= 0xDFFF:
                        port.reject("input_constraint_violation", "unicode_scalar")
                    code = 0x10000 + (code - 0xD800) * 1024 + low - 0xDC00
                    index += 6
                elif 0xDC00 <= code <= 0xDFFF:
                    port.reject("input_constraint_violation", "unicode_scalar")
            elif escape in '"\\/bfnrt':
                code = 0  # each of these decoded characters occupies one byte
            else:
                port.reject("invalid_syntax")
        if 0xD800 <= code <= 0xDFFF:
            port.reject("input_constraint_violation", "unicode_scalar")
        decoded_bytes += 1 if code < 128 else 2 if code < 2048 else 3 if code < 65536 else 4
        if decoded_bytes > 65_536:
            port.reject("input_constraint_violation", "string_length")
    port.reject("invalid_syntax")


def _space(text: str, index: int, port) -> int:
    while index < len(text):
        # A bounded native strip only detects all-whitespace chunks. It never
        # changes the retained source or admits non-JSON whitespace.
        size = min(64, len(text) - index)
        _byte_work(port, size * 4, 2)
        part = text[index:index + size]
        if not part.strip(" \t\r\n"):
            index += size
            continue
        for ch in part:
            port.charge(2)
            if ch not in " \t\r\n":
                return index
            index += 1
    return index


def _preflight(text: str, ledger: _InputLedger) -> tuple[int, int]:
    """Full finite JSON grammar preflight, depth stack and scalar limits.

    Object keys are not value nodes. No object/array payload is constructed.
    Return visited node/key counts for precharging the later decoder pass.
    """
    port = ledger.port
    port.charge(3)
    stack, index, started, nodes, keys = [], 0, False, 0, 0
    while True:
        index = _space(text, index, port)
        if not stack and started:
            if index != len(text):
                port.reject("invalid_syntax")
            port.check()
            return nodes, keys
        if index >= len(text):
            port.reject("invalid_syntax")
        port.charge(2)
        ch = text[index]
        if stack:
            frame = stack[-1]
            kind, state = frame
            if kind == "object" and state in ("first", "key"):
                if ch == "}" and state == "first":
                    stack.pop()
                    index += 1
                    continue
                if ch != '"':
                    port.reject("invalid_syntax")
                index = _scan_string(text, index, port)
                keys += 1
                frame[1] = "colon"
                continue
            if kind == "object" and state == "colon":
                if ch != ":":
                    port.reject("invalid_syntax")
                frame[1] = "value"
                index += 1
                continue
            if state == "after":
                closing = "}" if kind == "object" else "]"
                if ch == closing:
                    stack.pop()
                elif ch == ",":
                    frame[1] = "key" if kind == "object" else "value"
                else:
                    port.reject("invalid_syntax")
                index += 1
                continue
            if kind == "array" and state == "first" and ch == "]":
                stack.pop()
                index += 1
                continue
            frame[1] = "after"
        else:
            started = True
        ledger.add("nodes")
        nodes += 1
        if ch == "{" or ch == "[":
            ledger.depth(len(stack) + 1)
            port.charge(3)
            stack.append(["object" if ch == "{" else "array", "first"])
            index += 1
        elif ch == '"':
            index = _scan_string(text, index, port)
        elif ch in "-0123456789":
            start = index
            while index < len(text):
                port.charge(2)
                if text[index] not in "0123456789eE+-.":
                    break
                index += 1
                if index - start > 128:
                    port.interrupt("WU9-L09")
            _byte_work(port, index - start, 1)
            _number_from_token(text[start:index], port)
        else:
            literal = "true" if ch == "t" else "false" if ch == "f" else "null" if ch == "n" else ""
            port.charge(2)
            if not literal or text[index:index + len(literal)] != literal:
                port.reject("invalid_syntax")
            index += len(literal)


def _decode_utf8(raw: object, ledger: _InputLedger):
    port = ledger.port
    port.charge(1)
    if type(raw) is not bytes:
        port.reject("type_or_enum_violation")
    ledger.add("bytes", len(raw))
    # The raw byte guard precedes allocation and decoding. Strict UTF-8 never
    # invokes JSON's automatic UTF-16/32 sniffing or replacement decoding.
    _byte_work(port, len(raw), 1)
    try:
        text = raw.decode("utf-8", "strict")
    except UnicodeDecodeError:
        port.reject("invalid_syntax")
    port.check()
    nodes, keys = _preflight(text, ledger)
    # The known bounded decoder traversal is prepaid separately from preflight;
    # every hook additionally charges its own actual work.
    _byte_work(port, len(raw), 3 * (nodes + keys) + 1)

    def number(token):
        return _number_from_token(token, port)

    def constant(token):
        port.reject("invalid_syntax")

    def pairs_hook(pairs):
        port.charge(len(pairs) * 3 + 1)
        names = tuple((key, None) for key, value in pairs)
        names = _sorted_pairs(names, port)
        previous = None
        for key, unused in names:
            port.charge(1)
            if previous is not None and _compare_text(previous, key, port) == 0:
                port.reject("duplicate_key")
            previous = key
        port.charge(len(pairs) + 2)
        result = _DecodedObject(tuple(pairs))
        port.check()
        return result

    port.check()
    try:
        tree = json.loads(text, parse_int=number, parse_float=number,
                          parse_constant=constant, object_pairs_hook=pairs_hook)
    except json.JSONDecodeError:
        port.reject("invalid_syntax")
    port.check()
    return _capture_tree(tree, ledger, decoded=True)
