# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: REPORT_PRESENTATION. Bounded SIT-RP-0.1 J encoding.

Only project-owned frozen report values reach this private seam. It grants no
input admission, public serialization, source projection or report delivery.
Each emitted byte is reserved before its allocation, through the supplied
same-context output port. Work is charged separately for each traversal,
comparison, conversion and copy. No renderer owns a clock or fresh budget.
"""
from ..contracts.bundle import _Number, _number_bytes, _compare_text
from ..contracts.execution import _byte_work
from ..contracts.report import _ReportMapping, _ReportContractError


_MAX_INTEGER = 9_007_199_254_740_991


def _require(ok):
    if not ok:
        raise _ReportContractError('invalid_report_contract') from None


class _NumericPort:
    """Retain the existing exact-number arithmetic without admission effects."""
    __slots__ = ('_port',)

    def __init__(self, port):
        self._port = port

    def charge(self, units):
        self._port.charge(units)

    def check(self):
        self._port.check()

    def reject(self, code, constraint=None):
        _require(False)

    def interrupt(self, limit_id):
        _require(False)


def _atom_length(atom, port):
    """Measure the admitted atom before the existing helper emits its token.

    Exponent magnitude is bounded before decimal conversion; candidate lengths
    are compared before any zero expansion. The longest actual token is 128.
    This measures the same representation as contracts.bundle._number_bytes.
    """
    port.charge(5)
    c, e, sign = atom.coefficient, atom.exponent, atom.sign
    _require(type(c) is str and type(e) is int and type(sign) is int)
    _require(type(atom.source_kind) is str and
             atom.source_kind in ('integer', 'decimal', 'binary_float'))
    _require(sign in (-1, 0, 1) and 1 <= len(c) <= 128)
    _byte_work(port, len(c), len(c) + 1)
    _require(all('0' <= ch <= '9' for ch in c))
    if c == '0':
        _require(sign == 0 and e == 0)
        return 1
    _require(sign != 0 and c[0] != '0' and c[-1] != '0')
    negative = int(sign < 0)
    n = len(c)
    if e >= 0:
        _require(e <= 16 and n + e <= 16)
        _byte_work(port, 32, 3)
        digits = c + '0' * e
        _require(len(digits) < 16 or digits <= '9007199254740991')
        port.check()
        return n + e + negative
    _require(e.bit_length() <= 432)
    _byte_work(port, 140, 3)
    exponent_length = len(str(e))
    point = n + e
    ordinary = n + 1 if point > 0 else 2 - point + n
    scientific = n + 1 + exponent_length
    length = min(ordinary, scientific) + negative
    _require(length <= 128)
    port.check()
    return length


def _sorted_report_pairs(value, port):
    """Charged stable bottom-up merge; no dict hashing or custom sort key."""
    port.charge(2)
    pairs = value._pairs
    _require(type(pairs) is tuple)
    source = []
    for pair in pairs:
        port.charge(3)
        _require(type(pair) is tuple and len(pair) == 2)
        _require(type(pair[0]) is str)
        source.append(pair)
    n, width = len(source), 1
    while width < n:
        port.charge(1)
        target = []
        for start in range(0, n, width * 2):
            i, middle, end = start, min(start + width, n), min(start + width * 2, n)
            j = middle
            while i < middle or j < end:
                if j == end or (i < middle and
                        _compare_text(source[i][0], source[j][0], port) <= 0):
                    port.charge(1)
                    target.append(source[i])
                    i += 1
                else:
                    port.charge(1)
                    target.append(source[j])
                    j += 1
        source = target
        width *= 2
    for position in range(1, n):
        port.charge(1)
        _require(_compare_text(source[position - 1][0], source[position][0], port) < 0)
    port.charge(n + 1)
    result = tuple(source)
    port.check()
    return result


def _escaped(code):
    return (code < 32 or 127 <= code <= 159 or code == 0x061C or
            0x200E <= code <= 0x200F or 0x2028 <= code <= 0x202E or
            0x2066 <= code <= 0x2069)


class _JWriter:
    """One bounded result buffer; partial fragments never escape on a stop."""
    __slots__ = ('_port', '_encoding', '_parts', '_length')

    def __init__(self, port, encoding):
        _require(type(encoding) is str and encoding in ('json', 'markdown'))
        port.charge(4)
        self._port = port
        self._encoding = encoding
        self._parts = []
        self._length = 0

    def _reserve(self, length):
        self._port.charge_output(self._encoding, length)

    def _retain(self, fragment):
        # The caller already paid the fragment's creation. Retention/counter
        # arithmetic are distinct from the eventual whole-buffer copy.
        self._port.charge(2)
        self._parts.append(fragment)
        self._length += len(fragment)

    def literal(self, fragment):
        # All callers supply fixed internal syntax bytes, never source bytes.
        self._reserve(len(fragment))
        _byte_work(self._port, len(fragment), 1)
        self._retain(fragment)

    def string(self, value):
        port = self._port
        self.literal(b'"')
        for start in range(0, len(value), 64):
            size = min(64, len(value) - start)
            _byte_work(port, size * 4, 2)
            block = value[start:start + size]
            port.check()
            # Each input block is <=256 UTF-8 bytes. Measure before allocating
            # its encoded counterpart; escapes can expand it to <=384 bytes.
            _byte_work(port, size * 4, size + 1)
            length = 0
            for char in block:
                code = ord(char)
                _require(not 0xD800 <= code <= 0xDFFF)
                length += (6 if _escaped(code) else 2 if char in ('"', '\\')
                           else 1 if code < 128 else 2 if code < 2048
                           else 3 if code < 65536 else 4)
            port.check()
            self._reserve(length)
            _byte_work(port, size * 4, 2 * size + 2)
            _byte_work(port, length, size + 1)
            parts = []
            for char in block:
                code = ord(char)
                if _escaped(code):
                    fragment = ('\\u%04x' % code).encode('ascii')
                elif char in ('"', '\\'):
                    fragment = ('\\' + char).encode('ascii')
                else:
                    fragment = char.encode('utf-8')
                parts.append(fragment)
            port.check()
            _byte_work(port, length, len(parts) + 1)
            fragment = b''.join(parts)
            port.check()
            self._retain(fragment)
        self.literal(b'"')

    def integer(self, value):
        port = self._port
        port.charge(3)
        _require(-_MAX_INTEGER <= value <= _MAX_INTEGER)
        # Conversion is bounded by the portable range. Decimal digits are
        # measured without creating the final textual/byte representation.
        _byte_work(port, 34, 2)
        remaining = -value if value < 0 else value
        length = 1 + int(value < 0)
        while remaining >= 10:
            _byte_work(port, 34, 1)
            remaining //= 10
            length += 1
        self._reserve(length)
        _byte_work(port, length * 2, 2)
        fragment = str(value).encode('ascii')
        port.check()
        self._retain(fragment)

    def atom(self, value):
        port = self._port
        length = _atom_length(value, port)
        self._reserve(length)
        port.charge(1)
        fragment = _number_bytes(value, _NumericPort(port))
        _require(len(fragment) == length)
        self._retain(fragment)

    def value(self, value):
        port = self._port
        port.charge(3)
        pending = [('visit', value)]
        active = set()
        while pending:
            port.charge(1)
            action, current = pending.pop()
            if action == 'object':
                pairs, position, identity = current
                if position == len(pairs):
                    self.literal(b'}')
                    port.charge(1)
                    active.remove(identity)
                    continue
                if position:
                    self.literal(b',')
                port.charge(1)
                key, child = pairs[position]
                self.string(key)
                self.literal(b':')
                port.charge(3)
                pending.append(('object', (pairs, position + 1, identity)))
                pending.append(('visit', child))
                continue
            if action == 'array':
                items, position, identity = current
                if position == len(items):
                    self.literal(b']')
                    port.charge(1)
                    active.remove(identity)
                    continue
                if position:
                    self.literal(b',')
                port.charge(3)
                pending.append(('array', (items, position + 1, identity)))
                pending.append(('visit', items[position]))
                continue
            kind = type(current)
            if current is None:
                self.literal(b'null')
            elif kind is bool:
                self.literal(b'true' if current else b'false')
            elif kind is int:
                self.integer(current)
            elif kind is str:
                self.string(current)
            elif kind is _Number:
                self.atom(current)
            elif kind is _ReportMapping or kind is tuple:
                port.charge(3)
                identity = id(current)
                _require(identity not in active)
                active.add(identity)
                if kind is _ReportMapping:
                    pairs = _sorted_report_pairs(current, port)
                    self.literal(b'{')
                    port.charge(2)
                    pending.append(('object', (pairs, 0, identity)))
                else:
                    self.literal(b'[')
                    port.charge(2)
                    pending.append(('array', (current, 0, identity)))
            else:
                _require(False)
        port.check()

    def finish(self):
        port = self._port
        _byte_work(port, self._length, len(self._parts) + 1)
        result = b''.join(self._parts)
        port.check()
        return result


def _encode_j(value, port, *, encoding='json'):
    """Encode a trusted frozen value as J, without a terminal line feed.

    Exact number atoms are internal scalar support, not new public report
    fields or accepted caller values. No arbitrary mapping/dataclass is read.
    """
    writer = _JWriter(port, encoding)
    writer.value(value)
    return writer.finish()
