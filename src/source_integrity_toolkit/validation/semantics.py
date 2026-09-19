# Copyright 2026 Xiangyu Guo
# SPDX-License-Identifier: Apache-2.0
"""Owner: TEMPORAL_CONTRACT; supporting EVIDENCE_BASIS.

W05 input-only time validation under lineage section 3.1. No local timezone,
grant eligibility, event causality or conflict adjudication. Date precision is
retained as a date, never replaced by an assumed midnight instant. Mixed date /
instant window boundaries remain for their later owning analytical operation.
"""
from ..contracts.evidence import _InputObservation
from ..contracts.execution import _byte_work
from ..contracts.bundle import _compare_text
from .structure import _field


def _digits(text, start, stop, port):
    value = 0
    for i in range(start, stop):
        port.charge(2)
        ch = text[i]
        if not "0" <= ch <= "9":
            port.reject("invalid_time")
        value = value * 10 + ord(ch) - 48
    return value


def _date(text, port):
    port.charge(2)
    if len(text) < 10 or text[4] != "-" or text[7] != "-":
        port.reject("invalid_time")
    year, month, day = _digits(text, 0, 4, port), _digits(text, 5, 7, port), _digits(text, 8, 10, port)
    leap = year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)
    months = (31, 29 if leap else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
    if not 1 <= year <= 9999 or not 1 <= month <= 12 or not 1 <= day <= months[month - 1]:
        port.reject("invalid_time")
    prior = year - 1
    port.charge(25)
    ordinal = 365 * prior + prior // 4 - prior // 100 + prior // 400 + sum(months[:month - 1]) + day
    return ordinal


def _time_value(obj, port):
    state, text, precision = _field(obj, "state", port), _field(obj, "value", port), _field(obj, "precision", port)
    if state != "known":
        reason = _field(obj, "reason", port)
        if text is not None or precision is not None or type(reason) is not str or not reason:
            port.reject("invalid_time")
        return None
    if type(text) is not str or precision not in ("date", "instant"):
        port.reject("invalid_time")
    day = _date(text, port)
    if precision == "date":
        if len(text) != 10:
            port.reject("invalid_time")
        return ("date", day, "")
    if len(text) < 20 or text[10] != "T" or text[13] != ":" or text[16] != ":":
        port.reject("invalid_time")
    hour, minute, second = _digits(text, 11, 13, port), _digits(text, 14, 16, port), _digits(text, 17, 19, port)
    if hour > 23 or minute > 59 or second > 59:
        port.reject("invalid_time")
    i, fraction = 19, ""
    if text[i] == ".":
        i += 1
        start = i
        while i < len(text) and "0" <= text[i] <= "9":
            port.charge(2)
            i += 1
        if start == i:
            port.reject("invalid_time")
        end = i
        while end > start and text[end - 1] == "0":
            port.charge(2)
            end -= 1
        _byte_work(port, end - start, 1)
        fraction = text[start:end]
    offset = 0
    if i < len(text) and text[i] == "Z" and i + 1 == len(text):
        pass
    elif i + 6 == len(text) and text[i] in "+-" and text[i + 3] == ":":
        hours, minutes = _digits(text, i + 1, i + 3, port), _digits(text, i + 4, i + 6, port)
        if hours > 23 or minutes > 59:
            port.reject("invalid_time")
        offset = (hours * 3600 + minutes * 60) * (-1 if text[i] == "-" else 1)
    else:
        port.reject("invalid_time")
    port.charge(5)
    return ("instant", day * 86400 + hour * 3600 + minute * 60 + second - offset, fraction)


def _validate_semantics(occurrences, port):
    observations = []
    for shape, obj, owner, collection, prefix in occurrences:
        port.charge(1)
        if shape == "TimeValue":
            _time_value(obj, port)
        elif shape == "TimeWindow":
            start = _time_value(_field(obj, "start", port), port)
            end = _time_value(_field(obj, "end", port), port)
            # Only a same-precision, fully known inversion is observed. It is
            # accepted source data, not a structural failure or grant verdict.
            if start is not None and end is not None and start[0] == end[0]:
                port.charge(2)
                reverse = start[1] > end[1] or (start[1] == end[1] and _compare_text(start[2], end[2], port) > 0)
                if reverse:
                    identifier = _field(owner, "bundle_id" if collection == "bundle" else "id", port)
                    port.charge(3)
                    observations.append(_InputObservation("known_window_reversed", collection, identifier, prefix))
    port.charge(len(observations) + 1)
    result = tuple(observations)
    port.check()
    return result
