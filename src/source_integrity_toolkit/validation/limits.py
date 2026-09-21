# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: RUNTIME_BOUNDARY.

WU9-L01-L10 counting primitives only. The future capture/validator must call
these for every occurrence, including extensions and unselected records.
Testing a ledger threshold does not certify an absent parser's integration.
The separate analytical witness ledger activates WU9-L13. _InputLedger and
its historical _DEFERRED table retain their preparation-only meaning; encoded
report accounting remains deferred.
"""
from dataclasses import dataclass, field
from ..contracts.execution import _BudgetPort
from ..contracts.bundle import _string_lengths

_AGGREGATES = (
    ("bytes", 16_777_216, "WU9-L01"),
    ("inquiries", 32, "WU9-L03"),
    ("records", 10_000, "WU9-L04"),
    ("assertions", 30_000, "WU9-L05"),
    ("evidence_references", 10_000, "WU9-L06"),
    ("reference_occurrences", 200_000, "WU9-L07"),
    ("nodes", 500_000, "WU9-L08"),
)
_DEFERRED = (
    ("analytical_scope_work", 1_000_000, "WU9-L11"),
    ("witnesses", 20_000, "WU9-L13"),
    ("witness_members", 100_000, "WU9-L13"),
    ("report_representation_bytes", 67_108_864, "WU9-L14"),
)


@dataclass(slots=True, repr=False, eq=False)
class _InputLedger:
    """Private context: port and source mode are fixed by project orchestration.

    source_mode determines whether bytes count raw supplied input or compact J;
    it is not discovered from untrusted keys. No counter reset/refund exists.
    All mutable storage holds counts, never source text or a captured object.
    """
    port: _BudgetPort
    source_mode: str
    _counts: list = field(default_factory=list, init=False)
    _peak_depth: int = field(default=0, init=False)

    def __post_init__(self) -> None:
        self.port.charge(8)
        if type(self.source_mode) is not str or self.source_mode not in ("supplied_utf8", "constructed_value"):
            self.port.reject("type_or_enum_violation")
        self._counts = [0] * len(_AGGREGATES)
        self.port.check()

    def _index(self, name: str) -> int:
        self.port.charge(1)
        if type(name) is not str:
            raise TypeError("invalid_private_counter")
        # Fixed maximum name length is an internal argument contract, not a
        # source field restriction. No comparison against an unbounded key.
        if len(name) > 32:
            raise TypeError("invalid_private_counter")
        for i in range(len(_AGGREGATES)):
            self.port.charge(2)
            if name == _AGGREGATES[i][0]:
                return i
        raise TypeError("invalid_private_counter")

    def add(self, name: str, amount: int = 1) -> None:
        i = self._index(name)
        if type(amount) is not int or amount < 0:
            raise TypeError("invalid_private_counter")
        _, ceiling, limit = _AGGREGATES[i]
        if amount > ceiling - self._counts[i]:
            self.port.interrupt(limit)
        self.port.charge(1)
        self._counts[i] += amount
        self.port.check()

    def depth(self, level: int) -> None:
        self.port.charge(1)
        if type(level) is not int or level < 1:
            raise TypeError("invalid_private_depth")
        if level > 32:
            self.port.interrupt("WU9-L02")
        self._peak_depth = max(self._peak_depth, level)
        self.port.check()

    def snapshot(self) -> tuple:
        self.port.charge(len(_AGGREGATES) + 1)
        result = tuple(self._counts) + (self._peak_depth,)
        self.port.check()
        return result

    def field_bytes(self, value: object, *, locator: bool = False,
                    identifier: bool = False) -> tuple[int, int]:
        return _string_lengths(value, self.port, locator=locator, identifier=identifier)

    def children_fit(self, count: int) -> None:
        """Prospective lower bound, not a second count or an allocation permit.

        Used before enumerating a caller container. Actual occurrences are still
        counted when visited; the same alias therefore consumes its full size.
        """
        i = self._index("nodes")
        if type(count) is not int or count < 0:
            raise TypeError("invalid_private_counter")
        if count > _AGGREGATES[i][1] - self._counts[i]:
            self.port.interrupt("WU9-L08")
        self.port.check()


@dataclass(frozen=True, slots=True, repr=False, eq=False)
class _WitnessReservation:
    """Opaque project-owned count reservation; contains no evidence payload."""
    _owner: object
    _serial: int
    _witnesses: int
    _members: int


@dataclass(slots=True, repr=False, eq=False)
class _WitnessLedger:
    """One invocation's pending and retained WU9-L13 occurrences.

    Reservation does not establish witness validity or a completed result.
    The owner shares this ledger across jobs. Already retained Finding reuse
    reserves zero new witnesses; every additional member occurrence still counts.
    Payload traversal/qualification is separately charged by the semantic owner.
    Retained occurrences cannot be refunded to hide later contradictory work.
    """
    port: _BudgetPort
    _reserved_witnesses: int = field(default=0, init=False)
    _reserved_members: int = field(default=0, init=False)
    _retained_witnesses: int = field(default=0, init=False)
    _retained_members: int = field(default=0, init=False)
    _serial: int = field(default=0, init=False)
    _pending: dict = field(default_factory=dict, init=False)

    def reserve(self, witnesses: int = 0, members: int = 0) -> _WitnessReservation:
        self.port.check()
        if (type(witnesses) is not int or type(members) is not int or
                witnesses < 0 or members < 0 or (witnesses == 0 and members == 0)):
            raise TypeError("invalid_private_counter") from None
        if (witnesses > 20_000 - self._reserved_witnesses - self._retained_witnesses or
                members > 100_000 - self._reserved_members - self._retained_members):
            self.port.interrupt("WU9-L13")
        # Fixed administrative entries; witness payload visits are not prepaid.
        self.port.charge(4)
        token = _WitnessReservation(self, self._serial, witnesses, members)
        self._pending[self._serial] = token
        self._serial += 1
        self._reserved_witnesses += witnesses
        self._reserved_members += members
        return token

    def _reservation(self, token: object) -> _WitnessReservation:
        self.port.check()
        if (type(token) is not _WitnessReservation or token._owner is not self or
                type(token._serial) is not int or not 0 <= token._serial < self._serial or
                self._pending.get(token._serial) is not token):
            raise TypeError("invalid_private_reservation") from None
        return token

    def retain(self, token: object) -> None:
        item = self._reservation(token)
        # Each retained occurrence receives its own prospective entry charge.
        self.port.charge(1 + item._witnesses + item._members)
        self._reserved_witnesses -= item._witnesses
        self._reserved_members -= item._members
        self._retained_witnesses += item._witnesses
        self._retained_members += item._members
        del self._pending[item._serial]

    def release(self, token: object) -> None:
        item = self._reservation(token)
        self.port.charge(1)
        self._reserved_witnesses -= item._witnesses
        self._reserved_members -= item._members
        del self._pending[item._serial]

    def snapshot(self) -> tuple:
        self.port.charge(5)
        return (self._reserved_witnesses, self._reserved_members,
                self._retained_witnesses, self._retained_members)
