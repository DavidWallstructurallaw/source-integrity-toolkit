# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: INGESTION_CONTRACT.

Private immutable representation vocabulary, not an ingestion interface.
Construction requires already bounded project-owned parts. Constructors check
local representation invariants only; they neither parse/coerce caller objects
nor establish structural acceptance. W03 owns exact-number conversion and J;
W04/W05 own bounded capture and full validation. Hostile same-process mutation
of Python objects is outside the immutability claim.

Numbers retain their source category after coefficient normalization so a
future field validator can keep lexical-type requirements. Optional absence is
an absent object pair, distinct from a present pair whose value is None.
"""
from dataclasses import dataclass


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
    # Exact types prevent overloaded equality, hashing and conversion callbacks.
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
