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
import json
import re


_MAX_INTEGER = 9_007_199_254_740_991

# Fixed scalar transform selected by the frozen J profile. Values contain
# literal JSON escape text; no input-controlled mapping or callback is used.
_J_TRANSLATION = {
    0: "\\u0000",
    1: "\\u0001",
    2: "\\u0002",
    3: "\\u0003",
    4: "\\u0004",
    5: "\\u0005",
    6: "\\u0006",
    7: "\\u0007",
    8: "\\u0008",
    9: "\\u0009",
    10: "\\u000a",
    11: "\\u000b",
    12: "\\u000c",
    13: "\\u000d",
    14: "\\u000e",
    15: "\\u000f",
    16: "\\u0010",
    17: "\\u0011",
    18: "\\u0012",
    19: "\\u0013",
    20: "\\u0014",
    21: "\\u0015",
    22: "\\u0016",
    23: "\\u0017",
    24: "\\u0018",
    25: "\\u0019",
    26: "\\u001a",
    27: "\\u001b",
    28: "\\u001c",
    29: "\\u001d",
    30: "\\u001e",
    31: "\\u001f",
    34: "\\\"",
    92: "\\\\",
    127: "\\u007f",
    128: "\\u0080",
    129: "\\u0081",
    130: "\\u0082",
    131: "\\u0083",
    132: "\\u0084",
    133: "\\u0085",
    134: "\\u0086",
    135: "\\u0087",
    136: "\\u0088",
    137: "\\u0089",
    138: "\\u008a",
    139: "\\u008b",
    140: "\\u008c",
    141: "\\u008d",
    142: "\\u008e",
    143: "\\u008f",
    144: "\\u0090",
    145: "\\u0091",
    146: "\\u0092",
    147: "\\u0093",
    148: "\\u0094",
    149: "\\u0095",
    150: "\\u0096",
    151: "\\u0097",
    152: "\\u0098",
    153: "\\u0099",
    154: "\\u009a",
    155: "\\u009b",
    156: "\\u009c",
    157: "\\u009d",
    158: "\\u009e",
    159: "\\u009f",
    1564: "\\u061c",
    8206: "\\u200e",
    8207: "\\u200f",
    8232: "\\u2028",
    8233: "\\u2029",
    8234: "\\u202a",
    8235: "\\u202b",
    8236: "\\u202c",
    8237: "\\u202d",
    8238: "\\u202e",
    8294: "\\u2066",
    8295: "\\u2067",
    8296: "\\u2068",
    8297: "\\u2069",
}
_J_SCALAR_CLASSES = (
    r'(?P<short>["\\]+)|'
    r'(?P<escape>[\x00-\x1f\x7f-\x9f\u061c\u200e-\u200f\u2028-\u202e\u2066-\u2069]+)|'
    r'(?P<bad>[\ud800-\udfff]+)|'
    r'(?P<two>[\u00a0-\u061b\u061d-\u07ff]+)|'
    r'(?P<three>[\u0800-\u200d\u2010-\u2027\u202f-\u2065\u206a-\ud7ff\ue000-\uffff]+)|'
    r'(?P<four>[\U00010000-\U0010ffff]+)'
)
_J_WIDTHS = {'short': 2, 'escape': 6, 'two': 2, 'three': 3, 'four': 4}




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


class _CachedEncodingPort:
    """One finalization's paid ordering of immutable representation objects.

    Analytical jobs have already ended. This stores only exact frozen mapping
    identities and already charged sorted pairs, never source interpretations.
    The context is local to one encoding pair and is never delivered or global.
    Every consumption and all actual encoding/comparison still debit the same
    original restricted port. This object cannot start a budget or a job.
    """
    __slots__ = ('_port', '_pairs')

    def __init__(self, port):
        port.charge(3)
        self._port = port
        self._pairs = {}

    @property
    def _owner(self):
        return self._port._owner

    def charge(self, units):
        self._port.charge(units)

    def check(self):
        self._port.check()

    def charge_output(self, encoding, length):
        self._port.charge_output(encoding, length)


