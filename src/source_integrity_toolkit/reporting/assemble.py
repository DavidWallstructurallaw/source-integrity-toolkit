# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Bounded formal report assembly, without analysis, disclosure selection or I/O.

Owner: REPORT_PRESENTATION.  The internal seam consumes a completed private
outcome and the explicitly selected disclosure contract.  It returns only a
frozen logical document.  AuditReport delivery, encoders, and public invocation
remain the later owners' responsibility.
"""
from dataclasses import dataclass

from ..contracts import report as _c
from ..contracts import results as _r
from ..contracts.bundle import _Object, _Array, _Number, _j_scalar
from ..contracts.evidence import _PreparedBundle
from ..contracts.execution import _byte_work, _PreparationAborted, _AnalysisAborted

_PREFIXES = (('scopes', 'SIT-SCP-'), ('populations', 'SIT-POP-'),
    ('basis_index', 'SIT-BAS-'), ('capabilities', 'SIT-CAP-'),
    ('checks', 'SIT-CHK-'), ('results', 'SIT-RES-'),
    ('findings', 'SIT-FND-'), ('reasons', 'SIT-RSN-'))
_SCOPE_NOTE = ('Every planned field and exact represented scope for this Inquiry remains '
    'separately linked; no strongest-result summary or outside-world completeness is inferred.')
_FINDING_LIMIT = ('Conditional on the exact supplied scope, versions, premises and evidence basis. '
    'This finite observation cannot establish motive, censorship, authenticity, substantive truth, '
    'independence outside the examined dimension, causal success or a universal threat verdict. '
    'Threat associations are nonexclusive explanatory links, with no incident total or severity. '
    'No source contact, quarantine, removal, down-weighting, sanction or other intervention follows.')
_PATH_LIMIT = ('Citation and material paths do not create Claim-specific acquisition '
    'dependence, independent corroboration or a syndication accusation.')


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _WitnessLinks:
    refs: tuple
    result_ref: object


def _require(ok):
    _c._report_require(ok)


def _field(value, name, port):
    _require(type(value) in (_Object, _c._ReportMapping))
    pairs = value.items if type(value) is _Object else value._pairs
    for key, child in pairs:
        _byte_work(port, 4 * (len(name) + len(key)), 2)
        if key == name:
            return child
    raise _c._ReportContractError('invalid_report_contract')


def _plain(value, port):
    """Copy an already selected immutable JSON value; no source record dump."""
    port.charge(1)
    if value is None or type(value) in (str, bool, int):
        if type(value) is str:
            _byte_work(port, 4 * len(value), 1)
        return value
    if type(value) in (_Object, _c._ReportMapping):
        pairs = value.items if type(value) is _Object else value._pairs
        result = {}
        for key, child in pairs:
            _byte_work(port, 4 * len(key), 3)
            result[key] = _plain(child, port)
        return result
    if type(value) is _Array:
        value = value.items
    if type(value) is tuple:
        return tuple(_plain(child, port) for child in value)
    if type(value) is _Number:
        _require(value.exponent >= 0 and len(value.coefficient) + value.exponent <= 16)
        _byte_work(port, 17, 5)
        number = value.sign * int(value.coefficient) * (10 ** value.exponent)
        _require(-9007199254740991 <= number <= 9007199254740991)
        return number
    raise _c._ReportContractError('invalid_report_contract')


def _charge_key(key, port):
    if type(key) is bytes:
        _byte_work(port, len(key), 1)
    elif type(key) is tuple:
        port.charge(len(key) + 1)
        for child in key:
            _charge_key(child, port)
    else:
        _c._key_charge(key, port)



def _compare_key(left, right, port):
    """Lexicographic comparison charges only the actually visited prefixes."""
    port.charge(2)
    if left is right:
        return 0
    _require(type(left) is type(right))
    if type(left) is tuple:
        for a, b in zip(left, right):
            order = _compare_key(a, b, port)
            if order:
                return order
        port.charge(2)
        return -1 if len(left) < len(right) else 1 if len(left) > len(right) else 0
    if type(left) in (str, bytes):
        step = 32 if type(left) is str else 128
        size = min(len(left), len(right))
        for start in range(0, size, step):
            end = min(start + step, size)
            _byte_work(port, (end - start) * (8 if type(left) is str else 2), 5)
            a, b = left[start:end], right[start:end]
            if a != b:
                return -1 if a < b else 1
        port.charge(2)
        return -1 if len(left) < len(right) else 1 if len(left) > len(right) else 0
    _require(type(left) in (int, bool) or left is None)
    port.charge(2)
    return -1 if left < right else 1 if left > right else 0


def _sort(values, port):
    """Prospectively charged stable merge, including long tie-body bytes."""
    port.charge(len(values) + 1)
    source = list(values)
    width = 1
    while width < len(source):
        target = []
        for start in range(0, len(source), width * 2):
            port.charge(4)
            middle, end = min(start + width, len(source)), min(start + width * 2, len(source))
            left, right = start, middle
            while left < middle or right < end:
                port.charge(4)
                if left < middle and right < end:
                    take = _compare_key(source[left], source[right], port) <= 0
                else:
                    take = left < middle
                if take:
                    target.append(source[left]); left += 1
                else:
                    target.append(source[right]); right += 1
        source = target
        width *= 2
    return _c._paid_tuple(source, port)


def _j_key(value, port):
    """J of an ID-free semantic key, never an exported report encoding."""
    port.charge(1)
    if value is None or type(value) in (str, bool):
        return _j_scalar(value, port)
    if type(value) is int:
        _require(-9007199254740991 <= value <= 9007199254740991)
        _byte_work(port, 17, 3)
        return str(value).encode('ascii')
    if type(value) is tuple:
        pieces = [_j_key(child, port) for child in value]
        port.charge(len(pieces) + 2)
        length = sum(len(part) for part in pieces) + len(pieces) + 2
        _byte_work(port, length, len(pieces) + 2)
        return b'[' + b','.join(pieces) + b']'
    _require(type(value) is dict)
    keys = _sort(list(value), port)
    pieces = []
    for name in keys:
        port.charge(3)
        pieces.append(_j_scalar(name, port) + b':' + _j_key(value[name], port))
    length = sum(len(part) for part in pieces) + len(pieces) + 2
    _byte_work(port, length, len(pieces) + 2)
    return b'{' + b','.join(pieces) + b'}'


def _input(ref, port):
    _require(type(ref) is _r._InputRef)
    _c._charge_input_ref(ref, port)
    return {'collection': ref.collection, 'identifier': ref.identifier, 'selector': ref.selector}


def _anchor(value, port):
    """Finite keys terminate at Result anchors, including cyclic Reasons."""
    if type(value) is _c._PrivateFinding:
        return ('finding', value.condition_code, value.observation_kind,
                _anchor(value.scope_ref, port),
                _sort([_c._slot_key(ref, port) for ref in value.witness.input_refs], port))
    if type(value) is _c._Capability:
        port.charge(3)
        return ('capability', value.inquiry_ref, value.family)
    _require(type(value) in (_r._InputRef, _r._Scope, _r._Population, _r._BasisRef,
        _r._ResultRef, _r._WitnessRef, _r._Reason, _r._PrerequisiteCheck))
    if type(value) is _r._Scope:
        _c._charge_scope(value, port)
        key = value._key()
        _charge_key(key, port)
        return key
    return _c._slot_key(value, port)


class _Assembly:
    def __init__(self, outcome, selection, port):
        self.outcome, self.selection, self.port = outcome, selection, port
        self.rows = {name: [] for name, unused in _PREFIXES}
        self.objects, self.result_slots, self.basis_slots = {}, {}, {}
        self.selected, self.used = {}, set()
        self.witness_targets = {}
        self.identities, self.identifiers = {}, {}
        self.scope_keys = {}
        self.scope_identities = {}
        self.reference_tokens = {}
        for kind, entries in (('basis', selection.basis_entries),
                ('disclosure', selection.disclosures), ('finding', selection.finding_witnesses),
                ('owner', selection.owner_witnesses)):
            for owner, body in entries:
                port.charge(4)
                key = _anchor(owner, port) if kind in ('basis', 'disclosure') else id(owner)
                _charge_key(key, port)
                _require((kind, key) not in self.selected)
                self.selected[(kind, key)] = body

    def choose(self, kind, owner):
        key = _anchor(owner, self.port) if kind in ('basis', 'disclosure') else id(owner)
        _charge_key(key, self.port)
        self.port.charge(4)
        _require((kind, key) in self.selected)
        self.used.add((kind, key))
        return self.selected[(kind, key)]

    def add(self, kind, owner, anchor, body):
        self.port.charge(5)
        token = id(owner)
        if token in self.objects:
            return self.objects[token]
        row = {'kind': kind, 'owner': owner, 'anchor': anchor, 'body': body}
        self.rows[kind].append(row)
        self.objects[token] = row
        return row

    def ordered(self, refs):
        buckets, seen = {}, set()
        for ref in refs:
            self.port.charge(4)
            if id(ref) in seen:
                continue
            seen.add(id(ref))
            anchor = _anchor(ref, self.port)
            _charge_key(anchor, self.port)
            buckets.setdefault(anchor, []).append(ref)
        result = []
        for anchor in _sort(list(buckets), self.port):
            group = buckets[anchor]
            if len(group) == 1 or type(group[0]) in (_r._InputRef, _r._BasisRef, _r._ResultRef, _r._WitnessRef):
                result.append(group[0])
                continue
            bodies = {}
            for ref in group:
                key = _c._semantic_key(ref, self.port)
                _charge_key(key, self.port)
                bodies.setdefault(key, ref)
            for key in _sort(list(bodies), self.port):
                result.append(bodies[key])
        return _c._paid_tuple(result, self.port)

    def scope(self, value):
        if id(value) in self.objects:
            return
        self.add('scopes', value, _anchor(value, self.port), {
            'inquiry_ref': value.inquiry_ref, 'claim_refs': self.ordered(value.claim_refs),
            'target_refs': self.ordered(value.target_refs),
            'dependency_dimension': value.dependency_dimension, 'graph_view': value.graph_view,
            'temporal_basis': value.temporal_basis,
            'requested_time': None if value.requested_time is None else _plain(value.requested_time.fields, self.port),
            'coverage_refs': self.ordered(value.coverage_refs), 'qualifications': value.qualifications})

    def basis(self, value):
        if id(value) in self.objects:
            return
        chosen = self.choose('basis', value)
        anchor = _anchor(value, self.port)
        _charge_key(anchor, self.port)
        self.port.charge(2)
        if anchor in self.basis_slots:
            self.objects[id(value)] = self.basis_slots[anchor]
            return
        body = {name: child for name, child in chosen._pairs}
        self.port.charge(len(body) + 2)
        body['source'] = value.source
        self.basis_slots[anchor] = self.add('basis_index', value, anchor, body)

    def population(self, value):
        if id(value) in self.objects:
            return
        self.scope(value.scope)
        for ref in value.basis_refs:
            self.basis(ref)
        members = []
        for member in value.member_refs:
            self.port.charge(1)
            members.append({'case_ref': member.case_ref, 'before_ref': member.before_ref}
                if type(member) is _r._CaseTarget else member)
        indexed = [((_c._slot_key(original, self.port)), i) for i, original in enumerate(value.member_refs)]
        members = tuple(members[i] for unused, i in _sort(indexed, self.port))
        self.add('populations', value, _anchor(value, self.port), {
            'scope_ref': value.scope, 'unit': value.unit, 'member_refs': members,
            'selection_rule': value.selection_rule, 'coverage_refs': self.ordered(value.coverage_refs),
            'basis_refs': self.ordered(value.basis_refs), 'membership_state': value.membership_state,
            'qualifications': value.qualifications})

    def reason(self, value):
        if id(value) in self.objects:
            return
        self.scope(value.scope)
        self.add('reasons', value, _anchor(value, self.port), {
            'code': value.code, 'scope_ref': value.scope,
            'affected_result_refs': self.ordered(value.affected_result_refs),
            'input_refs': self.ordered(value.input_refs), 'detail': value.detail,
            'classification': value.classification})

    def check(self, value):
        if id(value) in self.objects:
            return
        self.scope(value.result_ref.scope)
        for reason in value.reason_refs:
            self.reason(reason)
        self.add('checks', value, _anchor(value, self.port), {
            'check_id': value.check_id, 'scope_ref': value.result_ref.scope,
            'state': value.state, 'input_refs': self.ordered(value.input_refs),
            'reason_refs': self.ordered(value.reason_refs), 'note': value.note})

    def partition(self, value):
        categories = []
        for category in value.categories:
            self.port.charge(3)
            members = []
            for member in category.member_refs:
                self.port.charge(1)
                members.append({'case_ref': member.case_ref, 'before_ref': member.before_ref}
                    if type(member) is _r._CaseTarget else member)
            order = _sort([(_c._slot_key(m, self.port), i) for i, m in enumerate(category.member_refs)], self.port)
            categories.append({'label': category.label, 'member_refs': tuple(members[i] for unused, i in order),
                               'count': category.count})
        return {'population_ref': value.population,
                'categories': tuple(categories),
                'total': len(value.population.member_refs)}

    def value(self, result):
        value, kind = result.value, result.value_kind
        if value is None:
            return None
        if kind == 'count':
            return value.value
        if kind == 'fraction':
            return {'numerator': value.numerator, 'denominator': value.denominator}
        if kind == 'completion_interval':
            return {'lower': {'numerator': value.lower.numerator, 'denominator': value.lower.denominator},
                'upper': {'numerator': value.upper.numerator, 'denominator': value.upper.denominator},
                'population_ref': value.lower.population, 'interval_kind': value.interval_kind,
                'partition': self.partition(value.partition)}
        if kind == 'partition':
            return self.partition(value)
        if kind == 'incidence':
            memberships, origins = [], {}
            for member in value.memberships:
                self.port.charge(3)
                memberships.append({'member_ref': member.member_ref,
                                    'origin_refs': self.ordered(member.origin_refs)})
                for origin in member.origin_refs:
                    key = _anchor(origin, self.port)
                    _charge_key(key, self.port)
                    self.port.charge(3)
                    if key not in origins:
                        origins[key] = (origin, [])
                    origins[key][1].append(member.member_ref)
            order = _sort([(_anchor(row['member_ref'], self.port), i) for i, row in enumerate(memberships)], self.port)
            counts = []
            for key in _sort(list(origins), self.port):
                origin, members = origins[key]
                counts.append({'origin_ref': origin, 'count': len(members), 'member_refs': self.ordered(members)})
            return {'population_ref': value.population, 'memberships': tuple(memberships[i] for unused, i in order),
                'origin_counts': tuple(counts), 'total': len(memberships), 'nonexclusive': True}
        if kind == 'record_disclosures':
            selected = self.choose('disclosure', result.ref)
            records = _field(selected, 'records', self.port)
            _check_disclosure_sources(result, records, self)
            return {'records': records}
        _require(kind == 'witness_collection')
        return {'witness_refs': _WitnessLinks(value.witness_refs, result.ref)}

    def result(self, value):
        self.scope(value.ref.scope)
        for item in value.population_refs:
            self.population(item)
        for item in value.basis_refs:
            self.basis(item)
        for item in value.check_refs:
            self.check(item)
        for item in value.reason_refs:
            self.reason(item)
        row = self.add('results', value, _anchor(value.ref, self.port), {
            'diagnostic_id': value.ref.diagnostic_id, 'field_key': value.ref.field_key,
            'scope_ref': value.ref.scope, 'population_refs': self.ordered(value.population_refs),
            'execution_state': value.execution_state, 'result_state': value.result_state,
            'result_origin': value.result_origin, 'value_kind': value.value_kind,
            'value': self.value(value), 'check_refs': self.ordered(value.check_refs),
            'basis_refs': self.ordered(value.basis_refs),
            'witness_refs': _WitnessLinks(value.witness_refs, value.ref),
            'reason_refs': self.ordered(value.reason_refs), 'interpretation_limit': value.interpretation_limit})
        key = row['anchor']
        _charge_key(key, self.port)
        self.port.charge(2)
        self.result_slots.setdefault(key, []).append(row)

    def finding(self, value):
        self.scope(value.scope_ref)
        for item in value.population_refs:
            self.population(item)
        for item in value.basis_refs:
            self.basis(item)
        for item in value.reason_refs:
            self.reason(item)
        witness = self.choose('finding', value)
        _check_finding_witness(value, witness, self)
        self.add('findings', value, _anchor(value, self.port), {
            'observation_kind': value.observation_kind, 'condition_code': value.condition_code,
            'diagnostic_refs': _sort(list(value.diagnostic_refs), self.port),
            'threat_family_refs': _sort(list(value.threat_family_refs), self.port),
            'scope_ref': value.scope_ref, 'population_refs': self.ordered(value.population_refs),
            'basis_refs': self.ordered(value.basis_refs), 'witness': witness,
            'contrary_input_refs': self.ordered(value.contrary_input_refs),
            'reason_refs': self.ordered(value.reason_refs), 'statement': value.statement,
            'interpretation_limit': value.interpretation_limit})

    def semantic(self, value):
        self.port.charge(1)
        if value is None or type(value) in (str, bool, int):
            if type(value) is str:
                _byte_work(self.port, 4 * len(value), 1)
            return value
        if type(value) is _r._InputRef:
            return _input(value, self.port)
        if type(value) is _c._ReportMapping:
            return {name: self.semantic(child) for name, child in value._pairs}
        if type(value) is dict:
            return {name: self.semantic(child) for name, child in value.items()}
        if type(value) is _WitnessLinks:
            return tuple(_anchor(ref, self.port) for ref in self.ordered(value.refs))
        if type(value) is tuple:
            return tuple(self.semantic(child) for child in value)
        if type(value) not in (_r._ResultRef, _r._WitnessRef) and id(value) in self.objects:
            row = self.objects[id(value)]
            self.port.charge(2)
            return self.reference_tokens.get(id(row['owner']), (row['anchor'], None))
        return ((self.result_anchor(value) if type(value) is _r._ResultRef else _anchor(value, self.port)), None)

    def scope_identity(self, scope):
        row = self.objects[id(scope)]
        self.port.charge(2)
        token = id(row['owner'])
        if token not in self.scope_identities:
            anchor, tie = self.identities[token]
            # UTF-8 J bytes and their decoded Unicode text have the same
            # lexicographic order; the latter is also a legal ID-free J leaf.
            _byte_work(self.port, len(tie), 3)
            self.scope_identities[token] = (anchor, tie.decode('utf-8'))
        return self.scope_identities[token]

    def result_anchor(self, ref):
        key = _anchor(ref, self.port)
        if id(ref.scope) in self.objects and id(self.objects[id(ref.scope)]['owner']) in self.identities:
            return key[:3] + (self.scope_identity(ref.scope),)
        return key

    def sorting_anchor(self, row):
        anchor, owner, kind = row['anchor'], row['owner'], row['kind']
        if kind == 'populations':
            return (anchor[0], self.scope_identity(owner.scope)) + anchor[2:]
        if kind == 'results':
            return self.result_anchor(owner.ref)
        if kind == 'checks':
            return (anchor[0], anchor[1], self.result_anchor(owner.result_ref))
        if kind == 'reasons':
            return anchor[:2] + (self.scope_identity(owner.scope),) + anchor[3:]
        if kind == 'findings':
            return anchor[:3] + (self.scope_identity(row['body']['scope_ref']),) + anchor[4:]
        return anchor

    def identities_for_rows(self):
        # Resolve finite explanatory identities in dependency order. ResultRef
        # terminates at its slot anchor, so Reason/Result cycles do not expand.
        # A linked full body is relevant only when its anchor has more than one
        # distinct meaning; unique source Basis metadata is never recursively
        # re-encoded inside every Finding's tie-break key.
        order = ('scopes', 'populations', 'reasons', 'checks', 'basis_index',
                 'results', 'findings', 'capabilities')
        prefixes = dict(_PREFIXES)
        for kind in order:
            prefix, buckets = prefixes[kind], {}
            if kind == 'results':
                for slot, rows in self.result_slots.items():
                    if len(rows) > 1:
                        previous = None
                        for row in rows:
                            body = _j_key(self.semantic(row['body']), self.port)
                            if previous is not None:
                                _byte_work(self.port, len(body) + len(previous), 1)
                                _require(body == previous)
                            previous = body
            for row in self.rows[kind]:
                anchor = self.sorting_anchor(row)
                _charge_key(anchor, self.port)
                self.port.charge(3)
                buckets.setdefault(anchor, []).append(row)
            unique = {}
            for anchor in _sort(list(buckets), self.port):
                group, bodies, previous = buckets[anchor], {}, None
                for row in group:
                    semantic = self.semantic(row['body']) if len(group) > 1 else None
                    tie = _j_key(semantic, self.port) if semantic is not None else b''
                    key = (anchor, tie)
                    _charge_key(key, self.port)
                    self.port.charge(4)
                    if kind == 'results' and previous is not None:
                        _require(key == previous)
                    previous = key
                    self.identities[id(row['owner'])] = key
                    unique.setdefault(key, row)
                    bodies.setdefault(tie, semantic)
                ambiguous = len(bodies) > 1
                for row in group:
                    identity = self.identities[id(row['owner'])]
                    self.port.charge(3)
                    self.reference_tokens[id(row['owner'])] = (
                        (anchor, bodies[identity[1]]) if ambiguous else (anchor, None))
            ordered = []
            for index, key in enumerate(_sort(list(unique), self.port)):
                self.port.charge(5)
                _byte_work(self.port, 17, 2)
                self.identifiers[(kind, key)] = prefix + str(index + 1).zfill(6)
                ordered.append(unique[key])
            self.rows[kind] = ordered

    def resolve_link(self, value):
        if type(value) is _r._ResultRef:
            key = _anchor(value, self.port)
            _charge_key(key, self.port)
            _require(key in self.result_slots)
            row = self.result_slots[key][0]
            actual = row['owner'].ref
            if value is not actual:
                left, right = _c._semantic_key(value, self.port), _c._semantic_key(actual, self.port)
                _charge_key((left, right), self.port)
                _require(left == right)
        else:
            self.port.charge(2)
            _require(id(value) in self.objects)
            row = self.objects[id(value)]
        key = self.identities[id(row['owner'])]
        _charge_key(key, self.port)
        return self.identifiers[(row['kind'], key)]

    def witness_links(self, refs, result_ref):
        result = []
        for ref in refs:
            key = _anchor(ref, self.port)
            _charge_key(key, self.port)
            _require(key in self.witness_targets)
            self.port.charge(len(self.witness_targets[key]) + 1)
            for owner in self.witness_targets[key]:
                if type(owner) is _c._PrivateFinding and owner.result_refs:
                    wanted = _anchor(result_ref, self.port)
                    if not any(_anchor(ref, self.port) == wanted for ref in owner.result_refs):
                        continue
                result.append(self.resolve_link(owner))
        return self.strings(result)

    def strings(self, values):
        result, previous = [], None
        for value in _sort(list(values), self.port):
            _byte_work(self.port, 4 * len(value), 2)
            if value != previous:
                result.append(value)
                previous = value
        return tuple(result)

    def resolve(self, value, name=None):
        self.port.charge(1)
        if value is None or type(value) in (str, bool, int):
            if type(value) is str:
                _byte_work(self.port, 4 * len(value), 1)
            return value
        if type(value) is _r._InputRef:
            return _input(value, self.port)
        if type(value) is _c._ReportMapping:
            return {key: self.resolve(child, key) for key, child in value._pairs}
        if type(value) is dict:
            return {key: self.resolve(child, key) for key, child in value.items()}
        if type(value) is _WitnessLinks:
            return self.witness_links(value.refs, value.result_ref)
        if type(value) is tuple:
            values = tuple(self.resolve(child) for child in value)
            if name in ('scope_refs', 'population_refs', 'basis_refs', 'check_refs', 'result_refs',
                    'affected_result_refs', 'available_result_refs', 'unavailable_result_refs',
                    'not_applicable_result_refs', 'not_evaluated_result_refs', 'reason_refs') and all(type(v) is str for v in values):
                return self.strings(values)
            return values
        return self.resolve_link(value)

    def capabilities(self):
        for cap in self.outcome.capabilities:
            self.port.charge(3)
            for check in cap.check_refs:
                self.check(check)
            for reason in cap.reason_refs:
                self.reason(reason)
            scopes = self.ordered(tuple(ref.scope for ref in cap.result_refs))
            self.add('capabilities', cap, _anchor(cap, self.port), {
                'diagnostic_id': cap.family,
                'inquiry_ref': _r._InputRef('inquiries', cap.inquiry_ref),
                'scope_refs': scopes, 'check_refs': self.ordered(cap.check_refs),
                'result_refs': self.ordered(cap.result_refs),
                'available_result_refs': self.ordered(cap.available_result_refs),
                'unavailable_result_refs': self.ordered(cap.unavailable_result_refs),
                'not_applicable_result_refs': self.ordered(cap.not_applicable_result_refs),
                'not_evaluated_result_refs': self.ordered(cap.not_evaluated_result_refs),
                'reason_refs': self.ordered(cap.reason_refs), 'scope_note': _SCOPE_NOTE})

    def domains(self):
        domains = []
        for index, label in _c.DOMAIN_LABELS:
            groups = {name: [] for name in ('available_result_refs', 'unavailable_result_refs',
                                           'not_evaluated_result_refs', 'reason_refs')}
            for domain in self.outcome.domains:
                self.port.charge(2)
                if domain.level_index != index:
                    continue
                for name, refs in (('available_result_refs', domain.available_result_refs),
                    ('unavailable_result_refs', domain.unavailable_result_refs),
                    ('not_evaluated_result_refs', domain.not_evaluated_result_refs),
                    ('reason_refs', domain.reason_refs)):
                    self.port.charge(len(refs) + 1)
                    groups[name].extend(refs)
            row = {'level_index': index, 'label': label}
            for name, refs in groups.items():
                row[name] = self.ordered(refs)
            domains.append(self.resolve(row))
        return tuple(domains)


def _graph_node(value, port):
    _require(type(value) is tuple and len(value) == 3 and value[0] == 'node')
    port.charge(4)
    return {'ref': value[1], 'kind': value[2]}


def _graph_edge(value, port):
    _require(type(value) is tuple and len(value) == 8 and value[0] == 'edge')
    port.charge(9)
    return {'source': _graph_node(value[1], port), 'target': _graph_node(value[2], port),
            'source_ref': value[4], 'predicate': value[5],
            'eligible': value[6], 'reason_codes': value[7]}


def _graph_component(payload, port):
    """Fixed witness representation, preserving every already retained slot."""
    _require(type(payload) is tuple and len(payload) == 9 and payload[0] == 'graph_witness')
    port.charge(16)
    material = dict(payload[7])
    result = {'type': 'graph_witness', 'kind': payload[1], 'member_count': payload[8]}
    for name in ('nodes', 'members', 'starts', 'examined_nodes', 'frontiers', 'terminals'):
        result[name] = tuple(_graph_node(value, port) for value in material[name])
    for name in ('edges', 'internal_edges', 'exit_edges', 'examined_edges', 'observations'):
        result[name] = tuple(_graph_edge(value, port) for value in material[name])
    result['target'] = None if material['target'] is None else _graph_node(material['target'], port)
    return result



def _selected_component(payload, port):
    _require(type(payload) is tuple and bool(payload))
    tag = payload[0]
    if tag == 'graph_witness':
        return _graph_component(payload, port)
    port.charge(len(payload) + 4)
    if tag in ('inventory_witness', 'selected_members'):
        _require(len(payload) == 3)
        return {'type': tag, 'members': payload[1], 'member_count': payload[2]}
    if tag == 'comparison_witness':
        _require(len(payload) == 5)
        return {'type': tag, 'assessment': payload[1], 'members': payload[2],
                'examined_assessments': payload[3], 'member_count': payload[4]}
    if tag == 'human_review_witness':
        _require(len(payload) == 5)
        return {'type': tag, 'members': payload[1], 'examined_assessments': payload[2],
                'source_refs': payload[3], 'member_count': payload[4]}
    _require(tag == 'correction_outcome_witness' and len(payload) == 4)
    return {'type': tag, 'members': payload[1], 'source_refs': payload[2], 'member_count': payload[3]}


def _check_finding_witness(finding, selected, assembly):
    port = assembly.port
    selected_refs = tuple(_as_input(ref, port) for ref in _field(selected, 'input_refs', port))
    _require(_ref_keys(selected_refs, port) == _ref_keys(finding.witness.input_refs, port))
    expected = tuple(_selected_component(payload, port) for payload in finding.witness.owner_witnesses)
    _require(_same(_field(selected, 'components', port), expected, assembly))


def _check_disclosure_sources(result, selected, assembly):
    port = assembly.port
    expected = [row.source for row in result.value.records]
    if result.ref.field_key == 'corrective_independence_disclosures':
        wanted = _ref_keys(result.witness_refs, port)
        for record in assembly.outcome.witnesses:
            if not any(_anchor(ref, port) in wanted for ref in record.refs):
                continue
            for payload in record.payload:
                if payload[0] == 'human_review_witness':
                    port.charge(len(payload[2]) + len(payload[3]) + 2)
                    expected.extend(payload[2])
                    expected.extend(payload[3])
    _require(len(selected) == len(expected))
    for row, source in zip(selected, expected):
        chosen = _field(row, 'source', port)
        if type(source) is _r._ResultRef:
            _require(type(chosen) is _r._ResultRef)
            left, right = _c._semantic_key(source, port), _c._semantic_key(chosen, port)
            _charge_key((left, right), port)
            _require(left == right)
        else:
            _require(_anchor(_as_input(chosen, port), port) == _anchor(source, port))

def _same(left, right, assembly):
    a, b = _j_key(assembly.semantic(left), assembly.port), _j_key(assembly.semantic(right), assembly.port)
    _byte_work(assembly.port, len(a) + len(b), 1)
    return a == b


def _ref_keys(refs, port):
    keys = []
    for ref in refs:
        key = _anchor(ref, port)
        _charge_key(key, port)
        keys.append(key)
    return _sort(keys, port)


def _related(record, outcome, port):
    keys = _ref_keys(record.refs, port)
    related = []
    for result in outcome.results:
        for ref in result.witness_refs:
            key = _anchor(ref, port)
            _charge_key((key, keys), port)
            if key in keys:
                port.charge(1)
                related.append(result)
                break
    _require(bool(related))
    return tuple(related)


def _scope_equal(left, right, assembly):
    port = assembly.port
    port.charge(3)
    if left is right:
        return True
    keys = []
    for scope in (left, right):
        token = id(scope)
        if token not in assembly.scope_keys:
            assembly.scope(scope)
            body = assembly.objects[token]['body']
            assembly.scope_keys[token] = (_anchor(scope, port), _j_key(assembly.semantic(body), port))
        key = assembly.scope_keys[token]
        _charge_key(key, port)
        keys.append(key)
    return keys[0] == keys[1]


def _component_matches_path(path, trace, assembly):
    """Membership check of existing proof material, never a graph search."""
    nodes, starts = path['nodes'], trace['starts']
    if not nodes or not starts or not any(_same(nodes[0], start, assembly) for start in starts):
        return False
    for edge in path['edges']:
        if not any(_same(edge, examined, assembly) for examined in trace['examined_edges']):
            return False
    return bool(path['edges'])


def _proof_metadata(component, view, port):
    port.charge(8)
    kind = component['kind']
    if kind == 'path':
        _require(bool(component['edges']) and all(edge['eligible'] is True for edge in component['edges']))
        _require(view in ('citation', 'material_transformation', 'claim_origin'))
        code = 'citation_path_witness' if view == 'citation' else 'transformation_path_witness'
        return code, 'positive_witness', ('SIT-TH002',), (
            'An eligible explicit path connects these exact endpoints in the named typed view.'), _PATH_LIMIT
    if kind == 'cycle':
        assurance = view == 'assertion_assurance'
        return ('assurance_loop_limitation' if assurance else 'view_cycle_witness',
            'qualification_gap' if assurance else 'positive_witness', ('SIT-TH005',),
            'A finite cycle is witnessed in this exact typed view within the requested start\'s reachable area.',
            'A cycle does not establish falsity, misconduct, absence of reality contact or represented benchmark feedback.')
    if kind == 'no_witness_in_examined_view':
        return 'scoped_no_witness', 'no_witness_in_examined_view', (), (
            'The completed typed search found no eligible witness between these endpoints in this examined supplied view.'), (
            'Examined nodes, predicates, observations and unknown frontiers remain in the finite witness. '
            'No outside-world independence or passed threat check follows.')
    raise _c._ReportContractError('invalid_report_contract')


def _proof_context(scope, port):
    key = _anchor(scope, port)
    # A retained proof may be represented at another operation/target Scope,
    # but never acquires another Inquiry, Claim, dimension or time context.
    port.charge(7)
    return key[1:3] + key[4:8]


def _assemble_witnesses(assembly):
    """Bind retained witnesses to their exact public homes and Finding IDs."""
    outcome, port = assembly.outcome, assembly.port
    selected_records, paths, consumed = [], [], {}
    for finding in outcome.findings:
        chosen = assembly.choose('finding', finding)
        components = _field(chosen, 'components', port)
        for component in components:
            if _field(component, 'type', port) == 'graph_witness':
                row = {name: child for name, child in component._pairs}
                if row['kind'] == 'path':
                    paths.append((row, _field(chosen, 'input_refs', port),
                        _proof_context(finding.scope_ref, port), finding.basis_refs))
    for record in outcome.witnesses:
        port.charge(len(record.refs) + 2)
        # Typed private links may retain another immutable instance of an
        # equal Scope. Register its complete body before identity resolution.
        for ref in record.refs:
            assembly.scope(ref.scope)
        related = _related(record, outcome, port)
        targets = []
        consumed[id(record)] = set()
        for finding in outcome.findings:
            if not any(_scope_equal(ref.scope, finding.scope_ref, assembly) for ref in record.refs):
                continue
            for index, payload in enumerate(record.payload):
                if any(_c._semantic_key(payload, port) == _c._semantic_key(part, port)
                       for part in finding.witness.owner_witnesses):
                    consumed[id(record)].add(index)
                    if not any(old is finding for old in targets):
                        targets.append(finding)
        graph = bool(record.payload) and all(part[0] == 'graph_witness' for part in record.payload)
        if graph:
            selected = assembly.choose('owner', record)
            components = _field(selected, 'components', port)
            _require(len(components) == len(record.payload))
            canonical = tuple(_graph_component(payload, port) for payload in record.payload)
            for component, actual in zip(components, canonical):
                _require(_same(component, actual, assembly))
            for component in canonical:
                if component['kind'] == 'path':
                    basis = []
                    for result in related:
                        port.charge(len(result.basis_refs) + 1)
                        basis.extend(result.basis_refs)
                    paths.append((component, _field(selected, 'input_refs', port),
                        _proof_context(record.refs[0].scope, port), tuple(basis)))
            if len(consumed[id(record)]) != len(record.payload):
                selected_records.append((record, related, selected, canonical, targets))
        else:
            _witness_home(record, related, assembly, consumed[id(record)])
        for ref in record.refs:
            key = _anchor(ref, port)
            _charge_key(key, port)
            port.charge(2)
            assembly.witness_targets[key] = list(targets)
    # Discovery order of independent witness records is not native array
    # order. Sort record groups, preserving each original payload tuple inside.
    ordered = []
    for index, row in enumerate(selected_records):
        record = row[0]
        key = (_anchor(record.refs[0].scope, port),
               _j_key(assembly.semantic(assembly.objects[id(record.refs[0].scope)]['body']), port),
               _j_key(assembly.semantic(row[3]), port))
        ordered.append((key, index))
    selected_records = [selected_records[index] for unused, index in _sort(ordered, port)]
    # One owner-scope proof can retain its complete trace alongside a concrete
    # already established path/cycle. It does not donate its scope to another job.
    groups = []
    for record, related, selected, components, targets in selected_records:
        scope = record.refs[0].scope
        _require(all(_scope_equal(scope, ref.scope, assembly) for ref in record.refs))
        group = None
        for old in groups:
            if _scope_equal(scope, old['scope'], assembly):
                group = old
                break
        if group is None:
            group = {'scope': scope, 'records': [], 'related': [], 'components': [], 'inputs': []}
            groups.append(group)
        port.charge(len(related) + len(components) + 5)
        group['records'].append(record)
        group['related'].extend(related)
        group['components'].extend(components)
        group['inputs'].extend(_field(selected, 'input_refs', port))
    for group in groups:
        scope, components = group['scope'], group['components']
        context = _proof_context(scope, port)
        primaries = [part for part in components if part['kind'] in ('path', 'cycle', 'no_witness_in_examined_view')]
        traces = [part for part in components if part['kind'] == 'complete_trace']
        _require(len(primaries) + len(traces) == len(components))
        for trace in traces:
            candidates = []
            for path, inputs, proof_context, proof_basis in paths:
                _charge_key((context, proof_context), port)
                if proof_context == context and _component_matches_path(path, trace, assembly):
                    candidates.append((path, inputs))
            if candidates:
                # All retained matching paths are kept; no newly searched or
                # manufactured path replaces an original owner's proof.
                for path, inputs in candidates:
                    if not any(_same(path, old, assembly) for old in primaries):
                        primaries.append(path)
                        group['inputs'].extend(inputs)
        if not primaries:
            continue
        for primary in primaries:
            code, observation, threats, statement, limit = _proof_metadata(primary, scope.graph_view, port)
            selected_components = [primary]
            for trace in traces:
                if primary['kind'] == 'path' and _component_matches_path(primary, trace, assembly):
                    selected_components.append(trace)
            supporting, related, input_rows = [], [], []
            for record in group['records']:
                selected = assembly.choose('owner', record)
                actual = tuple(_graph_component(payload, port) for payload in record.payload)
                contributes = any(_same(part, primary, assembly) or
                    (part['kind'] == 'complete_trace' and
                     primary['kind'] == 'path' and _component_matches_path(primary, part, assembly))
                    for part in actual)
                if contributes:
                    if any(_same(part, primary, assembly) for part in actual):
                        # Components retained by one exact owner keep their
                        # direct association; another Scope peer cannot add it.
                        selected_components.extend(part for part in actual if part['kind'] == 'complete_trace')
                    supporting.append(record)
                    related.extend(_related(record, outcome, port))
                    input_rows.extend(_field(selected, 'input_refs', port))
            _require(bool(supporting))
            selected_components = _dedup_components(selected_components, assembly)
            for record in supporting:
                for index, payload in enumerate(record.payload):
                    actual = _graph_component(payload, port)
                    if any(_same(actual, item, assembly) for item in selected_components):
                        consumed[id(record)].add(index)
            basis, families = [], []
            if primary['kind'] == 'path':
                for path, inputs, proof_context, proof_basis in paths:
                    _charge_key((context, proof_context), port)
                    if proof_context == context and _same(path, primary, assembly):
                        port.charge(len(proof_basis) + 1)
                        basis.extend(proof_basis)
            for result in related:
                port.charge(len(result.basis_refs) + 2)
                basis.extend(result.basis_refs)
                families.append(result.ref.diagnostic_id)
            inputs = assembly.ordered(tuple(_as_input(ref, port) for ref in input_rows))
            for ref in inputs:
                port.charge(2)
                basis.append(_r._BasisRef(ref))
            for ref in basis:
                assembly.basis(ref)
            body = {'observation_kind': observation, 'condition_code': code,
                'diagnostic_refs': assembly.strings(families), 'threat_family_refs': threats,
                'scope_ref': scope, 'population_refs': (), 'basis_refs': assembly.ordered(basis),
                'witness': {'input_refs': inputs, 'components': selected_components},
                'contrary_input_refs': (), 'reason_refs': (), 'statement': statement,
                'interpretation_limit': _FINDING_LIMIT + ' ' + limit}
            anchor = ('finding', code, observation, _anchor(scope, port),
                _sort([_anchor(ref, port) for ref in inputs], port))
            # The project-owned record is an identity handle only; allocation
            # order never enters the semantic key or emitted identifier.
            owner = object()
            assembly.add('findings', owner, anchor, body)
            for record in supporting:
                for ref in record.refs:
                    key = _anchor(ref, port)
                    _charge_key(key, port)
                    assembly.witness_targets[key].append(owner)


    # Require an actual public home for every retained component, including a
    # trace whose Scope also contains an unrelated record's primary witness.
    for record, related, selected, components, targets in selected_records:
        missing = tuple(part for index, part in enumerate(components)
                        if index not in consumed[id(record)])
        if missing:
            _require(all(part['kind'] == 'complete_trace' for part in missing))
            _trace_home({'scope': record.refs[0].scope, 'records': [record],
                         'components': missing}, assembly)
            consumed[id(record)].update(range(len(components)))
        _require(len(consumed[id(record)]) == len(components))


def _as_input(value, port):
    if type(value) is _r._InputRef:
        return value
    _require(type(value) in (dict, _c._ReportMapping))
    port.charge(6)
    fields = value if type(value) is dict else {key: child for key, child in value._pairs}
    _require(set(fields) == {'collection', 'identifier', 'selector'})
    return _r._InputRef(fields['collection'], fields['identifier'], fields['selector'])


def _dedup_components(components, assembly):
    result = []
    for component in components:
        if not any(_same(component, old, assembly) for old in result):
            result.append(component)
    assembly.port.charge(len(result) + 1)
    return tuple(result)


def _material_refs(value, port):
    """Visit only the known detached witness tuple grammar."""
    refs, pending = [], [value]
    while pending:
        port.charge(1)
        current = pending.pop()
        if type(current) is _r._InputRef:
            refs.append(current)
        elif type(current) is tuple:
            port.charge(len(current) + 1)
            pending.extend(current)
    return tuple(refs)


def _witness_home(record, related, assembly, represented=()):
    """Owner material has explicit homes, without inventing carrier Findings."""
    port = assembly.port
    allowed = ('inventory_witness', 'comparison_witness', 'selected_members',
               'human_review_witness', 'correction_outcome_witness')
    for payload in record.payload:
        _require(type(payload) is tuple and payload and payload[0] in allowed)
    homes = []
    for result in related:
        for population in result.population_refs:
            homes.extend(member for member in population.member_refs if type(member) is _r._InputRef)
        for basis in result.basis_refs:
            homes.append(basis.source)
        for check in result.check_refs:
            homes.extend(check.input_refs)
        for reason in result.reason_refs:
            homes.extend(reason.input_refs)
        homes.append(result.ref.scope.inquiry_ref)
        if result.result_state == 'available' and result.value_kind == 'record_disclosures':
            selected = assembly.choose('disclosure', result.ref)
            for row in _field(selected, 'records', port):
                homes.append(_as_input(_field(row, 'source', port), port))
    keys = _ref_keys(homes, port)
    for index, payload in enumerate(record.payload):
        port.charge(2)
        # These indices come from exact same-Scope matches to owner components
        # in Findings whose selected witnesses were already checked in finding().
        # Their ordered source slots have that concrete public home, including
        # nullable correction-case fields absent from a Result's root references.
        if index in represented:
            continue
        for ref in _material_refs((payload,), port):
            key = _anchor(ref, port)
            _charge_key((key, keys), port)
            _require(key in keys)


def _trace_home(group, assembly):
    """A trace without a concrete witness must remain in a scoped finding."""
    port = assembly.port
    for record in group['records']:
        matches = []
        for finding in assembly.outcome.findings:
            if not _scope_equal(group['scope'], finding.scope_ref, assembly):
                continue
            related = _related(record, assembly.outcome, port)
            result_keys = _ref_keys(tuple(result.ref for result in related), port)
            if any(_anchor(ref, port) in result_keys for ref in finding.result_refs):
                matches.append(finding)
        _require(bool(matches))
        for finding in matches:
            row = assembly.objects[id(finding)]
            chosen = row['body']['witness']
            components = chosen['components'] if type(chosen) is dict else _field(chosen, 'components', port)
            original_inputs = chosen['input_refs'] if type(chosen) is dict else _field(chosen, 'input_refs', port)
            selected = assembly.choose('owner', record)
            inputs = tuple(_as_input(ref, port) for ref in original_inputs) + tuple(
                _as_input(ref, port) for ref in _field(selected, 'input_refs', port))
            row['body']['witness'] = {'input_refs': assembly.ordered(inputs),
                'components': _dedup_components(list(components) +
                    list(group['components']), assembly)}
        for ref in record.refs:
            key = _anchor(ref, port)
            _charge_key(key, port)
            assembly.witness_targets[key].extend(matches)



def _document_values(value, port):
    port.charge(1)
    if type(value) is dict:
        return {name: _document_values(child, port) for name, child in value.items()}
    if type(value) is tuple:
        return [_document_values(child, port) for child in value]
    _require(value is None or type(value) in (str, bool, int))
    if type(value) is str:
        _byte_work(port, 4 * len(value), 1)
    return value


def _identity(prepared, port):
    qualification = ('In-process input has no raw file digest; no canonical object fingerprint is invented.',)
    if prepared is None:
        return {'source_mode': 'in_process', 'input_contract_version': None,
            'bundle_id': None, 'snapshot_id': None, 'declared_predecessor': None,
            'raw_file_digest': None, 'qualifications': qualification + (
                'Input identifiers were not retained as accepted metadata.',)}
    _require(type(prepared) is _PreparedBundle and prepared.source_mode == 'constructed_value')
    metadata = prepared.tree
    return {'source_mode': 'in_process',
        'input_contract_version': _field(prepared.tree, 'contract_version', port),
        'bundle_id': _field(metadata, 'bundle_id', port),
        'snapshot_id': _field(metadata, 'snapshot_id', port),
        'declared_predecessor': _plain(_field(metadata, 'predecessor', port), port),
        'raw_file_digest': None, 'qualifications': qualification}


def _run(state, completed, diagnostics, tool_version):
    _require(type(tool_version) is str and tool_version == '0.1.0.dev0')
    unknown = {'state': 'unknown', 'value': None, 'precision': None,
               'reason': 'not_recorded_by_SIT-RP-0.1'}
    return {'processing_state': state, 'tool_name': 'Source Integrity Toolkit',
        'tool_version': tool_version, 'input_contract_version': 'sit-bundle/0.1',
        'requested_diagnostic_ids': _c.FAMILIES, 'completed_diagnostic_ids': completed,
        'started_at': unknown, 'finished_at': unknown, 'diagnostics': diagnostics,
        'qualifications': _c._REPORT_RUN_QUALIFICATIONS}


def _assemble_report(outcome, selection, port, *, tool_version='0.1.0.dev0'):
    """Assemble one logical envelope under the supplied current invocation port."""
    port.check()
    port.charge(14)
    _require(type(outcome) is _c._AnalyticalOutcome)
    _c._validate_selected_report_disclosure(selection, port)
    assembly = _Assembly(outcome, selection, port)
    for result in outcome.results:
        assembly.result(result)
    for finding in outcome.findings:
        assembly.finding(finding)
    assembly.capabilities()
    _assemble_witnesses(assembly)
    _require(assembly.used == set(assembly.selected))
    assembly.identities_for_rows()
    document = {'contract_version': 'sit-report/0.1', 'report_kind': 'audit_report',
        'report_id': 'SIT-RPT-000001', 'input_identity': _identity(outcome.prepared, port),
        'input_validation': {'state': 'accepted', 'diagnostics': ()},
        'release_limits': _c._REPORT_RELEASE_LIMITS}
    completed = []
    for family in _c.FAMILIES:
        selected = [result for result in outcome.results if result.ref.diagnostic_id == family]
        port.charge(len(outcome.results) + len(selected) + 1)
        if selected and all(result.execution_state == 'completed' for result in selected):
            completed.append(family)
    diagnostics = ()
    if outcome.execution_state == 'interrupted':
        diagnostics = ({'code': 'resource_limit_reached', 'location': None,
            'safe_message': 'Analytical processing stopped at a fixed resource limit.', 'qualifications': ()},)
    document['run'] = _run(outcome.execution_state, tuple(completed), diagnostics, tool_version)
    for kind, unused in _PREFIXES:
        rows = []
        for row in assembly.rows[kind]:
            body = assembly.resolve(row['body'])
            body['id'] = assembly.resolve_link(row['owner'])
            rows.append(body)
        document[kind] = tuple(rows)
    document['observability_domains'] = assembly.domains()
    frozen = _c._freeze_report_document(_document_values(document, port), port)
    _c._validate_report_references(frozen, outcome.prepared, port)
    port.check()
    return frozen


def _assemble_diagnostic(stopped, port, *, prepared=None, tool_version='0.1.0.dev0'):
    """Safe empty analytical arrays; partial source material is never projected."""
    port.check()
    port.charge(24)
    _require(type(stopped) in (_PreparationAborted, _AnalysisAborted))
    stop = stopped.stop
    _require(prepared is None or (stop.input_state == 'accepted' and type(prepared) is _PreparedBundle))
    rejected = stop.execution_state == 'rejected'
    code = stopped.diagnostic_code if rejected else stop.reason_code
    qualifications = ()
    if rejected and stopped.constraint is not None:
        qualifications = (stopped.constraint,)
    diagnostic = {'code': code, 'location': None,
        'safe_message': 'Input was not accepted.' if rejected else 'Audit processing did not complete.',
        'qualifications': qualifications}
    document = {'contract_version': 'sit-report/0.1',
        'report_kind': 'validation_diagnostics' if rejected else 'processing_diagnostics',
        'report_id': 'SIT-RPT-000001',
        'run': _run(stop.execution_state, (), () if rejected else (diagnostic,), tool_version),
        'input_identity': _identity(prepared, port),
        'input_validation': {'state': stop.input_state, 'diagnostics': (diagnostic,) if rejected else ()},
        'observability_domains': (), 'release_limits': _c._REPORT_RELEASE_LIMITS}
    for name, unused in _PREFIXES:
        document[name] = ()
    document['reasons'] = ({'id': 'SIT-RSN-000001', 'code': stop.reason_code,
        'scope_ref': None, 'affected_result_refs': (), 'input_refs': (),
        'detail': 'The invocation did not produce an ordinary analytical report.',
        'classification': 'execution'},)
    frozen = _c._freeze_report_document(_document_values(document, port), port)
    _c._validate_report_references(frozen, prepared, port)
    port.check()
    return frozen
