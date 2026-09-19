# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: INGESTION_CONTRACT.

Private immutable values plus SIT-RP-0.1 scalar/J measuring primitives. This is
not dossier ingestion. Local constructors require bounded project-owned parts;
W04/W05 must guard construction and perform complete capture/validation. Scalar
helpers require a project-owned port, retain numeric source kind, and neither
coerce custom objects nor grant input acceptance. No report serializer exists.
"""
from dataclasses import dataclass
from .execution import _BudgetPort, _byte_work


def _require(ok: bool) -> None:
    if not ok:
        raise TypeError("invalid_private_representation")


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Number:
    """Exact sign/coefficient/exponent atom; no conversion or rounding here."""
    sign: int
    coefficient: str
    exponent: int
    source_kind: str

    def __post_init__(self) -> None:
        _require(type(self.sign) is int and self.sign in (-1, 0, 1))
        _require(type(self.coefficient) is str)
        _require(type(self.exponent) is int)
        _require(type(self.source_kind) is str and self.source_kind in
                 ("integer", "decimal", "binary_float"))
        c = self.coefficient
        _require(bool(c) and all("0" <= ch <= "9" for ch in c))
        if c == "0":
            _require(self.sign == 0 and self.exponent == 0)
        else:
            _require(self.sign != 0 and c[0] != "0" and c[-1] != "0")


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Array:
    """Ordered immutable JSON occurrences; aliases have no evidence identity."""
    items: tuple

    def __post_init__(self) -> None:
        _require(type(self.items) is tuple)
        for value in self.items:
            _require(_is_value(value))


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _Object:
    """Exact decoded key/value pairs; no key normalization or hidden default."""
    items: tuple

    def __post_init__(self) -> None:
        _require(type(self.items) is tuple)
        seen = set()
        for pair in self.items:
            _require(type(pair) is tuple and len(pair) == 2)
            key, value = pair
            _require(type(key) is str)
            _require(key not in seen and _is_value(value))
            seen.add(key)


def _is_value(value: object) -> bool:
    kind = type(value)
    return (value is None or kind is str or kind is bool or kind is _Number or
            kind is _Array or kind is _Object)


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _CapturedBundle:
    """Internal captured tree, deliberately carrying no accepted/pass flag."""
    tree: _Object
    source_mode: str

    def __post_init__(self) -> None:
        _require(type(self.tree) is _Object)
        _require(type(self.source_mode) is str and
                 self.source_mode in ("constructed_value", "supplied_utf8"))


_MAX_TOKEN = 128
_MAX_INTEGER = 9_007_199_254_740_991
_MAX_STRING = 65_536
_MAX_LOCATOR = 4_096
_MAX_IDENTIFIER = 128
_MAX_PRIVATE_PAIRS = 500_000


def _copy_text(text: str, start: int, stop: int, port: _BudgetPort) -> str:
    # The caller has already bounded exact str and offsets. Four bytes/scalar
    # conservatively covers UTF-8; charge before the bounded native slice.
    _byte_work(port, 4 * (stop - start), 1)
    result = text[start:stop]
    port.check()
    return result


def _normal_atom(sign: int, digits: str, exponent: int,
                 source_kind: str, port: _BudgetPort) -> _Number:
    """Only bounded project-created digit strings and checked exponent inputs."""
    left, right = 0, len(digits)
    while left < right:
        port.charge(2)
        if digits[left] != "0":
            break
        left += 1
    if left == right:
        port.charge(2)
        atom = _Number(0, "0", 0, source_kind)
    else:
        while right > left:
            port.charge(2)
            if digits[right - 1] != "0":
                break
            right -= 1
        _byte_work(port, 140, 1)  # bounded exponent arithmetic, no powers
        exponent += len(digits) - right
        coefficient = _copy_text(digits, left, right, port)
        # Constructor's digit validation is a separate bounded pass.
        _byte_work(port, len(coefficient), len(coefficient) + 1)
        atom = _Number(sign, coefficient, exponent, source_kind)
    _number_bytes(atom, port)  # includes magnitude and exact token ceiling
    port.check()
    return atom


def _number_from_token(token: object, port: _BudgetPort) -> _Number:
    """One already isolated raw JSON number token; no full JSON decoding."""
    port.charge(1)
    if type(token) is not str:
        port.reject("type_or_enum_violation")
    n = len(token)
    if n > _MAX_TOKEN:
        port.interrupt("WU9-L09")
    if not n:
        port.reject("invalid_syntax")
    # Each scalar is examined before further lexical processing. This also
    # bounds every subsequent slice/conversion independently of numeric value.
    for index in range(n):
        port.charge(2)
        ch = token[index]
        if ord(ch) > 127:
            port.reject("invalid_syntax")
    _byte_work(port, n * 4, n + 1)
    i = 1 if token[0] == "-" else 0
    sign = -1 if i else 1
    start = i
    if i >= n or not "0" <= token[i] <= "9":
        port.reject("invalid_syntax")
    if token[i] == "0":
        i += 1
    else:
        while i < n and "0" <= token[i] <= "9":
            port.charge(2)
            i += 1
    integer_end = i
    fraction_start, fraction_end = i, i
    if i < n and token[i] == ".":
        i += 1
        fraction_start = i
        while i < n and "0" <= token[i] <= "9":
            port.charge(2)
            i += 1
        fraction_end = i
        if fraction_start == fraction_end:
            port.reject("invalid_syntax")
    exp = 0
    exp_present = i < n and token[i] in ("e", "E")
    if exp_present:
        i += 1
        exp_start = i
        if i < n and token[i] in ("+", "-"):
            i += 1
        exp_digits = i
        while i < n and "0" <= token[i] <= "9":
            port.charge(2)
            i += 1
        if i == exp_digits:
            port.reject("invalid_syntax")
        # At most 128 characters. int allocation is O(token length), never
        # O(the exponent's value). No 10**exp, decimal expansion or clamping.
        _byte_work(port, n, 1)
        exp = int(token[exp_start:i])
        port.check()
    if i != n:
        port.reject("invalid_syntax")
    _byte_work(port, n * 3, 3)
    digits = token[start:integer_end] + token[fraction_start:fraction_end]
    kind = "decimal" if fraction_end > fraction_start or exp_present else "integer"
    return _normal_atom(sign, digits, exp - (fraction_end - fraction_start), kind, port)


def _number_from_builtin(value: object, port: _BudgetPort) -> _Number:
    """Exact built-in int/finite float only. bool is deliberately excluded."""
    port.charge(1)
    kind = type(value)
    if kind is int:
        # Compare before abs/str, which could copy an arbitrarily large int.
        if value < -_MAX_INTEGER or value > _MAX_INTEGER:
            port.reject("input_constraint_violation", "exact_integer_range")
        _byte_work(port, 17, 1)
        text = str(value)
        return _number_from_token(text, port)
    if kind is not float:
        port.reject("type_or_enum_violation")
    if not -float("inf") < value < float("inf"):
        port.reject("type_or_enum_violation")
    if value.is_integer() and (value < -_MAX_INTEGER or value > _MAX_INTEGER):
        port.reject("input_constraint_violation", "exact_integer_range")
    # CPython's finite binary float ratio is bounded independently of source
    # text. Precharge conservative operand/result bounds before native calls.
    _byte_work(port, 300, 1)
    numerator, denominator = value.as_integer_ratio()
    port.check()
    places = denominator.bit_length() - 1
    if not 0 <= places <= 1074 or denominator & (denominator - 1):
        raise RuntimeError("unsupported_private_float_ratio")
    _byte_work(port, 2800, 3)
    coefficient = abs(numerator) * (5 ** places)
    digits = str(coefficient)  # <= 1400 digits, far below interpreter ceiling
    port.check()
    return _normal_atom(-1 if numerator < 0 else 1, digits, -places, "binary_float", port)


def _number_bytes(atom: object, port: _BudgetPort) -> bytes:
    """The exact shortest J spelling; integral values use ordinary digits."""
    port.charge(1)
    if type(atom) is not _Number:
        port.reject("type_or_enum_violation")
    c, e, sign = atom.coefficient, atom.exponent, atom.sign
    n = len(c)
    if sign == 0:
        port.charge(1)
        port.check()
        return b"0"
    negative = sign < 0
    if e >= 0:
        # Establish prohibited integral magnitude without expanding an exponent.
        if e > 16 or n + e > 16:
            port.reject("input_constraint_violation", "exact_integer_range")
        _byte_work(port, 32, 2)
        digits = c + "0" * e
        if len(digits) == 16 and digits > "9007199254740991":
            port.reject("input_constraint_violation", "exact_integer_range")
        spelling = ("-" if negative else "") + digits
    else:
        # A canonical non-integral coefficient has no trailing zero. More than
        # 128 digits, or >432 exponent bits, necessarily exceeds token length.
        if n > _MAX_TOKEN or e.bit_length() > 432:
            port.interrupt("WU9-L09")
        _byte_work(port, 140, 1)
        exponent_text = str(e)
        point = n + e
        ordinary_length = n + 1 if point > 0 else 2 - point + n
        scientific_length = n + 1 + len(exponent_text)
        chosen_length = min(ordinary_length, scientific_length) + int(negative)
        if chosen_length > _MAX_TOKEN:
            port.interrupt("WU9-L09")
        _byte_work(port, chosen_length * 3, 3)
        if ordinary_length <= scientific_length:
            spelling = (c[:point] + "." + c[point:]) if point > 0 else ("0." + "0" * (-point) + c)
        else:
            spelling = c + "e" + exponent_text
        if negative:
            spelling = "-" + spelling
    _byte_work(port, len(spelling), 1)
    result = spelling.encode("ascii")
    port.check()  # no value returned after interruption of this component action
    return result


def _string_lengths(value: object, port: _BudgetPort, *, locator: bool = False,
                    identifier: bool = False) -> tuple[int, int]:
    """Decoded UTF-8 bytes and J string bytes, including quotes. No allocation
    proportional to an unexamined string. Limits are fixed by the field role;
    grammar validation of identifiers remains W05's separate responsibility.
    """
    port.charge(1)
    if type(value) is not str or type(locator) is not bool or type(identifier) is not bool:
        port.reject("type_or_enum_violation")
    ceiling = _MAX_IDENTIFIER if identifier else _MAX_LOCATOR if locator else _MAX_STRING
    constraint = "identifier_length" if identifier else "locator_length" if locator else "string_length"
    if len(value) > ceiling:
        port.reject("input_constraint_violation", constraint)
    decoded, encoded = 0, 2
    for index in range(len(value)):
        port.charge(2)  # one visit plus one <=4-byte block examination
        ch = value[index]
        code = ord(ch)
        if 0xD800 <= code <= 0xDFFF:
            port.reject("input_constraint_violation", "unicode_scalar")
        if identifier and code > 127:
            port.reject("input_constraint_violation", "identifier_ascii")
        width = 1 if code < 128 else 2 if code < 2048 else 3 if code < 65536 else 4
        decoded += width
        if decoded > ceiling:
            port.reject("input_constraint_violation", constraint)
        if code < 32 or 127 <= code <= 159 or code == 0x061C or 0x200E <= code <= 0x200F or 0x2028 <= code <= 0x202E or 0x2066 <= code <= 0x2069:
            encoded += 6
        elif ch in ('"', "\\"):
            encoded += 2
        else:
            encoded += width
    port.check()
    return decoded, encoded


def _j_scalar(value: object, port: _BudgetPort) -> bytes:
    """Bounded scalar component only; no tree or audit-report serialization."""
    port.charge(1)
    if value is None or type(value) is bool:
        port.charge(1)
        result = b"null" if value is None else b"true" if value else b"false"
        port.check()
        return result
    if type(value) is _Number:
        return _number_bytes(value, port)
    if type(value) is not str:
        port.reject("type_or_enum_violation")
    _, encoded = _string_lengths(value, port)
    port.charge(2)
    parts = [b'"']
    for index in range(len(value)):
        port.charge(3)  # visit, encode one <=6-byte fragment, retain entry
        ch = value[index]
        code = ord(ch)
        if code < 32 or 127 <= code <= 159 or code == 0x061C or 0x200E <= code <= 0x200F or 0x2028 <= code <= 0x202E or 0x2066 <= code <= 0x2069:
            fragment = ("\\u%04x" % code).encode("ascii")
        elif ch in ('"', "\\"):
            fragment = ("\\" + ch).encode("ascii")
        else:
            fragment = ch.encode("utf-8")
        parts.append(fragment)
    port.charge(1)
    parts.append(b'"')
    _byte_work(port, encoded, len(parts) + 1)
    result = b"".join(parts)
    port.check()
    return result


def _compare_text(left: str, right: str, port: _BudgetPort) -> int:
    """Keys are exact bounded strings from the internal index constructor."""
    port.charge(1)
    stop = min(len(left), len(right))
    i = 0
    while i < stop:
        size = min(32, stop - i)  # both sides together <=256 UTF-8 bytes
        _byte_work(port, size * 8, 3)
        a, b = left[i:i + size], right[i:i + size]
        port.check()
        if a < b:
            port.check()
            return -1
        if a > b:
            port.check()
            return 1
        i += size
    port.check()
    return -1 if len(left) < len(right) else 1 if len(left) > len(right) else 0


def _sorted_pairs(pairs: object, port: _BudgetPort) -> tuple:
    """Stable bottom-up merge of bounded immutable key/value pairs. No callable
    key, implicit deduplication, record merge or recursive sequence sorting.
    """
    port.charge(1)
    if type(pairs) is not tuple:
        port.reject("type_or_enum_violation")
    n = len(pairs)
    if n > _MAX_PRIVATE_PAIRS:
        port.interrupt("WU9-L08")
    source = []
    for pair in pairs:
        port.charge(2)
        if type(pair) is not tuple or len(pair) != 2 or not _is_value(pair[1]):
            port.reject("type_or_enum_violation")
        _string_lengths(pair[0], port)
        source.append(pair)
    width = 1
    while width < n:
        port.charge(1)
        target = []
        for start in range(0, n, width * 2):
            i, middle, end = start, min(start + width, n), min(start + width * 2, n)
            j = middle
            while i < middle or j < end:
                if j == end or (i < middle and _compare_text(source[i][0], source[j][0], port) <= 0):
                    port.charge(1)
                    target.append(source[i])
                    i += 1
                else:
                    port.charge(1)
                    target.append(source[j])
                    j += 1
        source = target
        width *= 2
    port.charge(n + 1)
    result = tuple(source)
    port.check()
    return result


def _lookup_pair(pairs: tuple, key: object, port: _BudgetPort) -> tuple | None:
    """Binary lookup in a project-created sorted index. Duplicate/identity
    acceptance is W05 work. This helper never validates an entire index on use.
    """
    port.charge(1)
    if type(pairs) is not tuple:
        port.reject("type_or_enum_violation")
    _string_lengths(key, port)
    low, high = 0, len(pairs)
    while low < high:
        port.charge(1)
        mid = (low + high) // 2
        compare = _compare_text(pairs[mid][0], key, port)
        if compare < 0:
            low = mid + 1
        else:
            high = mid
    if low < len(pairs) and _compare_text(pairs[low][0], key, port) == 0:
        port.check()
        return pairs[low]
    port.check()
    return None