def _sorted_report_pairs(value, port):
    """Charged stable bottom-up merge; no dict hashing or custom sort key."""
    port.charge(2)
    cache = type(port) is _CachedEncodingPort
    if cache:
        port.charge(3)
        key = id(value)
        existing = port._pairs.get(key)
        if existing is not None:
            port.charge(2)
            _require(existing[0] is value)
            port.check()
            return existing[1]
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
    if cache:
        port.charge(4)
        port._pairs[key] = (value, result)
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
            # Native scans are charged by their bounded byte passes. Ordinary
            # ASCII needs no per-character Python object construction. These
            # disjoint fixed classes count exact UTF-8/escape output width.
            _byte_work(port, size * 4, 2)
            length = size
            matches = re.finditer(_J_SCALAR_CLASSES, block)
            while True:
                port.charge(1)
                match = next(matches, None)
                if match is None:
                    break
                _byte_work(port, 32, 3)
                kind = match.lastgroup
                _require(kind != 'bad')
                _byte_work(port, 128, 4)
                length += (match.end() - match.start()) * (_J_WIDTHS[kind] - 1)
                port.check()
            port.check()
            self._reserve(length)
            # Reserve before either transformed text or encoded bytes exists.
            # Translation reads the scalar block and writes at most length
            # Unicode scalars. UTF-8 encoding is a separately paid pass.
            _byte_work(port, size * 4, 1)
            _byte_work(port, length * 4, 1)
            translated = block.translate(_J_TRANSLATION)
            port.check()
            _byte_work(port, length * 4, 1)
            _byte_work(port, length, 1)
            fragment = translated.encode('utf-8')
            port.check()
            _require(len(fragment) == length)
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


class _CheckingWriter(_JWriter):
    """Compare a frozen value with one completed output, by bounded fragments.

    This pass consumes ordinary work on the original port. It creates no
    second complete output and does not count the same retained bytes twice
    against L14. Each prospective temporary fragment is bounded by the bytes
    remaining in the completed output before its allocation.
    """
    __slots__ = ('_expected',)

    def __init__(self, port, encoding, expected):
        _require(type(expected) is bytes)
        _require(type(encoding) is str and encoding in ('json', 'markdown'))
        port.charge(5)
        self._port = port
        self._encoding = encoding
        self._parts = []
        self._length = 0
        self._expected = expected

    def _reserve(self, length):
        self._port.charge(3)
        _require(type(length) is int and 0 <= length <= len(self._expected) - self._length)

    def _retain(self, fragment):
        port = self._port
        port.charge(3)
        _require(type(fragment) is bytes)
        end = self._length + len(fragment)
        _require(end <= len(self._expected))
        _byte_work(port, len(fragment), 2)
        expected = self._expected[self._length:end]
        _byte_work(port, 2 * len(fragment), 1)
        _require(fragment == expected)
        self._length = end
        port.check()

    def string(self, value):
        """Decode one bounded existing scalar instead of re-encoding it.

        Framing is still checked against the fixed document walk. Only a JSON
        string token reaches the native decoder, never a container, number or
        callback. All scanning, decoding, copying and comparison passes debit
        this invocation. The original renderer owns exact J escape spelling;
        this separate check establishes the decoded scalar's complete meaning.
        """
        port = self._port
        port.charge(5)
        _require(type(value) is str)
        start = self._length
        _require(start < len(self._expected) and self._expected[start] == 34)
        # J uses at most six bytes per source scalar, plus its two quotes.
        ceiling = min(len(self._expected), start + 6 * len(value) + 2)
        position, escaped, end = start + 1, False, None
        while position < ceiling and end is None:
            size = min(256, ceiling - position)
            _byte_work(port, size, 3)
            block = self._expected[position:position + size]
            _byte_work(port, size, 1)
            for offset, byte in enumerate(block):
                if escaped:
                    escaped = False
                elif byte == 92:
                    escaped = True
                elif byte == 34:
                    end = position + offset + 1
                    break
            position += size
            port.check()
        _require(end is not None)
        length = end - start
        _byte_work(port, length, 2)
        token = self._expected[start:end]
        # UTF-8 decoding and JSON string decoding are two distinct passes.
        _byte_work(port, length, 1)
        _byte_work(port, length, 2)
        decoded = json.loads(token)
        port.check()
        _require(type(decoded) is str)
        _byte_work(port, 4 * len(value), 1)
        _byte_work(port, 4 * len(decoded), 1)
        _require(value == decoded)
        port.charge(1)
        self._length = end
        port.check()

    def finish(self):
        self._port.charge(2)
        _require(self._length == len(self._expected))
        self._port.check()


def _encode_j(value, port, *, encoding='json'):
    """Encode a trusted frozen value as J, without a terminal line feed.

    Exact number atoms are internal scalar support, not new public report
    fields or accepted caller values. No arbitrary mapping/dataclass is read.
    """
    writer = _JWriter(port, encoding)
    writer.value(value)
    return writer.finish()


def _repeat_syntax(writer, token, count):
    """Emit a tool-owned one-byte fence/indent token after its exact reserve."""
    _require(type(token) is bytes and token in (b' ', b'`'))
    _require(type(count) is int and count >= 0)
    writer._reserve(count)
    _byte_work(writer._port, count, 2)
    fragment = token * count
    writer._port.check()
    writer._retain(fragment)


