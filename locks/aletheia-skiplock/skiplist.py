"""Deterministic skip search. Empty list or a missing key is absence, not 0."""
from __future__ import annotations


def skip_search(vals: list[int], t: int) -> int:
    if not vals:
        raise ValueError("empty list is absence")
    i = 0
    n = len(vals)
    step = 1
    while step * 2 < n:
        step *= 2
    while step:
        while i + step < n and vals[i + step] <= t:
            i += step
        step //= 2
    if vals[i] != t:
        raise ValueError("missing key is absence")
    return i