def _fence_length(value, port):
    """Scan the frozen value for the exact longest backtick run in pretty J.

    J preserves literal backticks inside strings, while every string boundary
    contains a quote and container syntax contains no backtick. A run can cross
    scan blocks within one string, but cannot cross distinct strings or keys.
    No encoded body is allocated or charged to an output counter by this pass.
    """
    port.charge(3)
    pending = [('visit', value)]
    active = set()
    longest = 0
    while pending:
        port.charge(1)
        action, current = pending.pop()
        if action == 'leave':
            port.charge(1)
            active.remove(current)
            continue
        if action == 'object':
            pairs, position = current
            if position < len(pairs):
                port.charge(2)
                pair = pairs[position]
                _require(type(pair) is tuple and len(pair) == 2 and type(pair[0]) is str)
                port.charge(3)
                pending.append(('object', (pairs, position + 1)))
                pending.append(('visit', pair[1]))
                pending.append(('visit', pair[0]))
            continue
        if action == 'array':
            items, position = current
            if position < len(items):
                port.charge(3)
                pending.append(('array', (items, position + 1)))
                pending.append(('visit', items[position]))
            continue
        kind = type(current)
        if kind is str:
            # Two fixed linear native scans, each prepaid at the conservative
            # UTF-8 bound. No per-character objects or encoded body are copied.
            _byte_work(port, 4 * len(current), 3)
            _require(re.search(r'[\ud800-\udfff]', current) is None)
            port.check()
            _byte_work(port, 4 * len(current), 2)
            matches = re.finditer('`+', current)
            while True:
                port.charge(1)
                match = next(matches, None)
                if match is None:
                    break
                _byte_work(port, 128, 4)
                longest = max(longest, match.end() - match.start())
                port.check()
            port.check()
        elif kind is _ReportMapping or kind is tuple:
            port.charge(3)
            identity = id(current)
            _require(identity not in active)
            active.add(identity)
            port.charge(2)
            pending.append(('leave', identity))
            if kind is _ReportMapping:
                _require(type(current._pairs) is tuple)
                pending.append(('object', (current._pairs, 0)))
            else:
                pending.append(('array', (current, 0)))
        else:
            _require(current is None or kind is bool or kind is int or kind is _Number)
    port.check()
    return max(3, longest + 1)


def _write_pretty_j(writer, value):
    """Emit pretty J directly into the caller's one counted output buffer."""
    port = writer._port
    port.charge(3)
    pending = [('visit', (value, 0))]
    active = set()
    while pending:
        port.charge(1)
        action, current = pending.pop()
        if action == 'object':
            pairs, position, depth, identity = current
            if position == len(pairs):
                writer.literal(b'\n')
                _repeat_syntax(writer, b' ', 2 * depth)
                writer.literal(b'}')
                port.charge(1)
                active.remove(identity)
                continue
            if position:
                writer.literal(b',\n')
            _repeat_syntax(writer, b' ', 2 * (depth + 1))
            port.charge(1)
            key, child = pairs[position]
            writer.string(key)
            writer.literal(b': ')
            port.charge(3)
            pending.append(('object', (pairs, position + 1, depth, identity)))
            pending.append(('visit', (child, depth + 1)))
            continue
        if action == 'array':
            items, position, depth, identity = current
            if position == len(items):
                writer.literal(b'\n')
                _repeat_syntax(writer, b' ', 2 * depth)
                writer.literal(b']')
                port.charge(1)
                active.remove(identity)
                continue
            if position:
                writer.literal(b',\n')
            _repeat_syntax(writer, b' ', 2 * (depth + 1))
            port.charge(3)
            pending.append(('array', (items, position + 1, depth, identity)))
            pending.append(('visit', (items[position], depth + 1)))
            continue
        value, depth = current
        kind = type(value)
        if value is None:
            writer.literal(b'null')
        elif kind is bool:
            writer.literal(b'true' if value else b'false')
        elif kind is int:
            writer.integer(value)
        elif kind is str:
            writer.string(value)
        elif kind is _Number:
            writer.atom(value)
        elif kind is _ReportMapping or kind is tuple:
            port.charge(3)
            identity = id(value)
            _require(identity not in active)
            active.add(identity)
            if kind is _ReportMapping:
                pairs = _sorted_report_pairs(value, port)
                if not pairs:
                    writer.literal(b'{}')
                    port.charge(1)
                    active.remove(identity)
                else:
                    writer.literal(b'{\n')
                    port.charge(2)
                    pending.append(('object', (pairs, 0, depth, identity)))
            elif not value:
                writer.literal(b'[]')
                port.charge(1)
                active.remove(identity)
            else:
                writer.literal(b'[\n')
                port.charge(2)
                pending.append(('array', (value, 0, depth, identity)))
        else:
            _require(False)
    port.check()


def _encode_pretty_j(value, port, *, encoding='markdown'):
    """Private pretty-J component, with no terminal LF or Markdown framing."""
    writer = _JWriter(port, encoding)
    _write_pretty_j(writer, value)
    return writer.finish()
